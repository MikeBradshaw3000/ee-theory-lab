"""NONCANONICAL DIAGNOSIS — empirical sample: run the frozen instrument end to end (production cache)
on a bounded sample of sweeps and write every SweepResult row, to compare with the arithmetic predictor."""
import sys, json, dataclasses
sys.path.insert(0, ".")
from mfa_instrument.e1 import audit as A
cls, lo, hi, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
cache = A.load_production_cache('../artifacts/e1/threshold_cache_qualified.json', '../artifacts/e1/threshold_cache_qualification.json')
with open(out, 'a') as f:
    for i in range(lo, hi):
        r = A.run_sweep(cls, i, A.AUDIT_MASTER, cache)
        f.write(json.dumps(dataclasses.asdict(r)) + "\n"); f.flush()
