#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cycle 3, Wave Two: Rule D (Turnover-Limited Activation) - R3 Amendment
Topology: 50x50, Toroidal, Moore Radius 1
Observables: Psi_meanI_state, Psi_persistence_I (co-equal pair)

Purpose: Establish the behavioral map of the Rule D instrument to test whether 
independent active-cell turnover can produce lifted, non-degenerate near-null 
observables at responsive local coupling. 

Mechanism (R3): Turnover is a layered hazard. Active cells survive with Rule C's 
Lambda-survival probability AND independently survive the turnover hazard. At 
theta_turnover = 0, the rule perfectly recovers the M2 Rule C signed regime.

The run will produce outputs for the matched-coupling bracket at Lambda 0.40. 
Success (satisfying the matched-coupling bracket) supports the mechanism class. 
Failure fails to produce the mechanism.

Apparatus Parity: Tests local reimplementations against the validated c3_ctl_001_battery 
and c3_ss_001_battery modules to ensure byte-for-byte mathematical equivalence.
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
TICKS_PER_RUN = 200        
WINDOW_LENGTH = 100        
WINDOW_STEP = 25           
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
# Rule D (R3) Grid Configuration
# ==========================================
LAMBDA_ANCHOR = 0.40

# Rule C M2 Survival Probability Baseline at Lambda=0.40
S_LAMBDA = 0.40 

# Target c = +/- 0.35 at Lambda = 0.40
# M2 Precomputed specific kappa constants
KAPPA_VALS = [
    (-0.35, -0.7599),
    (0.35,  0.7599)
]

THETA_VALS = [0.0, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50]

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

        np.random.seed(PARITY_SEED)
        test_grid_2d = np.random.randint(0, 2, size=(50, 50))
        actual_I_persist = calculate_morans_i_toroidal_8(test_grid_2d)

        np.random.seed(PARITY_SEED)
        local_z_persist = compute_persistence_null(test_grid_2d, actual_I_persist)
        np.random.seed(PARITY_SEED)
        ctl_z_persist, _ = ctl.compute_persistence_null(test_grid_2d, actual_I_persist)
        assert np.isclose(local_z_persist, ctl_z_persist)

        np.random.seed(PARITY_SEED)
        test_grids_3d = np.random.randint(0, 2, size=(100, 50, 50))
        actual_meanI = np.mean(batch_morans_i_toroidal_8(test_grids_3d))

        np.random.seed(PARITY_SEED)
        local_z_meanI = compute_meanI_state_null(test_grids_3d, actual_meanI)
        np.random.seed(PARITY_SEED)
        ctl_z_meanI, _ = ctl.compute_meanI_state_null(test_grids_3d, actual_meanI)
        assert np.isclose(local_z_meanI, ctl_z_meanI)
        
    except AssertionError as e:
        raise RuntimeError(f"PRE-FLIGHT FAIL: Parity check broken. Reimplementation diverges. {e}")
    except Exception as e:
        raise RuntimeError(f"PRE-FLIGHT FAIL: Parity check execution error: {e}")
    finally:
        sys.path.pop(0)

# ==========================================
# Rule D (R3) Logic
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

def calculate_realized_delta_p(p_Lambda, kappa):
    """Computes realized delta p: p_become(q=1) - p_become(q=0)."""
    logit_p = np.log(p_Lambda / (1.0 - p_Lambda))
    q1_term = logit_p + kappa * (2.0 * 1.0 - 1.0)
    q0_term = logit_p + kappa * (2.0 * 0.0 - 1.0)
    p_become_q1 = 1.0 / (1.0 + np.exp(-q1_term))
    p_become_q0 = 1.0 / (1.0 + np.exp(-q0_term))
    return p_become_q1 - p_become_q0

def step_rule_d_r3(grid, p_Lambda, s_Lambda, kappa, theta_turnover):
    """
    Rule D (R3 Amendment) transition:
    - Becoming-active (0 -> 1) uses Rule C logit-linear coupling.
    - Staying-active (1 -> 1) uses s_Lambda multiplied by (1 - theta_turnover).
    Returns the new grid and diagnostic scalars for live-coupling guards.
    """
    neighbors = get_neighbor_count(grid)
    q_matrix = neighbors / 8.0
    g_q = 2.0 * q_matrix - 1.0
    
    logit_p = np.log(p_Lambda / (1.0 - p_Lambda))
    p_become_matrix = 1.0 / (1.0 + np.exp(-(logit_p + kappa * g_q)))
    
    q_mean = np.mean(q_matrix)
    q_var = np.var(q_matrix)
    mean_abs_perturbation = np.mean(np.abs(p_become_matrix - p_Lambda))
    
    rand_grid = np.random.rand(GRID_SIZE, GRID_SIZE)
    
    # Update fence: synchronous update from t-state, layered R3 hazard
    becomes_active = (grid == 0) & (rand_grid < p_become_matrix)
    
    effective_persistence = s_Lambda * (1.0 - theta_turnover)
    stays_active = (grid == 1) & (rand_grid < effective_persistence)
    
    active_count = np.sum(grid == 1)
    churn_count = np.sum((grid == 1) & ~stays_active)
    realized_churn_rate = (churn_count / active_count) if active_count > 0 else 0.0
    
    new_grid = (becomes_active | stays_active).astype(int)
    
    return new_grid, q_mean, q_var, mean_abs_perturbation, realized_churn_rate, effective_persistence

# ==========================================
# Execution Pipeline
# ==========================================

def execute_rule_d_r3():
    run_parity_check()
    
    out_dir = os.path.join("cycle3", "data_out")
    os.makedirs(out_dir, exist_ok=True)
    
    results = []
    
    for target_c, kappa in KAPPA_VALS:
        realized_delta_p = calculate_realized_delta_p(LAMBDA_ANCHOR, kappa)
        
        for theta_turnover in THETA_VALS:
            for seed in SEEDS:
                np.random.seed(seed)
                random.seed(seed)
                
                # Fixed Initialization (0.10 activation density)
                flat_grid = np.zeros(N_CELLS, dtype=int)
                flat_grid[:INIT_ACTIVE_CELLS] = 1
                np.random.shuffle(flat_grid)
                grid = flat_grid.reshape((GRID_SIZE, GRID_SIZE))
                
                states = np.zeros((TICKS_PER_RUN, GRID_SIZE, GRID_SIZE), dtype=int)
                rhos = np.zeros(TICKS_PER_RUN)
                
                q_means = np.zeros(TICKS_PER_RUN)
                q_vars = np.zeros(TICKS_PER_RUN)
                mean_abs_perts = np.zeros(TICKS_PER_RUN)
                churn_rates = np.zeros(TICKS_PER_RUN)
                
                # effective_persistence is mathematically constant per-setting, 
                # calculated locally in the transition step, grabbed once below.
                run_effective_persistence = 0.0
                
                for t in range(TICKS_PER_RUN):
                    states[t] = grid
                    rhos[t] = np.mean(grid)
                    
                    grid, q_m, q_v, abs_pert, churn, eff_persist = step_rule_d_r3(
                        grid, LAMBDA_ANCHOR, S_LAMBDA, kappa, theta_turnover
                    )
                    
                    q_means[t] = q_m
                    q_vars[t] = q_v
                    mean_abs_perts[t] = abs_pert
                    churn_rates[t] = churn
                    run_effective_persistence = eff_persist
                
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
                    
                    win_q_mean = np.mean(q_means[w_start:w_end])
                    win_q_var = np.mean(q_vars[w_start:w_end])
                    win_mean_abs_pert = np.mean(mean_abs_perts[w_start:w_end])
                    win_churn_rate = np.mean(churn_rates[w_start:w_end])
                    
                    results.append({
                        "Lambda_anchor": LAMBDA_ANCHOR,
                        "kappa": kappa,
                        "target_c": target_c,
                        "s_Lambda": S_LAMBDA,
                        "theta_turnover": theta_turnover,
                        "effective_persistence": round(run_effective_persistence, 4),
                        "realized_delta_p": round(realized_delta_p, 4),
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
                        "LowLow_Nondegenerate_Candidate": "True" if low_low_nondeg else "False",
                        "q_mean": round(win_q_mean, 4),
                        "q_var": round(win_q_var, 4),
                        "mean_abs_perturbation": round(win_mean_abs_pert, 4),
                        "realized_churn_rate": round(win_churn_rate, 4)
                    })

    df_results = pd.DataFrame(results)
    csv_path = os.path.join(out_dir, "c3_w2_rule_d_r3_results.csv")
    df_results.to_csv(csv_path, index=False)

if __name__ == "__main__":
    execute_rule_d_r3()
