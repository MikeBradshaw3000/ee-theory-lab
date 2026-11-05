"""tests/test_f8_m7.py — Flight 8 stage-1 module M7 (E1-R grammar carried). Temporary committed repositories, independent of the real
repository's commit state. Covers: the frozen declaration and tamper; stage binding and its roles (environment, placement, governance,
adapter record and the platform match); the governance record's binding to the placed modules' values; authorization records, the append-only
registry and 'source literals grant nothing'; canonical persistence; F8 run artifacts in rehearsal at reduced shape (trace replay, re-execution
replay, tamper, status/label derivation); tranche and benchmark smoke; the derived per-item records; and ONE successful end-to-end chain at
PRODUCTION shape with M1's lattice stepper replaced by a deterministic synthetic stepper (M6 audits and the known-answer corpus stubbed consistently
for producer and validator; M5's finite-N count process stubbed for the projection sweeps, disclosed): canonical stage → authorized apparatus jobs →
tranche → committed prerequisite manifest → production authorization → READY → skeleton census + assessment → skeleton stability (independent
panel) → realization census + morphology → realization stability → p1_evaluation → atomic canonical package (the full proposed 29-item
specification). Round-2 additions (L2 r1 D1–D8): warm/cold memo equivalence, job→object execution boundary, s7.3 order incl. the direct route,
execution-metadata / canonical-bytes / slot binding, the complete package with the projection ensemble and the tolerance ensembles, the
pricing validator, typed governance binding, the exact clearance marker. The governance values used here are TEST STAND-INS;
the stability panel is M1's third declared panel (config.py touched with this round, disclosed)."""
import dataclasses as dc
import json
import math
import os
import shutil
import subprocess
import numpy as np
import pytest

from mfa_instrument.f8 import runner as R, config as C, closure as CL, evaluator as E, audit as A, classify as K, null as N, verdict as V, dynamics as D

INST = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(INST, "..", "..", ".."))
SMALL = dict(grid=10, ticks=1100)
L = C.F8_LEVELS_MICRO


def _git(root, *a): return subprocess.run(["git", "-C", root, *a], check=True, capture_output=True, text=True).stdout.strip()
def _commit(root, msg="c"): _git(root, "-c", "core.autocrlf=false", "add", "-A"); _git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", msg)
def _write_canon(path, obj): os.makedirs(os.path.dirname(path), exist_ok=True); open(path, "w", newline="\n").write(R._canon(R._encode(obj)))
def _rehash(obj, body_fn): return dc.replace(obj, result_sha256=R._digest(body_fn(obj)))


class _ConformingEnv:
    conforms = True; lock_sha256 = R._ENV.EXPECTED_LOCK_SHA256; pins = {f"p{i}": ("1", "1", True) for i in range(20)}; failures = []
    python_version = "3.14.4"; python_implementation = "CPython"; venv_active = True


def _base_repo(root):
    inst = os.path.join(root, R.INSTRUMENT_ROOT_REL)
    for rel, _ in R.BOUND_SOURCES + ((R.RUNNER_REL, ""), (R.M7_TEST_REL, "")):
        dst = os.path.join(inst, rel); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(os.path.join(INST, rel), dst)
    for rel in [r for r, _ in R._fixed_records()]:
        dst = os.path.join(root, rel); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(os.path.join(REPO, rel), dst)
    return inst


STABILITY_BUILD_DATE = 20261102     # the M1 touch's build date (Interpretation 003 pt 6): config.F8_STABILITY_MASTER = 9e8 + this


# ---- test stand-in governance values (NOT M7's; the real record is Mike's). The specification is the FULL proposed list (R.PACKAGE_ITEMS, 29 items).
_PRED = {"LevelListRecord": ("exists", "exists"), "EnsembleSizesRecord": ("exists", "exists"), "ClosurePublicationRecord": ("closure_covers_levels", "exists"), "NullLawRecord": ("null_law_certified", "null_law_certified"),
         "RouterCollisionRecord": ("exists", "exists"), "ConformanceRecord": ("conformance_production_passed", "conformance_production_passed"),
         "KnownAnswerQualification": ("known_answer_recorded", "known_answer_passed"), "AuditRecord": ("audit_record_complete", "audit_record_pass"), "AuditQualification": ("qualification_recorded", "qualification_qualified"),
         "PricingRecord": ("price_recorded", "price_recorded"), "CalibrationCensus": ("census_canonical", "census_ceilings_met"), "ToleranceEnsembles": ("tolerance_ensembles_complete", "tolerance_ensembles_complete"),
         "ToleranceProgram": ("tolerance_program_complete", "tolerance_program_complete"), "ReferenceStructure": ("reference_of_record_dense", "reference_resolved"), "StabilityAudit": ("stability_canonical", "stability_all_agree"),
         "SweepEnsemble": ("sweep_ensemble_canonical", "sweep_ensemble_canonical"), "DesignStability": ("design_complete", "design_stable"), "SweepRecord": ("sweep_canonical", "sweep_all_evaluable"),
         "SkeletonAssessment": ("skeleton_assessment_recorded", "skeleton_assessment_complete"), "StabilitySweep": ("sweep_stability", "sweep_stability"), "StabilityRecord": ("stability_record_recorded", "stability_record_reproduced"),
         "MorphologyRecord": ("morphology_recorded", "morphology_pass1_evaluated"), "P1Evaluation": ("p1_recorded", "p1_recorded"), "ResourceBenchmark": ("benchmark_canonical", "benchmark_fits")}
_DEPS = {"m6_audit_qualification": (("design", "m6_design_audit"), ("held_out", "m6_held_out_audit")), "tolerance_ensembles": (("census", "calibration_census"),), "tolerance_program": (("census", "calibration_census"),),
         "reference_stability": (("primary", "dense_reference"),), "design_stability": (("ref", "dense_reference"), ("sweeps", "projection_sweep_ensemble")),
         "skeleton_assessment": (("skeleton_high", "skeleton_high_sweep"), ("skeleton_low", "skeleton_low_sweep"), ("census", "calibration_census")),
         "skeleton_stability": (("canonical_sweep", "skeleton_high_sweep"), ("stability_sweep", "skeleton_stability_sweep"), ("census", "calibration_census")),
         "realization_stability": (("canonical_sweep", "realization_sweep"), ("stability_sweep", "realization_stability_sweep"), ("census", "calibration_census")),
         "p1_evaluation": (("skeleton_high", "skeleton_high_sweep"), ("skeleton_low", "skeleton_low_sweep"), ("realization", "realization_sweep"), ("census", "calibration_census"))}


ITEMS = tuple(R.PackageItem(n, ty, R.default_producer(n, ty), _PRED[ty][0], _PRED[ty][1], _DEPS.get(n, ())) for n, ty in R.PACKAGE_ITEMS)
VOCAB = tuple(i.name for i in ITEMS)
PREREQS = (("calibration_tranche", "apparatus", "pass"), ("resource_actuals", "apparatus", "pass"), ("mp1_known_answer", "qualification", "pass"),
           ("m6_audit_qualification", "qualification", "pass"), ("calibration_census", "apparatus", "pass"), ("dense_reference", "scientific", "valid_complete"))
JOBS = tuple(j for j in R.CANONICAL_JOBS if j != "m6_price")      # m6_price is granted by a later version in the chain (its refusal under v1 is a test)
MASTERS = (("seed_panel", C.F8_SEED_PANEL_MASTER), ("calibration", C.F8_CALIBRATION_MASTER), ("null_validation_attempt1", N.VALIDATION_REPLICATE_MASTER),
           ("null_validation_attempt2", N.VALIDATION_PROTOCOL_ATTEMPT_2.replicate_master), ("projection", CL.PROJECTION_MASTER), ("known_answer", E.KNOWN_ANSWER_MASTER),
           ("m6_design", 620261102), ("m6_held_out", 720261102), ("m6_pricing", 820261102))
RK = (("tolerance_ensembles", "ToleranceEnsemble"), ("tolerance_program", "ToleranceProgram"))


def _gov_rec(adapter_body, prereqs=PREREQS, branch=(), required=None, **over):
    cr = dict(R.CONTRACT_RECORDS)
    f = dict(version=1, claim_tier="finite-horizon persistence (test)", flight_name="F8 stage 1 (test)", contract_sha256=R.CONTRACT_RECORDS[0][1], freeze_record_sha256=R.CONTRACT_RECORDS[1][1],
             appendix_a_sha256=R.CONTRACT_RECORDS[2][1], interpretation_001_sha256=R.CONTRACT_RECORDS[3][1], interpretation_002_sha256=R.CONTRACT_RECORDS[4][1], ratification_record_sha256=R.CONTRACT_RECORDS[5][1], interpretation_003_sha256=R.CONTRACT_RECORDS[6][1],
             generator_declaration_markdown_sha256="c73980585fc238209453ebadb4707d961e41d77b7970435e8ce4113298868e47", generator_declaration_digest=A.GENERATOR_DECLARATION_SHA256_LITERAL,
             audit_declaration_digest=A.AUDIT_DECLARATION_SHA256_LITERAL, evaluator_declaration_digest=E.EVALUATOR_SHA256_LITERAL, closure_declaration_digest=CL.CLOSURE_SHA256_LITERAL,
             null_declaration_digest=N.NULL_SHA256_LITERAL, verdict_declaration_digest=V.VERDICT_DECLARATION_SHA256_LITERAL, classify_declaration_digest=K.CLASSIFY_SHA256_LITERAL,
             config_declaration_digest=C.F8_DECLARATION_SHA256_LITERAL, null_validation_protocol_sha256=N.VALIDATION_PROTOCOL_ATTEMPT_2_SHA256_LITERAL,
             null_validation_decision=R.NULL_VALIDATION_DECISION_OF_RECORD, placement_date=A.PLACEMENT_DATE, stability_master=R.stability_master(), stability_seed_panel_sha256=C.frozen_digest(R.stability_seed_panel()), masters=MASTERS,
             adapter_body_sha256=adapter_body, package_item_vocabulary=VOCAB, required_package_items=tuple(i.name for i in ITEMS) if required is None else required,
             production_prerequisites=prereqs, branch_stopping=branch, record_kind_mapping=RK)
    f.update(over)
    return _rehash(R.F8Governance(**f), R._gov_body)


def _spec_rec(gov_sha, items=ITEMS): return _rehash(R.PackageSpecification(1, gov_sha, items), R._spec_body)


def _auth(stage, version, prod_manifest="", jobs=JOBS):
    a = R.AuthorizationRecord(version, "2026-11-02", "test-stand-in", stage.result_sha256, stage.governance_sha256, stage.package_spec_sha256, jobs, True, tuple(L[:5]), tuple(C.F8_SEED_PANEL[:3]), bool(prod_manifest), prod_manifest)
    return _rehash(a, R._auth_body)


def _publish_auth(root, auth):
    gov = os.path.join(root, R.GOVERNANCE_ROOT_REL); p = os.path.join(gov, f"AUTHORIZATION_{auth.version:03d}.json"); _write_canon(p, auth)
    rp = os.path.join(gov, R.AUTHORIZATION_REGISTRY_REL); entries = R._read_canonical(rp).entries if os.path.isfile(rp) else ()
    _write_canon(rp, _rehash(R.AuthorizationRegistry(entries + ((auth.version, R._sha_file(p)),)), lambda r: r.entries)); _commit(root, f"authorization v{auth.version}")


def _place_and_govern(root, inst, *, governance=True, spec=True, adapter=True):
    c1 = _git(root, "log", "-1", "--format=%H")
    rsha = R._sha_file(os.path.join(inst, R.RUNNER_REL)); tsha = R._sha_file(os.path.join(inst, R.M7_TEST_REL)); gov = os.path.join(root, R.GOVERNANCE_ROOT_REL)
    clear_rel = "flights/mfa_fidelity/build_records/L2_F8_M7_TEST_CLEARANCE.md"
    os.makedirs(os.path.dirname(os.path.join(root, clear_rel)), exist_ok=True)
    open(os.path.join(root, clear_rel), "w", newline="\n").write(f"# test clearance\nrunner {rsha}\ntest {tsha}\nFINAL VERDICT: SOUND\n")
    sr = _rehash(R.M7SuiteRecord("python -m pytest tests -q -p no:cacheprovider", 900, 2, 0, rsha, tsha, c1), lambda s: (s.invocation, s.passed, s.skipped, s.failed, s.runner_sha256, s.m7_test_sha256, s.tested_commit))
    _write_canon(os.path.join(gov, R.SUITE_RECORD_REL), sr)
    pr = R.M7PlacementRecord(rsha, tsha, clear_rel, R._sha_file(os.path.join(root, clear_rel)), c1, R._sha_file(os.path.join(gov, R.SUITE_RECORD_REL)))
    _write_canon(os.path.join(gov, R.PLACEMENT_RECORD_REL), _rehash(pr, lambda p: (p.runner_sha256, p.m7_test_sha256, p.l2_clearance_file, p.l2_clearance_sha256, p.placement_commit, p.suite_record_sha256)))
    ad_body = None
    if adapter:
        R.write_adapter_record(root); ad_body = A.adapter_from_json(open(os.path.join(gov, R.ADAPTER_RECORD_REL), "rb").read().decode("ascii")).body_sha256
    g = None
    if governance:
        g = _gov_rec(ad_body or "0" * 64); _write_canon(os.path.join(gov, R.GOVERNANCE_REL), g)
        if spec: _write_canon(os.path.join(gov, R.PACKAGE_SPEC_REL), _spec_rec(R._sha_file(os.path.join(gov, R.GOVERNANCE_REL))))
    _commit(root, "placed + governed")
    return g


@pytest.fixture(scope="module")
def repo(tmp_path_factory):
    root = str(tmp_path_factory.mktemp("repo")); _base_repo(root); _git(root, "init", "-q"); _commit(root, "placed"); return root


@pytest.fixture(scope="module")
def stage(repo): return R.bind_stage(repo)


# ======================= identity =======================
def test_frozen_identity_and_declared_values():
    R.verify_frozen_identity()
    if "PENDING" not in R.RUNNER_DECLARATION_SHA256_LITERAL: assert R._digest(R.RUNNER_DECLARATION) == R.RUNNER_DECLARATION_SHA256_LITERAL
    assert R.PRODUCTION_RUNS == 3360 and R.BENCHMARK_MARGIN == 0.30 and R.SOURCE_LITERALS_GRANT_NOTHING is True
    assert len(R.stability_seed_panel()) == 20 and not set(R.stability_seed_panel()) & (set(C.F8_SEED_PANEL) | set(C.F8_CALIBRATION_SEED_PANEL) | set(C.E1_RETIRED_SEED_PANEL))
    assert R.stability_master() == 9 * 10**8 + STABILITY_BUILD_DATE == C.F8_STABILITY_MASTER and R.stability_seed_panel() == C.F8_STABILITY_SEED_PANEL and R.null_decision_from_records(REPO) == R.NULL_VALIDATION_DECISION_OF_RECORD
    assert set(j for j, _, _ in R.JOB_OBJECTS) == set(R.LATTICE_JOBS) and len(R.PACKAGE_ITEMS) == 29
    assert set(R.CANONICAL_JOBS) == {j for j, _, _ in R.JOB_GRAPH} and set(R.PREDICATE_IDS) == set(R.PREDICATES)
    assert dict(R.BOUND_SOURCES)["mfa_instrument/f8/null.py"] == R._sha_file(os.path.join(INST, "mfa_instrument/f8/null.py"))
    assert not hasattr(N.NullValidation, "is_qualification_evidence") and "price_familywise" not in open(os.path.join(INST, "mfa_instrument/f8/null.py"), encoding="utf-8").read()
    for rel, h in R.BOUND_SOURCES: assert R._sha_file(os.path.join(INST, rel)) == h, rel
    for rel, h in R._fixed_records(): assert R._sha_file(os.path.join(REPO, rel)) == h, rel


@pytest.mark.parametrize("name,bad", [("RUNNER_DECLARATION_SHA256_LITERAL", "0" * 64), ("PRODUCTION_RUNS", 2400), ("BENCHMARK_MARGIN", 0.5), ("SOURCE_LITERALS_GRANT_NOTHING", False), ("CANONICAL_JOBS", ("dense_reference",)), ("STABILITY_BUILD_DATE", 20261101)])
def test_tamper_is_caught(monkeypatch, name, bad):
    monkeypatch.setattr(R, name, bad)
    with pytest.raises(R.RunnerDomainError): R.verify_frozen_identity()


# ======================= stage binding =======================
def test_stage_binds_noncanonical_without_environment_and_rederives(repo, stage):
    assert stage.role == "noncanonical" and stage.placement_record_sha256 is None and stage.governance_sha256 is None and stage.adapter_file_sha256 is None and not stage.adapter_platform_match
    assert tuple(h for _, h in stage.contract_record_digests) == tuple(h for _, h in R.CONTRACT_RECORDS + R.DECLARATION_RECORDS) and stage.platform_tag == R.platform_tag()
    R.validate_stage_identity(stage, repo)
    with pytest.raises(R.RunnerDomainError): R.validate_stage_identity(dc.replace(stage, role="canonical"), repo)
    with pytest.raises(R.RunnerDomainError): R.validate_stage_identity(dc.replace(stage, result_sha256="0" * 64), repo)


def test_stage_refuses_tampered_source_crlf_and_uncommitted_surface(tmp_path):
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root)
    p = os.path.join(inst, "mfa_instrument/f8/classify.py"); b = open(p, "rb").read()
    open(p, "wb").write(b + b"\n# t\n")
    with pytest.raises(R.ApparatusHalt, match="differs from its cleared identity"): R.bind_stage(root)
    open(p, "wb").write(b)
    open(os.path.join(inst, R.RUNNER_REL), "ab").write(b"\n")
    with pytest.raises(R.ApparatusHalt, match="uncommitted"): R.bind_stage(root)
    _commit(root); R.bind_stage(root)


def test_stage_roles_with_placement_governance_and_adapter(tmp_path, monkeypatch):
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root)
    monkeypatch.setattr(R._ENV, "check_environment", lambda pr: _ConformingEnv())
    pinned = str(tmp_path / "pinned"); os.makedirs(pinned)
    assert R.bind_stage(root, pinned).role == "noncanonical"                          # conforming env, no placement
    _place_and_govern(root, inst, governance=False, adapter=False)
    s = R.bind_stage(root, pinned); assert s.role == "pre_governance" and s.placement_record_sha256 and s.adapter_file_sha256 is None
    R.write_adapter_record(root); _commit(root, "adapter")
    s = R.bind_stage(root, pinned); assert s.role == "pre_governance" and s.adapter_platform_match and s.adapter_body_sha256 == R._live_adapter().body_sha256
    gov = os.path.join(root, R.GOVERNANCE_ROOT_REL)
    _write_canon(os.path.join(gov, R.GOVERNANCE_REL), _gov_rec(s.adapter_body_sha256)); _write_canon(os.path.join(gov, R.PACKAGE_SPEC_REL), _spec_rec(R._sha_file(os.path.join(gov, R.GOVERNANCE_REL)))); _commit(root, "gov")
    s = R.bind_stage(root, pinned); assert s.role == "canonical"
    assert R.bind_stage(root).role == "noncanonical"                                  # same repo, no pinned root → never canonical
    # a committed adapter whose payload identity differs (another platform's record) keeps the platform-independent surface but is NOT a canonical stage
    a = A.adapter_from_json(open(os.path.join(gov, R.ADAPTER_RECORD_REL), "rb").read().decode("ascii"))
    other = dc.replace(a, payload_identity="f" * 64); other = dc.replace(other, body_sha256=other.identity())
    open(os.path.join(gov, R.ADAPTER_RECORD_REL), "w", newline="\n", encoding="ascii").write(A.adapter_to_json(other))
    _write_canon(os.path.join(gov, R.GOVERNANCE_REL), _gov_rec(other.body_sha256)); _write_canon(os.path.join(gov, R.PACKAGE_SPEC_REL), _spec_rec(R._sha_file(os.path.join(gov, R.GOVERNANCE_REL)))); _commit(root, "foreign adapter")
    s = R.bind_stage(root, pinned); assert s.role == "pre_governance" and not s.adapter_platform_match
    # a committed adapter whose SURFACE differs is an apparatus halt
    bad = dc.replace(a, keys=a.keys[:-1], n_pass2=a.n_pass2 - 1); bad = dc.replace(bad, body_sha256=bad.identity())
    open(os.path.join(gov, R.ADAPTER_RECORD_REL), "w", newline="\n", encoding="ascii").write(A.adapter_to_json(bad)); _commit(root, "bad adapter")
    with pytest.raises(R.ApparatusHalt): R.bind_stage(root, pinned)


def test_placement_record_facts_are_mechanically_verified(tmp_path, monkeypatch):
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root)
    monkeypatch.setattr(R._ENV, "check_environment", lambda pr: _ConformingEnv()); pinned = str(tmp_path / "p"); os.makedirs(pinned)
    _place_and_govern(root, inst, governance=False, adapter=False)
    gov = os.path.join(root, R.GOVERNANCE_ROOT_REL); pr = R._read_canonical(os.path.join(gov, R.PLACEMENT_RECORD_REL))
    bad = dc.replace(pr, placement_commit="0" * 40); bad = _rehash(bad, lambda p: (p.runner_sha256, p.m7_test_sha256, p.l2_clearance_file, p.l2_clearance_sha256, p.placement_commit, p.suite_record_sha256))
    _write_canon(os.path.join(gov, R.PLACEMENT_RECORD_REL), bad); _commit(root, "forged placement")
    with pytest.raises(R.ApparatusHalt, match="placement record"): R.bind_stage(root, pinned)


def test_governance_record_binds_to_the_placed_modules_values():
    g = _gov_rec("a" * 64); R.validate_governance(g)
    for field, bad in (("placement_date", 20261101), ("generator_declaration_digest", "0" * 64), ("contract_sha256", "0" * 64), ("interpretation_003_sha256", "0" * 64), ("interpretation_003_sha256", "822ad8d88ad093c906fe1a8d74cc802fecc5799b5b132594054b96997b7d6187"),   # R2-4: the draft's identity is not the ratified one
                       ("null_validation_decision", "PASSED at alpha 0.05"),
                       ("null_validation_decision", R.NULL_VALIDATION_DECISION_OF_RECORD[:-2] + (("attempt_1_status", "PASSED"), R.NULL_VALIDATION_DECISION_OF_RECORD[-1])),   # D7: the contradictory statement
                       ("null_validation_decision", tuple((k, (True if k == "module_default_dkw_passed" else v)) for k, v in R.NULL_VALIDATION_DECISION_OF_RECORD)),                  # D7: default-alpha passage reversed
                       ("generator_declaration_markdown_sha256", "0" * 64), ("generator_declaration_markdown_sha256", "f" * 64),                                                              # D7: arbitrary 64-hex identity
                       ("stability_master", 920261101), ("stability_seed_panel_sha256", "0" * 64),
                       ("masters", MASTERS[:-1]), ("record_kind_mapping", ()), ("production_prerequisites", (("dense_reference", "scientific", "valid_complete"),)),
                       ("production_prerequisites", (("mp1_known_answer", "qualification", "pass"), ("m6_audit_qualification", "qualification", "pass"))),                               # D3a: job 0 passage missing
                       ("production_prerequisites", (("mp1_known_answer", "qualification", "pass"), ("m6_audit_qualification", "qualification", "pass"), ("calibration_census", "apparatus", "valid_complete")))):   # D3a: weakened
        with pytest.raises(R.RunnerDomainError): R.validate_governance(_rehash(dc.replace(g, **{field: bad}), R._gov_body))
    with pytest.raises(R.RunnerDomainError): R.validate_governance(g, adapter_body_sha256="b" * 64)


# ======================= canonical persistence =======================
def test_persist_and_load_record_roundtrip_and_refusals(repo, stage, tmp_path):
    rec = R.level_list_record(stage); p = str(tmp_path / "ll.json")
    R.persist_record(rec, p, stage, repo)
    raw = open(p, "rb").read(); assert raw == R._canon(json.loads(raw)).encode() and b"\r" not in raw
    r2, fsha = R.load_record(p, "LevelListRecord", stage, repo); assert r2 == rec and fsha == R._sha_file(p)
    with pytest.raises(R.RunnerDomainError): R.load_record(p, "EnsembleSizesRecord", stage, repo)
    with pytest.raises(R.RunnerDomainError): R.load_record(p, "LevelListRecord", stage, repo, require_job="stage1_package")   # no authorization binding in the envelope
    open(p, "ab").write(b" ")
    with pytest.raises(R.RunnerDomainError, match="canonical byte form"): R.load_record(p, "LevelListRecord", stage, repo)
    with pytest.raises(R.RunnerDomainError): R.persist_record(dc.replace(rec, max_spacing_micro=1), p, stage, repo)


def test_authorization_structure_and_registry_rules(repo, stage, tmp_path):
    with pytest.raises(R.RunnerDomainError): R.AuthorizationRecord(1, "d", "i", "s", "g", "p", ("not_a_job",), False, (), (), False, "")
    with pytest.raises(R.RunnerDomainError): R.AuthorizationRecord(1, "d", "i", "s", "g", "p", (), True, tuple(L[:4]), tuple(C.F8_SEED_PANEL[:3]), False, "")
    with pytest.raises(R.RunnerDomainError): R.AuthorizationRecord(1, "d", "i", "s", "g", "p", (), False, (), (), True, "")
    with pytest.raises(R.RunnerDomainError): R.validate_authorization(_auth(stage, 1), stage)      # the stage is not canonical
    with pytest.raises(R.RunnerDomainError): R.load_authorization(repo, stage, 1)
    with pytest.raises(R.RunnerDomainError): R.require_authorized(stage, repo, None, 1, "dense_reference")
    with pytest.raises(R.RunnerDomainError): R.validate_registry(R.AuthorizationRegistry(((2, "a" * 64), (1, "b" * 64)), ""))


# ======================= F8 run artifacts (rehearsal, reduced shape) =======================
@pytest.fixture(scope="module")
def rehearsal(repo, stage, tmp_path_factory):
    out = str(tmp_path_factory.mktemp("runs"))
    rec = R.run_level(L[12], "realization", "canonical", out, stage, "rehearsal", **SMALL)
    return out, rec


def test_rehearsal_level_record_derives_from_artifacts_and_replays(repo, stage, rehearsal):
    out, rec = rehearsal
    assert rec.mode == "rehearsal" and rec.label == "" and rec.pass_number == 1 and len(rec.runs) == 20 and all(x.status == "" for x in rec.runs)
    ld = os.path.join(out, R._level_dirname(L[12], "realization", "canonical"))
    R.validate_level_record(rec, stage=stage, level_dir=ld)
    R._ARTIFACT_REPLAY_MEMO.clear(); R.validate_level_record(rec, stage=stage, level_dir=ld, replay=True)
    res = R.result_from_artifacts(ld, rec.runs[0], L[12], SMALL["grid"], SMALL["ticks"])
    assert res.rho_sha256() == rec.runs[0].rho_sha256 and res.spec_hash == rec.runs[0].spec_hash
    bad = dc.replace(rec, runs=rec.runs[:19] + (dc.replace(rec.runs[19], rho_tail_mean=0.5),))
    with pytest.raises(R.RunnerDomainError): R.validate_level_record(_rehash(bad, R._level_body), stage=stage, level_dir=ld)
    rp, _ = R._run_paths(ld, rec.runs[3].seed, "realization"); b = open(rp, "rb").read(); open(rp, "wb").write(b[:-1] + bytes([b[-1] ^ 1]))
    R._ARTIFACT_REPLAY_MEMO.clear()
    with pytest.raises(R.RunnerDomainError): R.validate_level_record(rec, stage=stage, level_dir=ld)
    open(rp, "wb").write(b)
    with pytest.raises(R.RunnerDomainError): R.validate_level_record(_rehash(dc.replace(rec, label="S"), R._level_body), stage=stage, level_dir=ld)
    with pytest.raises(R.RunnerDomainError): R.run_level(L[12] + 1, "realization", "canonical", out, stage, "rehearsal")        # off-grid at production shape
    with pytest.raises(R.RunnerDomainError): R.run_level(L[12], "realization", "canonical", out, stage, "production", job="realization_census", **SMALL)   # production needs repo + authorization


def test_tranche_and_benchmark_smoke_at_reduced_shape(repo, stage, tmp_path):
    q = R._tranche_for_tests(L[:5], C.F8_SEED_PANEL[:3], str(tmp_path), stage, **SMALL)
    assert q.status == "passed" and q.n_runs == 15 and q.cleanup_proven and not os.path.exists(os.path.join(str(tmp_path), ".tranche_sealed"))
    R.validate_quarantine(q, stage=stage); R.validate_quarantine(q, stage=stage, replay=True)
    with pytest.raises(R.QuarantineViolation): q.profile
    with pytest.raises(R.RunnerDomainError): R.validate_quarantine(_rehash(dc.replace(q, status="passed", cleanup_proven=False), R._q_body), stage=stage)
    with pytest.raises(R.RunnerDomainError): R._tranche_for_tests(L[:5], C.F8_SEED_PANEL[:3], str(tmp_path), stage, grid=C.F8_GRID, ticks=C.F8_TICKS)
    b = R.run_benchmark_smoke(2, str(tmp_path / "b"), stage, **SMALL)
    assert b.role == "smoke" and len(b.artifact_manifest) == 4 and b.projected_wall_clock_s > 0
    R.validate_benchmark(b, stage=stage, artifact_dir=str(tmp_path / "b" / "benchmark_artifacts"))
    with pytest.raises(R.RunnerDomainError): R.validate_benchmark(_rehash(dc.replace(b, fits_with_margin=not b.fits_with_margin), R._b_body), stage=stage)


# ======================= derived records =======================
def test_derived_records_rederive_and_refuse_tamper(repo, stage):
    ll = R.level_list_record(stage); R.validate_level_list(ll, stage=stage); assert ll.w_res_micro == 293478
    es = R.ensemble_sizes_record(stage); R.validate_ensemble_sizes(es, stage=stage); assert es.production_runs == 3360 and es.dense_points == 701
    nl = R.null_law_record(stage); R.validate_null_law(nl, stage=stage); assert (nl.index_p, nl.index_t) == (14341, 14121) and nl.protocol_sha256 == N.VALIDATION_PROTOCOL_ATTEMPT_2_SHA256_LITERAL
    rc = R.router_collision_record(stage); R.validate_router_collision(rc, stage=stage); assert rc.reachable_pass2_levels == 338 and rc.reachable_cases == 276
    cp = R.closure_publication_record(stage, repo); R.validate_closure_publication_record(cp, stage=stage, repo_root=repo); assert cp.max_abs_deviation <= cp.bind_tol and cp.delta_m == CL.delta_m().value
    cf = R.conformance_record(stage, **SMALL); R.validate_conformance_record(cf, stage=stage); assert cf.passed
    for rec, fn in ((ll, R.validate_level_list), (es, R.validate_ensemble_sizes), (nl, R.validate_null_law), (rc, R.validate_router_collision)):
        with pytest.raises(R.RunnerDomainError): fn(dc.replace(rec, result_sha256="0" * 64), stage=stage)
    with pytest.raises(R.RunnerDomainError): R.validate_null_law(_rehash(dc.replace(nl, index_p=14340), lambda r: ((r.index_p, r.index_t, r.mode_p, r.mode_t, r.error_bound, r.payload_identity, r.protocol_sha256, r.construction_bound), r.stage_sha256)), stage=stage)


# ======================= THE chain at production shape with a synthetic stepper =======================
def _synthetic_run(spec):
    """Deterministic stand-in for M1's lattice stepper at PRODUCTION shape: skeleton objects extinct below m = 1 (absorbing, zeros after the first
    zero), persistent above with density near rho*_sk; realization/null persistent near rho*(m) / pi1; per-seed jitter from the stream key."""
    spec = C.validate_run_spec(spec)
    g = C.generator_from_key(spec.stream_key); T, n = spec.ticks, spec.n_cells
    m = CL.level_m(spec.level_micro)
    if spec.obj.startswith("skeleton"):
        if m <= 1.0 + 0.02 * (spec.obj == "skeleton_low"):
            ext = int(g.integers(5, 400)); counts = np.zeros(T + 1, dtype=np.int64); counts[:ext] = np.maximum(1, (n * 0.02 * np.exp(-np.arange(ext) / 50.0)).astype(np.int64)); counts[0] = max(counts[0], 1)
            extinction, advanced = ext, ext
        else:
            base = CL.rho_sk(m); counts = np.clip(np.rint(n * (base + 0.003 * g.standard_normal(T + 1))), 1, n).astype(np.int64); extinction, advanced = None, T
    else:
        base = CL.rho_re(m) if spec.obj == "realization" else D.stationary_pi1(spec.eta_floor, spec.mu); counts = np.clip(np.rint(n * (base + 0.003 * g.standard_normal(T + 1))), 1, n).astype(np.int64); extinction, advanced = None, T
    rho = counts.astype(np.float64) / np.float64(n); tail = counts[T - spec.tail_ticks + 1:]; nwin = spec.tail_ticks // spec.window
    wins = tuple(float(np.float64(int(tail[i * spec.window:(i + 1) * spec.window].sum())) / np.float64(spec.window * n)) for i in range(nwin))
    surv = all(int(tail[i * spec.window:(i + 1) * spec.window].min()) > 0 for i in range(nwin))
    draws = (1 if spec.obj in ("realization", "null") else 0) + advanced          # M1's draw accounting (dynamics.run), so the derived metadata (D4a) agree
    return D.F8RunResult(spec.spec_hash(), spec.level_micro, spec.level_id, spec.seed, spec.obj, rho, counts, extinction, advanced, wins, bool(surv), float(np.float64(int(tail.sum())) / np.float64(spec.tail_ticks * n)), spec.stream_key, draws)


def _fake_finite_n_counts(m, eta, g, n=CL.N_CELLS, ticks=C.F8_TICKS, start_pi1=None):
    """Fast deterministic stand-in for M5's finite-N count process, used ONLY so the 200 projection sweeps (and their replay) run in seconds in
    the chain; producer and validator both go through it (disclosed stub; the real process is M5's and is tested in test_f8_m5)."""
    base = CL.rho_re(m); return np.clip(np.rint(n * (base + 0.003 * g.standard_normal(ticks + 1))), 0, n).astype(np.int64)


def _fake_audit(adapter):
    def fake(ens, ad):
        assert ad.body_sha256 == adapter.body_sha256
        scores = []
        for name in A.CLASSES:
            iv, ic = A.INTENDED[name]; kind = "false_nd" if name in A.SCIENTIFIC_CLASSES else "false_scientific"
            s = A.ClassScore(name, iv, ic, 500, 500, 0, 0, kind, 0, A.clopper_pearson_upper(0, 500), True, True, 1.0, 500, ((iv, 500),), ((8, 500),) if name in A.RAMP_CLASSES else (), ())
            A.validate_class_score(s, 500); scores.append(s)
        f = (A.AUDIT_VERSION, ens, A.production_masters()[0 if ens == "design" else 1], 500, "production", adapter.body_sha256, adapter.payload_identity, A.AUDIT_DECLARATION_SHA256_LITERAL,
             A.GENERATOR_DECLARATION_SHA256_LITERAL, A.INTERPRETATION_002_SHA256, tuple(scores), True)
        return A.AuditRecord(*f, A._digest(A.AuditRecord(*f, "").identity_body()))
    return fake


def _fake_known_answer(sweeps_per_class=E.KNOWN_ANSWER_SWEEPS, pass_min=E.KNOWN_ANSWER_PASS_MIN, master=E.KNOWN_ANSWER_MASTER, census=None, classes=E.KA_CLASSES):
    cen = E.synthetic_census()
    rows = tuple((cls, "PRODUCED", "", sweeps_per_class, 0, sweeps_per_class) for cls in classes)
    q = E.KnownAnswerQualification(int(master), int(sweeps_per_class), int(pass_min), rows, True, cen.result_sha256, True, E.EVALUATOR_SHA256_LITERAL)
    return dc.replace(q, result_sha256=q.identity())


@pytest.fixture(scope="module")
def chain(tmp_path_factory):
    mp = pytest.MonkeyPatch()
    try:
        root = str(tmp_path_factory.mktemp("chain")); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root)
        mp.setattr(R._ENV, "check_environment", lambda pr: _ConformingEnv()); pinned = str(tmp_path_factory.mktemp("pinned"))
        mp.setattr(R._D, "run", _synthetic_run); mp.setattr(E, "known_answer_qualification", _fake_known_answer); mp.setattr(CL, "finite_n_counts", _fake_finite_n_counts)
        _place_and_govern(root, inst)
        stage = R.bind_stage(root, pinned); assert stage.role == "canonical"
        adapter = R._stage_adapter(root, stage); mp.setattr(R._A, "run_audit", _fake_audit(adapter))
        _publish_auth(root, _auth(stage, 1))
        gov = os.path.join(root, R.GOVERNANCE_ROOT_REL); base = os.path.join(gov, "prerequisites"); out = os.path.join(base, "package")
        R.validate_stage_identity(stage, root, pinned)
        recs = {}
        # s7.1 order is executable (D3d): the design audit needs the known-answer record; the held-out audit needs the design audit
        with pytest.raises(R.RunnerDomainError, match="s7.3 order"): R.run_canonical_job("m6_design_audit", stage, root, out, pinned, 1)
        recs["mp1_known_answer"], _ = R.run_canonical_job("mp1_known_answer", stage, root, out, pinned, 1)
        with pytest.raises(R.RunnerDomainError, match="s7.3 order"): R.run_canonical_job("m6_held_out_audit", stage, root, out, pinned, 1)
        for job in ("m6_design_audit", "m6_held_out_audit", "m6_audit_qualification", "m6_price", "calibration_census", "tolerance_program", "dense_reference", "reference_stability", "projection_sweeps", "resource_benchmark"):
            if job == "m6_price":
                with pytest.raises(R.RunnerDomainError): R.run_canonical_job("m6_price", stage, root, out, pinned, 1)      # not in v1's authorized jobs (source literals grant nothing)
                _publish_auth(root, _auth(stage, 2, jobs=R.CANONICAL_JOBS)); recs[job], _ = R.run_canonical_job(job, stage, root, out, pinned, 2); continue
            recs[job], _ = R.run_canonical_job(job, stage, root, out, pinned, 1)
        q, qpath = R.run_tranche(base, stage, root, pinned, 1)
        # a scientific job under v1 (no production flag) is refused BEFORE any run
        with pytest.raises(R.RunnerDomainError, match="production flag"): R.run_canonical_job("skeleton_census", stage, root, out, pinned, 1)
        # the produced records are COMMITTED (prerequisites are committed files), then the manifest (the governance record's exact set) → production authorization v2 → readiness
        _commit(root, "apparatus records")
        gsha = R._sha_file(os.path.join(gov, R.GOVERNANCE_REL))
        def entry(name, rel, deps=()):
            fp = os.path.join(base, rel); rec = R.load_record(fp, R.PREREQ_TYPES[name], stage, root, pinned, require_job=R.PREREQ_JOBS[name], **R._prereq_context(R.PrerequisiteEntry(name, R.PREREQ_TYPES[name], rel, R._sha_file(fp), "0" * 64, deps), base, stage, root, pinned, fp))[0]
            return R.PrerequisiteEntry(name, R.PREREQ_TYPES[name], rel, R._sha_file(fp), R._item_identity(rec), deps)
        entries = (entry("calibration_tranche", "calibration_tranche.json"), entry("resource_actuals", "package/resource_benchmark.json"), entry("mp1_known_answer", "package/mp1_known_answer.json"),
                   entry("calibration_census", "package/calibration_census.json"), entry("dense_reference", "package/dense_reference.json"),
                   entry("m6_audit_qualification", "package/m6_audit_qualification.json", (("design", "package/m6_design_audit.json", R._sha_file(os.path.join(base, "package/m6_design_audit.json"))), ("held_out", "package/m6_held_out_audit.json", R._sha_file(os.path.join(base, "package/m6_held_out_audit.json"))))))
        man = _rehash(R.ProductionPrerequisiteManifest(gsha, entries), R._manifest_body); _write_canon(os.path.join(gov, R.PREREQ_MANIFEST_REL), man); _commit(root, "prerequisites")
        _publish_auth(root, _auth(stage, 3, R._sha_file(os.path.join(gov, R.PREREQ_MANIFEST_REL))))
        rd = R.validate_prerequisites(R.load_authorization(root, stage, 3)[0], stage, root, pinned)
        # s7.3 order (D3b): realization cannot start before the skeleton census, its assessment AND the skeleton stability record exist — on the job route and the direct level route
        with pytest.raises(R.RunnerDomainError, match="s7.3 order"): R.run_canonical_job("realization_census", stage, root, out, pinned, 3)
        with pytest.raises(R.RunnerDomainError, match="s7.3 order"): R.run_level(L[0], "realization", "canonical", out, stage, "production", job="realization_census", adapter=adapter, repo_root=root, pinned_root=pinned, authorization_version=3)
        recs["skeleton_census"], _ = R.run_canonical_job("skeleton_census", stage, root, out, pinned, 3)
        with pytest.raises(R.RunnerDomainError, match="s7.3 order"): R.run_canonical_job("realization_census", stage, root, out, pinned, 3)     # assessment exists, stability does not
        # I003 pt 7 (R2-6): a stability job follows its census COMMITTED — valid but uncommitted census evidence is refused on both routes, BEFORE any run
        def boom(*a, **k): raise _Sentinel()
        with mp.context() as m2:
            m2.setattr(R, "_execute_run", boom)
            with pytest.raises(R.RunnerDomainError, match="COMMITTED"): R.run_canonical_job("skeleton_stability", stage, root, out, pinned, 3)
            with pytest.raises(R.RunnerDomainError, match="COMMITTED"): R.run_level(L[0], "skeleton_high", "stability", out, stage, "production", job="skeleton_stability", adapter=adapter, repo_root=root, pinned_root=pinned, authorization_version=3)
        _commit(root, "skeleton census committed")
        recs["skeleton_stability"], _ = R.run_canonical_job("skeleton_stability", stage, root, out, pinned, 3)
        recs["realization_census"], _ = R.run_canonical_job("realization_census", stage, root, out, pinned, 3)
        with pytest.raises(R.RunnerDomainError, match="COMMITTED"): R.run_canonical_job("realization_stability", stage, root, out, pinned, 3)
        _commit(root, "realization census committed")
        for job in ("realization_stability", "p1_evaluation", "stage1_package"):
            recs[job], _ = R.run_canonical_job(job, stage, root, out, pinned, 3)
        yield dict(root=root, inst=inst, pinned=pinned, stage=stage, adapter=adapter, out=out, base=base, recs=recs, tranche=q, tranche_path=qpath, readiness=rd, entries=entries, manifest=man)
    finally:
        mp.undo()


def test_chain_canonical_jobs_produced_authorized_records(chain):
    recs = chain["recs"]; stage = chain["stage"]
    assert recs["calibration_census"].role == "canonical" and recs["calibration_census"].ceilings_met in (True, False)
    assert recs["tolerance_program"].complete and recs["dense_reference"].role == "reference_of_record" and recs["reference_stability"].role == "canonical"
    assert type(recs["skeleton_census"]) is R.SkeletonAssessment and recs["skeleton_census"].complete and recs["skeleton_census"].t_s1_prime.test == "T-S1'"
    assert recs["realization_census"].verdict in V.VERDICTS and recs["realization_census"].verdict_scope == "pass-1 level set" and recs["realization_census"].final_set_obligation in ("open", "discharged_identically")
    assert recs["projection_sweeps"].role == "canonical" and recs["m6_price"].replicates == A.PRICING_REPLICATES
    assert recs["skeleton_stability"].obj == "skeleton_high" and recs["realization_stability"].obj == "realization" and recs["p1_evaluation"].role == "canonical"
    assert recs["p1_evaluation"].determination in ("PRODUCED", "NOT PRODUCED", "NOT DISTINGUISHED") and recs["resource_benchmark"].role == "canonical"
    pkg = recs["stage1_package"]; assert pkg.role == "canonical" and pkg.complete and len(pkg.items) == len(ITEMS) and pkg.stage_sha256 == stage.result_sha256
    doc = json.loads(open(os.path.join(chain["out"], "calibration_census.json"), "rb").read())
    assert doc["job"] == "calibration_census" and doc["authorization_version"] == 1 and doc["stage_sha256"] == stage.result_sha256
    for m in L:
        for obj, panel in (("skeleton_high", "calibration"), ("realization", "calibration"), ("skeleton_high", "canonical"), ("skeleton_low", "canonical"), ("realization", "canonical"), ("skeleton_high", "stability"), ("realization", "stability")):
            assert os.path.isfile(os.path.join(chain["out"], R._level_file(m, obj, panel)))
    assert os.path.isfile(os.path.join(chain["out"], "tolerance_ensembles.json")) and os.path.isfile(os.path.join(chain["out"], "projection_sweeps.ensemble.json"))


def test_chain_census_role_is_issued_only_by_m7_and_replays(chain):
    c = chain["recs"]["calibration_census"]; st = chain["stage"]
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census([], "canonical")
    R.validate_calibration_census(c, stage=st, repo_root=chain["root"], pinned_root=chain["pinned"], records_dir=chain["out"], adapter=chain["adapter"])
    forged = dc.replace(c, ceilings_met=not c.ceilings_met, stop_path_triggered=c.ceilings_met); forged = dc.replace(forged, result_sha256=forged.identity())
    with pytest.raises((R.RunnerDomainError, CL.ClosureDomainError)): R.validate_calibration_census(forged, stage=st, repo_root=chain["root"], pinned_root=chain["pinned"], records_dir=chain["out"], adapter=chain["adapter"])


def test_chain_package_replays_and_refuses_forgery(chain):
    pkg = chain["recs"]["stage1_package"]; st = chain["stage"]
    R.validate_stage_package(pkg, stage=st, repo_root=chain["root"], pinned_root=chain["pinned"], package_dir=chain["out"], adapter=chain["adapter"])
    forged = dc.replace(pkg, all_items_pass=not pkg.all_items_pass); forged = dc.replace(forged, result_sha256=R._digest(R._pkg_body(forged)))
    with pytest.raises(R.RunnerDomainError): R.validate_stage_package(forged, stage=st, repo_root=chain["root"], pinned_root=chain["pinned"], package_dir=chain["out"], adapter=chain["adapter"])
    with pytest.raises(R.RunnerDomainError): R.run_canonical_job("dense_reference", st, chain["root"], chain["out"], chain["pinned"], 9)   # no such authorization version
    # D5: the proposed specification without the projection ensemble cannot validate; without the tolerance ensembles it is not the ratified mapping's package
    spec, _ = R.load_package_spec(chain["root"], st)
    assert len(spec.items) == 29
    with pytest.raises(R.RunnerDomainError, match="SweepEnsemble"): R.validate_package_spec(_spec_rec(spec.governance_sha256, tuple(i for i in spec.items if i.name != "projection_sweep_ensemble")))


def test_chain_production_readiness_from_committed_prerequisites(chain):
    root, st, pinned, out, base = chain["root"], chain["stage"], chain["pinned"], chain["out"], chain["base"]; rd = chain["readiness"]; entries = chain["entries"]
    gov = os.path.join(root, R.GOVERNANCE_ROOT_REL); gsha = R._sha_file(os.path.join(gov, R.GOVERNANCE_REL))
    assert rd.all_valid_complete and rd.production_ready and {r[0] for r in rd.rows} == {e.name for e in entries}
    sh = R.load_record(os.path.join(out, "skeleton_high_sweep.json"), "SweepRecord", st, root, pinned, require_job="skeleton_census", records_dir=out, adapter=chain["adapter"])[0]
    lvl = R.load_record(os.path.join(out, R._level_file(L[0], "skeleton_high", "canonical")), "LevelRecord", st, root, pinned, require_job="skeleton_census", level_dir=os.path.join(out, R._level_dirname(L[0], "skeleton_high", "canonical")), adapter=chain["adapter"], records_dir=out)[0]
    assert lvl.job == "skeleton_census" and lvl.authorization_version == 3 and lvl.prerequisite_identities and sh.role == "canonical"
    cal = R.load_record(os.path.join(out, R._level_file(L[0], "realization", "calibration")), "LevelRecord", st, root, pinned, require_job="calibration_census", level_dir=os.path.join(out, R._level_dirname(L[0], "realization", "calibration")), adapter=chain["adapter"], records_dir=out)[0]
    assert cal.job == "calibration_census" and cal.authorization_version == 1 and cal.prerequisite_identities == ()
    # a partial prerequisite set is refused
    short = _rehash(R.ProductionPrerequisiteManifest(gsha, entries[:-1]), R._manifest_body); _write_canon(os.path.join(gov, R.PREREQ_MANIFEST_REL), short); _commit(root, "short")
    _publish_auth(root, _auth(st, 4, R._sha_file(os.path.join(gov, R.PREREQ_MANIFEST_REL))))
    with pytest.raises(R.RunnerDomainError, match="exact production set"): R.validate_prerequisites(R.load_authorization(root, st, 4)[0], st, root, pinned)
    _write_canon(os.path.join(gov, R.PREREQ_MANIFEST_REL), chain["manifest"]); _commit(root, "restore")
    with pytest.raises(R.EvaluabilityHalt): R.run_level(L[0] + 1, "realization", "canonical", os.path.join(root, "prod"), st, "production", job="realization_census", adapter=chain["adapter"], repo_root=root, pinned_root=pinned, authorization_version=3)
    with pytest.raises(R.RunnerDomainError): R.run_level(L[0], "realization", "canonical", os.path.join(root, "prod"), st, "production", job="realization_census", adapter=chain["adapter"], repo_root=root, pinned_root=pinned, authorization_version=1)   # v1 grants no production
    with pytest.raises(R.RunnerDomainError): R.run_level(L[0], "realization", "calibration", os.path.join(root, "prod"), st, "production", job="realization_census", adapter=chain["adapter"], repo_root=root, pinned_root=pinned, authorization_version=3)   # calibration panel is job 0's alone


def test_chain_registry_is_append_only_and_versions_immutable(chain):
    root, st = chain["root"], chain["stage"]; gov = os.path.join(root, R.GOVERNANCE_ROOT_REL)
    p = os.path.join(gov, "AUTHORIZATION_001.json"); a = R._read_canonical(p); before = _git(root, "rev-parse", "HEAD")
    try:
        _write_canon(p, _rehash(dc.replace(a, authorized_jobs=R.CANONICAL_JOBS), R._auth_body)); _commit(root, "rewrite v1")
        with pytest.raises(R.RunnerDomainError): R.load_authorization(root, st, 1)
        _git(root, "checkout", "HEAD~1", "--", "flights/mfa_fidelity/governance/f8_stage1/AUTHORIZATION_001.json"); _commit(root, "restore v1")
        with pytest.raises(R.RunnerDomainError, match="commits in its history"): R.load_authorization(root, st, 1)
    finally:
        _git(root, "reset", "--hard", before)          # the shared fixture repository is returned to its pre-tamper commit
    R.load_authorization(root, st, 1)


def test_chain_tranche_record_replays_and_quarantine_holds(chain):
    q = chain["tranche"]; st = chain["stage"]
    assert q.status == "passed" and q.authorization_version == 1
    R.validate_quarantine(q, stage=st, repo_root=chain["root"], pinned_root=chain["pinned"], replay=True)
    rec, _ = R.load_record(chain["tranche_path"], "TrancheQuarantine", st, chain["root"], chain["pinned"], require_job="calibration_tranche", replay=True)
    assert rec == q
    with pytest.raises(R.QuarantineViolation): q.labels


def test_chain_morphology_and_stability_records_rederive(chain):
    st = chain["stage"]; recs = chain["recs"]; out = chain["out"]; ad = chain["adapter"]
    m = recs["realization_census"]
    R.validate_morphology(m, stage=st, repo_root=chain["root"], pinned_root=chain["pinned"], records_dir=out, adapter=ad)
    assert len(m.insertion_halts) == len(m.insertions_micro) and m.verdict_scope == "pass-1 level set" and m.final_set_identical_to_pass1 == (m.insertions_micro == ()) and m.final_set_obligation == ("discharged_identically" if not m.insertions_micro else "open")
    with pytest.raises(R.RunnerDomainError): R.validate_morphology(_rehash(dc.replace(m, verdict_scope="final level set"), R._morph_body), stage=st, repo_root=chain["root"], pinned_root=chain["pinned"], records_dir=out, adapter=ad)
    sh = R.load_record(os.path.join(out, "skeleton_high_sweep.json"), "SweepRecord", st, chain["root"], chain["pinned"], require_job="skeleton_census", records_dir=out, adapter=ad)[0]
    ssw = R.load_record(os.path.join(out, "skeleton_stability_sweep.json"), "StabilitySweep", st, chain["root"], chain["pinned"], require_job="skeleton_stability", records_dir=out, adapter=ad)[0]
    assert ssw.panel == "stability" and ssw.sweep.role == "synthetic" and ssw.stability_master == R.stability_master() and tuple(m for m, _, _ in ssw.level_records) == tuple(L)
    cen = recs["calibration_census"]; s = recs["skeleton_stability"]
    R.validate_stability_record(s, stage=st, canonical_sweep=sh, stability_sweep=ssw, census=cen)
    forged = dc.replace(s, reproduced=not s.reproduced); forged = _rehash(forged, R._stab_body)
    with pytest.raises(R.RunnerDomainError): R.validate_stability_record(forged, stage=st, canonical_sweep=sh, stability_sweep=ssw, census=cen)
    # the calibration panel is never assembled into a scorable sweep (Interpretation 003 pt 9)
    with pytest.raises(R.RunnerDomainError): R._sweep_from_level_records("skeleton_high", {}, {}, "calibration")
    # the skeleton assessment replays and refuses a flipped test outcome
    ska = recs["skeleton_census"]; sl = R.load_record(os.path.join(out, "skeleton_low_sweep.json"), "SweepRecord", st, chain["root"], chain["pinned"], require_job="skeleton_census", records_dir=out, adapter=ad)[0]
    R.validate_skeleton_assessment(ska, stage=st, skeleton_high=sh, skeleton_low=sl, census=cen)
    bad = _rehash(dc.replace(ska, t_s1_prime=dc.replace(ska.t_s1_prime, outcome="FAIL" if ska.t_s1_prime.outcome != "FAIL" else "PASS")), R._ska_body)
    with pytest.raises(R.RunnerDomainError): R.validate_skeleton_assessment(bad, stage=st, skeleton_high=sh, skeleton_low=sl, census=cen)
    # the tolerance ensembles are a record kind of their own and replay from the census (D5b)
    te = R.load_record(os.path.join(out, "tolerance_ensembles.json"), "ToleranceEnsembles", st, chain["root"], chain["pinned"], require_job="tolerance_program", census=cen)[0]
    assert te.complete and len(te.ensembles) == 24 and all(type(e) is CL.ToleranceEnsemble for e in te.ensembles)
    for bad in (dc.replace(te, ensembles=te.ensembles[:23]), dc.replace(te, ensembles=te.ensembles[1:] + te.ensembles[:1]), dc.replace(te, ensembles=te.ensembles[:5] + (dc.replace(te.ensembles[5], s_hat_re=te.ensembles[5].s_hat_re + 1e-6),) + te.ensembles[6:])):
        with pytest.raises(R.RunnerDomainError): R.validate_tolerance_ensembles(_rehash(bad, R._tol_body), stage=st, census=cen)


# ======================= round-2 negatives (L2 r1 D1–D8) =======================
class _Sentinel(Exception): ...


def test_d2_job_object_boundary_refused_before_the_first_run(chain, monkeypatch):
    """D2: a forbidden (job, object, panel) is refused BEFORE execution; a permitted one reaches the execution sentinel."""
    root, st, pinned, ad = chain["root"], chain["stage"], chain["pinned"], chain["adapter"]; out = os.path.join(root, "boundary")
    def boom(*a, **k): raise _Sentinel()
    monkeypatch.setattr(R, "_execute_run", boom)
    for job, obj, panel in (("skeleton_census", "realization", "canonical"), ("realization_census", "skeleton_high", "canonical"), ("calibration_census", "null", "calibration"),
                            ("calibration_census", "skeleton_low", "calibration"), ("skeleton_stability", "skeleton_low", "stability"), ("realization_stability", "skeleton_high", "stability"),
                            ("skeleton_census", "skeleton_high", "stability"), ("realization_census", "realization", "calibration")):
        with pytest.raises(R.RunnerDomainError): R.run_level(L[0], obj, panel, out, st, "production", job=job, adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=1 if job == "calibration_census" else 3)
    with pytest.raises(_Sentinel): R.run_level(L[0], "skeleton_high", "calibration", out, st, "production", job="calibration_census", adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=1)
    assert not R._job_permits("calibration_census", "null", "calibration") and R._job_of("skeleton_low", "canonical") == "skeleton_census" and R._job_of("realization", "stability") == "realization_stability"
    with pytest.raises(R.RunnerDomainError): R._job_of("null", "canonical")


def test_d4_execution_metadata_canonical_bytes_and_slot_binding(repo, stage, rehearsal, tmp_path):
    out, rec = rehearsal; ld = os.path.join(out, R._level_dirname(L[12], "realization", "canonical"))
    x = rec.runs[2]; _, jp = R._run_paths(ld, x.seed, "realization"); original = open(jp, "rb").read()
    try:
        for field, bad in (("ticks_advanced", -17), ("draws_consumed", -23), ("extinction_tick", 42), ("ticks_advanced", x.ticks_advanced - 1), ("draws_consumed", x.draws_consumed + 1)):
            forged = dc.replace(x, **{field: bad}); open(jp, "w", newline="\n").write(R._canon(R._encode(forged)))
            lv = _rehash(dc.replace(rec, runs=rec.runs[:2] + (forged,) + rec.runs[3:]), R._level_body); R._ARTIFACT_REPLAY_MEMO.clear()
            with pytest.raises(R.RunnerDomainError, match="execution metadata|differs"): R.validate_level_record(lv, stage=stage, level_dir=ld)
            with pytest.raises(R.RunnerDomainError): R._check_provenance(ld, forged, L[12], SMALL["grid"], SMALL["ticks"], None, "rehearsal", True)     # re-execution replay too
        # D4b: equivalent but non-canonical bytes are refused
        open(jp, "w", newline="\n").write(json.dumps(json.loads(original), indent=2) + "\n"); R._ARTIFACT_REPLAY_MEMO.clear()
        with pytest.raises(R.RunnerDomainError, match="canonical byte form|differs"): R.validate_level_record(rec, stage=stage, level_dir=ld)
    finally:
        open(jp, "wb").write(original)
    R._ARTIFACT_REPLAY_MEMO.clear(); R.validate_level_record(rec, stage=stage, level_dir=ld)
    # D4c: a record valid for its own slot is not evidence for another
    R.require_level_slot(rec, L[12], "realization", "canonical", "", mode="rehearsal")
    for args in ((L[11], "realization", "canonical", ""), (L[12], "skeleton_high", "canonical", ""), (L[12], "realization", "calibration", ""), (L[12], "realization", "canonical", "realization_census")):
        with pytest.raises(R.RunnerDomainError): R.require_level_slot(rec, *args, mode="rehearsal")


def test_d4c_morphology_refuses_copied_level_files(chain):
    """One level's valid realization record copied into another slot: refused on load through the slot binding (previously accepted)."""
    root, st, pinned, ad, out = chain["root"], chain["stage"], chain["pinned"], chain["adapter"], chain["out"]
    src_f = os.path.join(out, R._level_file(L[3], "realization", "canonical")); dst_f = os.path.join(out, R._level_file(L[4], "realization", "canonical"))
    src_d = os.path.join(out, R._level_dirname(L[3], "realization", "canonical")); dst_d = os.path.join(out, R._level_dirname(L[4], "realization", "canonical"))
    keep_f = open(dst_f, "rb").read(); tmp_d = dst_d + ".keep"; os.rename(dst_d, tmp_d)
    try:
        shutil.copyfile(src_f, dst_f); shutil.copytree(src_d, dst_d)
        with pytest.raises(R.RunnerDomainError, match="not the production record of"): R._load_level_results(out, "realization", "canonical", st, root, pinned, ad)
        m = chain["recs"]["realization_census"]
        with pytest.raises(R.RunnerDomainError): R.validate_morphology(m, stage=st, repo_root=root, pinned_root=pinned, records_dir=out, adapter=ad)
    finally:
        shutil.rmtree(dst_d); os.rename(tmp_d, dst_d); open(dst_f, "wb").write(keep_f)
    R._load_level_results(out, "realization", "canonical", st, root, pinned, ad)


def test_d6_pricing_record_must_be_the_declared_experiment(chain):
    st, root, pinned, ad = chain["stage"], chain["root"], chain["pinned"], chain["adapter"]; r = chain["recs"]["m6_price"]
    R._v_price(r, adapter=ad)
    with pytest.raises(R.RunnerDomainError): R._v_price(r)
    for field, bad in (("replicates", 9999), ("master", 1), ("theta_p", -7.0), ("theta_t", 900.0), ("alpha_p_nominal", 0.8), ("construction_bound", -5.0), ("s_term_no_sustained", -1), ("s_term_no_sustained", r.s_term_no_sustained + 1),
                       ("source", "wrong_source"), ("declaration_sha256", "0" * 64), ("s_min_rejections", r.s_min_rejections + 1)):
        forged = dc.replace(r, **{field: bad})
        if field == "s_min_rejections": forged = dc.replace(forged, s_min_rejection_rate=forged.s_min_rejections / forged.replicates, cp_upper_95=A.clopper_pearson_upper(forged.s_min_rejections, forged.replicates))   # arithmetic consistent — still another experiment
        with pytest.raises(R.RunnerDomainError): R._v_price(forged, adapter=ad)
    # L2's probe record: arithmetically self-consistent, from no declared experiment
    probe = A.PricingRecord(10000, 1, -7.0, 900.0, 0, 0.0, A.clopper_pearson_upper(0, 10000), 0.8, -5.0, -1, "wrong_source", "0" * 64)
    with pytest.raises(R.RunnerDomainError): R._v_price(probe, adapter=ad)


def test_d8_clearance_requires_the_exact_final_verdict_marker(tmp_path, monkeypatch):
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root)
    monkeypatch.setattr(R._ENV, "check_environment", lambda pr: _ConformingEnv()); pinned = str(tmp_path / "p"); os.makedirs(pinned)
    _place_and_govern(root, inst, governance=False, adapter=False)
    pr = R._read_canonical(os.path.join(root, R.GOVERNANCE_ROOT_REL, R.PLACEMENT_RECORD_REL)); cf = os.path.join(root, pr.l2_clearance_file)
    rsha, tsha = pr.runner_sha256, pr.m7_test_sha256
    def place_clearance(text):
        open(cf, "w", newline="\n").write(text); _commit(root, "clearance")
        p2 = _rehash(dc.replace(pr, l2_clearance_sha256=R._sha_file(cf)), lambda p: (p.runner_sha256, p.m7_test_sha256, p.l2_clearance_file, p.l2_clearance_sha256, p.placement_commit, p.suite_record_sha256))
        _write_canon(os.path.join(root, R.GOVERNANCE_ROOT_REL, R.PLACEMENT_RECORD_REL), p2); _commit(root, "placement")
    head = f"runner {rsha}\ntest {tsha}\n"
    for adverse in (head + "FINAL VERDICT: DEFECT-WITH-REPAIR\nSOUND withheld pending repairs.\n", head + "FINAL VERDICT: DEFECT-WITH-REPAIR\nThe earlier round said 'FINAL VERDICT: SOUND' — superseded.\n",
                    head + "not SOUND\n", head + "FINAL VERDICT: SOUND\nFINAL VERDICT: DEFECT-WITH-REPAIR\n", head + "SOUND\n", head + "  FINAL VERDICT: SOUND (conditional)\n"):
        place_clearance(adverse)
        with pytest.raises(R.RunnerDomainError, match="FINAL VERDICT: SOUND"): R.verify_placement(root, rsha, tsha)
        with pytest.raises(R.ApparatusHalt): R.bind_stage(root, pinned)
    # R2-3: historical / quoted positives never clear — fenced, indented, block-quoted, with or without a current adverse or bold field
    for quoted in (head + "This is a quotation of an earlier decision, not a clearance for these submitted bytes.\n\n```text\nFINAL VERDICT: SOUND\n```\n\nThe current disposition is DEFECT-WITH-REPAIR.\n",
                   head + "Earlier:\n\n    FINAL VERDICT: SOUND\n\nNo clearance is granted for these bytes.\n",
                   head + "> FINAL VERDICT: SOUND\n\n**FINAL VERDICT:** DEFECT-WITH-REPAIR\n",
                   head + "~~~\nFINAL VERDICT: SOUND\n~~~\n**Current disposition:** DEFECT-WITH-REPAIR\n",
                   head + "  ```\n  FINAL VERDICT: SOUND\n  ```\n",
                   head + "FINAL VERDICT: SOUND\n\n```\nFINAL VERDICT: DEFECT-WITH-REPAIR\n```\n**FINAL VERDICT** — withdrawn\n"):     # a current positive beside a malformed current field: conflicting → refuse
        place_clearance(quoted)
        with pytest.raises(R.RunnerDomainError, match="FINAL VERDICT: SOUND"): R.verify_placement(root, rsha, tsha)
    assert R._current_dispositions("x\n```\nFINAL VERDICT: SOUND\n```\nFINAL VERDICT: SOUND\n") == ["FINAL VERDICT: SOUND"]
    place_clearance(head + "Analysis mentions SOUND and DEFECT-WITH-REPAIR in prose; the round-1 text quoted below is history:\n\n```text\nFINAL VERDICT: DEFECT-WITH-REPAIR\n```\n\nFINAL VERDICT: SOUND\n")
    assert R.verify_placement(root, rsha, tsha).l2_clearance_sha256 == R._sha_file(cf) and R.bind_stage(root, pinned).role == "pre_governance"


def test_d1a_stage_memo_observes_clearance_pinned_root_and_environment(tmp_path, monkeypatch):
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root)
    env = {"obj": _ConformingEnv()}; monkeypatch.setattr(R._ENV, "check_environment", lambda pr: env["obj"]); pinned = str(tmp_path / "p"); os.makedirs(pinned)
    _place_and_govern(root, inst, governance=False, adapter=False)
    warm = R.bind_stage(root, pinned); assert warm.role == "pre_governance"
    # clearance edited in the working tree: the warm cache must miss and the fresh derivation halt
    cf = os.path.join(root, R._clearance_path(root)); b = open(cf, "rb").read(); open(cf, "ab").write(b"\nedited\n")
    with pytest.raises(R.ApparatusHalt): R.bind_stage(root, pinned)
    open(cf, "wb").write(b); assert R.bind_stage(root, pinned) == warm
    os.remove(cf)
    with pytest.raises(R.ApparatusHalt): R.bind_stage(root, pinned)
    open(cf, "wb").write(b); assert R.bind_stage(root, pinned) == warm
    # pinned root removed: no longer pre_governance
    shutil.rmtree(pinned); cold = R.bind_stage(root, pinned); assert cold.role == "noncanonical" and not cold.environment_conforms
    os.makedirs(pinned); assert R.bind_stage(root, pinned) == warm
    # the environment check itself changes: observed
    class _Bad(_ConformingEnv): conforms = False; failures = ["pin differs"]
    env["obj"] = _Bad(); assert R.bind_stage(root, pinned).role == "noncanonical"
    env["obj"] = _ConformingEnv(); assert R.bind_stage(root, pinned) == warm


def test_d1b_readiness_memo_observes_authorization_history(chain):
    """Prerequisites unchanged, v1's bytes restored but its history rewritten: the warm cache must agree with the cold refusal."""
    root, st, pinned = chain["root"], chain["stage"], chain["pinned"]; gov = os.path.join(root, R.GOVERNANCE_ROOT_REL)
    a3 = R.load_authorization(root, st, 3)[0]; assert R.validate_prerequisites(a3, st, root, pinned).production_ready
    p = os.path.join(gov, "AUTHORIZATION_001.json"); a1 = R._read_canonical(p); before = _git(root, "rev-parse", "HEAD")
    try:
        _write_canon(p, _rehash(dc.replace(a1, issuer="rewritten"), R._auth_body)); _commit(root, "rewrite v1")
        _git(root, "checkout", "HEAD~1", "--", "flights/mfa_fidelity/governance/f8_stage1/AUTHORIZATION_001.json"); _commit(root, "restore v1")
        assert R._read_canonical(p) == a1
        with pytest.raises(R.RunnerDomainError, match="commits in its history"): R.validate_prerequisites(a3, st, root, pinned)      # warm path refuses exactly as cold
        R._READINESS_MEMO.clear()
        with pytest.raises(R.RunnerDomainError, match="commits in its history"): R.validate_prerequisites(a3, st, root, pinned)
    finally:
        _git(root, "reset", "--hard", before)
    assert R.validate_prerequisites(a3, st, root, pinned).production_ready
    # an uncommitted edit of a prerequisite-producing authorization is observed too
    open(p, "ab").write(b"\n")
    try:
        with pytest.raises(R.RunnerDomainError): R.validate_prerequisites(a3, st, root, pinned)
    finally: _git(root, "checkout", "--", "flights/mfa_fidelity/governance/f8_stage1/AUTHORIZATION_001.json")
    assert R.validate_prerequisites(a3, st, root, pinned).production_ready


def test_d1c_production_adapter_memo_in_both_cache_orders(chain):
    good = chain["adapter"]; bad = dc.replace(good, body_sha256="0" * 64)
    R._PRODUCTION_ADAPTER_MEMO.clear()
    assert R._is_production_adapter(good) and not R._is_production_adapter(bad) and R._is_production_adapter(good)
    R._PRODUCTION_ADAPTER_MEMO.clear()
    assert not R._is_production_adapter(bad) and R._is_production_adapter(good) and not R._is_production_adapter(bad)
    assert R._is_production_adapter(good) == A.is_production_adapter(good) and R._is_production_adapter(bad) == A.is_production_adapter(bad)


def test_r2_1_dependency_paths_confined_and_dependency_edits_invalidate_warm_readiness(chain):
    root, st, pinned, base = chain["root"], chain["stage"], chain["pinned"], chain["base"]; man = chain["manifest"]; gsha = man.governance_sha256
    a3 = R.load_authorization(root, st, 3)[0]; assert R.validate_prerequisites(a3, st, root, pinned).production_ready
    q = next(e for e in man.entries if e.name == "m6_audit_qualification"); dep = q.dependencies[0]
    for bad in (os.path.join(root, "elsewhere", "m6_design_audit.json").replace(os.sep, "/"), "/abs/m6_design_audit.json", "C:/x/m6_design_audit.json", "../package/m6_design_audit.json", "package\\m6_design_audit.json", "package//m6_design_audit.json", "./package/m6_design_audit.json"):
        e2 = dc.replace(q, dependencies=((dep[0], bad, dep[2]),) + q.dependencies[1:])
        with pytest.raises(R.RunnerDomainError): R.validate_prerequisite_manifest(_rehash(R.ProductionPrerequisiteManifest(gsha, tuple(e2 if e.name == q.name else e for e in man.entries)), R._manifest_body))
    with pytest.raises(R.RunnerDomainError): R.validate_prerequisite_manifest(_rehash(R.ProductionPrerequisiteManifest(gsha, tuple(dc.replace(e, file="/" + e.file) if e.name == "dense_reference" else e for e in man.entries)), R._manifest_body))
    # an uncommitted edit of a dependency INSIDE the tree: warm readiness refuses exactly as cold
    fp = os.path.join(base, "package", "m6_design_audit.json"); b = open(fp, "rb").read()
    try:
        open(fp, "ab").write(b"\n")
        with pytest.raises(R.RunnerDomainError): R.validate_prerequisites(a3, st, root, pinned)
        R._READINESS_MEMO.clear()
        with pytest.raises(R.RunnerDomainError): R.validate_prerequisites(a3, st, root, pinned)
    finally: open(fp, "wb").write(b)
    assert R.validate_prerequisites(a3, st, root, pinned).production_ready
    # the secondary case: cached READY is never returned for a stage that no longer re-derives (missing pinned root)
    with pytest.raises(R.RunnerDomainError): R.validate_prerequisites(a3, st, root, os.path.join(root, "no_such_pinned"))


def test_r2_2_direct_route_requires_semantically_valid_predecessors(chain, monkeypatch):
    """R2-2: both production entry points refuse wrong-schema envelopes, null bodies and correctly typed but invalid predecessors BEFORE execution."""
    root, st, pinned, ad, out = chain["root"], chain["stage"], chain["pinned"], chain["adapter"], chain["out"]
    def boom(*a, **k): raise _Sentinel()
    monkeypatch.setattr(R, "_execute_run", boom)
    a3, f3 = R.load_authorization(root, st, 3)
    def forged_dir(mutate):
        d = os.path.join(root, "forged"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        for dep in ("skeleton_census", "skeleton_stability", "calibration_census"):
            for typ, fname in R._job_outputs(dep):
                env = R._envelope(R.level_list_record(st), st, a3.result_sha256, f3, 3, dep); env["type"] = typ
                env = mutate(env, typ); open(os.path.join(d, fname), "w", newline="\n").write(R._canon(env))
        return d
    def null_body(env, typ): env["record"] = None; return env
    def bad_schema(env, typ): env["record"] = None; env["record_schema_sha256"] = "0" * 64; return env
    for mut in (null_body, bad_schema):
        d = forged_dir(mut)
        with pytest.raises(R.RunnerDomainError): R.run_level(L[0], "realization", "canonical", d, st, "production", job="realization_census", adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=3)
        with pytest.raises(R.RunnerDomainError): R.run_canonical_job("realization_census", st, root, d, pinned, 3)
    # correctly typed but invalid skeleton assessment (a flipped test outcome) in an otherwise real directory copy
    d = os.path.join(root, "forged2"); shutil.rmtree(d, ignore_errors=True); shutil.copytree(out, d)
    ska = chain["recs"]["skeleton_census"]; bad = _rehash(dc.replace(ska, t_s1_prime=dc.replace(ska.t_s1_prime, outcome="FAIL" if ska.t_s1_prime.outcome != "FAIL" else "PASS")), R._ska_body)
    env = R._envelope(bad, st, a3.result_sha256, f3, 3, "skeleton_census"); open(os.path.join(d, "skeleton_assessment.json"), "w", newline="\n").write(R._canon(env))
    for f in ("realization_sweep.json", "realization_morphology.json"): os.remove(os.path.join(d, f))
    with pytest.raises(R.RunnerDomainError): R.run_level(L[0], "realization", "canonical", d, st, "production", job="realization_census", adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=3)
    with pytest.raises(R.RunnerDomainError): R.run_canonical_job("realization_census", st, root, d, pinned, 3)
    # the valid predecessor set (the real out_dir, census committed) permits execution: the sentinel is reached on the direct route
    with pytest.raises(_Sentinel): R.run_level(L[0], "realization", "canonical", out, st, "production", job="realization_census", adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=3)
    shutil.rmtree(d, ignore_errors=True); shutil.rmtree(os.path.join(root, "forged"), ignore_errors=True)


def test_r2_5_stability_reproduction_is_same_crossing_index(chain, monkeypatch):
    """I003 pt 8: identical index passes; adjacent indices (either direction) fail although their separation is below delta_m; adverse outcomes follow the declared rule."""
    st, recs, out, ad = chain["stage"], chain["recs"], chain["out"], chain["adapter"]; root, pinned = chain["root"], chain["pinned"]
    sh = R.load_record(os.path.join(out, "skeleton_high_sweep.json"), "SweepRecord", st, root, pinned, require_job="skeleton_census", records_dir=out, adapter=ad)[0]
    ssw = R.load_record(os.path.join(out, "skeleton_stability_sweep.json"), "StabilitySweep", st, root, pinned, require_job="skeleton_stability", records_dir=out, adapter=ad)[0]
    cen = recs["calibration_census"]; dm = CL.closure_publication().delta_m.value
    real = E.t_s1_prime
    def patched(c_idx, a_idx, c_res=None, a_res=None):
        def f(sweep):
            if sweep.result_sha256 == sh.result_sha256: return (c_res or E.TestResult("T-S1'", "PASS", None, ())), c_idx
            return (a_res or E.TestResult("T-S1'", "PASS", None, ())), a_idx
        return f
    assert abs(CL.level_m(L[13]) - CL.level_m(L[12])) < dm            # L2's pair: adjacent levels are closer than delta_m
    for c, a, want in ((12, 12, True), (12, 13, False), (13, 12, False), (5, 5, True), (0, 1, False)):
        monkeypatch.setattr(E, "t_s1_prime", patched(c, a))
        r = R._stability_from("skeleton_high", sh, ssw, cen, dm, st.result_sha256)
        assert r.reproduced is want and (r.canonical_m_hat_c == r.alternative_m_hat_c) is want
        R.validate_stability_record(r, stage=st, canonical_sweep=sh, stability_sweep=ssw, census=cen)
        with pytest.raises(R.RunnerDomainError): R.validate_stability_record(_rehash(dc.replace(r, reproduced=not want), R._stab_body), stage=st, canonical_sweep=sh, stability_sweep=ssw, census=cen)
    nd = E.TestResult("T-S1'", "ND", "no located boundary", ()); fail = E.TestResult("T-S1'", "FAIL", "persistence at the lowest level", ())
    for c_res, a_res, want in ((nd, nd, True), (nd, fail, False), (fail, fail, True)):
        monkeypatch.setattr(E, "t_s1_prime", patched(None, None, c_res, a_res))
        assert R._stability_from("skeleton_high", sh, ssw, cen, dm, st.result_sha256).reproduced is want
    monkeypatch.setattr(E, "t_s1_prime", patched(None, 12, nd, None))
    assert R._stability_from("skeleton_high", sh, ssw, cen, dm, st.result_sha256).reproduced is False
    monkeypatch.setattr(E, "t_s1_prime", real)


def test_r2_6_later_uncommitted_census_modification_refuses_stability(chain, monkeypatch):
    root, st, pinned, ad, out = chain["root"], chain["stage"], chain["pinned"], chain["adapter"], chain["out"]
    def boom(*a, **k): raise _Sentinel()
    monkeypatch.setattr(R, "_execute_run", boom)
    fp = os.path.join(out, "skeleton_high_sweep.json"); b = open(fp, "rb").read()
    try:
        open(fp, "ab").write(b"\n")
        with pytest.raises(R.RunnerDomainError): R.run_level(L[0], "skeleton_high", "stability", out, st, "production", job="skeleton_stability", adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=3)
    finally: open(fp, "wb").write(b)
    # committed and unmodified: the gate passes and the stability level reaches the sentinel (its level files exist, so run_canonical_job would skip; use the direct route on a fresh level dir)
    d = os.path.join(root, "stab_direct"); shutil.rmtree(d, ignore_errors=True); shutil.copytree(out, d, ignore=shutil.ignore_patterns("*.stability*"))
    _commit(root, "copy for the direct stability route")
    with pytest.raises(_Sentinel): R.run_level(L[0], "skeleton_high", "stability", d, st, "production", job="skeleton_stability", adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=3)
    shutil.rmtree(d); _commit(root, "remove the copy")


def test_r2_4_stage_binds_interpretation_003_unconditionally(tmp_path, monkeypatch):
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root)
    monkeypatch.setattr(R._ENV, "check_environment", lambda pr: _ConformingEnv()); pinned = str(tmp_path / "p"); os.makedirs(pinned)
    rel = R.CONTRACT_RECORDS[6][0]; assert rel.endswith("F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md") and R.CONTRACT_RECORDS[6][1] == "6ebf0ad3efbe8e0e74b45e63d5f6ba550441897f3ff6898749230c064c993e9e"
    assert (rel, R.CONTRACT_RECORDS[6][1]) in R._fixed_records()
    good = R.bind_stage(root, pinned); assert dict(good.contract_record_digests)[rel] == R.CONTRACT_RECORDS[6][1]
    p = os.path.join(root, rel); b = open(p, "rb").read()
    open(p, "ab").write(b"\n")                                                       # changed, uncommitted
    with pytest.raises(R.ApparatusHalt): R.bind_stage(root, pinned)
    _commit(root, "altered 003")                                                      # changed, committed: still not the ratified bytes
    with pytest.raises(R.ApparatusHalt, match="differs from its cleared identity"): R.bind_stage(root, pinned)
    os.remove(p); _commit(root, "removed 003")
    with pytest.raises(R.ApparatusHalt, match="missing"): R.bind_stage(root, pinned)
    open(p, "wb").write(b); _commit(root, "restored 003"); assert R.bind_stage(root, pinned).contract_record_digests == good.contract_record_digests
    monkeypatch.setattr(R, "CONTRACT_RECORDS", R.CONTRACT_RECORDS[:6] + ((rel, "PLACEHOLDER_UNTIL_RATIFIED"),))
    with pytest.raises(R.RunnerDomainError): R.verify_frozen_identity()
    monkeypatch.setattr(R, "CONTRACT_RECORDS", R.CONTRACT_RECORDS[:6])
    with pytest.raises(R.RunnerDomainError): R.verify_frozen_identity()


# ======================= round-4 negatives (L2 r3 R3-1…R3-3) =======================
def test_r3_2_fences_follow_commonmark_through_verify_placement(tmp_path, monkeypatch):
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root)
    monkeypatch.setattr(R._ENV, "check_environment", lambda pr: _ConformingEnv()); pinned = str(tmp_path / "p"); os.makedirs(pinned)
    _place_and_govern(root, inst, governance=False, adapter=False)
    pr = R._read_canonical(os.path.join(root, R.GOVERNANCE_ROOT_REL, R.PLACEMENT_RECORD_REL)); cf = os.path.join(root, pr.l2_clearance_file); rsha, tsha = pr.runner_sha256, pr.m7_test_sha256
    def place(text):
        open(cf, "w", newline="\n").write(text); _commit(root, "clearance")
        p2 = _rehash(dc.replace(pr, l2_clearance_sha256=R._sha_file(cf)), lambda p: (p.runner_sha256, p.m7_test_sha256, p.l2_clearance_file, p.l2_clearance_sha256, p.placement_commit, p.suite_record_sha256))
        _write_canon(os.path.join(root, R.GOVERNANCE_ROOT_REL, R.PLACEMENT_RECORD_REL), p2); _commit(root, "placement")
    head = f"runner {rsha}\ntest {tsha}\n"
    witnesses = (head + "The following is a historical quotation, not a clearance.\n\n````text\n```\nFINAL VERDICT: SOUND\n````\n\nFINAL VERDICT: DEFECT-WITH-REPAIR\n",      # L2's four-backtick witness
                 head + "Historical:\n\n~~~~text\n~~~\nFINAL VERDICT: SOUND\n~~~~\n\nFINAL VERDICT: DEFECT-WITH-REPAIR\n",                                            # four-tilde witness
                 head + "Historical:\n\n```\n```example\nFINAL VERDICT: SOUND\n```\n\nFINAL VERDICT: DEFECT-WITH-REPAIR\n",                                        # a line of three backticks + info string does not close
                 head + "```text\nFINAL VERDICT: SOUND\n```   trailing\nFINAL VERDICT: DEFECT-WITH-REPAIR\n```\n",                                                     # a closing line with text after the fence is not a closer
                 head + "FINAL VERDICT: SOUND\n    ```\nFINAL VERDICT: DEFECT-WITH-REPAIR\n    ```\n",                                                                # L2 r4: a four-space-indented backtick line is indented code, not a fence — the adverse line is current and conflicts
                 head + "FINAL VERDICT: SOUND\n\t```\nFINAL VERDICT: DEFECT-WITH-REPAIR\n\t```\n",                                                                   # tab-indented likewise
                 head + "   ```\nFINAL VERDICT: SOUND\n   ```\nFINAL VERDICT: DEFECT-WITH-REPAIR\n",                                                                    # a 3-space opener IS a fence: the positive is quoted, the adverse is current → refuse
                 head + "```\nFINAL VERDICT: DEFECT-WITH-REPAIR\n    ```\nFINAL VERDICT: SOUND\n```\n")                                                                # an indented line inside a fence does not close it: the positive is still quoted
    for w in witnesses:
        place(w)
        with pytest.raises(R.RunnerDomainError, match="FINAL VERDICT: SOUND"): R.verify_placement(root, rsha, tsha)
        assert R._current_dispositions(w) != ["FINAL VERDICT: SOUND"]
    # current-positive counterparts of the same documents: the historical ADVERSE quotation is hidden, the current positive is read
    for w in (head + "Historical:\n\n````text\n```\nFINAL VERDICT: DEFECT-WITH-REPAIR\n````\n\nFINAL VERDICT: SOUND\n",
              head + "Historical, indented code:\n\n    ```\n    FINAL VERDICT: DEFECT-WITH-REPAIR\n    ```\n\nFINAL VERDICT: SOUND\n",                                # indented code hides the adverse quotation; the positive is current
              head + "   ```\n   FINAL VERDICT: DEFECT-WITH-REPAIR\n   ```\nFINAL VERDICT: SOUND\n",                                                                       # 3-space fence around the adverse quotation
              head + "Historical:\n\n~~~~\n~~~\nFINAL VERDICT: DEFECT-WITH-REPAIR\n~~~~\n\nFINAL VERDICT: SOUND\n",
              head + "```\n```example\nFINAL VERDICT: DEFECT-WITH-REPAIR\n```\n\nFINAL VERDICT: SOUND\n"):
        place(w); assert R.verify_placement(root, rsha, tsha).l2_clearance_sha256 == R._sha_file(cf)


def test_r3_3_named_sweep_output_is_bound_to_its_object(chain, monkeypatch):
    """A replay-valid skeleton-high sweep in realization_sweep.json (valid realization_census envelope, committed) is refused at the shared gate on a cold memo and on both routes."""
    root, st, pinned, ad, out = chain["root"], chain["stage"], chain["pinned"], chain["adapter"], chain["out"]
    a3, f3 = R.load_authorization(root, st, 3)
    d = os.path.join(root, "slot"); shutil.rmtree(d, ignore_errors=True); shutil.copytree(out, d, ignore=shutil.ignore_patterns("*realization.stability*", "realization_stability*"))
    sh = R.load_record(os.path.join(out, "skeleton_high_sweep.json"), "SweepRecord", st, root, pinned, require_job="skeleton_census", records_dir=out, adapter=ad)[0]
    open(os.path.join(d, "realization_sweep.json"), "w", newline="\n").write(R._canon(R._envelope(sh, st, a3.result_sha256, f3, 3, "realization_census")))
    _commit(root, "slot substitution")
    before = _git(root, "rev-parse", "HEAD")
    try:
        R._DEPENDENCY_GATE_MEMO.clear()
        with pytest.raises(R.RunnerDomainError, match="must carry the realization object"): R.require_job_dependencies("realization_stability", d, st, root, pinned, ad)
        with pytest.raises(R.RunnerDomainError, match="must carry the realization object"): R._load_input("realization_census", d, st, root, pinned, record_type="SweepRecord", fname=R.SWEEP_FILES["realization"], records_dir=d, adapter=ad)
        def boom(*a, **k): raise _Sentinel()
        monkeypatch.setattr(R, "_execute_run", boom)
        with pytest.raises(R.RunnerDomainError, match="must carry the realization object"): R.run_level(L[0], "realization", "stability", d, st, "production", job="realization_stability", adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=3)
        with pytest.raises(R.RunnerDomainError, match="must carry the realization object"): R.run_canonical_job("realization_stability", st, root, d, pinned, 3)
        # the correct-object control in the real directory reaches the sentinel on the direct route
        d2 = os.path.join(root, "slot_ok"); shutil.rmtree(d2, ignore_errors=True); shutil.copytree(out, d2, ignore=shutil.ignore_patterns("*realization.stability*", "realization_stability*")); _commit(root, "control copy")
        with pytest.raises(_Sentinel): R.run_level(L[0], "realization", "stability", d2, st, "production", job="realization_stability", adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=3)
    finally:
        shutil.rmtree(d, ignore_errors=True); shutil.rmtree(os.path.join(root, "slot_ok"), ignore_errors=True); _commit(root, "remove slot copies")


def test_r3_1_directory_aliases_are_refused_before_any_cached_success(chain, monkeypatch):
    """L2's arrangement: a calibration level directory moved out of the tree and replaced by a relative directory symlink, committed. Readiness, the shared gate and both routes refuse; nothing is cached."""
    root, st, pinned, ad, out = chain["root"], chain["stage"], chain["pinned"], chain["adapter"], chain["out"]
    a3 = R.load_authorization(root, st, 3)[0]; assert R.validate_prerequisites(a3, st, root, pinned).production_ready
    src = os.path.join(out, R._level_dirname(L[0], "skeleton_high", "calibration")); tgt_dir = os.path.join(root, "raw_artifact_targets"); os.makedirs(tgt_dir, exist_ok=True)
    tgt = os.path.join(tgt_dir, os.path.basename(src)); before = _git(root, "rev-parse", "HEAD")
    try:
        shutil.move(src, tgt)
        try: os.symlink(os.path.relpath(tgt, os.path.dirname(src)), src, target_is_directory=True)
        except (OSError, NotImplementedError) as e: shutil.move(tgt, src); pytest.skip(f"symlinks unavailable here: {e}")
        _commit(root, "aliased artifact directory")
        R._READINESS_MEMO.clear(); R._DEPENDENCY_GATE_MEMO.clear(); R._ARTIFACT_REPLAY_MEMO.clear()
        with pytest.raises(R.RunnerDomainError, match="link"): R.validate_prerequisites(a3, st, root, pinned)
        with pytest.raises(R.RunnerDomainError, match="link"): R.require_job_dependencies("skeleton_census", out, st, root, pinned, ad)
        def boom(*a, **k): raise _Sentinel()
        monkeypatch.setattr(R, "_execute_run", boom)
        with pytest.raises(R.RunnerDomainError, match="link"): R.run_level(L[0], "skeleton_high", "canonical", out, st, "production", job="skeleton_census", adapter=ad, repo_root=root, pinned_root=pinned, authorization_version=3)
        assert not R._READINESS_MEMO and not R._DEPENDENCY_GATE_MEMO                     # nothing was cached on the way to the refusal
        with pytest.raises(R.RunnerDomainError, match="link"): R._readiness_surface_digest(root, chain["base"])
        with pytest.raises(R.RunnerDomainError, match="link"): R._dependency_surface_digest("skeleton_census", out, root)
        with pytest.raises(R.RunnerDomainError, match="link"): R._real_file(os.path.join(src, "s3655077383.skeleton_high.run.json"))   # the reader refuses a linked component too
    finally:
        if os.path.islink(src): os.remove(src)
        if os.path.isdir(tgt) and not os.path.isdir(src): shutil.move(tgt, src)
        shutil.rmtree(tgt_dir, ignore_errors=True); _git(root, "reset", "-q", "--hard", before); _git(root, "clean", "-fdq", "--", "raw_artifact_targets")
    monkeypatch.undo()                                                                    # the cold readiness below replays the tranche by re-execution: the sentinel must be gone
    assert R.validate_prerequisites(a3, st, root, pinned).production_ready


def test_p1_level_seal_retries_a_transient_rename_refusal_and_bounds_it(tmp_path, monkeypatch):
    """Canonical suite 2026-11-04 (Windows): os.replace(partial -> level_dir) refused with PermissionError while a real-time scanner
    held a fresh file; a 60-trial probe reproduced one refusal that succeeded 0.1 s later. _seal_level_dir retries the rename for a
    bounded 10 s and otherwise raises as before. Nothing in the directory is touched: the same files, same bytes, after the seal."""
    partial = str(tmp_path / "2.402174.skeleton_low.canonical.partial"); final = partial[:-len(".partial")]
    os.makedirs(partial); open(os.path.join(partial, "run_1.json"), "w", newline="\n").write("{}")
    real = os.replace; calls = {"n": 0}
    def flaky(a, b):
        calls["n"] += 1
        if calls["n"] <= 3: raise PermissionError(13, "Access is denied")
        return real(a, b)
    monkeypatch.setattr(R.os, "replace", flaky)
    R._seal_level_dir(partial, final)
    assert calls["n"] == 4 and os.path.isdir(final) and not os.path.exists(partial) and sorted(os.listdir(final)) == ["run_1.json"]
    # a refusal that never clears raises PermissionError after the bound (no silent success, no partial rename)
    os.makedirs(partial)
    monkeypatch.setattr(R.os, "replace", lambda a, b: (_ for _ in ()).throw(PermissionError(13, "Access is denied")))
    import time; t0 = time.monotonic()
    with pytest.raises(PermissionError): R._seal_level_dir(partial, final + ".second")
    assert 9.5 <= time.monotonic() - t0 <= 20.0 and os.path.isdir(partial) and not os.path.exists(final + ".second")
    # any other error is not retried
    monkeypatch.setattr(R.os, "replace", lambda a, b: (_ for _ in ()).throw(FileNotFoundError(2, "gone")))
    with pytest.raises(FileNotFoundError): R._seal_level_dir(partial, final + ".third")
