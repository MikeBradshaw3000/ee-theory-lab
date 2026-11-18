"""Reproduce D1 against an unpacked Flight 9 M4 round-1 packet.

Usage: python reproduce_f9_m4_r1.py /path/to/unpacked-packet
Only constructed level labels and dictionaries are used.
"""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import sys

packet = Path(sys.argv[1]).resolve()
instrument = packet / "flights/mfa_fidelity/instrument"
source = instrument / "mfa_instrument/f9/outcomes.py"
expected = "6523da486b8bd9af02e3635e80e1f67434eb7cc8995caa3f8f6a5247bc7319c7"
assert sha256(source.read_bytes()).hexdigest() == expected, "wrong M4 source bytes"
sys.path.insert(0, str(instrument))
from mfa_instrument.f9 import config as C, outcomes as O

assert O.verify_outcome_declaration() == (
    "c94ec4bd7c9aa532264ab2adc91ab6d4948ebff652b5b58380e1befb54a35407"
)
good_arms = {
    terrain: O.arm_tier({
        level: O.level_tier("compatible", "compatible", O.is_same_family(terrain))
        for level in C.F9_LEVELS_MICRO
    })
    for terrain in C.F9_REQUIRED_TERRAINS
}
assert O.flight_b("P", good_arms, True)["B"] == "PRODUCED"
k = C.F9_LEVELS_MICRO[0]
base = good_arms["TA"]
variants = {}

bad = deepcopy(base)
bad["level_causes"][k] = ["apparatus unevaluable (missing level record)"]
assert k in bad["informative_levels"] and k in bad["follows_own_levels"]
assert bad["unevaluable_levels"] == [] and bad["determination"] == "COMPATIBLE"
variants["apparatus level cause but COMPATIBLE"] = bad

bad = deepcopy(base)
bad["causes"] = ["apparatus unevaluable (missing level record)"]
variants["apparatus arm cause but COMPATIBLE"] = bad

bad = deepcopy(base)
bad["level_causes"][k] = ["no registered contour of own index within ε"]
variants["own-adverse cause but follows-own level"] = bad

bad = deepcopy(base)
del bad["level_causes"]
variants["missing level_causes"] = bad

bad = deepcopy(base)
bad["level_causes"] = 1
variants["non-dict level_causes"] = bad

for label, bad in variants.items():
    arms = deepcopy(good_arms)
    arms["TA"] = bad
    accepted = O._check_arm(bad) is bad
    result = O.flight_b("P", arms, True)["B"]
    assert accepted and result == "PRODUCED"
    print(f"{label}: accepted={accepted}, B={result}")

bad = O.arm_tier({level: O.level_apparatus("missing") for level in C.F9_LEVELS_MICRO})
bad["causes"] = []
bad["level_causes"] = {}
assert O._check_arm(bad) is bad
print("apparatus arm without any cause: accepted=True")
