# TEST RECORD - C3-SS-001 Steady-state eligibility apparatus

> Copy of TEST_RECORD_TEMPLATE.md, filled for C3-SS-001. Pre-execution block written at design-phase open; execution and post-execution blocks filled after the canonical run and the review chain. Execution channel is Mike only; no layer executes.

---

## Pre-execution (write before running)

**Test ID:** C3-SS-001
**Test name:** Steady-state eligibility apparatus
**Registry status at open:** planned -> ready
**Date opened:** 2026-05-27

**Purpose - the question this test answers:**
> Does the steady-state apparatus, applied to synthetic rho(t) trajectories with known behavior, produce the designed six-case discrimination - correctly admitting earned steady-state windows and lifted-activation windows on the criteria it claims to apply, with the two flags genuinely independent? (The possible "no": if the apparatus fails to produce the case-by-case discrimination, it is not validated and no real-substrate window may be classified by it.)

**Theoretical target - which part of Regime-II-as-structural this bears on:**
> Steady-state eligibility precondition: no real-substrate window is classified as a lifted earned steady-state window before the apparatus passes on synthetic trajectories. This is the third and final precondition gate before any real-substrate value can be read as Regime II. It operationalizes "earned steady-state window" from PROBE_DESIGN_INPUTS_HELD Section 4 and the resume anchor. It does NOT presuppose which observable (Psi_meanI_state, Psi_persistence_I) is Regime-II coherence - the ontological question rides forward, unsettled, L4.

**Level this test is designed to address:** L1 and L2.
> By construction it cannot reach L3 or L4: the cases are synthetic rho(t) trajectories with no substrate, and nothing is interpreted for Regime-II-as-structural. L3 in this context refers to real-substrate steady-state eligibility - the validated apparatus applied to ABM output - which is a downstream gate, not this one.

**Inputs and parameters:**
> No substrate / no parquet - synthetic rho(t) arrays by construction. Six minimum cases (Layer 2 specification; trajectory length, window length, sliding step, and thresholds set by Layer 3's draft per the design contract):
> - Case 1 (positive control - flat lifted steady state): rho(t) at a lifted constant plus minimal noise.
> - Case 2 (drift-filter negative - monotone drift): rho(t) climbing or falling steadily through the trajectory at a lifted mean.
> - Case 3 (variability-filter negative - high wobble with near-zero slope): rho(t) oscillating with large amplitude around a lifted mean, mean-trend near zero.
> - Case 4 (lifted-flag negative - low trivial activity): rho(t) at a near-zero constant plus minimal noise. Tests independence of the two flags.
> - Case 5 (positional discrimination - late stabilization): rho(t) chaotic or drifting early, settling to a flat lifted plateau in the later portion.
> - Case 6 (positional discrimination - step transition): rho(t) at one plateau, then a sharp step, then a different (lifted) plateau.
> Windowing is required (Cases 5 and 6 cannot be discriminated by whole-trajectory analysis). The apparatus evaluates filters at multiple sliding window positions across each trajectory.
> Three window filters: relative_drift, rho_cv, rho_range_over_mean - each with a threshold. Lifted threshold for mean rho within the window. Mathematical definitions, threshold values, trajectory length, window length, sliding step, and lifted threshold set by Layer 3 per the design contract.
> Seed for any random elements (suggested in contract: 42, matching CTL-001; Layer 3 may refine).

**Script name and version:**
> New to Cycle 3 - drafted by Layer 3 per the design contract `SS001_LAYER3_CONTRACT.md` (this session). Path: `cycle3/c3_ss_001_battery.py`. Version tag at draft.

**Expected data produced:**
> A CSV summary, one row per (case, window_start) evaluation. Required columns: Case, Window_Start, Window_End, Mean_Rho, Relative_Drift, Rho_CV, Rho_Range_Over_Mean, Steady_State_Candidate, Lifted_Activation_Candidate. Output path: `cycle3/data_out/c3_ss_001_results.csv`. Layer 3 may add diagnostic columns; the listed columns are required.

**Expected output / pass criterion - stated per level:**
- L1 (implementation): the battery runs without error at the captured C3-ENV-001 environment; output finite and well-formed.
- L2 (measurement validity): every (case, window_start) row matches the designed pass/fail pattern for that case and window position:
  - Case 1: all windows produce (Steady_State_Candidate TRUE, Lifted_Activation_Candidate TRUE).
  - Case 2: all windows produce Steady_State_Candidate FALSE, with Relative_Drift exceeding its threshold.
  - Case 3: all windows produce Steady_State_Candidate FALSE, with BOTH Rho_CV AND Rho_Range_Over_Mean exceeding their thresholds.
  - Case 4: all windows produce (Steady_State_Candidate TRUE, Lifted_Activation_Candidate FALSE).
  - Case 5: early-positioned windows produce Steady_State_Candidate FALSE; late-positioned (plateau) windows produce (Steady_State_Candidate TRUE, Lifted_Activation_Candidate TRUE).
  - Case 6: windows whose span includes the step produce Steady_State_Candidate FALSE; windows entirely within either plateau produce the designed pattern for that plateau (steady, with lifting depending on plateau level).
  - The acceptance criterion is row-by-row alignment, not aggregate. Pessimistic-on-passing: each case discriminates a specific apparatus failure mode, and the discrimination must produce on every case. Do not collapse cases under any rationalization that "the remaining cases are sufficient."
- L3 (real-substrate steady-state eligibility): not applicable by construction. The validated apparatus applied to ABM output is a downstream gate, not this one.
- L4 (interpretation): not applicable - this gate is apparatus, not evidence for Regime-II-as-structural.

**Positive control:**
> Case 1 (flat lifted steady state) - must produce both flags TRUE on all windows before any output is interpreted. If Case 1 fails to produce, the apparatus has not cleared past L1 and no interpretation is licensed.

**Negative control:**
> Cases 2 (monotone drift) and 3 (high wobble) - each must fail Steady_State_Candidate on the specific filter the case targets, distinguishing the apparatus's correct rejection of unsteady trajectories from a measurement artifact. Case 4 (low trivial activity) is the lifted-flag negative control - must fail Lifted_Activation_Candidate while passing Steady_State_Candidate, verifying the two flags are independent. Cases 5 and 6 are positional discriminations - they verify the apparatus is genuinely windowed and the discrimination depends on window position; without them the apparatus could "pass" trivially by classifying whole trajectories.

**Interpretation boundary - declared in advance:**
> A pass establishes that the steady-state apparatus, applied to synthetic rho(t) trajectories at the design-contract parameters, correctly produces the six-case discrimination across all windows - the apparatus admits and rejects windows on the criteria it claims to apply, with the two flags genuinely independent. It does NOT establish anything about real-substrate values. It does NOT establish that any real ABM trajectory has earned a steady-state window. It does NOT establish anything about Regime-II coherence, and it does not settle the ontological question of which observable IS Regime-II coherence (L4, Mike / Layer 1, on relational-mutual-reinforcement grounds). The classification of real-substrate windows is the work that opens only after this gate clears. Seam: implementation / measurement (Layer 3 / Layer 2) vs meaning (Mike / Layer 1).

---

## Execution (Mike only)

**Date run:** 2026-05-27
**Machine / environment:** Captured C3-ENV-001 environment - top-level venv, Python 3.14.4, numpy pinned 2.4.4. _(confirm venv interpreter path per MESA_ENVIRONMENT_REPRODUCTION if needed)_
**Actual command run:**
```
python cycle3\c3_ss_001_battery.py
```
> Run parameters as settled by Layer 3 per the design contract: SEED = 42; TRAJECTORY_LENGTH = 200 ticks; WINDOW_LENGTH = 100 ticks; WINDOW_STEP = 25 ticks (yields 5 windows per trajectory; window intervals are half-open `[Window_Start, Window_End)`); LIFTED_THRESHOLD = 0.05; THRESH_RELATIVE_DRIFT = 0.10; THRESH_RHO_CV = 0.10; THRESH_RHO_RANGE_OVER_MEAN = 0.25.

**Output files generated:**
> `cycle3/data_out/c3_ss_001_results.csv` - the per-(case, window_start) summary, 30 rows, exactly the columns specified in the contract (Case, Window_Start, Window_End, Mean_Rho, Relative_Drift, Rho_CV, Rho_Range_Over_Mean, Steady_State_Candidate, Lifted_Activation_Candidate). Well-formed.

---

## Post-execution (write after running)

**Highest level cleared:** L2
> Beyond "script ran" (L1): the synthetic battery produces the full designed six-case discrimination, with every (case, window_start) row matching the predicted (Steady_State_Candidate, Lifted_Activation_Candidate) pair (30/30 rows). The apparatus cleared Layer 1 implementation review (script content matches contract spec; filter math implements suggested forms exactly; window iteration produces 5 positions per trajectory as specified), Layer 1 sufficiency-testing (canonical CSV row-by-row against Layer 3's predicted output), and Layer 2 substantive review (filter coupling is structural, not a flaw; flag-level discrimination is the gate's criterion).

**Result summary:**
> The apparatus produces the designed six-case discrimination at the contract parameters (trajectory 200, window 100, step 25, seed 42, thresholds drift 0.10 / cv 0.10 / range_over_mean 0.25 / lifted 0.05). Each value below is read from the canonical CSV:
> - Case 1 (flat lifted steady state, positive control): all 5 windows produce (T, T). Mean_Rho ~0.200, Relative_Drift 0.001-0.004, Rho_CV ~0.015, Rho_Range_Over_Mean ~0.049. All steady filters comfortably under thresholds; Mean_Rho comfortably over lifted threshold.
> - Case 2 (monotone drift, drift-filter negative): all 5 windows produce (F, T). Relative_Drift 0.359 to 0.548 across windows - fires drift filter. Filter coupling: CV (0.105-0.160) and Range (0.383-0.569) also fire on this case; structural to a linear ramp, not a flaw (Layer 2's substantive judgment).
> - Case 3 (high wobble, variability-filter negative): all 5 windows produce (F, T). Rho_CV ~0.282-0.287, Rho_Range_Over_Mean ~0.827-0.844 - fires CV and Range filters. Filter coupling: drift trips in 3 of 5 windows (0.149, 0.157, 0.166) due to period-20 sine in 100-tick window producing 4.95 periods with phase residual; finite-window oscillation produces this naturally (Layer 2).
> - Case 4 (low trivial activity, lifted-flag negative): all 5 windows produce (T, F). Mean_Rho 0.020-0.020 (below lifted threshold 0.05). Steady filters all pass with the narrowest margins in the design (CV ~0.056 vs 0.10; Range ~0.196 vs 0.25); adequate for the canonical seeded run.
> - Case 5 (late stabilization, positional discrimination): windows 0/25/50/75 produce (F, T), window 100 produces (T, T). Relative_Drift transitions cleanly across windows (0.998 to 0.703 to 0.375 to 0.113 to 0.0005); the late-positioned window locks onto the plateau.
> - Case 6 (step transition, positional discrimination): windows 0 and 100 produce (T, T) (each plateau is steady and lifted); windows 25/50/75 produce (F, T) (step-spanning windows fail steady on drift 0.750-1.198 and range 0.696-1.048). Pre-step plateau Mean_Rho 0.150, post-step plateau Mean_Rho 0.350.

**Control outcomes:**
- Positive control (Case 1): produces - all 5 windows (T, T) with comfortable margins on all filters.
- Negative controls (Cases 2, 3, 4, and Case 6 step-spanning windows): each produces the intended rejection. Cases 2 and 3 fire multiple filters (filter coupling is structural, not a flaw - Layer 2's substantive judgment). Case 4 distinguishes "steady but not lifted" cleanly (Mean_Rho 0.020, below lifted threshold). Case 6 step-spanning windows separate plateau windows from transition events.

**Steady-state eligibility outcome:**
> Applicable to this apparatus by construction - SS-001 IS the steady-state eligibility apparatus, evaluated synthetically. On the six cases: the apparatus correctly admits earned-steady-and-lifted windows (Case 1 all windows, Case 5 window 100, Case 6 windows 0 and 100) and rejects windows that should be rejected (Case 2 all, Case 3 all, Case 5 early windows, Case 6 step-spanning windows), with Case 4 distinguishing structural steadiness from lifted activation independently (steady but not lifted). All four diagnostics that license earned-window status are reported per window in the canonical CSV: relative drift < 0.10, rho_cv < 0.10, rho_range_over_mean < 0.25, mean_rho > 0.05 (lifted).

**Layer 2 substantive review verdict:**
> Layer 2 accepted C3-SS-001 at the flag-discrimination level. The apparatus correctly admits/rejects all 30 canonical synthetic windows according to the pre-specified (Steady_State_Candidate, Lifted_Activation_Candidate) expectations. Cases 2 and 3 are not pure per-filter unit tests; filter coupling is expected for strong ramps and finite-window oscillations. This is non-blocking because the gate tests earned-window flag behavior, not isolated unit testing of each filter. Case 4 margins are adequate for the canonical seeded run. C3-SS-001 clears the steady-state eligibility precondition, with no Regime-II interpretation attached. Layer 2 also noted the window interval convention should be explicit: window intervals are half-open `[Window_Start, Window_End)` (matching Python slicing).

**Interpretation (L4 - Mike / Layer 1 only):**
> Withheld. This test is apparatus validation, not interpretation. It establishes that the steady-state apparatus correctly produces the designed flag discrimination on synthetic rho(t) trajectories at the contract parameters. It establishes nothing about real-substrate values, nothing about whether any real ABM trajectory has earned a steady-state window, and nothing about Regime-II coherence or the ontological question of which observable IS Regime-II coherence (L4, Mike / Layer 1, on relational-mutual-reinforcement grounds).

**Divergence note (co-equal pair):**
> Not applicable to this gate by construction - SS-001 evaluates rho(t), which is a per-tick scalar (mean activation density over the grid), not the candidate Psi pair. The co-equal pair is engaged by CTL-001 and by the substantive probe phase that opens after this gate clears.

**Follow-up decision:**
> L2 pass. The third and final Cycle 3 precondition gate is cleared. All three precondition gates (C3-ENV-001 passed-L1, C3-CTL-001 valid-L2, C3-SS-001 valid-L2) now stand cleared. The apparatus is available for real-substrate window classification - a downstream gate not addressed by this test. Registry row advanced to valid-L2; script column advanced from "c3_ss_001_battery.py (Layer 3 draft pending)" to "c3_ss_001_battery.py" reflecting the script's now-canonical state. Transition rules and probe-design inputs (cycle3/PROBE_DESIGN_INPUTS_HELD.md) remain held, uncommitted - they open in their phase. The substantive probe phase is now unblocked at the precondition-gate level; opening it is Mike's call. Two forward items noted by Layer 2 and carried, neither blocking: (a) the two output flags (Steady_State_Candidate, Lifted_Activation_Candidate) must remain independent in any downstream apparatus and not be combined into a single "Regime-II eligible" flag; real-substrate interpretation needs both flags plus the coherence observable pair plus L4 judgment. (b) A supplemental filter-unit-test battery (cases isolating drift, CV, range_over_mean separately) is an optional future enhancement, not required for this gate.

**Registry status at close:** valid-L2
