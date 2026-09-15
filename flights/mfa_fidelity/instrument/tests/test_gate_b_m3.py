"""tests/test_gate_b_m3.py — Gate B module 3 (B2 harness). Alignment on both sides; the ported
screen reproduces the canonical no-tie tail; wrapper verification passes and fails under a mocked
execute_run; the full PROVISIONAL run passes; a planted candidate divergence halts fail-fast
with a persisted record; the certified claim travels verbatim."""
import json
import os
import numpy as np
import pytest

from mfa_instrument.gates.gate_b import b2 as B2
from mfa_instrument.gates.gate_b.reference import load_pinned_reference

PIN = os.environ.get("MFA_PINNED_REPO_ROOT")
needs_pin = pytest.mark.skipif(not PIN, reason="MFA_PINNED_REPO_ROOT unset (no pinned clone)")


@pytest.fixture(scope="module")
def ref():
    if not PIN:
        pytest.skip("MFA_PINNED_REPO_ROOT unset (no pinned clone)")
    return load_pinned_reference(PIN)


# ---------------- alignment (A2) ----------------
def test_reference_wrapper_records_pre_step_states(ref):
    st = B2.reference_wrapper_states(ref, "cm0", 0.0, 0.25, 0.4221, 201)
    assert st.shape == (400, 50, 50) and st.dtype.kind in "iu"
    rho = B2.rho_trajectory_from_states(st)
    assert rho[0] == 0.1                                   # exactly 250/2500: the initialized grid, pre-step
    assert st[0].sum() == 250 and rho[1] != rho[0]

def test_candidate_trajectory_is_pre_step_aligned_and_never_computes_tick_399_output(ref, monkeypatch):
    from mfa_instrument import dynamics as D
    calls = {"n": 0}; real = D.Dynamics.step
    def counting(self, sink): calls["n"] += 1; return real(self, sink)
    monkeypatch.setattr(D.Dynamics, "step", counting)
    rho = B2.candidate_rho_trajectory(ref, "cm0", 0.0, 0.25, 0.4221, 301)
    assert rho.shape == (400,) and rho[0] == 0.1 and calls["n"] == 399

def test_one_tick_shift_is_visible_on_both_sides(ref):
    """A shifted extraction (post-step of tick t labelled t) puts the post-step density of tick 0
    at index 0; it must differ from the pre-step 0.1 on both sides — the alignment is checkable."""
    st = B2.reference_wrapper_states(ref, "cm0", 0.0, 0.25, 0.4221, 201)
    shifted_ref0 = float(np.mean(ref.step_tcop_core(st[0], 0.25, 0.4221, np.random.default_rng(0).random((50, 50)))[0]))
    assert shifted_ref0 != 0.1
    cand = B2.candidate_rho_trajectory(ref, "cm0", 0.0, 0.25, 0.4221, 301)
    assert cand[0] == 0.1 and cand[1] != 0.1               # index 1 is the first post-step density

def test_wrapper_and_execute_run_loop_are_the_same_recipe(ref):
    """Independent hand replica of execute_run L488-507 must be array_equal to the wrapper."""
    import random as R_
    np_s = np.random.get_state(); py_s = R_.getstate()
    try:
        np.random.seed(137); R_.seed(137)
        flat = np.zeros(2500, dtype=int); flat[:250] = 1; np.random.shuffle(flat); grid = flat.reshape((50, 50))
        states = np.zeros((400, 50, 50), dtype=int)
        for t in range(400):
            states[t] = grid
            u_t = ref.u_t_for("cm1", 0.25, 0.0, t // 25)
            grid, _ = ref.step_tcop_core(grid, u_t, -0.4221, np.random.rand(50, 50))
    finally:
        np.random.set_state(np_s); R_.setstate(py_s)
    assert np.array_equal(states, B2.reference_wrapper_states(ref, "cm1", 0.25, 0.0, -0.4221, 137))


# ---------------- statistics ----------------
def test_screen_reproduces_canonical_no_tie_tail_and_identity_case():
    assert B2.conditional_permutation_p(12, tuple([1] * 40)) == 0.0011158015462314926
    x = np.full(20, 0.4)
    assert B2.gross_divergence_screen(x, x) == {"D_int": 0, "tie_blocks": 1, "p": 1.0, "alarm": False}

def test_screen_alarms_on_disjoint_samples_and_is_tie_invariant():
    a = np.linspace(0.30, 0.31, 20); b = np.linspace(0.40, 0.41, 20)
    s = B2.gross_divergence_screen(a, b); assert s["D_int"] == 20 and s["alarm"]
    # all-tied pooled sample: any label arrangement gives D=0 -> p=1 regardless of order
    t = np.full(20, 0.5); u = np.full(20, 0.5)
    assert B2.gross_divergence_screen(t, u)["p"] == 1.0 and B2.gross_divergence_screen(u, t)["p"] == 1.0

def test_welch_tost_exact_quantile_and_pass_fail():
    rng = np.random.default_rng(1)
    a = rng.normal(0.40, 0.0015, 20); b = a + 0.0002         # identical sample variances -> Welch df = 38 exactly
    r = B2.welch_tost(a, b)
    assert abs(r["df"] - 38.0) < 1e-9 and r["pass"]
    from scipy.stats import t as st
    assert r["t_quantile"] == float(st.ppf(1 - 0.05 / 8, 38)) and abs(r["t_quantile"] - 2.622) < 1e-3   # the frozen bound's "approximately 2.62"; exact 2.62220
    c = rng.normal(0.40, 0.0030, 20)                          # unequal variances -> Welch df < 38, larger quantile
    assert B2.welch_tost(a, c)["df"] < 38 and B2.welch_tost(a, c)["t_quantile"] > r["t_quantile"]
    assert not B2.welch_tost(a + 0.005, b)["pass"]         # the declared material divergence fails
    with pytest.raises(ValueError):
        B2.welch_tost(a[:19], b)


# ---------------- wrapper verification ----------------
def _fake_execute_run_factory(ref, perturb=False):
    def fake(mode, c_label, kappa, tier, u_const, seed, stage):
        st = B2.reference_wrapper_states(ref, mode, tier, u_const, kappa, seed).copy()
        if perturb and seed == 137:
            st[399, 0, 0] ^= 1
        return st, None, None
    return fake

def test_wrapper_verification_passes_against_faithful_execute_run(ref):
    ref.ns["execute_run"] = _fake_execute_run_factory(ref)
    try:
        rep = B2.B2Report("PROVISIONAL", "env", None, {})
        r = B2._Runner(rep); r.ref = ref
        v = B2.verify_wrapper(ref, r)
        assert v["status"] == "PASS" and len(v["runs"]) == 10 and all(x["identical"] for x in v["runs"])
        assert sum(1 for x in v["runs"] if x["seed"] == 137) == 2
    finally:
        del ref.ns["execute_run"]

def test_wrapper_verification_fails_on_single_cell_divergence(ref):
    ref.ns["execute_run"] = _fake_execute_run_factory(ref, perturb=True)
    try:
        rep = B2.B2Report("PROVISIONAL", "env", None, {})
        r = B2._Runner(rep); r.ref = ref
        with pytest.raises(B2.GateBFailure) as ei:
            B2.verify_wrapper(ref, r)
        rec = ei.value.record
        assert rec.failure_class == "wrapper" and rec.check == "states_bit_identity" and "seed 137" in rec.detail
        assert rec.expected != rec.observed
    finally:
        del ref.ns["execute_run"]

def test_wrapper_not_performed_under_extraction(ref):
    rep = B2.B2Report("PROVISIONAL", "env", None, {}); r = B2._Runner(rep); r.ref = ref
    assert B2.verify_wrapper(ref, r)["status"] == "NOT_PERFORMED"


# ---------------- full run, halts, refusals ----------------
@needs_pin
def test_b2_full_provisional_run_passes_all_eight_cells(tmp_path):
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.passed, rep.summary()
    assert [c.cell for c in rep.cells] == [c[0] for c in B2.CELLS]
    for c in rep.cells:
        assert abs(c.diff) < B2.DELTA and c.ci_low > -B2.DELTA and c.ci_high < B2.DELTA and not c.alarm
        assert len(c.ref_terminal) == 20 and len(c.cand_terminal) == 20
    assert rep.certified_claim == B2.CERTIFIED_CLAIM and rep.provenance["grammar"]["delta"] == 0.003
    assert rep.wrapper_verification["status"] == "NOT_PERFORMED" and not os.listdir(tmp_path)   # no success artifact

@needs_pin
def test_b2_halts_fail_fast_on_planted_candidate_kappa_sign(monkeypatch, tmp_path):
    real = B2._cell_cfg
    monkeypatch.setattr(B2, "_cell_cfg", lambda ref, mode, tier, u, k, root: real(ref, mode, tier, u, -k, root))
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert not rep.passed and f is not None
    assert f.failure_class in ("acceptance", "screen") and f.cell == "cm0_u0.00_k+0.4221"   # first kappa != 0 cell
    assert len(rep.cells) == 3 and rep.cells[0].tost_pass and rep.cells[1].tost_pass
    on_disk = json.load(open(f.written_to))
    assert len(on_disk["cells_completed"]) == 3 and on_disk["provenance"]["reference"]["commit_verified"] == "4d9a622"

@needs_pin
def test_b2_authoritative_refusals(tmp_path):
    with pytest.raises(ValueError, match="record_dir is mandatory"):
        B2.run_b2(PIN, label="AUTHORITATIVE", load_mode="FULL")
    rep = B2.run_b2(PIN, label="AUTHORITATIVE", load_mode="EXTRACTION", record_dir=str(tmp_path))
    assert rep.failure.failure_class == "environment" and rep.stages_completed == []

@needs_pin
def test_b2_authoritative_requires_wrapper_pass(monkeypatch, tmp_path):
    """Environment and load-mode gates satisfied artificially: an unverified wrapper still halts."""
    from mfa_instrument.gates.gate_b import environment as E
    real_check = E.check_environment
    def conforming(root):
        rec = real_check(root)
        return E.EnvironmentRecord(**{**rec.__dict__, "conforms": True, "failures": []})
    monkeypatch.setattr(B2, "check_environment", conforming)
    monkeypatch.setattr(B2, "load_pinned_reference", lambda root, mode, label: load_pinned_reference(root, "EXTRACTION", "PROVISIONAL"))
    rep = B2.run_b2(PIN, label="AUTHORITATIVE", load_mode="FULL", record_dir=str(tmp_path))
    assert rep.failure.failure_class == "wrapper" and rep.failure.check == "verification_required"


# ====================== round-2 additions (L2 module-3 review) ======================
import itertools
from math import comb as _comb
from mfa_instrument import dynamics as _D

# ---- 1. block diagnostics ----
@needs_pin
def test_block_diagnostics_exact_shape_reconstruction_and_verdict_inertness(ref):
    rho = B2.candidate_rho_trajectory(ref, "cm0", 0.0, 0.25, 0.4221, 301)
    term, blocks = B2.summaries_from_trajectory(rho)
    assert len(blocks) == 16 and term == float(rho[300:400].mean())
    assert blocks[3] == float(rho[75:100].mean()) and blocks[15] == float(rho[375:400].mean())
    rep = B2.run_b2(PIN)
    assert rep.passed
    for c in rep.cells:
        assert np.array(c.ref_blocks).shape == (20, 16) and np.array(c.cand_blocks).shape == (20, 16)
    c = rep.cells[0]
    # the terminal statistic is the mean of blocks 12..15 (ticks 300-399): consistency of the two summaries
    assert all(abs(np.mean(c.cand_blocks[i][12:16]) - c.cand_terminal[i]) < 1e-12 for i in range(20))
    # verdict inertness: overwrite the diagnostics and recompute the verdict from the report
    c.cand_blocks = [[9.0] * 16 for _ in range(20)]; c.ref_blocks = [[-9.0] * 16 for _ in range(20)]
    assert rep.passed and c.tost_pass and not c.alarm and B2._completion_defects(rep) == []

# ---- 2. candidate sink/time contract (fail-closed capture) ----
def _patch_step(monkeypatch, wrapper):
    real = _D.Dynamics.step
    monkeypatch.setattr(_D.Dynamics, "step", lambda self, sink: wrapper(self, sink, real))

def test_capture_refuses_missing_callback_after_first_tick(ref, monkeypatch):
    def w(self, sink, real):
        return real(self, sink if self.tick_count == 0 else None)       # omitted from tick 1 on
    _patch_step(monkeypatch, w)
    with pytest.raises(B2.CaptureError) as ei:
        B2.candidate_rho_trajectory(ref, "cm0", 0.0, 0.25, 0.4221, 301)
    assert ei.value.check == "sink_invocation_count" and "tick 1" in str(ei.value)

def test_capture_refuses_duplicate_callback(ref, monkeypatch):
    def w(self, sink, real):
        return real(self, (lambda t, f: (sink(t, f), sink(t, f))) if sink else None)
    _patch_step(monkeypatch, w)
    with pytest.raises(B2.CaptureError) as ei:
        B2.candidate_rho_trajectory(ref, "cm0", 0.0, 0.25, 0.4221, 301)
    assert ei.value.check == "sink_invocation_count" and "2 sink invocations" in str(ei.value)

def test_capture_refuses_wrong_callback_tick(ref, monkeypatch):
    def w(self, sink, real):
        return real(self, (lambda t, f: sink(t + 1, f)) if sink else None)
    _patch_step(monkeypatch, w)
    with pytest.raises(B2.CaptureError) as ei:
        B2.candidate_rho_trajectory(ref, "cm0", 0.0, 0.25, 0.4221, 301)
    assert ei.value.check == "sink_tick_index"

@pytest.mark.parametrize("mutate,check", [
    (lambda f: {**f, "is_active": f["is_active"].astype(np.int64)}, "is_active_dtype"),
    (lambda f: {**f, "is_active": f["is_active"][:49]}, "is_active_shape"),
    (lambda f: {k: v for k, v in f.items() if k != "Psi_local"}, "sink_field_family"),
])
def test_capture_refuses_malformed_state_field(ref, monkeypatch, mutate, check):
    def w(self, sink, real):
        return real(self, (lambda t, f: sink(t, mutate(f))) if sink else None)
    _patch_step(monkeypatch, w)
    with pytest.raises(B2.CaptureError) as ei:
        B2.candidate_rho_trajectory(ref, "cm0", 0.0, 0.25, 0.4221, 301)
    assert ei.value.check == check

# ---- 3. frozen completion independent of execution constants ----
def _stat_pass_runner(monkeypatch, ref):
    """Make every cell trivially pass statistically so only completion can fail."""
    base = B2.reference_wrapper_states(ref, "cm0", 0.0, 0.0, 0.0, 201)
    base_rho = B2.rho_trajectory_from_states(base)
    rng = np.random.default_rng(0)
    # both sides: the same base trajectory plus small independent per-seed noise -> equivalent, no ties
    monkeypatch.setattr(B2, "reference_wrapper_states", lambda *a, **k: base)
    monkeypatch.setattr(B2, "rho_trajectory_from_states", lambda st: base_rho + rng.normal(0, 1e-4, 400))
    real_cfg = B2._cell_cfg
    def cand(ref_, mode, tier, u, k, root, consumed_schedule=None):
        if consumed_schedule is not None:                      # honor the consumed-schedule contract
            consumed_schedule.append(tuple((int(a), float(b)) for a, b in B2._cell_cfg(ref_, mode, tier, u, k, root).drive_schedule))
        return base_rho + rng.normal(0, 1e-4, 400)
    monkeypatch.setattr(B2, "candidate_rho_trajectory", cand)

@needs_pin
def test_completion_refuses_narrowed_cell_map_structurally(ref, monkeypatch, tmp_path):
    _stat_pass_runner(monkeypatch, ref)
    monkeypatch.setattr(B2, "CELLS", B2.CELLS[:7])
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    # PRECEDENCE: the static preflight halts before any output exists
    assert rep.failure.failure_class == "structural" and rep.failure.check == "static_cells"
    assert rep.stages_completed == [] and rep.cells == [] and json.load(open(rep.failure.written_to))["check"] == "static_cells"
    # REDUNDANT DEFENSE: with the preflight bypassed, completion still catches it after the fact
    monkeypatch.setattr(B2, "_static_grammar_defects", lambda rep_: [])
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure.check == "cell_map" and len(rep.cells) == 7

@needs_pin
def test_completion_refuses_reordered_cell_map_structurally(ref, monkeypatch, tmp_path):
    _stat_pass_runner(monkeypatch, ref)
    monkeypatch.setattr(B2, "CELLS", B2.CELLS[::-1])
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure.check == "static_cells" and rep.stages_completed == []
    monkeypatch.setattr(B2, "_static_grammar_defects", lambda rep_: [])
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure.failure_class == "structural" and rep.failure.check == "cell_map"

@needs_pin
def test_completion_refuses_substituted_seed_with_unchanged_length(ref, monkeypatch, tmp_path):
    _stat_pass_runner(monkeypatch, ref)
    monkeypatch.setattr(B2, "REF_SEEDS", tuple(range(201, 220)) + (999,))
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure.check == "static_ref_seeds" and rep.stages_completed == []
    monkeypatch.setattr(B2, "_static_grammar_defects", lambda rep_: [])
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure.failure_class == "structural" and rep.failure.check == "seed_pools"

@needs_pin
def test_completion_refuses_truncated_vector(ref, monkeypatch, tmp_path):
    _stat_pass_runner(monkeypatch, ref)
    rep = B2.run_b2(PIN)
    assert rep.passed
    rep.cells[2].cand_blocks[5] = rep.cells[2].cand_blocks[5][:15]
    d = B2._completion_defects(rep)
    assert d and d[0][0] == "block_matrices" and not rep.passed
    rep2 = B2.run_b2(PIN); rep2.cells[0].ref_terminal.pop()
    assert B2._completion_defects(rep2)[0][0] == "terminal_vectors"

def test_frozen_object_and_execution_constants_agree_at_rest():
    assert tuple(B2.FROZEN_B2["cells"]) == B2.CELLS and B2.FROZEN_B2["ref_seeds"] == B2.REF_SEEDS
    assert B2.FROZEN_B2["wrapper_map"] == B2.WRAPPER_VERIFICATION_RUNS and B2.FROZEN_B2["delta"] == B2.DELTA

# ---- 4. statistical domain ----
def test_tost_domain_guards():
    a = np.random.default_rng(2).normal(0.4, 1e-3, 20)
    with pytest.raises(B2.StatisticalDomainError, match="exactly 20"):
        B2.welch_tost(a[:19], a)
    b = a.copy(); b[3] = np.nan
    with pytest.raises(B2.StatisticalDomainError, match="nonfinite"):
        B2.welch_tost(a, b)
    with pytest.raises(B2.StatisticalDomainError, match="float64"):
        B2.welch_tost(a.astype(np.float32), a)
    with pytest.raises(B2.StatisticalDomainError, match="zero-variance"):
        B2.welch_tost(np.full(20, 0.4), np.full(20, 0.4))

def test_screen_domain_guards():
    a = np.linspace(0.39, 0.41, 20)
    with pytest.raises(B2.StatisticalDomainError):
        B2.gross_divergence_screen(a[:19], a)
    with pytest.raises(B2.StatisticalDomainError):
        B2.gross_divergence_screen(np.r_[a[:19], np.inf], a)
    with pytest.raises(B2.StatisticalDomainError, match="summing to 40"):
        B2.conditional_permutation_p(5, (20, 19))
    with pytest.raises(B2.StatisticalDomainError, match="D_obs"):
        B2.conditional_permutation_p(21, tuple([1] * 40))
    with pytest.raises(B2.StatisticalDomainError, match="D_obs"):
        B2.conditional_permutation_p(-1, tuple([1] * 40))

def test_screen_dp_against_exhaustive_small_n_oracle():
    """Independent oracle: enumerate every label assignment at n=4 (C(8,4)=70) for several MIXED tie
    configurations and compare the DP's conditional tail exactly."""
    n = 4
    for blocks in [(1,)*8, (2, 1, 1, 2, 1, 1), (3, 5), (1, 2, 3, 2), (4, 4), (2, 2, 2, 2)]:
        for D_obs in range(0, n + 1):
            positions = list(range(2 * n))
            # map positions to blocks
            owner = [i for i, b in enumerate(blocks) for _ in range(b)]
            hits = 0
            for cand_pos in itertools.combinations(positions, n):
                cs = set(cand_pos); a = s = 0; D = 0; start = 0
                for i, b in enumerate(blocks):
                    c = sum(1 for q in range(start, start + b) if q in cs); start += b
                    a += c; s += b; D = max(D, abs(2 * a - s))
                hits += (D >= D_obs)
            assert abs(B2.conditional_permutation_p(D_obs, blocks, n=n) - hits / _comb(2 * n, n)) < 1e-15

def test_screen_dp_mixed_tie_against_monte_carlo_at_n20():
    """Second independent construction at the live n: random label assignments for a mixed-tie
    pooled sample; the DP tail must agree within Monte-Carlo error."""
    blocks = (3, 1, 1, 2, 1, 4, 1, 1, 2, 1, 1, 3, 1, 1, 2, 1, 1, 5, 1, 3, 1, 1, 1, 1)
    assert sum(blocks) == 40
    rng = np.random.default_rng(7); R = 200_000; N = 20
    owner = np.repeat(np.arange(len(blocks)), blocks)
    hits = 0
    for _ in range(R):
        lab = np.zeros(40, int); lab[rng.choice(40, N, replace=False)] = 1
        a = np.bincount(owner, weights=lab, minlength=len(blocks)).cumsum(); s = np.cumsum(blocks)
        hits += int(np.max(np.abs(2 * a - s)) >= 9)
    mc = hits / R; dp = B2.conditional_permutation_p(9, blocks)
    assert abs(mc - dp) < 4 * np.sqrt(dp * (1 - dp) / R) + 1e-9

# ---- 5. failure-path separation ----
def _synthetic_runner(monkeypatch, ref, cand_terms, ref_terms):
    """Feed constructed terminal values through the real ensemble loop as constant trajectories."""
    it_c = iter(cand_terms * 8); it_r = iter(ref_terms * 8)
    monkeypatch.setattr(B2, "reference_wrapper_states", lambda ref_, m, t_, u, k, s: np.full((400, 50, 50), 0, int))
    monkeypatch.setattr(B2, "rho_trajectory_from_states", lambda st: np.full(400, next(it_r)))
    def cand(ref_, m, t_, u, k, s, consumed_schedule=None):
        if consumed_schedule is not None:
            consumed_schedule.append(tuple((int(a), float(b)) for a, b in B2._cell_cfg(ref_, m, t_, u, k, s).drive_schedule))
        return np.full(400, next(it_c))
    monkeypatch.setattr(B2, "candidate_rho_trajectory", cand)

@needs_pin
def test_tost_only_failure_names_acceptance_welch_tost(ref, monkeypatch, tmp_path):
    ref_terms = list(np.linspace(0.399, 0.401, 20)); cand_terms = [0.400 + 0.006 * (1 if i % 2 else -1) for i in range(20)]
    _synthetic_runner(monkeypatch, ref, cand_terms, ref_terms)
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f.failure_class == "acceptance" and f.check == "welch_tost" and not rep.cells[0].alarm
    assert json.load(open(f.written_to))["check"] == "welch_tost"

@needs_pin
def test_screen_only_alarm_names_gross_divergence(ref, monkeypatch, tmp_path):
    ref_terms = list(np.linspace(0.3990, 0.4010, 20)); cand_terms = list(np.linspace(0.40110, 0.40120, 20))
    _synthetic_runner(monkeypatch, ref, cand_terms, ref_terms)
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f.failure_class == "screen" and f.check == "gross_divergence_alarm"
    assert rep.cells[0].tost_pass and rep.cells[0].D_int == 20
    assert json.load(open(f.written_to))["check"] == "gross_divergence_alarm"

@needs_pin
def test_statistical_domain_failure_is_named_in_run(ref, monkeypatch, tmp_path):
    _synthetic_runner(monkeypatch, ref, [0.4] * 20, [0.4] * 20)      # zero variance both sides
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure.failure_class == "statistical_domain" and "zero-variance" in rep.failure.detail

# ---- 6. wrapper evidence ----
@needs_pin
def test_late_wrapper_divergence_persists_all_preceding_runs(ref, monkeypatch, tmp_path):
    from mfa_instrument.gates.gate_b import environment as E
    real_check = E.check_environment
    monkeypatch.setattr(B2, "check_environment", lambda root: E.EnvironmentRecord(**{**real_check(root).__dict__, "conforms": True, "failures": []}))
    def loader(root, mode, label):
        r_ = load_pinned_reference(root, "EXTRACTION", "PROVISIONAL")
        r_.ns["execute_run"] = _fake_execute_run_factory(r_, perturb=True)    # diverges at seed 137 (runs 9-10)
        return r_
    monkeypatch.setattr(B2, "load_pinned_reference", loader)
    rep = B2.run_b2(PIN, label="AUTHORITATIVE", load_mode="FULL", record_dir=str(tmp_path))
    f = rep.failure
    assert f.failure_class == "wrapper" and f.check == "states_bit_identity"
    on_disk = json.load(open(f.written_to))
    wv = on_disk["wrapper_verification"]
    assert wv["status"] == "FAIL" and len(wv["runs"]) == 9 and all(x["identical"] for x in wv["runs"][:8])
    assert not wv["runs"][8]["identical"] and wv["first_failing_run"]["seed"] == 137
    assert wv["declared_map"][8] == ["cm1_t0.25_k+0.4221", 137]


# ====================== round-3 additions (L2 module-3 round-2 verification) ======================
import hashlib as _hl

@needs_pin
def test_wrapper_value_equality_with_different_dtype_fails_bit_identity(ref):
    def fake(mode, c_label, kappa, tier, u_const, seed, stage):
        return B2.reference_wrapper_states(ref, mode, tier, u_const, kappa, seed).astype(np.int32), None, None
    ref.ns["execute_run"] = fake
    try:
        rep = B2.B2Report("PROVISIONAL", "env", None, {}); r = B2._Runner(rep); r.ref = ref
        with pytest.raises(B2.GateBFailure) as ei:
            B2.verify_wrapper(ref, r)
        rec = ei.value.record; run0 = rep.wrapper_verification["runs"][0]
        assert rec.check == "states_bit_identity" and run0["array_equal_diagnostic"] is True and not run0["identical"]
        assert run0["actual_dtype"] == "int32" and run0["wrapper_dtype"] == "int64" and run0["actual_sha256"] != run0["wrapper_sha256"]
    finally:
        del ref.ns["execute_run"]

@needs_pin
def test_changed_runtime_claim_fails_independent_frozen_check(ref, monkeypatch, tmp_path):
    """The runtime claim text is altered AFTER the report exists (the dataclass default binds the
    original at import, so patching the module constant would not reach the report); the check
    compares the runtime text's digest against the INDEPENDENT frozen digest."""
    rep = B2.run_b2(PIN)
    assert rep.passed
    rep.certified_claim = B2.CERTIFIED_CLAIM + " Also distributional equivalence."
    d = B2._completion_defects(rep)
    assert d and d[0][0] == "certified_claim" and d[0][1] == B2.FROZEN_B2["claim_sha256"] and d[0][2] != d[0][1]
    assert not rep.passed

@needs_pin
def test_changed_claim_version_fails(ref, monkeypatch, tmp_path):
    _stat_pass_runner(monkeypatch, ref)
    rep = B2.run_b2(PIN)
    assert rep.passed
    rep.provenance["claim_version"] = "tampered"
    d = B2._completion_defects(rep)
    assert d and d[0][0] == "claim_version" and not rep.passed

@needs_pin
def test_changed_block_length_with_sixteen_blocks_fails_frozen_grammar(ref, monkeypatch, tmp_path):
    _stat_pass_runner(monkeypatch, ref)
    monkeypatch.setattr(B2, "BLOCK", 24)                     # 400 // 24 == 16: matrix shape unchanged
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure.check == "static_block" and rep.stages_completed == []       # precedence
    monkeypatch.setattr(B2, "_static_grammar_defects", lambda rep_: [])
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    # with the preflight bypassed, the per-cell schedule guard fires BEFORE any score (BLOCK shifts CM-1 timing
    # only from cell 7; the CM-0 cells pass first), and the record shows the first six cells completed
    assert rep.failure.failure_class == "structural" and rep.failure.check == "schedule_consumed"
    assert rep.failure.cell == "cm1_t0.25_k+0.4221" and len(rep.cells) == 6
    assert json.load(open(rep.failure.written_to))["stages_completed"] == ["preflight", "wrapper_verification"]

@needs_pin
def test_performed_provisional_wrapper_with_narrowed_map_fails_completion(ref, monkeypatch, tmp_path):
    _stat_pass_runner(monkeypatch, ref)
    monkeypatch.setattr(B2, "WRAPPER_VERIFICATION_RUNS", B2.WRAPPER_VERIFICATION_RUNS[:9])
    def loader(root, mode, label):
        r_ = load_pinned_reference(root, "EXTRACTION", "PROVISIONAL")
        r_.ns["execute_run"] = _fake_execute_run_factory(r_)
        return r_
    monkeypatch.setattr(B2, "load_pinned_reference", loader)
    rep = B2.run_b2(PIN, label="PROVISIONAL", load_mode="FULL", record_dir=str(tmp_path))
    assert rep.failure.check == "static_wrapper_map" and rep.stages_completed == []      # precedence
    monkeypatch.setattr(B2, "_static_grammar_defects", lambda rep_: [])
    rep = B2.run_b2(PIN, label="PROVISIONAL", load_mode="FULL", record_dir=str(tmp_path))
    assert rep.wrapper_verification["status"] == "PASS" and len(rep.wrapper_verification["runs"]) == 9
    assert rep.failure.failure_class == "structural" and rep.failure.check == "wrapper_map" and rep.cells == []

@needs_pin
def test_root_dependent_candidate_schedule_is_refused_not_hidden(ref, monkeypatch, tmp_path):
    real = B2._cell_cfg
    def cfg(ref_, mode, tier, u_const, kappa, root):
        c = real(ref_, mode, tier, u_const, kappa, root)
        if root == 305:                                        # one root gets a different schedule
            import dataclasses
            c = dataclasses.replace(c, drive_schedule=((0, 0.0), (7, 0.05)))
        return c
    monkeypatch.setattr(B2, "_cell_cfg", cfg)
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure.failure_class == "structural" and rep.failure.check == "schedule_consumed_uniform"
    assert "(7, 0.05)" in rep.failure.observed

@needs_pin
def test_kappa_dependent_schedule_shifting_all_roots_is_caught_against_frozen_expected(ref, monkeypatch, tmp_path):
    _stat_pass_runner(monkeypatch, ref)                        # statistics pass; schedule is the only defect
    real = B2._cell_cfg
    import dataclasses
    def cfg(ref_, mode, tier, u_const, kappa, root):
        c = real(ref_, mode, tier, u_const, kappa, root)
        return dataclasses.replace(c, drive_schedule=((0, u_const + 0.01),)) if mode == "cm0" and kappa > 0 else c
    monkeypatch.setattr(B2, "_cell_cfg", cfg)
    rep = B2.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure.failure_class == "structural" and rep.failure.check == "schedule_consumed"

@needs_pin
def test_failure_records_carry_stages_completed_at_wrapper_cell_and_completion(ref, monkeypatch, tmp_path):
    # cell failure
    ref_terms = list(np.linspace(0.399, 0.401, 20)); cand_terms = [0.400 + 0.006 * (1 if i % 2 else -1) for i in range(20)]
    _synthetic_runner(monkeypatch, ref, cand_terms, ref_terms)
    rep = B2.run_b2(PIN, record_dir=str(tmp_path / "a"))
    assert json.load(open(rep.failure.written_to))["stages_completed"] == ["preflight", "wrapper_verification"]

@needs_pin
def test_wrapper_failure_record_shows_preflight_only(ref, monkeypatch, tmp_path):
    from mfa_instrument.gates.gate_b import environment as E
    real_check = E.check_environment
    monkeypatch.setattr(B2, "check_environment", lambda root: E.EnvironmentRecord(**{**real_check(root).__dict__, "conforms": True, "failures": []}))
    def loader(root, mode, label):
        r_ = load_pinned_reference(root, "EXTRACTION", "PROVISIONAL"); r_.ns["execute_run"] = _fake_execute_run_factory(r_, perturb=True); return r_
    monkeypatch.setattr(B2, "load_pinned_reference", loader)
    rep = B2.run_b2(PIN, label="AUTHORITATIVE", load_mode="FULL", record_dir=str(tmp_path))
    assert json.load(open(rep.failure.written_to))["stages_completed"] == ["preflight"]

def test_pure_statistical_tests_run_without_pin():
    """Guard for the narrowed skip: this and the TOST/screen/DP tests carry no pin marker."""
    assert B2.conditional_permutation_p(0, tuple([1] * 40)) == 1.0


# ====================== round-4 additions (L2 module-3 round-3 verification): jurisdiction ======================
def _raise_if_called(name):
    def f(*a, **k):
        raise AssertionError(f"{name} must not be reached")
    return f

@needs_pin
def test_changed_stage_declaration_is_caught_statically_and_prefix_defense_stands(ref, monkeypatch, tmp_path):
    """A changed STAGES declaration halts at the static preflight (precedence); independently, the
    completion-level prefix defense flags a wrong recorded prefix on a finished report."""
    import mfa_instrument.gates.gate_b.b2 as M
    monkeypatch.setattr(M, "STAGES", ("preflight", "wrapper_verification", "ensembles", "ensembles", "completion"))
    rep = M.run_b2(PIN, record_dir=str(tmp_path))
    assert rep.failure is not None and rep.failure.check == "static_stages" and rep.failure.written_to
    monkeypatch.undo()
    rep2 = B2.run_b2(PIN)
    assert rep2.passed
    rep2.stages_completed[:] = ["preflight", "ensembles", "wrapper_verification", "completion"]
    assert not rep2.passed and any(d[0] == "stages" for d in B2._completion_defects(rep2))

@needs_pin
def test_completion_stage_persists_stages_failure_with_artifact(ref, monkeypatch, tmp_path):
    """Drive the completion stage directly with a wrong prefix: structural/stages must be persisted."""
    import mfa_instrument.gates.gate_b.b2 as M
    _stat_pass_runner(monkeypatch, ref)
    # make the ensembles stage silently drop its own stage name (simulate a stage-history defect)
    real_ens_summ = M.summaries_from_trajectory
    done = {"cells": 0}
    # patch: after the ensembles function returns, remove 'wrapper_verification' from the prefix
    orig_stage_fn_source = M.run_b2
    def patched_verify_wrapper(ref_, r):
        out = {"status": "NOT_PERFORMED", "reason": "test", "runs": []}
        r.rep.wrapper_verification.update(out)
        r.rep.stages_completed.append("bogus")      # contaminates the prefix before completion
        return r.rep.wrapper_verification
    monkeypatch.setattr(M, "verify_wrapper", patched_verify_wrapper)
    rep = M.run_b2(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f is not None and f.failure_class == "structural" and f.check == "stages"
    assert "bogus" in f.observed and json.load(open(f.written_to))["check"] == "stages"

@needs_pin
def test_narrowed_wrapper_map_halts_before_any_ensemble(ref, monkeypatch, tmp_path):
    """Bypass the static preflight (which would catch the narrowed constant first) to test the
    wrapper-stage guard alone; block the ENSEMBLE-ONLY functions, leave the wrapper's own inputs intact."""
    import mfa_instrument.gates.gate_b.b2 as M
    monkeypatch.setattr(M, "WRAPPER_VERIFICATION_RUNS", M.WRAPPER_VERIFICATION_RUNS[:9])
    monkeypatch.setattr(M, "_static_grammar_defects", lambda rep_: [])
    def loader(root, mode, label):
        r_ = load_pinned_reference(root, "EXTRACTION", "PROVISIONAL"); r_.ns["execute_run"] = _fake_execute_run_factory(r_); return r_
    monkeypatch.setattr(M, "load_pinned_reference", loader)
    monkeypatch.setattr(M, "candidate_rho_trajectory", _raise_if_called("candidate ensemble"))
    monkeypatch.setattr(M, "rho_trajectory_from_states", _raise_if_called("reference ensemble summaries"))
    rep = M.run_b2(PIN, label="PROVISIONAL", load_mode="FULL", record_dir=str(tmp_path))
    f = rep.failure
    assert f is not None and f.failure_class == "structural" and f.check == "wrapper_map"
    assert rep.stages_completed == ["preflight"] and rep.cells == [] and len(rep.wrapper_verification["runs"]) == 9
    assert json.load(open(f.written_to))["stages_completed"] == ["preflight"]

@needs_pin
def test_wrong_uniform_schedule_halts_before_tost_or_screen(ref, monkeypatch, tmp_path):
    import mfa_instrument.gates.gate_b.b2 as M, dataclasses
    real = M._cell_cfg
    monkeypatch.setattr(M, "_cell_cfg", lambda ref_, m, t_, u, k, root: dataclasses.replace(real(ref_, m, t_, u, k, root), drive_schedule=((0, u + 0.01),)))
    monkeypatch.setattr(M, "welch_tost", _raise_if_called("welch_tost"))
    monkeypatch.setattr(M, "gross_divergence_screen", _raise_if_called("gross_divergence_screen"))
    rep = M.run_b2(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f is not None and f.failure_class == "structural" and f.check == "schedule_consumed"
    assert rep.cells == [] and "no score computed" in f.detail

@needs_pin
def test_static_grammar_preflight_halts_changed_delta_before_any_output(ref, monkeypatch, tmp_path):
    import mfa_instrument.gates.gate_b.b2 as M
    monkeypatch.setattr(M, "DELTA", 0.004)
    monkeypatch.setattr(M, "verify_wrapper", _raise_if_called("wrapper stage"))
    monkeypatch.setattr(M, "reference_wrapper_states", _raise_if_called("ensembles"))
    rep = M.run_b2(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f.failure_class == "structural" and f.check == "static_delta" and f.stage == "preflight"
    assert rep.stages_completed == [] and "before any output" in f.detail

@needs_pin
def test_wrapper_runs_record_shapes(ref):
    ref.ns["execute_run"] = _fake_execute_run_factory(ref)
    try:
        rep = B2.B2Report("PROVISIONAL", "env", None, {}); r = B2._Runner(rep); r.ref = ref
        B2.verify_wrapper(ref, r)
        assert rep.wrapper_verification["runs"][0]["actual_shape"] == [400, 50, 50] == rep.wrapper_verification["runs"][0]["wrapper_shape"]
    finally:
        del ref.ns["execute_run"]


# ====================== round-5 addition (L2 module-3 round-4): stage-declaration bootstrap ======================
@needs_pin
@pytest.mark.parametrize("stages", [
    ("wrapper_verification", "preflight", "ensembles", "completion"),   # preflight not first
    ("ensembles", "completion"),                                          # preflight absent
    ("unknown_stage", "preflight", "ensembles", "completion"),            # unknown first
    (),                                                                   # empty
])
def test_malformed_stage_declaration_cannot_bypass_its_own_verifier(ref, monkeypatch, tmp_path, stages):
    import mfa_instrument.gates.gate_b.b2 as M
    monkeypatch.setattr(M, "STAGES", stages)
    monkeypatch.setattr(M, "verify_wrapper", _raise_if_called("wrapper stage"))
    monkeypatch.setattr(M, "reference_wrapper_states", _raise_if_called("ensembles"))
    monkeypatch.setattr(M, "candidate_rho_trajectory", _raise_if_called("ensembles"))
    rep = M.run_b2(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f is not None and f.failure_class == "structural" and f.check == "static_stages" and f.stage == "preflight"
    assert rep.stages_completed == [] and rep.cells == []
    assert os.path.exists(f.written_to) and json.load(open(f.written_to))["check"] == "static_stages"
