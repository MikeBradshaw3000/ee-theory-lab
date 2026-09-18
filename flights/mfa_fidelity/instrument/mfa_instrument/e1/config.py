"""mfa_instrument/e1/config.py — E1 stage-1 module M1: configuration, sweep identity, and the
total-Q-disable conformance preflight (Contract E1 §2, §3, v0.5 A, v0.8 C; design note §2 M1).

FROZEN OBJECTS (immutable literals bound to hardcoded digests, recomputed at every preflight):
  E1_LEVELS_MICRO  — the 24 pass-1 control values m in exact integer micro-units (six decimals),
                     endpoints 150000 and 850000, interior evenly spaced by exact rational
                     rounding; injective by construction and verified.
  E1_SEED_PANEL    — the 20 production seeds, drawn ONCE (2026-09-17) from a declared master seed
                     by a declared rule and hardcoded; reused at every level (paired by seed).
  E1_BASE_WIDTH_MICRO = 300000 (w = 0.3); grid 50; ticks 3000; bernoulli 0.5.

Nothing here runs the sweep. `e1_run_config` builds the immutable RunConfig for one (level, seed);
`run_level_run` executes exactly one run through the cleared instrument, writer, and verifier;
`conformance_preflight` proves the total-Q-disable configuration on a completed run's telemetry —
bases bit-identical to their initial values at every tick, no Q arithmetic path, no clip
movement, config recorded — by bit equality, never tolerance.
"""
from __future__ import annotations

import hashlib
import json
import os
import types
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pyarrow.parquet as pq

from ..config import DynamicsConstants, InitConfig, NoiseConfig, QConfig, RunConfig, MICRO_UNITS
from ..dynamics import Dynamics
from ..init import initialize
from ..rng import SeedRegistry
from ..telemetry import TelemetryWriter
from .. import verify as VERIFY

E1_VERSION = "e1_stage1_m1_v1 / Contract E1 v0.8 cumulative"

# ----------------------------------------------------------------------------- frozen sweep identity
E1_GRID = 50
E1_TICKS = 3000
E1_BASE_WIDTH_MICRO = 300_000                     # w = 0.3 exactly
E1_BERNOULLI_P = 0.5
E1_M_MIN_MICRO, E1_M_MAX_MICRO = 150_000, 850_000  # hard admissible endpoints (no clipping: m ± w/2 in [0,1])
E1_PASS1_LEVELS = 24


def _round_half_even(fr: Fraction) -> int:
    q, r = divmod(fr.numerator, fr.denominator)
    twice = 2 * r
    if twice < fr.denominator: return q
    if twice > fr.denominator: return q + 1
    return q if q % 2 == 0 else q + 1


def generate_pass1_levels_micro() -> Tuple[int, ...]:
    """Exact-rational generation: level_j = 150000 + round_half_even(j · 700000 / 23), j = 0..23."""
    span = Fraction(E1_M_MAX_MICRO - E1_M_MIN_MICRO)
    return tuple(E1_M_MIN_MICRO + _round_half_even(Fraction(j) * span / (E1_PASS1_LEVELS - 1)) for j in range(E1_PASS1_LEVELS))


# FROZEN LITERAL (established 2026-09-17 from the rule above; verified equal to the rule at every preflight)
E1_LEVELS_MICRO: Tuple[int, ...] = (
    150000, 180435, 210870, 241304, 271739, 302174, 332609, 363043, 393478, 423913, 454348, 484783,
    515217, 545652, 576087, 606522, 636957, 667391, 697826, 728261, 758696, 789130, 819565, 850000,
)
S_P1_NOM_MICRO = 30435                            # round6(0.70 / 23)  (E1 v0.8 §C)
S_P1_MAX_MICRO = max(b - a for a, b in zip(E1_LEVELS_MICRO, E1_LEVELS_MICRO[1:]))   # realized max spacing
DELTA_M_R_MICRO = 3382                            # round6(s_P1^nom / 9): the departure-zone width (v0.8 §C)

# FROZEN SEED PANEL — drawn once from master seed 20260917 by the rule below; hardcoded thereafter.
E1_SEED_PANEL_MASTER = 20260917
E1_SEED_PANEL: Tuple[int, ...] = (
    2117405799, 2804871216, 375183601, 701843324, 1075314870, 1719551416, 2685479494, 2666970591,
    632470092, 278031864, 2244203769, 3565777195, 1541399456, 2906227949, 4151989313, 2628184833,
    757868360, 872858888, 3907060348, 629405355,
)


def generate_seed_panel(master: int = E1_SEED_PANEL_MASTER, n: int = 20) -> Tuple[int, ...]:
    """The declared rule: SeedSequence(master) -> Generator -> n draws of uint32 without replacement."""
    g = np.random.default_rng(np.random.SeedSequence(master))
    out: List[int] = []
    while len(out) < n:
        s = int(g.integers(1, 2**32 - 1))
        if s not in out: out.append(s)
    return tuple(out)


def frozen_digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


E1_LEVELS_SHA256_LITERAL = "0366944a02a153d2d5ae3f3dfacd0e2f4d73d850c12b55523c95e6c757873477"   # established 2026-09-17
E1_SEED_PANEL_SHA256_LITERAL = "68309ed9f8be58088952675f2062afad2f59e3ebef10517ac43210b726a1c70d"   # established 2026-09-17

# THE E1 DECLARATION — one deeply immutable object (tuples only; no nested mutables), bound to an
# independent hardcoded digest literal, recomputed and compared inside every construction of an E1
# run configuration (L2 M1-1/M1-2). The committed A constants are part of it: E1 consumes the
# default DynamicsConstants, whose identity is frozen here field by field.
E1_CONSTANTS_EXPECTED: Tuple[Tuple[str, object], ...] = (
    ("alpha", 4.0), ("beta", 3.0), ("delta", 4.0), ("gamma_offset", 4.0), ("eta_floor", 0.01),
    ("w_v", 0.33), ("w_u", 0.33), ("w_r", 0.34), ("logit_l", None), ("kappa", None), ("p_survive", None),
)
E1_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("grid", E1_GRID), ("ticks", E1_TICKS), ("base_width_micro", E1_BASE_WIDTH_MICRO), ("bernoulli_p", E1_BERNOULLI_P),
    ("m_min_micro", E1_M_MIN_MICRO), ("m_max_micro", E1_M_MAX_MICRO), ("pass1_levels", E1_PASS1_LEVELS),
    ("levels_micro", E1_LEVELS_MICRO), ("seed_panel", E1_SEED_PANEL), ("s_p1_nom_micro", S_P1_NOM_MICRO),
    ("s_p1_max_micro", S_P1_MAX_MICRO), ("delta_m_r_micro", DELTA_M_R_MICRO),
    ("rule_mode", "symmetric_chain"), ("f_dispatch", "F_canonical"), ("q_read", "local"), ("gamma_psi", 0.0), ("gamma_rho", 0.0),
    ("noise_amplitude", 0.0), ("drive_schedule", ()), ("init_scheme", "bernoulli_p"), ("base_init_mode", "stochastic_ancestor"),
    ("constants", E1_CONSTANTS_EXPECTED),
)
E1_DECLARATION_SHA256_LITERAL = "76102dfbf514dc859f0045631dc1d3bcb0cfc376cca21ad3458ad20868e5dfa8"   # established 2026-09-17
E1_FROZEN = types.MappingProxyType(dict(E1_DECLARATION))      # read-only view for reporting; the tuple is the object


class E1ConfigError(ValueError):
    """A frozen E1 identity or admissibility rule is violated."""


def level_id(level_micro: int) -> str:
    """Canonical level identifier: the exact m value under the frozen '%.6f' format (v0.4 §4.2)."""
    return "%.6f" % (Fraction(level_micro, MICRO_UNITS))


def verify_frozen_identity() -> Dict[str, str]:
    """Recompute every frozen identity from its rule and compare to the literals. Fail-closed."""
    if generate_pass1_levels_micro() != E1_LEVELS_MICRO:
        raise E1ConfigError("frozen level list differs from its generating rule")
    if len(set(E1_LEVELS_MICRO)) != len(E1_LEVELS_MICRO) or list(E1_LEVELS_MICRO) != sorted(E1_LEVELS_MICRO):
        raise E1ConfigError("frozen level list is not injective and ascending")
    if len({level_id(m) for m in E1_LEVELS_MICRO}) != len(E1_LEVELS_MICRO):
        raise E1ConfigError("frozen level list is not injective under the '%.6f' identity format")
    if (E1_LEVELS_MICRO[0], E1_LEVELS_MICRO[-1]) != (E1_M_MIN_MICRO, E1_M_MAX_MICRO):
        raise E1ConfigError("frozen level list endpoints are not the hard admissible boundaries")
    for m in E1_LEVELS_MICRO:
        if m - E1_BASE_WIDTH_MICRO // 2 < 0 or m + E1_BASE_WIDTH_MICRO // 2 > MICRO_UNITS:
            raise E1ConfigError(f"level {m} would require clipping")
    if generate_seed_panel() != E1_SEED_PANEL or len(set(E1_SEED_PANEL)) != 20:
        raise E1ConfigError("frozen seed panel differs from its generating rule or is not 20 distinct seeds")
    d_levels, d_panel = frozen_digest(E1_LEVELS_MICRO), frozen_digest(E1_SEED_PANEL)
    if d_levels != E1_LEVELS_SHA256_LITERAL or d_panel != E1_SEED_PANEL_SHA256_LITERAL:
        raise E1ConfigError("frozen literal digest mismatch (levels or seed panel)")
    # the complete declaration: its literal digest, and EVERY field against the live execution global (L2 r2 M1-1)
    if frozen_digest(E1_DECLARATION) != E1_DECLARATION_SHA256_LITERAL:
        raise E1ConfigError("E1 declaration differs from its frozen literal digest")
    decl = dict(E1_DECLARATION)
    live = {"grid": E1_GRID, "ticks": E1_TICKS, "base_width_micro": E1_BASE_WIDTH_MICRO, "bernoulli_p": E1_BERNOULLI_P,
            "m_min_micro": E1_M_MIN_MICRO, "m_max_micro": E1_M_MAX_MICRO, "pass1_levels": E1_PASS1_LEVELS, "levels_micro": E1_LEVELS_MICRO,
            "seed_panel": E1_SEED_PANEL, "s_p1_nom_micro": S_P1_NOM_MICRO, "s_p1_max_micro": S_P1_MAX_MICRO, "delta_m_r_micro": DELTA_M_R_MICRO,
            "constants": E1_CONSTANTS_EXPECTED}
    for key, val in live.items():
        if decl[key] != val or type(decl[key]) is not type(val):
            raise E1ConfigError(f"E1 declaration field {key} differs from the live execution global")
    # HARD CONTRACT VALUES, stated independently of both the declaration and the globals (E1 v0.8 §C; v0.5 A)
    if (E1_M_MIN_MICRO, E1_M_MAX_MICRO, E1_PASS1_LEVELS, E1_SEED_PANEL_MASTER, len(E1_SEED_PANEL)) != (150000, 850000, 24, 20260917, 20):
        raise E1ConfigError("live sweep/seed globals differ from the hard contract values")
    # the DynamicsConstants FIELD SET must equal the declared set: an added behaviour-affecting default cannot stay undeclared
    if tuple(sorted(DynamicsConstants.__dataclass_fields__)) != tuple(sorted(n for n, _ in E1_CONSTANTS_EXPECTED)):
        raise E1ConfigError("DynamicsConstants field set differs from the declared constant set")
    if (decl["grid"], decl["ticks"], decl["base_width_micro"], decl["bernoulli_p"]) != (50, 3000, 300000, 0.5):
        raise E1ConfigError("E1 declaration shape/family values are not the contracted values")
    if (decl["rule_mode"], decl["f_dispatch"], decl["q_read"], decl["gamma_psi"], decl["gamma_rho"], decl["noise_amplitude"], decl["drive_schedule"],
            decl["init_scheme"], decl["base_init_mode"]) != ("symmetric_chain", "F_canonical", "local", 0.0, 0.0, 0.0, (), "bernoulli_p", "stochastic_ancestor"):
        raise E1ConfigError("E1 declaration configuration values are not the contracted values")
    k = DynamicsConstants()
    for name, val in decl["constants"]:
        if getattr(k, name) != val or type(getattr(k, name)) is not type(val):
            raise E1ConfigError(f"committed A constant {name} differs from the E1 declaration")
    if S_P1_NOM_MICRO != _round_half_even(Fraction(E1_M_MAX_MICRO - E1_M_MIN_MICRO, E1_PASS1_LEVELS - 1)):
        raise E1ConfigError("s_P1^nom differs from round6(0.70/23)")
    if DELTA_M_R_MICRO != _round_half_even(Fraction(S_P1_NOM_MICRO, 9)):
        raise E1ConfigError("Delta_m_R differs from round6(s_P1^nom / 9)")
    return {"levels_sha256": d_levels, "seed_panel_sha256": d_panel, "s_p1_max_micro": str(S_P1_MAX_MICRO)}


# ----------------------------------------------------------------------------- run configuration
def e1_run_config(level_micro: int, seed: int, *, grid: int = E1_GRID, ticks: int = E1_TICKS) -> RunConfig:
    """The immutable E1 RunConfig for one (level, seed). Grid/ticks are parameters ONLY so the
    preflight and controls can run at reduced size; production uses the frozen values."""
    verify_frozen_identity()                                  # mechanical, on every construction (L2 M1-1)
    if not isinstance(level_micro, int) or isinstance(level_micro, bool):
        raise E1ConfigError("level must be an exact integer micro-unit value")
    if level_micro - E1_BASE_WIDTH_MICRO // 2 < 0 or level_micro + E1_BASE_WIDTH_MICRO // 2 > MICRO_UNITS:
        raise E1ConfigError(f"level {level_micro} inadmissible: base interval would leave [0,1]")
    _exact_int(seed, "seed")
    if seed not in E1_SEED_PANEL and grid == E1_GRID and ticks == E1_TICKS:
        raise E1ConfigError("a production-shape run must use a seed from the frozen panel")
    return RunConfig(seed=int(seed), rule_mode="symmetric_chain", f_dispatch="F_canonical", grid_scale=grid, ticks=ticks,
                     q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0),
                     init=InitConfig(scheme="bernoulli_p", base_center_micro=int(level_micro), base_width_micro=E1_BASE_WIDTH_MICRO,
                                     bernoulli_p=E1_BERNOULLI_P, base_init_mode="stochastic_ancestor"),
                     noise=NoiseConfig(amplitude=0.0), drive_schedule=())


@dataclass
class LevelRun:
    level_micro: int
    level_id: str
    seed: int
    config_hash: str
    run_config_path: str
    telemetry_path: str
    rho_table_path: str
    verifier_passed: bool
    verifier_summary: str
    clipped_counts: Tuple[int, int, int]
    q_disabled: bool


def _exact_int(x, name: str) -> int:
    if isinstance(x, bool) or not isinstance(x, (int, np.integer)):
        raise E1ConfigError(f"{name} must be an exact non-Boolean integer, got {type(x).__name__}")
    return int(x)


def run_level_run(cfg: RunConfig, out_dir: str, stem: str) -> LevelRun:
    """Execute exactly one run: the governing declaration verified at ENTRY (L2 r2 M1-2 — the supplied
    configuration itself is not required to conform here; conformance judges that afterwards);
    frozen config written BEFORE execution; the cleared dynamics, writer (rho_global persisted — the
    Gate-R dual condition), and verifier. Returns the record; adjudicates nothing."""
    verify_frozen_identity()
    _exact_int(cfg.seed, "seed"); _exact_int(cfg.init.base_center_micro, "level")
    os.makedirs(out_dir, exist_ok=True)
    rc_path = os.path.join(out_dir, f"{stem}.run_config.json")
    chash = cfg.write_frozen(rc_path)
    reg = SeedRegistry(cfg.seed)
    dyn = reg.dynamics()                                   # ONE ancestor-faithful stream: init draws, then dynamics
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    model = Dynamics(cfg, state, dyn, emit_rho_global=True)
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho, cfg.noise.amplitude != 0.0, rule_mode=cfg.rule_mode)
    path = os.path.join(out_dir, f"{stem}.parquet")
    tw.open(path)
    for _ in range(cfg.ticks):
        model.step(tw.sink)
    tw.close()
    vrep = VERIFY.tier1_verify(path, cfg, rho_global_path=tw.rho_global_path, expect_rho_global=True)
    return LevelRun(cfg.init.base_center_micro, level_id(cfg.init.base_center_micro), cfg.seed, chash, rc_path, path,
                    tw.rho_global_path, bool(vrep.passed), vrep.summary(),
                    (int(model.clipped_v_count), int(model.clipped_u_count), int(model.clipped_r_count)), bool(model._q_disabled))


# ----------------------------------------------------------------------------- conformance preflight
@dataclass
class ConformanceReport:
    passed: bool
    checks: Dict[str, bool] = field(default_factory=dict)
    detail: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        return "E1 CONFORMANCE " + ("PASS" if self.passed else "FAIL") + " " + " ".join(f"{k}={'ok' if v else 'FAIL'}" for k, v in self.checks.items())


def expected_e1_config(level_micro: int, seed: int, grid: int, ticks: int) -> RunConfig:
    """The contracted E1 RunConfig for the run's declared identity (shape parameters as given)."""
    return e1_run_config(level_micro, seed, grid=grid, ticks=ticks)


def initial_active_count(cfg: RunConfig) -> int:
    """Tick-0 reconstruction (L2 r3 M1-6): replay INITIALIZATION ONLY from the frozen config/seed on the
    ancestor-faithful stream, stopping before any dynamics draw, and count the initial active cells."""
    reg = SeedRegistry(cfg.seed)
    state = initialize(cfg.init, cfg.grid_scale, reg.dynamics())
    return int(np.count_nonzero(state.is_active))


def _rho_table_matches_rows(run: LevelRun, cfg: RunConfig) -> Tuple[bool, Dict[str, Any]]:
    """ONE complete obligation on the persisted production rho object (L2 r3 M1-6): exact columns
    ["Tick", "rho_global"]; integer Tick dtype and float64 rho dtype; no nulls or nonfinite values;
    exactly cfg.ticks rows in exact tick order 0..ticks−1; rho[0] == initial active count / N
    reconstructed independently by replaying initialization only; rho[t] == count(is_active rows at
    t−1)/N bit-exact for every t ≥ 1."""
    try:
        import pandas as pd
        tbl = pd.read_parquet(run.rho_table_path); n = cfg.n_cells; d: Dict[str, Any] = {}
        d["columns_exact"] = list(tbl.columns) == ["Tick", "rho_global"]
        d["tick_dtype_integer"] = bool(np.issubdtype(tbl["Tick"].dtype, np.integer)) if d["columns_exact"] else False
        d["rho_dtype_float64"] = bool(tbl["rho_global"].dtype == np.float64) if d["columns_exact"] else False
        if not (d["columns_exact"] and d["tick_dtype_integer"] and d["rho_dtype_float64"]):
            return False, d
        ticks = tbl["Tick"].to_numpy(); rho = tbl["rho_global"].to_numpy()
        d["no_null_or_nonfinite"] = bool(not tbl["rho_global"].isna().any() and np.isfinite(rho).all())
        d["row_count_exact"] = len(tbl) == cfg.ticks
        d["tick_order_exact"] = bool(np.array_equal(ticks, np.arange(cfg.ticks)))
        if not (d["no_null_or_nonfinite"] and d["row_count_exact"] and d["tick_order_exact"]):
            return False, d
        k0 = initial_active_count(cfg)
        d["tick0_matches_initialization_replay"] = bool(rho[0] == float(np.float64(k0) / np.float64(n))); d["initial_active_count"] = k0
        pf = pq.ParquetFile(run.telemetry_path); counts: Dict[int, int] = {}
        for rg in range(pf.num_row_groups):
            df = pf.read_row_group(rg, columns=["Tick", "is_active"]).to_pandas()
            for tick, s in df.groupby("Tick")["is_active"].sum().items():
                counts[int(tick)] = counts.get(int(tick), 0) + int(s)
        bad = [t for t in range(1, cfg.ticks) if t - 1 not in counts or rho[t] != float(np.float64(counts[t - 1]) / np.float64(n))]
        d["mismatched_ticks"] = bad[:10]; d["ticks_ge1_match_row_states"] = not bad
        return bool(d["tick0_matches_initialization_replay"] and not bad), d
    except Exception as e:                # noqa: BLE001 — any read failure is a conformance failure, named
        return False, {"error": f"{type(e).__name__}: {e}"}


def conformance_preflight(run: LevelRun, cfg: RunConfig) -> ConformanceReport:
    """Total-Q-disable AND full-configuration conformance (Contract E1 §2; L2 M1-3/M1-4). Families,
    each named separately: declaration identity; rule/F; Q/read; drive/noise; initialization;
    constants; shape/seed policy; config record identity; the CLEARED e1_base_bit_identity verifier
    (mechanically invoked, its full check map retained); clip counters; Tier-1 verifier. A PASS means
    "the contracted E1 configuration was executed and its telemetry proves it", not less."""
    checks: Dict[str, bool] = {}; detail: Dict[str, Any] = {}
    # declaration identity (mechanical) — a tampered declaration cannot pass conformance
    try:
        detail["declaration"] = verify_frozen_identity(); checks["declaration_identity"] = True
    except E1ConfigError as e:
        checks["declaration_identity"] = False; detail["declaration_error"] = str(e)
    # the consumed configuration against the contracted one, family by family
    exp = None
    try:
        exp = expected_e1_config(cfg.init.base_center_micro, cfg.seed, cfg.grid_scale, cfg.ticks)
    except E1ConfigError as e:
        detail["expected_config_error"] = str(e)
    def fam(name: str, ok: bool) -> None: checks[name] = bool(ok)
    fam("rule_and_f", exp is not None and cfg.rule_mode == exp.rule_mode == "symmetric_chain" and cfg.f_dispatch == exp.f_dispatch == "F_canonical")
    fam("q_and_read", exp is not None and cfg.q == exp.q and cfg.q.q_read == "local" and cfg.q.gamma_psi == 0.0 and cfg.q.gamma_rho == 0.0
        and isinstance(cfg.q.gamma_psi, float) and isinstance(cfg.q.gamma_rho, float))
    fam("drive_and_noise", exp is not None and cfg.drive_schedule == () and cfg.noise == exp.noise and cfg.noise.amplitude == 0.0)
    fam("initialization", exp is not None and cfg.init == exp.init and cfg.init.scheme == "bernoulli_p" and cfg.init.bernoulli_p == 0.5
        and cfg.init.base_width_micro == E1_BASE_WIDTH_MICRO and cfg.init.base_init_mode == "stochastic_ancestor")
    fam("constants", exp is not None and cfg.constants == exp.constants == DynamicsConstants()
        and all(getattr(cfg.constants, n) == v for n, v in E1_CONSTANTS_EXPECTED))
    fam("shape_and_seed_policy", exp is not None and cfg.grid_scale == exp.grid_scale and cfg.ticks == exp.ticks
        and (cfg.seed in E1_SEED_PANEL or (cfg.grid_scale, cfg.ticks) != (E1_GRID, E1_TICKS)))
    fam("canonical_config_equal", exp is not None and cfg.canonical_json() == exp.canonical_json())
    fam("q_disabled_branch_selected", bool(run.q_disabled))
    # LevelRun identity bound to the consumed configuration (L2 r2 M1-3)
    fam("levelrun_identity_bound", run.level_micro == cfg.init.base_center_micro and run.level_id == level_id(cfg.init.base_center_micro)
        and run.seed == cfg.seed and type(run.seed) is int and os.path.isfile(run.rho_table_path or "") and os.path.isfile(run.telemetry_path))
    # config record identity
    on_disk = open(run.run_config_path, "rb").read()
    fam("run_config_recorded_lf_utf8", b"\r\n" not in on_disk)
    fam("run_config_hash_matches_executed", hashlib.sha256(on_disk).hexdigest() == run.config_hash == cfg.config_hash())
    rec = json.loads(on_disk.decode("utf-8"))
    fam("run_config_q_disabled_recorded", rec["q"]["gamma_psi"] == 0.0 and rec["q"]["gamma_rho"] == 0.0)
    # THE CLEARED E1 VERIFIER: tick-0 anchored raw-bit base identity, key coverage, full Q-column absence
    e1v = VERIFY.e1_base_bit_identity(run.telemetry_path, cfg)
    detail["e1_base_bit_identity"] = {"checks": dict(e1v.checks), "rows_seen": e1v.rows_seen, "summary": e1v.summary()}
    fam("e1_base_bit_identity_verifier", bool(e1v.passed))
    fam("clip_counters_zero", run.clipped_counts == (0, 0, 0))
    # rho TABLE VALUES against the row file (finding of record, round 3): the cleared Tier-1 verifier does
    # not value-check the tick table under a Q-disabled configuration (it consumes rho only through
    # Delta_from_rho under a global read). M2 reads production rho(t) from this table, so its values
    # are verified HERE: pre-update rho(t) == count(is_active rows at tick t−1)/N, bit-exact, every tick ≥ 1.
    checks["rho_table_values_match_row_states"], detail["rho_table_value_check"] = _rho_table_matches_rows(run, cfg)
    # Tier-1 RERUN on the artifacts currently named by the LevelRun — never the stored Boolean (L2 r2 M1-3)
    t1 = VERIFY.tier1_verify(run.telemetry_path, cfg, rho_global_path=run.rho_table_path, expect_rho_global=True)
    fam("tier1_verifier_rerun_passed", bool(t1.passed))
    detail["tier1_rerun"] = {"checks": dict(t1.checks), "rows_seen": t1.rows_seen, "summary": t1.summary()}
    detail["tier1_at_execution"] = run.verifier_summary
    return ConformanceReport(all(checks.values()), checks, detail)
