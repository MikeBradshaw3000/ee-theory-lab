"""L2 M4 round 1, D1: L2's six cases, reporting the outcome instead of asserting acceptance.

Usage: python l1_m4_round2_d1_outcomes.py /path/to/instrument
An adaptation by L1 of L2's Appendix A program (SHA-256 4c9604689b746c2e02f10c65f0c923aa176bc7dc06de1ec67e065f6364e72c9e):
the source-hash guard is removed and each case prints what happened at `_check_arm` and at the public `flight_b`
boundary. The six constructions are L2's, unchanged. Only constructed level labels and dictionaries are used.
"""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import sys

instrument = Path(sys.argv[1]).resolve()
source = instrument / "mfa_instrument/f9/outcomes.py"
print("outcomes.py", sha256(source.read_bytes()).hexdigest())
sys.path.insert(0, str(instrument))
from mfa_instrument.f9 import config as C, outcomes as O

print("declaration", O.verify_outcome_declaration())
good_arms = {t: O.arm_tier({k: O.level_tier("compatible", "compatible", O.is_same_family(t)) for k in C.F9_LEVELS_MICRO})
             for t in C.F9_REQUIRED_TERRAINS}
print("genuine arms: B =", O.flight_b("P", good_arms, True)["B"])
k = C.F9_LEVELS_MICRO[0]
base = good_arms["TA"]
variants = {}

bad = deepcopy(base); bad["level_causes"][k] = ["apparatus unevaluable (missing level record)"]
variants["apparatus level cause but COMPATIBLE"] = bad
bad = deepcopy(base); bad["causes"] = ["apparatus unevaluable (missing level record)"]
variants["apparatus arm cause but COMPATIBLE"] = bad
bad = deepcopy(base); bad["level_causes"][k] = ["no registered contour of own index within ε"]
variants["own-adverse cause but follows-own level"] = bad
bad = deepcopy(base); del bad["level_causes"]
variants["missing level_causes"] = bad
bad = deepcopy(base); bad["level_causes"] = 1
variants["non-dict level_causes"] = bad
bad = O.arm_tier({level: O.level_apparatus("missing") for level in C.F9_LEVELS_MICRO}); bad["causes"] = []; bad["level_causes"] = {}
variants["apparatus arm without any cause"] = bad


def outcome(fn, *a):
    try: return "ACCEPTED -> " + repr(fn(*a))
    except (O.F9OutcomeError, C.F9ConfigError) as e: return f"REFUSED ({type(e).__name__}: {e})"

accepted = 0
for label, bad in variants.items():
    arms = deepcopy(good_arms); arms["TA"] = bad
    a = outcome(lambda r: "valid arm record" if O._check_arm(r) is r else "?", bad)
    b = outcome(lambda x: "B = " + O.flight_b("P", x, True)["B"], arms)
    accepted += a.startswith("ACCEPTED") + b.startswith("ACCEPTED")
    print(f"{label}:\n    _check_arm: {a}\n    flight_b:   {b}")
print(f"acceptances: {accepted} of {2 * len(variants)}")
