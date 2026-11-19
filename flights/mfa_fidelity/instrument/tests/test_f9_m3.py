"""tests/test_f9_m3.py — Flight 9 module M3: the composition evaluator of contract §5.5.

Every map here is SYNTHETIC: integer seed maps built in the test from a chosen region. No run of the rule is made,
no master is used, and no run record or probe output is read. The tests establish the mechanics of each step against
independent implementations (exact rationals for the criterion, pairwise distances for the discrepancy, exhaustive
search for the pruning), the declared resampling stream, the result table at its boundaries, and that nothing placed
before M3 is touched."""
import hashlib
import json
import math
import os
from fractions import Fraction

import numpy as np
import pytest

from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import evaluator as E
from mfa_instrument.f9 import geometry as G
from mfa_instrument.f9 import identities as I
from mfa_instrument.f9 import terrain as T

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "mfa_instrument")
L, N, S, TAIL = C.F9_GRID, C.F9_N_CELLS, C.F9_N_SEEDS, C.F9_TAIL_TICKS
ONES = np.ones(S, dtype=np.int64)
RNG = lambda *k: np.random.Generator(np.random.PCG64(np.random.SeedSequence([4, 4, 3] + list(k))))


def _refused(fn, *a, **k):
    try: fn(*a, **k)
    except (C.F9ConfigError, E.F9EvaluatorError): return True
    return False


def flat_counts(mask, inside=350, outside=60):
    """Seed maps identical across seeds: `inside` active tail ticks in the region, `outside` elsewhere."""
    return np.broadcast_to(np.where(mask, inside, outside), (S, L, L)).astype(np.int64).copy()


def noisy_counts(mask, gen, inside=0.35, outside=0.06):
    return gen.binomial(TAIL, np.broadcast_to(np.where(mask, inside, outside), (S, L, L))).astype(np.int64)


def grow(mask, k):
    """The region enlarged by k cells in the 4-neighbour sense (k < 0 shrinks it)."""
    m = mask.copy()
    for _ in range(abs(k)):
        n = np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1) if k > 0 else \
            np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
        m = (m | n) if k > 0 else (m & n)
    return m


@pytest.fixture(scope="module")
def arrays(tmp_path_factory):
    d = str(tmp_path_factory.mktemp("f9_identities_m3"))
    I.write_bundle(d)
    return I.load_bundle(d)[1]


@pytest.fixture(scope="module")
def fams(arrays):
    return {t: E.index_families(arrays, t) for t in ("T0", "TA", "TB", "TD-4-2")}


# ======================= declaration =======================
def test_declaration_verifies_and_a_changed_literal_fails(monkeypatch):
    assert E.verify_evaluator_declaration() == E.EVALUATOR_DECLARATION_SHA256_LITERAL == C.frozen_digest(E.EVALUATOR_DECLARATION)
    assert (E.N_RESAMPLES, E.INVALID_MAX, E.SUPPORT_MIN, E.EPSILON, E._PRUNE_R2) == (1000, 50, 950, 2.0, 25)
    monkeypatch.setattr(E, "SUPPORT_MIN", 900); assert _refused(E.verify_evaluator_declaration); monkeypatch.undo()
    monkeypatch.setattr(E, "EVALUATOR_DECLARATION", E.EVALUATOR_DECLARATION[:-1]); assert _refused(E.verify_evaluator_declaration); monkeypatch.undo()
    monkeypatch.setattr(E, "EVALUATOR_DECLARATION_SHA256_LITERAL", "PLACEHOLDER"); assert _refused(E.verify_evaluator_declaration)


# ======================= steps 1, 2 and 4 =======================
def test_region_is_the_contracts_criterion_in_exact_rationals():
    gen = RNG(1)
    counts = gen.integers(0, TAIL + 1, size=(S, L, L))
    counts[:, :50] = gen.integers(150, 251, size=(S, 50, L))                  # a band whose box means straddle 0.20
    for weights in (ONES, np.bincount(gen.integers(0, S, size=S), minlength=S)):
        mask, B = E.occupied_region(counts, weights)
        total = [[sum(int(weights[s]) * int(counts[s, i, j]) for s in range(S)) for j in range(L)] for i in range(L)]
        for i in range(0, L, 7):
            for j in range(L):
                box = sum(total[(i + di) % L][(j + dj) % L] for di in (-1, 0, 1) for dj in (-1, 0, 1))
                assert box == B[i, j]
                p_bar_boxed = Fraction(box, 9 * S * TAIL)                     # the 3×3 mean of the seed mean of A/1000
                assert bool(mask[i, j]) == (p_bar_boxed >= Fraction(C.F9_THETA_MICRO, C.MICRO_UNITS))
        assert np.allclose(E.p_tilde(B), B / 360000.0)


def test_ties_at_theta_are_included_exactly():
    counts = np.full((S, L, L), 200, dtype=np.int64)                          # p̃ = 0.20 exactly, everywhere
    mask, B = E.occupied_region(counts, ONES)
    assert mask.all() and int(B[0, 0]) * 10 ** 6 == C.F9_THETA_MICRO * 9 * S * TAIL
    counts[0, 10, 10] -= 1                                                    # one tick fewer in one seed: nine box means fall below
    mask, _ = E.occupied_region(counts, ONES)
    want = np.ones((L, L), dtype=bool); want[9:12, 9:12] = False
    assert np.array_equal(mask, want)
    counts[1, 10, 10] += 1                                                    # restored by another seed
    assert E.occupied_region(counts, ONES)[0].all()


def test_inputs_are_checked():
    good = np.zeros((S, L, L), dtype=np.int64)
    for bad in (good.astype(float), good[:-1], good[:, :-1], good - 1, good + TAIL + 1, "x"):
        assert _refused(E.check_counts, bad)
    assert E.check_counts(good.astype(np.uint16)).dtype == np.int64
    for bad in (ONES.astype(float), ONES[:-1], ONES * 2, np.r_[ONES[:-2], [-1, 3]]):
        assert _refused(E.check_weights, bad)
    two = ONES.copy(); two[0] = 2; two[1] = 0
    assert int(E.check_weights(two).sum()) == S


def test_weights_are_bounded_before_they_are_summed_l2_m3_round1_d1():
    """L2 M3 round 1, D1: an unsigned sum can wrap to n_seeds and a conversion can make a large unsigned value
    negative. Each element is bounded in its own type first. L2's vector, and others of the same kind, are refused in
    every integer type; valid vectors of every integer type are accepted and come back as int64."""
    l2 = np.zeros(S, dtype=np.uint64); l2[0] = np.uint64(2 ** 64 - 1); l2[1] = np.uint64(41)
    assert int(l2.sum()) == S                                                 # the wrapped sum that passed in round 1
    assert _refused(E.check_weights, l2)
    wraps = []
    for dt, top in ((np.uint64, 2 ** 64), (np.uint32, 2 ** 32), (np.uint16, 2 ** 16), (np.uint8, 2 ** 8)):
        w = np.zeros(S, dtype=dt); w[0] = top - 1; w[1] = 41; wraps.append(w)                      # sums to top + 40
        w = np.zeros(S, dtype=dt); w[:2] = top // 2; w[2] = 40; wraps.append(w)                    # two halves and 40
    w = np.zeros(S, dtype=np.int64); w[0] = 2 ** 63 - 1; w[1] = 2 ** 63 - 1; w[2] = 42; wraps.append(w)   # signed wrap: -2 + 42
    w = np.zeros(S, dtype=np.int8); w[0] = 127; w[1] = 127; w[2] = 42; wraps.append(w)
    w = np.zeros(S, dtype=np.int64); w[0] = -1; w[1] = 41; wraps.append(w)                           # a true negative
    w = np.zeros(S, dtype=np.int64); w[0] = 41; wraps.append(w)                                     # above n_seeds, wrong sum
    for w in wraps: assert _refused(E.check_weights, w), (w.dtype, w[:3])
    valid = [np.ones(S), np.r_[40, np.zeros(S - 1)], np.r_[np.zeros(S - 1), 40], np.r_[20, 20, np.zeros(S - 2)], np.r_[2, 0, np.ones(S - 2)]]
    for v in valid:
        for dt in (np.uint64, np.uint32, np.uint16, np.uint8, np.int64, np.int32, np.int16, np.int8):
            out = E.check_weights(v.astype(dt))
            assert out.dtype == np.int64 and np.array_equal(out, v.astype(np.int64)) and int(out.sum()) == S
    # the same input rule for the seed maps: a large unsigned count is refused before conversion
    c = np.zeros((S, L, L), dtype=np.uint64); c[0, 0, 0] = np.uint64(2 ** 64 - 1)
    assert _refused(E.check_counts, c)
    c[0, 0, 0] = TAIL; assert int(E.check_counts(c)[0, 0, 0]) == TAIL
    # and a constructed resample set containing L2's row is an apparatus failure, not a draw: refused before anything is
    # computed, here on a map with no edge, where the resamples would not have been used at all
    mult = np.tile(np.ones(S, dtype=np.uint64), (1000, 1)); mult[17] = l2
    assert _refused(E.evaluate_level, np.full((S, L, L), 300, dtype=np.int64), {"H": E.IndexFamily(np.arange(N, dtype=np.float64).reshape(L, L), "TB", "H")}, (1,), multiplicities=mult)


def test_the_float_decision_at_epsilon_is_the_exact_decision_for_every_possible_term():
    """Every term of S is an order statistic sqrt(a)/2, or an interpolation sqrt(a)/2 + (sqrt(b)/2 - sqrt(a)/2)·(r/20),
    with a ≤ b integers in [0, 20000] (squared doubled distances on the torus) and r in 1..19. The float test `≤ 2.0`
    is compared with the same inequality decided on integers, for every (a, b, r) that can straddle ε."""
    assert 2 * (2 * L // 2) ** 2 == 20000                                    # the largest squared doubled distance: (L, L)
    # an order statistic: sqrt(a)/2 <= 2  <=>  a <= 16
    a = np.arange(0, 20001, dtype=np.int64)
    assert np.array_equal(np.sqrt(a.astype(np.float64)) / 2.0 <= 2.0, a <= 16)
    # an interpolation that straddles: a <= 16 < b
    a = np.arange(0, 17, dtype=np.int64)[:, None, None]; b = np.arange(17, 20001, dtype=np.int64)[None, :, None]; r = np.arange(1, 20, dtype=np.int64)[None, None, :]
    lo = np.sqrt(a.astype(np.float64)) / 2.0; hi = np.sqrt(b.astype(np.float64)) / 2.0
    as_computed = (lo + (hi - lo) * (r / 20.0)) <= 2.0                        # the module's written order
    # exactly: (20 - r)·sqrt(a) + r·sqrt(b) <= 80. Both sides of r·sqrt(b) <= 80 - (20 - r)·sqrt(a) are non-negative (sqrt(a) <= 4),
    # so square: 160(20 - r)·sqrt(a) <= M with M = 6400 + (20 - r)²a - r²b; then M >= 0 and 25600(20 - r)²a <= M².
    M = 6400 + (20 - r) ** 2 * a - r * r * b
    exact = (M >= 0) & (25600 * (20 - r) ** 2 * a <= M * M)
    assert as_computed.size == 17 * 19984 * 19 and np.array_equal(as_computed, exact) and exact.any() and not exact.all()
    # the module's own function on the straddling pairs nearest the boundary, and on pairs that do not straddle
    for (x, y, n) in ((16, 17, 2), (0, 6400, 2), (15, 17, 21), (16, 16, 2), (17, 20000, 2)):
        vals = np.sqrt(np.array([x] * 1 + [y] * (n - 1), dtype=np.float64)) / 2.0
        k, rr = divmod(19 * (n - 1), 20)
        want = Fraction(0)
        got = E.q95(np.sort(vals))
        ex = (x <= 16) if rr == 0 and k == 0 else None
        if n == 2:                                                            # one interpolation, weight 19/20
            Mx = 6400 + 1 * x - 361 * y
            ex = (y <= 16) or (x <= 16 and Mx >= 0 and 25600 * x <= Mx * Mx)
        if ex is not None: assert (got <= 2.0) == ex, (x, y, n)
    both_low = lo[:, 0, 0][:, None] + (2.0 - lo[:, 0, 0][:, None]) * (np.arange(1, 20) / 20.0)[None, :]   # a <= 16 and b = 16: never above ε
    assert (both_low <= 2.0).all()


def test_step4_reasons():
    def reason(mask): return E.step4(mask, G.edge(mask))
    z = np.zeros((L, L), dtype=bool)
    assert reason(z).startswith("no edge at theta") and reason(~z).startswith("no edge at theta")
    sq = z.copy(); sq[:10, :10] = True                                        # 100 cells, 40 bonds: informative
    assert reason(sq) is None and G.edge(sq).n_bonds == 40
    small = sq.copy(); small[0, 0] = False
    assert reason(small) == "the region has under 100 cells" and reason(~small) == "the complement has under 100 cells"
    few = G.Edge(G.edge(sq).points[:39], G.edge(sq).component[:39])           # not a real edge: the bond minimum alone
    assert E.step4(sq, few) == "the edge has under 40 bonds"


# ======================= step 6: distances, quantile, discrepancy =======================
def _torus_d2(a, b, pa, pb):
    """Pairwise squared distance in doubled units, cell by cell, from the definition."""
    H = 2 * L
    da = np.abs(a[:, None] - pa[None, :]); da = np.minimum(da, H - da)
    db = np.abs(b[:, None] - pb[None, :]); db = np.minimum(db, H - db)
    return da * da + db * db


def test_distance_grid_is_exact():
    gen = RNG(2)
    H = 2 * L
    ii, jj = (x.ravel() for x in np.meshgrid(np.arange(H), np.arange(H), indexing="ij"))
    for n in (1, 2, 7, 60, 400):
        a = gen.integers(0, H, size=n); b = gen.integers(0, H, size=n)
        if n == 2: a[:] = (0, H - 1); b[:] = (0, H - 1)                       # neighbours across the wrap
        want = _torus_d2(ii, jj, a, b).min(axis=1).reshape(H, H)
        got = E.distance_grid(a, b)
        assert got.dtype == np.int64 and np.array_equal(got, want)
    assert _refused(E.distance_grid, np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.int64))
    assert _refused(E.doubled, np.array([[1.0, 1.0]])) and _refused(E.doubled, np.array([[0.5, 0.5]])) and _refused(E.doubled, np.array([[0.25, 1.0]]))
    a, b = E.doubled(np.array([[0.5, 3.0], [99.5, 0.0], [4.0, 99.5]]))
    assert a.tolist() == [1, 199, 8] and b.tolist() == [6, 0, 199]


def test_quantile_rule():
    assert E.q95(np.array([3.0])) == 3.0 and E.q95(np.array([1.0, 2.0])) == 1.95
    assert E.q95(np.arange(21.0)) == 19.0                                     # 0.95·20 = 19 exactly: an order statistic
    assert E.q95(np.arange(41.0)) == 38.0
    gen = RNG(3)
    for n in (2, 3, 19, 20, 21, 40, 41, 100, 337, 1000):
        ints = np.sort(gen.integers(0, 10 ** 6, size=n))
        k, r = divmod(19 * (n - 1), 20)
        exact = Fraction(int(ints[k])) + (Fraction(int(ints[min(k + 1, n - 1)]) - int(ints[k]) if r else 0)) * Fraction(r, 20)
        got = E.q95(ints.astype(np.float64))
        assert abs(Fraction(got) - exact) <= Fraction(1, 10 ** 6)
        assert math.isclose(got, float(np.quantile(ints.astype(np.float64), 0.95)), rel_tol=1e-12)
    assert _refused(E.q95, np.zeros(0))


def _reference_S(e_obs, e_con, m=40):
    """S of §5.5 step 6 from pairwise float distances and numpy's quantile: nothing shared with the module."""
    def side(p, comp, q):
        d = np.abs(p[:, None, :] - q[None, :, :]); d = np.minimum(d, L - d)
        dist = np.sqrt((d ** 2).sum(axis=2)).min(axis=1)
        terms = [np.quantile(dist, 0.95)]
        for k in np.unique(comp):
            if (comp == k).sum() >= m: terms.append(np.quantile(dist[comp == k], 0.95))
        return terms
    return max(side(e_obs.points, e_obs.component, e_con.points) + side(e_con.points, e_con.component, e_obs.points))


def _strip(lo, hi):
    m = np.zeros((L, L), dtype=bool); m[:, lo:hi] = True
    return m


def test_joint_discrepancy_on_hand_cases():
    tr = lambda mask: E._Traced(G.edge(mask))
    a, b = tr(_strip(20, 60)), tr(_strip(23, 63))                              # the same strip moved three cells
    s = E.joint_discrepancy(a, b)
    assert s["S"] == 3.0 == s["global_E"] == s["global_C"] and s["resolved_E"] == s["resolved_C"] == 2
    assert E.joint_discrepancy(a, a)["S"] == 0.0
    wrap = E.joint_discrepancy(tr(_strip(0, 40)), tr(_strip(98, 100) | _strip(0, 38)))   # moved two cells across the wrap
    assert wrap["S"] == 2.0
    # four strips (eight lines, 800 bonds) and one far 10×10 square (40 bonds, 4.8% of the edge)
    strips = _strip(5, 10) | _strip(25, 30) | _strip(45, 50) | _strip(65, 70)
    sq = np.zeros((L, L), dtype=bool); sq[40:50, 80:90] = True
    both = E.joint_discrepancy(tr(strips | sq), tr(strips))
    assert both["global_E"] == 0.0 and both["global_C"] == 0.0               # the global terms do not see the square
    assert both["resolved_E"] == 9 and both["S"] > E.EPSILON                  # its own term does: every resolved component is checked
    assert both["S"] == max(v for _, v in both["components_E"])
    small = np.zeros((L, L), dtype=bool); small[40:49, 80:89] = True          # 9×9: 36 bonds, under m
    unseen = E.joint_discrepancy(tr(strips | small), tr(strips))
    assert unseen["resolved_E"] == 8 and unseen["S"] == 0.0                   # an unresolved component is not checked: the claim's stated limit
    none = E.joint_discrepancy(tr(small), tr(small))
    assert none["resolved_E"] == 0 and none["no_resolved_component_checked_on_E"] and none["no_resolved_component_checked_on_C"]
    assert E.joint_discrepancy(a, b, bound=3.0) is None and E.joint_discrepancy(a, b, bound=3.5)["S"] == 3.0


def test_joint_discrepancy_against_pairwise_reference():
    gen = RNG(4)
    blobs = []
    for _ in range(6):                                                        # irregular regions: thresholded smooth noise
        f = gen.normal(size=(L, L))
        for _ in range(6): f = sum(np.roll(np.roll(f, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1)) / 9.0
        blobs.append(f > np.quantile(f, gen.uniform(0.3, 0.7)))
    for x, y in zip(blobs[:-1], blobs[1:]):
        ex, ey = G.edge(x), G.edge(y)
        got = E.joint_discrepancy(E._Traced(ex), E._Traced(ey))["S"]
        assert math.isclose(got, _reference_S(ex, ey), rel_tol=1e-12, abs_tol=1e-12)
        g2 = E.joint_discrepancy(E._Traced(ex), E._Traced(G.edge(grow(x, 1))))["S"]
        assert math.isclose(g2, _reference_S(ex, G.edge(grow(x, 1))), rel_tol=1e-12, abs_tol=1e-12)


# ======================= step 5 and 7: families, pruning, the minimum =======================
def test_families_from_the_bundle(arrays, fams):
    sizes = {t: (len(f["P"]), len(f["H"])) for t, f in fams.items()}
    assert sizes["T0"] == (0, 0) and sizes["TB"] == (2600, 50) and sizes["TD-4-2"] == (250, 250) and sizes["TA"][0] == sizes["TA"][1] > 0
    ta = fams["TA"]
    assert ta["P"].contours_id == ta["H"].contours_id and ta["P"] is not ta["H"]            # shared contours, separate labels
    assert fams["TB"]["P"].contours_id != fams["TB"]["H"].contours_id
    ell = float(ta["P"].levels[100])
    assert ta["P"].label(100) == T.level_label("TA", "P", ell) == ell ** 3 and ta["H"].label(100) == ell
    assert _refused(E.index_families, arrays, "TZ") and _refused(E.index_families, {}, "TA")
    assert _refused(E.IndexFamily, arrays["omega/TA.shared.f64"], "TA", "Q")


def test_pruning_intervals_are_the_cells_within_reach(fams):
    fam = fams["TB"]["P"]; om = fam.family.omega
    gen = RNG(5)
    for _ in range(60):
        t = int(gen.integers(0, 2)); i = int(gen.integers(0, L)); j = int(gen.integers(0, L))
        mid = (i + 0.5, float(j)) if t == 0 else (float(i), j + 0.5)
        vals = []
        for ci in range(L):
            for cj in range(L):
                di = min(abs(ci - mid[0]), L - abs(ci - mid[0])); dj = min(abs(cj - mid[1]), L - abs(cj - mid[1]))
                if 4 * (di * di + dj * dj) <= 25: vals.append(om[ci, cj])     # centre within ε + 0.5 = 2.5 cells, on exact quarters
        assert fam._lo[t, i, j] == min(vals) and fam._hi[t, i, j] == max(vals) and len(vals) in (20, 21, 22)


CORPUS = [  # (terrain, index, how the region is made from a level set of the index's own comparison array)
    ("TB", "H", "exact"), ("TB", "H", "grown 1"), ("TB", "H", "grown 2"), ("TB", "H", "grown 3"), ("TB", "H", "noisy"), ("TB", "H", "square"),
    ("TD-4-2", "P", "exact"), ("TD-4-2", "P", "grown 2"), ("TD-4-2", "P", "shrunk 3"), ("TD-4-2", "P", "noisy"), ("TD-4-2", "P", "square"),
    ("TA", "P", "noisy"),
]


def _corpus_counts(fam, how, gen):
    level = float(fam.levels[len(fam) // 2])
    base = fam.family.omega >= level
    if how == "exact": return flat_counts(base)
    if how.startswith("grown"): return flat_counts(grow(base, int(how.split()[1])))
    if how.startswith("shrunk"): return flat_counts(grow(base, -int(how.split()[1])))
    if how == "noisy": return noisy_counts(base, gen)
    sq = np.zeros((L, L), dtype=bool); sq[13:47, 31:72] = True               # a region that is no level set of any terrain
    return flat_counts(sq)


@pytest.mark.parametrize("case", CORPUS, ids=lambda c: f"{c[0]}.{c[1]}-{c[2].replace(' ', '')}")
def test_pruned_and_exhaustive_search_agree(fams, case):
    """§5.5 step 7: the pruning is exact for the decision. Wherever Δ ≤ ε the two searches also give the same Δ and
    the same level; where Δ > ε the pruned search's least S is descriptive and is not compared."""
    terrain, index, how = case
    fam = fams[terrain][index]
    counts = _corpus_counts(fam, how, RNG(6, CORPUS.index(case)))
    pruned = E.evaluate_map(counts, ONES, {index: fam})
    brute = E.evaluate_map(counts, ONES, {index: fam}, brute=True)
    assert pruned["informative"] and brute["informative"]
    p, b = pruned["indices"][index], brute["indices"][index]
    assert p["within"] == b["within"] and b["examined"] == len(fam) and p["examined"] <= len(fam)
    if b["within"]:
        assert (p["delta"], p["level_index"], p["lambda_star"]) == (b["delta"], b["level_index"], b["lambda_star"])
        assert p["delta"] <= E.EPSILON and p["lambda_star"] == fam.label(p["level_index"])
    else:
        assert p["delta"] is None and "lambda_star" not in p and p["status"] in ("no registered contour within epsilon", "no contour examined")
        assert b["least_S_examined"] > E.EPSILON
    expect = {"exact": True, "grown 1": True, "grown 2": True, "noisy": True, "square": False}
    if how in expect: assert b["within"] == expect[how], how


def test_the_contour_cache_changes_no_result(fams, monkeypatch):
    fam = fams["TD-4-2"]["P"]
    counts = _corpus_counts(fam, "noisy", RNG(6, 9))
    usual = E.evaluate_map(counts, ONES, {"P": fam})["indices"]["P"]
    monkeypatch.setattr(E, "CONTOUR_CACHE", 1)                                # every contour is traced again
    fresh = E.IndexFamily(fam.family.omega, "TD-4-2", "P")
    again = E.evaluate_map(counts, ONES, {"P": fresh})["indices"]["P"]
    assert len(fresh._cache) == 1 and usual["examined"] > 1
    assert (usual["within"], usual["delta"], usual["level_index"], usual["terms"]) == (again["within"], again["delta"], again["level_index"], again["terms"])


def test_the_family_minimum_against_an_independent_search(fams):
    """On the 50-level family, Δ and its level by an exhaustive search that shares nothing with the module's."""
    fam = fams["TB"]["H"]
    for how, k in (("grown 1", 0), ("grown 3", 1), ("noisy", 2)):
        counts = _corpus_counts(fam, how, RNG(7, k))
        mask, _ = E.occupied_region(counts, ONES)
        e = G.edge(mask)
        ref = [_reference_S(e, G.edge(fam.family.omega >= float(l))) for l in fam.levels]
        got = E.evaluate_map(counts, ONES, {"H": fam}, brute=True)["indices"]["H"]
        best = got["terms"]["S"]
        assert math.isclose(best, min(ref), rel_tol=1e-12, abs_tol=1e-12) and got["within"] == (min(ref) <= 2.0)
        assert math.isclose(ref[got["level_index"]], min(ref), rel_tol=1e-12, abs_tol=1e-12)


def test_the_lowest_level_keeps_a_tie():
    """Two contours at exactly the same S from the edge: the lower level is the fitted one, in both searches."""
    om = np.zeros((L, L)); om[:, 40:60] = 1.0; om[:, 42:58] = 2.0             # level 1: columns [40, 60); level 2: columns [42, 58)
    fam = E.IndexFamily(om, "TB", "H")
    mask = np.zeros((L, L), dtype=bool); mask[:50, 40:60] = True; mask[50:, 42:58] = True   # half of each
    Etr = E._Traced(G.edge(mask))
    s1, s2 = (E.joint_discrepancy(Etr, fam.contour(k))["S"] for k in (0, 1))
    assert s1 == s2 == 2.0 and len(fam) == 2
    for brute in (False, True):
        f = E.fit(Etr, fam, brute)
        assert f["level_index"] == 0 and f["level"] == 1.0 and f["within"] and f["delta"] == 2.0
    rev = E.IndexFamily(-om, "TB", "H")                                       # the same two contours listed in the other order
    f = E.fit(Etr, rev, True)
    assert f["level_index"] == 0 and f["level"] == -1.0 and f["delta"] == 2.0


def test_epsilon_is_inclusive_and_not_enlarged():
    om = np.zeros((L, L)); om[:, 30:70] = 1.0
    fam = E.IndexFamily(om, "TB", "H")
    at = E.evaluate_map(flat_counts(_strip(31, 71)), ONES, {"H": fam})        # 0.35 inside, 0.06 outside: the 3×3 mean keeps a straight strip
    assert at["region_cells"] == 40 * L and at["indices"]["H"]["delta"] == 1.0
    wide = E.evaluate_map(flat_counts(_strip(31, 71), 1000, 0), ONES, {"H": fam})   # 1 inside, 0 outside: two of nine neighbours reach θ
    assert wide["region_cells"] == 42 * L                                    # the estimator widens it by a cell each side (§5.5 step 3's remark)
    two = E.fit(E._Traced(G.edge(_strip(32, 72))), fam)
    three = E.fit(E._Traced(G.edge(_strip(33, 73))), fam)
    assert two["within"] and two["delta"] == 2.0 and not three["within"] and three["delta"] is None
    assert three["status"] in ("no registered contour within epsilon", "no contour examined")
    brute3 = E.fit(E._Traced(G.edge(_strip(33, 73))), fam, True)
    assert brute3["least_S_examined"] == 3.0 and "descriptive" in brute3["note"]


# ======================= step 9 =======================
def test_the_resampling_stream_is_the_declared_one():
    key = (7, 1, 0, 1500000)
    mult = E.resample_multiplicities(key)
    idx = np.random.Generator(np.random.PCG64(np.random.SeedSequence([2 ** 64 + 905, 7, 1, 0, 1500000]))).integers(0, 40, size=(1000, 40))
    want = np.stack([np.bincount(row, minlength=40) for row in idx])
    assert mult.shape == (1000, 40) and np.array_equal(mult, want) and (mult.sum(axis=1) == 40).all()
    assert np.array_equal(mult, E.resample_multiplicities(key)) and not np.array_equal(mult, E.resample_multiplicities((7, 1, 0, 1550000)))
    for bad in ((), [7], (7.0,), (True,), (-1,), (2 ** 64,), "7"): assert _refused(E.resample_multiplicities, bad)
    assert E.arm_level_key(7, "TA", "P", 1500000) == key and E.arm_level_key(7, "TD-4-4", "H", 750000) == (7, 7, 1, 750000)
    for bad in ((7, "T0", "H", 1500000), (7, "TA", "P", 1525000), (9920261112, "TA", "P", 1500000)): assert _refused(E.arm_level_key, *bad)


def test_result_table_at_its_boundaries():
    r = E.result_from_counts
    assert r(950, 0, 50) == ("compatible", None) and r(949, 1, 50) == ("unresolved", None) and r(0, 950, 50) == ("adverse", None)
    assert r(949, 0, 51) == ("not informative", "unstable edge") and r(0, 949, 51) == ("not informative", "unstable edge")
    assert r(1000, 0, 0) == ("compatible", None) and r(0, 1000, 0) == ("adverse", None) and r(500, 500, 0) == ("unresolved", None)
    assert r(950, 50, 0) == ("compatible", None) and r(50, 950, 0) == ("adverse", None) and r(0, 0, 1000) == ("not informative", "unstable edge")
    for bad in ((950, 0, 49), (951, 0, 50), (-1, 951, 50), (950.0, 0, 50), (True, 949, 50)): assert _refused(r, *bad)


def test_a_level_on_its_own_contour_is_compatible_for_both_indices(fams):
    fam = fams["TA"]
    level_index = len(fam["P"]) // 2
    counts = noisy_counts(fam["P"].family.omega >= float(fam["P"].levels[level_index]), RNG(8))
    rec = E.evaluate_level(counts, fam, E.arm_level_key(7, "TA", "P", 1500000))
    assert rec["point"]["informative"] and rec["resampled"] and rec["declared_stream"] and rec["stream_role"] == 2 ** 64 + 905
    p, h = rec["indices"]["P"], rec["indices"]["H"]
    for x in (p, h):
        assert x["result"] == "compatible" and x["n_C"] + x["n_A"] + x["n_I"] == 1000 and x["n_C"] >= 950
        assert (x["types"] == "C").sum() == x["n_C"] and np.isfinite(x["delta"][x["types"] == "C"]).all() and np.isnan(x["delta"][x["types"] != "C"]).all()
    assert np.array_equal(p["types"], h["types"]) and np.array_equal(p["level_index"], h["level_index"])   # one resampled map, one shared family
    ks = p["level_index"][p["types"] == "C"]
    ells = fam["P"].levels[ks]
    assert p["lambda_star_range"] == [float(ells.min()) ** 3, float(ells.max()) ** 3] and h["lambda_star_range"] == [float(ells.min()), float(ells.max())]
    again = E.evaluate_level(counts, fam, E.arm_level_key(7, "TA", "P", 1500000))
    assert np.array_equal(again["indices"]["P"]["types"], p["types"]) and np.array_equal(again["indices"]["P"]["delta"], p["delta"], equal_nan=True)


def test_a_region_off_the_family_is_adverse_and_tb_separates_its_indices(fams):
    fam = fams["TB"]
    own = fam["H"].family.omega >= float(fam["H"].levels[25])                 # a level set of the height index on TB: a strip along x
    rec = E.evaluate_level(flat_counts(own), fam, (7, 2, 1, 1500000))
    assert rec["indices"]["H"]["result"] == "compatible" and rec["indices"]["H"]["n_C"] == 1000
    assert rec["indices"]["P"]["result"] == "adverse" and rec["indices"]["P"]["n_A"] == 1000 and rec["indices"]["P"]["lambda_star_range"] is None
    assert rec["point"]["indices"]["P"]["within"] is False and "lambda_star" not in rec["point"]["indices"]["P"]


def test_pruned_and_exhaustive_search_agree_on_every_resample(fams):
    """§5.5 step 7 on resamples: over the 1,000 draws of a noisy level, the typed outcome of every draw, and Δ and the
    level of every compatible draw, are the same with and without pruning. The region is two cells off its contour
    in the population and its estimated edge moves between draws, so the draws fall on both sides of ε."""
    om = np.zeros((L, L)); om[:, 30:70] = 1.0; om[:, 45:55] = 2.0             # two contours, far apart: the strips [30, 70) and [45, 55)
    fam = {"H": E.IndexFamily(om, "TB", "H")}
    gen = RNG(9)
    counts = noisy_counts(_strip(28, 72), gen, inside=0.206, outside=0.194)   # two cells off the first contour, behind a very shallow step
    a = E.evaluate_level(counts, fam, (3,))["indices"]["H"]
    b = E.evaluate_level(counts, fam, (3,), brute=True)["indices"]["H"]
    assert np.array_equal(a["types"], b["types"]) and (a["n_C"], a["n_A"], a["n_I"]) == (b["n_C"], b["n_A"], b["n_I"])
    assert np.array_equal(a["delta"], b["delta"], equal_nan=True) and np.array_equal(a["level_index"], b["level_index"])
    assert a["n_C"] >= 100 and a["n_A"] >= 100 and a["result"] == "unresolved"   # both kinds of valid draw occurred, in number


def test_unavailable_states(fams):
    ta, t0 = fams["TA"], fams["T0"]
    empty = E.evaluate_level(np.full((S, L, L), 50, dtype=np.int64), ta, (1,))
    full = E.evaluate_level(np.full((S, L, L), 900, dtype=np.int64), ta, (1,))
    for rec in (empty, full):
        assert not rec["resampled"] and all(x == {"result": "not informative", "cause": "no edge at theta", "resampled": False} for x in rec["indices"].values())
    dot = np.zeros((L, L), dtype=bool); dot[20:29, 20:29] = True              # 81 cells; the 3×3 mean takes its corners: under the minimum either way
    small = E.evaluate_level(flat_counts(dot), ta, (1,))
    assert small["point"]["reason"] == "the region has under 100 cells" and small["indices"]["P"]["cause"] == "below the informative minimum"
    const = E.evaluate_level(flat_counts(_strip(20, 60)), t0, (1,))           # an informative edge, a constant index
    assert const["point"]["informative"] and not const["resampled"]
    assert all(x == {"result": "not informative", "cause": "no eligible contour", "resampled": False} for x in const["indices"].values())
    assert const["point"]["indices"]["P"]["status"] == "no eligible contour"
    mixed = E.evaluate_level(flat_counts(_strip(20, 60)), {"P": t0["P"], "H": fams["TB"]["H"]}, (1,))   # one empty family does not stop the other
    assert mixed["indices"]["P"]["cause"] == "no eligible contour" and mixed["indices"]["H"]["resampled"] and mixed["resampled"]


def test_invalid_draws_at_the_boundary_of_fifty(fams):
    """Constructed resample sets (§6.1): a region carried by eight seeds exists at p̃ = 0.20 with all 40 seeds and
    vanishes when one of the eight is dropped. Exactly 50 such rows keep the result; 51 make the edge unstable."""
    fam = fams["TB"]
    region = grow(fam["H"].family.omega >= float(fam["H"].levels[25]), 1)     # one cell larger: the 3×3 mean at a tie takes the rim back
    counts = np.zeros((S, L, L), dtype=np.int64); counts[:8, region] = 1000
    point = E.evaluate_map(counts, ONES, {"H": fam["H"]})
    assert point["informative"] and point["indices"]["H"]["within"]
    drop = ONES.copy(); drop[0] = 0; drop[39] = 2                             # seven of the eight carriers: p̃ = 0.175 at most
    assert E.evaluate_map(counts, drop, {"H": fam["H"]})["reason"].startswith("no edge at theta")
    for n_invalid, result, cause in ((50, "compatible", None), (51, "not informative", "unstable edge")):
        mult = np.tile(ONES, (1000, 1)); mult[:n_invalid] = drop
        rec = E.evaluate_level(counts, {"H": fam["H"]}, (1,), multiplicities=mult)
        x = rec["indices"]["H"]
        assert (x["n_C"], x["n_A"], x["n_I"]) == (1000 - n_invalid, 0, n_invalid) and (x["result"], x["cause"]) == (result, cause)
        assert rec["declared_stream"] is False and sum(rec["invalid_reasons"].values()) == n_invalid
        assert np.isnan(x["delta"][:n_invalid]).all() and (x["level_index"][:n_invalid] == -1).all()      # an invalid draw has no discrepancy
    bad = np.tile(ONES, (1000, 1)); bad[3, 0] = 2
    assert _refused(E.evaluate_level, counts, {"H": fam["H"]}, (1,), multiplicities=bad)
    assert _refused(E.evaluate_level, counts, {"H": fam["H"]}, (1,), multiplicities=bad[:999])
    assert _refused(E.evaluate_level, counts, {}, (1,)) and _refused(E.evaluate_level, counts, {"H": "x"}, (1,))


# ======================= nothing placed before M3 is touched =======================
PLACED = {  # LF identities at 6e731b8 (the M2 placement)
    "f9/__init__.py": "7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e",
    "f9/config.py": "5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb",
    "f9/terrain.py": "b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9",
    "f9/geometry.py": "122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971",
    "f9/family.py": "ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1",
    "f9/spectral.py": "b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3",
    "f9/identities.py": "0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577",
    "f9/streams.py": "5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06",
    "f9/dynamics.py": "34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e",
}
UNTOUCHED = "c80d494aea4e5e452b4a96536f0bc68515918e4ac8c7f37e84d66bad7c7a3289"   # root, e1, f8, gates: the digest test_f9_m1.py holds


def _sha_lf(path):
    with open(path, "rb") as fh: return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def test_everything_placed_before_m3_is_byte_unchanged():
    for rel, want in PLACED.items(): assert _sha_lf(os.path.join(PKG, *rel.split("/"))) == want, rel
    # The files this module added are present beside them. The folder is not required to hold nothing else: this line
    # first required exactly that and failed as soon as a later module was placed (repaired 2026-11-18).
    assert {r.split("/")[1] for r in PLACED} | set(["evaluator.py"]) <= {fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")}
    h = hashlib.sha256()
    for sub in ("", "e1", "f8", "gates"):
        d = os.path.join(PKG, sub)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"): h.update((sub + "/" + fn if sub else fn).encode()); h.update(bytes.fromhex(_sha_lf(os.path.join(d, fn))))
    assert h.hexdigest() == UNTOUCHED
