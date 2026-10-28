"""mfa_instrument/f8/verdict.py — Flight 8 module M4: the TOTAL verdict function and the pass-2 router
(Contract F8 v0.8.4 §4.4–§4.7, §6.2; design note v0.3 §5–§6; E1 M4 carried verbatim except rule 4c).

CARRIED VERBATIM from E1 v0.4 §5 / v0.8 C–E (contract §4.4: "diagnosis: none implicated"): rules 1, 2, 3, 4a, 4b, the
precedence 1 > 2 > 3 > 4 and a > b > c > d, router rows P2R-1 … P2R-7 with 8 insertions in P2R-5/6 and 4 + 4 in
P2R-4, exact integer-micro-unit arithmetic with round-half-to-even, and the collision fallback (move to the
round-half-even midpoint of the accepted neighbours within the interval, else drop; every action recorded).

  rule 1  confident order violation (any confident S strictly below any confident N) -> NOT_PRODUCED (order violation)
  rule 2  no confident N anywhere:  bottom level confident S -> NOT_PRODUCED (no null-consistent phase)
                                    otherwise               -> NOT_DISTINGUISHED (bottom uncertainty)
  rule 3  no confident S anywhere:  top level confident N    -> NOT_PRODUCED (no sustained phase)
                                    otherwise               -> NOT_DISTINGUISHED (top uncertainty)
  rule 4  both confident phases, order respected — the band is the open interval between the highest confident N
          and the lowest confident S, unique by order-respect:
       4a any M outside the band                                   -> NOT_DISTINGUISHED (off-boundary mixture)
       4b U outside the band: at most OFF_BAND_U_ALLOWANCE, isolated -> else NOT_DISTINGUISHED (off-boundary unresolved)
       4c (F8, REPLACED — contract §4.4): the MEASURED WIDTH of the band, m(lowest confident S) − m(highest
          confident N) on the final level set, exceeds W_res          -> NOT_DISTINGUISHED (boundary unresolved at
                                                                        declared resolution W_res)
       4d otherwise                                                -> LOCATED, bracket [m₋, m₊]

W_res = 3 pass-1 spacings = 293,478 micro-units of m (§4.5; freeze record §3 item 18): a declaration in PD5's sense —
the instrument commits that a transition region narrower than W_res is bracketed and one wider is reported unresolved
at this resolution. E1's count-based 4c (BOUNDARY_SPAN_LIMIT = 3 levels) is NOT carried; the diagnosis located E1's
onset failures in that span limit after P2R-5/6 densification (L2 2026-10-20). No criterion anywhere references jump
size, slope, amplitude monotonicity or adjacent-level separation (§4.7: line, not drama).

JURISDICTION (§4.7, §4.9, §1.3(a)). No verdict of this module bears on P1: P1 is adjudicated by the M-P1 evaluator of
§4.11 alone. This module's `NOT_PRODUCED` is the morphology label of the g = 0-null-relative detection (expected over
the F8 sweep: rule 2, `no_null_consistent_phase`, because the realization exceeds the null's θ_P at every level); it is
never written `NOT PRODUCED` and never enters the P1 determination.

ROUTING SLACK (§4.6, §6.2, Appendix A). `routing_slack_table` reproduces Appendix A's certified Δ_route(B) for B = 1…9
from this module's own insertion arithmetic — every band of B pass-1 spacings, eight round-half-even interior
insertions, collided candidates REMOVED (the worst case for gaps, which dominates both fallback moves and drops), final
level set = every pass-1 level in the band plus kept insertions, Δ_route(B) = 2 × the largest final gap — and the
fact that candidates collide with pass-1 levels at every B that is a multiple of 3. The live router uses the fallback
(move/drop); the audit uses removal, as Appendix A does; both are reported.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from ..config import MICRO_UNITS
from . import config as C
from .classify import LEVEL_LABELS
from .config import F8_LEVELS_MICRO, F8_M_MAX_MICRO, F8_M_MIN_MICRO, S_P1_MICRO, W_RES_MICRO, level_id

CONFIDENT = ("S", "N")
UNCERTAIN = ("M", "U")
OFF_BAND_U_ALLOWANCE = 2                 # carried from E1 (isolated, non-adjacent); re-qualified under M6 like everything else

VERDICTS = ("NOT_PRODUCED", "NOT_DISTINGUISHED", "LOCATED")
NP_CAUSES = ("order_violation", "no_null_consistent_phase", "no_sustained_phase")
ND_CAUSES = ("bottom_uncertainty", "top_uncertainty", "off_boundary_mixture", "off_boundary_unresolved", "boundary_unresolved_at_W_res")
RULES = ("1", "2", "3", "4a", "4b", "4c", "4d")

P2R_ROWS = ("P2R-1", "P2R-2", "P2R-3", "P2R-4", "P2R-5", "P2R-6", "P2R-7")
P2R_SINGLE_BAND_INSERTIONS = 8           # rows 5 and 6 (contract §4.4)
P2R_PER_INTERVAL_INSERTIONS = 4          # row 4 (two intervals, 4 + 4)

VERDICT_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("labels", LEVEL_LABELS), ("confident", CONFIDENT), ("uncertain", UNCERTAIN),
    ("verdicts", VERDICTS), ("np_causes", NP_CAUSES), ("nd_causes", ND_CAUSES), ("rules", RULES),
    ("off_band_u_allowance", OFF_BAND_U_ALLOWANCE), ("rule_4c_form", "measured_band_width_exceeds_W_res"), ("w_res_micro", W_RES_MICRO),
    ("p2r_rows", P2R_ROWS), ("p2r_single_band_insertions", P2R_SINGLE_BAND_INSERTIONS),
    ("p2r_per_interval_insertions", P2R_PER_INTERVAL_INSERTIONS),
    ("micro_units", MICRO_UNITS), ("rounding", "round_half_to_even"),
    ("bottom_micro", F8_M_MIN_MICRO), ("top_micro", F8_M_MAX_MICRO), ("s_p1_micro", S_P1_MICRO),
)
VERDICT_DECLARATION_SHA256_LITERAL = "8648f273dbee910c37b9594b84d96310f4267f3775f5a60e8f64b2f83647595b"

# The F8 archetype -> intended-verdict table (contract §5.2). Known answers for M6; M4 reproduces it from label sequences.
ARCHETYPE_TABLE: Tuple[Tuple[str, str, Optional[str]], ...] = (
    ("gentle_onset", "LOCATED", None),
    ("abrupt_onset", "LOCATED", None),
    ("persistent_nonstationary_high_m", "LOCATED", None),
    ("nonmonotone_amplitude", "LOCATED", None),
    ("no_sustained_anywhere", "NOT_PRODUCED", "no_sustained_phase"),
    ("no_null_consistent_anywhere", "NOT_PRODUCED", "no_null_consistent_phase"),
    ("two_resolved_crossings", "NOT_PRODUCED", "order_violation"),
    ("reentrant", "NOT_PRODUCED", "order_violation"),
    ("off_band_mixture", "NOT_DISTINGUISHED", "off_boundary_mixture"),
    ("off_band_unresolved", "NOT_DISTINGUISHED", "off_boundary_unresolved"),
    ("wide_mixed_boundary", "NOT_DISTINGUISHED", "boundary_unresolved_at_W_res"),
    ("unresolved_heavy_boundary", "NOT_DISTINGUISHED", "boundary_unresolved_at_W_res"),
)
ARCHETYPE_TABLE_SHA256_LITERAL = "f1e1f09f00ab238637e73aa167231ef4bf130e7cae0374b5f2e3894feb5b72c9"

# Appendix A of record: Δ_route(B), B = 1..9, certified by exhaustive enumeration (contract §6.2; APPENDIX_A_OF_RECORD.md 94d52762…)
APPENDIX_A_DELTA_ROUTE: Tuple[int, ...] = (21740, 43480, 65218, 86958, 108696, 130436, 152174, 173914, 195654)
APPENDIX_A_DELTA_ROUTE_B4 = 86958
APPENDIX_A_COLLISION_B = (3, 6, 9, 12, 15, 18, 21)


class VerdictDomainError(ValueError):
    """Input outside the verdict function's or router's executable domain."""


def _digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


def verify_frozen_identity() -> None:
    """Fail-closed: M1's identity; the declaration's literal digest; every declared value equal to its live global; the
    archetype table's digest; the label alphabet equal to M2's; W_res = 3 s from M1."""
    C.verify_frozen_identity()
    if _digest(VERDICT_DECLARATION) != VERDICT_DECLARATION_SHA256_LITERAL:
        raise VerdictDomainError("verdict declaration differs from its frozen literal digest")
    d = dict(VERDICT_DECLARATION)
    live = {"labels": LEVEL_LABELS, "confident": CONFIDENT, "uncertain": UNCERTAIN, "verdicts": VERDICTS,
            "np_causes": NP_CAUSES, "nd_causes": ND_CAUSES, "rules": RULES, "off_band_u_allowance": OFF_BAND_U_ALLOWANCE,
            "w_res_micro": W_RES_MICRO, "p2r_rows": P2R_ROWS, "p2r_single_band_insertions": P2R_SINGLE_BAND_INSERTIONS,
            "p2r_per_interval_insertions": P2R_PER_INTERVAL_INSERTIONS, "micro_units": MICRO_UNITS,
            "rounding": "round_half_to_even", "bottom_micro": F8_M_MIN_MICRO, "top_micro": F8_M_MAX_MICRO, "s_p1_micro": S_P1_MICRO}
    for k, v in live.items():
        if d[k] != v or type(d[k]) is not type(v):
            raise VerdictDomainError(f"verdict declaration field {k} differs from the live global")
    if d["rule_4c_form"] != "measured_band_width_exceeds_W_res" or W_RES_MICRO != 3 * S_P1_MICRO or W_RES_MICRO != 293478:
        raise VerdictDomainError("rule 4c form or W_res differs from the contract (§4.4–§4.5)")
    if (OFF_BAND_U_ALLOWANCE, P2R_SINGLE_BAND_INSERTIONS, P2R_PER_INTERVAL_INSERTIONS) != (2, 8, 4):
        raise VerdictDomainError("carried E1 values differ from the contract's (§4.4)")
    if _digest(ARCHETYPE_TABLE) != ARCHETYPE_TABLE_SHA256_LITERAL:
        raise VerdictDomainError("archetype table differs from its frozen literal digest")
    if set(LEVEL_LABELS) != set(CONFIDENT) | set(UNCERTAIN) or MICRO_UNITS != 10 ** 6:
        raise VerdictDomainError("label alphabet or micro-unit base inconsistent with M1/M2")


# ----------------------------------------------------------------------------- inputs
def _sequence(labels: Sequence[str], levels_micro: Sequence[int]) -> Tuple[Tuple[str, ...], Tuple[int, ...]]:
    verify_frozen_identity()
    lab = tuple(labels); lv = tuple(levels_micro)
    if len(lab) != len(lv) or not lab:
        raise VerdictDomainError("labels and levels must be nonempty and of equal length")
    if any(x not in LEVEL_LABELS for x in lab):
        raise VerdictDomainError(f"labels must be drawn from {LEVEL_LABELS}")
    if any(isinstance(k, bool) or not isinstance(k, int) for k in lv):
        raise VerdictDomainError("levels must be exact non-Boolean integer micro-unit values")
    if list(lv) != sorted(lv) or len(set(lv)) != len(lv):
        raise VerdictDomainError("levels must be strictly ascending and distinct")
    if lv[0] < F8_M_MIN_MICRO or lv[-1] > F8_M_MAX_MICRO:
        raise VerdictDomainError("levels outside the frozen admissible range")
    return lab, lv


# ----------------------------------------------------------------------------- the verdict function
@dataclass(frozen=True)
class Verdict:
    verdict: str                      # NOT_PRODUCED | NOT_DISTINGUISHED | LOCATED
    cause: Optional[str]              # the named cause, or None for LOCATED
    rule: str                         # which rule fired: 1, 2, 3, 4a, 4b, 4c, 4d
    bracket_micro: Optional[Tuple[int, int]] = None      # [m₋, m₊] for LOCATED
    evidence: Tuple[Tuple[str, object], ...] = ()

    @property
    def bracket(self) -> Optional[Tuple[str, str]]:
        return (level_id(self.bracket_micro[0]), level_id(self.bracket_micro[1])) if self.bracket_micro else None


def band_indices(labels: Sequence[str]) -> Optional[Tuple[int, int]]:
    """(highest confident N index, lowest confident S index) when both confident phases exist and order is respected."""
    n_idx = [i for i, x in enumerate(labels) if x == "N"]; s_idx = [i for i, x in enumerate(labels) if x == "S"]
    if not n_idx or not s_idx or max(n_idx) > min(s_idx):
        return None
    return max(n_idx), min(s_idx)


def _contiguous_spans(idx: Sequence[int]) -> List[List[int]]:
    spans: List[List[int]] = []
    for i in sorted(idx):
        if spans and i == spans[-1][-1] + 1: spans[-1].append(i)
        else: spans.append([i])
    return spans


def measured_band_width_micro(labels: Sequence[str], levels_micro: Sequence[int]) -> Optional[int]:
    """m(lowest confident S) − m(highest confident N) on the given (final) level set, or None without a band (§4.4 4c)."""
    b = band_indices(labels)
    return None if b is None else int(levels_micro[b[1]] - levels_micro[b[0]])


def evaluate(labels: Sequence[str], levels_micro: Sequence[int]) -> Verdict:
    """The TOTAL verdict function: exactly one rule fires, by the contract's precedence. Applied to the FINAL level set
    (pass-1 levels plus kept insertions) for the verdict of record; at pass 1 it also drives the router."""
    lab, lv = _sequence(labels, levels_micro)
    n_idx = [i for i, x in enumerate(lab) if x == "N"]; s_idx = [i for i, x in enumerate(lab) if x == "S"]
    # rule 1 — confident order violation
    if n_idx and s_idx and min(s_idx) < max(n_idx):
        return Verdict("NOT_PRODUCED", "order_violation", "1", None,
                       (("lowest_confident_S", level_id(lv[min(s_idx)])), ("highest_confident_N", level_id(lv[max(n_idx)]))))
    # rule 2 — no confident N anywhere
    if not n_idx:
        if lab[0] == "S":
            return Verdict("NOT_PRODUCED", "no_null_consistent_phase", "2", None, (("bottom_level", level_id(lv[0])), ("bottom_label", lab[0])))
        return Verdict("NOT_DISTINGUISHED", "bottom_uncertainty", "2", None, (("bottom_level", level_id(lv[0])), ("bottom_label", lab[0])))
    # rule 3 — no confident S anywhere
    if not s_idx:
        if lab[-1] == "N":
            return Verdict("NOT_PRODUCED", "no_sustained_phase", "3", None, (("top_level", level_id(lv[-1])), ("top_label", lab[-1])))
        return Verdict("NOT_DISTINGUISHED", "top_uncertainty", "3", None, (("top_level", level_id(lv[-1])), ("top_label", lab[-1])))
    # rule 4 — both confident phases, order respected; the band is unique
    lo, hi = band_indices(lab)
    inside = range(lo + 1, hi)
    m_out = [i for i, x in enumerate(lab) if x == "M" and not (lo < i < hi)]
    if m_out:
        return Verdict("NOT_DISTINGUISHED", "off_boundary_mixture", "4a", None,
                       (("off_band_M_levels", tuple(level_id(lv[i]) for i in m_out)),))
    u_out = [i for i, x in enumerate(lab) if x == "U" and not (lo < i < hi)]
    u_spans = _contiguous_spans(u_out)
    if len(u_out) > OFF_BAND_U_ALLOWANCE or any(len(s) > 1 for s in u_spans):
        return Verdict("NOT_DISTINGUISHED", "off_boundary_unresolved", "4b", None,
                       (("off_band_U_levels", tuple(level_id(lv[i]) for i in u_out)), ("allowance", OFF_BAND_U_ALLOWANCE),
                        ("adjacent", any(len(s) > 1 for s in u_spans))))
    width = int(lv[hi] - lv[lo])                    # 4c (F8): the measured width of the band on this level set
    if width > W_RES_MICRO:
        return Verdict("NOT_DISTINGUISHED", "boundary_unresolved_at_W_res", "4c", None,
                       (("measured_width_micro", width), ("w_res_micro", W_RES_MICRO), ("band", (level_id(lv[lo]), level_id(lv[hi]))),
                        ("band_interior_levels", tuple(level_id(lv[i]) for i in inside))))
    return Verdict("LOCATED", None, "4d", (lv[lo], lv[hi]),
                   (("band_interior_levels", tuple(level_id(lv[i]) for i in inside)), ("measured_width_micro", width), ("w_res_micro", W_RES_MICRO)))


# ----------------------------------------------------------------------------- the P2R router (carried verbatim)
@dataclass(frozen=True)
class RouterDecision:
    row: str                                   # P2R-1 … P2R-7
    insertions_micro: Tuple[int, ...]          # strictly interior, non-duplicating, ascending
    intervals_micro: Tuple[Tuple[int, int], ...]
    evidence: Tuple[Tuple[str, object], ...] = ()
    fallback_moves: Tuple[Tuple[int, int], ...] = ()      # (nominal, moved) — empty when no collision occurred
    fallback_drops: Tuple[int, ...] = ()


def round_half_to_even_div(num: int, den: int) -> int:
    if den <= 0:
        raise VerdictDomainError("denominator must be positive")
    q, r = divmod(num, den)
    twice = 2 * r
    if twice < den: return q
    if twice > den: return q + 1
    return q if q % 2 == 0 else q + 1


def evenly_spaced_interior(lo_micro: int, hi_micro: int, count: int) -> Tuple[int, ...]:
    """`count` strictly interior points of (lo, hi): x_j = lo + round_half_even((j+1)(hi−lo)/(count+1)), j = 0..count−1."""
    if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
        raise VerdictDomainError("count must be an exact positive non-Boolean integer")
    if any(isinstance(x, bool) or not isinstance(x, int) for x in (lo_micro, hi_micro)) or hi_micro <= lo_micro:
        raise VerdictDomainError("interval must be given as exact ascending integer micro-units")
    width = hi_micro - lo_micro
    return tuple(lo_micro + round_half_to_even_div((j + 1) * width, count + 1) for j in range(count))


def _adjacency_intervals(labels: Sequence[str]) -> List[Tuple[int, int]]:
    out: List[Tuple[int, int]] = []
    conf = [i for i, x in enumerate(labels) if x in CONFIDENT]
    for a, b in zip(conf, conf[1:]):
        if labels[a] == "N" and labels[b] == "S":
            out.append((a, b))
    return out


def route(labels: Sequence[str], levels_micro: Sequence[int]) -> RouterDecision:
    """The pass-2 router: precedence-ordered rows, exactly one executes (E1 verbatim)."""
    lab, lv = _sequence(labels, levels_micro)
    v = evaluate(lab, lv)
    if v.rule in ("2", "3"):
        return RouterDecision("P2R-1", (), (), (("reason", "a confident phase is absent at pass 1"), ("verdict_rule", v.rule)))
    if v.rule == "1":
        return RouterDecision("P2R-2", (), (), (("reason", "confident order violation at pass 1"),))
    intervals = _adjacency_intervals(lab)
    if len(intervals) >= 3:
        return RouterDecision("P2R-3", (), tuple((lv[a], lv[b]) for a, b in intervals), (("reason", "three or more disjoint N->S intervals"),))
    if len(intervals) == 2:
        iv = tuple((lv[a], lv[b]) for a, b in intervals)
        cand = [x for a, b in iv for x in evenly_spaced_interior(a, b, P2R_PER_INTERVAL_INSERTIONS)]
        ins, moves, drops = _resolve_collisions(cand, lv, iv)
        return RouterDecision("P2R-4", ins, iv, (("reason", "exactly two disjoint N->S intervals"),), moves, drops)
    band = band_indices(lab)
    if band is not None:
        lo, hi = band; iv = ((lv[lo], lv[hi]),)
        interior = [i for i in range(lo + 1, hi)]
        row = "P2R-5" if interior else "P2R-6"
        cand = list(evenly_spaced_interior(lv[lo], lv[hi], P2R_SINGLE_BAND_INSERTIONS))
        ins, moves, drops = _resolve_collisions(cand, lv, iv)
        return RouterDecision(row, ins, iv, (("reason", "band with uncertain levels" if interior else "empty band (adjacent confident N, S)"),
                                             ("band", (level_id(lv[lo]), level_id(lv[hi])))), moves, drops)
    return RouterDecision("P2R-7", (), (), (("reason", "no refinement is defined for this sequence"),))


def _resolve_collisions(candidates: Sequence[int], existing: Sequence[int],
                        intervals: Sequence[Tuple[int, int]]) -> Tuple[Tuple[int, ...], Tuple[Tuple[int, int], ...], Tuple[int, ...]]:
    """The frozen fallback (E1 v0.7 C.2 / v0.8 E), verbatim."""
    accepted: List[int] = []; moves: List[Tuple[int, int]] = []; drops: List[int] = []
    taken = set(existing)
    for c in sorted(candidates):
        iv = next((x for x in intervals if x[0] < c < x[1]), None)
        if iv is None:
            drops.append(c); continue
        if c not in taken and c not in accepted:
            accepted.append(c); continue
        below = max([x for x in list(taken) + accepted if iv[0] <= x < c], default=None)
        above = min([x for x in list(taken) + accepted if c < x <= iv[1]], default=None)
        if below is None or above is None:
            drops.append(c); continue
        moved = round_half_to_even_div(below + above, 2)
        if not (iv[0] < moved < iv[1]) or moved in taken or moved in accepted:
            drops.append(c); continue
        accepted.append(moved); moves.append((c, moved))
    return tuple(sorted(accepted)), tuple(moves), tuple(drops)


def final_level_set(pass1_levels: Sequence[int], decision: RouterDecision) -> Tuple[int, ...]:
    """The level set the verdict of record is evaluated on: every pass-1 level plus the router's kept insertions."""
    return tuple(sorted(set(pass1_levels) | set(decision.insertions_micro)))


# ----------------------------------------------------------------------------- the collision audit and routing slack
@dataclass(frozen=True)
class RouterCase:
    row: str
    lo_micro: int
    hi_micro: int
    count: int
    witness_labels: Tuple[str, ...]


def reachable_router_cases() -> Tuple[RouterCase, ...]:
    """Derived from `route()` itself: for every pass-1 index pair (i, j), the canonical witness — N at and below i,
    uncertain strictly between, S at and above j — and what the router returns for it."""
    verify_frozen_identity()
    seen: Dict[Tuple[str, int, int, int], RouterCase] = {}
    n = len(F8_LEVELS_MICRO)
    for i in range(n):
        for j in range(i + 1, n):
            lab = ["U"] * n
            for k in range(0, i + 1): lab[k] = "N"
            for k in range(j, n): lab[k] = "S"
            d = route(tuple(lab), F8_LEVELS_MICRO)
            if not d.insertions_micro and not d.fallback_drops:
                continue
            count = P2R_SINGLE_BAND_INSERTIONS if d.row in ("P2R-5", "P2R-6") else P2R_PER_INTERVAL_INSERTIONS
            for (lo, hi) in d.intervals_micro:
                seen.setdefault((d.row, lo, hi, count), RouterCase(d.row, lo, hi, count, tuple(lab)))
    return tuple(seen[k] for k in sorted(seen))


def dead_rows() -> Dict[str, str]:
    return {"P2R-3": "preempted by rule 1 / P2R-2: multiple N->S intervals imply confident order violation",
            "P2R-4": "preempted by rule 1 / P2R-2: two N->S intervals imply confident order violation",
            "P2R-7": "unreachable: order-respected dual-phase sequences always have the unique band (P2R-5/6)"}


@dataclass(frozen=True)
class CollisionAudit:
    proven: bool                                  # does the no-collision proof close on the REACHABLE surface? (F8: no)
    reachable_cases_checked: int
    reachable_colliding: int
    colliding_band_spacings: Tuple[int, ...]      # the B (band width in pass-1 spacings) at which collisions occur
    arithmetic_cases_checked: int
    arithmetic_colliding: int
    min_gap_micro: int
    fallback_reachable: bool
    example_collision: Optional[Tuple[str, int, int, Tuple[int, ...]]] = None
    example_witness_labels: Tuple[str, ...] = ()


def _collides(lo: int, hi: int, count: int) -> Tuple[bool, Tuple[int, ...], int]:
    ins = evenly_spaced_interior(lo, hi, count)
    interior_levels = {x for x in F8_LEVELS_MICRO if lo < x < hi}
    hits = tuple(sorted(set(ins) & interior_levels))
    vals = sorted(set(ins))
    gaps = [b - a for a, b in zip(vals, vals[1:])] + [vals[0] - lo, hi - vals[-1]]
    return (bool(hits) or len(vals) != count or any(not (lo < x < hi) for x in ins)), hits, min(gaps)


def _band_spacings(lo: int, hi: int) -> int:
    return F8_LEVELS_MICRO.index(hi) - F8_LEVELS_MICRO.index(lo)


def collision_audit() -> CollisionAudit:
    """The reachable surface decides `proven`; the full pair × count superset is the conservative audit. On the F8 grid
    candidates collide with pass-1 levels at every band width that is a multiple of 3 spacings (Appendix A), so the
    fallback branch is live."""
    verify_frozen_identity()
    reach = reachable_router_cases()
    r_bad = 0; example = None; witness: Tuple[str, ...] = (); worst = None; bad_B: set = set()
    for c in reach:
        bad, hits, g = _collides(c.lo_micro, c.hi_micro, c.count)
        worst = g if worst is None else min(worst, g)
        if bad:
            r_bad += 1; bad_B.add(_band_spacings(c.lo_micro, c.hi_micro))
            if example is None:
                example = (c.row, c.lo_micro, c.hi_micro, hits); witness = c.witness_labels
    a_bad = 0; a_cases = 0
    for i in range(len(F8_LEVELS_MICRO)):
        for j in range(i + 1, len(F8_LEVELS_MICRO)):
            for count in (P2R_SINGLE_BAND_INSERTIONS, P2R_PER_INTERVAL_INSERTIONS):
                bad, _, g = _collides(F8_LEVELS_MICRO[i], F8_LEVELS_MICRO[j], count)
                a_cases += 1; a_bad += int(bad); worst = min(worst, g)
    return CollisionAudit(r_bad == 0, len(reach), r_bad, tuple(sorted(bad_B)), a_cases, a_bad, int(worst), r_bad > 0, example, witness)


def routing_slack_table(max_B: int = 9) -> Tuple[int, ...]:
    """Appendix A's Δ_route(B), B = 1..max_B, by its stated procedure: for every band (lo, hi) of B pass-1 spacings, the
    eight round-half-even interior insertions; candidates that collide with a pass-1 level REMOVED; final level set =
    every pass-1 level in the band plus the kept insertions; Δ_route(B) = 2 × the largest final-level gap over all
    bands of that width."""
    verify_frozen_identity()
    out: List[int] = []
    for B in range(1, max_B + 1):
        worst = 0
        for i in range(len(F8_LEVELS_MICRO) - B):
            lo, hi = F8_LEVELS_MICRO[i], F8_LEVELS_MICRO[i + B]
            pass1_in_band = [x for x in F8_LEVELS_MICRO if lo <= x <= hi]
            kept = [x for x in evenly_spaced_interior(lo, hi, P2R_SINGLE_BAND_INSERTIONS) if x not in pass1_in_band]
            final = sorted(set(pass1_in_band) | set(kept))
            worst = max(worst, max(b - a for a, b in zip(final, final[1:])))
        out.append(2 * worst)
    return tuple(out)


def routing_slack_max_B_le_4() -> int:
    return max(routing_slack_table(4))


def verify_against_appendix_a(appendix_a_path: str) -> Dict[str, object]:
    """Bind M4 to the object of record: the committed Appendix A's Δ_route table and collision statement must equal
    what this module's arithmetic produces."""
    raw = open(appendix_a_path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != C.F8_APPENDIX_A_SHA256:
        raise VerdictDomainError(f"APPENDIX_A_OF_RECORD.md identity {sha[:16]} is not the frozen {C.F8_APPENDIX_A_SHA256[:16]}")
    j = json.loads(re.search(r"```json\n(.*?)```", raw.decode("utf-8"), re.S).group(1))
    dr = j["delta_route"]
    table = tuple(int(dr[str(B)] if isinstance(dr, dict) else dr[B - 1]) for B in range(1, 10))
    ours = routing_slack_table(9)
    if table != ours or table != APPENDIX_A_DELTA_ROUTE:
        raise VerdictDomainError(f"Appendix A Δ_route {table} differs from M4's {ours} or the literal")
    if int(j["Delta_route_B4"]) != APPENDIX_A_DELTA_ROUTE_B4 or int(j["Delta_route_max_B_le_4"]) != routing_slack_max_B_le_4():
        raise VerdictDomainError("Appendix A Δ_route(4) / max over B ≤ 4 differ from M4")
    cb = tuple(int(x) for x in j["collision_B"])
    if cb != APPENDIX_A_COLLISION_B or cb != collision_audit().colliding_band_spacings:
        raise VerdictDomainError(f"Appendix A collision bands {cb} differ from M4's audit")
    return {"appendix_a_sha256": sha, "delta_route": ours, "collision_B": cb}


# ----------------------------------------------------------------------------- archetype reproduction (pass-1 sequences, 24 levels)
ARCHETYPE_SEQUENCES: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("gentle_onset", ("N",) * 8 + ("M", "U") + ("S",) * 14),                 # band 3 spacings = W_res exactly: LOCATED (not >)
    ("abrupt_onset", ("N",) * 12 + ("S",) * 12),
    ("persistent_nonstationary_high_m", ("N",) * 10 + ("M",) + ("S",) * 13),
    ("nonmonotone_amplitude", ("N",) * 9 + ("U",) + ("S",) * 14),
    ("no_sustained_anywhere", ("N",) * 24),
    ("no_null_consistent_anywhere", ("S",) * 24),
    ("two_resolved_crossings", ("N",) * 6 + ("S",) * 6 + ("N",) * 6 + ("S",) * 6),
    ("reentrant", ("N",) * 8 + ("S",) * 8 + ("N",) * 8),
    ("off_band_mixture", ("N",) * 4 + ("M",) + ("N",) * 5 + ("S",) * 14),
    ("off_band_unresolved", ("N",) * 8 + ("S",) * 2 + ("U", "U") + ("S",) * 12),
    ("wide_mixed_boundary", ("N",) * 8 + ("M",) * 5 + ("S",) * 11),           # band 6 spacings > W_res
    ("unresolved_heavy_boundary", ("N",) * 8 + ("U",) * 4 + ("S",) * 12),     # band 5 spacings > W_res
)


def reproduce_archetype_table() -> Tuple[Tuple[str, str, Optional[str], str, Optional[str], bool], ...]:
    verify_frozen_identity()
    seqs = dict(ARCHETYPE_SEQUENCES)
    if tuple(a for a, _, _ in ARCHETYPE_TABLE) != tuple(seqs):
        raise VerdictDomainError("archetype sequence set differs from the frozen table's archetypes")
    out = []
    for name, want_v, want_c in ARCHETYPE_TABLE:
        lab = seqs[name]
        if len(lab) != len(F8_LEVELS_MICRO):
            raise VerdictDomainError(f"archetype {name}: sequence length differs from the frozen pass-1 grid")
        v = evaluate(lab, F8_LEVELS_MICRO)
        out.append((name, want_v, want_c, v.verdict, v.cause, v.verdict == want_v and v.cause == want_c))
    return tuple(out)
