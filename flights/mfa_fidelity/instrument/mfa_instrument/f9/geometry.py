"""mfa_instrument/f9/geometry.py — Flight 9 module M1: the edge of a region and its components
(Contract F9 v0.7 §5.5 step 3; freeze record item 11).

The edge E of a region R (a boolean mask on the L×L torus) is the set of unit boundary segments
between a cell of R and a 4-neighbour outside R, with periodic wrapping. Each segment is represented
by its midpoint, a "bond". Every bond has equal weight.

A component is a connected piece of the boundary: two segments belong to the same component when
they meet at a cell corner. Where four segments meet at one corner (two cells of R touching only at
that corner), each of those cells' own two segments are joined to each other and not to the other
cell's. That is the convention of a 4-connected region and an 8-connected complement. So two cells
touching only at a corner have separate boundaries, a hole has its own component, and a strip that
wraps the torus has two.

The same routine serves the predicted side (a level set of a comparison array, `family`) and, in a
later module, the observed side (the occupied region). M1 uses it for the contour family only.

CANONICAL ORDER (a declaration of this module, so that identities are reproducible):
  bonds     — first every axis-0 bond in row-major order of its lower cell (i, j), the bond lying
              between cells (i, j) and (i+1, j) with midpoint (i + 0.5, j); then every axis-1 bond in
              row-major order, between (i, j) and (i, j+1) with midpoint (i, j + 0.5). Coordinates
              are in cells, in [0, L).
  components — numbered 0, 1, 2, … in order of first appearance along that bond order.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

from . import config as C
from .config import F9ConfigError


@dataclass(frozen=True)
class Edge:
    """The edge of one region: bond midpoints (n, 2) in cells, and the component number of each bond."""
    points: np.ndarray
    component: np.ndarray

    @property
    def n_bonds(self) -> int:
        return int(self.points.shape[0])

    @property
    def n_components(self) -> int:
        return int(self.component.max()) + 1 if self.component.size else 0

    def component_sizes(self) -> Tuple[int, ...]:
        """Bonds per component, in component order."""
        return tuple(int(k) for k in np.bincount(self.component, minlength=self.n_components)) if self.component.size else ()


def _check_mask(mask: np.ndarray) -> np.ndarray:
    m = np.asarray(mask)
    if m.dtype != np.bool_ or m.shape != (C.F9_GRID, C.F9_GRID):
        raise F9ConfigError("a region is a boolean (L, L) mask")
    return m


def edge(mask: np.ndarray) -> Edge:
    """Bonds and traced components of the region `mask`, in the canonical order of this module."""
    m = _check_mask(mask)
    L = C.F9_GRID
    b0 = m != np.roll(m, -1, axis=0)                  # axis-0 bond at (i, j): between (i, j) and (i+1, j)
    b1 = m != np.roll(m, -1, axis=1)                  # axis-1 bond at (i, j): between (i, j) and (i, j+1)
    n0 = int(b0.sum()); n1 = int(b1.sum()); n = n0 + n1
    if n == 0:
        return Edge(np.zeros((0, 2), dtype=np.float64), np.zeros((0,), dtype=np.int64))
    id0 = np.full((L, L), -1, dtype=np.int64); id0[b0] = np.arange(n0)
    id1 = np.full((L, L), -1, dtype=np.int64); id1[b1] = n0 + np.arange(n1)

    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb: parent[max(ra, rb)] = min(ra, rb)

    # The corner at the far corner of cell (a, b), shared by cells (a, b), (a+1, b), (a, b+1), (a+1, b+1).
    # The four segments that can end there:
    s_lo = id0                                        # axis-0 bond (a, b):   separates (a, b)   from (a+1, b)
    s_hi = np.roll(id0, -1, axis=1)                   # axis-0 bond (a, b+1): separates (a, b+1) from (a+1, b+1)
    t_lo = id1                                        # axis-1 bond (a, b):   separates (a, b)   from (a, b+1)
    t_hi = np.roll(id1, -1, axis=0)                   # axis-1 bond (a+1, b): separates (a+1, b) from (a+1, b+1)
    cnt = (s_lo >= 0).astype(np.int64) + (s_hi >= 0) + (t_lo >= 0) + (t_hi >= 0)
    if np.any((cnt == 1) | (cnt == 3)):               # impossible for a boundary: every corner has an even number of segments
        raise F9ConfigError("boundary segments do not close at a corner")
    for a, b in zip(*np.nonzero(cnt == 2)):
        seg = [int(s) for s in (s_lo[a, b], s_hi[a, b], t_lo[a, b], t_hi[a, b]) if s >= 0]
        union(seg[0], seg[1])
    for a, b in zip(*np.nonzero(cnt == 4)):
        # the region cells are one diagonal pair; each region cell's own two segments are joined to each other
        if m[a, b]:                                   # region cells (a, b) and (a+1, b+1)
            union(int(s_lo[a, b]), int(t_lo[a, b])); union(int(s_hi[a, b]), int(t_hi[a, b]))
        else:                                         # region cells (a+1, b) and (a, b+1)
            union(int(s_lo[a, b]), int(t_hi[a, b])); union(int(s_hi[a, b]), int(t_lo[a, b]))

    i0, j0 = np.nonzero(b0); i1, j1 = np.nonzero(b1)  # row-major, the same order the ids were assigned in
    pts = np.concatenate([np.stack([i0 + 0.5, j0.astype(np.float64)], axis=1),
                          np.stack([i1.astype(np.float64), j1 + 0.5], axis=1)]).astype(np.float64)
    roots = np.fromiter((find(k) for k in range(n)), dtype=np.int64, count=n)
    # `union` keeps the smallest id as root, so roots appear in increasing order of first appearance
    _uniq, comp = np.unique(roots, return_inverse=True)
    return Edge(pts, comp.astype(np.int64))


def is_informative(mask: np.ndarray, e: Edge = None) -> bool:
    """§5.5 step 4: the region and its complement each have at least 100 cells, and the edge has at least 40 bonds."""
    m = _check_mask(mask)
    inside = int(m.sum()); e = edge(m) if e is None else e
    return (inside >= C.F9_INFORMATIVE_MIN_CELLS and C.F9_N_CELLS - inside >= C.F9_INFORMATIVE_MIN_CELLS
            and e.n_bonds >= C.F9_INFORMATIVE_MIN_BONDS)
