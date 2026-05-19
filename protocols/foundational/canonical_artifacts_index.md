# Canonical Artifacts Index

**Document role.** Authoritative index of the canonical artifacts that constitute the EE Theory Lab record. For each artifact, the index specifies: what it is, where it lives, and what authority it carries. This is the document a fresh Claude instance consults to locate primary source for any verification under Rule 1.

**Authority.** This document is authoritative for *where* canonical artifacts live and *what authority* they carry. It is not authoritative for the artifacts' content; each artifact is its own authority on its content domain. When this index conflicts with primary source (the actual files at the stated paths), primary source wins and this document revises.

**Maintenance discipline.** Updated when canonical artifacts are added, moved, or superseded. Updates committed alongside the operations log of the session in which the change occurred. Stage 2 of the repository restructure (moves canonical artifacts via `git mv`) will trigger a coordinated update of this index.

**Path conventions.** All paths relative to `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` unless absolute. PowerShell uses backslash separators; git status output uses forward slashes; both refer to the same files.

**Relationship to other foundational documents.**
- `protocol_primer.md` specifies who uses these artifacts and how.
- `standing_rules.md` specifies the disciplines (especially Rule 1) under which artifacts are consulted.
- `vocabulary_quarantine.md` specifies the language used when discussing the artifacts.

---

## Section 1: Theory-level documents

### State of the Theory v1.1

The committed theoretical architecture; ten sections; "hard core." Authority: formal theoretical commitments. Defines the four open elements (μ(ρ), F(v,c,r), Q, nucleation mechanism), the two-stage Landau cascade structure, the critical ontological constraint (ACTION not decision), and the architecture's exclusionary clauses.

**Path:** Mike's local file (not in the repository's tracked tree as of session 9).

**Operational locatability:** requires Mike-provided attachment for any verification-against-primary-source check. Stage 2 will move this to `theory\state_of_theory\state_of_theory_v1_1.md` per session 6's v1.1 naming-collision resolution; until then, Layer 1 cannot verify content claims about this document without explicit Mike-provided access.

**Citation:** "State of the Theory v1.1." Do not cite "v1.1" alone without qualifier — multiple v1.1 documents exist (see naming-collision note below).

### State of the Theory v1.5 Overview

Manuscript foundation Phil writes from; v1.4 MFA underneath. Authority: manuscript-facing material. The leading edge of the team's worked-out positions has moved past v1.5 in places (e.g., the flagged "modest-resources-outperform-abundant" passage); v1.5 absorbs back-flow from those developments as Phil revises.

**Path:** Mike's local file (not in the repository's tracked tree as of session 9).

**Operational locatability:** requires Mike-provided attachment for verification. No committed Stage 2 target yet; the v1.5 Overview's repository placement is a question for Mike to arbitrate when manuscript work surfaces a need.

**Citation:** "State of the Theory v1.5 Overview" or "v1.5 Overview" with context.

---

## Section 2: Phase 4B specifications

### Phase 4B Specification v1.1

Analytical procedures for Phase 4B: Tier 1 strict matching, Tier 2 coarser matching, Tier 3 interpretable regression with pre-specified interaction families, two-field empirical_result × structural_status classification, cross-scale analysis. Authority: Phase 4B analytical procedures.

**Path:** `phase_4b\phase_4b_specification_v1.1.md`

**Verified:** session 9.

**Citation:** "Phase 4B Specification v1.1."

### Flight 6 Substrate Specification v1.1

Substrate implementation: the cellular engine that produces .parquet telemetry. Sections 6 and 8 specify the deterministic probability chain (Drive_Raw → p_base → p_act → realization) that reg_01 recovered. Section 13.2 specifies the shadow-copy structure (F_2_symmetric runs at each scale produce one underlying parquet file, three probe-named files via byte-identical shadow copies; F_LR runs produce one parquet file each). Section 15 enumerates implementation prohibitions; the protocol-applicable subset is lifted to `standing_rules.md` Rule 7.

Authority: substrate implementation.

**Path:** `flights\flight_6\Flight6_Substrate_Specification_v1.1.md.pdf`

**Verified:** session 6 (located and read end-to-end), session 9 (path re-verified, Section 15 re-verified against primary source).

**Citation:** "Flight 6 Substrate Specification v1.1" or "FSS v1.1" with context.

---

## Section 3: Tier 3 canonical implementation

The Tier 3 implementation cluster committed at `3189ab7` (session 7 reconciliation). All paths under `phase_4b\scripts\`.

### Intake module

Implements the seven-item structural-correctness checklist per intake specification. Defines `NormalizedPrereg` dataclass, the schema validator, and the `attach_tier2_globals` merge function.

**Path:** `phase_4b\scripts\_phase_4b_intake.py`

**Commit:** introduced at `3189ab7`.

### Test suite

Demonstrates all five exception types fire on deliberate violations. Routes inputs through the actual validation pipeline (not via mock objects per Rule 7.2).

**Path:** `phase_4b\scripts\test_intake.py`

**Commit:** introduced at `3189ab7`.

### Refactored regression consumer

Contract-mediated per intake §1.6. Reads pre-registration yaml, normalizes via the intake module, attaches Tier 2 globals, executes the regression, writes outputs.

**Path:** `phase_4b\scripts\tier3_regression.py`

**Commit:** introduced at `3189ab7`.

---

## Section 4: reg_01 pre-registration and outputs

The committed reg_01 cluster. Pre-registration and outputs committed at `3189ab7`. The pre-registration's `interpretation_boundary` content was restored from session 5's log to the canonical yaml during session 7's reconciliation.

### Pre-registration

Schema is contract-mediated intake format. `derived_variables` block declares per-run/tick constructions for `Local_Density_squared`, `rho_global`, `psi_global`. `interpretation_boundary.licenses` list (5 items) and `does_not_adjudicate` (4 items) restored under new schema; substantive scope matches session 5's log.

**Path:** `phase_4b\pre_registrations\reg_01_scale_interactions.yaml`

**Commit:** `3189ab7`.

### Primary coefficients

**Path:** `phase_4b\tier3_outputs\coefs_reg_01_scale_interactions.csv`

**Commit:** `3189ab7`.

### Sensitivity coefficients

**Path:** `phase_4b\tier3_outputs\coefs_reg_01_scale_interactions_sensitivity_cell.csv`

**Commit:** `3189ab7`.

### Regression report

**Path:** `phase_4b\tier3_outputs\report_reg_01_scale_interactions.md`

**Commit:** `3189ab7`.

**Note:** the `tier3_outputs/` directory is at `phase_4b\tier3_outputs\` (sibling of `scripts/`), NOT `phase_4b\scripts\tier3_outputs\`. The kit-revision-1 had this wrong; corrected in kit-revision-2 and verified during session 7.

---

## Section 5: Substrate data and Tier 2 derived outputs

### Canonical substrate data

Eight Flight 6 production parquet files (Flight 2 naming inheritance preserved). Four genuine substrate runs plus four byte-identical shadow copies per Flight 6 Substrate Specification §13.2. PRNG_seed 128561948, substrate_version v1.1.

**Path (absolute):** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\`

**Note on naming:** the directory is named `flight2_outputs` for inheritance reasons, but contains Flight 6 files. The mismatch is documented at the canonical record level (here) and will be resolved during Stage 4 (quarantine and rename).

### Tier 2 derived outputs

65 files. Per-probe-scale derived outputs (8 metric types × 8 probe-scale combinations = 64 files) plus the merged `global_timeseries.csv` bridging artifact (13.5MB, the canonical Tier 2 → Tier 3 join surface produced by `merge_globals.py`; status confirmed canonical during session 8's Stage 0 inventory).

**Path:** `phase_4b\tier2_outputs\`

### Tier 1 reports

Eight Tier 1 reports across the four-probe × two-scale matrix.

**Path:** `phase_4b\tier1_reports\`

### Cross-run analysis outputs

Three cross-run analysis files dated 5/17/2026 morning.

**Path:** `phase_4b\cross_run_outputs\`

**Stage 0 status:** these three directories (`tier2_outputs/`, `tier1_reports/`, `cross_run_outputs/`) are categorized as canonical in `RESTRUCTURE_INVENTORY.md` (committed at `1a68ca6`); Stage 2 will execute `git mv` placement per the inventory's moves-plan.

---

## Section 6: Diagnostic and forensic-text outputs

Per the Stage 0 canonical diagnostics directory convention (adopted session 8), all diagnostic stdout, log, and forensic-text outputs go under `phase_4b/diagnostics/`. Stage 2 will execute the moves; current locations as committed in `RESTRUCTURE_INVENTORY.md`:

### Session 5 diagnostic stdout

**Path:** `phase_4b\diagnostic_stdout.txt`

**Note:** at `phase_4b\` (sibling of `scripts\`), NOT `phase_4b\scripts\diagnostic_stdout.txt`. The kit-revision-1 had this wrong; corrected in kit-revision-2.

### Session 6 t27 forensic output

**Path:** `phase_4b\t27_diagnostic_stdout.txt`

### Earlier cross-run comparison output

**Path:** `cross_run_comparisons_df9122e.txt` (workspace root, awaiting Stage 2 move to `phase_4b/diagnostics/`)

---

## Section 7: Operations logs and routing artifacts

### Operations logs

All committed. Paths under `operations_log\`:

| Session | Path | Commit |
|---------|------|--------|
| 1–4 | `operations_log\` (older naming) | various commits up to `5d91828` |
| 5 | `operations_log\2026-05-18_phase_4b_session_5.md` | `3189ab7` |
| 6 | `operations_log\2026-05-19_phase_4b_session_6.md` | `3189ab7` |
| 7 | `operations_log\2026-05-19_phase_4b_session_7.md` | `4e66f27` |
| 8 | `operations_log\2026-05-19_phase_4b_session_8.md` | `3e38980` |
| 9 | (pending; drafted at session-end) | (pending commit) |

### Layer 1 routing package (session 5)

The `LAYER_1_ROUTING_PACKAGE.txt` file at workspace root is a canonical-record candidate (from session 5's Layer 2 routing on reg_01 interpretation). Stage 2 will place it under an appropriate routing-archive path per `RESTRUCTURE_INVENTORY.md`.

### Stage 1 routing packages (session 9)

**Path (pre-Stage-2):** `LAYER_2_ROUTING_STAGE1_PAIR1.md`, `LAYER_2_ROUTING_STAGE1_PAIR1_V2_ACCEPTANCE.md` at workspace root.

These will move to a routing-archive path during Stage 2 alongside the session 5 routing package.

---

## Section 8: Stage 0 inventory and restructure planning

### RESTRUCTURE_INVENTORY.md

The Stage 0 deliverable. Categorizes the 31 untracked items as of session 8 inventory time into canonical (74 files counting subdirectory contents, including the two reclassified-canonical scripts `inspect_tier3_provenance.py` and `merge_globals.py`) and scratch (22 scripts at workspace root). Includes Stage 2 moves-plan, four open items for subsequent stages, and verification section recording both Layer 1 cross-check and Layer 2 sanity scan.

**Path:** `RESTRUCTURE_INVENTORY.md` (workspace root)

**Commit:** `1a68ca6`.

---

## Section 9: Foundational document set

The current document plus its peers in `protocols/foundational/`. Committed in Stage 1 of the restructure.

| Document | Path | Status |
|----------|------|--------|
| Protocol primer | `protocols\foundational\protocol_primer.md` | committed `79db966` |
| Standing rules | `protocols\foundational\standing_rules.md` | committed `79db966` |
| Vocabulary quarantine | `protocols\foundational\vocabulary_quarantine.md` | (this commit pending) |
| Canonical artifacts index | `protocols\foundational\canonical_artifacts_index.md` | (this commit pending) |
| Current state | `protocols\foundational\current_state.md` | (pending later Stage 1 work) |
| README | `protocols\foundational\README.md` | (pending later Stage 1 work) |

Root-level orientation documents (`ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`) and `STANDING_ITEMS.md` are also pending later Stage 1 work.

---

## Section 10: Instantiation kit

The compressed instantiation surface for fresh Claude chats. Becomes a derived/compressed surface over the foundational document set as Stage 1 completes; not authoritative on its own once Stage 1 is committed.

**Current revision:** kit-revision-2 (drafted at session 7 end). kit-revision-3 is pending Stage 1 work and will absorb the eleven kit-improvement items accumulated across sessions 7-9.

**Path:** typically delivered as a session-handoff artifact under `claude_session_handoffs\YYYY-MM-DD[-N]\` rather than committed to the repository tree. Whether the kit lives at a stable repository path or remains a handoff artifact is a question for kit-revision-3 to resolve.

---

## Section 11: Naming-collision and citation discipline

Three documents share the "v1.1" designation:

1. State of the Theory v1.1 (theoretical architecture)
2. Phase 4B Specification v1.1 (analytical procedures)
3. Flight 6 Substrate Specification v1.1 (substrate implementation)

**Citation rule:** Do not cite "v1.1" alone without a qualified document path or full document name. In code comments, citations like `# per v1.1 Section 13.2` are ambiguous; use `# per FSS v1.1 Section 13.2` or `# per Flight 6 Substrate Specification v1.1 §13.2`.

**The post-Stage-2 path commitment:** the three v1.1 documents will live at:

- `theory\state_of_theory\state_of_theory_v1_1.md`
- `phase_4b\specifications\phase_4b_specification_v1_1.md`
- `substrate\flight6_v1_1\specifications\flight6_substrate_specification_v1_1.md`

These are the targets; Stage 2 executes the moves. This document updates accordingly when Stage 2 commits.

---

## Section 12: Workspace and tools

### Canonical workspace

**Path:** `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` (lowercase nested).

### Stale parallel tree

**Path:** `C:\Users\vkz244\EE_Theory_Lab\phase_4B\` (capital B at top level). To be archived during Stage 4.

### Canonical data outputs

**Path:** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` (absolute; named for inheritance reasons, contains Flight 6 files; Stage 4 will resolve the naming).

### Tools

- **Mesa 3.x + SolaraViz** — ABM substrate environment.
- **VS Code** — text editor, pure-editor mode (AI-agent features unused per protocol convention).
- **PowerShell** — Windows shell. Note: `git --no-pager <command>` bypasses the pager when long output is expected; `q` exits the pager interactively.
- **Node.js / docx npm package** — Word document generation (used selectively for Phil-facing artifacts).
- **ReportLab** — PDF transcripts.
- **Python + NumPy** — analytical work, Tier 3 regression execution.

---

— Drafted by Claude as Layer 1 central node, Stage 1 pair-2 of repository restructure, session 9. v2 incorporates Layer 2 review (operational locatability notes added for Mike-local theory files). Pending Layer 2 acceptance of v2 before commit per `protocol_primer.md` Section 3's protocol-infrastructure routing convention.
