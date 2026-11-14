"""Run: python round3_review_checks.py <extracted-packet-root> [--diagonals].

Uses terrain formulas and synthetic maps only. No lattice dynamics or probe
observation file is read. The full rounded-family global lower bound and an
attained joint score certify its exact joint minimum independently of pruning.
"""
from pathlib import Path
import sys
import numpy as np
from scipy.spatial import cKDTree

root = Path(sys.argv[1]).resolve()
arith = root / "flights/mfa_fidelity/contracts/flight9/arith_v0_4"
sys.path.insert(0, str(arith))
import f9_compare as T
import f9_evaluator_proto_v4 as E

P = T.load_probe(str(root / "flights/mfa_fidelity/design/flight9/probe/f9_probe.py"))
v, u, r = T.all_terrains(P)["TD-1-2"]
raw = P.compose("H", v, u, r)
omega = T.comparison_array(P, "TD-1-2", "H", v, u, r)
assert np.array_equal(omega, T.comparison_array(P, "TD-1-2", "P", v, u, r))
raw_cut = np.unique(raw)[1]
mask = raw >= raw_cut

# All 40 seeds receive this valid integer occupancy-count array.
# Its 3x3 mean is exactly .201 inside mask and .199 outside, in integer arithmetic.
signed = np.where(mask, 1, -1)
f = (1 + 2*np.cos(2*np.pi*np.arange(100)/100))/3
A = 200 + np.rint(np.fft.ifft2(
    np.fft.fft2(signed)/(f[:, None]*f[None, :])
).real).astype(np.int64)
summed = sum(np.roll(np.roll(A, i, 0), j, 1)
             for i in (-1, 0, 1) for j in (-1, 0, 1))
assert np.array_equal(summed, 9*(200 + signed))
assert 0 <= A.min() <= A.max() <= 1000
assert np.array_equal(E.box(A/1000) >= .2, mask)

ep, ec = E.edge(mask)
assert E.S_joint(ep, ec, *E.edge(raw >= raw_cut)) == 0
family = E.Family(omega)

def global_lower_bound(level):
    cp, _ = family.contour(level)
    return max(E.q95(cKDTree(cp, boxsize=100).query(ep)[0]),
               E.q95(cKDTree(ep, boxsize=100).query(cp)[0]))

bound, level = min((global_lower_bound(l), float(l)) for l in family.levels)
joint_at_level = E.S_joint(ep, ec, *family.contour(level))
assert joint_at_level == bound
assert bound > 2
pruned = E.evaluate(A/1000, family, .2)
assert pruned["informative"] and not pruned["within"]

print("Raw H cut:", repr(float(raw_cut)))
print("Raw / rounded proper-family sizes:", len(np.unique(raw))-1, len(family.levels))
print("Region / complement:", int(mask.sum()), int((~mask).sum()))
print("Bonds / component sizes:", len(ep), np.unique(ec, return_counts=True)[1].tolist())
print("Counts per 1000 ticks:", int(A.min()), int(A.max()))
print("Raw joint minimum:", 0.0)
print("Rounded joint minimum / level:", bound, level)
print("Pruned result:", pruned)
print("Identical 40-map panel: raw nC/nA/nI = 1000/0/0;")
print("rounded nC/nA/nI = 0/1000/0 for both P and H.")


# Exhaust every canonical comparison contour; no component routine is needed.
terrains = T.all_terrains(P)
perimeters = {}
for name, (v, u, r) in terrains.items():
    if name == "T0":
        continue
    for comp in "PH":
        w = T.comparison_array(P, name, comp, v, u, r)
        maximum = 0
        for cut in np.unique(w)[1:]:
            m = w >= cut
            nb = (np.count_nonzero(m != np.roll(m, 1, 0))
                  + np.count_nonzero(m != np.roll(m, 1, 1)))
            maximum = max(maximum, int(nb))
        perimeters[name + "." + comp] = maximum
print("Maximum perimeters:", perimeters)
assert max(perimeters.values()) == 768
assert 40 / 768 > .05 and 42 / 768 > .05

# The actual clipped-normal mean of a permitted small-positive-noise sweep.
from scipy.special import ndtr
from scipy.stats import beta
sigma = .001
minimum_margin = 1.
sweeps = {}
for name, (v, u, r) in terrains.items():
    if name == "T0":
        continue
    for comp in "PH":
        w = T.comparison_array(P, name, comp, v, u, r)
        z = (w - w.min()) / (w.max() - w.min())
        informative = 0
        occupied = []
        for k in range(25):
            mean0 = (.03 + .07*k/24) + (.2 + .4*k/24)*z
            a, b = -mean0/sigma, (1-mean0)/sigma
            phi_a = np.exp(-a*a/2) / np.sqrt(2*np.pi)
            phi_b = np.exp(-b*b/2) / np.sqrt(2*np.pi)
            mu = mean0*(ndtr(b)-ndtr(a)) - sigma*(phi_b-phi_a) + ndtr(-b)
            smooth = E.box(mu)
            region = smooth >= .2
            n = int(region.sum())
            nb = (np.count_nonzero(region != np.roll(region, 1, 0))
                  + np.count_nonzero(region != np.roll(region, 1, 1)))
            informative += int(100 <= n <= 9900 and nb >= 40)
            occupied.append(n)
            minimum_margin = min(minimum_margin, float(np.abs(smooth-.2).min()))
        sweeps[name + "." + comp] = (informative, min(occupied), max(occupied))
assert all(row[0] == 25 for row in sweeps.values())
print("Sweep (informative, min area, max area):", sweeps)
print("Minimum absolute threshold margin:", minimum_margin)
print("One-sided CP upper, 12/200:", beta.ppf(.95, 13, 188))
print("One-sided CP upper, 13/200:", beta.ppf(.95, 14, 187))

# Optional: certify the intermediate-band witnesses by exhaustive joint search.
if "--diagonals" in sys.argv[2:]:
    for name in ("TD-4-2", "TC"):
        v, u, r = terrains[name]
        w = T.comparison_array(P, name, "P", v, u, r)
        h = .06 + .40*(w-w.min())/(w.max()-w.min())
        family = E.Family(w)
        for dx, dy in ((1, 1), (2, 1), (2, 2)):
            shifted = np.roll(np.roll(h, dx, 0), dy, 1)
            result = E.evaluate(shifted, family, .2, brute=True)
            assert result["informative"]
            print("Diagonal:", name, dx, dy, result["best"][0])
