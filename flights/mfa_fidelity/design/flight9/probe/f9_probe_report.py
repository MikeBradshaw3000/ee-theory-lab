#!/usr/bin/env python3
"""Flight 9 pre-contract probe -- the declared report (NONCANONICAL, descriptive only).

Computes exactly the quantities R-1 ... R-8 of FLIGHT_9_PRE_PROBE_DECLARATION s5 from a completed probe output
directory, and nothing else. It computes no lambda-contour statistic, extracts no edge and renders no map.

usage: f9_probe_report.py OUT_DIR > report.json
"""
from __future__ import annotations

import hashlib, json, math, os, sys
from collections import defaultdict
import numpy as np

import f9_probe as P

FLOOR_REF = {W: 1.0 - (1.0 - (0.01 / (0.01 + P.Q_DE))) * (1.0 - 0.01) ** (W - 1) for W in P.WINDOWS}


def main(out_dir: str) -> dict:
    man = json.load(open(os.path.join(out_dir, "PROBE_MANIFEST.json")))
    if not os.path.exists(os.path.join(out_dir, "COMPLETE")): raise SystemExit("probe output is not complete")
    runs = man["runs"]
    groups = defaultdict(list)
    for r in runs: groups[(r["L"], r["terrain"], r["composition"], r["object"], r["kappa_micro"])].append(r)
    rep = {"manifest_sha256": hashlib.sha256(open(os.path.join(out_dir, "PROBE_MANIFEST.json"), "rb").read()).hexdigest(),
           "declaration_sha256": man["declaration_sha256"], "script_sha256": man["script_sha256"],
           "n_runs": len(runs), "floor_reference": {str(W): FLOOR_REF[W] for W in P.WINDOWS}}

    # R-1 seconds per run
    r1 = defaultdict(list)
    for r in runs: r1[(r["L"], r["object"])].append(r["seconds"])
    rep["R1_seconds_per_run"] = {f"L{L}_{o}": {"mean": float(np.mean(s)), "max": float(np.max(s)), "n": len(s)} for (L, o), s in sorted(r1.items())}

    occ = {}                # seed-mean W=1 occupancy maps, realization only
    r2, r3, r7, r8 = {}, {}, {}, {}
    for key, rs in sorted(groups.items()):
        L, name, comp, obj, km = key
        tag = f"L{L}_{name}_{comp}_{obj}_k{km}"
        dens = [r["tail_density"] for r in rs]
        r2[tag] = {"mean_tail_density": float(np.mean(dens)), "n_seeds": len(rs),
                   "survivors": int(sum(bool(r["survival"]) for r in rs)) if obj == "skeleton_high" else None}
        r7[tag] = {"sd_tail_density": float(np.std(dens, ddof=1)) if len(dens) > 1 else None}
        maps = []; v8 = {str(W): {"all_active_cells": 0, "all_inactive_cells": 0, "range_violations": 0} for W in P.WINDOWS}
        for r in rs:
            z = np.load(os.path.join(out_dir, r["file"]))
            for W in P.WINDOWS:
                n = r[f"n_windows_W{W}"]; A = z[f"A_W{W}"]; R0 = z[f"R0_W{W}"]
                v8[str(W)]["all_active_cells"] += int((A == n).sum()); v8[str(W)]["all_inactive_cells"] += int((A == 0).sum())
                v8[str(W)]["range_violations"] += int(((A < 0) | (A > n) | (R0 < 0) | (R0 > (n + 1) // 2) | ((A == n) & (R0 != 0)) | ((A < n) & (R0 < 1))).sum())
            maps.append(z["A_W1"].astype(np.float64) / r["n_windows_W1"])
        r8[tag] = v8
        if obj == "realization":
            m = np.mean(maps, axis=0); occ[(L, name, comp, km)] = m
            r3[tag] = {"p05": float(np.percentile(m, 5)), "p50": float(np.percentile(m, 50)), "p95": float(np.percentile(m, 95))}
    rep["R2_density_and_survival"] = r2; rep["R3_occupancy_percentiles_W1"] = r3
    rep["R7_seed_sd_tail_density"] = r7; rep["R8_summary_record_validity"] = r8

    # R-4 correlation between the two composition arms' occupancy maps (same terrain, L, kappa)
    r4 = {}
    for (L, name, comp, km), m in sorted(occ.items()):
        if comp != "P" or (L, name, "H", km) not in occ: continue
        h = occ[(L, name, "H", km)]
        sd = (float(m.std()), float(h.std()))
        r4[f"L{L}_{name}_k{km}"] = float(np.corrcoef(m.ravel(), h.ravel())[0, 1]) if min(sd) > 0 else None
    rep["R4_P_vs_H_map_correlation"] = r4

    # R-5 TB: fraction of across-cell variance of occupancy carried by the x-only means (x is array axis 0)
    r5 = {}
    for (L, name, comp, km), m in sorted(occ.items()):
        if name != "TB": continue
        tot = float(m.var())
        r5[f"L{L}_TB_{comp}_k{km}"] = float(m.mean(axis=1).var() / tot) if tot > 0 else None
    rep["R5_TB_x_only_variance_fraction"] = r5

    # R-6 TC: mean occupancy inside the patch (bump >= 0.5) and outside it (bump <= 0.05); geometry-defined
    r6 = {}
    for (L, name, comp, km), m in sorted(occ.items()):
        if name != "TC": continue
        b = P.tc_bump(L); inside = float(m[b >= 0.5].mean()); outside = float(m[b <= 0.05].mean())
        r6[f"L{L}_TC_{comp}_k{km}"] = {"inside": inside, "outside": outside, "ratio": (inside / outside) if outside > 0 else None,
                                       "n_inside": int((b >= 0.5).sum()), "n_outside": int((b <= 0.05).sum())}
    rep["R6_TC_inside_outside_occupancy"] = r6
    return rep


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1]), indent=1, sort_keys=True))
