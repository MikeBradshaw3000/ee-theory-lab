"""L2 synthetic reproducer for Flight 9 M6 round 1.

Run: python -B reproduce_m6_findings.py PATH_TO_EXTRACTED_INSTRUMENT
No lattice dynamics, master, or probe-output file is used.
This reports the submitted module's behavior; it does not alter the module.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import dynamics as D
from mfa_instrument.f9 import reports as R
from mfa_instrument.f9 import terrain as T

SHAPE = (40, 100, 100)


def record(values):
    a, r, first, last = values
    return {
        "A": np.full(SHAPE, a, dtype=np.int64),
        "R0": np.full(SHAPE, r, dtype=np.int64),
        "first": np.full(SHAPE, first, dtype=np.bool_),
        "last": np.full(SHAPE, last, dtype=np.bool_),
    }


def accepted(tuples):
    try:
        result = R.flicker({w: record(v) for w, v in tuples.items()})
        return True, result
    except R.F9ReportError as exc:
        return False, str(exc)


out = {"declaration_sha256": R.verify_reports_declaration()}
bad = {
    1: (0, 1, False, False),
    10: (100, 0, True, True),
    100: (10, 0, True, True),
}
ok, result = accepted(bad)
out["D1_impossible_stack_accepted"] = ok
if ok:
    out["D1_low_occupancy_band"] = result["bands"][0]

# Five cases isolate individual missing predicates. The inactive-segment
# increase also violates the active-segment condition, necessarily so when
# both endpoint implications hold.
cases = {
    "coarse_A_exceeds_fine_A": ((10, 1, True, False), (11, 1, True, False)),
    "fine_A_exceeds_10_times_coarse_A": ((111, 1, True, False), (11, 1, True, False)),
    "coarse_R0_exceeds_fine_R0": ((20, 1, True, False), (20, 2, True, False)),
    "coarse_Ra_exceeds_fine_Ra": ((20, 2, False, False), (20, 2, True, False)),
    "first_endpoint_implication_fails": ((20, 1, True, False), (20, 1, False, True)),
    "last_endpoint_implication_fails": ((20, 1, False, True), (20, 1, True, False)),
}
out["D1_targeted_cases_accepted"] = {
    name: accepted({1: fine, 10: coarse, 100: (10, 0, True, True)})[0]
    for name, (fine, coarse) in cases.items()
}

# This stack is realizable: no cell is ever active at any of the 1,000 ticks.
valid = {w: record((0, 1, False, False)) for w in (1, 10, 100)}
rep = R.flicker(valid)
out["D2_flicker_top_level_keys"] = list(rep)
out["D2_flicker_per_window_keys"] = list(rep["bands"][0]["windows"][1])
out["D2_floor_reference_present"] = "floor" in json.dumps(rep).lower()
pi1 = D.stationary_pi1(C.F9_ETA0)
a = 1.0 - math.exp(-C.F9_ETA0 * C.F9_DT)
out["D2_analytic_floor_window_occupancy"] = {
    w: 1.0 - (1.0 - pi1) * (1.0 - a) ** (w - 1)
    for w in (1, 10, 100)
}

u = T.bases("TC")[1]
inside, outside = R.tc_patch_sets(u)
shifted = np.roll(u, 1, axis=0)
shifted_inside, shifted_outside = R.tc_patch_sets(shifted)
counts = np.zeros(SHAPE, dtype=np.int64)
counts[:, inside] = 1000
counts[:, outside] = 100
out["D3_shifted_u_accepted"] = True
out["D3_mask_symmetric_differences"] = [
    int(np.count_nonzero(inside != shifted_inside)),
    int(np.count_nonzero(outside != shifted_outside)),
]
out["D3_correct_ratio"] = R.suppression_contrast(counts, u)["inside_over_outside"]
out["D3_shifted_ratio"] = R.suppression_contrast(counts, shifted)["inside_over_outside"]
out["schema_empty_quantiles"] = [rep["bands"][1]["windows"][w]["median"] for w in (1, 10, 100)]
out["schema_json_roundtrip_preserves_python_keys"] = json.loads(json.dumps(rep)) == rep

print(json.dumps(out, indent=2))
