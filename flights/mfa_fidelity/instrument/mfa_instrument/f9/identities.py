"""mfa_instrument/f9/identities.py — Flight 9 module M1: the identity build of Contract F9 v0.7 §3.4
step 4 (job `build_identities`, §8 step 1).

"At build, before any master is drawn: the canonical machine builds the base arrays, the comparison
arrays, the complete contour family of each (§5.5 step 5) with its traced components, and the
spectral values, and commits their identities. It verifies that on every same-family terrain the two
compositions' families are the same set of masks. These canonical objects are the ones every later
job uses and binds."

THE RECORD IS A FUNCTION OF THE BASE ARRAYS. `record_from_bases` computes every stated fact from the
24 base arrays it is given and the frozen declarations: the comparison arrays (the rounding rule of
§3.4 step 3 applied to those bases), the raw indices, the spectral values, the families with their
traced components, the same-family facts, and the terrain checks. `build_identity_record` applies it
to the bases the terrain formulas give on the running machine. `verify_bundle_deep` applies it to the
bases STORED in a bundle and requires the bundle's record to equal the result. So a record cannot
omit a declared object, point an arm at the wrong family, carry a comparison array that is not its
bases' or state a spectral value that does not follow, and still verify (L2, M1 round 1, R2).

WHAT EACH FUNCTION ESTABLISHES
  build_identity_record()  — the record for this machine's terrain arrays. No seed, no master, no
                             dynamics.
  write_bundle(out_dir)    — that record as canonical JSON, with the base arrays and comparison
                             arrays as raw bytes (§3.4 step 2), so that later jobs LOAD the canonical
                             objects and do not recompute a terrain through cos or tanh.
  load_bundle(dir)         — FORM AND BYTES ONLY: the record is canonical JSON of this type, version,
                             contract and declaration; it names exactly the declared array files; and
                             each file hashes to the value the record gives it. It does not check
                             that the record's statements are true of those arrays.
  verify_bundle_deep(dir)  — SEMANTICS: everything `load_bundle` checks, and then: the stored bases
                             agree with this machine's terrain formulas within the 1e-12 of §3.4
                             step 5; and the record equals `record_from_bases(stored bases)` in every
                             field except the environment. With float_rtol = 0 (the default, for the
                             machine that wrote the bundle) every float must be equal. A check on
                             another machine passes float_rtol = F9_SPR_RECOMPUTE_RTOL, the only other
                             value accepted, and each float then takes the rule of its own quantity
                             (FLOAT RULES below).
  compare_bundles(a, b)    — verifies both bundles deeply, then reports the largest base deviation
                             and whether the two registered families are the same masks (§3.4 step 5).

FLOAT RULES ON ANOTHER MACHINE (L2, M1 round 2). The recomputation starts from the STORED base
bytes, so only a quantity that passes through the platform's libm, a summation order or the
iteration can differ. Each such quantity has its own rule, and no rule borrows another's allowance:
  spr                      — contract §2.8: 1e-9 RELATIVE and nothing added, measured against the
                             smaller of the two magnitudes (so it holds whichever value is taken as
                             the reference). Beyond it the verifier raises `F9SpectralDiscrepancy`,
                             which carries the arm and both values so that a caller can record the
                             discrepancy; it never returns such a record as verified.
  g_spec                   — no tolerance in either mode: it must equal q/(Δt·spr) evaluated from the
                             RECORD'S OWN q and spr. One IEEE multiplication and one division of the
                             same operands give the same bits everywhere.
  q, eta0                  — module declaration, not a contract clause: within LIBM_ULPS = 2 units in
                             the last place of the libm result the rule passes through (exp(−μΔt) for
                             q, the logarithm itself for η₀).
  TB variance shares and   — module declaration, not a contract clause: within
  additive residual          DESCRIPTIVE_VARIANCE_ATOL = 1e-12 absolute. They are descriptive sums; the
                             ruled range of the x-share is enforced on the recomputed value in either
                             mode.
  every other float        — equal, in both modes (extremes, differences, levels and distances of the
                             stored arrays and the declared geometry: no libm, no summation).
The 1e-12 of §3.4 step 5 applies to base-array elements only, where `verify_bundle_deep` applies it.

WHAT NONE OF THEM ESTABLISHES. That a bundle is the canonical one. A record names no digest of
itself and proves nothing about who wrote it. Binding the authorized record's identity, the
instrument's source identity and the atomic publication of the bundle of record are the runner's,
under Mike's authorization for §8 step 1, on the canonical machine. Called anywhere else these
functions produce a noncanonical bundle that binds nothing. The environment field is descriptive.

SAME-FAMILY VERIFICATION. On TA, TC and the four TD variants both compositions take their contours
from one comparison array, so their families are the same masks by construction; the record states
that as checked facts. It also records how each raw index relates to that array: the largest fall of
the index following cells in order of increasing ω (ties in ω ordered by the index), and the largest
spread of the index inside one level class of ω. The 1e-12 bound of §3.4 step 3 is ENFORCED ON THE
FALL. The spread is reported only; it can approach the rounding unit, since a level class is 1e-12
wide in the latent.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import sys
from typing import Dict, Tuple

import numpy as np

from . import config as C
from . import family as F
from . import geometry as G
from . import spectral as S
from . import terrain as T
from .config import F9ConfigError

RECORD_NAME = "F9_IDENTITIES.json"
RECORD_TYPE = "F9IdentityRecord"
RECORD_SCHEMA = 2
SAME_FAMILY_INDEX_TOL = 1e-12                         # contract §3.4 step 3, on the fall
EMPTY_FAMILY = "empty: no eligible contour"
LIBM_ULPS = 2                                         # module declaration: q and η₀ on another machine (see FLOAT RULES)
DESCRIPTIVE_VARIANCE_ATOL = 1e-12                     # module declaration: TB's descriptive variance figures on another machine
BaseSet = Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray]]


class F9SpectralDiscrepancy(F9ConfigError):
    """Contract §2.8: a recomputation of an arm's spectral radius differs from the recorded value by more than 1e-9
    relative. Carries what a caller needs to record the discrepancy."""

    def __init__(self, arm: str, stated: float, recomputed: float):
        self.arm = arm; self.stated = stated; self.recomputed = recomputed
        self.relative = abs(stated - recomputed) / min(abs(stated), abs(recomputed)) if min(abs(stated), abs(recomputed)) > 0.0 else math.inf
        super().__init__(f"record.arms.{arm}.spr: stated {stated!r}, the stored arrays give {recomputed!r}: "
                         f"{self.relative!r} relative, beyond the {C.F9_SPR_RECOMPUTE_RTOL!r} of contract §2.8")


def canonical_json(obj) -> bytes:
    """Sorted keys, compact separators, ASCII, one trailing newline. Floats use Python's shortest round-trip repr."""
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def environment() -> Dict[str, str]:
    return {"platform": platform.platform(), "machine": platform.machine(), "python": platform.python_version(),
            "numpy": np.__version__, "byteorder": sys.byteorder}


def omega_key(name: str, comp: str):
    """The name of an arm's comparison array: one shared array on a same-family terrain, one per composition on TB, none on T0."""
    if name == "T0": return None
    return f"{name}.shared" if C.same_family_latent(name) is not None else f"{name}.{comp}"


def family_keys() -> Tuple[str, ...]:
    """The eight comparison arrays, in the order the arms first use them."""
    out = []
    for name, comp in C.F9_ARMS:
        k = omega_key(name, comp)
        if k is not None and k not in out: out.append(k)
    return tuple(out)


def array_files() -> Tuple[str, ...]:
    """The relative path (forward slashes) of every array of the bundle, in a fixed order. Paths are literal strings;
    they are never built with os.path.join, so they are the same on every platform."""
    return tuple(f"bases/{name}.{b}.f64" for name in C.F9_TERRAINS for b in ("v", "u", "r")) + tuple(f"omega/{k}.f64" for k in family_keys())


def derived_omega(name: str, comp: str, v: np.ndarray, u: np.ndarray, r: np.ndarray) -> np.ndarray:
    """The comparison array of §3.4 step 3 from GIVEN bases: the shared latent (v on TA and TD, u on TC) or, on TB, the
    composition's raw index; rounded to 12 places. No terrain formula is evaluated."""
    latent = C.same_family_latent(name)
    src = {"v": v, "u": u}[latent] if latent is not None else T.compose(comp, v, u, r)
    return np.ascontiguousarray(np.round(src, C.F9_ROUND_PLACES), dtype=np.float64)


def _unrounded(name: str, comp: str, v, u, r) -> np.ndarray:
    latent = C.same_family_latent(name)
    return {"v": v, "u": u}[latent] if latent is not None else T.compose(comp, v, u, r)


def _relation(om: np.ndarray, lam: np.ndarray) -> Dict[str, float]:
    om = om.ravel(); lam = lam.ravel()
    order = np.lexsort((lam, om)); seq = lam[order]; oms = om[order]
    fall = float(max(0.0, np.max(np.maximum.accumulate(seq) - seq)))
    starts = np.flatnonzero(np.r_[True, oms[1:] != oms[:-1]]); ends = np.r_[starts[1:], oms.size]
    spread = float(max(seq[e - 1] - seq[s] for s, e in zip(starts, ends)))    # within a class the sequence is sorted by λ
    return {"largest_fall": fall, "largest_spread_within_a_level": spread}


def _check_bases(bases: BaseSet) -> None:
    if sorted(bases) != sorted(C.F9_TERRAINS): raise F9ConfigError("bases must be given for exactly the declared terrains")
    for name, vur in bases.items():
        if len(vur) != 3: raise F9ConfigError(f"{name}: three base arrays are required")
        for b in vur:
            if not isinstance(b, np.ndarray) or b.dtype != np.float64 or b.shape != (C.F9_GRID, C.F9_GRID) or not np.all(np.isfinite(b)) \
                    or float(b.min()) < 0.0 or float(b.max()) > 1.0:
                raise F9ConfigError(f"{name}: a base is not a finite float64 (L, L) array in [0, 1]")


def record_from_bases(bases: BaseSet, env: Dict[str, str]) -> Dict[str, object]:
    """Every fact of the identity record, computed from the given base arrays and the frozen declarations."""
    frozen = C.verify_frozen_identity()
    _check_bases(bases)
    arrays: Dict[str, str] = {}
    terrains: Dict[str, object] = {}
    for name in C.F9_TERRAINS:
        v, u, r = bases[name]
        raws = {b: T.serialize(a) for b, a in (("v", v), ("u", u), ("r", r))}
        for b in ("v", "u", "r"): arrays[f"bases/{name}.{b}.f64"] = hashlib.sha256(raws[b]).hexdigest()
        entry: Dict[str, object] = {
            "base_sha256": hashlib.sha256(raws["v"] + raws["u"] + raws["r"]).hexdigest(),
            "base_min": float(min(v.min(), u.min(), r.min())), "base_max": float(max(v.max(), u.max(), r.max())),
        }
        if name == "T0" and not (np.all(v == 0.8) and np.all(u == 0.8) and np.all(r == 0.8)):
            raise F9ConfigError("T0: the bases are not the constant 0.8 of contract §3.1")
        if name in ("TA",) or name.startswith("TD"):
            if not (np.array_equal(v, u) and np.array_equal(v, r)): raise F9ConfigError(f"{name}: the three bases are not one common array")
        if name.startswith("TD"):
            core = T.td_core(name); e = G.edge(core)       # the declared geometry: integer cell sets, no cos or tanh
            if not np.array_equal(core, v > 0.6):          # the base rises through the middle of its step exactly at the core's edge
                raise F9ConfigError(f"{name}: the base array's upper half is not the declared core")
            entry["core"] = {"cells": int(core.sum()), "mask_sha256": hashlib.sha256(np.packbits(core.ravel()).tobytes()).hexdigest(),
                             "perimeter_bonds": e.n_bonds, "component_sizes": list(e.component_sizes()),
                             "least_distance_of_a_centre_to_the_edge": float(np.abs(T.td_delta(name)).min())}
        if name == "TB":
            P = T.compose("P", v, u, r); H = T.compose("H", v, u, r)
            vx = float(np.var(P.mean(axis=1))); vy = float(np.var(P.mean(axis=0)))
            sh = {"x": vx / (vx + vy), "y": vy / (vx + vy), "additive_residual": float(np.var(P) - vx - vy)}
            lo, hi = C.F9_TB_X_SHARE_RANGE
            if not (lo <= sh["x"] <= hi): raise F9ConfigError("TB: the product's x-share is outside the ruled range of contract §3.2")
            def _fall(a, b):
                seq = b.ravel()[np.lexsort((b.ravel(), a.ravel()))]
                return float(max(0.0, np.max(np.maximum.accumulate(seq) - seq)))
            entry["product_variance_shares"] = sh; entry["cross_fall"] = {"H_along_P": _fall(P, H), "P_along_H": _fall(H, P)}
        terrains[name] = entry

    omegas: Dict[str, np.ndarray] = {}
    families: Dict[str, object] = {}
    arms: Dict[str, object] = {}
    for name, comp in C.F9_ARMS:
        v, u, r = bases[name]
        lam = T.compose(comp, v, u, r)
        if float(lam.min()) <= 0.0: raise F9ConfigError(f"{name}.{comp}: the index is not strictly positive (the spectral routine's domain)")
        spr = S.spectral_radius(lam)
        key = omega_key(name, comp)
        arm: Dict[str, object] = {
            "terrain": name, "composition": comp, "omega_key": key,
            "index_sha256": T.array_sha256(lam), "index_min": float(lam.min()), "index_max": float(lam.max()),
            "spr": spr, "g_spec": C.q_deact() / (C.F9_DT * spr),
        }
        om = derived_omega(name, comp, v, u, r)
        if key is None:
            if not F.Family(om).is_empty: raise F9ConfigError("T0: a constant index must have an empty family")
            arm["family"] = EMPTY_FAMILY
        else:
            if key not in families:
                summ = F.family_summary(om); summ["omega_sha256"] = T.array_sha256(om)
                summ["distinct_values_before_rounding"] = int(np.unique(_unrounded(name, comp, v, u, r)).size) - 1     # descriptive: what rounding merged
                families[key] = summ; omegas[key] = om
                arrays[f"omega/{key}.f64"] = summ["omega_sha256"]
            elif not np.array_equal(om, omegas[key]):
                raise F9ConfigError(f"{name}: the two compositions do not derive the same comparison array")
            if C.same_family_latent(name) is not None:
                rel = _relation(om, lam)
                if rel["largest_fall"] > SAME_FAMILY_INDEX_TOL: raise F9ConfigError(f"{name}.{comp}: the raw index falls along the shared comparison array")
                arm["relation_to_shared_array"] = rel
        arms[f"{name}.{comp}"] = arm

    same_family: Dict[str, object] = {}
    for name, _latent in C.F9_SAME_FAMILY_LATENT:
        v, u, r = bases[name]
        oP, oH = derived_omega(name, "P", v, u, r), derived_omega(name, "H", v, u, r)
        mP, mH = families[omega_key(name, "P")]["masks_sha256"], F.masks_identity(oH)
        if not np.array_equal(oP, oH) or mP != mH: raise F9ConfigError(f"{name}: the two compositions' families are not the same set of masks")
        same_family[name] = {"arrays_identical": True, "masks_identical": True, "masks_sha256": mP}

    if sorted(arrays) != sorted(array_files()): raise F9ConfigError("internal: the arrays computed are not the declared arrays")
    return {
        "type": RECORD_TYPE, "schema": RECORD_SCHEMA,
        "version": C.F9_VERSION, "contract_sha256": C.F9_CONTRACT_SHA256, "freeze_record_sha256": C.F9_FREEZE_RECORD_SHA256,
        "declaration_sha256": frozen["declaration_sha256"],
        "grid": C.F9_GRID, "round_places": C.F9_ROUND_PLACES, "q": C.q_deact(), "eta0": C.F9_ETA0,
        "levels_micro": list(C.F9_LEVELS_MICRO),
        "environment": dict(env),
        "terrains": terrains, "arms": arms, "families": families, "same_family": same_family, "arrays": arrays,
    }


def machine_bases() -> BaseSet:
    """The bases the terrain formulas give on the running machine."""
    return {name: T.bases(name) for name in C.F9_TERRAINS}


def build_identity_record() -> Dict[str, object]:
    """The identity record for this machine's terrain arrays. Deterministic given the platform's libm."""
    return record_from_bases(machine_bases(), environment())


def record_identity(record: Dict[str, object]) -> str:
    """SHA-256 of the record's canonical JSON. A value to be bound from outside (the runner's); the record does not contain it."""
    return hashlib.sha256(canonical_json(record)).hexdigest()


def _resolve(out_dir: str, rel: str) -> str:
    """A declared relative path (forward slashes) under out_dir, as a filesystem path. Refuses anything that would leave out_dir."""
    parts = rel.split("/")
    if any(p in ("", ".", "..") for p in parts) or os.path.isabs(rel): raise F9ConfigError(f"unsafe relative path: {rel!r}")
    return os.path.join(out_dir, *parts)


def write_bundle(out_dir: str) -> Dict[str, object]:
    """Write the arrays and the record under out_dir (which must not already hold a record). Returns the record.
    Every file is written with explicit bytes; nothing depends on the platform's newline or text encoding."""
    if os.path.exists(os.path.join(out_dir, RECORD_NAME)): raise F9ConfigError("a record already exists in the target directory")
    bases = machine_bases()
    record = record_from_bases(bases, environment())
    payload = {f"bases/{name}.{b}.f64": T.serialize(bases[name][k]) for name in C.F9_TERRAINS for k, b in enumerate(("v", "u", "r"))}
    for name, comp in C.F9_ARMS:
        key = omega_key(name, comp)
        if key is not None: payload[f"omega/{key}.f64"] = T.serialize(derived_omega(name, comp, *bases[name]))
    for rel in array_files():
        if hashlib.sha256(payload[rel]).hexdigest() != record["arrays"][rel]: raise F9ConfigError(f"internal: bytes to be written differ from the record: {rel}")
        dst = _resolve(out_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as fh: fh.write(payload[rel])
    with open(os.path.join(out_dir, RECORD_NAME), "wb") as fh: fh.write(canonical_json(record))
    return record


def load_bundle(bundle_dir: str) -> Tuple[Dict[str, object], Dict[str, np.ndarray]]:
    """FORM AND BYTES ONLY (see the module docstring). Returns the record and the arrays by relative path."""
    with open(os.path.join(bundle_dir, RECORD_NAME), "rb") as fh: raw = fh.read()
    try: record = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, ValueError): raise F9ConfigError("record is not ASCII JSON")
    if not isinstance(record, dict) or canonical_json(record) != raw: raise F9ConfigError("record is not in canonical form")
    if record.get("type") != RECORD_TYPE or record.get("schema") != RECORD_SCHEMA: raise F9ConfigError("not an F9 identity record of this schema")
    frozen = C.verify_frozen_identity()
    for k in ("version", "contract_sha256", "freeze_record_sha256", "declaration_sha256"):
        if record.get(k) != frozen[k]: raise F9ConfigError(f"record's {k} differs from this instrument's frozen declaration")
    declared = array_files()
    named = record.get("arrays")
    if not isinstance(named, dict) or sorted(named) != sorted(declared): raise F9ConfigError("record does not name exactly the declared arrays")
    arrays: Dict[str, np.ndarray] = {}
    for rel in declared:
        with open(_resolve(bundle_dir, rel), "rb") as fh: b = fh.read()
        if hashlib.sha256(b).hexdigest() != named[rel]: raise F9ConfigError(f"array differs from its recorded identity: {rel}")
        arrays[rel] = T.deserialize(b)
    return record, arrays


def _float_rule(path: Tuple[str, ...]) -> str:
    """The rule of the float at `path` (the keys below the record's root) on another machine. See FLOAT RULES."""
    if len(path) == 3 and path[0] == "arms" and path[2] in ("spr", "g_spec"): return path[2]
    if path in (("q",), ("eta0",)): return path[0]
    if path[:3] == ("terrains", "TB", "product_variance_shares") and len(path) == 4: return "variance"
    return "exact"


def _same(a, b, cross: bool, path: Tuple[str, ...] = ()) -> None:
    """Structural equality of two JSON values: `a` stated by a record, `b` recomputed from its stored arrays. Types must
    match exactly. Floats must be equal, except that with `cross` (another machine) each float takes the rule of its
    quantity. An arm's g_spec is not compared here in that mode: `verify_bundle_deep` holds it to the record's own q
    and spr."""
    where = ".".join(("record",) + path)
    if type(a) is not type(b): raise F9ConfigError(f"{where}: type differs")
    if isinstance(a, dict):
        if sorted(a) != sorted(b): raise F9ConfigError(f"{where}: the entries present are not the entries required")
        for k in a: _same(a[k], b[k], cross, path + (k,))
    elif isinstance(a, list):
        if len(a) != len(b): raise F9ConfigError(f"{where}: length differs")
        for i, (x, y) in enumerate(zip(a, b)): _same(x, y, cross, path + (f"[{i}]",))
    elif isinstance(a, float):
        rule = _float_rule(path) if cross else "exact"
        if rule == "exact": ok = a == b
        elif rule == "spr":
            if not abs(a - b) <= C.F9_SPR_RECOMPUTE_RTOL * min(abs(a), abs(b)): raise F9SpectralDiscrepancy(path[1], a, b)
            ok = True
        elif rule == "g_spec": ok = True
        elif rule == "q": ok = abs(a - b) <= LIBM_ULPS * math.ulp(1.0 - b)
        elif rule == "eta0": ok = abs(a - b) <= LIBM_ULPS * math.ulp(b)
        else: ok = abs(a - b) <= DESCRIPTIVE_VARIANCE_ATOL
        if not ok: raise F9ConfigError(f"{where}: stated {a!r}, the stored arrays give {b!r}")
    elif a != b:
        raise F9ConfigError(f"{where}: stated {a!r}, the stored arrays give {b!r}")


def _stored_bases(arrays: Dict[str, np.ndarray]) -> BaseSet:
    return {name: tuple(arrays[f"bases/{name}.{b}.f64"] for b in ("v", "u", "r")) for name in C.F9_TERRAINS}


def verify_bundle_deep(bundle_dir: str, *, float_rtol: float = 0.0) -> Dict[str, object]:
    """SEMANTICS (see the module docstring). Loads the bundle, checks its stored bases against this machine's terrain
    formulas within 1e-12, recomputes the whole record from the stored bases, and requires the bundle's record to equal
    it in every field except the environment: every float equal when float_rtol = 0; each float under its own rule
    (module docstring, FLOAT RULES) when float_rtol = F9_SPR_RECOMPUTE_RTOL. No other value is accepted, so a caller
    cannot enlarge a frozen tolerance. Raises `F9SpectralDiscrepancy` for a spectral radius beyond §2.8's bound.
    Returns the verified record."""
    if type(float_rtol) is not float or float_rtol not in (0.0, C.F9_SPR_RECOMPUTE_RTOL):
        raise F9ConfigError("float_rtol is 0.0 (the writing machine) or F9_SPR_RECOMPUTE_RTOL (another machine); nothing else")
    cross = float_rtol != 0.0
    record, arrays = load_bundle(bundle_dir)
    env = record.get("environment")
    if not isinstance(env, dict) or sorted(env) != sorted(environment()) or not all(isinstance(x, str) for x in env.values()):
        raise F9ConfigError("record's environment is not the declared set of strings")
    stored = _stored_bases(arrays)
    _check_bases(stored)
    for name in C.F9_TERRAINS:                         # §3.4 step 5: a recomputation here agrees with the stored arrays
        for k, mine in enumerate(T.bases(name)):
            dev = float(np.max(np.abs(mine - stored[name][k])))
            if not dev <= C.F9_CROSS_PLATFORM_TOL: raise F9ConfigError(f"{name}: a stored base is {dev!r} from the declared terrain, beyond 1e-12")
    recomputed = record_from_bases(stored, env)
    _same(record, recomputed, cross)
    for arm, entry in record["arms"].items():          # in either mode: the gain follows from the record's own q and spr
        if entry["g_spec"] != record["q"] / (C.F9_DT * entry["spr"]):
            raise F9ConfigError(f"record.arms.{arm}.g_spec: does not equal q/(dt*spr) of the record's own q and spr")
    for key in family_keys():                          # the stored comparison arrays are the ones the stored bases derive
        if T.array_sha256(arrays[f"omega/{key}.f64"]) != recomputed["families"][key]["omega_sha256"]:
            raise F9ConfigError(f"{key}: the stored comparison array is not the one its bases derive")
    return record


def compare_bundles(dir_a: str, dir_b: str, *, float_rtol: float = C.F9_SPR_RECOMPUTE_RTOL) -> Dict[str, object]:
    """§3.4 step 5 between two bundles. BOTH ARE VERIFIED DEEPLY FIRST, so every identity compared here follows from its
    bundle's stored arrays. Reports the largest per-element base deviation, and separately whether the registered
    families are the same masks: numerical agreement to 1e-12 does not guarantee identical masks. The spectral
    difference BETWEEN the two records is reported against the smaller value and flagged, not refused; each record's
    own agreement with its stored arrays was already enforced by the deep verification."""
    ra = verify_bundle_deep(dir_a, float_rtol=float_rtol); rb = verify_bundle_deep(dir_b, float_rtol=float_rtol)
    _ra, aa = load_bundle(dir_a); _rb, ab = load_bundle(dir_b)
    dev = {rel: float(np.max(np.abs(aa[rel] - ab[rel]))) for rel in aa if rel.startswith("bases/")}
    worst_rel = max(dev, key=dev.get)
    fam = {key: {"levels_a": ra["families"][key]["n_levels"], "levels_b": rb["families"][key]["n_levels"],
                 "same_masks": ra["families"][key]["masks_sha256"] == rb["families"][key]["masks_sha256"],
                 "same_components": ra["families"][key]["components_sha256"] == rb["families"][key]["components_sha256"],
                 "same_family": ra["families"][key]["family_sha256"] == rb["families"][key]["family_sha256"]} for key in family_keys()}
    spr = {arm: abs(ra["arms"][arm]["spr"] - rb["arms"][arm]["spr"]) / min(ra["arms"][arm]["spr"], rb["arms"][arm]["spr"]) for arm in ra["arms"]}
    return {"record_a_sha256": record_identity(ra), "record_b_sha256": record_identity(rb),
            "largest_base_deviation": dev[worst_rel], "largest_base_deviation_array": worst_rel,
            "base_deviation_within_tolerance": bool(dev[worst_rel] <= C.F9_CROSS_PLATFORM_TOL),
            "base_arrays_bit_identical": all(ra["arrays"][rel] == rb["arrays"][rel] for rel in dev),
            "families": fam, "all_families_same_masks": all(v["same_masks"] for v in fam.values()),
            "largest_spr_relative_difference": max(spr.values()), "spr_within_tolerance": bool(max(spr.values()) <= C.F9_SPR_RECOMPUTE_RTOL),
            "environment_a": ra["environment"], "environment_b": rb["environment"]}
