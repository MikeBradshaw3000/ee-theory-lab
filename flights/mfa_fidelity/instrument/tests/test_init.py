"""Tests for init.py — Gate-A algorithmic lineage.
The reference implementation below is a VERBATIM transcription of the ancestor's
initialization lines (flight2_production.py @ 4d9a622, L117-128), executed against
the same Generator construction. Bit-equality against it is the discriminating test:
a call-shape substitution (e.g., lo + (hi-lo)*random()) or a loop-order change fails it."""
import sys
import numpy as np
import pytest

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.config import InitConfig, RunConfig
from mfa_instrument.rng import SeedRegistry
from mfa_instrument.init import initialize

PRNG_SEED = 0x7A9B31C
BASE_INIT_LOW, BASE_INIT_HIGH = 0.6, 0.9

def ancestor_reference(grid_scale):
    """Verbatim ancestor transcription (tuple grid_scale as in source)."""
    gs = (grid_scale, grid_scale)
    prng = np.random.default_rng(PRNG_SEED)
    v = np.zeros(gs, dtype=np.float64)
    u = np.zeros(gs, dtype=np.float64)
    r = np.zeros(gs, dtype=np.float64)
    is_active = np.zeros(gs, dtype=bool)
    for x in range(gs[0]):
        for y in range(gs[1]):
            v[x, y] = prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            u[x, y] = prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            r[x, y] = prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            is_active[x, y] = prng.random() < 0.5
    return v, u, r, is_active, prng

def test_bernoulli_bitexact_vs_ancestor_transcription():
    for gs in (5, 20):
        cfg = InitConfig()  # m=0.75, w=0.3 => (0.6, 0.9); p=0.5
        state = initialize(cfg, gs, SeedRegistry(PRNG_SEED).dynamics())
        av, au, ar, aa, _ = ancestor_reference(gs)
        assert np.array_equal(state.v, av)          # bitwise: array_equal on float64
        assert np.array_equal(state.u_base, au)
        assert np.array_equal(state.r, ar)
        assert np.array_equal(state.is_active, aa)

def test_post_init_stream_position_matches_ancestor():
    """After init, the NEXT draws must coincide — position in the sequence matters
    for the per-tick grid draw that follows (Gate-A sequence discipline)."""
    gs = 7
    state_dyn = SeedRegistry(PRNG_SEED).dynamics()
    initialize(InitConfig(), gs, state_dyn)
    _, _, _, _, ancestor_prng = ancestor_reference(gs)
    assert np.array_equal(state_dyn.generator.random(size=(gs, gs)),
                          ancestor_prng.random(size=(gs, gs)))

def test_dtypes_frozen():
    s = initialize(InitConfig(), 6, SeedRegistry(3).dynamics())
    assert s.v.dtype == np.float64 and s.u_base.dtype == np.float64
    assert s.r.dtype == np.float64 and s.is_active.dtype == bool

def test_general_level_bounds_and_determinism():
    cfg = InitConfig(base_center_micro=300_000, base_width_micro=300_000)  # U(0.15,0.45)
    a = initialize(cfg, 10, SeedRegistry(11).dynamics())
    b = initialize(cfg, 10, SeedRegistry(11).dynamics())
    assert np.array_equal(a.v, b.v) and np.array_equal(a.is_active, b.is_active)
    for arr in (a.v, a.u_base, a.r):
        assert arr.min() >= 0.15 and arr.max() <= 0.45

def test_fixed_count_exact_and_deterministic():
    cfg = InitConfig(scheme="fixed_count", fixed_count=25, bernoulli_p=0.5)
    # fixed_count requires validation via RunConfig path? InitConfig.validate needs n_cells:
    cfg.validate(100)
    a = initialize(cfg, 10, SeedRegistry(4).dynamics())
    b = initialize(cfg, 10, SeedRegistry(4).dynamics())
    assert int(a.is_active.sum()) == 25
    assert np.array_equal(a.is_active, b.is_active)
    assert np.array_equal(a.v, b.v)

def test_fixed_count_differs_from_bernoulli_lineage():
    """Discriminates: fixed_count is a NEW implementation, not the ancestor path —
    at matched seed its activity pattern must not equal the Bernoulli lineage's."""
    bern = initialize(InitConfig(), 10, SeedRegistry(4).dynamics())
    fc_cfg = InitConfig(scheme="fixed_count", fixed_count=int(bern.is_active.sum()))
    fc = initialize(fc_cfg, 10, SeedRegistry(4).dynamics())
    assert not np.array_equal(bern.is_active, fc.is_active)
