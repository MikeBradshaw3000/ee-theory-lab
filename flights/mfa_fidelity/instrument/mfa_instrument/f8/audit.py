"""mfa_instrument/f8/audit.py — Flight 8 module M6: the morphology audit (Contract F8 v0.8.4 §5.1–§5.4, §6.1–§6.4, §4.3
price; F8 Interpretation 002 `198d2991dd12168c…`; M6 generator declaration v0.3; E1 M6's framework `ce5ebecd7feb11f4…` carried; L2 build review r1 D1–D4 repaired: target legality
certified over the whole reachable surface, tests independent of the placement sentinel, hi − lo == w, reentrant onset on §6.4's range).

THE GENERATOR (declaration §3; Interpretation 002). Three regime sources, each an ACTIVE-COUNT PROCESS K[0..3000] on N = 2,500
cells (M1's record convention; M2 scores rho = K/N on the exact count grid):
  NULL       K0 ~ Bin(N, π₁); K_{t+1} = Bin(K_t, 1−q) + Bin(N−K_t, a), a = 1−e^(−η₀Δt): the §2.9 chain as an aggregate process —
             E at zero feedback, the law M3 certified its thresholds against.
  SUSTAINED  reading E: K0 ~ Bin(N, π₁); K_{t+1} = Bin(K_t, 1−q) + Bin(N−K_t, a_t(K_t)), a_t(k) = 1−e^(−(η₀ + c(m,t)·k/N)Δt);
             unmodulated c = gλ̄ = m·q/Δt (the §3.1 map's conditional expectation, bit-equal to M5 `finite_n_counts` on a shared
             stream); modulated c = c_tar(m,t) from a declared TARGET DENSITY schedule converted target → activation probability
             a_tar = q·r/(1−r) → hazard H = −ln(1−a_tar)/Δt → coefficient c_tar = (H−η₀)/r (L2 §5.2). Legal domain
             R_FLOOR ≤ r_tar < 1/(1+q) at EVERY reachable key ≥ lo (pass-2 insertions included), certified at parameter preflight
             from the frozen surface — refused (redrawn) never clipped. A target is a target: no reset, no claim it is the mean.
  DIP        the unmodulated E process with a NONTERMINAL zero window w ∈ [0, 8] and a terminal per-tick floor
             k_floor = ⌊idx_T/100⌋ + 1 = 142, so S_min = 0 ≤ θ_P and S_term ≥ 14,200/250,000 > θ_T BY SUPPORT (UNRESOLVED with
             certainty; contract §6.4). E1's terminal-window dip is NOT carried (under F8's single terminal window it would be
             NO_SUSTAINED).
No path is ever redrawn or discarded on account of its classification; preflight is on parameters only (Interpretation 002 pt 4).

STREAMS (declaration §5): regime uniforms SeedSequence([master, class, sweep, 0]) — 20, shared across every level of the sweep
(§5.1); parameters SeedSequence([master, class, sweep, 2, attempt]) in the one frozen draw order; runs
SeedSequence([master, class, sweep, 1, level_micro, seed_index]) — keyed by the level's exact micro-unit identity so an inserted
level's runs are the same stream whatever the routing order. Per run: K0, then U_t, V_t per tick, then (DIP) the window selector.

THE REACHABLE-LEVEL THRESHOLD ADAPTER (declaration §6; Interpretation 002 pt 6): M3's law is level-independent and M3 refuses
off-grid levels; the adapter binds every key of the router's reachable surface (24 pass-1 + the insertions `route()` can
produce over M4's canonical witnesses, post-fallback) to the ONE certified M3 payload. Role `production` only from the full
surface rebuilt from `route()` and the thresholds rebuilt from M3; validation is by REPLAY; a missing key at scoring time is an
APPARATUS HALT (the sweep HALTED, the class incomplete), never an on-demand derivation. Nothing in M1/M3 is modified.

SCORING AND QUALIFICATION (E1 M6 carried; contract §5.1, §5.4): per sweep 24 levels × 20 runs → M2 statuses → 16/2/4 labels →
M4 evaluate (descriptive) and route → pass-2 insertions scored the same way → final level set → M4 evaluate = THE VERDICT OF
RECORD. Applicable error: scientific-intent classes count final NOT_DISTINGUISHED; ND-intent classes count final LOCATED or
NOT_PRODUCED. Class complete_pass = attempted == scored == 500, zero halts of either kind, CP-95 upper ≤ 0.10; ensemble_pass =
every class complete on a production adapter; qualification = design AND held-out joined mechanically. Exact intended
verdict-and-cause agreement is DESCRIPTIVE ONLY. M-P1's criteria are not imported.

MASTERS (declaration §9): DERIVED@BUILD after the complete generator is placed — 6/7/8 followed by the placement date
(YYYYMMDD); `PLACEMENT_DATE` is None until that commit, and no production audit or price runs while it is None.

THE §4.3 PRICE (declaration §7): P_null(S_min > θ_P) over complete ten-window NULL runs under the pricing master, with the
exact one-sided CP-95 upper bound — descriptive, never a pass condition; separate from the later job-0 comparison (§8).
"""
from __future__ import annotations

import hashlib
import json
import math
import types
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..config import MICRO_UNITS
from . import classify as K
from . import closure as CL
from . import config as C
from . import null as N
from . import verdict as V
from .classify import COUNTS, N_CELLS, N_WINDOWS, RECORD_LEN, TAIL_START, WINDOW, level_counts, level_label, run_status
from .config import F8_LEVELS_MICRO, S_P1_MICRO, level_id

AUDIT_VERSION = "f8_stage1_m6_v1 / Contract F8 v0.8.4 §5.1-§5.4, §6, §4.3 / F8 Interpretation 002"
N_SEEDS = COUNTS["n_runs"]                                  # 20
TICKS = C.F8_TICKS                                          # 3000
ETA0, MU, DT, G = C.F8_ETA0, C.F8_MU, float(C.F8_DT), C.F8_G
_A_NULL, Q_DEACT, PI1 = N.chain_rates()                     # exactly as the stepper evaluates them (M3)
R_UPPER = 1.0 / (1.0 + Q_DEACT)                             # finite-hazard bound: a_tar < 1  ⇔  r < 1/(1+q)
M_MIN, M_MAX = C.F8_M_MIN_MICRO, C.F8_M_MAX_MICRO


class AuditDomainError(ValueError):
    """Frozen identity violated, input outside the audit's domain, or an apparatus defect."""


class GeneratorHalt(RuntimeError):
    """Preflight exhausted the frozen redraw budget: an apparatus failure, never a classifier error."""


def _digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _exact_int(x, name, lo=None):
    if isinstance(x, bool) or not isinstance(x, int):
        raise AuditDomainError(f"{name} must be an exact non-Boolean integer")
    if lo is not None and x < lo:
        raise AuditDomainError(f"{name} must be >= {lo}")
    return x


def _exact_float(x, name, lo=None, hi=None):
    if isinstance(x, bool) or not isinstance(x, float) or not math.isfinite(x):
        raise AuditDomainError(f"{name} must be a finite float")
    if (lo is not None and x < lo) or (hi is not None and x > hi):
        raise AuditDomainError(f"{name} out of range")
    return x


def _is_hex64(s) -> bool:
    return isinstance(s, str) and len(s) == 64 and all(c in "0123456789abcdef" for c in s)


# ----------------------------------------------------------------------------- audit declaration
SWEEPS_PER_CLASS = 500                                      # ratified: freeze record §3 item 23
CAP = 0.10                                                  # idem
CP_CONFIDENCE = 0.95                                        # idem (one-sided upper)
MAX_REDRAWS = 64                                            # [PROPOSED] declaration M6-6 (E1's budget)
PRICING_REPLICATES = 10_000                                 # [PROPOSED] declaration M6-9
COMPARISON_REPLICATES = 200                                 # [PROPOSED] declaration M6-10
PLACEMENT_DATE: Optional[int] = None                        # YYYYMMDD of the commit placing the complete generator (declaration §9)
MASTER_PREFIXES = (6, 7, 8)                                 # design, held-out, pricing
DECLARED_MASTERS = (C.F8_SEED_PANEL_MASTER, C.F8_CALIBRATION_MASTER, N.VALIDATION_REPLICATE_MASTER,
                    N.VALIDATION_PROTOCOL_ATTEMPT_2.replicate_master, CL.PROJECTION_MASTER, 520261028)
E1_RETIRED_MASTERS = (202609221, 202609222, 202609223)

INTENDED_MAP: Tuple[Tuple[str, str, Optional[str]], ...] = V.ARCHETYPE_TABLE      # the exact known-answer mapping (M4, frozen)
CLASSES = tuple(n for n, _, _ in INTENDED_MAP)
SCIENTIFIC_CLASSES = tuple(n for n, v, _ in INTENDED_MAP if v in ("LOCATED", "NOT_PRODUCED"))
ND_CLASSES = tuple(n for n, v, _ in INTENDED_MAP if v == "NOT_DISTINGUISHED")
INTENDED = types.MappingProxyType({n: (v, c) for n, v, c in INTENDED_MAP})

AUDIT_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("version", AUDIT_VERSION), ("scoring_object", "m3_level_independent_payload_via_reachable_adapter"),
    ("sweeps_per_class", SWEEPS_PER_CLASS), ("cap", CAP), ("cp_confidence", CP_CONFIDENCE), ("cp_side", "one-sided upper"),
    ("n_seeds", N_SEEDS), ("max_redraws", MAX_REDRAWS), ("pricing_replicates", PRICING_REPLICATES), ("comparison_replicates", COMPARISON_REPLICATES),
    ("master_rule", "design 6YYYYMMDD, held_out 7YYYYMMDD, pricing 8YYYYMMDD; YYYYMMDD = placement date of the complete generator"),
    ("classes", CLASSES), ("scientific_classes", SCIENTIFIC_CLASSES), ("nd_classes", ND_CLASSES),
    ("applicable_error", "scientific-intent classes: final NOT_DISTINGUISHED; ND-intent classes: final LOCATED or NOT_PRODUCED"),
    ("claim_boundary", "a pass establishes distinguished-as-scientific-vs-ND at the bound on this synthetic ensemble; exact archetype recognition is descriptive only; nothing is established about spatial lattice runs"),
    ("completion", "attempted == scored == 500 and halted == 0 and generator_halted == 0 and cap clears; ensemble_pass requires every class complete on a production adapter"),
    ("qualification", "design AND held-out records mechanically joined; ensemble_pass alone is never a freeze pass"),
    ("pairing", "common per-seed regime-assignment uniforms across levels (§5.1); trajectories never shared"),
    ("price", "P_null(S_min > theta_P) over complete ten-window NULL runs; exact CP upper; descriptive, never a pass condition"),
)
AUDIT_DECLARATION_SHA256_LITERAL = "58693fafa1717b01aecac0dc0c568528faff44c402f6f2d2b0fc8a0d2636d89a"   # established 2026-10-30 (unchanged in round 2)

# ----------------------------------------------------------------------------- generator declaration (complete, frozen)
R_FLOOR = CL.rho_re(CL.level_m(M_MIN))                      # [PROPOSED] M6-4: ρ*(m_min; η₀) = 0.066903…, the lowest unmodulated target
DRIFT_RANGE = (-0.10, 0.10)                                 # [PROPOSED] M6-5
DRIFT_MIN_ABS = 0.02
OSC_AMP_RANGE = (0.05, 0.25)
OSC_PERIOD_RANGE = (50, 400)
ATT_RANGE = (0.5, 0.9)
ATT_SCALE_RANGE = (0.2, 0.4)                                # in m
MIXTURE_PI_RANGE = (0.45, 0.55)                             # ratified: freeze record §3 item 14
W_A, W_L, W_U = 108_400, 228_842, 627_232                   # Appendix A (DERIVED@FREEZE)
GENTLE_WIDTH = (W_A, 205_958)                               # [w_A, 0.9·w_L] (Appendix A's declared range)
ABRUPT_WIDTH = (0, W_A)
WIDE_WIDTH = (689_956, 1_003_571)                           # [1.1·w_U, ⌊1.6·w_U⌋]  (M6-12)
TWO_CROSSING_OFFSETS = (4 * S_P1_MICRO, 7 * S_P1_MICRO)     # (391,304, 684,782) — the pair (4s, 7s)  (M6-7)
REENTRANT_RETURN_SPACINGS = (4.0, 6.0)                      # U[4, 6]·s, round-half-even to micro
EXTRA_INDEX_RANGE = (0, 3)                                  # inclusive pass-1 indices for the off-band classes
DIP_WINDOWS = (0, N_WINDOWS - 2)                            # NONTERMINAL: w ∈ {0, …, 8}
CLASS_WIDTH = types.MappingProxyType({"gentle_onset": "gentle", "off_band_mixture": "gentle", "wide_mixed_boundary": "wide",
                                      "unresolved_heavy_boundary": "wide", "abrupt_onset": "abrupt", "persistent_nonstationary_high_m": "abrupt",
                                      "nonmonotone_amplitude": "abrupt", "off_band_unresolved": "abrupt",
                                      "two_resolved_crossings": "zero", "reentrant": "zero", "no_sustained_anywhere": "none", "no_null_consistent_anywhere": "none"})
RAMP_CLASSES = ("gentle_onset", "abrupt_onset", "persistent_nonstationary_high_m", "nonmonotone_amplitude", "off_band_mixture",
                "off_band_unresolved", "wide_mixed_boundary", "unresolved_heavy_boundary")
TEMPORAL_MODES = ("constant", "drift", "oscillation")
PARAM_DRAW_ORDER = ("onset", "width", "temporal_selector", "drift", "amp", "period", "att", "att_scale", "pi", "return_offset", "extra_index")
RNG_HIERARCHY = ("regime uniforms SeedSequence([master, class, sweep, 0]) -> 20 uniforms shared across levels; "
                 "params SeedSequence([master, class, sweep, 2, attempt]) in PARAM_DRAW_ORDER; "
                 "runs SeedSequence([master, class, sweep, 1, level_micro, seed_index]): K0, then (U_t, V_t) per tick, then DIP window selector")

GENERATOR_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("sources", ("NULL", "SUSTAINED", "DIP")), ("sustained_source", "reading E: finite-N current-density closure (Interpretation 002)"),
    ("null_source", "E at zero feedback: independent two-state chains as an aggregate count process, stationary start"),
    ("count_process", "K0~Bin(N,pi1); K'=Bin(K,1-q)+Bin(N-K,1-exp(-(eta0+c*K/N)*dt)); c=m*q/dt unmodulated"),
    ("modulation", "target r_tar -> a_tar=q r/(1-r) -> H=-ln(1-a_tar)/dt -> c_tar=(H-eta0)/r; domain R_FLOOR<=r<1/(1+q); refused never clipped"),
    ("r_floor_rule", "rho_re(m_min)"), ("drift_range", DRIFT_RANGE), ("drift_min_abs", DRIFT_MIN_ABS), ("osc_amp_range", OSC_AMP_RANGE),
    ("osc_period_range", OSC_PERIOD_RANGE), ("att_range", ATT_RANGE), ("att_scale_range", ATT_SCALE_RANGE), ("mixture_pi_range", MIXTURE_PI_RANGE),
    ("schedules", "drift: rho*(m)(1+D(t/T-1/2)); oscillation: rho*(m)(1+A sin(2 pi t/P)); attenuation: max(r_floor, pi1+kappa(m)(rho*(m)-pi1)), kappa=1-A_att max(0,(m-onset)/M_sc)"),
    ("gentle_width", GENTLE_WIDTH), ("abrupt_width", ABRUPT_WIDTH), ("wide_width", WIDE_WIDTH),
    ("onset_range_ramp", (M_MIN + S_P1_MICRO, M_MAX - S_P1_MICRO)), ("onset_range_two_crossing", (M_MIN + S_P1_MICRO, M_MAX - 8 * S_P1_MICRO)),
    ("onset_range_reentrant", (M_MIN + S_P1_MICRO, M_MAX - 8 * S_P1_MICRO)),
    ("width_endpoints", "lo = onset - w//2, hi = lo + w (hi - lo == w for every integer w; for odd w the band midpoint is onset + 1/2 micro-unit)"),
    ("temporal_legality_domain", "every reachable key (24 pass-1 levels + the 338 reachable insertions) >= lo, before any trajectory"),
    ("two_crossing_offsets", TWO_CROSSING_OFFSETS), ("reentrant_return_spacings", REENTRANT_RETURN_SPACINGS), ("extra_index_range", EXTRA_INDEX_RANGE),
    ("dip_windows", DIP_WINDOWS), ("dip_terminal_floor_rule", "k_floor = idx_T // WINDOW + 1 per tick in the terminal window"),
    ("class_width", tuple(sorted(CLASS_WIDTH.items()))), ("temporal_modes", TEMPORAL_MODES), ("param_draw_order", PARAM_DRAW_ORDER),
    ("rng_hierarchy", RNG_HIERARCHY), ("max_redraws", MAX_REDRAWS), ("record_len", RECORD_LEN), ("n_cells", N_CELLS),
    ("intended_map", INTENDED_MAP),
)
GENERATOR_DECLARATION_SHA256_LITERAL = "dd0ff5ec51ff921b5316ffef103ecaa3783d71cba278458613c46767e7db5f57"   # established 2026-10-30, round 2 (D1, D3, D4)


def masters_for_date(date_yyyymmdd: int) -> Tuple[int, int, int]:
    d = _exact_int(date_yyyymmdd, "placement date", 20261030)
    if d > 20991231 or not (1 <= (d // 100) % 100 <= 12) or not (1 <= d % 100 <= 31):
        raise AuditDomainError("placement date must be a YYYYMMDD calendar date")
    return tuple(p * 10 ** 8 + d for p in MASTER_PREFIXES)


def production_masters() -> Tuple[int, int, int]:
    if PLACEMENT_DATE is None:
        raise AuditDomainError("masters are not yet established: PLACEMENT_DATE is None (set in the commit placing the complete generator)")
    ms = masters_for_date(PLACEMENT_DATE)
    if len(set(ms)) != 3 or set(ms) & set(DECLARED_MASTERS) or set(ms) & set(E1_RETIRED_MASTERS):
        raise AuditDomainError("masters collide with a declared or retired master")
    return ms


def verify_frozen_identity() -> None:
    C.verify_frozen_identity(); K.verify_frozen_identity(); N.verify_frozen_identity(); V.verify_frozen_identity(); CL.verify_frozen_identity()
    if "PENDING" not in AUDIT_DECLARATION_SHA256_LITERAL and _digest(AUDIT_DECLARATION) != AUDIT_DECLARATION_SHA256_LITERAL:
        raise AuditDomainError("audit declaration differs from its frozen literal digest")
    if "PENDING" not in GENERATOR_DECLARATION_SHA256_LITERAL and _digest(GENERATOR_DECLARATION) != GENERATOR_DECLARATION_SHA256_LITERAL:
        raise AuditDomainError("generator declaration differs from its frozen literal digest")
    d = dict(AUDIT_DECLARATION); g = dict(GENERATOR_DECLARATION)
    if len(d) != len(AUDIT_DECLARATION) or len(g) != len(GENERATOR_DECLARATION):
        raise AuditDomainError("duplicate declaration field")
    live_a = {"version": AUDIT_VERSION, "sweeps_per_class": SWEEPS_PER_CLASS, "cap": CAP, "cp_confidence": CP_CONFIDENCE, "n_seeds": N_SEEDS,
              "max_redraws": MAX_REDRAWS, "pricing_replicates": PRICING_REPLICATES, "comparison_replicates": COMPARISON_REPLICATES,
              "classes": CLASSES, "scientific_classes": SCIENTIFIC_CLASSES, "nd_classes": ND_CLASSES}
    live_g = {"drift_range": DRIFT_RANGE, "drift_min_abs": DRIFT_MIN_ABS, "osc_amp_range": OSC_AMP_RANGE, "osc_period_range": OSC_PERIOD_RANGE,
              "att_range": ATT_RANGE, "att_scale_range": ATT_SCALE_RANGE, "mixture_pi_range": MIXTURE_PI_RANGE, "gentle_width": GENTLE_WIDTH,
              "abrupt_width": ABRUPT_WIDTH, "wide_width": WIDE_WIDTH, "two_crossing_offsets": TWO_CROSSING_OFFSETS,
              "reentrant_return_spacings": REENTRANT_RETURN_SPACINGS, "extra_index_range": EXTRA_INDEX_RANGE, "dip_windows": DIP_WINDOWS,
              "class_width": tuple(sorted(CLASS_WIDTH.items())), "temporal_modes": TEMPORAL_MODES, "param_draw_order": PARAM_DRAW_ORDER,
              "rng_hierarchy": RNG_HIERARCHY, "max_redraws": MAX_REDRAWS, "record_len": RECORD_LEN, "n_cells": N_CELLS, "intended_map": INTENDED_MAP}
    for src, live in ((d, live_a), (g, live_g)):
        for k_, v_ in live.items():
            if src[k_] != v_ or type(src[k_]) is not type(v_):
                raise AuditDomainError(f"declaration field {k_} differs from the live global")
    if (SWEEPS_PER_CLASS, CAP, CP_CONFIDENCE, N_SEEDS, MAX_REDRAWS) != (500, 0.10, 0.95, 20, 64):
        raise AuditDomainError("audit hard values differ from the contract / declaration")
    if INTENDED_MAP != V.ARCHETYPE_TABLE or _digest(INTENDED_MAP) != V.ARCHETYPE_TABLE_SHA256_LITERAL:
        raise AuditDomainError("intended map differs from M4's frozen archetype table")
    if set(SCIENTIFIC_CLASSES) | set(ND_CLASSES) != set(CLASSES) or set(SCIENTIFIC_CLASSES) & set(ND_CLASSES) or set(CLASS_WIDTH) != set(CLASSES):
        raise AuditDomainError("class partition / width map inconsistent with the intended map")
    if (_A_NULL, Q_DEACT, PI1) != N.chain_rates() or R_UPPER != 1.0 / (1.0 + Q_DEACT):
        raise AuditDomainError("chain rates differ from M3's")
    if R_FLOOR != CL.rho_re(CL.level_m(M_MIN)) or not (PI1 < R_FLOOR < R_UPPER):
        raise AuditDomainError("modulation floor differs from rho_re(m_min) or lies outside the legal domain")
    if GENTLE_WIDTH != (W_A, 205958) or WIDE_WIDTH != (689956, 1003571) or ABRUPT_WIDTH != (0, W_A) or (W_A, W_L, W_U) != (108400, 228842, 627232):
        raise AuditDomainError("archetype widths differ from Appendix A's declared ranges")
    if TWO_CROSSING_OFFSETS != (391304, 684782) or DIP_WINDOWS != (0, 8) or S_P1_MICRO != 97826:
        raise AuditDomainError("offsets, DIP windows or spacing differ from the declaration")
    if PLACEMENT_DATE is not None:
        production_masters()


# ----------------------------------------------------------------------------- Clopper–Pearson (E1 M6, carried verbatim)
def _betacf(x: float, a: float, b: float) -> Tuple[float, bool]:
    MAXIT, EPS, FPMIN = 300, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = FPMIN if abs(d) < FPMIN else d; d = 1.0 / d; h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d; d = FPMIN if abs(d) < FPMIN else d; c = 1.0 + aa / c; c = FPMIN if abs(c) < FPMIN else c; d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d; d = FPMIN if abs(d) < FPMIN else d; c = 1.0 + aa / c; c = FPMIN if abs(c) < FPMIN else c; d = 1.0 / d
        de = d * c; h *= de
        if abs(de - 1.0) < EPS:
            return h, True
    return h, False


def _beta_cdf(x: float, a: float, b: float) -> float:
    if x <= 0.0: return 0.0
    if x >= 1.0: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        h, ok = _betacf(x, a, b); val = front * h / a
    else:
        h, ok = _betacf(1.0 - x, b, a); val = 1.0 - front * h / b
    if not ok or not math.isfinite(val):
        raise AuditDomainError("regularized incomplete beta did not converge or is nonfinite")
    return val


def _beta_ppf(q: float, a: float, b: float) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _beta_cdf(mid, a, b) < q: lo = mid
        else: hi = mid
    out = 0.5 * (lo + hi)
    if not math.isfinite(out): raise AuditDomainError("beta quantile nonfinite")
    return out


def clopper_pearson_upper(k, n, confidence=CP_CONFIDENCE) -> float:
    k = _exact_int(k, "k"); n = _exact_int(n, "n", 1); _exact_float(confidence, "confidence")
    if not (0.0 < confidence < 1.0): raise AuditDomainError("confidence must lie in (0, 1)")
    if not 0 <= k <= n: raise AuditDomainError("Clopper-Pearson requires 0 <= k <= n")
    if k == n: return 1.0
    return _beta_ppf(confidence, float(k + 1), float(n - k))


# ----------------------------------------------------------------------------- the reachable-level threshold adapter
ADAPTER_ROLES = ("production", "slice")


def reachable_pass2_levels() -> Tuple[int, ...]:
    """The insertion levels `route()` can produce, POST-FALLBACK, over M4's canonical band witnesses (every pass-1 index pair);
    insertions depend only on the band endpoints and the fixed pass-1 set, so this surface is complete for every sweep."""
    V.verify_frozen_identity()
    n = len(F8_LEVELS_MICRO); levels: set = set()
    for i in range(n):
        for j in range(i + 1, n):
            lab = ["U"] * n
            for k_ in range(0, i + 1): lab[k_] = "N"
            for k_ in range(j, n): lab[k_] = "S"
            levels |= {int(x) for x in V.route(tuple(lab), F8_LEVELS_MICRO).insertions_micro}
    levels -= set(F8_LEVELS_MICRO)
    return tuple(sorted(levels))


def reachable_surface_identity() -> str:
    return _digest(("m4", V.VERDICT_DECLARATION_SHA256_LITERAL, reachable_pass2_levels()))


@dataclass(frozen=True)
class ThresholdAdapter:
    role: str
    keys: Tuple[int, ...]                       # 24 pass-1 levels + the reachable insertions, ascending
    n_pass1: int
    n_pass2: int
    theta_p: float
    theta_t: float
    index_p: int                                # M3 window-count indices (platform-independent integers)
    index_t: int
    payload_identity: str                       # M3 NullThresholds payload identity as measured on this machine
    surface_sha256: str
    m3_declaration_sha256: str
    m4_declaration_sha256: str
    declaration_sha256: str
    body_sha256: str = ""

    def body(self) -> Dict[str, object]:
        d = asdict(self); d.pop("body_sha256", None); d["keys"] = list(self.keys); return d

    def identity(self) -> str:
        return hashlib.sha256(_canon(self.body()).encode()).hexdigest()

    def get(self, level_micro) -> Tuple[float, float]:
        m = _exact_int(level_micro, "level_micro")
        if m not in self._keyset():
            raise AuditDomainError(f"adapter has no key for level {m}: apparatus defect, the sweep halts")
        return self.theta_p, self.theta_t

    def _keyset(self):
        return set(self.keys)


def build_adapter(role: str = "production", keys: Optional[Sequence[int]] = None) -> ThresholdAdapter:
    """Role `production` only from the full surface and the full M3 payload; `slice` for tests (any subset of the surface)."""
    verify_frozen_identity()
    if role not in ADAPTER_ROLES: raise AuditDomainError("unknown adapter role")
    full = tuple(F8_LEVELS_MICRO) + reachable_pass2_levels()
    if role == "production":
        if keys is not None: raise AuditDomainError("a production adapter is built from the full surface, never from a key list")
        kk = tuple(sorted(full))
    else:
        kk = tuple(sorted(int(x) for x in (keys if keys is not None else F8_LEVELS_MICRO)))
        if len(set(kk)) != len(kk) or any(x not in full for x in kk): raise AuditDomainError("slice keys must be distinct members of the reachable surface")
    th = N.null_thresholds(F8_LEVELS_MICRO[0])
    a = ThresholdAdapter(role, kk, sum(1 for x in kk if x in F8_LEVELS_MICRO), sum(1 for x in kk if x not in F8_LEVELS_MICRO),
                         th.theta_p, th.theta_t, th.theta_p_certificate.index, th.theta_t_certificate.index, th.payload_identity(),
                         reachable_surface_identity(), N.NULL_SHA256_LITERAL, V.VERDICT_DECLARATION_SHA256_LITERAL, GENERATOR_DECLARATION_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(a, body_sha256=a.identity())


def validate_adapter(a: ThresholdAdapter) -> None:
    """Validation by REPLAY: the surface from route(), the thresholds from M3, the identity from the content."""
    if type(a) is not ThresholdAdapter: raise AuditDomainError("not a ThresholdAdapter")
    if a.role not in ADAPTER_ROLES or a.body_sha256 != a.identity(): raise AuditDomainError("adapter role or identity invalid")
    rebuilt = build_adapter(a.role, None if a.role == "production" else a.keys)
    if rebuilt != a: raise AuditDomainError("adapter does not replay to its recorded content")


def is_production_adapter(a) -> bool:
    try:
        if type(a) is not ThresholdAdapter or a.role != "production": return False
        validate_adapter(a)
        return a.n_pass1 == len(F8_LEVELS_MICRO) and a.n_pass2 == len(reachable_pass2_levels()) and (a.index_p, a.index_t) == (14341, 14121)
    except AuditDomainError:
        return False


def adapter_to_json(a: ThresholdAdapter) -> str:
    return _canon({"__type__": "F8ThresholdAdapter", "sha256": a.body_sha256, "body": a.body()})


def adapter_from_json(text: str) -> ThresholdAdapter:
    doc = json.loads(text, parse_constant=lambda c: (_ for _ in ()).throw(AuditDomainError(f"nonfinite constant {c}")))
    if doc.get("__type__") != "F8ThresholdAdapter": raise AuditDomainError("not an F8ThresholdAdapter document")
    b = doc["body"]
    a = ThresholdAdapter(b["role"], tuple(int(x) for x in b["keys"]), int(b["n_pass1"]), int(b["n_pass2"]), float(b["theta_p"]), float(b["theta_t"]),
                         int(b["index_p"]), int(b["index_t"]), b["payload_identity"], b["surface_sha256"], b["m3_declaration_sha256"],
                         b["m4_declaration_sha256"], b["declaration_sha256"], doc["sha256"])
    validate_adapter(a)
    return a


# ----------------------------------------------------------------------------- the count processes
def _count_process(coef, g: np.random.Generator, n: int = N_CELLS, ticks: int = TICKS) -> np.ndarray:
    """K[0..ticks]: K0 ~ Bin(n, π₁); K_{t+1} = Bin(K_t, 1−q) + Bin(n−K_t, 1−exp(−(η₀ + c_t·K_t/n)·Δt)). `coef` is a float (constant c)
    or a float64 array of length `ticks` (c_t for the advance into tick t+1, index t). Draw order per tick: survivors, then births.
    The unmodulated arithmetic is M5 `finite_n_counts`'s, expression for expression."""
    const = not isinstance(coef, np.ndarray)
    if not const and (coef.dtype != np.float64 or coef.shape != (ticks,)): raise AuditDomainError("coefficient series must be float64 of length ticks")
    q = Q_DEACT
    k = int(g.binomial(n, PI1)); out = np.empty(ticks + 1, dtype=np.int64); out[0] = k
    for t in range(1, ticks + 1):
        rho = k / n
        c = coef if const else float(coef[t - 1])
        p_act = 1.0 - math.exp(-(ETA0 + c * rho) * DT)
        survive = int(g.binomial(k, 1.0 - q)); born = int(g.binomial(n - k, p_act))
        k = survive + born; out[t] = k
    return out


def gen_null_run(g: np.random.Generator) -> np.ndarray:
    return _count_process(0.0, g)


def gen_sustained_run(m: float, coef: Optional[np.ndarray], g: np.random.Generator) -> np.ndarray:
    """Unmodulated (coef None): c = gλ̄ = m·q/Δt — M5 `lambda_bar`. Modulated: the declared c_tar series."""
    return _count_process(CL.lambda_bar(m) if coef is None else coef, g)


K_FLOOR_RULE = "idx_T // WINDOW + 1"


def dip_terminal_floor(adapter_index_t: int) -> int:
    return _exact_int(adapter_index_t, "index_t", 0) // WINDOW + 1


def gen_dip_run(m: float, g: np.random.Generator, index_t: int) -> np.ndarray:
    """The unmodulated E process; then (from the same stream) a NONTERMINAL window w ∈ [0, 8] is zeroed and the terminal window is
    floored at k_floor per tick. S_min = 0 ≤ θ_P and S_term ≥ (k_floor·WINDOW)/(WINDOW·N) > θ_T by support."""
    out = _count_process(CL.lambda_bar(m), g)
    w = int(g.integers(DIP_WINDOWS[0], DIP_WINDOWS[1] + 1))
    out[TAIL_START + w * WINDOW:TAIL_START + (w + 1) * WINDOW] = 0
    kf = dip_terminal_floor(index_t)
    term = slice(TAIL_START + (N_WINDOWS - 1) * WINDOW, TAIL_START + N_WINDOWS * WINDOW)
    out[term] = np.maximum(out[term], kf)
    return out


def rho_record(counts: np.ndarray) -> np.ndarray:
    if counts.shape != (RECORD_LEN,) or counts.dtype != np.int64 or (counts < 0).any() or (counts > N_CELLS).any():
        raise AuditDomainError("count record must be int64 of RECORD_LEN in [0, N_CELLS]")
    return counts.astype(np.float64) / np.float64(N_CELLS)


# ----------------------------------------------------------------------------- modulation: target -> probability -> hazard -> coefficient
def target_to_coefficient(r_tar: np.ndarray) -> np.ndarray:
    """a_tar = q·r/(1−r); H = −ln(1−a_tar)/Δt; c_tar = (H − η₀)/r. Domain R_FLOOR ≤ r < 1/(1+q) enforced: a violation is REFUSED."""
    r = np.asarray(r_tar, dtype=np.float64)
    if r.ndim != 1 or not np.isfinite(r).all(): raise AuditDomainError("target series must be finite float64")
    if (r < R_FLOOR).any() or (r >= R_UPPER).any():
        raise AuditDomainError(f"target density outside the legal domain [{R_FLOOR:.6f}, {R_UPPER:.6f})")
    a_tar = Q_DEACT * r / (1.0 - r)
    H = -np.log(1.0 - a_tar) / DT
    return (H - ETA0) / r


@dataclass(frozen=True)
class SweepParams:
    archetype: str
    onset_micro: int
    width_micro: int
    temporal: str
    drift: float
    amp: float
    period: int
    att: float
    att_scale: float
    pi: float
    return_offset_micro: int
    extra_index: int

    @property
    def lo(self) -> int: return self.onset_micro - self.width_micro // 2
    @property
    def hi(self) -> int: return self.lo + self.width_micro            # hi - lo == width_micro for every integer width (L2 M6 r1 D3)


def _draw_once(archetype: str, g: np.random.Generator) -> SweepParams:
    """One parameter draw in PARAM_DRAW_ORDER; every field is drawn for every class so a class's parameter identity never
    depends on which fields it reads."""
    kind = CLASS_WIDTH[archetype]
    if archetype in ("two_resolved_crossings", "reentrant"): onset_rng = (M_MIN + S_P1_MICRO, M_MAX - 8 * S_P1_MICRO)      # contract §6.4, one shared row
    else: onset_rng = (M_MIN + S_P1_MICRO, M_MAX - S_P1_MICRO)
    onset = int(g.integers(onset_rng[0], onset_rng[1] + 1))
    wr = {"gentle": GENTLE_WIDTH, "abrupt": ABRUPT_WIDTH, "wide": WIDE_WIDTH, "zero": (0, 0), "none": (0, 0)}[kind]
    width = int(g.integers(wr[0], wr[1] + 1))
    sel = float(g.random())
    temporal = ("drift" if sel < 0.5 else "oscillation") if archetype == "persistent_nonstationary_high_m" else "constant"
    drift = float(g.uniform(*DRIFT_RANGE)); amp = float(g.uniform(*OSC_AMP_RANGE)); period = int(g.integers(OSC_PERIOD_RANGE[0], OSC_PERIOD_RANGE[1] + 1))
    att = float(g.uniform(*ATT_RANGE)); att_scale = float(g.uniform(*ATT_SCALE_RANGE))
    pi = float(g.uniform(*MIXTURE_PI_RANGE))
    ret = int(round(float(g.uniform(*REENTRANT_RETURN_SPACINGS)) * S_P1_MICRO))      # U[4,6]·s, round-half-even (Python round) to integer micro
    extra = int(g.integers(EXTRA_INDEX_RANGE[0], EXTRA_INDEX_RANGE[1] + 1))
    return SweepParams(archetype, onset, width, temporal, drift, amp, period, att, att_scale, pi, ret, extra)


# ---- schedules
def target_schedule(prm: SweepParams, m: float) -> Optional[np.ndarray]:
    """The declared target-density series r_tar(m, t), t = 0..T−1 (the coefficient for the advance into tick t+1), or None for the
    constant (unmodulated) case. The domain check lives in `target_to_coefficient`."""
    rs = CL.rho_re(m)
    t = np.arange(TICKS, dtype=np.float64)
    if prm.archetype == "persistent_nonstationary_high_m":
        if prm.temporal == "drift": return rs * (1.0 + prm.drift * (t / TICKS - 0.5))
        if prm.temporal == "oscillation": return rs * (1.0 + prm.amp * np.sin(2.0 * np.pi * t / prm.period))
        raise AuditDomainError("persistent_nonstationary_high_m must be drift or oscillation")
    if prm.archetype == "nonmonotone_amplitude":
        kappa = 1.0 - prm.att * max(0.0, (m - prm.onset_micro / MICRO_UNITS) / prm.att_scale)
        return np.full(TICKS, max(R_FLOOR, PI1 + kappa * (rs - PI1)))
    return None


def coefficient_series(prm: SweepParams, m: float) -> Optional[np.ndarray]:
    sch = target_schedule(prm, m)
    return None if sch is None else target_to_coefficient(sch)


# ---- preflight
_RHO_RE: Dict[int, float] = {}
_SURFACE: Tuple[int, ...] = ()


def reachable_surface_keys() -> Tuple[int, ...]:
    """The 24 pass-1 levels plus the 338 reachable insertions (memoised): the domain on which a parameter candidate's targets
    must be legal, since any of these keys may be SUSTAINED-assigned in a sweep (L2 M6 r1 D1)."""
    global _SURFACE
    if not _SURFACE: _SURFACE = tuple(sorted(set(F8_LEVELS_MICRO) | set(reachable_pass2_levels())))
    return _SURFACE


def _rho_re_at(u: int) -> float:
    if u not in _RHO_RE: _RHO_RE[u] = CL.rho_re(CL.level_m(u))
    return _RHO_RE[u]


def _schedule_extremes(prm: SweepParams, u: int) -> Tuple[float, float]:
    """A closed-form ENVELOPE (lower, upper) of the target schedule at level key u, from the schedule's declared shape and without
    building the series: drift — the two end values (exact extremes of a linear ramp); oscillation — rs·(1 ∓ A), which contains the
    discrete series' extremes (equality only when some t hits a quarter period), so the legality check is conservative; attenuation —
    the constant. `test` asserts envelope ≤ series.min and series.max ≤ envelope for every schedule."""
    rs = _rho_re_at(u); m = CL.level_m(u)
    if prm.archetype == "persistent_nonstationary_high_m":
        if prm.temporal == "drift":
            ends = (rs * (1.0 - 0.5 * prm.drift), rs * (1.0 + prm.drift * ((TICKS - 1) / TICKS - 0.5)))
            return min(ends), max(ends)
        if prm.temporal == "oscillation":
            return rs * (1.0 - prm.amp), rs * (1.0 + prm.amp)
    if prm.archetype == "nonmonotone_amplitude":
        kappa = 1.0 - prm.att * max(0.0, (m - prm.onset_micro / MICRO_UNITS) / prm.att_scale)
        v = max(R_FLOOR, PI1 + kappa * (rs - PI1)); return v, v
    return rs, rs

def archetype_preflight(prm: SweepParams) -> Tuple[bool, str]:
    """Placement (E1's geometric checks on the F8 grid) AND morphology/legality (declaration §4.4; L2 §5.5): the named feature is
    actually instantiated and every target in the schedule's domain is legal. Never looks at a trajectory."""
    L = F8_LEVELS_MICRO; a = prm.archetype; lo, hi = prm.lo, prm.hi
    n_below = sum(1 for u in L if u < lo); n_above = sum(1 for u in L if u >= hi)
    if a in RAMP_CLASSES and (n_below < 1 or n_above < 1):
        return False, "onset window leaves no confident level on one side"
    if a == "two_resolved_crossings":
        b, c = prm.onset_micro + TWO_CROSSING_OFFSETS[0], prm.onset_micro + TWO_CROSSING_OFFSETS[1]
        regions = (lambda u: u < prm.onset_micro, lambda u: prm.onset_micro <= u < b, lambda u: b <= u < c, lambda u: u >= c)
        if not all(any(f(u) for u in L) for f in regions): return False, "N-S-N-S requires a level in each of the four regions"
    if a == "reentrant":
        r = prm.onset_micro + prm.return_offset_micro
        if not (any(u < prm.onset_micro for u in L) and any(prm.onset_micro <= u < r for u in L) and any(u >= r for u in L)):
            return False, "N-S-N requires a level below the onset, inside the sustained region and at or above the return"
    if a == "off_band_mixture" and not L[prm.extra_index] < lo: return False, "extra level is not below the band"
    if a == "off_band_unresolved":
        extras = L[prm.extra_index:prm.extra_index + 3]
        if len(extras) != 3 or not max(extras) < lo: return False, "the three extra levels are not all below the band"
    # legality of the targets over the SUSTAINED-eligible REACHABLE domain (every reachable key >= lo, pass-2 insertions included)
    if a in ("persistent_nonstationary_high_m", "nonmonotone_amplitude"):
        if a == "persistent_nonstationary_high_m":
            if prm.temporal == "drift" and abs(prm.drift) < DRIFT_MIN_ABS: return False, "drift below the declared minimum: feature absent"
            if prm.temporal == "oscillation" and not (OSC_PERIOD_RANGE[0] <= prm.period <= OSC_PERIOD_RANGE[1]): return False, "period outside range"
        for u in reachable_surface_keys():
            if u < lo: continue
            smin, smax = _schedule_extremes(prm, u)
            if smin < R_FLOOR or smax >= R_UPPER: return False, f"target leaves the legal domain at reachable key {u} (m={CL.level_m(u):.6f})"
    if a == "nonmonotone_amplitude":
        above = [CL.level_m(u) for u in L if u >= hi]
        if len(above) < 2: return False, "fewer than two levels above the onset: no profile to attenuate"
        prof = [float(target_schedule(prm, m)[0]) for m in above]
        if not prof[1] < prof[0]: return False, "resulting amplitude does not decrease from the first to the second level above the onset"
        if any(b > a_ for a_, b in zip(prof, prof[1:])): return False, "resulting amplitude is not non-increasing above the onset"
    return True, "ok"


def draw_params(archetype: str, master: int, class_index: int, sweep_index: int) -> Tuple[SweepParams, int]:
    """Deterministic redraw from SeedSequence([master, class, sweep, 2, attempt]) until preflight passes, up to MAX_REDRAWS;
    exhaustion raises GeneratorHalt. Returns (params, attempts)."""
    if archetype not in CLASSES: raise AuditDomainError(f"unknown archetype {archetype!r}")
    for attempt in range(MAX_REDRAWS):
        g = np.random.default_rng(np.random.SeedSequence([int(master), int(class_index), int(sweep_index), 2, attempt]))
        prm = _draw_once(archetype, g)
        ok, _ = archetype_preflight(prm)
        if ok: return prm, attempt + 1
    raise GeneratorHalt(f"{archetype}: preflight failed {MAX_REDRAWS} times for sweep {sweep_index}")


def regime_at(archetype: str, m_micro: int, prm: SweepParams, seed_u: float) -> str:
    L = F8_LEVELS_MICRO; lo, hi = prm.lo, prm.hi
    frac = 0.0 if m_micro < lo else (1.0 if (m_micro >= hi or hi == lo) else (m_micro - lo) / (hi - lo))
    ramp = "SUSTAINED" if seed_u < frac else "NULL"
    if archetype in ("gentle_onset", "abrupt_onset", "persistent_nonstationary_high_m", "nonmonotone_amplitude", "wide_mixed_boundary"): return ramp
    if archetype == "no_sustained_anywhere": return "NULL"
    if archetype == "no_null_consistent_anywhere": return "SUSTAINED"
    if archetype == "two_resolved_crossings":
        b, c = prm.onset_micro + TWO_CROSSING_OFFSETS[0], prm.onset_micro + TWO_CROSSING_OFFSETS[1]
        return "SUSTAINED" if (prm.onset_micro <= m_micro < b) or m_micro >= c else "NULL"
    if archetype == "reentrant":
        return "SUSTAINED" if prm.onset_micro <= m_micro < prm.onset_micro + prm.return_offset_micro else "NULL"
    if archetype == "off_band_mixture":
        return ("SUSTAINED" if seed_u < prm.pi else "NULL") if m_micro == L[prm.extra_index] else ramp
    if archetype == "off_band_unresolved":
        return "DIP" if m_micro in L[prm.extra_index:prm.extra_index + 3] else ramp
    if archetype == "unresolved_heavy_boundary":
        return "DIP" if lo <= m_micro < hi else ("SUSTAINED" if m_micro >= hi else "NULL")
    raise AuditDomainError(f"unknown archetype {archetype!r}")


# ----------------------------------------------------------------------------- one sweep
def run_stream(master: int, class_index: int, sweep_index: int, level_micro: int, seed_index: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([int(master), int(class_index), int(sweep_index), 1, int(level_micro), int(seed_index)]))


def regime_uniforms(master: int, class_index: int, sweep_index: int) -> np.ndarray:
    return np.random.default_rng(np.random.SeedSequence([int(master), int(class_index), int(sweep_index), 0])).random(N_SEEDS)


def generate_run(archetype: str, prm: SweepParams, m_micro: int, seed_index: int, seed_u: float, adapter: ThresholdAdapter,
                 master: int, class_index: int, sweep_index: int) -> Tuple[str, np.ndarray]:
    """(regime, counts) for one (level, seed) from its own stream. The adapter is consulted first: a missing key halts before a draw."""
    adapter.get(m_micro)
    regime = regime_at(archetype, m_micro, prm, seed_u)
    g = run_stream(master, class_index, sweep_index, m_micro, seed_index)
    m = CL.level_m(m_micro)
    if regime == "NULL": return regime, gen_null_run(g)
    if regime == "SUSTAINED": return regime, gen_sustained_run(m, coefficient_series(prm, m), g)
    return regime, gen_dip_run(m, g, adapter.index_t)


def _label_at(archetype: str, m_micro: int, prm: SweepParams, us: np.ndarray, adapter: ThresholdAdapter, master: int, ci: int, si: int) -> str:
    tp, tt = adapter.get(m_micro)
    statuses = []
    for j in range(N_SEEDS):
        _, counts = generate_run(archetype, prm, m_micro, j, float(us[j]), adapter, master, ci, si)
        statuses.append(run_status(rho_record(counts), tp, tt)[0])
    return level_label(level_counts(statuses))


@dataclass(frozen=True)
class SweepResult:
    archetype: str
    sweep_index: int
    master: int
    params: SweepParams
    preflight_attempts: int
    pass1_labels: Tuple[str, ...]
    pass1_verdict: str
    pass1_cause: Optional[str]
    router_row: str
    nominal_insertions: int
    realized_insertions: int
    insertions_micro: Tuple[int, ...]
    fallback_moves: Tuple[Tuple[int, int], ...]
    fallback_drops: Tuple[int, ...]
    final_levels_micro: Tuple[int, ...]
    final_labels: Tuple[str, ...]
    final_verdict: str
    final_cause: Optional[str]
    final_rule: str
    adapter_role: str
    adapter_sha256: str
    declaration_sha256: str
    generator_sha256: str
    evaluability_halt: Optional[str] = None
    generator_halt: Optional[str] = None


def run_sweep(archetype: str, sweep_index: int, master: int, adapter: ThresholdAdapter) -> SweepResult:
    verify_frozen_identity()
    if type(adapter) is not ThresholdAdapter: raise AuditDomainError("adapter must be a ThresholdAdapter")
    if archetype not in CLASSES: raise AuditDomainError(f"unknown archetype {archetype!r}")
    ci = CLASSES.index(archetype); _exact_int(sweep_index, "sweep_index", 0); _exact_int(master, "master", 1)
    ident = dict(adapter_role=adapter.role, adapter_sha256=adapter.body_sha256, declaration_sha256=AUDIT_DECLARATION_SHA256_LITERAL, generator_sha256=GENERATOR_DECLARATION_SHA256_LITERAL)
    empty_router = dict(router_row="", nominal_insertions=0, realized_insertions=0, insertions_micro=(), fallback_moves=(), fallback_drops=())
    try:
        prm, attempts = draw_params(archetype, master, ci, sweep_index)
    except GeneratorHalt as e:
        empty = SweepParams(archetype, 0, 0, "constant", 0.0, 0.0, 1, 0.0, 1.0, 0.0, 0, 0)
        return SweepResult(archetype, sweep_index, master, empty, MAX_REDRAWS, (), "", None, **empty_router, final_levels_micro=(), final_labels=(),
                           final_verdict="GENERATOR_HALT", final_cause=None, final_rule="", **ident, generator_halt=str(e))
    ok, why = archetype_preflight(prm)
    if not ok: raise AuditDomainError(f"preflight re-assertion failed after draw: {why}")
    us = regime_uniforms(master, ci, sweep_index)
    lab1: Tuple[str, ...] = (); v1 = None; router = dict(empty_router)
    try:
        lab1 = tuple(_label_at(archetype, u, prm, us, adapter, master, ci, sweep_index) for u in F8_LEVELS_MICRO)
        v1 = V.evaluate(lab1, F8_LEVELS_MICRO); d = V.route(lab1, F8_LEVELS_MICRO)
        nominal = V.P2R_SINGLE_BAND_INSERTIONS if d.row in ("P2R-5", "P2R-6") else (2 * V.P2R_PER_INTERVAL_INSERTIONS if d.row == "P2R-4" else 0)
        router = dict(router_row=d.row, nominal_insertions=nominal, realized_insertions=len(d.insertions_micro), insertions_micro=tuple(int(x) for x in d.insertions_micro),
                      fallback_moves=tuple(d.fallback_moves), fallback_drops=tuple(d.fallback_drops))
        if d.insertions_micro:
            lab2 = tuple(_label_at(archetype, int(u), prm, us, adapter, master, ci, sweep_index) for u in d.insertions_micro)
            merged = sorted(list(zip(F8_LEVELS_MICRO, lab1)) + list(zip((int(x) for x in d.insertions_micro), lab2)))
            levels_f = tuple(u for u, _ in merged); lab_f = tuple(l for _, l in merged)
        else:
            levels_f, lab_f = tuple(F8_LEVELS_MICRO), lab1
        vf = V.evaluate(lab_f, levels_f)
    except AuditDomainError as e:
        return SweepResult(archetype, sweep_index, master, prm, attempts, lab1, v1.verdict if v1 else "", v1.cause if v1 else None, **router,
                           final_levels_micro=(), final_labels=(), final_verdict="HALTED", final_cause=None, final_rule="", **ident, evaluability_halt=f"apparatus:{e}")
    return SweepResult(archetype, sweep_index, master, prm, attempts, lab1, v1.verdict, v1.cause, **router, final_levels_micro=levels_f, final_labels=lab_f,
                       final_verdict=vf.verdict, final_cause=vf.cause, final_rule=vf.rule, **ident)


# ----------------------------------------------------------------------------- scoring, completion, qualification (E1 M6 carried)
@dataclass(frozen=True)
class ClassScore:
    archetype: str
    intended_verdict: str
    intended_cause: Optional[str]
    attempted: int
    scored: int
    halted: int
    generator_halted: int
    applicable_error: str
    errors: int
    cp_upper_95: float
    statistical_cap_pass: bool
    complete_pass: bool
    exact_agreement_descriptive: float
    exact_agreement_count: int
    verdict_counts: Tuple[Tuple[str, int], ...]
    yield_distribution: Tuple[Tuple[int, int], ...]
    halt_keys: Tuple[str, ...]


def score_class(results: Sequence[SweepResult], requested: int) -> ClassScore:
    a = results[0].archetype; iv, ic = INTENDED[a]
    ghalt = [r for r in results if r.generator_halt]; ehalt = [r for r in results if r.evaluability_halt]
    scored = [r for r in results if not r.generator_halt and not r.evaluability_halt]
    kind = "false_nd" if a in SCIENTIFIC_CLASSES else "false_scientific"
    n = len(scored)
    hk = tuple(sorted({str(r.evaluability_halt) for r in ehalt}))
    if n == 0:
        return ClassScore(a, iv, ic, len(results), 0, len(ehalt), len(ghalt), kind, 0, 1.0, False, False, 0.0, 0, (), (), hk)
    errors = sum(1 for r in scored if r.final_verdict == "NOT_DISTINGUISHED") if kind == "false_nd" else sum(1 for r in scored if r.final_verdict in ("LOCATED", "NOT_PRODUCED"))
    ub = clopper_pearson_upper(errors, n); cap_ok = ub <= CAP
    complete = (len(results) == requested == SWEEPS_PER_CLASS) and n == SWEEPS_PER_CLASS and not ehalt and not ghalt and cap_ok
    vc: Dict[str, int] = {}; yd: Dict[int, int] = {}
    for r in scored:
        vc[r.final_verdict] = vc.get(r.final_verdict, 0) + 1
        if r.router_row in ("P2R-5", "P2R-6", "P2R-4"): yd[r.realized_insertions] = yd.get(r.realized_insertions, 0) + 1
    agree_n = sum(1 for r in scored if r.final_verdict == iv and r.final_cause == ic)
    return ClassScore(a, iv, ic, len(results), n, len(ehalt), len(ghalt), kind, errors, ub, cap_ok, complete, agree_n / n, agree_n,
                      tuple(sorted(vc.items())), tuple(sorted(yd.items())), hk)


def validate_class_score(s, requested: int) -> None:
    if type(s) is not ClassScore: raise AuditDomainError("validate_class_score requires an exact ClassScore")
    if s.archetype not in INTENDED: raise AuditDomainError(f"unknown archetype {s.archetype!r}")
    iv, ic = INTENDED[s.archetype]
    if (s.intended_verdict, s.intended_cause) != (iv, ic): raise AuditDomainError("intended verdict/cause differ from the frozen map")
    for k_ in ("attempted", "scored", "halted", "generator_halted", "errors"):
        v_ = getattr(s, k_)
        if type(v_) is not int or v_ < 0: raise AuditDomainError(f"ClassScore.{k_} must be a non-negative exact int")
    for k_ in ("statistical_cap_pass", "complete_pass"):
        if type(getattr(s, k_)) is not bool: raise AuditDomainError(f"ClassScore.{k_} must be an exact bool")
    if s.scored + s.halted + s.generator_halted != s.attempted: raise AuditDomainError("scored + halted + generator_halted must equal attempted")
    kind = "false_nd" if s.archetype in SCIENTIFIC_CLASSES else "false_scientific"
    if s.applicable_error != kind: raise AuditDomainError("applicable error differs from the class partition")
    vcs = s.verdict_counts
    if type(vcs) is not tuple or any(type(e) is not tuple or len(e) != 2 for e in vcs): raise AuditDomainError("verdict_counts must be an exact tuple of 2-tuples")
    keys = [e[0] for e in vcs]
    if any(type(k_) is not str or k_ not in V.VERDICTS for k_ in keys): raise AuditDomainError("verdict_counts keys must be M4 verdicts")
    if len(set(keys)) != len(keys) or keys != sorted(keys): raise AuditDomainError("verdict_counts must be unique and canonically ordered")
    if any(type(v_) is not int or isinstance(v_, bool) or v_ <= 0 for _, v_ in vcs): raise AuditDomainError("verdict_counts values must be positive exact ints")
    if sum(v_ for _, v_ in vcs) != s.scored: raise AuditDomainError("verdict_counts must sum to scored")
    if s.scored == 0 and vcs != (): raise AuditDomainError("unscored class must carry empty verdict_counts")
    vc = dict(vcs)
    errs = vc.get("NOT_DISTINGUISHED", 0) if kind == "false_nd" else vc.get("LOCATED", 0) + vc.get("NOT_PRODUCED", 0)
    if s.errors != errs: raise AuditDomainError("errors differ from the verdict counts")
    if type(s.exact_agreement_count) is not int or isinstance(s.exact_agreement_count, bool) or not 0 <= s.exact_agreement_count <= s.scored:
        raise AuditDomainError("exact_agreement_count must be an exact int in [0, scored]")
    if s.exact_agreement_count > vc.get(iv, 0): raise AuditDomainError("exact agreement cannot exceed the intended-verdict count")
    if s.exact_agreement_descriptive != ((s.exact_agreement_count / s.scored) if s.scored else 0.0): raise AuditDomainError("exact_agreement_descriptive must derive from the count")
    yd = s.yield_distribution
    if type(yd) is not tuple or any(type(e) is not tuple or len(e) != 2 for e in yd): raise AuditDomainError("yield_distribution must be an exact tuple of 2-tuples")
    ykeys = [e[0] for e in yd]
    if any(type(k_) is not int or isinstance(k_, bool) or k_ < 0 for k_ in ykeys) or len(set(ykeys)) != len(ykeys) or ykeys != sorted(ykeys):
        raise AuditDomainError("yield keys must be unique canonically ordered non-negative exact ints")
    if any(type(v_) is not int or isinstance(v_, bool) or v_ <= 0 for _, v_ in yd) or sum(v_ for _, v_ in yd) > s.scored:
        raise AuditDomainError("yield counts must be positive exact ints totalling at most scored")
    hk = s.halt_keys
    if type(hk) is not tuple or any(type(k_) is not str or not k_.startswith("apparatus:") for k_ in hk) or list(hk) != sorted(set(hk)):
        raise AuditDomainError("halt_keys must be a canonical tuple of unique apparatus: strings")
    if (s.halted == 0) != (hk == ()): raise AuditDomainError("halt_keys must be empty iff halted == 0")
    if s.scored == 0:
        if (s.cp_upper_95, s.statistical_cap_pass, s.complete_pass) != (1.0, False, False): raise AuditDomainError("unscored class must carry cp 1.0 and no passes")
    else:
        if s.cp_upper_95 != clopper_pearson_upper(s.errors, s.scored): raise AuditDomainError("cp_upper_95 differs from the recomputed bound")
        if s.statistical_cap_pass is not (s.cp_upper_95 <= CAP): raise AuditDomainError("statistical_cap_pass differs from the recomputed cap test")
        comp = (s.attempted == requested == SWEEPS_PER_CLASS) and s.scored == SWEEPS_PER_CLASS and s.halted == 0 and s.generator_halted == 0 and s.statistical_cap_pass
        if s.complete_pass is not comp: raise AuditDomainError("complete_pass differs from the recomputed completion rule")


@dataclass(frozen=True)
class AuditRecord:
    version: str
    ensemble: str
    master: int
    requested_sweeps_per_class: int
    adapter_role: str
    adapter_sha256: str
    adapter_payload_identity: str
    audit_declaration_sha256: str
    generator_declaration_sha256: str
    interpretation_002_sha256: str
    scores: Tuple[ClassScore, ...]
    ensemble_pass: bool
    record_sha256: str

    def identity_body(self):
        return (self.version, self.ensemble, self.master, self.requested_sweeps_per_class, self.adapter_role, self.adapter_sha256, self.adapter_payload_identity,
                self.audit_declaration_sha256, self.generator_declaration_sha256, self.interpretation_002_sha256, tuple(asdict(s) for s in self.scores), self.ensemble_pass)

    def summary(self) -> str:
        return " | ".join(f"{s.archetype}:{s.applicable_error}={s.errors}/{s.scored} ub={s.cp_upper_95:.3f} {'C' if s.complete_pass else '-'}" for s in self.scores) \
               + f" => ensemble_pass={self.ensemble_pass}"


INTERPRETATION_002_SHA256 = "198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034"
ENSEMBLES = ("design", "held_out")


def _ensemble_master(ensemble: str) -> int:
    if ensemble not in ENSEMBLES: raise AuditDomainError("ensemble must be 'design' or 'held_out'")
    return production_masters()[0 if ensemble == "design" else 1]


def validate_audit_record(rec, expect_production: bool = True) -> None:
    if type(rec) is not AuditRecord: raise AuditDomainError("validate_audit_record requires an exact AuditRecord")
    verify_frozen_identity()
    if rec.version != AUDIT_VERSION: raise AuditDomainError("record version differs from the audit version")
    if rec.ensemble not in ENSEMBLES: raise AuditDomainError("record ensemble unknown")
    if type(rec.requested_sweeps_per_class) is not int or rec.requested_sweeps_per_class < 1 or type(rec.ensemble_pass) is not bool or type(rec.master) is not int:
        raise AuditDomainError("record count/flag types")
    if (rec.audit_declaration_sha256, rec.generator_declaration_sha256, rec.interpretation_002_sha256) != (AUDIT_DECLARATION_SHA256_LITERAL, GENERATOR_DECLARATION_SHA256_LITERAL, INTERPRETATION_002_SHA256):
        raise AuditDomainError("record declaration identities differ from the current M6 declarations")
    if rec.adapter_role not in ADAPTER_ROLES: raise AuditDomainError("record adapter role unknown")
    if expect_production:
        if rec.master != _ensemble_master(rec.ensemble): raise AuditDomainError("record master differs from the production master of its ensemble")
        if rec.adapter_role != "production": raise AuditDomainError("a production record requires the production adapter")
        prod = build_adapter("production")
        if (rec.adapter_sha256, rec.adapter_payload_identity) != (prod.body_sha256, prod.payload_identity): raise AuditDomainError("record adapter identity does not replay")
    if tuple(s.archetype for s in rec.scores) != CLASSES: raise AuditDomainError("record class set/order differs from the frozen classes")
    for s in rec.scores: validate_class_score(s, rec.requested_sweeps_per_class)
    ens = all(s.complete_pass for s in rec.scores) and rec.adapter_role == "production" and expect_production
    if rec.ensemble_pass is not ens: raise AuditDomainError("ensemble_pass differs from the recomputed value")
    if rec.record_sha256 != _digest(rec.identity_body()): raise AuditDomainError("record identity does not recompute")


def run_audit(ensemble: str, adapter: ThresholdAdapter, sweeps_per_class: Optional[int] = None, master: Optional[int] = None) -> AuditRecord:
    """A production audit (500 per class) requires the production adapter, the production master of its ensemble and no `master`
    override; a smoke audit (fewer sweeps) may name any master and adapter role and is never a freeze pass."""
    verify_frozen_identity()
    if ensemble not in ENSEMBLES: raise AuditDomainError("ensemble must be 'design' or 'held_out'")
    if type(adapter) is not ThresholdAdapter: raise AuditDomainError("adapter must be a ThresholdAdapter")
    n = SWEEPS_PER_CLASS if sweeps_per_class is None else _exact_int(sweeps_per_class, "sweeps_per_class", 1)
    prod = is_production_adapter(adapter)
    if n == SWEEPS_PER_CLASS:
        if not prod: raise AuditDomainError("a 500-sweep audit requires the production adapter (identities re-derived, not the role label)")
        if master is not None: raise AuditDomainError("a 500-sweep audit runs under the production master of its ensemble, never an override")
        m = _ensemble_master(ensemble)
    else:
        m = _ensemble_master(ensemble) if master is None else _exact_int(master, "master", 1)
    scores = tuple(score_class([run_sweep(name, i, m, adapter) for i in range(n)], n) for name in CLASSES)
    ens = all(s.complete_pass for s in scores) and prod and n == SWEEPS_PER_CLASS
    fields = (AUDIT_VERSION, ensemble, m, n, adapter.role, adapter.body_sha256, adapter.payload_identity, AUDIT_DECLARATION_SHA256_LITERAL,
              GENERATOR_DECLARATION_SHA256_LITERAL, INTERPRETATION_002_SHA256, scores, ens)
    probe = AuditRecord(*fields, "")
    return AuditRecord(*fields, _digest(probe.identity_body()))


@dataclass(frozen=True)
class AuditQualification:
    design_record_sha256: str
    held_out_record_sha256: str
    adapter_sha256: str
    adapter_payload_identity: str
    audit_declaration_sha256: str
    generator_declaration_sha256: str
    interpretation_002_sha256: str
    qualified: bool
    reasons: Tuple[str, ...]
    qualification_sha256: str = ""

    def identity_body(self):
        return (self.design_record_sha256, self.held_out_record_sha256, self.adapter_sha256, self.adapter_payload_identity, self.audit_declaration_sha256,
                self.generator_declaration_sha256, self.interpretation_002_sha256, self.qualified, self.reasons)


def _qualification_reasons(design, held_out) -> List[str]:
    reasons: List[str] = []
    for rec, name in ((design, "design"), (held_out, "held_out")):
        try: validate_audit_record(rec, expect_production=True)
        except AuditDomainError as e: reasons.append(f"{name}: invalid record - {e}")
    for rec, name in ((design, "design"), (held_out, "held_out")):
        if type(rec) is not AuditRecord: reasons.append(f"{name}: not an AuditRecord"); continue
        if rec.ensemble != name: reasons.append(f"{name}: wrong ensemble label")
        if rec.requested_sweeps_per_class != SWEEPS_PER_CLASS: reasons.append(f"{name}: not 500 requested")
        if rec.adapter_role != "production": reasons.append(f"{name}: adapter not production")
        if tuple(s.archetype for s in rec.scores) != CLASSES: reasons.append(f"{name}: class set differs")
        for s in rec.scores:
            if not (s.attempted == s.scored == SWEEPS_PER_CLASS and s.halted == 0 and s.generator_halted == 0 and s.statistical_cap_pass and s.complete_pass):
                reasons.append(f"{name}:{s.archetype}: not complete")
        if not rec.ensemble_pass: reasons.append(f"{name}: ensemble_pass False")
    if type(design) is AuditRecord and type(held_out) is AuditRecord:
        if design.master == held_out.master: reasons.append("masters not distinct")
        if design.adapter_sha256 != held_out.adapter_sha256: reasons.append("adapter identities differ")
        if design.record_sha256 == held_out.record_sha256: reasons.append("record identities not distinct")
    return reasons


def validate_audit_qualification(q, design, held_out) -> None:
    if type(q) is not AuditQualification: raise AuditDomainError("validate_audit_qualification requires an exact AuditQualification")
    reasons = tuple(_qualification_reasons(design, held_out))
    if type(q.reasons) is not tuple or any(type(r) is not str for r in q.reasons) or q.reasons != reasons: raise AuditDomainError("qualification reasons differ from the recomputed reasons")
    if type(q.qualified) is not bool or q.qualified is not (not reasons): raise AuditDomainError("qualified must equal (reasons == ())")
    d_id = design.record_sha256 if type(design) is AuditRecord else ""; h_id = held_out.record_sha256 if type(held_out) is AuditRecord else ""
    if (q.design_record_sha256, q.held_out_record_sha256) != (d_id, h_id): raise AuditDomainError("qualification record identities differ from the records")
    prod = build_adapter("production")
    if (q.adapter_sha256, q.adapter_payload_identity) != (prod.body_sha256, prod.payload_identity): raise AuditDomainError("qualification adapter identity does not replay")
    if (q.audit_declaration_sha256, q.generator_declaration_sha256, q.interpretation_002_sha256) != (AUDIT_DECLARATION_SHA256_LITERAL, GENERATOR_DECLARATION_SHA256_LITERAL, INTERPRETATION_002_SHA256):
        raise AuditDomainError("qualification declaration identities differ from the current declarations")
    for k_ in ("adapter_sha256", "adapter_payload_identity", "audit_declaration_sha256", "generator_declaration_sha256", "interpretation_002_sha256", "qualification_sha256"):
        if not _is_hex64(getattr(q, k_)): raise AuditDomainError(f"qualification field {k_} is not a 64-hex sha256")
    if q.qualified and not (_is_hex64(q.design_record_sha256) and _is_hex64(q.held_out_record_sha256)): raise AuditDomainError("a qualified object must carry two record identities")
    if q.qualification_sha256 != _digest(q.identity_body()): raise AuditDomainError("qualification identity does not recompute")


def qualify_audit(design, held_out) -> AuditQualification:
    """THE FREEZE-QUALIFYING ACT for M6: both records validated, the reasons computed by the one frozen procedure, the object
    validated against both records before return."""
    reasons = tuple(_qualification_reasons(design, held_out))
    prod = build_adapter("production")
    fields = (design.record_sha256 if type(design) is AuditRecord else "", held_out.record_sha256 if type(held_out) is AuditRecord else "",
              prod.body_sha256, prod.payload_identity, AUDIT_DECLARATION_SHA256_LITERAL, GENERATOR_DECLARATION_SHA256_LITERAL, INTERPRETATION_002_SHA256, not reasons, reasons)
    q = AuditQualification(*fields); q = AuditQualification(*fields, _digest(q.identity_body()))
    validate_audit_qualification(q, design, held_out)
    return q


# ----------------------------------------------------------------------------- the §4.3 price and the job-0 comparison side
@dataclass(frozen=True)
class PricingRecord:
    replicates: int
    master: int
    theta_p: float
    theta_t: float
    s_min_rejections: int                 # the §4.3 event: S_min > θ_P under the NULL source
    s_min_rejection_rate: float
    cp_upper_95: float                    # exact one-sided upper bound on the rate
    alpha_p_nominal: float
    construction_bound: float             # N_WINDOWS·(1 − F_W(θ_P)), the Bonferroni bound of M3
    s_term_no_sustained: int              # descriptive: S_term ≤ θ_T (expected ≈ 1 − α_T)
    source: str
    declaration_sha256: str

    def summary(self) -> str:
        return (f"PRICE {self.replicates} NULL runs under {self.master}: S_min > theta_P {self.s_min_rejections} ({self.s_min_rejection_rate:.5f}), "
                f"CP-95 upper {self.cp_upper_95:.5f} vs alpha_P {self.alpha_p_nominal}; construction bound {self.construction_bound:.6f}")


def run_pricing(adapter: ThresholdAdapter, replicates: Optional[int] = None, master: Optional[int] = None) -> PricingRecord:
    """The contract's descriptive price (§4.3; Interpretation 002 pt 9a): complete ten-window NULL runs of the M6 NULL source,
    streams SeedSequence([pricing_master, 0, replicate]). The full 10,000 run requires the production adapter and master."""
    verify_frozen_identity()
    n = PRICING_REPLICATES if replicates is None else _exact_int(replicates, "replicates", 1)
    if n == PRICING_REPLICATES:
        if master is not None or not is_production_adapter(adapter): raise AuditDomainError("the full price runs under the production adapter and pricing master only")
        m = production_masters()[2]
    else:
        m = production_masters()[2] if master is None else _exact_int(master, "master", 1)
    th = N.null_thresholds(F8_LEVELS_MICRO[0])
    tp, tt = adapter.theta_p, adapter.theta_t
    rej = sno = 0
    for i in range(n):
        g = np.random.default_rng(np.random.SeedSequence([int(m), 0, int(i)]))
        st = K.tail_stats(rho_record(gen_null_run(g)))
        rej += st.s_min > tp; sno += st.s_term <= tt
    return PricingRecord(n, m, tp, tt, rej, rej / n, clopper_pearson_upper(rej, n), N.ALPHA_P, N.familywise_nominal_bound(th), sno, "m6_null_count_process", GENERATOR_DECLARATION_SHA256_LITERAL)


@dataclass(frozen=True)
class SurrogateLevelStats:
    """The surrogate side of the job-0 comparison (declaration §8): unmodulated E at a pass-1 level, n runs, tail density per
    Interpretation 001 (mean over ticks 2001..3000). The lattice side comes only from the separately authorized job 0."""
    level_micro: int
    replicates: int
    master: int
    tail_mean: float
    tail_sd: float                        # ddof = 1
    se_mean: float
    se_sd_approx: float                   # sd/sqrt(2(n-1))


def surrogate_level_stats(level_micro: int, master: int, replicates: int = COMPARISON_REPLICATES) -> SurrogateLevelStats:
    verify_frozen_identity()
    u = _exact_int(level_micro, "level_micro")
    if u not in F8_LEVELS_MICRO: raise AuditDomainError("the comparison is defined at pass-1 levels only")
    n = _exact_int(replicates, "replicates", 2); m = _exact_int(master, "master", 1)
    vals = []
    for i in range(n):
        g = np.random.default_rng(np.random.SeedSequence([m, 1, u, i]))
        vals.append(float(rho_record(gen_sustained_run(CL.level_m(u), None, g))[TAIL_START:].mean()))
    a = np.asarray(vals); sd = float(a.std(ddof=1))
    return SurrogateLevelStats(u, n, m, float(a.mean()), sd, sd / math.sqrt(n), sd / math.sqrt(2 * (n - 1)))
