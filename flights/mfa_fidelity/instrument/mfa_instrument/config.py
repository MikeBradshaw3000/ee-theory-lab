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
