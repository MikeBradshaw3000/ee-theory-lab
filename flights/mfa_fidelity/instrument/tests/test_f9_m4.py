"""tests/test_f9_m4.py — Flight 9 module M4: the outcome records of contract §5.6 and §7, and the persistence
record of §5.4.

Every input here is a typed label or a count made in the test. Nothing is run and nothing is read. Each rule is
checked against a second implementation written in the test from the contract's sentences, over every case where the
cases can be listed and over many random ones where they cannot, and against the contract's own named cases (§6.1 row
19, §6.2 rows 19 to 23)."""
import hashlib
import itertools
import math
import os
import re

import numpy as np
import pytest

from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import outcomes as O

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "mfa_instrument")
GRID = C.F9_LEVELS_MICRO
RES = ("compatible", "adverse", "unresolved")
RNG = lambda *k: np.random.Generator(np.random.PCG64(np.random.SeedSequence([4, 4, 4] + list(k))))


def _refused(fn, *a, **k):
    try: fn(*a, **k)
    except (C.F9ConfigError, O.F9OutcomeError): return True
    return False


# ======================= declaration and labels =======================
def test_declaration_verifies_and_the_labels_are_the_contracts(monkeypatch):
    assert O.verify_outcome_declaration() == O.OUTCOME_DECLARATION_SHA256_LITERAL == C.frozen_digest(O.OUTCOME_DECLARATION)
    with open(os.path.join(HERE, "..", "..", "contracts", "flight9", "FLIGHT_9_CONTRACT_v0_7.md"), encoding="utf-8") as fh: text = fh.read()
    labels = [O.CAUSE_NO_CONTOUR, O.CAUSE_NO_EDGE, O.CAUSE_UNDER_RESOLVED, O.CAUSE_UNSTABLE, O.CAUSE_FINITE_RESOLUTION, O.CAUSE_OWN_ADVERSE,
              O.CAUSE_INSUFFICIENT, O.CAUSE_ISOLATED, O.B_FOLLOWS_OWN, O.B_OWN_ADVERSE, O.D_RIVAL_EXCLUDED, O.D_RIVAL_NOT_ESTABLISHED, O.D_FOLLOWS_RIVAL,
              O.D_FOLLOWS_NEITHER, O.D_NOT_ADJUDICABLE, O.ARM_NO_DETERMINATION, O.FLIGHT_NO_DETERMINATION, O.PROFILE_NON_MONOTONE, O.PROFILE_ALL,
              O.PROFILE_NONE, O.PROFILE_BOTH, "ADVERSE", "COMPATIBLE", "NOT DISTINGUISHED", "PRODUCED", "NOT PRODUCED", "DISTINGUISHED"]
    for lab in labels: assert lab in text, lab                                # every label is a string of the frozen contract
    assert "apparatus unevaluable (<key>)" in text and O.CAUSE_APPARATUS.format(key="<key>") == "apparatus unevaluable (<key>)"
    monkeypatch.setattr(O, "D_WITNESS_MIN", 2); assert O.verify_outcome_declaration()   # the literal, not the name, is bound:
    monkeypatch.undo()
    monkeypatch.setattr(O, "OUTCOME_DECLARATION", O.OUTCOME_DECLARATION[:-1]); assert _refused(O.verify_outcome_declaration); monkeypatch.undo()
    monkeypatch.setattr(O, "LEVEL_TABLE", O.LEVEL_TABLE[:-1]); assert _refused(O.verify_outcome_declaration); monkeypatch.undo()
    monkeypatch.setattr(O, "OUTCOME_DECLARATION_SHA256_LITERAL", "PLACEHOLDER"); assert _refused(O.verify_outcome_declaration)


# ======================= level =======================
CONTRACT_LEVEL_TABLE = """
compatible | adverse | follows own | rival excluded
compatible | compatible | follows own | not distinguished
compatible | unresolved | follows own | rival not established
adverse | compatible | own adverse | follows rival
adverse | adverse | own adverse | follows neither
adverse | unresolved | own adverse | rival not established
"""


def test_level_table_is_the_contracts_rows():
    """The six explicit rows and the seventh ("unresolved | any | not distinguished | not distinguished"), read here from
    the contract's own table text and compared with the module on TB (separate families)."""
    with open(os.path.join(HERE, "..", "..", "contracts", "flight9", "FLIGHT_9_CONTRACT_v0_7.md"), encoding="utf-8") as fh: text = fh.read()
    rows = [tuple(x.strip() for x in line.strip().strip("|").split("|")) for line in CONTRACT_LEVEL_TABLE.strip().splitlines()]
    for own, rival, b, d in rows:
        assert f"| {own} | {rival} | {b} | {d}" in text                       # the row as the frozen contract prints it
        rec = O.level_tier(own, rival, False)
        assert (rec["b_status"], rec["discrimination"], rec["state"], rec["informative"]) == (b, d, "informative", True)
    assert "| unresolved | any | not distinguished | not distinguished |" in text
    for rival in RES:
        rec = O.level_tier("unresolved", rival, False)
        assert (rec["b_status"], rec["discrimination"]) == ("not distinguished", "not distinguished")
    assert "| compatible | compatible | follows own | not distinguished (same-family terrain: not adjudicable here) |" in text


def test_level_causes_and_kinds():
    for own in RES:
        for rival in RES:
            rec = O.level_tier(own, rival, False)
            want = (["finite resolution"] if "unresolved" in (own, rival) else []) + (["no registered contour of own index within ε"] if own == "adverse" else [])
            assert rec["causes"] == want and rec["own"] == own and rec["rival"] == rival
            assert rec["kind"] == {"adverse": "scientific adverse at the level", "unresolved": "scientific ND", "compatible": None}[own]
    for cause in ("no edge at θ", "under-resolved", "unstable edge"):
        rec = O.level_tier(None, None, False, not_informative_cause=cause)
        assert (rec["state"], rec["kind"], rec["cause"], rec["informative"], rec["b_status"]) == ("not informative", "scientific ND", cause, False, None)
    const = O.level_tier(None, None, False, not_informative_cause="no eligible contour")
    assert (const["state"], const["kind"], const["informative"]) == ("not scored", "unavailable", False)
    app = O.level_apparatus("run 17 missing")
    assert (app["state"], app["kind"], app["cause"], app["informative"]) == ("unevaluable", "apparatus", "apparatus unevaluable (run 17 missing)", False)
    assert _refused(O.level_tier, "compatible", None, False)                  # a result for one index only is not a level


def test_same_family_levels_are_not_adjudicable_and_must_agree():
    for r in RES:
        rec = O.level_tier(r, r, True)
        assert rec["discrimination"] == "not adjudicable here"
        assert rec["b_status"] == {"compatible": "follows own", "adverse": "own adverse", "unresolved": "not distinguished"}[r]
    for own, rival in itertools.permutations(RES, 2): assert _refused(O.level_tier, own, rival, True)
    assert _refused(O.level_tier, "compatible", None, True)
    assert [O.is_same_family(t) for t in C.F9_TERRAINS] == [False, True, False, True, True, True, True, True] and _refused(O.is_same_family, "TZ")


def test_level_inputs_are_checked():
    for bad in (("ok", "adverse", False), ("compatible", "ok", False), ("compatible", "adverse", 1), ("COMPATIBLE", "adverse", False), (None, None, False)):
        assert _refused(O.level_tier, *bad)
    assert _refused(O.level_tier, "compatible", "adverse", False, not_informative_cause="no edge at θ")
    assert _refused(O.level_tier, None, None, False, not_informative_cause="finite resolution")
    assert _refused(O.level_tier, None, None, False, not_informative_cause="no edge at theta")     # the evaluator's spelling is not a contract label
    assert _refused(O.level_apparatus, "") and _refused(O.level_apparatus, None)


def _ev(own, rival, own_cause=None, rival_cause=None):
    """An evaluation record shaped like M3's, for an arm under P (own = P, rival = H)."""
    return {"indices": {"P": {"result": own, "cause": own_cause}, "H": {"result": rival, "cause": rival_cause}}}


def test_level_from_the_evaluators_record():
    for own in RES:
        for rival in RES:
            assert O.level_from_evaluation(_ev(own, rival), "TB", "P") == O.level_tier(own, rival, False)
            swapped = O.level_from_evaluation(_ev(own, rival), "TB", "H")     # the same record read for the H arm: own and rival change places
            assert swapped == O.level_tier(rival, own, False)
        assert O.level_from_evaluation(_ev(own, own), "TA", "P") == O.level_tier(own, own, True)
    for theirs, ours in (("no edge at theta", "no edge at θ"), ("below the informative minimum", "under-resolved"), ("unstable edge", "unstable edge")):
        rec = O.level_from_evaluation(_ev("not informative", "not informative", theirs, theirs), "TC", "H")
        assert rec == O.level_tier(None, None, True, not_informative_cause=ours)
    const = O.level_from_evaluation(_ev("not informative", "not informative", "no eligible contour", "no eligible contour"), "T0", "P")
    assert const["state"] == "not scored"
    for bad in (_ev("not informative", "not informative", "no edge at theta", "unstable edge"),     # one map, two reasons
                _ev("not informative", "compatible", "no edge at theta"), _ev("compatible", "not informative", None, "unstable edge"),
                _ev("not informative", "compatible", "no eligible contour"), _ev("compatible", "not informative", None, "no eligible contour"),
                _ev("not informative", "not informative", "no eligible contour", "no eligible contour"),   # a constant index off T0
                _ev("not informative", "not informative", "new cause", "new cause"), {"indices": {"P": {}}}, {}):
        assert _refused(O.level_from_evaluation, bad, "TB", "P"), bad
    assert _refused(O.level_from_evaluation, _ev("compatible", "adverse"), "TA", "P")             # same family, unequal results
    assert _refused(O.level_from_evaluation, _ev("compatible", "compatible"), "T0", "P")          # T0 scored
    for theirs in ("no edge at theta", "below the informative minimum", "unstable edge", "no eligible contour"):   # L2 precedes L3 to L5 on T0
        t0 = O.level_from_evaluation(_ev("not informative", "not informative", theirs, theirs), "T0", "P")
        assert (t0["state"], t0["cause"]) == ("not scored", "no eligible contour")
    assert _refused(O.level_from_evaluation, _ev("compatible", "compatible"), "T0", "H")          # not an arm


# ======================= arm =======================
STATES = ("F", "A", "U", "N", "X")       # follows own, own adverse, not distinguished (unresolved), not informative, apparatus


def _level(code):
    return {"F": O.level_tier("compatible", "compatible", True), "A": O.level_tier("adverse", "adverse", True), "U": O.level_tier("unresolved", "unresolved", True),
            "N": O.level_tier(None, None, True, not_informative_cause="unstable edge"), "X": O.level_apparatus("fault")}[code]


def _sweep(codes):
    assert len(codes) == 25
    return {k: _level(c) for k, c in zip(GRID, codes)}


def _reference_arm(codes):
    """The arm rule from the contract's sentences, on a string of level codes."""
    if "X" in codes: return "no qualified determination", None
    if "AA" in codes: return "ADVERSE", None                                  # neighbours on the grid, both informative, no level between them
    informative = [c for c in codes if c in "FAU"]
    if len(informative) >= 3 and all(c == "F" for c in informative): return "COMPATIBLE", None
    causes = []
    if len(informative) < 3: causes.append("insufficient informative levels")
    if "A" in codes: causes.append("isolated adverse level")
    if "U" in codes: causes.append("finite resolution")
    return "NOT DISTINGUISHED", causes


def test_arm_rule_on_the_contracts_named_sweeps():
    def arm(codes): return O.arm_tier(_sweep(codes))
    n = "N" * 25
    two_adj = arm(n[:10] + "AA" + n[12:])                                      # exactly two informative levels, adjacent and adverse (§6.1 row 19)
    assert two_adj["determination"] == "ADVERSE" and two_adj["rule"] == "A2" and two_adj["informative_levels"] == [GRID[10], GRID[11]]
    assert two_adj["adjacent_adverse_pairs"] == [[GRID[10], GRID[11]]]
    two_comp = arm(n[:10] + "FF" + n[12:])                                     # two informative compatible levels (§6.1 row 19; §6.2 row 19)
    assert two_comp["determination"] == "NOT DISTINGUISHED" and two_comp["causes"] == ["insufficient informative levels"] and len(two_comp["informative_levels"]) == 2
    coarse = arm("AA" + n[2:])                                                 # 0.75 and 1.00: neighbours on the registered grid though 0.25 apart
    assert coarse["determination"] == "ADVERSE" and coarse["adjacent_adverse_pairs"] == [[750000, 1000000]]
    split = arm(n[:10] + "ANA" + n[13:])                                       # a level between them: not neighbours
    assert split["determination"] == "NOT DISTINGUISHED" and split["causes"] == ["insufficient informative levels", "isolated adverse level"]
    apart = arm("F" * 10 + "AFA" + "F" * 12)
    assert apart["determination"] == "NOT DISTINGUISHED" and apart["causes"] == ["isolated adverse level"] and apart["own_adverse_levels"] == [GRID[10], GRID[12]]
    three = arm(n[:5] + "F" + n[6:12] + "F" + n[13:20] + "F" + n[21:])
    assert three["determination"] == "COMPATIBLE" and three["rule"] == "A3" and three["rests_on_levels"] == [GRID[5], GRID[12], GRID[20]]
    unres = arm("F" * 12 + "U" + "F" * 12)
    assert unres["determination"] == "NOT DISTINGUISHED" and unres["causes"] == ["finite resolution"]
    both = arm("F" * 5 + "A" + "F" * 5 + "U" + "F" * 13)                        # two causes hold: both are recorded, in the contract's listing order
    assert both["causes"] == ["isolated adverse level", "finite resolution"]
    all3 = arm(n[:3] + "A" + n[4:9] + "U" + n[10:])
    assert all3["causes"] == ["insufficient informative levels", "isolated adverse level", "finite resolution"]
    none = arm(n)
    assert none["determination"] == "NOT DISTINGUISHED" and none["causes"] == ["insufficient informative levels"] and none["informative_levels"] == []
    app = arm("F" * 10 + "AA" + "X" + "F" * 12)                                # apparatus precedes the adverse rule
    assert app["determination"] == "no qualified determination" and app["rule"] == "A1" and app["causes"] == ["apparatus unevaluable (fault)"]
    assert arm("F" * 25)["determination"] == "COMPATIBLE" and arm("A" * 25)["determination"] == "ADVERSE"


def test_arm_rule_against_the_reference_on_many_sweeps():
    gen = RNG(1)
    seen = set()
    for trial in range(6000):
        weights = gen.dirichlet(np.ones(5) * gen.choice([0.2, 1.0, 5.0]))
        if trial % 3 == 0: weights[4] = 0.0; weights = weights / weights.sum()   # a third of the sweeps have no apparatus level
        codes = "".join(gen.choice(list(STATES), size=25, p=weights))
        want, causes = _reference_arm(codes)
        got = O.arm_tier(_sweep(codes))
        assert got["determination"] == want, codes
        if causes is not None: assert got["causes"] == causes, codes
        seen.add((want, tuple(causes or ())))
    assert {w for w, _ in seen} == {"no qualified determination", "ADVERSE", "COMPATIBLE", "NOT DISTINGUISHED"}
    assert len({c for w, c in seen if w == "NOT DISTINGUISHED"}) == 7                               # every non-empty set of the three causes occurred


def test_a_missing_level_record_is_an_apparatus_cause():
    full = _sweep("F" * 25)
    short = dict(full); del short[GRID[7]]
    none = dict(full); none[GRID[7]] = None
    for levels in (short, none):
        rec = O.arm_tier(levels)
        assert rec["determination"] == "no qualified determination" and rec["unevaluable_levels"] == [GRID[7]]
        assert rec["causes"] == ["apparatus unevaluable (missing level record)"]
    assert O.arm_tier({})["determination"] == "no qualified determination"
    for bad in ({1025000: _level("F")}, {"1000000": _level("F")}, {GRID[0]: {"state": "informative"}}, {GRID[0]: "F"}, [_level("F")] * 25,
                {GRID[0]: dict(_level("F"), informative=False)}, {GRID[0]: dict(_level("F"), b_status="ok")}):
        assert _refused(O.arm_tier, bad)


def test_a_level_record_that_contradicts_itself_is_refused():
    """A level record is accepted only if it is exactly what the level rule returns for its own contents."""
    good = {c: _level(c) for c in STATES}
    for rec in good.values(): assert O._check_level(rec) is rec
    tb = O.level_tier("compatible", "adverse", False)
    forged = [
        dict(good["A"], b_status="follows own"),                              # own adverse relabelled as following
        dict(good["U"], b_status="follows own"),
        dict(tb, discrimination="rival excluded", rival="compatible"),         # a witness without an adverse rival
        dict(tb, discrimination="not adjudicable here"),                       # same-family status with unequal results
        dict(good["F"], causes=["finite resolution"]), dict(good["A"], causes=[]), dict(good["A"], kind=None),
        dict(good["N"], state="informative"), dict(good["N"], cause="finite resolution"), dict(good["N"], own="compatible"),
        dict(good["X"], cause="apparatus unevaluable ()"), dict(good["X"], cause="fault"), dict(good["X"], state="not informative"),
        dict(good["F"], informative=1), dict(good["F"], extra=1), {k: v for k, v in good["F"].items() if k != "causes"},
    ]
    for rec in forged:
        assert _refused(O._check_level, rec), rec
        assert _refused(O.arm_tier, {GRID[0]: rec}), rec


EXPECTED_REFUSED = 367     # 17 genuine arms x 23 changes, less the changes that do not apply to an arm or are no change for it (counted, not assumed)


def _genuine_arms():
    """Genuine arm shapes: each rule, five of the seven sets of A4 causes (each cause alone, `isolated adverse level`
    with `finite resolution`, and all three; the two pairs that join `insufficient informative levels` with one other
    cause are not here and occur in the 6,000-sweep test), and the level shapes L2 named (follows own with the rival
    unresolved; own adverse with the rival unresolved), on TB so that the rival can differ."""
    n = "N" * 25
    def tb(codes): return O.arm_tier(_tb(codes))
    return {
        "A1": O.arm_tier(_sweep("X" + "F" * 24)), "A1 missing": O.arm_tier({k: _level("F") for k in GRID[1:]}), "A1 all": O.arm_tier({}),
        "A2": O.arm_tier(_sweep("F" * 10 + "AA" + "F" * 13)), "A3": O.arm_tier(_sweep("F" * 25)), "A3 three": O.arm_tier(_sweep(n[:5] + "F" + n[6:12] + "F" + n[13:20] + "F" + n[21:])),
        "A4 insufficient": O.arm_tier(_sweep(n[:10] + "FF" + n[12:])), "A4 isolated": O.arm_tier(_sweep("F" * 10 + "AFA" + "F" * 12)),
        "A4 finite": O.arm_tier(_sweep("F" * 12 + "U" + "F" * 12)), "A4 isolated+finite": O.arm_tier(_sweep("F" * 5 + "A" + "F" * 5 + "U" + "F" * 13)),
        "A4 all three": O.arm_tier(_sweep(n[:3] + "A" + n[4:9] + "U" + n[10:])), "A4 none informative": O.arm_tier(_sweep(n)),
        "TB follows own, rival unresolved": tb("E" * 25), "TB own adverse, rival unresolved": tb("F" * 6 + "G" + "F" * 18),
        "TB witnesses": tb("W" * 25), "TB follows rival": tb("R" * 25), "TB mixed": tb("WWW" + "B" + n[4:10] + "G" + "E" + n[12:]),
    }


def test_genuine_arm_records_are_accepted():
    arms = _genuine_arms()
    assert {a["rule"] for a in arms.values()} == {"A1", "A2", "A3", "A4"}
    assert arms["TB follows own, rival unresolved"]["determination"] == "COMPATIBLE"
    assert arms["TB follows own, rival unresolved"]["level_causes"][GRID[0]] == ["finite resolution"]      # a follows-own level may carry it
    assert arms["TB own adverse, rival unresolved"]["level_causes"][GRID[6]] == ["finite resolution", "no registered contour of own index within ε"]
    assert arms["A1 missing"]["causes"] == ["apparatus unevaluable (missing level record)"] and arms["A1 all"]["unevaluable_levels"] == list(GRID)
    for name, rec in arms.items():
        assert O._check_arm(rec) is rec, name
        assert sorted(rec["levels"]) == sorted(GRID) and O.arm_tier(rec["levels"]) == rec, name            # an arm is a function of the levels it carries
        slot = {t: arms["A3"] for t in C.F9_REQUIRED_TERRAINS}; slot["TB"] = rec
        O.flight_b("P", slot, True)                                                                         # and passes the public boundary


def _mutations(rec):
    """Changes to a genuine arm record, each of which makes it a record `arm_tier` cannot return."""
    import copy
    k0, k1 = GRID[0], GRID[1]
    def m(fn):
        r = copy.deepcopy(rec); fn(r); return r
    out = {
        # L2 M4 round 1, D1, the six reproduced cases
        "apparatus level cause": m(lambda r: r["level_causes"].__setitem__(k0, ["apparatus unevaluable (missing level record)"])),
        "apparatus arm cause": m(lambda r: r.__setitem__("causes", r["causes"] + ["apparatus unevaluable (missing level record)"])),
        "own-adverse level cause": m(lambda r: r["level_causes"].__setitem__(k0, ["no registered contour of own index within ε"])),
        "level_causes deleted": m(lambda r: r.pop("level_causes")),
        "level_causes not a mapping": m(lambda r: r.__setitem__("level_causes", 1)),
        "both cause structures erased": m(lambda r: (r.__setitem__("causes", []), r.__setitem__("level_causes", {}))) if (rec["causes"] or rec["level_causes"]) else None,
        # the same kind, on every other field
        "levels deleted": m(lambda r: r.pop("levels")), "levels not a mapping": m(lambda r: r.__setitem__("levels", list(r["levels"].values()))),
        "a level record missing": m(lambda r: r["levels"].pop(k1)), "a level record None": m(lambda r: r["levels"].__setitem__(k1, None)),
        "a level keyed by text": m(lambda r: r["levels"].__setitem__(str(k1), r["levels"].pop(k1))),
        "a level record replaced": m(lambda r: r["levels"].__setitem__(k1, _level("A" if rec["levels"][k1].get("b_status") != "own adverse" else "F"))),
        "a level record forged": m(lambda r: r["levels"][k1].__setitem__("informative", not r["levels"][k1]["informative"])),
        "an extra field": m(lambda r: r.__setitem__("note", "x")), "rule changed": m(lambda r: r.__setitem__("rule", "A3" if r["rule"] != "A3" else "A4")),
        "determination changed": m(lambda r: r.__setitem__("determination", "COMPATIBLE" if r["determination"] != "COMPATIBLE" else "ADVERSE")),
        "informative list shortened": m(lambda r: r["informative_levels"].pop()) if rec["informative_levels"] else None,
        "a list made a tuple": m(lambda r: r.__setitem__("follows_own_levels", tuple(r["follows_own_levels"]))),
        "a level made a float": m(lambda r: r["informative_levels"].__setitem__(0, float(r["informative_levels"][0]))) if rec["informative_levels"] else None,
        "causes made a tuple": m(lambda r: r.__setitem__("causes", tuple(r["causes"]))),
        "pairs emptied": m(lambda r: r.__setitem__("adjacent_adverse_pairs", [])) if rec["adjacent_adverse_pairs"] else None,
        "a pair added": m(lambda r: r["adjacent_adverse_pairs"].append([k0, k1])),
        "rests_on changed": m(lambda r: r.__setitem__("rests_on_levels", r["rests_on_levels"][:-1])) if "rests_on_levels" in rec else m(lambda r: r.__setitem__("rests_on_levels", [])),
    }
    return {k: v for k, v in out.items() if v is not None}


def test_an_arm_record_that_contradicts_itself_is_refused_l2_m4_round1_d1():
    """L2 M4 round 1, D1: an arm record is accepted only if recomputing the arm from the level records it carries gives
    back the whole record. L2's six cases and the same kind of change to every other field are refused, at `_check_arm`
    and through the public `flight_b` boundary, for every genuine arm shape."""
    arms = _genuine_arms()
    good = {t: arms["A3"] for t in C.F9_REQUIRED_TERRAINS}
    assert O.flight_b("P", good, True)["B"] == "PRODUCED"
    refused = 0
    for name, rec in arms.items():
        for what, bad in _mutations(rec).items():
            if repr(bad) == repr(rec): continue                               # the change is no change for this arm (e.g. the cause is already there)
            assert _refused(O._check_arm, bad), (name, what)
            assert _refused(O.flight_b, "P", dict(good, TB=bad), True), (name, what)
            refused += 1
    assert refused == EXPECTED_REFUSED, refused
    # L2's first case exactly: a COMPATIBLE arm whose first level is said to be apparatus-unevaluable can no longer give PRODUCED
    import copy
    bad = copy.deepcopy(arms["A3"]); bad["level_causes"][GRID[0]] = ["apparatus unevaluable (missing level record)"]
    assert GRID[0] in bad["informative_levels"] and bad["determination"] == "COMPATIBLE" and _refused(O.flight_b, "P", dict(good, TA=bad), True)
    mixed = copy.deepcopy(arms["A3"]); mixed["levels"][GRID[2]] = {1: 2, "state": "informative"}            # keys of two types: refused, typed
    assert _refused(O._check_arm, mixed) and _refused(O._check_level, {1: 2, "a": 3})
    for junk in ({"determination": "COMPATIBLE"}, {"determination": "ok"}, {}, None, "COMPATIBLE", dict(arms["A3"], levels={})):
        if junk is None: continue                                             # None is a missing arm: `no qualified scientific determination`, tested elsewhere
        assert _refused(O._check_arm, junk) and _refused(O.flight_b, "P", dict(good, TA=junk), True)


# ======================= flight =======================
def _arm_record(det):
    codes = {"C": "F" * 25, "A": "A" * 25, "N": "N" * 25, "X": "X" + "F" * 24}[det]
    return O.arm_tier(_sweep(codes))


def test_flight_b_over_every_combination_of_seven_arms():
    """4^7 combinations of arm determinations, with and without qualification, against the table of §5.6."""
    recs = {d: _arm_record(d) for d in "CANX"}
    count = {}
    for combo in itertools.product("CANX", repeat=7):
        arms = {t: recs[d] for t, d in zip(C.F9_REQUIRED_TERRAINS, combo)}
        for qual in (True, False):
            got = O.flight_b("P", arms, qual)["B"]
            if not qual or "X" in combo: want = "no qualified scientific determination"
            elif "A" in combo: want = "NOT PRODUCED"
            elif "N" in combo: want = "NOT DISTINGUISHED"
            else: want = "PRODUCED"
            assert got == want, (combo, qual)
            count[want] = count.get(want, 0) + 1
    assert sum(count.values()) == 2 * 4 ** 7 and count["PRODUCED"] == 1 and count["NOT PRODUCED"] == 3 ** 7 - 2 ** 7 and count["NOT DISTINGUISHED"] == 2 ** 7 - 1


def test_flight_b_records_and_missing_inputs():
    recs = {d: _arm_record(d) for d in "CANX"}
    all_c = {t: recs["C"] for t in C.F9_REQUIRED_TERRAINS}
    prod = O.flight_b("H", all_c, True)                                       # §6.2 row 20
    assert prod["B"] == "PRODUCED" and prod["composition"] == "H" and set(prod["domain"]) == set(C.F9_REQUIRED_TERRAINS)
    assert prod["domain"]["TA"] == list(GRID) and prod["resolution"] == {"theta_micro": 200000, "epsilon_micro": 2000000, "component_min_bonds": 40, "grid": 100, "n_seeds": 40, "tail_ticks": 1000}
    for slot in C.F9_REQUIRED_TERRAINS:                                       # §6.2 row 21: one adverse slot, six compatible
        one = dict(all_c); one[slot] = recs["A"]
        r = O.flight_b("P", one, True)
        assert r["B"] == "NOT PRODUCED" and r["adverse_arms"] == [slot] and r["reasons"] == [f"ADVERSE: {slot}"]
    nd = dict(all_c); nd["TC"] = recs["N"]
    assert O.flight_b("P", nd, True)["B"] == "NOT DISTINGUISHED"              # a required arm that lacks information stays in the conjunction
    short = dict(all_c); del short["TD-4-4"]
    none = dict(all_c); none["TD-4-4"] = None
    for arms in (short, none, {}):
        r = O.flight_b("P", arms, True)
        assert r["B"] == "no qualified scientific determination" and "TD-4-4" in r["missing_arms"]
    adverse_and_missing = dict(all_c); adverse_and_missing["TA"] = recs["A"]; del adverse_and_missing["TB"]
    assert O.flight_b("P", adverse_and_missing, True)["B"] == "no qualified scientific determination"   # a prerequisite failure precedes the science
    assert O.flight_b("P", all_c, False)["reasons"] == ["qualification not passed"]
    for bad in (("Q", all_c, True), ("P", all_c, 1), ("P", dict(all_c, T0=recs["C"]), True), ("P", dict(all_c, TA={"determination": "ok"}), True), ("P", dict(all_c, TA={"determination": "COMPATIBLE"}), True), ("P", [recs["C"]] * 7, True)):
        assert _refused(O.flight_b, *bad)


def _tb(codes):
    """TB level records from a string: W = follows own with rival excluded; R = own adverse, follows rival; F = follows own,
    rival compatible; E = follows own, rival unresolved; B = follows neither; G = own adverse, rival unresolved; U = unresolved;
    N = not informative; X = apparatus."""
    m = {"W": ("compatible", "adverse"), "R": ("adverse", "compatible"), "F": ("compatible", "compatible"), "E": ("compatible", "unresolved"),
         "B": ("adverse", "adverse"), "U": ("unresolved", "compatible"), "G": ("adverse", "unresolved")}
    out = {}
    for k, c in zip(GRID, codes):
        out[k] = O.level_apparatus("fault") if c == "X" else O.level_tier(None, None, False, not_informative_cause="no edge at θ") if c == "N" else O.level_tier(*m[c], False)
    return out


def test_flight_d():
    n = "N" * 25
    w3 = "WWW" + n[3:]
    d = O.flight_d({"P": _tb(w3), "H": _tb(n[:10] + "W" + n[11:15] + "WW" + n[17:])}, True)       # witnesses at different levels in the two arms
    assert d["D"] == "DISTINGUISHED" and d["witness_levels"]["P"] == list(GRID[:3]) and d["witness_levels"]["H"] == [GRID[10], GRID[15], GRID[16]]
    two = O.flight_d({"P": _tb(w3), "H": _tb("WW" + n[2:])}, True)
    assert two["D"] == "NOT DISTINGUISHED" and two["reasons"] == ["under 3 witnessing levels in the H arm (2)"]
    # §6.2 row 23: both arms would witness, but one informative level of one arm follows the rival
    rival = O.flight_d({"P": _tb("WWWW" + n[4:]), "H": _tb("WWW" + n[3:8] + "R" + n[9:])}, True)
    assert rival["D"] == "NOT DISTINGUISHED" and rival["follows_rival_levels"] == {"P": [], "H": [GRID[8]]} and rival["reasons"] == ["'follows rival' at an informative level of the H arm"]
    # §6.2 row 22: one index governs both arms: the arm of the other composition follows its rival throughout
    one_index = O.flight_d({"P": _tb("W" * 25), "H": _tb("R" * 25)}, True)
    assert one_index["D"] == "NOT DISTINGUISHED" and one_index["arms"] == {"P": "COMPATIBLE", "H": "ADVERSE"}
    # D can be DISTINGUISHED with an arm that is not COMPATIBLE for B: three witnesses and a level that follows neither
    mixed = O.flight_d({"P": _tb("WWW" + "B" + n[4:10] + "B" + n[11:]), "H": _tb("WWW" + n[3:])}, True)
    assert mixed["D"] == "DISTINGUISHED" and mixed["arms"]["P"] == "NOT DISTINGUISHED"
    weak = O.flight_d({"P": _tb("WWEF" + n[4:]), "H": _tb("WWW" + n[3:])}, True)                    # follows own without rival excluded is no witness
    assert weak["D"] == "NOT DISTINGUISHED" and weak["witness_levels"]["P"] == list(GRID[:2])
    for blocked in ({"P": _tb(w3)}, {"P": _tb(w3), "H": None}, {"P": _tb(w3), "H": _tb("X" + w3[1:])}):
        assert O.flight_d(blocked, True)["D"] == "no qualified scientific determination"
    assert O.flight_d({"P": _tb(w3), "H": _tb(w3)}, False)["D"] == "no qualified scientific determination"
    for bad in (({"Q": _tb(w3)}, True), ({"P": _tb(w3), "H": _tb(w3)}, "yes"), ([_tb(w3)], True)): assert _refused(O.flight_d, *bad)


def test_flight_d_against_a_reference_on_random_sweeps():
    gen = RNG(2)
    seen = set()
    for trial in range(1500):
        codes = {c: "".join(gen.choice(list("WRFEBUNX"), size=25, p=gen.dirichlet(np.r_[np.ones(7) * 0.4, 0.05 if trial % 2 else 1e-9]))) for c in "PH"}
        qual = bool(gen.random() < 0.9)
        got = O.flight_d({c: _tb(codes[c]) for c in "PH"}, qual)["D"]
        if not qual or "X" in codes["P"] or "X" in codes["H"]: want = "no qualified scientific determination"
        elif all(codes[c].count("W") >= 3 for c in "PH") and "R" not in codes["P"] + codes["H"]: want = "DISTINGUISHED"
        else: want = "NOT DISTINGUISHED"
        assert got == want, codes
        seen.add(want)
    assert len(seen) == 3


# ======================= persistence =======================
def test_clopper_pearson():
    lo, hi = O.clopper_pearson(0); assert lo == 0.0 and math.isclose(hi, 1 - 0.025 ** (1 / 40), rel_tol=1e-12)
    lo, hi = O.clopper_pearson(40); assert hi == 1.0 and math.isclose(lo, 0.025 ** (1 / 40), rel_tol=1e-12)
    for s in range(41):
        lo, hi = O.clopper_pearson(s)
        assert 0.0 <= lo <= s / 40 <= hi <= 1.0
        if s > 0: assert math.isclose(sum(math.comb(40, k) * lo ** k * (1 - lo) ** (40 - k) for k in range(s, 41)), 0.025, rel_tol=1e-9)
        if s < 40: assert math.isclose(sum(math.comb(40, k) * hi ** k * (1 - hi) ** (40 - k) for k in range(0, s + 1)), 0.025, rel_tol=1e-9)
        rlo, rhi = O.clopper_pearson(40 - s)                                  # symmetry
        assert math.isclose(lo, 1 - rhi, abs_tol=1e-12) and math.isclose(hi, 1 - rlo, abs_tol=1e-12)
    try:
        from scipy.stats import beta
    except Exception:
        beta = None
    if beta is not None:                                                      # the textbook form, where scipy is installed
        for s in range(1, 40):
            lo, hi = O.clopper_pearson(s)
            assert math.isclose(lo, beta.ppf(0.025, s, 41 - s), rel_tol=1e-10) and math.isclose(hi, beta.ppf(0.975, s + 1, 40 - s), rel_tol=1e-10)
    for bad in ((-1,), (41,), (36.0,), (True,), (3, 0)): assert _refused(O.clopper_pearson, *bad)
    with pytest.raises(TypeError): O.clopper_pearson(20, 40, 0.75)             # the tail is the declared 0.025 and is not an argument (L2 M4 round 1, §10)
    with pytest.raises(TypeError): O.clopper_pearson(20, 40, tail=float("inf"))
    assert O.clopper_pearson(36)[0] < 0.9                                     # meeting 36 of 40 is a panel criterion, not "probability at least 0.9"


def _reference_profile(met):
    s = "".join("1" if m else "0" for m in met)
    if re.search("10", s): return "non-monotone criterion profile"
    if "0" not in s: return "criterion met at all tested levels"
    if "1" not in s: return "criterion met at no tested level"
    assert re.fullmatch("0+1+", s)
    return "both criterion phases observed"


def test_persistence_profiles_on_named_sweeps():
    def rec(counts): return O.persistence_record(dict(zip(GRID, counts)))
    both = rec([0] * 6 + [35] + [36] + [40] * 17)
    assert both["profile"] == "both criterion phases observed" and both["kappa_c_micro"] == GRID[7] and both["bracket_micro"] == [GRID[6], GRID[7]]
    assert both["endpoints"]["lower"]["survivors"] == 35 and both["endpoints"]["upper"]["survivors"] == 36 and both["endpoints"]["lower"]["level_micro"] == GRID[6]
    assert both["endpoints"]["upper"]["clopper_pearson_95"] == list(O.clopper_pearson(36)) and both["levels"][GRID[7]]["meets_criterion"] is True
    every = rec([40] * 25)
    assert every["profile"] == "criterion met at all tested levels" and every["kappa_c_micro"] == 750000 and every["bracket_micro"] is None
    assert every["endpoints"]["lower"] is None and "unbracketed on the lower side" in every["endpoints"]["lower_cause"] and every["endpoints"]["upper"]["level_micro"] == 750000
    never = rec([35] * 25)
    assert never["profile"] == "criterion met at no tested level" and never["kappa_c_micro"] is None and never["endpoints"]["upper"] is None and never["endpoints"]["upper_cause"]
    dip = rec([0] * 5 + [40] * 5 + [20] + [40] * 14)                          # meets, fails higher up, then a terminal stretch
    assert dip["profile"] == "non-monotone criterion profile" and dip["kappa_c_micro"] is None and dip["bracket_micro"] is None and dip["descriptive_suffix_micro"] == GRID[11]
    tail_fails = rec([40] * 24 + [10])
    assert tail_fails["profile"] == "non-monotone criterion profile" and tail_fails["descriptive_suffix_micro"] is None and tail_fails["descriptive_suffix_cause"]
    last = rec([0] * 24 + [36])
    assert last["profile"] == "both criterion phases observed" and last["kappa_c_micro"] == 3000000 and last["bracket_micro"] == [2500000, 3000000]
    first_only_fail = rec([35] + [40] * 24)
    assert first_only_fail["kappa_c_micro"] == 1000000 and first_only_fail["bracket_micro"] == [750000, 1000000]


def test_persistence_against_the_reference_on_many_sweeps():
    gen = RNG(3)
    seen = set()
    for trial in range(4000):
        kind = trial % 4
        if kind == 0: counts = gen.integers(0, 41, size=25)
        elif kind == 1: counts = np.sort(gen.integers(0, 41, size=25))
        elif kind == 2: counts = np.where(np.arange(25) >= gen.integers(0, 26), gen.integers(36, 41, size=25), gen.integers(0, 36, size=25))
        else: counts = gen.choice([35, 36], size=25)
        counts = [int(c) for c in counts]
        met = [c >= 36 for c in counts]
        got = O.persistence_record(dict(zip(GRID, counts)))
        want = _reference_profile(met)
        assert got["profile"] == want, counts
        seen.add(want)
        if want == "both criterion phases observed":
            i = met.index(True)
            assert got["kappa_c_micro"] == GRID[i] and got["bracket_micro"] == [GRID[i - 1], GRID[i]] and all(met[i:]) and not any(met[:i])
        elif want == "criterion met at all tested levels": assert got["kappa_c_micro"] == GRID[0]
        else: assert got["kappa_c_micro"] is None
        if want == "non-monotone criterion profile":
            suffix = got["descriptive_suffix_micro"]
            if met[-1]:
                j = GRID.index(suffix); assert all(met[j:]) and not met[j - 1]
            else: assert suffix is None
        assert [got["levels"][k]["survivors"] for k in GRID] == counts
    assert len(seen) == 4


def test_persistence_inputs_and_missing_levels():
    full = dict(zip(GRID, [40] * 25))
    short = dict(full); del short[GRID[3]]
    none = dict(full); none[GRID[3]] = None
    for surv in (short, none, {}):
        rec = O.persistence_record(surv)
        assert rec["profile"] is None and rec["kind"] == "apparatus" and rec["cause"] == "apparatus unevaluable (missing level record)" and GRID[3] in rec["missing_levels"]
    zero = O.persistence_record(dict(zip(GRID, [0] * 25)))                     # every run extinct: a valid observation, not a missing one
    assert zero["profile"] == "criterion met at no tested level" and zero["kind"] is None
    for bad in ({1025000: 40}, dict(full, **{}) | {GRID[0]: 41}, dict(full) | {GRID[0]: -1}, dict(full) | {GRID[0]: 36.0}, dict(full) | {GRID[0]: True}, [40] * 25):
        assert _refused(O.persistence_record, bad)


# ======================= nothing placed before M4 is touched =======================
PLACED = {  # LF identities at 80306ab (the M3 placement); evaluator.py as repaired for §7's cause precedence (L2 M6B round 1, D1)
    "f9/__init__.py": "7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e",
    "f9/config.py": "5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb",
    "f9/terrain.py": "b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9",
    "f9/geometry.py": "122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971",
    "f9/family.py": "ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1",
    "f9/spectral.py": "b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3",
    "f9/identities.py": "0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577",
    "f9/streams.py": "5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06",
    "f9/dynamics.py": "34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e",
    "f9/evaluator.py": "ddfa49b11955de42d5b6638d892af4c75756ff6b1b5f35ea0884c4de7b2a07a1",
}
UNTOUCHED = "c80d494aea4e5e452b4a96536f0bc68515918e4ac8c7f37e84d66bad7c7a3289"   # root, e1, f8, gates: the digest test_f9_m1.py holds


def _sha_lf(path):
    with open(path, "rb") as fh: return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def test_everything_placed_before_m4_is_byte_unchanged():
    for rel, want in PLACED.items(): assert _sha_lf(os.path.join(PKG, *rel.split("/"))) == want, rel
    # The files this module added are present beside them. The folder is not required to hold nothing else: this line
    # first required exactly that and failed as soon as a later module was placed (repaired 2026-11-18).
    assert {r.split("/")[1] for r in PLACED} | set(["outcomes.py"]) <= {fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")}
    h = hashlib.sha256()
    for sub in ("", "e1", "f8", "gates"):
        d = os.path.join(PKG, sub)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"): h.update((sub + "/" + fn if sub else fn).encode()); h.update(bytes.fromhex(_sha_lf(os.path.join(d, fn))))
    assert h.hexdigest() == UNTOUCHED
