"""mfa_instrument/f9/reports.py — Flight 9 module M6, part 1: the reports that are statistics of a level's
maps (Contract F9 v0.7 §5.7 rows 1 to 3; §1.3 (b), (c), (d) measured side, and (e)).

REPORTED ONLY. Nothing here is scored or tested, nothing enters B or D, and no value gates anything
(§1.3, §5.7). A missing record prevents a claim of complete reporting; it is not a failure of B or D.

INPUTS. A level's 40 seed maps as integers: counts[s, i, j] = A_i(W = 1) of seed s, the cell's number of
active tail ticks (0..1000), as the evaluator takes them. For the flicker report, the §2.11 record of the
same 40 runs at each W. For the constancy report, the comparison array ω of the index (module M1). For
TC's contrast, TC's stored base u. This module reads no run record and holds no master: that the arrays
are the runs' and the bundle's is the runner's to establish. What this module can check from the arrays
it is given, it checks; those checks are necessary conditions and authenticate nothing.

RECORDS. Each report is a dict of str, int, float, bool, None, list and dict. None stands for a quantile
that does not exist (no defined record). The flicker record's per-width dicts are keyed by the integer
W; a JSON writer turns those keys into strings, and the persisted encoding is the runner's to declare.
These dicts are components of the eventual §5.9 records, not bound job records.

NOT HERE. The design-side margin summaries of §1.3 (d) and §3.2 are index geometry and belong to the
assembly of the margin report in the second reports module, with the evaluator-derived reports
(§1.3 f, g, h), the fidelity uncertainties of §5.7 row 4 and the persistence report.

ARITHMETIC. With t_i = Σ_s counts[s, i] and D = 40 × 1,000, the seed-mean occupancy is p̄_i = t_i / D and
the 3×3 average is p̃_i = B_i / (9D), B the periodic box sum of t. Every count, band and cut is decided on
those integers. The variances are exact rationals; their floats are one correctly rounded conversion.
The flicker statistic is one correctly rounded division of integers per record.

CONTOUR CONSTANCY, DESCRIPTIVE (§5.7 row 1; §1.3 (b)). On the unsmoothed maps X_s = counts[s]/1,000 and
their mean p̄.
  Bins. Cells are ordered by ω, ties by flat index. Tie blocks (cells with equal ω) are kept whole and
  added to the current bin until it holds at least 100 cells, when a new bin starts. A final bin under
  100 cells is merged into the one before.
  With P the operation that subtracts each bin's mean from its cells and N = 10,000:
      V_within = ‖P p̄‖² / N
      V_noise  = Σ_s ‖P(X_s − p̄)‖² / (40·39·N)
  Reported: V_within, V_noise, V_within − V_noise, the number of bins and each bin's cell count and range
  of ω. If V_noise = 0 the report says so. No ratio is reported. The difference includes the variation of
  occupancy across the λ values inside each bin and is not attributed to anything. It is not evidence for
  or against the uncoupled alternative (§1.3 (b)).

MEASURED MARGINS (§5.7 row 2; §1.3 (d)). On p̃ at W = 1. Core = cells with p̃ ≥ 0.30; band = cells with
0.10 ≤ p̃ < 0.30. Reported: both counts and band/core, "undefined" if the core is empty. Beside them the
floor reference 0.0523 (π₁). No criterion refers to the margins hypothesis (§3.2).

FLICKER DISTRIBUTIONS (§5.7 row 3; §2.11; §1.3 (c)). Cells are placed in the occupancy bands [0, 0.10),
[0.10, 0.20), [0.20, 0.30), [0.30, 1] by p̄. A record is one (cell, seed) at one W, with n = 1,000/W
windows, A active windows, R₀ observed inactive segments, and the first and last window states. Its
statistic is W·(n − A)/R₀ ticks; an all-active record (R₀ = 0) is "undefined: no inactive segment"; a
record whose first or last window is inactive has a segment touching an end and is possibly censored.
Per band and W: the number of records, the median and quartiles of the statistic over the records with
a defined value (possibly censored ones included), and the counts of undefined and of possibly censored
records. Recorded, not tested.
  The record checks. Before any statistic the stacked record is refused unless every (cell, seed)
  satisfies the relations the placed parser (`dynamics.parse_run`) requires and that can be checked from
  these arrays alone. Within each width, with R_a = R₀ − 1 + first + last the number of active segments:
  0 ≤ A ≤ n; 0 ≤ R₀ ≤ n − A; R₀ = 0 iff A = n; 0 ≤ R_a ≤ A; R_a = 0 iff A = 0. Between each finer width
  W_s and coarser width W_l = k·W_s, for the pairs (1, 10), (1, 100) and (10, 100), because the three
  records describe one tick sequence: A_l ≤ A_s ≤ k·A_l; R₀,l ≤ R₀,s; R_a,l ≤ R_a,s; first_s implies
  first_l; last_s implies last_l (L2 M6 round 1, D1). The parser's relations against the run's per-tick
  active counts need the count series and are not available here. A refusal is malformed report input,
  never an outcome.
  The floor references (pre-probe declaration §6 point 3, incorporated by §2.11): with the distribution
  the report carries the W-specific floor reference, 0.0523, 0.1342 and 0.6496 for W = 1, 10 and 100.
  Each is the floor-only probability that a window of W ticks holds any activity,
  1 − (1 − π₁)(1 − a)^(W − 1) with a = 1 − exp(−η₀Δt) (Appendix A.3). It is an occupancy of windows,
  not a duration in ticks, and it enters no band, statistic or count (L2 M6 round 1, D2).

TC'S SUPPRESSION CONTRAST (§1.3 (e); pre-probe declaration R-6). Mean occupancy p̄ over the cells inside
the patch (bump ≥ 0.5) and over the cells outside it (bump ≤ 0.05), and their ratio. The sets are
terrain geometry, the same for both compositions: bump = (0.9 − u)/0.85 from TC's stored base u (the
terrain's own formula, u = 0.9 − 0.85·bump). They hold 545 and 7,843 cells, and no cell is within 4e-4 of
either threshold. The two sizes are asserted on every call as a sanity check of the geometry. They do
not authenticate the array: other arrays give sets of the same sizes (TC's u shifted by one cell does)
and are accepted. u must be TC's base from the authenticated identity bundle, and binding it is the
runner's (L2 M6 round 1, D3). R-6 states the quantity on realization runs; this module computes it on
the maps it is given. It is near-face feedback suppression and is never evidence of literal
zero-collapse (§1.4).

READINGS THIS MODULE MAKES, each for Mike's ratification (the contract's sentence is given; nothing in
the contract is changed). The numbering is the review packet's.
  1. "Also the counts at the cut 0.20" (§5.7 row 2): the same two counts with 0.20 in place of 0.30,
     that is, cells with p̃ ≥ 0.20 and cells with 0.10 ≤ p̃ < 0.20, and their ratio.
  2. "The median and quartiles" (§5.7 row 3): the 0.25, 0.50 and 0.75 quantiles with linear
     interpolation between order statistics: for n sorted values the index is q·(n − 1) = k + r/4 and
     the value x[k] + (x[k+1] − x[k])·(r/4). §5.7 names no convention; this one is the module's choice,
     and it is the kind §5.5 step 6 names for its own quantile.
  3. "Possibly censored records" (§5.7 row 3) are counted among ALL records of the band, defined or
     not; an all-active record has no inactive segment and is never censored, so the count among
     defined records is the same number.
  4. Possibly censored records with a defined value are included in the median and quartiles: §5.7
     says "all (cell, seed) records with a defined value".
  5. A band with no cell, or with no defined record, reports its counts and None for each quantile.
  6. The constancy bins use the comparison array ω as M1 stores it (rounded to 12 places): a tie block
     is a set of cells with equal stored values, and no tolerance is applied.
  7. TC's contrast and §8. §8 step 15 names six report jobs and none of them is named for (e); the
     contrast is a named component of one of them, and which is the runner's. Coverage, accepted by
     Mike on 2026-11-23 for the governance record: the runner reports it for realization runs, both TC
     arms, every level (R-6); a skeleton contrast would be an addition and is not made. This module is
     neutral to the object.
  8. Each bin's cell count is reported beside its range of ω (§5.7 row 1 names the range only).
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

import numpy as np

from . import config as C
from . import dynamics as D
from . import evaluator as E
from .config import F9ConfigError

OCC_DENOMINATOR = C.F9_N_SEEDS * C.F9_TAIL_TICKS            # p̄_i = t_i / this
BOX_DENOMINATOR = 9 * OCC_DENOMINATOR                        # p̃_i = B_i / this
BIN_MIN_CELLS = 100                                          # §5.7 row 1
CORE_MICRO = 300_000                                         # §5.7 row 2: core p̃ >= 0.30
BAND_LOW_MICRO = 100_000                                     # §5.7 row 2: band 0.10 <= p̃ < 0.30
CUT_MICRO = 200_000                                          # §5.7 row 2: "the counts at the cut 0.20"
FLOOR_REFERENCE_LITERAL = "0.0523"                           # §5.7 row 2, §5.2
FLICKER_BAND_EDGES_MICRO = (0, 100_000, 200_000, 300_000)    # §5.7 row 3: [0, .10), [.10, .20), [.20, .30), [.30, 1]
FLICKER_BAND_LABELS = ("[0, 0.10)", "[0.10, 0.20)", "[0.20, 0.30)", "[0.30, 1]")
FLICKER_FLOOR_LITERALS = ((1, "0.0523"), (10, "0.1342"), (100, "0.6496"))    # pre-probe declaration §6 point 3; Appendix A.3
FLICKER_FLOOR_MEANING = ("floor-only probability that a window of W ticks holds any activity, 1 - (1 - pi_1)(1 - a)^(W - 1); "
                         "an occupancy of windows, not a duration in ticks; enters no band, statistic or count")
QUARTILES = (1, 2, 3)                                        # quarters: 0.25, 0.50, 0.75
TC_INSIDE_BUMP_MIN = 0.5                                     # §1.3 (e)
TC_OUTSIDE_BUMP_MAX = 0.05                                   # §1.3 (e)
TC_SET_SIZES = (545, 7843)                                   # inside, outside: measured from the terrain formula and asserted on every use
KIND = "reported only; never scored"

REPORTS_DECLARATION = (
    ("module", "f9.reports"), ("version", C.F9_VERSION), ("contract", C.F9_CONTRACT_SHA256),
    ("occupancy", "p_bar = seed total / (n_seeds * tail); p_tilde = 3x3 periodic box sum / (9 * n_seeds * tail)"),
    ("bin_min_cells", BIN_MIN_CELLS), ("bins", "order by omega, ties by flat index; tie blocks whole; close a bin at >= 100 cells; merge a final bin under 100 into the one before"),
    ("v_within", "sum over bins of [sum p_bar^2 - (sum p_bar)^2 / n_b] / N"),
    ("v_noise", "sum over seeds and bins of [sum (X_s - p_bar)^2 - (sum (X_s - p_bar))^2 / n_b] / (n_seeds * (n_seeds - 1) * N)"),
    ("core_micro", CORE_MICRO), ("band_low_micro", BAND_LOW_MICRO), ("cut_micro", CUT_MICRO), ("floor_reference", FLOOR_REFERENCE_LITERAL),
    ("flicker_band_edges_micro", FLICKER_BAND_EDGES_MICRO), ("flicker_windows", C.F9_FLICKER_WINDOWS),
    ("flicker_statistic", "W * (n - A) / R0; undefined iff R0 = 0; possibly censored iff the first or the last window is inactive"),
    ("flicker_record_checks", "per width, Ra = R0 - 1 + first + last: 0 <= A <= n; 0 <= R0 <= n - A; R0 = 0 iff A = n; 0 <= Ra <= A; Ra = 0 iff A = 0. "
                              "per pair Ws < Wl = k Ws: Al <= As <= k Al; R0l <= R0s; Ral <= Ras; first_s implies first_l; last_s implies last_l"),
    ("flicker_floor_references", FLICKER_FLOOR_LITERALS), ("flicker_floor_meaning", FLICKER_FLOOR_MEANING),
    ("quartiles", "x[k] + (x[k+1] - x[k]) * (r/4); k, r = divmod(q * (n - 1), 4), q = 1, 2, 3; over defined records"),
    ("tc_sets", "bump = (0.9 - u) / 0.85; inside bump >= 0.5; outside bump <= 0.05"), ("tc_set_sizes", TC_SET_SIZES),
    ("arithmetic", "counts, bands and cuts on integers; variances exact rationals; one correctly rounded division per flicker record"),
    ("kind", KIND),
)
REPORTS_DECLARATION_SHA256_LITERAL = "169a8d62bb568388729d88f7cd80c4750fbe7cdb7955a67285fea490607aa1d9"


class F9ReportError(F9ConfigError):
    """An input outside a report's domain, or a declaration that differs from its frozen digest."""


def verify_reports_declaration() -> str:
    C.verify_frozen_identity()
    digest = C.frozen_digest(REPORTS_DECLARATION)
    if digest != REPORTS_DECLARATION_SHA256_LITERAL: raise F9ReportError("the reports declaration differs from its frozen digest")
    if (C.F9_N_SEEDS, C.F9_TAIL_TICKS, C.F9_N_CELLS, C.F9_FLICKER_WINDOWS, C.F9_THETA_MICRO) != (40, 1000, 10_000, (1, 10, 100), CUT_MICRO):
        raise F9ReportError("the panel is not the one these reports are declared for")
    if (BIN_MIN_CELLS, CORE_MICRO, BAND_LOW_MICRO, FLICKER_BAND_EDGES_MICRO) != (100, 300_000, 100_000, (0, 100_000, 200_000, 300_000)):
        raise F9ReportError("report constants differ from §5.7")
    if round(D.stationary_pi1(C.F9_ETA0), 4) != float(FLOOR_REFERENCE_LITERAL): raise F9ReportError("the floor reference is not π₁ to four places")
    if tuple(W for W, _ in FLICKER_FLOOR_LITERALS) != C.F9_FLICKER_WINDOWS or FLICKER_FLOOR_LITERALS[0][1] != FLOOR_REFERENCE_LITERAL:
        raise F9ReportError("the flicker floor references are not one per window width")
    for W, literal in FLICKER_FLOOR_LITERALS:
        if round(floor_window_occupancy(W), 4) != float(literal): raise F9ReportError(f"W = {W}: the floor reference is not the rule's to four places")
    return digest


def floor_window_occupancy(W: int) -> float:
    """The floor-only probability that a window of W ticks holds any activity (Appendix A.3): 1 − (1 − π₁)(1 − a)^(W − 1)."""
    a = 1.0 - math.exp(-C.F9_ETA0 * C.F9_DT)
    return 1.0 - (1.0 - D.stationary_pi1(C.F9_ETA0)) * (1.0 - a) ** (W - 1)


def _frac(x: Fraction) -> Dict[str, object]:
    """An exact rational with its float (one correctly rounded conversion)."""
    return {"value": float(x), "exact": f"{x.numerator}/{x.denominator}"}


def seed_totals(counts) -> Tuple[np.ndarray, np.ndarray]:
    """(checked counts as int64, t = their sum over seeds)."""
    c = E.check_counts(counts)
    return c, c.sum(axis=0)


def _at_least(values: np.ndarray, micro: int, denominator: int) -> np.ndarray:
    """values/denominator >= micro/10^6, on integers."""
    return values * C.MICRO_UNITS >= micro * denominator


# ======================= contour constancy =======================
def constancy_bins(omega) -> Tuple[np.ndarray, List[Dict[str, object]]]:
    """(bin index of every cell in flat order, the bins): the binning of §5.7 row 1."""
    om = np.asarray(omega)
    if om.dtype != np.float64 or om.shape != (C.F9_GRID, C.F9_GRID) or not np.all(np.isfinite(om)):
        raise F9ReportError("the comparison array is a finite float64 (L, L) array")
    flat = om.ravel()
    order = np.argsort(flat, kind="stable")                                   # ties by flat index
    sorted_vals = flat[order]
    starts = np.flatnonzero(np.concatenate(([True], sorted_vals[1:] != sorted_vals[:-1])))     # first position of each tie block
    ends = np.concatenate((starts[1:], [flat.size]))
    edges = [0]                                                              # positions where a bin starts
    size = 0
    for a, b in zip(starts.tolist(), ends.tolist()):
        size += b - a
        if size >= BIN_MIN_CELLS:
            edges.append(b); size = 0
    if size > 0:                                                             # a final bin under 100 cells
        if len(edges) > 1: edges[-1] = flat.size                            # merged into the one before
        else: edges.append(flat.size)                                        # there is no bin before it (cannot happen at N = 10,000)
    which = np.empty(flat.size, dtype=np.int64)
    bins = []
    for k, (a, b) in enumerate(zip(edges[:-1], edges[1:])):
        which[order[a:b]] = k
        bins.append({"cells": b - a, "omega_min": float(sorted_vals[a]), "omega_max": float(sorted_vals[b - 1])})
    return which, bins


def _within_bin_sum_of_squares(values: np.ndarray, order: np.ndarray, starts: np.ndarray, sizes: List[int]) -> Fraction:
    """Σ over bins of [Σ x² − (Σ x)²/n_b] for an integer array x in flat order: ‖P x‖², exactly."""
    v = values.ravel()[order]
    sq = np.add.reduceat(v * v, starts)
    sm = np.add.reduceat(v, starts)
    total = Fraction(int(sq.sum()))
    by_size: Dict[int, int] = {}
    for s, n in zip(sm.tolist(), sizes): by_size[n] = by_size.get(n, 0) + s * s
    for n, ss in by_size.items(): total -= Fraction(ss, n)
    return total


def constancy(counts, omega) -> Dict[str, object]:
    """§5.7 row 1 for one level's maps and one comparison array."""
    verify_reports_declaration()
    c, t = seed_totals(counts)
    which, bins = constancy_bins(omega)
    order = np.argsort(which, kind="stable")
    sizes = [b["cells"] for b in bins]
    starts = np.concatenate(([0], np.cumsum(sizes)[:-1])).astype(np.int64)
    n, N, D_ = C.F9_N_SEEDS, C.F9_N_CELLS, OCC_DENOMINATOR
    # p̄ = t/D, so ‖P p̄‖² = ‖P t‖²/D². X_s − p̄ = (n·counts_s − t)/D with D = n·tail, so ‖P(X_s − p̄)‖² = ‖P(n·counts_s − t)‖²/D².
    v_within = _within_bin_sum_of_squares(t, order, starts, sizes) / (D_ * D_ * N)
    noise = Fraction(0)
    for s in range(n): noise += _within_bin_sum_of_squares(n * c[s] - t, order, starts, sizes)
    v_noise = noise / (D_ * D_ * n * (n - 1) * N)
    return {"record": "F9ContourConstancy", "kind": KIND, "bins": bins, "n_bins": len(bins),
            "V_within": _frac(v_within), "V_noise": _frac(v_noise), "V_within_minus_V_noise": _frac(v_within - v_noise),
            "V_noise_is_zero": v_noise == 0,
            "note": "descriptive; the difference includes the variation of occupancy across the λ values inside each bin and is not "
                    "attributed to anything; not evidence for or against the uncoupled alternative; no ratio is reported",
            "declaration_sha256": REPORTS_DECLARATION_SHA256_LITERAL}


# ======================= measured margins =======================
def margins(counts) -> Dict[str, object]:
    """§5.7 row 2 for one level's maps."""
    verify_reports_declaration()
    _, t = seed_totals(counts)
    B = E.box_sum(t)
    ge10, ge20, ge30 = (_at_least(B, m, BOX_DENOMINATOR) for m in (BAND_LOW_MICRO, CUT_MICRO, CORE_MICRO))

    def pair(core_mask, band_mask):
        core, band = int(core_mask.sum()), int(band_mask.sum())
        return {"core": core, "band": band, "band_over_core": _frac(Fraction(band, core)) if core else "undefined"}

    return {"record": "F9MeasuredMargins", "kind": KIND, "on": "p̃ at W = 1",
            "cut_0.30": pair(ge30, ge10 & ~ge30), "cut_0.20": pair(ge20, ge10 & ~ge20),
            "floor_reference": {"literal": FLOOR_REFERENCE_LITERAL, "pi_1": D.stationary_pi1(C.F9_ETA0)},
            "note": "no criterion, threshold or rule refers to the margins hypothesis (§3.2)",
            "declaration_sha256": REPORTS_DECLARATION_SHA256_LITERAL}


# ======================= flicker distributions =======================
def _check_windows(windows) -> Dict[int, Dict[str, np.ndarray]]:
    """The §2.11 record of a level's 40 runs: {W: {"A", "R0": integer (n_seeds, L, L); "first", "last": bool}}, with the
    relations `dynamics.parse_run` requires of a run that these arrays alone can show: within each width, and between
    widths (the three records are of one tick sequence). Necessary conditions; not an authentication."""
    if not isinstance(windows, dict) or {(type(k), k) for k in windows} != {(int, W) for W in C.F9_FLICKER_WINDOWS}:
        raise F9ReportError(f"the flicker record is keyed by the windows {C.F9_FLICKER_WINDOWS}")
    shape = (C.F9_N_SEEDS, C.F9_GRID, C.F9_GRID)
    out = {}
    for W in C.F9_FLICKER_WINDOWS:
        rec = windows[W]
        if not isinstance(rec, dict) or {(type(k), k) for k in rec} != {(str, k) for k in ("A", "R0", "first", "last")}:
            raise F9ReportError(f"W = {W}: a record carries exactly A, R0, first and last")
        n = C.F9_TAIL_TICKS // W
        A, R0, first, last = (np.asarray(rec[k]) for k in ("A", "R0", "first", "last"))
        if A.dtype.kind not in "iu" or R0.dtype.kind not in "iu" or first.dtype != np.bool_ or last.dtype != np.bool_ \
                or any(x.shape != shape for x in (A, R0, first, last)):
            raise F9ReportError(f"W = {W}: A and R0 are integer and first and last are boolean (n_seeds, L, L) arrays")
        if bool((A < 0).any()) or bool((A > n).any()) or bool((R0 < 0).any()) or bool((R0 > n).any()):       # in the input's own type
            raise F9ReportError(f"W = {W}: a window count is outside [0, {n}]")
        A, R0 = A.astype(np.int64), R0.astype(np.int64)
        Ra = R0 - 1 + first + last                                         # active segments
        if bool((R0 > n - A).any()) or bool(((R0 == 0) != (A == n)).any()) or bool((Ra < 0).any()) or bool((Ra > A).any()) \
                or bool(((Ra == 0) != (A == 0)).any()):
            raise F9ReportError(f"W = {W}: a record contradicts itself (A, R0, first, last)")
        out[W] = {"A": A, "R0": R0, "first": first, "last": last, "Ra": Ra}
    widths = C.F9_FLICKER_WINDOWS
    for Ws in widths:
        for Wl in widths:
            if Wl <= Ws or Wl % Ws: continue
            k = Wl // Ws
            s, l = out[Ws], out[Wl]
            if bool((l["A"] > s["A"]).any()) or bool((s["A"] > k * l["A"]).any()):
                raise F9ReportError(f"W = {Ws} and {Wl}: active windows are not nested")
            if bool((l["R0"] > s["R0"]).any()) or bool((l["Ra"] > s["Ra"]).any()):
                raise F9ReportError(f"W = {Ws} and {Wl}: more segments at the coarser width")
            if bool((s["first"] & ~l["first"]).any()) or bool((s["last"] & ~l["last"]).any()):
                raise F9ReportError(f"W = {Ws} and {Wl}: an end window is inactive though the finer end window in it is active")
    return {W: {key: rec[key] for key in ("A", "R0", "first", "last")} for W, rec in out.items()}


def quartiles(sorted_values: np.ndarray) -> Optional[List[float]]:
    """The 0.25, 0.50 and 0.75 quantiles with linear interpolation between order statistics; None for no values."""
    n = int(sorted_values.shape[0])
    if n == 0: return None
    out = []
    for q in QUARTILES:
        k, r = divmod(q * (n - 1), 4)
        lo = float(sorted_values[k])
        out.append(lo if r == 0 else lo + (float(sorted_values[k + 1]) - lo) * (r / 4))
    return out


def flicker(windows) -> Dict[str, object]:
    """§5.7 row 3 for one level: per occupancy band and W, the distribution of the §2.11 statistic."""
    verify_reports_declaration()
    w = _check_windows(windows)
    t = w[1]["A"].sum(axis=0)                                              # at W = 1, A is the cell's count of active tail ticks
    band = np.zeros(t.shape, dtype=np.int64)
    for edge in FLICKER_BAND_EDGES_MICRO[1:]: band += _at_least(t, edge, OCC_DENOMINATOR)
    out_bands = []
    for b, label in enumerate(FLICKER_BAND_LABELS):
        cells = band == b
        entry = {"band": label, "cells": int(cells.sum()), "windows": {}}
        for W in C.F9_FLICKER_WINDOWS:
            n = C.F9_TAIL_TICKS // W
            A, R0 = w[W]["A"][:, cells], w[W]["R0"][:, cells]
            first, last = w[W]["first"][:, cells], w[W]["last"][:, cells]
            defined = R0 > 0
            stat = np.sort((W * (n - A[defined])) / R0[defined])           # integer / integer: one correctly rounded division each
            qs = quartiles(stat)
            entry["windows"][W] = {"records": int(A.size), "defined": int(defined.sum()), "undefined_no_inactive_segment": int((~defined).sum()),
                                   "possibly_censored": int((~first | ~last).sum()),
                                   "q25": None if qs is None else qs[0], "median": None if qs is None else qs[1], "q75": None if qs is None else qs[2]}
        out_bands.append(entry)
    floor = {"meaning": FLICKER_FLOOR_MEANING,
             "by_window": {W: {"literal": literal, "value": floor_window_occupancy(W)} for W, literal in FLICKER_FLOOR_LITERALS}}
    return {"record": "F9FlickerDistributions", "kind": KIND, "statistic": "W·(n − A)/R₀ ticks", "bands_by": "p̄ at W = 1",
            "bands": out_bands, "floor_reference": floor, "note": "recorded, not tested",
            "declaration_sha256": REPORTS_DECLARATION_SHA256_LITERAL}


# ======================= TC's suppression contrast =======================
def tc_patch_sets(u) -> Tuple[np.ndarray, np.ndarray]:
    """(inside, outside): the cells with bump ≥ 0.5 and with bump ≤ 0.05, from TC's stored base u. The size check is a
    sanity check of the geometry; it does not establish that the array is TC's u (see the module docstring)."""
    a = np.asarray(u)
    if a.dtype != np.float64 or a.shape != (C.F9_GRID, C.F9_GRID) or not np.all(np.isfinite(a)): raise F9ReportError("u is a finite float64 (L, L) array")
    bump = (0.9 - a) / 0.85
    inside, outside = bump >= TC_INSIDE_BUMP_MIN, bump <= TC_OUTSIDE_BUMP_MAX
    if (int(inside.sum()), int(outside.sum())) != TC_SET_SIZES: raise F9ReportError("the patch sets do not have TC's sizes")
    return inside, outside


def suppression_contrast(counts, u) -> Dict[str, object]:
    """§1.3 (e) for one level's maps of a TC arm."""
    verify_reports_declaration()
    _, t = seed_totals(counts)
    inside, outside = tc_patch_sets(u)
    m_in = Fraction(int(t[inside].sum()), OCC_DENOMINATOR * TC_SET_SIZES[0])
    m_out = Fraction(int(t[outside].sum()), OCC_DENOMINATOR * TC_SET_SIZES[1])
    return {"record": "F9SuppressionContrast", "kind": KIND, "terrain": "TC", "inside_cells": TC_SET_SIZES[0], "outside_cells": TC_SET_SIZES[1],
            "mean_inside": _frac(m_in), "mean_outside": _frac(m_out), "inside_over_outside": _frac(m_in / m_out) if m_out else "undefined",
            "floor_reference": {"literal": FLOOR_REFERENCE_LITERAL, "pi_1": D.stationary_pi1(C.F9_ETA0)},
            "note": "near-face feedback suppression; never evidence of literal zero-collapse (§1.4)",
            "declaration_sha256": REPORTS_DECLARATION_SHA256_LITERAL}
