"""mfa_instrument/f9/evaluator_reports.py — Flight 9 module M6, part 2: the reports that apply the
composition evaluator or join records already defined (Contract F9 v0.7 §1.3 (a), (d) design side,
(f), (g), (h); §5.7 rows 5 and 6).

REPORTED ONLY. Nothing here is scored or tested, nothing enters B or D, and no value gates anything
(§1.3, §5.7). A missing record prevents a claim of complete reporting; it is not a failure of B or D.

THE SCORED EVALUATION IS NOT HERE. A level's scored record is `evaluator.evaluate_level` (module M3)
and nothing in this module produces, replaces or alters it. This module reads no run record and holds
no master: that the arrays it is given are the runs' and the identity bundle's is the runner's to
establish.

(f) THE EVALUATOR'S FULL OUTPUT AT θ = 0.10 AND θ = 0.30 (§1.3 (f)). "These never replace or rescue the
scored result."
  How θ is reached (Mike, 2026-11-23, option A). The placed evaluator holds θ = 0.20 in one function,
  `evaluator.occupied_region`; nothing after it takes θ. This module does not edit the placed evaluator
  and does not change the registered constant. It has its own `occupied_region_at(counts, weights, θ)`,
  the same integer criterion with θ as an argument, and its own copies of the two orchestration
  functions (`evaluate_map_at`, `evaluate_level_at`) that call the placed building blocks unchanged:
  `box_sum`, `geometry.edge`, `step4`, `_Traced`, `fit`, `resample_multiplicities`,
  `result_from_counts`. At θ = 0.20 the copy must return the placed evaluator's record, field for field
  (tested); it accepts 0.20 for that test only and is never the scored path. Before anything else the
  copy verifies this module's declaration (and with it the evaluator's, the outcome module's and the
  stream's) and validates θ. A damaged declaration among those, or a θ outside the three accepted, is
  refused here; that is a difference from the placed evaluator in what is refused and not in any
  returned record (L2 M6B round 1, Q1).
  Cause precedence (L2 M6B round 1, D1). The copy carries the placed evaluator's order as repaired at
  `7a1094a`: an index whose family is empty is `no eligible contour` whatever the observed map is (§7:
  L2 above L3 and L4; §6.2 row 15: "the cause does not depend on the sample"), and only then does a
  non-informative map give its own cause. Round 1 of this module copied the earlier, wrong order from
  the evaluator as then placed, and its equality tests could not see an error both sides shared. The
  point record describes the map in every case.
  The resamples (reading 1). The outputs at 0.10 and 0.30 use the declared evaluator stream of the same
  arm and level as the scored evaluation, so the three thresholds are evaluated on the same 1,000
  resampled maps.
  The step-4 minimums (100 cells each side, 40 bonds) and ε, m, the family and the result table are the
  registered ones at every θ.

(g) THE SKELETON'S BOUNDARY (§1.3 (g); §5.7 row 5). The §5.5 rule on the unconditional seed-mean map of
all 40 skeleton runs of a level: an extinct run contributes its recorded tail, zeros after extinction.
  Reading 2 (Mike, 2026-11-23): "the §5.5 rule" is the whole of it, steps 1 to 9, at θ = 0.20, so the
  record is the placed `evaluator.evaluate_level` applied to the skeleton maps. Its compatible, adverse
  or unresolved word is a description of the skeleton map and is not B.
  Reading 3: its resamples come from a stream of its own, the arm-and-level key with the skeleton's
  object code appended, (master, terrain code, composition code, κ in micro-units, 1). The contract
  names no stream for it.
  On T0 the family is empty and every index's cause is `no eligible contour`, whatever the map (§7). On
  the other arms a map with no edge gives the evaluator's `no edge at theta`.

(h) COMPONENT COVERAGE (§1.3 (h); §5.7 row 6). "For every scored level, the number of components on each
side, how many are resolved, and each one's 95th-percentile distance." Computed from the level's maps
by the placed steps 1 to 7 on the observed map (all weights one); no evaluation record is accepted on
its word. Per index: the observed edge's components and the fitted contour's components, each with its
bonds, whether it is resolved (at least m = 40 bonds), and the 0.95 quantile of its bonds' distances to
the whole opposite edge.
  Reading 4: "each one's" is every component's, resolved or not. A resolved component's value is the
  term the evaluator used (tested equal); an unresolved component's value is the same quantile, computed
  here, and it entered no decision.
  Reading 5: the contour is the one the fit reports: the minimizing contour when Δ ≤ ε; otherwise the
  contour with the least S among those examined, labelled as §5.5 step 7 labels it (descriptive; need
  not be the family minimum). If no contour was examined, or the family is empty, or the level is not
  informative, the observed side's counts are reported where they exist and the rest carries its cause.

(d) DESIGN-SIDE MARGIN SUMMARIES (§1.3 (d); §3.2), for the four TD variants, from the variant's stored
base v and the declared core (`terrain.td_core`): the core's cells, lattice perimeter and components;
the band = cells whose base lies strictly between 10% and 90% of the base step, S = (v − 0.3)/0.6 in
(0.1, 0.9), with its split inside and outside the core; band/core; and the largest base step between
4-neighbours. They are index geometry and use no run. The definitions are those of the contract's
arithmetic (`contracts/flight9/arith/td_final.py`), and the result must reproduce §3.2's table (band
cells, band/core and largest step to three places, perimeter): those are constants of the declaration
and are asserted on every call. As with TC's set sizes, the assertions are a sanity check and do not
authenticate the array; v must be the variant's base from the authenticated identity bundle, and
binding it is the runner's. No criterion refers to the margins hypothesis (§3.2).

(a) THE SKELETON PERSISTENCE DIAGNOSTIC, ASSEMBLED (§1.3 (a); §5.4). For every arm, the §5.4 record of
its skeleton sweep (`outcomes.persistence_record`, module M4), computed here from survivor counts; no
persistence record is accepted on its word. An arm that is absent is listed as missing and the report
says it is not complete. It makes no claim about coupling.

RECORDS. The evaluation records are the placed evaluator's and carry its numpy arrays (the typed draws,
their Δ and level indices); the other records are str, int, float, bool, None, list and dict. Per-θ
records are keyed by θ in integer micro-units. The persisted encoding is the runner's to declare. These
dicts are components of the eventual §5.9 records, not bound job records.

NOT HERE. The fidelity items of §1.2′ (ii) and (iii) and their uncertainties (§5.7 row 4): local m on the
observed edge, and occupancy and edges against the closure's map. The contract names them; F9
Interpretation 002 (accepted 2026-11-24) fixes their summaries; they are built as a third reports
module. That interpretation takes the skeleton's resample stream from this module's reading 3.

READINGS THIS MODULE MAKES, each for Mike's ratification with the governance record (nothing in the
contract is changed). The wrapper of (f) and readings 1 and 2 were L1's recommendations, which Mike
accepted on 2026-11-23 before this module was written; readings 3 to 7 are L1's.
  1. θ = 0.10 and 0.30 use the scored evaluation's resample stream (above, (f)).
  2. The skeleton's boundary is steps 1 to 9 (above, (g)).
  3. The skeleton's resample stream is the arm-and-level key with the skeleton's object code appended.
  4. Component coverage gives every component its quantile, resolved or not.
  5. Component coverage uses the contour the fit reports.
  6. The design-side band is strict at both ends, as the contract's arithmetic computed it.
  7. The persistence report covers the fifteen arms of §8 (T0 under P only) and the high-initialization
     skeleton sweep; T0's low sweep belongs to T0's own record (§5.8).
"""
from __future__ import annotations

from fractions import Fraction
from typing import Dict, Optional, Tuple

import numpy as np

from . import config as C
from . import evaluator as E
from . import geometry as G
from . import outcomes as O
from . import streams as R
from . import terrain as T
from .config import F9ConfigError

KIND = "reported only; never scored"
THETAS_REPORTED_MICRO = C.F9_THETA_REPORTED_MICRO          # (100_000, 300_000): §5.5 step 2, §1.3 (f)
THETAS_ACCEPTED_MICRO = (100_000, 200_000, 300_000)        # 0.20 is accepted for the equality test against the placed evaluator only
BOX_DENOMINATOR = 9 * C.F9_N_SEEDS * C.F9_TAIL_TICKS
SKELETON_OBJECT_CODE = dict(R.OBJECT_CODES)["skeleton"]    # 1: appended to the arm-and-level key (reading 3)
TD_BASE_LOW, TD_BASE_STEP = 0.3, 0.6                       # §3.1: t = 0.3 + 0.6·S
TD_BAND = (0.1, 0.9)                                       # §3.2: 10–90% of the base step, strict
TD_DESIGN_TABLE = (                                        # §3.2's table: (variant, lattice perimeter, band cells, band/core, largest base step)
    ("TD-1-2", 200, 676, "0.338", "0.145"), ("TD-1-4", 200, 1376, "0.688", "0.074"),
    ("TD-4-2", 416, 1424, "0.712", "0.142"), ("TD-4-4", 416, 2816, "1.408", "0.074"),
)

EVALUATOR_REPORTS_DECLARATION = (
    ("module", "f9.evaluator_reports"), ("version", C.F9_VERSION), ("contract", C.F9_CONTRACT_SHA256),
    ("evaluator_declaration", E.EVALUATOR_DECLARATION_SHA256_LITERAL),
    ("thetas_reported_micro", THETAS_REPORTED_MICRO), ("thetas_accepted_micro", THETAS_ACCEPTED_MICRO),
    ("criterion_at_theta", "box_sum * 10^6 >= theta_micro * 9 * n_seeds * tail"),
    ("orchestration", "the placed evaluator's evaluate_map and evaluate_level with theta as an argument; building blocks called unchanged"),
    ("unavailable_precedence", "an empty family first (no eligible contour), then a non-informative map's cause: contract section 7, L2 above L3 and L4"),
    ("reported_theta_stream", "the scored evaluation's: evaluator.arm_level_key"),
    ("skeleton_rule", "evaluator.evaluate_level (steps 1 to 9) at the registered theta on the 40 skeleton maps"),
    ("skeleton_stream", "arm-and-level key + (skeleton object code,)"), ("skeleton_object_code", SKELETON_OBJECT_CODE),
    ("coverage", "observed map, steps 1 to 7; every component of each side: bonds, resolved, q95 of its distances to the whole opposite edge; the contour the fit reports"),
    ("td_band", "S = (v - 0.3) / 0.6; band = 0.1 < S < 0.9"), ("td_step", "largest absolute base difference between 4-neighbours"),
    ("td_design_table", TD_DESIGN_TABLE),
    ("persistence", "outcomes.persistence_record per arm of the fifteen, from survivor counts"),
    ("kind", KIND),
)
EVALUATOR_REPORTS_DECLARATION_SHA256_LITERAL = "a9227f81c1b088dfdcd86d625747b3b2c26323cf25c3092cbc4d4e6fe071e979"


class F9EvaluatorReportError(F9ConfigError):
    """An input outside a report's domain, or a declaration that differs from its frozen digest."""


def verify_evaluator_reports_declaration() -> str:
    C.verify_frozen_identity()
    if E.verify_evaluator_declaration() != E.EVALUATOR_DECLARATION_SHA256_LITERAL: raise F9EvaluatorReportError("the evaluator's declaration is not the placed one")
    O.verify_outcome_declaration(); R.verify_stream_declaration()
    digest = C.frozen_digest(EVALUATOR_REPORTS_DECLARATION)
    if digest != EVALUATOR_REPORTS_DECLARATION_SHA256_LITERAL: raise F9EvaluatorReportError("the evaluator-reports declaration differs from its frozen digest")
    if THETAS_REPORTED_MICRO != (100_000, 300_000) or C.F9_THETA_MICRO != 200_000 or C.F9_THETA_MICRO in THETAS_REPORTED_MICRO:
        raise F9EvaluatorReportError("the reported thresholds are not 0.10 and 0.30 beside a scored 0.20")
    if tuple(n for n, *_ in TD_DESIGN_TABLE) != tuple(n for n, _ in C.F9_TD_PARAMS) or SKELETON_OBJECT_CODE != 1:
        raise F9EvaluatorReportError("the design table or the skeleton code is not the declared one")
    return digest


def _theta(theta_micro) -> int:
    if type(theta_micro) is not int or theta_micro not in THETAS_ACCEPTED_MICRO:
        raise F9EvaluatorReportError(f"θ is 100000 or 300000 micro-units (200000 for the equality test only): {theta_micro!r}")
    return theta_micro


# ======================= (f) the evaluator at another θ =======================
def occupied_region_at(counts: np.ndarray, weights: np.ndarray, theta_micro: int) -> Tuple[np.ndarray, np.ndarray]:
    """`evaluator.occupied_region` with θ as an argument: the region {p̃ ≥ θ}, ties included, and the box sum."""
    total = np.tensordot(weights, counts, axes=(0, 0))
    B = E.box_sum(total)
    return B * C.MICRO_UNITS >= _theta(theta_micro) * BOX_DENOMINATOR, B


def evaluate_map_at(counts: np.ndarray, weights: np.ndarray, families: Dict[str, E.IndexFamily], theta_micro: int, brute: bool = False) -> Dict[str, object]:
    """`evaluator.evaluate_map` with θ as an argument (steps 1 to 7 on one map, for every index in `families`)."""
    mask, B = occupied_region_at(counts, weights, theta_micro)
    e = G.edge(mask)
    reason = E.step4(mask, e)
    out = {"region_cells": int(mask.sum()), "bonds": e.n_bonds, "component_sizes": list(e.component_sizes()),
           "informative": reason is None, "reason": reason, "indices": {}}
    if reason is not None: return out
    Et = E._Traced(e)
    done: Dict[int, Dict[str, object]] = {}
    for name, fam in families.items():
        if fam.contours_id not in done: done[fam.contours_id] = E.fit(Et, fam, brute)
        entry = dict(done[fam.contours_id])
        if entry.get("within"): entry["lambda_star"] = fam.label(entry["level_index"])
        out["indices"][name] = entry
    return out


def evaluate_level_at(counts, families: Dict[str, E.IndexFamily], key, theta_micro: int, brute: bool = False) -> Dict[str, object]:
    """`evaluator.evaluate_level` with θ as an argument, on the declared stream for `key` (no constructed resamples)."""
    verify_evaluator_reports_declaration()
    theta_micro = _theta(theta_micro)
    counts = E.check_counts(counts); families = E._check_families(families); key = E.stream_key(key)
    ones = np.ones(C.F9_N_SEEDS, dtype=np.int64)
    point = evaluate_map_at(counts, ones, families, theta_micro, brute)
    record: Dict[str, object] = {"stream_key": list(key), "stream_role": E.EVALUATOR_STREAM_ROLE, "n_resamples": E.N_RESAMPLES,
                                 "declared_stream": True, "point": point, "indices": {}, "resampled": False}
    applicable = {}
    for name, fam in families.items():
        if len(fam) == 0:                                                   # §7: L2 (constant index) before L3 and L4 (the map's state)
            record["indices"][name] = {"result": E.RESULT_NOT_INFORMATIVE, "cause": E.CAUSE_NO_CONTOUR, "resampled": False}
        elif not point["informative"]:
            cause = E.CAUSE_NO_EDGE if point["reason"].startswith("no edge") else E.CAUSE_BELOW_MINIMUM
            record["indices"][name] = {"result": E.RESULT_NOT_INFORMATIVE, "cause": cause, "resampled": False}
        else:
            applicable[name] = fam
    if not applicable: return record
    mult = E.resample_multiplicities(key)
    n = E.N_RESAMPLES
    types = {name: np.empty(n, dtype="U1") for name in applicable}
    delta = {name: np.full(n, np.nan) for name in applicable}
    level_index = {name: np.full(n, -1, dtype=np.int64) for name in applicable}
    reasons: Dict[str, int] = {}
    for r in range(n):
        draw = evaluate_map_at(counts, mult[r], applicable, theta_micro, brute)
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
        result, cause = E.result_from_counts(n_C, n_A, n_I)
        entry = {"result": result, "cause": cause, "resampled": True, "n_C": n_C, "n_A": n_A, "n_I": n_I,
                 "types": types[name], "delta": delta[name], "level_index": level_index[name]}
        if n_C:
            labels = [fam.label(int(k)) for k in level_index[name][types[name] == "C"]]
            entry["lambda_star_range"] = [min(labels), max(labels)]
        else:
            entry["lambda_star_range"] = None
        record["indices"][name] = entry
    return record


def reported_thresholds(counts, families: Dict[str, E.IndexFamily], key) -> Dict[str, object]:
    """§1.3 (f) for one realization level: the evaluator's full output at θ = 0.10 and θ = 0.30, on the scored
    evaluation's resample stream (`key` is that evaluation's key, `evaluator.arm_level_key`)."""
    verify_evaluator_reports_declaration()
    return {"record": "F9ReportedThresholds", "kind": KIND, "theta_micro": {t: evaluate_level_at(counts, families, key, t) for t in THETAS_REPORTED_MICRO},
            "scored_theta_micro": C.F9_THETA_MICRO,
            "note": "these never replace or rescue the scored result; same resample stream as the scored evaluation; step-4 minimums, ε, m and the family unchanged",
            "declaration_sha256": EVALUATOR_REPORTS_DECLARATION_SHA256_LITERAL}


# ======================= (g) the skeleton's boundary =======================
def skeleton_level_key(master: int, terrain: str, composition: str, level_micro: int) -> Tuple[int, ...]:
    """The evaluator stream key of an arm's skeleton level: (master, terrain code, composition code, κ in micro-units,
    skeleton object code). Distinct from every realization key, which has four elements."""
    R.check_run_identity(master, terrain, composition, "skeleton", "all_active", level_micro, 0)
    return (master, dict(R.TERRAIN_CODES)[terrain], dict(R.COMPOSITION_CODES)[composition], level_micro, SKELETON_OBJECT_CODE)


def skeleton_boundary(counts, families: Dict[str, E.IndexFamily], key) -> Dict[str, object]:
    """§1.3 (g) for one skeleton level: the §5.5 rule (steps 1 to 9, θ = 0.20) on the seed maps of all 40 skeleton runs,
    an extinct run's map being its recorded tail. `key` is `skeleton_level_key(...)`."""
    verify_evaluator_reports_declaration()
    key = E.stream_key(key)
    if len(key) != 5 or key[-1] != SKELETON_OBJECT_CODE: raise F9EvaluatorReportError("the key is not a skeleton level's (skeleton_level_key)")
    return {"record": "F9SkeletonBoundary", "kind": KIND, "theta_micro": C.F9_THETA_MICRO, "evaluation": E.evaluate_level(counts, families, key),
            "note": "the §5.5 rule on the unconditional seed-mean map of all 40 skeleton runs; a description of the skeleton map; not B",
            "declaration_sha256": EVALUATOR_REPORTS_DECLARATION_SHA256_LITERAL}


# ======================= (h) component coverage =======================
def _side_components(mine: E._Traced, other: E._Traced) -> list:
    """Every component of `mine`: bonds, resolved, and the 0.95 quantile of its bonds' distances to the whole of `other`."""
    d = E._cells(other.grid[mine.a, mine.b])
    out = []
    for k, n in enumerate(mine.sizes):
        out.append({"bonds": int(n), "resolved": bool(n >= C.F9_COMPONENT_MIN_BONDS), "q95_distance": E.q95(np.sort(d[mine.edge.component == k]))})
    return out


def component_coverage(counts, families: Dict[str, E.IndexFamily]) -> Dict[str, object]:
    """§1.3 (h) for one scored level: per index, the components of the observed edge and of the contour the fit
    reports, from the level's maps (steps 1 to 7 on the observed map at the registered θ)."""
    verify_evaluator_reports_declaration()
    counts = E.check_counts(counts); families = E._check_families(families)
    mask, _B = E.occupied_region(counts, np.ones(C.F9_N_SEEDS, dtype=np.int64))
    e = G.edge(mask)
    reason = E.step4(mask, e)
    sizes = [int(n) for n in e.component_sizes()]
    out: Dict[str, object] = {"record": "F9ComponentCoverage", "kind": KIND, "theta_micro": C.F9_THETA_MICRO, "component_min_bonds": C.F9_COMPONENT_MIN_BONDS,
                              "informative": reason is None, "reason": reason,
                              "observed": {"bonds": e.n_bonds, "components": len(sizes), "resolved": sum(1 for n in sizes if n >= C.F9_COMPONENT_MIN_BONDS), "component_bonds": sizes},
                              "indices": {}, "declaration_sha256": EVALUATOR_REPORTS_DECLARATION_SHA256_LITERAL}
    if reason is not None: return out
    Et = E._Traced(e)
    done: Dict[int, Dict[str, object]] = {}
    for name, fam in families.items():
        if fam.contours_id not in done:
            f = E.fit(Et, fam)
            entry: Dict[str, object] = {"status": f["status"], "family_size": f["family_size"]}
            if "level_index" in f:
                Cn = fam.contour(f["level_index"])
                obs, con = _side_components(Et, Cn), _side_components(Cn, Et)
                entry.update(level_index=f["level_index"], level=f["level"], within=f["within"], S=f["terms"]["S"],
                             contour_is="the minimizing contour" if f["within"] else "least S among the contours examined; descriptive; need not be the family minimum",
                             observed_components=obs, contour_components=con,
                             contour={"bonds": Cn.edge.n_bonds, "components": len(con), "resolved": sum(1 for c in con if c["resolved"])},
                             no_resolved_component_checked_on_observed=not any(c["resolved"] for c in obs),
                             no_resolved_component_checked_on_contour=not any(c["resolved"] for c in con))
            else:
                entry.update(cause=E.CAUSE_NO_CONTOUR if f["family_size"] == 0 else "no contour examined", observed_components=None, contour_components=None)
            done[fam.contours_id] = entry
        out["indices"][name] = dict(done[fam.contours_id])
    return out


# ======================= (d) design-side margins =======================
def design_margins(name: str, v) -> Dict[str, object]:
    """§1.3 (d), design side, for one TD variant from its stored base v (see the module docstring for what the
    assertions do and do not establish)."""
    verify_evaluator_reports_declaration()
    table = {n: row for n, *row in TD_DESIGN_TABLE}
    if name not in table: raise F9EvaluatorReportError(f"design-side margins are declared for the TD variants: {name!r}")
    a = np.asarray(v)
    if a.dtype != np.float64 or a.shape != (C.F9_GRID, C.F9_GRID) or not np.all(np.isfinite(a)): raise F9EvaluatorReportError("v is a finite float64 (L, L) array")
    core = T.td_core(name)
    if not np.array_equal(core, a > TD_BASE_LOW + TD_BASE_STEP / 2): raise F9EvaluatorReportError(f"{name}: the base's upper half is not the declared core")
    e = G.edge(core)
    S = (a - TD_BASE_LOW) / TD_BASE_STEP
    band = (S > TD_BAND[0]) & (S < TD_BAND[1])
    n_core, n_band = int(core.sum()), int(band.sum())
    step = float(max(np.abs(a - np.roll(a, 1, axis=0)).max(), np.abs(a - np.roll(a, 1, axis=1)).max()))
    ratio = Fraction(n_band, n_core)
    perimeter, band_cells, ratio_lit, step_lit = table[name]
    if (e.n_bonds, n_band, f"{float(ratio):.3f}", f"{step:.3f}") != (perimeter, band_cells, ratio_lit, step_lit):
        raise F9EvaluatorReportError(f"{name}: the base does not reproduce the design table of contract §3.2")
    return {"record": "F9DesignMargins", "kind": KIND, "terrain": name,
            "core": {"cells": n_core, "perimeter_bonds": e.n_bonds, "components": e.n_components, "component_bonds": [int(k) for k in e.component_sizes()]},
            "band": {"cells": n_band, "inside_core": int((band & core).sum()), "outside_core": int((band & ~core).sum())},
            "band_over_core": {"value": float(ratio), "exact": f"{ratio.numerator}/{ratio.denominator}"},
            "largest_base_step": step, "contract_table": {"perimeter": perimeter, "band_cells": band_cells, "band_over_core": ratio_lit, "largest_base_step": step_lit},
            "note": "index geometry; no run; no criterion, threshold or rule refers to the margins hypothesis (§3.2)",
            "declaration_sha256": EVALUATOR_REPORTS_DECLARATION_SHA256_LITERAL}


# ======================= (a) the persistence diagnostic, assembled =======================
def arm_name(terrain: str, composition: str) -> str:
    if (terrain, composition) not in C.F9_ARMS: raise F9EvaluatorReportError(f"not a declared arm: {terrain!r}.{composition!r}")
    return f"{terrain}.{composition}"


def persistence_report(survivors_by_arm: Dict[str, Optional[Dict[int, Optional[int]]]]) -> Dict[str, object]:
    """§1.3 (a) for the panel: `survivors_by_arm["TA.P"][κ micro]` = the number of the arm's 40 high-initialization
    skeleton runs at that level that survived. An arm that is absent or None is listed as missing."""
    verify_evaluator_reports_declaration()
    names = [arm_name(t, c) for t, c in C.F9_ARMS]
    if not isinstance(survivors_by_arm, dict) or any(type(k) is not str or k not in names for k in survivors_by_arm):
        raise F9EvaluatorReportError("survivors are keyed by the declared arms, 'terrain.composition'")
    arms: Dict[str, object] = {}
    missing = []
    for n in names:
        s = survivors_by_arm.get(n)
        if s is None: arms[n] = None; missing.append(n)
        else: arms[n] = O.persistence_record(s)
    incomplete = [n for n in names if arms[n] is not None and arms[n]["profile"] is None]
    return {"record": "F9PersistenceReport", "kind": KIND, "arms": arms, "missing_arms": missing, "arms_with_missing_levels": incomplete,
            "complete": not missing and not incomplete,
            "note": "skeleton, all cells active at t = 0; a panel and grid description; pointwise intervals; no claim about coupling (§1.3 (a))",
            "declaration_sha256": EVALUATOR_REPORTS_DECLARATION_SHA256_LITERAL}
