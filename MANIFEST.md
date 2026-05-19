# MANIFEST

**Document role.** Top-level directory listing for the EE Theory Lab repository. Describes what each top-level directory contains, what is canonical, what is pending Stage 2-4 of the restructure, and how to find more detailed indexing. This is the directory-tree-level orientation document; for artifact-level location and authority, see `protocols/foundational/canonical_artifacts_index.md`.

**Authority.** Authoritative for the top-level directory layout. Not authoritative for what lives inside subdirectories (defers to the artifacts index and to in-subdirectory README files where they exist).

**Maintenance discipline.** Updated when top-level directories are added, moved, or quarantined. Updates committed alongside the operations log of the session in which the change occurred. The restructure stages (especially Stage 2 moves, Stage 4 quarantine) will trigger updates.

---

## Top-level directories

### `protocols/`

Protocol infrastructure. Currently contains one subdirectory: `protocols/foundational/`, the canonical foundational document set. Six documents specifying protocol structure, standing rules, vocabulary discipline, canonical artifacts, current state, and the foundational set's reading sequence. **Authoritative for protocol structure and standing rules.**

For details: `protocols/foundational/README.md`.

### `phase_4b/`

Phase 4B work — analytical procedures, substrate-output consumers, pre-registrations, regression outputs, derived outputs. Heavy directory. Includes:

- `phase_4b/specifications/` (target post-Stage-2; currently `phase_4b/phase_4b_specification_v1.1.md` at directory root)
- `phase_4b/scripts/` (Tier 3 canonical implementation: `_phase_4b_intake.py`, `test_intake.py`, `tier3_regression.py`)
- `phase_4b/pre_registrations/` (reg_01 yaml)
- `phase_4b/tier3_outputs/` (reg_01 outputs — sibling of `scripts/`)
- `phase_4b/tier2_outputs/` (currently untracked, pending Stage 2 — 65 files including the canonical merged `global_timeseries.csv`)
- `phase_4b/tier1_reports/` (currently untracked, pending Stage 2)
- `phase_4b/cross_run_outputs/` (currently untracked, pending Stage 2)
- `phase_4b/diagnostics/` (target post-Stage-2; currently diagnostic stdout files at `phase_4b/` directory root)

**Authoritative for Phase 4B procedures, implementations, and outputs.**

For details: `protocols/foundational/canonical_artifacts_index.md` Sections 2-6.

### `flights/`

Flight specifications. Includes:

- `flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf` — Flight 6 Substrate Specification v1.1, **authoritative for substrate implementation**.

Other flight directories may exist but are not currently canonical material for Phase 4B work.

### `operations_log/`

Session-by-session operations logs. Each log captures session arc, substantive findings, procedural findings, items resolved, items not resolved, methodological observations, pending decisions, and resume anchor for the next session. **Authoritative for what happened in past sessions.**

Naming convention: `YYYY-MM-DD_phase_NX_session_K.md` (current convention as of session 7+).

For the canonical list with commit references: `protocols/foundational/canonical_artifacts_index.md` Section 7.

### `claude_session_handoffs/`

Session-handoff folders for cold-starting fresh Claude chats. Each folder is named by date (e.g., `2026-05-19-2/`) and contains:

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

Stage 0 inventory deliverable. Categorizes the working-tree items from session 8 inventory time into canonical and scratch, with the Stage 2 moves-plan. **Authoritative for the restructure's planned moves**; committed at `1a68ca6`.

### `STANDING_ITEMS.md` (pending Stage 1)

Deferred-items tracker. Each item has a trigger condition and acceptance criterion per the bullet-proof deferral process. Consulted at session open to check for items whose triggers are met by current HEAD/working-tree state.

### Workspace-root scratch and routing files (pending Stage 2)

A number of items remain at workspace root as of session 9, pending Stage 2 `git mv` operations:

- 22 scratch scripts categorized in `RESTRUCTURE_INVENTORY.md` (Stage 4 quarantine targets)
- `LAYER_1_ROUTING_PACKAGE.txt` (session 5 routing artifact; Stage 2 archive)
- `LAYER_2_ROUTING_STAGE1_PAIR{1,2,3}.md` and `LAYER_2_ROUTING_STAGE1_PAIR{1,2,3}_V2_ACCEPTANCE.md` (session 9 routing artifacts; Stage 2 archive)
- `cross_run_comparisons_df9122e.txt` (Stage 2 move to `phase_4b/diagnostics/`)
- `stage_1_pair{1,2,3}_commit_message.txt` (used for `git commit -F`; may be cleaned at session end)

The two recently-reclassified canonical scripts (`inspect_tier3_provenance.py`, `merge_globals.py`) also sit at workspace root pending Stage 2 move to `phase_4b/scripts/`.

---

## Pending Stage 2-4 commitments

The Stage 2 moves-plan in `RESTRUCTURE_INVENTORY.md` will execute the following structural moves:

- Phase 4B specification and Flight 6 substrate specification to qualified-path locations (per `protocols/foundational/canonical_artifacts_index.md` Section 11).
- Diagnostic stdout files to `phase_4b/diagnostics/`.
- Tier 2, Tier 1, cross-run output directories from untracked to canonical placement.
- Routing artifacts to a routing-archive path.
- Reclassified canonical scripts to `phase_4b/scripts/`.

Stage 4 will quarantine the 22 scratch scripts and the stale parallel `EE_Theory_Lab/phase_4B/` tree (capital B at workspace parent level). Stage 3 will add manifests for parquet outputs.

This MANIFEST updates as those stages execute.

---

— Drafted by Claude as Layer 1 central node, Stage 1 root-level orientation, session 9. Layer 2 sanity scan return: no findings against this document. Ready for commit.
