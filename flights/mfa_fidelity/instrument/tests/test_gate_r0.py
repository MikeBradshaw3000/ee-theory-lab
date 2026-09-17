"""tests/test_gate_r0.py — Gate R0: projection-bridge correctness (round 4). Bridge closed forms and
fail-closed contracts; independence of the exact-rational expectation path; the full constructed-case
run; joint-narrowing refusal against the UNMODIFIED gate; noncoercive comparators; failure grammar;
AST no-feedback; Q2 persistence negatives; labels, provenance, and the AUTHORITATIVE success rule;
the 28-mutant qualification battery and its own can-fail proofs."""
import contextlib
import json
import os
from fractions import Fraction
from unittest import mock
import numpy as np
import pandas as pd
import pytest

from mfa_instrument import bridge as BR
from mfa_instrument.gates import gate_r0 as R0
from mfa_instrument.gates.gate_b.comparators import ComparatorError

PIN = os.environ.get("MFA_PINNED_REPO_ROOT")
needs_pin = pytest.mark.skipif(not PIN, reason="MFA_PINNED_REPO_ROOT unset (no pinned clone)")
G = R0.G
Z = lambda: np.zeros((G, G))
H = lambda: np.full((G, G), 0.5)


# ======================= bridge: closed forms and contracts (pin-free) =======================
def test_checkerboard_and_stripes_closed_forms():
    cb, st = R0.grid_named("checkerboard"), R0.grid_named("row_stripes")
    assert BR.rho_global(cb) == 0.5 and BR.local_read_dispersion(BR.local_density(cb), 0.5) == 0.0 and BR.morans_i(cb) == 0.0
    ld = BR.local_density(st)
    assert BR.local_read_dispersion(ld, BR.rho_global(st)) == 1 / 16 and BR.morans_i(st) == -0.5
    assert BR.config_neighbourhood_correlation(ld, ld) == 1.0 and BR.config_neighbourhood_correlation(1.0 - ld, ld) == -1.0

def test_exact_expectation_path_is_independent_and_agrees():
    for name in R0.R0_CASES["q1_grids"]:
        g = R0.grid_named(name)
        assert np.array_equal(np.array([[float(x) for x in row] for row in R0.exact_local_density(g)]), BR.local_density(g))
        assert float(R0.exact_rho(g)) == BR.rho_global(g)
        em = R0.exact_moran(g)
        if em is None:
            with pytest.raises(BR.BridgeDomainError): BR.morans_i(g)
        else:
            assert float(em) == BR.morans_i(g)
    assert R0.exact_moran(R0.grid_named("checkerboard")) == Fraction(0) and R0.exact_moran(R0.grid_named("row_stripes")) == Fraction(-1, 2)

@pytest.mark.parametrize("bad", [
    lambda: BR.rho_global(np.zeros((0, 0), bool)),
    lambda: BR.local_density(np.zeros((0, 0), bool)),
    lambda: BR.local_read_dispersion(np.zeros((0, 0)), 0.5),
    lambda: BR.base_distribution_dispersion(np.zeros((0, 0)), np.zeros((0, 0)), np.zeros((0, 0))),
    lambda: BR.config_neighbourhood_correlation(np.zeros((0, 0)), np.zeros((0, 0))),
    lambda: BR.morans_i(np.zeros((0, 0), bool)),
])
def test_empty_inputs_are_refused_not_nan(bad):
    with pytest.raises(BR.BridgeDomainError):
        bad()

@pytest.mark.parametrize("bad,msg", [
    (lambda: BR.q_response(Z().astype(np.float32), 0.5, 0.0, 0.0, H(), H(), H()), "float64"),
    (lambda: BR.q_response(Z(), np.full((G,), 0.5), 0.0, 0.0, H(), H(), H()), "2-D"),                 # broadcastable 1-D activation
    (lambda: BR.q_response(Z(), np.full((G, G), 0.5, np.float32), 0.0, 0.0, H(), H(), H()), "float64"),
    (lambda: BR.q_response(Z(), 0.5, 0.0, 0.0, H(), np.full((G + 1, G + 1), 0.5), H()), "shape"),
    (lambda: BR.q_response(Z(), 0.5, float("nan"), 0.0, H(), H(), H()), "nonfinite"),
    (lambda: BR.q_response(Z(), 0.5, 0.0, float("inf"), H(), H(), H()), "nonfinite"),
    (lambda: BR.q_response(Z(), 1.5, 0.0, 0.0, H(), H(), H()), "outside"),
    (lambda: BR.q_response(Z(), np.full((G, G), -0.1), 0.0, 0.0, H(), H(), H()), "outside"),
    (lambda: BR.q_response(Z(), 0.5, 0.0, 0.0, np.full((G, G), np.nan), H(), H()), "nonfinite"),
    (lambda: BR.q_response(Z(), 0.5, 0.0, 0.0, np.full((G, G), 1.5), H(), H()), "outside"),
    (lambda: BR.q_response(Z(), 1, 0.0, 0.0, H(), H(), H()), "float scalar"),                        # integer scalar refused
    (lambda: BR.local_read_dispersion(H(), float("nan")), "nonfinite"),
    (lambda: BR.local_read_dispersion(H(), 1.5), "outside"),
    (lambda: BR.base_distribution_dispersion(H(), np.full((G + 1, G + 1), 0.5), H()), "shape"),
    (lambda: BR.config_neighbourhood_correlation(H(), np.full((G + 1, G + 1), 0.5)), "shape"),
    (lambda: BR.local_density(np.array([[0, 2], [1, 0]])), "binary"),
])
def test_bridge_contracts_refuse_without_coercion(bad, msg):
    with pytest.raises(BR.BridgeDomainError, match=msg):
        bad()

def test_q_response_fields_and_pre_clip_counting_with_distinct_bases():
    psi = Z(); v = np.full((G, G), 0.875); u = np.full((G, G), 0.5); r = np.full((G, G), 0.0)
    q = BR.q_response(psi, 0.5, 0.0, 1.0, v, u, r)                      # delta = 0.5 everywhere
    assert q.clipped_v == G * G and q.clipped_u_base == 0 and q.clipped_r == 0
    assert np.all(q.v_new == 1.0) and np.all(q.u_base_new == 1.0) and np.all(q.r_new == 0.5) and q.mean_delta == 0.5
    q2 = BR.q_response(np.full((G, G), -8.0), 0.0, 0.25, 0.0, np.full((G, G), 0.125), u, r)   # delta = -2: low clip
    assert q2.clipped_v == G * G and np.all(q2.v_new == 0.0) and q2.mean_delta == -2.0

def test_undefined_statistics_are_refused_not_zero():
    with pytest.raises(BR.BridgeDomainError): BR.morans_i(np.ones((G, G), bool))
    with pytest.raises(BR.BridgeDomainError): BR.config_neighbourhood_correlation(H(), np.random.default_rng(0).random((G, G)))


# ======================= harness structure (pin-free) =======================
def test_frozen_map_is_immutable_and_bound_to_the_literal_digest():
    import types
    assert isinstance(R0.FROZEN_R0, types.MappingProxyType)
    with pytest.raises(TypeError):
        R0.FROZEN_R0["grid"] = 8
    assert R0.frozen_map_digest(R0.FROZEN_R0) == R0.FROZEN_R0_SHA256_LITERAL
    assert all(R0.R0_CASES[k] == R0.FROZEN_R0[k] for k in R0.R0_CASES)

def test_no_feedback_check_uses_ast_on_file_bytes(monkeypatch):
    ok, sha = R0._no_feedback_path()
    assert ok and len(sha) == 64
    real = R0._read_dynamics_bytes
    monkeypatch.setattr(R0, "_read_dynamics_bytes", lambda: real().replace(b"import numpy as np", b"import numpy as np\nfrom . import bridge", 1))
    assert R0._no_feedback_path()[0] is False
    monkeypatch.setattr(R0, "_read_dynamics_bytes", lambda: real() + b"\n# the word bridge in a comment is not an import\n")
    assert R0._no_feedback_path()[0] is True

def test_scalar_comparator_is_noncoercive():
    rep = R0.R0Report("PROVISIONAL", "env", None, {}); r = R0._R(rep); r.stage = "t"
    r.scalar("ok", 0.5, 0.5)
    with pytest.raises(R0.R0Halt) as ei:
        r.scalar("f32", np.float32(0.5), 0.5)                          # numerically equal, wrong dtype
    assert ei.value.record.failure_class == "comparator"
    rep2 = R0.R0Report("PROVISIONAL", "env", None, {}); r2 = R0._R(rep2); r2.stage = "t"
    with pytest.raises(R0.R0Halt) as ei2:
        r2.exact_int("count", 1.0, 1)                                    # float-valued counter refused
    assert ei2.value.record.failure_class == "comparator"
    rep3 = R0.R0Report("PROVISIONAL", "env", None, {}); r3 = R0._R(rep3); r3.stage = "t"
    with pytest.raises(R0.R0Halt):
        r3.exact_int("count", True, 1)                                   # bool refused

def test_labels_are_fail_closed():
    with pytest.raises(ValueError, match="unknown label"):
        R0.run_r0("/nonexistent", label="authoritative")
    with pytest.raises(ValueError, match="unknown label"):
        R0.run_r0_qualification("/nonexistent", record_dir="/tmp/x", label="CANONICAL")
    with pytest.raises(ValueError, match="record_dir is mandatory"):
        R0.run_r0("/nonexistent", label="AUTHORITATIVE")


# ======================= full run =======================
@needs_pin
def test_r0_full_run_passes_with_complete_provenance(tmp_path):
    rep = R0.run_r0(PIN, record_dir=str(tmp_path))
    assert rep.passed, rep.summary()
    assert dict(rep.checks) == dict(R0.FROZEN_COMPLETION["checks"]) and rep.comparator_evaluations == R0.FROZEN_COMPLETION["comparator_evaluations"]
    assert list(rep.refusals_verified) == list(R0.FROZEN_COMPLETION["refusals"]) and rep.stages_completed == list(R0.STAGES)
    for k in ("candidate_commit", "candidate_worktree_dirty", "candidate_dynamics_sha256", "dynamics_source_sha256", "bridge_source_sha256",
              "gate_r0_source_sha256", "governing", "frozen_case_map_sha256_literal", "frozen_ledger_sha256_literal",
              "frozen_completion_sha256_literal", "dynamics_file_sha256_at_ast_check"):
        assert k in rep.provenance, k
    assert "spec_sha256" not in rep.provenance and rep.provenance["governing"]["merge_specification_sha256"].startswith("39f66673")
    assert rep.provenance["candidate_dynamics_sha256"] == rep.provenance["dynamics_source_sha256"] == rep.provenance["dynamics_file_sha256_at_ast_check"]
    assert not os.listdir(tmp_path)                                    # PROVISIONAL: no success artifact

@needs_pin
def test_r0_refuses_joint_narrowing_against_the_unmodified_gate(monkeypatch, tmp_path):
    """BOTH the execution declaration and the frozen map are narrowed together; the UNMODIFIED gate
    must refuse at the static preflight by the literal digest, before any output."""
    narrowed = dict(R0.FROZEN_R0); narrowed["q1_grids"] = narrowed["q1_grids"][:3]
    import types
    monkeypatch.setattr(R0, "FROZEN_R0", types.MappingProxyType(narrowed))
    monkeypatch.setitem(R0.R0_CASES, "q1_grids", narrowed["q1_grids"])
    rep = R0.run_r0(PIN, record_dir=str(tmp_path))
    assert not rep.passed and rep.failure.check == "frozen_case_map_digest" and rep.stages_completed == [] and rep.checks == {}

@needs_pin
def test_r0_completion_refuses_missing_comparator_with_counts_preserved(monkeypatch, tmp_path):
    """Remove one Q4 comparator while keeping the stage count by a spurious extra check: the literal
    completion object refuses on evaluation total and check identity."""
    real = R0._R.scalar
    state = {"skipped": False}
    def scalar(self, check, observed, expected):
        if check == "morans_i" and not state["skipped"]:
            state["skipped"] = True; self.rep.checks[self.stage] = self.rep.checks.get(self.stage, 0) + 1; return   # counted, not evaluated
        return real(self, check, observed, expected)
    monkeypatch.setattr(R0._R, "scalar", scalar)
    rep = R0.run_r0(PIN, record_dir=str(tmp_path))
    assert not rep.passed and rep.failure.failure_class == "structural" and rep.failure.check == "frozen_evaluation_total"

@needs_pin
def test_r0_failure_grammar_classifies_comparator_and_stub(monkeypatch, tmp_path):
    from mfa_instrument.gates.gate_b import stub as S
    real = S.FrozenSequenceGenerator.random
    monkeypatch.setattr(S.FrozenSequenceGenerator, "random", lambda self, size=None, **k: (_ for _ in ()).throw(S.StubError("planted")))
    rep = R0.run_r0(PIN, record_dir=str(tmp_path))
    assert rep.failure.failure_class == "stub" and rep.failure.check == "frozen_sequence_stub" and rep.failure.stage == "q1"
    assert json.load(open(rep.failure.written_to))["case_id"].startswith("q1|")

@needs_pin
def test_r0_halts_with_bits_on_planted_instrument_defect(monkeypatch, tmp_path):
    from mfa_instrument import dynamics as D
    real = D._moore_sum_a
    monkeypatch.setattr(D, "_moore_sum_a", lambda x: real(x) + np.roll(x, 1, axis=0))
    rep = R0.run_r0(PIN, record_dir=str(tmp_path))
    assert rep.failure.check == "Local_Density_instrument" and rep.failure.stage == "q1" and rep.failure.expected != rep.failure.observed


# ======================= Q2 persistence negatives =======================
def _tamper_rho_table(monkeypatch, fn):
    from mfa_instrument import telemetry as T
    real_close = T.TelemetryWriter.close
    def close(self):
        real_close(self)
        if self.rho_global_path:
            df = pd.read_parquet(self.rho_global_path); fn(df).to_parquet(self.rho_global_path, index=False)
    monkeypatch.setattr(T.TelemetryWriter, "close", close)

@needs_pin
@pytest.mark.parametrize("name,fn,check", [
    ("shifted_tick", lambda df: df.assign(Tick=df["Tick"] + 1), "rho_global_table_tick"),
    ("dropped_tick", lambda df: df.iloc[:-1], "rho_global_table_shape"),
    ("reordered_rows", lambda df: df.iloc[::-1].reset_index(drop=True), "rho_global_table_tick"),
    ("post_update_value", lambda df: df.assign(rho_global=df["rho_global"].shift(-1).fillna(df["rho_global"].iloc[-1])), "rho_global_table_values"),
])
def test_q2_persisted_table_negatives(monkeypatch, tmp_path, name, fn, check):
    _tamper_rho_table(monkeypatch, fn)
    rep = R0.run_r0(PIN, record_dir=str(tmp_path))
    assert rep.failure.stage == "q2" and rep.failure.check == check, rep.failure.summary()

@needs_pin
def test_q2_omitted_rho_table_is_caught(monkeypatch, tmp_path):
    from mfa_instrument import telemetry as T
    real_close = T.TelemetryWriter.close
    def close(self): self.rho_global_table = []; real_close(self); self.rho_global_path = None
    monkeypatch.setattr(T.TelemetryWriter, "close", close)
    rep = R0.run_r0(PIN, record_dir=str(tmp_path))
    assert rep.failure.stage == "q2" and rep.failure.check == "rho_global_table_persisted"


# ======================= AUTHORITATIVE success rule =======================
@needs_pin
def test_authoritative_success_report_is_persisted_when_environment_conforms(monkeypatch, tmp_path):
    """The chosen rule (R12 option 1): run_r0 writes the AUTHORITATIVE success report atomically. The
    environment is artificially conformed here so the rule can be tested off the canonical machine."""
    from mfa_instrument.gates.gate_b import environment as E
    real = E.check_environment
    monkeypatch.setattr(R0, "check_environment", lambda root: E.EnvironmentRecord(**{**real(root).__dict__, "conforms": True, "failures": []}))
    rep = R0.run_r0(PIN, label="AUTHORITATIVE", record_dir=str(tmp_path))
    assert rep.passed and rep.written_to and os.path.isfile(rep.written_to)
    on_disk = json.load(open(rep.written_to))
    assert on_disk["kind"] == "r0_authoritative_report" and on_disk["passed"] is True and on_disk["label"] == "AUTHORITATIVE"
    assert b"\r\n" not in open(rep.written_to, "rb").read()

@needs_pin
def test_authoritative_refuses_nonconforming_environment_before_output(tmp_path):
    rep = R0.run_r0(PIN, label="AUTHORITATIVE", record_dir=str(tmp_path))
    from mfa_instrument.gates.gate_b.environment import check_environment
    if check_environment(PIN).conforms:
        pytest.skip("canonical environment conforms; refusal path not reachable here")
    assert rep.failure.failure_class == "environment" and rep.stages_completed == [] and rep.written_to is None


# ======================= qualification =======================
@needs_pin
def test_r0_qualification_passes_with_artifacts_bound(tmp_path):
    rec = R0.run_r0_qualification(PIN, record_dir=str(tmp_path))
    assert rec.passed, rec.summary()
    assert len(rec.mutants) == 28 and all(m.rejected and m.attributed and m.artifact_sha256 and os.path.isfile(m.artifact_path) for m in rec.mutants)
    by = {m.id: m for m in rec.mutants}
    assert by[16].observed_check == "dynamics_digest_consistency" and by[28].observed_check == "bridge_feedback_path" and by[28].observed_stage == "preflight"
    assert by[22].observed_check == "rho_tick_index" and by[23].observed_check == "rho_global_table_persisted"
    assert by[20].observed_case.startswith("q3|sink") and by[21].observed_case.startswith("q3|sink") and by[26].observed_check == "comparator_contract"
    assert rec.stages_completed == ["manifest_preflight", "positive_control", "mutants"]
    on_disk = json.load(open(rec.written_to))
    assert on_disk["passed"] is True and all(m["artifact_sha256"] for m in on_disk["mutants"])

@needs_pin
def test_r0_qualification_fails_on_survivor_alone(monkeypatch, tmp_path):
    R0._register_all()
    noop = lambda: contextlib.ExitStack(); noop.mutation_id = "bridge:divisor_9"
    monkeypatch.setitem(R0._R0_IMPL, "bridge:divisor_9", noop)
    rec = R0.run_r0_qualification(PIN, record_dir=str(tmp_path))
    assert not rec.passed and sum(not m.rejected for m in rec.mutants) == 1 and rec.mutants[1].detail == "NOT REJECTED"
    assert rec.positive_control["passed"] and all(m.rejected and m.attributed for m in rec.mutants if m.id != 2)

@needs_pin
def test_r0_qualification_fails_on_altered_implementation_identity(monkeypatch, tmp_path):
    R0._register_all()
    monkeypatch.setitem(R0._R0_IMPL, "bridge:divisor_9", R0._R0_IMPL["bridge:stencil_cardinal"])
    rec = R0.run_r0_qualification(PIN, record_dir=str(tmp_path))
    assert not rec.passed and rec.failure and "registry" in rec.failure and rec.mutants == []


# ======================= round-3 additions (L2 R0 round-2 verification) =======================
def test_scalar_contract_refuses_zero_dimensional_ndarray():
    with pytest.raises(BR.BridgeDomainError, match="float scalar required"):
        BR.q_response(Z(), np.array(0.5), 0.0, 0.0, H(), H(), H())
    with pytest.raises(BR.BridgeDomainError, match="float scalar required"):
        BR.local_read_dispersion(H(), np.array(0.5))
    assert BR.local_read_dispersion(H(), np.float64(0.5)) == 0.0                         # np.float64 scalar admissible

def test_finite_inputs_producing_nonfinite_output_are_refused():
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with pytest.raises(BR.BridgeDomainError, match="nonfinite"):
            BR.q_response(np.full((G, G), 1e308), 0.5, 10.0, 0.0, H(), H(), H())            # Γ·Ψ overflows
        x = np.where(np.indices((G, G))[0] % 2 == 0, 1e200, -1e200); y = np.where(np.indices((G, G))[1] % 2 == 0, 1e200, -1e200)
        with pytest.raises(BR.BridgeDomainError, match="nonfinite"):
            BR.config_neighbourhood_correlation(x, y)                                        # dx*dx overflows

def test_r0_governing_identity_is_r0s_own_not_gate_bs():
    from mfa_instrument.gates.gate_b import b1 as B1
    gov = R0.R0_GOVERNING
    assert gov["merge_specification_sha256"] == "39f66673657b0f429691c908142f889d9ef3d463a8372455cba95db7c486f52a"
    assert gov["merge_specification_sha256"] != B1.SPEC_SHA256 and gov["r0_design_declaration_sha256"] != B1.SPEC_SHA256
    src = open(R0.__file__, encoding="utf-8").read()          # explicit UTF-8: the source carries Ψ/Σ/− (Windows default is cp1252)
    assert "SPEC_SHA256" not in src.replace("R0_GOVERNING", "") and "spec_sha256" not in src.split("R0_GOVERNING")[0]

@needs_pin
def test_r0_refuses_same_total_comparator_substitution(monkeypatch, tmp_path):
    """One legitimate Q4 comparator is replaced by an extra invocation of ANOTHER comparator: stage
    count, evaluation total, refusals, and stage order all unchanged; the frozen ledger refuses."""
    real = R0._R.scalar
    state = {"done": False}
    def scalar(self, check, observed, expected):
        if check == "morans_i" and not state["done"]:
            state["done"] = True
            return real(self, "local_read_dispersion", 0.0, 0.0)       # same-stage substitution, same totals
        return real(self, check, observed, expected)
    monkeypatch.setattr(R0._R, "scalar", scalar)
    rep = R0.run_r0(PIN, record_dir=str(tmp_path))
    assert not rep.passed and rep.failure.check == "frozen_comparator_ledger"
    assert dict(rep.checks) == dict(R0.FROZEN_COMPLETION["checks"]) and rep.comparator_evaluations == R0.FROZEN_COMPLETION["comparator_evaluations"]

@needs_pin
def test_r0_refuses_inconsistent_dynamics_digests_mechanically(monkeypatch, tmp_path):
    real = R0._read_dynamics_bytes
    monkeypatch.setattr(R0, "_read_dynamics_bytes", lambda: real() + b"\n# trailing comment changes bytes, not imports\n")
    rep = R0.run_r0(PIN, record_dir=str(tmp_path))
    assert not rep.passed and rep.failure.failure_class == "provenance" and rep.failure.check == "dynamics_digest_consistency"

@needs_pin
def test_qualification_refuses_joint_manifest_and_registry_narrowing(monkeypatch, tmp_path):
    """Both the manifest and the registry are narrowed together; the unmodified qualification code
    refuses by the manifest's literal digest before the positive control."""
    R0._register_all()
    narrowed = R0.FROZEN_R0_MANIFEST[:5]
    monkeypatch.setattr(R0, "FROZEN_R0_MANIFEST", narrowed)
    keep = {mid for (_, _, _, mid, _, _, _) in narrowed}
    for mid in [m for m in list(R0._R0_IMPL) if m not in keep]:
        monkeypatch.delitem(R0._R0_IMPL, mid)
    monkeypatch.setattr(R0, "run_r0", lambda *a, **k: (_ for _ in ()).throw(AssertionError("positive control must not run")))
    rec = R0.run_r0_qualification(PIN, record_dir=str(tmp_path))
    assert not rec.passed and rec.failure and "literal digest" in rec.failure and rec.mutants == []

@needs_pin
def test_right_check_in_wrong_stage_is_unattributed(monkeypatch, tmp_path):
    """A mutant declared for Q4 that is rejected by the same-named check in the wrong stage/case must
    be UNATTRIBUTED (jurisdiction is part of attribution)."""
    R0._register_all()
    # declare mutant 13 (dispersion ddof1) as expecting stage q1 with a q1 case prefix: right check, wrong jurisdiction
    entries = list(R0.FROZEN_R0_MANIFEST)
    i13 = [k for k, e in enumerate(entries) if e[0] == 13][0]
    e = entries[i13]; entries[i13] = (e[0], e[1], e[2], e[3], e[4], "q1", ("q1|",))
    monkeypatch.setattr(R0, "FROZEN_R0_MANIFEST", tuple(entries))
    monkeypatch.setattr(R0, "FROZEN_R0_MANIFEST_SHA256_LITERAL", R0.frozen_map_digest({"manifest": tuple(entries)}))
    rec = R0.run_r0_qualification(PIN, record_dir=str(tmp_path))
    m13 = [m for m in rec.mutants if m.id == 13][0]
    assert m13.rejected and m13.observed_check == "local_read_dispersion" and not m13.attributed and "UNATTRIBUTED" in m13.detail and not rec.passed

def test_frozen_ledger_and_completion_bound_to_literal_digests():
    assert R0.frozen_map_digest(R0.FROZEN_LEDGER) == R0.FROZEN_LEDGER_SHA256_LITERAL
    assert R0.frozen_map_digest(R0.FROZEN_COMPLETION) == R0.FROZEN_COMPLETION_SHA256_LITERAL
    assert R0.frozen_map_digest({"manifest": R0.FROZEN_R0_MANIFEST}) == R0.FROZEN_R0_MANIFEST_SHA256_LITERAL
    assert sum(sum(v.values()) for v in R0.FROZEN_LEDGER.values()) == R0.FROZEN_COMPLETION["comparator_evaluations"] + len(R0.FROZEN_COMPLETION["refusals"])   # ledger = evaluations + refusal invocations


# ======================= round-4 additions (L2 R0 round-3 verification) =======================
def test_correlation_finite_intermediates_overflowing_product_is_correct_not_false_zero():
    """L2's witness: sxx, syy, sxy individually finite; sxx*syy overflows. The stable denominator
    returns the correct +1 (never the false finite 0 of sqrt(sxx*syy))."""
    idx = np.indices((G, G))
    x = np.where(idx[0] % 2 == 0, 1e90, -1e90).astype(np.float64)
    assert BR.config_neighbourhood_correlation(x, x) == 1.0
    assert BR.config_neighbourhood_correlation(x, -x) == -1.0
    y = np.where(idx[1] % 2 == 0, 1e90, -1e90).astype(np.float64)
    assert BR.config_neighbourhood_correlation(x, y) == 0.0                    # orthogonal patterns, huge magnitude

@needs_pin
def test_qualification_refuses_source_drift_after_positive_control(monkeypatch, tmp_path):
    """After the positive control, the reported bridge source identity changes while the in-memory
    implementation does not: qualification must refuse on the named consistency check."""
    R0._register_all()
    real = R0._file_sha
    state = {"n": 0}
    def sha(path):
        d = real(path)
        if os.path.abspath(path) == os.path.abspath(BR.__file__):
            state["n"] += 1
            if state["n"] > 2:                                              # entry read + positive control read stay true; later reads drift
                return "0" * 64
        return d
    monkeypatch.setattr(R0, "_file_sha", sha)
    rec = R0.run_r0_qualification(PIN, record_dir=str(tmp_path))
    assert not rec.passed and rec.failure and rec.failure.startswith("qualification_source_consistency") and "bridge_source_sha256" in rec.failure
    assert rec.positive_control["passed"] and rec.mutants == []

@needs_pin
def test_qualification_record_carries_baseline_bundle_and_mutants_match_it(tmp_path):
    rec = R0.run_r0_qualification(PIN, record_dir=str(tmp_path))
    assert rec.passed
    b = rec.provenance["baseline_identity_bundle"]
    assert b["bridge_source_sha256"] == rec.provenance["bridge_source_sha256"] and b["gate_r0_source_sha256"] == rec.provenance["gate_r0_source_sha256"]
    for m in rec.mutants:
        art = json.load(open(m.artifact_path))
        for k in R0.IDENTITY_BUNDLE_KEYS:
            assert art["provenance"].get(k) == b[k], (m.id, k)
        if m.mutation_id not in R0.IDENTITY_CHANNEL_MUTANTS:
            assert art["provenance"].get("dynamics_source_sha256") == b["dynamics_source_sha256"], m.id
