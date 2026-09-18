"""tests/test_e1_m1_m2.py — E1 stage-1 modules M1 (config) and M2 (classify). Frozen identities
verify against their generating rules and literal digests; the conformance preflight passes on a
real run and fails on planted defects; the classifier's constructed controls match exact answers;
count rules are total and exclusive; nothing consumes intervals."""
import json
import os
from fractions import Fraction
from itertools import product
import numpy as np
import pytest

from mfa_instrument import config as CFG
from mfa_instrument.e1 import config as C
from mfa_instrument.e1 import classify as K


# ======================= M1: frozen identities =======================
def test_frozen_level_list_matches_rule_and_contract_arithmetic():
    C.verify_frozen_identity()
    assert C.E1_LEVELS_MICRO == C.generate_pass1_levels_micro() and len(C.E1_LEVELS_MICRO) == 24
    assert (C.E1_LEVELS_MICRO[0], C.E1_LEVELS_MICRO[-1]) == (150000, 850000)
    assert C.S_P1_NOM_MICRO == 30435 and C.DELTA_M_R_MICRO == 3382 and C.S_P1_MAX_MICRO in (30434, 30435)
    assert sorted({b - a for a, b in zip(C.E1_LEVELS_MICRO, C.E1_LEVELS_MICRO[1:])}) == [30434, 30435]
    assert C.level_id(150000) == "0.150000" and C.level_id(180435) == "0.180435" and len({C.level_id(m) for m in C.E1_LEVELS_MICRO}) == 24

def test_seed_panel_is_rule_generated_and_frozen():
    assert C.E1_SEED_PANEL == C.generate_seed_panel() and len(set(C.E1_SEED_PANEL)) == 20
    assert C.frozen_digest(C.E1_SEED_PANEL) == C.E1_SEED_PANEL_SHA256_LITERAL

def test_frozen_identity_tamper_blocks_config_construction(monkeypatch):
    """The tamper is caught INSIDE e1_run_config (mechanical), not only by a separately called helper."""
    monkeypatch.setattr(C, "E1_LEVELS_SHA256_LITERAL", "0" * 64)
    with pytest.raises(C.E1ConfigError, match="digest"): C.e1_run_config(C.E1_LEVELS_MICRO[0], C.E1_SEED_PANEL[0])
    monkeypatch.undo()
    monkeypatch.setattr(C, "E1_DECLARATION_SHA256_LITERAL", "0" * 64)
    with pytest.raises(C.E1ConfigError, match="declaration"): C.e1_run_config(C.E1_LEVELS_MICRO[0], C.E1_SEED_PANEL[0])
    monkeypatch.undo()
    monkeypatch.setattr(C, "E1_LEVELS_MICRO", C.E1_LEVELS_MICRO[:-1] + (850001,))
    with pytest.raises(C.E1ConfigError): C.e1_run_config(C.E1_LEVELS_MICRO[0], C.E1_SEED_PANEL[0])

def test_declaration_binds_committed_constants_and_full_configuration():
    assert isinstance(C.E1_DECLARATION, tuple) and C.frozen_digest(C.E1_DECLARATION) == C.E1_DECLARATION_SHA256_LITERAL
    d = dict(C.E1_DECLARATION)
    assert d["f_dispatch"] == "F_canonical" and d["q_read"] == "local" and d["drive_schedule"] == () and d["noise_amplitude"] == 0.0
    assert dict(d["constants"])["alpha"] == 4.0 and dict(d["constants"])["eta_floor"] == 0.01 and dict(d["constants"])["kappa"] is None

def test_declaration_joint_tamper_cannot_self_define(monkeypatch):
    decl = tuple((k, "F_LR") if k == "f_dispatch" else (k, v) for k, v in C.E1_DECLARATION)
    monkeypatch.setattr(C, "E1_DECLARATION", decl); monkeypatch.setattr(C, "E1_DECLARATION_SHA256_LITERAL", C.frozen_digest(decl))
    with pytest.raises(C.E1ConfigError, match="configuration values"): C.verify_frozen_identity()

def test_changed_committed_constant_is_refused(monkeypatch):
    """If the instrument's default constants ever drift from the committed A values, the E1 declaration refuses."""
    import dataclasses
    from mfa_instrument import config as CFG2
    Drifted = dataclasses.make_dataclass("Drifted", [(f.name, f.type, dataclasses.field(default=(4.5 if f.name == "alpha" else f.default)))
                                                      for f in dataclasses.fields(CFG2.DynamicsConstants)])
    monkeypatch.setattr(C, "DynamicsConstants", Drifted)
    with pytest.raises(C.E1ConfigError, match="constant"): C.verify_frozen_identity()

def test_run_config_is_the_contracted_configuration():
    cfg = C.e1_run_config(C.E1_LEVELS_MICRO[0], C.E1_SEED_PANEL[0])
    assert cfg.rule_mode == "symmetric_chain" and cfg.f_dispatch == "F_canonical" and cfg.grid_scale == 50 and cfg.ticks == 3000
    assert cfg.q.gamma_psi == 0.0 and cfg.q.gamma_rho == 0.0 and cfg.q.q_read == "local"
    assert cfg.init.base_center_micro == 150000 and cfg.init.base_width_micro == 300000 and cfg.init.bernoulli_p == 0.5
    assert cfg.init.m == 0.15 and cfg.init.w == 0.3 and cfg.noise.amplitude == 0.0 and cfg.drive_schedule == ()
    assert cfg.init.base_init_mode == "stochastic_ancestor"

def test_run_config_refuses_inadmissible_level_and_off_panel_production_seed():
    with pytest.raises(C.E1ConfigError, match="inadmissible"): C.e1_run_config(100000, C.E1_SEED_PANEL[0])
    with pytest.raises(C.E1ConfigError, match="frozen panel"): C.e1_run_config(500000, 12345)
    with pytest.raises(C.E1ConfigError, match="exact integer"): C.e1_run_config(0.5, C.E1_SEED_PANEL[0])


# ======================= M1: conformance preflight on a real run =======================
@pytest.fixture(scope="module")
def small_run(tmp_path_factory):
    d = tmp_path_factory.mktemp("e1run")
    cfg = C.e1_run_config(C.E1_LEVELS_MICRO[12], 7, grid=16, ticks=40)
    return cfg, C.run_level_run(cfg, str(d), "probe")

def test_conformance_preflight_passes_on_real_run(small_run):
    cfg, run = small_run
    rep = C.conformance_preflight(run, cfg)
    assert rep.passed, rep.summary()
    assert run.q_disabled and run.clipped_counts == (0, 0, 0) and run.verifier_passed
    assert b"\r\n" not in open(run.run_config_path, "rb").read()
    assert json.load(open(run.run_config_path))["q"]["gamma_psi"] == 0.0

def test_conformance_refuses_base_drift(small_run, monkeypatch, tmp_path):
    """A planted defect: the bases are perturbed after tick 0 — the streamed bit-identity check must fail."""
    from mfa_instrument import dynamics as D
    real = D.Dynamics.step
    def drifting(self, sink=None):
        real(self, sink); self._v = np.nextafter(self._v, 1.0)
    monkeypatch.setattr(D.Dynamics, "step", drifting)
    cfg = C.e1_run_config(C.E1_LEVELS_MICRO[12], 7, grid=16, ticks=12)
    run = C.run_level_run(cfg, str(tmp_path), "drift")
    rep = C.conformance_preflight(run, cfg)
    assert not rep.passed and rep.checks["e1_base_bit_identity_verifier"] is False and rep.detail["e1_base_bit_identity"]["checks"]["base_bit_identity"] > 0

def _nonconforming(tmp_path, stem, **over):
    """A Q-disabled, base-stable run whose configuration deviates from E1 in exactly one family; the
    conformance ledger must name that family."""
    import dataclasses
    base = C.e1_run_config(C.E1_LEVELS_MICRO[12], 7, grid=16, ticks=12)
    cfg = dataclasses.replace(base, **over)
    run = C.run_level_run(cfg, str(tmp_path), stem)
    return cfg, run, C.conformance_preflight(run, cfg)

def test_conformance_refuses_wrong_f_dispatch(tmp_path):
    cfg, run, rep = _nonconforming(tmp_path, "f", f_dispatch="F_2_symmetric")
    assert not rep.passed and rep.checks["rule_and_f"] is False and rep.checks["e1_base_bit_identity_verifier"] is True   # bases still fixed: only the family fails

def test_conformance_refuses_global_q_read(tmp_path):
    cfg, run, rep = _nonconforming(tmp_path, "q", q=CFG.QConfig(q_read="global", gamma_psi=0.0, gamma_rho=0.0))
    assert not rep.passed and rep.checks["q_and_read"] is False and rep.checks["q_disabled_branch_selected"] is True

def test_conformance_refuses_nonempty_drive(tmp_path):
    cfg, run, rep = _nonconforming(tmp_path, "d", drive_schedule=((0, 0.1),))
    assert not rep.passed and rep.checks["drive_and_noise"] is False

def test_conformance_refuses_nonzero_mfa_noise(tmp_path, small_run):
    """The E1 runner constructs no noise stream, so a noise-enabled config cannot even execute through it
    (a stronger refusal); the conformance ledger, asked about such a config, names the family."""
    import dataclasses
    with pytest.raises(Exception):
        _nonconforming(tmp_path, "n", noise=CFG.NoiseConfig(amplitude=0.01))
    cfg, run = small_run
    rep = C.conformance_preflight(run, dataclasses.replace(cfg, noise=CFG.NoiseConfig(amplitude=0.01)))
    assert not rep.passed and rep.checks["drive_and_noise"] is False and rep.checks["run_config_hash_matches_executed"] is False

def test_conformance_refuses_wrong_initialization(tmp_path):
    cfg, run, rep = _nonconforming(tmp_path, "i", init=CFG.InitConfig(scheme="bernoulli_p", base_center_micro=C.E1_LEVELS_MICRO[12], base_width_micro=200000, bernoulli_p=0.5, base_init_mode="stochastic_ancestor"))
    assert not rep.passed and rep.checks["initialization"] is False
    with pytest.raises(CFG.ConfigError):                       # the instrument itself refuses deterministic bases under symmetric_chain
        _nonconforming(tmp_path, "i2", init=CFG.InitConfig(scheme="bernoulli_p", base_center_micro=C.E1_LEVELS_MICRO[12], base_width_micro=300000, bernoulli_p=0.5, base_init_mode="deterministic_level"))
    cfg, run, rep = _nonconforming(tmp_path, "i3", init=CFG.InitConfig(scheme="bernoulli_p", base_center_micro=C.E1_LEVELS_MICRO[12], base_width_micro=300000, bernoulli_p=0.25, base_init_mode="stochastic_ancestor"))
    assert not rep.passed and rep.checks["initialization"] is False

def test_conformance_refuses_changed_constant(tmp_path):
    import dataclasses
    cfg, run, rep = _nonconforming(tmp_path, "k", constants=dataclasses.replace(CFG.DynamicsConstants(), beta=3.5))
    assert not rep.passed and rep.checks["constants"] is False

def test_writer_mode_is_bound_to_the_consumed_config(monkeypatch, tmp_path):
    from mfa_instrument import telemetry as T
    seen = {}
    real = T.TelemetryWriter.__init__
    def init(self, *a, **k): seen["rule_mode"] = k.get("rule_mode"); real(self, *a, **k)
    monkeypatch.setattr(T.TelemetryWriter, "__init__", init)
    cfg = C.e1_run_config(C.E1_LEVELS_MICRO[12], 7, grid=16, ticks=6); C.run_level_run(cfg, str(tmp_path), "w")
    assert seen["rule_mode"] == cfg.rule_mode == "symmetric_chain"

def test_cleared_verifier_is_mechanically_invoked_and_decisive(monkeypatch, small_run, tmp_path):
    """A defect only the cleared E1 verifier catches — duplicate-for-missing rows with unchanged base
    bits — fails conformance through the mechanically invoked verifier, whose check map is retained."""
    cfg, run = small_run
    import pyarrow.parquet as pq, pyarrow as pa, dataclasses
    import pandas as pd
    tbl = pq.read_table(run.telemetry_path).to_pandas()
    # (a) no tick 0: the anchor is gone — only the cleared verifier's tick-0 anchoring sees this
    no0 = tbl[tbl["Tick"] != 0]
    p0 = str(tmp_path / "no0.parquet"); pq.write_table(pa.Table.from_pandas(no0, preserve_index=False), p0)
    rep = C.conformance_preflight(dataclasses.replace(run, telemetry_path=p0), cfg)
    assert not rep.passed and rep.checks["e1_base_bit_identity_verifier"] is False
    chk = rep.detail["e1_base_bit_identity"]["checks"]
    assert chk["tick0_baseline_complete"] > 0 or chk["anchored_without_tick0"] > 0 or chk["rows_total"] > 0
    # (b) a legacy Q column: the full absence set the cleared verifier asserts
    legacy = tbl.copy(); legacy["Delta_v"] = 0.0
    p1 = str(tmp_path / "legacy.parquet"); pq.write_table(pa.Table.from_pandas(legacy, preserve_index=False), p1)
    rep2 = C.conformance_preflight(dataclasses.replace(run, telemetry_path=p1), cfg)
    assert not rep2.passed and rep2.checks["e1_base_bit_identity_verifier"] is False and rep2.detail["e1_base_bit_identity"]["checks"]["schema_absent_Delta_v"] == 1
    # (c) signed-zero substitution in a base: raw-bit identity, not numeric equality
    sz = tbl.copy(); sz.loc[sz["Tick"] == sz["Tick"].max(), "b_i_v"] = sz.loc[sz["Tick"] == sz["Tick"].max(), "b_i_v"] * 0.0 - 0.0
    p2 = str(tmp_path / "sz.parquet"); pq.write_table(pa.Table.from_pandas(sz, preserve_index=False), p2)
    rep3 = C.conformance_preflight(dataclasses.replace(run, telemetry_path=p2), cfg)
    assert not rep3.passed and rep3.detail["e1_base_bit_identity"]["checks"]["base_bit_identity"] > 0

def test_conformance_refuses_q_enabled_configuration(tmp_path):
    cfg = CFG.RunConfig(seed=7, rule_mode="symmetric_chain", f_dispatch="F_canonical", grid_scale=16, ticks=12,
                        q=CFG.QConfig(q_read="local", gamma_psi=0.01, gamma_rho=0.0),
                        init=CFG.InitConfig(base_center_micro=500000, base_width_micro=300000), noise=CFG.NoiseConfig(0.0), drive_schedule=())
    run = C.run_level_run(cfg, str(tmp_path), "qon")
    rep = C.conformance_preflight(run, cfg)
    assert not rep.passed and rep.checks["q_and_read"] is False and rep.checks["q_disabled_branch_selected"] is False

def test_conformance_refuses_tampered_run_config(small_run, tmp_path):
    cfg, run = small_run
    import dataclasses, shutil
    tampered = dataclasses.replace(run, run_config_path=str(tmp_path / "rc.json"))
    raw = open(run.run_config_path, "rb").read()
    assert b'"gamma_psi":0.0' in raw                                       # the canonical form has no space
    open(tampered.run_config_path, "wb").write(raw.replace(b'"gamma_psi":0.0', b'"gamma_psi":0.0 ', 1))   # one added byte
    rep = C.conformance_preflight(tampered, cfg)
    assert not rep.passed and rep.checks["run_config_hash_matches_executed"] is False


# ======================= M2: frozen definitions and constructed controls =======================
def test_classify_declaration_is_deeply_immutable_and_gated():
    import types
    assert K.frozen_digest() == K.CLASSIFY_SHA256_LITERAL and isinstance(K.CLASSIFY_DECLARATION, tuple)
    assert all(not isinstance(v, (dict, list, set)) for _, v in K.CLASSIFY_DECLARATION)
    assert K.TAIL_START == 2000 and K.TAIL_END == 2999 and K.N_WINDOWS == 10 and K.TERMINAL_WINDOWS == (7, 8, 9)
    K.verify_frozen_identity()

def test_classify_identity_gate_blocks_public_entry_points(monkeypatch):
    monkeypatch.setattr(K, "CLASSIFY_SHA256_LITERAL", "0" * 64)
    with pytest.raises(K.ClassifyDomainError, match="digest"): K.tail_stats(np.zeros(3000))
    with pytest.raises(K.ClassifyDomainError, match="digest"): K.run_status(np.zeros(3000), 0.1, 0.1)
    with pytest.raises(K.ClassifyDomainError, match="digest"): K.level_label(K.LevelCounts(16, 2, 2))
    with pytest.raises(K.ClassifyDomainError, match="digest"): K.qualify_controls()

def test_classify_joint_tamper_cannot_self_define(monkeypatch):
    """Change a count constant AND re-establish the digest from the live declaration: the value check
    against the contracted numbers still refuses."""
    monkeypatch.setattr(K, "CONFIDENT_MIN", 15)
    decl = tuple((k, (("n_runs", 20), ("confident_min", 15), ("confident_max_other", 2), ("mixed_min_each", 4))) if k == "counts" else (k, v) for k, v in K.CLASSIFY_DECLARATION)
    monkeypatch.setattr(K, "CLASSIFY_DECLARATION", decl)
    monkeypatch.setattr(K, "CLASSIFY_SHA256_LITERAL", __import__("hashlib").sha256(repr(decl).encode()).hexdigest())
    with pytest.raises(K.ClassifyDomainError, match="count rule"): K.verify_frozen_identity()

def test_frozen_control_case_map_completes_exactly():
    q = K.qualify_controls()
    assert q.passed and len(q.results) == 6 and not q.missing and not q.extra
    assert all(ok and intended == observed for _, intended, observed, ok in q.results)
    assert K.controls_digest() == K.CONTROL_CASES_SHA256_LITERAL

def test_control_narrowing_is_refused():
    ids = [c[0] for c in K.CONTROL_CASES]
    q = K.qualify_controls(execution_ids=ids[:5])
    assert not q.passed and q.missing == ("near_null_hoverer",)
    with pytest.raises(K.ClassifyDomainError, match="unknown control"): K.qualify_controls(execution_ids=ids + ["bogus"])
    with pytest.raises(K.ClassifyDomainError, match="unknown control"): K.constructed_series("bogus", 0.125, 0.125)

def test_control_case_map_tamper_is_refused(monkeypatch):
    monkeypatch.setattr(K, "CONTROL_CASES", K.CONTROL_CASES[:5])
    with pytest.raises(K.ClassifyDomainError, match="digest"): K.qualify_controls()
    monkeypatch.undo()
    stale = K.CONTROL_CASES[:5] + ((K.CONTROL_CASES[5][0], K.CONTROL_CASES[5][1], K.CONTROL_CASES[5][2], K.CONTROL_CASES[5][3], K.CONTROL_CASES[5][4], "SUSTAINED"),)
    monkeypatch.setattr(K, "CONTROL_CASES", stale); monkeypatch.setattr(K, "CONTROL_CASES_SHA256_LITERAL", K.controls_digest())   # joint tamper
    q = K.qualify_controls()
    assert not q.passed and q.results[5][1] == "SUSTAINED" and q.results[5][2] == "NO_SUSTAINED"   # the definitions still decide

def test_precedence_boundary_conventions():
    th = float(np.float64(300) / np.float64(2500))                                   # the hoverer's grid value, 0.12
    r, *_ = K.constructed_series("near_null_hoverer", th, th, hover_count=300)
    assert K.run_status(r, th, th)[0] == "NO_SUSTAINED"                             # S_min == θ_P is NOT sustained; S_term == θ_T IS null
    assert K.run_status(r, np.nextafter(th, 0.0), th)[0] == "SUSTAINED"             # strictly above θ_P
    assert K.run_status(r, th, np.nextafter(th, 0.0))[0] == "UNRESOLVED"            # neither earned

def test_classifier_domain_refusals():
    with pytest.raises(K.ClassifyDomainError): K.tail_stats(np.zeros(2999))
    with pytest.raises(K.ClassifyDomainError): K.tail_stats(np.zeros(3000, np.float32))
    with pytest.raises(K.ClassifyDomainError): K.tail_stats(np.full(3000, 1.5))
    with pytest.raises(K.ClassifyDomainError): K.run_status(np.zeros(3000), np.array(0.1), 0.1)
    with pytest.raises(K.ClassifyDomainError): K.run_status(np.zeros(3000), 0.1, 1)

def test_level_label_is_total_and_exclusive_over_all_count_triples():
    """Every (n_sus, n_no, n_unr) summing to 20 maps to exactly one label; S and N never co-hold."""
    seen = {}
    for n_sus in range(21):
        for n_no in range(21 - n_sus):
            c = K.LevelCounts(n_sus, n_no, 20 - n_sus - n_no)
            lab = K.level_label(c); seen[(n_sus, n_no)] = lab
            s_rule = n_sus >= 16 and n_no <= 2; n_rule = n_no >= 16 and n_sus <= 2; m_rule = n_sus >= 4 and n_no >= 4
            assert not (s_rule and n_rule) and lab == ("S" if s_rule else "N" if n_rule else "M" if m_rule else "U")
    assert set(seen.values()) == {"S", "N", "M", "U"} and len(seen) == 231

def test_level_counts_from_statuses():
    c = K.level_counts(["SUSTAINED"] * 17 + ["NO_SUSTAINED"] * 2 + ["UNRESOLVED"])
    assert (c.n_sus, c.n_no, c.n_unr) == (17, 2, 1) and K.level_label(c) == "S"
    with pytest.raises(K.ClassifyDomainError): K.level_counts(["SUSTAINED"] * 19)

@pytest.mark.parametrize("bad", [K.LevelCounts(16, -1, 5), K.LevelCounts(16, 2.0, 2), K.LevelCounts(True, 16, 3),
                                 K.LevelCounts(21, 0, -1), K.LevelCounts(np.float64(16.0), 2, 2), K.LevelCounts(16, 2, 2.5)])
def test_level_label_refuses_impossible_counts(bad):
    with pytest.raises(K.ClassifyDomainError):
        K.level_label(bad)

def _by_seed(seq):
    return {s: st for s, st in zip(C.E1_SEED_PANEL, seq)}

def test_bootstrap_is_descriptive_seed_keyed_and_pairing_respecting():
    st = {"0.150000": _by_seed(["NO_SUSTAINED"] * 20), "0.500000": _by_seed(["SUSTAINED"] * 10 + ["NO_SUSTAINED"] * 10)}
    iv = K.seed_bootstrap_intervals(st, analysis_seed=1, n_resamples=200)
    assert iv["0.150000"]["no_sustained"] == (1.0, 1.0) and 0.0 < iv["0.500000"]["sustained"][0] < 0.5 < iv["0.500000"]["sustained"][1] < 1.0
    assert K.level_label(K.level_counts(list(st["0.500000"].values()))) == "M"        # labels are functions of counts alone
    src = open(K.__file__, encoding="utf-8").read()
    assert "seed_bootstrap_intervals" not in src.split("def level_label")[1].split("def seed_bootstrap")[0]

def test_bootstrap_refuses_malformed_inputs_typed():
    good = {"0.150000": _by_seed(["NO_SUSTAINED"] * 20)}
    with pytest.raises(K.ClassifyDomainError, match="unknown run status"): K.seed_bootstrap_intervals({"x": _by_seed(["BOGUS"] * 20)}, 1, 10)
    with pytest.raises(K.ClassifyDomainError, match="analysis_seed"): K.seed_bootstrap_intervals(good, -1, 10)
    with pytest.raises(K.ClassifyDomainError, match="analysis_seed"): K.seed_bootstrap_intervals(good, True, 10)
    with pytest.raises(K.ClassifyDomainError, match="n_resamples"): K.seed_bootstrap_intervals(good, 1, 0)
    with pytest.raises(K.ClassifyDomainError, match="n_resamples"): K.seed_bootstrap_intervals(good, 1, 2.0)
    with pytest.raises(K.ClassifyDomainError, match="nonempty"): K.seed_bootstrap_intervals({}, 1, 10)
    bad_panel = {s + 1: st for s, st in good["0.150000"].items()}                     # permuted / off-panel identities
    with pytest.raises(K.ClassifyDomainError, match="frozen seed panel"): K.seed_bootstrap_intervals({"x": bad_panel}, 1, 10)
    short = dict(list(good["0.150000"].items())[:19])
    with pytest.raises(K.ClassifyDomainError, match="frozen seed panel"): K.seed_bootstrap_intervals({"x": short}, 1, 10)
    with pytest.raises(K.ClassifyDomainError): K.seed_bootstrap_intervals({"x": ["NO_SUSTAINED"] * 20}, 1, 10)   # positional, not keyed


# ======================= round-3 additions (L2 M1/M2 round-2 review) =======================
def test_m1_declaration_live_global_divergence_on_sweep_is_refused(monkeypatch):
    """Declaration digest AND declaration both updated to a narrowed level list; the live global unchanged:
    the direct declaration-to-live comparison refuses (not only the rule check)."""
    decl = list(C.E1_DECLARATION); i = [k for k, (n, _) in enumerate(decl) if n == "levels_micro"][0]
    decl[i] = ("levels_micro", C.E1_LEVELS_MICRO[:23]); decl = tuple(decl)
    monkeypatch.setattr(C, "E1_DECLARATION", decl); monkeypatch.setattr(C, "E1_DECLARATION_SHA256_LITERAL", C.frozen_digest(decl))
    with pytest.raises(C.E1ConfigError, match="levels_micro"): C.verify_frozen_identity()
    with pytest.raises(C.E1ConfigError): C.e1_run_config(C.E1_LEVELS_MICRO[0], C.E1_SEED_PANEL[0])

def test_m1_joint_tamper_of_seed_master_and_panel_is_refused(monkeypatch):
    monkeypatch.setattr(C, "E1_SEED_PANEL_MASTER", 1)
    new_panel = C.generate_seed_panel(1); monkeypatch.setattr(C, "E1_SEED_PANEL", new_panel)
    monkeypatch.setattr(C, "E1_SEED_PANEL_SHA256_LITERAL", C.frozen_digest(new_panel))
    with pytest.raises(C.E1ConfigError): C.verify_frozen_identity()                      # hard contract value 20260917 refuses

def test_m1_constants_field_set_must_match_declaration(monkeypatch):
    monkeypatch.setattr(C, "E1_CONSTANTS_EXPECTED", C.E1_CONSTANTS_EXPECTED[:-1])
    decl = tuple((n, C.E1_CONSTANTS_EXPECTED if n == "constants" else v) for n, v in C.E1_DECLARATION)
    monkeypatch.setattr(C, "E1_DECLARATION", decl); monkeypatch.setattr(C, "E1_DECLARATION_SHA256_LITERAL", C.frozen_digest(decl))
    with pytest.raises(C.E1ConfigError, match="field set"): C.verify_frozen_identity()

def test_run_level_run_verifies_declaration_at_entry(monkeypatch, tmp_path):
    cfg = C.e1_run_config(C.E1_LEVELS_MICRO[12], 7, grid=16, ticks=12)
    monkeypatch.setattr(C, "E1_DECLARATION_SHA256_LITERAL", "0" * 64)
    with pytest.raises(C.E1ConfigError, match="digest"): C.run_level_run(cfg, str(tmp_path), "stale")
    assert not os.listdir(tmp_path)                                                       # nothing executed or written

def test_non_integral_seed_refused():
    with pytest.raises(C.E1ConfigError, match="exact non-Boolean integer"): C.e1_run_config(500000, 7.0, grid=16, ticks=12)
    with pytest.raises(C.E1ConfigError, match="exact non-Boolean integer"): C.e1_run_config(500000, True, grid=16, ticks=12)

def test_conformance_reruns_tier1_on_current_artifacts(small_run, tmp_path):
    """The stored verifier Boolean is true; the CURRENT rho table is altered post-run: conformance must fail
    through the rerun, and the base-identity verifier still passes (the mutation is outside its surface)."""
    import dataclasses, pandas as pd, shutil
    cfg, run = small_run
    rt = tmp_path / "rho.parquet"; shutil.copy(run.rho_table_path, rt)
    df = pd.read_parquet(rt); k = round(float(df.loc[3, "rho_global"]) * cfg.n_cells)
    df.loc[3, "rho_global"] = float(np.float64((k + 1) % cfg.n_cells) / np.float64(cfg.n_cells)); df.to_parquet(rt, index=False)   # on-grid, one count off
    tampered = dataclasses.replace(run, rho_table_path=str(rt))
    rep = C.conformance_preflight(tampered, cfg)
    # the stored Boolean is stale-true; the base-identity verifier is blind to rho; the Tier-1 rerun is also blind
    # to rho VALUES under a Q-disabled config (finding of record) — conformance's own value check catches it.
    assert tampered.verifier_passed is True and rep.checks["e1_base_bit_identity_verifier"] is True
    assert rep.checks["rho_table_values_match_row_states"] is False and rep.detail["rho_table_value_check"]["mismatched_ticks"] == [3] and not rep.passed
    # and a mutation Tier-1 DOES see (a dropped tick) fails the rerun regardless of the stored Boolean
    df2 = pd.read_parquet(run.rho_table_path).iloc[:-1]; rt2 = tmp_path / "rho2.parquet"; df2.to_parquet(rt2, index=False)
    rep2 = C.conformance_preflight(dataclasses.replace(run, rho_table_path=str(rt2)), cfg)
    assert rep2.checks["tier1_verifier_rerun_passed"] is False

def test_conformance_binds_levelrun_identity(small_run):
    import dataclasses
    cfg, run = small_run
    rep = C.conformance_preflight(dataclasses.replace(run, seed=run.seed + 1), cfg)
    assert rep.checks["levelrun_identity_bound"] is False and not rep.passed
    rep = C.conformance_preflight(dataclasses.replace(run, level_id="0.999999"), cfg)
    assert rep.checks["levelrun_identity_bound"] is False

def test_m2_live_tail_drift_against_declaration_is_refused(monkeypatch):
    monkeypatch.setattr(K, "TAIL_START", 1900); monkeypatch.setattr(K, "TAIL_END", 2899); monkeypatch.setattr(K, "RUN_LEN", 2900)   # arithmetic preserved
    with pytest.raises(K.ClassifyDomainError, match="tail"): K.verify_frozen_identity()
    monkeypatch.undo()
    monkeypatch.setattr(K, "STATUSES", ("SUSTAINED", "NO_SUSTAINED", "OTHER"))
    with pytest.raises(K.ClassifyDomainError, match="statuses"): K.verify_frozen_identity()

def test_bootstrap_refuses_non_integral_seed_keys():
    ok = {s: "SUSTAINED" for s in C.E1_SEED_PANEL}
    bad = {float(s): "SUSTAINED" for s in C.E1_SEED_PANEL}
    with pytest.raises(K.ClassifyDomainError): K.seed_bootstrap_intervals({"0.150000": bad}, analysis_seed=1, n_resamples=50)
    K.seed_bootstrap_intervals({"0.150000": ok}, analysis_seed=1, n_resamples=50)

def test_frozen_control_numeric_expectation_is_independent_of_generator(monkeypatch):
    """A generator defect that changes stable_above_null's level from 1250 to 1875: its own exact answer
    moves with it, M2 agrees with the moved series, but the FROZEN rational (1/2) does not — refused."""
    real = K.constructed_series
    def defective(kind, tp, tt, **kw):
        r, intended, smin, sterm = real(kind, tp, tt, **kw)
        if kind == "stable_above_null":
            r = r.copy(); r[K.TAIL_START:] = np.float64(1875) / np.float64(K.N_CELLS)
            from fractions import Fraction as F
            smin = sterm = F(3, 4)
        return r, intended, smin, sterm
    monkeypatch.setattr(K, "constructed_series", defective)
    q = K.qualify_controls()
    assert not q.passed and [r for r in q.results if r[0] == "stable_above_null"][0][3] is False

def test_duplicate_control_ids_refused():
    ids = [c for c, *_ in K.CONTROL_CASES]
    with pytest.raises(K.ClassifyDomainError, match="duplicate"): K.qualify_controls(execution_ids=ids + [ids[0]])

def test_control_parameter_keys_are_exact():
    with pytest.raises(K.ClassifyDomainError, match="parameter keys"): K.constructed_series("stable_above_null", 0.12, 0.12, hover_count=300)
    with pytest.raises(K.ClassifyDomainError, match="parameter keys"): K.constructed_series("near_null_hoverer", 0.12, 0.12)

def test_tail_stats_are_count_grid_exact_and_refuse_off_grid():
    r = np.zeros(3000); r[2000:] = np.float64(1250) / np.float64(2500)
    st = K.tail_stats(r); assert st.s_min == 0.5 and st.s_term == 0.5
    r[2500] = 0.3333
    with pytest.raises(K.ClassifyDomainError, match="count grid"): K.tail_stats(r)


# ======================= round-4 additions (L2 round-3 review, M1-6) =======================
def _rho_variant(run, tmp_path, fn, name):
    import dataclasses, pandas as pd
    df = pd.read_parquet(run.rho_table_path); df = fn(df); pth = tmp_path / f"{name}.parquet"; df.to_parquet(pth, index=False)
    return dataclasses.replace(run, rho_table_path=str(pth))

def test_rho_table_tick0_is_reconstructed_from_initialization_replay(small_run, tmp_path):
    import numpy as np
    cfg, run = small_run
    rep = C.conformance_preflight(run, cfg)
    d = rep.detail["rho_table_value_check"]
    assert rep.passed and d["tick0_matches_initialization_replay"] and d["initial_active_count"] == C.initial_active_count(cfg)
    n = cfg.n_cells
    bad = _rho_variant(run, tmp_path, lambda df: df.assign(rho_global=[float(np.float64((round(v * n) + 1) % n) / np.float64(n)) if i == 0 else v for i, v in enumerate(df["rho_global"])]), "tick0")
    rep = C.conformance_preflight(bad, cfg)
    assert not rep.passed and rep.detail["rho_table_value_check"]["tick0_matches_initialization_replay"] is False

@pytest.mark.parametrize("name,fn,key", [
    ("float_tick", lambda df: df.assign(Tick=df["Tick"].astype("float64")), "tick_dtype_integer"),
    ("float32_rho", lambda df: df.assign(rho_global=df["rho_global"].astype("float32")), "rho_dtype_float64"),
    ("nan_rho", lambda df: df.assign(rho_global=[float("nan") if i == 5 else v for i, v in enumerate(df["rho_global"])]), "no_null_or_nonfinite"),
    ("duplicate_row", lambda df: __import__("pandas").concat([df, df.iloc[[3]]], ignore_index=True), "row_count_exact"),
    ("out_of_order", lambda df: df.iloc[::-1].reset_index(drop=True), "tick_order_exact"),
    ("extra_column", lambda df: df.assign(extra=1.0), "columns_exact"),
])
def test_rho_table_contract_negatives(small_run, tmp_path, name, fn, key):
    cfg, run = small_run
    rep = C.conformance_preflight(_rho_variant(run, tmp_path, fn, name), cfg)
    assert not rep.passed and rep.detail["rho_table_value_check"][key] is False
