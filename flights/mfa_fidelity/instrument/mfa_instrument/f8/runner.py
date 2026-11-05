"""mfa_instrument/f8/runner.py — Flight 8 stage-1 module M7: the stage package (Contract F8 v0.8.4 §7.1–§7.4, §8; E1-R's
grammar carried from `e1/runner.py` `f33fbb54c115225c…` (L2 M7 rounds 1–7); F8 Interpretations 001 `6bf7304fd3ee287c…` and
002 `198d2991dd12168c…`; the stage-1 ratification record v1.0 `cdedfcb4540d950b…` §E).

THREE PRINCIPLES (E1 M7, L2 §3–§13, carried unchanged)
A. AUTHORIZATION IS A RECORD, NOT A BOOLEAN. Source literals grant nothing — ever. Every canonical job, the tranche, production
   and the package each require a separate, Mike-ratified, digest-bound AuthorizationRecord committed in the governance
   directory, naming the exact bound stage identity, the governance and package-specification identities, the authorized jobs,
   the exact tranche panel and the production prerequisites. Every canonical result is produced THROUGH `run_canonical_job`,
   which writes the authorization binding into the persisted envelope from the record it just loaded; a pre-authorization
   result cannot be wrapped afterwards.
B. THE IDENTITY SURFACE IS LARGER THAN CODE. The F8 stage binds: every runtime source and cleared test of the whole
   `mfa_instrument` package (e1, f8, core, gates — from disk, equal to cleared literals, committed, clean); the M7 placement
   record; the authoritative Gate A/B/R0 records; the FROZEN CONTRACT RECORDS (contract v0.8.4, freeze record, Appendix A,
   Interpretations 001 and 002, the ratification record v1.0 — full identities as literals); the committed THRESHOLD ADAPTER
   RECORD (M6's `ThresholdAdapter` as built on the canonical machine: keys, indices and surface re-derived here, the
   platform-sensitive payload identity compared and the match recorded); the pinned ancestor and the lock identity through
   Gate B's environment checker; Mike's typed F8 governance record and the Package Specification (absent → `pre_governance`);
   the versioned record-schema identity.
C. EVERY RECORD DERIVES, INCLUDING M7'S OWN. LevelRecord from persisted run artifacts (M1's density parquet + a canonical run
   record), the summary fields recomputed from the trace by M-P1's `observation_from_result` and the status by M2 against the
   adapter; full re-execution replay on demand and mandatory for the tranche; CalibrationCensus (job 0) with the CANONICAL
   role issued ONLY here; SweepRecords by M-P1's replaying builder; the audits and qualifications by M6's and M-P1's own
   validators; typed per-item package records with item-specific predicates; StagePackage with a replaying validator, one
   file per item, written LAST.

WHAT F8 M7 DISCHARGES (ratification record §E): (1) sole issuer of the canonical census role; (2) M6's verdict of record is
the final-level-set verdict — asserted on every persisted AuditRecord by re-evaluating each class's sweeps' final labels is
M6's own validator's job; here the package predicate requires `ensemble_pass` and completeness; (3) `is_qualification_evidence`
removed from M3 in the same placement (disclosed); (4) `price_familywise` docstring corrected in M3 (disclosed); (5) the null-
validation protocol identity travels in the governance record with its decision; (6) the M-P1 qualification of record is the
job `mp1_known_answer`, M7-issued, canonical machine; (7) Interpretation identities, declaration digests, adapter identity (from
the committed ASCII JSON, never from the suite record) and the masters' derivation are fields of the governance record and of
the stage; (8) the two stale-comment obligations are left to the next touch of their test modules; (9) exp()-derived fields are
recorded as what the canonical machine saw and compared, never assumed.

STAGE ROLES: `canonical` (environment conforms; placement, governance, specification and adapter records committed; adapter
platform match); `pre_governance` (conforming environment and placement, governance records absent); `noncanonical`.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import posixpath as _pp
import platform
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..config import MICRO_UNITS
from ..gates.gate_b import environment as _ENV
from . import audit as _A
from . import classify as _K
from . import closure as _CL
from . import config as _C
from . import dynamics as _D
from . import evaluator as _E
from . import null as _N
from . import verdict as _V
from .classify import level_counts, level_label, run_status
from .config import F8_GRID, F8_LEVELS_MICRO, F8_SEED_PANEL, F8_CALIBRATION_SEED_PANEL, F8_TICKS, level_id
from .verdict import route

RUNNER_VERSION = "f8_stage1_m7_v1 / Contract F8 v0.8.4 s7 / E1-R grammar carried / Interpretations 001-002 / ratification v1.0"
RECORD_SCHEMA_VERSION = 1


class RunnerDomainError(ValueError): ...
class ApparatusHalt(RuntimeError): ...
class EvaluabilityHalt(RuntimeError):
    """A router-inserted pass-2 level that M1's frozen production guard cannot execute (production-shape runs are defined on the
    pass-1 grid only). Halts the LEVEL; recorded on the morphology record; never an apparatus failure of M7."""
class AnomalyHalt(RuntimeError): ...
class QuarantineViolation(PermissionError): ...


def _digest(obj) -> str: return hashlib.sha256(repr(obj).encode()).hexdigest()
def _sha_file(path: str) -> str: return hashlib.sha256(open(path, "rb").read()).hexdigest()
def _is_hex(s, n: int) -> bool: return isinstance(s, str) and len(s) == n and all(c in "0123456789abcdef" for c in s)
def _canon(doc) -> str: return json.dumps(doc, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _frozen_mapping(decl, name):
    keys = [k for k, _ in decl]
    if len(set(keys)) != len(keys): raise RunnerDomainError(f"{name}: duplicate declaration field names")
    return dict(decl)


# ----------------------------------------------------------------------------- frozen declaration
INSTRUMENT_ROOT_REL = "flights/mfa_fidelity/instrument"            # POSIX literals: repo-relative, platform-independent
GOVERNANCE_ROOT_REL = "flights/mfa_fidelity/governance/f8_stage1"
RUNNER_REL = "mfa_instrument/f8/runner.py"
M7_TEST_REL = "tests/test_f8_m7.py"
PLACEMENT_RECORD_REL = "M7_PLACEMENT_RECORD.json"
GOVERNANCE_REL = "F8_GOVERNANCE.json"
PACKAGE_SPEC_REL = "PACKAGE_SPECIFICATION.json"
ADAPTER_RECORD_REL = "F8_THRESHOLD_ADAPTER.json"                   # M6's production adapter as built on the canonical machine (ASCII, canonical bytes)
RATIFICATION_RECORD_REL = "F8_STAGE1_RATIFICATION_RECORD_v1_0.md"
AUTHORIZATION_GLOB = "AUTHORIZATION_"
AUTHORIZATION_REGISTRY_REL = "AUTHORIZATION_REGISTRY.json"
PREREQUISITES_REL = "prerequisites"
PREREQ_MANIFEST_REL = "PRODUCTION_PREREQUISITES.json"
SUITE_RECORD_REL = "M7_SUITE_RECORD.json"
CLEARANCE_DIR_REL = "flights/mfa_fidelity/build_records"
ANCESTOR_COMMIT = "4d9a622"                      # Gate A's pinned ancestor commit (short id as the gate record names it)
GATE_RECORDS: Tuple[Tuple[str, str], ...] = (    # authoritative records, full cleared identities (E1 M7, carried)
    ("flights/mfa_fidelity/gates/gate_a/GATE_A_AUTHORITATIVE_RECORD.md", "719a9706f34e6c08119993f1826242939e6a2331fc77cf50a61c769d2710ca74"),
    ("flights/mfa_fidelity/gates/gate_b/GATE_B_AUTHORITATIVE_CERTIFICATION_RECORD.md", "940d88a426d9530449d4c9d93d4a23085d354b678e2229edcf849806f6685883"),
    ("flights/mfa_fidelity/gates/gate_r0/GATE_R0_REGISTER_CLOSURE.md", "59fd2a54a344f994346001eab2ec14b03357018536e3386318138df079e6e741"),
)
CONTRACT_RECORDS: Tuple[Tuple[str, str], ...] = (   # the frozen F8 contract surface, full identities measured from a fresh clone at 2c8827b
    ("flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md", "e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182"),
    ("flights/mfa_fidelity/contracts/flight8/FLIGHT_8_FREEZE_RECORD.md", "16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2"),
    ("flights/mfa_fidelity/contracts/flight8/APPENDIX_A_OF_RECORD.md", "94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653"),
    ("flights/mfa_fidelity/rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md", "6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86"),
    ("flights/mfa_fidelity/rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md", "198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034"),
    ("flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_RATIFICATION_RECORD_v1_0.md", "cdedfcb4540d950be69695b589b3f8cc8b5164278b7d57e850eb7ff8b601346b"),
    ("flights/mfa_fidelity/rulings/F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md", "6ebf0ad3efbe8e0e74b45e63d5f6ba550441897f3ff6898749230c064c993e9e"),   # ratified 2026-11-03, commit 1978a01 (L2 r2 R2-4: bound unconditionally)
)
DECLARATION_RECORDS: Tuple[Tuple[str, str], ...] = (   # approved declaration / decision documents the governance record must name BY IDENTITY (L2 r1 D7)
    ("flights/mfa_fidelity/build_records/F8_M6_GENERATOR_DECLARATION_v0_3.md", "c73980585fc238209453ebadb4707d961e41d77b7970435e8ce4113298868e47"),
    ("flights/mfa_fidelity/build_records/F8_M3_NULL_VALIDATION_ATTEMPT1_FAILED_2026-10-27.json", "a95509d3e809d70ba1d8977735ff88868d02ea3ac961305a70886f1128ce28ff"),
    ("flights/mfa_fidelity/build_records/F8_M3_NULL_VALIDATION_PROTOCOL_ATTEMPT2_RATIFIED_2026-10-27.json", "834a788bd39ee77123260d1023bc29f9343c684725004f36339a0be97ee2bfa4"),
    ("flights/mfa_fidelity/build_records/F8_M3_NULL_VALIDATION_ATTEMPT2_2026-10-28.json", "b10a9d5a89e43978a756d704e2e730bb8cba69953f82d03fa52e3e715dc4741e"),
)
GENERATOR_DECLARATION_MARKDOWN_REL, GENERATOR_DECLARATION_MARKDOWN_SHA256 = DECLARATION_RECORDS[0]
NULL_ATTEMPT2_RECORD_REL = DECLARATION_RECORDS[3][0]
STABILITY_MASTER_PREFIX = 9                          # config.F8_STABILITY_MASTER = 9e8 + the build date of the M1 touch (Interpretation 003 pt 6): M1's own convention for its panels
STABILITY_BUILD_DATE = 20261102
PREREQ_VOCAB = ("calibration_tranche", "resource_actuals", "mp1_known_answer", "m6_audit_qualification", "calibration_census", "dense_reference", "reference_stability")   # the package is the END state, never a prerequisite of the jobs it contains
SCIENTIFIC_JOBS = ("skeleton_census", "skeleton_stability", "realization_census", "realization_stability", "p1_evaluation")   # s7.1: run only after passage of both qualifications — the readiness gate
LATTICE_JOBS = ("calibration_census", "skeleton_census", "realization_census", "skeleton_stability", "realization_stability")
JOB_OBJECTS: Tuple[Tuple[str, Tuple[str, ...], str], ...] = (   # the ONE exact job -> (permitted objects, panel) mapping, enforced before any run and on every persisted level (L2 r1 D2)
    ("calibration_census", ("skeleton_high", "realization"), "calibration"),
    ("skeleton_census", ("skeleton_high", "skeleton_low"), "canonical"),
    ("realization_census", ("realization",), "canonical"),
    ("skeleton_stability", ("skeleton_high",), "stability"),          # Interpretation 003 pt 7: the independent stability panel
    ("realization_stability", ("realization",), "stability"),
)
MANDATORY_PREREQUISITES: Tuple[Tuple[str, str], ...] = (("mp1_known_answer", "pass"), ("m6_audit_qualification", "pass"), ("calibration_census", "pass"))   # s7.1 + s3.4/s7.3 item 0 (L2 r1 D3a)
PREREQ_KINDS = ("apparatus", "qualification", "scientific")
PREREQ_REQUIREMENTS = ("pass", "valid_complete")
BENCHMARK_LEVEL_MICRO = F8_LEVELS_MICRO[12]      # 1,423,913: the frozen canonical benchmark panel (level 12; first three canonical seeds)
BENCHMARK_SEEDS = 3
TRANCHE_SEEDS = 3                               # [PROPOSED] E1 v0.2 §7.5, carried
TRANCHE_LEVELS = 5                              # [PROPOSED]
BENCHMARK_MARGIN = 0.30
PRODUCTION_RUNS = (24 * 20 * 2) + (24 * 20 * 2) + (24 * 20) + (24 * 20 * 2)   # job 0 (2 objects) + skeleton census (2 objects) + realization census + two stability jobs = 3,360 production-shape lattice runs (Interpretation 003 pt 10)
CANONICAL_JOBS = ("mp1_known_answer", "m6_design_audit", "m6_held_out_audit", "m6_audit_qualification", "m6_price",
                  "calibration_census", "tolerance_program", "dense_reference", "reference_stability", "projection_sweeps",
                  "skeleton_census", "skeleton_stability", "realization_census", "realization_stability", "p1_evaluation",
                  "resource_benchmark", "stage1_package")
SOURCE_LITERALS_GRANT_NOTHING = True
STAGE_ROLES = ("canonical", "pre_governance", "noncanonical")
HALT_CLASSES = ("apparatus", "evaluability_operational", "anomaly_domain")
RUN_OBJECTS = tuple(_C.OBJECT_CODES)             # skeleton_high, skeleton_low, realization, null
PANELS = ("canonical", "calibration", "stability")
PACKAGE_ITEMS: Tuple[Tuple[str, str], ...] = (   # [PROPOSED]; the frozen list lives in the Package Specification Record
    ("level_list_and_spacings", "LevelListRecord"), ("ensemble_sizes", "EnsembleSizesRecord"), ("closure_publication", "ClosurePublicationRecord"),
    ("null_law", "NullLawRecord"), ("router_collision_record", "RouterCollisionRecord"), ("conformance_preflight", "ConformanceRecord"),
    ("mp1_known_answer", "KnownAnswerQualification"), ("m6_design_audit", "AuditRecord"), ("m6_held_out_audit", "AuditRecord"),
    ("m6_audit_qualification", "AuditQualification"), ("m6_price", "PricingRecord"),
    ("calibration_census", "CalibrationCensus"), ("tolerance_ensembles", "ToleranceEnsembles"), ("tolerance_program", "ToleranceProgram"),
    ("dense_reference", "ReferenceStructure"), ("reference_stability", "StabilityAudit"), ("projection_sweep_ensemble", "SweepEnsemble"), ("design_stability", "DesignStability"),
    ("skeleton_high_sweep", "SweepRecord"), ("skeleton_low_sweep", "SweepRecord"), ("skeleton_assessment", "SkeletonAssessment"),
    ("skeleton_stability_sweep", "StabilitySweep"), ("skeleton_stability", "StabilityRecord"),
    ("realization_sweep", "SweepRecord"), ("realization_morphology", "MorphologyRecord"),
    ("realization_stability_sweep", "StabilitySweep"), ("realization_stability", "StabilityRecord"), ("p1_evaluation", "P1Evaluation"),
    ("resource_actuals", "ResourceBenchmark"),
)
PREDICATE_IDS = ("exists", "reference_of_record_dense", "reference_resolved", "stability_canonical", "stability_all_agree", "design_complete", "design_stable",
                 "sweep_ensemble_canonical", "audit_record_complete", "audit_record_pass", "qualification_recorded", "qualification_qualified",
                 "known_answer_recorded", "known_answer_passed", "census_canonical", "census_ceilings_met", "tolerance_program_recorded", "tolerance_program_complete",
                 "sweep_canonical", "sweep_all_evaluable", "sweep_stability", "morphology_recorded", "morphology_pass1_evaluated", "morphology_final_set_identical", "stability_record_recorded", "stability_record_reproduced",
                 "skeleton_assessment_recorded", "skeleton_assessment_complete", "tolerance_ensembles_recorded", "tolerance_ensembles_complete",
                 "p1_recorded", "p1_evaluated", "benchmark_canonical", "benchmark_fits", "conformance_production", "conformance_production_passed",
                 "null_law_certified", "closure_covers_levels", "price_recorded", "quarantine_recorded", "quarantine_passed")
BOUND_SOURCES: Tuple[Tuple[str, str], ...] = (   # cleared placed identities at 2c8827b (M1–M6, M-P1 sources and tests; e1; instrument core; gates). null.py is the M7-touched
    ("mfa_instrument/__init__.py", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),   # version placed WITH this module (obligations 3–4).
    ("mfa_instrument/bridge.py", "0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e"),
    ("mfa_instrument/config.py", "f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872"),
    ("mfa_instrument/dynamics.py", "483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8"),
    ("mfa_instrument/e1/__init__.py", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("mfa_instrument/e1/audit.py", "ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3"),
    ("mfa_instrument/e1/classify.py", "db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3"),
    ("mfa_instrument/e1/config.py", "934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22"),
    ("mfa_instrument/e1/null.py", "58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa"),
    ("mfa_instrument/e1/projection.py", "29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2"),
    ("mfa_instrument/e1/runner.py", "f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769"),
    ("mfa_instrument/e1/verdict.py", "e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf"),
    ("mfa_instrument/f8/__init__.py", "49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d"),
    ("mfa_instrument/f8/audit.py", "81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e"),
    ("mfa_instrument/f8/classify.py", "42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219"),
    ("mfa_instrument/f8/closure.py", "9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278"),
    ("mfa_instrument/f8/config.py", "3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7"),   # M1 touched with M7 round 2 (third panel; disclosed)
    ("mfa_instrument/f8/dynamics.py", "cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b"),
    ("mfa_instrument/f8/evaluator.py", "61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a"),
    ("mfa_instrument/f8/null.py", "2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb"),
    ("mfa_instrument/f8/verdict.py", "c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2"),
    ("mfa_instrument/gates/__init__.py", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("mfa_instrument/gates/gate_a.py", "a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c"),
    ("mfa_instrument/gates/gate_b/__init__.py", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("mfa_instrument/gates/gate_b/b1.py", "5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99"),
    ("mfa_instrument/gates/gate_b/b2.py", "c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83"),
    ("mfa_instrument/gates/gate_b/comparators.py", "5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d"),
    ("mfa_instrument/gates/gate_b/environment.py", "d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87"),
    ("mfa_instrument/gates/gate_b/qualification.py", "fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43"),
    ("mfa_instrument/gates/gate_b/reference.py", "085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d"),
    ("mfa_instrument/gates/gate_b/stub.py", "9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6"),
    ("mfa_instrument/gates/gate_r0.py", "4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f"),
    ("mfa_instrument/init.py", "43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18"),
    ("mfa_instrument/rng.py", "fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62"),
    ("mfa_instrument/schema_contract.py", "e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc"),
    ("mfa_instrument/telemetry.py", "5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725"),
    ("mfa_instrument/verify.py", "9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d"),
    ("tests/test_f8_m1.py", "ca9a547286290aabc497fc228e10dd845711cd1b359bc21fcb125d92e8285007"),   # M1 test touched with M7 round 2
    ("tests/test_f8_m2_m3.py", "d0d26e75280dffef269e05f95e391b1db775a0f4712a5b3eac2f31ff50336460"),
    ("tests/test_f8_m4.py", "8b8976b2c3602e0cc3932676cc6a091c69569af515bc183c374208578afa6d12"),
    ("tests/test_f8_m5.py", "27cb5c965242ad2bde9aa61c5403eb97473190b67b1d232a2d801c5bd2097b41"),
    ("tests/test_f8_mp1.py", "f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d"),
    ("tests/test_f8_m6.py", "808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca"),
)

RUNNER_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("version", RUNNER_VERSION), ("record_schema_version", RECORD_SCHEMA_VERSION), ("tranche", (TRANCHE_SEEDS, TRANCHE_LEVELS)),
    ("benchmark_margin", BENCHMARK_MARGIN), ("production_runs", PRODUCTION_RUNS), ("canonical_jobs", CANONICAL_JOBS),
    ("source_literals_grant_nothing", SOURCE_LITERALS_GRANT_NOTHING), ("stage_roles", STAGE_ROLES), ("halt_classes", HALT_CLASSES),
    ("package_items_proposed", PACKAGE_ITEMS), ("bound_sources", BOUND_SOURCES), ("gate_records", GATE_RECORDS), ("contract_records", CONTRACT_RECORDS),
    ("ancestor_commit", ANCESTOR_COMMIT), ("lock_sha256", _ENV.EXPECTED_LOCK_SHA256), ("pin_count", _ENV.EXPECTED_PIN_COUNT),
    ("prereq_vocab", PREREQ_VOCAB), ("scientific_jobs", SCIENTIFIC_JOBS), ("lattice_jobs", LATTICE_JOBS), ("benchmark_panel", (BENCHMARK_LEVEL_MICRO, BENCHMARK_SEEDS)), ("predicate_ids", PREDICATE_IDS),
    ("prereq_kinds", PREREQ_KINDS), ("prereq_requirements", PREREQ_REQUIREMENTS), ("run_objects", RUN_OBJECTS), ("panels", PANELS), ("job_objects", JOB_OBJECTS),
    ("mandatory_prerequisites", MANDATORY_PREREQUISITES), ("declaration_records", DECLARATION_RECORDS), ("stability_master_rule", "config.F8_STABILITY_MASTER = 9e8 + 20261102 (the M1 touch's build date; M1's convention); panel = config.generate_seed_panel(master), a frozen M1 literal, disjoint from the canonical, calibration and E1 panels"),
    ("clearance_marker", "FINAL VERDICT: SOUND"),
    ("governance_root", GOVERNANCE_ROOT_REL), ("adapter_record", ADAPTER_RECORD_REL), ("restart_granularity", "whole level (one object, one panel)"),
    ("run_artifacts", "per run: <level_id>/s<seed>.<obj>.rho_global.parquet (M1 write_rho_table) + s<seed>.<obj>.run.json (canonical); replay = M1 re-execution on the same platform"),
    ("census_role_issuer", "the CANONICAL CalibrationCensus role is issued only by run_canonical_job('calibration_census')"),
    ("authorization", "separate Mike-ratified AuthorizationRecord in the governance directory; source grants nothing"),
)
RUNNER_DECLARATION_SHA256_LITERAL = "0ce2e7b5eaca1804b10cc68706380bd93f5efe007c34c7fe74a6eb878cd8b4b8"   # re-established 2026-11-02 (round 2; round 1 was 7b2ecefdd9b30365…)


def verify_frozen_identity() -> None:
    _C.verify_frozen_identity(); _K.verify_frozen_identity(); _N.verify_frozen_identity(); _V.verify_frozen_identity(); _CL.verify_frozen_identity(); _E.verify_frozen_identity(); _A.verify_frozen_identity()
    if not _is_hex(RUNNER_DECLARATION_SHA256_LITERAL, 64): raise RunnerDomainError("runner declaration digest literal is not a 64-hex sha256 (no sentinel or placeholder is accepted; R2-7 applied to M7 itself)")
    if _digest(RUNNER_DECLARATION) != RUNNER_DECLARATION_SHA256_LITERAL: raise RunnerDomainError("runner declaration differs from its frozen literal digest")
    d = _frozen_mapping(RUNNER_DECLARATION, "RUNNER_DECLARATION")
    live = {"version": RUNNER_VERSION, "record_schema_version": RECORD_SCHEMA_VERSION, "tranche": (TRANCHE_SEEDS, TRANCHE_LEVELS), "benchmark_margin": BENCHMARK_MARGIN,
            "production_runs": PRODUCTION_RUNS, "canonical_jobs": CANONICAL_JOBS, "source_literals_grant_nothing": SOURCE_LITERALS_GRANT_NOTHING, "stage_roles": STAGE_ROLES,
            "halt_classes": HALT_CLASSES, "package_items_proposed": PACKAGE_ITEMS, "bound_sources": BOUND_SOURCES, "gate_records": GATE_RECORDS, "contract_records": CONTRACT_RECORDS,
            "ancestor_commit": ANCESTOR_COMMIT, "lock_sha256": _ENV.EXPECTED_LOCK_SHA256, "pin_count": _ENV.EXPECTED_PIN_COUNT, "governance_root": GOVERNANCE_ROOT_REL,
            "prereq_vocab": PREREQ_VOCAB, "scientific_jobs": SCIENTIFIC_JOBS, "lattice_jobs": LATTICE_JOBS, "benchmark_panel": (BENCHMARK_LEVEL_MICRO, BENCHMARK_SEEDS), "predicate_ids": PREDICATE_IDS, "prereq_kinds": PREREQ_KINDS,
            "prereq_requirements": PREREQ_REQUIREMENTS, "run_objects": RUN_OBJECTS, "panels": PANELS, "adapter_record": ADAPTER_RECORD_REL, "job_objects": JOB_OBJECTS,
            "mandatory_prerequisites": MANDATORY_PREREQUISITES, "declaration_records": DECLARATION_RECORDS}
    for k, v in live.items():
        if d[k] != v or type(d[k]) is not type(v): raise RunnerDomainError(f"runner declaration field {k} differs from the live global")
    if PRODUCTION_RUNS != 3360 or BENCHMARK_MARGIN != 0.30 or SOURCE_LITERALS_GRANT_NOTHING is not True or _ENV.EXPECTED_PIN_COUNT != 20 or len({p for p, _ in BOUND_SOURCES}) != len(BOUND_SOURCES):
        raise RunnerDomainError("runner hard values differ from the contract")
    if any(not _is_hex(h, 64) for _, h in BOUND_SOURCES if "PLACEHOLDER" not in h) or any(not _is_hex(h, 64) for _, h in GATE_RECORDS) or any(not _is_hex(h, 64) for _, h in CONTRACT_RECORDS):
        raise RunnerDomainError("bound identities malformed")
    if set(PREDICATE_IDS) != set(PREDICATES): raise RunnerDomainError("declared predicate alphabet differs from the implemented predicates")
    if {t for _, t in PACKAGE_ITEMS} - set(VALIDATORS): raise RunnerDomainError("a proposed package item names a type without a validator")
    if "\\" in repr(RUNNER_DECLARATION): raise RunnerDomainError("declared paths must be platform-independent POSIX literals")
    if BENCHMARK_LEVEL_MICRO not in F8_LEVELS_MICRO or set(CANONICAL_JOBS) != {j for j, _, _ in JOB_GRAPH}: raise RunnerDomainError("benchmark level or job list inconsistent")
    jo = {j for j, _, _ in JOB_OBJECTS}
    if jo != set(LATTICE_JOBS) or any(p not in PANELS or any(o not in RUN_OBJECTS or o == "null" for o in objs) for _, objs, p in JOB_OBJECTS): raise RunnerDomainError("job -> object mapping inconsistent with the lattice jobs, panels and objects")
    if any(not _is_hex(h, 64) for _, h in DECLARATION_RECORDS) or len(CONTRACT_RECORDS) != 7: raise RunnerDomainError("declaration record identities malformed or a contract record is unbound")
    sp = stability_seed_panel()
    if stability_master() != STABILITY_MASTER_PREFIX * 10**8 + STABILITY_BUILD_DATE or sp != _C.generate_seed_panel(stability_master()) or len(set(sp)) != 20 \
            or set(sp) & (set(F8_SEED_PANEL) | set(F8_CALIBRATION_SEED_PANEL) | set(_C.E1_RETIRED_SEED_PANEL)):
        raise RunnerDomainError("M1's stability panel is not the declared rule's or is not disjoint from the canonical, calibration and E1 panels (Interpretation 003 pt 6)")


NULL_VALIDATION_DECISION_OF_RECORD: Tuple[Tuple[str, object], ...] = (   # TYPED decision facts (ratification v1.0 §E.5; L2 r1 D7), re-derived at bind from the committed attempt records
    ("protocol_sha256", "20ae18f0a85d9b6ce3972acb2630529bd300a92fbc16e5f6f8b1a48a537abf2a"), ("attempt", 2), ("status", "PASSED"), ("qualification_passed", True),
    ("primary_alpha", 0.025), ("auxiliary_alpha", 0.025), ("designated_statistic", 0.04450291658966543), ("primary_bound", 0.04680826120821986), ("auxiliary_bound", 0.05781267909234066),
    ("module_default_alpha", 0.05), ("module_default_bound", 0.04294694083467376), ("module_default_dkw_passed", False),
    ("attempt_1_status", "FAILED"), ("attempt_1_disposition", "L2 round-2 ruling 2026-10-27: designated terminal-window DKW is the primary statistic; FAIL (0.0837 > 0.0679); union PASS cannot substitute; record retained immutable"),
)


def null_decision_from_records(repo_root: str) -> Tuple[Tuple[str, object], ...]:
    """Derive the decision tuple from the COMMITTED attempt records (identities fixed in DECLARATION_RECORDS): the only source of these values."""
    a1 = json.loads(open(os.path.join(repo_root, DECLARATION_RECORDS[1][0]), "rb").read().decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
    a2 = json.loads(open(os.path.join(repo_root, NULL_ATTEMPT2_RECORD_REL), "rb").read().decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
    r = a2["record"]; pr = _N.VALIDATION_PROTOCOL_ATTEMPT_2
    if a2["protocol_sha256"] != _N.VALIDATION_PROTOCOL_ATTEMPT_2_SHA256_LITERAL or r["protocol_sha256"] != a2["protocol_sha256"]: raise ApparatusHalt("attempt-2 record does not name the ratified protocol")
    return (("protocol_sha256", a2["protocol_sha256"]), ("attempt", int(a2["attempt"])), ("status", a2["status"]), ("qualification_passed", bool(r["qualification_passed"])),
            ("primary_alpha", pr.primary_alpha), ("auxiliary_alpha", pr.auxiliary_alpha), ("designated_statistic", float(r["dkw_sup_deviation"])), ("primary_bound", float(a2["primary_bound"])), ("auxiliary_bound", float(a2["auxiliary_bound"])),
            ("module_default_alpha", 0.05), ("module_default_bound", float(r["dkw_bound"])), ("module_default_dkw_passed", bool(r["dkw_passed"])),
            ("attempt_1_status", a1["status"]), ("attempt_1_disposition", a1["disposition"]))


def stability_master() -> int: return int(_C.F8_STABILITY_MASTER)


def stability_seed_panel() -> Tuple[int, ...]: return tuple(_C.F8_STABILITY_SEED_PANEL)


# ----------------------------------------------------------------------------- records registry and schema identity
RECORD_TYPES: Dict[str, type] = {}


def _register(*classes) -> None:
    for c in classes:
        if c.__name__ in RECORD_TYPES and RECORD_TYPES[c.__name__] is not c: raise RunnerDomainError(f"record type name {c.__name__} already registered")
        RECORD_TYPES[c.__name__] = c


def record_schema_identity() -> str:
    return _digest((RECORD_SCHEMA_VERSION, tuple(sorted((f"{c.__module__}.{c.__qualname__}", tuple((f.name, str(f.type)) for f in dataclasses.fields(c))) for c in RECORD_TYPES.values()))))


def _git(repo_root: str, *args) -> str:
    out = subprocess.run(["git", "-C", repo_root, *args], capture_output=True, text=True)
    if out.returncode != 0: raise ApparatusHalt(f"git {' '.join(args)} failed: {out.stderr.strip()[:120]}")
    return out.stdout.strip()


def _committed_equals_working(repo_root: str, rel: str) -> bool:
    blob = subprocess.run(["git", "-C", repo_root, "show", f"HEAD:{rel.replace(os.sep, '/')}"], capture_output=True)
    return blob.returncode == 0 and hashlib.sha256(blob.stdout).hexdigest() == _sha_file(os.path.join(repo_root, rel))


def _refuse_const(c): raise RunnerDomainError(f"nonfinite JSON constant {c}")


def _no_dup(pairs):
    d = {}
    for k, v in pairs:
        if k in d: raise RunnerDomainError(f"duplicate JSON key {k!r}")
        d[k] = v
    return d


def _read_canonical(path: str):
    raw = open(path, "rb").read()
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
    if _canon(doc).encode() != raw: raise RunnerDomainError(f"{os.path.basename(path)} is not in canonical byte form")
    return _decode(doc)


# ----------------------------------------------------------------------------- 1. stage identity
@dataclass(frozen=True)
class StageIdentity:
    role: str
    commit: str                                      # the last commit that touched the bound surface
    head_commit: str                                 # descriptive (excluded from the identity body)
    source_digests: Tuple[Tuple[str, str], ...]
    runner_sha256: str
    m7_test_sha256: str
    placement_record_sha256: Optional[str]
    gate_record_digests: Tuple[Tuple[str, str], ...]
    contract_record_digests: Tuple[Tuple[str, str], ...]
    ancestor_commit: str
    lock_sha256: str
    environment_conforms: bool
    environment_sha256: str
    environment_failures: Tuple[str, ...]
    adapter_file_sha256: Optional[str]               # the committed F8_THRESHOLD_ADAPTER.json (None until written)
    adapter_body_sha256: Optional[str]               # its body identity (platform-sensitive through the payload identity)
    adapter_surface_sha256: Optional[str]            # the reachable-surface identity it carries (platform-independent; must equal the live rebuild)
    adapter_platform_match: bool                     # the committed payload identity equals this machine's rebuild
    governance_sha256: Optional[str]
    package_spec_sha256: Optional[str]
    record_schema_sha256: str
    m7_declaration_sha256: str
    platform_tag: str                                # descriptive but IN the identity: records bind the platform they were produced on
    result_sha256: str = ""


_STAGE_FIELDS = tuple(f.name for f in dataclasses.fields(StageIdentity) if f.name not in ("result_sha256", "head_commit"))
def _stage_body(s) -> Tuple: return tuple(getattr(s, k) for k in _STAGE_FIELDS)
def _gov(repo_root: str, rel: str) -> str: return os.path.join(repo_root, GOVERNANCE_ROOT_REL, rel)


def platform_tag() -> str:
    return f"{platform.system()}-{platform.machine()}-py{platform.python_version()}-np{np.__version__}"


def _derive_stage(repo_root: str, pinned_root: Optional[str]) -> Dict[str, Any]:
    verify_frozen_identity()
    inst = os.path.join(repo_root, INSTRUMENT_ROOT_REL)
    if not os.path.isdir(inst): raise ApparatusHalt("instrument root not found")
    digests = []
    for rel, want in BOUND_SOURCES:
        p = os.path.join(inst, rel)
        if not os.path.isfile(p): raise ApparatusHalt(f"bound source missing: {rel}")
        b = open(p, "rb").read()
        if b"\r\n" in b: raise ApparatusHalt(f"CRLF in bound source {rel}")
        h = hashlib.sha256(b).hexdigest()
        if h != want: raise ApparatusHalt(f"placed source {rel} differs from its cleared identity")
        digests.append((rel, h))
    for rel in (RUNNER_REL, M7_TEST_REL):
        if not os.path.isfile(os.path.join(inst, rel)): raise ApparatusHalt(f"{rel} is not placed")
    runner_sha = _sha_file(os.path.join(inst, RUNNER_REL)); test_sha = _sha_file(os.path.join(inst, M7_TEST_REL))
    head = _git(repo_root, "rev-parse", "HEAD")
    if not _is_hex(head, 40): raise ApparatusHalt("HEAD is not a 40-hex object id")
    def fixed(table, what):
        out = []
        for rel, want in table:
            p = os.path.join(repo_root, rel)
            if not os.path.isfile(p): raise ApparatusHalt(f"{what} missing: {rel}")
            h = _sha_file(p)
            if h != want: raise ApparatusHalt(f"{what} {rel} differs from its cleared identity")
            out.append((rel, h))
        return tuple(out)
    gate_d = fixed(GATE_RECORDS, "authoritative gate record"); con_d = fixed(CONTRACT_RECORDS, "frozen contract record"); decl_d = fixed(_fixed_records()[len(GATE_RECORDS) + len(CONTRACT_RECORDS):], "declaration record")
    if null_decision_from_records(repo_root) != NULL_VALIDATION_DECISION_OF_RECORD: raise ApparatusHalt("the committed null-validation attempt records do not yield the decision tuple of record")
    surface = _surface_paths(repo_root)
    if _git(repo_root, "status", "--porcelain", "--", *surface): raise ApparatusHalt("the bound surface has uncommitted changes")
    commit = _git(repo_root, "log", "-1", "--format=%H", "--", *surface)
    if not _is_hex(commit, 40): raise ApparatusHalt("no commit touches the bound surface")
    for rel in [_pp.join(INSTRUMENT_ROOT_REL, r) for r, _ in BOUND_SOURCES] + [_pp.join(INSTRUMENT_ROOT_REL, RUNNER_REL), _pp.join(INSTRUMENT_ROOT_REL, M7_TEST_REL)] + [r for r, _ in _fixed_records()]:
        if not _committed_equals_working(repo_root, rel): raise ApparatusHalt(f"working file differs from the committed object: {rel}")
    def opt(rel):
        p = _gov(repo_root, rel)
        if not os.path.isfile(p): return None
        if not _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, rel)): raise ApparatusHalt(f"governance record not committed: {rel}")
        return _sha_file(p)
    placement = opt(PLACEMENT_RECORD_REL); governance = opt(GOVERNANCE_REL); spec = opt(PACKAGE_SPEC_REL); adapter_file = opt(ADAPTER_RECORD_REL)
    if placement is not None:
        try: verify_placement(repo_root, runner_sha, test_sha)
        except RunnerDomainError as e: raise ApparatusHalt(f"placement record does not verify: {e}")
    # the committed adapter record vs this machine's rebuild (M6 build_adapter): platform-independent parts must EQUAL; the payload identity match is recorded
    ad_body = ad_surface = None; ad_match = False
    if adapter_file is not None:
        try: committed = _parse_adapter_record(_gov(repo_root, ADAPTER_RECORD_REL))
        except Exception as e: raise ApparatusHalt(f"committed adapter record malformed: {type(e).__name__}: {str(e)[:100]}")
        live = _live_adapter()
        if (committed.role, committed.keys, committed.n_pass1, committed.n_pass2, committed.index_p, committed.index_t, committed.surface_sha256, committed.m3_declaration_sha256, committed.m4_declaration_sha256, committed.declaration_sha256) \
                != (live.role, live.keys, live.n_pass1, live.n_pass2, live.index_p, live.index_t, live.surface_sha256, live.m3_declaration_sha256, live.m4_declaration_sha256, live.declaration_sha256):
            raise ApparatusHalt("committed adapter record differs from M6's rebuild on the platform-independent surface")
        ad_body, ad_surface, ad_match = committed.body_sha256, committed.surface_sha256, (committed.payload_identity == live.payload_identity and committed.body_sha256 == live.body_sha256)
    gov_rec = None
    if governance is not None:
        try:
            gov_rec = _read_canonical(_gov(repo_root, GOVERNANCE_REL))
            if type(gov_rec) is not F8Governance: raise RunnerDomainError("not an F8Governance record")
            validate_governance(gov_rec, contract_digests=con_d, adapter_body_sha256=ad_body)
        except RunnerDomainError as e: raise ApparatusHalt(f"F8 governance record does not validate: {e}")
    if spec is not None:
        if gov_rec is None: raise ApparatusHalt("a Package Specification requires the committed F8 governance record")
        try:
            ps = _read_canonical(_gov(repo_root, PACKAGE_SPEC_REL))
            if type(ps) is not PackageSpecification: raise RunnerDomainError("not a PackageSpecification")
            validate_package_spec(ps, governance=gov_rec, governance_sha256=governance)
        except RunnerDomainError as e: raise ApparatusHalt(f"package specification does not validate against the governance record: {e}")
    if pinned_root and os.path.isdir(pinned_root):
        try: env = _ENV.check_environment(pinned_root)
        except Exception as e: env = None; env_fail = (f"environment check failed: {type(e).__name__}: {str(e)[:80]}",)
        if env is not None:
            conforms = bool(env.conforms and env.lock_sha256 == _ENV.EXPECTED_LOCK_SHA256 and len(env.pins) == _ENV.EXPECTED_PIN_COUNT)
            env_sha = _digest((env.python_version, env.python_implementation, env.lock_sha256, tuple(sorted((k, v[0], v[1]) for k, v in env.pins.items())), env.venv_active))
            env_fail = tuple(env.failures) + (() if env.lock_sha256 == _ENV.EXPECTED_LOCK_SHA256 else ("lock identity differs",))
        else: conforms, env_sha = False, _digest(("no environment record",))
    else:
        conforms, env_sha, env_fail = False, _digest(("no pinned root",)), ("pinned root absent: environment not qualified",)
    role = "canonical" if (conforms and placement and governance and spec and adapter_file and ad_match) else ("pre_governance" if (conforms and placement) else "noncanonical")
    return dict(role=role, commit=commit, head_commit=head, source_digests=tuple(digests), runner_sha256=runner_sha, m7_test_sha256=test_sha, placement_record_sha256=placement,
                gate_record_digests=gate_d, contract_record_digests=con_d + decl_d, ancestor_commit=ANCESTOR_COMMIT, lock_sha256=_ENV.EXPECTED_LOCK_SHA256, environment_conforms=conforms,
                environment_sha256=env_sha, environment_failures=tuple(env_fail), adapter_file_sha256=adapter_file, adapter_body_sha256=ad_body, adapter_surface_sha256=ad_surface,
                adapter_platform_match=bool(ad_match), governance_sha256=governance, package_spec_sha256=spec, record_schema_sha256=record_schema_identity(),
                m7_declaration_sha256=RUNNER_DECLARATION_SHA256_LITERAL, platform_tag=platform_tag())


_STAGE_MEMO: Dict[Tuple, Dict[str, Any]] = {}


def _fixed_records() -> List[Tuple[str, str]]:
    """Every fixed record the stage binds: gates, the frozen contract records (incl. Interpretations 001-003 and the ratification record) and the
    declaration records. No conditional membership (L2 r2 R2-4)."""
    return list(GATE_RECORDS) + list(CONTRACT_RECORDS) + list(DECLARATION_RECORDS)


def _clearance_path(repo_root: str) -> Optional[str]:
    """The L2 clearance file the committed placement record names (structural read; verified by verify_placement) — part of the surface (L2 r1 D1a)."""
    p = _gov(repo_root, PLACEMENT_RECORD_REL)
    if not os.path.isfile(p): return None
    try:
        doc = json.loads(open(p, "rb").read().decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
        cf = doc["fields"]["l2_clearance_file"] if doc.get("__type__") == "M7PlacementRecord" else None
        return cf if isinstance(cf, str) and cf.startswith(CLEARANCE_DIR_REL + "/") and ".." not in cf else None
    except Exception: return None


def _surface_paths(repo_root: Optional[str] = None) -> List[str]:
    paths = [_pp.join(INSTRUMENT_ROOT_REL, r) for r, _ in BOUND_SOURCES] + [_pp.join(INSTRUMENT_ROOT_REL, RUNNER_REL), _pp.join(INSTRUMENT_ROOT_REL, M7_TEST_REL)] \
            + [_pp.join(GOVERNANCE_ROOT_REL, g) for g in (PLACEMENT_RECORD_REL, SUITE_RECORD_REL, GOVERNANCE_REL, PACKAGE_SPEC_REL, ADAPTER_RECORD_REL)] + [r for r, _ in _fixed_records()]
    cf = _clearance_path(repo_root) if repo_root else None
    return paths + ([cf] if cf else [])


def _environment_probe(pinned_root: Optional[str]) -> Tuple:
    """Every environment fact the stage derivation reads, freshly observed (L2 r1 D1a): the pinned root's existence, the check's outcome."""
    if not (pinned_root and os.path.isdir(pinned_root)): return ("no pinned root",)
    try: env = _ENV.check_environment(pinned_root)
    except Exception as e: return ("environment check failed", type(e).__name__, str(e)[:80])
    return (env.conforms, env.python_version, env.python_implementation, env.lock_sha256, tuple(sorted((k, v[0], v[1]) for k, v in env.pins.items())), env.venv_active, tuple(env.failures))


def _derive_stage_memoized(repo_root: str, pinned_root: Optional[str]) -> Dict[str, Any]:
    """CONTENT-ADDRESSED MEMO (disclosed, E1 M7's discipline): the key is every byte the derivation reads — HEAD, the porcelain status of the
    whole bound surface (including the clearance file the placement record names), the digest of every surface file present on disk, a fresh
    environment probe of the pinned root (existence, lock identity, pins), frozen code and platform. A hit returns the same derivation the full
    procedure produced on those bytes; any change to any input misses (L2 r1 D1a)."""
    sp = _surface_paths(repo_root)
    head = _git(repo_root, "rev-parse", "HEAD"); status = _git(repo_root, "status", "--porcelain", "--", *sp)
    files = tuple((p, _sha_file(os.path.join(repo_root, p))) for p in sp if os.path.isfile(os.path.join(repo_root, p)))
    key = (os.path.abspath(repo_root), pinned_root and os.path.abspath(pinned_root), _environment_probe(pinned_root), head, status, files, _frozen_code_key(), platform_tag())
    if key not in _STAGE_MEMO: _STAGE_MEMO[key] = _derive_stage(repo_root, pinned_root)
    return _STAGE_MEMO[key]


def bind_stage(repo_root: str, pinned_root: Optional[str] = None) -> StageIdentity:
    f = _derive_stage_memoized(repo_root, pinned_root)
    return StageIdentity(**f, result_sha256=_digest(_stage_body(StageIdentity(**f))))


def validate_stage_identity(s, repo_root: str, pinned_root: Optional[str] = None) -> None:
    if type(s) is not StageIdentity or s.role not in STAGE_ROLES: raise RunnerDomainError("exact StageIdentity with a known role required")
    f = _derive_stage_memoized(repo_root, pinned_root)
    for k, v in f.items():
        if k == "head_commit": continue
        if getattr(s, k) != v: raise RunnerDomainError(f"stage field {k} does not re-derive from the repository")
    if s.result_sha256 != _digest(_stage_body(s)): raise RunnerDomainError("stage identity does not recompute")


def _parse_adapter_record(path: str):
    """Structural parse of a committed F8ThresholdAdapter document (ASCII canonical bytes; self-consistent identity). M6's own replaying loader
    is applied only where the platform matches (`_stage_adapter`); on another platform the payload identity cannot replay and the document is
    compared field by field instead."""
    raw = open(path, "rb").read(); raw.decode("ascii")
    doc = json.loads(raw.decode("ascii"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
    if _canon(doc).encode() != raw or doc.get("__type__") != "F8ThresholdAdapter" or set(doc) != {"__type__", "sha256", "body"}: raise RunnerDomainError("adapter record is not a canonical F8ThresholdAdapter document")
    b = doc["body"]
    a = _A.ThresholdAdapter(b["role"], tuple(int(x) for x in b["keys"]), int(b["n_pass1"]), int(b["n_pass2"]), float(b["theta_p"]), float(b["theta_t"]), int(b["index_p"]), int(b["index_t"]),
                            b["payload_identity"], b["surface_sha256"], b["m3_declaration_sha256"], b["m4_declaration_sha256"], b["declaration_sha256"], doc["sha256"])
    if a.body_sha256 != a.identity() or a.role != "production": raise RunnerDomainError("adapter record identity does not recompute or role is not production")
    return a


def write_adapter_record(repo_root: str) -> str:
    """Write M6's production adapter as built on THIS machine to the governance directory as ASCII canonical bytes (the identity M7
    binds; written once on the canonical machine, committed, never regenerated elsewhere). Returns the file identity."""
    a = _A.build_adapter("production"); text = _A.adapter_to_json(a)
    text.encode("ascii")
    p = _gov(repo_root, ADAPTER_RECORD_REL); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", newline="\n", encoding="ascii") as f: f.write(text)
    return _sha_file(p)


# ----------------------------------------------------------------------------- placement, suite, governance records
@dataclass(frozen=True)
class M7SuiteRecord:
    invocation: str
    passed: int
    skipped: int
    failed: int
    runner_sha256: str
    m7_test_sha256: str
    tested_commit: str
    result_sha256: str = ""


def validate_suite_record(s, **ctx) -> None:
    if type(s) is not M7SuiteRecord or not isinstance(s.invocation, str) or "pytest" not in s.invocation or " tests" not in s.invocation: raise RunnerDomainError("suite record must name the complete canonical pytest invocation over tests")
    if any(type(x) is not int or x < 0 for x in (s.passed, s.skipped, s.failed)) or s.passed < 1 or s.failed != 0: raise RunnerDomainError("suite record must report a passing suite with zero failures")
    if not (_is_hex(s.runner_sha256, 64) and _is_hex(s.m7_test_sha256, 64) and _is_hex(s.tested_commit, 40)): raise RunnerDomainError("suite record identities malformed")
    if s.result_sha256 != _digest((s.invocation, s.passed, s.skipped, s.failed, s.runner_sha256, s.m7_test_sha256, s.tested_commit)): raise RunnerDomainError("suite record identity does not recompute")


@dataclass(frozen=True)
class M7PlacementRecord:
    runner_sha256: str
    m7_test_sha256: str
    l2_clearance_file: str
    l2_clearance_sha256: str
    placement_commit: str
    suite_record_sha256: str
    result_sha256: str = ""


def validate_placement_record(pr, runner_sha: Optional[str] = None, test_sha: Optional[str] = None, **ctx) -> None:
    if type(pr) is not M7PlacementRecord or not all(_is_hex(x, 64) for x in (pr.runner_sha256, pr.m7_test_sha256, pr.l2_clearance_sha256, pr.suite_record_sha256)) or not _is_hex(pr.placement_commit, 40):
        raise RunnerDomainError("placement record malformed")
    if not isinstance(pr.l2_clearance_file, str) or not pr.l2_clearance_file.startswith(CLEARANCE_DIR_REL + "/") or ".." in pr.l2_clearance_file: raise RunnerDomainError("clearance file must lie under build_records")
    if runner_sha is not None and (pr.runner_sha256, pr.m7_test_sha256) != (runner_sha, test_sha): raise RunnerDomainError("placed runner/test differ from the M7 placement record")
    if pr.result_sha256 != _digest((pr.runner_sha256, pr.m7_test_sha256, pr.l2_clearance_file, pr.l2_clearance_sha256, pr.placement_commit, pr.suite_record_sha256)): raise RunnerDomainError("placement record identity does not recompute")


def _current_dispositions(txt: str) -> List[str]:
    """The CURRENT disposition lines of an L2 document (L2 r2 R2-3): lines at column 0 that mention FINAL VERDICT, taken OUTSIDE fenced code
    (``` or ~~~ fences at any indent), indented code (four spaces or a tab) and block quotes (>). A line mentioning FINAL VERDICT in any
    other form than the exact canonical line is returned as-is, so the caller fails closed on malformed or conflicting dispositions."""
    out: List[str] = []; fence: Optional[Tuple[str, int]] = None            # (fence character, opening length) — CommonMark 0.31 s4.5 (L2 r3 R3-2, r4)
    for raw in txt.splitlines():
        ln = raw.rstrip("\r")
        indent = len(ln) - len(ln.lstrip(" ")); st = ln.lstrip()
        indented_code = ln.startswith("\t") or indent >= 4                     # four or more spaces (or a tab) is INDENTED CODE, never a fence (CommonMark s4.4/s4.5; L2 r4)
        if fence is None:
            if not indented_code and (st.startswith("```") or st.startswith("~~~")):
                ch = st[0]; n = len(st) - len(st.lstrip(ch)); fence = (ch, n); continue   # an opener indented 0-3 spaces
        else:
            if not indented_code:
                ch, n = fence; m = len(st) - len(st.lstrip(ch))
                if st.startswith(ch) and m >= n and st[m:].strip() == "": fence = None   # a closer: same character, indented 0-3, at least as long, nothing but whitespace after
            continue
        if indented_code or st.startswith(">"): continue                          # indented code or block quote: quoted material
        if "FINAL VERDICT" in ln: out.append(ln if ln == "FINAL VERDICT: SOUND" else f"malformed/non-current: {ln.strip()[:60]}")
    return out


def verify_placement(repo_root: str, runner_sha: str, test_sha: str) -> M7PlacementRecord:
    pr = _read_canonical(_gov(repo_root, PLACEMENT_RECORD_REL))
    if type(pr) is not M7PlacementRecord: raise RunnerDomainError("not an M7PlacementRecord")
    validate_placement_record(pr, runner_sha, test_sha)
    placed = _git(repo_root, "log", "-1", "--format=%H", "--", _pp.join(INSTRUMENT_ROOT_REL, RUNNER_REL), _pp.join(INSTRUMENT_ROOT_REL, M7_TEST_REL))
    if placed != pr.placement_commit: raise RunnerDomainError("placement commit is not the last commit that touched runner.py and test_f8_m7.py")
    cf = os.path.join(repo_root, pr.l2_clearance_file)
    if not os.path.isfile(cf) or not _committed_equals_working(repo_root, pr.l2_clearance_file) or _sha_file(cf) != pr.l2_clearance_sha256: raise RunnerDomainError("L2 clearance file absent, uncommitted, or not the named identity")
    txt = open(cf, "rb").read().decode("utf-8", "replace")
    if runner_sha not in txt or test_sha not in txt: raise RunnerDomainError("L2 clearance file does not name both cleared M7 identities")
    disp = _current_dispositions(txt)
    if disp != ["FINAL VERDICT: SOUND"]: raise RunnerDomainError(f"L2 clearance file must carry exactly one current final-disposition line reading 'FINAL VERDICT: SOUND' outside quoted or code material; found {disp} (E1 M7 marker; L2 r1 D8, r2 R2-3)")
    sp = _gov(repo_root, SUITE_RECORD_REL)
    if not os.path.isfile(sp) or not _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, SUITE_RECORD_REL)) or _sha_file(sp) != pr.suite_record_sha256: raise RunnerDomainError("suite record absent, uncommitted, or not the named identity")
    sr = _read_canonical(sp)
    if type(sr) is not M7SuiteRecord: raise RunnerDomainError("suite record is not an M7SuiteRecord")
    validate_suite_record(sr)
    if (sr.runner_sha256, sr.m7_test_sha256, sr.tested_commit) != (runner_sha, test_sha, pr.placement_commit): raise RunnerDomainError("suite record names different files or a different commit")
    return pr


@dataclass(frozen=True)
class F8Governance:
    """Machine-readable governance record for F8 stage 1 (Mike's values; M7 enforces the grammar and holds no scientific value).
    Carries every identity the ratification record §E says M7 must carry."""
    version: int
    claim_tier: str
    flight_name: str
    contract_sha256: str
    freeze_record_sha256: str
    appendix_a_sha256: str
    interpretation_001_sha256: str
    interpretation_002_sha256: str
    ratification_record_sha256: str
    interpretation_003_sha256: str                   # ratified 2026-11-03 (6ebf0ad3…), bound by M7 (R2-4)
    generator_declaration_markdown_sha256: str       # F8_M6_GENERATOR_DECLARATION_v0_3.md (or the ratified successor)
    generator_declaration_digest: str                # M6 GENERATOR_DECLARATION tuple digest
    audit_declaration_digest: str
    evaluator_declaration_digest: str
    closure_declaration_digest: str
    null_declaration_digest: str
    verdict_declaration_digest: str
    classify_declaration_digest: str
    config_declaration_digest: str
    null_validation_protocol_sha256: str             # attempt-2 protocol identity (travels with its decision)
    null_validation_decision: Tuple[Tuple[str, object], ...]   # TYPED: must EQUAL NULL_VALIDATION_DECISION_OF_RECORD (derived from the committed attempt records at bind)
    placement_date: int                              # M6's placement date (masters 6/7/8)
    stability_master: int                            # M1's F8_STABILITY_MASTER (Interpretation 003 pt 6; the M1 touch placed with M7)
    stability_seed_panel_sha256: str                 # M1's F8_STABILITY_PANEL_SHA256_LITERAL
    masters: Tuple[Tuple[str, int], ...]             # every declared master by role
    adapter_body_sha256: str                         # the committed adapter record's body identity (canonical machine)
    package_item_vocabulary: Tuple[str, ...]
    required_package_items: Tuple[str, ...]
    production_prerequisites: Tuple[Tuple[str, str, str], ...]
    branch_stopping: Tuple[Tuple[str, str], ...]
    record_kind_mapping: Tuple[Tuple[str, str], ...]  # (E1-R record kind, F8 record type) — M5-5
    result_sha256: str = ""


_GOV_FIELDS = tuple(f.name for f in dataclasses.fields(F8Governance) if f.name != "result_sha256")
def _gov_body(g) -> Tuple: return tuple(getattr(g, k) for k in _GOV_FIELDS)

EXPECTED_MASTER_ROLES = ("seed_panel", "calibration", "null_validation_attempt1", "null_validation_attempt2", "projection", "known_answer", "m6_design", "m6_held_out", "m6_pricing")


def validate_governance(g, contract_digests: Optional[Tuple[Tuple[str, str], ...]] = None, adapter_body_sha256: Optional[str] = None, **ctx) -> None:
    """Grammar and binding: typed, closed alphabets; the frozen identities EQUAL the literals the stage binds; the declaration digests
    EQUAL the placed modules'; the masters EQUAL the placed modules' derivations; the adapter body equals the committed record's."""
    if type(g) is not F8Governance or type(g.version) is not int or g.version < 1: raise RunnerDomainError("governance record malformed")
    if not (isinstance(g.claim_tier, str) and g.claim_tier and isinstance(g.flight_name, str) and g.flight_name): raise RunnerDomainError("governance claim tier and flight name required")
    ids = (g.contract_sha256, g.freeze_record_sha256, g.appendix_a_sha256, g.interpretation_001_sha256, g.interpretation_002_sha256, g.ratification_record_sha256, g.interpretation_003_sha256,
           g.generator_declaration_markdown_sha256, g.generator_declaration_digest, g.audit_declaration_digest, g.evaluator_declaration_digest, g.closure_declaration_digest,
           g.null_declaration_digest, g.verdict_declaration_digest, g.classify_declaration_digest, g.config_declaration_digest, g.null_validation_protocol_sha256, g.adapter_body_sha256)
    if any(not _is_hex(x, 64) for x in ids): raise RunnerDomainError("governance identities must be sha256 hex")
    want = dict(CONTRACT_RECORDS)
    if (g.contract_sha256, g.freeze_record_sha256, g.appendix_a_sha256, g.interpretation_001_sha256, g.interpretation_002_sha256, g.ratification_record_sha256, g.interpretation_003_sha256) != tuple(want[r] for r, _ in CONTRACT_RECORDS):
        raise RunnerDomainError("governance contract identities differ from the frozen contract records M7 binds (incl. Interpretation 003 as ratified)")
    if contract_digests is not None and tuple(h for _, h in contract_digests)[:len(CONTRACT_RECORDS)] != tuple(h for _, h in CONTRACT_RECORDS): raise RunnerDomainError("stage contract digests differ from the declaration")
    if g.generator_declaration_markdown_sha256 != GENERATOR_DECLARATION_MARKDOWN_SHA256: raise RunnerDomainError("governance generator declaration Markdown identity is not the approved declaration M7 binds (L2 r1 D7)")
    if (g.generator_declaration_digest, g.audit_declaration_digest, g.evaluator_declaration_digest, g.closure_declaration_digest, g.null_declaration_digest, g.verdict_declaration_digest, g.classify_declaration_digest, g.config_declaration_digest) \
            != (_A.GENERATOR_DECLARATION_SHA256_LITERAL, _A.AUDIT_DECLARATION_SHA256_LITERAL, _E.EVALUATOR_SHA256_LITERAL, _CL.CLOSURE_SHA256_LITERAL, _N.NULL_SHA256_LITERAL, _V.VERDICT_DECLARATION_SHA256_LITERAL, _K.CLASSIFY_SHA256_LITERAL, _C.F8_DECLARATION_SHA256_LITERAL):
        raise RunnerDomainError("governance declaration digests differ from the placed modules")
    if g.null_validation_protocol_sha256 != _N.VALIDATION_PROTOCOL_ATTEMPT_2_SHA256_LITERAL or g.null_validation_decision != NULL_VALIDATION_DECISION_OF_RECORD:
        raise RunnerDomainError("null-validation protocol identity or its typed decision of record differs (attempt 2 PASSED under the ratified protocol; module-default alpha 0.05 FAILS, disclosed; attempt 1 FAILED, retained)")
    if g.stability_master != stability_master() or g.stability_seed_panel_sha256 != _C.F8_STABILITY_PANEL_SHA256_LITERAL:
        raise RunnerDomainError("governance stability master / panel identity differ from M7's derivation (Interpretation 003 pt 6)")
    if type(g.placement_date) is not int or g.placement_date != _A.PLACEMENT_DATE: raise RunnerDomainError("governance placement date differs from the placed M6 literal")
    m = dict(g.masters)
    if tuple(r for r, _ in g.masters) != EXPECTED_MASTER_ROLES or len(m) != len(g.masters): raise RunnerDomainError("governance masters must name exactly the declared roles in order")
    want_m = {"seed_panel": _C.F8_SEED_PANEL_MASTER, "calibration": _C.F8_CALIBRATION_MASTER, "null_validation_attempt1": _N.VALIDATION_REPLICATE_MASTER,
              "null_validation_attempt2": _N.VALIDATION_PROTOCOL_ATTEMPT_2.replicate_master, "projection": _CL.PROJECTION_MASTER, "known_answer": _E.KNOWN_ANSWER_MASTER}
    want_m.update(zip(("m6_design", "m6_held_out", "m6_pricing"), _A.production_masters()))
    if m != want_m: raise RunnerDomainError("governance masters differ from the placed modules' derivations")
    if adapter_body_sha256 is not None and g.adapter_body_sha256 != adapter_body_sha256: raise RunnerDomainError("governance adapter identity differs from the committed adapter record")
    for name, tup in (("vocabulary", g.package_item_vocabulary), ("required items", g.required_package_items)):
        if type(tup) is not tuple or any(not isinstance(x, str) or not x for x in tup) or len(set(tup)) != len(tup): raise RunnerDomainError(f"governance {name} must be a tuple of unique names")
    if not g.package_item_vocabulary or not set(g.required_package_items) <= set(g.package_item_vocabulary): raise RunnerDomainError("required package items must lie in the vocabulary")
    pr = g.production_prerequisites
    if type(pr) is not tuple or any(type(e) is not tuple or len(e) != 3 or e[0] not in PREREQ_VOCAB or e[1] not in PREREQ_KINDS or e[2] not in PREREQ_REQUIREMENTS for e in pr): raise RunnerDomainError("production prerequisites must be (name, kind, requirement) triples in the declared alphabets")
    if len({e[0] for e in pr}) != len(pr): raise RunnerDomainError("production prerequisite names must be unique")
    for name, req in MANDATORY_PREREQUISITES:
        if not any(e[0] == name and e[2] == req for e in pr): raise RunnerDomainError(f"contract s7.1/s3.4/s7.3: {name} {req} is a mandatory production prerequisite (L2 r1 D3a)")
    bs = g.branch_stopping
    if type(bs) is not tuple or any(type(e) is not tuple or len(e) != 2 or e[0] not in {p[0] for p in pr} or e[1] not in PREDICATE_IDS for e in bs): raise RunnerDomainError("branch-stopping entries must name a production prerequisite and a declared predicate")
    rk = g.record_kind_mapping
    if type(rk) is not tuple or dict(rk).get("tolerance_ensembles") != "ToleranceEnsemble" or dict(rk).get("tolerance_program") != "ToleranceProgram": raise RunnerDomainError("record-kind mapping must carry M5-5 as ratified")
    if g.result_sha256 != _digest(_gov_body(g)): raise RunnerDomainError("governance identity does not recompute")


def load_governance(repo_root: str, stage) -> Tuple[F8Governance, str]:
    p = _gov(repo_root, GOVERNANCE_REL)
    if stage.governance_sha256 is None or not os.path.isfile(p) or _sha_file(p) != stage.governance_sha256: raise RunnerDomainError("no committed F8 governance record is bound by this stage")
    g = _read_canonical(p)
    if type(g) is not F8Governance: raise RunnerDomainError("file is not an F8Governance record")
    validate_governance(g, contract_digests=stage.contract_record_digests, adapter_body_sha256=stage.adapter_body_sha256)
    return g, stage.governance_sha256


def _require_committed(repo_root: str, path: str) -> None:
    rel = os.path.relpath(os.path.abspath(path), os.path.abspath(repo_root)).replace(os.sep, "/")
    if rel.startswith("..") or not _committed_equals_working(repo_root, rel): raise RunnerDomainError(f"{rel} is not committed (equal to its git object)")


def _is_alias(parent: str, name: str) -> bool:
    """True if `name` under `parent` is any kind of alias — a symbolic link on any platform, or a Windows junction / reparse point — detected
    as a resolution step AT THIS COMPONENT: realpath(parent/name) must equal realpath(parent)/name. Aliases above `parent` do not matter."""
    p = os.path.join(parent, name)
    return os.path.islink(p) or os.path.normcase(os.path.realpath(p)) != os.path.normcase(os.path.join(os.path.realpath(parent), name))


def _walk_no_links(root: str):
    """os.walk over `root` that REFUSES any alias (symbolic link, junction, reparse point; directory or file) anywhere under it (L2 r3 R3-1):
    the digests key what the validators read, and an alias would let a validator read bytes the digest never saw. Yields (dirpath, filename)."""
    if os.path.islink(root): raise RunnerDomainError(f"{root} is a link: artifact and record trees must be real directories")
    for dp, dns, fs in os.walk(root):
        for d in dns:
            if _is_alias(dp, d): raise RunnerDomainError(f"{os.path.join(dp, d)} is a directory link or junction: refused before any cached derivation")
        for f in fs:
            if _is_alias(dp, f): raise RunnerDomainError(f"{os.path.join(dp, f)} is a file link: refused before any cached derivation")
            yield dp, f


def _real_file(path: str) -> str:
    """A path a validator reads must be a regular file with no link or junction in any component below the filesystem root (R3-1)."""
    ap = os.path.abspath(path); parent, name = os.path.split(ap); chain = []
    while name:
        chain.append((parent, name)); parent, name = os.path.split(parent)
    for par, nm in reversed(chain):
        if _is_alias(par, nm): raise RunnerDomainError(f"{os.path.join(par, nm)} is a link or junction: refused")
    if not os.path.isfile(path): raise RunnerDomainError(f"{path} is not a regular file")
    return path


def _tree_digest(root: str) -> str:
    acc = []
    for dp, f in _walk_no_links(root):
        fp = os.path.join(dp, f); acc.append((os.path.relpath(fp, root).replace(os.sep, "/"), _sha_file(fp)))
    return _digest(tuple(sorted(acc)))


def _readiness_surface_digest(repo_root: str, base: str) -> str:
    """What a readiness derivation may read under the prerequisites tree BESIDES the manifest-named files (those are keyed by
    `_manifest_files_digest`): job 0's level records and artifacts (every file naming the calibration panel — the canonical census
    replays them) and the benchmark artifacts (the ResourceBenchmark replay reads them), each with its bytes and committed state. Outputs
    of the scientific jobs written into the same tree cannot be read by readiness and do not key it (round 3: the whole-tracked-tree digest
    of round 2 grew with every committed census and is replaced by this exact read set)."""
    clean = _clean_tracked_set(repo_root, base); acc = []
    for dp, f in _walk_no_links(base):
        fp = os.path.join(dp, f); r = os.path.relpath(fp, repo_root).replace(os.sep, "/")
        if ".calibration" in r or "/benchmark_artifacts/" in r or r.endswith("calibration_tranche.json"): acc.append((r, _sha_file(fp), r in clean))
    return _digest(tuple(sorted(acc)))


def _authorization_surface_digest(repo_root: str) -> str:
    """Every authority input a readiness derivation reads (L2 r1 D1b): each AUTHORIZATION_*.json and the registry — working-tree content,
    whether it equals its committed object, and the FULL commit history of the file (the one-commit-per-version rule reads history)."""
    gdir = _gov(repo_root, ""); acc = []
    names = sorted(f for f in os.listdir(gdir) if f.startswith(AUTHORIZATION_GLOB) or f == AUTHORIZATION_REGISTRY_REL) if os.path.isdir(gdir) else []
    for n in names:
        rel = _pp.join(GOVERNANCE_ROOT_REL, n)
        acc.append((n, _sha_file(os.path.join(gdir, n)), _committed_equals_working(repo_root, rel), tuple(_git(repo_root, "log", "--format=%H", "--", rel).splitlines())))
    return _digest((tuple(acc), _git(repo_root, "rev-parse", "HEAD")))


_READINESS_MEMO: Dict[Tuple, Any] = {}
_ARTIFACT_REPLAY_MEMO: Dict[Tuple, bool] = {}
_LIVE_ADAPTER_MEMO: Dict[Tuple, Any] = {}


_PRODUCTION_ADAPTER_MEMO: Dict[Tuple, bool] = {}


def _is_production_adapter(a) -> bool:
    """M6's `is_production_adapter` (a full replay through `build_adapter`), memoised on the adapter's content identity and the frozen code key:
    the adapter is immutable content, so the replay's verdict is a pure function of (content, frozen code, this platform)."""
    if type(a) is not _A.ThresholdAdapter: return False
    key = (a.identity(), a.body_sha256, _frozen_code_key(), platform_tag())     # the stored checksum is content too (L2 r1 D1c)
    if key not in _PRODUCTION_ADAPTER_MEMO: _PRODUCTION_ADAPTER_MEMO[key] = _A.is_production_adapter(a)
    return _PRODUCTION_ADAPTER_MEMO[key]


def _live_adapter():
    """M6's production adapter rebuilt on this machine — a pure function of frozen code and this platform's libm; memoised on the frozen code key."""
    key = _frozen_code_key()
    if key not in _LIVE_ADAPTER_MEMO: _LIVE_ADAPTER_MEMO[key] = _A.build_adapter("production")
    return _LIVE_ADAPTER_MEMO[key]


def _frozen_code_key() -> Tuple[str, ...]:
    return (_A.AUDIT_DECLARATION_SHA256_LITERAL, _A.GENERATOR_DECLARATION_SHA256_LITERAL, _V.VERDICT_DECLARATION_SHA256_LITERAL, _N.NULL_SHA256_LITERAL,
            _C.F8_DECLARATION_SHA256_LITERAL, _K.CLASSIFY_SHA256_LITERAL, _CL.CLOSURE_SHA256_LITERAL, _E.EVALUATOR_SHA256_LITERAL, RUNNER_DECLARATION_SHA256_LITERAL)


# ----------------------------------------------------------------------------- authorization records (E1 M7, carried; F8 tranche panel)
@dataclass(frozen=True)
class AuthorizationRecord:
    version: int
    issued: str
    issuer: str
    stage_sha256: str
    governance_sha256: str
    package_spec_sha256: str
    authorized_jobs: Tuple[str, ...]
    tranche_authorized: bool
    tranche_levels_micro: Tuple[int, ...]
    tranche_seeds: Tuple[int, ...]
    production_authorized: bool
    prerequisite_manifest_sha256: str
    result_sha256: str = ""

    def __post_init__(self) -> None: _validate_authorization_structure(self)


def _validate_authorization_structure(a) -> None:
    if type(a.version) is not int or a.version < 1 or not isinstance(a.issued, str) or not a.issued or not isinstance(a.issuer, str) or not a.issuer: raise RunnerDomainError("authorization version/issued/issuer malformed")
    if type(a.authorized_jobs) is not tuple or any(j not in CANONICAL_JOBS for j in a.authorized_jobs) or len(set(a.authorized_jobs)) != len(a.authorized_jobs): raise RunnerDomainError("authorized jobs malformed")
    if type(a.tranche_authorized) is not bool or type(a.production_authorized) is not bool: raise RunnerDomainError("authorization flags must be exact bools")
    if a.tranche_authorized:
        if len(a.tranche_levels_micro) != TRANCHE_LEVELS or len(a.tranche_seeds) != TRANCHE_SEEDS or any(m not in F8_LEVELS_MICRO for m in a.tranche_levels_micro) or any(s not in F8_SEED_PANEL for s in a.tranche_seeds) \
                or len(set(a.tranche_levels_micro)) != TRANCHE_LEVELS or len(set(a.tranche_seeds)) != TRANCHE_SEEDS:
            raise RunnerDomainError("tranche panel must be exactly the declared count of distinct frozen levels and canonical seeds")
    if a.production_authorized != _is_hex(a.prerequisite_manifest_sha256, 64) or (not a.production_authorized and a.prerequisite_manifest_sha256 != ""):
        raise RunnerDomainError("production authorization requires exactly one committed prerequisite-manifest identity (and none otherwise)")


_AUTH_FIELDS = tuple(f.name for f in dataclasses.fields(AuthorizationRecord) if f.name != "result_sha256")
def _auth_body(a) -> Tuple: return tuple(getattr(a, k) for k in _AUTH_FIELDS)


def validate_authorization(a, stage: StageIdentity) -> None:
    if type(a) is not AuthorizationRecord: raise RunnerDomainError("exact AuthorizationRecord required")
    _validate_authorization_structure(a)
    if type(stage) is not StageIdentity or stage.role != "canonical": raise RunnerDomainError("authorization requires a CANONICAL bound stage")
    if a.stage_sha256 != stage.result_sha256: raise RunnerDomainError("authorization names a different stage")
    if (a.governance_sha256, a.package_spec_sha256) != (stage.governance_sha256, stage.package_spec_sha256): raise RunnerDomainError("authorization governance/package-spec identities differ from the stage")
    if a.result_sha256 != _digest(_auth_body(a)): raise RunnerDomainError("authorization identity does not recompute")


@dataclass(frozen=True)
class AuthorizationRegistry:
    entries: Tuple[Tuple[int, str], ...]
    result_sha256: str = ""


def validate_registry(r, **ctx) -> None:
    if type(r) is not AuthorizationRegistry or type(r.entries) is not tuple or not r.entries: raise RunnerDomainError("authorization registry malformed or empty")
    vs = [e[0] for e in r.entries]
    if any(type(e) is not tuple or len(e) != 2 or type(e[0]) is not int or not _is_hex(e[1], 64) for e in r.entries) or vs != sorted(vs) or len(set(vs)) != len(vs) or vs[0] < 1: raise RunnerDomainError("registry entries must be strictly increasing versions with sha256 file identities")
    if r.result_sha256 != _digest(r.entries): raise RunnerDomainError("registry identity does not recompute")


def verify_registry_history(repo_root: str) -> None:
    rel = _pp.join(GOVERNANCE_ROOT_REL, AUTHORIZATION_REGISTRY_REL)
    revs = _git(repo_root, "log", "--reverse", "--format=%H", "--", rel).splitlines(); prev: Tuple = ()
    for h in revs:
        blob = subprocess.run(["git", "-C", repo_root, "show", f"{h}:{rel}"], capture_output=True)
        if blob.returncode != 0: continue
        doc = json.loads(blob.stdout.decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const); reg = _decode(doc)
        if type(reg) is not AuthorizationRegistry: raise RunnerDomainError(f"registry revision {h[:10]} is not an AuthorizationRegistry")
        if reg.entries[:len(prev)] != prev: raise RunnerDomainError(f"registry revision {h[:10]} alters existing entries (registry is append-only)")
        prev = reg.entries


def load_authorization(repo_root: str, stage: StageIdentity, version: int) -> Tuple[AuthorizationRecord, str]:
    if isinstance(version, bool) or not isinstance(version, int) or version < 1: raise RunnerDomainError("authorization version must be an exact positive non-Boolean integer")
    v = version; rel = f"{AUTHORIZATION_GLOB}{v:03d}.json"; p = _gov(repo_root, rel); rp = _gov(repo_root, AUTHORIZATION_REGISTRY_REL)
    for path, name in ((p, rel), (rp, AUTHORIZATION_REGISTRY_REL)):
        if not os.path.isfile(path): raise RunnerDomainError(f"{name} does not exist")
        if not _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, name)): raise RunnerDomainError(f"{name} is not committed")
    reg = _read_canonical(rp)
    if type(reg) is not AuthorizationRegistry: raise RunnerDomainError("registry file is not an AuthorizationRegistry")
    validate_registry(reg)
    verify_registry_history(repo_root)
    fsha = _sha_file(p)
    if (v, fsha) not in reg.entries: raise RunnerDomainError(f"authorization v{v} at {fsha[:12]} is not listed in the ratified registry")
    hist = _git(repo_root, "log", "--format=%H", "--", _pp.join(GOVERNANCE_ROOT_REL, rel)).splitlines()
    if len(hist) != 1: raise RunnerDomainError(f"authorization v{v} has {len(hist)} commits in its history: versions are append-only and immutable")
    a = _read_canonical(p)
    if type(a) is not AuthorizationRecord or a.version != v: raise RunnerDomainError("file is not the AuthorizationRecord of that version")
    validate_authorization(a, stage)
    return a, fsha


def require_authorized(stage: StageIdentity, repo_root: str, pinned_root: Optional[str], version: int, job: str) -> Tuple[AuthorizationRecord, str]:
    if job not in CANONICAL_JOBS: raise RunnerDomainError(f"{job!r} is not a declared canonical job")
    validate_stage_identity(stage, repo_root, pinned_root)
    if stage.role != "canonical": raise RunnerDomainError(f"canonical act requires a canonical stage; bound stage is {stage.role}: {stage.environment_failures[:2]}")
    a, fsha = load_authorization(repo_root, stage, version)
    if job not in a.authorized_jobs: raise RunnerDomainError(f"job {job} is not authorized by record v{a.version} (source literals grant nothing)")
    return a, fsha


# ----------------------------------------------------------------------------- 2. persisted records (canonical bytes; validators on write and load) — E1 M7, carried
def _encode(obj):
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        name = type(obj).__name__
        if name not in RECORD_TYPES: raise RunnerDomainError(f"record type {name} is not registered")
        return {"__type__": name, "fields": {f.name: _encode(getattr(obj, f.name)) for f in dataclasses.fields(obj)}}
    if isinstance(obj, (tuple, list)): return [_encode(x) for x in obj]
    if isinstance(obj, float) and not np.isfinite(obj): raise RunnerDomainError("nonfinite floats cannot be persisted")
    if obj is None or isinstance(obj, (bool, int, float, str)): return obj
    raise RunnerDomainError(f"unpersistable value of type {type(obj).__name__}")


def _decode(x):
    if isinstance(x, dict):
        if set(x) != {"__type__", "fields"} or x["__type__"] not in RECORD_TYPES: raise RunnerDomainError("malformed persisted record object")
        cls = RECORD_TYPES[x["__type__"]]; fields = {f.name for f in dataclasses.fields(cls)}
        if set(x["fields"]) != fields: raise RunnerDomainError(f"persisted {cls.__name__} fields differ from the frozen schema")
        return cls(**{k: _decode(v) for k, v in x["fields"].items()})
    if isinstance(x, list): return tuple(_decode(v) for v in x)
    if isinstance(x, float) and not np.isfinite(x): raise RunnerDomainError("nonfinite constant in persisted record")
    return x


ENVELOPE_KEYS = {"type", "record_schema_sha256", "stage_sha256", "authorization_sha256", "authorization_file_sha256", "authorization_version", "job", "record"}


def _envelope(obj, stage: StageIdentity, auth_sha, auth_file, auth_ver, job) -> Dict[str, Any]:
    return {"type": type(obj).__name__, "record_schema_sha256": record_schema_identity(), "stage_sha256": stage.result_sha256, "authorization_sha256": auth_sha,
            "authorization_file_sha256": auth_file, "authorization_version": auth_ver, "job": job, "record": _encode(obj)}


def _write(obj, path, stage, env) -> str:
    text = _canon(env)
    with open(path, "w", newline="\n", encoding="utf-8") as f: f.write(text)
    return hashlib.sha256(text.encode()).hexdigest()


def persist_record(obj, path: str, stage: StageIdentity, repo_root: str, pinned_root: Optional[str] = None, **ctx) -> str:
    validate_stage_identity(stage, repo_root, pinned_root)
    typ = type(obj).__name__
    if typ not in VALIDATORS: raise RunnerDomainError(f"no validator registered for {typ}")
    VALIDATORS[typ](obj, stage=stage, repo_root=repo_root, pinned_root=pinned_root, **ctx)
    return _write(obj, path, stage, _envelope(obj, stage, None, None, None, None))


def _persist_canonical(obj, path, stage, repo_root, pinned_root, auth: AuthorizationRecord, auth_file: str, job: str, **ctx) -> str:
    typ = type(obj).__name__
    VALIDATORS[typ](obj, stage=stage, repo_root=repo_root, pinned_root=pinned_root, **ctx)
    return _write(obj, path, stage, _envelope(obj, stage, auth.result_sha256, auth_file, auth.version, job))


GOVERNANCE_JOBS = ("production", "calibration_tranche")


def load_record(path: str, expected_type: str, stage: StageIdentity, repo_root: str, pinned_root: Optional[str] = None, *, require_job: Optional[str] = None, **ctx):
    if expected_type not in VALIDATORS: raise RunnerDomainError(f"no validator registered for {expected_type}")
    raw = open(_real_file(path), "rb").read()
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
    if _canon(doc).encode() != raw: raise RunnerDomainError("persisted record is not in canonical byte form")
    if set(doc) != ENVELOPE_KEYS: raise RunnerDomainError("persisted envelope keys differ")
    if doc["type"] != expected_type: raise RunnerDomainError(f"persisted record is {doc['type']}, expected {expected_type}")
    if doc["record_schema_sha256"] != record_schema_identity(): raise RunnerDomainError("persisted record schema differs from the current schema")
    validate_stage_identity(stage, repo_root, pinned_root)
    if doc["stage_sha256"] != stage.result_sha256: raise RunnerDomainError("persisted record belongs to a different stage")
    if require_job is not None:
        if doc["job"] != require_job or type(doc["authorization_version"]) is not int: raise RunnerDomainError(f"record was not produced under an authorization for job {require_job}")
        a, fsha = load_authorization(repo_root, stage, doc["authorization_version"])
        grants = (a.production_authorized if require_job == "production" else a.tranche_authorized if require_job == "calibration_tranche" else require_job in a.authorized_jobs)
        if (doc["authorization_sha256"], doc["authorization_file_sha256"]) != (a.result_sha256, fsha) or not grants:
            raise RunnerDomainError(f"record's authorization binding does not match the committed authorization v{a.version} granting {require_job}")
    rec = _decode(doc["record"])
    if type(rec).__name__ != expected_type: raise RunnerDomainError("decoded record type mismatch")
    VALIDATORS[expected_type](rec, stage=stage, repo_root=repo_root, pinned_root=pinned_root, **ctx)
    return rec, hashlib.sha256(raw).hexdigest()


# ----------------------------------------------------------------------------- 3. F8 run artifacts (M1 F8RunResult persisted; the trace is the observation)
@dataclass(frozen=True)
class RunProvenance:
    """One M1 run: identity, the persisted trace's identities, and the summary fields the trace must recompute to (Interpretation 001)."""
    seed: int
    obj: str
    panel: str
    spec_hash: str
    stream_key: Tuple[int, int, int]
    rho_sha256: str                     # M1 F8RunResult.rho_sha256() (the float64 density array)
    rho_file_sha256: str                # the parquet file
    survival: bool
    rho_tail_mean: float
    tail_window_means: Tuple[float, ...]
    extinction_tick: Optional[int]
    ticks_advanced: int
    draws_consumed: int
    status: str                         # M2 status against the adapter (realization/null objects; "" for skeleton objects and in rehearsal)
    theta_p: float
    theta_t: float


def _run_paths(level_dir: str, seed: int, obj: str) -> Tuple[str, str]:
    return os.path.join(level_dir, f"s{seed}.{obj}.rho_global.parquet"), os.path.join(level_dir, f"s{seed}.{obj}.run.json")


def _read_rho_series(path: str) -> np.ndarray:
    import pyarrow.parquet as pq
    t = pq.read_table(path)
    if t.column_names != ["Tick", "rho_global"]: raise ApparatusHalt("persisted rho table schema differs from M1's")
    arr = t.column("rho_global").to_numpy().astype(np.float64, copy=False)
    tick = t.column("Tick").to_numpy()
    if not np.array_equal(tick, np.arange(arr.size)): raise ApparatusHalt("persisted rho table ticks are not 0..T")
    return np.ascontiguousarray(arr)


def result_from_artifacts(level_dir: str, prov: RunProvenance, level_micro: int, grid: int, ticks: int) -> _D.F8RunResult:
    """Rebuild M1's F8RunResult from the persisted trace and the run record (counts recovered exactly from the density record), so that
    M-P1's `sweep_from_results` validates the observation against the SPEC and recomputes every summary from the trace (D3)."""
    rp, _ = _run_paths(level_dir, prov.seed, prov.obj)
    if not os.path.isfile(rp) or _sha_file(_real_file(rp)) != prov.rho_file_sha256: raise RunnerDomainError(f"rho table for seed {prov.seed} ({prov.obj}) absent or not the recorded identity")
    rho = _read_rho_series(rp)
    n = grid * grid
    if rho.shape != (ticks + 1,): raise RunnerDomainError("persisted trace length differs from the record's shape")
    counts = np.rint(rho * np.float64(n)).astype(np.int64)
    if not np.array_equal(counts.astype(np.float64) / np.float64(n), rho): raise RunnerDomainError("persisted trace is not on the count grid")
    res = _D.F8RunResult(prov.spec_hash, int(level_micro), level_id(level_micro), int(prov.seed), prov.obj, rho, counts, prov.extinction_tick, int(prov.ticks_advanced),
                         tuple(prov.tail_window_means), bool(prov.survival), float(prov.rho_tail_mean), tuple(prov.stream_key), int(prov.draws_consumed))
    if res.rho_sha256() != prov.rho_sha256: raise RunnerDomainError("persisted trace identity differs from the recorded rho_sha256")
    return res


def _execution_metadata(counts: np.ndarray, spec) -> Tuple[Optional[int], int, int]:
    """M1's execution facts DERIVED from the spec and the persisted trace (dynamics.run, placed): the absorbing objects (eta_floor == 0) record
    the first zero count as the extinction tick and stop there; the others advance the full horizon; draws = initialization draw (realization/null)
    + one per advanced tick (L2 r1 D4a)."""
    T = int(spec.ticks); absorbing = (spec.eta_floor == 0.0)
    zeros = np.flatnonzero(counts == 0)
    extinction = int(zeros[0]) if (absorbing and zeros.size) else None
    if extinction is not None and np.any(counts[extinction:] != 0): raise RunnerDomainError("absorbing trace is not zero after its extinction tick")
    advanced = T if extinction is None else extinction
    draws = (1 if spec.obj in ("realization", "null") else 0) + advanced
    return extinction, advanced, draws


def _read_run_record(jp: str) -> RunProvenance:
    """The per-run record is read through the CANONICAL-BYTE reader: exact bytes, exact type (L2 r1 D4b)."""
    raw = open(jp, "rb").read()
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
    if _canon(doc).encode() != raw: raise RunnerDomainError("run record is not in canonical byte form")
    prov = _decode(doc)
    if type(prov) is not RunProvenance: raise RunnerDomainError("run record is not a RunProvenance")
    return prov


def _seal_level_dir(partial: str, level_dir: str) -> None:
    """Rename the completed .partial directory to its final name (all-or-nothing, as before). On Windows a real-time scanner may
    briefly hold a handle on a freshly written file inside the directory, and the rename is refused with PermissionError
    (WinError 5) although nothing is wrong with the bytes (canonical suite 2026-11-04: 18 M7 errors; a 60-trial probe reproduced
    one refusal that succeeded 0.1 s later). The rename is retried for a bounded 10 s; any other error, or exhaustion, raises
    as before. Nothing written, hashed or validated changes: the directory contents are untouched and a rename either happens
    whole or not at all."""
    import time
    deadline = time.monotonic() + 10.0
    while True:
        try: os.replace(partial, level_dir); return
        except PermissionError:
            if time.monotonic() >= deadline: raise
            time.sleep(0.1)


def _execute_run(level_micro: int, seed: int, obj: str, panel: str, grid: int, ticks: int, out_dir: str, adapter) -> Tuple[RunProvenance, _D.F8RunResult]:
    spec = _C.f8_run_spec(level_micro, seed, obj, grid=grid, ticks=ticks, panel=panel)
    try: res = _D.run(spec)
    except Exception as e: raise ApparatusHalt(f"run failed at level {level_id(level_micro)} seed {seed} ({obj}): {type(e).__name__}: {e}")
    rp, jp = _run_paths(out_dir, seed, obj)
    rho_file = _D.write_rho_table(res, rp)
    status = ""; tp = tt = 0.0
    if adapter is not None and obj in ("realization", "null"):
        try: tp, tt = adapter.get(level_micro)
        except _A.AuditDomainError as e: raise ApparatusHalt(f"adapter lacks a key for level {level_id(level_micro)}: {e}")
        try: status = run_status(res.rho, tp, tt)[0]
        except _K.ClassifyDomainError as e: raise AnomalyHalt(f"level {level_id(level_micro)} seed {seed}: {e}")
    prov = RunProvenance(int(seed), obj, panel, res.spec_hash, tuple(res.stream_key), res.rho_sha256(), rho_file, bool(res.survival), float(res.rho_tail_mean), tuple(res.tail_window_means),
                         res.extinction_tick, int(res.ticks_advanced), int(res.draws_consumed), status, float(tp), float(tt))
    with open(jp, "w", newline="\n", encoding="utf-8") as f: f.write(_canon(_encode(prov)))
    return prov, res


def _check_provenance(level_dir: str, prov: RunProvenance, level_micro: int, grid: int, ticks: int, adapter, mode: str, replay: bool) -> None:
    """Trace-level replay (always): the run record file equals the record, the trace exists at its identity and recomputes every summary
    through M-P1's observation (spec reconstructed), and the status recomputes by M2. Re-execution replay (`replay`): M1 re-run under the
    reconstructed spec must reproduce the trace identity — same platform only; the stage records the platform."""
    rp, jp = _run_paths(level_dir, prov.seed, prov.obj)
    if not os.path.isfile(jp) or _read_run_record(_real_file(jp)) != prov: raise RunnerDomainError(f"run record for seed {prov.seed} ({prov.obj}) absent or differs")
    spec = _C.f8_run_spec(level_micro, prov.seed, prov.obj, grid=grid, ticks=ticks, panel=prov.panel)
    if prov.spec_hash != spec.spec_hash() or tuple(prov.stream_key) != spec.stream_key: raise RunnerDomainError(f"seed {prov.seed}: spec hash / stream key do not reconstruct")
    res = result_from_artifacts(level_dir, prov, level_micro, grid, ticks)
    ext, adv, drw = _execution_metadata(np.asarray(res.active_counts), spec)
    if (prov.extinction_tick, prov.ticks_advanced, prov.draws_consumed) != (ext, adv, drw) or type(prov.ticks_advanced) is not int or type(prov.draws_consumed) is not int or (prov.extinction_tick is not None and type(prov.extinction_tick) is not int):
        raise RunnerDomainError(f"seed {prov.seed}: execution metadata (extinction tick, ticks advanced, draws) do not derive from the spec and trace")
    surv, rho_hat, wins = _E.observation_from_result(res, spec)
    if (surv, rho_hat, wins) != (prov.survival, prov.rho_tail_mean, tuple(prov.tail_window_means)): raise RunnerDomainError(f"seed {prov.seed}: summary fields do not recompute from the trace")
    if mode == "production" and prov.obj in ("realization", "null"):
        tp, tt = adapter.get(level_micro)
        if (prov.theta_p, prov.theta_t) != (tp, tt) or run_status(res.rho, tp, tt)[0] != prov.status: raise RunnerDomainError(f"seed {prov.seed}: status does not recompute against the adapter")
    elif prov.status != "" or prov.theta_p != 0.0 or prov.theta_t != 0.0: raise RunnerDomainError("a skeleton or rehearsal run carries no status")
    if replay:
        r2 = _D.run(spec)
        if r2.rho_sha256() != prov.rho_sha256 or (r2.extinction_tick, r2.ticks_advanced, r2.draws_consumed, r2.survival, r2.rho_tail_mean, tuple(r2.tail_window_means)) != (prov.extinction_tick, prov.ticks_advanced, prov.draws_consumed, prov.survival, prov.rho_tail_mean, tuple(prov.tail_window_means)):
            raise RunnerDomainError(f"seed {prov.seed}: M1 re-execution does not reproduce the persisted trace and its execution metadata on this platform")


RUN_MODES = ("production", "rehearsal")


@dataclass(frozen=True)
class LevelRecord:
    """One (level, object, panel): the 20 panel runs with their artifacts; the label (realization/null, production) by M2's 16/2/4."""
    mode: str
    job: str                                      # the canonical job that produced the level ("" in rehearsal)
    level_micro: int
    obj: str
    panel: str
    grid: int
    ticks: int
    pass_number: int
    router_manifest_sha256: str
    runs: Tuple[RunProvenance, ...]
    label: str
    adapter_body_sha256: str
    stage_sha256: str
    authorization_version: int
    authorization_sha256: str
    authorization_file_sha256: str
    prerequisite_identities: Tuple[Tuple[str, str, str], ...]
    result_sha256: str = ""


_LEVEL_FIELDS = tuple(f.name for f in dataclasses.fields(LevelRecord) if f.name != "result_sha256")
def _level_body(r) -> Tuple: return tuple(getattr(r, k) for k in _LEVEL_FIELDS)
def _level_file(level_micro: int, obj: str, panel: str) -> str: return f"{level_id(level_micro)}.{obj}.{panel}.level.json"
def _level_dirname(level_micro: int, obj: str, panel: str) -> str: return f"{level_id(level_micro)}.{obj}.{panel}"


def _panel_seeds(panel: str) -> Tuple[int, ...]:
    if panel not in PANELS: raise RunnerDomainError("unknown panel")
    if panel == "stability": return tuple(stability_seed_panel())
    return tuple(F8_SEED_PANEL if panel == "canonical" else F8_CALIBRATION_SEED_PANEL)


def _job_permits(job: str, obj: str, panel: str) -> bool:
    """THE job -> (objects, panel) mapping (L2 r1 D2), consulted before any run and on every persisted production level."""
    for j, objs, p in JOB_OBJECTS:
        if j == job: return obj in objs and panel == p
    return False


def require_level_slot(r, level_micro: int, obj: str, panel: str, job: str, mode: str = "production") -> None:
    """Bind a loaded LevelRecord to the slot it was requested for (L2 r1 D4c): a record valid for its own level is not evidence for another's."""
    if (r.mode, r.level_micro, r.obj, r.panel, r.job) != (mode, int(level_micro), obj, panel, job): raise RunnerDomainError(f"level record is not the {mode} record of ({level_id(level_micro)}, {obj}, {panel}, {job})")


def validate_level_record(r, stage=None, level_dir: Optional[str] = None, adapter=None, repo_root: Optional[str] = None, pinned_root: Optional[str] = None, records_dir: Optional[str] = None, replay: bool = False, **ctx) -> None:
    if type(r) is not LevelRecord or r.mode not in RUN_MODES or r.obj not in RUN_OBJECTS or r.panel not in PANELS: raise RunnerDomainError("exact LevelRecord with known mode/object/panel required")
    on_grid = r.level_micro in F8_LEVELS_MICRO
    if r.pass_number != (1 if on_grid else 2): raise RunnerDomainError("pass number does not derive from the frozen pass-1 grid")
    if on_grid != (r.router_manifest_sha256 == ""): raise RunnerDomainError("a pass-2 level requires a router manifest identity; a pass-1 level carries none")
    if tuple(x.seed for x in r.runs) != _panel_seeds(r.panel) or any(type(x) is not RunProvenance or x.obj != r.obj or x.panel != r.panel for x in r.runs): raise RunnerDomainError("a level record carries exactly its panel's twenty runs of its object, in order")
    for x in r.runs:
        if not (_is_hex(x.spec_hash, 64) and _is_hex(x.rho_sha256, 64) and _is_hex(x.rho_file_sha256, 64)) or len(x.tail_window_means) != _K.N_WINDOWS: raise RunnerDomainError("run provenance malformed")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("level record belongs to a different stage")
    if r.mode == "production":
        if (r.grid, r.ticks) != (F8_GRID, F8_TICKS): raise RunnerDomainError("production level requires the frozen production shape")
        if not on_grid: raise RunnerDomainError("M1's frozen guard defines production-shape runs on the pass-1 grid only; a pass-2 level record cannot exist (EvaluabilityHalt is recorded on the morphology record instead)")
        if not _job_permits(r.job, r.obj, r.panel): raise RunnerDomainError(f"job {r.job} does not run ({r.obj}, {r.panel}) (L2 r1 D2)")
        if level_dir is None or adapter is None or repo_root is None or stage is None: raise RunnerDomainError("a production level record validates only with its stage, repository, artifact directory and the production adapter")
        if not _is_production_adapter(adapter) or adapter.body_sha256 != r.adapter_body_sha256 or stage.adapter_body_sha256 != adapter.body_sha256: raise RunnerDomainError("production level requires the stage's committed production adapter")
        if r.obj in ("realization", "null"):
            if any(x.status not in _K.STATUSES for x in r.runs): raise RunnerDomainError("production runs of a scored object require legal statuses")
            if r.label != level_label(level_counts(tuple(x.status for x in r.runs))): raise RunnerDomainError("level label does not re-derive from the statuses")
        elif r.label != "" or any(x.status != "" for x in r.runs): raise RunnerDomainError("skeleton objects carry no status or label")
        auth, afile = load_authorization(repo_root, stage, r.authorization_version)
        if r.job not in auth.authorized_jobs or (auth.result_sha256, afile) != (r.authorization_sha256, r.authorization_file_sha256): raise RunnerDomainError("level record's job authorization does not reproduce from the committed record")
        if r.job in SCIENTIFIC_JOBS:
            if not auth.production_authorized: raise RunnerDomainError("a scientific lattice job requires the production flag (s7.1 readiness)")
            rd = validate_prerequisites(auth, stage, repo_root, pinned_root)
            if not rd.production_ready or tuple((n, rid, auth.prerequisite_manifest_sha256) for n, _, _, rid, _, _ in rd.rows) != r.prerequisite_identities: raise RunnerDomainError("level record's prerequisites do not re-validate to a production-ready state with the carried identities")
        elif r.prerequisite_identities != (): raise RunnerDomainError("an apparatus lattice job carries no prerequisite identities")
    else:
        if r.job != "" or r.label != "" or r.authorization_version != 0 or r.authorization_sha256 != "" or r.authorization_file_sha256 != "" or r.prerequisite_identities != () or r.adapter_body_sha256 != "" or any(x.status != "" for x in r.runs):
            raise RunnerDomainError("a rehearsal level carries no classification, authorization, adapter or prerequisites")
    if level_dir is not None and os.path.islink(level_dir): raise RunnerDomainError("level artifact directory is a link: refused")
    akey = (r.result_sha256, _tree_digest(level_dir) if level_dir is not None and os.path.isdir(level_dir) else "", getattr(adapter, "body_sha256", ""), replay, _frozen_code_key())
    if level_dir is not None and akey not in _ARTIFACT_REPLAY_MEMO:
        for x in r.runs: _check_provenance(level_dir, x, r.level_micro, r.grid, r.ticks, adapter, r.mode, replay)
        if r.result_sha256 == _digest(_level_body(r)): _ARTIFACT_REPLAY_MEMO[akey] = True
    if r.result_sha256 != _digest(_level_body(r)): raise RunnerDomainError("level record identity does not recompute")


def run_level(level_micro: int, obj: str, panel: str, out_dir: str, stage: StageIdentity, mode: str, *, job: str = "", adapter=None, grid: int = F8_GRID, ticks: int = F8_TICKS,
              repo_root: Optional[str] = None, pinned_root: Optional[str] = None, authorization_version: Optional[int] = None) -> LevelRecord:
    """One (level, object, panel), all-or-nothing, twenty runs. Production: canonical stage, the COMMITTED production authorization, prerequisites
    READY, production shape, the stage's committed adapter; persisted canonically. Pass is derived from the grid; production-shape runs exist
    on the pass-1 grid only (M1's guard), so a pass-2 request in production is an EvaluabilityHalt before any run."""
    verify_frozen_identity()
    if mode not in RUN_MODES or obj not in RUN_OBJECTS or panel not in PANELS: raise RunnerDomainError("unknown run mode, object or panel")
    if type(stage) is not StageIdentity: raise RunnerDomainError("exact StageIdentity required")
    on_grid = level_micro in F8_LEVELS_MICRO
    auth = None; auth_file = ""; prereqs: Tuple = ()
    if mode == "production":
        if repo_root is None or authorization_version is None: raise RunnerDomainError("production requires the repository and an authorization version")
        validate_stage_identity(stage, repo_root, pinned_root)
        if stage.role != "canonical": raise RunnerDomainError("production requires a canonical stage")
        if not on_grid: raise EvaluabilityHalt(f"level {level_micro} is off the pass-1 grid: M1's frozen production guard cannot execute it")
        if not _job_permits(job, obj, panel): raise RunnerDomainError(f"job {job} does not run ({obj}, {panel}): refused before any run (L2 r1 D2)")
        auth, auth_file = load_authorization(repo_root, stage, authorization_version)
        if job not in auth.authorized_jobs: raise RunnerDomainError(f"job {job} is not authorized by record v{auth.version} (source literals grant nothing)")
        if job in SCIENTIFIC_JOBS:
            if not auth.production_authorized: raise RunnerDomainError(f"the scientific jobs are not authorized by record v{auth.version}: production flag absent (s7.1)")
            rd = validate_prerequisites(auth, stage, repo_root, pinned_root)
            if not rd.production_ready: raise RunnerDomainError(f"production is not READY: valid/complete={rd.all_valid_complete}, branch stops={[s for s in rd.branch_stops if s[2]]}")
            prereqs = tuple((n, rid, auth.prerequisite_manifest_sha256) for n, _, _, rid, _, _ in rd.rows)
        if (grid, ticks) != (F8_GRID, F8_TICKS): raise RunnerDomainError("production requires the frozen production shape")
        if adapter is None or not _is_production_adapter(adapter) or adapter.body_sha256 != stage.adapter_body_sha256: raise ApparatusHalt("production requires the stage's committed production adapter")
        require_job_dependencies(job, out_dir, stage, repo_root, pinned_root, adapter)    # the SAME semantic gate on the direct route (L2 r1 D3b; r2 R2-2, R2-6)
    else:
        if not on_grid and (grid, ticks) == (F8_GRID, F8_TICKS): raise RunnerDomainError("rehearsal at production shape runs only on the frozen pass-1 grid")
        adapter = None
    level_dir = os.path.join(out_dir, _level_dirname(level_micro, obj, panel)); partial = level_dir + ".partial"
    if os.path.exists(partial): shutil.rmtree(partial)
    os.makedirs(partial)
    runs: List[RunProvenance] = []
    for seed in _panel_seeds(panel):
        prov, _ = _execute_run(level_micro, seed, obj, panel, grid, ticks, partial, adapter if mode == "production" else None)
        runs.append(prov)
    if os.path.exists(level_dir): shutil.rmtree(level_dir)
    _seal_level_dir(partial, level_dir)
    lab = level_label(level_counts(tuple(x.status for x in runs))) if (mode == "production" and obj in ("realization", "null")) else ""
    body = dict(mode=mode, job=job if mode == "production" else "", level_micro=int(level_micro), obj=obj, panel=panel, grid=int(grid), ticks=int(ticks), pass_number=1 if on_grid else 2, router_manifest_sha256="", runs=tuple(runs), label=lab,
                adapter_body_sha256=adapter.body_sha256 if mode == "production" else "", stage_sha256=stage.result_sha256,
                authorization_version=auth.version if auth else 0, authorization_sha256=auth.result_sha256 if auth else "", authorization_file_sha256=auth_file, prerequisite_identities=prereqs)
    rec = LevelRecord(**body, result_sha256=_digest(_level_body(LevelRecord(**body))))
    if mode == "production":
        _persist_canonical(rec, os.path.join(out_dir, _level_file(level_micro, obj, panel)), stage, repo_root, pinned_root, auth, auth_file, job, level_dir=level_dir, adapter=adapter, records_dir=out_dir)
    return rec


def _job_of(obj: str, panel: str) -> str:
    for j, objs, p in JOB_OBJECTS:
        if obj in objs and p == panel: return j
    raise RunnerDomainError(f"no lattice job runs ({obj}, {panel})")


def _load_level_results(records_dir: str, obj: str, panel: str, stage, repo_root, pinned_root, adapter, *, replay: bool = False) -> Tuple[Dict[int, List[_D.F8RunResult]], Dict[int, str], Tuple[Tuple[int, str, str], ...]]:
    """Every pass-1 level's authorized production LevelRecord for (obj, panel) → M1 results rebuilt from the artifacts (or a halt key where the
    level file is absent). Returns (results by level, halts by level, (level, file sha, record identity) rows)."""
    results: Dict[int, List[_D.F8RunResult]] = {}; halts: Dict[int, str] = {}; rows = []
    for m in F8_LEVELS_MICRO:
        fp = os.path.join(records_dir, _level_file(m, obj, panel))
        if not os.path.isfile(fp): halts[m] = f"apparatus:level {level_id(m)} ({obj}, {panel}) not produced"; continue
        rec, fsha = load_record(fp, "LevelRecord", stage, repo_root, pinned_root, require_job=_job_of(obj, panel), level_dir=os.path.join(records_dir, _level_dirname(m, obj, panel)), adapter=adapter, records_dir=records_dir, replay=replay)
        require_level_slot(rec, m, obj, panel, _job_of(obj, panel))
        results[m] = [result_from_artifacts(os.path.join(records_dir, _level_dirname(m, obj, panel)), x, m, rec.grid, rec.ticks) for x in rec.runs]
        rows.append((m, fsha, rec.result_sha256))
    return results, halts, tuple(rows)


# ----------------------------------------------------------------------------- 4. calibration-tranche quarantine (E1 grammar on F8 runs; evidence replayable by re-execution)
@dataclass(frozen=True)
class TrancheQuarantine:
    levels_micro: Tuple[int, ...]
    seeds: Tuple[int, ...]
    grid: int
    ticks: int
    n_runs: int
    spec_hashes: Tuple[str, ...]
    rho_sha256: Tuple[str, ...]
    rho_file_sha256: Tuple[str, ...]
    wall_clock_s: float
    bytes_written: int
    cleanup_proven: bool
    status: str
    stage_sha256: str
    authorization_version: int
    authorization_sha256: str
    authorization_file_sha256: str
    result_sha256: str = ""

    def __getattr__(self, name): raise QuarantineViolation(f"the calibration-tranche quarantine exposes no {name!r}: integrity, cost and provenance only")


_Q_FIELDS = tuple(f.name for f in dataclasses.fields(TrancheQuarantine) if f.name != "result_sha256")
def _q_body(q) -> Tuple: return tuple(getattr(q, k) for k in _Q_FIELDS)
TRANCHE_OBJECT = "realization"


def validate_quarantine(q, stage=None, repo_root=None, pinned_root=None, replay: bool = False, **ctx) -> None:
    if type(q) is not TrancheQuarantine: raise RunnerDomainError("exact TrancheQuarantine required")
    n = len(q.levels_micro) * len(q.seeds)
    if q.n_runs != n or any(len(v) != n for v in (q.spec_hashes, q.rho_sha256, q.rho_file_sha256)): raise RunnerDomainError("tranche provenance vectors inconsistent")
    if any(not _is_hex(h, 64) for v in (q.spec_hashes, q.rho_sha256, q.rho_file_sha256) for h in v) or type(q.cleanup_proven) is not bool or q.status not in ("passed", "failed"): raise RunnerDomainError("tranche provenance malformed")
    if not (type(q.wall_clock_s) is float and np.isfinite(q.wall_clock_s) and q.wall_clock_s >= 0.0) or type(q.bytes_written) is not int or q.bytes_written < 0: raise RunnerDomainError("tranche cost fields must be finite and non-negative")
    if q.status != ("passed" if (q.cleanup_proven and n == TRANCHE_SEEDS * TRANCHE_LEVELS) else "failed"): raise RunnerDomainError("tranche status does not derive from its cleanup/count facts")
    for i, (m, s) in enumerate((m, s) for m in q.levels_micro for s in q.seeds):
        if q.spec_hashes[i] != _C.f8_run_spec(int(m), int(s), TRANCHE_OBJECT, grid=q.grid, ticks=q.ticks).spec_hash(): raise RunnerDomainError("tranche spec hashes do not re-derive from the contracted specifications")
    if stage is not None and q.stage_sha256 != stage.result_sha256: raise RunnerDomainError("quarantine belongs to a different stage")
    authorized = bool(q.authorization_sha256 or q.authorization_file_sha256 or q.authorization_version)
    if authorized:
        if (q.grid, q.ticks) != (F8_GRID, F8_TICKS): raise RunnerDomainError("an authorized tranche runs at production shape")
        if repo_root is None or stage is None: raise RunnerDomainError("an authorized tranche validates only against its committed authorization")
        a, afile = load_authorization(repo_root, stage, q.authorization_version)
        if not a.tranche_authorized or (a.result_sha256, afile) != (q.authorization_sha256, q.authorization_file_sha256) or (q.levels_micro, q.seeds) != (a.tranche_levels_micro, a.tranche_seeds):
            raise RunnerDomainError("tranche panel/identities do not reproduce from the committed tranche authorization")
    if replay:
        import tempfile
        d = tempfile.mkdtemp()
        try: r2 = _tranche_execute(q.levels_micro, q.seeds, d, stage if stage is not None else _StageStub(q.stage_sha256), q.grid, q.ticks, q.authorization_version, q.authorization_sha256, q.authorization_file_sha256)
        finally: shutil.rmtree(d, ignore_errors=True)
        if (r2.rho_sha256, r2.rho_file_sha256) != (q.rho_sha256, q.rho_file_sha256): raise RunnerDomainError("tranche evidence does not reproduce by deterministic re-execution on this platform")
    if q.result_sha256 != _digest(_q_body(q)): raise RunnerDomainError("quarantine identity does not recompute")


@dataclass(frozen=True)
class _StageStub:
    result_sha256: str


def _tranche_execute(levels, seeds, out_dir, stage, grid, ticks, auth_ver, auth_sha, auth_file) -> TrancheQuarantine:
    sealed = os.path.join(out_dir, ".tranche_sealed"); shutil.rmtree(sealed, ignore_errors=True); os.makedirs(sealed)
    sh, rs, rf = [], [], []; nbytes = 0; t0 = time.perf_counter(); n = 0; written: List[str] = []
    try:
        for m in levels:
            for s in seeds:
                prov, _ = _execute_run(int(m), int(s), TRANCHE_OBJECT, "canonical", grid, ticks, sealed, None)
                rp, jp = _run_paths(sealed, int(s), TRANCHE_OBJECT)
                sh.append(prov.spec_hash); rs.append(prov.rho_sha256); rf.append(prov.rho_file_sha256); n += 1
                written += [rp, jp]; nbytes += os.path.getsize(rp) + os.path.getsize(jp)
    finally:
        shutil.rmtree(sealed, ignore_errors=True)
    wall = float(time.perf_counter() - t0)
    clean = (not os.path.exists(sealed)) and not any(os.path.exists(p) for p in written) and n == len(levels) * len(seeds)
    status = "passed" if (clean and n == TRANCHE_SEEDS * TRANCHE_LEVELS) else "failed"
    body = dict(levels_micro=tuple(int(x) for x in levels), seeds=tuple(int(x) for x in seeds), grid=grid, ticks=ticks, n_runs=n, spec_hashes=tuple(sh), rho_sha256=tuple(rs), rho_file_sha256=tuple(rf),
                wall_clock_s=wall, bytes_written=int(nbytes), cleanup_proven=bool(clean), status=status, stage_sha256=stage.result_sha256,
                authorization_version=auth_ver, authorization_sha256=auth_sha, authorization_file_sha256=auth_file)
    return TrancheQuarantine(**body, result_sha256=_digest(_q_body(TrancheQuarantine(**body))))


def run_tranche(out_dir: str, stage: StageIdentity, repo_root: str, pinned_root: Optional[str], authorization_version: int) -> Tuple[TrancheQuarantine, str]:
    verify_frozen_identity(); validate_stage_identity(stage, repo_root, pinned_root)
    if stage.role != "canonical": raise RunnerDomainError("the tranche requires a canonical stage")
    auth, fsha = load_authorization(repo_root, stage, authorization_version)
    if not auth.tranche_authorized: raise RunnerDomainError(f"the calibration tranche is not authorized by record v{auth.version} (source literals grant nothing)")
    q = _tranche_execute(auth.tranche_levels_micro, auth.tranche_seeds, out_dir, stage, F8_GRID, F8_TICKS, auth.version, auth.result_sha256, fsha)
    path = os.path.join(out_dir, "calibration_tranche.json")
    _persist_canonical(q, path, stage, repo_root, pinned_root, auth, fsha, "calibration_tranche")
    return q, path


def _tranche_for_tests(levels, seeds, out_dir, stage, *, grid: int, ticks: int) -> TrancheQuarantine:
    if (grid, ticks) == (F8_GRID, F8_TICKS): raise RunnerDomainError("the test helper may not run at production shape")
    if len(levels) != TRANCHE_LEVELS or len(seeds) != TRANCHE_SEEDS: raise RunnerDomainError("the tranche is exactly the declared seeds x levels")
    return _tranche_execute(levels, seeds, out_dir, stage, grid, ticks, 0, "", "")


# ----------------------------------------------------------------------------- 5. resource benchmark (gated; every objective file fact re-derived)
@dataclass(frozen=True)
class ResourceBenchmark:
    role: str
    level_micro: int
    seeds: Tuple[int, ...]
    grid: int
    ticks: int
    spec_hashes: Tuple[str, ...]
    artifact_manifest: Tuple[Tuple[str, str, int], ...]   # (file name, sha256, byte size): rho parquet and run record per seed
    rho_bytes_per_run: Tuple[int, ...]
    wall_clock_per_run_s: Tuple[float, ...]
    readback_s_per_run: Tuple[float, ...]
    projected_wall_clock_s: float
    projected_bytes: int
    free_bytes_measured: int
    fits_with_margin: bool
    stage_sha256: str
    authorization_version: int
    authorization_sha256: str
    authorization_file_sha256: str
    result_sha256: str = ""


_B_FIELDS = tuple(f.name for f in dataclasses.fields(ResourceBenchmark) if f.name != "result_sha256")
def _b_body(b) -> Tuple: return tuple(getattr(b, k) for k in _B_FIELDS)
BENCHMARK_OBJECT = "realization"


def validate_benchmark(b, stage=None, repo_root=None, pinned_root=None, artifact_dir: Optional[str] = None, **ctx) -> None:
    if type(b) is not ResourceBenchmark or b.role not in ("canonical", "smoke"): raise RunnerDomainError("exact ResourceBenchmark required")
    n = len(b.seeds)
    if not (1 <= n <= 20 and n == len(b.spec_hashes) == len(b.rho_bytes_per_run) == len(b.wall_clock_per_run_s) == len(b.readback_s_per_run)) or len(b.artifact_manifest) != 2 * n: raise RunnerDomainError("measurement vectors inconsistent")
    if any(s not in F8_SEED_PANEL for s in b.seeds) or any(type(x) is not float or not np.isfinite(x) or x <= 0.0 for x in b.wall_clock_per_run_s + b.readback_s_per_run) \
            or any(type(x) is not int or x <= 0 for x in b.rho_bytes_per_run) or type(b.free_bytes_measured) is not int or b.free_bytes_measured < 0: raise RunnerDomainError("benchmark measurements out of domain")
    for i, s in enumerate(b.seeds):
        if b.spec_hashes[i] != _C.f8_run_spec(b.level_micro, s, BENCHMARK_OBJECT, grid=b.grid, ticks=b.ticks).spec_hash(): raise RunnerDomainError("benchmark spec hashes do not re-derive")
    per_run_bytes = [b.artifact_manifest[2 * i][2] + b.artifact_manifest[2 * i + 1][2] for i in range(n)]
    pw = PRODUCTION_RUNS * max(b.wall_clock_per_run_s) * (1 + BENCHMARK_MARGIN); pb = int(PRODUCTION_RUNS * max(per_run_bytes) * (1 + BENCHMARK_MARGIN))
    if (b.projected_wall_clock_s, b.projected_bytes, b.fits_with_margin) != (pw, pb, pb <= b.free_bytes_measured): raise RunnerDomainError("projections do not derive from the measurements")
    if stage is not None and b.stage_sha256 != stage.result_sha256: raise RunnerDomainError("benchmark belongs to a different stage")
    if b.role == "canonical":
        if (b.grid, b.ticks) != (F8_GRID, F8_TICKS) or (b.level_micro, b.seeds) != (BENCHMARK_LEVEL_MICRO, tuple(F8_SEED_PANEL[:BENCHMARK_SEEDS])): raise RunnerDomainError("a canonical benchmark uses production shape and the frozen panel")
        if artifact_dir is None or repo_root is None or stage is None: raise RunnerDomainError("a canonical benchmark validates only with its kept artifacts and its committed authorization")
        a, afile = load_authorization(repo_root, stage, b.authorization_version)
        if "resource_benchmark" not in a.authorized_jobs or (a.result_sha256, afile) != (b.authorization_sha256, b.authorization_file_sha256): raise RunnerDomainError("benchmark authorization does not reproduce from the committed record")
    elif b.authorization_version or b.authorization_sha256 or b.authorization_file_sha256: raise RunnerDomainError("a smoke benchmark carries no authorization")
    expected = tuple(os.path.basename(p) for s in b.seeds for p in _run_paths("", s, BENCHMARK_OBJECT))
    if tuple(nm for nm, _, _ in b.artifact_manifest) != expected: raise RunnerDomainError("artifact manifest must be exactly the rho table and run record per seed, in canonical order")
    if tuple(b.artifact_manifest[2 * i][2] for i in range(n)) != b.rho_bytes_per_run: raise RunnerDomainError("per-run byte counts differ from the manifest")
    if artifact_dir is not None:
        for name, sha, size in b.artifact_manifest:
            fp = os.path.join(artifact_dir, name)
            if not os.path.isfile(fp) or _sha_file(fp) != sha or os.path.getsize(fp) != size: raise RunnerDomainError(f"benchmark artifact {name} absent or differs from its manifest entry")
        for i, s in enumerate(b.seeds):
            prov = _decode(json.loads(open(os.path.join(artifact_dir, b.artifact_manifest[2 * i + 1][0]), "rb").read().decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const))
            if type(prov) is not RunProvenance or prov.seed != s or prov.spec_hash != b.spec_hashes[i]: raise RunnerDomainError(f"benchmark run record for seed {s} malformed")
            _check_provenance(artifact_dir, prov, b.level_micro, b.grid, b.ticks, None, "rehearsal", False)
    if b.result_sha256 != _digest(_b_body(b)): raise RunnerDomainError("benchmark identity does not recompute")


def _benchmark_execute(n_runs, out_dir, stage, grid, ticks, level_micro, role, auth_ver, auth_sha, auth_file) -> ResourceBenchmark:
    d = os.path.join(out_dir, "benchmark_artifacts"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    sh, man, walls, rb, rbk = [], [], [], [], []
    try:
        for seed in F8_SEED_PANEL[:n_runs]:
            t0 = time.perf_counter(); prov, _ = _execute_run(level_micro, seed, BENCHMARK_OBJECT, "canonical", grid, ticks, d, None); walls.append(float(time.perf_counter() - t0))
            rp, jp = _run_paths(d, seed, BENCHMARK_OBJECT)
            sh.append(prov.spec_hash)
            for fp in (rp, jp): man.append((os.path.basename(fp), _sha_file(fp), int(os.path.getsize(fp))))
            rb.append(int(os.path.getsize(rp)))
            t1 = time.perf_counter(); _sha_file(rp); _read_rho_series(rp); rbk.append(max(float(time.perf_counter() - t1), 1e-9))
        free = int(shutil.disk_usage(out_dir).free)
    except Exception:
        shutil.rmtree(d, ignore_errors=True); raise
    per_run = [man[2 * i][2] + man[2 * i + 1][2] for i in range(n_runs)]
    pw = PRODUCTION_RUNS * max(walls) * (1 + BENCHMARK_MARGIN); pb = int(PRODUCTION_RUNS * max(per_run) * (1 + BENCHMARK_MARGIN))
    body = dict(role=role, level_micro=int(level_micro), seeds=tuple(F8_SEED_PANEL[:n_runs]), grid=grid, ticks=ticks, spec_hashes=tuple(sh), artifact_manifest=tuple(man), rho_bytes_per_run=tuple(rb),
                wall_clock_per_run_s=tuple(walls), readback_s_per_run=tuple(rbk), projected_wall_clock_s=pw, projected_bytes=pb, free_bytes_measured=free, fits_with_margin=pb <= free,
                stage_sha256=stage.result_sha256, authorization_version=auth_ver, authorization_sha256=auth_sha, authorization_file_sha256=auth_file)
    return ResourceBenchmark(**body, result_sha256=_digest(_b_body(ResourceBenchmark(**body))))


def run_benchmark_smoke(n_runs: int, out_dir: str, stage: StageIdentity, *, grid: int, ticks: int, level_micro: int = BENCHMARK_LEVEL_MICRO) -> ResourceBenchmark:
    verify_frozen_identity()
    if (grid, ticks) == (F8_GRID, F8_TICKS): raise RunnerDomainError("the smoke benchmark may not run at production shape")
    if isinstance(n_runs, bool) or not isinstance(n_runs, int) or not 1 <= n_runs <= 20: raise RunnerDomainError("n_runs must be 1..20")
    return _benchmark_execute(n_runs, out_dir, stage, grid, ticks, level_micro, "smoke", 0, "", "")


# ----------------------------------------------------------------------------- 6. production prerequisites (E1 M7, carried; F8 vocabulary)
@dataclass(frozen=True)
class PrerequisiteEntry:
    name: str
    record_type: str
    file: str
    file_sha256: str
    record_identity: str
    dependencies: Tuple[Tuple[str, str, str], ...]


@dataclass(frozen=True)
class ProductionPrerequisiteManifest:
    governance_sha256: str
    entries: Tuple[PrerequisiteEntry, ...]
    result_sha256: str = ""


def _manifest_body(m) -> Tuple: return (m.governance_sha256, tuple(dataclasses.astuple(e) for e in m.entries))

PREREQ_TYPES = {"calibration_tranche": "TrancheQuarantine", "resource_actuals": "ResourceBenchmark", "mp1_known_answer": "KnownAnswerQualification",
                "m6_audit_qualification": "AuditQualification", "calibration_census": "CalibrationCensus", "dense_reference": "ReferenceStructure", "reference_stability": "StabilityAudit"}
PREREQ_JOBS = {"calibration_tranche": "calibration_tranche", "resource_actuals": "resource_benchmark", "mp1_known_answer": "mp1_known_answer",
               "m6_audit_qualification": "m6_audit_qualification", "calibration_census": "calibration_census", "dense_reference": "dense_reference", "reference_stability": "reference_stability"}
PREREQ_DEPENDENCY_ROLES = {"StabilityAudit": ("primary",), "AuditQualification": ("design", "held_out")}
_DEP_TYPES = {"primary": "ReferenceStructure", "design": "AuditRecord", "held_out": "AuditRecord"}
_DEP_JOBS = {"primary": "dense_reference", "design": "m6_design_audit", "held_out": "m6_held_out_audit"}


def _confined_rel(rel) -> bool:
    """A manifest path must be a relative POSIX path that stays INSIDE the prerequisites tree on every platform (L2 r2 R2-1): no absolute form
    (POSIX or Windows drive/UNC), no '..' segment, no backslash, no empty segment."""
    if not isinstance(rel, str) or not rel or rel.startswith("/") or rel.startswith("\\") or ":" in rel or "\\" in rel: return False
    parts = rel.split("/")
    return all(p not in ("", ".", "..") for p in parts) and _pp.normpath(rel) == rel


def validate_prerequisite_manifest(m, **ctx) -> None:
    if type(m) is not ProductionPrerequisiteManifest or not _is_hex(m.governance_sha256, 64) or type(m.entries) is not tuple or not m.entries: raise RunnerDomainError("prerequisite manifest malformed")
    for e in m.entries:
        if type(e) is not PrerequisiteEntry or e.name not in PREREQ_VOCAB or e.record_type != PREREQ_TYPES[e.name] or not _is_hex(e.file_sha256, 64) or not _is_hex(e.record_identity, 64): raise RunnerDomainError("prerequisite entry malformed")
        if not _confined_rel(e.file) or any(type(d) is not tuple or len(d) != 3 or d[0] not in PREREQ_DEPENDENCY_ROLES.get(e.record_type, ()) or not _confined_rel(d[1]) or not _is_hex(d[2], 64) for d in e.dependencies):
            raise RunnerDomainError(f"prerequisite {e.name}: file/dependency entries malformed or not in the type's dependency schema")
        if {d[0] for d in e.dependencies} != set(PREREQ_DEPENDENCY_ROLES.get(e.record_type, ())) or len({d[0] for d in e.dependencies}) != len(e.dependencies): raise RunnerDomainError(f"prerequisite {e.name}: dependencies must be exactly the type's schema")
    if len({e.name for e in m.entries}) != len(m.entries): raise RunnerDomainError("prerequisite names must be unique")
    if m.result_sha256 != _digest(_manifest_body(m)): raise RunnerDomainError("prerequisite manifest identity does not recompute")


@dataclass(frozen=True)
class ProductionReadiness:
    governance_sha256: str
    manifest_sha256: str
    rows: Tuple[Tuple[str, str, str, str, bool, bool], ...]
    branch_stops: Tuple[Tuple[str, str, bool], ...]
    all_valid_complete: bool
    production_ready: bool


def _manifest_files_digest(repo_root: str, base: str, mp: str) -> str:
    """Every file the committed manifest NAMES (entries and their dependencies), resolved under the prerequisites tree: working bytes and
    committed-equals-working — the complete resolved dependency graph enters the readiness key (L2 r2 R2-1)."""
    if not os.path.isfile(mp): return ""
    try:
        doc = json.loads(open(mp, "rb").read().decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
        entries = doc["fields"]["entries"] if doc.get("__type__") == "ProductionPrerequisiteManifest" else []
    except Exception: return "unreadable"
    acc = []
    for e in entries:
        rels = [e["fields"]["file"]] + [d[1] for d in e["fields"]["dependencies"]]
        for rel in rels:
            fp = os.path.join(base, *rel.split("/")) if _confined_rel(rel) else None
            acc.append((rel, _sha_file(fp) if fp and os.path.isfile(fp) else "absent", _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, PREREQUISITES_REL, rel)) if fp and os.path.isfile(fp) else False))
    return _digest(tuple(acc))


def validate_prerequisites(auth: AuthorizationRecord, stage: StageIdentity, repo_root: str, pinned_root: Optional[str]) -> ProductionReadiness:
    validate_stage_identity(stage, repo_root, pinned_root)                       # fresh stage facts before any cached readiness is returned (L2 r2 R2-1, secondary)
    gov, gsha = load_governance(repo_root, stage)
    mp = _gov(repo_root, PREREQ_MANIFEST_REL); base = _gov(repo_root, PREREQUISITES_REL)
    key = (os.path.abspath(repo_root), stage.result_sha256, auth.result_sha256, auth.prerequisite_manifest_sha256, _sha_file(mp) if os.path.isfile(mp) else "", _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, PREREQ_MANIFEST_REL)) if os.path.isfile(mp) else False,
           _readiness_surface_digest(repo_root, base) if os.path.isdir(base) else "", _manifest_files_digest(repo_root, base, mp), _authorization_surface_digest(repo_root), gsha, _digest(_gov_body(gov)), stage.package_spec_sha256, _frozen_code_key(), platform_tag())
    if key in _READINESS_MEMO: return _READINESS_MEMO[key]
    rd = _validate_prerequisites_uncached(auth, stage, repo_root, pinned_root, gov, gsha, mp, base)
    _READINESS_MEMO[key] = rd
    return rd


def _prereq_context(e, base, stage, repo_root, pinned_root, fp) -> Dict[str, Any]:
    ctxk: Dict[str, Any] = {}
    for role, rel, dsha in e.dependencies:
        if not _confined_rel(rel): raise RunnerDomainError(f"prerequisite {e.name} dependency {role}: path not confined to the prerequisites tree")
        dp = os.path.join(base, *rel.split("/"))
        if not os.path.isfile(dp) or _sha_file(dp) != dsha: raise RunnerDomainError(f"prerequisite {e.name} dependency {role} absent or not the named identity")
        _require_committed(repo_root, dp)
        ctxk[role] = load_record(dp, _DEP_TYPES[role], stage, repo_root, pinned_root, require_job=_DEP_JOBS[role], expect_production=True)[0]
    if e.record_type == "ResourceBenchmark": ctxk["artifact_dir"] = os.path.join(os.path.dirname(fp), "benchmark_artifacts")
    if e.record_type == "TrancheQuarantine": ctxk["replay"] = True
    if e.record_type == "CalibrationCensus": ctxk["records_dir"] = os.path.dirname(fp); ctxk["adapter"] = _stage_adapter(repo_root, stage)
    return ctxk


def _validate_prerequisites_uncached(auth, stage, repo_root, pinned_root, gov, gsha, mp, base) -> "ProductionReadiness":
    if not os.path.isfile(mp) or _sha_file(mp) != auth.prerequisite_manifest_sha256 or not _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, PREREQ_MANIFEST_REL)):
        raise RunnerDomainError("the committed prerequisite manifest is absent or is not the one the authorization names")
    man = _read_canonical(mp)
    if type(man) is not ProductionPrerequisiteManifest: raise RunnerDomainError("file is not a ProductionPrerequisiteManifest")
    validate_prerequisite_manifest(man)
    if man.governance_sha256 != gsha: raise RunnerDomainError("prerequisite manifest names a different governance record")
    required = {n: (k, q) for n, k, q in gov.production_prerequisites}
    if {e.name for e in man.entries} != set(required): raise RunnerDomainError(f"prerequisite set differs from the governance record's exact production set: {sorted(required)}")
    rows = []
    for e in man.entries:
        if not _confined_rel(e.file): raise RunnerDomainError(f"prerequisite {e.name}: path not confined to the prerequisites tree")
        fp = os.path.join(base, *e.file.split("/"))
        if not os.path.isfile(fp) or _sha_file(fp) != e.file_sha256: raise RunnerDomainError(f"prerequisite {e.name} is absent or differs from its manifest file identity")
        _require_committed(repo_root, fp)
        ctxk = _prereq_context(e, base, stage, repo_root, pinned_root, fp)
        rec, _ = load_record(fp, e.record_type, stage, repo_root, pinned_root, require_job=PREREQ_JOBS[e.name], **ctxk)
        if _item_identity(rec) != e.record_identity: raise RunnerDomainError(f"prerequisite {e.name} record identity differs from the manifest")
        vc, ps = PREREQ_STATES[e.record_type](rec)
        if e.record_type == "ResourceBenchmark":
            for name, _, _ in rec.artifact_manifest: _require_committed(repo_root, os.path.join(os.path.dirname(fp), "benchmark_artifacts", name))
        k, q = required[e.name]; rows.append((e.name, k, q, e.record_identity, vc, ps))
    stops = []
    loaded = {e.name: None for e in man.entries}
    for item, pred in gov.branch_stopping:                       # F8: a branch stop names a PREREQUISITE item (the package is the end state, not an input to readiness)
        e = next((x for x in man.entries if x.name == item), None)
        if e is None: raise RunnerDomainError(f"branch-stopping item {item} is not among the prerequisites")
        fp = os.path.join(base, *e.file.split("/"))
        rec, _ = load_record(fp, e.record_type, stage, repo_root, pinned_root, require_job=PREREQ_JOBS[e.name], **_prereq_context(e, base, stage, repo_root, pinned_root, fp))
        stops.append((item, pred, _eval_predicate(pred, rec)))
    allvc = all(r[4] for r in rows)
    ready = allvc and all((r[5] if r[2] == "pass" else r[4]) for r in rows) and not any(h for _, _, h in stops)
    return ProductionReadiness(gsha, auth.prerequisite_manifest_sha256, tuple(rows), tuple(stops), allvc, ready)


def R_BENCH_MANIFEST(path: str):
    doc = json.loads(open(path, "rb").read().decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
    return tuple(tuple(e) for e in doc["record"]["fields"]["artifact_manifest"])


PREREQ_STATES = {
    "TrancheQuarantine": lambda r: (r.status in ("passed", "failed") and bool(r.authorization_sha256), r.status == "passed"),
    "ResourceBenchmark": lambda r: (r.role == "canonical", r.role == "canonical" and r.fits_with_margin),
    "KnownAnswerQualification": lambda r: (r.census_is_declared_synthetic, r.passed),
    "AuditQualification": lambda r: (True, r.qualified),
    "CalibrationCensus": lambda r: (r.role == "canonical", r.role == "canonical" and r.ceilings_met),
    "ReferenceStructure": lambda r: (r.role == "reference_of_record", r.role == "reference_of_record" and r.structure_class != "REFERENCE-UNRESOLVED"),
    "StabilityAudit": lambda r: (r.role == "canonical", r.role == "canonical" and r.all_alternatives_agree),
}


# ----------------------------------------------------------------------------- 7. typed per-item records (each derives)
@dataclass(frozen=True)
class LevelListRecord:
    levels_micro: Tuple[int, ...]
    spacings_micro: Tuple[int, ...]
    max_spacing_micro: int
    w_res_micro: int
    stage_sha256: str
    result_sha256: str = ""


def level_list_record(stage: StageIdentity) -> LevelListRecord:
    lv = tuple(F8_LEVELS_MICRO); sp = tuple(b - a for a, b in zip(lv, lv[1:]))
    return LevelListRecord(lv, sp, max(sp), _C.W_RES_MICRO, stage.result_sha256, _digest((lv, sp, max(sp), _C.W_RES_MICRO, stage.result_sha256)))


def validate_level_list(r, stage=None, **ctx) -> None:
    if type(r) is not LevelListRecord or r.levels_micro != tuple(F8_LEVELS_MICRO) or r.spacings_micro != tuple(b - a for a, b in zip(r.levels_micro, r.levels_micro[1:])) or r.max_spacing_micro != max(r.spacings_micro) or r.max_spacing_micro != _C.S_P1_MAX_MICRO or r.w_res_micro != _C.W_RES_MICRO:
        raise RunnerDomainError("level list does not derive from the frozen levels")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("level list belongs to a different stage")
    if r.result_sha256 != _digest((r.levels_micro, r.spacings_micro, r.max_spacing_micro, r.w_res_micro, r.stage_sha256)): raise RunnerDomainError("level list identity does not recompute")


@dataclass(frozen=True)
class EnsembleSizesRecord:
    production_runs: int
    morphology_sweeps_per_class: int
    design_stability_sweeps: int
    dense_points: int
    known_answer_sweeps: int
    pricing_replicates: int
    panel_n: int
    stage_sha256: str
    result_sha256: str = ""


def _sizes() -> Tuple: return (PRODUCTION_RUNS, _A.SWEEPS_PER_CLASS, _CL.DESIGN_STABILITY_SWEEPS, _CL.DENSE_POINTS, _E.KNOWN_ANSWER_SWEEPS, _A.PRICING_REPLICATES, _CL.PANEL_N)


def ensemble_sizes_record(stage: StageIdentity) -> EnsembleSizesRecord:
    v = _sizes(); return EnsembleSizesRecord(*v, stage.result_sha256, _digest((v, stage.result_sha256)))


def validate_ensemble_sizes(r, stage=None, **ctx) -> None:
    if type(r) is not EnsembleSizesRecord or (r.production_runs, r.morphology_sweeps_per_class, r.design_stability_sweeps, r.dense_points, r.known_answer_sweeps, r.pricing_replicates, r.panel_n) != _sizes(): raise RunnerDomainError("ensemble sizes differ from the declared programs")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("ensemble sizes belong to a different stage")
    if r.result_sha256 != _digest((_sizes(), r.stage_sha256)): raise RunnerDomainError("ensemble sizes identity does not recompute")


@dataclass(frozen=True)
class ClosurePublicationRecord:
    """M5's closure publication (replayed) bound to Appendix A of record through M5's verifier on the committed file (bind tolerance; the
    machine's deviation recorded, Interpretation of M5-6)."""
    publication_sha256: str
    appendix_a_sha256: str
    bind_tol: float
    max_abs_deviation: float
    bit_equal: bool
    delta_m: float
    m_infl: float
    m_lat: float
    stage_sha256: str
    result_sha256: str = ""


def _closure_facts(repo_root: str) -> Tuple:
    pub = _CL.closure_publication(); _CL.validate_closure_publication(pub)
    v = _CL.verify_against_appendix_a(os.path.join(repo_root, CONTRACT_RECORDS[2][0]))
    return (pub.result_sha256, v["appendix_a_sha256"], float(v["bind_tol"]), float(v["max_abs_deviation"]), bool(v["bit_equal"]), float(v["delta_m"]), float(v["m_infl"]), float(v["m_lat"]))


def closure_publication_record(stage: StageIdentity, repo_root: str) -> ClosurePublicationRecord:
    f = _closure_facts(repo_root); return ClosurePublicationRecord(*f, stage.result_sha256, _digest((f, stage.result_sha256)))


def validate_closure_publication_record(r, stage=None, repo_root=None, **ctx) -> None:
    if type(r) is not ClosurePublicationRecord or repo_root is None: raise RunnerDomainError("exact ClosurePublicationRecord and the repository required")
    f = _closure_facts(repo_root)
    if (r.publication_sha256, r.appendix_a_sha256, r.bind_tol, r.max_abs_deviation, r.bit_equal, r.delta_m, r.m_infl, r.m_lat) != f: raise RunnerDomainError("closure publication record does not re-derive through M5 on this machine")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("closure publication belongs to a different stage")
    if r.result_sha256 != _digest((f, r.stage_sha256)): raise RunnerDomainError("closure publication identity does not recompute")


@dataclass(frozen=True)
class NullLawRecord:
    """M3's level-independent law as this machine certifies it: the two indices (platform-independent), modes, certificate bound, the
    payload identity (platform-sensitive, recorded), the attempt-2 protocol identity and the familywise construction bound."""
    index_p: int
    index_t: int
    mode_p: str
    mode_t: str
    error_bound: float
    payload_identity: str
    protocol_sha256: str
    construction_bound: float
    stage_sha256: str
    result_sha256: str = ""


def _null_facts() -> Tuple:
    th = _N.null_thresholds(F8_LEVELS_MICRO[0])
    return (th.theta_p_certificate.index, th.theta_t_certificate.index, th.theta_p_certificate.mode, th.theta_t_certificate.mode, float(th.theta_p_certificate.error_bound), th.payload_identity(),
            _N.VALIDATION_PROTOCOL_ATTEMPT_2_SHA256_LITERAL, float(_N.familywise_nominal_bound(th)))


def null_law_record(stage: StageIdentity) -> NullLawRecord:
    f = _null_facts(); return NullLawRecord(*f, stage.result_sha256, _digest((f, stage.result_sha256)))


def validate_null_law(r, stage=None, **ctx) -> None:
    if type(r) is not NullLawRecord: raise RunnerDomainError("exact NullLawRecord required")
    f = _null_facts()
    if (r.index_p, r.index_t, r.mode_p, r.mode_t, r.error_bound, r.payload_identity, r.protocol_sha256, r.construction_bound) != f: raise RunnerDomainError("null law record does not re-derive through M3 on this machine")
    if (r.index_p, r.index_t) != (14341, 14121): raise RunnerDomainError("null law indices differ from the certified values")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("null law belongs to a different stage")
    if r.result_sha256 != _digest((f, r.stage_sha256)): raise RunnerDomainError("null law identity does not recompute")


@dataclass(frozen=True)
class RouterCollisionRecord:
    reachable_cases: int
    reachable_colliding: int
    colliding_band_spacings: Tuple[int, ...]
    reachable_pass2_levels: int
    fallback_reachable: bool
    stage_sha256: str
    result_sha256: str = ""


def _router_facts() -> Tuple:
    a = _V.collision_audit()
    return (a.reachable_cases_checked, a.reachable_colliding, tuple(a.colliding_band_spacings), len(_A.reachable_pass2_levels()), bool(a.fallback_reachable))


def router_collision_record(stage: StageIdentity) -> RouterCollisionRecord:
    f = _router_facts(); return RouterCollisionRecord(*f, stage.result_sha256, _digest((f, stage.result_sha256)))


def validate_router_collision(r, stage=None, **ctx) -> None:
    if type(r) is not RouterCollisionRecord or (r.reachable_cases, r.reachable_colliding, r.colliding_band_spacings, r.reachable_pass2_levels, r.fallback_reachable) != _router_facts(): raise RunnerDomainError("router collision facts do not re-derive from M4/M6")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("router record belongs to a different stage")
    if r.result_sha256 != _digest((_router_facts(), r.stage_sha256)): raise RunnerDomainError("router record identity does not recompute")


@dataclass(frozen=True)
class ConformanceRecord:
    """M1 determinism on this platform at the declared shape: one realization run's spec hash and trace identity, re-executed by the validator."""
    level_micro: int
    seed: int
    grid: int
    ticks: int
    spec_hash: str
    rho_sha256: str
    draws_consumed: int
    passed: bool
    stage_sha256: str
    result_sha256: str = ""


def _conformance_facts(level_micro: int, seed: int, grid: int, ticks: int) -> Tuple:
    spec = _C.f8_run_spec(level_micro, seed, "realization", grid=grid, ticks=ticks)
    r1 = _D.run(spec); r2 = _D.run(spec)
    return (spec.spec_hash(), r1.rho_sha256(), int(r1.draws_consumed), bool(r1.rho_sha256() == r2.rho_sha256() and r1.draws_consumed == r2.draws_consumed))


def conformance_record(stage: StageIdentity, *, level_micro: int = BENCHMARK_LEVEL_MICRO, seed: int = F8_SEED_PANEL[0], grid: int = F8_GRID, ticks: int = F8_TICKS) -> ConformanceRecord:
    f = _conformance_facts(level_micro, seed, grid, ticks)
    body = (int(level_micro), int(seed), grid, ticks) + f + (stage.result_sha256,)
    return ConformanceRecord(*body, _digest(body))


def validate_conformance_record(r, stage=None, **ctx) -> None:
    if type(r) is not ConformanceRecord or not _is_hex(r.spec_hash, 64) or not _is_hex(r.rho_sha256, 64) or r.seed not in F8_SEED_PANEL: raise RunnerDomainError("conformance record malformed")
    if (r.spec_hash, r.rho_sha256, r.draws_consumed, r.passed) != _conformance_facts(r.level_micro, r.seed, r.grid, r.ticks): raise RunnerDomainError("conformance facts do not reproduce by re-execution on this platform")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("conformance record belongs to a different stage")
    if r.result_sha256 != _digest((r.level_micro, r.seed, r.grid, r.ticks, r.spec_hash, r.rho_sha256, r.draws_consumed, r.passed, r.stage_sha256)): raise RunnerDomainError("conformance record identity does not recompute")


@dataclass(frozen=True)
class MorphologyRecord:
    """The realization census's M4 morphology (contract s7.3 item 3; s4.9: secondary, never bears on P1): the 24 pass-1 labels from the
    authorized realization LevelRecords, M4's verdict on the pass-1 set, the router's decision, and the EVALUABILITY HALT for every requested
    insertion (M1's frozen guard cannot execute production-shape runs off the pass-1 grid), so the verdict of record is the pass-1 verdict with
    that scope stated. The s1.3(a) expectation (rule 2, no_null_consistent_phase) is compared descriptively."""
    pass1_records: Tuple[Tuple[int, str, str], ...]   # (level, file sha256, record identity)
    pass1_labels: Tuple[str, ...]
    verdict: str
    cause: Optional[str]
    rule: str
    router_row: str
    insertions_micro: Tuple[int, ...]
    fallback_moves: Tuple[Tuple[int, int], ...]
    fallback_drops: Tuple[int, ...]
    insertion_halts: Tuple[Tuple[int, str], ...]
    verdict_scope: str                                  # ALWAYS "pass-1 level set" (Interpretation 003 pt 1): the record never writes "final level set"
    final_set_identical_to_pass1: bool                  # True iff the router requested no insertion: the pass-1 verdict IS the final-level-set verdict
    final_set_obligation: str                           # "discharged_identically" | "open" (Interpretation 003 pt 2; s4.4's final-set obligation is never discharged by an insertion-requesting pass-1 report)
    matches_expectation: bool                           # verdict NOT_PRODUCED / no_null_consistent_phase (s1.3(a), s4.9), descriptive
    adapter_body_sha256: str
    stage_sha256: str
    result_sha256: str = ""


_MORPH_FIELDS = tuple(f.name for f in dataclasses.fields(MorphologyRecord) if f.name != "result_sha256")
def _morph_body(r) -> Tuple: return tuple(getattr(r, k) for k in _MORPH_FIELDS)


def _morphology_from_rows(rows, labels, adapter_body, stage_sha) -> MorphologyRecord:
    v = _V.evaluate(labels, F8_LEVELS_MICRO); d = route(labels, F8_LEVELS_MICRO)
    ins = tuple(int(x) for x in d.insertions_micro)
    halts = tuple((m, f"evaluability:M1 production guard: level {m} is off the pass-1 grid") for m in ins)
    body = dict(pass1_records=rows, pass1_labels=tuple(labels), verdict=v.verdict, cause=v.cause, rule=v.rule, router_row=d.row, insertions_micro=ins, fallback_moves=tuple(d.fallback_moves),
                fallback_drops=tuple(d.fallback_drops), insertion_halts=halts, verdict_scope="pass-1 level set", final_set_identical_to_pass1=(not ins), final_set_obligation="discharged_identically" if not ins else "open",
                matches_expectation=(v.verdict, v.cause) == ("NOT_PRODUCED", "no_null_consistent_phase"),
                adapter_body_sha256=adapter_body, stage_sha256=stage_sha)
    return MorphologyRecord(**body, result_sha256=_digest(_morph_body(MorphologyRecord(**body))))


def validate_morphology(r, stage=None, repo_root=None, pinned_root=None, records_dir: Optional[str] = None, adapter=None, **ctx) -> None:
    if type(r) is not MorphologyRecord or len(r.pass1_labels) != len(F8_LEVELS_MICRO) or tuple(m for m, _, _ in r.pass1_records) != tuple(F8_LEVELS_MICRO): raise RunnerDomainError("morphology record must cover exactly the pass-1 grid")
    if r.verdict_scope != "pass-1 level set" or r.final_set_obligation not in ("discharged_identically", "open"): raise RunnerDomainError("morphology scope is the pass-1 level set (Interpretation 003 pt 1-2)")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("morphology record belongs to a different stage")
    if records_dir is None or adapter is None or stage is None or repo_root is None: raise RunnerDomainError("a MorphologyRecord validates only with its stage, repository, records directory and the production adapter (full replay)")
    labels = []
    for (m, fsha, rid) in r.pass1_records:
        fp = os.path.join(records_dir, _level_file(m, "realization", "canonical"))
        if not os.path.isfile(fp) or _sha_file(fp) != fsha: raise RunnerDomainError(f"realization level record for {level_id(m)} absent or not the named identity")
        rec, _ = load_record(fp, "LevelRecord", stage, repo_root, pinned_root, require_job="realization_census", level_dir=os.path.join(records_dir, _level_dirname(m, "realization", "canonical")), adapter=adapter, records_dir=records_dir)
        require_level_slot(rec, m, "realization", "canonical", "realization_census")                       # L2 r1 D4c: the loaded record must BE this slot's record
        if rec.result_sha256 != rid: raise RunnerDomainError("level record identity differs")
        labels.append(rec.label)
    if _morphology_from_rows(r.pass1_records, tuple(labels), adapter.body_sha256, r.stage_sha256) != r: raise RunnerDomainError("morphology record does not re-derive from the level records through M4")


@dataclass(frozen=True)
class StabilitySweep:
    """M7's wrapper for a sweep assembled from the STABILITY panel's authorized LevelRecords (Interpretation 003 pt 7): M-P1's SweepRecord
    inside carries M-P1's own non-canonical role `synthetic` (its alphabet is canonical|synthetic; M7 adds no role to a placed module) and
    replays from the level records exactly as a canonical sweep does, with the spec reconstructed on the stability panel. Never enters P1."""
    obj: str
    panel: str                                          # "stability"
    stability_master: int
    sweep: _E.SweepRecord                               # M-P1 role `synthetic` (its alphabet): a synthetic LevelData carries no run provenance, so it travels here instead
    level_records: Tuple[Tuple[int, str, str], ...]     # (level, file sha256, record identity) of the stability-panel LevelRecords
    run_provenance: Tuple[Tuple[int, Tuple[str, ...], Tuple[str, ...]], ...]   # per level: the 20 run spec hashes and trace identities, in panel order
    stage_sha256: str
    result_sha256: str = ""


_SSW_FIELDS = tuple(f.name for f in dataclasses.fields(StabilitySweep) if f.name != "result_sha256")
def _ssw_body(r) -> Tuple: return tuple(getattr(r, k) for k in _SSW_FIELDS)


@dataclass(frozen=True)
class StabilityRecord:
    """s7.3 items 2 and 4 (Interpretation 003 pt 8): the canonical result reproduced on the INDEPENDENT stability seed panel of the same
    object. Skeleton: T-S1' on both sweeps gives the SAME crossing-interval index, or both return the same non-PASS outcome and cause
    (I003 pt 8; the separation and delta_m fields are descriptive only — adjacent indices are NOT a reproduction, L2 r2 R2-5). Realization: T-R1' (against the calibration census bands) gives the same outcome and cause. M-P1's own
    test functions score both sweeps; the reproduction is an instrument statement and never enters P1."""
    obj: str                                            # skeleton_high | realization
    canonical_sweep_sha256: str
    stability_sweep_sha256: str                         # the persisted StabilitySweep's identity
    census_sha256: str
    canonical_outcome: str
    canonical_cause: Optional[str]
    canonical_m_hat_c: Optional[str]
    alternative_outcome: str
    alternative_cause: Optional[str]
    alternative_m_hat_c: Optional[str]
    delta_m: float
    separation: Optional[float]
    reproduced: bool
    stage_sha256: str
    result_sha256: str = ""


_STAB_FIELDS = tuple(f.name for f in dataclasses.fields(StabilityRecord) if f.name != "result_sha256")
def _stab_body(r) -> Tuple: return tuple(getattr(r, k) for k in _STAB_FIELDS)


def _sweep_from_level_records(obj: str, results_by_level, halts_by_level, panel: str):
    """A sweep assembled by M7 from M1 results of a panel for scoring by M-P1's test functions. Canonical panel: M-P1's own builder.
    Stability panel: the same observation recomputation (D3) with the spec reconstructed on the stability panel; M-P1 role `synthetic`
    (which by M-P1's grammar carries no per-run provenance inside the LevelData) — returns (SweepRecord, run_provenance rows)."""
    if panel == "canonical": return _E.sweep_from_results(obj, results_by_level, halts_by_level)
    if panel != "stability": raise RunnerDomainError("sweeps are assembled from the canonical or the stability panel only (the calibration panel is never scored)")
    seeds = _panel_seeds(panel); levels = []; prov = []
    for u in F8_LEVELS_MICRO:
        if u in halts_by_level: levels.append(_E.LevelData(u, (), (), True, halts_by_level[u], (), ())); prov.append((u, (), ())); continue
        by = {}
        for r in results_by_level[u]:
            spec = _C.f8_run_spec(u, r.seed, obj, panel=panel)
            if r.spec_hash != spec.spec_hash(): raise RunnerDomainError("stability-panel spec hash does not reconstruct")
            surv, rho_hat, wins = _E.observation_from_result(r, spec)
            if (bool(r.survival), float(r.rho_tail_mean), tuple(r.tail_window_means)) != (surv, rho_hat, wins): raise RunnerDomainError("stability run summary does not recompute")
            by[r.seed] = r
        if set(by) != set(seeds): raise RunnerDomainError("stability level does not carry exactly the stability panel's seeds")
        ordered = [by[sd] for sd in seeds]
        levels.append(_E.LevelData(u, tuple(bool(r.survival) for r in ordered), tuple(float(r.rho_tail_mean) for r in ordered), False, "", (), ()))
        prov.append((u, tuple(r.spec_hash for r in ordered), tuple(r.rho_sha256() for r in ordered)))
    rec = _E.SweepRecord(obj, "synthetic", tuple(levels), _E.EVALUATOR_SHA256_LITERAL)
    return dataclasses.replace(rec, result_sha256=rec.identity()), tuple(prov)


def _stability_sweep_from_records(obj: str, records_dir: str, stage, repo_root, pinned_root, adapter) -> StabilitySweep:
    results, halts, rows = _load_level_results(records_dir, obj, "stability", stage, repo_root, pinned_root, adapter)
    sw, prov = _sweep_from_level_records(obj, results, halts, "stability")
    body = dict(obj=obj, panel="stability", stability_master=stability_master(), sweep=sw, level_records=rows, run_provenance=prov, stage_sha256=stage.result_sha256)
    return StabilitySweep(**body, result_sha256=_digest(_ssw_body(StabilitySweep(**body))))


def validate_stability_sweep(r, stage=None, repo_root=None, pinned_root=None, records_dir: Optional[str] = None, adapter=None, **ctx) -> None:
    if type(r) is not StabilitySweep or r.obj not in ("skeleton_high", "realization") or r.panel != "stability" or type(r.sweep) is not _E.SweepRecord or r.sweep.role != "synthetic" or r.sweep.obj != r.obj: raise RunnerDomainError("exact StabilitySweep of a stability object required")
    _E.validate_sweep_record(r.sweep)
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("stability sweep belongs to a different stage")
    if records_dir is None or stage is None or repo_root is None or adapter is None: raise RunnerDomainError("a StabilitySweep validates only by replay from its stability-panel level records")
    if _stability_sweep_from_records(r.obj, records_dir, stage, repo_root, pinned_root, adapter) != r: raise RunnerDomainError("stability sweep does not replay from the stability-panel level records")


def _stability_from(obj: str, canonical_sweep: _E.SweepRecord, ssw: StabilitySweep, census, delta_m: float, stage_sha: str) -> StabilityRecord:
    alt_sweep = ssw.sweep
    if obj == "skeleton_high":
        r_c, c = _E.t_s1_prime(canonical_sweep); r_a, a = _E.t_s1_prime(alt_sweep)
        mc = level_id(F8_LEVELS_MICRO[c]) if c is not None else None; ma = level_id(F8_LEVELS_MICRO[a]) if a is not None else None
        sep = abs(_CL.level_m(F8_LEVELS_MICRO[a]) - _CL.level_m(F8_LEVELS_MICRO[c])) if (a is not None and c is not None) else None
        rep = (c is not None and a is not None and c == a) or (c is None and a is None and (r_c.outcome, r_c.cause) == (r_a.outcome, r_a.cause))   # I003 pt 8: the SAME crossing-interval index (L2 r2 R2-5); separation is descriptive
    elif obj == "realization":
        r_c = _E.t_r1_prime(canonical_sweep, census); r_a = _E.t_r1_prime(alt_sweep, census); mc = ma = None; sep = None
        rep = (r_c.outcome, r_c.cause) == (r_a.outcome, r_a.cause)
    else: raise RunnerDomainError("stability is defined for skeleton_high and realization")
    body = dict(obj=obj, canonical_sweep_sha256=canonical_sweep.result_sha256, stability_sweep_sha256=ssw.result_sha256, census_sha256=census.result_sha256, canonical_outcome=r_c.outcome, canonical_cause=r_c.cause,
                canonical_m_hat_c=mc, alternative_outcome=r_a.outcome, alternative_cause=r_a.cause, alternative_m_hat_c=ma, delta_m=float(delta_m), separation=sep, reproduced=bool(rep), stage_sha256=stage_sha)
    return StabilityRecord(**body, result_sha256=_digest(_stab_body(StabilityRecord(**body))))


def validate_stability_record(r, stage=None, repo_root=None, pinned_root=None, records_dir: Optional[str] = None, canonical_sweep=None, stability_sweep=None, census=None, adapter=None, **ctx) -> None:
    if type(r) is not StabilityRecord or r.obj not in ("skeleton_high", "realization"): raise RunnerDomainError("exact StabilityRecord required")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("stability record belongs to a different stage")
    if canonical_sweep is None or stability_sweep is None or census is None or stage is None: raise RunnerDomainError("a StabilityRecord validates only with its canonical sweep, its stability sweep and the census")
    if canonical_sweep.result_sha256 != r.canonical_sweep_sha256 or canonical_sweep.obj != r.obj or canonical_sweep.role != "canonical": raise RunnerDomainError("stability record names a different canonical sweep")
    if type(stability_sweep) is not StabilitySweep or stability_sweep.result_sha256 != r.stability_sweep_sha256 or stability_sweep.obj != r.obj: raise RunnerDomainError("stability record names a different stability sweep")
    if census.result_sha256 != r.census_sha256 or census.role != "canonical": raise RunnerDomainError("stability record names a different census")
    if _stability_from(r.obj, canonical_sweep, stability_sweep, census, _CL.closure_publication().delta_m.value, r.stage_sha256) != r: raise RunnerDomainError("stability record does not re-derive")


# ---------------- skeleton assessment (s7.3 item 1: evaluated when job 1 completes, BEFORE realization runs; L2 r1 D3c)
@dataclass(frozen=True)
class SkeletonAssessment:
    """Job 1's assessment of record: T-S1', T-S1c and T-S2 on the two skeleton sweeps against the canonical census, with the skeleton fidelity
    facts (i)-(ii): m_hat_c - 1 and m_hat_c - m_lat, and the per-level skeleton fidelity rows above the boundary. Derived by M-P1's own test
    functions; a replaying validator. The realization census REQUIRES this record (and the skeleton stability record) to exist, authorized."""
    skeleton_high_sweep_sha256: str
    skeleton_low_sweep_sha256: str
    census_sha256: str
    closure_publication_sha256: str
    t_s1_prime: _E.TestResult
    t_s1c: Optional[_E.TestResult]
    t_s2: Optional[_E.TestResult]
    m_hat_c: Optional[str]
    m_hat_c_minus_one: Optional[float]
    m_hat_c_minus_m_lat: Optional[float]
    skeleton_fidelity_rows: Tuple[Tuple, ...]
    complete: bool
    stage_sha256: str
    result_sha256: str = ""


_SKA_FIELDS = tuple(f.name for f in dataclasses.fields(SkeletonAssessment) if f.name != "result_sha256")
def _ska_body(r) -> Tuple: return tuple(getattr(r, k) for k in _SKA_FIELDS)


def _skeleton_assessment(sh: _E.SweepRecord, sl: _E.SweepRecord, census, stage_sha: str) -> SkeletonAssessment:
    pub = _CL.closure_publication(); _CL.validate_closure_publication(pub); dm = pub.delta_m.value
    r1, c = _E.t_s1_prime(sh)
    r1c = _E.t_s1c(sh, census, c) if c is not None else None
    r2 = _E.t_s2(sl, c, dm) if c is not None else None
    m_c = _CL.level_m(F8_LEVELS_MICRO[c]) if c is not None else None
    rows = []
    if c is not None:
        for i, u in enumerate(F8_LEVELS_MICRO):
            if i >= c and not sh.levels[i].unevaluable:
                med = sh.levels[i].med; rows.append((level_id(u), med, pub.rho_sk[i], pub.pair_sk[i], _CL.fidelity_band(census, i), med - pub.rho_sk[i], med - pub.pair_sk[i]))
    body = dict(skeleton_high_sweep_sha256=sh.result_sha256, skeleton_low_sweep_sha256=sl.result_sha256, census_sha256=census.result_sha256, closure_publication_sha256=pub.result_sha256,
                t_s1_prime=r1, t_s1c=r1c, t_s2=r2, m_hat_c=level_id(F8_LEVELS_MICRO[c]) if c is not None else None, m_hat_c_minus_one=(m_c - 1.0) if m_c is not None else None,
                m_hat_c_minus_m_lat=(m_c - pub.m_lat) if m_c is not None else None, skeleton_fidelity_rows=tuple(rows), complete=True, stage_sha256=stage_sha)
    return SkeletonAssessment(**body, result_sha256=_digest(_ska_body(SkeletonAssessment(**body))))


def validate_skeleton_assessment(r, stage=None, skeleton_high=None, skeleton_low=None, census=None, **ctx) -> None:
    if type(r) is not SkeletonAssessment: raise RunnerDomainError("exact SkeletonAssessment required")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("skeleton assessment belongs to a different stage")
    if skeleton_high is None or skeleton_low is None or census is None or stage is None: raise RunnerDomainError("a SkeletonAssessment validates only with its two sweeps and the census")
    if (skeleton_high.result_sha256, skeleton_low.result_sha256, census.result_sha256) != (r.skeleton_high_sweep_sha256, r.skeleton_low_sweep_sha256, r.census_sha256) or (skeleton_high.obj, skeleton_low.obj, skeleton_high.role, skeleton_low.role, census.role) != ("skeleton_high", "skeleton_low", "canonical", "canonical", "canonical"):
        raise RunnerDomainError("skeleton assessment names different inputs")
    if _skeleton_assessment(skeleton_high, skeleton_low, census, r.stage_sha256) != r: raise RunnerDomainError("skeleton assessment does not replay through M-P1's tests")


# ---------------- tolerance ensembles (M5-5: a record kind SEPARATE from the program; L2 r1 D5b)
@dataclass(frozen=True)
class ToleranceEnsembles:
    """The 24 per-level ToleranceEnsemble records of M5 (`closure.tolerance_ensembles`), retained and persisted as ONE typed collection whose
    validator replays every level's ensemble from the canonical census (M5-5 keeps `tolerance_ensembles` and `tolerance_program` separate)."""
    census_sha256: str
    ensembles: Tuple[_CL.ToleranceEnsemble, ...]
    complete: bool
    stage_sha256: str
    result_sha256: str = ""


def _tol_body(r) -> Tuple: return (r.census_sha256, tuple(dataclasses.astuple(e) for e in r.ensembles), r.complete, r.stage_sha256)


def tolerance_ensembles_record(census, stage_sha: str) -> ToleranceEnsembles:
    ens = _CL.tolerance_ensembles(census)
    body = dict(census_sha256=census.result_sha256, ensembles=ens, complete=(len(ens) == len(F8_LEVELS_MICRO) and tuple(e.level_micro for e in ens) == tuple(F8_LEVELS_MICRO)), stage_sha256=stage_sha)
    return ToleranceEnsembles(**body, result_sha256=_digest(_tol_body(ToleranceEnsembles(**body))))


def validate_tolerance_ensembles(r, stage=None, census=None, **ctx) -> None:
    if type(r) is not ToleranceEnsembles or any(type(e) is not _CL.ToleranceEnsemble for e in r.ensembles): raise RunnerDomainError("exact ToleranceEnsembles of M5 ToleranceEnsemble records required")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("tolerance ensembles belong to a different stage")
    if census is None or stage is None or census.role != "canonical" or census.result_sha256 != r.census_sha256: raise RunnerDomainError("tolerance ensembles validate only against their canonical census")
    if tolerance_ensembles_record(census, r.stage_sha256) != r: raise RunnerDomainError("tolerance ensembles do not replay from the census through M5")


# ----------------------------------------------------------------------------- 8. job graph, specification, package (E1 M7 mechanics carried; F8 jobs)
JOB_GRAPH: Tuple[Tuple[str, Tuple[Tuple[str, str], ...], Tuple[str, ...]], ...] = (
    ("mp1_known_answer", (("KnownAnswerQualification", "mp1_known_answer.json"),), ()),
    ("m6_design_audit", (("AuditRecord", "m6_design_audit.json"),), ("mp1_known_answer",)),                           # s7.1 order (L2 r1 D3d)
    ("m6_held_out_audit", (("AuditRecord", "m6_held_out_audit.json"),), ("m6_design_audit",)),
    ("m6_audit_qualification", (("AuditQualification", "m6_audit_qualification.json"),), ("m6_design_audit", "m6_held_out_audit")),
    ("m6_price", (("PricingRecord", "m6_price.json"),), ()),
    ("calibration_census", (("CalibrationCensus", "calibration_census.json"),), ()),
    ("tolerance_program", (("ToleranceProgram", "tolerance_program.json"), ("ToleranceEnsembles", "tolerance_ensembles.json")), ("calibration_census",)),
    ("dense_reference", (("ReferenceStructure", "dense_reference.json"),), ()),
    ("reference_stability", (("StabilityAudit", "reference_stability.json"),), ("dense_reference",)),
    ("projection_sweeps", (("DesignStability", "projection_sweeps.json"), ("SweepEnsemble", "projection_sweeps.ensemble.json")), ("dense_reference",)),
    ("skeleton_census", (("SweepRecord", "skeleton_high_sweep.json"), ("SweepRecord", "skeleton_low_sweep.json"), ("SkeletonAssessment", "skeleton_assessment.json")), ("calibration_census",)),
    ("skeleton_stability", (("StabilitySweep", "skeleton_stability_sweep.json"), ("StabilityRecord", "skeleton_stability.json")), ("skeleton_census", "calibration_census")),
    ("realization_census", (("SweepRecord", "realization_sweep.json"), ("MorphologyRecord", "realization_morphology.json")), ("skeleton_census", "skeleton_stability", "calibration_census")),   # s7.3: skeleton result known BEFORE realization runs (L2 r1 D3b)
    ("realization_stability", (("StabilitySweep", "realization_stability_sweep.json"), ("StabilityRecord", "realization_stability.json")), ("realization_census", "calibration_census")),
    ("p1_evaluation", (("P1Evaluation", "p1_evaluation.json"),), ("skeleton_census", "realization_census", "calibration_census")),
    ("resource_benchmark", (("ResourceBenchmark", "resource_benchmark.json"),), ()),
    ("stage1_package", (("StagePackage", "stage1_package.json"),), ()),
)
DERIVED_TYPES = ("LevelListRecord", "EnsembleSizesRecord", "ClosurePublicationRecord", "NullLawRecord", "RouterCollisionRecord", "ConformanceRecord")
DEPENDENCY_SCHEMA = {
    "StabilityAudit": (("primary", "ReferenceStructure"),),
    "DesignStability": (("ref", "ReferenceStructure"), ("sweeps", "SweepEnsemble")),
    "AuditQualification": (("design", "AuditRecord"), ("held_out", "AuditRecord")),
    "ToleranceProgram": (("census", "CalibrationCensus"),),
    "StabilityRecord": (("canonical_sweep", "SweepRecord"), ("stability_sweep", "StabilitySweep"), ("census", "CalibrationCensus")),
    "SkeletonAssessment": (("skeleton_high", "SweepRecord"), ("skeleton_low", "SweepRecord"), ("census", "CalibrationCensus")),
    "ToleranceEnsembles": (("census", "CalibrationCensus"),),
    "P1Evaluation": (("skeleton_high", "SweepRecord"), ("skeleton_low", "SweepRecord"), ("realization", "SweepRecord"), ("census", "CalibrationCensus")),
}
SWEEP_FILES = {"skeleton_high": "skeleton_high_sweep.json", "skeleton_low": "skeleton_low_sweep.json", "realization": "realization_sweep.json"}
STABILITY_SWEEP_FILES = {"skeleton_high": "skeleton_stability_sweep.json", "realization": "realization_stability_sweep.json"}
MULTI_OUTPUT_FILES = {"SweepRecord": ("skeleton_high_sweep", "skeleton_low_sweep", "realization_sweep"), "StabilitySweep": ("skeleton_stability_sweep", "realization_stability_sweep")}


def _job_outputs(job: str) -> Tuple[Tuple[str, str], ...]:
    for j, outs, _ in JOB_GRAPH:
        if j == job: return outs
    raise RunnerDomainError(f"{job!r} is not in the job graph")


def _item_file(item) -> str:
    if item.producer_job == "derived": return f"derived.{item.name}.json"
    if item.record_type in MULTI_OUTPUT_FILES:
        if item.name not in MULTI_OUTPUT_FILES[item.record_type]: raise RunnerDomainError(f"item {item.name}: a {item.record_type} item must be one of {MULTI_OUTPUT_FILES[item.record_type]}")
        return f"{item.name}.json"
    for typ, fname in _job_outputs(item.producer_job):
        if typ == item.record_type and "{" not in fname: return fname
    raise RunnerDomainError(f"item {item.name}: producer {item.producer_job} has no single output of type {item.record_type}")


@dataclass(frozen=True)
class PackageItem:
    name: str
    record_type: str
    producer_job: str
    complete_predicate: str
    pass_predicate: str
    dependencies: Tuple[Tuple[str, str], ...]


@dataclass(frozen=True)
class PackageSpecification:
    version: int
    governance_sha256: str
    items: Tuple[PackageItem, ...]
    result_sha256: str = ""


def _spec_body(s) -> Tuple: return (s.version, s.governance_sha256, tuple(tuple(dataclasses.astuple(i)) for i in s.items))


def validate_package_spec(s, stage=None, governance=None, governance_sha256: Optional[str] = None, **ctx) -> None:
    if type(s) is not PackageSpecification or type(s.version) is not int or s.version < 1 or not _is_hex(s.governance_sha256, 64): raise RunnerDomainError("package specification malformed")
    if type(s.items) is not tuple or not s.items: raise RunnerDomainError("package specification has no items")
    by = {}
    for i in s.items:
        if type(i) is not PackageItem: raise RunnerDomainError("package items must be PackageItem records")
        if i.name in by: raise RunnerDomainError("package item names must be unique")
        by[i.name] = i
    if governance is not None:
        if type(governance) is not F8Governance or (governance_sha256 is not None and s.governance_sha256 != governance_sha256): raise RunnerDomainError("specification names a different governance record")
        unknown = set(by) - set(governance.package_item_vocabulary)
        if unknown: raise RunnerDomainError(f"item names outside the governance vocabulary: {sorted(unknown)}")
        missing = set(governance.required_package_items) - set(by)
        if missing: raise RunnerDomainError(f"governance-required items missing from the specification: {sorted(missing)}")
        for item, pid in governance.branch_stopping:
            if pid not in PREDICATES or PREDICATES[pid][0] not in ("*", PREREQ_TYPES[item]): raise RunnerDomainError(f"branch-stop predicate {pid} does not apply to {item} ({PREREQ_TYPES[item]})")
    for i in s.items:
        if i.record_type not in RECORD_TYPES or i.record_type not in VALIDATORS: raise RunnerDomainError(f"item {i.name}: unknown record type {i.record_type}")
        if i.producer_job == "derived":
            if i.record_type not in DERIVED_TYPES: raise RunnerDomainError(f"item {i.name}: type {i.record_type} is not derivable")
        else:
            if i.record_type not in [typ for typ, _ in _job_outputs(i.producer_job)]: raise RunnerDomainError(f"item {i.name}: producer {i.producer_job} does not output {i.record_type}")
            _item_file(i)
        for pid in (i.complete_predicate, i.pass_predicate):
            if pid not in PREDICATES: raise RunnerDomainError(f"item {i.name}: unknown predicate {pid}")
            if PREDICATES[pid][0] not in ("*", i.record_type): raise RunnerDomainError(f"item {i.name}: predicate {pid} does not apply to {i.record_type}")
        schema = DEPENDENCY_SCHEMA.get(i.record_type, ())
        if type(i.dependencies) is not tuple or tuple(r for r, _ in i.dependencies) != tuple(r for r, _ in schema): raise RunnerDomainError(f"item {i.name}: dependencies must be exactly the type's schema {schema}")
        if len({n for _, n in i.dependencies}) != len(i.dependencies): raise RunnerDomainError(f"item {i.name}: duplicate dependencies")
        for (role, target), (_, dtype) in zip(i.dependencies, schema):
            if target not in by or target == i.name or by[target].record_type != dtype: raise RunnerDomainError(f"item {i.name}: dependency {role} must be an item of type {dtype}")
    if stage is not None and stage.governance_sha256 is not None and s.governance_sha256 != stage.governance_sha256: raise RunnerDomainError("specification names a different governance record than the stage")
    if s.result_sha256 != _digest(_spec_body(s)): raise RunnerDomainError("package specification identity does not recompute")


def load_package_spec(repo_root: str, stage: StageIdentity) -> Tuple[PackageSpecification, str]:
    p = _gov(repo_root, PACKAGE_SPEC_REL)
    if not os.path.isfile(p) or stage.package_spec_sha256 is None: raise RunnerDomainError("no committed Package Specification is bound by this stage")
    if not _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, PACKAGE_SPEC_REL)) or _sha_file(p) != stage.package_spec_sha256: raise RunnerDomainError("the Package Specification on disk is not the committed one the stage bound")
    s = _read_canonical(p)
    if type(s) is not PackageSpecification: raise RunnerDomainError("file is not a PackageSpecification")
    gov, gsha = load_governance(repo_root, stage)
    validate_package_spec(s, stage=stage, governance=gov, governance_sha256=gsha)
    return s, stage.package_spec_sha256


PREDICATES = {
    "exists": ("*", lambda r: True),
    "reference_of_record_dense": ("ReferenceStructure", lambda r: r.role == "reference_of_record" and r.levels_micro == _CL.dense_grid_micro()),
    "reference_resolved": ("ReferenceStructure", lambda r: r.role == "reference_of_record" and r.structure_class != "REFERENCE-UNRESOLVED"),
    "stability_canonical": ("StabilityAudit", lambda r: r.role == "canonical"),
    "stability_all_agree": ("StabilityAudit", lambda r: r.role == "canonical" and r.all_alternatives_agree),
    "design_complete": ("DesignStability", lambda r: r.role == "canonical" and r.evaluable),
    "design_stable": ("DesignStability", lambda r: r.role == "canonical" and r.evaluable and bool(r.design_stable)),
    "sweep_ensemble_canonical": ("SweepEnsemble", lambda r: len(r.sweeps) == _CL.DESIGN_STABILITY_SWEEPS),
    "audit_record_complete": ("AuditRecord", lambda r: r.requested_sweeps_per_class == _A.SWEEPS_PER_CLASS and len(r.scores) == len(_A.CLASSES)
                              and all(s.attempted == s.scored == _A.SWEEPS_PER_CLASS and s.halted == 0 and s.generator_halted == 0 for s in r.scores)),
    "audit_record_pass": ("AuditRecord", lambda r: r.ensemble_pass),
    "qualification_recorded": ("AuditQualification", lambda r: True),
    "qualification_qualified": ("AuditQualification", lambda r: r.qualified),
    "known_answer_recorded": ("KnownAnswerQualification", lambda r: r.census_is_declared_synthetic and r.sweeps_per_class == _E.KNOWN_ANSWER_SWEEPS),
    "known_answer_passed": ("KnownAnswerQualification", lambda r: r.passed),
    "census_canonical": ("CalibrationCensus", lambda r: r.role == "canonical"),
    "census_ceilings_met": ("CalibrationCensus", lambda r: r.role == "canonical" and r.ceilings_met),
    "tolerance_program_recorded": ("ToleranceProgram", lambda r: True),
    "tolerance_program_complete": ("ToleranceProgram", lambda r: r.complete),
    "sweep_canonical": ("SweepRecord", lambda r: r.role == "canonical"),
    "sweep_all_evaluable": ("SweepRecord", lambda r: r.role == "canonical" and not any(l.unevaluable for l in r.levels)),
    "morphology_recorded": ("MorphologyRecord", lambda r: True),
    "morphology_pass1_evaluated": ("MorphologyRecord", lambda r: r.verdict in _V.VERDICTS and r.verdict_scope == "pass-1 level set" and len(r.insertion_halts) == len(r.insertions_micro)),
    "morphology_final_set_identical": ("MorphologyRecord", lambda r: r.final_set_identical_to_pass1 and r.final_set_obligation == "discharged_identically"),
    "sweep_stability": ("StabilitySweep", lambda r: r.panel == "stability" and r.sweep.role == "synthetic"),
    "skeleton_assessment_recorded": ("SkeletonAssessment", lambda r: True),
    "skeleton_assessment_complete": ("SkeletonAssessment", lambda r: r.complete and r.t_s1_prime.outcome in ("PASS", "FAIL", "ND")),
    "tolerance_ensembles_recorded": ("ToleranceEnsembles", lambda r: True),
    "tolerance_ensembles_complete": ("ToleranceEnsembles", lambda r: r.complete),
    "stability_record_recorded": ("StabilityRecord", lambda r: True),
    "stability_record_reproduced": ("StabilityRecord", lambda r: r.reproduced),
    "p1_recorded": ("P1Evaluation", lambda r: r.role == "canonical"),
    "p1_evaluated": ("P1Evaluation", lambda r: r.role == "canonical" and r.determination in ("PRODUCED", "NOT PRODUCED")),
    "benchmark_canonical": ("ResourceBenchmark", lambda r: r.role == "canonical"),
    "benchmark_fits": ("ResourceBenchmark", lambda r: r.role == "canonical" and r.fits_with_margin),
    "conformance_production": ("ConformanceRecord", lambda r: (r.grid, r.ticks) == (F8_GRID, F8_TICKS)),
    "conformance_production_passed": ("ConformanceRecord", lambda r: r.passed and (r.grid, r.ticks) == (F8_GRID, F8_TICKS)),
    "null_law_certified": ("NullLawRecord", lambda r: (r.index_p, r.index_t) == (14341, 14121)),
    "closure_covers_levels": ("ClosurePublicationRecord", lambda r: r.max_abs_deviation <= r.bind_tol),
    "price_recorded": ("PricingRecord", lambda r: r.replicates == _A.PRICING_REPLICATES and r.master == _A.production_masters()[2] and r.source == "m6_null_count_process"),
    "quarantine_recorded": ("TrancheQuarantine", lambda r: r.status in ("passed", "failed")),
    "quarantine_passed": ("TrancheQuarantine", lambda r: r.status == "passed"),
}


@dataclass(frozen=True)
class StagePackage:
    role: str
    stage_sha256: str
    governance_sha256: str
    package_spec_sha256: str
    authorization_version: int
    authorization_sha256: str
    authorization_file_sha256: str
    items: Tuple[Tuple[str, str, str, str, str, bool, bool], ...]
    complete: bool
    all_items_pass: bool
    result_sha256: str = ""


def _pkg_body(p) -> Tuple: return (p.role, p.stage_sha256, p.governance_sha256, p.package_spec_sha256, p.authorization_version, p.authorization_sha256, p.authorization_file_sha256, p.items, p.complete, p.all_items_pass)


def _item_identity(rec) -> str:
    return getattr(rec, "result_sha256", None) or getattr(rec, "qualification_sha256", None) or getattr(rec, "record_sha256", None) or _digest(rec)


def _eval_predicate(pid: str, rec) -> bool:
    if pid not in PREDICATES: raise RunnerDomainError(f"unknown predicate {pid}")
    applies, fn = PREDICATES[pid]
    if applies not in ("*", type(rec).__name__): raise RunnerDomainError(f"predicate {pid} does not apply to {type(rec).__name__}")
    try: return bool(fn(rec))
    except Exception as e: raise RunnerDomainError(f"predicate {pid} failed on {type(rec).__name__}: {type(e).__name__}")


def _dependency_kwargs(item, loaded: Dict[str, Any]) -> Dict[str, Any]:
    kw: Dict[str, Any] = {}
    for role, target in item.dependencies:
        rec = loaded[target]
        kw[role] = rec.sweeps if type(rec).__name__ == "SweepEnsemble" else rec   # StabilitySweep passes whole (validator reads .sweep)
    return kw


def _item_context(record_type: str, package_dir: str, adapter) -> Dict[str, Any]:
    kw: Dict[str, Any] = {}
    if record_type == "ResourceBenchmark": kw["artifact_dir"] = os.path.join(package_dir, "benchmark_artifacts")
    if record_type == "AuditRecord": kw["expect_production"] = True
    if record_type == "PricingRecord": kw["adapter"] = adapter
    if record_type in ("CalibrationCensus", "SweepRecord", "MorphologyRecord", "StabilityRecord", "StabilitySweep"): kw["records_dir"] = package_dir; kw["adapter"] = adapter
    return kw


def _assemble(spec_items, package_dir: str, stage, repo_root, pinned_root, canonical: bool, adapter, provisional_ctx: Optional[Dict[str, Dict[str, Any]]] = None):
    loaded: Dict[str, Any] = {}; rows = []; pending = list(spec_items)
    while pending:
        progress = False
        for i in list(pending):
            if all(t in loaded for _, t in i.dependencies):
                pending.remove(i); progress = True
                fname = _item_file(i); fp = os.path.join(package_dir, fname)
                if not os.path.isfile(fp): raise RunnerDomainError(f"package item {i.name} file {fname} is absent")
                kw = _dependency_kwargs(i, loaded); kw.update(_item_context(i.record_type, package_dir, adapter))
                if not canonical and provisional_ctx: kw.update(provisional_ctx.get(i.name, {}))
                if canonical: kw["require_job"] = "stage1_package" if i.producer_job == "derived" else i.producer_job
                rec, fsha = load_record(fp, i.record_type, stage, repo_root, pinned_root, **kw)
                _bind_named_output(i.record_type, fname, rec)
                loaded[i.name] = rec
                rows.append((i.name, i.record_type, fname, fsha, _item_identity(rec), _eval_predicate(i.complete_predicate, rec), _eval_predicate(i.pass_predicate, rec)))
        if not progress: raise RunnerDomainError("package dependencies are cyclic or unresolved")
    rows = tuple(rows)
    return rows, all(r[5] for r in rows), all(r[6] for r in rows)


def validate_stage_package(p, stage=None, repo_root=None, pinned_root=None, package_dir: Optional[str] = None, adapter=None, **ctx) -> None:
    if type(p) is not StagePackage or p.role not in ("canonical", "provisional"): raise RunnerDomainError("exact StagePackage required")
    if p.role == "provisional" and p.complete: raise RunnerDomainError("a provisional package can never be complete")
    if len({r[2] for r in p.items}) != len(p.items): raise RunnerDomainError("one persisted file per item")
    if stage is not None and p.stage_sha256 != stage.result_sha256: raise RunnerDomainError("package belongs to a different stage")
    if p.result_sha256 != _digest(_pkg_body(p)): raise RunnerDomainError("package identity does not recompute")
    if p.role == "canonical":
        if stage is None or repo_root is None or package_dir is None: raise RunnerDomainError("a canonical package validates only by replay: stage, repository and package directory required")
        for r in p.items:
            fp = os.path.join(package_dir, r[2])
            if not os.path.isfile(fp) or _sha_file(fp) != r[3]: raise RunnerDomainError(f"package item {r[0]} file identity differs from the carried identity")
        auth, afile = load_authorization(repo_root, stage, p.authorization_version)
        if "stage1_package" not in auth.authorized_jobs or (auth.result_sha256, afile) != (p.authorization_sha256, p.authorization_file_sha256): raise RunnerDomainError("package authorization does not reproduce from the committed record")
        spec, ssha = load_package_spec(repo_root, stage)
        if (ssha, spec.governance_sha256) != (p.package_spec_sha256, p.governance_sha256): raise RunnerDomainError("package names a different specification or governance record")
        rows, complete, allpass = _assemble(spec.items, package_dir, stage, repo_root, pinned_root, True, adapter if adapter is not None else _stage_adapter(repo_root, stage))
        if (rows, complete, allpass) != (p.items, p.complete, p.all_items_pass): raise RunnerDomainError("package does not reproduce by replay")


def _stage_adapter(repo_root: str, stage: StageIdentity):
    """The committed adapter record the stage binds, loaded through M6 (canonical role requires the platform match the stage recorded)."""
    if stage.adapter_file_sha256 is None: raise RunnerDomainError("the stage binds no adapter record")
    p = _gov(repo_root, ADAPTER_RECORD_REL)
    if _sha_file(p) != stage.adapter_file_sha256: raise RunnerDomainError("adapter record on disk differs from the stage's")
    if not stage.adapter_platform_match: raise RunnerDomainError("the committed adapter record was built on another platform: no canonical act here (stage is not canonical)")
    a = _A.adapter_from_json(open(p, "rb").read().decode("ascii"))          # M6's replaying loader: production role re-derived on THIS platform
    if a.body_sha256 != stage.adapter_body_sha256 or not _is_production_adapter(a): raise RunnerDomainError("adapter body identity differs from the stage's or is not production under M6")
    return a


def default_producer(name: str, record_type: str) -> str:
    """The producer job of a proposed item: derived types → "derived"; an item NAMED for a job that outputs the type → that job (the two M6 audits
    and the three sweeps share types); otherwise the unique job outputting the type."""
    if record_type in DERIVED_TYPES: return "derived"
    jobs = [j for j, outs, _ in JOB_GRAPH if any(o == record_type for o, _ in outs)]
    if name in jobs: return name
    named = [j for j in jobs if name.startswith(j.replace("_census", "")) or name.startswith(j)]
    if len(jobs) == 1: return jobs[0]
    if len(named) == 1: return named[0]
    raise RunnerDomainError(f"item {name}: no unique producer for {record_type} among {jobs}")


def assemble_package_provisional(package_dir: str, stage: StageIdentity, repo_root: str, pinned_root: Optional[str] = None, contexts: Optional[Dict[str, Dict[str, Any]]] = None, adapter=None) -> StagePackage:
    verify_frozen_identity()
    items = tuple(PackageItem(n, ty, default_producer(n, ty), "exists", "exists", ()) for n, ty in PACKAGE_ITEMS)
    rows, _, allpass = _assemble(items, package_dir, stage, repo_root, pinned_root, False, adapter, contexts)
    body = ("provisional", stage.result_sha256, "", "", 0, "", "", rows, False, allpass)
    return StagePackage(*body, _digest(body))


def _produce_derived(item, stage, repo_root) -> Any:
    t = item.record_type
    if t == "LevelListRecord": return level_list_record(stage)
    if t == "EnsembleSizesRecord": return ensemble_sizes_record(stage)
    if t == "ClosurePublicationRecord": return closure_publication_record(stage, repo_root)
    if t == "NullLawRecord": return null_law_record(stage)
    if t == "RouterCollisionRecord": return router_collision_record(stage)
    if t == "ConformanceRecord": return conformance_record(stage)
    raise RunnerDomainError(f"type {t} is not derivable")


@dataclass(frozen=True)
class SweepEnsemble:
    sweeps: Tuple[_CL.ProjectionSweep, ...]
    result_sha256: str = ""


def validate_sweep_ensemble(e, **ctx) -> None:
    if type(e) is not SweepEnsemble or type(e.sweeps) is not tuple: raise RunnerDomainError("exact SweepEnsemble required")
    for s in e.sweeps: _CL.validate_projection_sweep(s)
    if tuple(s.sweep_index for s in e.sweeps) != tuple(range(_CL.DESIGN_STABILITY_SWEEPS)): raise RunnerDomainError("a sweep ensemble carries exactly sweeps 0..199 once, in order")
    if {s.master for s in e.sweeps} != {_CL.PROJECTION_MASTER}: raise RunnerDomainError("a sweep ensemble carries the projection master")
    if e.result_sha256 != _digest(tuple(s.result_sha256 for s in e.sweeps)): raise RunnerDomainError("sweep ensemble identity does not recompute")


# ---- job 0: the calibration census (the CANONICAL role issued here and nowhere else)
def _census_from_records(records_dir, stage, repo_root, pinned_root, adapter, *, replay: bool = False) -> Tuple[_CL.CalibrationCensus, Tuple]:
    runs = []; rows = []
    for obj in _CL.CALIBRATION_OBJECTS:
        results, halts, r = _load_level_results(records_dir, obj, "calibration", stage, repo_root, pinned_root, adapter, replay=replay)
        if halts: raise RunnerDomainError(f"job 0 is incomplete: {sorted(halts.values())[:2]}")
        rows += list(r)
        for m, rs in results.items():
            for res in rs: runs.append(_CL.calibration_run(res))
    prov = _CL.calibration_census(runs, "derived_provisional")
    body = dataclasses.asdict(prov); body["role"] = "canonical"; body.pop("result_sha256")
    c = _CL.CalibrationCensus(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in body.items()})
    c = _coerce_census(c)
    return dataclasses.replace(c, result_sha256=c.identity()), tuple(rows)


def _coerce_census(c):
    """asdict turns nested tuples into lists; rebuild with tuples so the identity matches M5's content form."""
    def tup(x): return tuple(tup(y) for y in x) if isinstance(x, (list, tuple)) else x
    return _CL.CalibrationCensus(**{f.name: tup(getattr(c, f.name)) for f in dataclasses.fields(_CL.CalibrationCensus)})


def validate_calibration_census(c, stage=None, repo_root=None, pinned_root=None, records_dir: Optional[str] = None, adapter=None, **ctx) -> None:
    """M5's structural validator, then: a canonical census REPLAYS from the authorized job-0 LevelRecords in `records_dir` (both objects,
    calibration panel) — the role is the only field M7 sets, and only through this replay."""
    _CL.validate_calibration_census(c)
    if c.role == "canonical":
        if records_dir is None or stage is None or repo_root is None or adapter is None: raise RunnerDomainError("a canonical census validates only by replay from its job-0 level records")
        c2, _ = _census_from_records(records_dir, stage, repo_root, pinned_root, adapter)
        if c2 != c: raise RunnerDomainError("canonical census does not replay from the job-0 level records")


def validate_tolerance_program(tp, census=None, **ctx) -> None:
    if census is None: raise RunnerDomainError("a ToleranceProgram validates only with its census")
    if type(tp) is not _CL.ToleranceProgram or tp != _CL.tolerance_program(census) or census.role != "canonical": raise RunnerDomainError("tolerance program does not re-derive from the canonical census")


COMMITTED_DEPENDENCIES: Tuple[Tuple[str, Tuple[str, ...]], ...] = (   # I003 pt 7: a stability job follows the corresponding canonical census COMMITTED (L2 r2 R2-6)
    ("skeleton_stability", ("skeleton_census",)),
    ("realization_stability", ("realization_census",)),
)
_DEPENDENCY_GATE_MEMO: Dict[Tuple, bool] = {}


def _job_own_prefixes(job: str) -> Tuple[str, ...]:
    """File-name prefixes of the outputs the job ITSELF writes into out_dir (its level records/artifact dirs and its output files): these are not
    inputs of any predecessor's validator, so they are excluded from the dependency-surface key."""
    pre = [fname for _, fname in _job_outputs(job)]
    for j, objs, panel in JOB_OBJECTS:
        if j == job: pre += [f"{level_id(m)}.{o}.{panel}" for m in F8_LEVELS_MICRO for o in objs]
    return tuple(pre)


def _clean_tracked_set(repo_root: str, root: str) -> set:
    """Repo-relative paths under `root` that are tracked AND equal to their committed object (two git calls, not one per file)."""
    rel = os.path.relpath(os.path.abspath(root), os.path.abspath(repo_root)).replace(os.sep, "/")
    tracked = set(l for l in _git(repo_root, "ls-files", "--", rel).splitlines() if l)
    dirty = set()
    for l in _git(repo_root, "status", "--porcelain", "--untracked-files=all", "--", rel).splitlines():
        if not l: continue
        path = l[3:].strip().strip('"')
        for part in path.split(" -> "): dirty.add(part.strip().strip('"'))       # a rename row names both the old and the new path
    return tracked - dirty


def _dependency_surface_digest(job: str, out_dir: str, repo_root: str) -> str:
    """Everything a predecessor's replaying validator may read under out_dir — every file except the current job's own outputs — with each file's
    bytes and committed state (L2 r2 R2-2: 'any replay cache must cover the full dependency surface'; R2-6: commitment is part of the surface)."""
    own = _job_own_prefixes(job); acc = []; clean = _clean_tracked_set(repo_root, out_dir)
    for dp, f in _walk_no_links(out_dir):
        fp = os.path.join(dp, f); rel = os.path.relpath(fp, out_dir).replace(os.sep, "/")
        if any(rel.startswith(px) for px in own): continue
        acc.append((rel, _sha_file(fp), os.path.relpath(fp, repo_root).replace(os.sep, "/") in clean))
    return _digest(tuple(sorted(acc)))


NAMED_OUTPUT_OBJECTS: Dict[str, str] = {**{f: o for o, f in SWEEP_FILES.items()}, **{f: o for o, f in STABILITY_SWEEP_FILES.items()}}


def _bind_named_output(typ: str, fname: str, rec) -> None:
    """A SweepRecord / StabilitySweep persisted under a named output file must BE the object that name denotes (L2 r3 R3-3): a replay-valid
    sweep of another object in the slot is refused wherever a named output is loaded."""
    if fname in NAMED_OUTPUT_OBJECTS and getattr(rec, "obj", None) != NAMED_OUTPUT_OBJECTS[fname]:
        raise RunnerDomainError(f"{fname} must carry the {NAMED_OUTPUT_OBJECTS[fname]} object; it carries {getattr(rec, 'obj', None)!r}")


def require_job_dependencies(job: str, out_dir: str, stage, repo_root, pinned_root, adapter) -> None:
    """s7.1/s7.3 order as EXECUTABLE checks, applied identically on the job route and the direct level route (L2 r1 D3b-d; r2 R2-2): every
    output file of every predecessor job in JOB_GRAPH must exist in `out_dir` and load as an authorized canonical record of that job with its
    validator REPLAYING (schema identity, exact type, full semantic validation); for the stability jobs the corresponding census outputs must
    also EQUAL their committed git objects (I003 pt 7; R2-6). Memoised on the complete dependency surface (every non-own file's bytes and
    committed state, the stage, the authorization surface, frozen code) so a level loop does not replay 48 records per level."""
    key = (job, os.path.abspath(out_dir), stage.result_sha256, _dependency_surface_digest(job, out_dir, repo_root), _authorization_surface_digest(repo_root), _frozen_code_key(), platform_tag())
    if key in _DEPENDENCY_GATE_MEMO: return
    deps = next(d for j, _, d in JOB_GRAPH if j == job); must_commit = dict(COMMITTED_DEPENDENCIES).get(job, ())
    for dep in deps:
        for typ, fname in _job_outputs(dep):
            fp = os.path.join(out_dir, fname)
            if not os.path.isfile(fp): raise RunnerDomainError(f"job {job} requires {dep}'s {typ} ({fname}) produced under authorization first (s7.3 order)")
            rec, _ = load_record(fp, typ, stage, repo_root, pinned_root, require_job=dep, **_dependency_context(typ, fname, out_dir, stage, repo_root, pinned_root, adapter))
            _bind_named_output(typ, fname, rec)
            if dep in must_commit and not _committed_equals_working(repo_root, os.path.relpath(fp, repo_root).replace(os.sep, "/")):
                raise RunnerDomainError(f"job {job} requires {dep}'s {fname} COMMITTED before it runs (Interpretation 003 pt 7): the file is absent from or differs from its git object")
    _DEPENDENCY_GATE_MEMO[key] = True


def _dependency_context(typ: str, fname: str, out_dir: str, stage, repo_root, pinned_root, adapter) -> Dict[str, Any]:
    """The validation context a predecessor's output needs when checked as a dependency (its own inputs, loaded under their jobs)."""
    kw: Dict[str, Any] = _item_context(typ, out_dir, adapter)
    def inp(j, t=None, f=None, **c): return _load_input(j, out_dir, stage, repo_root, pinned_root, record_type=t, fname=f, **c)
    if typ == "AuditQualification": kw.update(design=inp("m6_design_audit", expect_production=True), held_out=inp("m6_held_out_audit", expect_production=True))
    elif typ in ("ToleranceProgram", "ToleranceEnsembles"): kw.update(census=inp("calibration_census", records_dir=out_dir, adapter=adapter))
    elif typ == "StabilityAudit": kw.update(primary=inp("dense_reference"))
    elif typ == "DesignStability": kw.update(ref=inp("dense_reference"), sweeps=inp("projection_sweeps", "SweepEnsemble", records_dir=out_dir).sweeps)
    elif typ == "SkeletonAssessment":
        kw.update(skeleton_high=inp("skeleton_census", "SweepRecord", SWEEP_FILES["skeleton_high"], records_dir=out_dir, adapter=adapter), skeleton_low=inp("skeleton_census", "SweepRecord", SWEEP_FILES["skeleton_low"], records_dir=out_dir, adapter=adapter),
                  census=inp("calibration_census", records_dir=out_dir, adapter=adapter))
    elif typ == "StabilityRecord":
        obj = "skeleton_high" if fname.startswith("skeleton") else "realization"; cjob = "skeleton_census" if obj == "skeleton_high" else "realization_census"; sjob = "skeleton_stability" if obj == "skeleton_high" else "realization_stability"
        kw.update(canonical_sweep=inp(cjob, "SweepRecord", SWEEP_FILES[obj], records_dir=out_dir, adapter=adapter), stability_sweep=inp(sjob, "StabilitySweep", STABILITY_SWEEP_FILES[obj], records_dir=out_dir, adapter=adapter),
                  census=inp("calibration_census", records_dir=out_dir, adapter=adapter))
    elif typ == "P1Evaluation":
        kw.update(skeleton_high=inp("skeleton_census", "SweepRecord", SWEEP_FILES["skeleton_high"], records_dir=out_dir, adapter=adapter), skeleton_low=inp("skeleton_census", "SweepRecord", SWEEP_FILES["skeleton_low"], records_dir=out_dir, adapter=adapter),
                  realization=inp("realization_census", "SweepRecord", SWEEP_FILES["realization"], records_dir=out_dir, adapter=adapter), census=inp("calibration_census", records_dir=out_dir, adapter=adapter))
    elif typ == "PricingRecord": kw.update(adapter=adapter)
    return kw


def _load_input(job: str, out_dir: str, stage, repo_root, pinned_root, record_type: Optional[str] = None, fname: Optional[str] = None, **ctx):
    outs = _job_outputs(job); typ = record_type or outs[0][0]; f = fname or dict(outs)[typ]; p = os.path.join(out_dir, f)
    if not os.path.isfile(p): raise RunnerDomainError(f"input {job} has not been produced under authorization in {out_dir}")
    rec = load_record(p, typ, stage, repo_root, pinned_root, require_job=job, **ctx)[0]
    _bind_named_output(typ, f, rec)
    return rec


def run_canonical_job(job: str, stage: StageIdentity, repo_root: str, out_dir: str, pinned_root: Optional[str], authorization_version: int, **params) -> Tuple[Any, str]:
    """THE ONLY producer of canonical outputs (E1 M7, carried). Lattice-run jobs (calibration_census, skeleton_census, realization_census)
    execute their LevelRecords through `run_level` in production mode under the same authorization (production flag required by run_level)
    and then derive their records from the persisted artifacts; everything else derives from authorized persisted inputs."""
    auth, fsha = require_authorized(stage, repo_root, pinned_root, authorization_version, job)
    os.makedirs(out_dir, exist_ok=True); outs = dict((t, f) for t, f in _job_outputs(job)); ctx: Dict[str, Any] = {}
    adapter = _stage_adapter(repo_root, stage)
    def put(rec, fname, **c): _persist_canonical(rec, os.path.join(out_dir, fname), stage, repo_root, pinned_root, auth, fsha, job, **c); return os.path.join(out_dir, fname)
    if job in SCIENTIFIC_JOBS:
        if not auth.production_authorized: raise RunnerDomainError(f"scientific job {job} requires the production flag of record v{auth.version} (s7.1: both qualifications passed, readiness derived)")
        if not validate_prerequisites(auth, stage, repo_root, pinned_root).production_ready: raise RunnerDomainError("production is not READY")
    require_job_dependencies(job, out_dir, stage, repo_root, pinned_root, adapter)      # EXECUTABLE dependencies (L2 r1 D3): every output of every predecessor job, authorized and valid, before any run
    def levels(obj, panel):
        if not _job_permits(job, obj, panel): raise RunnerDomainError(f"job {job} does not run ({obj}, {panel})")
        for m in F8_LEVELS_MICRO:
            if not os.path.isfile(os.path.join(out_dir, _level_file(m, obj, panel))):
                run_level(m, obj, panel, out_dir, stage, "production", job=job, adapter=adapter, repo_root=repo_root, pinned_root=pinned_root, authorization_version=authorization_version)
    if job == "mp1_known_answer":
        rec = _E.known_answer_qualification()
    elif job in ("m6_design_audit", "m6_held_out_audit"):
        rec = _A.run_audit("design" if job == "m6_design_audit" else "held_out", adapter); ctx = {"expect_production": True}
    elif job == "m6_audit_qualification":
        d = _load_input("m6_design_audit", out_dir, stage, repo_root, pinned_root, expect_production=True); h = _load_input("m6_held_out_audit", out_dir, stage, repo_root, pinned_root, expect_production=True)
        rec = _A.qualify_audit(d, h); ctx = {"design": d, "held_out": h}
    elif job == "m6_price":
        rec = _A.run_pricing(adapter); ctx = {"adapter": adapter}
    elif job == "calibration_census":
        for obj in _CL.CALIBRATION_OBJECTS: levels(obj, "calibration")
        rec, _ = _census_from_records(out_dir, stage, repo_root, pinned_root, adapter); ctx = {"records_dir": out_dir, "adapter": adapter}
    elif job == "tolerance_program":
        census = _load_input("calibration_census", out_dir, stage, repo_root, pinned_root, records_dir=out_dir, adapter=adapter)
        put(tolerance_ensembles_record(census, stage.result_sha256), outs["ToleranceEnsembles"], census=census)       # M5-5: the ensembles are their own record kind (L2 r1 D5b)
        rec = _CL.tolerance_program(census); ctx = {"census": census}
    elif job == "dense_reference": rec = _CL.dense_reference()
    elif job == "reference_stability":
        primary = _load_input("dense_reference", out_dir, stage, repo_root, pinned_root)
        rec = _CL.stability_audit(primary, "canonical"); ctx = {"primary": primary}
    elif job == "projection_sweeps":
        ref = _load_input("dense_reference", out_dir, stage, repo_root, pinned_root)
        sweeps = tuple(_CL.projection_sweep(i) for i in range(_CL.DESIGN_STABILITY_SWEEPS)); ens = SweepEnsemble(sweeps, _digest(tuple(s.result_sha256 for s in sweeps)))
        put(ens, outs["SweepEnsemble"]); rec = _CL.design_stability(ref, sweeps); ctx = {"ref": ref, "sweeps": sweeps}
        return rec, put(rec, outs["DesignStability"], **ctx)
    elif job == "skeleton_census":
        sweeps = {}
        for obj in ("skeleton_high", "skeleton_low"):
            levels(obj, "canonical")
            results, halts, _ = _load_level_results(out_dir, obj, "canonical", stage, repo_root, pinned_root, adapter)
            sweeps[obj] = _E.sweep_from_results(obj, results, halts); put(sweeps[obj], SWEEP_FILES[obj], records_dir=out_dir, adapter=adapter)
        census = _load_input("calibration_census", out_dir, stage, repo_root, pinned_root, records_dir=out_dir, adapter=adapter)
        sh = _load_input(job, out_dir, stage, repo_root, pinned_root, record_type="SweepRecord", fname=SWEEP_FILES["skeleton_high"], records_dir=out_dir, adapter=adapter)
        sl = _load_input(job, out_dir, stage, repo_root, pinned_root, record_type="SweepRecord", fname=SWEEP_FILES["skeleton_low"], records_dir=out_dir, adapter=adapter)
        rec = _skeleton_assessment(sh, sl, census, stage.result_sha256); ctx = {"skeleton_high": sh, "skeleton_low": sl, "census": census}     # s7.3 item 1: the skeleton result is known BEFORE realization runs (L2 r1 D3c)
    elif job == "realization_census":
        levels("realization", "canonical")
        results, halts, rows = _load_level_results(out_dir, "realization", "canonical", stage, repo_root, pinned_root, adapter)
        sw = _E.sweep_from_results("realization", results, halts); put(sw, SWEEP_FILES["realization"], records_dir=out_dir, adapter=adapter)
        labels = []
        for m in F8_LEVELS_MICRO:
            rec_m, _ = load_record(os.path.join(out_dir, _level_file(m, "realization", "canonical")), "LevelRecord", stage, repo_root, pinned_root, require_job="realization_census", level_dir=os.path.join(out_dir, _level_dirname(m, "realization", "canonical")), adapter=adapter, records_dir=out_dir)
            labels.append(rec_m.label)
        rec = _morphology_from_rows(rows, tuple(labels), adapter.body_sha256, stage.result_sha256); ctx = {"records_dir": out_dir, "adapter": adapter}
    elif job in ("skeleton_stability", "realization_stability"):
        obj = "skeleton_high" if job == "skeleton_stability" else "realization"
        cjob = "skeleton_census" if obj == "skeleton_high" else "realization_census"
        canon = _load_input(cjob, out_dir, stage, repo_root, pinned_root, record_type="SweepRecord", fname=SWEEP_FILES[obj], records_dir=out_dir, adapter=adapter)
        census = _load_input("calibration_census", out_dir, stage, repo_root, pinned_root, records_dir=out_dir, adapter=adapter)
        levels(obj, "stability")                                                                      # Interpretation 003 pt 7: the independent stability panel, under THIS job
        put(_stability_sweep_from_records(obj, out_dir, stage, repo_root, pinned_root, adapter), STABILITY_SWEEP_FILES[obj], records_dir=out_dir, adapter=adapter)
        ssw = _load_input(job, out_dir, stage, repo_root, pinned_root, record_type="StabilitySweep", fname=STABILITY_SWEEP_FILES[obj], records_dir=out_dir, adapter=adapter)
        rec = _stability_from(obj, canon, ssw, census, _CL.closure_publication().delta_m.value, stage.result_sha256); ctx = {"canonical_sweep": canon, "stability_sweep": ssw, "census": census}
    elif job == "p1_evaluation":
        sh = _load_input("skeleton_census", out_dir, stage, repo_root, pinned_root, record_type="SweepRecord", fname=SWEEP_FILES["skeleton_high"], records_dir=out_dir, adapter=adapter)
        sl = _load_input("skeleton_census", out_dir, stage, repo_root, pinned_root, record_type="SweepRecord", fname=SWEEP_FILES["skeleton_low"], records_dir=out_dir, adapter=adapter)
        re_ = _load_input("realization_census", out_dir, stage, repo_root, pinned_root, record_type="SweepRecord", fname=SWEEP_FILES["realization"], records_dir=out_dir, adapter=adapter)
        census = _load_input("calibration_census", out_dir, stage, repo_root, pinned_root, records_dir=out_dir, adapter=adapter)
        rec = _E.evaluate_p1(sh, sl, re_, census); ctx = {"skeleton_high": sh, "skeleton_low": sl, "realization": re_, "census": census}
    elif job == "resource_benchmark":
        rec = _benchmark_execute(BENCHMARK_SEEDS, out_dir, stage, F8_GRID, F8_TICKS, BENCHMARK_LEVEL_MICRO, "canonical", auth.version, auth.result_sha256, fsha); ctx = {"artifact_dir": os.path.join(out_dir, "benchmark_artifacts")}
    elif job == "stage1_package":
        spec, ssha = load_package_spec(repo_root, stage)
        for i in spec.items:
            if i.producer_job == "derived": put(_produce_derived(i, stage, repo_root), _item_file(i))
        rows, complete, allpass = _assemble(spec.items, out_dir, stage, repo_root, pinned_root, True, adapter)
        body = ("canonical", stage.result_sha256, spec.governance_sha256, ssha, auth.version, auth.result_sha256, fsha, rows, complete, allpass)
        rec = StagePackage(*body, _digest(body)); ctx = {"package_dir": out_dir, "adapter": adapter}
    else: raise RunnerDomainError(f"job {job} has no executable")
    return rec, put(rec, outs[type(rec).__name__], **ctx)


# ----------------------------------------------------------------------------- validators and registry
def _v_reference(r, **c): _CL.validate_reference_structure(r)
def _v_stability(r, primary=None, **c):
    if primary is None: raise RunnerDomainError("a persisted StabilityAudit requires its primary reference")
    _CL.validate_stability_audit(r, primary)
def _v_design(r, ref=None, sweeps=None, **c):
    if ref is None or sweeps is None: raise RunnerDomainError("a persisted DesignStability requires its reference and sweeps")
    _CL.validate_design_stability(r, ref, sweeps, replay=True)
def _v_sweep_proj(r, **c): _CL.validate_projection_sweep(r)
def _v_audit_record(r, **c): _A.validate_audit_record(r, expect_production=c.get("expect_production", True))
def _v_audit_qual(r, design=None, held_out=None, **c):
    if design is None or held_out is None: raise RunnerDomainError("a persisted AuditQualification requires both records")
    _A.validate_audit_qualification(r, design, held_out)
def _v_known_answer(r, **c):
    if type(r) is not _E.KnownAnswerQualification or r.result_sha256 != r.identity() or r.declaration_sha256 != _E.EVALUATOR_SHA256_LITERAL: raise RunnerDomainError("known-answer record invalid")
    if r != _E.known_answer_qualification(r.sweeps_per_class, r.pass_min, r.master): raise RunnerDomainError("known-answer qualification does not replay")
_PRICE_REPLAY_MEMO: Dict[Tuple, bool] = {}


def _v_price(r, adapter=None, **c):
    """L2 r1 D6: the persisted price must BE the declared experiment — exact types and domains, the frozen replicate count and pricing master, the
    stage adapter's thresholds, M3's nominal alpha_P and construction bound, the declared NULL source and generator declaration identity — and
    its counts must REPLAY through M6's `run_pricing` under the stage adapter (deterministic; memoised on the full record content + adapter)."""
    if type(r) is not _A.PricingRecord: raise RunnerDomainError("not a PricingRecord")
    if adapter is None: raise RunnerDomainError("a persisted PricingRecord validates only against the stage's production adapter")
    if any(type(x) is not int for x in (r.replicates, r.master, r.s_min_rejections, r.s_term_no_sustained)) or not (0 <= r.s_min_rejections <= r.replicates and 0 <= r.s_term_no_sustained <= r.replicates): raise RunnerDomainError("pricing counts malformed")
    if r.replicates != _A.PRICING_REPLICATES or r.master != _A.production_masters()[2]: raise RunnerDomainError("pricing record is not the frozen replicate count under the pricing master")
    if (r.theta_p, r.theta_t) != (adapter.theta_p, adapter.theta_t) or not _is_production_adapter(adapter): raise RunnerDomainError("pricing thresholds are not the stage adapter's")
    if r.alpha_p_nominal != _N.ALPHA_P or r.construction_bound != _N.familywise_nominal_bound(_N.null_thresholds(F8_LEVELS_MICRO[0])): raise RunnerDomainError("pricing nominal alpha / construction bound are not M3's")
    if r.source != "m6_null_count_process" or r.declaration_sha256 != _A.GENERATOR_DECLARATION_SHA256_LITERAL: raise RunnerDomainError("pricing source or generator declaration identity differ from M6's")
    if r.cp_upper_95 != _A.clopper_pearson_upper(r.s_min_rejections, r.replicates) or r.s_min_rejection_rate != r.s_min_rejections / r.replicates: raise RunnerDomainError("pricing record arithmetic does not recompute")
    key = (dataclasses.astuple(r), adapter.body_sha256, _frozen_code_key(), platform_tag())
    if key not in _PRICE_REPLAY_MEMO: _PRICE_REPLAY_MEMO[key] = (_A.run_pricing(adapter) == r)
    if not _PRICE_REPLAY_MEMO[key]: raise RunnerDomainError("pricing record does not replay through M6's run_pricing under the stage adapter")
def _v_sweep_record(r, stage=None, repo_root=None, pinned_root=None, records_dir=None, adapter=None, **c):
    _E.validate_sweep_record(r)
    if r.role != "canonical": raise RunnerDomainError("a persisted sweep must be canonical")
    if records_dir is None or stage is None or repo_root is None or adapter is None: raise RunnerDomainError("a canonical SweepRecord validates only by replay from its level records")
    results, halts, _ = _load_level_results(records_dir, r.obj, "canonical", stage, repo_root, pinned_root, adapter)
    _E.validate_sweep_record(r, results, halts)
def _v_p1(r, skeleton_high=None, skeleton_low=None, realization=None, census=None, **c):
    if any(x is None for x in (skeleton_high, skeleton_low, realization, census)): raise RunnerDomainError("a persisted P1Evaluation requires its three sweeps and the census")
    if type(r) is not _E.P1Evaluation or r != _E.evaluate_p1(skeleton_high, skeleton_low, realization, census): raise RunnerDomainError("P1 evaluation does not replay from its inputs")
def _v_stage(r, repo_root=None, pinned_root=None, **c): validate_stage_identity(r, repo_root, pinned_root)
def _v_auth(r, stage=None, **c): validate_authorization(r, stage)

VALIDATORS = {"ReferenceStructure": _v_reference, "StabilityAudit": _v_stability, "DesignStability": _v_design, "ProjectionSweep": _v_sweep_proj, "SweepEnsemble": validate_sweep_ensemble,
              "AuditRecord": _v_audit_record, "AuditQualification": _v_audit_qual, "KnownAnswerQualification": _v_known_answer, "PricingRecord": _v_price,
              "CalibrationCensus": validate_calibration_census, "ToleranceProgram": validate_tolerance_program, "SweepRecord": _v_sweep_record, "MorphologyRecord": validate_morphology,
              "StabilityRecord": validate_stability_record, "StabilitySweep": validate_stability_sweep, "SkeletonAssessment": validate_skeleton_assessment, "ToleranceEnsembles": validate_tolerance_ensembles, "P1Evaluation": _v_p1, "StageIdentity": _v_stage, "AuthorizationRecord": _v_auth,
              "LevelRecord": validate_level_record, "TrancheQuarantine": validate_quarantine, "ResourceBenchmark": validate_benchmark, "StagePackage": validate_stage_package,
              "PackageSpecification": validate_package_spec, "LevelListRecord": validate_level_list, "EnsembleSizesRecord": validate_ensemble_sizes,
              "ClosurePublicationRecord": validate_closure_publication_record, "NullLawRecord": validate_null_law, "RouterCollisionRecord": validate_router_collision,
              "ConformanceRecord": validate_conformance_record, "M7PlacementRecord": validate_placement_record, "AuthorizationRegistry": validate_registry,
              "ProductionPrerequisiteManifest": validate_prerequisite_manifest, "F8Governance": validate_governance, "M7SuiteRecord": validate_suite_record}

_register(StageIdentity, AuthorizationRecord, AuthorizationRegistry, M7PlacementRecord, M7SuiteRecord, F8Governance, RunProvenance, LevelRecord, PrerequisiteEntry,
          ProductionPrerequisiteManifest, TrancheQuarantine, ResourceBenchmark, PackageItem, PackageSpecification, StagePackage, SweepEnsemble, LevelListRecord,
          EnsembleSizesRecord, ClosurePublicationRecord, NullLawRecord, RouterCollisionRecord, ConformanceRecord, MorphologyRecord, StabilityRecord, StabilitySweep, SkeletonAssessment, ToleranceEnsembles,
          _CL.ReferenceStructure, _CL.StabilityAudit, _CL.DesignStability, _CL.ProjectionSweep, _CL.CalibrationCensus, _CL.ToleranceProgram, _CL.ToleranceEnsemble, _CL.DeltaM,
          _A.AuditRecord, _A.ClassScore, _A.AuditQualification, _A.PricingRecord, _E.KnownAnswerQualification, _E.SweepRecord, _E.LevelData, _E.P1Evaluation, _E.TestResult, _E.FidelityTier)
for _n in RECORD_TYPES:
    if _n not in VALIDATORS and _n not in ("RunProvenance", "ClassScore", "PackageItem", "PrerequisiteEntry", "DeltaM", "LevelData", "TestResult", "FidelityTier", "ToleranceEnsemble"): raise RunnerDomainError(f"registered type {_n} has no validator")
