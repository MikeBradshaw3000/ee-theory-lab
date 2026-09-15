"""gates/gate_b/b2.py — B2: declared-ensemble distributional comparison (Gate B Specification
v0.4, FROZEN 2026-09-04; §4 of the v0.2 base as amended by v0.3 A2/A3/A5/A7 and v0.4 A4R/A6R;
certified claim per Mike's Path-B ruling of 2026-08-26).

CERTIFIED CLAIM (verbatim, carried in every report): Gate B2 certifies terminal-window
ensemble-mean equivalence plus the priced gross-divergence screen, and nothing more. It does
not certify distributional equivalence; a genuine distributional-equivalence criterion is a
named future object conditioned on an ensemble size that would give it real discriminating
power.

Reference side — the VERIFIED WRAPPER (§2 as amended by A7): a dynamics-only executor
replicating `execute_run` L488-507 exactly (legacy seeding of both RNGs; shuffle-init of 250
of 2,500; per tick: record pre-step state, u_t_for(mode, tier, u_const, t//25), one
rand_grid, step_tcop_core) using the pinned module's own functions. Its `states` output must
be bit-identical to the actual pinned `execute_run` on the declared ten-run
subset — one canonical run per B2 cell at seed 42 plus seed 137 in both CM-1 cells — which
requires FULL reference mode (execute_run exists only there). Bit-identical means: exact shape,
exact dtype, exact canonical bytes (equal SHA-256); np.array_equal is recorded as a diagnostic
only. AUTHORITATIVE requires that verification to PASS in the same run; PROVISIONAL records it
NOT_PERFORMED under EXTRACTION.

Candidate side — the instrument through its PUBLIC path (`Dynamics.step`), rule_mode
become_survive, Q-disabled, Generator regime (SeedRegistry(root).dynamics()), fixed_count
250, with the FROZEN ALIGNMENT (A2): rho[0] from the initialized pre-step grid; rho[t] for
t = 1..399 from the public-step output of tick t-1; the post-step state after tick 399 is
never computed. Both trajectories are exactly the 400 pre-step states.

Acceptance grammar (A3/A4R/A5): per cell, Welch two-one-sided tests on per-run terminal-
window mean rho (ticks 300-399), delta = 0.003, alpha_cell = 0.05/8, exact Student-t quantile
(scipy); the 98.75% interval of the candidate-reference mean difference must lie within
+/-delta; all eight cells must pass. Gross-divergence screen: tie-invariant ECDF statistic
D_int = max over unique pooled values of |2a - s|; exact conditional permutation null given
the observed tie blocks (DP over blocks with weights prod C(b_i, c_i)); alarm iff
p = P(D_int >= D_obs | tie blocks) <= 0.00125 (inclusive); familywise KS budget 0.01. Any
TOST failure or alarm is a fail-fast halt with an atomic failure record (v0.4 section 7).
Never-relax-after-output is in force: nothing here may be adjusted in light of any output.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import random as _pyrandom
import tempfile
import time
import uuid
from dataclasses import asdict, dataclass, field
from math import comb, sqrt
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from scipy.stats import t as _student_t

from ...config import RunConfig, InitConfig, DynamicsConstants
from ...dynamics import Dynamics
from ...init import initialize
from ...rng import SeedRegistry
from .b1 import (COMPARATOR_VERSION, SPEC_SHA256, SPEC_VERSION, ProvenanceError, candidate_provenance)
from .environment import (EXPECTED_LOCK_SHA256, EnvironmentCheckError, EnvironmentRecord, check_environment)
from .reference import (EXPECTED_SHA256 as REFERENCE_SHA256, PINNED_COMMIT, PINNED_RELPATH,
                        PinnedReference, ReferenceError, load_pinned_reference)

# ----------------------------------------------------------------------------- frozen grammar
GRID = 50
N_CELLS = GRID * GRID
INIT_ACTIVE = 250
TICKS = 400
BLOCK = 25
TERMINAL = (300, 400)
N_PER_SIDE = 20
DELTA = 0.003
ALPHA_CELL = 0.05 / 8
ALPHA_KS = 0.00125                      # 0.01 / 8, Bonferroni from the familywise KS budget
REF_SEEDS = tuple(range(201, 221))
CAND_ROOTS = tuple(range(301, 321))
CELLS: Tuple[Tuple[str, str, float, float, float], ...] = (
    # (id, mode, tier, u_const, kappa)
    ("cm0_u0.00_k+0.0000", "cm0", 0.0, 0.0, 0.0),
    ("cm0_u0.25_k+0.0000", "cm0", 0.0, 0.25, 0.0),
    ("cm0_u0.00_k+0.4221", "cm0", 0.0, 0.0, +0.4221),
    ("cm0_u0.00_k-0.4221", "cm0", 0.0, 0.0, -0.4221),
    ("cm0_u0.25_k+0.4221", "cm0", 0.0, 0.25, +0.4221),
    ("cm0_u0.25_k-0.4221", "cm0", 0.0, 0.25, -0.4221),
    ("cm1_t0.25_k+0.4221", "cm1", 0.25, 0.0, +0.4221),
    ("cm1_t0.25_k-0.4221", "cm1", 0.25, 0.0, -0.4221),
)
WRAPPER_VERIFICATION_RUNS: Tuple[Tuple[str, int], ...] = tuple((c[0], 42) for c in CELLS) + (
    ("cm1_t0.25_k+0.4221", 137), ("cm1_t0.25_k-0.4221", 137))
# FROZEN B2 COMPLETION OBJECT (B2-3): a deliberately SEPARATE literal from the execution
# constants above. The completion stage compares what ran against THIS, so a narrowed,
# reordered, or re-seeded execution cannot define its own passing expectation. Any edit here
# is an edit to the frozen grammar (versioned amendment by Mike's act, never in place).
FROZEN_B2: Dict[str, Any] = {
    "cells": (("cm0_u0.00_k+0.0000", "cm0", 0.0, 0.0, 0.0), ("cm0_u0.25_k+0.0000", "cm0", 0.0, 0.25, 0.0),
              ("cm0_u0.00_k+0.4221", "cm0", 0.0, 0.0, +0.4221), ("cm0_u0.00_k-0.4221", "cm0", 0.0, 0.0, -0.4221),
              ("cm0_u0.25_k+0.4221", "cm0", 0.0, 0.25, +0.4221), ("cm0_u0.25_k-0.4221", "cm0", 0.0, 0.25, -0.4221),
              ("cm1_t0.25_k+0.4221", "cm1", 0.25, 0.0, +0.4221), ("cm1_t0.25_k-0.4221", "cm1", 0.25, 0.0, -0.4221)),
    "ref_seeds": tuple(range(201, 221)), "cand_roots": tuple(range(301, 321)), "n_per_side": 20,
    "ticks": 400, "block": 25, "n_blocks": 16, "terminal": (300, 400),
    "delta": 0.003, "alpha_cell": 0.00625, "alpha_ks": 0.00125,
    "wrapper_map": (("cm0_u0.00_k+0.0000", 42), ("cm0_u0.25_k+0.0000", 42), ("cm0_u0.00_k+0.4221", 42),
                    ("cm0_u0.00_k-0.4221", 42), ("cm0_u0.25_k+0.4221", 42), ("cm0_u0.25_k-0.4221", 42),
                    ("cm1_t0.25_k+0.4221", 42), ("cm1_t0.25_k-0.4221", 42),
                    ("cm1_t0.25_k+0.4221", 137), ("cm1_t0.25_k-0.4221", 137)),
    "stages": ("preflight", "wrapper_verification", "ensembles", "completion"),
    "claim_version": "Path-B ruling 2026-08-26 / Gate B v0.4",
    # Independent identity of the certified claim text: compared against the RUNTIME text's digest,
    # never against the module constant that seeds it (3B).
    "claim_sha256": "21e084028edbd0e29d7ca5f4be005e1e6e1fbf65ef40c0eac6b09fa99004cc2c",
    # Expected candidate schedule tuple per cell, as literals (reference-defined levels; B1 certifies
    # the candidate's schedule FUNCTION, B2 records and checks the schedule CONSUMED).
    "expected_schedules": {
        "cm0_u0.00_k+0.0000": ((0, 0.0),), "cm0_u0.25_k+0.0000": ((0, 0.25),),
        "cm0_u0.00_k+0.4221": ((0, 0.0),), "cm0_u0.00_k-0.4221": ((0, 0.0),),
        "cm0_u0.25_k+0.4221": ((0, 0.25),), "cm0_u0.25_k-0.4221": ((0, 0.25),),
        "cm1_t0.25_k+0.4221": tuple((b * 25, (0.0, 0.125, 0.25)[b % 3]) for b in range(16)),
        "cm1_t0.25_k-0.4221": tuple((b * 25, (0.0, 0.125, 0.25)[b % 3]) for b in range(16)),
    },
}
STAGES: Tuple[str, ...] = ("preflight", "wrapper_verification", "ensembles", "completion")   # compared to FROZEN_B2["stages"] at preflight
CERTIFIED_CLAIM = ("Gate B2 certifies terminal-window ensemble-mean equivalence plus the priced "
                   "gross-divergence screen, and nothing more. It does not certify distributional "
                   "equivalence; a genuine distributional-equivalence criterion is a named future "
                   "object conditioned on an ensemble size that would give it real discriminating "
                   "power. (Mike's Path-B ruling of record, 2026-08-26.)")


# ----------------------------------------------------------------------------- records
class GateBFailure(RuntimeError):
    def __init__(self, record: "B2FailureRecord") -> None:
        super().__init__(record.summary())
        self.record = record


class StatisticalDomainError(ValueError):
    """Named refusal: input outside the frozen executable domain of a statistic (B2-4)."""


class CaptureError(RuntimeError):
    """Named structural refusal at the candidate sink/time boundary (B2-2)."""
    def __init__(self, check: str, message: str) -> None:
        super().__init__(message); self.check = check


@dataclass
class CellResult:
    cell: str
    definition: Dict[str, Any]              # mode, tier, u_const, kappa, and the ACTUAL candidate schedule tuple
    ref_seeds: List[int]
    cand_roots: List[int]
    ref_terminal: List[float]
    cand_terminal: List[float]
    ref_blocks: List[List[float]]           # (20, 16) diagnostic-only, derived from the same trajectories
    cand_blocks: List[List[float]]          # (20, 16) diagnostic-only
    ref_mean: float
    cand_mean: float
    diff: float
    welch_se: float
    welch_df: float
    t_quantile: float
    half_width: float
    ci_low: float
    ci_high: float
    tost_pass: bool
    D_int: int
    tie_blocks: int
    screen_p: float
    alarm: bool


@dataclass
class B2FailureRecord:
    failure_class: str      # reference | environment | provenance | wrapper | acceptance | screen | statistical_domain | structural | internal
    stage: str
    cell: str
    check: str
    detail: str
    expected: str
    observed: str
    environment: str
    environment_record: Optional[Dict[str, Any]]
    provenance: Dict[str, Any]
    cells_completed: List[Dict[str, Any]]
    wrapper_verification: Dict[str, Any]     # ordered declared map + every completed run + status (B2-5)
    stages_completed: List[str]              # frozen §7: stages completed before the halt
    written_to: Optional[str] = None

    def summary(self) -> str:
        return (f"B2 HALT [{self.failure_class}] stage={self.stage} cell={self.cell} check={self.check} "
                f"expected={self.expected} observed={self.observed} detail={self.detail!r} "
                f"cells_completed={len(self.cells_completed)}")


@dataclass
class B2Report:
    label: str
    environment: str
    environment_record: Optional[Dict[str, Any]]
    provenance: Dict[str, Any]
    certified_claim: str = CERTIFIED_CLAIM
    wrapper_verification: Dict[str, Any] = field(default_factory=lambda: {
        "status": "NOT_PERFORMED", "declared_map": [list(x) for x in FROZEN_B2["wrapper_map"]], "runs": []})
    cells: List[CellResult] = field(default_factory=list)
    failure: Optional[B2FailureRecord] = None
    stages_completed: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return (self.failure is None and _completion_defects(self) == []
                and all(c.tost_pass and not c.alarm for c in self.cells))

    def summary(self) -> str:
        cells = " ".join(f"{c.cell}:d={c.diff:+.5f}[{c.ci_low:+.5f},{c.ci_high:+.5f}]"
                         f"{'T' if c.tost_pass else 'F'}/D{c.D_int}p{c.screen_p:.4g}{'!' if c.alarm else ''}" for c in self.cells)
        return (f"B2[{self.label}] wrapper={self.wrapper_verification['status']} {cells} "
                + ("=> PASS" if self.passed else f"=> FAIL ({self.failure.summary() if self.failure else 'incomplete'})"))


def write_failure_record_atomically(record: B2FailureRecord, record_dir: str) -> str:
    os.makedirs(record_dir, exist_ok=True)
    final = os.path.join(record_dir, f"gate_b_b2_failure_{time.time_ns()}_{os.getpid()}_{uuid.uuid4().hex[:8]}.json")
    fd, tmp = tempfile.mkstemp(dir=record_dir, prefix=".b2_failure_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(asdict(record), fh, indent=1, default=str); fh.flush(); os.fsync(fh.fileno())
        os.replace(tmp, final)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return final


# ----------------------------------------------------------------------------- reference wrapper
def reference_wrapper_states(ref: PinnedReference, mode: str, tier: float, u_const: float, kappa: float,
                             seed: int) -> np.ndarray:
    """Replicates execute_run L488-507 exactly, with the pinned module's own step and schedule.
    Returns the 400 pre-step states, dtype int, shape (400, 50, 50). Both global RNG states are
    saved and restored in `finally`."""
    np_state = np.random.get_state(); py_state = _pyrandom.getstate()
    try:
        np.random.seed(seed)
        _pyrandom.seed(seed)
        flat_grid = np.zeros(N_CELLS, dtype=int)
        flat_grid[:INIT_ACTIVE] = 1
        np.random.shuffle(flat_grid)
        grid = flat_grid.reshape((GRID, GRID))
        states = np.zeros((TICKS, GRID, GRID), dtype=int)
        for t in range(TICKS):
            states[t] = grid
            block_idx = t // BLOCK
            u_t = ref.u_t_for(mode, tier, u_const, block_idx)
            rand_grid = np.random.rand(GRID, GRID)
            grid, _ = ref.step_tcop_core(grid, u_t, kappa, rand_grid)
        return states
    finally:
        np.random.set_state(np_state); _pyrandom.setstate(py_state)


def rho_trajectory_from_states(states: np.ndarray) -> np.ndarray:
    return states.reshape(TICKS, -1).mean(axis=1)


def summaries_from_trajectory(rho: np.ndarray) -> Tuple[float, List[float]]:
    """From ONE aligned 400-state trajectory: the terminal statistic and the 16 diagnostic block
    means (B2-1). Never recompute a seed separately for the two summaries."""
    rho = np.asarray(rho, dtype=np.float64)
    if rho.shape != (TICKS,) or not np.isfinite(rho).all():
        raise StatisticalDomainError(f"trajectory must be {TICKS} finite values, got shape {rho.shape}")
    terminal = float(rho[TERMINAL[0]:TERMINAL[1]].mean())
    blocks = [float(rho[b * BLOCK:(b + 1) * BLOCK].mean()) for b in range(TICKS // BLOCK)]
    return terminal, blocks


def terminal_mean_from_states(states: np.ndarray) -> float:
    return summaries_from_trajectory(rho_trajectory_from_states(states))[0]


# ----------------------------------------------------------------------------- candidate
def _cell_cfg(ref: PinnedReference, mode: str, tier: float, u_const: float, kappa: float, root: int) -> RunConfig:
    if mode == "cm0":
        schedule: Tuple[Tuple[int, float], ...] = ((0, float(u_const)),)
    else:
        schedule = tuple((b * BLOCK, float(ref.u_t_for("cm1", tier, 0.0, b))) for b in range(TICKS // BLOCK))
    return RunConfig(seed=root, rule_mode="become_survive", grid_scale=GRID, ticks=TICKS,
                     init=InitConfig(scheme="fixed_count", fixed_count=INIT_ACTIVE),
                     constants=DynamicsConstants(logit_l=float(ref.LOGIT_L), kappa=float(kappa),
                                                 p_survive=float(ref.LAMBDA)),
                     drive_schedule=schedule)


def candidate_rho_trajectory(ref: PinnedReference, mode: str, tier: float, u_const: float, kappa: float,
                             root: int, consumed_schedule: Optional[List[Tuple[Tuple[int, float], ...]]] = None) -> np.ndarray:
    """The instrument through its public path under the FROZEN alignment (A2): 400 pre-step
    densities; the post-step state after tick 399 is never computed. The drive_schedule of the
    configuration ACTUALLY consumed is appended to `consumed_schedule` when given (B2-6)."""
    cfg = _cell_cfg(ref, mode, tier, u_const, kappa, root)
    if consumed_schedule is not None:
        consumed_schedule.append(tuple((int(a), float(b)) for a, b in cfg.drive_schedule))
    dyn = SeedRegistry(root).dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    model = Dynamics(cfg, state, dyn)
    rhos = np.zeros(TICKS)
    rhos[0] = float(np.mean(state.is_active))                  # pre-step: the initialized grid
    expected_fields = frozenset({"g_q", "p_become", "rand_grid", "is_active", "Psi_local"})
    for t in range(TICKS - 1):                                  # ticks 0..398 -> pre-step states 1..399
        captures: List[Tuple[int, np.ndarray]] = []             # FRESH per tick (B2-2)
        def sink(tick, fields, _t=t, _c=captures):
            have = frozenset(fields)
            if have != expected_fields:
                raise CaptureError("sink_field_family", f"tick {_t}: fields {sorted(have)} != expected B family")
            s = fields["is_active"]
            if not isinstance(s, np.ndarray) or s.dtype != np.bool_:
                raise CaptureError("is_active_dtype", f"tick {_t}: is_active dtype {getattr(s, 'dtype', type(s))} is not bool")
            if s.shape != (GRID, GRID):
                raise CaptureError("is_active_shape", f"tick {_t}: is_active shape {s.shape} != {(GRID, GRID)}")
            _c.append((int(tick), s.copy()))                    # copy before leaving the callback
        model.step(sink)
        if len(captures) != 1:
            raise CaptureError("sink_invocation_count", f"tick {t}: {len(captures)} sink invocations, expected exactly 1")
        emitted_tick, s = captures[0]
        if emitted_tick != t:
            raise CaptureError("sink_tick_index", f"tick {t}: sink reported tick {emitted_tick}")
        rhos[t + 1] = float(np.mean(s))
    return rhos


def candidate_terminal_mean(ref: PinnedReference, mode: str, tier: float, u_const: float, kappa: float,
                            root: int) -> float:
    return summaries_from_trajectory(candidate_rho_trajectory(ref, mode, tier, u_const, kappa, root))[0]




# ----------------------------------------------------------------------------- statistics
def _panel(x, role: str) -> np.ndarray:
    a = np.asarray(x)
    if a.dtype != np.float64:
        raise StatisticalDomainError(f"{role}: float64 required, got {a.dtype}")
    if a.shape != (N_PER_SIDE,):
        raise StatisticalDomainError(f"{role}: exactly {N_PER_SIDE} values required, got shape {a.shape}")
    if not np.isfinite(a).all():
        raise StatisticalDomainError(f"{role}: nonfinite value present")
    return a


def welch_tost(cand, ref) -> Dict[str, Any]:
    """Welch TOST on two frozen-size float64 panels. Zero-variance (zero-SE) input is REFUSED,
    not resolved by a limiting convention: any deterministic-limit treatment is Mike's ruling to
    make before it is implemented (B2-4)."""
    a = _panel(cand, "candidate"); b = _panel(ref, "reference")
    # Degeneracy is a STRUCTURAL fact, not a floating-point one: a constant panel has zero variance
    # by definition, but np.var of twenty identical non-representable values is ~1e-34, not 0, and a
    # "se > 0" guard is defeated by rounding. Refuse on bit-identical values within a side.
    for arr, role in ((a, "candidate"), (b, "reference")):
        if np.all(arr.view(np.uint64) == arr.view(np.uint64)[0]):
            raise StatisticalDomainError(f"{role}: zero-variance panel (all values identical); a limiting "
                                         "rule is Mike's ruling to make, not the code's")
    d = float(a.mean() - b.mean())
    va, vb = float(a.var(ddof=1)), float(b.var(ddof=1))
    se = sqrt(va / N_PER_SIDE + vb / N_PER_SIDE)
    if not (np.isfinite(se) and se > 0.0):
        raise StatisticalDomainError(f"Welch SE must be finite and positive, got {se!r}")
    df = (va / N_PER_SIDE + vb / N_PER_SIDE) ** 2 / ((va / N_PER_SIDE) ** 2 / (N_PER_SIDE - 1)
                                                    + (vb / N_PER_SIDE) ** 2 / (N_PER_SIDE - 1))
    if not (np.isfinite(df) and df > 0.0):
        raise StatisticalDomainError(f"Welch df must be finite and positive, got {df!r}")
    tq = float(_student_t.ppf(1.0 - ALPHA_CELL, df))            # exact quantile (frozen env: scipy 1.17.1)
    hw = tq * se
    if not all(np.isfinite(v) for v in (tq, hw, d - hw, d + hw)):
        raise StatisticalDomainError("nonfinite quantile or interval endpoint")
    return {"diff": d, "se": se, "df": float(df), "t_quantile": tq, "half_width": hw,
            "ci_low": d - hw, "ci_high": d + hw, "pass": (d - hw > -DELTA) and (d + hw < DELTA)}


def ecdf_D_int(cand, ref, n: int = N_PER_SIDE) -> Tuple[int, Tuple[int, ...]]:
    """Tie-invariant: D_int = max over unique-value prefixes of |2a - s| (a = #cand <= v, s = #pooled <= v).
    `n` is exposed ONLY so the DP can be checked against an exhaustive small-n oracle in tests."""
    a = np.asarray(cand, dtype=np.float64); b = np.asarray(ref, dtype=np.float64)
    if a.shape != (n,) or b.shape != (n,) or not (np.isfinite(a).all() and np.isfinite(b).all()):
        raise StatisticalDomainError(f"screen requires exactly {n} finite values per side")
    pooled = np.concatenate([a, b])
    labels = np.concatenate([np.ones(n, int), np.zeros(n, int)])
    order = np.argsort(pooled, kind="mergesort")
    pv, lv = pooled[order], labels[order]
    blocks: List[int] = []; cand_in: List[int] = []
    i = 0
    while i < 2 * n:
        j = i
        while j < 2 * n and pv[j] == pv[i]:
            j += 1
        blocks.append(j - i); cand_in.append(int(lv[i:j].sum())); i = j
    D = 0; a = s = 0
    for bsz, c in zip(blocks, cand_in):
        a += c; s += bsz
        D = max(D, abs(2 * a - s))
    return D, tuple(blocks)


def conditional_permutation_p(D_obs: int, blocks: Tuple[int, ...], n: int = N_PER_SIDE) -> float:
    """Exact P(D_int >= D_obs | tie blocks): DP over blocks, state (candidate labels used,
    running max capped at D_obs), weights prod C(b_i, c_i), normalized by C(2n, n). The DP's
    terminal weight is asserted equal to C(2n, n) before pricing (B2-4)."""
    N = n
    if not all(isinstance(b, (int, np.integer)) and b >= 1 for b in blocks) or sum(blocks) != 2 * N:
        raise StatisticalDomainError(f"tie blocks must be positive integers summing to {2 * N}, got {blocks}")
    if not isinstance(D_obs, (int, np.integer)) or not (0 <= D_obs <= N):
        raise StatisticalDomainError(f"D_obs must be an integer in [0, {N}], got {D_obs!r}")
    total = comb(2 * N, N)
    dp: Dict[Tuple[int, int], int] = {(0, 0): 1}
    s = 0
    for bsz in blocks:
        s2 = s + bsz
        nxt: Dict[Tuple[int, int], int] = {}
        for (a, m), w in dp.items():
            for c in range(0, min(bsz, N - a) + 1):
                if (s - a) + (bsz - c) > N:
                    continue
                a2 = a + c
                m2 = min(max(m, abs(2 * a2 - s2)), D_obs)
                nxt[(a2, m2)] = nxt.get((a2, m2), 0) + w * comb(bsz, c)
        dp = nxt; s = s2
    terminal_weight = sum(w for (a, m), w in dp.items() if a == N)
    if terminal_weight != total:
        raise StatisticalDomainError(f"DP normalization {terminal_weight} != C({2*N},{N}) = {total}")
    hit = sum(w for (a, m), w in dp.items() if a == N and m >= D_obs)
    return hit / total


def gross_divergence_screen(cand, ref) -> Dict[str, Any]:
    a = _panel(cand, "candidate"); b = _panel(ref, "reference")
    D, blocks = ecdf_D_int(a, b)
    p = conditional_permutation_p(D, blocks)
    return {"D_int": D, "tie_blocks": int(sum(1 for b in blocks if b > 1)), "p": p, "alarm": p <= ALPHA_KS}


# ----------------------------------------------------------------------------- runner
class _Runner:
    def __init__(self, rep: B2Report) -> None:
        self.rep = rep; self.ref: Optional[PinnedReference] = None
        self.stage = "preflight"; self.cell = "-"

    def fail(self, failure_class: str, check: str, expected: str, observed: str, detail: str = "") -> None:
        rec = B2FailureRecord(failure_class=failure_class, stage=self.stage, cell=self.cell, check=check,
                              detail=detail, expected=expected, observed=observed, environment=self.rep.environment,
                              environment_record=self.rep.environment_record, provenance=dict(self.rep.provenance),
                              cells_completed=[asdict(c) for c in self.rep.cells],
                              wrapper_verification=dict(self.rep.wrapper_verification),
                              stages_completed=list(self.rep.stages_completed))
        self.rep.failure = rec
        raise GateBFailure(rec)

    def classify_and_fail(self, exc: BaseException) -> None:
        if isinstance(exc, GateBFailure):
            raise exc
        if isinstance(exc, EnvironmentCheckError):
            self.fail("environment", "frozen_pin_source", "", "", str(exc))
        if isinstance(exc, ReferenceError):
            self.fail("reference", "reference_load", "", "", str(exc))
        if isinstance(exc, ProvenanceError):
            self.fail("provenance", exc.check, "", "", str(exc))
        if isinstance(exc, CaptureError):
            self.fail("structural", exc.check, "", "", str(exc))
        if isinstance(exc, StatisticalDomainError):
            self.fail("statistical_domain", "input_domain", "", "", str(exc))
        self.fail("internal", "unexpected_exception", "", "", f"{type(exc).__name__}: {exc}")


def _completion_defects(rep: "B2Report", include_stage_check: bool = True) -> List[Tuple[str, str, str]]:
    """Compare what ran against FROZEN_B2 — never against the execution constants (B2-3).
    Returns (check, expected, observed) triples; empty means complete."""
    F = FROZEN_B2; out: List[Tuple[str, str, str]] = []
    got = [(c.cell, c.definition["mode"], c.definition["tier"], c.definition["u_const"], c.definition["kappa"]) for c in rep.cells]
    if got != list(F["cells"]):
        out.append(("cell_map", repr(list(F["cells"])), repr(got)))
    for c in rep.cells:
        if c.ref_seeds != list(F["ref_seeds"]) or c.cand_roots != list(F["cand_roots"]):
            out.append(("seed_pools", f"{list(F['ref_seeds'])}/{list(F['cand_roots'])}", f"{c.ref_seeds}/{c.cand_roots}@{c.cell}"))
        if len(c.ref_terminal) != F["n_per_side"] or len(c.cand_terminal) != F["n_per_side"]:
            out.append(("terminal_vectors", f"{F['n_per_side']} per side", f"{len(c.ref_terminal)}/{len(c.cand_terminal)}@{c.cell}"))
        if (len(c.ref_blocks) != F["n_per_side"] or len(c.cand_blocks) != F["n_per_side"]
                or any(len(b) != F["n_blocks"] for b in c.ref_blocks + c.cand_blocks)):
            out.append(("block_matrices", f"({F['n_per_side']},{F['n_blocks']}) per side", f"malformed@{c.cell}"))
    for c in rep.cells:
        exp_sched = [list(x) for x in F["expected_schedules"].get(c.cell, ())]
        if c.definition.get("candidate_schedule") != exp_sched:
            out.append(("schedule_consumed", repr(exp_sched), f"{c.definition.get('candidate_schedule')!r}@{c.cell}"))
    grammar = rep.provenance.get("grammar", {})
    exp_grammar = {"delta": F["delta"], "alpha_cell": F["alpha_cell"], "alpha_ks": F["alpha_ks"],
                   "n_per_side": F["n_per_side"], "terminal_window": list(F["terminal"]), "ticks": F["ticks"],
                   "block": F["block"], "n_blocks": F["n_blocks"]}
    for k, v in exp_grammar.items():
        if grammar.get(k) != v:
            out.append(("grammar_" + k, repr(v), repr(grammar.get(k))))
    if include_stage_check and rep.stages_completed != list(F["stages"]):
        out.append(("stages", repr(list(F["stages"])), repr(rep.stages_completed)))
    wv = rep.wrapper_verification
    if wv.get("status") != "NOT_PERFORMED":                     # performed at all -> frozen map, exactly (3C)
        done = [(x["cell"], x["seed"]) for x in wv.get("runs", [])]
        if done != list(F["wrapper_map"]):
            out.append(("wrapper_map", repr(list(F["wrapper_map"])), f"{wv.get('status')}:{done}"))
    if rep.label == "AUTHORITATIVE" and wv.get("status") != "PASS":
        out.append(("wrapper_status", "PASS", str(wv.get("status"))))
    # certified claim: runtime text digest vs the INDEPENDENT frozen digest, plus the version (3B)
    if hashlib.sha256(rep.certified_claim.encode()).hexdigest() != F["claim_sha256"]:
        out.append(("certified_claim", F["claim_sha256"], hashlib.sha256(rep.certified_claim.encode()).hexdigest()))
    if rep.provenance.get("claim_version") != F["claim_version"]:
        out.append(("claim_version", F["claim_version"], repr(rep.provenance.get("claim_version"))))
    return out


def _static_grammar_defects(rep: "B2Report") -> List[Tuple[str, str, str]]:
    """STATIC preflight (L2 m3 r3 item 1A): the execution constants that will govern this run are
    compared to FROZEN_B2 BEFORE any wrapper or ensemble output exists. A gate must never score
    under a grammar it already knows is not the frozen grammar."""
    F = FROZEN_B2; out: List[Tuple[str, str, str]] = []
    checks = [("cells", tuple(F["cells"]), tuple(CELLS)), ("ref_seeds", tuple(F["ref_seeds"]), tuple(REF_SEEDS)),
              ("cand_roots", tuple(F["cand_roots"]), tuple(CAND_ROOTS)), ("n_per_side", F["n_per_side"], N_PER_SIDE),
              ("ticks", F["ticks"], TICKS), ("block", F["block"], BLOCK), ("n_blocks", F["n_blocks"], TICKS // BLOCK),
              ("terminal", tuple(F["terminal"]), tuple(TERMINAL)), ("delta", F["delta"], DELTA),
              ("alpha_cell", F["alpha_cell"], ALPHA_CELL), ("alpha_ks", F["alpha_ks"], ALPHA_KS),
              ("wrapper_map", tuple(F["wrapper_map"]), tuple(WRAPPER_VERIFICATION_RUNS)),
              ("stages", tuple(F["stages"]), tuple(STAGES)),
              ("claim_sha256", F["claim_sha256"], hashlib.sha256(rep.certified_claim.encode()).hexdigest()),
              ("claim_version", F["claim_version"], rep.provenance.get("claim_version"))]
    for name, expected, observed in checks:
        if expected != observed:
            out.append(("static_" + name, repr(expected), repr(observed)))
    return out


def _cell_by_id(cell_id: str) -> Tuple[str, str, float, float, float]:
    for c in CELLS:
        if c[0] == cell_id:
            return c
    raise KeyError(cell_id)


def verify_wrapper(ref: PinnedReference, r: _Runner) -> Dict[str, Any]:
    """Ten-run bit-identity of the wrapper's states against the actual pinned execute_run.
    FULL mode only (execute_run is absent under EXTRACTION -> NOT_PERFORMED, recorded)."""
    wv = r.rep.wrapper_verification
    if "execute_run" not in ref.ns:
        wv.update({"status": "NOT_PERFORMED", "reason": "execute_run unavailable (EXTRACTION mode)"})
        return wv
    wv["status"] = "IN_PROGRESS"
    runs: List[Dict[str, Any]] = wv["runs"]                      # accumulates in the report (B2-5)
    for cell_id, seed in WRAPPER_VERIFICATION_RUNS:
        r.cell = f"{cell_id}|seed={seed}"
        _, mode, tier, u_const, kappa = _cell_by_id(cell_id)
        np_state = np.random.get_state(); py_state = _pyrandom.getstate()
        try:
            actual = ref.execute_run(mode, f"k{kappa:+.4f}", kappa, tier, u_const, seed, "gate_b_wrapper_verification")
        finally:
            np.random.set_state(np_state); _pyrandom.setstate(py_state)
        actual_states = np.asarray(actual[0])
        wrapper_states = reference_wrapper_states(ref, mode, tier, u_const, kappa, seed)
        a_bytes = np.ascontiguousarray(actual_states).tobytes(); w_bytes = np.ascontiguousarray(wrapper_states).tobytes()
        a_sha, w_sha = hashlib.sha256(a_bytes).hexdigest(), hashlib.sha256(w_bytes).hexdigest()
        # BIT identity, literally (B2-5 repair): exact shape, exact dtype, exact canonical bytes.
        # np.array_equal is recorded as a DIAGNOSTIC only — it is True across differing integer dtypes.
        identical = (actual_states.shape == wrapper_states.shape and actual_states.dtype == wrapper_states.dtype
                     and a_bytes == w_bytes and a_sha == w_sha)
        runs.append({"cell": cell_id, "seed": seed, "identical": bool(identical),
                     "actual_shape": list(actual_states.shape), "wrapper_shape": list(wrapper_states.shape),
                     "actual_dtype": str(actual_states.dtype), "wrapper_dtype": str(wrapper_states.dtype),
                     "actual_sha256": a_sha, "wrapper_sha256": w_sha,
                     "array_equal_diagnostic": bool(actual_states.shape == wrapper_states.shape
                                                    and np.array_equal(actual_states, wrapper_states))})
        if not identical:
            wv["status"] = "FAIL"; wv["first_failing_run"] = runs[-1]
            r.fail("wrapper", "states_bit_identity", runs[-1]["actual_sha256"], runs[-1]["wrapper_sha256"],
                   f"wrapper diverges from pinned execute_run at {cell_id} seed {seed}")
    wv["status"] = "PASS"
    return wv


def run_b2(pinned_root: str, label: str = "PROVISIONAL", load_mode: str = "EXTRACTION",
           record_dir: Optional[str] = None, qualification: bool = False) -> B2Report:
    if (label == "AUTHORITATIVE" or qualification) and record_dir is None:
        raise ValueError("AUTHORITATIVE and formal-qualification Gate B runs require a persistent "
                         "failure-record owner: record_dir is mandatory (refused before start)")
    env_str = f"python{platform.python_version()}/numpy{np.__version__}"
    prov: Dict[str, Any] = {"label": label, "load_mode": load_mode, "environment": env_str,
                            "expected": {"reference_commit": PINNED_COMMIT, "reference_relpath": PINNED_RELPATH,
                                         "reference_sha256": REFERENCE_SHA256, "lock_sha256": EXPECTED_LOCK_SHA256,
                                         "pinned_root_arg": os.path.realpath(pinned_root)},
                            "spec": SPEC_VERSION, "spec_sha256": SPEC_SHA256, "comparators": COMPARATOR_VERSION,
                            "claim_version": FROZEN_B2["claim_version"],
                            "grammar": {"delta": DELTA, "alpha_cell": ALPHA_CELL, "alpha_ks": ALPHA_KS,
                                        "n_per_side": N_PER_SIDE, "terminal_window": list(TERMINAL), "ticks": TICKS,
                                        "block": BLOCK, "n_blocks": TICKS // BLOCK,
                                        "ref_seeds": list(REF_SEEDS), "cand_roots": list(CAND_ROOTS),
                                        "cells": [list(c) for c in CELLS],
                                        "frozen_completion_object": {k: (list(v) if isinstance(v, tuple) else v)
                                                                     for k, v in FROZEN_B2.items()}}}
    rep = B2Report(label=label, environment=env_str, environment_record=None, provenance=prov)
    r = _Runner(rep)

    def _boundary(stage: str, fn: Callable[[], Any]) -> Any:
        r.stage = stage
        try:
            return fn()
        except BaseException as e:            # noqa: BLE001
            try:
                r.classify_and_fail(e)
            except GateBFailure as gf:
                if record_dir is not None:
                    gf.record.written_to = write_failure_record_atomically(gf.record, record_dir)
                return None

    def _preflight() -> None:
        r.cell = "environment"
        envrec: EnvironmentRecord = check_environment(pinned_root)
        rep.environment_record = asdict(envrec); prov["environment_conforms"] = envrec.conforms
        if label == "AUTHORITATIVE" and not envrec.conforms:
            r.fail("environment", "frozen_environment", "conforming", "non-conforming", "; ".join(envrec.failures))
        if label == "AUTHORITATIVE" and load_mode != "FULL":
            r.fail("environment", "load_mode", "FULL", load_mode, "AUTHORITATIVE requires FULL reference import")
        r.cell = "reference"
        r.ref = load_pinned_reference(pinned_root, load_mode, label)
        prov["reference"] = asdict(r.ref.provenance)
        r.cell = "candidate_provenance"
        inst_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        candidate_provenance(inst_root, prov)
        r.cell = "static_frozen_grammar"
        defects = _static_grammar_defects(rep)
        if defects:
            r.fail("structural", defects[0][0], defects[0][1], defects[0][2],
                   f"{len(defects)} static frozen-grammar defect(s) before any output: {[d[0] for d in defects]}")

    def _wrapper() -> None:
        verify_wrapper(r.ref, r)
        wv = rep.wrapper_verification
        if wv["status"] != "NOT_PERFORMED":                     # performed at all -> frozen map, NOW (item 2)
            done = [(x["cell"], x["seed"]) for x in wv["runs"]]
            if done != list(FROZEN_B2["wrapper_map"]):
                r.cell = "wrapper"
                r.fail("structural", "wrapper_map", repr(list(FROZEN_B2["wrapper_map"])), f"{wv['status']}:{done}",
                       "performed wrapper map is not the frozen ten-run map; halting before any ensemble")
        if label == "AUTHORITATIVE" and rep.wrapper_verification["status"] != "PASS":
            r.cell = "wrapper"
            r.fail("wrapper", "verification_required", "PASS", rep.wrapper_verification["status"],
                   "AUTHORITATIVE requires the ten-run wrapper bit-identity verification to PASS")

    def _ensembles() -> None:
        for cell_id, mode, tier, u_const, kappa in CELLS:
            r.cell = cell_id
            ref_summ = [summaries_from_trajectory(rho_trajectory_from_states(
                reference_wrapper_states(r.ref, mode, tier, u_const, kappa, s))) for s in REF_SEEDS]
            consumed: List[Tuple[Tuple[int, float], ...]] = []
            cand_summ = [summaries_from_trajectory(candidate_rho_trajectory(r.ref, mode, tier, u_const, kappa, s, consumed))
                         for s in CAND_ROOTS]
            if len(consumed) != len(CAND_ROOTS) or any(sc != consumed[0] for sc in consumed):
                r.fail("structural", "schedule_consumed_uniform", "one identical schedule across all 20 candidate runs",
                       repr(sorted(set(consumed))), f"candidate schedules differ across roots at {cell_id}")
            expected_sched = tuple((int(a), float(b)) for a, b in FROZEN_B2["expected_schedules"][cell_id])
            if consumed[0] != expected_sched:                    # BEFORE any panel/TOST/screen (item 3)
                r.fail("structural", "schedule_consumed", repr(expected_sched), repr(consumed[0]),
                       f"consumed schedule is not the frozen schedule for {cell_id}; no score computed")
            ref_t = np.array([x[0] for x in ref_summ]); cand_t = np.array([x[0] for x in cand_summ])
            tost = welch_tost(cand_t, ref_t)
            scr = gross_divergence_screen(cand_t, ref_t)
            res = CellResult(cell=cell_id,
                             definition={"mode": mode, "tier": tier, "u_const": u_const, "kappa": kappa,
                                         "candidate_schedule": [list(x) for x in consumed[0]]},
                             ref_seeds=list(REF_SEEDS), cand_roots=list(CAND_ROOTS),
                             ref_terminal=[float(x) for x in ref_t], cand_terminal=[float(x) for x in cand_t],
                             ref_blocks=[x[1] for x in ref_summ], cand_blocks=[x[1] for x in cand_summ],
                             ref_mean=float(ref_t.mean()), cand_mean=float(cand_t.mean()), diff=tost["diff"],
                             welch_se=tost["se"], welch_df=tost["df"], t_quantile=tost["t_quantile"],
                             half_width=tost["half_width"], ci_low=tost["ci_low"], ci_high=tost["ci_high"],
                             tost_pass=bool(tost["pass"]), D_int=int(scr["D_int"]), tie_blocks=int(scr["tie_blocks"]),
                             screen_p=float(scr["p"]), alarm=bool(scr["alarm"]))
            rep.cells.append(res)
            if res.alarm:
                r.fail("screen", "gross_divergence_alarm", f"p > {ALPHA_KS}", f"D_int={res.D_int} p={res.screen_p:.6g}",
                       f"exact conditional permutation screen alarmed at {cell_id}")
            if not res.tost_pass:
                r.fail("acceptance", "welch_tost", f"CI within ±{DELTA}", f"[{res.ci_low:+.6f}, {res.ci_high:+.6f}]",
                       f"terminal-window mean equivalence failed at {cell_id}")

    def _completion() -> None:
        r.cell = "frozen_completion"
        prefix = list(FROZEN_B2["stages"][:-1])
        if rep.stages_completed != prefix:                       # persisted structural/stages (item 4)
            r.fail("structural", "stages", repr(prefix), repr(rep.stages_completed), "stage prefix differs from the frozen declaration")
        defects = _completion_defects(rep, include_stage_check=False)
        if defects:
            r.fail("structural", defects[0][0], defects[0][1], defects[0][2],
                   f"{len(defects)} frozen-completion defect(s): {[d[0] for d in defects]}")

    # Bootstrap (L2 m3 r4 item 1): the preflight — which verifies the stage declaration itself — runs
    # UNCONDITIONALLY, independent of the mutable STAGES tuple. No declared stage name is consulted
    # or indexed before the static check has established STAGES == FROZEN_B2["stages"].
    _boundary("preflight", _preflight)
    if rep.failure is not None:
        return rep
    rep.stages_completed.append("preflight")
    stage_fns = {"wrapper_verification": _wrapper, "ensembles": _ensembles, "completion": _completion}
    for name in tuple(STAGES)[1:]:                       # verified by the preflight to equal the frozen remainder
        fn = stage_fns.get(name)
        if fn is None:                                   # unreachable after the static check; fail closed anyway
            r.stage = "driver"; r.cell = name
            r.fail("structural", "static_stages", repr(list(FROZEN_B2["stages"])), repr(list(STAGES)),
                   f"unknown stage {name!r} reached the driver")
        _boundary(name, fn)
        if rep.failure is not None:
            return rep
        rep.stages_completed.append(name)
    return rep
