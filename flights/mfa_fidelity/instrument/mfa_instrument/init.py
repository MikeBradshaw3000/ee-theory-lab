"""mfa_instrument.init — Initialization with Gate-A algorithmic lineage.

Spec anchors: Merge Specification v0.4 FROZEN §5.1 (algorithmic lineage vs. parameter
choice; Gate A freezes the exact ancestor algorithm); facts v1.1 S1(b).

Ancestor source of truth (flight2_production.py @ 4d9a622, L123–128, read verbatim
2026-08-23 — not from memory):

    for x in range(self.grid_scale[0]):
        for y in range(self.grid_scale[1]):
            self.v[x, y] = self.prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            self.u[x, y] = self.prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            self.r[x, y] = self.prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
            self.is_active[x, y] = self.prng.random() < 0.5

Frozen consequences honored here:
  - scalar Generator.uniform(low, high) calls — NOT manual low + (high-low)*random(),
    which would diverge in floating point even at identical stream consumption;
  - draw order per cell: v, u_base, r, activity — cell-by-cell, x-outer/y-inner;
  - dtype float64 throughout, no intermediate coercion;
  - arrays preallocated with np.zeros exactly as the ancestor does.

`fixed_count` is a NEW merged-instrument implementation (spec §5.1 as corrected at
v0.4/blocker-1): not bit-exact preservation of Lineage B's legacy initialization,
RNG realization, or seedwise history; its dynamical behavior is Gate-B2 territory.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .config import InitConfig, ConfigError
from .rng import DynamicsStream


@dataclass(frozen=True)
class GridState:
    """Initialized model state. Ownership note (Build Plan v0.2, finding D): these
    arrays are handed to dynamics, which becomes their sole mutating owner; every
    other consumer receives read-only views or copies."""
    v: np.ndarray = field(repr=False)
    u_base: np.ndarray = field(repr=False)   # ledger: u_base, never bare u
    r: np.ndarray = field(repr=False)
    is_active: np.ndarray = field(repr=False)


def initialize(init_cfg: InitConfig, grid_scale: int, dyn: DynamicsStream) -> GridState:
    """Dispatch on the init scheme. Consumes ONLY the dynamics stream, exactly as the
    ancestor does — initialization draws are part of the Gate-A sequence.

    Base algorithm (L2 Phase-1 review D2 — CONFIG-BOUND): init_cfg.base_init_mode
    selects "stochastic_ancestor" (Gate-A cell-by-cell draws) or
    "deterministic_level" (np.full at m; zero base draws consumed; the
    become_survive/B-comparable policy). The former runner-side draw_bases switch is
    REMOVED — no unrecorded argument can change RNG consumption; the mode serializes
    in run_config.json and cross-validates against rule_mode at RunConfig level."""
    draw_bases = (init_cfg.base_init_mode == "stochastic_ancestor")
    if init_cfg.scheme == "bernoulli_p":
        return _init_bernoulli_ancestor_lineage(init_cfg, grid_scale, dyn, draw_bases)
    if init_cfg.scheme == "fixed_count":
        return _init_fixed_count(init_cfg, grid_scale, dyn, draw_bases)
    raise ConfigError(f"unknown init scheme {init_cfg.scheme!r}")   # unreachable post-validation


def _init_bernoulli_ancestor_lineage(cfg: InitConfig, grid_scale: int,
                                     dyn: DynamicsStream, draw_bases: bool = True) -> GridState:
    """The ancestor algorithm, generalized only in its (low, high) parameters.

    At m = 0.75, w = 0.3 (=> low 0.6, high 0.9), p = 0.5, this reproduces the
    ancestor's initialization bit-exactly at matched seed — asserted by test against
    a verbatim transcription of the quoted ancestor lines, and certified by Gate A.
    """
    lo = cfg.m - cfg.w / 2.0
    hi = cfg.m + cfg.w / 2.0
    shape = (grid_scale, grid_scale)
    g = dyn.generator

    is_active = np.zeros(shape, dtype=bool)
    if draw_bases:
        v = np.zeros(shape, dtype=np.float64)
        u_base = np.zeros(shape, dtype=np.float64)
        r = np.zeros(shape, dtype=np.float64)
        for x in range(shape[0]):
            for y in range(shape[1]):
                v[x, y] = g.uniform(lo, hi)
                u_base[x, y] = g.uniform(lo, hi)
                r[x, y] = g.uniform(lo, hi)
                is_active[x, y] = g.random() < cfg.bernoulli_p
    else:
        v = np.full(shape, cfg.m, dtype=np.float64)
        u_base = np.full(shape, cfg.m, dtype=np.float64)
        r = np.full(shape, cfg.m, dtype=np.float64)
        for x in range(shape[0]):
            for y in range(shape[1]):
                is_active[x, y] = g.random() < cfg.bernoulli_p

    return GridState(v=v, u_base=u_base, r=r, is_active=is_active)


def _init_fixed_count(cfg: InitConfig, grid_scale: int, dyn: DynamicsStream,
                      draw_bases: bool = True) -> GridState:
    """Merged-instrument fixed-count activity placement (declared draw order):
    bases first via the ancestor's cell-by-cell base loop (three scalar uniforms per
    cell, no activity draw), then ONE Generator.permutation over cell indices, first
    `fixed_count` cells active. New implementation; certified distributionally (B2)."""
    lo = cfg.m - cfg.w / 2.0
    hi = cfg.m + cfg.w / 2.0
    shape = (grid_scale, grid_scale)
    n_cells = grid_scale * grid_scale
    g = dyn.generator

    if draw_bases:
        v = np.zeros(shape, dtype=np.float64)
        u_base = np.zeros(shape, dtype=np.float64)
        r = np.zeros(shape, dtype=np.float64)
        for x in range(shape[0]):
            for y in range(shape[1]):
                v[x, y] = g.uniform(lo, hi)
                u_base[x, y] = g.uniform(lo, hi)
                r[x, y] = g.uniform(lo, hi)
    else:
        v = np.full(shape, cfg.m, dtype=np.float64)
        u_base = np.full(shape, cfg.m, dtype=np.float64)
        r = np.full(shape, cfg.m, dtype=np.float64)

    order = g.permutation(n_cells)
    is_active_flat = np.zeros(n_cells, dtype=bool)
    is_active_flat[order[: int(cfg.fixed_count)]] = True
    is_active = is_active_flat.reshape(shape)

    return GridState(v=v, u_base=u_base, r=r, is_active=is_active)
