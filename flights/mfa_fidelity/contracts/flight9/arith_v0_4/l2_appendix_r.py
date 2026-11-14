from pathlib import Path
import sys
import numpy as np
from scipy.spatial import cKDTree

root = Path(sys.argv[1]).resolve()
arith = root / "flights/mfa_fidelity/contracts/flight9/arith_v0_3"
sys.path.insert(0, str(arith))
import f9_evaluator_proto as E
import f9_terrains as T

L = 100

def counts_for(mask):
    # Invert the periodic box mean, then certify the result in integers.
    signed = np.where(mask, 1, -1)
    f = (1 + 2*np.cos(2*np.pi*np.arange(L)/L))/3
    inverse = np.fft.ifft2(
        np.fft.fft2(signed)/(f[:, None]*f[None, :])
    ).real
    A = 200 + np.rint(inverse).astype(np.int64)
    summed = sum(
        np.roll(np.roll(A, i, 0), j, 1)
        for i in (-1, 0, 1) for j in (-1, 0, 1)
    )
    assert np.array_equal(summed, 9*(200 + signed))
    assert 0 <= A.min() <= A.max() <= 1000
    assert np.array_equal(E.box(A/1000) >= .2, mask)
    return A

def bonds(mask):
    points = []
    for axis in (0, 1):
        i, j = np.nonzero(mask != np.roll(mask, -1, axis))
        points.append(
            np.column_stack(((i+.5) % L, j))
            if axis == 0 else
            np.column_stack((i, (j+.5) % L))
        )
    return np.concatenate(points)

def global_score(a, b):
    return max(
        E.q95(cKDTree(b, boxsize=L).query(a)[0]),
        E.q95(cKDTree(a, boxsize=L).query(b)[0])
    )

# Q4: two disconnected loops merged by one region/background pair.
x, y = np.indices((L, L))
a = np.where(y % 2 == 0, 2, 40)
predicted = (x >= a) & (x < 60)
observed = (x >= a) & (x < 70)
ep, ec = E.edge(observed)
cp, cc = E.edge(predicted)
d = cKDTree(cp, boxsize=L).query(ep)[0]
straight = np.isclose(ep[:, 0], 69.5)
assert len(ep) == len(cp) == 4000
assert len(np.unique(ec)) == len(np.unique(cc)) == 1
assert straight.sum() == 100
assert E.q95(d[straight]) == 10
assert E.S_joint(ep, ec, cp, cc) == 0
A = counts_for(observed)
q4 = E.evaluate(A/1000, E.Family(predicted.astype(float)), .2)
assert q4["informative"] and q4["within"]
print("Q4:", int(A.min()), int(A.max()), q4)

# Q9: actual TC arrays, translated highest rounded-P contour.
probe = root / "flights/mfa_fidelity/design/flight9/probe/f9_probe.py"
P = T.load_probe(str(probe))
v, u, r = T.all_terrains(P)["TC"]
lam = {
    name: T.quantize(P.compose(name, v, u, r))
    for name in ("P", "H")
}
observed = np.roll(lam["P"] >= .729, 2, axis=0)
A = counts_for(observed)
ep, ec = E.edge(observed)
assert observed.sum() == 739 and len(ep) == 396
print("TC counts:", int(A.min()), int(A.max()))

for name in ("P", "H"):
    family = E.Family(lam[name])
    best_global, level = min(
        (global_score(ep, bonds(lam[name] >= level)), float(level))
        for level in family.levels
    )
    cp, cc = family.contour(level)
    attained_joint = E.S_joint(ep, ec, cp, cc)
    assert attained_joint == best_global
    result = E.evaluate(A/1000, family, .2)
    assert result["within"] == (name == "P")
    print(name, len(family.levels), best_global,
          attained_joint, level, result)

