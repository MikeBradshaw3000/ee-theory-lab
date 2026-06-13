r"""
tau_rho-at-base verification wrapper (Rule E opens-resolution, pre-spec hygiene).

PURE READ. Imports the committed tau_rho_diagnostic functions UNCHANGED and runs
them on the coupled-base un-conditioned (alpha=0) trajectories: Rule C M2 at
target c = +/-0.35 (kappa = +/-0.7599), L=0.40. The committed diagnostic measured
tau_rho = 1.66 on the kappa=0 (Lambda-only) source; the Rule E first pass layers
onto a COUPLED base at c=+/-0.35, whose autocorrelation was unmeasured. This
wrapper measures it, per the resolution memo's pre-spec verification requirement.
Worst-case across BOTH signs and all seeds and both estimators governs (matching
how tau_rho=1.66 was taken). Writes nothing. Seeds nothing. Edits nothing.

Run from repo root:
    python cycle3\wave_two\tau_rho_at_base_verify.py
"""

import numpy as np
import glob, re, importlib.util, os

# Import the committed diagnostic as a module WITHOUT modifying it.
_DIAG_PATH = os.path.join("cycle3", "wave_two", "tau_rho_diagnostic.py")
_spec = importlib.util.spec_from_file_location("tau_rho_diagnostic", _DIAG_PATH)
_diag = importlib.util.module_from_spec(_spec)
# Executing the module runs its kp0_0000 measurement once (harmless pure read);
# we then reuse its functions and constants on the 7599 families.
_spec.loader.exec_module(_diag)

per_tick_rho = _diag.per_tick_rho
acf = _diag.acf
integrated_act = _diag.integrated_act
efolding = _diag.efolding
BURN_IN = _diag.BURN_IN

FAMILIES = {
    "c=+0.35 (kp0_7599)": r"cycle3\data_out\c3_w2_rule_c_m2_states_L0.4_kp0_7599_s*.npz",
    "c=-0.35 (km0_7599)": r"cycle3\data_out\c3_w2_rule_c_m2_states_L0.4_km0_7599_s*.npz",
}

print()
print("=" * 64)
print("tau_rho-at-base verification | coupled base c=+/-0.35, L=0.40")
print(f"reusing committed diagnostic functions | burn-in: {BURN_IN} ticks")
print("=" * 64)

all_worst = []
for label, pattern in FAMILIES.items():
    files = sorted(glob.glob(pattern))
    if not files:
        raise SystemExit(f"No NPZ files found for {label} at {pattern}")
    print(f"\n{label} | files: {len(files)}")
    print("-" * 64)
    ti_list, ef_list = [], []
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
        ti_list.append(ti)
        ef_list.append(ef)
        print(f"seed {seed:>6} | T={T} tail_n={len(tail)} "
              f"rho_mean={tail.mean():.4f} rho_sd={tail.std():.4f} "
              f"lag1_ac={ac[1]:+.3f} tau_int={ti:.2f} efold={ef:.2f}")
    ti_arr, ef_arr = np.array(ti_list), np.array(ef_list)
    fam_worst = max(ti_arr.max(), ef_arr.max())
    all_worst.append((label, fam_worst))
    print("-" * 64)
    print(f"{label} | tau_int min/max/mean = "
          f"{ti_arr.min():.2f}/{ti_arr.max():.2f}/{ti_arr.mean():.2f} | "
          f"efold min/max/mean = {ef_arr.min():.2f}/{ef_arr.max():.2f}/{ef_arr.mean():.2f}")
    print(f"{label} | family worst-case: {fam_worst:.2f} ticks")

print()
print("=" * 64)
governing = max(w for _, w in all_worst)
for label, w in all_worst:
    print(f"  {label}: worst {w:.2f}")
print(f"GOVERNING coupled-base tau_rho (worst across both signs): {governing:.2f} ticks")
print(f"(committed kappa=0 baseline was 1.66 ticks; 25-tick block target)")
if governing <= 5:
    verdict = "tau_rho <= 5: 25-tick block-lag STRONGLY clears the lower bound at the coupled base. Block premise holds."
elif governing <= 10:
    verdict = "5 < tau_rho <= 10: 25-tick block-lag acceptable at the coupled base. Block premise holds."
elif governing < 25:
    verdict = "10 < tau_rho < 25: 25-tick MARGINAL at the coupled base. Return block premise to Layer 2 with this measurement before any spec."
else:
    verdict = "tau_rho >= 25: coupled base compresses the margin past the block. Block premise FAILS as sized; return to Layer 2 before any spec."
print("VERDICT:", verdict)
print("=" * 64)
