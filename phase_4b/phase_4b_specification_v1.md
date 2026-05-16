# Phase 4B Specification v1

**Status:** Draft v1 for cross-layer review. Drafted from seeds per the orientation routing of 16 May 2026; no standalone Phase 4B specification document existed prior to this draft. Routes for Layer 2 (ChatGPT) and Layer 3 (Gemini) review before commitment.

**Scope:** This specification covers the analytical procedures that operate on Flight 2's empirical record (eight production .parquet files plus eight diagnostic CSVs). It does not specify the substrate code that produced those artifacts; that is covered by Flight 6 Substrate Specification v1.1.

**Provenance:** Drafted by Claude from four seed sources: (1) v1.1 substrate specification references to Phase 4B procedures (Section 2, Section 13.2, Section 14.2); (2) the cross-review commitment that Term_Lambda be required telemetry because Phase 4B requires probability-chain decomposition; (3) the Flight 2 diagnostic CSV schema as a working Tier 2 template; (4) the three Flight 2 substantive findings as load-bearing context. Layer 2 working notes from ChatGPT (16 May 2026 orientation reply) provided seeds for Tier 1 / Tier 2 / Tier 3 specifications, two-field classification value sets, and Flight 2 sufficiency mapping.

**Changes from prior state:** This is v1; no prior version exists.

---

## 1. Governing principles

Phase 4B separates three operations the substrate empirical record requires: verification, characterization, and inference. Each operates on the same .parquet artifacts but answers a different question.

**Verification** (Tier 1) asks: did the substrate do what v1.1 says it does? This is row-level and formula-level. Persisted telemetry columns must obey the substrate equations to specified tolerance. Verification produces pass/fail per artifact.

**Characterization** (Tier 2) asks: what cascade behavior did the substrate produce? This is aggregate and descriptive. Time series, epoch summaries, distributions, spatial diagnostics, F-form comparisons, scale comparisons. Characterization produces structured findings, not pass/fail.

**Inference** (Tier 3) asks: what does the cascade behavior license us to claim? This is regression-based, with pre-registered interaction families derived from v1.1's causal structure. Inference produces estimated effects, confidence intervals, and the two-field classification of what each estimated effect licenses architecturally.

The separation is load-bearing. Verification failures invalidate downstream characterization and inference. Characterization findings do not automatically upgrade to inferential claims. Inferential claims do not automatically upgrade to architectural closure — the two-field classification (Section 6) is the mechanism that prevents that upgrade.

**Pass/fail thresholds in Phase 4B come from v1.1 commitments, not from analytical convenience.** Tier 1 has pass/fail thresholds (the realization invariant under v1.1 Section 8 and Section 14.2; the substrate equations under v1.1 Sections 6-10). Tier 2 produces structured findings without forced adjudication. Tier 3 produces estimates with explicit uncertainty. Any analytical threshold not traceable to a v1.1 commitment is exploratory and must be flagged as such.

**Missing required telemetry is substrate failure, not analytical opportunity.** If a required column is absent from a Flight 2 parquet file, Phase 4B does not infer or impute. The substrate failure is surfaced for remediation. Derived columns are permissible only when explicitly specified in this document.

## 2. Tier 1 — strict matching

Tier 1 verifies that persisted telemetry obeys the substrate equations specified in v1.1 Sections 6-10. Tier 1 is row-level and formula-level. For each Flight 2 production parquet file, Tier 1 recomputes derived columns from persisted base columns and checks equality to specified tolerance.

### 2.1 Required verifications

For every row in every Flight 2 production parquet file (eight files; row counts per v1.1 Section 13.3):

**V1. Drive decomposition.**
```
Drive_Raw = Term_Lambda + Term_Density_Pos + Term_Overcrowding + Term_Offset
```

**V2. Term_Lambda definition.**
```
Term_Lambda = ALPHA · Lambda_total
```
where ALPHA = 4.0 per v1.1 Section 3.

**V3. Density terms.**
```
Term_Density_Pos = BETA · Local_Density
Term_Overcrowding = -DELTA · Local_Density²
Term_Offset = -GAMMA_OFFSET
```
where BETA = 3.0, DELTA = 4.0, GAMMA_OFFSET = 4.0 per v1.1 Section 3.

**V4. Probability chain.**
```
p_base = 1 / (1 + exp(-Drive_Raw))
p_act = p_base + ETA · (1 - p_base)
```
where ETA = 0.01 per v1.1 Section 3.

**V5. Realization invariant.**
```
is_active(t+1) = 1 ⟺ PRNG_draw(t) < p_act(t)
```
Per v1.1 Section 14.2, default verification granularity is full per-(cell, tick). Flight 2 closure recorded 0 mismatches across 12,000,000 row-level checks; Tier 1 re-verifies this from persisted .parquet values (not in-memory recomputation).

**V6. F-form computation.**
For F_LR runs:
```
Lambda_total = min(b_i_v, b_i_u, b_i_r)
```
For F_2_symmetric runs:
```
Lambda_multiplicative = b_i_v · b_i_u · b_i_r
Lambda_additive = W_V · b_i_v + W_U · b_i_u + W_R · b_i_r
Lambda_total = Lambda_multiplicative · Lambda_additive
```
where W_V = 0.33, W_U = 0.33, W_R = 0.34 per v1.1 Section 3.

**V7. Q update.**
```
Delta_v = GAMMA_Q · Psi_local
Delta_u = GAMMA_Q · Psi_local
Delta_r = GAMMA_Q · Psi_local
```
where GAMMA_Q = 0.001 per v1.1 Section 3. Q diagonal discipline (v1.1 Section 10) requires Delta_v, Delta_u, Delta_r logged separately even though they receive the same scalar update; Tier 1 verifies this separately for each column.

**V8. Pre-Q vs post-Q tick discipline.**
For consecutive ticks t and t+1 for the same cell, persisted b_i_v at tick t+1 must equal persisted b_i_v at tick t plus persisted Delta_v at tick t (within numerical clipping to [0, 1] per v1.1 Section 10):
```
b_i_v(t+1) = clip(b_i_v(t) + Delta_v(t), 0, 1)
```
Identical checks for b_i_u and b_i_r. This verifies the v1.1 Section 6 step 13 commitment that the row records pre-Q bases used to compute that row's Lambda and the Q updates produced in response to that row's Psi_local.

### 2.2 Tolerances

Floating-point equality uses absolute tolerance ε_strict = 1e-10 for recomputed columns. Rationale: NumPy float64 operations have machine epsilon ~2.2e-16; with double-precision substrate arithmetic, accumulated error across the verified operations should remain well below 1e-10. Larger tolerances should be flagged in Tier 1 output and investigated.

Where v1.1 Section 10 specifies clipping to [0, 1], the verification accommodates clipping: a row whose unclipped recomputation falls outside [0, 1] is verified against the clipped persisted value, and clipping events are counted separately per v1.1 Section 11.

### 2.3 Tier 1 output

For each of the eight Flight 2 production parquet files, Tier 1 produces:

```
Tier 1 Verification — {filename}
V1 (Drive decomposition): N rows, M mismatches at tolerance 1e-10
V2 (Term_Lambda): N rows, M mismatches at tolerance 1e-10
V3 (Density terms): N rows, M mismatches at tolerance 1e-10
V4 (Probability chain): N rows, M mismatches at tolerance 1e-10
V5 (Realization invariant): N rows, M mismatches
V6 (F-form): N rows, M mismatches at tolerance 1e-10
V7 (Q update): 3N column-rows, M mismatches at tolerance 1e-10
V8 (Pre-Q vs post-Q): N-1 consecutive-tick pairs per cell, M mismatches at tolerance 1e-10
Clipping events: v=K_v, u=K_u, r=K_r (matched to substrate-reported counts: yes/no)
Tier 1 verdict: PASS / FAIL
```

PASS requires zero mismatches across all eight verifications, modulo documented clipping. Any FAIL surfaces specific row identifiers (Tick, Agent_X, Agent_Y) for investigation; Tier 1 failure halts Phase 4B for that artifact pending substrate remediation.

### 2.4 What Tier 1 does not verify

Tier 1 verifies that the substrate did what v1.1 says it does on the artifacts produced. Tier 1 does not verify:
- The PRNG state evolution itself (verified by Flight 1 parity hashes).
- That v1.1 itself is the correct architectural commitment (architectural question, not verification question).
- Spatial diagnostic computations from the analysis CSVs (those are Tier 2 outputs, not substrate telemetry; their verification is against the analysis script specification, not v1.1).

## 3. Tier 2 — coarser matching

Tier 2 characterizes the cascade behavior produced by the substrate. Tier 2 is aggregate and descriptive. The Flight 2 diagnostic CSV schema is the working Tier 2 template; Phase 4B's Tier 2 specification standardizes that schema as the canonical characterization output for Phase 4B work going forward.

### 3.1 Required aggregate computations

For each of the four Flight 2 production runs (F_LR × {20×20, 40×40} and F_2_symmetric × {20×20, 40×40}):

**T2.1 Global time series.** Per-tick aggregates of ρ(t), Ψ(t), mean Lambda_total, mean Drive_Raw, mean p_act, mean Psi_local, mean b_i_v, mean b_i_u, mean b_i_r, std of each. The Flight 2 `global_timeseries.csv` is the working format; Phase 4B Tier 2 preserves this 17-column schema.

**T2.2 Epoch summaries.** Mean, std, min, max of T2.1 aggregates over seven epochs (epoch 0-99, 100-499, 500-999, 1000-1499, 1500-1999, 2000-2499, 2500-2999). The Flight 2 `epoch_summary.csv` schema is preserved.

**T2.3 Selected-tick distributions.** Quantile statistics (min, 5%, 10%, 25%, 50%, 75%, 90%, 95%, max, mean, std) for Lambda_total, Drive_Raw, p_act, Psi_local, b_i_v, b_i_u, b_i_r at eight selected ticks (t=0, 100, 500, 1000, 1500, 2000, 2500, 2999). The Flight 2 `selected_tick_distributions.csv` schema is preserved.

**T2.4 Psi sign decomposition.** Per-tick counts of cells with Psi_local < 0, = 0, > 0; per-tick conditional means of Psi_local within each sign group. The Flight 2 `psi_sign_decomposition.csv` schema is preserved.

**T2.5 Spatial diagnostics.** Moran's I for Psi_local; Moran's I for is_active; same-sign share for Psi_local; size of largest same-sign connected component for Psi_local. Computed at selected ticks per T2.3. The Flight 2 `psi_spatial_diagnostics.csv` schema is preserved.

**T2.6 Base-boundary summary.** Per-tick counts of cells with bases at or near boundaries [0, ε_boundary] and [1-ε_boundary, 1] for v, u, r; min and max bases per tick. The Flight 2 `base_boundary_summary.csv` schema is preserved.

**T2.7 F-form comparison.** Per-epoch deltas of T2.1 aggregates between F_LR and F_2_symmetric runs at matched scale. The Flight 2 `fform_comparison.csv` schema is preserved.

**T2.8 Compression fingerprint.** Per-column compressed size in the .parquet file and per-column cardinality (distinct value count). The Flight 2 `compression_fingerprint.csv` schema is preserved.

### 3.2 Tier 2 output

For each of the four production runs, eight CSV files matching the Flight 2 diagnostic schemas. For Flight 2 specifically, the eight CSVs already exist and are the canonical Tier 2 output; Phase 4B Tier 2 verifies that the existing CSVs match the schema and updates the canonical record path. For future production runs under Phase 4B, the analysis script that produces these CSVs is itself subject to Layer 1 pre-execution review (per the discipline calibration from Flight 2 that analysis scripts gating Layer 2 review require Layer 1 review).

### 3.3 Pass/fail in Tier 2

Tier 2 does not produce pass/fail per ChatGPT's recommendation, with one exception: the realization invariant from v1.1 Section 8. If T2.4 or T2.5 reveal patterns inconsistent with the substrate equations Tier 1 verified, that surfaces a Tier 1 failure missed at row level. This is anomaly detection; it operates by characterization but produces a Tier 1 verdict, not a Tier 2 verdict.

Otherwise Tier 2 produces structured findings. The three Flight 2 substantive findings are the working example: F-form distinguishability is sharp and scale-stable; Q is slow but cumulatively consequential; no macroscopic Ψ coherence at A3 + U(0.6, 0.9) + 3000 ticks. Each is a Tier 2 finding derived from the Flight 2 diagnostic CSVs; each is structured (specific quantitative claims with scale and parameter context) rather than yes/no.

### 3.4 Forward extensibility

Tier 2's schema is extensible. New diagnostic columns may be added if motivated by Tier 3 inferential needs or by subsequent Cycle 2 substrate runs. Schema additions must be documented and routed for cross-layer review; silent schema drift is prohibited.

## 4. Tier 3 — interpretable regression with pre-specified interaction families

Tier 3 produces estimated effects with explicit uncertainty, using regression families pre-registered from v1.1's causal structure. Pre-registration is load-bearing: it prevents exploratory regression fishing and post hoc interaction selection. The pre-registered families enter the analysis before the regression is run.

### 4.1 Outcome variables

Tier 3 regressions use one of three outcome variables:

**O1. `is_active(t+1)`** — binary; regressed via logistic regression. Tests what cellular and contextual factors predict cellular activation.

**O2. `p_act(t)`** — continuous in [0, 1]; regressed via linear regression with logit-transformed outcome, or via beta regression. Tests what cellular and contextual factors produce the realized activation probability.

**O3. `ds(t) = is_active(t+1) - is_active(t)`** — categorical {-1, 0, +1}; regressed via multinomial logistic regression. Tests what factors predict state-change events.

Outcome variable selection is per analytical question; analyses must declare which outcome is used and why before fitting.

### 4.2 Pre-registered interaction families

Five pre-registered interaction families per ChatGPT's Layer 2 working notes:

**IF1. F-form × Λ pathway.**
- `F_variant × Lambda_total`
- `F_variant × Term_Lambda`

Architectural question: do F_LR and F_2_symmetric produce different cascade signatures through the Λ pathway, beyond what the unconditional F_variant effect captures?

**IF2. F-form × density pathway.**
- `F_variant × Local_Density`
- `F_variant × Local_Density²`

Architectural question: does the same density feedback behave differently once F-form has placed the run in a different activation regime?

**IF3. Q-history × time interaction.**
- `epoch × F_variant`
- `epoch × mean bases`
- `epoch × Psi_local` (optional)

Architectural question: how does Q-driven base drift modify cascade behavior over time, and does the modification differ by F-form?

**IF4. Base-structure interactions.**
- `b_i_v × b_i_u × b_i_r` (full three-way), or pairwise interactions only if theoretically motivated

Architectural question: does limiting-reagent behavior versus multiplicative-gated behavior produce distinguishable activation signatures at the cellular level?

**IF5. Scale interactions.**
- `scale × F_variant`
- `scale × rho_global`
- `scale × psi_global`

Architectural question: is observed F-form separation scale-stable or finite-size-driven?

### 4.3 Primary predictors

All Tier 3 regressions include as primary terms:
- `Lambda_total`
- `Local_Density`, `Local_Density²`
- `Term_Lambda`, `Term_Density_Pos`, `Term_Overcrowding`
- `p_act` (when not the outcome)
- `Psi_local`
- pre-Q bases `b_i_v`, `b_i_u`, `b_i_r`
- `F_variant` indicator
- `scale` indicator
- `epoch` or continuous `t`

### 4.4 Pre-registration protocol

For each Tier 3 regression run on the Flight 2 record:
1. Outcome variable named with justification
2. Primary predictors listed
3. Interaction families included (from IF1-IF5; subsets of IF3-IF5 are permitted with justification)
4. Sample restriction stated (which Flight 2 files, which tick ranges, which cells)
5. Estimation method stated (logistic, linear, beta, multinomial)
6. Standard error method stated (clustered by cell, by tick, by run, or sandwich)
7. Pre-registration is timestamped and committed before regression is fit.

Post hoc additions of predictors or interactions outside IF1-IF5 are exploratory; if performed, they are labeled exploratory and reported with the pre-registered analysis, not in place of it.

### 4.5 Tier 3 output

For each pre-registered regression:
- Coefficient table with point estimates, standard errors, confidence intervals
- Marginal effect plots for the interaction terms in the registered families
- Goodness-of-fit diagnostics (deviance, log-likelihood, classification accuracy for logistic outcomes)
- Pre-registration document attached as provenance

Tier 3 does not produce pass/fail. Tier 3 produces estimated effects that feed the two-field classification (Section 6).

### 4.6 What Tier 3 does not produce

Tier 3 does not produce architectural closure. A statistically significant interaction effect does not select F_LR over F_2_symmetric for Open Element 14. A null effect does not refute v1.1's commitment. The two-field classification is the discipline that prevents this category error.

Tier 3 also does not produce causal claims. Tier 3 regressions describe statistical structure in the Flight 2 record; that record was produced by the v1.1 substrate under known mechanisms, so the regression structure traces back to those mechanisms by construction. The interesting Tier 3 outputs are the relative magnitudes of effects (which interaction families carry the most signal) and the scale-stability of effects, not "is there an effect."

## 5. Cross-scale analysis

Cross-scale analysis compares 20×20 and 40×40 production runs to distinguish substantive cascade behavior from finite-size artifacts. Per ChatGPT's Layer 2 working notes:

- Mean-level signatures stable across scale → arise from F-form and cascade equations.
- Aggregate variance shrinks at 40×40 → consistent with finite-size scaling.
- Pattern at 20×20 but not at 40×40 → likely finite-size or realization-sensitive; not a substantive finding.
- Pattern strengthens at 40×40 → spatial structure or aggregation effect; investigate.
- Mean-stable + variance-reducing → supports scale-stable characterization.

### 5.1 Required cross-scale comparisons

For each F-form (F_LR, F_2_symmetric), Tier 2 aggregates at 20×20 and 40×40 are compared on:
- Mean ρ over each epoch
- Mean Ψ over each epoch
- Mean Lambda_total, Drive_Raw, p_act
- Std of ρ over each epoch
- Moran's I for Psi_local at selected ticks
- F-form deltas at matched scale (T2.7 outputs)

### 5.2 Cross-scale verdict

Each compared aggregate receives a cross-scale verdict from: `scale_stable`, `variance_reducing_only`, `scale_dependent_strengthening`, `scale_dependent_disappearing`, `scale_dependent_other`.

For Flight 2 specifically, the closure record names cross-scale F-form ratios as scale-invariant within 1%. Phase 4B Tier 2 cross-scale verdict for F-form distinguishability is `scale_stable` (means stable; variance reduces with N as expected). This is the working example.

### 5.3 What cross-scale analysis does not establish

Two scales (20×20 and 40×40) is the minimum for cross-scale comparison; it is not sufficient for finite-size scaling theory in the formal sense. Phase 4B's cross-scale analysis tests scale-stability of qualitative patterns, not the functional form of scaling. Claims about scaling exponents or thermodynamic-limit behavior require additional substrate runs at additional scales (deferred to future cycles).

## 6. Two-field empirical_result × structural_status classification

The two-field classification operates on Tier 2 findings and Tier 3 estimates. Each claim derived from Phase 4B work receives one value from each field.

### 6.1 Field 1: empirical_result

Describes what the data did. Permissible values:

- `matches_expected` — observed pattern matches a pre-existing architectural prediction or theoretical expectation
- `partially_matches_expected` — observed pattern matches some aspects of expectation, diverges on others
- `diverges_from_expected` — observed pattern contradicts an existing prediction
- `not_observed_under_tested_conditions` — pattern absent under the parameters/initial conditions/run length tested; framing prevents over-generalization to "doesn't happen"
- `not_tested` — claim's empirical content was not part of the run design
- `indeterminate` — data does not adjudicate; result depends on tolerance or sample restriction choices

### 6.2 Field 2: structural_status

Describes what the empirical result licenses architecturally. Permissible values:

- `substrate_verified` — Tier 1 confirmed substrate did what v1.1 says (verification finding, not substantive)
- `substantive_finding` — Tier 2 or Tier 3 result that materially informs architectural understanding within the tested regime
- `parameter_regime_finding` — finding bounded to the specific parameters tested; does not generalize without further runs
- `requires_additional_probe` — claim is engageable but needs substrate runs outside Flight 2's design (e.g., parameter sweep, repeat-seed, alternative initialization)
- `open_element_not_resolved` — claim engages a named open architectural element (e.g., Open Element 14) but is not the arbitration for it
- `out_of_phase_4b_scope` — claim requires work outside Phase 4B's analytical procedures (theoretical work, additional substrate runs, cross-paper arbitration)
- `architecture_not_tested` — claim presupposes an architectural commitment that Flight 2 did not exercise

The `out_of_phase_4b_scope` value is included per Claude's note in the orientation engagement: the two-field classification needs to handle "out of scope" distinctly from "in scope but not yet tested." This keeps Phase 4B honest about what its analytical procedures can and cannot adjudicate.

### 6.3 Discipline

The classification prevents two error modes:
- **Inferential creep:** treating a Tier 3 estimate or Tier 2 finding as architectural closure.
- **Scope inflation:** treating a Phase 4B finding as resolving an open element it does not actually adjudicate.

For each Phase 4B-derived claim, both fields are stated explicitly. Claims that resist clean classification (e.g., partial match on empirical_result and ambiguous structural_status) are flagged for cross-layer review rather than forced into a category.

### 6.4 Worked examples for Flight 2

| Claim | empirical_result | structural_status |
|---|---|---|
| Realization invariant holds across 12M rows | matches_expected | substrate_verified |
| F-form distinguishability is sharp and scale-stable | matches_expected | substantive_finding |
| F_2_symmetric is evaluable (Λ ≈ 0.32 >> ε_Λ) | matches_expected | substantive_finding |
| F_2_symmetric should be selected for Open Element 14 | not_tested | open_element_not_resolved |
| Q is slow but cumulatively consequential over 3000 ticks | matches_expected | substantive_finding |
| Q behavior beyond 3000 ticks | not_tested | requires_additional_probe |
| No macroscopic Ψ coherence at A3 + U(0.6, 0.9) + 3000 ticks | not_observed_under_tested_conditions | parameter_regime_finding |
| Macroscopic Ψ coherence emerges under other parameters | not_tested | requires_additional_probe |
| F-form ratios are scale-invariant within 1% (Flight 2 scales) | matches_expected | substantive_finding |
| Finite-size scaling functional form | not_tested | out_of_phase_4b_scope |
| Variance across PRNG seeds at fixed parameters | not_tested | requires_additional_probe |
| Nucleation under spatially-localized initial conditions | not_tested | requires_additional_probe |

The table is illustrative, not exhaustive. Phase 4B analyses populate the classification as findings emerge.

## 7. Flight 2 coverage map

This section maps Phase 4B procedures to whether Flight 2's empirical record can support them directly versus whether additional substrate runs would be required.

### 7.1 Directly supported by Flight 2

1. **Tier 1 verification (V1-V8)** — Flight 2 produced .parquet files with the 25-column telemetry; Tier 1 verifies each formula chain row-level.

2. **Tier 2 characterization (T2.1-T2.8)** — Flight 2 produced eight diagnostic CSVs matching the canonical Tier 2 schema; the CSVs exist and Tier 2 verifies schema match plus updates canonical paths.

3. **Tier 3 regressions on F-form × {Λ pathway, density pathway, scale}** — Flight 2 produced matched-seed runs across both F-forms at both scales; IF1, IF2, IF5 are supported.

4. **Tier 3 regression on Q-history × time** — Flight 2 produced 3000-tick runs with persisted base evolution; IF3 is supported.

5. **Tier 3 base-structure interactions** — Flight 2 produced cellular telemetry with pre-Q bases; IF4 is supported within the U(0.6, 0.9) initialization range.

6. **Cross-scale analysis between 20×20 and 40×40** — Flight 2 produced both scales for both F-forms.

7. **Two-field classification of Flight 2-derived claims** — every claim derived from items 1-6 receives the classification.

### 7.2 Not directly supported by Flight 2

1. **Repeat-seed variance estimation** — Flight 2 was matched-seed design. PRNG-realization variance cannot be estimated from a single seed per cell. Would require Flight 3a-style run.

2. **Parameter-space behavior beyond A3** — Flight 2 used locked A3 parameters (α=4, β=3, δ=4, γ=4, η=0.01). Parameter sweeps would require Flight 3c-style run.

3. **Nucleation behavior** — Flight 2 used random Bernoulli(0.5) activation initialization per v1.1 Section 5.3. Spatially-localized initialization would require Flight 3b-style run with substrate extension.

4. **Long-horizon Q behavior** — Flight 2 ran 3000 ticks per v1.1 Section 3 TICKS_PRODUCTION. Boundary-regime Q behavior would require longer runs.

5. **Final arbitration of Open Element 14** — Flight 2 characterized both F-forms under one regime but did not arbitrate F-form selection. Architectural arbitration is `out_of_phase_4b_scope` in the two-field classification.

6. **General coherence-emergence claims** — Flight 2 produced `not_observed_under_tested_conditions` for macroscopic Ψ coherence. Other parameters, initializations, or run lengths remain open architectural questions.

7. **Cross-substrate-version comparison** — Flight 2 was the first v1.1 production run. Comparison to prior substrate versions or to alternative implementations would require additional runs.

### 7.3 Phase 4B work licensed by Flight 2

Phase 4B v1 procedures licensed by Flight 2 are items 1-7 in Section 7.1. The procedures in Section 7.2 are named as Phase 4B-relevant but require substrate work outside Flight 2's scope; their `structural_status` is `requires_additional_probe` and they are deferred to future cycle decisions.

Phase 4B v1 does not block on items 7.2. The analytical work supportable from Flight 2 is substantial and can proceed.

## 8. Open items

Items deferred to subsequent Phase 4B iterations or cross-layer review:

**O1. Numerical tolerances for Tier 1.** The ε_strict = 1e-10 specification in Section 2.2 is Claude's draft. Layer 2 (ChatGPT) flagged tolerance specification as open in their orientation reply. Cross-layer review should confirm or revise.

**O2. Standard error method for Tier 3.** Section 4.4 lists clustered (by cell, tick, run) and sandwich as options. The choice has implications for inference under the spatially-correlated cellular structure that Ψ_local introduces. Cross-layer review needed.

**O3. Beta regression vs logit-transformed linear for O2 outcome.** Section 4.1 lists both. The choice affects boundary behavior of p_act near 0 and 1. Worth Layer 2 review of which is more interpretable for the cellular cascade context.

**O4. Whether Tier 3 includes interaction families beyond IF1-IF5.** Section 4.2 lists five pre-registered families derived from ChatGPT's Layer 2 working notes. Cross-layer review may identify additional architecturally-motivated families.

**O5. Pre-registration mechanism.** Section 4.4 requires pre-registration of Tier 3 regressions but does not specify where the pre-registration is committed (operations log? a dedicated `phase_4b/pre_registrations/` directory? a Mike-routed artifact?). Operational detail for future work.

**O6. Forward Tier 2 schema additions.** Section 3.4 permits Tier 2 schema extension. The first plausible extension is per-cell base trajectory clustering (do cells fall into characteristic Q-evolution clusters?), but no specific addition is in Phase 4B v1.

**O7. Whether the realization invariant Tier 1 check should re-verify Flight 2's existing 0-mismatch claim, or whether Flight 2's already-executed check suffices.** Section 2.1 V5 specifies re-verification; this may be redundant. Operational call for Layer 1 review.

## 9. Implementation prohibitions

Carried forward from v1.1 Section 15 with Phase 4B-specific extensions:

**P1. No inference of missing telemetry columns.** Already in v1.1 Section 15; carried forward unchanged.

**P2. No exploratory regression masquerading as pre-registered.** If a regression is fit with predictors or interactions not in the pre-registration document, it is labeled exploratory in Tier 3 output and not used for the two-field classification.

**P3. No upgrade of statistical significance to architectural closure.** A Tier 3 p-value below conventional thresholds does not arbitrate v1.1 architectural commitments. The two-field classification is the only path to structural_status.

**P4. No analysis-stage repair of substrate failure.** Already in v1.1 Section 15; carried forward unchanged.

**P5. No Tier 2 pass/fail thresholds not traceable to v1.1.** Section 1's source-of-thresholds rule applies.

**P6. No silent schema drift in Tier 2 outputs.** Section 3.4's documentation requirement applies.

**P7. No mid-analysis substrate substitution.** Phase 4B operates on the artifacts the substrate produced. If a substrate question arises during Phase 4B work, it surfaces as substrate failure or substrate scope question, not as Phase 4B analytical substitution.

## 10. Sources and canonical references

This specification implements analytical procedures referenced by:

- **Flight 6 Substrate Specification v1.1** (`flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf`) — Section 2 names Tier 1/2/3, two-field classification, cross-scale analysis; Section 13.2 names production .parquet outputs Phase 4B operates on; Section 14.2 names the realization-invariant verification granularity Phase 4B Tier 1 inherits.

- **Cross-review commitment for Term_Lambda** (Layer 2 originating, Layer 3 strengthening, integrated in v1.1 Section 16.2 item 5) — Term_Lambda required because Phase 4B requires probability-chain decomposition.

- **Flight 2 closure record** (`operations_log/2026-05-15_flight_2_closure.md`) — three substantive findings; eight production .parquet files; eight diagnostic CSVs as working Tier 2 template.

- **ChatGPT Layer 2 orientation reply** (16 May 2026) — seeds for Tier 1 verification list, Tier 2 schema preservation, Tier 3 interaction families (IF1-IF5), two-field classification value sets, cross-scale analysis verdict structure, Flight 2 coverage mapping.

- **Round 1 closure note** (`operations_log/2026-05-16_round_1_closure.md`) — Phase 4B opens as Path A consequence.

- **Phase 4B orientation routing to ChatGPT** (`chatgpt_routing_phase_4b_orientation.md`, 16 May 2026) — routing that produced ChatGPT's Layer 2 reply.

The Flight 2 .parquet files and diagnostic CSVs remain the canonical empirical record. Phase 4B procedures operate on them; they are not modified by Phase 4B work.

---

End of Phase 4B Specification v1.

Subject to:
- Layer 2 (ChatGPT) cross-review
- Layer 3 (Gemini) cross-review for implementation feasibility of Tier 1-3 analysis scripts
- Mike's commitment after cross-review convergence on commit-readiness
- Subsequent Layer 1 (Claude) review of Phase 4B implementation scripts before execution, per the discipline calibration that analysis scripts gating Layer 2 review require Layer 1 review

— Claude, drafted from seeds per the orientation routing of 16 May 2026
