"""tests/test_e1_m5.py — E1 stage-1 module M5, round 3. Every freeze-facing record is DERIVED: contradictions with
recomputed digests refuse; canonical tolerances re-derive by replay; the design ensemble is exact (indices 0..199 once,
one master, one canonical cache bundle, one declaration, 200 validated sweeps); T2-L validates the gate and every sweep;
stability alternatives are carried as complete validated reference records (halts and modes included) with summary rows derived from them; the quadrature basis and both caches are content-bound; the actual
projection-sweep constructor is exercised through its validator and mutated on every surface. Round-2 families retained."""
import dataclasses as dc
import math
from itertools import product
import numpy as np
import pytest

from mfa_instrument.e1 import projection as P, classify as K, verdict as V, null as N, audit as A, config as C
from mfa_instrument.e1.config import E1_LEVELS_MICRO as L

LV7 = [150000, 250000, 350000, 450000, 550000, 650000, 750000]
BUNDLE = (A.PRODUCTION_CACHE_BODY_SHA256_LITERAL, A.PRODUCTION_CACHE_FILE_SHA256_LITERAL, A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL)


def _f(obj):
    """Shallow field copy (dataclasses.asdict would recurse into nested records)."""
    return {k: getattr(obj, k) for k in obj.__dataclass_fields__}

def _mk(cls, **kw):
    """Construct a frozen record with its identity computed from the given fields (the honest constructor path)."""
    probe = object.__new__(cls); idf = {"sweep_sha256", "result_sha256"}
    for name in cls.__dataclass_fields__:
        if name not in idf: object.__setattr__(probe, name, kw[name])
    ident = {P.ProjectionSweep: P._sweep_identity, P.DesignStability: P._ds_identity, P.T2L: P._t2l_identity, P.StabilityAudit: P._sa_identity, P.ReferenceStructure: P._reference_result_identity, P.Tolerances: P._tolerance_identity}[cls](probe)
    key = "sweep_sha256" if cls is P.ProjectionSweep else "result_sha256"
    return cls(**{**kw, key: ident})

def _sw(i, labels, bundle=BUNDLE, halt=None, master=None, decl=None):
    """A sweep whose M4/router fields are DERIVED from its labels (the only way a synthetic sweep validates)."""
    labels = tuple(labels); v1 = P.evaluate(labels, L); d = P.route(labels, L)
    nominal = V.P2R_SINGLE_BAND_INSERTIONS if d.row in ("P2R-5", "P2R-6") else (2 * V.P2R_PER_INTERVAL_INSERTIONS if d.row == "P2R-4" else 0)
    if halt:
        fl, fb, vd, cs, rl, br = (), (), "HALTED", None, "", None
    else:
        # inserted levels resolve: N below the pass-1 band midpoint, S above (so a located band stays located after pass 2)
        n_idx = [i for i, x in enumerate(labels) if x == "N"]; s_idx = [i for i, x in enumerate(labels) if x == "S"]
        mid = (L[max(n_idx)] + L[min(s_idx)]) // 2 if n_idx and s_idx else 0
        merged = sorted(list(zip(L, labels)) + [(m, "N" if m < mid else "S") for m in d.insertions_micro]); fl = tuple(m for m, _ in merged); fb = tuple(l for _, l in merged)
        vf = P.evaluate(fb, fl); vd, cs, rl, br = vf.verdict, vf.cause, vf.rule, vf.bracket_micro
    return _mk(P.ProjectionSweep, sweep_index=i, master=master or P.PROJECTION_MASTER, pass1_labels=labels, pass1_verdict=v1.verdict, pass1_cause=v1.cause, router_row=d.row, nominal_insertions=nominal,
               realized_insertions=len(d.insertions_micro), insertions_micro=tuple(d.insertions_micro), fallback_moves=tuple(d.fallback_moves), fallback_drops=tuple(d.fallback_drops),
               final_levels_micro=fl, final_labels=fb, verdict=vd, cause=cs, rule=rl, bracket_micro=br, cache_body_sha256=bundle[0], cache_file_sha256=bundle[1], cache_qualification_sha256=bundle[2],
               m5_declaration_sha256=decl or P.PROJECTION_DECLARATION_SHA256_LITERAL, halt_category=halt, halt_detail="x" if halt else None)

ALL_S = ("S",) * 24
BAND = ("N",) * 10 + ("U",) * 2 + ("S",) * 12

def _record_ref(labels, monkeypatch):
    lv = tuple(LV7[:len(labels)]); monkeypatch.setattr(P, "dense_grid_micro", lambda: lv); monkeypatch.setattr(P, "DENSE_POINTS", len(lv))
    return P.structure_class(labels, lv, modes=tuple(("exact_certified", "exact_certified") for _ in lv), role="reference_of_record")


# ---------------- identity / hygiene / basis ----------------
def test_frozen_declaration_no_result_and_basis_bound():
    P.verify_frozen_identity(); d = dict(P.PROJECTION_DECLARATION)
    assert "NONE IN THE INSTRUMENT" in d["reference_result"] and d["t2s_table"] == P.T2S_TABLE
    assert not P._GL_X.flags.writeable and not P._GL_W.flags.writeable
    with pytest.raises(ValueError): P._GL_W[0] = 1.0
    with pytest.raises(ValueError): P._GL_X[0] = 0.0
    src = open(P.__file__, encoding="utf-8").read(); assert "PROVISIONAL SAMPLED CLOSURE FINDING" in src

def test_embedded_result_and_basis_tamper_refuse(monkeypatch):
    decl = tuple((k, "NO-NULL-PHASE established" if k == "reference_result" else v) for k, v in P.PROJECTION_DECLARATION)
    monkeypatch.setattr(P, "PROJECTION_DECLARATION", decl); monkeypatch.setattr(P, "PROJECTION_DECLARATION_SHA256_LITERAL", P._digest(decl))
    with pytest.raises(P.ProjectionDomainError, match="must not carry a reference result"): P.verify_frozen_identity()
    monkeypatch.undo()
    gw = np.polynomial.legendre.leggauss(16)[1].copy(); gw[0] += 1e-12; gw.setflags(write=False); monkeypatch.setattr(P, "_GL_W", gw)
    with pytest.raises(P.ProjectionDomainError, match="Gauss-Legendre basis"): P.verify_frozen_identity()

def test_cache_entry_replacement_refused_not_only_assignment():
    lam, wt = P._nodes(L[12]); fake_w = np.full_like(wt, 1.0 / wt.size); fake_w.setflags(write=False); fl = lam.copy(); fl.setflags(write=False)
    P._NODE_CACHE[L[12]] = (fl, fake_w, P._content(fl, fake_w))
    with pytest.raises(P.ProjectionDomainError, match="regenerated"): P.g_map(0.5, L[12])
    del P._NODE_CACHE[L[12]]
    o = P.orbit(L[12]); fo = o.copy(); fo[5] += 1e-9; fo.setflags(write=False); P._ORBIT_CACHE[L[12]] = (fo, P._content(fo))
    with pytest.raises(P.ProjectionDomainError, match="recomputed"): P.orbit(L[12])
    del P._ORBIT_CACHE[L[12]]
    with pytest.raises(ValueError): P.orbit(L[12])[0] = 0.0


# ---------------- closure / geometry (carried) ----------------
def test_closure_validated_three_ways_and_tail_transcription():
    cv = P.closure_validation(L[12], mc_samples=300_000)
    assert cv["abs_gl16_minus_gl8_rho0.0"] < 1e-14 and cv["abs_gl16_minus_mc_rho0.0"] < 1e-4 and cv["abs_template_minus_gl16_rho0"] < 2e-3
    r = np.zeros(3000); r[2000:] = np.float64(1250) / 2500; r[2200:2300] = np.float64(1000) / 2500
    assert abs(P.projected_tail_stats(r).s_min - K.tail_stats(r).s_min) < 1e-12
    with pytest.raises(K.ClassifyDomainError): K.tail_stats(P.orbit(L[5]))


# ---------------- ReferenceStructure derived (§3) ----------------
def test_exact_grid_contradiction_with_recomputed_digest_refused():
    lv = P.dense_grid_micro(); modes = (("exact_certified", "exact_certified"),) * 701
    kw = dict(role="reference_of_record", structure_class="UNIQUE-THRESHOLD", labels=("S",) * 701, levels_micro=lv, grid_sha256=P._digest(lv), expected_points=701, realized_points=701,
              precision_halt_count=0, precision_halts=(), modes=modes, bracket_micro=(400000, 500000), midpoint_micro=450000, off_band_u_total=0, off_band_u_max_run=0,
              reason="both phases, order respected", m3_reference_sha256=P.m3_reference_identity(), m5_declaration_sha256=P.PROJECTION_DECLARATION_SHA256_LITERAL)
    with pytest.raises(P.ProjectionDomainError, match="do not re-derive"): _mk(P.ReferenceStructure, **kw)
    good = dict(kw, structure_class="NO-NULL-PHASE", bracket_micro=None, midpoint_micro=None, reason="no N; hard bottom point S")
    r = _mk(P.ReferenceStructure, **good); assert r.role == "reference_of_record"
    with pytest.raises(P.ProjectionDomainError, match="midpoint"): _mk(P.ReferenceStructure, **dict(good, structure_class="NO-NULL-PHASE", midpoint_micro=1))
    with pytest.raises(P.ProjectionDomainError, match="recorded threshold modes"): _mk(P.ReferenceStructure, **dict(good, modes=(P.UNRECORDED_MODE,) * 701))
    with pytest.raises(P.ProjectionDomainError, match="legal modes"): _mk(P.ReferenceStructure, **dict(good, modes=(("exact_certified", "mystery"),) + modes[1:]))
    hal = dict(good, role="analysis_subset", expected_points=701, precision_halt_count=1, precision_halts=(P.level_id(lv[3]),), modes=modes[:3] + (P.HALT_MODE,) + modes[4:], labels=("S",) * 3 + ("U",) + ("S",) * 697,
               structure_class="REFERENCE-UNRESOLVED", reason="reference null failed its precision requirement at grid instantiation")
    _mk(P.ReferenceStructure, **hal)                                                                                      # halt consistent: accepted as analysis
    with pytest.raises(P.ProjectionDomainError, match="zero precision halts"): _mk(P.ReferenceStructure, **dict(hal, role="reference_of_record"))
    with pytest.raises(P.ProjectionDomainError, match="halt mode must coincide"): _mk(P.ReferenceStructure, **dict(hal, labels=("S",) * 701))

def test_structure_classifier_total_and_jurisprudence():
    counts = {}
    for lab in product("SNU", repeat=7):
        r = P.structure_class(lab, LV7); counts[r.structure_class] = counts.get(r.structure_class, 0) + 1
    assert set(counts) == set(P.STRUCTURE_CLASSES) and sum(counts.values()) == 3 ** 7
    assert P.structure_class("NNUUSSS", LV7).bracket_micro == (LV7[1], LV7[4]) and P.structure_class("NNNNNUU", LV7).structure_class == "REFERENCE-UNRESOLVED"

def test_coarse_reference_role_and_record_boundary():
    ref = P.classify_grid([L[0], L[12], L[23]]); assert ref.role == "analysis_subset" and ref.structure_class == "NO-NULL-PHASE"
    with pytest.raises(P.ProjectionDomainError): dc.replace(ref, role="reference_of_record")
    with pytest.raises(P.ProjectionDomainError, match="exact dense grid"): P.classify_grid([L[0], L[12], L[23]], role="reference_of_record")


# ---------------- Tolerances derived (§4.1) ----------------
def test_fabricated_canonical_tolerance_refused_at_scientific_use(monkeypatch):
    tol = P.tolerances(L[12], n_replicates=40); assert tol.role == "smoke"
    with pytest.raises(P.ProjectionDomainError, match="finite"): dc.replace(tol, orbit_tail_mean=float("nan"))
    with pytest.raises(P.ProjectionDomainError, match="identity"): dc.replace(tol, tau_eq_ci_half_width=tol.tau_eq_ci_half_width + 1e-9)   # CI fields bound
    forged = _mk(P.Tolerances, **dict(dc.asdict(tol), tau_eq=0.1))                                                       # formatting passes
    with pytest.raises(P.ProjectionDomainError, match="re-derive by replay"): P.validate_tolerances(forged, replay=True)
    forged2 = _mk(P.Tolerances, **dict(dc.asdict(tol), tau_disp_ci_half_width=tol.tau_disp_ci_half_width + 1e-9))
    with pytest.raises(P.ProjectionDomainError, match="re-derive by replay"): P.validate_tolerances(forged2, replay=True)
    P.validate_tolerances(tol, replay=True)                                                                               # the real one re-derives
    with pytest.raises(P.ProjectionDomainError, match="canonical"): _mk(P.Tolerances, **dict(dc.asdict(tol), role="canonical"))
    with pytest.raises(P.ProjectionDomainError, match="canonical role"): _mk(P.Tolerances, **dict(dc.asdict(tol), n_replicates=1000, master=P.TOLERANCE_MASTER))   # exact program must be canonical
    ref_a = P.classify_grid([L[10], L[12], L[14]])
    assert P.t1_orbit_tail_agreement(L[12], [tol.orbit_tail_mean] * 10, tol, ref_a).status == "NOT EVALUABLE"
    with pytest.raises(P.ProjectionDomainError, match="re-derive by replay"): P.t1_orbit_tail_agreement(L[12], [0.05] * 10, forged, ref_a)

def test_dispersion_uses_exact_range_statistic():
    tol = P.tolerances(L[12], n_replicates=100)
    reps = P.finite_n_homogeneous(L[12], 100, P.TOLERANCE_MASTER, 1); tails = reps[:, P.TAIL_START:].mean(axis=1)
    rng_stat = tails.reshape(5, 20).max(axis=1) - tails.reshape(5, 20).min(axis=1)
    assert tol.tau_disp == float(np.quantile(rng_stat, 0.95, method="linear")) and tol.tau_disp != tol.tau_eq


# ---------------- ProjectionSweep derived (§11) ----------------
def test_actual_projection_sweep_validates_and_every_surface_mutation_refuses():
    a = "/home/claude/verify-m6/flights/mfa_fidelity/artifacts/e1/"
    try: c = A.load_production_cache(a + "threshold_cache_qualified.json", a + "threshold_cache_qualification.json")
    except Exception: pytest.skip("committed production cache not present in this environment")
    s = P.projection_sweep(0, c); P.validate_projection_sweep(s)
    assert (s.cache_body_sha256, s.cache_file_sha256, s.cache_qualification_sha256) == BUNDLE and s.master == P.PROJECTION_MASTER
    for mut in (dict(pass1_verdict="LOCATED"), dict(router_row="P2R-6"), dict(verdict="LOCATED", cause=None), dict(rule="4d"), dict(bracket_micro=(L[3], L[5])),
                dict(master=1), dict(m5_declaration_sha256="0" * 64), dict(cache_body_sha256="0" * 64), dict(halt_category="mystery", halt_detail="x"),
                dict(final_labels=s.final_labels[:-1] + ("U",)), dict(sweep_index=-1)):
        with pytest.raises(P.ProjectionDomainError): dc.replace(s, **mut)                                              # identity stale
        with pytest.raises(P.ProjectionDomainError): _mk(P.ProjectionSweep, **{**dc.asdict(s), **mut})                  # identity recomputed: semantics refuse

def test_synthetic_sweeps_must_derive():
    s = _sw(0, ALL_S); assert s.verdict == "NOT_PRODUCED" and s.cause == "no_null_consistent_phase"
    with pytest.raises(P.ProjectionDomainError): _mk(P.ProjectionSweep, **{**dc.asdict(s), "pass1_cause": "order_violation"})
    h = _sw(1, ALL_S, halt="evaluability:uncertified_threshold"); assert h.verdict == "HALTED"
    with pytest.raises(P.ProjectionDomainError): _mk(P.ProjectionSweep, **{**dc.asdict(h), "final_labels": ALL_S})


# ---------------- DesignStability exact ensemble (§4.2) ----------------
def test_exact_ensemble_required(monkeypatch):
    ref_r = _record_ref("SSS", monkeypatch)
    good = [_sw(i, ALL_S) for i in range(200)]
    d = P.design_stability(ref_r, good); assert d.complete and d.design_stable and d.status == "DESIGN-STABLE"; P.validate_design_stability(d, ref_r, good)
    dup = [good[0]] * 200; d2 = P.design_stability(ref_r, dup); assert not d2.complete and "incomplete" in d2.status
    wrong_master = good[:199] + [_sw(199, ALL_S, master=1)] if False else None
    with pytest.raises(P.ProjectionDomainError, match="master"): _sw(199, ALL_S, master=1)                             # cannot even construct
    with pytest.raises(P.ProjectionDomainError, match="source-literal production identities"): _sw(199, ALL_S, bundle=("a" * 64, "b" * 64, "c" * 64))   # a non-production bundle cannot even construct
    forged = dc.replace(d, design_stable=True, complete=True, n_matching=200)
    with pytest.raises(P.ProjectionDomainError): P.validate_design_stability(forged, ref_r, dup)                       # forged gate against the real (duplicate) ensemble
    halt = good[:199] + [_sw(199, ALL_S, halt="evaluability:uncertified_threshold")]
    d3 = P.design_stability(ref_r, halt); assert d3.halted == 1 and not d3.complete and abs(d3.match_rate_over_attempted - 0.995) < 1e-12

def test_analysis_reference_or_short_ensemble_never_stable():
    ref_a = P.classify_grid([L[0], L[12], L[23]])
    assert not P.design_stability(ref_a, [_sw(i, ALL_S) for i in range(50)]).complete


# ---------------- T2-L validates the gate and every sweep (§4.3) ----------------
def test_t2l_forged_gate_and_duplicate_ensemble_cannot_open(monkeypatch):
    ref_r = _record_ref("NNUSS", monkeypatch); assert ref_r.structure_class == "UNIQUE-THRESHOLD"
    full = [_sw(i, BAND) for i in range(200)]; ds = P.design_stability(ref_r, full); assert ds.design_stable
    r = P.t2l(ref_r, ds, full, ref_r.bracket_micro); assert r.status in ("RECOVERED", "NOT RECOVERED", "NOT EVALUABLE") and r.attempted == 200 and r.result_sha256 == P._t2l_identity(r)
    dup = [full[0]] * 200
    with pytest.raises(P.ProjectionDomainError): P.t2l(ref_r, ds, dup, ref_r.bracket_micro)                            # gate was for a different ensemble
    ds40 = P.design_stability(ref_r, full[:40]); assert not ds40.complete
    with pytest.raises(P.ProjectionDomainError): P.t2l(ref_r, dc.replace(ds40, complete=True, design_stable=True, status="DESIGN-STABLE"), full, ref_r.bracket_micro)   # stale identity
    forged = _mk(P.DesignStability, **{**dc.asdict(ds40), "complete": True, "design_stable": True, "status": "DESIGN-STABLE", "attempted": 200, "scored": 200, "n_matching": 200})
    with pytest.raises(P.ProjectionDomainError, match="do not re-derive"): P.t2l(ref_r, forged, full, ref_r.bracket_micro)              # recomputed identity, semantics refuse
    with pytest.raises(P.ProjectionDomainError): P.t2l(ref_r, ds, full, (ref_r.bracket_micro[1], ref_r.bracket_micro[0]))
    assert P.t2l(ref_r, ds40, full[:40], ref_r.bracket_micro).status == "NOT EVALUABLE"

def test_160_brackets_plus_40_halts_cannot_recover(monkeypatch):
    ref_r = _record_ref("NNUSS", monkeypatch)
    sweeps = [_sw(i, BAND) for i in range(160)] + [_sw(i, BAND, halt="evaluability:uncertified_threshold") for i in range(160, 200)]
    ds = P.design_stability(ref_r, sweeps); r = P.t2l(ref_r, ds, sweeps, ref_r.bracket_micro)
    assert r.status == "NOT EVALUABLE" and r.halted == 40 and math.isclose(r.fail_fraction_over_attempted, 0.2)

def test_apparatus_cache_failure_raises(monkeypatch):
    class Fake:
        role = "production_frozen"; body_sha256 = "b" * 64; file_sha256 = "f" * 64; qualification_sha256 = "q" * 64
        def get(self, m, s): raise A.AuditDomainError("no entry")
    monkeypatch.setattr(A, "is_production_cache", lambda c: True)
    with pytest.raises(P.ProjectionApparatusError): P.projection_sweep(0, Fake())


# ---------------- T2-S grammar (carried) ----------------
def test_t2s_total_over_45_and_malformed_refuse():
    legal = [("LOCATED", None)] + [("NOT_PRODUCED", c) for c in V.NP_CAUSES] + [("NOT_DISTINGUISHED", c) for c in V.ND_CAUSES]
    assert sum(1 for rc in P.STRUCTURE_CLASSES for ev, ec in legal if P.t2s(rc, ev, ec).status in P.T2S_STATUSES) == 45
    with pytest.raises(P.ProjectionDomainError): P.t2s("NO-NULL-PHASE", "NOT_PRODUCED", "boundary_unresolved")


# ---------------- stability (§4.4, §7) ----------------
def test_stability_alternatives_carry_halts_and_halted_alternative_fails_closed(monkeypatch):
    lv = [L[0], L[12], L[23]]; primary = P.classify_grid(lv)
    s = P.stability_audit(lv, primary); P.validate_stability_audit(s, primary)
    assert s.n_realized == 6 and len(s.alternative_records) == 6 and all(len(a) == 9 and a[6] == 0 for a in s.alternatives) and not s.any_alternative_halted and s.role == "analysis_subset" and not s.complete
    with pytest.raises(P.ProjectionDomainError): P.validate_stability_audit(dc.replace(s, within_delta_m_stab=True), primary)
    # a halted alternative: patch the analysis constructor to raise the precision error for one level
    real = N.conditional_thresholds_for_analysis
    def flaky(m, *a, **k):
        if m == L[12]: raise N.NullDomainError(f"threshold not certified at level {P.level_id(m)}: forced")
        return real(m, *a, **k)
    monkeypatch.setattr(N, "conditional_thresholds_for_analysis", flaky)
    s2 = P.stability_audit(lv, primary)
    assert s2.any_alternative_halted and all(a[6] == 1 and a[2] == "REFERENCE-UNRESOLVED" for a in s2.alternatives) and not s2.complete and not s2.within_delta_m_stab
    P.validate_stability_audit(s2, primary)

def test_missing_axis_cell_fails_completion(monkeypatch):
    monkeypatch.setattr(P, "STABILITY_ALT_SEED_SETS", 1)
    with pytest.raises(P.ProjectionDomainError, match="stability_alt_seed_sets"): P.verify_frozen_identity()



# ======================= round 4 (L2 r3 §11): T2-L record validation; alternative records derived =======================
def _canon_pair(monkeypatch):
    ref_r = _record_ref("NNUSS", monkeypatch); full = [_sw(i, BAND) for i in range(200)]; ds = P.design_stability(ref_r, full); assert ds.design_stable
    return ref_r, full, ds

def test_r4_arbitrary_t2l_with_recomputed_identity_refused(monkeypatch):
    ref_r, full, ds = _canon_pair(monkeypatch)
    kw = dict(status="RECOVERED", reason="fabricated", envelope_micro=(1, 2), reference_bracket_micro=ref_r.bracket_micro, production_bracket_micro=ref_r.bracket_micro, attempted=0, halted=0, n_conditioned=0,
              fail_fraction_over_attempted=0.0, ci_half_widths_micro=None, e_l_micro=None, e_u_micro=None, gates=(), conditioned_sha256="", bootstrap_sha256="", design_stability_status="arbitrary",
              design_stability_sha256="b" * 64, reference_sha256="c" * 64)
    fake = _mk(P.T2L, **kw)
    with pytest.raises(P.ProjectionDomainError, match="does not re-derive"): P.validate_t2l(fake, ref_r, ds, full, ref_r.bracket_micro)
    with pytest.raises(P.ProjectionDomainError, match="exact T2L"): P.validate_t2l("x", ref_r, ds, full, ref_r.bracket_micro)

def test_r4_t2l_field_by_field_mutation_refused(monkeypatch):
    ref_r, full, ds = _canon_pair(monkeypatch)
    r = P.t2l(ref_r, ds, full, ref_r.bracket_micro); P.validate_t2l(r, ref_r, ds, full, ref_r.bracket_micro)
    flip = {"RECOVERED": "NOT RECOVERED", "NOT RECOVERED": "RECOVERED", "NOT EVALUABLE": "RECOVERED"}
    for mut in (dict(status=flip[r.status]), dict(reason="x"), dict(attempted=199), dict(halted=1), dict(n_conditioned=r.n_conditioned + 1), dict(fail_fraction_over_attempted=0.5),
                dict(envelope_micro=(1, 2)), dict(e_l_micro=99999), dict(gates=tuple((n, not ok) for n, ok in r.gates)), dict(conditioned_sha256="0" * 64), dict(bootstrap_sha256="0" * 64),
                dict(design_stability_status="x"), dict(design_stability_sha256="0" * 64), dict(reference_sha256="0" * 64), dict(production_bracket_micro=(ref_r.bracket_micro[0] + 1, ref_r.bracket_micro[1]))):
        with pytest.raises(P.ProjectionDomainError): P.validate_t2l(dc.replace(r, **mut), ref_r, ds, full, ref_r.bracket_micro)                # stale identity
        with pytest.raises(P.ProjectionDomainError): P.validate_t2l(_mk(P.T2L, **{**dc.asdict(r), **mut}), ref_r, ds, full, ref_r.bracket_micro)  # recomputed identity: semantics refuse
    with pytest.raises(P.ProjectionDomainError): P.validate_t2l(r, ref_r, ds, full[:199], ref_r.bracket_micro)                                     # different ensemble supplied

def test_r4_fabricated_six_cell_audit_refused():
    ref = P.classify_grid([L[0], L[12], L[23]])
    rows = tuple((k, j, ref.structure_class, None, None, None, 0, (), "a" * 64) for k in range(2) for j in range(3))
    kw = dict(role="canonical", primary_class=ref.structure_class, primary_sha256=ref.result_sha256, grid_sha256=P._digest(ref.levels_micro), alternative_records=(), alternatives=rows, n_expected=6, n_realized=6,
              class_reproduced_by_all=True, any_alternative_halted=False, max_displacement_micro=None, complete=True, within_delta_m_stab=True)
    fake = _mk(P.StabilityAudit, **kw)
    with pytest.raises(P.ProjectionDomainError, match="do not derive from the alternative records"): P.validate_stability_audit(fake, ref)
    kw2 = dict(kw, alternative_records=tuple((k, j, "notarecord") for k in range(2) for j in range(3)))
    with pytest.raises(P.ProjectionDomainError, match="malformed"): P.validate_stability_audit(_mk(P.StabilityAudit, **kw2), ref)

def test_r4_alternative_mutations_refused_and_six_records_derive(monkeypatch):
    lv = [L[0], L[12], L[23]]; ref = P.classify_grid(lv); s = P.stability_audit(lv, ref)
    P.validate_stability_audit(s, ref, replay=True)                                                                      # all six deterministic records reproduce
    assert all(type(r) is P.ReferenceStructure and r.role == "analysis_subset" and len(r.modes) == 3 for _, _, r in s.alternative_records)
    assert s.alternatives == P._sa_rows(ref, s.alternative_records) and all(a[8] == r.result_sha256 for a, (_, _, r) in zip(s.alternatives, s.alternative_records))
    k0, j0, r0 = s.alternative_records[0]
    # a mutated alternative record cannot even be constructed with its own identity recomputed (its class must derive from its labels)
    with pytest.raises(P.ProjectionDomainError): _mk(P.ReferenceStructure, **{**_f(r0), "structure_class": "UNIQUE-THRESHOLD", "bracket_micro": (L[0], L[12]), "midpoint_micro": (L[0] + L[12]) // 2})
    with pytest.raises(P.ProjectionDomainError): _mk(P.ReferenceStructure, **{**_f(r0), "modes": (("mystery", "mystery"),) * 3})
    # a VALID but different alternative record substituted in (labels changed consistently): rows derive from it, so the summary no longer matches → refuse
    alt = P.structure_class(("U", "S", "S"), tuple(lv), modes=r0.modes)
    recs = ((k0, j0, alt),) + s.alternative_records[1:]
    with pytest.raises(P.ProjectionDomainError, match="do not derive"): P.validate_stability_audit(_mk(P.StabilityAudit, **{**_f(s), "alternative_records": recs}), ref)
    rows2 = P._sa_rows(ref, recs); bad = _mk(P.StabilityAudit, **{**_f(s), "alternative_records": recs, "alternatives": rows2, "class_reproduced_by_all": False})
    with pytest.raises(P.ProjectionDomainError, match="replay"): P.validate_stability_audit(bad, ref, replay=True)        # consistent, but not what (k, j) produces
    with pytest.raises(P.ProjectionDomainError): P.validate_stability_audit(_mk(P.StabilityAudit, **{**_f(s), "alternatives": s.alternatives[:-1] + (s.alternatives[-1][:8] + ("0" * 64,),)}), ref)
    with pytest.raises(P.ProjectionDomainError): P.validate_stability_audit(_mk(P.StabilityAudit, **{**_f(s), "within_delta_m_stab": True}), ref)
