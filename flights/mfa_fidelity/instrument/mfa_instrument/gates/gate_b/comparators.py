"""gates/gate_b/comparators.py — the frozen comparator set (Gate B v0.4 §1.1).

  * float64 arrays and scalars: RAW BIT EQUALITY via uint64 view — signed-zero
    discriminating (np.array_equal passes +0.0 == -0.0; this does not). Shape and
    dtype are asserted BEFORE comparison; a dtype or shape mismatch is a failure,
    never a coercion.
  * next state: ancestor output asserted binary integer {0,1}; candidate asserted
    the frozen boolean dtype; exact logical equality after canonicalizing the
    ANCESTOR to bool. The candidate never abandons its committed dtype to pass.
  * allclose is a DIAGNOSTIC only (tolerance frozen and named: numpy defaults
    rtol=1e-5, atol=1e-8); it never enters a verdict.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


ALLCLOSE_RTOL = 1e-5     # frozen diagnostic tolerance (numpy default), named
ALLCLOSE_ATOL = 1e-8


class ComparatorError(TypeError):
    """Shape/dtype contract violation — a failure, not a coercion."""


@dataclass(frozen=True)
class BitCompare:
    differing_cells: int
    allclose_diagnostic: bool

    @property
    def bit_exact(self) -> bool:
        return self.differing_cells == 0


def raw_bits_differ(candidate: np.ndarray, reference: np.ndarray) -> int:
    """Count float64 cells whose raw bit patterns differ. Raises on shape/dtype mismatch."""
    c = np.asarray(candidate)
    r = np.asarray(reference)
    if c.dtype != np.float64 or r.dtype != np.float64:
        raise ComparatorError(f"float64 required: candidate {c.dtype}, reference {r.dtype}")
    if c.shape != r.shape:
        raise ComparatorError(f"shape mismatch: candidate {c.shape}, reference {r.shape}")
    return int(np.count_nonzero(np.ascontiguousarray(c).view(np.uint64)
                                != np.ascontiguousarray(r).view(np.uint64)))


def compare_float64(candidate: np.ndarray, reference: np.ndarray) -> BitCompare:
    n = raw_bits_differ(candidate, reference)
    return BitCompare(differing_cells=n, allclose_diagnostic=bool(np.allclose(candidate, reference,
                                                                          rtol=ALLCLOSE_RTOL, atol=ALLCLOSE_ATOL)))


def _as_float64_scalar(x, role: str) -> np.ndarray:
    """dtype-first, noncoercive (L2 C1): a Python float is a float64 scalar and is admissible;
    a NumPy float32 (or any non-float64) scalar is REFUSED, never normalized; arrays are refused."""
    a = np.asarray(x)
    if a.shape != ():
        raise ComparatorError(f"{role}: scalar required, got shape {a.shape}")
    if a.dtype != np.float64:
        raise ComparatorError(f"{role}: float64 scalar required, got {a.dtype}")
    return a


def scalar_bits(x) -> str:
    return f"0x{int(_as_float64_scalar(x, 'scalar').view(np.uint64)):016x}"


def scalar_bits_equal(candidate, reference) -> bool:
    c = _as_float64_scalar(candidate, "candidate")
    r = _as_float64_scalar(reference, "reference")
    return int(c.view(np.uint64)) == int(r.view(np.uint64))


def state_mismatches(candidate_state: np.ndarray, ancestor_state: np.ndarray) -> int:
    """Exact logical comparison. Candidate must be bool; ancestor must be integer in {0,1}."""
    c = np.asarray(candidate_state)
    a = np.asarray(ancestor_state)
    if c.dtype != np.bool_:
        raise ComparatorError(f"candidate state must be the frozen boolean dtype, got {c.dtype}")
    if not np.issubdtype(a.dtype, np.integer):
        raise ComparatorError(f"ancestor state must be an integer dtype, got {a.dtype}")
    if not np.isin(a, (0, 1)).all():
        raise ComparatorError("ancestor state must be binary {0,1}")
    if c.shape != a.shape:
        raise ComparatorError(f"shape mismatch: candidate {c.shape}, ancestor {a.shape}")
    return int(np.count_nonzero(c != a.astype(bool)))
