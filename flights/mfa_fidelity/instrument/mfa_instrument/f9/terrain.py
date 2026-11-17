"""mfa_instrument/f9/terrain.py — Flight 9 module M1: terrains, compositions, comparison arrays and
their serialization (Contract F9 v0.7 §2.2, §3.1–§3.4).

Every terrain is closed-form on the unit torus: cell (i, j) sits at x = i/L, y = j/L, with i the
index along axis 0 (§3, §3.4 step 2). No random draw, no reference to g, λ-derived thresholds or any
dynamic quantity enters a terrain.

Three different arrays are kept apart, as §3.4 step 3 requires:
  bases (v, u, r)        — the terrain itself; their bytes are the terrain's base identity.
  raw index λ^X          — P = v·u·r or H = (v + u + r)/3; the dynamics and the spectral
                           normalization use this and nothing else.
  comparison array ω     — the array whose level sets are the registered contour family, rounded to
                           12 decimal places. On a same-family terrain it is ONE array for both
                           compositions (the common base t on TA and TD; u on TC). On TB each
                           composition has its own (its raw index, rounded). T0 has none that
                           carries a contour (both indices are constant).

Platform note. cos and tanh go through the platform's libm, which may differ by an ulp between
machines. Nothing here claims bit equality across platforms: the canonical machine's arrays are the
objects of record (§3.4 step 4) and a recomputation elsewhere is compared at 1e-12 (§3.4 step 5).
"""
from __future__ import annotations

import hashlib
from typing import Dict, Tuple

import numpy as np

from . import config as C
from .config import F9ConfigError

Bases = Tuple[np.ndarray, np.ndarray, np.ndarray]


def _axes() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """(x, y) on the unit torus and (X, Y) in cells, each of shape (L, L); axis 0 is the x index."""
    L = C.F9_GRID
    ii = np.arange(L, dtype=np.float64)
    X = ii[:, None] * np.ones((1, L)); Y = np.ones((L, 1)) * ii[None, :]
    return X / L, Y / L, X, Y


def _c(z: np.ndarray) -> np.ndarray:
    return np.cos(2.0 * np.pi * z)


def td_delta(name: str) -> np.ndarray:
    """Signed distance in cells from each cell centre to the edge of the TD core, positive inside (§3.1, §3.2).
    The core is the union of the declared discs, so the distance to its edge is the largest of R − (distance to a centre)."""
    centres, R, _w = C.td_params(name)
    L = C.F9_GRID
    _x, _y, X, Y = _axes()
    best = np.full((L, L), -np.inf)
    for cx, cy in centres:
        dx = np.abs(X - cx); dx = np.minimum(dx, L - dx)
        dy = np.abs(Y - cy); dy = np.minimum(dy, L - dy)
        best = np.maximum(best, R - np.sqrt(dx * dx + dy * dy))
    return best


def td_core(name: str) -> np.ndarray:
    """The core C of a TD variant as a boolean mask: cells whose centre lies inside a disc. Checked against §3.2 on every call."""
    delta = td_delta(name)
    core = delta > 0.0
    if int(core.sum()) != C.F9_TD_CORE_CELLS:
        raise F9ConfigError(f"{name}: core has {int(core.sum())} cells, contract §3.2 requires {C.F9_TD_CORE_CELLS}")
    if float(np.abs(delta).min()) < C.F9_TD_CORE_EDGE_CLEARANCE:
        raise F9ConfigError(f"{name}: a cell centre lies within {C.F9_TD_CORE_EDGE_CLEARANCE} cells of the core's edge")
    return core


def bases(name: str) -> Bases:
    """The three base arrays (v, u, r) of a terrain: float64, shape (L, L), C-contiguous, every value in [0, 1]."""
    if name not in C.F9_TERRAINS: raise F9ConfigError(f"not a declared terrain: {name!r}")
    L = C.F9_GRID
    x, y, _X, _Y = _axes()
    if name == "T0":
        v = np.full((L, L), 0.8); u = v.copy(); r = v.copy()
    elif name == "TA":
        t = 0.6 + 0.15 * (_c(x) + _c(y)); v, u, r = t, t.copy(), t.copy()
    elif name == "TB":
        p = C.tb_params()
        s = p["s0"] + p["a"] * _c(x); d = p["d0"] + p["b"] * _c(y)
        v = s + d; u = s - d; r = np.full((L, L), p["r0"])
    elif name == "TC":
        bump = (((1.0 + _c(x - 0.5)) / 2.0) ** 4) * (((1.0 + _c(y - 0.5)) / 2.0) ** 4)
        v = np.full((L, L), 0.9); r = v.copy(); u = 0.9 - 0.85 * bump
    else:                                             # the four TD variants
        _centres, _R, w = C.td_params(name)
        td_core(name)                                 # the §3.2 checks run before the bases are returned
        t = 0.3 + 0.6 * 0.5 * (1.0 + np.tanh(td_delta(name) / w)); v, u, r = t, t.copy(), t.copy()
    out = tuple(np.ascontiguousarray(b, dtype=np.float64) for b in (v, u, r))
    for b in out:
        if b.shape != (L, L) or not np.all(np.isfinite(b)) or float(b.min()) < 0.0 or float(b.max()) > 1.0:
            raise F9ConfigError(f"{name}: a base is not a finite (L, L) array in [0, 1]")
    return out


def compose(comp: str, v: np.ndarray, u: np.ndarray, r: np.ndarray) -> np.ndarray:
    """The raw index λ^X (§2.2): P = F_canonical = v·u·r; H = F_baseline = (v + u + r)/3 (rival only)."""
    if comp == "P": return v * u * r
    if comp == "H": return (v + u + r) / 3.0
    raise F9ConfigError(f"not a declared composition: {comp!r}")


def raw_index(name: str, comp: str) -> np.ndarray:
    return compose(comp, *bases(name))


def comparison_array(name: str, comp: str) -> np.ndarray:
    """ω for (terrain, composition), rounded to 12 decimal places (§3.4 step 3). Same-family terrains return the same
    array for both compositions. T0's array is constant; its family is empty (§5.5 step 5)."""
    if comp not in C.F9_COMPOSITIONS: raise F9ConfigError(f"not a declared composition: {comp!r}")
    v, u, r = bases(name)
    latent = C.same_family_latent(name)
    src = {"v": v, "u": u}[latent] if latent is not None else compose(comp, v, u, r)
    return np.ascontiguousarray(np.round(src, C.F9_ROUND_PLACES), dtype=np.float64)


def level_label(name: str, comp: str, ell: float) -> float:
    """The composition's own index value on the contour at comparison level ell (§3.4 step 3). A label for the fidelity
    report; it decides nothing."""
    if comp not in C.F9_COMPOSITIONS: raise F9ConfigError(f"not a declared composition: {comp!r}")
    if name not in C.F9_TERRAINS: raise F9ConfigError(f"not a declared terrain: {name!r}")
    if name == "TA" or name.startswith("TD"): return ell ** 3 if comp == "P" else ell
    if name == "TC": return 0.81 * ell if comp == "P" else (1.8 + ell) / 3.0
    if name == "TB": return ell
    raise F9ConfigError(f"no contour label on {name!r}")


def serialize(a: np.ndarray) -> bytes:
    """Little-endian IEEE float64, C order (§3.4 step 2)."""
    a = np.asarray(a)
    if a.shape != (C.F9_GRID, C.F9_GRID): raise F9ConfigError("array is not (L, L)")
    return np.ascontiguousarray(a, dtype="<f8").tobytes(order="C")


def deserialize(raw: bytes) -> np.ndarray:
    n = C.F9_GRID
    if len(raw) != 8 * n * n: raise F9ConfigError("byte length is not that of an (L, L) float64 array")
    return np.frombuffer(raw, dtype="<f8").reshape(n, n).astype(np.float64)


def array_sha256(a: np.ndarray) -> str:
    return hashlib.sha256(serialize(a)).hexdigest()


def base_identity(name: str) -> str:
    """SHA-256 of the bytes of v, then u, then r (§3.4 step 2)."""
    return hashlib.sha256(b"".join(serialize(b) for b in bases(name))).hexdigest()


def tb_variance_shares() -> Dict[str, float]:
    """The x and y shares of the across-cell variance of TB's product (§3.2 criterion). The product is r·(s(x)² − d(y)²),
    additive in x and y, so the shares are the variances of the two row and column means over their sum."""
    lam = raw_index("TB", "P")
    vx = float(np.var(lam.mean(axis=1))); vy = float(np.var(lam.mean(axis=0)))
    return {"x": vx / (vx + vy), "y": vy / (vx + vy), "additive_residual": float(np.var(lam) - vx - vy)}


def monotone_violation(name: str, comp: str) -> float:
    """Following cells in order of increasing ω, the largest fall of the raw index λ^X (§3.3, §3.4 step 3). Zero or of
    rounding size on a same-family terrain; the contract reports 0.0876 for H along P on TB, which is a different
    comparison (see `tb_cross_fall`)."""
    om = comparison_array(name, comp).ravel(); lam = raw_index(name, comp).ravel()
    order = np.lexsort((lam, om))                     # ties in ω broken by λ, so a tie cannot create a spurious fall
    seq = lam[order]
    return float(max(0.0, np.max(np.maximum.accumulate(seq) - seq)))


def tb_cross_fall() -> Dict[str, float]:
    """On TB: following cells in order of increasing P, the largest fall of H, and the converse (§3.3)."""
    v, u, r = bases("TB"); P = compose("P", v, u, r).ravel(); H = compose("H", v, u, r).ravel()
    def fall(a, b):
        seq = b[np.lexsort((b, a))]
        return float(max(0.0, np.max(np.maximum.accumulate(seq) - seq)))
    return {"H_along_P": fall(P, H), "P_along_H": fall(H, P)}
