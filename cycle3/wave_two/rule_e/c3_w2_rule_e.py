#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cycle 3, Wave Two: Rule E (Lagged-Lambda Conditioning)
Topology: 50x50, Toroidal, Moore Radius 1
Observables: Psi_meanI_state, Psi_persistence_I (co-equal pair)

Purpose: Establish the behavioral map of the Rule E instrument. The script produces
outputs to evaluate whether a macro-conditioned, lagged activation-density signal
modifies structural behavior.

Mechanism: A 25-tick block-lag conditions the becoming-active logit parameter.
Survival stays strictly on the un-conditioned bare Lambda baseline (Leak-Surface Guard).
At alpha = 0.0, the script bypasses conditioning by branch, running bit-exact Rule C (F3 Bypass).

Apparatus Parity: Tests local reimplementations against validated c3_ctl_001_battery
and c3_ss_001_battery modules. Validates alpha=0 recovery against committed c3_w2_rule_c_m2.
"""

import sys
import os
import random

# ==========================================
# Pre-flight Verification (Fail Fast)
# ==========================================
if sys.prefix == sys.base_prefix:
    raise RuntimeError("PRE-FLIGHT FAIL: Virtual environment is not active.")

if sys.version_info[:2] != (3, 14):
    raise RuntimeError(f"PRE-FLIGHT FAIL: Python 3.14.x required. Found: {sys.version_info[:2]}")

try:
    import numpy as np
    import pandas as pd
    import mesa
except ImportError as e:
    raise RuntimeError(f"PRE-FLIGHT FAIL: Critical import missing. {e}")

if np.__version__ != "2.4.4":
    raise RuntimeError(f"PRE-FLIGHT FAIL: numpy 2.4.4 required. Found: {np.__version__}")

if not os.path.exists(os.path.join("cycle3", "c3_ctl_001_battery.py")):
    raise RuntimeError("PRE-FLIGHT FAIL: cycle3 directory or c3_ctl_001_battery.py unreachable.")

# ==========================================
# Locked Apparatus Parameters
# ==========================================
GRID_SIZE = 50
N_CELLS = GRID_SIZE * GRID_SIZE
TICKS_PER_RUN = 400        # Expanded to 400 ticks (100 burn-in, 300 post)
WINDOW_LENGTH = 100
WINDOW_STEP = 25
BLOCK_LENGTH = 25          # Non-overlapping macro blocks
SEEDS = [42, 137, 256, 1024, 31415]
TARGET_RHO_INIT = 0.10
INIT_ACTIVE_CELLS = round(TARGET_RHO_INIT * N_CELLS)

# SS-001 & Degeneracy Thresholds
THRESH_RELATIVE_DRIFT = 0.10
THRESH_RHO_CV = 0.10
THRESH_RHO_RANGE_OVER_MEAN = 0.25
LIFTED_THRESHOLD = 0.05
VAR_EPSILON = 1e-3
LOW_Z_THRESH = 2.0
PERMUTATIONS = 199

# ==========================================
# Rule E Grid Configuration
# ==========================================
P_LAMBDA = 0.40

# Precomputed Kappa anchors matching c = +/- 0.35 at Lambda = 0.40
KAPPA_PLUS = 0.7599
KAPPA_MINUS = -0.7599

# Alpha Tier Setup
TARGET_D_VALS = [0.0, 0.0125, 0.025, 0.05, 0.10]

def compute_alpha_grid(p_L, d_vals):
    """Computes specific alpha adjustments via logit inversion."""
    grid = []
    logit_pL = np.log(p_L / (1.0 - p_L))
    for d in d_vals:
        if d == 0.0:
            grid.append((d, 0.0, 0.0))
        else:
            alpha_plus = np.log((p_L + d) / (1.0 - (p_L + d))) - logit_pL
            alpha_minus = np.log((p_L - d) / (1.0 - (p_L - d))) - logit_pL
            grid.append((d, alpha_plus, alpha_minus))
    return grid

ALPHA_TIERS = compute_alpha_grid(P_LAMBDA, TARGET_D_VALS)

# ==========================================
# Helper: Sanitization
# ==========================================
def sanitize_float(val):
    """Formats floats to matched string conventions for join keys and filenames."""
    return f"{val:+.4f}".replace("-", "m").replace("+", "p").replace(".", "_")

# ==========================================
# Apparatus Functions (Wave One Parity)
# ==========================================
def calculate_morans_i_toroidal_8(grid):
    grid_mean = np.mean(grid)
    grid_var = np.var(grid)
    if grid_var < 1e-9:
        return 0.0
    centered = grid - grid_mean
    w_sum = (
        np.roll(centered, 1, axis=0) + np.roll(centered, -1, axis=0) +
        np.roll(centered, 1, axis=1) + np.roll(centered, -1, axis=1) +
        np.roll(np.roll(centered, 1, axis=0), 1, axis=1) +
        np.roll(np.roll(centered, 1, axis=0), -1, axis=1) +
        np.roll(np.roll(centered, -1, axis=0), 1, axis=1) +
        np.roll(np.roll(centered, -1, axis=0), -1, axis=1)
    )
    numerator = np.sum(centered * w_sum)
    denominator = np.sum(centered**2)
    return (1.0 / 8.0) * (numerator / denominator)

def batch_morans_i_toroidal_8(grids):
    grid_mean = np.mean(grids, axis=(1, 2), keepdims=True)
    grid_var = np.var(grids, axis=(1, 2), keepdims=True)
    valid_mask = np.squeeze(grid_var) > 1e-9
    if not np.any(valid_mask):
        return np.zeros(grids.shape[0])
    centered = grids - grid_mean
    w_sum = (
        np.roll(centered, 1, axis=1) + np.roll(centered, -1, axis=1) +
        np.roll(centered, 1, axis=2) + np.roll(centered, -1, axis=2) +
        np.roll(np.roll(centered, 1, axis=1), 1, axis=2) +
        np.roll(np.roll(centered, 1, axis=1), -1, axis=2) +
        np.roll(np.roll(centered, -1, axis=1), 1, axis=2) +
        np.roll(np.roll(centered, -1, axis=1), -1, axis=2)
    )
    numerator = np.sum(centered * w_sum, axis=(1, 2))
    denominator = np.sum(centered**2, axis=(1, 2))
    I_vals = np.zeros(grids.shape[0])
    np.divide(numerator, denominator, out=I_vals, where=valid_mask)
    return (1.0 / 8.0) * I_vals

def compute_persistence_null(grid, actual_I, num_permutations=PERMUTATIONS):
    if np.var(grid) < 1e-9:
        return 0.0
    flat_grid = grid.flatten()
    null_Is = np.zeros(num_permutations)
    for i in range(num_permutations):
        shuffled = np.random.permutation(flat_grid).reshape((GRID_SIZE, GRID_SIZE))
        null_Is[i] = calculate_morans_i_toroidal_8(shuffled)
    null_std = np.std(null_Is)
    return (actual_I - np.mean(null_Is)) / null_std if null_std > 1e-9 else 0.0

def compute_meanI_state_null(actual_grids, actual_meanI, num_permutations=PERMUTATIONS):
    null_meanIs = np.zeros(num_permutations)
    ticks, h, w = actual_grids.shape
    flat_grids = actual_grids.reshape(ticks, -1)
    for p in range(num_permutations):
        rand_idx = np.random.rand(ticks, h * w).argsort(axis=1)
        shuffled_flat = np.take_along_axis(flat_grids, rand_idx, axis=1)
        tick_Is = batch_morans_i_toroidal_8(shuffled_flat.reshape(ticks, h, w))
        null_meanIs[p] = np.mean(tick_Is)
    null_std = np.std(null_meanIs)
    return (actual_meanI - np.mean(null_meanIs)) / null_std if null_std > 1e-9 else 0.0

def evaluate_window_ss(rho_window):
    mean_rho = np.mean(rho_window)
    epsilon = 1e-9
    t = np.arange(WINDOW_LENGTH)
    slope, _ = np.polyfit(t, rho_window, 1)
    relative_drift = (abs(slope) * WINDOW_LENGTH) / (mean_rho + epsilon)
    rho_cv = np.std(rho_window) / (mean_rho + epsilon)
    rho_range_over_mean = (np.max(rho_window) - np.min(rho_window)) / (mean_rho + epsilon)

    steady = (relative_drift < THRESH_RELATIVE_DRIFT) and \
             (rho_cv < THRESH_RHO_CV) and \
             (rho_range_over_mean < THRESH_RHO_RANGE_OVER_MEAN)
    lifted = mean_rho > LIFTED_THRESHOLD

    return relative_drift, rho_cv, rho_range_over_mean, mean_rho, steady, lifted

def run_parity_check():
    sys.path.insert(0, os.path.abspath("cycle3"))
    try:
        import c3_ctl_001_battery as ctl
        import c3_ss_001_battery as ss

        PARITY_SEED = 7
        np.random.seed(PARITY_SEED)

        test_grids = np.random.randint(0, 2, size=(100, 50, 50))
        test_rho = np.mean(test_grids, axis=(1, 2))

        assert np.isclose(calculate_morans_i_toroidal_8(test_grids[0]), ctl.calculate_morans_i_toroidal_8(test_grids[0]))
        assert np.allclose(batch_morans_i_toroidal_8(test_grids), ctl.batch_morans_i_toroidal_8(test_grids))

        loc_res = evaluate_window_ss(test_rho)
        ext_res = ss.evaluate_window(test_rho)
        assert np.isclose(loc_res[0], ext_res["Relative_Drift"])
        assert np.isclose(loc_res[1], ext_res["Rho_CV"])
        assert loc_res[4] == ext_res["Steady_State_Candidate"]

    except AssertionError as e:
        raise RuntimeError(f"PRE-FLIGHT FAIL: Parity check broken. Reimplementation diverges. {e}")
    except Exception as e:
        raise RuntimeError(f"PRE-FLIGHT FAIL: Parity check execution error: {e}")
    finally:
        sys.path.pop(0)

# ==========================================
# Rule E Core Implementation
# ==========================================
def get_neighbor_count(grid):
    return (
        np.roll(grid, 1, axis=0) + np.roll(grid, -1, axis=0) +
        np.roll(grid, 1, axis=1) + np.roll(grid, -1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), -1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), -1, axis=1)
    )

def step_rule_e(grid, p_Lambda, kappa, alpha, g_E):
    """
    Rule E Transition.
    Leak-Surface Guard: conditioned g_E acts ONLY on the becoming-active logit.
    Staying-active strictly utilizes bare p_Lambda.
    rand_grid is drawn INSIDE the step function to preserve exact draw-order parity
    with committed Rule C.
    """
    rand_grid = np.random.rand(GRID_SIZE, GRID_SIZE)
    neighbors = get_neighbor_count(grid)
    q = neighbors / 8.0

    if alpha == 0.0:
        # F3 Bypass: Bit-exact recovery of Rule C un-conditioned behavior.
        logit_p = np.log(p_Lambda / (1.0 - p_Lambda))
        p_become = 1.0 / (1.0 + np.exp(-(logit_p + kappa * (2.0 * q - 1.0))))
        becomes_active = (grid == 0) & (rand_grid < p_become)
    else:
        # Lagged Conditioning Branch
        logit_eff = np.log(p_Lambda / (1.0 - p_Lambda)) + alpha * g_E
        p_become_eff = 1.0 / (1.0 + np.exp(-(logit_eff + kappa * (2.0 * q - 1.0))))
        becomes_active = (grid == 0) & (rand_grid < p_become_eff)

    # UNCONDITIONED SURVIVAL
    stays_active = (grid == 1) & (rand_grid < p_Lambda)

    # Correction 3: Diagnostic term for logging computed uniformly without branch-forcing 0
    cond_term = alpha * g_E

    return (becomes_active | stays_active).astype(int), cond_term

def verify_f3_bypass():
    """Build-verification ensuring alpha=0 recovers committed Rule C M2 bit-exactly."""
    sys.path.insert(0, os.path.abspath("cycle3"))
    try:
        import c3_w2_rule_c_m2 as rule_c
    except ImportError:
        raise RuntimeError("BUILD FAIL: Could not import committed c3_w2_rule_c_m2.py for F3 trajectory verification.")
    finally:
        sys.path.pop(0)

    for kappa_val in [KAPPA_PLUS, KAPPA_MINUS]:
        for seed in SEEDS:
            # Trajectory 1: Committed Rule C
            np.random.seed(seed)
            random.seed(seed)
            flat_grid = np.zeros(N_CELLS, dtype=int)
            flat_grid[:INIT_ACTIVE_CELLS] = 1
            np.random.shuffle(flat_grid)
            grid_c = flat_grid.reshape((GRID_SIZE, GRID_SIZE))

            states_c = np.zeros((TICKS_PER_RUN, GRID_SIZE, GRID_SIZE), dtype=int)
            for t in range(TICKS_PER_RUN):
                states_c[t] = grid_c
                grid_c = rule_c.step_rule_c(grid_c, P_LAMBDA, kappa_val)

            # Trajectory 2: Rule E with alpha = 0.0
            np.random.seed(seed)
            random.seed(seed)
            flat_grid = np.zeros(N_CELLS, dtype=int)
            flat_grid[:INIT_ACTIVE_CELLS] = 1
            np.random.shuffle(flat_grid)
            grid_e = flat_grid.reshape((GRID_SIZE, GRID_SIZE))

            states_e = np.zeros((TICKS_PER_RUN, GRID_SIZE, GRID_SIZE), dtype=int)
            for t in range(TICKS_PER_RUN):
                states_e[t] = grid_e
                grid_e, _ = step_rule_e(grid_e, P_LAMBDA, kappa_val, 0.0, 999.0)

            if not np.array_equal(states_c, states_e):
                raise RuntimeError(f"BUILD FAIL: F3 alpha=0 bypass failed bit-exact recovery at kappa={kappa_val}, seed={seed}.")

    # Prescribed verification report string
    print(f"alpha=0 Rule E reproduces committed Rule C M2 bit-exactly over a full 400-tick trajectory at (Lambda={P_LAMBDA}, kappa=+/-0.7599, each seed)")


# ==========================================
# Execution Pipeline
# ==========================================

def execute_rule_e():
    run_parity_check()
    verify_f3_bypass()

    out_dir = os.path.join("cycle3", "data_out")
    os.makedirs(out_dir, exist_ok=True)

    # ------------------------------------------
    # Phase 1: Pre-Registered Split Constants
    # ------------------------------------------
    def measure_baseline(kappa_val):
        baseline_block_means = []
        for seed in SEEDS:
            np.random.seed(seed)
            random.seed(seed)
            flat_grid = np.zeros(N_CELLS, dtype=int)
            flat_grid[:INIT_ACTIVE_CELLS] = 1
            np.random.shuffle(flat_grid)
            grid = flat_grid.reshape((GRID_SIZE, GRID_SIZE))

            rhos = np.zeros(TICKS_PER_RUN)
            for t in range(TICKS_PER_RUN):
                grid, _ = step_rule_e(grid, P_LAMBDA, kappa_val, 0.0, 0.0)
                rhos[t] = np.mean(grid)

            # Block-level aggregation
            for b in range(TICKS_PER_RUN // BLOCK_LENGTH):
                b_rho = np.mean(rhos[b*BLOCK_LENGTH : (b+1)*BLOCK_LENGTH])
                baseline_block_means.append(b_rho)

        return np.mean(baseline_block_means), np.std(baseline_block_means, ddof=0)

    print("Measuring Alpha=0 Baselines...")
    M_ref_plus, sigma_M_plus = measure_baseline(KAPPA_PLUS)
    M_ref_minus, sigma_M_minus = measure_baseline(KAPPA_MINUS)

    if sigma_M_plus < 1e-6 or sigma_M_minus < 1e-6:
        raise RuntimeError("BUILD FAIL: Ill-conditioned macro channel. Block standard deviation is near-zero.")

    print(f"Plus Anchor: M_ref={M_ref_plus:.4f}, sigma_M={sigma_M_plus:.4f}")
    print(f"Minus Anchor: M_ref={M_ref_minus:.4f}, sigma_M={sigma_M_minus:.4f}")

    # ------------------------------------------
    # Phase 2: The Main Rule E Sweep
    # ------------------------------------------
    window_results = []
    block_results = []

    for base_sign, kappa_val, M_ref, sigma_M in [("+", KAPPA_PLUS, M_ref_plus, sigma_M_plus),
                                                 ("-", KAPPA_MINUS, M_ref_minus, sigma_M_minus)]:
        for target_d, alpha_plus, alpha_minus in ALPHA_TIERS:
            alpha_val = alpha_plus if base_sign == "+" else alpha_minus
            if target_d == 0.0:
                alpha_val = 0.0

            for seed in SEEDS:
                # Correction 2: Sanitized float tokens for run_id and NPZ key
                k_str = sanitize_float(kappa_val)
                a_str = sanitize_float(alpha_val)
                run_id = f"R_E_k{k_str}_a{a_str}_s{seed}"

                np.random.seed(seed)
                random.seed(seed)

                flat_grid = np.zeros(N_CELLS, dtype=int)
                flat_grid[:INIT_ACTIVE_CELLS] = 1
                np.random.shuffle(flat_grid)
                grid = flat_grid.reshape((GRID_SIZE, GRID_SIZE))

                states = np.zeros((TICKS_PER_RUN, GRID_SIZE, GRID_SIZE), dtype=int)
                rhos = np.zeros(TICKS_PER_RUN)

                # Block tracking records
                block_cond_logs = np.zeros(TICKS_PER_RUN // BLOCK_LENGTH)
                block_gE_logs = np.zeros(TICKS_PER_RUN // BLOCK_LENGTH)
                block_M_logs = np.zeros(TICKS_PER_RUN // BLOCK_LENGTH)

                for b_idx in range(TICKS_PER_RUN // BLOCK_LENGTH):
                    if b_idx == 0:
                        M_m = M_ref
                    else:
                        M_m = np.mean(rhos[(b_idx-1)*BLOCK_LENGTH : b_idx*BLOCK_LENGTH])

                    g_E = (M_m - M_ref) / sigma_M

                    block_M_logs[b_idx] = M_m
                    block_gE_logs[b_idx] = g_E

                    b_cond_log = 0.0
                    for tick_in_b in range(BLOCK_LENGTH):
                        t = b_idx * BLOCK_LENGTH + tick_in_b
                        grid, cond_term = step_rule_e(grid, P_LAMBDA, kappa_val, alpha_val, g_E)
                        states[t] = grid
                        rhos[t] = np.mean(grid)
                        b_cond_log = cond_term

                    block_cond_logs[b_idx] = b_cond_log

                    # Log to Block CSV
                    b_states = states[b_idx*BLOCK_LENGTH : (b_idx+1)*BLOCK_LENGTH]
                    b_rho_realized = np.mean(rhos[b_idx*BLOCK_LENGTH : (b_idx+1)*BLOCK_LENGTH])
                    b_raw_meanI = np.mean(batch_morans_i_toroidal_8(b_states))
                    b_persist_grid = np.mean(b_states, axis=0)
                    b_raw_persistI = calculate_morans_i_toroidal_8(b_persist_grid)

                    block_results.append({
                        "run_id": run_id,
                        "block_idx": b_idx,
                        "M_block": round(M_m, 4),
                        "g_E_value": round(g_E, 4),
                        "cond_logit_term": round(b_cond_log, 4),
                        "realized_block_rho": round(b_rho_realized, 4),
                        "raw_Psi_meanI_state_block": round(b_raw_meanI, 4),
                        "raw_Psi_persistence_I_block": round(b_raw_persistI, 4)
                    })

                # Correction 2: Sanitized NPZ filename
                npz_path = os.path.join(out_dir, f"c3_w2_rule_e_states_{run_id}.npz")
                np.savez_compressed(npz_path, states=states)

                # Window evaluations (step 25, len 100)
                for w_start in range(0, TICKS_PER_RUN - WINDOW_LENGTH + 1, WINDOW_STEP):
                    w_end = w_start + WINDOW_LENGTH
                    window_states = states[w_start:w_end]
                    window_rhos = rhos[w_start:w_end]

                    drift, cv, range_over, mean_rho, steady_cand, lifted_cand = evaluate_window_ss(window_rhos)

                    tick_Is = batch_morans_i_toroidal_8(window_states)
                    psi_meanI_state = np.mean(tick_Is)
                    psi_meanI_state_z = compute_meanI_state_null(window_states, psi_meanI_state)

                    persistence_grid = np.mean(window_states, axis=0)
                    psi_persistence_I = calculate_morans_i_toroidal_8(persistence_grid)
                    psi_persistence_I_z = compute_persistence_null(persistence_grid, psi_persistence_I)

                    mean_active_state_variance = np.mean([np.var(g) for g in window_states])
                    persistence_std = np.std(persistence_grid)

                    extinction_deg = bool(mean_rho <= LIFTED_THRESHOLD)
                    saturation_deg = bool((mean_rho >= 0.95) or (mean_active_state_variance < VAR_EPSILON))

                    low_low_nondeg = bool(
                        lifted_cand and
                        (not extinction_deg) and
                        (not saturation_deg) and
                        (abs(psi_meanI_state_z) < LOW_Z_THRESH) and
                        (abs(psi_persistence_I_z) < LOW_Z_THRESH) and
                        (mean_active_state_variance >= VAR_EPSILON)
                    )

                    window_results.append({
                        "run_id": run_id,
                        "base_sign": base_sign,
                        "kappa": kappa_val,
                        "target_d": target_d,
                        "alpha": round(alpha_val, 4),
                        "seed": seed,
                        "window_start": w_start,
                        "Psi_meanI_state": round(psi_meanI_state, 4),
                        "Psi_meanI_state_z": round(psi_meanI_state_z, 4),
                        "Psi_persistence_I": round(psi_persistence_I, 4),
                        "Psi_persistence_I_z": round(psi_persistence_I_z, 4),
                        "relative_drift": round(drift, 4),
                        "rho_cv": round(cv, 4),
                        "rho_range_over_mean": round(range_over, 4),
                        "mean_rho": round(mean_rho, 4),
                        "Steady_State_Candidate": "True" if steady_cand else "False",
                        "Lifted_Activation_Candidate": "True" if lifted_cand else "False",
                        "mean_active_state_variance": round(mean_active_state_variance, 4),
                        "persistence_std": round(persistence_std, 4),
                        "extinction_degenerate": "True" if extinction_deg else "False",
                        "saturation_degenerate": "True" if saturation_deg else "False",
                        "LowLow_Nondegenerate_Candidate": "True" if low_low_nondeg else "False"
                    })

    df_windows = pd.DataFrame(window_results)
    csv_windows = os.path.join(out_dir, "c3_w2_rule_e_windows.csv")
    df_windows.to_csv(csv_windows, index=False)

    df_blocks = pd.DataFrame(block_results)
    csv_blocks = os.path.join(out_dir, "c3_w2_rule_e_blocks.csv")
    df_blocks.to_csv(csv_blocks, index=False)

if __name__ == "__main__":
    execute_rule_e()
