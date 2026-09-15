"""gates/gate_b/stub.py — counted frozen-sequence Generator stub (Gate B v0.4 §3).

Installed through the construction path the instrument provides for stream control
(`DynamicsStream(generator=stub)`); the candidate is then driven through its PUBLIC
dispatch (`Dynamics.step`). The stub satisfies the Generator interface the dynamics
use — `random(size=...)` — and enforces the one-shared-draw discipline structurally:

  * validates every declared grid (float64, exact shape, finite, in [0,1)) — no coercion;
  * returns the next predeclared rand_grid as a READ-ONLY copy;
  * asserts the requested shape is exactly (grid_scale, grid_scale);
  * counts calls; raises on more than one full-grid draw per tick (`next_tick()`
    delimits ticks), on sequence exhaustion, and — via `assert_consumed()` — on
    surplus at case end.

A two-draw mutant fails by COUNT, not by statistics. Any other Generator method is
absent on purpose: a candidate reaching for one raises AttributeError.
"""
from __future__ import annotations

from typing import Sequence

import numpy as np


class StubError(RuntimeError):
    pass


class FrozenSequenceGenerator:
    def __init__(self, grids: Sequence[np.ndarray], grid_scale: int) -> None:
        self._grids = []
        for i, g in enumerate(grids):
            a = np.asarray(g)
            if a.dtype != np.float64:                     # validate, never coerce (L2 S2)
                raise StubError(f"grid {i} dtype {a.dtype} is not float64")
            if a.shape != (grid_scale, grid_scale):
                raise StubError(f"grid {i} has shape {a.shape}, expected {(grid_scale, grid_scale)}")
            if not np.isfinite(a).all():
                raise StubError(f"grid {i} contains nonfinite values")
            if (a < 0.0).any() or (a >= 1.0).any():
                raise StubError(f"grid {i} has values outside [0, 1)")
            c = np.ascontiguousarray(a).copy()
            c.setflags(write=False)
            self._grids.append(c)
        self._shape = (grid_scale, grid_scale)
        self._pos = 0
        self._draws_this_tick = 0
        self.total_draws = 0

    def random(self, size=None, **kwargs):
        if kwargs:
            raise StubError(f"unexpected Generator.random kwargs {sorted(kwargs)}")
        shape = tuple(size) if size is not None else None
        if shape != self._shape:
            raise StubError(f"draw shape {size} != {self._shape}")
        if self._draws_this_tick >= 1:
            raise StubError("second full-grid draw within one tick: shared-draw discipline broken")
        if self._pos >= len(self._grids):
            raise StubError("frozen sequence exhausted")
        g = self._grids[self._pos]
        self._pos += 1
        self._draws_this_tick += 1
        self.total_draws += 1
        out = g.copy()
        out.setflags(write=False)                          # immutable in the candidate's hands (L2 S1)
        return out

    def next_tick(self) -> None:
        self._draws_this_tick = 0

    def assert_consumed(self) -> None:
        if self._pos != len(self._grids):
            raise StubError(f"sequence not fully consumed: {self._pos}/{len(self._grids)} draws")

    @property
    def remaining(self) -> int:
        return len(self._grids) - self._pos
