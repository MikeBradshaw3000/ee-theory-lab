#!/usr/bin/env python3
"""Contract F9 v0.6: support checks of the four unavailable-state recipes of s6.2 row 15, at ZERO noise. SYNTHETIC maps and
terrain arrays only; no lattice run; no probe output. They show the recipes give their typed states; under calibration-derived
noise the typed truth is certified on the clipped population map.
Usage: unavailable_states_v6.py <f9_probe.py> <dir of arith_v0_4> <out.json>"""
import sys, json, math, numpy as np
sys.path.insert(0, sys.argv[2])
import f9_compare as T, f9_evaluator_proto_v4 as EV
P = T.load_probe(sys.argv[1]); terr = T.all_terrains(P); L = 100; out = {}
def scale(w): return (w - w.min()) / (w.max() - w.min())
def state(pmap, theta=0.20):
    n = int(EV.region(pmap, theta).sum())
    return "empty" if n == 0 else "full" if n == L * L else "edge"
arrays = {}
for name in ("TA", "TB", "TC", "TD-1-2", "TD-1-4", "TD-4-2", "TD-4-4"):
    v, u, r = terr[name]
    if name == "TB":
        for c in "PH": arrays["TB." + c] = T.comparison_array(P, name, c, v, u, r)
    else: arrays[name] = T.comparison_array(P, name, "P", v, u, r)
# 1. constant map: capped ranges [0.03, 0.14] and [0.26, 0.40]; reported near-threshold range (0.14, 0.26)
grid = lambda a, b, n=45: [a + (b - a) * i / (n - 1) for i in range(n)]
out["constant_map"] = {
    "low_range_0.03_0.14": sorted({state(np.full((L, L), c)) for c in grid(0.03, 0.14)}),
    "high_range_0.26_0.40": sorted({state(np.full((L, L), c)) for c in grid(0.26, 0.40)}),
    "near_threshold_0.14_0.26": sorted({state(np.full((L, L), c)) for c in grid(0.141, 0.259)})}
# 2. saturated map: constant on [0.60, 1.00]
out["saturated_map_0.60_1.00"] = sorted({state(np.full((L, L), c)) for c in grid(0.60, 1.00)})
# 3. empty region: the low map 0.03 + 0.05 z on each canonical comparison array
out["empty_region_low_map"] = {k: dict(state=state(0.03 + 0.05 * scale(w)), max=float((0.03 + 0.05 * scale(w)).max())) for k, w in arrays.items()}
# 4. constant index: its family is empty; the map is a generic level map of a canonical array, informative on its own
const = np.round(np.full((L, L), 0.8), 12)
out["constant_index_family_size"] = int(len(EV.Family(const).levels))
ci = {}
for k, w in arrays.items():
    z = scale(w); fam = EV.Family(w); row = {}
    for c0 in (0.03, 0.10):
        for c1 in (0.2, 0.6):
            e = EV.evaluate(c0 + c1 * z, fam, 0.20)
            row["c0=%.2f,c1=%.1f" % (c0, c1)] = bool(e["informative"])
    ci[k] = row
out["generic_level_map_informative_at_coefficient_corners"] = ci
# 5. a constant stays constant under the clipped-normal mean (one value of sigma per value of the pre-noise map)
def clipped_mean(m, s):
    if s == 0: return m
    Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2))); phi = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
    a, b = -m / s, (1 - m) / s
    return m * (Phi(b) - Phi(a)) - s * (phi(b) - phi(a)) + 1 - Phi(b)
out["clipped_mean_examples"] = {"m=0.03,s=0.10": clipped_mean(0.03, 0.10), "m=0.14,s=0.10": clipped_mean(0.14, 0.10), "m=0.26,s=0.10": clipped_mean(0.26, 0.10), "m=1.00,s=0.10": clipped_mean(1.0, 0.10)}
json.dump(out, open(sys.argv[3], "w"), indent=1); print(json.dumps(out, indent=1))
