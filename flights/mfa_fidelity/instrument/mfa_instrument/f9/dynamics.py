"""mfa_instrument/f9/dynamics.py — Flight 9 module M2 (rule half): the hazard rule with a per-cell
index, one run of it, and the run's record (Contract F9 v0.7 §2.1–§2.11, §5.1).

THE RULE (§2.4; cell i of the L×L periodic Moore lattice, x_i ∈ {0, 1}, Δt = 1):
    inactive → active:   1 − exp(−[η_floor + g·λ_i·d_i(t)]·Δt)
    active → inactive:   1 − exp(−μ·Δt)
d_i(t) is the active fraction of the eight Moore neighbours at t (§2.3). No other term. The floor is not
gated by any base, and floor-generated events are not masked out of density.

TIMING (§2.5). Synchronous two-phase advance: every probability is read from the state at t; one
full-grid uniform is drawn (one uniform per cell per tick, from the run's own stream); all cells advance
together. The uniform decides both directions: an inactive cell activates iff u < P_act; an active cell
stays active iff u >= q.

OBJECTS AND STARTS (§2.6, §5.8).
  realization, stationary_floor — η_floor = η₀; each cell active at t = 0 with probability
        π₁ = a/(a + q), a = 1 − exp(−η₀Δt), decided by the run stream's FIRST full-grid uniform.
  skeleton, all_active          — η_floor = 0; every cell active at t = 0; nothing is drawn for the start.
  skeleton, low (T0 only)       — η_floor = 0; exactly round(N·0.02) = 200 cells active, chosen without
        replacement by the initialization-pattern stream.
At η_floor = 0 the all-inactive state is exactly absorbing. An extinct skeleton stops advancing and stops
drawing; its remaining counts and tail states are exactly zero. Extinction is a valid observation.

WHERE λ AND g COME FROM. A run takes its index array and its g_spec from an `ArmContext`, built from an
identity bundle of module M1: the index is composed from the bundle's STORED base arrays (no terrain
formula is evaluated here), its hash must be the one the identity record states for the arm, and g_spec
and spr are the record's. The gain is g = κ·g_spec (§2.8). The context does not establish that the
bundle is the canonical one or that it was verified: that is the caller's (`identities.verify_bundle_deep`)
and the runner's.

THE RECORD OF A RUN (§5.1, §2.11).
  counts[t], t = 0..T        — the global active count; counts[0] is the state after initialization.
  extinction_tick            — skeleton only: the first t with zero active cells; otherwise None.
  survival                   — active count > 0 at every tail tick (§5.4).
  per W in {1, 10, 100}, per cell: A (active windows), R0 (observed inactive segments), and the first and
        last window states. Windows are non-overlapping complete blocks aligned to the first tail tick;
        a window is active if the cell is active at any tick in it. At W = 1, A is the cell's count of
        active tail ticks, which is what the evaluator's occupancy estimate uses (§5.5 step 1).
The statistic of §2.11 and every report are other modules'. Nothing here adjudicates anything.

SERIALIZATION. `serialize_run` gives one byte string: an 8-byte magic, a 4-byte little-endian header
length, the header as canonical JSON, then the arrays in a fixed order (counts as int32; A and R0 as
uint16; first and last packed to bits; all little-endian, C order). The writing machine's η₀ and q are
not serialized: the floor is stated by its probability literal and rule, the deactivation by μ. The
header does carry the arm's spr and g_spec as the identity record states them, and g = κ·g_spec; g_spec
derives from the identity record's q, which passed through exp on the machine that built the bundle.

WHAT VALIDATES A RECORD. Three different things, kept apart:
  `parse_run`      — form (exact JSON types, canonical bytes, lengths), this instrument's declarations,
                     each array against its stated hash, and NECESSARY relations between the stored
                     quantities: relations every record of the rule satisfies whatever its trajectory
                     (`_check_consistency` lists them). A record that passes is not thereby a trajectory
                     of the rule: the relations are necessary, not sufficient.
  `replay_equals`  — reruns the record's own run on this machine with a given arm context and requires
                     the same bytes. On the writing machine a record is established by replay.
  authentication   — that the arm context is the verified canonical bundle's, and that the record is the
                     one a job of record wrote: the runner's. Nothing here establishes it.

REDUCTION (§5.1). `reduction_check` compares `step` with a constant index against the placed Flight 8
scalar step at equal state, effective gain, floor, μ, timing and uniforms, array for array.

PLATFORM. The activation probability passes through exp. Two platforms can differ in its last place, so
a trajectory is reproducible on one machine and environment and is not claimed bit for bit across
platforms. The runs of record are the canonical machine's.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import struct
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import numpy as np

from ..dynamics import _moore_sum_a
from . import config as C
from . import identities as I
from . import spectral as S
from . import streams as R
from . import terrain as T
from .config import F9ConfigError

RUN_MAGIC = b"F9RUN\x00\x01\n"
RUN_TYPE = "F9RunRecord"
RUN_SCHEMA = 1
REDUCTION_STREAM = (9, 5, 1)                          # apparatus stream of `reduction_check`: no master, no run key (keys have seven elements)


class F9DynamicsError(RuntimeError):
    """The stepper or the run record was asked for something the frozen rule does not define."""


# ======================= the rule =======================
def local_density(x: np.ndarray) -> np.ndarray:
    """d_i = (active Moore neighbours of i)/8, periodic, in the frozen package's accumulation order (§2.3)."""
    return _moore_sum_a(x.astype(np.float64)) / 8.0


def activation_probability(eta_floor: float, g: float, lam: np.ndarray, d: np.ndarray, dt: int = C.F9_DT) -> np.ndarray:
    """1 − exp(−[η_floor + g·λ_i·d_i]·Δt), in the contract's written form, float64 (§2.4)."""
    return 1.0 - np.exp(-(eta_floor + g * lam * d) * dt)


def stationary_pi1(eta_floor: float, mu: float = C.F9_MU, dt: int = C.F9_DT) -> float:
    """π₁ = a/(a + q): the floor-only stationary occupancy (§5.2)."""
    a = 1.0 - math.exp(-eta_floor * dt); q = C.q_deact(mu, dt)
    return a / (a + q) if (a + q) > 0 else 0.0


def step(x: np.ndarray, u: np.ndarray, *, eta_floor: float, g: float, lam: np.ndarray, mu: float = C.F9_MU, dt: int = C.F9_DT) -> np.ndarray:
    """One synchronous tick from state x with the full-grid uniform u (§2.4, §2.5)."""
    p_act = activation_probability(eta_floor, g, lam, local_density(x), dt)
    return np.where(x, u >= C.q_deact(mu, dt), u < p_act)


# ======================= the arm =======================
@dataclass(frozen=True, eq=False)
class ArmContext:
    """What a run needs from the identity bundle for one arm (see WHERE λ AND g COME FROM)."""
    terrain: str
    composition: str
    lam: np.ndarray                 # the raw index λ^X, float64 (L, L), read-only
    index_sha256: str
    spr: float
    g_spec: float
    identity_record_sha256: str


def arm_context(record: Dict[str, object], arrays: Dict[str, np.ndarray], terrain: str, composition: str) -> ArmContext:
    """The arm's context from a loaded identity bundle (`identities.load_bundle` or `verify_bundle_deep` + `load_bundle`)."""
    if (terrain, composition) not in C.F9_ARMS: raise F9ConfigError(f"not a declared arm: {terrain!r}.{composition!r}")
    try:
        entry = record["arms"][f"{terrain}.{composition}"]
        v, u, r = (arrays[f"bases/{terrain}.{b}.f64"] for b in ("v", "u", "r"))
        stated, spr, g_spec, q = entry["index_sha256"], entry["spr"], entry["g_spec"], record["q"]
    except (KeyError, TypeError):
        raise F9ConfigError("the identity bundle does not carry this arm")
    lam = np.ascontiguousarray(T.compose(composition, v, u, r), dtype=np.float64)
    if lam.shape != (C.F9_GRID, C.F9_GRID) or T.array_sha256(lam) != stated:
        raise F9ConfigError(f"{terrain}.{composition}: the index composed from the stored bases is not the one the identity record states")
    if not all(type(z) is float for z in (spr, g_spec, q)) or not (spr > 0.0) or g_spec != q / (C.F9_DT * spr):
        raise F9ConfigError(f"{terrain}.{composition}: the record's g_spec does not follow from its q and spr")
    if not float(lam.min()) > 0.0: raise F9ConfigError(f"{terrain}.{composition}: the index is not strictly positive")
    lam.setflags(write=False)
    return ArmContext(terrain, composition, lam, stated, spr, g_spec, I.record_identity(record))


# ======================= the run =======================
@dataclass(frozen=True)
class F9RunSpec:
    master: int
    terrain: str
    composition: str
    obj: str
    init: str
    level_micro: int
    seed_index: int

    def check(self) -> "F9RunSpec":
        R.check_run_identity(self.master, self.terrain, self.composition, self.obj, self.init, self.level_micro, self.seed_index)
        return self

    @property
    def stream_key(self) -> Tuple[int, ...]:
        return R.stream_key(self.master, self.terrain, self.composition, self.obj, self.init, self.level_micro, self.seed_index)

    @property
    def eta_floor(self) -> float:
        self.check()
        return C.F9_ETA0 if self.obj == "realization" else 0.0


def initial_state(spec: F9RunSpec, gen: np.random.Generator) -> np.ndarray:
    """The state at t = 0 (see OBJECTS AND STARTS). `gen` is the run's tick stream; only the stationary start draws from it."""
    spec.check()
    L, n = C.F9_GRID, C.F9_N_CELLS
    if spec.init == "all_active":
        return np.ones((L, L), dtype=bool)
    if spec.init == "low":
        k = int(round(n * R.RHO0_LOW_MICRO / C.MICRO_UNITS))
        idx = R.init_pattern_generator(spec.stream_key).choice(n, size=k, replace=False)
        x = np.zeros(n, dtype=bool); x[idx] = True
        return x.reshape(L, L)
    if spec.init == "stationary_floor":
        return gen.random((L, L)) < stationary_pi1(spec.eta_floor)
    raise F9DynamicsError(f"no initialization defined for {spec.init!r}")


class _Windows:
    """The §2.11 record at one window width W, accumulated tick by tick over the tail."""

    def __init__(self, W: int, L: int):
        self.W = W; self.n = 0; self._k = 0
        self._cur = np.zeros((L, L), dtype=bool); self._prev = np.zeros((L, L), dtype=bool)
        self.A = np.zeros((L, L), dtype=np.int64); self.R0 = np.zeros((L, L), dtype=np.int64)
        self.first = np.zeros((L, L), dtype=bool); self.last = np.zeros((L, L), dtype=bool)

    def add(self, x: np.ndarray) -> None:
        self._cur |= x; self._k += 1
        if self._k < self.W: return
        cur = self._cur
        self.A += cur
        if self.n == 0:
            self.first = cur.copy(); self.R0 += ~cur          # an inactive first window opens a segment
        else:
            self.R0 += (~cur) & self._prev                    # a segment opens where an active window is followed by an inactive one
        self._prev = cur; self.last = cur
        self._cur = np.zeros_like(cur); self._k = 0; self.n += 1


@dataclass(frozen=True, eq=False)
class F9RunResult:
    spec: F9RunSpec
    arm: ArmContext
    g: float
    counts: np.ndarray                                  # int64, length T + 1
    extinction_tick: Optional[int]
    ticks_advanced: int
    draws_consumed: int                                 # full-grid uniforms taken from the tick stream (the stationary start's included)
    survival: bool
    windows: Dict[int, Dict[str, np.ndarray]]           # W -> {"A", "R0" (int64), "first", "last" (bool)}

    @property
    def tail_active_sum(self) -> int:
        return int(self.counts[C.F9_TICKS - C.F9_TAIL_TICKS + 1:].sum())


def run(spec: F9RunSpec, arm: ArmContext) -> F9RunResult:
    """Execute one run of the frozen rule. Adjudicates nothing."""
    spec.check()
    R.verify_stream_declaration()
    if not isinstance(arm, ArmContext) or (arm.terrain, arm.composition) != (spec.terrain, spec.composition):
        raise F9ConfigError("the arm context is not this run's arm")
    L, T_, tail = C.F9_GRID, C.F9_TICKS, C.F9_TAIL_TICKS
    eta = spec.eta_floor
    g = S.gain(spec.level_micro, arm.g_spec)
    gen = R.generator_from_key(spec.stream_key)
    x = initial_state(spec, gen)
    draws = 1 if spec.init == "stationary_floor" else 0
    counts = np.zeros(T_ + 1, dtype=np.int64); counts[0] = int(np.count_nonzero(x))
    absorbing = eta == 0.0
    extinction: Optional[int] = 0 if (absorbing and counts[0] == 0) else None
    advanced = 0
    wins = {W: _Windows(W, L) for W in C.F9_FLICKER_WINDOWS}
    for t in range(1, T_ + 1):
        if extinction is None:
            u = gen.random((L, L)); draws += 1
            x = step(x, u, eta_floor=eta, g=g, lam=arm.lam)
            advanced = t
            counts[t] = int(np.count_nonzero(x))
            if absorbing and counts[t] == 0: extinction = t
        if t > T_ - tail:
            for w in wins.values(): w.add(x)                # after extinction x is all-inactive and stays so
    for w in wins.values():
        if w.n * w.W != tail: raise F9DynamicsError("a window width does not divide the tail")
    survival = bool((counts[T_ - tail + 1:] > 0).all())
    windows = {W: {"A": w.A, "R0": w.R0, "first": w.first, "last": w.last} for W, w in wins.items()}
    return F9RunResult(spec, arm, g, counts, extinction, advanced, draws, survival, windows)


# ======================= the record =======================
def _array_blobs(res: F9RunResult) -> Tuple[Tuple[str, bytes], ...]:
    out = [("counts", np.ascontiguousarray(res.counts, dtype="<i4").tobytes())]
    for W in C.F9_FLICKER_WINDOWS:
        w = res.windows[W]
        out.append((f"A_W{W}", np.ascontiguousarray(w["A"], dtype="<u2").tobytes()))
        out.append((f"R0_W{W}", np.ascontiguousarray(w["R0"], dtype="<u2").tobytes()))
        out.append((f"first_W{W}", np.packbits(w["first"].ravel()).tobytes()))
        out.append((f"last_W{W}", np.packbits(w["last"].ravel()).tobytes()))
    return tuple(out)


def array_names() -> Tuple[str, ...]:
    return ("counts",) + tuple(f"{k}_W{W}" for W in C.F9_FLICKER_WINDOWS for k in ("A", "R0", "first", "last"))


def _array_sizes() -> Dict[str, int]:
    n = C.F9_N_CELLS; bits = (n + 7) // 8
    out = {"counts": 4 * (C.F9_TICKS + 1)}
    for W in C.F9_FLICKER_WINDOWS:
        out.update({f"A_W{W}": 2 * n, f"R0_W{W}": 2 * n, f"first_W{W}": bits, f"last_W{W}": bits})
    return out


def run_header(res: F9RunResult, blobs=None) -> Dict[str, object]:
    blobs = _array_blobs(res) if blobs is None else blobs
    s = res.spec
    return {
        "type": RUN_TYPE, "schema": RUN_SCHEMA, "version": C.F9_VERSION,
        "contract_sha256": C.F9_CONTRACT_SHA256, "declaration_sha256": C.verify_frozen_identity()["declaration_sha256"],
        "stream_declaration_sha256": R.verify_stream_declaration(),
        "master": s.master, "master_class": R.master_class(s.master), "terrain": s.terrain, "composition": s.composition,
        "object": s.obj, "initialization": s.init, "level_micro": s.level_micro, "level_id": C.level_id(s.level_micro), "seed_index": s.seed_index,
        "stream_key": list(s.stream_key),
        "identity_record_sha256": res.arm.identity_record_sha256, "index_sha256": res.arm.index_sha256,
        "spr": res.arm.spr, "g_spec": res.arm.g_spec, "g": res.g,
        "floor_probability": C.F9_FLOOR_PROBABILITY if s.obj == "realization" else 0.0, "floor_rule": C.F9_ETA0_RULE, "mu": C.F9_MU,
        "grid": C.F9_GRID, "dt": C.F9_DT, "ticks": C.F9_TICKS, "tail_ticks": C.F9_TAIL_TICKS, "windows": list(C.F9_FLICKER_WINDOWS),
        "extinction_tick": res.extinction_tick, "ticks_advanced": res.ticks_advanced, "draws_consumed": res.draws_consumed,
        "survival": res.survival, "tail_active_sum": res.tail_active_sum,
        "arrays": {name: hashlib.sha256(b).hexdigest() for name, b in blobs},
    }


def serialize_run(res: F9RunResult) -> bytes:
    """The run's record as one byte string (see SERIALIZATION)."""
    for W in C.F9_FLICKER_WINDOWS:
        if int(res.windows[W]["A"].max()) > 65535 or int(res.windows[W]["R0"].max()) > 65535: raise F9DynamicsError("a window count does not fit its declared type")
    if int(res.counts.max()) > 2 ** 31 - 1: raise F9DynamicsError("a count does not fit its declared type")
    blobs = _array_blobs(res)
    head = I.canonical_json(run_header(res, blobs))
    return RUN_MAGIC + struct.pack("<I", len(head)) + head + b"".join(b for _, b in blobs)


def run_identity(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


_HEADER_TYPES = {
    "type": str, "schema": int, "version": str, "contract_sha256": str, "declaration_sha256": str, "stream_declaration_sha256": str,
    "master": int, "master_class": str, "terrain": str, "composition": str, "object": str, "initialization": str,
    "level_micro": int, "level_id": str, "seed_index": int, "stream_key": list, "identity_record_sha256": str, "index_sha256": str,
    "spr": float, "g_spec": float, "g": float, "floor_probability": float, "floor_rule": str, "mu": float,
    "grid": int, "dt": int, "ticks": int, "tail_ticks": int, "windows": list,
    "extinction_tick": (int, type(None)), "ticks_advanced": int, "draws_consumed": int, "survival": bool, "tail_active_sum": int, "arrays": dict,
}


def _is_hex64(s) -> bool:
    return isinstance(s, str) and len(s) == 64 and all(ch in "0123456789abcdef" for ch in s)


def _int_list_is(value, want) -> bool:
    """`value` is a list of exact integers (no bool, no float) equal, element by element, to `want`."""
    return type(value) is list and len(value) == len(want) and all(type(a) is int and a == b for a, b in zip(value, want))


def parse_run(blob: bytes) -> Tuple[Dict[str, object], Dict[str, np.ndarray]]:
    """Form, declarations, bytes and internal consistency of a run record (see SERIALIZATION). Returns the header and
    the arrays (counts int64; A and R0 int64 (L, L); first and last bool (L, L))."""
    if not isinstance(blob, (bytes, bytearray)) or len(blob) < len(RUN_MAGIC) + 4 or bytes(blob[:len(RUN_MAGIC)]) != RUN_MAGIC:
        raise F9DynamicsError("not an F9 run record")
    blob = bytes(blob)
    (hlen,) = struct.unpack("<I", blob[len(RUN_MAGIC):len(RUN_MAGIC) + 4])
    start = len(RUN_MAGIC) + 4
    sizes = _array_sizes()
    if len(blob) != start + hlen + sum(sizes.values()): raise F9DynamicsError("the record's length is not the declared length")
    raw_head = blob[start:start + hlen]
    try:
        h = json.loads(raw_head.decode("ascii"))
        canonical = isinstance(h, dict) and I.canonical_json(h) == raw_head       # raises on NaN or an infinity
    except (UnicodeDecodeError, ValueError): raise F9DynamicsError("the header is not ASCII JSON of finite values")
    if not canonical: raise F9DynamicsError("the header is not in canonical form")
    if sorted(h) != sorted(_HEADER_TYPES): raise F9DynamicsError("the header's fields are not the declared fields")
    for k, typ in _HEADER_TYPES.items():
        ok = isinstance(h[k], typ) if isinstance(typ, tuple) else type(h[k]) is typ
        if not ok or (isinstance(h[k], bool) and typ is not bool): raise F9DynamicsError(f"header field {k!r} has the wrong type")
    frozen = C.verify_frozen_identity()
    if (h["type"], h["schema"], h["version"], h["contract_sha256"], h["declaration_sha256"], h["stream_declaration_sha256"]) != \
            (RUN_TYPE, RUN_SCHEMA, C.F9_VERSION, C.F9_CONTRACT_SHA256, frozen["declaration_sha256"], R.verify_stream_declaration()):
        raise F9DynamicsError("the record was not written under this instrument's declarations")
    try:
        spec = F9RunSpec(h["master"], h["terrain"], h["composition"], h["object"], h["initialization"], h["level_micro"], h["seed_index"]).check()
    except F9ConfigError as e:
        raise F9DynamicsError(f"the record does not name a declared run: {e}")
    T_, tail, n, L = C.F9_TICKS, C.F9_TAIL_TICKS, C.F9_N_CELLS, C.F9_GRID
    realization = spec.obj == "realization"
    if not _int_list_is(h["stream_key"], spec.stream_key) or h["master_class"] != R.master_class(spec.master) or h["level_id"] != C.level_id(spec.level_micro):
        raise F9DynamicsError("the record's stream key or labels do not follow from its run identity")
    if (h["grid"], h["dt"], h["ticks"], h["tail_ticks"], h["mu"], h["floor_rule"]) != (L, C.F9_DT, T_, tail, C.F9_MU, C.F9_ETA0_RULE) \
            or not _int_list_is(h["windows"], C.F9_FLICKER_WINDOWS):
        raise F9DynamicsError("the record's lattice, horizon, windows or rule constants are not the declared ones")
    if h["floor_probability"] != (C.F9_FLOOR_PROBABILITY if realization else 0.0): raise F9DynamicsError("the record's floor is not its object's")
    if not _is_hex64(h["identity_record_sha256"]) or not _is_hex64(h["index_sha256"]): raise F9DynamicsError("an identity in the header is not a sha256")
    if not (h["spr"] > 0.0 and h["g_spec"] > 0.0) or h["g"] != S.gain(spec.level_micro, h["g_spec"]):
        raise F9DynamicsError("the record's gain does not follow from its level and g_spec")
    if sorted(h["arrays"]) != sorted(array_names()) or not all(_is_hex64(v) for v in h["arrays"].values()):
        raise F9DynamicsError("the header does not name exactly the declared arrays, each by a sha256")
    arrays: Dict[str, np.ndarray] = {}
    pos = start + hlen
    for name in array_names():
        b = blob[pos:pos + sizes[name]]; pos += sizes[name]
        if hashlib.sha256(b).hexdigest() != h["arrays"][name]: raise F9DynamicsError(f"array differs from its stated identity: {name}")
        if name == "counts": arrays[name] = np.frombuffer(b, dtype="<i4").astype(np.int64)
        elif name.startswith(("A_", "R0_")): arrays[name] = np.frombuffer(b, dtype="<u2").astype(np.int64).reshape(L, L)
        else:
            bits = np.unpackbits(np.frombuffer(b, dtype=np.uint8))
            if bits[n:].any(): raise F9DynamicsError(f"padding bits are set: {name}")
            arrays[name] = bits[:n].astype(bool).reshape(L, L)
    _check_consistency(h, arrays, spec)
    return h, arrays


def _check_consistency(h: Dict[str, object], a: Dict[str, np.ndarray], spec: F9RunSpec) -> None:
    """NECESSARY relations between the stored quantities: what every record of the rule satisfies, whatever the
    trajectory. Not sufficient: see WHAT VALIDATES A RECORD.

    Counts.     0 <= counts <= N. Realization: every tick advanced, T + 1 draws, no extinction tick. Skeleton: the
                extinction tick is the first zero count and nothing is active after it; ticks advanced and draws
                follow from it; counts[0] is the declared start's.
    Tail.       survival = every tail count > 0; tail_active_sum = the sum of tail counts = the sum of A at W = 1.
    Per W.      With n windows: A <= n; R0 <= n - A; R0 = 0 exactly where A = n; the active segments
                Ra = R0 - 1 + first + last satisfy 0 <= Ra <= A, with Ra = 0 exactly where A = 0.
    W against the counts (c_t the tail counts, window j of width W):
                the number of cells active in window j lies between max and sum of c_t over the window. Hence
                sum_j max <= sum of A <= sum of c_t, and the same bounds on the first and the last window's masks.
                At W = 1 these are equalities: the first and last masks have exactly counts[first tail tick] and
                counts[T] cells. A cell is active only at ticks with a positive count: at W = 1, A <= the number of
                such tail ticks; at least max c_t cells have A > 0; at most min c_t cells have A = n.
    Nested W.   For every pair Ws < Wl with Wl a multiple of Ws (k = Wl/Ws), cell by cell: A_l <= A_s <= k·A_l;
                R0_l <= R0_s and Ra_l <= Ra_s (distinct coarse segments lie in distinct fine segments); an active
                fine end window implies an active coarse end window."""
    T_, tail, n = C.F9_TICKS, C.F9_TAIL_TICKS, C.F9_N_CELLS
    counts = a["counts"]; tc = counts[T_ - tail + 1:]
    bad = lambda why: F9DynamicsError(f"the record is not consistent: {why}")
    if counts.min() < 0 or counts.max() > n: raise bad("a count is outside [0, N]")
    ext, adv, draws = h["extinction_tick"], h["ticks_advanced"], h["draws_consumed"]
    if spec.obj == "realization":
        if ext is not None or adv != T_ or draws != T_ + 1: raise bad("a realization run advances every tick and has no extinction tick")
    else:
        zeros = np.flatnonzero(counts == 0)
        first_zero = int(zeros[0]) if zeros.size else None
        if ext != first_zero: raise bad("the extinction tick is not the first tick with zero active cells")
        if ext is not None and counts[ext:].any(): raise bad("activity after extinction")
        if adv != (T_ if ext is None else ext) or draws != adv: raise bad("ticks advanced or draws consumed do not follow from the extinction tick")
        start = n if spec.init == "all_active" else int(round(n * R.RHO0_LOW_MICRO / C.MICRO_UNITS))
        if counts[0] != start: raise bad("the initial count is not the declared start's")
    if h["survival"] != bool((tc > 0).all()): raise bad("survival is not 'active at every tail tick'")
    if h["tail_active_sum"] != int(tc.sum()) or int(a["A_W1"].sum()) != int(tc.sum()): raise bad("the tail's active total differs between the counts and the W = 1 record")
    seg = {}
    for W in C.F9_FLICKER_WINDOWS:
        nw = tail // W
        A, R0 = a[f"A_W{W}"], a[f"R0_W{W}"]
        first, last = a[f"first_W{W}"], a[f"last_W{W}"]
        Ra = R0 - 1 + first.astype(np.int64) + last.astype(np.int64)      # active segments: they alternate with the inactive ones
        seg[W] = (A, R0, Ra, first, last)
        if A.max() > nw or (R0 > nw - A).any() or ((A == nw) != (R0 == 0)).any(): raise bad(f"W = {W}: inactive segments against inactive windows")
        if (Ra < 0).any() or (Ra > A).any() or ((A == 0) != (Ra == 0)).any(): raise bad(f"W = {W}: active segments against active windows")
        blocks = tc.reshape(nw, W)
        lo, hi = blocks.max(axis=1), blocks.sum(axis=1)                   # per window: bounds on the number of cells active in it
        if not (int(lo.sum()) <= int(A.sum()) <= int(hi.sum())): raise bad(f"W = {W}: active windows against the tail counts")
        if not (int(lo[0]) <= int(first.sum()) <= int(hi[0])): raise bad(f"W = {W}: the first window's mask against the counts of its ticks")
        if not (int(lo[-1]) <= int(last.sum()) <= int(hi[-1])): raise bad(f"W = {W}: the last window's mask against the counts of its ticks")
    A1 = seg[1][0]
    if A1.max() > int((tc > 0).sum()): raise bad("a cell is active at more tail ticks than have any activity")
    if int((A1 > 0).sum()) < int(tc.max()) or int((A1 == tail).sum()) > int(tc.min()): raise bad("the cells ever active, or always active, against the largest or smallest tail count")
    widths = C.F9_FLICKER_WINDOWS
    for Ws in widths:
        for Wl in widths:
            if Wl <= Ws or Wl % Ws: continue
            k = Wl // Ws
            (As, R0s, Ras, fs, ls), (Al, R0l, Ral, fl, ll) = seg[Ws], seg[Wl]
            if (Al > As).any() or (As > k * Al).any(): raise bad(f"W = {Ws} and {Wl}: active windows are not nested")
            if (R0l > R0s).any() or (Ral > Ras).any(): raise bad(f"W = {Ws} and {Wl}: more segments at the coarser width")
            if (fs & ~fl).any() or (ls & ~ll).any(): raise bad(f"W = {Ws} and {Wl}: an end window is inactive though the finer end window in it is active")


def replay_equals(blob: bytes, arm: ArmContext) -> bool:
    """Parse the record, rerun its own run on this machine with the given arm context, and compare bytes. False when the
    arm context is not the one the record binds or the bytes differ."""
    h, _ = parse_run(blob)
    if (arm.terrain, arm.composition, arm.identity_record_sha256, arm.index_sha256, arm.spr, arm.g_spec) != \
            (h["terrain"], h["composition"], h["identity_record_sha256"], h["index_sha256"], h["spr"], h["g_spec"]):
        return False
    spec = F9RunSpec(h["master"], h["terrain"], h["composition"], h["object"], h["initialization"], h["level_micro"], h["seed_index"])
    return serialize_run(run(spec, arm)) == bytes(blob)


# ======================= reduction (§5.1) =======================
REDUCTION_CASES: Tuple[Tuple[float, float, float], ...] = tuple(
    (eta, g, lam) for eta in (0.0, C.F9_ETA0) for g, lam in ((1.0, 0.05), (1.0, 0.2758), (1.0, 0.45), (0.5, 0.512), (1.25, 0.512), (2.0, 0.8))
)
REDUCTION_TICKS = 200


def _sha_lf(path: str) -> str:
    with open(path, "rb") as fh: return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def reduction_check(t0_g_spec: Optional[float] = None) -> Dict[str, object]:
    """§5.1: with a constant index the per-cell step returns exactly the placed Flight 8 scalar step's array at equal
    state, effective gain, floor, μ, timing and uniforms. Two forms per case: Flight 8 given the same g and λ̄; and
    Flight 8 given g = 1 and λ̄ = g·λ (the effective gain as one number). With `t0_g_spec` (T0's g_spec from an identity
    record) every declared level of T0 is added, at T0's index 0.8³. Uniforms come from a declared apparatus stream."""
    from ..f8 import dynamics as F8D                   # the placed scalar step, imported, not copied
    L = C.F9_GRID
    cases = list(REDUCTION_CASES)
    if t0_g_spec is not None:
        cases += [(eta, S.gain(lv, t0_g_spec), 0.8 * 0.8 * 0.8) for eta in (0.0, C.F9_ETA0) for lv in C.F9_LEVELS_MICRO]
    equal = True; ticks = 0; unequal = []
    for k, (eta, g, lam_bar) in enumerate(cases):
        gen = np.random.Generator(np.random.PCG64(np.random.SeedSequence(list(REDUCTION_STREAM) + [k])))
        x = gen.random((L, L)) < 0.4
        lam = np.full((L, L), lam_bar)
        for _ in range(REDUCTION_TICKS):
            u = gen.random((L, L))
            mine = step(x, u, eta_floor=eta, g=g, lam=lam)
            a = F8D.step(x, u, eta_floor=eta, g=g, lambda_bar=lam_bar, mu=C.F9_MU)
            b = F8D.step(x, u, eta_floor=eta, g=1.0, lambda_bar=g * lam_bar, mu=C.F9_MU)
            same = bool(np.array_equal(mine, a) and np.array_equal(mine, b))
            if not same and k not in unequal: unequal.append(k)
            equal = equal and same; ticks += 1
            x = a
    return {"reduction_equal": equal, "cases": len(cases), "ticks_compared": ticks, "unequal_cases": unequal,
            "t0_levels_included": t0_g_spec is not None, "f8_dynamics_sha256_lf": _sha_lf(os.path.abspath(F8D.__file__)),
            "f9_version": C.F9_VERSION}
