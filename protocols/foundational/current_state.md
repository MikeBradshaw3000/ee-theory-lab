# Current State

**Document role.** Snapshot of the EE Theory Lab's current phase, latest substantive findings, open items, and next anticipated work. This is the document a fresh Claude instance consults to answer "where are we now?"

**Authority.** This document is authoritative for current-state orientation. When it conflicts with primary source (committed code, operations logs, the actual repository state), primary source wins and this document revises. Per Rule 1, current-state claims should be verified against `git log --oneline` and operational reality before being treated as load-bearing.

**Maintenance discipline.** Updated at session end. Volatile sections (those marked **As of session N**) are rewritten each session; stable structural content (the section headings, what each section tracks) changes only when the protocol's understanding of what's worth tracking evolves.

**Relationship to root-level `CURRENT_STATE.md`.** This document is the foundational-set version, scoped to load-bearing protocol-state material for AI instances and Mike. The root-level `CURRENT_STATE.md` is a higher-level orientation derivative aimed at the same audience but with broader scope (project-level state including manuscript-side context that is not strictly Phase 4B work).

**Relationship to other foundational documents.** This document tracks session-volatile state. For stable theoretical and historical content (Two-paper structure, Four Grand Challenges, Cycle 1/Cycle 2 framework, A3 reference baseline), see `theoretical_context.md`. For operational/environmental detail (workspace paths, Python environment, dependencies, PowerShell hazards), see `environment_reference.md`. For personal-context discipline, see `personal_context.md`. The foundational set's role distinctions are documented at `canonical_artifacts_index.md` Section 9.

---

## Section 1: Current phase

**As of session 18 (2026-05-21):**

Phase 4B repository restructure substantively complete (Stages 0-4 closed sessions 8-14). Stage 5 (resume Phase 4B analytical work) is in progress; item 6 route-selection arbitrated session 15; item 6a pre-registration drafting and Layer 2 full cycle completed session 16; Layer 3 execution routing for item 6a in hand session 16; item 15 component 1 (Stage 1 EDA implementation script) closed session 17 with v3 committed at `22aedba`; item 15 component 2 (Stage 1 EDA execution) reframed at session 18 — v3.1 defensive execution patch architecturally Layer-2-accepted but execution blocked pending item 12 resolution (substrate path/filename mismatch surfaced during attempted execution).

Stage sequence:

- **Stages 0-4** — closed sessions 8-14 (unchanged from session 16 framing)
- **Stage 5** — In progress (item 6 arbitration session 15; item 6a closure + Layer 3 routing session 16; item 15 component 1 closure session 17 with v3 script committed; item 15 component 2 architectural acceptance + execution-prerequisite friction surfacing session 18)

Session 17 produced the v3 Stage 1 EDA implementation script after full Layer 1 + Layer 2 substantive review cycle (R1-R6 + S1b integrated; Layer 2 v3-acceptance clean). Session 18 produced: routing v1→v2→v2.1→re-route arc for execution component; Layer 3 capability category-error finding (Layer 3 = code generation + analytical synthesis on pasted outputs; NOT local execution); Layer 2 multi-surface review resolving the category-error via five-role protocol taxonomy; v3.1 patch through full review cycle (Layer 3 pre-execution review surfacing two concerns; Layer 1 surfacing a deeper R5-propagation concern; combined v3.1 patch through Gemini production → Layer 2 rejection → revision → Layer 2 clean acceptance); execution attempt revealing path+filename mismatch surfaced as item 12's canonical content; substrate existence verified at out-of-repo path with file signatures consistent with real production but uncertain-trust due to incident-proximity timeframe.

---

## Section 2: Latest substantive finding

**As of session 18 (2026-05-21):**

Five substantive findings canonical:

**Findings 1-3 (reg_01 identity-recovery; Item 6 route-selection arbitration; Item 6a pre-registration committed):** Unchanged from session 16 framing. Reference the session 16 version of this document (in the session 16 ops log / handoff) for full detail. Summary: reg_01 is a pipeline-validation regression recovering the substrate's deterministic probability chain at machine precision, not adjudicating F-form selection; item 6 route-selection replaced the five-route articulation with a four-way operational structure (items 6a/6b/6c + items 13/14); item 6a pre-registration committed under `phase_4b/pre_registrations/item_6a_f_form_characterization.{yaml,md}` as a Reading A+ document pair with eight-field YAML schema, seven-trigger escalation rule, IF1+IF2 primary with IF5 sensitivity. Shadow-copy substrate fact (F_2_symmetric probe2/probe3 byte-identical to probe1) remains load-bearing for finding 2.

**Finding 4 — v3 Stage 1 EDA implementation script committed (session 17).** Script at `phase_4b/scripts/item_6a_stage1_eda.py` (332 lines), commit `22aedba`. v3 after full Layer 1 + Layer 2 review cycle: original Layer 1 routing → Gemini v1 → Layer 1 review surfaced R1/R2a/R3/S1 (R3 sub-option α recommended; S1b for joint perturbations per Mike's pessimistic-on-passing-tests arbitration) → Gemini v2 → Layer 2 consolidated review surfaced R4 (E1/E7 admissibility logic requires crit_3_base_pass not crit_1_base_pass alone), R5 (group rolling-rho by full condition tuple not run_id alone), R6 (avoid implicit tick-contiguity assumption; positional computation Mike-arbitrated as Reading α) plus framing-asymmetry observation on Layer 1's R3 implementation drift → Gemini v3 → Layer 1 review clean → Layer 2 v3-acceptance clean greenlight. Item 15 acceptance component 1 closes. Components 2-6 active.

**Finding 5 — v3.1 defensive execution patch architecturally accepted; execution blocked by item 12 friction (session 18).** Patch covers two changes: required-file assertion preventing false E1 escalation when one parquet file missing; full-condition keying through `base_evals` and perturbation lookup completing R5's pipeline-wide trajectory-isolation invariant (Layer 2 retrospective observation: R5 was closed too locally at `compute_rolling_rho` in session 17). Patch went through Gemini pre-execution review identifying two of three concerns; Layer 1 surfaced deeper R5-propagation concern; Layer 2 multi-surface review recommended combined v3.1 patch; Gemini first v3.1 production partially propagated R5; Layer 2 pre-commit review rejected as incomplete; Gemini revision produced full propagation; Layer 2 acceptance clean greenlight. v3.1 architecturally Layer-2-accepted, not file-committed at session 18 close (content preserved in session 18 chat transcript). Execution blocked operationally by item 12 friction (path+filename mismatch between v3 script's expectations and `flight2_production.py`'s RUNS dictionary outputs at the documented out-of-repo location). Substrate exists at `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` per item 12 canonical content; eight expected files dated 15 May 2026 morning with sizes and timestamps consistent with real production but produced in incident-proximity timeframe — uncertain-trust as authoritative baseline. Layer 3 capability category-error finding (Layer 3 ≠ local execution layer) resolved by Layer 2's five-role protocol taxonomy: Layer 3 implementation; local execution by Mike; Layer 3 output interpretation on pasted artifacts; Layer 1 synthesis/review; Layer 2 substantive review.

Item 15 component 2 forward path: item 12 resolution (substantive operational work) is now Priority 1 for session 19; substrate reproduction-for-authority decision is Priority 2; v3.1 commit decision is Priority 3 (can sequence with or after item 12 resolution); item 15 component 2 execution becomes possible after item 12 resolution; components 3-6 follow.

---

## Section 3: Open items

**As of session 18 (2026-05-21):**

All active deferred items live in `STANDING_ITEMS.md` with explicit trigger conditions and acceptance criteria. Currently open (as of session 18 close):

### Stage 5 items (Phase 4B analytical work resumption)

- **Item 15 — Item 6a Layer 3 execution.** Component 1 closed session 17 (v3 script at `22aedba`). Component 2 status reframed session 18: v3.1 defensive execution patch architecturally Layer-2-accepted (Gemini production → Layer 2 rejection → revision → Layer 2 clean greenlight) but execution blocked operationally by item 12 friction (substrate path+filename mismatch). v3.1 not yet file-committed at session 18 close; Layer 2's recommended commit message: "item15: add defensive Stage 1 EDA execution guards" with note covering required input-file assertion and full-condition trajectory isolation propagation. Components 3-6 sequence after component 2 execution unblocks.
- **Item 12 — flight2_outputs naming resolution.** Trigger met session 18; substrate exists at documented out-of-repo path with all eight expected files; v3 script's path resolution and `DATA_FILES` constant don't align with production script's RUNS dictionary outputs. Priority 1 for session 19 substantive work.
- **Item 6b — Repeat-seed and non-shadow-copied F-form substrate design.** Triggered when future F-form arbitration work requires repeat-seed variance estimation or independent F_2_symmetric probe-differential data. Outside Phase 4B.
- **Item 6c — Final Open Element 14 arbitration.** Triggered when item 6a Phase 4B characterization is complete (item 15 execution outputs) and items 6b, 13, 14 are sufficiently advanced.
- **Item 13 — Ψ operationalization commitment.** Three-component acceptance. Triggered when Phase 4B analytical work requires Ψ-structure analysis.
- **Item 14 — Q-form commitment.** Two-component acceptance. Triggered when Phase 4B analytical work requires Q-driven base drift analysis.

### Cross-session items

- **Item 7 — F multiplicativity commitment verification.** Independent trigger (v1.5 Overview revision work from Phil's timeline).
- **Item 10 — ChatGPT and Gemini onboarding under session-9 framework.** Triggered when fresh ChatGPT or Gemini instances are needed and prior-cycle primers are inadequate. Session 18's prior-Gemini consultation experience confirms this item's substantive content (current Cycle 2 protocol differs materially from prior-cycle Gemini chats; full apprising at chat-open is necessary).
- **Item 12 — flight2_outputs naming resolution.** (Listed under Stage 5 items above; trigger met session 18.)

### Cross-session items not in STANDING_ITEMS

- **Manuscript implications.** Phil's manuscript work is independent of Phase 4B's analytical phase. Whether and when reg_01 finding, the item 6 route-selection arbitration, and item 6a pre-registration land in the v1.5 Overview is Phil's call.
- **Substrate reproduction-for-authority decision.** Session 18 surfaced that existing 15 May 2026 substrate has uncertain-trust due to incident-proximity timeframe. Mike's choice on whether/how to reproduce under current Cycle 2 protocol with full Layer 1/2/3 review discipline. Sequenced with item 12 resolution at session 19.
- **Foundational set maintenance.** Each session-end checks for kit-revision triggers per Rule 2. Session 18 produced multiple kit-revision-N candidate observations (see Section 5).

---

## Section 4: Next anticipated work

**As of session 18 (2026-05-21):**

Next session (session 19):

- **Priority 1: Item 12 resolution.** flight2_outputs naming resolution. Decide target directory name; decide whether substrate moves into repo or stays at parent location; update v3.1 script's `DATA_FILES` constant and path resolution; coordinate with other canonical scripts referencing the location; update `canonical_artifacts_index.md` Section 5; close item 12.
- **Priority 2: Substrate reproduction-for-authority decision.** Existing 15 May files have uncertain authoritative trust. Options: full reproduction under current Cycle 2 protocol with byte-for-byte comparison; accept existing as baseline (lower assurance); mixed approach.
- **Priority 3: v3.1 commit decision.** Layer-2-accepted artifact ready to commit per Layer 2's recommended message; v3.1 content in session 18 chat transcript; sequencing relative to items 12 and reproduction is Mike's call.
- **Priority 4: Item 15 component 2 execution.** Possible after Priority 1; possibly after Priority 2 depending on substrate trust resolution.
- **Priority 5: STANDING_ITEMS independent-trigger check.** Items 6b/6c/7/10/13/14 carried from session 18.

Several sessions out:

- Item 15 components 3-6 execution and review (unchanged from session 16 framing once execution unblocks).
- Item 13/14 may advance independently per their triggers.
- Items 6b, 6c surface per their triggers.
- Item 7 surfaces per Phil's manuscript timeline.

Stage 5 (resume Phase 4B analytical work) remains in progress; item 12 resolution and substrate reproduction-for-authority are the immediate session 19 substantive milestones; item 15 component 2 execution downstream of both.

---

## Section 5: Working-pattern state

**As of session 18 (2026-05-21):**

Working pattern committed in the kit as of kit-revision-4 (session 14). Operational pattern through session 16:

- PowerShell commands delivered one per fenced block; Mike pastes one-click, runs, pastes output back.
- One-click copy panes used only for content Mike will act on (PS commands, messages to other AIs, file content for placement). Informational content (status summaries, file lists, instructions about what to do next) goes in plain text.
- Visual demarcation after PS output: horizontal rule + bold "Response to your output:" label.
- File edits delivered as full-file overwrites; Mike downloads, moves into workspace via PS.
- File-system manipulation defaults to PowerShell (not File Explorer drag).
- File contents → chat context: chat UI attachment (one-step drag or button); PS-clipboard pattern (`Get-Content | Set-Clipboard` + chat paste) available but is two thumb-steps with sequence-discipline risk if multiple files (the two `Set-Clipboard` invocations must be separated by chat paste to avoid clipboard clobber).
- Multi-file `present_files` delivery: Mike prefers separate-file downloads; Claude makes separate `present_files` calls.
- For substantial multi-file reads, concatenation-via-PowerShell into a single bundle file for one upload is preferred to many separate uploads.
- Session-handoff folder: `claude_session_handoffs/YYYY-MM-DD[-N]/` contains the kit and the just-closed session's operations log.
- Opening instruction to next-session Claude is a single sentence pointing at the kit; substantive operational knowledge belongs inside the kit.
- Session-open verification (added session 10): `git ls-tree HEAD -- <relevant directories>` for any directory where session work will produce new canonical material.
- Kit-location verification at session open (added session 14, kit-revision-4 §7): primary-source check of kit revision location (workspace root + handoff folder copies); distinguish `git status --short` (changes only) from `Get-ChildItem` (existence).
- Kit-revision-4 §3 (added session 14): paste-truncation sub-discipline for batched `Move-Item` arrays; enumerate-don't-pattern-match for working-tree contents; `git add -A` scope hazard.
- Kit-revision-4 §8 (added session 14): prose-framing-vs-STANDING_ITEMS hazard.

### Working-pattern observations from session 15 (folding into kit-revision-N):

- **Substrate-state-vs-interpretation framing-mitigation self-correction.** Multi-round Layer 2 engagement on item 6 produced multiple instances of Layer 1 framing trying to proceed past substrate verification; the discipline caught each. Pattern: Layer 1's working memory produces coherent framings that occupy space between known facts; Rule 1 substrate verification before downstream claims catches the drift symmetrically including Layer 1.
- **Substrate-verification-before-Mike-question discipline.** Two instances in session 15 where Layer 1 routed a substrate question to Mike when canonical record (operations logs) was the authoritative source. The corrective: substrate questions about commitment events route to operations logs first; Layer 3 substrate-state engagement for substrate observability; Mike's input is authoritative for arbitration but not substrate for commitment events.
- **Articulation-gap surfacing pattern.** Discovered inconsistency between STANDING_ITEMS item 6 / current_state.md Section 2 (five-route articulation) and Phase 4B Specification v1.1 (F-form arbitration outside_phase_4b_scope) surfaced during Layer 1 substrate read in preparation for pre-registration drafting. Pattern: cross-document substrate reads at key transitions catch un-reconciled framings before they become operational.
- **Layer 3 engagement-frequency observation.** Session 15 was the first Layer 3 routing in 5+ sessions. Prior Layer 3 underuse was a deliberate response to a substrate condition (Gemini in fast mode produced errors); that substrate condition has changed (Gemini Pro at full capacity), but the engagement discipline persisted from when it was correct. Future kit-revision-N: substantive arbitrations benefit from Layer 1 → Layer 3 → Layer 2 → Mike sequence (substrate-state-before-substantive-engagement) rather than Layer 1 → Layer 2 → Mike default.
- **Layer 3 quality-assessment pattern.** Layer 1 review of Layer 3 returns produces framing-correction value (Gemini's "Data Quality Flag" framing on shadow-copy structure was corrected by Layer 1 to "substrate-designed constraint" per FSS §13.2 primary source; minor implementation-tilt observations also surfaced). The central-node Layer 1 review discipline established when Gemini was in fast mode continues to add value with Gemini at full capacity.
- **Multi-round Layer 2 engagement productivity.** Three Layer 2 rounds plus one Layer 3 round produced substantively converged framing with substrate-grounded specificity (transition-proxy candidates; IF1/IF2/IF3 translation mapping; item 6 split structure; refined items 13/14 acceptance). The convergence pattern across rounds rested on substrate verification at multiple layers, not on iterative refinement of Layer 2 framing alone.

### Working-pattern observations from session 16 (folding into kit-revision-N):

- **File-contents-default-to-chat-attachment (symmetric to file-system-defaults-to-PowerShell).** Session 16 surfaced an asymmetry in the thumb-economy principle: file-system operations (moves, commits, status checks) default to PowerShell because PS is one-click for those operations; but for getting file contents into chat context, the chat UI's attachment is one thumb-step, while `Get-Content | Set-Clipboard` + chat paste is two thumb-steps with sequence-discipline risk. The kit-revision-4 file-system-defaults-to-PowerShell discipline should be paired with a symmetric file-contents-default-to-chat-attachment discipline.
- **Sequential Set-Clipboard requires intervening chat paste.** When PS-clipboard pattern IS used for multiple files (e.g., sequential `Get-Content | Set-Clipboard` for two files in one PS turn), the two PS commands must be separated by a chat-paste step or the second clobbers the first. The protocol failure mode: Layer 1 issues both PS commands without waiting for the intervening paste; Mike runs both; the first file's contents are lost from clipboard before they reach chat. Recovery is non-destructive (re-run the lost command) but adds round-trips.
- **Routing-package representation vs artifact attachment.** Two consecutive Layer 2 routings (substantive review, v2-acceptance) returned with the explicit boundary observation that Layer 2 was reviewing the routing-package representation of the draft rather than the actual artifact text. Layer 2's discipline of explicitly flagging the boundary is correct and load-bearing; Layer 1's discipline gap was structuring the routing as if attachments had reached Layer 2 when they had not. Worth registering for kit-revision-N: routing packages that reference attached artifacts should explicitly verify attachment delivery (the attachment is the load-bearing content; the routing markdown is the framing wrapper) or substitute attachment with paste-into-routing when the artifact is short enough.
- **Filename-canonicalization verification.** Session 16 surfaced a guessed-filename propagation pattern: Layer 1's Q1 follow-up routing guessed canonical filenames (`probe3_fusion` vs the actual `probe3_fusion_residual`); Gemini's return corrected; downstream documents would have inherited the guessed names without the verification step. A one-time `Get-ChildItem flight2_outputs/` substrate read early in any session producing canonical-path-referencing artifacts would catch the propagation hazard before it requires correction. (Session 18 note: this exact hazard recurred at scale — the v3 script's DATA_FILES constant inherited guessed filenames that don't match production output; see item 12.)
- **Layer 1 → Layer 3 → Layer 2 → Mike sequencing validated.** Session 16's full Layer 2 cycle (substantive review + v2-acceptance) followed the corrected sequencing surfaced in session 15: Layer 3 substrate-state engagement (Q1 routing) preceded Layer 2 substantive engagement; Layer 2 substantive review operated against substrate-verified ground from the start. The convergence to clean v2-acceptance across all five questions with only seven required revisions (vs session 15's three Layer 2 rounds) is consistent with the substrate-grounded-ground efficiency the sequencing was meant to produce. The pattern: substantive arbitrations benefit when Layer 2 sees Layer 3 substrate state in hand at the substantive review's start.
- **Closure on acceptance-component wording per literal reading.** Item 6a's component 7 ("Layer 3 routing in hand for execution against Flight 2 canonical substrate") closed on the routing being drafted, not on execution completing. Pattern: STANDING_ITEMS acceptance criteria's literal wording is binding; closure follows the wording, not paraphrases. The Layer 3 *execution* work becomes a new tracked item (item 15) when the routing-in-hand criterion is met; this preserves both the closure discipline (item 6a closes cleanly) and the operational continuity (item 15 inherits the execution scope).

### Working-pattern observations from session 17 (folding into kit-revision-N):

- **Multi-cycle Layer 1 + Layer 2 + Layer 3 review for substantive implementation artifacts produces convergent quality.** Item 15 component 1's v1 → v2 → v3 cycle (Layer 1 review surfacing R1/R2a/R3/S1; Layer 2 review surfacing R4/R5/R6 plus R3-drift framing-asymmetry observation; Layer 2 v3-acceptance clean) demonstrates the pattern works for first-time implementation production. Future kit-revision-N: substantive implementation scripts benefit from at least one full Layer 1 → Layer 3 → Layer 2 cycle plus a v-acceptance pass before commit.
- **Closure-by-acceptance-component-wording (cont.).** Item 15 acceptance component 1 closed session 17 on literal wording ("Stage 1 EDA implementation script committed under `phase_4b/scripts/`"); closure does not include component 1's execution path. Pattern carries from session 16's item 6a component 7 closure: STANDING_ITEMS acceptance criteria's literal wording is binding.
- **No-preserved-divergence pattern as framing-independence finding.** Session 17's Layer 1 → Layer 2 cycle on the v3 script closed with the R4-R6 divergences converged through substantive engagement (Layer 2's R5 caught a real grouping error; R4 caught a real admissibility-logic error; R6 caught a real tick-contiguity assumption). Layer 2's framing-asymmetry observation flagged that the convergence was substantive (real errors fixed), not refinement-driven funnel convergence. (Session 18 note: R5 propagation turned out incomplete even after session 17's convergence — see Finding 5 / §4 of session 18 ops log — which is itself evidence that the session-17 convergence closed R5 too locally.)

### Working-pattern observations from session 18 (folding into kit-revision-N):

- **One-click affordance for all Claude output (extension of file-contents-default-to-chat-attachment).** Beyond chat attachment for file contents, the broader principle: anything Claude produces that Mike might want to copy needs single-click affordance. Manual find-and-replace operations, prompt-prefix inclusion in fenced code blocks, and inline code commands all force expensive thumb work (cursor placement, sweep-select, stop-at-correct-character) onto Mike. Discipline: no placeholder templates requiring manual integration; no prompt-prefix in fenced code blocks; no inline code commands; complete integrated documents in chat; full-file downloads for substantial new/replaced content, append-blocks for purely additive changes.
- **Primary-source re-grounding discipline.** When routing or reviewing primary-source-dependent content (script structure, pre-registration structure, file paths, file locations, STANDING_ITEMS canonical content), Layer 1 must inspect primary artifact or explicitly mark description as unverified. Five recurrences in session 18 surfaced different aspects of the same pattern: v1 routing's five primary-source-dependent failures (Layer 2 caught); Reading α/γ drift on R5 propagation completion (Layer 2 caught at pre-commit review); substrate-uncertainty narrative outpacing diagnostic data (Mike caught); prior-Gemini Pro-mode response read under current-protocol assumptions (Mike caught); compressed-memory framing on substrate state when item 12 canonically documented the location (surfaced only when STANDING_ITEMS pulled as primary source).
- **AI Layer capability-surface awareness (Layer 2's five-role taxonomy).** Layer 3 = code-generation + analytical-synthesis-on-pasted-outputs; NOT local execution. The Layer 1/2/3 protocol structure had been mis-routing execution work to Layer 3 when local execution belongs to Mike. Layer 2's resolution: (1) Layer 3 implementation = Gemini writes/revises code; (2) local execution = Mike or local environment runs code; (3) Layer 3 output interpretation = Gemini analyzes pasted logs/artifacts; (4) Layer 1 synthesis/review = Claude integrates into canonical record; (5) Layer 2 substantive review = ChatGPT checks framing, architecture, implementation logic. Future kit-revision-N: roles named explicitly per this taxonomy.
- **Cross-cycle architectural awareness at instantiation.** Kit-revision-4 instantiation produced Claude (ABM 14) without Cycle 1 → Cycle 2 transition framing context, without standing rule #6 surfaced (committed `0c1a98f` 16 May 2026), and without STANDING_ITEMS.md primary-source consultation as default. Session 18 demonstrated that operating without this cross-cycle context produces avoidable framing failures. Kit-revision-N candidate: kit should instantiate Claude with multi-session/cross-cycle context including rule #6, the Cycle 1/Cycle 2 transition framing, the fabrication-failure-mode disciplines, and STANDING_ITEMS.md primary-source consultation discipline.
- **Pessimistic-on-passing-claims for substrate verification.** Verification reports in canonical record do not by themselves attest to real execution; their existence is necessary but not sufficient. Session 18's substrate verification required file-signature analysis (sizes, timestamps, shadow-copy structure) plus realistic execution-time signature (23-min F_LR 40×40 run inconsistent with fabrication) plus prior-Gemini consultation as a separate evidence path, not just analytical-output existence in canonical record.
- **STANDING_ITEMS.md as first-consultation surface.** Layer 1 should consult STANDING_ITEMS.md at session open (per kit's resume-anchor discipline) for any items whose trigger condition might be met by current state. Session 18 demonstrated that item 12 (canonical since session 14, documenting the substrate's exact out-of-repo location) was relevant from session 18 open but only surfaced 3+ hours in when STANDING_ITEMS was pulled for closure cluster drafting.
- **Rapid-reframe-iteration pattern.** Layer 1 producing multiple successive reframes on a substantive question without stable substrate-grounded ground generates drift rather than convergence. Session 18 had four+ reframes on the substrate-trust question, each correcting for something Layer 1 missed in the prior, with the sequence producing accumulating ground-uncertainty until file-evidence provided stable ground. Discipline: when Layer 1 is iterating reframes, slow down to substrate-grounded ground rather than producing another reframe.
- **AI-instance-state visibility.** Mike's correction on prior-Gemini Pro vs fast mode surfaced that AI Layer state (which mode an instance is operating in) is a first-class operational variable. The Layer 1/2/3 protocol's downstream disciplines (rule #6 orientation, primary-source verification) operate on the assumption that the AI Layer is in a known state; when the state can shift silently, downstream disciplines lose substrate-ground. Kit-revision-N candidate or STANDING_ITEMS protocol update: AI Layer state should be explicitly verifiable at routing time, not assumed.

---

## Section 6: Protocol state

**As of session 18 (2026-05-21):**

- HEAD at session 17 close: `ddea343` (session 17 closure cluster). HEAD at session 18 close: [to be filled after closure cluster commits; left self-referential per Mike's arbitration — session 19 verifies live via `git rev-parse HEAD`].
- Layer assignments: Claude = Layer 1 (central node), ChatGPT = Layer 2 (substantive review), Gemini = Layer 3 (implementation). Mike arbitrates. Refined by session 18: Layer 3 ≠ local execution layer. Layer 2's five-role taxonomy is the canonical resolution (Layer 3 implementation; local execution by Mike; Layer 3 output interpretation on pasted artifacts; Layer 1 synthesis/review; Layer 2 substantive review).
- Foundational document set: unchanged structurally; current_state.md and STANDING_ITEMS.md updated session 18 absorbing item 15 component 1 closure (session 17), v3.1 patch arc (session 18), item 12 trigger surfacing (session 18), and substrate finding characterization (session 18).
- Instantiation kit: kit-revision-4 (committed session 14, `06df20d`). Kit-revision-N anticipated to absorb session 15-18 working-pattern observations, including:
  - Sessions 15-16: substrate-state-vs-interpretation framing; substrate-verification-before-Mike-question discipline; Layer 1 → Layer 3 → Layer 2 → Mike sequence; Layer 3 quality-assessment pattern; file-contents-default-to-chat-attachment; sequential Set-Clipboard discipline; routing-package vs artifact-attachment verification; filename-canonicalization verification; sequencing validation; literal-wording closure.
  - Session 17: multi-cycle Layer 1/2/3 review producing convergent quality on first-time implementation; closure-by-acceptance-component-wording (cont.); no-preserved-divergence as framing-independence finding.
  - Session 18: one-click affordance for all Claude output (extension); primary-source re-grounding discipline; AI Layer capability-surface awareness (Layer 2's five-role taxonomy); cross-cycle architectural awareness at instantiation (including rule #6, fabrication-failure-mode disciplines, STANDING_ITEMS first-consultation surface); pessimistic-on-passing-claims for substrate verification; rapid-reframe-iteration pattern discipline; AI-instance-state visibility as first-class operational variable.
- Routing convention: full Layer 2 cycle for protocol-infrastructure routings includes v2-acceptance pass before commit (per `protocol_primer.md` Section 3); other full-cycle routings commit after Layer 1 incorporation. Session 18 session-validated the pattern of pre-routing review (Layer 1 → Layer 2 review of routing package → Layer 3 receives) for execution and implementation-revision routings.

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

— Drafted by Claude as Layer 1 central node, Stage 1 pair-3 of repository restructure, session 9. v2 incorporates Layer 2 review (Open Element 14 label removed and restated in committed terms; completed Section 15 lift item removed from open items; "confirmed" replaced with "verified by primary-source review"). Session 10 update: Stage-1 framing updated, cross-references to new foundational documents added, session 10 substantive work reflected, session 10 as deliverable 3 of item 9 reconciliation. Session 15 update: item 6 substantive arbitration absorbed (route-selection result; four-way structure replacing five-route articulation; items 6a/6b/6c open; items 13/14 added with refined component-structure acceptance); Stage 4 closure and Stage 5 in-progress reflected; session 15 working-pattern observations folded into Section 5. Session 16 update: item 6a closure absorbed (pre-registration v2 draft pair committed; Layer 2 full cycle clean; Layer 3 execution routing in hand; Q1 follow-up substrate verification corroborating shadow-copy claim); item 15 added for Layer 3 execution work; session 16 working-pattern observations folded into Section 5 (file-contents-default-to-chat-attachment; Set-Clipboard sequencing; routing-package vs artifact-attachment; filename-canonicalization; sequencing validation; literal-wording closure). Session 18 update (absorbing session 17 + session 18): item 15 component 1 closure (session 17, v3 script at `22aedba`) reflected in new Finding 4; v3.1 patch arc, Layer 3 capability category-error, item 12 trigger-met, and substrate-finding characterization (session 18) reflected in new Finding 5 and Sections 1/3/4/6; session 17 and session 18 working-pattern observations folded into Section 5.
