import sys, time, json, numpy as np
sys.path.insert(0, "/home/claude/work/v3")
import f9_terrains as T, f9_evaluator_proto as EV
P = T.load_probe(sys.argv[1]); L = 100; rng = np.random.default_rng(12345)
out = {}
# --- definition checks against L2's synthetic examples
strips = np.zeros((L, L), bool)
for x0 in (0, 20, 40, 60, 80): strips[x0:x0 + 5, :] = True
def Sj(a, b): Ea, Eac = EV.edge(a); Cb, Cbc = EV.edge(b); return EV.S_joint(Ea, Eac, Cb, Cbc)
pred = strips.copy(); pred[8:18, 20:30] = True
out["L2_missing_island_S"] = Sj(strips, pred)
pred2 = strips.copy(); pred2[8:18, 20:40] = True; obs2 = strips.copy(); obs2[8:18, 20:35] = True
out["L2_partial_patch_S"] = Sj(obs2, pred2)
E, Ec = EV.edge(pred); ids, cnt = np.unique(Ec, return_counts=True); out["components_strips_plus_island"] = sorted(cnt.tolist())
# checkerboard junction: two diagonally touching 10x10 blocks are separate components
cb = np.zeros((L, L), bool); cb[10:20, 10:20] = True; cb[20:30, 20:30] = True
out["diagonal_blocks_components"] = sorted(np.unique(EV.edge(cb)[1], return_counts=True)[1].tolist())
hole = np.zeros((L, L), bool); hole[30:60, 30:60] = True; hole[40:50, 40:50] = False
out["block_with_hole_components"] = sorted(np.unique(EV.edge(hole)[1], return_counts=True)[1].tolist())
# --- cost and exactness on synthetic maps: p = h(lambda) + noise, 20 or 40 seed maps, bootstrap draws
terr = T.all_terrains(P)
def synth(lam, n_seeds, sd):
    z = (lam - lam.min()) / (lam.max() - lam.min()); base = 0.06 + 0.40 * z
    return np.stack([base + sd * rng.standard_normal((L, L)) for _ in range(n_seeds)])
timing = {}
for name, own, rival in (("TB", "P", "H"), ("TB", "H", "P"), ("TA", "P", "H"), ("TD-4-2", "P", "H"), ("TC", "P", "H")):
    v, u, r = terr[name]; lam_o = T.quantize(P.compose(own, v, u, r)); lam_r = T.quantize(P.compose(rival, v, u, r))
    fo = EV.Family(lam_o); fr = EV.Family(lam_r)
    maps = synth(lam_o, 40, 0.04)
    t0 = time.time(); res_o = []; res_r = []; nadm = []
    for b in range(60):
        pm = maps[rng.integers(0, 40, 40)].mean(0)
        a = EV.evaluate(pm, fo, 0.20); c = EV.evaluate(pm, fr, 0.20)
        if a["informative"]: res_o.append(a["within"]); res_r.append(c["within"]); nadm.append((a["n_adm"], c["n_adm"]))
    dt = (time.time() - t0) / 60
    # exactness of pruning on the point map: brute force over the complete own family
    pm = maps.mean(0); a = EV.evaluate(pm, fo, 0.20); E, Ec = EV.edge(EV.box(pm) >= 0.20)
    t1 = time.time(); brute = min(EV.S_joint(E, Ec, *fo.contour(l)) for l in fo.levels); tb = time.time() - t1
    timing[name + "." + own] = dict(family_own=len(fo.levels), family_rival=len(fr.levels), sec_per_draw_both_indices=round(dt, 4),
        own_within=int(sum(res_o)), rival_within=int(sum(res_r)), draws=len(res_o), mean_adm_own=float(np.mean([n[0] for n in nadm])), mean_adm_rival=float(np.mean([n[1] for n in nadm])),
        point_S_pruned=None if a["best"] is None else round(a["best"][0], 4), point_S_brute=round(brute, 4), brute_sec=round(tb, 2),
        pruned_equals_brute_decision=bool((a["best"] is not None and a["best"][0] <= EV.EPS) == (brute <= EV.EPS)))
out["timing"] = timing
json.dump(out, open(sys.argv[2], "w"), indent=1); print(json.dumps(out, indent=1))
