"""Flight 9 contract terrains at L = 100 (Contract F9 v0.3 s3). Closed-form; terrain arithmetic only."""
import importlib.util, math, hashlib
import numpy as np
L = 100
def load_probe(path):
    spec = importlib.util.spec_from_file_location("f9_probe", path); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P); return P
_ii = np.arange(L, dtype=np.float64)
x = (_ii / L)[:, None] * np.ones((1, L)); y = np.ones((L, 1)) * (_ii / L)[None, :]
X = _ii[:, None] * np.ones((1, L)); Y = np.ones((L, 1)) * _ii[None, :]
TB_PARAMS = dict(s0=0.55, a=0.07, d0=0.19, b=0.19, r0=0.3)
C1 = [(49.5, 49.5)]; C4 = [(24.5, 24.5), (24.5, 74.5), (74.5, 24.5), (74.5, 74.5)]
TD = {"TD-1-2": (C1, 25.3, 2.0), "TD-1-4": (C1, 25.3, 4.0), "TD-4-2": (C4, 12.65, 2.0), "TD-4-4": (C4, 12.65, 4.0)}
def _c(z): return np.cos(2.0 * np.pi * z)
def tb(r0=None):
    q = TB_PARAMS; s = q["s0"] + q["a"] * _c(x); d = q["d0"] + q["b"] * _c(y)
    return s + d, s - d, np.full((L, L), q["r0"] if r0 is None else r0)
def td_delta(centres, R):
    best = np.full((L, L), -np.inf)
    for cx, cy in centres:
        dx = np.abs(X - cx); dx = np.minimum(dx, L - dx); dy = np.abs(Y - cy); dy = np.minimum(dy, L - dy)
        best = np.maximum(best, R - np.sqrt(dx * dx + dy * dy))
    return best
def td(name):
    cs, R, w = TD[name]; t = 0.3 + 0.6 * 0.5 * (1 + np.tanh(td_delta(cs, R) / w)); return t, t.copy(), t.copy()
def all_terrains(P):
    T = {"T0": P.terrain("T0", L), "TA": P.terrain("TA", L), "TB": tb(), "TC": P.terrain("TC", L)}
    for k in TD: T[k] = td(k)
    return T
def bases_sha(v, u, r):
    """SHA-256 of v, u, r concatenated: each C-contiguous, shape (100, 100), axis 0 = x index, little-endian float64."""
    return hashlib.sha256(b"".join(np.ascontiguousarray(b_, dtype="<f8").tobytes() for b_ in (v, u, r))).hexdigest()
def quantize(lam):
    """Index values rounded to 12 decimal places before any ranking or thresholding (tie rule, s5.5 step 5)."""
    return np.round(lam, 12)
