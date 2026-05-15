# Architectural Review — Flight 2 Analysis Script

**Date:** 15 May 2026
**Reviewer:** Claude (Layer 1)
**Code under review:** `flight2_analysis.py` (Cycle 2 Round 1 Flight 2 analytical script implementing ChatGPT's seven-section diagnostic specification, with three Layer 1 patches honored)

---

## Verdict: PASS

The script implements all seven sections of ChatGPT's Layer 2 analytical request, with three Layer 1-flagged patches honored exactly as requested. Path discipline, memory-aware loading via batch iteration, reproducibility provenance, and methodological caveats all present. Eight CSVs produced cleanly on first execution.

## What was checked

### Path discipline (v1.1 Section 4 carry-forward)

```python
base_path = Path(__file__).resolve().parent
input_dir = base_path / "flight2_outputs"
output_dir = base_path / "flight2_analysis_outputs"
output_dir.mkdir(exist_ok=True)
```

All file I/O relative to script location. No working-directory dependence. No hardcoded paths. Section 4 honored.

### Memory-aware loading (per Claude addition 1 to ChatGPT's request)

`pq.ParquetFile.iter_batches(columns=available_cols)` reads selected columns only, batch-by-batch. No full-file DataFrame loads. Confirmed empirically: 4.8M-row parquet files processed without memory pressure.

The pattern mirrors Flight 2 substrate's chunked-write architecture: streaming reads with bounded in-memory state. Layer 1 carry-forward discipline.

### Reproducibility provenance (per Claude addition 2)

For each input parquet file, the script reads and prints:
- Substrate_version
- F_variant
- Scale
- PRNG_seed
- Execution_timestamp
- File size
- Row count

Confirms the analysis is reading the Flight 2 production files this run claims to analyze. Confirmed empirically: all four metadata blocks printed cleanly, matching Flight 2 substrate's written metadata.

### Patch 1 — Probe1-first sort (Layer 1 patch request)

```python
files = sorted(input_dir.glob("*.parquet"), key=lambda p: (0 if 'probe1' in p.name else 1, p.name))
```

`probe1` filenames sorted first to ensure they're registered as canonical sources before their shadow copies dedup against them. Verified empirically: four shadow copies (probe2_starvation_F2sym_20x20, probe2_starvation_F2sym_40x40, probe3_fusion_residual_20x20, probe3_fusion_residual_40x40) all correctly identified `flight6_probe1_overcrowding_*` files as their canonical sources.

Without this patch, `Path.glob` would return files in OS-dependent order; if a shadow happened to sort first, the canonical run_id would have been mis-attributed to the shadow's filename. Patch resolves this risk completely.

### Patch 2 — Direct column access with explicit error (Layer 1 patch request)

```python
req_cols = ['b_i_v', 'b_i_u', 'b_i_r', 'Lambda_total', 'Psi_local', 'Local_Density', 'Drive_Raw', 'p_act']
for c in req_cols:
    if c not in group.columns:
        raise KeyError(f"Required column '{c}' missing from parquet batch for Tick {tick}")

tg['psi_s'] += group['Psi_local'].sum()
# ... direct column access throughout
v = group['b_i_v']
u = group['b_i_u']
r = group['b_i_r']
L = group['Lambda_total']
```

Replaces the `group.get(col, 0)` fallback pattern from the fast-mode first draft. Explicit precondition check raises on missing column rather than silently substituting zeros. The defensive-but-fail-loudly variant of the original ask; preserves defensive intent without enabling silent failure.

Verified empirically: no errors raised across all four production runs, confirming all required columns were present in all batches.

### Patch 3 — Methodological caveats in terminal summary (Layer 1 patch request)

```python
print("\n[METHODOLOGICAL CAVEATS]")
print("  Cardinality counted at 1e-6 precision. F_2_symmetric's smoother distribution")
print("    may produce slight undercount vs. F_LR's natural 1e-4 granularity.")
print("  Connected component labeling is non-toroidal (scipy.ndimage.label limitation).")
print("    Moran's I and same-sign share are toroidal and unaffected.")
print("    Components spanning the torus boundary may be split.")
```

Documents two analytical choices that affect downstream interpretation:
1. Cardinality rounding at 1e-6 may undercount F_2_symmetric's smoother distribution vs F_LR's natural 1e-4 granularity
2. scipy.ndimage.label is non-toroidal; components spanning grid boundary may split

Moran's I (computed via `np.roll`) and same-sign share (computed via `np.roll`) are toroidal and explicitly noted as unaffected. Layer 2 reads outputs with caveats present.

### Seven sections implemented

**1. Global time series per independent run** (`global_timeseries.csv`, 3.2 MB). 12,000 rows (3000 ticks × 4 runs). Full 17-column schema: run_id, F_variant, scale, Tick, rho, psi_global, mean_v/u/r, sd_v/u/r, mean_Lambda, sd_Lambda, mean_Drive, mean_p_act, mean_Local_Density.

SDs computed via streaming variance: accumulate sum and sum-of-squares per tick, finalize via `sqrt(max(0, sum_sq/n - (sum/n)²))`. Numerically robust with safety floor.

**2. Epoch summaries** (`epoch_summary.csv`, 18 KB). 28 rows (7 epochs × 4 runs). Built from completed global time series via `pd.cut` epoch binning and groupby. `observed=False` parameter set explicitly for pandas-future safety on categorical groupby.

**3. Selected-tick distributions** (`selected_tick_distributions.csv`, 58 KB). 11 quantiles per metric (mean, sd, min, p01, p05, p25, median, p75, p95, p99, max). 8 metrics × 8 selected ticks × 4 runs = 256 rows.

**3b. Psi sign decomposition** (`psi_sign_decomposition.csv`, 2.8 KB). Negative/zero/positive counts plus conditional means at each selected tick.

**4. Psi structure diagnostics** (`psi_spatial_diagnostics.csv`, 4.7 KB). Moran's I for Psi_local and is_active (toroidal via np.roll). Same-sign share (toroidal). Connected component stats (non-toroidal, caveat documented).

**5. Base boundary** (`base_boundary_summary.csv`, 5.3 KB). Low/high counts at 0.01 and 0.99 thresholds plus min/max bases per selected tick.

**6. F-form distinguishability** (`fform_comparison.csv`, 2.2 KB). F_2_symmetric minus F_LR deltas per scale per epoch.

**7. Compression fingerprint** (`compression_fingerprint.csv`, 1.0 KB). Total file size, per-column compressed bytes (via pq metadata row group iteration), cardinality counts at 1e-6 precision (with caveat documented).

### Process notes

**Initial fast-mode Gemini draft** under-delivered against ChatGPT's seven-section specification:
- Missing `epoch_summary.csv` entirely (accumulator initialized but never populated, never written)
- Missing `fform_comparison.csv` entirely
- `global_timeseries.csv` schema missing 8 of 13 requested columns plus all SDs
- `selected_tick_distributions.csv` missing p01, p25, p75, p99
- `selected_tick_distributions.csv` missing Psi sign decomposition entirely
- `psi_spatial_diagnostics.csv` missing same-sign share and component sizes
- `compression_fingerprint.csv` missing cardinality counts

Layer 1 pre-execution review caught the gaps. Rewrite requested in advanced mode with explicit gap-by-gap specification.

**Advanced-mode rewrite** delivered all seven sections, all required columns, all quantiles, all sign decomposition. Three targeted patches still required: probe1-first sort (real bug), defensive column access (latent bug), methodological caveats (documentation).

**Final patched script** (this review) honored all three patches exactly. Pre-execution review confirmed no carry-forward drift in helper functions (Moran's I, same-sign share, comp_stats), provenance header, or batch-iteration pattern.

The mode-switching pattern is recorded as the second instance during Cycle 2 Round 1 Flight 2 (the first was the all-in-one orchestrator slip in the substrate script). Pattern under monitoring per operations log; not yet a new standing rule.

## Empirical execution results

Eight CSV files produced cleanly on first execution after Layer 1 sign-off. Provenance header printed for four unique files. Four shadow-copy detections correctly identified probe2 and probe3 files as byte-identical to their probe1 sources. Methodological caveats printed before [COMPLETE]. No errors, no warnings.

File sizes match expectations:
- global_timeseries.csv: 3.2 MB (matches 12,000 rows × 17 columns × ~15 char/float)
- All other CSVs in expected ranges (1-58 KB)

Substantive data inspected via Layer 1 spot-check of `epoch_summary.csv`: F_2_symmetric and F_LR epoch-0-99 values match analytical predictions from base distribution within 1%; F-form distinguishability strong and scale-stable. Cleared for Layer 2 routing.

— Claude (Layer 1 architectural review, Cycle 2 Round 1 Flight 2 analytical infrastructure)
