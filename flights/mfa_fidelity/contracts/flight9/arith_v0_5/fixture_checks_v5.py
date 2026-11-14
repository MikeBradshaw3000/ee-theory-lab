#!/usr/bin/env python3
"""Contract F9 v0.5: checks of the declared qualification fixtures and of the registered-family scope. SYNTHETIC maps and terrain
arrays only; no lattice run; no probe output. Usage: fixture_checks_v5.py <f9_probe.py> <dir of arith_v0_4> <out.json>"""
import sys, json, math, numpy as np
sys.path.insert(0, sys.argv[2])
import f9_compare as T, f9_evaluator_proto_v4 as EV
P = T.load_probe(sys.argv[1]); L = 100; out = {}
def Phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
# ---- strip fixture (s6.2): five full-height strips; an island 9 cells wide in x and b cells tall in a gap
def strips():
    m = np.zeros((L, L), bool)
    for x0 in (0, 20, 40, 60, 80): m[x0:x0 + 5, :] = True
    return m
def island(b, gap=0, y0=20):
    m = np.zeros((L, L), bool); x0 = 20 * gap + 8
    for dy in range(b): m[x0:x0 + 9, (y0 + dy) % L] = True
    return m
fx = {}
for b, bonds in ((10, 38), (11, 40), (12, 42)):
    isl = island(b); contour_mask = strips() | isl
    fam = EV.Family(contour_mask.astype(float))                       # binary synthetic index: one registered contour
    C, Cc = EV.edge(contour_mask)
    sizes = sorted(np.unique(Cc, return_counts=True)[1].tolist())
    row = {"island_bonds": int((np.unique(EV.edge(isl)[1], return_counts=True)[1]).sum()), "contour_bonds": int(len(C)), "share": float(bonds / len(C)), "component_sizes": sizes}
    # distance from island bonds to the nearest strip bond
    Ei, _ = EV.edge(isl); Es, _ = EV.edge(strips())
    from scipy.spatial import cKDTree
    row["island_to_strips_min_distance"] = float(cKDTree(Es, boxsize=L).query(Ei)[0].min())
    for label, occ in (("absent", strips()), ("present", contour_mask)):
        pmap = np.where(occ, 0.30, 0.10)
        e = EV.evaluate(pmap, fam, 0.20, brute=True)
        reg = EV.region(pmap, 0.20); E, Ec = EV.edge(reg); t = EV.S_terms(E, Ec, C, Cc)
        row[label] = dict(informative=e["informative"], S=e["best"][0], within=e["within"], region_cells=int(reg.sum()),
                          global_E=t["global_E"], global_C=t["global_C"], comp_C=[x for x in t["comp_C"] if x[0] < 100], comp_E=[x for x in t["comp_E"] if x[0] < 100])
    fx[str(bonds)] = row
out["strip_fixture"] = fx
# ---- intermediate bands: diagonal translations (L2 round 3 s5.1), TD-4-2 only here
terr = T.all_terrains(P); v, u, r = terr["TD-4-2"]; w = T.comparison_array(P, "TD-4-2", "P", v, u, r)
h = 0.06 + 0.40 * (w - w.min()) / (w.max() - w.min()); fam = EV.Family(w); d = {}
for dx, dy in ((1, 1), (2, 1), (2, 2), (3, 0)):
    d["%d,%d" % (dx, dy)] = EV.evaluate(np.roll(np.roll(h, dx, 0), dy, 1), fam, 0.20, brute=True)["best"][0]
out["TD-4-2_translation_true_delta"] = d
# ---- low-information construction: the flat-low map has no edge at theta
flat = 0.03 + 0.05 * (w - w.min()) / (w.max() - w.min()); out["flat_low_map_max"] = float(flat.max()); out["flat_low_informative"] = EV.evaluate(flat, fam, 0.20)["informative"]
# ---- registered-family scope (R3-1): L2's TD-1-2 raw-cut case
v, u, r = terr["TD-1-2"]; raw = P.compose("H", v, u, r); om = T.comparison_array(P, "TD-1-2", "H", v, u, r)
vals = np.unique(raw); mask = raw >= vals[1]; E, Ec = EV.edge(mask); famr = EV.Family(om)
best = min((EV.S_joint(E, Ec, *famr.contour(l)), float(l)) for l in famr.levels)
out["TD-1-2_raw_cut"] = dict(raw_cut=float(vals[1]), raw_min=float(vals[0]), index_difference=float(vals[1] - vals[0]), raw_family=int(len(vals) - 1), registered_family=int(len(famr.levels)),
                             region=int(mask.sum()), bonds=int(len(E)), registered_min_S=best[0], registered_min_level=best[1])
# how many raw contours the rounding removes, per same-family terrain
rem = {}
for name in T.SAME_FAMILY_LATENT:
    v, u, r = terr[name]; lat = {"v": v, "u": u}[T.SAME_FAMILY_LATENT[name]]
    rem[name] = dict(latent_unrounded=int(len(np.unique(lat)) - 1), registered=int(len(np.unique(np.round(lat, 12))) - 1))
v, u, r = terr["TB"]
for c in "PH":
    rawi = P.compose(c, v, u, r); rem["TB." + c] = dict(index_unrounded=int(len(np.unique(rawi)) - 1), registered=int(len(np.unique(np.round(rawi, 12))) - 1))
out["raw_vs_registered_family_sizes"] = rem
json.dump(out, open(sys.argv[3], "w"), indent=1); print(json.dumps(out, indent=1))
