# MANIFEST

**Document role.** Top-level directory listing for the EE Theory Lab repository. Describes what each top-level directory contains, what is canonical, what is pending Stage 3-4 of the restructure, and how to find more detailed indexing. This is the directory-tree-level orientation document; for artifact-level location and authority, see `protocols/foundational/canonical_artifacts_index.md`.

**Authority.** Authoritative for the top-level directory layout. Not authoritative for what lives inside subdirectories (defers to the artifacts index and to in-subdirectory README files where they exist).

**Maintenance discipline.** Updated when top-level directories are added, moved, or quarantined. Updates committed alongside the operations log of the session in which the change occurred. The restructure stages (Stage 2 moves landed session 12; Stage 3 manifests pending; Stage 4 quarantine pending) trigger updates.

---

## Top-level directories

### `protocols/`

Protocol infrastructure. Currently contains one subdirectory: `protocols/foundational/`, the canonical foundational document set. Six documents specifying protocol structure, standing rules, vocabulary discipline, canonical artifacts, current state, and the foundational set's reading sequence. **Authoritative for protocol structure and standing rules.**

For details: `protocols/foundational/README.md`.

### `phase_4b/`

Phase 4B work — analytical procedures, substrate-output consumers, pre-registrations, regression outputs, derived outputs. Heavy directory. Includes:

- `phase_4b/phase_4b_specification_v1.1.md` (target path reserved at `phase_4b/specifications/`; move deferred to future restructure stage per `canonical_artifacts_index.md` Section 12)
- `phase_4b/scripts/` (Tier 3 canonical implementation: `_phase_4b_intake.py`, `test_intake.py`, `tier3_regression.py`; plus `inspect_tier3_provenance.py` and `merge_globals.py` moved to canonical placement at session 12)
- `phase_4b/pre_registrations/` (reg_01 yaml)
- `phase_4b/tier3_outputs/` (reg_01 outputs — sibling of `scripts/`)
- `phase_4b/tier2_outputs/` (canonical — 65 files including the merged `global_timeseries.csv` bridging artifact; README at `phase_4b/tier2_outputs/README.md` documents the bridging role)
- `phase_4b/tier1_reports/` (canonical — 8 Tier 1 reports across the probe-scale matrix)
- `phase_4b/cross_run_outputs/` (canonical — 3 cross-run analysis files)
- `phase_4b/diagnostics/` (canonical diagnostics directory — diagnostic stdout files, t27 forensic output, earlier cross-run comparison output)
- `phase_4b/reviews/layer3/` (canonical routing-archive — session 5 Layer 2 routing package at `2026-05-18_reg_01_routing_package.txt`)

**Authoritative for Phase 4B procedures, implementations, and outputs.**

For details: `protocols/foundational/canonical_artifacts_index.md` Sections 2-7.

### `flights/`

Flight specifications. Includes:

- `flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf` — Flight 6 Substrate Specification v1.1, **authoritative for substrate implementation**. (Target path reserved at `substrate/flight6_v1_1/specifications/`; move deferred to future restructure stage per `canonical_artifacts_index.md` Section 12.)

Other flight directories may exist but are not currently canonical material for Phase 4B work.

### `operations_log/`

Session-by-session operations logs. Each log captures session arc, substantive findings, procedural findings, items resolved, items not resolved, methodological observations, pending decisions, and resume anchor for the next session. **Authoritative for what happened in past sessions.**

Naming convention: `YYYY-MM-DD_phase_NX_session_K.md` (current convention as of session 7+).

For the canonical list with commit references: `protocols/foundational/canonical_artifacts_index.md` Section 7.

### `claude_session_handoffs/`

Session-handoff folders for cold-starting fresh Claude chats. Each folder is named by date (e.g., `2026-05-20-3/`) and contains:

- The current instantiation kit
- The just-closed session's operations log (load-bearing for next-session orientation)
- Optionally, one or two prior session logs for cross-session continuity

The convention is specified in `protocols/foundational/standing_rules.md` Rule 2.

---

## Top-level files

### `ORIENTATION.md`

Repository entry point. The document a fresh reader (Claude, Mike, or anyone) lands on when first encountering the repository.

### `CURRENT_STATE.md` (this directory level)

Project-level current state — theoretical-architecture state, manuscript-side context, cross-workstream coordination. Complementary to `protocols/foundational/current_state.md`, which is Phase-4B-and-protocol scoped.

### `MANIFEST.md`

This document.

### `RESTRUCTURE_INVENTORY.md`

Stage 0 inventory deliverable. Categorizes the working-tree items from session 8 inventory time into canonical and scratch, with the Stage 2 moves-plan. **Authoritative for the restructure's planned moves** (Stage 2 executed at session 12); committed at `1a68ca6`.

### `STANDING_ITEMS.md`

Deferred-items tracker. Each item has a trigger condition and acceptance criterion per the bullet-proof deferral process. Consulted at session open to check for items whose triggers are met by current HEAD/working-tree state.

### Workspace-root scratch and routing files

A number of items remain at workspace root as of session 12, pending future Stage 4 quarantine or other restructure decisions:

- 22 scratch scripts categorized in `RESTRUCTURE_INVENTORY.md` (Stage 4 quarantine targets)
- `LAYER_2_ROUTING_STAGE1_PAIR{1,2,3}.md` and `LAYER_2_ROUTING_STAGE1_PAIR{1,2,3}_V2_ACCEPTANCE.md` (session 9 routing artifacts; not in the Stage 0 inventory's Stage 2 moves-plan; pending future restructure decision)
- `LAYER_2_ROUTING_KIT_V3_SCAN.md` and `LAYER_2_ROUTING_STAGE1_ORIENTATION_SCAN.md` (session 9 routing artifacts; same status)
- `item9_*` files (session 10 item 9 reconciliation working artifacts)
- `deliverable3_*` files (session 10 working artifacts)
- `stage_1_pair{1,2,3}_commit_message.txt`, `kit_revision_3_commit_message.txt`, `session_9_*_commit_message.txt`, `standing_items_commit_message.txt` (commit-message files used for `git commit -F`; may be cleaned at future session)
- `new_claude_primer_distribution_workflow.md` (session 9 working artifact)
- `D README.md` (deletion pending future cleanup decision)

The `LAYER_1_ROUTING_PACKAGE.txt`, `cross_run_comparisons_df9122e.txt`, `inspect_tier3_provenance.py`, and `merge_globals.py` items previously at workspace root were moved to canonical placement at session 12 (commit `919db5b`).

---

## Pending Stage 3-4 commitments

The Stage 2 moves-plan in `RESTRUCTURE_INVENTORY.md` was executed at session 12 (commit `919db5b` + documentation commit), closing item 3 and item 8 in STANDING_ITEMS. The remaining restructure stages:

- **Stage 3** will add manifests for parquet outputs (per STANDING_ITEMS item 4).
- **Stage 4** will quarantine the 22 scratch scripts and the stale parallel `EE_Theory_Lab/phase_4B/` tree at workspace parent level (per STANDING_ITEMS item 5).
- **Future restructure** will execute the three v1.1 document moves per `canonical_artifacts_index.md` Section 12, scoped separately from the session 12 Stage 2 cluster.

This MANIFEST updates as those stages execute.

---

— Originally drafted by Claude as Layer 1 central node, Stage 1 root-level orientation, session 9. Layer 2 sanity scan return at draft time: no findings. Session 12 Stage 2 closure cluster updated the `phase_4b/` subdirectory listing, the workspace-root scratch and routing files listing, and the Stage 3-4 commitments section to reflect Stage 2 moves landed at `919db5b`.
