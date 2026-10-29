"""mfa_instrument/f8/closure.py — Flight 8 module M5: the closure and the census (Contract F8 v0.8.4 §3, §4.8, §7.3;
design note v0.3 §3; E1 M5's framework carried, its content rebuilt from §3).

THE CLOSURE (§3.1, homogeneous bases, d_i = ρ):  ρ_{t+1} = (1 − ρ_t)·[1 − e^(−(η_floor + gλ̄ρ_t)Δt)] + ρ_t·e^(−μΔt).
Skeleton (η_floor = 0): ρ = 0 is a fixed point with multiplier J₀ = e^(−μΔt) + gλ̄Δt; the crossing J₀ = 1 ⇔ m = 1 (§3.2);
for m > 1 a positive fixed point ρ*_sk(m), continuous from zero. Realization (η₀): a unique positive fixed point
ρ*(m; η₀) at every m (§3.3), inflection m_infl. Both tables are APPENDIX A's objects of record (`94d527624beafa7c…`):
this module computes them by Appendix A's own procedure (the same iteration, start, tolerance and float64 arithmetic)
and `verify_against_appendix_a` requires bit equality with the committed JSON. Δm (§3.4), m_infl, m_lat (the pair
closure of Appendix B.2, Appendix A row) are reproduced the same way.

OUTCOME HYGIENE (E1 M5's L2 ruling, carried): this module carries NO reference result. The reference structure of record
is created only by the canonical dense job (`dense_reference`, role `reference_of_record`, exact declared grid, zero
halts), in a separate result record; analysis-subset objects keep their own role and can never issue a freeze-facing
status. The pre-registered EXPECTATION for the realization's M4 morphology is stated in the contract, not here (§1.3(a),
§4.9: `NOT_PRODUCED (no null-consistent phase)`, because ρ*(m; η₀) > θ_P at every sweep level).

WHAT M5 PUBLISHES (the closure-fidelity comparators of §1.2′, never scored): the closure crossing m = 1; the pair crossing
m_lat; the realization inflection m_infl; ρ*_sk(m) and ρ*(m; η₀) at the 24 levels; the pair skeleton and realization
branches at the 24 levels. And the §3.4 TOLERANCE MACHINERY: Δm; the evaluability band k_R·√(ŝ_X(m₋)² + ŝ_X(m₊)²)·1.2533/√20
and the fidelity band k_R·ŝ(m)·1.2533/√20 from the two-part CALIBRATION CENSUS (§7.3 job 0, its own master, never
scored); the MDD ceilings max_m MDD_X ≤ 0.02 with the predeclared STOP PATH (a violation stops the stage before any
canonical census; a new instrument version follows — never a sample-size change after data exist).

DESIGN STABILITY (E1-R grammar, §7.3 item 4): `projection_sweep` runs the closure with FINITE-N INDEPENDENT-CELL sampling
(each of N cells follows the map's probabilities independently — the zero-correlation lattice) through M2's statuses, the
16/2/4 label and M4's verdict, and `design_stability` compares the sweeps' categories with the reference of record over an
exact declared ensemble with halts failing closed (any halt → NOT EVALUABLE; rates over the attempted denominator).

REFERENCE STABILITY (§4.8 "as E1"; F8 has no base template under homogeneous bases — declaration M5-3): the structure
class must be reproduced on alternative dense grids (half and double the declared step) and the fixed points by an
independent solver (bisection on g(ρ) − ρ) within a declared tolerance; validated by replay.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..config import MICRO_UNITS
from . import classify as K
from . import config as C
from . import dynamics as D
from . import null as N
from . import verdict as V
from .classify import N_CELLS, N_WINDOWS, WINDOW
from .config import F8_LEVELS_MICRO, level_id

CLOSURE_VERSION = "f8_stage1_m5_v1"
MU, DT, ETA0, G = C.F8_MU, float(C.F8_DT), C.F8_ETA0, C.F8_G
Q_DEACT = 1.0 - math.exp(-MU * DT)
N_CELLS_F = float(N_CELLS)
# Appendix A's fixed-point procedure (appendix_a.py v2 `fixed_point`): start 0.5, tol 1e-15, cap 400000 iterations
FP_RHO0, FP_TOL, FP_ITERS = 0.5, 1e-15, 400000
T_PRE = C.F8_TICKS - C.F8_TAIL_TICKS                      # 2000
QS_MIN_ACTIVE = 50                                        # ratified: freeze record §3 item 15
K_R = 3                                                   # ratified: item 17
MEDIAN_SE_FACTOR = 1.2533                                 # standard error of a median of 20 = 1.2533·ŝ/√20 (§3.4)
PANEL_N = 20
MDD_CEILING = 0.02                                        # ratified: item 12 (both objects)
DENSE_POINTS = 701                                        # §4.8 [PROPOSED — E1's count]; declaration M5-1 (positions by round-half-even micro-units)
DESIGN_STABILITY_SWEEPS = 200                             # E1's declared ensemble, carried (declaration M5-2)
PROJECTION_MASTER = 420261028                             # declared: finite-N projection-sweep master (separate from every panel/validation master)
STABILITY_FP_TOL = 1e-11                                  # declared: agreement of the independent fixed-point solver with Appendix A's iteration
APPENDIX_A_BIND_TOL = 1e-12                               # declared (M5-6): absolute tolerance binding this module's fixed-point tables, Δm and m_lat to
                                                          # Appendix A's JSON. Same procedure and float64 expression order, but exp() is the platform's
                                                          # libm (glibc vs UCRT differ by ≤ 1 ulp), so bit equality is not a cross-platform property.
HALT_POLICY = "any halt in a canonical ensemble -> gate NOT EVALUABLE (incomplete); rates reported over the attempted denominator"
STRUCTURE_CLASSES = ("ORDER-VIOLATING/MULTIPLE", "NO-SUSTAINED-PHASE", "NO-NULL-PHASE", "REFERENCE-UNRESOLVED", "UNIQUE-THRESHOLD")
STRUCTURE_FROM_RULE = {"1": "ORDER-VIOLATING/MULTIPLE", "2": ("NO-NULL-PHASE", "REFERENCE-UNRESOLVED"), "3": ("NO-SUSTAINED-PHASE", "REFERENCE-UNRESOLVED"),
                       "4a": "REFERENCE-UNRESOLVED", "4b": "REFERENCE-UNRESOLVED", "4c": "REFERENCE-UNRESOLVED", "4d": "UNIQUE-THRESHOLD"}

CLOSURE_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("version", CLOSURE_VERSION), ("mu", MU), ("dt", DT), ("eta0", ETA0), ("g", G), ("n_cells", N_CELLS),
    ("map", "rho' = (1-rho)(1-exp(-(eta+g*lambda_bar*rho)*dt)) + rho*exp(-mu*dt); lambda_bar = m*(1-exp(-mu*dt))/(g*dt)"),
    ("fixed_point_procedure", (FP_RHO0, FP_TOL, FP_ITERS)), ("t_pre", T_PRE), ("qs_min_active", QS_MIN_ACTIVE), ("k_r", K_R),
    ("median_se_factor", MEDIAN_SE_FACTOR), ("panel_n", PANEL_N), ("mdd_ceiling", MDD_CEILING),
    ("dense_points", DENSE_POINTS), ("design_stability_sweeps", DESIGN_STABILITY_SWEEPS), ("projection_master", PROJECTION_MASTER),
    ("stability_fp_tol", STABILITY_FP_TOL), ("appendix_a_bind_tol", APPENDIX_A_BIND_TOL), ("halt_policy", HALT_POLICY), ("structure_classes", STRUCTURE_CLASSES),
    ("reference_result", "NONE IN THE INSTRUMENT: the reference of record is created only by the canonical dense job (separate result record)"),
    ("appendix_a_sha256", C.F8_APPENDIX_A_SHA256),
)
CLOSURE_SHA256_LITERAL = "11074edcacbe26d2fe3b33eff4f7fca4a328a5d7b9dcd84786d2f115206ce204"


class ClosureDomainError(ValueError):
    """Frozen identity violated or input outside the closure's domain."""


class ClosureApparatusError(RuntimeError):
    """An apparatus defect during a canonical job: halts the stage, never a replicate."""


def _digest(obj) -> str: return hashlib.sha256(repr(obj).encode()).hexdigest()
def _canon(obj) -> str: return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def verify_frozen_identity() -> None:
    if _digest(CLOSURE_DECLARATION) != CLOSURE_SHA256_LITERAL:
        raise ClosureDomainError("closure declaration differs from its frozen literal digest")
    C.verify_frozen_identity(); K.verify_frozen_identity(); N.verify_frozen_identity(); V.verify_frozen_identity()
    d = dict(CLOSURE_DECLARATION)
    live = {"mu": MU, "dt": DT, "eta0": ETA0, "g": G, "n_cells": N_CELLS, "fixed_point_procedure": (FP_RHO0, FP_TOL, FP_ITERS), "t_pre": T_PRE,
            "qs_min_active": QS_MIN_ACTIVE, "k_r": K_R, "median_se_factor": MEDIAN_SE_FACTOR, "panel_n": PANEL_N, "mdd_ceiling": MDD_CEILING,
            "dense_points": DENSE_POINTS, "design_stability_sweeps": DESIGN_STABILITY_SWEEPS, "projection_master": PROJECTION_MASTER,
            "stability_fp_tol": STABILITY_FP_TOL, "appendix_a_bind_tol": APPENDIX_A_BIND_TOL, "structure_classes": STRUCTURE_CLASSES, "appendix_a_sha256": C.F8_APPENDIX_A_SHA256, "version": CLOSURE_VERSION}
    for k_, v_ in live.items():
        if d[k_] != v_ or type(d[k_]) is not type(v_):
            raise ClosureDomainError(f"closure declaration field {k_} differs from the live global")
    if (QS_MIN_ACTIVE, K_R, MDD_CEILING, PANEL_N, T_PRE) != (50, 3, 0.02, 20, 2000) or MU != 0.2 or ETA0 != -math.log(0.99) or G != 1.0:
        raise ClosureDomainError("closure constants differ from the ratified values")
    if PROJECTION_MASTER in (C.F8_SEED_PANEL_MASTER, C.F8_CALIBRATION_MASTER, N.VALIDATION_REPLICATE_MASTER, N.VALIDATION_PROTOCOL_ATTEMPT_2.replicate_master, 20260917):
        raise ClosureDomainError("projection master collides with another declared master")
    if len(C.F8_SEED_PANEL) != PANEL_N or len(C.F8_CALIBRATION_SEED_PANEL) != PANEL_N:
        raise ClosureDomainError("panel size differs from the declared 20")


# ----------------------------------------------------------------------------- the map and its fixed points (Appendix A's arithmetic)
def lambda_bar(m: float) -> float:
    """Appendix A: glam = m·q/Dt (identical arithmetic to appendix_a.py `fmap`)."""
    return m * Q_DEACT / DT


def g_map(rho: float, m: float, eta: float) -> float:
    """§3.1, scalar, in Appendix A's exact float64 expression order."""
    glam = lambda_bar(m)
    return (1 - rho) * (1 - math.exp(-(eta + glam * rho) * DT)) + rho * math.exp(-MU * DT)


def g_map_vec(rho: np.ndarray, m: float, eta: float) -> np.ndarray:
    glam = lambda_bar(m)
    return (1.0 - rho) * (1.0 - np.exp(-(eta + glam * rho) * DT)) + rho * math.exp(-MU * DT)


def fixed_point(m: float, eta: float, rho0: float = FP_RHO0, iters: int = FP_ITERS, tol: float = FP_TOL) -> float:
    """Appendix A's `fixed_point`, verbatim in procedure: iterate from rho0 until |Δ| < tol."""
    rho = rho0
    for _ in range(iters):
        r2 = g_map(rho, m, eta)
        if abs(r2 - rho) < tol:
            return r2
        rho = r2
    return rho


def rho_sk(m: float) -> float:
    """Skeleton fixed point: exactly 0 for m ≤ 1 (the absorbing state is stable), else the positive branch (Appendix A)."""
    return 0.0 if m <= 1.0 else fixed_point(m, 0.0)


def rho_re(m: float) -> float:
    return fixed_point(m, ETA0)


def skeleton_multiplier(m: float) -> float:
    """J₀ = e^(−μΔt) + gλ̄Δt at ρ = 0 (§3.2); J₀ = 1 ⇔ m = 1."""
    return math.exp(-MU * DT) + lambda_bar(m) * DT


def fixed_point_bisection(m: float, eta: float, lo: float = 1e-12, hi: float = 1.0, iters: int = 200) -> float:
    """INDEPENDENT solver for the positive fixed point: bisection on h(ρ) = g(ρ) − ρ, which is positive just above 0 when
    the positive branch exists and negative at ρ = 1 (g(1) = e^(−μ) < 1)."""
    f_lo = g_map(lo, m, eta) - lo
    if f_lo <= 0.0:
        return 0.0
    for _ in range(iters):
        mid = (lo + hi) / 2
        if g_map(mid, m, eta) - mid > 0.0: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def level_m(level_micro: int) -> float:
    """Appendix A's level value: levels_m = [u / MICRO]."""
    return int(level_micro) / MICRO_UNITS


def tables() -> Tuple[Dict[str, float], Dict[str, float]]:
    """ρ*_sk and ρ*(m; η₀) at the 24 pass-1 levels, keyed by Appendix A's "%.6f" rendering."""
    verify_frozen_identity()
    ms = [level_m(u) for u in F8_LEVELS_MICRO]
    return {f"{m:.6f}": rho_sk(m) for m in ms}, {f"{m:.6f}": rho_re(m) for m in ms}


# ----------------------------------------------------------------------------- Δm, m_infl, m_lat (Appendix A rows)
@dataclass(frozen=True)
class DeltaM:
    lower: float          # 1 − m ≥ ln N/(q·T_pre): deterministic decay of the active count from the high initialization
    upper: float          # m − 1 at N·ρ*_sk(m) = 50 (bisection on §3.1)
    s: float              # one pass-1 spacing in m
    value: float          # max(lower, upper) + s


def delta_m() -> DeltaM:
    verify_frozen_identity()
    lower = math.log(N_CELLS) / (Q_DEACT * T_PRE)
    lo, hi = 1.0, 2.5
    for _ in range(200):
        mid = (lo + hi) / 2
        if N_CELLS * rho_sk(mid) < QS_MIN_ACTIVE: lo = mid
        else: hi = mid
    upper = hi - 1.0
    s_m = C.S_P1_MICRO / MICRO_UNITS
    return DeltaM(lower, upper, s_m, max(lower, upper) + s_m)


def m_infl() -> float:
    """argmax dρ*/dm by central differences on the 0.0005 grid over [0.5, 2.0] (Appendix A row 9)."""
    verify_frozen_identity()
    grid = [0.5 + i * 0.0005 for i in range(int((2.0 - 0.5) / 0.0005) + 1)]
    vals = [rho_re(m) for m in grid]
    best, best_m = -1.0, None
    for k in range(1, len(grid) - 1):
        d = (vals[k + 1] - vals[k - 1]) / (grid[k + 1] - grid[k - 1])
        if d > best: best, best_m = d, grid[k]
    return best_m


def pair_leading_multiplier(m: float) -> float:
    """Appendix B.2 linearization of the η = 0 pair map at the absorbing state (Appendix A's `leading_multiplier`)."""
    q = Q_DEACT; glam = m * q
    a1 = 1 - math.exp(-glam / 8)
    A = [[1 - q + 8 * a1, -8 * a1], [2 * (1 - q) * a1, (1 - q) ** 2 - 2 * (1 - q) * a1]]
    tr = A[0][0] + A[1][1]; det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    disc = tr * tr - 4 * det
    if disc >= 0:
        return max(abs((tr + math.sqrt(disc)) / 2), abs((tr - math.sqrt(disc)) / 2))
    return math.sqrt(det)


def m_lat() -> float:
    verify_frozen_identity()
    lo, hi = 1.0, 2.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if pair_leading_multiplier(mid) < 1: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def _pair_step(rho: float, pAA: float, eta: float, m: float) -> Tuple[float, float]:
    """Appendix B.2 nonlinear pair map (pair_approx.py `step`), one synchronous tick."""
    qd = Q_DEACT; glam = m * qd
    if rho <= 0: return 0.0, 0.0
    qA_I = (rho - pAA) / (1 - rho) if rho < 1 else 0.0
    qA_I = min(max(qA_I, 0.0), 1.0)
    pAI = rho - pAA; pII = 1 - 2 * rho + pAA
    def ak(k): return 1 - math.exp(-(eta + glam * k / 8))
    def E_a(n, p, offset=0): return sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) * ak(k + offset) for k in range(n + 1))
    rho2 = rho * (1 - qd) + (1 - rho) * E_a(8, qA_I)
    pAA2 = pAA * (1 - qd) ** 2 + 2 * pAI * (1 - qd) * E_a(7, qA_I, offset=1) + pII * E_a(7, qA_I) ** 2
    return rho2, pAA2


def pair_fixed_point(eta: float, m: float, rho0: float = 0.5, iters: int = 20000) -> float:
    rho, pAA = rho0, rho0 * rho0
    for _ in range(iters):
        r2, p2 = _pair_step(rho, pAA, eta, m)
        if abs(r2 - rho) < 1e-13 and abs(p2 - pAA) < 1e-13: return r2
        rho, pAA = r2, p2
    return rho


# ----------------------------------------------------------------------------- the closure publication (fidelity-tier comparators)
@dataclass(frozen=True)
class ClosurePublication:
    version: str
    m_closure: float                       # 1.0, the mean-field crossing (§3.2)
    m_lat: float                           # pair-approximation crossing (Appendix B)
    m_infl: float                          # realization inflection (§3.3)
    delta_m: DeltaM
    levels_micro: Tuple[int, ...]
    rho_sk: Tuple[float, ...]              # at the 24 levels
    rho_re: Tuple[float, ...]
    pair_sk: Tuple[float, ...]             # pair skeleton branch at the 24 levels
    pair_re: Tuple[float, ...]             # pair realization branch
    declaration_sha256: str
    result_sha256: str = ""

    def identity(self) -> str:
        d = asdict(self); d.pop("result_sha256", None); return hashlib.sha256(_canon(d).encode()).hexdigest()


def closure_publication() -> ClosurePublication:
    verify_frozen_identity()
    sk, re_ = tables(); ms = [level_m(u) for u in F8_LEVELS_MICRO]
    pub = ClosurePublication(CLOSURE_VERSION, 1.0, m_lat(), m_infl(), delta_m(), tuple(F8_LEVELS_MICRO),
                             tuple(sk[f"{m:.6f}"] for m in ms), tuple(re_[f"{m:.6f}"] for m in ms),
                             tuple(pair_fixed_point(0.0, m) for m in ms), tuple(pair_fixed_point(ETA0, m) for m in ms), CLOSURE_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(pub, result_sha256=pub.identity())


def validate_closure_publication(p: ClosurePublication) -> None:
    """Validation is by REPLAY."""
    if type(p) is not ClosurePublication: raise ClosureDomainError("not a ClosurePublication")
    if p != closure_publication(): raise ClosureDomainError("closure publication does not replay to its recorded content")


def _parse_appendix_a(raw: bytes) -> dict:
    """The JSON block of an identity-verified APPENDIX_A_OF_RECORD.md (factored so a test can substitute the payload
    after the identity gate without touching that gate)."""
    return json.loads(re.search(r"```json\n(.*?)```", raw.decode("utf-8"), re.S).group(1))


def verify_against_appendix_a(appendix_a_path: str) -> Dict[str, object]:
    """Bind M5 to the object of record. The committed Appendix A's identity must be the frozen SHA-256 exactly; its
    fixed-point tables, Δm (all four fields) and m_lat must equal this module's values to within APPENDIX_A_BIND_TOL
    (absolute); m_infl (a grid value), π₁ and the pass-1 levels must be equal exactly. Same procedure and float64
    expression order as appendix_a.py, but exp() is the platform's libm, so the tables agree bit for bit on the
    platform that produced Appendix A and to ≤ 1 ulp elsewhere; the result reports the maximum deviation and the
    keys that are not bit-equal so the placement record can state what the machine saw."""
    raw = open(appendix_a_path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != C.F8_APPENDIX_A_SHA256:
        raise ClosureDomainError(f"APPENDIX_A_OF_RECORD.md identity {sha[:16]} is not the frozen {C.F8_APPENDIX_A_SHA256[:16]}")
    j = _parse_appendix_a(raw)
    if tuple(int(x) for x in j["levels_micro"]) != F8_LEVELS_MICRO:                       # D4: exact, enforced, not merely reported
        raise ClosureDomainError("Appendix A pass-1 level list differs from the frozen F8_LEVELS_MICRO")
    sk, re_ = tables()
    dm = delta_m(); jd = j["delta_m"]
    mlat = m_lat()
    rows: Dict[str, Tuple[float, float]] = {}
    for name, mine, theirs in (("rho_sk", sk, j["rho_sk"]), ("rho_re", re_, j["rho_re"])):
        if set(theirs) != set(mine): raise ClosureDomainError(f"Appendix A {name} table is keyed on other levels than M5's")
        rows.update({f"{name}[{k}]": (mine[k], float(theirs[k])) for k in theirs})
    rows.update({f"delta_m.{k}": (getattr(dm, k), float(jd[k])) for k in ("lower", "upper", "s", "value")})
    rows["m_lat"] = (mlat, float(j["m_lat"]))
    devs = {k: abs(a - b) for k, (a, b) in rows.items()}
    over = sorted(k for k, d in devs.items() if not d <= APPENDIX_A_BIND_TOL)
    if over: raise ClosureDomainError(f"Appendix A differs from M5 beyond the declared tolerance {APPENDIX_A_BIND_TOL:g}: {over}")
    if float(j["m_infl"]) != m_infl(): raise ClosureDomainError("Appendix A m_infl differs from M5 (grid value; exact)")
    if float(j["null"]["pi1"]) != N.chain_rates()[2]: raise ClosureDomainError("Appendix A pi1 differs from M3's chain rates")
    not_bit_equal = tuple(sorted(k for k, d in devs.items() if d != 0.0))
    return {"appendix_a_sha256": sha, "delta_m": dm.value, "m_infl": m_infl(), "m_lat": mlat,
            "levels_match": True,                                                             # enforced above; kept affirmatively for provenance
            "bind_tol": APPENDIX_A_BIND_TOL, "max_abs_deviation": max(devs.values()), "not_bit_equal": not_bit_equal,
            "bit_equal": not not_bit_equal}


# ----------------------------------------------------------------------------- orbits, projected labels, the dense census
def orbit(m: float, eta: float, rho0: float, ticks: int = C.F8_TICKS) -> np.ndarray:
    """Deterministic orbit of the map from ρ₀, length ticks + 1 (M1's record convention: index t = state after tick t)."""
    out = np.empty(ticks + 1); out[0] = rho0; r = rho0
    for t in range(1, ticks + 1):
        r = g_map(r, m, eta); out[t] = r
    return out


@dataclass(frozen=True)
class ProjectedTail:
    window_means: Tuple[float, ...]
    s_min: float
    s_term: float
    orbit_tail_mean: float


def projected_tail_stats(series: np.ndarray) -> ProjectedTail:
    """M2's geometry on a deterministic orbit (which is not on the count grid, so M2's exact-count path does not apply)."""
    if not isinstance(series, np.ndarray) or series.dtype != np.float64 or series.shape != (K.RECORD_LEN,) or not np.isfinite(series).all() or (series < 0).any() or (series > 1).any():
        raise ClosureDomainError("series must be a finite float64 record of RECORD_LEN in [0, 1]")
    tail = series[K.TAIL_START:K.TAIL_END + 1]
    wm = tuple(float(np.mean(tail[i * WINDOW:(i + 1) * WINDOW])) for i in range(N_WINDOWS))
    return ProjectedTail(wm, float(min(wm)), wm[K.TERMINAL_WINDOW], float(np.mean(tail)))


def projected_label(m_micro: int, th: N.NullThresholds) -> Tuple[str, ProjectedTail]:
    """The realization closure's level label: the orbit from the null's stationary density, M2's precedence against the
    thresholds, and the 16/2/4 rule on 20 identical statuses (S / N / U)."""
    pt = projected_tail_stats(orbit(level_m(m_micro), ETA0, th.pi1))
    status = "SUSTAINED" if pt.s_min > th.theta_p else ("NO_SUSTAINED" if pt.s_term <= th.theta_t else "UNRESOLVED")
    return K.level_label(K.LevelCounts(*(PANEL_N if status == s else 0 for s in K.STATUSES))), pt


def _rhe(fr: Fraction) -> int:
    q, r = divmod(fr.numerator, fr.denominator); twice = 2 * r
    if twice < fr.denominator: return q
    if twice > fr.denominator: return q + 1
    return q if q % 2 == 0 else q + 1


def dense_grid_micro(points: int = DENSE_POINTS) -> Tuple[int, ...]:
    """`points` levels evenly spaced over the sweep in exact micro-units, round-half-even (M1's rule; declaration M5-1).
    The 24 pass-1 levels are among them when (points − 1) is a multiple of 23 (701 − 1 = 700 is not; declared)."""
    span = Fraction(C.F8_M_MAX_MICRO - C.F8_M_MIN_MICRO)
    return tuple(C.F8_M_MIN_MICRO + _rhe(Fraction(j) * span / (points - 1)) for j in range(points))


REFERENCE_ROLES = ("analysis_subset", "reference_of_record")


@dataclass(frozen=True)
class ReferenceStructure:
    role: str
    levels_micro: Tuple[int, ...]
    labels: Tuple[str, ...]
    structure_class: str
    verdict: str
    cause: Optional[str]
    rule: str
    bracket_micro: Optional[Tuple[int, int]]
    bottom_label: str
    top_label: str
    n_levels: int
    halts: Tuple[str, ...]
    threshold_identity: str                 # M3 law identity the labels were scored against
    declaration_sha256: str
    result_sha256: str = ""

    def identity(self) -> str:
        d = asdict(self); d.pop("result_sha256", None); return hashlib.sha256(_canon(d).encode()).hexdigest()


def _structure_class(v: V.Verdict, labels: Sequence[str], halts: Sequence[str]) -> str:
    if halts: return "REFERENCE-UNRESOLVED"
    s = STRUCTURE_FROM_RULE[v.rule]
    if isinstance(s, tuple): return s[0] if v.verdict == "NOT_PRODUCED" else s[1]
    return s


def classify_grid(levels: Sequence[int], role: str = "analysis_subset", halts: Sequence[str] = ()) -> ReferenceStructure:
    verify_frozen_identity()
    if role not in REFERENCE_ROLES: raise ClosureDomainError("unknown reference role")
    lv = tuple(int(x) for x in levels)
    if role == "reference_of_record" and (lv != dense_grid_micro() or halts):
        raise ClosureDomainError("reference_of_record requires the exact declared dense grid and zero halts")
    th = N.null_thresholds(F8_LEVELS_MICRO[0])              # the law is level-independent (M3)
    labels = tuple(projected_label(m, th)[0] for m in lv)
    v = V.evaluate(labels, lv)
    r = ReferenceStructure(role, lv, labels, _structure_class(v, labels, halts), v.verdict, v.cause, v.rule, v.bracket_micro,
                           labels[0], labels[-1], len(lv), tuple(halts), th.payload_identity(), CLOSURE_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(r, result_sha256=r.identity())


def dense_reference() -> ReferenceStructure:
    """THE canonical dense job: the reference structure of record (role issued only here)."""
    return classify_grid(dense_grid_micro(), "reference_of_record")


def validate_reference_structure(r: ReferenceStructure) -> None:
    """Validation by REPLAY of the labels and the verdict from the levels and role."""
    if type(r) is not ReferenceStructure: raise ClosureDomainError("not a ReferenceStructure")
    if r != classify_grid(r.levels_micro, r.role, r.halts): raise ClosureDomainError("reference structure does not replay to its recorded content")


# ----------------------------------------------------------------------------- reference stability (declaration M5-3)
STABILITY_ROLES = ("analysis_subset", "canonical")


@dataclass(frozen=True)
class StabilityAudit:
    role: str
    primary_sha256: str
    alternative_grids: Tuple[Tuple[int, str, bool], ...]      # (points, structure class, agrees with primary)
    fixed_point_max_abs_diff: float                           # Appendix A iteration vs independent bisection, over the 24 levels, both objects
    fixed_point_tol: float
    fixed_points_agree: bool
    all_alternatives_agree: bool
    declaration_sha256: str
    result_sha256: str = ""

    def identity(self) -> str:
        d = asdict(self); d.pop("result_sha256", None); return hashlib.sha256(_canon(d).encode()).hexdigest()


def stability_audit(primary: ReferenceStructure, role: str = "analysis_subset") -> StabilityAudit:
    verify_frozen_identity()
    if role not in STABILITY_ROLES: raise ClosureDomainError("unknown stability role")
    if role == "canonical" and primary.role != "reference_of_record": raise ClosureDomainError("a canonical stability audit requires the reference of record as primary")
    alts = []
    for pts in (351, 1401):
        r = classify_grid(dense_grid_micro(pts), "analysis_subset")
        alts.append((pts, r.structure_class, r.structure_class == primary.structure_class))
    diffs = []
    for u in F8_LEVELS_MICRO:
        m = level_m(u)
        diffs.append(abs(rho_re(m) - fixed_point_bisection(m, ETA0)))
        diffs.append(abs(rho_sk(m) - fixed_point_bisection(m, 0.0)))
    mx = float(max(diffs)); ok = mx <= STABILITY_FP_TOL
    s = StabilityAudit(role, primary.result_sha256, tuple(alts), mx, STABILITY_FP_TOL, ok, bool(ok and all(a[2] for a in alts)), CLOSURE_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(s, result_sha256=s.identity())


def validate_stability_audit(s: StabilityAudit, primary: ReferenceStructure) -> None:
    if type(s) is not StabilityAudit: raise ClosureDomainError("not a StabilityAudit")
    if s.primary_sha256 != primary.result_sha256: raise ClosureDomainError("stability audit does not name the primary")
    if s != stability_audit(primary, s.role): raise ClosureDomainError("stability audit does not replay")


# ----------------------------------------------------------------------------- §3.4 tolerance machinery from the calibration census
CALIBRATION_OBJECTS = ("realization", "skeleton_high")       # the two parts of job 0 (§7.3)


@dataclass(frozen=True)
class CalibrationRun:
    """One run of job 0, as M1 executed it: the spec reconstructed and validated (M1 D2), the object, the panel, the stream
    key, and the tail density. The census is built ONLY from these (L2 M5 r1 D2)."""
    level_micro: int
    seed: int
    obj: str
    spec_hash: str
    stream_key: Tuple[int, int, int]
    rho_tail_mean: float
    survival: bool
    rho_sha256: str                    # identity of the persisted density record (M1 `F8RunResult.rho_sha256`)


def calibration_run(result) -> CalibrationRun:
    """From an M1 `F8RunResult` produced on the CALIBRATION panel for one of the two job-0 objects: reconstruct the spec
    from the result's identity fields (production shape, calibration panel) and require the result's spec hash and
    stream key to be that spec's — a result from another panel, object, shape or stream is refused."""
    verify_frozen_identity()
    if result.obj not in CALIBRATION_OBJECTS: raise ClosureDomainError(f"job 0 runs only {CALIBRATION_OBJECTS}; got {result.obj!r}")
    try:
        spec = C.f8_run_spec(result.level_micro, result.seed, result.obj, panel="calibration")   # production shape; refuses non-calibration seeds and non-pass-1 levels
    except C.F8ConfigError as e:
        raise ClosureDomainError(f"not a job-0 run: {e}") from e
    if result.spec_hash != spec.spec_hash() or tuple(result.stream_key) != spec.stream_key:
        raise ClosureDomainError("result is not a production-shape calibration-panel run of the reconstructed spec")
    if len(result.rho) != C.F8_TICKS + 1: raise ClosureDomainError("result record length is not the production shape")
    return CalibrationRun(int(result.level_micro), int(result.seed), result.obj, result.spec_hash, tuple(result.stream_key), float(result.rho_tail_mean), bool(result.survival), result.rho_sha256())


@dataclass(frozen=True)
class CalibrationCensus:
    """Job 0 (§7.3): ŝ(m) and ŝ_sk(m) — the seed-to-seed standard deviation (ddof = 1) of the tail density at each level
    under the realization rule and under the skeleton rule from the high initialization (extinct runs contribute ρ̂ = 0),
    over the 20-seed CALIBRATION panel. Never scored, never reused. Carries the MDD ceilings and the stop-path verdict.
    PROVENANCE (L2 M5 r1 D2): built only from `CalibrationRun`s whose specs reconstruct on the calibration panel at the
    production shape; the census records every run's spec hash and density-record identity. ROLE: `canonical` is issued
    only by M7 when the runs were produced under the job-0 authorization; this module issues `derived_provisional`."""
    role: str
    levels_micro: Tuple[int, ...]
    calibration_panel_sha256: str
    calibration_master: int
    objects: Tuple[str, str]
    s_hat_re: Tuple[float, ...]
    s_hat_sk: Tuple[float, ...]
    mdd_re: Tuple[float, ...]              # k_R·ŝ·1.2533/√20 per level
    mdd_sk: Tuple[float, ...]
    max_mdd_re: float
    max_mdd_sk: float
    mdd_ceiling: float
    ceilings_met: bool                     # both maxima ≤ ceiling
    stop_path_triggered: bool              # not ceilings_met: the stage stops before any canonical census (§3.4)
    rho_hat_re: Tuple[Tuple[float, ...], ...]   # per level, in CALIBRATION PANEL ORDER
    rho_hat_sk: Tuple[Tuple[float, ...], ...]
    run_spec_hashes_re: Tuple[Tuple[str, ...], ...]
    run_spec_hashes_sk: Tuple[Tuple[str, ...], ...]
    run_rho_sha256_re: Tuple[Tuple[str, ...], ...]
    run_rho_sha256_sk: Tuple[Tuple[str, ...], ...]
    declaration_sha256: str
    result_sha256: str = ""

    def identity(self) -> str:
        d = asdict(self); d.pop("result_sha256", None); return hashlib.sha256(_canon(d).encode()).hexdigest()


CENSUS_ROLES = ("derived_provisional", "canonical")


def _sd(xs: Sequence[float]) -> float:
    a = np.asarray(xs, dtype=np.float64)
    return float(a.std(ddof=1))


def calibration_census(runs: Sequence[CalibrationRun], role: str = "derived_provisional") -> CalibrationCensus:
    """Build the census from exactly 24 levels × 20 calibration seeds × 2 objects of validated `CalibrationRun`s. Any other
    set — a missing or duplicated (level, seed, object), a seed off the calibration panel, a third object — is refused."""
    verify_frozen_identity()
    if role not in CENSUS_ROLES: raise ClosureDomainError("unknown census role")
    if role == "canonical": raise ClosureDomainError("the canonical census role is issued only by M7 under the job-0 authorization (M5 issues derived_provisional)")
    if any(type(r) is not CalibrationRun for r in runs): raise ClosureDomainError("census inputs must be CalibrationRun records")
    panel = tuple(C.F8_CALIBRATION_SEED_PANEL)
    want = {(u, sd, o) for u in F8_LEVELS_MICRO for sd in panel for o in CALIBRATION_OBJECTS}
    have = [(r.level_micro, r.seed, r.obj) for r in runs]
    if len(set(have)) != len(have): raise ClosureDomainError("duplicate (level, seed, object) in census inputs")
    if set(have) != want: raise ClosureDomainError(f"census inputs must be exactly 24 levels × 20 calibration seeds × 2 objects; got {len(have)}")
    for r in runs:
        try:
            spec = C.f8_run_spec(r.level_micro, r.seed, r.obj, panel="calibration")
        except C.F8ConfigError as e:
            raise ClosureDomainError(f"census run is not a job-0 run: {e}") from e
        if r.spec_hash != spec.spec_hash() or r.stream_key != spec.stream_key: raise ClosureDomainError("a census run's spec hash or stream key does not reconstruct")
        if not (0.0 <= r.rho_tail_mean <= 1.0): raise ClosureDomainError("tail densities must lie in [0, 1]")
    by = {(r.level_micro, r.seed, r.obj): r for r in runs}
    def rows(obj, field): return tuple(tuple(getattr(by[(u, sd, obj)], field) for sd in panel) for u in F8_LEVELS_MICRO)
    re_, sk = rows("realization", "rho_tail_mean"), rows("skeleton_high", "rho_tail_mean")
    s_re = tuple(_sd(r) for r in re_); s_sk = tuple(_sd(r) for r in sk)
    f = K_R * MEDIAN_SE_FACTOR / math.sqrt(PANEL_N)
    mdd_re = tuple(f * x for x in s_re); mdd_sk = tuple(f * x for x in s_sk)
    mx_re, mx_sk = max(mdd_re), max(mdd_sk)
    met = bool(mx_re <= MDD_CEILING and mx_sk <= MDD_CEILING)
    c = CalibrationCensus(role, tuple(F8_LEVELS_MICRO), C.F8_CALIBRATION_PANEL_SHA256_LITERAL, C.F8_CALIBRATION_MASTER, CALIBRATION_OBJECTS,
                          s_re, s_sk, mdd_re, mdd_sk, mx_re, mx_sk, MDD_CEILING, met, not met, re_, sk,
                          rows("realization", "spec_hash"), rows("skeleton_high", "spec_hash"), rows("realization", "rho_sha256"), rows("skeleton_high", "rho_sha256"), CLOSURE_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(c, result_sha256=c.identity())


def validate_calibration_census(c: CalibrationCensus, runs: Optional[Sequence[CalibrationRun]] = None) -> None:
    """Structural validation: role, panel, master, objects, declaration, identity; the arithmetic recomputed from the
    recorded rows; every recorded spec hash re-derived from (level, seed, object) on the calibration panel. With `runs`,
    full replay from the inputs."""
    if type(c) is not CalibrationCensus: raise ClosureDomainError("not a CalibrationCensus")
    if c.role not in CENSUS_ROLES or c.calibration_panel_sha256 != C.F8_CALIBRATION_PANEL_SHA256_LITERAL or c.calibration_master != C.F8_CALIBRATION_MASTER \
            or c.objects != CALIBRATION_OBJECTS or c.declaration_sha256 != CLOSURE_SHA256_LITERAL or c.levels_micro != tuple(F8_LEVELS_MICRO):
        raise ClosureDomainError("census provenance fields are not the frozen ones")
    if c.result_sha256 != c.identity(): raise ClosureDomainError("census identity does not match its content")
    panel = tuple(C.F8_CALIBRATION_SEED_PANEL)
    for obj, hashes in (("realization", c.run_spec_hashes_re), ("skeleton_high", c.run_spec_hashes_sk)):
        for li, u in enumerate(F8_LEVELS_MICRO):
            for si, sd in enumerate(panel):
                if hashes[li][si] != C.f8_run_spec(u, sd, obj, panel="calibration").spec_hash():
                    raise ClosureDomainError(f"recorded spec hash for ({obj}, {u}, {sd}) does not reconstruct on the calibration panel")
    f = K_R * MEDIAN_SE_FACTOR / math.sqrt(PANEL_N)
    if c.s_hat_re != tuple(_sd(r) for r in c.rho_hat_re) or c.s_hat_sk != tuple(_sd(r) for r in c.rho_hat_sk) \
            or c.mdd_re != tuple(f * x for x in c.s_hat_re) or c.mdd_sk != tuple(f * x for x in c.s_hat_sk) \
            or c.max_mdd_re != max(c.mdd_re) or c.max_mdd_sk != max(c.mdd_sk) or c.ceilings_met != (c.max_mdd_re <= MDD_CEILING and c.max_mdd_sk <= MDD_CEILING) or c.stop_path_triggered == c.ceilings_met:
        raise ClosureDomainError("census arithmetic does not recompute from its recorded rows")
    if runs is not None and c != calibration_census(runs, c.role): raise ClosureDomainError("census does not replay from the supplied runs")


# ----------------------------------------------------------------------------- the two F8 record kinds (D3): kept separate, mapping for the governance record
@dataclass(frozen=True)
class ToleranceEnsemble:
    """F8 reading of E1-R's `tolerance_ensembles` record kind (§7.3 item 4): ONE LEVEL's calibration ensemble — the 20
    calibration-panel runs of EACH job-0 object at that level, with ŝ and MDD for both. The mapping to the E1-R kind is a
    governance item for Mike's F8 governance record (declaration M5-5 as repaired), not an M5 decision."""
    level_micro: int
    level_id: str
    s_hat_re: float
    s_hat_sk: float
    mdd_re: float
    mdd_sk: float
    rho_hat_re: Tuple[float, ...]
    rho_hat_sk: Tuple[float, ...]
    run_spec_hashes_re: Tuple[str, ...]
    run_spec_hashes_sk: Tuple[str, ...]
    census_sha256: str


def tolerance_ensembles(c: CalibrationCensus) -> Tuple[ToleranceEnsemble, ...]:
    validate_calibration_census(c)
    return tuple(ToleranceEnsemble(u, level_id(u), c.s_hat_re[i], c.s_hat_sk[i], c.mdd_re[i], c.mdd_sk[i], c.rho_hat_re[i], c.rho_hat_sk[i],
                                   c.run_spec_hashes_re[i], c.run_spec_hashes_sk[i], c.result_sha256) for i, u in enumerate(F8_LEVELS_MICRO))


@dataclass(frozen=True)
class ToleranceProgram:
    """F8 reading of E1-R's `tolerance_program` record kind: the census COMPLETE over the full declared level set, both
    objects, with the MDD ceilings evaluated and the stop path stated. complete ⇔ every level's ensemble present (24/24)."""
    census_sha256: str
    levels_micro: Tuple[int, ...]
    ensemble_count: int
    complete: bool
    ceilings_met: bool
    stop_path_triggered: bool


def tolerance_program(c: CalibrationCensus) -> ToleranceProgram:
    ens = tolerance_ensembles(c)
    return ToleranceProgram(c.result_sha256, c.levels_micro, len(ens), len(ens) == len(F8_LEVELS_MICRO), c.ceilings_met, c.stop_path_triggered)


def evaluability_band(census: CalibrationCensus, obj: str, i_lo: int, i_hi: int) -> float:
    """k_R·√(ŝ_X(m₋)² + ŝ_X(m₊)²)·1.2533/√20 for adjacent pass-1 levels i_lo < i_hi, X the sweep's own object (§4.11)."""
    if i_hi != i_lo + 1 or not (0 <= i_lo < len(F8_LEVELS_MICRO) - 1): raise ClosureDomainError("evaluability band is defined for adjacent pass-1 levels")
    s = census.s_hat_sk if obj.startswith("skeleton") else census.s_hat_re if obj == "realization" else None
    if s is None: raise ClosureDomainError("object must be a skeleton sweep or the realization")
    return K_R * math.sqrt(s[i_lo] ** 2 + s[i_hi] ** 2) * MEDIAN_SE_FACTOR / math.sqrt(PANEL_N)


def fidelity_band(census: CalibrationCensus, i: int) -> float:
    """k_R·ŝ(m)·1.2533/√20 (realization part) at pass-1 level i (§3.4, §1.2′)."""
    return K_R * census.s_hat_re[i] * MEDIAN_SE_FACTOR / math.sqrt(PANEL_N)


# ----------------------------------------------------------------------------- finite-N projection sweeps and design stability (E1-R grammar)
HALT_CATEGORIES = ("evaluability:uncertified_threshold",)


@dataclass(frozen=True)
class ProjectionSweep:
    sweep_index: int
    master: int
    levels_micro: Tuple[int, ...]
    labels: Tuple[str, ...]
    verdict: str
    cause: Optional[str]
    rule: str
    structure_class: str
    halts: Tuple[str, ...]
    threshold_identity: str
    declaration_sha256: str
    result_sha256: str = ""

    def identity(self) -> str:
        d = asdict(self); d.pop("result_sha256", None); return hashlib.sha256(_canon(d).encode()).hexdigest()


def finite_n_counts(m: float, eta: float, g: np.random.Generator, n: int = N_CELLS, ticks: int = C.F8_TICKS, start_pi1: Optional[float] = None) -> np.ndarray:
    """The closure realized by N INDEPENDENT cells (no neighbourhood: each cell sees the global density): active count
    series, length ticks + 1, from a Binomial(n, π₁) start. Two binomial draws per tick."""
    q = Q_DEACT; glam = lambda_bar(m)
    pi1 = D.stationary_pi1(eta, MU) if start_pi1 is None else start_pi1
    k = int(g.binomial(n, pi1)); out = np.empty(ticks + 1, dtype=np.int64); out[0] = k
    for t in range(1, ticks + 1):
        rho = k / n
        p_act = 1.0 - math.exp(-(eta + glam * rho) * DT)
        survive = int(g.binomial(k, 1.0 - q)); born = int(g.binomial(n - k, p_act))
        k = survive + born; out[t] = k
    return out


def projection_sweep(sweep_index: int, master: int = PROJECTION_MASTER) -> ProjectionSweep:
    """One sweep: 24 levels × 20 seeds of the finite-N independent-cell closure (realization rule), each run scored by M2
    against M3's thresholds on the exact count grid, labelled 16/2/4, the sequence adjudicated by M4."""
    verify_frozen_identity()
    if isinstance(sweep_index, bool) or not isinstance(sweep_index, int) or sweep_index < 0: raise ClosureDomainError("sweep_index must be a non-negative integer")
    th = N.null_thresholds(F8_LEVELS_MICRO[0]); halts: List[str] = []; labels: List[str] = []
    for li, u in enumerate(F8_LEVELS_MICRO):
        statuses = []
        for s in range(PANEL_N):
            g = np.random.default_rng(np.random.SeedSequence([int(master), int(sweep_index), li, s]))
            counts = finite_n_counts(level_m(u), ETA0, g)
            rho = counts.astype(np.float64) / np.float64(N_CELLS)
            statuses.append(K.run_status(rho, th.theta_p, th.theta_t)[0])
        labels.append(K.level_label(K.level_counts(statuses)))
    v = V.evaluate(labels, F8_LEVELS_MICRO)
    sw = ProjectionSweep(int(sweep_index), int(master), tuple(F8_LEVELS_MICRO), tuple(labels), v.verdict, v.cause, v.rule, _structure_class(v, labels, halts), tuple(halts), th.payload_identity(), CLOSURE_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(sw, result_sha256=sw.identity())


def validate_projection_sweep_structure(s: ProjectionSweep, threshold_identity: Optional[str] = None) -> None:
    """Pure structural validator (L2 M5 r1 D1): exact type; the declared master; the frozen declaration; the threshold
    identity (M3's law the labels were scored against); identity == content; labels/levels on the frozen grid; the
    verdict and class recomputed from the labels. No replay (that is `validate_projection_sweep`)."""
    if type(s) is not ProjectionSweep: raise ClosureDomainError("not a ProjectionSweep")
    if s.master != PROJECTION_MASTER: raise ClosureDomainError(f"sweep master {s.master} is not the declared PROJECTION_MASTER")
    if s.declaration_sha256 != CLOSURE_SHA256_LITERAL: raise ClosureDomainError("sweep declaration identity is not the frozen one")
    if threshold_identity is not None and s.threshold_identity != threshold_identity: raise ClosureDomainError("sweep threshold identity differs from the reference's")
    if s.result_sha256 != s.identity(): raise ClosureDomainError("sweep identity does not match its content")
    if s.levels_micro != tuple(F8_LEVELS_MICRO) or len(s.labels) != len(F8_LEVELS_MICRO): raise ClosureDomainError("sweep levels are not the frozen pass-1 grid")
    if any(h not in HALT_CATEGORIES for h in s.halts): raise ClosureDomainError("unknown halt category")
    v = V.evaluate(s.labels, s.levels_micro)
    if (v.verdict, v.cause, v.rule) != (s.verdict, s.cause, s.rule) or s.structure_class != _structure_class(v, s.labels, s.halts):
        raise ClosureDomainError("sweep verdict/class do not recompute from its labels")


def validate_projection_sweep(s: ProjectionSweep) -> None:
    """Full replay."""
    validate_projection_sweep_structure(s)
    if s != projection_sweep(s.sweep_index, s.master): raise ClosureDomainError("projection sweep does not replay")


def clopper_pearson_lower(k: int, n: int, conf: float = 0.95) -> float:
    """Exact one-sided lower bound on a binomial proportion (bisection on the binomial CDF)."""
    if k <= 0: return 0.0
    if k >= n: return (1.0 - conf) ** (1.0 / n)                 # exact: the p with P(X = n | p) = 1 − conf
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        tail = sum(math.comb(n, j) * mid ** j * (1 - mid) ** (n - j) for j in range(k, n + 1))   # P(X ≥ k | p = mid)
        if tail < 1.0 - conf: lo = mid
        else: hi = mid
    return (lo + hi) / 2


@dataclass(frozen=True)
class DesignStability:
    role: str                              # "canonical" iff the exact declared ensemble with zero halts; else "analysis_subset"
    reference_sha256: str
    reference_class: str
    attempted: int
    scored: int
    halted: int
    matching: int
    match_rate_over_attempted: float
    cp_lower_95: float
    evaluable: bool                        # QUALIFICATION field: True iff role == canonical (reference of record, exactly the declared 200 indices, zero halts) — HALT_POLICY (L2 M5 r2 D1-R2)
    design_stable: Optional[bool]          # QUALIFICATION field: None unless evaluable; else every sweep's class equals the reference class
    subset_all_match: Optional[bool]       # DESCRIPTIVE: every attempted non-halted sweep matches (None if any halt) — never qualification
    sweep_sha256s: Tuple[str, ...]
    declaration_sha256: str
    result_sha256: str = ""

    def identity(self) -> str:
        d = asdict(self); d.pop("result_sha256", None); return hashlib.sha256(_canon(d).encode()).hexdigest()


def validate_sweep_set(ref: ReferenceStructure, sweeps: Sequence[ProjectionSweep], *, replay: bool = False) -> None:
    """The qualification gate for a design-stability ensemble (D1): the reference structurally valid (identity == content,
    frozen declaration; replayed when `replay`), every sweep structurally valid against the reference's threshold identity
    (replayed when `replay`), indices distinct. Canonical role additionally requires the reference of record and exactly the
    declared index set 0..199 — enforced in `design_stability`."""
    if type(ref) is not ReferenceStructure: raise ClosureDomainError("not a ReferenceStructure")
    if ref.result_sha256 != ref.identity() or ref.declaration_sha256 != CLOSURE_SHA256_LITERAL or ref.role not in REFERENCE_ROLES:
        raise ClosureDomainError("reference identity/declaration/role invalid")
    if replay: validate_reference_structure(ref)
    idx = [s.sweep_index for s in sweeps]
    if len(set(idx)) != len(idx): raise ClosureDomainError("duplicate sweep indices")
    for s in sweeps:
        validate_projection_sweep_structure(s, ref.threshold_identity)
        if replay: validate_projection_sweep(s)


def design_stability(ref: ReferenceStructure, sweeps: Sequence[ProjectionSweep], *, replay: bool = False) -> DesignStability:
    verify_frozen_identity()
    validate_sweep_set(ref, sweeps, replay=replay)
    if ref.role != "reference_of_record" and len(sweeps) >= DESIGN_STABILITY_SWEEPS: raise ClosureDomainError("a full ensemble must be judged against the reference of record")
    idx = [s.sweep_index for s in sweeps]
    halted = sum(1 for s in sweeps if s.halts); scored = len(sweeps) - halted
    matching = sum(1 for s in sweeps if not s.halts and s.structure_class == ref.structure_class)
    attempted = len(sweeps)
    canonical = attempted == DESIGN_STABILITY_SWEEPS and halted == 0 and ref.role == "reference_of_record" and sorted(idx) == list(range(DESIGN_STABILITY_SWEEPS))
    evaluable = bool(canonical)                                                        # qualification only for the complete canonical ensemble
    stable = (matching == attempted) if evaluable else None
    subset_all_match = (matching == attempted) if (halted == 0 and attempted > 0) else None
    d = DesignStability("canonical" if canonical else "analysis_subset", ref.result_sha256, ref.structure_class, attempted, scored, halted, matching,
                        matching / attempted if attempted else 0.0, clopper_pearson_lower(matching, attempted) if attempted else 0.0, evaluable, stable, subset_all_match,
                        tuple(s.result_sha256 for s in sweeps), CLOSURE_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(d, result_sha256=d.identity())


def validate_design_stability(d: DesignStability, ref: ReferenceStructure, sweeps: Sequence[ProjectionSweep], *, replay: bool = False) -> None:
    """Recompute from the (validated) reference and sweeps; `replay=True` (M7, before accepting a persisted canonical record)
    replays every sweep and the reference."""
    if type(d) is not DesignStability: raise ClosureDomainError("not a DesignStability")
    if d.result_sha256 != d.identity(): raise ClosureDomainError("design-stability identity does not match its content")
    if d.evaluable != (d.role == "canonical") or (d.design_stable is not None) != d.evaluable:
        raise ClosureDomainError("qualification fields are reserved for the canonical ensemble (D1-R2)")
    if d != design_stability(ref, sweeps, replay=replay): raise ClosureDomainError("design stability does not replay from its reference and sweeps")
