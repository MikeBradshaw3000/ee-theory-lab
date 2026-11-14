#!/usr/bin/env python3
"""Contract F9 v0.5: support checks of the special arm and flight constructions of s6.2, at ZERO noise (the pre-noise maps
themselves). SYNTHETIC maps and terrain arrays only; no lattice run; no probe output. These show the constructions can be built;
they are not certificates for any calibration-derived noise, under which s6.0 governs acceptance.
Usage: special_constructions_v5.py <f9_probe.py> <dir of arith_v0_4> <out.json>"""
import sys, json, numpy as np
sys.path.insert(0, sys.argv[2])
import f9_compare as T, f9_evaluator_proto_v4 as EV
P = T.load_probe(sys.argv[1]); terr = T.all_terrains(P); out = {}
K = 25
def hk(k, z): return (0.03 + 0.07 * k / (K - 1)) + (0.2 + 0.4 * k / (K - 1)) * z          # k = 0..24
def scale(w): return (w - w.min()) / (w.max() - w.min())
def level(pmap, fam):
    e = EV.evaluate(pmap, fam, 0.20)
    if not e["informative"]: return "ni"
    return "c" if e["within"] else "a"
def arm_rule(own):                                                                         # s5.6 arm tier, no apparatus state
    inf = [i for i, s in enumerate(own) if s != "ni"]
    if any(own[i] == "a" and own[i + 1] == "a" for i in range(K - 1)): return "ADVERSE"
    if len(inf) >= 3 and all(own[i] == "c" for i in inf): return "COMPATIBLE"
    return "NOT DISTINGUISHED"
arrays = {}
for name in ("TA", "TB", "TC", "TD-1-2", "TD-1-4", "TD-4-2", "TD-4-4"):
    v, u, r = terr[name]
    if name == "TB":
        for c in "PH": arrays["TB." + c] = T.comparison_array(P, name, c, v, u, r)
    else: arrays[name] = T.comparison_array(P, name, "P", v, u, r)
fams = {k: EV.Family(w) for k, w in arrays.items()}
# A. generic sweep, untranslated and translated three cells along axis 0 and along axis 1
A = {}
for k_, w in arrays.items():
    z = scale(w); row = {}
    for tag, (dx, dy) in (("0,0", (0, 0)), ("3,0", (3, 0)), ("0,3", (0, 3))):
        own = [level(np.roll(np.roll(hk(k, z), dx, 0), dy, 1), fams[k_]) for k in range(K)]
        row[tag] = dict(levels="".join(x[0] for x in own), informative=sum(s != "ni" for s in own), arm=arm_rule(own))
    A[k_] = row
out["generic_sweep"] = A
# B. low-information arm: flat-low map everywhere except two adjacent grid positions
B = {}
for k_, w in arrays.items():
    z = scale(w); res = set()
    for j in range(K - 1):
        own = [level(hk(k, z) if k in (j, j + 1) else 0.03 + 0.05 * z, fams[k_]) for k in range(K)]
        res.add((arm_rule(own), sum(s != "ni" for s in own)))
    B[k_] = sorted(res)
out["low_information_arm_over_24_positions"] = B
# C. TB: own and rival status per level for each generating index
C = {}
for gen in "PH":
    z = scale(arrays["TB." + gen]); other = "H" if gen == "P" else "P"
    own = [level(hk(k, z), fams["TB." + gen]) for k in range(K)]; riv = [level(hk(k, z), fams["TB." + other]) for k in range(K)]
    C["generated_from_" + gen] = dict(against_generating_index="".join(x[0] for x in own), against_other_index="".join(x[0] for x in riv))
out["TB_cross"] = C
json.dump(out, open(sys.argv[3], "w"), indent=1); print(json.dumps(out, indent=1))
