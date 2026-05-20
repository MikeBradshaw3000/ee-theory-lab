# STANDING_ITEMS

**Document role.** Deferred-items tracker. Operational process artifact for items whose execution is deferred to a specific future condition. Consulted at each session open per the kit's resume-anchor discipline: a fresh Claude checks STANDING_ITEMS.md for items whose trigger conditions are met by current HEAD/working-tree state.

**Authority.** Authoritative for what is deferred and what triggers each item. Not authoritative for the items' substantive content (the operations logs, foundational current_state.md, RESTRUCTURE_INVENTORY.md remain the substantive sources). When this document's trigger condition for an item is met but the item's substantive content has evolved, the substantive sources win.

**Maintenance discipline.**
- Items added when a deferral is committed (typically in an operations log or in-session arbitration by Mike).
- Items removed when their acceptance criterion is met; the removal is committed alongside the operations log of the session in which the item executed.
- The format of each entry is fixed: **what** (the action), **trigger** (the condition under which it executes), **acceptance** (what counts as done).
- Stage-transition items have triggers expressed in terms of the preceding stage's completion, making the stage sequence operationally enforced by this document.

**Relationship to other documents.**
- `protocols/foundational/current_state.md` Section 3 names the open items at the high level; STANDING_ITEMS.md is the operational tracker with explicit trigger and acceptance criteria.
- The kit's resume anchor (kit-revision-3 onward) references this document by path; the check at session open is structural.
- `RESTRUCTURE_INVENTORY.md` is the moves-plan that Stage 2 executes against; the moves-plan is the substantive content, this document tracks the stage as one item.

---

## Items

### 2. Push to origin

**What.** `git push` to send the local main commits to `origin/main`.

**Trigger.** Post-Stage-1 natural commit cluster. Stage 1 is complete when all foundational documents, root-level orientation documents, STANDING_ITEMS.md, kit-revision-3, the session 9 operations log, and the session 10 reconciliation commit cluster are committed. Push fires once the cluster is closed; sequencing relative to the pre-registration reproducibility verification (item 1) is at Mike's arbitration.

**Acceptance.** `git push` reports success; `git log` confirms parity with `origin/main` (HEAD on local main matches HEAD on origin/main).

---

### 3. Stage 2 execution — canonical artifact moves

**What.** Execute the `git mv` operations specified in `RESTRUCTURE_INVENTORY.md` moves-plan. Moves include: Phase 4B specification and Flight 6 substrate specification to qualified-path locations (per `protocols/foundational/canonical_artifacts_index.md` Section 12); diagnostic stdout files to `phase_4b/diagnostics/`; Tier 2, Tier 1, cross-run output directories from untracked to canonical placement; routing artifacts to routing-archive path; reclassified canonical scripts (`inspect_tier3_provenance.py`, `merge_globals.py`) to `phase_4b/scripts/`.

**Trigger.** Stage 1 complete (all items in Stage 1 closed) AND item 1 (pre-registration reproducibility verification) executed. The dependency on item 1 is per its trigger note: verification before further restructure work.

**Acceptance.** All moves-plan items executed via `git mv`; commit cluster references `RESTRUCTURE_INVENTORY.md` items; `canonical_artifacts_index.md` updated to reflect new paths; `MANIFEST.md` updated to remove "pending Stage 2" markers; this STANDING_ITEMS.md entry closes.

---

### 4. Stage 3 execution — manifests for parquet outputs

**What.** Add manifests for parquet outputs (the eight Flight 6 production files in `flight2_outputs/`) and substrate files. Manifest format combines ChatGPT's Q4 recommendation with Flight 6 Substrate Specification Section 14.1's verification structure — one canonical manifest schema serving both purposes. Located at `phase_4b/outputs/parquet_manifest.csv` with documentation at `phase_4b/outputs/parquet_manifest.md` (or equivalent locations per Stage 2 placement).

**Trigger.** Stage 2 (item 3) complete.

**Acceptance.** Manifests committed at the specified locations; manifest content covers all eight production parquet files; `canonical_artifacts_index.md` updated to reflect manifest locations and authority.

---

### 5. Stage 4 execution — quarantine stale and scratch material

**What.** Move stale and scratch material to archive locations. Quarantine targets per `RESTRUCTURE_INVENTORY.md` Stage 4: the 22 scratch scripts at workspace root; the stale parallel `EE_Theory_Lab/phase_4B/` tree (capital B at workspace parent level).

**Trigger.** Stage 3 (item 4) complete.

**Acceptance.** Quarantine moves executed; `MANIFEST.md` updated to reflect quarantine locations; the parallel `phase_4B/` tree no longer surfaces in `git status` as an untracked-or-confused parent directory; this STANDING_ITEMS.md entry closes.

---

### 6. Stage 5 transition — next analytical phase

**What.** Decide which macro-level F-form adjudication route (aggregate trajectory comparisons, Ψ-structure analysis, Q-driven base drift, regime-transition timing, repeat-seed designs) becomes the next pre-registered analytical work. Specify the pre-registration. Route to Layer 2 for full cycle. Once pre-registered, route to Layer 3 (Gemini) for execution against canonical substrate data.

**Trigger.** Stage 4 (item 5) complete; restructure cluster fully landed.

**Acceptance.** Architectural decision arbitrated by Mike; new pre-registration committed under `phase_4b/pre_registrations/`; Layer 2 full cycle complete on the pre-registration; Layer 3 routing in hand.

---

### 7. F multiplicativity commitment verification

**What.** Verify the current commitment status of F(v,c,r)'s multiplicativity property. This is a precondition for the surgical fix to v1.5 Overview's "modest-resources-outperform-abundant" passage (per project memory: Move A field-observed puzzle is fine; Move B is self-referential and contradicts the situating-not-replacing stance; the multiplicative-composition point should live in technical sections on F rather than in Move B's prose).

**Trigger.** When v1.5 Overview revision work surfaces from Phil's manuscript timeline. Independent of restructure stages; not blocking other work.

**Acceptance.** Commitment status documented (either confirmed multiplicative, or specified as one of multiple compatible forms, or specified as open). Documentation written to a substantive location (likely State of the Theory v1.1 amendment if a commitment is locked, or to operations log if status is open). When status is documented, the v1.5 surgical fix becomes executable on Phil's timeline.

---

### 8. `global_timeseries.csv` rename-or-README decision

**What.** Decide whether to rename `phase_4b/tier2_outputs/global_timeseries.csv` to a name that disambiguates it from the per-probe-scale `global_timeseries_*.csv` files, or to add a README in `phase_4b/tier2_outputs/` documenting the file's role as the merged Tier 2 → Tier 3 bridging artifact. Canonical status of the file was settled during session 8 Stage 0 inventory; the disambiguating-documentation choice is pending.

**Trigger.** Stage 2 (item 3) execution. The rename or README addition happens during Stage 2, not after, because Stage 2 is when canonical artifact placement is settled.

**Acceptance.** Either rename executed via `git mv`, or README added at `phase_4b/tier2_outputs/README.md`. `canonical_artifacts_index.md` Section 5 updated to reflect the chosen disambiguation.

---

### 10. ChatGPT and Gemini onboarding under session-9 framework

**What.** Produce ChatGPT and Gemini onboarding documents under the session-9 foundational-set framework (analogous to the kit-revision-3 cold-start surface for Claude). The prior-cycle primer documents at `protocols/onboarding/chatgpt_new_chat_primer.md` and `protocols/onboarding/gemini_new_chat_primer.md` were anchored to Cycle 2 Round 1 Post-Flight-2-Closure state; substantive content has moved sufficiently since that salvaging them as still-authoritative would require substantial rewriting against current state. Item 9 reconciliation deferred this work as out-of-scope.

Provenance: item 9 reconciliation Section 1.1 (in `PRIOR_CYCLE_RECONCILIATION_PLAN.md`) arbitrated this item to deferred status. The deferral is recorded in `protocols/onboarding/README.md` (the supersession marker added in the session 10 commit cluster).

**Trigger.** When a fresh ChatGPT or Gemini instance is needed for substantive work and the existing prior-cycle primers are determined inadequate as cold-start surface. Could fire structurally with Stage 5 (when next analytical phase opens), or earlier if Mike opens new ChatGPT or Gemini chats during restructure stages 2-4 and finds the prior-cycle primers' anchoring to Cycle 2 Round 1 Post-Flight-2-Closure state insufficient.

**Acceptance.** ChatGPT onboarding document and Gemini onboarding document drafted against current state. Likely shape: compressed surfaces over the foundational set (parallel to kit-revision-3 for Claude), with role definitions per `protocol_primer.md`, vocabulary discipline per `vocabulary_quarantine.md`, primary-source verification discipline per `standing_rules.md`. Committed at canonical paths (likely under `protocols/foundational/` or a new `protocols/onboarding_current/` sibling to the prior-cycle directory).

---

### 11. Pipeline gap: outcome-construction not wired into intake (supersedes item 1)

**What.** The session 10 execution of item 1 (pre-registration reproducibility verification) surfaced that the committed canonical pipeline at `3189ab7` cannot produce the committed reg_01 outputs at `3189ab7`. The pipeline fails at `validate_formula_variables` because outcome variable `logit_p_base` is never constructed. The intake module's CONSTRUCTION_REGISTRY contains `_eta_floor_inversion` (which when applied constructs `logit_p_base` from `p_act`), and the yaml's outcome block correctly references the registry key (`eta_floor_inversion_of_p_base`). However, `construct_derived_variables` iterates only the yaml's `derived_variables` block, not the outcome block. The function exists and is registered; it is never called.

The pre-reconciliation regression script at `89b85f4` had inline outcome construction (`df['logit_p_base'], boundary_count = eta_floor_inversion(df['p_act'])`). The reconciliation commit `3189ab7` deleted this line, moved the function into the intake module's CONSTRUCTION_REGISTRY, and updated imports — but did not wire the registry into the pipeline.

This item supersedes item 1. The substantive reg_01 finding from session 6 is not invalidated but is under flag pending item 11 closure; the committed outputs may be substantively correct (produced by an earlier valid pipeline) but cannot be reproduced by the current committed code.

**Trigger.** Open. Immediate priority; supersedes items 2 (push to origin) and 3 (Stage 2 execution) because push should not propagate a pipeline that cannot reproduce its committed outputs and Stage 2 moves should not proceed against an unstable canonical record.

**Acceptance.** Three sub-deliverables:

1. **Determine whether the committed outputs are substantively correct.** Run the pre-reconciliation pipeline (the `89b85f4` regression script with inline outcome construction, against the `b10682a` yaml schema or with appropriate adaptation) and check whether it produces outputs matching the committed `3189ab7` outputs. Or identify the actual code path that produced the committed outputs through git history, file timestamps, or operations-log archaeology. Findings documented in the executing session's operations log.

2. **Wire the outcome-construction step into the current pipeline.** Code fix to `_phase_4b_intake.py`. Likely shape: add a `construct_outcome(df, normalized)` function that runs the CONSTRUCTION_REGISTRY against `normalized.outcome_construction` after `construct_derived_variables`. Call site added to `run_tier3` in `tier3_regression.py` between the existing `construct_derived_variables` call and `validate_formula_variables`. Layer 1 architectural review before commit per protocol-infrastructure-routing discipline.

3. **Re-run with the fixed pipeline and diff against committed outputs.** Per the original item 1 acceptance criteria, with the corrected pipeline. Clean diff confirms substantive correctness of committed outputs. Non-clean diff surfaces a further gap requiring Mike's arbitration on what the canonical outputs should be.

**Substantive implications for the canonical record.** `protocols/foundational/current_state.md` Section 2 (latest substantive finding: reg_01 identity-recovery) requires update at item 11 closure. Until then, the framing preserves the reg_01 finding as substantively committed-but-pipeline-flagged.

**Toolchain.** `tier3_regression.py` at `phase_4b/scripts/`; `_phase_4b_intake.py` at `phase_4b/scripts/`; `_phase_4b_common.py` at `phase_4b/scripts/` (contains the `eta_floor_inversion` function the intake module imports); pre-registration yaml at `phase_4b/pre_registrations/reg_01_scale_interactions.yaml`. Committed reg_01 outputs at `phase_4b/tier3_outputs/`. All paths verified during item 1 execution.

---

## Maintenance log

This section records when items closed or new items added. Each entry references the operations log of the session in which the change occurred.

- **Item 9 added (session 9 close).** Prior-cycle canonical material discovered via primary-source verification at session-9 close. The session 9 operations log addendum records the discovery; this STANDING_ITEMS.md update commits the trigger structure for session 10 reconciliation.
- **Item 9 closed and removed (session 10).** Three deliverables completed: `PRIOR_CYCLE_INVENTORY.md` (workspace root), `PRIOR_CYCLE_RECONCILIATION_PLAN.md` (workspace root), and the canonical record update commit cluster (foundational set updates, three new foundational documents, two new in-directory READMEs, operations_log README update). Layer 2 sanity scan returned PASS-with-notes; patches incorporated before commit. Item 9's acceptance criteria fully met. Per the maintenance discipline (items removed when acceptance is met), item 9 is removed from this list. The reconciliation cluster's operations log records the closure.
- **Item 10 added (session 10).** ChatGPT and Gemini onboarding under session-9 framework, deferred during item 9 reconciliation as out-of-scope for that item. The session 10 operations log records the deferral arbitration.
- **Item 1 closed and removed (session 10).** Item 1 execution surfaced a pipeline gap: the committed canonical pipeline at `3189ab7` cannot produce the committed reg_01 outputs at `3189ab7` because outcome-construction is not wired into the intake pipeline. Per item 1's acceptance criteria ("If outputs do not match, a gap exists; the gap is surfaced as a routed task and remains tracked under a new item that supersedes this one"), item 1 closes via the surfacing of the gap. Item 11 added to supersede.
- **Item 11 added (session 10).** Pipeline gap: outcome-construction not wired into intake. Three sub-deliverables: determine substantive correctness of committed outputs, wire the construction step into the pipeline, re-run and diff. Supersedes items 1, 2 (push to origin), and 3 (Stage 2 execution) in priority. The session 10 operations log addendum documents the diagnostic trace.

---

— Drafted by Claude as Layer 1 central node, Stage 1 root-level operational process artifact, session 9. Updated session 10 with item 9 removal (acceptance criteria met by reconciliation deliverables and Layer 2 sanity scan), item 10 addition (deferred ChatGPT/Gemini onboarding), item 1 closure (gap surfaced per acceptance criteria), and item 11 addition (pipeline gap superseding item 1). No Layer 2 routing per the agreed sanity-scan-distribution convention (operational process artifact, not architectural deliverable). Ready for commit.
