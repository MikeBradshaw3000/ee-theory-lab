"""tests/test_gate_b_m2.py — Gate B module 2 (B1 harness): the full run must pass, and the
harness must be SHOWN to fail — halting at the first defective case with an atomic record —
under planted defects on either side. Formal 30-mutant qualification is module 4."""
import os
import numpy as np
import pytest

from mfa_instrument.gates.gate_b import b1 as B1

PIN = os.environ.get("MFA_PINNED_REPO_ROOT")
pytestmark = pytest.mark.skipif(not PIN, reason="MFA_PINNED_REPO_ROOT unset (no pinned clone)")


def test_b1_full_run_passes_all_five_batteries():
    rep = B1.run_b1(PIN)
    assert rep.passed, rep.summary()
    assert rep.batteries == {"single_step": 486, "threshold_witness": 27, "stencil_motif": 108,
                             "chained": 150, "schedule_table": 4000}
    assert rep.cases_compared == 4771 and rep.stages_completed == list(rep.batteries)
    assert rep.provenance["reference"]["commit_verified"] == "4d9a622" and rep.provenance["spec_sha256"] == B1.SPEC_SHA256


def test_b1_refuses_authoritative_outside_canonical_env_or_extraction_mode(tmp_path):
    rep = B1.run_b1(PIN, label="AUTHORITATIVE", load_mode="EXTRACTION", record_dir=str(tmp_path))
    assert not rep.passed and rep.failure.failure_class == "environment" and rep.failure.battery == "preflight"
    assert rep.environment_record is not None and rep.stages_completed == []


def test_b1_halts_on_one_ulp_reference_perturbation(monkeypatch):
    """Planted defect on the REFERENCE side: p_become off by one ULP in one cell -> halt at the
    first case, comparator named, bit patterns recorded, no stage completed."""
    real = B1.load_pinned_reference
    def loader(root, load_mode="EXTRACTION", label="PROVISIONAL"):
        ref = real(root, load_mode, label)
        step = ref.ns["step_tcop_core"]
        def bad_step(grid, u_t, kappa, rand_grid):
            nxt, p = step(grid, u_t, kappa, rand_grid)
            p = p.copy(); p[7, 9] = np.nextafter(p[7, 9], 1.0)
            return nxt, p
        ref.ns["step_tcop_core"] = bad_step
        return ref
    monkeypatch.setattr(B1, "load_pinned_reference", loader)
    rep = B1.run_b1(PIN)
    assert not rep.passed and rep.failure is not None
    f = rep.failure
    assert f.battery == "single_step" and f.comparator == "p_become_bits" and f.mismatches == 1
    assert f.expected_bits.startswith("0x") and f.observed_bits.startswith("0x") and f.expected_bits != f.observed_bits
    assert rep.stages_completed == [] and rep.cases_compared == 0


def test_b1_halts_on_candidate_kappa_sign_flip(monkeypatch):
    """Planted defect on the CANDIDATE side: kappa plumbed with the wrong sign. Cases with
    kappa=0 are blind to it by construction; the halt must land on the first kappa != 0 case."""
    real_cfg = B1._cfg
    monkeypatch.setattr(B1, "_cfg", lambda ref, kappa, schedule, ticks: real_cfg(ref, -kappa, schedule, ticks))
    rep = B1.run_b1(PIN)
    assert not rep.passed
    f = rep.failure
    assert f.battery == "single_step" and f.comparator == "p_become_bits"
    assert "k=+0.1042" in f.case_id and "u=0.0" in f.case_id     # first nonzero-kappa case in the frozen order
    assert rep.cases_compared == 1                                 # exactly the one blind (kappa=0) case passed


def test_b1_halts_on_schedule_defect_in_schedule_table(monkeypatch):
    """Candidate schedule realizes CM-1 with the block order permuted: every step battery is
    unaffected (they supply u_t externally), and the halt lands in the schedule table."""
    monkeypatch.setattr(B1, "_cm1_schedule",
                        lambda tier: tuple((b * 25, (0.0, tier, tier / 2.0)[b % 3]) for b in range(16)))
    rep = B1.run_b1(PIN)
    assert not rep.passed
    f = rep.failure
    assert f.battery == "schedule_table" and f.comparator == "u_t_bits" and "cm1|tier=0.1" in f.case_id
    assert rep.stages_completed == ["single_step", "threshold_witness", "stencil_motif", "chained"]


def test_b1_halts_on_threshold_convention_defect(monkeypatch):
    """Reference mutated to `<=` in the become branch: single-step and stencil cases can pass
    (rand equal to p is measure-zero there), so the halt must land in the threshold witnesses."""
    real = B1.load_pinned_reference
    def loader(root, load_mode="EXTRACTION", label="PROVISIONAL"):
        ref = real(root, load_mode, label)
        ns = ref.ns
        def le_step(grid, u_t, kappa, rand_grid):
            neighbors = ns["get_neighbor_count"](grid)
            q_i = neighbors / 8.0; g_q = 2.0 * q_i - 1.0
            p_become = ns["sigmoid"](ns["LOGIT_L"] + u_t + kappa * g_q)
            become = (grid == 0) & (rand_grid <= p_become)            # <= : the planted defect
            stay = (grid == 1) & (rand_grid < ns["LAMBDA"])
            return (become | stay).astype(int), p_become
        ns["step_tcop_core"] = le_step
        return ref
    monkeypatch.setattr(B1, "load_pinned_reference", loader)
    rep = B1.run_b1(PIN)
    assert not rep.passed
    f = rep.failure
    assert f.battery == "threshold_witness" and f.comparator == "is_active_exact" and "|equal" in f.case_id
    assert rep.stages_completed == ["single_step"]


# ====================== round-2 additions (L2 review of modules 1-2) ======================
import json
import numpy as _np
from mfa_instrument.gates.gate_b.comparators import ComparatorError as _CE
from mfa_instrument.gates.gate_b.stub import StubError as _SE
from mfa_instrument.gates.gate_b.reference import ReferenceError as _RE

def test_b1_frozen_battery_map_and_counts_encoded_in_gate():
    rep = B1.run_b1(PIN)
    assert rep.passed and dict(B1.FROZEN_BATTERIES) == rep.batteries
    assert rep.cases_compared == 4771 and rep.comparator_evaluations > rep.cases_compared
    assert rep.allclose_diagnostic["false"] == 0 and rep.allclose_diagnostic["true"] > 0

def test_b1_narrowed_battery_is_a_persisted_structural_failure(monkeypatch, tmp_path):
    """Narrow the single-step drive set: no comparator fails, yet the gate issues the common
    structural failure record and writes it (L2 r2 10D/12) — never a silent passed=False."""
    monkeypatch.setattr(B1, "U_SET", B1.U_SET[:3])
    rep = B1.run_b1(PIN, record_dir=str(tmp_path))
    assert not rep.passed and rep.failure is not None and rep.failure.failure_class == "structural"
    assert rep.failure.comparator == "battery_map" and rep.failure.battery == "completion"
    assert rep.failure.written_to and json.load(open(rep.failure.written_to))["comparator"] == "battery_map"

def test_b1_scalar_p_survive_mismatch_produces_record_with_bits(monkeypatch):
    real = B1._cfg
    def cfg(ref, kappa, schedule, ticks):
        c = real(ref, kappa, schedule, ticks)
        object.__setattr__(c.constants, "p_survive", _np.nextafter(0.4, 1.0)) if hasattr(c.constants, "__dict__") else None
        return c
    monkeypatch.setattr(B1, "_cfg", cfg)
    rep = B1.run_b1(PIN)
    assert not rep.passed and rep.failure.failure_class == "scalar" and rep.failure.comparator == "p_survive_bits"
    assert rep.failure.expected_bits == "0x3fd999999999999a" and rep.failure.observed_bits == "0x3fd999999999999b"
    assert rep.failure.battery == "preflight" and rep.stages_completed == []

def test_b1_comparator_contract_violation_becomes_record(monkeypatch):
    real = B1.load_pinned_reference
    def loader(root, load_mode="EXTRACTION", label="PROVISIONAL"):
        ref = real(root, load_mode, label); step = ref.ns["step_tcop_core"]
        ref.ns["step_tcop_core"] = lambda g, u, k, r: (lambda n, p: (n, p.astype(_np.float32)))(*step(g, u, k, r))
        return ref
    monkeypatch.setattr(B1, "load_pinned_reference", loader)
    rep = B1.run_b1(PIN)
    assert rep.failure.failure_class == "comparator" and rep.failure.comparator == "comparator_contract"
    assert "float64" in rep.failure.detail and rep.failure.battery == "single_step"

def test_b1_stub_failures_are_attributed_records(monkeypatch):
    """Candidate mutated to draw twice per tick: the stub halts by COUNT and the record names it."""
    from mfa_instrument import dynamics as D
    real_step = D.Dynamics._step_become_survive
    def two_draws(self, sink):
        self._g.random(size=(self.cfg.grid_scale, self.cfg.grid_scale)); return real_step(self, sink)
    monkeypatch.setattr(D.Dynamics, "_step_become_survive", two_draws)
    rep = B1.run_b1(PIN)
    assert rep.failure.failure_class == "stub" and "second full-grid draw" in rep.failure.detail

def test_b1_wrong_field_family_fails_by_named_check_not_keyerror(monkeypatch):
    from mfa_instrument import dynamics as D
    real_step = D.Dynamics._step_become_survive
    def a_family(self, sink):
        real_step(self, lambda t, f: sink(t, {"PRNG_draw": f["rand_grid"], "p_act": f["p_become"],
                                              "is_active": f["is_active"]}) if sink else None)
    monkeypatch.setattr(D.Dynamics, "_step_become_survive", a_family)
    rep = B1.run_b1(PIN)
    assert rep.failure.failure_class == "field_family" and rep.failure.comparator == "sink_field_family"
    assert "PRNG_draw" in rep.failure.detail and "g_q" in rep.failure.detail

def test_b1_missing_pin_source_is_a_named_environment_failure_with_artifact(tmp_path):
    """Nonexistent root: the FIRST failure is the frozen pin source, classified 'environment' —
    never 'internal'. (This test found that gap.)"""
    rep = B1.run_b1(str(tmp_path / "nope"), record_dir=str(tmp_path / "rec"))
    f = rep.failure
    assert f.failure_class == "environment" and f.comparator == "frozen_pin_source" and f.case_id == "environment"
    on_disk = json.load(open(f.written_to))
    assert on_disk["failure_class"] == "environment" and "unreadable" in on_disk["detail"]
    assert not any(n.startswith(".b1_failure_") for n in os.listdir(tmp_path / "rec"))     # no temp residue

def test_b1_reference_absence_is_a_named_reference_failure_with_artifact(tmp_path):
    import subprocess
    root = tmp_path / "pin"
    subprocess.run(["git", "clone", "-q", "--shared", PIN, str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "checkout", "-q", "4d9a622"], check=True)
    os.remove(root / "cycle3" / "wave_two" / "c3_w2_tcop.py")
    rep = B1.run_b1(str(root), record_dir=str(tmp_path / "rec"))
    f = rep.failure
    assert f.failure_class == "reference" and f.case_id == "reference" and "absent" in f.detail
    assert f.written_to and json.load(open(f.written_to))["stages_completed"] == []

def test_b1_failure_record_written_atomically_for_battery_halt(monkeypatch, tmp_path):
    real_cfg = B1._cfg
    monkeypatch.setattr(B1, "_cfg", lambda ref, kappa, schedule, ticks: real_cfg(ref, -kappa, schedule, ticks))
    rep = B1.run_b1(PIN, record_dir=str(tmp_path))
    assert rep.failure.written_to and json.load(open(rep.failure.written_to))["comparator"] == "p_become_bits"

def test_b1_schedule_table_is_per_tick_and_catches_interior_tick_defect(monkeypatch):
    """Defect at tick 7 of block 3 only — invisible to start/middle/end sampling, caught per-tick."""
    from mfa_instrument import dynamics as D
    real = D.Dynamics._u_t
    monkeypatch.setattr(D.Dynamics, "_u_t", lambda self, tick: real(self, tick) + (1e-9 if tick == 82 else 0.0))
    rep = B1.run_b1(PIN)
    assert rep.failure.battery == "schedule_table" and rep.failure.comparator == "u_t_bits"
    assert rep.failure.case_id.endswith("|tick=82") and rep.failure.expected_bits.startswith("0x")
    assert rep.stages_completed == ["single_step", "threshold_witness", "stencil_motif", "chained"]

def test_b1_allclose_diagnostic_present_but_never_alters_verdict(monkeypatch):
    """A 1e-12 reference perturbation: allclose says 'true', raw bits say fail — the verdict is raw bits."""
    real = B1.load_pinned_reference
    def loader(root, load_mode="EXTRACTION", label="PROVISIONAL"):
        ref = real(root, load_mode, label); step = ref.ns["step_tcop_core"]
        ref.ns["step_tcop_core"] = lambda g, u, k, r: (lambda n, p: (n, p + 1e-12))(*step(g, u, k, r))
        return ref
    monkeypatch.setattr(B1, "load_pinned_reference", loader)
    rep = B1.run_b1(PIN)
    assert not rep.passed and rep.failure.comparator == "p_become_bits"
    assert rep.allclose_diagnostic["true"] >= 1 and rep.allclose_diagnostic["false"] == 0

def test_b1_run_leaves_global_rng_states_unchanged():
    _np.random.seed(11); import random as R_; R_.seed(12)
    a, b = _np.random.get_state()[1].copy(), R_.getstate()
    B1.run_b1(PIN)
    assert _np.array_equal(a, _np.random.get_state()[1]) and R_.getstate() == b

def test_b1_rand_grid_identity_records_count_and_bits(monkeypatch):
    """Candidate emits a corrupted rand_grid copy: identity check reports the real mismatch count."""
    from mfa_instrument import dynamics as D
    real_step = D.Dynamics._step_become_survive
    def corrupt(self, sink):
        def s(t, f):
            g = f["rand_grid"].copy(); g[0, 0] = _np.nextafter(g[0, 0], 1.0); g[1, 1] = 0.123
            sink(t, {**f, "rand_grid": g})
        real_step(self, s if sink else None)
    monkeypatch.setattr(D.Dynamics, "_step_become_survive", corrupt)
    rep = B1.run_b1(PIN)
    assert rep.failure.comparator == "rand_grid_identity" and rep.failure.mismatches == 2
    assert rep.failure.expected_bits.startswith("0x") and rep.failure.expected_bits != rep.failure.observed_bits


# ====================== round-3 additions (L2 round-2 verification) ======================
def test_b1_frozen_totals_and_diagnostic_counts_exact():
    rep = B1.run_b1(PIN)
    assert rep.passed and rep.comparator_evaluations == 7085 and sum(rep.allclose_diagnostic.values()) == 6314
    assert rep.comparator_evaluations_by_battery == B1.FROZEN_COMPARATOR_EVALS_PER_BATTERY

def test_b1_omitted_comparator_is_a_structural_failure(monkeypatch, tmp_path):
    """Skip the g_q comparator at runtime: all 4,771 case counts survive, but the frozen
    comparator total does not — the gate halts structurally with a persisted record."""
    real = B1._Runner.compare_case
    def skip_gq(self, case_id, grid, rand, cand, ref_next, ref_p, consumed):
        cand = dict(cand); cand["g_q"] = _np.asarray(B1._ancestor_g_q(self.ref, grid))     # force pass...
        return real(self, case_id, grid, rand, cand, ref_next, ref_p, consumed)
    # ...then remove one evaluation's accounting to simulate an omitted comparator
    monkeypatch.setattr(B1, "_ancestor_g_q", lambda ref, grid: (_np.asarray(ref.get_neighbor_count(grid)) / 8.0) * 2.0 - 1.0)
    real_eval = B1._Runner._eval
    calls = {"n": 0}
    def eval_once_less(self):
        calls["n"] += 1
        if calls["n"] == 5:   # drop exactly one evaluation
            return
        real_eval(self)
    monkeypatch.setattr(B1._Runner, "_eval", eval_once_less)
    rep = B1.run_b1(PIN, record_dir=str(tmp_path))
    assert rep.failure is not None and rep.failure.failure_class == "structural"
    assert rep.failure.comparator in ("comparator_set_completion", "diagnostic_completion")

def test_b1_authoritative_and_qualification_refuse_to_start_without_record_owner():
    with pytest.raises(ValueError, match="record_dir is mandatory"):
        B1.run_b1(PIN, label="AUTHORITATIVE", load_mode="FULL")
    with pytest.raises(ValueError, match="record_dir is mandatory"):
        B1.run_b1(PIN, qualification=True)

def test_b1_persisted_record_carries_full_environment_and_accumulated_provenance(monkeypatch, tmp_path):
    """A candidate-provenance failure must retain the already-earned environment record and
    reference provenance plus the expected identities (L2 r2 10A/10B)."""
    monkeypatch.setattr(B1, "candidate_provenance", lambda root, sink: (_ for _ in ()).throw(B1.ProvenanceError("candidate_git", "candidate provenance: git rev-parse HEAD failed: simulated")))
    rep = B1.run_b1(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f.failure_class == "provenance" and f.case_id == "candidate_provenance"
    on_disk = json.load(open(f.written_to))
    assert on_disk["environment_record"]["lock_sha256"] == "c10e02c5db497570ffeb45dc92857fcc633cb38364858a35458096950d02de7c"
    assert len(on_disk["environment_record"]["pins"]) == 20
    assert on_disk["provenance"]["reference"]["commit_verified"] == "4d9a622"        # earned before the failure
    assert on_disk["provenance"]["expected"]["reference_sha256"].startswith("466455f2")  # expected identities retained
    assert "candidate_commit" not in on_disk["provenance"]                              # never earned

def test_b1_environment_failure_retains_expected_identities(tmp_path):
    rep = B1.run_b1(str(tmp_path / "nope"), record_dir=str(tmp_path / "rec"))
    on_disk = json.load(open(rep.failure.written_to))
    assert on_disk["failure_class"] == "environment" and on_disk["environment_record"] is None
    assert on_disk["provenance"]["expected"]["reference_commit"] == "4d9a622" and "reference" not in on_disk["provenance"]

def test_b1_dynamics_digest_read_failure_retains_partial_candidate_provenance(monkeypatch, tmp_path):
    """dynamics.py unreadable AFTER commit and dirtiness were earned: the persisted record keeps
    both, omits the digest, names the dedicated sub-check, and retains everything earlier."""
    real_open = open
    def bad_open(path, *a, **k):
        if str(path).endswith("dynamics.py") and a and "rb" in a:
            raise PermissionError("simulated")
        return real_open(path, *a, **k)
    monkeypatch.setattr("builtins.open", bad_open)
    rep = B1.run_b1(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f.failure_class == "provenance" and f.comparator == "candidate_dynamics_sha256"
    on_disk = json.load(open(f.written_to))
    pv = on_disk["provenance"]
    assert "candidate_commit" in pv and len(pv["candidate_commit"]) >= 7
    assert "candidate_worktree_dirty" in pv and isinstance(pv["candidate_worktree_dirty"], bool)
    assert "candidate_dynamics_sha256" not in pv
    assert pv["reference"]["commit_verified"] == "4d9a622" and pv["expected"]["lock_sha256"].startswith("c10e02c5")
    assert on_disk["environment_record"]["lock_sha256"].startswith("c10e02c5")

def test_b1_git_failure_is_named_candidate_git(monkeypatch, tmp_path):
    import subprocess as sp
    real_run = sp.run
    def bad_run(cmd, *a, **k):
        if cmd[:2] == ["git", "-C"] and "rev-parse" in cmd and "HEAD" in cmd and "--short=7" not in cmd:
            class R: returncode = 128; stdout = ""; stderr = "fatal: simulated"
            return R()
        return real_run(cmd, *a, **k)
    monkeypatch.setattr(sp, "run", bad_run)
    rep = B1.run_b1(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f.failure_class == "provenance" and f.comparator == "candidate_git" and "simulated" in f.detail
    pv = json.load(open(f.written_to))["provenance"]
    assert "candidate_commit" not in pv and pv["reference"]["commit_verified"] == "4d9a622"

def test_b1_reference_read_failure_is_reference_class(monkeypatch, tmp_path):
    from mfa_instrument.gates.gate_b import reference as RR
    real_open = open
    def bad_open(path, *a, **k):
        if str(path).endswith("c3_w2_tcop.py") and a and "rb" in a:
            raise OSError("simulated I/O")
        return real_open(path, *a, **k)
    monkeypatch.setattr("builtins.open", bad_open)
    rep = B1.run_b1(PIN, record_dir=str(tmp_path))
    assert rep.failure.failure_class == "reference" and "unreadable" in rep.failure.detail

def test_b1_two_rapid_failures_do_not_overwrite(monkeypatch, tmp_path):
    monkeypatch.setattr(B1, "candidate_provenance", lambda root, sink: (_ for _ in ()).throw(B1.ProvenanceError("candidate_git", "candidate provenance: simulated")))
    a = B1.run_b1(PIN, record_dir=str(tmp_path)).failure.written_to
    b = B1.run_b1(PIN, record_dir=str(tmp_path)).failure.written_to
    assert a != b and os.path.exists(a) and os.path.exists(b)

def test_b1_scalar_and_schedule_diagnostics_are_evaluated(monkeypatch):
    """p_survive and the 4,000 u_t comparisons each contribute a diagnostic: 6,314 total."""
    rep = B1.run_b1(PIN)
    assert sum(rep.allclose_diagnostic.values()) == 2313 + 4000 + 1


# ====================== bounded O1 repair (module-4 review): stub-failure case identity ======================
def test_b1_stub_failure_carries_true_case_identity(monkeypatch, tmp_path):
    """A candidate that draws twice fails by stub count INSIDE model.step; the record must name the
    case being executed, never a stale label from preflight (frozen §7)."""
    from mfa_instrument import dynamics as D
    real_step = D.Dynamics._step_become_survive
    def two_draws(self, sink):
        self._g.random(size=(self.cfg.grid_scale, self.cfg.grid_scale)); return real_step(self, sink)
    monkeypatch.setattr(D.Dynamics, "_step_become_survive", two_draws)
    rep = B1.run_b1(PIN, record_dir=str(tmp_path))
    f = rep.failure
    assert f.failure_class == "stub" and f.battery == "single_step"
    assert f.case_id == "all_inactive|u=0.0|k=+0.0000" and f.case_id != "p_survive"
    assert json.load(open(f.written_to))["case_id"] == "all_inactive|u=0.0|k=+0.0000"
