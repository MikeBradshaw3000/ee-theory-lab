"""tests/test_e1_m4.py — E1 stage-1 module M4: the total verdict function and the P2R router.

The verdict function is verified EXHAUSTIVELY over all 4^8 = 65,536 label sequences (exactly one
rule fires; the rules hold as written) and by property sampling at L = 24 and 32; the frozen
archetype table is reproduced row by row; the router's rows are mutually exclusive and precedence
ordered; every insertion is strictly interior, non-duplicating, and computed in exact micro-units;
the collision proof is executed and its counterexample recorded; the frozen fallback is exercised on
a reachable colliding band. The tests verify the contract's written rules — they create nothing."""
from itertools import product
import random
import pytest

from mfa_instrument.e1 import verdict as V
from mfa_instrument.e1.config import E1_LEVELS_MICRO as L


def _levels(n):
    """n ascending admissible micro-levels. For n > 24 the extra levels are INTERIOR insertions between
    frozen pass-1 levels — what pass 2 actually produces — never values beyond the frozen endpoints."""
    if n <= len(L):
        return L[:n]
    extra = n - len(L)
    ins = [V.round_half_to_even_div(L[i] + L[i + 1], 2) for i in range(extra)]
    return tuple(sorted(set(L) | set(ins)))


# ---------------- frozen identity ----------------
def test_frozen_declaration_and_archetype_table():
    V.verify_frozen_identity()
    assert V._digest(V.VERDICT_DECLARATION) == V.VERDICT_DECLARATION_SHA256_LITERAL
    assert V._digest(V.ARCHETYPE_TABLE) == V.ARCHETYPE_TABLE_SHA256_LITERAL
    assert V.OFF_BAND_U_ALLOWANCE == 2 and V.BOUNDARY_SPAN_LIMIT == 3 and V.P2R_SINGLE_BAND_INSERTIONS == 8

def test_declaration_live_drift_refused(monkeypatch):
    monkeypatch.setattr(V, "BOUNDARY_SPAN_LIMIT", 5)
    with pytest.raises(V.VerdictDomainError, match="boundary_span_limit"): V.verify_frozen_identity()
    monkeypatch.undo()
    decl = tuple((k, 5 if k == "boundary_span_limit" else v) for k, v in V.VERDICT_DECLARATION)
    monkeypatch.setattr(V, "VERDICT_DECLARATION", decl); monkeypatch.setattr(V, "VERDICT_DECLARATION_SHA256_LITERAL", V._digest(decl))
    with pytest.raises(V.VerdictDomainError, match="boundary_span_limit"): V.verify_frozen_identity()   # joint tamper still refuses


# ---------------- exhaustive totality ----------------
def test_verdict_function_is_total_and_single_rule_over_all_4_to_the_8():
    """All 65,536 sequences in {S,N,M,U}^8: exactly one verdict, one named rule, and the rule that
    fired is the first applicable rule of the contract's precedence — recomputed here independently."""
    lv = _levels(8); counts = {}
    for lab in product(V.LEVEL_LABELS, repeat=8):
        v = V.evaluate(lab, lv)
        assert v.verdict in V.VERDICTS and v.rule in V.RULES
        assert (v.cause is None) == (v.verdict == "LOCATED")
        assert (v.bracket_micro is not None) == (v.verdict == "LOCATED")
        n = [i for i, x in enumerate(lab) if x == "N"]; s = [i for i, x in enumerate(lab) if x == "S"]
        if n and s and min(s) < max(n):      expected = "1"
        elif not n:                           expected = "2"
        elif not s:                           expected = "3"
        else:
            lo, hi = max(n), min(s)
            out = lambda i: not (lo < i < hi)
            m_out = [i for i, x in enumerate(lab) if x == "M" and out(i)]
            u_out = [i for i, x in enumerate(lab) if x == "U" and out(i)]
            adj = any(b - a == 1 for a, b in zip(sorted(u_out), sorted(u_out)[1:]))
            if m_out: expected = "4a"
            elif len(u_out) > V.OFF_BAND_U_ALLOWANCE or adj: expected = "4b"
            elif hi - lo - 1 > V.BOUNDARY_SPAN_LIMIT: expected = "4c"
            else: expected = "4d"
        assert v.rule == expected, (lab, v.rule, expected)
        counts[v.rule] = counts.get(v.rule, 0) + 1
    assert sum(counts.values()) == 4 ** 8 and set(counts) == set(V.RULES)

@pytest.mark.parametrize("n", [24, 32])
def test_property_sampling_at_production_lengths(n):
    rng = random.Random(20260918 + n); lv = _levels(n)
    for _ in range(4000):
        lab = tuple(rng.choice(V.LEVEL_LABELS) for _ in range(n))
        v = V.evaluate(lab, lv)
        assert v.verdict in V.VERDICTS and v.rule in V.RULES
        if v.verdict == "LOCATED":
            lo, hi = v.bracket_micro
            assert lo < hi and lab[lv.index(lo)] == "N" and lab[lv.index(hi)] == "S"
            assert all(x in V.UNCERTAIN for x in lab[lv.index(lo) + 1:lv.index(hi)])

def test_band_uniqueness_theorem_holds_wherever_order_is_respected():
    lv = _levels(8)
    for lab in product(V.LEVEL_LABELS, repeat=8):
        b = V.band_indices(lab)
        n = [i for i, x in enumerate(lab) if x == "N"]; s = [i for i, x in enumerate(lab) if x == "S"]
        assert (b is not None) == bool(n and s and max(n) < min(s))
        if b: assert b == (max(n), min(s))


# ---------------- named rule behaviours ----------------
def test_rule_1_precedes_everything():
    lv = _levels(6)
    assert V.evaluate(("S", "N", "M", "U", "M", "U"), lv).rule == "1"          # order violation despite off-band M/U
    assert V.evaluate(("S", "N", "S", "N", "S", "N"), lv).cause == "order_violation"

def test_rules_2_and_3_distinguish_affirmative_from_uncertain_boundaries():
    lv = _levels(5)
    assert V.evaluate(("S", "S", "S", "S", "S"), lv).cause == "no_null_consistent_phase"   # bottom confident S
    assert V.evaluate(("M", "S", "S", "S", "S"), lv).cause == "bottom_uncertainty"         # bottom uncertain: never affirmative
    assert V.evaluate(("U", "M", "S", "S", "S"), lv).cause == "bottom_uncertainty"
    assert V.evaluate(("N", "N", "N", "N", "N"), lv).cause == "no_sustained_phase"          # top confident N
    assert V.evaluate(("N", "N", "N", "N", "M"), lv).cause == "top_uncertainty"

def test_rule_4_allowances_at_their_exact_boundaries():
    lv = _levels(10)
    base = ["N", "N", "N", "N", "S", "S", "S", "S", "S", "S"]
    ok = base.copy(); ok[0] = "U"; ok[2] = "U"                       # two isolated, non-adjacent off-band U
    assert V.evaluate(tuple(ok), lv).verdict == "LOCATED"
    three = base.copy(); three[0] = three[2] = "U"; three[6] = "U"   # three: over the allowance
    assert V.evaluate(tuple(three), lv).cause == "off_boundary_unresolved"
    adj = base.copy(); adj[0] = adj[1] = "U"                          # two but adjacent
    assert V.evaluate(tuple(adj), lv).cause == "off_boundary_unresolved"
    m = base.copy(); m[1] = "M"
    assert V.evaluate(tuple(m), lv).cause == "off_boundary_mixture"   # 4a precedes 4b
    span3 = ("N", "U", "U", "U", "S") + ("S",) * 5
    assert V.evaluate(span3, lv).verdict == "LOCATED" and V.evaluate(span3, lv).evidence[1][1] == 3
    span4 = ("N", "U", "U", "U", "U", "S", "S", "S", "S", "S")
    assert V.evaluate(span4, lv).cause == "boundary_unresolved"

def test_located_bracket_is_the_band_closure():
    lv = _levels(6)
    v = V.evaluate(("N", "N", "M", "S", "S", "S"), lv)
    assert v.verdict == "LOCATED" and v.bracket_micro == (lv[1], lv[3]) and v.bracket == ("0.180435", "0.241304")


# ---------------- archetype table ----------------
def test_archetype_table_reproduced_row_by_row():
    rows = V.reproduce_archetype_table()
    assert len(rows) == len(V.ARCHETYPE_TABLE) and all(r[5] for r in rows), [r for r in rows if not r[5]]
    assert {r[3] for r in rows} == set(V.VERDICTS)

def test_archetype_sequences_must_match_the_frozen_grid(monkeypatch):
    seqs = tuple((n, s[:-1]) if n == "gentle_onset" else (n, s) for n, s in V.ARCHETYPE_SEQUENCES)
    monkeypatch.setattr(V, "ARCHETYPE_SEQUENCES", seqs)
    with pytest.raises(V.VerdictDomainError, match="sequence length"): V.reproduce_archetype_table()


# ---------------- router ----------------
def test_router_rows_are_exclusive_and_precedence_ordered():
    lv = _levels(24)
    assert V.route(("N",) * 24, lv).row == "P2R-1"                                   # rule 3 -> no pass 2
    assert V.route(("S",) * 24, lv).row == "P2R-1"                                   # rule 2 -> no pass 2
    assert V.route(("S",) * 12 + ("N",) * 12, lv).row == "P2R-2"                     # order violation
    two = ("N",) * 6 + ("S",) * 6 + ("N",) * 6 + ("S",) * 6
    assert V.evaluate(two, lv).rule == "1" and V.route(two, lv).row == "P2R-2"        # R2 precedes R3/R4
    band_u = ("N",) * 8 + ("U",) * 2 + ("S",) * 14
    d = V.route(band_u, lv); assert d.row == "P2R-5" and len(d.insertions_micro) == 8
    empty = ("N",) * 8 + ("S",) * 16
    d6 = V.route(empty, lv); assert d6.row == "P2R-6" and len(d6.insertions_micro) == 8

def test_insertions_are_strictly_interior_non_duplicating_and_exact():
    lv = _levels(24)
    d = V.route(("N",) * 8 + ("U",) * 2 + ("S",) * 14, lv)
    lo, hi = d.intervals_micro[0]
    assert all(isinstance(x, int) and lo < x < hi for x in d.insertions_micro)
    assert len(set(d.insertions_micro)) == 8 and not (set(d.insertions_micro) & set(lv))
    assert list(d.insertions_micro) == sorted(d.insertions_micro)

def test_round_half_to_even_is_the_frozen_rule():
    assert V.round_half_to_even_div(5, 2) == 2 and V.round_half_to_even_div(7, 2) == 4      # .5 -> even
    assert V.round_half_to_even_div(4, 2) == 2 and V.round_half_to_even_div(5, 3) == 2
    with pytest.raises(V.VerdictDomainError): V.round_half_to_even_div(1, 0)
    with pytest.raises(V.VerdictDomainError): V.evenly_spaced_interior(150000, 150000, 8)
    with pytest.raises(V.VerdictDomainError): V.evenly_spaced_interior(150000, 200000, 0)
    with pytest.raises(V.VerdictDomainError): V.evenly_spaced_interior(150000, 200000, True)


# ---------------- the collision audit, reachability, and the fallback ----------------
def test_collision_audit_does_not_close_on_the_reachable_surface():
    """FINDING OF RECORD: the preferred proof path does NOT close. The counterexample is drawn from the
    MECHANICALLY DERIVED reachable router surface, not the arithmetic superset."""
    a = V.collision_audit()
    assert a.proven is False and a.fallback_reachable is True
    assert a.reachable_colliding > 0 and a.reachable_cases_checked == 276 and a.reachable_colliding == 84
    assert a.arithmetic_cases_checked == 552 and a.arithmetic_colliding == 130 and a.arithmetic_colliding > a.reachable_colliding
    row, lo, hi, hits = a.example_collision
    assert (row, lo, hi, hits) == ("P2R-5", 150000, 241304, (180435,)) and all(lo < h < hi for h in hits)

def test_reported_collision_example_is_in_the_mechanically_reachable_set():
    a = V.collision_audit()
    row, lo, hi, _ = a.example_collision
    cases = {(c.row, c.lo_micro, c.hi_micro) for c in V.reachable_router_cases()}
    assert (row, lo, hi) in cases
    d = V.route(a.example_witness_labels, L)                    # the witness really produces that interval
    assert d.row == row and d.intervals_micro == ((lo, hi),)

def test_reachable_surface_is_derived_from_the_router_and_contains_only_live_rows():
    cases = V.reachable_router_cases()
    assert {c.row for c in cases} == {"P2R-5", "P2R-6"} and len(cases) == 276
    for c in cases:
        d = V.route(c.witness_labels, L)
        assert d.row == c.row and (c.lo_micro, c.hi_micro) in d.intervals_micro
        assert c.count == V.P2R_SINGLE_BAND_INSERTIONS                       # the DECLARED count for the row
        assert 0 < len(d.insertions_micro) <= c.count                        # realized count may be lower — see the yield finding

def test_insertion_yield_finding_of_record():
    """FINDING OF RECORD (routed to L2 and Mike as a contract question): on wide bands, evenly spaced
    candidates can land on EVERY interior pass-1 level, and the frozen fallback then drops those with no
    valid neighbour pair. P2R-5 therefore delivers FEWER than its declared 8 insertions on part of the
    reachable surface. The worst case is the widest band: all 8 candidates collide, 6 are dropped and 2
    move by one micro-unit, yielding 2 refinement levels. This module reports the realized yield; it does
    not silently accept 8 nor manufacture substitutes."""
    yields = {}
    for c in V.reachable_router_cases():
        n = len(V.route(c.witness_labels, L).insertions_micro)
        yields[n] = yields.get(n, 0) + 1
    assert yields == {2: 3, 3: 3, 4: 9, 5: 5, 6: 13, 7: 6, 8: 237}
    assert sum(v for k, v in yields.items() if k < 8) == 39 and yields[8] == 237
    worst = V.route(tuple(["N"] + ["U"] * 8 + ["S"] * 15), L)
    assert worst.intervals_micro == ((150000, 423913),) and len(worst.insertions_micro) == 2
    assert len(worst.fallback_drops) == 6 and worst.fallback_moves == ((332609, 332608), (363043, 363044))
    assert set(V.evenly_spaced_interior(150000, 423913, 8)) == {x for x in L if 150000 < x < 423913}   # every candidate collided

def test_short_yield_bands_are_already_boundary_unresolved_after_pass_2():
    """MITIGATION, established by computation: pass 2 never relabels pass-1 levels, so a band whose
    interior already holds more than BOUNDARY_SPAN_LIMIT uncertain levels is NOT DISTINGUISHED (rule 4c)
    after pass 2 whatever pass 2 inserts. EVERY short-yield band has >= 8 uncertain interior levels.
    Therefore the yield shortfall changes NO verdict: no band that could have been LOCATED loses
    insertions. Reported, not assumed."""
    for c in V.reachable_router_cases():
        d = V.route(c.witness_labels, L)
        interior = len([x for x in L if c.lo_micro < x < c.hi_micro])
        if len(d.insertions_micro) < V.P2R_SINGLE_BAND_INSERTIONS:
            assert interior >= 8 > V.BOUNDARY_SPAN_LIMIT
            # after pass 2 (insertions added as uncertain-or-anything), the pass-1 interior stays uncertain: 4c fires
            # under EVERY pass-2 labelling of the insertions — systematic patterns and 100 random ones — the
            # >= 8 uncertain pass-1 levels remain, and land either inside the band (span > 3 -> 4c) or outside
            # it (> 2 off-band U or an M -> 4a/4b): NOT DISTINGUISHED always. No labelling rescues the band.
            combined_levels = tuple(sorted(set(L) | set(d.insertions_micro)))
            base = {lv: l for lv, l in zip(L, c.witness_labels)}
            rng = random.Random(c.lo_micro * 7 + c.hi_micro)
            patterns = [["S"] * len(d.insertions_micro), ["N"] * len(d.insertions_micro), ["U"] * len(d.insertions_micro),
                        ["N" if k % 2 else "S" for k in range(len(d.insertions_micro))]]
            patterns += [[rng.choice(V.LEVEL_LABELS) for _ in d.insertions_micro] for _ in range(100)]
            for pat in patterns:
                lab = dict(base); lab.update(zip(d.insertions_micro, pat))
                v = V.evaluate(tuple(lab[x] for x in combined_levels), combined_levels)
                assert v.verdict != "LOCATED", (c.lo_micro, c.hi_micro, pat, v)

@pytest.mark.parametrize("row", ["P2R-3", "P2R-4", "P2R-7"])
def test_declared_dead_rows_are_unreachable_over_the_label_grammar(row):
    """Contract-grounded dead rows (v0.4 §5 retains P2R-3/4 'for totality ... unreachable without order
    violation, which R2 precedes'). Asserted, not assumed: no sequence in a large randomized and
    structured search reaches them, and the structural reason holds by construction."""
    assert row in V.dead_rows()
    rng = random.Random(4242)
    for _ in range(20000):
        lab = tuple(rng.choice(V.LEVEL_LABELS) for _ in range(len(L)))
        assert V.route(lab, L).row != row
    # the structural reason, checked directly: two N->S intervals imply a confident order violation
    for _ in range(5000):
        lab = tuple(rng.choice(V.LEVEL_LABELS) for _ in range(len(L)))
        if len(V._adjacency_intervals(lab)) >= 2:
            assert V.evaluate(lab, L).rule == "1" and V.route(lab, L).row == "P2R-2"

def test_fallback_fires_on_the_counterexample_band_with_the_exact_move_chain():
    """The reachable counterexample band (0.150000, 0.241304): N at L[0], uncertain interior, S from
    L[3]. The nominal candidate lands on the pass-1 level 180435 and moves to the round-half-to-even
    midpoint of its accepted neighbours; that moved point is an eligible neighbour for the next
    candidate, which therefore moves in turn. Exact chain asserted."""
    lab = tuple(["N"] + ["U", "U"] + ["S"] * 21)
    d = V.route(lab, L)
    assert d.row == "P2R-5" and d.intervals_micro == ((150000, 241304),)
    assert d.fallback_moves == ((180435, 190580), (190580, 195652))
    assert d.fallback_drops == ()
    assert len(d.insertions_micro) == 8 and len(set(d.insertions_micro)) == 8
    assert not (set(d.insertions_micro) & set(L))
    assert all(150000 < x < 241304 for x in d.insertions_micro) and list(d.insertions_micro) == sorted(d.insertions_micro)
    assert d.insertions_micro == (160145, 170290, 190580, 195652, 200724, 210869, 221014, 231159)

def test_fallback_chain_is_deterministic_across_repeated_calls():
    lab = tuple(["N"] + ["U", "U"] + ["S"] * 21)
    a, b = V.route(lab, L), V.route(lab, L)
    assert a.insertions_micro == b.insertions_micro == (160145, 170290, 190580, 195652, 200724, 210869, 221014, 231159)
    assert a.fallback_moves == b.fallback_moves == ((180435, 190580), (190580, 195652)) and a.fallback_drops == b.fallback_drops == ()

def test_a_non_colliding_reachable_band_records_no_moves():
    lab = tuple(["N"] * 4 + ["U"] * 3 + ["S"] * 17)
    d = V.route(lab, L)
    assert d.intervals_micro == ((241304, 363043),) and d.fallback_moves == () and d.fallback_drops == ()
    assert len(d.insertions_micro) == 8 and not (set(d.insertions_micro) & set(L))

# ---------------- domains ----------------
@pytest.mark.parametrize("bad", [
    lambda: V.evaluate((), ()),
    lambda: V.evaluate(("X",), (150000,)),
    lambda: V.evaluate(("N", "S"), (150000,)),
    lambda: V.evaluate(("N", "S"), (150000, 150000)),
    lambda: V.evaluate(("N", "S"), (241304, 150000)),
    lambda: V.evaluate(("N", "S"), (150000, 900000)),
    lambda: V.evaluate(("N", "S"), (150000, True)),
])
def test_domain_refusals(bad):
    with pytest.raises(V.VerdictDomainError): bad()
