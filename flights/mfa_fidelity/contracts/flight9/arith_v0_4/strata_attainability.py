#!/usr/bin/env python3
"""Which certified true discrepancies are attainable by translating a compatible map, and the prototype's cost per draw.
SYNTHETIC maps only. Usage: strata_attainability.py <f9_probe.py> <out.json>"""
import sys, os, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f9_compare as T, f9_evaluator_proto_v4 as EV
P = T.load_probe(sys.argv[1]); L = 100; terr = T.all_terrains(P); out = {"translation_true_delta": {}, "timing": {}}
def h(om): z = (om - om.min()) / (om.max() - om.min()); return 0.06 + 0.40 * z
for name, comp in (("TD-4-2", "P"), ("TB", "H"), ("TD-1-2", "H"), ("TC", "P")):
    v, u, r = terr[name]; om = T.comparison_array(P, name, comp, v, u, r); fam = EV.Family(om); row = {}
    for axis in (0, 1):
        for k in range(0, 6):
            e = EV.evaluate(np.roll(h(om), k, axis=axis), fam, 0.20, brute=True)
            row["axis%d_k%d" % (axis, k)] = None if not e["informative"] else round(e["best"][0], 6)
    out["translation_true_delta"][name + "." + comp] = row; print(name, comp, row, flush=True)
rng = np.random.default_rng(12345)
for name, comp, rival in (("TB", "P", "H"), ("TA", "P", "H"), ("TD-4-2", "P", "H")):
    v, u, r = terr[name]; fo = EV.Family(T.comparison_array(P, name, comp, v, u, r)); fr = EV.Family(T.comparison_array(P, name, rival, v, u, r))
    maps = np.stack([h(fo.lam) + 0.04 * rng.standard_normal((L, L)) for _ in range(40)])
    for _ in range(3): EV.evaluate(maps[rng.integers(0, 40, 40)].mean(0), fo, 0.20)
    t0 = time.time(); n = 40; w = 0
    for b in range(n):
        pm = maps[rng.integers(0, 40, 40)].mean(0); a_ = EV.evaluate(pm, fo, 0.20); EV.evaluate(pm, fr, 0.20); w += int(a_.get("within", False))
    out["timing"][name + "." + comp] = dict(sec_per_draw_both_indices=round((time.time() - t0) / n, 4), own_within=w, draws=n); print(name, out["timing"][name + "." + comp], flush=True)
json.dump(out, open(sys.argv[2], "w"), indent=1)
