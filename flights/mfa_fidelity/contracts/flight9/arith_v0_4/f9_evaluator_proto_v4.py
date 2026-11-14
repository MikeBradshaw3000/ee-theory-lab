"""Prototype of the Contract F9 v0.4 s5.5 evaluator: connected traced contour components (F1).
For definition checks and cost measurement on SYNTHETIC maps only. Not an instrument module. Reads no probe output."""
import math, numpy as np
from scipy.spatial import cKDTree
L = 100; EPS = 2.0; M_RES = 40; QL = 0.95
def box(a): return sum(np.roll(np.roll(a, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1)) / 9.0
def edge(mask):
    """Boundary segments ("bonds") between a cell of the region and a 4-neighbour outside it, as midpoints, with a component id each.
    A component is a connected piece of the boundary: segments are joined where they meet at a cell corner. Where four segments meet
    (two region cells touching only at that corner) each region cell's own two segments are joined to each other and not to the other cell's,
    which is the convention of a 4-connected region and an 8-connected complement. Periodic in both directions."""
    m = mask
    b0 = m != np.roll(m, -1, 0)            # ax0 bond (i,j): between cell (i,j) and (i+1,j); corners (i,j-1) and (i,j)
    b1 = m != np.roll(m, -1, 1)            # ax1 bond (i,j): between cell (i,j) and (i,j+1); corners (i-1,j) and (i,j)
    id0 = -np.ones((L, L), dtype=np.int64); id1 = -np.ones((L, L), dtype=np.int64)
    n0 = int(b0.sum()); n1 = int(b1.sum()); id0[b0] = np.arange(n0); id1[b1] = n0 + np.arange(n1)
    parent = np.arange(n0 + n1)
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[max(ra, rb)] = min(ra, rb)
    # corner (a,b) is shared by cells (a,b), (a+1,b), (a,b+1), (a+1,b+1); its four possible segments:
    s_lo = id0; s_hi = np.roll(id0, -1, 1)           # ax0 bond (a,b), ax0 bond (a,b+1)
    t_lo = id1; t_hi = np.roll(id1, -1, 0)           # ax1 bond (a,b), ax1 bond (a+1,b)
    cnt = (s_lo >= 0).astype(int) + (s_hi >= 0) + (t_lo >= 0) + (t_hi >= 0)
    for a, b in zip(*np.nonzero(cnt == 2)):
        seg = [s for s in (s_lo[a, b], s_hi[a, b], t_lo[a, b], t_hi[a, b]) if s >= 0]; union(seg[0], seg[1])
    for a, b in zip(*np.nonzero(cnt == 4)):
        # region cells are a diagonal pair; join each region cell's own two segments
        if m[a, b]:   union(s_lo[a, b], t_lo[a, b]); union(s_hi[a, b], t_hi[a, b])      # cells (a,b) and (a+1,b+1)
        else:         union(s_lo[a, b], t_hi[a, b]); union(s_hi[a, b], t_lo[a, b])      # cells (a+1,b) and (a,b+1)
    assert not np.any((cnt == 1) | (cnt == 3))
    i0, j0 = np.nonzero(b0); i1, j1 = np.nonzero(b1)
    pts = np.concatenate([np.stack([(i0 + 0.5) % L, j0.astype(float)], 1), np.stack([i1.astype(float), (j1 + 0.5) % L], 1)])
    comp = np.array([find(k) for k in range(n0 + n1)], dtype=np.int64)
    return pts, comp
def q95(v): return float(np.quantile(v, QL))
def S_terms(E, Ec, C, Cc):
    dE = cKDTree(C, boxsize=L).query(E)[0]; dC = cKDTree(E, boxsize=L).query(C)[0]
    terms = {"global_E": q95(dE), "global_C": q95(dC), "comp_E": [], "comp_C": []}
    for key, pts_c, d in (("comp_E", Ec, dE), ("comp_C", Cc, dC)):
        ids, cnt = np.unique(pts_c, return_counts=True)
        for k, n in zip(ids, cnt):
            if n >= M_RES: terms[key].append((int(n), q95(d[pts_c == k])))
    return terms
def S_joint(E, Ec, C, Cc):
    t = S_terms(E, Ec, C, Cc); return max([t["global_E"], t["global_C"]] + [v for _, v in t["comp_E"]] + [v for _, v in t["comp_C"]])
class Family:
    def __init__(self, omega):
        self.lam = omega; self.levels = np.unique(omega)[1:]; self._cache = {}
        ii, jj = np.meshgrid(np.arange(L), np.arange(L), indexing="ij"); self.tree = cKDTree(np.stack([ii.ravel(), jj.ravel()], 1).astype(float), boxsize=L); self.flat = omega.ravel()
    def contour(self, l):
        if l not in self._cache: self._cache[l] = edge(self.lam >= l)
        return self._cache[l]
    def admissible(self, E):
        nb = self.tree.query_ball_point(E, EPS + 0.5 + 1e-9)
        lo = np.array([self.flat[n].min() for n in nb]); hi = np.array([self.flat[n].max() for n in nb])
        need = int(math.floor(QL * (len(E) - 1))) + 1
        cov = np.searchsorted(np.sort(lo), self.levels, side="left") - np.searchsorted(np.sort(hi), self.levels, side="left")
        return self.levels[cov >= need]
def region(pmap, theta): return box(pmap) >= theta
def evaluate(pmap, fam, theta, brute=False):
    mask = region(pmap, theta); n = int(mask.sum())
    if n < 100 or L * L - n < 100: return dict(informative=False)
    E, Ec = edge(mask)
    if len(E) < 40: return dict(informative=False)
    cand = fam.levels if brute else fam.admissible(E); best = None
    for l in cand:
        s = S_joint(E, Ec, *fam.contour(l))
        if best is None or s < best[0]: best = (s, float(l))
    return dict(informative=True, within=bool(best is not None and best[0] <= EPS), n_examined=int(len(cand)), best=best, n_bonds=int(len(E)))
