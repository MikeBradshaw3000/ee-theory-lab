"""tests/test_f9_m2.py — Flight 9 module M2: the stream key and its codes; the per-cell-index hazard step against an
independent cell-by-cell implementation and against the placed Flight 8 scalar step (the reduction of contract §5.1);
the three declared starts; one run's record against an independent re-simulation and the probe's window formula; the
serialized record's round trip, its refusals, and replay; and that nothing placed before M2 is touched.

Every run here uses a TEST master (below streams.TEST_MASTER_LIMIT). The tests assert the mechanics of the rule and of
the record. They assert nothing about where activity is, and compute nothing against an index contour.

Platform policy. A trajectory passes through exp. It is compared with a re-simulation on the same machine, never with
a stored hash."""
import ast
import dataclasses
import hashlib
import json
import math
import os
import struct

import numpy as np
import pytest

from mfa_instrument.f8 import dynamics as F8D
from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import dynamics as D
from mfa_instrument.f9 import identities as I
from mfa_instrument.f9 import spectral as S
from mfa_instrument.f9 import streams as R

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "mfa_instrument")
L, N, T_, TAIL = C.F9_GRID, C.F9_N_CELLS, C.F9_TICKS, C.F9_TAIL_TICKS
M = 7                                                                         # a test master


def _refused(fn, *a, **k):
    try: fn(*a, **k)
    except (C.F9ConfigError, D.F9DynamicsError): return True
    return False


# ======================= streams =======================
def test_stream_declaration_verifies_and_covers_the_frozen_configuration():
    assert R.verify_stream_declaration() == R.STREAM_DECLARATION_SHA256_LITERAL == C.frozen_digest(R.STREAM_DECLARATION)
    t = R.code_tables()
    assert list(t["terrain"]) == list(C.F9_TERRAINS) and list(t["terrain"].values()) == list(range(8))
    assert t["composition"] == {"P": 0, "H": 1} and t["object"] == {"realization": 0, "skeleton": 1}
    assert t["initialization"] == {"stationary_floor": 0, "all_active": 1, "low": 2}
    assert R.RHO0_LOW_MICRO == 20000 and int(round(N * R.RHO0_LOW_MICRO / C.MICRO_UNITS)) == 200


def test_a_changed_stream_literal_fails_the_preflight(monkeypatch):
    monkeypatch.setattr(R, "STREAM_DECLARATION", R.STREAM_DECLARATION[:-1] + (("seed_rule", "other"),))
    assert _refused(R.verify_stream_declaration)
    monkeypatch.undo()
    monkeypatch.setattr(R, "STREAM_DECLARATION_SHA256_LITERAL", "PLACEHOLDER")
    assert _refused(R.verify_stream_declaration)
    monkeypatch.undo()
    monkeypatch.setattr(R, "TERRAIN_CODES", R.TERRAIN_CODES[1:] + R.TERRAIN_CODES[:1])
    assert _refused(R.verify_stream_declaration)


def test_the_key_is_the_contracts_tuple_in_order():
    assert R.stream_key(M, "T0", "P", "realization", "stationary_floor", 750000, 0) == (7, 0, 0, 0, 0, 750000, 0)
    assert R.stream_key(123456789012, "TD-4-4", "H", "skeleton", "all_active", 3000000, 39) == (123456789012, 7, 1, 1, 1, 3000000, 39)
    assert R.stream_key(M, "T0", "P", "skeleton", "low", 1050000, 5) == (7, 0, 0, 1, 2, 1050000, 5)


def _all_runs(master):
    for terrain, comp in C.F9_ARMS:
        for obj, init in (("realization", "stationary_floor"), ("skeleton", "all_active")) + ((("skeleton", "low"),) if terrain == "T0" else ()):
            for lv in C.F9_LEVELS_MICRO:
                for s in range(C.F9_N_SEEDS):
                    yield (master, terrain, comp, obj, init, lv, s)


def test_every_declared_run_has_its_own_key():
    keys = [R.stream_key(*r) for r in _all_runs(M)]
    assert len(keys) == 15 * 2 * 25 * 40 + 25 * 40 == 31000 and len(set(keys)) == len(keys)
    assert not set(keys) & {R.stream_key(*r) for r in _all_runs(M + 1)}


def test_undeclared_runs_and_masters_are_refused():
    ok = (M, "TA", "P", "realization", "stationary_floor", 1000000, 0)
    R.check_run_identity(*ok)
    bad = [
        (M, "T0", "H") + ok[3:],                                              # T0 has no H arm
        (M, "TZ", "P") + ok[3:], (M, "TA", "Q") + ok[3:],
        ok[:3] + ("null", "stationary_floor", 1000000, 0),
        ok[:3] + ("realization", "all_active", 1000000, 0), ok[:3] + ("skeleton", "stationary_floor", 1000000, 0),
        ok[:3] + ("skeleton", "low", 1000000, 0),                             # the low start is T0's only
        ok[:5] + (1025000, 0), ok[:5] + (1000000.0, 0), ok[:5] + (True, 0),
        ok[:6] + (40,), ok[:6] + (-1,), ok[:6] + (True,), ok[:6] + (0.0,),
    ]
    for b in bad: assert _refused(R.check_run_identity, *b), b
    for m in (0, -1, True, 7.0, "7", None, 2 ** 64): assert _refused(R.check_master, m), m
    assert R.check_master(2 ** 64 - 1) == 2 ** 64 - 1
    assert R.master_class(1) == R.master_class(999_999) == "test" and R.master_class(1_000_000) == "stage"
    for key in ((7, 0, 0, 0, 0, 750000), (7, 9, 0, 0, 0, 750000, 0), (7, 0, 0, 0, 1, 750000, 0), [7, 0, 0, 0, 0, 750000, 0], (7, 0, 0, 0, 0, 750000, 40)):
        assert _refused(R.generator_from_key, key) and _refused(R.init_pattern_generator, key)


# L2 M2 round 1, R2. Every master an earlier instrument declared, read from the PLACED SOURCE and not from streams.py:
# (file under mfa_instrument, the integer literals that must appear in it, the masters they give).
EARLIER_MASTERS = (
    ("e1/config.py", (20260917,), (20260917,)),
    ("e1/null.py", (202609171, 202609172), (202609171, 202609172)),
    ("e1/audit.py", (202609221, 202609222, 202609223), (202609221, 202609222, 202609223)),
    ("e1/projection.py", (202609301, 202609302, 202609303, 202609304), (202609301, 202609302, 202609303, 202609304)),
    ("f8/config.py", (20261026, 120261026, 920261102), (20261026, 120261026, 920261102)),
    ("f8/null.py", (220261026, 320261027), (220261026, 320261027)),
    ("f8/closure.py", (420261028,), (420261028,)),
    ("f8/evaluator.py", (520261028,), (520261028,)),
    ("f8/audit.py", (20261102, 6, 7, 8, 202609221, 202609222, 202609223), (620261102, 720261102, 820261102)),   # prefix·10^8 + placement date
)
PROBE_SOURCE = os.path.join(HERE, "..", "..", "design", "flight9", "probe", "f9_probe.py")
PROBE_MASTER = 9920261112


def _int_literals(path):
    with open(path, encoding="utf-8") as fh: tree = ast.parse(fh.read())
    return {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and type(n.value) is int}


def test_every_earlier_master_is_refused_l2_m2_round1_r2():
    """L2 M2 round 1, R2: the exclusion is checked against the placed source of E1 and Flight 8 and the probe's source,
    not against the list under test. Refusal is required of every public path to a stream."""
    grounded = []
    for rel, literals, masters in EARLIER_MASTERS:
        found = _int_literals(os.path.join(PKG, *rel.split("/")))
        assert set(literals) <= found, rel
        grounded += list(masters)
    assert (620261102, 720261102, 820261102) == tuple(p * 10 ** 8 + 20261102 for p in (6, 7, 8))
    assert PROBE_MASTER in _int_literals(PROBE_SOURCE)
    grounded.append(PROBE_MASTER)
    assert len(grounded) == len(set(grounded)) == 21 and set(grounded) == set(R.RETIRED_MASTERS)
    assert {202609221, 202609222, 202609223} <= set(R.RETIRED_MASTERS)        # the three L2 found accepted
    rest = ("T0", "P", "realization", "stationary_floor", 1500000, 0)
    for m in grounded:
        assert _refused(R.check_master, m) and _refused(R.master_class, m), m
        assert _refused(R.check_run_identity, m, *rest) and _refused(R.stream_key, m, *rest), m
        assert _refused(D.F9RunSpec(m, *rest).check) and _refused(lambda: D.F9RunSpec(m, *rest).stream_key), m
        assert _refused(R.generator_from_key, (m, 0, 0, 0, 0, 1500000, 0)) and _refused(R.init_pattern_generator, (m, 0, 0, 0, 0, 1500000, 0)), m
    for fresh in (M, 999_999, 1_000_000, 202609224, 9920261113, 2 ** 64 - 1):  # controls: neighbours of retired values are masters
        assert R.check_master(fresh) == fresh and R.stream_key(fresh, *rest)[0] == fresh


def test_the_stream_is_pcg64_of_the_seed_sequence_of_the_key():
    key = R.stream_key(M, "TB", "H", "realization", "stationary_floor", 1250000, 3)
    raw = np.random.PCG64(np.random.SeedSequence([7, 2, 1, 0, 0, 1250000, 3])).random_raw(6)
    want = (raw >> np.uint64(11)).astype(np.float64) * 2.0 ** -53                # the 53-bit uniform of each raw word
    assert np.array_equal(R.generator_from_key(key).random(6), want)
    assert np.array_equal(R.generator_from_key(key).random((2, 3)).ravel(), want)   # a full-grid draw is the same words in C order
    other = R.init_pattern_generator(key).random(6)
    raw2 = np.random.PCG64(np.random.SeedSequence([7, 2, 1, 0, 0, 1250000, 3, 1])).random_raw(6)
    assert np.array_equal(other, (raw2 >> np.uint64(11)).astype(np.float64) * 2.0 ** -53) and not np.array_equal(other, want)


# ======================= the rule =======================
def _loop_step(x, u, eta, g, lam, mu):
    """Cell by cell, from the contract's sentences: no numpy arithmetic, no shared code."""
    n = x.shape[0]
    q = 1.0 - math.exp(-mu)
    out = np.zeros_like(x); margin = np.inf
    for i in range(n):
        for j in range(n):
            if x[i, j]:
                out[i, j] = u[i, j] >= q; margin = min(margin, abs(u[i, j] - q))
            else:
                k = sum(int(x[(i + di) % n, (j + dj) % n]) for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di, dj) != (0, 0))
                p = 1.0 - math.exp(-(eta + g * lam[i, j] * (k / 8.0)))
                out[i, j] = u[i, j] < p; margin = min(margin, abs(u[i, j] - p))
    return out, margin


@pytest.mark.parametrize("eta", [0.0, C.F9_ETA0])
def test_step_is_the_written_rule_cell_by_cell(eta):
    gen = np.random.Generator(np.random.PCG64(np.random.SeedSequence([4, 4, int(eta > 0)])))
    n = 17
    lam = 0.05 + 0.9 * gen.random((n, n))
    x = gen.random((n, n)) < 0.35
    for _ in range(40):
        u = gen.random((n, n))
        want, margin = _loop_step(x, u, eta, 1.7, lam, C.F9_MU)
        assert margin > 1e-12                                                 # no decision sits within rounding of its threshold
        got = D.step(x, u, eta_floor=eta, g=1.7, lam=lam)
        assert got.dtype == bool and np.array_equal(got, want)
        x = got


def test_the_step_reads_the_state_at_t_only():
    """Two-phase advance: a cell's new neighbours do not enter its own tick. A lone active cell with deactivation
    certain (u = 0) and its neighbours' activation certain (u = 0 < P) gives exactly the eight neighbours next."""
    x = np.zeros((9, 9), dtype=bool); x[4, 4] = True
    nxt = D.step(x, np.zeros((9, 9)), eta_floor=0.0, g=5.0, lam=np.ones((9, 9)))
    want = np.zeros((9, 9), dtype=bool); want[3:6, 3:6] = True; want[4, 4] = False
    assert np.array_equal(nxt, want)
    wrap = np.zeros((9, 9), dtype=bool); wrap[0, 0] = True                    # periodic
    nxt = D.step(wrap, np.zeros((9, 9)), eta_floor=0.0, g=5.0, lam=np.ones((9, 9)))
    assert nxt.sum() == 8 and nxt[8, 8] and nxt[0, 8] and nxt[8, 0] and nxt[1, 1] and not nxt[0, 0]


def test_floor_is_not_gated_and_zero_floor_is_absorbing():
    empty = np.zeros((L, L), dtype=bool)
    lam = np.full((L, L), 1e-300)                                            # an index of essentially zero does not gate the floor
    u = np.random.Generator(np.random.PCG64(5)).random((L, L))
    a = 1.0 - math.exp(-C.F9_ETA0)
    assert np.array_equal(D.step(empty, u, eta_floor=C.F9_ETA0, g=3.0, lam=lam), u < a)
    assert not D.step(empty, u, eta_floor=0.0, g=3.0, lam=np.ones((L, L))).any()
    assert D.stationary_pi1(C.F9_ETA0) == pytest.approx(0.052282, abs=5e-7) and D.stationary_pi1(0.0) == 0.0
    assert a == pytest.approx(0.01, abs=1e-15)


def test_reduction_to_the_placed_flight8_step():
    out = D.reduction_check()
    assert out["reduction_equal"] is True and out["unequal_cases"] == [] and out["cases"] == len(D.REDUCTION_CASES) == 12
    assert out["ticks_compared"] == 12 * D.REDUCTION_TICKS and out["t0_levels_included"] is False
    with open(os.path.join(PKG, "f8", "dynamics.py"), "rb") as fh: lf = hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()
    assert out["f8_dynamics_sha256_lf"] == lf == "cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b"


def test_reduction_check_can_fail(monkeypatch):
    """The comparison is not vacuous: a step that differs in one cell at one tick is reported, with its case."""
    real = D.step
    calls = {"n": 0}
    def off_by_one(x, u, **k):
        out = real(x, u, **k); calls["n"] += 1
        if calls["n"] == 3 * D.REDUCTION_TICKS + 5: out = out.copy(); out[0, 0] = ~out[0, 0]
        return out
    monkeypatch.setattr(D, "step", off_by_one)
    out = D.reduction_check()
    assert out["reduction_equal"] is False and out["unequal_cases"] == [3]


# ======================= runs =======================
@pytest.fixture(scope="module")
def bundle(tmp_path_factory):
    d = str(tmp_path_factory.mktemp("f9_identities_m2"))
    I.write_bundle(d)
    return I.load_bundle(d)


@pytest.fixture(scope="module")
def arms(bundle):
    rec, arr = bundle
    return {a: D.arm_context(rec, arr, *a) for a in (("T0", "P"), ("TB", "H"), ("TC", "P"))}


def test_arm_context_takes_the_stored_index_and_the_records_gain(bundle):
    rec, arr = bundle
    for terrain, comp in C.F9_ARMS:
        a = D.arm_context(rec, arr, terrain, comp)
        e = rec["arms"][f"{terrain}.{comp}"]
        assert (a.index_sha256, a.spr, a.g_spec) == (e["index_sha256"], e["spr"], e["g_spec"]) and a.identity_record_sha256 == I.record_identity(rec)
        assert a.lam.dtype == np.float64 and a.lam.shape == (L, L) and not a.lam.flags.writeable
        with pytest.raises(ValueError): a.lam[0, 0] = 1.0
    assert np.all(D.arm_context(rec, arr, "T0", "P").lam == 0.8 * 0.8 * 0.8)
    assert _refused(D.arm_context, rec, arr, "T0", "H") and _refused(D.arm_context, rec, {}, "TA", "P")
    swapped = dict(arr); swapped["bases/TA.v.f64"] = arr["bases/TC.v.f64"]
    assert _refused(D.arm_context, rec, swapped, "TA", "P")                   # the index is not the one the record states
    bad = json.loads(json.dumps(rec)); bad["arms"]["TA.P"]["g_spec"] *= 2.0
    assert _refused(D.arm_context, bad, arr, "TA", "P")
    assert D.reduction_check(rec["arms"]["T0.P"]["g_spec"])["reduction_equal"] is True


def _resimulate(spec, arm):
    """An independent driver: the same stream and step, the whole tail kept, the window record by the probe's formula."""
    gen = R.generator_from_key(spec.stream_key)
    eta = C.F9_ETA0 if spec.obj == "realization" else 0.0
    if spec.init == "stationary_floor":
        a = 1.0 - math.exp(-eta); x = gen.random((L, L)) < a / (a + (1.0 - math.exp(-C.F9_MU)))
    elif spec.init == "all_active": x = np.ones((L, L), dtype=bool)
    else:
        x = np.zeros(N, dtype=bool); x[R.init_pattern_generator(spec.stream_key).choice(N, size=200, replace=False)] = True; x = x.reshape(L, L)
    g = (spec.level_micro / 1_000_000) * arm.g_spec
    counts = [int(x.sum())]; tail = np.zeros((TAIL, L, L), dtype=bool); dead = False
    for t in range(1, T_ + 1):
        if not dead:
            x = D.step(x, gen.random((L, L)), eta_floor=eta, g=g, lam=arm.lam)
            dead = eta == 0.0 and not x.any()
        counts.append(int(x.sum()))
        if t > T_ - TAIL: tail[t - (T_ - TAIL) - 1] = x
    out = {}
    for W in (1, 10, 100):
        n = TAIL // W
        yw = tail.reshape(n, W, L, L).any(axis=1)
        A = yw.sum(axis=0)
        K = (yw[1:] != yw[:-1]).sum(axis=0)
        first = yw[0].astype(int); last = yw[-1].astype(int)
        R0 = np.where(A == n, 0, (K + 2 - first - last) // 2)
        out[W] = (A, R0, yw[0], yw[-1])
    return np.array(counts), out, tail


RUNS = [
    (("T0", "P"), "realization", "stationary_floor", 1500000, 0),
    (("T0", "P"), "skeleton", "all_active", 750000, 1),
    (("T0", "P"), "skeleton", "low", 2000000, 2),
    (("TB", "H"), "skeleton", "all_active", 1000000, 3),
    (("TC", "P"), "realization", "stationary_floor", 1000000, 39),
]


@pytest.fixture(scope="module")
def results(arms):
    out = {}
    for arm, obj, init, lv, s in RUNS:
        spec = D.F9RunSpec(M, arm[0], arm[1], obj, init, lv, s)
        out[(arm, obj, init, lv, s)] = (spec, D.run(spec, arms[arm]))
    return out


@pytest.mark.parametrize("case", RUNS, ids=lambda c: f"{c[0][0]}.{c[0][1]}-{c[1]}-{c[2]}-{c[3]}")
def test_a_runs_record_is_the_rule_re_simulated(results, arms, case):
    spec, res = results[case]
    counts, wins, tail = _resimulate(spec, arms[case[0]])
    assert np.array_equal(res.counts, counts) and res.counts.shape == (T_ + 1,)
    assert res.g == S.gain(spec.level_micro, arms[case[0]].g_spec)
    for W in (1, 10, 100):
        A, R0, first, last = wins[W]
        w = res.windows[W]
        assert np.array_equal(w["A"], A) and np.array_equal(w["R0"], R0) and np.array_equal(w["first"], first) and np.array_equal(w["last"], last)
    assert np.array_equal(res.windows[1]["A"], tail.sum(axis=0))            # W = 1: active tail ticks per cell
    assert res.survival == bool((counts[T_ - TAIL + 1:] > 0).all()) and res.tail_active_sum == int(tail.sum())
    if spec.obj == "realization":
        assert res.extinction_tick is None and res.ticks_advanced == T_ and res.draws_consumed == T_ + 1
    else:
        zeros = np.flatnonzero(counts == 0)
        assert res.extinction_tick == (int(zeros[0]) if zeros.size else None)
        assert res.ticks_advanced == res.draws_consumed == (T_ if res.extinction_tick is None else res.extinction_tick)
        assert counts[0] == (N if spec.init == "all_active" else 200)


def test_the_test_runs_cover_extinction_and_survival(results):
    """The mechanics above are exercised on both branches: at least one skeleton run goes extinct and one does not."""
    sk = [r for (a, obj, *_), (s, r) in results.items() if obj == "skeleton"]
    assert any(r.extinction_tick is not None for r in sk) and any(r.extinction_tick is None for r in sk)
    for r in sk:
        if r.extinction_tick is not None:
            assert not r.counts[r.extinction_tick:].any() and not r.survival
            if r.extinction_tick <= T_ - TAIL:
                for W in (1, 10, 100):
                    w = r.windows[W]
                    assert not w["A"].any() and np.all(w["R0"] == 1) and not w["first"].any() and not w["last"].any()


def test_window_record_on_fixed_sequences():
    """The accumulator against hand-counted cells: (sequence of 20 ticks) -> A, R0, first, last at W = 1 and W = 5."""
    seqs = {
        "all_on": [1] * 20, "all_off": [0] * 20,
        "on_then_off": [1] * 7 + [0] * 13, "off_then_on": [0] * 13 + [1] * 7,
        "two_gaps": [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "ends_off": [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        "one_tick": [0] * 12 + [1] + [0] * 7,
    }
    want = {  # name: ((A, R0, first, last) at W=1, the same at W=5)
        "all_on": ((20, 0, 1, 1), (4, 0, 1, 1)), "all_off": ((0, 1, 0, 0), (0, 1, 0, 0)),
        "on_then_off": ((7, 1, 1, 0), (2, 1, 1, 0)), "off_then_on": ((7, 1, 0, 1), (2, 1, 0, 1)),
        "two_gaps": ((15, 2, 1, 1), (4, 0, 1, 1)), "ends_off": ((18, 2, 0, 0), (4, 0, 1, 1)),
        "one_tick": ((1, 2, 0, 0), (1, 2, 0, 0)),
    }
    names = sorted(seqs)
    for W, col in ((1, 0), (5, 1)):
        acc = D._Windows(W, len(names))
        for t in range(20):
            x = np.zeros((len(names), len(names)), dtype=bool)
            x[0, :] = [bool(seqs[n][t]) for n in names]
            acc.add(x)
        assert acc.n == 20 // W
        for j, n in enumerate(names):
            assert (int(acc.A[0, j]), int(acc.R0[0, j]), int(acc.first[0, j]), int(acc.last[0, j])) == want[n][col], (n, W)


def test_runs_are_repeatable_and_separate(results, arms):
    (case, (spec, res)) = next(iter(results.items()))
    again = D.run(spec, arms[case[0]])
    assert D.serialize_run(again) == D.serialize_run(res)
    other = D.run(D.F9RunSpec(M, spec.terrain, spec.composition, spec.obj, spec.init, spec.level_micro, spec.seed_index + 1), arms[case[0]])
    assert not np.array_equal(other.counts, res.counts)
    assert _refused(D.run, spec, arms[("TB", "H")])                           # an arm context that is not the run's arm
    assert _refused(D.run, D.F9RunSpec(M, "TA", "P", "skeleton", "low", 1000000, 0), arms[("T0", "P")])


def test_starts(arms):
    key = lambda obj, init, s: D.F9RunSpec(M, "T0", "P", obj, init, 1500000, s)
    g1 = R.generator_from_key(key("realization", "stationary_floor", 0).stream_key)
    x = D.initial_state(key("realization", "stationary_floor", 0), g1)
    first = R.generator_from_key(key("realization", "stationary_floor", 0).stream_key).random((L, L))
    assert np.array_equal(x, first < D.stationary_pi1(C.F9_ETA0))            # the stream's first full-grid uniform decides the start
    assert abs(x.mean() - 0.052282) < 5 * math.sqrt(0.052282 * 0.947718 / N)
    g2 = R.generator_from_key(key("skeleton", "all_active", 0).stream_key)
    assert D.initial_state(key("skeleton", "all_active", 0), g2).all()
    assert np.array_equal(g2.random(4), R.generator_from_key(key("skeleton", "all_active", 0).stream_key).random(4))   # nothing was drawn
    lows = []
    for s in (0, 1):
        g3 = R.generator_from_key(key("skeleton", "low", s).stream_key)
        lo = D.initial_state(key("skeleton", "low", s), g3); lows.append(lo)
        assert lo.sum() == 200 and np.array_equal(g3.random(4), R.generator_from_key(key("skeleton", "low", s).stream_key).random(4))
        assert np.array_equal(lo, D.initial_state(key("skeleton", "low", s), None))     # the pattern needs no tick stream
    assert not np.array_equal(lows[0], lows[1])


# ======================= the serialized record =======================
def _split(blob):
    start = len(D.RUN_MAGIC) + 4
    (hlen,) = struct.unpack("<I", blob[len(D.RUN_MAGIC):start])
    return json.loads(blob[start:start + hlen]), blob[start + hlen:]


def _join(header, body):
    head = I.canonical_json(header)
    return D.RUN_MAGIC + struct.pack("<I", len(head)) + head + body


@pytest.mark.parametrize("case", RUNS, ids=lambda c: f"{c[0][0]}.{c[0][1]}-{c[1]}-{c[2]}-{c[3]}")
def test_record_round_trips_and_replays(results, arms, case):
    spec, res = results[case]
    blob = D.serialize_run(res)
    assert len(blob) == len(D.RUN_MAGIC) + 4 + len(I.canonical_json(D.run_header(res))) + 4 * (T_ + 1) + 3 * (4 * N + 2 * 1250)
    h, a = D.parse_run(blob)
    assert h == json.loads(I.canonical_json(D.run_header(res))) and sorted(a) == sorted(D.array_names())
    assert np.array_equal(a["counts"], res.counts)
    for W in (1, 10, 100):
        for k in ("A", "R0", "first", "last"): assert np.array_equal(a[f"{k}_W{W}"], res.windows[W][k])
    assert h["master_class"] == "test" and h["stream_key"] == list(spec.stream_key) and h["g"] == res.g
    assert h["floor_probability"] == (0.01 if spec.obj == "realization" else 0.0)
    assert D.replay_equals(blob, arms[case[0]]) and D.run_identity(blob) == hashlib.sha256(blob).hexdigest()
    wrong = next(v for k, v in arms.items() if k != case[0])
    assert D.replay_equals(blob, wrong) is False                              # not the arm the record binds


def _set(k, v):
    def f(h): h[k] = v
    return f


HEADER_TAMPERS = {
    "type": _set("type", "Other"), "schema": _set("schema", 2), "version": _set("version", "f9_stage1_v2"),
    "contract": _set("contract_sha256", "0" * 64), "declaration": _set("declaration_sha256", "0" * 64), "stream_declaration": _set("stream_declaration_sha256", "0" * 64),
    "retired_master": _set("master", 9920261112), "master_class": _set("master_class", "stage"), "terrain": _set("terrain", "TZ"),
    "undeclared_level": _set("level_micro", 1025000), "level_id": _set("level_id", "9.000000"), "seed": _set("seed_index", 40),
    "stream_key": lambda h: h["stream_key"].__setitem__(6, h["stream_key"][6] + 1), "gain": lambda h: h.__setitem__("g", h["g"] * (1 + 1e-15)),
    "floor": lambda h: h.__setitem__("floor_probability", 0.01 - h["floor_probability"]), "mu": _set("mu", 0.25), "ticks": _set("ticks", 2999),
    "windows": _set("windows", [1, 10]), "survival": lambda h: h.__setitem__("survival", not h["survival"]),
    "tail_sum": lambda h: h.__setitem__("tail_active_sum", h["tail_active_sum"] + 1), "draws": lambda h: h.__setitem__("draws_consumed", h["draws_consumed"] + 1),
    "advanced": lambda h: h.__setitem__("ticks_advanced", h["ticks_advanced"] - 1), "extra_field": _set("note", "x"),
    "missing_field": lambda h: h.pop("mu"), "int_for_float": _set("spr", 1), "bool_for_int": _set("seed_index", True),
    "identity_not_hex": _set("index_sha256", "x" * 64), "array_missing": lambda h: h["arrays"].pop("A_W10"),
    "extinction": lambda h: h.__setitem__("extinction_tick", 5 if h["extinction_tick"] is None else None),
}


@pytest.mark.parametrize("name", sorted(HEADER_TAMPERS))
def test_a_changed_header_is_refused(results, name):
    for (case, (spec, res)) in list(results.items())[:2]:                     # a realization run and an extinct skeleton run
        h, body = _split(D.serialize_run(res))
        HEADER_TAMPERS[name](h)
        assert _refused(D.parse_run, _join(h, body)), (name, case)


def _rehash(h, body):
    """Restate every array hash from the body, so that only the consistency checks stand between the record and acceptance."""
    sizes = D._array_sizes(); pos = 0
    for n in D.array_names():
        h["arrays"][n] = hashlib.sha256(body[pos:pos + sizes[n]]).hexdigest(); pos += sizes[n]
    return h


def _with_array(blob, name, fn):
    h, body = _split(blob); sizes = D._array_sizes(); pos = 0
    for n in D.array_names():
        if n == name: break
        pos += sizes[n]
    dtype = "<i4" if name == "counts" else "<u2" if name.startswith(("A_", "R0_")) else np.uint8
    arr = np.frombuffer(body[pos:pos + sizes[name]], dtype=dtype).copy(); fn(arr)
    body = body[:pos] + arr.tobytes() + body[pos + sizes[name]:]
    return h, body


def test_changed_bytes_are_refused_with_and_without_restated_hashes(results):
    (case, (spec, res)) = next(iter(results.items()))                         # the realization run on T0
    blob = D.serialize_run(res)
    assert _refused(D.parse_run, blob[:-1]) and _refused(D.parse_run, blob + b"\x00") and _refused(D.parse_run, b"F9RUN\x00\x02\n" + blob[8:])
    assert _refused(D.parse_run, blob[:-1] + bytes([blob[-1] ^ 1]))           # one bit, hashes as stated
    h, body = _split(blob)
    assert _refused(D.parse_run, D.RUN_MAGIC + struct.pack("<I", len(I.canonical_json(h)) + 1) + I.canonical_json(h) + b" " + body[1:])
    spaced = json.dumps(h, sort_keys=True).encode() + b"\n"                    # same content, not canonical
    assert _refused(D.parse_run, D.RUN_MAGIC + struct.pack("<I", len(spaced)) + spaced + body)
    cell = int(np.flatnonzero((res.windows[1]["A"].ravel() > 0) & (res.windows[1]["A"].ravel() < TAIL))[0])
    changes = {
        "count_above_N": ("counts", lambda a: a.__setitem__(5, N + 1)),
        "tail_count_changed": ("counts", lambda a: a.__setitem__(T_, a[T_] + 1)),
        "A_W1_changed": ("A_W1", lambda a: a.__setitem__(cell, a[cell] + 1)),
        "R0_zero_where_inactive_windows_exist": ("R0_W1", lambda a: a.__setitem__(cell, 0)),
        "R0_more_than_inactive_windows": ("R0_W10", lambda a: a.__setitem__(cell, 101)),
        "A_W10_above_A_W1": ("A_W10", lambda a: a.__setitem__(int(np.argmin(res.windows[1]["A"].ravel())), 100)),
        "A_W100_too_few_for_A_W1": ("A_W100", lambda a: a.__setitem__(int(np.argmax(res.windows[1]["A"].ravel())), 0)),
        "padding_bit_set": ("last_W100", lambda a: a.__setitem__(len(a) - 1, a[-1] | 1)) if N % 8 else None,
    }
    for name, ch in changes.items():
        if ch is None: continue
        h2, body2 = _with_array(blob, *ch)
        assert _refused(D.parse_run, _join(h2, body2)), name                  # the stated hash no longer holds
        assert _refused(D.parse_run, _join(_rehash(h2, body2), body2)), name   # and with the hash restated, the record is inconsistent
    D.parse_run(_join(*_split(blob)))                                         # the helpers reproduce an accepted record


def _altered(res, fn):
    """A record whose window arrays were changed before serialization, so that every array hash is the true hash of
    the changed bytes and the header is canonical: only the consistency checks can refuse it."""
    windows = {W: {k: v.copy() for k, v in row.items()} for W, row in res.windows.items()}
    fn(windows)
    return D.serialize_run(dataclasses.replace(res, windows=windows))


def test_impossible_summaries_are_refused_by_the_parser_l2_m2_round1_r1(results, arms):
    """L2 M2 round 1, R1a and R1b, by L2's constructions, and further relations of the same kind. Each altered record
    contradicts its own stored quantities; the parser itself must refuse it. The unaltered record is the control."""
    (case, (spec, res)) = next(iter(results.items()))                         # the T0 realization run, as in L2's Appendix A
    D.parse_run(_altered(res, lambda w: None))
    w = res.windows
    t_first, t_last = T_ - TAIL + 1, T_
    made = {}
    # R1a: at W = 1 the end masks are the states at the first and last tail ticks
    for end, tick in (("first", t_first), ("last", t_last)):
        cells = np.argwhere(w[1][end] & (w[1]["R0"] >= 2) & (w[1]["A"] >= 3)); assert len(cells)
        c = tuple(int(v) for v in cells[0])
        def clear(win, end=end, c=c): win[1][end][c] = False
        blob = _altered(res, clear)
        assert int(w[1][end].sum()) == int(res.counts[tick])                  # the true record satisfies the identity
        made[f"R1a_{end}"] = blob
    # R1b: an active 100-tick window holds at most ten active 10-tick windows
    lower = (w[1]["A"] + 99) // 100
    cells = np.argwhere((w[10]["A"] > 10 * lower) & (lower >= 2) & (lower < 10)); assert len(cells)
    c = tuple(int(v) for v in cells[0])
    def few_coarse(win, c=c): win[100]["A"][c] = lower[c]; win[100]["R0"][c] = 1
    made["R1b_A10_above_10_A100"] = _altered(res, few_coarse)
    # the same kind, beyond L2's witnesses
    ra1 = w[1]["R0"] - 1 + w[1]["first"] + w[1]["last"]
    c = tuple(int(v) for v in np.argwhere(~w[1]["last"] & (w[1]["A"] >= 100) & (w[1]["A"] <= 400) & (w[1]["R0"] >= 3) & (ra1 >= 3))[0])
    def coarse_segments(win, c=c):                                            # every single-width and count relation holds, and A is nested
        win[10]["A"][c] = 50; win[10]["R0"][c] = 1; win[10]["first"][c] = True; win[10]["last"][c] = False      # one inactive segment at W = 10
        win[100]["A"][c] = 7; win[100]["R0"][c] = 3; win[100]["first"][c] = True; win[100]["last"][c] = False   # three at W = 100
    made["more_coarse_segments_than_fine"] = _altered(res, coarse_segments)
    c = tuple(int(v) for v in np.argwhere(w[10]["first"] & (w[100]["A"] >= 2) & (w[100]["R0"] == 0))[0])
    def coarse_first_off(win, c=c): win[100]["first"][c] = False; win[100]["A"][c] -= 1; win[100]["R0"][c] = 1
    made["first_W10_active_first_W100_inactive"] = _altered(res, coarse_first_off)
    refused = 0; reasons = {}
    for name, blob in made.items():
        with pytest.raises(D.F9DynamicsError, match="not consistent") as info: D.parse_run(blob)
        reasons[name] = str(info.value); refused += 1
    assert refused == 5 and "more segments at the coarser width" in reasons["more_coarse_segments_than_fine"]
    assert "first window's mask" in reasons["R1a_first"] and "last window's mask" in reasons["R1a_last"] and "not nested" in reasons["R1b_A10_above_10_A100"]
    assert "end window is inactive" in reasons["first_W10_active_first_W100_inactive"]
    # counts against the W = 1 record: one more always-active cell than the smallest tail count allows
    quiet = D.run(D.F9RunSpec(M, "T0", "P", "skeleton", "all_active", 750000, 1), arms[("T0", "P")])
    assert quiet.extinction_tick is not None and quiet.extinction_tick <= T_ - TAIL
    def active_after_extinction(win): win[1]["A"][0, 0] = 1; win[1]["R0"][0, 0] = 2
    assert _refused(D.parse_run, _altered(quiet, active_after_extinction))


def test_undeclared_json_types_are_refused_l2_m2_round1_r1c(results):
    """L2 M2 round 1, R1c: a value equal to the declared integer but of another JSON type is not the declared value."""
    (case, (spec, res)) = next(iter(results.items()))
    h, body = _split(D.serialize_run(res))
    D.parse_run(_join(h, body))
    key = list(spec.stream_key)
    cases = {
        "float_stream_key": ("stream_key", [float(v) for v in key]),          # L2's witness
        "bool_window": ("windows", [True, 10, 100]),                         # L2's witness
        "one_float_in_key": ("stream_key", key[:5] + [float(key[5])] + key[6:]),
        "bool_in_key": ("stream_key", key[:6] + [False]),                    # seed index 0
        "float_windows": ("windows", [1.0, 10.0, 100.0]),
        "short_key": ("stream_key", key[:6]), "long_windows": ("windows", [1, 10, 100, 1000]),
        "key_not_a_list": ("stream_key", {"0": 7}), "array_hash_not_a_string": ("arrays", dict(h["arrays"], counts=7)),
    }
    for name, (field, value) in cases.items():
        h2 = json.loads(json.dumps(h)); h2[field] = value
        assert _refused(D.parse_run, _join(h2, body)), name
    start = len(D.RUN_MAGIC) + 4
    raw = I.canonical_json(h)
    for token in (b"Infinity", b"NaN", b"-Infinity"):                         # not finite: json.loads reads them, the parser refuses them
        bad = raw.replace(b'"mu":0.2', b'"mu":' + token); assert bad != raw
        assert _refused(D.parse_run, D.RUN_MAGIC + struct.pack("<I", len(bad)) + bad + body), token


def test_consistency_relations_hold_on_arbitrary_tails():
    """No true record is refused: the relations of `_check_consistency` are NECESSARY, so they must hold for the summaries
    of ANY binary tail, not only for tails the rule produces. Tails here are synthetic (independent cells, persistent
    cells, bursts, sparse, empty, full, and a tail that dies part-way); the summaries are computed by the probe's
    formula from the whole tail, and the counts before the tail are arbitrary."""
    gen = np.random.Generator(np.random.PCG64(np.random.SeedSequence([4, 4, 9])))
    spec = D.F9RunSpec(M, "T0", "P", "realization", "stationary_floor", 1500000, 0)
    def markov(p_on, p_off):                                                  # per-cell two-state chains with cell-specific rates
        x = gen.random((L, L)) < 0.5; out = np.zeros((TAIL, L, L), dtype=bool)
        for t in range(TAIL):
            u = gen.random((L, L)); x = np.where(x, u >= p_off, u < p_on); out[t] = x
        return out
    tails = {
        "independent": gen.random((TAIL, L, L)) < gen.random((L, L)),
        "persistent": markov(0.02 * gen.random((L, L)), 0.02 * gen.random((L, L))),
        "flicker": markov(0.5 * gen.random((L, L)), 0.2 + 0.8 * gen.random((L, L))),
        "sparse": gen.random((TAIL, L, L)) < 0.0005,
        "empty": np.zeros((TAIL, L, L), dtype=bool), "full": np.ones((TAIL, L, L), dtype=bool),
    }
    dying = markov(0.3 * gen.random((L, L)), 0.3 * gen.random((L, L))); dying[437:] = False
    tails["dies_part_way"] = dying
    bursts = np.zeros((TAIL, L, L), dtype=bool); bursts[::97] = gen.random((len(range(0, TAIL, 97)), L, L)) < 0.3
    tails["bursts"] = bursts
    for name, tail in tails.items():
        a = {"counts": np.concatenate([gen.integers(0, N + 1, size=T_ - TAIL + 1), tail.reshape(TAIL, -1).sum(axis=1)]).astype(np.int64)}
        for W in (1, 10, 100):
            n = TAIL // W
            yw = tail.reshape(n, W, L, L).any(axis=1)
            A = yw.sum(axis=0); K = (yw[1:] != yw[:-1]).sum(axis=0)
            a[f"A_W{W}"] = A; a[f"R0_W{W}"] = np.where(A == n, 0, (K + 2 - yw[0].astype(int) - yw[-1].astype(int)) // 2)
            a[f"first_W{W}"] = yw[0]; a[f"last_W{W}"] = yw[-1]
        tc = a["counts"][T_ - TAIL + 1:]
        h = {"extinction_tick": None, "ticks_advanced": T_, "draws_consumed": T_ + 1, "survival": bool((tc > 0).all()), "tail_active_sum": int(tc.sum())}
        D._check_consistency(h, a, spec)                                      # raises if any relation fails


def test_a_consistent_forgery_is_refused_by_replay_only(results, arms):
    """`parse_run` checks what every record satisfies; it cannot know the trajectory. Moving one active tail tick from one
    cell to another keeps every total and every bound. The parser accepts it; replay does not. So a record is established
    by replay, and the parser's guarantee is form and consistency."""
    (case, (spec, res)) = next(iter(results.items()))
    blob = D.serialize_run(res)
    A = res.windows[1]["A"].ravel()
    ok = (A >= 3) & (A <= TAIL - 3) & (res.windows[10]["A"].ravel() * 10 >= A + 1) & (res.windows[10]["A"].ravel() <= A - 1) \
        & (res.windows[100]["A"].ravel() * 100 >= A + 1) & (res.windows[100]["A"].ravel() <= A - 1) \
        & (res.windows[1]["R0"].ravel() <= TAIL - A - 1) & (res.windows[1]["R0"].ravel() - 1 + res.windows[1]["first"].ravel() + res.windows[1]["last"].ravel() <= A - 1)
    i, j = (int(k) for k in np.flatnonzero(ok)[:2])
    def move(a): a[i] += 1; a[j] -= 1
    h2, body2 = _with_array(blob, "A_W1", move)
    forged = _join(_rehash(h2, body2), body2)
    D.parse_run(forged)                                                       # necessary relations hold; the trajectory is not this one
    assert D.replay_equals(forged, arms[case[0]]) is False and D.replay_equals(blob, arms[case[0]]) is True


# ======================= nothing placed before M2 is touched =======================
PLACED = {  # LF identities at 7af5094 (the M1 placement)
    "f9/__init__.py": "7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e",
    "f9/config.py": "5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb",
    "f9/terrain.py": "b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9",
    "f9/geometry.py": "122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971",
    "f9/family.py": "ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1",
    "f9/spectral.py": "b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3",
    "f9/identities.py": "0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577",
}
UNTOUCHED = "c80d494aea4e5e452b4a96536f0bc68515918e4ac8c7f37e84d66bad7c7a3289"   # root, e1, f8, gates: the digest test_f9_m1.py holds


def _sha_lf(path):
    with open(path, "rb") as fh: return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def test_m1_e1_and_f8_are_byte_unchanged():
    for rel, want in PLACED.items(): assert _sha_lf(os.path.join(PKG, *rel.split("/"))) == want, rel
    # The files this module added are present beside them. The folder is not required to hold nothing else: this line
    # first required exactly that and failed as soon as a later module was placed (repaired 2026-11-18).
    assert {r.split("/")[1] for r in PLACED} | set(["dynamics.py", "streams.py"]) <= {fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")}
    h = hashlib.sha256()
    for sub in ("", "e1", "f8", "gates"):
        d = os.path.join(PKG, sub)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"): h.update((sub + "/" + fn if sub else fn).encode()); h.update(bytes.fromhex(_sha_lf(os.path.join(d, fn))))
    assert h.hexdigest() == UNTOUCHED
