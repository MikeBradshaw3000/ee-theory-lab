"""tests/test_e1_m7.py — E1 stage-1 module M7, round 4. Temporary committed repositories (independent of the real repository's commit state).
Covers L2 r3 §16 items 19–22: the five mechanical counterexamples (arbitrary placement facts; partial prerequisite set; caller-selected pass
number; unknown item name; forged authorized quarantine with negative cost); ONE successful complete production-prerequisite chain; ONE
successful canonical package assembly → persistence → reload → prerequisite replay using only committed files; and the fourteen families
against the repaired paths. The governance record used here holds TEST STAND-IN values; M7 itself contains none."""
import dataclasses as dc
import json
import os
import shutil
import subprocess
import numpy as np
import pytest

from mfa_instrument.e1 import runner as R, projection as P, config as C, audit as A, classify as K, verdict as V

INST = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(INST, "..", "..", ".."))
SMALL = dict(grid=10, ticks=60)
SMOKE = dict(grid=8, ticks=60)    # below-production helpers: ALWAYS distinct from the chain fixture's stand-in production shape (SMALL), so no test outcome depends on test order
L = C.E1_LEVELS_MICRO
DENSE3 = (L[0], L[12], L[23])
AMEND = "# E1-R AMENDMENT (test stand-in)\namendment_version: 0\nclaim_tier: realization-level\nflight_name: E1-R\nverdict_grammar: test\npackage_grammar: test\n"


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
    for rel in [r for r, _ in R.GATE_RECORDS] + [r for r, _ in R.CACHE_FILES]:
        dst = os.path.join(root, rel); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(os.path.join(REPO, rel), dst)
    return inst


# ---- test stand-in governance values (NOT M7's; the real record is Mike's)
ITEMS = (R.PackageItem("dense_reference", "ReferenceStructure", "dense_reference", "reference_of_record_dense", "reference_resolved", ()),
         R.PackageItem("reference_stability", "StabilityAudit", "reference_stability", "stability_canonical_complete", "stability_within", (("primary", "dense_reference"),)),
         R.PackageItem("m6_design_audit", "AuditRecord", "m6_design_audit", "audit_record_complete", "audit_record_pass", ()),
         R.PackageItem("m6_held_out_audit", "AuditRecord", "m6_held_out_audit", "audit_record_complete", "audit_record_pass", ()),
         R.PackageItem("m6_audit_qualification", "AuditQualification", "m6_audit_qualification", "qualification_recorded", "qualification_qualified", (("design", "m6_design_audit"), ("held_out", "m6_held_out_audit"))),
         R.PackageItem("resource_actuals", "ResourceBenchmark", "resource_benchmark", "benchmark_canonical", "benchmark_fits", ()),
         R.PackageItem("level_list_and_spacings", "LevelListRecord", "derived", "exists", "exists", ()))
VOCAB = tuple(i.name for i in ITEMS) + ("design_stability", "projection_sweep_ensemble")
PREREQS = (("stage1_package", "scientific", "valid_complete"), ("calibration_tranche", "apparatus", "pass"), ("resource_actuals", "apparatus", "pass"), ("m6_audit_qualification", "qualification", "pass"))
JOBS = ("dense_reference", "reference_stability", "tolerance_ensembles", "tolerance_program", "m6_design_audit", "m6_held_out_audit", "m6_audit_qualification", "resource_benchmark", "stage1_package")


def _gov_rec(amend_sha, prereqs=PREREQS, branch=(), required=None):
    g = R.E1RGovernance(1, amend_sha, "realization-level (test)", "E1-R (test)", VOCAB, tuple(i.name for i in ITEMS) if required is None else required, prereqs, branch)
    return _rehash(g, R._gov_body)


def _spec_rec(gov_sha, items=ITEMS): return _rehash(R.PackageSpecification(1, gov_sha, items), R._spec_body)


def _auth(stage, version, prod_manifest=""):
    a = R.AuthorizationRecord(version, "2026-10-03", "test-stand-in", stage.result_sha256, stage.amendment_sha256, stage.governance_sha256, stage.package_spec_sha256,
                              JOBS, True, tuple(L[:5]), tuple(C.E1_SEED_PANEL[:3]), bool(prod_manifest), prod_manifest)
    return _rehash(a, R._auth_body)


def _publish_auth(root, auth):
    gov = os.path.join(root, R.GOVERNANCE_ROOT_REL); p = os.path.join(gov, f"AUTHORIZATION_{auth.version:03d}.json"); _write_canon(p, auth)
    rp = os.path.join(gov, R.AUTHORIZATION_REGISTRY_REL); entries = R._read_canonical(rp).entries if os.path.isfile(rp) else ()
    _write_canon(rp, _rehash(R.AuthorizationRegistry(entries + ((auth.version, R._sha_file(p)),)), lambda r: r.entries)); _commit(root, f"authorization v{auth.version}")


def _place_and_govern(root, inst, *, governance=True, spec=True):
    """Placement (mechanically verifiable), suite record, clearance file, amendment, governance, specification — committed."""
    c1 = _git(root, "log", "-1", "--format=%H")
    rsha = R._sha_file(os.path.join(inst, R.RUNNER_REL)); tsha = R._sha_file(os.path.join(inst, R.M7_TEST_REL)); gov = os.path.join(root, R.GOVERNANCE_ROOT_REL)
    clear_rel = "flights/mfa_fidelity/build_records/L2_E1_M7_TEST_CLEARANCE.md"
    os.makedirs(os.path.dirname(os.path.join(root, clear_rel)), exist_ok=True)
    open(os.path.join(root, clear_rel), "w", newline="\n").write(f"# test clearance\nrunner {rsha}\ntest {tsha}\nFINAL VERDICT: SOUND\n")
    sr = _rehash(R.M7SuiteRecord("python -m pytest tests -q -p no:cacheprovider", 600, 2, 0, rsha, tsha, c1), lambda s: (s.invocation, s.passed, s.skipped, s.failed, s.runner_sha256, s.m7_test_sha256, s.tested_commit))
    _write_canon(os.path.join(gov, R.SUITE_RECORD_REL), sr)
    pr = R.M7PlacementRecord(rsha, tsha, clear_rel, R._sha_file(os.path.join(root, clear_rel)), c1, R._sha_file(os.path.join(gov, R.SUITE_RECORD_REL)))
    _write_canon(os.path.join(gov, R.PLACEMENT_RECORD_REL), _rehash(pr, lambda p: (p.runner_sha256, p.m7_test_sha256, p.l2_clearance_file, p.l2_clearance_sha256, p.placement_commit, p.suite_record_sha256)))
    open(os.path.join(gov, R.AMENDMENT_REL), "w", newline="\n").write(AMEND); amend = R._sha_file(os.path.join(gov, R.AMENDMENT_REL))
    g = None
    if governance:
        g = _gov_rec(amend); _write_canon(os.path.join(gov, R.GOVERNANCE_REL), g)
        if spec: _write_canon(os.path.join(gov, R.PACKAGE_SPEC_REL), _spec_rec(R._sha_file(os.path.join(gov, R.GOVERNANCE_REL))))
    _commit(root, "placed + governed")
    return g


@pytest.fixture(scope="module")
def repo(tmp_path_factory):
    root = str(tmp_path_factory.mktemp("repo")); _base_repo(root); _git(root, "init", "-q"); _commit(root, "placed"); return root


@pytest.fixture(scope="module")
def stage(repo): return R.bind_stage(repo)


def _fake_audit(sc):
    def fake(ens, cache):
        f = (A.AUDIT_VERSION, ens, A.AUDIT_MASTER if ens == "design" else A.HELD_OUT_MASTER, 500, "production_frozen", A.PRODUCTION_CACHE_BODY_SHA256_LITERAL, A.PRODUCTION_CACHE_FILE_SHA256_LITERAL,
             A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL, A.AUDIT_DECLARATION_SHA256_LITERAL, A.GENERATOR_DECLARATION_SHA256_LITERAL, sc, True)
        return A.AuditRecord(*f, A._digest(A.AuditRecord(*f, "").identity_body()))
    return fake


@pytest.fixture(scope="module")
def chain(tmp_path_factory):
    """THE successful end-to-end chain at reduced shape (3-level dense grid; 10x60 runs; M6 audits stubbed): canonical stage → authorized jobs →
    atomic canonical package → authorized tranche → committed prerequisite manifest → production authorization → production READY."""
    mp = pytest.MonkeyPatch()
    try:                                                                  # guaranteed cleanup: a failed setup must never leak stubs into later modules
        mp.setattr(R._ENV, "check_environment", lambda root: _ConformingEnv())
        mp.setattr(P, "dense_grid_micro", lambda: DENSE3); mp.setattr(P, "DENSE_POINTS", 3); mp.setattr(P, "verify_frozen_identity", lambda: None)
        mp.setattr(R, "E1_GRID", SMALL["grid"]); mp.setattr(R, "E1_TICKS", SMALL["ticks"])
        sc = tuple(A.ClassScore(n, *A.INTENDED[n], 500, 500, 0, 0, "false_nd" if n in A.SCIENTIFIC_CLASSES else "false_scientific", 0, A.clopper_pearson_upper(0, 500), True, True, 1.0, 500, ((A.INTENDED[n][0], 500),), (), ()) for n in A.CLASSES)
        mp.setattr(A, "run_audit", _fake_audit(sc))
        root = str(tmp_path_factory.mktemp("chain")); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root, "placed")
        _place_and_govern(root, inst)
        stage = R.bind_stage(root, pinned_root=root); assert stage.role == "canonical", stage.environment_failures
        _publish_auth(root, _auth(stage, 1)); assert R.bind_stage(root, pinned_root=root).result_sha256 == stage.result_sha256
        pre = os.path.join(root, R.GOVERNANCE_ROOT_REL, R.PREREQUISITES_REL)
        for job in ("dense_reference", "reference_stability", "m6_design_audit", "m6_held_out_audit", "m6_audit_qualification", "resource_benchmark"):
            R.run_canonical_job(job, stage, root, pre, root, 1, cache=None)
        pkg, pkg_path = R.run_canonical_job("stage1_package", stage, root, pre, root, 1)
        q, q_path = R.run_tranche(pre, stage, root, root, 1)
        def entry(name, typ, fname, deps=()):
            fp = os.path.join(pre, fname); rec = R._read_canonical(fp) if False else R.load_record(fp, typ, stage, root, root, require_job=R.PREREQ_JOBS[name], **({"package_dir": pre} if typ == "StagePackage" else {}),
                                                                                             **({"artifact_dir": os.path.join(pre, "benchmark_artifacts")} if typ == "ResourceBenchmark" else {}),
                                                                                             **({k: R.load_record(os.path.join(pre, f), "AuditRecord", stage, root, root, require_job=j)[0] for k, f, j in deps}))[0]
            return R.PrerequisiteEntry(name, typ, fname, R._sha_file(fp), R._item_identity(rec), tuple((k, f, R._sha_file(os.path.join(pre, f))) for k, f, _ in deps))
        entries = (entry("stage1_package", "StagePackage", "stage1_package.json"), entry("calibration_tranche", "TrancheQuarantine", "calibration_tranche.json"),
                   entry("resource_actuals", "ResourceBenchmark", "resource_benchmark.json"),
                   entry("m6_audit_qualification", "AuditQualification", "m6_audit_qualification.json", (("design", "m6_design_audit.json", "m6_design_audit"), ("held_out", "m6_held_out_audit.json", "m6_held_out_audit"))))
        man = _rehash(R.ProductionPrerequisiteManifest(stage.governance_sha256, entries), R._manifest_body)
        mpath = os.path.join(root, R.GOVERNANCE_ROOT_REL, R.PREREQ_MANIFEST_REL); _write_canon(mpath, man); _commit(root, "prerequisites + manifest")
        _publish_auth(root, _auth(stage, 2, prod_manifest=R._sha_file(mpath)))
        assert R.bind_stage(root, pinned_root=root).result_sha256 == stage.result_sha256          # none of this moved the stage
    except BaseException:
        mp.undo()
        raise
    yield dict(root=root, stage=stage, pre=pre, pkg=pkg, pkg_path=pkg_path, q=q, man=man, mp=mp)
    mp.undo()


# ======================= identity =======================
def test_frozen_identity_and_no_scientific_values_in_source():
    R.verify_frozen_identity()
    src = open(R.__file__, encoding="utf-8").read()
    assert "required_package_items=(" not in src and "production_prerequisites=(" not in src and set(R.PREDICATES) == set(R.PREDICATE_IDS)
    assert not any(n in dir(R) for n in ("CANONICAL_JOBS_AUTHORIZED", "TRANCHE_AUTHORIZED", "PRODUCTION_AUTHORIZED", "JOB_FOR_ITEM"))
    import inspect
    for fn in (R.require_authorized, R.run_canonical_job, R.run_level, R.run_tranche, R.load_record):
        assert "auth" not in inspect.signature(fn).parameters and "pass_number" not in inspect.signature(fn).parameters


def test_pre_amendment_is_default_deny(repo, stage, tmp_path, monkeypatch):
    assert stage.role == "noncanonical" and stage.governance_sha256 is None and stage.package_spec_sha256 is None
    with pytest.raises(R.RunnerDomainError, match="canonical stage"): R.require_authorized(stage, repo, None, 1, "dense_reference")
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root, "placed")
    _place_and_govern(root, inst, governance=False)
    monkeypatch.setattr(R._ENV, "check_environment", lambda r: _ConformingEnv())
    s = R.bind_stage(root, pinned_root=root); assert s.role == "pre_amendment"                  # placed + qualified environment, no governance → never canonical
    with pytest.raises(R.RunnerDomainError, match="canonical stage"): R.require_authorized(s, root, root, 1, "dense_reference")


# ======================= L2 r3 counterexample 1: placement facts =======================
def test_arbitrary_placement_facts_refused(tmp_path, monkeypatch):
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root, "placed")
    _place_and_govern(root, inst)
    gov = os.path.join(root, R.GOVERNANCE_ROOT_REL); pr = R._read_canonical(os.path.join(gov, R.PLACEMENT_RECORD_REL))
    body = lambda p: (p.runner_sha256, p.m7_test_sha256, p.l2_clearance_file, p.l2_clearance_sha256, p.placement_commit, p.suite_record_sha256)
    for mut, why in ((dict(l2_clearance_sha256="a" * 64), "clearance"), (dict(placement_commit="b" * 40), "placement commit"), (dict(suite_record_sha256="c" * 64), "suite record")):
        _write_canon(os.path.join(gov, R.PLACEMENT_RECORD_REL), _rehash(dc.replace(pr, **mut), body)); _commit(root, why)
        with pytest.raises(R.ApparatusHalt, match="placement record does not verify"): R.bind_stage(root)
    cf = os.path.join(root, "flights/mfa_fidelity/build_records/L2_E1_M7_TEST_CLEARANCE.md"); open(cf, "w", newline="\n").write("no verdict here\n")
    _write_canon(os.path.join(gov, R.PLACEMENT_RECORD_REL), _rehash(dc.replace(pr, l2_clearance_sha256=R._sha_file(cf)), body)); _commit(root, "no-sound")
    with pytest.raises(R.ApparatusHalt, match="placement record does not verify"): R.bind_stage(root)


# ======================= L2 r3 counterexample 2: partial prerequisite set =======================
def test_partial_prerequisite_set_refused(chain, monkeypatch):
    root, stage = chain["root"], chain["stage"]; auth, _ = R.load_authorization(root, stage, 2)
    R.validate_prerequisites(auth, stage, root, root)
    g, gsha = R.load_governance(root, stage)
    monkeypatch.setattr(R, "load_governance", lambda r, s: (_rehash(dc.replace(g, production_prerequisites=g.production_prerequisites + (("dense_reference", "scientific", "valid_complete"),)), R._gov_body), gsha))
    with pytest.raises(R.RunnerDomainError, match="exact production set"): R.validate_prerequisites(auth, stage, root, root)


# ======================= L2 r3 counterexample 3: pass number =======================
def test_pass_number_derived_never_chosen(tmp_path, repo, stage):
    lr = R.run_level(L[12], str(tmp_path), stage, None, "rehearsal", **SMALL)
    assert lr.pass_number == 1 and lr.router_manifest_sha256 == ""
    with pytest.raises(R.RunnerDomainError, match="pass number does not derive"): R.validate_level_record(_rehash(dc.replace(lr, pass_number=2), R._level_body))
    with pytest.raises(R.RunnerDomainError, match="router manifest"): R.validate_level_record(_rehash(dc.replace(lr, router_manifest_sha256="a" * 64), R._level_body))
    off = A.reachable_pass2_levels()[0]
    with pytest.raises(R.RunnerDomainError, match="pass-1 grid"): R.run_level(off, str(tmp_path), stage, None, "rehearsal", **SMALL)


def test_router_manifest_derives_and_reachability_drives_halt_class():
    labels = ("N",) * 10 + ("U",) * 2 + ("S",) * 12; d = V.route(labels, L); surf = set(A.reachable_pass2_levels())
    body = (tuple((m, "a" * 64) for m in L), labels, d.row, tuple(d.insertions_micro), tuple(d.fallback_moves), tuple(d.fallback_drops), tuple(m in surf for m in d.insertions_micro), "b" * 64)
    rm = R.RouterManifest(*body, R._digest(body))
    with pytest.raises(R.RunnerDomainError, match="validates only with"): R.validate_router_manifest(rm)   # L2 r4 family 4: self-consistent but unreplayed → refused
    assert all(rm.reachable) and len(rm.insertions_micro) > 0                                  # router outputs on the qualified surface: a cache miss there is APPARATUS
    with pytest.raises(R.RunnerDomainError, match="re-derive"): R.validate_router_manifest(_rehash(dc.replace(rm, insertions_micro=rm.insertions_micro[:-1]), R._router_body))
    with pytest.raises(R.RunnerDomainError, match="reachability"): R.validate_router_manifest(_rehash(dc.replace(rm, reachable=(False,) + rm.reachable[1:]), R._router_body))


# ======================= L2 r3 counterexample 4: unknown item name =======================
def test_unknown_item_name_and_spec_grammar_refused(chain):
    root, stage = chain["root"], chain["stage"]; g, gsha = R.load_governance(root, stage)
    arb = ITEMS + (R.PackageItem("arbitrary_item", "LevelListRecord", "derived", "exists", "exists", ()),)
    with pytest.raises(R.RunnerDomainError, match="outside the governance vocabulary"): R.validate_package_spec(_spec_rec(gsha, arb), governance=g, governance_sha256=gsha)
    with pytest.raises(R.RunnerDomainError, match="missing"): R.validate_package_spec(_spec_rec(gsha, ITEMS[:-1]), governance=g, governance_sha256=gsha)
    bad = [(dc.replace(ITEMS[0], producer_job="reference_stability"), "does not output"), (dc.replace(ITEMS[0], complete_predicate="benchmark_fits"), "does not apply"),
           (dc.replace(ITEMS[1], dependencies=()), "exactly the type's schema"), (dc.replace(ITEMS[1], dependencies=(("primary", "resource_actuals"),)), "must be an item of type"),
           (dc.replace(ITEMS[4], dependencies=(("design", "m6_design_audit"), ("held_out", "m6_design_audit"))), "duplicate"), (dc.replace(ITEMS[6], record_type="ReferenceStructure"), "not derivable")]
    for item, why in bad:
        items = tuple(item if i.name == item.name else i for i in ITEMS)
        with pytest.raises(R.RunnerDomainError, match=why): R.validate_package_spec(_spec_rec(gsha, items), governance=g, governance_sha256=gsha)


# ======================= L2 r3 counterexample 5: forged authorized quarantine =======================
def test_forged_authorized_quarantine_with_negative_cost_refused(chain, tmp_path, repo, stage):
    q = R._tranche_for_tests(L[:5], C.E1_SEED_PANEL[:3], str(tmp_path), stage, **SMOKE)      # 10x60 is the chain's stand-in production shape
    forged = _rehash(dc.replace(q, authorization_version=1, authorization_sha256="a" * 64, authorization_file_sha256="b" * 64, wall_clock_s=-5.0, bytes_written=-10), R._q_body)
    with pytest.raises(R.RunnerDomainError, match="finite and non-negative"): R.validate_quarantine(forged)
    forged2 = _rehash(dc.replace(q, authorization_version=1, authorization_sha256="a" * 64, authorization_file_sha256="b" * 64), R._q_body)
    with pytest.raises(R.RunnerDomainError, match="production shape|committed"): R.validate_quarantine(forged2)
    real = chain["q"]; R.validate_quarantine(real, stage=chain["stage"], repo_root=chain["root"], pinned_root=chain["root"], replay=True)
    tampered = _rehash(dc.replace(real, telemetry_sha256=("0" * 64,) + real.telemetry_sha256[1:]), R._q_body)
    with pytest.raises(R.RunnerDomainError, match="re-execution"): R.validate_quarantine(tampered, stage=chain["stage"], repo_root=chain["root"], pinned_root=chain["root"], replay=True)


# ======================= the two successful paths =======================
def test_successful_canonical_package_persisted_reloaded_and_replayed(chain):
    root, stage, pre, pkg = chain["root"], chain["stage"], chain["pre"], chain["pkg"]
    assert pkg.role == "canonical" and pkg.complete and len(pkg.items) == len(ITEMS)
    rec, _ = R.load_record(chain["pkg_path"], "StagePackage", stage, root, root, require_job="stage1_package", package_dir=pre)
    assert rec == pkg
    names = [r[0] for r in pkg.items]; assert names.index("dense_reference") < names.index("reference_stability") and names.index("m6_held_out_audit") < names.index("m6_audit_qualification")
    forged = _rehash(dc.replace(pkg, complete=True, items=pkg.items[:-1] + ((pkg.items[-1][0], pkg.items[-1][1], pkg.items[-1][2], pkg.items[-1][3], "f" * 64, True, True),)), R._pkg_body)
    with pytest.raises(R.RunnerDomainError, match="replay"): R.validate_stage_package(forged, stage=stage, repo_root=root, pinned_root=root, package_dir=pre)


def test_successful_complete_production_prerequisite_chain(chain):
    root, stage = chain["root"], chain["stage"]; auth, _ = R.load_authorization(root, stage, 2)
    rd = R.validate_prerequisites(auth, stage, root, root)
    assert rd.all_valid_complete and rd.production_ready and {r[0] for r in rd.rows} == {n for n, _, _ in PREREQS} and rd.branch_stops == ()


def test_completion_and_readiness_are_separate_derived_states(chain, monkeypatch):
    """Mike's ruling encoded as GRAMMAR: an adverse-but-valid scientific result stays complete; readiness is separate, and a governance-declared
    branch-stopping result makes production NOT ready while the package remains complete."""
    root, stage = chain["root"], chain["stage"]; auth, _ = R.load_authorization(root, stage, 2); g, gsha = R.load_governance(root, stage)
    monkeypatch.setattr(R, "load_governance", lambda r, s: (_rehash(dc.replace(g, branch_stopping=(("dense_reference", "reference_resolved"),)), R._gov_body), gsha))
    rd = R.validate_prerequisites(auth, stage, root, root)
    assert rd.all_valid_complete and not rd.production_ready and rd.branch_stops == (("dense_reference", "reference_resolved", True),)


# ======================= authorization =======================
def test_authorization_exact_int_version_and_registry_prefix(chain, tmp_path):
    stage = chain["stage"]
    for v in (True, 1.0, "1", 0):
        with pytest.raises(R.RunnerDomainError, match="exact positive"): R.load_authorization(chain["root"], stage, v)
    root = str(tmp_path / "copy"); shutil.copytree(chain["root"], root)                      # alter a COPY: the shared chain repository stays clean
    gov = os.path.join(root, R.GOVERNANCE_ROOT_REL); rp = os.path.join(gov, R.AUTHORIZATION_REGISTRY_REL); reg = R._read_canonical(rp)
    altered = _rehash(R.AuthorizationRegistry(((1, "0" * 64),) + reg.entries[1:]), lambda r: r.entries); _write_canon(rp, altered); _commit(root, "alter registry")
    try:
        with pytest.raises(R.RunnerDomainError, match="append-only|not listed"): R.load_authorization(root, stage, 2)
    finally:
        _write_canon(rp, reg); _commit(root, "restore registry")
    with pytest.raises(R.RunnerDomainError, match="append-only"): R.load_authorization(root, stage, 2)        # history now holds an alteration: refused forever


def test_production_authorization_requires_one_manifest(stage):
    with pytest.raises(R.RunnerDomainError, match="manifest"): R.AuthorizationRecord(9, "d", "i", "a" * 64, "b" * 64, "c" * 64, "d" * 64, ("dense_reference",), False, (), (), True, "")
    with pytest.raises(R.RunnerDomainError, match="manifest"): R.AuthorizationRecord(9, "d", "i", "a" * 64, "b" * 64, "c" * 64, "d" * 64, ("dense_reference",), False, (), (), False, "e" * 64)


# ======================= stage surface =======================
def test_stage_surface_binds_and_forgeries_refuse(repo, stage):
    R.validate_stage_identity(stage, repo)
    assert stage.cache_body_sha256 == A.PRODUCTION_CACHE_BODY_SHA256_LITERAL and all(len(h) == 64 for _, h in stage.gate_record_digests)
    for mut in (dict(role="canonical"), dict(governance_sha256="0" * 64), dict(commit="0" * 40)):
        with pytest.raises(R.RunnerDomainError, match="does not re-derive"): R.validate_stage_identity(_rehash(dc.replace(stage, **mut), R._stage_body), repo)


def test_governance_must_name_the_committed_amendment(tmp_path):
    root = str(tmp_path / "r"); inst = _base_repo(root); _git(root, "init", "-q"); _commit(root, "placed"); _place_and_govern(root, inst)
    gov = os.path.join(root, R.GOVERNANCE_ROOT_REL); _write_canon(os.path.join(gov, R.GOVERNANCE_REL), _gov_rec("0" * 64)); _commit(root, "wrong amendment")
    with pytest.raises(R.ApparatusHalt, match="different"): R.bind_stage(root)
    with pytest.raises(R.RunnerDomainError, match="alphabets"): R.validate_governance(_gov_rec("1" * 64, prereqs=(("stage1_package", "scientific", "mystery"),)))
    with pytest.raises(R.RunnerDomainError, match="vocabulary"): R.validate_governance(_gov_rec("1" * 64, required=("not_in_vocabulary",)))
    with pytest.raises(R.RunnerDomainError, match="branch-stopping"): R.validate_governance(_gov_rec("1" * 64, branch=(("dense_reference", "mystery"),)))
    R.validate_governance(_gov_rec("1" * 64))


# ======================= persistence =======================
def test_canonical_bytes_duplicates_nonfinite_and_envelope_binding(tmp_path, repo, stage):
    ref = P.classify_grid([L[0], L[12], L[23]]); p = str(tmp_path / "r.json"); R.persist_record(ref, p, stage, repo)
    raw = open(p, "rb").read(); open(p, "wb").write(raw + b"\n")
    with pytest.raises(R.RunnerDomainError, match="canonical byte form"): R.load_record(p, "ReferenceStructure", stage, repo)
    t = R._canon(json.loads(raw)); open(p, "wb").write((t[:-1] + ',"job":null}').encode())
    with pytest.raises(R.RunnerDomainError, match="duplicate JSON key"): R.load_record(p, "ReferenceStructure", stage, repo)
    open(p, "wb").write(raw)
    with pytest.raises(R.RunnerDomainError, match="not produced under an authorization"): R.load_record(p, "ReferenceStructure", stage, repo, require_job="dense_reference")


# ======================= runner records =======================
def test_level_record_derives_and_restarts_whole(tmp_path, repo, stage, monkeypatch):
    lr = R.run_level(L[12], str(tmp_path), stage, None, "rehearsal", **SMALL); R.validate_level_record(lr, stage=stage, level_dir=str(tmp_path / C.level_id(L[12])))
    with pytest.raises(R.RunnerDomainError, match="config hash"): R.validate_level_record(_rehash(dc.replace(lr, runs=(dc.replace(lr.runs[0], config_hash="0" * 64),) + lr.runs[1:]), R._level_body))
    prod = _rehash(dc.replace(lr, mode="production", grid=C.E1_GRID, ticks=C.E1_TICKS), R._level_body)
    with pytest.raises(R.RunnerDomainError): R.validate_level_record(prod)
    real = C.run_level_run; calls = {"n": 0}
    def flaky(cfg, d, stem):
        calls["n"] += 1
        if calls["n"] == 7: raise OSError("hiccup")
        return real(cfg, d, stem)
    monkeypatch.setattr(C, "run_level_run", flaky)
    with pytest.raises(R.ApparatusHalt): R.run_level(L[3], str(tmp_path), stage, None, "rehearsal", **SMALL)
    assert not os.path.isdir(tmp_path / C.level_id(L[3]))


def test_production_run_refused_until_ready(chain, tmp_path, monkeypatch):
    root, stage = chain["root"], chain["stage"]
    with pytest.raises(R.RunnerDomainError, match="production is not authorized"): R.run_level(L[0], str(tmp_path), stage, None, "production", repo_root=root, pinned_root=root, authorization_version=1)
    g, gsha = R.load_governance(root, stage)
    monkeypatch.setattr(R, "load_governance", lambda r, s: (_rehash(dc.replace(g, branch_stopping=(("dense_reference", "reference_resolved"),)), R._gov_body), gsha))
    with pytest.raises(R.RunnerDomainError, match="not READY"): R.run_level(L[0], str(tmp_path), stage, None, "production", repo_root=root, pinned_root=root, authorization_version=2)


# ======================= benchmark / sweep ensemble / conformance =======================
def test_benchmark_file_facts_rederived(tmp_path, repo, stage):
    b = R.run_benchmark_smoke(2, str(tmp_path), stage, **SMOKE); ad = str(tmp_path / "benchmark_artifacts"); R.validate_benchmark(b, stage=stage, artifact_dir=ad)
    for mut, why in ((dict(telemetry_bytes_per_run=(1,) + b.telemetry_bytes_per_run[1:]), "byte counts|projections"), (dict(parquet_row_groups=b.parquet_row_groups + 1), "row-group"),
                     (dict(wall_clock_per_run_s=(-1.0,) + b.wall_clock_per_run_s[1:]), "domain"), (dict(free_bytes_measured=-1), "domain")):
        f = dc.replace(b, **mut)
        if "wall_clock" in mut or "telemetry" in mut:
            pw = 640 * max(f.wall_clock_per_run_s) * 1.3; pb = int(640 * max(t + r for t, r in zip(f.telemetry_bytes_per_run, f.rho_bytes_per_run)) * 1.3); f = dc.replace(f, projected_wall_clock_s=pw, projected_bytes=pb, fits_with_margin=pb <= f.free_bytes_measured)
        with pytest.raises(R.RunnerDomainError, match=why): R.validate_benchmark(_rehash(f, R._b_body), stage=stage, artifact_dir=ad)


def test_sweep_ensemble_is_the_exact_canonical_ensemble():
    labels = ("S",) * 24; v1 = V.evaluate(labels, L); d = V.route(labels, L)
    def sw(i):
        f = (i, P.PROJECTION_MASTER, labels, v1.verdict, v1.cause, d.row, 0, 0, (), (), (), tuple(L), labels, v1.verdict, v1.cause, v1.rule, v1.bracket_micro,
             A.PRODUCTION_CACHE_BODY_SHA256_LITERAL, A.PRODUCTION_CACHE_FILE_SHA256_LITERAL, A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL, P.PROJECTION_DECLARATION_SHA256_LITERAL, None, None)
        probe = object.__new__(P.ProjectionSweep)
        for n, val in zip(P.ProjectionSweep.__dataclass_fields__, f + ("",)): object.__setattr__(probe, n, val)
        return P.ProjectionSweep(*f, P._sweep_identity(probe))
    sweeps = tuple(sw(i) for i in range(200)); e = R.SweepEnsemble(sweeps, R._digest(tuple(s.sweep_sha256 for s in sweeps))); R.validate_sweep_ensemble(e)
    short = sweeps[:199]
    with pytest.raises(R.RunnerDomainError, match="0..199"): R.validate_sweep_ensemble(R.SweepEnsemble(short, R._digest(tuple(s.sweep_sha256 for s in short))))
    dup = (sweeps[0],) + sweeps[:199]
    with pytest.raises(R.RunnerDomainError, match="0..199"): R.validate_sweep_ensemble(R.SweepEnsemble(dup, R._digest(tuple(s.sweep_sha256 for s in dup))))
    item = R.PackageItem("design_stability", "DesignStability", "projection_sweeps", "design_complete", "design_stable", (("ref", "dense_reference"), ("sweeps", "projection_sweep_ensemble")))
    assert R._dependency_kwargs(item, {"dense_reference": "REF", "projection_sweep_ensemble": e}) == {"ref": "REF", "sweeps": sweeps}      # sweeps resolved from the loaded ensemble item


def test_conformance_record_reexecutes_m1(tmp_path, repo, stage):
    cp = R.conformance_record(str(tmp_path), stage, **SMALL); R.validate_conformance_record(cp, stage=stage, work_dir=str(tmp_path))
    fake = dc.replace(cp, checks=tuple((k, True) for k, _ in cp.checks) + (("invented", True),))
    fake = dc.replace(fake, result_sha256=R._digest((fake.level_micro, fake.seed, fake.grid, fake.ticks, fake.config_hash, fake.checks, fake.passed, fake.stage_sha256)))
    with pytest.raises(R.RunnerDomainError, match="do not reproduce"): R.validate_conformance_record(fake, stage=stage, work_dir=str(tmp_path))


def test_tranche_quarantine_fail_closed_and_failed_is_ineligible(tmp_path, repo, stage):
    q = R._tranche_for_tests(L[:5], C.E1_SEED_PANEL[:3], str(tmp_path), stage, **SMOKE); R.validate_quarantine(q, stage=stage)
    assert q.status == "passed" and q.cleanup_proven and not any(f.endswith(".parquet") for _, _, fs in os.walk(tmp_path) for f in fs)
    for name in R._QUARANTINE_BLOCKED:
        with pytest.raises(R.QuarantineViolation): getattr(q, name)
    failed = _rehash(dc.replace(q, verifier_passed=(False,) + q.verifier_passed[1:], status="failed"), R._q_body); R.validate_quarantine(failed)
    assert not R.PREDICATES["quarantine_passed"][1](failed) and R.PREDICATES["quarantine_recorded"][1](failed)



# ======================= round 5 (L2 r4 §16 families 1-8; §18 items 10-11) =======================
def test_r5_branch_stop_joined_to_specification():
    g_bad_type = _gov_rec("a" * 64, branch=(("dense_reference", "benchmark_fits"),))
    with pytest.raises(R.RunnerDomainError, match="does not apply"): R.validate_package_spec(_spec_rec("b" * 64), governance=g_bad_type, governance_sha256="b" * 64)
    g_absent = _gov_rec("a" * 64, branch=(("design_stability", "design_complete"),))           # in the vocabulary, absent from the specification
    with pytest.raises(R.RunnerDomainError, match="absent from the Package Specification"): R.validate_package_spec(_spec_rec("b" * 64), governance=g_absent, governance_sha256="b" * 64)
    g_ok = _gov_rec("a" * 64, branch=(("dense_reference", "reference_resolved"),)); R.validate_package_spec(_spec_rec("b" * 64), governance=g_ok, governance_sha256="b" * 64)
    with pytest.raises(R.RunnerDomainError, match="does not apply"): R._eval_predicate("benchmark_fits", P.classify_grid([L[0], L[12], L[23]]))   # fail-closed invocation


def test_r5_halted_audit_is_neither_complete_nor_passing():
    def score(n, scored, halted):
        return A.ClassScore(n, *A.INTENDED[n], 500, scored, halted, 0, "false_nd" if n in A.SCIENTIFIC_CLASSES else "false_scientific", 0, A.clopper_pearson_upper(0, max(scored, 1)), True,
                            scored == 500 and halted == 0, 1.0, scored, ((A.INTENDED[n][0], scored),), (), tuple(("k",) for _ in range(halted)))
    sc = tuple(score(n, 499, 1) if i == 0 else score(n, 500, 0) for i, n in enumerate(A.CLASSES))
    f = (A.AUDIT_VERSION, "design", A.AUDIT_MASTER, 500, "production_frozen", A.PRODUCTION_CACHE_BODY_SHA256_LITERAL, A.PRODUCTION_CACHE_FILE_SHA256_LITERAL,
         A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL, A.AUDIT_DECLARATION_SHA256_LITERAL, A.GENERATOR_DECLARATION_SHA256_LITERAL, sc, False)
    rec = A.AuditRecord(*f, A._digest(A.AuditRecord(*f, "").identity_body()))
    assert R._eval_predicate("audit_record_complete", rec) is False and R._eval_predicate("audit_record_pass", rec) is False
    full = tuple(score(n, 500, 0) for n in A.CLASSES); g = f[:10] + (full, True)
    assert R._eval_predicate("audit_record_complete", A.AuditRecord(*g, A._digest(A.AuditRecord(*g, "").identity_body()))) is True


def test_r5_benchmark_manifest_exact(tmp_path, repo, stage):
    b = R.run_benchmark_smoke(2, str(tmp_path), stage, **SMOKE); ad = str(tmp_path / "benchmark_artifacts"); R.validate_benchmark(b, stage=stage, artifact_dir=ad)
    m = b.artifact_manifest
    for bad, why in ((m[:2] + (m[0],) + m[3:], "duplicate"), (m[:2] + (m[1],) + m[3:], "omits run-config"), (m[3:] + m[:3], "noncanonical order"), (m + (("extra.bin", "0" * 64, 1),), "extra file")):
        with pytest.raises(R.RunnerDomainError, match="artifact manifest|measurement vectors"): R.validate_benchmark(_rehash(dc.replace(b, artifact_manifest=bad), R._b_body), stage=stage, artifact_dir=ad)
    forged_cfg = m[:2] + ((m[2][0], "0" * 64, m[2][2]),) + m[3:]
    with pytest.raises(R.RunnerDomainError, match="contracted configuration"): R.validate_benchmark(_rehash(dc.replace(b, artifact_manifest=forged_cfg), R._b_body), stage=stage, artifact_dir=ad)


def test_r5_tolerance_program_complete_and_incomplete(chain, monkeypatch, tmp_path):
    root, stage = chain["root"], chain["stage"]; out = str(tmp_path / "tol")
    monkeypatch.setattr(R, "TOLERANCE_PROGRAM_LEVELS", (L[0], L[12])); monkeypatch.setattr(R, "verify_frozen_identity", lambda: None); monkeypatch.setattr(P, "TOLERANCE_REPLICATES", 20)   # M5 minimum; canonical value 1000 in production
    R.run_canonical_job("tolerance_ensembles", stage, root, out, root, 1, level_micro=L[0])
    part, ppath = R.run_canonical_job("tolerance_program", stage, root, out, root, 1)
    assert not part.complete and [e[0] for e in part.entries] == [L[0]]                       # a subset is recorded as INCOMPLETE, never as the program
    R.run_canonical_job("tolerance_ensembles", stage, root, out, root, 1, level_micro=L[12])
    with pytest.raises(R.RunnerDomainError, match="omitted"): R.validate_tolerance_program(part, stage=stage, repo_root=root, pinned_root=root, program_dir=out)   # stale program refused
    full, fpath = R.run_canonical_job("tolerance_program", stage, root, out, root, 1)
    assert full.complete and [e[0] for e in full.entries] == [L[0], L[12]]
    rec, _ = R.load_record(fpath, "ToleranceProgram", stage, root, root, require_job="tolerance_program", program_dir=out); assert rec == full
    with pytest.raises(R.RunnerDomainError, match="completion does not derive"): R.validate_tolerance_program(_rehash(dc.replace(part, complete=True), R._tp_body), stage=stage, repo_root=root, pinned_root=root, program_dir=out)
    with pytest.raises(R.RunnerDomainError): R.run_canonical_job("tolerance_ensembles", stage, root, out, root, 1, level_micro=L[5])    # not a program level


def test_r5_pass2_level_record_forces_full_router_replay(chain, monkeypatch):
    """End-to-end at the chain's stand-in production shape: 24 authorized pass-1 levels → router manifest → pass-2 level → reload with FULL replay.
    M2's classification is defined only at 3000 ticks, so status is stubbed to a deterministic function of the cache row; everything else is real."""
    root, stage = chain["root"], chain["stage"]; out = os.path.join(root, "production")
    cache = A.load_production_cache(os.path.join(root, R.CACHE_FILES[0][0]), os.path.join(root, R.CACHE_FILES[1][0]))
    by_theta = {(cache.get(m, s).theta_p, cache.get(m, s).theta_t): i for i, m in enumerate(L) for s in C.E1_SEED_PANEL}
    status = lambda rho, tp, tt: (("NO_SUSTAINED" if by_theta.get((tp, tt), 99) < 10 else "UNRESOLVED" if by_theta.get((tp, tt), 99) < 12 else "SUSTAINED"), None)
    monkeypatch.setattr(R, "run_status", status)
    for m in L: R.run_level(m, out, stage, cache, "production", repo_root=root, pinned_root=root, authorization_version=2, grid=SMALL["grid"], ticks=SMALL["ticks"])
    rm, rpath = R.build_router_manifest(out, stage, root, root, 2, cache)
    assert rm.pass1_labels == ("N",) * 10 + ("U",) * 2 + ("S",) * 12 and rm.insertions_micro and all(rm.reachable)
    m2 = rm.insertions_micro[0]; lr2 = R.run_level(m2, out, stage, cache, "production", repo_root=root, pinned_root=root, authorization_version=2, grid=SMALL["grid"], ticks=SMALL["ticks"])
    assert lr2.pass_number == 2 and lr2.router_manifest_sha256 == R._sha_file(rpath)
    back, _ = R.load_record(os.path.join(out, f"{C.level_id(m2)}.level.json"), "LevelRecord", stage, root, root, require_job="production", level_dir=os.path.join(out, C.level_id(m2)), cache=cache, records_dir=out)
    assert back == lr2
    p1 = os.path.join(out, f"{C.level_id(L[0])}.level.json"); raw = open(p1, "rb").read()
    try:
        open(p1, "wb").write(raw.replace(b'"label":"N"', b'"label":"S"'))                       # a pass-1 record behind the manifest is altered
        with pytest.raises(R.RunnerDomainError): R.load_record(os.path.join(out, f"{C.level_id(m2)}.level.json"), "LevelRecord", stage, root, root, require_job="production", level_dir=os.path.join(out, C.level_id(m2)), cache=cache, records_dir=out)
    finally:
        open(p1, "wb").write(raw)



# ======================= round 6: platform independence =======================
def test_r6_declared_paths_are_platform_independent(monkeypatch):
    """The frozen declaration must digest identically on every platform: no declared path may carry a platform separator, and a
    backslashed path is refused by M7's own identity check (the Windows failure mode that blocked placement)."""
    R.verify_frozen_identity()
    assert "\\" not in repr(R.RUNNER_DECLARATION)
    for name in ("INSTRUMENT_ROOT_REL", "GOVERNANCE_ROOT_REL", "RUNNER_REL", "M7_TEST_REL", "CLEARANCE_DIR_REL"):
        v = getattr(R, name); assert "\\" not in v and "/" in v
        monkeypatch.setattr(R, name, v.replace("/", "\\"))
        with pytest.raises(R.RunnerDomainError, match="platform-independent|differs"): R.verify_frozen_identity()
        monkeypatch.setattr(R, name, v)
    import ntpath
    win = tuple((k, ntpath.join(*v.split("/")) if k == "governance_root" else v) for k, v in R.RUNNER_DECLARATION)
    assert R._digest(win) != R.RUNNER_DECLARATION_SHA256_LITERAL          # the old construction would have diverged on Windows
