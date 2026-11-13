#!/usr/bin/env python3
"""F9 contract step 1 -- terrain arithmetic ONLY. No run of the rule, no probe output read.
Uses terrain arrays and the Moore adjacency (spectral radius) and nothing else."""
import importlib.util, json, math, sys, hashlib
import numpy as np
spec = importlib.util.spec_from_file_location("f9_probe", sys.argv[1]); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
L = 100
Q = P.Q_DE
def grid(L):
    x = (np.arange(L, dtype=np.float64) / L)[:, None] * np.ones((1, L))
    y = np.ones((L, 1)) * (np.arange(L, dtype=np.float64) / L)[None, :]
    return x, y
def shares(lam):
    tot = lam.var()
    if tot == 0: return None
    sx = lam.mean(axis=1).var() / tot; sy = lam.mean(axis=0).var() / tot
    return sx, sy, 1.0 - sx - sy
def arm(v, u, r):
    out = {}
    for c in ("P", "H"):
        lam = P.compose(c, v, u, r); spr = P.spectral_radius(lam); sh = shares(lam)
        out[c] = dict(lmin=float(lam.min()), lmax=float(lam.max()), lmean=float(lam.mean()), ratio=float(lam.max()/lam.min()),
                      cv=float(lam.std()/lam.mean()), sx=sh[0], sy=sh[1], sxy=sh[2], spr=spr, gspec=Q/spr, sha=P.sha(lam)[:16])
    return out
res = {"L": L, "q": Q}
# ---- 0. reproduce the record's TB figure from the committed formula
rep = {}
for LL in (50, 100):
    v, u, r = P.terrain("TB", LL)
    rep[LL] = {c: shares(P.compose(c, v, u, r)) for c in ("P", "H")}
res["TB_as_probed"] = rep
v, u, r = P.terrain("TB", L); res["TB_as_probed_arm"] = arm(v, u, r)
# ---- 1. TB family: v = s + d, u = s - d, r = r0; s = s0 + a cos(2 pi x); d = d0 + b cos(2 pi y)
def tb(s0, a, d0, b, r0=0.8, LL=L):
    x, y = grid(LL); s = s0 + a * P._c(x); d = d0 + b * P._c(y)
    return s + d, s - d, np.full((LL, LL), r0)
def closed_share(s0, a, d0, b):
    vx = 2*s0*s0*a*a + a**4/8; vy = 2*d0*d0*b*b + b**4/8
    return vx/(vx+vy)
cands = {"TB-1 symmetric": (0.55, 0.07, 0.0, 0.38), "TB-2 offset": (0.55, 0.07, 0.19, 0.19),
         "TB-3 symmetric 70/30": (0.55, 0.09, 0.0, 0.36), "TB-4 offset 70/30": (0.55, 0.09, 0.18, 0.18)}
res["TB_candidates"] = {}
for k, (s0, a, d0, b) in cands.items():
    v, u, r = tb(s0, a, d0, b)
    e = arm(v, u, r); e["params"] = dict(s0=s0, a=a, d0=d0, b=b, r0=0.8)
    e["base_min"] = float(min(v.min(), u.min())); e["base_max"] = float(max(v.max(), u.max()))
    e["closed_form_sx"] = closed_share(s0, a, d0, b)
    v5, u5, r5 = tb(s0, a, d0, b, LL=50); e["sx_L50"] = shares(P.compose("P", v5, u5, r5))[0]
    res["TB_candidates"][k] = e
# scan: what the constraint set allows (bases in [floor, 1], share target), closed form checked above against arrays
scan = []
for floor in (0.02, 0.05, 0.10, 0.15, 0.20):
    for target in (0.5, 0.6, 0.7):
        best = None
        for s0 in np.arange(0.40, 0.701, 0.01):
            for D in np.arange(0.05, 0.50, 0.005):
                # symmetric form d0 = 0, b = D: Var_y = D^4/8 ; solve a for target share
                vy = D**4/8; vx = vy*target/(1-target)
                # 2 s0^2 a^2 + a^4/8 = vx
                a2 = (-2*s0*s0 + math.sqrt(4*s0**4 + vx/2))*4
                a = math.sqrt(a2)
                if s0 + a + D <= 1.0 + 1e-12 and s0 - a - D >= floor - 1e-12:
                    if best is None or a > best[0]: best = (a, s0, D)
        if best: scan.append(dict(floor=floor, target_sx=target, a_max=best[0], s0=best[1], D=best[2], height_ratio=(2*(best[1]+best[0])+0.8)/(2*(best[1]-best[0])+0.8)))
res["TB_scan_max_x_amplitude"] = scan
# ---- 2. TD: core = closed-form set C (n equal discs, total area fraction phi), profile S = (1 + tanh(delta/w))/2
def td_delta(n_side, phi, LL=L):
    x, y = grid(LL); n = n_side*n_side; R = math.sqrt(phi/(n*math.pi))
    best = np.full((LL, LL), -np.inf)
    for i in range(n_side):
        for j in range(n_side):
            cx = (i + 0.5)/n_side; cy = (j + 0.5)/n_side
            dx = np.abs(x - cx); dx = np.minimum(dx, 1 - dx); dy = np.abs(y - cy); dy = np.minimum(dy, 1 - dy)
            best = np.maximum(best, R - np.sqrt(dx*dx + dy*dy))
    return best, R
def lattice_perimeter(core):
    return int((core != np.roll(core, 1, 0)).sum() + (core != np.roll(core, 1, 1)).sum())
T_LO, T_HI, PHI = 0.3, 0.9, 0.20
res["TD"] = {"phi": PHI, "t_lo": T_LO, "t_hi": T_HI, "variants": []}
for n_side in (1, 2, 4):
    delta, R = td_delta(n_side, PHI)
    core = delta >= 0
    for w_cells in (1.0, 2.0, 4.0):
        w = w_cells / L
        S = 0.5*(1 + np.tanh(delta / w)); t = T_LO + (T_HI - T_LO)*S
        band = (S > 0.1) & (S < 0.9)
        a_ = arm(t, t, t)
        n = n_side*n_side
        res["TD"]["variants"].append(dict(n_discs=n, R_cells=R*L, gap_cells=(1.0/n_side - 2*R)*L, w_cells=w_cells,
            core_cells=int(core.sum()), perim_continuum_cells=2*math.pi*R*n*L, perim_lattice_edges=lattice_perimeter(core),
            band_cells=int(band.sum()), band_over_core=float(band.sum()/core.sum()), band_inside=int((band & core).sum()),
            S_min=float(S.min()), S_max=float(S.max()),
            half_height_is_core=bool(np.array_equal(S >= 0.5, core)),
            P=dict(lmin=a_["P"]["lmin"], lmax=a_["P"]["lmax"], spr=a_["P"]["spr"], gspec=a_["P"]["gspec"]),
            H=dict(lmin=a_["H"]["lmin"], lmax=a_["H"]["lmax"], spr=a_["H"]["spr"], gspec=a_["H"]["gspec"])))
# composition-independence check: core equals the set where each index exceeds its own value at S = 1/2
delta, R = td_delta(2, PHI); S = 0.5*(1 + np.tanh(delta/(2.0/L))); t = T_LO + (T_HI-T_LO)*S; tm = (T_LO+T_HI)/2
res["TD"]["core_equals_P_superlevel"] = bool(np.array_equal(P.compose("P", t, t, t) >= tm**3, delta >= 0))
res["TD"]["core_equals_H_superlevel"] = bool(np.array_equal(P.compose("H", t, t, t) >= tm, delta >= 0))
json.dump(res, open(sys.argv[2], "w"), indent=1)
print("written")
