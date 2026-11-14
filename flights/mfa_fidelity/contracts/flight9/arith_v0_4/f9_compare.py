"""Contract F9 v0.4: terrains (unchanged from v0.3) and the canonical comparison arrays of s3.4.
Terrain arithmetic only."""
import importlib.util, hashlib
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
def tb():
    q = TB_PARAMS; s = q["s0"] + q["a"] * _c(x); d = q["d0"] + q["b"] * _c(y); return s + d, s - d, np.full((L, L), q["r0"])
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
    return hashlib.sha256(b"".join(np.ascontiguousarray(b_, dtype="<f8").tobytes() for b_ in (v, u, r))).hexdigest()
SAME_FAMILY_LATENT = {"TA": "v", "TC": "u", "TD-1-2": "v", "TD-1-4": "v", "TD-4-2": "v", "TD-4-4": "v"}
def comparison_array(P, name, comp, v, u, r):
    """The array whose level sets are the contour family for (terrain, composition), rounded to 12 places.
    Same-family terrains: ONE latent array for both compositions (TA, TD: the common base t = v; TC: u), so both use identical masks.
    TB: each composition's own index."""
    if name in SAME_FAMILY_LATENT:
        return np.round({"v": v, "u": u}[SAME_FAMILY_LATENT[name]], 12)
    return np.round(P.compose(comp, v, u, r), 12)
def level_label(name, comp, ell):
    """The composition's own index value on the contour at latent level ell (fidelity label only)."""
    if name in ("TA",) or name.startswith("TD"): return ell ** 3 if comp == "P" else ell
    if name == "TC": return 0.81 * ell if comp == "P" else (1.8 + ell) / 3.0
    return ell
