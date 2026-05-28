# Layer 2 - C3-SS-001 substantive review request

Layer 2, requesting substantive review of the C3-SS-001 steady-state apparatus design. The apparatus has cleared Layer 1 implementation review on the script and Layer 1 sufficiency-testing on the canonical CSV - both at the flag level. Three design-tightness concerns are surfaced below for your judgment before the gate advances to valid-L2.

## Cycle 3 context

Two of three Cycle 3 precondition gates are cleared (C3-ENV-001 passed-L1, C3-CTL-001 valid-L2). C3-SS-001 is the third and final precondition gate before any real-substrate value can be read as Regime II. The substantive probe phase opens only after this gate clears. The held probe-design inputs at `cycle3/PROBE_DESIGN_INPUTS_HELD.md` come off the shelf only when that phase opens.

The apparatus validates the "earned steady-state window" criterion - a window of rho(t) is earned-steady-and-lifted when, independently: mean rho exceeds a lifted threshold, AND rho is stable across the window (no drift, no excessive CV, no large range). Three filters (relative_drift, rho_cv, rho_range_over_mean) test steadiness; one threshold (mean rho > 0.05) tests lifted activation. Two output flags (Steady_State_Candidate, Lifted_Activation_Candidate) carry the per-window verdict.

## What was specified, drafted, and run

**Contract specification:** six minimum cases with Layer 3 latitude on filter mathematical definitions, threshold values, trajectory/window/step parameters, and trajectory-shape specifics. Cases 5 and 6 forced the apparatus to be windowed (multiple sliding positions per trajectory) - whole-trajectory analysis could not discriminate them.

**Layer 3 draft and execution chain:**
- Script: `cycle3/c3_ss_001_battery.py` (drafted by Layer 3, run by Mike on the captured C3-ENV-001 environment - top-level venv, Python 3.14.4, numpy 2.4.4).
- CSV: `cycle3/data_out/c3_ss_001_results.csv` (run-of-record).
- Layer 3 also routed an interpretation back, initially in L2-clearance language; reframed at Layer 1's pushback into predicted-output language Layer 1 could sufficiency-test against.

**Open design parameters as settled by Layer 3:**

- Trajectory length 200 ticks; window length 100 ticks (matching CTL-001); sliding step 25 ticks (5 windows per trajectory).
- Seed = 42.
- Filter definitions (exactly as implemented):
  - `relative_drift = abs(slope) * window_length / mean_rho`, slope from `np.polyfit(t, rho_window, 1)`.
  - `rho_cv = std(rho_window) / mean_rho`, using `np.std` (population std, ddof=0).
  - `rho_range_over_mean = (max(rho) - min(rho)) / mean_rho`.
- Thresholds: drift < 0.10; cv < 0.10; range_over_mean < 0.25; lifted > 0.05.
- Trajectory shapes per case (see "Implementation" section below).

## Implementation (full script content)

```python
import numpy as np
import pandas as pd
import os

# C3-SS-001: Steady-State Synthetic Battery
# Validates time-window filtering machinery

SEED = 42
TRAJECTORY_LENGTH = 200
WINDOW_LENGTH = 100
WINDOW_STEP = 25
LIFTED_THRESHOLD = 0.05

THRESH_RELATIVE_DRIFT = 0.10
THRESH_RHO_CV = 0.10
THRESH_RHO_RANGE_OVER_MEAN = 0.25

np.random.seed(SEED)

def get_noise(length, amplitude=0.005):
    return np.random.uniform(-amplitude, amplitude, length)

def case_1_flat_lifted():
    return 0.20 + get_noise(TRAJECTORY_LENGTH)

def case_2_monotone_drift():
    t = np.arange(TRAJECTORY_LENGTH)
    return 0.10 + (0.15 / TRAJECTORY_LENGTH) * t + get_noise(TRAJECTORY_LENGTH)

def case_3_high_wobble():
    t = np.arange(TRAJECTORY_LENGTH)
    return 0.20 + 0.08 * np.sin(2 * np.pi * t / 20) + get_noise(TRAJECTORY_LENGTH)

def case_4_low_trivial():
    return 0.02 + get_noise(TRAJECTORY_LENGTH, amplitude=0.002)

def case_5_late_stabilization():
    rho = np.zeros(TRAJECTORY_LENGTH)
    t = np.arange(100)
    rho[0:100] = 0.10 + (0.20 / 100) * t + get_noise(100)
    rho[100:200] = 0.30 + get_noise(100)
    return rho

def case_6_step_transition():
    rho = np.zeros(TRAJECTORY_LENGTH)
    rho[0:100] = 0.15 + get_noise(100)
    rho[100:200] = 0.35 + get_noise(100)
    return rho

def evaluate_window(rho_window):
    mean_rho = np.mean(rho_window)
    epsilon = 1e-9
    t = np.arange(WINDOW_LENGTH)
    slope, _ = np.polyfit(t, rho_window, 1)
    relative_drift = (abs(slope) * WINDOW_LENGTH) / (mean_rho + epsilon)
    rho_cv = np.std(rho_window) / (mean_rho + epsilon)
    rho_range_over_mean = (np.max(rho_window) - np.min(rho_window)) / (mean_rho + epsilon)
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

# (run_battery loops cases x window positions, writes CSV. Code identical to evaluation pattern above; full file on disk.)
```

## Canonical CSV (the actual run, 30 rows)

```
Case,Window_Start,Window_End,Mean_Rho,Relative_Drift,Rho_CV,Rho_Range_Over_Mean,Steady_State_Candidate,Lifted_Activation_Candidate
1_flat_lifted,0,100,0.1997,0.001,0.0148,0.0491,True,True
1_flat_lifted,25,125,0.1999,0.0013,0.0151,0.0491,True,True
1_flat_lifted,50,150,0.1999,0.0042,0.015,0.0491,True,True
1_flat_lifted,75,175,0.1997,0.0021,0.0142,0.049,True,True
1_flat_lifted,100,200,0.2,0.004,0.0146,0.0489,True,True
2_monotone_drift,0,100,0.1373,0.5484,0.1597,0.5691,False,True
2_monotone_drift,25,125,0.1562,0.4709,0.1372,0.5208,False,True
2_monotone_drift,50,150,0.1745,0.4194,0.1221,0.4445,False,True
2_monotone_drift,75,175,0.1929,0.3856,0.1123,0.3904,False,True
2_monotone_drift,100,200,0.212,0.3592,0.1046,0.3833,False,True
3_high_wobble,0,100,0.2002,0.1487,0.285,0.829,False,True
3_high_wobble,25,125,0.2004,0.0144,0.2865,0.8444,False,True
3_high_wobble,50,150,0.2006,0.1571,0.2837,0.8412,False,True
3_high_wobble,75,175,0.2007,0.0194,0.2818,0.841,False,True
3_high_wobble,100,200,0.2003,0.1656,0.2813,0.8271,False,True
4_low_trivial,0,100,0.0197,0.0145,0.0539,0.196,True,False
4_low_trivial,25,125,0.0198,0.0227,0.0556,0.1956,True,False
4_low_trivial,50,150,0.0199,0.0314,0.0557,0.1884,True,False
4_low_trivial,75,175,0.02,0.0077,0.0566,0.1908,True,False
4_low_trivial,100,200,0.0201,0.015,0.0561,0.1934,True,False
5_late_stabilization,0,100,0.1986,0.9984,0.2886,1.0044,False,True
5_late_stabilization,25,125,0.2425,0.7032,0.2064,0.6352,False,True
5_late_stabilization,50,150,0.2739,0.3749,0.1207,0.3985,False,True
5_late_stabilization,75,175,0.293,0.1131,0.0477,0.1989,False,True
5_late_stabilization,100,200,0.2997,0.0005,0.0092,0.0325,True,True
6_step_transition,0,100,0.1503,0.0087,0.0204,0.0652,True,True
6_step_transition,25,125,0.2002,1.1276,0.4344,1.0476,False,True
6_step_transition,50,150,0.2504,1.1978,0.4,0.8377,False,True
6_step_transition,75,175,0.3005,0.7503,0.289,0.6958,False,True
6_step_transition,100,200,0.3505,0.0,0.0085,0.0282,True,True
```

## Layer 1 sufficiency-test verdict

30/30 rows produce the predicted (Steady_State_Candidate, Lifted_Activation_Candidate) pair. Per the contract's L2 acceptance criterion (row-by-row alignment, not aggregate), the criterion is met at the flag level. The apparatus produces the designed six-case discrimination on the canonical run.

## Three concerns surfaced for Layer 2

### Concern 1 - Case 2 fires all three filters, not just drift

A monotone linear drift produces elevated CV and elevated Range alongside the drift slope. Window 0 of Case 2: Drift 0.548, CV 0.160, Range 0.569 - all three over their thresholds. This is structural - a linear ramp's standard deviation scales with the slope (sigma ~ slope * window_length / sqrt(12)) and its range equals slope * window_length. Removing the drift filter would not change Case 2's outcome, because CV and Range still fire.

The contract intent was that "each case discriminates a specific apparatus failure mode." The actual situation: Case 2 does not uniquely test the drift filter. The flag outcome is correct, but the discrimination structure is weaker than the contract implied.

### Concern 2 - Case 3 drift residual breaks the "pure CV/Range failure" intent

Case 3 uses a sine wave of period 20 ticks in a 100-tick window: 99/20 = 4.95 periods per window, not exactly 5. The 0.05-period phase residual produces nonzero linear-regression slope dependent on window starting phase. Result:

| Window | Actual Drift |
|---|---|
| 0 | 0.149 (fires, > 0.10) |
| 25 | 0.014 (does not fire) |
| 50 | 0.157 (fires) |
| 75 | 0.019 (does not fire) |
| 100 | 0.166 (fires) |

In 3 of 5 windows, drift trips alongside CV and Range. Same flag outcome (F, T) in all windows, but Case 3 no longer uniquely tests the CV/Range filters. A period of 25 ticks would give exactly 4 periods per window and remove the residual by symmetry.

### Concern 3 - Case 4 margins are tight, especially CV

Case 4 (low trivial activity) actuals:
- Mean_Rho ~0.02 vs Lifted threshold 0.05 (margin 0.03, fails lifted - correct).
- Drift ~0.008-0.031 vs threshold 0.10 (passes, margin ~0.07).
- CV ~0.054-0.057 vs threshold 0.10 (passes, **margin ~0.044**).
- Range ~0.188-0.196 vs threshold 0.25 (passes, **margin ~0.054**).

The CV margin (~0.044) and Range margin (~0.054) are the narrowest in the design. With seed=42 and noise amplitude +/- 0.002 this is stable, but Case 4 has the least robustness against noise-amplitude or seed variation. A noise amplitude of +/- 0.001 would tighten CV to ~0.028 and Range to ~0.10 - cleaner separation from threshold without affecting the trivial-activity property.

## Questions for Layer 2

1. **Filter-isolation versus flag-outcome.** The flag outcomes are correct on every row, but Cases 2 and 3 no longer uniquely test their named filters. Does the loss of per-filter isolation constitute a substantive design weakness worth correcting before valid-L2, or is row-level flag correctness sufficient for the L2 measurement-validity criterion as stated?

2. **Margins on Case 4.** Is the CV margin of ~0.044 adequate for a measurement-validity gate, or should Case 4's noise amplitude be tightened to widen the margin?

3. **Battery extension.** The contract permitted Layer 3 to add cases beyond the six if the additions strengthen discrimination. Layer 3 did not. Would a 7th case be useful - one that fails ONLY on drift (small slope, very low CV/Range) and an 8th that fails ONLY on CV (high-frequency sine with whole periods to zero out drift residual)? These would restore per-filter isolation without changing what already works.

4. **Anything else.** Open question to Layer 2 on validity grounds - implementation correctness Layer 1 has covered; what we need from you is substantive design judgment.

## Routing

Layer 2 returns verdict and any requested adjustments to Mike. Three possible outcomes:

(a) Substantive design accepted as-is. Layer 1 fills the test record's Post-execution block, registry advances valid-L2, third precondition gate clears.

(b) Margin tightening on Case 4 only (no structural change). Layer 3 produces a one-line patch, Mike re-runs, Layer 1 re-verifies the CSV. Minor delay.

(c) Battery extension or case-shape revision (Concerns 1 and 2). Layer 3 produces a revised script, Mike re-runs, Layer 1 re-reviews end-to-end. Substantial revision; the current CSV becomes superseded; clean re-pass required.

The substantive call is Layer 2's. Layer 1 has no opinion to push - the three concerns are surfaced honestly, and substantively any of (a), (b), (c) is defensible.

## Vocabulary (binding)

- rho = activation density. Psi = coherence (not used in this gate by construction). Lambda = structural conduciveness (not used in this gate).
- "earned steady-state window" - the operational target.
- Candidates **produce** or **fail to produce**; never "confirm" or "demonstrate".
- "fraction of active neighbors" is fine (local); never "fraction of the population".
- Agents act (no decision / optimization / utility / cognitive language); not directly applicable to this gate, but the discipline holds across the project.
