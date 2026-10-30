"""mfa_instrument/f8/evaluator.py — Flight 8 module M-P1: the structural evaluator (Contract F8 v0.8.4 §1.1′, §1.2,
§1.2′, §3.4, §4.11, §5.4; freeze record §3 items 9, 10, 11, 13, 17, 21, 24).

P1 IS ADJUDICATED HERE AND NOWHERE ELSE (§4.7(2)). Four pre-registered tests on the two committed objects, none referencing
the location of the crossing in m or the amplitude of the branch:
  T-S1′  a boundary exists: skeleton-high sweep; m̂_c = lowest level with surv ≥ 18 such that surv ≥ 18 at every level above
         it; (i) no level ≥ 18 → fails validly `no active phase in sweep`; (ii) ≥ 18 at every level incl. the lowest → fails
         validly `no inactive phase in sweep`; (iii) ≥ 18 somewhere but not at every level above → NOT DISTINGUISHED
         `non-monotone survival`; (iv) otherwise pass, m̂_c recorded.
  T-S1c  continuity-compatible onset: above m̂_c, med(m) non-decreasing under the evaluability rule; every increase ≤ f_J ×
         (med(m_max) − med(m̂_c)), f_J = 0.25; an increase beyond f_J → NOT DISTINGUISHED `continuity unresolved at grid
         resolution (<level>)` — steepness has NO valid-failure branch (§1.2, R1); a pass claims §1.1′'s consistency only.
  T-S2   no hysteresis: the same procedure on the skeleton-low sweep gives m̂_low; pass iff |m̂_low − m̂_c| ≤ Δm (0.1201);
         m̂_low > m̂_c + Δm — a hysteretic signature, two distinct boundaries, the mark of a discontinuous transition, which
         the transcritical form excludes — fails validly `hysteresis`.
  T-R1′  rounded continuation: realization sweep; med(m) positive at every level (else fails validly `realization extinct at
         <level>`); non-decreasing under the evaluability rule; continuity-compatible in the T-S1c sense.
P1 = PRODUCED iff all four pass; NOT PRODUCED iff any fails validly (named causes); NOT DISTINGUISHED iff any is unevaluable
or returns its ND branch. `PRODUCED` carries exactly §1.1′'s inferential strength (finite-horizon persistence at the declared
size, horizon, panel and resolution — never a thermodynamic critical point). The scientific determination `NOT PRODUCED` is
distinct in name and jurisdiction from M4's `NOT_PRODUCED` label (§4.7).

EVALUABILITY RULE (§4.11; every monotonicity clause uses it). A reversal med(m₊) < med(m₋) between adjacent levels in a
test's domain is DISREGARDED iff its magnitude ≤ k_R·√(ŝ_X(m₋)² + ŝ_X(m₊)²)·1.2533/√20 — the bound on the difference of two
independent noisy medians — with X the sweep's own committed object: ŝ_sk from the skeleton part of the calibration census
for the skeleton sweeps, ŝ from the realization part for the realization sweep (M5 `evaluability_band`; no cross-object
stand-in). A reversal beyond the band is an EVALUABILITY OUTCOME: NOT DISTINGUISHED, cause `non-monotone at finite sample
(<levels>)`; at a 20-seed panel it is never a valid scientific failure of the present instrument.

PER RUN. survival = tail active count > 0 throughout every tail window (M1: the window MINIMUM); ρ̂ = tail-window mean density
over the whole tail with zero contributions after an extinction (M1 `rho_tail_mean`, as placed). An extinct run is a valid
observation, never "missing": extinct before the tail → survival 0, ρ̂ 0; extinct inside the tail → survival 0, ρ̂ > 0 (the
pre-extinction contributions; L2 M-P1 r1 D4 — the evaluator carries M1's observable unchanged and recomputes it from the
persisted trace, D3; any other aggregate is a ruling on M1, not an M-P1 coercion). A run that halts on an apparatus error is UNEVALUABLE; a level with any
unevaluable seed is unevaluable; an unevaluable level inside a test's domain makes that test NOT DISTINGUISHED (apparatus),
recorded with the halt key.

FIDELITY TIER (§1.2′; recorded with bands, never scored): (i) m̂_c − 1 and m̂_c − m_lat; (ii) med against ρ*_sk and the pair
skeleton branch above the boundary, and against ρ*(m; η₀) and the pair realization branch across the sweep, with the fidelity
band k_R·ŝ(m)·1.2533/√20; (iii) m̂_infl (steepest ascent by central differences on the pass-1 grid, interior levels, ties → the
lower level; `inflection at sweep edge` flag) against m_infl and m̂_c; (iv) the below-boundary ratio med(m)/med(m̂_c + Δm) over
m < m̂_c − Δm. Bad agreement is published as such, never recast.

KNOWN-ANSWER QUALIFICATION (§4.11, §5.4; apparatus prerequisite, passage required). Synthetic sweeps from the map with declared
noise, DISCRIMINATING BY CONSTRUCTION: the per-seed noise amplitude is below half the applicable evaluability band at every
level except where a control injects its feature, so only the intended branch can trigger. Classes: continuous crossing at
m_c ∈ {0.8, 1.0, 1.25} (must pass all four); crossing below / above the sweep (must fail T-S1′ with its cause); a steep
continuous branch (must yield ND continuity, never a valid failure); a hysteretic pair at 2·Δm (must fail T-S2 `hysteresis`);
a realization extinct at one level (must fail T-R1′ `realization extinct`); a single injected reversal of 2× the combined band
(must yield ND `non-monotone at finite sample`). CROSS-TRIGGER RULE: the intended verdict with a cause other than its named one
FAILS the qualification. Passage = every class returns exactly its named verdict and cause on ≥ 95 of 100 replicates. These test
the evaluator's implementation; they validate no closure against the lattice (Appendix B.5).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import closure as CL
from . import config as C
from .config import F8_LEVELS_MICRO, level_id

EVALUATOR_VERSION = "f8_stage1_mp1_v1"
PANEL_N = 20
SURV_THRESHOLD = 18                       # ratified: freeze record §3 item 24
F_J = 0.25                                # ratified: item 13 (ND branch only)
K_R = CL.K_R                              # 3 (item 17)
SWEEP_OBJECTS = ("skeleton_high", "skeleton_low", "realization")
TESTS = ("T-S1'", "T-S1c", "T-S2", "T-R1'")
OUTCOMES = ("PASS", "FAIL", "ND")
P1_DETERMINATIONS = ("PRODUCED", "NOT PRODUCED", "NOT DISTINGUISHED")
VALID_FAILURE_CAUSES = ("no active phase in sweep", "no inactive phase in sweep", "hysteresis", "realization extinct")
ND_CAUSE_KINDS = ("non-monotone survival", "continuity unresolved at grid resolution", "non-monotone at finite sample", "apparatus")
KNOWN_ANSWER_MC = (0.8, 1.0, 1.25)        # ratified: item 21
KNOWN_ANSWER_SWEEPS = 100                 # item 21
KNOWN_ANSWER_PASS_MIN = 95                # item 21
KNOWN_ANSWER_MASTER = 520261028           # declared: the synthetic corpus master (separate from every other declared master)
SYNTHETIC_S_HAT = 0.01                    # declared: the synthetic census's ŝ_X(m) at every level (both objects) for the corpus
KA_CLASSES = ("pass_crossing_0.8", "pass_crossing_1.0", "pass_crossing_1.25", "fail_no_inactive_phase", "fail_no_active_phase",
              "nd_steep_continuous", "fail_hysteresis", "fail_realization_extinct", "nd_injected_reversal")

RATIO_UNCERTAINTY_CONVENTION = ("comparison (iv) is reported as the ratio of two seed medians with their two calibrated widths "
                                "k_R*s_hat(m)*1.2533/sqrt(20) stated separately (numerator level and reference level); no propagated "
                                "ratio band, coverage or covariance assumption is claimed")   # declared (D7)

EVALUATOR_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("version", EVALUATOR_VERSION), ("panel_n", PANEL_N), ("surv_threshold", SURV_THRESHOLD), ("f_j", F_J), ("k_r", K_R),
    ("median_se_factor", CL.MEDIAN_SE_FACTOR), ("sweep_objects", SWEEP_OBJECTS), ("tests", TESTS), ("outcomes", OUTCOMES),
    ("p1_determinations", P1_DETERMINATIONS), ("valid_failure_causes", VALID_FAILURE_CAUSES), ("nd_cause_kinds", ND_CAUSE_KINDS),
    ("known_answer_mc", KNOWN_ANSWER_MC), ("known_answer_sweeps", KNOWN_ANSWER_SWEEPS), ("known_answer_pass_min", KNOWN_ANSWER_PASS_MIN),
    ("known_answer_master", KNOWN_ANSWER_MASTER), ("synthetic_s_hat", SYNTHETIC_S_HAT), ("ka_classes", KA_CLASSES),
    ("claim_strength", "finite-horizon persistence at the declared N, T, panel and resolution; not a thermodynamic critical point (s1.1')"),
    ("jurisdiction", "P1 adjudicated here alone; M4 verdicts never bear on P1 (s4.7)"),
    ("ratio_uncertainty_convention", RATIO_UNCERTAINTY_CONVENTION),
)
EVALUATOR_SHA256_LITERAL = "cc1f176eb12dde347351f77ddf661dfa7fdb6f9662d83be28906155687a5d86f"


class EvaluatorDomainError(ValueError):
    """Frozen identity violated or input outside the evaluator's domain."""


def _digest(obj) -> str: return hashlib.sha256(repr(obj).encode()).hexdigest()
def _canon(obj) -> str: return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def verify_frozen_identity() -> None:
    if _digest(EVALUATOR_DECLARATION) != EVALUATOR_SHA256_LITERAL:
        raise EvaluatorDomainError("evaluator declaration differs from its frozen literal digest")
    CL.verify_frozen_identity()
    d = dict(EVALUATOR_DECLARATION)
    live = {"panel_n": PANEL_N, "surv_threshold": SURV_THRESHOLD, "f_j": F_J, "k_r": K_R, "median_se_factor": CL.MEDIAN_SE_FACTOR, "sweep_objects": SWEEP_OBJECTS,
            "tests": TESTS, "outcomes": OUTCOMES, "p1_determinations": P1_DETERMINATIONS, "valid_failure_causes": VALID_FAILURE_CAUSES, "nd_cause_kinds": ND_CAUSE_KINDS,
            "known_answer_mc": KNOWN_ANSWER_MC, "known_answer_sweeps": KNOWN_ANSWER_SWEEPS, "known_answer_pass_min": KNOWN_ANSWER_PASS_MIN,
            "known_answer_master": KNOWN_ANSWER_MASTER, "synthetic_s_hat": SYNTHETIC_S_HAT, "ka_classes": KA_CLASSES, "version": EVALUATOR_VERSION,
            "ratio_uncertainty_convention": RATIO_UNCERTAINTY_CONVENTION}
    for k_, v_ in live.items():
        if d[k_] != v_ or type(d[k_]) is not type(v_):
            raise EvaluatorDomainError(f"evaluator declaration field {k_} differs from the live global")
    if (PANEL_N, SURV_THRESHOLD, F_J, K_R, KNOWN_ANSWER_MC, KNOWN_ANSWER_SWEEPS, KNOWN_ANSWER_PASS_MIN) != (20, 18, 0.25, 3, (0.8, 1.0, 1.25), 100, 95):
        raise EvaluatorDomainError("evaluator constants differ from the ratified values (freeze record §3 items 13, 17, 21, 24)")
    if KNOWN_ANSWER_MASTER in (C.F8_SEED_PANEL_MASTER, C.F8_CALIBRATION_MASTER, CL.PROJECTION_MASTER, 20260917):
        raise EvaluatorDomainError("known-answer master collides with another declared master")


# ----------------------------------------------------------------------------- sweep records (the evaluator's inputs)
@dataclass(frozen=True)
class LevelData:
    """One pass-1 level of one sweep: the 20 seeds' (survival, ρ̂) in panel order, or unevaluable with its halt key."""
    level_micro: int
    survivals: Tuple[bool, ...]            # 20, panel order (empty if unevaluable)
    rho_hats: Tuple[float, ...]            # 20, panel order (empty if unevaluable)
    unevaluable: bool = False
    halt_key: str = ""
    run_spec_hashes: Tuple[str, ...] = ()  # provenance, panel order (empty for synthetic)
    run_rho_sha256s: Tuple[str, ...] = () # identity of each run's persisted density record (M1 `F8RunResult.rho_sha256`), panel order (empty for synthetic)

    @property
    def surv(self) -> int: return sum(1 for s in self.survivals if s)

    @property
    def med(self) -> float: return float(np.median(np.asarray(self.rho_hats, dtype=np.float64)))


@dataclass(frozen=True)
class SweepRecord:
    """One of the three canonical sweeps (or a synthetic one): 24 levels of LevelData for one committed object."""
    obj: str                               # skeleton_high | skeleton_low | realization
    role: str                              # canonical | synthetic
    levels: Tuple[LevelData, ...]
    declaration_sha256: str
    result_sha256: str = ""

    def identity(self) -> str:
        d = asdict(self); d.pop("result_sha256", None); return hashlib.sha256(_canon(d).encode()).hexdigest()


SWEEP_ROLES = ("canonical", "synthetic")


def observation_from_result(r, spec) -> Tuple[bool, float, Tuple[float, ...]]:
    """Recompute (survival, ρ̂, tail-window means) from the result's persisted active-count trace with M1's frozen count-grid
    arithmetic (dynamics.py `run`, M1-r3: one integer sum, one division per quantity; survival = window MINIMUM > 0 for every
    tail window). The persisted trace is the observation; the result's cached summary fields must equal this recomputation
    exactly (L2 M-P1 r1 D3). ρ̂ is the mean over the WHOLE tail with zero contributions after an extinction — M1's placed
    definition, which the evaluator carries unchanged (L2 M-P1 r1 D4): a run extinct inside the tail is a valid observation
    with survival False and ρ̂ > 0."""
    T, n, tail_ticks, window = spec.ticks, spec.n_cells, spec.tail_ticks, spec.window
    counts = np.asarray(r.active_counts)
    if counts.dtype != np.int64 or counts.shape != (T + 1,): raise EvaluatorDomainError("active-count trace is not an int64 vector of length ticks + 1")
    if np.any(counts < 0) or np.any(counts > n): raise EvaluatorDomainError("active counts outside [0, n_cells]")
    rho = np.asarray(r.rho)
    if rho.dtype != np.float64 or rho.shape != (T + 1,) or not np.array_equal(rho, counts.astype(np.float64) / np.float64(n)):
        raise EvaluatorDomainError("density record does not equal active_counts / n_cells")
    nwin = tail_ticks // window
    tail_counts = counts[T - tail_ticks + 1:]
    wins = tuple(float(np.float64(int(tail_counts[i * window:(i + 1) * window].sum())) / np.float64(window * n)) for i in range(nwin))
    survival = all(int(tail_counts[i * window:(i + 1) * window].min()) > 0 for i in range(nwin))
    rho_hat = float(np.float64(int(tail_counts.sum())) / np.float64(tail_ticks * n))
    if spec.eta_floor == 0.0:                                 # skeleton: exactly absorbing — zeros after the first zero, extinction tick consistent
        zeros = np.flatnonzero(counts == 0)
        ext = int(zeros[0]) if zeros.size else None
        if ext is not None and np.any(counts[ext:] != 0): raise EvaluatorDomainError("absorbing skeleton trace is non-zero after extinction")
        if r.extinction_tick != ext: raise EvaluatorDomainError("cached extinction tick does not equal the trace's first zero")
    return bool(survival), rho_hat, wins


def sweep_from_results(obj: str, results_by_level: Dict[int, Sequence], halts_by_level: Optional[Dict[int, str]] = None) -> SweepRecord:
    """Build a CANONICAL sweep record from M1 `F8RunResult`s: for each pass-1 level either the 20 canonical-panel results
    (specs reconstructed and matched — a result off the panel, of another object or shape is refused; the persisted trace
    validated at the production shape and the cached summary fields recomputed from it, D3) or a halt key. The level
    carries each run's spec hash AND density-record identity, so the sweep identity binds the observation, not only the
    specification."""
    verify_frozen_identity()
    from . import dynamics as D
    if obj not in SWEEP_OBJECTS: raise EvaluatorDomainError(f"unknown sweep object {obj!r}")
    halts = dict(halts_by_level or {})
    panel = tuple(C.F8_SEED_PANEL); levels: List[LevelData] = []
    for u in F8_LEVELS_MICRO:
        if u in halts:
            if u in results_by_level: raise EvaluatorDomainError(f"level {u}: both results and a halt supplied")
            if not isinstance(halts[u], str) or not halts[u]: raise EvaluatorDomainError("halt key must be a non-empty string")
            levels.append(LevelData(u, (), (), True, halts[u], (), ())); continue
        rs = list(results_by_level.get(u, ()))
        if len(rs) != PANEL_N: raise EvaluatorDomainError(f"level {u}: {len(rs)} results, need {PANEL_N} (or a halt key)")
        by_seed = {}
        for r in rs:
            if type(r) is not D.F8RunResult: raise EvaluatorDomainError(f"level {u}: not an M1 F8RunResult")
            if r.obj != obj or r.level_micro != u: raise EvaluatorDomainError(f"level {u}: result object/level mismatch")
            try: spec = C.f8_run_spec(u, r.seed, obj)
            except C.F8ConfigError as e: raise EvaluatorDomainError(f"level {u}: not a canonical-panel production-shape run: {e}") from e
            if r.spec_hash != spec.spec_hash() or tuple(r.stream_key) != spec.stream_key: raise EvaluatorDomainError(f"level {u}: spec hash / stream key do not reconstruct")
            surv, rho_hat, wins = observation_from_result(r, spec)
            if bool(r.survival) != surv or float(r.rho_tail_mean) != rho_hat or tuple(r.tail_window_means) != wins:
                raise EvaluatorDomainError(f"level {u}, seed {r.seed}: cached summary (survival, rho_tail_mean, tail_window_means) does not recompute from the persisted trace")
            if r.seed in by_seed: raise EvaluatorDomainError(f"level {u}: duplicate seed {r.seed}")
            by_seed[r.seed] = r
        if set(by_seed) != set(panel): raise EvaluatorDomainError(f"level {u}: seeds are not exactly the canonical panel")
        ordered = [by_seed[sd] for sd in panel]
        levels.append(LevelData(u, tuple(bool(r.survival) for r in ordered), tuple(float(r.rho_tail_mean) for r in ordered), False, "",
                                tuple(r.spec_hash for r in ordered), tuple(r.rho_sha256() for r in ordered)))
    rec = SweepRecord(obj, "canonical", tuple(levels), EVALUATOR_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(rec, result_sha256=rec.identity())


_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def validate_sweep_record(s: SweepRecord, results_by_level: Optional[Dict[int, Sequence]] = None, halts_by_level: Optional[Dict[int, str]] = None) -> None:
    """Structural validation; with the original run records supplied, validation by REPLAY (the sweep must equal the one
    `sweep_from_results` rebuilds from them, D3)."""
    if type(s) is not SweepRecord: raise EvaluatorDomainError("not a SweepRecord")
    if s.obj not in SWEEP_OBJECTS or s.role not in SWEEP_ROLES or s.declaration_sha256 != EVALUATOR_SHA256_LITERAL: raise EvaluatorDomainError("sweep record header invalid")
    if s.result_sha256 != s.identity(): raise EvaluatorDomainError("sweep record identity does not match its content")
    if tuple(l.level_micro for l in s.levels) != tuple(F8_LEVELS_MICRO): raise EvaluatorDomainError("sweep levels are not the frozen pass-1 grid")
    for l in s.levels:
        if l.unevaluable:
            if l.survivals or l.rho_hats or l.run_spec_hashes or l.run_rho_sha256s or not l.halt_key: raise EvaluatorDomainError("an unevaluable level carries only its halt key")
        else:
            if len(l.survivals) != PANEL_N or len(l.rho_hats) != PANEL_N or l.halt_key: raise EvaluatorDomainError("an evaluable level carries exactly 20 seeds and no halt key")
            if any(not (0.0 <= x <= 1.0) for x in l.rho_hats): raise EvaluatorDomainError("ρ̂ must lie in [0, 1]")
            # D4: survival True requires ρ̂ > 0 (every window minimum > 0 ⇒ positive tail sum); the converse is NOT required —
            # a run extinct inside the tail has survival False and ρ̂ > 0 under M1's placed tail-mean definition.
            if any(sv and not (x > 0.0) for x, sv in zip(l.rho_hats, l.survivals)): raise EvaluatorDomainError("a surviving run cannot have zero tail density")
            if s.role == "canonical":
                if len(l.run_spec_hashes) != PANEL_N or len(l.run_rho_sha256s) != PANEL_N: raise EvaluatorDomainError("a canonical level carries 20 run spec hashes and 20 density-record identities")
                if any(not _HEX64.match(h) for h in l.run_rho_sha256s): raise EvaluatorDomainError("density-record identities must be SHA-256 hex")
                for si, sd in enumerate(C.F8_SEED_PANEL):
                    if l.run_spec_hashes[si] != C.f8_run_spec(l.level_micro, sd, s.obj).spec_hash(): raise EvaluatorDomainError("canonical run spec hash does not reconstruct")
            elif l.run_spec_hashes or l.run_rho_sha256s: raise EvaluatorDomainError("a synthetic level carries no run provenance")
    if results_by_level is not None:
        if s.role != "canonical": raise EvaluatorDomainError("replay validation applies to canonical sweeps")
        if s != sweep_from_results(s.obj, results_by_level, halts_by_level): raise EvaluatorDomainError("sweep record does not replay from the supplied run records")


# ----------------------------------------------------------------------------- the evaluability band
def band(census: CL.CalibrationCensus, obj: str, i_lo: int, i_hi: int) -> float:
    """The combined two-level band (§4.11) from the calibration census for the sweep's own object."""
    return CL.evaluability_band(census, obj, i_lo, i_hi)


# ----------------------------------------------------------------------------- test results and the P1 determination
@dataclass(frozen=True)
class TestResult:
    test: str
    outcome: str                           # PASS | FAIL | ND
    cause: Optional[str]                   # named cause for FAIL/ND; None for PASS
    detail: Tuple[Tuple[str, object], ...] = ()


def _level_value(u: int) -> float: return CL.level_m(u)


def _boundary(sweep: SweepRecord) -> Tuple[Optional[int], Optional[TestResult], Optional[str]]:
    """T-S1′'s procedure on a skeleton sweep. Returns (index of m̂_c, failure/ND result or None, apparatus halt key or None).
    The domain is every level: any unevaluable level makes the test ND (apparatus)."""
    for l in sweep.levels:
        if l.unevaluable: return None, TestResult("T-S1'", "ND", f"apparatus ({l.halt_key})", (("level", level_id(l.level_micro)),)), l.halt_key
    surv = [l.surv for l in sweep.levels]
    hi = [i for i, s in enumerate(surv) if s >= SURV_THRESHOLD]
    if not hi: return None, TestResult("T-S1'", "FAIL", "no active phase in sweep", (("surv", tuple(surv)),)), None
    if all(s >= SURV_THRESHOLD for s in surv): return None, TestResult("T-S1'", "FAIL", "no inactive phase in sweep", (("surv", tuple(surv)),)), None
    # m̂_c: lowest level with surv ≥ 18 such that surv ≥ 18 at every level above it
    c = None
    for i in range(len(surv)):
        if all(s >= SURV_THRESHOLD for s in surv[i:]): c = i; break
    if c is None or any(s >= SURV_THRESHOLD for s in surv[:c]):
        # ≥ 18 somewhere but not monotone above it (c is None cannot happen once hi is nonempty since the top level alone satisfies the suffix condition)
        return None, TestResult("T-S1'", "ND", "non-monotone survival", (("surv", tuple(surv)),)), None
    return c, None, None


def _monotone_and_continuity(sweep: SweepRecord, census: CL.CalibrationCensus, start: int, test: str) -> Optional[TestResult]:
    """The shared T-S1c / T-R1′ body on levels start..end: unevaluable → ND apparatus; beyond-band reversal → ND non-monotone;
    increase > f_J × range → ND continuity. Returns None when the clauses pass."""
    lv = sweep.levels
    for l in lv[start:]:
        if l.unevaluable: return TestResult(test, "ND", f"apparatus ({l.halt_key})", (("level", level_id(l.level_micro)),))
    meds = [l.med for l in lv]
    rng = meds[-1] - meds[start]
    for i in range(start, len(lv) - 1):
        d = meds[i + 1] - meds[i]
        if d < 0.0:
            b = band(census, sweep.obj, i, i + 1)
            if -d > b:
                return TestResult(test, "ND", f"non-monotone at finite sample ({level_id(lv[i].level_micro)}, {level_id(lv[i + 1].level_micro)})",
                                  (("reversal", -d), ("band", b)))
    for i in range(start, len(lv) - 1):
        d = meds[i + 1] - meds[i]
        # EVERY increase is compared with f_J × range, whatever the sign of the range (L2 M-P1 r1 D2): with a zero or
        # negative endpoint range (reachable because within-band reversals are disregarded) the allowed increase is ≤ 0,
        # so any positive increment is an excess; non-positive increments are governed by the reversal clause above only.
        if d > 0.0 and d > F_J * rng:
            return TestResult(test, "ND", f"continuity unresolved at grid resolution ({level_id(lv[i + 1].level_micro)})", (("increase", d), ("f_J_times_range", F_J * rng)))
    return None


def t_s1_prime(skeleton_high: SweepRecord) -> Tuple[TestResult, Optional[int]]:
    c, res, _ = _boundary(skeleton_high)
    if res is not None: return res, None
    return TestResult("T-S1'", "PASS", None, (("m_hat_c", level_id(skeleton_high.levels[c].level_micro)), ("index", c))), c


def t_s1c(skeleton_high: SweepRecord, census: CL.CalibrationCensus, c_index: int) -> TestResult:
    r = _monotone_and_continuity(skeleton_high, census, c_index, "T-S1c")
    return r if r is not None else TestResult("T-S1c", "PASS", None, (("claim", "consistency with a continuous onset at resolution s (s1.1')"),))


def t_s2(skeleton_low: SweepRecord, c_index: int, delta_m: float) -> TestResult:
    lo_idx, res, _ = _boundary(skeleton_low)
    if res is not None:
        return TestResult("T-S2", res.outcome, res.cause, (("from", "skeleton-low boundary"),) + res.detail)
    m_c = _level_value(F8_LEVELS_MICRO[c_index]); m_low = _level_value(F8_LEVELS_MICRO[lo_idx])
    sep = abs(m_low - m_c)
    detail = (("m_hat_low", level_id(F8_LEVELS_MICRO[lo_idx])), ("m_hat_c", level_id(F8_LEVELS_MICRO[c_index])), ("separation", sep), ("delta_m", delta_m))
    if sep <= delta_m: return TestResult("T-S2", "PASS", None, detail)
    return TestResult("T-S2", "FAIL", "hysteresis", detail)


def t_r1_prime(realization: SweepRecord, census: CL.CalibrationCensus) -> TestResult:
    for l in realization.levels:
        if l.unevaluable: return TestResult("T-R1'", "ND", f"apparatus ({l.halt_key})", (("level", level_id(l.level_micro)),))
    for l in realization.levels:
        if not (l.med > 0.0): return TestResult("T-R1'", "FAIL", f"realization extinct at {level_id(l.level_micro)}", (("level", level_id(l.level_micro)),))
    r = _monotone_and_continuity(realization, census, 0, "T-R1'")
    return r if r is not None else TestResult("T-R1'", "PASS", None, ())


def p1_determination(results: Sequence[TestResult]) -> Tuple[str, Optional[str]]:
    """PRODUCED iff all four pass; NOT PRODUCED iff any fails validly (first named cause in test order); else NOT DISTINGUISHED."""
    if all(r.outcome == "PASS" for r in results): return "PRODUCED", None
    fails = [r for r in results if r.outcome == "FAIL"]
    if fails: return "NOT PRODUCED", fails[0].cause
    nds = [r for r in results if r.outcome == "ND"]
    return "NOT DISTINGUISHED", nds[0].cause if nds else None


# ----------------------------------------------------------------------------- the fidelity tier (recorded, never scored)
@dataclass(frozen=True)
class FidelityTier:
    """Recorded, never scored (§1.2′). Reporting per L2 M-P1 r1 D7: comparison (ii) rows carry the SIGNED residuals
    observed − closure and observed − pair explicitly; comparison (iv) names the actual grid reference level selected under
    MP1-4 (the first pass-1 level ≥ m̂_c + Δm) with its median, and reports the numerator and reference calibrated widths
    SEPARATELY (RATIO_UNCERTAINTY_CONVENTION); when no ratio is available the reason is named."""
    m_hat_c: Optional[float]
    shift_vs_closure: Optional[float]          # m̂_c − 1
    shift_vs_pair: Optional[float]             # m̂_c − m_lat
    skeleton_vs_rho_sk: Tuple[Tuple[str, float, float, float, float, float, float], ...]      # (level, med, ρ*_sk, pair_sk, band, med − ρ*_sk, med − pair_sk) above the boundary
    realization_vs_rho_re: Tuple[Tuple[str, float, float, float, float, float, float], ...]   # (level, med, ρ*, pair_re, band, med − ρ*, med − pair_re) across the sweep
    m_hat_infl: Optional[float]
    inflection_at_sweep_edge: bool
    shift_infl_vs_closure: Optional[float]     # m̂_infl − m_infl
    shift_infl_vs_boundary: Optional[float]    # m̂_infl − m̂_c
    ratio_reference: Optional[Tuple[str, float, float]]      # (reference level actually selected, med there, its width k_R·ŝ·1.2533/√20)
    ratio_unavailable_reason: str              # "" when ratios are available; else the named reason
    below_boundary_ratios: Tuple[Tuple[str, float, float, float], ...]   # (level, med(m), med(m)/med(ref), numerator width) over m < m̂_c − Δm
    delta_m: float


def steepest_ascent(realization: SweepRecord) -> Tuple[Optional[float], bool]:
    """m̂_infl: the pass-1 level at which the central difference [med(m₊) − med(m₋)]/(m₊ − m₋) is maximal (interior levels;
    ties → the lower level). The edge flag is set when the one-sided slope at an endpoint exceeds every interior one."""
    lv = realization.levels
    if any(l.unevaluable for l in lv): return None, False
    meds = [l.med for l in lv]; ms = [_level_value(l.level_micro) for l in lv]
    best, best_i = -math.inf, None
    for i in range(1, len(lv) - 1):
        d = (meds[i + 1] - meds[i - 1]) / (ms[i + 1] - ms[i - 1])
        if d > best: best, best_i = d, i
    edge = max((meds[1] - meds[0]) / (ms[1] - ms[0]), (meds[-1] - meds[-2]) / (ms[-1] - ms[-2])) > best
    return ms[best_i], edge


def fidelity_tier(skeleton_high: SweepRecord, realization: SweepRecord, census: CL.CalibrationCensus, c_index: Optional[int], pub: CL.ClosurePublication) -> FidelityTier:
    dm = pub.delta_m.value
    m_c = _level_value(F8_LEVELS_MICRO[c_index]) if c_index is not None else None
    sk_rows = []; re_rows = []; ratios = []; ref_row = None; reason = ""
    for i, u in enumerate(F8_LEVELS_MICRO):
        fb = CL.fidelity_band(census, i)
        if not realization.levels[i].unevaluable:
            med = realization.levels[i].med
            re_rows.append((level_id(u), med, pub.rho_re[i], pub.pair_re[i], fb, med - pub.rho_re[i], med - pub.pair_re[i]))
        if c_index is not None and i >= c_index and not skeleton_high.levels[i].unevaluable:
            med = skeleton_high.levels[i].med
            sk_rows.append((level_id(u), med, pub.rho_sk[i], pub.pair_sk[i], fb, med - pub.rho_sk[i], med - pub.pair_sk[i]))
    if c_index is None: reason = "no located boundary (T-S1' did not pass)"
    elif any(l.unevaluable for l in realization.levels): reason = "apparatus: an unevaluable realization level"
    else:
        ref_idx = next((i for i, u in enumerate(F8_LEVELS_MICRO) if _level_value(u) >= m_c + dm), None)
        if ref_idx is None: reason = "reference level m_hat_c + delta_m lies above the sweep"
        elif not (realization.levels[ref_idx].med > 0.0): reason = f"non-positive reference median at {level_id(F8_LEVELS_MICRO[ref_idx])}"
        else:
            ref = realization.levels[ref_idx].med
            ref_row = (level_id(F8_LEVELS_MICRO[ref_idx]), ref, CL.fidelity_band(census, ref_idx))
            ratios = [(level_id(u), realization.levels[i].med, realization.levels[i].med / ref, CL.fidelity_band(census, i))
                      for i, u in enumerate(F8_LEVELS_MICRO) if _level_value(u) < m_c - dm]
            if not ratios: reason = "no pass-1 level below m_hat_c - delta_m"
    m_infl_hat, edge = steepest_ascent(realization)
    return FidelityTier(m_c, (m_c - 1.0) if m_c is not None else None, (m_c - pub.m_lat) if m_c is not None else None, tuple(sk_rows), tuple(re_rows),
                        m_infl_hat, edge, (m_infl_hat - pub.m_infl) if m_infl_hat is not None else None,
                        (m_infl_hat - m_c) if (m_infl_hat is not None and m_c is not None) else None, ref_row, reason, tuple(ratios), dm)


# ----------------------------------------------------------------------------- the P1 evaluation record
@dataclass(frozen=True)
class P1Evaluation:
    role: str                                  # canonical | synthetic
    determination: str                         # PRODUCED | NOT PRODUCED | NOT DISTINGUISHED
    cause: Optional[str]
    tests: Tuple[TestResult, ...]
    m_hat_c: Optional[str]
    fidelity: Optional[FidelityTier]
    census_sha256: str
    publication_sha256: str
    sweep_sha256s: Tuple[str, str, str]
    claim_strength: str
    declaration_sha256: str
    result_sha256: str = ""

    def identity(self) -> str:
        d = asdict(self); d.pop("result_sha256", None); return hashlib.sha256(_canon(d).encode()).hexdigest()


def evaluate_p1(skeleton_high: SweepRecord, skeleton_low: SweepRecord, realization: SweepRecord, census: CL.CalibrationCensus,
                pub: Optional[CL.ClosurePublication] = None) -> P1Evaluation:
    """The four tests in order, the determination, the fidelity tier. Δm is Appendix A's, read from the closure publication,
    which must REPLAY to M5's frozen content (L2 M-P1 r1 D1): there is no Δm override at this entry point, and a publication
    whose content differs from the frozen one — with its original identity retained or recomputed — is refused by M5's replay
    validator before any test runs. (`t_s2`'s `delta_m` argument is reachable only from unit tests of that one function.)
    A synthetic census is admissible only with synthetic sweeps."""
    verify_frozen_identity()
    for s, o in ((skeleton_high, "skeleton_high"), (skeleton_low, "skeleton_low"), (realization, "realization")):
        validate_sweep_record(s)
        if s.obj != o: raise EvaluatorDomainError(f"sweep passed as {o} has object {s.obj}")
    roles = {skeleton_high.role, skeleton_low.role, realization.role}
    if len(roles) != 1: raise EvaluatorDomainError("the three sweeps must share a role")
    role = roles.pop()
    CL.validate_calibration_census(census)
    if role == "canonical" and census.role != "canonical": raise EvaluatorDomainError("a canonical P1 evaluation requires the canonical (M7-issued) calibration census")
    if pub is None: pub = CL.closure_publication()
    try: CL.validate_closure_publication(pub)
    except CL.ClosureDomainError as e: raise EvaluatorDomainError(f"closure publication refused: {e}") from e
    dm = pub.delta_m.value
    r1, c = t_s1_prime(skeleton_high)
    if c is None:
        r2 = TestResult("T-S1c", "ND", f"not evaluable: T-S1' did not locate a boundary ({r1.cause})", ())
        r3 = TestResult("T-S2", "ND", f"not evaluable: T-S1' did not locate a boundary ({r1.cause})", ())
    else:
        r2 = t_s1c(skeleton_high, census, c); r3 = t_s2(skeleton_low, c, dm)
    r4 = t_r1_prime(realization, census)
    tests = (r1, r2, r3, r4)
    det, cause = p1_determination(tests)
    fid = fidelity_tier(skeleton_high, realization, census, c, pub) if pub is not None else None
    ev = P1Evaluation(role, det, cause, tests, level_id(F8_LEVELS_MICRO[c]) if c is not None else None, fid, census.result_sha256, pub.result_sha256,
                      (skeleton_high.result_sha256, skeleton_low.result_sha256, realization.result_sha256),
                      "finite-horizon persistence at the declared N, T, panel and resolution (s1.1'); never a thermodynamic critical point", EVALUATOR_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(ev, result_sha256=ev.identity())


# ----------------------------------------------------------------------------- known-answer corpus (§4.11, §5.4)
def synthetic_census(s_hat: float = SYNTHETIC_S_HAT) -> CL.CalibrationCensus:
    """A declared SYNTHETIC census for the corpus: ŝ_X(m) = s_hat at every level for both objects, built as a real census
    object from provenance-valid CalibrationRun shells (so the band arithmetic is the production path) with role
    derived_provisional. Its rows are constants ± a two-point spread that gives ddof-1 SD exactly s_hat."""
    verify_frozen_identity()
    runs = []
    a = s_hat * math.sqrt(PANEL_N - 1) / math.sqrt(PANEL_N)      # ±a alternating over 20 gives SD(ddof=1) = s_hat exactly
    for u in F8_LEVELS_MICRO:
        for si, sd in enumerate(C.F8_CALIBRATION_SEED_PANEL):
            for obj in CL.CALIBRATION_OBJECTS:
                spec = C.f8_run_spec(u, sd, obj, panel="calibration")
                val = 0.5 + (a if si % 2 == 0 else -a)
                runs.append(CL.CalibrationRun(u, sd, obj, spec.spec_hash(), spec.stream_key, val, True, "00" * 32))
    return CL.calibration_census(runs)


def _synthetic_sweep(obj: str, meds: Sequence[float], survs: Sequence[int], noise_amp: float, g: np.random.Generator,
                     feature: Optional[Dict[int, Tuple[float, float]]] = None) -> SweepRecord:
    """Per level: 20 seeds with ρ̂ = med ± uniform(−noise_amp, noise_amp) (the median of the 20 then lies within noise_amp of
    `med`), survivals = the first `surv` seeds. `feature` injects (med, amp) at given level indices."""
    levels = []
    for i, u in enumerate(F8_LEVELS_MICRO):
        m, amp = (feature or {}).get(i, (meds[i], noise_amp))
        vals = np.clip(m + g.uniform(-amp, amp, PANEL_N), 0.0, 1.0) if m > 0.0 else np.zeros(PANEL_N)
        if obj.startswith("skeleton"):
            sv = [k < survs[i] for k in range(PANEL_N)]
            vals = np.where(sv, np.maximum(vals, 1e-9) if m > 0.0 else 0.0, 0.0)   # non-survivors contribute 0; survivors positive
            if survs[i] > 0 and m <= 0.0: vals = np.where(sv, 1e-6, 0.0)
        else:
            sv = [m > 0.0] * PANEL_N                                          # an extinct realization level is non-surviving (M1's observable)
        levels.append(LevelData(u, tuple(bool(x) for x in sv), tuple(float(x) for x in vals), False, "", (), ()))
    rec = SweepRecord(obj, "synthetic", tuple(levels), EVALUATOR_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(rec, result_sha256=rec.identity())


def _branch(m_c: float, kind: str) -> List[float]:
    """The map's branch shifted so its crossing sits at m_c: skeleton ρ*_sk(m − m_c + 1); realization ρ*(m − m_c + 1; η₀)."""
    out = []
    for u in F8_LEVELS_MICRO:
        m = _level_value(u) - m_c + 1.0
        out.append(CL.rho_sk(m) if kind == "skeleton" else CL.rho_re(max(m, 1e-6)))
    return out


def steep_continuous_branch(m_c: float = 1.0) -> List[float]:
    """The steep-continuous control (MP1-3, repaired per L2 M-P1 r1 D5). Let c be the first pass-1 index with m > m_c, sk the
    map's skeleton branch shifted to m_c, R = sk[-1] − sk[c] the sampled range above the boundary, J = 2·f_J·R the declared
    first rise. The control is the piecewise-linear interpolant through the samples: steep[c] = sk[c]; steep[c+1] = sk[c] + J
    (the first adjacent rise is EXACTLY J); for i ≥ c+1 the remaining range R − J is distributed over the levels above c+1 in
    proportion to the original branch's rise above level c+1, so the endpoint sk[-1] is preserved and the branch stays
    non-decreasing. Below c the branch is the original (survival is 0 there and T-S1c's domain starts at c)."""
    ms = [_level_value(u) for u in F8_LEVELS_MICRO]
    sk = _branch(m_c, "skeleton"); c = next(i for i, m in enumerate(ms) if m > m_c)
    R = sk[-1] - sk[c]; J = 2 * F_J * R; steep = list(sk)
    denom = sk[-1] - sk[c + 1]
    for i in range(c + 1, len(ms)):
        steep[i] = sk[c] + J + (R - J) * (sk[i] - sk[c + 1]) / denom
    return steep


def known_answer_case(class_name: str, replicate: int, census: CL.CalibrationCensus, pub: CL.ClosurePublication, master: int = KNOWN_ANSWER_MASTER) -> Tuple[P1Evaluation, str, str]:
    """Generate one synthetic case of the named class and evaluate it. Returns (evaluation, intended determination,
    intended cause-prefix). Noise amplitude = 0.45 × the smallest applicable band (below half the band everywhere)."""
    verify_frozen_identity()
    if class_name not in KA_CLASSES: raise EvaluatorDomainError(f"unknown known-answer class {class_name!r}")
    g = np.random.default_rng(np.random.SeedSequence([int(master), KA_CLASSES.index(class_name), int(replicate)]))
    dm = pub.delta_m.value
    min_band = min(band(census, o, i, i + 1) for o in ("skeleton_high", "realization") for i in range(len(F8_LEVELS_MICRO) - 1))
    amp = 0.45 * min_band
    ms = [_level_value(u) for u in F8_LEVELS_MICRO]
    def survs_for(mc): return [PANEL_N if m > mc else 0 for m in ms]
    def build(mc_high, mc_low, sk_meds, re_meds, re_feature=None, sk_feature=None):
        hi = _synthetic_sweep("skeleton_high", sk_meds, survs_for(mc_high), amp, g, sk_feature)
        lo = _synthetic_sweep("skeleton_low", sk_meds, survs_for(mc_low), amp, g, sk_feature)
        re_ = _synthetic_sweep("realization", re_meds, [PANEL_N] * len(ms), amp, g, re_feature)
        return hi, lo, re_
    if class_name.startswith("pass_crossing_"):
        mc = float(class_name.split("_")[-1])
        hi, lo, re_ = build(mc, mc, _branch(mc, "skeleton"), _branch(mc, "realization"))
        return evaluate_p1(hi, lo, re_, census, pub), "PRODUCED", ""
    if class_name == "fail_no_inactive_phase":                    # crossing below the sweep: every level survives
        mc = 0.1
        hi, lo, re_ = build(mc, mc, _branch(mc, "skeleton"), _branch(mc, "realization"))
        return evaluate_p1(hi, lo, re_, census, pub), "NOT PRODUCED", "no inactive phase in sweep"
    if class_name == "fail_no_active_phase":                      # crossing above the sweep: nothing survives in the skeleton; the realization
        mc = 3.0                                                  # is the ordinary branch at m_c = 1 so that no test other than T-S1' can trigger
        hi, lo, re_ = build(mc, mc, [0.0] * len(ms), _branch(1.0, "realization"))   # (L2 r1 §6.3: the m_c = 3 realization carried a continuity ND at 2.5)
        return evaluate_p1(hi, lo, re_, census, pub), "NOT PRODUCED", "no active phase in sweep"
    if class_name == "nd_steep_continuous":                       # continuous, compressed inside one spacing: the FIRST adjacent rise above the boundary
        hi, lo, re_ = build(1.0, 1.0, steep_continuous_branch(1.0), _branch(1.0, "realization"))   # is exactly 2·f_J × range (MP1-3; L2 r1 D5)
        return evaluate_p1(hi, lo, re_, census, pub), "NOT DISTINGUISHED", "continuity unresolved at grid resolution"
    if class_name == "fail_hysteresis":                           # low/high crossings differ by 2·Δm
        mc = 1.0
        hi, lo, re_ = build(mc, mc + 2 * dm, _branch(mc, "skeleton"), _branch(mc, "realization"))
        return evaluate_p1(hi, lo, re_, census, pub), "NOT PRODUCED", "hysteresis"
    if class_name == "fail_realization_extinct":                  # realization extinct at one level
        mc = 1.0; re_meds = _branch(mc, "realization"); k = 3
        hi, lo, re_ = build(mc, mc, _branch(mc, "skeleton"), re_meds, re_feature={k: (0.0, 0.0)})
        return evaluate_p1(hi, lo, re_, census, pub), "NOT PRODUCED", "realization extinct"
    if class_name == "nd_injected_reversal":                      # one reversal of 2× the combined band at one adjacent pair of the realization
        mc = 1.0; re_meds = _branch(mc, "realization"); k = 15
        b = band(census, "realization", k - 1, k)
        hi, lo, re_ = build(mc, mc, _branch(mc, "skeleton"), re_meds, re_feature={k: (re_meds[k - 1] - 2 * b, amp)})
        return evaluate_p1(hi, lo, re_, census, pub), "NOT DISTINGUISHED", "non-monotone at finite sample"
    raise EvaluatorDomainError("unreachable")


@dataclass(frozen=True)
class KnownAnswerQualification:
    master: int
    sweeps_per_class: int
    pass_min: int
    per_class: Tuple[Tuple[str, str, str, int, int, int], ...]   # (class, intended determination, intended cause prefix, exact matches, cross-trigger failures, total)
    passed: bool
    census_sha256: str
    census_is_declared_synthetic: bool    # D6: the census REPLAYS to synthetic_census() (ŝ = 0.01 both objects, derived_provisional); passage requires it
    declaration_sha256: str
    result_sha256: str = ""

    def identity(self) -> str:
        d = asdict(self); d.pop("result_sha256", None); return hashlib.sha256(_canon(d).encode()).hexdigest()


def known_answer_qualification(sweeps_per_class: int = KNOWN_ANSWER_SWEEPS, pass_min: int = KNOWN_ANSWER_PASS_MIN, master: int = KNOWN_ANSWER_MASTER,
                               census: Optional[CL.CalibrationCensus] = None, classes: Sequence[str] = KA_CLASSES) -> KnownAnswerQualification:
    """Every class, `sweeps_per_class` replicates; a case counts iff it returns EXACTLY the intended determination AND a cause
    beginning with the named cause (cross-trigger rule: right determination, wrong cause → fails). Passage iff every class
    has ≥ pass_min exact matches AND the run is the declared one: every class, the declared replicate count, minimum and
    master, and the DECLARED SYNTHETIC CENSUS (replay identity of `synthetic_census()`; L2 M-P1 r1 D6 — a different census,
    however valid, is a different experiment and yields a non-qualifying development record; a canonical-role census is
    refused from this path outright, since the corpus is independent of job 0)."""
    verify_frozen_identity()
    census = synthetic_census() if census is None else census
    CL.validate_calibration_census(census)
    if census.role != "derived_provisional": raise EvaluatorDomainError("the known-answer corpus runs only under a synthetic (derived_provisional) census, never the canonical one")
    declared = census.result_sha256 == synthetic_census().result_sha256
    pub = CL.closure_publication()
    rows = []
    for cls in classes:
        exact = cross = 0
        for r in range(sweeps_per_class):
            ev, want_det, want_cause = known_answer_case(cls, r, census, pub, master)
            det_ok = ev.determination == want_det
            cause_ok = (want_cause == "" and ev.cause is None) or (want_cause != "" and ev.cause is not None and ev.cause.startswith(want_cause))
            if det_ok and cause_ok: exact += 1
            elif det_ok and not cause_ok: cross += 1
        rows.append((cls, want_det, want_cause, exact, cross, sweeps_per_class))
    passed = all(ex >= pass_min for *_, ex, _, _ in rows) and tuple(classes) == KA_CLASSES and sweeps_per_class == KNOWN_ANSWER_SWEEPS \
        and pass_min == KNOWN_ANSWER_PASS_MIN and master == KNOWN_ANSWER_MASTER and declared
    q = KnownAnswerQualification(int(master), int(sweeps_per_class), int(pass_min), tuple(rows), bool(passed), census.result_sha256, bool(declared), EVALUATOR_SHA256_LITERAL)
    import dataclasses as _dc
    return _dc.replace(q, result_sha256=q.identity())
