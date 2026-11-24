import numpy as np
from mfa_instrument.f9 import evaluator as E
from mfa_instrument.f9 import evaluator_reports as X
from mfa_instrument.f9 import terrain as T

f = E.IndexFamily(T.comparison_array("T0", "P"), "T0", "P")
families = {"P": f, "H": f.shared_with("H")}
assert len(f) == 0
key = E.arm_level_key(777, "T0", "P", 1_000_000)
skeleton_key = X.skeleton_level_key(777, "T0", "P", 1_000_000)
expected = {
    "result": "not informative",
    "cause": "no eligible contour",
    "resampled": False,
}

empty = np.zeros((40, 100, 100), dtype=np.int64)
full = np.full_like(empty, 1000)
small = empty.copy()
small[:, 10:16, 10:16] = 1000

for state, counts in (("empty", empty), ("full", full),
                      ("under_minimum", small)):
    records = {
        "placed_020": E.evaluate_level(counts, families, key),
        "skeleton_020": X.skeleton_boundary(
            counts, families, skeleton_key
        )["evaluation"],
    }
    reports = X.reported_thresholds(counts, families, key)
    for theta, record in reports["theta_micro"].items():
        records[f"reported_{theta}"] = record
    for route, record in records.items():
        point = record["point"]
        causes = {name: entry["cause"]
                  for name, entry in record["indices"].items()}
        print(state, route, point["region_cells"], point["bonds"], causes)
        assert record["resampled"] is False
        assert all(entry != expected
                   for entry in record["indices"].values())

print("Reproduced: all 12 routes violate constant-index cause precedence.")
