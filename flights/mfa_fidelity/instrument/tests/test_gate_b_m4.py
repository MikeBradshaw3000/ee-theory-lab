"""tests/test_gate_b_m4.py — Gate B module 4: formal qualification battery. The battery passes on
the cleared harness under an independent frozen manifest, and the battery itself is shown to fail
when a mutant survives, lands on an undeclared check, is narrowed/altered, or when a prerequisite
fails (a qualification that cannot fail is not a qualification)."""
import contextlib
import json
import os
from unittest import mock
import numpy as np
import pytest

from mfa_instrument.gates.gate_b import qualification as Q
from mfa_instrument.gates.gate_b import b1 as B1
from mfa_instrument.gates.gate_b import b2 as B2
from mfa_instrument.gates.gate_b.reference import load_pinned_reference

PIN = os.environ.get("MFA_PINNED_REPO_ROOT")
needs_pin = pytest.mark.skipif(not PIN, reason="MFA_PINNED_REPO_ROOT unset (no pinned clone)")


# ---------------- declaration and manifest (pin-free) ----------------
def test_frozen_manifest_and_runtime_declaration_agree_at_rest():
    assert Q._manifest_defects() == []
    assert [m.id for m in Q.MUTANTS] == list(range(1, 33)) and len(Q.FROZEN_MANIFEST) == 32
    assert Q.MUTANTS[30].harness == "alignment_witness" and Q.MUTANTS[27].harness == Q.MUTANTS[28].harness == "schedule_table"
    assert "unexpected_exception" not in Q.MUTANTS[26].expected_checks          # mutant 27 (wrong dispatch)

def test_manifest_digest_is_canonical_and_binds_harness_and_mutation_ids():
    entries = [(m.id, m.name, m.harness, m.mutation_id, m.expected_checks) for m in Q.MUTANTS]
    assert __import__("hashlib").sha256(repr(Q._canonical(entries)).encode()).hexdigest() == Q.FROZEN_MANIFEST_SHA256
    altered = list(entries); i, n, h, mid, c = altered[0]; altered[0] = (i, n, h, "step:DIFFERENT", c)
    assert sorted(Q._IMPLEMENTATIONS) == sorted(m.mutation_id for m in Q.MUTANTS)          # dispatcher is closed over the manifest
    assert __import__("hashlib").sha256(repr(Q._canonical(altered)).encode()).hexdigest() != Q.FROZEN_MANIFEST_SHA256

def test_qualification_requires_record_owner():
    with pytest.raises(ValueError, match="record_dir is mandatory"):
        Q.run_qualification("/nonexistent", record_dir=None)

def test_fp_witness_frozen_patterns_are_one_ulp_apart_in_both_logit_and_p():
    W = Q.FROZEN_FP_WITNESS
    for a, b in (("logit_original", "logit_regrouped"), ("p_become_original", "p_become_regrouped")):
        assert abs(int(W[a], 16) - int(W[b], 16)) == 1


# ---------------- positive run ----------------
@needs_pin
def test_qualification_passes_and_persists_complete_evidence(tmp_path):
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert rec.passed, rec.summary()
    assert rec.stages_completed == list(Q.QUALIFICATION_STAGES)     # in memory: all five, including the record act
    assert len(rec.mutants) == 32 and all(m.rejected and m.attributed for m in rec.mutants)
    # complete positive-control report embedded (Q6)
    pc = rec.positive_control
    assert pc["batteries"] == dict(B1.FROZEN_BATTERIES) and pc["environment_record"]["lock_sha256"].startswith("c10e02c5")
    assert pc["provenance"]["candidate_dynamics_sha256"] and pc["comparator_evaluations"] == B1.FROZEN_COMPARATOR_EVALS
    # every b1/schedule mutant links its artifact by path and digest, with bit evidence where the comparator carries it
    for m in rec.mutants:
        if m.harness in ("b1", "schedule_table"):
            assert m.artifact_path and os.path.isfile(m.artifact_path) and m.artifact_sha256
    assert any(m.id == 30 and m.expected_bits and m.observed_bits and m.expected_bits != m.observed_bits for m in rec.mutants)
    # frozen surfaces (L2 §1): 8a scalar, 8b threshold witness, 28/29 on the schedule table, 31 by the constructed transient
    by = {m.id: m for m in rec.mutants}
    assert by[8].observed_check == "p_survive_bits" and by[8].observed_battery == "preflight"
    assert by[9].observed_check == "is_active_exact" and "|equal" in by[9].observed_case
    assert by[28].observed_check == "u_t_bits" and by[28].observed_battery == "schedule_table"
    assert by[29].observed_check == "u_t_bits" and by[29].observed_battery == "schedule_table" and "cm1" in by[29].observed_case
    assert by[31].observed_case == "constructed_all_active_transient"
    assert rec.fp_witness["matches_frozen"] and rec.fp_witness["p_become_bits_differ"]
    assert rec.alignment_witness["constructed_transient"]["aligned_rho0"] == 1.0 and rec.alignment_witness["constructed_transient"]["rho0_margin"] > 0.3
    assert rec.base_invariance_witness["passed"] and not rec.base_invariance_witness["under_base_leakage_mutant"]["passed"]
    assert rec.solved_offset_enumeration["passed"] and rec.solved_offset_enumeration["config_source_sha256"]
    on_disk = json.load(open(rec.written_to))
    assert on_disk["passed"] is True and on_disk["provenance"]["runtime_declaration_sha256"] == Q.FROZEN_MANIFEST_SHA256


# ---------------- can-fail proofs of the battery itself ----------------
@needs_pin
def test_narrowed_all_valid_mutant_list_fails_structurally_before_any_run(monkeypatch, tmp_path):
    monkeypatch.setattr(Q, "MUTANTS", Q.MUTANTS[:2])
    monkeypatch.setattr(B1, "run_b1", lambda *a, **k: (_ for _ in ()).throw(AssertionError("positive control must not run")))
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert not rec.passed and rec.failure.failure_class == "structural" and rec.failure.check == "frozen_manifest"
    assert rec.stages_completed == [] and rec.mutants == [] and os.path.exists(rec.failure.written_to)

@needs_pin
def test_altered_mutation_id_with_same_id_name_checks_fails_manifest(monkeypatch, tmp_path):
    m0 = Q.MUTANTS[0]
    altered = Q.MutantSpec(m0.id, m0.name, m0.description, m0.harness, "step:kappa_abs", m0.expected_checks)
    monkeypatch.setattr(Q, "MUTANTS", (altered,) + Q.MUTANTS[1:])
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert rec.failure.check == "frozen_manifest" and "step:kappa_abs" in rec.failure.detail

@needs_pin
def test_altered_implementation_with_all_manifest_fields_unchanged_fails_preflight(monkeypatch, tmp_path):
    """Mutant 1's frozen fields are untouched; the implementation registered under its mutation_id is
    swapped for mutant 2's (which the same allowable check would reject). The preflight must halt on
    implementation identity BEFORE the positive control."""
    monkeypatch.setitem(Q._IMPLEMENTATIONS, "step:kappa_sign_flip", Q._IMPLEMENTATIONS["step:kappa_abs"])
    monkeypatch.setattr(B1, "run_b1", lambda *a, **k: (_ for _ in ()).throw(AssertionError("positive control must not run")))
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert rec.failure.failure_class == "structural" and rec.failure.check == "implementation_identity"
    assert "step:kappa_abs" in rec.failure.detail and rec.stages_completed == [] and rec.mutants == []

@needs_pin
def test_surviving_mutant_alone_fails_an_otherwise_complete_qualification(monkeypatch, tmp_path):
    """The full frozen family runs; exactly one executor is patched to report survival. Every other pass
    limb is satisfied (asserted), so survival is the sole reason `passed` is False."""
    real = Q._run_mutant_b1
    def executor(pinned_root, m, load_mode, label, record_dir):
        r = real(pinned_root, m, load_mode, label, record_dir)
        if m.id == 5:
            return Q.MutantResult(m.id, m.name, m.harness, m.mutation_id, sorted(m.expected_checks), False, None, None, None, False, "NOT REJECTED (planted)")
        return r
    monkeypatch.setattr(Q, "_run_mutant_b1", executor)
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert not rec.passed and rec.failure is None
    assert len(rec.mutants) == 32 and sum(not m.rejected for m in rec.mutants) == 1 and not rec.mutants[4].rejected
    assert all(m.rejected and m.attributed for m in rec.mutants if m.id != 5)
    assert rec.positive_control["passed"] and rec.base_invariance_witness["passed"] and rec.alignment_witness["passed"]
    assert rec.fp_witness["passed"] and rec.solved_offset_enumeration["passed"] and Q._manifest_defects() == []
    assert not rec.base_invariance_witness["under_base_leakage_mutant"]["passed"]

@needs_pin
def test_unattributed_rejection_alone_fails_an_otherwise_complete_qualification(monkeypatch, tmp_path):
    real = Q._run_mutant_b1
    def executor(pinned_root, m, load_mode, label, record_dir):
        r = real(pinned_root, m, load_mode, label, record_dir)
        if m.id == 5:
            r.attributed = False; r.observed_check = "is_active_exact"; r.detail += " (planted UNATTRIBUTED)"
        return r
    monkeypatch.setattr(Q, "_run_mutant_b1", executor)
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert not rec.passed and rec.failure is None
    assert all(m.rejected for m in rec.mutants) and sum(not m.attributed for m in rec.mutants) == 1
    assert all(m.attributed for m in rec.mutants if m.id != 5)

@needs_pin
def test_alignment_mutant_with_wrong_expected_check_is_unattributed(monkeypatch, tmp_path):
    ref = load_pinned_reference(PIN)
    m = Q.MUTANTS[30]
    wrong = Q.MutantSpec(m.id, m.name, "", m.harness, m.mutation_id, frozenset({"p_become_bits"}))
    res = Q._run_mutant_alignment(ref, wrong)
    assert res.rejected and not res.attributed and "UNATTRIBUTED" in res.detail

@needs_pin
def test_failed_positive_control_halts_before_any_mutant(monkeypatch, tmp_path):
    monkeypatch.setattr(B1, "U_SET", B1.U_SET[:3])
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert not rec.passed and rec.failure.failure_class == "positive_control" and rec.mutants == []
    assert rec.stages_completed == ["manifest_preflight"] and not any(n.startswith("mutant_") for n in os.listdir(tmp_path))
    on_disk = json.load(open(rec.failure.written_to))
    assert on_disk["kind"] == "qualification_failure" and on_disk["positive_control"]["passed"] is False

@needs_pin
def test_failed_witness_halts_before_any_mutant(monkeypatch, tmp_path):
    monkeypatch.setattr(Q, "fp_witness", lambda ref: {"passed": False, "reason": "forced"})
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert rec.failure.failure_class == "witness" and rec.failure.check == "fp_witness" and rec.mutants == []
    assert rec.stages_completed == ["manifest_preflight", "positive_control"]

@needs_pin
def test_injected_solved_offset_support_is_detected_and_scored(monkeypatch, tmp_path):
    from mfa_instrument import config as C
    monkeypatch.setattr(C, "SOLVED_OFFSET_VALUES", (0.07,), raising=False)
    so = Q.solved_offset_enumeration()
    assert so["solved_offset_values_discovered"] == [0.07] and so["missing_from_frozen_table"] == [0.07] and not so["passed"]
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert rec.failure.check == "solved_offset_enumeration" and rec.mutants == []
    monkeypatch.setattr(C, "SOLVED_OFFSET_VALUES", (0.25,), raising=False)      # declared in the frozen CM-0 set
    assert Q.solved_offset_enumeration()["passed"]

def test_solved_offset_dict_registry_is_enumerated_and_refused(monkeypatch):
    from mfa_instrument import config as C
    monkeypatch.setattr(C, "SOLVED_OFFSET_VALUES", {"0.10": 0.07, "nested": [0.25, np.array([0.5, 0.07])]}, raising=False)
    so = Q.solved_offset_enumeration()
    assert so["solved_offset_values_discovered"] == [0.07, 0.25, 0.5] and so["missing_from_frozen_table"] == [0.07] and not so["passed"]

def test_solved_offset_unparseable_registry_fails_closed(monkeypatch):
    from mfa_instrument import config as C
    class Registry:                                  # a future registry object the scanner cannot enumerate
        pass
    monkeypatch.setattr(C, "SOLVED_OFFSET_REGISTRY", Registry(), raising=False)
    so = Q.solved_offset_enumeration()
    assert so["unparsed_surfaces"] == ["config.SOLVED_OFFSET_REGISTRY: Registry"] and not so["passed"]
    assert so["solved_offset_values_discovered"] == []       # absence is NOT inferred from an unparsed surface

def test_solved_offset_source_identity_mismatch_refuses(monkeypatch):
    monkeypatch.setitem(Q.FROZEN_CANDIDATE_SOURCE_SHA256, "dynamics.py", "0" * 64)
    so = Q.solved_offset_enumeration()
    assert not so["source_identity_ok"] and not so["passed"] and so["unparsed_surfaces"] == [] and so["missing_from_frozen_table"] == []

def test_fp_witness_g_q_consistency_is_executable(monkeypatch):
    monkeypatch.setitem(Q.FROZEN_FP_WITNESS, "g_q", -0.75)          # inconsistent with neighbor_count 0
    class R: LOGIT_L = float(np.log(0.4 / 0.6))
    w = Q.fp_witness(R())
    assert not w["passed"] and "inconsistent" in w["reason"]

@needs_pin
def test_qualification_stage_exception_leaves_atomic_failure_record(monkeypatch, tmp_path):
    monkeypatch.setattr(Q, "alignment_witness", lambda ref: (_ for _ in ()).throw(RuntimeError("witness crashed")))
    rec = Q.run_qualification(PIN, record_dir=str(tmp_path))
    assert rec.failure.failure_class == "internal" and rec.failure.stage == "witnesses" and "witness crashed" in rec.failure.detail
    on_disk = json.load(open(rec.failure.written_to))
    assert on_disk["stages_completed"] == ["manifest_preflight", "positive_control"] and on_disk["positive_control"]["passed"] is True

@needs_pin
def test_mutant_30_fails_on_constructed_transient_shifted_window(monkeypatch):
    ref = load_pinned_reference(PIN)
    w = Q.alignment_witness(ref)
    assert w["passed"] and w["constructed_transient"]["aligned_rho0"] == 1.0
    with Q.MUTANTS[30].apply():
        w2 = Q.alignment_witness(ref)
    ct = w2["constructed_transient"]
    assert not ct["passed"] and ct["aligned_rho0"] != 1.0 and abs(ct["aligned_rho0"] - w["constructed_transient"]["shifted_rho0"]) < 1e-12

@needs_pin
def test_base_invariance_witness_detects_base_leakage():
    ref = load_pinned_reference(PIN)
    assert Q.base_invariance_witness(ref)["passed"]
    with Q.MUTANTS[31].apply():
        w = Q.base_invariance_witness(ref)
        assert not w["passed"] and w["bit_differences"]["p_become"] > 0
