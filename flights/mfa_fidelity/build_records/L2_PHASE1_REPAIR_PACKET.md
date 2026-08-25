# Note to L2 — Phase-1 Repair Packet: Minimum Repair Set Items 1–10 Implemented

**From:** L1, routed by Mike
**Register:** closed, scoped — verification of your Phase-1 review's minimum repair set. Full current source of every Phase-1 file is carried verbatim below the rule (previously reviewed texts superseded); digests at the foot. Suite: 63/63 (53 prior + the required negative matrix and ownership demonstrations).

## Repair map (your item → implementation, with its discriminating test)

1. **State-alias surfaces (D1a/D1b):** `Dynamics.__init__` takes ownership by **private copies** of all four state arrays — the caller's `GridState` retains no reference to live state. Telemetry receives a **copy** of `delta` (`delta_telem`); the private array alone feeds the Step-12 update. Tests: `test_dynamics_owns_private_copies` (hostile caller zeroes the retained GridState mid-run; terrain unaffected) and `test_sink_cannot_alter_q_update` (hostile sink un-freezes and overwrites Delta_v; evolution bit-identical to a sink-free run).
2. **Base-draw policy config-bound (D2):** new immutable field `InitConfig.base_init_mode ∈ {"stochastic_ancestor", "deterministic_level"}`; the runner-side `draw_bases` argument is **deleted**; the mode serializes in run_config.json with everything else; RunConfig cross-validates (symmetric_chain requires stochastic_ancestor). Your added test requirement honored: the policy test now compares the **next** Generator output post-init against a shadow, so hidden post-permutation consumption is detected.
3. **Gate-A surfaces (D5/N4/N5):** `GATE_A_LABELS` is a closed set — unknown labels raise before anything runs. `GateAReport` separates `behavioral_bit_exact` from `gate_passed`; `gate_passed` requires **preflight AND behavioral**, and `passed` is an alias of the stronger property so no consumer can read the weak one under the strong name. `load_ancestor` computes the ancestor file's SHA-256 and enforces it when an expectation is supplied; **AUTHORITATIVE requires the expectation** (raises without it) in addition to the environment conformance refusal. The ancestor digest enters the report.
4. **rho_global decoupled and persisted (N1/N2):** `Dynamics(..., emit_rho_global=True)` makes emission a run-mode obligation independent of Q's read — an E1 total-Q-disable run emits it (tested). `TelemetryWriter.close()` persists the tick table as `<stem>.rho_global.parquet`; `artifact_paths()` feeds both files to the canonical digest; the verifier requires the artifact when expected and forbids it otherwise, and validates its schema and exact tick coverage.
5. **become_survive nonzero-Q rejected (N3, interim per your disjunction):** construction raises; silent ignoring is foreclosed. The permanent branch choice (implement the common-Q skeleton vs. freeze the rejection as the supported subset) is Phase-2 integration work, flagged for that packet.
6. **Tier-1 schema- and completeness-enforcing (V1/V3):** `expected_schema(cfg)` derives the required column set from the configuration **independently of the writer**; missing and forbidden columns both fail before recomputation. Completeness: `passed` is False on empty reports or zero rows (the `all([])` hole closed); exact row totals, per-tick row counts, per-(Tick, Agent_X, Agent_Y) uniqueness, and coordinate ranges enforced from the consumed configuration.
7. **Global-Q verification (V2):** `Delta_from_rho == gamma_rho · rho_global(t)` verified by tick-join against the persisted table; planted 1e-15 defect caught (tested).
8. **E1 identity truly bitwise, tick-0 anchored (V4):** float64 storage compared via `view(np.uint64)`; tick-0 baselines required for every cell (`anchored_without_tick0` fails first-row anchoring); empty and truncated inputs fail; the absence set now includes `Delta_from_Psi`/`Delta_from_rho`. Tested with a 1-ulp `nextafter` plant and an explicit −0.0/+0.0 plant that numeric equality would have passed.
9. **Machine-specific import removed (V6):** all five test files import repo-relative from the test file's own location; no absolute L1 path exists anywhere.
10. **Negative matrix (V7):** missing schema; forbidden schema; empty/dropped-tick/dropped-row/duplicated-row files; global-Q; rho_global artifact missing; `Term_Offset` and `gamma_coef` plants (V5); ulp-level bit identity; no-tick-0; plus the two hostile-actor ownership tests.

**V5 additions in the verifier:** `Term_Offset`, `gamma_coef`, `Delta_from_Psi == 0` when Γ_Ψ = 0, global `Delta_from_rho`, and the tick table's own schema/coverage.

## Review requested (closed register)

1. Per repair item 1–10: **REPAIRED AS REQUIRED** or **REPAIR DEFECT** with location.
2. Any new defect introduced by the repairs: **NONE FOUND** complete.
3. **Phase-1 closure disposition:** PHASE 1 COMPLETE (subject to the final authoritative regression per the build plan) or remaining blockers named.

---

# ARTIFACT: mfa_instrument/config.py
```python
"""mfa_instrument.config — Run configuration: immutable, validated, canonically serialized.

Spec anchors: Merge Specification v0.4 FROZEN §7.3 (run_config.json / run_record.json,
canonical serialization, digests), §9.2 (one consumed object, written before the run),
§10 (naming ledger). Contract E1 v0.8 §C (six-decimal control values).

Boundary rules (Build Plan v0.2, L2 finding C):
  - Deeply immutable after construction (frozen dataclasses; tuples only; no dicts).
  - No module mutates, normalizes, or defaults into a validated config.
  - run_config.json is serialized from this exact object; run-derived state goes in
    the run record, never back into configuration.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
from dataclasses import dataclass, field
from typing import Optional, Tuple

# ---------------------------------------------------------------------------
# Naming ledger (frozen spec §10). These are the only legal values.
# ---------------------------------------------------------------------------
RULE_MODES = ("symmetric_chain", "become_survive")
Q_READS = ("local", "global")
F_DISPATCH_LABELS = ("F_canonical", "F_2_symmetric", "F_LR", "F_baseline")
F_BASELINE = "F_baseline"  # carried, legacy-unused: arbitration required to select
INIT_ACTIVITY_SCHEMES = ("bernoulli_p", "fixed_count")

MICRO_UNITS = 10 ** 6  # six-decimal control values, exact integer micro-units (E1 v0.8 §C/§E)


class ConfigError(ValueError):
    """Raised when a configuration fails validation at construction."""


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise ConfigError(msg)


def as_micro_units(m: float) -> int:
    """Exact integer micro-unit representation of a six-decimal control value.

    Raises ConfigError if `m` is not exactly representable at six decimals
    (E1 v0.8: six-decimal values ARE the consumed control values, not aliases).
    """
    k = round(m * MICRO_UNITS)
    _require(abs(m * MICRO_UNITS - k) < 1e-6, f"control value {m!r} is not a six-decimal value")
    _require(0 <= k <= MICRO_UNITS, f"control value {m!r} outside [0, 1]")
    return int(k)


# ---------------------------------------------------------------------------
# Constants block — Lineage A committed values are the defaults (facts v1.1 S1(b)).
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class DynamicsConstants:
    alpha: float = 4.0
    beta: float = 3.0
    delta: float = 4.0
    gamma_offset: float = 4.0
    eta_floor: float = 0.01           # A's nucleation floor; never called eta_MFA
    w_v: float = 0.33                 # F_2_symmetric weights
    w_u: float = 0.33
    w_r: float = 0.34
    logit_l: Optional[float] = None   # become_survive only; None in symmetric_chain
    kappa: Optional[float] = None     # become_survive only
    p_survive: Optional[float] = None # become_survive only: survival is rand < p_survive,
                                      # a CONSTANT probability ("bare p_Lambda"), source-read
                                      # from c3_w2_tcop.py L272 (stay_active: rand < LAMBDA)

    def validate(self, rule_mode: str) -> None:
        _require(0.0 <= self.eta_floor < 1.0, "eta_floor must be in [0, 1)")
        if rule_mode == "become_survive":
            _require(self.logit_l is not None and self.kappa is not None
                     and self.p_survive is not None,
                     "become_survive requires logit_l, kappa, and p_survive")
            _require(0.0 <= self.p_survive <= 1.0, "p_survive must be a probability")
        else:
            _require(self.logit_l is None and self.kappa is None and self.p_survive is None,
                     "symmetric_chain must not carry logit_l/kappa/p_survive (ledger: these "
                     "are become_survive symbols; A's local terms are density/overcrowding)")


@dataclass(frozen=True)
class QConfig:
    """Extended-Q linear form (spec §4.1): delta_b = gamma_psi*Psi_local + gamma_rho*act.
    gamma_psi == gamma_rho == 0.0 is the E1 total-Q-disable configuration: dynamics
    must execute NO base-update arithmetic (paths absent, not zero-valued)."""
    q_read: str = "local"
    gamma_psi: float = 0.0
    gamma_rho: float = 0.0

    def validate(self) -> None:
        _require(self.q_read in Q_READS, f"q_read must be one of {Q_READS}")


BASE_INIT_MODES = ("stochastic_ancestor", "deterministic_level")


@dataclass(frozen=True)
class InitConfig:
    scheme: str = "bernoulli_p"
    base_center_micro: int = 750_000      # m in micro-units (ancestor: U(0.6,0.9) => m=0.75)
    base_width_micro: int = 300_000       # w in micro-units (w = 0.3)
    bernoulli_p: float = 0.5
    fixed_count: Optional[int] = None     # fixed_count scheme only
    base_init_mode: str = "stochastic_ancestor"
    # L2 Phase-1 review D2: the base-initialization ALGORITHM lives in the immutable
    # consumed configuration — "stochastic_ancestor" (the Gate-A cell-by-cell draw
    # sequence) or "deterministic_level" (np.full at m, zero base draws; the
    # become_survive/B-comparable policy). No runner-side switch exists; the value
    # serializes into run_config.json with everything else.

    def validate(self, n_cells: int) -> None:
        _require(self.scheme in INIT_ACTIVITY_SCHEMES,
                 f"init scheme must be one of {INIT_ACTIVITY_SCHEMES}")
        _require(self.base_init_mode in BASE_INIT_MODES,
                 f"base_init_mode must be one of {BASE_INIT_MODES}")
        lo = self.base_center_micro - self.base_width_micro // 2
        hi = self.base_center_micro + self.base_width_micro // 2
        _require(0 <= lo and hi <= MICRO_UNITS,
                 "base interval must lie within [0,1] with NO clipping (E1 §3)")
        if self.scheme == "fixed_count":
            _require(self.fixed_count is not None and 0 <= self.fixed_count <= n_cells,
                     "fixed_count scheme requires 0 <= fixed_count <= n_cells")
        else:
            _require(self.fixed_count is None, "bernoulli_p scheme must not set fixed_count")
            _require(0.0 <= self.bernoulli_p <= 1.0, "bernoulli_p must be in [0,1]")

    @property
    def m(self) -> float:
        return self.base_center_micro / MICRO_UNITS

    @property
    def w(self) -> float:
        return self.base_width_micro / MICRO_UNITS


@dataclass(frozen=True)
class NoiseConfig:
    """D4 noise architecture. amplitude == 0.0 => no stream construction, no draws,
    no arithmetic (zero-amplitude no-draw bypass; spec §6.2 as corrected)."""
    amplitude: float = 0.0

    def validate(self) -> None:
        _require(self.amplitude >= 0.0, "noise amplitude must be >= 0")


@dataclass(frozen=True)
class RunConfig:
    seed: int
    rule_mode: str = "symmetric_chain"
    f_dispatch: str = "F_canonical"
    grid_scale: int = 50
    ticks: int = 3000
    constants: DynamicsConstants = field(default_factory=DynamicsConstants)
    q: QConfig = field(default_factory=QConfig)
    init: InitConfig = field(default_factory=InitConfig)
    noise: NoiseConfig = field(default_factory=NoiseConfig)
    drive_schedule: Tuple[Tuple[int, float], ...] = ()   # ((start_tick, u_t), ...); () => u_t = 0
    allow_legacy_f_baseline: bool = False                 # Mike-arbitrated override only
    label: str = ""

    def __post_init__(self) -> None:
        _require(isinstance(self.seed, int) and self.seed >= 0, "seed must be a non-negative int")
        _require(self.rule_mode in RULE_MODES, f"rule_mode must be one of {RULE_MODES}")
        _require(self.f_dispatch in F_DISPATCH_LABELS,
                 f"f_dispatch must be one of {F_DISPATCH_LABELS}")
        if self.f_dispatch == F_BASELINE:
            _require(self.allow_legacy_f_baseline,
                     "F_baseline is carried legacy-unused; selecting it requires Mike's "
                     "arbitration (spec §2.1) — set allow_legacy_f_baseline=True only then")
        _require(self.grid_scale >= 2, "grid_scale must be >= 2")
        _require(self.ticks >= 1, "ticks must be >= 1")
        self.constants.validate(self.rule_mode)
        self.q.validate()
        self.init.validate(self.n_cells)
        if self.rule_mode == "symmetric_chain":
            _require(self.init.base_init_mode == "stochastic_ancestor",
                     "symmetric_chain requires base_init_mode='stochastic_ancestor' "
                     "(the Gate-A draw sequence); deterministic_level is the "
                     "become_survive/B-comparable policy (L2 Phase-1 review D2)")
        self.noise.validate()
        last = -1
        for start, u in self.drive_schedule:
            _require(isinstance(start, int) and 0 <= start < self.ticks,
                     "drive schedule ticks must be ints within the run")
            _require(start > last, "drive schedule must be strictly tick-ordered")
            _require(u >= 0.0, "u_t must be >= 0")
            last = start

    @property
    def n_cells(self) -> int:
        return self.grid_scale * self.grid_scale

    # -- canonical serialization (spec §7.3): UTF-8, sorted keys, no insignificant
    #    whitespace, LF; floats via repr round-trip (shortest exact) ------------
    def canonical_json(self) -> str:
        return json.dumps(dataclasses.asdict(self), sort_keys=True,
                          separators=(",", ":"), ensure_ascii=False) + "\n"

    def config_hash(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    def write_frozen(self, path: str) -> str:
        """Write run_config.json BEFORE execution from this exact object; return its hash.
        The file is never rewritten after execution (immutable-config boundary)."""
        payload = self.canonical_json()
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(payload)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_run_record(config_hash: str, telemetry_digest: str,
                     environment: Tuple[Tuple[str, str], ...],
                     completion: Tuple[Tuple[str, str], ...]) -> str:
    """run_record.json content (spec §7.3): emitted AFTER execution; references the
    config hash; sits outside every digest it reports. Canonical serialization."""
    record = {
        "config_hash": config_hash,
        "telemetry_digest": telemetry_digest,
        "environment": [list(kv) for kv in environment],
        "completion": [list(kv) for kv in completion],
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
```

# ARTIFACT: mfa_instrument/rng.py
```python
"""mfa_instrument.rng — Immutable seed provenance and role-specific stream discipline.

Spec anchors: Merge Specification v0.4 FROZEN §1.1 (single explicit Generator regime),
§6 (noise stream independent, non-interleaved; zero-amplitude => no construction).
Build Plan v0.2, L2 finding B: role-typed handles; child derivation from immutable
seed material, never by consuming draws; non-ancestor roles ABSENT (not idle) under
the Gate-A configuration.

CRITICAL Gate-A fact: the dynamics stream must be constructed EXACTLY as the ancestor
constructs it — np.random.default_rng(seed) — so the draw sequence is bit-identical
at matched seed (facts v1.1 S1(b): PRNG_SEED -> default_rng). It is therefore NOT
derived through the role registry. All other roles derive from SeedSequence
([root_seed, ROLE_CODE, *context]) and can never touch the dynamics sequence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

import numpy as np

from .config import MICRO_UNITS, ConfigError, as_micro_units

# ---------------------------------------------------------------------------
# Frozen role codes (prospectively recorded; never renumbered).
# Dynamics deliberately has NO role code: it is not registry-derived.
# ---------------------------------------------------------------------------
ROLE_CODES: Dict[str, int] = {
    "noise": 1,                # eta_MFA stream (D4); constructed only if amplitude > 0
    "observable_null": 2,      # rebuilt B null machinery (spec S1(c)(5))
    "null_generation": 3,      # E1 reference template + replicate uniforms (E1 §4.2)
    "audit": 4,                # morphology generators, held-out ensembles (E1 §7)
    "bootstrap": 5,            # level-summary and envelope bootstrap (E1 §4.3, v0.6 §D)
    "projection_ensemble": 6,  # finite-N projection sweeps (T2-S/T2-L)
}


class RoleError(TypeError):
    """Raised when a stream is requested or injected outside its role discipline."""


@dataclass(frozen=True)
class RoleStream:
    """A typed handle: the role name travels with the Generator so a module cannot
    silently receive the wrong stream. Modules type-check `role` at their boundary."""
    role: str
    generator: np.random.Generator = field(repr=False)

    def expect(self, role: str) -> np.random.Generator:
        if self.role != role:
            raise RoleError(f"stream role {self.role!r} injected where {role!r} required")
        return self.generator


@dataclass(frozen=True)
class DynamicsStream:
    """The ancestor-faithful dynamics Generator. Deliberately a distinct type from
    RoleStream: no API accepts one where the other is required."""
    generator: np.random.Generator = field(repr=False)


class SeedRegistry:
    """Immutable root; derives role streams; records every derivation prospectively.

    - Dynamics: np.random.default_rng(root_seed), ancestor-identical construction.
    - Roles: np.random.default_rng(np.random.SeedSequence([root, code, *context])).
    - Derivation NEVER consumes draws from any existing stream.
    - gate_a_mode=True: only the dynamics stream may be constructed; every role
      request raises (absence, not idleness — the strongest bypass implementation).
    """

    def __init__(self, root_seed: int, gate_a_mode: bool = False) -> None:
        if not isinstance(root_seed, int) or root_seed < 0:
            raise ConfigError("root_seed must be a non-negative int")
        self._root = root_seed
        self._gate_a = bool(gate_a_mode)
        self._derivations: list[Tuple[str, Tuple[int, ...]]] = []
        self._dynamics_built = False

    # -- dynamics ----------------------------------------------------------
    def dynamics(self) -> DynamicsStream:
        if self._dynamics_built:
            raise RoleError("dynamics stream may be constructed exactly once per run")
        self._dynamics_built = True
        self._derivations.append(("dynamics", (self._root,)))
        return DynamicsStream(np.random.default_rng(self._root))

    # -- roles -------------------------------------------------------------
    def role(self, name: str, *context: int) -> RoleStream:
        if self._gate_a:
            raise RoleError(f"role stream {name!r} requested under Gate-A configuration: "
                            "non-ancestor stochastic roles must be ABSENT (spec §8.1)")
        if name not in ROLE_CODES:
            raise RoleError(f"unknown role {name!r}; legal roles: {sorted(ROLE_CODES)}")
        for c in context:
            if not isinstance(c, int) or c < 0:
                raise ConfigError("role context values must be non-negative ints")
        key = (self._root, ROLE_CODES[name], *context)
        self._derivations.append((name, key))
        seq = np.random.SeedSequence(list(key))
        return RoleStream(role=name, generator=np.random.default_rng(seq))

    def null_generation_for_level(self, m: float) -> RoleStream:
        """Level-keyed null stream: context = exact six-decimal micro-units of m
        (E1 v0.8 §C/E: integer micro-units are the canonical level identity)."""
        return self.role("null_generation", as_micro_units(m))

    def replicate_uniform_stream(self, replicate_index: int) -> RoleStream:
        """Replicate-keyed (NOT level-keyed) uniforms, reused identically across all m
        (E1 v0.6 §B: common random numbers across the dense grid)."""
        if replicate_index < 0:
            raise ConfigError("replicate_index must be >= 0")
        return self.role("null_generation", MICRO_UNITS + 1, replicate_index)

    # -- provenance --------------------------------------------------------
    def derivations(self) -> Tuple[Tuple[str, Tuple[int, ...]], ...]:
        """Every derivation performed, in order, for prospective recording in
        run_config/run_record. Read-only snapshot."""
        return tuple(self._derivations)


def make_noise_stream(registry: SeedRegistry, amplitude: float) -> Optional[RoleStream]:
    """D4 discipline: at amplitude 0, NO stream is constructed and None is returned —
    callers must branch on None, never on amplitude comparison against a live stream."""
    if amplitude == 0.0:
        return None
    return registry.role("noise")
```

# ARTIFACT: mfa_instrument/init.py
```python
"""mfa_instrument.init — Initialization with Gate-A algorithmic lineage.

Spec anchors: Merge Specification v0.4 FROZEN §5.1 (algorithmic lineage vs. parameter
choice; Gate A freezes the exact ancestor algorithm); facts v1.1 S1(b).

Ancestor source of truth (flight2_production.py @ 4d9a622, L123–128, read verbatim
2026-08-23 — not from memory):

    for x in range(self.grid_scale[0]):
        for y in range(self.grid_scale[1]):
            self.v[x, y] = self.prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            self.u[x, y] = self.prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            self.r[x, y] = self.prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            self.is_active[x, y] = self.prng.random() < 0.5

Frozen consequences honored here:
  - scalar Generator.uniform(low, high) calls — NOT manual low + (high-low)*random(),
    which would diverge in floating point even at identical stream consumption;
  - draw order per cell: v, u_base, r, activity — cell-by-cell, x-outer/y-inner;
  - dtype float64 throughout, no intermediate coercion;
  - arrays preallocated with np.zeros exactly as the ancestor does.

`fixed_count` is a NEW merged-instrument implementation (spec §5.1 as corrected at
v0.4/blocker-1): not bit-exact preservation of Lineage B's legacy initialization,
RNG realization, or seedwise history; its dynamical behavior is Gate-B2 territory.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .config import InitConfig, ConfigError
from .rng import DynamicsStream


@dataclass(frozen=True)
class GridState:
    """Initialized model state. Ownership note (Build Plan v0.2, finding D): these
    arrays are handed to dynamics, which becomes their sole mutating owner; every
    other consumer receives read-only views or copies."""
    v: np.ndarray = field(repr=False)
    u_base: np.ndarray = field(repr=False)   # ledger: u_base, never bare u
    r: np.ndarray = field(repr=False)
    is_active: np.ndarray = field(repr=False)


def initialize(init_cfg: InitConfig, grid_scale: int, dyn: DynamicsStream) -> GridState:
    """Dispatch on the init scheme. Consumes ONLY the dynamics stream, exactly as the
    ancestor does — initialization draws are part of the Gate-A sequence.

    Base algorithm (L2 Phase-1 review D2 — CONFIG-BOUND): init_cfg.base_init_mode
    selects "stochastic_ancestor" (Gate-A cell-by-cell draws) or
    "deterministic_level" (np.full at m; zero base draws consumed; the
    become_survive/B-comparable policy). The former runner-side draw_bases switch is
    REMOVED — no unrecorded argument can change RNG consumption; the mode serializes
    in run_config.json and cross-validates against rule_mode at RunConfig level."""
    draw_bases = (init_cfg.base_init_mode == "stochastic_ancestor")
    if init_cfg.scheme == "bernoulli_p":
        return _init_bernoulli_ancestor_lineage(init_cfg, grid_scale, dyn, draw_bases)
    if init_cfg.scheme == "fixed_count":
        return _init_fixed_count(init_cfg, grid_scale, dyn, draw_bases)
    raise ConfigError(f"unknown init scheme {init_cfg.scheme!r}")   # unreachable post-validation


def _init_bernoulli_ancestor_lineage(cfg: InitConfig, grid_scale: int,
                                     dyn: DynamicsStream, draw_bases: bool = True) -> GridState:
    """The ancestor algorithm, generalized only in its (low, high) parameters.

    At m = 0.75, w = 0.3 (=> low 0.6, high 0.9), p = 0.5, this reproduces the
    ancestor's initialization bit-exactly at matched seed — asserted by test against
    a verbatim transcription of the quoted ancestor lines, and certified by Gate A.
    """
    lo = cfg.m - cfg.w / 2.0
    hi = cfg.m + cfg.w / 2.0
    shape = (grid_scale, grid_scale)
    g = dyn.generator

    is_active = np.zeros(shape, dtype=bool)
    if draw_bases:
        v = np.zeros(shape, dtype=np.float64)
        u_base = np.zeros(shape, dtype=np.float64)
        r = np.zeros(shape, dtype=np.float64)
        for x in range(shape[0]):
            for y in range(shape[1]):
                v[x, y] = g.uniform(lo, hi)
                u_base[x, y] = g.uniform(lo, hi)
                r[x, y] = g.uniform(lo, hi)
                is_active[x, y] = g.random() < cfg.bernoulli_p
    else:
        v = np.full(shape, cfg.m, dtype=np.float64)
        u_base = np.full(shape, cfg.m, dtype=np.float64)
        r = np.full(shape, cfg.m, dtype=np.float64)
        for x in range(shape[0]):
            for y in range(shape[1]):
                is_active[x, y] = g.random() < cfg.bernoulli_p

    return GridState(v=v, u_base=u_base, r=r, is_active=is_active)


def _init_fixed_count(cfg: InitConfig, grid_scale: int, dyn: DynamicsStream,
                      draw_bases: bool = True) -> GridState:
    """Merged-instrument fixed-count activity placement (declared draw order):
    bases first via the ancestor's cell-by-cell base loop (three scalar uniforms per
    cell, no activity draw), then ONE Generator.permutation over cell indices, first
    `fixed_count` cells active. New implementation; certified distributionally (B2)."""
    lo = cfg.m - cfg.w / 2.0
    hi = cfg.m + cfg.w / 2.0
    shape = (grid_scale, grid_scale)
    n_cells = grid_scale * grid_scale
    g = dyn.generator

    if draw_bases:
        v = np.zeros(shape, dtype=np.float64)
        u_base = np.zeros(shape, dtype=np.float64)
        r = np.zeros(shape, dtype=np.float64)
        for x in range(shape[0]):
            for y in range(shape[1]):
                v[x, y] = g.uniform(lo, hi)
                u_base[x, y] = g.uniform(lo, hi)
                r[x, y] = g.uniform(lo, hi)
    else:
        v = np.full(shape, cfg.m, dtype=np.float64)
        u_base = np.full(shape, cfg.m, dtype=np.float64)
        r = np.full(shape, cfg.m, dtype=np.float64)

    order = g.permutation(n_cells)
    is_active_flat = np.zeros(n_cells, dtype=bool)
    is_active_flat[order[: int(cfg.fixed_count)]] = True
    is_active = is_active_flat.reshape(shape)

    return GridState(v=v, u_base=u_base, r=r, is_active=is_active)
```

# ARTIFACT: mfa_instrument/dynamics.py
```python
"""mfa_instrument.dynamics — The unified execution core.

Spec anchors: Merge Specification v0.4 FROZEN §1.2 (common skeleton; dispatch replaces
the probability construction wholesale; become/survive computed directly, never layered
on A's chain), §2 (F dispatch incl. F_canonical slot-addition), §4 (extended Q, causal
timing, both bypasses absent-not-zero), §6.2 (noise bypass), §8.1 (Gate-A discipline).

Source-of-truth transcriptions (read from the pinned clone @ 4d9a622, not memory):
  - Lineage A step: flight2_production.py L146–252 — exact FP ordering preserved,
    including the Moore-sum accumulation ORDER (offsets list, += loop), the drive-term
    sum order, sigmoid = 1/(1+exp(-x)), telemetry BEFORE base update (Step 13 then 12).
  - Lineage B step: c3_w2_tcop.py L263–272 — p_become = sigmoid(LOGIT_L + u_t + κ·g_q)
    on inactive cells; survival at the CONSTANT p_survive ("bare p_Λ": rand < Λ);
    ONE shared rand_grid for both branches (committed discipline); its own 8-term
    neighbor-count expression.

Ownership (Build Plan v0.2, findings A/D): this module is the sole owner of mutable
v/u_base/r/is_active state and of the single authoritative causal Ψ_local computation.
Telemetry sinks receive read-only views; nothing feeds values back into Q.
"""
from __future__ import annotations

from typing import Callable, Dict, Optional

import numpy as np

from .config import RunConfig
from .init import GridState
from .rng import DynamicsStream, RoleStream

TelemetrySink = Callable[[int, Dict[str, np.ndarray]], None]

# Ancestor Moore offsets, exact list order (accumulation order affects FP sums).
_MOORE_OFFSETS_A = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def _sigmoid(x: np.ndarray) -> np.ndarray:
    """Ancestor's exact form (flight2_production.py L107): NOT scipy expit."""
    return 1.0 / (1.0 + np.exp(-x))


def _moore_sum_a(grid_matrix: np.ndarray) -> np.ndarray:
    """Verbatim ancestor accumulation (get_moore_sum): zeros_like float64, += in the
    frozen offset order."""
    total = np.zeros_like(grid_matrix, dtype=np.float64)
    for dx, dy in _MOORE_OFFSETS_A:
        total += np.roll(np.roll(grid_matrix, dx, axis=0), dy, axis=1)
    return total


def _neighbor_count_b(grid: np.ndarray) -> np.ndarray:
    """Verbatim Lineage B expression order (c3_w2_tcop.py get_neighbor_count)."""
    return (
        np.roll(grid, 1, axis=0) + np.roll(grid, -1, axis=0) +
        np.roll(grid, 1, axis=1) + np.roll(grid, -1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), -1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), -1, axis=1)
    )


class Dynamics:
    """Owns state; advances it; emits read-only telemetry fields per tick."""

    def __init__(self, cfg: RunConfig, state: GridState, dyn: DynamicsStream,
                 noise: Optional[RoleStream] = None,
                 emit_rho_global: bool = False) -> None:
        self.cfg = cfg
        self._g = dyn.generator
        # L2 review D1(a): ownership by PRIVATE COPIES — the caller's GridState
        # retains no reference to live model state; external mutation is
        # mechanically impossible, not documentation-discouraged.
        self._v = state.v.copy()
        self._u_base = state.u_base.copy()
        self._r = state.r.copy()
        self._is_active = state.is_active.copy()
        # L2 review N1: rho_global is a Gate-R recovery quantity, required in E1
        # local-primary runs where Q never reads it — emission is therefore a
        # run-mode obligation independent of Q configuration.
        self._emit_rho_global = bool(emit_rho_global)
        # N3: mechanically reject configurations this branch does not implement —
        # silent ignoring of a nonzero-Q become_survive config is the named
        # wrong-values defect class. Until the common-Q skeleton exists for
        # become_survive, such configurations are refused at construction.
        if cfg.rule_mode == "become_survive" and (cfg.q.gamma_psi != 0.0
                                                  or cfg.q.gamma_rho != 0.0):
            raise ValueError(
                "become_survive with nonzero Q coefficients is not implemented in "
                "this build phase; the frozen skeleton's Q update for this rule mode "
                "must be built (or the config changed), never silently ignored "
                "(L2 Phase-1 review N3)")
        self.tick_count = 0
        self.clipped_v_count = 0
        self.clipped_u_count = 0
        self.clipped_r_count = 0
        # D4: at amplitude 0 the caller passes None; no stream exists here at all.
        if cfg.noise.amplitude == 0.0 and noise is not None:
            raise ValueError("noise stream constructed under zero amplitude (D4 bypass violated)")
        self._noise = noise
        # Q bypass structure resolved ONCE, as absent paths, not zero-valued arithmetic.
        self._q_disabled = (cfg.q.gamma_psi == 0.0 and cfg.q.gamma_rho == 0.0)
        self._rho_read = (cfg.q.gamma_rho != 0.0)
        # Drive schedule resolved to a per-tick lookup (empty schedule => always 0.0).
        self._schedule = tuple(cfg.drive_schedule)

    # -- read-only state access (finding D: no writeable aliases leave this module) --
    def view_bases(self):
        """Durable read-only snapshots (L2 code-audit D1): copies with writeable=False.
        Copies cannot alias internal state; the flag communicates intent; protection
        cannot be lifted on the originals because callers never receive them."""
        out = []
        for arr in (self._v, self._u_base, self._r):
            c = arr.copy()
            c.flags.writeable = False
            out.append(c)
        return tuple(out)

    def snapshot_active(self) -> np.ndarray:
        return self._is_active.copy()

    def _u_t(self, tick: int) -> float:
        u = 0.0
        for start, val in self._schedule:
            if tick >= start:
                u = val
            else:
                break
        return u

    # ------------------------------------------------------------------ step
    def step(self, sink: Optional[TelemetrySink] = None) -> None:
        if self.cfg.rule_mode == "symmetric_chain":
            self._step_symmetric_chain(sink)
        else:
            self._step_become_survive(sink)
        self.tick_count += 1

    # -- Lineage A chain, ancestor FP ordering preserved ---------------------
    def _step_symmetric_chain(self, sink: Optional[TelemetrySink]) -> None:
        cfg = self.cfg
        k = cfg.constants
        tick_idx = self.tick_count

        # Step 1: pre-Q base copies (ancestor names preserved in telemetry fields)
        b_i_v = self._v.copy()
        b_i_u = self._u_base.copy()
        b_i_r = self._r.copy()

        bases_stack = np.stack([self._v, self._u_base, self._r], axis=0)
        limiting_base_argmin = np.argmin(bases_stack, axis=0)
        lambda_multiplicative = self._v * self._u_base * self._r
        lambda_additive = k.w_v * self._v + k.w_u * self._u_base + k.w_r * self._r

        # Step 2: F dispatch — ancestor branches verbatim + the D3 slot-addition.
        f = cfg.f_dispatch
        if f == "F_baseline":
            lambda_total = (self._v + self._u_base + self._r) / 3.0
        elif f == "F_LR":
            lambda_total = np.min(bases_stack, axis=0)
        elif f == "F_2_symmetric":
            lambda_total = lambda_multiplicative * lambda_additive
        elif f == "F_canonical":
            lambda_total = lambda_multiplicative  # Λ = v·u_base·r (already computed)
        else:  # unreachable post-validation
            raise ValueError(f"Unknown F-form: {f}")

        # Step 3: local density
        active_int = self._is_active.astype(np.float64)
        local_density = _moore_sum_a(active_int) / 8.0

        # Step 4: drive components — ancestor term names and sum order; u_t appended
        # ONLY when nonzero (absent at zero: Gate-A arithmetic identical to ancestor).
        term_lambda = k.alpha * lambda_total
        term_density_pos = k.beta * local_density
        term_overcrowding = -k.delta * (local_density ** 2)
        term_offset = np.full_like(self._v, -k.gamma_offset)
        drive_raw = term_lambda + term_density_pos + term_overcrowding + term_offset
        u_t = self._u_t(tick_idx)
        if u_t != 0.0:
            drive_raw = drive_raw + u_t
        # D4 noise: absent at amplitude 0 (no stream exists); additive when enabled.
        if self._noise is not None:
            noise_draw = self._noise.expect("noise").normal(
                0.0, cfg.noise.amplitude, size=drive_raw.shape)
            drive_raw = drive_raw + noise_draw
        else:
            noise_draw = None

        # Step 5: probability chain (eta_floor is ancestor ETA)
        p_base = _sigmoid(drive_raw)
        p_act = np.clip(p_base + k.eta_floor * (1.0 - p_base), 0.0, 1.0)

        # Pre-update rho_global (D2 causal timing when Q consumes it; N1: also a
        # Gate-R recovery artifact requested by run mode regardless of Q's read).
        if (self._rho_read and cfg.q.q_read == "global") or self._emit_rho_global:
            rho_global = float(np.mean(self._is_active))
        else:
            rho_global = None

        # Step 6: one full-grid draw
        prng_draw = self._g.random(size=(cfg.grid_scale, cfg.grid_scale))
        next_state = prng_draw < p_act

        # Steps 7–8: synchronous advance
        ds = next_state.astype(int) - self._is_active.astype(int)
        self._is_active = next_state.copy()

        # Step 9: causal Psi_local — THE authoritative mechanism computation.
        sum_neighbor_ds = _moore_sum_a(ds.astype(np.float64))
        psi_local = ds * sum_neighbor_ds

        # Step 11 (Q deltas), computed here so telemetry can carry them, but the
        # base UPDATE stays after telemetry per ancestor order (Step 13 then 12).
        # (L2 code-audit D3: components computed here, always as arrays; telemetry
        # receives clean grid-shaped fields and does no dynamics inference.)
        if self._q_disabled:
            delta = None            # E1 total-Q-disable: no arithmetic exists.
            delta_from_psi = delta_from_rho = None
        elif not self._rho_read:
            delta = cfg.q.gamma_psi * psi_local        # ancestor expression exactly
            delta_from_psi = delta_from_rho = None     # decomposition columns absent
        else:
            if cfg.q.q_read == "local":
                rho_term = cfg.q.gamma_rho * local_density
            else:
                rho_term = np.full_like(psi_local, cfg.q.gamma_rho * rho_global,
                                        dtype=np.float64)
            if cfg.q.gamma_psi == 0.0:
                psi_term = np.zeros_like(psi_local, dtype=np.float64)
                delta = rho_term
            else:
                psi_term = cfg.q.gamma_psi * psi_local
                delta = psi_term + rho_term
            delta_from_psi, delta_from_rho = psi_term, rho_term

        # Step 13: telemetry BEFORE base update (ancestor order). Read-only fields.
        # (L2 code-audit D1: live state is COPIED before exposure; every field is a
        # per-tick temporary or a copy; all are frozen once and never un-frozen —
        # dynamics only READS them after this point, and they go out of scope.)
        if sink is not None:
            fields: Dict[str, np.ndarray] = {
                "b_i_v": b_i_v, "b_i_u": b_i_u, "b_i_r": b_i_r,
                "limiting_base_argmin": limiting_base_argmin,
                "Lambda_multiplicative": lambda_multiplicative,
                "Lambda_additive": lambda_additive, "Lambda_total": lambda_total,
                "Local_Density": local_density, "Drive_Raw": drive_raw,
                "Term_Density_Pos": term_density_pos,
                "Term_Overcrowding": term_overcrowding, "Term_Offset": term_offset,
                "p_base": p_base, "p_act": p_act, "PRNG_draw": prng_draw,
                "is_active": self._is_active.copy(), "Psi_local": psi_local,
                "Term_Lambda": term_lambda,
            }
            if delta is not None:
                # L2 review D1(b): delta is used causally AFTER the sink returns
                # (the Step-12 base update); telemetry receives a COPY so no sink,
                # however misbehaved, can alter the subsequent Q update.
                delta_telem = delta.copy()
                if delta_from_psi is not None:
                    fields["Delta_from_Psi"] = delta_from_psi
                    fields["Delta_from_rho"] = delta_from_rho
                fields["Delta_v"] = delta_telem
                fields["Delta_u"] = delta_telem
                fields["Delta_r"] = delta_telem
            if rho_global is not None:
                fields["rho_global"] = np.float64(rho_global)
            if noise_draw is not None:
                fields["Noise_Draw"] = noise_draw
            for a in fields.values():
                if isinstance(a, np.ndarray):
                    a.flags.writeable = False
            sink(tick_idx, fields)

        # Step 12: base update with clip counters — ONLY when Q arithmetic exists.
        if delta is not None:
            v_new = self._v + delta
            u_new = self._u_base + delta
            r_new = self._r + delta
            self.clipped_v_count += int(np.sum((v_new < 0.0) | (v_new > 1.0)))
            self.clipped_u_count += int(np.sum((u_new < 0.0) | (u_new > 1.0)))
            self.clipped_r_count += int(np.sum((r_new < 0.0) | (r_new > 1.0)))
            self._v = np.clip(v_new, 0.0, 1.0)
            self._u_base = np.clip(u_new, 0.0, 1.0)
            self._r = np.clip(r_new, 0.0, 1.0)

    # -- Lineage B rule, computed directly (never layered on A's chain) ------
    def _step_become_survive(self, sink: Optional[TelemetrySink]) -> None:
        cfg = self.cfg
        k = cfg.constants
        tick_idx = self.tick_count
        u_t = self._u_t(tick_idx)

        grid = self._is_active.astype(int)
        neighbors = _neighbor_count_b(grid)
        q_i = neighbors / 8.0
        g_q = 2.0 * q_i - 1.0
        p_become = _sigmoid(k.logit_l + u_t + k.kappa * g_q)

        rand_grid = self._g.random(size=(cfg.grid_scale, cfg.grid_scale))  # ONE shared grid
        become_active = (grid == 0) & (rand_grid < p_become)
        stay_active = (grid == 1) & (rand_grid < k.p_survive)   # bare p_Λ: constant
        next_grid = (become_active | stay_active)

        ds = next_grid.astype(int) - grid
        self._is_active = next_grid.copy()
        psi_local = ds * _moore_sum_a(ds.astype(np.float64))    # mechanism emission

        if sink is not None:
            fields = {"p_become": p_become, "g_q": g_q, "rand_grid": rand_grid,
                      "is_active": self._is_active.copy(), "Psi_local": psi_local}
            for a in fields.values():
                a.flags.writeable = False
            sink(tick_idx, fields)
        # Bases untouched: become_survive runs frozen-bases configurations (spec §1.3).
```

# ARTIFACT: mfa_instrument/telemetry.py
```python
"""mfa_instrument.telemetry — Row-family emission, parquet streaming, canonical digest.

Spec anchors: Merge Specification v0.4 FROZEN §7.1 (25-column ancestor family +
Delta_from_Psi/Delta_from_rho + conditional Noise_Draw; rho_global tick table),
§7.3 (canonical telemetry digest: parquet files' raw bytes in ascending lexicographic
filename order, each preceded by its filename as a UTF-8 line), §8.1 (instrumentation
must not alter state, evaluation order, dtype, or stochastic consumption — this module
only reads the read-only field views the dynamics sink provides).

Ancestor column order (flight2_production.py @ 4d9a622, telemetry row dict, verbatim):
Tick, Agent_X, Agent_Y, b_i_v, b_i_u, b_i_r, limiting_base_argmin,
Lambda_multiplicative, Lambda_additive, Lambda_total, Local_Density, Drive_Raw,
Term_Density_Pos, Term_Overcrowding, Term_Offset, p_base, p_act, PRNG_draw,
is_active, Psi_local, gamma_coef, Delta_v, Delta_u, Delta_r, Term_Lambda  (25 columns)

Row order: per tick, cells in np.indices row-major flatten order (ancestor xs/ys loop).
"""
from __future__ import annotations

import hashlib
import os
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ANCESTOR_COLUMNS = [
    "Tick", "Agent_X", "Agent_Y", "b_i_v", "b_i_u", "b_i_r", "limiting_base_argmin",
    "Lambda_multiplicative", "Lambda_additive", "Lambda_total", "Local_Density",
    "Drive_Raw", "Term_Density_Pos", "Term_Overcrowding", "Term_Offset", "p_base",
    "p_act", "PRNG_draw", "is_active", "Psi_local", "gamma_coef", "Delta_v",
    "Delta_u", "Delta_r", "Term_Lambda",
]
EXTENSION_COLUMNS = ["Delta_from_Psi", "Delta_from_rho"]   # spec §4.5, when rho channel active
NOISE_COLUMN = "Noise_Draw"                                 # conditional (η_MFA enabled)


class TelemetryWriter:
    """Builds per-tick row frames from the dynamics sink fields (vectorized; values
    identical to the ancestor's per-cell loop) and streams them to parquet in chunks.

    Schema policy: the column set is fixed at construction from the configuration —
    Gate-A configurations carry exactly the 25 ancestor columns (extension columns
    STRUCTURALLY ABSENT, per §8.1's preflight); rho-channel configurations add the
    two decomposition columns; noise-enabled adds Noise_Draw. E1 total-Q-disable
    drops gamma_coef/Delta_v/u/r (no Q arithmetic exists to report).
    """

    def __init__(self, grid_scale: int, gamma_psi: float, gamma_rho: float,
                 noise_enabled: bool, chunk_ticks: int = 500) -> None:
        self._gs = grid_scale
        xs, ys = np.indices((grid_scale, grid_scale))
        self._xs = xs.flatten()
        self._ys = ys.flatten()
        self._gamma_psi = gamma_psi
        q_disabled = (gamma_psi == 0.0 and gamma_rho == 0.0)
        cols = list(ANCESTOR_COLUMNS)
        if q_disabled:
            for c in ("gamma_coef", "Delta_v", "Delta_u", "Delta_r"):
                cols.remove(c)
        if gamma_rho != 0.0:
            cols += EXTENSION_COLUMNS
        if noise_enabled:
            cols.append(NOISE_COLUMN)
        self.columns = cols
        self._chunk_ticks = chunk_ticks
        self._frames: List[pd.DataFrame] = []
        self._ticks_buffered = 0
        self._writer: Optional[pq.ParquetWriter] = None
        self._schema: Optional[pa.Schema] = None
        self._path: Optional[str] = None
        self.rows_written = 0
        self.rho_global_table: List[tuple] = []   # (tick, rho_global) tick-level table (§7.2)

    # -- sink --------------------------------------------------------------
    def sink(self, tick: int, fields: Dict[str, np.ndarray]) -> None:
        n = self._xs.size
        data: Dict[str, np.ndarray] = {
            "Tick": np.full(n, tick, dtype=np.int64),
            "Agent_X": self._xs.astype(np.int64),
            "Agent_Y": self._ys.astype(np.int64),
        }
        for col in self.columns:
            if col in data:
                continue
            if col == "gamma_coef":
                data[col] = np.full(n, self._gamma_psi, dtype=np.float64)
            else:
                data[col] = np.asarray(fields[col]).reshape(-1)
        if "rho_global" in fields:
            self.rho_global_table.append((tick, float(fields["rho_global"])))
        self._frames.append(pd.DataFrame(data, columns=self.columns))
        self._ticks_buffered += 1
        if self._path is not None and self._ticks_buffered >= self._chunk_ticks:
            self._flush()

    # -- parquet streaming (ancestor pattern: schema from first chunk, snappy) ----
    def open(self, path: str) -> None:
        self._path = path

    def _flush(self) -> None:
        if not self._frames:
            return
        df = pd.concat(self._frames, ignore_index=True)
        if self._writer is None:
            table = pa.Table.from_pandas(df, preserve_index=False)
            self._schema = table.schema
            self._writer = pq.ParquetWriter(self._path, self._schema, compression="snappy")
            self._writer.write_table(table)
        else:
            table = pa.Table.from_pandas(df, preserve_index=False, schema=self._schema)
            self._writer.write_table(table)
        self.rows_written += len(df)
        self._frames.clear()
        self._ticks_buffered = 0

    def close(self) -> None:
        if self._path is not None:
            self._flush()
        if self._writer is not None:
            self._writer.close()
            self._writer = None
        # N2 (L2 Phase-1 review): the rho_global tick table is a REQUIRED persisted
        # artifact wherever it is populated — an in-memory list is not the spec's
        # tick-level table. Written beside the row file as <stem>.rho_global.parquet;
        # its filename enters the same canonical digest set as every telemetry file.
        if self._path is not None and self.rho_global_table:
            rho_df = pd.DataFrame(self.rho_global_table, columns=["Tick", "rho_global"])
            self.rho_global_path = self._path.rsplit(".parquet", 1)[0] + ".rho_global.parquet"
            rho_df.to_parquet(self.rho_global_path, index=False)
        else:
            self.rho_global_path = None

    def artifact_paths(self) -> List[str]:
        """Every persisted artifact of this writer, for the canonical digest."""
        out = []
        if self._path is not None:
            out.append(self._path)
        if getattr(self, "rho_global_path", None):
            out.append(self.rho_global_path)
        return out

    # -- in-memory access (harness/test use) -------------------------------
    def frame(self) -> pd.DataFrame:
        """Concatenated buffered frames. ONLY valid in pure in-memory use: if the
        writer was opened for streaming, buffered frames are a partial tail and
        returning them would silently misrepresent the run (L2 code-audit D6)."""
        if self._path is not None:
            raise RuntimeError("frame() is unavailable on a streaming writer: rows have "
                               "been flushed to disk; read the parquet file instead")
        return pd.concat(self._frames, ignore_index=True) if self._frames else pd.DataFrame(columns=self.columns)


def telemetry_digest(paths: List[str]) -> str:
    """Spec §7.3 canonical construction: SHA-256 over the concatenation of the files'
    raw bytes in ascending lexicographic FILENAME order, each preceded by its filename
    as a UTF-8 line ('<name>\\n'). Filenames therefore enter the digest; the run record
    is outside every digest it reports."""
    names = [os.path.basename(p) for p in paths]
    if len(set(names)) != len(names):
        raise ValueError("telemetry_digest requires unique basenames: the canonical "
                         "construction is filename-keyed (L2 code-audit D6)")
    h = hashlib.sha256()
    for p in sorted(paths, key=lambda q: os.path.basename(q)):
        h.update((os.path.basename(p) + "\n").encode("utf-8"))
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    return h.hexdigest()
```

# ARTIFACT: mfa_instrument/verify.py
```python
"""mfa_instrument.verify — Tier-1 row-level recomputation (the verification spine).

Spec anchors: Merge Specification v0.4 FROZEN §7.2. Rebuilt per L2 Phase-1 review
V1–V5: the verifier is now SCHEMA- AND COMPLETENESS-ENFORCING —

  V1: the expected column set is BUILT FROM THE CONFIGURATION and compared against
      the file before any recomputation; missing columns and forbidden columns both
      fail. Conditional artifacts (Noise_Draw; the rho_global tick table) are
      required-or-forbidden by configuration, never merely tolerated.
  V2: the global-Q decomposition is verified (Delta_from_rho == gamma_rho *
      rho_global(t), joined by tick against the persisted tick table).
  V3: completeness is enforced from the consumed configuration: rows_seen must equal
      ticks * grid_scale^2; every tick 0..ticks-1 present; exactly one row per
      (Tick, Agent_X, Agent_Y); full coordinate coverage. An empty report FAILS
      (all([]) can never again mean PASS).
  V4: E1 base identity is BITWISE (float64 storage via view(np.uint64)), tick-0
      anchored, coverage-enforcing, empty-rejecting, and asserts the absence of
      every Q-related column including the decomposition pair.
  V5: every persisted component in the declared families is checked — Term_Offset,
      gamma_coef, Delta_from_Psi (including the gamma_psi == 0 zero requirement),
      global Delta_from_rho, and the rho_global tick table itself.

All value checks remain EXACT equality: tolerances would hide the FP-ordering
divergence Tier-1 exists to catch.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Tuple

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from .config import RunConfig
from .telemetry import ANCESTOR_COLUMNS, EXTENSION_COLUMNS, NOISE_COLUMN


@dataclass
class Tier1Report:
    checks: Dict[str, int] = field(default_factory=dict)   # name -> mismatch count
    rows_seen: int = 0
    ticks_seen: Tuple[int, int] = (0, 0)

    def record(self, name: str, mismatches: int) -> None:
        self.checks[name] = self.checks.get(name, 0) + int(mismatches)

    @property
    def passed(self) -> bool:
        # V3: an empty report is a FAILURE, not a vacuous pass.
        if not self.checks or self.rows_seen == 0:
            return False
        return all(v == 0 for v in self.checks.values())

    def summary(self) -> str:
        parts = [f"{k}={'OK' if v == 0 else f'{v} MISMATCHES'}" for k, v in self.checks.items()]
        return (f"TIER-1 rows={self.rows_seen} ticks={self.ticks_seen[0]}..{self.ticks_seen[1]} "
                + " ".join(parts) + (" => PASS" if self.passed else " => FAIL"))


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def expected_schema(cfg: RunConfig) -> Set[str]:
    """V1: the required column set, derived from the consumed configuration exactly
    as TelemetryWriter derives its schema — but independently, so a writer defect
    cannot define its own expectation."""
    cols = set(ANCESTOR_COLUMNS)
    if cfg.q.gamma_psi == 0.0 and cfg.q.gamma_rho == 0.0:
        cols -= {"gamma_coef", "Delta_v", "Delta_u", "Delta_r"}
    if cfg.q.gamma_rho != 0.0:
        cols |= set(EXTENSION_COLUMNS)
    if cfg.noise.amplitude > 0.0:
        cols.add(NOISE_COLUMN)
    return cols


def tier1_verify(parquet_path: str, cfg: RunConfig,
                 rho_global_path: Optional[str] = None,
                 expect_rho_global: Optional[bool] = None,
                 batch_size: int = 200_000) -> Tier1Report:
    """Stream the telemetry and recompute every Tier-1 invariant, with schema and
    completeness enforced before and during recomputation.

    expect_rho_global: whether the run was a Gate-R/rho-emitting run (defaults to
    the Q-global condition; E1 Gate-R runs pass True explicitly per spec §7.2)."""
    rep = Tier1Report()
    k = cfg.constants
    if expect_rho_global is None:
        expect_rho_global = (cfg.q.gamma_rho != 0.0 and cfg.q.q_read == "global")

    # ---- V1: schema gate ----
    pf = pq.ParquetFile(parquet_path)
    have = set(pf.schema_arrow.names)
    want = expected_schema(cfg)
    rep.record("schema_missing_columns", len(want - have))
    rep.record("schema_forbidden_columns", len(have - want))
    if want != have:
        return rep   # recomputation on a wrong-schema file proves nothing

    # ---- rho_global tick table: required-or-forbidden (V1/N1/N2) ----
    rho_df: Optional[pd.DataFrame] = None
    if expect_rho_global:
        if rho_global_path is None:
            rep.record("rho_global_artifact_missing", 1)
            return rep
        rho_df = pd.read_parquet(rho_global_path)
        rep.record("rho_global_schema",
                   0 if list(rho_df.columns) == ["Tick", "rho_global"] else 1)
        rep.record("rho_global_tick_coverage",
                   0 if np.array_equal(np.sort(rho_df["Tick"].to_numpy()),
                                       np.arange(cfg.ticks)) else 1)
    else:
        rep.record("rho_global_artifact_forbidden", 0 if rho_global_path is None else 1)

    # ---- streaming recomputation with completeness accounting (V3) ----
    n_cells = cfg.n_cells
    tick_row_counts = np.zeros(cfg.ticks, dtype=np.int64)
    dup_or_range_bad = 0
    coord_bad = 0
    rho_map = (dict(zip(rho_df["Tick"].to_numpy(), rho_df["rho_global"].to_numpy()))
               if rho_df is not None else {})

    t_min: Optional[int] = None
    t_max: Optional[int] = None

    for batch in pf.iter_batches(batch_size=batch_size):
        df = batch.to_pandas()
        n = len(df)
        rep.rows_seen += n
        ticks = df["Tick"].to_numpy()
        if ticks.size:
            t_min = int(ticks.min()) if t_min is None else min(t_min, int(ticks.min()))
            t_max = int(ticks.max()) if t_max is None else max(t_max, int(ticks.max()))
        in_range = (ticks >= 0) & (ticks < cfg.ticks)
        dup_or_range_bad += int((~in_range).sum())
        np.add.at(tick_row_counts, ticks[in_range], 1)
        xy_ok = ((df["Agent_X"].to_numpy() >= 0) & (df["Agent_X"].to_numpy() < cfg.grid_scale)
                 & (df["Agent_Y"].to_numpy() >= 0) & (df["Agent_Y"].to_numpy() < cfg.grid_scale))
        coord_bad += int((~xy_ok).sum())
        key = (ticks.astype(np.int64) * n_cells
               + df["Agent_X"].to_numpy(np.int64) * cfg.grid_scale
               + df["Agent_Y"].to_numpy(np.int64))
        dup_or_range_bad += int(n - np.unique(key).size)

        # 1. Realization invariant.
        rep.record("realization_invariant",
                   int((df["is_active"] != (df["PRNG_draw"] < df["p_act"])).sum()))

        # 2. Λ recomputation per dispatch label.
        v, u, r = (df["b_i_v"].to_numpy(), df["b_i_u"].to_numpy(), df["b_i_r"].to_numpy())
        lam_mult = v * u * r
        lam_add = k.w_v * v + k.w_u * u + k.w_r * r
        rep.record("lambda_multiplicative",
                   int((df["Lambda_multiplicative"].to_numpy() != lam_mult).sum()))
        rep.record("lambda_additive",
                   int((df["Lambda_additive"].to_numpy() != lam_add).sum()))
        f = cfg.f_dispatch
        if f == "F_baseline":
            lam = (v + u + r) / 3.0
        elif f == "F_LR":
            lam = np.minimum(np.minimum(v, u), r)
        elif f == "F_2_symmetric":
            lam = lam_mult * lam_add
        else:
            lam = lam_mult
        rep.record("lambda_total_dispatch",
                   int((df["Lambda_total"].to_numpy() != lam).sum()))

        # 3. Drive decomposition — every persisted component (V5).
        dens = df["Local_Density"].to_numpy()
        term_lambda = k.alpha * df["Lambda_total"].to_numpy()
        term_dens = k.beta * dens
        term_over = -k.delta * (dens ** 2)
        term_off = np.full_like(v, -k.gamma_offset)
        drive = term_lambda + term_dens + term_over + term_off
        if cfg.drive_schedule:
            u_t_col = np.zeros(n, dtype=np.float64)
            for start, val in cfg.drive_schedule:
                u_t_col = np.where(ticks >= start, val, u_t_col)
            nonzero = u_t_col != 0.0
            drive = np.where(nonzero, drive + u_t_col, drive)
        if NOISE_COLUMN in have:
            drive = drive + df[NOISE_COLUMN].to_numpy()
        rep.record("term_lambda", int((df["Term_Lambda"].to_numpy() != term_lambda).sum()))
        rep.record("term_density_pos", int((df["Term_Density_Pos"].to_numpy() != term_dens).sum()))
        rep.record("term_overcrowding", int((df["Term_Overcrowding"].to_numpy() != term_over).sum()))
        rep.record("term_offset", int((df["Term_Offset"].to_numpy() != term_off).sum()))
        rep.record("drive_raw", int((df["Drive_Raw"].to_numpy() != drive).sum()))

        # 4. Probability chain.
        p_base = _sigmoid(df["Drive_Raw"].to_numpy())
        p_act = np.clip(p_base + k.eta_floor * (1.0 - p_base), 0.0, 1.0)
        rep.record("p_base", int((df["p_base"].to_numpy() != p_base).sum()))
        rep.record("p_act", int((df["p_act"].to_numpy() != p_act).sum()))

        # 5. Q decomposition — applicability guaranteed by the V1 schema gate.
        if "Delta_v" in want:
            psi = df["Psi_local"].to_numpy()
            rep.record("gamma_coef",
                       int((df["gamma_coef"].to_numpy() != cfg.q.gamma_psi).sum()))
            if "Delta_from_rho" in want:
                dpsi = df["Delta_from_Psi"].to_numpy()
                drho = df["Delta_from_rho"].to_numpy()
                rep.record("q_decomposition_sum",
                           int((df["Delta_v"].to_numpy() != dpsi + drho).sum()))
                if cfg.q.gamma_psi != 0.0:
                    rep.record("delta_from_psi",
                               int((dpsi != cfg.q.gamma_psi * psi).sum()))
                else:
                    rep.record("delta_from_psi_zero", int((dpsi != 0.0).sum()))   # V5
                if cfg.q.q_read == "local":
                    rep.record("delta_from_rho_local",
                               int((drho != cfg.q.gamma_rho * dens).sum()))
                else:                                                              # V2
                    expected = np.array([cfg.q.gamma_rho * rho_map.get(t, np.nan)
                                         for t in ticks])
                    rep.record("delta_from_rho_global",
                               int((drho != expected).sum()))
            else:
                rep.record("q_ancestor_expression",
                           int((df["Delta_v"].to_numpy() != cfg.q.gamma_psi * psi).sum()))
            rep.record("q_uniform_across_bases",
                       int((df["Delta_v"].to_numpy() != df["Delta_u"].to_numpy()).sum()
                           + (df["Delta_v"].to_numpy() != df["Delta_r"].to_numpy()).sum()))

    # ---- V3 completeness verdicts ----
    rep.record("rows_total",
               0 if rep.rows_seen == cfg.ticks * n_cells else 1)
    rep.record("tick_coverage_exact",
               0 if bool(np.all(tick_row_counts == n_cells)) else 1)
    rep.record("row_duplication_or_range", dup_or_range_bad)
    rep.record("coordinate_range", coord_bad)
    rep.ticks_seen = (t_min if t_min is not None else -1,
                      t_max if t_max is not None else -1)
    return rep


def e1_base_bit_identity(parquet_path: str, cfg: RunConfig,
                         batch_size: int = 200_000) -> Tier1Report:
    """Contract E1 v0.8 §2 conformance, rebuilt per V4: TRUE bitwise identity
    (float64 storage compared as uint64 views), tick-0 anchored, coverage-enforced,
    empty-rejecting, with the full Q-column absence set asserted."""
    rep = Tier1Report()
    pf = pq.ParquetFile(parquet_path)
    cols = set(pf.schema_arrow.names)
    for q_col in ("Delta_v", "Delta_u", "Delta_r", "gamma_coef",
                  "Delta_from_Psi", "Delta_from_rho"):        # V4: full set
        rep.record(f"schema_absent_{q_col}", 0 if q_col not in cols else 1)

    n_cells = cfg.n_cells
    base_bits: Dict[int, Tuple[int, int, int]] = {}
    tick0_seen = np.zeros(n_cells, dtype=bool)
    tick_row_counts = np.zeros(cfg.ticks, dtype=np.int64)
    mismatches = 0
    anchored_late = 0

    for batch in pf.iter_batches(batch_size=batch_size,
                                 columns=["Tick", "Agent_X", "Agent_Y",
                                          "b_i_v", "b_i_u", "b_i_r"]):
        df = batch.to_pandas()
        rep.rows_seen += len(df)
        ticks = df["Tick"].to_numpy()
        in_range = (ticks >= 0) & (ticks < cfg.ticks)
        np.add.at(tick_row_counts, ticks[in_range], 1)
        keys = (df["Agent_X"].to_numpy(np.int64) * cfg.grid_scale
                + df["Agent_Y"].to_numpy(np.int64))
        bv = df["b_i_v"].to_numpy(np.float64).view(np.uint64)
        bu = df["b_i_u"].to_numpy(np.float64).view(np.uint64)
        br = df["b_i_r"].to_numpy(np.float64).view(np.uint64)
        for i in range(len(df)):
            key = int(keys[i]); t = int(ticks[i])
            bits = (int(bv[i]), int(bu[i]), int(br[i]))
            if t == 0:
                base_bits[key] = bits
                tick0_seen[key] = True
            else:
                if key not in base_bits:
                    anchored_late += 1        # V4: no first-row anchoring allowed
                elif bits != base_bits[key]:
                    mismatches += 1

    rep.record("base_bit_identity", mismatches)
    rep.record("tick0_baseline_complete", 0 if bool(tick0_seen.all()) else 1)
    rep.record("anchored_without_tick0", anchored_late)
    rep.record("rows_total", 0 if rep.rows_seen == cfg.ticks * n_cells else 1)
    rep.record("tick_coverage_exact",
               0 if bool(np.all(tick_row_counts == n_cells)) else 1)
    return rep
```

# ARTIFACT: mfa_instrument/gates/gate_a.py
```python
"""mfa_instrument.gates.gate_a — Gate A: Lineage A preservation (bit-exact, conditional).

Spec anchors: Merge Specification v0.4 FROZEN §8.1 — two-level harness:
  STRUCTURAL PREFLIGHT (diagnostic, never a substitute): six checks establishing that
  the Gate-A configuration executes no extension path;
  BEHAVIORAL CERTIFICATION (the actual gate): complete matched-seed comparison against
  flight2_production.py — bit-exact state and telemetry equality.

PROVISIONAL vs AUTHORITATIVE (Build Plan v0.2, L2 finding 1): any run of this harness
during build is a CHECKPOINT; the certification is only the final run on the complete
integrated stage-1 commit, on Mike's machine, under the frozen environment. Every
report emitted here is labeled accordingly.

The ancestor is IMPORTED FROM THE PINNED SOURCE FILE (never transcribed): the
comparison target is flight2_production.NumpyEEModel itself.
"""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
import pandas as pd

from ..config import RunConfig, QConfig, InitConfig
from ..rng import SeedRegistry, RoleError
from ..init import initialize
from ..dynamics import Dynamics
from ..telemetry import TelemetryWriter, ANCESTOR_COLUMNS

GATE_A_SEED = 0x7A9B31C          # facts v1.1 S6(a): the matched seed
ANCESTOR_GAMMA_Q = 0.001          # ancestor GAMMA_Q; Gate-A gamma_psi


def load_ancestor(pinned_repo_root: str, expected_sha256: "str|None" = None,
                  require_provenance: bool = False):
    """Import the ancestor module from the pinned clone, with provenance
    verification (L2 Phase-1 review N4): the file's SHA-256 is computed and,
    when an expectation is supplied (mandatory for AUTHORITATIVE runs), enforced
    BEFORE import — the harness must never certify parity against a modified or
    wrong reference. The digest is returned for the report either way."""
    import hashlib
    path = pinned_repo_root + "/" + ANCESTOR_REL_PATH
    with open(path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    if require_provenance and expected_sha256 is None:
        raise RuntimeError("AUTHORITATIVE Gate A requires an expected ancestor "
                           "digest; none supplied (L2 Phase-1 review N4)")
    if expected_sha256 is not None and digest != expected_sha256:
        raise RuntimeError(f"ancestor provenance FAILED: {path} has sha256 {digest}, "
                           f"expected {expected_sha256}")
    spec = importlib.util.spec_from_file_location("flight2_production", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["flight2_production"] = mod
    spec.loader.exec_module(mod)
    return mod, digest


def gate_a_config(f_form: str, grid_scale: int, ticks: int) -> RunConfig:
    """The channels-zeroed Gate-A configuration (spec §8.1): symmetric_chain, A's
    constants (config defaults), u_t = 0 (empty schedule), noise 0 (no stream),
    gamma_rho = 0 (no-read bypass), gamma_psi = ancestor GAMMA_Q, ancestor init
    parameters, ancestor-existing f_form (F_canonical has no ancestor branch)."""
    if f_form == "F_canonical":
        raise ValueError("Gate A requires an ancestor-existing F form (no F_canonical "
                         "branch exists at 4d9a622)")
    return RunConfig(
        seed=GATE_A_SEED, rule_mode="symmetric_chain", f_dispatch=f_form,
        grid_scale=grid_scale, ticks=ticks,
        q=QConfig(q_read="local", gamma_psi=ANCESTOR_GAMMA_Q, gamma_rho=0.0),
        init=InitConfig(),                     # m=0.75, w=0.3 => U(0.6, 0.9); p=0.5
        allow_legacy_f_baseline=(f_form == "F_baseline"),
    )


@dataclass
class PreflightReport:
    checks: List[Tuple[str, bool]] = field(default_factory=list)

    def record(self, name: str, ok: bool) -> None:
        self.checks.append((name, ok))

    @property
    def passed(self) -> bool:
        return all(ok for _, ok in self.checks)


def structural_preflight(cfg: RunConfig) -> PreflightReport:
    """Spec §8.1's six checks, run on a short constructed execution. Diagnostic only."""
    rep = PreflightReport()
    # (i) Gate-A registry forbids every non-ancestor stream (absence, not idleness).
    reg = SeedRegistry(cfg.seed, gate_a_mode=True)
    try:
        reg.role("noise")
        rep.record("noise_stream_absent", False)
    except RoleError:
        rep.record("noise_stream_absent", True)
    dyn = reg.dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    d = Dynamics(cfg, state, dyn)
    # (ii) no rho read is configured; the activation-read branch is unreachable.
    rep.record("no_rho_read_configured", d._rho_read is False)
    # (iii) telemetry schema: extension columns structurally absent.
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho, False)
    rep.record("delta_from_rho_structurally_absent",
               "Delta_from_rho" not in tw.columns and "Delta_from_Psi" not in tw.columns)
    rep.record("noise_column_absent", "Noise_Draw" not in tw.columns)
    # (iv) rho_global never computed: run ticks, assert tick table stays empty.
    seen = {}
    for _ in range(3):
        d.step(lambda t, f: seen.update(f))
    rep.record("rho_global_never_emitted", "rho_global" not in seen
               and len(tw.rho_global_table) == 0)
    # (v) dynamics-stream consumption equals ancestor expectation:
    #     init draws = 4 * n_cells scalars (v,u,r,activity per cell); per tick = one
    #     grid-shaped draw. An independent probe replays exactly that consumption.
    n = cfg.n_cells
    probe = np.random.default_rng(cfg.seed)
    for _ in range(n):
        probe.uniform(0.6, 0.9); probe.uniform(0.6, 0.9); probe.uniform(0.6, 0.9)
        probe.random()
    for _ in range(3):
        probe.random(size=(cfg.grid_scale, cfg.grid_scale))
    rep.record("draw_count_and_order_match",
               bool(np.array_equal(d._g.random(7), probe.random(7))))
    return rep


FROZEN_PYTHON_PREFIX = "3.14."     # spec §7.4 working assumption (executable hard-fail)
FROZEN_NUMPY = "2.4.4"             # spec §7.4 lock-file pin
GATE_A_LABELS = ("PROVISIONAL", "AUTHORITATIVE")   # closed set (L2 Phase-1 review D5)
# N4: ancestor provenance — the authoritative comparison target's frozen identity.
ANCESTOR_REL_PATH = ("flights/cycle2_round1/02_flight_1_v1_1_parity/"
                     "flight2_production.py")
ANCESTOR_SHA256 = None   # frozen at first authoritative-machine read; see load_ancestor


@dataclass
class GateAReport:
    label: str                     # member of GATE_A_LABELS (closed set)
    f_form: str
    grid_scale: int
    ticks: int
    preflight: PreflightReport
    state_bit_exact: bool
    telemetry_bit_exact: bool
    environment: str
    ancestor_sha256: str = ""

    @property
    def behavioral_bit_exact(self) -> bool:
        """The behavioral comparison alone (L2 D5 separation)."""
        return self.state_bit_exact and self.telemetry_bit_exact

    @property
    def gate_passed(self) -> bool:
        """The two-level harness verdict: BOTH layers (frozen §8.1). A failed
        structural preflight can never be silently absorbed (L2 review N5)."""
        return self.preflight.passed and self.behavioral_bit_exact

    # `passed` retained as an alias of the harness verdict so no consumer can
    # accidentally read the weaker property under the stronger name.
    @property
    def passed(self) -> bool:
        return self.gate_passed

    def summary(self) -> str:
        return (f"GATE A [{self.label}] f={self.f_form} grid={self.grid_scale} "
                f"ticks={self.ticks} preflight={'PASS' if self.preflight.passed else 'FAIL'} "
                f"state={'BIT-EXACT' if self.state_bit_exact else 'DIVERGED'} "
                f"telemetry={'BIT-EXACT' if self.telemetry_bit_exact else 'DIVERGED'} "
                f"gate={'PASS' if self.gate_passed else 'FAIL'} "
                f"ancestor_sha256={self.ancestor_sha256[:12]} env={self.environment}")


def run_gate_a(pinned_repo_root: str, f_form: str, grid_scale: int, ticks: int,
               label: str = "PROVISIONAL",
               expected_ancestor_sha256: "str|None" = None) -> GateAReport:
    """Two-level harness: structural preflight + behavioral comparison against the
    ancestor class itself, matched seed, full state + telemetry rows, bitwise."""
    import platform
    if label not in GATE_A_LABELS:
        raise ValueError(f"Gate-A label must be one of {GATE_A_LABELS}, got {label!r} "
                         "(closed set; L2 Phase-1 review D5)")
    anc_mod, anc_digest = load_ancestor(pinned_repo_root, expected_ancestor_sha256,
                                        require_provenance=(label == "AUTHORITATIVE"))
    cfg = gate_a_config(f_form, grid_scale, ticks)

    # Ancestor: its own class, its own module-level PRNG_SEED (verify it matches).
    assert anc_mod.PRNG_SEED == GATE_A_SEED, "ancestor seed constant mismatch"
    anc = anc_mod.NumpyEEModel((grid_scale, grid_scale), f_form)

    # Ours.
    reg = SeedRegistry(cfg.seed, gate_a_mode=True)
    dyn = reg.dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    ours = Dynamics(cfg, state, dyn)
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho, False)

    state_ok = True
    telem_ok = True
    for _ in range(ticks):
        anc.step()
        ours.step(tw.sink)
        state_ok &= (np.array_equal(ours._v, anc.v) and
                     np.array_equal(ours._u_base, anc.u) and
                     np.array_equal(ours._r, anc.r) and
                     np.array_equal(ours._is_active, anc.is_active))
        if not state_ok:
            break

    if state_ok:
        anc_df = pd.DataFrame(anc.telemetry_buffer)[ANCESTOR_COLUMNS]
        our_df = tw.frame()[ANCESTOR_COLUMNS]
        telem_ok = anc_df.shape == our_df.shape and all(
            np.array_equal(anc_df[c].to_numpy(), our_df[c].to_numpy())
            for c in ANCESTOR_COLUMNS)
    else:
        telem_ok = False

    env = f"python{platform.python_version()}/numpy{np.__version__}"
    env_conforms = (platform.python_version().startswith(FROZEN_PYTHON_PREFIX)
                    and np.__version__ == FROZEN_NUMPY)
    if label == "AUTHORITATIVE" and not env_conforms:
        raise RuntimeError(
            f"AUTHORITATIVE Gate A refused: environment {env} does not conform to the "
            f"frozen pins (python {FROZEN_PYTHON_PREFIX}x / numpy {FROZEN_NUMPY}); "
            "run on the canonical venv (L2 code-audit D5). PROVISIONAL runs may proceed "
            "in non-conforming environments and are labeled accordingly.")
    if not env_conforms:
        env += " [NON-CONFORMING: provisional only]"
    return GateAReport(label=label, f_form=f_form, grid_scale=grid_scale, ticks=ticks,
                       preflight=structural_preflight(cfg),
                       state_bit_exact=bool(state_ok), telemetry_bit_exact=bool(telem_ok),
                       environment=env, ancestor_sha256=anc_digest)
```

# ARTIFACT: tests/test_config_rng.py
```python
"""Tests for config.py and rng.py — Build Plan v0.2 first deliverables.
Pessimistic-on-passing: each test names what alternative it discriminates against."""
import dataclasses, json, sys
import numpy as np
import pytest

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.config import (RunConfig, DynamicsConstants, QConfig, InitConfig,
                                   NoiseConfig, ConfigError, as_micro_units, build_run_record)
from mfa_instrument.rng import SeedRegistry, RoleError, DynamicsStream, make_noise_stream

# ---- config: immutability (vs. silently mutable shared state) ----
def test_config_deeply_immutable():
    c = RunConfig(seed=5)
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.seed = 6
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.q.gamma_psi = 1.0

# ---- config: canonical serialization is stable and key-sorted ----
def test_canonical_json_stable_and_sorted():
    a = RunConfig(seed=5).canonical_json()
    b = RunConfig(seed=5).canonical_json()
    assert a == b and a.endswith("\n") and " " not in a.split('"label"')[0]
    keys = list(json.loads(a).keys())
    assert keys == sorted(keys)

def test_config_hash_changes_with_content():
    assert RunConfig(seed=5).config_hash() != RunConfig(seed=6).config_hash()

# ---- config: naming-ledger validation (vs. wrong-values-under-right-names) ----
def test_ledger_enums_enforced():
    with pytest.raises(ConfigError): RunConfig(seed=1, rule_mode="mesa")
    with pytest.raises(ConfigError): RunConfig(seed=1, f_dispatch="F_multiplicative")
    with pytest.raises(ConfigError):
        RunConfig(seed=1, q=QConfig(q_read="aggregate"))

def test_f_baseline_requires_arbitration_flag():
    with pytest.raises(ConfigError): RunConfig(seed=1, f_dispatch="F_baseline")
    RunConfig(seed=1, f_dispatch="F_baseline", allow_legacy_f_baseline=True)  # ok

def test_kappa_quarantined_from_symmetric_chain():
    with pytest.raises(ConfigError):
        RunConfig(seed=1, constants=DynamicsConstants(kappa=0.2, logit_l=-1.0, p_survive=0.4))
    RunConfig(seed=1, rule_mode="become_survive",
              constants=DynamicsConstants(kappa=0.2, logit_l=-1.0, p_survive=0.4))  # ok
    with pytest.raises(ConfigError):  # missing p_survive
        RunConfig(seed=1, rule_mode="become_survive",
                  constants=DynamicsConstants(kappa=0.2, logit_l=-1.0))

# ---- config: six-decimal exactness and no-clipping (E1 §3, v0.8) ----
def test_micro_units_exactness():
    assert as_micro_units(0.030435) == 30435
    with pytest.raises(ConfigError): as_micro_units(0.70/23)  # non-terminating
def test_base_interval_no_clipping():
    with pytest.raises(ConfigError):
        RunConfig(seed=1, init=InitConfig(base_center_micro=100_000, base_width_micro=300_000))

# ---- config: drive schedule ordering ----
def test_drive_schedule_ordering():
    RunConfig(seed=1, drive_schedule=((0, 0.0), (25, 0.5)))
    with pytest.raises(ConfigError):
        RunConfig(seed=1, drive_schedule=((25, 0.5), (0, 0.0)))

# ---- run record: outside its own digest, references config hash ----
def test_run_record_shape():
    rec = json.loads(build_run_record("aa", "bb", (("python","3.14.0"),), (("status","ok"),)))
    assert rec["config_hash"] == "aa" and rec["telemetry_digest"] == "bb"

# ---- rng: dynamics stream is ancestor-identical (vs. registry-derived divergence) ----
def test_dynamics_matches_ancestor_construction():
    reg = SeedRegistry(0x7A9B31C)
    ours = reg.dynamics().generator.random(1000)
    ancestor = np.random.default_rng(0x7A9B31C).random(1000)
    assert np.array_equal(ours, ancestor)

def test_dynamics_constructed_once():
    reg = SeedRegistry(1); reg.dynamics()
    with pytest.raises(RoleError): reg.dynamics()

# ---- rng: role streams independent of dynamics consumption ----
def test_role_streams_do_not_consume_dynamics():
    r1 = SeedRegistry(9); d1 = r1.dynamics().generator
    r1.role("audit"); r1.role("bootstrap", 3)
    after = d1.random(100)
    d2 = SeedRegistry(9).dynamics().generator
    assert np.array_equal(after, d2.random(100))

def test_role_streams_deterministic_and_distinct():
    a = SeedRegistry(9).role("audit").generator.random(10)
    b = SeedRegistry(9).role("audit").generator.random(10)
    c = SeedRegistry(9).role("bootstrap").generator.random(10)
    assert np.array_equal(a, b) and not np.array_equal(a, c)

# ---- rng: typed handles reject wrong-role injection ----
def test_role_handle_expect():
    s = SeedRegistry(9).role("audit")
    with pytest.raises(RoleError): s.expect("bootstrap")
    s.expect("audit")

# ---- rng: Gate-A absence discipline (vs. idle-but-present streams) ----
def test_gate_a_mode_forbids_roles():
    reg = SeedRegistry(0x7A9B31C, gate_a_mode=True)
    reg.dynamics()
    with pytest.raises(RoleError): reg.role("noise")
    with pytest.raises(RoleError): reg.null_generation_for_level(0.75)

# ---- rng: D4 zero-amplitude => None, no construction ----
def test_noise_bypass_returns_none():
    reg = SeedRegistry(9)
    assert make_noise_stream(reg, 0.0) is None
    assert all(name != "noise" for name, _ in reg.derivations())
    assert make_noise_stream(reg, 0.1) is not None

# ---- rng: level keys are exact micro-units; replicate keys cannot collide with them ----
def test_level_and_replicate_keys():
    reg = SeedRegistry(9)
    a = reg.null_generation_for_level(0.150000).generator.random(5)
    b = reg.null_generation_for_level(0.150001).generator.random(5)
    assert not np.array_equal(a, b)
    with pytest.raises(ConfigError): reg.null_generation_for_level(0.1234567)
    r = reg.replicate_uniform_stream(0).generator.random(5)
    assert not np.array_equal(r, a)

def test_provenance_recorded():
    reg = SeedRegistry(9); reg.dynamics(); reg.role("audit", 7)
    names = [n for n, _ in reg.derivations()]
    assert names == ["dynamics", "audit"]
```

# ARTIFACT: tests/test_init.py
```python
"""Tests for init.py — Gate-A algorithmic lineage.
The reference implementation below is a VERBATIM transcription of the ancestor's
initialization lines (flight2_production.py @ 4d9a622, L117-128), executed against
the same Generator construction. Bit-equality against it is the discriminating test:
a call-shape substitution (e.g., lo + (hi-lo)*random()) or a loop-order change fails it."""
import sys
import numpy as np
import pytest

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.config import InitConfig, RunConfig
from mfa_instrument.rng import SeedRegistry
from mfa_instrument.init import initialize

PRNG_SEED = 0x7A9B31C
BASE_INIT_LOW, BASE_INIT_HIGH = 0.6, 0.9

def ancestor_reference(grid_scale):
    """Verbatim ancestor transcription (tuple grid_scale as in source)."""
    gs = (grid_scale, grid_scale)
    prng = np.random.default_rng(PRNG_SEED)
    v = np.zeros(gs, dtype=np.float64)
    u = np.zeros(gs, dtype=np.float64)
    r = np.zeros(gs, dtype=np.float64)
    is_active = np.zeros(gs, dtype=bool)
    for x in range(gs[0]):
        for y in range(gs[1]):
            v[x, y] = prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            u[x, y] = prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            r[x, y] = prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            is_active[x, y] = prng.random() < 0.5
    return v, u, r, is_active, prng

def test_bernoulli_bitexact_vs_ancestor_transcription():
    for gs in (5, 20):
        cfg = InitConfig()  # m=0.75, w=0.3 => (0.6, 0.9); p=0.5
        state = initialize(cfg, gs, SeedRegistry(PRNG_SEED).dynamics())
        av, au, ar, aa, _ = ancestor_reference(gs)
        assert np.array_equal(state.v, av)          # bitwise: array_equal on float64
        assert np.array_equal(state.u_base, au)
        assert np.array_equal(state.r, ar)
        assert np.array_equal(state.is_active, aa)

def test_post_init_stream_position_matches_ancestor():
    """After init, the NEXT draws must coincide — position in the sequence matters
    for the per-tick grid draw that follows (Gate-A sequence discipline)."""
    gs = 7
    state_dyn = SeedRegistry(PRNG_SEED).dynamics()
    initialize(InitConfig(), gs, state_dyn)
    _, _, _, _, ancestor_prng = ancestor_reference(gs)
    assert np.array_equal(state_dyn.generator.random(size=(gs, gs)),
                          ancestor_prng.random(size=(gs, gs)))

def test_dtypes_frozen():
    s = initialize(InitConfig(), 6, SeedRegistry(3).dynamics())
    assert s.v.dtype == np.float64 and s.u_base.dtype == np.float64
    assert s.r.dtype == np.float64 and s.is_active.dtype == bool

def test_general_level_bounds_and_determinism():
    cfg = InitConfig(base_center_micro=300_000, base_width_micro=300_000)  # U(0.15,0.45)
    a = initialize(cfg, 10, SeedRegistry(11).dynamics())
    b = initialize(cfg, 10, SeedRegistry(11).dynamics())
    assert np.array_equal(a.v, b.v) and np.array_equal(a.is_active, b.is_active)
    for arr in (a.v, a.u_base, a.r):
        assert arr.min() >= 0.15 and arr.max() <= 0.45

def test_fixed_count_exact_and_deterministic():
    cfg = InitConfig(scheme="fixed_count", fixed_count=25, bernoulli_p=0.5)
    # fixed_count requires validation via RunConfig path? InitConfig.validate needs n_cells:
    cfg.validate(100)
    a = initialize(cfg, 10, SeedRegistry(4).dynamics())
    b = initialize(cfg, 10, SeedRegistry(4).dynamics())
    assert int(a.is_active.sum()) == 25
    assert np.array_equal(a.is_active, b.is_active)
    assert np.array_equal(a.v, b.v)

def test_fixed_count_differs_from_bernoulli_lineage():
    """Discriminates: fixed_count is a NEW implementation, not the ancestor path —
    at matched seed its activity pattern must not equal the Bernoulli lineage's."""
    bern = initialize(InitConfig(), 10, SeedRegistry(4).dynamics())
    fc_cfg = InitConfig(scheme="fixed_count", fixed_count=int(bern.is_active.sum()))
    fc = initialize(fc_cfg, 10, SeedRegistry(4).dynamics())
    assert not np.array_equal(bern.is_active, fc.is_active)
```

# ARTIFACT: tests/test_dynamics.py
```python
"""Tests for dynamics.py. The A-side reference is a verbatim transcription of the
ancestor's NumpyEEModel (flight2_production.py @ 4d9a622); the B-side reference is a
verbatim transcription of step_tcop_core (c3_w2_tcop.py). Bit-equality against these
discriminates FP-ordering, draw-order, and update-order divergence."""
import sys
import numpy as np
import pytest

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.config import RunConfig, DynamicsConstants, QConfig, InitConfig, NoiseConfig
from mfa_instrument.rng import SeedRegistry
from mfa_instrument.init import initialize
from mfa_instrument.dynamics import Dynamics, _sigmoid

PRNG_SEED = 0x7A9B31C
ALPHA, BETA, DELTA, GAMMA_OFFSET, ETA, GAMMA_Q = 4.0, 3.0, 4.0, 4.0, 0.01, 0.001
W_V, W_U, W_R = 0.33, 0.33, 0.34
LOW, HIGH = 0.6, 0.9

class AncestorModel:
    """Verbatim transcription of the ancestor step (telemetry loop omitted; all
    per-tick arrays captured for comparison)."""
    MOORE = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    def __init__(self, gs, f_form):
        self.gs = (gs, gs); self.f_form = f_form
        self.prng = np.random.default_rng(PRNG_SEED)
        self.v = np.zeros(self.gs, dtype=np.float64)
        self.u = np.zeros(self.gs, dtype=np.float64)
        self.r = np.zeros(self.gs, dtype=np.float64)
        self.is_active = np.zeros(self.gs, dtype=bool)
        for x in range(gs):
            for y in range(gs):
                self.v[x,y] = self.prng.uniform(LOW, HIGH)
                self.u[x,y] = self.prng.uniform(LOW, HIGH)
                self.r[x,y] = self.prng.uniform(LOW, HIGH)
                self.is_active[x,y] = self.prng.random() < 0.5
    def moore(self, m):
        t = np.zeros_like(m, dtype=np.float64)
        for dx, dy in self.MOORE:
            t += np.roll(np.roll(m, dx, axis=0), dy, axis=1)
        return t
    def step(self):
        bases = np.stack([self.v, self.u, self.r], axis=0)
        lam_mult = self.v * self.u * self.r
        lam_add = W_V*self.v + W_U*self.u + W_R*self.r
        if self.f_form == "F_baseline": lam = (self.v + self.u + self.r) / 3.0
        elif self.f_form == "F_LR": lam = np.min(bases, axis=0)
        elif self.f_form == "F_2_symmetric": lam = lam_mult * lam_add
        else: raise ValueError
        dens = self.moore(self.is_active.astype(np.float64)) / 8.0
        drive = ALPHA*lam + BETA*dens + (-DELTA*(dens**2)) + np.full_like(self.v, -GAMMA_OFFSET)
        p_base = 1.0/(1.0+np.exp(-drive))
        p_act = np.clip(p_base + ETA*(1.0-p_base), 0.0, 1.0)
        draw = self.prng.random(size=self.gs)
        nxt = draw < p_act
        ds = nxt.astype(int) - self.is_active.astype(int)
        self.is_active = nxt.copy()
        psi = ds * self.moore(ds.astype(np.float64))
        delta = GAMMA_Q * psi
        self.last = dict(drive=drive, p_base=p_base, p_act=p_act, draw=draw, psi=psi, delta=delta)
        vn, un, rn = self.v+delta, self.u+delta, self.r+delta
        self.v, self.u, self.r = np.clip(vn,0,1), np.clip(un,0,1), np.clip(rn,0,1)

def make_ours(f_form, gamma_psi=GAMMA_Q, gamma_rho=0.0, q_read="local", gs=12,
              allow_baseline=False, schedule=()):
    cfg = RunConfig(seed=PRNG_SEED, f_dispatch=f_form, grid_scale=gs, ticks=3000,
                    q=QConfig(q_read=q_read, gamma_psi=gamma_psi, gamma_rho=gamma_rho),
                    allow_legacy_f_baseline=allow_baseline, drive_schedule=schedule)
    dyn = SeedRegistry(PRNG_SEED, gate_a_mode=(gamma_rho==0.0 and not schedule)).dynamics()
    state = initialize(cfg.init, gs, dyn)
    return cfg, Dynamics(cfg, state, dyn)

@pytest.mark.parametrize("f_form,allow", [("F_2_symmetric",False),("F_LR",False),("F_baseline",True)])
def test_symmetric_chain_bitexact_vs_ancestor(f_form, allow):
    gs = 12
    anc = AncestorModel(gs, f_form)
    _, ours = make_ours(f_form, allow_baseline=allow, gs=gs)
    captured = {}
    def sink(t, fields): captured.update({k: np.array(v) for k, v in fields.items()})
    for _ in range(5):
        anc.step(); ours.step(sink)
    assert np.array_equal(ours._v, anc.v)          # bases bit-identical after 5 Q ticks
    assert np.array_equal(ours._u_base, anc.u)
    assert np.array_equal(ours._r, anc.r)
    assert np.array_equal(ours._is_active, anc.is_active)
    assert np.array_equal(captured["Drive_Raw"], anc.last["drive"])
    assert np.array_equal(captured["p_act"], anc.last["p_act"])
    assert np.array_equal(captured["PRNG_draw"], anc.last["draw"])
    assert np.array_equal(captured["Psi_local"], anc.last["psi"])
    assert np.array_equal(captured["Delta_v"], anc.last["delta"])

def test_e1_total_q_disable_bases_bit_identical():
    cfg, ours = make_ours("F_canonical", gamma_psi=0.0, gamma_rho=0.0)
    v0, u0, r0 = ours._v.copy(), ours._u_base.copy(), ours._r.copy()
    for _ in range(20): ours.step()
    assert np.array_equal(ours._v, v0) and np.array_equal(ours._u_base, u0)
    assert np.array_equal(ours._r, r0)
    assert ours.clipped_v_count == 0  # no clip machinery ran

def test_f_canonical_is_triple_product():
    _, ours = make_ours("F_canonical", gamma_psi=0.0)
    got = {}
    ours.step(lambda t, f: got.update(f))
    assert np.array_equal(got["Lambda_total"], got["Lambda_multiplicative"])

def test_u_t_zero_is_absent_not_added():
    """Same seed, one config with empty schedule, one with explicit (0, 0.0):
    drive must be bit-identical (absence == explicit zero here because the branch
    doesn't execute at u_t==0.0)."""
    _, a = make_ours("F_2_symmetric"); _, b = make_ours("F_2_symmetric", schedule=((0,0.0),))
    ga, gb = {}, {}
    a.step(lambda t,f: ga.update(f)); b.step(lambda t,f: gb.update(f))
    assert np.array_equal(ga["Drive_Raw"], gb["Drive_Raw"])

def test_u_t_nonzero_shifts_drive():
    _, a = make_ours("F_2_symmetric"); _, b = make_ours("F_2_symmetric", schedule=((0,0.5),))
    ga, gb = {}, {}
    a.step(lambda t,f: ga.update(f)); b.step(lambda t,f: gb.update(f))
    assert np.allclose(gb["Drive_Raw"] - ga["Drive_Raw"], 0.5)

def test_global_q_read_moves_bases_uniformly():
    cfg, ours = make_ours("F_canonical", gamma_psi=0.0, gamma_rho=0.01, q_read="global")
    v0 = ours._v.copy()
    got = {}
    ours.step(lambda t,f: got.update(f))
    assert "rho_global" in got
    dv = ours._v - v0
    assert np.allclose(dv, dv.flat[0])  # common-mode write: identical delta everywhere

def test_local_q_read_moves_bases_locally():
    cfg, ours = make_ours("F_canonical", gamma_psi=0.0, gamma_rho=0.01, q_read="local")
    v0 = ours._v.copy()
    ours.step()
    dv = ours._v - v0
    assert not np.allclose(dv, dv.flat[0])  # varies with Local_Density

def test_noise_stream_under_zero_amplitude_rejected():
    cfg, _ = make_ours("F_2_symmetric")
    reg = SeedRegistry(1)
    dyn = reg.dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    with pytest.raises(ValueError):
        Dynamics(cfg, state, dyn, noise=reg.role("noise"))

# ---- become_survive vs verbatim B transcription ----
B_LAMBDA = 0.40
B_LOGIT = float(np.log(B_LAMBDA/(1.0-B_LAMBDA)))
def b_reference_step(grid, u_t, kappa, rand_grid):
    n = (np.roll(grid,1,0)+np.roll(grid,-1,0)+np.roll(grid,1,1)+np.roll(grid,-1,1)+
         np.roll(np.roll(grid,1,0),1,1)+np.roll(np.roll(grid,1,0),-1,1)+
         np.roll(np.roll(grid,-1,0),1,1)+np.roll(np.roll(grid,-1,0),-1,1))
    g_q = 2.0*(n/8.0)-1.0
    p_become = 1.0/(1.0+np.exp(-(B_LOGIT+u_t+kappa*g_q)))
    become = (grid==0)&(rand_grid<p_become)
    stay = (grid==1)&(rand_grid<B_LAMBDA)
    return (become|stay).astype(int), p_become

def test_become_survive_rule_equivalence_mini_b1():
    gs = 10
    cfg = RunConfig(seed=77, rule_mode="become_survive", grid_scale=gs,
                    init=InitConfig(scheme="fixed_count", fixed_count=10),
                    constants=DynamicsConstants(logit_l=B_LOGIT, kappa=0.2, p_survive=B_LAMBDA),
                    drive_schedule=((0, 0.3),))
    dyn = SeedRegistry(77).dynamics()
    state = initialize(cfg.init, gs, dyn)
    ours = Dynamics(cfg, state, dyn)
    grid_ref = state.is_active.astype(int).copy()
    # replay our stream's draws through the reference:
    shadow = SeedRegistry(77).dynamics().generator
    initialize(cfg.init, gs, type("D", (), {"generator": shadow})())  # consume init draws identically
    got = {}
    for _ in range(4):
        rand_grid = shadow.random(size=(gs, gs))
        grid_ref, p_ref = b_reference_step(grid_ref, 0.3, 0.2, rand_grid)
        ours.step(lambda t, f: got.update({k: np.array(v) for k, v in f.items()}))
        assert np.array_equal(got["p_become"], p_ref)
        assert np.array_equal(got["rand_grid"], rand_grid)
        assert np.array_equal(ours._is_active.astype(int), grid_ref)

def test_become_survive_survival_invariant_to_drive_and_coupling():
    """Facts v1.1: survival invariant to u_t and kappa — p_survive is the constant."""
    gs = 8
    def run(kappa, u):
        cfg = RunConfig(seed=5, rule_mode="become_survive", grid_scale=gs,
                        init=InitConfig(scheme="fixed_count", fixed_count=64),  # all active
                        constants=DynamicsConstants(logit_l=B_LOGIT, kappa=kappa, p_survive=B_LAMBDA),
                        drive_schedule=((0, u),) if u else ())
        dyn = SeedRegistry(5).dynamics()
        d = Dynamics(cfg, initialize(cfg.init, gs, dyn), dyn)
        d.step()
        return d._is_active.copy()
    assert np.array_equal(run(0.0, 0.0), run(0.9, 0.7))  # all-active grid: only survival acts
```

# ARTIFACT: tests/test_telemetry_gate_a.py
```python
"""Telemetry + provisional Gate A. The Gate-A test imports the ACTUAL ancestor file
from the pinned clone — the strongest available discriminator short of the
authoritative run on the execution machine."""
import sys, os, tempfile
import numpy as np
import pandas as pd
import pytest

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.telemetry import TelemetryWriter, telemetry_digest, ANCESTOR_COLUMNS
from mfa_instrument.gates.gate_a import run_gate_a, gate_a_config, structural_preflight

REPO = "/home/claude/repo"

def test_gate_a_schema_is_exactly_ancestor_25():
    tw = TelemetryWriter(10, 0.001, 0.0, False)
    assert tw.columns == ANCESTOR_COLUMNS and len(tw.columns) == 25

def test_e1_schema_drops_q_columns():
    tw = TelemetryWriter(10, 0.0, 0.0, False)
    for c in ("gamma_coef", "Delta_v", "Delta_u", "Delta_r", "Delta_from_rho"):
        assert c not in tw.columns

def test_rho_schema_adds_decomposition():
    tw = TelemetryWriter(10, 0.0, 0.01, False)
    assert "Delta_from_Psi" in tw.columns and "Delta_from_rho" in tw.columns

def test_digest_canonical_construction():
    with tempfile.TemporaryDirectory() as td:
        a, b = os.path.join(td, "b.parquet"), os.path.join(td, "a.parquet")
        open(a, "wb").write(b"BBB"); open(b, "wb").write(b"AAA")
        d1 = telemetry_digest([a, b])
        d2 = telemetry_digest([b, a])          # order-insensitive input, filename-sorted
        assert d1 == d2
        import hashlib
        h = hashlib.sha256()
        h.update(b"a.parquet\n"); h.update(b"AAA")
        h.update(b"b.parquet\n"); h.update(b"BBB")
        assert d1 == h.hexdigest()             # exact spec construction

def test_gate_a_rejects_f_canonical():
    with pytest.raises(ValueError):
        gate_a_config("F_canonical", 10, 5)

def test_structural_preflight_passes():
    rep = structural_preflight(gate_a_config("F_2_symmetric", 8, 3))
    assert rep.passed, rep.checks

@pytest.mark.parametrize("f_form", ["F_2_symmetric", "F_LR", "F_baseline"])
def test_provisional_gate_a_against_actual_ancestor(f_form):
    rep = run_gate_a(REPO, f_form, grid_scale=12, ticks=25, label="PROVISIONAL")
    assert rep.preflight.passed, rep.preflight.checks
    assert rep.state_bit_exact, rep.summary()
    assert rep.telemetry_bit_exact, rep.summary()

def test_parquet_roundtrip_and_rho_table():
    from mfa_instrument.config import RunConfig, QConfig
    from mfa_instrument.rng import SeedRegistry
    from mfa_instrument.init import initialize
    from mfa_instrument.dynamics import Dynamics
    cfg = RunConfig(seed=3, f_dispatch="F_canonical", grid_scale=6, ticks=10,
                    q=QConfig(q_read="global", gamma_psi=0.0, gamma_rho=0.01))
    dyn = SeedRegistry(3).dynamics()
    d = Dynamics(cfg, initialize(cfg.init, 6, dyn), dyn)
    tw = TelemetryWriter(6, 0.0, 0.01, False, chunk_ticks=4)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw.open(p)
        for _ in range(10):
            d.step(tw.sink)
        tw.close()
        df = pd.read_parquet(p)
        assert len(df) == 10 * 36 and tw.rows_written == 360
        assert len(tw.rho_global_table) == 10       # tick-level table, one row per tick
        assert "Delta_from_rho" in df.columns
        # realization invariant holds on the written file
        assert bool((df["is_active"] == (df["PRNG_draw"] < df["p_act"])).all())
```

# ARTIFACT: tests/test_verify.py
```python
"""Tests for verify.py (V1-V5 rebuild) — negative matrix expanded per V7:
schema (missing/forbidden), completeness (empty/truncated/dropped/duplicated),
global-Q, rho_global artifact, Term_Offset, gamma_coef, raw-bit identity.
Path binding per V6: repo-relative via conftest-style pathing, no absolute L1 path."""
import os, sys, tempfile
import numpy as np
import pandas as pd
import pytest

# V6: repo-relative import — the package root is this test file's parent's parent.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.config import RunConfig, QConfig, InitConfig, DynamicsConstants
from mfa_instrument.rng import SeedRegistry
from mfa_instrument.init import initialize
from mfa_instrument.dynamics import Dynamics
from mfa_instrument.telemetry import TelemetryWriter
from mfa_instrument.verify import tier1_verify, e1_base_bit_identity, expected_schema

def run_to_parquet(cfg, path, emit_rho=False):
    reg = SeedRegistry(cfg.seed, gate_a_mode=(cfg.q.gamma_rho == 0.0 and not cfg.drive_schedule
                                              and cfg.noise.amplitude == 0.0 and not emit_rho))
    dyn = reg.dynamics()
    d = Dynamics(cfg, initialize(cfg.init, cfg.grid_scale, dyn), dyn, emit_rho_global=emit_rho)
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho,
                         cfg.noise.amplitude > 0, chunk_ticks=5)
    tw.open(path)
    for _ in range(cfg.ticks):
        d.step(tw.sink)
    tw.close()
    return tw

def gate_a_cfg(**kw):
    d = dict(seed=0x7A9B31C, f_dispatch="F_2_symmetric", grid_scale=8, ticks=12,
             q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    d.update(kw); return RunConfig(**d)

def test_tier1_passes_clean_run():
    cfg = gate_a_cfg()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = tier1_verify(p, cfg)
        assert rep.passed, rep.summary()
        assert rep.rows_seen == 12 * 64

def test_tier1_global_q_with_rho_artifact():
    """V2: global decomposition verified against the persisted tick table."""
    cfg = RunConfig(seed=9, f_dispatch="F_canonical", grid_scale=8, ticks=10,
                    q=QConfig(q_read="global", gamma_psi=0.001, gamma_rho=0.02))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw = run_to_parquet(cfg, p)
        assert tw.rho_global_path is not None            # N2: artifact persisted
        rep = tier1_verify(p, cfg, rho_global_path=tw.rho_global_path)
        assert rep.passed, rep.summary()
        # plant a wrong global decomposition value
        df = pd.read_parquet(p); df.loc[df.index[100], "Delta_from_rho"] += 1e-15
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep2 = tier1_verify(p2, cfg, rho_global_path=tw.rho_global_path)
        assert not rep2.passed and rep2.checks["delta_from_rho_global"] > 0

def test_tier1_missing_rho_artifact_fails():
    cfg = RunConfig(seed=9, f_dispatch="F_canonical", grid_scale=6, ticks=5,
                    q=QConfig(q_read="global", gamma_psi=0.0, gamma_rho=0.02))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = tier1_verify(p, cfg, rho_global_path=None)
        assert not rep.passed and rep.checks["rho_global_artifact_missing"] == 1

def test_tier1_e1_local_gate_r_rho_emission():
    """N1: E1 total-Q-disable run CAN emit rho_global as a Gate-R obligation."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=8,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw = run_to_parquet(cfg, p, emit_rho=True)
        assert tw.rho_global_path is not None
        rep = tier1_verify(p, cfg, rho_global_path=tw.rho_global_path,
                           expect_rho_global=True)
        assert rep.passed, rep.summary()

def test_tier1_schema_missing_column_fails():
    """V1: a run generated under active Q with a Q column REMOVED must fail."""
    cfg = gate_a_cfg()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p).drop(columns=["Delta_v"])
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep = tier1_verify(p2, cfg)
        assert not rep.passed and rep.checks["schema_missing_columns"] > 0

def test_tier1_schema_forbidden_column_fails():
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=4,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p); df["Delta_v"] = 0.0     # forbidden under total-disable
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep = tier1_verify(p2, cfg)
        assert not rep.passed and rep.checks["schema_forbidden_columns"] > 0

def test_tier1_empty_truncated_dropped_duplicated_fail():
    """V3: the completeness matrix."""
    cfg = gate_a_cfg(grid_scale=6, ticks=6)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        cases = {
            "empty": full.iloc[0:0],
            "dropped_tick": full[full.Tick != 3],
            "dropped_row": full.drop(index=full.index[77]),
            "duplicated_row": pd.concat([full, full.iloc[[50]]], ignore_index=True),
        }
        for name, df in cases.items():
            p2 = os.path.join(td, f"{name}.parquet"); df.to_parquet(p2)
            rep = tier1_verify(p2, cfg)
            assert not rep.passed, f"{name}: {rep.summary()}"

def test_tier1_catches_planted_value_defects():
    cfg = gate_a_cfg(f_dispatch="F_LR", grid_scale=8, ticks=6)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        for col, check, mut in [
            ("is_active", "realization_invariant", lambda x: not x),
            ("Lambda_total", "lambda_total_dispatch", lambda x: x + 1e-12),
            ("Drive_Raw", "drive_raw", lambda x: x + 1e-9),
            ("Term_Offset", "term_offset", lambda x: x + 1e-12),      # V5
            ("gamma_coef", "gamma_coef", lambda x: x + 1e-9),          # V5
            ("p_act", "p_act", lambda x: min(1.0, x + 1e-12)),
            ("Delta_v", "q_ancestor_expression", lambda x: x + 1e-15),
        ]:
            df = pd.read_parquet(p)
            df.loc[df.index[37], col] = mut(df.loc[df.index[37], col])
            p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
            rep = tier1_verify(p2, cfg)
            assert not rep.passed and rep.checks[check] > 0, (col, rep.summary())

def test_e1_bit_identity_true_bitwise():
    """V4: negative-zero substitution — numerically equal, bitwise different."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=8,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = e1_base_bit_identity(p, cfg)
        assert rep.passed, rep.summary()
        df = pd.read_parquet(p)
        # plant -0.0 over +0.0-like: force a value whose bits differ but compares ==
        idx = df[(df.Tick == 5)].index[3]
        orig = df.loc[idx, "b_i_v"]
        df.loc[idx, "b_i_v"] = np.nextafter(orig, np.inf)   # 1-ulp bit change
        p2 = os.path.join(td, "ulp.parquet"); df.to_parquet(p2)
        rep2 = e1_base_bit_identity(p2, cfg)
        assert not rep2.passed and rep2.checks["base_bit_identity"] == 1
        # negative-zero case, explicit
        df2 = pd.read_parquet(p)
        z_idx = df2.index[10]
        df2.loc[df2[df2.Tick == 0].index, "b_i_u"] = 0.0     # tick-0 baseline +0.0
        df2.loc[df2[(df2.Tick > 0)].index, "b_i_u"] = 0.0
        df2.loc[df2[(df2.Tick == 4)].index[7], "b_i_u"] = -0.0
        p3 = os.path.join(td, "negzero.parquet"); df2.to_parquet(p3)
        rep3 = e1_base_bit_identity(p3, cfg)
        assert rep3.checks["base_bit_identity"] >= 1        # == would have passed it

def test_e1_bit_identity_coverage_and_empty():
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=6,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        for name, df in {"empty": full.iloc[0:0],
                         "no_tick0": full[full.Tick != 0],
                         "truncated": full[full.Tick < 4]}.items():
            p2 = os.path.join(td, f"{name}.parquet"); df.to_parquet(p2)
            rep = e1_base_bit_identity(p2, cfg)
            assert not rep.passed, (name, rep.summary())

def test_e1_bit_identity_rejects_all_q_columns():
    """V4: decomposition columns also forbidden under total-Q-disable."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=3,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p); df["Delta_from_rho"] = 0.0
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep = e1_base_bit_identity(p2, cfg)
        assert not rep.passed and rep.checks["schema_absent_Delta_from_rho"] == 1

def test_become_survive_no_base_draws_policy():
    """D2 (config-bound): deterministic_level consumes no base draws; the NEXT
    generator output after init coincides with a shadow's post-permutation draw."""
    gs = 6
    cfg = RunConfig(seed=11, rule_mode="become_survive", grid_scale=gs,
                    init=InitConfig(scheme="fixed_count", fixed_count=9,
                                    base_init_mode="deterministic_level"),
                    constants=DynamicsConstants(logit_l=-0.405465, kappa=0.2, p_survive=0.4))
    dyn = SeedRegistry(11).dynamics()
    state = initialize(cfg.init, gs, dyn)
    assert np.all(state.v == cfg.init.m) and state.v.dtype == np.float64
    shadow = np.random.default_rng(11)
    ref = shadow.permutation(gs * gs)
    expect = np.zeros(gs * gs, dtype=bool); expect[ref[:9]] = True
    assert np.array_equal(state.is_active.reshape(-1), expect)
    assert np.array_equal(dyn.generator.random(16), shadow.random(16))

def test_symmetric_chain_rejects_deterministic_level():
    with pytest.raises(Exception):
        RunConfig(seed=1, init=InitConfig(base_init_mode="deterministic_level"))

def test_become_survive_rejects_nonzero_q():
    """N3: silent ignoring foreclosed — construction raises."""
    cfg = RunConfig(seed=2, rule_mode="become_survive", grid_scale=6,
                    init=InitConfig(scheme="fixed_count", fixed_count=5,
                                    base_init_mode="deterministic_level"),
                    constants=DynamicsConstants(logit_l=-0.4, kappa=0.1, p_survive=0.4),
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    dyn = SeedRegistry(2).dynamics()
    with pytest.raises(ValueError):
        Dynamics(cfg, initialize(cfg.init, 6, dyn), dyn)

def test_dynamics_owns_private_copies():
    """D1(a): mutating the caller's GridState after construction changes nothing."""
    cfg = RunConfig(seed=3, f_dispatch="F_canonical", grid_scale=6, ticks=3,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    dyn = SeedRegistry(3).dynamics()
    state = initialize(cfg.init, 6, dyn)
    d = Dynamics(cfg, state, dyn)
    state.v[:] = 0.0                                      # hostile caller
    d.step()
    assert not np.any(d._v == 0.0)                        # terrain unaffected

def test_sink_cannot_alter_q_update():
    """D1(b): a hostile sink un-freezing and mutating Delta_v cannot change bases."""
    cfg = RunConfig(seed=4, f_dispatch="F_canonical", grid_scale=6, ticks=1,
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    def hostile(tick, fields):
        arr = fields["Delta_v"]
        arr.flags.writeable = True
        arr[:] = 99.0
    dyn = SeedRegistry(4).dynamics()
    d = Dynamics(cfg, initialize(cfg.init, 6, dyn), dyn)
    d.step(hostile)
    assert d._v.max() <= 1.0                              # clip would mask; check delta scale:
    dyn2 = SeedRegistry(4).dynamics()
    d2 = Dynamics(cfg, initialize(cfg.init, 6, dyn2), dyn2)
    d2.step()                                             # no sink
    assert np.array_equal(d._v, d2._v)                    # identical evolution
```

# DIGESTS
```
f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872  mfa_instrument/config.py
fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62  mfa_instrument/rng.py
43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18  mfa_instrument/init.py
d92ed9d13e409dee76f3bb497aae72e8bc425213cb54cb34de935756d7712cd6  mfa_instrument/dynamics.py
1ff66d62081fd4a7273f8f70906f9d09732e0c7ab853cd760d2ae28dddb83af9  mfa_instrument/telemetry.py
d18f273e25fa19ab3420a74f82595a5b8af9711c893834b57a7d69ceee7a34b4  mfa_instrument/verify.py
b2038025cdfd06f67e664c083924efa938d9f1f6b966ebcab694cd3b41999eae  mfa_instrument/gates/gate_a.py
33d57941cbcbb5b92995db5e3780850d95f990ba3fd40643674ea578120fedb7  tests/test_config_rng.py
bae7e9c4cde09720900f7c73fd9fd1759b8d604743e201e0a2e9bda406c5a92b  tests/test_init.py
6a3e70998ca47da23b278aeb80c56a372d5616cbbffdb0e912854c019811529c  tests/test_dynamics.py
875c565f645b36d9ebadd6082056d5bbff50ec7a318542fa4ead28206d9f1343  tests/test_telemetry_gate_a.py
db638474340171e0f7cc48947eceb9e78bbc16a2755fb4666fa1e5ac344991ed  tests/test_verify.py
```
*End of packet.*
