"""mfa_instrument/f9/t0.py — Flight 9 module M5, part 2: T0, the flat terrain (Contract F9 v0.7 §4.3, §5.8).

T0 IS NEVER SCORED BY §5.5. Its index is constant and has no contour. What is computed here is (a) the
reference object κ̂_c,T0 of §4.3 and (b) Flight 8's four tests rerun on T0 "as a scientific consistency
exercise" (§5.8). T0's record is PRODUCED, NOT PRODUCED or NOT DISTINGUISHED for T0 alone. It gates no
endpoint; an adverse or ND result there is not automatically a coding defect; it does not resolve onset
continuity; T0's measured value never retunes a scored tolerance. The apparatus check of §5.8 (i) is
M2's `reduction_check`; it is not repeated here.

INPUTS. Three sweeps on T0 under P, each over the 25 registered levels with 40 seeds: skeleton-high (all
cells active at t = 0), skeleton-low (ρ₀ = 0.02) and realization. Per level a sweep carries, in seed
order, each run's survival (active count > 0 at every tail tick, §5.4) and its tail active-count sum (an
integer; the run's tail density is that sum over 1,000 × 10,000). A level that is absent or None is a
missing record. And the calibration census's T0 panels (§8 step 4), as tail sums per level, for the
skeleton from the high initialization and for the realization. This module binds nothing to a run
record: that the numbers are the runs' is the runner's to establish.

ARITHMETIC. Every decision below is made on integers or exact rationals (Python int and Fraction). With
D = 1,000 × 10,000, a level's median density is (a + b)/(2D), a and b the 20th and 21st of the 40 sorted
tail sums; ŝ² is the exact sample variance of the 40 densities; the band is compared squared. No decision
passes through a float. The floats in the record are for reading and are computed from those exact values
by correctly rounded operations (integer and rational division, square root).

κ̂_c,T0 (§4.3) is §5.4's κ̂_c of the skeleton-high sweep, by M4's `persistence_record`, with its survival
counts and its absent and non-monotone cases. It is available when that record has a κ̂_c (both phases
observed, or the criterion met at every tested level, where it is unbracketed below) and unavailable
otherwise. A non-monotone profile's descriptive suffix statistic is not κ̂_c,T0.

THE FOUR TESTS (Contract F8 v0.8.4 §1.2 and §4.11, as the placed Flight 8 evaluator applies them, with
§5.8's redeclarations: the §2.9 grid, 40 seeds, 36 of 40, the bracket, the slope criterion, the band).
  T-S1′  a boundary exists. Skeleton-high. No level meets the criterion → FAIL `no active phase in
         sweep`. Every level meets it → FAIL `no inactive phase in sweep`. A level meets it and a higher
         one does not → ND `non-monotone survival`. Otherwise PASS, and the boundary is the first level of
         the terminal stretch; it then equals κ̂_c,T0. A missing level anywhere → ND, apparatus.
  T-S1c  continuity-compatible onset. Skeleton-high, over the levels at and above the boundary. In order:
         (1) a missing level in the domain → ND, apparatus; (2) a reversal med_{j+1} < med_j between
         adjacent levels larger than the band → ND `non-monotone at finite sample (<levels>)`, the lowest
         such pair; a reversal within the band is disregarded; (3) for an increase, J_j =
         0.10·(med_{j+1} − med_j)/(κ_{j+1} − κ_j); J_j > f_J × range → ND `continuity unresolved at grid
         resolution (<level j+1>)`, the lowest such pair. f_J = 0.25. The range is the median at the top
         level minus the median at the boundary. Steepness has no FAIL branch.
  T-S2   no hysteresis. In order: (1) a missing level in skeleton-low → ND, apparatus; (2) the bracket
         applies only if skeleton-high and skeleton-low each have a boundary (by the T-S1′ procedure)
         whose level and the level just below it are both in the fine grid (1.00 to 2.00) and 0.05 apart;
         otherwise ND `bracket outside fine grid`. A boundary at 1.00 does not qualify, and a complete
         low sweep with no boundary at all (no level meeting the criterion, every level meeting it, or a
         non-monotone profile) does not supply one; (3) PASS iff |κ̂_low − κ̂_c| ≤ 0.0754, else FAIL
         `hysteresis`. T-S2 has no other FAIL. Both sweeps' §5.4 records are kept in the T0 record
         whatever T-S2 returns.
  T-R1′  rounded continuation. Realization, the whole grid. A missing level → ND, apparatus. A level
         whose median is not positive → FAIL `realization extinct at <level>`, the lowest. Then clauses
         (2) and (3) of T-S1c over the whole grid, the range being the top level's median minus the
         lowest level's.
  If T-S1′ does not pass, T-S1c and T-S2 are ND `not evaluable: T-S1′ did not locate a boundary (<its
  cause>)`. T0's record is PRODUCED iff all four pass; NOT PRODUCED iff any FAILs (the first in the order
  above gives the cause); otherwise NOT DISTINGUISHED (the first ND gives the cause).
  THE BAND (§5.8). 3·√(ŝ_X(κ₋)² + ŝ_X(κ₊)²)·1.2533/√40, ŝ_X the seed-to-seed standard deviation of tail
  density in the calibration census at that level for the sweep's object. The band is consulted only
  where a reversal occurs. If the calibration panel lacks a level of any reversing pair in a test's
  domain, that test is ND, apparatus, before any reversal is judged.

READINGS THIS MODULE MAKES, each for Mike's ratification (the contract's sentence is given; nothing in
the contract is changed):
  1. ŝ_X uses the divisor 39, as Flight 8's census did (ddof = 1). §5.8 names the statistic and not the
     divisor.
  2. "The branch's sampled range" is the endpoint difference Contract F8 §4.11 states, med(top) −
     med(lowest level of the domain), not the largest median minus the smallest. The two agree on a
     monotone branch; the endpoint form is never the larger, so it never allows more.
  3. The skeleton continuity test keeps the reversal clause, as in Contract F8 §4.11. §5.8 says "keeps
     Flight 8's reversal rule" of the realization test only.
  4. T-S2 fails with `hysteresis` when the two boundaries differ by more than the bracket in EITHER
     direction, as the placed Flight 8 evaluator does. Contract F8 §4.11 states the pass condition with
     an absolute value and names the cause for κ̂_low above κ̂_c.
  5. RULED by Mike, 2026-11-18, on L2's M5 round-1 finding D1: §5.8's eligibility rule governs T-S2
     once T-S1′ has located the high boundary. A complete skeleton-low sweep that gives no boundary is
     "otherwise": ND `bracket outside fine grid`, not Flight 8's FAIL from the low sweep's phases. (Round
     1 of this module had Flight 8's outcome first; that was L1's reading and is withdrawn.)
  6. With every eligible boundary on the 0.05 grid, two eligible boundaries pass T-S2 exactly when they
     are the same level or neighbours. Any bracket from 0.05 to under 0.10 gives the same outcomes; the
     registered 0.0754 is the value used.
  7. The proxy of §5.8 (the high-initialization skeleton's ŝ for the low sweep) is declared and unused:
     no test compares medians of the low sweep.
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

from . import config as C
from . import outcomes as O
from .config import F9ConfigError

SWEEPS = ("skeleton_high", "skeleton_low", "realization")
CALIBRATION_OBJECTS = ("skeleton", "realization")
BAND_OBJECT = (("skeleton_high", "skeleton"), ("skeleton_low", "skeleton"), ("realization", "realization"))   # the low sweep's proxy (§5.8)
TESTS = ("T-S1′", "T-S1c", "T-S2", "T-R1′")
PASS, FAIL, ND = "PASS", "FAIL", "ND"
PRODUCED, NOT_PRODUCED, NOT_DISTINGUISHED = "PRODUCED", "NOT PRODUCED", "NOT DISTINGUISHED"

TAIL_DENOMINATOR = C.F9_TAIL_TICKS * C.F9_N_CELLS                # a run's tail density is its tail sum over this
BRACKET_MICRO = 75_400                                           # §5.8, A.4: max(0.0254, 0.0055) + 0.05; freeze record item 3
BRACKET_TERMS_MICRO = (25_400, 5_500, 50_000)                    # lower term, upper term, fine-grid spacing (A.4)
FINE_GRID_MICRO = (1_000_000, 2_000_000)                         # §2.9: 1.00 to 2.00 in steps of 0.05
FINE_SPACING_MICRO = 50_000
F_J = Fraction(1, 4)                                             # §5.8; freeze record item 3
J_INTERVAL = Fraction(1, 10)                                     # §5.8: J normalized to an interval of 0.10
K_R = 3                                                          # §5.8: the 3 of the band
MEDIAN_SE_FACTOR = Fraction(12533, 10000)                        # §5.8: 1.2533
S_HAT_DIVISOR = C.F9_N_SEEDS - 1                                 # reading 1

CAUSE_NO_ACTIVE = "no active phase in sweep"
CAUSE_NO_INACTIVE = "no inactive phase in sweep"
CAUSE_NON_MONOTONE_SURVIVAL = "non-monotone survival"
CAUSE_REVERSAL = "non-monotone at finite sample ({lo}, {hi})"
CAUSE_CONTINUITY = "continuity unresolved at grid resolution ({level})"
CAUSE_HYSTERESIS = "hysteresis"
CAUSE_BRACKET = "bracket outside fine grid"                      # §5.8
CAUSE_EXTINCT = "realization extinct at {level}"
CAUSE_NO_BOUNDARY = "not evaluable: T-S1′ did not locate a boundary ({cause})"
CAUSE_REFERENCE = "reference unavailable"                        # §5.8, §7

T0_DECLARATION = (
    ("module", "f9.t0"), ("version", C.F9_VERSION), ("contract", C.F9_CONTRACT_SHA256),
    ("sweeps", SWEEPS), ("calibration_objects", CALIBRATION_OBJECTS), ("band_object", BAND_OBJECT), ("tests", TESTS),
    ("outcomes", (PASS, FAIL, ND)), ("determinations", (PRODUCED, NOT_PRODUCED, NOT_DISTINGUISHED)),
    ("tail_denominator", TAIL_DENOMINATOR), ("survivors_min", C.F9_SURVIVAL_MIN), ("n_seeds", C.F9_N_SEEDS),
    ("bracket_micro", BRACKET_MICRO), ("bracket_terms_micro", BRACKET_TERMS_MICRO), ("fine_grid_micro", FINE_GRID_MICRO),
    ("fine_spacing_micro", FINE_SPACING_MICRO), ("f_j", "1/4"), ("j_interval", "1/10"), ("k_r", K_R), ("median_se_factor", "12533/10000"),
    ("s_hat_divisor", S_HAT_DIVISOR), ("median", "mean of the 20th and 21st of the 40 sorted tail sums"),
    ("causes", (CAUSE_NO_ACTIVE, CAUSE_NO_INACTIVE, CAUSE_NON_MONOTONE_SURVIVAL, CAUSE_REVERSAL, CAUSE_CONTINUITY, CAUSE_HYSTERESIS, CAUSE_BRACKET,
                CAUSE_EXTINCT, CAUSE_NO_BOUNDARY, CAUSE_REFERENCE, O.CAUSE_APPARATUS)),
    ("range", "median at the top level minus median at the lowest level of the domain"),
    ("order", "apparatus; (T-R1′: extinct;) lowest beyond-band reversal; lowest excess increase"),
    ("hysteresis", "missing low level: apparatus; else two eligible boundaries or ND bracket outside fine grid (a low sweep with no boundary supplies none); "
                   "then |difference| <= bracket, either direction"),
    ("reference", "kappa_c of the skeleton-high sweep by outcomes.persistence_record"),
    ("arithmetic", "decisions on integers and exact rationals; floats reported only"),
    ("kind", "scientific consistency exercise; gates nothing"),
)
T0_DECLARATION_SHA256_LITERAL = "0b5417a9050ee12ebf133f310a75e2c52cc32d269a0a246674cef469195a5a38"


class F9T0Error(F9ConfigError):
    """An input outside this module's domain, or a declaration that differs from its frozen digest."""


def verify_t0_declaration() -> str:
    C.verify_frozen_identity()
    O.verify_outcome_declaration()
    digest = C.frozen_digest(T0_DECLARATION)
    if digest != T0_DECLARATION_SHA256_LITERAL: raise F9T0Error("the T0 declaration differs from its frozen digest")
    if (BRACKET_MICRO, F_J, J_INTERVAL, K_R, MEDIAN_SE_FACTOR, C.F9_SURVIVAL_MIN, C.F9_N_SEEDS, TAIL_DENOMINATOR) != \
            (75_400, Fraction(1, 4), Fraction(1, 10), 3, Fraction(12533, 10000), 36, 40, 10_000_000):
        raise F9T0Error("T0 constants differ from the registered values (§5.8; freeze record items 1 and 3)")
    if BRACKET_MICRO != max(BRACKET_TERMS_MICRO[0], BRACKET_TERMS_MICRO[1]) + BRACKET_TERMS_MICRO[2]: raise F9T0Error("the bracket is not its stated sum")
    return digest


# ======================= inputs =======================
def _apparatus(key: str) -> str: return O.CAUSE_APPARATUS.format(key=key)


def _check_tail_sums(xs, what: str) -> Tuple[int, ...]:
    if not isinstance(xs, (list, tuple)) or len(xs) != C.F9_N_SEEDS or any(type(x) is not int or not (0 <= x <= TAIL_DENOMINATOR) for x in xs):
        raise F9T0Error(f"{what}: {C.F9_N_SEEDS} integer tail sums, each from 0 to {TAIL_DENOMINATOR}")
    return tuple(xs)


def check_sweep(sweep, name: str) -> Dict[int, Optional[Dict[str, tuple]]]:
    """A sweep is a mapping from a registered level to {"survival": 40 bools, "tail_sum": 40 ints}, or to None; an absent
    level is None. A surviving run has at least one active cell at each of the 1,000 tail ticks, and a run that did not
    survive has none at one of them at least; a level that contradicts that is refused."""
    if name not in SWEEPS: raise F9T0Error(f"not a T0 sweep: {name!r}")
    if not isinstance(sweep, dict): raise F9T0Error(f"{name}: a sweep is a mapping from a registered level to its observations")
    out: Dict[int, Optional[Dict[str, tuple]]] = {}
    for k, obs in sweep.items():
        if type(k) is not int or k not in C.F9_LEVELS_MICRO: raise F9T0Error(f"{name}: not a registered level: {k!r}")
        if obs is None: continue
        if not isinstance(obs, dict) or {(type(f), f) for f in obs} != {(str, "survival"), (str, "tail_sum")}:
            raise F9T0Error(f"{name} {k}: a level carries exactly `survival` and `tail_sum`")
        sv = obs["survival"]
        if not isinstance(sv, (list, tuple)) or len(sv) != C.F9_N_SEEDS or any(type(s) is not bool for s in sv):
            raise F9T0Error(f"{name} {k}: {C.F9_N_SEEDS} booleans of survival")
        ts = _check_tail_sums(obs["tail_sum"], f"{name} {k}")
        for s, t in zip(sv, ts):
            if s and t < C.F9_TAIL_TICKS: raise F9T0Error(f"{name} {k}: a surviving run has at least one active cell at every tail tick")
            if not s and t > (C.F9_TAIL_TICKS - 1) * C.F9_N_CELLS: raise F9T0Error(f"{name} {k}: a run that did not survive has an empty tail tick")
        out[k] = {"survival": tuple(sv), "tail_sum": ts}
    return {k: out.get(k) for k in C.F9_LEVELS_MICRO}


def check_calibration(calibration) -> Dict[str, Dict[int, Optional[Tuple[int, ...]]]]:
    """The calibration census's T0 panels: {"skeleton": {level: 40 tail sums or None}, "realization": {...}}; an absent
    level is None."""
    if not isinstance(calibration, dict) or {(type(k), k) for k in calibration} != {(str, o) for o in CALIBRATION_OBJECTS}:
        raise F9T0Error("the calibration panels are keyed by `skeleton` and `realization`")
    out = {}
    for obj in CALIBRATION_OBJECTS:
        panel = calibration[obj]
        if not isinstance(panel, dict): raise F9T0Error(f"calibration {obj}: a mapping from a registered level to 40 tail sums")
        got = {}
        for k, xs in panel.items():
            if type(k) is not int or k not in C.F9_LEVELS_MICRO: raise F9T0Error(f"calibration {obj}: not a registered level: {k!r}")
            if xs is not None: got[k] = _check_tail_sums(xs, f"calibration {obj} {k}")
        out[obj] = {k: got.get(k) for k in C.F9_LEVELS_MICRO}
    return out


# ======================= exact statistics =======================
def median_twice(tail_sums: Sequence[int]) -> int:
    """Twice the median of the 40 tail sums: the 20th plus the 21st in sorted order. The median density is this over
    2 × TAIL_DENOMINATOR."""
    xs = sorted(_check_tail_sums(tail_sums, "median"))
    h = C.F9_N_SEEDS // 2
    return xs[h - 1] + xs[h]


def s_hat_squared(tail_sums: Sequence[int]) -> Fraction:
    """ŝ², exactly: the variance (divisor 39) of the 40 tail densities."""
    xs = _check_tail_sums(tail_sums, "s_hat")
    n = C.F9_N_SEEDS
    return Fraction(n * sum(x * x for x in xs) - sum(xs) ** 2, n * S_HAT_DIVISOR * TAIL_DENOMINATOR ** 2)


def band_squared(s2_lo: Fraction, s2_hi: Fraction) -> Fraction:
    """The square of the §5.8 band: 9·(ŝ₋² + ŝ₊²)·1.2533²/40."""
    return K_R * K_R * (s2_lo + s2_hi) * MEDIAN_SE_FACTOR * MEDIAN_SE_FACTOR / C.F9_N_SEEDS


def _density(twice: int) -> float: return twice / (2 * TAIL_DENOMINATOR)
def _root(x: Fraction) -> float: return math.sqrt(x) if x > 0 else 0.0


# ======================= the tests =======================
def _result(test: str, outcome: str, cause: Optional[str], **detail) -> Dict[str, object]:
    return {"test": test, "outcome": outcome, "cause": cause, "detail": detail}


def _boundary(sweep: Dict[int, Optional[dict]], test: str):
    """The T-S1′ procedure on a skeleton sweep: (index of the boundary or None, the result if no boundary, the §5.4 record)."""
    grid = C.F9_LEVELS_MICRO
    survivors = {k: (None if sweep[k] is None else sum(sweep[k]["survival"])) for k in grid}
    rec = O.persistence_record(survivors)
    missing = [k for k in grid if sweep[k] is None]
    if missing:
        return None, _result(test, ND, _apparatus("missing level record"), missing_levels=missing), rec
    counts = [survivors[k] for k in grid]
    profile = rec["profile"]
    if profile == O.PROFILE_NONE: return None, _result(test, FAIL, CAUSE_NO_ACTIVE, survivors=counts), rec
    if profile == O.PROFILE_ALL: return None, _result(test, FAIL, CAUSE_NO_INACTIVE, survivors=counts), rec
    if profile == O.PROFILE_NON_MONOTONE: return None, _result(test, ND, CAUSE_NON_MONOTONE_SURVIVAL, survivors=counts), rec
    if profile != O.PROFILE_BOTH: raise F9T0Error("an unknown persistence profile")
    return grid.index(rec["kappa_c_micro"]), None, rec


def _eligible(index: int) -> bool:
    """§5.8: the level just below the boundary and the boundary level are both in the fine grid and 0.05 apart."""
    grid = C.F9_LEVELS_MICRO
    if index < 1: return False
    below, at = grid[index - 1], grid[index]
    lo, hi = FINE_GRID_MICRO
    return lo <= below <= hi and lo <= at <= hi and at - below == FINE_SPACING_MICRO


def _monotone_and_continuity(test: str, sweep, panel, start: int) -> Optional[Dict[str, object]]:
    """Clauses (1) to (3) of T-S1c over the levels from `start` to the top. None when all pass."""
    grid = C.F9_LEVELS_MICRO
    dom = grid[start:]
    missing = [k for k in dom if sweep[k] is None]
    if missing: return _result(test, ND, _apparatus("missing level record"), missing_levels=missing)
    med = {k: median_twice(sweep[k]["tail_sum"]) for k in dom}
    pairs = list(zip(dom[:-1], dom[1:]))
    reversals = [(a, b) for a, b in pairs if med[b] < med[a]]
    need = sorted({k for pr in reversals for k in pr})
    cal_missing = [k for k in need if panel[k] is None]
    if cal_missing: return _result(test, ND, _apparatus("missing calibration level record"), missing_levels=cal_missing)
    for a, b in reversals:
        band2 = band_squared(s_hat_squared(panel[a]), s_hat_squared(panel[b]))
        rev = Fraction(med[a] - med[b], 2 * TAIL_DENOMINATOR)
        if rev * rev > band2:
            return _result(test, ND, CAUSE_REVERSAL.format(lo=C.level_id(a), hi=C.level_id(b)), levels_micro=[a, b], reversal=float(rev), band=_root(band2))
    rng = med[dom[-1]] - med[dom[0]]                                   # twice the range, in tail-sum units
    for a, b in pairs:
        inc = med[b] - med[a]
        # J > f_J·range with J = (1/10)·(inc/2D)/((b − a)/10⁶) and range = rng/2D, on integers. Every increase is compared,
        # whatever the sign of the range: with a zero or negative range any increase is an excess (Flight 8, M-P1 r1 D2).
        if inc > 0 and J_INTERVAL * inc * C.MICRO_UNITS > F_J * rng * (b - a):
            j = float(J_INTERVAL * Fraction(inc, 2 * TAIL_DENOMINATOR) / Fraction(b - a, C.MICRO_UNITS))
            return _result(test, ND, CAUSE_CONTINUITY.format(level=C.level_id(b)), levels_micro=[a, b], J=j, f_J_times_range=float(F_J * Fraction(rng, 2 * TAIL_DENOMINATOR)))
    return None


def _reference(rec: Dict[str, object]) -> Dict[str, object]:
    """κ̂_c,T0 from the skeleton-high sweep's §5.4 record: available when that record has a κ̂_c."""
    k_c = rec["kappa_c_micro"]
    return {"available": k_c is not None, "kappa_c_t0_micro": k_c, "bracket_micro": rec["bracket_micro"], "profile": rec["profile"],
            "cause": None if k_c is not None else CAUSE_REFERENCE, "reference_cause": None if k_c is not None else (rec.get("kappa_c_cause") or rec["cause"])}


def evaluate_t0(skeleton_high, skeleton_low, realization, calibration) -> Dict[str, object]:
    """The T0 record of §5.8 and the reference object of §4.3, from the three sweeps and the calibration panels."""
    verify_t0_declaration()
    grid = C.F9_LEVELS_MICRO
    hi, lo, re = check_sweep(skeleton_high, "skeleton_high"), check_sweep(skeleton_low, "skeleton_low"), check_sweep(realization, "realization")
    cal = check_calibration(calibration)

    c, r1, rec_hi = _boundary(hi, "T-S1′")
    lo_c, lo_res, rec_lo = _boundary(lo, "T-S2")
    if c is None:
        r2 = _result("T-S1c", ND, CAUSE_NO_BOUNDARY.format(cause=r1["cause"]))
        r3 = _result("T-S2", ND, CAUSE_NO_BOUNDARY.format(cause=r1["cause"]))
    else:
        r1 = _result("T-S1′", PASS, None, boundary_micro=grid[c], survivors=[sum(hi[k]["survival"]) for k in grid])
        r2 = _monotone_and_continuity("T-S1c", hi, cal["skeleton"], c) or _result("T-S1c", PASS, None, domain_micro=list(grid[c:]))
        low_missing = [k for k in grid if lo[k] is None]
        if low_missing:
            r3 = _result("T-S2", ND, _apparatus("missing level record"), missing_levels=low_missing, source="skeleton-low")
        else:
            d = {"boundary_micro": grid[c], "low_boundary_micro": None if lo_c is None else grid[lo_c], "low_profile": rec_lo["profile"],
                 "separation_micro": None if lo_c is None else abs(grid[lo_c] - grid[c]), "bracket_micro": BRACKET_MICRO,
                 "eligible": {"boundary": _eligible(c), "low_boundary": lo_c is not None and _eligible(lo_c)}}
            if not (d["eligible"]["boundary"] and d["eligible"]["low_boundary"]): r3 = _result("T-S2", ND, CAUSE_BRACKET, **d)
            elif d["separation_micro"] <= BRACKET_MICRO: r3 = _result("T-S2", PASS, None, **d)
            else: r3 = _result("T-S2", FAIL, CAUSE_HYSTERESIS, **d)

    missing = [k for k in grid if re[k] is None]
    if missing:
        r4 = _result("T-R1′", ND, _apparatus("missing level record"), missing_levels=missing)
    else:
        extinct = [k for k in grid if not median_twice(re[k]["tail_sum"]) > 0]
        if extinct: r4 = _result("T-R1′", FAIL, CAUSE_EXTINCT.format(level=C.level_id(extinct[0])), levels_micro=extinct)
        else: r4 = _monotone_and_continuity("T-R1′", re, cal["realization"], 0) or _result("T-R1′", PASS, None, domain_micro=list(grid))

    tests = [r1, r2, r3, r4]
    fails = [t for t in tests if t["outcome"] == FAIL]
    nds = [t for t in tests if t["outcome"] == ND]
    if fails: determination, cause = NOT_PRODUCED, fails[0]["cause"]
    elif nds: determination, cause = NOT_DISTINGUISHED, nds[0]["cause"]
    else: determination, cause = PRODUCED, None

    def medians(sweep): return {k: (None if sweep[k] is None else _density(median_twice(sweep[k]["tail_sum"]))) for k in grid}
    def s_hats(panel): return {k: (None if panel[k] is None else _root(s_hat_squared(panel[k]))) for k in grid}
    return {"record": "F9T0Record", "kind": "scientific consistency exercise; gates no endpoint", "terrain": "T0", "composition": "P",
            "determination": determination, "cause": cause, "tests": tests, "reference": _reference(rec_hi),
            "persistence": {"skeleton_high": rec_hi, "skeleton_low": rec_lo},
            "medians": {"skeleton_high": medians(hi), "skeleton_low": medians(lo), "realization": medians(re)},
            "s_hat": {"skeleton": s_hats(cal["skeleton"]), "realization": s_hats(cal["realization"])},
            "constants": {"survivors_min": C.F9_SURVIVAL_MIN, "n_seeds": C.F9_N_SEEDS, "bracket_micro": BRACKET_MICRO, "f_J": float(F_J),
                          "J_interval": float(J_INTERVAL), "k_R": K_R, "median_se_factor": float(MEDIAN_SE_FACTOR), "s_hat_divisor": S_HAT_DIVISOR},
            "note": "for T0 alone; an adverse or ND result is not automatically a coding defect; onset continuity is not resolved",
            "declaration_sha256": T0_DECLARATION_SHA256_LITERAL}


def reference_from_sweep(skeleton_high) -> Dict[str, object]:
    """κ̂_c,T0 alone (§4.3), from the skeleton-high sweep: the §5.4 record and whether a reference exists."""
    verify_t0_declaration()
    hi = check_sweep(skeleton_high, "skeleton_high")
    rec = O.persistence_record({k: (None if hi[k] is None else sum(hi[k]["survival"])) for k in C.F9_LEVELS_MICRO})
    return dict(_reference(rec), persistence=rec)
