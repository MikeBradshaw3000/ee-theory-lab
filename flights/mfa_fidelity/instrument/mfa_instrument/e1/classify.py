"""mfa_instrument/e1/classify.py — E1 stage-1 module M2: tail statistics, run statuses, level
labels (Contract E1 §4.1 v0.3, §4.3 v0.3, v0.5 A; design note §2 M2).

Pure functions on a run's pre-update rho(t) series (ticks 0..2999, from the persisted rho_global
tick table). No verdict logic lives here (M4) and no threshold is computed here (M3); thresholds
θ_P, θ_T are INPUTS. Nothing consumes amplitude, slope, monotonicity, or intervals — the bootstrap
reports descriptive intervals only, by the count rules' own definition.

FROZEN OBJECTS: the tail = ticks 2000..2999 inclusive (1000 ticks); ten NON-OVERLAPPING windows
of 100; S_min = min of the ten window means; S_term = mean over the terminal 300 ticks (windows
8-10); statuses by precedence SUSTAINED (S_min > θ_P) → NO SUSTAINED ACTIVATION (S_term ≤ θ_T)
→ UNRESOLVED; level labels by counts over the 20 paired runs: S (n_sus ≥ 16 ∧ n_no ≤ 2),
N (n_no ≥ 16 ∧ n_sus ≤ 2), M (n_sus ≥ 4 ∧ n_no ≥ 4), U otherwise. The 16/2/4 counts are
[PROPOSED] — carried here as the executable definition, ratifiable only via the M6 audit.

Exactness: every statistic is one integer count sum and one division on the production count grid
k/2500; the constructed controls live on that grid and their frozen rational statistics are known independently.
"""
from __future__ import annotations

import hashlib
import types
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .config import E1_SEED_PANEL

TAIL_START, TAIL_END = 2000, 2999                 # inclusive
TAIL_LEN = TAIL_END - TAIL_START + 1              # 1000
WINDOW = 100
N_WINDOWS = TAIL_LEN // WINDOW                    # 10, non-overlapping
TERMINAL_WINDOWS = (7, 8, 9)                      # windows 8-10 (1-based) = the terminal 300 ticks
RUN_LEN = 3000
STATUSES = ("SUSTAINED", "NO_SUSTAINED", "UNRESOLVED")
LEVEL_LABELS = ("S", "N", "M", "U")
N_RUNS, CONFIDENT_MIN, CONFIDENT_MAX_OTHER, MIXED_MIN_EACH = 20, 16, 2, 4          # [PROPOSED] 16/2/4 counts
COUNTS = types.MappingProxyType({"n_runs": N_RUNS, "confident_min": CONFIDENT_MIN, "confident_max_other": CONFIDENT_MAX_OTHER, "mixed_min_each": MIXED_MIN_EACH})

# THE CLASSIFIER DECLARATION — deeply immutable (tuples only), bound to an independent literal digest,
# verified by `verify_frozen_identity()` which every public classification entry point invokes (L2 M2-1).
CLASSIFY_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("n_cells", 2500),
    ("tail", (TAIL_START, TAIL_END)), ("tail_len", TAIL_LEN), ("window", WINDOW), ("n_windows", N_WINDOWS),
    ("terminal_windows", TERMINAL_WINDOWS), ("run_len", RUN_LEN),
    ("counts", (("n_runs", N_RUNS), ("confident_min", CONFIDENT_MIN), ("confident_max_other", CONFIDENT_MAX_OTHER), ("mixed_min_each", MIXED_MIN_EACH))),
    ("statuses", STATUSES), ("labels", LEVEL_LABELS),
)
CLASSIFY_SHA256_LITERAL = "1f537198ae235de7e20a27c3a52dfed0663311ac6505d1c6895b97e5c197252c"   # established 2026-09-17 (amended: n_cells; count-grid arithmetic)
CLASSIFY_FROZEN = types.MappingProxyType(dict(CLASSIFY_DECLARATION))      # read-only view; the tuple is the object


def frozen_digest() -> str:
    return hashlib.sha256(repr(CLASSIFY_DECLARATION).encode()).hexdigest()


class ClassifyDomainError(ValueError):
    """Input outside the classifier's executable domain (never coerced)."""


def verify_frozen_identity() -> None:
    """Fail-closed: the digest literal; the tail/window arithmetic; the terminal indices; the domains;
    the [PROPOSED] counts — each recomputed from the module globals and compared to the declaration."""
    if frozen_digest() != CLASSIFY_SHA256_LITERAL:
        raise ClassifyDomainError("classifier declaration differs from its frozen literal digest")
    d = dict(CLASSIFY_DECLARATION)
    if d["tail"] != (2000, 2999) or d["tail_len"] != 1000 or d["window"] != 100 or d["n_windows"] != 10 or d["run_len"] != 3000:
        raise ClassifyDomainError("tail geometry differs from the contracted values")
    if TAIL_END - TAIL_START + 1 != TAIL_LEN or TAIL_LEN != WINDOW * N_WINDOWS or TAIL_END != RUN_LEN - 1:
        raise ClassifyDomainError("tail arithmetic inconsistent")
    if d["terminal_windows"] != (7, 8, 9) or TERMINAL_WINDOWS != (N_WINDOWS - 3, N_WINDOWS - 2, N_WINDOWS - 1):
        raise ClassifyDomainError("terminal windows are not windows 8-10")
    if d["statuses"] != ("SUSTAINED", "NO_SUSTAINED", "UNRESOLVED") or d["labels"] != ("S", "N", "M", "U"):
        raise ClassifyDomainError("status/label domains differ from the declaration")
    if dict(d["counts"]) != {"n_runs": 20, "confident_min": 16, "confident_max_other": 2, "mixed_min_each": 4} or dict(d["counts"]) != dict(COUNTS):
        raise ClassifyDomainError("count rule values differ from the declaration")
    # EVERY declaration entry equals the live execution object the classifier uses (L2 r2 M2-1)
    live = {"tail": (TAIL_START, TAIL_END), "tail_len": TAIL_LEN, "window": WINDOW, "n_windows": N_WINDOWS, "terminal_windows": TERMINAL_WINDOWS,
            "run_len": RUN_LEN, "statuses": STATUSES, "labels": LEVEL_LABELS}
    for key, val in live.items():
        if d[key] != val or type(d[key]) is not type(val):
            raise ClassifyDomainError(f"classifier declaration field {key} differs from the live global")
    from .config import E1_GRID, verify_frozen_identity as _m1_identity
    _m1_identity()
    if N_CELLS != E1_GRID * E1_GRID or d["n_cells"] != N_CELLS:
        raise ClassifyDomainError("N_CELLS differs from the M1 grid or the declaration")


def _series(rho) -> np.ndarray:
    if not isinstance(rho, np.ndarray) or rho.dtype != np.float64 or rho.ndim != 1:
        raise ClassifyDomainError("rho series must be a 1-D float64 ndarray")
    if rho.shape[0] != RUN_LEN:
        raise ClassifyDomainError(f"rho series must have exactly {RUN_LEN} ticks, got {rho.shape[0]}")
    if not np.isfinite(rho).all() or (rho < 0.0).any() or (rho > 1.0).any():
        raise ClassifyDomainError("rho series must be finite in [0, 1]")
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
    s_term: float


N_CELLS = 2500                                    # bound to the M1 grid by verify_frozen_identity


def recover_counts(rho) -> np.ndarray:
    """Production rho(t) is the float64 of count/N_CELLS (rho_global = mean(is_active)). The integer
    count is recovered EXACTLY by rounding rho·N (the float error is far below 1/2) and the recovery
    is verified by reconstruction: a series not on the count grid is REFUSED. Every tail statistic is
    then one integer sum and one division — bit-identical to the exact null law's grid values and to
    the MC path (L2 r2 M3-5), so a run and its threshold never differ by rounding."""
    r = _series(rho)
    k = np.rint(r * np.float64(N_CELLS))
    if not np.array_equal(k / np.float64(N_CELLS), r):
        raise ClassifyDomainError("rho series is not on the count grid k/N_CELLS (not a production density series)")
    return k.astype(np.int64)


def tail_stats(rho) -> TailStats:
    verify_frozen_identity()
    k = recover_counts(rho)[TAIL_START:TAIL_END + 1]
    wm = tuple(float(np.float64(int(np.sum(k[i * WINDOW:(i + 1) * WINDOW]))) / np.float64(WINDOW * N_CELLS)) for i in range(N_WINDOWS))
    s_min = float(min(wm))
    term = k[TERMINAL_WINDOWS[0] * WINDOW:(TERMINAL_WINDOWS[-1] + 1) * WINDOW]
    s_term = float(np.float64(int(np.sum(term))) / np.float64(len(TERMINAL_WINDOWS) * WINDOW * N_CELLS))
    return TailStats(wm, s_min, s_term)


# ----------------------------------------------------------------------------- run status
def run_status(rho, theta_p, theta_t) -> Tuple[str, TailStats]:
    """Precedence: SUSTAINED iff S_min > θ_P; else NO_SUSTAINED iff S_term ≤ θ_T; else UNRESOLVED."""
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
    """S: n_sus ≥ 16 ∧ n_no ≤ 2; N: n_no ≥ 16 ∧ n_sus ≤ 2; M: n_sus ≥ 4 ∧ n_no ≥ 4; else U.
    The rules are mutually exclusive by arithmetic (S and N cannot both hold with 20 runs; S/N
    exclude M by the ≤ 2 clause); precedence is stated anyway so the function is total by text."""
    verify_frozen_identity()
    ns, nn, nu = _count(c.n_sus, "n_sus"), _count(c.n_no, "n_no"), _count(c.n_unr, "n_unr")
    if ns + nn + nu != COUNTS["n_runs"]:
        raise ClassifyDomainError("counts do not sum to the run count")
    c = LevelCounts(ns, nn, nu)
    cm, co, mm = COUNTS["confident_min"], COUNTS["confident_max_other"], COUNTS["mixed_min_each"]
    if c.n_sus >= cm and c.n_no <= co: return "S"
    if c.n_no >= cm and c.n_sus <= co: return "N"
    if c.n_sus >= mm and c.n_no >= mm: return "M"
    return "U"


# ----------------------------------------------------------------------------- descriptive bootstrap
def seed_bootstrap_intervals(statuses_by_level: Dict[str, Dict[int, str]], analysis_seed: int, n_resamples: int = 10_000) -> Dict[str, Dict[str, Tuple[float, float]]]:
    """DESCRIPTIVE per-level MARGINAL intervals computed from ONE shared paired resampling plan (L2 M2-4
    wording): statuses are keyed by the frozen seed identity (seed -> status) and every level must carry
    exactly the frozen panel; one resample-index matrix over the panel is reused at every level; each
    level's count fractions are then collapsed to marginal 2.5/97.5 percentiles (Hyndman–Fan type 7).
    The returned intervals encode NO joint threshold-location uncertainty; downstream code must not
    infer one from them. No classification consumes these intervals (Contract v0.2 §4.3, item 6)."""
    verify_frozen_identity()
    if isinstance(analysis_seed, bool) or not isinstance(analysis_seed, (int, np.integer)) or int(analysis_seed) < 0:
        raise ClassifyDomainError("analysis_seed must be a non-negative integer")
    if isinstance(n_resamples, bool) or not isinstance(n_resamples, (int, np.integer)) or int(n_resamples) < 1:
        raise ClassifyDomainError("n_resamples must be a positive integer")
    if not isinstance(statuses_by_level, dict) or not statuses_by_level:
        raise ClassifyDomainError("statuses_by_level must be a nonempty mapping level_id -> {seed: status}")
    panel = tuple(E1_SEED_PANEL); n = len(panel)
    if n != COUNTS["n_runs"]:
        raise ClassifyDomainError("frozen seed panel size differs from the run count")
    ordered: Dict[str, Tuple[str, ...]] = {}
    for lv, by_seed in statuses_by_level.items():
        if not isinstance(by_seed, dict) or any(isinstance(k, bool) or type(k) is not int for k in by_seed) \
                or tuple(sorted(by_seed)) != tuple(sorted(panel)) or len(by_seed) != n:
            raise ClassifyDomainError(f"level {lv}: statuses must be keyed by exactly the frozen seed panel")
        ordered[lv] = _status_seq([by_seed[s] for s in panel])          # one common order: the panel's
    g = np.random.default_rng(np.random.SeedSequence([int(analysis_seed), 0xE1B007]))
    idx = g.integers(0, n, size=(int(n_resamples), n))
    out: Dict[str, Dict[str, Tuple[float, float]]] = {}
    for lv, seq in ordered.items():
        arr = np.array([STATUSES.index(s) for s in seq])
        res = arr[idx]
        out[lv] = {name: (float(np.percentile(np.mean(res == code, axis=1), 2.5, method="linear")),
                          float(np.percentile(np.mean(res == code, axis=1), 97.5, method="linear")))
                   for name, code in (("sustained", 0), ("no_sustained", 1), ("unresolved", 2))}
    return out


# ----------------------------------------------------------------------------- constructed controls
# THE CONTROL CASE MAP (L2 M2-5): immutable, digest-bound; ids, parameters, boundary role, the exact
# construction of S_min/S_term, and the intended status under the declared control thresholds.
CONTROL_THRESHOLDS = (0.12, 0.12)                     # 300/2500: ON the count grid, so the hoverer sits EXACTLY at both
# (id, params (exact key set), boundary role, S_min EXACT (num, den), S_term EXACT (num, den), intended status)
# The numeric expectations are frozen INDEPENDENTLY of the generator (L2 r2 M2-3): changing a control's
# construction cannot move its expected answer. Thresholds for qualification are CONTROL_THRESHOLDS.
CONTROL_CASES: Tuple[Tuple[str, Tuple[Tuple[str, object], ...], str, Tuple[int, int], Tuple[int, int], str], ...] = (
    ("stable_above_null", (), "clear SUSTAINED", (1, 2), (1, 2), "SUSTAINED"),
    ("extinct_decayed", (), "clear NO_SUSTAINED", (0, 1), (0, 1), "NO_SUSTAINED"),
    ("bounded_oscillation_persistent", (), "persistence without stationarity", (1, 2), (1, 2), "SUSTAINED"),
    ("slow_drift_persistent", (), "nonstationary persistence", (1, 2), (9, 10), "SUSTAINED"),
    ("still_relaxing_unresolved", (), "neither criterion earned", (0, 1), (1, 2), "UNRESOLVED"),
    ("near_null_hoverer", (("hover_count", 300),), "exactly at both thresholds: S_min == θ_P (not >), S_term == θ_T (≤)", (3, 25), (3, 25), "NO_SUSTAINED"),
)
CONTROL_CASES_SHA256_LITERAL = "b3a21386cfd35b983865d07074f34929c7650777ff3da26cca8649d54c107192"   # established 2026-09-17 (amended: count-grid controls, frozen rationals)


def controls_digest() -> str:
    return hashlib.sha256(repr(CONTROL_CASES).encode()).hexdigest()


def constructed_series(kind: str, theta_p, theta_t, **kw) -> Tuple[np.ndarray, str, Fraction, Fraction]:
    """The §7.2 known-answer series. Returns (rho, intended_status, exact_S_min, exact_S_term).
    Every constructed value lies EXACTLY on the frozen production count grid k/2500 (not necessarily
    dyadic in binary), and its frozen rational statistic is known independently; the intended status follows from those answers and the given thresholds by the frozen
    precedence — the control derives its expectation from the DEFINITIONS, not from the code."""
    verify_frozen_identity()
    declared_params = {cid: tuple(k for k, _ in params) for cid, params, *_ in CONTROL_CASES}
    if kind not in declared_params:
        raise ClassifyDomainError(f"unknown control {kind!r}")
    if tuple(sorted(kw)) != tuple(sorted(declared_params[kind])):          # exact key set (L2 r2 M2-5)
        raise ClassifyDomainError(f"control {kind!r}: parameter keys {sorted(kw)} != declared {sorted(declared_params[kind])}")
    tp_f = _threshold(theta_p, "theta_P"); tt_f = _threshold(theta_t, "theta_T")
    r = np.zeros(RUN_LEN, dtype=np.float64)
    tail = slice(TAIL_START, TAIL_END + 1)
    g = lambda k: np.float64(k) / np.float64(N_CELLS)          # a value ON the count grid
    if kind == "stable_above_null":
        r[tail] = g(1250)
    elif kind == "extinct_decayed":
        r[:TAIL_START] = g(625); r[tail] = 0.0
    elif kind == "bounded_oscillation_persistent":            # alternating 1000/1500 -> every window mean 1250/2500
        r[tail] = np.where(np.arange(TAIL_LEN) % 2 == 0, g(1000), g(1500))
    elif kind == "slow_drift_persistent":                     # windows 1250 + 125·i -> min 1250; terminal mean 2250/2500
        for i in range(N_WINDOWS): r[TAIL_START + i * WINDOW:TAIL_START + (i + 1) * WINDOW] = g(1250 + 125 * i)
    elif kind == "still_relaxing_unresolved":
        r[tail] = g(1250); r[TAIL_START + 2 * WINDOW:TAIL_START + 3 * WINDOW] = 0.0
    elif kind == "near_null_hoverer":
        hk = kw.get("hover_count")
        if isinstance(hk, bool) or not isinstance(hk, int) or not 0 <= hk <= N_CELLS:
            raise ClassifyDomainError("hover_count must be an integer count in [0, N_CELLS]")
        r[tail] = g(hk)
    else:
        raise ClassifyDomainError(f"unknown control {kind!r}")
    K = [int(round(float(x) * N_CELLS)) for x in r[tail]]                     # exact counts by construction
    wm = [Fraction(sum(K[i * WINDOW:(i + 1) * WINDOW]), WINDOW * N_CELLS) for i in range(N_WINDOWS)]
    s_min = min(wm); s_term = Fraction(sum(K[TERMINAL_WINDOWS[0] * WINDOW:(TERMINAL_WINDOWS[-1] + 1) * WINDOW]), 3 * WINDOW * N_CELLS)
    # The frozen status operation compares the float64 of a grid value against a float64 threshold
    # (M2 run_status). The intended status is derived by THAT operation on the exact statistics —
    # not by exact-rational comparison against Fraction(float), which idealizes the threshold.
    intended = "SUSTAINED" if float(s_min) > tp_f else ("NO_SUSTAINED" if float(s_term) <= tt_f else "UNRESOLVED")
    return r, intended, s_min, s_term


@dataclass
class ControlQualification:
    passed: bool
    results: Tuple[Tuple[str, str, str, bool], ...]      # (id, intended, observed, exact)
    missing: Tuple[str, ...]
    extra: Tuple[str, ...]


def qualify_controls(execution_ids: Optional[Sequence[str]] = None) -> ControlQualification:
    """The frozen control qualification: every declared control EXACTLY ONCE (L2 r2 M2-4 — duplicates
    refused), no extras; for each, three quantities must agree bit-exactly — (1) the generated
    series' statistics computed by exact rational arithmetic, (2) M2's tail_stats on the series,
    (3) the INDEPENDENTLY FROZEN rational expectations in CONTROL_CASES — and the observed status must
    equal the frozen intended status under CONTROL_THRESHOLDS."""
    verify_frozen_identity()
    if controls_digest() != CONTROL_CASES_SHA256_LITERAL:
        raise ClassifyDomainError("control case map differs from its frozen literal digest")
    declared = {cid: (dict(params), (smn, smd), (stn, std), intended) for cid, params, _, (smn, smd), (stn, std), intended in CONTROL_CASES}
    ids = tuple(c for c, *_ in CONTROL_CASES) if execution_ids is None else tuple(execution_ids)
    if len(set(ids)) != len(ids):
        raise ClassifyDomainError(f"duplicate control execution ids: {sorted(c for c in ids if ids.count(c) > 1)}")
    for cid in ids:
        if cid not in declared:
            raise ClassifyDomainError(f"unknown control {cid!r}")
    tp, tt = CONTROL_THRESHOLDS
    results: List[Tuple[str, str, str, bool]] = []
    for cid in ids:
        params, smin_exp, sterm_exp, intended_decl = declared[cid]
        r, intended_def, s_min_gen, s_term_gen = constructed_series(cid, tp, tt, **params)
        status, st = run_status(r, tp, tt)
        frozen_smin, frozen_sterm = Fraction(*smin_exp), Fraction(*sterm_exp)
        exact = (s_min_gen == frozen_smin and s_term_gen == frozen_sterm                     # generator == frozen
                 and st.s_min == float(frozen_smin) and st.s_term == float(frozen_sterm))     # M2 == frozen (raw float of exact)
        results.append((cid, intended_decl, status, exact and intended_def == intended_decl))
    missing = tuple(c for c in declared if c not in ids); extra = ()
    passed = not missing and len(ids) == len(declared) and all(ok and intended == observed for _, intended, observed, ok in results)
    return ControlQualification(passed, tuple(results), missing, extra)
