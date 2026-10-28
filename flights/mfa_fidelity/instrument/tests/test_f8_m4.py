"""tests/test_f8_m4.py — Flight 8 module M4: the verdict function is total and agrees with an INDEPENDENT reference
transcription of the contract's rules on every label sequence of a 7-level sub-grid (4^7 = 16,384) and on the F8
archetypes; rule 4c is the W_res width form (strict >, physical units, final level set), never a level count; the router
rows, insertion arithmetic and fallback carry verbatim from E1 (checked against E1's own module on E1's grid); the
collision audit and Δ_route table reproduce APPENDIX_A_OF_RECORD.md; nothing in e1 is touched."""
import itertools
import os
import dataclasses
import pytest

from mfa_instrument.f8 import config as C
from mfa_instrument.f8 import verdict as V
from mfa_instrument.e1 import verdict as EV
from mfa_instrument.e1 import config as E1C

HERE = os.path.dirname(os.path.abspath(__file__))
APPENDIX_A = os.path.normpath(os.path.join(HERE, "..", "..", "contracts", "flight8", "APPENDIX_A_OF_RECORD.md"))
L = C.F8_LEVELS_MICRO
SUB = L[6:13]                                      # a 7-level sub-grid straddling m = 1 (0.837 … 1.424)


def reference(labels, levels):
    """Independent transcription of contract §4.4 (rules 1–3, 4a, 4b verbatim from E1; 4c = width > W_res)."""
    n = [i for i, x in enumerate(labels) if x == "N"]; s = [i for i, x in enumerate(labels) if x == "S"]
    if n and s and min(s) < max(n): return ("NOT_PRODUCED", "order_violation", "1")
    if not n: return ("NOT_PRODUCED", "no_null_consistent_phase", "2") if labels[0] == "S" else ("NOT_DISTINGUISHED", "bottom_uncertainty", "2")
    if not s: return ("NOT_PRODUCED", "no_sustained_phase", "3") if labels[-1] == "N" else ("NOT_DISTINGUISHED", "top_uncertainty", "3")
    lo, hi = max(n), min(s)
    outside = [i for i in range(len(labels)) if not (lo < i < hi)]
    if any(labels[i] == "M" for i in outside): return ("NOT_DISTINGUISHED", "off_boundary_mixture", "4a")
    u = [i for i in outside if labels[i] == "U"]
    if len(u) > 2 or any(b - a == 1 for a, b in zip(u, u[1:])): return ("NOT_DISTINGUISHED", "off_boundary_unresolved", "4b")
    if levels[hi] - levels[lo] > 293478: return ("NOT_DISTINGUISHED", "boundary_unresolved_at_W_res", "4c")
    return ("LOCATED", None, "4d")


# ======================= identity =======================
def test_frozen_identity_and_carried_values():
    V.verify_frozen_identity()
    assert V.W_RES_MICRO == 293478 == 3 * C.S_P1_MICRO and V.OFF_BAND_U_ALLOWANCE == 2 and (V.P2R_SINGLE_BAND_INSERTIONS, V.P2R_PER_INTERVAL_INSERTIONS) == (8, 4)
    assert dict(V.VERDICT_DECLARATION)["rule_4c_form"] == "measured_band_width_exceeds_W_res" and "boundary_unresolved_at_W_res" in V.ND_CAUSES
    assert not hasattr(V, "BOUNDARY_SPAN_LIMIT")                                                    # E1's count-based 4c is not carried

@pytest.mark.parametrize("name,bad", [("VERDICT_DECLARATION_SHA256_LITERAL", "0" * 64), ("ARCHETYPE_TABLE_SHA256_LITERAL", "0" * 64),
                                      ("W_RES_MICRO", 293479), ("OFF_BAND_U_ALLOWANCE", 3), ("P2R_SINGLE_BAND_INSERTIONS", 7)])
def test_tamper_is_caught(monkeypatch, name, bad):
    monkeypatch.setattr(V, name, bad)
    with pytest.raises(V.VerdictDomainError): V.evaluate(("N",) * 24, L)


# ======================= totality and agreement with the reference =======================
def test_verdict_function_total_and_equal_to_reference_on_all_4_to_the_7_sequences():
    rules = set(); counts = {}
    for lab in itertools.product(V.LEVEL_LABELS, repeat=7):
        v = V.evaluate(lab, SUB); ref = reference(lab, SUB)
        assert (v.verdict, v.cause, v.rule) == ref, (lab, v, ref)
        rules.add(v.rule); counts[v.rule] = counts.get(v.rule, 0) + 1
        assert (v.bracket_micro is not None) == (v.verdict == "LOCATED")
        if v.verdict == "LOCATED":
            assert v.bracket_micro[1] - v.bracket_micro[0] <= V.W_RES_MICRO and dict(v.evidence)["measured_width_micro"] == v.bracket_micro[1] - v.bracket_micro[0]
    assert rules == set(V.RULES)                                                                    # every rule fires somewhere

def test_rule_4c_is_width_in_physical_units_on_the_given_level_set_strictly_greater():
    # pass-1 grid: band of exactly 3 spacings (= W_res) is LOCATED; 4 spacings is unresolved
    lab3 = ("N",) * 8 + ("U", "U") + ("S",) * 14; lab4 = ("N",) * 8 + ("U",) * 3 + ("S",) * 13
    v3, v4 = V.evaluate(lab3, L), V.evaluate(lab4, L)
    assert v3.rule == "4d" and V.measured_band_width_micro(lab3, L) == L[10] - L[7] == 293478
    assert v4.rule == "4c" and dict(v4.evidence)["measured_width_micro"] == L[11] - L[7] > 293478
    # the SAME label pattern on a denser (final) level set narrows the band below W_res -> LOCATED: width, not count
    d = V.route(lab4, L); final = V.final_level_set(L, d)
    assert d.row == "P2R-5" and len(final) == 24 + len(d.insertions_micro)
    # after pass 2 suppose the inserted levels resolve all but the two innermost: width = one inserted gap pair < W_res
    lo, hi = L[7], L[11]; ins = d.insertions_micro
    labels_final = []
    for x in final:
        if x <= ins[2]: labels_final.append("N")
        elif x >= ins[5]: labels_final.append("S")
        else: labels_final.append("U")
    vf = V.evaluate(labels_final, final)
    assert vf.rule == "4d" and vf.bracket_micro == (ins[2], ins[5]) and ins[5] - ins[2] < V.W_RES_MICRO
    # the interior still holds 3 uncertain levels (two insertions straddle a pass-1 level), the number E1's 4c counted
    # against its limit; here only the width (one insertion gap pair < W_res) decides: LOCATED
    assert sum(1 for x in labels_final if x == "U") == 3 and len([x for x in final if ins[2] < x < ins[5]]) == 3

def test_no_shape_criterion_exists():
    import inspect
    src = inspect.getsource(V.evaluate)
    for word in ("slope", "jump", "monoton", "amplitude", "separation"):
        assert word not in src.lower()


# ======================= router carried verbatim =======================
def test_router_rows_and_fallback_equal_e1_on_e1_grid_patterns():
    """Feed identical label patterns to E1's router on E1's grid and F8's router on F8's grid: rows, interval indices
    and relative insertion positions agree; the arithmetic helpers are identical functions."""
    for a, b in [(3, 7), (7, 10), (10, 11), (5, 14), (0, 23), (11, 12), (2, 5), (8, 20)]:
        lab = ["U"] * 24
        for k in range(a + 1): lab[k] = "N"
        for k in range(b, 24): lab[k] = "S"
        de, df = EV.route(tuple(lab), E1C.E1_LEVELS_MICRO), V.route(tuple(lab), L)
        assert de.row == df.row and len(de.intervals_micro) == len(df.intervals_micro)
        for (lo_e, hi_e), (lo_f, hi_f) in zip(de.intervals_micro, df.intervals_micro):
            assert E1C.E1_LEVELS_MICRO.index(lo_e) == L.index(lo_f) and E1C.E1_LEVELS_MICRO.index(hi_e) == L.index(hi_f)
    for num, den in [(7, 2), (9, 2), (10, 4), (-7, 2), (123456789, 7)]:
        assert V.round_half_to_even_div(num, den) == EV.round_half_to_even_div(num, den)
    assert V.evenly_spaced_interior(250000, 543478, 8) == EV.evenly_spaced_interior(250000, 543478, 8)
    assert V._resolve_collisions([5, 10, 15], [10], [(0, 20)]) == EV._resolve_collisions([5, 10, 15], [10], [(0, 20)])

def test_router_precedence_and_dead_rows():
    n = 24
    assert V.route(("N",) * n, L).row == "P2R-1" and V.route(("U",) * n, L).row == "P2R-1"
    assert V.route(("N",) * 6 + ("S",) * 6 + ("N",) * 6 + ("S",) * 6, L).row == "P2R-2"
    d = V.route(("N",) * 11 + ("S",) * 13, L)
    assert d.row == "P2R-6" and len(d.insertions_micro) == 8 and all(L[10] < x < L[11] for x in d.insertions_micro)
    d5 = V.route(("N",) * 8 + ("U",) * 3 + ("S",) * 13, L)
    assert d5.row == "P2R-5" and len(d5.insertions_micro) == 8 and d5.fallback_moves == () and d5.fallback_drops == ()
    rows = {V.route(c.witness_labels, L).row for c in V.reachable_router_cases()}
    assert rows <= {"P2R-5", "P2R-6"} and set(V.dead_rows()) == {"P2R-3", "P2R-4", "P2R-7"}

def test_collision_fallback_is_live_on_the_f8_grid_and_recorded():
    lab = ["U"] * 24
    for k in range(1): lab[k] = "N"
    for k in range(3, 24): lab[k] = "S"                      # band 250000 -> 543478 (B = 3): two candidates collide
    d = V.route(tuple(lab), L)
    assert d.row == "P2R-5" and d.fallback_moves and not set(d.insertions_micro) & set(L) and len(d.insertions_micro) == 8
    assert all(L[0] < x < L[3] for x in d.insertions_micro) and len(set(d.insertions_micro)) == 8
    for nominal, moved in d.fallback_moves:
        assert nominal in L and moved not in L


# ======================= Appendix A reproduction =======================
def test_routing_slack_table_and_collision_bands_equal_appendix_a_literals():
    assert V.routing_slack_table(9) == V.APPENDIX_A_DELTA_ROUTE and V.routing_slack_max_B_le_4() == 86958
    a = V.collision_audit()
    assert not a.proven and a.fallback_reachable and a.reachable_cases_checked == 276 and a.colliding_band_spacings == (3, 6, 9, 12, 15, 18, 21)
    assert a.example_collision is not None and a.example_collision[0] == "P2R-5"

@pytest.mark.skipif(not os.path.isfile(APPENDIX_A), reason="repository contracts directory not present")
def test_m4_binds_to_appendix_a_of_record():
    out = V.verify_against_appendix_a(APPENDIX_A)
    assert out["appendix_a_sha256"] == C.F8_APPENDIX_A_SHA256 and out["delta_route"][3] == 86958


# ======================= archetypes and domain =======================
def test_archetype_table_reproduces_and_width_edges():
    rep = V.reproduce_archetype_table()
    assert len(rep) == 12 and all(ok for *_, ok in rep)
    assert {n for n, *_ in rep} == {n for n, *_ in V.ARCHETYPE_TABLE}
    gentle = dict(V.ARCHETYPE_SEQUENCES)["gentle_onset"]
    assert V.measured_band_width_micro(gentle, L) == V.W_RES_MICRO                                   # exactly W_res: LOCATED

def test_domain_refusals():
    with pytest.raises(V.VerdictDomainError): V.evaluate(("N",) * 23, L)
    with pytest.raises(V.VerdictDomainError): V.evaluate(("N",) * 23 + ("X",), L)
    with pytest.raises(V.VerdictDomainError): V.evaluate(("N",) * 24, L[::-1])
    with pytest.raises(V.VerdictDomainError): V.evaluate(("N", "S"), (240000, 300000))
    with pytest.raises(V.VerdictDomainError): V.evaluate(("N", "S"), (300000, 300000))
    with pytest.raises(V.VerdictDomainError): V.evenly_spaced_interior(5, 5, 8)
    with pytest.raises(V.VerdictDomainError): V.evenly_spaced_interior(0, 10, 0)

def test_f8_m4_does_not_touch_e1():
    EV.verify_frozen_identity()
    assert EV.VERDICT_DECLARATION_SHA256_LITERAL == "16e2e1e0a7cc9afa601cf77a7886887cafba05b082c3627a3bf0c041eb9bd0d1" and EV.BOUNDARY_SPAN_LIMIT == 3
