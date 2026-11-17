"""mfa_instrument/f9/spectral.py — Flight 9 module M1: the spectral-relative gain (Contract F9 v0.7
§2.8).

For composition X on a fixed terrain, with A the Moore adjacency of the L×L torus:
    B_X = diag(λ^X)·A/8;   g_spec,X = q/(Δt·spr(B_X));   κ = g/g_spec,X.
Everything here is computed from terrain arrays and the adjacency, before any dynamic data. It is
never normalized by an observed onset, occupancy or fitted edge. If spr = 0 there is no finite
crossing, no division and no level.

THE COMMITTED ROUTINE. spr(diag(λ)·A/8) is computed by power iteration on the similar symmetric
operator D^(1/2)·(A/8)·D^(1/2), D = diag(λ), from the uniform unit vector, stopping when
abs(ray − last) <= F9_SPR_TOL·max(1.0, abs(ray)) between iterations (at most F9_SPR_MAX_ITER
iterations). On the declared arms ray is below 1, so the stop is an ABSOLUTE change of 1e-14 in the
Rayleigh quotient. The Moore sum is the frozen package root's `_moore_sum_a`, imported, so the accumulation
order is the one the specification froze. This is the routine of the committed probe
(`design/flight9/probe/f9_probe.py::spectral_radius`). The value of record is the one the canonical
build computes; a recomputation elsewhere agrees to 1e-9 relative or the discrepancy is recorded.

DOMAIN. The routine is the instrument's for the fifteen declared arms, whose indices are strictly positive: there the
operator is irreducible and aperiodic, its largest eigenvalue is simple and strictly dominant, and the uniform start
has a component along its eigenvector. The function accepts any finite non-negative square array and makes no accuracy
claim outside that domain. With zeros in the index the operator can be periodic and the iteration can stop on a wrong
value: for an 8×8 array that is 1 at (3,3), (2,2), (2,4), (4,3) and 0 elsewhere the spectral radius is sqrt(3)/8 and
the routine returns about 0.1875 (L2, M1 round 1 §7).

ACCURACY OF THE ROUTINE ON THE DECLARED ARMS (measured at build, container, 2026-11-16; a property, not a claim of the
contract). The
Rayleigh quotient of a symmetric operator never exceeds its largest eigenvalue, and the stopping rule looks at its
change, not at its error, so the returned value sits slightly below the true spectral radius. Against an implicitly
restarted Lanczos eigenvalue (scipy eigsh, tol 1e-14) the routine is low by at most 3.0e-12 relative across the fifteen
arms. `test_f9_m1.py` repeats the comparison wherever scipy is installed and holds it to the contract's 1e-9.
"""
from __future__ import annotations

import math

import numpy as np

from ..config import MICRO_UNITS
from ..dynamics import _moore_sum_a
from . import config as C
from .config import F9ConfigError


def spectral_radius(lam: np.ndarray, *, tol: float = C.F9_SPR_TOL, max_iter: int = C.F9_SPR_MAX_ITER) -> float:
    """The committed routine's value for spr(diag(lam)·A/8). Of record for the declared arms only (see DOMAIN above).
    Returns 0.0 when lam is identically zero."""
    lam = np.asarray(lam, dtype=np.float64)
    if lam.ndim != 2 or lam.shape[0] != lam.shape[1] or not np.all(np.isfinite(lam)) or float(lam.min()) < 0.0:
        raise F9ConfigError("the index must be a finite, non-negative square array")
    if float(lam.max()) <= 0.0: return 0.0
    s = np.sqrt(lam)
    w = np.ones_like(lam) / math.sqrt(lam.size)
    last = 0.0
    for _ in range(max_iter):
        z = s * _moore_sum_a(s * w) / 8.0
        ray = float(np.sum(w * z))
        n = float(np.linalg.norm(z))
        if n == 0.0: return 0.0
        w = z / n
        if abs(ray - last) <= tol * max(1.0, abs(ray)): return ray
        last = ray
    raise F9ConfigError("spectral_radius: no convergence within the declared iterations")


def g_spec(lam: np.ndarray) -> float:
    """g_spec,X = q/(Δt·spr(B_X)). Raises when spr = 0: there is no finite crossing and no level (§2.8)."""
    spr = spectral_radius(lam)
    if spr <= 0.0: raise F9ConfigError("spr = 0: no finite crossing, no division, no level (contract §2.8)")
    return C.q_deact() / (C.F9_DT * spr)


def gain(level_micro: int, g_spec_value: float) -> float:
    """The raw gain g at a declared κ level: g = κ·g_spec,X."""
    C.level_id(level_micro)                           # refuses an undeclared level
    return (level_micro / MICRO_UNITS) * g_spec_value


def local_m(lam: np.ndarray, g: float) -> np.ndarray:
    """The per-cell quantity m_i = g·λ_i·Δt/q, persisted beside κ (§2.8). On a flat terrain at κ = 1 it equals 1."""
    return g * np.asarray(lam, dtype=np.float64) * C.F9_DT / C.q_deact()
