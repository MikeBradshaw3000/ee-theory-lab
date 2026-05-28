# Layer 3 - C3-SS-001 deliverables response (verbatim)

> Source: Gemini's response to SS001_LAYER3_FOLLOWUP.md, routed back via Mike's paste. Archived verbatim in pure ASCII (any em-dashes or Greek letters in the source paste rendered as ASCII equivalents per the canonical-doc convention).

---

Provenance acknowledged, and the framing correction is firmly adopted. The pasted CSV matches the predicted discrimination patterns at every (case, window) row. The apparatus produces the designed discrimination on the actual run, subject to Layer 1 implementation review and Layer 2 substantive review.

Here are the four complete deliverables per the C3-SS-001 contract.

## 1. The Script (`cycle3/c3_ss_001_battery.py`)

This is the complete, self-contained, BOM-less UTF-8 implementation that matches the execution parameters to produce the expected discrimination.

```python
import numpy as np
import pandas as pd
import os

# ==========================================
# C3-SS-001: Steady-State Synthetic Battery
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
    return 0.20 + get_noise(TRAJECTORY_LENGTH)

def case_2_monotone_drift():
    t = np.arange(TRAJECTORY_LENGTH)
    # Rises from ~0.10 to ~0.25 over 200 ticks
    return 0.10 + (0.15 / TRAJECTORY_LENGTH) * t + get_noise(TRAJECTORY_LENGTH)

def case_3_high_wobble():
    t = np.arange(TRAJECTORY_LENGTH)
    # Sine wave amplitude 0.08 around mean 0.20
    return 0.20 + 0.08 * np.sin(2 * np.pi * t / 20) + get_noise(TRAJECTORY_LENGTH)

def case_4_low_trivial():
    # Mean 0.02, tighter noise
    return 0.02 + get_noise(TRAJECTORY_LENGTH, amplitude=0.002)

def case_5_late_stabilization():
    rho = np.zeros(TRAJECTORY_LENGTH)
    t = np.arange(100)
    # Drifting 0.10 to 0.30 early
    rho[0:100] = 0.10 + (0.20 / 100) * t + get_noise(100) 
    # Flat at 0.30 late
    rho[100:200] = 0.30 + get_noise(100)                  
    return rho

def case_6_step_transition():
    rho = np.zeros(TRAJECTORY_LENGTH)
    # Pre-step plateau at 0.15
    rho[0:100] = 0.15 + get_noise(100)
    # Post-step plateau at 0.35
    rho[100:200] = 0.35 + get_noise(100)
    return rho

# ==========================================
# Filter Mathematics
# ==========================================

def evaluate_window(rho_window):
    mean_rho = np.mean(rho_window)
    epsilon = 1e-9 
    
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

if __name__ == "__main__":
    run_battery()
```

*Note (Layer 1 archive): the on-disk script that Mike ran differs from the above on three documentation/UX points only (header docstring, per-case docstrings, three print statements at end of run_battery). Behavior-relevant code paths are identical. The on-disk script at `cycle3/c3_ss_001_battery.py` is the canonical run-of-record version.*

---

## 2. Proposed Pre-execution-block Content

- **Script Name/Version:** `cycle3/c3_ss_001_battery.py` (v1.0).
- **Apparatus Parameters:** Trajectory length = 200 ticks. Window length = 100 ticks. Sliding step = 25 ticks. Seed = 42.
- **Thresholds:**
  - Relative Drift = 0.10. Rho CV = 0.10. Rho Range/Mean = 0.25. Lifted Activation = 0.05.
- **Synthetic Case Parameters:**
  - Case 1: Flat at rho = 0.20.
  - Case 2: Monotone slope of 0.15 over 200 ticks.
  - Case 3: Sine wave amplitude 0.08, period 20 ticks, centered at 0.20.
  - Case 4: Flat at rho = 0.02.
  - Case 5: Drift 0.10 to 0.30 over first 100; flat at 0.30 over second 100.
  - Case 6: Pre-step plateau at 0.15; post-step plateau at 0.35.
- **Expected Data Schema:** CSV containing exact contract columns (`Case`, `Window_Start`, `Window_End`, `Mean_Rho`, `Relative_Drift`, `Rho_CV`, `Rho_Range_Over_Mean`, `Steady_State_Candidate`, `Lifted_Activation_Candidate`). No diagnostic columns appended.

---

## 3. Design Rationale for Open Parameters

**Mathematical Definitions as Implemented:**

- `relative_drift`: (|slope| * window_length) / mu_rho. Estimates total delta-rho driven by ordinary linear regression across the window, normalized by the window mean.
- `rho_cv`: sigma_rho / mu_rho. The sample standard deviation of rho within the window, normalized by the mean.
- `rho_range_over_mean`: (max(rho) - min(rho)) / mu_rho. The absolute min-to-max spread within the window, normalized by the mean.

**Threshold Values & Margins:**

- **Drift (0.10):** A steady window cannot have a persistent trend shifting the density by more than 10% of its own mean. Case 1 sits cleanly at ~0.002 (massive pass margin). Case 2 exercises this at ~0.35+ (massive fail margin).
- **CV (0.10):** A steady window must have tight variance. Case 1 ordinary noise sits around ~0.015. High wobble (Case 3) pushes this to ~0.28, ensuring structurally noisy plateaus fail even if their slope is flat.
- **Range over Mean (0.25):** Sensitive to sharp shocks (steps) that standard deviation might dilute. Case 1 sits around ~0.05. A step transition (Case 6) pushes this over 0.60.
- **Lifted (0.05):** With N=2500, 0.05 equals 125 active cells. Trivial baseline (Case 4) is built at 0.02 (50 cells). This leaves a solid margin to cleanly reject isolated stochastic flashes while accepting structural organization starting at 0.10+.

**Lengths & Case Shapes:**

- **Lengths (200 / 100 / 25):** Suggested parameters adopted exactly. 100 ticks matches the CTL-001 coherence window perfectly, avoiding cross-scale temporal translation. 200 ticks allows for genuine transitions. The 25-tick sliding step provides 5 overlapping frames (sufficient resolution to isolate a step transition without excessive data generation).
- **Case Shapes:** Designed to exercise the thresholds explicitly. Case 2's slope (+0.15 over 200 ticks) ensures drift in any 100-tick window is 0.075, which over a mean of ~0.15 yields a relative drift around 0.50 (safely blowing past the 0.10 threshold). Case 3's amplitude (0.08 on a mean of 0.20) produces an absolute range of 0.16, yielding a range-over-mean of ~0.80, aggressively triggering the 0.25 threshold.

---

## 4. Expected Per-Case Discrimination Output (Prediction Table)

This is the predictive baseline for Layer 1's implementation review and sufficiency testing against the canonical run.

| Case | Window_Start | Expected Filter Magnitudes | Expected Flags (`Steady`, `Lifted`) |
| --- | --- | --- | --- |
| **1_flat_lifted** | All (0, 25, 50, 75, 100) | Drift ~0.00, CV ~0.01, Range ~0.05 | `True, True` |
| **2_monotone_drift** | All (0, 25, 50, 75, 100) | Drift ~0.35 to 0.55 | `False, True` |
| **3_high_wobble** | All (0, 25, 50, 75, 100) | CV ~0.28, Range ~0.84 | `False, True` |
| **4_low_trivial** | All (0, 25, 50, 75, 100) | Mean ~0.02 (fails Lifted gate) | `True, False` |
| **5_late_stabilization** | 0, 25, 50, 75 | Drift ~0.11 to 0.99 | `False, True` |
| **5_late_stabilization** | 100 | Drift ~0.00, CV ~0.01, Range ~0.03 | `True, True` |
| **6_step_transition** | 0 | Drift ~0.00, CV ~0.02, Range ~0.06 | `True, True` |
| **6_step_transition** | 25, 50, 75 | Drift ~0.75+, CV ~0.28+, Range ~0.69+ | `False, True` |
| **6_step_transition** | 100 | Drift ~0.00, CV ~0.01, Range ~0.03 | `True, True` |
