# Canonical Artifacts Index

**Document role.** Authoritative index of the canonical artifacts that constitute the EE Theory Lab record. For each artifact, the index specifies: what it is, where it lives, and what authority it carries. This is the document a fresh Claude instance consults to locate primary source for any verification under Rule 1.

**Authority.** This document is authoritative for *where* canonical artifacts live and *what authority* they carry. It is not authoritative for the artifacts' content; each artifact is its own authority on its content domain. When this index conflicts with primary source (the actual files at the stated paths), primary source wins and this document revises.

**Maintenance discipline.** Updated when canonical artifacts are added, moved, or superseded. Updates committed alongside the operations log of the session in which the change occurred. Stage 2 of the repository restructure (moves canonical artifacts to qualified-path locations) triggered a coordinated update of this index at session 12 (commit cluster `919db5b` + `adfdb28`). Stage 3 (manifest schema + scaffolding) triggered an update at session 13 adding Section 14. Stage 4 (quarantine) triggered an update at session 14 to Sections 5, 7, 8, 11, 13. The 2026-05-25 Cycle 3 / C3-CTL-001 closure added Section 15 (cycle records).

**Path conventions.** All paths relative to `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` unless absolute. PowerShell uses backslash separators; git status output uses forward slashes; both refer to the same files.

**Relationship to other foundational documents.**
- `protocol_primer.md` specifies who uses these artifacts and how.
- `standing_rules.md` specifies the disciplines (especially Rule 1) under which artifacts are consulted.
- `vocabulary_quarantine.md` specifies the language used when discussing the artifacts.
- `current_state.md` tracks session-volatile state; `theoretical_context.md` tracks stable theoretical/historical content; `environment_reference.md` tracks operational/environmental detail; `personal_context.md` tracks personal-context discipline.

---

## Section 1: Theory-level documents

### State of the Theory v1.1

The committed theoretical architecture; ten sections; "hard core." Authority: formal theoretical commitments. Defines the four open elements (μ(ρ), F(v,c,r), Q, nucleation mechanism), the two-stage Landau cascade structure, the critical ontological constraint (ACTION not decision), and the architecture's exclusionary clauses.

**Path:** Mike's local file (not in the repository's tracked tree as of session 12).

**Operational locatability:** requires Mike-provided attachment for any verification-against-primary-source check. A target path is reserved at `theory\state_of_theory\state_of_theory_v1_1.md` per Section 12; the move is deferred to a future restructure stage (see Section 12). Until the file is in the tracked tree, Layer 1 cannot verify content claims about this document without explicit Mike-provided access.

**Citation:** "State of the Theory v1.1." Do not cite "v1.1" alone without qualifier — multiple v1.1 documents exist (see naming-collision note below).

### State of the Theory v1.5 Overview

Manuscript foundation Phil writes from; v1.4 MFA underneath. Authority: manuscript-facing material. The leading edge of the team's worked-out positions has moved past v1.5 in places (e.g., the flagged "modest-resources-outperform-abundant" passage); v1.5 absorbs back-flow from those developments as Phil revises.

**Path:** Mike's local file (not in the repository's tracked tree as of session 12).

**Operational locatability:** requires Mike-provided attachment for verification. No committed restructure target yet; the v1.5 Overview's repository placement is a question for Mike to arbitrate when manuscript work surfaces a need.

**Citation:** "State of the Theory v1.5 Overview" or "v1.5 Overview" with context.

---

## Section 2: Phase 4B specifications

### Phase 4B Specification v1.1

Analytical procedures for Phase 4B: Tier 1 strict matching, Tier 2 coarser matching, Tier 3 interpretable regression with pre-specified interaction families, two-field empirical_result × structural_status classification, cross-scale analysis. Authority: Phase 4B analytical procedures.

**Path:** `phase_4b\phase_4b_specification_v1.1.md`

**Verified:** session 9.

**Note on future placement:** A target path is reserved at `phase_4b\specifications\phase_4b_specification_v1_1.md` per Section 12; the move is deferred to a future restructure stage (see Section 12).

**Citation:** "Phase 4B Specification v1.1."

### Flight 6 Substrate Specification v1.1

Substrate implementation: the cellular engine that produces .parquet telemetry. Sections 6 and 8 specify the deterministic probability chain (Drive_Raw → p_base → p_act → realization) that reg_01 recovered. Section 13.2 specifies the shadow-copy structure (F_2_symmetric runs at each scale produce one underlying parquet file, three probe-named files via byte-identical shadow copies; F_LR runs produce one parquet file each). Section 14.1 specifies the per-artifact verification structure (file existence, file size, row count, column count, required columns, tick range, unique cells, F_variant, non-empty, realization invariant, clipping summary) — referenced by Section 14 below. Section 15 enumerates implementation prohibitions; the protocol-applicable subset is lifted to `standing_rules.md` Rule 7.

Authority: substrate implementation.

**Path:** `flights\flight_6\Flight6_Substrate_Specification_v1.1.md.pdf`

**Verified:** session 6 (located and read end-to-end), session 9 (path re-verified, Section 15 re-verified against primary source).

**Note on future placement:** A target path is reserved at `substrate\flight6_v1_1\specifications\flight6_substrate_specification_v1_1.md` per Section 12; the move is deferred to a future restructure stage (see Section 12).

**Citation:** "Flight 6 Substrate Specification v1.1" or "FSS v1.1" with context.

---

## Section 3: Tier 3 canonical implementation

The Tier 3 implementation cluster committed at `3189ab7` (session 7 reconciliation) plus the reproducibility-toolchain scripts moved to canonical placement at session 12 (commit `919db5b`) plus the regenerate-manifest scaffolding added at session 13 (Stage 3). All paths under `phase_4b\scripts\`.

### Intake module

Implements the seven-item structural-correctness checklist per intake specification. Defines `NormalizedPrereg` dataclass, the schema validator, the `attach_tier2_globals` merge function, and (added session 11 per item 11 closure) `construct_outcome`.

**Path:** `phase_4b\scripts\_phase_4b_intake.py`

**Commit:** introduced at `3189ab7`; updated session 11 (`b8a6833`).

### Test suite

Demonstrates all five exception types fire on deliberate violations. Routes inputs through the actual validation pipeline (not via mock objects per Rule 7.2).

**Path:** `phase_4b\scripts\test_intake.py`

**Commit:** introduced at `3189ab7`.

### Refactored regression consumer

Contract-mediated per intake §1.6. Reads pre-registration yaml, normalizes via the intake module, attaches Tier 2 globals, executes the regression, writes outputs. The construction-phase ordering (added session 11) calls `construct_outcome` between `construct_derived_variables` and `attach_tier2_globals` in `run_tier3`.

**Path:** `phase_4b\scripts\tier3_regression.py`

**Commit:** introduced at `3189ab7`; updated session 11 (`b8a6833`).

### Provenance inspection tool

Reusable provenance-inspection tool. Cross-checks parquet files against the canonical four filenames in `reg_01_scale_interactions.yaml`. Validates expected metadata (PRNG_seed 128561948, substrate_version v1.1, total ticks 3000, column count 25). Output for human review; does not pick canonical files automatically.

**Path:** `phase_4b\scripts\inspect_tier3_provenance.py`

**Commit:** moved to canonical placement at `919db5b` (session 12 Stage 2 commit 1).

### Merged globals producer

Producer of canonical `global_timeseries.csv`. Globs `global_timeseries_*.csv` files in `phase_4b/tier2_outputs/`, injects filename-derived `run_id` column, concatenates, writes master. Load-bearing on reproducibility — if pre-registration reproducibility verification needs to regenerate the merged globals, this is the script.

**Path:** `phase_4b\scripts\merge_globals.py`

**Commit:** moved to canonical placement at `919db5b` (session 12 Stage 2 commit 1).

### Regenerate-manifest scaffolding

Canonical scaffolding for the parquet manifest regeneration flow. Stage 3 deliverable: establishes the contract for Layer 3 implementation (manifest discovery, identity/structure parsing, FSS §14.1 verification invocation, provenance population, deterministic ordering, atomic write). Per Mike's Q2b arbitration: Stage 3 is scaffolding only; Layer 3 routing implements the substantive logic. Per Mike's arbitration C: verification logic lives in a separate module at `phase_4b\scripts\_manifest_verification.py` (also Layer 3 deliverable).

**Path:** `phase_4b\scripts\regenerate_manifest.py`

**Commit:** introduced at session 13 Stage 3 closure cluster (`fc9d4c4`).

**Companion module (Layer 3 implementation):** `phase_4b\scripts\_manifest_verification.py` — reusable verification module implementing the FSS §14.1 check set. Imported by `regenerate_manifest.py` per the existing `_phase_4b_intake.py` + `tier3_regression.py` pattern.

---

## Section 4: reg_01 pre-registration and outputs

The committed reg_01 cluster. Pre-registration committed at `3189ab7`. Outputs initially committed at `3189ab7`; canonical outputs replaced at session 11 (`b8a6833`) per item 11 closure (outcome-construction wired into pipeline; new pipeline outputs canonical, historical outputs at `3189ab7` accessible via git). The pre-registration's `interpretation_boundary` content was restored from session 5's log to the canonical yaml during session 7's reconciliation.

### Pre-registration

Schema is contract-mediated intake format. `derived_variables` block declares per-run/tick constructions for `Local_Density_squared`, `rho_global`, `psi_global`. `interpretation_boundary.licenses` list (5 items) and `does_not_adjudicate` (4 items) restored under new schema; substantive scope matches session 5's log.

**Path:** `phase_4b\pre_registrations\reg_01_scale_interactions.yaml`

**Commit:** `3189ab7`.

### Primary coefficients

**Path:** `phase_4b\tier3_outputs\coefs_reg_01_scale_interactions.csv`

**Commit:** `3189ab7` (initial); canonical replaced at `b8a6833` (session 11).

### Sensitivity coefficients

**Path:** `phase_4b\tier3_outputs\coefs_reg_01_scale_interactions_sensitivity_cell.csv`

**Commit:** `3189ab7` (initial); canonical replaced at `b8a6833` (session 11).

### Regression report

**Path:** `phase_4b\tier3_outputs\report_reg_01_scale_interactions.md`

**Commit:** `3189ab7` (initial); canonical replaced at `b8a6833` (session 11).

**Note:** the `tier3_outputs/` directory is at `phase_4b\tier3_outputs\` (sibling of `scripts/`), NOT `phase_4b\scripts\tier3_outputs\`. The kit-revision-1 had this wrong; corrected in kit-revision-2 and verified during session 7.

---

## Section 5: Substrate data and Tier 2 derived outputs

### Canonical substrate data

Eight Flight 6 production parquet files (Flight 2 naming inheritance preserved). Four genuine substrate runs plus four byte-identical shadow copies per Flight 6 Substrate Specification §13.2. PRNG_seed 128561948, substrate_version v1.1.

**Path (absolute):** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\`

**Note on naming.** The directory is named `flight2_outputs` for inheritance reasons but contains Flight 6 files. The naming mismatch was previously framed for Stage 4 resolution in earlier revisions of this Section 5; STANDING_ITEMS item 5's canonical scope as committed at session 14 start named only the 22 scratch scripts and the capital-B parallel tree, not the `flight2_outputs/` rename. Per Mike's A+C arbitration at session 14: honest-record the gap; promote naming resolution to its own tracked item (STANDING_ITEMS item 12 added session 14). The naming mismatch persists; resolution deferred per item 12.

**Per-file verification record:** the manifest at `phase_4b\manifests\parquet_manifest.csv` documents each physical file's identity, shadow-copy status, and FSS §14.1 verification payload. See Section 14 below.

### Tier 2 derived outputs

65 files. Per-probe-scale derived outputs (8 metric types × 8 probe-scale combinations = 64 files) plus the merged `global_timeseries.csv` bridging artifact (13.5MB, the canonical Tier 2 → Tier 3 join surface produced by `merge_globals.py`; status confirmed canonical during session 8's Stage 0 inventory). A README at `phase_4b\tier2_outputs\README.md` (added session 12 per item 8 closure) documents the merged-globals bridging role to disambiguate it from the per-probe-scale `global_timeseries_*.csv` files.

**Path:** `phase_4b\tier2_outputs\`

### Tier 1 reports

Eight Tier 1 reports across the four-probe × two-scale matrix.

**Path:** `phase_4b\tier1_reports\`

### Cross-run analysis outputs

Three cross-run analysis files dated 5/17/2026 morning.

**Path:** `phase_4b\cross_run_outputs\`

**Status:** these three directories (`tier2_outputs/`, `tier1_reports/`, `cross_run_outputs/`) were categorized as canonical in `RESTRUCTURE_INVENTORY.md` (committed at `1a68ca6`) and landed at canonical placement at session 12 (commit `919db5b`, Stage 2 commit 1).

---

## Section 6: Diagnostic and forensic-text outputs

Per the Stage 0 canonical diagnostics directory convention (adopted session 8), all diagnostic stdout, log, and forensic-text outputs are located under `phase_4b/diagnostics/`. Moves to canonical placement landed at session 12 (commit `919db5b`, Stage 2 commit 1).

### Session 5 diagnostic stdout

**Path:** `phase_4b\diagnostics\diagnostic_stdout.txt`

**Commit:** moved to canonical placement at `919db5b` (session 12 Stage 2 commit 1).

### Session 6 t27 forensic output

**Path:** `phase_4b\diagnostics\t27_diagnostic_stdout.txt`

**Commit:** moved to canonical placement at `919db5b` (session 12 Stage 2 commit 1).

### Earlier cross-run comparison output

**Path:** `phase_4b\diagnostics\cross_run_comparisons_df9122e.txt`

**Commit:** moved to canonical placement at `919db5b` (session 12 Stage 2 commit 1).

---

## Section 7: Operations logs and routing artifacts

### Operations logs

All committed. Paths under `operations_log\`. The directory has a `README.md` documenting filename conventions, authorship, the honest-record principle, and pointers to the current standing-rules location.

**Authority:** Canonical historical record of session-by-session decisions, gate closures, discipline events, and protocol additions. Per the README's honest-record principle, entries are not retroactively edited; later entries that correct earlier ones preserve both.

The directory spans prior-cycle work (May 14-19 entries documenting Cycle 2 Round 1 work) and current Phase 4B work (sessions 2-onward).

| Session/event | Path | Commit |
|---------------|------|--------|
| Prior-cycle work (May 14-19) | `operations_log\2026-05-14_*` through `operations_log\2026-05-19_*` (16 entries) | various commits up to `5d91828` |
| 5 | `operations_log\2026-05-18_phase_4b_session_5.md` | `3189ab7` |
| 6 | `operations_log\2026-05-19_phase_4b_session_6.md` | `3189ab7` |
| 7 | `operations_log\2026-05-19_phase_4b_session_7.md` | `4e66f27` |
| 8 | `operations_log\2026-05-19_phase_4b_session_8.md` | `3e38980` |
| 9 | `operations_log\2026-05-20_phase_4b_session_9.md` | `ff2704d` (original log), addendum at `53aa62e`, date-revert at `5f5a762` |
| 10 | `operations_log\2026-05-20_phase_4b_session_10.md` | `93e6dbb` (original), addendum at `207b484` |
| 11 | `operations_log\2026-05-20_phase_4b_session_11.md` | `b8a6833` |
| 12 | `operations_log\2026-05-20_phase_4b_session_12.md` | `6fb607d` (item 2 closure cluster); extended Stage 2 closure at `cc851a5` |
| 13 | `operations_log\2026-05-20_phase_4b_session_13.md` | `fc9d4c4` (Stage 3 closure cluster) |
| 14 | `operations_log\2026-05-20_phase_4b_session_14.md` | Stage 4 closure cluster (pending this commit) |

### Architectural reviews

Five Layer 1 architectural review documents from May 14-15 2026, covering A3 parity code, Flight 1 v1.1 implementation, v1.1/A3 divergence, Flight 2 analysis script, and Flight 2 substrate.

**Path:** `protocols\architectural_reviews\`

**Authority:** Canonical historical record of Layer 1 review outputs, parallel to operations logs. Each review documents what was checked, what passed, what was deferred or flagged. The directory has a `README.md` documenting its role.

The directory is open for new entries (Layer 1 architectural reviews of future substrate/analysis code).

**Verified:** session 10 (item 9 reconciliation, primary-source read of all five reviews completed).

### Routing artifacts

**Layer 1 routing package (session 5).** The session 5 Layer 2 routing package on reg_01 interpretation, containing four artifact sections (intake module pre-Layer-1-review state, regression consumer pre-review state, regression report, test suite) plus Layer 3 covering note. Captures the handoff state, not the final state (post-review canonical versions landed at `3189ab7`).

**Path:** `phase_4b\reviews\layer3\2026-05-18_reg_01_routing_package.txt`

**Commit:** moved to canonical placement at `919db5b` (session 12 Stage 2 commit 1).

**Stage 1 routing packages (session 9).** `LAYER_2_ROUTING_STAGE1_PAIR1.md`, `LAYER_2_ROUTING_STAGE1_PAIR1_V2_ACCEPTANCE.md`, and the other Stage 1 routing artifacts at workspace root were quarantined at session 14 Stage 4 closure cluster (per Mike's scope-expansion arbitration to include post-Stage-0 residue). Location: `archive\scratch\2026-05_pre_restructure\post_stage0_residue\`. Not canonical going forward — Stage 1 work landed in the commits the routing packages helped produce; the packages themselves are working artifacts now archived.

---

## Section 8: Stage 0 inventory and restructure planning

### RESTRUCTURE_INVENTORY.md

The Stage 0 deliverable. Categorizes the 31 untracked items as of session 8 inventory time into canonical (74 files counting subdirectory contents, including the two reclassified-canonical scripts `inspect_tier3_provenance.py` and `merge_globals.py`) and scratch (22 scripts at workspace root). Includes Stage 2 moves-plan, four open items for subsequent stages, and verification section recording both Layer 1 cross-check and Layer 2 sanity scan.

**Path:** `RESTRUCTURE_INVENTORY.md` (workspace root)

**Commit:** `1a68ca6`. Note: the inventory's Stage 2 moves-plan specified `git mv` operations, but the source items were never tracked in git history. Session 12 executed the moves via PowerShell `Move-Item` + `git add`, operationally equivalent to `git mv` for untracked sources. The session 12 operations log records the mechanism deviation; the inventory is preserved as the Stage 0 historical deliverable.

**Amendment to v3 at session 14.** Stage 4 execution surfaced two scope expansions relative to the Stage 0 plan: (i) Group B count corrected from 22 to 23 (`distribute_new_claude_primer.py` was missed by Stage 0 enumeration; matches the Group B `distribute_*` pattern); (ii) post-Stage-0 residue (24 items accumulated between session 8 inventory and session 14) added to Stage 4 quarantine under Mike's in-band arbitration. The Stage 0 categorization itself is preserved unchanged in v3; the amendment is an additive "Stage 4 actual executed scope" section documenting the divergence between Stage 0 plan and Stage 4 execution.

### PRIOR_CYCLE_INVENTORY.md and PRIOR_CYCLE_RECONCILIATION_PLAN.md

One-time task-shaped artifacts produced as deliverables 1 and 2 of STANDING_ITEMS item 9 (prior-cycle canonical material reconciliation). Workspace root placement parallels `RESTRUCTURE_INVENTORY.md`. Finite life — closed out at session 10's reconciliation cluster.

**Paths:** `PRIOR_CYCLE_INVENTORY.md`, `PRIOR_CYCLE_RECONCILIATION_PLAN.md` (workspace root)

**Commits:** session 10 reconciliation commit cluster (`72fcc4c` through `93e6dbb`).

---

## Section 9: Foundational document set

The current document plus its peers in `protocols/foundational/`. Stage 1 documents committed during session 9; session 10 reconciliation cluster added three new documents and updated several existing ones as part of item 9 reconciliation.

| Document | Path | Status |
|----------|------|--------|
| Protocol primer | `protocols\foundational\protocol_primer.md` | committed `79db966` (session 9 pair 1) |
| Standing rules | `protocols\foundational\standing_rules.md` | committed `79db966` (session 9 pair 1); historical lineage section added in session 10 reconciliation cluster |
| Vocabulary quarantine | `protocols\foundational\vocabulary_quarantine.md` | committed `6603799` (session 9 pair 2); eligibility prohibition, source-domain scrubs section, and Open Element 14 cross-reference added in session 10 reconciliation cluster |
| Canonical artifacts index | `protocols\foundational\canonical_artifacts_index.md` | committed `6603799` (session 9 pair 2); updated in session 10 reconciliation cluster; updated in session 12 Stage 2 closure cluster; updated in session 13 Stage 3 closure cluster (added Section 14); updated in session 14 Stage 4 closure cluster; updated 2026-05-25 (added Section 15, cycle records) |
| Current state | `protocols\foundational\current_state.md` | committed `a8bc52c` (session 9 pair 3); Stage-1-complete framing updated in session 10 reconciliation cluster |
| README | `protocols\foundational\README.md` | committed `a8bc52c` (session 9 pair 3) |
| Theoretical context | `protocols\foundational\theoretical_context.md` | committed in session 10 reconciliation cluster |
| Personal context | `protocols\foundational\personal_context.md` | committed in session 10 reconciliation cluster |
| Environment reference | `protocols\foundational\environment_reference.md` | committed in session 10 reconciliation cluster |

Root-level orientation documents (`ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`) and `STANDING_ITEMS.md` were committed during session 9 Stage 1 work; `MANIFEST.md` updated in session 12 Stage 2 closure cluster, session 13 Stage 3 closure cluster, and session 14 Stage 4 closure cluster. `STANDING_ITEMS.md` updated in session 12 (items 2, 3, 8 closed), session 13 (item 4 closed), and session 14 (item 5 closed, item 12 added).

### Foundational document role distinctions (added session 10)

The foundational set decomposes by what each document tracks:

- **Stable theoretical/historical content:** `theoretical_context.md` (Two-paper structure, Four Grand Challenges, Cycle 1/Cycle 2 framework, A3 reference baseline, vocabulary scrub history).
- **Stable operational/environmental content:** `environment_reference.md` (workspace, Python environment, dependencies, PowerShell hazards, tools).
- **Stable personal-context discipline:** `personal_context.md` (Mike's intellectual lineage, contemplative practice, Mokie; discipline of not raising unprompted).
- **Stable protocol content:** `protocol_primer.md`, `standing_rules.md`, `vocabulary_quarantine.md`.
- **Index over stable content:** `canonical_artifacts_index.md` (this document).
- **Session-volatile state:** `current_state.md` (current phase, latest finding, open items, next anticipated work, working pattern, protocol state).

---

## Section 10: Prior-cycle canonical material (added session 10)

This section indexes the directories containing prior-cycle (pre-session-9) canonical material that the session-9 foundational set did not initially engage. Item 9 reconciliation (session 10) inventoried these and made determinations about each; full inventory at `PRIOR_CYCLE_INVENTORY.md`, reconciliation plan at `PRIOR_CYCLE_RECONCILIATION_PLAN.md`.

### protocols\onboarding\

Four prior-cycle primer documents drafted 15 May 2026 for fresh AI partner instantiation: `new_chat_primer.md`, `chatgpt_new_chat_primer.md`, `gemini_new_chat_primer.md`, `chatgpt_routing_note.md`.

**Status:** Superseded by `protocols/foundational/` plus the instantiation kit as cold-start primer surface. The directory has a `README.md` (added session 10) documenting the supersession and explaining what carry-forward content moved where in the session-10 reconciliation.

**Path:** `protocols\onboarding\`

### protocols\architectural_reviews\

See Section 7 above. Architectural review outputs preserved as historical canonical record.

### operations_log\

See Section 7 above. Prior-cycle operations logs (May 14-19) preserved per the honest-record principle.

---

## Section 11: Instantiation kit

The compressed instantiation surface for fresh Claude chats. Becomes a derived/compressed surface over the foundational document set as Stage 1 completes; not authoritative on its own once Stage 1 is committed.

**Current revision:** kit-revision-3 (drafted at session 9 end). Kit-revision-4 is anticipated, incorporating accumulated deferred items from sessions 11, 12, 13, and 14:

From session 11: the "path-space land grab" framing into Rule 7.4 territory; the "any copy-target, not just PS" principle; the "informational content does not need a copy-pane" principle; the v1_1_divergence_review footnote as discipline precedent; handoff-folder attachment discipline (attach contents to opener message rather than reference by path); venv activation in pre-flight verification; PowerShell `-SimpleMatch` literal-vs-alternation semantic; `--no-pager` for diff visibility; working-pattern-discipline-degradation-under-reconstruction observation.

From session 12: paste-back hazard on filenames-in-code-blocks; the (N)-suffix Downloads cleanup discipline; the file-path-in-copy-block unified discipline.

From session 13: pre-flight Downloads cleanup as documented discipline before file delivery (operationalized in session 13's revised-artifacts delivery; absent in session 12's (N)-suffix incident); batched-PS-commands distinction (idempotent file-copy operations safe to batch; state-changing git operations not); Layer 2 sanity-scan-distribution convention clarification (architectural deliverables warrant scan; operational deliverables with in-band Mike arbitration may not).

From session 14: enumerate-don't-pattern-match discipline (move lists built by group-pattern matching against an inventory rather than complete enumeration of working-tree state caused the `distribute_new_claude_primer.py` miss; corrective is direct working-tree enumeration at execution time); `git add -A` scope hazard (sweeps untracked items that may or may not be in commit scope; use explicit paths when scope is non-total); paste-truncation recovery pattern (long batched `Move-Item` commands can exceed PS multi-line copy capacity, leaving PS at `>>` continuation prompt; recovery is Ctrl+C or empty-line Enter, then resending in smaller batches).

Per session 12's Layer-1 working-memory instance, the handoff-folder attachment discipline is operationally demonstrated.

**Path:** typically delivered as a session-handoff artifact under `claude_session_handoffs\YYYY-MM-DD[-N]\` rather than committed to the repository tree. Whether the kit lives at a stable repository path or remains a handoff artifact is a question carrying forward from session 9's pending decisions.

---

## Section 12: Naming-collision and citation discipline

Three documents share the "v1.1" designation:

1. State of the Theory v1.1 (theoretical architecture)
2. Phase 4B Specification v1.1 (analytical procedures)
3. Flight 6 Substrate Specification v1.1 (substrate implementation)

**Citation rule:** Do not cite "v1.1" alone without a qualified document path or full document name. In code comments, citations like `# per v1.1 Section 13.2` are ambiguous; use `# per FSS v1.1 Section 13.2` or `# per Flight 6 Substrate Specification v1.1 §13.2`.

**Reserved target paths.** The three v1.1 documents have target paths reserved here for future restructure work:

- `theory\state_of_theory\state_of_theory_v1_1.md`
- `phase_4b\specifications\phase_4b_specification_v1_1.md`
- `substrate\flight6_v1_1\specifications\flight6_substrate_specification_v1_1.md`

These are reserved targets, not yet executed. The session 12 Stage 2 cluster executed the inventory's six moves and three Group E stagings; the v1.1 document moves are deferred to a future restructure stage to be specified separately. Format considerations (e.g., the FSS v1.1's current `.md.pdf` extension vs. the target `.md` extension) and cross-file reference impact (code comments, operations logs, manuscript references) need scoping before the moves execute. This document updates when those moves land.

---

## Section 13: Workspace and tools

Detailed operational reference for the production environment is in `protocols/foundational/environment_reference.md`. The summary below is for quick lookup.

### Canonical workspace

**Path:** `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` (lowercase nested).

### Stale parallel tree (quarantined session 14)

**Original path:** `C:\Users\vkz244\EE_Theory_Lab\phase_4B\` (capital B at top level).

**Quarantine path:** `archive\scratch\2026-05_pre_restructure\capital_B_parallel_tree\phase_4B\`. The capital-B parallel tree was quarantined at session 14 Stage 4 closure per STANDING_ITEMS item 5 acceptance criterion. `Test-Path` against the original workspace-parent location returns `False` post-move. The tree is preserved in the archive as historical record; not consulted as canonical source for any future work.

### Canonical data outputs

**Path:** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` (absolute; named for inheritance reasons, contains Flight 6 files).

**Note on naming:** rename to reflect Flight 6 contents is tracked as STANDING_ITEMS item 12 (added session 14). See Section 5 above.

### Tools

- **Mesa 3.x + SolaraViz** — ABM substrate environment.
- **VS Code** — text editor, pure-editor mode (AI-agent features unused per protocol convention).
- **PowerShell** — Windows shell. Note: `git --no-pager <command>` bypasses the pager when long output is expected; `q` exits the pager interactively.
- **Node.js / docx npm package** — Word document generation (used selectively for Phil-facing artifacts).
- **ReportLab** — PDF transcripts.
- **Python + NumPy** — analytical work, Tier 3 regression execution.

For Python version, dependency versions, and PowerShell hazards (Notepad UTF-8 BOM, paste-back failure modes, etc.), see `environment_reference.md`.

---

## Section 14: Parquet manifests (added session 13)

Per-file verification and identity record for the canonical substrate data at `flight2_outputs/`. The manifest is a generated artifact (script-driven, not manually maintained) that records each physical parquet file's identity, shadow-copy structure, and FSS §14.1 verification payload. Authority: the canonical record of what each physical parquet file is, how it relates to other physical files via shadow-copy structure, and whether it satisfies substrate-output expectations.

### Manifest schema documentation

**Path:** `phase_4b\manifests\parquet_manifest.md`

**Authority:** canonical schema specification — field names, allowed values, semantics. References FSS v1.1 §14.1 (verification structure), FSS v1.1 §13.2 (shadow-copy structure), and ChatGPT's Q4 recommendation (manifest-now-Git-LFS-later storage philosophy). Synthesizes these into one canonical manifest schema.

**Commit:** introduced at session 13 Stage 3 closure cluster (`fc9d4c4`).

### Manifest CSV

**Path:** `phase_4b\manifests\parquet_manifest.csv`

**Authority:** canonical schema specification (header row) plus one illustrative example row demonstrating field meanings. Per Mike's Q2b arbitration: Stage 3 produces schema specification only; manifest population (running `regenerate_manifest.py` against the eight Flight 6 production parquets) is deferred to Layer 3 routing. The example row uses session-6-verified data for `probe1_overcrowding_20x20` to demonstrate the `genuine + sha256_match + session_6_sha256` combination; placeholder values (`EXAMPLE_64_HEX_SHA256`, `EXAMPLE_FILE_SIZE`, `EXAMPLE_ROW_COUNT`) and `not_available` for `git_head_at_generation` are clearly marked as illustrative. Direct edits to the CSV are prohibited per the maintenance discipline; updates happen via the regenerate script.

**Commit:** introduced at session 13 Stage 3 closure cluster (`fc9d4c4`).

### Regenerate script

**Path:** `phase_4b\scripts\regenerate_manifest.py`

See Section 3 above for the script entry. Scaffolding only at Stage 3 (per Mike's Q2b arbitration); Layer 3 implements the substantive logic. Companion module `_manifest_verification.py` (Layer 3 deliverable) implements the FSS §14.1 check set.

### Verification-record store (reserved path)

**Path:** `phase_4b\manifests\byte_identity_verifications.csv` (path reserved; file not yet created)

**Authority:** record store for SHA-256 byte-identity verification results. Separate from the manifest itself per Mike's arbitration B. Updates to the store happen via a separate verify-byte-identity operation (queued for a future session); subsequent manifest regeneration consults the store to upgrade `shadow_copy_status` from `presumed_shadow_copy` to `verified_shadow_copy`. Distinct from the manifest's `sha256` field, which is computed at every regeneration as the file's identity hash.

### Three distinguishable operations

The manifest discipline involves three operations that should not be conflated:

1. **Manifest regeneration** — `regenerate_manifest.py` reads parquet files at `flight2_outputs/`, computes per-file fields including `sha256`, populates the manifest CSV. Runs whenever parquet outputs change.
2. **Substrate verification** — applies FSS §14.1 checks via `_manifest_verification.py`. Runs as part of manifest regeneration.
3. **Byte-identity verification** — compares SHA-256 hashes across files in a `shadow_copy_group` to upgrade `shadow_copy_status`. Separate from manifest regeneration. Updates the verification-record store; subsequent regeneration reflects the updated record.

See `phase_4b/manifests/parquet_manifest.md` for full discipline detail.

### Layer 2 sanity scan record

Stage 3 schema and scaffolding were drafted by Claude (Layer 1) after Layer 2 (ChatGPT) substantive input on the schema design. The drafted artifacts were routed back to Layer 2 for sanity scan; Layer 2 returned a conditional greenlight with four polish edits, all incorporated in the committed versions:
- `byte_identity_verification_method` clarified as a compact method/result enum
- CSV example placeholder polish (hash-shaped `EXAMPLE_64_HEX_SHA256`; `not_available` for `git_head_at_generation`; explicit illustrative-only marker)
- `sha256` field semantics clarified as distinct from byte-identity verification operation
- `os.PathLike` annotation note added for Layer 3 implementation hazard

Session 13 ops log records the routing cycle.

## Section 15: Cycle records (added 2026-05-25)

Cycle-level closure and current-cycle apparatus. Cycle-internal artifacts are indexed within each cycle's own directory; this section points to the cycle-level authorities and defers to them for internals.

### Cycle 2 closure

**Path:** `cycle2\CYCLE2_CLOSURE.md`

**Authority:** the deliberate Cycle 2 boundary closure (closed 2026-05-24, closure executed 2026-05-25; boundary marker git tag `cycle2-close`). Authoritative for the Cycle 2 closure boundary and for what Cycle 2 produced (why the inherited substrate and the `Psi_local` diagnostic could not carry the manuscript-facing claim).

### Cycle 3 (current)

**Paths:** `cycle3\CYCLE3_OVERVIEW.md` (frame); `cycle3\CYCLE3_TEST_REGISTRY.md` (test index).

**Authority:** the registry is the in-subdirectory authority for Cycle 3 test state — which tests exist and how far up the four-level discipline (L1 implementation / L2 measurement validity / L3 steady-state eligibility / L4 interpretation) each has cleared. Per-test records (`TEST_RECORD_C3-ENV-001.md` passed-L1; `TEST_RECORD_C3-CTL-001.md` valid-L2), the synthetic control-battery apparatus (`c3_ctl_001_battery.py` + `cycle3\data_out\`), the reproduction-environment set (`MESA_ENVIRONMENT_REPRODUCTION.md`, `ENVIRONMENT_SNAPSHOT.md`, `requirements.lock.txt`, `mesa_smoke_test.py`), the held probe-design inputs (`PROBE_DESIGN_INPUTS_HELD.md`), resume anchors, instantiation prompts, and the cross-layer routing archive (`cycle3\routing\`) all live under `cycle3\`; the overview and registry are their index. Closure and gate events are recorded in `operations_log\`.

---

— Originally drafted by Claude as Layer 1 central node, Stage 1 pair-2 of repository restructure, session 9. v2 incorporated Layer 2 review (operational locatability notes added for Mike-local theory files). Session 10 reconciliation cluster added Section 10, updated Section 9, updated Section 11 for kit-revision-4 anticipation, condensed Section 13 with cross-reference to `environment_reference.md`. Session 12 Stage 2 closure cluster updated Sections 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12 to reflect the moves landed at `919db5b` and to soft-update Section 12 per session 12 arbitration. Session 13 Stage 3 closure cluster added Section 14 (parquet manifests), updated Section 3 (added regenerate-manifest scaffolding entry), updated Section 5 (cross-reference to Section 14), updated Section 2 (added FSS §14.1 cross-reference to Section 14), updated Section 7 (added session 12 extended commit and session 13 commit-pending entry), updated Section 11 (kit-revision-4 deferred items grown with session 12 + session 13 additions). Session 14 Stage 4 closure cluster updated Section 5 (replaced "Stage 4 will resolve naming" framing with item 12 cross-reference per Mike's A+C arbitration), Section 7 (added session 13 commit hash `fc9d4c4` and session 14 commit-pending entry; updated Stage 1 routing packages note to reflect quarantine), Section 8 (added v3 amendment note on RESTRUCTURE_INVENTORY), Section 9 (added session 14 to canonical_artifacts_index.md history and STANDING_ITEMS.md history), Section 11 (added session 14 deferred items: enumerate-don't-pattern-match discipline, `git add -A` scope hazard, paste-truncation recovery pattern), Section 13 (updated Stale parallel tree entry to reflect quarantine; added item 12 cross-reference for flight2_outputs naming). Layer 2 sanity scan deferred per Mike's A arbitration at session 14 (Stage 4 closure assessed as operational rather than architectural per the session-13 sanity-scan-distribution convention). The 2026-05-25 Cycle 3 / C3-CTL-001 closure added Section 15 (cycle records) and updated the maintenance-discipline note and the Section 9 changelog row.
