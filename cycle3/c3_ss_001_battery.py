import numpy as np
import pandas as pd
import os

# ==========================================
# C3-SS-001: Steady-State Synthetic Battery
# Validates time-window filtering machinery
# ==========================================

# Open Design Parameters
SEED = 42
TRAJECTORY_LENGTH = 200
WINDOW_LENGTH = 100
WINDOW_STEP = 25
LIFTED_THRESHOLD = 0.05

# Filter Thresholds
THRESH_RELATIVE_DRIFT = 0.10
THRESH_RHO_CV = 0.10
THRESH_RHO_RANGE_OVER_MEAN = 0.25

np.random.seed(SEED)

def get_noise(length, amplitude=0.005):
    return np.random.uniform(-amplitude, amplitude, length)

# ==========================================
# Case Generators
# ==========================================

def case_1_flat_lifted():
    """Flat lifted steady state. Expected: All windows pass steady and lifted."""
    return 0.20 + get_noise(TRAJECTORY_LENGTH)

def case_2_monotone_drift():
    """Monotone drift. Expected: All windows fail steady (drift exceeds threshold)."""
    t = np.arange(TRAJECTORY_LENGTH)
    return 0.10 + (0.15 / TRAJECTORY_LENGTH) * t + get_noise(TRAJECTORY_LENGTH)

def case_3_high_wobble():
    """High wobble, near-zero slope. Expected: All windows fail steady (CV and Range exceed)."""
    t = np.arange(TRAJECTORY_LENGTH)
    return 0.20 + 0.08 * np.sin(2 * np.pi * t / 20) + get_noise(TRAJECTORY_LENGTH)

def case_4_low_trivial():
    """Low trivial activity. Expected: All windows pass steady, fail lifted."""
    return 0.02 + get_noise(TRAJECTORY_LENGTH, amplitude=0.002)

def case_5_late_stabilization():
    """Late stabilization. Expected: Early windows fail steady; window 100 passes steady and lifted."""
    rho = np.zeros(TRAJECTORY_LENGTH)
    t = np.arange(100)
    rho[0:100] = 0.10 + (0.20 / 100) * t + get_noise(100) # Drifting early
    rho[100:200] = 0.30 + get_noise(100)                  # Flat late
    return rho

def case_6_step_transition():
    """Step transition. Expected: Windows overlapping t=100 fail steady; independent plateaus pass steady."""
    rho = np.zeros(TRAJECTORY_LENGTH)
    rho[0:100] = 0.15 + get_noise(100)
    rho[100:200] = 0.35 + get_noise(100)
    return rho

# ==========================================
# Filter Mathematics
# ==========================================

def evaluate_window(rho_window):
    mean_rho = np.mean(rho_window)
    epsilon = 1e-9 # Prevent division by zero
    
    # 1. Relative Drift
    t = np.arange(WINDOW_LENGTH)
    slope, _ = np.polyfit(t, rho_window, 1)
    relative_drift = (abs(slope) * WINDOW_LENGTH) / (mean_rho + epsilon)
    
    # 2. Coefficient of Variation
    rho_cv = np.std(rho_window) / (mean_rho + epsilon)
    
    # 3. Range over Mean
    rho_range_over_mean = (np.max(rho_window) - np.min(rho_window)) / (mean_rho + epsilon)
    
    # Candidate Flags
    steady_state_candidate = (
        (relative_drift < THRESH_RELATIVE_DRIFT) and
        (rho_cv < THRESH_RHO_CV) and
        (rho_range_over_mean < THRESH_RHO_RANGE_OVER_MEAN)
    )
    lifted_activation_candidate = mean_rho > LIFTED_THRESHOLD
    
    return {
        "Mean_Rho": mean_rho,
        "Relative_Drift": relative_drift,
        "Rho_CV": rho_cv,
        "Rho_Range_Over_Mean": rho_range_over_mean,
        "Steady_State_Candidate": steady_state_candidate,
        "Lifted_Activation_Candidate": lifted_activation_candidate
    }

# ==========================================
# Execution Pipeline
# ==========================================

def run_battery():
    cases = {
        "1_flat_lifted": case_1_flat_lifted(),
        "2_monotone_drift": case_2_monotone_drift(),
        "3_high_wobble": case_3_high_wobble(),
        "4_low_trivial": case_4_low_trivial(),
        "5_late_stabilization": case_5_late_stabilization(),
        "6_step_transition": case_6_step_transition()
    }
    
    window_starts = list(range(0, TRAJECTORY_LENGTH - WINDOW_LENGTH + 1, WINDOW_STEP))
    results = []
    
    for case_name, trajectory in cases.items():
        for w_start in window_starts:
            w_end = w_start + WINDOW_LENGTH
            rho_window = trajectory[w_start:w_end]
            
            metrics = evaluate_window(rho_window)
            
            row = {
                "Case": case_name,
                "Window_Start": w_start,
                "Window_End": w_end,
                "Mean_Rho": round(metrics["Mean_Rho"], 4),
                "Relative_Drift": round(metrics["Relative_Drift"], 4),
                "Rho_CV": round(metrics["Rho_CV"], 4),
                "Rho_Range_Over_Mean": round(metrics["Rho_Range_Over_Mean"], 4),
                "Steady_State_Candidate": metrics["Steady_State_Candidate"],
                "Lifted_Activation_Candidate": metrics["Lifted_Activation_Candidate"]
            }
            results.append(row)
            
    df_results = pd.DataFrame(results)
    
    output_dir = os.path.join("cycle3", "data_out")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "c3_ss_001_results.csv")
    df_results.to_csv(out_path, index=False)
    
    print("\n--- C3-SS-001 Steady-State Battery Execution Complete ---")
    print(f"Evaluated {len(results)} windows across {len(cases)} cases.")
    print(f"Results saved to {out_path}")

if __name__ == "__main__":
    run_battery()