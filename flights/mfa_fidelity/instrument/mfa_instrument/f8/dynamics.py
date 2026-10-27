"""mfa_instrument/f8/dynamics.py — Flight 8 module M1 (substrate half): the hazard rule, executed exactly as
Contract F8 v0.8.4 §2.1–§2.9 writes it, and nothing else.

THE RULE (per cell i on the L×L periodic Moore lattice, x_i ∈ {0, 1}, tick dt = 1; §2.4):
    inactive → active:   P_i = 1 − exp(−[eta_floor + g·lambda_bar·d_i(t)]·dt)
    active → inactive:   P_i = 1 − exp(−mu·dt)
with d_i(t) the active fraction of the eight Moore neighbours at t (§2.3), lambda_i = lambda_bar homogeneous (§2.2).
No other term: no overcrowding, no gamma_offset, no sigma(drive) chain (§2.4, last sentence). Q off, drive 0, noise off.

TIMING (§2.5): synchronous two-phase advance — read all probabilities from the state at t; ONE full-grid uniform
draw (one uniform per cell per tick, from the run's own Generator); advance all simultaneously. The uniform decides
both directions: an inactive cell activates iff u < P_act; an active cell stays active iff u >= P_deact.

OBJECTS (§2.6, §2.9, §4.1): skeleton_high (eta_floor = 0, all active at t = 0); skeleton_low (eta_floor = 0, a
fraction rho0 = 0.02 of cells active, chosen uniformly at random from the declared INIT_LOW stream); realization
(eta_floor = eta0, stationary-null start pi_1 = a/(a + q) drawn cell-wise from the run stream, no burn-in); null
(g = 0, eta_floor = eta0, same stationary start) — each cell then an independent two-state chain.

RECORD. rho[0] is the density at t = 0 (after initialization, before any tick); rho[t] for t = 1..T is the density
after tick t. The tail is the last `tail_ticks` entries rho[T − tail + 1 .. T], split into non-overlapping windows
of `window` ticks in order. Survival (skeleton) = active count > 0 at every tick of every tail window. An extinct skeleton run
stops advancing (the all-inactive state is exactly absorbing at eta_floor = 0; the remaining densities are exactly
0) and is a valid observation, never "missing" (§4.11). The Moore accumulation uses the frozen package's verbatim
offset order (`mfa_instrument.dynamics._moore_sum_a`), imported, not copied.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np

from ..dynamics import _moore_sum_a
from . import config as C
from .config import F8RunSpec, F8ConfigError


class F8DynamicsError(RuntimeError):
    """The stepper was asked to do something the frozen rule does not define."""


def activation_probability(eta_floor: float, g: float, lambda_bar: float, d: np.ndarray, dt: int = C.F8_DT) -> np.ndarray:
    """P_act = 1 − exp(−[eta_floor + g·lambda_bar·d]·dt), in the contract's written form (float64)."""
    return 1.0 - np.exp(-(eta_floor + g * lambda_bar * d) * dt)


def deactivation_probability(mu: float, dt: int = C.F8_DT) -> float:
    return 1.0 - math.exp(-mu * dt)


def stationary_pi1(eta_floor: float, mu: float, dt: int = C.F8_DT) -> float:
    """pi_1 = a/(a + q), a = 1 − e^(−eta_floor dt), q = 1 − e^(−mu dt) (§2.9)."""
    a = 1.0 - math.exp(-eta_floor * dt); q = deactivation_probability(mu, dt)
    return a / (a + q) if (a + q) > 0 else 0.0


def local_density(x: np.ndarray) -> np.ndarray:
    """d_i = (number of active Moore neighbours of i)/8, periodic boundaries, frozen offset order (§2.3)."""
    return _moore_sum_a(x.astype(np.float64)) / 8.0


def initial_state(spec: F8RunSpec, gen: np.random.Generator) -> np.ndarray:
    """The t = 0 state for the spec's object. The realization/null draw consumes the run stream's first full-grid
    uniform; the skeleton-low pattern comes from the declared INIT_LOW stream; skeleton-high draws nothing."""
    L = spec.grid
    if spec.obj == "skeleton_high":
        return np.ones((L, L), dtype=bool)
    if spec.obj == "skeleton_low":
        k = int(round(spec.n_cells * C.F8_RHO0_LOW_MICRO / C.MICRO_UNITS))
        idx = C.init_low_generator(spec.seed, spec.level_micro).choice(spec.n_cells, size=k, replace=False)
        x = np.zeros(spec.n_cells, dtype=bool); x[idx] = True
        return x.reshape(L, L)
    if spec.obj in ("realization", "null"):
        pi1 = stationary_pi1(spec.eta_floor, spec.mu)
        return gen.random((L, L)) < pi1
    raise F8DynamicsError(f"no initialization defined for object {spec.obj!r}")


def step(x: np.ndarray, u: np.ndarray, *, eta_floor: float, g: float, lambda_bar: float, mu: float, dt: int = C.F8_DT) -> np.ndarray:
    """One synchronous tick of the hazard rule from state x with the full-grid uniform u (§2.4–§2.5)."""
    p_act = activation_probability(eta_floor, g, lambda_bar, local_density(x), dt)
    p_de = deactivation_probability(mu, dt)
    return np.where(x, u >= p_de, u < p_act)


@dataclass(frozen=True)
class F8RunResult:
    spec_hash: str
    level_micro: int
    level_id: str
    seed: int
    obj: str
    rho: np.ndarray                 # float64, length ticks + 1; rho[0] at t = 0
    active_counts: np.ndarray       # int64, length ticks + 1
    extinction_tick: Optional[int]  # first t with zero active cells (skeleton); None otherwise
    ticks_advanced: int             # ticks actually stepped (an extinct skeleton stops early)
    tail_window_means: Tuple[float, ...]
    survival: bool                  # every tail window has active count > 0
    rho_tail_mean: float            # mean density over the tail ticks (extinct → 0.0 contributions, §4.11)
    stream_key: Tuple[int, int, int]
    draws_consumed: int             # full-grid uniform draws from the run stream (init draw included for realization/null)

    def rho_sha256(self) -> str:
        return hashlib.sha256(np.ascontiguousarray(self.rho, dtype=np.float64).tobytes()).hexdigest()


def run(spec: F8RunSpec) -> F8RunResult:
    """Execute one run of the frozen rule under the spec; adjudicates nothing."""
    spec = C.validate_run_spec(spec)        # full reconstruction; execution uses only the reconstructed spec (L2 M1 r1 D2)
    if spec.stream_key != C.stream_key(spec.seed, spec.obj, spec.level_micro):
        raise F8ConfigError("recorded stream key differs from the derivation")
    gen = C.generator_from_key(spec.stream_key)    # the executed stream IS the recorded key
    L, T, n = spec.grid, spec.ticks, spec.n_cells
    draws = 0
    x = initial_state(spec, gen)
    if spec.obj in ("realization", "null"): draws += 1
    counts = np.zeros(T + 1, dtype=np.int64); counts[0] = int(np.count_nonzero(x))
    absorbing = spec.eta_floor == 0.0
    extinction: Optional[int] = 0 if (absorbing and counts[0] == 0) else None
    advanced = 0
    for t in range(1, T + 1):
        if extinction is not None:
            break                                  # exactly absorbing: all remaining counts stay 0 (already zero-filled)
        u = gen.random((L, L)); draws += 1
        x = step(x, u, eta_floor=spec.eta_floor, g=spec.g, lambda_bar=spec.lambda_bar, mu=spec.mu)
        advanced = t
        counts[t] = int(np.count_nonzero(x))
        if absorbing and counts[t] == 0:
            extinction = t
    rho = counts.astype(np.float64) / np.float64(n)
    tail = rho[T - spec.tail_ticks + 1:]
    nwin = spec.tail_ticks // spec.window
    wins = tuple(float(tail[i * spec.window:(i + 1) * spec.window].mean()) for i in range(nwin))
    tail_counts = counts[T - spec.tail_ticks + 1:]
    # survival (§4.11): active count > 0 throughout every tail window — the MINIMUM over each window, so a run extinct
    # inside the last window does not survive (L1 r2 D5; for the absorbing skeleton this is exactly counts[T] > 0)
    survival = all(int(tail_counts[i * spec.window:(i + 1) * spec.window].min()) > 0 for i in range(nwin))
    return F8RunResult(spec.spec_hash(), spec.level_micro, spec.level_id, spec.seed, spec.obj, rho, counts, extinction, advanced,
                       wins, bool(survival), float(tail.mean()), spec.stream_key, draws)


def write_rho_table(res: F8RunResult, path: str) -> str:
    """Persist the density record as a parquet table ["Tick", "rho_global"] (E1's column grammar; F8 meaning: row t is the
    density AFTER tick t, row 0 the initial density). Returns the file's SHA-256."""
    import pyarrow as pa, pyarrow.parquet as pq
    tbl = pa.table({"Tick": pa.array(np.arange(len(res.rho), dtype=np.int64)), "rho_global": pa.array(res.rho, type=pa.float64())})
    pq.write_table(tbl, path)
    return hashlib.sha256(open(path, "rb").read()).hexdigest()
