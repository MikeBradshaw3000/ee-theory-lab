# Tier 2 Outputs

**Directory role.** Phase 4B Tier 2 derived outputs. The 65 files in this directory comprise two distinct artifact categories: 64 per-probe-scale derived outputs, and one merged bridging artifact.

## File inventory

### Per-probe-scale derived outputs (64 files)

Eight metric types × eight probe-scale combinations = 64 files. The eight metric types:

- `base_boundary_summary_*` (8 files)
- `compression_fingerprint_*` (8 files)
- `epoch_summary_*` (8 files)
- `global_timeseries_*` (8 files — note plural; per-probe-scale, distinct from the merged file described below)
- `psi_sign_decomposition_*` (8 files)
- `psi_spatial_diagnostics_*` (8 files)
- `q_effect_decomposition_*` (8 files)
- `selected_tick_distributions_*` (8 files)

Each file is named by probe-scale: `flight6_probe{N}_{description}_{scale}` where N is 1-3, description varies, and scale is 20x20 or 40x40. Probes 1, 3 contribute one variant each; probe 2 contributes two F-form variants (F2sym, FLR).

### Merged bridging artifact (1 file)

`global_timeseries.csv` (no probe-scale suffix) is the Tier 2 → Tier 3 bridging artifact. Distinct from the per-probe-scale `global_timeseries_*.csv` files described above.

**Role.** Produced by `phase_4b/scripts/merge_globals.py`, which globs `global_timeseries_*.csv` files in this directory, injects a filename-derived `run_id` column to preserve probe-scale provenance, concatenates, and writes the master. The resulting file (~13.5 MB) is what `tier3_regression.py` consumes via `attach_tier2_globals`.

**Why the naming.** The unsuffixed file shares a stem with the per-probe-scale files (`global_timeseries`) because it is constructed from them. The absence of a probe-scale suffix is the disambiguation: per-probe-scale files have suffixes, the merged master does not. This README documents the convention to prevent confusion when fresh-Claude sessions or other readers encounter the directory listing.

**Canonical status.** Confirmed canonical during session 8 Stage 0 inventory; landed at canonical placement at session 12 (commit `919db5b`, Stage 2 commit 1). Load-bearing for Tier 3 reproducibility: if pre-registration reproducibility verification needs to regenerate the merged globals, `merge_globals.py` is the script.

## Item 8 disambiguation note

STANDING_ITEMS item 8 (closed at session 12) arbitrated the disambiguation choice between renaming the merged file (e.g., to `tier2_to_tier3_merged_globals.csv`) and adding a README. The README path was selected as the lower-risk option: rename would have required updating both `merge_globals.py`'s output target and `tier3_regression.py`'s input expectation, while README documents the bridging role without touching the operational artifact. This file is the disambiguation deliverable.

---

— Drafted by Claude as Layer 1 central node, session 12 Stage 2 closure cluster (item 3 + item 8 closure), 2026-05-20. Per Mike's arbitration (Arbitration 1 of the Stage 2 cluster): README path, not rename.
