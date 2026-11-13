"""Prototype of the Contract F9 v0.3 s5.5 evaluator, for cost measurement and definition checks on SYNTHETIC maps only.
Not an instrument module. Reads no probe output."""
import math, numpy as np
from scipy.spatial import cKDTree
L = 100; EPS = 2.0; M_RES = 40; QL = 0.95
def box(a): return sum(np.roll(np.roll(a, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1)) / 9.0
def _label_periodic(mask, eight):
    """Connected components on the torus. eight=False: 4-neighbour; eight=True: 8-neighbour. Returns int labels, 0 = not in mask."""
    lab = -np.ones((L, L), dtype=np.int64); idx = np.flatnonzero(mask.ravel()); parent = {int(i): int(i) for i in idx}
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    shifts = [(1, 0), (0, 1)] + ([(1, 1), (1, -1)] if eight else [])
    for di, dj in shifts:
        nb = np.roll(np.roll(mask, -di, 0), -dj, 1) & mask
        ii, jj = np.nonzero(nb)
        for i, j in zip(ii.tolist(), jj.tolist()):
            a = find(i * L + j); b = find(((i + di) % L) * L + (j + dj) % L)
            if a != b: parent[max(a, b)] = min(a, b)
    out = np.zeros((L, L), dtype=np.int64); roots = {}
    for i in idx.tolist():
        r = find(i); out.flat[i] = roots.setdefault(r, len(roots) + 1)
    return out
def edge(mask):
    """Bonds between a cell in the region and a 4-neighbour outside it; midpoint coordinates; component id per bond.
    A component is the set of bonds between one 4-connected region component and one 8-connected background component."""
    occ = _label_periodic(mask, False); bg = _label_periodic(~mask, True)
    pts = []; comp = []
    for ax in (0, 1):
        nxt = np.roll(mask, -1, ax); diff = mask != nxt; i, j = np.nonzero(diff)
        i2 = (i + 1) % L if ax == 0 else i; j2 = j if ax == 0 else (j + 1) % L
        inside_first = mask[i, j]
        o = np.where(inside_first, occ[i, j], occ[i2, j2]); b = np.where(inside_first, bg[i2, j2], bg[i, j])
        mid = np.stack([(i + 0.5) % L, j.astype(float)], 1) if ax == 0 else np.stack([i.astype(float), (j + 0.5) % L], 1)
        pts.append(mid); comp.append(o * 100000 + b)
    return np.concatenate(pts), np.concatenate(comp)
def q95(v): return float(np.quantile(v, QL))          # numpy default: linear interpolation
def S_joint(E, Ec, C, Cc):
    """max(global symmetric q95, q95 of every resolved component of E to C, of every resolved component of C to E)."""
    dE = cKDTree(C, boxsize=L).query(E)[0]; dC = cKDTree(E, boxsize=L).query(C)[0]
    s = max(q95(dE), q95(dC))
    for pts_c, d in ((Ec, dE), (Cc, dC)):
        ids, cnt = np.unique(pts_c, return_counts=True)
        for k in ids[cnt >= M_RES]: s = max(s, q95(d[pts_c == k]))
    return s
class Family:
    """All distinct proper superlevel masks of a quantized index (the complete family), with pruning support."""
    def __init__(self, lam):
        self.lam = lam; self.levels = np.unique(lam)[1:]            # mask(l) = lam >= l, proper and nonempty
        self._cache = {}
        ii, jj = np.meshgrid(np.arange(L), np.arange(L), indexing="ij"); self.cells = np.stack([ii.ravel(), jj.ravel()], 1).astype(float)
        self.tree = cKDTree(self.cells, boxsize=L); self.flat = lam.ravel()
    def contour(self, l):
        if l not in self._cache: self._cache[l] = edge(self.lam >= l)
        return self._cache[l]
    def admissible(self, E):
        """Levels that can possibly have q95(E -> C) <= EPS: a contour bond within EPS of e has both its cells within EPS + 0.5 of e,
        so its level lies in [min, max] of the index over those cells. Necessary condition; exact."""
        nb = self.tree.query_ball_point(E, EPS + 0.5 + 1e-9)
        lo = np.array([self.flat[n].min() for n in nb]); hi = np.array([self.flat[n].max() for n in nb])
        need = int(math.floor(QL * (len(E) - 1))) + 1                 # order statistics that must be <= EPS under linear interpolation
        cov = np.searchsorted(np.sort(lo), self.levels, side="left")  # bonds with lo < l   (level must exceed the lower cell)
        cov = cov - np.searchsorted(np.sort(hi), self.levels, side="left")  # minus bonds with hi < l
        return self.levels[cov >= need]
def evaluate(pmap, fam, theta, registered=None):
    """Returns dict: informative, within (exact over the complete family), n_adm, S_min over admissible (or None)."""
    mask = box(pmap) >= theta; n = int(mask.sum())
    if n < 100 or L * L - n < 100: return dict(informative=False)
    E, Ec = edge(mask)
    if len(E) < 40: return dict(informative=False)
    adm = fam.admissible(E); best = None
    for l in adm:
        C, Cc = fam.contour(l); s = S_joint(E, Ec, C, Cc)
        if best is None or s < best[0]: best = (s, float(l))
    return dict(informative=True, within=bool(best is not None and best[0] <= EPS), n_adm=int(len(adm)), best=best, n_bonds=int(len(E)))
