"""mfa_instrument/f9/outcomes.py — Flight 9 module M4: the outcome records of Contract F9 v0.7 §5.6
with the precedence of §7 (level, arm, flight B, flight D), and the skeleton persistence record of
§5.4 and §1.3(a).

This module is pure rule: it turns typed inputs into typed records. It runs nothing, draws nothing,
holds no master and reads no file. Every label it emits is the contract's own string.

LEVEL (§5.6 level tier; §7 L1 to L7, highest precedence first). An arm's level takes the evaluator's
result for the arm's own index and for the rival index (module M3).
  L1  apparatus (run halted; record missing, corrupt or out of range; evaluator fault):
      `apparatus unevaluable (<key>)` — the level is unevaluable.
  L2  constant index: `no eligible contour` — the index is not scored at any level.
  L3  R at θ empty or full: `no edge at θ` — scientific ND, the level is not informative.
  L4  R or its complement under 100 cells, or under 40 bonds: `under-resolved` — not informative.
  L5  more than 50 invalid draws: `unstable edge` — not informative.
  Otherwise the level is INFORMATIVE and the table of §5.6 gives two statuses, recorded separately:
      own         rival        B status            discrimination status
      compatible  adverse      follows own         rival excluded
      compatible  compatible   follows own         not distinguished
      compatible  unresolved   follows own         rival not established
      adverse     compatible   own adverse         follows rival
      adverse     adverse      own adverse         follows neither
      adverse     unresolved   own adverse         rival not established
      unresolved  any          not distinguished   not distinguished
  L6  neither count reaches 950 (own or rival unresolved): cause `finite resolution`.
  L7  own adverse: cause `no registered contour of own index within ε`.
  On a same-family terrain the two indices share one family. Their results are equal by construction
  (unequal results there are an apparatus fault and raise), and the discrimination status is always
  `not adjudicable here`.

THE EVALUATOR'S CAUSE STRINGS. M3 names three unavailable causes in its own words (`no edge at theta`,
`below the informative minimum`, `no eligible contour`) and `unstable edge`. The contract's §7 labels
for the first two are `no edge at θ` and `under-resolved`. `level_from_evaluation` translates them;
the records of this module carry the contract's labels only. (M3's strings are placed bytes; they are
noted for its next touch.)

ARM (§5.6 arm tier; §7 A1 to A4), over the 25 registered levels of §2.9, in this order:
  A1  any level unevaluable for an apparatus reason (a missing level record included):
      `no qualified determination`.
  A2  "own adverse" at two levels that are neighbours on the registered grid, both informative, with no
      level between them: ADVERSE. This applies even if only two levels are informative.
  A3  at least 3 informative levels and "follows own" at every informative level: COMPATIBLE. The record
      states the informative levels it rests on.
  A4  otherwise NOT DISTINGUISHED, with cause.
  An arm record carries the 25 level records it was computed from (a missing one as its apparatus record).
  Every other field is derived from them, and a record is accepted downstream only if recomputing the arm
  from the levels it carries gives back the whole record, field for field and type for type.
  THE CAUSE OF A4. The contract names three causes and does not say which is recorded when more than one
  holds. This module records EVERY cause that holds, in the contract's listing order, and chooses
  none over another:
      `insufficient informative levels`  — fewer than 3 informative levels;
      `isolated adverse level`           — at least one informative level is "own adverse";
      `finite resolution`                — at least one informative level is "not distinguished" (own
                                           unresolved).
  At least one always holds when A1 to A3 do not apply.

FLIGHT B, per composition X (§5.6): a conjunction over the seven required arms; no vote across terrains.
  qualification not passed, or any required arm without a qualified determination (a missing arm record
      included)                                        → `no qualified scientific determination`
  at least one required arm ADVERSE                    → NOT PRODUCED
  no required arm ADVERSE, at least one NOT DISTINGUISHED → NOT DISTINGUISHED
  all seven required arms COMPATIBLE                   → PRODUCED, with domain and resolution stated
FLIGHT D, on TB (§5.6), from the two TB arms' level records (each arm's determination is computed here):
  qualification not passed, or either TB arm without a qualified determination
                                                       → `no qualified scientific determination`
  DISTINGUISHED iff in each TB arm at least 3 informative levels carry "follows own" with "rival
      excluded", and no informative level in either arm carries "follows rival". The witnessing levels
      need not be the same in the two arms; both witness sets are reported.
  otherwise NOT DISTINGUISHED, with what was missing (the contract names no D causes; the record states
      each arm's witness count and every "follows rival" level).

PERSISTENCE (§5.4, §1.3(a)). For a skeleton arm: the surviving seeds s of 40 at each of the 25 levels,
each with a two-sided 95% Clopper–Pearson interval (pointwise; not a simultaneous band and not an
interval for κ̂_c). A level meets the criterion when s ≥ 36. The profile, by the first row that applies:
  some level meets the criterion and a higher level fails it → "non-monotone criterion profile"; if a
      terminal stretch meets the criterion its lowest level is a descriptive suffix statistic, otherwise
      unavailable; κ̂_c unavailable; never a monotone-crossing claim
  every tested level meets it → "criterion met at all tested levels"; κ̂_c = the lowest tested level;
      unbracketed on the lower side
  no tested level meets it   → "criterion met at no tested level"; κ̂_c unavailable
  a failing lower stretch, then a terminal stretch meeting it → "both criterion phases observed"; κ̂_c =
      the first level of the terminal stretch; bracket = the failing level just below it and κ̂_c
Interval records are supplied for the endpoints that exist; an absent endpoint has its cause. Every bound
is a panel and grid description, never a population confidence bound. The record makes no claim about
coupling. An extinct run is a valid observation: s counts it as not surviving.
The Clopper–Pearson bounds are computed here from the binomial tail by bisection (no external
library): lower = the p at which P(X ≥ s) = 0.025 (0 when s = 0); upper = the p at which
P(X ≤ s) = 0.025 (1 when s = n).
"""
from __future__ import annotations

import functools
import math
from typing import Dict, List, Optional, Sequence, Tuple

from . import config as C
from .config import F9ConfigError

# ----------------------------------------------------------------------------- the contract's labels
COMPATIBLE, ADVERSE, UNRESOLVED = "compatible", "adverse", "unresolved"                     # an index's result at a level (§5.5 step 9)
B_FOLLOWS_OWN, B_OWN_ADVERSE, B_NOT_DISTINGUISHED = "follows own", "own adverse", "not distinguished"
D_RIVAL_EXCLUDED, D_NOT_DISTINGUISHED, D_RIVAL_NOT_ESTABLISHED = "rival excluded", "not distinguished", "rival not established"
D_FOLLOWS_RIVAL, D_FOLLOWS_NEITHER, D_NOT_ADJUDICABLE = "follows rival", "follows neither", "not adjudicable here"

CAUSE_APPARATUS = "apparatus unevaluable ({key})"                                           # L1
CAUSE_NO_CONTOUR = "no eligible contour"                                                    # L2
CAUSE_NO_EDGE = "no edge at θ"                                                              # L3
CAUSE_UNDER_RESOLVED = "under-resolved"                                                     # L4
CAUSE_UNSTABLE = "unstable edge"                                                            # L5
CAUSE_FINITE_RESOLUTION = "finite resolution"                                               # L6; arm A4
CAUSE_OWN_ADVERSE = "no registered contour of own index within ε"                           # L7
CAUSE_INSUFFICIENT = "insufficient informative levels"                                      # arm A4
CAUSE_ISOLATED = "isolated adverse level"                                                   # arm A4

STATE_UNEVALUABLE, STATE_NOT_SCORED, STATE_NOT_INFORMATIVE, STATE_INFORMATIVE = "unevaluable", "not scored", "not informative", "informative"
KIND_APPARATUS, KIND_UNAVAILABLE, KIND_SCIENTIFIC_ND, KIND_SCIENTIFIC_ADVERSE = "apparatus", "unavailable", "scientific ND", "scientific adverse at the level"

ARM_ADVERSE, ARM_COMPATIBLE, ARM_NOT_DISTINGUISHED, ARM_NO_DETERMINATION = "ADVERSE", "COMPATIBLE", "NOT DISTINGUISHED", "no qualified determination"
FLIGHT_PRODUCED, FLIGHT_NOT_PRODUCED, FLIGHT_NOT_DISTINGUISHED = "PRODUCED", "NOT PRODUCED", "NOT DISTINGUISHED"
FLIGHT_DISTINGUISHED = "DISTINGUISHED"
FLIGHT_NO_DETERMINATION = "no qualified scientific determination"

PROFILE_NON_MONOTONE = "non-monotone criterion profile"
PROFILE_ALL = "criterion met at all tested levels"
PROFILE_NONE = "criterion met at no tested level"
PROFILE_BOTH = "both criterion phases observed"

LEVEL_TABLE: Tuple[Tuple[str, str, str, str], ...] = (            # own, rival, B status, discrimination status (§5.6)
    (COMPATIBLE, ADVERSE, B_FOLLOWS_OWN, D_RIVAL_EXCLUDED),
    (COMPATIBLE, COMPATIBLE, B_FOLLOWS_OWN, D_NOT_DISTINGUISHED),
    (COMPATIBLE, UNRESOLVED, B_FOLLOWS_OWN, D_RIVAL_NOT_ESTABLISHED),
    (ADVERSE, COMPATIBLE, B_OWN_ADVERSE, D_FOLLOWS_RIVAL),
    (ADVERSE, ADVERSE, B_OWN_ADVERSE, D_FOLLOWS_NEITHER),
    (ADVERSE, UNRESOLVED, B_OWN_ADVERSE, D_RIVAL_NOT_ESTABLISHED),
    (UNRESOLVED, COMPATIBLE, B_NOT_DISTINGUISHED, D_NOT_DISTINGUISHED),
    (UNRESOLVED, ADVERSE, B_NOT_DISTINGUISHED, D_NOT_DISTINGUISHED),
    (UNRESOLVED, UNRESOLVED, B_NOT_DISTINGUISHED, D_NOT_DISTINGUISHED),
)
D_WITNESS_MIN = 3                                                 # §5.6 flight D: at least 3 informative witnessing levels per TB arm
ARM_COMPATIBLE_MIN = 3                                            # §5.6 arm rule 3: at least 3 informative levels
CP_CONFIDENCE_TAIL = 0.025                                        # §1.3(a): two-sided 95%
D_TERRAIN = "TB"

# what the evaluator (M3) calls the causes, and the contract's label for each
EVALUATOR_CAUSES: Tuple[Tuple[str, str], ...] = (
    ("no edge at theta", CAUSE_NO_EDGE), ("below the informative minimum", CAUSE_UNDER_RESOLVED),
    ("unstable edge", CAUSE_UNSTABLE), ("no eligible contour", CAUSE_NO_CONTOUR),
)

OUTCOME_DECLARATION = (
    ("level_table", LEVEL_TABLE), ("d_not_adjudicable", D_NOT_ADJUDICABLE),
    ("level_causes", (CAUSE_APPARATUS, CAUSE_NO_CONTOUR, CAUSE_NO_EDGE, CAUSE_UNDER_RESOLVED, CAUSE_UNSTABLE, CAUSE_FINITE_RESOLUTION, CAUSE_OWN_ADVERSE)),
    ("arm_labels", (ARM_NO_DETERMINATION, ARM_ADVERSE, ARM_COMPATIBLE, ARM_NOT_DISTINGUISHED)),
    ("arm_causes_in_listing_order", (CAUSE_INSUFFICIENT, CAUSE_ISOLATED, CAUSE_FINITE_RESOLUTION)), ("arm_cause_rule", "every cause that holds"),
    ("arm_compatible_min", ARM_COMPATIBLE_MIN),
    ("flight_labels", (FLIGHT_NO_DETERMINATION, FLIGHT_NOT_PRODUCED, FLIGHT_NOT_DISTINGUISHED, FLIGHT_PRODUCED, FLIGHT_DISTINGUISHED)),
    ("d_terrain", D_TERRAIN), ("d_witness_min", D_WITNESS_MIN),
    ("profiles_in_order", (PROFILE_NON_MONOTONE, PROFILE_ALL, PROFILE_NONE, PROFILE_BOTH)),
    ("cp_tail", CP_CONFIDENCE_TAIL), ("cp_rule", "binomial tail equal to the tail probability, by bisection"),
    ("evaluator_causes", EVALUATOR_CAUSES),
)
OUTCOME_DECLARATION_SHA256_LITERAL = "c94ec4bd7c9aa532264ab2adc91ab6d4948ebff652b5b58380e1befb54a35407"


class F9OutcomeError(RuntimeError):
    """An outcome rule was given something the contract does not define (an apparatus failure, §7)."""


def verify_outcome_declaration() -> str:
    C.verify_frozen_identity()
    if (C.F9_SURVIVAL_MIN, C.F9_N_SEEDS, len(C.F9_LEVELS_MICRO), len(C.F9_REQUIRED_TERRAINS)) != (36, 40, 25, 7):
        raise F9ConfigError("the survival criterion, panel, grid or required arms are not those of the contract")
    if len(LEVEL_TABLE) != 9 or {(o, r) for o, r, _, _ in LEVEL_TABLE} != {(o, r) for o in (COMPATIBLE, ADVERSE, UNRESOLVED) for r in (COMPATIBLE, ADVERSE, UNRESOLVED)}:
        raise F9ConfigError("the level table does not cover every pair of results once")
    if D_TERRAIN not in C.F9_REQUIRED_TERRAINS or C.same_family_latent(D_TERRAIN) is not None:
        raise F9ConfigError("the discrimination terrain is not a required terrain with separate families")
    lit = OUTCOME_DECLARATION_SHA256_LITERAL
    if len(lit) != 64 or any(ch not in "0123456789abcdef" for ch in lit):
        raise F9ConfigError("outcome declaration digest literal is not a 64-hex sha256 (no sentinel or placeholder is accepted)")
    if C.frozen_digest(OUTCOME_DECLARATION) != lit:
        raise F9ConfigError("outcome declaration differs from its frozen literal digest")
    return lit


def _arm(terrain, composition) -> Tuple[str, str]:
    if (terrain, composition) not in C.F9_ARMS: raise F9ConfigError(f"not a declared arm: {terrain!r}.{composition!r}")
    return terrain, composition


def is_same_family(terrain: str) -> bool:
    if terrain not in C.F9_TERRAINS: raise F9ConfigError(f"not a declared terrain: {terrain!r}")
    return C.same_family_latent(terrain) is not None


# ======================= level =======================
def level_apparatus(key: str) -> Dict[str, object]:
    """L1: the level is unevaluable for an apparatus reason named by `key`."""
    if not isinstance(key, str) or not key: raise F9OutcomeError("an apparatus cause needs a key")
    return {"state": STATE_UNEVALUABLE, "kind": KIND_APPARATUS, "cause": CAUSE_APPARATUS.format(key=key), "informative": False,
            "own": None, "rival": None, "b_status": None, "discrimination": None, "causes": [CAUSE_APPARATUS.format(key=key)]}


def level_tier(own: str, rival: Optional[str], same_family: bool, *, not_informative_cause: Optional[str] = None) -> Dict[str, object]:
    """The level record from the two indices' results (§5.6 level tier, §7 L2 to L7).

    `not_informative_cause` is one of `no edge at θ`, `under-resolved`, `unstable edge` (L3 to L5) or `no eligible
    contour` (L2: a constant index, which is T0's; neither index is scored); then `own` and `rival` must be None.
    Otherwise `own` and `rival` are the two indices' results."""
    if type(same_family) is not bool: raise F9OutcomeError("same_family is a bool")
    if not_informative_cause is not None:
        if own is not None or rival is not None: raise F9OutcomeError("a level that is not informative carries no index result")
        if not_informative_cause == CAUSE_NO_CONTOUR:
            return {"state": STATE_NOT_SCORED, "kind": KIND_UNAVAILABLE, "cause": CAUSE_NO_CONTOUR, "informative": False,
                    "own": None, "rival": None, "b_status": None, "discrimination": None, "causes": [CAUSE_NO_CONTOUR]}
        if not_informative_cause not in (CAUSE_NO_EDGE, CAUSE_UNDER_RESOLVED, CAUSE_UNSTABLE): raise F9OutcomeError(f"not a cause of an uninformative level: {not_informative_cause!r}")
        return {"state": STATE_NOT_INFORMATIVE, "kind": KIND_SCIENTIFIC_ND, "cause": not_informative_cause, "informative": False,
                "own": None, "rival": None, "b_status": None, "discrimination": None, "causes": [not_informative_cause]}
    results = (COMPATIBLE, ADVERSE, UNRESOLVED)
    if own not in results or rival not in results: raise F9OutcomeError(f"not index results: {own!r}, {rival!r}")
    if same_family and rival != own: raise F9OutcomeError("on a same-family terrain the two indices share one family: their results must be equal")
    causes: List[str] = []
    b, d = next((bb, dd) for o, r, bb, dd in LEVEL_TABLE if (o, r) == (own, rival))
    if same_family: d = D_NOT_ADJUDICABLE
    if own == UNRESOLVED or rival == UNRESOLVED: causes.append(CAUSE_FINITE_RESOLUTION)       # L6
    if own == ADVERSE: causes.append(CAUSE_OWN_ADVERSE)                                       # L7
    kind = KIND_SCIENTIFIC_ADVERSE if own == ADVERSE else (KIND_SCIENTIFIC_ND if own == UNRESOLVED else None)
    return {"state": STATE_INFORMATIVE, "kind": kind, "cause": None, "informative": True,           # an informative level's causes are in `causes`
            "own": own, "rival": rival, "b_status": b, "discrimination": d, "causes": causes}


def level_from_evaluation(record: Dict[str, object], terrain: str, composition: str) -> Dict[str, object]:
    """The level record of an arm from the evaluator's record of that level (M3's `evaluate_level`), which carries a
    result for each index under the names 'P' and 'H'. The evaluator's cause strings are translated to the contract's."""
    _arm(terrain, composition)
    rival_name = "H" if composition == "P" else "P"
    try:
        own, rival = record["indices"][composition], record["indices"][rival_name]
        own_result, rival_result = own["result"], rival["result"]
    except (KeyError, TypeError):
        raise F9OutcomeError("the evaluation record does not carry both indices")
    translate = dict(EVALUATOR_CAUSES)
    def cause(x):
        c = x.get("cause")
        if c not in translate: raise F9OutcomeError(f"the evaluator gave an unknown cause: {c!r}")
        return translate[c]
    same = is_same_family(terrain)
    if own_result == "not informative" or rival_result == "not informative":
        # Steps 1 to 4 and the invalid draws belong to the map, not to an index, and a constant index is T0's, where both
        # indices are constant. So on every declared arm the two indices are unavailable together and for one reason.
        if own_result != rival_result or cause(own) != cause(rival):
            raise F9OutcomeError("the two indices of one level cannot be unavailable for different reasons, or one without the other")
        if terrain == "T0":                                       # L2 precedes L3 to L5: the constant index is not scored, whatever the map
            return level_tier(None, None, same, not_informative_cause=CAUSE_NO_CONTOUR)
        if cause(own) == CAUSE_NO_CONTOUR: raise F9OutcomeError("`no eligible contour` is the constant index's state: T0's, and only T0's")
        return level_tier(None, None, same, not_informative_cause=cause(own))
    if terrain == "T0": raise F9OutcomeError("T0's index is constant: it cannot have been scored")
    return level_tier(own_result, rival_result, same)


# ======================= arm =======================
_LEVEL_KEYS = ("state", "kind", "cause", "informative", "own", "rival", "b_status", "discrimination", "causes")


def _check_level(rec) -> Dict[str, object]:
    """A level record is accepted only if it is exactly what `level_tier` or `level_apparatus` returns for its own
    contents: the record is rebuilt from its inputs and compared. A record whose fields contradict one another, or
    that lacks or adds a field, is refused."""
    if not isinstance(rec, dict) or {(type(k), k) for k in rec} != {(str, k) for k in _LEVEL_KEYS}: raise F9OutcomeError("not a level record")
    state = rec["state"]
    if state == STATE_UNEVALUABLE:
        cause = rec["cause"]
        head, tail = CAUSE_APPARATUS.split("{key}")
        if not isinstance(cause, str) or not cause.startswith(head) or not cause.endswith(tail) or len(cause) <= len(head) + len(tail):
            raise F9OutcomeError("an unevaluable level record does not carry an apparatus cause")
        rebuilt = level_apparatus(cause[len(head):len(cause) - len(tail)])
    elif state in (STATE_NOT_SCORED, STATE_NOT_INFORMATIVE):
        if rec["own"] is not None or rec["rival"] is not None: raise F9OutcomeError("a level that is not informative carries no index result")
        rebuilt = level_tier(None, None, False, not_informative_cause=rec["cause"])
    elif state == STATE_INFORMATIVE:
        rebuilt = level_tier(rec["own"], rec["rival"], rec["discrimination"] == D_NOT_ADJUDICABLE)
    else:
        raise F9OutcomeError("not a level record")
    if rebuilt != rec or any(type(rebuilt[k]) is not type(rec[k]) for k in _LEVEL_KEYS): raise F9OutcomeError("a level record's fields contradict one another")
    return rec


def arm_tier(levels: Dict[int, Optional[Dict[str, object]]]) -> Dict[str, object]:
    """The arm's B record from its level records, keyed by κ in micro-units (§5.6 arm tier, §7 A1 to A4). A registered
    level that is absent from `levels`, or present as None, is a missing record: an apparatus cause (A1)."""
    verify_outcome_declaration()
    return _arm_tier(levels)


def _arm_tier(levels) -> Dict[str, object]:
    if not isinstance(levels, dict): raise F9OutcomeError("levels is a mapping from a registered level to its record")
    for k in levels:
        if type(k) is not int or k not in C.F9_LEVELS_MICRO: raise F9OutcomeError(f"not a registered level: {k!r}")
    grid = C.F9_LEVELS_MICRO
    recs = [(_check_level(levels[k]) if levels.get(k) is not None else level_apparatus("missing level record")) for k in grid]
    unevaluable = [grid[i] for i, r in enumerate(recs) if r["state"] == STATE_UNEVALUABLE]
    informative = [grid[i] for i, r in enumerate(recs) if r["informative"]]
    adverse = [grid[i] for i, r in enumerate(recs) if r["informative"] and r["b_status"] == B_OWN_ADVERSE]
    not_dist = [grid[i] for i, r in enumerate(recs) if r["informative"] and r["b_status"] == B_NOT_DISTINGUISHED]
    follows = [grid[i] for i, r in enumerate(recs) if r["informative"] and r["b_status"] == B_FOLLOWS_OWN]
    pairs = [(grid[i], grid[i + 1]) for i in range(len(grid) - 1)
             if recs[i]["informative"] and recs[i + 1]["informative"] and recs[i]["b_status"] == B_OWN_ADVERSE and recs[i + 1]["b_status"] == B_OWN_ADVERSE]
    out: Dict[str, object] = {"levels": {grid[i]: dict(r, causes=list(r["causes"])) for i, r in enumerate(recs)},      # the 25 level records the arm was computed from
                              "informative_levels": informative, "own_adverse_levels": adverse, "not_distinguished_levels": not_dist,
                              "follows_own_levels": follows, "unevaluable_levels": unevaluable, "adjacent_adverse_pairs": [list(p) for p in pairs],
                              "level_causes": {grid[i]: list(r["causes"]) for i, r in enumerate(recs) if r["causes"]}}
    if unevaluable:                                               # A1
        out.update(determination=ARM_NO_DETERMINATION, rule="A1", causes=sorted({c for i, r in enumerate(recs) if r["state"] == STATE_UNEVALUABLE for c in r["causes"]}))
    elif pairs:                                                   # A2
        out.update(determination=ARM_ADVERSE, rule="A2", causes=[])
    elif len(informative) >= ARM_COMPATIBLE_MIN and len(follows) == len(informative):   # A3
        out.update(determination=ARM_COMPATIBLE, rule="A3", causes=[], rests_on_levels=informative)
    else:                                                         # A4: every cause that holds, in the contract's listing order
        causes = []
        if len(informative) < ARM_COMPATIBLE_MIN: causes.append(CAUSE_INSUFFICIENT)
        if adverse: causes.append(CAUSE_ISOLATED)
        if not_dist: causes.append(CAUSE_FINITE_RESOLUTION)
        if not causes: raise F9OutcomeError("no cause holds for a NOT DISTINGUISHED arm")       # cannot happen; kept as a guard
        out.update(determination=ARM_NOT_DISTINGUISHED, rule="A4", causes=causes)
    return out


# ======================= flight =======================
def _same_typed(a, b) -> bool:
    """Equality of two records as values AND as types, recursively (True is not 1; 1 is not 1.0; a list is not a tuple)."""
    if type(a) is not type(b): return False
    if isinstance(a, dict):
        if {(type(k), k) for k in a} != {(type(k), k) for k in b} or not all(type(k) in (int, str) for k in a): return False
        return all(_same_typed(v, b[k]) for k, v in a.items())
    if isinstance(a, list): return len(a) == len(b) and all(_same_typed(x, y) for x, y in zip(a, b))
    return a == b


def _check_arm(rec) -> Dict[str, object]:
    """An arm record is accepted only if it is exactly what `arm_tier` returns for the level records it carries: the arm
    is recomputed from `rec["levels"]` (each level record is itself rebuilt and compared) and every field of the given
    record, with its type, must equal the recomputed record's. A record with a missing, extra, malformed or contradictory
    field is refused (L2 M4 round 1, D1). This is consistency, not provenance."""
    if not isinstance(rec, dict) or not isinstance(rec.get("levels"), dict): raise F9OutcomeError("not an arm record")
    if {(type(k), k) for k in rec["levels"]} != {(int, k) for k in C.F9_LEVELS_MICRO} or any(v is None for v in rec["levels"].values()):
        raise F9OutcomeError("an arm record carries one level record for each registered level")
    rebuilt = _arm_tier(rec["levels"])
    if not _same_typed(rebuilt, rec): raise F9OutcomeError("an arm record's fields do not follow from the level records it carries")
    return rec


def flight_b(composition: str, arms: Dict[str, Optional[Dict[str, object]]], qualification_passed: bool) -> Dict[str, object]:
    """B for composition X: the conjunction over the seven required arms, keyed by terrain. An absent or None arm record
    is a missing mandatory input: it propagates as `no qualified scientific determination` (§7)."""
    verify_outcome_declaration()
    if composition not in C.F9_COMPOSITIONS: raise F9ConfigError(f"not a declared composition: {composition!r}")
    if type(qualification_passed) is not bool: raise F9OutcomeError("qualification_passed is a bool")
    if not isinstance(arms, dict) or any(t not in C.F9_REQUIRED_TERRAINS for t in arms): raise F9OutcomeError("arms is a mapping from a required terrain to its arm record")
    det = {t: (_check_arm(arms[t])["determination"] if arms.get(t) is not None else None) for t in C.F9_REQUIRED_TERRAINS}
    missing = [t for t, d in det.items() if d is None]
    without = [t for t, d in det.items() if d == ARM_NO_DETERMINATION]
    adverse = [t for t, d in det.items() if d == ARM_ADVERSE]
    nd = [t for t, d in det.items() if d == ARM_NOT_DISTINGUISHED]
    compatible = [t for t, d in det.items() if d == ARM_COMPATIBLE]
    out: Dict[str, object] = {"composition": composition, "qualification_passed": qualification_passed, "arms": det, "missing_arms": missing,
                              "arms_without_determination": without, "adverse_arms": adverse, "not_distinguished_arms": nd, "compatible_arms": compatible}
    if not qualification_passed or missing or without:
        why = (["qualification not passed"] if not qualification_passed else []) + [f"missing arm record: {t}" for t in missing] + [f"arm without a qualified determination: {t}" for t in without]
        out.update(B=FLIGHT_NO_DETERMINATION, reasons=why)
    elif adverse: out.update(B=FLIGHT_NOT_PRODUCED, reasons=[f"ADVERSE: {t}" for t in adverse])
    elif nd: out.update(B=FLIGHT_NOT_DISTINGUISHED, reasons=[f"NOT DISTINGUISHED: {t}" for t in nd])
    else:
        out.update(B=FLIGHT_PRODUCED, reasons=[],
                   domain={t: list(arms[t]["rests_on_levels"]) for t in C.F9_REQUIRED_TERRAINS},
                   resolution={"theta_micro": C.F9_THETA_MICRO, "epsilon_micro": C.F9_EPSILON_MICRO, "component_min_bonds": C.F9_COMPONENT_MIN_BONDS,
                               "grid": C.F9_GRID, "n_seeds": C.F9_N_SEEDS, "tail_ticks": C.F9_TAIL_TICKS})
    return out


def _witnesses(levels: Dict[int, Optional[Dict[str, object]]]) -> Tuple[List[int], List[int]]:
    wit, rival = [], []
    for k in C.F9_LEVELS_MICRO:
        r = levels.get(k)
        if r is None or not _check_level(r)["informative"]: continue
        if r["b_status"] == B_FOLLOWS_OWN and r["discrimination"] == D_RIVAL_EXCLUDED: wit.append(k)
        if r["discrimination"] == D_FOLLOWS_RIVAL: rival.append(k)
    return wit, rival


def flight_d(level_records: Dict[str, Optional[Dict[int, Optional[Dict[str, object]]]]], qualification_passed: bool) -> Dict[str, object]:
    """D on TB, from the level records of the two TB arms keyed by composition ('P', 'H'). Each arm's determination is
    computed here from its levels by `arm_tier`, so the two cannot disagree. An absent or None arm is a missing
    mandatory input."""
    verify_outcome_declaration()
    if type(qualification_passed) is not bool: raise F9OutcomeError("qualification_passed is a bool")
    if not isinstance(level_records, dict) or any(c not in C.F9_COMPOSITIONS for c in level_records): raise F9OutcomeError("the TB arms are keyed by composition")
    arms = {c: (arm_tier(level_records[c]) if level_records.get(c) is not None else None) for c in C.F9_COMPOSITIONS}
    det = {c: (arms[c]["determination"] if arms[c] is not None else None) for c in C.F9_COMPOSITIONS}
    out: Dict[str, object] = {"terrain": D_TERRAIN, "qualification_passed": qualification_passed, "arms": det}
    blocked = [c for c in C.F9_COMPOSITIONS if det[c] is None or det[c] == ARM_NO_DETERMINATION]
    if not qualification_passed or blocked:
        out.update(D=FLIGHT_NO_DETERMINATION, reasons=(["qualification not passed"] if not qualification_passed else [])
                   + [(f"missing arm record: {D_TERRAIN}.{c}" if det[c] is None else f"arm without a qualified determination: {D_TERRAIN}.{c}") for c in blocked])
        return out
    wit, rival = {}, {}
    for c in C.F9_COMPOSITIONS: wit[c], rival[c] = _witnesses(level_records[c])
    out.update(witness_levels=wit, follows_rival_levels=rival)
    short = [c for c in C.F9_COMPOSITIONS if len(wit[c]) < D_WITNESS_MIN]
    any_rival = [c for c in C.F9_COMPOSITIONS if rival[c]]
    if not short and not any_rival: out.update(D=FLIGHT_DISTINGUISHED, reasons=[])
    else:
        out.update(D=FLIGHT_NOT_DISTINGUISHED,
                   reasons=[f"under {D_WITNESS_MIN} witnessing levels in the {c} arm ({len(wit[c])})" for c in short] + [f"'follows rival' at an informative level of the {c} arm" for c in any_rival])
    return out


# ======================= persistence =======================
def _binom_tail_ge(s: int, n: int, p: float) -> float:
    """P(X >= s) for X ~ Binomial(n, p)."""
    return math.fsum(math.comb(n, k) * p ** k * (1.0 - p) ** (n - k) for k in range(s, n + 1))


def clopper_pearson(s: int, n: int = C.F9_N_SEEDS) -> Tuple[float, float]:
    """The two-sided 95% Clopper–Pearson interval for a survival probability from s survivors of n (see module docstring).
    The tail probability is the declared 0.025 and is not an argument."""
    if type(s) is not int or type(n) is not int or n <= 0 or not (0 <= s <= n): raise F9OutcomeError("s survivors of n: integers with 0 <= s <= n")
    return _clopper_pearson(s, n, CP_CONFIDENCE_TAIL)


@functools.lru_cache(maxsize=None)
def _clopper_pearson(s: int, n: int, tail: float) -> Tuple[float, float]:
    def solve(f):                                                 # f increasing in p from below `tail` to above it
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if mid == lo or mid == hi: break
            if f(mid) < tail: lo = mid
            else: hi = mid
        return 0.5 * (lo + hi)
    lower = 0.0 if s == 0 else solve(lambda p: _binom_tail_ge(s, n, p))                       # P(X >= s) rises with p
    upper = 1.0 if s == n else 1.0 - solve(lambda q: _binom_tail_ge(n - s, n, q))             # P(X <= s; p) = P(n - X >= n - s; 1 - p)
    return lower, upper


def persistence_record(survivors: Dict[int, Optional[int]]) -> Dict[str, object]:
    """The §5.4 record of a skeleton sweep: `survivors[κ micro]` = the number of the 40 seeds whose run survived (active
    at every tail tick). A registered level that is absent or None is a missing record: the profile is then
    `apparatus unevaluable (missing level record)` and nothing is described."""
    verify_outcome_declaration()
    if not isinstance(survivors, dict): raise F9OutcomeError("survivors is a mapping from a registered level to a count")
    for k, s in survivors.items():
        if type(k) is not int or k not in C.F9_LEVELS_MICRO: raise F9OutcomeError(f"not a registered level: {k!r}")
        if s is not None and (type(s) is not int or not (0 <= s <= C.F9_N_SEEDS)): raise F9OutcomeError(f"not a survivor count: {s!r}")
    grid = C.F9_LEVELS_MICRO
    missing = [k for k in grid if survivors.get(k) is None]
    if missing:
        return {"profile": None, "kind": KIND_APPARATUS, "cause": CAUSE_APPARATUS.format(key="missing level record"), "missing_levels": missing,
                "kappa_c_micro": None, "bracket_micro": None, "levels": None}
    met = [survivors[k] >= C.F9_SURVIVAL_MIN for k in grid]
    levels = {k: {"survivors": survivors[k], "n": C.F9_N_SEEDS, "meets_criterion": met[i], "clopper_pearson_95": list(clopper_pearson(survivors[k]))} for i, k in enumerate(grid)}
    first_terminal = len(grid)                                    # index of the first level of the terminal stretch that meets the criterion
    while first_terminal > 0 and met[first_terminal - 1]: first_terminal -= 1
    out: Dict[str, object] = {"kind": None, "cause": None, "levels": levels, "criterion": {"survivors_min": C.F9_SURVIVAL_MIN, "n": C.F9_N_SEEDS},
                              "note": "a panel and grid description; not a population confidence bound; no claim about coupling"}
    non_monotone = any(met[i] and not met[j] for i in range(len(grid)) for j in range(i + 1, len(grid)))
    def endpoint(i): return {"level_micro": grid[i], **levels[grid[i]]}
    if non_monotone:
        suffix = grid[first_terminal] if first_terminal < len(grid) else None
        out.update(profile=PROFILE_NON_MONOTONE, kappa_c_micro=None, kappa_c_cause="non-monotone criterion profile: no crossing is claimed", bracket_micro=None,
                   descriptive_suffix_micro=suffix, descriptive_suffix_cause=None if suffix is not None else "no terminal stretch meets the criterion",
                   endpoints={"lower": None, "lower_cause": "no bracket on a non-monotone profile", "upper": None, "upper_cause": "no bracket on a non-monotone profile"})
    elif all(met):
        out.update(profile=PROFILE_ALL, kappa_c_micro=grid[0], kappa_c_cause=None, bracket_micro=None,
                   endpoints={"lower": None, "lower_cause": "unbracketed on the lower side: every tested level meets the criterion", "upper": endpoint(0), "upper_cause": None})
    elif not any(met):
        out.update(profile=PROFILE_NONE, kappa_c_micro=None, kappa_c_cause="criterion met at no tested level", bracket_micro=None,
                   endpoints={"lower": None, "lower_cause": "criterion met at no tested level", "upper": None, "upper_cause": "criterion met at no tested level"})
    else:                                                         # a failing lower stretch, then a terminal stretch meeting the criterion
        out.update(profile=PROFILE_BOTH, kappa_c_micro=grid[first_terminal], kappa_c_cause=None, bracket_micro=[grid[first_terminal - 1], grid[first_terminal]],
                   endpoints={"lower": endpoint(first_terminal - 1), "lower_cause": None, "upper": endpoint(first_terminal), "upper_cause": None})
    return out
