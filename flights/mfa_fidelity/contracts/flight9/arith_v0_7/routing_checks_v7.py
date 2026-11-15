#!/usr/bin/env python3
"""Contract F9 v0.7: support checks of (R5-1) the routing of constant maps by their clipped population value and (R5-2) the
row-15 error event. Scalar arithmetic only: no terrain, no lattice run, no probe output. The noise values used are
illustrative; sigma_seed is derived from the calibration census, which has not been run.
Usage: routing_checks_v7.py <out.json>"""
import sys, json, math
THETA, HALF = 0.20, 0.06
def Phi(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def phi(x): return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
def a_of(c, s):                                               # mean of clip(c + s Z, 0, 1): the population value of a constant map
    if s == 0: return float(c)
    lo, hi = -c / s, (1 - c) / s
    return c * (Phi(hi) - Phi(lo)) - s * (phi(hi) - phi(lo)) + 1 - Phi(hi)
def route(c, s): return "capped" if abs(a_of(c, s) - THETA) >= HALF else "near"
out = {}
N = 37001; grid = [0.03 + 0.37 * i / (N - 1) for i in range(N)]   # c uniform on [0.03, 0.40], step 1e-5
# 1. zero noise: the routing reproduces v0.6's ranges
cap = [c for c in grid if route(c, 0) == "capped"]; near = [c for c in grid if route(c, 0) == "near"]
out["zero_noise"] = dict(capped_low_max=max(c for c in cap if c < THETA), capped_high_min=min(c for c in cap if c > THETA),
                         near_min=min(near), near_max=max(near), capped_fraction=len(cap) / N, near_fraction=len(near) / N,
                         endpoint_c_0_14=route(0.14, 0), endpoint_c_0_26=route(0.26, 0))
# 2. L2's round-5 witnesses
out["witnesses"] = {"c=0.13,s=0.31": dict(a=a_of(0.13, 0.31), row=route(0.13, 0.31), v0_6_row="capped"),
                    "c=0.25,s=0.35": dict(a=a_of(0.25, 0.35), row=route(0.25, 0.35), v0_6_row="near"),
                    "c=0.13,s=0.312351766810106": dict(a=a_of(0.13, 0.312351766810106), row=route(0.13, 0.312351766810106), v0_6_row="capped")}
# 3. share of the proposal routed to each row at illustrative constant noise levels (both rows need 2% to fill within budget)
fr = {}
for s in (0.0, 0.02, 0.05, 0.10, 0.20, 0.31, 0.35):
    r = [route(c, s) for c in grid]; a = [a_of(c, s) for c in grid]
    fr["s=%.2f" % s] = dict(capped=r.count("capped") / N, near=r.count("near") / N, a_min=min(a), a_max=max(a))
out["routing_shares_at_constant_sigma"] = fr
out["needed_share"] = dict(capped=50 / 2500, near=200 / 10000)
# 4. the saturated range [0.60, 1.00]: least population value at the same noise levels
out["saturated_min_population_value"] = {"s=%.2f" % s: min(a_of(0.60 + 0.40 * i / 4000, s) for i in range(4001)) for s in (0.0, 0.10, 0.20, 0.35)}
# 5. the reference cause of a sample by the precedence of s7 (L2..L7), and the row-15 error event for the three map states
def reference(family_empty, cells_in, cells_out, bonds, n_invalid, n_compat, n_adverse):
    if family_empty: return "no eligible contour"
    if cells_in == 0 or cells_out == 0: return "no edge at theta"
    if cells_in < 100 or cells_out < 100 or bonds < 40: return "under-resolved"
    if n_invalid > 50: return "unstable edge"
    if n_compat >= 950: return "compatible"
    if n_adverse >= 950: return "adverse"
    return "finite resolution"
def error(output, sample, apparatus_failure=False):
    return apparatus_failure or output in ("compatible", "adverse") or output != reference(**sample)
S = lambda **k: dict(dict(family_empty=False, cells_in=0, cells_out=10000, bonds=0, n_invalid=0, n_compat=0, n_adverse=0), **k)
cases = {
 "empty sample, reported no edge": ("no edge at theta", S()),
 "empty sample, reported under-resolved (L2's witness)": ("under-resolved", S()),
 "60-cell sample region, reported under-resolved": ("under-resolved", S(cells_in=60, cells_out=9940, bonds=34)),
 "60-cell sample region, reported no edge": ("no edge at theta", S(cells_in=60, cells_out=9940, bonds=34)),
 "informative sample, 300 invalid draws, reported unstable edge": ("unstable edge", S(cells_in=400, cells_out=9600, bonds=90, n_invalid=300)),
 "informative sample, 20 invalid draws, reported unstable edge": ("unstable edge", S(cells_in=400, cells_out=9600, bonds=90, n_invalid=20, n_compat=500, n_adverse=480)),
 "informative sample, neither count at 950, reported finite resolution": ("finite resolution", S(cells_in=400, cells_out=9600, bonds=90, n_invalid=20, n_compat=500, n_adverse=480)),
 "non-constant family, reported no eligible contour": ("no eligible contour", S()),
 "informative sample, 960 adverse, reported adverse": ("adverse", S(cells_in=400, cells_out=9600, bonds=90, n_adverse=960)),
}
out["row15_error_event"] = {k: dict(output=o, reference=reference(**s), error=bool(error(o, s))) for k, (o, s) in cases.items()}
json.dump(out, open(sys.argv[1], "w"), indent=1); print(json.dumps(out, indent=1))
