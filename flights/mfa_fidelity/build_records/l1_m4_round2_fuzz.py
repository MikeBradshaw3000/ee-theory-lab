"""Replace each position of each genuine arm record (and each field of three level records) by each of 21 junk values and
report: acceptances, typed refusals, and any exception that is not the module's own.
Usage: python l1_m4_round2_fuzz.py /path/to/instrument   (reads tests/test_f9_m4.py for the genuine arms)"""
import sys, copy, collections
from pathlib import Path
inst = Path(sys.argv[1]).resolve(); sys.path.insert(0, str(inst / "tests")); sys.path.insert(0, str(inst))
import test_f9_m4 as T
from mfa_instrument.f9 import config as C, outcomes as O
junk = [None, True, False, 0, 1, 1.0, float("nan"), "", "x", [], [1], (), {}, {"a": 1}, {1: 2, "a": 3}, b"x", object(), 10**30, -1, [[]], {"state": []}]
arms = T._genuine_arms(); other = collections.Counter(); acc = typed = same = 0
def walk(o, path=()):
    yield path
    if isinstance(o, dict):
        for k in list(o): yield from walk(o[k], path + (k,))
    elif isinstance(o, list):
        for i in range(len(o)): yield from walk(o[i], path + (i,))
def setp(o, path, v):
    for p in path[:-1]: o = o[p]
    o[path[-1]] = v
good = {t: arms["A3"] for t in C.F9_REQUIRED_TERRAINS}
for name, rec in arms.items():
    paths = [p for p in walk(rec) if p]
    step = max(1, len(paths) // 120)
    for p in paths[::step]:
        for j in junk:
            bad = copy.deepcopy(rec); setp(bad, p, j)
            if repr(bad) == repr(rec): same += 1; continue
            for fn, args in ((O._check_arm, (bad,)), (O.flight_b, ("P", dict(good, TB=bad), True))):
                try: fn(*args); acc += 1; print("ACCEPTED", name, p, repr(j)[:30])
                except (O.F9OutcomeError, C.F9ConfigError): typed += 1
                except Exception as e: other[type(e).__name__ + ": " + str(e)[:60]] += 1
print(f"arm records: {len(arms)} genuine; calls refused with the module's own exception {typed}; accepted {acc}; other exceptions {sum(other.values())} {dict(other)}; no-change cases skipped {same}")
lv = [O.level_tier("compatible", "adverse", False), O.level_apparatus("missing"), O.level_tier(None, None, False, not_informative_cause="no eligible contour")]
acc = typed = same = 0; other = collections.Counter()
for r in lv:
    for k in list(r) + [1]:
        for j in junk:
            b = copy.deepcopy(r); b[k] = j
            if repr(b) == repr(r): same += 1; continue
            try: O._check_level(b); acc += 1; print("ACCEPTED level", k, repr(j))
            except (O.F9OutcomeError, C.F9ConfigError): typed += 1
            except Exception as e: other[type(e).__name__ + ": " + str(e)[:60]] += 1
print(f"level records: refused with the module's own exception {typed}; accepted {acc}; other exceptions {sum(other.values())} {dict(other)}; no-change cases skipped {same}")
