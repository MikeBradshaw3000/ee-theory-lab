import math
import numpy as np
from scipy.special import ndtr
from scipy.optimize import brentq

theta = 0.20

def clipped_mean(c, sigma):
    if sigma == 0:
        return float(c)
    a = -c / sigma
    b = (1.0 - c) / sigma
    phi = lambda z: math.exp(-0.5*z*z) / math.sqrt(2.0*math.pi)
    return float(
        c * (ndtr(b) - ndtr(a))
        - sigma * (phi(b) - phi(a))
        + 1.0 - ndtr(b)
    )

# Interior example: row 15 accepts a population map close to theta.
near = clipped_mean(0.13, 0.31)
assert 0.03 < 0.13 < 0.14
assert abs(near - theta) < 0.001
print("c=.13, sigma=.31:", near)

# Reverse example: row 25 accepts a population map outside the band.
far = clipped_mean(0.25, 0.35)
assert 0.14 < 0.25 < 0.26
assert abs(far - theta) > 0.06
print("c=.25, sigma=.35:", far)

s = brentq(
    lambda sigma: clipped_mean(0.13, sigma) - theta,
    0.25, 0.40, xtol=1e-15
)
print("sigma giving population mean theta:", s)
print("population endpoints for c in [.12,.14]:",
      clipped_mean(0.12, s), clipped_mean(0.14, s))
print("intercept-interval mass in constant proposal:", 0.02 / 0.25)

# Valid 1,000-tick occupancy fractions, 40 seeds at each cell.
x = np.r_[np.full(5, 0.936), 0.195, np.full(34, 0.010)]
i, j = np.indices((100, 100))
idx = (np.arange(40)[:, None, None]
       + 4*i[None, :, :] + 12*j[None, :, :]) % 40
X = x[idx]
residual = X - X.mean(axis=0)
box = sum(
    np.roll(np.roll(X, dx, axis=1), dy, axis=2)
    for dx in (-1, 0, 1)
    for dy in (-1, 0, 1)
) / 9.0

sigma_bin = float(x.std(ddof=1))
a2 = float(np.median(box.std(axis=0, ddof=1) / np.sqrt(40)))
rho1 = float(
    np.sum(residual * (
        np.roll(residual, -1, axis=1)
        + np.roll(residual, -1, axis=2)
    )) / (2 * np.sum(residual**2))
)
assert 0.12 < x.mean() < 0.14
assert a2 < 0.02
assert rho1 <= 0
assert abs(clipped_mean(0.13, sigma_bin) - theta) < 0.001
print("bin mean / SD:", float(x.mean()), sigma_bin)
print("A2 median SE / pooled rho1:", a2, rho1)
print("population mean at c=.13:", clipped_mean(0.13, sigma_bin))

# Row-15 cause-accounting witness.
# A canonical family is nonempty; the realized sample region is empty.
# L3 therefore requires "no edge at theta", before L4 "under-resolved".
output = "under-resolved"
decisive = output in {"compatible", "adverse"}
apparatus_failure = False
v06_literal_error = decisive or apparatus_failure
correct_sample_cause = False
assert not v06_literal_error
assert not correct_sample_cause
print("wrong sample cause omitted by v0.6:", not v06_literal_error)
