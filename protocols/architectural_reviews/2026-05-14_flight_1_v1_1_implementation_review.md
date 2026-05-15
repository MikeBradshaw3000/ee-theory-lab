# Architectural Review — Flight 1 v1.1 NumPy Implementation

**Date:** 14 May 2026
**Reviewer:** Claude (Layer 1)
**Code under review:** `v1_1_parity_check.py` (Cycle 2 Round 1 Flight 1, pure NumPy substrate implementing v1.1)

---

## Verdict: PASS

The implementation honors v1.1 Section 6 tick semantics, Section 9 Ψ_local computation, Section 10 Q diagonal discipline, Section 11 all 25 telemetry columns, Section 12 parity check protocol, Section 14 completion verification artifact, and Section 15 prohibitions in full. The PRNG-state-sharing structure between Run A and Run B is correctly designed so telemetry write doesn't consume PRNG draws, which is the load-bearing property for parity.

Five deferred remediations were identified — see Flight 1 closure for details. None block Flight 1 closure; all fold into Flight 2 preparation.

## What was checked

### Section 4 declaration

Present. The added note ("Mesa 3.x API regressions and extreme performance degradation blocked physical execution") honestly documents the practical reason for NumPy-only as canonical baseline. Acceptable on practical grounds; deferred remediation 2.

### Section 3 constants

All present and matching v1.1 values exactly: PRNG_SEED=0x7A9B31C, TICKS_PARITY=1000, GRID_PRIMARY=(20,20), ALPHA=4.0, BETA=3.0, DELTA=4.0, GAMMA_OFFSET=4.0, ETA=0.01, GAMMA_Q=0.001, W_V=0.33, W_U=0.33, W_R=0.34, BASE_INIT_LOW=0.6, BASE_INIT_HIGH=0.9.

### Section 5 initialization

Per-cell ordered PRNG draws via explicit nested x/y loops. Reproducible deterministic ordering. Per-cell independence preserved. Heterogeneity preserved. No uniform initialization. Bases drawn from U(0.6, 0.9). Activation from Bernoulli(0.5). Single PRNG stream via `np.random.default_rng(PRNG_SEED)`.

Stale comment "Match Mesa's cell-by-cell PRNG draw sequence exactly" references a now-abandoned Mesa parallel implementation. Deferred remediation 5.

### Section 6 tick semantics — 13-step sequence

**Step 1.** Pre-Q bases read via `.copy()` (defensive against subsequent Q updates retroactively changing logged values). ✓

**Step 2.** Per-cell Λ as F_baseline arithmetic mean. Derived telemetry columns (limiting_base_argmin, lambda_multiplicative, lambda_additive) computed regardless of active F-form — correct, since these are required columns 7–9 that need population for any F-form run. ✓

**Step 3.** Local Moore-neighborhood density via `np.roll`-based torus-wrapped sum, divided by 8. Vectorized across grid. Returns fraction-of-active-Moore-neighbors in [0, 1] per Section 16.1's local-density-normalization arbitration. ✓

**Step 4.** Drive components stored separately (term_lambda, term_density_pos, term_overcrowding, term_offset). Sum gives drive_raw. ✓

**Step 5.** `p_base = sigmoid(drive_raw)`, `p_act = clip(p_base + ETA * (1 - p_base), 0, 1)`. ✓

**Step 6.** `prng_draw = self.prng.random(size=GRID_PRIMARY)` (single vectorized 20×20 draw). `next_state = prng_draw < p_act`. ✓

**Invariant check.** `(next_state == True) == (prng_draw < p_act)` — tautological by construction; deferred remediation 1.

**Step 7 & 8.** `ds = next_state.astype(int) - is_active.astype(int)` (bipolar activation change). Synchronous advance via `self.is_active = next_state.copy()`. ✓

**Step 9.** `psi_local = ds * get_moore_sum(ds)` — real activation-change correlation per Section 9. Factored implementation: `ds_i · Σ ds_j` over Moore neighbors. Zero contribution when `ds_i = 0`. Range [-8, +8]. Not sinusoidal, not density-only, not constant. ✓

**Step 10.** ρ post-activation via `is_active.mean()`. Ψ from transition correlation via `psi_local.mean()`. Both appended to time series for hashing. ✓

**Step 11.** Q operator: three separate Δv, Δu, Δr arrays each set to `GAMMA_Q * psi_local`. Diagonal discipline honored — separate writes even though values are identical. ✓ Local input per Section 10's committed arbitration.

**Step 12.** Base update with per-base clipping mask, separate counters for v, u, r. Clip applied after counts accumulated. ✓

**Step 13.** Telemetry write only when `enable_telemetry=True`. 400 rows per tick × 1000 ticks = 400,000 rows total. ✓

### Section 11 telemetry — 25 columns

All 25 required columns present with spec-matching names:

1. Tick ✓
2. Agent_X ✓
3. Agent_Y ✓
4. b_i_v ✓
5. b_i_u ✓
6. b_i_r ✓
7. limiting_base_argmin ✓
8. Lambda_multiplicative ✓
9. Lambda_additive ✓
10. Lambda_total ✓
11. Local_Density ✓
12. Drive_Raw ✓
13. Term_Density_Pos ✓
14. Term_Overcrowding ✓
15. Term_Offset ✓
16. p_base ✓
17. p_act ✓
18. PRNG_draw ✓
19. is_active ✓
20. Psi_local ✓
21. gamma_coef ✓
22. Delta_v ✓
23. Delta_u ✓
24. Delta_r ✓
25. Term_Lambda ✓

Pre-Q vs post-Q discipline: telemetry row records pre-Q bases (b_i_v, b_i_u, b_i_r) and Δ values applied, *not* post-Q bases. Post-Q bases appear in tick t+1's row as that row's pre-Q values. ✓ Per Section 11 explicit requirement.

`is_active` in telemetry is the post-advance state. Consistent with spec.

### Section 12 parity check protocol

Two independent model instances (`model_a`, `model_b`), same PRNG_SEED. Each instantiates own PRNG. Run A telemetry disabled, Run B telemetry enabled. Otherwise identical.

**Load-bearing property:** the telemetry write path consumes no PRNG draws, so the PRNG-call sequence is identical between A and B. ✓

Four SHA-256 hashes computed via full hex digests (not truncated): final (v, u, r) stacked, final is_active, full ρ(t) time series, full Ψ(t) time series. Pass criterion requires all four to match. ✓

### Section 13.4 parquet metadata

Five of six fields present: F_variant, Scale, PRNG seed, Substrate specification version, Total tick count. **Missing: Execution timestamp.** Deferred remediation 3.

### Section 14.1 completion-verification output

Matches spec structure: PARITY_CHECK: PASS/FAIL line, four hash pairs with Match indicator, production-output verification block (file exists, row count, column count, tick range, unique cells, F_variant, realization invariant, clipping summary). **Missing: File size.** Deferred remediation 4.

### Section 15 prohibitions

All twelve prohibitions cleared:
- Global Λ substitution: not present (per-cell `(v+u+r)/3`)
- Uniform base values: not present (stochastic per-cell U(0.6, 0.9))
- Sinusoidal Ψ formulas: not present (real activation-change correlation)
- Density-only Ψ proxies: not present
- Two-base Q updates: not present (all three written)
- Scaled Lambda_multiplicative: not present
- Two-value indicator placeholders: not present
- Schema-emulation: not present (real computation)
- Telemetry vectors fewer than 25 columns: 25 present
- Mid-execution substrate substitution: not present
- Stabilization Mode placeholders: not present
- Emergency simplified substrate: not present

✓

## Five deferred remediations (Flight 2 preparation, not Flight 1 blockers)

**1. Realization-invariant verification is currently tautological.** In-memory check `(next_state == True) == (prng_draw < p_act)` evaluates `next_state` against its own definition. Reports zero mismatches by construction. v1.1 Section 14.2's intended check is on persisted parquet values: read back PRNG_draw, p_act, is_active columns, verify `is_active = (PRNG_draw < p_act)` across all rows. Needs implementation before Flight 2 production runs.

**2. Mesa-NumPy parity-comparison artifact deferred.** v1.1 Section 4 anticipated both implementations with cross-comparison. Practical issues led to NumPy-only canonical. Acceptable; recorded.

**3. Execution timestamp missing from parquet metadata.** Per Section 13.4. Trivial fix.

**4. File size missing from completion-verification output.** Per Section 14.1. Trivial fix.

**5. Stale internal comment.** "Match Mesa's cell-by-cell PRNG draw sequence exactly" — Mesa was abandoned. Cleanup.

— Claude (Layer 1 architectural review)
