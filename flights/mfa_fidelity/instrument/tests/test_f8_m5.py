"""tests/test_f8_m5.py — Flight 8 module M5: the §3.1 map and its fixed points reproduce APPENDIX_A_OF_RECORD.md (exact
identity; tables, Δm and m_lat within the declared 1e-12 — bit-equal on the producing platform, ≤ 1 ulp of libm elsewhere;
m_infl exact); the skeleton crossing is exactly m = 1; the pair closure reproduces Appendix B.3; the
dense census issues the reference of record only on the exact grid with zero halts and gives the pre-registered class;
reference stability and the independent solver agree; the §3.4 band machinery and MDD stop path are exact arithmetic on
census content; finite-N projection sweeps replay and design stability fails closed on halts."""
import dataclasses
import math
import os
import numpy as np
import pytest

from mfa_instrument.f8 import config as C
from mfa_instrument.f8 import classify as K
from mfa_instrument.f8 import null as N
from mfa_instrument.f8 import verdict as V
from mfa_instrument.f8 import closure as CL

HERE = os.path.dirname(os.path.abspath(__file__))
APPENDIX_A = os.path.normpath(os.path.join(HERE, "..", "..", "contracts", "flight8", "APPENDIX_A_OF_RECORD.md"))
L = C.F8_LEVELS_MICRO


# ======================= identity and the map =======================
def test_frozen_identity_and_constants():
    CL.verify_frozen_identity()
    assert (CL.QS_MIN_ACTIVE, CL.K_R, CL.MDD_CEILING, CL.PANEL_N, CL.T_PRE, CL.DENSE_POINTS) == (50, 3, 0.02, 20, 2000, 701)
    assert CL.Q_DEACT == 1.0 - math.exp(-0.2) and CL.lambda_bar(1.0) == CL.Q_DEACT

@pytest.mark.parametrize("name,bad", [("CLOSURE_SHA256_LITERAL", "0" * 64), ("QS_MIN_ACTIVE", 60), ("K_R", 2), ("MDD_CEILING", 0.03), ("DENSE_POINTS", 700)])
def test_tamper_is_caught(monkeypatch, name, bad):
    monkeypatch.setattr(CL, name, bad)
    with pytest.raises(CL.ClosureDomainError): CL.tables()

def test_map_is_the_contract_equation_and_skeleton_crossing_is_exactly_m_equals_one():
    for m, eta, rho in [(0.5, 0.0, 0.1), (1.3, CL.ETA0, 0.2), (2.5, 0.0, 0.5)]:
        glam = m * CL.Q_DEACT
        assert CL.g_map(rho, m, eta) == (1 - rho) * (1 - math.exp(-(eta + glam * rho))) + rho * math.exp(-0.2)
    assert CL.skeleton_multiplier(1.0) == math.exp(-0.2) + CL.Q_DEACT and abs(CL.skeleton_multiplier(1.0) - 1.0) < 1e-15
    assert CL.skeleton_multiplier(0.9) < 1.0 < CL.skeleton_multiplier(1.1)
    assert CL.rho_sk(1.0) == 0.0 and CL.rho_sk(0.999) == 0.0 and CL.rho_sk(1.001) > 0.0
    assert CL.g_map(0.0, 1.5, 0.0) == 0.0                                                  # the absorbing state is a fixed point of the skeleton map
    assert CL.rho_re(0.25) > 0.0 and CL.g_map_vec(np.array([0.1, 0.2]), 1.3, CL.ETA0)[0] == CL.g_map(0.1, 1.3, CL.ETA0)

def test_fixed_points_monotone_continuous_from_zero_and_rounded():
    sk, re_ = CL.tables()
    vs = [sk[k] for k in sk]; vr = [re_[k] for k in re_]
    assert all(b >= a for a, b in zip(vs, vs[1:])) and all(b > a for a, b in zip(vr, vr[1:]))
    assert vs[0] == 0.0 and vs[7] == 0.0 and vs[8] > 0.0 and L[7] < 1_000_000 < L[8]                # 0 up to and including the last level below 1
    assert all(r > s for r, s in zip(vr, vs)) and abs(vr[0] - 0.0669) < 1e-3 and abs(vs[-1] - 0.5483) < 1e-3   # contract Appendix A rounded values
    assert abs(CL.rho_re(1.0) - 0.1994) < 1e-3


# ======================= Appendix A, exact identity and tolerance-bound tables =======================
@pytest.mark.skipif(not os.path.isfile(APPENDIX_A), reason="repository contracts directory not present")
def test_m5_binds_to_appendix_a_within_declared_tolerance():
    out = CL.verify_against_appendix_a(APPENDIX_A)
    assert out["appendix_a_sha256"] == C.F8_APPENDIX_A_SHA256 and out["levels_match"]
    assert abs(out["delta_m"] - 0.120126265992375) <= CL.APPENDIX_A_BIND_TOL and out["m_infl"] == CL.m_infl() and abs(out["m_infl"] - 1.1765) < 1e-12
    assert out["bind_tol"] == 1e-12 and out["max_abs_deviation"] <= 1e-15      # ≤ a few ulp on any platform's libm
    assert out["bit_equal"] == (len(out["not_bit_equal"]) == 0)
    assert all(k.startswith(("rho_sk[", "rho_re[", "delta_m.", "m_lat")) for k in out["not_bit_equal"])

@pytest.mark.skipif(not os.path.isfile(APPENDIX_A), reason="repository contracts directory not present")
def test_appendix_a_tolerance_is_operative_in_both_directions(monkeypatch):
    real = CL.rho_sk
    # perturb only levels above 1.5 so Δm's bisection (near m ≈ 1.02) is untouched and the deviation is the injected one
    monkeypatch.setattr(CL, "rho_sk", lambda m: real(m) + (5e-13 if m > 1.5 else 0.0))    # inside the band: binds, not bit-equal
    out = CL.verify_against_appendix_a(APPENDIX_A)
    assert not out["bit_equal"] and 4e-13 < out["max_abs_deviation"] <= 1e-12 and any(k.startswith("rho_sk[") for k in out["not_bit_equal"])
    monkeypatch.setattr(CL, "rho_sk", lambda m: real(m) + (2e-12 if m > 1.5 else 0.0))    # outside the band: refused, offending keys named
    with pytest.raises(CL.ClosureDomainError, match="beyond the declared tolerance"): CL.verify_against_appendix_a(APPENDIX_A)
    monkeypatch.setattr(CL, "rho_sk", real)
    monkeypatch.setattr(CL, "m_infl", lambda: 1.1765000000000001)                           # m_infl is a grid value: exact, no tolerance
    with pytest.raises(CL.ClosureDomainError, match="m_infl"): CL.verify_against_appendix_a(APPENDIX_A)

@pytest.mark.skipif(not os.path.isfile(APPENDIX_A), reason="repository contracts directory not present")
def test_appendix_a_level_list_is_enforced_by_the_verifier_itself(monkeypatch, tmp_path):
    """D4 (L2 round 4): the pass-1 level list is a binding predicate, not a reported flag. The identity gate is left intact;
    the parsed payload is substituted after it (one level moved by one micro-unit; dropped; reordered) and the verifier
    must refuse on its own — no caller inspection of `levels_match`."""
    real_parse = CL._parse_appendix_a
    def altered(mutate):
        def parse(raw):
            j = real_parse(raw); lv = list(j["levels_micro"]); mutate(lv); j["levels_micro"] = lv; return j
        return parse
    for mutate in (lambda lv: lv.__setitem__(5, lv[5] + 1), lambda lv: lv.pop(), lambda lv: lv.reverse()):
        monkeypatch.setattr(CL, "_parse_appendix_a", altered(mutate))
        with pytest.raises(CL.ClosureDomainError, match="pass-1 level list"): CL.verify_against_appendix_a(APPENDIX_A)
    monkeypatch.setattr(CL, "_parse_appendix_a", real_parse)
    assert CL.verify_against_appendix_a(APPENDIX_A)["levels_match"] is True
    # the identity gate still precedes everything: a byte-altered copy is refused before parsing
    bad = tmp_path / "altered_appendix_a.md"
    with open(APPENDIX_A, "rb") as f: bad.write_bytes(f.read() + b"\n")
    with pytest.raises(CL.ClosureDomainError, match="identity"): CL.verify_against_appendix_a(str(bad))

def test_delta_m_m_infl_m_lat_values():
    dm = CL.delta_m()
    assert abs(dm.lower - 0.021581283487712034) < 1e-15 and abs(dm.upper - 0.022300265992375) < 1e-15 and dm.s == 0.097826 and dm.value == max(dm.lower, dm.upper) + dm.s
    assert abs(dm.lower - math.log(2500) / (CL.Q_DEACT * 2000)) < 1e-15 and 2500 * CL.rho_sk(1.0 + dm.upper) >= 50 > 2500 * CL.rho_sk(1.0 + dm.upper - 1e-9)
    assert abs(CL.m_infl() - 1.1765) < 1e-9 and abs(CL.m_lat() - 1.1414) < 5e-4
    assert abs(CL.pair_leading_multiplier(1.0) - 0.9789) < 5e-4 and abs(CL.pair_leading_multiplier(CL.m_lat()) - 1.0) < 1e-9       # Appendix B.3

def test_pair_closure_reproduces_appendix_b3():
    assert abs(CL.pair_fixed_point(0.0, 1.2) - 0.051) < 2e-3 and abs(CL.pair_fixed_point(0.0, 1.5) - 0.242) < 2e-3 and abs(CL.pair_fixed_point(0.0, 2.5) - 0.526) < 2e-3
    assert abs(CL.pair_fixed_point(CL.ETA0, 0.25) - 0.066) < 2e-3 and abs(CL.pair_fixed_point(CL.ETA0, 1.0) - 0.176) < 2e-3 and abs(CL.pair_fixed_point(CL.ETA0, 2.5) - 0.544) < 2e-3
    assert CL.pair_fixed_point(0.0, 1.0) == 0.0 or CL.pair_fixed_point(0.0, 1.0) < 1e-6                                      # below m_lat the pair skeleton dies

def test_closure_publication_replays_and_is_identity_bound():
    pub = CL.closure_publication(); CL.validate_closure_publication(pub)
    assert pub.m_closure == 1.0 and len(pub.rho_sk) == 24 and pub.result_sha256 == pub.identity()
    with pytest.raises(CL.ClosureDomainError): CL.validate_closure_publication(dataclasses.replace(pub, m_lat=1.2))


# ======================= the census =======================
def test_dense_grid_round_half_even_and_declaration():
    g = CL.dense_grid_micro()
    assert len(g) == 701 and g[0] == 250000 and g[-1] == 2500000 and list(g) == sorted(set(g))
    assert set(L) - set(g)                                                                      # declared: 700 is not a multiple of 23, so not every pass-1 level is a dense point
    assert CL.dense_grid_micro(24) == L                                                         # the same rule reproduces M1's grid at 24 points

def test_dense_reference_issues_the_role_only_on_the_exact_grid_and_gives_the_pre_registered_class():
    ref = CL.dense_reference(); CL.validate_reference_structure(ref)
    assert ref.role == "reference_of_record" and ref.n_levels == 701 and ref.halts == ()
    assert ref.structure_class == "NO-NULL-PHASE" and (ref.verdict, ref.cause, ref.rule) == ("NOT_PRODUCED", "no_null_consistent_phase", "2")   # §1.3(a), §4.9
    assert set(ref.labels) == {"S"} and ref.threshold_identity == N.null_thresholds(L[0]).payload_identity()
    with pytest.raises(CL.ClosureDomainError): CL.classify_grid(L, "reference_of_record")
    with pytest.raises(CL.ClosureDomainError): CL.classify_grid(CL.dense_grid_micro(), "reference_of_record", halts=("x",))
    sub = CL.classify_grid(L, "analysis_subset"); assert sub.role == "analysis_subset" and sub.structure_class == "NO-NULL-PHASE"
    with pytest.raises(CL.ClosureDomainError): CL.validate_reference_structure(dataclasses.replace(ref, structure_class="UNIQUE-THRESHOLD"))

def test_projected_label_uses_m2_precedence_and_16_2_4():
    th = N.null_thresholds(L[0])
    lab, pt = CL.projected_label(L[0], th)
    assert lab == "S" and pt.s_min > th.theta_p and len(pt.window_means) == 10 and pt.s_term == pt.window_means[9]
    # a synthetic orbit below theta_T everywhere -> N; between -> U
    low = np.full(K.RECORD_LEN, 0.01); mid = np.full(K.RECORD_LEN, (th.theta_p + th.theta_t) / 2)
    for series, want in ((low, "N"), (mid, "U")):
        pt2 = CL.projected_tail_stats(series)
        st = "SUSTAINED" if pt2.s_min > th.theta_p else ("NO_SUSTAINED" if pt2.s_term <= th.theta_t else "UNRESOLVED")
        assert K.level_label(K.LevelCounts(*(20 if st == s else 0 for s in K.STATUSES))) == want
    with pytest.raises(CL.ClosureDomainError): CL.projected_tail_stats(np.full(3000, 0.5))

def test_structure_class_map_covers_every_rule():
    for lab, want in [(("N",) * 24, "NO-SUSTAINED-PHASE"), (("S",) * 24, "NO-NULL-PHASE"), (("U",) * 24, "REFERENCE-UNRESOLVED"),
                      (("N",) * 6 + ("S",) * 6 + ("N",) * 6 + ("S",) * 6, "ORDER-VIOLATING/MULTIPLE"), (("N",) * 12 + ("S",) * 12, "UNIQUE-THRESHOLD"),
                      (("N",) * 8 + ("U",) * 5 + ("S",) * 11, "REFERENCE-UNRESOLVED"), (("N",) * 4 + ("M",) + ("N",) * 5 + ("S",) * 14, "REFERENCE-UNRESOLVED")]:
        assert CL._structure_class(V.evaluate(lab, L), lab, ()) == want
    assert CL._structure_class(V.evaluate(("S",) * 24, L), ("S",) * 24, ("halt",)) == "REFERENCE-UNRESOLVED"


# ======================= reference stability =======================
def test_stability_audit_canonical_requires_the_reference_and_agrees():
    ref = CL.dense_reference()
    sa = CL.stability_audit(ref, "canonical"); CL.validate_stability_audit(sa, ref)
    assert sa.all_alternatives_agree and sa.fixed_points_agree and sa.fixed_point_max_abs_diff < CL.STABILITY_FP_TOL and {a[0] for a in sa.alternative_grids} == {351, 1401}
    sub = CL.classify_grid(L, "analysis_subset")
    with pytest.raises(CL.ClosureDomainError): CL.stability_audit(sub, "canonical")
    with pytest.raises(CL.ClosureDomainError): CL.validate_stability_audit(dataclasses.replace(sa, all_alternatives_agree=False), ref)

def test_independent_solver_agrees_and_detects_the_absorbing_branch():
    for u in L:
        m = CL.level_m(u)
        assert abs(CL.fixed_point_bisection(m, CL.ETA0) - CL.rho_re(m)) < 1e-11 and abs(CL.fixed_point_bisection(m, 0.0) - CL.rho_sk(m)) < 1e-11
    assert CL.fixed_point_bisection(0.9, 0.0) == 0.0 and CL.fixed_point_bisection(1.5, 0.0) > 0.0


# ======================= §3.4 calibration bands, provenance (D2), record kinds (D3) =======================
def _runs(spread_re=0.004, spread_sk=0.006, seed=1, obj_swap=False, panel="calibration"):
    """960 CalibrationRun records with VALID provenance (specs reconstructed on the calibration panel) and synthetic
    densities around the closure's fixed points — exercises the census arithmetic and the provenance checks without 960
    production-shape lattice runs."""
    g = np.random.default_rng(seed); sk, re_ = CL.tables(); seeds = C.F8_CALIBRATION_SEED_PANEL if panel == "calibration" else C.F8_SEED_PANEL
    out = []
    for u in L:
        m = CL.level_m(u)
        for sd in seeds:
            for obj in CL.CALIBRATION_OBJECTS:
                spec = C.f8_run_spec(u, sd, obj, panel=panel)
                centre = re_[f"{m:.6f}"] if obj == "realization" else (sk[f"{m:.6f}"] if m > 1.0 else 0.0)
                val = float(np.clip(centre + g.normal(0, spread_re if obj == "realization" else spread_sk), 0, 1)) if centre > 0 else 0.0
                rec_obj = ("skeleton_high" if obj == "realization" else "realization") if obj_swap else obj
                out.append(CL.CalibrationRun(u, sd, rec_obj, spec.spec_hash(), spec.stream_key, val, val > 0, "ab" * 32))
    return out

def test_calibration_run_from_a_real_stepper_result_and_refusals():
    from mfa_instrument.f8 import dynamics as D
    r = D.run(C.f8_run_spec(L[23], C.F8_CALIBRATION_SEED_PANEL[0], "realization", panel="calibration"))
    cr = CL.calibration_run(r)
    assert cr.obj == "realization" and cr.spec_hash == r.spec_hash and cr.rho_tail_mean == r.rho_tail_mean and cr.rho_sha256 == r.rho_sha256()
    r_canon = D.run(C.f8_run_spec(L[23], C.F8_SEED_PANEL[0], "realization"))                     # canonical panel: not a job-0 run
    with pytest.raises(CL.ClosureDomainError): CL.calibration_run(r_canon)
    r_low = D.run(C.f8_run_spec(L[23], C.F8_CALIBRATION_SEED_PANEL[0], "skeleton_low", grid=8, ticks=100))
    with pytest.raises(CL.ClosureDomainError): CL.calibration_run(r_low)                            # wrong object
    r_smoke = D.run(C.f8_run_spec(L[23], 5, "realization", grid=8, ticks=100))
    with pytest.raises(CL.ClosureDomainError): CL.calibration_run(r_smoke)                          # not production shape / not panel
    with pytest.raises(CL.ClosureDomainError): CL.calibration_run(dataclasses.replace(r, spec_hash="0" * 64))

def test_calibration_census_arithmetic_bands_and_replay():
    runs = _runs(); c = CL.calibration_census(runs); CL.validate_calibration_census(c); CL.validate_calibration_census(c, runs)
    assert c.role == "derived_provisional" and c.calibration_master == C.F8_CALIBRATION_MASTER and c.objects == ("realization", "skeleton_high")
    f = 3 * 1.2533 / math.sqrt(20)
    for i in range(24):
        assert c.s_hat_re[i] == float(np.std(c.rho_hat_re[i], ddof=1)) and c.mdd_re[i] == f * c.s_hat_re[i]
        assert CL.fidelity_band(c, i) == 3 * c.s_hat_re[i] * 1.2533 / math.sqrt(20)
        assert c.run_spec_hashes_re[i][0] == C.f8_run_spec(L[i], C.F8_CALIBRATION_SEED_PANEL[0], "realization", panel="calibration").spec_hash()
    assert c.s_hat_sk[0] == 0.0 and c.mdd_sk[0] == 0.0                                           # extinct below the boundary: ŝ_sk ≈ 0 (§3.4)
    assert c.ceilings_met and not c.stop_path_triggered
    assert CL.evaluability_band(c, "skeleton_high", 3, 4) == 3 * math.sqrt(c.s_hat_sk[3] ** 2 + c.s_hat_sk[4] ** 2) * 1.2533 / math.sqrt(20)
    assert CL.evaluability_band(c, "realization", 3, 4) == 3 * math.sqrt(c.s_hat_re[3] ** 2 + c.s_hat_re[4] ** 2) * 1.2533 / math.sqrt(20)
    with pytest.raises(CL.ClosureDomainError): CL.evaluability_band(c, "realization", 3, 5)
    with pytest.raises(CL.ClosureDomainError): CL.evaluability_band(c, "null", 3, 4)
    for kw in ({"s_hat_re": c.s_hat_re[:-1] + (0.0,)}, {"ceilings_met": not c.ceilings_met}, {"calibration_master": 1}, {"role": "canonical"},
               {"run_spec_hashes_re": (("0" * 64,) * 20,) + c.run_spec_hashes_re[1:]}):
        with pytest.raises(CL.ClosureDomainError): CL.validate_calibration_census(dataclasses.replace(c, **kw))

def test_d2_census_provenance_refusals():
    runs = _runs()
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census(runs, role="canonical")        # M7 issues canonical, never M5
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census(_runs(obj_swap=True))           # swapped objects: spec hashes do not reconstruct
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census(_runs(panel="canonical"))       # wrong panel (wrong master)
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census(runs[:-1])                      # one run missing
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census(runs + [runs[0]])               # duplicate
    bad = list(runs); bad[0] = dataclasses.replace(bad[0], spec_hash="0" * 64)
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census(bad)
    bad2 = list(runs); bad2[0] = dataclasses.replace(bad2[0], stream_key=(1, 2, 3))
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census(bad2)
    bad3 = list(runs); bad3[0] = dataclasses.replace(bad3[0], rho_tail_mean=1.5)
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census(bad3)
    with pytest.raises(CL.ClosureDomainError): CL.calibration_census([("not", "a", "run")] + runs[1:])

def test_mdd_ceiling_violation_triggers_the_stop_path():
    c = CL.calibration_census(_runs(spread_re=0.03))
    assert c.max_mdd_re > 0.02 and not c.ceilings_met and c.stop_path_triggered
    CL.validate_calibration_census(c)

def test_d3_record_kinds_are_separate_and_complete():
    c = CL.calibration_census(_runs()); ens = CL.tolerance_ensembles(c); prog = CL.tolerance_program(c)
    assert len(ens) == 24 and all(e.census_sha256 == c.result_sha256 and len(e.rho_hat_re) == 20 and len(e.run_spec_hashes_sk) == 20 for e in ens)
    assert ens[5].level_id == C.level_id(L[5]) and ens[5].s_hat_re == c.s_hat_re[5]
    assert prog.complete and prog.ensemble_count == 24 and prog.census_sha256 == c.result_sha256 and prog.ceilings_met and not prog.stop_path_triggered


# ======================= finite-N projection sweeps and design stability =======================
def test_finite_n_counts_track_the_map_and_sweep_replays():
    g = np.random.default_rng(5)
    counts = CL.finite_n_counts(2.5, CL.ETA0, g, n=2500, ticks=600)
    assert counts.shape == (601,) and counts.min() >= 0 and counts.max() <= 2500
    assert abs(counts[300:].mean() / 2500 - CL.rho_re(2.5)) < 0.01                                 # independent-cell closure sits on the map's fixed point
    sw = CL.projection_sweep(0); CL.validate_projection_sweep(sw)
    assert sw.structure_class == "NO-NULL-PHASE" and sw.halts == () and sw.master == CL.PROJECTION_MASTER and sw.result_sha256 == sw.identity()
    assert CL.projection_sweep(0) == sw and CL.projection_sweep(1) != sw
    with pytest.raises(CL.ClosureDomainError): CL.validate_projection_sweep(dataclasses.replace(sw, labels=("N",) * 24))
    with pytest.raises(CL.ClosureDomainError): CL.projection_sweep(-1)

def test_d1_sweep_set_validation_refuses_wrong_master_mutation_and_bad_reference():
    ref = CL.dense_reference(); sw0 = CL.projection_sweep(0)
    CL.validate_projection_sweep_structure(sw0, ref.threshold_identity)
    wrong_master = CL.projection_sweep(1, master=999)                                             # buildable for diagnostics…
    with pytest.raises(CL.ClosureDomainError): CL.validate_sweep_set(ref, [sw0, wrong_master])    # …but never admissible to an ensemble
    with pytest.raises(CL.ClosureDomainError): CL.validate_sweep_set(ref, [sw0, dataclasses.replace(sw0, sweep_index=1, labels=("N",) * 24)])   # mutated content ≠ identity
    forged = dataclasses.replace(sw0, sweep_index=1, labels=("N",) * 24); forged = dataclasses.replace(forged, result_sha256=forged.identity())
    with pytest.raises(CL.ClosureDomainError): CL.validate_sweep_set(ref, [sw0, forged])          # consistent identity but verdict/class do not recompute
    with pytest.raises(CL.ClosureDomainError): CL.validate_sweep_set(ref, [sw0, dataclasses.replace(sw0, threshold_identity="0" * 64, result_sha256="")])
    with pytest.raises(CL.ClosureDomainError): CL.validate_sweep_set(dataclasses.replace(ref, structure_class="UNIQUE-THRESHOLD"), [sw0])      # reference identity broken
    with pytest.raises(CL.ClosureDomainError): CL.validate_sweep_set(ref, [sw0, sw0])
    CL.validate_sweep_set(ref, [sw0], replay=True)

def test_d1_canonical_role_requires_declared_master_and_exact_index_set():
    """A factored check with minimal fixtures: a 200-sweep ensemble under another master cannot be canonical (D1)."""
    ref = CL.dense_reference(); sw0 = CL.projection_sweep(0)
    fakes = []
    for i in range(200):
        f = dataclasses.replace(sw0, sweep_index=i, master=999); fakes.append(dataclasses.replace(f, result_sha256=f.identity()))
    with pytest.raises(CL.ClosureDomainError): CL.design_stability(ref, fakes)
    good = []
    for i in range(200):
        f = dataclasses.replace(sw0, sweep_index=i); good.append(dataclasses.replace(f, result_sha256=f.identity()))
    d = CL.design_stability(ref, good)                                                            # structurally valid stand-ins (not replayed): canonical by structure
    assert d.role == "canonical" and d.attempted == 200 and d.cp_lower_95 > 0.98 and d.evaluable and d.design_stable is True
    # a stand-in whose CONTENT differs from the real sweep (a consistent LOCATED sequence) passes structure but fails replay
    v = V.evaluate(("N",) * 12 + ("S",) * 12, L)
    fake = dataclasses.replace(sw0, sweep_index=1, labels=("N",) * 12 + ("S",) * 12, verdict=v.verdict, cause=v.cause, rule=v.rule, structure_class="UNIQUE-THRESHOLD")
    fake = dataclasses.replace(fake, result_sha256=fake.identity())
    CL.validate_projection_sweep_structure(fake, ref.threshold_identity)
    with pytest.raises(CL.ClosureDomainError): CL.design_stability(ref, [sw0, fake], replay=True)    # replay: sweep 1 ≠ projection_sweep(1)
    sub = CL.classify_grid(L, "analysis_subset")
    with pytest.raises(CL.ClosureDomainError): CL.design_stability(sub, good)                     # full ensemble needs the reference of record
    shifted = good[1:] + [dataclasses.replace(good[0], sweep_index=200, result_sha256=dataclasses.replace(good[0], sweep_index=200).identity())]
    ds = CL.design_stability(ref, shifted)
    assert ds.role == "analysis_subset" and not ds.evaluable and ds.design_stable is None and ds.subset_all_match is True   # D1-R2: 200 sweeps, zero halts, all matching — still NOT qualified (indices 1..200)
    with pytest.raises(CL.ClosureDomainError): CL.validate_design_stability(dataclasses.replace(ds, evaluable=True, result_sha256=dataclasses.replace(ds, evaluable=True).identity()), ref, shifted)

def test_design_stability_roles_halts_and_cp():
    ref = CL.dense_reference(); sws = [CL.projection_sweep(i) for i in range(2)]
    d = CL.design_stability(ref, sws, replay=True); CL.validate_design_stability(d, ref, sws)
    assert d.role == "analysis_subset" and d.attempted == 2 and d.matching == 2 and 0 < d.cp_lower_95 < 1
    assert not d.evaluable and d.design_stable is None and d.subset_all_match is True            # D1-R2: a subset is descriptive, never qualified
    with pytest.raises(CL.ClosureDomainError): CL.design_stability(ref, [sws[0], dataclasses.replace(sws[1], halts=("evaluability:uncertified_threshold",))])   # identity ≠ content
    halted = dataclasses.replace(sws[1], halts=("evaluability:uncertified_threshold",), structure_class="REFERENCE-UNRESOLVED"); halted = dataclasses.replace(halted, result_sha256=halted.identity())
    d2 = CL.design_stability(ref, [sws[0], halted])
    assert not d2.evaluable and d2.design_stable is None and d2.subset_all_match is None and d2.halted == 1 and d2.match_rate_over_attempted == 0.5   # HALT_POLICY: fail closed, attempted denominator
    with pytest.raises(CL.ClosureDomainError): CL.design_stability(ref, [sws[0], sws[0]])
    with pytest.raises(CL.ClosureDomainError): CL.validate_design_stability(dataclasses.replace(d, matching=1), ref, sws)
    forged = dataclasses.replace(d, matching=1); forged = dataclasses.replace(forged, result_sha256=forged.identity())
    with pytest.raises(CL.ClosureDomainError): CL.validate_design_stability(forged, ref, sws)
    assert abs(CL.clopper_pearson_lower(200, 200) - 0.985) < 5e-4 and CL.clopper_pearson_lower(0, 200) == 0.0 and 0.96 < CL.clopper_pearson_lower(198, 200) < 0.975

def test_f8_m5_does_not_touch_e1():
    from mfa_instrument.e1 import projection as EP
    assert EP.PROJECTION_DECLARATION_SHA256_LITERAL == "e9a109a505433fa42fea08ac4ee1830dde9b418fb35f1740c7453a4ad0cf4fc0"
