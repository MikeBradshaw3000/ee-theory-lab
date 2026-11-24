"""f9_m6b_round1_d1_routes_after_repair.py — L2's Appendix R reproducer for D1 (M6B round 1), turned into the conformance
check L2 prescribed: the final per-entry inequality is replaced with equality, and the point's cells and bonds are asserted
against the values of L2's section 2 table. Run with flights/mfa_fidelity/instrument on PYTHONPATH. Constructed counts only; no lattice run.
Nothing here is part of the instrument."""
import hashlib
import numpy as np
from mfa_instrument.f9 import evaluator as E
from mfa_instrument.f9 import evaluator_reports as X
from mfa_instrument.f9 import terrain as T

for m in (E, X): print(m.__name__, hashlib.sha256(open(m.__file__, "rb").read()).hexdigest())
f = E.IndexFamily(T.comparison_array("T0", "P"), "T0", "P")
families = {"P": f, "H": f.shared_with("H")}
assert len(f) == 0
key = E.arm_level_key(777, "T0", "P", 1_000_000)
skeleton_key = X.skeleton_level_key(777, "T0", "P", 1_000_000)
expected = {"result": "not informative", "cause": "no eligible contour", "resampled": False}
empty = np.zeros((40, 100, 100), dtype=np.int64)
full = np.full_like(empty, 1000)
small = empty.copy()
small[:, 10:16, 10:16] = 1000
TABLE = {("empty", 100000): (0, 0), ("empty", 200000): (0, 0), ("empty", 300000): (0, 0),
         ("full", 100000): (10000, 0), ("full", 200000): (10000, 0), ("full", 300000): (10000, 0),
         ("under_minimum", 100000): (64, 32), ("under_minimum", 200000): (60, 32), ("under_minimum", 300000): (52, 32)}
rows = 0
for state, counts in (("empty", empty), ("full", full), ("under_minimum", small)):
    records = {"placed_020": (200000, E.evaluate_level(counts, families, key)),
               "skeleton_020": (200000, X.skeleton_boundary(counts, families, skeleton_key)["evaluation"])}
    reports = X.reported_thresholds(counts, families, key)
    for theta, record in reports["theta_micro"].items(): records[f"reported_{theta}"] = (theta, record)
    for route, (theta, record) in records.items():
        point = record["point"]
        causes = {name: entry["cause"] for name, entry in record["indices"].items()}
        print(state, route, point["region_cells"], point["bonds"], point["informative"], repr(point["reason"]), causes)
        assert record["resampled"] is False and point["informative"] is False
        assert (point["region_cells"], point["bonds"]) == TABLE[(state, theta)]
        assert all(entry == expected for entry in record["indices"].values())
        rows += 1
assert rows == 12
print("All 12 routes: both index entries are 'no eligible contour'; the point records still describe the maps.")
