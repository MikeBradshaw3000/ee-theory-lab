"""Write the three F8 stage-1 governance records on the CANONICAL machine (run from flights/mfa_fidelity/instrument in the canonical env):
  governance/f8_stage1/F8_THRESHOLD_ADAPTER.json   M6's production adapter as built on this machine (ASCII canonical bytes; written once, committed, never regenerated)
  governance/f8_stage1/F8_GOVERNANCE.json          F8Governance — Mike's ratified values (G1–G6 below) + every identity derived from the placed modules
  governance/f8_stage1/PACKAGE_SPECIFICATION.json  PackageSpecification v1 — the 29 package items with producers, predicates and dependency schemas (G7)
Every value that is not Mike's is DERIVED from the placed modules' literals; validate_governance / validate_package_spec enforce equality, so a wrong
value cannot be written. Prints the identities; writes nothing outside governance/f8_stage1/. Idempotent for the adapter: an existing record is read, not rewritten.
Usage: python make_f8_governance.py <repo_root>"""
import os, sys, dataclasses as dc, hashlib, platform
sys.path.insert(0, os.getcwd())
from mfa_instrument.f8 import runner as R, config as C, closure as CL, evaluator as E, audit as A, classify as K, null as N, verdict as V

repo = os.path.abspath(sys.argv[1]); gov = os.path.join(repo, R.GOVERNANCE_ROOT_REL)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def write_canon(path, obj):
    text = R._canon(R._encode(obj)); text.encode("ascii")
    with open(path, "w", newline="\n", encoding="ascii") as f: f.write(text)
    return sha(path)

# ---- 1. adapter record (this machine's production adapter), written once
ap = os.path.join(gov, R.ADAPTER_RECORD_REL)
if os.path.isfile(ap): adapter_note = "existing (not rewritten)"
else: R.write_adapter_record(repo); adapter_note = "written now"
adapter = A.adapter_from_json(open(ap, "rb").read().decode("ascii"))

# ---- 2. governance record: Mike's values G1–G6
G1_CLAIM_TIER = "finite-horizon persistence at the declared size, horizon, panel and resolution (Contract F8 v0.8.4 s1.1')"
G2_FLIGHT_NAME = "Flight 8 stage 1 (f8_stage1_v1): zero-floor skeleton and realization persistence on the frozen homogeneous lattice"
G3_VOCABULARY = tuple(n for n, _ in R.PACKAGE_ITEMS); G3_REQUIRED = G3_VOCABULARY            # all 29 items required
G4_PREREQUISITES = (("calibration_tranche", "apparatus", "pass"), ("resource_actuals", "apparatus", "pass"),
                    ("mp1_known_answer", "qualification", "pass"), ("m6_audit_qualification", "qualification", "pass"),
                    ("calibration_census", "apparatus", "pass"), ("dense_reference", "scientific", "valid_complete"),
                    ("reference_stability", "scientific", "valid_complete"))
G5_BRANCH_STOPPING = ()                                                                        # none (E1-R precedent; the census ceiling stop path is its PASS requirement)
G6_RECORD_KINDS = (("tolerance_ensembles", "ToleranceEnsemble"), ("tolerance_program", "ToleranceProgram"))   # M5-5 as ratified
MASTERS = (("seed_panel", C.F8_SEED_PANEL_MASTER), ("calibration", C.F8_CALIBRATION_MASTER), ("null_validation_attempt1", N.VALIDATION_REPLICATE_MASTER),
           ("null_validation_attempt2", N.VALIDATION_PROTOCOL_ATTEMPT_2.replicate_master), ("projection", CL.PROJECTION_MASTER), ("known_answer", E.KNOWN_ANSWER_MASTER)) \
          + tuple(zip(("m6_design", "m6_held_out", "m6_pricing"), A.production_masters()))
cr = R.CONTRACT_RECORDS
g = R.F8Governance(version=1, claim_tier=G1_CLAIM_TIER, flight_name=G2_FLIGHT_NAME,
                   contract_sha256=cr[0][1], freeze_record_sha256=cr[1][1], appendix_a_sha256=cr[2][1], interpretation_001_sha256=cr[3][1], interpretation_002_sha256=cr[4][1],
                   ratification_record_sha256=cr[5][1], interpretation_003_sha256=cr[6][1],
                   generator_declaration_markdown_sha256=R.GENERATOR_DECLARATION_MARKDOWN_SHA256, generator_declaration_digest=A.GENERATOR_DECLARATION_SHA256_LITERAL,
                   audit_declaration_digest=A.AUDIT_DECLARATION_SHA256_LITERAL, evaluator_declaration_digest=E.EVALUATOR_SHA256_LITERAL, closure_declaration_digest=CL.CLOSURE_SHA256_LITERAL,
                   null_declaration_digest=N.NULL_SHA256_LITERAL, verdict_declaration_digest=V.VERDICT_DECLARATION_SHA256_LITERAL, classify_declaration_digest=K.CLASSIFY_SHA256_LITERAL,
                   config_declaration_digest=C.F8_DECLARATION_SHA256_LITERAL, null_validation_protocol_sha256=N.VALIDATION_PROTOCOL_ATTEMPT_2_SHA256_LITERAL,
                   null_validation_decision=R.null_decision_from_records(repo), placement_date=A.PLACEMENT_DATE, stability_master=R.stability_master(),
                   stability_seed_panel_sha256=C.F8_STABILITY_PANEL_SHA256_LITERAL, masters=MASTERS, adapter_body_sha256=adapter.body_sha256,
                   package_item_vocabulary=G3_VOCABULARY, required_package_items=G3_REQUIRED, production_prerequisites=G4_PREREQUISITES,
                   branch_stopping=G5_BRANCH_STOPPING, record_kind_mapping=G6_RECORD_KINDS)
g = dc.replace(g, result_sha256=R._digest(R._gov_body(g)))
R.validate_governance(g, adapter_body_sha256=adapter.body_sha256)
gsha = write_canon(os.path.join(gov, R.GOVERNANCE_REL), g)

# ---- 3. package specification: G7 predicates per record type (complete, pass); dependency schema is the type's (DEPENDENCY_SCHEMA), producers are the job graph's
PRED = {"LevelListRecord": ("exists", "exists"), "EnsembleSizesRecord": ("exists", "exists"), "ClosurePublicationRecord": ("closure_covers_levels", "exists"),
        "NullLawRecord": ("null_law_certified", "null_law_certified"), "RouterCollisionRecord": ("exists", "exists"), "ConformanceRecord": ("conformance_production_passed", "conformance_production_passed"),
        "KnownAnswerQualification": ("known_answer_recorded", "known_answer_passed"), "AuditRecord": ("audit_record_complete", "audit_record_pass"),
        "AuditQualification": ("qualification_recorded", "qualification_qualified"), "PricingRecord": ("price_recorded", "price_recorded"),
        "CalibrationCensus": ("census_canonical", "census_ceilings_met"), "ToleranceEnsembles": ("tolerance_ensembles_complete", "tolerance_ensembles_complete"),
        "ToleranceProgram": ("tolerance_program_complete", "tolerance_program_complete"), "ReferenceStructure": ("reference_of_record_dense", "reference_resolved"),
        "StabilityAudit": ("stability_canonical", "stability_all_agree"), "SweepEnsemble": ("sweep_ensemble_canonical", "sweep_ensemble_canonical"),
        "DesignStability": ("design_complete", "design_stable"), "SweepRecord": ("sweep_canonical", "sweep_all_evaluable"),
        "SkeletonAssessment": ("skeleton_assessment_recorded", "skeleton_assessment_complete"), "StabilitySweep": ("sweep_stability", "sweep_stability"),
        "StabilityRecord": ("stability_record_recorded", "stability_record_reproduced"), "MorphologyRecord": ("morphology_recorded", "morphology_pass1_evaluated"),
        "P1Evaluation": ("p1_recorded", "p1_recorded"), "ResourceBenchmark": ("benchmark_canonical", "benchmark_fits")}
DEPS = {"m6_audit_qualification": (("design", "m6_design_audit"), ("held_out", "m6_held_out_audit")), "tolerance_ensembles": (("census", "calibration_census"),),
        "tolerance_program": (("census", "calibration_census"),), "reference_stability": (("primary", "dense_reference"),),
        "design_stability": (("ref", "dense_reference"), ("sweeps", "projection_sweep_ensemble")),
        "skeleton_assessment": (("skeleton_high", "skeleton_high_sweep"), ("skeleton_low", "skeleton_low_sweep"), ("census", "calibration_census")),
        "skeleton_stability": (("canonical_sweep", "skeleton_high_sweep"), ("stability_sweep", "skeleton_stability_sweep"), ("census", "calibration_census")),
        "realization_stability": (("canonical_sweep", "realization_sweep"), ("stability_sweep", "realization_stability_sweep"), ("census", "calibration_census")),
        "p1_evaluation": (("skeleton_high", "skeleton_high_sweep"), ("skeleton_low", "skeleton_low_sweep"), ("realization", "realization_sweep"), ("census", "calibration_census"))}
items = tuple(R.PackageItem(n, t, R.default_producer(n, t), PRED[t][0], PRED[t][1], DEPS.get(n, ())) for n, t in R.PACKAGE_ITEMS)
spec = R.PackageSpecification(1, gsha, items); spec = dc.replace(spec, result_sha256=R._digest(R._spec_body(spec)))
R.validate_package_spec(spec, governance=g, governance_sha256=gsha)
ssha = write_canon(os.path.join(gov, R.PACKAGE_SPEC_REL), spec)

lines = [f"platform {platform.platform()} py{platform.python_version()}",
         f"adapter record {R.ADAPTER_RECORD_REL} {sha(ap)} ({adapter_note}); payload_identity {adapter.payload_identity}; body_sha256 {adapter.body_sha256}",
         f"governance {R.GOVERNANCE_REL} {gsha}; result_sha256 {g.result_sha256}; stability_master {g.stability_master}; placement_date {g.placement_date}",
         f"masters {dict(g.masters)}", f"null decision {g.null_validation_decision}",
         f"package specification {R.PACKAGE_SPEC_REL} {ssha}; items {len(items)}; result_sha256 {spec.result_sha256}"]
print("\n".join(lines))
