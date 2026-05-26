# MANIFEST

**Document role.** Top-level directory listing for the EE Theory Lab repository. Describes what each top-level directory contains, what is canonical, what is quarantined, and how to find more detailed indexing. This is the directory-tree-level orientation document; for artifact-level location and authority, see `protocols/foundational/canonical_artifacts_index.md`.

**Authority.** Authoritative for the top-level directory layout. Not authoritative for what lives inside subdirectories (defers to the artifacts index and to in-subdirectory README files where they exist).

**Maintenance discipline.** Updated when top-level directories are added, moved, or quarantined. Updates committed alongside the operations log of the session in which the change occurred. The restructure stages (Stage 2 moves landed session 12; Stage 3 manifest schema and scaffolding landed session 13; Stage 4 quarantine landed session 14) trigger updates.

---

## Top-level directories

### `protocols/`

Protocol infrastructure. Currently contains one subdirectory: `protocols/foundational/`, the canonical foundational document set. Six documents specifying protocol structure, standing rules, vocabulary discipline, canonical artifacts, current state, and the foundational set's reading sequence. **Authoritative for protocol structure and standing rules.**

For details: `protocols/foundational/README.md`.

### `phase_4b/`

Phase 4B work — analytical procedures, substrate-output consumers, pre-registrations, regression outputs, derived outputs, manifests. Heavy directory. Includes:

- `phase_4b/phase_4b_specification_v1.1.md` (target path reserved at `phase_4b/specifications/`; move deferred to future restructure stage per `canonical_artifacts_index.md` Section 12)
- `phase_4b/scripts/` (Tier 3 canonical implementation: `_phase_4b_intake.py`, `test_intake.py`, `tier3_regression.py`; reproducibility-toolchain scripts `inspect_tier3_provenance.py` and `merge_globals.py` moved to canonical placement at session 12; regenerate-manifest scaffolding `regenerate_manifest.py` added session 13; companion verification module `_manifest_verification.py` is a Layer 3 deliverable not yet added)
- `phase_4b/pre_registrations/` (reg_01 yaml)
- `phase_4b/tier3_outputs/` (reg_01 outputs — sibling of `scripts/`)
- `phase_4b/tier2_outputs/` (canonical — 65 files including the merged `global_timeseries.csv` bridging artifact; README at `phase_4b/tier2_outputs/README.md` documents the bridging role)
- `phase_4b/tier1_reports/` (canonical — 8 Tier 1 reports across the probe-scale matrix)
- `phase_4b/cross_run_outputs/` (canonical — 3 cross-run analysis files)
- `phase_4b/diagnostics/` (canonical diagnostics directory — diagnostic stdout files, t27 forensic output, earlier cross-run comparison output)
- `phase_4b/reviews/layer3/` (canonical routing-archive — session 5 Layer 2 routing package at `2026-05-18_reg_01_routing_package.txt`)
- `phase_4b/manifests/` (canonical manifest directory — parquet manifest schema documentation and CSV; added session 13 Stage 3)

**Authoritative for Phase 4B procedures, implementations, outputs, and manifests.**

For details: `protocols/foundational/canonical_artifacts_index.md` Sections 2-7 and Section 14.

### `cycle2/`

Cycle 2 closure record. Contains `CYCLE2_CLOSURE.md` — the deliberate boundary closure for Cycle 2 (closed 2026-05-24, closure executed 2026-05-25; boundary marker git tag `cycle2-close`). Records what Cycle 2 produced — why the inherited substrate and the `Psi_local` diagnostic could not carry the manuscript-facing claim — and the settled record Cycle 3 inherits. **Authoritative for the Cycle 2 closure boundary.**

For details: `cycle2/CYCLE2_CLOSURE.md`.

### `cycle3/`

Cycle 3 — the current cycle. The precondition-gate apparatus, reproduction environment, and test records preceding the substantive probe phase. Includes:

- `CYCLE3_OVERVIEW.md` — the Cycle 3 frame.
- `CYCLE3_TEST_REGISTRY.md` — the cycle's test index: which tests exist and how far up the four-level discipline (L1 implementation / L2 measurement validity / L3 steady-state eligibility / L4 interpretation) each has cleared. **The in-subdirectory authority for Cycle 3 test state.**
- `TEST_RECORD_TEMPLATE.md` and per-test records — `TEST_RECORD_C3-ENV-001.md` (passed-L1), `TEST_RECORD_C3-CTL-001.md` (valid-L2).
- `c3_ctl_001_battery.py` and `data_out/` — the C3-CTL-001 synthetic control battery (run of record) and its output.
- Reproduction-environment set — `MESA_ENVIRONMENT_REPRODUCTION.md`, `ENVIRONMENT_SNAPSHOT.md`, `requirements.lock.txt`, `mesa_smoke_test.py` — the pinned environment Cycle 3 runs execute in (Python 3.14.4, Mesa 3.5.1, top-level `venv`).
- Resume anchors (`RESUME_*.md`) and new-session instantiation prompts; the highest-dated resume governs.
- `routing/` — cross-layer routing notes.

**Authoritative for Cycle 3 precondition gates, test records, and reproduction environment.**

For details: `cycle3/CYCLE3_OVERVIEW.md` and `cycle3/CYCLE3_TEST_REGISTRY.md`.

### `environment/`

Environment setup material. Contains `Mesa setup.docx` — Mesa setup documentation. Distinct from the cycle-scoped reproduction set under `cycle3/`, which pins the specific environment a given cycle's runs executed in.

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

The convention is specified in `protocols/foundational/standing_rules.md` Rule 2. The directory is untracked-by-design as a session-handoff working surface; tracking status remains an open question pending future arbitration.

### `archive/`

Quarantine for stale and scratch material. Added session 14 (Stage 4 closure). Currently contains:

- `archive/scratch/2026-05_pre_restructure/` — Stage 4 quarantine cluster. Three groups: 23 Group B scratch scripts at top level (the 22 enumerated by RESTRUCTURE_INVENTORY's Stage 0 categorization plus `distribute_new_claude_primer.py` surfaced during execution); the capital-B parallel tree at `capital_B_parallel_tree/phase_4B/` (8 files tracked by git plus 1 gitignored `.pyc`); post-Stage-0 residue at `post_stage0_residue/` (24 items: 8 LAYER_2_ROUTING_*, 7 deliverable3/item9/primer-workflow, 9 commit-message txts).

The `archive/` directory is the destination convention for future quarantine clusters. Subdirectory naming follows `archive/<purpose>/<period_or_event>/` (e.g., `archive/scratch/2026-05_pre_restructure/` for the Stage 4 cluster).

---

## Top-level files

### `ORIENTATION.md`

Repository entry point. The document a fresh reader (Claude, Mike, or anyone) lands on when first encountering the repository.

### `CURRENT_STATE.md` (this directory level)

Project-level current state — theoretical-architecture state, manuscript-side context, cross-workstream coordination. Complementary to `protocols/foundational/current_state.md`, which is Phase-4B-and-protocol scoped.

### `MANIFEST.md`

This document.

### `RESTRUCTURE_INVENTORY.md`

Stage 0 inventory deliverable. Categorizes the working-tree items from session 8 inventory time into canonical and scratch, with the Stage 2 moves-plan. **Authoritative for the restructure's planned moves** (Stage 2 executed at session 12); committed at `1a68ca6`. Amended to v3 at session 14 to document Stage 4 actual executed scope.

### `STANDING_ITEMS.md`

Deferred-items tracker. Each item has a trigger condition and acceptance criterion per the bullet-proof deferral process. Consulted at session open to check for items whose triggers are met by current HEAD/working-tree state.

### Workspace-root state (post-Stage-4)

The session 14 Stage 4 quarantine cluster removed the bulk of workspace-root scratch and routing files. Remaining at workspace root post-Stage-4:

- `D README.md` (deferred deletion, carried since session 9; separate cleanup decision pending)
- `claude_session_handoffs/` (active per Rule 2, untracked-by-design)
- The canonical top-level files enumerated above (`ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`, `RESTRUCTURE_INVENTORY.md`, `STANDING_ITEMS.md`)

The `LAYER_1_ROUTING_PACKAGE.txt`, `cross_run_comparisons_df9122e.txt`, `inspect_tier3_provenance.py`, and `merge_globals.py` items previously at workspace root were moved to canonical placement at session 12 (commit `919db5b`). The 23 scratch scripts, the capital-B parallel tree, and the 24 post-Stage-0 residue items were quarantined to `archive/scratch/2026-05_pre_restructure/` at session 14 Stage 4 closure.

---

## Pending future-restructure commitments

Stage 2 (item 3) executed at session 12 (commits `919db5b` + `adfdb28`). Stage 3 (item 4) executed at session 13 (commit `fc9d4c4`). Stage 4 (item 5) executed at session 14 (this closure cluster). The remaining restructure-adjacent work:

- **Stage 5 transition** (STANDING_ITEMS item 6): next analytical phase. Architectural decision arbitrated by Mike; new pre-registration committed under `phase_4b/pre_registrations/`; Layer 2 full cycle complete; Layer 3 routing in hand. Trigger met by Stage 4 closure.
- **flight2_outputs naming resolution** (STANDING_ITEMS item 12, added session 14): rename the absolute-path `flight2_outputs/` directory to reflect its Flight 6 contents. Surfaced as a discovered gap during session 14 Stage 4 documentation drafting; not in item 5's canonical scope. Trigger: when restructure attention returns to top-level naming, or when a substantive operation surfaces friction from the mismatch.
- **Future restructure** will execute the three v1.1 document moves per `canonical_artifacts_index.md` Section 12, scoped separately.

This MANIFEST updates as those stages execute.

---

— Originally drafted by Claude as Layer 1 central node, Stage 1 root-level orientation, session 9. Layer 2 sanity scan return at draft time: no findings. Session 12 Stage 2 closure cluster updated the `phase_4b/` subdirectory listing, the workspace-root scratch and routing files listing, and the Stage 3-4 commitments section to reflect Stage 2 moves landed at `919db5b`. Session 13 Stage 3 closure cluster updated the `phase_4b/` subdirectory listing to add `phase_4b/manifests/`, updated the script entry to mention `regenerate_manifest.py`, and renamed the trailing section to "Pending Stage 4 commitments" reflecting Stage 3 landed. Session 14 Stage 4 closure cluster added the `archive/` top-level directory entry, replaced the workspace-root scratch and routing files section with the post-Stage-4 state, and renamed the trailing section to "Pending future-restructure commitments" reflecting Stage 4 landed. The 2026-05-25 Cycle 3 / C3-CTL-001 closure cluster added the `cycle2/`, `cycle3/`, and `environment/` top-level directory entries — top-level directories that postdate the Stage 4 restructure documentation.
