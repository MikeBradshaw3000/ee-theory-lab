"""tests/test_f9_m6.py — Flight 9 module M6, part 1: the map-statistic reports of contract §5.7 rows 1 to 3 and §1.3 (e)
(`f9/reports.py`).

No lattice run is made, no run record is read, and no report is computed on output of the rule. Every map and every
flicker record given to the reports is constructed here: named maps with stated answers, and random integer maps and
random binary sequences from a fixed generator. The only contract objects used are index geometry: the arms'
comparison arrays (for the binning) and TC's base u (for the patch sets). Each report is checked against a second
implementation written in the test from the contract's sentences."""
import hashlib
import itertools
import json
import math
import os
from fractions import Fraction

import numpy as np
import pytest

from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import dynamics as D
from mfa_instrument.f9 import evaluator as E
from mfa_instrument.f9 import reports as R
from mfa_instrument.f9 import terrain as T

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "mfa_instrument")
L, N, S, TAIL = C.F9_GRID, C.F9_N_CELLS, C.F9_N_SEEDS, C.F9_TAIL_TICKS
RNG = lambda *k: np.random.Generator(np.random.PCG64(np.random.SeedSequence([6, 6, 6] + list(k))))


def _refused(fn, *a, **k):
    try: fn(*a, **k)
    except (C.F9ConfigError, E.F9EvaluatorError): return True
    return False


def _fr(entry):
    n, d = entry["exact"].split("/")
    f = Fraction(int(n), int(d))
    assert entry["value"] == float(f)
    return f


def _random_counts(rng, structure=True):
    """Integer seed maps with a spatial profile, so that every band and both sides of every cut are populated."""
    if structure:
        i, j = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
        p = 0.5 * (1 + np.cos(2 * np.pi * (i - 30) / L)) * 0.5 * (1 + np.cos(2 * np.pi * (j - 60) / L))
    else:
        p = rng.uniform(0, 1, (L, L))
    return rng.binomial(TAIL, p, size=(S, L, L)).astype(np.int64)


# ======================= declaration =======================
def test_declaration_and_registered_values():
    assert R.verify_reports_declaration() == R.REPORTS_DECLARATION_SHA256_LITERAL == C.frozen_digest(R.REPORTS_DECLARATION)
    assert (R.OCC_DENOMINATOR, R.BOX_DENOMINATOR, R.BIN_MIN_CELLS) == (40_000, 360_000, 100)
    assert (R.CORE_MICRO, R.BAND_LOW_MICRO, R.CUT_MICRO) == (300_000, 100_000, 200_000) and R.CUT_MICRO == C.F9_THETA_MICRO
    assert R.FLICKER_BAND_EDGES_MICRO == (0, 100_000, 200_000, 300_000) and len(R.FLICKER_BAND_LABELS) == 4
    assert R.FLOOR_REFERENCE_LITERAL == "0.0523" and f"{D.stationary_pi1(C.F9_ETA0):.4f}" == "0.0523"          # §5.2, §5.7
    assert R.FLICKER_FLOOR_LITERALS == ((1, "0.0523"), (10, "0.1342"), (100, "0.6496"))                        # pre-probe declaration §6 point 3
    assert (R.TC_INSIDE_BUMP_MIN, R.TC_OUTSIDE_BUMP_MAX, R.TC_SET_SIZES) == (0.5, 0.05, (545, 7843))
    assert issubclass(R.F9ReportError, C.F9ConfigError)
    d = dict(R.REPORTS_DECLARATION)
    assert d["contract"] == C.F9_CONTRACT_SHA256 and d["flicker_windows"] == (1, 10, 100) and d["kind"] == "reported only; never scored"
    assert d["flicker_floor_references"] == R.FLICKER_FLOOR_LITERALS and d["flicker_floor_meaning"] == R.FLICKER_FLOOR_MEANING
    assert "Al <= As <= k Al" in d["flicker_record_checks"]


# ======================= constancy: the bins =======================
def _bins_by_loop(flat):
    """§5.7 row 1's binning, cell by cell: sort by ω (ties by index); a bin closes when it holds at least 100 cells and
    the next cell's ω differs from the last one's; a final bin under 100 is merged into the one before."""
    order = sorted(range(len(flat)), key=lambda i: (flat[i], i))
    bins, cur = [], []
    for pos, i in enumerate(order):
        cur.append(i)
        last_of_block = pos == len(order) - 1 or flat[order[pos + 1]] != flat[i]
        if last_of_block and len(cur) >= 100: bins.append(cur); cur = []
    if cur:
        if bins: bins[-1].extend(cur)
        else: bins.append(cur)
    return bins


def _check_bins(om):
    which, bins = R.constancy_bins(om)
    flat = om.ravel()
    ref = _bins_by_loop(flat.tolist())
    assert len(bins) == len(ref) and which.shape == (N,)
    for k, cells in enumerate(ref):
        assert np.array_equal(np.flatnonzero(which == k), np.sort(cells))
        assert bins[k] == {"cells": len(cells), "omega_min": float(flat[cells].min()), "omega_max": float(flat[cells].max())}
    assert sum(b["cells"] for b in bins) == N and all(b["cells"] >= 100 for b in bins)
    assert all(bins[k]["omega_max"] < bins[k + 1]["omega_min"] for k in range(len(bins) - 1))          # no ω value lies in two bins
    return bins


def test_bins_on_named_arrays():
    idx = np.arange(N, dtype=np.float64)
    bins = _check_bins(idx.reshape(L, L))                                   # all distinct: 100 bins of exactly 100
    assert len(bins) == 100 and {b["cells"] for b in bins} == {100}
    bins = _check_bins(np.full((L, L), 0.7))                                # one tie block
    assert bins == [{"cells": N, "omega_min": 0.7, "omega_max": 0.7}]
    bins = _check_bins((idx // 37).reshape(L, L))                           # blocks of 37 (270 of them) and one of 10
    assert len(bins) == 90 and [b["cells"] for b in bins] == [111] * 89 + [121]          # three blocks a bin; the short last bin is merged
    bins = _check_bins((idx // 100).reshape(L, L)[::-1].copy())             # blocks of exactly 100, in reversed cell order
    assert len(bins) == 100 and all(b["omega_min"] == b["omega_max"] == float(k) for k, b in enumerate(bins))
    bins = _check_bins(np.minimum(idx // 99, 100).reshape(L, L))            # 99, 99, ... : two blocks a bin (198), remainder merged
    assert bins[0]["cells"] == 198 and sum(b["cells"] for b in bins) == N
    om = idx.copy(); om[:9940] = np.arange(9940) // 70; om[9940:] = 1e6     # 71 bins of two blocks of 70, then a short block of 60
    bins = _check_bins(om.reshape(L, L))
    assert len(bins) == 71 and [b["cells"] for b in bins] == [140] * 70 + [200] and bins[-1]["omega_max"] == 1e6


def test_bins_on_random_tie_structures_and_on_the_contract_arms():
    rng = RNG(1)
    for trial in range(12):
        k = int(rng.integers(1, 400))
        _check_bins(rng.integers(0, k, N).astype(np.float64).reshape(L, L))
    for terrain, comp in C.F9_ARMS:
        bins = _check_bins(T.comparison_array(terrain, comp))
        assert 1 <= len(bins) <= 100
    assert len(R.constancy_bins(T.comparison_array("T0", "P"))[1]) == 1     # a flat index is one tie block


def test_bin_inputs_are_checked():
    om = T.comparison_array("TA", "P")
    assert _refused(R.constancy_bins, om.astype(np.float32)) and _refused(R.constancy_bins, om[:50]) and _refused(R.constancy_bins, om.ravel())
    bad = om.copy(); bad[3, 3] = np.nan
    assert _refused(R.constancy_bins, bad)
    bad[3, 3] = np.inf
    assert _refused(R.constancy_bins, bad)


# ======================= constancy: the variances =======================
def _constancy_float(counts, om):
    """V_within and V_noise from the contract's formulas in floating point, with the test's own binning."""
    bins = _bins_by_loop(om.ravel().tolist())
    X = counts.reshape(S, N) / float(TAIL)
    pbar = X.mean(axis=0)

    def P(x):
        out = x.copy()
        for cells in bins: out[cells] -= x[cells].mean()
        return out

    vw = float((P(pbar) ** 2).sum()) / N
    vn = sum(float((P(X[s] - pbar) ** 2).sum()) for s in range(S)) / (40 * 39 * N)
    return vw, vn


def _constancy_exact(counts, om):
    """The same in rationals, value by value (slow; used once)."""
    bins = _bins_by_loop(om.ravel().tolist())
    c = counts.reshape(S, N).tolist()
    t = [sum(c[s][i] for s in range(S)) for i in range(N)]

    def ss(x):
        tot = Fraction(0)
        for cells in bins:
            m = Fraction(sum(x[i] for i in cells), len(cells))
            tot += sum((x[i] - m) ** 2 for i in cells)
        return tot

    vw = ss(t) / (40_000 ** 2 * N)
    vn = sum(ss([40 * c[s][i] - t[i] for i in range(N)]) for s in range(S)) / (40_000 ** 2 * 40 * 39 * N)
    return vw, vn


def test_constancy_against_the_float_reference_on_random_maps():
    rng = RNG(2)
    for trial, arm in enumerate((("TA", "P"), ("TB", "H"), ("TC", "P"), ("TD-1-2", "P"), ("T0", "P"))):
        om = T.comparison_array(*arm)
        counts = _random_counts(rng, structure=trial % 2 == 0)
        rep = R.constancy(counts, om)
        vw, vn = _constancy_float(counts, om)
        assert abs(rep["V_within"]["value"] - vw) <= 1e-12 * max(vw, 1e-300) + 1e-18
        assert abs(rep["V_noise"]["value"] - vn) <= 1e-12 * max(vn, 1e-300) + 1e-18
        assert _fr(rep["V_within_minus_V_noise"]) == _fr(rep["V_within"]) - _fr(rep["V_noise"])
        assert rep["n_bins"] == len(rep["bins"]) == len(_bins_by_loop(om.ravel().tolist())) and rep["V_noise_is_zero"] is False


def test_constancy_is_exact():
    rng = RNG(3)
    om = T.comparison_array("TB", "P")
    counts = _random_counts(rng)
    rep = R.constancy(counts, om)
    vw, vn = _constancy_exact(counts, om)
    assert _fr(rep["V_within"]) == vw and _fr(rep["V_noise"]) == vn


def test_constancy_named_cases():
    om = (np.arange(N, dtype=np.float64) // 100).reshape(L, L)             # 100 bins: the rows
    row = np.arange(L, dtype=np.int64)
    # identical seeds, constant within each bin: both variances are zero, and the report says so
    counts = np.broadcast_to((row * 10)[None, :, None], (S, L, L)).copy()
    rep = R.constancy(counts, om)
    assert _fr(rep["V_within"]) == 0 and _fr(rep["V_noise"]) == 0 and rep["V_noise_is_zero"] is True
    # identical seeds, varying within each bin: X = j/1000 along a row; the within-row variance of 0..99 is (100² − 1)/12
    counts = np.broadcast_to(row[None, None, :], (S, L, L)).copy()
    rep = R.constancy(counts, om)
    assert _fr(rep["V_within"]) == Fraction(9999, 12) / 10 ** 6 and _fr(rep["V_noise"]) == 0 and rep["V_noise_is_zero"] is True
    # with ONE bin the same map has the same within variance (every cell's deviation from the grand mean is the same)
    assert _fr(R.constancy(counts, np.full((L, L), 0.5))["V_within"]) == Fraction(9999, 12) / 10 ** 6
    # seeds differ by a constant per seed: P removes it, so V_noise is zero although the seeds differ
    counts = np.broadcast_to(row[None, None, :], (S, L, L)) + np.arange(S)[:, None, None]
    rep = R.constancy(counts, om)
    assert _fr(rep["V_within"]) == Fraction(9999, 12) / 10 ** 6 and _fr(rep["V_noise"]) == 0
    # one seed differs in one cell by 1000 ticks (X differs by 1): Σ_s‖P(X_s − p̄)‖² = (39/40)·(99/100), by hand
    counts = np.zeros((S, L, L), dtype=np.int64); counts[7, 12, 34] = 1000
    rep = R.constancy(counts, om)
    assert _fr(rep["V_noise"]) == Fraction(39, 40) * Fraction(99, 100) / (40 * 39 * N)
    assert _fr(rep["V_within"]) == Fraction(1, 1600) * Fraction(99, 100) / N and rep["V_noise_is_zero"] is False
    assert sorted(rep) == sorted(["record", "kind", "bins", "n_bins", "V_within", "V_noise", "V_within_minus_V_noise", "V_noise_is_zero", "note",
                                  "declaration_sha256"]) and rep["kind"] == R.KIND                     # these and nothing else: no ratio is reported


def test_v_noise_estimates_the_seed_noise_of_the_mean():
    """Independent binomial seeds about a profile constant within bins: E[V_within] = E[V_noise], the difference is noise only."""
    rng = RNG(4)
    om = (np.arange(N, dtype=np.float64) // 100).reshape(L, L)
    p = np.broadcast_to(np.linspace(0.05, 0.95, L)[:, None], (L, L))
    counts = rng.binomial(TAIL, p, size=(S, L, L)).astype(np.int64)
    rep = R.constancy(counts, om)
    vw, vn = rep["V_within"]["value"], rep["V_noise"]["value"]
    expected = float(np.mean(p * (1 - p))) / TAIL / S * (99 / 100)
    assert abs(vn - expected) < 0.02 * expected and abs(vw - vn) < 0.1 * expected


# ======================= margins =======================
def _ptilde_by_padding(t):
    pad = np.pad(t, 1, mode="wrap")
    B = sum(pad[1 + di:1 + di + L, 1 + dj:1 + dj + L] for di in (-1, 0, 1) for dj in (-1, 0, 1))
    return B


def _margins_ref(counts):
    B = _ptilde_by_padding(counts.sum(axis=0)).ravel().tolist()
    p = [Fraction(b, 9 * 40_000) for b in B]
    out = {}
    for name, cut in (("cut_0.30", Fraction(3, 10)), ("cut_0.20", Fraction(1, 5))):
        core = sum(1 for x in p if x >= cut); band = sum(1 for x in p if Fraction(1, 10) <= x < cut)
        out[name] = (core, band)
    return out


def test_margins_against_the_rational_reference_on_random_maps():
    rng = RNG(5)
    for trial in range(4):
        counts = _random_counts(rng, structure=trial < 3)
        if trial == 1: counts = counts // 3
        rep = R.margins(counts)
        ref = _margins_ref(counts)
        for name in ("cut_0.30", "cut_0.20"):
            core, band = ref[name]
            assert (rep[name]["core"], rep[name]["band"]) == (core, band)
            assert core > 0 and _fr(rep[name]["band_over_core"]) == Fraction(band, core)
        assert rep["cut_0.20"]["core"] == int(E.occupied_region(counts, np.ones(S, dtype=np.int64))[0].sum())     # the evaluator's region at θ = 0.20
        assert rep["cut_0.30"]["core"] + rep["cut_0.30"]["band"] == rep["cut_0.20"]["core"] + rep["cut_0.20"]["band"]


def test_margins_named_cases():
    flat = lambda k: np.full((S, L, L), k, dtype=np.int64)
    r = R.margins(flat(300))                                              # p̃ = 0.30 exactly: ties are in the core
    assert r["cut_0.30"] == {"core": N, "band": 0, "band_over_core": {"value": 0.0, "exact": "0/1"}}
    r = R.margins(flat(299))
    assert r["cut_0.30"] == {"core": 0, "band": N, "band_over_core": "undefined"} and r["cut_0.20"]["core"] == N
    r = R.margins(flat(100))                                              # p̃ = 0.10 exactly: in the band
    assert (r["cut_0.30"]["band"], r["cut_0.20"]["band"]) == (N, N) and r["cut_0.20"]["band_over_core"] == "undefined"
    r = R.margins(flat(99))
    assert (r["cut_0.30"]["core"], r["cut_0.30"]["band"], r["cut_0.20"]["core"], r["cut_0.20"]["band"]) == (0, 0, 0, 0)
    r = R.margins(flat(200))
    assert (r["cut_0.20"]["core"], r["cut_0.20"]["band"], r["cut_0.30"]["band"]) == (N, 0, N)
    # a 10×10 block fully active in every seed, straddling the periodic seam. p̃ takes the values 1 (64 cells), 6/9 (32),
    # 4/9 (4), 3/9 (32), 2/9 (8), 1/9 (4): core at 0.30 = 132, band = 12; core at 0.20 = 140, band = 4.
    counts = np.zeros((S, L, L), dtype=np.int64)
    for i in range(95, 105):
        for j in range(-3, 7): counts[:, i % L, j % L] = TAIL
    r = R.margins(counts)
    assert (r["cut_0.30"]["core"], r["cut_0.30"]["band"], r["cut_0.20"]["core"], r["cut_0.20"]["band"]) == (132, 12, 140, 4)
    assert _fr(r["cut_0.30"]["band_over_core"]) == Fraction(12, 132) and _fr(r["cut_0.20"]["band_over_core"]) == Fraction(4, 140)
    # the same occupancy concentrated in one seed of 40 gives p̃ ≤ 1/40 everywhere: nothing
    counts[1:] = 0
    r = R.margins(counts)
    assert (r["cut_0.30"]["core"], r["cut_0.30"]["band"]) == (0, 0)
    assert r["floor_reference"] == {"literal": "0.0523", "pi_1": D.stationary_pi1(C.F9_ETA0)} and r["on"] == "p̃ at W = 1"


def test_margin_thresholds_are_decided_on_integers():
    """One tick either side of each cut, where a float p̃ could round the wrong way."""
    for micro, name, key in ((300_000, "cut_0.30", "core"), (200_000, "cut_0.20", "core"), (100_000, "cut_0.30", "band")):
        B_cut = micro * 360_000 // 10 ** 6                                # the box sum at the cut exactly: 108,000 / 72,000 / 36,000
        assert B_cut * 10 ** 6 == micro * 360_000
        base = B_cut // 360                                               # per-seed per-cell count giving the cut exactly
        counts = np.full((S, L, L), base, dtype=np.int64)
        assert R.margins(counts)[name][key] == N
        counts[0, 50, 50] -= 1                                            # nine cells' box sums fall one tick below the cut
        assert R.margins(counts)[name][key] == N - 9


# ======================= flicker =======================
def _sequences_to_windows(seq_iter):
    """Feed tail ticks through the placed `_Windows` (one run): {W: record}."""
    wins = {W: D._Windows(W, L) for W in C.F9_FLICKER_WINDOWS}
    for x in seq_iter:
        for w in wins.values(): w.add(x)
    assert all(w.n * w.W == TAIL for w in wins.values())
    return {W: {"A": w.A, "R0": w.R0, "first": w.first, "last": w.last} for W, w in wins.items()}


def _stack(per_seed):
    return {W: {k: np.stack([r[W][k] for r in per_seed]) for k in ("A", "R0", "first", "last")} for W in C.F9_FLICKER_WINDOWS}


@pytest.fixture(scope="module")
def flicker_case():
    """40 constructed runs of 1,000 tail ticks: each cell is a two-state chain with its own on and off probabilities, plus
    cells that are always active and cells that are never active. The sequences of 250 cells are kept for the direct check."""
    rng = RNG(6)
    p_on = rng.uniform(0.002, 0.6, (L, L)); p_off = rng.uniform(0.002, 0.6, (L, L))
    p_on[:, :40] *= 0.05                                                   # a low-occupancy region, so every band is populated
    always = np.zeros((L, L), dtype=bool); always[0, :] = True
    never = np.zeros((L, L), dtype=bool); never[1, :] = True
    keep = np.arange(0, N, 40)
    per_seed, kept = [], []
    for s in range(S):
        x = rng.random((L, L)) < p_on / (p_on + p_off)
        hist = np.empty((TAIL, keep.size), dtype=bool)

        def ticks():
            nonlocal x
            for t in range(TAIL):
                u = rng.random((L, L))
                x = np.where(x, u >= p_off, u < p_on)
                x = (x | always) & ~never
                hist[t] = x.ravel()[keep]
                yield x

        per_seed.append(_sequences_to_windows(ticks())); kept.append(hist)
    return _stack(per_seed), keep, np.stack(kept)


def _direct(seq, W):
    """One cell's record at width W from its tick sequence, by reading the windows and their inactive segments."""
    n = len(seq) // W
    win = [any(seq[k * W:(k + 1) * W]) for k in range(n)]
    lengths, run = [], 0
    for a in win:
        if not a: run += 1
        elif run: lengths.append(run); run = 0
    if run: lengths.append(run)
    mean = None if not lengths else Fraction(W * sum(lengths), len(lengths))          # mean inactive-segment length in ticks
    return {"A": sum(win), "R0": len(lengths), "first": win[0], "last": win[-1], "mean": mean, "censored": (not win[0]) or (not win[-1])}


def test_the_statistic_is_the_mean_inactive_segment_length(flicker_case):
    """W·(n − A)/R₀ on the placed parser's record equals the mean length, in ticks, of the observed inactive segments."""
    windows, keep, kept = flicker_case
    for W in C.F9_FLICKER_WINDOWS:
        n = TAIL // W
        checked = 0
        for s in range(0, S, 7):
            for c in range(0, keep.size, 3):
                i, j = divmod(int(keep[c]), L)
                d = _direct(kept[s, :, c].tolist(), W)
                rec = {k: windows[W][k][s, i, j] for k in ("A", "R0", "first", "last")}
                assert (int(rec["A"]), int(rec["R0"]), bool(rec["first"]), bool(rec["last"])) == (d["A"], d["R0"], d["first"], d["last"])
                if d["R0"]: assert Fraction(W * (n - d["A"]), d["R0"]) == d["mean"]
                else: assert d["mean"] is None and d["A"] == n
                checked += 1
        assert checked >= 400
    assert np.array_equal(windows[1]["A"][3].ravel()[keep], kept[3].sum(axis=0))                                       # at W = 1, A is the tail count


def _flicker_ref(windows):
    """§5.7 row 3 record by record, with rational band placement and numpy's quantile."""
    t = windows[1]["A"].sum(axis=0)
    out = []
    edges = [Fraction(0), Fraction(1, 10), Fraction(1, 5), Fraction(3, 10)]
    pbar = [Fraction(int(v), 40_000) for v in t.ravel()]
    band = np.array([max(b for b in range(4) if x >= edges[b]) for x in pbar]).reshape(L, L)
    for b in range(4):
        cells = band == b
        entry = {"cells": int(cells.sum()), "windows": {}}
        for W in C.F9_FLICKER_WINDOWS:
            n = TAIL // W
            A, R0 = windows[W]["A"][:, cells].ravel(), windows[W]["R0"][:, cells].ravel()
            f, l = windows[W]["first"][:, cells].ravel(), windows[W]["last"][:, cells].ravel()
            vals = np.array([W * (n - int(a)) / int(r) for a, r in zip(A, R0) if r > 0])
            q = [None] * 3 if vals.size == 0 else [float(v) for v in np.quantile(vals, [0.25, 0.5, 0.75])]
            entry["windows"][W] = {"records": int(A.size), "defined": int(vals.size), "undefined": int((R0 == 0).sum()),
                                   "censored": int(sum(1 for a, b_ in zip(f, l) if not a or not b_)), "q": q}
        out.append(entry)
    return out


def _compare(rep, ref):
    assert [b["band"] for b in rep["bands"]] == list(R.FLICKER_BAND_LABELS)
    for got, want in zip(rep["bands"], ref):
        assert got["cells"] == want["cells"] and sorted(got["windows"]) == [1, 10, 100]
        for W in C.F9_FLICKER_WINDOWS:
            g, w = got["windows"][W], want["windows"][W]
            assert (g["records"], g["defined"], g["undefined_no_inactive_segment"], g["possibly_censored"]) == (w["records"], w["defined"], w["undefined"], w["censored"])
            assert g["records"] == S * got["cells"] == g["defined"] + g["undefined_no_inactive_segment"]
            for a, b in zip((g["q25"], g["median"], g["q75"]), w["q"]):
                assert (a is None and b is None) or abs(a - b) <= 1e-12 * abs(b)


def test_flicker_against_the_reference(flicker_case):
    windows = flicker_case[0]
    rep = R.flicker(windows)
    _compare(rep, _flicker_ref(windows))
    assert sum(b["cells"] for b in rep["bands"]) == N and all(b["cells"] > 0 for b in rep["bands"])                    # every band is exercised
    top = rep["bands"][3]["windows"]
    assert all(top[W]["undefined_no_inactive_segment"] >= S * L for W in (1, 10, 100))                                 # the always-active row
    assert rep["bands"][0]["windows"][1]["possibly_censored"] >= S * L                                                 # the never-active row
    assert all(0 < b["windows"][W]["defined"] for b in rep["bands"][:3] for W in (1, 10))
    assert rep["statistic"] == "W·(n − A)/R₀ ticks" and rep["note"] == "recorded, not tested"
    _check_floor(rep)


def _check_floor(rep):
    """The W-specific floor references (pre-probe declaration §6 point 3), each with its own width, from the rule's constants."""
    fl = rep["floor_reference"]
    assert sorted(fl) == ["by_window", "meaning"] and list(fl["by_window"]) == [1, 10, 100]
    assert "occupancy of windows, not a duration in ticks" in fl["meaning"]
    a = 0.01; q = 1.0 - math.exp(-0.2); pi1 = a / (a + q)                     # §2.6, §2.7, §5.2, written out here
    for W, literal, six in ((1, "0.0523", "0.052282"), (10, "0.1342", "0.134244"), (100, "0.6496", "0.649601")):       # Appendix A.3
        e = fl["by_window"][W]
        assert sorted(e) == ["literal", "value"] and e["literal"] == literal
        assert abs(e["value"] - (1.0 - (1.0 - pi1) * (1.0 - a) ** (W - 1))) < 1e-12 and f"{e['value']:.4f}" == literal and f"{e['value']:.6f}" == six
    assert abs(fl["by_window"][1]["value"] - D.stationary_pi1(C.F9_ETA0)) < 1e-15
    for band in rep["bands"]:                                                 # the references enter no band entry
        for W in (1, 10, 100): assert not any("floor" in k for k in band["windows"][W])


def _uniform_windows(pattern):
    """Every cell and seed with the same tick pattern (a list of 1,000 booleans)."""
    one = {W: _direct(pattern, W) for W in C.F9_FLICKER_WINDOWS}
    full = lambda v, dt: np.full((S, L, L), v, dtype=dt)
    return {W: {"A": full(one[W]["A"], np.int64), "R0": full(one[W]["R0"], np.int64), "first": full(one[W]["first"], bool),
                "last": full(one[W]["last"], bool)} for W in C.F9_FLICKER_WINDOWS}


def test_flicker_named_cases():
    def only(rep, band):
        assert [b["cells"] for b in rep["bands"]] == [N if k == band else 0 for k in range(4)]
        for k, b in enumerate(rep["bands"]):
            if k != band:
                for W in (1, 10, 100):
                    assert b["windows"][W] == {"records": 0, "defined": 0, "undefined_no_inactive_segment": 0, "possibly_censored": 0,
                                               "q25": None, "median": None, "q75": None}
        return rep["bands"][band]["windows"]

    for pattern in ([True] * 1000, [False] * 1000):                         # three empty bands each; all-active has no defined record, all-inactive has every record defined
        _check_floor(R.flicker(_uniform_windows(pattern)))
    w = only(R.flicker(_uniform_windows([True] * 1000)), 3)                 # all active: undefined, never censored
    for W in (1, 10, 100):
        assert w[W] == {"records": S * N, "defined": 0, "undefined_no_inactive_segment": S * N, "possibly_censored": 0, "q25": None, "median": None, "q75": None}
    w = only(R.flicker(_uniform_windows([False] * 1000)), 0)                # never active: one segment of the whole tail, censored
    for W in (1, 10, 100):
        assert w[W] == {"records": S * N, "defined": S * N, "undefined_no_inactive_segment": 0, "possibly_censored": S * N, "q25": 1000.0, "median": 1000.0, "q75": 1000.0}
    # active on ticks 0..249 only (p̄ = 0.25, band [0.20, 0.30)): one inactive segment of 750 ticks, touching the end
    w = only(R.flicker(_uniform_windows([t < 250 for t in range(1000)])), 2)
    for W, length in ((1, 750.0), (10, 750.0), (100, 700.0)):                # at W = 100 the window 200..299 holds active ticks
        assert (w[W]["median"], w[W]["possibly_censored"], w[W]["defined"]) == (length, S * N, S * N)
    # active one tick in ten, on the tick 5 of each ten (p̄ = 0.10, band [0.10, 0.20)): at W = 1 segments of 5, 9 × 99 and 4
    # ticks (101 segments, 900 inactive ticks); at W = 10 and 100 every window is active
    w = only(R.flicker(_uniform_windows([t % 10 == 5 for t in range(1000)])), 1)
    assert w[1]["median"] == 900 / 101 and w[1]["possibly_censored"] == S * N and w[1]["defined"] == S * N
    assert all(w[W]["undefined_no_inactive_segment"] == S * N and w[W]["possibly_censored"] == 0 and w[W]["median"] is None for W in (10, 100))
    # band edges are ties upward: p̄ = 0.30 exactly is in [0.30, 1], and one tick fewer in one seed is in [0.20, 0.30)
    win = _uniform_windows([t < 300 for t in range(1000)])
    only(R.flicker(win), 3)
    win[1]["A"][0, 5, 5] -= 1
    assert [b["cells"] for b in R.flicker(win)["bands"]] == [0, 0, 1, N - 1]


def _stack_of(t1, t10, t100):
    """Every cell and seed with the same (A, R0, first, last) at each width."""
    full = lambda v, dt: np.full((S, L, L), v, dtype=dt)
    return {W: {"A": full(t[0], np.int64), "R0": full(t[1], np.int64), "first": full(t[2], bool), "last": full(t[3], bool)}
            for W, t in ((1, t1), (10, t10), (100, t100))}


def _tuple_of(seq, W):
    d = _direct(seq, W)
    return (d["A"], d["R0"], d["first"], d["last"])


def test_records_at_different_widths_must_be_of_one_sequence():
    """L2 M6 round 1, D1. The three widths describe one tick sequence; a stack that breaks one of the declared between-width
    relations is refused. The relations are necessary and not sufficient: L2's round-2 stack (20, 1, True, False) at W = 1
    and 10 with (2, 1, True, False) at W = 100 passes them and is the record of no sequence."""
    # L2's counterexample: never active at W = 1, always active at W = 10 and W = 100
    assert _refused(R.flicker, _stack_of((0, 1, False, False), (100, 0, True, True), (10, 0, True, True)))
    # L2's six targeted cases (W = 1, W = 10), with W = 100 all active; each tuple is possible at its own width
    cases = {"coarse A exceeds fine A": ((10, 1, True, False), (11, 1, True, False)),
             "fine A exceeds 10 x coarse A": ((111, 1, True, False), (11, 1, True, False)),
             "coarse R0 exceeds fine R0": ((20, 1, True, False), (20, 2, True, False)),
             "coarse Ra exceeds fine Ra": ((20, 2, False, False), (20, 2, True, False)),
             "first: fine active, coarse inactive": ((20, 1, True, False), (20, 1, False, True)),
             "last: fine active, coarse inactive": ((20, 1, False, True), (20, 1, True, False))}
    for name, (fine, coarse) in cases.items():
        assert _refused(R.flicker, _stack_of(fine, coarse, (10, 0, True, True))), name
    # the same relations between W = 10 and W = 100, and between W = 1 and W = 100, each beside records of one real sequence
    seq = [t < 200 or 500 <= t < 505 for t in range(1000)]                  # W=1 (205, 2, T, F); W=10 (21, 2, T, F); W=100 (3, 2, T, F)
    t1, t10, t100 = (_tuple_of(seq, W) for W in (1, 10, 100))
    assert (t1, t10, t100) == ((205, 2, True, False), (21, 2, True, False), (3, 2, True, False))
    assert R.flicker(_stack_of(t1, t10, t100))["record"] == "F9FlickerDistributions"
    for name, forged in (("A_10 above 10 x A_100", (2, 1, True, False)),
                         ("more segments at W = 100 than at W = 10", (3, 3, True, False)),
                         ("first_10 active, first_100 inactive", (3, 2, False, True))):
        A, R0, f, l = forged; Ra = R0 - 1 + f + l
        assert R0 <= 10 - A and (R0 == 0) == (A == 10) and 0 <= Ra <= A and (Ra == 0) == (A == 0), name      # possible at W = 100 alone
        assert _refused(R.flicker, _stack_of(t1, t10, forged)), name
    back = seq[::-1]                                                        # the mirror image: W=1 (205, 2, F, T); W=10 (21, 2, F, T)
    b1, b10, b100 = (_tuple_of(back, W) for W in (1, 10, 100))
    assert b100 == (3, 2, False, True) and R.flicker(_stack_of(b1, b10, b100))["record"] == "F9FlickerDistributions"
    assert _refused(R.flicker, _stack_of(b1, b10, (3, 2, True, False)))     # last_10 active, last_100 inactive
    short = [t < 5 for t in range(1000)]                                    # W=1 (5, 1, T, F); W=10 and W=100 (1, 1, T, F)
    s1, s10, s100 = (_tuple_of(short, W) for W in (1, 10, 100))
    assert (s10, s100) == ((1, 1, True, False), (1, 1, True, False)) and R.flicker(_stack_of(s1, s10, s100))["record"] == "F9FlickerDistributions"
    assert _refused(R.flicker, _stack_of(s1, s10, (2, 1, True, False)))     # A_100 = 2 above A_10 = 1
    assert _refused(R.flicker, _stack_of((1, 2, False, False), t10, t100))  # A_10 = 21 above A_1 = 1
    assert _refused(R.flicker, _stack_of((500, 2, True, False), t10, t100))  # A_1 = 500 above 10 x A_10 = 210
    # Necessary, not sufficient: (3, 1, True, True) is not this sequence's W = 100 record, but another sequence has these
    # three summaries, so the arrays alone cannot show the forgery and it is accepted. Binding records to runs is the runner's.
    assert R.flicker(_stack_of(t1, t10, (3, 1, True, True)))["record"] == "F9FlickerDistributions"


def test_the_single_width_relations_are_exactly_realizability():
    """Among all (A, R0, first, last) for n = 10 windows, the per-width relations accept exactly the tuples some sequence has.
    Each candidate is placed at W = 100 beside W = 1 and W = 10 records of a sequence that nests under it when it is possible."""
    realizable = {}
    for bits in itertools.product((False, True), repeat=10):
        realizable.setdefault(_tuple_of(list(bits), 1), bits)
    assert len(realizable) == 92
    accepted = 0
    for A, R0, f, l in itertools.product(range(11), range(11), (False, True), (False, True)):
        Ra = R0 - 1 + f + l
        by_rule = R0 <= 10 - A and (R0 == 0) == (A == 10) and 0 <= Ra <= A and (Ra == 0) == (A == 0)
        assert by_rule == ((A, R0, f, l) in realizable), (A, R0, f, l)
        if by_rule: accepted += 1
    assert accepted == 92
    for tup, bits in list(realizable.items())[::7]:                         # realizable tuples are accepted beside their own sequence
        seq = [b for b in bits for _ in range(100)]
        assert R.flicker(_stack_of(_tuple_of(seq, 1), _tuple_of(seq, 10), tup))["record"] == "F9FlickerDistributions"


def test_each_single_width_relation_refuses_on_its_own():
    """A forged W = 100 tuple that breaks ONE per-width relation and nests under real W = 1 and W = 10 records."""
    def case(active_ticks, forged):
        seq = [active_ticks(t) for t in range(1000)]
        stack = _stack_of(_tuple_of(seq, 1), _tuple_of(seq, 10), forged)
        fine = [stack[W] for W in (1, 10)]
        A, R0, f, l = forged; Ra = R0 - 1 + f + l
        for s, k in zip(fine, (100, 10)):                                   # the forgery passes every between-width relation
            As, R0s, fs, ls = (int(s["A"][0, 0, 0]), int(s["R0"][0, 0, 0]), bool(s["first"][0, 0, 0]), bool(s["last"][0, 0, 0]))
            assert A <= As <= k * A and R0 <= R0s and Ra <= R0s - 1 + fs + ls and (not fs or f) and (not ls or l)
        return _refused(R.flicker, stack)

    assert case(lambda t: t < 400 or t >= 900, (5, 0, True, True))          # R0 = 0 though A < n
    assert case(lambda t: t in (0, 200, 400, 600, 999), (2, 3, True, True))  # Ra = 4 active segments in A = 2 windows
    assert case(lambda t: 10 <= t < 990, (10, 0, False, False))             # Ra = -1
    assert case(lambda t: t % 200 < 100 or t >= 900, (8, 3, True, True))    # R0 = 3 inactive segments in n - A = 2 windows
    assert case(lambda t: 100 <= t < 400, (3, 1, False, False))             # Ra = 0 though A > 0


def test_quartiles_are_linear_between_order_statistics():
    assert R.quartiles(np.array([])) is None
    assert R.quartiles(np.array([4.0])) == [4.0, 4.0, 4.0]
    assert R.quartiles(np.array([1.0, 2.0])) == [1.25, 1.5, 1.75]
    assert R.quartiles(np.array([1.0, 2.0, 3.0, 4.0])) == [1.75, 2.5, 3.25]
    assert R.quartiles(np.array([1.0, 2.0, 3.0, 4.0, 10.0])) == [2.0, 3.0, 4.0]
    assert R.quartiles(np.array([0.0, 0.0, 8.0, 8.0, 8.0, 100.0])) == [2.0, 8.0, 8.0]
    rng = RNG(7)
    for n in list(range(1, 30)) + [101, 1000, 4001]:
        v = np.sort(rng.exponential(5.0, n))
        got, want = R.quartiles(v), np.quantile(v, [0.25, 0.5, 0.75])
        assert all(abs(a - b) <= 1e-12 * abs(b) for a, b in zip(got, want))


def test_flicker_inputs_are_checked(flicker_case):
    good = flicker_case[0]
    copy = lambda: {W: {k: v.copy() for k, v in good[W].items()} for W in good}
    assert R.flicker(copy())["record"] == "F9FlickerDistributions"
    assert _refused(R.flicker, None) and _refused(R.flicker, {1: good[1], 10: good[10]}) and _refused(R.flicker, {**good, 1000: good[1]})
    assert _refused(R.flicker, {True: good[1], 10: good[10], 100: good[100]})                 # True == 1, but it is not the key 1
    assert _refused(R.flicker, {"1": good[1], 10: good[10], 100: good[100]})
    for drop in ("A", "R0", "first", "last"):
        w = copy(); del w[10][drop]
        assert _refused(R.flicker, w)
    w = copy(); w[1]["extra"] = w[1]["A"]
    assert _refused(R.flicker, w)
    for key, bad in (("A", lambda a: a.astype(np.float64)), ("R0", lambda a: a.astype(np.float64)), ("first", lambda a: a.astype(np.int64)),
                     ("last", lambda a: a.astype(np.int8)), ("A", lambda a: a[:39]), ("R0", lambda a: a[:, :99]), ("first", lambda a: a[..., None])):
        w = copy(); w[10][key] = bad(w[10][key])
        assert _refused(R.flicker, w), key

    def broken(W, key, value, where=(0, 2, 2)):
        w = copy(); w[W][key][where] = value
        return _refused(R.flicker, w)

    assert broken(1, "A", -1) and broken(1, "A", 1001) and broken(10, "A", 101) and broken(100, "R0", 11) and broken(1, "R0", -1)
    a, r = int(good[1]["A"][0, 2, 2]), int(good[1]["R0"][0, 2, 2])
    assert 0 < a < 1000 and r > 0
    assert broken(1, "R0", 0)                                               # no inactive segment, yet not all active
    assert broken(1, "R0", 1000 - a + 1)                                    # more inactive segments than inactive windows
    assert broken(1, "A", 1000)                                             # all active, yet an inactive segment
    both = np.argwhere(good[1]["first"] & good[1]["last"] & (good[1]["A"] > 5) & (good[1]["A"] < 990))
    i = tuple(int(v) for v in both[0])                                      # a record that starts and ends active, and is not all active
    w = copy(); w[1]["R0"][i] = 0                                           # ... has an inactive segment
    assert _refused(R.flicker, w)
    w = copy(); w[1]["A"][i] = 2; w[1]["R0"][i] = 3                         # four active segments cannot fit in two active windows
    assert _refused(R.flicker, w)
    w = copy(); w[1]["A"][i] = 2; w[1]["R0"][i] = 1                         # possible at W = 1 alone, but not beside this cell's
    assert int(w[10]["A"][i]) > 2 and _refused(R.flicker, w)                #   W = 10 record (L2 M6 round 1, D1: round 1 accepted it)
    ends = _uniform_windows([t in (0, 999) for t in range(1000)])           # active at the first and the last tick only: one sequence
    assert all((int(ends[W]["A"][i]), int(ends[W]["R0"][i]), bool(ends[W]["first"][i]), bool(ends[W]["last"][i])) == (2, 1, True, True) for W in (1, 10, 100))
    assert R.flicker(ends)["record"] == "F9FlickerDistributions"            # (2, 1, True, True) at every width IS possible
    w = copy(); w[1]["A"][i] = 998; w[1]["R0"][i] = 3                       # three inactive segments in two inactive windows
    assert _refused(R.flicker, w)
    w = copy(); j = (0, 0, 3); w[1]["first"][j] = False; w[1]["last"][j] = False       # all active, yet inactive at both ends
    assert int(w[1]["A"][j]) == 1000 and _refused(R.flicker, w)
    w = copy(); i = (0, 0, 3)                                               # an always-active cell: first and last must be active
    assert int(w[1]["A"][i]) == 1000
    w[1]["first"][i] = False
    assert _refused(R.flicker, w)
    w = copy(); i = (0, 1, 3)                                               # a never-active cell cannot have an active first window
    assert int(w[1]["A"][i]) == 0
    w[1]["first"][i] = True
    assert _refused(R.flicker, w)
    w = copy(); w[1]["A"] = w[1]["A"].astype(np.uint64); w[1]["A"][0, 2, 2] = 2 ** 63 + 5      # refused in its own type, before conversion
    assert _refused(R.flicker, w)
    w = copy(); w[10]["A"] = w[10]["A"].astype(np.int16); w[10]["R0"] = w[10]["R0"].astype(np.uint8)       # narrower integer types are accepted
    assert R.flicker(w) == R.flicker(copy())


# ======================= TC's suppression contrast =======================
def _tc_bump():
    """TC's bump from the contract's formula (§3.2), written here with explicit loops."""
    out = np.empty((L, L))
    for i in range(L):
        for j in range(L):
            a = (1.0 + np.cos(2 * np.pi * (i / L - 0.5))) / 2.0
            b = (1.0 + np.cos(2 * np.pi * (j / L - 0.5))) / 2.0
            out[i, j] = a ** 4 * b ** 4
    return out


def test_tc_patch_sets_are_the_terrains_geometry():
    v, u, r = T.bases("TC")
    inside, outside = R.tc_patch_sets(u)
    bump = _tc_bump()
    assert np.max(np.abs(u - (0.9 - 0.85 * bump))) < 1e-14                  # the test's bump is the terrain's
    assert np.array_equal(inside, bump >= 0.5) and np.array_equal(outside, bump <= 0.05)
    assert (int(inside.sum()), int(outside.sum())) == (545, 7843) and not (inside & outside).any()
    assert float(np.min(np.abs(bump - 0.5))) > 1e-3 and float(np.min(np.abs(bump - 0.05))) > 4e-4      # no cell near either threshold
    assert inside[49, 49] and inside[50, 50] and outside[0, 0] and outside[99, 0]                      # the patch is at the centre
    for name in ("T0", "TA", "TB", "TD-4-4"):
        assert _refused(R.tc_patch_sets, T.bases(name)[1]), name
    assert _refused(R.tc_patch_sets, T.bases("TC")[0]) and _refused(R.tc_patch_sets, u.astype(np.float32)) and _refused(R.tc_patch_sets, u[:50])
    bad = u.copy(); bad[0, 0] = np.nan
    assert _refused(R.tc_patch_sets, bad)
    # The size check is a sanity check, not an authentication (L2 M6 round 1, D3): TC's u shifted by one cell has sets of
    # the same sizes and is ACCEPTED, with different sets. Binding u to the identity bundle is the runner's.
    si, so = R.tc_patch_sets(np.roll(u, 1, axis=0))
    assert (int(si.sum()), int(so.sum())) == (545, 7843) and (int((si != inside).sum()), int((so != outside).sum())) == (54, 102)


def test_suppression_contrast_cases():
    u = T.bases("TC")[1]
    inside, outside = R.tc_patch_sets(u)
    counts = np.zeros((S, L, L), dtype=np.int64); counts[:, inside] = TAIL
    r = R.suppression_contrast(counts, u)
    assert _fr(r["mean_inside"]) == 1 and _fr(r["mean_outside"]) == 0 and r["inside_over_outside"] == "undefined"
    counts = np.full((S, L, L), 123, dtype=np.int64)
    r = R.suppression_contrast(counts, u)
    assert _fr(r["mean_inside"]) == _fr(r["mean_outside"]) == Fraction(123, 1000) and _fr(r["inside_over_outside"]) == 1
    counts = np.zeros((S, L, L), dtype=np.int64); counts[:, inside] = 50; counts[:, outside] = 800; counts[:, ~inside & ~outside] = 1000
    r = R.suppression_contrast(counts, u)                                   # the cells in neither set do not enter
    assert _fr(r["mean_inside"]) == Fraction(1, 20) and _fr(r["mean_outside"]) == Fraction(4, 5) and _fr(r["inside_over_outside"]) == Fraction(1, 16)
    assert (r["inside_cells"], r["outside_cells"], r["terrain"], r["kind"]) == (545, 7843, "TC", R.KIND)
    rng = RNG(8)
    for _ in range(3):
        counts = _random_counts(rng, structure=False)
        r = R.suppression_contrast(counts, u)
        pbar = counts.mean(axis=0) / TAIL
        assert abs(r["mean_inside"]["value"] - pbar[inside].mean()) < 1e-12 and abs(r["mean_outside"]["value"] - pbar[outside].mean()) < 1e-12
        assert abs(r["inside_over_outside"]["value"] - pbar[inside].mean() / pbar[outside].mean()) < 1e-12
    assert _refused(R.suppression_contrast, counts, T.bases("TA")[1])


# ======================= inputs, records, earlier modules =======================
def test_map_inputs_are_checked():
    om = T.comparison_array("TA", "P"); u = T.bases("TC")[1]
    good = np.zeros((S, L, L), dtype=np.int64)
    for fn in (lambda c: R.constancy(c, om), R.margins, lambda c: R.suppression_contrast(c, u)):
        assert fn(good)["kind"] == R.KIND
        assert _refused(fn, good.astype(np.float64)) and _refused(fn, good[:39]) and _refused(fn, good[:, :99]) and _refused(fn, good[0])
        bad = good.copy(); bad[3, 4, 5] = 1001
        assert _refused(fn, bad)
        bad[3, 4, 5] = -1
        assert _refused(fn, bad)
        big = good.astype(np.uint64); big[0, 0, 0] = 2 ** 64 - 1
        assert _refused(fn, big)
        assert fn(good.astype(np.int16)) == fn(good)


def _leaves(x):
    if isinstance(x, dict):
        for k, v in x.items():
            assert type(k) in (str, int)
            yield from _leaves(v)
    elif isinstance(x, list):
        for v in x: yield from _leaves(v)
    else: yield x


def _str_keys(x):
    if isinstance(x, dict): return {str(k): _str_keys(v) for k, v in x.items()}
    return [_str_keys(v) for v in x] if isinstance(x, list) else x


def test_the_flicker_record_is_plain_data_with_integer_width_keys(flicker_case):
    """str, int, float, bool, None, list, dict. The per-width dicts are keyed by the integer W; a JSON writer makes those
    keys strings, so the record reloads equal to itself with its keys as strings. The persisted encoding is the runner's."""
    for rep in (R.flicker(flicker_case[0]), R.flicker(_uniform_windows([True] * 1000))):
        assert {type(v) for v in _leaves(rep)} <= {str, int, float, bool, type(None)}
        assert json.loads(json.dumps(rep)) == _str_keys(rep) != rep
        assert rep["kind"] == R.KIND and rep["declaration_sha256"] == R.REPORTS_DECLARATION_SHA256_LITERAL
        assert not any(k in rep for k in ("result", "tier", "cause", "pass", "verdict"))
    assert any(v is None for v in _leaves(R.flicker(_uniform_windows([True] * 1000))))        # None: a quantile that does not exist


def test_records_are_plain_data_and_reported_only():
    rng = RNG(9)
    counts = _random_counts(rng)
    recs = [R.constancy(counts, T.comparison_array("TC", "H")), R.margins(counts), R.suppression_contrast(counts, T.bases("TC")[1])]
    for rec in recs:
        assert json.loads(json.dumps(rec)) == rec                           # only str, int, float, bool, list, dict
        assert rec["kind"] == "reported only; never scored" and rec["declaration_sha256"] == R.REPORTS_DECLARATION_SHA256_LITERAL
        assert not any(k in rec for k in ("result", "tier", "cause", "pass", "verdict"))
    assert [r["record"] for r in recs] == ["F9ContourConstancy", "F9MeasuredMargins", "F9SuppressionContrast"]
    before = counts.copy()
    R.constancy(counts, T.comparison_array("TC", "H")); R.margins(counts)
    assert np.array_equal(counts, before)                                   # inputs are not modified


def test_the_reports_do_not_touch_scored_modules():
    """reports.py imports config, dynamics and evaluator only, and none of the scored modules imports it."""
    src = open(os.path.join(PKG, "f9", "reports.py"), encoding="utf-8").read()
    imports = [ln.strip() for ln in src.splitlines() if ln.startswith(("from ", "import "))]
    assert imports == ["from __future__ import annotations", "import math", "from fractions import Fraction", "from typing import Dict, List, Optional, Tuple",
                       "import numpy as np", "from . import config as C", "from . import dynamics as D", "from . import evaluator as E",
                       "from .config import F9ConfigError"]
    for fn in os.listdir(os.path.join(PKG, "f9")):
        if fn.endswith(".py") and fn != "reports.py":
            other = open(os.path.join(PKG, "f9", fn), encoding="utf-8").read()
            assert "import reports" not in other and "from .reports" not in other, fn


PLACED = {  # LF identities at 67aa10c (main after the M5 placement, the test repair and the governance records); evaluator.py as repaired for §7's cause precedence (L2 M6B round 1, D1)
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
}
UNTOUCHED = "c80d494aea4e5e452b4a96536f0bc68515918e4ac8c7f37e84d66bad7c7a3289"   # root, e1, f8, gates: the digest test_f9_m1.py holds


def _sha_lf(path):
    with open(path, "rb") as fh: return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def test_everything_placed_before_m6_is_byte_unchanged():
    for rel, want in PLACED.items(): assert _sha_lf(os.path.join(PKG, *rel.split("/"))) == want, rel
    # Subset form: the folder holds these and reports.py, and is not required to hold nothing else.
    assert {r.split("/")[1] for r in PLACED} | {"reports.py"} <= {fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")}
    h = hashlib.sha256()
    for sub in ("", "e1", "f8", "gates"):
        d = os.path.join(PKG, sub)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"): h.update((sub + "/" + fn if sub else fn).encode()); h.update(bytes.fromhex(_sha_lf(os.path.join(d, fn))))
    assert h.hexdigest() == UNTOUCHED
