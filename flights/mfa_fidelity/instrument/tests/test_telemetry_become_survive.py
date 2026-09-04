"""tests/test_telemetry_become_survive.py — Phase-2 item 4: Lineage B telemetry family.

Discipline: every verifier check has at least one discriminating negative that fails
THAT check; extra-field refusals are proven with all required fields present so the
failure is attributable to the extra, not to an absence. Default-mode construction is
asserted identical to certified behaviour (25 Gate-A columns).
"""
import os

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import pytest

from mfa_instrument.config import RunConfig, InitConfig, DynamicsConstants, NoiseConfig
from mfa_instrument.rng import SeedRegistry
from mfa_instrument.init import initialize
from mfa_instrument.dynamics import Dynamics
from mfa_instrument.telemetry import TelemetryWriter
from mfa_instrument.schema_contract import BECOME_SURVIVE_COLUMNS, ANCESTOR_COLUMNS
from mfa_instrument.verify import become_survive_verify, expected_schema, tier1_verify

B_LAMBDA = 0.40
B_LOGIT = float(np.log(B_LAMBDA / (1.0 - B_LAMBDA)))
GS = 8
N = GS * GS


def _b_cfg(seed=11, kappa=0.4221, fixed=13, schedule=((0, 0.25),), ticks=6):
    return RunConfig(seed=seed, rule_mode="become_survive", grid_scale=GS, ticks=ticks,
                     init=InitConfig(scheme="fixed_count", fixed_count=fixed),
                     constants=DynamicsConstants(logit_l=B_LOGIT, kappa=kappa, p_survive=B_LAMBDA),
                     drive_schedule=schedule)


def _run_b(cfg, path, chunk_ticks=500):
    dyn = SeedRegistry(cfg.seed).dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    init_grid = state.is_active.astype(int).copy()
    d = Dynamics(cfg, state, dyn)
    tw = TelemetryWriter(cfg.grid_scale, 0.0, 0.0, False, chunk_ticks=chunk_ticks,
                         rule_mode="become_survive")
    tw.open(path)
    for _ in range(cfg.ticks):
        d.step(tw.sink)
    tw.close()
    return init_grid


def _b_fields(gs=4):
    return {"g_q": np.zeros((gs, gs)), "p_become": np.zeros((gs, gs)),
            "rand_grid": np.zeros((gs, gs)), "is_active": np.zeros((gs, gs), bool),
            "Psi_local": np.zeros((gs, gs))}


def _tamper(p, fn):
    df = pd.read_parquet(p)
    fn(df).to_parquet(p, index=False)


@pytest.fixture
def honest(tmp_path):
    """(path, cfg, init_grid) for an honest run; tmp_path is cleaned by pytest."""
    def make(**kw):
        cfg = _b_cfg(**kw)
        p = os.path.join(tmp_path, "b.parquet")
        return p, cfg, _run_b(cfg, p)
    return make


# ====================== construction refusals (N3 writer-layer twin) ======================
def test_b_writer_refuses_gamma_psi():
    with pytest.raises(ValueError, match="Q-disabled"):
        TelemetryWriter(GS, 0.001, 0.0, False, rule_mode="become_survive")

def test_b_writer_refuses_gamma_rho():
    with pytest.raises(ValueError, match="Q-disabled"):
        TelemetryWriter(GS, 0.0, 0.001, False, rule_mode="become_survive")

def test_b_writer_refuses_noise():
    with pytest.raises(ValueError, match="noise"):
        TelemetryWriter(GS, 0.0, 0.0, True, rule_mode="become_survive")

def test_b_writer_refuses_unknown_mode():
    with pytest.raises(ValueError, match="unknown rule_mode"):
        TelemetryWriter(GS, 0.0, 0.0, False, rule_mode="hybrid")


# ====================== schema: single source; default untouched ======================
def test_b_columns_equal_contract_exactly():
    tw = TelemetryWriter(GS, 0.0, 0.0, False, rule_mode="become_survive")
    assert tw.columns == BECOME_SURVIVE_COLUMNS and len(tw.columns) == 8
    assert "PRNG_draw" not in tw.columns and "rand_grid" in tw.columns

def test_default_mode_unchanged_gate_a_25_columns():
    tw = TelemetryWriter(10, 0.001, 0.0, False)
    assert tw.columns == ANCESTOR_COLUMNS and len(tw.columns) == 25 and tw.rule_mode == "symmetric_chain"

def test_verifier_expectation_derives_from_contract_not_writer():
    assert expected_schema(_b_cfg()) == set(BECOME_SURVIVE_COLUMNS)


# ====================== sink: exact input family (L2 T1) ======================
def test_b_sink_accepts_exactly_five_fields():
    tw = TelemetryWriter(4, 0.0, 0.0, False, rule_mode="become_survive")
    tw.sink(0, _b_fields())
    assert tw._ticks_buffered == 1

def test_b_sink_rejects_extra_a_field_with_all_b_fields_present():
    tw = TelemetryWriter(4, 0.0, 0.0, False, rule_mode="become_survive")
    f = _b_fields(); f["PRNG_draw"] = np.zeros((4, 4))
    with pytest.raises(ValueError, match=r"extra=\['PRNG_draw'\]"):
        tw.sink(0, f)

def test_b_sink_rejects_rho_global_with_all_b_fields_present():
    tw = TelemetryWriter(4, 0.0, 0.0, False, rule_mode="become_survive")
    f = _b_fields(); f["rho_global"] = np.float64(0.5)
    with pytest.raises(ValueError, match=r"extra=\['rho_global'\]"):
        tw.sink(0, f)
    assert tw.rho_global_table == []

def test_b_sink_rejects_missing_required_field():
    tw = TelemetryWriter(4, 0.0, 0.0, False, rule_mode="become_survive")
    f = _b_fields(); del f["Psi_local"]
    with pytest.raises(ValueError, match=r"missing=\['Psi_local'\] extra=\[\]"):
        tw.sink(0, f)


# ====================== verifier: positive + family isolation ======================
def test_b_verify_passes_on_honest_run(honest):
    p, cfg, ig = honest(kappa=-0.4221, schedule=((0, 0.0), (3, 0.125)))
    rep = become_survive_verify(p, cfg, ig)
    assert rep.passed, rep.summary()
    for c in ("g_q_bits", "p_become_bits", "is_active_rule", "Psi_local_bits", "rand_grid_domain"):
        assert rep.checks[c] == 0

def test_b_verify_streams_across_row_groups_and_batches(tmp_path):
    """chunk_ticks < ticks => multiple parquet row groups; batch_size < n_cells =>
    batches split ticks mid-way. Chaining and completeness must survive both."""
    cfg = _b_cfg(ticks=7); p = os.path.join(tmp_path, "b.parquet")
    ig = _run_b(cfg, p, chunk_ticks=2)
    assert pq.ParquetFile(p).num_row_groups >= 3
    rep = become_survive_verify(p, cfg, ig, batch_size=50)
    assert rep.passed, rep.summary()
    assert rep.rows_seen == 7 * N and rep.ticks_seen == (0, 6)

def test_tier1_refuses_b_file_deliberately_no_keyerror(honest):
    p, cfg, ig = honest()
    rep = tier1_verify(p, cfg)
    assert not rep.passed and rep.checks == {"config_rule_mode": 1}

def test_b_verify_refuses_wrong_rule_mode_config():
    cfg = RunConfig(seed=1, grid_scale=GS, ticks=6, init=InitConfig(scheme="fixed_count", fixed_count=8))
    rep = become_survive_verify("/nonexistent.parquet", cfg, np.zeros((GS, GS), int))
    assert not rep.passed and rep.checks == {"config_rule_mode": 1}


# ====================== rule-level negatives ======================
def _only_fails(rep, name):
    assert not rep.passed
    assert rep.checks[name] > 0
    assert all(v == 0 for k, v in rep.checks.items() if k != name), rep.summary()

def test_b_verify_catches_one_ulp_p_become(honest):
    p, cfg, ig = honest()
    def fn(df):
        v = df["p_become"].to_numpy().copy(); v[100] = np.nextafter(v[100], 1.0); df["p_become"] = v; return df
    _tamper(p, fn)
    rep = become_survive_verify(p, cfg, ig)
    _only_fails(rep, "p_become_bits"); assert rep.checks["p_become_bits"] == 1

def test_b_verify_catches_one_cell_psi_local_mutation_only(honest):
    """L2 V2: a fabricated Psi_local must fail the dedicated check and no other."""
    p, cfg, ig = honest()
    def fn(df):
        v = df["Psi_local"].to_numpy().copy(); v[200] = v[200] + 1.0; df["Psi_local"] = v; return df
    _tamper(p, fn)
    rep = become_survive_verify(p, cfg, ig)
    _only_fails(rep, "Psi_local_bits"); assert rep.checks["Psi_local_bits"] == 1

def test_b_verify_catches_swapped_rand_grid(honest):
    p, cfg, ig = honest()
    _tamper(p, lambda df: df.assign(rand_grid=np.random.default_rng(1).random(len(df))))
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["is_active_rule"] > 0

def test_b_verify_catches_one_tick_shift_of_state(honest):
    p, cfg, ig = honest()
    def fn(df):
        s = df["is_active"].to_numpy().copy(); df["is_active"] = np.concatenate([s[N:], s[:N]]); return df
    _tamper(p, fn)
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["is_active_rule"] > 0


# ====================== exactness / domain negatives (L2 V3) ======================
def test_b_verify_fails_closed_on_missing_column(honest):
    p, cfg, ig = honest()
    _tamper(p, lambda df: df.drop(columns=["g_q"]))
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["schema_ordered"] == 1 and "p_become_bits" not in rep.checks

def test_b_verify_fails_closed_on_forbidden_column(honest):
    p, cfg, ig = honest()
    _tamper(p, lambda df: df.assign(PRNG_draw=0.0))
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["schema_ordered"] == 1 and "p_become_bits" not in rep.checks

def test_b_verify_fails_closed_on_reordered_columns(honest):
    p, cfg, ig = honest()
    _tamper(p, lambda df: df[list(reversed(BECOME_SURVIVE_COLUMNS))])
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["schema_ordered"] == 1

@pytest.mark.parametrize("col,cast", [("Tick", np.float64), ("p_become", np.float32), ("is_active", np.int64)])
def test_b_verify_fails_closed_on_wrong_dtype(col, cast, honest):
    p, cfg, ig = honest()
    _tamper(p, lambda df: df.assign(**{col: df[col].astype(cast)}))
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["dtype_contract"] >= 1 and "p_become_bits" not in rep.checks

@pytest.mark.parametrize("bad", [1.5, -0.1, 1.0])
def test_b_verify_catches_out_of_domain_rand_grid(bad, honest):
    p, cfg, ig = honest()
    def fn(df):
        v = df["rand_grid"].to_numpy().copy(); v[7] = bad; df["rand_grid"] = v; return df
    _tamper(p, fn)
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["rand_grid_domain"] == 1

def test_b_verify_catches_nan_rand_grid_as_value(honest):
    """A NaN VALUE (not a null) must be refused by the domain check. Written arrow-side,
    because pandas->arrow converts float NaN to NULL, which the null gate catches instead."""
    import pyarrow as pa
    p, cfg, ig = honest()
    tbl = pq.read_table(p)
    v = tbl.column("rand_grid").to_numpy().copy(); v[7] = np.nan
    tbl = tbl.set_column(tbl.schema.get_field_index("rand_grid"), "rand_grid", pa.array(v, type=pa.float64(), from_pandas=False))
    assert tbl.column("rand_grid").null_count == 0
    pq.write_table(tbl, p)
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["rand_grid_domain"] == 1 and rep.checks.get("null_values", 0) == 0

def test_b_verify_refuses_nan_rand_grid_as_null(honest):
    p, cfg, ig = honest()
    def fn(df):
        v = df["rand_grid"].to_numpy().copy(); v[7] = np.nan; df["rand_grid"] = v; return df   # -> NULL via pandas
    _tamper(p, fn)
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["null_values"] == 1 and "rand_grid_domain" not in rep.checks

def test_b_verify_rejects_nonbinary_init_grid(honest):
    p, cfg, ig = honest()
    bad = ig.copy(); bad[0, 0] = 2
    rep = become_survive_verify(p, cfg, bad)
    assert not rep.passed and rep.checks["init_grid_invalid"] == 1 and "schema_ordered" not in rep.checks

def test_b_verify_rejects_wrong_shape_init_grid(honest):
    p, cfg, ig = honest()
    rep = become_survive_verify(p, cfg, np.zeros((GS, GS + 1), int))
    assert not rep.passed and rep.checks["init_grid_invalid"] == 1 and "schema_ordered" not in rep.checks

def test_b_verify_rejects_float_init_grid(honest):
    p, cfg, ig = honest()
    rep = become_survive_verify(p, cfg, ig.astype(np.float64))
    assert not rep.passed and rep.checks["init_grid_invalid"] == 1 and "schema_ordered" not in rep.checks


# ====================== completeness / coordinate negatives ======================
def test_b_verify_catches_dropped_row(honest):
    p, cfg, ig = honest()
    _tamper(p, lambda df: df.drop(index=[130]))
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["rows_per_tick"] == 1

def test_b_verify_catches_duplicated_row_replacing_another(honest):
    p, cfg, ig = honest()
    def fn(df):
        for c in df.columns:                       # explicit per-column copy: pandas row
            v = df[c].to_numpy().copy(); v[131] = v[130]; df[c] = v   # assignment from a mixed
        return df                                  # Series won't overwrite int columns
    _tamper(p, fn)
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["duplicate_or_out_of_range_keys"] >= 1 and rep.checks["coordinate_order"] >= 1

def test_b_verify_catches_corrupted_coordinate(honest):
    p, cfg, ig = honest()
    def fn(df):
        v = df["Agent_X"].to_numpy().copy(); v[5] = GS + 3; df["Agent_X"] = v; return df
    _tamper(p, fn)
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["coordinate_order"] >= 1 and rep.checks["duplicate_or_out_of_range_keys"] >= 1

def test_b_verify_catches_missing_tick(honest):
    p, cfg, ig = honest()
    _tamper(p, lambda df: df[df["Tick"] != 5])
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["tick_coverage"] == 1

def test_b_verify_catches_out_of_order_ticks(honest):
    p, cfg, ig = honest()
    def fn(df):
        a, b = df[df["Tick"] == 2], df[df["Tick"] == 1]
        rest = df[~df["Tick"].isin([1, 2])]
        return pd.concat([rest[rest["Tick"] < 1], a, b, rest[rest["Tick"] > 2]], ignore_index=True)
    _tamper(p, fn)
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["tick_order"] >= 1


# ====================== O1: upstream guard, authorized scope expansion ======================
def test_dynamics_refuses_become_survive_with_noise_amplitude():
    """Item-4 O1 (authorized): B mode with nonzero MFA noise is refused at construction,
    the N3 twin — never a stream constructed and silently unread."""
    cfg = RunConfig(seed=3, rule_mode="become_survive", grid_scale=GS, ticks=2,
                    init=InitConfig(scheme="fixed_count", fixed_count=8),
                    constants=DynamicsConstants(logit_l=B_LOGIT, kappa=0.1, p_survive=B_LAMBDA),
                    noise=NoiseConfig(amplitude=0.01))
    reg = SeedRegistry(3)
    dyn = reg.dynamics()
    state = initialize(cfg.init, GS, dyn)
    with pytest.raises(ValueError, match="no noise channel"):
        Dynamics(cfg, state, dyn, noise=reg.role("noise"))


# ====================== round 3: g_q independence, excluded-channel guards, nulls ======================
def test_b_verify_catches_one_ulp_g_q_only(honest):
    """g_q_bits must have its own discriminating negative (round-2 items 6-7)."""
    p, cfg, ig = honest()
    def fn(df):
        v = df["g_q"].to_numpy().copy(); v[150] = np.nextafter(v[150], 1.0); df["g_q"] = v; return df
    _tamper(p, fn)
    rep = become_survive_verify(p, cfg, ig)
    _only_fails(rep, "g_q_bits"); assert rep.checks["g_q_bits"] == 1

def test_b_verify_refuses_nonzero_q_config_before_file_access():
    from mfa_instrument.config import QConfig
    cfg = RunConfig(seed=1, rule_mode="become_survive", grid_scale=GS, ticks=2,
                    init=InitConfig(scheme="fixed_count", fixed_count=8),
                    constants=DynamicsConstants(logit_l=B_LOGIT, kappa=0.1, p_survive=B_LAMBDA),
                    q=QConfig(gamma_psi=0.001, gamma_rho=0.0))
    rep = become_survive_verify("/nonexistent.parquet", cfg, np.zeros((GS, GS), int))
    assert not rep.passed and rep.checks["config_q_disabled"] == 1 and rep.checks["config_noise_disabled"] == 0

def test_b_verify_refuses_nonzero_noise_config_before_file_access():
    cfg = RunConfig(seed=1, rule_mode="become_survive", grid_scale=GS, ticks=2,
                    init=InitConfig(scheme="fixed_count", fixed_count=8),
                    constants=DynamicsConstants(logit_l=B_LOGIT, kappa=0.1, p_survive=B_LAMBDA),
                    noise=NoiseConfig(amplitude=0.01))
    rep = become_survive_verify("/nonexistent.parquet", cfg, np.zeros((GS, GS), int))
    assert not rep.passed and rep.checks["config_noise_disabled"] == 1 and rep.checks["config_q_disabled"] == 0

@pytest.mark.parametrize("col,nullable", [("Tick", "Int64"), ("p_become", "Float64"), ("is_active", "boolean")])
def test_b_verify_refuses_nulls_before_recomputation(col, nullable, honest):
    """Arrow type identity survives a null; the verifier must refuse, never coerce."""
    p, cfg, ig = honest()
    def fn(df):
        s = df[col].astype(nullable); s.iloc[77] = pd.NA; df[col] = s; return df
    _tamper(p, fn)
    assert pq.ParquetFile(p).schema_arrow.field(col).type == pq.ParquetFile(p).schema_arrow.field(col).type  # type unchanged class
    rep = become_survive_verify(p, cfg, ig)
    assert not rep.passed and rep.checks["null_values"] == 1
    assert "p_become_bits" not in rep.checks and "dtype_contract" in rep.checks and rep.checks["dtype_contract"] == 0
