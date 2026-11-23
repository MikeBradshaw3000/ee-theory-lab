import hashlib
import json
import sys
from pathlib import Path

import numpy as np

instrument = Path(sys.argv[1]).resolve()
source = instrument / "mfa_instrument/f9/reports.py"
expected = "f42f93c586288ee14ee11dfe8e2430e544e81529a2eaba17e73b0bf4345a92de"
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
sys.path.insert(0, str(instrument))
from mfa_instrument.f9 import reports as R

WIDTHS = (1, 10, 100)
KEYS = ("A", "R0", "first", "last")
SHAPE = (40, 100, 100)


def stacked(tuples):
    return {
        w: {
            key: np.full(
                SHAPE, value,
                dtype=bool if key in ("first", "last") else np.int64
            )
            for key, value in zip(KEYS, tup)
        }
        for w, tup in zip(WIDTHS, tuples)
    }


def direct_summary(ticks, width):
    active = np.asarray(ticks, dtype=bool).reshape(-1, width).any(axis=1)
    inactive_segments = int(not active[0]) + int(
        np.count_nonzero(active[:-1] & ~active[1:])
    )
    return (
        int(active.sum()), inactive_segments,
        bool(active[0]), bool(active[-1])
    )


forged = (
    (20, 1, True, False),
    (20, 1, True, False),
    (2, 1, True, False),
)
prefix = np.arange(1000) < 20
actual = tuple(direct_summary(prefix, w) for w in WIDTHS)
assert actual == (
    (20, 1, True, False),
    (2, 1, True, False),
    (1, 1, True, False),
)
bad_report = R.flicker(stacked(forged))
good_report = R.flicker(stacked(actual))


def medians(report):
    return [report["bands"][0]["windows"][w]["median"] for w in WIDTHS]


assert medians(bad_report) == [980.0, 800.0, 800.0]
assert medians(good_report) == [980.0, 980.0, 900.0]

old_counterexample = (
    (0, 1, False, False),
    (100, 0, True, True),
    (10, 0, True, True),
)
try:
    R.flicker(stacked(old_counterexample))
except R.F9ReportError:
    old_counterexample_refused = True
else:
    old_counterexample_refused = False
assert old_counterexample_refused

print(json.dumps({
    "source_sha256": expected,
    "declaration_sha256": R.verify_reports_declaration(),
    "round1_counterexample_refused": old_counterexample_refused,
    "forged_stack_accepted": True,
    "forged_tuples": forged,
    "tuples_forced_by_the_fine_prefix": actual,
    "forged_medians": medians(bad_report),
    "actual_prefix_medians": medians(good_report),
    "floor_reference": bad_report["floor_reference"],
}, indent=2))
