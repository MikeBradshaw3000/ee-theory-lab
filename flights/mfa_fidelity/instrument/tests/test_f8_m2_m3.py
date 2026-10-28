"""tests/test_f8_m2_m3.py — Flight 8 modules M2 (classify) and M3 (Markov null). M2: frozen identities; exact count-grid
statistics on the F8 record convention; S_term = the single terminal window; status precedence; 16/2/4 labels total and
exclusive; known-answer controls bit-exact. M3: the per-cell transfer-matrix law against brute-force path enumeration and
an exact rational DP; the N-fold law against an exact rational convolution at small N and the direct path at N = 2500;
certificates and quantile certification fail closed; thresholds level-independent, cached per level, replayed; the
stepper at g = 0 realizes the law (DKW); Appendix A's null row reproduced."""
import dataclasses
import itertools
import math
from fractions import Fraction
import numpy as np
import pytest

from mfa_instrument.f8 import config as C
from mfa_instrument.f8 import dynamics as D
from mfa_instrument.f8 import classify as K
from mfa_instrument.f8 import null as N


def _record(tail_counts_by_window, pre=0):
    """A production-shape record rho[0..3000] on the count grid with given per-window constant counts."""
    r = np.full(K.RECORD_LEN, np.float64(pre) / 2500.0)
    for i, c in enumerate(tail_counts_by_window):
        r[K.TAIL_START + i * K.WINDOW:K.TAIL_START + (i + 1) * K.WINDOW] = np.float64(c) / 2500.0
    return r


# ======================= M2 =======================
def test_m2_frozen_identity_and_geometry():
    K.verify_frozen_identity()
    assert K.frozen_digest() == K.CLASSIFY_SHA256_LITERAL and K.controls_digest() == K.CONTROL_CASES_SHA256_LITERAL
    assert (K.TAIL_START, K.TAIL_END, K.WINDOW, K.N_WINDOWS, K.TERMINAL_WINDOW, K.RECORD_LEN, K.N_CELLS) == (2001, 3000, 100, 10, 9, 3001, 2500)
    assert dict(K.COUNTS) == {"n_runs": 20, "confident_min": 16, "confident_max_other": 2, "mixed_min_each": 4}

@pytest.mark.parametrize("name,bad", [("CLASSIFY_SHA256_LITERAL", "0" * 64), ("WINDOW", 50), ("TERMINAL_WINDOW", 8), ("CONFIDENT_MIN", 15)])
def test_m2_tamper_is_caught(monkeypatch, name, bad):
    monkeypatch.setattr(K, name, bad)
    with pytest.raises(K.ClassifyDomainError): K.tail_stats(_record([1250] * 10))

def test_m2_tail_is_the_last_1000_post_advance_ticks_and_s_term_is_the_tenth_window():
    r = _record([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], pre=2500)   # pre-tail saturated: must not enter
    st = K.tail_stats(r)
    assert st.window_means == tuple(c / 2500.0 for c in range(100, 1100, 100)) and st.s_min == 100 / 2500.0 and st.s_term == 1000 / 2500.0
    assert K.window_counts(r) == tuple(c * 100 for c in range(100, 1100, 100))
    r2 = r.copy(); r2[2000] = 0.0                                           # tick 2000 is outside the tail
    assert K.tail_stats(r2) == st
    r3 = r.copy(); r3[2001] = 0.0                                           # tick 2001 is inside
    assert K.tail_stats(r3) != st

def test_m2_refuses_off_grid_and_wrong_length_records():
    assert K.tail_stats(np.full(3001, 0.3)).s_min == 0.3                                     # 750/2500 is ON the grid
    with pytest.raises(K.ClassifyDomainError): K.tail_stats(np.full(3001, 0.30001))
    with pytest.raises(K.ClassifyDomainError): K.tail_stats(np.full(3000, 0.5))
    with pytest.raises(K.ClassifyDomainError): K.tail_stats(np.full(3001, 0.5, dtype=np.float32))
    bad = _record([1250] * 10); bad[2500] = 1.5
    with pytest.raises(K.ClassifyDomainError): K.tail_stats(bad)

def test_m2_run_status_precedence_and_threshold_domain():
    r = _record([1250] * 10)
    assert K.run_status(r, 0.12, 0.12)[0] == "SUSTAINED"
    assert K.run_status(_record([0] * 10), 0.12, 0.12)[0] == "NO_SUSTAINED"
    assert K.run_status(_record([1250] * 9 + [0]), 0.12, 0.12)[0] == "NO_SUSTAINED"       # terminal window alone decides
    assert K.run_status(_record([0] + [1250] * 9), 0.12, 0.12)[0] == "UNRESOLVED"
    assert K.run_status(_record([300] * 10), 0.12, 0.12)[0] == "NO_SUSTAINED"             # exactly at both thresholds
    for bad in (0.12j, "0.12", 1, True, np.float32(0.12), 1.5, float("nan")):
        with pytest.raises(K.ClassifyDomainError): K.run_status(r, bad, 0.12)

def test_m2_level_labels_total_exclusive_and_verbatim():
    seen = set()
    for ns in range(21):
        for nn in range(21 - ns):
            lab = K.level_label(K.LevelCounts(ns, nn, 20 - ns - nn)); seen.add(lab)
            exp = "S" if ns >= 16 and nn <= 2 else "N" if nn >= 16 and ns <= 2 else "M" if ns >= 4 and nn >= 4 else "U"
            assert lab == exp
    assert seen == {"S", "N", "M", "U"}
    with pytest.raises(K.ClassifyDomainError): K.level_label(K.LevelCounts(16, 2, 3))
    with pytest.raises(K.ClassifyDomainError): K.level_counts(["SUSTAINED"] * 19)
    with pytest.raises(K.ClassifyDomainError): K.level_counts(["SUSTAINED"] * 19 + ["MAYBE"])
    assert K.level_counts(["SUSTAINED"] * 17 + ["NO_SUSTAINED"] * 2 + ["UNRESOLVED"]) == K.LevelCounts(17, 2, 1)

def test_m2_statuses_by_seed_require_exactly_the_panel():
    good = {s: "SUSTAINED" for s in C.F8_SEED_PANEL}
    assert K.level_statuses_by_seed(good) == ("SUSTAINED",) * 20
    bad = dict(good); bad.pop(C.F8_SEED_PANEL[0]); bad[12345] = "SUSTAINED"
    with pytest.raises(K.ClassifyDomainError): K.level_statuses_by_seed(bad)
    with pytest.raises(K.ClassifyDomainError): K.level_statuses_by_seed({s: "SUSTAINED" for s in C.F8_CALIBRATION_SEED_PANEL})

def test_m2_controls_qualify_bit_exact_and_duplicates_refused():
    q = K.qualify_controls()
    assert q.passed and len(q.results) == 7 and not q.missing and all(ok and i == o for _, i, o, ok in q.results)
    assert {cid for cid, *_ in K.CONTROL_CASES} == {r[0] for r in q.results}
    with pytest.raises(K.ClassifyDomainError): K.qualify_controls(["stable_above_null", "stable_above_null"])
    assert not K.qualify_controls(["stable_above_null"]).passed
    r, intended, smin, sterm = K.constructed_series("slow_drift_persistent", 0.12, 0.12)
    assert (smin, sterm, intended) == (Fraction(1, 2), Fraction(19, 20), "SUSTAINED") and K.tail_stats(r).s_term == 0.95

def test_m2_classifies_a_real_stepper_record():
    r = D.run(C.f8_run_spec(C.F8_LEVELS_MICRO[23], C.F8_SEED_PANEL[0], "realization"))
    th = N.null_thresholds(C.F8_LEVELS_MICRO[23])
    status, st = K.run_status(r.rho, th.theta_p, th.theta_t)
    assert status == "SUSTAINED" and st.window_means == r.tail_window_means and st.s_min > th.theta_p


# ======================= M3: the per-cell law =======================
def _brute_cell_pmf(a, q, pi1, w):
    """Enumerate every path of a stationary two-state chain over w ticks, exact rationals."""
    A, Qd, P1 = Fraction(a), Fraction(q), Fraction(pi1)
    out = [Fraction(0)] * (w + 1)
    for path in itertools.product((0, 1), repeat=w):
        p = P1 if path[0] else 1 - P1
        for x, y in zip(path, path[1:]):
            p *= (A if y else 1 - A) if x == 0 else (1 - Qd if y else Qd)
        out[sum(path)] += p
    return out

def test_m3_cell_law_matches_brute_force_and_exact_dp_at_small_window():
    a, q, pi1 = N.chain_rates()
    for w in (1, 2, 5, 8):
        brute = _brute_cell_pmf(a, q, pi1, w)
        assert N.cell_window_pmf_exact(a, q, pi1, w) == brute
        f = N.cell_window_pmf(a, q, pi1, w)
        assert max(abs(Fraction(float(x)) - b) for x, b in zip(f, brute)) < Fraction(1, 10**14) and abs(f.sum() - 1.0) < 1e-14

def test_m3_cell_law_moments_at_window_100():
    a, q, pi1 = N.chain_rates()
    f = N.cell_window_pmf(a, q, pi1); k = np.arange(101)
    assert abs((k * f).sum() - 100 * pi1) < 1e-12                           # stationary mean occupancy = W·π₁
    rho = 1.0 - a - q; var_exact = sum(pi1 * (1 - pi1) * rho ** abs(i - j) for i in range(100) for j in range(100))
    assert abs(((k - 100 * pi1) ** 2 * f).sum() - var_exact) < 1e-10        # exact stationary variance of a two-state chain sum
    assert N.certified_cell_pmf(a, q, pi1)[2] < 1e-14

def test_m3_n_fold_law_fft_matches_exact_rational_convolution_at_small_n():
    a, q, pi1 = N.chain_rates()
    cell, cert, _ = N.certified_cell_pmf(a, q, pi1)
    ex = N.cell_window_pmf_exact(a, q, pi1)
    conv = ex
    for _ in range(3):                                                     # 4-fold exact convolution
        conv = [sum(conv[i] * ex[k - i] for i in range(max(0, k - 100), min(k, len(conv) - 1) + 1)) for k in range(len(conv) + 100)]
    pmf, wcert = N.window_count_pmf(cell, cert, 4)
    assert pmf.size == 401 and wcert.reps == 4 and wcert.support == 400
    assert max(abs(Fraction(float(x)) - e) for x, e in zip(pmf, conv)) < Fraction(1, 10**13)

def test_m3_production_law_direct_path_and_appendix_a_null_row():
    pmf, cdf, cell_cert, w_cert, dist, disc_max, disc, agree = N.window_count_law()
    assert pmf.size == 250001 and w_cert.reps == 2500 and agree and disc_max <= w_cert.sum_l1_bound and disc < 1e-20
    k = np.arange(pmf.size); mean = (k * pmf).sum() / 250000; sd = np.sqrt(((k - mean * 250000) ** 2 * pmf).sum()) / 250000
    assert abs(mean - 0.052282320137314486) < 1e-9 and abs(sd - 0.0013366382702463503) < 2e-9    # Appendix A: pi1, sigma_null
    direct, off, _ = N.direct_convolution_pmf_truncated(N.certified_cell_pmf(*N.chain_rates())[0])
    assert abs(direct.sum() - 1.0) < 1e-12 and np.max(np.abs(direct - pmf)) < 1e-12


# ======================= M3: certificates and thresholds =======================
def test_m3_thresholds_level_independent_certified_and_ordered():
    ths = [N.null_thresholds(m) for m in C.F8_LEVELS_MICRO]
    assert len({(t.theta_p, t.theta_t) for t in ths}) == 1 and all(t.theta_p > t.theta_t for t in ths)
    t = ths[0]
    assert t.theta_p_certificate.quantile == 0.9999 and t.theta_t_certificate.quantile == 0.999
    assert t.theta_p == t.theta_p_certificate.index / 250000 and t.theta_t == t.theta_t_certificate.index / 250000
    assert abs(t.theta_p - 0.0573) < 2e-4                                   # Appendix A's Gaussian provisional theta_P, exact now
    assert N.familywise_nominal_bound(t) <= N.ALPHA_P
    for c in (t.theta_p_certificate, t.theta_t_certificate):
        assert c.certified and c.mode in N.THRESHOLD_MODES_SET and 0 <= c.displacement <= 3 and c.cdf_at_selected - c.error_bound >= c.quantile
    assert ths[5].level_id == C.level_id(C.F8_LEVELS_MICRO[5]) and ths[5].payload_identity() != ths[0].payload_identity()

def test_m3_thresholds_refuse_non_pass1_levels_and_tamper():
    for bad in (1_000_000, 250_001, True, 2.5):
        with pytest.raises(N.NullDomainError): N.null_thresholds(bad)

@pytest.mark.parametrize("name,bad", [("NULL_SHA256_LITERAL", "0" * 64), ("ALPHA_T", 0.01), ("Q_P", 0.999), ("NULL_ERROR_BOUND_FLOOR", 1e-12)])
def test_m3_declaration_tamper_is_caught(monkeypatch, name, bad):
    monkeypatch.setattr(N, name, bad)
    with pytest.raises(N.NullDomainError): N.verify_frozen_identity()

def test_m3_certificate_objects_fail_closed():
    t = N.null_thresholds(C.F8_LEVELS_MICRO[0]); c = t.theta_t_certificate
    for kw in ({"certified": False}, {"mode": "exact_certified"} if c.mode == "conservative_coverage" else {"mode": "conservative_coverage"},
               {"value": c.value + 1e-9}, {"displacement": c.displacement + 1}, {"quantile": 0.99}, {"denominator": 2500}, {"ordinary_certifiable": not c.ordinary_certifiable}):
        with pytest.raises(N.NullDomainError): dataclasses.replace(c, **kw)
    for kw in ({"theta_t": t.theta_t + 4e-6}, {"theta_p": t.theta_t}, {"level_micro": 1_000_000}, {"direct_agrees": False}, {"a": 0.5}, {"scoring_object_version": "x"},
               {"direct_max_cdf_discrepancy": 1.0}, {"theta_p_certificate": t.theta_t_certificate}):
        with pytest.raises(N.NullDomainError): dataclasses.replace(t, **kw)
    with pytest.raises(N.NullDomainError): dataclasses.replace(t.window_pmf_certificate, sum_l1_bound=1e-3)

def test_m3_quantile_selection_modes():
    cdf = np.array([0.0, 0.5, 0.9985, 0.9992, 0.99991, 0.99999, 1.0]); N_ = N.WINDOW_DENOM
    c = N._quantile(cdf, N.Q_T, 1e-5)                                         # margins 0.0005 / 0.0002 > eps: exact mode
    assert c.mode == "exact_certified" and c.index == 3 == c.ordinary_index and c.displacement == 0
    c2 = N._quantile(cdf, N.Q_T, 3e-4)                                        # margin_at 0.0002 < eps: conservative, k_safe = 4
    assert c2.mode == "conservative_coverage" and c2.ordinary_index == 3 and c2.index == 4 and c2.displacement == 1
    with pytest.raises(N.NullDomainError): N._quantile(cdf, N.Q_P, 2e-4)      # F(k) − eps ≥ 0.9999 never holds before the top

def test_m3_cache_builds_replays_roundtrips_and_refuses_tamper():
    cache = N.build_threshold_cache(); N.validate_threshold_cache(cache)
    assert cache.n_levels == 24 and cache.role == "production" and len({e[1] for e in cache.entries}) == 1 and len({e[3] for e in cache.entries}) == 24
    js = N.cache_to_json(cache); assert N.cache_from_json(js) == cache
    bad = js.replace(cache.entries[0][3], "0" * 64, 1)
    with pytest.raises(N.NullDomainError): N.cache_from_json(bad)
    N.validate_threshold_cache(dataclasses.replace(cache, role="slice"))                       # a slice over all levels is legitimate
    tampered = cache.entries[:1] + ((cache.entries[1][0], cache.entries[1][1] + 4e-6, cache.entries[1][2], cache.entries[1][3]),) + cache.entries[2:]
    with pytest.raises(N.NullDomainError): N.validate_threshold_cache(dataclasses.replace(cache, entries=tampered))
    with pytest.raises(N.NullDomainError): N.build_threshold_cache(C.F8_LEVELS_MICRO[:3], "production")
    sl = N.build_threshold_cache(C.F8_LEVELS_MICRO[:3], "slice"); assert sl.n_levels == 3 and sl.law_identity == cache.law_identity
    with pytest.raises(N.NullDomainError): N.build_threshold_cache([1_000_000], "slice")


# ======================= M3: the stepper realizes the law =======================
def test_m3_stepper_null_matches_law_at_reduced_grid_with_scaled_thresholds():
    v = N.validate_on_stepper(60, grid=12, ticks=1100)
    assert v.n_cells_scaled and v.thresholds_scope == "smoke_scaled_grid" and not v.production_scope_eligible and not v.qualification_passed
    assert v.dkw_passed and v.dkw_bound == math.sqrt(math.log(40.0) / 120.0) and abs(v.empirical_mean_density - N.chain_rates()[2]) < 0.01
    assert abs(v.exceed_q99_rate - 0.01) < 0.03
    th = N.null_thresholds(C.F8_LEVELS_MICRO[0])
    assert (v.theta_p_used, v.theta_t_used) != (th.theta_p, th.theta_t) and v.theta_p_used > v.theta_t_used      # D2: the scaled law's own quantiles
    assert v.theta_t_used > th.theta_t                                                                              # a smaller N has a wider null: higher quantiles
    assert v.exceed_theta_t_rate <= 0.02 and v.exceed_theta_p_rate <= 0.01                                        # calibrated against the scaled nominal, not mixed

def test_m3_stepper_null_at_full_n_is_qualification_scope_and_shape_policy():
    v = N.validate_on_stepper(10)
    th = N.null_thresholds(C.F8_LEVELS_MICRO[0])
    assert not v.n_cells_scaled and v.thresholds_scope == "production_cache" and v.production_scope_eligible
    assert not v.qualification_passed and v.protocol_id == "" and v.protocol_sha256 == ""                       # H3: eligible is not passed; unregistered never passes
    assert (v.theta_p_used, v.theta_t_used) == (th.theta_p, th.theta_t) and v.grid == 50 and v.ticks == 1100 and v.n_replicates == 10
    assert v.dkw_bound == math.sqrt(math.log(40.0) / 20.0) and v.union_bound == math.sqrt(math.log(400.0) / 20.0) and v.union_bound > v.dkw_bound
    assert abs(v.empirical_mean_density - 0.0523) < 0.002 and v.s_min_rejection_rate == 0.0 and len(v.per_window_sup_deviation) == 10
    assert abs(v.window_lag1_corr_exact - 0.0245) < 1e-3
    with pytest.raises(N.NullDomainError): N.validate_on_stepper(10, grid=50, ticks=3000)
    with pytest.raises(N.NullDomainError): N.validate_on_stepper(10, ticks=900)
    with pytest.raises(N.NullDomainError): N.validate_on_stepper(5)

def test_m3_validation_record_refuses_the_iid_all_windows_interpretation_and_scope_mismatch():
    """D1: a record claiming the DKW bound at n = 10·replicates (the dependent all-windows sample) is refused; D2: a scaled
    record cannot be relabelled production scope."""
    v = N.validate_on_stepper(10, grid=8, ticks=1100)
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, dkw_bound=math.sqrt(math.log(40.0) / (2 * 100)))
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, dkw_passed=not v.dkw_passed)
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, union_passed=not v.union_passed)
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, union_bound=v.dkw_bound)
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, per_window_sup_deviation=v.per_window_sup_deviation[:9])
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, dkw_p_value=0.5)
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, thresholds_scope="production_cache")
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, n_cells_scaled=False)
    assert v.all_windows_sup_deviation >= 0.0 and v.dkw_sup_deviation >= 0.0

def test_f8_m2_m3_do_not_touch_e1():
    from mfa_instrument.e1 import config as E1, classify as EK
    E1.verify_frozen_identity(); EK.verify_frozen_identity()
    assert EK.CLASSIFY_SHA256_LITERAL == "1f537198ae235de7e20a27c3a52dfed0663311ac6505d1c6895b97e5c197252c"


def test_m3_consecutive_windows_are_dependent_and_the_exact_correlation_is_right():
    """D1 substance: adjacent windows of one trajectory are correlated through their boundary ticks. The exact value is
    checked against brute-force summation at a small window and the chain's known autocorrelation."""
    a, q, pi1 = N.chain_rates(); r = 1 - a - q
    for w in (2, 5, 20):
        v = pi1 * (1 - pi1)
        cov = sum(v * r ** (t - s) for s in range(w) for t in range(w, 2 * w)); var = sum(v * r ** abs(t - s) for s in range(w) for t in range(w))
        assert abs(N.window_lag1_correlation(a, q, pi1, 1, w) - cov / var) < 1e-12
    c100 = N.window_lag1_correlation(a, q, pi1)
    assert 0.02 < c100 < 0.03 and abs(c100 - r / ((1 - r) ** 2) / (100 * (1 + r) / (1 - r) - 2 * r * (1 - r ** 100) / (1 - r) ** 2)) < 2e-3


# ======================= H1/H3: registered protocol and qualification grammar =======================
def test_h3_eligibility_is_never_passage_and_unregistered_records_cannot_claim_it():
    v = N.validate_on_stepper(10)
    assert v.production_scope_eligible and not v.qualification_passed
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, qualification_passed=True)                       # no protocol → cannot pass
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, protocol_sha256="ab" * 32)
    with pytest.raises(N.NullDomainError): dataclasses.replace(v, production_scope_eligible=False)

def test_h1_attempt1_is_retained_and_the_ratified_protocol_is_fixed():
    P = N.VALIDATION_PROTOCOL_ATTEMPT_2
    assert P.ratified_by == "Mike 2026-10-27" and P.attempt == 2 and P.prior_attempts == (N.ATTEMPT_1,) and N.ATTEMPT_1[:3] == (1, 220261026, 400) and "FAILED" in N.ATTEMPT_1[3]
    assert (P.n_replicates, P.replicate_master, P.grid, P.ticks, P.decision_rule) == (1000, 320261027, 50, 1100, "primary_and_auxiliary")
    assert P.replicate_master not in (N.VALIDATION_REPLICATE_MASTER, C.F8_SEED_PANEL_MASTER, C.F8_CALIBRATION_MASTER)
    assert P.joint_false_fail_bound == 0.05 and abs(P.primary_bound() - math.sqrt(math.log(80.0) / 2000.0)) < 1e-15 and abs(P.auxiliary_bound() - math.sqrt(math.log(800.0) / 2000.0)) < 1e-15
    assert P.identity() == N.VALIDATION_PROTOCOL_ATTEMPT_2_SHA256_LITERAL                                          # the registered identity
    draft = dataclasses.replace(P, ratified_by="")
    with pytest.raises(N.NullDomainError): N.validate_on_stepper(P.n_replicates, P.replicate_master, protocol=draft)   # a draft is refused before any run
    with pytest.raises(N.NullDomainError): N.decide_under_protocol(N.validate_on_stepper(10), draft)
    with pytest.raises(N.NullDomainError): N.validate_on_stepper(10, P.replicate_master, protocol=P)                  # n must equal the registration

def test_h1_protocol_invariants_fail_closed():
    P = N.VALIDATION_PROTOCOL_ATTEMPT_2
    for kw in ({"replicate_master": 220261026}, {"replicate_master": C.F8_SEED_PANEL_MASTER}, {"joint_false_fail_bound": 0.025}, {"attempt": 3},
               {"decision_rule": "union_only"}, {"grid": 50, "ticks": 3000}, {"n_replicates": 5}, {"primary_statistic": "pooled_dkw"}):
        with pytest.raises(N.NullDomainError): dataclasses.replace(P, **kw)
    primary_only = dataclasses.replace(P, decision_rule="primary_only", joint_false_fail_bound=0.025)
    assert primary_only.identity() != P.identity()
    ratified = dataclasses.replace(P, ratified_by="test")
    assert ratified.identity() != P.identity()                                                                   # ratification changes the identity

def test_h1_ratified_protocol_decides_and_binds_the_record(monkeypatch):
    """A ratified protocol at a smoke-sized n (test only — the real attempt-2 values are Mike's to ratify) produces a record
    bound to the protocol identity whose qualification_passed equals the stated decision rule, and refuses mismatched runs."""
    P = dataclasses.replace(N.VALIDATION_PROTOCOL_ATTEMPT_2, protocol_id="test_only_stand_in", n_replicates=12, replicate_master=999000111, ratified_by="test-only")
    with pytest.raises(N.NullDomainError):                                                                        # the registered id with altered content is refused
        N.validate_on_stepper(12, 999000111, protocol=dataclasses.replace(P, protocol_id=N.VALIDATION_PROTOCOL_ATTEMPT_2.protocol_id))
    v = N.validate_on_stepper(12, 999000111, protocol=P)
    assert v.protocol_id == P.protocol_id and v.protocol_sha256 == P.identity() and v.production_scope_eligible
    expect = v.dkw_sup_deviation <= P.primary_bound() and all(d <= P.auxiliary_bound() for d in v.per_window_sup_deviation)
    assert v.qualification_passed == expect == N.decide_under_protocol(dataclasses.replace(v, protocol_id="", protocol_sha256="", qualification_passed=False), P)
    with pytest.raises(N.NullDomainError): N.validate_on_stepper(12, 999000112, protocol=P)                      # master differs from the registration
    with pytest.raises(N.NullDomainError): N.validate_on_stepper(13, 999000111, protocol=P)
