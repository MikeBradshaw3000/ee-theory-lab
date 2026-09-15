"""gates/gate_b/b1.py — B1: deterministic rule-equivalence (Gate B Specification v0.4,
FROZEN 2026-09-04; §3 of the v0.2 base as amended by v0.3 A1).

Form (inherited from Lineage B's own parity pattern): identical inputs to candidate and
reference; per-output comparison with the FROZEN comparator set; fail-fast halt with an
atomic failure record. The candidate is exercised through the instrument's PUBLIC
dispatch — a `Dynamics` constructed with rule_mode="become_survive" (Q-disabled) and
stepped through `Dynamics.step` — never by calling the private branch; its draws are
supplied by the counted frozen-sequence stub through `DynamicsStream`. The reference is
the pinned module's own `step_tcop_core` (digest-verified, isolated import; the verified
bytes are the bytes executed). The harness contains no re-transcription of B's rule.

FROZEN battery map (exact; `passed` requires equality with it, in this stage order — the
gate itself refuses a narrowed or reordered battery, independent of any test runner):
  single_step        486   G(9) × U(6) × K(9), one declared rand_grid per grid
  threshold_witness   27   3 grids × 3 (u,κ) × {below, equal, above}
  stencil_motif      108   3 centers × counts 0–8 × {center inactive, active} × 2 (u,κ)
  chained            150   25 + 25 + 75 + 25 ticks, one frozen grid per tick
  schedule_table    4000   10 declared schedules × every tick 0–399 (per-tick, v0.3 A1)

Comparators per case bundle: sink field family exact; rand_grid identity (raw bits);
p_become raw bits; g_q raw bits (ancestor-DERIVED diagnostic: the ancestor's own
get_neighbor_count and its L267-268 expression — not an independent certification of the
ancestor's g_q arithmetic); next-state exact after canonicalizing the ANCESTOR to bool;
stub consumption asserted after every case; scalar p_survive bits == ancestor LAMBDA once,
before any case. The ancestor-pattern allclose (rtol=1e-5, atol=1e-8, named) is computed and
reported as a DIAGNOSTIC for every float comparison; it never enters the verdict.

Failure grammar (v0.4 §7): every failure class — reference (absence/digest/commit/import),
environment, provenance, scalar, comparator dtype/shape, stub count/shape/exhaustion/surplus,
sink field family, and any unexpected exception inside a battery — is converted by one
stage-aware boundary into the same `FailureRecord`, which is WRITTEN ATOMICALLY (temp file +
fsync + rename) by this module when `record_dir` is given. No success artifact is ever
written by this module.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import random as _pyrandom
import subprocess
import tempfile
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from ...config import RunConfig, InitConfig, DynamicsConstants
from ...dynamics import Dynamics
from ...init import GridState
from ...rng import DynamicsStream
from .comparators import (ALLCLOSE_ATOL, ALLCLOSE_RTOL, ComparatorError, raw_bits_differ,
                          scalar_bits, scalar_bits_equal, state_mismatches)
from .environment import (EXPECTED_LOCK_SHA256, EnvironmentCheckError, EnvironmentRecord,
                          check_environment)
from .reference import (EXPECTED_SHA256 as REFERENCE_SHA256, PINNED_COMMIT, PINNED_RELPATH,
                        PinnedReference, ReferenceError, load_pinned_reference)
from .stub import FrozenSequenceGenerator, StubError

GRID = 50
N_CELLS = GRID * GRID
INIT_ACTIVE = 250
PARITY_SEED = 0x7A9B31C
U_SET = (0.0, 0.05, 0.10, 0.125, 0.25, 0.50)
BERN_RHOS = (0.05, 0.10, 0.40, 0.60, 0.95)
WITNESS_UK = ((0.0, 0.0), (0.25, 0.4221), (0.10, -0.2090))
MOTIF_UK = ((0.0, 0.4221), (0.25, -0.4221))
SCHEDULE_CM0_UCONST = (0.0, 0.05, 0.10, 0.125, 0.25, 0.50)
SCHEDULE_CM1_TIERS = (0.0, 0.10, 0.25, 0.50)
SCHEDULE_TICKS = 400
EXPECTED_SINK_FIELDS = frozenset({"g_q", "p_become", "rand_grid", "is_active", "Psi_local"})
FROZEN_BATTERIES: Tuple[Tuple[str, int], ...] = (("single_step", 486), ("threshold_witness", 27),
                                                  ("stencil_motif", 108), ("chained", 150),
                                                  ("schedule_table", 4000))
# Frozen completion totals (L2 r2 items 9/12): 771 dynamic cases × 4 comparators + 4,000 u_t + 1 p_survive.
FROZEN_COMPARATOR_EVALS = 771 * 4 + 4000 + 1          # 7085
FROZEN_DIAG_EVALS = 771 * 3 + 4000 + 1                # 6314: allclose on every float comparison
FROZEN_COMPARATOR_EVALS_PER_BATTERY = {"preflight": 1, "single_step": 486 * 4, "threshold_witness": 27 * 4,
                                       "stencil_motif": 108 * 4, "chained": 150 * 4, "schedule_table": 4000}
SPEC_VERSION = "GATE_B_SPECIFICATION_v0_4 (FROZEN 2026-09-04)"
SPEC_SHA256 = "e2f06bb1ad0aaa7ff05cc3da4b69c4b87bbad5c54bb7cafc4e78d4ee029e7fbd"
COMPARATOR_VERSION = "raw-float64-bit / dtype-canonical-state / allclose-diagnostic(1e-5,1e-8), v0.4"


# ----------------------------------------------------------------------------- records
class ProvenanceError(RuntimeError):
    """Typed candidate-provenance failure naming the exact sub-check that failed."""
    def __init__(self, check: str, message: str) -> None:
        super().__init__(message)
        self.check = check


class GateBFailure(RuntimeError):
    """Carries a FailureRecord; the single exception type the stage boundary raises."""
    def __init__(self, record: "FailureRecord") -> None:
        super().__init__(record.summary())
        self.record = record


@dataclass
class FailureRecord:
    failure_class: str      # reference | environment | provenance | scalar | comparator | stub | field_family | structural | internal
    battery: str
    case_id: str
    comparator: str
    mismatches: int
    expected_bits: str
    observed_bits: str
    detail: str
    environment: str
    environment_record: Optional[Dict[str, Any]]      # the COMPLETE EnvironmentRecord (L2 r2 10A)
    provenance: Dict[str, Any]                        # accumulated stage by stage (10B)
    stages_completed: List[str]
    cases_compared_before_halt: int
    comparator_evaluations_before_halt: int
    written_to: Optional[str] = None

    def summary(self) -> str:
        return (f"B1 HALT [{self.failure_class}] battery={self.battery} case={self.case_id} "
                f"comparator={self.comparator} mismatches={self.mismatches} expected={self.expected_bits} "
                f"observed={self.observed_bits} detail={self.detail!r} env={self.environment} "
                f"stages_completed={self.stages_completed} cases_before_halt={self.cases_compared_before_halt}")


@dataclass
class B1Report:
    label: str
    environment: str
    environment_record: Optional[Dict[str, Any]]
    provenance: Dict[str, Any]
    batteries: Dict[str, int] = field(default_factory=dict)      # battery -> case bundles compared
    cases_compared: int = 0
    comparator_evaluations: int = 0
    comparator_evaluations_by_battery: Dict[str, int] = field(default_factory=dict)
    allclose_diagnostic: Dict[str, int] = field(default_factory=lambda: {"true": 0, "false": 0})
    failure: Optional[FailureRecord] = None
    stages_completed: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Exact frozen battery map, in stage order, fully completed, no failure — encoded in
        the gate itself, not delegated to a test runner (L2 B8)."""
        return (self.failure is None
                and list(self.batteries.items()) == list(FROZEN_BATTERIES)
                and self.stages_completed == [n for n, _ in FROZEN_BATTERIES]
                and self.cases_compared == sum(n for _, n in FROZEN_BATTERIES)
                and self.comparator_evaluations == FROZEN_COMPARATOR_EVALS
                and self.comparator_evaluations_by_battery == FROZEN_COMPARATOR_EVALS_PER_BATTERY
                and sum(self.allclose_diagnostic.values()) == FROZEN_DIAG_EVALS)

    def summary(self) -> str:
        s = " ".join(f"{k}={v}" for k, v in self.batteries.items())
        return (f"B1[{self.label}] {s} cases={self.cases_compared} comparator_evals={self.comparator_evaluations} "
                f"allclose_diag={self.allclose_diagnostic} env={self.environment} "
                + ("=> PASS" if self.passed else f"=> FAIL ({self.failure.summary() if self.failure else 'incomplete battery map'})"))


def write_failure_record_atomically(record: FailureRecord, record_dir: str) -> str:
    """Temp file in the target directory, fsync, rename: the record either exists complete or
    does not exist at all."""
    os.makedirs(record_dir, exist_ok=True)
    final = os.path.join(record_dir, f"gate_b_b1_failure_{time.time_ns()}_{os.getpid()}_{uuid.uuid4().hex[:8]}.json")
    fd, tmp = tempfile.mkstemp(dir=record_dir, prefix=".b1_failure_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(asdict(record), fh, indent=1, default=str)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, final)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return final


# ----------------------------------------------------------------------------- helpers
def _bits_at(x: np.ndarray, idx: Tuple[int, ...]) -> str:
    v = np.asarray(x, dtype=np.float64)[idx] if idx else np.asarray(x, dtype=np.float64)
    return f"0x{int(np.asarray(v).view(np.uint64)):016x}"


def _first_diff_index(a: np.ndarray, b: np.ndarray) -> Tuple[int, ...]:
    d = np.argwhere(np.ascontiguousarray(a).view(np.uint64) != np.ascontiguousarray(b).view(np.uint64))
    return tuple(int(i) for i in d[0]) if len(d) else ()


def candidate_provenance(instrument_root: str, sink: Dict[str, Any]) -> None:
    """Fail closed (L2 B2) and ACCUMULATE (L2 r3 3B): each identity is written into `sink` the
    moment it is earned, so a later sub-check failure loses nothing already measured. Each
    sub-check raises a typed ProvenanceError naming itself: `candidate_git` for git-command
    failures, `candidate_dynamics_sha256` for candidate-source read/hash failures."""
    def git(*args: str) -> str:
        try:
            out = subprocess.run(["git", "-C", instrument_root, *args], capture_output=True, text=True)
        except OSError as e:
            raise ProvenanceError("candidate_git", f"candidate provenance: git unavailable: {e}") from e
        if out.returncode != 0:
            raise ProvenanceError("candidate_git", f"candidate provenance: git {' '.join(args)} failed: "
                                                   f"{out.stderr.strip() or out.returncode}")
        return out.stdout.strip()
    sink["candidate_commit"] = git("rev-parse", "HEAD")
    sink["candidate_worktree_dirty"] = bool(git("status", "--porcelain"))
    dyn_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "dynamics.py")
    try:
        sink["candidate_dynamics_sha256"] = hashlib.sha256(open(dyn_path, "rb").read()).hexdigest()
    except OSError as e:
        raise ProvenanceError("candidate_dynamics_sha256",
                              f"candidate provenance: dynamics.py unreadable: {e}") from e


def reference_init_grid(ref: PinnedReference, seed: int) -> np.ndarray:
    """B's own initialization (execute_run L488-494) under the legacy-global regime, with BOTH
    NumPy and Python `random` global states saved and restored in `finally` (L2 B3)."""
    np_state = np.random.get_state()
    py_state = _pyrandom.getstate()
    try:
        np.random.seed(seed)
        _pyrandom.seed(seed)
        flat = np.zeros(N_CELLS, dtype=int)
        flat[:INIT_ACTIVE] = 1
        np.random.shuffle(flat)
        return flat.reshape((GRID, GRID))
    finally:
        np.random.set_state(np_state)
        _pyrandom.setstate(py_state)


def _bern_grid(rho: float, rng: np.random.Generator) -> np.ndarray:
    return (rng.random((GRID, GRID)) < rho).astype(int)


def _grid_set(ref: PinnedReference, rng: np.random.Generator) -> List[Tuple[str, np.ndarray]]:
    gs: List[Tuple[str, np.ndarray]] = [("all_inactive", np.zeros((GRID, GRID), int)),
                                        ("all_active", np.ones((GRID, GRID), int)),
                                        ("b_init_42", reference_init_grid(ref, 42)),
                                        ("b_init_137", reference_init_grid(ref, 137))]
    for rho in BERN_RHOS:
        gs.append((f"bern_{rho:.2f}", _bern_grid(rho, rng)))
    return gs


def _kappa_set(ref: PinnedReference) -> Tuple[float, ...]:
    """The frozen K set is the κ member (second element) of each committed KAPPA_MAP pair."""
    return tuple(float(k) for (_, k) in ref.KAPPA_MAP)


def _protect(a: np.ndarray) -> np.ndarray:
    c = np.ascontiguousarray(a).copy(); c.setflags(write=False); return c


def _candidate(cfg: RunConfig, grid: np.ndarray, grids: Sequence[np.ndarray]) -> Tuple[Dynamics, FrozenSequenceGenerator]:
    """Fresh model per case: bases are inert float64 fill (the B rule reads no bases; N3 ruling);
    state from `grid`; draws from the counted stub via the instrument's own construction path."""
    fill = np.full((cfg.grid_scale, cfg.grid_scale), 0.5)
    state = GridState(v=fill.copy(), u_base=fill.copy(), r=fill.copy(), is_active=grid.astype(bool))
    stub = FrozenSequenceGenerator(grids, cfg.grid_scale)
    return Dynamics(cfg, state, DynamicsStream(generator=stub)), stub


def _cfg(ref: PinnedReference, kappa: float, schedule: Tuple[Tuple[int, float], ...], ticks: int) -> RunConfig:
    return RunConfig(seed=1, rule_mode="become_survive", grid_scale=GRID, ticks=ticks,
                     init=InitConfig(scheme="fixed_count", fixed_count=INIT_ACTIVE),
                     constants=DynamicsConstants(logit_l=float(ref.LOGIT_L), kappa=float(kappa),
                                                 p_survive=float(ref.LAMBDA)),
                     drive_schedule=schedule)


def _ancestor_g_q(ref: PinnedReference, grid: np.ndarray) -> np.ndarray:
    neighbors = ref.get_neighbor_count(grid)
    q_i = neighbors / 8.0
    return 2.0 * q_i - 1.0


def _cm1_schedule(tier: float) -> Tuple[Tuple[int, float], ...]:
    return tuple((b * 25, (0.0, tier / 2.0, tier)[b % 3]) for b in range(16))


class _ConsumedSoFar:
    """Per-tick consumption view for chained cases: exactly `expected` draws so far."""
    def __init__(self, stub: FrozenSequenceGenerator, expected: int) -> None:
        self._stub = stub; self._expected = expected
    def assert_consumed(self) -> None:
        if self._stub.total_draws != self._expected:
            raise StubError(f"expected {self._expected} draws so far, saw {self._stub.total_draws}")


# ----------------------------------------------------------------------------- runner
class _Runner:
    def __init__(self, rep: B1Report) -> None:
        self.ref: Optional[PinnedReference] = None
        self.rep = rep
        self.battery = "preflight"; self.case_id = "-"

    def fail(self, failure_class: str, comparator: str, mismatches: int, expected: str, observed: str,
             detail: str = "") -> None:
        rec = FailureRecord(failure_class=failure_class, battery=self.battery, case_id=self.case_id,
                            comparator=comparator, mismatches=int(mismatches), expected_bits=expected,
                            observed_bits=observed, detail=detail, environment=self.rep.environment,
                            environment_record=self.rep.environment_record,
                            provenance=dict(self.rep.provenance), stages_completed=list(self.rep.stages_completed),
                            cases_compared_before_halt=self.rep.cases_compared,
                            comparator_evaluations_before_halt=self.rep.comparator_evaluations)
        self.rep.failure = rec
        raise GateBFailure(rec)

    def classify_and_fail(self, exc: BaseException) -> None:
        """Every exception reaching the stage boundary becomes the same failure grammar."""
        if isinstance(exc, GateBFailure):
            raise exc
        if isinstance(exc, EnvironmentCheckError):
            self.fail("environment", "frozen_pin_source", 1, "", "", str(exc))
        if isinstance(exc, ReferenceError):
            self.fail("reference", "reference_load", 1, "", "", str(exc))
        if isinstance(exc, StubError):
            self.fail("stub", "frozen_sequence_stub", 1, "", "", str(exc))
        if isinstance(exc, ComparatorError):
            self.fail("comparator", "comparator_contract", 1, "", "", str(exc))
        if isinstance(exc, ProvenanceError):
            self.fail("provenance", exc.check, 1, "", "", str(exc))
        self.fail("internal", "unexpected_exception", 1, "", "", f"{type(exc).__name__}: {exc}")

    def _eval(self) -> None:
        self.rep.comparator_evaluations += 1
        self.rep.comparator_evaluations_by_battery[self.battery] = self.rep.comparator_evaluations_by_battery.get(self.battery, 0) + 1

    def _diag(self, a, b) -> None:
        """One comparator evaluation + the frozen allclose diagnostic (arrays or scalars)."""
        self._eval()
        key = "true" if np.allclose(a, b, rtol=ALLCLOSE_RTOL, atol=ALLCLOSE_ATOL) else "false"
        self.rep.allclose_diagnostic[key] += 1

    def compare_case(self, case_id: str, grid: np.ndarray, rand: np.ndarray, cand: Dict[str, np.ndarray],
                     ref_next: np.ndarray, ref_p: np.ndarray, consumed) -> None:
        self.case_id = case_id
        have = frozenset(cand)
        if have != EXPECTED_SINK_FIELDS:                           # named field-family check (L2 B10)
            self.fail("field_family", "sink_field_family", 1, repr(sorted(EXPECTED_SINK_FIELDS)), repr(sorted(have)),
                      f"missing={sorted(EXPECTED_SINK_FIELDS - have)} extra={sorted(have - EXPECTED_SINK_FIELDS)}")
        n = raw_bits_differ(cand["rand_grid"], rand); self._diag(cand["rand_grid"], rand)
        if n:
            i = _first_diff_index(cand["rand_grid"], rand)
            self.fail("comparator", "rand_grid_identity", n, _bits_at(rand, i), _bits_at(cand["rand_grid"], i))
        n = raw_bits_differ(cand["p_become"], ref_p); self._diag(cand["p_become"], ref_p)
        if n:
            i = _first_diff_index(cand["p_become"], ref_p)
            self.fail("comparator", "p_become_bits", n, _bits_at(ref_p, i), _bits_at(cand["p_become"], i))
        g_ref = _ancestor_g_q(self.ref, grid)
        n = raw_bits_differ(cand["g_q"], g_ref); self._diag(cand["g_q"], g_ref)
        if n:
            i = _first_diff_index(cand["g_q"], g_ref)
            self.fail("comparator", "g_q_bits", n, _bits_at(g_ref, i), _bits_at(cand["g_q"], i))
        n = state_mismatches(cand["is_active"], ref_next); self._eval()
        if n:
            self.fail("comparator", "is_active_exact", n, "ancestor next-state", "candidate next-state")
        consumed.assert_consumed()                                  # per case (L2 B9)
        self.rep.cases_compared += 1

    def step_case(self, case_id: str, cfg: RunConfig, grid: np.ndarray, u_t: float, kappa: float,
                  rand: np.ndarray) -> None:
        self.case_id = case_id                       # BEFORE the step: a stub/candidate failure inside
        model, stub = _candidate(cfg, grid, [_protect(rand)])   # model.step carries the true case identity (§7)
        captured: Dict[str, np.ndarray] = {}
        model.step(lambda tick, fields: captured.update({k: np.asarray(v) for k, v in fields.items()}))
        ref_next, ref_p = self.ref.step_tcop_core(grid, u_t, kappa, _protect(rand))
        self.compare_case(case_id, grid, rand, captured, ref_next, ref_p, stub)


# ----------------------------------------------------------------------------- batteries
def _battery_single_step(r: _Runner, rng: np.random.Generator) -> int:
    ref = r.ref; count = 0
    for gname, grid in _grid_set(ref, rng):
        rand = rng.random((GRID, GRID))
        for u in U_SET:
            for k in _kappa_set(ref):
                r.step_case(f"{gname}|u={u}|k={k:+.4f}", _cfg(ref, k, ((0, u),), 1), grid, u, k, rand); count += 1
    return count


def _battery_threshold_witnesses(r: _Runner, rng: np.random.Generator) -> int:
    ref = r.ref; count = 0
    grids = [("all_inactive", np.zeros((GRID, GRID), int)), ("bern_0.40", _bern_grid(0.40, rng)),
             ("b_init_42", reference_init_grid(ref, 42))]
    for gname, grid in grids:
        for (u, k) in WITNESS_UK:
            cfg = _cfg(ref, k, ((0, u),), 1)
            _, p = ref.step_tcop_core(grid, u, k, rng.random((GRID, GRID)))
            thresh = np.where(grid == 1, float(ref.LAMBDA), p)
            for wname, rand in (("below", np.nextafter(thresh, -np.inf)), ("equal", thresh.copy()),
                                ("above", np.nextafter(thresh, np.inf))):
                r.step_case(f"{gname}|u={u}|k={k:+.4f}|{wname}", cfg, grid, u, k, rand); count += 1
    return count


def _motif_grid(center: Tuple[int, int], count: int, center_active: bool) -> np.ndarray:
    g = np.zeros((GRID, GRID), int); cx, cy = center
    for (dx, dy) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)][:count]:
        g[(cx + dx) % GRID, (cy + dy) % GRID] = 1
    g[cx, cy] = 1 if center_active else 0
    return g


def _battery_stencil_motifs(r: _Runner, rng: np.random.Generator) -> int:
    ref = r.ref; count = 0
    for cname, center in (("interior", (25, 25)), ("corner_wrap", (0, 0)), ("edge_wrap", (0, 25))):
        for n in range(9):
            for active in (False, True):
                grid = _motif_grid(center, n, active)
                nc = int(ref.get_neighbor_count(grid)[center])
                if nc != n:
                    r.case_id = f"{cname}|n={n}|center_active={active}"
                    r.fail("internal", "motif_construction", 1, str(n), str(nc), "motif realized wrong neighbor count")
                rand = rng.random((GRID, GRID))
                for (u, k) in MOTIF_UK:
                    r.step_case(f"{cname}|n={n}|center_active={active}|u={u}|k={k:+.4f}",
                                _cfg(ref, k, ((0, u),), 1), grid, u, k, rand); count += 1
    return count


def _battery_chained(r: _Runner, rng: np.random.Generator) -> int:
    ref = r.ref; count = 0
    seqs = [("a_cm0_pos", reference_init_grid(ref, 42), 25, 0.4221, ((0, 0.25),), lambda t: 0.25),
            ("b_cm0_neg", _bern_grid(0.10, rng), 25, -0.4221, ((0, 0.25),), lambda t: 0.25),
            ("c_cm1_cycle", reference_init_grid(ref, 42), 75, 0.4221, ((0, 0.0), (25, 0.125), (50, 0.25)),
             lambda t: float(ref.u_t_for("cm1", 0.25, 0.0, t // 25))),
            ("d_survival_only", np.ones((GRID, GRID), int), 25, 0.0, ((0, 0.0),), lambda t: 0.0)]
    for name, grid0, ticks, k, schedule, u_of in seqs:
        grids = [_protect(rng.random((GRID, GRID))) for _ in range(ticks)]
        model, stub = _candidate(_cfg(ref, k, schedule, ticks), grid0, grids)
        grid = grid0.copy()
        for t in range(ticks):
            u = u_of(t)
            r.case_id = f"{name}|t={t}|u={u}|k={k:+.4f}"     # BEFORE the step (§7 first-failing-case identity)
            captured: Dict[str, np.ndarray] = {}
            model.step(lambda tick, fields: captured.update({kk: np.asarray(v) for kk, v in fields.items()}))
            ref_next, ref_p = ref.step_tcop_core(grid, u, k, grids[t])
            r.compare_case(f"{name}|t={t}|u={u}|k={k:+.4f}", grid, grids[t], captured, ref_next, ref_p,
                           _ConsumedSoFar(stub, t + 1))
            grid = np.asarray(ref_next).astype(int)
            stub.next_tick(); count += 1
        stub.assert_consumed()
    return count


def _battery_schedule_table(r: _Runner) -> int:
    """Per-tick (v0.3 A1; L2 B4): every tick 0–399 of every declared schedule, raw-bit equality."""
    ref = r.ref; count = 0
    checks: List[Tuple[str, Tuple[Tuple[int, float], ...], str, float, float]] = []
    for uc in SCHEDULE_CM0_UCONST:
        checks.append((f"cm0|u_const={uc}", ((0, uc),), "cm0", 0.0, uc))
    for tier in SCHEDULE_CM1_TIERS:
        checks.append((f"cm1|tier={tier}", _cm1_schedule(tier), "cm1", tier, 0.0))
    for name, schedule, mode, tier, uc in checks:
        model, _ = _candidate(_cfg(ref, 0.0, schedule, SCHEDULE_TICKS), np.zeros((GRID, GRID), int), [])
        for tick in range(SCHEDULE_TICKS):
            r.case_id = f"{name}|tick={tick}"
            cand_u = float(model._u_t(tick))                    # the candidate's schedule function (adjudicated)
            ref_u = float(ref.u_t_for(mode, tier, uc, tick // 25))
            r._diag(cand_u, ref_u)                              # scalar diagnostic too (L2 r2 item 9)
            if not scalar_bits_equal(cand_u, ref_u):
                r.fail("comparator", "u_t_bits", 1, scalar_bits(ref_u), scalar_bits(cand_u))
            r.rep.cases_compared += 1; count += 1
    return count


# ----------------------------------------------------------------------------- entry
def run_b1(pinned_root: str, label: str = "PROVISIONAL", load_mode: str = "EXTRACTION",
           record_dir: Optional[str] = None, qualification: bool = False) -> B1Report:
    if (label == "AUTHORITATIVE" or qualification) and record_dir is None:
        raise ValueError("AUTHORITATIVE and formal-qualification Gate B runs require a persistent "
                         "failure-record owner: record_dir is mandatory (refused before start)")
    env_str = f"python{platform.python_version()}/numpy{np.__version__}"
    # Provenance ACCUMULATES: expected identities first, then each earned identity in turn (L2 r2 10B).
    prov: Dict[str, Any] = {"label": label, "load_mode": load_mode, "environment": env_str,
                            "expected": {"reference_commit": PINNED_COMMIT, "reference_relpath": PINNED_RELPATH,
                                         "reference_sha256": REFERENCE_SHA256, "lock_sha256": EXPECTED_LOCK_SHA256,
                                         "pinned_root_arg": os.path.realpath(pinned_root)},
                            "spec": SPEC_VERSION, "spec_sha256": SPEC_SHA256, "comparators": COMPARATOR_VERSION}
    rep = B1Report(label=label, environment=env_str, environment_record=None, provenance=prov)
    r = _Runner(rep)

    def _boundary(stage: str, fn: Callable[[], Any]) -> Any:
        r.battery = stage
        try:
            return fn()
        except BaseException as e:                 # noqa: BLE001 — the boundary converts everything
            try:
                r.classify_and_fail(e)
            except GateBFailure as gf:
                if record_dir is not None:
                    gf.record.written_to = write_failure_record_atomically(gf.record, record_dir)
                return None

    def _preflight() -> None:
        r.case_id = "environment"
        envrec: EnvironmentRecord = check_environment(pinned_root)
        rep.environment_record = asdict(envrec)
        prov["environment_conforms"] = envrec.conforms
        if label == "AUTHORITATIVE" and not envrec.conforms:
            r.fail("environment", "frozen_environment", len(envrec.failures), "conforming", "non-conforming",
                   "; ".join(envrec.failures))
        if label == "AUTHORITATIVE" and load_mode != "FULL":
            r.fail("environment", "load_mode", 1, "FULL", load_mode, "AUTHORITATIVE requires FULL reference import")
        r.case_id = "reference"
        r.ref = load_pinned_reference(pinned_root, load_mode, label)
        prov["reference"] = asdict(r.ref.provenance)
        r.case_id = "candidate_provenance"
        inst_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        candidate_provenance(inst_root, prov)          # accumulates in place; partial on failure
        r.case_id = "p_survive"
        cand_ps = _cfg(r.ref, 0.0, ((0, 0.0),), 1).constants.p_survive
        r._diag(cand_ps, float(r.ref.LAMBDA))                  # scalar diagnostic (L2 r2 item 9)
        if not scalar_bits_equal(cand_ps, r.ref.LAMBDA):
            r.fail("scalar", "p_survive_bits", 1, scalar_bits(r.ref.LAMBDA), scalar_bits(cand_ps))

    _boundary("preflight", _preflight)
    if rep.failure is not None:
        return rep
    rng = np.random.default_rng(PARITY_SEED)
    for name, fn in (("single_step", lambda: _battery_single_step(r, rng)),
                     ("threshold_witness", lambda: _battery_threshold_witnesses(r, rng)),
                     ("stencil_motif", lambda: _battery_stencil_motifs(r, rng)),
                     ("chained", lambda: _battery_chained(r, rng)),
                     ("schedule_table", lambda: _battery_schedule_table(r))):
        count = _boundary(name, fn)
        if rep.failure is not None:
            return rep                             # fail-fast: nothing downstream
        rep.batteries[name] = int(count)
        rep.stages_completed.append(name)

    def _completion() -> None:
        """Structural completion (L2 r2 10D/12): an incomplete, narrowed, or reordered frozen
        battery, or a missing comparator/diagnostic invocation, is a certification failure in
        the common grammar — never a silent passed=False."""
        r.case_id = "frozen_completion"
        if list(rep.batteries.items()) != list(FROZEN_BATTERIES) or rep.stages_completed != [n for n, _ in FROZEN_BATTERIES]:
            r.fail("structural", "battery_map", 1, repr(list(FROZEN_BATTERIES)), repr(list(rep.batteries.items())),
                   "battery map or stage order differs from the frozen map")
        if rep.cases_compared != sum(n for _, n in FROZEN_BATTERIES):
            r.fail("structural", "case_total", 1, str(sum(n for _, n in FROZEN_BATTERIES)), str(rep.cases_compared))
        if rep.comparator_evaluations != FROZEN_COMPARATOR_EVALS or rep.comparator_evaluations_by_battery != FROZEN_COMPARATOR_EVALS_PER_BATTERY:
            r.fail("structural", "comparator_set_completion", 1, f"{FROZEN_COMPARATOR_EVALS} {FROZEN_COMPARATOR_EVALS_PER_BATTERY}",
                   f"{rep.comparator_evaluations} {rep.comparator_evaluations_by_battery}")
        if sum(rep.allclose_diagnostic.values()) != FROZEN_DIAG_EVALS:
            r.fail("structural", "diagnostic_completion", 1, str(FROZEN_DIAG_EVALS), str(sum(rep.allclose_diagnostic.values())))
    _boundary("completion", _completion)
    return rep
