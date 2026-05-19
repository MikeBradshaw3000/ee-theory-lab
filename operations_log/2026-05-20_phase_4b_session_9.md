# Operations Log: 2026-05-19 — Session 9: Stage 1 Complete (Foundational Set, Root-Level Orientation, STANDING_ITEMS, Kit-Revision-3)

**Date:** 2026-05-19
**HEAD at session start:** `3e38980` (session 8 operations log commit)
**HEAD at session end:** `b73a591` (kit-revision-3 commit) — pending this log commit
**Session anchor for resume:** HEAD after this log commits

## Session arc

Ninth session, and the first to operate entirely under kit-revision-2 with the framing of Stage 1 production as the substantive deliverable. Opened with a kit-driven cold start that surfaced two operational gaps: the session 8 operations log was missing from the handoff folder, and the supplementary note prior-Claude drafted to bridge the gap was structurally a parallel instantiation document (the wrong form). Both gaps surfaced kit-improvement items that fold into kit-revision-3.

The session decomposed into six commit clusters, all under the framing of Stage 1 of the repository restructure:

1. **Pair 1** — protocol_primer.md and standing_rules.md (full Layer 2 cycle + v2-acceptance). Committed at `79db966`.
2. **Pair 2** — vocabulary_quarantine.md and canonical_artifacts_index.md (full Layer 2 cycle + v2-acceptance). Committed at `6603799`.
3. **Pair 3** — current_state.md and README.md (full Layer 2 cycle + v2-acceptance); completes `protocols/foundational/`. Committed at `a8bc52c`.
4. **Root-level orientation** — ORIENTATION.md, CURRENT_STATE.md, MANIFEST.md (Layer 2 sanity scan). Committed at `af59c33`.
5. **STANDING_ITEMS.md** — operational deferred-items tracker (no Layer 2 routing). Committed at `5877486`.
6. **Kit-revision-3** — compressed cold-start surface over the now-canonical foundational set (Layer 2 sanity scan). Committed at `b73a591`.

Stage 1 substantive work closed with kit-revision-3 committed; this operations log is the last work item before the session 10 handoff folder preparation.

The session produced six routing cycles total: three full Layer 2 cycles (each followed by v2-acceptance) on the foundational document pairs, and three Layer 2 sanity scans on the derivative material. The session validated the v2-acceptance step as effective discipline (Layer 2 caught a same-session vocabulary-quarantine violation that Layer 1's self-review missed), the routing-shape distribution as appropriate to deliverable type (heavy review for load-bearing material; sanity scan for derivative material), and the cold-start economy as production-capable (substantial work fit cleanly inside one session after the foundational set instantiation overhead was paid).

## Substantive findings

**Stage 1 complete.** Six commits over the course of session 9 produce the foundational document set (`protocols/foundational/` with six documents), the root-level orientation spine (`ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`), the operational deferred-items tracker (`STANDING_ITEMS.md`), and kit-revision-3. With these committed, the canonical material that earlier sessions paid cold-start cost to reconstruct from working memory now lives at stable repository paths with clear authority hierarchy.

The foundational document set is six documents:

- `protocols/foundational/protocol_primer.md` (committed `79db966`) — multi-AI protocol structure
- `protocols/foundational/standing_rules.md` (committed `79db966`) — protocol-level standing rules (Rule 1-10 with Rule 7 expanded as 7.1-7.7)
- `protocols/foundational/vocabulary_quarantine.md` (committed `6603799`) — prohibited terms, permitted framings, drift-prone vocabulary
- `protocols/foundational/canonical_artifacts_index.md` (committed `6603799`) — where canonical artifacts live and what authority they carry
- `protocols/foundational/current_state.md` (committed `a8bc52c`) — Phase 4B and protocol current state
- `protocols/foundational/README.md` (committed `a8bc52c`) — entry point and reading sequence

**Kit-revision-3 supersedes kit-revision-2.** Kit-revision-2 (drafted at session 7 end) carried the protocol primer, vocabulary quarantine, standing rules, and canonical artifacts index content directly because the foundational set did not yet exist as committed canonical documents. Kit-revision-3 is structurally different: it is a compressed cold-start surface over the now-canonical foundational set, with summaries and pointers rather than content reproduction. The kit is now leaner in canonical-material reproduction but richer in operational content (the new Section 3 captures eleven kit-improvement items from sessions 7-9).

Kit-revision-3 is at workspace root, committed `b73a591`. The session 10 handoff folder delivers kit-revision-3 as the default instantiation surface; kit-revision-2 is preserved in git history and is no longer the operational surface.

**Pre-registration reproducibility verification trigger condition met.** With Stage 1 complete (this log commits as the final Stage 1 work), the pre-registration reproducibility verification (item 1 in `STANDING_ITEMS.md`) is now eligible to fire as the first substantive action of session 10. This is a structural trigger fire that the bullet-proof deferral process makes operational.

**`global_timeseries.csv` rename-or-README decision deferred to Stage 2.** Per `STANDING_ITEMS.md` item 8, the disambiguating-documentation choice for the canonical Tier 2 → Tier 3 bridging artifact fires during Stage 2 execution. The canonical status of the file was settled during session 8 Stage 0 inventory; only the disambiguation choice remains.

## Procedural findings

**Cold-start opening surfaced two operational gaps.** Session 9 instantiation began with kit-revision-2 (uploaded by Mike via the session-handoff folder) plus a supplementary note prior-Claude drafted at session 8 close. The session 8 operations log itself was missing from the handoff folder. Two findings:

1. **Session-handoff folder must contain the just-closed session's operations log.** Without it, next-session Claude operates from kit-summary plus prose-summary supplementary material, which is the working-memory failure mode the protocol is structurally designed to avoid. The supplementary note was substantive (it captured working-pattern observations that did not yet exist in kit-revision-2), but its absence of primary-source backing required new Claude to verify against git log and request the operations log explicitly. This is added to the kit-revision-3 working-pattern section and to `standing_rules.md` Rule 2 as a sub-discipline.

2. **Opening instruction to next-session Claude is a single sentence pointing at the kit.** Prior-Claude drafted a multi-page supplementary note because the kit did not yet contain the working-pattern material. The supplementary note as a form was structurally wrong: it competed with the kit for instantiation authority. The corrective discipline: all substantive operational knowledge belongs *inside* the kit (kit-revision-3 now has the working-pattern section); the opening instruction is a single sentence pointing at the kit. This is added to `standing_rules.md` Rule 2.

**Layer 1-specific working-memory instance: Open Element 14 vocabulary-quarantine violation.** During pair-3 drafting (current_state.md v1), Layer 1 used the label "Open Element 14" in Section 2's restatement of the reg_01 analytical scope. The label is the canonical example of drift-prone vocabulary in `vocabulary_quarantine.md` Section 3 (committed at `6603799` earlier in the same session as the violation). Layer 1 drafted the quarantine, then violated it in a sibling document within the same session.

Layer 2 caught the violation on first pass during the pair-3 sanity check; Layer 1 self-review failed to catch it before routing. The instance is registered at commit-level in `a8bc52c`'s commit message and is captured here for the canonical record. Rule 7.4 (memory-based reconstruction without canonical source verification) applies symmetrically across all AI partners including Layer 1; Layer 1's central-node role does not exempt Layer 1 from the discipline. Corrective rule: when Layer 1 drafts vocabulary-discipline canonical material and other documents in the same session, Layer 1 self-review of those other documents must specifically check against the just-drafted vocabulary material before routing. The self-review failure is registered here so future Layer 1 instances can apply the discipline structurally.

**Multi-file delivery preference surfaced.** Two delivery shapes for multi-file `present_files` calls were tested:

- Multi-file `present_files` call → downloads as a single zip → requires `Expand-Archive` step.
- Sequential single-file `present_files` calls → downloads as separate files → requires `Move-Item` only.

Mike's preference is separate files, not zips. The unzip step is thumb expense; sequential single-file `present_files` calls eliminate it at the cost of slightly more click events per delivery. This is captured in kit-revision-3 Section 3 (file delivery subsection) and is now operational practice.

**PowerShell paste-back failure modes.** Two paste-back incidents during the session: PS interpreted text from Claude's response as command input when the response and the command block weren't visually separated enough. Recovery in both cases was Ctrl+C or Enter on an empty line to clear PS's multi-line continuation. The kit-revision-3 working-pattern section captures the failure mode and the convention that mitigates it: PS commands in fenced code blocks should be unambiguously paste-targets, with lean response text immediately above and below to keep paste-targeting unambiguous.

**Path-doubling error caught and corrected.** Layer 1 issued a PS command with a redundant `ee-theory-lab\` prefix when Mike's shell was already at the lowercase nested workspace root. The error surfaced through PS's `Cannot find path` message. The corrective: Layer 1 should treat the kit's "relative to `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\`" path convention as Mike's actual working directory, not as a path to be reproduced as a prefix. Single-incident this session; worth noting for future Layer 1 instances.

**Routing-shape distribution worked as designed.** Six routing cycles, three shapes:

- Three full Layer 2 cycles (each with v2-acceptance pass) on the foundational document pairs. Each pair yielded specified revisions; v2-acceptance closed each pair before commit.
- Three Layer 2 sanity scans on derivative material (root-level orientation; kit-revision-3). The kit-revision-3 sanity scan was clear with no findings; the root-level orientation sanity scan yielded two patches incorporated directly without v2-acceptance.
- No routing on `STANDING_ITEMS.md` (operational process artifact) or this operations log (Mike-author convention).

The distribution matches the decision committed earlier in the session: full cycle for load-bearing protocol-infrastructure material; sanity scan for derivative material; no routing for process artifacts. The yields validated the distribution — Layer 2's full-cycle reviews surfaced architectural patches (chronology clarification, v2-acceptance convention, primary-source override parallelism, thumb-economy subordinacy, "solid" tier clarification, Open Element discipline omission, "homeostatic imperative" rationale tightening, Mike-local artifact operational locatability, Open Element 14 vocabulary violation, completed-item categorization drift, sequencing clarification, audience clarification). Sanity scans surfaced fewer items but caught real ones (authority hierarchy ordering, "terrain reshaping" drift).

**Layer 1 boundary-crossings registered.** Extensive this session, all disclosed at the time and registered in the relevant commit messages:

1. Direct drafting of all six foundational documents (pairs 1, 2, 3).
2. Direct drafting of all three root-level orientation documents.
3. Direct drafting of `STANDING_ITEMS.md`.
4. Direct drafting of kit-revision-3.
5. Direct drafting of all six Layer 2 routing packages (three full cycle, three v2-acceptance, two sanity scan — total eight routing artifacts).
6. Direct drafting of all six commit messages.
7. Direct drafting of this operations log.

The pattern is justified by session economics (Layer 1 had primary source loaded; round-trips to Layer 3 would not have produced different content) and by deliverable type (none of these are Layer 3 implementation artifacts). The boundary-crossing pattern remains a tracked feature of the central-node role; whether it should be tightened toward stricter layer discipline is a protocol-level question Mike arbitrates over time.

## Items resolved

**Stage 1 (kit Section 2 item 1, session 8 pending-decision 1).** Resolved by the six Stage 1 commits. The foundational document set, root-level orientation, deferred-items tracker, and kit-revision-3 are all in the canonical record.

**Section 15 prohibitions lift (kit Section 2 item 4, session 6 commitment).** Resolved by `protocols/foundational/standing_rules.md` Rule 7 expansion (committed `79db966`). The lift translated each protocol-applicable Section 15 item to Rule 7.1-7.7 with citations back to the substrate specification.

**Kit revisions (kit-improvement tracking from sessions 7-8 plus session-9 additions).** Resolved by kit-revision-3 commit (`b73a591`). Eleven items absorbed into the kit's structural redesign and the new working-pattern section.

**`global_timeseries.csv` canonical status (session 7 pending decision 3).** Confirmed canonical at session 8 Stage 0 inventory; this session adds the disambiguating-documentation decision as `STANDING_ITEMS.md` item 8 (deferred to Stage 2 execution).

**Foundational document set kit reference correction (session 7 pending decision 3, session 8 pending decision 3).** Resolved by kit-revision-3 referencing the canonical foundational set at `protocols/foundational/` rather than carrying its own canonical content.

**Multi-file delivery preference, paste-back failure mitigation, opening-instruction discipline (surfaced this session).** Resolved by kit-revision-3 Section 3 and `standing_rules.md` Rule 2 sub-disciplines.

## Items not resolved

All items not resolved are tracked in `STANDING_ITEMS.md` (committed `5877486`). Listing here for cross-reference:

1. **Pre-registration reproducibility verification.** Trigger condition met by this session's close.
2. **Push to origin.** Local main 9 ahead of origin/main after this commit count.
3. **Stage 2 execution — canonical artifact moves.** Trigger fires after items 1 and 2 close.
4. **Stage 3 execution — manifests for parquet outputs.** Trigger fires after Stage 2.
5. **Stage 4 execution — quarantine stale and scratch material.** Trigger fires after Stage 3.
6. **Stage 5 transition — next analytical phase.** Trigger fires after Stage 4.
7. **F multiplicativity commitment verification.** Independent trigger (v1.5 Overview revision work surfaces).
8. **`global_timeseries.csv` rename-or-README decision.** Fires during Stage 2 execution.

## Methodological observations

**Cold-start economics validated at third instance.** Session 7 was the first session under the foundational document set (working from kit-revision-2 as the operational surface). Session 8 was the second. Session 9 is the third, and the first to produce the canonical foundational set itself. Across all three, kit-driven instantiation enabled substantive work within the first session of the new framework. Session 9 additionally validated that the cold-start cost amortizes against substantial work in the same chat: six commit clusters fit inside one session because the cold-start cost was paid and harvested.

The lesson, registered in kit-revision-3 Section 3 / Cold-start economy subsection: cold-start cost is paid to enable work, not to enable another cold start. The "dedicated session" convention from session 6 names a fatigue/scope-mixing concern, not a fresh-chat-per-stage rule.

**The foundational set is now canonical infrastructure.** Future Claude instances instantiating from session 10 onward have a stable canonical reference at `protocols/foundational/`. The kit becomes the cold-start pointer to canonical material rather than the canonical material itself. This is the structural fix to the cold-start cost problem named in session 6.

**The v2-acceptance step is effective discipline.** All three full Layer 2 cycles this session included v2-acceptance. The acceptance pass caught nothing substantive (no Layer 1 drift in v2 incorporation), but the discipline operated as designed: Layer 2 verified that Layer 1's incorporation matched Layer 2's intent, and that Layer 1 had not introduced material beyond Layer 2's review. The discipline is cheap (a short routing message + Layer 2 read) and prevents a known framing-asymmetry pattern (Layer 1's compression of Layer 2's review into Layer 1's framing during v1→v2 incorporation). Worth retaining as the standard for protocol-infrastructure routings.

**The Open Element 14 violation is a Layer-1-specific working-memory instance worth registering.** Session 7 surfaced two Layer-1-specific working-memory instances (git status text vs git log primary source; staging batch sequencing). This session adds a third (vocabulary quarantine violation in a same-session sibling document). The pattern: Layer 1 enforces a discipline against other layers but the same discipline applies to Layer 1 reflexively, and Layer 1 self-review can miss the application when guard is down on documents drafted alongside the discipline-defining canonical material. Rule 7.4 already names the symmetric application; the operational form of the self-review check needs strengthening when Layer 1 is drafting vocabulary-discipline material and other documents in the same session.

**Framing-asymmetry pattern caught at the orientation-document level.** Layer 2's pair-3 review surfaced not just the Open Element 14 violation but also categorization drift, sequencing ambiguity, and audience overcompression. These are not architectural issues; they are framing-compression effects that Layer 1 did not see during self-review. The discipline (route to Layer 2 when Mike names limits of his own ability to judge a Layer-1-drafted artifact; sanity scan as low-cost containment) operated as designed.

**Eleven kit-improvement items accumulated and absorbed.** The accumulation pattern across sessions 7-9 demonstrates that kit-revision discipline (Rule 2 sub-discipline added this session: kit revision committed alongside operations log if working-pattern changes surfaced) is operational and load-bearing. Without the accumulation discipline, the eleven items would have re-surfaced as cold-start gaps in future sessions. With it, kit-revision-3 absorbs them and the operational gap is closed.

**Layer 1 drafted approximately twenty artifacts this session.** Six canonical foundational documents, three root-level orientation documents, one deferred-items tracker, one kit revision, eight routing packages (three full cycle, three v2-acceptance, two sanity scan), six commit messages, and this operations log. The boundary-crossing pattern is extensive but justified by session economics; the alternative (round-trips to Layer 3 for code-like artifact production) was not the right shape for this session's deliverable type. Worth registering for future protocol-level assessment.

## Pending decisions for session 10

1. **Pre-registration reproducibility verification.** Per `STANDING_ITEMS.md` item 1, this fires as the first substantive action of session 10. Layer 1 will execute or surface for arbitration on routing shape (whether it routes to Layer 3 for code execution or runs directly).

2. **Push to origin.** Per `STANDING_ITEMS.md` item 2, fires post-Stage-1 natural commit cluster. The cluster is now closed; push is eligible. Sequencing relative to item 1 is at Mike's arbitration.

3. **Stage 2 execution.** Per `STANDING_ITEMS.md` item 3, fires after items 1 and 2 close. The moves-plan is in `RESTRUCTURE_INVENTORY.md`; Stage 2 is substantial work and may warrant its own session.

4. **Kit storage path question.** Whether to standardize on a stable repository path for the kit (e.g., `protocols/kit/`) versus continuing the session-handoff-folder delivery pattern. Registered in kit-revision-3 commit message; not blocking but worth surfacing for arbitration.

5. **Session 10 routing-shape distribution.** Whether session 10 continues the routing-shape distribution from this session, or whether new routing patterns emerge as the restructure transitions from Stage 1 (document drafting) to Stage 2 (file moves).

## Resume anchor for session 10

When this conversation resumes:

1. **Verify HEAD:** `git rev-parse HEAD` should return the commit of this log entry, once committed.

2. **Verify working-tree state:** `git status --short` should show the remaining items pending Stage 2 work: the scratch scripts at workspace root (per `RESTRUCTURE_INVENTORY.md` Stage 4 categorization), the routing artifacts (Stage 2 archive targets), the diagnostic stdout files (Stage 2 moves to `phase_4b/diagnostics/`), and the three derived-output subdirectories pending Stage 2 placement.

3. **Read this log entry to orient.**

4. **Check `STANDING_ITEMS.md` for triggered items.** Item 1 (pre-registration reproducibility verification) is triggered by this session's close (Stage 1 complete). Item 2 (push to origin) is eligible by virtue of the closed commit cluster. Whether to fire item 1 before item 2 or vice versa is Mike's arbitration.

5. **First substantive action:** per the trigger ordering Mike arbitrates. The bullet-proof deferral process means item 1 has structural priority (its trigger names item-immediately-following-Stage-1-completion), but Mike's arbitration can sequence them differently if useful.

Standing items spanning sessions: pre-registration reproducibility verification (newly triggered), push to origin (newly eligible), Stages 2-5 execution (sequenced triggers), F multiplicativity commitment verification (independent trigger), `global_timeseries.csv` rename-or-README decision (Stage 2 execution), manuscript implications (Phil's timing independent).

**Foundational set updates this session:** all six foundational documents committed for the first time (pairs 1-3). Root-level orientation committed. STANDING_ITEMS.md committed. Kit-revision-3 committed. Stage 1 substantively complete with this log commit closing the session.

— Drafted by Claude as Layer 1 central node, session 9 end operations log entry, post-Stage-1-substantive-completion, pre-session-10-handoff

---

## Post-commit addendum: prior-cycle canonical material discovered at session close

After the session 9 operations log committed at `ff2704d`, while preparing the session 10 handoff folder, a primary-source check on an unrelated file (`new_claude_primer_distribution_workflow.md`, found at workspace root) surfaced a reference to `protocols/onboarding/`. Verification against primary source (`git ls-tree HEAD -- protocols/onboarding/`) returned four committed canonical files:

- `protocols/onboarding/new_chat_primer.md`
- `protocols/onboarding/chatgpt_new_chat_primer.md`
- `protocols/onboarding/gemini_new_chat_primer.md`
- `protocols/onboarding/chatgpt_routing_note.md`

Provenance verification (`git log --oneline --all -- protocols/onboarding/`) returned two commits both predating `5d91828` (origin/main): `0522639` ("Initial Cycle 1 artifacts: substrate spec v1.1, Mesa setup, cross-instance primers") and `e3d7014` ("Update new_chat_primer.md for Cycle 2 Round 1 post-Flight 2 closure state").

Inspection of the committed `new_chat_primer.md` content (first 30 lines) showed substantial prior-cycle canonical material including: a reading sequence pointing at `operations_log/README.md`, `operations_log/2026-05-14_emulation_discovery.md`, and `operations_log/2026-05-15_flight_2_closure.md`; a "two-paper structure" framing (AMR mean-field foundation paper plus substrate-work paper) not engaged by any session-7-onward canonical material; references to "standing rules 1-4" originating in the May 14 emulation-discovery event (different rule numbering than the current Rule 1-10); references to `protocols/architectural_reviews/2026-05-15_*` as review-template material.

**Implication.** Session 9's Stage 1 work produced `protocols/foundational/` (six canonical documents) and `kit-revision-3` as canonical orientation infrastructure without inventorying pre-existing canonical material at adjacent canonical paths. Both directories now sit at canonical paths in HEAD with no documentation reconciling them; a fresh reader has no way to determine which is current operational truth. This is a Layer-1-specific working-memory instance — Layer 1 enforced primary-source verification discipline on session-7-onward material but did not extend the verification to the pre-existing canonical record at session 9 open. Rule 1 (no complexity floor) and Rule 7.4 (memory-based reconstruction without canonical source verification prohibited symmetrically including for Layer 1) both apply.

**Correction by reframing, not by retroactive completion.** The session 9 operations log claim of "Stage 1 substantively complete" is corrected to "Stage 1 substantively complete *modulo a discovered reconciliation requirement.*" The reconciliation work is too substantial to land within the remaining context-window budget of session 9; attempting it under time pressure would replicate the working-memory failure that produced the gap.

The reconciliation is added to `STANDING_ITEMS.md` as item 9 with explicit trigger: before any other Stage 2 work begins in session 10. The trigger supersedes items 1 (pre-registration reproducibility verification) and 2 (push to origin) because the verification's canonical-record context may depend on prior-cycle material not yet integrated, and push-to-origin should not propagate the current incomplete canonical structure to remote.

**Three Layer-1-specific working-memory instances this session, not two.** The session arc and methodological observations sections of this log undercount: the Open Element 14 vocabulary violation, the session-handoff folder log omission at session open, and the supplementary-note-as-parallel-instantiation-document form failure are noted. The third instance — failure to inventory prior-cycle canonical material before producing parallel canonical material in the same paths-of-concern — is added here for the canonical record. Corrective discipline going forward: at session open, Layer 1's HEAD and working-tree verification must include `git ls-tree HEAD -- <relevant directories>` for any directory where session work will produce new canonical material, regardless of whether the directory appears in the prior session's resume anchor.

**Updated standing items for session 10.** Per `STANDING_ITEMS.md` (now with item 9 added in a follow-up commit), session 10 opens with three triggered items in priority order:

1. Item 9: Prior-cycle canonical material reconciliation (supersedes the trigger order of items 1 and 2)
2. Item 1: Pre-registration reproducibility verification (eligible after item 9 closes)
3. Item 2: Push to origin (eligible after item 9 closes; sequencing relative to item 1 at Mike's arbitration)

**Resume anchor for session 10 (revised).** When this conversation resumes:

1. Verify HEAD; the follow-up commit (this addendum + STANDING_ITEMS.md update) will be the new HEAD, not `ff2704d`.
2. Verify working-tree state.
3. Read this operations log entry (including this addendum) to orient.
4. Check `STANDING_ITEMS.md` for triggered items. Item 9 is the first action.
5. First substantive action: item 9 inventory and reconciliation per the acceptance criteria in `STANDING_ITEMS.md`.

— Addendum drafted by Claude as Layer 1 central node, post-commit at session 9 close, on discovery of the prior-cycle canonical material gap. Honesty-of-record discipline prioritized over end-of-session closure framing.
