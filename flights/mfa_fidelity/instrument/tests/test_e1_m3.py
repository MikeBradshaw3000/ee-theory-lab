"""tests/test_e1_m3.py — E1 stage-1 module M3: the null object (round 2). Frozen declaration bound to
M1/M2 and its live globals; template and constant bypasses closed; the exact law vs its certified
float64 evaluation; typed domains; count-exact MC through M2; the frozen three-level validation with
exact completion; cross-level common random numbers; the public-path memorylessness witness."""
import hashlib
import numpy as np
import pytest

from mfa_instrument.config import DynamicsConstants
from mfa_instrument.e1 import null as N
from mfa_instrument.e1 import classify as K
from mfa_instrument.e1 import config as C


# ---------------- declaration ----------------
def test_null_declaration_frozen_and_bound_to_m1_m2():
    N.verify_frozen_identity()
    assert N._digest(N.NULL_DECLARATION) == N.NULL_DECLARATION_SHA256_LITERAL
    d = dict(N.NULL_DECLARATION)
    assert d["constants"] == C.E1_CONSTANTS_EXPECTED and d["template_sha256"] == N.NULL_TEMPLATE_SHA256_LITERAL and d["law"] == "exact_poisson_binomial" and d["evaluation"] == "float64_fft"

def test_null_declaration_live_drift_and_upstream_failures_refuse(monkeypatch):
    monkeypatch.setattr(N, "NULL_QUANTILE", 0.95)
    with pytest.raises(N.NullDomainError, match="quantile"): N.verify_frozen_identity()
    monkeypatch.undo()
    monkeypatch.setattr(C, "E1_DECLARATION_SHA256_LITERAL", "0" * 64)
    with pytest.raises(C.E1ConfigError): N.null_thresholds(150000)                       # M1 identity failure blocks production
    monkeypatch.undo()
    monkeypatch.setattr(K, "CLASSIFY_SHA256_LITERAL", "0" * 64)
    with pytest.raises(K.ClassifyDomainError): N.null_thresholds(150000)                 # M2 identity failure blocks production

def test_joint_tamper_of_declaration_and_literal_still_refuses(monkeypatch):
    decl = tuple((k, 0.95 if k == "quantile" else v) for k, v in N.NULL_DECLARATION)
    monkeypatch.setattr(N, "NULL_DECLARATION", decl); monkeypatch.setattr(N, "NULL_DECLARATION_SHA256_LITERAL", N._digest(decl))
    with pytest.raises(N.NullDomainError, match="quantile"): N.verify_frozen_identity()  # live global disagrees


# ---------------- template and constants ----------------
def test_template_is_reverified_every_call_and_returned_protected(monkeypatch):
    t = N.rank_template(); assert not t.flags.writeable and hashlib.sha256(t.tobytes()).hexdigest() == N.NULL_TEMPLATE_SHA256_LITERAL
    cache = N._TEMPLATE_CACHE; cache.setflags(write=True); cache[0, 0] = 0.5                 # tamper the cache itself
    with pytest.raises(N.NullDomainError, match="digest"): N.rank_template()
    N._TEMPLATE_CACHE = None                                                                 # restore

@pytest.mark.parametrize("bad", [np.zeros((2500, 2)), np.zeros((2500, 3), np.float32), np.full((2500, 3), 1.0), np.full((2500, 3), np.nan)])
def test_malformed_custom_template_refused(bad):
    with pytest.raises(N.NullDomainError): N.validate_template(bad)

def test_production_api_admits_no_constant_or_template_override():
    import inspect
    assert "k" not in inspect.signature(N.null_p_act).parameters and "template" not in inspect.signature(N.null_p_act).parameters
    assert "k" not in inspect.signature(N.null_thresholds).parameters
    alt = DynamicsConstants(alpha=5.0)
    p_alt = N._p_act_with(150000, alt, N.rank_template()); p_prod = N.null_p_act(150000)
    assert not np.array_equal(p_alt, p_prod)                                                 # the private path differs; production cannot reach it


# ---------------- exact law vs float64 evaluation ----------------
@pytest.mark.parametrize("p,reps", [([0.1, 0.3, 0.55], 1), ([0.1, 0.3, 0.55], 3), ([0.02, 0.05, 0.1, 0.2, 0.5, 0.9], 4)])
def test_fft_matches_brute_force_and_dp(p, reps):
    p = np.array(p)
    pmf, cert = N.poisson_binomial_pmf(p, reps)
    assert np.max(np.abs(N.brute_force_pmf(p, reps) - pmf)) < 1e-12
    assert np.max(np.abs(N.per_tick_count_pmf_dp(p) - N.per_tick_count_pmf(p)[0])) < 1e-15
    assert np.max(np.abs(N.direct_convolution_pmf(p, reps) - pmf)) < 1e-12

def test_certificates_measure_the_float64_evaluation():
    th = N.null_thresholds(150000)
    for c in (th.window_pmf_certificate, th.terminal_pmf_certificate):
        assert c.max_imag_residual < 1e-12 and c.total_negative_mass < 1e-9 and abs(c.raw_normalisation_error) < 1e-9 and c.clip_renorm_correction < 1e-9
    for q in (th.theta_p_certificate, th.theta_t_certificate):
        assert q.certified and q.margin_below > q.error_bound and q.margin_at > q.error_bound and q.cdf_below < 0.99 <= q.cdf_at
    assert th.law == "exact_poisson_binomial" and th.evaluation == "float64_fft" and th.sampling_ci_half_width == 0.0 and th.numerically_certified

def test_uncertified_quantile_is_refused(monkeypatch):
    monkeypatch.setattr(N, "NULL_ERROR_BOUND_FLOOR", 1.0)                                  # a bound no crossing can clear
    decl = tuple((k, 1.0 if k == "error_bound_floor" else v) for k, v in N.NULL_DECLARATION)
    monkeypatch.setattr(N, "NULL_DECLARATION", decl); monkeypatch.setattr(N, "NULL_DECLARATION_SHA256_LITERAL", N._digest(decl))
    with pytest.raises(N.NullDomainError, match="not numerically certified"): N.null_thresholds(150000)

def test_final_cdfs_validated_by_independent_direct_path_with_identical_quantile_indices():
    nm = N.validate_numerics(150000)
    assert nm["tick_max_abs_diff"] <= nm["tick_error_bound"]
    assert nm["fmin_cdf_max_abs_diff"] <= nm["fmin_final_bound"] and nm["fterm_cdf_max_abs_diff"] <= nm["fterm_final_bound"]
    assert nm["theta_p_index_fft"] == nm["theta_p_index_direct"] and nm["theta_t_index_fft"] == nm["theta_t_index_direct"]
    assert nm["direct_discarded_mass_t"] < 1e-20

def test_quantile_certificates_carry_final_cdf_bounds():
    th = N.null_thresholds(150000)
    b_min, b_term = N.final_cdf_bounds(th.window_pmf_certificate, th.terminal_pmf_certificate)
    assert th.theta_p_certificate.error_bound == b_min == N.f_min_derivative_bound() * th.window_pmf_certificate.sum_l1_bound == 10.0 * th.window_pmf_certificate.sum_l1_bound
    assert th.theta_t_certificate.error_bound == b_term == th.terminal_pmf_certificate.sum_l1_bound
    assert th.terminal_pmf_certificate.sum_l1_bound >= 300 * th.terminal_pmf_certificate.tick_l1_bound       # inherited per-tick error propagated

def test_planted_final_cdf_bound_failure_refuses(monkeypatch):
    monkeypatch.setattr(N, "f_min_derivative_bound", lambda: 1e6)                           # a final-CDF bound no crossing can clear
    with pytest.raises(N.NullDomainError, match="not numerically certified"): N.null_thresholds(150000)

def test_derivative_bound_cannot_be_weakened_or_stiffened_by_a_free_constant():
    """There is no independent constant: the multiplier is derived from frozen N_WINDOWS, and a changed
    window count refuses at the identity gate before any certificate is computed."""
    src = open(N.__file__, encoding="utf-8").read()
    assert "F_MIN_DERIVATIVE_BOUND" not in src and N.f_min_derivative_bound() == 10.0

def test_downward_weakened_window_count_is_refused(monkeypatch):
    monkeypatch.setattr(N, "N_WINDOWS", 5)                                                   # would halve the θ_P bound if it were honoured
    with pytest.raises(N.NullDomainError): N.f_min_derivative_bound()
    with pytest.raises(N.NullDomainError): N.null_thresholds(150000)

def test_truncated_direct_path_matches_full_direct_path_on_small_case():
    p = np.array([0.02, 0.05, 0.1, 0.2, 0.5, 0.9])
    full = N.direct_convolution_pmf(p, 4); trunc, disc = N.direct_convolution_pmf_truncated(p, 4, tail_cut=1e-300)
    assert np.max(np.abs(full - trunc)) < 1e-15 and disc == 0.0

def test_validation_acceptance_values_frozen_and_joint_tamper_refused(monkeypatch):
    d = dict(N.VALIDATION_DECLARATION)
    assert d["quantile_allowance"] == 5e-4 and d["exceedance_cap"] == 0.03 and d["quantile_rule"].startswith("abs(mc - exact) <") and d["exceedance_rule"] == "frac <= cap"
    monkeypatch.setattr(N, "VALIDATION_EXCEEDANCE_CAP", 0.5)
    decl = tuple((k, 0.5 if k == "exceedance_cap" else v) for k, v in N.VALIDATION_DECLARATION)
    monkeypatch.setattr(N, "VALIDATION_DECLARATION", decl); monkeypatch.setattr(N, "VALIDATION_SHA256_LITERAL", N._digest(decl))
    with pytest.raises(N.NullDomainError, match="acceptance values"): N.run_validation()   # the hard check still refuses


# ---------------- domains ----------------
@pytest.mark.parametrize("bad", [lambda: N.poisson_binomial_pmf(np.array([0.1]), 2.0), lambda: N.poisson_binomial_pmf(np.array([0.1]), True),
                                 lambda: N.poisson_binomial_pmf(np.array([0.1]), 0), lambda: N.monte_carlo_tail_statistics(150000, 0, 1),
                                 lambda: N.monte_carlo_tail_statistics(150000, 2, 0), lambda: N.simulate_null_rho(150000, -1, 1),
                                 lambda: N.null_p_act(0.5), lambda: N.null_p_act(100000), lambda: N.poisson_binomial_pmf(np.array([1.5]), 2)])
def test_typed_domain_refusals(bad):
    with pytest.raises(N.NullDomainError): bad()


# ---------------- MC bit-consistency with M2 ----------------
def test_mc_statistics_are_m2_tail_stats_on_the_same_series():
    rho = N.simulate_null_rho(150000, 0, N.VALIDATION_REPLICATE_MASTER)
    st = K.tail_stats(rho)
    s_min, s_term = N.monte_carlo_tail_statistics(150000, 1, N.VALIDATION_REPLICATE_MASTER)
    assert s_min[0] == st.s_min and s_term[0] == st.s_term                                  # raw-bit: the MC IS M2's operation
    assert K.recover_counts(rho).dtype == np.int64


# ---------------- validation program ----------------
def test_validation_declaration_frozen_and_exact_completion():
    assert N._digest(N.VALIDATION_DECLARATION) == N.VALIDATION_SHA256_LITERAL and N.VALIDATION_LEVELS_MICRO == (150000, 515217, 850000)
    with pytest.raises(N.NullDomainError, match="declared level set"): N.run_validation(execution_levels=[150000, 850000])
    with pytest.raises(N.NullDomainError, match="declared level set"): N.run_validation(execution_levels=[150000, 515217, 850000, 150000])

def test_three_level_two_statistic_validation_passes():
    v = N.run_validation()
    assert v.passed and len(v.levels) == 3 and all(L["sup_dev_min"] <= L["dkw_bound"] and L["sup_dev_term"] <= L["dkw_bound"] for L in v.levels)

def test_common_random_numbers_across_distinct_levels():
    w = N.common_random_numbers_witness()
    assert w["p_hi_dominates_p_lo"] and w["same_uniforms_across_levels"] and w["drawwise_dominance_hi_over_lo"] and w["counts_hi_first_tick"] > w["counts_lo_first_tick"]

def test_public_path_memorylessness_witness():
    w = N.memorylessness_witness()
    assert w["same_p_act"] and w["same_next_states"] and w["tick0_next"] is False and w["tick1_next"] is True

def test_threshold_ordering_and_level_identity():
    th0, th23 = N.null_thresholds(150000), N.null_thresholds(850000)
    assert th0.theta_p < th0.p_act_mean < th0.theta_t and th0.theta_t < th23.theta_t and th0.level_id == "0.150000"
