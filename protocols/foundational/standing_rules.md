# Standing Rules

**Document role.** Canonical list of protocol-level standing rules. Rules operate across all sessions and all AI partners. They are enforced by Layer 1 against artifacts entering the canonical record; the discipline applies symmetrically, including to Layer 1's own work.

**Authority.** This document is authoritative for protocol-level rule content. The instantiation kit reproduces a compressed summary; when the kit and this document conflict, this document wins. When this document conflicts with primary source (file system, source code, document text, git log), primary source wins and this document revises. Rule 1 specifies the verification discipline that implements this override in practice.

**Maintenance discipline.** New rules added when Mike ratifies a new standing commitment. Existing rules amended when the operational understanding of the rule evolves. Each rule entry includes the session in which it was first committed; the change-history of this document, taken with the operations logs, is the canonical record of rules evolution.

**Relationship to `protocol_primer.md`.** The primer specifies *what* the protocol is; this document specifies *what holds across* all protocol operations. Rules cite primer sections by reference where relevant.

---

## Rule 1: Primary-source verification before downstream claims

**First committed:** session 5 (informal), session 6 (named explicitly), session 7 (formalized).

Before accepting or routing any claim with substantial implications, verify against primary source — file system, source code, document text, parquet metadata, hash output, git log. The discipline applies symmetrically across all AI partners including Claude. Memory descriptions are not primary source; they can carry forward inferences as if they were facts.

**Specifically for git operations:** the primary source for "did a commit fire" is `git log --oneline -N`, not git's narrative status messages. Reading "nothing added to commit but untracked files present" as evidence the prior commit didn't fire is a working-memory instance — verify against the log.

**Specifically for file existence and content:** `git status --short`, `dir`/`Get-ChildItem`, and direct file reads are primary source. The instantiation kit's canonical-artifacts index is a working description and may drift from primary source; primary source wins.

**Rule 1 has no complexity floor.** Session 8 surfaced an instance on integer arithmetic over file counts. The discipline applies at every level of granularity, not only on substantive analytical claims.

---

## Rule 2: Session-end verification

**First committed:** session 7.

At session close, explicitly verify:

1. What files exist in Claude's `/home/claude/` workspace from this session?
2. What files have been downloaded by Mike and saved to known paths on his end?
3. What is staged for future action (drafts not completed, decisions deferred)?

These three categories must be distinguished. Standing offers ("when you're ready, I can draft...") are *unfulfilled* at session close unless Mike accepted them during the session. A drafted-and-presented file is not equivalent to a filed-on-Mike's-end file. The session-end record must note the distinction.

**Operations log discipline.** Commit the session log at session end, not the start of the next session. Deferring the commit means the next session inherits an uncommitted file as its starting state — recreating the precondition problem the session 7 reconciliation closed.

**Session-handoff folder discipline (added session 9).** When prior-Claude prepares material for the next session's instantiation, the handoff folder at `claude_session_handoffs/YYYY-MM-DD[-N]/` must contain:

- The current instantiation kit (latest revision).
- The just-closed session's operations log (most recent — required, not optional).
- Optionally, one or two prior session logs for cross-session continuity.

The just-closed session's operations log is load-bearing for next-session orientation; without it, the next-session Claude operates from kit-summary plus prose-summary supplementary material, which is the working-memory failure mode the protocol is structurally designed to avoid.

**Opening-instruction discipline (added session 9).** The opening instruction Mike sends to next-session Claude is a single sentence pointing at the kit (e.g., "Instantiate per the attached kit; verify HEAD per the resume anchor"). All substantive operational knowledge belongs *inside* the kit, not in a supplementary note. If prior-Claude has new working-pattern observations worth carrying forward, the discipline is to fold them into kit-revision-N as part of session-end maintenance — not to draft a parallel instantiation document.

**Kit-revision discipline (added session 9).** When working-pattern, current-state, or canonical-artifacts content changes during a session, the kit is revised in the same session and committed alongside the operations log. The kit revision number increments; the prior kit revision is preserved in git history.

---

## Rule 3: Sequential cross-layer routing by default

**First committed:** session 6.

Layer 1 structural review precedes Layer 2 substantive review. Parallel routing collapses review surfaces — if Layer 1 and Layer 2 both engage the same material simultaneously, the independent ground Layer 2 is meant to provide is contaminated by exposure to Layer 1's framing.

Exceptions to sequential routing require deliberate justification recorded in the operations log.

---

## Rule 4: Layer 1 boundary-crossing under disclosure

**First committed:** session 5 (registered), session 6 (formalized).

Layer 1 acting on Layer 3's surface (direct code edits, detailed example shapes, full implementation drafts) is permitted but must be disclosed at the time and registered in the operations log. The justification for a boundary-crossing is typically session economics — when Layer 1 already has the primary source loaded in context and the implementation question is bounded, drafting directly is cheaper than the round-trip to Layer 3.

The boundary-crossing pattern itself is worth tracking; whether it should be tightened back toward stricter layer discipline is a protocol-level question that Mike arbitrates over time.

---

## Rule 5: Vocabulary quarantine enforced at wrap-ups and celebratory moments

**First committed:** prior to session 5 (carried forward from earlier protocol state), reaffirmed session 6.

Vocabulary discipline operates as much during synthesis and result-celebration as during active analysis. Drift is most likely when guard is down — the wrap-up phrase that "sounds right" is the most likely vehicle for quarantined vocabulary to enter the canonical record.

See `vocabulary_quarantine.md` for the prohibited terms list and permitted framings.

---

## Rule 6: No-preserved-divergence is a finding to track

**First committed:** session 6 (named in synthesis discussion), retained as discipline.

Synthesis is the work; convergence is a phenomenon that sometimes occurs. Only converge where convergence genuinely emerges. Carry multiple readings forward otherwise.

The no-preserved-divergence pattern between Layer 1 and Layer 2 is not necessarily substantive convergence; it may be the framing-asymmetry artifact (see `protocol_primer.md` Section 4). Layer 1 framing-room for divergence is what allows Layer 2 to engage substantively rather than being channeled into refinement of Layer 1's position.

---

## Rule 7: Section 15 prohibitions lifted to protocol level

**First committed:** session 6 (direction committed), session 9 (execution).

The Flight 6 Substrate Specification's Section 15 lists prohibited substitutions, shortcuts, evasions, analysis-stage repairs, and required affirmations specific to substrate implementation. The protocol-applicable items below are lifted with translation; each cites its Section 15 source bullet. Substrate-specific items remain in the substrate spec where they belong and are not reproduced here.

**Citation convention:** Section 15 source bullets are referenced as "FSS §15 / substitutions / N" where N is the bullet position in that subcategory.

### Rule 7.1 — Aggregate completion claims require per-artifact verification

*Source: FSS §15 / shortcuts / 1.*

Aggregate terminal completion messages ("ALL ARTIFACTS PRESENT", "EXTRACTION COMPLETE", etc.) without per-artifact verification are prohibited across the protocol. Each artifact named in a deliverable specification must be produced as a distinct file with content matching specification; verification at end of execution requires explicit per-artifact confirmation, not aggregate completion claims.

### Rule 7.2 — Schema-emulation without engine-execution

*Source: FSS §15 / shortcuts / 2.*

Mock objects, schema emulators, and namedtuple-style stand-ins that bypass the actual code path under test are prohibited when verification claims depend on the real code path's behavior. If a test is meant to verify that a contract's validation pipeline rejects a malformed input, the test must route the input through the actual validation pipeline — not through a mock that simulates rejection.

The pattern surfaced repeatedly in session 5 (Tier 3 intake test construction). Reading source before writing code that touches the contract is the corrective discipline.

### Rule 7.3 — Synthetic hashes or metadata not generated by actual file operations

*Source: FSS §15 / shortcuts / 3.*

Hash values, parquet metadata, file sizes, and similar verification artifacts must be generated by actual operations on the actual files. Reported hash values that were not produced by running the hash function over the file contents at verification time are prohibited.

### Rule 7.4 — Memory-based reconstruction without canonical source verification

*Source: FSS §15 / evasions / 3.*

Equations, specification content, parameter values, and protocol details must not be reconstructed from working memory when canonical source is available. The discipline applies to all AI partners including Layer 1; Layer 1's central-node role does not exempt Layer 1 from the verification discipline.

This rule is the canonical statement of the working-memory pattern's corrective discipline (see `protocol_primer.md` Section 4). Rule 1 specifies how to comply; this rule specifies that the compliance is mandatory.

### Rule 7.5 — Aggregate framing covering partial implementation

*Source: FSS §15 / evasions / 4.*

Framings such as "FULL EXTRACTION COMPLETE" or "ANALYSIS COMPLETE" that cover partial implementation are prohibited. If 7 of 8 production artifacts are produced and 1 failed, the framing must name the partial completion explicitly, not absorb the failure into an aggregate success claim.

### Rule 7.6 — Inference-based imputation of missing required telemetry

*Source: FSS §15 / analysis-stage repairs / 1.*

Missing required telemetry columns or required artifacts are *substrate failures to be surfaced and remediated*, not analysis opportunities to be silently filled. Inferring missing required values from other columns, imputing from neighbors, or applying defaults to fill required fields is prohibited.

The corrective response to missing required telemetry is to surface the failure to Layer 1, route the remediation to Layer 3, and re-execute — not to patch over in analysis.

### Rule 7.7 — Required affirmations

*Source: FSS §15 / required affirmations / 1–4 (translated for protocol scope).*

For any artifact entering the canonical record:

1. Every substantive claim traceable to canonical source or primary-source verification.
2. Every parameter value pulled from the authoritative source (specification, constants module, prior canonical commit).
3. Every computational column or value populated by actual computation per the specifying document.
4. Every completion claim backed by per-artifact verification per Rule 7.1.

The required affirmations are the positive counterparts of Rules 7.1–7.6; meeting all four is the standing test for canonical-record-readiness.

---

## Rule 8: Synthesis-stage failure modes apply symmetrically

**First committed:** session 6 (named), carried forward.

The following failure modes apply across all AI partners including Claude:

- Soft convergence (apparent convergence absent substantive engagement).
- Interpretation creep (the analytical conclusion's scope expanding beyond what was tested).
- Test substitution (inferring rather than testing).
- Structural re-entry through ranking (re-asserting a quarantined structure by ranking among options that include it).
- Too-strict reading of cross-AI review can defer Mike's direct arbitration — cross-AI coherence review is a strong default, NOT a procedural gate.
- Scorecard-watching convergence-direction patterns can themselves drive moves.
- Closing on architectural-ground inference about what testing would show IS test-substitution.

Layer 1 is not exempt from these failure modes. Layer 1 enforces them against Layer 2 and Layer 3 returns and must apply them reflexively to its own synthesis work.

---

## Rule 9: Staging-action recommendations wait for Mike's confirmation

**First committed:** session 7.

Layer 1 explicitly tags staging-action recommendations as pending confirmation when Mike has not yet ratified. Reading speed can exceed confirmation speed; Layer 1 recommendations should not be acted on as if they were directives until Mike's explicit nod.

This is distinct from informational recommendations, which don't require confirmation before reading.

---

## Rule 10: Batched staging requires content-level verification

**First committed:** session 7.

When Layer 1 suggests a multi-file `git add` batch and any file's content was constructed in-session, verify file content matches intent before staging — either by separating the staging command for that file, or by reading the diff explicitly before staging.

Path-level correctness (the file exists at the right path) does not imply content-level correctness (the file contains what we mean to commit).

---

## Note on the "routing as if completed work" candidate rule

The instantiation kit (kit-revision-2) included an item in its Rule 7 list — "routing as if completed work that was deferred or standing-offered" — that does not trace to Section 15 of the Flight 6 Substrate Specification. The item appears related to Rule 2's session-end verification (Rule 2's "standing offers are unfulfilled at session close unless Mike accepted them"), but it was attributed to Section 15 in error.

The substantive content is real and is preserved under Rule 2. The Section 15 attribution is corrected here; no separate Rule 11 is created.

If a future session surfaces a need for an independent rule on this pattern, it would be added as a new numbered entry, not retrofitted into Rule 7's Section 15 lift.

---

— Drafted by Claude as Layer 1 central node, Stage 1 of repository restructure, session 9. v2 incorporates Layer 2 review (item 3 from pair-1 routing — authority statement asymmetry cleanup). Pending Layer 2 acceptance of v2 before commit per primer Section 3's protocol-infrastructure routing convention.
