# Item 6a Pre-Registration — F-form-relevant Characterization (v2)

**Pre-registration ID:** `item_6a_f_form_characterization`
**Document pair:** This Markdown document + `item_6a_f_form_characterization.yaml` (Phase 4B v1.1 §4.4 schema)
**Scope:** Phase 4B Tier 3 regression-based F-form-relevant characterization, per STANDING_ITEMS item 6a.
**Status:** v2 draft. Integrates Layer 2 substantive review (session 16, full cycle): revisions 1, 2, 3, 4, 5, 7 mechanical; revision 6 (IF5 status) arbitrated by Mike as Option B (sensitivity-version addition). Pending Layer 2 v2-acceptance pass and Layer 3 routing per item 6a acceptance components 6–7.

---

## 1. Purpose and scope

This pre-registration commits Phase 4B Tier 3 analyses for **F-form-relevant characterization** — the work item 6a names. The scope is bounded:

- **What this pre-registration does:** characterize how F_LR and F_2_symmetric produce different cascade behavior through the Λ pathway (IF1) and density pathway (IF2), using `logit(p_base)` as the canonical outcome per Phase 4B v1.1 §4.1 O2. Includes a pre-registered IF5 sensitivity version testing scale-interaction effects on F-form differentiation (per Layer 2 revision 6, Option B).
- **What this pre-registration does not do:** arbitrate F_LR vs F_2_symmetric for Open Element 14 (item 6c scope, outside_phase_4b_scope); commit Ψ-operationalization (item 13); commit Q-form (item 14); analyze Q-driven base evolution beyond row-level base predictors; substantively engage cross-probe F_2_symmetric comparisons (foreclosed by FSS v1.1 §13.2 shadow-copy structure).

**Substrate-supported scope clarification (per Layer 2 revision 5).** The current item 6a analysis does not estimate F-form-by-probe differential behavior. It estimates F-form-relevant characterization only within the substrate-supported `probe1_overcrowding` partition. The original item 6 history included cross-probe F-form adjudication language; this pre-registration over-corrects toward clarity by structurally restricting to the probe1_overcrowding partition and naming the restriction explicitly.

The interpretation_boundary clauses in the YAML schema make all exclusions explicit per acceptance components 2 and 4 (seven `does_not_adjudicate` clauses including the new transition-proxy clause from Layer 2 revision 2).

## 2. Pre-registration structure: Reading A+

This pre-registration follows **Reading A+** as arbitrated from Layer 2 round-3 review:

- **One document pair** (this Markdown + the companion YAML) covers both EDA and confirmatory stages
- **Binding EDA/confirmatory partition** internal to the document
- **Pre-specified locking criteria** for confirmatory parameters
- **Mandatory escalation rule** (Section 5 below) that triggers a second confirmatory pre-registration if EDA invalidates more than parameter values

The single-document structure matches Phase 4B v1.1 §4.4's pre-registration framing; the two-stage discipline is enforced internally rather than by document multiplication.

## 3. Stage 1 — Exploratory Calibration (EDA)

### 3.1 Stage 1 scope

EDA stage selects parameter values for the confirmatory stage's transition-proxy analyses. **EDA is explicitly non-adjudicative** for primary findings; its outputs feed parameter locks, not substantive claims.

### 3.2 EDA data partition

- **Calibration subset:** F_LR 20×20 and F_2_symmetric 20×20 production runs (both probe1_overcrowding files; the smaller-scale subset)
- **Held-out confirmatory subset:** F_LR 40×40 and F_2_symmetric 40×40 production runs (both probe1_overcrowding files; the larger-scale subset)
- **Validity mask applied:** `is_valid_probe_data` per shadow-copy handling rule in YAML schema. For this pre-registration's data files (probe1_overcrowding only across both F-forms), the mask evaluates to True for all rows — but the mask is implemented and applied as a discipline against later inclusion of additional probe files.

The 20×20-vs-40×40 partition supports two analytical purposes simultaneously:
- Calibration-stage parameter selection uses only 20×20 data (held-out 40×40 preserved for confirmatory)
- The held-out 40×40 data permits a built-in cross-scale check on confirmatory findings (a §5.1 cross-scale comparison emerges naturally from the partition)

### 3.3 Transition-proxy form

The transition-proxy form is committed in this pre-registration. Parameter values are EDA-stage calibration outputs.

**Committed proxy form:**

> First epoch in which the rolling-mean ρ exceeds threshold τ for Z consecutive ticks within a run.

Where:
- **ρ = per-tick fraction of cells with `is_active == 1`** (per §3.1 T2.1 specification). The construction reads the persisted `is_active` column at cell-tick granularity and aggregates to per-tick mean. **`is_active` is excluded from regression predictors** (see YAML `excluded_variables`) **but is the substrate base column for ρ construction.** The regression-exclusion and proxy-construction roles are operationally distinct (per Layer 2 revision 3).
- Rolling mean computed over window of size W ticks
- τ = threshold value in [0, 1]
- Z = consecutive-tick persistence requirement (positive integer)
- "Epoch" interpretation per §3.1 T2.2 boundaries (epoch 0-99, 100-499, etc.)

**EDA-calibrated parameters:** W, τ, Z. Allowed parameter search spaces:

- W ∈ {10, 25, 50, 100, 200} ticks
- τ ∈ {0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50}
- Z ∈ {5, 10, 25, 50, 100} ticks

The search spaces are bounded a priori; EDA cannot select parameters outside these ranges without triggering the escalation rule (Section 5).

**Substrate-mechanical computation:** Per Layer 3 substrate-state engagement (session 16), rolling-mean ρ is computable from persisted `is_active` columns via `compute_rolling_rho` (Layer 3 implementation, session 16). The implementation is substrate-mechanical (column derivation from persisted base data); the window size parameter is committed under EDA calibration in this pre-registration rather than inherited as an implementation default.

**Transition-proxy interpretation boundary (per Layer 2 revision 2).** The rolling-mean ρ proxy is a substrate-supported transition marker for Phase 4B characterization. It operates on the Λ→ρ side of the cascade (activation-density behavior). It does NOT operationalize the full Λ→ρ→μ(ρ)→Ψ cascade; it does NOT reach Ψ and therefore cannot claim the Regime II/III coherence transition. The seventh `does_not_adjudicate` clause in the YAML captures this boundary structurally.

### 3.4 EDA outputs

EDA stage produces:

1. **Rolling-ρ trajectories** for both 20×20 calibration runs (F_LR, F_2_symmetric) at the five candidate W values
2. **Threshold-crossing tables** at each candidate (τ, Z) combination, recording the first-crossing epoch per run per (W, τ, Z) combination
3. **Diagnostic visualizations** of rolling-ρ trajectories with candidate threshold lines overlaid
4. **Calibration report** documenting (W, τ, Z) selection per the locking rule below, OR an escalation report if no admissible combination satisfies the rule (E7)

EDA outputs are committed alongside the pre-registration with explicit `exploratory` flag per Phase 4B v1.1 §1 source-of-thresholds rule. They are NOT used for primary substantive findings.

### 3.5 Allowed EDA-stage tuning

Only the following are permitted as EDA-stage tuning:

- Selection of (W, τ, Z) from the pre-specified search spaces above
- Visualization parameter choices (axes, color schemes, plot annotations) for the diagnostic outputs
- Reporting granularity for the calibration report

NOT permitted as EDA-stage tuning (escalation rule triggers):

- Proxy form revision (e.g., switching to a different aggregation than rolling-mean ρ, or to a different threshold-crossing rule)
- Parameter search-space expansion
- Confirmatory outcome variable change
- Inclusion criterion change for data files
- Shadow-copy handling rule change
- Interpretation_boundary clause change
- Discretionary tie-breaking in (W, τ, Z) selection when the locking rule produces no unique combination (handled by E7)

## 4. Stage 2 — Confirmatory Characterization

### 4.1 Locking rule

**(W, τ, Z) values are locked at the end of EDA stage** under the following criteria:

1. **Visual stability across calibration runs.** Selected (W, τ, Z) must produce a rolling-ρ trajectory in which the first-threshold-crossing epoch is identifiable (i.e., not at trajectory boundaries) in BOTH calibration runs (F_LR 20×20 and F_2_symmetric 20×20).

2. **Parameter parsimony.** Among (W, τ, Z) combinations satisfying criterion 1, the smallest W and the largest Z (relative to candidate sets) are preferred. Rationale: smaller W preserves trajectory shape (less smoothing); larger Z reduces sensitivity to single-tick spikes. The largest τ that still produces an identifiable crossing in both runs is preferred (later, more discriminating threshold).

3. **Cross-F-form discriminability.** Selected (W, τ, Z) must produce a difference in first-crossing-epoch between F_LR and F_2_symmetric runs that is consistent across the 20×20 calibration runs (i.e., the same F-form crosses earlier in both 20×20 runs at the locked values).

4. **Escalation if no (W, τ, Z) satisfies all three criteria, OR if the locking rule cannot select a unique combination, OR if all admissible combinations produce vacuous/unstable transition markers.** See Section 5, triggers E1 and E7.

The locked (W, τ, Z) values are committed to a `calibration_locked.yaml` document under `phase_4b/pre_registrations/item_6a_f_form_characterization/` (subdirectory created for the pair) before any confirmatory analysis is run. Once locked, confirmatory analysis uses these values without further tuning.

### 4.2 Confirmatory data partition and analyses

**Confirmatory data:** F_LR 40×40 and F_2_symmetric 40×40 production runs (probe1_overcrowding files).

**Confirmatory analyses:**

1. **Primary regression IF1 (F-form × Λ pathway).** Linear regression of `logit(p_base)` on the predictor set in the YAML schema, with IF1 interaction predicates (`F_variant × Lambda_total`, `F_variant × Term_Lambda`) included. Cluster-robust standard errors per `cluster_run_tick`.

2. **Primary regression IF2 (F-form × density pathway).** Same predictor set, with IF2 interaction predicates (`F_variant × Local_Density`, `F_variant × Local_Density²`) included.

3. **Transition-proxy regression.** First-crossing epoch (per locked W, τ, Z) regressed on F_variant. Reports: per-run first-crossing epoch, F_LR vs F_2_symmetric difference, sensitivity to seed (matched-seed Flight 2 design limits this to N=1 per F-form per scale).

4. **Cross-scale comparison (descriptive verdict).** First-crossing epochs and IF1/IF2 coefficient estimates compared between 20×20 calibration runs and 40×40 confirmatory runs. Per Phase 4B v1.1 §5, cross-scale verdict assigned (scale_stable | variance_reducing_only | scale_dependent_strengthening | scale_dependent_disappearing | scale_dependent_other). **This analysis produces a descriptive verdict over separate per-scale fits; it is structurally distinct from the IF5 sensitivity-version regression in analysis 5, which produces interaction-coefficient estimates in a single combined regression.** (Distinction per Layer 2 revision 6.)

5. **IF5 sensitivity regression (per Layer 2 revision 6, Option B).** Linear regression of `logit(p_base)` on the predictor set plus IF5 sensitivity predicates (`scale × F_variant`, `scale × Lambda_total`, `scale × Local_Density`), using both 20×20 and 40×40 confirmatory-stage data jointly. Reports: IF5 interaction coefficients with standard errors and confidence intervals; comparison of F-form effects estimated with vs without IF5 sensitivity terms. **This sensitivity does NOT elevate scale-stability to a main claim; it tests whether F-form differentiation and the Λ/density pathway effects vary across scale.**

### 4.3 Sensitivity checks

Pre-registered sensitivities (in addition to IF5 sensitivity regression above):

- **Cell-level clustering** (per YAML `uncertainty_method.sensitivity_checks`) as alternative to `cluster_run_tick`
- **IF1 sensitivity version** (Q-history modulation): activated if primary IF1 surfaces epoch-conditional effects within a single F-form; pre-registered predicates per YAML
- **IF2 sensitivity version** (density threshold): activated only as exploratory diagnostic; explicitly non-adjudicative for primary IF2 claims; pre-registered predicates per YAML

### 4.4 Confirmatory output

Per Phase 4B v1.1 §4.5:

- **Markdown report** at `phase_4b/reports/item_6a_f_form_characterization.md` containing: regression specification recap, coefficient tables with point estimates / SEs / CIs (primary IF1, primary IF2, IF5 sensitivity), marginal effect plot references, goodness-of-fit diagnostics, interpretation against this pre-registration's interpretation_boundary, transition-proxy first-crossing analysis, cross-scale verdict assignment, two-field classification of all primary findings
- **Structured CSV tables** at `phase_4b/reports/item_6a_*.csv` for coefficient tables, marginal effects, transition-proxy results, cross-scale comparison, IF5 sensitivity results

No Jupyter notebooks per Phase 4B v1.1 §4.5 / P8.

## 5. Escalation rule

If during EDA stage execution OR review of EDA outputs, any of the following conditions hold, **the confirmatory stage of this pre-registration is suspended** and a separate confirmatory pre-registration is required before any confirmatory analyses are run:

**E1.** No (W, τ, Z) in the pre-specified search spaces satisfies all three locking criteria in Section 4.1.

**E2.** EDA reveals that the rolling-mean ρ proxy form is structurally inadequate (e.g., the rolling-mean trajectory is non-monotonic in a way that makes "first crossing" ambiguous; OR a different proxy form is substantively more appropriate per EDA findings).

**E3.** EDA reveals that the confirmatory data partition (F_LR 40×40 + F_2_symmetric 40×40) is inadequate for the substantive question (e.g., 40×40 trajectories are qualitatively different from 20×20 in a way that EDA cannot bridge).

**E4.** EDA reveals that the shadow-copy handling rule (validity mask) requires revision based on substrate facts not anticipated at this pre-registration's drafting (including substrate facts from the pending Q1 follow-up if they contradict the structural claim).

**E5.** EDA reveals that the interpretation_boundary clauses in the YAML schema require revision (e.g., a finding is empirically engaged that the boundary clauses said this pre-registration would not engage).

**E6.** EDA reveals that the regression predictor set or excluded_variables in the YAML schema requires revision based on substrate facts (e.g., a collinearity or substrate-equation identity not anticipated at drafting).

**E7 (added v2 per Layer 2 revision 1). Calibration non-identifiability or degeneracy.** If the EDA stage cannot select a unique or pre-specified tie-broken W/τ/Z combination under the locking rule, OR if all admissible combinations produce unstable, vacuous, or non-informative transition markers, the confirmatory stage is paused and a second confirmatory pre-registration is required. **This trigger fires distinctly from E1**: E1 catches the case where no combination satisfies the criteria at all; E7 catches the case where multiple combinations satisfy the criteria but no principled selection emerges from the locking rule, OR where combinations satisfying the criteria still produce degenerate transition markers (vacuous = no first-crossing within trajectory; non-informative = first-crossing values cluster at trajectory boundaries; unstable = small parameter perturbations produce large changes in first-crossing values). Without E7, the locking rule could become discretionary at the point where Reading A+ depends on binding discipline.

**Escalation procedure:**

1. EDA stage closes with explicit non-adjudicative outputs and an escalation report documenting which trigger fired and why
2. The closing of EDA stage is committed alongside the EDA outputs
3. A second confirmatory pre-registration is drafted under `phase_4b/pre_registrations/item_6a_f_form_characterization/confirmatory_v2.yaml` (and companion .md) addressing the surfaced issue, with its own Layer 2 full cycle and Layer 3 routing
4. Confirmatory analyses use the new pre-registration, not this one

The escalation rule is the structural safeguard against "pre-registration drift" (treating a confirmatory stage as substantively pre-registered when EDA findings have effectively rewritten its content). Without the escalation rule, Reading A's single-document compactness would be vulnerable to soft-revision of the confirmatory stage. The seven explicit triggers (E1–E7) catch the failure modes Layer 2 and Layer 1 have anticipated.

## 6. Rationale for IF1 + IF2 primary mapping with IF5 sensitivity

The IF1 + IF2 primary mapping plus IF5 sensitivity-version scope (per Mike's session 16 arbitrations on both the original scope and Layer 2 revision 6) reflects:

**IF1 + IF2 primary.** Conservative interpretation of "F-form-relevant characterization." F-form × Λ pathway and F-form × density pathway are the most directly substrate-grounded interactions for the architectural question item 6a engages.

**IF3 (Q-history × time) excluded entirely.** Item 6a's STANDING_ITEMS acceptance 1 allows IF3 as time/epoch interaction without Q-form claims, but Layer 2 substantive review explicitly endorsed excluding IF3 on the grounds that it risks smuggling Q-history claims back into a draft that does not commit Q-form. Epoch enters only as primary categorical control; if epoch-conditional patterns surface in IF1 primary results, the pre-registered IF1 sensitivity-version (Q-history modulation) can be activated.

**IF4 (base structure) excluded.** Cellular-level F-form mechanism analysis that more directly engages Open Element 14 arbitration (item 6c scope).

**IF5 (scale interactions) as sensitivity, not primary (Layer 2 revision 6, Option B; Mike's arbitration).** Two structural considerations:
- The 20×20→40×40 confirmatory design uses cross-scale data; without IF5 in any form, the cross-scale comparison (analysis 4) could be misread as a formal scale-interaction test
- IF5 as primary would elevate scale-stability to a main item 6a claim; the §6.4 worked-example claim "F-form distinguishability is sharp and scale-stable" is then a primary finding rather than a descriptive verdict
- IF5 as sensitivity protects against the misreading risk without expanding the primary claim surface: the IF5 sensitivity regression (analysis 5) produces interaction coefficients reported alongside primary findings; the cross-scale comparison (analysis 4) produces a verdict over per-scale fits. The two outputs play distinct roles

The trade-off versus IF1 + IF2 only: modest expansion in YAML's `sensitivity_versions` block; one additional confirmatory analysis (analysis 5); modest expansion in interpretation_boundary to clarify IF5 sensitivity's role (substantive characterization, not Open Element 14 adjudication).

## 7. Outstanding substrate verification (non-blocking, per Layer 2 revision 7)

This pre-registration was drafted before the Layer 3 Q1 follow-up return (substrate verification of shadow-copy structural claim via SHA-256 hashes and `flight2_production.py` excerpt). The structural claim that F_2_symmetric probe2/probe3 are byte-identical shadow copies of probe1 is supported by:

- Layer 3 substrate-state engagement (session 16): SHA-256 hash analysis on F_2_symmetric probe1/2/3 returning identical hashes; F_LR probe1/2/3 returning distinct hashes
- FSS v1.1 §13.2 citation in STANDING_ITEMS item 6a acceptance 3 (primary source)
- Phase 4B v1.1 §7.1 supporting the matched-seed design across F-forms at both scales

**The pending Q1 verification is non-blocking for drafting because the pre-registration already restricts analysis to the substrate-distinct partition (probe1_overcrowding files only for F_2_symmetric) and contains an escalation trigger (E4) if the shadow-copy substrate claim is contradicted.** The non-blocking treatment is defensible because the structural safeguards (partition restriction + E4) protect the analysis against substrate-fact contradiction; it is not casual deferral. (Per Layer 2 revision 7.)

If the Q1 follow-up surfaces a substrate fact that contradicts the structural claim, E4 fires; this pre-registration's shadow_copy_handling rule and data_files scope require revision before commit.

## 8. Acceptance map

Mapping of this pre-registration pair (YAML + this Markdown) to STANDING_ITEMS item 6a acceptance components:

| Acceptance | This pre-registration |
|---|---|
| 1. Pre-registration committed under `phase_4b/pre_registrations/` using Phase 4B v1.1 tier/IF vocabulary, following eight-field YAML schema per §4.4 | YAML document (this pair) |
| 2. Explicit `interpretation_boundary.does_not_adjudicate` clause naming Open Element 14 architectural selection per Phase 4B v1.1 §6.4 | YAML `interpretation_boundary.does_not_adjudicate` first entry; seven clauses total in v2 |
| 3. Explicit shadow-copy handling rule per FSS v1.1 §13.2 | YAML `interpretation_boundary.shadow_copy_handling`; Markdown Sections 3.2 and 4.2 |
| 4. Explicit distinction between exploratory calibration and confirmatory characterization | Markdown Sections 3, 4, 5 (Reading A+ with seven-trigger escalation rule including E7) |
| 5. Trajectory and transition-proxy metrics restricted to substrate-supported comparisons | YAML `data_files` (probe1_overcrowding only for F_2_symmetric); validity mask; Markdown Section 3.2; substrate-supported scope clarification in Markdown Section 1 |
| 6. Layer 2 full cycle complete on the pre-registration | Substantive review complete (session 16); v2-acceptance pass pending on this v2 draft |
| 7. Layer 3 routing in hand for execution against Flight 2 canonical substrate | Pending; routing draft follows v2-acceptance closure |

## 9. v2 changelog

v2 changes from v1 draft, per Layer 2 substantive review (session 16):

1. **E7 added (Layer 2 revision 1).** Section 5; calibration non-identifiability or degeneracy as seventh escalation trigger.
2. **Seventh `does_not_adjudicate` clause added (Layer 2 revision 2).** YAML; transition-proxy non-equivalence to true regime transition; explicitly bounded to Λ→ρ side of cascade.
3. **`is_active` use clarification (Layer 2 revision 3).** YAML `excluded_variables` rationale expanded; new `predictors.proxy_construction` block; Markdown Section 3.3 explicit on ρ construction from `is_active`.
4. **η-floor inversion as deterministic reconstruction (Layer 2 revision 4).** YAML `outcome.construction.nature` and `nature_clarification` added; Rule 7 protection explicit.
5. **Substrate-supported scope language strengthened (Layer 2 revision 5).** Markdown Section 1 over-correcting toward clarity on probe1_overcrowding partition restriction; YAML `data_files` comment expanded.
6. **IF5 as sensitivity (Layer 2 revision 6, Option B; Mike's arbitration).** YAML `interactions.sensitivity_versions.IF5_sensitivity_scale_interaction` added with three predicate predicates; Markdown Section 4.2 analysis 5 added; Markdown Section 6 rationale expanded; not-included IF5_primary entry added.
7. **Q1 follow-up non-blocking justification strengthened (Layer 2 revision 7).** YAML `shadow_copy_handling.non_blocking_q1_followup_justification` added; Markdown Section 7 rewritten with structural-safeguards-not-casual-deferral framing.

---

— Drafted by Claude as Layer 1 central node, session 16, item 6a pre-registration v2 (YAML + Markdown pair). Integrates Layer 2 substantive review findings (revisions 1-5, 7 mechanical; revision 6 arbitrated by Mike). Pending Layer 2 v2-acceptance pass per acceptance component 6, and Layer 3 routing per acceptance component 7.
