#!/usr/bin/env python3
"""Contract F9 v0.1 -- Appendix A precursor. Terrain arrays, Moore adjacency and closed-form rule constants ONLY.
No run of the rule; no probe output is read."""
import importlib.util, sys, math, json, hashlib
import numpy as np
from scipy.spatial import cKDTree
spec = importlib.util.spec_from_file_location("f9_probe", sys.argv[1]); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
L = 100; N = L*L; Q = P.Q_DE; ETA0 = P.ETA0
out = {"L": L, "q": Q, "eta0": ETA0}
ii = np.arange(L, dtype=np.float64)
x = (ii/L)[:, None]*np.ones((1, L)); y = np.ones((L, 1))*(ii/L)[None, :]
X = ii[:, None]*np.ones((1, L)); Y = np.ones((L, 1))*ii[None, :]
def tb2():
    s = 0.55 + 0.07*P._c(x); d = 0.19 + 0.19*P._c(y); return s + d, s - d, np.full((L, L), 0.8)
def td(centres, R, w):
    best = np.full((L, L), -np.inf)
    for cx, cy in centres:
        dx = np.abs(X-cx); dx = np.minimum(dx, L-dx); dy = np.abs(Y-cy); dy = np.minimum(dy, L-dy)
        best = np.maximum(best, R - np.sqrt(dx*dx+dy*dy))
    t = 0.3 + 0.6*0.5*(1+np.tanh(best/w)); return t, t.copy(), t.copy()
C1 = [(49.5, 49.5)]; C4 = [(24.5, 24.5), (24.5, 74.5), (74.5, 24.5), (74.5, 74.5)]
TERR = {"T0": P.terrain("T0", L), "TA": P.terrain("TA", L), "TB": tb2(), "TC": P.terrain("TC", L),
        "TD-1-2": td(C1, 25.3, 2.0), "TD-1-4": td(C1, 25.3, 4.0), "TD-4-2": td(C4, 12.65, 2.0), "TD-4-4": td(C4, 12.65, 4.0)}
def monotone_related(a, b):
    """True iff the two arrays induce the same weak ordering of cells (identical contour families and ordering)."""
    o = np.lexsort((b.ravel(), a.ravel())); a_s = a.ravel()[o]; b_s = b.ravel()[o]
    # within a-ties b must be constant (to tolerance); across increasing a, b non-decreasing
    tol = 1e-12
    return bool(np.all(np.diff(b_s) >= -tol))
tab = {}
for k, (v, u, r) in TERR.items():
    e = {"bases_sha256": hashlib.sha256(b"".join(np.ascontiguousarray(b_).tobytes() for b_ in (v, u, r))).hexdigest(),
         "base_min": float(min(v.min(), u.min(), r.min())), "base_max": float(max(v.max(), u.max(), r.max()))}
    lam = {}
    for c in "PH":
        lam[c] = P.compose(c, v, u, r); spr = P.spectral_radius(lam[c])
        e[c] = dict(lmin=float(lam[c].min()), lmax=float(lam[c].max()), lmean=float(lam[c].mean()), spr=spr, gspec=Q/spr, lam_sha256=P.sha(lam[c]))
    e["same_contour_family"] = monotone_related(lam["P"], lam["H"]) and monotone_related(lam["H"], lam["P"])
    tab[k] = e
out["terrains"] = tab
# ---- contour geometry: bond sets and the symmetric q95 distance (cells)
def bonds(high):
    a = high != np.roll(high, -1, 0); b = high != np.roll(high, -1, 1)
    i1, j1 = np.nonzero(a); i2, j2 = np.nonzero(b)
    return np.concatenate([np.stack([(i1+0.5) % L, j1.astype(float)], 1), np.stack([i2.astype(float), (j2+0.5) % L], 1)])
def D(E, C):
    if len(E) == 0 or len(C) == 0: return float("inf")
    d1 = cKDTree(C, boxsize=L).query(E)[0]; d2 = cKDTree(E, boxsize=L).query(C)[0]
    return float(max(np.quantile(d1, 0.95), np.quantile(d2, 0.95)))
def levels(lam, n=99):
    return np.quantile(lam.ravel(), np.arange(1, n+1)/(n+1))
def sep_table(lamA, lamB):
    LB = [bonds(lamB >= t) for t in levels(lamB)]
    res = []
    for pct, t in zip(range(1, 100), levels(lamA)):
        if pct % 10: continue
        CA = bonds(lamA >= t)
        res.append((pct, len(CA), min(D(CA, cb) for cb in LB)))
    return res
v, u, r = TERR["TB"]; lp = P.compose("P", v, u, r); lh = P.compose("H", v, u, r)
out["TB_sep_P_contour_to_nearest_H_contour"] = sep_table(lp, lh)
out["TB_sep_H_contour_to_nearest_P_contour"] = sep_table(lh, lp)
for k in ("TA", "TC", "TD-4-2"):
    v, u, r = TERR[k]; out[k+"_sep_P_to_H_max"] = max(s[2] for s in sep_table(P.compose("P", v, u, r), P.compose("H", v, u, r)))
# ---- levels
kap = [750000] + list(range(1000000, 2000001, 100000)) + [2250000, 2500000, 3000000]
out["kappa_micro"] = kap; out["n_levels"] = len(kap)
# ---- rule constants
a = 1 - math.exp(-ETA0); pi1 = a/(a+Q)
out["null"] = dict(a=a, pi1=pi1, mean_active_spell=1/Q, anyW={W: 1-(1-pi1)*(1-a)**(W-1) for W in (1, 10, 100)})
# ---- T0 finite-size terms at N = 10,000 (Contract F8 s3.4 procedure), mean-field map
def rho_sk(m):
    g_lam = m*Q; rho = 0.5
    for _ in range(200000):
        new = (1-rho)*(1-math.exp(-g_lam*rho)) + rho*(1-Q)
        if abs(new-rho) < 1e-15: break
        rho = new
    return rho
lo, hi = 1.0001, 1.5
for _ in range(60):
    mid = (lo+hi)/2
    if N*rho_sk(mid) >= 50: hi = mid
    else: lo = mid
out["T0_dm"] = dict(lower=math.log(N)/(Q*2000), upper=hi-1, spacing=0.1, dm=max(math.log(N)/(Q*2000), hi-1)+0.1)
# ---- per-cell sampling SE of the seed-mean W=1 occupancy, INDEPENDENT-CHAIN APPROXIMATION ONLY (20 seeds x 1000 ticks)
se = {}
for p in (0.0523, 0.1, 0.2, 0.3, 0.5):
    ae = p*Q/(1-p); rho = 1-ae-Q; se[p] = math.sqrt(p*(1-p)*(1+rho)/(1-rho)/(20*1000))
out["cell_se_indep_chain"] = se
# ---- run counts
arms = [("T0", "P")] + [(t, c) for t in ("TA", "TB", "TC", "TD-1-2", "TD-1-4", "TD-4-2", "TD-4-4") for c in "PH"]
n_arms = len(arms); nl = len(kap)
out["runs"] = dict(arms=n_arms, census=n_arms*2*nl*20, t0_low=nl*20, calibration=n_arms*2*nl*20, stability=n_arms*2*nl*20)
json.dump(out, open(sys.argv[2], "w"), indent=1); print(json.dumps(out, indent=1))
