"""tests/test_f8_mp1.py — Flight 8 module M-P1: each of the four tests follows §4.11 case by case on constructed sweeps
(boundary cases i–iv, the evaluability rule's disregard/ND branches with the census band, f_J continuity as ND only — on
EVERY positive increase, whatever the sign of the endpoint range (L2 r1 D2) — Δm's strict bracket, extinction as a valid
failure, apparatus halts as ND with their key); the P1 determination's precedence; the frozen closure publication enforced
by replay and no Δm override at the entry point (D1); canonical sweep provenance from M1 results with the observation
recomputed from the persisted trace, density-record identities carried, truncated/stale/tampered records refused (D3),
mid-tail extinction accepted as M1 defines it (D4); the fidelity tier's arithmetic with signed residuals, the actual ratio
reference and the component widths (D7); the steep control's declared first rise (D5); qualification bound to the declared
synthetic census and the cross-trigger counter exercised on its real path (D6); nothing in e1 touched."""
import dataclasses
import math
import numpy as np
import pytest

from mfa_instrument.f8 import config as C
from mfa_instrument.f8 import closure as CL
from mfa_instrument.f8 import dynamics as D
from mfa_instrument.f8 import evaluator as E

L = C.F8_LEVELS_MICRO
MS = [CL.level_m(u) for u in L]


@pytest.fixture(scope="module")
def census():
    return E.synthetic_census()


@pytest.fixture(scope="module")
def pub():
    return CL.closure_publication()


def mk(obj, meds, survs=None, role="synthetic", unevaluable=None):
    """A sweep with exactly `meds` as the per-level medians (20 identical seeds), survivals = first survs[i] seeds."""
    levels = []
    for i, u in enumerate(L):
        if unevaluable and i in unevaluable:
            levels.append(E.LevelData(u, (), (), True, unevaluable[i], (), ())); continue
        sv = [k < (survs[i] if survs is not None else 20) for k in range(20)]
        vals = [meds[i] if sv[k] or not obj.startswith("skeleton") else 0.0 for k in range(20)]
        levels.append(E.LevelData(u, tuple(sv), tuple(float(v) for v in vals), False, "", (), ()))
    rec = E.SweepRecord(obj, role, tuple(levels), E.EVALUATOR_SHA256_LITERAL)
    return dataclasses.replace(rec, result_sha256=rec.identity())


def branch(kind, mc=1.0): return E._branch(mc, kind)
def survs(mc): return [20 if m > mc else 0 for m in MS]
def reseal(sweep, levels): s = dataclasses.replace(sweep, levels=tuple(levels)); return dataclasses.replace(s, result_sha256=s.identity())


def forced_result(spec, counts):
    """An M1-shaped F8RunResult whose trace is `counts` and whose cached summary fields are M1's own arithmetic over it
    (the summary code of dynamics.run, applied to a forced trajectory — an integration fixture, not a lattice experiment)."""
    T, n = spec.ticks, spec.n_cells
    counts = np.asarray(counts, dtype=np.int64); assert counts.shape == (T + 1,)
    rho = counts.astype(np.float64) / np.float64(n)
    tail_counts = counts[T - spec.tail_ticks + 1:]; nwin = spec.tail_ticks // spec.window
    wins = tuple(float(np.float64(int(tail_counts[i * spec.window:(i + 1) * spec.window].sum())) / np.float64(spec.window * n)) for i in range(nwin))
    survival = all(int(tail_counts[i * spec.window:(i + 1) * spec.window].min()) > 0 for i in range(nwin))
    zeros = np.flatnonzero(counts == 0); ext = int(zeros[0]) if (spec.eta_floor == 0.0 and zeros.size) else None
    return D.F8RunResult(spec.spec_hash(), spec.level_micro, spec.level_id, spec.seed, spec.obj, rho, counts, ext, T, wins, bool(survival),
                         float(np.float64(int(tail_counts.sum())) / np.float64(spec.tail_ticks * n)), spec.stream_key, T)


def full_level(u, obj="skeleton_high", counts_fn=None):
    out = []
    for sd in C.F8_SEED_PANEL:
        spec = C.f8_run_spec(u, sd, obj)
        counts = np.full(spec.ticks + 1, spec.n_cells, dtype=np.int64) if counts_fn is None else counts_fn(spec)
        out.append(forced_result(spec, counts))
    return out


# ======================= identity =======================
def test_frozen_identity_and_ratified_values():
    E.verify_frozen_identity()
    assert (E.SURV_THRESHOLD, E.F_J, E.K_R, E.KNOWN_ANSWER_MC, E.KNOWN_ANSWER_SWEEPS, E.KNOWN_ANSWER_PASS_MIN) == (18, 0.25, 3, (0.8, 1.0, 1.25), 100, 95)
    assert dict(E.EVALUATOR_DECLARATION)["ratio_uncertainty_convention"] == E.RATIO_UNCERTAINTY_CONVENTION

@pytest.mark.parametrize("name,bad", [("EVALUATOR_SHA256_LITERAL", "0" * 64), ("SURV_THRESHOLD", 17), ("F_J", 0.3), ("KNOWN_ANSWER_PASS_MIN", 90), ("RATIO_UNCERTAINTY_CONVENTION", "propagated band")])
def test_tamper_is_caught(monkeypatch, name, bad):
    monkeypatch.setattr(E, name, bad)
    with pytest.raises(E.EvaluatorDomainError): E.verify_frozen_identity()


# ======================= T-S1' (cases i–iv) =======================
def test_t_s1_prime_cases():
    sk = branch("skeleton")
    r, c = E.t_s1_prime(mk("skeleton_high", sk, survs(1.0)))
    assert r.outcome == "PASS" and L[c] == 1032609 and dict(r.detail)["m_hat_c"] == "1.032609"           # lowest level with surv ≥ 18 and all above
    r, c = E.t_s1_prime(mk("skeleton_high", [0.0] * 24, [0] * 24))
    assert (r.outcome, r.cause, c) == ("FAIL", "no active phase in sweep", None)                         # (i)
    r, c = E.t_s1_prime(mk("skeleton_high", [0.3] * 24, [20] * 24))
    assert (r.outcome, r.cause, c) == ("FAIL", "no inactive phase in sweep", None)                       # (ii)
    sv = survs(1.0); sv[15] = 10
    r, c = E.t_s1_prime(mk("skeleton_high", sk, sv))
    assert (r.outcome, r.cause, c) == ("ND", "non-monotone survival", None)                              # (iii): ≥18 somewhere, a dip above
    sv2 = survs(1.0); sv2[3] = 19                                                                        # an isolated surviving level BELOW the boundary
    r, c = E.t_s1_prime(mk("skeleton_high", sk, sv2))
    assert (r.outcome, r.cause) == ("ND", "non-monotone survival")                                       # also (iii): survival not monotone
    sv3 = survs(1.0); sv3[8] = 18; sv3[9] = 17                                                           # threshold is exactly 18 (not 17)
    r, c = E.t_s1_prime(mk("skeleton_high", sk, sv3))
    assert r.outcome == "ND"
    sv4 = survs(1.0); sv4[8] = 17
    r, c = E.t_s1_prime(mk("skeleton_high", sk, sv4))
    assert r.outcome == "PASS" and L[c] == L[9]                                                          # boundary moves up one level
    r, c = E.t_s1_prime(mk("skeleton_high", sk, survs(1.0), unevaluable={12: "HALT-apparatus-xyz"}))
    assert r.outcome == "ND" and r.cause == "apparatus (HALT-apparatus-xyz)"


# ======================= evaluability rule, T-S1c, T-R1' =======================
def test_evaluability_rule_disregards_within_band_and_flags_beyond(census):
    sk = branch("skeleton"); b = E.band(census, "skeleton_high", 15, 16)
    assert abs(b - 3 * math.sqrt(2) * 0.01 * 1.2533 / math.sqrt(20)) < 1e-12
    within = list(sk); within[16] = within[15] - 0.9 * b
    assert E.t_s1c(mk("skeleton_high", within, survs(1.0)), census, 8).outcome == "PASS"                 # reversal ≤ band: disregarded
    beyond = list(sk); beyond[16] = beyond[15] - 1.1 * b
    r = E.t_s1c(mk("skeleton_high", beyond, survs(1.0)), census, 8)
    assert r.outcome == "ND" and r.cause.startswith("non-monotone at finite sample (") and "1.717391" in r.cause and "1.815217" in r.cause
    # the realization uses ITS object's band (same synthetic ŝ here, but the call path is the realization's)
    re_ = branch("realization"); rb = E.band(census, "realization", 10, 11)
    beyond_r = list(re_); beyond_r[11] = beyond_r[10] - 1.1 * rb
    r = E.t_r1_prime(mk("realization", beyond_r), census)
    assert r.outcome == "ND" and r.cause.startswith("non-monotone at finite sample")
    with pytest.raises(CL.ClosureDomainError): E.band(census, "null", 0, 1)

def test_t_s1c_continuity_is_nd_never_a_valid_failure(census):
    sk = branch("skeleton"); c = 8
    rng = sk[-1] - sk[c]; steep = list(sk)
    steep[c + 1] = sk[c] + 0.3 * rng                                                                     # one increase > f_J·range
    for i in range(c + 2, 24): steep[i] = max(steep[i], steep[c + 1])
    r = E.t_s1c(mk("skeleton_high", steep, survs(1.0)), census, c)
    assert r.outcome == "ND" and r.cause == f"continuity unresolved at grid resolution ({C.level_id(L[c + 1])})"
    assert E.t_s1c(mk("skeleton_high", sk, survs(1.0)), census, c).outcome == "PASS"                     # the map's branch is continuity-compatible
    assert all(r.outcome != "FAIL" for r in [E.t_s1c(mk("skeleton_high", steep, survs(1.0)), census, c)])
    # domain starts at m̂_c: an ACTUAL steep rise below the boundary (survival stays 0 there) is not in T-S1c's domain (L2 r1 §6.3)
    # (the sweep keeps 20 survivors at every level so the rise is really present in the medians — `mk` zeroes non-survivors)
    low_steep = [max(x, 0.2) if i >= 3 else 0.0 for i, x in enumerate(sk)]                                # a 0.2 step at 2→3, plateau, then the branch
    assert low_steep[3] - low_steep[2] > E.F_J * sk[-1] and mk("skeleton_high", low_steep, [20] * 24).levels[3].med == 0.2
    assert E.t_s1c(mk("skeleton_high", low_steep, [20] * 24), census, c).outcome == "PASS"
    r = E.t_s1c(mk("skeleton_high", low_steep, [20] * 24), census, 2)                                       # the same rise inside the domain is caught
    assert (r.outcome, r.cause) == ("ND", f"continuity unresolved at grid resolution ({C.level_id(L[3])})")

def test_continuity_is_checked_on_every_increase_whatever_the_endpoint_range(census):
    """L2 r1 D2: an interior bump followed by a within-band return gives a zero (or negative) endpoint range; the increase is
    an excess over f_J × range and must give the continuity ND in both domains, never a scientific FAIL."""
    c = 8; b = E.band(census, "skeleton_high", 12, 13)
    flat = [0.0] * c + [0.300] * (24 - c); flat[12] = 0.305                                               # +0.005 then −0.005 (< band 0.0119); range 0.0
    assert 0.005 < b
    r = E.t_s1c(mk("skeleton_high", flat, survs(1.0)), census, c)
    assert (r.outcome, r.cause) == ("ND", f"continuity unresolved at grid resolution ({C.level_id(L[12])})")
    neg = list(flat); neg[-1] = 0.299                                                                     # endpoint range −0.001
    r = E.t_s1c(mk("skeleton_high", neg, survs(1.0)), census, c)
    assert r.outcome == "ND" and r.cause.startswith("continuity unresolved")
    rflat = [0.300] * 24; rflat[12] = 0.305                                                               # realization domain, range 0.0
    r = E.t_r1_prime(mk("realization", rflat), census)
    assert r.outcome == "ND" and r.cause.startswith("continuity unresolved")
    assert E.t_r1_prime(mk("realization", [0.300] * 24), census).outcome == "PASS"                        # constant profile: no increase, passes
    dec = [0.300 - 0.0004 * i for i in range(24)]                                                         # only within-band decreases: passes
    assert E.t_r1_prime(mk("realization", dec), census).outcome == "PASS"
    # full propagation: with a located boundary and no other finding the determination is NOT DISTINGUISHED, not NOT PRODUCED
    hi = mk("skeleton_high", flat, survs(1.0)); lo = mk("skeleton_low", flat, survs(1.0)); re_ = mk("realization", [0.3] * 24)
    ev = E.evaluate_p1(hi, lo, re_, census)
    assert ev.determination == "NOT DISTINGUISHED" and ev.cause.startswith("continuity unresolved") and [t.outcome for t in ev.tests] == ["PASS", "ND", "PASS", "PASS"]

def test_t_r1_prime_extinction_positivity_and_order(census):
    re_ = branch("realization")
    assert E.t_r1_prime(mk("realization", re_), census).outcome == "PASS"
    ext = list(re_); ext[5] = 0.0
    r = E.t_r1_prime(mk("realization", ext), census)
    assert (r.outcome, r.cause) == ("FAIL", f"realization extinct at {C.level_id(L[5])}")
    r = E.t_r1_prime(mk("realization", re_, unevaluable={0: "HALT-k"}), census)
    assert r.outcome == "ND" and r.cause == "apparatus (HALT-k)"
    rng = re_[-1] - re_[0]; steep = list(re_); steep[10] = re_[9] + 0.3 * rng
    for i in range(11, 24): steep[i] = max(steep[i], steep[10])
    r = E.t_r1_prime(mk("realization", steep), census)
    assert r.outcome == "ND" and r.cause.startswith("continuity unresolved at grid resolution")


# ======================= T-S2 =======================
def test_t_s2_bracket_is_delta_m_inclusive(pub):
    dm = pub.delta_m.value; sk = branch("skeleton"); c = 8
    assert E.t_s2(mk("skeleton_low", sk, survs(1.0)), c, dm).outcome == "PASS"                             # same boundary
    assert E.t_s2(mk("skeleton_low", sk, survs(1.1)), c, dm).outcome == "PASS"                             # one level up: 0.0978 ≤ 0.1201
    r = E.t_s2(mk("skeleton_low", sk, survs(1.2)), c, dm)
    assert (r.outcome, r.cause) == ("FAIL", "hysteresis") and dict(r.detail)["separation"] > dm            # two levels up: 0.1957 > 0.1201
    r = E.t_s2(mk("skeleton_low", sk, survs(0.9)), c, dm)
    assert r.outcome == "PASS"                                                                              # low boundary BELOW the high one by one level: |sep| ≤ Δm
    r = E.t_s2(mk("skeleton_low", [0.0] * 24, [0] * 24), c, dm)
    assert (r.outcome, r.cause) == ("FAIL", "no active phase in sweep")
    r = E.t_s2(mk("skeleton_low", sk, survs(1.0), unevaluable={20: "HALT-z"}), c, dm)
    assert r.outcome == "ND" and "apparatus" in r.cause
    assert E.t_s2(mk("skeleton_low", sk, survs(1.0)), c, 0.05).outcome == "PASS" and E.t_s2(mk("skeleton_low", sk, survs(1.1)), c, 0.05).outcome == "FAIL"   # Δm is the operative bracket


# ======================= D1: the frozen publication and Δm are enforced at the entry point =======================
def test_evaluate_p1_enforces_the_frozen_closure_publication_and_has_no_delta_m_override(census, pub):
    sk = branch("skeleton"); re_ = branch("realization")
    hi = mk("skeleton_high", sk, survs(1.0)); lo2 = mk("skeleton_low", sk, survs(1.2)); lo1 = mk("skeleton_low", sk, survs(1.1)); rr = mk("realization", re_)
    ev = E.evaluate_p1(hi, lo2, rr, census, pub)
    assert (ev.determination, ev.cause) == ("NOT PRODUCED", "hysteresis") and dict(ev.tests[2].detail)["delta_m"] == pub.delta_m.value == ev.fidelity.delta_m
    assert E.evaluate_p1(hi, lo1, rr, census, pub).determination == "PRODUCED"                              # one spacing: inside the frozen bracket
    with pytest.raises(TypeError): E.evaluate_p1(hi, lo2, rr, census, pub, delta_m=0.3)                     # no override parameter exists
    stale = dataclasses.replace(pub, delta_m=dataclasses.replace(pub.delta_m, value=0.3))                   # Δm altered, identity retained
    with pytest.raises(E.EvaluatorDomainError, match="closure publication refused"): E.evaluate_p1(hi, lo2, rr, census, stale)
    recomputed = dataclasses.replace(stale, result_sha256=stale.identity())                                  # Δm altered, identity recomputed
    with pytest.raises(E.EvaluatorDomainError, match="closure publication refused"): E.evaluate_p1(hi, lo2, rr, census, recomputed)
    assert E.evaluate_p1(hi, lo2, rr, census).publication_sha256 == pub.result_sha256                       # the default is the frozen publication


# ======================= determination and the full evaluation =======================
def test_p1_determination_precedence():
    P = lambda t: E.TestResult(t, "PASS", None); F = lambda t, c: E.TestResult(t, "FAIL", c); N = lambda t, c: E.TestResult(t, "ND", c)
    assert E.p1_determination([P("a"), P("b"), P("c"), P("d")]) == ("PRODUCED", None)
    assert E.p1_determination([P("a"), N("b", "x"), F("c", "hysteresis"), P("d")]) == ("NOT PRODUCED", "hysteresis")     # a valid failure outranks an ND
    assert E.p1_determination([P("a"), N("b", "x"), N("c", "y"), P("d")]) == ("NOT DISTINGUISHED", "x")

def test_evaluate_p1_on_the_map_branches_is_produced_and_records_fidelity(census, pub):
    hi = mk("skeleton_high", branch("skeleton"), survs(1.0)); lo = mk("skeleton_low", branch("skeleton"), survs(1.0)); re_ = mk("realization", branch("realization"))
    ev = E.evaluate_p1(hi, lo, re_, census, pub)
    assert ev.determination == "PRODUCED" and ev.cause is None and ev.role == "synthetic" and ev.m_hat_c == "1.032609"
    assert [t.outcome for t in ev.tests] == ["PASS"] * 4 and ev.result_sha256 == ev.identity()
    f = ev.fidelity
    assert abs(f.shift_vs_closure - 0.032609) < 1e-9 and abs(f.shift_vs_pair - (1.032609 - pub.m_lat)) < 1e-9 and f.delta_m == pub.delta_m.value
    assert len(f.realization_vs_rho_re) == 24 and f.realization_vs_rho_re[0][1] == f.realization_vs_rho_re[0][2] and f.realization_vs_rho_re[0][5] == 0.0   # med == ρ* by construction
    assert len(f.skeleton_vs_rho_sk) == 24 - 8 and all(row[4] == CL.fidelity_band(census, i + 8) for i, row in enumerate(f.skeleton_vs_rho_sk))
    assert f.m_hat_infl is not None and 1.0 < f.m_hat_infl < 1.3 and f.shift_infl_vs_closure == f.m_hat_infl - pub.m_infl and not f.inflection_at_sweep_edge
    assert f.ratio_reference is not None and f.ratio_unavailable_reason == ""
    assert len(f.below_boundary_ratios) == sum(1 for m in MS if m < 1.032609 - pub.delta_m.value) and all(0 < row[2] < 1 for row in f.below_boundary_ratios)
    assert "finite-horizon persistence" in ev.claim_strength

def test_fidelity_rows_carry_signed_residuals_the_actual_ratio_reference_and_component_widths(census, pub):
    """L2 r1 D7. Residuals keep their signs; the reference is the first grid level ≥ m̂_c + Δm (MP1-4) with its median and
    width; each ratio row carries the numerator width; unavailable ratios carry their reason; none of it scores P1."""
    sk = branch("skeleton"); re_ = branch("realization"); c = 8
    up = [x + 0.02 for x in re_]; down = [max(x - 0.02, 0.001) for x in re_]
    f_up = E.fidelity_tier(mk("skeleton_high", sk, survs(1.0)), mk("realization", up), census, c, pub)
    f_dn = E.fidelity_tier(mk("skeleton_high", sk, survs(1.0)), mk("realization", down), census, c, pub)
    assert all(abs(r[5] - 0.02) < 1e-12 and abs(r[6] - (r[1] - r[3])) < 1e-15 for r in f_up.realization_vs_rho_re)
    assert all(r[5] < 0.0 for r in f_dn.realization_vs_rho_re)
    ref_idx = next(i for i, m in enumerate(MS) if m >= MS[c] + pub.delta_m.value)                           # 1.032609 + 0.1201 → 1.228261 (two levels up)
    assert ref_idx == c + 2 and f_up.ratio_reference == (C.level_id(L[ref_idx]), up[ref_idx], CL.fidelity_band(census, ref_idx))
    for lv, med, ratio, w in f_up.below_boundary_ratios:
        i = [C.level_id(u) for u in L].index(lv)
        assert MS[i] < MS[c] - pub.delta_m.value and med == up[i] and ratio == up[i] / up[ref_idx] and w == CL.fidelity_band(census, i)
    # unavailable ratios name their reason
    assert E.fidelity_tier(mk("skeleton_high", sk, survs(1.0)), mk("realization", re_), census, None, pub).ratio_unavailable_reason.startswith("no located boundary")
    zero_ref = list(re_); zero_ref[ref_idx] = 0.0
    assert E.fidelity_tier(mk("skeleton_high", sk, survs(1.0)), mk("realization", zero_ref), census, c, pub).ratio_unavailable_reason.startswith("non-positive reference median")
    assert "above the sweep" in E.fidelity_tier(mk("skeleton_high", sk, survs(2.3)), mk("realization", re_), census, 22, pub).ratio_unavailable_reason
    assert "apparatus" in E.fidelity_tier(mk("skeleton_high", sk, survs(1.0)), mk("realization", re_, unevaluable={3: "HALT-q"}), census, c, pub).ratio_unavailable_reason
    # fidelity disagreement and the edge flag change nothing in the four-test determination
    ev_up = E.evaluate_p1(mk("skeleton_high", sk, survs(1.0)), mk("skeleton_low", sk, survs(1.0)), mk("realization", up), census, pub)
    ev_re = E.evaluate_p1(mk("skeleton_high", sk, survs(1.0)), mk("skeleton_low", sk, survs(1.0)), mk("realization", re_), census, pub)
    assert ev_up.determination == ev_re.determination == "PRODUCED" and [t.outcome for t in ev_up.tests] == [t.outcome for t in ev_re.tests]

def test_evaluate_p1_role_and_object_discipline(census, pub):
    hi = mk("skeleton_high", branch("skeleton"), survs(1.0)); lo = mk("skeleton_low", branch("skeleton"), survs(1.0)); re_ = mk("realization", branch("realization"))
    with pytest.raises(E.EvaluatorDomainError): E.evaluate_p1(lo, hi, re_, census, pub)                     # objects swapped
    with pytest.raises(E.EvaluatorDomainError): E.evaluate_p1(hi, lo, mk("realization", branch("realization"), role="canonical"), census, pub)   # mixed roles / canonical needs canonical census
    canon = mk("skeleton_high", branch("skeleton"), survs(1.0), role="canonical")                         # canonical without run provenance: refused by validation
    with pytest.raises(E.EvaluatorDomainError): E.validate_sweep_record(canon)
    with pytest.raises(E.EvaluatorDomainError): E.validate_sweep_record(dataclasses.replace(hi, result_sha256="0" * 64))
    bad_levels = hi.levels[:1] + (dataclasses.replace(hi.levels[1], rho_hats=(1.5,) + hi.levels[1].rho_hats[1:]),) + hi.levels[2:]
    with pytest.raises(E.EvaluatorDomainError): E.validate_sweep_record(reseal(hi, bad_levels))
    with pytest.raises(E.EvaluatorDomainError): E.validate_sweep_record(reseal(hi, hi.levels[:1] + (dataclasses.replace(hi.levels[1], run_spec_hashes=("x",) * 20),) + hi.levels[2:]))   # synthetic carries no provenance
    surv_zero = (True,) * 20
    with pytest.raises(E.EvaluatorDomainError, match="surviving run cannot have zero"): E.validate_sweep_record(reseal(hi, hi.levels[:1] + (dataclasses.replace(hi.levels[1], survivals=surv_zero),) + hi.levels[2:]))

def test_when_t_s1_prime_fails_the_dependent_tests_are_not_evaluable_and_t_r1_still_runs(census, pub):
    hi = mk("skeleton_high", [0.0] * 24, [0] * 24); lo = mk("skeleton_low", branch("skeleton"), survs(1.0)); re_ = mk("realization", branch("realization"))
    ev = E.evaluate_p1(hi, lo, re_, census, pub)
    assert ev.determination == "NOT PRODUCED" and ev.cause == "no active phase in sweep" and ev.m_hat_c is None
    assert ev.tests[1].outcome == "ND" and "did not locate a boundary" in ev.tests[1].cause and ev.tests[3].outcome == "PASS"
    assert ev.fidelity.m_hat_c is None and ev.fidelity.skeleton_vs_rho_sk == () and ev.fidelity.below_boundary_ratios == ()
    assert len(ev.fidelity.realization_vs_rho_re) == 24 and ev.fidelity.m_hat_infl is not None                # boundary-independent observations are retained


# ======================= canonical sweep provenance from M1 results (D3, D4) =======================
def test_sweep_from_results_binds_to_canonical_panel_runs():
    u = L[23]
    results = {u: [D.run(C.f8_run_spec(u, sd, "skeleton_high")) for sd in C.F8_SEED_PANEL[:3]]}
    with pytest.raises(E.EvaluatorDomainError): E.sweep_from_results("skeleton_high", results)             # 3 of 20
    results = {u: [D.run(C.f8_run_spec(u, sd, "skeleton_high", grid=8, ticks=100)) for sd in range(20)]}
    with pytest.raises(E.EvaluatorDomainError): E.sweep_from_results("skeleton_high", results)             # smoke shape / off panel
    # a full level of REAL production runs for one level, every other level halted (shape of the record, not a result)
    full = [D.run(C.f8_run_spec(u, sd, "skeleton_high")) for sd in C.F8_SEED_PANEL]
    halts = {v: f"HALT-not-run-{i}" for i, v in enumerate(L) if v != u}
    sw = E.sweep_from_results("skeleton_high", {u: full}, halts)
    E.validate_sweep_record(sw); E.validate_sweep_record(sw, {u: full}, halts)                               # structural, then by replay
    assert sw.role == "canonical" and sw.levels[23].surv == sum(r.survival for r in full) and sw.levels[0].unevaluable
    assert len(sw.levels[23].run_spec_hashes) == 20 and sw.levels[23].run_rho_sha256s == tuple(r.rho_sha256() for r in full)
    both = dict(halts); both[u] = "HALT-both"
    with pytest.raises(E.EvaluatorDomainError): E.sweep_from_results("skeleton_high", {u: full}, both)
    with pytest.raises(E.EvaluatorDomainError): E.sweep_from_results("realization", {u: full}, halts)      # object mismatch

def test_the_observation_is_recomputed_from_the_persisted_trace_and_stale_or_tampered_records_are_refused():
    """L2 r1 D3: the cached summary must equal M1's arithmetic over the trace; the sweep identity binds the density records."""
    u = L[23]; halts = {v: f"HALT-{i}" for i, v in enumerate(L) if v != u}
    full = full_level(u)                                                                                      # forced all-active trajectories through M1's summary arithmetic
    sw = E.sweep_from_results("skeleton_high", {u: full}, halts)
    assert sw.levels[23].surv == 20 and sw.levels[23].med == 1.0
    trunc = [dataclasses.replace(r, rho=r.rho[:1], active_counts=r.active_counts[:1]) for r in full]        # truncated traces
    with pytest.raises(E.EvaluatorDomainError, match="length ticks \\+ 1"): E.sweep_from_results("skeleton_high", {u: trunc}, halts)
    stale = [dataclasses.replace(r, survival=False, rho_tail_mean=0.0, tail_window_means=(0.0,) * 10) for r in full]   # full traces, lying summaries
    with pytest.raises(E.EvaluatorDomainError, match="does not recompute"): E.sweep_from_results("skeleton_high", {u: stale}, halts)
    altered = []                                                                                              # altered trace content → a different observation identity
    for r in full:
        cnt = r.active_counts.copy(); cnt[2500:] = 1
        altered.append(forced_result(C.f8_run_spec(u, r.seed, "skeleton_high"), cnt))
    sw2 = E.sweep_from_results("skeleton_high", {u: altered}, halts)
    assert sw2.result_sha256 != sw.result_sha256 and sw2.levels[23].run_rho_sha256s != sw.levels[23].run_rho_sha256s and sw2.levels[23].med < 1.0
    with pytest.raises(E.EvaluatorDomainError, match="does not replay"): E.validate_sweep_record(sw, {u: altered}, halts)
    bad_rho = [dataclasses.replace(r, rho=r.rho * 0.5) for r in full]                                        # density record inconsistent with the counts
    with pytest.raises(E.EvaluatorDomainError, match="active_counts / n_cells"): E.sweep_from_results("skeleton_high", {u: bad_rho}, halts)
    with pytest.raises(E.EvaluatorDomainError, match="not an M1 F8RunResult"): E.sweep_from_results("skeleton_high", {u: [dataclasses.asdict(r) for r in full]}, halts)

def test_extinction_before_inside_and_at_the_end_of_the_tail_is_a_valid_observation_as_m1_defines_it():
    """L2 r1 D4: the evaluator carries M1's placed observable. Extinct before the tail → survival False, ρ̂ 0; extinct inside
    the tail → survival False, ρ̂ > 0 (the pre-extinction contributions); extinct inside the final window → the same;
    never extinct → survival True. Each is accepted into the sweep and the summary arithmetic is M1's."""
    u = L[23]; halts = {v: f"HALT-{i}" for i, v in enumerate(L) if v != u}
    spec0 = C.f8_run_spec(u, C.F8_SEED_PANEL[0], "skeleton_high"); T, n = spec0.ticks, spec0.n_cells
    def trajectory(last_active):
        def f(spec):
            c = np.zeros(spec.ticks + 1, dtype=np.int64); c[:last_active + 1] = spec.n_cells; return c
        return f
    cases = {"before": T - 1500, "early_window": 2050, "final_window": T - 10, "never": T}
    expect = {"before": (False, 0.0, T - 1499), "early_window": (False, 0.05, 2051), "final_window": (False, 0.99, T - 9), "never": (True, 1.0, None)}
    for name, last in cases.items():
        lvl = full_level(u, counts_fn=trajectory(last))
        surv, rho_hat, ext = expect[name]
        assert all(r.survival == surv and abs(r.rho_tail_mean - rho_hat) < 1e-12 and r.extinction_tick == ext for r in lvl), name
        r0 = lvl[0]
        assert E.observation_from_result(r0, C.f8_run_spec(u, r0.seed, "skeleton_high")) == (r0.survival, r0.rho_tail_mean, r0.tail_window_means)
        sw = E.sweep_from_results("skeleton_high", {u: lvl}, halts)                                        # accepted, not coerced
        E.validate_sweep_record(sw)
        assert sw.levels[23].surv == (20 if surv else 0) and abs(sw.levels[23].med - rho_hat) < 1e-12
    assert expect["early_window"][1] == 50 / 1000 and full_level(u, counts_fn=trajectory(2050))[0].tail_window_means == (0.5,) + (0.0,) * 9
    # a trace that is non-zero after its first zero is not an absorbing skeleton trace, and a wrong cached extinction tick is refused
    def resurrect(spec):
        c = np.full(spec.ticks + 1, spec.n_cells, dtype=np.int64); c[2050] = 0; return c
    with pytest.raises(E.EvaluatorDomainError, match="non-zero after extinction"): E.sweep_from_results("skeleton_high", {u: full_level(u, counts_fn=resurrect)}, halts)
    wrong_ext = [dataclasses.replace(r, extinction_tick=2050) for r in full_level(u, counts_fn=trajectory(2050))]
    with pytest.raises(E.EvaluatorDomainError, match="extinction tick"): E.sweep_from_results("skeleton_high", {u: wrong_ext}, halts)


# ======================= known-answer corpus (D5, D6) =======================
def test_synthetic_census_has_declared_s_hat_and_valid_provenance(census):
    CL.validate_calibration_census(census)
    assert all(abs(s - 0.01) < 1e-15 for s in census.s_hat_re + census.s_hat_sk) and census.role == "derived_provisional"
    assert E.synthetic_census().result_sha256 == census.result_sha256                                       # deterministic: the declared identity

def test_steep_control_first_rise_is_exactly_the_declared_two_f_j_of_the_range(census, pub):
    """L2 r1 D5 / MP1-3: the first adjacent rise above the boundary is 2·f_J × R exactly; the endpoint is preserved; the
    branch is non-decreasing; the generated case yields the continuity ND with its named cause, never a scientific FAIL."""
    sk = branch("skeleton", 1.0); c = next(i for i, m in enumerate(MS) if m > 1.0)
    st = E.steep_continuous_branch(1.0); R = sk[-1] - sk[c]
    assert st[:c + 1] == sk[:c + 1] and abs((st[c + 1] - st[c]) - 2 * E.F_J * R) < 1e-15 and abs((st[c + 1] - st[c]) / R - 0.5) < 1e-14
    assert abs(st[-1] - sk[-1]) < 1e-15 and all(st[i + 1] >= st[i] for i in range(c, 23))                    # endpoint preserved (to an ulp)
    assert all(st[i + 1] - st[i] <= E.F_J * R + 1e-15 for i in range(c + 1, 23))                            # only the declared rise exceeds f_J·R
    for r in range(3):
        ev, want_det, want_cause = E.known_answer_case("nd_steep_continuous", r, census, pub)
        assert ev.determination == "NOT DISTINGUISHED" and ev.cause == f"continuity unresolved at grid resolution ({C.level_id(L[c + 1])})"
        assert all(t.outcome != "FAIL" for t in ev.tests)

@pytest.mark.parametrize("cls", E.KA_CLASSES)
def test_each_known_answer_class_returns_its_named_verdict_and_cause_on_three_replicates(cls, census, pub):
    for r in range(3):
        ev, want_det, want_cause = E.known_answer_case(cls, r, census, pub)
        assert ev.determination == want_det, (cls, r, ev.tests)
        if want_cause: assert ev.cause is not None and ev.cause.startswith(want_cause), (cls, r, ev.cause)
        else: assert ev.cause is None
        if cls == "fail_no_active_phase": assert ev.tests[3].outcome == "PASS", ev.tests[3]                    # the control is clean: only T-S1' triggers (L2 r1 §6.3)

def test_qualification_is_bound_to_the_declared_synthetic_census(census):
    """L2 r1 D6: a different but valid synthetic census, or a canonical-role census, cannot qualify."""
    q = E.known_answer_qualification(sweeps_per_class=2, classes=E.KA_CLASSES[:2], census=census)            # a reduced run is NOT a record of qualification
    assert not q.passed and q.census_is_declared_synthetic and len(q.per_class) == 2 and q.per_class[0][3] == 2 and q.per_class[0][4] == 0 and q.result_sha256 == q.identity()
    other = E.synthetic_census(0.005)
    CL.validate_calibration_census(other)
    q2 = E.known_answer_qualification(sweeps_per_class=1, classes=E.KA_CLASSES[:1], census=other)
    assert not q2.census_is_declared_synthetic and not q2.passed and q2.census_sha256 != census.result_sha256
    canon = dataclasses.replace(other, role="canonical"); canon = dataclasses.replace(canon, result_sha256=canon.identity())
    with pytest.raises(E.EvaluatorDomainError, match="synthetic"): E.known_answer_qualification(sweeps_per_class=1, classes=E.KA_CLASSES[:1], census=canon)
    with pytest.raises(E.EvaluatorDomainError): E.known_answer_case("no_such_class", 0, census, CL.closure_publication())

def test_cross_trigger_counter_on_the_real_qualification_path(monkeypatch, census):
    """Controlled evaluator outputs through the ACTUAL counter and final gate: 95 named matches + 5 right-determination /
    wrong-cause cases pass; 94 + 6 do not; the cross-trigger count is carried separately."""
    def controlled(wrong):
        def fake(cls, r, cen, pub, master=E.KNOWN_ANSWER_MASTER):
            cause = "hysteresis" if r >= wrong else "no active phase in sweep"
            ev = E.P1Evaluation("synthetic", "NOT PRODUCED", cause, (), None, None, cen.result_sha256, pub.result_sha256, ("", "", ""), "", E.EVALUATOR_SHA256_LITERAL)
            return ev, "NOT PRODUCED", "hysteresis"
        return fake
    for wrong, want in ((5, True), (6, False)):
        monkeypatch.setattr(E, "known_answer_case", controlled(wrong))
        q = E.known_answer_qualification(census=census)
        assert all(row[3] == 100 - wrong and row[4] == wrong and row[5] == 100 for row in q.per_class) and q.passed is want
    monkeypatch.setattr(E, "known_answer_case", controlled(0))
    assert not E.known_answer_qualification(census=E.synthetic_census(0.005)).passed                          # the declared census is part of passage

def test_f8_mp1_does_not_touch_e1():
    from mfa_instrument.e1 import projection as EP
    assert EP.PROJECTION_DECLARATION_SHA256_LITERAL == "e9a109a505433fa42fea08ac4ee1830dde9b418fb35f1740c7453a4ad0cf4fc0"
