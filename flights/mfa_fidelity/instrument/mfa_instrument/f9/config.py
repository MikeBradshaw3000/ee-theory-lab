"""mfa_instrument/f9/config.py — Flight 9 module M1: the frozen declarations of Contract F9 v0.7
(§2, §3, §5.5, §9; freeze record §3) as immutable literals bound to a declaration digest.

Nothing here is a choice made at build. Every value is the frozen contract's or the freeze record's;
the section is cited beside it. The one object M1 adds is the DECLARATION DIGEST: the SHA-256 of the
repr of `F9_DECLARATION`, hardcoded below and recomputed at every preflight, so that a changed literal
cannot pass silently. One value is deliberately outside the digest: the floor hazard η₀ is a float
computed through libm. The digest carries its rule and its probability literal instead, and the
preflight checks that the float in use is the rule applied to that literal on the running machine.

NOT HERE, by the contract: masters and seed panels (drawn by stage, §8, DERIVED@BUILD; later modules),
stream keys (§2.5; the dynamics module), and every calibration-derived quantity (σ_seed, ℓ_c; step 4).

Units. Control values κ and occupancy thresholds are exact integers in micro-units (10^-6), the
convention of the frozen package root. Lengths are in lattice cells.
"""
from __future__ import annotations

import hashlib
import math
from typing import Dict, Tuple

from ..config import MICRO_UNITS

F9_VERSION = "f9_stage1_v1"                                                                    # freeze record §3.2 item 18
F9_CONTRACT_SHA256 = "60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168"        # FLIGHT_9_CONTRACT_v0_7.md (frozen)
F9_FREEZE_RECORD_SHA256 = "66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c"   # FLIGHT_9_FREEZE_RECORD.md

# ----------------------------------------------------------------------------- lattice and rule (contract §2)
F9_GRID = 100                                     # §2.1, RULED
F9_N_CELLS = F9_GRID * F9_GRID
F9_DT = 1                                         # §2.1
F9_MU = 0.2                                       # §2.7 deactivation rate (the Overview's lapse β; NOT the Overview's μ(ρ))
F9_FLOOR_PROBABILITY = 0.01                       # §2.6: the realization floor as a per-tick probability, RULED (carried from Contract F8)
F9_ETA0_RULE = "-ln(1 - floor_probability)"       # the rule and the probability enter the declaration digest; the float does not
F9_ETA0 = -math.log(1.0 - 0.01)                   # the floor hazard in use. Through libm, so possibly an ulp apart across platforms;
                                                  # `verify_frozen_identity` requires it to equal the rule applied to F9_FLOOR_PROBABILITY here
F9_TICKS = 3000                                   # §2.10; freeze record item 9
F9_TAIL_TICKS = 1000                              # §2.10; freeze record item 9
F9_N_SEEDS = 40                                   # §2.10, RULED 2026-11-13
F9_SURVIVAL_MIN = 36                              # §5.4; freeze record item 1
F9_FLICKER_WINDOWS = (1, 10, 100)                 # §2.11, RULED

# ----------------------------------------------------------------------------- levels (contract §2.9; freeze record item 8)
def generate_levels_micro() -> Tuple[int, ...]:
    """0.75; 1.00 to 2.00 in steps of 0.05; 2.25; 2.50; 3.00 — 25 values of κ in integer micro-units."""
    fine = tuple(range(1_000_000, 2_000_000 + 1, 50_000))
    return (750_000,) + fine + (2_250_000, 2_500_000, 3_000_000)


F9_LEVELS_MICRO: Tuple[int, ...] = (
    750000,
    1000000, 1050000, 1100000, 1150000, 1200000, 1250000, 1300000, 1350000, 1400000, 1450000, 1500000,
    1550000, 1600000, 1650000, 1700000, 1750000, 1800000, 1850000, 1900000, 1950000, 2000000,
    2250000, 2500000, 3000000,
)

# ----------------------------------------------------------------------------- terrains, compositions, arms (contract §3)
F9_TERRAINS: Tuple[str, ...] = ("T0", "TA", "TB", "TC", "TD-1-2", "TD-1-4", "TD-4-2", "TD-4-4")
F9_REQUIRED_TERRAINS: Tuple[str, ...] = ("TA", "TB", "TC", "TD-1-2", "TD-1-4", "TD-4-2", "TD-4-4")      # §3.3: seven required arms per composition
F9_COMPOSITIONS: Tuple[str, ...] = ("P", "H")     # §2.2: P = F_canonical = v·u·r; H = F_baseline = (v+u+r)/3 (rival only)
F9_ARMS: Tuple[Tuple[str, str], ...] = (("T0", "P"),) + tuple((t, c) for t in F9_REQUIRED_TERRAINS for c in F9_COMPOSITIONS)   # §8: 15 arms; T0 under P only

# TB (§3.1, §3.2): s = S0 + A·c(x); d = D0 + B·c(y); v = s + d; u = s − d; r = R0
F9_TB_PARAMS: Tuple[Tuple[str, float], ...] = (("s0", 0.55), ("a", 0.07), ("d0", 0.19), ("b", 0.19), ("r0", 0.3))
# TD (§3.2): core = union of n discs centred on cell corners; (centres in cells, radius in cells, tanh width w in cells)
_C1 = ((49.5, 49.5),)
_C4 = ((24.5, 24.5), (24.5, 74.5), (74.5, 24.5), (74.5, 74.5))
F9_TD_PARAMS: Tuple[Tuple[str, Tuple[Tuple[Tuple[float, float], ...], float, float]], ...] = (
    ("TD-1-2", (_C1, 25.3, 2.0)), ("TD-1-4", (_C1, 25.3, 4.0)), ("TD-4-2", (_C4, 12.65, 2.0)), ("TD-4-4", (_C4, 12.65, 4.0)),
)
F9_TD_CORE_CELLS = 2000                           # §3.2: |C| = 2,000 exactly in every variant
F9_TD_CORE_EDGE_CLEARANCE = 0.03                  # §3.2: no cell centre within 0.03 cells of the core's edge
F9_TB_X_SHARE_RANGE = (0.40, 0.60)                # §3.2 criterion, RULED

# Same-family terrains and the latent whose level sets both compositions use (§3.4 step 3; freeze record item 6)
F9_SAME_FAMILY_LATENT: Tuple[Tuple[str, str], ...] = (
    ("TA", "v"), ("TC", "u"), ("TD-1-2", "v"), ("TD-1-4", "v"), ("TD-4-2", "v"), ("TD-4-4", "v"),
)
F9_ROUND_PLACES = 12                              # §3.4 step 3; freeze record items 6 and 16
F9_CROSS_PLATFORM_TOL = 1e-12                     # §3.4 step 5 (per element, base arrays)
F9_SPR_RECOMPUTE_RTOL = 1e-9                      # §2.8 (relative, a recomputation elsewhere)

# ----------------------------------------------------------------------------- evaluator resolutions declared in §5.5 (used by `geometry`, `family`)
F9_THETA_MICRO = 200_000                          # §5.5 step 2; freeze record item 10 (scored)
F9_THETA_REPORTED_MICRO = (100_000, 300_000)      # §5.5 step 2; freeze record item 10 (reported)
F9_INFORMATIVE_MIN_CELLS = 100                    # §5.5 step 4; freeze record item 12
F9_INFORMATIVE_MIN_BONDS = 40                     # §5.5 step 4; freeze record item 12
F9_COMPONENT_MIN_BONDS = 40                       # §5.5 step 6, m; freeze record item 13
F9_EPSILON_MICRO = 2_000_000                      # §5.5 step 8, ε = 2.0 cells; freeze record item 14

# ----------------------------------------------------------------------------- spectral routine (§2.8: "the committed routine")
F9_SPR_TOL = 1e-14                                # stop: abs(ray - last) <= tol*max(1.0, abs(ray)); absolute on the declared arms (ray < 1)
F9_SPR_MAX_ITER = 200_000


class F9ConfigError(ValueError):
    """A frozen Flight 9 declaration failed its preflight, or a caller asked for an undeclared object."""


def q_deact(mu: float = F9_MU, dt: int = F9_DT) -> float:
    """Per-tick deactivation probability q = 1 − exp(−μ·Δt) (§2.4, §2.7)."""
    return 1.0 - math.exp(-mu * dt)


def level_id(level_micro: int) -> str:
    """The six-decimal label of a κ level, e.g. 1050000 → '1.050000'."""
    if isinstance(level_micro, bool) or not isinstance(level_micro, int) or level_micro not in F9_LEVELS_MICRO:
        raise F9ConfigError(f"not a declared level: {level_micro!r}")
    return f"{level_micro // MICRO_UNITS}.{level_micro % MICRO_UNITS:06d}"


def tb_params() -> Dict[str, float]:
    return dict(F9_TB_PARAMS)


def td_params(name: str):
    d = dict(F9_TD_PARAMS)
    if name not in d: raise F9ConfigError(f"not a TD variant: {name!r}")
    return d[name]


def same_family_latent(name: str):
    """'v' or 'u' for a same-family terrain; None for TB (each composition has its own array) and for T0."""
    return dict(F9_SAME_FAMILY_LATENT).get(name)


F9_DECLARATION = (
    ("version", F9_VERSION), ("contract_sha256", F9_CONTRACT_SHA256), ("freeze_record_sha256", F9_FREEZE_RECORD_SHA256),
    ("grid", F9_GRID), ("dt", F9_DT), ("mu", F9_MU), ("floor_probability", F9_FLOOR_PROBABILITY), ("eta0_rule", F9_ETA0_RULE), ("ticks", F9_TICKS), ("tail_ticks", F9_TAIL_TICKS),
    ("n_seeds", F9_N_SEEDS), ("survival_min", F9_SURVIVAL_MIN), ("flicker_windows", F9_FLICKER_WINDOWS),
    ("levels_micro", F9_LEVELS_MICRO), ("terrains", F9_TERRAINS), ("required_terrains", F9_REQUIRED_TERRAINS),
    ("compositions", F9_COMPOSITIONS), ("arms", F9_ARMS), ("tb_params", F9_TB_PARAMS), ("td_params", F9_TD_PARAMS),
    ("td_core_cells", F9_TD_CORE_CELLS), ("td_core_edge_clearance", F9_TD_CORE_EDGE_CLEARANCE), ("tb_x_share_range", F9_TB_X_SHARE_RANGE),
    ("same_family_latent", F9_SAME_FAMILY_LATENT), ("round_places", F9_ROUND_PLACES), ("cross_platform_tol", F9_CROSS_PLATFORM_TOL),
    ("spr_recompute_rtol", F9_SPR_RECOMPUTE_RTOL), ("theta_micro", F9_THETA_MICRO), ("theta_reported_micro", F9_THETA_REPORTED_MICRO),
    ("informative_min_cells", F9_INFORMATIVE_MIN_CELLS), ("informative_min_bonds", F9_INFORMATIVE_MIN_BONDS),
    ("component_min_bonds", F9_COMPONENT_MIN_BONDS), ("epsilon_micro", F9_EPSILON_MICRO),
    ("spr_tol", F9_SPR_TOL), ("spr_max_iter", F9_SPR_MAX_ITER),
)


def frozen_digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


F9_DECLARATION_SHA256_LITERAL = "7fbef2ff2a04e9bc0825e6bbfeb70ce867d15cc51ec22e7b4eac0a6c0ff8a3b3"


def verify_frozen_identity() -> Dict[str, str]:
    """Recompute every frozen literal from its rule and the declaration digest from its literal; raise on any difference."""
    if F9_LEVELS_MICRO != generate_levels_micro() or len(F9_LEVELS_MICRO) != 25 or len(set(F9_LEVELS_MICRO)) != 25:
        raise F9ConfigError("level literal differs from the rule of contract §2.9")
    if tuple(sorted(F9_LEVELS_MICRO)) != F9_LEVELS_MICRO:
        raise F9ConfigError("levels are not in increasing order")
    if len(F9_ARMS) != 15 or len(set(F9_ARMS)) != 15 or F9_ARMS[0] != ("T0", "P"):
        raise F9ConfigError("arm list is not the fifteen arms of contract §8")
    if set(dict(F9_TD_PARAMS)) != {t for t in F9_TERRAINS if t.startswith("TD")}:
        raise F9ConfigError("TD parameter table does not cover the four TD variants")
    if {t for t, _ in F9_SAME_FAMILY_LATENT} != set(F9_REQUIRED_TERRAINS) - {"TB"}:
        raise F9ConfigError("same-family table does not cover exactly the required terrains other than TB")
    if F9_ETA0_RULE != "-ln(1 - floor_probability)" or F9_ETA0 != -math.log(1.0 - F9_FLOOR_PROBABILITY):
        raise F9ConfigError("the floor hazard does not follow from its declared rule and probability (contract §2.6)")
    lit = F9_DECLARATION_SHA256_LITERAL
    if len(lit) != 64 or any(ch not in "0123456789abcdef" for ch in lit):
        raise F9ConfigError("F9 declaration digest literal is not a 64-hex sha256 (no sentinel or placeholder is accepted)")
    if frozen_digest(F9_DECLARATION) != lit:
        raise F9ConfigError("F9 declaration differs from its frozen literal digest")
    return {"version": F9_VERSION, "declaration_sha256": lit, "contract_sha256": F9_CONTRACT_SHA256, "freeze_record_sha256": F9_FREEZE_RECORD_SHA256}
