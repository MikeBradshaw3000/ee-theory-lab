from mfa_instrument.f9 import config as C, t0 as T

def obs(survives, total):
    return {"survival": [survives] * 40, "tail_sum": [total] * 40}

grid = C.F9_LEVELS_MICRO
high = {
    k: obs(k >= 1_000_000, 1_000_000 if k >= 1_000_000 else 0)
    for k in grid
}
low = {k: obs(False, 0) for k in grid}
realization = {k: obs(True, 1_000_000) for k in grid}
calibration = {
    obj: {k: [1_000_000] * 40 for k in grid}
    for obj in ("skeleton", "realization")
}

r = T.evaluate_t0(high, low, realization, calibration)
print("high boundary:", r["reference"]["kappa_c_t0_micro"])
print("high eligible:", T._eligible(grid.index(1_000_000)))
for test in r["tests"]:
    print(test["test"], test["outcome"], test["cause"])
print("T0:", r["determination"], r["cause"])
