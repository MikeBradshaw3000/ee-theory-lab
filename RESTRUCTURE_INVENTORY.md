# Restructure Inventory — Stage 0

**Date:** 2026-05-19 (session 8)
**Working-tree state at inventory time:** HEAD `4e66f27`, 31 untracked items
**Deliverable purpose:** categorize each untracked item as canonical / scratch / superseded, and produce a moves-plan for Stage 2 execution.

**Revision history:**
- v1 (initial draft) — Layer 1 categorization based on filename + operations-log context with inspection of two ambiguous items.
- v2 (this version) — incorporates Layer 2 sanity scan: diagnostics-directory convention adopted, workspace-root placement option removed for `cross_run_comparisons_df9122e.txt`, quarantine path tightened, verification section revised.

---

## Methodology

Session 8 worked through the 31 untracked items grouped by location and type. Items with unambiguous disposition (clear from filename + operations-log context) received blanket categorization; items with ambiguity (`inspect_tier3_provenance.py`, `merge_globals.py`) received primary-source inspection before categorization. The `(c) strategy` is documented in session 8's operations log.

Stage 0 only categorizes. Nothing moves. Stage 2 executes the moves-plan below.

---

## Summary counts

| Disposition | Count | Notes |
|---|---|---|
| Canonical | 9 working-tree entries (74 files counting subdirectory contents) | preserved with Stage 2 moves |
| Scratch | 22 working-tree entries (all scripts at workspace root) | quarantined in Stage 4 |
| Superseded | 0 | none surfaced |
| **Total** | **31 working-tree entries** | matches `git status --short` |

---

## Convention adopted during inventory

**Canonical diagnostics directory: `phase_4b/diagnostics/`.** All diagnostic stdout, log, and forensic-text outputs are placed under this single canonical location. This applies to `cross_run_comparisons_df9122e.txt`, `phase_4b/diagnostic_stdout.txt`, and `phase_4b/t27_diagnostic_stdout.txt`. Workspace-root placement is not used for diagnostic artifacts. This convention is one of Stage 0's structural outputs and is reflected in the Stage 2 moves-plan below.

---

## Group A — Canonical-record candidate (1 item)

| File | Size | Date | Disposition | Stage 2 target |
|---|---|---|---|---|
| `LAYER_1_ROUTING_PACKAGE.txt` | 35,780 B | 2026-05-18 06:57 | **Canonical** | `phase_4b/reviews/layer3/2026-05-18_reg_01_routing_package.txt` |

**Content:** Session-5 Layer 3 → Layer 1 routing package. Four artifact sections (intake module pre-Layer-1-review state, regression consumer pre-review state, regression report, test suite) plus Layer 3 covering note. Confirmed via header scan (lines 1, 22, 414, 598, 740).

**Forensic note:** Contains pre-Layer-1-review state of intake module, regression consumer, report, and tests. The post-review canonical versions are what landed in commit `3189ab7`. The file's value is precisely that it captures the handoff state, not the final state.

---

## Group B — Scratch scripts at workspace root (22 items)

All scripts in this group are one-shot maintenance code from prior sessions. Per session 5 § 38–44 and session 7's working-memory-pattern findings, these scripts were produced during debug cycles or content-distribution operations and were never intended for canonical-record preservation.

### Session-4 fix-script cluster (8 items, all scratch)

Per session 5 § 38–44, the working-memory-pattern instances from session 4. All quarantined in Stage 4.

| File | Disposition |
|---|---|
| `fix_cluster_var_alias.py` | Scratch |
| `fix_codefence.py` | Scratch |
| `fix_conflict.py` | Scratch |
| `fix_outcome_name.py` | Scratch |
| `fix_path_resolution.py` | Scratch |
| `fix_t2_sanity_columns.py` | Scratch |
| `fix_t2_sanity_v2.py` | Scratch |
| `fix_t2_sanity_v3.py` | Scratch |

### V8 diagnostic family (4 items, all scratch)

Numbered debugging iteration ("v8"). One-shot diagnostic scripts.

| File | Disposition |
|---|---|
| `build_v8_tick0_patch.py` | Scratch |
| `diagnose_v8_failure.py` | Scratch |
| `diagnose_v8_formula.py` | Scratch |
| `diagnose_v8_tick0.py` | Scratch |

### Distribute scripts (5 items, all scratch)

One-shot content-distribution helpers. Each name references a specific session event.

| File | Disposition |
|---|---|
| `distribute_fabrication_incident.py` | Scratch |
| `distribute_phase_4b_v1.py` | Scratch |
| `distribute_phase_4b_v1_1.py` | Scratch |
| `distribute_rule_6_refinement.py` | Scratch |
| `distribute_session_log.py` | Scratch |

### Other one-shot patches and writers (5 items, all scratch)

| File | Disposition |
|---|---|
| `build_t22_patch.py` | Scratch |
| `patch_cross_run_diagnostics.py` | Scratch |
| `patch_t27_refactor_tightened.py` | Scratch |
| `write_tier3.py` | Scratch — canonical `tier3_regression.py` already exists in `phase_4b/scripts/` |
| `write_yaml.py` | Scratch |

### Inspected scripts (2 items, both canonical) — moved out of Group B's scratch list

These two scripts were inspected during session 8 and reclassified as canonical. They appear in Group F (canonical scripts) below to keep Group B's scratch list clean.

---

## Group C — Workspace-root canonical txt file (1 item)

| File | Disposition | Stage 2 target |
|---|---|---|
| `cross_run_comparisons_df9122e.txt` | **Canonical** | `phase_4b/diagnostics/cross_run_comparisons_df9122e.txt` |

**Content:** Earlier cross-run comparison output. Suffix `df9122e` appears to be a git short-hash tagging the output to a specific commit at generation time — a discipline pattern worth preserving and possibly formalizing as a Stage 1 standing rule.

**Stage 2 placement:** under the canonical diagnostics directory. Workspace-root placement is not used (would recreate the mixed-forensic-surface problem Stage 0 is solving).

---

## Group D — Phase 4B diagnostic stdouts (2 items)

| File | Size | Date | Disposition | Stage 2 target |
|---|---|---|---|---|
| `phase_4b/diagnostic_stdout.txt` | 3,190 B | 2026-05-17 06:10 | **Canonical** | `phase_4b/diagnostics/diagnostic_stdout.txt` |
| `phase_4b/t27_diagnostic_stdout.txt` | 2,688 B | 2026-05-17 07:19 | **Canonical** | `phase_4b/diagnostics/t27_diagnostic_stdout.txt` |

**Date observation:** both files dated 2026-05-17, one calendar day before "session 5" (2026-05-18). The files were generated during cross-run runs the morning of 5/17 and consumed analytically in sessions 5 and 6. Operations-log narrative compresses out the calendar gap; the filesystem timestamps preserve it.

---

## Group E — Phase 4B derived-output subdirectories (3 items, 65 files)

### `phase_4b/cross_run_outputs/` (3 files, all canonical)

| File | Size | Date |
|---|---|---|
| `cross_scale_metrics.csv` | 37,061 B | 2026-05-17 07:19 |
| `cross_scale_report.md` | 460 B | 2026-05-17 07:19 |
| `fform_comparison.csv` | 2,382 B | 2026-05-17 07:19 |

### `phase_4b/tier1_reports/` (8 files, all canonical)

Eight Tier 1 reports across the four-probe × two-scale matrix (probe1_overcrowding, probe2_starvation_F2sym, probe2_starvation_FLR, probe3_fusion_residual × 20x20, 40x40). All generated 2026-05-16 evening.

### `phase_4b/tier2_outputs/` (65 files, all canonical)

64 per-probe-scale derived outputs (eight metric types × four probe types × two scales) plus one merged `global_timeseries.csv`. Structure verified via group-count: 8 metric types × 8 probe-scale combinations = 64, plus the unsuffixed merged file.

**Merged-globals confirmed canonical.** `global_timeseries.csv` (13,585,461 B, 2026-05-17 20:27) is the Tier 2 → Tier 3 bridging artifact produced by `merge_globals.py` (timestamps differ by 24 seconds). Contains `run_id` column to support Tier 3 clustering. Columns match what session-7's log § 22 describes as the canonical Tier 2 globals inspected during derived_variables resolution.

**Stage 2 recommendation:** rename merged file or add `phase_4b/tier2_outputs/README.md` documenting its bridging role. Recommendation is a Stage 2 / Stage 3 decision, not a Stage 0 categorization.

---

## Group F — Canonical scripts at workspace root (2 items, reclassified from Group B during inspection)

| File | Size | Date | Disposition | Stage 2 target |
|---|---|---|---|---|
| `inspect_tier3_provenance.py` | 12,141 B | 2026-05-17 16:18 | **Canonical** | `phase_4b/scripts/inspect_tier3_provenance.py` |
| `merge_globals.py` | 891 B | 2026-05-17 20:27 | **Canonical** | `phase_4b/scripts/merge_globals.py` |

**`inspect_tier3_provenance.py`:** Reusable provenance-inspection tool. Cross-checks parquet files against the canonical four filenames in `reg_01_scale_interactions.yaml`. Validates expected metadata (PRNG_seed 128561948, substrate_version v1.1, total ticks 3000, column count 25). Output for human review; does not pick canonical files automatically. Hardcoded path `WORKSPACE_ROOT = Path(r"C:\Users\vkz244\EE_Theory_Lab")` — refactoring to `get_paths()` pattern is a Stage 5 concern.

**`merge_globals.py`:** Producer of canonical `global_timeseries.csv`. Globs `global_timeseries_*.csv` files in `phase_4b/tier2_outputs/`, injects filename-derived `run_id` column, concatenates, writes master. Load-bearing on reproducibility — if pre-registration reproducibility verification (standing item) needs to regenerate the merged globals, this is the script.

---

## Stage 2 moves-plan

Executed in Stage 2 via `git mv` (preserving git history). Files marked scratch are not moved here; they go to quarantine in Stage 4.

### Moves for canonical items

| Source | Target |
|---|---|
| `LAYER_1_ROUTING_PACKAGE.txt` | `phase_4b/reviews/layer3/2026-05-18_reg_01_routing_package.txt` |
| `inspect_tier3_provenance.py` | `phase_4b/scripts/inspect_tier3_provenance.py` |
| `merge_globals.py` | `phase_4b/scripts/merge_globals.py` |
| `cross_run_comparisons_df9122e.txt` | `phase_4b/diagnostics/cross_run_comparisons_df9122e.txt` |
| `phase_4b/diagnostic_stdout.txt` | `phase_4b/diagnostics/diagnostic_stdout.txt` |
| `phase_4b/t27_diagnostic_stdout.txt` | `phase_4b/diagnostics/t27_diagnostic_stdout.txt` |

Items already in `phase_4b/` derived-output subdirectories (Group E) need no path moves but should be staged and committed as part of Stage 2's canonical-baseline commit.

### Quarantine for scratch items (Stage 4)

All 22 scripts in Group B go to `archive/scratch/2026-05_pre_restructure/`.

---

## Open items surfaced during Stage 0

1. **Hash-tagging convention** for output files (e.g., the `df9122e` suffix on `cross_run_comparisons_df9122e.txt`). Worth considering as a Stage 1 standing rule if it surfaces elsewhere. The convention has informal value (tags output to a specific commit at generation time); formalizing it would make the value explicit.

2. **`global_timeseries.csv` naming/documentation** — Stage 2 or Stage 3 decision: rename for explicit role-labeling (e.g., `tier2_to_tier3_merged_globals.csv`) or add a README in `phase_4b/tier2_outputs/` documenting its bridging role.

3. **Pre-registration reproducibility verification** — standing item from session 7. Now feasible: `merge_globals.py` + `inspect_tier3_provenance.py` + `tier3_regression.py` together constitute the reproducibility toolchain. Re-running `tier3_regression.py` against the committed yaml should produce the committed reg_01 outputs.

4. **Date-vs-session-narrative gap** — `phase_4b/diagnostic_stdout.txt` is dated 5/17 but is described in operations logs as a session-5 artifact (session 5 = 2026-05-18). Worth noting but not a categorization issue.

---

## Verification

**Layer 1 tree-vs-inventory cross-check (session 8).** Every `git status --short` untracked item maps to an inventory entry; every inventory entry maps to a `git status --short` item. Cross-check executed during inventory work. This is a Layer 1 record, not independent proof of correctness.

**Layer 2 sanity scan (session 8, ChatGPT).** Independent read of the v1 inventory against the same `git status` output. Coverage check clean; categorization check identified one item (`cross_run_comparisons_df9122e.txt`) where the v1 inventory left workspace-root as an option that should be removed; moves-plan check identified path tightening for the same item plus a quarantine-path cleanup; open-items check suggested adding a canonical diagnostics directory convention. All flags incorporated in v2. The Layer 2 read was against the inventory document, not against independent inspection of the working tree itself; consistency confirmation rather than independent verification.

**Per-item disposition discipline.** Each scratch-categorized item was assigned by filename + operations-log context (session 5 § 38–44 for the fix-script cluster, naming conventions for the v8 and distribute families). Per-item primary-source inspection was performed for `inspect_tier3_provenance.py` and `merge_globals.py`; both reclassified canonical based on inspection results. Spot-check on remaining scratch items remains available at Mike's discretion before Stage 4 quarantine executes.

---

— Drafted with Claude as Layer 1 central node, session 8, pre-Stage-2 inventory deliverable. v2 incorporates Layer 2 sanity scan from ChatGPT.
