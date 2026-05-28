# C3-SS-001 - Design / Implementation Contract for Layer 3

## Cycle 3 context (orientation)

Two of three Cycle 3 precondition gates are cleared:

- **C3-ENV-001** passed-L1: canonical environment captured (top-level venv, Python 3.14.4, Mesa 3.5.1, numpy pinned 2.4.4).
- **C3-CTL-001** valid-L2: the synthetic control battery (`cycle3/c3_ctl_001_battery.py`) at the locked 50x50 toroidal Moore-1 topology produces the designed five-case discrimination on both observables (Psi_meanI_state, Psi_persistence_I), each grounded against its own grid-local permutation null.

**C3-SS-001** is the third and final precondition gate. It is the last apparatus check before any real-substrate value can be read as Regime-II coherence. Opening it has been arbitrated. This contract is the design / implementation brief.

Origin/main: `e5530af`.

## Layer 3 capability boundary (binding)

Per the five-role taxonomy:

1. **Layer 3 implementation** - Gemini writes the script and proposes design parameters.
2. **Local execution** - Mike runs the script. Layer 3 does NOT execute against the substrate; Layer 3 has no local execution environment.
3. **Layer 3 output interpretation** - Gemini analyzes results Mike pastes back.
4. **Layer 1 synthesis / implementation review** - Claude reviews the implementation against the acceptance criteria, sufficiency-tested.
5. **Layer 2 substantive review** - ChatGPT reviews the design choices on validity grounds.

This contract requests roles 1 (and later 3). Deliverables are runnable code and design rationale, not execution results. A response that narrates execution is a category error.

## What SS-001 is for

SS-001 validates the apparatus that decides whether a window of rho(t) is an *earned steady-state window* with *lifted activation*. The validation is performed on synthetic rho(t) trajectories whose correct classification is known by construction.

"Earned steady-state window" (per the resume anchor and `cycle3/PROBE_DESIGN_INPUTS_HELD.md` Section 4) is the operational target. A window of rho(t) is earned-steady-and-lifted when, independently:

- **Lifted:** mean rho across the window exceeds a lifted threshold (activation has emerged above trivial baseline).
- **Steady:** rho is stable across the window - no sustained drift, no excessive variability, no large excursions.

Both conditions must hold independently. A window can be steady-but-not-lifted, or lifted-but-not-steady. Only when both hold does the window qualify as a *lifted earned steady-state window*.

SS-001 is precondition-gate machinery, equivalent in role to CTL-001 but for the time-window side. SS-001 explicitly does NOT touch real substrate. No ABM output, no parquet, no Mesa run. Synthetic rho(t) arrays only.

## Apparatus to be built

A synthetic battery script that:

1. Generates the six minimum cases of rho(t) trajectories with known behavior (Section "Six minimum cases" below).
2. Evaluates each trajectory at multiple sliding window positions (windowing is required - see "Windowing is required" below).
3. For each (case, window) pair, computes three filter values and two candidate flags.
4. Outputs a CSV summary, one row per (case, window) evaluation.

## Windowing is required

Cases 5 and 6 (late stabilization, step transition) require windowed evaluation - they cannot be discriminated by whole-trajectory analysis. The apparatus must apply each filter to multiple window positions across each trajectory.

Suggested starting point (Layer 3 may refine with justification):

- Trajectory length per case: 200 ticks.
- Window length: 100 ticks (matching CTL-001's window).
- Sliding window step: 25 ticks, yielding windows starting at t = 0, 25, 50, 75, 100; ending at t = 100, 125, 150, 175, 200. Five windows per trajectory.

For Cases 1-4, all five windows should produce the same result (the trajectory is positionally uniform). For Cases 5 and 6, the result varies across windows by design.

## The three window filters

Filter names (binding):

- `relative_drift` - detects sustained trend within the window.
- `rho_cv` - detects excessive variability around the mean within the window.
- `rho_range_over_mean` - detects large excursions within the window.

Mathematical definitions: Layer 3 to propose with justification. Suggested starting points (Layer 3 may refine):

- `relative_drift`: |slope| * window_length / mean(rho) - magnitude of total drift over the window, normalized by the window mean. Slope from ordinary linear regression on (tick_index, rho).
- `rho_cv`: std(rho) / mean(rho) - standard coefficient of variation over the window.
- `rho_range_over_mean`: (max(rho) - min(rho)) / mean(rho) - range over the window, normalized by the window mean.

Threshold values for each filter: Layer 3 to propose with justification. Thresholds must be chosen so the six-case discrimination works (see Section "L1 / L2 acceptance criteria").

## Two candidate output flags

- `steady_state_candidate` - TRUE when all three filter values within the window are below their thresholds.
- `lifted_activation_candidate` - TRUE when mean(rho) within the window exceeds the lifted threshold.

Lifted threshold value: Layer 3 to propose with justification. The threshold must distinguish "trivially nonzero baseline" from "substantively lifted activation." Suggested starting point: around rho = 0.05 (5% mean activation). Layer 3 to refine.

The two flags are independent: a window can be (steady, not lifted) - Case 4 - or (lifted, not steady) - Cases 2, 3, and early portions of Case 5.

## Six minimum cases (must produce the designed discrimination)

1. **Flat lifted steady state.** rho(t) at a lifted constant value plus minimal noise.
   - Expected: all windows produce (steady_state_candidate TRUE, lifted_activation_candidate TRUE).

2. **Monotone drift.** rho(t) climbing or falling steadily across the trajectory; trajectory mean at a lifted value.
   - Expected: all windows produce steady_state_candidate FALSE, with `relative_drift` exceeding its threshold.

3. **High wobble with near-zero slope.** rho(t) oscillating with large amplitude around a lifted mean, with mean-trend near zero.
   - Expected: all windows produce steady_state_candidate FALSE, with BOTH `rho_cv` AND `rho_range_over_mean` exceeding their thresholds.

4. **Low trivial activity.** rho(t) at a near-zero constant plus minimal noise.
   - Expected: all windows produce (steady_state_candidate TRUE, lifted_activation_candidate FALSE).

5. **Late stabilization.** rho(t) chaotic or drifting in the early portion of the trajectory, settling to a flat lifted plateau in the later portion.
   - Expected: early-positioned windows produce steady_state_candidate FALSE; late-positioned (plateau) windows produce (steady_state_candidate TRUE, lifted_activation_candidate TRUE). The window-position-dependent transition is the discrimination.

6. **Step transition.** rho(t) at one plateau (possibly low), then a sharp step, then a different (lifted) plateau.
   - Expected: windows whose span includes the step produce steady_state_candidate FALSE (the step shows up as drift, range, or both). Windows entirely within either plateau produce the designed pattern for that plateau (steady, with lifting depending on plateau level).

Layer 3 may add cases beyond these six if the additions strengthen discrimination against alternative apparatus designs (i.e., they discriminate the correct apparatus from a more permissive or more restrictive one). Justify additions briefly.

## L1 / L2 acceptance criteria

- **L1 (implementation):** the battery runs without error; outputs finite and well-formed.
- **L2 (measurement validity):** every (case, window) row in the output CSV matches the designed pass/fail pattern for that case and window position, per Section "Six minimum cases" above. The pass criterion is row-by-row alignment, not aggregate; the discrimination must produce on every case.

**Pessimistic-on-passing:** the six-case structure was chosen because each case discriminates a specific apparatus failure mode. Do not collapse cases, weaken the discrimination, or reduce the case set under any rationalization that "the remaining cases are sufficient." The acceptance criterion tests sufficiency case-by-case, not in aggregate.

## Levels NOT addressed (by construction)

- **L3 (steady-state eligibility on real substrate):** not applicable - this is the synthetic battery with no substrate involvement.
- **L4 (interpretation, Regime-II-as-structural):** not applicable - this gate is apparatus, not evidence.

## Interpretation boundary (declared in advance)

A pass establishes that the SS apparatus correctly discriminates the six designed cases on synthetic rho(t). It establishes:

- NOTHING about real-substrate values.
- NOTHING about whether any real ABM trajectory has earned steady-state.
- NOTHING about Regime-II coherence.
- NOTHING about which observable (Psi_meanI_state, Psi_persistence_I) is Regime-II coherence - that ontological question rides forward, unsettled, L4.

The classification of real-substrate windows is the work that opens only after this gate clears.

## Fixed conventions

- Script path: `cycle3/c3_ss_001_battery.py`
- Output CSV: `cycle3/data_out/c3_ss_001_results.csv`
- File encoding: BOM-less UTF-8 (canonical convention; do not add BOM).
- Run from repo root: `python cycle3\c3_ss_001_battery.py`
- Environment: the captured C3-ENV-001 environment (top-level venv, Python 3.14.4, numpy pinned 2.4.4). Mesa is not required for this gate.

## Open design parameters (Layer 3 to propose with justification)

- Mathematical definitions of `relative_drift`, `rho_cv`, `rho_range_over_mean`.
- Threshold value for each of the three filters.
- Lifted threshold value.
- Trajectory length per case (suggested: 200 ticks).
- Window length (suggested: 100 ticks).
- Sliding window step (suggested: 25 ticks, yielding 5 windows per trajectory).
- Seed value for any random elements in case generation (suggested: 42, matching CTL-001).
- Specific shapes for the synthetic trajectories (e.g., exact slope for Case 2, exact wobble amplitude for Case 3, exact step magnitude for Case 6) - choose values that exercise the filters near but clearly beyond their thresholds, so the discrimination is robust without being artificially easy.

## Output CSV schema (suggested; Layer 3 may refine)

One row per (case, window_start). Suggested columns:

- `Case` - case identifier (e.g., "1_flat_lifted", "2_monotone_drift", ...).
- `Window_Start` - starting tick index of the window.
- `Window_End` - ending tick index of the window.
- `Mean_Rho` - mean of rho within the window.
- `Relative_Drift` - the relative_drift filter value.
- `Rho_CV` - the rho_cv filter value.
- `Rho_Range_Over_Mean` - the rho_range_over_mean filter value.
- `Steady_State_Candidate` - TRUE / FALSE.
- `Lifted_Activation_Candidate` - TRUE / FALSE.

Layer 3 may add columns if useful for diagnosis (e.g., individual threshold-crossing flags), but the listed columns are required.

## Deliverables expected from Layer 3

1. **The script** `cycle3/c3_ss_001_battery.py`, complete and runnable, BOM-less UTF-8. Self-contained; no imports beyond numpy / pandas / standard library unless justified.
2. **Proposed Pre-execution block content** for `cycle3/TEST_RECORD_C3-SS-001.md`. Layer 1 will write the final test record; Layer 3's draft populates the design-side fields (script name and version, run parameters, expected per-case pass criteria stated per level).
3. **Short rationale** (a few paragraphs) for the open design parameters - filter mathematical definitions, threshold values, window mechanics, lifted threshold. Sufficient that Layer 2 can review the choices on validity grounds.
4. **Expected per-case discrimination output** - what the CSV should contain when the script is run. One row per (case, window_start), with the expected filter values (approximate, given any noise) and the expected candidate flags. This supports sufficiency-testing at Layer 1's implementation review, before Mike's canonical run.

Deliverable 4 is required, not optional. The sufficiency-tested discipline operates by comparing the actual run output against Layer 3's predicted output; without the prediction, Layer 1 cannot test sufficiency, only assert it.

## Vocabulary (binding)

- rho = activation density.
- Psi = coherence (not used in this gate by construction).
- Lambda = structural conduciveness (not used in this gate).
- "earned steady-state window" - the operational target of this gate.
- Agents act (no decision / optimization / utility / cognitive language). Not directly applicable to this gate (rho(t) is a scalar time series), but the discipline holds across the project.
- "the point(s) at which mu(rho) = 0" (never rho_c).
- "per-cell active-state values" for the underlying substrate cells; rho(t) is the per-tick scalar mean of those values over the grid.
- Candidates PRODUCE or FAIL TO PRODUCE - never "confirm" / "demonstrate".
- "fraction of active neighbors" is fine (local); never "fraction of the population".

## Routing

Layer 3 returns deliverables to Mike (one channel: Mike pastes). Mike routes to Layer 1 for implementation review (sufficiency-tested, not asserted). Layer 1 routes to Layer 2 for substantive review. Mike runs the canonical execution after both reviews clear. Test record advances to valid-L2 only on Mike's canonical run producing the designed discrimination.
