"""tests/test_f8_m6.py — Flight 8 module M6: the generator is reading E (Interpretation 002) — the unmodulated SUSTAINED source is
bit-equal to M5's `finite_n_counts`, the NULL source is E at zero feedback whose terminal-window law matches M3's F_W (DKW), the
conditional expectation is the §3.1 map; modulation converts target → probability → hazard → coefficient and refuses illegal
targets; preflight instantiates the named morphology and never sees a trajectory; the F8 DIP is UNRESOLVED by support (E1's
terminal dip would be NO_SUSTAINED); the reachable-level adapter covers every insertion the router can produce and halts on a
missing key; streams are per (level, seed) and order-independent; scoring, records and the qualification join carry E1 M6's
grammar with the adapter in place of the cache; masters are derived from the placement date and refused while it is unset. Round 2
(L2 build review r1): target legality is certified over the whole reachable surface before any trajectory (D1, with L2's accepted-then-
halted candidate as the regression); every placement-sentinel test establishes its own state and the established-date branch is
exercised with no-draw sentries (D2); hi − lo == w for every width (D3); the reentrant onset stays on §6.4's range (D4)."""
import dataclasses
import json
import math
import numpy as np
import pytest

from mfa_instrument.f8 import audit as A
from mfa_instrument.f8 import classify as K
from mfa_instrument.f8 import closure as CL
from mfa_instrument.f8 import config as C
from mfa_instrument.f8 import null as N
from mfa_instrument.f8 import verdict as V

L = C.F8_LEVELS_MICRO
SMOKE_MASTER = 999


@pytest.fixture(scope="module")
def adapter():
    return A.build_adapter("production")


@pytest.fixture(scope="module")
def sweeps(adapter):
    return {name: A.run_sweep(name, 0, SMOKE_MASTER, adapter) for name in A.CLASSES}


# ======================= identity =======================
def test_frozen_identity_and_declared_values():
    A.verify_frozen_identity()
    assert (A.SWEEPS_PER_CLASS, A.CAP, A.CP_CONFIDENCE, A.N_SEEDS, A.MAX_REDRAWS) == (500, 0.10, 0.95, 20, 64)
    assert A.INTENDED_MAP == V.ARCHETYPE_TABLE and len(A.CLASSES) == 12 and set(A.SCIENTIFIC_CLASSES) | set(A.ND_CLASSES) == set(A.CLASSES)
    assert A._digest(A.AUDIT_DECLARATION) == A.AUDIT_DECLARATION_SHA256_LITERAL and A._digest(A.GENERATOR_DECLARATION) == A.GENERATOR_DECLARATION_SHA256_LITERAL
    assert (A._A_NULL, A.Q_DEACT, A.PI1) == N.chain_rates() and A.R_UPPER == 1.0 / (1.0 + A.Q_DEACT)
    assert A.R_FLOOR == CL.rho_re(0.25) and A.PI1 < A.R_FLOOR < A.R_UPPER
    assert A.GENTLE_WIDTH == (108400, 205958) and A.WIDE_WIDTH == (689956, 1003571) and A.TWO_CROSSING_OFFSETS == (391304, 684782) and A.DIP_WINDOWS == (0, 8)


@pytest.mark.parametrize("name,bad", [("AUDIT_DECLARATION_SHA256_LITERAL", "0" * 64), ("GENERATOR_DECLARATION_SHA256_LITERAL", "0" * 64), ("CAP", 0.2),
                                      ("SWEEPS_PER_CLASS", 400), ("MAX_REDRAWS", 8), ("GENTLE_WIDTH", (100000, 205958)), ("DIP_WINDOWS", (0, 9)),
                                      ("TWO_CROSSING_OFFSETS", (300000, 684782)), ("R_FLOOR", 0.06)])
def test_tamper_is_caught(monkeypatch, name, bad):
    monkeypatch.setattr(A, name, bad)
    with pytest.raises(A.AuditDomainError): A.verify_frozen_identity()


# ======================= masters =======================
def test_masters_are_derived_from_the_placement_date_and_refused_while_unset(monkeypatch):
    monkeypatch.setattr(A, "PLACEMENT_DATE", None)                 # the unset state is established HERE, not assumed of the source (D2)
    with pytest.raises(A.AuditDomainError, match="PLACEMENT_DATE"): A.production_masters()
    assert A.masters_for_date(20261101) == (620261101, 720261101, 820261101)
    with pytest.raises(A.AuditDomainError): A.masters_for_date(20261345)
    monkeypatch.setattr(A, "PLACEMENT_DATE", 20261101)
    ms = A.production_masters(); assert len(set(ms)) == 3 and not set(ms) & set(A.DECLARED_MASTERS) and not set(ms) & set(A.E1_RETIRED_MASTERS)
    A.verify_frozen_identity()
    monkeypatch.setattr(A, "DECLARED_MASTERS", A.DECLARED_MASTERS + (620261101,))
    with pytest.raises(A.AuditDomainError, match="collide"): A.verify_frozen_identity()


# ======================= the count processes =======================
@pytest.mark.parametrize("m", [0.25, 1.0, 1.619565, 2.5])
def test_unmodulated_sustained_source_is_bit_equal_to_m5_finite_n_counts(m):
    g1 = np.random.default_rng(np.random.SeedSequence([7, int(m * 1e6)])); g2 = np.random.default_rng(np.random.SeedSequence([7, int(m * 1e6)]))
    assert np.array_equal(A.gen_sustained_run(m, None, g1), CL.finite_n_counts(m, CL.ETA0, g2))


def test_conditional_expectation_is_the_contract_map():
    """E[K'|K=k] = (1−q)k + (N−k)(1−exp(−(η₀+gλ̄k/N))) = N·F_m(k/N): the dynamic bridge to §3.1 that reading A lacks."""
    for m in (0.25, 1.0, 2.5):
        for k in (0, 50, 500, 2499):
            rho = k / A.N_CELLS
            e = (1 - A.Q_DEACT) * k + (A.N_CELLS - k) * (1 - math.exp(-(A.ETA0 + CL.lambda_bar(m) * rho) * A.DT))
            assert abs(e / A.N_CELLS - CL.g_map(rho, m, CL.ETA0)) < 1e-12


def test_null_source_is_e_at_zero_feedback_and_matches_m3_law_on_the_terminal_window():
    """g = 0 reduction: the NULL run is `_count_process(0.0)`; its terminal-window count over 200 independent runs agrees with M3's
    F_W under the DKW bound at α = 0.05 (bound 0.096 at n = 200). A smoke-scale check, not the §4.3 price."""
    g = np.random.default_rng(np.random.SeedSequence([11, 0])); g2 = np.random.default_rng(np.random.SeedSequence([11, 0]))
    assert np.array_equal(A.gen_null_run(g), A._count_process(0.0, g2))
    pmf, cdf, *_ = N.window_count_law()
    n = 200; des = []
    for i in range(n):
        gi = np.random.default_rng(np.random.SeedSequence([11, 1, i]))
        wc = K.window_counts(A.rho_record(A.gen_null_run(gi)))
        des.append(wc[-1])
    emp = np.searchsorted(np.sort(np.array(des)), np.arange(cdf.size), side="right") / n
    sup = float(np.max(np.abs(emp - cdf))); bound = math.sqrt(math.log(2.0 / 0.05) / (2.0 * n))
    assert sup <= bound, (sup, bound)


def test_rho_record_is_on_the_count_grid_and_m2_accepts_it():
    g = np.random.default_rng(3)
    r = A.rho_record(A.gen_sustained_run(1.0, None, g))
    assert r.shape == (K.RECORD_LEN,) and r.dtype == np.float64
    K.recover_counts(r)
    with pytest.raises(A.AuditDomainError): A.rho_record(np.zeros(3000, dtype=np.int64))


# ======================= modulation: target -> probability -> hazard -> coefficient =======================
def test_coefficient_at_the_fixed_point_is_lambda_bar_and_conversion_is_two_steps():
    for u in L:
        m = CL.level_m(u); rs = CL.rho_re(m)
        c = A.target_to_coefficient(np.array([rs]))[0]
        assert abs(c / CL.lambda_bar(m) - 1.0) < 1e-11
        a_tar = A.Q_DEACT * rs / (1 - rs); H = -math.log(1 - a_tar) / A.DT
        assert c == pytest.approx((H - A.ETA0) / rs, rel=1e-13)      # numpy vs math log: ≤ 1 ulp
        assert abs((a_tar - A.ETA0) / rs - c) > 1e-6          # the probability passed straight through as a hazard would be wrong


@pytest.mark.parametrize("r", [0.0, 0.05, 0.066, 0.8466, 0.9, float("nan")])
def test_illegal_targets_are_refused_never_clipped(r):
    with pytest.raises(A.AuditDomainError): A.target_to_coefficient(np.array([r]))


def test_legal_domain_boundaries():
    A.target_to_coefficient(np.array([A.R_FLOOR]))
    A.target_to_coefficient(np.array([np.nextafter(A.R_UPPER, 0.0)]))
    with pytest.raises(A.AuditDomainError): A.target_to_coefficient(np.array([A.R_UPPER]))


def _prm(**kw):
    base = dict(archetype="gentle_onset", onset_micro=1_000_000, width_micro=150_000, temporal="constant", drift=0.0, amp=0.1, period=200,
                att=0.7, att_scale=0.3, pi=0.5, return_offset_micro=500_000, extra_index=0)
    base.update(kw); return A.SweepParams(**base)


def test_schedules_have_the_declared_shapes():
    m = 1.5; rs = CL.rho_re(m)
    d = A.target_schedule(_prm(archetype="persistent_nonstationary_high_m", temporal="drift", drift=0.1), m)
    assert d.shape == (A.TICKS,) and d[0] == rs * 0.95 and abs(d[-1] - rs * (1 + 0.1 * ((A.TICKS - 1) / A.TICKS - 0.5))) < 1e-15
    o = A.target_schedule(_prm(archetype="persistent_nonstationary_high_m", temporal="oscillation", amp=0.2, period=100), m)
    assert o[0] == rs and abs(o[25] - rs * 1.2) < 1e-12 and abs(o[75] - rs * 0.8) < 1e-12
    att = A.target_schedule(_prm(archetype="nonmonotone_amplitude", onset_micro=1_000_000, att=0.9, att_scale=0.2), 2.5)
    assert att[0] == A.R_FLOOR                                  # the floor binds by design at high m (declared max(), not a clip)
    assert A.target_schedule(_prm(), m) is None and A.coefficient_series(_prm(), m) is None


# ======================= preflight =======================
def test_preflight_geometry_and_morphology():
    ok, _ = A.archetype_preflight(_prm()); assert ok
    assert not A.archetype_preflight(_prm(onset_micro=260_000, width_micro=100_000))[0]            # no confident level below
    assert not A.archetype_preflight(_prm(archetype="persistent_nonstationary_high_m", temporal="drift", drift=0.01))[0]   # feature absent
    assert A.archetype_preflight(_prm(archetype="persistent_nonstationary_high_m", temporal="drift", drift=0.05))[0]
    # oscillation at a low onset with a large amplitude drives the target below the floor at low eligible levels -> refused
    assert not A.archetype_preflight(_prm(archetype="persistent_nonstationary_high_m", temporal="oscillation", amp=0.25, onset_micro=400_000, width_micro=50_000))[0]
    assert A.archetype_preflight(_prm(archetype="persistent_nonstationary_high_m", temporal="oscillation", amp=0.25, onset_micro=1_500_000, width_micro=50_000))[0]
    # nonmonotone: a weak attenuation gives a RISING resulting profile (rho* rises faster than kappa falls) -> refused
    ok, why = A.archetype_preflight(_prm(archetype="nonmonotone_amplitude", onset_micro=1_000_000, width_micro=0, att=0.05, att_scale=0.4))
    assert not ok and "decrease" in why
    assert A.archetype_preflight(_prm(archetype="nonmonotone_amplitude", onset_micro=1_000_000, width_micro=0, att=0.9, att_scale=0.2))[0]
    assert not A.archetype_preflight(_prm(archetype="nonmonotone_amplitude", onset_micro=2_450_000, width_micro=0))[0]   # < 2 levels above
    assert A.archetype_preflight(_prm(archetype="two_resolved_crossings", onset_micro=500_000, width_micro=0))[0]
    assert not A.archetype_preflight(_prm(archetype="two_resolved_crossings", onset_micro=1_900_000, width_micro=0))[0]
    assert A.archetype_preflight(_prm(archetype="reentrant", onset_micro=500_000, width_micro=0, return_offset_micro=400_000))[0]
    assert not A.archetype_preflight(_prm(archetype="off_band_mixture", onset_micro=400_000, width_micro=150_000, extra_index=3))[0]
    assert A.archetype_preflight(_prm(archetype="off_band_unresolved", onset_micro=1_000_000, width_micro=50_000, extra_index=3))[0]
    assert not A.archetype_preflight(_prm(archetype="off_band_unresolved", onset_micro=600_000, width_micro=50_000, extra_index=3))[0]


def test_draw_params_is_deterministic_records_attempts_and_halts_on_exhaustion(monkeypatch):
    p1, n1 = A.draw_params("gentle_onset", 123, 0, 5); p2, n2 = A.draw_params("gentle_onset", 123, 0, 5)
    assert p1 == p2 and n1 == n2 >= 1
    assert A.draw_params("gentle_onset", 123, 0, 6)[0] != p1
    monkeypatch.setattr(A, "archetype_preflight", lambda prm: (False, "forced"))
    with pytest.raises(A.GeneratorHalt): A.draw_params("gentle_onset", 123, 0, 5)


def test_preflight_never_consults_a_trajectory(monkeypatch):
    called = []
    monkeypatch.setattr(A, "_count_process", lambda *a, **k: called.append(1))
    A.draw_params("nonmonotone_amplitude", 5, 3, 0); A.draw_params("persistent_nonstationary_high_m", 5, 2, 0)
    assert called == []


# ======================= DIP =======================
def test_dip_is_unresolved_by_support_and_e1_terminal_dip_would_not_be(adapter):
    tp, tt = adapter.theta_p, adapter.theta_t
    assert A.dip_terminal_floor(adapter.index_t) == 142 and 142 * 100 / 250000 > tt and 141 * 100 / 250000 <= tt
    for i in range(20):
        g = np.random.default_rng(np.random.SeedSequence([21, i]))
        c = A.gen_dip_run(1.0, g, adapter.index_t)
        st = K.run_status(A.rho_record(c), tp, tt)
        assert st[0] == "UNRESOLVED" and st[1].s_min == 0.0 and st[1].s_term > tt
        assert (c[K.TAIL_START + 9 * 100:K.TAIL_START + 10 * 100] >= 142).all()
    # an entirely empty process: the floor alone carries S_term, at the equality value 14,200/250,000
    g = np.random.default_rng(0)
    c = A.gen_dip_run(0.25, g, adapter.index_t)
    zero = c.copy(); zero[:] = 0; zero[K.TAIL_START + 900:] = 142
    st = K.run_status(A.rho_record(zero), tp, tt); assert st[0] == "UNRESOLVED" and st[1].s_term == 14200 / 250000
    # E1's construction (zero the terminal window) under F8's single terminal window: NO_SUSTAINED, not UNRESOLVED
    e1 = A.gen_sustained_run(1.0, None, np.random.default_rng(1)); e1[K.TAIL_START + 900:] = 0
    assert K.run_status(A.rho_record(e1), tp, tt)[0] == "NO_SUSTAINED"


# ======================= the reachable-level adapter =======================
def test_adapter_covers_the_reachable_surface_and_binds_the_one_payload(adapter):
    assert adapter.role == "production" and adapter.n_pass1 == 24 and adapter.n_pass2 == 338 and len(adapter.keys) == 362
    assert (adapter.index_p, adapter.index_t) == (14341, 14121) and adapter.theta_p == 14341 / 250000 and adapter.theta_t == 14121 / 250000
    th = N.null_thresholds(L[0]); assert adapter.payload_identity == th.payload_identity()
    assert A.is_production_adapter(adapter)
    n = len(L)
    for i in range(n):
        for j in range(i + 1, n):
            lab = ["N"] * (i + 1) + ["U"] * (j - i - 1) + ["S"] * (n - j)
            for x in V.route(tuple(lab), L).insertions_micro: assert int(x) in adapter.keys
    with pytest.raises(A.AuditDomainError, match="no key"): adapter.get(L[0] + 1)
    with pytest.raises(A.AuditDomainError): A.build_adapter("production", keys=L)
    A.validate_adapter(adapter)
    assert A.adapter_from_json(A.adapter_to_json(adapter)) == adapter
    bad = dataclasses.replace(adapter, theta_p=0.06)
    with pytest.raises(A.AuditDomainError): A.validate_adapter(bad)
    assert not A.is_production_adapter(bad)
    sl = A.build_adapter("slice", keys=L); assert sl.role == "slice" and not A.is_production_adapter(sl) and sl.get(L[3]) == (adapter.theta_p, adapter.theta_t)
    with pytest.raises(A.AuditDomainError): A.build_adapter("slice", keys=(L[0] + 1,))


def test_adapter_json_tamper_is_caught(adapter):
    doc = json.loads(A.adapter_to_json(adapter)); doc["body"]["keys"] = doc["body"]["keys"][:-1]
    with pytest.raises(A.AuditDomainError): A.adapter_from_json(json.dumps(doc))


# ======================= streams =======================
def test_run_streams_are_per_level_and_seed_and_order_independent(adapter):
    prm, _ = A.draw_params("gentle_onset", SMOKE_MASTER, 0, 0); us = A.regime_uniforms(SMOKE_MASTER, 0, 0)
    r1 = A.generate_run("gentle_onset", prm, L[5], 3, float(us[3]), adapter, SMOKE_MASTER, 0, 0)
    _ = A.generate_run("gentle_onset", prm, L[9], 3, float(us[3]), adapter, SMOKE_MASTER, 0, 0)
    r2 = A.generate_run("gentle_onset", prm, L[5], 3, float(us[3]), adapter, SMOKE_MASTER, 0, 0)
    assert r1[0] == r2[0] and np.array_equal(r1[1], r2[1])
    r3 = A.generate_run("gentle_onset", prm, L[5], 4, float(us[4]), adapter, SMOKE_MASTER, 0, 0)
    assert not np.array_equal(r1[1], r3[1])
    assert np.array_equal(A.regime_uniforms(SMOKE_MASTER, 0, 0), us) and us.shape == (20,)
    assert A.run_stream(1, 2, 3, L[0], 0).random() != A.run_stream(1, 2, 3, L[0] + 1, 0).random()


# ======================= sweeps =======================
def test_one_sweep_per_class_is_well_formed_and_scored_on_the_final_level_set(sweeps, adapter):
    for name, r in sweeps.items():
        assert r.archetype == name and r.generator_halt is None and r.evaluability_halt is None
        assert len(r.pass1_labels) == 24 and r.final_verdict in V.VERDICTS and r.adapter_sha256 == adapter.body_sha256
        assert r.router_row in ("P2R-1", "P2R-2", "P2R-5", "P2R-6")
        assert r.final_levels_micro == tuple(sorted(set(L) | set(r.insertions_micro)))
        v = V.evaluate(r.final_labels, r.final_levels_micro); assert (v.verdict, v.cause, v.rule) == (r.final_verdict, r.final_cause, r.final_rule)
        for x in r.insertions_micro: assert x in adapter.keys
    # classes whose verdict is deterministic given the regime assignment
    for name in ("no_sustained_anywhere", "no_null_consistent_anywhere", "two_resolved_crossings", "reentrant", "unresolved_heavy_boundary", "off_band_unresolved"):
        assert (sweeps[name].final_verdict, sweeps[name].final_cause) == A.INTENDED[name], name
    assert sweeps["no_null_consistent_anywhere"].pass1_labels == ("S",) * 24 and sweeps["no_sustained_anywhere"].pass1_labels == ("N",) * 24


def test_missing_adapter_key_is_an_apparatus_halt_not_a_derivation(adapter):
    sl = A.build_adapter("slice", keys=L)           # pass-1 only: any insertion is a missing key
    r = A.run_sweep("abrupt_onset", 0, SMOKE_MASTER, sl)
    assert r.final_verdict == "HALTED" and r.evaluability_halt.startswith("apparatus:") and r.realized_insertions == 8 and len(r.pass1_labels) == 24
    s = A.score_class([r], 1)
    assert s.halted == 1 and s.scored == 0 and s.complete_pass is False and s.cp_upper_95 == 1.0 and s.halt_keys == (r.evaluability_halt,)
    A.validate_class_score(s, 1)


def test_generator_halt_is_recorded_in_completion(monkeypatch, adapter):
    monkeypatch.setattr(A, "archetype_preflight", lambda prm: (False, "forced"))
    r = A.run_sweep("gentle_onset", 0, SMOKE_MASTER, adapter)
    assert r.generator_halt and r.final_verdict == "GENERATOR_HALT" and r.preflight_attempts == A.MAX_REDRAWS
    s = A.score_class([r], 1); assert s.generator_halted == 1 and not s.complete_pass; A.validate_class_score(s, 1)


# ======================= scoring, records, qualification =======================
def test_class_scores_recompute_and_tamper_is_caught(sweeps):
    for name, r in sweeps.items():
        s = A.score_class([r], 1); A.validate_class_score(s, 1)
        assert s.applicable_error == ("false_nd" if name in A.SCIENTIFIC_CLASSES else "false_scientific") and s.attempted == s.scored == 1
        assert s.complete_pass is False                       # requested 1 != 500
        bad = dataclasses.replace(s, errors=s.errors + 1)
        with pytest.raises(A.AuditDomainError): A.validate_class_score(bad, 1)
    s = A.score_class([sweeps["gentle_onset"]], 1)
    with pytest.raises(A.AuditDomainError): A.validate_class_score(dataclasses.replace(s, complete_pass=True), 1)
    with pytest.raises(A.AuditDomainError): A.validate_class_score(dataclasses.replace(s, exact_agreement_descriptive=0.5), 1)


def test_clopper_pearson_known_values():
    assert A.clopper_pearson_upper(0, 500) == pytest.approx(1 - 0.05 ** (1 / 500), abs=1e-9)
    assert A.clopper_pearson_upper(500, 500) == 1.0 and A.clopper_pearson_upper(0, 10000) == pytest.approx(0.0002995, abs=2e-7)
    assert A.clopper_pearson_upper(29, 500) < A.CAP < A.clopper_pearson_upper(45, 500)


def test_smoke_audit_record_validates_and_production_paths_are_refused(adapter, monkeypatch):
    monkeypatch.setattr(A, "PLACEMENT_DATE", None)                 # D2: the refusals below are the UNSET branch, established locally
    rec = A.run_audit("design", adapter, sweeps_per_class=1, master=SMOKE_MASTER)
    assert rec.ensemble_pass is False and rec.requested_sweeps_per_class == 1 and rec.master == SMOKE_MASTER and rec.adapter_role == "production"
    A.validate_audit_record(rec, expect_production=False)
    with pytest.raises(A.AuditDomainError): A.validate_audit_record(rec, expect_production=True)        # not a production master
    with pytest.raises(A.AuditDomainError): A.validate_audit_record(dataclasses.replace(rec, ensemble_pass=True), expect_production=False)
    with pytest.raises(A.AuditDomainError): A.validate_audit_record(dataclasses.replace(rec, record_sha256="0" * 64), expect_production=False)
    with pytest.raises(A.AuditDomainError): A.run_audit("design", adapter)                               # 500 sweeps: masters unset
    with pytest.raises(A.AuditDomainError): A.run_audit("design", A.build_adapter("slice", keys=L), sweeps_per_class=500)
    with pytest.raises(A.AuditDomainError): A.run_audit("design", adapter, sweeps_per_class=500, master=SMOKE_MASTER)
    held = A.run_audit("held_out", adapter, sweeps_per_class=1, master=SMOKE_MASTER + 1)
    q = A.qualify_audit(rec, held)
    assert q.qualified is False and any("not 500 requested" in r for r in q.reasons) and q.design_record_sha256 == rec.record_sha256
    A.validate_audit_qualification(q, rec, held)
    with pytest.raises(A.AuditDomainError): A.validate_audit_qualification(dataclasses.replace(q, qualified=True), rec, held)
    q2 = A.qualify_audit(rec, rec); assert "masters not distinct" in q2.reasons and "record identities not distinct" in q2.reasons


class _Sentry(Exception):
    pass


def test_established_date_dispatches_production_paths_under_the_derived_masters_without_a_draw(adapter, monkeypatch):
    """D2: with a date established, the 500-sweep audit and the full price DISPATCH under the derived masters; sentries at
    `run_sweep` and `gen_null_run` stop them before any parameter or trajectory draw, so no production observation is generated."""
    monkeypatch.setattr(A, "PLACEMENT_DATE", 20261101)
    seen = {}
    def sweep_sentry(archetype, sweep_index, master, ad):
        seen["sweep"] = (archetype, sweep_index, master, ad.body_sha256); raise _Sentry()
    monkeypatch.setattr(A, "run_sweep", sweep_sentry)
    with pytest.raises(_Sentry): A.run_audit("design", adapter)
    assert seen["sweep"] == (A.CLASSES[0], 0, 620261101, adapter.body_sha256)
    with pytest.raises(_Sentry): A.run_audit("held_out", adapter)
    assert seen["sweep"][2] == 720261101
    with pytest.raises(A.AuditDomainError): A.run_audit("design", adapter, master=SMOKE_MASTER)        # overrides stay refused
    with pytest.raises(A.AuditDomainError): A.run_audit("design", A.build_adapter("slice", keys=L))
    def null_sentry(g):
        seen["price_first_draw"] = g.integers(0, 2 ** 31); raise _Sentry()
    monkeypatch.setattr(A, "gen_null_run", null_sentry)
    with pytest.raises(_Sentry): A.run_pricing(adapter)
    expected = np.random.default_rng(np.random.SeedSequence([820261101, 0, 0])).integers(0, 2 ** 31)
    assert seen["price_first_draw"] == expected                       # the pricing stream is the declared one under the derived master
    with pytest.raises(A.AuditDomainError): A.run_pricing(adapter, master=SMOKE_MASTER)
    # a production-record validation with the date established compares the master to the derived one
    assert A._ensemble_master("design") == 620261101 and A._ensemble_master("held_out") == 720261101


# ======================= D1 / D3 / D4 regressions (L2 build review r1) =======================
def test_d1_target_legality_is_certified_over_the_reachable_surface_before_any_trajectory(adapter, monkeypatch):
    """L2's reproduction: sweep 302 of `persistent_nonstationary_high_m` under smoke master 999 — attempt 1 drew onset 457,729,
    width 14,827, oscillation A = 0.2332, legal at every pass-1 level ≥ lo but illegal at the reachable insertion 456,522. The
    candidate must now be refused at preflight (never after a draw), the accepted candidate must be legal at every reachable key ≥ lo,
    and the sweep must complete without an apparatus halt."""
    ci = A.CLASSES.index("persistent_nonstationary_high_m")
    p0 = A._draw_once("persistent_nonstationary_high_m", np.random.default_rng(np.random.SeedSequence([999, ci, 302, 2, 0])))
    assert (p0.onset_micro, p0.width_micro, p0.temporal, p0.period) == (457729, 14827, "oscillation", 348) and abs(p0.amp - 0.23318631999240286) < 1e-15
    assert min(A.target_schedule(p0, CL.level_m(543478))) >= A.R_FLOOR            # legal on the lowest eligible pass-1 level …
    assert min(A.target_schedule(p0, CL.level_m(456522))) < A.R_FLOOR             # … illegal at the first reachable insertion
    ok, why = A.archetype_preflight(p0); assert not ok and "456522" in why
    called = []; monkeypatch.setattr(A, "_count_process", lambda *a, **k: called.append(1) or np.zeros(A.RECORD_LEN, dtype=np.int64))
    prm, attempts = A.draw_params("persistent_nonstationary_high_m", 999, ci, 302)
    assert called == [] and attempts == 2
    for u in A.reachable_surface_keys():
        if u >= prm.lo:
            s = A.target_schedule(prm, CL.level_m(u)); assert s.min() >= A.R_FLOOR and s.max() < A.R_UPPER
    monkeypatch.undo()
    r = A.run_sweep("persistent_nonstationary_high_m", 302, 999, adapter)
    assert r.evaluability_halt is None and r.generator_halt is None and r.final_verdict in V.VERDICTS and r.preflight_attempts == 2


def test_schedule_envelope_bounds_the_series_everywhere():
    for a, kw in (("persistent_nonstationary_high_m", dict(temporal="drift", drift=0.08)), ("persistent_nonstationary_high_m", dict(temporal="drift", drift=-0.07)),
                  ("persistent_nonstationary_high_m", dict(temporal="oscillation", amp=0.2, period=333)), ("persistent_nonstationary_high_m", dict(temporal="oscillation", amp=0.1, period=400)),
                  ("nonmonotone_amplitude", dict(att=0.8, att_scale=0.3))):
        prm = _prm(archetype=a, onset_micro=1_000_000, width_micro=50_000, **kw)
        for u in (1_032_609, 1_050_000, 2_500_000):
            s = A.target_schedule(prm, CL.level_m(u)); lo_, hi_ = A._schedule_extremes(prm, u)
            assert lo_ <= s.min() + 1e-15 and s.max() <= hi_ + 1e-15
            if kw.get("temporal") != "oscillation": assert abs(lo_ - s.min()) < 1e-15 and abs(hi_ - s.max()) < 1e-15
    assert len(A.reachable_surface_keys()) == 362


@pytest.mark.parametrize("w", [0, 1, 2, 108401, 192863, 689957, 1003571])
def test_d3_width_endpoints_preserve_the_integer_width(w):
    p = _prm(width_micro=w); assert p.hi - p.lo == w and p.lo == p.onset_micro - w // 2
    if w == 0: assert p.lo == p.hi == p.onset_micro
    p7, _ = A.draw_params("gentle_onset", 999, 0, 7)
    assert (p7.onset_micro, p7.width_micro) == (1485901, 192863) and p7.hi - p7.lo == 192863       # L2's reproduction


def test_d3_odd_width_ramp_fraction_uses_the_declared_width():
    p = _prm(width_micro=1, onset_micro=1_000_000)
    assert A.regime_at("gentle_onset", 1_000_000, p, 0.0) == "NULL" and A.regime_at("gentle_onset", 1_000_001, p, 0.99) == "SUSTAINED"


def test_d4_reentrant_onset_stays_on_the_frozen_range():
    ci = A.CLASSES.index("reentrant"); top = C.F8_M_MAX_MICRO - 8 * C.S_P1_MICRO
    assert dict(A.GENERATOR_DECLARATION)["onset_range_reentrant"] == (C.F8_M_MIN_MICRO + C.S_P1_MICRO, top) == (347826, 1717392)
    onsets = [A.draw_params("reentrant", 999, ci, i)[0].onset_micro for i in range(120)]
    assert max(onsets) <= top and min(onsets) >= 347826
    p24, _ = A.draw_params("reentrant", 999, ci, 24); assert p24.onset_micro <= top                 # L2's draw now lies inside
    for i in range(0, 120, 17):
        p = A.draw_params("reentrant", 999, ci, i)[0]
        assert any(u >= p.onset_micro + p.return_offset_micro for u in L)                             # a final NULL region always exists


def test_dip_direct_function_with_an_empty_process_and_the_last_nonterminal_window(adapter, monkeypatch):
    """L2's direct-function case: substitute an all-zero count process and force w = 8 — the function itself floors the terminal
    window at 142 and M2 returns UNRESOLVED; one count below the floor's total (14,121) would be NO_SUSTAINED."""
    monkeypatch.setattr(A, "_count_process", lambda *a, **k: np.zeros(A.RECORD_LEN, dtype=np.int64))
    g = np.random.default_rng(0)
    c = A.gen_dip_run(1.0, g, adapter.index_t)
    assert (c[K.TAIL_START + 900:] == 142).all() and (c[:K.TAIL_START + 900] == 0).all()
    assert K.run_status(A.rho_record(c), adapter.theta_p, adapter.theta_t)[0] == "UNRESOLVED"
    t = c.copy(); t[K.TAIL_START + 900:] = 141; t[K.TAIL_START + 900] = 162          # 99·141 + 162 = 14,121 exactly: at the threshold
    assert K.run_status(A.rho_record(t), adapter.theta_p, adapter.theta_t)[0] == "NO_SUSTAINED"
    t[K.TAIL_START + 900] = 163                                                          # 14,122: one above
    assert K.run_status(A.rho_record(t), adapter.theta_p, adapter.theta_t)[0] == "UNRESOLVED"


# ======================= price and comparison side =======================
def test_price_is_the_s_min_event_with_exact_cp_and_the_full_run_is_gated(adapter, monkeypatch):
    monkeypatch.setattr(A, "PLACEMENT_DATE", None)                 # D2
    p = A.run_pricing(adapter, replicates=40, master=SMOKE_MASTER)
    assert p.replicates == 40 and p.s_min_rejection_rate == p.s_min_rejections / 40 and p.cp_upper_95 == A.clopper_pearson_upper(p.s_min_rejections, 40)
    assert p.alpha_p_nominal == 0.001 and 0 < p.construction_bound <= 0.001 and p.source == "m6_null_count_process" and p.s_term_no_sustained >= 36
    with pytest.raises(A.AuditDomainError): A.run_pricing(adapter)                                        # full price: masters unset
    with pytest.raises(A.AuditDomainError): A.run_pricing(adapter, replicates=A.PRICING_REPLICATES, master=SMOKE_MASTER)


def test_surrogate_level_stats_is_interpretation_001_tail_density():
    s = A.surrogate_level_stats(L[0], SMOKE_MASTER, replicates=12)
    assert s.replicates == 12 and abs(s.tail_mean - CL.rho_re(0.25)) < 0.005 and s.tail_sd > 0 and s.se_mean == s.tail_sd / math.sqrt(12)
    with pytest.raises(A.AuditDomainError): A.surrogate_level_stats(L[0] + 1, SMOKE_MASTER, replicates=4)
