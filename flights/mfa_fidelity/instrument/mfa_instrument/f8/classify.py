"""mfa_instrument/f8/classify.py — Flight 8 module M2: tail statistics, run statuses, level labels
(Contract F8 v0.8.4 §4.1–§4.2; design note v0.3 §5 M2; E1 M2 carried with the F8 record convention).

Pure functions on a run's density record rho[0..3000] (M1 convention: rho[0] at t = 0, rho[t] after tick t —
`f8.dynamics.F8RunResult.rho`, or the persisted ["Tick", "rho_global"] table). No verdict logic lives here (M4) and
no threshold is computed here (M3); θ_P, θ_T are INPUTS. Nothing consumes amplitude, slope or monotonicity.

FROZEN OBJECTS (contract §4.1–§4.2): the tail = the last 1,000 post-advance ticks, 2001..3000 inclusive; ten
NON-OVERLAPPING windows of 100 in order; S_min = min of the ten window means; **S_term = the terminal (tenth)
window's mean** — the contract's "terminal-window mean", one window, the object §4.3 prices θ_T on ("the exact
two-state transfer-matrix law of a single window's occupancy"); E1's three-window terminal mean is NOT carried
(declaration M2-1, for L2). Statuses by precedence SUSTAINED (S_min > θ_P) → NO_SUSTAINED (S_term ≤ θ_T) →
UNRESOLVED; level labels over the 20 seeds: S (n_sus ≥ 16 ∧ n_no ≤ 2), N (the reverse), M (n_sus ≥ 4 ∧ n_no ≥ 4),
else U — the frozen 16/2/4 rule, retained as the secondary-observable classifier and re-qualified under M6; nothing
about it is pre-approved (contract §4.2).

Exactness: every statistic is one integer count sum and one division on the production count grid k/2500 (counts
recovered exactly from rho and verified by reconstruction), so a run and its threshold never differ by rounding.
"""
from __future__ import annotations

import hashlib
import types
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import config as C

TAIL_START, TAIL_END = 2001, 3000                 # inclusive, post-advance ticks (M1 record convention)
TAIL_LEN = TAIL_END - TAIL_START + 1              # 1000
WINDOW = 100
N_WINDOWS = TAIL_LEN // WINDOW                    # 10, non-overlapping
TERMINAL_WINDOW = N_WINDOWS - 1                   # the tenth window (0-based 9): S_term (contract §4.2, one window)
RECORD_LEN = C.F8_TICKS + 1                       # 3001 entries: rho[0] .. rho[3000]
N_CELLS = C.F8_GRID * C.F8_GRID                   # 2500
STATUSES = ("SUSTAINED", "NO_SUSTAINED", "UNRESOLVED")
LEVEL_LABELS = ("S", "N", "M", "U")
N_RUNS, CONFIDENT_MIN, CONFIDENT_MAX_OTHER, MIXED_MIN_EACH = 20, 16, 2, 4          # the frozen 16/2/4 counts (§4.2)
COUNTS = types.MappingProxyType({"n_runs": N_RUNS, "confident_min": CONFIDENT_MIN, "confident_max_other": CONFIDENT_MAX_OTHER, "mixed_min_each": MIXED_MIN_EACH})

CLASSIFY_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("n_cells", N_CELLS), ("record_len", RECORD_LEN),
    ("tail", (TAIL_START, TAIL_END)), ("tail_len", TAIL_LEN), ("window", WINDOW), ("n_windows", N_WINDOWS),
    ("terminal_window", TERMINAL_WINDOW), ("s_term_windows", 1),
    ("counts", (("n_runs", N_RUNS), ("confident_min", CONFIDENT_MIN), ("confident_max_other", CONFIDENT_MAX_OTHER), ("mixed_min_each", MIXED_MIN_EACH))),
    ("statuses", STATUSES), ("labels", LEVEL_LABELS),
)
CLASSIFY_SHA256_LITERAL = "63598f020e77dfccfe0eb3e2d60a29412515744b65b292e90f1446f22a311d2d"
CLASSIFY_FROZEN = types.MappingProxyType(dict(CLASSIFY_DECLARATION))


def frozen_digest() -> str:
    return hashlib.sha256(repr(CLASSIFY_DECLARATION).encode()).hexdigest()


class ClassifyDomainError(ValueError):
    """Input outside the classifier's executable domain (never coerced)."""


def verify_frozen_identity() -> None:
    """Fail-closed: the digest literal; the tail/window arithmetic against M1's frozen values; the domains; the counts."""
    if frozen_digest() != CLASSIFY_SHA256_LITERAL:
        raise ClassifyDomainError("classifier declaration differs from its frozen literal digest")
    C.verify_frozen_identity()
    d = dict(CLASSIFY_DECLARATION)
    if d["tail"] != (2001, 3000) or d["tail_len"] != 1000 or d["window"] != 100 or d["n_windows"] != 10 or d["record_len"] != 3001 or d["n_cells"] != 2500:
        raise ClassifyDomainError("tail geometry differs from the contracted values")
    if TAIL_END - TAIL_START + 1 != TAIL_LEN or TAIL_LEN != WINDOW * N_WINDOWS or TAIL_END != C.F8_TICKS or TAIL_LEN != C.F8_TAIL_TICKS \
            or WINDOW != C.F8_WINDOW or N_WINDOWS != C.F8_N_WINDOWS or N_CELLS != C.F8_GRID * C.F8_GRID or RECORD_LEN != C.F8_TICKS + 1:
        raise ClassifyDomainError("tail arithmetic inconsistent with M1")
    if d["terminal_window"] != 9 or TERMINAL_WINDOW != N_WINDOWS - 1 or d["s_term_windows"] != 1:
        raise ClassifyDomainError("S_term is not the single terminal window")
    if d["statuses"] != ("SUSTAINED", "NO_SUSTAINED", "UNRESOLVED") or d["labels"] != ("S", "N", "M", "U"):
        raise ClassifyDomainError("status/label domains differ from the declaration")
    if dict(d["counts"]) != {"n_runs": 20, "confident_min": 16, "confident_max_other": 2, "mixed_min_each": 4} or dict(d["counts"]) != dict(COUNTS) \
            or (N_RUNS, CONFIDENT_MIN, CONFIDENT_MAX_OTHER, MIXED_MIN_EACH) != (20, 16, 2, 4):
        raise ClassifyDomainError("count rule values differ from the declaration or the live globals")
    live = {"tail": (TAIL_START, TAIL_END), "tail_len": TAIL_LEN, "window": WINDOW, "n_windows": N_WINDOWS, "terminal_window": TERMINAL_WINDOW,
            "record_len": RECORD_LEN, "n_cells": N_CELLS, "statuses": STATUSES, "labels": LEVEL_LABELS}
    for key, val in live.items():
        if d[key] != val or type(d[key]) is not type(val):
            raise ClassifyDomainError(f"classifier declaration field {key} differs from the live global")
    if len(C.F8_SEED_PANEL) != N_RUNS:
        raise ClassifyDomainError("frozen seed panel size differs from the run count")


def _series(rho) -> np.ndarray:
    if not isinstance(rho, np.ndarray) or rho.dtype != np.float64 or rho.ndim != 1:
        raise ClassifyDomainError("rho record must be a 1-D float64 ndarray")
    if rho.shape[0] != RECORD_LEN:
        raise ClassifyDomainError(f"rho record must have exactly {RECORD_LEN} entries (rho[0..3000]), got {rho.shape[0]}")
    if not np.isfinite(rho).all() or (rho < 0.0).any() or (rho > 1.0).any():
        raise ClassifyDomainError("rho record must be finite in [0, 1]")
    return rho


def _threshold(x, name: str) -> float:
    if isinstance(x, (bool, np.ndarray)) or not isinstance(x, (float, np.float64)):
        raise ClassifyDomainError(f"{name}: float threshold required, got {type(x).__name__}")
    v = float(x)
    if not np.isfinite(v) or v < 0.0 or v > 1.0:
        raise ClassifyDomainError(f"{name}: threshold must be finite in [0, 1]")
    return v


# ----------------------------------------------------------------------------- tail statistics
@dataclass(frozen=True)
class TailStats:
    window_means: Tuple[float, ...]     # ten, in order
    s_min: float
    s_term: float                       # the tenth window's mean


def recover_counts(rho) -> np.ndarray:
    """rho[t] is the float64 of count/N_CELLS. The integer count is recovered EXACTLY by rounding and verified by
    reconstruction; a record not on the count grid is REFUSED."""
    r = _series(rho)
    k = np.rint(r * np.float64(N_CELLS))
    if not np.array_equal(k / np.float64(N_CELLS), r):
        raise ClassifyDomainError("rho record is not on the count grid k/N_CELLS (not a production density record)")
    return k.astype(np.int64)


def window_counts(rho) -> Tuple[int, ...]:
    """The ten tail-window active-count totals (each in 0..WINDOW·N_CELLS) — the statistic M3's law is stated on."""
    verify_frozen_identity()
    k = recover_counts(rho)[TAIL_START:TAIL_END + 1]
    return tuple(int(np.sum(k[i * WINDOW:(i + 1) * WINDOW])) for i in range(N_WINDOWS))


def tail_stats(rho) -> TailStats:
    wc = window_counts(rho)
    wm = tuple(float(np.float64(c) / np.float64(WINDOW * N_CELLS)) for c in wc)
    return TailStats(wm, float(min(wm)), wm[TERMINAL_WINDOW])


# ----------------------------------------------------------------------------- run status
def run_status(rho, theta_p, theta_t) -> Tuple[str, TailStats]:
    """Precedence (§4.2): SUSTAINED iff S_min > θ_P; else NO_SUSTAINED iff S_term ≤ θ_T; else UNRESOLVED."""
    verify_frozen_identity()
    tp = _threshold(theta_p, "theta_P"); tt = _threshold(theta_t, "theta_T")
    st = tail_stats(rho)
    if st.s_min > tp:
        return "SUSTAINED", st
    if st.s_term <= tt:
        return "NO_SUSTAINED", st
    return "UNRESOLVED", st


# ----------------------------------------------------------------------------- level label
@dataclass(frozen=True)
class LevelCounts:
    n_sus: int
    n_no: int
    n_unr: int


def _status_seq(statuses: Sequence[str]) -> Tuple[str, ...]:
    if isinstance(statuses, (str, bytes)) or not hasattr(statuses, "__len__"):
        raise ClassifyDomainError("a sequence of run statuses is required")
    if any(not isinstance(s, str) or s not in STATUSES for s in statuses):
        raise ClassifyDomainError("unknown run status")
    return tuple(statuses)


def _count(x, name: str) -> int:
    if isinstance(x, bool) or not isinstance(x, (int, np.integer)):
        raise ClassifyDomainError(f"{name}: exact integral count required, got {type(x).__name__}")
    v = int(x)
    if v < 0 or v > COUNTS["n_runs"]:
        raise ClassifyDomainError(f"{name}: count {v} outside [0, {COUNTS['n_runs']}]")
    return v


def level_counts(statuses: Sequence[str]) -> LevelCounts:
    verify_frozen_identity()
    statuses = _status_seq(statuses)
    if len(statuses) != COUNTS["n_runs"]:
        raise ClassifyDomainError(f"exactly {COUNTS['n_runs']} run statuses required, got {len(statuses)}")
    return LevelCounts(sum(s == "SUSTAINED" for s in statuses), sum(s == "NO_SUSTAINED" for s in statuses), sum(s == "UNRESOLVED" for s in statuses))


def level_label(c: LevelCounts) -> str:
    """S: n_sus ≥ 16 ∧ n_no ≤ 2; N: n_no ≥ 16 ∧ n_sus ≤ 2; M: n_sus ≥ 4 ∧ n_no ≥ 4; else U (carried verbatim)."""
    verify_frozen_identity()
    ns, nn, nu = _count(c.n_sus, "n_sus"), _count(c.n_no, "n_no"), _count(c.n_unr, "n_unr")
    if ns + nn + nu != COUNTS["n_runs"]:
        raise ClassifyDomainError("counts do not sum to the run count")
    cm, co, mm = COUNTS["confident_min"], COUNTS["confident_max_other"], COUNTS["mixed_min_each"]
    if ns >= cm and nn <= co: return "S"
    if nn >= cm and ns <= co: return "N"
    if ns >= mm and nn >= mm: return "M"
    return "U"


def level_statuses_by_seed(statuses_by_seed: Dict[int, str]) -> Tuple[str, ...]:
    """Order a level's statuses by the frozen canonical panel; the key set must be exactly the panel."""
    verify_frozen_identity()
    panel = tuple(C.F8_SEED_PANEL)
    if not isinstance(statuses_by_seed, dict) or any(isinstance(k, bool) or type(k) is not int for k in statuses_by_seed) \
            or tuple(sorted(statuses_by_seed)) != tuple(sorted(panel)):
        raise ClassifyDomainError("statuses must be keyed by exactly the frozen canonical seed panel")
    return _status_seq([statuses_by_seed[s] for s in panel])


# ----------------------------------------------------------------------------- constructed controls (known answers)
CONTROL_THRESHOLDS = (0.12, 0.12)                     # 300/2500: ON the count grid, so the hoverer sits EXACTLY at both
# (id, params, boundary role, S_min EXACT (num, den), S_term EXACT (num, den), intended status) — expectations frozen
# INDEPENDENTLY of the generator; S_term is the single terminal window (contract §4.2).
CONTROL_CASES: Tuple[Tuple[str, Tuple[Tuple[str, object], ...], str, Tuple[int, int], Tuple[int, int], str], ...] = (
    ("stable_above_null", (), "clear SUSTAINED", (1, 2), (1, 2), "SUSTAINED"),
    ("extinct_decayed", (), "clear NO_SUSTAINED", (0, 1), (0, 1), "NO_SUSTAINED"),
    ("bounded_oscillation_persistent", (), "persistence without stationarity", (1, 2), (1, 2), "SUSTAINED"),
    ("slow_drift_persistent", (), "nonstationary persistence; terminal window 2375/2500", (1, 2), (19, 20), "SUSTAINED"),
    ("still_relaxing_unresolved", (), "neither criterion earned (one empty window; terminal window 1250/2500)", (0, 1), (1, 2), "UNRESOLVED"),
    ("terminal_collapse_no_sustained", (), "sustained early, empty terminal window: S_term alone decides NO_SUSTAINED", (0, 1), (0, 1), "NO_SUSTAINED"),
    ("near_null_hoverer", (("hover_count", 300),), "exactly at both thresholds: S_min == θ_P (not >), S_term == θ_T (≤)", (3, 25), (3, 25), "NO_SUSTAINED"),
)
CONTROL_CASES_SHA256_LITERAL = "60a7d6b0482fcd25b488b4a8ef13f6e517dd08d32c7b1a3f139c1da01ecf1076"


def controls_digest() -> str:
    return hashlib.sha256(repr(CONTROL_CASES).encode()).hexdigest()


def constructed_series(kind: str, theta_p, theta_t, **kw) -> Tuple[np.ndarray, str, Fraction, Fraction]:
    """Known-answer records. Returns (rho, intended_status, exact_S_min, exact_S_term). Every value lies on the count
    grid k/2500; the intended status follows from the frozen precedence applied to the exact statistics."""
    verify_frozen_identity()
    declared_params = {cid: tuple(k for k, _ in params) for cid, params, *_ in CONTROL_CASES}
    if kind not in declared_params:
        raise ClassifyDomainError(f"unknown control {kind!r}")
    if tuple(sorted(kw)) != tuple(sorted(declared_params[kind])):
        raise ClassifyDomainError(f"control {kind!r}: parameter keys {sorted(kw)} != declared {sorted(declared_params[kind])}")
    tp_f = _threshold(theta_p, "theta_P"); tt_f = _threshold(theta_t, "theta_T")
    r = np.zeros(RECORD_LEN, dtype=np.float64)
    tail = slice(TAIL_START, TAIL_END + 1)
    g = lambda k: np.float64(k) / np.float64(N_CELLS)
    w = lambda i: slice(TAIL_START + i * WINDOW, TAIL_START + (i + 1) * WINDOW)
    if kind == "stable_above_null":
        r[tail] = g(1250)
    elif kind == "extinct_decayed":
        r[:TAIL_START] = g(625); r[tail] = 0.0
    elif kind == "bounded_oscillation_persistent":
        r[tail] = np.where(np.arange(TAIL_LEN) % 2 == 0, g(1000), g(1500))
    elif kind == "slow_drift_persistent":
        for i in range(N_WINDOWS): r[w(i)] = g(1250 + 125 * i)
    elif kind == "still_relaxing_unresolved":
        r[tail] = g(1250); r[w(2)] = 0.0
    elif kind == "terminal_collapse_no_sustained":
        r[tail] = g(1250); r[w(TERMINAL_WINDOW)] = 0.0
    elif kind == "near_null_hoverer":
        hk = kw.get("hover_count")
        if isinstance(hk, bool) or not isinstance(hk, int) or not 0 <= hk <= N_CELLS:
            raise ClassifyDomainError("hover_count must be an integer count in [0, N_CELLS]")
        r[tail] = g(hk)
    else:
        raise ClassifyDomainError(f"unknown control {kind!r}")
    K = [int(round(float(x) * N_CELLS)) for x in r[tail]]
    wm = [Fraction(sum(K[i * WINDOW:(i + 1) * WINDOW]), WINDOW * N_CELLS) for i in range(N_WINDOWS)]
    s_min = min(wm); s_term = wm[TERMINAL_WINDOW]
    intended = "SUSTAINED" if float(s_min) > tp_f else ("NO_SUSTAINED" if float(s_term) <= tt_f else "UNRESOLVED")
    return r, intended, s_min, s_term


@dataclass
class ControlQualification:
    passed: bool
    results: Tuple[Tuple[str, str, str, bool], ...]      # (id, intended, observed, exact)
    missing: Tuple[str, ...]


def qualify_controls(execution_ids: Optional[Sequence[str]] = None) -> ControlQualification:
    """Every declared control exactly once; generator statistics == frozen rationals == M2's tail_stats (bit-exact);
    observed status == frozen intended status under CONTROL_THRESHOLDS."""
    verify_frozen_identity()
    if controls_digest() != CONTROL_CASES_SHA256_LITERAL:
        raise ClassifyDomainError("control case map differs from its frozen literal digest")
    declared = {cid: (dict(params), (smn, smd), (stn, std), intended) for cid, params, _, (smn, smd), (stn, std), intended in CONTROL_CASES}
    ids = tuple(c for c, *_ in CONTROL_CASES) if execution_ids is None else tuple(execution_ids)
    if len(set(ids)) != len(ids):
        raise ClassifyDomainError("duplicate control execution ids")
    for cid in ids:
        if cid not in declared:
            raise ClassifyDomainError(f"unknown control {cid!r}")
    tp, tt = CONTROL_THRESHOLDS
    results: List[Tuple[str, str, str, bool]] = []
    for cid in ids:
        params, smin_exp, sterm_exp, intended_decl = declared[cid]
        r, intended_def, s_min_gen, s_term_gen = constructed_series(cid, tp, tt, **params)
        status, st = run_status(r, tp, tt)
        fs, ft = Fraction(*smin_exp), Fraction(*sterm_exp)
        exact = (s_min_gen == fs and s_term_gen == ft and st.s_min == float(fs) and st.s_term == float(ft))
        results.append((cid, intended_decl, status, exact and intended_def == intended_decl))
    missing = tuple(c for c in declared if c not in ids)
    passed = not missing and len(ids) == len(declared) and all(ok and intended == observed for _, intended, observed, ok in results)
    return ControlQualification(passed, tuple(results), missing)
