"""tests/test_f9_m6b.py — Flight 9 module M6, part 2: the reports that apply the evaluator or join placed records
(`f9/evaluator_reports.py`; contract §1.3 (a), (d) design side, (f), (g), (h)).

No lattice run is made, no run record is read, and no report is computed on output of the rule. Every map is
constructed here from a fixed generator; the only contract objects used are index geometry (comparison arrays, TD
bases and cores). The placed evaluator is the oracle for the evaluator at another θ: θ = 0.10 on counts c is the
placed θ = 0.20 on 2c, and θ = 0.30 on 3k is the placed θ = 0.20 on 2k, exactly, on integers."""
import hashlib
import json
import os
from fractions import Fraction

import numpy as np
import pytest

from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import evaluator as E
from mfa_instrument.f9 import evaluator_reports as X
from mfa_instrument.f9 import geometry as G
from mfa_instrument.f9 import outcomes as O
from mfa_instrument.f9 import streams as R
from mfa_instrument.f9 import terrain as T

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "mfa_instrument")
L, N, S, TAIL = C.F9_GRID, C.F9_N_CELLS, C.F9_N_SEEDS, C.F9_TAIL_TICKS
M = 777                                                                      # a test master
ONES = np.ones(S, dtype=np.int64)
RNG = lambda *k: np.random.Generator(np.random.PCG64(np.random.SeedSequence([6, 6, 2] + list(k))))


def _refused(fn, *a, **k):
    try: fn(*a, **k)
    except (C.F9ConfigError, E.F9EvaluatorError, O.F9OutcomeError): return True
    return False


def _same(a, b):
    """Equality of two records, type for type, numpy arrays included (nan equal to nan)."""
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return isinstance(a, np.ndarray) and isinstance(b, np.ndarray) and a.dtype == b.dtype and a.shape == b.shape and \
            (np.array_equal(a, b, equal_nan=True) if a.dtype.kind == "f" else np.array_equal(a, b))
    if type(a) is not type(b): return False
    if isinstance(a, dict): return list(a) == list(b) and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)): return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return a == b


def _families(terrain):
    if C.same_family_latent(terrain) is not None:
        first = E.IndexFamily(T.comparison_array(terrain, "P"), terrain, "P")
        return {"P": first, "H": first.shared_with("H")}
    return {c: E.IndexFamily(T.comparison_array(terrain, c), terrain, c) for c in C.F9_COMPOSITIONS}


def _profile_counts(rng, terrain, comp, n_max, top):
    """Integer seed maps (each count at most n_max) whose mean rises with the arm's index from 0 to about top·n_max."""
    lam = T.raw_index(terrain, comp)
    p = top * (lam - lam.min()) / (lam.max() - lam.min())
    return rng.binomial(n_max, p, size=(S, L, L)).astype(np.int64)


# ======================= declaration =======================
def test_declaration_and_registered_values():
    assert X.verify_evaluator_reports_declaration() == X.EVALUATOR_REPORTS_DECLARATION_SHA256_LITERAL == C.frozen_digest(X.EVALUATOR_REPORTS_DECLARATION)
    assert X.THETAS_REPORTED_MICRO == C.F9_THETA_REPORTED_MICRO == (100_000, 300_000) and C.F9_THETA_MICRO == 200_000
    assert X.THETAS_ACCEPTED_MICRO == (100_000, 200_000, 300_000) and X.BOX_DENOMINATOR == 360_000
    assert X.SKELETON_OBJECT_CODE == 1 == dict(R.OBJECT_CODES)["skeleton"]
    assert X.TD_DESIGN_TABLE == (("TD-1-2", 200, 676, "0.338", "0.145"), ("TD-1-4", 200, 1376, "0.688", "0.074"),
                                 ("TD-4-2", 416, 1424, "0.712", "0.142"), ("TD-4-4", 416, 2816, "1.408", "0.074"))          # contract §3.2's table
    d = dict(X.EVALUATOR_REPORTS_DECLARATION)
    assert d["contract"] == C.F9_CONTRACT_SHA256 and d["evaluator_declaration"] == E.EVALUATOR_DECLARATION_SHA256_LITERAL and d["kind"] == X.KIND
    assert issubclass(X.F9EvaluatorReportError, C.F9ConfigError)


# ======================= (f) the criterion at θ =======================
def test_the_criterion_at_theta_is_the_contracts_inequality():
    rng = RNG(1)
    for trial in range(4):
        counts = rng.integers(0, 1001, (S, L, L)) if trial else _profile_counts(rng, "TA", "P", 1000, 0.5)
        w = np.bincount(rng.integers(0, S, S), minlength=S).astype(np.int64) if trial % 2 else ONES
        placed, B = E.occupied_region(counts, w)
        got, B2 = X.occupied_region_at(counts, w, 200_000)
        assert np.array_equal(got, placed) and np.array_equal(B, B2)                      # θ = 0.20: the placed criterion
        for micro, frac in ((100_000, Fraction(1, 10)), (300_000, Fraction(3, 10))):
            got, _ = X.occupied_region_at(counts, w, micro)
            want = np.array([Fraction(int(b), 360_000) >= frac for b in B.ravel()]).reshape(L, L)
            assert np.array_equal(got, want)
        r10, r20, r30 = (X.occupied_region_at(counts, w, t)[0] for t in (100_000, 200_000, 300_000))
        assert not (r30 & ~r20).any() and not (r20 & ~r10).any()                          # nested regions
    for micro, base in ((100_000, 100), (300_000, 300)):                                  # ties are in; one tick below is out
        counts = np.full((S, L, L), base, dtype=np.int64)
        assert X.occupied_region_at(counts, ONES, micro)[0].all()
        counts[0, 50, 50] -= 1
        assert int(X.occupied_region_at(counts, ONES, micro)[0].sum()) == N - 9
    counts = np.zeros((S, L, L), dtype=np.int64)
    for bad in (150_000, 0, 0.1, True, "100000", None, 100_000.0, np.int64(100_000)):
        assert _refused(X.occupied_region_at, counts, ONES, bad), bad
        assert _refused(X.evaluate_level_at, counts, _families("T0"), (M, 0, 0, 1_500_000), bad), bad


# ======================= (f) the whole evaluator at θ, against the placed evaluator =======================
@pytest.fixture(scope="module")
def ta():
    """One constructed level on TA's families. k has counts up to 166, so 2k, 3k and 6k are valid seed maps, and
    θ = 0.10 on 3k ≡ placed θ = 0.20 on 6k;  θ = 0.30 on 3k ≡ placed θ = 0.20 on 2k;  θ = 0.20 on 3k is the placed 3k."""
    fams = _families("TA")
    k = _profile_counts(RNG(2), "TA", "P", 166, 0.9)
    key = E.arm_level_key(M, "TA", "P", 1_500_000)
    return {"fams": fams, "k": k, "key": key, "placed_2k": E.evaluate_level(2 * k, fams, key), "placed_3k": E.evaluate_level(3 * k, fams, key),
            "placed_6k": E.evaluate_level(6 * k, fams, key), "reported_3k": X.reported_thresholds(3 * k, fams, key)}


def test_at_the_scored_threshold_the_wrapper_is_the_placed_evaluator(ta):
    got = X.evaluate_level_at(3 * ta["k"], ta["fams"], ta["key"], 200_000)
    assert _same(got, ta["placed_3k"])
    assert got["point"]["informative"] and got["resampled"] and got["indices"]["P"]["n_C"] + got["indices"]["P"]["n_A"] + got["indices"]["P"]["n_I"] == 1000


def test_the_reported_thresholds_against_the_placed_evaluator_on_scaled_maps(ta):
    rep = ta["reported_3k"]
    assert list(rep["theta_micro"]) == [100_000, 300_000] and rep["kind"] == X.KIND and rep["record"] == "F9ReportedThresholds"
    assert rep["scored_theta_micro"] == 200_000 and "never replace or rescue the scored result" in rep["note"]
    assert _same(rep["theta_micro"][100_000], ta["placed_6k"])                # B(3k) ≥ 36,000  ⇔  B(6k) ≥ 72,000
    assert _same(rep["theta_micro"][300_000], ta["placed_2k"])                # B(3k) ≥ 108,000 ⇔  B(2k) ≥ 72,000
    cells = [ta[n]["point"]["region_cells"] for n in ("placed_6k", "placed_3k", "placed_2k")]
    assert cells[0] > cells[1] > cells[2] > 100 and all(ta[n]["point"]["informative"] and ta[n]["resampled"] for n in ("placed_6k", "placed_3k", "placed_2k"))
    assert not _same(rep["theta_micro"][100_000], rep["theta_micro"][300_000])            # the three thresholds give three different records
    assert not _same(rep["theta_micro"][100_000], ta["placed_3k"]) and not _same(rep["theta_micro"][300_000], ta["placed_3k"])
    for t in (100_000, 300_000):                                              # the scored evaluation's stream: the same key, the declared resamples
        assert rep["theta_micro"][t]["stream_key"] == list(ta["key"]) and rep["theta_micro"][t]["declared_stream"] is True


def test_the_wrapper_on_two_families_and_on_unavailable_states():
    fams = _families("TB")                                                    # each composition has its own family (2,600 and 50 contours)
    assert fams["P"].contours_id != fams["H"].contours_id and (len(fams["P"]), len(fams["H"])) == (2600, 50)
    counts = _profile_counts(RNG(3), "TB", "H", 1000, 0.5)
    key = E.arm_level_key(M, "TB", "H", 1_250_000)
    placed = E.evaluate_level(counts, fams, key)
    assert placed["resampled"] and _same(X.evaluate_level_at(counts, fams, key, 200_000), placed)
    assert _same(X.evaluate_map_at(counts, ONES, fams, 200_000, brute=True), E.evaluate_map(counts, ONES, fams, brute=True))
    zeros = np.zeros((S, L, L), dtype=np.int64)                               # no edge at θ
    full = np.full((S, L, L), 1000, dtype=np.int64)
    small = zeros.copy(); small[:, 10:16, 10:16] = 1000                       # a region under 100 cells
    for c in (zeros, full, small):
        placed = E.evaluate_level(c, fams, key)
        assert not placed["resampled"] and _same(X.evaluate_level_at(c, fams, key, 200_000), placed)
        rep = X.reported_thresholds(c, fams, key)
        for t in (100_000, 300_000):
            assert rep["theta_micro"][t]["indices"]["P"]["result"] == "not informative" and not rep["theta_micro"][t]["resampled"]
    assert X.reported_thresholds(zeros, fams, key)["theta_micro"][100_000]["indices"]["H"]["cause"] == "no edge at theta"
    assert X.reported_thresholds(small, fams, key)["theta_micro"][300_000]["indices"]["H"]["cause"] == "below the informative minimum"
    t0 = _families("T0")                                                      # a constant index: no eligible contour
    assert len(t0["P"]) == 0
    half = zeros.copy(); half[:, :50, :] = 1000
    placed = E.evaluate_level(half, t0, (M, 0, 0, 1_500_000))
    assert placed["indices"]["P"]["cause"] == "no eligible contour" and _same(X.evaluate_level_at(half, t0, (M, 0, 0, 1_500_000), 200_000), placed)
    assert X.reported_thresholds(half, t0, (M, 0, 0, 1_500_000))["theta_micro"][300_000]["indices"]["H"]["cause"] == "no eligible contour"
    assert _refused(X.evaluate_level_at, half.astype(np.float64), t0, (M, 0, 0, 1_500_000), 100_000)
    assert _refused(X.evaluate_level_at, half, {}, (M, 0, 0, 1_500_000), 100_000) and _refused(X.evaluate_level_at, half, t0, [M], 100_000)


# ======================= cause precedence on every route (L2 M6B round 1, D1) =======================
def test_a_constant_index_outranks_the_maps_state_on_every_route():
    """§7: a constant index (L2) is above an empty or full region (L3) and an under-resolved one (L4); §6.2 row 15: "the
    cause does not depend on the sample". In round 1 all twelve routes of L2's Appendix R returned the map's cause: three
    through the evaluator as then placed, nine through this module. Here: L2's three maps and a small-complement map, through the placed evaluator, the copy at θ = 0.20, both
    reported thresholds and the skeleton boundary, with constant, non-constant and mixed families."""
    t0, tb = _families("T0"), _families("TB")
    assert len(t0["P"]) == 0 == len(t0["H"]) and len(tb["H"]) == 50
    no_contour = {"result": "not informative", "cause": "no eligible contour", "resampled": False}
    key = E.arm_level_key(M, "T0", "P", 1_000_000); skey = X.skeleton_level_key(M, "T0", "P", 1_000_000)
    empty = np.zeros((S, L, L), dtype=np.int64); full = np.full((S, L, L), 1000, dtype=np.int64)
    small = empty.copy(); small[:, 10:16, 10:16] = 1000                       # L2's patch
    hole = full.copy(); hole[:, 10:16, 10:16] = 0                             # a complement under 100 cells
    # (map, map cause, {θ: (region cells, bonds)})
    cases = {"empty": (empty, "no edge at theta", {100_000: (0, 0), 200_000: (0, 0), 300_000: (0, 0)}),
             "full": (full, "no edge at theta", {100_000: (N, 0), 200_000: (N, 0), 300_000: (N, 0)}),
             "under_minimum": (small, "below the informative minimum", {100_000: (64, 32), 200_000: (60, 32), 300_000: (52, 32)}),
             "small complement": (hole, "below the informative minimum", {100_000: (N - 16, 16), 200_000: (N - 16, 16), 300_000: (N - 16, 16)})}
    for name, (counts, map_cause, geometry) in cases.items():
        map_entry = {"result": "not informative", "cause": map_cause, "resampled": False}
        routes = {"placed 0.20": (E.evaluate_level(counts, t0, key), 200_000), "copy 0.20": (X.evaluate_level_at(counts, t0, key, 200_000), 200_000),
                  "skeleton 0.20": (X.skeleton_boundary(counts, t0, skey)["evaluation"], 200_000)}
        rep = X.reported_thresholds(counts, t0, key)
        for t in (100_000, 300_000): routes[f"reported {t}"] = (rep["theta_micro"][t], t)
        for route, (rec, theta) in routes.items():
            assert rec["indices"] == {"P": no_contour, "H": no_contour} and rec["resampled"] is False, (name, route)
            p = rec["point"]                                                  # the point still describes the map
            assert not p["informative"] and (p["region_cells"], p["bonds"]) == geometry[theta], (name, route, p["region_cells"], p["bonds"])
        assert _same(routes["copy 0.20"][0], routes["placed 0.20"][0])
        mixed = {"P": t0["P"], "H": tb["H"]}                                  # each index its own cause
        mkey = E.arm_level_key(M, "TB", "H", 1_000_000); mskey = X.skeleton_level_key(M, "TB", "H", 1_000_000)
        mrep = X.reported_thresholds(counts, mixed, mkey)
        for rec in (mrep["theta_micro"][100_000], mrep["theta_micro"][300_000], X.skeleton_boundary(counts, mixed, mskey)["evaluation"],
                    X.evaluate_level_at(counts, mixed, mkey, 200_000)):
            assert rec["indices"] == {"P": no_contour, "H": map_entry}, name
        assert _same(X.evaluate_level_at(counts, mixed, mkey, 200_000), E.evaluate_level(counts, mixed, mkey))
        ordinary = X.reported_thresholds(counts, tb, mkey)                    # non-constant families keep the map's cause
        for t in (100_000, 300_000): assert ordinary["theta_micro"][t]["indices"] == {"P": map_entry, "H": map_entry}, name
    assert geometry is not None and cases["under_minimum"][2][200_000] == (60, 32)


# ======================= (g) the skeleton's boundary =======================
def test_skeleton_key_and_boundary():
    key = X.skeleton_level_key(M, "TA", "H", 1_250_000)
    assert key == (M, 1, 1, 1_250_000, 1) and key[:4] == E.arm_level_key(M, "TA", "H", 1_250_000)
    assert X.skeleton_level_key(M, "T0", "P", 750_000) == (M, 0, 0, 750_000, 1)
    assert _refused(X.skeleton_level_key, M, "T0", "H", 750_000) and _refused(X.skeleton_level_key, M, "TA", "P", 1_234_567)
    assert _refused(X.skeleton_level_key, 0, "TA", "P", 1_000_000) and _refused(X.skeleton_level_key, R.RETIRED_MASTERS[0], "TA", "P", 1_000_000)
    a = E.resample_multiplicities(key); b = E.resample_multiplicities(key[:4])
    assert not np.array_equal(a, b)                                           # its own stream: not the realization's resamples
    fams = _families("TA")
    counts = _profile_counts(RNG(4), "TA", "H", 1000, 0.6)
    counts[::20] = 0                                                          # two extinct runs: their recorded tails are zeros
    assert not counts[0].any() and not counts[20].any() and counts[1].any()   #   (with ten extinct the same check takes minutes: the resampled edges move)
    rec = X.skeleton_boundary(counts, fams, key)
    assert rec["record"] == "F9SkeletonBoundary" and rec["kind"] == X.KIND and rec["theta_micro"] == 200_000 and "not B" in rec["note"]
    assert _same(rec["evaluation"], E.evaluate_level(counts, fams, key)) and rec["evaluation"]["resampled"]
    assert rec["evaluation"]["stream_key"] == list(key)
    extinct = np.zeros((S, L, L), dtype=np.int64)                             # every run extinct: the map has no edge
    rec = X.skeleton_boundary(extinct, fams, key)
    assert rec["evaluation"]["indices"]["P"] == {"result": "not informative", "cause": "no edge at theta", "resampled": False}
    assert X.skeleton_boundary(counts, _families("T0"), X.skeleton_level_key(M, "T0", "P", 1_500_000))["evaluation"]["indices"]["P"]["cause"] == "no eligible contour"
    for bad in (key[:4], key[:4] + (0,), key + (1,), list(key)):              # a realization key, or any other, is refused
        assert _refused(X.skeleton_boundary, extinct, fams, bad), bad


# ======================= (h) component coverage =======================
def _brute_q95(mine: G.Edge, other: G.Edge):
    """Per component of `mine`: the 0.95 quantile of its bonds' torus distances to the nearest bond of `other`, by brute force."""
    d = np.abs(mine.points[:, None, :] - other.points[None, :, :])
    d = np.minimum(d, L - d)
    nearest = np.sqrt((d ** 2).sum(axis=2)).min(axis=1)
    return [float(np.quantile(nearest[mine.component == k], 0.95)) for k in range(mine.n_components)]


def test_component_coverage_on_a_constructed_map():
    """Four discs (TD-4-2's core) fully active in every seed, plus two adjacent cells between them. After the 3×3 mean
    the region at θ = 0.20 is every cell with at least two of its nine neighbours active, so the pair becomes a 3×2
    block with a boundary of 10 bonds: an unresolved component, and under 5% of the edge."""
    fams = _families("TD-4-2")
    core = T.td_core("TD-4-2")
    active = core.copy(); active[49, 49:51] = True
    assert not core[44:56, 44:56].any()
    counts = np.where(active, 1000, 0)[None].repeat(S, axis=0).astype(np.int64)
    rep = X.component_coverage(counts, fams)
    neighbours = sum(np.roll(np.roll(active, di, 0), dj, 1) for di in (-1, 0, 1) for dj in (-1, 0, 1))
    region = neighbours >= 2                                                  # the region, written independently
    e = G.edge(region)
    assert rep["informative"] and rep["reason"] is None and rep["theta_micro"] == 200_000 and rep["component_min_bonds"] == 40
    assert rep["observed"] == {"bonds": e.n_bonds, "components": 5, "resolved": 4, "component_bonds": [int(n) for n in e.component_sizes()]}
    assert sorted(rep["observed"]["component_bonds"])[0] == 10                # the block's boundary: 10 bonds, unresolved
    point = E.evaluate_map(counts, ONES, fams)
    for name in ("P", "H"):
        ent, f = rep["indices"][name], point["indices"][name]
        assert ent["status"] == f["status"] == "within epsilon" and ent["within"] and ent["level_index"] == f["level_index"] and ent["S"] == f["terms"]["S"]
        assert ent["contour_is"] == "the minimizing contour"
        con = fams[name].family.contour(float(fams[name].levels[ent["level_index"]]))
        assert ent["contour"] == {"bonds": con.n_bonds, "components": con.n_components, "resolved": sum(1 for n in con.component_sizes() if n >= 40)}
        # resolved components carry exactly the evaluator's terms, in component order
        assert [(c["bonds"], c["q95_distance"]) for c in ent["observed_components"] if c["resolved"]] == f["terms"]["components_E"]
        assert [(c["bonds"], c["q95_distance"]) for c in ent["contour_components"] if c["resolved"]] == f["terms"]["components_C"]
        assert len(f["terms"]["components_E"]) == 4 and f["terms"]["resolved_E"] == 4
        # every component, resolved or not, against brute-force distances
        for got, want in zip(ent["observed_components"], _brute_q95(e, con)): assert abs(got["q95_distance"] - want) < 1e-12
        for got, want in zip(ent["contour_components"], _brute_q95(con, e)): assert abs(got["q95_distance"] - want) < 1e-12
        assert [c["bonds"] for c in ent["observed_components"]] == rep["observed"]["component_bonds"]
        block = [c for c in ent["observed_components"] if not c["resolved"]]
        assert len(block) == 1 and block[0]["bonds"] == 10 and block[0]["q95_distance"] > 2.0          # far from every contour bond, and in no decision
        assert ent["no_resolved_component_checked_on_observed"] is False and ent["no_resolved_component_checked_on_contour"] is False
    assert _same(rep["indices"]["P"], rep["indices"]["H"])                    # one shared family
    assert json.loads(json.dumps(rep)) == rep                                 # plain data


def test_a_component_of_exactly_forty_bonds_is_resolved():
    """A constructed comparison array with one contour: a 30×30 square and a 10×10 square (120 and 40 bonds). The map is
    fully active on the two squares shrunk by one cell, so its region at θ = 0.20 is each square less its four corners."""
    om = np.zeros((L, L)); om[10:40, 10:40] = 1.0; om[60:70, 60:70] = 1.0
    fam = E.IndexFamily(om, "TA", "P")
    assert len(fam) == 1 and sorted(fam.family.contour(1.0).component_sizes()) == [40, 120]
    counts = np.zeros((S, L, L), dtype=np.int64); counts[:, 11:39, 11:39] = 1000; counts[:, 61:69, 61:69] = 1000
    rep = X.component_coverage(counts, {"P": fam})
    f = E.evaluate_map(counts, ONES, {"P": fam})["indices"]["P"]
    ent = rep["indices"]["P"]
    assert rep["observed"] == {"bonds": 160, "components": 2, "resolved": 2, "component_bonds": [120, 40]} and ent["within"] and f["within"]
    assert ent["contour"] == {"bonds": 160, "components": 2, "resolved": 2}
    assert [(c["bonds"], c["resolved"]) for c in ent["observed_components"]] == [(120, True), (40, True)] == [(c["bonds"], c["resolved"]) for c in ent["contour_components"]]
    assert [(c["bonds"], c["q95_distance"]) for c in ent["observed_components"]] == f["terms"]["components_E"]
    assert [(c["bonds"], c["q95_distance"]) for c in ent["contour_components"]] == f["terms"]["components_C"] and f["terms"]["resolved_E"] == 2
    counts[:, 61:69, 61:69] = 0; counts[:, 61:68, 61:69] = 1000                # a 9×10 block less its corners: 38 bonds, not resolved
    rep = X.component_coverage(counts, {"P": fam})
    assert rep["observed"] == {"bonds": 158, "components": 2, "resolved": 1, "component_bonds": [120, 38]}
    assert [c["resolved"] for c in rep["indices"]["P"]["observed_components"]] == [True, False]


def test_component_coverage_unavailable_states():
    fams = _families("TA")
    zeros = np.zeros((S, L, L), dtype=np.int64)
    rep = X.component_coverage(zeros, fams)
    assert (rep["informative"], rep["reason"], rep["indices"]) == (False, "no edge at theta: the region is empty", {})
    assert rep["observed"] == {"bonds": 0, "components": 0, "resolved": 0, "component_bonds": []}
    half = zeros.copy(); half[:, :50, :] = 1000                               # a band that wraps the torus: two straight edges
    rep = X.component_coverage(half, _families("T0"))
    assert rep["informative"] and rep["observed"]["components"] == 2 and rep["observed"]["resolved"] == 2
    assert rep["indices"]["P"] == {"status": "no eligible contour", "family_size": 0, "cause": "no eligible contour", "observed_components": None, "contour_components": None}
    rep = X.component_coverage(half, fams)                                    # straight edges against TA's closed contours: not within ε
    point = E.evaluate_map(half, ONES, fams)
    ent, f = rep["indices"]["P"], point["indices"]["P"]
    assert ent["status"] == f["status"] and f["within"] is False
    if "level_index" in f:
        assert ent["within"] is False and ent["contour_is"].startswith("least S among the contours examined") and ent["S"] == f["terms"]["S"] > 2.0
        assert [(c["bonds"], c["q95_distance"]) for c in ent["observed_components"] if c["resolved"]] == f["terms"]["components_E"]
    else:
        assert ent["cause"] == "no contour examined" and ent["observed_components"] is None
    assert _refused(X.component_coverage, half.astype(np.float32), fams) and _refused(X.component_coverage, half, {"P": None})


# ======================= (d) design-side margins =======================
def test_design_margins_reproduce_the_contracts_table():
    for name, perimeter, band_cells, ratio, step in X.TD_DESIGN_TABLE:
        v = T.bases(name)[0]
        rep = X.design_margins(name, v)
        centres, Rad, w = C.td_params(name)
        Sref = 0.5 * (1.0 + np.tanh(T.td_delta(name) / w))                    # the contract's arithmetic (arith/td_final.py), written here
        band = (Sref > 0.1) & (Sref < 0.9); core = T.td_delta(name) >= 0
        assert rep["core"] == {"cells": 2000, "perimeter_bonds": perimeter, "components": len(centres), "component_bonds": [perimeter // len(centres)] * len(centres)}
        assert perimeter == int((core != np.roll(core, 1, 0)).sum() + (core != np.roll(core, 1, 1)).sum())
        assert rep["band"] == {"cells": band_cells, "inside_core": int((band & core).sum()), "outside_core": int((band & ~core).sum())}
        assert int(band.sum()) == band_cells and rep["band"]["inside_core"] + rep["band"]["outside_core"] == band_cells
        assert Fraction(rep["band_over_core"]["exact"]) == Fraction(band_cells, 2000) and f"{rep['band_over_core']['value']:.3f}" == ratio
        t = 0.3 + 0.6 * Sref
        assert abs(rep["largest_base_step"] - max(np.abs(t - np.roll(t, 1, 0)).max(), np.abs(t - np.roll(t, 1, 1)).max())) < 1e-12 and f"{rep['largest_base_step']:.3f}" == step
        assert rep["contract_table"] == {"perimeter": perimeter, "band_cells": band_cells, "band_over_core": ratio, "largest_base_step": step}
        assert float(np.minimum(np.abs(Sref - 0.1), np.abs(Sref - 0.9)).min()) > 1e-4          # no cell near either band limit
        assert rep["kind"] == X.KIND and json.loads(json.dumps(rep)) == rep
    v12 = T.bases("TD-1-2")[0]
    assert _refused(X.design_margins, "TA", T.bases("TA")[0]) and _refused(X.design_margins, "TD-1-2", T.bases("TA")[0])
    assert _refused(X.design_margins, "TD-1-2", T.bases("TD-1-4")[0])         # the same core, another width: the table refuses it
    assert _refused(X.design_margins, "TD-1-2", T.bases("TD-4-2")[0]) and _refused(X.design_margins, "TD-1-2", np.roll(v12, 1, axis=0))
    assert _refused(X.design_margins, "TD-1-2", v12.astype(np.float32)) and _refused(X.design_margins, "TD-1-2", v12[:50])
    bad = v12.copy(); bad[0, 0] = np.nan
    assert _refused(X.design_margins, "TD-1-2", bad)


# ======================= (a) the persistence report =======================
def _sweep(first_met):
    return {k: (40 if i >= first_met else 3) for i, k in enumerate(C.F9_LEVELS_MICRO)}


def test_persistence_report_assembles_the_placed_records():
    names = [f"{t}.{c}" for t, c in C.F9_ARMS]
    assert len(names) == 15 and names[0] == "T0.P" and "T0.H" not in names
    sweeps = {n: _sweep(3 + i % 5) for i, n in enumerate(names)}
    sweeps["TB.H"] = {k: 40 for k in C.F9_LEVELS_MICRO}; sweeps["TC.P"] = {k: 0 for k in C.F9_LEVELS_MICRO}
    sweeps["TD-4-4.H"] = {k: (40 if i % 2 else 10) for i, k in enumerate(C.F9_LEVELS_MICRO)}
    rep = X.persistence_report(sweeps)
    assert list(rep["arms"]) == names and rep["complete"] is True and rep["missing_arms"] == [] and rep["arms_with_missing_levels"] == []
    for n in names: assert _same(rep["arms"][n], O.persistence_record(sweeps[n]))
    assert rep["arms"]["TA.P"]["kappa_c_micro"] == C.F9_LEVELS_MICRO[4] and rep["arms"]["TB.H"]["kappa_c_micro"] == 750_000
    assert rep["arms"]["TC.P"]["kappa_c_micro"] is None and rep["arms"]["TD-4-4.H"]["profile"] == O.PROFILE_NON_MONOTONE
    assert rep["kind"] == X.KIND and "no claim about coupling" in rep["note"] and json.loads(json.dumps(rep))["arms"]["TA.P"]["kappa_c_micro"] == C.F9_LEVELS_MICRO[4]
    partial = dict(sweeps); del partial["TA.H"]; partial["TC.H"] = None
    lev = dict(sweeps["TB.P"]); del lev[1_500_000]; partial["TB.P"] = lev
    rep = X.persistence_report(partial)
    assert rep["complete"] is False and rep["missing_arms"] == ["TA.H", "TC.H"] and rep["arms_with_missing_levels"] == ["TB.P"]
    assert rep["arms"]["TA.H"] is None and rep["arms"]["TB.P"]["missing_levels"] == [1_500_000]
    only_level = dict(sweeps); only_level["TB.P"] = lev                         # every arm present, one level record missing
    rep = X.persistence_report(only_level)
    assert rep["missing_arms"] == [] and rep["arms_with_missing_levels"] == ["TB.P"] and rep["complete"] is False
    only_arm = dict(sweeps); del only_arm["TD-1-2.P"]
    assert X.persistence_report(only_arm)["complete"] is False and X.persistence_report(only_arm)["arms_with_missing_levels"] == []
    assert X.persistence_report({})["missing_arms"] == names
    assert _refused(X.persistence_report, {"T0.H": _sweep(3)}) and _refused(X.persistence_report, {("TA", "P"): _sweep(3)}) and _refused(X.persistence_report, None)
    assert _refused(X.persistence_report, {"TA.P": {1_500_000: 41}}) and _refused(X.arm_name, "T0", "H") and X.arm_name("TD-1-2", "H") == "TD-1-2.H"


# ======================= the module's place =======================
def test_the_reports_reach_the_scored_modules_one_way():
    src = open(os.path.join(PKG, "f9", "evaluator_reports.py"), encoding="utf-8").read()
    imports = [ln.strip() for ln in src.splitlines() if ln.startswith(("from ", "import "))]
    assert imports == ["from __future__ import annotations", "from fractions import Fraction", "from typing import Dict, Optional, Tuple", "import numpy as np",
                       "from . import config as C", "from . import evaluator as E", "from . import geometry as G", "from . import outcomes as O",
                       "from . import streams as R", "from . import terrain as T", "from .config import F9ConfigError"]
    for fn in os.listdir(os.path.join(PKG, "f9")):
        if fn.endswith(".py") and fn != "evaluator_reports.py":
            other = open(os.path.join(PKG, "f9", fn), encoding="utf-8").read()
            assert "evaluator_reports" not in other, fn
    assert "F9_THETA_MICRO =" not in src and "C.F9_THETA_MICRO =" not in src                      # the registered constant is read, never assigned
    theta_before = C.F9_THETA_MICRO
    X.occupied_region_at(np.zeros((S, L, L), dtype=np.int64), ONES, 100_000)
    assert C.F9_THETA_MICRO == theta_before == 200_000


PLACED = {  # LF identities at ff136d7: the M6 part 1 placement, with evaluator.py as repaired at 7a1094a (cause precedence)
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
    "f9/closure.py": "7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9",
    "f9/t0.py": "a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472",
    "f9/reports.py": "f42f93c586288ee14ee11dfe8e2430e544e81529a2eaba17e73b0bf4345a92de",
}
UNTOUCHED = "c80d494aea4e5e452b4a96536f0bc68515918e4ac8c7f37e84d66bad7c7a3289"   # root, e1, f8, gates: the digest test_f9_m1.py holds


def _sha_lf(path):
    with open(path, "rb") as fh: return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def test_everything_placed_before_m6b_is_byte_unchanged():
    for rel, want in PLACED.items(): assert _sha_lf(os.path.join(PKG, *rel.split("/"))) == want, rel
    # Subset form: the folder holds these and evaluator_reports.py, and is not required to hold nothing else.
    assert {r.split("/")[1] for r in PLACED} | {"evaluator_reports.py"} <= {fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")}
    h = hashlib.sha256()
    for sub in ("", "e1", "f8", "gates"):
        d = os.path.join(PKG, sub)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"): h.update((sub + "/" + fn if sub else fn).encode()); h.update(bytes.fromhex(_sha_lf(os.path.join(d, fn))))
    assert h.hexdigest() == UNTOUCHED
