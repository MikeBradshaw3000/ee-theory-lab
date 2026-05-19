# Current State

**Document role.** Snapshot of the EE Theory Lab's current phase, latest substantive findings, open items, and next anticipated work. This is the document a fresh Claude instance consults to answer "where are we now?"

**Authority.** This document is authoritative for current-state orientation. When it conflicts with primary source (committed code, operations logs, the actual repository state), primary source wins and this document revises. Per Rule 1, current-state claims should be verified against `git log --oneline` and operational reality before being treated as load-bearing.

**Maintenance discipline.** Updated at session end. Volatile sections (those marked **As of session N**) are rewritten each session; stable structural content (the section headings, what each section tracks) changes only when the protocol's understanding of what's worth tracking evolves.

**Relationship to root-level `CURRENT_STATE.md`.** This document is the foundational-set version, scoped to load-bearing protocol-state material for AI instances and Mike. The root-level `CURRENT_STATE.md` is a higher-level orientation derivative aimed at the same audience but with broader scope (project-level state including manuscript-side context that is not strictly Phase 4B work).

---

## Section 1: Current phase

**As of session 9 (2026-05-20):**

The project is in the middle of a multi-stage repository restructure, committed across sessions 6-8 of Phase 4B. Stage 0 (freeze and inventory) was committed at `1a68ca6` during session 8. Stage 1 (add orientation spine — the foundational document set, root-level orientation documents, kit revision) is the current stage and is being executed during session 9.

Stage sequence (committed session 6):

- **Stage 0** — Freeze and inventory. **Committed at `1a68ca6`.**
- **Stage 1** — Add orientation spine. **In progress, session 9.**
- **Stage 2** — Move unambiguous canonical artifacts via `git mv`.
- **Stage 3** — Add manifests, especially for parquet outputs and substrate files.
- **Stage 4** — Quarantine stale and scratch material.
- **Stage 5** — Resume Phase 4B analytical work.

---

## Section 2: Latest substantive finding

**As of session 9 (2026-05-20):**

The most recent substantive analytical finding is from session 6: Tier 3 reg_01 is substantively complete as a pipeline-validation regression, with the R²=1.000 identity-recovery interpretation verified by primary-source review of the Flight 6 Substrate Specification v1.1 sections 6 and 8. The substrate's deterministic probability chain (Drive_Raw → p_base → p_act → realization) is what reg_01 recovered at machine precision; F_variant and scale enter only indirectly through Term_Lambda.

The reg_01 finding does not adjudicate the architectural selection between F_LR and F_2_symmetric for the functional form of F(v,c,r). F-form adjudication routes to macro-level analyses for the next analytical phase: aggregate trajectory comparisons, Ψ-structure analysis, Q-driven base drift, regime-transition timing, repeat-seed designs.

No analytical work has happened since session 6. Sessions 7-9 have been protocol infrastructure (reconciliation, Stage 0 inventory, Stage 1 foundational set drafting).

---

## Section 3: Open items

**As of session 9 (2026-05-20):**

### Stage 1 remaining (this session's work)

- Pair 3: `current_state.md` (this document) and `README.md` for the foundational set.
- Root-level orientation documents: `ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`.
- `STANDING_ITEMS.md` (deferred-items tracker per the bullet-proof deferral process).
- Kit-revision-3 (incorporates eleven kit-improvement items accumulated across sessions 7-9).

### Post-Stage-1 standing items

- **Pre-registration reproducibility verification.** Re-run `tier3_regression.py` against the committed yaml at `3189ab7`; diff outputs against committed reg_01 outputs. Trigger: first action of the session immediately following Stage 1 completion. Acceptance: diff output committed to operations log.
- **Push to origin.** Local main several commits ahead of origin/main. Trigger: post-Stage-1 natural commit cluster. Acceptance: `git push` reports success and `git log` confirms parity with `origin/main`.

### Post-restructure standing items

- **Next analytical phase decision.** Which macro-level F-form adjudication route (aggregate trajectory, Ψ-structure, Q-drift, regime-transition timing, repeat-seed) becomes the next pre-registered work. Mike arbitrates. Deferred until restructure complete enough to support analytical work.

### Cross-session items

- **Manuscript implications.** Phil's manuscript work is independent of Phase 4B's analytical phase. Whether and when the reg_01 finding lands in the v1.5 Overview is Phil's call. No action item from the protocol side.
- **Foundational set maintenance.** Each session-end checks for kit-revision triggers (working-pattern changes, current-state changes, canonical-artifacts changes). Rule 2 specifies the discipline.

---

## Section 4: Next anticipated work

**As of session 9 (2026-05-20):**

Within this session:

- Complete pair-3 (current_state + README) with Layer 2 full cycle.
- Root-level orientation documents (likely Layer 2 sanity scan rather than full cycle).
- `STANDING_ITEMS.md` (no Layer 2 routing — operational process artifact).
- Kit-revision-3 (likely Layer 2 sanity scan).
- Session 9 operations log.
- Session 10 handoff folder.

Next session (session 10):

- First action: pre-registration reproducibility verification per the trigger condition.
- Stage 2 execution: `git mv` operations per `RESTRUCTURE_INVENTORY.md` moves-plan.
- Push to origin if commit cluster is at a natural point.

Several sessions out:

- Stages 3-4 (manifests; quarantine).
- Stage 5 resumption: next analytical phase decision and pre-registration.
- ABM probe execution by Layer 3 (Gemini) once probe is specified.
- Substantive results analysis with Layer 2 (ChatGPT), likely from a fresh Claude session that has the committed substrate and analytical outputs as primary source.

---

## Section 5: Working-pattern state

**As of session 9 (2026-05-20):**

Working pattern committed in the kit as of kit-revision-2 plus additions surfaced during sessions 7-9. Kit-revision-3 will absorb the surfaced additions. Operational pattern:

- PowerShell commands delivered one per fenced block; Mike pastes one-click, runs, pastes output back.
- Visual demarcation after PS output: horizontal rule + bold "Response to your output:" label.
- File edits delivered as full-file overwrites; Mike downloads, moves into workspace via PS.
- File-system manipulation defaults to PowerShell (not File Explorer drag).
- Multi-file `present_files` delivery: Mike prefers separate-file downloads; Claude makes separate `present_files` calls.
- Session-handoff folder: `claude_session_handoffs/YYYY-MM-DD[-N]/` contains the kit and the just-closed session's operations log.
- Opening instruction to next-session Claude is a single sentence pointing at the kit; substantive operational knowledge belongs inside the kit.

---

## Section 6: Protocol state

**As of session 9 (2026-05-20):**

- HEAD: `6603799` (pair-2 commit). Local main 5 commits ahead of origin/main.
- Layer assignments: Claude = Layer 1 (central node), ChatGPT = Layer 2 (substantive review), Gemini = Layer 3 (implementation/execution). Mike arbitrates.
- Foundational document set: pairs 1 and 2 committed; pair 3 (current_state + README) in progress.
- Instantiation kit: kit-revision-2 (drafted at session 7 end); kit-revision-3 pending Stage 1 completion.
- Routing convention: full Layer 2 cycle for protocol-infrastructure routings includes v2-acceptance pass before commit (per `protocol_primer.md` Section 3); other full-cycle routings commit after Layer 1 incorporation.

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

— Drafted by Claude as Layer 1 central node, Stage 1 pair-3 of repository restructure, session 9. v2 incorporates Layer 2 review (Open Element 14 label removed and restated in committed terms; completed Section 15 lift item removed from open items; "confirmed" replaced with "verified by primary-source review"). Pending Layer 2 acceptance of v2 before commit per `protocol_primer.md` Section 3's protocol-infrastructure routing convention.
