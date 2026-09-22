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
    with pytest.raises(C.E1ConfigError): N.reference_thresholds(150000)                       # M1 identity failure blocks production
    monkeypatch.undo()
    monkeypatch.setattr(K, "CLASSIFY_SHA256_LITERAL", "0" * 64)
    with pytest.raises(K.ClassifyDomainError): N.reference_thresholds(150000)                 # M2 identity failure blocks production

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
    th = N.reference_thresholds(150000)
    for c in (th.window_pmf_certificate, th.terminal_pmf_certificate):
        assert c.max_imag_residual < 1e-12 and c.total_negative_mass < 1e-9 and abs(c.raw_normalisation_error) < 1e-9 and c.clip_renorm_correction < 1e-9
    for q in (th.theta_p_certificate, th.theta_t_certificate):
        assert q.certified and q.margin_below > q.error_bound and q.margin_at > q.error_bound and q.cdf_below < 0.99 <= q.cdf_at
    assert th.law == "exact_poisson_binomial" and th.evaluation == "float64_fft" and th.sampling_ci_half_width == 0.0 and th.numerically_certified

def test_uncertified_quantile_is_refused(monkeypatch):
    monkeypatch.setattr(N, "NULL_ERROR_BOUND_FLOOR", 1.0)                                  # a bound no crossing can clear
    decl = tuple((k, 1.0 if k == "error_bound_floor" else v) for k, v in N.NULL_DECLARATION)
    monkeypatch.setattr(N, "NULL_DECLARATION", decl); monkeypatch.setattr(N, "NULL_DECLARATION_SHA256_LITERAL", N._digest(decl))
    # under the amendment a bound no crossing can clear leaves NO support point for the conservative mode either: HALT
    with pytest.raises(N.NullDomainError, match="no support point clears"): N.reference_thresholds(150000)

def test_final_cdfs_validated_by_independent_direct_path_with_identical_quantile_indices():
    nm = N.validate_numerics(150000)
    assert nm["tick_max_abs_diff"] <= nm["tick_error_bound"]
    assert nm["fmin_cdf_max_abs_diff"] <= nm["fmin_final_bound"] and nm["fterm_cdf_max_abs_diff"] <= nm["fterm_final_bound"]
    assert nm["theta_p_index_fft"] == nm["theta_p_index_direct"] and nm["theta_t_index_fft"] == nm["theta_t_index_direct"]
    assert nm["direct_discarded_mass_t"] < 1e-20

def test_quantile_certificates_carry_final_cdf_bounds():
    th = N.reference_thresholds(150000)
    b_min, b_term = N.final_cdf_bounds(th.window_pmf_certificate, th.terminal_pmf_certificate)
    assert th.theta_p_certificate.error_bound == b_min == N.f_min_derivative_bound() * th.window_pmf_certificate.sum_l1_bound == 10.0 * th.window_pmf_certificate.sum_l1_bound
    assert th.theta_t_certificate.error_bound == b_term == th.terminal_pmf_certificate.sum_l1_bound
    assert th.terminal_pmf_certificate.sum_l1_bound >= 300 * th.terminal_pmf_certificate.tick_l1_bound       # inherited per-tick error propagated

def test_planted_final_cdf_bound_failure_refuses(monkeypatch):
    monkeypatch.setattr(N, "f_min_derivative_bound", lambda: 1e6)                           # a final-CDF bound no crossing can clear
    with pytest.raises(N.NullDomainError, match="no support point clears"): N.reference_thresholds(150000)   # conservative mode halts too

def test_derivative_bound_cannot_be_weakened_or_stiffened_by_a_free_constant():
    """There is no independent constant: the multiplier is derived from frozen N_WINDOWS, and a changed
    window count refuses at the identity gate before any certificate is computed."""
    src = open(N.__file__, encoding="utf-8").read()
    assert "F_MIN_DERIVATIVE_BOUND" not in src and N.f_min_derivative_bound() == 10.0

def test_downward_weakened_window_count_is_refused(monkeypatch):
    monkeypatch.setattr(N, "N_WINDOWS", 5)                                                   # would halve the θ_P bound if it were honoured
    with pytest.raises(N.NullDomainError): N.f_min_derivative_bound()
    with pytest.raises(N.NullDomainError): N.reference_thresholds(150000)

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
    th0, th23 = N.reference_thresholds(150000), N.reference_thresholds(850000)
    assert th0.theta_p < th0.p_act_mean < th0.theta_t and th0.theta_t < th23.theta_t and th0.level_id == "0.150000"


# ======================= amendment of record (2026-09-21): conditional per-seed null; conservative coverage mode =======================
from mfa_instrument.e1 import config as _C
from mfa_instrument.init import initialize as _initialize
from mfa_instrument.rng import SeedRegistry as _SeedRegistry


def _prod_bases(m, seed):
    cfg = _C.e1_run_config(m, seed)
    st = _initialize(cfg.init, cfg.grid_scale, _SeedRegistry(seed).dynamics())
    return st.v, st.u_base, st.r

def test_amended_declaration_names_the_primary_scoring_object():
    d = dict(N.NULL_DECLARATION)
    assert d["primary_scoring_object"] == "conditional_per_seed" and "validation" in d["reference_template_use"] and d["template_rng_role"] == 0xE10000
    assert d["quantile_modes"] == ("exact_certified", "conservative_coverage") and N._digest(N.NULL_DECLARATION) == N.NULL_DECLARATION_SHA256_LITERAL

def test_conservative_coverage_mode_at_a_known_ambiguous_level():
    th = N.reference_thresholds(508454); q = th.theta_p_certificate
    assert q.mode == "conservative_coverage" and q.ordinary_certifiable is False and q.ordinary_index == 9980
    assert q.conservative_index == 9981 and q.index == 9981 and q.displacement == 1                 # reported for THIS level, no global claim
    assert q.cdf_at_selected - q.error_bound >= 0.99                                                # true F(k_safe) >= q guaranteed
    assert th.theta_p == float(np.float64(9981) / np.float64(250000)) and th.numerically_certified and "conservative_coverage" in th.threshold_modes

def test_exact_mode_reports_but_does_not_select_k_safe():
    th = N.reference_thresholds(150000); q = th.theta_t_certificate
    assert q.mode == "exact_certified" and q.ordinary_certifiable and q.index == q.ordinary_index and q.conservative_index >= q.ordinary_index

def test_conservative_mode_halts_when_no_support_point_clears(monkeypatch):
    cdf = np.linspace(0.0, 0.99, 1000)                                                              # never reaches q + eps
    with pytest.raises(N.NullDomainError, match="no support point"): N._quantile(cdf, 1000, 1e-6)

def test_conditional_thresholds_are_the_production_object_bound_to_bases_and_seed():
    m = 850000; seed = _C.E1_SEED_PANEL[1]; v, u, r = _prod_bases(m, seed)
    th = N.conditional_thresholds(m, seed, v, u, r)
    assert th.role == "conditional_per_seed" and th.seed == seed and th.bases_sha256 == N.bases_identity(v, u, r) and th.level_id == "0.850000"
    assert th.numerically_certified and th.theta_p < th.p_act_mean < th.theta_t and th.config_hash and th.scoring_identity
    ch = _C.e1_run_config(m, seed).config_hash()
    assert N.require_production_scoring_object(th, m, seed, N.bases_identity(v, u, r), ch) is th
    p = N.conditional_p_act(v, u, r); assert abs(float(np.mean(p)) - th.p_act_mean) == 0.0

def test_reference_object_is_refused_for_production_scoring():
    ref = N.reference_thresholds(850000)
    assert ref.role == "reference_template" and ref.seed is None and ref.bases_sha256 is None and ref.scoring_identity is None
    with pytest.raises(N.NullDomainError, match="conditional per-seed"): N.require_production_scoring_object(ref, 850000, _C.E1_SEED_PANEL[0], "0" * 64, "1" * 64)
    with pytest.raises(N.NullDomainError, match="retired"): N.null_thresholds(150000)                   # the generic alias is retired

def test_finding_1_reproduced_with_the_conditional_object():
    """At the top of the sweep some production seeds' MEAN null activity exceeds the reference θ_T; their
    conditional θ_T sits above their own mean, as a null threshold must."""
    m = 850000; ref = N.reference_thresholds(m); above = 0
    for seed in _C.E1_SEED_PANEL[:4]:
        v, u, r = _prod_bases(m, seed); th = N.conditional_thresholds(m, seed, v, u, r)
        above += th.p_act_mean > ref.theta_t
        assert th.theta_t > th.p_act_mean
    assert above >= 1

def test_conditional_bases_domains_and_identity():
    m = 515217; seed = _C.E1_SEED_PANEL[0]; v, u, r = _prod_bases(m, seed)
    with pytest.raises(N.NullDomainError): N.conditional_thresholds(m, seed, v.astype(np.float32), u, r)
    with pytest.raises(N.NullDomainError): N.conditional_thresholds(m, seed, v.reshape(-1), u, r)      # flattened production bases refused
    with pytest.raises(N.NullDomainError): N.conditional_thresholds(m, True, v, u, r)
    bad = v.copy(); bad.flat[0] = 1.5
    with pytest.raises(N.NullDomainError): N.conditional_thresholds(m, seed, bad, u, r)
    v2 = v.copy(); v2.flat[0] = np.nextafter(v2.flat[0], 1.0)
    assert N.bases_identity(v2, u, r) != N.bases_identity(v, u, r)                                  # one ulp changes the identity


# ======================= reopening round 2: the twelve discriminating negatives (L2 §12) =======================
def test_neg1_duplicate_declaration_field_names_refused(monkeypatch):
    decl = N.NULL_DECLARATION + (("quantile", 0.99),)
    monkeypatch.setattr(N, "NULL_DECLARATION", decl); monkeypatch.setattr(N, "NULL_DECLARATION_SHA256_LITERAL", N._digest(decl))
    with pytest.raises(N.NullDomainError, match="duplicate declaration field"): N.verify_frozen_identity()
    keys = [k for k, _ in N.NULL_DECLARATION[:-1]]; assert len(set(keys)) == len(keys) and "template_rng_role" in keys and "reference_template_use" in keys

def test_neg2_changed_template_rng_role_refused_even_with_cache(monkeypatch):
    N.rank_template()                                                                                   # cache exists
    monkeypatch.setattr(N, "NULL_TEMPLATE_ROLE", 0xE10001)
    decl = tuple((k, 0xE10001 if k == "template_rng_role" else v) for k, v in N.NULL_DECLARATION)
    monkeypatch.setattr(N, "NULL_DECLARATION", decl); monkeypatch.setattr(N, "NULL_DECLARATION_SHA256_LITERAL", N._digest(decl))
    with pytest.raises(N.NullDomainError, match="template RNG role"): N.verify_frozen_identity()
    with pytest.raises(N.NullDomainError): N.reference_thresholds(150000)

def test_neg3_bases_from_right_seed_wrong_level_refused():
    seed = _C.E1_SEED_PANEL[0]; v, u, r = _prod_bases(850000, seed)
    with pytest.raises(N.NullDomainError, match="not the replayed initialization"): N.conditional_thresholds(515217, seed, v, u, r)

def test_neg4_bases_from_right_level_wrong_seed_refused():
    v, u, r = _prod_bases(850000, _C.E1_SEED_PANEL[0])
    with pytest.raises(N.NullDomainError, match="not the replayed initialization"): N.conditional_thresholds(850000, _C.E1_SEED_PANEL[1], v, u, r)

def test_neg5_out_of_panel_and_negative_seed_refused():
    v, u, r = _prod_bases(850000, _C.E1_SEED_PANEL[0])
    for bad in (12345, -1, 0, 2**31):
        with pytest.raises(N.NullDomainError, match="frozen E1 production seeds"): N.conditional_thresholds(850000, bad, v, u, r)

def test_neg6_one_bit_base_mismatch_against_replay_refused():
    seed = _C.E1_SEED_PANEL[0]; v, u, r = _prod_bases(850000, seed)
    for arr, name in ((v, "v"), (u, "u_base"), (r, "r")):
        bad = arr.copy(); bad.flat[1234] = np.nextafter(bad.flat[1234], 0.0)
        args = {"v": v, "u_base": u, "r": r}; args[name] = bad
        with pytest.raises(N.NullDomainError, match=f"{name}: supplied bases"): N.conditional_thresholds(850000, seed, args["v"], args["u_base"], args["r"])

def test_neg7_flattened_or_wrong_shape_production_bases_refused():
    seed = _C.E1_SEED_PANEL[0]; v, u, r = _prod_bases(850000, seed)
    with pytest.raises(N.NullDomainError, match="shape"): N.conditional_thresholds(850000, seed, v.reshape(-1), u, r)
    with pytest.raises(N.NullDomainError, match="shape"): N.conditional_thresholds(850000, seed, v.reshape(25, 100), u, r)
    N.conditional_thresholds_for_analysis(850000, v.reshape(-1), u.reshape(-1), r.reshape(-1))         # analysis path accepts flat, reference role

def test_neg8_guard_refuses_another_runs_valid_conditional_object():
    m = 850000; s0, s1 = _C.E1_SEED_PANEL[0], _C.E1_SEED_PANEL[1]
    v0, u0, r0 = _prod_bases(m, s0); th0 = N.conditional_thresholds(m, s0, v0, u0, r0)
    v1, u1, r1 = _prod_bases(m, s1); ch1 = _C.e1_run_config(m, s1).config_hash()
    with pytest.raises(N.NullDomainError, match="does not belong to the run"): N.require_production_scoring_object(th0, m, s1, N.bases_identity(v1, u1, r1), ch1)
    with pytest.raises(N.NullDomainError, match="does not belong to the run"): N.require_production_scoring_object(th0, 515217, s0, th0.bases_sha256, th0.config_hash)

def test_neg9_fabricated_conditional_role_object_refused():
    import dataclasses
    ref = N.reference_thresholds(150000)
    with pytest.raises(N.NullDomainError):                                                              # __post_init__ refuses inconsistent metadata
        dataclasses.replace(ref, role="conditional_per_seed", seed=_C.E1_SEED_PANEL[0], bases_sha256="ab" * 32, config_hash="cd" * 32, scoring_identity="ef" * 32)
    with pytest.raises(N.NullDomainError): dataclasses.replace(ref, role="mystery")
    with pytest.raises(N.NullDomainError): N.require_production_scoring_object("not an object", 150000, _C.E1_SEED_PANEL[0], "x", "y")

def test_neg10_certificate_mode_inconsistency_refused():
    import dataclasses
    ref = N.reference_thresholds(150000)
    with pytest.raises(N.NullDomainError, match="modes"): dataclasses.replace(ref, threshold_modes=("conservative_coverage", "exact_certified"))
    with pytest.raises(N.NullDomainError, match="certified"): dataclasses.replace(ref, numerically_certified=False)

def test_neg11_no_production_facing_module_scores_with_the_reference_or_alias():
    """Source-level integration check: production-scoring paths must reach only the conditional constructor and the
    context-aware guard. (M6/M7 are amended in their own rounds; this asserts the M3 surface and that the alias is dead.)"""
    src = open(N.__file__, encoding="utf-8").read()
    assert 'raise NullDomainError("null_thresholds is retired' in src
    assert "def require_production_scoring_object(th, expected_level_micro: int, expected_seed: int, expected_bases_sha256: str" in src
    for line in src.splitlines():
        if "PRODUCTION" in line and "template" in line.lower():
            assert "never" in line.lower() or "not production" in line.lower() or "NOT a production" in line, line

def test_neg12_independent_direct_path_validates_the_conservative_mode_case():
    nm = N.validate_numerics(508454)
    assert nm["theta_p_mode_fft"] == "conservative_coverage" == nm["theta_p_mode_direct"]
    assert int(nm["theta_p_ordinary_direct"]) == 9980 and int(nm["theta_p_index_direct"]) == 9981 == int(nm["theta_p_index_fft"])
    assert nm["theta_p_coverage_ok_direct"] and nm["fmin_cdf_max_abs_diff"] <= nm["fmin_final_bound"]
    assert N.CONSERVATIVE_MODE_LEVELS_MICRO == (508454,) and dict(N.VALIDATION_DECLARATION)["conservative_mode_levels_micro"] == (508454,)
    cdf = np.linspace(0.0, 0.99, 1000)
    with pytest.raises(N.NullDomainError, match="direct path: no support point"): N._direct_selection(cdf, 1e-6)


# ======================= reopening round 3: payload identity, semantic invariants, full triangle allowance (L2 r2 §13) =======================
import dataclasses as _dc


def _valid_conditional():
    m = 850000; seed = _C.E1_SEED_PANEL[1]; ch, v, u, r = N._replay_initialization(m, seed)
    return m, seed, ch, v, u, r, N.conditional_thresholds(m, seed, v, u, r)

def test_r3_direct_call_duplicate_declaration_refused_in_derivative_bound(monkeypatch):
    decl = N.NULL_DECLARATION + (("n_windows", 10),)
    monkeypatch.setattr(N, "NULL_DECLARATION", decl)
    with pytest.raises(N.NullDomainError, match="duplicate declaration field"): N.f_min_derivative_bound()
    src = open(N.__file__, encoding="utf-8").read(); assert "dict(NULL_DECLARATION)" not in src and "dict(VALIDATION_DECLARATION)" not in src

def test_r3_altered_theta_values_cannot_be_constructed():
    *_, th = _valid_conditional()
    with pytest.raises(N.NullDomainError, match="theta values"): _dc.replace(th, theta_p=0.0)
    with pytest.raises(N.NullDomainError, match="theta values"): _dc.replace(th, theta_t=th.theta_t + 1e-9)

def test_r3_altered_nested_certificate_with_unchanged_context_refused():
    *_, th = _valid_conditional()
    c = th.theta_t_certificate
    with pytest.raises(N.NullDomainError): _dc.replace(c, index=c.index + 1)                                         # certificate invariants
    with pytest.raises(N.NullDomainError): _dc.replace(c, mode="conservative_coverage")
    with pytest.raises(N.NullDomainError): _dc.replace(c, value=0.0)
    # a certificate rebuilt consistently but DIFFERENT from the one the payload digest was computed on is refused at the object
    alt = N.QuantileCertificate(c.index, c.value, c.cdf_below, c.cdf_at, c.margin_below, c.margin_at, c.error_bound * 2, True, c.mode,
                                c.ordinary_index, c.ordinary_certifiable, c.conservative_index, c.displacement, c.cdf_at_selected, c.denominator)
    with pytest.raises(N.NullDomainError, match="payload identity|error bounds must equal"): _dc.replace(th, theta_t_certificate=alt)   # round 4: geometry refuses first

def test_r3_wrong_level_id_refused():
    *_, th = _valid_conditional()
    with pytest.raises(N.NullDomainError, match="level_id"): _dc.replace(th, level_id="0.850001")

def test_r3_wrong_law_evaluation_or_p_act_mean_refused():
    *_, th = _valid_conditional()
    with pytest.raises(N.NullDomainError, match="law/evaluation"): _dc.replace(th, evaluation="fft32")
    with pytest.raises(N.NullDomainError, match="law/evaluation"): _dc.replace(th, sampling_ci_half_width=0.1)
    with pytest.raises(N.NullDomainError, match="payload identity"): _dc.replace(th, p_act_mean=th.p_act_mean + 1e-6)
    with pytest.raises(N.NullDomainError, match="p_act_mean"): _dc.replace(th, p_act_mean=float("nan"))

def test_r3_scoring_object_version_frozen_and_drift_refused(monkeypatch):
    assert dict(N.NULL_DECLARATION)["scoring_object_version"] == "e1_conditional_null_v1"
    monkeypatch.setattr(N, "SCORING_OBJECT_VERSION", "e1_conditional_null_v2")
    with pytest.raises(N.NullDomainError, match="scoring_object_version|scoring object version"): N.verify_frozen_identity()
    m, seed = 850000, _C.E1_SEED_PANEL[1]; ch, v, u, r = N._replay_initialization(m, seed)
    with pytest.raises(N.NullDomainError, match="scoring_object_version|scoring object version"): N.conditional_thresholds(m, seed, v, u, r)   # production blocked under drift

def test_r3_production_guard_reruns_frozen_identity(monkeypatch):
    m, seed, ch, v, u, r, th = _valid_conditional()
    monkeypatch.setattr(N, "NULL_DECLARATION_SHA256_LITERAL", "0" * 64)
    with pytest.raises(N.NullDomainError, match="digest"): N.require_production_scoring_object(th, m, seed, N.bases_identity(v, u, r), ch)

def test_r3_guard_inputs_are_typed_and_noncoercive():
    m, seed, ch, v, u, r, th = _valid_conditional()
    b = N.bases_identity(v, u, r)
    with pytest.raises(N.NullDomainError): N.require_production_scoring_object(th, 850000.0, seed, b, ch)
    with pytest.raises(N.NullDomainError): N.require_production_scoring_object(th, m, float(seed), b, ch)
    with pytest.raises(N.NullDomainError): N.require_production_scoring_object(th, m, True, b, ch)
    with pytest.raises(N.NullDomainError, match="64-hex"): N.require_production_scoring_object(th, m, seed, b[:-1], ch)
    with pytest.raises(N.NullDomainError, match="64-hex"): N.require_production_scoring_object(th, m, seed, b, ch.upper())

def test_r3_analysis_object_carries_distinct_nonproduction_role():
    m, seed, ch, v, u, r, _ = _valid_conditional()
    a = N.conditional_thresholds_for_analysis(m, v.reshape(-1), u.reshape(-1), r.reshape(-1))
    assert a.role == "analysis_bases" and a.seed is None and a.bases_sha256 is None and a.scoring_identity is None
    assert N.reference_thresholds(150000).role == "reference_template"                                                # distinguishable by role
    with pytest.raises(N.NullDomainError, match="conditional per-seed"): N.require_production_scoring_object(a, m, seed, N.bases_identity(v, u, r), ch)

def test_r3_direct_path_uses_full_triangle_allowance_and_ordinary_indices_agree():
    nm = N.validate_numerics(508454)
    assert nm["direct_allowance_p"] >= nm["fmin_final_bound"] + nm["direct_discarded_mass_w"]                  # includes the measured CDF discrepancy
    assert nm["direct_allowance_p"] > nm["fmin_final_bound"] + nm["direct_discarded_mass_w"] or nm["fmin_cdf_max_abs_diff"] - nm["direct_discarded_mass_w"] == 0.0
    assert nm["theta_p_ordinary_fft"] == nm["theta_p_ordinary_direct"] == 9980.0 and nm["theta_t_ordinary_fft"] == nm["theta_t_ordinary_direct"]
    assert nm["theta_p_index_fft"] == nm["theta_p_index_direct"] == 9981.0 and nm["theta_p_mode_direct"] == "conservative_coverage"
    src = open(N.__file__, encoding="utf-8").read()
    assert 'n["theta_p_ordinary_fft"] == n["theta_p_ordinary_direct"]' in src and 'c["theta_p_ordinary_fft"] == c["theta_p_ordinary_direct"]' in src


# ======================= reopening round 4: computed certifiability, geometry binding, declared triangle rule (L2 r3 §14) =======================
def _probe_digest(th, **overrides):
    probe = object.__new__(N.NullThresholds)
    for k, val in th.__dict__.items(): object.__setattr__(probe, k, val)
    for k, val in overrides.items(): object.__setattr__(probe, k, val)
    return N.threshold_payload_identity(probe)

def test_r4_false_conservative_certificate_refused():
    """Both ordinary margins exceed ε but the Boolean claims uncertifiable: the COMPUTED margin test refuses."""
    q = 0.99; below, at = 0.989, 0.991
    with pytest.raises(N.NullDomainError, match="computed margin test"):
        N.QuantileCertificate(1000, float(np.float64(1000) / np.float64(1000000)), below, at, q - below, at - q, 0.0001, True,
                              "conservative_coverage", 999, False, 1000, 1, 0.992, 1000000)
    with pytest.raises(N.NullDomainError, match="computed margin test"):                                  # the mirror: exact mode claiming certifiable with tiny margins
        N.QuantileCertificate(999, float(np.float64(999) / np.float64(1000000)), below, at, q - below, at - q, 0.5, True,
                              "exact_certified", 999, True, 1000, 1, at, 1000000)
    with pytest.raises(N.NullDomainError, match="straddle"):                                              # ordinary crossing must straddle q
        N.QuantileCertificate(999, float(np.float64(999) / np.float64(1000000)), 0.991, 0.992, q - 0.991, 0.992 - q, 0.0001, True,
                              "exact_certified", 999, True, 1000, 1, 0.992, 1000000)

def test_r4_wrong_grid_and_geometry_refused_even_with_recomputed_payload():
    *_, th = _valid_conditional()
    c = th.theta_p_certificate; den = 1000000
    wrong = N.QuantileCertificate(c.index, float(np.float64(c.index) / np.float64(den)), c.cdf_below, c.cdf_at, c.margin_below, c.margin_at,
                                  c.error_bound, True, c.mode, c.ordinary_index, c.ordinary_certifiable, c.conservative_index, c.displacement, c.cdf_at_selected, den)
    with pytest.raises(N.NullDomainError, match="denominators"):
        _dc.replace(th, theta_p_certificate=wrong, theta_p=wrong.value, payload_sha256=_probe_digest(th, theta_p_certificate=wrong, theta_p=wrong.value))
    with pytest.raises(N.NullDomainError, match="reps/support|multiple of reps"):
        _dc.replace(th.window_pmf_certificate, reps=99)                                                    # round 6: the certificate refuses on its own
    tb = _dc.replace(th.terminal_pmf_certificate, support=750000 + 300)                                    # still a multiple of reps: geometry refuses
    with pytest.raises(N.NullDomainError, match="reps/support"):
        _dc.replace(th, terminal_pmf_certificate=tb, payload_sha256=_probe_digest(th, terminal_pmf_certificate=tb))
    # certificate error bound must EQUAL final_cdf_bounds of the carried PMF certificates
    loose = _dc.replace(c, error_bound=c.error_bound * 0.5, ordinary_certifiable=(c.margin_below > c.error_bound * 0.5 and c.margin_at > c.error_bound * 0.5))
    with pytest.raises(N.NullDomainError, match="error bounds must equal"):
        _dc.replace(th, theta_p_certificate=loose, payload_sha256=_probe_digest(th, theta_p_certificate=loose))

def test_r4_guard_reruns_the_complete_semantic_validator(monkeypatch):
    m, seed, ch, v, u, r, th = _valid_conditional()
    # a post-construction mutation that bypasses __post_init__ entirely (object.__setattr__) and recomputes the digest:
    object.__setattr__(th.window_pmf_certificate, "reps", 99)                                              # bypass the certificate's own construction too
    object.__setattr__(th, "payload_sha256", N.threshold_payload_identity(th))
    with pytest.raises(N.NullDomainError, match="reps/support|multiple of reps"): N.require_production_scoring_object(th, m, seed, N.bases_identity(v, u, r), ch)

def test_r4_declared_direct_allowance_rule_is_the_full_triangle_and_joint_tamper_refused(monkeypatch):
    rule = dict(N.VALIDATION_DECLARATION)["conservative_mode_rule"]
    assert "max absolute FFT/direct CDF discrepancy" in rule and rule == N.DIRECT_ALLOWANCE_RULE
    stale = "direct path re-selects under allowance = final bound + discarded mass; modes and selected indices agree; coverage condition holds; ordinary index agrees"
    decl = tuple((k, stale if k == "conservative_mode_rule" else val) for k, val in N.VALIDATION_DECLARATION)
    monkeypatch.setattr(N, "VALIDATION_DECLARATION", decl); monkeypatch.setattr(N, "VALIDATION_SHA256_LITERAL", N._digest(decl))
    with pytest.raises(N.NullDomainError, match="full triangle"): N.run_validation()
    monkeypatch.setattr(N, "DIRECT_ALLOWANCE_RULE", stale)                                                  # even jointly with the live rule text
    with pytest.raises(N.NullDomainError, match="full triangle"): N.run_validation()


# ======================= reopening round 5: nested certificate re-validation; exact rule identity (L2 r4 §11) =======================
def test_r5_nested_certificate_bypass_refused_at_the_guard():
    """L2's concrete bypass: flip a nested certificate's Boolean with object.__setattr__ (bypassing its
    construction), recompute the PARENT payload digest — parent fields stay mutually consistent — and
    require the guard to refuse on the nested semantic inconsistency."""
    m, seed, ch, v, u, r, th = _valid_conditional()
    q = th.theta_p_certificate
    object.__setattr__(q, "ordinary_certifiable", not q.ordinary_certifiable)
    object.__setattr__(th, "payload_sha256", N.threshold_payload_identity(th))
    with pytest.raises(N.NullDomainError, match="computed margin test"): N.require_production_scoring_object(th, m, seed, N.bases_identity(v, u, r), ch)
    # nested crossing/mode fields the same way
    m, seed, ch, v, u, r, th = _valid_conditional(); q = th.theta_t_certificate
    object.__setattr__(q, "mode", "conservative_coverage"); object.__setattr__(th, "threshold_modes", (th.theta_p_certificate.mode, "conservative_coverage"))
    object.__setattr__(th, "payload_sha256", N.threshold_payload_identity(th))
    with pytest.raises(N.NullDomainError): N.require_production_scoring_object(th, m, seed, N.bases_identity(v, u, r), ch)
    # a foreign-typed certificate substituted in place is refused by exact type
    m, seed, ch, v, u, r, th = _valid_conditional()
    class Impostor:                                                                                  # duck-typed lookalike
        def __init__(self, c): self.__dict__.update(c.__dict__)
    object.__setattr__(th, "theta_t_certificate", Impostor(th.theta_t_certificate)); object.__setattr__(th, "payload_sha256", N.threshold_payload_identity(th))
    with pytest.raises(N.NullDomainError): N.require_production_scoring_object(th, m, seed, N.bases_identity(v, u, r), ch)

def test_r5_phrase_preserving_false_rule_joint_tamper_refused(monkeypatch):
    """A semantically false rule that KEEPS the discrepancy phrase, installed jointly in the live rule and the
    declaration with a re-established declaration digest: the independent exact identity refuses."""
    false = "direct allowance = max absolute FFT/direct CDF discrepancy only; ordinary index, selected index, mode, and coverage condition must agree"
    decl = tuple((k, false if k == "conservative_mode_rule" else val) for k, val in N.VALIDATION_DECLARATION)
    monkeypatch.setattr(N, "DIRECT_ALLOWANCE_RULE", false)
    monkeypatch.setattr(N, "VALIDATION_DECLARATION", decl); monkeypatch.setattr(N, "VALIDATION_SHA256_LITERAL", N._digest(decl))
    with pytest.raises(N.NullDomainError, match="independent exact identity"): N.run_validation()
    # and a rule whose exact identity is also re-established but whose TERMS are altered
    monkeypatch.setattr(N, "DIRECT_ALLOWANCE_RULE_SHA256_LITERAL", __import__("hashlib").sha256(false.encode()).hexdigest())
    with pytest.raises(N.NullDomainError, match="terms differ"): N.run_validation()
    assert N.DIRECT_ALLOWANCE_TERMS == ("primary final-CDF bound", "max absolute FFT/direct CDF discrepancy", "discarded mass")


# ======================= reopening round 6: PMF certificate semantics; carried per-tick bound (L2 r5 §6) =======================
def test_r6_pmf_certificate_validator_and_carried_tick_certificate():
    *_, th = _valid_conditional()
    tk = th.tick_pmf_certificate
    assert tk is not None and tk.reps == 1 and tk.support == N.N_CELLS and tk.tick_l1_bound == tk.sum_l1_bound
    assert th.window_pmf_certificate.tick_l1_bound == tk.sum_l1_bound == th.terminal_pmf_certificate.tick_l1_bound
    w = th.window_pmf_certificate
    assert w.sum_l1_bound == w.reps * w.tick_l1_bound + N._own_bound(w.max_imag_residual, w.total_negative_mass, w.raw_normalisation_error, w.clip_renorm_correction)
    with pytest.raises(N.NullDomainError, match="sum == reps x tick"): _dc.replace(w, sum_l1_bound=w.sum_l1_bound * 0.5)
    with pytest.raises(N.NullDomainError, match="own recomputed"): _dc.replace(tk, sum_l1_bound=tk.sum_l1_bound * 0.5)
    with pytest.raises(N.NullDomainError): _dc.replace(w, reps=True)
    with pytest.raises(N.NullDomainError): _dc.replace(w, max_imag_residual=-1e-9)
    with pytest.raises(N.NullDomainError): _dc.replace(w, sum_l1_bound=float("inf"))

def test_r6_neg1_understated_sum_bound_with_consistent_quantile_and_recomputed_payload_refused():
    m, seed, ch, v, u, r, th = _valid_conditional()
    w = th.window_pmf_certificate; q = th.theta_p_certificate
    object.__setattr__(w, "sum_l1_bound", w.sum_l1_bound * 0.5)
    b_min, _ = N.final_cdf_bounds(w, th.terminal_pmf_certificate)
    object.__setattr__(q, "error_bound", b_min); object.__setattr__(q, "ordinary_certifiable", bool(q.margin_below > b_min and q.margin_at > b_min))
    object.__setattr__(th, "payload_sha256", N.threshold_payload_identity(th))
    with pytest.raises(N.NullDomainError, match="sum == reps x tick"): N.require_production_scoring_object(th, m, seed, N.bases_identity(v, u, r), ch)

def test_r6_neg2_consistently_lowered_inherited_tick_bound_refused():
    """Lower tick_l1_bound in BOTH window and terminal certificates, keep each sum identity consistent by lowering
    the sums too, lower both quantile bounds consistently, recompute the payload: the carried per-tick
    certificate's identity refuses."""
    m, seed, ch, v, u, r, th = _valid_conditional()
    for pc in (th.window_pmf_certificate, th.terminal_pmf_certificate):
        own = N._own_bound(pc.max_imag_residual, pc.total_negative_mass, pc.raw_normalisation_error, pc.clip_renorm_correction)
        new_tick = pc.tick_l1_bound * 0.5
        object.__setattr__(pc, "tick_l1_bound", new_tick); object.__setattr__(pc, "sum_l1_bound", pc.reps * new_tick + own)
    b_min, b_term = N.final_cdf_bounds(th.window_pmf_certificate, th.terminal_pmf_certificate)
    for q, b in ((th.theta_p_certificate, b_min), (th.theta_t_certificate, b_term)):
        object.__setattr__(q, "error_bound", b); object.__setattr__(q, "ordinary_certifiable", bool(q.margin_below > b and q.margin_at > b))
    object.__setattr__(th, "payload_sha256", N.threshold_payload_identity(th))
    with pytest.raises(N.NullDomainError, match="inherit the carried per-tick"): N.require_production_scoring_object(th, m, seed, N.bases_identity(v, u, r), ch)

def test_r6_neg3_duck_typed_pmf_certificate_refused():
    m, seed, ch, v, u, r, th = _valid_conditional()
    class Impostor:
        def __init__(self, c): self.__dict__.update(c.__dict__)
    object.__setattr__(th, "window_pmf_certificate", Impostor(th.window_pmf_certificate)); object.__setattr__(th, "payload_sha256", N.threshold_payload_identity(th))
    with pytest.raises(N.NullDomainError, match="exact PmfCertificate"): N.require_production_scoring_object(th, m, seed, N.bases_identity(v, u, r), ch)

def test_r6_neg4_conservative_witness_cannot_be_flipped_to_exact_by_understating_eps():
    """On the declared witness 0.508454 (reference path carries the same certificate structure): lower ε enough
    that the ordinary crossing 9980 would certify, rebuild every affected field consistently (mode, index, value,
    displacement, cdf_at_selected, parent theta and modes), recompute the payload — refused before scoring."""
    th = N.reference_thresholds(508454); q = th.theta_p_certificate
    assert q.mode == "conservative_coverage" and q.index == 9981
    w = th.window_pmf_certificate; tiny = q.margin_at * 0.5                      # an ε under which 9980 would certify
    own = N._own_bound(w.max_imag_residual, w.total_negative_mass, w.raw_normalisation_error, w.clip_renorm_correction)
    fake_sum = tiny / N.f_min_derivative_bound()
    object.__setattr__(w, "sum_l1_bound", fake_sum); object.__setattr__(w, "tick_l1_bound", (fake_sum - own) / w.reps)
    b_min, _ = N.final_cdf_bounds(w, th.terminal_pmf_certificate)
    for k, val in (("error_bound", b_min), ("ordinary_certifiable", True), ("mode", "exact_certified"), ("index", 9980),
                   ("value", float(np.float64(9980) / np.float64(q.denominator))), ("displacement", q.conservative_index - 9980), ("cdf_at_selected", q.cdf_at)):
        object.__setattr__(q, k, val)
    object.__setattr__(th, "theta_p", q.value); object.__setattr__(th, "threshold_modes", ("exact_certified", th.theta_t_certificate.mode))
    object.__setattr__(th, "payload_sha256", N.threshold_payload_identity(th))
    with pytest.raises(N.NullDomainError): N.validate_null_thresholds(th)                                # refused on the PMF/tick identities
    assert N.reference_thresholds(508454).theta_p_certificate.index == 9981                               # the real object is unchanged
