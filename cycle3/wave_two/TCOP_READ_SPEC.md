# Two-channel ordering probe — read spec (CANONICAL)

**Status: CANONICAL. Mike-arbitrated 2026-07-06: A1–A5 all resolved as jointly recommended (L1+L2). Lineage: L1 draft v1 → L2 attack (reject-as-ratification-ready; 5 major defects; replacement texts supplied; A1–A4 recommendations) → L1 full-acceptance merge v2 with five disclosed refinements D1–D5 → L2 fidelity pass CLEAN (no fidelity failures; D1–D5 all accepted; A5 lexicographic form preferred by L2 over its own earlier either-or wording as the stricter rule) → Mike arbitration 2026-07-06 (A1–A5 as recommended) → this placement form. NON-EXECUTING: this spec does not run the read; execution is Mike's, on the Section 11 sequence. Governed by TWO_CHANNEL_ORDERING_PROBE_CONTRACT.md (8c94d8c), THRESHOLDING_ADDENDUM.md (8a777e6), TWO_CHANNEL_ORDERING_PROBE_DESIGN_RESOLUTION.md (Sections 1–6 verbatim binding), THRESHOLD_FIXING_READ_SPEC_v2_1.md conventions; committed findings files > resolution > contract+addendum > this spec. Numeric ground: threshold_fixing_read_results.json (v3) at full float precision.**

**Arbitration record (Mike, 2026-07-06): A1 — CM-0 dominance: conservative three-component form (correlation, slope, variance each strictly exceeding matched CM-0 maxima; D1 max(0,·) well-definedness folded). A2 — onset aggregation: k_onset=2, s_onset=3, with the sentinel layer. A3 — G4 row-pass: strict all-primary-block conjunction, no tail tolerance. A4 — earned-window: Branch A, max-observed floors operative; Branch B named-not-triggered. A5 — differential tracking: lexicographic burden ordering (operative rule).**

**Disclosed refinements register (all L2-accepted at the fidelity pass):**
- **D1 (Section 3.1):** CM-0 dominance thresholds defined as max(0, max signed value); if 0, the frozen G1 floor thresholds remain the binding constraint. Well-definedness repair following the floor-null max(0, max) precedent.
- **D2 (Section 4.3):** c=0 enters the path (b) comparison universe as the sign-neutral zero endpoint of both sign families, making the tracking rule's matched c=0 side executable.
- **D3 (Section 7):** differential-tracking burden is lexicographic: not worse on in-bin exceed count AND strictly better on at least one of (count, mean residue excess). Arbitrated operative as A5.
- **D4 (Section 4.2):** the contract's "predeclared G4 slope attenuation allowance" was never emitted by the thresholding stage; no allowance exists, none is applied, none may be invented at read time.
- **D5 (Sections 3.2, 7):** sentinel events are recorded in a dedicated JSON section and surfaced in the findings record — never suppressed — but do not halt execution; findings-layer, not fail-closed-layer.

## 0. What this read is and is not

This is THE READ: the first and only evaluation of the committed TCOP dataset (180 CM-1 + 135 CM-0 runs, a4fb946) against the frozen addendum. It evaluates gates; it never tunes them. No threshold, floor, ceiling, bin width, bin origin, count rule, comparison family, or dominance rule may be derived from, adjusted by, or selected in light of any CM-1 or CM-0 statistic. Every constant was frozen at 8a777e6 before any probe output existed; every rule is fixed in this spec before any CM-1/CM-0 comparison is computed. No rerun with a different control RNG seed to move any outcome (no-rerun discipline, binding). Candidate language enforced: the probe PRODUCES or FAILS TO PRODUCE; axis-specific outcomes per co-equal observable; "falsified" only as parenthetical shorthand in private notes. No outcome reclassifies Comparator 0, moves L4, closes Rule E B/C, closes the CM-2 hold, or closes any mechanism class. No density-stability claim (Λ=0.40 single anchor; Λ=0.20 named-not-triggered).

## 1. Inputs and fail-closed manifest

Inputs: `c3_w2_tcop_blocks.csv`, `c3_w2_tcop_windows.csv`, all 315 TCOP state NPZs, `c3_w2_tcop_preflight.json`, `threshold_fixing_read_results.json` (v3), and the committed helper source for reconstruction. The read records SHA-256 digests for every file consumed, its own digest, and the preflight script digest (466455f2…b7e7) for lineage.

**Structural verification (all fail closed):** 5040 block rows and 4095 window rows verified by full decomposition — by mode, tier, c_label, seed, block/window index, and primary-family flag; CM-1 = 180 runs, CM-0 = 135 runs; every run has exactly 16 block rows, 13 window rows, and one (400,50,50) NPZ; the three solved u_const values verified against c3_w2_tcop_preflight.json (0.04977134874876729 / 0.12339551870278656 / 0.24248438819907564) before any CM-0 comparison is computed; threshold values restated in this spec verified against the JSON. Any missing file, shape/row-count/decomposition mismatch, digest failure, or threshold mismatch halts the read; nothing is emitted.

## 2. Read constants and conventions (fixed here)

- **Read-control RNG seed: 20260706, frozen.** PERMUTATIONS = 199. No rerun to move any outcome.
- **Quantile discipline:** every quantile carries an explicit method string; method="lower" for small-sample order statistics.
- **Primary families:** primary blocks 3–14; primary windows = starts at ticks {75,100,125,150,175,200,225,250,275}, 9 per seed, phase-balanced 3/3/3. Block 15, blocks 0–2, non-primary windows: diagnostics only; flags govern selection; no default slicing includes block 15.
- **Axis-specific controls (canonical):** Ψ_meanI_state residue = per-cell independent time shuffle (axis=0, the v3-repaired orientation); Ψ_persistence_I residue = spatial permutation of the persistence grid (committed compute_persistence_null convention). Residue = abs(raw_stat − mean_control_stat). The time-shuffle persistence residue is algebraically zero, diagnostic-only if computed, never the operative persistence gate. The read script includes the invariance demonstration as a self-check (must return True) before any residue is used.
- **Reconstruction convention (binding):** p_become(t) reconstructed from states[t] as the field that would update t→t+1; no draw, no advance; committed helpers imported or reproduced byte-for-byte, copied source recorded in-script; approximate re-vectorization prohibited. CM-1 rows: logit(p_Λ) + u_t(block) + κ(2q−1) with the row's frozen schedule. CM-0 rows: the row's selected solved offset.
- **Gate-source discipline:** NPZ reconstruction is the SOLE gate source for every gate-bearing quantity. Recorded CSV columns are exhaustively cross-checked (Section 8) and serve as diagnostics; any CSV column not exhaustively verified is labeled diagnostic-only in the JSON. The five `*_APPARATUS_ONLY` window columns are machinery, never findings, read only for degeneracy fencing.
- **Schedule ground truth and invariant checks:** the `u_t` block-CSV column is verified against in-script regeneration of the frozen schedule (L(b) = [0, u/2, u][b mod 3], cycle start block 0) for every CM-1 row, and against the selected solved offset for every CM-0 row; `schedule_phase` is verified equal to block_idx mod 3 for every block row. Mismatch fails closed.
- **Vocabulary (binding):** "zero-mode driver imprint" primary label; unqualified "synchrony" excluded; lift always written as lift without SPATIAL/DIFFERENTIAL organization; "dominance" outcome-language only; no κ-as-μ(ρ) language; no claim that c remained constant under drive unless `driven_realized_contrast_mean/range` show it.

## 3. Rules fixed before any CM-1/CM-0 comparison

### 3.1 CM-0 dominance rule (G1(iv); immutable; Mike-arbitrated A1)

For each nonzero CM-1 row at (c_label, tier, seed), the matched CM-0 comparator cell is: same c_label, the solved static offset for that tier, all five canonical seeds. For each matched CM-0 run, compute the identical block-ρ regression against the centered three-level template over primary blocks 3–14 at the three circular phase alignments (all false alignments by construction).

The comparator set emits: 15 signed correlations, 15 signed slopes, and 5 block-ρ variances (ddof=0, phase-independent). The operative CM-0 thresholds are (D1): **max(0, maximum signed correlation)**, **max(0, maximum signed slope)**, and **the maximum block-ρ variance**. Negative anti-phase CM-0 alignments are reported but do not define the positive driver-imprint threshold; if no matched signed value is positive, the operative dominance threshold is 0 and the frozen G1 floor thresholds remain the binding constraint.

A CM-1 row satisfies G1(iv) only if, at the construction phase, its correlation, positive slope, and block-ρ variance each STRICTLY exceed the corresponding matched CM-0 maximum. If any matched CM-0 row is missing, malformed, digest-mismatched, or otherwise invalid, the matched comparison FAILS CLOSED; the read does not trim the comparator set.

Execution-order enforcement: the read script computes and digest-freezes all CM-0 comparator sets (an intermediate emission recorded in the JSON) BEFORE loading any CM-1 row. No CM-0 statistic is selected, trimmed, or reweighted after any CM-1 statistic is seen. The 15-point coarseness is recorded as an apparatus limit, not a precision claim.

### 3.2 Onset aggregation under max-observed floors (Mike-arbitrated A2, A4)

**Branch A operative (A4):** the 9-window earned-window rule remains UNVERIFIED; MAX-OBSERVED is the operative per-window onset floor on both raw and residue, per axis: meanI raw 0.001990247078984684 / residue 0.0021133919208696263; persistence raw 0.022837296913806253 / residue 0.023108397313261055. The 97.5th-percentile values travel alongside as diagnostics only and license nothing. Branch B — verification of the 9-window earned-window rule — remains NAMED-NOT-TRIGGERED and requires separate Mike authorization for any additional floor-family execution.

**Per-window exceedance (axis-specific):** a primary window exceeds on an axis iff raw magnitude is strictly above the axis raw floor AND the axis-appropriate residue is strictly above the axis residue floor. Z travels alongside, never sufficient. Conjunctive-across-axes onset PROHIBITED; each axis evaluated and recorded independently.

**Sentinel exceedance (D5):** any above-floor primary-window exceedance is recorded as a sentinel event with axis, row, seed, window, schedule phase, signed raw value, residue value, z-score, and matched-ρ / gate context. Sentinel events do not by themselves create a setting-level onset flag, but they may not be suppressed from the risky-form record, especially at κ≈0. Sentinels are recorded in a dedicated JSON section and surfaced in the findings record; they do not halt execution.

**Row-level onset flag:** per (tier, c_label, seed, axis), row onset requires at least **k_onset = 2** primary-window exceedances on that axis. The phase distribution of exceeding windows is reported.

**Setting-level onset flag:** per (tier, c_label, axis), setting onset requires at least **s_onset = 3** of 5 seeds carrying the row-level flag. This is the ONLY setting-level onset flag licensed while the earned-window rule remains unverified. Window counts per row and per setting are always reported alongside flags.

## 4. Gate evaluation

### 4.1 G1 — schedule imprint (row-level; nonzero CM-1 tiers only; u=0 excluded)

Per nonzero CM-1 row: regress NPZ-reconstructed block-mean ρ on the centered frozen schedule over primary blocks 3–14 at the lag-0, construction-phase convention (phase fixed at block 0; best-lag prohibited; lag ±1 diagnostic only). Report signed slope, covariance amplitude, Pearson correlation, block-ρ variance (ddof=0), schedule phase. PASS iff jointly: slope > 0; correlation > 0.7840162452332338; slope > 0.0026279999999999915; AND the Section 3.1 dominance rule holds. Correlation without amplitude is no driver imprint; overdispersion without phase-locked response is no driver imprint. G1b floor variance (> 4.469162666666656e-06) reported per row as necessary-not-sufficient; never substitutes for dominance. G1 failure = apparatus limit for common-mode-lift claims: recorded, never dropped, never evidence.

### 4.2 G2 — differential reach (D4 folded)

prop_I is the full-surface Moran's I of the reconstructed becoming-active propensity field, computed per primary block and aggregated per row as the mean over primary blocks. The inactive-cell-masked value is diagnostic only.

At c = 0, the propensity field is spatially constant by construction. The read records `zero-variance / non-identifiable, consistent with spatially constant` (spatial variance below machine-scale ε, fixed in-script and recorded); it does NOT insert a numeric zero into the trend sequence and never records a numeric prop_I from a degenerate Moran denominator.

**Endpoint activation condition:** per nonzero tier and sign, the lower empirical support across the five seed-level row means at |c| = 0.35 must clear the sign-specific frozen floor: 0.3832176592110196 (c>0) / 0.38138345899890086 (c<0). **(D4):** the contract's "predeclared G4 slope attenuation allowance" was never emitted by the thresholding stage; no allowance exists, none is applied, none may be invented at read time — the frozen floors apply unadjusted.

**Trend condition:** evaluated per tier, per sign, ACROSS the seed set, over the nonzero magnitudes {0.05, 0.10, 0.20, 0.35}. Operative trend statistic, fixed before execution: the median row-level prop_I AND the lower-support row-level prop_I must be nondecreasing with |c|, with the |c| = 0.35 endpoint clearing the activation floor. Per-seed non-monotone steps are reported as diagnostics and may narrow interpretation, but per-seed strict monotonicity is NOT the gate. Signs never pooled to manufacture monotonicity. A sign failure is explicitly reported. If G2 fails for a sign/tier, that region FAILED TO ACTIVATE the differential channel; no ordering failure is readable there.

### 4.3 G3 — matched-ρ / common-support (D2 folded)

**Bin grid, fixed before any comparison:** global, half-open intervals on window_mean_rho, origin rho_origin = 0.35, width Δρ_match = 0.002827351608578471, spanning [0.35, 0.55]. Bin k = [0.35 + k·w, 0.35 + (k+1)·w). No pair-specific or sliding bins. A window belongs to exactly one bin; windows outside the band are out-of-support (apparatus admissibility, reported, never dropped silently).

**Comparison universe, fixed before evaluation:**
1. Path (a): all c = 0 tier pairs among u ∈ {0, 0.10, 0.25, 0.50}.
2. Path (b) (D2): within each nonzero tier, per sign, all pairs (c_low, c_high) with |c_low| < |c_high| drawn from {0, 0.05, 0.10, 0.20, 0.35}, where c = 0 enters as the sign-neutral zero endpoint of both sign families; plus the feasibility audit's predeclared path_a_best_pairs / path_b_best_pairs.
3. Any additional pair class must be listed in this spec before execution or it is diagnostic only.

For every pair in the universe, EVERY global ρ bin is evaluated and reported as: eligible, count-failed, seed-failed, phase-confounded, or out-of-support. Eligibility requires jointly: N_bin_min = 9 primary windows per side per bin; S_bin_min = 3 seeds per side; no single seed > half the qualifying windows on either side; and the phase rule (phase-stratified explicitly, or window-start phase histograms match within one window per phase, else common-support-present-but-phase-confounded and excluded from ordering claims). The read may not select only favorable bins after seeing organization statistics; nothing is relaxed after output. Setting-level mean differences and IQR-plus-pooled-SD overlap are descriptive only. The stratified read is primary: organization as a function of BOTH ρ and prop_I; no κ-tracking claim off an un-stratified sweep.

### 4.4 G4 — compression / slope audit (Mike-arbitrated A3)

Per primary block, from the reconstructed field: mean_slope = mean_i[p_i(1−p_i)], q05_slope, tail_mass (fraction outside [0.05, 0.95]), p_min, p_max, mean_p. **Row pass:** a row is G4 in-band iff across ALL primary blocks: min(mean_slope) ≥ 0.22556575062981687 AND min(q05_slope) ≥ 0.19883692760900232 AND max(tail_mass) ≤ 0.0. Because tail_mass is a discrete fraction of cells, NO floating tolerance is applied to the count: any cell with p_i < 0.05 or p_i > 0.95 creates positive tail mass and fails the row. Near-threshold margins for all three quantities are reported. p̄(1−p̄) is a summary only, never sufficient. G4 failures are fenced apparatus limits.

## 5. Onset evaluation (axis-specific; Section 3.2 rules; signed discipline)

For every run (CM-1 all tiers including u=0, and CM-0), per primary window, per axis: raw Ψ (NPZ-recomputed) and axis-appropriate control residue (199 permutations, seed 20260706, frozen). Per-window exceedance, sentinel record, row-level flag (k_onset), setting-level flag (s_onset), all counts reported. Z from the committed null machinery travels alongside, never sufficient; raw travels with z; residue travels with raw.

**Signed effect discipline:** onset thresholds are applied to magnitudes, but every onset record also carries the signed raw value and signed residue/excess where defined. Positive, near-null, and negative anti-structured outcomes are recorded separately. A magnitude exceedance is never automatically described as positive organization. Onset outcomes recorded per axis; no pooled observable; neither observable named theoretical Ψ.

## 6. Decomposition read, zero-mode diagnostics, and the stratified read

The decomposition is the core of the instrument, per (tier, c_label, seed): (i) common-only contribution — verified per Section 4.2's zero-variance handling, never assumed; (ii) differential/full-surface contribution — reported against |c| per sign; (iii) realized state/persistence observables — reported against both ρ and prop_I strata. Outcome language only throughout. Zero-mode diagnostics per row: ρ_t overdispersion, autocorrelation, block-timescale modulation, schedule cross-correlation. The schedule-conditional read (organization conditioned on within-cycle schedule level via u_t) is descriptive only — never a gate, never an onset criterion. The factorization diagnostic prop_I(u,κ) ≈ f(u)·g(κ) is an EXPECTED DIAGNOSTIC only; departures informative, recorded, never automatic failure.

## 7. Operational outcome rules (axis-specific; D3 operative per Mike's A5)

For each axis separately, outcome is evaluated only inside bins where G1–G4 pass and G3 eligibility holds. For each eligible comparison bin, compute per side: window_exceed_count (in-bin), row_onset_count, setting_onset_flag, mean raw magnitude, mean residue and excess above operative floors, median and lower-support prop_I.

**κ≈0 common-mode-alone risky event:** any sentinel exceedance at c = 0 under verified G1 (at the row's tier), G3, and G4 is recorded as a SENTINEL RISKY EVENT and surfaced (D5). A setting-level risky-form failure under path (a) requires the Section 3.2 setting-level onset flag at c = 0 on EITHER co-equal axis (axis-conjunctive requirement prohibited), under verified common-mode lift: G1 passed for the tier's c=0 rows, lifted ρ, prop_I recorded zero-variance/non-identifiable.

**Differential tracking (A5, operative):** for a sign/tier/bin family with G2 passed and G3 eligible, the axis TRACKS the differential channel only if: at least one responsive side at |c| ≥ 0.20 carries the setting-level onset flag while the matched c = 0 side carries none, AND in the eligible matched-ρ bin the responsive side is not worse on in-bin window-exceed count AND strictly better on at least one of (in-bin window-exceed count, mean residue excess).

**PRODUCES the predicted structure (per axis):** differential tracking holds in at least one eligible path (b) family, AND path (a) shows no setting-level onset at c = 0 on that axis under verified common-mode lift.

**FAILS TO PRODUCE (risky form, per axis):** (a) the setting-level onset flag fires at c = 0 on that axis under verified lift (sentinel events alone are recorded and surfaced but do not constitute the setting-level failure); OR (b) G2 passes, G3 holds, G4 holds, and no eligible responsive comparison shows differential tracking on that axis — recorded as "fails to produce differential tracking." Sub-reading under (b): if differential prop_I rises but realized organization does not, the welding claim weakens; recorded as bearing on Reading B's realized-level content, distinct from the ordering claim.

**Under-determined / gate-failed:** every G1–G4 failure region and every ineligible bin — apparatus limits, never evidence for or against. No-result and under-determined outcomes are recorded SEPARATELY from candidate failure.

Three reading categories with qualified wording carried: zero-mode driver imprint (primary label; apparatus-level only — not coherence, not synchrony in the theoretical sense, not Regime II); spatial organization (meanI axis); persistence organization (persistence axis). Every claim carries its gate provenance (gates passed, bins, flags).

## 8. Recorded-vs-reconstructed consistency audit

Before gate evaluation, the read EXHAUSTIVELY verifies all gate-bearing CSV quantities against NPZ reconstruction where applicable: all primary-block block_rho; all primary-window window_mean_rho; all primary flags and exclusion reasons; all schedule values u_t and schedule_phase; all identifiers; and all G2/G4 diagnostic summaries used for cross-checking. Raw observables used as gates are NPZ-recomputed for ALL primary windows (they are anyway, as the sole gate source). If any raw CSV column is sample-checked rather than exhaustively checked, the JSON labels that column diagnostic-only and NPZ reconstruction is the sole gate source for it. Any mismatch beyond fixed tolerance (recorded in-script) FAILS CLOSED and routes to Mike as a possible recording defect — never patched in-read, never absorbed by tolerance widening, never substituted.

## 9. Output

One machine-readable results file: `cycle3/data_out/tcop_read_results.json`, keyed by section: input manifest (all digests, counts, decomposition verification); read constants; the frozen CM-0 comparator sets with intermediate-emission digest; per-row G1/G1b/G4 records with near-threshold margins; per-sign-per-tier G2 records including the zero-variance c=0 records; ALL attempted G3 pairs × bins with eligibility outcomes; per-row and per-setting onset records with window counts and phase distributions per axis; the dedicated SENTINEL section; signed-effect records; decomposition and zero-mode diagnostics; the exhaustive consistency-audit record; an INVALID/HALT record section (empty on clean execution; populated with the halt reason and state if any fail-closed condition fires); and an **outcome-classification evidence table**: for every produces / fails-to-produce / under-determined label, the complete numeric evidence chain (bins, counts, flags, excesses, gate provenance) sufficient to audit the label from the JSON alone, without a prose findings step. Console echo for the transit record. A separate L1-authored findings document grounds from this JSON afterward; it is a subsequent artifact, not part of execution.

## 10. Discipline fences

Pessimistic-on-passing applies to this read's own emissions first: every PASS reports what alternative could have produced the observation and which recorded diagnostic discriminates against it. No threshold tuned on probe output; no rerun; no CM-0 statistic selected, trimmed, or reweighted after CM-1 output is seen; no post-hoc comparison-family selection (the Section 4.3 universe is closed at ratification); no relaxation of any count rule after output; failed rows/bins reported as apparatus limits, never dropped; sign-separated reporting before any sign-symmetry summary; full-surface prop_I is the gate quantity; raw travels with z, z never sufficient; recorded diagnostics never silently substitute for reconstruction; APPARATUS_ONLY columns never appear in findings; block 15 and non-primary windows never enter primary calculations; u=0 tier excluded from G1; no density-stability claim; Comparator 0, L4, CM-2, Rule E B/C untouched regardless of outcome.

## 11. Sequence

Spec CANONICAL (this placement) → L1 drafts `tcop_read.py` (pure read; L1-drafted; no L3 unless a substrate fact requires it) → Mike executes → results JSON → L1 authors the findings document from the JSON → deferred-commit cluster with ops log (spec + script + results JSON + findings + ops log). Nothing here executes; nothing licenses outcome language before the read runs.
