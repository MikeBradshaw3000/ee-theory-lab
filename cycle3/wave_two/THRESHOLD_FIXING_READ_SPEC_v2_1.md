# Threshold-fixing pure read — spec v2.1 (merged; L2 fidelity-passed; axis-specific onset controls folded)

**Status: SPEC v2.1. v2 received a CLEAN L2 fidelity pass. v2.1 folds one post-fidelity clarification, L1-discovered and L2-concurred with replacement text (2026-07-04): the per-cell time-shuffle control is ALGEBRAICALLY INVARIANT for Psi_persistence_I (a permutation cannot change a time-mean, so the persistence grid is preserved cell-by-cell and the residue is identically zero), making the literal v2 persistence residue gate unsatisfiable or vacuous. Section 3.7 now uses AXIS-SPECIFIC residue controls: per-cell time-shuffle for Psi_meanI_state; spatial-permutation of the persistence grid (committed compute_persistence_null convention) for Psi_persistence_I. Recorded as a contract/spec clarification forced by an algebraic invariant, not a threshold choice; carried into the contract addendum with this lineage. All other v2 content unchanged.**

## 0. What this read is and is not

Emits the numeric thresholds the contract fixes from committed data before any run. Runs AFTER contract placement (8c94d8c) and AFTER the F3-validated null-extension run (F3 bit-exact 5/5). Output: one machine-readable results file (`threshold_fixing_read_results.json`); the contract addendum is a SEPARATE authored artifact grounding from that file. The read touches NO probe output (none exists); nothing is tuned on CM-1/CM-0 output; the read may not be rerun with different control RNG to move any threshold (no-rerun discipline, binding).

## 1. Input families (verified present)

**Family F — null-extension floor:** `c3_w2_null_extension_states_L0.4_kp0_0000_s{seed}.npz`, 5 seeds, (400,50,50), F3-validated. Supplies G1 nulls, overdispersion null, onset nulls, and sigma_window_F.

**Family M — committed Rule C M2 (200-tick, Lambda=0.40):** cells c=0, |c|=0.05, 0.10, 0.20, 0.35 both signs (kp/km 0_1042, 0_2090, 0_4221, 0_7599, plus kp0_0000), 5 seeds each, all verified on disk this session. Supplies G2 anchor, G4 constants, sigma_window_M.

**Rule constants:** Lambda=0.40; committed c->kappa map at Lambda=0.40. Propensity reconstruction: p_become(t) is reconstructed from states[t] as the field that would be used to update from state t to t+1; NO random draw is made and NO state is advanced. The read must either import the committed helper functions (neighbor count, logistic form) or reproduce them byte-for-byte, with the copied source recorded in the read script. Approximate re-vectorization is a reconstruction gap and is prohibited.

**Input manifest and fail-closed (L2 item 12):** the results JSON records input file names, array shapes, seed list, file digests (SHA-256) for every NPZ consumed, the read script's own digest, and the F3 validation status of Family F. Any missing or shape-mismatched input FAILS CLOSED: the read halts, emits nothing.

## 2. Primary analysis family

Family F: primary block set = blocks 3-14 inclusive (12 blocks; four complete 3-block cycles); primary window set = window starts at blocks 3-11 (ticks 75..275, 9 windows/seed, phase-balanced 3/3/3). Blocks 0-2, 15 and non-primary windows: diagnostics only. Family M: committed M2 window structure (starts 0,25,50,75,100). Family-split status (L2-corrected): clean for G2, clean for G4 given the planned-drive envelope (3.6), NOT clean for G3 — the G3 rho scale is bridged across families via max(sigma_window_F, sigma_window_M) (3.4).

## 3. The eight emissions (L2 replacement texts, verbatim where given)

### 3.1 G1 floor imprint null

Purpose: the false-alignment guard for G1's schedule-imprint component. The floor has no schedule; the null is the distribution of apparent alignment between floor block-mean rho and an arbitrary 3-block-periodic template across all admissible integer block phases.

For each floor seed, compute block-mean rho over the primary block set, blocks 3-14 inclusive, giving 12 block values. For each phase phi in {0,1,2}, construct the centered 3-block template [0, 0.5, 1] repeating over the 12 blocks at that phase. For each seed-phase pair, compute: (1) Pearson correlation r(seed, phi); (2) OLS schedule slope beta(seed, phi) = cov(rho_block, template) / var(template), in block-rho units per unit template; (3) covariance amplitude cov(seed, phi) as a diagnostic.

This yields 15 seed-phase values for each statistic. The G1 correlation threshold is max(0, max r(seed, phi)). The G1 slope/amplitude threshold is max(0, max beta(seed, phi)). Mean and SD are descriptive only.

A nonzero CM-1 row passes the G1 imprint component only if, at the construction phase, its correlation exceeds the correlation threshold, its slope is positive, and its slope exceeds the slope/amplitude threshold. Correlation without amplitude is no driver imprint. Overdispersion without phase-locked slope is no driver imprint. The 15-point coarse-null limitation is recorded as an apparatus-limit note in the results JSON and contract addendum.

### 3.2 G1 floor overdispersion null

For each Family F seed, compute block-mean rho over primary blocks 3-14 and compute the block-rho variance with fixed ddof = 0. Emit the five seed-level variances, their max, mean, and SD. The G1 floor-overdispersion threshold is the maximum of the five seed-level variances.

This threshold is necessary but not sufficient for G1b. It establishes that a CM-1 row has more block-rho variance than the 400-tick lambda-only floor. It does not substitute for the full 135-row CM-0 comparator dominance rule, which remains a separate predeclared comparator relation evaluated after CM-0 exists. No result may say "above CM-0" from this floor threshold alone.

### 3.3 G2 activation anchor

For each required Family M cell, reconstruct p_become from the committed state grid at tick t using the exact committed Rule C neighbor-count and logistic formula. The reconstructed field is the propensity field that would be used to update from state t to t+1; no random draw is made and no state is advanced. The read must either import the committed helper functions or reproduce them byte-for-byte in the read script, with the copied source recorded in the script.

The primary G2 statistic is Moran's I of the full becoming-active propensity surface, averaged over the fixed committed M2 tick family. The read also emits an inactive-cell-masked diagnostic, but the gate anchor remains the full-surface statistic unless Mike explicitly changes the contract.

For each sign separately at |c| = 0.35, emit all five per-seed prop_I values, the mean, median, minimum, and the lower empirical 10% value using a fixed non-interpolating method: method = "lower" / empirical order statistic. With five seeds, no interpolated percentile may define the threshold. The G2 activation floor is the sign-specific lower empirical support value emitted by this rule.

The c = 0, |c| = 0.05, |c| = 0.10, and |c| = 0.20 values are emitted for trend reference. Signs are reported separately before any sign-symmetry summary. The trend rule is per tier, per sign, across the seed set; positive and negative signs are never pooled to manufacture monotonicity.

### 3.4 G3 rho-match scale (Delta_rho_match)

Purpose: fix the absolute rho-bin width for matched-rho comparisons on the same unit used by the G3 pairwise read.

The primary unit for G3 matching is the window-mean rho of eligible primary windows, not an unspecified block-rho mean. The pure read emits: (1) sigma_window_F: within-setting SD of primary-window mean rho from Family F, using the 400-tick primary window family; (2) sigma_window_M: pooled within-setting SD of committed M2 window-mean rho from Family M over the required Lambda = 0.40 cells; (3) sigma_rho_match = max(sigma_window_F, sigma_window_M).

The provisional bin half-width is 2 * sigma_rho_match. The read also computes the smallest construction-predicted nonzero tier/rho separation relevant to the planned comparisons. If 2 * sigma_rho_match is larger than half that smallest predicted separation, the cap binds and Delta_rho_match is set to the capped value. The results JSON reports whether the cap bound.

A matched-rho comparison may only use bins of width Delta_rho_match on the same rho unit used in the comparison. A setting-level mean difference below Delta_rho_match is descriptive only; it does not replace bin-level common support.

### 3.5 G3 bin-eligibility constants (N_bin_min, S_bin_min)

Purpose: fix minimum support per side per rho bin for pairwise matched-rho comparisons. This is not SS-001 and is not a setting-level earned-window rule.

With 9 primary windows per seed and 5 seeds, each setting has 45 primary window-instances. Set N_bin_min = 9 per side per bin: one complete primary-window-family equivalent. Set S_bin_min = 3 per side per bin: at least three of the five canonical seeds represented. No single seed may contribute more than half of the qualifying windows on either side.

Each eligible bin must also pass a schedule-phase composition check. Either the comparison is explicitly phase-stratified, or the two sides' window-start phase histograms over the three schedule phases must match within a predeclared tolerance of one window per phase. A rho bin that has enough windows but fails the phase-composition rule is reported as common-support present but phase-confounded; it is not used for an ordering claim.

### 3.6 G4 compression constants

Purpose: prevent a mean-slope proxy from hiding compressed-tail read-through.

For every required Family M cell and sign, reconstruct the full p_become field and compute, per tick: (1) mean_slope = mean_i[p_i(1-p_i)]; (2) q05_slope = 5th percentile_i[p_i(1-p_i)]; (3) tail_mass = fraction_i[p_i < 0.05 or p_i > 0.95]; (4) p_min, p_max, and mean_p.

Emit all distributions sign-separated. The G4 constants are: mean_slope_floor = lower empirical 10% value of the per-tick mean_slope distribution, fixed non-interpolating method = "lower"; q05_slope_floor = lower empirical 10% value of the per-tick q05_slope distribution, same method; tail_mass_ceiling = the maximum observed committed responsive tail_mass; absolute hard interval [p_low, p_high] = [0.05, 0.95].

The read also computes a construction-only planned-drive envelope over every CM-1 schedule level and every planned c label. If any planned envelope violates [0.05, 0.95] or implies tail mass above the emitted committed ceiling before any seed, the read reports a pre-seed compression risk and marks the affected planned cell as not seedable without Mike narrowing the design or explicitly accepting the apparatus limit.

A future CM-1 row passes G4 only if its actual driven propensity fields pass all three emitted criteria: mean-slope floor, lower-tail slope floor, and tail-mass ceiling. Passing mean slope alone is never sufficient.

### 3.7 Onset null

Purpose: emit raw-effect and control-residue floor thresholds per co-equal observable on the 400-tick primary window family.

For Family F, compute raw per-window Psi_meanI_state and Psi_persistence_I magnitudes on the nine primary windows per seed. Residue controls are AXIS-SPECIFIC.

For Psi_meanI_state, compute the per-cell independent time-shuffle null with fixed PERMUTATIONS = 199, fixed read-control RNG seed recorded in the JSON, fixed permutation construction, and fixed statistic definition.

For Psi_persistence_I, do NOT use per-cell time shuffles as the operative residue control, because they preserve each cell's within-window time mean and therefore preserve the persistence grid exactly. Instead compute the spatial-permutation null on the persistence grid, using the committed persistence-null machinery / compute_persistence_null convention, with the same fixed PERMUTATIONS = 199, fixed read-control RNG seed, fixed permutation construction, and no-rerun discipline. The spatial permutation preserves the marginal distribution of cell persistence values while destroying adjacency structure.

Residue is defined axis-specifically as abs(raw_stat - mean_control_stat), where mean_control_stat is the mean of the appropriate axis-specific control null. The JSON records the control type, RNG seed, permutation count, residue definition, and quantile method for each axis.

The read must explicitly report that the per-cell time-shuffle persistence residue is algebraically zero / invariant and is diagnostic-only if computed. It is never used as the operative persistence residue gate.

Emit, per axis: all 45 raw magnitudes, all 45 residue magnitudes, the 97.5th-percentile threshold with the exact quantile method recorded, and the maximum observed floor value. If the 97.5th percentile is lower than the maximum observed floor value, the addendum must state whether the later setting-level earned-window rule is carrying that false-window allowance. Without that setting-level rule explicitly attached, the operative onset floor is the maximum observed floor value.

**Operative-floor conditional (convergence record):** the contract's Section 7 onset clause conditions the setting-level earned-window flag on verification for the primary window count; that verification has NOT been performed for the 9-window family. Therefore the MAX-OBSERVED value is the operative per-window onset floor until the earned-window rule is verified for the 9-window primary family; the 97.5th-percentile value travels alongside for when that verification lands. The addendum records this conditional explicitly. (L1 contest withdrawn on this ground.)

A CM-1 onset on an axis requires exceeding both the raw floor and the AXIS-APPROPRIATE control-residue floor on that axis. For Psi_meanI_state, the residue floor is time-shuffle residue. For Psi_persistence_I, the residue floor is spatial-permutation residue. Z-scores travel with the read but never suffice. Axis-specific; conjunctive-across-axes onset prohibited.

### 3.8 Pre-seed common-support feasibility audit

Purpose: identify whether the planned ordering read has predeclared matched-rho comparison families before any CM-1 or CM-0 seed.

The audit is construction-only and reads no probe output. For each planned (tier, c-label, sign) cell and schedule level, solve the mean-field fixed point self-consistently: rho* = p_eff(rho*) / (1 - s + p_eff(rho*)), where p_eff uses the planned common-mode level, the committed c->kappa constant, and mean-neighbor occupancy q = rho*. Do not treat p_eff as independent of rho.

Emit point predictions and buffered rho bands. The buffer must include Delta_rho_match and the larger of the Family F and Family M rho-variability scales emitted in 3.4.

Classification has three values: feasible, not_feasible, indeterminate. Feasible: at least one predeclared comparison family for falsification path (a) and at least one for path (b) has predicted common support after buffering. Not_feasible: no such common support even after conservative buffering. Indeterminate: the mean-field approximation is not decisive enough to certify or rule out common support.

A not_feasible or indeterminate result halts automatic seedability and routes to Mike. It is not worked around by relaxing G3 after output. A feasible result is necessary but not sufficient; realized G3 can still fail and be recorded as an apparatus limit.

## 4. Output

One file: `cycle3/data_out/threshold_fixing_read_results.json`, keyed by emission, each carrying computed values, method-derived thresholds, apparatus-limit notes, plus: the input manifest (filenames, shapes, SHA-256 digests, seed list, F3 status), the read-control RNG seed, the residue definition, every quantile method string, and the read script's own digest. Console echo for the transit record. Missing input fails closed. No probe seed; no state written.

## 5. Discipline fences (carried, hardened per the verdict)

- Pessimistic-on-passing applies to the read's own emissions.
- Every quantile/percentile carries an explicit method (non-interpolating "lower" for 5-seed statistics; recorded method for 45-window statistics).
- Shuffle-control RNG frozen and recorded; no rerun-to-move-threshold, ever.
- Byte-for-byte apparatus reuse for reconstruction; copied source recorded in-script.
- Sign-separated reporting before any sign-symmetry summary (G2, G4).
- Full-surface prop_I is the gate; the inactive-masked value is a diagnostic and never silently replaces it.
- CM-0 dominance is NOT emitted by this read (CM-0 rows are not committed data); the full 135-row comparator rule remains a separate predeclared relation evaluated after CM-0 exists.
- Family M's inherited candidate columns are not read; all statistics from states, never the M2 results CSV.
- The feasibility audit's not_feasible/indeterminate halts route to Mike; never worked around.

## 6. Sequence

Spec v2 (this) -> L2 fidelity check -> Mike execution approval -> L1 drafts the read script (pure read, L1-drafted per contract Section 6 sequencing — no Layer 3) -> Mike executes -> results JSON -> L1 authors the contract addendum from the JSON -> addendum + read script + results held for the deferred ops-log commit -> THEN, separately and only on Mike's explicit call, seeding. Nothing here opens seeding.
