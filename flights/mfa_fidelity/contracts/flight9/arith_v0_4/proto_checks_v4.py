#!/usr/bin/env python3
"""Definition checks for Contract F9 v0.4 on SYNTHETIC maps and terrain arrays only. Usage: proto_checks_v4.py <f9_probe.py> <out.json>"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f9_compare as T, f9_evaluator_proto_v4 as EV
P = T.load_probe(sys.argv[1]); L = 100; out = {}
def sizes(mask): return sorted(np.unique(EV.edge(mask)[1], return_counts=True)[1].tolist())
def Sj(obs, pred): return EV.S_joint(*EV.edge(obs), *EV.edge(pred))
# --- component convention (F1)
strips = np.zeros((L, L), bool)
for x0 in (0, 20, 40, 60, 80): strips[x0:x0 + 5, :] = True
isl = strips.copy(); isl[8:18, 20:30] = True
out["strips_plus_island_component_sizes"] = sizes(isl)
cb = np.zeros((L, L), bool); cb[10:20, 10:20] = True; cb[20:30, 20:30] = True; out["diagonal_blocks_component_sizes"] = sizes(cb)
hole = np.zeros((L, L), bool); hole[30:60, 30:60] = True; hole[40:50, 40:50] = False; out["block_with_hole_component_sizes"] = sizes(hole)
out["L2_r1_missing_island_S"] = Sj(strips, isl)
p2 = strips.copy(); p2[8:18, 20:40] = True; o2 = strips.copy(); o2[8:18, 20:35] = True; out["L2_r1_partial_patch_S"] = Sj(o2, p2)
xx, yy = np.indices((L, L)); a = np.where(yy % 2 == 0, 2, 40)
pred = (xx >= a) & (xx < 60); obs = (xx >= a) & (xx < 70)
out["L2_r2_zigzag_component_sizes_observed"] = sizes(obs); out["L2_r2_zigzag_S"] = Sj(obs, pred)
t = EV.S_terms(*EV.edge(obs), *EV.edge(pred)); out["L2_r2_zigzag_terms"] = t
# --- common masks on same-family terrains (F2)
terr = T.all_terrains(P); fam_sizes = {}
for name, (v, u, r) in terr.items():
    if name == "T0": continue
    wP = T.comparison_array(P, name, "P", v, u, r); wH = T.comparison_array(P, name, "H", v, u, r)
    fam_sizes[name] = dict(P=int(len(np.unique(wP)) - 1), H=int(len(np.unique(wH)) - 1), identical_arrays=bool(np.array_equal(wP, wH)))
    if name in T.SAME_FAMILY_LATENT:
        # the composition's own raw index is a non-decreasing function of the latent array (no inversion beyond float noise)
        for c in "PH":
            raw = P.compose(c, v, u, r).ravel(); o = np.argsort(wP.ravel(), kind="stable"); rs = raw[o]
            fam_sizes[name]["max_inversion_" + c] = float((np.maximum.accumulate(rs) - rs).max())
out["family_sizes"] = fam_sizes
def counts_for(mask):
    signed = np.where(mask, 1, -1); f = (1 + 2 * np.cos(2 * np.pi * np.arange(L) / L)) / 3
    A = 200 + np.rint(np.fft.ifft2(np.fft.fft2(signed) / (f[:, None] * f[None, :])).real).astype(np.int64)
    assert np.array_equal(sum(np.roll(np.roll(A, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1)), 9 * (200 + signed)); return A
v, u, r = terr["TC"]
old_P = np.round(P.compose("P", v, u, r), 12); obs_tc = np.roll(old_P >= 0.729, 2, axis=0); A = counts_for(obs_tc)
res = {}
for c in "PH":
    fam = EV.Family(T.comparison_array(P, "TC", c, v, u, r)); e = EV.evaluate(A / 1000, fam, 0.20, brute=True)
    res[c] = dict(family=int(len(fam.levels)), within=e["within"], S_min=e["best"][0], latent_level=e["best"][1], label=T.level_label("TC", c, e["best"][1]))
out["L2_r2_TC_translation_common_masks"] = res
# --- clipped-normal mean (F4)
def Phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
def phi(z): return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
def clip_mean(m, s):
    a = (0 - m) / s; b = (1 - m) / s; return m * (Phi(b) - Phi(a)) - s * (phi(b) - phi(a)) + (1 - Phi(b))
out["clip_mean_m0.03_s0.10"] = clip_mean(0.03, 0.10)
rng = np.random.default_rng(7); out["clip_mean_monte_carlo"] = float(np.clip(0.03 + 0.10 * rng.standard_normal(4_000_000), 0, 1).mean())
# --- provenance items (F7)
ordv = {}
for name, (v, u, r) in terr.items():
    p = P.compose("P", v, u, r).ravel(); h = P.compose("H", v, u, r).ravel(); o = np.argsort(p, kind="stable"); hs = h[o]
    ordv[name] = float((np.maximum.accumulate(hs) - hs).max())
out["max_fall_of_H_along_increasing_P"] = ordv
steps = {}
for k in T.TD:
    t_ = T.td(k)[0]; steps[k] = float(max(np.abs(t_ - np.roll(t_, 1, 0)).max(), np.abs(t_ - np.roll(t_, 1, 1)).max()))
out["td_largest_base_step"] = steps
json.dump(out, open(sys.argv[2], "w"), indent=1); print(json.dumps(out, indent=1))
