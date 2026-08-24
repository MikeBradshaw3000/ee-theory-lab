"""Tests for config.py and rng.py — Build Plan v0.2 first deliverables.
Pessimistic-on-passing: each test names what alternative it discriminates against."""
import dataclasses, json, sys
import numpy as np
import pytest

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.config import (RunConfig, DynamicsConstants, QConfig, InitConfig,
                                   NoiseConfig, ConfigError, as_micro_units, build_run_record)
from mfa_instrument.rng import SeedRegistry, RoleError, DynamicsStream, make_noise_stream

# ---- config: immutability (vs. silently mutable shared state) ----
def test_config_deeply_immutable():
    c = RunConfig(seed=5)
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.seed = 6
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.q.gamma_psi = 1.0

# ---- config: canonical serialization is stable and key-sorted ----
def test_canonical_json_stable_and_sorted():
    a = RunConfig(seed=5).canonical_json()
    b = RunConfig(seed=5).canonical_json()
    assert a == b and a.endswith("\n") and " " not in a.split('"label"')[0]
    keys = list(json.loads(a).keys())
    assert keys == sorted(keys)

def test_config_hash_changes_with_content():
    assert RunConfig(seed=5).config_hash() != RunConfig(seed=6).config_hash()

# ---- config: naming-ledger validation (vs. wrong-values-under-right-names) ----
def test_ledger_enums_enforced():
    with pytest.raises(ConfigError): RunConfig(seed=1, rule_mode="mesa")
    with pytest.raises(ConfigError): RunConfig(seed=1, f_dispatch="F_multiplicative")
    with pytest.raises(ConfigError):
        RunConfig(seed=1, q=QConfig(q_read="aggregate"))

def test_f_baseline_requires_arbitration_flag():
    with pytest.raises(ConfigError): RunConfig(seed=1, f_dispatch="F_baseline")
    RunConfig(seed=1, f_dispatch="F_baseline", allow_legacy_f_baseline=True)  # ok

def test_kappa_quarantined_from_symmetric_chain():
    with pytest.raises(ConfigError):
        RunConfig(seed=1, constants=DynamicsConstants(kappa=0.2, logit_l=-1.0, p_survive=0.4))
    RunConfig(seed=1, rule_mode="become_survive",
              constants=DynamicsConstants(kappa=0.2, logit_l=-1.0, p_survive=0.4))  # ok
    with pytest.raises(ConfigError):  # missing p_survive
        RunConfig(seed=1, rule_mode="become_survive",
                  constants=DynamicsConstants(kappa=0.2, logit_l=-1.0))

# ---- config: six-decimal exactness and no-clipping (E1 §3, v0.8) ----
def test_micro_units_exactness():
    assert as_micro_units(0.030435) == 30435
    with pytest.raises(ConfigError): as_micro_units(0.70/23)  # non-terminating
def test_base_interval_no_clipping():
    with pytest.raises(ConfigError):
        RunConfig(seed=1, init=InitConfig(base_center_micro=100_000, base_width_micro=300_000))

# ---- config: drive schedule ordering ----
def test_drive_schedule_ordering():
    RunConfig(seed=1, drive_schedule=((0, 0.0), (25, 0.5)))
    with pytest.raises(ConfigError):
        RunConfig(seed=1, drive_schedule=((25, 0.5), (0, 0.0)))

# ---- run record: outside its own digest, references config hash ----
def test_run_record_shape():
    rec = json.loads(build_run_record("aa", "bb", (("python","3.14.0"),), (("status","ok"),)))
    assert rec["config_hash"] == "aa" and rec["telemetry_digest"] == "bb"

# ---- rng: dynamics stream is ancestor-identical (vs. registry-derived divergence) ----
def test_dynamics_matches_ancestor_construction():
    reg = SeedRegistry(0x7A9B31C)
    ours = reg.dynamics().generator.random(1000)
    ancestor = np.random.default_rng(0x7A9B31C).random(1000)
    assert np.array_equal(ours, ancestor)

def test_dynamics_constructed_once():
    reg = SeedRegistry(1); reg.dynamics()
    with pytest.raises(RoleError): reg.dynamics()

# ---- rng: role streams independent of dynamics consumption ----
def test_role_streams_do_not_consume_dynamics():
    r1 = SeedRegistry(9); d1 = r1.dynamics().generator
    r1.role("audit"); r1.role("bootstrap", 3)
    after = d1.random(100)
    d2 = SeedRegistry(9).dynamics().generator
    assert np.array_equal(after, d2.random(100))

def test_role_streams_deterministic_and_distinct():
    a = SeedRegistry(9).role("audit").generator.random(10)
    b = SeedRegistry(9).role("audit").generator.random(10)
    c = SeedRegistry(9).role("bootstrap").generator.random(10)
    assert np.array_equal(a, b) and not np.array_equal(a, c)

# ---- rng: typed handles reject wrong-role injection ----
def test_role_handle_expect():
    s = SeedRegistry(9).role("audit")
    with pytest.raises(RoleError): s.expect("bootstrap")
    s.expect("audit")

# ---- rng: Gate-A absence discipline (vs. idle-but-present streams) ----
def test_gate_a_mode_forbids_roles():
    reg = SeedRegistry(0x7A9B31C, gate_a_mode=True)
    reg.dynamics()
    with pytest.raises(RoleError): reg.role("noise")
    with pytest.raises(RoleError): reg.null_generation_for_level(0.75)

# ---- rng: D4 zero-amplitude => None, no construction ----
def test_noise_bypass_returns_none():
    reg = SeedRegistry(9)
    assert make_noise_stream(reg, 0.0) is None
    assert all(name != "noise" for name, _ in reg.derivations())
    assert make_noise_stream(reg, 0.1) is not None

# ---- rng: level keys are exact micro-units; replicate keys cannot collide with them ----
def test_level_and_replicate_keys():
    reg = SeedRegistry(9)
    a = reg.null_generation_for_level(0.150000).generator.random(5)
    b = reg.null_generation_for_level(0.150001).generator.random(5)
    assert not np.array_equal(a, b)
    with pytest.raises(ConfigError): reg.null_generation_for_level(0.1234567)
    r = reg.replicate_uniform_stream(0).generator.random(5)
    assert not np.array_equal(r, a)

def test_provenance_recorded():
    reg = SeedRegistry(9); reg.dynamics(); reg.role("audit", 7)
    names = [n for n, _ in reg.derivations()]
    assert names == ["dynamics", "audit"]
