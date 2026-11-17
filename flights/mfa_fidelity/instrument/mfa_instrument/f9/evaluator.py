"""mfa_instrument/f9/evaluator.py — Flight 9 module M3: the composition evaluator N-E of Contract F9
v0.7 §5.5, steps 1 to 9, for one level of one arm.

INPUT. The 40 seed maps of a level as integers: counts[s, i, j] = A_i(W = 1) of seed s, the number of
tail ticks at which cell i was active (0..1000). And, for each index Y to be compared, the registered
family of its comparison array (module M1). λ, g, κ and the terrain enter nowhere in steps 1 to 4.

THE ORDER IS THE CONTRACT'S: occupancy estimate, occupancy criterion, edge, comparison.

ARITHMETIC. Steps 1 to 4 and the distances are decided on integers. The quantile and S are IEEE
double values built from correctly rounded operations (one square root, a halving, and the written
interpolation), so they are the same on every conforming platform; they are floats, not exact reals.
The one decision made on them, S ≤ ε, nevertheless equals the decision in exact real arithmetic for
every input the lattice can produce: a term is x[k] alone (then the test is d² ≤ 16 on integers) or
an interpolation between sqrt(a)/2 and sqrt(b)/2 with integers a ≤ b ≤ 20,000 and weight r/20, and
`test_f9_m3.py` compares the float decision with an integer decision over every such (a, b, r).
The fitted level among several contours within ε is chosen by comparing float values of S; that
choice is fidelity, and the decision does not depend on it. In detail:
  Step 1-2  p̃_i ≥ θ is decided as  B_i · 10^6 ≥ θ_micro · 9 · n_seeds · tail,  with B_i the 3×3 periodic
            box sum of the seed-summed counts. This is the contract's criterion evaluated exactly, ties
            included. The float p̃ = B/(9·n_seeds·tail) is for reports only.
  Step 3    The edge and its components are `geometry.edge` (M1).
  Step 4    Cell and bond counts are integers.
  Step 6    Bond midpoints lie on the half-cell lattice. In doubled coordinates they are integer points
            of a 2L×2L torus, and the squared distance from every lattice point to the nearest bond of
            an edge is an integer, computed exactly (`distance_grid`). A distance in cells is
            sqrt(d²)/2: one correctly rounded square root and an exact halving.
            Q₀.₉₅ with linear interpolation between order statistics: for n sorted values the index is
            0.95·(n − 1) = k + r/20 with k = 19(n − 1) // 20 and r = 19(n − 1) mod 20, and the value is
            x[k] + (x[k+1] − x[k])·(r/20), in that written order (x[k] alone when r = 0).
  Step 7    Pruning. A contour level ℓ is ADMISSIBLE for an edge E when at least k + 1 bonds e of E
            (the number that must lie within ε for the first term's quantile not to exceed ε) have
            min ω < ℓ ≤ max ω over the cells whose centres are within ε + 0.5 of e, decided on integers
            (squared distance in doubled units ≤ (2ε + 1)²). A level that is not admissible has S > ε.
            The minimum is taken over the admissible levels in increasing ℓ with a strict comparison,
            so the lowest ℓ wins a tie. `brute=True` examines every level; the two modes must give the
            same decision and, whenever Δ ≤ ε, the same Δ and level (tested).
  Step 8    Δ ≤ ε compares a float built as above with ε = 2.0 (see ARITHMETIC for why that is exact).

STEP 9, THE RESAMPLES. 1,000 resamples of the 40 seed maps with replacement; steps 1 to 7 in full on
each; the same resampled map serves every index. A resample is a vector of 40 multiplicities summing to
40, so the resampled map is again an integer sum. The stream is
    numpy.random.Generator(PCG64(SeedSequence([EVALUATOR_STREAM_ROLE] + key))),
one draw `integers(0, 40, size=(1000, 40))`, with `key` a tuple of non-negative integers supplied by
the caller (the job that evaluates an arm and level, or a qualification case). EVALUATOR_STREAM_ROLE is
2^64 + 905: no master is that large (M2), so no evaluator stream is a run's stream. The stream and the
draw count are frozen; no rerun is made to move a label.
Each draw is typed: 'C' valid with Δ ≤ ε; 'A' valid with Δ > ε; 'I' invalid (it fails step 4), with its
reason. An invalid draw is never given a discrepancy. The result for an index, in this order:
n_I > 50 → not informative (unstable edge); n_C ≥ 950 → compatible; n_A ≥ 950 → adverse; otherwise
unresolved. The denominator is always 1,000.

WHAT THE EVALUATOR RETURNS, AND WHAT IT DOES NOT DO. `evaluate_level` returns the point record of the
observed map and, per index, the typed counts and the result. It applies step 9 only when the observed
level is informative and the index's family is not empty; otherwise the index's result is the
unavailable state with its cause (`no edge at θ`, `below the informative minimum`, `no eligible
contour`). It does not combine indices, levels or arms (§5.6), read a run record, hold a master, or
write a file. A runtime fault or a malformed input raises: that is an apparatus failure (§7), never an
invalid draw.
"""
from __future__ import annotations

import math
from collections import OrderedDict
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import config as C
from . import family as F
from . import geometry as G
from . import terrain as T
from .config import F9ConfigError

# ----------------------------------------------------------------------------- declarations (contract §5.5)
N_RESAMPLES = 1000                                    # step 9
INVALID_MAX = 50                                      # step 9: n_I > 50 is an unstable edge
SUPPORT_MIN = 950                                     # step 9: n_C >= 950 compatible; n_A >= 950 adverse
QUANTILE = (19, 20)                                   # step 6: 0.95 as an exact fraction
EVALUATOR_STREAM_ROLE = 2 ** 64 + 905                 # first element of every evaluator stream's seed sequence
CONTOUR_CACHE = 256                                   # contours kept per family (speed only; no result depends on it)

EVALUATOR_DECLARATION = (
    ("n_resamples", N_RESAMPLES), ("invalid_max", INVALID_MAX), ("support_min", SUPPORT_MIN), ("quantile", QUANTILE),
    ("stream_role", EVALUATOR_STREAM_ROLE), ("bit_generator", "PCG64"), ("seed_rule", "SeedSequence([role] + list(key))"),
    ("resample_draw", "integers(0, n_seeds, size=(n_resamples, n_seeds))"),
    ("criterion", "box_sum * 10^6 >= theta_micro * 9 * n_seeds * tail"),
    ("distance", "integer squared distance on the doubled torus; cells = sqrt(d2)/2"),
    ("quantile_rule", "x[k] + (x[k+1] - x[k]) * (r/20); k, r = divmod(19*(n-1), 20)"),
    ("pruning", "admissible iff at least k+1 bonds have min < level <= max over cells within eps + 0.5"),
    ("minimum", "increasing level, strict comparison"),
    ("result_order", ("unstable edge", "compatible", "adverse", "unresolved")),
)
EVALUATOR_DECLARATION_SHA256_LITERAL = "79e93ccade624ec473c7c60225183458e0ed168e13c4e23fb7dbaa6ed2d2fef7"

RESULT_COMPATIBLE, RESULT_ADVERSE, RESULT_UNRESOLVED, RESULT_NOT_INFORMATIVE = "compatible", "adverse", "unresolved", "not informative"
CAUSE_UNSTABLE, CAUSE_NO_EDGE, CAUSE_BELOW_MINIMUM, CAUSE_NO_CONTOUR = "unstable edge", "no edge at theta", "below the informative minimum", "no eligible contour"


class F9EvaluatorError(RuntimeError):
    """The evaluator was given something the contract does not define (an apparatus failure, §7)."""


def verify_evaluator_declaration() -> str:
    C.verify_frozen_identity()
    if (C.F9_N_SEEDS, C.F9_TAIL_TICKS, C.F9_THETA_MICRO, C.F9_EPSILON_MICRO, C.F9_COMPONENT_MIN_BONDS) != (40, 1000, 200_000, 2_000_000, 40):
        raise F9ConfigError("the evaluator's resolutions are not those of contract §5.5")
    if (2 * C.F9_EPSILON_MICRO) % C.MICRO_UNITS: raise F9ConfigError("epsilon is not a multiple of half a cell")
    if (N_RESAMPLES, INVALID_MAX, SUPPORT_MIN, QUANTILE) != (1000, 50, 950, (19, 20)) or EVALUATOR_STREAM_ROLE < 2 ** 64:
        raise F9ConfigError("the resampling rule is not that of contract §5.5 step 9")
    lit = EVALUATOR_DECLARATION_SHA256_LITERAL
    if len(lit) != 64 or any(ch not in "0123456789abcdef" for ch in lit):
        raise F9ConfigError("evaluator declaration digest literal is not a 64-hex sha256 (no sentinel or placeholder is accepted)")
    if C.frozen_digest(EVALUATOR_DECLARATION) != lit:
        raise F9ConfigError("evaluator declaration differs from its frozen literal digest")
    return lit


EPSILON = C.F9_EPSILON_MICRO / C.MICRO_UNITS                             # 2.0 cells, exact
_PRUNE_R2 = (2 * C.F9_EPSILON_MICRO // C.MICRO_UNITS + 1) ** 2           # (2ε + 1)² in doubled units: 25


# ======================= steps 1 and 2: the occupied region =======================
def check_counts(counts) -> np.ndarray:
    """The seed maps of one level: an integer array (n_seeds, L, L) of tail-tick counts in [0, tail]."""
    a = np.asarray(counts)
    if a.dtype.kind not in "iu" or a.shape != (C.F9_N_SEEDS, C.F9_GRID, C.F9_GRID):
        raise F9EvaluatorError("seed maps are an integer (n_seeds, L, L) array")
    if bool((a < 0).any()) or bool((a > C.F9_TAIL_TICKS).any()):              # in the input's own type, before any conversion
        raise F9EvaluatorError("a tail count is outside [0, tail]")
    return a.astype(np.int64)


def check_weights(weights) -> np.ndarray:
    """Seed multiplicities: n_seeds non-negative integers summing to n_seeds (all ones for the observed map)."""
    w = np.asarray(weights)
    if w.dtype.kind not in "iu" or w.shape != (C.F9_N_SEEDS,):
        raise F9EvaluatorError("weights are n_seeds non-negative integers summing to n_seeds")
    # Each element is bounded in the input's own type BEFORE conversion or summation (L2 M3 round 1, D1): an unsigned
    # sum can wrap to n_seeds, and a conversion can turn a large unsigned value negative. Forty values in [0, 40]
    # cannot overflow a signed 64-bit sum.
    if bool((w < 0).any()) or bool((w > C.F9_N_SEEDS).any()):
        raise F9EvaluatorError("weights are n_seeds non-negative integers summing to n_seeds")
    w = w.astype(np.int64)
    if int(w.sum()) != C.F9_N_SEEDS:
        raise F9EvaluatorError("weights are n_seeds non-negative integers summing to n_seeds")
    return w


def box_sum(total: np.ndarray) -> np.ndarray:
    """3×3 periodic box sum of an integer (L, L) array."""
    out = np.zeros_like(total)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1): out += np.roll(np.roll(total, di, axis=0), dj, axis=1)
    return out


def occupied_region(counts: np.ndarray, weights: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Steps 1 and 2 on integers: the region {p̃ ≥ θ}, ties included, and the box sum B it was decided on."""
    total = np.tensordot(weights, counts, axes=(0, 0))
    B = box_sum(total)
    return B * C.MICRO_UNITS >= C.F9_THETA_MICRO * 9 * C.F9_N_SEEDS * C.F9_TAIL_TICKS, B


def p_tilde(B: np.ndarray) -> np.ndarray:
    """The 3×3-averaged seed-mean occupancy as a float, for reports. No decision reads it."""
    return B / float(9 * C.F9_N_SEEDS * C.F9_TAIL_TICKS)


def step4(mask: np.ndarray, e: G.Edge) -> Optional[str]:
    """None when the level is informative; otherwise the reason it is not (§5.5 step 4)."""
    inside = int(mask.sum())
    if inside == 0: return "no edge at theta: the region is empty"
    if inside == C.F9_N_CELLS: return "no edge at theta: the region is full"
    if inside < C.F9_INFORMATIVE_MIN_CELLS: return "the region has under 100 cells"
    if C.F9_N_CELLS - inside < C.F9_INFORMATIVE_MIN_CELLS: return "the complement has under 100 cells"
    if e.n_bonds < C.F9_INFORMATIVE_MIN_BONDS: return "the edge has under 40 bonds"
    return None


# ======================= step 6: exact distances and the joint discrepancy =======================
def doubled(points: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Bond midpoints (cells) as integer points of the 2L×2L torus."""
    p2 = 2.0 * np.asarray(points, dtype=np.float64)
    q = np.rint(p2).astype(np.int64)
    if q.shape[0] and (np.any(q != p2) or np.any((q[:, 0] + q[:, 1]) % 2 != 1)):
        raise F9EvaluatorError("points are not bond midpoints")
    H = 2 * C.F9_GRID
    return q[:, 0] % H, q[:, 1] % H


def distance_grid(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """For every point of the 2L×2L torus, the squared distance (doubled units, an exact integer) to the nearest of
    the points (a, b). Two exact passes: the circular distance to the nearest point in the same column, then the
    minimum over columns of that squared plus the squared circular column offset."""
    H = 2 * C.F9_GRID
    if a.size == 0: raise F9EvaluatorError("an empty edge has no distance grid")
    src = np.zeros((H, H), dtype=bool); src[a, b] = True
    idx = np.arange(3 * H, dtype=np.int64)[:, None]
    s3 = np.tile(src, (3, 1))
    far = 8 * H
    last = np.maximum.accumulate(np.where(s3, idx, -far), axis=0)
    nxt = np.minimum.accumulate(np.where(s3, idx, far)[::-1], axis=0)[::-1]
    g = np.minimum(idx - last, nxt - idx)[H:2 * H]
    has = src.any(axis=0)
    g2 = np.where(has[None, :], g * g, np.int64(10 ** 9))
    d2 = np.full((H, H), np.int64(10 ** 9))
    for delta in range(-(H // 2), H // 2 + 1):
        np.minimum(d2, np.roll(g2, delta, axis=1) + delta * delta, out=d2)
    return d2


def q95(sorted_values: np.ndarray) -> float:
    """The 0.95 quantile with linear interpolation between order statistics, by the rule in the module docstring."""
    n = int(sorted_values.shape[0])
    if n == 0: raise F9EvaluatorError("no quantile of an empty set")
    k, r = divmod(QUANTILE[0] * (n - 1), QUANTILE[1])
    lo = float(sorted_values[k])
    if r == 0: return lo
    return lo + (float(sorted_values[k + 1]) - lo) * (r / QUANTILE[1])


def _cells(d2: np.ndarray) -> np.ndarray:
    return np.sqrt(d2.astype(np.float64)) / 2.0


class _Traced:
    """An edge with what the comparison needs: its doubled points, its distance grid, and its resolved components."""

    def __init__(self, e: G.Edge):
        self.edge = e
        self.a, self.b = doubled(e.points)
        self.grid = distance_grid(self.a, self.b)
        sizes = e.component_sizes()
        self.sizes = sizes
        self.resolved = tuple(k for k, n in enumerate(sizes) if n >= C.F9_COMPONENT_MIN_BONDS)


def _side(mine: _Traced, other: _Traced, bound: Optional[float]):
    """One side's terms: the global quantile of the distances from `mine`'s bonds to `other`, then one per resolved
    component of `mine`. Stops early (returns None) as soon as a term is not below `bound`."""
    d = _cells(other.grid[mine.a, mine.b])
    g = q95(np.sort(d))
    if bound is not None and not g < bound: return None
    comps = []
    for k in mine.resolved:
        v = q95(np.sort(d[mine.edge.component == k]))
        if bound is not None and not v < bound: return None
        comps.append((int(mine.sizes[k]), v))
    return g, comps


def joint_discrepancy(E: _Traced, Cn: _Traced, bound: Optional[float] = None) -> Optional[Dict[str, object]]:
    """S(E, C) of step 6 with its terms. With `bound`, returns None as soon as some term is not below it (S is the
    maximum of the terms, so S would not be below it either)."""
    left = _side(E, Cn, bound)
    if left is None: return None
    right = _side(Cn, E, bound)
    if right is None: return None
    terms = [left[0], right[0]] + [v for _, v in left[1]] + [v for _, v in right[1]]
    return {"S": max(terms), "global_E": left[0], "global_C": right[0], "components_E": left[1], "components_C": right[1],
            "resolved_E": len(left[1]), "resolved_C": len(right[1]),
            "no_resolved_component_checked_on_E": not left[1], "no_resolved_component_checked_on_C": not right[1]}


# ======================= step 5 and 7: a family prepared for comparison =======================
class IndexFamily:
    """The registered family of one index's comparison array, with the per-bond level intervals the pruning uses and
    a bounded cache of traced contours. `terrain` and `composition` label the fitted level (M1's `level_label`).

    On a same-family terrain the two indices share one comparison array: `shared_with(composition)` gives the other
    index over the same contours (they are traced once), with its own label."""

    def __init__(self, omega: np.ndarray, terrain: str, composition: str):
        if terrain not in C.F9_TERRAINS or composition not in C.F9_COMPOSITIONS:
            raise F9ConfigError(f"not a declared terrain and composition: {terrain!r}.{composition!r}")
        self.family = F.Family(omega)
        self.terrain, self.composition = terrain, composition
        self.levels = np.array(self.family.levels, dtype=np.float64)
        self._cache: "OrderedDict[int, _Traced]" = OrderedDict()
        self._lo, self._hi = self._intervals(self.family.omega) if len(self.levels) else (None, None)
        self.contours_id = id(self._cache)                    # equal for indices that share contours

    def shared_with(self, composition: str) -> "IndexFamily":
        if composition not in C.F9_COMPOSITIONS: raise F9ConfigError(f"not a declared composition: {composition!r}")
        other = object.__new__(IndexFamily)
        other.__dict__.update(self.__dict__)
        other.composition = composition
        return other

    def __len__(self) -> int:
        return int(self.levels.shape[0])

    @staticmethod
    def _intervals(om: np.ndarray):
        """lo[t, i, j], hi[t, i, j]: the least and greatest ω over the cells whose centres are within ε + 0.5 of the
        bond of type t at (i, j) (t = 0: midpoint (i + 0.5, j); t = 1: midpoint (i, j + 0.5))."""
        L = C.F9_GRID
        lo = np.full((2, L, L), np.inf); hi = np.full((2, L, L), -np.inf)
        reach = int(math.isqrt(_PRUNE_R2)) // 2 + 2
        for k in range(-reach, reach + 1):
            for m in range(-reach, reach + 1):
                shifted = None
                for t, (di, dj) in enumerate(((2 * k - 1, 2 * m), (2 * k, 2 * m - 1))):   # cell (i+k, j+m) minus the bond, doubled
                    if di * di + dj * dj <= _PRUNE_R2:
                        if shifted is None: shifted = np.roll(np.roll(om, -k, axis=0), -m, axis=1)   # shifted[i, j] = ω[i+k, j+m]
                        np.minimum(lo[t], shifted, out=lo[t]); np.maximum(hi[t], shifted, out=hi[t])
        return lo, hi

    def admissible(self, E: _Traced) -> np.ndarray:
        """Indices (increasing) of the levels a contour within ε of E's first term can have (step 7)."""
        t = (E.a % 2 == 0).astype(np.int64)                     # a odd: an axis-0 bond (type 0); a even: type 1
        i = np.where(t == 0, (E.a - 1) // 2, E.a // 2); j = np.where(t == 0, E.b // 2, (E.b - 1) // 2)
        lo = np.sort(self._lo[t, i, j]); hi = np.sort(self._hi[t, i, j])
        need = (QUANTILE[0] * (E.a.size - 1)) // QUANTILE[1] + 1
        cover = np.searchsorted(lo, self.levels, side="left") - np.searchsorted(hi, self.levels, side="left")
        return np.flatnonzero(cover >= need)

    def contour(self, k: int) -> _Traced:
        got = self._cache.get(k)
        if got is None:
            got = _Traced(self.family.contour(float(self.levels[k])))
            self._cache[k] = got
            if len(self._cache) > CONTOUR_CACHE: self._cache.popitem(last=False)
        else:
            self._cache.move_to_end(k)
        return got

    def label(self, k: int) -> float:
        return T.level_label(self.terrain, self.composition, float(self.levels[k]))


def fit(E: _Traced, fam: IndexFamily, brute: bool = False) -> Dict[str, object]:
    """Step 7 for one edge and one family: Δ = the least S over the family, decided exactly."""
    if len(fam) == 0:
        return {"status": CAUSE_NO_CONTOUR, "family_size": 0, "examined": 0, "within": None, "delta": None}
    cand = np.arange(len(fam)) if brute else fam.admissible(E)
    best = None; best_k = -1
    for k in cand:
        k = int(k)
        s = joint_discrepancy(E, fam.contour(k), None if best is None else best["S"])
        if s is not None: best, best_k = s, k                 # strictly below the best so far: the lowest level keeps a tie
    out = {"family_size": len(fam), "examined": int(len(cand)), "pruned": not brute}
    if best is None:
        out.update(status="no contour examined", within=False, delta=None)
        return out
    within = bool(best["S"] <= EPSILON)
    out.update(within=within, level_index=best_k, level=float(fam.levels[best_k]), terms=best)
    if within:
        out.update(status="within epsilon", delta=best["S"])
    else:
        out.update(status="no registered contour within epsilon", delta=None, least_S_examined=best["S"],
                   note="least S among the contours examined; descriptive; need not be the family minimum")
    return out


def evaluate_map(counts: np.ndarray, weights: np.ndarray, families: Dict[str, IndexFamily], brute: bool = False) -> Dict[str, object]:
    """Steps 1 to 7 on one map (the seed maps with the given multiplicities), for every index in `families`."""
    mask, B = occupied_region(counts, weights)
    e = G.edge(mask)
    reason = step4(mask, e)
    out = {"region_cells": int(mask.sum()), "bonds": e.n_bonds, "component_sizes": list(e.component_sizes()),
           "informative": reason is None, "reason": reason, "indices": {}}
    if reason is not None: return out
    E = _Traced(e)
    done: Dict[int, Dict[str, object]] = {}
    for name, fam in families.items():
        if fam.contours_id not in done: done[fam.contours_id] = fit(E, fam, brute)   # shared contours are fitted once
        entry = dict(done[fam.contours_id])
        if entry.get("within"): entry["lambda_star"] = fam.label(entry["level_index"])   # the index's own label; fidelity only
        out["indices"][name] = entry
    return out


# ======================= step 9 =======================
def stream_key(key) -> Tuple[int, ...]:
    if not isinstance(key, tuple) or not key or not all(type(k) is int and 0 <= k < 2 ** 64 for k in key):
        raise F9EvaluatorError("an evaluator stream key is a non-empty tuple of integers in [0, 2^64)")
    return key


def resample_multiplicities(key) -> np.ndarray:
    """The 1,000 resamples of the declared stream for `key`, as (1000, n_seeds) multiplicities."""
    gen = np.random.Generator(np.random.PCG64(np.random.SeedSequence([EVALUATOR_STREAM_ROLE] + list(stream_key(key)))))
    idx = gen.integers(0, C.F9_N_SEEDS, size=(N_RESAMPLES, C.F9_N_SEEDS))
    out = np.zeros((N_RESAMPLES, C.F9_N_SEEDS), dtype=np.int64)
    np.add.at(out, (np.arange(N_RESAMPLES)[:, None], idx), 1)
    return out


def result_from_counts(n_C: int, n_A: int, n_I: int) -> Tuple[str, Optional[str]]:
    """The table of step 9, in its order. The denominator is always N_RESAMPLES."""
    if not all(type(n) is int and n >= 0 for n in (n_C, n_A, n_I)) or n_C + n_A + n_I != N_RESAMPLES:
        raise F9EvaluatorError("the typed counts do not sum to the number of resamples")
    if n_I > INVALID_MAX: return RESULT_NOT_INFORMATIVE, CAUSE_UNSTABLE
    if n_C >= SUPPORT_MIN: return RESULT_COMPATIBLE, None
    if n_A >= SUPPORT_MIN: return RESULT_ADVERSE, None
    return RESULT_UNRESOLVED, None


def _check_families(families) -> Dict[str, IndexFamily]:
    if not isinstance(families, dict) or not families or not all(isinstance(k, str) and isinstance(v, IndexFamily) for k, v in families.items()):
        raise F9EvaluatorError("families is a non-empty mapping from an index name to an IndexFamily")
    return families


def evaluate_level(counts, families: Dict[str, IndexFamily], key, brute: bool = False, multiplicities: Optional[np.ndarray] = None) -> Dict[str, object]:
    """§5.5 for one level: the observed map's record, and per index the typed resample counts and the result.

    `multiplicities` replaces the declared stream's resamples (a (1000, n_seeds) integer array of valid weight rows).
    It exists for the qualification's constructed resample sets (§6.1); a record made with it says so and is not a
    record of the declared rule."""
    verify_evaluator_declaration()
    counts = check_counts(counts); families = _check_families(families); key = stream_key(key)
    mult = None
    if multiplicities is not None:                            # checked before anything is computed, whether or not it will be used
        given = np.asarray(multiplicities)
        if given.shape != (N_RESAMPLES, C.F9_N_SEEDS): raise F9EvaluatorError("constructed resamples are (n_resamples, n_seeds)")
        mult = np.stack([check_weights(row) for row in given])
    ones = np.ones(C.F9_N_SEEDS, dtype=np.int64)
    point = evaluate_map(counts, ones, families, brute)
    record: Dict[str, object] = {"stream_key": list(key), "stream_role": EVALUATOR_STREAM_ROLE, "n_resamples": N_RESAMPLES,
                                 "declared_stream": multiplicities is None, "point": point, "indices": {}, "resampled": False}
    applicable = {}
    for name, fam in families.items():
        if not point["informative"]:
            cause = CAUSE_NO_EDGE if point["reason"].startswith("no edge") else CAUSE_BELOW_MINIMUM
            record["indices"][name] = {"result": RESULT_NOT_INFORMATIVE, "cause": cause, "resampled": False}
        elif len(fam) == 0:
            record["indices"][name] = {"result": RESULT_NOT_INFORMATIVE, "cause": CAUSE_NO_CONTOUR, "resampled": False}
        else:
            applicable[name] = fam
    if not applicable: return record
    if mult is None: mult = resample_multiplicities(key)
    types = {name: np.empty(N_RESAMPLES, dtype="U1") for name in applicable}
    delta = {name: np.full(N_RESAMPLES, np.nan) for name in applicable}
    level_index = {name: np.full(N_RESAMPLES, -1, dtype=np.int64) for name in applicable}
    reasons: Dict[str, int] = {}
    for r in range(N_RESAMPLES):
        draw = evaluate_map(counts, mult[r], applicable, brute)
        if not draw["informative"]:
            reasons[draw["reason"]] = reasons.get(draw["reason"], 0) + 1
            for name in applicable: types[name][r] = "I"
            continue
        for name in applicable:
            f = draw["indices"][name]
            if f["within"]:
                types[name][r] = "C"; delta[name][r] = f["delta"]; level_index[name][r] = f["level_index"]
            else:
                types[name][r] = "A"
    record["resampled"] = True
    record["invalid_reasons"] = dict(sorted(reasons.items()))
    for name, fam in applicable.items():
        n_C = int((types[name] == "C").sum()); n_A = int((types[name] == "A").sum()); n_I = int((types[name] == "I").sum())
        result, cause = result_from_counts(n_C, n_A, n_I)
        entry = {"result": result, "cause": cause, "resampled": True, "n_C": n_C, "n_A": n_A, "n_I": n_I,
                 "types": types[name], "delta": delta[name], "level_index": level_index[name]}
        if n_C:
            labels = [fam.label(int(k)) for k in level_index[name][types[name] == "C"]]
            entry["lambda_star_range"] = [min(labels), max(labels)]
        else:
            entry["lambda_star_range"] = None                 # "no compatible resample"
        record["indices"][name] = entry
    return record


def index_families(arrays: Dict[str, np.ndarray], terrain: str) -> Dict[str, IndexFamily]:
    """Both indices' families for a terrain, from the arrays of an identity bundle (M1). On a same-family terrain the
    two share one comparison array; on TB each has its own; on T0 the index is constant and both families are empty.
    That the arrays are the canonical bundle's is the caller's to establish."""
    from . import identities as I
    if terrain not in C.F9_TERRAINS: raise F9ConfigError(f"not a declared terrain: {terrain!r}")
    try:
        if terrain == "T0":
            v, u, r = (arrays[f"bases/T0.{b}.f64"] for b in ("v", "u", "r"))
            return {comp: IndexFamily(np.ascontiguousarray(np.round(T.compose(comp, v, u, r), C.F9_ROUND_PLACES)), terrain, comp) for comp in C.F9_COMPOSITIONS}
        if C.same_family_latent(terrain) is not None:
            first = IndexFamily(arrays[f"omega/{I.omega_key(terrain, 'P')}.f64"], terrain, "P")
            return {"P": first, "H": first.shared_with("H")}
        return {comp: IndexFamily(arrays[f"omega/{I.omega_key(terrain, comp)}.f64"], terrain, comp) for comp in C.F9_COMPOSITIONS}
    except KeyError:
        raise F9EvaluatorError("the identity bundle's arrays do not carry this terrain")


def arm_level_key(master: int, terrain: str, composition: str, level_micro: int) -> Tuple[int, ...]:
    """The evaluator stream key of an arm and level of a panel: (master, terrain code, composition code, κ in
    micro-units). The arm is the one whose realization runs are evaluated; both indices use this one stream."""
    from . import streams as R
    R.check_run_identity(master, terrain, composition, "realization", "stationary_floor", level_micro, 0)
    return (master, dict(R.TERRAIN_CODES)[terrain], dict(R.COMPOSITION_CODES)[composition], level_micro)
