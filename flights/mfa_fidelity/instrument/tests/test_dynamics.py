"""Tests for dynamics.py. The A-side reference is a verbatim transcription of the
ancestor's NumpyEEModel (flight2_production.py @ 4d9a622); the B-side reference is a
verbatim transcription of step_tcop_core (c3_w2_tcop.py). Bit-equality against these
discriminates FP-ordering, draw-order, and update-order divergence."""
import sys
import numpy as np
import pytest

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.config import RunConfig, DynamicsConstants, QConfig, InitConfig, NoiseConfig
from mfa_instrument.rng import SeedRegistry
from mfa_instrument.init import initialize
from mfa_instrument.dynamics import Dynamics, _sigmoid

PRNG_SEED = 0x7A9B31C
ALPHA, BETA, DELTA, GAMMA_OFFSET, ETA, GAMMA_Q = 4.0, 3.0, 4.0, 4.0, 0.01, 0.001
W_V, W_U, W_R = 0.33, 0.33, 0.34
LOW, HIGH = 0.6, 0.9

class AncestorModel:
    """Verbatim transcription of the ancestor step (telemetry loop omitted; all
    per-tick arrays captured for comparison)."""
    MOORE = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    def __init__(self, gs, f_form):
        self.gs = (gs, gs); self.f_form = f_form
        self.prng = np.random.default_rng(PRNG_SEED)
        self.v = np.zeros(self.gs, dtype=np.float64)
        self.u = np.zeros(self.gs, dtype=np.float64)
        self.r = np.zeros(self.gs, dtype=np.float64)
        self.is_active = np.zeros(self.gs, dtype=bool)
        for x in range(gs):
            for y in range(gs):
                self.v[x,y] = self.prng.uniform(LOW, HIGH)
                self.u[x,y] = self.prng.uniform(LOW, HIGH)
                self.r[x,y] = self.prng.uniform(LOW, HIGH)
                self.is_active[x,y] = self.prng.random() < 0.5
    def moore(self, m):
        t = np.zeros_like(m, dtype=np.float64)
        for dx, dy in self.MOORE:
            t += np.roll(np.roll(m, dx, axis=0), dy, axis=1)
        return t
    def step(self):
        bases = np.stack([self.v, self.u, self.r], axis=0)
        lam_mult = self.v * self.u * self.r
        lam_add = W_V*self.v + W_U*self.u + W_R*self.r
        if self.f_form == "F_baseline": lam = (self.v + self.u + self.r) / 3.0
        elif self.f_form == "F_LR": lam = np.min(bases, axis=0)
        elif self.f_form == "F_2_symmetric": lam = lam_mult * lam_add
        else: raise ValueError
        dens = self.moore(self.is_active.astype(np.float64)) / 8.0
        drive = ALPHA*lam + BETA*dens + (-DELTA*(dens**2)) + np.full_like(self.v, -GAMMA_OFFSET)
        p_base = 1.0/(1.0+np.exp(-drive))
        p_act = np.clip(p_base + ETA*(1.0-p_base), 0.0, 1.0)
        draw = self.prng.random(size=self.gs)
        nxt = draw < p_act
        ds = nxt.astype(int) - self.is_active.astype(int)
        self.is_active = nxt.copy()
        psi = ds * self.moore(ds.astype(np.float64))
        delta = GAMMA_Q * psi
        self.last = dict(drive=drive, p_base=p_base, p_act=p_act, draw=draw, psi=psi, delta=delta)
        vn, un, rn = self.v+delta, self.u+delta, self.r+delta
        self.v, self.u, self.r = np.clip(vn,0,1), np.clip(un,0,1), np.clip(rn,0,1)

def make_ours(f_form, gamma_psi=GAMMA_Q, gamma_rho=0.0, q_read="local", gs=12,
              allow_baseline=False, schedule=()):
    cfg = RunConfig(seed=PRNG_SEED, f_dispatch=f_form, grid_scale=gs, ticks=3000,
                    q=QConfig(q_read=q_read, gamma_psi=gamma_psi, gamma_rho=gamma_rho),
                    allow_legacy_f_baseline=allow_baseline, drive_schedule=schedule)
    dyn = SeedRegistry(PRNG_SEED, gate_a_mode=(gamma_rho==0.0 and not schedule)).dynamics()
    state = initialize(cfg.init, gs, dyn)
    return cfg, Dynamics(cfg, state, dyn)

@pytest.mark.parametrize("f_form,allow", [("F_2_symmetric",False),("F_LR",False),("F_baseline",True)])
def test_symmetric_chain_bitexact_vs_ancestor(f_form, allow):
    gs = 12
    anc = AncestorModel(gs, f_form)
    _, ours = make_ours(f_form, allow_baseline=allow, gs=gs)
    captured = {}
    def sink(t, fields): captured.update({k: np.array(v) for k, v in fields.items()})
    for _ in range(5):
        anc.step(); ours.step(sink)
    assert np.array_equal(ours._v, anc.v)          # bases bit-identical after 5 Q ticks
    assert np.array_equal(ours._u_base, anc.u)
    assert np.array_equal(ours._r, anc.r)
    assert np.array_equal(ours._is_active, anc.is_active)
    assert np.array_equal(captured["Drive_Raw"], anc.last["drive"])
    assert np.array_equal(captured["p_act"], anc.last["p_act"])
    assert np.array_equal(captured["PRNG_draw"], anc.last["draw"])
    assert np.array_equal(captured["Psi_local"], anc.last["psi"])
    assert np.array_equal(captured["Delta_v"], anc.last["delta"])

def test_e1_total_q_disable_bases_bit_identical():
    cfg, ours = make_ours("F_canonical", gamma_psi=0.0, gamma_rho=0.0)
    v0, u0, r0 = ours._v.copy(), ours._u_base.copy(), ours._r.copy()
    for _ in range(20): ours.step()
    assert np.array_equal(ours._v, v0) and np.array_equal(ours._u_base, u0)
    assert np.array_equal(ours._r, r0)
    assert ours.clipped_v_count == 0  # no clip machinery ran

def test_f_canonical_is_triple_product():
    _, ours = make_ours("F_canonical", gamma_psi=0.0)
    got = {}
    ours.step(lambda t, f: got.update(f))
    assert np.array_equal(got["Lambda_total"], got["Lambda_multiplicative"])

def test_u_t_zero_is_absent_not_added():
    """Same seed, one config with empty schedule, one with explicit (0, 0.0):
    drive must be bit-identical (absence == explicit zero here because the branch
    doesn't execute at u_t==0.0)."""
    _, a = make_ours("F_2_symmetric"); _, b = make_ours("F_2_symmetric", schedule=((0,0.0),))
    ga, gb = {}, {}
    a.step(lambda t,f: ga.update(f)); b.step(lambda t,f: gb.update(f))
    assert np.array_equal(ga["Drive_Raw"], gb["Drive_Raw"])

def test_u_t_nonzero_shifts_drive():
    _, a = make_ours("F_2_symmetric"); _, b = make_ours("F_2_symmetric", schedule=((0,0.5),))
    ga, gb = {}, {}
    a.step(lambda t,f: ga.update(f)); b.step(lambda t,f: gb.update(f))
    assert np.allclose(gb["Drive_Raw"] - ga["Drive_Raw"], 0.5)

def test_global_q_read_moves_bases_uniformly():
    cfg, ours = make_ours("F_canonical", gamma_psi=0.0, gamma_rho=0.01, q_read="global")
    v0 = ours._v.copy()
    got = {}
    ours.step(lambda t,f: got.update(f))
    assert "rho_global" in got
    dv = ours._v - v0
    assert np.allclose(dv, dv.flat[0])  # common-mode write: identical delta everywhere

def test_local_q_read_moves_bases_locally():
    cfg, ours = make_ours("F_canonical", gamma_psi=0.0, gamma_rho=0.01, q_read="local")
    v0 = ours._v.copy()
    ours.step()
    dv = ours._v - v0
    assert not np.allclose(dv, dv.flat[0])  # varies with Local_Density

def test_noise_stream_under_zero_amplitude_rejected():
    cfg, _ = make_ours("F_2_symmetric")
    reg = SeedRegistry(1)
    dyn = reg.dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    with pytest.raises(ValueError):
        Dynamics(cfg, state, dyn, noise=reg.role("noise"))

# ---- become_survive vs verbatim B transcription ----
B_LAMBDA = 0.40
B_LOGIT = float(np.log(B_LAMBDA/(1.0-B_LAMBDA)))
def b_reference_step(grid, u_t, kappa, rand_grid):
    n = (np.roll(grid,1,0)+np.roll(grid,-1,0)+np.roll(grid,1,1)+np.roll(grid,-1,1)+
         np.roll(np.roll(grid,1,0),1,1)+np.roll(np.roll(grid,1,0),-1,1)+
         np.roll(np.roll(grid,-1,0),1,1)+np.roll(np.roll(grid,-1,0),-1,1))
    g_q = 2.0*(n/8.0)-1.0
    p_become = 1.0/(1.0+np.exp(-(B_LOGIT+u_t+kappa*g_q)))
    become = (grid==0)&(rand_grid<p_become)
    stay = (grid==1)&(rand_grid<B_LAMBDA)
    return (become|stay).astype(int), p_become

def test_become_survive_rule_equivalence_mini_b1():
    gs = 10
    cfg = RunConfig(seed=77, rule_mode="become_survive", grid_scale=gs,
                    init=InitConfig(scheme="fixed_count", fixed_count=10),
                    constants=DynamicsConstants(logit_l=B_LOGIT, kappa=0.2, p_survive=B_LAMBDA),
                    drive_schedule=((0, 0.3),))
    dyn = SeedRegistry(77).dynamics()
    state = initialize(cfg.init, gs, dyn)
    ours = Dynamics(cfg, state, dyn)
    grid_ref = state.is_active.astype(int).copy()
    # replay our stream's draws through the reference:
    shadow = SeedRegistry(77).dynamics().generator
    initialize(cfg.init, gs, type("D", (), {"generator": shadow})())  # consume init draws identically
    got = {}
    for _ in range(4):
        rand_grid = shadow.random(size=(gs, gs))
        grid_ref, p_ref = b_reference_step(grid_ref, 0.3, 0.2, rand_grid)
        ours.step(lambda t, f: got.update({k: np.array(v) for k, v in f.items()}))
        assert np.array_equal(got["p_become"], p_ref)
        assert np.array_equal(got["rand_grid"], rand_grid)
        assert np.array_equal(ours._is_active.astype(int), grid_ref)

def test_become_survive_survival_invariant_to_drive_and_coupling():
    """Facts v1.1: survival invariant to u_t and kappa — p_survive is the constant."""
    gs = 8
    def run(kappa, u):
        cfg = RunConfig(seed=5, rule_mode="become_survive", grid_scale=gs,
                        init=InitConfig(scheme="fixed_count", fixed_count=64),  # all active
                        constants=DynamicsConstants(logit_l=B_LOGIT, kappa=kappa, p_survive=B_LAMBDA),
                        drive_schedule=((0, u),) if u else ())
        dyn = SeedRegistry(5).dynamics()
        d = Dynamics(cfg, initialize(cfg.init, gs, dyn), dyn)
        d.step()
        return d._is_active.copy()
    assert np.array_equal(run(0.0, 0.0), run(0.9, 0.7))  # all-active grid: only survival acts
