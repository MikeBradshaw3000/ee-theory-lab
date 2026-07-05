# Two-channel ordering probe — thresholding addendum (CANONICAL)

**Status: CANONICAL ADDENDUM to TWO_CHANNEL_ORDERING_PROBE_CONTRACT.md. Freezes the numeric thresholds the contract's Section 6 predeclared "from committed data only, before any run." Authored by Layer 1 from the machine-readable results file `cycle3/data_out/threshold_fixing_read_results.json` (the valid v3 read output); no number in this addendum originates anywhere but that committed computed source. NON-SEEDING: the probe remains UNSEEDED; seeding opens only on Mike's separate explicit call. This addendum completes the contract for seeding readiness.**

## 1. Provenance and lineage

Read spec: THRESHOLD_FIXING_READ_SPEC v2.1 (v2 L2-fidelity-passed; v2.1 folded the L2-concurred axis-specific onset-control clarification). Read script: `threshold_fixing_read.py` (v3). Inputs: F3-validated null-extension floor family (Family F, 400-tick, Λ=0.40, κ=0, 5 seeds) and committed Rule C M2 responsive NPZs (Family M, 200-tick, Λ=0.40, c∈{0,±0.05,±0.10,±0.20,±0.35}, 5 seeds); SHA-256 manifest recorded in the JSON; fail-closed on any missing/mis-shaped input. Read-control RNG seed 20260704, frozen; PERMUTATIONS=199; all quantiles non-interpolating method="lower". Byte-for-byte apparatus reuse from committed `c3_w2_rule_c_m2.py`.

**Two implementation defects were found and repaired during execution, each caught by a discipline artifact, each proven isolated by a built-in audit against the preserved prior JSON:**
- **Repair 1 (v1→v2, L2-arbitrated):** the G3 Δρ_match cap min-ed over ALL construction-predicted band separations, including same-tier cross-c near-degenerate pairs that are matched-rho TARGETS, collapsing Δρ_match to 4e-5 and contradicting the feasibility audit. Corrected to the discriminating-set rule (adjacent tier/schedule-level ρ strata at the same c and sign; cross-c/cross-sign matching pairs excluded). Repair-isolation audit PASS: all non-3.4 emissions bit-identical.
- **Repair 2 (v2→v3):** the onset meanI control used argsort(axis=1) — cells-within-ticks (the committed z-score convention, a per-tick spatial shuffle) — not the spec's per-cell independent time shuffle (axis=0). Caught by L2's invariance hardening clause: the time-shuffle persistence-invariance demonstration returned False, impossible under the labeled control. Corrected to axis=0; the fix consumes no RNG, so all other emissions reproduced bit-identically. Repair-isolation audit v3 PASS; invariance demonstration True.

The two preserved invalid JSONs (`..._INVALID_v1.json`, `..._INVALID_v2.json`) are retained as the audit-lineage record. The operative results file is `threshold_fixing_read_results.json` (v3).

## 2. Frozen thresholds (the addendum proper)

### G1 — schedule imprint (hard gate, nonzero CM-1 tiers)
- **Correlation threshold:** 0.7840 (coarse 15-point max-null; conservative maximum, not a percentile)
- **Slope/amplitude threshold:** 0.002628 (block-ρ units per unit template)
- A nonzero CM-1 row passes only if, at the construction phase: correlation > 0.7840 AND slope > 0 AND slope > 0.002628. Correlation without amplitude is no driver imprint.
- **Apparatus limit (recorded, binding):** the 3-block schedule period over the 12-block primary set admits exactly 3 integer phase alignments, giving 15 pooled seed-phase null values. The thresholds are the conservative maxima of a deliberately coarse null (Fork A option iii, Mike-arbitrated). This is a hard-to-pass gate by design; the coarseness is a known apparatus limit, not a precision claim.

### G1b — floor overdispersion
- **Threshold:** block-ρ variance > 4.47e-6 (max of 5 seed-level variances, ddof=0)
- Necessary but NOT sufficient for G1b; does NOT substitute for the full 135-row CM-0 comparator dominance rule (a separate predeclared relation evaluated after CM-0 exists). No result may say "above CM-0" from this floor threshold alone.

### G2 — differential-channel activation anchor (sign-separated)
- **Positive activation floor (|c|=0.35, c>0):** prop_I ≥ 0.3832
- **Negative activation floor (|c|=0.35, c<0):** prop_I ≥ 0.3814
- Lower empirical 10% (method="lower") of the per-seed full-surface prop_I. Gate anchor is full-surface prop_I; the inactive-cell-masked value is diagnostic only and never replaces the gate. Trend rule per tier / per sign / across the seed set; signs never pooled to manufacture monotonicity. (These reconstructed floors independently reproduce the committed ~+0.38 anchor, both signs — a validation of the reconstruction pipeline.)

### G3 — matched-rho / common-support
- **Δρ_match = 0.00283** (window-mean-ρ unit). Provisional 2×σ_ρ_match = 0.002990 (σ_window_F=0.000675, σ_window_M=0.001495, σ_ρ_match=max=0.001495); cap bound at 0.5·sep_discrim_min = 0.5·0.005655 = 0.002827; Δρ_match = min(provisional, cap) = 0.00283. Cap-bound = True.
- **N_bin_min = 9** primary windows per side per bin; **S_bin_min = 3** seeds per side; no single seed > half the qualifying windows on either side; schedule-phase composition match within one window per phase, else the bin is common-support-present-but-phase-confounded and excluded from ordering claims.

### G4 — compression / slope audit
- **mean_slope_floor:** mean_i[p_i(1−p_i)] ≥ 0.2256 (lower 10%, method="lower")
- **q05_slope_floor:** 5th-percentile cell slope ≥ 0.19884 (lower 10%)
- **tail_mass_ceiling:** fraction of cells with p_i outside [0.05,0.95] ≤ 0.0000 (max observed committed responsive tail mass — maximally strict; no committed responsive cell ever compressed)
- **Hard interval:** [0.05, 0.95]
- A CM-1 row passes only on all three criteria; mean slope alone never sufficient. Planned-drive envelope over all CM-1 schedule levels × c-labels: **no pre-seed compression risk** (no planned cell violates the hard interval or the tail ceiling).

### Onset criteria (axis-specific controls; operative floor = max-observed)
Per contract Section 7 and the operative-floor conditional: the setting-level earned-window rule is NOT yet verified for the 9-window primary family, so **max-observed is the operative per-window onset floor**; the 97.5th-percentile values travel alongside for when that verification lands.

- **Psi_meanI_state** (control: per-cell independent time shuffle):
  - raw floor (operative, max-observed): 0.00199 — 97.5th-pct alongside: 0.001526
  - residue floor (operative, max-observed): 0.002113 — 97.5th-pct alongside: 0.001744
- **Psi_persistence_I** (control: spatial permutation of the persistence grid, committed convention):
  - raw floor (operative, max-observed): 0.02284 — 97.5th-pct alongside: 0.017538
  - residue floor (operative, max-observed): 0.02311 — 97.5th-pct alongside: 0.017522
- Onset on an axis requires exceeding BOTH the raw and axis-appropriate residue floors on that axis. Z reported alongside, never sufficient. Axis-specific; conjunctive-across-axes onset prohibited.
- **Recorded invariant (binding):** the per-cell time-shuffle persistence residue is algebraically zero (a permutation cannot change a time-mean); it is diagnostic-only and is NEVER the operative persistence residue gate. Persistence uses the spatial-permutation control. (Numerically demonstrated True in the v3 read.)

### Feasibility (pre-seed common-support audit)
- **OVERALL: feasible.** Path (a) (common-mode-alone at κ≈0 across tiers): feasible. Path (b) (differential channel at matched ρ across κ): feasible. Buffer = Δρ_match + σ_ρ_match = 0.00432. Self-consistent mean-field fixed points ρ* = p_eff(ρ*)/(1−s+p_eff(ρ*)), s=0.40.
- The design is seedable as an ordering probe. Feasible is necessary, not sufficient — realized G3 can still fail per-comparison and be recorded as an apparatus limit.

## 3. What this addendum does not do

Does not seed CM-1 or CM-0; does not authorize seeding; does not engage Layer 3; does not reclassify Comparator 0; does not move L4; does not open CM-2 or Rule E B/C; does not verify the 9-window earned-window rule (a named open item — the operative onset floor is max-observed until it is verified); does not claim density-stability. The probe remains NAMED-and-CONTRACTED but UNSEEDED. Seeding opens only on Mike's separate, explicit call.

## 4. Attribution

Layer 1 authored from the committed v3 results JSON. Thresholds L2-attacked (read spec: reject-as-execution-ready, 8 emission verdicts + 13 items, all folded; fidelity pass clean), axis-specific control clarification L1-discovered / L2-concurred, both implementation defects L1-discovered (one L2-arbitrated, one caught by L2's own hardening clause) and audit-proven isolated. Mike arbitrated: Fork A (coarse null option iii), the defect-repair-not-tuning dispositions, and all execution approvals. Committed together with the read spec v2.1, the read script v3, both preserved invalid JSONs, the valid results JSON, and the consolidated ops log (deferred-commit cluster).
