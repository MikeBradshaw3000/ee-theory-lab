# TEST RECORD - C3-OBS-001 Wave-one substantive probe (Rules A + B)

> Copy of TEST_RECORD_TEMPLATE.md, filled for C3-OBS-001. Pre-execution block written at design-phase open; execution and post-execution blocks filled after the canonical run and the review chain. Execution channel is Mike only; no layer executes. This is the first substantive probe after the three precondition gates (C3-ENV-001 passed-L1, C3-CTL-001 valid-L2, C3-SS-001 valid-L2) cleared. It is wave one of the substantive probe phase, scoped to Rules A and B; Rule C is deferred to wave two.

---

## Pre-execution (write before running)

**Test ID:** C3-OBS-001
**Test name:** Wave-one substantive probe (Rules A + B)
**Registry status at open:** planned -> ready
**Date opened:** 2026-05-28

**Purpose - the question this test answers:**
> Under controlled structural-conduciveness conditions, does the substrate produce the design-anticipated discrimination among candidate coherence signatures - specifically, does any (rule, band, seed, window) produce a lifted, non-degenerate low/low candidate signature (lifted rho with both Psi_meanI_state and Psi_persistence_I near null over an earned steady-state window), and does Rule A serve as a non-discriminating both-agree baseline while Rule B separates the co-equal observables? (The possible "no": the substrate may not enter the low/low candidate regime under the sampled rules, or Rule A may fail to act as a baseline, or Rule B may fail to separate the observables. Any of these is wave-one DATA, not a defect.)

**Theoretical target - which part of Regime-II-as-structural this bears on:**
> The load-bearing design point from PROBE_DESIGN_INPUTS_HELD Section 4: the substantive probe varies Lambda and looks for the SEQUENCE - Lambda changes, rho lifts, coherence signatures remain low over an earned steady-state window, and only under other conditions do one or both coherence signatures lift. This is the ABM analog of Lambda -> rho -> mu(rho) -> Psi. The lifted-rho + low/low candidate signature (PROBE_DESIGN_INPUTS_HELD Section 5: candidate Regime II) is the specific signature wave one searches for, operationalized as the LowLow_Nondegenerate_Candidate flag. The test does NOT presuppose which observable (Psi_meanI_state, Psi_persistence_I) is Regime-II coherence - the ontological question rides forward, unsettled, L4. It does NOT assign any regime; regime assignment is L4 (Mike / Layer 1).

**Level this test is designed to address:** L1 (implementation) and apparatus-level substrate observation (the discrimination among candidate signatures), not L4.
> By construction it does not reach L4: candidate signatures are read against grid-local nulls and earned-window eligibility, with no interpretation of what any signature MEANS for Regime-II-as-structural. The L4 question - which observable, if either, IS Regime-II coherence - is held for Mike / Layer 1 on coherence-as-relational-mutual-reinforcement grounds.

**Inputs and parameters:**
> Locked Cycle 3 baseline topology: 50x50 grid, Moore radius 1 (8-neighbor), toroidal. Random starting rho ~ 0.10. Synchronous update. Two rules:
> - Rule A (both-agree baseline): threshold-style rule swept over tau_A in {1,2,3,4,5,6,7,8}.
> - Rule B (range-bound rule): swept over four bands [1,2], [2,3], [2,4], [3,4].
> Five seeds per (rule, parameter): 42, 137, 256, 1024, 31415. Sweep A = 8 tau values x 5 seeds = 40 runs; Sweep B = 4 bands x 5 seeds = 20 runs; 60 runs total.
> Earned steady-state windowing per the SS-001-validated apparatus (relative_drift, rho_cv, rho_range_over_mean filters; lifted-mean threshold), producing the Steady_State_Candidate and Lifted_Activation_Candidate flags. Coherence observables (Psi_meanI_state, Psi_persistence_I) computed as z-scores against grid-local permutation nulls. LowLow_Nondegenerate_Candidate flag fires when both coherence z-scores are below LOW_Z_THRESH = 2.0 over an earned, lifted, non-degenerate window. Degeneracy flags: extinction_degenerate, saturation_degenerate.

**Script name and version:**
> New to Cycle 3 - drafted by Layer 3 per the code-production contract (this session), folding the six Layer 2 design edits and the modified delivery flow (Layer 1 packages and delivers). Path: `cycle3/c3_obs_001_battery.py` (15,851 bytes, BOM-less UTF-8, LF line endings). Code v1 -> four Layer 1 corrections -> v2 (the version that ran).

**Expected data produced:**
> An aggregate CSV, one row per (rule, lambda_id, seed, window_start) evaluation, plus per-run NPZ state files. Required columns (21, per contract Section 6 schema): rule, lambda_id, seed, window_start, Psi_meanI_state, Psi_meanI_state_z, Psi_persistence_I, Psi_persistence_I_z, relative_drift, rho_cv, rho_range_over_mean, mean_rho, Steady_State_Candidate, Lifted_Activation_Candidate, mean_active_state_variance, persistence_std, extinction_degenerate, saturation_degenerate, LowLow_Nondegenerate_Candidate, Tick_to_Freeze, Tick_to_Zero. Output paths: `cycle3/data_out/c3_obs_001_results.csv` (300 rows: 200 Sweep A + 100 Sweep B), `cycle3/data_out/c3_obs_001_states_*.npz` (60 files).

**Expected output / pass criterion - stated per level:**
- L1 (implementation): the battery runs without error at the captured C3-ENV-001 environment; pre-flight passes (venv-active, Python 3.14.4, numpy 2.4.4, mesa import, cycle3 reachability); parity check passes against the CTL-001 and SS-001 modules including seed-reset null-parity; output finite and well-formed.
- Apparatus-level substrate observation: the battery produces, per (rule, lambda_id, seed, window), the flag set and z-scores the design specifies, so that the candidate-signature discrimination can be read from the CSV. There is no pass/fail "signature must appear" criterion - the substrate produces or fails to produce the low/low candidate signature, and either outcome is recorded as wave-one data. Pessimistic-on-passing: a flag set that could be produced by something other than what the design anticipates is not read as the anticipated signature.
- L4 (interpretation): not applicable - this probe is apparatus-level substrate observation, not evidence for Regime-II-as-structural. The L4 entry is empty by design.

**Positive control:**
> Rule A as the both-agree non-discriminating baseline - it should not produce a divergent joint signature or a LowLow_Nondegenerate_Candidate signature, serving as the reference against which Rule B's separation of the observables is read.

**Negative control:**
> The LowLow_Nondegenerate_Candidate flag with LOW_Z_THRESH = 2.0 - if it fires only where both coherence z-scores are genuinely near null over an earned, lifted, non-degenerate window, it discriminates the low/low candidate regime from organized or degenerate windows. Degeneracy flags (extinction_degenerate, saturation_degenerate) separate trivial endpoints (all-zero or saturated grids) from substantive windows.

**Interpretation boundary - declared in advance:**
> A result establishes what the substrate produced under the locked baseline topology, the random starting rho, the synchronous update, and the sampled rules and parameters - at apparatus level only. It does NOT establish anything about Regime-II coherence, does NOT settle the ontological question of which observable IS Regime-II coherence (L4, Mike / Layer 1, on relational-mutual-reinforcement grounds), and does NOT assign any regime. A negative result (the low/low candidate signature failing to appear) is wave-one DATA about the sampled rules, not a defect of the apparatus and not evidence about the theory. Seam: implementation / measurement (Layer 3 / Layer 2) vs meaning (Mike / Layer 1).

---

## Execution (Mike only)

**Date run:** 2026-05-28
**Machine / environment:** Captured C3-ENV-001 environment - venv at `C:\Users\vkz244\EE_Theory_Lab\venv` (workspace top-level, NOT repo root), Python 3.14.4, Mesa 3.5.1, numpy pinned 2.4.4.
**Actual command run:**
```
python cycle3\c3_obs_001_battery.py
```
> Pre-flight passed (venv-active, Python 3.14.4, numpy 2.4.4, mesa import, cycle3 reachability). Parity check passed all six assertions against the CTL-001 and SS-001 modules, including the seed-reset null-parity checks.

**Output files generated:**
> `cycle3/data_out/c3_obs_001_results.csv` - 300 window rows (200 Sweep A + 100 Sweep B exactly), 21 columns matching the contract Section 6 schema. Well-formed. Plus 60 NPZ state files at `cycle3/data_out/c3_obs_001_states_*.npz` (40 Rule A = 8 tau_A x 5 seeds; 20 Rule B = 4 bands x 5 seeds).

---

## Post-execution (write after running)

**Highest level cleared:** apparatus-level substrate observation (beyond L1).
> The battery ran clean (L1), and the candidate-signature discrimination is readable per (rule, lambda_id, seed, window) from the canonical CSV. The run cleared Layer 1 implementation review (code v2 clean after four corrections), Layer 1 sufficiency-testing (per-flag aggregation against the CSV - see the note on the [1,2] correction below), and Layer 2 substantive review (accept-with-required-amendments to canonical synthesis; no code rerun, no gate reopening, no L4). No L4 level is claimed or cleared; the L4 entry is empty by design.

**Result summary:**
> All figures below are read from the canonical CSV via per-(rule, lambda_id, seed) and per-(rule, lambda_id) aggregation. The LowLow_Nondegenerate_Candidate flag is False on all 300 rows - the wave-one low/low candidate signature did not appear under either rule.
>
> RULE A (both-agree baseline, tau_A in {1..8}; 5 seeds each):
> - Non-discriminating across all tau_A. No divergent joint signature, no LowLow_Nondegenerate_Candidate on any (tau_A, seed, window). Rule A's meaningful-failure criterion was not triggered.
> - Endpoint substrate adjudication: tau_A in {1,2,3} produced saturation (saturation_degenerate True). tau_A = 1,2: mean_rho ~0.99, Tick_to_Freeze 4-10, no extinction (Tick_to_Zero sentinel -1 on all). tau_A = 3: transient structure before saturation (Psi_meanI_state_z mean ~217, up to ~653; mean_rho ~0.935; Tick_to_Freeze 41-57, mean ~51). tau_A in {4,5,6,7,8} produced collapse to near-zero (mean_rho ~0.0002; Tick_to_Zero 1-4).
> - No stable locked-cluster regime appeared. Both prior pictures of Rule A dynamics (primary source's "high tau -> locked clusters"; Layer 3's pre-run "intermediate tau -> locked clusters") were not produced under wave-one conditions. Scope-limited: this refutation applies to the locked Cycle 3 baseline topology, random starting rho ~0.10, synchronous Rule A update, and the tested tau_A sweep - NOT to all Rule A variants, topologies, or initial densities.
> - Dual-degeneracy note (observed): for tau_A in {4,5,6,7,8}, both saturation_degenerate AND extinction_degenerate fire True on the same rows. Read from the CSV: Tick_to_Freeze and Tick_to_Zero coincide (tau_A = 4: both mean ~3; tau_A in {5,6,7,8}: both mean ~1). A grid that collapses to all-zero on the same tick it stops changing is simultaneously "frozen" (no further change) and "extinct" (rho = 0), so both degeneracy tests fire. This is recorded as observed; it changes no finding (both flags mean the window is degenerate / non-eligible).
>
> RULE B (range-bound rule, bands [1,2], [2,3], [2,4], [3,4]; 5 seeds each):
> - The eligible-or-near-eligible bands [1,2], [2,3], [2,4] share the earned-window signed signature: positive Psi_meanI_state z and negative Psi_persistence_I z - per-tick spatial organization of active-state configurations with anti-clustered persistence. NOT "high meanI / low persistence": the persistence z is genuinely negative (anti-clustered), not near-null. Per-band z means (from CSV): [1,2] meanI ~195, persistence ~-15; [2,3] meanI ~149, persistence ~-8; [2,4] meanI ~244, persistence ~-4.
> - Band [2,3] - ROBUST. Steady_State_Candidate True on multiple windows for all 5 seeds (4,4,4,4,3 of 5 windows per seed). The strongest earned-window result. Lifted on 5/5 seeds. mean_rho ~0.383.
> - Band [2,4] - EARNED-BUT-HETEROGENEOUS. Steady_State_Candidate True on all 5 seeds at the seed-level (>=1 earned window each), but window-count robustness is mixed: seeds 137, 256, 31415 earn multiple windows (4 each); seeds 42 and 1024 earn a single window each (1 each). Recorded as earned-but-heterogeneous, NOT grouped with [2,3] as uniformly robust. Lifted on 5/5 seeds. mean_rho ~0.465. (See the seed-level-occurrence vs window-count-robustness distinction below.)
> - Band [1,2] - BOUNDARY / NEAR-STEADY. Steady_State_Candidate True on only 1 of 25 windows across 5 seeds (seed 42, one window; the other four seeds earn none). Similar signed tendency to the eligible bands but does NOT earn steady windows comparably. NOT earned-steady on 5/5 seeds. Lifted on 5/5 seeds. mean_rho ~0.326.
> - Band [3,4] - NON-ELIGIBLE / UNSTABLE. Steady_State_Candidate True on 0 windows for 4 of 5 seeds (sustained upward drift; failed relative_drift and rho_range_over_mean). The 5th seed (31415) earns some windows but is saturation_degenerate (saturating, not cleanly steady); seeds 42 and 256 show partial extinction (3 and 2 extinction-degenerate windows). mean_rho ~0.094 (range 0.007-0.291). Non-eligible contrast observation (below).

**Seed-level-occurrence vs window-count-robustness distinction (named reading lens):**
> Two distinct levels of evidence, named here because they separate [2,3] from [2,4] and will recur in wave-two band comparison:
> - Seed-level occurrence: whether a seed produced AT LEAST ONE earned steady-state window.
> - Window-count robustness: HOW MANY earned windows each seed produced.
> The SS-001-validated apparatus is explicitly about earned steady-state windows, so window-count is the load-bearing measure of band robustness, not isolated seed-level occurrence. Under this distinction: [2,3] has 5/5 seed-level occurrence AND uniform multi-window robustness; [2,4] has 5/5 seed-level occurrence but mixed window-count robustness (multi-window on 3 seeds, single-window on 2); [1,2] has 1/5 seed-level occurrence. A ">=1 window per seed" criterion would group [2,4] with [2,3], smoothing over a real primary-source difference - the same overstatement shape the [1,2] correction addressed.

**[3,4] non-eligible contrast observation (fenced from the earned-window signature):**
> [3,4]'s coherence z-scores are positive Psi_meanI_state (~368 mean) and strongly POSITIVE Psi_persistence_I (~86 mean, range ~57-98) - the persistence sign is OPPOSITE to the eligible-or-near-eligible bands' negative persistence. This z-score retains its ordinary measurement meaning against the grid-local null (eligibility gates signature-status, not measurement-validity), so the sign is a valid apparatus-level description of what the substrate produced under [3,4]. But [3,4] is predominantly non-eligible / unstable, so this is recorded as a NON-ELIGIBLE CONTRAST OBSERVATION (instability-coupled), NOT as an earned-window signature and NOT comparable to the eligible bands' signature. It does not reopen eligibility. It may be an artifact of the non-steady dynamics (drifting / degenerating / saturating dynamics can themselves produce clustered persistence maps) - that is a substantive instability property, not measurement error. The sign-flip is retained because it is informative for the signed-framework amendment and wave-two probe design: the persistence axis does not merely weaken outside the eligible window - it reverses under the unstable band.

**Control outcomes:**
- Positive control (Rule A as non-discriminating baseline): produces - no divergent joint signature, no LowLow_Nondegenerate_Candidate on any Rule A row. Rule A acts as the both-agree baseline as designed (though it produced saturation/extinction rather than the hypothesized locked-cluster intermediate - see endpoint adjudication).
- Negative control (LowLow_Nondegenerate_Candidate flag, LOW_Z_THRESH = 2.0): the flag fired on 0 of 300 rows. In Rule A it is blocked by degeneracy (saturation or extinction). In Rule B it is blocked by large positive Psi_meanI_state z values (~140-370) in the lifted windows. The threshold worked as specified; the substrate did not enter the low/low candidate regime under these rules. DO NOT loosen LOW_Z_THRESH on this basis - Layer 2 specifically guarded against this synthesis move. The False-everywhere result is wave-one DATA (the design-anticipated signature did not appear under Rules A or B), not a defect.

**Held-inputs framework note:**
> The observed Rule B signature (positive meanI / negative persistence) falls OUTSIDE the held PROBE_DESIGN_INPUTS_HELD Section 2 quadrant scheme, which is a 2x2 high/low framework assuming "low" = near-null (z near zero). The substrate produced significantly negative (anti-clustered) persistence, which the 2x2 has no cell for; and [3,4] produced strongly positive persistence, the opposite end of the same axis. This motivates the held-inputs amendment (separate cluster item) to a signed three-level framework: positive structured / near-null / negative anti-structured on each axis. The framework being amended literally lacks the cells the wave-one data occupy.

**Layer 2 substantive review verdict:**
> Accept-with-required-amendments to canonical synthesis. No code rerun. No gate reopening. No L4 interpretation. The required amendments, all concurred by Layer 1 on independent grounds: (1) correct the Rule B [1,2] reading from Layer 3's initial "earned-steady on 5/5 seeds" to boundary / near-steady (CSV: 1/25 windows). (2) amend the held-inputs quadrant framework to a signed three-level scheme (negative persistence is anti-clustered, not near-null). (3) record the Rule A endpoint amendment (saturation/extinction, no locked-cluster regime under wave-one conditions; scope-limited). (4) record LowLow_Nondegenerate_Candidate False on all rows as an apparatus-level negative finding; do not revise LOW_Z_THRESH. (5) preserve the L4 boundary. Two further primary-source refinements surfaced by Layer 1's per-(rule, lambda_id, seed) aggregation and routed to Layer 2 during synthesis, both accepted: the [2,4] earned-but-heterogeneous correction (Layer 2 verdict: record as earned-but-heterogeneous, not grouped with [2,3]; the seed-level-occurrence vs window-count-robustness distinction is above the resolution the record should assert), and the [3,4] non-eligible contrast observation (Layer 2 verdict: record the positive-persistence sign in a separately labeled non-eligible contrast / instability-coupled field, not in the earned-window signature; eligibility gates signature-status, not measurement-validity).

**Interpretation (L4 - Mike / Layer 1 only):**
> Withheld. Empty by design. This probe is apparatus-level substrate observation, not interpretation. It establishes what the substrate produced under the locked baseline topology and the sampled rules and parameters. It establishes nothing about Regime-II coherence, nothing about whether any observed signature IS Regime-II coherence, and does not settle the ontological question of which observable (Psi_meanI_state, Psi_persistence_I) IS Regime-II coherence (L4, Mike / Layer 1, on coherence-as-relational-mutual-reinforcement grounds).

**Divergence note (co-equal pair):**
> Wave one engages the co-equal pair directly, and the pair separated under Rule B: Psi_meanI_state and Psi_persistence_I took opposite signs in the eligible bands (positive meanI, negative persistence), so the observables are not redundant under this rule - they measure distinct properties (per-tick spatial organization vs same-cell clustered persistence). This is an apparatus-level separation; it does NOT name either observable as theoretical Psi and does NOT settle which, if either, IS Regime-II coherence. The pair is held co-equal; the separation is data for the later L4 question, not the answer.

**Follow-up decision:**
> Apparatus-level closure for wave one (Rules A + B). The substantive findings stand recorded with the required amendments. Wave one did NOT produce the lifted, non-degenerate, low/low candidate signature under either rule - a negative apparatus-level finding recorded as data. Forward items for wave two (a SEPARATE decision, not seeded here): whether Rule C (deferred from wave one) should be designed as the candidate for producing the lifted low/low signature; whether Rule B's range-bound family structurally produces too much per-tick spatial organization whenever it sustains lifted rho; whether a Lambda-driven independent-activation or weakly-coupled-stochastic rule is needed as a substrate-side low/low generator; whether the signed three-level framework opens probe-design possibilities the 2x2 concealed; and whether finer-grained tau_A around the saturation/extinction boundary (tau_A = 3 -> 4) is worth sampling. Registry row added at valid-L2 (Mike arbitrates the exact status string). The held transition-rule menu and probe-design inputs receive the wave-one amendment in a separate cluster item.

**Registry status at close:** valid-L2
