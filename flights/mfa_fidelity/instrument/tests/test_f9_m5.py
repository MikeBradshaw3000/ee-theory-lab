"""tests/test_f9_m5.py — Flight 9 module M5: the comparators of contract §4 (`f9/closure.py`) and T0's reference object
and four tests of §4.3 and §5.8 (`f9/t0.py`).

No lattice run is made and no run record is read. The closure is iterated on constructed indices and on the contract's
own terrain arrays; every sweep given to the T0 tests is built here from chosen survival counts and tail sums. Each
rule is checked against a second implementation written in the test from the contract's sentences, on named cases with
stated answers and on many random sweeps."""
import copy
import hashlib
import math
import os
import statistics
from fractions import Fraction

import numpy as np
import pytest

from mfa_instrument.f9 import closure as CL
from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import dynamics as D
from mfa_instrument.f9 import identities as I
from mfa_instrument.f9 import outcomes as O
from mfa_instrument.f9 import spectral as S
from mfa_instrument.f9 import t0 as Z
from mfa_instrument.f9 import terrain as T

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "mfa_instrument")
GRID = C.F9_LEVELS_MICRO
DEN = Z.TAIL_DENOMINATOR
Q = C.q_deact()
RNG = lambda *k: np.random.Generator(np.random.PCG64(np.random.SeedSequence([5, 5, 5] + list(k))))


def _refused(fn, *a, **k):
    try: fn(*a, **k)
    except (C.F9ConfigError, O.F9OutcomeError): return True
    return False


# ======================= closure: declaration and map =======================
def test_closure_declaration_and_registered_solver_values():
    assert CL.verify_closure_declaration() == CL.CLOSURE_DECLARATION_SHA256_LITERAL == C.frozen_digest(CL.CLOSURE_DECLARATION)
    assert (CL.SOLVER_TOL, CL.SOLVER_MAX_ITER) == (1e-12, 200000)                      # §4.2; freeze record item 15
    assert CL.start_value("skeleton") == 1.0 and CL.start_value("realization") == D.stationary_pi1(C.F9_ETA0)
    a = 0.01
    assert abs(CL.start_value("realization") - a / (a + Q)) < 1e-15 and round(CL.start_value("realization"), 6) == 0.052282      # A.3
    assert (CL.CAUSE_UNAVAILABLE, CL.CAUSE_REFERENCE) == ("comparator unavailable", "reference unavailable")                     # §7
    assert _refused(CL.start_value, "skeleton_low")
    assert issubclass(CL.F9ClosureError, C.F9ConfigError)


def _step_by_loops(p, eta, g, lam):
    """§4.2's map written cell by cell with explicit periodic neighbours."""
    n0, n1 = p.shape
    out = np.empty_like(p)
    for i in range(n0):
        for j in range(n1):
            s = 0.0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di or dj: s += p[(i + di) % n0, (j + dj) % n1]
            out[i, j] = (1.0 - p[i, j]) * (1.0 - math.exp(-C.F9_DT * (eta + g * lam[i, j] * s / 8.0))) + (1.0 - Q) * p[i, j]
    return out


def test_the_map_is_the_contracts_formula():
    rng = RNG(1)
    for shape in ((3, 3), (5, 7), (12, 12)):
        for eta in (0.0, C.F9_ETA0):
            lam = rng.uniform(0.0, 1.0, shape); p = rng.uniform(0.0, 1.0, shape); g = float(rng.uniform(0.0, 3.0))
            got = CL.closure_step(p, eta_floor=eta, g=g, lam=lam)
            assert np.max(np.abs(got - _step_by_loops(p, eta, g, lam))) < 1e-15
    lam = rng.uniform(0.1, 1.0, (6, 6))
    assert np.max(np.abs(CL.closure_step(np.zeros((6, 6)), eta_floor=0.0, g=1.7, lam=lam))) == 0.0        # p = 0 is fixed without a floor
    one = CL.closure_step(np.zeros((6, 6)), eta_floor=C.F9_ETA0, g=1.7, lam=lam)
    assert np.allclose(one, 0.01, rtol=0, atol=1e-15)                                                      # with the floor, 0 moves to the floor probability


def _flat_root(eta, gl):
    """The positive root of (1 − p)(1 − exp(−(η + gλ·p))) = q·p by bisection."""
    f = lambda p: (1.0 - p) * (1.0 - math.exp(-(eta + gl * p))) - Q * p
    lo, hi = 1e-9, 1.0
    assert f(lo) > 0 > f(hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


def test_flat_index_fixed_points_against_the_scalar_equation():
    lam = np.full((6, 6), 0.512)
    for kappa in (1.05, 1.2, 1.5, 2.0, 3.0):
        r = CL.iterate(lam, kappa * Q / 0.512, 0.0, 1.0)
        assert r["converged"] and r["last_change"] <= 1e-12 and r["map"].shape == (6, 6)
        assert float(np.ptp(r["map"])) == 0.0 and abs(r["map"][0, 0] - _flat_root(0.0, kappa * Q)) < 1e-9
    for kappa in (0.0, 0.75, 1.0, 1.5, 3.0):
        r = CL.iterate(lam, kappa * Q / 0.512, C.F9_ETA0, CL.start_value("realization"))
        assert r["converged"] and abs(r["map"][0, 0] - _flat_root(C.F9_ETA0, kappa * Q)) < 1e-9
    r = CL.iterate(lam, 0.0, C.F9_ETA0, CL.start_value("realization"))                 # no feedback: the start is the fixed point
    assert r["iterations"] == 1 and abs(r["map"][0, 0] - CL.start_value("realization")) < 1e-15


def test_skeleton_below_the_crossing_converges_to_a_small_positive_map_not_zero():
    r = CL.iterate(np.full((6, 6), 0.512), 0.75 * Q / 0.512, 0.0, 1.0)
    assert r["converged"] and 0.0 < float(r["map"].max()) < 1e-10                     # the fixed point is 0; the rule stops on the change


def test_nonconvergence_is_comparator_unavailable_with_no_map():
    """At κ = 1 exactly the zero-floor map on a flat index decays like 1/k: after 200,000 applications the change is still
    above 1e-12, so the registered solver reports the comparator unavailable (§4.2)."""
    r = CL.iterate(np.full((4, 4), 0.512), Q / 0.512, 0.0, 1.0)
    assert r["converged"] is False and r["iterations"] == 200000 and r["map"] is None and r["last_change"] > 1e-12
    assert 1e-11 < r["last_change"] < 1e-9


def _moore_matrix(shape):
    n0, n1 = shape; n = n0 * n1
    A = np.zeros((n, n))
    for i in range(n0):
        for j in range(n1):
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di or dj: A[i * n1 + j, ((i + di) % n0) * n1 + (j + dj) % n1] += 1.0
    return A


def test_the_crossing_is_where_the_zero_floor_map_loses_stability_at_zero():
    """§4.1: with g = κ·g_spec, the linearization of the zero-floor map at p = 0, (1 − q)·I + g·diag(λ)·A/8, has spectral
    radius 1 at κ = 1; below it the closure returns to zero and above it it does not."""
    rng = RNG(2)
    lam = rng.uniform(0.2, 1.0, (8, 8))
    gs = S.g_spec(lam)
    A = _moore_matrix(lam.shape)
    for kappa, side in ((0.9, -1), (1.0, 0), (1.1, 1)):
        M = (1.0 - Q) * np.eye(64) + kappa * gs * np.diag(lam.ravel()) @ A / 8.0
        rho = float(np.max(np.abs(np.linalg.eigvals(M))))
        assert (abs(rho - 1.0) < 1e-9) if side == 0 else ((rho - 1.0) * side > 1e-3)
    below = CL.iterate(lam, 0.9 * gs, 0.0, 1.0); above = CL.iterate(lam, 1.2 * gs, 0.0, 1.0)
    assert below["converged"] and float(below["map"].max()) < 1e-9
    assert above["converged"] and float(above["map"].min()) > 1e-3
    assert np.max(np.abs(_step_by_loops(above["map"], 0.0, 1.2 * gs, lam) - above["map"])) < 2e-12      # a fixed point of the written map


def test_closure_inputs_are_checked():
    lam = np.full((4, 4), 0.5)
    good = (lam, 0.3, 0.0, 1.0)
    CL.iterate(*good)
    for bad in ((lam.astype(np.float32),) + good[1:], (np.full((2, 4), 0.5),) + good[1:], (np.full(16, 0.5),) + good[1:], (-lam,) + good[1:],
                (np.full((4, 4), np.nan),) + good[1:], (lam, -0.1, 0.0, 1.0), (lam, 1, 0.0, 1.0), (lam, float("inf"), 0.0, 1.0), (lam, 0.3, -1e-9, 1.0),
                (lam, 0.3, 0.0, 1.5), (lam, 0.3, 0.0, True), (lam, 0.3, None, 1.0)):
        assert _refused(CL.iterate, *bad)


# ======================= closure on the contract's arms =======================
@pytest.fixture(scope="module")
def arms(tmp_path_factory):
    d = str(tmp_path_factory.mktemp("f9_identities_m5"))
    I.write_bundle(d)
    rec, arr = I.load_bundle(d)
    return {a: D.arm_context(rec, arr, *a) for a in (("T0", "P"), ("TA", "P"), ("TB", "H"))}


def test_site_closure_records_on_contract_arms(arms):
    t0 = arms[("T0", "P")]
    for obj, level in (("skeleton", 1500000), ("realization", 1500000), ("realization", 750000), ("skeleton", 750000)):
        out = CL.site_closure(t0, level, obj)
        rec, p = out["record"], out["map"]
        assert rec["available"] is True and rec["cause"] is None and rec["iterations"] < 1000 and rec["last_change"] <= 1e-12
        assert (rec["terrain"], rec["composition"], rec["object"], rec["level_micro"]) == ("T0", "P", obj, level)
        assert rec["g"] == S.gain(level, t0.g_spec) and rec["g_spec"] == t0.g_spec and rec["index_sha256"] == t0.index_sha256
        assert rec["eta_floor"] == (C.F9_ETA0 if obj == "realization" else 0.0) and rec["start"] == CL.start_value(obj)
        assert rec["solver"] == {"tol": 1e-12, "max_iter": 200000} and rec["declaration_sha256"] == CL.CLOSURE_DECLARATION_SHA256_LITERAL
        assert p.shape == (100, 100) and p.dtype == np.float64 and rec["map_min"] == float(p.min()) and rec["map_max"] == float(p.max())
        if (obj, level) != ("skeleton", 750000):
            assert abs(float(p.mean()) - _flat_root(rec["eta_floor"], (level / 1e6) * Q)) < 1e-9        # T0 is flat: the scalar equation
        else:
            assert 0.0 < rec["map_max"] < 1e-10
    for arm in (arms[("TA", "P")], arms[("TB", "H")]):
        for obj in CL.CLOSURE_OBJECTS:
            out = CL.site_closure(arm, 2000000, obj)
            rec, p = out["record"], out["map"]
            assert rec["available"] and float(p.min()) >= 0.0 and float(p.max()) < 1.0 and float(np.ptp(p)) > 0.01          # a map with structure
            eta = rec["eta_floor"]
            assert np.max(np.abs(CL.closure_step(p, eta_floor=eta, g=rec["g"], lam=arm.lam) - p)) <= 1e-12                   # one more application moves it no further
            assert rec["map_sha256"] == hashlib.sha256(T.serialize(p)).hexdigest()
    assert _refused(CL.site_closure, t0, 1025000, "skeleton") and _refused(CL.site_closure, t0, 1500000, "skeleton_low")
    assert _refused(CL.site_closure, None, 1500000, "skeleton") and _refused(CL.site_closure, t0, 1.5, "skeleton")


def test_skeleton_closure_at_the_crossing_is_unavailable_on_t0(arms):
    """The registered solver on a contract arm: T0's skeleton at κ = 1.00 does not reach 1e-12 in 200,000 applications. The
    record says `comparator unavailable` and carries no map (§4.2, §7). About a minute."""
    out = CL.site_closure(arms[("T0", "P")], 1000000, "skeleton")
    rec = out["record"]
    assert out["map"] is None and rec["available"] is False and rec["cause"] == "comparator unavailable" and rec["iterations"] == 200000
    assert rec["last_change"] > 1e-12 and rec["map_sha256"] is None and rec["map_mean"] is None


# ======================= closure: the threshold against the crossing and against T0 =======================
def _counts(first_met=None, pattern=None):
    """Survivor counts: 40 from index `first_met` up and 0 below, or by a pattern string of '1' (40) and '0' (0)."""
    if pattern is None: pattern = "0" * first_met + "1" * (25 - first_met)
    return {k: (40 if ch == "1" else 0) for k, ch in zip(GRID, pattern)}


def test_threshold_fidelity_cases():
    gs, gs0 = 0.5, 0.354
    f = CL.threshold_fidelity("TA", "P", _counts(7), gs, _counts(5), gs0)
    x, t = f["against_crossing"], f["against_t0"]
    assert GRID[7] == 1300000 and GRID[5] == 1200000
    assert x["available"] and x["kappa_c_micro"] == 1300000 and x["normalized_shift_micro"] == 300000 and x["bracket_lower_micro"] == 1250000
    assert x["bracket_lower_normalized_shift_micro"] == 250000 and x["g_at_kappa_c"] == S.gain(1300000, gs) and abs(x["raw_g_shift"] - 0.3 * gs) < 1e-15
    assert abs(x["bracket_lower_raw_g_shift"] - 0.25 * gs) < 1e-15 and x["bracketed"] is True
    assert t["available"] and t["difference_micro"] == 100000 and t["reference_kappa_c_micro"] == 1200000
    assert t["g_at_kappa_c"] == S.gain(1300000, gs) and t["reference_g_at_kappa_c"] == S.gain(1200000, gs0)
    assert f["persistence"] == O.persistence_record(_counts(7)) and f["t0_persistence"] == O.persistence_record(_counts(5)) and f["crossing_micro"] == 1000000
    # a threshold below the crossing is a negative shift, recorded as such
    assert CL.threshold_fidelity("TA", "P", _counts(1), gs)["against_crossing"]["normalized_shift_micro"] == 0
    # every level meets the criterion: κ̂_c is the lowest level, unbracketed, and usable
    f = CL.threshold_fidelity("TC", "H", _counts(0), gs, _counts(0), gs0)
    assert f["against_crossing"]["kappa_c_micro"] == 750000 and f["against_crossing"]["normalized_shift_micro"] == -250000
    assert f["against_crossing"]["bracketed"] is False and f["against_crossing"]["bracket_lower_raw_g_shift"] is None
    assert f["against_t0"]["available"] and f["against_t0"]["difference_micro"] == 0 and f["against_t0"]["reference_bracketed"] is False
    # the arm has no κ̂_c: its own cause, twice
    for pat, cause in (("0" * 25, "criterion met at no tested level"), ("0" * 5 + "1" + "0" + "1" * 18, "non-monotone criterion profile: no crossing is claimed")):
        f = CL.threshold_fidelity("TA", "H", _counts(pattern=pat), gs, _counts(5), gs0)
        assert f["against_crossing"] == {"available": False, "cause": cause, "profile": O.persistence_record(_counts(pattern=pat))["profile"]}
        assert f["against_t0"]["available"] is False and f["against_t0"]["cause"] == cause and f["against_t0"]["reference_kappa_c_micro"] == 1200000
    # T0 has no κ̂_c, or was not supplied, or lacks a level: `reference unavailable`, whatever the arm shows
    nm = "0" * 5 + "1" + "0" + "1" * 18
    assert O.persistence_record(_counts(pattern=nm))["descriptive_suffix_micro"] == GRID[7]                 # the suffix statistic exists and is not used
    missing = dict(_counts(5)); missing[GRID[3]] = None
    for ref in (_counts(pattern="0" * 25), _counts(pattern=nm), missing, None):
        f = CL.threshold_fidelity("TA", "P", _counts(7), gs, ref, None if ref is None else gs0)
        assert f["against_crossing"]["available"] and f["against_t0"]["available"] is False and f["against_t0"]["cause"] == "reference unavailable"
        assert "difference_micro" not in f["against_t0"]
    # T0 against itself
    f = CL.threshold_fidelity("T0", "P", _counts(5), gs0, _counts(5), gs0)
    assert f["against_t0"]["difference_micro"] == 0
    for bad in (("T0", "H", _counts(5), gs), ("TA", "P", _counts(5), 0.0), ("TA", "P", _counts(5), 1), ("TA", "P", _counts(5), gs, _counts(5), None),
                ("TA", "P", _counts(5), gs, None, gs0), ("TA", "P", {1025000: 3}, gs), ("TA", "P", _counts(5), gs, _counts(5), float("nan"))):
        assert _refused(CL.threshold_fidelity, *bad)


# ======================= T0: declaration and constants =======================
def test_t0_declaration_and_registered_values():
    assert Z.verify_t0_declaration() == Z.T0_DECLARATION_SHA256_LITERAL == C.frozen_digest(Z.T0_DECLARATION)
    assert (Z.BRACKET_MICRO, Z.F_J, Z.J_INTERVAL, Z.K_R, Z.MEDIAN_SE_FACTOR) == (75400, Fraction(1, 4), Fraction(1, 10), 3, Fraction(12533, 10000))
    assert Z.TAIL_DENOMINATOR == 1000 * 10000 and Z.S_HAT_DIVISOR == 39 and C.F9_SURVIVAL_MIN == 36 and C.F9_N_SEEDS == 40
    assert Z.CAUSE_BRACKET == "bracket outside fine grid" and Z.CAUSE_REFERENCE == "reference unavailable"       # §5.8
    assert Z.TESTS == ("T-S1′", "T-S1c", "T-S2", "T-R1′") and issubclass(Z.F9T0Error, C.F9ConfigError)


def test_the_bracket_is_appendix_a4s_arithmetic():
    """A.4: lower term ln N/(q·2,000); upper term the least κ − 1 with N·ρ*_sk ≥ 50 on the homogeneous map; plus the 0.05
    spacing. Recomputed here; the registered 0.0754 is the value the module uses."""
    lower = math.log(C.F9_N_CELLS) / (Q * (C.F9_TICKS - C.F9_TAIL_TICKS))
    assert round(lower, 4) == 0.0254
    target = 50 / C.F9_N_CELLS
    lo, hi = 1.0, 1.1
    for _ in range(100):                                             # bisection on κ for ρ*_sk(κ) = 50/N
        mid = 0.5 * (lo + hi)
        if _flat_root(0.0, mid * Q) < target: lo = mid
        else: hi = mid
    upper = hi - 1.0
    assert round(upper, 4) == 0.0055
    assert round(max(round(lower, 4), round(upper, 4)) + 0.05, 4) == 0.0754 and Z.BRACKET_TERMS_MICRO == (25400, 5500, 50000)


def test_bracket_eligibility_is_the_fine_grid_rule():
    eligible = [GRID[i] for i in range(25) if Z._eligible(i)]
    assert eligible == [1000000 + 50000 * j for j in range(1, 21)]                    # 1.05 to 2.00: not 0.75, not 1.00, not 2.25 and above
    # with the registered bracket, two eligible boundaries are within it exactly when they are the same level or neighbours
    for a in eligible:
        for b in eligible:
            assert (abs(a - b) <= Z.BRACKET_MICRO) == (abs(a - b) <= 50000)


# ======================= T0: building sweeps =======================
def _level(med_sum, s=40, dead_sum=0):
    """40 seeds, `s` of them surviving with tail sum `med_sum` each; the others with `dead_sum`."""
    return {"survival": [True] * s + [False] * (40 - s), "tail_sum": [med_sum] * s + [dead_sum] * (40 - s)}


def _skeleton(boundary, top=4_000_000, base=400_000, s_below=0):
    """A skeleton sweep with its boundary at index `boundary`: below it `s_below` survivors; from it up, 40 survivors
    and medians rising linearly in κ from `base` to `top`."""
    k0, k1 = GRID[boundary], GRID[-1]
    out = {}
    for i, k in enumerate(GRID):
        if i < boundary: out[k] = _level(base, s_below)
        else: out[k] = _level(base + (top - base) * (k - k0) // max(1, k1 - k0))
    return out


def _realization(lo=600_000, top=6_000_000):
    return {k: _level(lo + (top - lo) * (k - GRID[0]) // (GRID[-1] - GRID[0])) for k in GRID}


def _calibration(spread=2_000, centre=1_000_000):
    """Panels with half the seeds at centre − spread and half at centre + spread at every level."""
    row = [centre - spread] * 20 + [centre + spread] * 20
    return {"skeleton": {k: list(row) for k in GRID}, "realization": {k: list(row) for k in GRID}}


def _run(hi=None, lo=None, re=None, cal=None):
    return Z.evaluate_t0(_skeleton(5) if hi is None else hi, _skeleton(5) if lo is None else lo, _realization() if re is None else re,
                         _calibration() if cal is None else cal)


def _tests(rec): return {t["test"]: (t["outcome"], t["cause"]) for t in rec["tests"]}


# ======================= T0: named cases =======================
def test_eligibility_governs_t_s2_l2_m5_round1_d1():
    """L2 M5 round 1, D1, and Mike's ruling of 2026-11-18: once T-S1′ has located the high boundary and no low record is
    missing, T-S2 is ND `bracket outside fine grid` unless BOTH sweeps have a boundary eligible under §5.8. A low sweep
    with no boundary does not bring back Flight 8's FAIL. T-S2's only FAIL is `hysteresis`."""
    obs = lambda survives, total: {"survival": [survives] * 40, "tail_sum": [total] * 40}
    # L2's counterexample, as written in its Appendix A
    high = {k: obs(k >= 1_000_000, 1_000_000 if k >= 1_000_000 else 0) for k in GRID}
    low = {k: obs(False, 0) for k in GRID}
    realization = {k: obs(True, 1_000_000) for k in GRID}
    calibration = {o: {k: [1_000_000] * 40 for k in GRID} for o in ("skeleton", "realization")}
    rec = Z.evaluate_t0(high, low, realization, calibration)
    assert rec["reference"]["kappa_c_t0_micro"] == 1000000 and Z._eligible(GRID.index(1000000)) is False
    assert _tests(rec) == {"T-S1′": ("PASS", None), "T-S1c": ("PASS", None), "T-S2": ("ND", "bracket outside fine grid"), "T-R1′": ("PASS", None)}
    assert (rec["determination"], rec["cause"]) == ("NOT DISTINGUISHED", "bracket outside fine grid")
    assert rec["persistence"]["skeleton_low"]["profile"] == "criterion met at no tested level"            # the low sweep's phases are kept
    d = rec["tests"][2]["detail"]
    assert d["low_boundary_micro"] is None and d["separation_micro"] is None and d["low_profile"] == "criterion met at no tested level"
    assert d["eligible"] == {"boundary": False, "low_boundary": False}
    # every kind of low sweep without a boundary, against a high boundary inside the fine grid, at its lower edge and above it
    none = {k: _level(0, 0) for k in GRID}
    nm = _skeleton(8); nm[GRID[3]] = _level(400_000, 40)
    lows = {"criterion met at no tested level": none, "criterion met at all tested levels": _skeleton(0), "non-monotone criterion profile": nm}
    for b_hi in (1, 5, 21, 22, 24):                                                   # 1.00, 1.20, 2.00, 2.25, 3.00
        for profile, low in lows.items():
            rec = _run(hi=_skeleton(b_hi), lo=low)
            t = _tests(rec)
            assert t["T-S2"] == ("ND", "bracket outside fine grid") and t["T-S1′"] == t["T-S1c"] == t["T-R1′"] == ("PASS", None)
            assert (rec["determination"], rec["cause"]) == ("NOT DISTINGUISHED", "bracket outside fine grid")
            d = rec["tests"][2]["detail"]
            assert d["low_profile"] == profile == rec["persistence"]["skeleton_low"]["profile"] and d["low_boundary_micro"] is None
            assert d["eligible"] == {"boundary": Z._eligible(b_hi), "low_boundary": False}
    # an ineligible low boundary against an eligible high one, and the reverse
    for b_hi, b_lo in ((5, 1), (5, 22), (1, 5), (22, 5)):
        assert _tests(_run(hi=_skeleton(b_hi), lo=_skeleton(b_lo)))["T-S2"] == ("ND", "bracket outside fine grid")
    # a missing low record stays an apparatus result, whatever the high boundary: it is not relabelled
    key = "apparatus unevaluable (missing level record)"
    for b_hi in (1, 5, 22):
        for low in (_skeleton(5), none, _skeleton(0)):
            low = dict(low); low[GRID[11]] = None
            rec = _run(hi=_skeleton(b_hi), lo=low)
            assert _tests(rec)["T-S2"] == ("ND", key) and rec["tests"][2]["detail"]["missing_levels"] == [GRID[11]] and rec["cause"] == key
    # the high sweep's prerequisite is unchanged: without a located high boundary T-S2 is the dependency ND
    assert _tests(_run(hi=none, lo=none))["T-S2"] == ("ND", "not evaluable: T-S1′ did not locate a boundary (no active phase in sweep)")
    # and with two eligible boundaries the comparison is what it was
    assert _tests(_run(hi=_skeleton(5), lo=_skeleton(6)))["T-S2"] == ("PASS", None)
    assert _tests(_run(hi=_skeleton(5), lo=_skeleton(7)))["T-S2"] == ("FAIL", "hysteresis")


def test_l2s_exact_boundary_witnesses():
    """L2 M5 round 1, §5: two constructions where a decision sits exactly on its limit."""
    # the band between a constant panel and one with a single seed at 1,200,000 is exactly 37,599/(2D)
    flat, one = [1_000_000] * 40, [1_000_000] * 39 + [1_200_000]
    assert Z.band_squared(Z.s_hat_squared(flat), Z.s_hat_squared(one)) == Fraction(37_599, 2 * DEN) ** 2
    cal = _calibration(); cal["skeleton"][GRID[10]] = flat; cal["skeleton"][GRID[11]] = one
    assert (GRID[10], GRID[11]) == (1450000, 1500000)
    for half, want in ((37_598, ("PASS", None)), (37_599, ("PASS", None)), (37_600, ("ND", "non-monotone at finite sample (1.450000, 1.500000)"))):
        incs = [50_000] * 19; incs[5] = incs[6] = 5_000                                # a shallow stretch, so the rise after the reversal is no excess
        hi = _fine_branch(incs)
        v = hi[GRID[10]]["tail_sum"][0]
        hi[GRID[11]] = {"survival": [True] * 40, "tail_sum": [v - half] * 20 + [v] * 20}
        assert _tests(_run(hi=hi, cal=cal))["T-S1c"] == want
    # across 1.00 → 1.05 with an endpoint range of 2,000,000 tail-sum counts, the limit on the increase is 250,000
    for inc, want in ((249_999, ("PASS", None)), (250_000, ("PASS", None)), (250_001, ("ND", "continuity unresolved at grid resolution (1.050000)"))):
        rest = 2_000_000 - inc
        incs = [inc] + [rest // 22] * 22; incs[1] += rest - sum(incs[1:])
        hi = _fine_branch(incs, boundary=1)
        assert sum(incs) == 2_000_000 and max(incs[1:]) < 250_000 and _tests(_run(hi=hi, lo=_skeleton(1)))["T-S1c"] == want


def test_a_continuous_crossing_inside_the_fine_grid_is_produced():
    for b in (2, 5, 12, 21):                                                          # boundaries at 1.05, 1.20, 1.55, 2.00
        rec = _run(hi=_skeleton(b), lo=_skeleton(b))
        assert rec["determination"] == "PRODUCED" and rec["cause"] is None and all(v == ("PASS", None) for v in _tests(rec).values())
        assert rec["reference"] == {"available": True, "kappa_c_t0_micro": GRID[b], "bracket_micro": [GRID[b - 1], GRID[b]],
                                    "profile": "both criterion phases observed", "cause": None, "reference_cause": None}
        assert rec["tests"][0]["detail"]["boundary_micro"] == GRID[b] and rec["record"] == "F9T0Record" and (rec["terrain"], rec["composition"]) == ("T0", "P")
    # neighbours on the fine grid are within the bracket, in either order
    for b_hi, b_lo in ((5, 6), (6, 5)):
        assert _run(hi=_skeleton(b_hi), lo=_skeleton(b_lo))["determination"] == "PRODUCED"
    # 36 survivors meet the criterion and 35 do not
    hi = _skeleton(5); hi[GRID[5]] = _level(400_000, 36)
    assert _run(hi=hi)["tests"][0]["detail"]["boundary_micro"] == GRID[5]
    hi[GRID[5]] = _level(400_000, 35)
    assert _run(hi=hi)["tests"][0]["detail"]["boundary_micro"] == GRID[6]


def test_boundary_absent_or_non_monotone():
    none = {k: _level(0, 0) for k in GRID}
    rec = _run(hi=none)
    assert rec["determination"] == "NOT PRODUCED" and rec["cause"] == "no active phase in sweep"
    t = _tests(rec)
    assert t["T-S1′"] == ("FAIL", "no active phase in sweep")
    assert t["T-S1c"] == t["T-S2"] == ("ND", "not evaluable: T-S1′ did not locate a boundary (no active phase in sweep)") and t["T-R1′"] == ("PASS", None)
    assert rec["reference"]["available"] is False and rec["reference"]["cause"] == "reference unavailable" and rec["reference"]["kappa_c_t0_micro"] is None
    rec = _run(hi=_skeleton(0))                                                       # every level meets the criterion
    assert rec["determination"] == "NOT PRODUCED" and _tests(rec)["T-S1′"] == ("FAIL", "no inactive phase in sweep")
    assert rec["reference"]["available"] is True and rec["reference"]["kappa_c_t0_micro"] == 750000 and rec["reference"]["bracket_micro"] is None   # §5.4: usable, unbracketed
    nm = _skeleton(8); nm[GRID[3]] = _level(400_000, 40)                              # a level meets it and higher ones do not
    rec = _run(hi=nm)
    assert rec["determination"] == "NOT DISTINGUISHED" and rec["cause"] == "non-monotone survival" and rec["reference"]["available"] is False
    assert rec["persistence"]["skeleton_high"]["descriptive_suffix_micro"] == GRID[8]                       # carried, and not the reference
    # a complete low sweep with no boundary supplies no eligible boundary: T-S2 is ND by §5.8's rule (see the D1 test below)
    for low in (none, _skeleton(0), nm):
        rec = _run(lo=low)
        assert _tests(rec)["T-S2"] == ("ND", "bracket outside fine grid") and rec["determination"] == "NOT DISTINGUISHED"
    # a realization failure outranks an ND elsewhere: NOT PRODUCED iff any test fails
    re = _realization(); re[GRID[4]] = _level(0, 0)
    rec = _run(hi=nm, re=re)
    assert rec["determination"] == "NOT PRODUCED" and rec["cause"] == "realization extinct at 1.150000"


def test_hysteresis_and_the_bracket():
    for b_hi, b_lo in ((5, 7), (7, 5), (3, 20)):                                      # two or more fine steps apart, either direction
        rec = _run(hi=_skeleton(b_hi), lo=_skeleton(b_lo))
        assert _tests(rec)["T-S2"] == ("FAIL", "hysteresis") and rec["determination"] == "NOT PRODUCED" and rec["cause"] == "hysteresis"
        d = rec["tests"][2]["detail"]
        assert d["separation_micro"] == abs(GRID[b_hi] - GRID[b_lo]) and d["bracket_micro"] == 75400 and d["eligible"] == {"boundary": True, "low_boundary": True}
    # §5.8: a boundary at 1.00 does not qualify (the level below is 0.75); nor does one above 2.00
    for b_hi, b_lo in ((1, 1), (1, 2), (2, 1), (22, 22), (21, 22), (24, 24), (22, 5)):
        rec = _run(hi=_skeleton(b_hi), lo=_skeleton(b_lo))
        t = _tests(rec)
        assert t["T-S2"] == ("ND", "bracket outside fine grid") and rec["determination"] == "NOT DISTINGUISHED" and rec["cause"] == "bracket outside fine grid"
        assert t["T-S1′"] == t["T-S1c"] == t["T-R1′"] == ("PASS", None)               # the other tests stand
        assert rec["tests"][2]["detail"]["eligible"] == {"boundary": Z._eligible(b_hi), "low_boundary": Z._eligible(b_lo)}
    # an ineligible bracket does not hide a failure elsewhere
    re = _realization(); re[GRID[0]] = _level(0, 0)
    rec = _run(hi=_skeleton(1), lo=_skeleton(1), re=re)
    assert rec["determination"] == "NOT PRODUCED" and rec["cause"] == "realization extinct at 0.750000"


def _fine_branch(incs, base=1_000_000, boundary=5):
    """Skeleton-high with boundary at index 5 (1.20) and the given increments of the median tail sum over the 19 pairs
    above it: 16 fine pairs to 2.00, then 2.00→2.25, 2.25→2.50, 2.50→3.00."""
    assert len(incs) == 24 - boundary
    out = {k: _level(base, 0) for k in GRID[:boundary]}
    v = base
    out[GRID[boundary]] = _level(v)
    for k, d in zip(GRID[boundary + 1:], incs):
        v += d; out[k] = _level(v)
    return out


def test_the_continuity_criterion_is_a_slope_on_the_non_uniform_grid():
    """J = 0.10·Δmed/Δκ against 0.25·range. On a fine pair (Δκ = 0.05) J = 2·Δmed, so the limit is range/8; on
    2.00→2.25 and 2.25→2.50 (Δκ = 0.25) J = 0.4·Δmed, limit 0.625·range; on 2.50→3.00 (Δκ = 0.5) J = 0.2·Δmed, limit
    1.25·range, which no single increase reaches."""
    even = [40_000] * 19                                                              # range 760,000
    assert _tests(_run(hi=_fine_branch(even)))["T-S1c"] == ("PASS", None)
    # a fine pair exactly at the limit passes; one unit over is ND, naming the upper level
    incs = [100_000] + [700_000 // 18] * 18; incs[1] += 800_000 - sum(incs)           # range exactly 800,000; first pair = range/8
    assert sum(incs) == 800_000 and _tests(_run(hi=_fine_branch(incs)))["T-S1c"] == ("PASS", None)
    incs[0] += 1; incs[1] -= 1
    rec = _run(hi=_fine_branch(incs))
    assert _tests(rec)["T-S1c"] == ("ND", "continuity unresolved at grid resolution (1.250000)") and rec["determination"] == "NOT DISTINGUISHED"
    d = rec["tests"][1]["detail"]
    assert d["levels_micro"] == [1200000, 1250000] and abs(d["J"] - 0.10 * (100_001 / DEN) / 0.05) < 1e-15 and abs(d["f_J_times_range"] - 0.25 * 800_000 / DEN) < 1e-15
    # the same half-range step is an excess across a fine pair and not across 2.00→2.25
    step = 400_000
    rest = (800_000 - step) // 18
    fine = [rest] * 19; fine[3] = step; fine[0] += 800_000 - sum(fine)
    coarse = [rest] * 19; coarse[16] = step; coarse[0] += 800_000 - sum(coarse)
    assert GRID[5 + 17] == 2250000 and sum(fine) == sum(coarse) == 800_000
    assert _tests(_run(hi=_fine_branch(fine)))["T-S1c"] == ("ND", "continuity unresolved at grid resolution (1.400000)")
    assert _tests(_run(hi=_fine_branch(coarse)))["T-S1c"] == ("PASS", None)
    for big, want in ((500_000, ("PASS", None)), (500_001, ("ND", "continuity unresolved at grid resolution (2.250000)"))):   # 0.625·range on the 0.25 pair
        coarse = [(800_000 - big) // 18] * 19; coarse[16] = big; coarse[0] += 800_000 - sum(coarse)
        assert sum(coarse) == 800_000 and min(coarse) > 0 and _tests(_run(hi=_fine_branch(coarse)))["T-S1c"] == want
    assert True
    # the lowest excess pair is the one named
    two = list(even); two[4] = 300_000; two[9] = 300_000
    assert _tests(_run(hi=_fine_branch(two)))["T-S1c"] == ("ND", "continuity unresolved at grid resolution (1.450000)")
    # a flat branch has range 0 and no increase: it passes; a boundary at the top level has no pair and passes
    assert _tests(_run(hi=_fine_branch([0] * 19)))["T-S1c"] == ("PASS", None)
    assert _tests(_run(hi=_skeleton(24), lo=_skeleton(24)))["T-S1c"] == ("PASS", None)
    # the realization test applies the same criterion over the whole grid, from the lowest level
    re = _realization(); jump = dict(re)
    for k in GRID[10:]: jump[k] = _level(re[k]["tail_sum"][0] + 3_000_000)
    rec = _run(re=jump)
    assert _tests(rec)["T-R1′"] == ("ND", f"continuity unresolved at grid resolution ({C.level_id(GRID[10])})")


def _band_limit(cal_a, cal_b):
    """The largest reversal of the median tail sum (in units of half a tail-sum count) that is within the band."""
    band2 = Fraction(9) * (Fraction(statistics.variance([Fraction(x, DEN) for x in cal_a])) + Fraction(statistics.variance([Fraction(x, DEN) for x in cal_b]))) \
        * Fraction(12533, 10000) ** 2 / 40
    lim = math.isqrt(int(band2 * (2 * DEN) ** 2))                                     # the largest integer r with (r/2D)² ≤ band²
    assert Fraction(lim, 2 * DEN) ** 2 <= band2 < Fraction(lim + 1, 2 * DEN) ** 2
    return lim


def test_a_reversal_within_the_band_is_disregarded_and_one_beyond_it_is_nd():
    cal = _calibration(spread=2_000)
    lim = _band_limit(cal["skeleton"][GRID[8]], cal["skeleton"][GRID[9]])              # in half-counts: the median's difference times 2D
    assert 2_000 < lim < 4_000
    even = [40_000] * 19
    def with_reversal(half_counts):
        hi = _fine_branch(even)
        v = hi[GRID[8]]["tail_sum"][0]
        row = [v - half_counts] * 20 + [v] * 20                                         # the median is v − h/2
        assert Z.median_twice(row) == 2 * v - half_counts
        hi[GRID[9]] = {"survival": [True] * 40, "tail_sum": row}
        return hi
    rec = _run(hi=with_reversal(lim), cal=cal)
    assert _tests(rec)["T-S1c"] == ("PASS", None) and rec["determination"] == "PRODUCED"                  # at the limit: disregarded
    rec = _run(hi=with_reversal(lim + 1), cal=cal)
    assert _tests(rec)["T-S1c"] == ("ND", "non-monotone at finite sample (1.350000, 1.400000)") and rec["determination"] == "NOT DISTINGUISHED"
    d = rec["tests"][1]["detail"]
    s = float(np.std(np.array(cal["skeleton"][GRID[8]]) / DEN, ddof=1))
    assert abs(d["band"] - 3 * math.sqrt(2 * s * s) * 1.2533 / math.sqrt(40)) < 1e-12 * d["band"] and abs(d["reversal"] - (lim + 1) / (2 * DEN)) < 1e-18
    # a wider calibration spread widens the band: the same reversal is then disregarded
    wide = _calibration(spread=4_000)
    assert _tests(_run(hi=with_reversal(lim + 1), cal=wide))["T-S1c"] == ("PASS", None)
    # each object uses its own panel: widening the realization's panel does not rescue a skeleton reversal, and the reverse
    mixed = {"skeleton": cal["skeleton"], "realization": wide["realization"]}
    assert _tests(_run(hi=with_reversal(lim + 1), cal=mixed))["T-S1c"][0] == "ND"
    re = _realization(); v = re[GRID[12]]["tail_sum"][0]
    re[GRID[13]] = {"survival": [True] * 40, "tail_sum": [v - (lim + 1)] * 20 + [v] * 20}     # a reversal of lim + 1 half-counts
    assert _tests(_run(re=re, cal=cal))["T-R1′"] == ("ND", f"non-monotone at finite sample ({C.level_id(GRID[12])}, {C.level_id(GRID[13])})")
    assert _tests(_run(re=re, cal={"skeleton": cal["skeleton"], "realization": wide["realization"]}))["T-R1′"] == ("PASS", None)
    # a reversal below the boundary is outside the skeleton test's domain
    hi = _skeleton(8, s_below=10)
    hi[GRID[2]] = _level(9_000_000, 10); hi[GRID[3]] = _level(1_000, 10)
    assert _tests(_run(hi=hi, lo=_skeleton(8)))["T-S1c"] == ("PASS", None)


def test_realization_extinct_and_apparatus():
    re = _realization()
    re[GRID[6]] = _level(5_000_000, 20)                                               # 20 at zero: the median is half of one value, positive
    assert Z.median_twice(re[GRID[6]]["tail_sum"]) == 5_000_000
    re[GRID[6]] = _level(5_000_000, 19)                                               # 21 at zero: the median is zero
    re[GRID[9]] = _level(0, 0)
    rec = _run(re=re)
    assert _tests(rec)["T-R1′"] == ("FAIL", "realization extinct at 1.250000") and rec["tests"][3]["detail"]["levels_micro"] == [GRID[6], GRID[9]]
    assert rec["determination"] == "NOT PRODUCED"
    # a missing level: ND apparatus for the tests whose domain holds it
    key = "apparatus unevaluable (missing level record)"
    for drop in (GRID[2], GRID[10]):
        hi = _skeleton(5); hi[drop] = None
        rec = _run(hi=hi)
        t = _tests(rec)
        assert t["T-S1′"] == ("ND", key) and t["T-S1c"] == t["T-S2"] == ("ND", f"not evaluable: T-S1′ did not locate a boundary ({key})")
        assert rec["determination"] == "NOT DISTINGUISHED" and rec["cause"] == key and rec["reference"]["available"] is False
        assert rec["reference"]["cause"] == "reference unavailable" and rec["tests"][0]["detail"]["missing_levels"] == [drop]
    lo = _skeleton(5); del lo[GRID[7]]                                                # an absent key is a missing level too
    assert _tests(_run(lo=lo))["T-S2"] == ("ND", key)
    re = _realization(); re[GRID[0]] = None
    assert _tests(_run(re=re))["T-R1′"] == ("ND", key)
    # a missing calibration level matters only where a reversal has to be judged
    cal = _calibration(); cal["skeleton"][GRID[9]] = None; del cal["realization"][GRID[3]]
    assert _run(cal=cal)["determination"] == "PRODUCED"
    hi = _fine_branch([40_000] * 19); hi[GRID[9]] = _level(hi[GRID[8]]["tail_sum"][0] - 1)
    rec = _run(hi=hi, cal=cal)
    assert _tests(rec)["T-S1c"] == ("ND", "apparatus unevaluable (missing calibration level record)") and rec["tests"][1]["detail"]["missing_levels"] == [GRID[9]]


def test_t0_inputs_are_checked():
    good = (_skeleton(5), _skeleton(5), _realization(), _calibration())
    Z.evaluate_t0(*good)
    def swap(i, fn):
        args = [copy.deepcopy(a) for a in good]; fn(args[i]); return args
    k = GRID[6]
    bad = [
        swap(0, lambda s: s[k].__setitem__("survival", [True] * 39)), swap(0, lambda s: s[k].__setitem__("survival", [1] * 40)),
        swap(1, lambda s: s[k].__setitem__("tail_sum", [1.0] * 40)), swap(2, lambda s: s[k].__setitem__("tail_sum", [True] * 40)),
        swap(2, lambda s: s[k].__setitem__("tail_sum", [DEN + 1] * 40)), swap(0, lambda s: s[k].__setitem__("tail_sum", [-1] * 40)),
        swap(0, lambda s: s[k].__setitem__("extra", 1)), swap(0, lambda s: s[k].pop("survival")), swap(0, lambda s: s.__setitem__(1025000, s[k])),
        swap(0, lambda s: s.__setitem__(str(k), s[k])), swap(0, lambda s: s.__setitem__(k, [])),
        swap(0, lambda s: s[k].__setitem__("tail_sum", [999] * 40)),                                     # survives, yet fewer than one active cell per tail tick
        swap(1, lambda s: s[GRID[0]].__setitem__("tail_sum", [999 * 10000 + 1] * 40)),                   # did not survive, yet no empty tail tick is possible
        swap(3, lambda c: c.pop("realization")), swap(3, lambda c: c.__setitem__("skeleton_low", {})), swap(3, lambda c: c["skeleton"].__setitem__(k, [1] * 39)),
        swap(3, lambda c: c["skeleton"].__setitem__(k, [0.5] * 40)), swap(3, lambda c: c["realization"].__setitem__(1025000, [1] * 40)),
        swap(3, lambda c: c.__setitem__("skeleton", [])),
    ]
    for args in bad: assert _refused(Z.evaluate_t0, *args)
    for args in ((None,) + good[1:], good[:3] + (None,), ([],) + good[1:]): assert _refused(Z.evaluate_t0, *args)
    assert _refused(Z.check_sweep, good[0], "skeleton") and _refused(Z.median_twice, [1] * 39) and _refused(Z.s_hat_squared, [1.0] * 40)
    # edge values that are valid: a survivor with exactly one active cell per tail tick; a non-survivor one tick short of full
    ok = copy.deepcopy(good[0]); ok[k]["tail_sum"] = [1000] * 40
    Z.check_sweep(ok, "skeleton_high")
    ok = copy.deepcopy(good[0]); ok[GRID[0]]["tail_sum"] = [999 * 10000] * 40
    Z.check_sweep(ok, "skeleton_high")


def test_exact_statistics_against_the_library():
    rng = RNG(3)
    for _ in range(200):
        xs = [int(x) for x in rng.integers(0, DEN + 1, 40)]
        dens = [Fraction(x, DEN) for x in xs]
        assert Fraction(Z.median_twice(xs), 2 * DEN) == statistics.median(dens)
        assert Z.s_hat_squared(xs) == statistics.variance(dens)
        ys = [int(x) for x in rng.integers(0, DEN + 1, 40)]
        b2 = Z.band_squared(Z.s_hat_squared(xs), Z.s_hat_squared(ys))
        f = 3 * math.sqrt(np.var(np.array(xs) / DEN, ddof=1) + np.var(np.array(ys) / DEN, ddof=1)) * 1.2533 / math.sqrt(40)
        assert abs(math.sqrt(b2) - f) <= 1e-12 * f
    assert Z.s_hat_squared([7] * 40) == 0 and Z.band_squared(Fraction(0), Fraction(0)) == 0


def test_reference_object_alone():
    ref = Z.reference_from_sweep(_skeleton(5))
    assert ref["available"] and ref["kappa_c_t0_micro"] == 1200000 and ref["persistence"] == O.persistence_record({k: (40 if i >= 5 else 0) for i, k in enumerate(GRID)})
    assert ref == dict(_run()["reference"], persistence=ref["persistence"])
    gone = _skeleton(5); gone[GRID[20]] = None
    ref = Z.reference_from_sweep(gone)
    assert ref["available"] is False and ref["cause"] == "reference unavailable" and ref["reference_cause"] == "apparatus unevaluable (missing level record)"
    # the reference feeds the threshold comparison through counts, never through a record
    counts = {k: sum(v["survival"]) for k, v in _skeleton(5).items()}
    assert CL.threshold_fidelity("TA", "P", _counts(7), 0.5, counts, 0.354)["against_t0"]["reference_kappa_c_micro"] == 1200000


# ======================= T0: a second implementation, on random sweeps =======================
def _reference_t0(hi, lo, re, cal):
    """The four tests written again from the contract's sentences, on Fractions and the statistics library."""
    def boundary(sw):
        if any(sw.get(k) is None for k in GRID): return None, ("ND", "apparatus unevaluable (missing level record)")
        met = [sum(sw[k]["survival"]) >= 36 for k in GRID]
        if not any(met): return None, ("FAIL", "no active phase in sweep")
        if all(met): return None, ("FAIL", "no inactive phase in sweep")
        if any(met[i] and not met[j] for i in range(25) for j in range(i + 1, 25)): return None, ("ND", "non-monotone survival")
        first = met.index(True)
        return first, None
    def med(obs): return statistics.median([Fraction(x, DEN) for x in obs["tail_sum"]])
    def tail(sw, panel, start):
        dom = GRID[start:]
        if any(sw.get(k) is None for k in dom): return ("ND", "apparatus unevaluable (missing level record)")
        m = [med(sw[k]) for k in dom]
        rev = [j for j in range(len(dom) - 1) if m[j + 1] < m[j]]
        if any(panel.get(dom[j]) is None or panel.get(dom[j + 1]) is None for j in rev): return ("ND", "apparatus unevaluable (missing calibration level record)")
        for j in rev:
            s2 = sum(statistics.variance([Fraction(x, DEN) for x in panel[dom[i]]]) for i in (j, j + 1))
            if (m[j] - m[j + 1]) ** 2 > 9 * s2 * Fraction(12533, 10000) ** 2 / 40:
                return ("ND", f"non-monotone at finite sample ({C.level_id(dom[j])}, {C.level_id(dom[j + 1])})")
        rng_ = m[-1] - m[0]
        for j in range(len(dom) - 1):
            J = Fraction(1, 10) * (m[j + 1] - m[j]) / Fraction(dom[j + 1] - dom[j], 10 ** 6)
            if m[j + 1] > m[j] and J > Fraction(1, 4) * rng_: return ("ND", f"continuity unresolved at grid resolution ({C.level_id(dom[j + 1])})")
        return ("PASS", None)
    c, r1 = boundary(hi)
    if c is None:
        r2 = r3 = ("ND", f"not evaluable: T-S1′ did not locate a boundary ({r1[1]})")
    else:
        r1 = ("PASS", None); r2 = tail(hi, cal["skeleton"], c)
        cl, low_result = boundary(lo)
        fine = lambda i: i is not None and i >= 1 and 1000000 <= GRID[i - 1] and GRID[i] <= 2000000 and GRID[i] - GRID[i - 1] == 50000
        if any(lo.get(k) is None for k in GRID): r3 = ("ND", "apparatus unevaluable (missing level record)")
        elif not (fine(c) and fine(cl)): r3 = ("ND", "bracket outside fine grid")                # §5.8's "otherwise", a low sweep with no boundary included
        else: r3 = ("PASS", None) if abs(Fraction(GRID[cl] - GRID[c], 10 ** 6)) <= Fraction(754, 10000) else ("FAIL", "hysteresis")
    if any(re.get(k) is None for k in GRID): r4 = ("ND", "apparatus unevaluable (missing level record)")
    else:
        dead = [k for k in GRID if med(re[k]) <= 0]
        r4 = ("FAIL", f"realization extinct at {C.level_id(dead[0])}") if dead else tail(re, cal["realization"], 0)
    rs = [r1, r2, r3, r4]
    fails = [r for r in rs if r[0] == "FAIL"]; nds = [r for r in rs if r[0] == "ND"]
    det = ("NOT PRODUCED", fails[0][1]) if fails else (("NOT DISTINGUISHED", nds[0][1]) if nds else ("PRODUCED", None))
    return det, rs


def _random_sweep(rng, kind):
    """A sweep with a random survival profile and random medians: mostly a rising branch with noise, sometimes a jump, a
    reversal, a dead level or a missing one."""
    b = int(rng.integers(0, 26)) if rng.random() < 0.85 else 25
    out = {}
    level_v = int(rng.integers(100_000, 900_000))
    slope = int(rng.integers(0, 60_000))
    noise = int(rng.choice([0, 0, 200, 3_000, 40_000]))
    for i, k in enumerate(GRID):
        s = 40 if i >= b else int(rng.integers(0, 36))
        if rng.random() < 0.04: s = int(rng.integers(30, 41))                          # a stray count near the criterion
        if kind == "realization": s = 40
        level_v = max(1_000, level_v + slope + (int(rng.integers(-noise, noise + 1)) if noise else 0))
        if rng.random() < 0.03: level_v += int(rng.integers(200_000, 2_000_000))        # a jump
        if rng.random() < 0.03: level_v = max(1_000, level_v - int(rng.integers(1, 30_000)))   # a reversal
        vals = [min(DEN, max(1_000, level_v + (int(rng.integers(-noise, noise + 1)) if noise else 0))) for _ in range(s)]
        obs = {"survival": [True] * s + [False] * (40 - s), "tail_sum": vals + [0] * (40 - s)}
        if kind == "realization" and rng.random() < 0.005: obs = {"survival": [False] * 40, "tail_sum": [0] * 40}
        out[k] = obs
    if rng.random() < 0.04: out[GRID[int(rng.integers(0, 25))]] = None
    if rng.random() < 0.02: del out[GRID[int(rng.integers(0, 25))]]
    return out


def _random_calibration(rng):
    cal = {}
    for obj in ("skeleton", "realization"):
        spread = int(rng.choice([0, 50, 2_000, 30_000]))
        cal[obj] = {k: [int(x) for x in rng.integers(500_000 - spread, 500_000 + spread + 1, 40)] for k in GRID}
        if rng.random() < 0.05: cal[obj][GRID[int(rng.integers(0, 25))]] = None
        if rng.random() < 0.10:                                                        # a panel with many levels missing
            for i in rng.choice(25, 12, replace=False): cal[obj][GRID[int(i)]] = None
    return cal


def test_the_four_tests_against_the_second_implementation_on_random_sweeps():
    rng = RNG(4)
    seen = set(); dets = {}; low_without_boundary = 0
    n = 4000
    for _ in range(n):
        hi = _random_sweep(rng, "skeleton")
        if rng.random() < 0.6:                                                        # a low sweep related to the high one: same or shifted boundary
            lo = copy.deepcopy(hi)
            shift = int(rng.integers(-3, 4))
            met = [k for k in GRID if lo.get(k) is not None and sum(lo[k]["survival"]) >= 36]
            if met and shift:
                i0 = GRID.index(met[0])
                for i in range(max(0, i0 + min(shift, 0)), min(25, i0 + max(shift, 0))):
                    lo[GRID[i]] = _level(500_000, 40 if shift < 0 else 0)
        else:
            lo = _random_sweep(rng, "skeleton")
        re = _random_sweep(rng, "realization"); cal = _random_calibration(rng)
        rec = Z.evaluate_t0(hi, lo, re, cal)
        det, rs = _reference_t0(hi, lo, re, cal)
        if rec["tests"][0]["outcome"] == "PASS" and rec["tests"][2]["cause"] == "bracket outside fine grid" and rec["tests"][2]["detail"]["low_boundary_micro"] is None:
            low_without_boundary += 1
        assert (rec["determination"], rec["cause"]) == det
        assert [(t["outcome"], t["cause"]) for t in rec["tests"]] == rs
        dets[det[0]] = dets.get(det[0], 0) + 1
        for t in rec["tests"]:
            c = t["cause"]
            kind = None if c is None else c.split(" (")[0].split(" at 0")[0].split(" at 1")[0].split(" at 2")[0].split(" at 3")[0]
            seen.add((t["test"], t["outcome"], kind))
    assert set(dets) == {"PRODUCED", "NOT PRODUCED", "NOT DISTINGUISHED"} and min(dets.values()) >= 20, dets
    want = {("T-S1′", "PASS", None), ("T-S1′", "FAIL", "no active phase in sweep"), ("T-S1′", "FAIL", "no inactive phase in sweep"),
            ("T-S1′", "ND", "non-monotone survival"), ("T-S1′", "ND", "apparatus unevaluable"),
            ("T-S1c", "PASS", None), ("T-S1c", "ND", "non-monotone at finite sample"), ("T-S1c", "ND", "continuity unresolved at grid resolution"),
            ("T-S1c", "ND", "not evaluable: T-S1′ did not locate a boundary"), ("T-S1c", "ND", "apparatus unevaluable"),
            ("T-S2", "PASS", None), ("T-S2", "FAIL", "hysteresis"), ("T-S2", "ND", "bracket outside fine grid"), ("T-S2", "ND", "apparatus unevaluable"),
            ("T-S2", "ND", "not evaluable: T-S1′ did not locate a boundary"),
            ("T-R1′", "PASS", None), ("T-R1′", "FAIL", "realization extinct"), ("T-R1′", "ND", "non-monotone at finite sample"),
            ("T-R1′", "ND", "continuity unresolved at grid resolution"), ("T-R1′", "ND", "apparatus unevaluable")}
    assert want <= seen, want - seen
    assert {x for x in seen if x[0] == "T-S2"} == {x for x in want if x[0] == "T-S2"}      # T-S2 fails by `hysteresis` alone and carries no phase cause (D1)
    assert low_without_boundary >= 200                                                 # complete low sweeps with no boundary, under a located high boundary
    # a missing skeleton-high level always stops T-S1′ first, so T-S1c's only apparatus path is the calibration panel
    assert ("T-S1c", "ND", "apparatus unevaluable") in seen


def test_the_record_is_plain_data_and_states_its_scope():
    import json
    rec = _run()
    back = json.loads(json.dumps(rec))
    assert back["determination"] == "PRODUCED" and set(back["medians"]) == {"skeleton_high", "skeleton_low", "realization"}
    assert back["kind"] == "scientific consistency exercise; gates no endpoint" and "not automatically a coding defect" in back["note"]
    assert rec["declaration_sha256"] == Z.T0_DECLARATION_SHA256_LITERAL and rec["constants"]["bracket_micro"] == 75400
    assert rec["medians"]["realization"][GRID[0]] == 600_000 / DEN and rec["s_hat"]["skeleton"][GRID[0]] == math.sqrt(Fraction(40 * 2000 ** 2, 39 * DEN ** 2))
    same = _run()
    assert same == rec                                                                # a function of its inputs


# ======================= nothing placed before M5 is touched =======================
PLACED = {  # LF identities at 6823c41 (the M4 placement); evaluator.py as repaired for §7's cause precedence (L2 M6B round 1, D1)
    "f9/__init__.py": "7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e",
    "f9/config.py": "5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb",
    "f9/terrain.py": "b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9",
    "f9/geometry.py": "122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971",
    "f9/family.py": "ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1",
    "f9/spectral.py": "b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3",
    "f9/identities.py": "0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577",
    "f9/streams.py": "5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06",
    "f9/dynamics.py": "34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e",
    "f9/evaluator.py": "ddfa49b11955de42d5b6638d892af4c75756ff6b1b5f35ea0884c4de7b2a07a1",
    "f9/outcomes.py": "fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1",
}
UNTOUCHED = "c80d494aea4e5e452b4a96536f0bc68515918e4ac8c7f37e84d66bad7c7a3289"   # root, e1, f8, gates: the digest test_f9_m1.py holds


def _sha_lf(path):
    with open(path, "rb") as fh: return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def test_everything_placed_before_m5_is_byte_unchanged():
    for rel, want in PLACED.items(): assert _sha_lf(os.path.join(PKG, *rel.split("/"))) == want, rel
    # M5's two files are present beside them. The folder is NOT required to hold nothing else: the earlier modules' tests
    # required that, and each of those assertions fails as soon as a later module is placed (found while building M5).
    assert {r.split("/")[1] for r in PLACED} | {"closure.py", "t0.py"} <= {fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")}
    h = hashlib.sha256()
    for sub in ("", "e1", "f8", "gates"):
        d = os.path.join(PKG, sub)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"): h.update((sub + "/" + fn if sub else fn).encode()); h.update(bytes.fromhex(_sha_lf(os.path.join(d, fn))))
    assert h.hexdigest() == UNTOUCHED
