"""tests/test_f8_m1.py — Flight 8 module M1: frozen identities verify against their generating rules, the literals,
and APPENDIX_A_OF_RECORD.md; the hazard rule executes exactly as Contract F8 v0.8.4 §2 writes it (probabilities,
synchrony, absorbing skeleton, null independence, stream derivation, extinction as a valid observation); the stepper
is bit-identical to the committed design-evidence probe's rule under identical uniforms; nothing in e1 is touched."""
import math
import os
from fractions import Fraction
import numpy as np
import pytest

from mfa_instrument import config as CFG
from mfa_instrument.config import DynamicsConstants
from mfa_instrument.f8 import config as C
from mfa_instrument.f8 import dynamics as D

HERE = os.path.dirname(os.path.abspath(__file__))
APPENDIX_A = os.path.normpath(os.path.join(HERE, "..", "..", "contracts", "flight8", "APPENDIX_A_OF_RECORD.md"))
SMOKE = dict(grid=8, ticks=100)  # below production shape: any seed admissible; tail = all 100 ticks = one window (shape policy, D3)


# ======================= frozen identities =======================
def test_frozen_level_list_matches_rule_contract_arithmetic_and_appendix_a():
    C.verify_frozen_identity()
    assert C.F8_LEVELS_MICRO == C.generate_pass1_levels_micro() and len(C.F8_LEVELS_MICRO) == 24
    assert (C.F8_LEVELS_MICRO[0], C.F8_LEVELS_MICRO[-1]) == (250000, 2500000)
    assert sorted({b - a for a, b in zip(C.F8_LEVELS_MICRO, C.F8_LEVELS_MICRO[1:])}) == [97826, 97827]
    assert C.S_P1_MICRO == 97826 and C.W_RES_MICRO == 293478 == 3 * C.S_P1_MICRO
    assert C.level_id(250000) == "0.250000" and C.level_id(934783) == "0.934783" and len({C.level_id(m) for m in C.F8_LEVELS_MICRO}) == 24
    assert sum(1 for m in C.F8_LEVELS_MICRO if m < 1_000_000) >= 7 and sum(1 for m in C.F8_LEVELS_MICRO if m > 1_000_000) >= 7   # crossing interior (§4.1)

@pytest.mark.skipif(not os.path.isfile(APPENDIX_A), reason="repository contracts directory not present")
def test_m1_binds_to_appendix_a_of_record():
    out = C.verify_against_appendix_a(APPENDIX_A)
    assert out["appendix_a_sha256"] == C.F8_APPENDIX_A_SHA256 and out["levels_match"] and abs(out["delta_m"] - 0.1201) < 5e-5

def test_seed_panels_rule_generated_distinct_and_disjoint():
    assert C.F8_SEED_PANEL == C.generate_seed_panel(C.F8_SEED_PANEL_MASTER) and len(set(C.F8_SEED_PANEL)) == 20
    assert C.F8_CALIBRATION_SEED_PANEL == C.generate_seed_panel(C.F8_CALIBRATION_MASTER) and len(set(C.F8_CALIBRATION_SEED_PANEL)) == 20
    assert not set(C.F8_SEED_PANEL) & set(C.F8_CALIBRATION_SEED_PANEL)
    assert C.F8_SEED_PANEL_MASTER != C.F8_CALIBRATION_MASTER and 20260917 not in (C.F8_SEED_PANEL_MASTER, C.F8_CALIBRATION_MASTER)
    assert C.frozen_digest(C.F8_SEED_PANEL) == C.F8_SEED_PANEL_SHA256_LITERAL
    assert C.frozen_digest(C.F8_CALIBRATION_SEED_PANEL) == C.F8_CALIBRATION_PANEL_SHA256_LITERAL

def test_e1_frozen_panel_is_not_reused():
    from mfa_instrument.e1 import config as E1
    assert not set(E1.E1_SEED_PANEL) & set(C.F8_SEED_PANEL) and E1.E1_SEED_PANEL_MASTER != C.F8_SEED_PANEL_MASTER
    assert E1.E1_LEVELS_MICRO != C.F8_LEVELS_MICRO

@pytest.mark.parametrize("name,bad", [
    ("F8_LEVELS_SHA256_LITERAL", "0" * 64), ("F8_SEED_PANEL_SHA256_LITERAL", "0" * 64),
    ("F8_CALIBRATION_PANEL_SHA256_LITERAL", "0" * 64), ("F8_DECLARATION_SHA256_LITERAL", "0" * 64),
    ("F8_MU", 0.25), ("W_RES_MICRO", 293479), ("F8_G", 2.0),
])
def test_frozen_identity_tamper_blocks_spec_construction(monkeypatch, name, bad):
    monkeypatch.setattr(C, name, bad)
    with pytest.raises(C.F8ConfigError):
        C.f8_run_spec(C.F8_LEVELS_MICRO[0], C.F8_SEED_PANEL[0], "realization")

def test_tampered_level_literal_is_caught(monkeypatch):
    monkeypatch.setattr(C, "F8_LEVELS_MICRO", C.F8_LEVELS_MICRO[:-1] + (2500001,))
    with pytest.raises(C.F8ConfigError):
        C.f8_run_spec(C.F8_LEVELS_MICRO[0], C.F8_SEED_PANEL[0], "realization")

def test_declaration_names_the_frozen_contract_and_rule_values():
    d = dict(C.F8_DECLARATION)
    assert d["contract_sha256"].startswith("e87277a2d11e948f") and d["appendix_a_sha256"].startswith("94d527624beafa7c")
    assert d["version"] == "f8_stage1_v1" and d["mu"] == 0.2 and d["g"] == 1.0 and d["eta0"] == -math.log(0.99)
    assert d["f_dispatch"] == "F_2_symmetric" and d["bases"] == "homogeneous" and d["q"] == "off" and d["drive"] == 0.0 and d["noise"] == 0.0
    assert d["timing"] == "synchronous_two_phase" and d["neighbourhood"] == "moore_8_periodic"


# ======================= control coordinate and bases =======================
def test_control_coordinate_m_equals_one_at_the_closure_crossing():
    q = C.q_deact()
    assert q == 1.0 - math.exp(-0.2)
    lam = C.lambda_bar_from_level(1_000_000)
    assert lam == q and C.F8_G * lam * C.F8_DT / q == 1.0                      # m = 1 <=> g·lambda_bar·dt = 1 − e^(−mu dt)
    assert C.lambda_bar_from_level(250_000) == 0.25 * q and C.lambda_bar_from_level(2_500_000) == 2.5 * q

def test_homogeneous_bases_reach_lambda_bar_under_the_frozen_f_2_symmetric_form():
    k = DynamicsConstants()
    for m in C.F8_LEVELS_MICRO:
        lam = C.lambda_bar_from_level(m); b = C.homogeneous_base_from_lambda(lam)
        assert 0.0 < b < 1.0
        f = (b * b * b) * (k.w_v * b + k.w_u * b + k.w_r * b)                 # F_2_symmetric at v = u = r = b
        assert abs(f - lam) <= 8 * np.finfo(np.float64).eps * max(lam, 1.0)
    with pytest.raises(C.F8ConfigError): C.homogeneous_base_from_lambda(1.5)


# ======================= the rule =======================
def test_activation_and_deactivation_probabilities_are_the_written_forms():
    d = np.arange(9, dtype=np.float64) / 8.0
    for eta in (0.0, C.F8_ETA0):
        p = D.activation_probability(eta, 1.0, 0.3, d)
        assert np.array_equal(p, 1.0 - np.exp(-(eta + 0.3 * d)))
    assert D.activation_probability(0.0, 1.0, 0.3, np.zeros(3))[0] == 0.0       # skeleton, no active neighbours: exactly 0
    assert D.deactivation_probability(0.2) == 1.0 - math.exp(-0.2)
    assert abs(1.0 - math.exp(-C.F8_ETA0) - 0.01) < 1e-15                      # eta0 reproduces the spec's per-tick 0.01 (RULED)
    assert abs(D.stationary_pi1(C.F8_ETA0, 0.2) - 0.052282320137314486) < 1e-15  # Appendix A pi1

def test_skeleton_all_inactive_is_exactly_absorbing():
    x = np.zeros((6, 6), dtype=bool)
    for u in (np.zeros((6, 6)), np.full((6, 6), 1e-300), np.random.default_rng(1).random((6, 6))):
        assert not D.step(x, u, eta_floor=0.0, g=1.0, lambda_bar=0.45, mu=0.2).any()

def test_null_transitions_are_independent_of_neighbours():
    rng = np.random.default_rng(7); u = rng.random((10, 10))
    x1 = rng.random((10, 10)) < 0.5; x2 = x1.copy(); x2[::2, ::2] = ~x2[::2, ::2]    # same cells differ in neighbourhood
    y1 = D.step(x1, u, eta_floor=C.F8_ETA0, g=0.0, lambda_bar=0.45, mu=0.2)
    y2 = D.step(x2, u, eta_floor=C.F8_ETA0, g=0.0, lambda_bar=0.45, mu=0.2)
    same = x1 == x2
    assert np.array_equal(y1[same], y2[same])                                   # outcome depends only on own state and own uniform
    a = 1.0 - math.exp(-C.F8_ETA0); q = D.deactivation_probability(0.2)
    assert np.array_equal(y1, np.where(x1, u >= q, u < a))

def test_synchronous_update_reads_only_the_state_at_t():
    L = 9; x = np.zeros((L, L), dtype=bool); x[4, 4] = True
    u = np.zeros((L, L))                                                        # every cell draws u = 0: activates iff p_act > 0
    y = D.step(x, u, eta_floor=0.0, g=1.0, lambda_bar=0.45, mu=0.2)
    moore = {(4 + i, 4 + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)}
    assert {tuple(p) for p in np.argwhere(y)} == moore                           # only Moore neighbours at t activate; the centre deactivates (u < q)
    assert not y[4, 4]

def test_local_density_uses_periodic_moore_eight():
    x = np.zeros((5, 5), dtype=bool); x[0, 0] = True
    d = D.local_density(x)
    assert d[0, 0] == 0.0 and d[4, 4] == 1 / 8 and d[1, 1] == 1 / 8 and d[0, 4] == 1 / 8 and d[2, 2] == 0.0
    assert d.sum() == 1.0

def test_stepper_is_bit_identical_to_the_committed_probe_rule_under_identical_uniforms():
    """The design-evidence probe (contracts/flight8/lattice_check.py) writes the rule as pa = 1 − exp(−(eta + g·lam·k/8)),
    x' = where(x, u >= pd, u < pa) with the eight np.roll shifts. Same uniforms, same trajectory, bit for bit."""
    L, T, mu, m, eta = 20, 50, 0.2, 1.5, 0.0
    qd = 1 - math.exp(-mu); glam = m * qd
    rng = np.random.default_rng(3); x_probe = np.ones((L, L), bool); x_ours = x_probe.copy(); us = [rng.random((L, L)) for _ in range(T)]
    for u in us:
        k = sum(np.roll(np.roll(x_probe, di, 0), dj, 1) for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di, dj) != (0, 0)).astype(float)
        pa = 1 - np.exp(-(eta + glam * k / 8)); x_probe = np.where(x_probe, u >= qd, u < pa)
        x_ours = D.step(x_ours, u, eta_floor=eta, g=1.0, lambda_bar=glam, mu=mu)
        assert np.array_equal(x_probe, x_ours)


# ======================= streams, specs, runs =======================
def test_stream_keys_separate_objects_and_levels_and_reproduce():
    s = C.F8_SEED_PANEL[0]; m0, m1 = C.F8_LEVELS_MICRO[0], C.F8_LEVELS_MICRO[1]
    keys = {C.stream_key(s, o, m) for o in C.OBJECT_CODES for m in (m0, m1)}
    assert len(keys) == 2 * len(C.OBJECT_CODES)
    a = C.run_generator(s, "realization", m0).random(4); b = C.run_generator(s, "realization", m0).random(4)
    c = C.run_generator(s, "realization", m1).random(4); d = C.run_generator(s, "skeleton_high", m0).random(4)
    assert np.array_equal(a, b) and not np.array_equal(a, c) and not np.array_equal(a, d)
    e = C.init_low_generator(s, m0).random(4)
    assert not np.array_equal(e, a) and np.array_equal(e, C.init_low_generator(s, m0).random(4))

def test_spec_construction_policies():
    m, s = C.F8_LEVELS_MICRO[5], C.F8_SEED_PANEL[3]
    sp = C.f8_run_spec(m, s, "realization")
    assert (sp.eta_floor, sp.g, sp.mu, sp.grid, sp.ticks, sp.tail_ticks, sp.window) == (C.F8_ETA0, 1.0, 0.2, 50, 3000, 1000, 100)
    assert C.f8_run_spec(m, s, "null").g == 0.0 and C.f8_run_spec(m, s, "skeleton_high").eta_floor == 0.0 and C.f8_run_spec(m, s, "skeleton_low").eta_floor == 0.0
    with pytest.raises(C.F8ConfigError, match="panel"): C.f8_run_spec(m, 12345, "realization")                 # production shape, non-panel seed
    with pytest.raises(C.F8ConfigError): C.f8_run_spec(m, C.F8_CALIBRATION_SEED_PANEL[0], "skeleton_low", panel="calibration")
    assert C.f8_run_spec(m, C.F8_CALIBRATION_SEED_PANEL[0], "skeleton_high", panel="calibration").obj == "skeleton_high"
    assert C.f8_run_spec(m, 12345, "realization", **SMOKE).grid == 8                                             # smoke shape: any seed
    with pytest.raises(C.F8ConfigError): C.f8_run_spec(m, s, "unknown_object")
    with pytest.raises(C.F8ConfigError): C.f8_run_spec(m, True, "realization")
    with pytest.raises(C.F8ConfigError): C.f8_run_spec(1.0, s, "realization")
    assert sp.spec_hash() == C.f8_run_spec(m, s, "realization").spec_hash() and sp.declaration_sha256 == C.F8_DECLARATION_SHA256_LITERAL

def test_realization_stationary_start_frequency_and_draw_accounting():
    for s in C.F8_SEED_PANEL[:3]:
        sp = C.f8_run_spec(C.F8_LEVELS_MICRO[0], s, "realization", grid=50, ticks=100)
        r = D.run(sp)
        pi1 = D.stationary_pi1(C.F8_ETA0, 0.2); sd = math.sqrt(2500 * pi1 * (1 - pi1))
        assert abs(r.active_counts[0] - 2500 * pi1) < 5 * sd
        assert r.draws_consumed == 101 and r.ticks_advanced == 100 and len(r.rho) == 101 and r.rho[0] == r.active_counts[0] / 2500.0
    sk = D.run(C.f8_run_spec(C.F8_LEVELS_MICRO[23], C.F8_SEED_PANEL[0], "skeleton_high", grid=50, ticks=100))
    assert sk.active_counts[0] == 2500 and sk.draws_consumed == 100 and sk.extinction_tick is None

def test_skeleton_low_initial_fraction_is_exactly_rho0():
    r = D.run(C.f8_run_spec(C.F8_LEVELS_MICRO[23], C.F8_SEED_PANEL[0], "skeleton_low", grid=50, ticks=100))
    assert r.active_counts[0] == 50

def test_extinction_is_a_valid_observation_and_absorbing_thereafter():
    r = D.run(C.f8_run_spec(C.F8_LEVELS_MICRO[0], 99, "skeleton_low", grid=10, ticks=200))     # m = 0.25: skeleton dies quickly
    assert r.extinction_tick is not None and r.ticks_advanced == r.extinction_tick < 200
    assert not r.survival and not r.active_counts[r.extinction_tick:].any()
    assert r.rho_tail_mean == float(r.rho[1:].mean()) and r.draws_consumed == r.extinction_tick   # tail = whole run below production shape
    # at production tail length an extinction before the tail contributes exactly 0 (§4.11: a valid observation)
    r2 = D.run(C.f8_run_spec(C.F8_LEVELS_MICRO[0], C.F8_SEED_PANEL[1], "skeleton_low", grid=50, ticks=3000))
    assert r2.extinction_tick is not None and r2.extinction_tick < 2001 and r2.rho_tail_mean == 0.0 and r2.tail_window_means == (0.0,) * 10

def test_run_is_deterministic_and_tail_windows_are_ordered_and_complete():
    sp = C.f8_run_spec(C.F8_LEVELS_MICRO[23], 5, "realization", grid=12, ticks=400)
    r1, r2 = D.run(sp), D.run(sp)
    assert np.array_equal(r1.rho, r2.rho) and r1.rho_sha256() == r2.rho_sha256()
    assert len(r1.tail_window_means) == 4 and sp.tail_ticks == 400 and r1.tail_window_means == tuple(float(r1.rho[1 + i * 100:1 + (i + 1) * 100].mean()) for i in range(4))
    assert r1.rho_tail_mean == float(r1.rho[1:].mean())

def test_rho_table_roundtrip(tmp_path):
    import pandas as pd
    r = D.run(C.f8_run_spec(C.F8_LEVELS_MICRO[10], 11, "realization", **SMOKE))
    sha = D.write_rho_table(r, str(tmp_path / "x.parquet"))
    tbl = pd.read_parquet(tmp_path / "x.parquet")
    assert list(tbl.columns) == ["Tick", "rho_global"] and len(tbl) == 101 and np.array_equal(tbl["rho_global"].to_numpy(), r.rho) and len(sha) == 64

def test_f8_does_not_touch_e1_identities():
    from mfa_instrument.e1 import config as E1
    E1.verify_frozen_identity()
    assert E1.E1_DECLARATION_SHA256_LITERAL == "76102dfbf514dc859f0045631dc1d3bcb0cfc376cca21ad3458ad20868e5dfa8"


# ======================= round-2 repairs (L2 M1 r1 D1–D4) =======================
def test_d1_production_shape_requires_a_frozen_pass1_level():
    s = C.F8_SEED_PANEL[0]
    for bad in (1_000_000, 250_001, 2_600_000, 100):
        with pytest.raises(C.F8ConfigError, match="pass-1 level"): C.f8_run_spec(bad, s, "skeleton_high")
        with pytest.raises(C.F8ConfigError, match="pass-1 level"): C.f8_run_spec(bad, C.F8_CALIBRATION_SEED_PANEL[0], "realization", panel="calibration")
    for m in C.F8_LEVELS_MICRO: assert C.f8_run_spec(m, s, "skeleton_high").level_micro == m
    assert C.f8_run_spec(1_000_000, s, "skeleton_high", **SMOKE).level_micro == 1_000_000      # controls below production shape: any level

@pytest.mark.parametrize("field,value", [
    ("g", 0.0), ("g", 2.0), ("eta_floor", 0.0), ("eta_floor", 0.5), ("mu", 0.3), ("lambda_bar", 0.9), ("base_homogeneous", 0.5),
    ("obj", "null"), ("panel", "calibration"), ("seed", 12345), ("level_micro", 1_000_000), ("level_id", "1.000000"),
    ("tail_ticks", 900), ("window", 50), ("stream_key", (1, 2, 3)), ("declaration_sha256", "0" * 64),
    ("g", 1), ("grid", 50.0),                                                   # type changes with equal value
])
def test_d2_mutated_spec_cannot_execute(field, value):
    import dataclasses
    good = C.f8_run_spec(C.F8_LEVELS_MICRO[12], C.F8_SEED_PANEL[0], "realization")
    bad = dataclasses.replace(good, **{field: value})
    with pytest.raises(C.F8ConfigError): C.validate_run_spec(bad)
    with pytest.raises(C.F8ConfigError): D.run(bad)

def test_d2_shape_substitution_yields_an_honest_reduced_spec_not_a_disguised_production_run():
    """Replacing grid/ticks with a valid reduced shape is indistinguishable from building that reduced spec: the record states
    its own shape, the tail follows the shape, and no production-shape identity is claimed (production = (50, 3000) exactly)."""
    import dataclasses
    good = C.f8_run_spec(C.F8_LEVELS_MICRO[12], C.F8_SEED_PANEL[0], "realization")
    for kw in ({"grid": 49}, {"ticks": 2900}):
        red = C.validate_run_spec(dataclasses.replace(good, **kw))
        assert red == C.f8_run_spec(good.level_micro, good.seed, good.obj, grid=red.grid, ticks=red.ticks) and (red.grid, red.ticks) != (50, 3000)

    good = C.f8_run_spec(C.F8_LEVELS_MICRO[3], C.F8_SEED_PANEL[2], "skeleton_low", **SMOKE)
    assert C.validate_run_spec(good) == good
    class Fake: pass
    with pytest.raises(C.F8ConfigError): C.validate_run_spec(Fake())
    import dataclasses
    with pytest.raises(C.F8ConfigError): C.validate_run_spec(dataclasses.replace(good, panel="neither"))

def test_d2_executed_stream_is_the_recorded_key():
    sp = C.f8_run_spec(C.F8_LEVELS_MICRO[20], 77, "realization", **SMOKE)
    g = C.generator_from_key(sp.stream_key); x0 = g.random((8, 8)) < D.stationary_pi1(C.F8_ETA0, 0.2)
    r = D.run(sp)
    assert r.stream_key == sp.stream_key and r.active_counts[0] == int(np.count_nonzero(x0))

@pytest.mark.parametrize("grid,ticks", [(0, 100), (1, 100), (2, 100), (8, 0), (8, 50), (8, 150), (8, 950), (51, 3000), (50, 3001), (-3, 100)])
def test_d3_undefined_shapes_fail_closed(grid, ticks):
    with pytest.raises(C.F8ConfigError): C.f8_run_spec(C.F8_LEVELS_MICRO[0], 5, "realization", grid=grid, ticks=ticks)

@pytest.mark.parametrize("grid,ticks,wins", [(3, 100, 1), (8, 300, 3), (8, 1000, 10), (8, 1050, 10), (8, 2000, 10), (50, 3000, 10)])
def test_d3_defined_shapes_give_whole_windows_and_finite_means(grid, ticks, wins):
    seed = 5 if (grid, ticks) != (50, 3000) else C.F8_SEED_PANEL[0]
    r = D.run(C.f8_run_spec(C.F8_LEVELS_MICRO[23], seed, "realization", grid=grid, ticks=ticks))
    assert len(r.tail_window_means) == wins and np.isfinite(r.rho_tail_mean) and all(np.isfinite(r.tail_window_means))

def test_d4_panels_checked_against_the_actual_retired_e1_panel(monkeypatch):
    from mfa_instrument.e1 import config as E1
    assert C.E1_RETIRED_SEED_PANEL == E1.E1_SEED_PANEL and C.E1_RETIRED_SEED_PANEL_SHA256 == E1.E1_SEED_PANEL_SHA256_LITERAL
    C.verify_frozen_identity()
    # discriminating collision: plant one retired E1 seed into the canonical panel (digest literal re-pointed so only the overlap can fail)
    planted = C.F8_SEED_PANEL[:-1] + (C.E1_RETIRED_SEED_PANEL[4],)
    monkeypatch.setattr(C, "F8_SEED_PANEL", planted)
    monkeypatch.setattr(C, "generate_seed_panel", lambda master, n=20: planted if master == C.F8_SEED_PANEL_MASTER else C.F8_CALIBRATION_SEED_PANEL)
    monkeypatch.setattr(C, "F8_SEED_PANEL_SHA256_LITERAL", C.frozen_digest(planted))
    with pytest.raises(C.F8ConfigError, match="retired panel"): C.verify_frozen_identity()

def test_d4_tampered_retired_literal_is_caught(monkeypatch):
    monkeypatch.setattr(C, "E1_RETIRED_SEED_PANEL", C.E1_RETIRED_SEED_PANEL[:-1] + (1,))
    with pytest.raises(C.F8ConfigError, match="retired-panel literal"): C.verify_frozen_identity()


def test_d5_extinction_inside_the_last_tail_window_is_not_survival():
    """Find a smoke-shape skeleton run that dies inside its LAST tail window; it must not survive (L1 r2 D5)."""
    found = None
    for seed in range(400):
        r = D.run(C.f8_run_spec(1_300_000, seed, "skeleton_high", grid=6, ticks=300))
        if r.extinction_tick is not None and 201 < r.extinction_tick <= 300:
            found = r; break
    assert found is not None, "no discriminating case found in the search range"
    assert found.active_counts[201:found.extinction_tick].min() > 0 and not found.survival
    alive = D.run(C.f8_run_spec(C.F8_LEVELS_MICRO[23], C.F8_SEED_PANEL[0], "skeleton_high"))
    assert alive.survival == (alive.active_counts[-1] > 0) == True
