"""tests/test_e1_m6.py — E1 stage-1 module M6 rebuild, round 2. The seventeen test families of L2's §15,
runnable in-container without the full 7,580-row artifact: completion (A1), mechanical qualification (A2),
the production-cache boundary (A3), archetype preflight and redraw (A4), the frozen generator and intended map
(A5), complete sweep records (A6), fail-closed Clopper–Pearson with full-family parity against an independent
binomial-tail path, typed domains, CDF validation, per-seed pricing bounds, and the narrowed claim boundary."""
import dataclasses as dc
import hashlib
import json
import math
import numpy as np
import pytest

from mfa_instrument.e1 import audit as A, classify as K, verdict as V, null as N, config as C
from mfa_instrument.e1.config import E1_LEVELS_MICRO as L, E1_SEED_PANEL as P

IDENT = dict(cache_role="production_frozen", cache_body_sha256="x", declaration_sha256=A.AUDIT_DECLARATION_SHA256_LITERAL, generator_sha256=A.GENERATOR_DECLARATION_SHA256_LITERAL)
PRM = A.SweepParams("abrupt_onset", 500000, 0, 0.4, "constant", 0.0, 0.1, 100, 0.5, 0, 0)


def _ok(a="abrupt_onset", i=0, verdict="LOCATED", cause=None):
    return A.SweepResult(a, i, PRM, 1, ("N",) * 24, "LOCATED", None, "P2R-6", 8, 8, (), (), (), tuple(L), ("N",) * 24, verdict, cause, "4d", **IDENT)

def _halt(a="abrupt_onset", i=0):
    return A.SweepResult(a, i, PRM, 1, ("N",) * 24, "LOCATED", None, "P2R-6", 8, 8, (), (), (), (), (), "HALTED", None, "", **IDENT, evaluability_halt="uncertified_threshold@0.5#seed1")


# ---------------- identity, generator declaration, intended map (A5) ----------------
def test_frozen_identity_and_generator_declaration():
    A.verify_frozen_identity()
    assert A._digest(A.AUDIT_DECLARATION) == A.AUDIT_DECLARATION_SHA256_LITERAL and A._digest(A.GENERATOR_DECLARATION) == A.GENERATOR_DECLARATION_SHA256_LITERAL
    g = dict(A.GENERATOR_DECLARATION)
    assert g["intended_map"] == V.ARCHETYPE_TABLE and g["max_redraws"] == 64 and g["dip_window_ticks"] == K.WINDOW
    assert "regime-assignment" in dict(A.AUDIT_DECLARATION)["pairing"] and "descriptive only" in dict(A.AUDIT_DECLARATION)["claim_boundary"]

def test_generator_declaration_live_consistency_enforced(monkeypatch):
    """A declaration and its digest may be re-self-defined together. This test proves only live/declaration
    consistency and one-sided drift refusal. The audit record binds the DECLARATION identities. The exact placed M6
    source/commit/build identity is a separate M7 stage-package obligation and must be bound before either
    500-per-class ensemble executes (L2 M6 round-4 ruling §7)."""
    monkeypatch.setattr(A, "NONMONOTONE_ATTENUATION", 0.7)
    decl = tuple((k, 0.7 if k == "nonmonotone_attenuation" else v) for k, v in A.GENERATOR_DECLARATION)
    monkeypatch.setattr(A, "GENERATOR_DECLARATION", decl); monkeypatch.setattr(A, "GENERATOR_DECLARATION_SHA256_LITERAL", A._digest(decl))
    A.verify_frozen_identity()                                                                   # live and declared agree: passes
    monkeypatch.setattr(A, "NONMONOTONE_ATTENUATION", 0.5)                                       # live drifts from the (tampered) declaration
    with pytest.raises(A.AuditDomainError, match="differs from the live global"): A.verify_frozen_identity()

def test_intended_map_bound_to_m4_table(monkeypatch):
    bad = A.INTENDED_MAP[:-1] + (("unresolved_heavy_boundary", "LOCATED", None),)
    monkeypatch.setattr(A, "INTENDED_MAP", bad)
    decl = tuple((k, bad if k == "intended_map" else v) for k, v in A.GENERATOR_DECLARATION)
    monkeypatch.setattr(A, "GENERATOR_DECLARATION", decl); monkeypatch.setattr(A, "GENERATOR_DECLARATION_SHA256_LITERAL", A._digest(decl))
    with pytest.raises(A.AuditDomainError, match="M4's frozen archetype table"): A.verify_frozen_identity()


# ---------------- Clopper–Pearson: full family vs an independent binomial-tail path ----------------
def _cp_upper_by_binomial_tail(k, n, conf=0.95):
    """Independent path: the smallest p with P(X <= k | Bin(n,p)) <= 1 - conf, by bisection on an exact log-space binomial CDF."""
    def cdf(p):
        if p <= 0: return 1.0 if k >= 0 else 0.0
        if p >= 1: return 0.0 if k < n else 1.0
        s = 0.0
        for j in range(k + 1):
            s += math.exp(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * math.log(p) + (n - j) * math.log1p(-p))
        return s
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if cdf(mid) > 1 - conf: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

def test_cp_full_family_parity_and_monotonicity():
    prev = -1.0
    for k in range(0, 501, 1):
        ub = A.clopper_pearson_upper(k, 500)
        if k < 500: assert abs(ub - _cp_upper_by_binomial_tail(k, 500)) < 2e-7, k
        assert ub >= prev; prev = ub
    assert A.clopper_pearson_upper(500, 500) == 1.0
    prev = -1.0
    for k in range(0, 401):                                                                      # pricing family n=400: full parity + monotonicity
        ub = A.clopper_pearson_upper(k, 400)
        if k < 400: assert abs(ub - _cp_upper_by_binomial_tail(k, 400)) < 2e-7, k
        assert ub >= prev; prev = ub

def test_cp_domains_and_nonconvergence(monkeypatch):
    for bad in ((-1, 5), (6, 5), (True, 5), (1, 0), (1.0, 5), (1, 5.0)):
        with pytest.raises(A.AuditDomainError): A.clopper_pearson_upper(*bad)
    for conf in (0.0, 1.0, 1.5, float("nan"), True):
        with pytest.raises(A.AuditDomainError): A.clopper_pearson_upper(1, 5, conf)
    monkeypatch.setattr(A, "_betacf", lambda x, a, b: (1.0, False))
    with pytest.raises(A.AuditDomainError, match="did not converge"): A.clopper_pearson_upper(1, 5)


# ---------------- A1 completion ----------------
def test_499_clean_plus_one_halt_cannot_pass():
    s = A.score_class([_ok(i=i) for i in range(499)] + [_halt(i=499)], 500)
    assert s.attempted == 500 and s.scored == 499 and s.halted == 1 and s.statistical_cap_pass and not s.complete_pass
    assert A.score_class([_ok(i=i) for i in range(500)], 500).complete_pass
    assert not A.score_class([_ok(i=i) for i in range(500)], 499).complete_pass                   # requested != 500
    g = dc.replace(_ok(i=3), final_verdict="GENERATOR_HALT", generator_halt="exhausted")
    assert not A.score_class([_ok(i=i) for i in range(499)] + [g], 500).complete_pass
    assert A.score_class([_halt()], 500).scored == 0 and A.score_class([_halt()], 500).cp_upper_95 == 1.0


# ---------------- A2 qualification: records must VALIDATE, not merely agree ----------------
BUNDLE = ("b" * 64, "f" * 64, "e" * 64)         # a stand-in production identity bundle (all lowercase hex) installed via monkeypatch for these tests

def _genuine_score(n, complete=True):
    iv, ic = A.INTENDED[n]; kind = "false_nd" if n in A.SCIENTIFIC_CLASSES else "false_scientific"
    scored = 500 if complete else 499
    return A.ClassScore(n, iv, ic, 500, scored, 0 if complete else 1, 0, kind, 0, A.clopper_pearson_upper(0, scored), True, complete, 1.0, scored, ((iv, scored),), (),
                        () if complete else ("uncertified_threshold@0.5#seed1",))

def _genuine_record(ens, complete=True, monkeypatch=None):
    master = A.AUDIT_MASTER if ens == "design" else A.HELD_OUT_MASTER
    sc = tuple(_genuine_score(n, complete) for n in A.CLASSES)
    ens_pass = complete
    fields = (A.AUDIT_VERSION, ens, master, 500, "production_frozen", *BUNDLE, A.AUDIT_DECLARATION_SHA256_LITERAL, A.GENERATOR_DECLARATION_SHA256_LITERAL, sc, ens_pass)
    probe = A.AuditRecord(*fields, "")
    return A.AuditRecord(*fields, A._digest(probe.identity_body()))

@pytest.fixture
def prod_literals(monkeypatch):
    monkeypatch.setattr(A, "PRODUCTION_CACHE_BODY_SHA256_LITERAL", BUNDLE[0]); monkeypatch.setattr(A, "PRODUCTION_CACHE_FILE_SHA256_LITERAL", BUNDLE[1])
    monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", BUNDLE[2])

def test_genuine_records_qualify_and_identity_recomputes(prod_literals):
    d = _genuine_record("design"); h = _genuine_record("held_out")
    q = A.qualify_audit(d, h)
    assert q.qualified and q.reasons == () and q.qualification_sha256 == A._digest(q.identity_body())
    assert (q.cache_body_sha256, q.cache_file_sha256, q.cache_qualification_sha256) == BUNDLE
    A.validate_audit_qualification(q, d, h)
    assert not A.qualify_audit(d, None).qualified and not A.qualify_audit(d, _genuine_record("held_out", complete=False)).qualified

def test_fabricated_or_mutated_audit_qualification_refused(prod_literals):
    """L2 r3 §5: the freeze-qualifying object is validated against its records — every mutation refused."""
    d = _genuine_record("design"); h = _genuine_record("held_out"); q = A.qualify_audit(d, h)
    for bad in (dc.replace(q, qualified=False), dc.replace(q, reasons=("x",)), dc.replace(q, design_record_sha256="0" * 64),
                dc.replace(q, held_out_record_sha256=h.record_sha256[::-1]), dc.replace(q, cache_body_sha256="0" * 64),
                dc.replace(q, audit_declaration_sha256="0" * 64), dc.replace(q, qualification_sha256="0" * 64), dc.replace(q, qualified=True, reasons=("r",))):
        with pytest.raises(A.AuditDomainError): A.validate_audit_qualification(bad, d, h)
    fab = A.AuditQualification("1" * 64, "2" * 64, *BUNDLE, A.AUDIT_DECLARATION_SHA256_LITERAL, A.GENERATOR_DECLARATION_SHA256_LITERAL, True, (), "3" * 64)
    with pytest.raises(A.AuditDomainError): A.validate_audit_qualification(fab, d, h)
    with pytest.raises(A.AuditDomainError): A.validate_audit_qualification("not an object", d, h)
    # a refused pair yields a validated, unqualified object with its reasons recomputable
    bad_h = _genuine_record("held_out", complete=False); q2 = A.qualify_audit(d, bad_h)
    assert not q2.qualified and q2.reasons; A.validate_audit_qualification(q2, d, bad_h)

def test_arbitrary_mutually_consistent_records_refused():
    """L2's counterexample: the round-2 helper's records (r1/r2, cachex) — mutually consistent, never producible by run_audit."""
    sc = tuple(_genuine_score(n) for n in A.CLASSES)
    rec = lambda ens, m, sha: A.AuditRecord(A.AUDIT_VERSION, ens, m, 500, "production_frozen", "cachex", "filex", "qualx", A.AUDIT_DECLARATION_SHA256_LITERAL, A.GENERATOR_DECLARATION_SHA256_LITERAL, sc, True, sha)
    q = A.qualify_audit(rec("design", A.AUDIT_MASTER, "r1"), rec("held_out", A.HELD_OUT_MASTER, "r2"))
    assert not q.qualified and any("invalid record" in r for r in q.reasons)

def test_mutated_record_without_rehash_refused(prod_literals):
    d = _genuine_record("design")
    m = dc.replace(d, master=A.AUDIT_MASTER + 1)                                        # field changed, hash stale
    with pytest.raises(A.AuditDomainError): A.validate_audit_record(m)
    m2 = dc.replace(d, requested_sweeps_per_class=499)                                   # changes scores' completion consistency too
    with pytest.raises(A.AuditDomainError): A.validate_audit_record(m2)

def test_mutated_record_with_wrong_or_stale_rehash_refused(prod_literals):
    d = _genuine_record("design")
    m = dc.replace(d, ensemble_pass=False)
    m = dc.replace(m, record_sha256="0" * 64)                                           # intentionally wrong hash
    with pytest.raises(A.AuditDomainError, match="recomputed|recompute"): A.validate_audit_record(m)

@pytest.mark.parametrize("field,val", [("version", "other"), ("audit_declaration_sha256", "0" * 64), ("generator_declaration_sha256", "0" * 64),
                                       ("cache_body_sha256", "0" * 64), ("cache_file_sha256", "0" * 64), ("cache_qualification_sha256", "0" * 64)])
def test_identity_fields_refused(prod_literals, field, val):
    d = _genuine_record("design"); m = dc.replace(d, **{field: val}); m = dc.replace(m, record_sha256=A._digest(m.identity_body()))
    with pytest.raises(A.AuditDomainError): A.validate_audit_record(m)

def test_forged_class_score_refused(prod_literals):
    good = _genuine_score("abrupt_onset")
    for bad in (dc.replace(good, errors=500), dc.replace(good, cp_upper_95=1.0), dc.replace(good, statistical_cap_pass=False), dc.replace(good, complete_pass=False),
                dc.replace(good, applicable_error="false_scientific"), dc.replace(good, intended_verdict="NOT_PRODUCED"), dc.replace(good, verdict_counts=(("NOT_DISTINGUISHED", 500),)),
                dc.replace(good, scored=499), dc.replace(good, attempted=True),
                # R3-C1: unknown label; duplicate key hidden by dict(); non-canonical order; Boolean count; list not tuple; nonempty for unscored
                dc.replace(good, verdict_counts=(("UNKNOWN", 500),)), dc.replace(good, verdict_counts=(("LOCATED", 250), ("LOCATED", 250))),
                dc.replace(good, verdict_counts=(("NOT_PRODUCED", 1), ("LOCATED", 499)), errors=0), dc.replace(good, verdict_counts=(("LOCATED", True),)),
                dc.replace(good, verdict_counts=[("LOCATED", 500)]),
                # 3.3 descriptive aggregates
                dc.replace(good, exact_agreement_descriptive=0.5), dc.replace(good, exact_agreement_count=501), dc.replace(good, yield_distribution=((8, 600),)),
                dc.replace(good, yield_distribution=((8, 1), (8, 1))), dc.replace(good, halt_keys=("x",)), dc.replace(good, halt_keys=("uncertified_threshold@0.5#seed1",))):
        with pytest.raises(A.AuditDomainError): A.validate_class_score(bad, 500)
    A.validate_class_score(good, 500)
    empty = A.ClassScore("abrupt_onset", *A.INTENDED["abrupt_onset"], 3, 0, 3, 0, "false_nd", 0, 1.0, False, False, 0.0, 0, (), (), ("uncertified_threshold@0.5#seed1",))
    A.validate_class_score(empty, 3)
    with pytest.raises(A.AuditDomainError): A.validate_class_score(dc.replace(empty, verdict_counts=(("LOCATED", 0),)), 3)
    with pytest.raises(A.AuditDomainError): A.validate_class_score(_genuine_score("wide_mixed_boundary")._replace(applicable_error="false_nd") if hasattr(good, "_replace") else dc.replace(_genuine_score("wide_mixed_boundary"), applicable_error="false_nd"), 500)


# ---------------- A3 production-cache boundary ----------------
PRODUCTION_BODY_SHA256 = "4659b062414f7b77680cb9c2df3bdb967675376b9908ed10f5fefd843b8e9feb"     # canonical-machine qualification 2026-09-28
PRODUCTION_FILE_SHA256 = "608844ff7bd636d59faed391398524879806abdddd3c0bfc92b3396e7c93932e"
PRODUCTION_QUALIFICATION_SHA256 = "5c933778c0a8f1056ace4bf14fd27e496b4ce7446ddd156f7d17a485e6d153ab"     # committed record file bytes, 790f73e


def test_production_identities_established_and_slice_cannot_run_500(tmp_path, monkeypatch):
    assert A.PRODUCTION_CACHE_BODY_SHA256_LITERAL == PRODUCTION_BODY_SHA256 and A.PRODUCTION_CACHE_FILE_SHA256_LITERAL == PRODUCTION_FILE_SHA256
    assert A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL == PRODUCTION_QUALIFICATION_SHA256
    if "PENDING" in A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL:
        with pytest.raises(A.AuditDomainError, match="not yet established"): A.load_production_cache(str(tmp_path / "a.json"), str(tmp_path / "q.json"))
    monkeypatch.setattr(A, "PRODUCTION_CACHE_BODY_SHA256_LITERAL", "__PENDING_QUALIFICATION__")
    with pytest.raises(A.AuditDomainError, match="not yet established"): A.load_production_cache(str(tmp_path / "a.json"), str(tmp_path / "q.json"))
    monkeypatch.undo()
    sl = A.ThresholdCache({}, "slice", "sliceid")
    with pytest.raises(A.AuditDomainError, match="production_frozen"): A.run_audit("design", sl, sweeps_per_class=500)
    assert not A.is_production_cache(sl)
    with pytest.raises(A.AuditDomainError): A.ThresholdCache({}, "mystery", "x")

def test_role_label_alone_does_not_confer_production_status():
    fake = A.ThresholdCache({}, "production_frozen", "notthecommitted", "nofile", None)
    assert not A.is_production_cache(fake)
    with pytest.raises(A.AuditDomainError, match="production_frozen"): A.run_audit("design", fake, sweeps_per_class=500)

def _fake_mapping():
    hdr = A.artifact_header()
    return {(m, s): A.SeedThreshold(m, s, 0.03, 0.031, ("exact_certified", "exact_certified"), "a" * 64, "b" * 64, "c" * 64, "d" * 64)
            for m in tuple(L) + tuple(hdr["pass2_levels"]) for s in P}

def _qual(bd, fs):
    hdr = A.artifact_header()
    return A.CacheQualification(A.AUDIT_VERSION, bd, fs, hdr["n_rows"], hdr["n_rows"], hdr["n_levels"], hdr["n_pass2_levels"], True,
                                hdr["m3_declaration_sha256"], hdr["m3_scoring_object_version"], hdr["m4_declaration_sha256"], hdr["reachable_surface_sha256"])

def test_fabricated_cache_with_copied_literals_is_not_production(monkeypatch):
    """L2 §5.1: 7580 expected keys, arbitrary thresholds, the public literal strings copied in, a manufactured qualification → False."""
    by = _fake_mapping(); bd, fs = A.cache_semantic_identity(A.ThresholdCache(by, "slice", "s"))
    monkeypatch.setattr(A, "PRODUCTION_CACHE_BODY_SHA256_LITERAL", "1" * 64); monkeypatch.setattr(A, "PRODUCTION_CACHE_FILE_SHA256_LITERAL", "2" * 64)
    fq = _qual("1" * 64, "2" * 64); monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", fq.record_sha256())
    fake = A.ThresholdCache(by, "production_frozen", "1" * 64, "2" * 64, fq, fq.record_sha256())                 # copied literal strings
    assert not A.is_production_cache(fake)                                                                            # re-derivation disagrees
    # the genuine case: literals equal what the mapping re-derives; qualification identity derived from the object
    rq = _qual(bd, fs)
    monkeypatch.setattr(A, "PRODUCTION_CACHE_BODY_SHA256_LITERAL", bd); monkeypatch.setattr(A, "PRODUCTION_CACHE_FILE_SHA256_LITERAL", fs)
    monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", rq.record_sha256())
    real = A.ThresholdCache(by, "production_frozen", bd, fs, rq, rq.record_sha256())
    assert A.is_production_cache(real)
    # mutate one row while keeping the carried strings: re-derivation refuses
    by2 = dict(by); k0 = next(iter(by2)); by2[k0] = dc.replace(by2[k0], theta_t=by2[k0].theta_t + 1e-9)
    assert not A.is_production_cache(A.ThresholdCache(by2, "production_frozen", bd, fs, rq, rq.record_sha256()))
    assert A.cache_semantic_identity(real) == (bd, fs)

def test_carried_qualification_file_identity_must_derive_from_the_object(monkeypatch):
    """L2 R3-CQ1: a valid qualification object with a MISMATCHED carried qualification_sha256 is not production; and if
    the source literal is monkeypatched to that mismatched string, semantic derivation still refuses."""
    by = _fake_mapping(); bd, fs = A.cache_semantic_identity(A.ThresholdCache(by, "slice", "s"))
    q = _qual(bd, fs); real_qs = q.record_sha256()
    monkeypatch.setattr(A, "PRODUCTION_CACHE_BODY_SHA256_LITERAL", bd); monkeypatch.setattr(A, "PRODUCTION_CACHE_FILE_SHA256_LITERAL", fs)
    monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", real_qs)
    assert A.is_production_cache(A.ThresholdCache(by, "production_frozen", bd, fs, q, real_qs))
    assert not A.is_production_cache(A.ThresholdCache(by, "production_frozen", bd, fs, q, "9" * 64))                # carried string mismatched
    monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", "9" * 64)                              # literal moved to the bad string
    assert not A.is_production_cache(A.ThresholdCache(by, "production_frozen", bd, fs, q, "9" * 64))                # object digest still disagrees

def test_qualification_record_exact_types_and_identity(tmp_path, monkeypatch):
    by = _fake_mapping(); bd, fs = A.cache_semantic_identity(A.ThresholdCache(by, "slice", "s"))
    with pytest.raises(A.AuditDomainError, match="exactly True|type"): A.CacheQualification(**{**dc.asdict(_qual(bd, fs)), "replay_verification_complete": 1})
    with pytest.raises(A.AuditDomainError, match="type"): A.CacheQualification(**{**dc.asdict(_qual(bd, fs)), "n_rows": 7580.0})
    with pytest.raises(A.AuditDomainError, match="64-hex"): A.CacheQualification(**{**dc.asdict(_qual(bd, fs)), "body_sha256": "xyz"})
    # loader: the qualification FILE identity must equal the committed literal
    p = tmp_path / "c.json"; q = tmp_path / "q.json"
    A.write_artifact(str(p), [dc.asdict(v) | {"modes": list(v.modes)} for v in by.values()])
    bd2, fs2 = A.load_artifact_rows(str(p))[1:]
    monkeypatch.setattr(A, "PRODUCTION_CACHE_BODY_SHA256_LITERAL", bd2); monkeypatch.setattr(A, "PRODUCTION_CACHE_FILE_SHA256_LITERAL", fs2)
    q.write_text(_qual(bd2, fs2).canonical()); qs = hashlib.sha256(q.read_bytes()).hexdigest()
    monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", qs)
    c = A.load_production_cache(str(p), str(q)); assert A.is_production_cache(c) and c.qualification_sha256 == qs
    q.write_text(_qual(bd2, fs2).canonical() + " ")                                                                   # equivalent-looking, different bytes
    with pytest.raises(A.AuditDomainError, match="qualification record file identity"): A.load_production_cache(str(p), str(q))
    q.write_text(json.dumps({**dc.asdict(_qual(bd2, fs2)), "replay_verification_complete": 1}))
    monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", hashlib.sha256(q.read_bytes()).hexdigest())
    with pytest.raises(A.AuditDomainError): A.load_production_cache(str(p), str(q))

def _fake_rows(n_levels_extra=None):
    hdr = A.artifact_header(); levels = tuple(L) + tuple(hdr["pass2_levels"])
    rows = []
    for m in levels:
        for s in P:
            rows.append({"level_micro": m, "seed": s, "theta_p": 0.03, "theta_t": 0.031, "modes": ["exact_certified", "exact_certified"],
                         "bases_sha256": "a" * 64, "config_hash": "b" * 64, "scoring_identity": "c" * 64, "payload_sha256": "d" * 64})
    return rows

def test_artifact_parser_schema_refusals(tmp_path):
    p = tmp_path / "c.json"
    rows = _fake_rows()
    bd, fs = A.write_artifact(str(p), rows)
    by, bd2, fs2 = A.load_artifact_rows(str(p)); assert (bd, fs) == (bd2, fs2) and len(by) == A.artifact_header()["n_rows"]
    def write(body_mut):
        doc = json.loads(p.read_text()); body_mut(doc["body"]); doc["sha256"] = hashlib.sha256(A._canon(doc["body"]).encode()).hexdigest(); p.write_text(A._canon(doc))
    write(lambda b: b["rows"].pop());                       # wrong row count
    with pytest.raises(A.AuditDomainError, match="exactly"): A.load_artifact_rows(str(p))
    A.write_artifact(str(p), rows); write(lambda b: b["rows"].__setitem__(1, dict(b["rows"][0])))     # duplicate key
    with pytest.raises(A.AuditDomainError, match="duplicate|canonical"): A.load_artifact_rows(str(p))
    A.write_artifact(str(p), rows); write(lambda b: b["rows"][0].__setitem__("theta_p", "0.03"))        # coercible type
    with pytest.raises(A.AuditDomainError, match="type"): A.load_artifact_rows(str(p))
    A.write_artifact(str(p), rows); write(lambda b: b["rows"][0].__setitem__("seed", True))             # Boolean
    with pytest.raises(A.AuditDomainError): A.load_artifact_rows(str(p))
    A.write_artifact(str(p), rows); write(lambda b: b.__setitem__("n_seeds", 19))                       # wrong body count
    with pytest.raises(A.AuditDomainError, match="header"): A.load_artifact_rows(str(p))
    A.write_artifact(str(p), rows); write(lambda b: b["rows"].reverse())                                # order
    with pytest.raises(A.AuditDomainError, match="canonical"): A.load_artifact_rows(str(p))
    A.write_artifact(str(p), rows); doc = json.loads(p.read_text()); doc["sha256"] = "0" * 64; p.write_text(A._canon(doc))
    with pytest.raises(A.AuditDomainError, match="digest"): A.load_artifact_rows(str(p))

def test_production_load_refuses_wrong_identity_and_incomplete_replay(tmp_path, monkeypatch):
    p = tmp_path / "c.json"; q = tmp_path / "q.json"
    bd, fs = A.write_artifact(str(p), _fake_rows())
    monkeypatch.setattr(A, "PRODUCTION_CACHE_BODY_SHA256_LITERAL", bd); monkeypatch.setattr(A, "PRODUCTION_CACHE_FILE_SHA256_LITERAL", fs)
    hdr = A.artifact_header()
    rec = A.CacheQualification(A.AUDIT_VERSION, bd, fs, hdr["n_rows"], hdr["n_rows"], hdr["n_levels"], hdr["n_pass2_levels"], True,
                               hdr["m3_declaration_sha256"], hdr["m3_scoring_object_version"], hdr["m4_declaration_sha256"], hdr["reachable_surface_sha256"])
    q.write_text(rec.canonical()); monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", hashlib.sha256(q.read_bytes()).hexdigest())
    c = A.load_production_cache(str(p), str(q)); assert c.role == "production_frozen" and A.is_production_cache(c)
    with pytest.raises(A.AuditDomainError, match="exactly True"): dc.replace(rec, replay_verification_complete=False)     # cannot even construct
    q.write_text(A._canon({**dc.asdict(rec), "body_sha256": "0" * 64})); monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", hashlib.sha256(q.read_bytes()).hexdigest())
    with pytest.raises(A.AuditDomainError): A.load_production_cache(str(p), str(q))
    monkeypatch.setattr(A, "PRODUCTION_CACHE_BODY_SHA256_LITERAL", "1" * 64)
    with pytest.raises(A.AuditDomainError, match="committed production identities"): A.load_production_cache(str(p), str(q))

def test_missing_reachable_row_halts_production_but_slice_derives(monkeypatch):
    """In production a missing reachable key is an apparatus defect; only a slice cache may derive on demand."""
    hdr = A.artifact_header()
    by = {(L[0], s): A.SeedThreshold(L[0], s, 0.03, 0.031, ("exact_certified", "exact_certified"), "a", "b", "c", "d") for s in P}
    prod = A.ThresholdCache(by, "production_frozen", "x", "y", None)
    g = np.random.default_rng(1); prm = A.SweepParams("abrupt_onset", 500000, 0, 0.4, "constant", 0.0, 0.1, 100, 0.5, 0, 0)
    with pytest.raises(A.AuditDomainError, match="apparatus defect"): A._label_at("abrupt_onset", L[5], prm, g.random(20), prod, g, production=True)
    monkeypatch.setattr(A, "_slice_inserted", lambda m, s: A.SeedThreshold(m, s, 0.03, 0.031, ("exact_certified", "exact_certified"), "a", "b", "c", "d"))
    lab = A._label_at("abrupt_onset", L[5], prm, g.random(20), A.ThresholdCache(by, "slice", "s"), g, production=False)
    assert lab in K.LEVEL_LABELS

def test_cache_get_typed_and_immutable():
    by = {(L[0], P[0]): A.SeedThreshold(L[0], P[0], 0.03, 0.031, ("exact_certified", "exact_certified"), "a", "b", "c", "d")}
    c = A.ThresholdCache(by, "slice", "s")
    assert c.get(L[0], P[0]).seed == P[0]
    for bad in ((150000.0, P[0]), (L[0], float(P[0])), (True, P[0]), (L[0], 12345), (100000, P[0])):
        with pytest.raises(A.AuditDomainError): c.get(*bad)
    with pytest.raises(A.AuditDomainError): c.role = "production_frozen"
    with pytest.raises(TypeError): c._by[(1, 2)] = None


# ---------------- A4 preflight and redraw ----------------
@pytest.mark.parametrize("prm,why", [
    (A.SweepParams("reentrant", 700000, 0, 0.4, "constant", 0.0, 0.1, 100, 0.5, 899999, 0), "second onset beyond the sweep"),
    (A.SweepParams("two_resolved_crossings", 700000, 0, 0.4, "constant", 0.0, 0.1, 100, 0.5, 0, 0), "four regions"),
    (A.SweepParams("off_band_mixture", 300000, 120000, 0.4, "constant", 0.0, 0.1, 100, 0.5, 0, 3), "not below the band"),
    (A.SweepParams("off_band_unresolved", 300000, 20000, 0.4, "constant", 0.0, 0.1, 100, 0.5, 0, 3), "not all below the band"),
])
def test_l2_counterexamples_refused_by_preflight(prm, why):
    ok, reason = A.archetype_preflight(prm); assert not ok and why in reason

def test_redraw_is_deterministic_bounded_and_recorded(monkeypatch):
    for name in A.CLASSES:
        for i in range(30):
            prm, n = A.draw_params(name, A.AUDIT_MASTER, A.CLASSES.index(name), i)
            assert A.archetype_preflight(prm)[0] and 1 <= n <= A.MAX_REDRAWS and prm == A.draw_params(name, A.AUDIT_MASTER, A.CLASSES.index(name), i)[0]
    monkeypatch.setattr(A, "archetype_preflight", lambda p: (False, "forced"))
    with pytest.raises(A.GeneratorHalt): A.draw_params("reentrant", A.AUDIT_MASTER, 7, 0)
    r = A.run_sweep("reentrant", 0, A.AUDIT_MASTER, A.ThresholdCache({}, "slice", "s"))
    assert r.generator_halt and r.final_verdict == "GENERATOR_HALT" and r.preflight_attempts == A.MAX_REDRAWS
    s = A.score_class([r], 1); assert s.generator_halted == 1 and s.scored == 0 and not s.complete_pass

def test_pairing_is_common_regime_assignment():
    prm, _ = A.draw_params("gentle_onset", A.AUDIT_MASTER, 0, 3); us = np.random.default_rng(11).random(20)
    prev = set()
    for m in L:
        cur = {s for s in range(20) if A.regime_at("gentle_onset", m, prm, float(us[s]))[0] == "SUSTAINED"}
        assert prev <= cur; prev = cur


# ---------------- A6 record; regimes; CDF; typed domains ----------------
def test_sweep_record_carries_router_fallback_and_final_profile():
    sl = A.slice_cache([L[0], L[23]])
    with pytest.raises(A.AuditDomainError): A.run_sweep("abrupt_onset", 0.0, A.AUDIT_MASTER, sl)
    f = [k for k in A.SweepResult.__dataclass_fields__]
    for k in ("params", "preflight_attempts", "insertions_micro", "fallback_moves", "fallback_drops", "final_levels_micro", "final_labels", "cache_role", "cache_body_sha256", "declaration_sha256", "generator_sha256"):
        assert k in f

def test_regime_domains_and_dip_uses_window_constant():
    g = np.random.default_rng(3)
    with pytest.raises(A.AuditDomainError): A.gen_sustained_run(0.4, "sinusoid", 0.0, 0.1, 100, g)
    with pytest.raises(A.AuditDomainError): A.gen_sustained_run(0.4, "constant", 0.0, 0.1, 0, g)
    with pytest.raises(A.AuditDomainError): A.gen_sustained_run(1.4, "constant", 0.0, 0.1, 100, g)
    with pytest.raises(A.AuditDomainError): A.gen_sustained_run(0.4, "drift", float("nan"), 0.1, 100, g)
    r = A.gen_dip_run(0.4, g); k = K.recover_counts(r)[K.TAIL_START:]
    assert (k == 0).sum() == K.WINDOW and A.DIP_WINDOWS == (0, K.N_WINDOWS - 1)

def test_cdf_validation_and_series_domains():
    good = np.cumsum(np.full(A.N_CELLS + 1, 1.0 / (A.N_CELLS + 1))); v = A._validated_cdf(good); assert v[-1] == 1.0 and not v.flags.writeable
    for bad in (good[:-1], good.astype(np.float32), np.flip(good), good * 0.9, np.where(np.arange(good.size) == 3, np.nan, good)):
        with pytest.raises(A.AuditDomainError): A._validated_cdf(bad)
    with pytest.raises(A.AuditDomainError): A._series_from_counts(np.zeros(A.TAIL_LEN))
    with pytest.raises(A.AuditDomainError): A._series_from_counts(np.full(A.TAIL_LEN, A.N_CELLS + 1, dtype=np.int64))

def test_audit_and_pricing_typed_inputs():
    sl = A.ThresholdCache({}, "slice", "s")
    for bad in (1.5, "1", True, 0):
        with pytest.raises(A.AuditDomainError): A.run_audit("design", sl, sweeps_per_class=bad)
    with pytest.raises(A.AuditDomainError): A.run_audit("production", sl, sweeps_per_class=1)
    with pytest.raises(A.AuditDomainError): A.run_pricing(levels=[L[0], L[0]], replicates=1)
    with pytest.raises(A.AuditDomainError): A.run_pricing(levels=[True], replicates=1)
    with pytest.raises(A.AuditDomainError): A.run_pricing(levels=[L[0]], replicates=0)
    with pytest.raises(A.AuditDomainError, match="nonempty"): A.run_pricing(levels=[], replicates=1)


# ---------------- pricing: per-seed bounds; Finding 1 ----------------
def test_pricing_reports_per_seed_cp_and_pooled_descriptive_and_finding_1():
    pr = A.run_pricing(levels=[L[23]], replicates=3)
    assert len(pr.per_seed_exceed_reference[0][1]) == 20 and pr.replicates_per_seed == 3
    assert pr.worst_seed_cp_upper_reference > pr.worst_seed_cp_upper_conditional
    assert pr.pooled_rate_reference_descriptive > pr.pooled_rate_conditional_descriptive
    assert "descriptive" in pr.summary()


# ---------------- claim boundary (§13) ----------------
def test_claim_boundary_exact_agreement_is_descriptive_only():
    # LOCATED intended, NOT_PRODUCED observed: NOT an applicable error, but exact agreement drops
    rs = [_ok(i=i, verdict="NOT_PRODUCED", cause="order_violation") for i in range(40)]
    s = A.score_class(rs, 40); assert s.errors == 0 and s.statistical_cap_pass and s.exact_agreement_descriptive == 0.0   # CP(0,40)=0.072 < cap
    src = open(A.__file__, encoding="utf-8").read()
    assert "DESCRIPTIVE ONLY" in src and "exact_agreement_descriptive" in src and "recognize morphology classes" not in src

def test_ensemble_pass_requires_production_cache_even_when_all_classes_complete(monkeypatch):
    """A slice cache can never yield ensemble_pass, even with every class artificially complete."""
    sl = A.ThresholdCache({}, "slice", "s")
    monkeypatch.setattr(A, "run_sweep", lambda a, i, m, c: _ok(a, i, *A.INTENDED[a]))       # every sweep at its intended verdict
    rec = A.run_audit("held_out", sl, sweeps_per_class=3)
    assert all(s.errors == 0 for s in rec.scores) and rec.ensemble_pass is False and rec.cache_role == "slice" and len(rec.record_sha256) == 64
    assert not any(s.complete_pass for s in rec.scores)                                          # requested 3 != 500


# ======================= round 4 (L2 r3 §14): verdict alphabet, qualification self-validation, object/file digest =======================
def test_r4_unknown_and_duplicate_verdict_labels_refused():
    """R3-C1: a forged score with verdicts outside M4's alphabet, or duplicates hidden by dict(), cannot manufacture a pass."""
    g = _genuine_score("abrupt_onset")
    with pytest.raises(A.AuditDomainError, match="M4 verdicts|frozen verdict set"): A.validate_class_score(dc.replace(g, verdict_counts=(("UNKNOWN", 500),), exact_agreement_count=0, exact_agreement_descriptive=0.0), 500)
    with pytest.raises(A.AuditDomainError, match="unique"): A.validate_class_score(dc.replace(g, verdict_counts=(("LOCATED", 250), ("LOCATED", 250))), 500)
    with pytest.raises(A.AuditDomainError, match="canonical"): A.validate_class_score(dc.replace(g, verdict_counts=(("NOT_PRODUCED", 1), ("LOCATED", 499)), exact_agreement_count=499, exact_agreement_descriptive=499 / 500, errors=0), 500)
    with pytest.raises(A.AuditDomainError, match="positive exact"): A.validate_class_score(dc.replace(g, verdict_counts=(("LOCATED", 500), ("NOT_PRODUCED", 0))), 500)
    with pytest.raises(A.AuditDomainError, match="positive exact"): A.validate_class_score(dc.replace(g, verdict_counts=(("LOCATED", True),)), 500)
    nd = _genuine_score("wide_mixed_boundary")
    with pytest.raises(A.AuditDomainError, match="M4 verdicts|frozen verdict set"): A.validate_class_score(dc.replace(nd, verdict_counts=(("UNKNOWN", 500),), exact_agreement_count=0, exact_agreement_descriptive=0.0), 500)
    empty = _genuine_score("abrupt_onset", complete=False)
    z = dc.replace(empty, scored=0, halted=500, cp_upper_95=1.0, statistical_cap_pass=False, complete_pass=False, exact_agreement_count=0, exact_agreement_descriptive=0.0, verdict_counts=(), halt_keys=("uncertified_threshold@0.5#seed1",))
    A.validate_class_score(z, 500)
    with pytest.raises(A.AuditDomainError): A.validate_class_score(dc.replace(z, verdict_counts=(("LOCATED", 0),)), 500)     # refused (zero count) before the empty-tuple rule
    with pytest.raises(A.AuditDomainError, match="empty|sum"): A.validate_class_score(dc.replace(z, verdict_counts=(("LOCATED", 1),)), 500)

def test_r4_descriptive_aggregates_are_derived():
    g = _genuine_score("abrupt_onset")
    with pytest.raises(A.AuditDomainError, match="derive from the count|derived ratio|differs"): A.validate_class_score(dc.replace(g, exact_agreement_descriptive=0.5), 500)
    with pytest.raises(A.AuditDomainError, match="exceed"): A.validate_class_score(dc.replace(g, verdict_counts=(("LOCATED", 499), ("NOT_PRODUCED", 1)), exact_agreement_count=500), 500)
    with pytest.raises(A.AuditDomainError, match="yield"): A.validate_class_score(dc.replace(g, yield_distribution=((8, 300), (8, 300))), 500)
    with pytest.raises(A.AuditDomainError, match="halt"): A.validate_class_score(dc.replace(g, halt_keys=("uncertified_threshold@x",)), 500)          # halted == 0 but keys present

def test_r4_fabricated_and_mutated_audit_qualification_refused(prod_literals):
    d = _genuine_record("design"); h = _genuine_record("held_out")
    q = A.qualify_audit(d, h); assert q.qualified
    A.validate_audit_qualification(q, d, h)
    for mut in (dict(qualified=False), dict(reasons=("x",)), dict(design_record_sha256="0" * 64), dict(held_out_record_sha256="0" * 64),
                dict(cache_body_sha256="0" * 64), dict(audit_declaration_sha256="0" * 64), dict(qualification_sha256="0" * 64)):
        m = dc.replace(q, **mut)
        with pytest.raises(A.AuditDomainError): A.validate_audit_qualification(m, d, h)
    fab = A.AuditQualification("1" * 64, "2" * 64, *BUNDLE, A.AUDIT_DECLARATION_SHA256_LITERAL, A.GENERATOR_DECLARATION_SHA256_LITERAL, True, (), "")
    with pytest.raises(A.AuditDomainError): A.validate_audit_qualification(fab, d, h)
    fab2 = dc.replace(fab, design_record_sha256=d.record_sha256, held_out_record_sha256=h.record_sha256)
    fab2 = dc.replace(fab2, qualification_sha256=A._digest(fab2.identity_body()))                                         # consistent digest, but records unvalidated? they are genuine here:
    A.validate_audit_qualification(fab2, d, h)                                                                            # recomputes to the same object → accepted (it IS the qualification)
    with pytest.raises(A.AuditDomainError): A.validate_audit_qualification(dc.replace(fab2, qualified=False), d, h)
    with pytest.raises(A.AuditDomainError, match="exact AuditQualification"): A.validate_audit_qualification("q", d, h)

def test_r4_qualification_object_digest_must_equal_carried_and_literal(tmp_path, monkeypatch):
    by = _fake_mapping(); p = tmp_path / "c.json"; q = tmp_path / "q.json"
    A.write_artifact(str(p), [dc.asdict(v) | {"modes": list(v.modes)} for v in by.values()])
    bd, fs = A.load_artifact_rows(str(p))[1:]
    monkeypatch.setattr(A, "PRODUCTION_CACHE_BODY_SHA256_LITERAL", bd); monkeypatch.setattr(A, "PRODUCTION_CACHE_FILE_SHA256_LITERAL", fs)
    qual = _qual(bd, fs); q.write_text(qual.canonical()); qs = hashlib.sha256(q.read_bytes()).hexdigest()
    assert qual.record_sha256() == qs                                                                                     # canonical file == object digest
    monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", qs)
    c = A.load_production_cache(str(p), str(q)); assert A.is_production_cache(c)
    # valid object, mismatched carried string
    assert not A.is_production_cache(A.ThresholdCache(dict(c._by), "production_frozen", bd, fs, qual, "0" * 64))
    # literal monkeypatched to the mismatched string: semantic derivation from the object still refuses
    monkeypatch.setattr(A, "PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL", "0" * 64)
    assert not A.is_production_cache(A.ThresholdCache(dict(c._by), "production_frozen", bd, fs, qual, "0" * 64))
    with pytest.raises(A.AuditDomainError): A.load_production_cache(str(p), str(q))
