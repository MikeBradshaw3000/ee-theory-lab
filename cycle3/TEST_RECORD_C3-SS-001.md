# TEST RECORD - C3-SS-001 Steady-state eligibility apparatus

> Copy of TEST_RECORD_TEMPLATE.md, filled for C3-SS-001. Pre-execution block written at design-phase open; execution and post-execution blocks left for Mike. Execution channel is Mike only; no layer executes.

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

**Date run:**
**Machine / environment:** _(confirm venv interpreter path per MESA_ENVIRONMENT_REPRODUCTION)_
**Actual command run:**
```
<paste verbatim>
```

**Output files generated:**

---

## Post-execution (write after running)

**Highest level cleared:**

**Result summary:**

**Control outcomes:**
- Positive control:
- Negative control:

**Steady-state eligibility outcome (if applicable):**

**Interpretation (L4 - Mike / Layer 1 only):**

**Divergence note (co-equal pair):**
> Not applicable to this gate by construction - SS-001 evaluates rho(t), which is a per-tick scalar (mean activation density over the grid), not the candidate Psi pair. The co-equal pair is engaged by CTL-001 and by the substantive probe phase that opens after this gate clears.

**Follow-up decision:**

**Registry status at close:**
