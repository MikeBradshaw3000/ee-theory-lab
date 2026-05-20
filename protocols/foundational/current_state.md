# Current State

**Document role.** Snapshot of the EE Theory Lab's current phase, latest substantive findings, open items, and next anticipated work. This is the document a fresh Claude instance consults to answer "where are we now?"

**Authority.** This document is authoritative for current-state orientation. When it conflicts with primary source (committed code, operations logs, the actual repository state), primary source wins and this document revises. Per Rule 1, current-state claims should be verified against `git log --oneline` and operational reality before being treated as load-bearing.

**Maintenance discipline.** Updated at session end. Volatile sections (those marked **As of session N**) are rewritten each session; stable structural content (the section headings, what each section tracks) changes only when the protocol's understanding of what's worth tracking evolves.

**Relationship to root-level `CURRENT_STATE.md`.** This document is the foundational-set version, scoped to load-bearing protocol-state material for AI instances and Mike. The root-level `CURRENT_STATE.md` is a higher-level orientation derivative aimed at the same audience but with broader scope (project-level state including manuscript-side context that is not strictly Phase 4B work).

**Relationship to other foundational documents.** This document tracks session-volatile state. For stable theoretical and historical content (Two-paper structure, Four Grand Challenges, Cycle 1/Cycle 2 framework, A3 reference baseline), see `theoretical_context.md`. For operational/environmental detail (workspace paths, Python environment, dependencies, PowerShell hazards), see `environment_reference.md`. For personal-context discipline, see `personal_context.md`. The foundational set's role distinctions are documented at `canonical_artifacts_index.md` Section 9.

---

## Section 1: Current phase

**As of session 10 (2026-05-20):**

The project is in the middle of a multi-stage repository restructure, committed across sessions 6-8 of Phase 4B. Stage 0 (freeze and inventory) was committed at `1a68ca6` during session 8. Stage 1 (add orientation spine — the foundational document set, root-level orientation documents, kit revision) was substantively completed in session 9 with the foundational set, root-level orientation, STANDING_ITEMS.md, and kit-revision-3 committed. Stage 1 closed in session 10 *after the prior-cycle reconciliation* (item 9 of STANDING_ITEMS), which surfaced pre-existing canonical material at `protocols/onboarding/`, `protocols/architectural_reviews/`, and `operations_log/` that the session-9 foundational set had not initially engaged.

**Stage 1 status: Complete after reconciliation.** The session-9 closing framing of "Stage 1 substantively complete" is corrected to "Stage 1 substantively complete *after the discovered reconciliation requirement*." The reconciliation work fired in session 10 per item 9's structural trigger.

Stage sequence (committed session 6):

- **Stage 0** — Freeze and inventory. **Committed at `1a68ca6`.**
- **Stage 1** — Add orientation spine. **Complete after reconciliation (sessions 9-10).**
- **Stage 2** — Move unambiguous canonical artifacts via `git mv`. **Next.**
- **Stage 3** — Add manifests, especially for parquet outputs and substrate files.
- **Stage 4** — Quarantine stale and scratch material.
- **Stage 5** — Resume Phase 4B analytical work.

---

## Section 2: Latest substantive finding

**As of session 10 (2026-05-20):**

The most recent substantive analytical finding is from session 6: Tier 3 reg_01 is substantively complete as a pipeline-validation regression, with the R²=1.000 identity-recovery interpretation verified by primary-source review of the Flight 6 Substrate Specification v1.1 sections 6 and 8. The substrate's deterministic probability chain (Drive_Raw → p_base → p_act → realization) is what reg_01 recovered at machine precision; F_variant and scale enter only indirectly through Term_Lambda.

The reg_01 finding does not adjudicate the architectural selection between F_LR and F_2_symmetric for the functional form of F(v,c,r). F-form adjudication routes to macro-level analyses for the next analytical phase: aggregate trajectory comparisons, Ψ-structure analysis, Q-driven base drift, regime-transition timing, repeat-seed designs.

No analytical work has happened since session 6. Sessions 7-10 have been protocol infrastructure (reconciliation, Stage 0 inventory, Stage 1 foundational set drafting and prior-cycle reconciliation).

---

## Section 3: Open items

**As of session 10 (2026-05-20):**

### Post-Stage-1 standing items (now eligible after item 9 closes)

- **Pre-registration reproducibility verification.** Re-run `tier3_regression.py` against the committed yaml at `3189ab7`; diff outputs against committed reg_01 outputs. Eligible to fire as the first substantive action of session 11 (or later session 10 work if context budget permits).
- **Push to origin.** Local main is multiple commits ahead of origin/main after the session-10 reconciliation commit cluster. Eligible to fire post-cluster.

### Post-restructure standing items

- **Next analytical phase decision.** Which macro-level F-form adjudication route becomes the next pre-registered work. Mike arbitrates. Deferred until restructure complete enough to support analytical work.

### Cross-session items

- **Manuscript implications.** Phil's manuscript work is independent of Phase 4B's analytical phase. Whether and when the reg_01 finding lands in the v1.5 Overview is Phil's call. No action item from the protocol side.
- **F multiplicativity commitment verification.** Independent trigger (v1.5 Overview revision work surfaces). See `STANDING_ITEMS.md`.
- **Foundational set maintenance.** Each session-end checks for kit-revision triggers (working-pattern changes, current-state changes, canonical-artifacts changes). Rule 2 specifies the discipline.
- **Kit-revision-4.** Anticipated post-item-9 closure work. See `STANDING_ITEMS.md` and `canonical_artifacts_index.md` Section 11 for the items kit-revision-4 incorporates.
- **ChatGPT and Gemini onboarding under session-9 framework.** The session-9 foundational set is Claude-focused; ChatGPT and Gemini onboarding under the current framework was deferred during item 9 reconciliation. See `STANDING_ITEMS.md` for the open item.

All active deferred items live in `STANDING_ITEMS.md` with explicit trigger conditions and acceptance criteria.

---

## Section 4: Next anticipated work

**As of session 10 (2026-05-20):**

Within this session (session 10):

- Item 9 reconciliation: three deliverables (inventory, plan, canonical record update). Inventory and plan committed. Canonical record update commit cluster is the final session-10 substantive work item.
- Layer 2 sanity scan of the deliverable-3 file set per the foundational-set discipline.
- Session 10 operations log.
- Session 11 handoff folder.

Next session (session 11):

- Pre-registration reproducibility verification (per STANDING_ITEMS item 1).
- Push to origin (per STANDING_ITEMS item 2).
- Stage 2 execution: `git mv` operations per `RESTRUCTURE_INVENTORY.md` moves-plan.

Several sessions out:

- Stages 3-4 (manifests; quarantine).
- Stage 5 resumption: next analytical phase decision and pre-registration.
- ABM probe execution by Layer 3 (Gemini) once probe is specified.
- Substantive results analysis with Layer 2 (ChatGPT), likely from a fresh Claude session that has the committed substrate and analytical outputs as primary source.

---

## Section 5: Working-pattern state

**As of session 10 (2026-05-20):**

Working pattern committed in the kit as of kit-revision-3, with additions surfaced during session 10 that fold into kit-revision-4. Operational pattern:

- PowerShell commands delivered one per fenced block; Mike pastes one-click, runs, pastes output back.
- One-click copy panes used only for content Mike will act on (PS commands, messages to other AIs, file content for placement). Informational content (status summaries, file lists, instructions about what to do next) goes in plain text.
- Visual demarcation after PS output: horizontal rule + bold "Response to your output:" label.
- File edits delivered as full-file overwrites; Mike downloads, moves into workspace via PS.
- File-system manipulation defaults to PowerShell (not File Explorer drag).
- Multi-file `present_files` delivery: Mike prefers separate-file downloads; Claude makes separate `present_files` calls.
- For substantial multi-file reads, concatenation-via-PowerShell into a single bundle file for one upload is preferred to many separate uploads.
- Session-handoff folder: `claude_session_handoffs/YYYY-MM-DD[-N]/` contains the kit and the just-closed session's operations log.
- Opening instruction to next-session Claude is a single sentence pointing at the kit; substantive operational knowledge belongs inside the kit.
- Session-open verification (added session 10): `git ls-tree HEAD -- <relevant directories>` for any directory where session work will produce new canonical material, regardless of whether the directory appears in the prior session's resume anchor. Path-space land-grab discipline.

---

## Section 6: Protocol state

**As of session 10 (2026-05-20):**

- HEAD: `5f5a762` (session 9 date-revert commit) at session 10 open; advances through the session-10 reconciliation commit cluster.
- Layer assignments: Claude = Layer 1 (central node), ChatGPT = Layer 2 (substantive review), Gemini = Layer 3 (implementation/execution). Mike arbitrates.
- Foundational document set: pairs 1-3 committed during session 9; three new documents (`theoretical_context.md`, `personal_context.md`, `environment_reference.md`) and updates to existing documents committed during session 10 as part of item 9 reconciliation.
- Instantiation kit: kit-revision-3 (drafted at session 9 end). Kit-revision-4 anticipated post-item-9 closure.
- Routing convention: full Layer 2 cycle for protocol-infrastructure routings includes v2-acceptance pass before commit (per `protocol_primer.md` Section 3); other full-cycle routings commit after Layer 1 incorporation. Session 10 deliverable 3 routes for Layer 2 sanity scan per the discipline-distribution convention (substantive foundational updates get Layer 2 review, but not full v2-acceptance cycle).

---

## Section 7: How to update this document at session end

The volatile sections are 1-6 above. Each session-end update should:

1. Update **Section 1** if the current phase has changed (a stage closed or opened).
2. Update **Section 2** if a new substantive finding has landed in the canonical record.
3. Update **Section 3** by removing resolved open items, adding new ones, and updating session-numbered triggers and acceptance criteria where relevant.
4. Update **Section 4** to reflect new next-anticipated work.
5. Update **Section 5** if the working pattern has evolved (new conventions, retired conventions).
6. Update **Section 6** with new HEAD, new commits ahead of origin, new kit revision number, etc.

The **As of session N** marker at the top of each volatile section gets the new session number. The structural content (section headings, what each section tracks) is stable and changes only when the protocol's tracking discipline evolves.

---

— Drafted by Claude as Layer 1 central node, Stage 1 pair-3 of repository restructure, session 9. v2 incorporates Layer 2 review (Open Element 14 label removed and restated in committed terms; completed Section 15 lift item removed from open items; "confirmed" replaced with "verified by primary-source review"). Stage-1 framing updated, cross-references to new foundational documents added, session 10 substantive work reflected, session 10 as deliverable 3 of item 9 reconciliation. Pending Layer 2 sanity scan before commit.
