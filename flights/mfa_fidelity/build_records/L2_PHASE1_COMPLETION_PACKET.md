# Note to L2 — Phase 1 Completion Packet: Code-Audit Fixes + Remaining Phase-1 Modules

**From:** L1, routed by Mike
**Register:** closed, scoped — the incremental source-level review you named ("the remaining files... should receive the same source-level treatment before the stage-1 package is assembled"). Phase 2 proceeds in parallel per Mike's direction; your findings integrate as the audit's did.
**Carried verbatim below the rule, in order:** (1) defect-fix map; (2) `dynamics.py` (corrected); (3) `init.py` (corrected); (4) `telemetry.py` (corrected); (5) `gates/gate_a.py` (corrected); (6) `verify.py` (new); (7) `tests/test_verify.py` (new); (8) the provisional Gate-A checkpoint report. Previously-audited files are superseded by these texts; digests at the foot.

## 1. Defect-fix map (your audit → implementation)

- **D1 (ownership durability):** `view_bases` now returns read-only **copies** — aliasing impossible, protection permanent, no restore path exists. The sink freezes all fields once and never un-freezes; live `is_active` is **copied** before exposure; the special-case bookkeeping you flagged is deleted. Both rule-mode sinks share the discipline.
- **D2 (become_survive init draws):** now an explicit, documented, tested policy — `initialize(..., draw_bases=False)` fills bases deterministically at the level value m (np.full, float64) with **zero base draws consumed**; the default (True) is the ancestor-faithful path, so no silent divergence exists. Test: stream-position identity — under draw_bases=False the first consumption is the activity placement itself.
- **D3 (delta scalar/array):** dynamics now computes `delta_from_psi` / `delta_from_rho` as explicit grid-shaped arrays (global-mode scalar broadcast via np.full_like at the source), always hands telemetry clean arrays, and telemetry's scalar-inference branch is removed. FP note: v + full(c) is elementwise bit-identical to v + c.
- **D4 (dead probe expression):** removed; the preflight's consumption check is the clean independent probe only.
- **D5 (environment conformance):** `run_gate_a` **refuses the AUTHORITATIVE label** outside python 3.14.x / numpy 2.4.4 (frozen §7.4 pins), raising with the reason; non-conforming environments are stamped "[NON-CONFORMING: provisional only]" in the report. My unverified import-bypass claim is withdrawn; nothing now depends on it.
- **D6 (frame()/digest):** `frame()` raises on a streaming writer (partial-tail misrepresentation foreclosed); `telemetry_digest` rejects duplicate basenames before hashing.

## 2. New modules for first-pass source review

`verify.py` implements the Tier-1 spine (frozen §7.2): realization invariant; Λ recomputation per dispatch label; full drive decomposition including u_t reconstruction from the frozen schedule and the conditional noise term; probability chain; Q decomposition (schema-driven applicability); all streamed batch-wise over the written parquet at **exact equality** — tolerances would hide the FP-ordering divergence Tier-1 exists to catch. Plus `e1_base_bit_identity` (Contract E1 §2 conformance: schema absence of Q columns + streamed base bit-identity). Its test file plants one-bit defects (1e-12/1e-15) in five columns and requires each named check to catch its plant — a verifier that cannot fail is not a verifier.

## 3. Provisional Gate-A checkpoint (labeled per the build plan; certifies nothing)

`GATE A [PROVISIONAL] f=F_2_symmetric grid=50 ticks=100 preflight=PASS state=BIT-EXACT telemetry=BIT-EXACT env=python3.12.3/numpy2.4.4 [NON-CONFORMING: provisional only]`
Comparison target: the actual `flight2_production.py` imported from the pinned clone at `4d9a622` (never a transcription). The pytest harness additionally runs all three ancestor F-forms at 12×12/25. Full suite: 53/53.

## 4. Review requested (closed register)

1. Per defect D1–D6: **FIXED AS REQUIRED** or **FIX DEFECT** with location.
2. Source-level defects in `verify.py` / `test_verify.py` (first pass): enumerated findings; **NONE FOUND** complete.
3. Any new defect introduced by the fixes into previously-audited files: **NONE FOUND** complete.
Phase 2 (Gate B, observables) will arrive as the next incremental packet.

---

# ARTIFACT 2: mfa_instrument/dynamics.py
```python
"""mfa_instrument.dynamics — The unified execution core.

Spec anchors: Merge Specification v0.4 FROZEN §1.2 (common skeleton; dispatch replaces
the probability construction wholesale; become/survive computed directly, never layered
on A's chain), §2 (F dispatch incl. F_canonical slot-addition), §4 (extended Q, causal
timing, both bypasses absent-not-zero), §6.2 (noise bypass), §8.1 (Gate-A discipline).

Source-of-truth transcriptions (read from the pinned clone @ 4d9a622, not memory):
  - Lineage A step: flight2_production.py L146–252 — exact FP ordering preserved,
    including the Moore-sum accumulation ORDER (offsets list, += loop), the drive-term
    sum order, sigmoid = 1/(1+exp(-x)), telemetry BEFORE base update (Step 13 then 12).
  - Lineage B step: c3_w2_tcop.py L263–272 — p_become = sigmoid(LOGIT_L + u_t + κ·g_q)
    on inactive cells; survival at the CONSTANT p_survive ("bare p_Λ": rand < Λ);
    ONE shared rand_grid for both branches (committed discipline); its own 8-term
    neighbor-count expression.

Ownership (Build Plan v0.2, findings A/D): this module is the sole owner of mutable
v/u_base/r/is_active state and of the single authoritative causal Ψ_local computation.
Telemetry sinks receive read-only views; nothing feeds values back into Q.
"""
from __future__ import annotations

from typing import Callable, Dict, Optional

import numpy as np

from .config import RunConfig
from .init import GridState
from .rng import DynamicsStream, RoleStream

TelemetrySink = Callable[[int, Dict[str, np.ndarray]], None]

# Ancestor Moore offsets, exact list order (accumulation order affects FP sums).
_MOORE_OFFSETS_A = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def _sigmoid(x: np.ndarray) -> np.ndarray:
    """Ancestor's exact form (flight2_production.py L107): NOT scipy expit."""
    return 1.0 / (1.0 + np.exp(-x))


def _moore_sum_a(grid_matrix: np.ndarray) -> np.ndarray:
    """Verbatim ancestor accumulation (get_moore_sum): zeros_like float64, += in the
    frozen offset order."""
    total = np.zeros_like(grid_matrix, dtype=np.float64)
    for dx, dy in _MOORE_OFFSETS_A:
        total += np.roll(np.roll(grid_matrix, dx, axis=0), dy, axis=1)
    return total


def _neighbor_count_b(grid: np.ndarray) -> np.ndarray:
    """Verbatim Lineage B expression order (c3_w2_tcop.py get_neighbor_count)."""
    return (
        np.roll(grid, 1, axis=0) + np.roll(grid, -1, axis=0) +
        np.roll(grid, 1, axis=1) + np.roll(grid, -1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), -1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), -1, axis=1)
    )


class Dynamics:
    """Owns state; advances it; emits read-only telemetry fields per tick."""

    def __init__(self, cfg: RunConfig, state: GridState, dyn: DynamicsStream,
                 noise: Optional[RoleStream] = None) -> None:
        self.cfg = cfg
        self._g = dyn.generator
        self._v = state.v
        self._u_base = state.u_base
        self._r = state.r
        self._is_active = state.is_active
        self.tick_count = 0
        self.clipped_v_count = 0
        self.clipped_u_count = 0
        self.clipped_r_count = 0
        # D4: at amplitude 0 the caller passes None; no stream exists here at all.
        if cfg.noise.amplitude == 0.0 and noise is not None:
            raise ValueError("noise stream constructed under zero amplitude (D4 bypass violated)")
        self._noise = noise
        # Q bypass structure resolved ONCE, as absent paths, not zero-valued arithmetic.
        self._q_disabled = (cfg.q.gamma_psi == 0.0 and cfg.q.gamma_rho == 0.0)
        self._rho_read = (cfg.q.gamma_rho != 0.0)
        # Drive schedule resolved to a per-tick lookup (empty schedule => always 0.0).
        self._schedule = tuple(cfg.drive_schedule)

    # -- read-only state access (finding D: no writeable aliases leave this module) --
    def view_bases(self):
        """Durable read-only snapshots (L2 code-audit D1): copies with writeable=False.
        Copies cannot alias internal state; the flag communicates intent; protection
        cannot be lifted on the originals because callers never receive them."""
        out = []
        for arr in (self._v, self._u_base, self._r):
            c = arr.copy()
            c.flags.writeable = False
            out.append(c)
        return tuple(out)

    def snapshot_active(self) -> np.ndarray:
        return self._is_active.copy()

    def _u_t(self, tick: int) -> float:
        u = 0.0
        for start, val in self._schedule:
            if tick >= start:
                u = val
            else:
                break
        return u

    # ------------------------------------------------------------------ step
    def step(self, sink: Optional[TelemetrySink] = None) -> None:
        if self.cfg.rule_mode == "symmetric_chain":
            self._step_symmetric_chain(sink)
        else:
            self._step_become_survive(sink)
        self.tick_count += 1

    # -- Lineage A chain, ancestor FP ordering preserved ---------------------
    def _step_symmetric_chain(self, sink: Optional[TelemetrySink]) -> None:
        cfg = self.cfg
        k = cfg.constants
        tick_idx = self.tick_count

        # Step 1: pre-Q base copies (ancestor names preserved in telemetry fields)
        b_i_v = self._v.copy()
        b_i_u = self._u_base.copy()
        b_i_r = self._r.copy()

        bases_stack = np.stack([self._v, self._u_base, self._r], axis=0)
        limiting_base_argmin = np.argmin(bases_stack, axis=0)
        lambda_multiplicative = self._v * self._u_base * self._r
        lambda_additive = k.w_v * self._v + k.w_u * self._u_base + k.w_r * self._r

        # Step 2: F dispatch — ancestor branches verbatim + the D3 slot-addition.
        f = cfg.f_dispatch
        if f == "F_baseline":
            lambda_total = (self._v + self._u_base + self._r) / 3.0
        elif f == "F_LR":
            lambda_total = np.min(bases_stack, axis=0)
        elif f == "F_2_symmetric":
            lambda_total = lambda_multiplicative * lambda_additive
        elif f == "F_canonical":
            lambda_total = lambda_multiplicative  # Λ = v·u_base·r (already computed)
        else:  # unreachable post-validation
            raise ValueError(f"Unknown F-form: {f}")

        # Step 3: local density
        active_int = self._is_active.astype(np.float64)
        local_density = _moore_sum_a(active_int) / 8.0

        # Step 4: drive components — ancestor term names and sum order; u_t appended
        # ONLY when nonzero (absent at zero: Gate-A arithmetic identical to ancestor).
        term_lambda = k.alpha * lambda_total
        term_density_pos = k.beta * local_density
        term_overcrowding = -k.delta * (local_density ** 2)
        term_offset = np.full_like(self._v, -k.gamma_offset)
        drive_raw = term_lambda + term_density_pos + term_overcrowding + term_offset
        u_t = self._u_t(tick_idx)
        if u_t != 0.0:
            drive_raw = drive_raw + u_t
        # D4 noise: absent at amplitude 0 (no stream exists); additive when enabled.
        if self._noise is not None:
            noise_draw = self._noise.expect("noise").normal(
                0.0, cfg.noise.amplitude, size=drive_raw.shape)
            drive_raw = drive_raw + noise_draw
        else:
            noise_draw = None

        # Step 5: probability chain (eta_floor is ancestor ETA)
        p_base = _sigmoid(drive_raw)
        p_act = np.clip(p_base + k.eta_floor * (1.0 - p_base), 0.0, 1.0)

        # Pre-update Q activation input (D2 causal timing): computed BEFORE the draw
        # only in global mode; local mode reuses Step 3's pre-update Local_Density.
        if self._rho_read and cfg.q.q_read == "global":
            rho_global = float(np.mean(self._is_active))
        else:
            rho_global = None

        # Step 6: one full-grid draw
        prng_draw = self._g.random(size=(cfg.grid_scale, cfg.grid_scale))
        next_state = prng_draw < p_act

        # Steps 7–8: synchronous advance
        ds = next_state.astype(int) - self._is_active.astype(int)
        self._is_active = next_state.copy()

        # Step 9: causal Psi_local — THE authoritative mechanism computation.
        sum_neighbor_ds = _moore_sum_a(ds.astype(np.float64))
        psi_local = ds * sum_neighbor_ds

        # Step 11 (Q deltas), computed here so telemetry can carry them, but the
        # base UPDATE stays after telemetry per ancestor order (Step 13 then 12).
        # (L2 code-audit D3: components computed here, always as arrays; telemetry
        # receives clean grid-shaped fields and does no dynamics inference.)
        if self._q_disabled:
            delta = None            # E1 total-Q-disable: no arithmetic exists.
            delta_from_psi = delta_from_rho = None
        elif not self._rho_read:
            delta = cfg.q.gamma_psi * psi_local        # ancestor expression exactly
            delta_from_psi = delta_from_rho = None     # decomposition columns absent
        else:
            if cfg.q.q_read == "local":
                rho_term = cfg.q.gamma_rho * local_density
            else:
                rho_term = np.full_like(psi_local, cfg.q.gamma_rho * rho_global,
                                        dtype=np.float64)
            if cfg.q.gamma_psi == 0.0:
                psi_term = np.zeros_like(psi_local, dtype=np.float64)
                delta = rho_term
            else:
                psi_term = cfg.q.gamma_psi * psi_local
                delta = psi_term + rho_term
            delta_from_psi, delta_from_rho = psi_term, rho_term

        # Step 13: telemetry BEFORE base update (ancestor order). Read-only fields.
        # (L2 code-audit D1: live state is COPIED before exposure; every field is a
        # per-tick temporary or a copy; all are frozen once and never un-frozen —
        # dynamics only READS them after this point, and they go out of scope.)
        if sink is not None:
            fields: Dict[str, np.ndarray] = {
                "b_i_v": b_i_v, "b_i_u": b_i_u, "b_i_r": b_i_r,
                "limiting_base_argmin": limiting_base_argmin,
                "Lambda_multiplicative": lambda_multiplicative,
                "Lambda_additive": lambda_additive, "Lambda_total": lambda_total,
                "Local_Density": local_density, "Drive_Raw": drive_raw,
                "Term_Density_Pos": term_density_pos,
                "Term_Overcrowding": term_overcrowding, "Term_Offset": term_offset,
                "p_base": p_base, "p_act": p_act, "PRNG_draw": prng_draw,
                "is_active": self._is_active.copy(), "Psi_local": psi_local,
                "Term_Lambda": term_lambda,
            }
            if delta is not None:
                if delta_from_psi is not None:
                    fields["Delta_from_Psi"] = delta_from_psi
                    fields["Delta_from_rho"] = delta_from_rho
                fields["Delta_v"] = delta
                fields["Delta_u"] = delta
                fields["Delta_r"] = delta
            if rho_global is not None:
                fields["rho_global"] = np.float64(rho_global)
            if noise_draw is not None:
                fields["Noise_Draw"] = noise_draw
            for a in fields.values():
                if isinstance(a, np.ndarray):
                    a.flags.writeable = False
            sink(tick_idx, fields)

        # Step 12: base update with clip counters — ONLY when Q arithmetic exists.
        if delta is not None:
            v_new = self._v + delta
            u_new = self._u_base + delta
            r_new = self._r + delta
            self.clipped_v_count += int(np.sum((v_new < 0.0) | (v_new > 1.0)))
            self.clipped_u_count += int(np.sum((u_new < 0.0) | (u_new > 1.0)))
            self.clipped_r_count += int(np.sum((r_new < 0.0) | (r_new > 1.0)))
            self._v = np.clip(v_new, 0.0, 1.0)
            self._u_base = np.clip(u_new, 0.0, 1.0)
            self._r = np.clip(r_new, 0.0, 1.0)

    # -- Lineage B rule, computed directly (never layered on A's chain) ------
    def _step_become_survive(self, sink: Optional[TelemetrySink]) -> None:
        cfg = self.cfg
        k = cfg.constants
        tick_idx = self.tick_count
        u_t = self._u_t(tick_idx)

        grid = self._is_active.astype(int)
        neighbors = _neighbor_count_b(grid)
        q_i = neighbors / 8.0
        g_q = 2.0 * q_i - 1.0
        p_become = _sigmoid(k.logit_l + u_t + k.kappa * g_q)

        rand_grid = self._g.random(size=(cfg.grid_scale, cfg.grid_scale))  # ONE shared grid
        become_active = (grid == 0) & (rand_grid < p_become)
        stay_active = (grid == 1) & (rand_grid < k.p_survive)   # bare p_Λ: constant
        next_grid = (become_active | stay_active)

        ds = next_grid.astype(int) - grid
        self._is_active = next_grid.copy()
        psi_local = ds * _moore_sum_a(ds.astype(np.float64))    # mechanism emission

        if sink is not None:
            fields = {"p_become": p_become, "g_q": g_q, "rand_grid": rand_grid,
                      "is_active": self._is_active.copy(), "Psi_local": psi_local}
            for a in fields.values():
                a.flags.writeable = False
            sink(tick_idx, fields)
        # Bases untouched: become_survive runs frozen-bases configurations (spec §1.3).
```

# ARTIFACT 3: mfa_instrument/init.py
```python
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


def initialize(init_cfg: InitConfig, grid_scale: int, dyn: DynamicsStream,
               draw_bases: bool = True) -> GridState:
    """Dispatch on the init scheme. Consumes ONLY the dynamics stream, exactly as the
    ancestor does — initialization draws are part of the Gate-A sequence.

    draw_bases (L2 code-audit D2 — EXPLICIT POLICY): in become_survive configurations
    the rule never reads bases; the runner passes draw_bases=False and bases are set
    DETERMINISTICALLY to the level value m (np.full, float64) with NO stochastic base
    draws consumed — the dynamics stream then serves activity placement and per-tick
    draws only, preserving B-comparable stream economy. symmetric_chain configurations
    always pass draw_bases=True (the Gate-A sequence). The policy is the caller's
    declared choice, recorded in run provenance; there is no silent default divergence
    because the default (True) is the ancestor-faithful path."""
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
```

# ARTIFACT 4: mfa_instrument/telemetry.py
```python
"""mfa_instrument.telemetry — Row-family emission, parquet streaming, canonical digest.

Spec anchors: Merge Specification v0.4 FROZEN §7.1 (25-column ancestor family +
Delta_from_Psi/Delta_from_rho + conditional Noise_Draw; rho_global tick table),
§7.3 (canonical telemetry digest: parquet files' raw bytes in ascending lexicographic
filename order, each preceded by its filename as a UTF-8 line), §8.1 (instrumentation
must not alter state, evaluation order, dtype, or stochastic consumption — this module
only reads the read-only field views the dynamics sink provides).

Ancestor column order (flight2_production.py @ 4d9a622, telemetry row dict, verbatim):
Tick, Agent_X, Agent_Y, b_i_v, b_i_u, b_i_r, limiting_base_argmin,
Lambda_multiplicative, Lambda_additive, Lambda_total, Local_Density, Drive_Raw,
Term_Density_Pos, Term_Overcrowding, Term_Offset, p_base, p_act, PRNG_draw,
is_active, Psi_local, gamma_coef, Delta_v, Delta_u, Delta_r, Term_Lambda  (25 columns)

Row order: per tick, cells in np.indices row-major flatten order (ancestor xs/ys loop).
"""
from __future__ import annotations

import hashlib
import os
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ANCESTOR_COLUMNS = [
    "Tick", "Agent_X", "Agent_Y", "b_i_v", "b_i_u", "b_i_r", "limiting_base_argmin",
    "Lambda_multiplicative", "Lambda_additive", "Lambda_total", "Local_Density",
    "Drive_Raw", "Term_Density_Pos", "Term_Overcrowding", "Term_Offset", "p_base",
    "p_act", "PRNG_draw", "is_active", "Psi_local", "gamma_coef", "Delta_v",
    "Delta_u", "Delta_r", "Term_Lambda",
]
EXTENSION_COLUMNS = ["Delta_from_Psi", "Delta_from_rho"]   # spec §4.5, when rho channel active
NOISE_COLUMN = "Noise_Draw"                                 # conditional (η_MFA enabled)


class TelemetryWriter:
    """Builds per-tick row frames from the dynamics sink fields (vectorized; values
    identical to the ancestor's per-cell loop) and streams them to parquet in chunks.

    Schema policy: the column set is fixed at construction from the configuration —
    Gate-A configurations carry exactly the 25 ancestor columns (extension columns
    STRUCTURALLY ABSENT, per §8.1's preflight); rho-channel configurations add the
    two decomposition columns; noise-enabled adds Noise_Draw. E1 total-Q-disable
    drops gamma_coef/Delta_v/u/r (no Q arithmetic exists to report).
    """

    def __init__(self, grid_scale: int, gamma_psi: float, gamma_rho: float,
                 noise_enabled: bool, chunk_ticks: int = 500) -> None:
        self._gs = grid_scale
        xs, ys = np.indices((grid_scale, grid_scale))
        self._xs = xs.flatten()
        self._ys = ys.flatten()
        self._gamma_psi = gamma_psi
        q_disabled = (gamma_psi == 0.0 and gamma_rho == 0.0)
        cols = list(ANCESTOR_COLUMNS)
        if q_disabled:
            for c in ("gamma_coef", "Delta_v", "Delta_u", "Delta_r"):
                cols.remove(c)
        if gamma_rho != 0.0:
            cols += EXTENSION_COLUMNS
        if noise_enabled:
            cols.append(NOISE_COLUMN)
        self.columns = cols
        self._chunk_ticks = chunk_ticks
        self._frames: List[pd.DataFrame] = []
        self._ticks_buffered = 0
        self._writer: Optional[pq.ParquetWriter] = None
        self._schema: Optional[pa.Schema] = None
        self._path: Optional[str] = None
        self.rows_written = 0
        self.rho_global_table: List[tuple] = []   # (tick, rho_global) tick-level table (§7.2)

    # -- sink --------------------------------------------------------------
    def sink(self, tick: int, fields: Dict[str, np.ndarray]) -> None:
        n = self._xs.size
        data: Dict[str, np.ndarray] = {
            "Tick": np.full(n, tick, dtype=np.int64),
            "Agent_X": self._xs.astype(np.int64),
            "Agent_Y": self._ys.astype(np.int64),
        }
        for col in self.columns:
            if col in data:
                continue
            if col == "gamma_coef":
                data[col] = np.full(n, self._gamma_psi, dtype=np.float64)
            else:
                data[col] = np.asarray(fields[col]).reshape(-1)
        if "rho_global" in fields:
            self.rho_global_table.append((tick, float(fields["rho_global"])))
        self._frames.append(pd.DataFrame(data, columns=self.columns))
        self._ticks_buffered += 1
        if self._path is not None and self._ticks_buffered >= self._chunk_ticks:
            self._flush()

    # -- parquet streaming (ancestor pattern: schema from first chunk, snappy) ----
    def open(self, path: str) -> None:
        self._path = path

    def _flush(self) -> None:
        if not self._frames:
            return
        df = pd.concat(self._frames, ignore_index=True)
        if self._writer is None:
            table = pa.Table.from_pandas(df, preserve_index=False)
            self._schema = table.schema
            self._writer = pq.ParquetWriter(self._path, self._schema, compression="snappy")
            self._writer.write_table(table)
        else:
            table = pa.Table.from_pandas(df, preserve_index=False, schema=self._schema)
            self._writer.write_table(table)
        self.rows_written += len(df)
        self._frames.clear()
        self._ticks_buffered = 0

    def close(self) -> None:
        if self._path is not None:
            self._flush()
        if self._writer is not None:
            self._writer.close()
            self._writer = None

    # -- in-memory access (harness/test use) -------------------------------
    def frame(self) -> pd.DataFrame:
        """Concatenated buffered frames. ONLY valid in pure in-memory use: if the
        writer was opened for streaming, buffered frames are a partial tail and
        returning them would silently misrepresent the run (L2 code-audit D6)."""
        if self._path is not None:
            raise RuntimeError("frame() is unavailable on a streaming writer: rows have "
                               "been flushed to disk; read the parquet file instead")
        return pd.concat(self._frames, ignore_index=True) if self._frames else pd.DataFrame(columns=self.columns)


def telemetry_digest(paths: List[str]) -> str:
    """Spec §7.3 canonical construction: SHA-256 over the concatenation of the files'
    raw bytes in ascending lexicographic FILENAME order, each preceded by its filename
    as a UTF-8 line ('<name>\\n'). Filenames therefore enter the digest; the run record
    is outside every digest it reports."""
    names = [os.path.basename(p) for p in paths]
    if len(set(names)) != len(names):
        raise ValueError("telemetry_digest requires unique basenames: the canonical "
                         "construction is filename-keyed (L2 code-audit D6)")
    h = hashlib.sha256()
    for p in sorted(paths, key=lambda q: os.path.basename(q)):
        h.update((os.path.basename(p) + "\n").encode("utf-8"))
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    return h.hexdigest()
```

# ARTIFACT 5: mfa_instrument/gates/gate_a.py
```python
"""mfa_instrument.gates.gate_a — Gate A: Lineage A preservation (bit-exact, conditional).

Spec anchors: Merge Specification v0.4 FROZEN §8.1 — two-level harness:
  STRUCTURAL PREFLIGHT (diagnostic, never a substitute): six checks establishing that
  the Gate-A configuration executes no extension path;
  BEHAVIORAL CERTIFICATION (the actual gate): complete matched-seed comparison against
  flight2_production.py — bit-exact state and telemetry equality.

PROVISIONAL vs AUTHORITATIVE (Build Plan v0.2, L2 finding 1): any run of this harness
during build is a CHECKPOINT; the certification is only the final run on the complete
integrated stage-1 commit, on Mike's machine, under the frozen environment. Every
report emitted here is labeled accordingly.

The ancestor is IMPORTED FROM THE PINNED SOURCE FILE (never transcribed): the
comparison target is flight2_production.NumpyEEModel itself.
"""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
import pandas as pd

from ..config import RunConfig, QConfig, InitConfig
from ..rng import SeedRegistry, RoleError
from ..init import initialize
from ..dynamics import Dynamics
from ..telemetry import TelemetryWriter, ANCESTOR_COLUMNS

GATE_A_SEED = 0x7A9B31C          # facts v1.1 S6(a): the matched seed
ANCESTOR_GAMMA_Q = 0.001          # ancestor GAMMA_Q; Gate-A gamma_psi


def load_ancestor(pinned_repo_root: str):
    """Import the ancestor module from the pinned clone (source of truth)."""
    path = (pinned_repo_root +
            "/flights/cycle2_round1/02_flight_1_v1_1_parity/flight2_production.py")
    spec = importlib.util.spec_from_file_location("flight2_production", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["flight2_production"] = mod
    spec.loader.exec_module(mod)
    return mod


def gate_a_config(f_form: str, grid_scale: int, ticks: int) -> RunConfig:
    """The channels-zeroed Gate-A configuration (spec §8.1): symmetric_chain, A's
    constants (config defaults), u_t = 0 (empty schedule), noise 0 (no stream),
    gamma_rho = 0 (no-read bypass), gamma_psi = ancestor GAMMA_Q, ancestor init
    parameters, ancestor-existing f_form (F_canonical has no ancestor branch)."""
    if f_form == "F_canonical":
        raise ValueError("Gate A requires an ancestor-existing F form (no F_canonical "
                         "branch exists at 4d9a622)")
    return RunConfig(
        seed=GATE_A_SEED, rule_mode="symmetric_chain", f_dispatch=f_form,
        grid_scale=grid_scale, ticks=ticks,
        q=QConfig(q_read="local", gamma_psi=ANCESTOR_GAMMA_Q, gamma_rho=0.0),
        init=InitConfig(),                     # m=0.75, w=0.3 => U(0.6, 0.9); p=0.5
        allow_legacy_f_baseline=(f_form == "F_baseline"),
    )


@dataclass
class PreflightReport:
    checks: List[Tuple[str, bool]] = field(default_factory=list)

    def record(self, name: str, ok: bool) -> None:
        self.checks.append((name, ok))

    @property
    def passed(self) -> bool:
        return all(ok for _, ok in self.checks)


def structural_preflight(cfg: RunConfig) -> PreflightReport:
    """Spec §8.1's six checks, run on a short constructed execution. Diagnostic only."""
    rep = PreflightReport()
    # (i) Gate-A registry forbids every non-ancestor stream (absence, not idleness).
    reg = SeedRegistry(cfg.seed, gate_a_mode=True)
    try:
        reg.role("noise")
        rep.record("noise_stream_absent", False)
    except RoleError:
        rep.record("noise_stream_absent", True)
    dyn = reg.dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    d = Dynamics(cfg, state, dyn)
    # (ii) no rho read is configured; the activation-read branch is unreachable.
    rep.record("no_rho_read_configured", d._rho_read is False)
    # (iii) telemetry schema: extension columns structurally absent.
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho, False)
    rep.record("delta_from_rho_structurally_absent",
               "Delta_from_rho" not in tw.columns and "Delta_from_Psi" not in tw.columns)
    rep.record("noise_column_absent", "Noise_Draw" not in tw.columns)
    # (iv) rho_global never computed: run ticks, assert tick table stays empty.
    seen = {}
    for _ in range(3):
        d.step(lambda t, f: seen.update(f))
    rep.record("rho_global_never_emitted", "rho_global" not in seen
               and len(tw.rho_global_table) == 0)
    # (v) dynamics-stream consumption equals ancestor expectation:
    #     init draws = 4 * n_cells scalars (v,u,r,activity per cell); per tick = one
    #     grid-shaped draw. An independent probe replays exactly that consumption.
    n = cfg.n_cells
    probe = np.random.default_rng(cfg.seed)
    for _ in range(n):
        probe.uniform(0.6, 0.9); probe.uniform(0.6, 0.9); probe.uniform(0.6, 0.9)
        probe.random()
    for _ in range(3):
        probe.random(size=(cfg.grid_scale, cfg.grid_scale))
    rep.record("draw_count_and_order_match",
               bool(np.array_equal(d._g.random(7), probe.random(7))))
    return rep


FROZEN_PYTHON_PREFIX = "3.14."     # spec §7.4 working assumption (executable hard-fail)
FROZEN_NUMPY = "2.4.4"             # spec §7.4 lock-file pin


@dataclass
class GateAReport:
    label: str                     # "PROVISIONAL" or "AUTHORITATIVE"
    f_form: str
    grid_scale: int
    ticks: int
    preflight: PreflightReport
    state_bit_exact: bool
    telemetry_bit_exact: bool
    environment: str

    @property
    def passed(self) -> bool:
        return self.state_bit_exact and self.telemetry_bit_exact

    def summary(self) -> str:
        return (f"GATE A [{self.label}] f={self.f_form} grid={self.grid_scale} "
                f"ticks={self.ticks} preflight={'PASS' if self.preflight.passed else 'FAIL'} "
                f"state={'BIT-EXACT' if self.state_bit_exact else 'DIVERGED'} "
                f"telemetry={'BIT-EXACT' if self.telemetry_bit_exact else 'DIVERGED'} "
                f"env={self.environment}")


def run_gate_a(pinned_repo_root: str, f_form: str, grid_scale: int, ticks: int,
               label: str = "PROVISIONAL") -> GateAReport:
    """Behavioral comparison: the ancestor class itself vs. the merged instrument,
    matched seed, full state + full telemetry rows, bitwise."""
    import platform
    anc_mod = load_ancestor(pinned_repo_root)
    cfg = gate_a_config(f_form, grid_scale, ticks)

    # Ancestor: its own class, its own module-level PRNG_SEED (verify it matches).
    assert anc_mod.PRNG_SEED == GATE_A_SEED, "ancestor seed constant mismatch"
    anc = anc_mod.NumpyEEModel((grid_scale, grid_scale), f_form)

    # Ours.
    reg = SeedRegistry(cfg.seed, gate_a_mode=True)
    dyn = reg.dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    ours = Dynamics(cfg, state, dyn)
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho, False)

    state_ok = True
    telem_ok = True
    for _ in range(ticks):
        anc.step()
        ours.step(tw.sink)
        state_ok &= (np.array_equal(ours._v, anc.v) and
                     np.array_equal(ours._u_base, anc.u) and
                     np.array_equal(ours._r, anc.r) and
                     np.array_equal(ours._is_active, anc.is_active))
        if not state_ok:
            break

    if state_ok:
        anc_df = pd.DataFrame(anc.telemetry_buffer)[ANCESTOR_COLUMNS]
        our_df = tw.frame()[ANCESTOR_COLUMNS]
        telem_ok = anc_df.shape == our_df.shape and all(
            np.array_equal(anc_df[c].to_numpy(), our_df[c].to_numpy())
            for c in ANCESTOR_COLUMNS)
    else:
        telem_ok = False

    env = f"python{platform.python_version()}/numpy{np.__version__}"
    env_conforms = (platform.python_version().startswith(FROZEN_PYTHON_PREFIX)
                    and np.__version__ == FROZEN_NUMPY)
    if label == "AUTHORITATIVE" and not env_conforms:
        raise RuntimeError(
            f"AUTHORITATIVE Gate A refused: environment {env} does not conform to the "
            f"frozen pins (python {FROZEN_PYTHON_PREFIX}x / numpy {FROZEN_NUMPY}); "
            "run on the canonical venv (L2 code-audit D5). PROVISIONAL runs may proceed "
            "in non-conforming environments and are labeled accordingly.")
    if not env_conforms:
        env += " [NON-CONFORMING: provisional only]"
    return GateAReport(label=label, f_form=f_form, grid_scale=grid_scale, ticks=ticks,
                       preflight=structural_preflight(cfg),
                       state_bit_exact=bool(state_ok), telemetry_bit_exact=bool(telem_ok),
                       environment=env)
```

# ARTIFACT 6: mfa_instrument/verify.py
```python
"""mfa_instrument.verify — Tier-1 row-level recomputation (the verification spine).

Spec anchors: Merge Specification v0.4 FROZEN §7.2 — realization invariant, drive
decomposition recomputation, Q decomposition recomputation, Λ recomputation per
dispatch label — streamed over the written telemetry, batch-wise, so verification
never trusts in-memory state. Plus Contract E1 v0.8 §2's bit-identity base check
(total-Q-disable conformance) as a streaming invariant.

Every check recomputes from PERSISTED columns only: a check that consulted live model
state could pass for the wrong reason (pessimistic-on-passing applied to the harness).
Exact equality (==) is used wherever the telemetry writes the very arrays the dynamics
computed; recomputed-expression checks use exact equality too, because the recomputation
reproduces the frozen FP ordering — any tolerance would hide ordering divergence, which
is precisely what Tier-1 exists to catch.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
import pyarrow.parquet as pq

from .config import RunConfig


@dataclass
class Tier1Report:
    checks: Dict[str, int] = field(default_factory=dict)   # name -> mismatch count
    rows_seen: int = 0
    ticks_seen: Tuple[int, int] = (0, 0)

    def record(self, name: str, mismatches: int) -> None:
        self.checks[name] = self.checks.get(name, 0) + int(mismatches)

    @property
    def passed(self) -> bool:
        return all(v == 0 for v in self.checks.values())

    def summary(self) -> str:
        parts = [f"{k}={'OK' if v == 0 else f'{v} MISMATCHES'}" for k, v in self.checks.items()]
        return (f"TIER-1 rows={self.rows_seen} ticks={self.ticks_seen[0]}..{self.ticks_seen[1]} "
                + " ".join(parts) + (" => PASS" if self.passed else " => FAIL"))


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def tier1_verify(parquet_path: str, cfg: RunConfig, batch_size: int = 200_000) -> Tier1Report:
    """Stream the telemetry file and recompute every Tier-1 invariant.

    Applicable to symmetric_chain telemetry (the ancestor family). Column presence is
    schema-driven: Q checks run only where Q columns exist; decomposition checks only
    where the rho channel wrote them.
    """
    rep = Tier1Report()
    pf = pq.ParquetFile(parquet_path)
    cols = {c for c in pf.schema_arrow.names}
    k = cfg.constants

    t_min: Optional[int] = None
    t_max: Optional[int] = None

    for batch in pf.iter_batches(batch_size=batch_size):
        df = batch.to_pandas()
        n = len(df)
        rep.rows_seen += n
        t_min = int(df["Tick"].min()) if t_min is None else min(t_min, int(df["Tick"].min()))
        t_max = int(df["Tick"].max()) if t_max is None else max(t_max, int(df["Tick"].max()))

        # 1. Realization invariant (spec §7.2): is_active == (PRNG_draw < p_act).
        rep.record("realization_invariant",
                   int((df["is_active"] != (df["PRNG_draw"] < df["p_act"])).sum()))

        # 2. Λ recomputation per dispatch label, from the persisted base columns.
        v, u, r = (df["b_i_v"].to_numpy(), df["b_i_u"].to_numpy(), df["b_i_r"].to_numpy())
        lam_mult = v * u * r
        lam_add = k.w_v * v + k.w_u * u + k.w_r * r
        rep.record("lambda_multiplicative",
                   int((df["Lambda_multiplicative"].to_numpy() != lam_mult).sum()))
        rep.record("lambda_additive",
                   int((df["Lambda_additive"].to_numpy() != lam_add).sum()))
        f = cfg.f_dispatch
        if f == "F_baseline":
            lam = (v + u + r) / 3.0
        elif f == "F_LR":
            lam = np.minimum(np.minimum(v, u), r)
        elif f == "F_2_symmetric":
            lam = lam_mult * lam_add
        else:  # F_canonical
            lam = lam_mult
        rep.record("lambda_total_dispatch",
                   int((df["Lambda_total"].to_numpy() != lam).sum()))

        # 3. Drive decomposition (exact FP ordering of the frozen chain).
        dens = df["Local_Density"].to_numpy()
        term_lambda = k.alpha * df["Lambda_total"].to_numpy()
        term_dens = k.beta * dens
        term_over = -k.delta * (dens ** 2)
        term_off = np.full_like(v, -k.gamma_offset)
        drive = term_lambda + term_dens + term_over + term_off
        # u_t reconstruction per persisted tick (schedule is config-frozen).
        u_t_col = np.zeros(n, dtype=np.float64)
        if cfg.drive_schedule:
            ticks = df["Tick"].to_numpy()
            for start, val in cfg.drive_schedule:
                u_t_col = np.where(ticks >= start, val, u_t_col)
            nonzero = u_t_col != 0.0
            drive = np.where(nonzero, drive + u_t_col, drive)
        if "Noise_Draw" in cols:
            drive = drive + df["Noise_Draw"].to_numpy()
        rep.record("term_lambda", int((df["Term_Lambda"].to_numpy() != term_lambda).sum()))
        rep.record("term_density_pos", int((df["Term_Density_Pos"].to_numpy() != term_dens).sum()))
        rep.record("term_overcrowding", int((df["Term_Overcrowding"].to_numpy() != term_over).sum()))
        rep.record("drive_raw", int((df["Drive_Raw"].to_numpy() != drive).sum()))

        # 4. Probability chain.
        p_base = _sigmoid(df["Drive_Raw"].to_numpy())
        p_act = np.clip(p_base + k.eta_floor * (1.0 - p_base), 0.0, 1.0)
        rep.record("p_base", int((df["p_base"].to_numpy() != p_base).sum()))
        rep.record("p_act", int((df["p_act"].to_numpy() != p_act).sum()))

        # 5. Q decomposition (only where the schema carries it).
        if "Delta_v" in cols:
            psi = df["Psi_local"].to_numpy()
            if "Delta_from_rho" in cols:
                total = df["Delta_from_Psi"].to_numpy() + df["Delta_from_rho"].to_numpy()
                rep.record("q_decomposition_sum",
                           int((df["Delta_v"].to_numpy() != total).sum()))
                if cfg.q.gamma_psi != 0.0:
                    rep.record("delta_from_psi",
                               int((df["Delta_from_Psi"].to_numpy()
                                    != cfg.q.gamma_psi * psi).sum()))
                if cfg.q.q_read == "local":
                    rep.record("delta_from_rho_local",
                               int((df["Delta_from_rho"].to_numpy()
                                    != cfg.q.gamma_rho * dens).sum()))
            else:
                rep.record("q_ancestor_expression",
                           int((df["Delta_v"].to_numpy() != cfg.q.gamma_psi * psi).sum()))
            rep.record("q_uniform_across_bases",
                       int((df["Delta_v"].to_numpy() != df["Delta_u"].to_numpy()).sum()
                           + (df["Delta_v"].to_numpy() != df["Delta_r"].to_numpy()).sum()))

    rep.ticks_seen = (t_min or 0, t_max or 0)
    return rep


def e1_base_bit_identity(parquet_path: str, batch_size: int = 200_000) -> Tier1Report:
    """Contract E1 v0.8 §2 conformance: under total-Q-disable, b_i_v/u/r are
    bit-identical at every tick to their tick-0 values, streamed cell-wise.
    Also asserts the Q columns are structurally absent (the schema check)."""
    rep = Tier1Report()
    pf = pq.ParquetFile(parquet_path)
    cols = set(pf.schema_arrow.names)
    for q_col in ("Delta_v", "Delta_u", "Delta_r", "gamma_coef"):
        rep.record(f"schema_absent_{q_col}", 0 if q_col not in cols else 1)

    baseline: Dict[Tuple[int, int], Tuple[float, float, float]] = {}
    for batch in pf.iter_batches(batch_size=batch_size,
                                 columns=["Tick", "Agent_X", "Agent_Y",
                                          "b_i_v", "b_i_u", "b_i_r"]):
        df = batch.to_pandas()
        rep.rows_seen += len(df)
        for row in df.itertuples(index=False):
            key = (row.Agent_X, row.Agent_Y)
            if key not in baseline:
                baseline[key] = (row.b_i_v, row.b_i_u, row.b_i_r)
            else:
                b = baseline[key]
                if (row.b_i_v, row.b_i_u, row.b_i_r) != b:
                    rep.record("base_bit_identity", 1)
    rep.record("base_bit_identity", 0)   # ensure key exists on all-clean runs
    return rep
```

# ARTIFACT 7: tests/test_verify.py
```python
"""Tests for verify.py — Tier-1 streams over WRITTEN parquet, and each check is
demonstrated to actually catch a planted defect (a verifier that cannot fail is not
a verifier: pessimistic-on-passing applied to the harness itself)."""
import sys, os, tempfile
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, "/home/claude/build")
from mfa_instrument.config import RunConfig, QConfig, InitConfig
from mfa_instrument.rng import SeedRegistry
from mfa_instrument.init import initialize
from mfa_instrument.dynamics import Dynamics
from mfa_instrument.telemetry import TelemetryWriter
from mfa_instrument.verify import tier1_verify, e1_base_bit_identity

def run_to_parquet(cfg, path, draw_bases=True):
    reg = SeedRegistry(cfg.seed, gate_a_mode=(cfg.q.gamma_rho == 0.0 and not cfg.drive_schedule
                                              and cfg.noise.amplitude == 0.0))
    dyn = reg.dynamics()
    d = Dynamics(cfg, initialize(cfg.init, cfg.grid_scale, dyn, draw_bases), dyn)
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho,
                         cfg.noise.amplitude > 0, chunk_ticks=5)
    tw.open(path)
    for _ in range(cfg.ticks):
        d.step(tw.sink)
    tw.close()
    return tw

def test_tier1_passes_on_gate_a_style_run():
    cfg = RunConfig(seed=0x7A9B31C, f_dispatch="F_2_symmetric", grid_scale=8, ticks=12,
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = tier1_verify(p, cfg)
        assert rep.passed, rep.summary()
        assert rep.rows_seen == 12 * 64

def test_tier1_passes_with_rho_channel_and_drive():
    cfg = RunConfig(seed=9, f_dispatch="F_canonical", grid_scale=8, ticks=10,
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.02),
                    drive_schedule=((0, 0.0), (4, 0.3)))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = tier1_verify(p, cfg)
        assert rep.passed, rep.summary()

def _corrupt_and_expect(cfg, column, check_name, mutate):
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p)
        df.loc[df.index[37], column] = mutate(df.loc[df.index[37], column])
        p2 = os.path.join(td, "bad.parquet")
        df.to_parquet(p2)
        rep = tier1_verify(p2, cfg)
        assert not rep.passed
        assert rep.checks[check_name] > 0, rep.summary()

def test_tier1_catches_planted_defects():
    cfg = RunConfig(seed=4, f_dispatch="F_LR", grid_scale=8, ticks=6,
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    _corrupt_and_expect(cfg, "is_active", "realization_invariant", lambda x: not x)
    _corrupt_and_expect(cfg, "Lambda_total", "lambda_total_dispatch", lambda x: x + 1e-12)
    _corrupt_and_expect(cfg, "Drive_Raw", "drive_raw", lambda x: x + 1e-9)
    _corrupt_and_expect(cfg, "p_act", "p_act", lambda x: min(1.0, x + 1e-12))
    _corrupt_and_expect(cfg, "Delta_v", "q_ancestor_expression", lambda x: x + 1e-15)

def test_e1_bit_identity_passes_and_catches():
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=8,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = e1_base_bit_identity(p)
        assert rep.passed, rep.summary()
        # plant: drift one base value at tick 5
        df = pd.read_parquet(p)
        idx = df[(df.Tick == 5)].index[3]
        df.loc[idx, "b_i_v"] += 1e-12
        p2 = os.path.join(td, "bad.parquet")
        df.to_parquet(p2)
        rep2 = e1_base_bit_identity(p2)
        assert not rep2.passed and rep2.checks["base_bit_identity"] == 1

def test_e1_bit_identity_rejects_q_columns_in_schema():
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=3,
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = e1_base_bit_identity(p)   # Q columns present => schema checks fail
        assert not rep.passed

def test_become_survive_no_base_draws_policy():
    """D2 policy test: draw_bases=False consumes no base draws — activity placement
    is stream-position-identical to a fresh generator's immediate draws."""
    from mfa_instrument.config import DynamicsConstants
    gs = 6
    cfg = RunConfig(seed=11, rule_mode="become_survive", grid_scale=gs,
                    init=InitConfig(scheme="fixed_count", fixed_count=9),
                    constants=DynamicsConstants(logit_l=-0.405465, kappa=0.2, p_survive=0.4))
    dyn = SeedRegistry(11).dynamics()
    state = initialize(cfg.init, gs, dyn, draw_bases=False)
    assert np.all(state.v == cfg.init.m) and state.v.dtype == np.float64
    ref = np.random.default_rng(11).permutation(gs * gs)   # first consumption is the permutation
    expect = np.zeros(gs * gs, dtype=bool); expect[ref[:9]] = True
    assert np.array_equal(state.is_active.reshape(-1), expect)
```

# ARTIFACT 8: Digests
```
69a23a4d9ca0e2ed1c3a8ed46c75d9120d818d75179e7af99c2c16b48971f366  mfa_instrument/dynamics.py
de124b4aabe2b3fa17ed749beb9a689525daaedf819ae55220e7c1e22313b330  mfa_instrument/init.py
b2b61b3e00cef4bb7ea4bef78eb074362aff852bb6381eec9634d1464a625dbd  mfa_instrument/telemetry.py
27c9504679c58f30171649f4907de1869a8c3667589c46741c30e48a4850213b  mfa_instrument/gates/gate_a.py
3aff7d408ef9e0460a8c3c244b6903ba38d1a84da71f01a9accb89abea3634c7  mfa_instrument/verify.py
7432152625f01cdc1d50fb9e2c4b23f81eb38480e77967a1a9f19e78667784ea  test_verify.py
```
*End of packet.*
