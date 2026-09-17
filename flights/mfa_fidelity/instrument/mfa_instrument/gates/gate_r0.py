"""mfa_instrument/gates/gate_r0.py — Gate R0: projection-bridge implementation correctness
(Merge Specification v0.4 FROZEN §8.3; R0 design note 2026-09-16; departure-statistic set
DECLARED by Mike 2026-09-16).

R0 is instrument validation. It proves that the instrument (symmetric_chain path, driven through
the PUBLIC Dynamics.step) and the projection bridge (`mfa_instrument/bridge.py`) compute the four
projection quantities correctly on constructed cases whose answers are known BEFORE anything runs:

  Q1  the local quantity Q reads      Local_Density (Moore count / 8); rho_global under global read
  Q2  aggregate rho(t)                 the pre-update grid mean, persisted per tick
  Q3  the population-aggregated Q response   delta_b decomposition, clipped bases, clip counters, means
  Q4  the declared departure statistics       local-read dispersion; configuration–neighbourhood
                                              correlation and Moran's I; base-distribution dispersion

Expectations are computed by an INDEPENDENT exact-rational path (`Fraction`, brute-force loops over
cells, the frozen definitions transcribed here) and compared to the instrument's emitted fields and
the bridge's outputs by RAW FLOAT64 BIT EQUALITY. Constructed cases use a 16x16 grid and dyadic
values so every exact answer is representable and every bridge computation is exact sums followed
by one correctly rounded division — which is what makes bit equality against float(Fraction) a
legitimate comparator rather than a coincidence. Undefined statistics are required to be REFUSED.

Frozen case map (`FROZEN_R0`, immutable, bound to a literal digest) drives what runs; `passed` is
defined against the separate FROZEN_COMPLETION and FROZEN_LEDGER literals, each bound to its own
literal digest; a narrowed, reordered, or substituted execution is a structural failure. Fail-fast with an atomic failure record; the failure grammar,
environment check, label discipline, and record ownership follow Gate B. All writers use LF newlines.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import tempfile
import time
import uuid
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

import ast
import types
from .. import bridge as BR
from .. import verify as VERIFY
from ..config import RunConfig, InitConfig, DynamicsConstants, QConfig
from ..dynamics import Dynamics
from ..init import GridState
from ..rng import DynamicsStream
from ..telemetry import TelemetryWriter
from .gate_b.b1 import ProvenanceError, candidate_provenance
from .gate_b.comparators import ComparatorError, raw_bits_differ, scalar_bits_equal, scalar_bits
from .gate_b.environment import EnvironmentCheckError, EnvironmentRecord, check_environment
from .gate_b.stub import FrozenSequenceGenerator, StubError

R0_VERSION = "gate_r0_v3 / Merge Spec v0.4 FROZEN section 8.3 / departure set declared 2026-09-16"
# R0's OWN governing identities (L2 R0 r2 10A) — never Gate B's specification constants.
R0_GOVERNING = types.MappingProxyType({
    "merge_specification": "MERGE_SPECIFICATION_v0_4_FROZEN.md",
    "merge_specification_sha256": "39f66673657b0f429691c908142f889d9ef3d463a8372455cba95db7c486f52a",   # committed blob at 60bdd9c
    "r0_design_declaration": "DESIGN_NOTE_GATE_R0.md (departure set DECLARED by Mike 2026-09-16)",
    "r0_design_declaration_sha256": "08a503ec145bd076661341703f51e78f0045816fbe06d5380c39b303d6dd6031",
})
G = 16                                       # constructed-case grid (dyadic cell count)
N = G * G
GRID_MOTIF = 50                              # Gate B's motif grid for the local read

# ----------------------------------------------------------------------------- frozen case map
FROZEN_R0: Dict[str, Any] = {
    "grid": G, "n_cells": N, "motif_grid": GRID_MOTIF,
    "q1_grids": ("all_inactive", "all_active", "checkerboard", "row_stripes", "single_active", "two_by_two_block"),
    "q1_motifs": tuple((c, n) for c in ("interior", "corner_wrap", "edge_wrap") for n in range(9)),
    "q2_trajectories": (("draws_zero_from_quarter", "local"), ("draws_zero_from_quarter", "global"),
                        ("draws_one_from_half", "local"), ("draws_one_from_half", "global")),
    "q2_ticks": 4,
    "q3_cases": (("iso", "local", 0.25, 0.5, "high"), ("iso", "global", 0.25, 0.5, "high"),
                 ("row", "local", 0.03125, 0.0625, "none"), ("checker", "global", 0.03125, 0.0625, "none"),
                 ("sink", "local", 0.25, 0.5, "low"), ("sink", "global", 0.25, 0.5, "low")),
    "q4_dispersion": ("checkerboard", "row_stripes", "single_active", "two_by_two_block"),
    "q4_correlation": ("plus_one", "minus_one", "zero"),
    "q4_moran": ("checkerboard", "row_stripes", "single_active", "two_by_two_block"),
    "q4_moran_refused": ("all_inactive", "all_active"),
    "q4_base_dispersion": ("halves", "quarters"),
    "stages": ("preflight", "q1", "q2", "q3", "q4", "completion"),
}
# EXECUTION DECLARATION — a deliberately separate literal from FROZEN_R0. The stages read THIS; the
# preflight compares it to FROZEN_R0 before any output. Three frozen objects, three roles:
#   FROZEN_R0        — the case/execution declaration (what runs), bound to its literal digest;
#   FROZEN_COMPLETION — stage/check/evaluation/refusal completion (what "complete" means);
#   FROZEN_LEDGER    — the exact comparator surface (which checks, how many times, per stage).
# `passed` is computed from FROZEN_COMPLETION and FROZEN_LEDGER — never from FROZEN_R0 or R0_CASES —
# so a narrowed or reordered execution cannot narrow its own expectation.
R0_CASES: Dict[str, Any] = {
    "q1_grids": ("all_inactive", "all_active", "checkerboard", "row_stripes", "single_active", "two_by_two_block"),
    "q1_motifs": tuple((c, n) for c in ("interior", "corner_wrap", "edge_wrap") for n in range(9)),
    "q2_trajectories": (("draws_zero_from_quarter", "local"), ("draws_zero_from_quarter", "global"),
                        ("draws_one_from_half", "local"), ("draws_one_from_half", "global")),
    "q2_ticks": 4,
    "q3_cases": (("iso", "local", 0.25, 0.5, "high"), ("iso", "global", 0.25, 0.5, "high"),
                 ("row", "local", 0.03125, 0.0625, "none"), ("checker", "global", 0.03125, 0.0625, "none"),
                 ("sink", "local", 0.25, 0.5, "low"), ("sink", "global", 0.25, 0.5, "low")),
    "q4_dispersion": ("checkerboard", "row_stripes", "single_active", "two_by_two_block"),
    "q4_correlation": ("plus_one", "minus_one", "zero"),
    "q4_moran": ("checkerboard", "row_stripes", "single_active", "two_by_two_block"),
    "q4_moran_refused": ("all_inactive", "all_active"),
    "q4_base_dispersion": ("halves", "quarters"),
}
STAGES: Tuple[str, ...] = ("preflight", "q1", "q2", "q3", "q4", "completion")
LABELS = ("PROVISIONAL", "AUTHORITATIVE")
FROZEN_R0 = types.MappingProxyType(FROZEN_R0)          # immutable at rest
# INDEPENDENT LITERAL DIGEST of the frozen case map (L2 R7): recomputed from the runtime object and
# compared at every preflight, so a jointly narrowed FROZEN_R0/R0_CASES cannot redefine "complete".
FROZEN_R0_SHA256_LITERAL = "ce043d526a6e5c808c52ae797e9ee828daed79554ec725510114127f0610ced0"   # established from the frozen literal (amended 2026-09-16 for low-clip/distinct-base Q3); verified at every preflight


def frozen_map_digest(m) -> str:
    return hashlib.sha256(repr(sorted((k, repr(v)) for k, v in dict(m).items())).encode()).hexdigest()


# FROZEN COMPARATOR LEDGER (L2 R0 r2 item 8): the exact per-stage multiset of check names and invocation
# counts. Established by the run of 2026-09-16 and frozen; the completion gate requires EXACT equality —
# a missing, extra, renamed, moved, or one-for-one substituted comparator all refuse.
FROZEN_LEDGER = types.MappingProxyType({
    "q1": types.MappingProxyType({"Local_Density_bridge": 33, "Local_Density_instrument": 33, "rho_global_bridge": 6}),
    "q2": types.MappingProxyType({"cleared_verifier_rho_table": 4, "rho_global_pre_update": 16, "rho_global_table_dtypes": 4, "rho_global_table_persisted": 4, "rho_global_table_shape": 4, "rho_global_table_tick": 4, "rho_global_table_values": 4, "rho_tick_index": 16}),
    "q3": types.MappingProxyType({"Delta_from_Psi_bridge": 6, "Delta_from_Psi_instrument": 6, "Delta_from_rho_bridge": 6, "Delta_from_rho_instrument": 6, "Psi_local_instrument": 6, "clipped_r_bridge": 6, "clipped_r_count": 6, "clipped_u_base_bridge": 6, "clipped_u_base_count": 6, "clipped_v_bridge": 6, "clipped_v_count": 6, "delta_bridge": 6, "is_active_next_instrument": 6, "mean_delta_bridge": 6, "mean_delta_from_psi_bridge": 6, "mean_delta_from_rho_bridge": 6, "r_new_bridge": 6, "r_post_update": 6, "u_base_new_bridge": 6, "u_base_post_update": 6, "v_new_bridge": 6, "v_post_update": 6}),
    "q4": types.MappingProxyType({"base_mean_r": 2, "base_mean_u_base": 2, "base_mean_v": 2, "base_var_r": 2, "base_var_u_base": 2, "base_var_v": 2, "config_neighbourhood_correlation": 3, "correlation_refused_on_zero_variance": 1, "local_read_dispersion": 4, "morans_i": 4, "morans_i_refused_on_constant_grid": 2}),
})
FROZEN_LEDGER_SHA256_LITERAL = "1f512d4ed98ff207f133b5764f9a9db52a9c759f713494e1a884cd4c53622201"   # established 2026-09-16; verified at every preflight
FROZEN_COMPLETION_SHA256_LITERAL = "7b361c144d1201d80a9a19b5f831d7e744f1cf1aee5491a39b39b5d985cb0a15"   # established 2026-09-16
# FROZEN COMPLETION OBJECT (L2 R8): literal counts and identities, independent of any map.
FROZEN_COMPLETION = types.MappingProxyType({
    # established by the run of 2026-09-16 and frozen: Q1 6 grids×3 + 27 motifs×2; Q2 4 trajectories×(4 ticks + 1
    # persistence bundle); Q3 6 cases×22 (10 instrument + 12 bridge); Q4 4 + 3 + 4 + 2×6.
    "checks": types.MappingProxyType({"q1": 72, "q2": 20, "q3": 132, "q4": 23}),
    "comparator_evaluations": 283,        # = ledger total (286) − the 3 refusal invocations
    "refusals": ("morans_i_refused_on_constant_grid|all_inactive", "morans_i_refused_on_constant_grid|all_active",
                 "correlation_refused_on_zero_variance|constant"),
    "stages": ("preflight", "q1", "q2", "q3", "q4", "completion"),
    "grid": 16, "n_cells": 256, "motif_grid": 50,
})


# ----------------------------------------------------------------------------- constructions
def grid_named(name: str, g: int = G) -> np.ndarray:
    idx = np.indices((g, g))
    if name == "all_inactive": return np.zeros((g, g), bool)
    if name == "all_active": return np.ones((g, g), bool)
    if name == "checkerboard": return ((idx[0] + idx[1]) % 2).astype(bool)
    if name == "row_stripes": return (idx[0] % 2).astype(bool)
    if name == "single_active":
        a = np.zeros((g, g), bool); a[g // 2, g // 2] = True; return a
    if name == "two_by_two_block":
        a = np.zeros((g, g), bool); a[3:5, 3:5] = True; return a
    raise KeyError(name)


def motif_grid(center_name: str, count: int, g: int = GRID_MOTIF) -> Tuple[np.ndarray, Tuple[int, int]]:
    c = {"interior": (g // 2, g // 2), "corner_wrap": (0, 0), "edge_wrap": (0, g // 2)}[center_name]
    a = np.zeros((g, g), bool)
    for (dx, dy) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)][:count]:
        a[(c[0] + dx) % g, (c[1] + dy) % g] = True
    return a, c


# ----------------------------------------------------------------------------- exact expectations
# INDEPENDENT of bridge.py: Fractions, explicit loops, the frozen definitions transcribed.
_MOORE = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def exact_moore_count(grid: np.ndarray) -> List[List[int]]:
    g = grid.shape[0]
    return [[sum(int(grid[(i + dx) % g, (j + dy) % g]) for dx, dy in _MOORE) for j in range(g)] for i in range(g)]


def exact_local_density(grid: np.ndarray) -> List[List[Fraction]]:
    return [[Fraction(c, 8) for c in row] for row in exact_moore_count(grid)]


def exact_rho(grid: np.ndarray) -> Fraction:
    return Fraction(int(grid.sum()), grid.size)


def exact_dispersion(ld: List[List[Fraction]], rho: Fraction) -> Fraction:
    n = len(ld) * len(ld[0])
    return sum((x - rho) ** 2 for row in ld for x in row) / n


def exact_moran(grid: np.ndarray) -> Optional[Fraction]:
    g = grid.shape[0]; n = g * g
    xbar = Fraction(int(grid.sum()), n)
    d = [[Fraction(int(grid[i, j])) - xbar for j in range(g)] for i in range(g)]
    denom = sum(x * x for row in d for x in row)
    if denom == 0:
        return None
    num = Fraction(0)
    for i in range(g):
        for j in range(g):
            num += d[i][j] * sum(d[(i + dx) % g][(j + dy) % g] for dx, dy in _MOORE)
    return num / (8 * denom)                       # (N/W)·num/denom with W = 8N


def exact_base_stats(field_: List[List[Fraction]]) -> Tuple[Fraction, Fraction]:
    n = len(field_) * len(field_[0])
    m = sum(x for row in field_ for x in row) / n
    return m, sum((x - m) ** 2 for row in field_ for x in row) / n


def f(x: Fraction) -> float:
    return float(x)      # correctly rounded conversion of the exact rational


# ----------------------------------------------------------------------------- records
class R0Halt(RuntimeError):
    def __init__(self, record: "R0FailureRecord") -> None:
        super().__init__(record.summary()); self.record = record


@dataclass
class R0FailureRecord:
    failure_class: str          # environment | structural | comparator | domain | internal
    stage: str
    case_id: str
    check: str
    expected: str
    observed: str
    detail: str
    environment: str
    environment_record: Optional[Dict[str, Any]]
    provenance: Dict[str, Any]
    checks_completed: Dict[str, int]
    stages_completed: List[str]
    written_to: Optional[str] = None

    def summary(self) -> str:
        return (f"R0 HALT [{self.failure_class}] stage={self.stage} case={self.case_id} check={self.check} "
                f"expected={self.expected} observed={self.observed} detail={self.detail!r} stages={self.stages_completed}")


@dataclass
class R0Report:
    label: str
    environment: str
    environment_record: Optional[Dict[str, Any]]
    provenance: Dict[str, Any]
    checks: Dict[str, int] = field(default_factory=dict)          # stage -> comparisons made
    ledger: Dict[str, Dict[str, int]] = field(default_factory=dict)   # stage -> {check name: invocations}
    comparator_evaluations: int = 0
    refusals_verified: List[str] = field(default_factory=list)     # identities, not a count
    stages_completed: List[str] = field(default_factory=list)
    failure: Optional[R0FailureRecord] = None
    written_to: Optional[str] = None

    @property
    def passed(self) -> bool:
        """Against the FROZEN_COMPLETION literal only: exact check map (no extras), exact evaluation
        total, exact refusal identities and order, exact stage order."""
        C = FROZEN_COMPLETION
        return (self.failure is None and self.stages_completed == list(C["stages"])
                and dict(self.checks) == dict(C["checks"]) and self.comparator_evaluations == C["comparator_evaluations"]
                and list(self.refusals_verified) == list(C["refusals"])
                and {s: dict(v) for s, v in self.ledger.items()} == {s: dict(v) for s, v in FROZEN_LEDGER.items()})

    def summary(self) -> str:
        c = " ".join(f"{k}={v}" for k, v in self.checks.items())
        return (f"R0[{self.label}] {c} evals={self.comparator_evaluations} refusals={len(self.refusals_verified)} "
                f"env={self.environment} => {'PASS' if self.passed else 'FAIL'}" + (f" ({self.failure.summary()})" if self.failure else ""))


def _write_atomically(payload: Dict[str, Any], record_dir: str, prefix: str) -> str:
    os.makedirs(record_dir, exist_ok=True)
    final = os.path.join(record_dir, f"{prefix}_{time.time_ns()}_{os.getpid()}_{uuid.uuid4().hex[:8]}.json")
    fd, tmp = tempfile.mkstemp(dir=record_dir, prefix=f".{prefix}_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", newline="\n") as fh:
            json.dump(payload, fh, indent=1, default=str); fh.flush(); os.fsync(fh.fileno())
        os.replace(tmp, final)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return final


# ----------------------------------------------------------------------------- instrument driving
def _cfg(g: int, q_read: str, gamma_psi: float = 0.0, gamma_rho: float = 0.0, ticks: int = 8) -> RunConfig:
    return RunConfig(seed=1, rule_mode="symmetric_chain", grid_scale=g, ticks=ticks,
                     init=InitConfig(scheme="fixed_count", fixed_count=1),
                     q=QConfig(gamma_psi=gamma_psi, gamma_rho=gamma_rho, q_read=q_read),
                     drive_schedule=((0, 0.0),))


def _model(cfg: RunConfig, grid: np.ndarray, draws: List[np.ndarray], v, u, r) -> Tuple[Dynamics, FrozenSequenceGenerator]:
    state = GridState(v=np.array(v, dtype=np.float64), u_base=np.array(u, dtype=np.float64),
                      r=np.array(r, dtype=np.float64), is_active=grid.astype(bool))
    stub = FrozenSequenceGenerator(draws, cfg.grid_scale)
    return Dynamics(cfg, state, DynamicsStream(generator=stub), emit_rho_global=True), stub


def _step_capture(model: Dynamics) -> Dict[str, Any]:
    cap: Dict[str, Any] = {}
    model.step(lambda t, fl: cap.update({k: np.asarray(v) if hasattr(v, "shape") else v for k, v in fl.items()}) or cap.update({"_tick": t}))
    return cap


# ----------------------------------------------------------------------------- runner
class _R:
    def __init__(self, rep: R0Report) -> None:
        self.rep = rep; self.stage = "preflight"; self.case = "-"

    def fail(self, cls: str, check: str, expected: str, observed: str, detail: str = "") -> None:
        rec = R0FailureRecord(cls, self.stage, self.case, check, expected, observed, detail, self.rep.environment,
                              self.rep.environment_record, dict(self.rep.provenance), dict(self.rep.checks), list(self.rep.stages_completed))
        self.rep.failure = rec
        raise R0Halt(rec)

    def _ledger(self, check: str) -> None:
        """Every ledger entry is one comparator evaluation; the ledger IS the evaluation surface."""
        st = self.rep.ledger.setdefault(self.stage, {}); st[check] = st.get(check, 0) + 1

    def bits(self, check: str, observed: np.ndarray, expected: np.ndarray) -> None:
        self.rep.comparator_evaluations += 1; self._ledger(check)
        n = raw_bits_differ(np.asarray(observed, dtype=np.float64) if np.asarray(observed).dtype == np.float64 else np.asarray(observed), np.asarray(expected))
        if n:
            i = tuple(int(x) for x in np.argwhere(np.ascontiguousarray(observed).view(np.uint64) != np.ascontiguousarray(expected).view(np.uint64))[0])
            self.fail("comparator", check, f"{np.asarray(expected)[i]!r}", f"{np.asarray(observed)[i]!r}", f"{n} cells differ; first at {i}")
        self.rep.checks[self.stage] = self.rep.checks.get(self.stage, 0) + 1

    def scalar(self, check: str, observed, expected: float) -> None:
        """Noncoercive (L2 R5): the OBSERVED object goes to the dtype-first comparator as-is (a
        float32 or integer scalar is a comparator-contract failure, never promoted); expected is a
        Python float produced by float(Fraction)."""
        self.rep.comparator_evaluations += 1; self._ledger(check)
        if not isinstance(expected, float):
            self.fail("internal", check, "float expectation", type(expected).__name__)
        try:
            ok = scalar_bits_equal(observed, expected)
        except ComparatorError as e:
            self.fail("comparator", check, "float64 scalar", repr(type(observed).__name__), str(e))
        if not ok:
            self.fail("comparator", check, scalar_bits(expected), scalar_bits(observed), f"expected {expected!r} observed {observed!r}")
        self.rep.checks[self.stage] = self.rep.checks.get(self.stage, 0) + 1

    def exact_int(self, check: str, observed, expected: int) -> None:
        """Integers must BE integral scalar types (never bool, float, or a float-valued 1.0)."""
        self.rep.comparator_evaluations += 1; self._ledger(check)
        if isinstance(observed, bool) or not isinstance(observed, (int, np.integer)):
            self.fail("comparator", check, "integral scalar", type(observed).__name__, "integer comparator refuses non-integral or boolean observed values")
        if int(observed) != int(expected):
            self.fail("comparator", check, str(expected), str(observed))
        self.rep.checks[self.stage] = self.rep.checks.get(self.stage, 0) + 1

    def refused(self, identity: str, fn: Callable[[], Any]) -> None:
        self._ledger(identity.split("|")[0])
        try:
            out = fn()
        except BR.BridgeDomainError:
            self.rep.refusals_verified.append(identity); return
        self.fail("domain", identity, "BridgeDomainError", repr(out), "undefined statistic returned a value instead of refusing")


# ----------------------------------------------------------------------------- stages
def _q1(r: _R) -> None:
    for name in R0_CASES["q1_grids"]:
        r.case = f"q1|{name}"
        grid = grid_named(name)
        exp_ld = np.array([[f(x) for x in row] for row in exact_local_density(grid)])
        # instrument: emitted Local_Density through the public step (draws irrelevant to the read)
        m, stub = _model(_cfg(G, "local"), grid, [np.zeros((G, G))], np.full((G, G), 0.5), np.full((G, G), 0.5), np.full((G, G), 0.5))
        cap = _step_capture(m)
        r.bits("Local_Density_instrument", cap["Local_Density"], exp_ld)
        r.bits("Local_Density_bridge", BR.local_density(grid), exp_ld)
        r.scalar("rho_global_bridge", BR.rho_global(grid), f(exact_rho(grid)))
    for (cname, n) in R0_CASES["q1_motifs"]:
        r.case = f"q1|motif|{cname}|n={n}"
        grid, c = motif_grid(cname, n)
        exp_ld = np.array([[f(x) for x in row] for row in exact_local_density(grid)])
        if exact_moore_count(grid)[c[0]][c[1]] != n:
            r.fail("internal", "motif_construction", str(n), str(exact_moore_count(grid)[c[0]][c[1]]))
        m, _ = _model(_cfg(GRID_MOTIF, "local"), grid, [np.zeros((GRID_MOTIF, GRID_MOTIF))],
                      np.full((GRID_MOTIF, GRID_MOTIF), 0.5), np.full((GRID_MOTIF, GRID_MOTIF), 0.5), np.full((GRID_MOTIF, GRID_MOTIF), 0.5))
        cap = _step_capture(m)
        r.bits("Local_Density_instrument", cap["Local_Density"], exp_ld)
        r.bits("Local_Density_bridge", BR.local_density(grid), exp_ld)


def _q2(r: _R) -> None:
    for (traj, q_read) in R0_CASES["q2_trajectories"]:
        r.case = f"q2|{traj}|{q_read}"
        if traj == "draws_zero_from_quarter":
            grid = np.zeros((G, G), bool); grid.flat[:N // 4] = True; draw = 0.0      # every activation passes
        else:
            grid = np.zeros((G, G), bool); grid.flat[:N // 2] = True; draw = np.nextafter(1.0, 0.0)   # none passes (p_act <= 1)
        T = R0_CASES["q2_ticks"]
        draws = [np.full((G, G), draw)] * T
        cfg = _cfg(G, q_read, ticks=T)                 # the persistence run is COMPLETE per its own config
        m, stub = _model(cfg, grid, draws, np.full((G, G), 0.5), np.full((G, G), 0.5), np.full((G, G), 0.5))
        # expected pre-update rho sequence from the exact construction
        cur = grid.copy(); expected_seq = []
        for t in range(T):
            expected_seq.append(f(exact_rho(cur)))
            cur = np.ones_like(cur) if draw == 0.0 else np.zeros_like(cur)
        # (a) computation: the emitted scalar through the public step, tick-indexed
        rows = []
        for t in range(T):
            cap = _step_capture(m); rows.append((cap["_tick"], cap["rho_global"]))
            stub.next_tick()
        stub.assert_consumed()
        for t in range(T):
            r.exact_int("rho_tick_index", rows[t][0], t)
            r.scalar("rho_global_pre_update", rows[t][1], expected_seq[t])
            r.rep.checks[r.stage] -= 1          # one Q2 check per tick (index + value together)
        # (b) PERSISTENCE (L2 R1): the production TelemetryWriter writes the tick table; it is read
        #     back and compared bit-exact, and the CLEARED verifier is invoked mechanically on the run.
        tmpd = tempfile.mkdtemp(prefix="r0_q2_")
        try:
            path = os.path.join(tmpd, "q2.parquet")
            m2, stub2 = _model(cfg, grid, [np.full((G, G), draw)] * T, np.full((G, G), 0.5), np.full((G, G), 0.5), np.full((G, G), 0.5))
            tw = TelemetryWriter(G, 0.0, 0.0, False)
            tw.open(path)
            for t in range(T):
                m2.step(tw.sink); stub2.next_tick()
            tw.close(); stub2.assert_consumed()
            r._ledger("rho_global_table_persisted"); r.rep.comparator_evaluations += 1
            if not tw.rho_global_path or not os.path.isfile(tw.rho_global_path):
                r.fail("comparator", "rho_global_table_persisted", "tick table artifact", "absent", "no rho_global tick table was written")
            import pandas as pd
            tbl = pd.read_parquet(tw.rho_global_path)
            if list(tbl.columns) != ["Tick", "rho_global"] or len(tbl) != T:
                r.fail("comparator", "rho_global_table_shape", f"['Tick','rho_global'] x {T}", f"{list(tbl.columns)} x {len(tbl)}")
            ticks = tbl["Tick"].to_numpy(); vals = tbl["rho_global"].to_numpy()
            if vals.dtype != np.float64 or not np.issubdtype(ticks.dtype, np.integer):
                r.fail("comparator", "rho_global_table_dtypes", "int / float64", f"{ticks.dtype} / {vals.dtype}")
            r._ledger("rho_global_table_shape"); r._ledger("rho_global_table_dtypes"); r._ledger("rho_global_table_tick"); r.rep.comparator_evaluations += 3
            for t in range(T):
                if int(ticks[t]) != t: r.fail("comparator", "rho_global_table_tick", str(t), str(int(ticks[t])), "persisted tick index differs")
            r.bits("rho_global_table_values", vals, np.array(expected_seq)); r.rep.checks[r.stage] -= 1
            r._ledger("cleared_verifier_rho_table")
            vrep = VERIFY.tier1_verify(path, cfg, rho_global_path=tw.rho_global_path, expect_rho_global=True)
            if not vrep.passed:
                r.fail("comparator", "cleared_verifier_rho_table", "tier1_verify PASS", vrep.summary(), "the cleared telemetry verifier rejected the Gate-R run")
            r.rep.checks[r.stage] += 1          # one persistence bundle per trajectory
            r.rep.comparator_evaluations += 1
        finally:
            import shutil; shutil.rmtree(tmpd, ignore_errors=True)


def _q3_bases(kind: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Distinct per-base spatial patterns and values (L2 R4), all dyadic, all in [0,1]."""
    idx = np.indices((G, G))
    if kind == "high":    # v near the top (clips high widely), u_base mid, r low (clips high rarely)
        return np.where(idx[0] < 8, 0.875, 0.75), np.where(idx[1] % 2 == 0, 0.5, 0.25), np.full((G, G), 0.0625)
    if kind == "low":     # bases near zero so a negative delta clips low, with per-base differences
        return np.where(idx[0] < 8, 0.0, 0.125), np.where(idx[1] % 2 == 0, 0.25, 0.0), np.full((G, G), 0.5)
    return np.full((G, G), 0.5), np.where(idx[0] % 2 == 0, 0.375, 0.625), np.where(idx[1] < 8, 0.25, 0.75)   # no clip


def _q3(r: _R) -> None:
    for (pattern, q_read, gpsi, grho, bases_kind) in R0_CASES["q3_cases"]:
        r.case = f"q3|{pattern}|{q_read}|gpsi={gpsi}|grho={grho}|bases={bases_kind}"
        grid = np.zeros((G, G), bool)
        if pattern == "iso": grid[8, 8] = True; draws = np.zeros((G, G))                       # all become active
        elif pattern == "row": grid[4, :] = True; draws = np.zeros((G, G))
        elif pattern == "checker": grid = grid_named("checkerboard"); draws = np.zeros((G, G))
        else:   # "sink": centre inactive activates (draw 0) while its eight active neighbours die (draw ~1)
            grid[7:10, 7:10] = True; grid[8, 8] = False
            draws = np.full((G, G), np.nextafter(1.0, 0.0)); draws[8, 8] = 0.0
        cfg = _cfg(G, q_read, gpsi, grho)
        v0, u0, r0 = _q3_bases(bases_kind)
        m, stub = _model(cfg, grid, [draws], v0, u0, r0)
        cap = _step_capture(m)
        # exact expectation: next state from the draws against p_act; but p_act is the instrument's —
        # the CONSTRUCTIONS make it irrelevant: draw 0 always activates, draw nextafter(1) never does
        nxt = [[1 if draws[i, j] == 0.0 else 0 for j in range(G)] for i in range(G)]
        ds = [[nxt[i][j] - int(grid[i, j]) for j in range(G)] for i in range(G)]
        moore_ds = [[sum(ds[(i + dx) % G][(j + dy) % G] for dx, dy in _MOORE) for j in range(G)] for i in range(G)]
        psi = [[Fraction(ds[i][j] * moore_ds[i][j]) for j in range(G)] for i in range(G)]
        # The frozen Psi_local definition is the ancestor's FLOAT product float64(ds)·float64(Σds) (dynamics
        # Step 9, verbatim ancestor). Exact rationals carry no signed zero; IEEE does: a zero product takes
        # the sign of its factors' signs. This rule is transcribed here as part of the definition, so the
        # signed-zero-discriminating comparator compares like with like. It propagates through Γ_Ψ·Ψ (Γ>0)
        # and vanishes in any sum with a nonzero term or with +0.0 (−0 + +0 = +0).
        def psi_neg_zero(i, j):
            return psi[i][j] == 0 and ((ds[i][j] < 0) != (moore_ds[i][j] < 0)) and (ds[i][j] != 0 or moore_ds[i][j] != 0)
        ld = exact_local_density(grid); rho = exact_rho(grid)
        ai = ld if q_read == "local" else [[rho] * G for _ in range(G)]
        gp, gr = Fraction(gpsi), Fraction(grho)
        dpsi = [[gp * psi[i][j] for j in range(G)] for i in range(G)]
        drho = [[gr * ai[i][j] for j in range(G)] for i in range(G)]
        delta = [[dpsi[i][j] + drho[i][j] for j in range(G)] for i in range(G)]
        def to_arr(M, signed_zero=None):
            out = np.array([[f(x) for x in row] for row in M])
            if signed_zero is not None:
                for i in range(G):
                    for j in range(G):
                        if signed_zero(i, j): out[i, j] = -0.0
            return out
        # delta's zero sign: dpsi (−0 or +0) + drho (+x or +0): −0 + +0 = +0, so delta zero is always +0 unless drho is also −0 (never: Γ_ρ≥0, ai≥0)
        exact_bases = {}
        for name, b in (("v", v0), ("u_base", u0), ("r", r0)):
            bf = [[Fraction(float(b[i, j])) for j in range(G)] for i in range(G)]
            newb = [[bf[i][j] + delta[i][j] for j in range(G)] for i in range(G)]
            exact_bases[name] = (sum(1 for row in newb for x in row if x < 0 or x > 1),
                                 [[min(max(x, Fraction(0)), Fraction(1)) for x in row] for row in newb])
        # instrument: emitted decomposition and Psi; committed post-update bases; per-base counters
        r.bits("Delta_from_Psi_instrument", cap["Delta_from_Psi"], to_arr(dpsi, psi_neg_zero))
        r.bits("Delta_from_rho_instrument", cap["Delta_from_rho"], to_arr(drho))
        r.bits("Psi_local_instrument", cap["Psi_local"], to_arr(psi, psi_neg_zero))
        r.bits("is_active_next_instrument", cap["is_active"].astype(np.float64), np.array(nxt, dtype=np.float64))
        r.bits("v_post_update", m._v, to_arr(exact_bases["v"][1])); r.bits("u_base_post_update", m._u_base, to_arr(exact_bases["u_base"][1])); r.bits("r_post_update", m._r, to_arr(exact_bases["r"][1]))
        r.exact_int("clipped_v_count", m.clipped_v_count, exact_bases["v"][0]); r.exact_int("clipped_u_base_count", m.clipped_u_count, exact_bases["u_base"][0]); r.exact_int("clipped_r_count", m.clipped_r_count, exact_bases["r"][0])
        # bridge: every QResponse field on the same inputs
        qr = BR.q_response(to_arr(psi, psi_neg_zero), to_arr(ai) if q_read == "local" else f(rho), gpsi, grho, v0, u0, r0)
        r.bits("Delta_from_Psi_bridge", qr.delta_from_psi, to_arr(dpsi, psi_neg_zero)); r.bits("Delta_from_rho_bridge", qr.delta_from_rho, to_arr(drho)); r.bits("delta_bridge", qr.delta, to_arr(delta))
        r.bits("v_new_bridge", qr.v_new, to_arr(exact_bases["v"][1])); r.bits("u_base_new_bridge", qr.u_base_new, to_arr(exact_bases["u_base"][1])); r.bits("r_new_bridge", qr.r_new, to_arr(exact_bases["r"][1]))
        r.exact_int("clipped_v_bridge", qr.clipped_v, exact_bases["v"][0]); r.exact_int("clipped_u_base_bridge", qr.clipped_u_base, exact_bases["u_base"][0]); r.exact_int("clipped_r_bridge", qr.clipped_r, exact_bases["r"][0])
        r.scalar("mean_delta_from_psi_bridge", qr.mean_delta_from_psi, f(sum(x for row in dpsi for x in row) / N))
        r.scalar("mean_delta_from_rho_bridge", qr.mean_delta_from_rho, f(sum(x for row in drho for x in row) / N))
        r.scalar("mean_delta_bridge", qr.mean_delta, f(sum(x for row in delta for x in row) / N))
        # the constructed case must realise the clip regime it declares (construction self-check)
        lows = highs = 0
        for name, b in (("v", v0), ("u_base", u0), ("r", r0)):
            for i in range(G):
                for j in range(G):
                    x = Fraction(float(b[i, j])) + delta[i][j]
                    lows += x < 0; highs += x > 1
        realised = "low" if lows else ("high" if highs else "none")
        if realised != bases_kind:
            r.fail("internal", "q3_construction_regime", bases_kind, realised, "constructed case does not realise its declared clip regime")


def _q4(r: _R) -> None:
    for name in R0_CASES["q4_dispersion"]:
        r.case = f"q4|dispersion|{name}"; grid = grid_named(name)
        r.scalar("local_read_dispersion", BR.local_read_dispersion(BR.local_density(grid), BR.rho_global(grid)),
                 f(exact_dispersion(exact_local_density(grid), exact_rho(grid))))
    ld = BR.local_density(grid_named("row_stripes"))
    for name in R0_CASES["q4_correlation"]:
        r.case = f"q4|correlation|{name}"
        if name == "plus_one": r.scalar("config_neighbourhood_correlation", BR.config_neighbourhood_correlation(ld, ld), 1.0)
        elif name == "minus_one": r.scalar("config_neighbourhood_correlation", BR.config_neighbourhood_correlation(1.0 - ld, ld), -1.0)
        else:
            # zero by construction: x alternates by column while Local_Density varies by row (stripes) -> covariance exactly 0
            x = (np.indices((G, G))[1] % 2).astype(np.float64)
            r.scalar("config_neighbourhood_correlation", BR.config_neighbourhood_correlation(x, ld), 0.0)
    for name in R0_CASES["q4_moran"]:
        r.case = f"q4|moran|{name}"; grid = grid_named(name)
        r.scalar("morans_i", BR.morans_i(grid), f(exact_moran(grid)))
    for name in R0_CASES["q4_moran_refused"]:
        r.case = f"q4|moran_refused|{name}"
        r.refused(f"morans_i_refused_on_constant_grid|{name}", lambda g=grid_named(name): BR.morans_i(g))
    r.case = "q4|correlation_refused|constant"
    r.refused("correlation_refused_on_zero_variance|constant", lambda: BR.config_neighbourhood_correlation(np.full((G, G), 0.5), ld))
    for name in R0_CASES["q4_base_dispersion"]:
        r.case = f"q4|base_dispersion|{name}"
        if name == "halves":
            v = np.where(np.indices((G, G))[0] < G // 2, 0.25, 0.75); u = np.full((G, G), 0.5); rr = np.where(np.indices((G, G))[1] % 2 == 0, 0.0, 1.0)
        else:
            v = np.full((G, G), 0.25); u = np.where(np.indices((G, G))[0] % 4 == 0, 1.0, 0.0); rr = np.where((np.indices((G, G)).sum(0)) % 2 == 0, 0.125, 0.375)
        out = BR.base_distribution_dispersion(v, u, rr)
        for bname, arr in (("v", v), ("u_base", u), ("r", rr)):
            em, ev = exact_base_stats([[Fraction(float(x)) for x in row] for row in arr])
            r.scalar(f"base_mean_{bname}", out[bname][0], f(em)); r.scalar(f"base_var_{bname}", out[bname][1], f(ev))


def _read_dynamics_bytes() -> bytes:
    from .. import dynamics as D
    return open(D.__file__, "rb").read()


def _no_feedback_path() -> Tuple[bool, str]:
    """Structural guarantee (L2 R11): the actual dynamics.py FILE BYTES are parsed with `ast`; any
    direct `import`/`from ... import` reference to the bridge module refuses. Claim limited to the
    declared direct-import boundary. Returns (ok, file-byte digest)."""
    raw = _read_dynamics_bytes()
    tree = ast.parse(raw)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(a.name.split(".")[-1] == "bridge" for a in node.names):
            return False, hashlib.sha256(raw).hexdigest()
        if isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[-1] == "bridge" or any(a.name == "bridge" for a in node.names):
                return False, hashlib.sha256(raw).hexdigest()
    return True, hashlib.sha256(raw).hexdigest()


# ----------------------------------------------------------------------------- entry
def _file_sha(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run_r0(pinned_root: str, label: str = "PROVISIONAL", record_dir: Optional[str] = None) -> R0Report:
    if label not in LABELS:
        raise ValueError(f"unknown label {label!r}; frozen set {LABELS}")
    if label == "AUTHORITATIVE" and record_dir is None:
        raise ValueError("AUTHORITATIVE Gate R0 requires a persistent record owner: record_dir is mandatory")
    env = f"python{platform.python_version()}/numpy{np.__version__}"
    from .. import dynamics as D
    prov: Dict[str, Any] = {"label": label, "environment": env, "r0_version": R0_VERSION,
                            "governing": dict(R0_GOVERNING),
                            "frozen_case_map_sha256_literal": FROZEN_R0_SHA256_LITERAL,
                            "frozen_ledger_sha256_literal": FROZEN_LEDGER_SHA256_LITERAL,
                            "frozen_completion_sha256_literal": FROZEN_COMPLETION_SHA256_LITERAL,
                            "bridge_source_sha256": _file_sha(BR.__file__), "gate_r0_source_sha256": _file_sha(__file__),
                            "dynamics_source_sha256": _file_sha(D.__file__)}
    rep = R0Report(label=label, environment=env, environment_record=None, provenance=prov)
    r = _R(rep)

    def _boundary(stage: str, fn: Callable[[], None]) -> None:
        r.stage = stage
        try:
            fn()
        except R0Halt:
            pass
        except BaseException as e:            # noqa: BLE001 — one grammar for every failure class
            cls = ("environment" if isinstance(e, EnvironmentCheckError) else "comparator" if isinstance(e, ComparatorError)
                   else "stub" if isinstance(e, StubError) else "provenance" if isinstance(e, ProvenanceError)
                   else "domain" if isinstance(e, BR.BridgeDomainError) else "internal")
            check = getattr(e, "check", None) or {"environment": "frozen_pin_source", "comparator": "comparator_contract", "stub": "frozen_sequence_stub",
                                                    "domain": "unexpected_refusal", "internal": "unexpected_exception"}.get(cls, "unexpected_exception")
            try: r.fail(cls, check, "", "", f"{type(e).__name__}: {e}")
            except R0Halt: pass
        if rep.failure is not None:
            if record_dir is not None:
                rep.failure.written_to = _write_atomically({**asdict(rep.failure), "kind": "r0_failure"}, record_dir, "gate_r0_failure")
        else:
            rep.stages_completed.append(stage)

    def _preflight() -> None:
        r.case = "environment"
        envrec: EnvironmentRecord = check_environment(pinned_root)
        rep.environment_record = asdict(envrec); prov["environment_conforms"] = envrec.conforms
        if label == "AUTHORITATIVE" and not envrec.conforms:
            r.fail("environment", "frozen_environment", "conforming", "non-conforming", "; ".join(envrec.failures))
        r.case = "candidate_provenance"
        inst_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        candidate_provenance(inst_root, prov)                          # accumulating, typed (Gate B standard)
        r.case = "source_identity_consistency"
        # single-object discipline (10B): every read of dynamics.py must agree BEFORE any verdict
        ids = {prov.get("candidate_dynamics_sha256"), prov.get("dynamics_source_sha256")}
        if len(ids) != 1 or None in ids:
            r.fail("provenance", "dynamics_digest_consistency", "one identity", repr(sorted(str(i) for i in ids)), "dynamics.py digests differ across preflight reads")
        r.case = "static_frozen_case_map"
        digest = frozen_map_digest(FROZEN_R0)
        if digest != FROZEN_R0_SHA256_LITERAL:
            r.fail("structural", "frozen_case_map_digest", FROZEN_R0_SHA256_LITERAL, digest, "runtime FROZEN_R0 differs from the frozen literal digest")
        if frozen_map_digest(FROZEN_LEDGER) != FROZEN_LEDGER_SHA256_LITERAL:
            r.fail("structural", "frozen_ledger_digest", FROZEN_LEDGER_SHA256_LITERAL, frozen_map_digest(FROZEN_LEDGER), "runtime FROZEN_LEDGER differs from its literal digest")
        if frozen_map_digest(FROZEN_COMPLETION) != FROZEN_COMPLETION_SHA256_LITERAL:
            r.fail("structural", "frozen_completion_digest", FROZEN_COMPLETION_SHA256_LITERAL, frozen_map_digest(FROZEN_COMPLETION), "runtime FROZEN_COMPLETION differs from its literal digest")
        if tuple(STAGES) != tuple(FROZEN_R0["stages"]) or tuple(STAGES) != tuple(FROZEN_COMPLETION["stages"]):
            r.fail("structural", "static_stages", repr(FROZEN_COMPLETION["stages"]), repr(STAGES))
        if (G, N, GRID_MOTIF) != (FROZEN_COMPLETION["grid"], FROZEN_COMPLETION["n_cells"], FROZEN_COMPLETION["motif_grid"]):
            r.fail("structural", "static_constants", repr((FROZEN_COMPLETION["grid"], FROZEN_COMPLETION["n_cells"], FROZEN_COMPLETION["motif_grid"])), repr((G, N, GRID_MOTIF)))
        exec_keys = set(R0_CASES); frozen_exec_keys = set(FROZEN_R0) - {"grid", "n_cells", "motif_grid", "stages"}
        if exec_keys != frozen_exec_keys:
            r.fail("structural", "static_key_sets", repr(sorted(frozen_exec_keys)), repr(sorted(exec_keys)))
        for key, val in R0_CASES.items():
            if val != FROZEN_R0[key]:
                r.fail("structural", f"static_{key}", repr(FROZEN_R0[key]), repr(val), "execution declaration differs from the frozen case map")
        r.case = "no_feedback_path"
        ok, dyn_sha = _no_feedback_path(); prov["dynamics_file_sha256_at_ast_check"] = dyn_sha
        if dyn_sha != prov["dynamics_source_sha256"]:
            r.fail("provenance", "dynamics_digest_consistency", prov["dynamics_source_sha256"], dyn_sha, "dynamics.py bytes at the AST check differ from the provenance read")
        if not ok:
            r.fail("structural", "bridge_feedback_path", "dynamics.py has no bridge import", "bridge import present (AST)")

    def _completion() -> None:
        r.case = "frozen_completion"
        if rep.stages_completed != list(STAGES[:-1]):
            r.fail("structural", "stages", repr(list(STAGES[:-1])), repr(rep.stages_completed))
        C = FROZEN_COMPLETION
        if dict(rep.checks) != dict(C["checks"]):
            r.fail("structural", "frozen_check_map", repr(dict(C["checks"])), repr(dict(rep.checks)))
        if rep.comparator_evaluations != C["comparator_evaluations"]:
            r.fail("structural", "frozen_evaluation_total", str(C["comparator_evaluations"]), str(rep.comparator_evaluations))
        if list(rep.refusals_verified) != list(C["refusals"]):
            r.fail("structural", "frozen_refusal_identities", repr(list(C["refusals"])), repr(list(rep.refusals_verified)))
        got = {s: dict(v) for s, v in rep.ledger.items()}; want = {s: dict(v) for s, v in FROZEN_LEDGER.items()}
        if got != want:
            diff = {s: {k: (want.get(s, {}).get(k), got.get(s, {}).get(k)) for k in set(want.get(s, {})) | set(got.get(s, {})) if want.get(s, {}).get(k) != got.get(s, {}).get(k)} for s in set(want) | set(got)}
            r.fail("structural", "frozen_comparator_ledger", "exact per-stage check ledger", repr({s: d for s, d in diff.items() if d}), "comparator surface differs from the frozen ledger")

    _boundary("preflight", _preflight)
    if rep.failure is not None: return rep
    for name, fn in (("q1", lambda: _q1(r)), ("q2", lambda: _q2(r)), ("q3", lambda: _q3(r)), ("q4", lambda: _q4(r)), ("completion", _completion)):
        _boundary(name, fn)
        if rep.failure is not None: return rep
    if label == "AUTHORITATIVE":
        # FROZEN RULE (L2 R12, option 1): an AUTHORITATIVE R0 success is persisted atomically by run_r0
        # itself; the report is the gate artifact. PROVISIONAL runs persist failures only.
        rep.written_to = _write_atomically({**asdict(rep), "passed": rep.passed, "kind": "r0_authoritative_report"}, record_dir, "gate_r0_AUTHORITATIVE_report")
    return rep


# =============================================================================== qualification
# The gate must be shown to fail: controlled deformations of the BRIDGE and of the INSTRUMENT paths R0
# exercises, each rejected by a check declared BEFORE it runs. Frozen manifest, closed dispatcher,
# runtime declaration compared to the manifest before any mutant executes (the Gate B discipline).
import contextlib
from unittest import mock

# Mutants that deform the dynamics IDENTITY channel by design (declared): their own runs may carry a
# dynamics digest different from the baseline; every other identity must still agree (r3 item 6).
IDENTITY_CHANNEL_MUTANTS = frozenset({"dyn:import_bridge_bytes", "dyn:import_bridge_all_reads"})
IDENTITY_BUNDLE_KEYS = ("candidate_commit", "bridge_source_sha256", "gate_r0_source_sha256", "governing",
                        "frozen_case_map_sha256_literal", "frozen_ledger_sha256_literal", "frozen_completion_sha256_literal")
DYNAMICS_IDENTITY_KEYS = ("candidate_dynamics_sha256", "dynamics_source_sha256")
FROZEN_R0_MANIFEST_SHA256_LITERAL = "b577bd32017e6ae7686b05ade03077eda690497009b806e340d9c21e495aa60c"   # established 2026-09-16 (28 entries); verified at qualification preflight
# (id, name, target, mutation_id, allowable checks, expected stage, allowable case prefixes)
FROZEN_R0_MANIFEST: Tuple[Tuple[int, str, str, str, Tuple[str, ...], str, Tuple[str, ...]], ...] = (
    (1, "bridge_stencil_cardinal", "bridge", "bridge:stencil_cardinal", ("Local_Density_bridge",), "q1", ('q1|',)),
    (2, "bridge_divisor_9", "bridge", "bridge:divisor_9", ("Local_Density_bridge",), "q1", ('q1|',)),
    (3, "instrument_stencil_cardinal", "instrument", "dyn:moore_cardinal", ("Local_Density_instrument",), "q1", ('q1|',)),
    (4, "bridge_rho_off_by_one", "bridge", "bridge:rho_plus_one", ("rho_global_bridge",), "q1", ('q1|',)),
    (5, "instrument_rho_post_update", "instrument", "sink:rho_post_update", ("rho_global_pre_update",), "q2", ('q2|',)),
    (6, "instrument_local_density_post_update", "instrument", "sink:ld_post_update", ("Local_Density_instrument",), "q1", ('q1|',)),
    (7, "bridge_decomposition_swapped", "bridge", "bridge:decomp_swap", ("Delta_from_Psi_bridge",), "q3", ('q3|',)),
    (8, "instrument_decomposition_swapped", "instrument", "sink:decomp_swap", ("Delta_from_Psi_instrument",), "q3", ('q3|',)),
    (9, "bridge_clip_counted_after_clip", "bridge", "bridge:clip_after", ("clipped_v_bridge", "clipped_u_base_bridge", "clipped_r_bridge"), "q3", ('q3|',)),
    (10, "instrument_clip_counters_reset", "instrument", "dyn:clip_reset", ("clipped_v_count", "clipped_u_base_count", "clipped_r_count"), "q3", ('q3|',)),
    (11, "bridge_moran_self_weight", "bridge", "bridge:moran_self", ("morans_i",), "q4", ('q4|moran|',)),
    (12, "bridge_moran_undefined_returns_zero", "bridge", "bridge:moran_zero", ("morans_i_refused_on_constant_grid|all_inactive",), "q4", ('q4|moran_refused|',)),
    (13, "bridge_dispersion_ddof1", "bridge", "bridge:dispersion_ddof1", ("local_read_dispersion",), "q4", ('q4|dispersion|',)),
    (14, "bridge_correlation_undefined_returns_zero", "bridge", "bridge:corr_zero", ("correlation_refused_on_zero_variance|constant",), "q4", ('q4|correlation_refused|',)),
    (15, "bridge_base_variance_ddof1", "bridge", "bridge:base_ddof1", ("base_var_v",), "q4", ('q4|base_dispersion|',)),
    (16, "dynamics_source_inconsistent_across_reads", "structural", "dyn:import_bridge_bytes", ("dynamics_digest_consistency",), "preflight", ('no_feedback_path',)),
    (17, "bridge_base_outputs_swapped", "bridge", "bridge:base_swap", ("u_base_new_bridge", "r_new_bridge"), "q3", ('q3|',)),
    (18, "bridge_r_counter_from_v", "bridge", "bridge:r_counter_from_v", ("clipped_r_bridge",), "q3", ('q3|sink|',)),
    (19, "bridge_mean_delta_wrong", "bridge", "bridge:mean_delta_wrong", ("mean_delta_bridge",), "q3", ('q3|',)),
    (20, "bridge_low_clip_not_counted", "bridge", "bridge:low_clip_uncounted", ("clipped_v_bridge", "clipped_u_base_bridge", "clipped_r_bridge"), "q3", ('q3|sink|',)),
    (21, "instrument_low_clip_not_counted", "instrument", "dyn:low_clip_uncounted", ("clipped_v_count", "clipped_u_base_count", "clipped_r_count"), "q3", ('q3|sink|',)),
    (22, "instrument_tick_index_shift", "instrument", "sink:tick_shift", ("rho_tick_index",), "q2", ('q2|',)),
    (23, "writer_omits_rho_table", "instrument", "writer:no_rho_table", ("rho_global_table_persisted",), "q2", ('q2|',)),
    (24, "bridge_correlation_sign_flipped", "bridge", "bridge:corr_sign", ("config_neighbourhood_correlation",), "q4", ('q4|correlation|',)),
    (25, "bridge_base_mean_shifted", "bridge", "bridge:base_mean_shift", ("base_mean_v",), "q4", ('q4|base_dispersion|',)),
    (26, "instrument_local_density_float32", "instrument", "sink:ld_float32", ("comparator_contract",), "q1", ('q1|',)),
    (27, "instrument_bases_swapped_post_update", "instrument", "dyn:bases_swap", ("v_post_update", "r_post_update"), "q3", ('q3|',)),
    (28, "dynamics_imports_bridge_consistently", "structural", "dyn:import_bridge_all_reads", ("bridge_feedback_path",), "preflight", ('no_feedback_path',)),
)
_R0_IMPL: Dict[str, Callable[[], contextlib.ExitStack]] = {}


def _reg(mid: str, factory):
    factory.mutation_id = mid; _R0_IMPL[mid] = factory; return factory


def _patch(target, name, value):
    def apply():
        st = contextlib.ExitStack(); st.enter_context(mock.patch.object(target, name, value)); return st
    return apply


def _sink_wrap(transform):
    """Patch Dynamics.step so the sink sees transformed fields (instrument-path mutants)."""
    real = Dynamics.step
    def step(self, sink=None):
        return real(self, (lambda t, fl: sink(t, transform(self, fl))) if sink else None)
    return _patch(Dynamics, "step", step)


def _register_all() -> None:
    if _R0_IMPL: return
    from .. import dynamics as D
    _reg("bridge:stencil_cardinal", _patch(BR, "_MOORE_OFFSETS", ((-1, 0), (1, 0), (0, -1), (0, 1))))
    _reg("bridge:divisor_9", _patch(BR, "local_density", lambda grid: BR.moore_count(grid).astype(np.float64) / 9.0))
    def moore_cardinal(x):
        out = np.zeros_like(x, dtype=np.float64)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)): out += np.roll(np.roll(x, dx, 0), dy, 1)
        return out
    _reg("dyn:moore_cardinal", _patch(D, "_moore_sum_a", moore_cardinal))
    _reg("bridge:rho_plus_one", _patch(BR, "rho_global", lambda grid: float(np.float64(int(np.asarray(grid).sum()) + 1) / np.float64(np.asarray(grid).size))))
    _reg("sink:rho_post_update", _sink_wrap(lambda self, fl: {**fl, "rho_global": np.float64(np.mean(fl["is_active"]))} if "rho_global" in fl else fl))
    _reg("sink:ld_post_update", _sink_wrap(lambda self, fl: {**fl, "Local_Density": BR.local_density(fl["is_active"])} if "Local_Density" in fl else fl))
    real_q = BR.q_response
    def swapped(psi, ai, gp, gr, v, u, r):
        q = real_q(psi, ai, gp, gr, v, u, r)
        return BR.QResponse(q.delta_from_rho, q.delta_from_psi, q.delta, q.v_new, q.u_base_new, q.r_new, q.clipped_v, q.clipped_u_base, q.clipped_r,
                            q.mean_delta_from_rho, q.mean_delta_from_psi, q.mean_delta)
    _reg("bridge:decomp_swap", _patch(BR, "q_response", swapped))
    _reg("sink:decomp_swap", _sink_wrap(lambda self, fl: {**fl, "Delta_from_Psi": fl["Delta_from_rho"], "Delta_from_rho": fl["Delta_from_Psi"]} if "Delta_from_Psi" in fl else fl))
    def clip_after(psi, ai, gp, gr, v, u, r):
        q = real_q(psi, ai, gp, gr, v, u, r)
        c = int(np.sum((q.v_new < 0.0) | (q.v_new > 1.0)))          # counted AFTER clipping: always 0
        return BR.QResponse(q.delta_from_psi, q.delta_from_rho, q.delta, q.v_new, q.u_base_new, q.r_new, c, c, c, q.mean_delta_from_psi, q.mean_delta_from_rho, q.mean_delta)
    _reg("bridge:clip_after", _patch(BR, "q_response", clip_after))
    real_step = Dynamics.step
    def reset_counters(self, sink=None):
        real_step(self, sink); self.clipped_v_count = self.clipped_u_count = self.clipped_r_count = 0
    _reg("dyn:clip_reset", _patch(Dynamics, "step", reset_counters))
    def moran_self(grid):                                        # Moran's I alone, with a self-weight term; stencil untouched
        g = np.asarray(grid).astype(np.float64); n = np.float64(g.size); d = g - np.float64(np.sum(g)) / n
        denom = np.float64(np.sum(d * d))
        if denom == 0.0: raise BR.BridgeDomainError("constant grid")
        lag = d.copy()
        for dx, dy in BR._MOORE_OFFSETS: lag += np.roll(np.roll(d, dx, 0), dy, 1)
        return float(np.float64(np.sum(d * lag)) / (np.float64(8.0) * denom))
    _reg("bridge:moran_self", _patch(BR, "morans_i", moran_self))
    real_moran = BR.morans_i
    def moran_zero(grid):
        try: return real_moran(grid)
        except BR.BridgeDomainError: return 0.0
    _reg("bridge:moran_zero", _patch(BR, "morans_i", moran_zero))
    _reg("bridge:dispersion_ddof1", _patch(BR, "local_read_dispersion", lambda ld, rho: float(np.float64(np.sum((np.asarray(ld) - rho) ** 2)) / np.float64(np.asarray(ld).size - 1))))
    real_corr = BR.config_neighbourhood_correlation
    def corr_zero(x, y):
        try: return real_corr(x, y)
        except BR.BridgeDomainError: return 0.0
    _reg("bridge:corr_zero", _patch(BR, "config_neighbourhood_correlation", corr_zero))
    real_bd = BR.base_distribution_dispersion
    def bd_ddof1(v, u, r):
        out = real_bd(v, u, r); n = np.asarray(v).size
        return {k: (m, var * n / (n - 1)) for k, (m, var) in out.items()}
    _reg("bridge:base_ddof1", _patch(BR, "base_distribution_dispersion", bd_ddof1))
    import sys as _sys
    _self = _sys.modules[__name__]
    real_bytes = _read_dynamics_bytes
    _reg("dyn:import_bridge_bytes", _patch(_self, "_read_dynamics_bytes", lambda: real_bytes().replace(b"import numpy as np", b"import numpy as np\nfrom . import bridge", 1)))
    mutated = real_bytes().replace(b"import numpy as np", b"import numpy as np\nfrom . import bridge", 1)
    mutated_sha = hashlib.sha256(mutated).hexdigest()
    real_file_sha = _file_sha
    from .. import dynamics as _Dm
    def consistent_apply():
        st = contextlib.ExitStack()
        st.enter_context(mock.patch.object(_self, "_read_dynamics_bytes", lambda: mutated))
        st.enter_context(mock.patch.object(_self, "_file_sha", lambda path: mutated_sha if os.path.abspath(path) == os.path.abspath(_Dm.__file__) else real_file_sha(path)))
        real_cp = candidate_provenance
        def cp(root, sink):
            real_cp(root, sink); sink["candidate_dynamics_sha256"] = mutated_sha
        st.enter_context(mock.patch.object(_self, "candidate_provenance", cp))
        return st
    _reg("dyn:import_bridge_all_reads", consistent_apply)
    real_q2 = BR.q_response
    def base_swap(psi, ai, gp, gr, v, u, r):
        q = real_q2(psi, ai, gp, gr, v, u, r)
        return BR.QResponse(q.delta_from_psi, q.delta_from_rho, q.delta, q.v_new, q.r_new, q.u_base_new, q.clipped_v, q.clipped_r, q.clipped_u_base, q.mean_delta_from_psi, q.mean_delta_from_rho, q.mean_delta)
    _reg("bridge:base_swap", _patch(BR, "q_response", base_swap))
    def r_from_v(psi, ai, gp, gr, v, u, r):
        q = real_q2(psi, ai, gp, gr, v, u, r)
        return BR.QResponse(q.delta_from_psi, q.delta_from_rho, q.delta, q.v_new, q.u_base_new, q.r_new, q.clipped_v, q.clipped_u_base, q.clipped_v, q.mean_delta_from_psi, q.mean_delta_from_rho, q.mean_delta)
    _reg("bridge:r_counter_from_v", _patch(BR, "q_response", r_from_v))
    def mean_wrong(psi, ai, gp, gr, v, u, r):
        q = real_q2(psi, ai, gp, gr, v, u, r)
        return BR.QResponse(q.delta_from_psi, q.delta_from_rho, q.delta, q.v_new, q.u_base_new, q.r_new, q.clipped_v, q.clipped_u_base, q.clipped_r, q.mean_delta_from_psi, q.mean_delta_from_rho, q.mean_delta_from_psi)
    _reg("bridge:mean_delta_wrong", _patch(BR, "q_response", mean_wrong))
    def low_uncounted(psi, ai, gp, gr, v, u, r):
        q = real_q2(psi, ai, gp, gr, v, u, r)
        raw = [np.asarray(b) + q.delta for b in (v, u, r)]
        c = [int(np.sum(x > 1.0)) for x in raw]                       # counts high only
        return BR.QResponse(q.delta_from_psi, q.delta_from_rho, q.delta, q.v_new, q.u_base_new, q.r_new, c[0], c[1], c[2], q.mean_delta_from_psi, q.mean_delta_from_rho, q.mean_delta)
    _reg("bridge:low_clip_uncounted", _patch(BR, "q_response", low_uncounted))
    real_step2 = Dynamics.step
    def dyn_low_uncounted(self, sink=None):
        v0, u0, r0 = self._v.copy(), self._u_base.copy(), self._r.copy()
        c0 = (self.clipped_v_count, self.clipped_u_count, self.clipped_r_count)
        real_step2(self, sink)
        # recount as if low clips were not counted: subtract the low-clip entries this step produced
        # (approximated by recomputing from the bases' committed values: any base that is exactly 0.0 now and was > 0 before)
        lows = (int(np.sum((self._v == 0.0) & (v0 > 0.0))), int(np.sum((self._u_base == 0.0) & (u0 > 0.0))), int(np.sum((self._r == 0.0) & (r0 > 0.0))))
        self.clipped_v_count -= lows[0]; self.clipped_u_count -= lows[1]; self.clipped_r_count -= lows[2]
    _reg("dyn:low_clip_uncounted", _patch(Dynamics, "step", dyn_low_uncounted))
    def tick_shift(self, sink=None):
        return real_step2(self, (lambda t, fl: sink(t + 1, fl)) if sink else None)
    _reg("sink:tick_shift", _patch(Dynamics, "step", tick_shift))
    real_close = TelemetryWriter.close
    def close_no_table(self):
        self.rho_global_table = []; real_close(self); self.rho_global_path = None
    _reg("writer:no_rho_table", _patch(TelemetryWriter, "close", close_no_table))
    real_corr2 = BR.config_neighbourhood_correlation
    _reg("bridge:corr_sign", _patch(BR, "config_neighbourhood_correlation", lambda x, y: -real_corr2(x, y)))
    real_bd2 = BR.base_distribution_dispersion
    _reg("bridge:base_mean_shift", _patch(BR, "base_distribution_dispersion", lambda v, u, r: {k: (m + 1.0 / np.asarray(v).size, var) for k, (m, var) in real_bd2(v, u, r).items()}))
    _reg("sink:ld_float32", _sink_wrap(lambda self, fl: {**fl, "Local_Density": fl["Local_Density"].astype(np.float32)} if "Local_Density" in fl else fl))
    def bases_swap(self, sink=None):
        real_step2(self, sink); self._v, self._r = self._r, self._v
    _reg("dyn:bases_swap", _patch(Dynamics, "step", bases_swap))


@dataclass
class R0MutantResult:
    id: int; name: str; target: str; mutation_id: str; expected_checks: List[str]
    rejected: bool; observed_check: Optional[str]; observed_stage: Optional[str]; observed_case: Optional[str]; attributed: bool; detail: str
    artifact_path: Optional[str] = None; artifact_sha256: Optional[str] = None


@dataclass
class R0QualificationRecord:
    version: str; environment: str; label: str; provenance: Dict[str, Any]
    positive_control: Dict[str, Any] = field(default_factory=dict)
    mutants: List[R0MutantResult] = field(default_factory=list)
    stages_completed: List[str] = field(default_factory=list)
    failure: Optional[str] = None
    written_to: Optional[str] = None

    @property
    def passed(self) -> bool:
        want = [(i, n, tg, mid, tuple(sorted(c))) for (i, n, tg, mid, c, _, _) in FROZEN_R0_MANIFEST]
        got = [(m.id, m.name, m.target, m.mutation_id, tuple(sorted(m.expected_checks))) for m in self.mutants]
        return (self.failure is None and self.positive_control.get("passed") is True and got == want
                and all(m.rejected and m.attributed and m.artifact_sha256 for m in self.mutants)
                and self.stages_completed == ["manifest_preflight", "positive_control", "mutants"])

    def summary(self) -> str:
        return (f"R0 QUALIFICATION[{self.label}] positive_control={self.positive_control.get('passed')} mutants rejected="
                f"{sum(m.rejected for m in self.mutants)}/{len(self.mutants)} attributed={sum(m.attributed for m in self.mutants)}/{len(self.mutants)} "
                f"=> {'PASS' if self.passed else 'FAIL'}" + (f" ({self.failure})" if self.failure else ""))


def run_r0_qualification(pinned_root: str, record_dir: str, label: str = "PROVISIONAL") -> R0QualificationRecord:
    if label not in LABELS:
        raise ValueError(f"unknown label {label!r}; frozen set {LABELS}")
    if record_dir is None:
        raise ValueError("formal R0 qualification requires a persistent record owner: record_dir is mandatory")
    _register_all()
    env = f"python{platform.python_version()}/numpy{np.__version__}"
    rec = R0QualificationRecord(version=R0_VERSION, environment=env, label=label,
                                provenance={"frozen_manifest_sha256_literal": FROZEN_R0_MANIFEST_SHA256_LITERAL, "governing": dict(R0_GOVERNING),
                                            "execution_precondition": "fresh Python process; no stale bytecode (L2 r3 O1)",
                                            "bridge_source_sha256": _file_sha(BR.__file__),      # one read function for every identity
                                            "gate_r0_source_sha256": _file_sha(__file__)})
    want_ids = [mid for (_, _, _, mid, _, _, _) in FROZEN_R0_MANIFEST]
    if frozen_map_digest({"manifest": FROZEN_R0_MANIFEST}) != FROZEN_R0_MANIFEST_SHA256_LITERAL:
        rec.failure = "structural: runtime FROZEN_R0_MANIFEST differs from its literal digest"
        rec.written_to = _write_atomically({**asdict(rec), "passed": False}, record_dir, "gate_r0_qualification_FAILURE"); return rec
    if sorted(_R0_IMPL) != sorted(want_ids) or any(getattr(_R0_IMPL[m], "mutation_id", None) != m for m in want_ids):
        rec.failure = "structural: implementation registry does not match the frozen manifest"
        rec.written_to = _write_atomically({**asdict(rec), "passed": False}, record_dir, "gate_r0_qualification_FAILURE"); return rec
    rec.stages_completed.append("manifest_preflight")
    pc = run_r0(pinned_root, label=label, record_dir=os.path.join(record_dir, "positive_control"))
    rec.positive_control = {**asdict(pc), "passed": pc.passed}
    if not pc.passed:
        rec.failure = "positive_control: the unmutated gate did not pass"
        rec.written_to = _write_atomically({**asdict(rec), "passed": False}, record_dir, "gate_r0_qualification_FAILURE"); return rec
    # BASELINE IDENTITY BUNDLE (r3 item 6): the positive control's provenance is the one source identity of
    # this qualification. Qualification-entry identities must agree with it now; every mutant run must
    # carry it too (dynamics identity exempt only for the declared identity-channel mutants).
    baseline = {k: pc.provenance.get(k) for k in IDENTITY_BUNDLE_KEYS + DYNAMICS_IDENTITY_KEYS}
    rec.provenance["baseline_identity_bundle"] = baseline
    entry = {"bridge_source_sha256": rec.provenance["bridge_source_sha256"], "gate_r0_source_sha256": rec.provenance["gate_r0_source_sha256"],
             "governing": rec.provenance["governing"], "frozen_case_map_sha256_literal": FROZEN_R0_SHA256_LITERAL,
             "frozen_ledger_sha256_literal": FROZEN_LEDGER_SHA256_LITERAL, "frozen_completion_sha256_literal": FROZEN_COMPLETION_SHA256_LITERAL}
    drift = {k: (entry[k], baseline.get(k)) for k in entry if entry[k] != baseline.get(k)}
    if drift:
        rec.failure = f"qualification_source_consistency: entry identities differ from the positive control: {sorted(drift)}"
        rec.written_to = _write_atomically({**asdict(rec), "passed": False}, record_dir, "gate_r0_qualification_FAILURE"); return rec
    rec.stages_completed.append("positive_control")
    for (i, name, target, mid, checks, exp_stage, case_prefixes) in FROZEN_R0_MANIFEST:
        with _R0_IMPL[mid]():
            rep = run_r0(pinned_root, label=label, record_dir=os.path.join(record_dir, f"mutant_{i:02d}"))
        # every mutant run must execute the baseline source identities (dynamics exempt for identity-channel mutants)
        mprov = rep.failure.provenance if rep.failure is not None else rep.provenance
        keys = IDENTITY_BUNDLE_KEYS + (() if mid in IDENTITY_CHANNEL_MUTANTS else DYNAMICS_IDENTITY_KEYS)
        drift = [k for k in keys if mprov.get(k) != baseline.get(k)]
        if drift:
            rec.failure = f"qualification_source_consistency: mutant {i} ({name}) ran under different identities: {drift}"
            rec.written_to = _write_atomically({**asdict(rec), "passed": False}, record_dir, "gate_r0_qualification_FAILURE"); return rec
        if rep.failure is None:
            rec.mutants.append(R0MutantResult(i, name, target, mid, sorted(checks), False, None, None, None, False, "NOT REJECTED"))
        else:
            fr = rep.failure
            attributed = (fr.check in checks) and (fr.stage == exp_stage) and any(str(fr.case_id).startswith(pfx) for pfx in case_prefixes)
            sha = hashlib.sha256(open(fr.written_to, "rb").read()).hexdigest() if fr.written_to and os.path.isfile(fr.written_to) else None
            rec.mutants.append(R0MutantResult(i, name, target, mid, sorted(checks), True, fr.check, fr.stage, fr.case_id, attributed,
                                              f"rejected by {fr.failure_class}/{fr.check} at {fr.stage}:{fr.case_id}" + ("" if attributed else f" (UNATTRIBUTED: declared {exp_stage}:{case_prefixes})"),
                                              fr.written_to, sha))
    rec.stages_completed.append("mutants")
    rec.written_to = _write_atomically({**asdict(rec), "passed": rec.passed}, record_dir, "gate_r0_qualification")
    return rec
