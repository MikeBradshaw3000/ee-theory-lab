"""L1's reproduction of L2's M6B round-2 section 4.4 construction (constant index beside an unstable sibling), written from
L2's description. Constructed counts and a synthetic one-contour family; test master 777. Nothing here is part of the instrument."""
import hashlib, numpy as np
from mfa_instrument.f9 import evaluator as E, evaluator_reports as X, terrain as T
for m in (E, X): print(m.__name__, hashlib.sha256(open(m.__file__, "rb").read()).hexdigest())
omega = np.zeros((100, 100)); omega[1:49, :] = 1
P = E.IndexFamily(T.comparison_array("T0", "P"), "T0", "P"); H = E.IndexFamily(omega, "TB", "H")
print("family sizes", len(P), len(H))
fam = {"P": P, "H": H}
counts = np.zeros((40, 100, 100), dtype=np.int64); counts[:21, :50, :] = 400
key = E.arm_level_key(777, "TB", "H", 1_000_000); skey = X.skeleton_level_key(777, "TB", "H", 1_000_000)
placed = E.evaluate_level(counts, fam, key); copy = X.evaluate_level_at(counts, fam, key, 200_000); skel = X.skeleton_boundary(counts, fam, skey)["evaluation"]
for name, r in (("placed", placed), ("copy", copy), ("skeleton", skel)):
    h = r["indices"]["H"]
    print(name, r["point"]["region_cells"], r["point"]["bonds"], r["indices"]["P"], {k: h[k] for k in h if k in ("result", "cause", "n_compatible", "n_adverse", "n_invalid", "counts")})
print(sorted(placed["indices"]["H"]))
for name, r in (("placed", placed), ("copy", copy), ("skeleton", skel)):
    h = r["indices"]["H"]; print(name, {k: v for k, v in h.items() if isinstance(v, (int, str, bool)) or v is None})
def same(a, b):
    if isinstance(a, dict): return isinstance(b, dict) and a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, np.ndarray): return isinstance(b, np.ndarray) and a.dtype == b.dtype and a.shape == b.shape and (np.array_equal(a, b, equal_nan=True) if a.dtype.kind == "f" else np.array_equal(a, b))   # nan marks an invalid draw
    if isinstance(a, (list, tuple)): return type(a) is type(b) and len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return type(a) is type(b) and a == b
print("copy equals placed, every field:", same(copy, placed))
