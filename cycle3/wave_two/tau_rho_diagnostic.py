"""
tau_rho diagnostic (Rule E lag-realizability, pre-contract hygiene).

PURE READ. Loads existing Rule C M2 kappa=0 (Lambda-only, un-conditioned local
rule) L=0.40 state trajectories, computes per-tick rho, estimates the macro
density autocorrelation time on the SETTLED tail, reports per-seed and pooled
against the L2 decision thresholds. Writes nothing. Seeds nothing.

Source rationale: kp0_0000 at L0.4 IS the un-conditioned local rule at the
working anchor (kappa=0 is Lambda-only by construction). This is the correct
local-only source for tau_rho. Comparator-epsilon is a perturbed process and is
NOT used; Comparator-0 has no state NPZ in the record.

tau_rho must be estimated on the settled tail only. Including the initial
transient relaxation toward the lifted fixed point would conflate relaxation
time with steady-state fluctuation autocorrelation and inflate the estimate.
We discard a burn-in and estimate on the tail.
"""

import numpy as np
import glob, os, re

PATTERN = r"cycle3\data_out\c3_w2_rule_c_m2_states_L0.4_kp0_0000_s*.npz"
BURN_IN = 100          # discard first 100 of 200 ticks as transient; estimate on settled tail
LOW_AC_FLOOR = 0.0     # ACF values below this are treated as noise for integrated-time summation cutoff

def per_tick_rho(states):
    # states: (T, 50, 50) int {0,1}; rho_t = active fraction per tick
    return states.reshape(states.shape[0], -1).mean(axis=1)

def acf(x, max_lag):
    x = x - x.mean()
    var = np.dot(x, x) / len(x)
    if var == 0:
        return np.zeros(max_lag + 1)
    out = np.empty(max_lag + 1)
    for k in range(max_lag + 1):
        out[k] = np.dot(x[:len(x)-k], x[k:]) / (len(x) - k) / var
    return out

def integrated_act(ac):
    # tau_int = 1 + 2*sum_{k>=1} rho_k, truncated at first non-positive ACF (Sokal-style)
    s = 0.0
    for k in range(1, len(ac)):
        if ac[k] <= 0:
            break
        s += ac[k]
    return 1.0 + 2.0 * s

def efolding(ac):
    # first lag where ACF drops below 1/e; linear-interp between bracketing lags
    thr = 1.0 / np.e
    for k in range(1, len(ac)):
        if ac[k] < thr:
            a0, a1 = ac[k-1], ac[k]
            if a0 == a1:
                return float(k)
            return (k - 1) + (a0 - thr) / (a0 - a1)
    return float(len(ac) - 1)  # did not decay below 1/e within window

files = sorted(glob.glob(PATTERN))
if not files:
    raise SystemExit("No kp0_0000 L0.4 NPZ files found at expected pattern.")

print(f"tau_rho diagnostic | source: Rule C M2 kappa=0, L=0.40 (un-conditioned local rule)")
print(f"burn-in discarded: {BURN_IN} ticks | files: {len(files)}")
print("-" * 64)

pooled_tail = []
seed_tau_int = []
seed_efold = []
max_lag = None

for f in files:
    seed = re.search(r"_s(\d+)\.npz$", f).group(1)
    d = np.load(f)
    states = d["states"]
    T = states.shape[0]
    rho = per_tick_rho(states)
    tail = rho[BURN_IN:]
    if max_lag is None:
        max_lag = min(50, len(tail) - 2)
    ml = min(max_lag, len(tail) - 2)
    ac = acf(tail, ml)
    ti = integrated_act(ac)
    ef = efolding(ac)
    seed_tau_int.append(ti)
    seed_efold.append(ef)
    pooled_tail.append(tail)
    print(f"seed {seed:>6} | T={T} tail_n={len(tail)} "
          f"rho_mean={tail.mean():.4f} rho_sd={tail.std():.4f} "
          f"lag1_ac={ac[1]:+.3f} tau_int={ti:.2f} efold={ef:.2f}")

print("-" * 64)
ti_arr = np.array(seed_tau_int)
ef_arr = np.array(seed_efold)
print(f"tau_int  per-seed: min={ti_arr.min():.2f} max={ti_arr.max():.2f} mean={ti_arr.mean():.2f}")
print(f"efolding per-seed: min={ef_arr.min():.2f} max={ef_arr.max():.2f} mean={ef_arr.mean():.2f}")

worst = max(ti_arr.max(), ef_arr.max())
print("-" * 64)
print(f"governing estimate (worst of tau_int.max / efold.max): {worst:.2f} ticks")
if worst <= 5:
    verdict = "tau_rho <= 5: 25-tick block-lag STRONGLY clears the lower bound."
elif worst <= 10:
    verdict = "5 < tau_rho <= 10: 25-tick block-lag acceptable."
elif worst < 25:
    verdict = "10 < tau_rho < 25: 25 MARGINAL; consider 50-tick block-lag."
else:
    verdict = "tau_rho >= 25: Rule E likely inert/circular under current windows; rest at scoping."
print("VERDICT:", verdict)
