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
                 noise: Optional[RoleStream] = None,
                 emit_rho_global: bool = False) -> None:
        self.cfg = cfg
        self._g = dyn.generator
        # L2 review D1(a): ownership by PRIVATE COPIES — the caller's GridState
        # retains no reference to live model state; external mutation is
        # mechanically impossible, not documentation-discouraged.
        self._v = state.v.copy()
        self._u_base = state.u_base.copy()
        self._r = state.r.copy()
        self._is_active = state.is_active.copy()
        # L2 review N1: rho_global is a Gate-R recovery quantity, required in E1
        # local-primary runs where Q never reads it — emission is therefore a
        # run-mode obligation independent of Q configuration.
        self._emit_rho_global = bool(emit_rho_global)
        # N3: mechanically reject configurations this branch does not implement —
        # silent ignoring of a nonzero-Q become_survive config is the named
        # wrong-values defect class. Until the common-Q skeleton exists for
        # become_survive, such configurations are refused at construction.
        if cfg.rule_mode == "become_survive" and (cfg.q.gamma_psi != 0.0
                                                  or cfg.q.gamma_rho != 0.0):
            raise ValueError(
                "become_survive with nonzero Q coefficients is not implemented in "
                "this build phase; the frozen skeleton's Q update for this rule mode "
                "must be built (or the config changed), never silently ignored "
                "(L2 Phase-1 review N3)")
        # N3 twin (Phase-2 item-4 O1, authorized scope expansion, Mike 2026-09-03):
        # the B step consumes no MFA-noise term; a become_survive config carrying
        # nonzero noise amplitude would construct a stream this branch never reads —
        # silent ignoring of an inapplicable channel, the same defect class.
        if cfg.rule_mode == "become_survive" and cfg.noise.amplitude != 0.0:
            raise ValueError(
                "become_survive carries no noise channel; noise.amplitude must be 0.0 "
                "(refused at construction, never silently ignored — item-4 O1)")
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

        # Pre-update rho_global (D2 causal timing when Q consumes it; N1: also a
        # Gate-R recovery artifact requested by run mode regardless of Q's read).
        if (self._rho_read and cfg.q.q_read == "global") or self._emit_rho_global:
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
                # L2 review D1(b): delta is used causally AFTER the sink returns
                # (the Step-12 base update); telemetry receives a COPY so no sink,
                # however misbehaved, can alter the subsequent Q update.
                delta_telem = delta.copy()
                if delta_from_psi is not None:
                    fields["Delta_from_Psi"] = delta_from_psi
                    fields["Delta_from_rho"] = delta_from_rho
                fields["Delta_v"] = delta_telem
                fields["Delta_u"] = delta_telem
                fields["Delta_r"] = delta_telem
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
