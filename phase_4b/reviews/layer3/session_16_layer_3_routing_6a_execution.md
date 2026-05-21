# Layer 3 Routing — Session 16: Item 6a Pre-Registration Execution Against Flight 2 Substrate

**From:** Mike Bradshaw, on behalf of Layer 1 (Claude)
**To:** Gemini (Layer 3)
**Routing purpose:** Execution of the item 6a F-form-relevant characterization pre-registration (v2) against Flight 2 canonical substrate. This routing closes item 6a acceptance component 7 ("Layer 3 routing in hand for execution against Flight 2 canonical substrate"); the pre-registration commit + this routing are the conditions for component 7 closure.

**Attachments (required for execution):**
- `item_6a_f_form_characterization_v2.yaml` — Phase 4B v1.1 §4.4 schema with full predictor/interaction/uncertainty specification
- `item_6a_f_form_characterization_v2.md` — Reading A+ rationale, EDA/confirmatory partition, seven-trigger escalation rule

---

## Context

Session 16 produced an item 6a pre-registration v2 draft pair after a full Layer 2 cycle (substantive review + v2-acceptance). Layer 2 accepted v2 as represented. Layer 1 verified artifact correspondence (R1–R7 present in v2 files). Mike has arbitrated:

- Two-stage scope: Reading A+ (one document pair, binding EDA/confirmatory partition, seven-trigger escalation rule)
- Primary interactions: IF1 + IF2; IF5 as sensitivity-version (Layer 2 revision 6, Option B); IF3, IF4 excluded with rationale
- Transition-proxy form: first epoch in which rolling-mean ρ exceeds threshold τ for Z consecutive ticks; (W, τ, Z) as EDA-calibrated parameters from pre-specified search spaces
- Specific-proxy approach with calibration/confirmatory split (not threshold-sensitivity-curves)

The pre-registration is structurally complete and ready for Layer 3 execution.

## Execution scope

This routing requests Layer 3 to execute the item 6a pre-registration in two stages, with **explicit Layer 2 + Layer 1 review checkpoint between EDA and confirmatory stages** per the binding Reading A+ structure.

### Stage 1: EDA execution

**Inputs:**
- Pre-registration: v2 YAML + Markdown pair (this routing's attachments)
- Data files: F_LR 20×20 and F_2_symmetric 20×20 production runs (probe1_overcrowding files); per YAML `data_files` and Markdown Section 3.2 calibration subset
- Validity mask: per Markdown Section 3.2 and YAML `interpretation_boundary.shadow_copy_handling.implementation.validity_mask`; substrate-mechanical implementation produced in session 16

**EDA execution steps:**

1. **Load calibration data.** F_LR 20×20 and F_2_symmetric 20×20 probe1_overcrowding parquet files via the canonical Phase 4B intake pattern (single-file-at-a-time per §2.3 memory hygiene; explicit DataFrame release between files).

2. **Compute per-tick ρ trajectories.** For each calibration run, aggregate `is_active` to per-tick mean (ρ = per-tick fraction of cells with `is_active == 1`). Use the substrate-mechanical `compute_rolling_rho` function produced in session 16 (or equivalent), at each candidate window size W ∈ {10, 25, 50, 100, 200} ticks.

3. **Compute threshold-crossing tables.** For each (W, τ, Z) combination with τ ∈ {0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50} and Z ∈ {5, 10, 25, 50, 100}, record first-crossing epoch per run (the first epoch in which rolling-mean ρ exceeds τ for Z consecutive ticks).

4. **Produce diagnostic visualizations.** Rolling-ρ trajectories for both calibration runs at each W, with candidate threshold lines overlaid.

5. **Apply locking rule (Markdown Section 4.1).** Evaluate (W, τ, Z) candidates against three criteria:
   - Visual stability across calibration runs (first-crossing identifiable in BOTH 20×20 runs)
   - Parameter parsimony (smallest W, largest Z, largest τ subject to criterion 1)
   - Cross-F-form discriminability (same F-form crosses earlier in both 20×20 runs at locked values)

6. **Surface locking outcome.** One of three possible outcomes:
   - **Locked:** unique (W, τ, Z) combination satisfies all three criteria; produce calibration report with locked values
   - **E1 escalation:** no combination satisfies the criteria; produce escalation report
   - **E7 escalation:** multiple combinations satisfy criteria but no principled selection emerges, OR all admissible combinations produce degenerate transition markers (vacuous/non-informative/unstable per Markdown Section 5 E7 definitions); produce escalation report

7. **Apply other escalation triggers as relevant.** If during execution any of E2–E6 conditions surface (proxy form structurally inadequate; partition inadequate; substrate-fact contradiction; interpretation_boundary clause needs revision; predictor set needs revision), produce escalation report.

**EDA outputs (committed to git):**

- `phase_4b/pre_registrations/item_6a_f_form_characterization/eda_outputs/rolling_rho_trajectories_FLR_20x20.csv`
- `phase_4b/pre_registrations/item_6a_f_form_characterization/eda_outputs/rolling_rho_trajectories_F2sym_20x20.csv`
- `phase_4b/pre_registrations/item_6a_f_form_characterization/eda_outputs/threshold_crossing_tables.csv`
- `phase_4b/pre_registrations/item_6a_f_form_characterization/eda_outputs/diagnostic_visualizations/` (rolling-ρ plots at each W with threshold lines overlaid)
- `phase_4b/pre_registrations/item_6a_f_form_characterization/eda_outputs/calibration_report.md` (CLI-generated Markdown per §4.5; explicit `exploratory` flag per §1)
- **EITHER** `phase_4b/pre_registrations/item_6a_f_form_characterization/calibration_locked.yaml` (if locked) **OR** `phase_4b/pre_registrations/item_6a_f_form_characterization/eda_outputs/escalation_report.md` (if escalated)

All EDA outputs marked `exploratory` per Phase 4B v1.1 §1 source-of-thresholds rule. They are NOT used for primary substantive findings.

### EDA → Confirmatory checkpoint (Layer 2 + Layer 1 review)

**Hard checkpoint before any confirmatory execution.** After Stage 1 closes (locked OR escalated), Layer 3 stops. The EDA outputs are routed through:

- **Layer 1 review:** verify locking rule application, verify EDA outputs match v2 specification, verify any escalation trigger was correctly applied
- **Layer 2 review** (if locking succeeded): substantive review of the calibration_locked.yaml against locking rule criteria; sanity-check on whether the locked values appear substrate-plausible
- **Mike's arbitration:** confirm execution proceeds to Stage 2 with the locked values, OR confirm escalation, OR direct alternative path

**Layer 3 does NOT proceed to confirmatory execution without explicit arbitration from Mike via Layer 1.** This checkpoint is the binding discipline that makes Reading A+'s single-document compactness substantively equivalent to Reading B's two-document sequential structure.

### Stage 2: Confirmatory execution (gated by checkpoint)

**Inputs (post-checkpoint):**
- Calibration_locked.yaml (Stage 1 output)
- Confirmatory data: F_LR 40×40 and F_2_symmetric 40×40 production runs (probe1_overcrowding files)

**Confirmatory execution steps:**

1. **Load confirmatory data.** F_LR 40×40 and F_2_symmetric 40×40 probe1_overcrowding parquet files per Phase 4B v1.1 §2.3 memory hygiene.

2. **Execute primary IF1 regression.** Linear regression of `logit(p_base)` on the predictor set per YAML `predictors.primary`, with IF1 interaction predicates (`F_variant × Lambda_total`, `F_variant × Term_Lambda`). η-floor inversion construction per YAML `outcome.construction`. Cluster-robust standard errors per `cluster_run_tick`.

3. **Execute primary IF2 regression.** Same predictor set; IF2 interaction predicates (`F_variant × Local_Density`, `F_variant × Local_Density²`).

4. **Execute transition-proxy regression.** Using locked (W, τ, Z) from calibration_locked.yaml: compute rolling-ρ trajectories for 40×40 confirmatory runs; identify first-crossing epoch per run; regress first-crossing epoch on F_variant. Report F_LR vs F_2_symmetric difference.

5. **Execute cross-scale comparison (analysis 4, descriptive verdict).** Compare first-crossing epochs and IF1/IF2 coefficient estimates between 20×20 calibration runs and 40×40 confirmatory runs. Assign cross-scale verdict per §5.2 value set (scale_stable | variance_reducing_only | scale_dependent_strengthening | scale_dependent_disappearing | scale_dependent_other).

6. **Execute IF5 sensitivity regression (analysis 5).** Linear regression of `logit(p_base)` on predictor set plus IF5 sensitivity predicates (`scale × F_variant`, `scale × Lambda_total`, `scale × Local_Density`), using both 20×20 calibration data and 40×40 confirmatory data jointly. Report IF5 interaction coefficients. **Structurally distinct from analysis 4 per Markdown Section 4.2.**

7. **Execute pre-registered sensitivities.** Cell-level clustering as alternative to `cluster_run_tick`; IF1 sensitivity-version (Q-history modulation) activated only if primary IF1 surfaces epoch-conditional effects within a single F-form per YAML pre-registered trigger; IF2 sensitivity-version (density threshold) as exploratory diagnostic per YAML pre-registered status.

8. **Produce confirmatory output.** Markdown report and structured CSVs per Phase 4B v1.1 §4.5; no Jupyter notebooks per P8.

**Confirmatory outputs (committed to git):**

- `phase_4b/reports/item_6a_f_form_characterization.md` (CLI-generated Markdown; primary IF1, primary IF2, IF5 sensitivity, transition-proxy regression, cross-scale verdict, two-field classification of primary findings)
- `phase_4b/reports/item_6a_coefficient_tables.csv` (coefficient tables for primary IF1, primary IF2, IF5 sensitivity)
- `phase_4b/reports/item_6a_marginal_effects.csv`
- `phase_4b/reports/item_6a_transition_proxy_results.csv`
- `phase_4b/reports/item_6a_cross_scale_comparison.csv` (analysis 4 verdict)
- `phase_4b/reports/item_6a_if5_sensitivity_results.csv` (analysis 5)
- `phase_4b/reports/item_6a_sensitivity_clustering_comparison.csv` (cell-level vs run × tick comparison)

## Implementation latitude

This is execution, not substrate-state engagement. The latitude is:

**Implementation permitted:**
- All data loading, regression fitting, output generation per the pre-registration's specification
- Computational implementation choices within Phase 4B v1.1 constraints (statsmodels per §4.1 reference; CLI argparse per §3.2; Markdown + CSV output per §4.5)
- Substrate-mechanical column derivations explicitly specified in the pre-registration (rolling-mean ρ, threshold-crossing tables)

**Implementation NOT permitted (escalation rule territory):**
- Proxy form revision
- Parameter search-space expansion
- Confirmatory outcome variable change
- Interpretation_boundary clause modification
- Shadow-copy handling rule change
- Discretionary tie-breaking in (W, τ, Z) selection (handled by E7)
- Any pre-registration modification mid-execution

If any of these conditions surface during execution, the escalation trigger fires and Layer 3 produces an escalation report rather than proceeding.

## Pre-execution review

Per Phase 4B's protocol convention (referenced in v1.1 §11 item 15 closure), Layer 3 implementation scripts are subject to Layer 1 pre-execution review. Layer 3 produces the implementation scripts and the Layer 1 reviews them before execution. The pre-execution review is structurally analogous to the Layer 2 v2-acceptance pass — a sanity check on the implementation against the pre-registration's specification.

**Sequence:**
1. Layer 3 produces Stage 1 (EDA) implementation script
2. Layer 1 pre-execution review
3. Mike's arbitration to proceed
4. Stage 1 execution
5. EDA → Confirmatory checkpoint (per above)
6. Layer 3 produces Stage 2 (confirmatory) implementation script
7. Layer 1 pre-execution review of Stage 2 script
8. Mike's arbitration to proceed
9. Stage 2 execution
10. Final output review

The two implementation scripts are separate deliverables; combining them risks bypassing the EDA → Confirmatory checkpoint.

## Substrate-state context (from session 16 prior routing)

For Layer 3's working context:

- Canonical persisted column names: `Psi_local`, `Delta_v`, `Delta_u`, `Delta_r` at cell-tick 1-tick granularity (confirmed session 16)
- F_LR has probe-distinct outputs across all three probes (session 16 substrate-state finding); F_2_symmetric has probe1_overcrowding genuine + probe2/probe3 byte-identical shadow copies per FSS v1.1 §13.2
- The data-validity mask substrate-mechanical implementation from session 16 is available for use
- IF1, IF2 implemented and validated through `reg_01` per Phase 4B v1.1 §3.1; IF3 implemented but unvalidated for macro-transitions (not relevant for item 6a since IF3 is excluded)
- Q1 follow-up (SHA-256 hashes + flight2_production.py code excerpt for shadow-copy verification) was requested in session 16 and remains pending; the pre-registration treats it as non-blocking per Layer 2 revision 7, with escalation rule E4 as the safeguard against substrate-fact contradiction

## What this routing is not asking

- Not asking for new substrate-state engagement (Q1 follow-up is the outstanding substrate-state question and is non-blocking for execution per E4 mechanism)
- Not asking for pre-registration revision (pre-registration is committed; revisions go through new pre-registration drafting per escalation procedure)
- Not asking for Layer 3 architectural commitments (item 6a's interpretation_boundary explicitly excludes architectural arbitration; items 13, 14 are separate workstreams)
- Not asking for execution of items 6b, 6c, 13, 14 (each has its own future routing)

## Return format

Layer 3 produces the Stage 1 (EDA) implementation script as the first return; Layer 1 reviews; Mike arbitrates execution proceed. After Stage 1 executes, EDA outputs return through the EDA → Confirmatory checkpoint; only after Mike's arbitration on the checkpoint does Layer 3 produce the Stage 2 (confirmatory) implementation script.

— Routing drafted by Claude as Layer 1 central node, session 16, item 6a Layer 3 routing for execution (closes acceptance component 7), for relay to Layer 3 via Mike.
