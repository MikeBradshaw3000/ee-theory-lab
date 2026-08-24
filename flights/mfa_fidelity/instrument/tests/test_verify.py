"""Tests for verify.py (V1-V5 rebuild) — negative matrix expanded per V7:
schema (missing/forbidden), completeness (empty/truncated/dropped/duplicated),
global-Q, rho_global artifact, Term_Offset, gamma_coef, raw-bit identity.
Path binding per V6: repo-relative via conftest-style pathing, no absolute L1 path."""
import os, sys, tempfile
import numpy as np
import pandas as pd
import pytest

# V6: repo-relative import — the package root is this test file's parent's parent.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.config import RunConfig, QConfig, InitConfig, DynamicsConstants
from mfa_instrument.rng import SeedRegistry
from mfa_instrument.init import initialize
from mfa_instrument.dynamics import Dynamics
from mfa_instrument.telemetry import TelemetryWriter
from mfa_instrument.verify import tier1_verify, e1_base_bit_identity, expected_schema

def run_to_parquet(cfg, path, emit_rho=False):
    reg = SeedRegistry(cfg.seed, gate_a_mode=(cfg.q.gamma_rho == 0.0 and not cfg.drive_schedule
                                              and cfg.noise.amplitude == 0.0 and not emit_rho))
    dyn = reg.dynamics()
    d = Dynamics(cfg, initialize(cfg.init, cfg.grid_scale, dyn), dyn, emit_rho_global=emit_rho)
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho,
                         cfg.noise.amplitude > 0, chunk_ticks=5)
    tw.open(path)
    for _ in range(cfg.ticks):
        d.step(tw.sink)
    tw.close()
    return tw

def gate_a_cfg(**kw):
    d = dict(seed=0x7A9B31C, f_dispatch="F_2_symmetric", grid_scale=8, ticks=12,
             q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    d.update(kw); return RunConfig(**d)

def test_tier1_passes_clean_run():
    cfg = gate_a_cfg()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = tier1_verify(p, cfg)
        assert rep.passed, rep.summary()
        assert rep.rows_seen == 12 * 64

def test_tier1_global_q_with_rho_artifact():
    """V2: global decomposition verified against the persisted tick table."""
    cfg = RunConfig(seed=9, f_dispatch="F_canonical", grid_scale=8, ticks=10,
                    q=QConfig(q_read="global", gamma_psi=0.001, gamma_rho=0.02))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw = run_to_parquet(cfg, p)
        assert tw.rho_global_path is not None            # N2: artifact persisted
        rep = tier1_verify(p, cfg, rho_global_path=tw.rho_global_path)
        assert rep.passed, rep.summary()
        # plant a wrong global decomposition value
        df = pd.read_parquet(p); df.loc[df.index[100], "Delta_from_rho"] += 1e-15
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep2 = tier1_verify(p2, cfg, rho_global_path=tw.rho_global_path)
        assert not rep2.passed and rep2.checks["delta_from_rho_global"] > 0

def test_tier1_missing_rho_artifact_fails():
    cfg = RunConfig(seed=9, f_dispatch="F_canonical", grid_scale=6, ticks=5,
                    q=QConfig(q_read="global", gamma_psi=0.0, gamma_rho=0.02))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = tier1_verify(p, cfg, rho_global_path=None)
        assert not rep.passed and rep.checks["rho_global_artifact_missing"] == 1

def test_tier1_e1_local_gate_r_rho_emission():
    """N1: E1 total-Q-disable run CAN emit rho_global as a Gate-R obligation."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=8,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw = run_to_parquet(cfg, p, emit_rho=True)
        assert tw.rho_global_path is not None
        rep = tier1_verify(p, cfg, rho_global_path=tw.rho_global_path,
                           expect_rho_global=True)
        assert rep.passed, rep.summary()

def test_tier1_schema_missing_column_fails():
    """V1: a run generated under active Q with a Q column REMOVED must fail."""
    cfg = gate_a_cfg()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p).drop(columns=["Delta_v"])
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep = tier1_verify(p2, cfg)
        assert not rep.passed and rep.checks["schema_missing_columns"] > 0

def test_tier1_schema_forbidden_column_fails():
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=4,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p); df["Delta_v"] = 0.0     # forbidden under total-disable
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep = tier1_verify(p2, cfg)
        assert not rep.passed and rep.checks["schema_forbidden_columns"] > 0

def test_tier1_empty_truncated_dropped_duplicated_fail():
    """V3: the completeness matrix."""
    cfg = gate_a_cfg(grid_scale=6, ticks=6)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        cases = {
            "empty": full.iloc[0:0],
            "dropped_tick": full[full.Tick != 3],
            "dropped_row": full.drop(index=full.index[77]),
            "duplicated_row": pd.concat([full, full.iloc[[50]]], ignore_index=True),
        }
        for name, df in cases.items():
            p2 = os.path.join(td, f"{name}.parquet"); df.to_parquet(p2)
            rep = tier1_verify(p2, cfg)
            assert not rep.passed, f"{name}: {rep.summary()}"

def test_tier1_catches_planted_value_defects():
    cfg = gate_a_cfg(f_dispatch="F_LR", grid_scale=8, ticks=6)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        for col, check, mut in [
            ("is_active", "realization_invariant", lambda x: not x),
            ("Lambda_total", "lambda_total_dispatch", lambda x: x + 1e-12),
            ("Drive_Raw", "drive_raw", lambda x: x + 1e-9),
            ("Term_Offset", "term_offset", lambda x: x + 1e-12),      # V5
            ("gamma_coef", "gamma_coef", lambda x: x + 1e-9),          # V5
            ("p_act", "p_act", lambda x: min(1.0, x + 1e-12)),
            ("Delta_v", "q_ancestor_expression", lambda x: x + 1e-15),
        ]:
            df = pd.read_parquet(p)
            df.loc[df.index[37], col] = mut(df.loc[df.index[37], col])
            p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
            rep = tier1_verify(p2, cfg)
            assert not rep.passed and rep.checks[check] > 0, (col, rep.summary())

def test_e1_bit_identity_true_bitwise():
    """V4: negative-zero substitution — numerically equal, bitwise different."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=8,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = e1_base_bit_identity(p, cfg)
        assert rep.passed, rep.summary()
        df = pd.read_parquet(p)
        # plant -0.0 over +0.0-like: force a value whose bits differ but compares ==
        idx = df[(df.Tick == 5)].index[3]
        orig = df.loc[idx, "b_i_v"]
        df.loc[idx, "b_i_v"] = np.nextafter(orig, np.inf)   # 1-ulp bit change
        p2 = os.path.join(td, "ulp.parquet"); df.to_parquet(p2)
        rep2 = e1_base_bit_identity(p2, cfg)
        assert not rep2.passed and rep2.checks["base_bit_identity"] == 1
        # negative-zero case, explicit
        df2 = pd.read_parquet(p)
        z_idx = df2.index[10]
        df2.loc[df2[df2.Tick == 0].index, "b_i_u"] = 0.0     # tick-0 baseline +0.0
        df2.loc[df2[(df2.Tick > 0)].index, "b_i_u"] = 0.0
        df2.loc[df2[(df2.Tick == 4)].index[7], "b_i_u"] = -0.0
        p3 = os.path.join(td, "negzero.parquet"); df2.to_parquet(p3)
        rep3 = e1_base_bit_identity(p3, cfg)
        assert rep3.checks["base_bit_identity"] >= 1        # == would have passed it

def test_e1_bit_identity_coverage_and_empty():
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=6,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        for name, df in {"empty": full.iloc[0:0],
                         "no_tick0": full[full.Tick != 0],
                         "truncated": full[full.Tick < 4]}.items():
            p2 = os.path.join(td, f"{name}.parquet"); df.to_parquet(p2)
            rep = e1_base_bit_identity(p2, cfg)
            assert not rep.passed, (name, rep.summary())

def test_e1_bit_identity_rejects_all_q_columns():
    """V4: decomposition columns also forbidden under total-Q-disable."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=3,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p); df["Delta_from_rho"] = 0.0
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep = e1_base_bit_identity(p2, cfg)
        assert not rep.passed and rep.checks["schema_absent_Delta_from_rho"] == 1

def test_become_survive_no_base_draws_policy():
    """D2 (config-bound): deterministic_level consumes no base draws; the NEXT
    generator output after init coincides with a shadow's post-permutation draw."""
    gs = 6
    cfg = RunConfig(seed=11, rule_mode="become_survive", grid_scale=gs,
                    init=InitConfig(scheme="fixed_count", fixed_count=9,
                                    base_init_mode="deterministic_level"),
                    constants=DynamicsConstants(logit_l=-0.405465, kappa=0.2, p_survive=0.4))
    dyn = SeedRegistry(11).dynamics()
    state = initialize(cfg.init, gs, dyn)
    assert np.all(state.v == cfg.init.m) and state.v.dtype == np.float64
    shadow = np.random.default_rng(11)
    ref = shadow.permutation(gs * gs)
    expect = np.zeros(gs * gs, dtype=bool); expect[ref[:9]] = True
    assert np.array_equal(state.is_active.reshape(-1), expect)
    assert np.array_equal(dyn.generator.random(16), shadow.random(16))

def test_symmetric_chain_rejects_deterministic_level():
    with pytest.raises(Exception):
        RunConfig(seed=1, init=InitConfig(base_init_mode="deterministic_level"))

def test_become_survive_rejects_nonzero_q():
    """N3: silent ignoring foreclosed — construction raises."""
    cfg = RunConfig(seed=2, rule_mode="become_survive", grid_scale=6,
                    init=InitConfig(scheme="fixed_count", fixed_count=5,
                                    base_init_mode="deterministic_level"),
                    constants=DynamicsConstants(logit_l=-0.4, kappa=0.1, p_survive=0.4),
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    dyn = SeedRegistry(2).dynamics()
    with pytest.raises(ValueError):
        Dynamics(cfg, initialize(cfg.init, 6, dyn), dyn)

def test_dynamics_owns_private_copies():
    """D1(a): mutating the caller's GridState after construction changes nothing."""
    cfg = RunConfig(seed=3, f_dispatch="F_canonical", grid_scale=6, ticks=3,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    dyn = SeedRegistry(3).dynamics()
    state = initialize(cfg.init, 6, dyn)
    d = Dynamics(cfg, state, dyn)
    state.v[:] = 0.0                                      # hostile caller
    d.step()
    assert not np.any(d._v == 0.0)                        # terrain unaffected

def test_sink_cannot_alter_q_update():
    """D1(b): a hostile sink un-freezing and mutating Delta_v cannot change bases."""
    cfg = RunConfig(seed=4, f_dispatch="F_canonical", grid_scale=6, ticks=1,
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    def hostile(tick, fields):
        arr = fields["Delta_v"]
        arr.flags.writeable = True
        arr[:] = 99.0
    dyn = SeedRegistry(4).dynamics()
    d = Dynamics(cfg, initialize(cfg.init, 6, dyn), dyn)
    d.step(hostile)
    assert d._v.max() <= 1.0                              # clip would mask; check delta scale:
    dyn2 = SeedRegistry(4).dynamics()
    d2 = Dynamics(cfg, initialize(cfg.init, 6, dyn2), dyn2)
    d2.step()                                             # no sink
    assert np.array_equal(d._v, d2._v)                    # identical evolution


def _same_size_duplicate_for_missing(full, cfg, victim_pos, donor_pos):
    """Remove one legitimate row; duplicate another from the SAME tick: totals and
    per-tick counts unchanged — only exact key coverage can catch it."""
    df = full.drop(index=full.index[victim_pos]).reset_index(drop=True)
    donor = full.iloc[[donor_pos]]
    return pd.concat([df, donor], ignore_index=True)

def test_tier1_duplicate_for_missing_same_size_cross_batch():
    """Items 3+5: same-size substitution, copies forced into different batches by
    placing the duplicate at the frame's end (verifier batch_size splits them)."""
    cfg = gate_a_cfg(grid_scale=6, ticks=6)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        tick3 = full[full.Tick == 3]
        bad = _same_size_duplicate_for_missing(full, cfg, victim_pos=tick3.index[5],
                                               donor_pos=tick3.index[20])
        p2 = os.path.join(td, "bad.parquet"); bad.to_parquet(p2)
        rep = tier1_verify(p2, cfg, batch_size=100)   # duplicate pair spans batches
        assert not rep.passed
        assert rep.checks["row_duplication_or_range"] > 0
        assert rep.checks["key_coverage_complete"] == 1
        assert rep.checks["rows_total"] == 0          # the counting checks CANNOT catch it
        assert rep.checks["tick_coverage_exact"] == 0

def test_e1_duplicate_for_missing_unchanged_bits():
    """Items 4+5: the substitution preserves base bits (bases constant under E1),
    so base_bit_identity stays zero — structural coverage alone must fail it."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=6,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        tick4 = full[full.Tick == 4]
        bad = _same_size_duplicate_for_missing(full, cfg, victim_pos=tick4.index[2],
                                               donor_pos=tick4.index[9])
        p2 = os.path.join(td, "bad.parquet"); bad.to_parquet(p2)
        rep = e1_base_bit_identity(p2, cfg, batch_size=100)
        assert not rep.passed
        assert rep.checks["base_bit_identity"] == 0   # bits unchanged — as constructed
        assert rep.checks["row_duplication"] > 0
        assert rep.checks["key_coverage_complete"] == 1

def test_malformed_rho_schema_fails_closed():
    """Item 7: wrong columns => failed report returned, never an exception."""
    cfg = RunConfig(seed=9, f_dispatch="F_canonical", grid_scale=6, ticks=5,
                    q=QConfig(q_read="global", gamma_psi=0.0, gamma_rho=0.02))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw = run_to_parquet(cfg, p)
        bad_rho = os.path.join(td, "bad_rho.parquet")
        pd.DataFrame({"T": [0], "value": [0.5]}).to_parquet(bad_rho)
        rep = tier1_verify(p, cfg, rho_global_path=bad_rho)
        assert not rep.passed and rep.checks["rho_global_schema"] == 1


def test_e1_alias_coordinate_rejected():
    """Closure negative (L2 held-item): (-1, 6) on a 6x6 grid flattens to key 0,
    aliasing legal (0,0). Row and per-tick counts are preserved, so only independent
    coordinate validation (and the resulting key-coverage gap) can fail the file."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=6,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p)
        idx = df[(df.Tick == 3) & (df.Agent_X == 2) & (df.Agent_Y == 4)].index[0]
        df.loc[idx, "Agent_X"] = -1
        df.loc[idx, "Agent_Y"] = 6            # flattened: -1*6 + 6 = 0 => aliases (0,0)
        p2 = os.path.join(td, "alias.parquet"); df.to_parquet(p2)
        rep = e1_base_bit_identity(p2, cfg, batch_size=100)
        assert not rep.passed
        assert rep.checks["coordinate_range"] == 1
        assert rep.checks["key_coverage_complete"] == 1   # (3,2,4) now uncovered
        assert rep.checks["rows_total"] == 0              # counting checks cannot catch it
        assert rep.checks["tick_coverage_exact"] == 0

def test_e1_gross_coordinate_fails_closed():
    """Closure negative: grossly out-of-range coordinates yield a FAILED REPORT,
    never an indexing exception (fail-closed, matching the rho discipline)."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=4,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p)
        df.loc[df.index[7], "Agent_X"] = 9999
        df.loc[df.index[8], "Agent_Y"] = -777
        df.loc[df.index[9], "Tick"] = 10_000          # out-of-range tick too
        p2 = os.path.join(td, "gross.parquet"); df.to_parquet(p2)
        rep = e1_base_bit_identity(p2, cfg, batch_size=50)   # must not raise
        assert not rep.passed
        assert rep.checks["coordinate_range"] >= 2
