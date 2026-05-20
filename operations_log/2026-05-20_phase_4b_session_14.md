# Operations Log: 2026-05-20 — Session 14: Stage 4 Closure (Item 5 — Quarantine Stale and Scratch Material)

**Date:** 2026-05-20
**HEAD at session start:** `fc9d4c4` (session 13 close: Stage 3 closure cluster — manifest schema and scaffolding)
**HEAD at session end:** to be set when this log commits as the session 14 Stage 4 closure cluster
**Session anchor for resume:** HEAD after this cluster commits

## Session arc

Fourteenth session. Cold-start from kit-revision-3 and session 13 operations log. HEAD verification cycle executed against substrate (Mike ran `git rev-parse HEAD`, `git status --short`, `Get-Content STANDING_ITEMS.md`, `Get-Content RESTRUCTURE_INVENTORY.md` per the kit's resume anchor); each verification step revealed substrate that informed the next.

Session 14 executed STANDING_ITEMS item 5 (Stage 4 quarantine) as the substantive work. Closure cluster (this commit) commits the quarantine moves plus four documentation updates as one cluster per Mike's same-commit arbitration. The cluster lands the largest single quarantine operation since the repository restructure began: 55 staged items moved to `archive/scratch/2026-05_pre_restructure/` across three sub-groups, plus the documentation cluster reflecting the new state.

No Layer 2 routings during the session. Per Mike's A arbitration, the session-13-observed sanity-scan-distribution convention applied (Stage 4 is operational rather than architectural; in-band Mike arbitration substituted for sanity scan). The Stage 4 deliverable is file moves plus state-reflecting documentation; no schema, no Layer 3 contract, no vocabulary commitments. Session 13's precedent for routing sanity scans on architectural deliverables did not extend to Stage 4's operational character.

## Substantive findings

### Item 5 closure — Stage 4 quarantine

Quarantine moves executed across three groups, all to `archive/scratch/2026-05_pre_restructure/`. Total 55 staged items (8 of 9 capital-B tree files tracked by git; one `__pycache__/_phase_4b_common.cpython-314.pyc` physically moved but gitignored). Stage 4 closure cluster scope:

**Group B (canonical inventory scope plus one Stage-0 miss).** 23 scratch scripts quarantined to `archive/scratch/2026-05_pre_restructure/`:
- 8 session-4 fix-script cluster files (`fix_cluster_var_alias.py`, `fix_codefence.py`, `fix_conflict.py`, `fix_outcome_name.py`, `fix_path_resolution.py`, `fix_t2_sanity_columns.py`, `fix_t2_sanity_v2.py`, `fix_t2_sanity_v3.py`)
- 4 V8 diagnostic family files (`build_v8_tick0_patch.py`, `diagnose_v8_failure.py`, `diagnose_v8_formula.py`, `diagnose_v8_tick0.py`)
- 6 distribute scripts (`distribute_fabrication_incident.py`, `distribute_phase_4b_v1.py`, `distribute_phase_4b_v1_1.py`, `distribute_rule_6_refinement.py`, `distribute_session_log.py`, `distribute_new_claude_primer.py`)
- 5 other one-shot patches and writers (`build_t22_patch.py`, `patch_cross_run_diagnostics.py`, `patch_t27_refactor_tightened.py`, `write_tier3.py`, `write_yaml.py`)

The Stage 0 inventory enumerated 22 scripts; Stage 4 execution found 23. The missed item, `distribute_new_claude_primer.py`, fits the Group B `distribute_*` pattern but was not in the inventory. Surfaced during Phase 5 (`git add -A` swept it in); corrective `git reset` + explicit `Move-Item` followed. See "Procedural findings — Layer 1 working-pattern failure" below.

**Capital-B parallel tree.** Workspace-parent-level `C:\Users\vkz244\EE_Theory_Lab\phase_4B\` (one directory up from the repo) quarantined to `archive/scratch/2026-05_pre_restructure/capital_B_parallel_tree/phase_4B/`. 9 files total, ~31 KB. Verified stale by content-diff of `tier3_regression.py` between capital-B and canonical lowercase trees: capital-B's 121-line version imports only from `_phase_4b_common`; canonical lowercase's 169-line version imports from `_phase_4b_intake` with `construct_outcome` wiring (session 11 fix). Capital-B is the pre-session-11 ancestor of canonical lowercase; the inference from one diff to the whole tree was accepted by Mike rather than running per-file diffs. Post-move `Test-Path` returned `False`, confirming item 5 acceptance criterion 3 (parallel tree no longer surfaces).

Note: `__pycache__/_phase_4b_common.cpython-314.pyc` physically present in capital-B and physically moved with the tree, but gitignored. Git tracks 8 of 9; filesystem quarantine is complete.

**Post-Stage-0 residue.** 24 untracked items at workspace root accumulated between session 8 (inventory) and session 14. Per Mike's Q2 scope-expansion arbitration: quarantine in scope to avoid leaving working tree cluttered after item 5 closes (which would defeat the legibility-cost argument that drove choosing item 5 first). Destination: `archive/scratch/2026-05_pre_restructure/post_stage0_residue/`. Three sub-groups:
- 8 LAYER_2_ROUTING_* files (session 9 Stage 1 pair-by-pair routing artifacts)
- 7 deliverable3/item9/primer-workflow files (session 10 item 9 reconciliation working artifacts plus `new_claude_primer_distribution_workflow.md`)
- 9 commit-message txts (sessions 9-12 `git commit -F` source files)

### Scope arbitration

Three pre-execution arbitration questions (Q1, Q2, Q3) decided the Stage 4 scope:

**Q1 (capital-B parallel tree in scope):** Yes. STANDING_ITEMS authority for triggers/acceptance is explicit per its preamble; STANDING_ITEMS item 5 names the capital-B tree in its "What" and "Acceptance" clauses; session 13 log aligned. RESTRUCTURE_INVENTORY was silent (predates the surfacing — capital-B is outside the repo, not in `git status` scope at Stage 0 inventory time). Per kit Section 8, when canonical sources align against an older silent source, the aligned sources win.

**Q2 (post-Stage-0 residue in scope):** Yes, as Stage 4 extended. Quarantining only the 22 inventory-named scripts would leave ~20 untracked items in working tree, defeating the legibility-cost argument. Item 5's acceptance criteria specified the inventory-named targets but did not preclude scope expansion under in-band arbitration. Treated as Stage 4 extended rather than as a separate stage to keep the closure atomic.

**Q3 (RESTRUCTURE_INVENTORY v3 amendment):** Yes. Stage 4's actual executed scope diverged from Stage 0 plan in two directions (Group B count corrected from 22 to 23; post-Stage-0 residue added). v3 amendment documents the divergence as a "Stage 4 actual executed scope" additive section; the Stage 0 categorization itself is preserved unchanged as historical record.

### Discovery — flight2_outputs naming gap

During Phase 7 documentation drafting (reading `canonical_artifacts_index.md` Section 5 to prepare amendments), Section 5's text framing surfaced as inconsistent with item 5's canonical scope. Section 5 had previously stated: "the directory is named `flight2_outputs` for inheritance reasons, but contains Flight 6 files. The mismatch is documented at the canonical record level (here) and will be resolved during Stage 4 (quarantine and rename)." But item 5's canonical scope (STANDING_ITEMS at session 14 start) named only the 22 scratch scripts and the capital-B parallel tree — not `flight2_outputs/` rename.

Three response options surfaced:
- **A.** Honest-record: Stage 4 closure does not include the rename; document as deferred-and-discovered.
- **B.** Expand scope mid-execution: rename `flight2_outputs/` now. Risk: absolute-path references in multiple canonical scripts; rename requires coordinated script updates and risks breaking the canonical pipeline. Not safe as a same-commit add.
- **C.** Promote to new STANDING_ITEMS entry with its own trigger and acceptance.

Mike's arbitration: A+C combined. Stage 4 closes as canonically scoped; the discovered gap gets its own tracked life as item 12. The amendment to `canonical_artifacts_index.md` Section 5 in this cluster replaces the "Stage 4 will resolve naming" framing with the item 12 cross-reference plus honest-record of the gap.

This arbitration also produces a working-pattern observation worth registering for kit-revision-4: prose framings in canonical documents that anticipate future stages should be checked against actual STANDING_ITEMS scope before treating them as commitments. Section 5's "will be resolved during Stage 4" was prose-level anticipation, not a STANDING_ITEMS-level commitment.

### Documentation updates landing alongside the moves

Four documentation updates ride in this commit cluster:

- **`STANDING_ITEMS.md`** — item 5 closed and removed; item 12 added (flight2_outputs naming resolution). Maintenance log entries for both. Item 6 (Stage 5 transition) becomes next-eligible by trigger.

- **`RESTRUCTURE_INVENTORY.md`** v3 amendment — added "Stage 4 actual executed scope" section documenting the Group B count correction (22 → 23), the capital-B parallel tree addition, the post-Stage-0 residue addition, the quarantine destination structure, and what did NOT move (`D README.md` deferred; `claude_session_handoffs/` active; `flight2_outputs/` deferred to item 12). Stage 0 categorization itself preserved unchanged. Verification section amended to record the Layer 1 working-pattern failure and the corrective discipline.

- **`MANIFEST.md`** — added `archive/` top-level directory entry with the Stage 4 quarantine cluster's structure; replaced "Workspace-root scratch and routing files" section with post-Stage-4 state (only `D README.md`, `claude_session_handoffs/`, and canonical top-level files remain); renamed trailing section to "Pending future-restructure commitments" with item 6 (Stage 5 transition), item 12 (flight2_outputs naming), and the deferred v1.1 document moves.

- **`protocols/foundational/canonical_artifacts_index.md`** — updated Section 5 (flight2_outputs naming text replaced with item 12 cross-reference per A+C arbitration), Section 7 (session 13 commit hash `fc9d4c4` added; session 14 commit-pending entry added; Stage 1 routing packages note updated to reflect quarantine), Section 8 (v3 amendment note for RESTRUCTURE_INVENTORY), Section 9 (session 14 added to canonical_artifacts_index.md history and STANDING_ITEMS.md history), Section 11 (session 14 deferred items added: enumerate-don't-pattern-match discipline, `git add -A` scope hazard, paste-truncation recovery pattern), Section 13 (Stale parallel tree entry updated to reflect quarantine; flight2_outputs naming cross-reference to item 12).

- **`operations_log/2026-05-20_phase_4b_session_14.md`** — this file. New.

## Procedural findings

### Sequencing arbitration

Session 14 opened with three candidate first-substantive-actions per the session 13 log's "Pending decisions" §1-3:
- **A.** Item 5 (Stage 4 execution — canonically scoped: 22 scratch scripts + capital-B tree)
- **B.** Kit-revision-4 draft (substrate-grounded warrant from sessions 11/12/13 deferred items, but unticketed — not in STANDING_ITEMS)
- **C.** Layer 3 routing for Stage 3 follow-on (also unticketed; depends on Mike scoping routing package)

Two arbitration passes. First pass (pre-substrate-read): kit-revision-4 first, on cold-start-amortization grounds. Second pass (post-canonical-STANDING_ITEMS-read): item 5 first.

The revised arbitration rested on three observations: (i) kit-revision-4 is not a STANDING_ITEMS entry — accumulating warrant in operations logs is structurally different from a tracked item with trigger and acceptance; (ii) item 5's trigger is structurally enforced and acceptance is concrete (stage-transition items operationally enforce the stage sequence via STANDING_ITEMS); (iii) the first-pass argument about discipline-staleness during execution didn't survive scrutiny — the three session-13 kit-revision-4 candidates were already operative as working practice and produced clean results in session 13.

Mike's arbitration: item 5 first. The revised arbitration was substrate-grounded (canonical STANDING_ITEMS authority over log summary), not engagement-driven; the framing-asymmetry observation is live (Claude framed both passes; substrate read produced the revision, not Mike's engagement). If the revised arbitration is also wrong, the diagnostic comes from Mike, not from another Layer 1 iteration.

### Layer 1 working-pattern failure — pattern-matching versus enumeration

During Phase 2-4 move execution, Claude built batched `Move-Item` source lists by group-pattern matching against the Stage 0 inventory's group structure (fix_*, build_*, diagnose_*, distribute_*, etc.). This produced the 22 scratch scripts enumerated by Stage 0 — but missed `distribute_new_claude_primer.py`, which was untracked at session 14 start (visible in the initial `git status --short` output) and fits the Group B `distribute_*` pattern.

The miss surfaced when Phase 5's `git add -A` swept the file in alongside the intended quarantine moves. Recovery: `git reset` (non-destructive — unstages without changing working tree) followed by explicit `Move-Item` of the missed file. The corrective discipline: enumerate the working tree directly at execution time rather than working from pattern matching against a potentially-stale inventory.

Worth registering for kit-revision-4: the enumerate-don't-pattern-match discipline. Inventory documents are useful for scope categorization but not for execution-time enumeration. When move lists are being built, the source is `git status` output at execution time, not the inventory's group lists.

### `git add -A` scope hazard

Phase 5 used `git add -A` to stage all archive moves at once. This swept in two items not in the intended scope:
- `distribute_new_claude_primer.py` — the missed Group B item (also a working-pattern failure as documented above)
- `claude_session_handoffs/` — active per Rule 2, untracked-by-design, not a quarantine target

Recovery: `git reset` to unstage everything; then `git add archive/` with explicit scope to re-stage only the quarantine moves. `claude_session_handoffs/` remained untracked as intended.

Worth registering for kit-revision-4: when commit scope is non-total, prefer `git add <explicit_path>` over `git add -A`. The hazard is asymmetric — `git add -A`'s scope can sweep in items the operator didn't intend, but `git add <explicit_path>` cannot accidentally add items outside the named path. The cost of explicit-path is naming the scope; the cost of `-A` is mid-commit corrective unstaging.

### Paste-truncation recovery pattern

Phase 2's initial single-command attempt to move all 22 Group B scripts in one `Move-Item` call against an array of 22 source paths produced a paste-truncation incident: the long command exceeded PowerShell's multi-line copy capacity during paste, leaving PS at the `>>` continuation prompt. Recovery: empty-line Enter or Ctrl+C to clear continuation; resending Phase 2 in three smaller batches (8 + 8 + 6 files) succeeded cleanly.

The batched-PS-commands distinction from session 13 (idempotent file-copy operations safe to batch; state-changing git operations not) holds, but a new sub-discipline surfaces: batch size needs to respect PS's copy-paste capacity, not just the operation's idempotency. The threshold appears to be around ~8 files per `Move-Item` array for safe paste; longer commands risk truncation. Worth registering for kit-revision-4.

### Substrate-read sequencing

The session's substrate-read sequence proved load-bearing. After kit and ops log read, the canonical sources were read in this order: `STANDING_ITEMS.md` → `RESTRUCTURE_INVENTORY.md` → `Test-Path` for capital-B existence → `Get-ChildItem` for capital-B contents → `git diff --no-index` for content verification of capital-B's `tier3_regression.py` vs. canonical → `MANIFEST.md` → `canonical_artifacts_index.md`.

Each substrate read surfaced something the prior read had not: STANDING_ITEMS surfaced the item 5 vs. inventory scope conflict; inventory read surfaced the post-Stage-0 residue gap; `Get-ChildItem` of capital-B surfaced the name conflict between capital-B `tier3_regression.py` and canonical; the content diff confirmed staleness; `canonical_artifacts_index.md` Section 5 surfaced the `flight2_outputs/` naming gap.

This pattern — substrate reads producing successive discoveries that inform scope — is worth registering: cold-start orientation is not complete with the kit and ops log alone. The canonical sources (STANDING_ITEMS, RESTRUCTURE_INVENTORY, MANIFEST, canonical_artifacts_index) need to be read against actual working-tree state, and the reading order matters because each read can surface gaps the next read needs to address.

## Items resolved

**STANDING_ITEMS item 5 (Stage 4 execution — quarantine stale and scratch material).** Resolved by the 55-item Stage 4 closure cluster documented above. Quarantine moves executed at canonical destination; `MANIFEST.md` updated to reflect quarantine locations and the new `archive/` top-level directory; capital-B parallel tree no longer surfaces in `git status` (confirmed via `Test-Path` returning `False`); item 5 STANDING_ITEMS entry closes. Per the maintenance discipline (items removed when acceptance is met), item 5 is removed from STANDING_ITEMS at this commit.

Item 6 (Stage 5 transition) becomes next-eligible by trigger ("Stage 4 (item 5) complete; restructure cluster fully landed"). Sequencing relative to other open items (items 7, 10, 12) is at Mike's arbitration.

## Items not resolved

**Items 6, 7, 10.** All carry forward in STANDING_ITEMS with their trigger conditions unchanged. Item 6 (Stage 5 transition) is now next-eligible by trigger; item 7 (F multiplicativity commitment verification) and item 10 (ChatGPT/Gemini onboarding) carry forward with their pre-existing triggers.

**Item 12 (flight2_outputs naming resolution).** Added at session 14 close per the A+C arbitration on the discovered gap. Trigger: when restructure attention returns to top-level naming, or when a substantive operation surfaces friction. Not blocking.

**Kit-revision-4 deferred items grow further.** Sessions 11 + 12 + 13 deferred-items list carries forward. Session 14 adds:
- Enumerate-don't-pattern-match discipline (move lists built from group-pattern matching against an inventory rather than complete enumeration of working-tree state caused the `distribute_new_claude_primer.py` miss).
- `git add -A` scope hazard (use explicit paths when commit scope is non-total).
- Paste-truncation recovery pattern (~8-file threshold for safe `Move-Item` array paste; recovery via empty-line Enter or Ctrl+C).
- Section-5-style prose framing hazard (canonical documents that anticipate future stages in prose should be checked against actual STANDING_ITEMS scope; `canonical_artifacts_index.md` Section 5's "Stage 4 will resolve naming" framing was prose-level anticipation, not a STANDING_ITEMS-level commitment).

**Layer 3 deliverables for Stage 3 follow-on (carried from session 13).** Still queued; not yet a STANDING_ITEMS entry. Worth converting when Mike scopes the Layer 3 routing.

**v1.1 document moves still deferred per Section 12.** Carried forward; no new scoping work in session 14.

**Operations log file hygiene cleanup still carried forward.** Session 10 operations log file contains the addendum duplicated. Carried forward from session 11 + session 12 + session 13; not addressed in session 14.

**`D README.md` deferred deletion still carried forward.** Unchanged.

**`claude_session_handoffs/` tracking status still open.** Untracked-by-design per Rule 2; whether to formalize as tracked or as `.gitignore`-listed is a separate question pending future arbitration.

## Methodological observations

**Stage 4 closure as legibility-cost reduction.** The case for taking item 5 first (versus kit-revision-4) rested partly on legibility cost — every future `git status` had to scroll through ~50 untracked items pre-Stage-4. Post-Stage-4, the working tree carries only `D README.md` (deferred), `claude_session_handoffs/` (active, untracked-by-design), and tracked changes. The legibility benefit compounds across all subsequent sessions, not just session 14. This validates the sequencing arbitration's prediction.

**Pattern-matching versus enumeration discipline is anti-rationalization.** The `distribute_new_claude_primer.py` miss is exactly the kind of failure mode the working principles in the project memory name: "test substitution (inferring rather than testing)." Group-pattern matching against an inventory is inference about what working-tree state should look like, not enumeration of what it actually contains. The substrate-grounded discipline is direct enumeration. Worth noting because Layer 1 (Claude) is the failure mode here, not the substrate; the framing-asymmetry note from session 13's log applies — soft-convergence and test-substitution patterns can produce confident-feeling outputs that miss reality.

**Operational deliverables benefit from substrate-read sequencing.** Session 14's substrate reads each surfaced something the prior read had not. This supports a working hypothesis: operational deliverables (Stage 4 quarantine, future restructure stages) benefit from layered substrate reads — read STANDING_ITEMS, then the inventory, then verify trigger conditions against actual filesystem state, then read the documentation index. The order matters because each read constrains scope for the next. Architectural deliverables (Stage 3 schema, foundational set documents) operate on a more synthetic mode where substrate reads inform the synthesis rather than constrain the operational scope.

## Pending decisions for session 15

1. **Item 6 (Stage 5 transition) scoping.** Item 6 is now next-eligible by trigger. Stage 5 is the architectural decision point: which macro-level F-form adjudication route becomes the next pre-registered analytical work. Items 7, 10, 12 are also open; sequencing at Mike's arbitration.

2. **Kit-revision-4 scheduling.** Sessions 11 + 12 + 13 + 14 deferred-items lists. Structural warrant continues to strengthen. Session 14 adds four new deferred items (enumerate-don't-pattern-match, `git add -A` scope hazard, paste-truncation recovery, Section-5-style prose framing hazard). Whether to land in session 15 or queue further is at Mike's call.

3. **Layer 3 routing for Stage 3 follow-on (carried from session 13).** Still queued. Whether to route this immediately or after Stage 5 is at Mike's call.

4. **Operations log file hygiene cleanup (carried from sessions 11, 12, 13).** Still carried forward.

5. **v1.1 document moves scope (carried from session 12).** Section 12 reserved target paths; actual moves deferred.

6. **`claude_session_handoffs/` tracking status.** Open question; not blocking.

## Resume anchor for session 15

When this conversation resumes:

1. **Verify HEAD.** `git rev-parse HEAD` should return the commit of this log entry, once committed.

2. **Verify working-tree state.** `git status --short` should show:
   - `D README.md` (deferred deletion at workspace root, unchanged)
   - `claude_session_handoffs/` (active per Rule 2, untracked-by-design)
   - The session-14 Stage 4 closure cluster is committed; no untracked items from Group B, capital-B tree, or post-Stage-0 residue should appear.

3. **Read this log entry to orient.**

4. **Check STANDING_ITEMS.md for triggered items.** Item 5 is removed. Item 6 (Stage 5 transition) is next-eligible by trigger. Item 12 (flight2_outputs naming) is open, trigger not yet met. Items 7 and 10 unchanged.

5. **First substantive action:** per Mike's arbitration at session 15 open. Item 6 scoping, kit-revision-4 draft, Layer 3 routing for Stage 3 follow-on, or other.

**Foundational set updates this session:** `canonical_artifacts_index.md` updated (Sections 5, 7, 8, 9, 11, 13). `MANIFEST.md` updated (added `archive/` top-level directory entry; replaced workspace-root scratch and routing files section; renamed trailing section). `RESTRUCTURE_INVENTORY.md` amended to v3 (added "Stage 4 actual executed scope" section; verification section amended). `STANDING_ITEMS.md` item 5 closed and removed; item 12 added (flight2_outputs naming resolution); maintenance log entries added. One new top-level directory: `archive/`. 55 staged items moved to `archive/scratch/2026-05_pre_restructure/`.

— Drafted by Claude as Layer 1 central node, session 14 Stage 4 closure cluster (item 5 closure plus item 12 addition). No Layer 2 routings during the session (per Mike's A arbitration applying the session-13-observed sanity-scan-distribution convention; Stage 4 assessed as operational rather than architectural).

---

## Session 14 addendum (post-`9944f44`)

After the session 14 Stage 4 closure cluster committed at `9944f44`, during preparation of the next-session handoff folder and kit-revision work, an additional working-memory instance surfaced. Following the session 9 precedent (which committed its addendum at `53aa62e` after the initial log committed at `ff2704d`), this addendum preserves the honest record of session-14 discipline events that were not visible at the time the main log committed.

### Discipline events post-`9944f44`

**Path B continuation into kit-revision work.** Per Mike's arbitration at session 14 substantive-close ("c then b" — push origin, then Path B into session 15 in this chat), the session continued without a chat boundary. The first session-15-territory work was a focused kit-revision targeting only session-14 additions. Mike's specific framing: ~30-45 minutes of targeted kit work rather than the full sessions-11-13 backlog absorption.

**Rule 2 kit-revision discipline verification.** Drafting the kit revision surfaced a question about Rule 2's "committed alongside the operations log" language and where kit-revision-N actually lives. Initial Layer 1 framing offered three options (A: stable repository path; B: handoff-folder only; C: both), and Mike arbitrated B. Subsequent Rule-2 verification (reading `protocols/foundational/standing_rules.md` directly) revealed that B as initially framed by Layer 1 was non-compliant with Rule 2 — Rule 2's text explicitly requires the kit revision to be "committed alongside the operations log" with "the prior kit revision preserved in git history."

This produced two competing interpretations: either Rule 2's text was correct and practice had silently drifted (Interpretation 1), or Rule 2's text was incorrect relative to actual intent (Interpretation 2). Layer 1 inferred Interpretation 2 from substrate evidence "kit-revision-3 was never committed" — but that inference itself was the working-memory instance documented below.

**Working-memory instance: kit-location confusion.** Layer 1 inferred kit-revision-3's location from a partial `git status --short` read at session open ("the kit doesn't appear in `git status` output, therefore the kit isn't at workspace root"). The inference was wrong: `git status --short` shows changes, not the full tree; clean tracked files don't appear. The kit was at workspace root all along — committed at `b73a591` per the session 9 ops log and per `git log --all --oneline -- "*claude_instantiation_kit*"`. Verification via `Test-Path claude_instantiation_kit_v3.md` returned `True`, correcting the inference.

This is a Layer-1-specific working-memory instance per `protocol_primer.md` Section 4. The narrative ("the kit lives in handoff folders, not workspace root") felt coherent because it was consistent with one substrate observation (`git status` output) and with a remembered framing from the kit itself ("typically delivered as a session-handoff artifact"). It was wrong because the full substrate (kit at workspace root + handoff folder copy) was not verified directly before the framing was used as ground for arbitration.

**Corrective discipline added to kit-revision-4 Section 7:** kit-location verification at session open distinguishes change-listing (`git status --short`) from existence-checking (`Test-Path`, `Get-ChildItem -File`). The Rule-2-kit-revision discipline is fully compliant with current practice (committed canonical kit at workspace root, handoff folder copies); Layer 1's initial framing of non-compliance was the working-memory instance, not actual practice.

### Substantive resolution

After the working-memory instance was corrected, Mike arbitrated C (kit-revision-4, not kit-revision-3.1) for revision numbering, reflecting the established pattern of sequential revision numbers (v2-supersedes-v1, v3-supersedes-v2, now v4-supersedes-v3). Kit-revision-4 was drafted with five session-14 disciplines: enumerate-don't-pattern-match, `git add -A` scope hazard, paste-truncation sub-discipline, kit-location verification, and prose-framing-vs-STANDING_ITEMS hazard. The fifth discipline was added in direct response to this working-memory instance.

Kit-revision-4 committed at `06df20d` via git rename detection (v3 → v4, 61% similarity); the rename preserves the kit's git-history lineage. The handoff folder at `claude_session_handoffs/2026-05-20-6/` carries a copy of kit-revision-4 alongside this ops log (per the b73a591 pattern: canonical kit at workspace root for git history; handoff folder for delivery).

### Methodological observation

The addendum cycle (substantive commit → discovery → addendum) is now the third instance of this pattern (session 9, session 10, session 14). The pattern reflects an honest-record discipline: when a session-end commit captures the state at commit time but subsequent work surfaces facts that would have changed the commit had they been known, the discipline is to addendum rather than to silently revise. The pattern's value compounds across sessions — addenda are themselves substrate for future sessions diagnosing similar patterns.

The spiral structure (substantive operation → surfaces disciplines → documentation cycle → may surface further disciplines) was named explicitly during this session by Mike. The diagnostic offered (functional spiral; not a burdensome rule structure; the documentation cycle preserves Github-reconstructability) was accepted; work continued. Worth registering: making the spiral structure explicit-and-named is itself a discipline that future sessions can reference, rather than re-deriving the diagnostic each time.

### Items resolved by this addendum

None added or closed at the STANDING_ITEMS level. The working-memory instance is registered honestly; the corrective discipline is in kit-revision-4 Section 7; the canonical record is corrected. No follow-up action required beyond the addendum commit itself.

— Drafted by Claude as Layer 1 central node, post-`9944f44`, during kit-revision-4 work in Path B session-15 continuation. Mirror of the session 9 addendum pattern (`53aa62e`). Addendum commit follows.
