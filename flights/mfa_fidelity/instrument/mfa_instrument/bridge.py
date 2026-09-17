"""mfa_instrument/bridge.py — the projection bridge: pure, measurement-side computations of the
four R0 quantities (Merge Specification v0.4 FROZEN §8.3; MFP v1.1 §4; R0 design note; departure-
statistic set DECLARED by Mike 2026-09-16).

NEVER imported by dynamics.py; nothing here feeds Q. Inputs are grids and emitted fields; outputs
are numbers. Every input is validated fail-closed — dtype, shape, emptiness, finiteness, and
architectural domain — and never coerced or broadcast; undefined statistics are REFUSED
(BridgeDomainError), never returned as 0 or as a nonfinite value.

Exactness (stated narrowly): on Gate R0's CONSTRUCTED cases — dyadic values on a power-of-two grid —
the arithmetic below is exact sums followed by a single correctly rounded division (or an exact
square root of a perfect square), so results equal float(Fraction) bit for bit. No such claim is
made for general R1 data; there the bridge is ordinary float64 arithmetic in a fixed, declared order.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

_MOORE_OFFSETS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


class BridgeDomainError(ValueError):
    """The input is outside the bridge's executable domain, or the statistic is undefined on it."""


def _finite_out(x, name: str):
    """Output discipline (L2 R0 r2 1B): a bridge function never returns a nonfinite measurement."""
    if not np.isfinite(np.asarray(x)).all():
        raise BridgeDomainError(f"{name}: nonfinite result refused (overflow or undefined arithmetic)")
    return x


# ----------------------------------------------------------------------------- validation
def _grid_bool(grid) -> np.ndarray:
    g = np.asarray(grid)
    if g.ndim != 2 or g.shape[0] != g.shape[1] or g.size == 0:
        raise BridgeDomainError(f"nonempty square 2-D grid required, got shape {g.shape}")
    if g.dtype == np.bool_:
        return g
    if np.issubdtype(g.dtype, np.integer) and np.isin(g, (0, 1)).all():
        return g.astype(bool)
    raise BridgeDomainError(f"binary grid required, got dtype {g.dtype}")


def _field(x, name: str, shape: Tuple[int, ...] = None, lo: float = None, hi: float = None) -> np.ndarray:
    """A nonempty 2-D float64 field; exact shape when given; finite; within [lo, hi] when given.
    No coercion: a float32 or integer field is refused, not promoted."""
    if not isinstance(x, np.ndarray):
        raise BridgeDomainError(f"{name}: ndarray required, got {type(x).__name__}")
    if x.dtype != np.float64:
        raise BridgeDomainError(f"{name}: float64 required, got {x.dtype}")
    if x.ndim != 2 or x.size == 0:
        raise BridgeDomainError(f"{name}: nonempty 2-D field required, got shape {x.shape}")
    if shape is not None and x.shape != tuple(shape):
        raise BridgeDomainError(f"{name}: shape {x.shape} != required {tuple(shape)}")
    if not np.isfinite(x).all():
        raise BridgeDomainError(f"{name}: nonfinite value")
    if lo is not None and (x < lo).any() or hi is not None and (x > hi).any():
        raise BridgeDomainError(f"{name}: value outside [{lo}, {hi}]")
    return x


def _scalar(x, name: str, lo: float = None, hi: float = None) -> float:
    """A finite float64 / Python-float scalar and only a scalar; no array, no bool, no integer."""
    # The frozen scalar set is {float, np.float64}: every np.ndarray (including shape ()), bool, and
    # integer type is refused (L2 R0 r2 1A).
    if isinstance(x, np.ndarray) or isinstance(x, bool) or isinstance(x, (int, np.integer)) or not isinstance(x, (float, np.float64)):
        raise BridgeDomainError(f"{name}: float scalar required (float or np.float64), got {type(x).__name__}")
    v = float(x)
    if not np.isfinite(v):
        raise BridgeDomainError(f"{name}: nonfinite")
    if lo is not None and v < lo or hi is not None and v > hi:
        raise BridgeDomainError(f"{name}: {v} outside [{lo}, {hi}]")
    return v


# ----------------------------------------------------------------------------- Q1: the local read
def moore_count(grid) -> np.ndarray:
    """Toroidal Moore-neighbourhood active count per cell (integer; order-invariant)."""
    g = _grid_bool(grid).astype(np.int64)
    out = np.zeros_like(g)
    for dx, dy in _MOORE_OFFSETS:
        out += np.roll(np.roll(g, dx, axis=0), dy, axis=1)
    return out


def local_density(grid) -> np.ndarray:
    """Local_Density: Moore active count / 8 (§3.2, symmetric_chain read)."""
    return moore_count(grid).astype(np.float64) / 8.0


# ----------------------------------------------------------------------------- Q2: aggregate rho
def rho_global(grid) -> float:
    """Aggregate rho: the grid mean — exact integer sum, one division. Pre-update semantics (§4.1)
    are the CALLER's obligation: pass the pre-update grid."""
    g = _grid_bool(grid)
    return _finite_out(float(np.float64(int(g.sum())) / np.float64(g.size)), "rho_global")


# ----------------------------------------------------------------------------- Q3: Q response
@dataclass(frozen=True)
class QResponse:
    delta_from_psi: np.ndarray
    delta_from_rho: np.ndarray
    delta: np.ndarray
    v_new: np.ndarray
    u_base_new: np.ndarray
    r_new: np.ndarray
    clipped_v: int
    clipped_u_base: int
    clipped_r: int
    mean_delta_from_psi: float
    mean_delta_from_rho: float
    mean_delta: float


def q_response(psi_local, activation_input, gamma_psi, gamma_rho, v, u_base, r) -> QResponse:
    """The committed extended-Q form (§4.1): delta_b = Γ_Ψ·Ψ_local + Γ_ρ·activation_input, the SAME
    delta added to each base, bases clipped to [0,1], per-base clip counters counting out-of-range
    entries BEFORE the clip (dynamics.py Step 12); decomposition per §4.5; population aggregates as
    exact means. `activation_input` is a full field of the same shape (local read) or a finite float
    scalar (global read) — never broadcast from any other shape."""
    psi = _field(psi_local, "Psi_local")
    shape = psi.shape
    gp = _scalar(gamma_psi, "gamma_psi"); gr = _scalar(gamma_rho, "gamma_rho")
    if isinstance(activation_input, np.ndarray) and activation_input.shape != ():
        ai = _field(activation_input, "activation_input", shape, 0.0, 1.0)
    else:
        ai = np.full(shape, _scalar(activation_input, "activation_input", 0.0, 1.0), dtype=np.float64)
    v = _field(v, "v", shape, 0.0, 1.0); u = _field(u_base, "u_base", shape, 0.0, 1.0); r = _field(r, "r", shape, 0.0, 1.0)
    dpsi = np.float64(gp) * psi
    drho = np.float64(gr) * ai
    delta = dpsi + drho
    vn, un, rn = v + delta, u + delta, r + delta
    cv = int(np.sum((vn < 0.0) | (vn > 1.0))); cu = int(np.sum((un < 0.0) | (un > 1.0))); cr = int(np.sum((rn < 0.0) | (rn > 1.0)))
    n = np.float64(psi.size)
    for arr, nm in ((dpsi, "delta_from_psi"), (drho, "delta_from_rho"), (delta, "delta")):
        _finite_out(arr, nm)
    means = [_finite_out(float(np.float64(np.sum(a)) / n), nm) for a, nm in ((dpsi, "mean_delta_from_psi"), (drho, "mean_delta_from_rho"), (delta, "mean_delta"))]
    return QResponse(dpsi, drho, delta, np.clip(vn, 0.0, 1.0), np.clip(un, 0.0, 1.0), np.clip(rn, 0.0, 1.0), cv, cu, cr, means[0], means[1], means[2])


# ----------------------------------------------------------------------------- Q4: departures
def local_read_dispersion(local_density_field, rho) -> float:
    """Declared statistic 1: population variance of Local_Density about rho_global — mean of squared
    deviations (one division). rho must be a finite density in [0,1]."""
    ld = _field(local_density_field, "Local_Density", None, 0.0, 1.0)
    rr = _scalar(rho, "rho_global", 0.0, 1.0)
    dev = ld - np.float64(rr)
    return _finite_out(float(np.float64(np.sum(dev * dev)) / np.float64(ld.size)), "local_read_dispersion")


def config_neighbourhood_correlation(x, y) -> float:
    """Declared statistic 2a: Pearson correlation across cells between a configuration quantity and
    Local_Density (numerator and denominator over the same N, so the ddof convention cancels).
    REFUSED when either variance is 0; inputs must be nonempty float64 fields of equal shape."""
    xa = _field(x, "x"); ya = _field(y, "y", xa.shape)
    n = np.float64(xa.size)
    dx = xa - np.float64(np.sum(xa)) / n
    dy = ya - np.float64(np.sum(ya)) / n
    sxx = np.float64(np.sum(dx * dx)); syy = np.float64(np.sum(dy * dy)); sxy = np.float64(np.sum(dx * dy))
    if not (np.isfinite(sxx) and np.isfinite(syy) and np.isfinite(sxy)):
        raise BridgeDomainError("correlation: nonfinite intermediate refused (overflow)")
    if sxx == 0.0 or syy == 0.0:
        raise BridgeDomainError("correlation undefined: zero variance")
    # Stable denominator (L2 R0 r3 item 2): sqrt(sxx)·sqrt(syy), never sqrt(sxx·syy) — two individually
    # finite variances can have an overflowing product, which would yield a FALSE finite zero.
    den = np.float64(np.sqrt(sxx)) * np.float64(np.sqrt(syy))
    if not (np.isfinite(den) and den > 0.0):
        raise BridgeDomainError("correlation: nonfinite or zero denominator refused")
    return _finite_out(float(sxy / den), "config_neighbourhood_correlation")


def morans_i(grid) -> float:
    """Declared statistic 2b: Moran's I of is_active under toroidal Moore weights (w_ij = 1 for the
    eight neighbours, no self-weight): I = Σ_i (x_i−x̄)·Σ_{j∈Moore(i)} (x_j−x̄) / (8·Σ_i (x_i−x̄)²).
    REFUSED when the grid is constant."""
    g = _grid_bool(grid).astype(np.float64)
    n = np.float64(g.size)
    d = g - np.float64(np.sum(g)) / n
    denom = np.float64(np.sum(d * d))
    if denom == 0.0:
        raise BridgeDomainError("Moran's I undefined: constant grid")
    lag = np.zeros_like(d)
    for dx, dy in _MOORE_OFFSETS:
        lag += np.roll(np.roll(d, dx, axis=0), dy, axis=1)
    return _finite_out(float(np.float64(np.sum(d * lag)) / (np.float64(8.0) * denom)), "morans_i")


def base_distribution_dispersion(v, u_base, r) -> Dict[str, Tuple[float, float]]:
    """Declared statistic 3: per-base population mean and population variance (ddof=0, one division
    each) of (v, u_base, r); the three fields must share one nonempty shape and lie in [0,1]."""
    va = _field(v, "v", None, 0.0, 1.0); ua = _field(u_base, "u_base", va.shape, 0.0, 1.0); ra = _field(r, "r", va.shape, 0.0, 1.0)
    out = {}
    for name, a in (("v", va), ("u_base", ua), ("r", ra)):
        n = np.float64(a.size)
        m = np.float64(np.sum(a)) / n
        dev = a - m
        out[name] = (_finite_out(float(m), f"base_mean_{name}"), _finite_out(float(np.float64(np.sum(dev * dev)) / n), f"base_var_{name}"))
    return out
