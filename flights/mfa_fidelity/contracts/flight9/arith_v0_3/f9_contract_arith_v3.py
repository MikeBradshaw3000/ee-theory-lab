#!/usr/bin/env python3
"""Contract F9 v0.3 -- Appendix A precursor. Terrain arrays, Moore adjacency, closed-form constants and the site closure ONLY.
No run of the rule; no probe output is read. Usage: f9_contract_arith_v3.py <path to f9_probe.py> <output json>"""
import sys, math, json, os
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import beta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f9_terrains as T
P = T.load_probe(sys.argv[1]); L = T.L; N = L * L; Q = P.Q_DE; ETA0 = P.ETA0
out = {"L": L, "q": Q, "eta0": ETA0, "tb_params": T.TB_PARAMS}
TERR = T.all_terrains(P)
def same_family(a, b):
    """True iff a and b induce the same weak ordering of cells: equal ties, and b non-decreasing in a."""
    o = np.argsort(a.ravel(), kind="stable"); a_s = a.ravel()[o]; b_s = b.ravel()[o]
    grp = np.concatenate([[0], np.cumsum(np.diff(a_s) != 0)])
    bmin = np.full(grp[-1] + 1, np.inf); bmax = np.full(grp[-1] + 1, -np.inf)
    np.minimum.at(bmin, grp, b_s); np.maximum.at(bmax, grp, b_s)
    return bool(np.all(bmin == bmax) and np.all(np.diff(bmin) > 0))
assert same_family(np.array([0., 0.]), np.array([0., 1.])) is False            # the v0.2 helper passed this pair
def shares(lam):
    tot = lam.var(); return (float(lam.mean(axis=1).var() / tot), float(lam.mean(axis=0).var() / tot)) if tot > 0 else None
tab = {}
for k, (v, u, r) in TERR.items():
    e = {"bases_sha256": T.bases_sha(v, u, r), "base_min": float(min(v.min(), u.min(), r.min())), "base_max": float(max(v.max(), u.max(), r.max()))}
    lam = {}
    for c in "PH":
        raw = P.compose(c, v, u, r); lam[c] = T.quantize(raw); spr = P.spectral_radius(raw)
        e[c] = dict(lmin=float(raw.min()), lmax=float(raw.max()), ratio=float(raw.max() / raw.min()), spr=spr, gspec=Q / spr,
                    complete_family=int(len(np.unique(lam[c])) - 1), shares=shares(raw))
    e["same_contour_family_quantized"] = same_family(lam["P"], lam["H"]) and same_family(lam["H"], lam["P"])
    tab[k] = e
out["terrains"] = tab
# TB contour separation, global symmetric q95, deciles
def bonds(high):
    a = high != np.roll(high, -1, 0); b = high != np.roll(high, -1, 1); i1, j1 = np.nonzero(a); i2, j2 = np.nonzero(b)
    return np.concatenate([np.stack([(i1 + 0.5) % L, j1.astype(float)], 1), np.stack([i2.astype(float), (j2 + 0.5) % L], 1)])
def D(E, C):
    return float(max(np.quantile(cKDTree(C, boxsize=L).query(E)[0], 0.95), np.quantile(cKDTree(E, boxsize=L).query(C)[0], 0.95)))
def sep(lamA, lamB):
    LB = [bonds(lamB >= t) for t in np.unique(lamB)[1:]]
    return [(p, min(D(bonds(lamA >= t), cb) for cb in LB)) for p, t in ((p, np.quantile(lamA.ravel(), p / 100)) for p in range(10, 100, 10))]
v, u, r = TERR["TB"]; lp = T.quantize(P.compose("P", v, u, r)); lh = T.quantize(P.compose("H", v, u, r))
out["TB_sep_H_contour_to_nearest_P_contour_complete_family"] = sep(lh, lp)
out["TB_sep_P_contour_to_nearest_H_contour_complete_family"] = sep(lp, lh)
# levels
kap = [750000] + list(range(1000000, 2000001, 50000)) + [2250000, 2500000, 3000000]
out["kappa_micro"] = kap; out["n_levels"] = len(kap)
a = 1 - math.exp(-ETA0); pi1 = a / (a + Q)
out["null"] = dict(a=a, pi1=pi1, mean_active_spell=1 / Q, anyW={W: 1 - (1 - pi1) * (1 - a) ** (W - 1) for W in (1, 10, 100)})
def rho_sk(m):
    rho = 0.5
    for _ in range(200000):
        new = (1 - rho) * (1 - math.exp(-m * Q * rho)) + rho * (1 - Q)
        if abs(new - rho) < 1e-15: break
        rho = new
    return rho
lo, hi = 1.0001, 1.5
for _ in range(60):
    mid = (lo + hi) / 2
    if N * rho_sk(mid) >= 50: hi = mid
    else: lo = mid
low = math.log(N) / (Q * 2000)
out["T0_bracket"] = dict(lower=low, upper=hi - 1, spacing=0.05, value=max(low, hi - 1) + 0.05)
SEEDS = 40
out["cell_se_indep_chain_40seeds"] = {p: math.sqrt(p * (1 - p) * (1 + (1 - p * Q / (1 - p) - Q)) / (1 - (1 - p * Q / (1 - p) - Q)) / (SEEDS * 1000)) for p in (0.0523, 0.1, 0.2, 0.3, 0.5)}
arms = 15; nl = len(kap)
out["runs"] = dict(seeds=SEEDS, levels=nl, calibration=arms * 2 * nl * SEEDS, t0_census=3 * nl * SEEDS, skeleton_census=14 * nl * SEEDS,
                   realization_census=14 * nl * SEEDS, census_stability=2 * 14 * nl * SEEDS)
out["runs"]["total_dynamics"] = sum(out["runs"][k] for k in ("calibration", "t0_census", "skeleton_census", "realization_census", "census_stability"))
out["runs"]["container_hours_at_probe_speed"] = out["runs"]["total_dynamics"] * (0.96 + 0.62) / 2 / 3600
def cp(k, n, conf=0.95):
    al = (1 - conf) / 2; return (0.0 if k == 0 else float(beta.ppf(al, k, n - k + 1)), 1.0 if k == n else float(beta.ppf(1 - al, k + 1, n - k)))
out["cp_two_sided_95"] = {"%d/%d" % (k, SEEDS): cp(k, SEEDS) for k in (0, 20, 36, 40)}
k = 0
while beta.ppf(0.95, k + 1, 200 - k) <= 0.10: k += 1
out["qualification_max_errors_of_200"] = k - 1
out["survival_threshold_of_40"] = 36
# closure-estimated informative levels on the contract grid
PI1 = pi1
def closure(lam, g, p):
    for it in range(200000):
        new = (1 - p) * (1 - np.exp(-(ETA0 + g * lam * P.moore_sum(p) / 8.0))) + (1 - Q) * p
        if np.abs(new - p).max() < 1e-12: return new
        p = new
def box(a_): return sum(np.roll(np.roll(a_, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1)) / 9
def nbonds(h): return int((h != np.roll(h, -1, 0)).sum() + (h != np.roll(h, -1, 1)).sum())
win = {}
for name, (v, u, r) in TERR.items():
    if name == "T0": continue
    for c in "PH":
        lam = P.compose(c, v, u, r); gs = Q / P.spectral_radius(lam); p = np.full((L, L), PI1); row = {}
        for th in (0.10, 0.20, 0.30): row[th] = 0
        for km in kap:
            p = closure(lam, km / 1e6 * gs, p); pt = box(p)
            for th in row:
                h = pt >= th; n = int(h.sum()); row[th] += int(n >= 100 and N - n >= 100 and nbonds(h) >= 40)
        win[name + "." + c] = {str(k_): v_ for k_, v_ in row.items()}
out["closure_informative_levels_of_25"] = win
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(json.dumps({k_: out[k_] for k_ in out if k_ != "terrains"}, indent=1))
for k_, e in tab.items(): print(k_, e["bases_sha256"][:16], round(e["base_min"], 4), round(e["base_max"], 4), e["same_contour_family_quantized"],
    {c: (round(e[c]["lmin"], 4), round(e[c]["lmax"], 4), round(e[c]["ratio"], 4), round(e[c]["spr"], 6), round(e[c]["gspec"], 6), e[c]["complete_family"], None if e[c]["shares"] is None else tuple(round(s, 4) for s in e[c]["shares"])) for c in "PH"})
