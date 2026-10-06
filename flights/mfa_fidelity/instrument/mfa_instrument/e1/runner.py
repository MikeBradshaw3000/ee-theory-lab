"""mfa_instrument/e1/runner.py — E1 stage-1 module M7, ROUND 2: the stage package (Contract E1 v0.2 §7.5, §7.8, §8, §9;
v0.3 §7; v0.8 §F; design note §2 M7; L2 M7 first-pass review §17, items 1–28; the five adjudication rulings).

THREE PRINCIPLES (L2 §3–§13)
A. AUTHORIZATION IS A RECORD, NOT A BOOLEAN. Source literals grant nothing — ever. A canonical job, the tranche,
   production and the package each require a separate, Mike-ratified, digest-bound AuthorizationRecord, committed
   in the governance directory, carrying the exact bound stage identity, the E1-R amendment identity, the package-
   specification identity, the authorized job names, the exact tranche panel, the production prerequisites, the issuer,
   version and date. Every canonical result is produced THROUGH `run_canonical_job`, which attaches the authorization
   and stage identities to the persisted envelope at execution; a pre-authorization result cannot be wrapped afterwards
   because the envelope's authorization binding is written by the wrapper from the record it validated.
B. THE IDENTITY SURFACE IS LARGER THAN CODE. The stage binds: the runtime sources and cleared tests (from disk, equal to
   cleared literals, committed, clean); the M7 placement record; the authoritative Gate A/B/R0 records; the pinned
   ancestor commit and the lock-blob identity THROUGH Gate B's environment checker (full twenty-pin qualification —
   canonical role comes from Gate B's `conforms`, never from a Python version string); the ACTUAL threshold-cache and
   qualification files (file digests and the re-derived body digest); the E1-R amendment and package-specification
   records (absent until Mike writes them → the stage is `pre_amendment`); the versioned record-schema identity.
C. EVERY RECORD DERIVES, INCLUDING M7'S OWN. LevelRecord from run artifacts and the complete scoring bundle;
   TrancheQuarantine with its exact panel, per-run provenance and cleanup proof; ResourceBenchmark gated, with
   verifier/conformance per run and full telemetry+rho readback; typed per-item package records with item-specific
   predicates (an analysis-subset reference can never fill the dense-reference slot); StagePackage with a validator,
   one file per item, and canonical assembly DISABLED until the package specification exists.

Canonical-record loading refuses duplicate JSON keys, nonfinite constants and non-canonical bytes, validates the stage
on write and on load, and runs the record's own validator. Rehearsal is retained as a separate noncanonical role
(adjudication 4). The package item list stays [PROPOSED] (adjudication 5).
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
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import audit as _A
from . import classify as _K
from . import config as _C
from . import null as _N
from . import projection as _P
from . import verdict as _V
from ..gates.gate_b import environment as _ENV
from .classify import level_counts, level_label, run_status
from .verdict import route
from .config import E1_GRID, E1_LEVELS_MICRO, E1_SEED_PANEL, E1_TICKS, level_id

RUNNER_VERSION = "e1_stage1_m7_v6 / platform-independent declared paths (POSIX literals); round-5 content unchanged"
RECORD_SCHEMA_VERSION = 2


class RunnerDomainError(ValueError): ...
class ApparatusHalt(RuntimeError): ...
class EvaluabilityHalt(RuntimeError):
    """Operational evaluability event: a router-inserted pass-2 level whose conditional threshold was never qualified
    (outside the reachable surface the cache covers). Halts the LEVEL; recorded; never an apparatus failure."""
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
INSTRUMENT_ROOT_REL = "flights/mfa_fidelity/instrument"            # POSIX literal: repo-relative paths are platform-independent
GOVERNANCE_ROOT_REL = "flights/mfa_fidelity/governance/e1_stage1"  # POSIX literal (declared and digested)
RUNNER_REL = "mfa_instrument/e1/runner.py"
M7_TEST_REL = "tests/test_e1_m7.py"
PLACEMENT_RECORD_REL = "M7_PLACEMENT_RECORD.json"
AMENDMENT_REL = "E1R_AMENDMENT.md"
PACKAGE_SPEC_REL = "PACKAGE_SPECIFICATION.json"
AUTHORIZATION_GLOB = "AUTHORIZATION_"
ANCESTOR_COMMIT = "4d9a622"                      # Gate A's pinned ancestor commit (short id as the gate record names it)
GATE_RECORDS: Tuple[Tuple[str, str], ...] = (    # authoritative records, FULL cleared identities at main a24fd5e
    ("flights/mfa_fidelity/gates/gate_a/GATE_A_AUTHORITATIVE_RECORD.md", "719a9706f34e6c08119993f1826242939e6a2331fc77cf50a61c769d2710ca74"),
    ("flights/mfa_fidelity/gates/gate_b/GATE_B_AUTHORITATIVE_CERTIFICATION_RECORD.md", "940d88a426d9530449d4c9d93d4a23085d354b678e2229edcf849806f6685883"),
    ("flights/mfa_fidelity/gates/gate_r0/GATE_R0_REGISTER_CLOSURE.md", "59fd2a54a344f994346001eab2ec14b03357018536e3386318138df079e6e741"),
)
AUTHORIZATION_REGISTRY_REL = "AUTHORIZATION_REGISTRY.json"
PREREQUISITES_REL = "prerequisites"              # governance/e1_stage1/prerequisites/<name>.json: the records a production authorization names
GOVERNANCE_REL = "E1R_GOVERNANCE.json"            # Mike's typed, canonical, machine-readable E1-R governance record (values live THERE, never here)
PREREQ_MANIFEST_REL = "PRODUCTION_PREREQUISITES.json"
SUITE_RECORD_REL = "M7_SUITE_RECORD.json"
CLEARANCE_DIR_REL = "flights/mfa_fidelity/build_records"
PREREQ_VOCAB = ("stage1_package", "calibration_tranche", "resource_actuals", "dense_reference", "reference_stability", "m6_audit_qualification")   # loadable prerequisite KINDS (mechanics)
PREREQ_KINDS = ("apparatus", "qualification", "scientific")     # grammar: the governance record classifies each prerequisite
PREREQ_REQUIREMENTS = ("pass", "valid_complete")               # grammar: what the governance record may require of each prerequisite
BENCHMARK_LEVEL_MICRO = 515217                   # frozen canonical benchmark panel (level 12; first three frozen seeds)
BENCHMARK_SEEDS = 3
AMENDMENT_REQUIRED_FIELDS = ("amendment_version:", "claim_tier:", "flight_name:", "verdict_grammar:", "package_grammar:")   # the amendment-record contract
PREDICATE_IDS = ("exists", "reference_of_record_dense", "reference_resolved", "stability_canonical_complete", "stability_within", "design_complete", "design_stable", "sweep_ensemble_canonical", "audit_record_complete", "audit_record_pass", "qualification_recorded", "qualification_qualified", "benchmark_canonical", "benchmark_fits", "conformance_production", "conformance_production_passed", "null_precision_dense", "null_precision_dense_no_halts", "closure_covers_levels", "quarantine_recorded", "quarantine_passed", "tolerance_program_recorded", "tolerance_program_complete")
CACHE_FILES: Tuple[Tuple[str, str], ...] = (
    ("flights/mfa_fidelity/artifacts/e1/threshold_cache_qualified.json", _A.PRODUCTION_CACHE_FILE_SHA256_LITERAL),
    ("flights/mfa_fidelity/artifacts/e1/threshold_cache_qualification.json", _A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL),
)
TRANCHE_SEEDS = 3                               # [PROPOSED] v0.2 §7.5
TRANCHE_LEVELS = 5                              # [PROPOSED]
BENCHMARK_MARGIN = 0.30
PRODUCTION_RUNS = (24 + 8) * 20
CANONICAL_JOBS = ("dense_reference", "reference_stability", "projection_sweeps", "tolerance_ensembles", "tolerance_program", "m6_design_audit", "m6_held_out_audit", "m6_audit_qualification", "resource_benchmark", "stage1_package")
TOLERANCE_PROGRAM_LEVELS = tuple(E1_LEVELS_MICRO)  # the declared canonical tolerance program: one 1,000-replicate ensemble per pass-1 level
SOURCE_LITERALS_GRANT_NOTHING = True            # default-deny: no in-process value can authorize anything (L2 adjudication 3)
STAGE_ROLES = ("canonical", "pre_amendment", "noncanonical")
HALT_CLASSES = ("apparatus", "evaluability_operational", "anomaly_domain")
PACKAGE_ITEMS: Tuple[Tuple[str, str], ...] = (  # [PROPOSED pending the E1-R amendment]; the frozen list lives in the Package Specification Record
    ("conformance_preflight", "ConformanceRecord"), ("closure_publication", "ClosurePublication"), ("null_precision", "NullPrecisionRecord"),
    ("dense_reference", "ReferenceStructure"), ("reference_stability", "StabilityAudit"), ("level_list_and_spacings", "LevelListRecord"),
    ("design_stability", "DesignStability"), ("router_collision_record", "RouterCollisionRecord"), ("m6_audit_qualification", "AuditQualification"),
    ("ensemble_sizes", "EnsembleSizesRecord"), ("resource_actuals", "ResourceBenchmark"),
)
BOUND_SOURCES: Tuple[Tuple[str, str], ...] = (      # cleared placed identities (M1–M6 sources and tests; instrument core; gates)
    ("mfa_instrument/__init__.py", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("mfa_instrument/bridge.py", "0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e"),
    ("mfa_instrument/config.py", "f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872"),
    ("mfa_instrument/dynamics.py", "483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8"),
    ("mfa_instrument/e1/__init__.py", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("mfa_instrument/e1/audit.py", "ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3"),
    ("mfa_instrument/e1/classify.py", "db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3"),
    ("mfa_instrument/e1/config.py", "934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22"),
    ("mfa_instrument/e1/null.py", "58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa"),
    ("mfa_instrument/e1/projection.py", "29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2"),
    ("mfa_instrument/e1/verdict.py", "e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf"),
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
    ("tests/test_e1_m1_m2.py", "4a9221bb997cd42ec9d49d3fd1ac1012c0a19b4fe65fe17472a9fab0e1d36739"),
    ("tests/test_e1_m3.py", "684acf2d8a881051d9556bd235a46ec3dc997486c0fc41f94d10fd667a56d090"),
    ("tests/test_e1_m4.py", "9f707b2b2156488365e5398e6fc4dc86d25af47aaea66cc663e210f9c49fc496"),
    ("tests/test_e1_m5.py", "82dcdfffc70994e11a278c2f95136f2b4c28838612c0d98b487e9c49693ba977"),
    ("tests/test_e1_m6.py", "f0353709311d100154bfcb85578fee7baa4cd8bb12b241b67365b86df8c72b8f"),
)

RUNNER_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("version", RUNNER_VERSION), ("record_schema_version", RECORD_SCHEMA_VERSION), ("tranche", (TRANCHE_SEEDS, TRANCHE_LEVELS)),
    ("benchmark_margin", BENCHMARK_MARGIN), ("production_runs", PRODUCTION_RUNS), ("canonical_jobs", CANONICAL_JOBS),
    ("source_literals_grant_nothing", SOURCE_LITERALS_GRANT_NOTHING), ("stage_roles", STAGE_ROLES), ("halt_classes", HALT_CLASSES),
    ("package_items_proposed", PACKAGE_ITEMS), ("bound_sources", BOUND_SOURCES), ("gate_records", GATE_RECORDS), ("cache_files", CACHE_FILES),
    ("ancestor_commit", ANCESTOR_COMMIT), ("lock_sha256", _ENV.EXPECTED_LOCK_SHA256), ("pin_count", _ENV.EXPECTED_PIN_COUNT),
    ("prereq_vocab", PREREQ_VOCAB), ("benchmark_panel", (BENCHMARK_LEVEL_MICRO, BENCHMARK_SEEDS)), ("amendment_required_fields", AMENDMENT_REQUIRED_FIELDS),
    ("predicate_ids", PREDICATE_IDS), ("prereq_kinds", PREREQ_KINDS), ("prereq_requirements", PREREQ_REQUIREMENTS), ("tolerance_program_levels", TOLERANCE_PROGRAM_LEVELS),
    ("governance_root", GOVERNANCE_ROOT_REL), ("restart_granularity", "whole level"),
    ("authorization", "separate Mike-ratified AuthorizationRecord in the governance directory; source grants nothing"),
)
RUNNER_DECLARATION_SHA256_LITERAL = "23bf1eb8dd73e4ab6322f3bfea49c05109120877e450837b5a8b7513d4ea2291"   # established 2026-10-04 (round 6; platform-independent)


def verify_frozen_identity() -> None:
    _C.verify_frozen_identity(); _K.verify_frozen_identity(); _N.verify_frozen_identity(); _V.verify_frozen_identity(); _A.verify_frozen_identity(); _P.verify_frozen_identity()
    if _digest(RUNNER_DECLARATION) != RUNNER_DECLARATION_SHA256_LITERAL: raise RunnerDomainError("runner declaration differs from its frozen literal digest")
    d = _frozen_mapping(RUNNER_DECLARATION, "RUNNER_DECLARATION")
    live = {"version": RUNNER_VERSION, "record_schema_version": RECORD_SCHEMA_VERSION, "tranche": (TRANCHE_SEEDS, TRANCHE_LEVELS), "benchmark_margin": BENCHMARK_MARGIN,
            "production_runs": PRODUCTION_RUNS, "canonical_jobs": CANONICAL_JOBS, "source_literals_grant_nothing": SOURCE_LITERALS_GRANT_NOTHING, "stage_roles": STAGE_ROLES,
            "halt_classes": HALT_CLASSES, "package_items_proposed": PACKAGE_ITEMS, "bound_sources": BOUND_SOURCES, "gate_records": GATE_RECORDS, "cache_files": CACHE_FILES,
            "ancestor_commit": ANCESTOR_COMMIT, "lock_sha256": _ENV.EXPECTED_LOCK_SHA256, "pin_count": _ENV.EXPECTED_PIN_COUNT, "governance_root": GOVERNANCE_ROOT_REL,
            "prereq_vocab": PREREQ_VOCAB, "benchmark_panel": (BENCHMARK_LEVEL_MICRO, BENCHMARK_SEEDS), "amendment_required_fields": AMENDMENT_REQUIRED_FIELDS,
            "predicate_ids": PREDICATE_IDS, "prereq_kinds": PREREQ_KINDS, "prereq_requirements": PREREQ_REQUIREMENTS, "tolerance_program_levels": TOLERANCE_PROGRAM_LEVELS}
    for k, v in live.items():
        if d[k] != v or type(d[k]) is not type(v): raise RunnerDomainError(f"runner declaration field {k} differs from the live global")
    if PRODUCTION_RUNS != 640 or BENCHMARK_MARGIN != 0.30 or SOURCE_LITERALS_GRANT_NOTHING is not True or _ENV.EXPECTED_PIN_COUNT != 20 or len({p for p, _ in BOUND_SOURCES}) != len(BOUND_SOURCES):
        raise RunnerDomainError("runner hard values differ from the contract")
    if any(not _is_hex(h, 64) for _, h in BOUND_SOURCES) or any(not _is_hex(h, 64) for _, h in GATE_RECORDS) or any(not _is_hex(h, 64) for _, h in CACHE_FILES):
        raise RunnerDomainError("bound identities malformed")
    if set(PREDICATE_IDS) != set(PREDICATES): raise RunnerDomainError("declared predicate alphabet differs from the implemented predicates")
    if "\\" in repr(RUNNER_DECLARATION) or any("\\" in x for x in (INSTRUMENT_ROOT_REL, GOVERNANCE_ROOT_REL, RUNNER_REL, M7_TEST_REL, CLEARANCE_DIR_REL)):
        raise RunnerDomainError("declared paths must be platform-independent POSIX literals")


# ----------------------------------------------------------------------------- records registry and schema identity
RECORD_TYPES: Dict[str, type] = {}


def _register(*classes) -> None:
    for c in classes:
        if c.__name__ in RECORD_TYPES and RECORD_TYPES[c.__name__] is not c: raise RunnerDomainError(f"record type name {c.__name__} already registered")
        RECORD_TYPES[c.__name__] = c


def record_schema_identity() -> str:
    """Versioned identity of every persisted record schema: fully-qualified class, field names and declared types."""
    return _digest((RECORD_SCHEMA_VERSION, tuple(sorted((f"{c.__module__}.{c.__qualname__}", tuple((f.name, str(f.type)) for f in dataclasses.fields(c))) for c in RECORD_TYPES.values()))))


def _git(repo_root: str, *args) -> str:
    out = subprocess.run(["git", "-C", repo_root, *args], capture_output=True, text=True)
    if out.returncode != 0: raise ApparatusHalt(f"git {' '.join(args)} failed: {out.stderr.strip()[:120]}")
    return out.stdout.strip()


def _committed_equals_working(repo_root: str, rel: str) -> bool:
    blob = subprocess.run(["git", "-C", repo_root, "show", f"HEAD:{rel.replace(os.sep, '/')}"], capture_output=True)
    return blob.returncode == 0 and hashlib.sha256(blob.stdout).hexdigest() == _sha_file(os.path.join(repo_root, rel))


# ----------------------------------------------------------------------------- 1. stage identity (eleven-part surface)
@dataclass(frozen=True)
class StageIdentity:
    role: str
    commit: str                                      # the last commit that touched the bound surface (the stage's commit)
    head_commit: str                                 # descriptive: HEAD at binding (excluded from the identity body)
    source_digests: Tuple[Tuple[str, str], ...]
    runner_sha256: str
    m7_test_sha256: str
    placement_record_sha256: Optional[str]           # None before M7 placement
    gate_record_digests: Tuple[Tuple[str, str], ...]
    ancestor_commit: str
    lock_sha256: str
    environment_conforms: bool
    environment_sha256: str                           # identity of Gate B's full EnvironmentRecord (pins, versions, lock)
    environment_failures: Tuple[str, ...]
    cache_file_digests: Tuple[Tuple[str, str], ...]
    cache_body_sha256: str
    amendment_sha256: Optional[str]                   # None until the E1-R amendment exists
    governance_sha256: Optional[str]                  # None until Mike's machine-readable E1-R governance record exists
    package_spec_sha256: Optional[str]                # None until the Package Specification Record exists
    record_schema_sha256: str
    m7_declaration_sha256: str
    result_sha256: str = ""


_STAGE_FIELDS = tuple(f.name for f in dataclasses.fields(StageIdentity) if f.name not in ("result_sha256", "head_commit"))
def _stage_body(s) -> Tuple: return tuple(getattr(s, k) for k in _STAGE_FIELDS)


def _gov(repo_root: str, rel: str) -> str: return os.path.join(repo_root, GOVERNANCE_ROOT_REL, rel)


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
    gate_d = []
    for rel, want16 in GATE_RECORDS:   # (full identities; the name is historical)
        p = os.path.join(repo_root, rel)
        if not os.path.isfile(p): raise ApparatusHalt(f"authoritative gate record missing: {rel}")
        h = _sha_file(p)
        if h != want16: raise ApparatusHalt(f"gate record {rel} differs from its cleared identity")
        gate_d.append((rel, h))
    cache_d = []
    for rel, want in CACHE_FILES:
        p = os.path.join(repo_root, rel)
        if not os.path.isfile(p): raise ApparatusHalt(f"cache artifact missing: {rel}")
        h = _sha_file(p)
        if h != want: raise ApparatusHalt(f"cache artifact {rel} differs from its committed identity")
        cache_d.append((rel, h))
    # M6's FULL production loader: qualification record semantics, body/file identities, mapping re-derivation (L2 r2 §3.4).
    # CONTENT-ADDRESSED MEMO: the key is the two cache FILE digests (recomputed above on every call) plus the frozen M3/M4/M6 declaration
    # identities; identical bytes under identical frozen code yield an identical qualification. Only successes are memoized.
    body_sha = _qualify_cache_memoized(repo_root, tuple(h for _, h in cache_d))
    # clean committed surface: bound sources, runner/test, the three governance records, gate records, cache files.
    # AUTHORIZATION_* files are NOT part of the surface: an authorization names the stage, so it cannot be part of the stage.
    surface = [_pp.join(INSTRUMENT_ROOT_REL, r) for r, _ in BOUND_SOURCES] + [_pp.join(INSTRUMENT_ROOT_REL, RUNNER_REL), _pp.join(INSTRUMENT_ROOT_REL, M7_TEST_REL)] \
              + [_pp.join(GOVERNANCE_ROOT_REL, g) for g in (PLACEMENT_RECORD_REL, SUITE_RECORD_REL, AMENDMENT_REL, GOVERNANCE_REL, PACKAGE_SPEC_REL)] + [r for r, _ in GATE_RECORDS] + [r for r, _ in CACHE_FILES]
    if _git(repo_root, "status", "--porcelain", "--", *surface): raise ApparatusHalt("the bound surface has uncommitted changes")
    # THE STAGE COMMIT = the last commit that touched the bound surface (prospective: later commits that do not touch it, e.g. an
    # authorization record, leave the stage identity unchanged); HEAD is recorded descriptively.
    commit = _git(repo_root, "log", "-1", "--format=%H", "--", *surface)
    if not _is_hex(commit, 40): raise ApparatusHalt("no commit touches the bound surface")
    for rel in [_pp.join(INSTRUMENT_ROOT_REL, r) for r, _ in BOUND_SOURCES] + [_pp.join(INSTRUMENT_ROOT_REL, RUNNER_REL), _pp.join(INSTRUMENT_ROOT_REL, M7_TEST_REL)] + [r for r, _ in GATE_RECORDS] + [r for r, _ in CACHE_FILES]:
        if not _committed_equals_working(repo_root, rel): raise ApparatusHalt(f"working file differs from the committed object: {rel}")
    # governance records (optional until written; when present they must be committed)
    def opt(rel):
        p = _gov(repo_root, rel)
        if not os.path.isfile(p): return None
        if not _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, rel)): raise ApparatusHalt(f"governance record not committed: {rel}")
        return _sha_file(p)
    placement = opt(PLACEMENT_RECORD_REL); amendment = opt(AMENDMENT_REL); governance = opt(GOVERNANCE_REL); spec = opt(PACKAGE_SPEC_REL)
    if placement is not None:                                          # typed placement record whose MECHANICAL facts are checked against the repository
        try: verify_placement(repo_root, runner_sha, test_sha)
        except RunnerDomainError as e: raise ApparatusHalt(f"placement record does not verify: {e}")
    if amendment is not None:                                          # the amendment-record contract: required fields present
        txt = open(_gov(repo_root, AMENDMENT_REL), "rb").read()
        if b"\r\n" in txt or not all(f.encode() in txt for f in AMENDMENT_REQUIRED_FIELDS): raise ApparatusHalt("E1-R amendment record does not satisfy the amendment-record contract")
    gov_rec = None
    if governance is not None:                                         # Mike's machine-readable governance: typed, canonical, bound to the committed amendment
        try:
            gov_rec = _read_canonical(_gov(repo_root, GOVERNANCE_REL))
            if type(gov_rec) is not E1RGovernance: raise RunnerDomainError("not an E1RGovernance record")
            validate_governance(gov_rec)
        except RunnerDomainError as e: raise ApparatusHalt(f"E1-R governance record does not validate: {e}")
        if amendment is None or gov_rec.amendment_sha256 != amendment: raise ApparatusHalt("E1-R governance record names a different (or absent) amendment")
    if spec is not None:                                               # the committed specification is validated AGAINST the governance record at binding
        if gov_rec is None: raise ApparatusHalt("a Package Specification requires the committed E1-R governance record")
        try:
            ps = _read_canonical(_gov(repo_root, PACKAGE_SPEC_REL))
            if type(ps) is not PackageSpecification: raise RunnerDomainError("not a PackageSpecification")
            validate_package_spec(ps, governance=gov_rec, governance_sha256=governance)
        except RunnerDomainError as e: raise ApparatusHalt(f"package specification does not validate against the governance record: {e}")
    # environment: Gate B's full qualification
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
    role = "canonical" if (conforms and placement and amendment and governance and spec) else ("pre_amendment" if (conforms and placement) else "noncanonical")
    return dict(role=role, commit=commit, head_commit=head, source_digests=tuple(digests), runner_sha256=runner_sha, m7_test_sha256=test_sha, placement_record_sha256=placement,
                gate_record_digests=tuple(gate_d), ancestor_commit=ANCESTOR_COMMIT, lock_sha256=_ENV.EXPECTED_LOCK_SHA256, environment_conforms=conforms, environment_sha256=env_sha,
                environment_failures=tuple(env_fail), cache_file_digests=tuple(cache_d), cache_body_sha256=body_sha, amendment_sha256=amendment, governance_sha256=governance, package_spec_sha256=spec,
                record_schema_sha256=record_schema_identity(), m7_declaration_sha256=RUNNER_DECLARATION_SHA256_LITERAL)


def _refuse_const(c): raise RunnerDomainError(f"nonfinite JSON constant {c}")


def _read_canonical(path: str):
    raw = open(path, "rb").read()
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
    if _canon(doc).encode() != raw: raise RunnerDomainError(f"{os.path.basename(path)} is not in canonical byte form")
    return _decode(doc)


@dataclass(frozen=True)
class M7SuiteRecord:
    """The canonical suite result on the placed bytes (committed under governance)."""
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
    """Governed placement record. Every field named as a mechanical identity is checked against the repository by `verify_placement`."""
    runner_sha256: str
    m7_test_sha256: str
    l2_clearance_file: str                       # path relative to the repository root (under build_records)
    l2_clearance_sha256: str
    placement_commit: str                        # must equal the last commit that touched runner.py and test_e1_m7.py
    suite_record_sha256: str
    result_sha256: str = ""


def validate_placement_record(pr, runner_sha: Optional[str] = None, test_sha: Optional[str] = None, **ctx) -> None:
    if type(pr) is not M7PlacementRecord or not all(_is_hex(x, 64) for x in (pr.runner_sha256, pr.m7_test_sha256, pr.l2_clearance_sha256, pr.suite_record_sha256)) or not _is_hex(pr.placement_commit, 40):
        raise RunnerDomainError("placement record malformed")
    if not isinstance(pr.l2_clearance_file, str) or not pr.l2_clearance_file.startswith(CLEARANCE_DIR_REL.replace(os.sep, "/") + "/") or ".." in pr.l2_clearance_file: raise RunnerDomainError("clearance file must lie under build_records")
    if runner_sha is not None and (pr.runner_sha256, pr.m7_test_sha256) != (runner_sha, test_sha): raise RunnerDomainError("placed runner/test differ from the M7 placement record")
    if pr.result_sha256 != _digest((pr.runner_sha256, pr.m7_test_sha256, pr.l2_clearance_file, pr.l2_clearance_sha256, pr.placement_commit, pr.suite_record_sha256)): raise RunnerDomainError("placement record identity does not recompute")


def verify_placement(repo_root: str, runner_sha: str, test_sha: str) -> M7PlacementRecord:
    """Mechanical verification (L2 r3 R3-1): the placement commit IS the last commit touching runner/test; the L2 clearance file exists, is
    committed, has the named identity, names both cleared file identities, and states the SOUND/placeable disposition; the suite record is
    committed, typed, passing, names the same files, and tested the placement commit."""
    pr = _read_canonical(_gov(repo_root, PLACEMENT_RECORD_REL))
    if type(pr) is not M7PlacementRecord: raise RunnerDomainError("not an M7PlacementRecord")
    validate_placement_record(pr, runner_sha, test_sha)
    placed = _git(repo_root, "log", "-1", "--format=%H", "--", _pp.join(INSTRUMENT_ROOT_REL, RUNNER_REL), _pp.join(INSTRUMENT_ROOT_REL, M7_TEST_REL))
    if placed != pr.placement_commit: raise RunnerDomainError("placement commit is not the last commit that touched runner.py and test_e1_m7.py")
    cf = os.path.join(repo_root, pr.l2_clearance_file)
    if not os.path.isfile(cf) or not _committed_equals_working(repo_root, pr.l2_clearance_file) or _sha_file(cf) != pr.l2_clearance_sha256: raise RunnerDomainError("L2 clearance file absent, uncommitted, or not the named identity")
    txt = open(cf, "rb").read().decode("utf-8", "replace")
    if runner_sha not in txt or test_sha not in txt: raise RunnerDomainError("L2 clearance file does not name both cleared M7 identities")
    if "FINAL VERDICT: SOUND" not in txt: raise RunnerDomainError("L2 clearance file does not state the final SOUND disposition")
    sp = _gov(repo_root, SUITE_RECORD_REL)
    if not os.path.isfile(sp) or not _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, SUITE_RECORD_REL)) or _sha_file(sp) != pr.suite_record_sha256: raise RunnerDomainError("suite record absent, uncommitted, or not the named identity")
    sr = _read_canonical(sp)
    if type(sr) is not M7SuiteRecord: raise RunnerDomainError("suite record is not an M7SuiteRecord")
    validate_suite_record(sr)
    if (sr.runner_sha256, sr.m7_test_sha256, sr.tested_commit) != (runner_sha, test_sha, pr.placement_commit): raise RunnerDomainError("suite record names different files or a different commit")
    return pr


# ----------------------------------------------------------------------------- the E1-R governance record (Mike's values; M7 enforces, contains none)
@dataclass(frozen=True)
class E1RGovernance:
    """Machine-readable half of the E1-R amendment. Every scientific VALUE lives here; M7 holds only the grammar it is checked against."""
    version: int
    amendment_sha256: str                                            # the committed E1R_AMENDMENT.md this record implements
    claim_tier: str
    flight_name: str
    package_item_vocabulary: Tuple[str, ...]                         # every name a Package Specification may use
    required_package_items: Tuple[str, ...]                          # the items a complete package must contain
    production_prerequisites: Tuple[Tuple[str, str, str], ...]       # (prerequisite in PREREQ_VOCAB, kind in PREREQ_KINDS, requirement in PREREQ_REQUIREMENTS) — the EXACT set
    branch_stopping: Tuple[Tuple[str, str], ...]                     # (package item name, predicate id): if the predicate holds, production readiness is FALSE
    result_sha256: str = ""


def _gov_body(g) -> Tuple:
    return (g.version, g.amendment_sha256, g.claim_tier, g.flight_name, g.package_item_vocabulary, g.required_package_items, g.production_prerequisites, g.branch_stopping)


def validate_governance(g, **ctx) -> None:
    """Grammar only: typed, closed alphabets, internal consistency. The values are Mike's."""
    if type(g) is not E1RGovernance or type(g.version) is not int or g.version < 1 or not _is_hex(g.amendment_sha256, 64): raise RunnerDomainError("governance record malformed")
    if not (isinstance(g.claim_tier, str) and g.claim_tier and isinstance(g.flight_name, str) and g.flight_name): raise RunnerDomainError("governance claim tier and flight name required")
    for name, tup in (("vocabulary", g.package_item_vocabulary), ("required items", g.required_package_items)):
        if type(tup) is not tuple or any(not isinstance(x, str) or not x for x in tup) or len(set(tup)) != len(tup): raise RunnerDomainError(f"governance {name} must be a tuple of unique names")
    if not g.package_item_vocabulary or not set(g.required_package_items) <= set(g.package_item_vocabulary): raise RunnerDomainError("required package items must lie in the vocabulary")
    pr = g.production_prerequisites
    if type(pr) is not tuple or any(type(e) is not tuple or len(e) != 3 or e[0] not in PREREQ_VOCAB or e[1] not in PREREQ_KINDS or e[2] not in PREREQ_REQUIREMENTS for e in pr): raise RunnerDomainError("production prerequisites must be (name, kind, requirement) triples in the declared alphabets")
    if len({e[0] for e in pr}) != len(pr): raise RunnerDomainError("production prerequisite names must be unique")
    bs = g.branch_stopping
    if type(bs) is not tuple or any(type(e) is not tuple or len(e) != 2 or e[0] not in g.package_item_vocabulary or e[1] not in PREDICATE_IDS for e in bs): raise RunnerDomainError("branch-stopping entries must name a vocabulary item and a declared predicate")
    if g.result_sha256 != _digest(_gov_body(g)): raise RunnerDomainError("governance identity does not recompute")


def load_governance(repo_root: str, stage) -> Tuple[E1RGovernance, str]:
    p = _gov(repo_root, GOVERNANCE_REL)
    if stage.governance_sha256 is None or not os.path.isfile(p) or _sha_file(p) != stage.governance_sha256: raise RunnerDomainError("no committed E1-R governance record is bound by this stage")
    g = _read_canonical(p)
    if type(g) is not E1RGovernance: raise RunnerDomainError("file is not an E1RGovernance record")
    validate_governance(g)
    return g, stage.governance_sha256


def _require_committed(repo_root: str, path: str) -> None:
    rel = os.path.relpath(os.path.abspath(path), os.path.abspath(repo_root)).replace(os.sep, "/")
    if rel.startswith("..") or not _committed_equals_working(repo_root, rel): raise RunnerDomainError(f"{rel} is not committed (equal to its git object)")


def _tree_digest(root: str) -> str:
    """Content digest of every file under `root` (paths and bytes, sorted) — recomputed from disk on every call."""
    acc = []
    for dp, _, fs in os.walk(root):
        for f in fs:
            fp = os.path.join(dp, f); acc.append((os.path.relpath(fp, root).replace(os.sep, "/"), _sha_file(fp)))
    return _digest(tuple(sorted(acc)))


_READINESS_MEMO: Dict[Tuple, Any] = {}
_ARTIFACT_REPLAY_MEMO: Dict[Tuple, bool] = {}
_CACHE_QUALIFICATION_MEMO: Dict[Tuple, str] = {}
_REACHABLE_MEMO: Dict[Tuple, Tuple[int, ...]] = {}


def _frozen_code_key() -> Tuple[str, ...]:
    return (_A.AUDIT_DECLARATION_SHA256_LITERAL, _A.GENERATOR_DECLARATION_SHA256_LITERAL, _V.VERDICT_DECLARATION_SHA256_LITERAL, _N.NULL_DECLARATION_SHA256_LITERAL,
            _C.E1_DECLARATION_SHA256_LITERAL, _K.CLASSIFY_SHA256_LITERAL, _P.PROJECTION_DECLARATION_SHA256_LITERAL, RUNNER_DECLARATION_SHA256_LITERAL)


def _qualify_cache_memoized(repo_root: str, file_digests: Tuple[str, ...]) -> str:
    key = (file_digests, _frozen_code_key())
    if key not in _CACHE_QUALIFICATION_MEMO:
        try: pc = _A.load_production_cache(os.path.join(repo_root, CACHE_FILES[0][0]), os.path.join(repo_root, CACHE_FILES[1][0]))
        except Exception as e: raise ApparatusHalt(f"production cache does not qualify through M6's loader: {type(e).__name__}: {str(e)[:100]}")
        if not _A.is_production_cache(pc): raise ApparatusHalt("production cache is not production_frozen under M6's derivation")
        if (_A.PRODUCTION_CACHE_FILE_SHA256_LITERAL, _A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL) != file_digests: raise ApparatusHalt("cache file digests differ from M6's literals")
        _CACHE_QUALIFICATION_MEMO[key] = pc.body_sha256
    return _CACHE_QUALIFICATION_MEMO[key]


def _reachable_surface() -> Tuple[int, ...]:
    """M6's reachable pass-2 surface, memoized on the frozen M4/M6 declaration identities (a pure function of frozen code)."""
    key = _frozen_code_key()
    if key not in _REACHABLE_MEMO: _REACHABLE_MEMO[key] = tuple(_A.reachable_pass2_levels())
    return _REACHABLE_MEMO[key]


def _no_dup(pairs):
    d = {}
    for k, v in pairs:
        if k in d: raise RunnerDomainError(f"duplicate JSON key {k!r}")
        d[k] = v
    return d


def bind_stage(repo_root: str, pinned_root: Optional[str] = None) -> StageIdentity:
    f = _derive_stage(repo_root, pinned_root)
    return StageIdentity(**f, result_sha256=_digest(_stage_body(StageIdentity(**f))))


def validate_stage_identity(s, repo_root: str, pinned_root: Optional[str] = None) -> None:
    if type(s) is not StageIdentity or s.role not in STAGE_ROLES: raise RunnerDomainError("exact StageIdentity with a known role required")
    f = _derive_stage(repo_root, pinned_root)
    for k, v in f.items():
        if k == "head_commit": continue                                            # descriptive only
        if getattr(s, k) != v: raise RunnerDomainError(f"stage field {k} does not re-derive from the repository")
    if s.result_sha256 != _digest(_stage_body(s)): raise RunnerDomainError("stage identity does not recompute")


# ----------------------------------------------------------------------------- authorization records (Mike's)
@dataclass(frozen=True)
class AuthorizationRecord:
    version: int
    issued: str                                  # ISO date
    issuer: str                                  # ratifier
    stage_sha256: str                            # the exact bound StageIdentity this authorization is for
    amendment_sha256: str
    governance_sha256: str
    package_spec_sha256: str
    authorized_jobs: Tuple[str, ...]
    tranche_authorized: bool
    tranche_levels_micro: Tuple[int, ...]
    tranche_seeds: Tuple[int, ...]
    production_authorized: bool
    prerequisite_manifest_sha256: str            # file identity of the committed PRODUCTION_PREREQUISITES.json ("" unless production is authorized)
    result_sha256: str = ""

    def __post_init__(self) -> None: _validate_authorization_structure(self)


def _validate_authorization_structure(a) -> None:
    """Stage-independent structure: a malformed authorization cannot be constructed at all."""
    if type(a.version) is not int or a.version < 1 or not isinstance(a.issued, str) or not a.issued or not isinstance(a.issuer, str) or not a.issuer: raise RunnerDomainError("authorization version/issued/issuer malformed")
    if type(a.authorized_jobs) is not tuple or any(j not in CANONICAL_JOBS for j in a.authorized_jobs) or len(set(a.authorized_jobs)) != len(a.authorized_jobs): raise RunnerDomainError("authorized jobs malformed")
    if type(a.tranche_authorized) is not bool or type(a.production_authorized) is not bool: raise RunnerDomainError("authorization flags must be exact bools")
    if a.tranche_authorized:
        if len(a.tranche_levels_micro) != TRANCHE_LEVELS or len(a.tranche_seeds) != TRANCHE_SEEDS or any(m not in E1_LEVELS_MICRO for m in a.tranche_levels_micro) or any(s not in E1_SEED_PANEL for s in a.tranche_seeds) \
                or len(set(a.tranche_levels_micro)) != TRANCHE_LEVELS or len(set(a.tranche_seeds)) != TRANCHE_SEEDS:
            raise RunnerDomainError("tranche panel must be exactly the declared count of distinct frozen levels and seeds")
    if a.production_authorized != _is_hex(a.prerequisite_manifest_sha256, 64) or (not a.production_authorized and a.prerequisite_manifest_sha256 != ""):
        raise RunnerDomainError("production authorization requires exactly one committed prerequisite-manifest identity (and none otherwise)")


_AUTH_FIELDS = tuple(f.name for f in dataclasses.fields(AuthorizationRecord) if f.name != "result_sha256")
def _auth_body(a) -> Tuple: return tuple(getattr(a, k) for k in _AUTH_FIELDS)


def validate_authorization(a, stage: StageIdentity) -> None:
    """An authorization is valid only for the exact canonical stage it names (structure re-checked; identity last)."""
    if type(a) is not AuthorizationRecord: raise RunnerDomainError("exact AuthorizationRecord required")
    _validate_authorization_structure(a)
    if type(stage) is not StageIdentity or stage.role != "canonical": raise RunnerDomainError("authorization requires a CANONICAL bound stage")
    if a.stage_sha256 != stage.result_sha256: raise RunnerDomainError("authorization names a different stage")
    if (a.amendment_sha256, a.governance_sha256, a.package_spec_sha256) != (stage.amendment_sha256, stage.governance_sha256, stage.package_spec_sha256): raise RunnerDomainError("authorization amendment/governance/package-spec identities differ from the stage")
    if a.result_sha256 != _digest(_auth_body(a)): raise RunnerDomainError("authorization identity does not recompute")


@dataclass(frozen=True)
class AuthorizationRegistry:
    """Mike-ratified registry binding each authorization version to its exact file identity (append-only: a version, once
    listed, can never change; the file's git history must hold exactly one commit)."""
    entries: Tuple[Tuple[int, str], ...]         # (version, file sha256), strictly increasing versions
    result_sha256: str = ""


def validate_registry(r, **ctx) -> None:
    if type(r) is not AuthorizationRegistry or type(r.entries) is not tuple or not r.entries: raise RunnerDomainError("authorization registry malformed or empty")
    vs = [e[0] for e in r.entries]
    if any(type(e) is not tuple or len(e) != 2 or type(e[0]) is not int or not _is_hex(e[1], 64) for e in r.entries) or vs != sorted(vs) or len(set(vs)) != len(vs) or vs[0] < 1: raise RunnerDomainError("registry entries must be strictly increasing versions with sha256 file identities")
    if r.result_sha256 != _digest(r.entries): raise RunnerDomainError("registry identity does not recompute")


def verify_registry_history(repo_root: str) -> None:
    """Append-only registry: every committed revision's entries must be a PREFIX of the next revision's (existing entries never change)."""
    rel = _pp.join(GOVERNANCE_ROOT_REL, AUTHORIZATION_REGISTRY_REL).replace(os.sep, "/")
    revs = _git(repo_root, "log", "--reverse", "--format=%H", "--", rel).splitlines(); prev: Tuple = ()
    for h in revs:
        blob = subprocess.run(["git", "-C", repo_root, "show", f"{h}:{rel}"], capture_output=True)
        if blob.returncode != 0: continue                                            # a revision that deleted the file is skipped; every later revision must still EXTEND the last committed entries
        doc = json.loads(blob.stdout.decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const); reg = _decode(doc)
        if type(reg) is not AuthorizationRegistry: raise RunnerDomainError(f"registry revision {h[:10]} is not an AuthorizationRegistry")
        if reg.entries[:len(prev)] != prev: raise RunnerDomainError(f"registry revision {h[:10]} alters existing entries (registry is append-only)")
        prev = reg.entries


def load_authorization(repo_root: str, stage: StageIdentity, version: int) -> Tuple[AuthorizationRecord, str]:
    """THE ONLY way an authorization enters a gate: the committed canonical file for `version`, listed in the committed
    registry at exactly that file identity, with exactly one commit in its history (append-only), validated against the stage.
    Returns (record, file sha256)."""
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
    hist = _git(repo_root, "log", "--format=%H", "--", _pp.join(GOVERNANCE_ROOT_REL, rel).replace(os.sep, "/")).splitlines()
    if len(hist) != 1: raise RunnerDomainError(f"authorization v{v} has {len(hist)} commits in its history: versions are append-only and immutable")
    a = _read_canonical(p)
    if type(a) is not AuthorizationRecord or a.version != v: raise RunnerDomainError("file is not the AuthorizationRecord of that version")
    validate_authorization(a, stage)
    return a, fsha


def require_authorized(stage: StageIdentity, repo_root: str, pinned_root: Optional[str], version: int, job: str) -> Tuple[AuthorizationRecord, str]:
    """THE gate in front of every canonical act: re-validated canonical stage; the COMMITTED authorization of `version` loaded by
    this function itself (no caller-supplied object is ever a grant); the job required. Returns (record, file sha256)."""
    if job not in CANONICAL_JOBS: raise RunnerDomainError(f"{job!r} is not a declared canonical job")
    validate_stage_identity(stage, repo_root, pinned_root)
    if stage.role != "canonical": raise RunnerDomainError(f"canonical act requires a canonical stage; bound stage is {stage.role}: {stage.environment_failures[:2]}")
    a, fsha = load_authorization(repo_root, stage, version)
    if job not in a.authorized_jobs: raise RunnerDomainError(f"job {job} is not authorized by record v{a.version} (source literals grant nothing)")
    return a, fsha


# ----------------------------------------------------------------------------- 2. persisted records (canonical bytes; validators on write and load)
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


def _envelope(obj, stage: StageIdentity, auth_sha: Optional[str], auth_file: Optional[str], auth_ver: Optional[int], job: Optional[str]) -> Dict[str, Any]:
    return {"type": type(obj).__name__, "record_schema_sha256": record_schema_identity(), "stage_sha256": stage.result_sha256, "authorization_sha256": auth_sha,
            "authorization_file_sha256": auth_file, "authorization_version": auth_ver, "job": job, "record": _encode(obj)}


def _write(obj, path, stage, env) -> str:
    text = _canon(env)
    with open(path, "w", newline="\n", encoding="utf-8") as f: f.write(text)
    return hashlib.sha256(text.encode()).hexdigest()


def persist_record(obj, path: str, stage: StageIdentity, repo_root: str, pinned_root: Optional[str] = None, **ctx) -> str:
    """PUBLIC: validate the stage AND the record, write canonical LF bytes with NO authorization binding (a non-canonical envelope)."""
    validate_stage_identity(stage, repo_root, pinned_root)
    typ = type(obj).__name__
    if typ not in VALIDATORS: raise RunnerDomainError(f"no validator registered for {typ}")
    VALIDATORS[typ](obj, stage=stage, repo_root=repo_root, pinned_root=pinned_root, **ctx)
    return _write(obj, path, stage, _envelope(obj, stage, None, None, None, None))


def _persist_canonical(obj, path, stage, repo_root, pinned_root, auth: AuthorizationRecord, auth_file: str, job: str, **ctx) -> str:
    """PRIVATE to run_canonical_job: the only writer of a canonical envelope; `auth` here is always the record the gate just loaded."""
    typ = type(obj).__name__
    VALIDATORS[typ](obj, stage=stage, repo_root=repo_root, pinned_root=pinned_root, **ctx)
    return _write(obj, path, stage, _envelope(obj, stage, auth.result_sha256, auth_file, auth.version, job))


def load_record(path: str, expected_type: str, stage: StageIdentity, repo_root: str, pinned_root: Optional[str] = None, *, require_job: Optional[str] = None, **ctx):
    """Canonical bytes only; duplicate keys and nonfinite constants refused; stage validated; exact schema rebuilt; the record's own
    validator run. With `require_job`, the envelope's authorization is LOADED FROM THE COMMITTED FILE of the envelope's version by this
    loader (never supplied), must equal the envelope's record and file identities, and must grant that job."""
    if expected_type not in VALIDATORS: raise RunnerDomainError(f"no validator registered for {expected_type}")
    raw = open(path, "rb").read()
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


# ----------------------------------------------------------------------------- 3. runner: derived LevelRecord, router manifest, prerequisites
RUN_MODES = ("production", "rehearsal")
GOVERNANCE_JOBS = ("production", "calibration_tranche")       # envelope job tokens granted by authorization FLAGS rather than the job list


@dataclass(frozen=True)
class RunProvenance:
    seed: int
    config_hash: str
    run_config_sha256: str
    rho_table_sha256: str
    telemetry_sha256: str
    verifier_checks_sha256: str
    conformance_checks_sha256: str
    verifier_passed: bool
    conformance_passed: bool
    status: str
    scoring_identity: str
    threshold_payload_sha256: str


@dataclass(frozen=True)
class LevelRecord:
    mode: str
    level_micro: int
    grid: int
    ticks: int
    pass_number: int                             # DERIVED: 1 iff the level is on the frozen pass-1 grid; 2 only through a validated router manifest
    router_manifest_sha256: str                  # file identity of the authorized router manifest ("" for pass 1)
    runs: Tuple[RunProvenance, ...]
    label: str
    cache_body_sha256: str
    cache_file_sha256: str
    cache_qualification_sha256: str
    stage_sha256: str
    authorization_version: int                   # 0 in rehearsal
    authorization_sha256: str
    authorization_file_sha256: str
    prerequisite_identities: Tuple[Tuple[str, str, str], ...]
    result_sha256: str = ""


_LEVEL_FIELDS = tuple(f.name for f in dataclasses.fields(LevelRecord) if f.name != "result_sha256")
def _level_body(r) -> Tuple: return tuple(getattr(r, k) for k in _LEVEL_FIELDS)


def _rerun_m1_on_artifacts(level_dir: str, seed: int, level_micro: int, grid: int, ticks: int):
    from ..verify import tier1_verify
    cfg = _C.e1_run_config(level_micro, seed, grid=grid, ticks=ticks)
    tp = os.path.join(level_dir, f"s{seed}.parquet"); rp = os.path.join(level_dir, f"s{seed}.rho_global.parquet"); cp = os.path.join(level_dir, f"s{seed}.run_config.json")
    for q in (tp, rp, cp):
        if not os.path.isfile(q): raise RunnerDomainError(f"artifact missing for seed {seed}: {os.path.basename(q)}")
    rep = tier1_verify(tp, cfg, rho_global_path=rp, expect_rho_global=True)
    run = _C.LevelRun(level_micro, level_id(level_micro), seed, cfg.config_hash(), cp, tp, rp, bool(rep.passed), "", (0, 0, 0), True)
    return cfg, rep, _C.conformance_preflight(run, cfg), tp, rp, cp


def _read_rho_series(path: str) -> np.ndarray:
    import pandas as pd
    t = pd.read_parquet(path)
    if list(t.columns) != ["Tick", "rho_global"] or t["rho_global"].dtype != np.float64: raise ApparatusHalt("persisted rho table schema differs from M1's")
    return t["rho_global"].to_numpy()


# ---- router manifest (the only way to a pass-2 level)
@dataclass(frozen=True)
class RouterManifest:
    pass1_records: Tuple[Tuple[int, str], ...]   # (level, persisted LevelRecord FILE identity) for all 24 pass-1 levels, in order
    pass1_labels: Tuple[str, ...]
    router_row: str
    insertions_micro: Tuple[int, ...]
    fallback_moves: Tuple[Tuple[int, int], ...]
    fallback_drops: Tuple[int, ...]
    reachable: Tuple[bool, ...]                  # per insertion: on M6's qualified reachable pass-2 surface
    stage_sha256: str
    result_sha256: str = ""


def _router_body(r) -> Tuple: return (r.pass1_records, r.pass1_labels, r.router_row, r.insertions_micro, r.fallback_moves, r.fallback_drops, r.reachable, r.stage_sha256)


def validate_router_manifest(r, stage=None, repo_root=None, pinned_root=None, records_dir: Optional[str] = None, cache=None, **ctx) -> None:
    """Derived: the router decision recomputed from the labels by M4; reachability from M6's surface; with `records_dir` every pass-1
    LevelRecord file re-hashed and loaded under the production authorization through its own (artifact-replaying) validator."""
    if type(r) is not RouterManifest: raise RunnerDomainError("exact RouterManifest required")
    if tuple(m for m, _ in r.pass1_records) != tuple(E1_LEVELS_MICRO) or any(not _is_hex(h, 64) for _, h in r.pass1_records) or len(r.pass1_labels) != len(E1_LEVELS_MICRO): raise RunnerDomainError("router manifest must cover exactly the frozen pass-1 grid")
    d = route(r.pass1_labels, E1_LEVELS_MICRO)
    if (r.router_row, r.insertions_micro, r.fallback_moves, r.fallback_drops) != (d.row, tuple(d.insertions_micro), tuple(d.fallback_moves), tuple(d.fallback_drops)): raise RunnerDomainError("router decision does not re-derive from the pass-1 labels")
    surf = set(_reachable_surface())
    if r.reachable != tuple(m in surf for m in r.insertions_micro): raise RunnerDomainError("reachability flags do not derive from M6's surface")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("router manifest belongs to a different stage")
    if records_dir is None or cache is None or stage is None or repo_root is None:
        raise RunnerDomainError("a RouterManifest validates only with its stage, repository, pass-1 records directory and the production cache (full replay)")
    if True:
        for (m, fsha), lab in zip(r.pass1_records, r.pass1_labels):
            fp = os.path.join(records_dir, f"{level_id(m)}.level.json")
            if not os.path.isfile(fp) or _sha_file(fp) != fsha: raise RunnerDomainError(f"pass-1 level record for {level_id(m)} absent or not the named identity")
            rec, _ = load_record(fp, "LevelRecord", stage, repo_root, pinned_root, require_job="production", level_dir=os.path.join(records_dir, level_id(m)), cache=cache, records_dir=records_dir)
            if rec.label != lab: raise RunnerDomainError(f"pass-1 label for {level_id(m)} differs from its level record")
    if r.result_sha256 != _digest(_router_body(r)): raise RunnerDomainError("router manifest identity does not recompute")


def build_router_manifest(records_dir: str, stage: StageIdentity, repo_root: str, pinned_root: Optional[str], authorization_version: int, cache) -> Tuple[RouterManifest, str]:
    """Production-gated: load the 24 persisted pass-1 level records, derive the router decision, persist the manifest canonically."""
    validate_stage_identity(stage, repo_root, pinned_root)
    if stage.role != "canonical": raise RunnerDomainError("the router manifest requires a canonical stage")
    auth, afile = load_authorization(repo_root, stage, authorization_version)
    if not auth.production_authorized: raise RunnerDomainError("the router manifest is a production act and requires production authorization")
    recs, labels = [], []
    for m in E1_LEVELS_MICRO:
        fp = os.path.join(records_dir, f"{level_id(m)}.level.json")
        if not os.path.isfile(fp): raise RunnerDomainError(f"pass-1 level {level_id(m)} has not been produced")
        rec, _ = load_record(fp, "LevelRecord", stage, repo_root, pinned_root, require_job="production", level_dir=os.path.join(records_dir, level_id(m)), cache=cache, records_dir=records_dir)
        recs.append((m, _sha_file(fp))); labels.append(rec.label)
    d = route(tuple(labels), E1_LEVELS_MICRO); surf = set(_reachable_surface())
    body = (tuple(recs), tuple(labels), d.row, tuple(d.insertions_micro), tuple(d.fallback_moves), tuple(d.fallback_drops), tuple(m in surf for m in d.insertions_micro), stage.result_sha256)
    rm = RouterManifest(*body, _digest(body)); path = os.path.join(records_dir, "router_manifest.json")
    _persist_canonical(rm, path, stage, repo_root, pinned_root, auth, afile, "production", records_dir=records_dir, cache=cache)
    return rm, path


# ---- production prerequisites (the committed manifest; the governance record's EXACT set)
@dataclass(frozen=True)
class PrerequisiteEntry:
    name: str                                    # in PREREQ_VOCAB
    record_type: str
    file: str                                    # path relative to the governance prerequisites directory
    file_sha256: str
    record_identity: str
    dependencies: Tuple[Tuple[str, str, str], ...]   # (validator role, relative file, file sha256): every context the validator needs, as committed files


@dataclass(frozen=True)
class ProductionPrerequisiteManifest:
    governance_sha256: str
    entries: Tuple[PrerequisiteEntry, ...]
    result_sha256: str = ""


def _manifest_body(m) -> Tuple: return (m.governance_sha256, tuple(dataclasses.astuple(e) for e in m.entries))


def validate_prerequisite_manifest(m, **ctx) -> None:
    if type(m) is not ProductionPrerequisiteManifest or not _is_hex(m.governance_sha256, 64) or type(m.entries) is not tuple or not m.entries: raise RunnerDomainError("prerequisite manifest malformed")
    for e in m.entries:
        if type(e) is not PrerequisiteEntry or e.name not in PREREQ_VOCAB or e.record_type != PREREQ_TYPES[e.name] or not _is_hex(e.file_sha256, 64) or not _is_hex(e.record_identity, 64): raise RunnerDomainError("prerequisite entry malformed")
        if ".." in e.file or os.path.isabs(e.file) or any(type(d) is not tuple or len(d) != 3 or d[0] not in PREREQ_DEPENDENCY_ROLES.get(e.record_type, ()) or ".." in d[1] or not _is_hex(d[2], 64) for d in e.dependencies):
            raise RunnerDomainError(f"prerequisite {e.name}: file/dependency entries malformed or not in the type's dependency schema")
        if {d[0] for d in e.dependencies} != set(PREREQ_DEPENDENCY_ROLES.get(e.record_type, ())) or len({d[0] for d in e.dependencies}) != len(e.dependencies): raise RunnerDomainError(f"prerequisite {e.name}: dependencies must be exactly the type's schema")
    if len({e.name for e in m.entries}) != len(m.entries): raise RunnerDomainError("prerequisite names must be unique")
    if m.result_sha256 != _digest(_manifest_body(m)): raise RunnerDomainError("prerequisite manifest identity does not recompute")


PREREQ_TYPES = {"stage1_package": "StagePackage", "calibration_tranche": "TrancheQuarantine", "resource_actuals": "ResourceBenchmark", "dense_reference": "ReferenceStructure",
                "reference_stability": "StabilityAudit", "m6_audit_qualification": "AuditQualification"}
PREREQ_JOBS = {"stage1_package": "stage1_package", "calibration_tranche": "calibration_tranche", "resource_actuals": "resource_benchmark", "dense_reference": "dense_reference",
               "reference_stability": "reference_stability", "m6_audit_qualification": "m6_audit_qualification"}
PREREQ_DEPENDENCY_ROLES = {"StabilityAudit": ("primary",), "AuditQualification": ("design", "held_out")}   # validator context roles, each a committed file


@dataclass(frozen=True)
class ProductionReadiness:
    """The two SEPARATE derived states: every required prerequisite VALID (and complete), and production READY (requirements met, no branch stopped)."""
    governance_sha256: str
    manifest_sha256: str
    rows: Tuple[Tuple[str, str, str, str, bool, bool], ...]   # (name, kind, requirement, record identity, valid_complete, passes)
    branch_stops: Tuple[Tuple[str, str, bool], ...]            # (item, predicate, holds)
    all_valid_complete: bool
    production_ready: bool


def validate_prerequisites(auth: AuthorizationRecord, stage: StageIdentity, repo_root: str, pinned_root: Optional[str], cache=None) -> ProductionReadiness:
    """Load the committed manifest the authorization names; require its names to EQUAL the governance record's production set; load each
    prerequisite at its exact file identity through its own validator with every dependency resolved from committed files; derive validity,
    passage and readiness per the governance record (pass → the item's pass predicate; valid_complete → its completeness predicate);
    evaluate the governance record's branch-stopping declarations on the loaded package items."""
    gov, gsha = load_governance(repo_root, stage)
    mp = _gov(repo_root, PREREQ_MANIFEST_REL); base = _gov(repo_root, PREREQUISITES_REL)
    # CONTENT-ADDRESSED MEMO (disclosed): key = every byte the validation reads (the whole prerequisites tree and the manifest, digested from
    # disk now) + the authorization, stage, governance and specification identities + frozen code. Only successful derivations are kept.
    key = (stage.result_sha256, auth.result_sha256, auth.prerequisite_manifest_sha256, _sha_file(mp) if os.path.isfile(mp) else "", _tree_digest(base) if os.path.isdir(base) else "",
           gsha, _digest(_gov_body(gov)), stage.package_spec_sha256, _frozen_code_key())   # keyed on the governance CONTENT used, not only its file identity
    if key in _READINESS_MEMO: return _READINESS_MEMO[key]
    rd = _validate_prerequisites_uncached(auth, stage, repo_root, pinned_root, gov, gsha, mp, base)
    _READINESS_MEMO[key] = rd
    return rd


def _validate_prerequisites_uncached(auth, stage, repo_root, pinned_root, gov, gsha, mp, base) -> "ProductionReadiness":
    if not os.path.isfile(mp) or _sha_file(mp) != auth.prerequisite_manifest_sha256 or not _committed_equals_working(repo_root, _pp.join(GOVERNANCE_ROOT_REL, PREREQ_MANIFEST_REL)):
        raise RunnerDomainError("the committed prerequisite manifest is absent or is not the one the authorization names")
    man = _read_canonical(mp)
    if type(man) is not ProductionPrerequisiteManifest: raise RunnerDomainError("file is not a ProductionPrerequisiteManifest")
    validate_prerequisite_manifest(man)
    if man.governance_sha256 != gsha: raise RunnerDomainError("prerequisite manifest names a different governance record")
    required = {n: (k, q) for n, k, q in gov.production_prerequisites}
    if {e.name for e in man.entries} != set(required): raise RunnerDomainError(f"prerequisite set differs from the governance record's exact production set: {sorted(required)}")
    rows = []; pkg = None; pkg_dir = None
    for e in man.entries:
        fp = os.path.join(base, e.file)
        if not os.path.isfile(fp) or _sha_file(fp) != e.file_sha256: raise RunnerDomainError(f"prerequisite {e.name} is absent or differs from its manifest file identity")
        _require_committed(repo_root, fp)
        ctxk: Dict[str, Any] = {}
        for role, rel, dsha in e.dependencies:
            dp = os.path.join(base, rel)
            if not os.path.isfile(dp) or _sha_file(dp) != dsha: raise RunnerDomainError(f"prerequisite {e.name} dependency {role} absent or not the named identity")
            _require_committed(repo_root, dp)
            dtype = {"primary": "ReferenceStructure", "design": "AuditRecord", "held_out": "AuditRecord"}[role]
            djob = {"primary": "dense_reference", "design": "m6_design_audit", "held_out": "m6_held_out_audit"}[role]
            ctxk[role] = load_record(dp, dtype, stage, repo_root, pinned_root, require_job=djob)[0]
        if e.record_type == "StagePackage": ctxk["package_dir"] = os.path.dirname(fp)
        if e.record_type == "ResourceBenchmark": ctxk["artifact_dir"] = os.path.join(os.path.dirname(fp), "benchmark_artifacts")
        if e.record_type == "TrancheQuarantine": ctxk["replay"] = True                 # an authorized passed tranche is proven by deterministic re-execution
        rec, _ = load_record(fp, e.record_type, stage, repo_root, pinned_root, require_job=PREREQ_JOBS[e.name], **ctxk)
        if _item_identity(rec) != e.record_identity: raise RunnerDomainError(f"prerequisite {e.name} record identity differs from the manifest")
        vc, ps = PREREQ_STATES[e.record_type](rec)
        if e.record_type == "StagePackage":
            pkg, pkg_dir = rec, os.path.dirname(fp)
            for row in rec.items: _require_committed(repo_root, os.path.join(pkg_dir, row[2]))
            for row in rec.items:
                if row[1] == "ResourceBenchmark":
                    for name, _, _ in R_BENCH_MANIFEST(os.path.join(pkg_dir, row[2])): _require_committed(repo_root, os.path.join(pkg_dir, "benchmark_artifacts", name))
        if e.record_type == "ResourceBenchmark":
            for name, _, _ in rec.artifact_manifest: _require_committed(repo_root, os.path.join(os.path.dirname(fp), "benchmark_artifacts", name))
        k, q = required[e.name]; rows.append((e.name, k, q, e.record_identity, vc, ps))
    stops = []
    for item, pred in gov.branch_stopping:                       # evaluated on the loaded, replay-validated package's items
        if pkg is None: raise RunnerDomainError("branch-stopping declarations require the stage-1 package among the prerequisites")
        row = next((r for r in pkg.items if r[0] == item), None)
        if row is None: raise RunnerDomainError(f"branch-stopping item {item} is not in the package")
        rec, _ = load_record(os.path.join(pkg_dir, row[2]), row[1], stage, repo_root, pinned_root, **_package_item_context(item, row[1], pkg, pkg_dir, stage, repo_root, pinned_root))
        stops.append((item, pred, _eval_predicate(pred, rec)))
    allvc = all(r[4] for r in rows)
    ready = allvc and all((r[5] if r[2] == "pass" else r[4]) for r in rows) and not any(h for _, _, h in stops)
    return ProductionReadiness(gsha, auth.prerequisite_manifest_sha256, tuple(rows), tuple(stops), allvc, ready)


def R_BENCH_MANIFEST(path: str):
    """The artifact manifest of a persisted ResourceBenchmark (read structurally; the record itself is validated by its own loader)."""
    doc = json.loads(open(path, "rb").read().decode("utf-8"), object_pairs_hook=_no_dup, parse_constant=_refuse_const)
    return tuple(tuple(e) for e in doc["record"]["fields"]["artifact_manifest"])


# per prerequisite type: (valid_complete, passes) — generic mechanics; the governance record decides which is REQUIRED
PREREQ_STATES = {
    "StagePackage": lambda r: (r.role == "canonical" and r.complete, r.role == "canonical" and r.complete and r.all_items_pass),
    "TrancheQuarantine": lambda r: (r.status in ("passed", "failed") and bool(r.authorization_sha256), r.status == "passed"),
    "ResourceBenchmark": lambda r: (r.role == "canonical", r.role == "canonical" and r.fits_with_margin),
    "ReferenceStructure": lambda r: (r.role == "reference_of_record", r.role == "reference_of_record" and r.structure_class != "REFERENCE-UNRESOLVED"),
    "StabilityAudit": lambda r: (r.role == "canonical" and r.complete, r.role == "canonical" and r.complete and r.within_delta_m_stab),
    "AuditQualification": lambda r: (True, r.qualified),
}


def validate_level_record(r, stage=None, level_dir: Optional[str] = None, cache=None, repo_root: Optional[str] = None, pinned_root: Optional[str] = None, records_dir: Optional[str] = None, **ctx) -> None:
    """DERIVED. Pass derived from the grid (pass 2 only through the named router manifest, which must list the level); config hashes from the
    contracted configuration; production context MANDATORY: artifacts re-hashed with M1 re-run, every series re-scored against the cache, the
    COMMITTED authorization reloaded (production flag, identities), and the prerequisites re-validated to the carried identities."""
    if type(r) is not LevelRecord or r.mode not in RUN_MODES: raise RunnerDomainError("exact LevelRecord with a known mode required")
    _P._level(r.level_micro)
    on_grid = r.level_micro in E1_LEVELS_MICRO
    if r.pass_number != (1 if on_grid else 2): raise RunnerDomainError("pass number does not derive from the frozen pass-1 grid")
    if on_grid != (r.router_manifest_sha256 == ""): raise RunnerDomainError("a pass-2 level requires a router manifest identity; a pass-1 level carries none")
    if tuple(x.seed for x in r.runs) != tuple(E1_SEED_PANEL): raise RunnerDomainError("a level record carries exactly the frozen twenty-seed panel in order")
    for x in r.runs:
        if type(x) is not RunProvenance or not all(_is_hex(h, 64) for h in (x.config_hash, x.run_config_sha256, x.rho_table_sha256, x.telemetry_sha256, x.verifier_checks_sha256, x.conformance_checks_sha256)) \
                or not (x.verifier_passed is True and x.conformance_passed is True): raise RunnerDomainError("every run must carry sha256 identities and both verifier and conformance passes")
        if x.config_hash != _C.e1_run_config(r.level_micro, x.seed, grid=r.grid, ticks=r.ticks).config_hash(): raise RunnerDomainError(f"config hash for seed {x.seed} does not re-derive from the contracted configuration")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("level record belongs to a different stage")
    if r.mode == "production":
        if (r.grid, r.ticks) != (E1_GRID, E1_TICKS): raise RunnerDomainError("production level requires the frozen production shape")
        if (r.cache_body_sha256, r.cache_file_sha256, r.cache_qualification_sha256) != (_A.PRODUCTION_CACHE_BODY_SHA256_LITERAL, _A.PRODUCTION_CACHE_FILE_SHA256_LITERAL, _A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL): raise RunnerDomainError("production level requires the source-literal cache bundle")
        if any(x.status not in _K.STATUSES or not _is_hex(x.scoring_identity, 64) or not _is_hex(x.threshold_payload_sha256, 64) for x in r.runs): raise RunnerDomainError("production runs require legal statuses and scoring identities")
        if r.label != level_label(level_counts(tuple(x.status for x in r.runs))): raise RunnerDomainError("level label does not re-derive from the statuses")
        if level_dir is None or cache is None or repo_root is None or stage is None: raise RunnerDomainError("a production level record validates only with its stage, repository, artifact directory and the production cache")
        auth, afile = load_authorization(repo_root, stage, r.authorization_version)
        if not auth.production_authorized or (auth.result_sha256, afile) != (r.authorization_sha256, r.authorization_file_sha256): raise RunnerDomainError("level record's production authorization does not reproduce from the committed record")
        rd = validate_prerequisites(auth, stage, repo_root, pinned_root, cache)
        if not rd.production_ready or tuple((n, rid, auth.prerequisite_manifest_sha256) for n, _, _, rid, _, _ in rd.rows) != r.prerequisite_identities: raise RunnerDomainError("level record's prerequisites do not re-validate to a production-ready state with the carried identities")
        if not on_grid:
            rdir = records_dir or os.path.dirname(level_dir); rp_ = os.path.join(rdir, "router_manifest.json")
            if not os.path.isfile(rp_) or _sha_file(rp_) != r.router_manifest_sha256: raise RunnerDomainError("the named router manifest is absent or differs")
            rm, _ = load_record(rp_, "RouterManifest", stage, repo_root, pinned_root, require_job="production", records_dir=rdir, cache=cache)
            if r.level_micro not in rm.insertions_micro: raise RunnerDomainError("pass-2 level is not an accepted insertion of the router manifest")
    else:
        if not on_grid: raise RunnerDomainError("rehearsal runs only on the frozen pass-1 grid")
        if r.label != "" or r.authorization_version != 0 or r.authorization_sha256 != "" or r.authorization_file_sha256 != "" or r.prerequisite_identities != () or any(x.status != "" or x.scoring_identity != "" or x.threshold_payload_sha256 != "" for x in r.runs):
            raise RunnerDomainError("a rehearsal level carries no classification, authorization or prerequisites")
    akey = (r.result_sha256, _tree_digest(level_dir) if level_dir is not None and os.path.isdir(level_dir) else "", getattr(cache, "body_sha256", ""), _frozen_code_key())
    if level_dir is not None and akey not in _ARTIFACT_REPLAY_MEMO:
        for x in r.runs:
            cfg, rep, conf, tp, rp, cp = _rerun_m1_on_artifacts(level_dir, x.seed, r.level_micro, r.grid, r.ticks)
            if (_sha_file(rp), _sha_file(tp), _sha_file(cp)) != (x.rho_table_sha256, x.telemetry_sha256, x.run_config_sha256): raise RunnerDomainError(f"persisted artifacts for seed {x.seed} differ from the record")
            if not rep.passed or not conf.passed: raise RunnerDomainError(f"re-run verifier/conformance fails on the artifacts of seed {x.seed}")
            if (_digest(tuple(sorted(rep.checks.items()))), _digest(tuple(sorted(conf.checks.items())))) != (x.verifier_checks_sha256, x.conformance_checks_sha256): raise RunnerDomainError(f"verifier/conformance check identities do not reproduce for seed {x.seed}")
            if r.mode == "production":
                th = cache.get(r.level_micro, x.seed)
                if (th.scoring_identity, th.payload_sha256) != (x.scoring_identity, x.threshold_payload_sha256): raise RunnerDomainError("run scoring identities differ from the cache")
                if run_status(_read_rho_series(rp), th.theta_p, th.theta_t)[0] != x.status: raise RunnerDomainError(f"status for seed {x.seed} does not re-derive from the persisted series")
        if r.result_sha256 == _digest(_level_body(r)): _ARTIFACT_REPLAY_MEMO[akey] = True
    if r.result_sha256 != _digest(_level_body(r)): raise RunnerDomainError("level record identity does not recompute")


def run_level(level_micro: int, out_dir: str, stage: StageIdentity, cache, mode: str, *, grid: int = E1_GRID, ticks: int = E1_TICKS,
              repo_root: Optional[str] = None, pinned_root: Optional[str] = None, authorization_version: Optional[int] = None) -> LevelRecord:
    """One level, all-or-nothing. The PASS is derived, never chosen: on-grid → pass 1; off-grid → pass 2 only if the authorized router
    manifest in out_dir lists the level. Production: the committed authorization (production flag) is loaded here, the prerequisites must
    re-validate to production READY, production shape and the derived cache are required, and the record is persisted canonically. A cache
    miss is APPARATUS on the qualified surface (pass 1, or a reachable pass-2 level) and EVALUABILITY only for a router output outside it."""
    verify_frozen_identity()
    if mode not in RUN_MODES: raise RunnerDomainError("unknown run mode")
    if type(stage) is not StageIdentity: raise RunnerDomainError("exact StageIdentity required")
    _P._level(level_micro); on_grid = level_micro in E1_LEVELS_MICRO; pass_number = 1 if on_grid else 2; rm_sha = ""; reachable = True
    auth = None; auth_file = ""; prereqs: Tuple = ()
    if mode == "rehearsal" and not on_grid: raise RunnerDomainError("rehearsal runs only on the frozen pass-1 grid")
    if mode == "production":
        if repo_root is None or authorization_version is None: raise RunnerDomainError("production requires the repository and an authorization version")
        validate_stage_identity(stage, repo_root, pinned_root)
        if stage.role != "canonical": raise RunnerDomainError("production requires a canonical stage")
        auth, auth_file = load_authorization(repo_root, stage, authorization_version)
        if not auth.production_authorized: raise RunnerDomainError(f"production is not authorized by record v{auth.version} (source literals grant nothing)")
        rd = validate_prerequisites(auth, stage, repo_root, pinned_root, cache)
        if not rd.production_ready: raise RunnerDomainError(f"production is not READY: valid/complete={rd.all_valid_complete}, branch stops={[s for s in rd.branch_stops if s[2]]}")
        prereqs = tuple((n, rid, auth.prerequisite_manifest_sha256) for n, _, _, rid, _, _ in rd.rows)
        if (grid, ticks) != (E1_GRID, E1_TICKS): raise RunnerDomainError("production requires the frozen production shape")
        if not _A.is_production_cache(cache): raise ApparatusHalt("production requires the derived production cache")
        if not on_grid:
            rp_ = os.path.join(out_dir, "router_manifest.json")
            if not os.path.isfile(rp_): raise RunnerDomainError("a pass-2 level requires the authorized router manifest")
            rm, _ = load_record(rp_, "RouterManifest", stage, repo_root, pinned_root, require_job="production", records_dir=out_dir, cache=cache)
            if level_micro not in rm.insertions_micro: raise RunnerDomainError("level is not an accepted insertion of the router manifest")
            rm_sha = _sha_file(rp_); reachable = rm.reachable[rm.insertions_micro.index(level_micro)]
    level_dir = os.path.join(out_dir, level_id(level_micro)); partial = level_dir + ".partial"
    if os.path.exists(partial): shutil.rmtree(partial)
    os.makedirs(partial)
    from ..verify import tier1_verify
    runs: List[RunProvenance] = []
    for seed in E1_SEED_PANEL:
        cfg = _C.e1_run_config(level_micro, seed, grid=grid, ticks=ticks)
        try: run = _C.run_level_run(cfg, partial, f"s{seed}")
        except Exception as e: raise ApparatusHalt(f"run failed at level {level_id(level_micro)} seed {seed}: {type(e).__name__}: {e}")
        cp = _C.conformance_preflight(run, cfg)
        if not (run.verifier_passed and cp.passed): raise ApparatusHalt(f"conformance/verifier failed at level {level_id(level_micro)} seed {seed}: {cp.summary()[:160]}")
        status = sid = psha = ""
        if mode == "production":
            try: th = cache.get(level_micro, seed)
            except _A.AuditDomainError as e:
                if not reachable: raise EvaluabilityHalt(f"pass-2 level {level_id(level_micro)} lies outside the qualified reachable surface: {e}")
                raise ApparatusHalt(f"production cache lacks a qualified key (level {level_id(level_micro)}, seed {seed}): {e}")
            try: status = run_status(_read_rho_series(run.rho_table_path), th.theta_p, th.theta_t)[0]
            except _K.ClassifyDomainError as e: raise AnomalyHalt(f"level {level_id(level_micro)} seed {seed}: {e}")
            sid, psha = th.scoring_identity, th.payload_sha256
        rep_ = tier1_verify(run.telemetry_path, cfg, rho_global_path=run.rho_table_path, expect_rho_global=True)
        runs.append(RunProvenance(int(seed), run.config_hash, _sha_file(run.run_config_path), _sha_file(run.rho_table_path), _sha_file(run.telemetry_path),
                                  _digest(tuple(sorted(rep_.checks.items()))), _digest(tuple(sorted(cp.checks.items()))), True, True, status, sid, psha))
    if os.path.exists(level_dir): shutil.rmtree(level_dir)
    os.replace(partial, level_dir)
    lab = level_label(level_counts(tuple(x.status for x in runs))) if mode == "production" else ""
    bundle = (cache.body_sha256, cache.file_sha256, cache.qualification_sha256) if mode == "production" else ("", "", "")
    body = dict(mode=mode, level_micro=int(level_micro), grid=int(grid), ticks=int(ticks), pass_number=pass_number, router_manifest_sha256=rm_sha, runs=tuple(runs), label=lab,
                cache_body_sha256=bundle[0], cache_file_sha256=bundle[1], cache_qualification_sha256=bundle[2], stage_sha256=stage.result_sha256,
                authorization_version=auth.version if auth else 0, authorization_sha256=auth.result_sha256 if auth else "", authorization_file_sha256=auth_file, prerequisite_identities=prereqs)
    rec = LevelRecord(**body, result_sha256=_digest(_level_body(LevelRecord(**body))))
    if mode == "production":
        _persist_canonical(rec, os.path.join(out_dir, f"{level_id(level_micro)}.level.json"), stage, repo_root, pinned_root, auth, auth_file, "production",
                           level_dir=level_dir, cache=cache, records_dir=out_dir)
    return rec


# ----------------------------------------------------------------------------- 4. calibration-tranche quarantine (gated; evidence replayable by deterministic re-execution)
@dataclass(frozen=True)
class TrancheQuarantine:
    """Integrity, invariant, cost and provenance ONLY. Never holds rho, statuses, labels or a profile. Per-run evidence (config, artifact
    and check-set identities) makes an authorized record provable by deterministic re-execution after the artifacts are deleted."""
    levels_micro: Tuple[int, ...]
    seeds: Tuple[int, ...]
    grid: int
    ticks: int
    n_runs: int
    config_hashes: Tuple[str, ...]
    rho_table_sha256: Tuple[str, ...]
    telemetry_sha256: Tuple[str, ...]
    verifier_checks_sha256: Tuple[str, ...]
    conformance_checks_sha256: Tuple[str, ...]
    verifier_passed: Tuple[bool, ...]
    conformance_passed: Tuple[bool, ...]
    wall_clock_s: float
    bytes_written: int
    cleanup_proven: bool
    status: str
    stage_sha256: str
    authorization_version: int
    authorization_sha256: str
    authorization_file_sha256: str
    result_sha256: str = ""

    def __getattr__(self, name): raise QuarantineViolation(f"the calibration-tranche quarantine exposes no {name!r}: integrity, invariant, cost and provenance only")


_Q_FIELDS = tuple(f.name for f in dataclasses.fields(TrancheQuarantine) if f.name != "result_sha256")
def _q_body(q) -> Tuple: return tuple(getattr(q, k) for k in _Q_FIELDS)
_QUARANTINE_BLOCKED = ("profile", "rho", "labels", "statuses", "label", "verdict", "series", "levels")


def validate_quarantine(q, stage=None, repo_root=None, pinned_root=None, replay: bool = False, **ctx) -> None:
    """Structure, finite non-negative costs, derived status, re-derived config hashes; an AUTHORIZED record reloads its committed authorization
    (tranche flag, exact panel, identities) and requires production shape; replay=True re-executes the panel and requires every per-run identity."""
    if type(q) is not TrancheQuarantine: raise RunnerDomainError("exact TrancheQuarantine required")
    n = len(q.levels_micro) * len(q.seeds)
    vecs = (q.config_hashes, q.rho_table_sha256, q.telemetry_sha256, q.verifier_checks_sha256, q.conformance_checks_sha256, q.verifier_passed, q.conformance_passed)
    if q.n_runs != n or any(len(v) != n for v in vecs): raise RunnerDomainError("tranche provenance vectors inconsistent")
    if any(not _is_hex(h, 64) for v in vecs[:5] for h in v) or type(q.cleanup_proven) is not bool or q.status not in ("passed", "failed"): raise RunnerDomainError("tranche provenance malformed")
    if not (type(q.wall_clock_s) is float and np.isfinite(q.wall_clock_s) and q.wall_clock_s >= 0.0) or type(q.bytes_written) is not int or q.bytes_written < 0: raise RunnerDomainError("tranche cost fields must be finite and non-negative")
    expect = "passed" if (all(q.verifier_passed) and all(q.conformance_passed) and q.cleanup_proven and n == TRANCHE_SEEDS * TRANCHE_LEVELS) else "failed"
    if q.status != expect: raise RunnerDomainError("tranche status does not derive from its verifier/conformance/cleanup facts")
    for i, (m, s) in enumerate((m, s) for m in q.levels_micro for s in q.seeds):
        if q.config_hashes[i] != _C.e1_run_config(int(m), int(s), grid=q.grid, ticks=q.ticks).config_hash(): raise RunnerDomainError("tranche config hashes do not re-derive from the contracted configurations")
    if stage is not None and q.stage_sha256 != stage.result_sha256: raise RunnerDomainError("quarantine belongs to a different stage")
    authorized = bool(q.authorization_sha256 or q.authorization_file_sha256 or q.authorization_version)
    if authorized:
        if (q.grid, q.ticks) != (E1_GRID, E1_TICKS): raise RunnerDomainError("an authorized tranche runs at production shape")
        if repo_root is None or stage is None: raise RunnerDomainError("an authorized tranche validates only against its committed authorization")
        a, afile = load_authorization(repo_root, stage, q.authorization_version)
        if not a.tranche_authorized or (a.result_sha256, afile) != (q.authorization_sha256, q.authorization_file_sha256) or (q.levels_micro, q.seeds) != (a.tranche_levels_micro, a.tranche_seeds):
            raise RunnerDomainError("tranche panel/identities do not reproduce from the committed tranche authorization")
    if replay:
        import tempfile
        d = tempfile.mkdtemp()
        try:
            r2 = _tranche_execute(q.levels_micro, q.seeds, d, stage if stage is not None else _StageStub(q.stage_sha256), q.grid, q.ticks, q.authorization_version, q.authorization_sha256, q.authorization_file_sha256)
        finally: shutil.rmtree(d, ignore_errors=True)
        if (r2.rho_table_sha256, r2.telemetry_sha256, r2.verifier_checks_sha256, r2.conformance_checks_sha256, r2.verifier_passed, r2.conformance_passed) != \
           (q.rho_table_sha256, q.telemetry_sha256, q.verifier_checks_sha256, q.conformance_checks_sha256, q.verifier_passed, q.conformance_passed):
            raise RunnerDomainError("tranche evidence does not reproduce by deterministic re-execution")
    if q.result_sha256 != _digest(_q_body(q)): raise RunnerDomainError("quarantine identity does not recompute")


@dataclass(frozen=True)
class _StageStub:
    result_sha256: str


def _tranche_execute(levels, seeds, out_dir, stage, grid, ticks, auth_ver, auth_sha, auth_file) -> TrancheQuarantine:
    from ..verify import tier1_verify
    sealed = os.path.join(out_dir, ".tranche_sealed"); shutil.rmtree(sealed, ignore_errors=True); os.makedirs(sealed)
    ch, rs, ts, vk, ck, vp, cpd = [], [], [], [], [], [], []; nbytes = 0; t0 = time.perf_counter(); n = 0; written: List[str] = []
    try:
        for m in levels:
            for s in seeds:
                cfg = _C.e1_run_config(int(m), int(s), grid=grid, ticks=ticks)
                run = _C.run_level_run(cfg, sealed, f"t{n}"); cp = _C.conformance_preflight(run, cfg)
                rep = tier1_verify(run.telemetry_path, cfg, rho_global_path=run.rho_table_path, expect_rho_global=True)
                ch.append(run.config_hash); rs.append(_sha_file(run.rho_table_path)); ts.append(_sha_file(run.telemetry_path))
                vk.append(_digest(tuple(sorted(rep.checks.items())))); ck.append(_digest(tuple(sorted(cp.checks.items())))); vp.append(bool(rep.passed)); cpd.append(bool(cp.passed)); n += 1
                written += [run.telemetry_path, run.rho_table_path, run.run_config_path]
                nbytes += sum(os.path.getsize(p) for p in (run.telemetry_path, run.rho_table_path, run.run_config_path))
    finally:
        shutil.rmtree(sealed, ignore_errors=True)
    wall = float(time.perf_counter() - t0)
    clean = (not os.path.exists(sealed)) and not any(os.path.exists(p) for p in written) and n == len(levels) * len(seeds)
    status = "passed" if (all(vp) and all(cpd) and clean and n == TRANCHE_SEEDS * TRANCHE_LEVELS) else "failed"
    body = dict(levels_micro=tuple(int(x) for x in levels), seeds=tuple(int(x) for x in seeds), grid=grid, ticks=ticks, n_runs=n, config_hashes=tuple(ch), rho_table_sha256=tuple(rs),
                telemetry_sha256=tuple(ts), verifier_checks_sha256=tuple(vk), conformance_checks_sha256=tuple(ck), verifier_passed=tuple(vp), conformance_passed=tuple(cpd),
                wall_clock_s=wall, bytes_written=int(nbytes), cleanup_proven=bool(clean), status=status, stage_sha256=stage.result_sha256,
                authorization_version=auth_ver, authorization_sha256=auth_sha, authorization_file_sha256=auth_file)
    return TrancheQuarantine(**body, result_sha256=_digest(_q_body(TrancheQuarantine(**body))))


def run_tranche(out_dir: str, stage: StageIdentity, repo_root: str, pinned_root: Optional[str], authorization_version: int) -> Tuple[TrancheQuarantine, str]:
    """THE authorized tranche: canonical stage; the COMMITTED authorization loaded here (tranche flag, exact panel); production shape;
    persisted canonically under the envelope job 'calibration_tranche'. Returns (record, persisted path)."""
    verify_frozen_identity(); validate_stage_identity(stage, repo_root, pinned_root)
    if stage.role != "canonical": raise RunnerDomainError("the tranche requires a canonical stage")
    auth, fsha = load_authorization(repo_root, stage, authorization_version)
    if not auth.tranche_authorized: raise RunnerDomainError(f"the calibration tranche is not authorized by record v{auth.version} (source literals grant nothing)")
    q = _tranche_execute(auth.tranche_levels_micro, auth.tranche_seeds, out_dir, stage, E1_GRID, E1_TICKS, auth.version, auth.result_sha256, fsha)
    path = os.path.join(out_dir, "calibration_tranche.json")
    _persist_canonical(q, path, stage, repo_root, pinned_root, auth, fsha, "calibration_tranche")
    return q, path


def _tranche_for_tests(levels, seeds, out_dir, stage, *, grid: int, ticks: int) -> TrancheQuarantine:
    """PRIVATE test helper: below production shape; carries no authorization; never canonical."""
    if (grid, ticks) == (E1_GRID, E1_TICKS): raise RunnerDomainError("the test helper may not run at production shape")
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
    config_hashes: Tuple[str, ...]
    artifact_manifest: Tuple[Tuple[str, str, int], ...]   # (file name, sha256, byte size) for every retained artifact: telemetry, rho, run-config per seed
    telemetry_bytes_per_run: Tuple[int, ...]
    rho_bytes_per_run: Tuple[int, ...]
    parquet_row_groups: int
    wall_clock_per_run_s: Tuple[float, ...]               # measured assertions (finite, positive) bound to the manifest
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


def validate_benchmark(b, stage=None, repo_root=None, pinned_root=None, artifact_dir: Optional[str] = None, **ctx) -> None:
    """Derived: config hashes; domains; projections; with `artifact_dir` (MANDATORY for canonical) every manifest file's identity AND size is
    re-derived, per-run byte counts equal the file sizes, the row-group count is reproduced, and M1 re-runs on the artifacts; a canonical record
    reloads its committed authorization (benchmark job) and uses the frozen panel."""
    import pyarrow.parquet as pq
    if type(b) is not ResourceBenchmark or b.role not in ("canonical", "smoke"): raise RunnerDomainError("exact ResourceBenchmark required")
    n = len(b.seeds)
    if not (1 <= n <= 20 and n == len(b.config_hashes) == len(b.telemetry_bytes_per_run) == len(b.rho_bytes_per_run) == len(b.wall_clock_per_run_s) == len(b.readback_s_per_run)) or len(b.artifact_manifest) != 3 * n:
        raise RunnerDomainError("measurement vectors inconsistent")
    if any(s not in E1_SEED_PANEL for s in b.seeds) or any(type(x) is not float or not np.isfinite(x) or x <= 0.0 for x in b.wall_clock_per_run_s + b.readback_s_per_run) \
            or any(type(x) is not int or x <= 0 for x in b.telemetry_bytes_per_run + b.rho_bytes_per_run) or type(b.free_bytes_measured) is not int or b.free_bytes_measured < 0 or type(b.parquet_row_groups) is not int or b.parquet_row_groups < 1:
        raise RunnerDomainError("benchmark measurements out of domain")
    _P._level(b.level_micro)
    for i, s in enumerate(b.seeds):
        if b.config_hashes[i] != _C.e1_run_config(b.level_micro, s, grid=b.grid, ticks=b.ticks).config_hash(): raise RunnerDomainError("benchmark config hashes do not re-derive")
    pw = PRODUCTION_RUNS * max(b.wall_clock_per_run_s) * (1 + BENCHMARK_MARGIN); pb = int(PRODUCTION_RUNS * max(t + r for t, r in zip(b.telemetry_bytes_per_run, b.rho_bytes_per_run)) * (1 + BENCHMARK_MARGIN))
    if (b.projected_wall_clock_s, b.projected_bytes, b.fits_with_margin) != (pw, pb, pb <= b.free_bytes_measured): raise RunnerDomainError("projections do not derive from the measurements")
    if stage is not None and b.stage_sha256 != stage.result_sha256: raise RunnerDomainError("benchmark belongs to a different stage")
    if b.role == "canonical":
        if (b.grid, b.ticks) != (E1_GRID, E1_TICKS) or (b.level_micro, b.seeds) != (BENCHMARK_LEVEL_MICRO, tuple(E1_SEED_PANEL[:BENCHMARK_SEEDS])): raise RunnerDomainError("a canonical benchmark uses production shape and the frozen panel")
        if artifact_dir is None or repo_root is None or stage is None: raise RunnerDomainError("a canonical benchmark validates only with its kept artifacts and its committed authorization")
        a, afile = load_authorization(repo_root, stage, b.authorization_version)
        if "resource_benchmark" not in a.authorized_jobs or (a.result_sha256, afile) != (b.authorization_sha256, b.authorization_file_sha256): raise RunnerDomainError("benchmark authorization does not reproduce from the committed record")
    elif b.authorization_version or b.authorization_sha256 or b.authorization_file_sha256: raise RunnerDomainError("a smoke benchmark carries no authorization")
    expected = tuple(f"s{s}{suf}" for s in b.seeds for suf in (".parquet", ".rho_global.parquet", ".run_config.json"))
    if tuple(n for n, _, _ in b.artifact_manifest) != expected: raise RunnerDomainError("artifact manifest must be exactly telemetry, rho and run-config per seed, unique, in canonical order")
    for i, s in enumerate(b.seeds):
        if b.artifact_manifest[3 * i + 2][1] != _C.e1_run_config(b.level_micro, s, grid=b.grid, ticks=b.ticks).config_hash(): raise RunnerDomainError(f"run-config identity for seed {s} is not the contracted configuration's")
    if artifact_dir is not None:
        names = []
        for name, sha, size in b.artifact_manifest:
            fp = os.path.join(artifact_dir, name)
            if not os.path.isfile(fp) or _sha_file(fp) != sha or os.path.getsize(fp) != size: raise RunnerDomainError(f"benchmark artifact {name} absent or differs from its manifest entry")
            names.append(name)
        rg = 0
        for i, s in enumerate(b.seeds):
            if dict((nm, sz) for nm, _, sz in b.artifact_manifest).get(f"s{s}.parquet") != b.telemetry_bytes_per_run[i] or dict((nm, sz) for nm, _, sz in b.artifact_manifest).get(f"s{s}.rho_global.parquet") != b.rho_bytes_per_run[i]:
                raise RunnerDomainError("per-run byte counts differ from the retained file sizes")
            cfg, rep, conf, tp, rp, cp = _rerun_m1_on_artifacts(artifact_dir, s, b.level_micro, b.grid, b.ticks)
            if not (rep.passed and conf.passed): raise RunnerDomainError(f"benchmark artifacts for seed {s} do not re-verify")
            rg = max(rg, pq.ParquetFile(tp).num_row_groups)
        if rg != b.parquet_row_groups: raise RunnerDomainError("parquet row-group count does not reproduce from the retained artifacts")
    if b.result_sha256 != _digest(_b_body(b)): raise RunnerDomainError("benchmark identity does not recompute")


def _benchmark_execute(n_runs, out_dir, stage, grid, ticks, level_micro, role, auth_ver, auth_sha, auth_file) -> ResourceBenchmark:
    import pandas as pd, pyarrow.parquet as pq
    d = os.path.join(out_dir, "benchmark_artifacts"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    ch, man, walls, tb, rb, rbk = [], [], [], [], [], []; rgs = 0
    try:
        for seed in E1_SEED_PANEL[:n_runs]:
            cfg = _C.e1_run_config(level_micro, seed, grid=grid, ticks=ticks)
            t0 = time.perf_counter(); run = _C.run_level_run(cfg, d, f"s{seed}"); walls.append(float(time.perf_counter() - t0))
            cp = _C.conformance_preflight(run, cfg)
            if not (run.verifier_passed and cp.passed): raise ApparatusHalt(f"benchmark run seed {seed}: verifier/conformance failed")
            ch.append(run.config_hash)
            for fp in (run.telemetry_path, run.rho_table_path, run.run_config_path): man.append((os.path.basename(fp), _sha_file(fp), int(os.path.getsize(fp))))
            tb.append(int(os.path.getsize(run.telemetry_path))); rb.append(int(os.path.getsize(run.rho_table_path)))
            t1 = time.perf_counter(); _sha_file(run.telemetry_path); _sha_file(run.rho_table_path); pd.read_parquet(run.telemetry_path); pd.read_parquet(run.rho_table_path); rbk.append(max(float(time.perf_counter() - t1), 1e-9))
            rgs = max(rgs, pq.ParquetFile(run.telemetry_path).num_row_groups)
        free = int(shutil.disk_usage(out_dir).free)
    except Exception:
        shutil.rmtree(d, ignore_errors=True); raise
    pw = PRODUCTION_RUNS * max(walls) * (1 + BENCHMARK_MARGIN); pb = int(PRODUCTION_RUNS * max(t + r for t, r in zip(tb, rb)) * (1 + BENCHMARK_MARGIN))
    body = dict(role=role, level_micro=int(level_micro), seeds=tuple(E1_SEED_PANEL[:n_runs]), grid=grid, ticks=ticks, config_hashes=tuple(ch), artifact_manifest=tuple(man),
                telemetry_bytes_per_run=tuple(tb), rho_bytes_per_run=tuple(rb), parquet_row_groups=rgs, wall_clock_per_run_s=tuple(walls), readback_s_per_run=tuple(rbk),
                projected_wall_clock_s=pw, projected_bytes=pb, free_bytes_measured=free, fits_with_margin=pb <= free, stage_sha256=stage.result_sha256,
                authorization_version=auth_ver, authorization_sha256=auth_sha, authorization_file_sha256=auth_file)
    return ResourceBenchmark(**body, result_sha256=_digest(_b_body(ResourceBenchmark(**body))))


def run_benchmark_smoke(n_runs: int, out_dir: str, stage: StageIdentity, *, grid: int, ticks: int, level_micro: int = E1_LEVELS_MICRO[12]) -> ResourceBenchmark:
    verify_frozen_identity()
    if (grid, ticks) == (E1_GRID, E1_TICKS): raise RunnerDomainError("the smoke benchmark may not run at production shape")
    if isinstance(n_runs, bool) or not isinstance(n_runs, int) or not 1 <= n_runs <= 20: raise RunnerDomainError("n_runs must be 1..20")
    return _benchmark_execute(n_runs, out_dir, stage, grid, ticks, level_micro, "smoke", 0, "", "")


# ----------------------------------------------------------------------------- typed per-item package records (each derives)
@dataclass(frozen=True)
class LevelListRecord:
    levels_micro: Tuple[int, ...]
    spacings_micro: Tuple[int, ...]
    max_spacing_micro: int
    stage_sha256: str
    result_sha256: str = ""


def level_list_record(stage: StageIdentity) -> LevelListRecord:
    lv = tuple(E1_LEVELS_MICRO); sp = tuple(b - a for a, b in zip(lv, lv[1:]))
    return LevelListRecord(lv, sp, max(sp), stage.result_sha256, _digest((lv, sp, max(sp), stage.result_sha256)))


def validate_level_list(r, stage=None, **ctx) -> None:
    if type(r) is not LevelListRecord or r.levels_micro != tuple(E1_LEVELS_MICRO) or r.spacings_micro != tuple(b - a for a, b in zip(r.levels_micro, r.levels_micro[1:])) or r.max_spacing_micro != max(r.spacings_micro) != 0 and r.max_spacing_micro != _C.S_P1_MAX_MICRO:
        raise RunnerDomainError("level list does not derive from the frozen levels")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("level list belongs to a different stage")
    if r.result_sha256 != _digest((r.levels_micro, r.spacings_micro, r.max_spacing_micro, r.stage_sha256)): raise RunnerDomainError("level list identity does not recompute")


@dataclass(frozen=True)
class EnsembleSizesRecord:
    production_runs: int
    morphology_sweeps_per_class: int
    design_stability_sweeps: int
    tolerance_replicates: int
    dense_points: int
    stage_sha256: str
    result_sha256: str = ""


def ensemble_sizes_record(stage: StageIdentity) -> EnsembleSizesRecord:
    v = (PRODUCTION_RUNS, _A.SWEEPS_PER_CLASS, _P.DESIGN_STABILITY_SWEEPS, _P.TOLERANCE_REPLICATES, _P.DENSE_POINTS)
    return EnsembleSizesRecord(*v, stage.result_sha256, _digest((v, stage.result_sha256)))


def validate_ensemble_sizes(r, stage=None, **ctx) -> None:
    v = (PRODUCTION_RUNS, _A.SWEEPS_PER_CLASS, _P.DESIGN_STABILITY_SWEEPS, _P.TOLERANCE_REPLICATES, _P.DENSE_POINTS)
    if type(r) is not EnsembleSizesRecord or (r.production_runs, r.morphology_sweeps_per_class, r.design_stability_sweeps, r.tolerance_replicates, r.dense_points) != v: raise RunnerDomainError("ensemble sizes differ from the declared programs")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("ensemble sizes belong to a different stage")
    if r.result_sha256 != _digest((v, r.stage_sha256)): raise RunnerDomainError("ensemble sizes identity does not recompute")


@dataclass(frozen=True)
class ClosurePublication:
    """R1a publication: closure validation figures at declared levels and the fixed-point census; re-derived by the validator."""
    levels_micro: Tuple[int, ...]
    mc_samples: int
    validation: Tuple[Tuple[int, Tuple[Tuple[str, float], ...]], ...]
    census_counts: Tuple[int, ...]
    census_changes: int
    stage_sha256: str
    result_sha256: str = ""


def closure_publication(levels: Sequence[int], mc_samples: int, stage: StageIdentity) -> ClosurePublication:
    lv = tuple(_P._level(x) for x in levels)
    val = tuple((m, tuple(sorted(_P.closure_validation(m, mc_samples=mc_samples).items()))) for m in lv)
    c = _P.fixed_point_census(lv)
    body = (lv, int(mc_samples), val, c.counts, c.structure_changes, stage.result_sha256)
    return ClosurePublication(*body, _digest(body))


def validate_closure_publication(r, stage=None, **ctx) -> None:
    if type(r) is not ClosurePublication: raise RunnerDomainError("exact ClosurePublication required")
    val = tuple((m, tuple(sorted(_P.closure_validation(m, mc_samples=r.mc_samples).items()))) for m in r.levels_micro); c = _P.fixed_point_census(r.levels_micro)
    if (r.validation, r.census_counts, r.census_changes) != (val, c.counts, c.structure_changes): raise RunnerDomainError("closure publication does not re-derive")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("closure publication belongs to a different stage")
    if r.result_sha256 != _digest((r.levels_micro, r.mc_samples, r.validation, r.census_counts, r.census_changes, r.stage_sha256)): raise RunnerDomainError("closure publication identity does not recompute")


@dataclass(frozen=True)
class NullPrecisionRecord:
    """Per level: the reference null's threshold modes and halts, re-derived by the validator through M3."""
    levels_micro: Tuple[int, ...]
    modes: Tuple[Tuple[str, str], ...]
    halts: Tuple[str, ...]
    stage_sha256: str
    result_sha256: str = ""


def _null_precision(levels):
    modes, halts = [], []
    for m in levels:
        try: modes.append(tuple(_N.reference_thresholds(m).threshold_modes))
        except _N.NullDomainError as e:
            if "no support point" in str(e) or "not certified" in str(e): halts.append(level_id(m)); modes.append(("halt", "halt"))
            else: raise
    return tuple(modes), tuple(halts)


def null_precision_record(levels: Sequence[int], stage: StageIdentity) -> NullPrecisionRecord:
    lv = tuple(_P._level(x) for x in levels); md, h = _null_precision(lv)
    return NullPrecisionRecord(lv, md, h, stage.result_sha256, _digest((lv, md, h, stage.result_sha256)))


def validate_null_precision(r, stage=None, **ctx) -> None:
    if type(r) is not NullPrecisionRecord: raise RunnerDomainError("exact NullPrecisionRecord required")
    if (r.modes, r.halts) != _null_precision(r.levels_micro): raise RunnerDomainError("null precision does not re-derive through M3")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("null precision belongs to a different stage")
    if r.result_sha256 != _digest((r.levels_micro, r.modes, r.halts, r.stage_sha256)): raise RunnerDomainError("null precision identity does not recompute")


@dataclass(frozen=True)
class RouterCollisionRecord:
    """M4's reachable-surface facts, re-derived: reachable bands, bands whose nominal insertions collide, reachable pass-2 levels."""
    reachable_bands: int
    colliding_bands: int
    reachable_pass2_levels: int
    stage_sha256: str
    result_sha256: str = ""


def _router_facts() -> Tuple[int, int, int]:
    L = E1_LEVELS_MICRO; n = len(L); bands = colliding = 0
    for i in range(n):
        for j in range(i + 1, n):
            lab = ["U"] * n
            for k in range(0, i + 1): lab[k] = "N"
            for k in range(j, n): lab[k] = "S"
            d = _V.route(tuple(lab), L)
            if d.row in ("P2R-5", "P2R-6"):
                bands += 1; colliding += 1 if (d.fallback_moves or d.fallback_drops) else 0
    return bands, colliding, len(_reachable_surface())


def router_collision_record(stage: StageIdentity) -> RouterCollisionRecord:
    f = _router_facts(); return RouterCollisionRecord(*f, stage.result_sha256, _digest((f, stage.result_sha256)))


def validate_router_collision(r, stage=None, **ctx) -> None:
    if type(r) is not RouterCollisionRecord or (r.reachable_bands, r.colliding_bands, r.reachable_pass2_levels) != _router_facts(): raise RunnerDomainError("router collision facts do not re-derive from M4")
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("router record belongs to a different stage")
    if r.result_sha256 != _digest(((r.reachable_bands, r.colliding_bands, r.reachable_pass2_levels), r.stage_sha256)): raise RunnerDomainError("router record identity does not recompute")


@dataclass(frozen=True)
class ConformanceRecord:
    """The total-Q-disable conformance preflight on one executed run at the declared shape (production shape when canonical)."""
    level_micro: int
    seed: int
    grid: int
    ticks: int
    config_hash: str
    checks: Tuple[Tuple[str, bool], ...]
    passed: bool
    stage_sha256: str
    result_sha256: str = ""


def conformance_record(out_dir: str, stage: StageIdentity, *, level_micro: int = E1_LEVELS_MICRO[12], seed: int = E1_SEED_PANEL[0], grid: int = E1_GRID, ticks: int = E1_TICKS) -> ConformanceRecord:
    d = os.path.join(out_dir, ".conformance"); os.makedirs(d, exist_ok=True)
    try:
        cfg = _C.e1_run_config(level_micro, seed, grid=grid, ticks=ticks); run = _C.run_level_run(cfg, d, "c"); cp = _C.conformance_preflight(run, cfg)
        body = (int(level_micro), int(seed), grid, ticks, run.config_hash, tuple(sorted(cp.checks.items())), bool(cp.passed), stage.result_sha256)
    finally: shutil.rmtree(d, ignore_errors=True)
    return ConformanceRecord(*body, _digest(body))


def validate_conformance_record(r, stage=None, work_dir: Optional[str] = None, **ctx) -> None:
    """Derived from the EXACT M1 report: the validator re-executes the run at the recorded shape/seed and re-runs the conformance preflight;
    the check set must reproduce exactly (an invented all-true check set is refused)."""
    if type(r) is not ConformanceRecord or not _is_hex(r.config_hash, 64) or r.passed is not all(ok for _, ok in r.checks) or r.seed not in E1_SEED_PANEL: raise RunnerDomainError("conformance record malformed or passed flag does not derive")
    if r.config_hash != _C.e1_run_config(r.level_micro, r.seed, grid=r.grid, ticks=r.ticks).config_hash(): raise RunnerDomainError("conformance config hash does not re-derive from the contracted configuration")
    import tempfile
    d = tempfile.mkdtemp(dir=work_dir) if work_dir else tempfile.mkdtemp()
    try:
        cfg = _C.e1_run_config(r.level_micro, r.seed, grid=r.grid, ticks=r.ticks); run = _C.run_level_run(cfg, d, "c"); cp = _C.conformance_preflight(run, cfg)
        if tuple(sorted(cp.checks.items())) != r.checks or bool(cp.passed) is not r.passed: raise RunnerDomainError("conformance checks do not reproduce M1's report")
    finally: shutil.rmtree(d, ignore_errors=True)
    if stage is not None and r.stage_sha256 != stage.result_sha256: raise RunnerDomainError("conformance record belongs to a different stage")
    if r.result_sha256 != _digest((r.level_micro, r.seed, r.grid, r.ticks, r.config_hash, r.checks, r.passed, r.stage_sha256)): raise RunnerDomainError("conformance record identity does not recompute")


# ----------------------------------------------------------------------------- 6. job graph, specification (linked to governance), package (single authorized producer; package record written last; replayed)
JOB_GRAPH: Tuple[Tuple[str, Tuple[Tuple[str, str], ...], Tuple[str, ...]], ...] = (     # (job, ((output type, file name), ...), input jobs)
    ("dense_reference", (("ReferenceStructure", "dense_reference.json"),), ()),
    ("reference_stability", (("StabilityAudit", "reference_stability.json"),), ("dense_reference",)),
    ("projection_sweeps", (("DesignStability", "projection_sweeps.json"), ("SweepEnsemble", "projection_sweeps.ensemble.json")), ("dense_reference",)),
    ("tolerance_ensembles", (("Tolerances", "tolerance_ensembles.{level}.json"),), ()),
    ("tolerance_program", (("ToleranceProgram", "tolerance_program.json"),), ("tolerance_ensembles",)),
    ("m6_design_audit", (("AuditRecord", "m6_design_audit.json"),), ()),
    ("m6_held_out_audit", (("AuditRecord", "m6_held_out_audit.json"),), ()),
    ("m6_audit_qualification", (("AuditQualification", "m6_audit_qualification.json"),), ("m6_design_audit", "m6_held_out_audit")),
    ("resource_benchmark", (("ResourceBenchmark", "resource_benchmark.json"),), ()),
    ("stage1_package", (("StagePackage", "stage1_package.json"),), ()),
)
DERIVED_TYPES = ("LevelListRecord", "EnsembleSizesRecord", "RouterCollisionRecord", "NullPrecisionRecord", "ClosurePublication", "ConformanceRecord")
DEPENDENCY_SCHEMA = {   # per record type: (validator role, dependency record type) — exactly these, in this order
    "StabilityAudit": (("primary", "ReferenceStructure"),),
    "DesignStability": (("ref", "ReferenceStructure"), ("sweeps", "SweepEnsemble")),
    "AuditQualification": (("design", "AuditRecord"), ("held_out", "AuditRecord")),
}


def _job_outputs(job: str) -> Tuple[Tuple[str, str], ...]:
    for j, outs, _ in JOB_GRAPH:
        if j == job: return outs
    raise RunnerDomainError(f"{job!r} is not in the job graph")


def _item_file(item) -> str:
    """The deterministic file an item occupies in the package directory (never chosen by a caller)."""
    if item.producer_job == "derived": return f"derived.{item.name}.json"
    for typ, fname in _job_outputs(item.producer_job):
        if typ == item.record_type and "{" not in fname: return fname
    raise RunnerDomainError(f"item {item.name}: producer {item.producer_job} has no single output of type {item.record_type}")


@dataclass(frozen=True)
class PackageItem:
    name: str                                    # in the governance record's vocabulary
    record_type: str
    producer_job: str                            # a job-graph job whose output type matches, or "derived"
    complete_predicate: str                      # VALID AND COMPLETE (adverse-but-valid results count as complete when this predicate says so)
    pass_predicate: str                          # PASSES (used by production readiness when the governance record requires passage)
    dependencies: Tuple[Tuple[str, str], ...]    # (role, item name): exactly DEPENDENCY_SCHEMA[record_type]


@dataclass(frozen=True)
class PackageSpecification:
    """Package mechanics, linked to (and checked against) Mike's governance record."""
    version: int
    governance_sha256: str
    items: Tuple[PackageItem, ...]
    result_sha256: str = ""


def _spec_body(s) -> Tuple: return (s.version, s.governance_sha256, tuple(tuple(dataclasses.astuple(i)) for i in s.items))


def validate_package_spec(s, stage=None, governance=None, governance_sha256: Optional[str] = None, **ctx) -> None:
    """Item names in the governance vocabulary and every governance-required item present; producer/output-type compatibility with the frozen
    job graph; predicates in the closed alphabet AND applicable to the item's type; exact dependency schema with type-matched, unique targets."""
    if type(s) is not PackageSpecification or type(s.version) is not int or s.version < 1 or not _is_hex(s.governance_sha256, 64): raise RunnerDomainError("package specification malformed")
    if type(s.items) is not tuple or not s.items: raise RunnerDomainError("package specification has no items")
    by = {}
    for i in s.items:
        if type(i) is not PackageItem: raise RunnerDomainError("package items must be PackageItem records")
        if i.name in by: raise RunnerDomainError("package item names must be unique")
        by[i.name] = i
    if governance is not None:
        if type(governance) is not E1RGovernance or (governance_sha256 is not None and s.governance_sha256 != governance_sha256): raise RunnerDomainError("specification names a different governance record")
        unknown = set(by) - set(governance.package_item_vocabulary)
        if unknown: raise RunnerDomainError(f"item names outside the governance vocabulary: {sorted(unknown)}")
        missing = set(governance.required_package_items) - set(by)
        if missing: raise RunnerDomainError(f"governance-required items missing from the specification: {sorted(missing)}")
        for item, pid in governance.branch_stopping:                  # the join (L2 r4 R4-G1): every branch stop must be evaluable on the canonical package
            if item not in by: raise RunnerDomainError(f"branch-stop item {item} is absent from the Package Specification")
            if item not in governance.required_package_items: raise RunnerDomainError(f"branch-stop item {item} is not a required package item (it may be absent from a complete package)")
            if pid not in PREDICATES or PREDICATES[pid][0] not in ("*", by[item].record_type): raise RunnerDomainError(f"branch-stop predicate {pid} does not apply to {item} ({by[item].record_type})")
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


PREDICATES = {   # id -> (applicable record type or "*", function). Closed alphabet; NO default.
    "exists": ("*", lambda r: True),
    "reference_of_record_dense": ("ReferenceStructure", lambda r: r.role == "reference_of_record" and r.levels_micro == _P.dense_grid_micro()),
    "reference_resolved": ("ReferenceStructure", lambda r: r.role == "reference_of_record" and r.structure_class != "REFERENCE-UNRESOLVED"),
    "stability_canonical_complete": ("StabilityAudit", lambda r: r.role == "canonical" and r.complete),
    "stability_within": ("StabilityAudit", lambda r: r.role == "canonical" and r.complete and r.within_delta_m_stab),
    "design_complete": ("DesignStability", lambda r: r.complete),
    "design_stable": ("DesignStability", lambda r: r.complete and r.design_stable),
    "sweep_ensemble_canonical": ("SweepEnsemble", lambda r: len(r.sweeps) == _P.DESIGN_STABILITY_SWEEPS),
    "audit_record_complete": ("AuditRecord", lambda r: r.requested_sweeps_per_class == _A.SWEEPS_PER_CLASS and len(r.scores) == len(_A.CLASSES)
                              and all(s.attempted == s.scored == _A.SWEEPS_PER_CLASS and s.halted == 0 and s.generator_halted == 0 for s in r.scores)),
    "audit_record_pass": ("AuditRecord", lambda r: r.ensemble_pass),
    "qualification_recorded": ("AuditQualification", lambda r: True),
    "qualification_qualified": ("AuditQualification", lambda r: r.qualified),
    "benchmark_canonical": ("ResourceBenchmark", lambda r: r.role == "canonical"),
    "benchmark_fits": ("ResourceBenchmark", lambda r: r.role == "canonical" and r.fits_with_margin),
    "conformance_production": ("ConformanceRecord", lambda r: (r.grid, r.ticks) == (E1_GRID, E1_TICKS)),
    "conformance_production_passed": ("ConformanceRecord", lambda r: r.passed and (r.grid, r.ticks) == (E1_GRID, E1_TICKS)),
    "null_precision_dense": ("NullPrecisionRecord", lambda r: r.levels_micro == _P.dense_grid_micro()),
    "null_precision_dense_no_halts": ("NullPrecisionRecord", lambda r: r.levels_micro == _P.dense_grid_micro() and r.halts == ()),
    "closure_covers_levels": ("ClosurePublication", lambda r: set(r.levels_micro) >= set(E1_LEVELS_MICRO)),
    "quarantine_recorded": ("TrancheQuarantine", lambda r: r.status in ("passed", "failed")),
    "quarantine_passed": ("TrancheQuarantine", lambda r: r.status == "passed"),
    "tolerance_program_recorded": ("ToleranceProgram", lambda r: True),
    "tolerance_program_complete": ("ToleranceProgram", lambda r: r.complete),
}


@dataclass(frozen=True)
class StagePackage:
    role: str                                    # canonical | provisional
    stage_sha256: str
    governance_sha256: str
    package_spec_sha256: str
    authorization_version: int
    authorization_sha256: str
    authorization_file_sha256: str
    items: Tuple[Tuple[str, str, str, str, str, bool, bool], ...]   # (name, type, file, file sha256, record identity, valid_complete, passes)
    complete: bool                               # DERIVED STATE 1: every item loaded, validated and valid-complete (adverse-but-valid results included)
    all_items_pass: bool                         # every item's pass predicate holds (an input to readiness; never itself readiness)
    result_sha256: str = ""


def _pkg_body(p) -> Tuple: return (p.role, p.stage_sha256, p.governance_sha256, p.package_spec_sha256, p.authorization_version, p.authorization_sha256, p.authorization_file_sha256, p.items, p.complete, p.all_items_pass)


def _item_identity(rec) -> str:
    return getattr(rec, "result_sha256", None) or getattr(rec, "qualification_sha256", None) or getattr(rec, "record_sha256", None) or _digest(rec)


def _eval_predicate(pid: str, rec) -> bool:
    """Fail-closed predicate invocation: an inapplicable type or an internal failure is a RunnerDomainError, never an uncontrolled exception."""
    if pid not in PREDICATES: raise RunnerDomainError(f"unknown predicate {pid}")
    applies, fn = PREDICATES[pid]
    if applies not in ("*", type(rec).__name__): raise RunnerDomainError(f"predicate {pid} does not apply to {type(rec).__name__}")
    try: return bool(fn(rec))
    except Exception as e: raise RunnerDomainError(f"predicate {pid} failed on {type(rec).__name__}: {type(e).__name__}")


def _dependency_kwargs(item, loaded: Dict[str, Any]) -> Dict[str, Any]:
    """Validator context built ONLY from loaded package items (the self-contained dependency graph)."""
    kw: Dict[str, Any] = {}
    for role, target in item.dependencies:
        rec = loaded[target]
        kw[role] = rec.sweeps if type(rec).__name__ == "SweepEnsemble" else rec
    return kw


def _assemble(spec_items, package_dir: str, stage, repo_root, pinned_root, canonical: bool, provisional_ctx: Optional[Dict[str, Dict[str, Any]]] = None):
    """Load each item ONCE from its deterministic file, in dependency order; resolve dependencies from LOADED items only; require each
    job-produced canonical item to carry its producer's authorization; evaluate both predicates; derive the two package states."""
    loaded: Dict[str, Any] = {}; rows = []; pending = list(spec_items)
    while pending:
        progress = False
        for i in list(pending):
            if all(t in loaded for _, t in i.dependencies):
                pending.remove(i); progress = True
                fname = _item_file(i); fp = os.path.join(package_dir, fname)
                if not os.path.isfile(fp): raise RunnerDomainError(f"package item {i.name} file {fname} is absent")
                kw = _dependency_kwargs(i, loaded)
                if not canonical and provisional_ctx: kw.update(provisional_ctx.get(i.name, {}))
                if i.record_type == "ResourceBenchmark": kw["artifact_dir"] = os.path.join(package_dir, "benchmark_artifacts")
                if i.record_type == "ToleranceProgram": kw["program_dir"] = package_dir
                if i.record_type == "AuditRecord": kw["expect_production"] = True
                if canonical: kw["require_job"] = "stage1_package" if i.producer_job == "derived" else i.producer_job
                rec, fsha = load_record(fp, i.record_type, stage, repo_root, pinned_root, **kw)
                loaded[i.name] = rec
                rows.append((i.name, i.record_type, fname, fsha, _item_identity(rec), _eval_predicate(i.complete_predicate, rec), _eval_predicate(i.pass_predicate, rec)))
        if not progress: raise RunnerDomainError("package dependencies are cyclic or unresolved")
    rows = tuple(rows)
    return rows, all(r[5] for r in rows), all(r[6] for r in rows)


def validate_stage_package(p, stage=None, repo_root=None, pinned_root=None, package_dir: Optional[str] = None, **ctx) -> None:
    """REPLAY. A canonical package re-loads the committed specification and authorization and every item from the package directory at the carried
    file identities, resolves every dependency from those files, and must reproduce every row and both derived states. A self-hash is never enough."""
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
        rows, complete, allpass = _assemble(spec.items, package_dir, stage, repo_root, pinned_root, True)
        if (rows, complete, allpass) != (p.items, p.complete, p.all_items_pass): raise RunnerDomainError("package does not reproduce by replay")


def assemble_package_provisional(package_dir: str, stage: StageIdentity, repo_root: str, pinned_root: Optional[str] = None, contexts: Optional[Dict[str, Dict[str, Any]]] = None) -> StagePackage:
    """DEVELOPMENT ONLY: the [PROPOSED] list with 'exists' predicates; external contexts allowed here and nowhere canonical; NEVER complete."""
    verify_frozen_identity()
    items = tuple(PackageItem(n, ty, "derived" if ty in DERIVED_TYPES else next(j for j, outs, _ in JOB_GRAPH if any(o == ty for o, _ in outs)), "exists", "exists", ()) for n, ty in PACKAGE_ITEMS)
    rows, _, allpass = _assemble(items, package_dir, stage, repo_root, pinned_root, False, contexts)
    body = ("provisional", stage.result_sha256, "", "", 0, "", "", rows, False, allpass)
    return StagePackage(*body, _digest(body))


def _produce_derived(item, stage) -> Any:
    t = item.record_type
    if t == "LevelListRecord": return level_list_record(stage)
    if t == "EnsembleSizesRecord": return ensemble_sizes_record(stage)
    if t == "RouterCollisionRecord": return router_collision_record(stage)
    if t == "NullPrecisionRecord": return null_precision_record(_P.dense_grid_micro(), stage)
    if t == "ClosurePublication": return closure_publication(E1_LEVELS_MICRO, 200_000, stage)
    if t == "ConformanceRecord": return conformance_record(os.path.join(os.getcwd(), ".m7_conformance"), stage)
    raise RunnerDomainError(f"type {t} is not derivable")


@dataclass(frozen=True)
class SweepEnsemble:
    sweeps: Tuple[_P.ProjectionSweep, ...]
    result_sha256: str = ""


def validate_sweep_ensemble(e, **ctx) -> None:
    """The canonical 200-sweep evidence: exactly DESIGN_STABILITY_SWEEPS sweeps, indices 0..199 once in order, one source-literal cache bundle, the projection master."""
    if type(e) is not SweepEnsemble or type(e.sweeps) is not tuple: raise RunnerDomainError("exact SweepEnsemble required")
    for s in e.sweeps: _P.validate_projection_sweep(s)
    if tuple(s.sweep_index for s in e.sweeps) != tuple(range(_P.DESIGN_STABILITY_SWEEPS)): raise RunnerDomainError("a sweep ensemble carries exactly sweeps 0..199 once, in order")
    if {(s.cache_body_sha256, s.cache_file_sha256, s.cache_qualification_sha256, s.master) for s in e.sweeps} != {(_A.PRODUCTION_CACHE_BODY_SHA256_LITERAL, _A.PRODUCTION_CACHE_FILE_SHA256_LITERAL, _A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL, _P.PROJECTION_MASTER)}:
        raise RunnerDomainError("a sweep ensemble carries one source-literal cache bundle and the projection master")
    if e.result_sha256 != _digest(tuple(s.sweep_sha256 for s in e.sweeps)): raise RunnerDomainError("sweep ensemble identity does not recompute")


@dataclass(frozen=True)
class ToleranceProgram:
    """The canonical tolerance PROGRAM: the exact required level set, one authorized canonical tolerance per level, and a derived completion state."""
    levels_micro: Tuple[int, ...]                        # exactly TOLERANCE_PROGRAM_LEVELS
    entries: Tuple[Tuple[int, str, str, str], ...]        # (level, file, file sha256, record identity) — present levels, canonical order
    complete: bool                                        # DERIVED: every required level present
    stage_sha256: str
    authorization_version: int
    result_sha256: str = ""


def _tp_body(t_) -> Tuple: return (t_.levels_micro, t_.entries, t_.complete, t_.stage_sha256, t_.authorization_version)


def validate_tolerance_program(tp, stage=None, repo_root=None, pinned_root=None, program_dir: Optional[str] = None, **ctx) -> None:
    """Structure, exact level set, canonical order, derived completion; REPLAY (mandatory): every entry's file re-hashed and loaded under its
    tolerance_ensembles authorization through M5's replaying validator, canonical role required, record identity reproduced; and no
    required-level file present on disk may be omitted from the entries (a subset can never pass as the program)."""
    if type(tp) is not ToleranceProgram or tp.levels_micro != TOLERANCE_PROGRAM_LEVELS: raise RunnerDomainError("a ToleranceProgram carries exactly the declared program levels")
    lv = [e[0] for e in tp.entries]
    if lv != [m for m in TOLERANCE_PROGRAM_LEVELS if m in set(lv)] or len(set(lv)) != len(lv): raise RunnerDomainError("tolerance entries must be unique program levels in canonical order")
    fmt = dict(_job_outputs("tolerance_ensembles"))["Tolerances"]
    if any(e[1] != fmt.format(level=level_id(e[0])) or not _is_hex(e[2], 64) or not _is_hex(e[3], 64) for e in tp.entries): raise RunnerDomainError("tolerance entries must name the level-addressed file with sha256 identities")
    if tp.complete != (tuple(lv) == TOLERANCE_PROGRAM_LEVELS): raise RunnerDomainError("tolerance-program completion does not derive from the entries")
    if stage is not None and tp.stage_sha256 != stage.result_sha256: raise RunnerDomainError("tolerance program belongs to a different stage")
    if program_dir is None or stage is None or repo_root is None: raise RunnerDomainError("a ToleranceProgram validates only by replay: stage, repository and program directory required")
    for m in TOLERANCE_PROGRAM_LEVELS:
        fp = os.path.join(program_dir, fmt.format(level=level_id(m)))
        if os.path.isfile(fp) and m not in lv: raise RunnerDomainError(f"tolerance file for {level_id(m)} exists but is omitted from the program")
    for m, fname, fsha, rid in tp.entries:
        fp = os.path.join(program_dir, fname)
        if not os.path.isfile(fp) or _sha_file(fp) != fsha: raise RunnerDomainError(f"tolerance file for {level_id(m)} absent or differs")
        rec, _ = load_record(fp, "Tolerances", stage, repo_root, pinned_root, require_job="tolerance_ensembles")
        if rec.role != "canonical" or rec.level_micro != m or _item_identity(rec) != rid: raise RunnerDomainError(f"tolerance for {level_id(m)} is not the canonical record named by the program")
    if tp.result_sha256 != _digest(_tp_body(tp)): raise RunnerDomainError("tolerance program identity does not recompute")


def build_tolerance_program(out_dir: str, stage, repo_root, pinned_root, authorization_version: int) -> ToleranceProgram:
    """Finalizer: enumerate the authorized level files present for the declared program levels; completion is derived, never asserted."""
    fmt = dict(_job_outputs("tolerance_ensembles"))["Tolerances"]; entries = []
    for m in TOLERANCE_PROGRAM_LEVELS:
        fp = os.path.join(out_dir, fmt.format(level=level_id(m)))
        if os.path.isfile(fp):
            rec, fsha = load_record(fp, "Tolerances", stage, repo_root, pinned_root, require_job="tolerance_ensembles")
            entries.append((m, os.path.basename(fp), fsha, _item_identity(rec)))
    body = (TOLERANCE_PROGRAM_LEVELS, tuple(entries), tuple(e[0] for e in entries) == TOLERANCE_PROGRAM_LEVELS, stage.result_sha256, authorization_version)
    return ToleranceProgram(*body, _digest(body))


def _load_input(job: str, out_dir: str, stage, repo_root, pinned_root, record_type: Optional[str] = None, **ctx):
    outs = _job_outputs(job); typ = record_type or outs[0][0]; fname = dict(outs)[typ]; p = os.path.join(out_dir, fname)
    if not os.path.isfile(p): raise RunnerDomainError(f"input {job} has not been produced under authorization in {out_dir}")
    return load_record(p, typ, stage, repo_root, pinned_root, require_job=job, **ctx)[0]


def run_canonical_job(job: str, stage: StageIdentity, repo_root: str, out_dir: str, pinned_root: Optional[str], authorization_version: int, **params) -> Tuple[Any, str]:
    """THE ONLY producer of canonical outputs: the gate loads the COMMITTED authorization; dependent jobs load their inputs from THEIR authorized
    persisted outputs; outputs persist by the private canonical writer at the job graph's deterministic file names. `stage1_package` is the
    SINGLE AUTHORIZED PRODUCER of the package (not a filesystem transaction): derived item files are written first; every item is then loaded
    and validated from the package directory; the StagePackage record is written LAST, so an interruption leaves item files but no package
    record — and a package record exists only if every item it names validated."""
    auth, fsha = require_authorized(stage, repo_root, pinned_root, authorization_version, job)
    os.makedirs(out_dir, exist_ok=True); outs = dict((t, f) for t, f in _job_outputs(job)); ctx: Dict[str, Any] = {}
    def put(rec, fname, **c): _persist_canonical(rec, os.path.join(out_dir, fname), stage, repo_root, pinned_root, auth, fsha, job, **c); return os.path.join(out_dir, fname)
    if job == "dense_reference": rec = _P.dense_reference()
    elif job == "reference_stability":
        primary = _load_input("dense_reference", out_dir, stage, repo_root, pinned_root)
        if primary.role != "reference_of_record": raise RunnerDomainError("stability requires the reference of record")
        rec = _P.stability_audit(primary.levels_micro, primary); ctx = {"primary": primary}
    elif job == "projection_sweeps":
        ref = _load_input("dense_reference", out_dir, stage, repo_root, pinned_root); cache = params["cache"]
        sweeps = tuple(_P.projection_sweep(i, cache) for i in range(_P.DESIGN_STABILITY_SWEEPS)); ens = SweepEnsemble(sweeps, _digest(tuple(s.sweep_sha256 for s in sweeps)))
        put(ens, outs["SweepEnsemble"]); rec = _P.design_stability(ref, sweeps); ctx = {"ref": ref, "sweeps": sweeps}
        return rec, put(rec, outs["DesignStability"], **ctx)
    elif job == "tolerance_ensembles":
        lv = params["level_micro"]
        if lv not in TOLERANCE_PROGRAM_LEVELS: raise RunnerDomainError("tolerance ensembles are computed only for the declared program levels")
        rec = _P.tolerances(lv, n_replicates=_P.TOLERANCE_REPLICATES)
        if rec.role != "canonical": raise RunnerDomainError("a canonical tolerance job must produce a canonical-role record")
        return rec, put(rec, outs["Tolerances"].format(level=level_id(lv)))
    elif job == "tolerance_program":
        rec = build_tolerance_program(out_dir, stage, repo_root, pinned_root, auth.version); ctx = {"program_dir": out_dir}
    elif job in ("m6_design_audit", "m6_held_out_audit"): rec = _A.run_audit("design" if job == "m6_design_audit" else "held_out", params["cache"]); ctx = {"expect_production": True}
    elif job == "m6_audit_qualification":
        d = _load_input("m6_design_audit", out_dir, stage, repo_root, pinned_root, expect_production=True); h = _load_input("m6_held_out_audit", out_dir, stage, repo_root, pinned_root, expect_production=True)
        rec = _A.qualify_audit(d, h); ctx = {"design": d, "held_out": h}
    elif job == "resource_benchmark":
        rec = _benchmark_execute(BENCHMARK_SEEDS, out_dir, stage, E1_GRID, E1_TICKS, BENCHMARK_LEVEL_MICRO, "canonical", auth.version, auth.result_sha256, fsha); ctx = {"artifact_dir": os.path.join(out_dir, "benchmark_artifacts")}
    elif job == "stage1_package":
        spec, ssha = load_package_spec(repo_root, stage)
        for i in spec.items:
            if i.producer_job == "derived": put(_produce_derived(i, stage), _item_file(i))
        rows, complete, allpass = _assemble(spec.items, out_dir, stage, repo_root, pinned_root, True)
        body = ("canonical", stage.result_sha256, spec.governance_sha256, ssha, auth.version, auth.result_sha256, fsha, rows, complete, allpass)
        rec = StagePackage(*body, _digest(body)); ctx = {"package_dir": out_dir}
    else: raise RunnerDomainError(f"job {job} has no executable")
    return rec, put(rec, list(outs.values())[0], **ctx)


def _package_item_context(item_name: str, record_type: str, pkg, pkg_dir: str, stage, repo_root, pinned_root) -> Dict[str, Any]:
    """Validator context for one package item, resolved from the package's committed spec and item files (used by branch-stopping evaluation)."""
    spec, _ = load_package_spec(repo_root, stage); by = {i.name: i for i in spec.items}; rows = {r[0]: r for r in pkg.items}; loaded: Dict[str, Any] = {}
    def get(n):
        if n not in loaded:
            i = by[n]; kw = {k: v for k, v in ((role, get(t)) for role, t in i.dependencies)}
            kw = {k: (v.sweeps if type(v).__name__ == "SweepEnsemble" else v) for k, v in kw.items()}
            if i.record_type == "ResourceBenchmark": kw["artifact_dir"] = os.path.join(pkg_dir, "benchmark_artifacts")
            if i.record_type == "ToleranceProgram": kw["program_dir"] = pkg_dir
            if i.record_type == "AuditRecord": kw["expect_production"] = True
            loaded[n] = load_record(os.path.join(pkg_dir, rows[n][2]), i.record_type, stage, repo_root, pinned_root, **kw)[0]
        return loaded[n]
    i = by[item_name]; kw = {role: get(t) for role, t in i.dependencies}
    kw = {k: (v.sweeps if type(v).__name__ == "SweepEnsemble" else v) for k, v in kw.items()}
    if record_type == "ResourceBenchmark": kw["artifact_dir"] = os.path.join(pkg_dir, "benchmark_artifacts")
    if record_type == "ToleranceProgram": kw["program_dir"] = pkg_dir
    if record_type == "AuditRecord": kw["expect_production"] = True
    return kw


# ----------------------------------------------------------------------------- validators and registry
def _v_reference(r, **c): _P.validate_reference_structure(r)
def _v_stability(r, primary=None, **c):
    if primary is None: raise RunnerDomainError("a persisted StabilityAudit requires its primary reference")
    _P.validate_stability_audit(r, primary, replay=True)
def _v_design(r, ref=None, sweeps=None, **c):
    if ref is None or sweeps is None: raise RunnerDomainError("a persisted DesignStability requires its reference and sweeps")
    _P.validate_design_stability(r, ref, sweeps)
def _v_t2l(r, ref=None, ds=None, sweeps=None, production_bracket=None, **c): _P.validate_t2l(r, ref, ds, sweeps, production_bracket)
def _v_sweep(r, **c): _P.validate_projection_sweep(r)
def _v_tol(r, **c): _P.validate_tolerances(r, replay=True)
def _v_audit_record(r, **c): _A.validate_audit_record(r, expect_production=c.get("expect_production", True))
def _v_audit_qual(r, design=None, held_out=None, **c):
    if design is None or held_out is None: raise RunnerDomainError("a persisted AuditQualification requires both records")
    _A.validate_audit_qualification(r, design, held_out)
def _v_stage(r, repo_root=None, pinned_root=None, **c): validate_stage_identity(r, repo_root, pinned_root)
def _v_auth(r, stage=None, **c): validate_authorization(r, stage)

VALIDATORS = {"ReferenceStructure": _v_reference, "StabilityAudit": _v_stability, "DesignStability": _v_design, "T2L": _v_t2l, "ProjectionSweep": _v_sweep, "Tolerances": _v_tol,
              "AuditRecord": _v_audit_record, "AuditQualification": _v_audit_qual, "StageIdentity": _v_stage, "AuthorizationRecord": _v_auth,
              "LevelRecord": validate_level_record, "TrancheQuarantine": validate_quarantine, "ResourceBenchmark": validate_benchmark, "StagePackage": validate_stage_package,
              "PackageSpecification": validate_package_spec, "LevelListRecord": validate_level_list, "EnsembleSizesRecord": validate_ensemble_sizes,
              "ClosurePublication": validate_closure_publication, "NullPrecisionRecord": validate_null_precision, "RouterCollisionRecord": validate_router_collision,
              "ConformanceRecord": validate_conformance_record, "M7PlacementRecord": validate_placement_record, "AuthorizationRegistry": validate_registry,
              "SweepEnsemble": validate_sweep_ensemble, "RouterManifest": validate_router_manifest, "ProductionPrerequisiteManifest": validate_prerequisite_manifest,
              "E1RGovernance": validate_governance, "M7SuiteRecord": validate_suite_record, "ToleranceProgram": validate_tolerance_program}

_register(StageIdentity, AuthorizationRecord, AuthorizationRegistry, M7PlacementRecord, M7SuiteRecord, E1RGovernance, RunProvenance, LevelRecord, RouterManifest, PrerequisiteEntry,
          ProductionPrerequisiteManifest, TrancheQuarantine, ResourceBenchmark, PackageItem, PackageSpecification, StagePackage, SweepEnsemble, ToleranceProgram, LevelListRecord,
          EnsembleSizesRecord, ClosurePublication, NullPrecisionRecord, RouterCollisionRecord, ConformanceRecord,
          _P.ReferenceStructure, _P.StabilityAudit, _P.DesignStability, _P.T2L, _P.ProjectionSweep, _P.Tolerances, _A.AuditRecord, _A.ClassScore, _A.AuditQualification)
for _n in RECORD_TYPES:
    if _n not in VALIDATORS and _n not in ("RunProvenance", "ClassScore", "PackageItem", "PrerequisiteEntry"): raise RunnerDomainError(f"registered type {_n} has no validator")
