"""Telemetry + provisional Gate A. The Gate-A test imports the ACTUAL ancestor file
from the pinned clone — the strongest available discriminator short of the
authoritative run on the execution machine."""
import sys, os, tempfile
import numpy as np
import pandas as pd
import pytest

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.telemetry import TelemetryWriter, telemetry_digest, ANCESTOR_COLUMNS
from mfa_instrument.gates.gate_a import run_gate_a, gate_a_config, structural_preflight

# Item 2 (L2 closure review): the pinned ancestor repository is an EXPLICIT
# integration dependency, supplied by the invoking environment — never a
# machine-specific constant. Canonical invocation exports MFA_PINNED_REPO_ROOT.
REPO = os.environ.get("MFA_PINNED_REPO_ROOT")
requires_pinned_repo = pytest.mark.skipif(
    REPO is None, reason="MFA_PINNED_REPO_ROOT not set: pinned-ancestor integration "
                         "tests require the 4d9a622 clone path")

def test_gate_a_schema_is_exactly_ancestor_25():
    tw = TelemetryWriter(10, 0.001, 0.0, False)
    assert tw.columns == ANCESTOR_COLUMNS and len(tw.columns) == 25

def test_e1_schema_drops_q_columns():
    tw = TelemetryWriter(10, 0.0, 0.0, False)
    for c in ("gamma_coef", "Delta_v", "Delta_u", "Delta_r", "Delta_from_rho"):
        assert c not in tw.columns

def test_rho_schema_adds_decomposition():
    tw = TelemetryWriter(10, 0.0, 0.01, False)
    assert "Delta_from_Psi" in tw.columns and "Delta_from_rho" in tw.columns

def test_digest_canonical_construction():
    with tempfile.TemporaryDirectory() as td:
        a, b = os.path.join(td, "b.parquet"), os.path.join(td, "a.parquet")
        open(a, "wb").write(b"BBB"); open(b, "wb").write(b"AAA")
        d1 = telemetry_digest([a, b])
        d2 = telemetry_digest([b, a])          # order-insensitive input, filename-sorted
        assert d1 == d2
        import hashlib
        h = hashlib.sha256()
        h.update(b"a.parquet\n"); h.update(b"AAA")
        h.update(b"b.parquet\n"); h.update(b"BBB")
        assert d1 == h.hexdigest()             # exact spec construction

def test_gate_a_rejects_f_canonical():
    with pytest.raises(ValueError):
        gate_a_config("F_canonical", 10, 5)

def test_structural_preflight_passes():
    rep = structural_preflight(gate_a_config("F_2_symmetric", 8, 3))
    assert rep.passed, rep.checks

@requires_pinned_repo
@pytest.mark.parametrize("f_form", ["F_2_symmetric", "F_LR", "F_baseline"])
def test_provisional_gate_a_against_actual_ancestor(f_form):
    rep = run_gate_a(REPO, f_form, grid_scale=12, ticks=25, label="PROVISIONAL")
    assert rep.preflight.passed, rep.preflight.checks
    assert rep.state_bit_exact, rep.summary()
    assert rep.telemetry_bit_exact, rep.summary()

def test_parquet_roundtrip_and_rho_table():
    from mfa_instrument.config import RunConfig, QConfig
    from mfa_instrument.rng import SeedRegistry
    from mfa_instrument.init import initialize
    from mfa_instrument.dynamics import Dynamics
    cfg = RunConfig(seed=3, f_dispatch="F_canonical", grid_scale=6, ticks=10,
                    q=QConfig(q_read="global", gamma_psi=0.0, gamma_rho=0.01))
    dyn = SeedRegistry(3).dynamics()
    d = Dynamics(cfg, initialize(cfg.init, 6, dyn), dyn)
    tw = TelemetryWriter(6, 0.0, 0.01, False, chunk_ticks=4)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw.open(p)
        for _ in range(10):
            d.step(tw.sink)
        tw.close()
        df = pd.read_parquet(p)
        assert len(df) == 10 * 36 and tw.rows_written == 360
        assert len(tw.rho_global_table) == 10       # tick-level table, one row per tick
        assert "Delta_from_rho" in df.columns
        # realization invariant holds on the written file
        assert bool((df["is_active"] == (df["PRNG_draw"] < df["p_act"])).all())


def test_raw_bit_comparator_rejects_signed_zero():
    """Item 1 negative test: np.array_equal accepts what the Gate-A comparator must
    reject — the comparator, not numeric equality, earns the BIT-EXACT claim."""
    from mfa_instrument.gates.gate_a import raw_bit_equal
    a = np.array([0.0, 1.5]); b = np.array([-0.0, 1.5])
    assert np.array_equal(a, b)              # numeric equality passes it
    assert not raw_bit_equal(a, b)           # raw storage rejects it
    assert not raw_bit_equal(a, a.astype(np.float32))   # dtype mismatch rejected
    assert raw_bit_equal(a, a.copy())

def test_authoritative_requires_frozen_digest_supplied():
    from mfa_instrument.gates.gate_a import run_gate_a, ANCESTOR_SHA256
    assert isinstance(ANCESTOR_SHA256, str) and len(ANCESTOR_SHA256) == 64
