"""mfa_instrument/f9/family.py — Flight 9 module M1: the registered contour family of a comparison
array (Contract F9 v0.7 §5.5 step 5; §3.4 steps 3 and 4; §1.2 B).

For a comparison array ω, the family is every set {ω ≥ ℓ} for ℓ a distinct value of ω other than its
minimum. Each set is non-empty and proper, no two are equal, and the family is every level set of ω.
It is the REGISTERED family: complete for ω, and not for the raw index. A constant ω has an empty
family (`no eligible contour`).

IDENTITY (a declaration of this module). The family's identity is the SHA-256 of, for each level in
increasing order: the level as a little-endian float64 (struct "<d"), then the mask packed to bits in
row-major order (numpy.packbits, big-endian bit order within a byte). Two families have the same
identity exactly when they have the same levels and the same masks. The MASK identity omits the
levels, so that two arrays with different values and the same nested masks can be compared as sets
of masks. The COMPONENT identity binds the traced partition itself: per level in order, the number of
bonds and the number of components (struct "<ii"), then the component number of every bond in the
canonical bond order of `geometry` (int32, little-endian). The bond positions are determined by the
mask and that order, so the mask identity together with the component identity fixes which bonds
belong to which component. Counts and sizes alone would not: two different partitions of the same
bonds can have the same sizes (L2, M1 round 1, R1).
"""
from __future__ import annotations

import hashlib
import struct
from typing import Dict, Tuple

import numpy as np

from . import config as C
from . import geometry as G
from .config import F9ConfigError


class Family:
    """The registered family of one comparison array. Holds the array and its levels; masks and edges are built on demand."""

    def __init__(self, omega: np.ndarray):
        om = np.asarray(omega)
        if om.dtype != np.float64 or om.shape != (C.F9_GRID, C.F9_GRID) or not np.all(np.isfinite(om)):
            raise F9ConfigError("a comparison array is a finite float64 (L, L) array")
        self.omega = om
        self.levels: Tuple[float, ...] = tuple(float(x) for x in np.unique(om)[1:])

    def __len__(self) -> int:
        return len(self.levels)

    @property
    def is_empty(self) -> bool:
        return len(self.levels) == 0

    def mask(self, level: float) -> np.ndarray:
        if level not in self.levels: raise F9ConfigError("not a registered level of this family")
        return self.omega >= level

    def contour(self, level: float) -> G.Edge:
        return G.edge(self.mask(level))


def masks_identity(omega: np.ndarray) -> str:
    """The mask identity of the registered family of ω, without tracing any contour."""
    fam = Family(omega); h = hashlib.sha256()
    for ell in fam.levels: h.update(np.packbits(fam.mask(ell).ravel()).tobytes())
    return h.hexdigest()

def family_summary(omega: np.ndarray) -> Dict[str, object]:
    """Identities and descriptive counts of the registered family of ω. Every contour is traced once."""
    fam = Family(omega)
    h_family = hashlib.sha256(); h_masks = hashlib.sha256(); h_comp = hashlib.sha256()
    n_bonds = []; n_comp = []; cells = []
    prev = None
    for ell in fam.levels:
        m = fam.mask(ell)
        k = int(m.sum())
        if k == 0 or k == C.F9_N_CELLS: raise F9ConfigError("a registered level set is empty or the whole lattice")
        if prev is not None and not (np.all(prev[m]) and k < int(prev.sum())):
            raise F9ConfigError("registered level sets are not strictly nested")
        prev = m
        packed = np.packbits(m.ravel()).tobytes()
        h_family.update(struct.pack("<d", ell)); h_family.update(packed); h_masks.update(packed)
        e = G.edge(m)
        sizes = e.component_sizes()
        h_comp.update(struct.pack("<ii", e.n_bonds, len(sizes))); h_comp.update(np.asarray(e.component, dtype="<i4").tobytes())
        n_bonds.append(e.n_bonds); n_comp.append(len(sizes)); cells.append(k)
    lev = np.asarray(fam.levels, dtype=np.float64)
    gaps = np.diff(lev) if len(lev) > 1 else np.zeros((0,))
    return {
        "n_levels": len(fam.levels),
        "family_sha256": h_family.hexdigest(), "masks_sha256": h_masks.hexdigest(), "components_sha256": h_comp.hexdigest(),
        "level_min": float(lev[0]) if len(lev) else None, "level_max": float(lev[-1]) if len(lev) else None,
        "min_level_gap": float(gaps.min()) if gaps.size else None,
        "bonds_min": min(n_bonds) if n_bonds else None, "bonds_max": max(n_bonds) if n_bonds else None,
        "components_max": max(n_comp) if n_comp else None,
        "cells_min": min(cells) if cells else None, "cells_max": max(cells) if cells else None,
    }
