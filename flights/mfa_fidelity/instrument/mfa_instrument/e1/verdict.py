"""mfa_instrument/e1/verdict.py — E1 stage-1 module M4: the TOTAL verdict function and the pass-2
router (Contract E1 v0.4 §5 rebuilt; v0.7 C; v0.8 C/E; design note §2 M4).

THE VERDICT FUNCTION is total over {S, N, M, U}^L by precedence: exactly one rule fires for every
sequence. The rules below are the contract's §5 transcribed; the tests VERIFY them exhaustively and
create nothing.

  rule 1  confident order violation (any confident S strictly below any confident N)
            -> NOT PRODUCED (order violation)
  rule 2  no confident N anywhere:  bottom level confident S -> NOT PRODUCED (no null-consistent phase)
                                    otherwise               -> NOT DISTINGUISHED (bottom uncertainty)
  rule 3  no confident S anywhere:  top level confident N    -> NOT PRODUCED (no sustained phase)
                                    otherwise               -> NOT DISTINGUISHED (top uncertainty)
  rule 4  both confident phases, order respected — the band is the open interval between the highest
          confident N and the lowest confident S, unique by order-respect:
       4a any M outside the band            -> NOT DISTINGUISHED (off-boundary mixture)
       4b U outside the band: at most OFF_BAND_U_ALLOWANCE, isolated and non-adjacent
                                             -> else NOT DISTINGUISHED (off-boundary unresolved)
       4c contiguous uncertain span inside the band > BOUNDARY_SPAN_LIMIT after pass 2
                                             -> NOT DISTINGUISHED (boundary unresolved)
       4d otherwise                          -> LOCATED THRESHOLD, bracket [m₋, m₊]

Precedence is 1 > 2 > 3 > 4, and inside rule 4, a > b > c > d. No jump, slope, monotonicity, or
separation criterion exists anywhere: line, not drama.

THE P2R ROUTER (rows P2R-1 … P2R-7, precedence-ordered, exactly one executes) proposes strictly
interior, non-duplicating insertions. ALL insertion arithmetic is in exact integer micro-units
(k = m × 10⁶) with round-half-to-even applied explicitly; `collision_audit` performs the v0.8 E
attempted proof over BOTH the mechanically derived reachable router surface and the full arithmetic
superset. The preferred proof path does NOT close — a reachable P2R-5 interval collides — so the
frozen deterministic fallback (v0.7 C.2 / v0.8 E) is a live branch, exercised rather than removed.

ROW REACHABILITY, of record: under the frozen precedence, rule 1 -> P2R-2 preempts every sequence with
two or more N->S confident adjacency intervals (such a sequence necessarily has a confident S below a
later confident N), so P2R-3 and P2R-4 are retained-but-dead rows — as the contract itself anticipates
(v0.4 §5: "retained for totality ... unreachable without order violation, which R2 precedes — noted,
harmless"). P2R-7 is likewise dead: any sequence reaching it has both confident phases in order, which
yields the unique band (P2R-5 or P2R-6). This module keeps all seven rows executable and ASSERTS their
dead status by test rather than manufacturing sequences to fire them.

[PROPOSED] values (OFF_BAND_U_ALLOWANCE = 2, BOUNDARY_SPAN_LIMIT = 3, P2R insertion counts) are
carried as the executable definition and ratify only via the M6 morphology audit.
"""
from __future__ import annotations

import hashlib
import types
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

from ..config import MICRO_UNITS
from . import config as _C
from .classify import LEVEL_LABELS
from .config import E1_LEVELS_MICRO, E1_M_MAX_MICRO, E1_M_MIN_MICRO, level_id

CONFIDENT = ("S", "N")
UNCERTAIN = ("M", "U")
OFF_BAND_U_ALLOWANCE = 2                 # [PROPOSED] isolated, non-adjacent
BOUNDARY_SPAN_LIMIT = 3                  # [PROPOSED] contiguous uncertain span inside the band, after pass 2

VERDICTS = ("NOT_PRODUCED", "NOT_DISTINGUISHED", "LOCATED")
NP_CAUSES = ("order_violation", "no_null_consistent_phase", "no_sustained_phase")
ND_CAUSES = ("bottom_uncertainty", "top_uncertainty", "off_boundary_mixture", "off_boundary_unresolved", "boundary_unresolved")
RULES = ("1", "2", "3", "4a", "4b", "4c", "4d")

P2R_ROWS = ("P2R-1", "P2R-2", "P2R-3", "P2R-4", "P2R-5", "P2R-6", "P2R-7")
P2R_SINGLE_BAND_INSERTIONS = 8           # rows 5 and 6
P2R_PER_INTERVAL_INSERTIONS = 4          # row 4 (two intervals, 4 + 4)

VERDICT_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("labels", LEVEL_LABELS), ("confident", CONFIDENT), ("uncertain", UNCERTAIN),
    ("verdicts", VERDICTS), ("np_causes", NP_CAUSES), ("nd_causes", ND_CAUSES), ("rules", RULES),
    ("off_band_u_allowance", OFF_BAND_U_ALLOWANCE), ("boundary_span_limit", BOUNDARY_SPAN_LIMIT),
    ("p2r_rows", P2R_ROWS), ("p2r_single_band_insertions", P2R_SINGLE_BAND_INSERTIONS),
    ("p2r_per_interval_insertions", P2R_PER_INTERVAL_INSERTIONS),
    ("micro_units", MICRO_UNITS), ("rounding", "round_half_to_even"),
    ("bottom_micro", E1_M_MIN_MICRO), ("top_micro", E1_M_MAX_MICRO),
)
VERDICT_DECLARATION_SHA256_LITERAL = "16e2e1e0a7cc9afa601cf77a7886887cafba05b082c3627a3bf0c041eb9bd0d1"   # established 2026-09-18

# The archetype -> intended-verdict table (v0.4 §7 as amended). Known answers for M6; M4 reproduces
# it from label sequences the table's own descriptions determine.
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
    ("wide_mixed_boundary", "NOT_DISTINGUISHED", "boundary_unresolved"),
    ("unresolved_heavy_boundary", "NOT_DISTINGUISHED", "boundary_unresolved"),
)
ARCHETYPE_TABLE_SHA256_LITERAL = "1eeaabbd5c2a084e6d66f4d80258aa58cd512e13cfd848939c2d0ac22ce67bf1"   # established 2026-09-18


class VerdictDomainError(ValueError):
    """Input outside the verdict function's or router's executable domain."""


def _digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


def verify_frozen_identity() -> None:
    """Fail-closed: M1's identity; the declaration's literal digest; every declared value equal to its
    live global; the archetype table's digest; the label alphabet equal to M2's."""
    _C.verify_frozen_identity()
    if _digest(VERDICT_DECLARATION) != VERDICT_DECLARATION_SHA256_LITERAL:
        raise VerdictDomainError("verdict declaration differs from its frozen literal digest")
    d = dict(VERDICT_DECLARATION)
    live = {"labels": LEVEL_LABELS, "confident": CONFIDENT, "uncertain": UNCERTAIN, "verdicts": VERDICTS,
            "np_causes": NP_CAUSES, "nd_causes": ND_CAUSES, "rules": RULES,
            "off_band_u_allowance": OFF_BAND_U_ALLOWANCE, "boundary_span_limit": BOUNDARY_SPAN_LIMIT,
            "p2r_rows": P2R_ROWS, "p2r_single_band_insertions": P2R_SINGLE_BAND_INSERTIONS,
            "p2r_per_interval_insertions": P2R_PER_INTERVAL_INSERTIONS, "micro_units": MICRO_UNITS,
            "rounding": "round_half_to_even", "bottom_micro": E1_M_MIN_MICRO, "top_micro": E1_M_MAX_MICRO}
    for k, v in live.items():
        if d[k] != v or type(d[k]) is not type(v):
            raise VerdictDomainError(f"verdict declaration field {k} differs from the live global")
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
    if lv[0] < E1_M_MIN_MICRO or lv[-1] > E1_M_MAX_MICRO:
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
    """The band's bounding indices (highest confident N, lowest confident S) when both confident
    phases exist and order is respected; else None. Unique by order-respect."""
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


def evaluate(labels: Sequence[str], levels_micro: Sequence[int]) -> Verdict:
    """The TOTAL verdict function: exactly one rule fires, by the contract's precedence."""
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
    lo, hi = band_indices(lab)                     # highest confident N index, lowest confident S index
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
    span = len(inside)                              # every interior level is uncertain by construction of the band
    if span > BOUNDARY_SPAN_LIMIT:
        return Verdict("NOT_DISTINGUISHED", "boundary_unresolved", "4c", None,
                       (("boundary_span", span), ("limit", BOUNDARY_SPAN_LIMIT),
                        ("band", (level_id(lv[lo]), level_id(lv[hi])))))
    return Verdict("LOCATED", None, "4d", (lv[lo], lv[hi]),
                   (("band_interior_levels", tuple(level_id(lv[i]) for i in inside)), ("boundary_span", span)))


# ----------------------------------------------------------------------------- the P2R router
@dataclass(frozen=True)
class RouterDecision:
    row: str                                   # P2R-1 … P2R-7
    insertions_micro: Tuple[int, ...]          # strictly interior, non-duplicating, ascending
    intervals_micro: Tuple[Tuple[int, int], ...]
    evidence: Tuple[Tuple[str, object], ...] = ()
    fallback_moves: Tuple[Tuple[int, int], ...] = ()      # (nominal, moved) — empty when the proof holds
    fallback_drops: Tuple[int, ...] = ()


def round_half_to_even_div(num: int, den: int) -> int:
    """Exact integer division with round-half-to-even — the frozen rounding rule (v0.8 E)."""
    if den <= 0:
        raise VerdictDomainError("denominator must be positive")
    q, r = divmod(num, den)
    twice = 2 * r
    if twice < den: return q
    if twice > den: return q + 1
    return q if q % 2 == 0 else q + 1


def evenly_spaced_interior(lo_micro: int, hi_micro: int, count: int) -> Tuple[int, ...]:
    """`count` strictly interior points of (lo, hi), evenly spaced in EXACT integer micro-units with
    round-half-to-even: x_j = lo + round((j+1)(hi−lo)/(count+1)), j = 0..count−1 (v0.8 C/E)."""
    if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
        raise VerdictDomainError("count must be an exact positive non-Boolean integer")
    if any(isinstance(x, bool) or not isinstance(x, int) for x in (lo_micro, hi_micro)) or hi_micro <= lo_micro:
        raise VerdictDomainError("interval must be given as exact ascending integer micro-units")
    width = hi_micro - lo_micro
    return tuple(lo_micro + round_half_to_even_div((j + 1) * width, count + 1) for j in range(count))


def _adjacency_intervals(labels: Sequence[str]) -> List[Tuple[int, int]]:
    """Disjoint N→S adjacency intervals: index pairs (i, j) with label N at i, S at j, j > i, and no
    confident label strictly between."""
    out: List[Tuple[int, int]] = []
    conf = [i for i, x in enumerate(labels) if x in CONFIDENT]
    for a, b in zip(conf, conf[1:]):
        if labels[a] == "N" and labels[b] == "S":
            out.append((a, b))
    return out


def route(labels: Sequence[str], levels_micro: Sequence[int]) -> RouterDecision:
    """The pass-2 router: precedence-ordered rows, exactly one executes. Insertions are strictly
    interior to their refinement interval, non-duplicating against pass-1 levels and each other, in
    exact micro-units. COLLISIONS ARE POSSIBLE on the frozen grid (see `collision_audit`); when one
    occurs, the frozen deterministic fallback moves or drops candidates and records every action."""
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
    """The frozen fallback (v0.7 C.2 / v0.8 E), applied only if a collision occurs: candidates in
    ascending nominal order; a colliding candidate is moved to the round-half-to-even midpoint of its
    immediate accepted neighbours WITHIN its own refinement interval; a moved point must remain
    strictly interior to that interval and preserve strict order against all accepted levels, else the
    candidate is dropped. Every move and drop is returned for the run record."""
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


# ----------------------------------------------------------------------------- the collision proof
@dataclass(frozen=True)
class RouterCase:
    row: str
    lo_micro: int
    hi_micro: int
    count: int
    witness_labels: Tuple[str, ...]


def reachable_router_cases() -> Tuple[RouterCase, ...]:
    """MECHANICALLY DERIVED from `route()` itself (L2 M4-P1): for every ordered pair of pass-1 indices
    (i, j), i < j, construct the canonical witness — confident N at and below i, uncertain strictly
    between, confident S at and above j — and ASK THE ROUTER what it does; only what the router
    actually returns enters the set. No 4^24 enumeration is needed: a reachable P2R-5/6 interval is
    bounded by the highest confident N and the lowest confident S with every interior level uncertain,
    which is exactly this family's shape."""
    verify_frozen_identity()
    seen: Dict[Tuple[str, int, int, int], RouterCase] = {}
    n = len(E1_LEVELS_MICRO)
    for i in range(n):
        for j in range(i + 1, n):
            lab = ["U"] * n
            for k in range(0, i + 1): lab[k] = "N"
            for k in range(j, n): lab[k] = "S"
            d = route(tuple(lab), E1_LEVELS_MICRO)
            if not d.insertions_micro:
                continue
            count = P2R_SINGLE_BAND_INSERTIONS if d.row in ("P2R-5", "P2R-6") else P2R_PER_INTERVAL_INSERTIONS
            for (lo, hi) in d.intervals_micro:
                seen.setdefault((d.row, lo, hi, count), RouterCase(d.row, lo, hi, count, tuple(lab)))
    return tuple(seen[k] for k in sorted(seen))


def dead_rows() -> Dict[str, str]:
    """Rows no label sequence can reach under the frozen precedence, with the reason (asserted by test)."""
    return {"P2R-3": "preempted by rule 1 / P2R-2: multiple N->S intervals imply confident order violation",
            "P2R-4": "preempted by rule 1 / P2R-2: two N->S intervals imply confident order violation",
            "P2R-7": "unreachable: order-respected dual-phase sequences always have the unique band (P2R-5/6)"}


@dataclass(frozen=True)
class CollisionAudit:
    proven: bool                                  # does the PREFERRED proof path close on the REACHABLE surface?
    reachable_cases_checked: int
    reachable_colliding: int
    arithmetic_cases_checked: int                 # the full pair x insertion-count superset (includes dead rows)
    arithmetic_colliding: int
    min_gap_micro: int
    fallback_reachable: bool
    example_collision: Optional[Tuple[str, int, int, Tuple[int, ...]]] = None   # FROM THE REACHABLE SET
    example_witness_labels: Tuple[str, ...] = ()


def _collides(lo: int, hi: int, count: int) -> Tuple[bool, Tuple[int, ...], int]:
    ins = evenly_spaced_interior(lo, hi, count)
    interior_levels = {x for x in E1_LEVELS_MICRO if lo < x < hi}
    hits = tuple(sorted(set(ins) & interior_levels))
    vals = sorted(set(ins))
    gaps = [b - a for a, b in zip(vals, vals[1:])] + [vals[0] - lo, hi - vals[-1]]
    return (bool(hits) or len(vals) != count or any(not (lo < x < hi) for x in ins)), hits, min(gaps)


def collision_audit() -> CollisionAudit:
    """The v0.8 E attempted proof over two clearly separated domains (L2 M4-P1): the REACHABLE router
    surface (derived from `route()`), which decides `proven`; and the full arithmetic superset, reported
    as a conservative audit that includes retained-but-dead rows. The counterexample, when the proof
    fails, comes from the REACHABLE set and carries its witness sequence."""
    verify_frozen_identity()
    reach = reachable_router_cases()
    r_bad = 0; example = None; witness: Tuple[str, ...] = (); worst = None
    for c in reach:
        bad, hits, g = _collides(c.lo_micro, c.hi_micro, c.count)
        worst = g if worst is None else min(worst, g)
        if bad:
            r_bad += 1
            if example is None:
                example = (c.row, c.lo_micro, c.hi_micro, hits); witness = c.witness_labels
    a_bad = 0; a_cases = 0
    for i in range(len(E1_LEVELS_MICRO)):
        for j in range(i + 1, len(E1_LEVELS_MICRO)):
            for count in (P2R_SINGLE_BAND_INSERTIONS, P2R_PER_INTERVAL_INSERTIONS):
                bad, _, g = _collides(E1_LEVELS_MICRO[i], E1_LEVELS_MICRO[j], count)
                a_cases += 1; a_bad += int(bad); worst = min(worst, g)
    return CollisionAudit(r_bad == 0, len(reach), r_bad, a_cases, a_bad, int(worst), r_bad > 0, example, witness)


# ----------------------------------------------------------------------------- archetype reproduction
ARCHETYPE_SEQUENCES: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("gentle_onset", ("N",) * 8 + ("M", "U") + ("S",) * 14),
    ("abrupt_onset", ("N",) * 12 + ("S",) * 12),
    ("persistent_nonstationary_high_m", ("N",) * 10 + ("M",) + ("S",) * 13),
    ("nonmonotone_amplitude", ("N",) * 9 + ("U",) + ("S",) * 14),
    ("no_sustained_anywhere", ("N",) * 24),
    ("no_null_consistent_anywhere", ("S",) * 24),
    ("two_resolved_crossings", ("N",) * 6 + ("S",) * 6 + ("N",) * 6 + ("S",) * 6),
    ("reentrant", ("N",) * 8 + ("S",) * 8 + ("N",) * 8),
    ("off_band_mixture", ("N",) * 4 + ("M",) + ("N",) * 5 + ("S",) * 14),
    ("off_band_unresolved", ("N",) * 8 + ("S",) * 2 + ("U", "U") + ("S",) * 12),
    ("wide_mixed_boundary", ("N",) * 8 + ("M",) * 5 + ("S",) * 11),
    ("unresolved_heavy_boundary", ("N",) * 8 + ("U",) * 4 + ("S",) * 12),
)


def reproduce_archetype_table() -> Tuple[Tuple[str, str, Optional[str], str, Optional[str], bool], ...]:
    """Run each declared archetype sequence through the verdict function and compare with the frozen
    table: (archetype, intended verdict, intended cause, observed verdict, observed cause, agrees)."""
    verify_frozen_identity()
    seqs = dict(ARCHETYPE_SEQUENCES)
    if tuple(a for a, _, _ in ARCHETYPE_TABLE) != tuple(seqs):
        raise VerdictDomainError("archetype sequence set differs from the frozen table's archetypes")
    out = []
    for name, want_v, want_c in ARCHETYPE_TABLE:
        lab = seqs[name]
        if len(lab) != len(E1_LEVELS_MICRO):
            raise VerdictDomainError(f"archetype {name}: sequence length differs from the frozen pass-1 grid")
        v = evaluate(lab, E1_LEVELS_MICRO)
        out.append((name, want_v, want_c, v.verdict, v.cause, v.verdict == want_v and v.cause == want_c))
    return tuple(out)
