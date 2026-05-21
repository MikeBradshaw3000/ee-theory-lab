# Current State

**Document role.** Snapshot of the EE Theory Lab's current phase, latest substantive findings, open items, and next anticipated work. This is the document a fresh Claude instance consults to answer "where are we now?"

**Authority.** This document is authoritative for current-state orientation. When it conflicts with primary source (committed code, operations logs, the actual repository state), primary source wins and this document revises. Per Rule 1, current-state claims should be verified against `git log --oneline` and operational reality before being treated as load-bearing.

**Maintenance discipline.** Updated at session end. Volatile sections (those marked **As of session N**) are rewritten each session; stable structural content (the section headings, what each section tracks) changes only when the protocol's understanding of what's worth tracking evolves.

**Relationship to root-level `CURRENT_STATE.md`.** This document is the foundational-set version, scoped to load-bearing protocol-state material for AI instances and Mike. The root-level `CURRENT_STATE.md` is a higher-level orientation derivative aimed at the same audience but with broader scope (project-level state including manuscript-side context that is not strictly Phase 4B work).

**Relationship to other foundational documents.** This document tracks session-volatile state. For stable theoretical and historical content (Two-paper structure, Four Grand Challenges, Cycle 1/Cycle 2 framework, A3 reference baseline), see `theoretical_context.md`. For operational/environmental detail (workspace paths, Python environment, dependencies, PowerShell hazards), see `environment_reference.md`. For personal-context discipline, see `personal_context.md`. The foundational set's role distinctions are documented at `canonical_artifacts_index.md` Section 9.

---

## Section 1: Current phase

**As of session 16 (2026-05-20):**

Phase 4B repository restructure is substantively complete. Stages 0-4 all closed across sessions 8-14. Stage 5 (resume Phase 4B analytical work) is in progress; item 6 route-selection arbitrated session 15; item 6a pre-registration drafting and Layer 2 full cycle completed session 16; Layer 3 execution routing for item 6a in hand session 16.

Stage sequence (committed session 6; closures committed across sessions 8-14):

- **Stage 0** — Freeze and inventory. **Closed at `1a68ca6`** (session 8).
- **Stage 1** — Add orientation spine (foundational document set, root-level orientation, STANDING_ITEMS.md, kit-revision-3). **Closed at sessions 9-10** with item 9 reconciliation cluster.
- **Stage 2** — Move unambiguous canonical artifacts. **Closed at session 12** (commits `919db5b`, `adfdb28`).
- **Stage 3** — Manifests for parquet outputs. **Closed at session 13** (commit `fc9d4c4`).
- **Stage 4** — Quarantine stale and scratch material. **Closed at session 14** (commit `9944f44`).
- **Stage 5** — Resume Phase 4B analytical work. **In progress** (item 6 route-selection arbitrated session 15; item 6a Phase 4B characterization pre-registration committed session 16 with Layer 2 full cycle clean and Layer 3 execution routing in hand; item 6a closes per acceptance component 7 wording; item 15 added for the Layer 3 execution work that follows).

Session 16 produced the item 6a pre-registration v2 draft pair (YAML + Markdown), full Layer 2 cycle (substantive review producing seven required revisions; v2-acceptance pass returning clean accept), Q1 follow-up substrate verification corroborating the shadow-copy structural claim at the primary-source layer (SHA-256 hashes + flight2_production.py code excerpt), and the Layer 3 execution routing closing item 6a acceptance component 7.

---

## Section 2: Latest substantive finding

**As of session 16 (2026-05-20):**

Three substantive findings are canonical as of session 16:

**Finding 1 — reg_01 identity-recovery (session 6).** Tier 3 reg_01 is substantively complete as a pipeline-validation regression, with the R²=1.000 identity-recovery interpretation verified by primary-source review of the Flight 6 Substrate Specification v1.1 sections 6 and 8. The substrate's deterministic probability chain (Drive_Raw → p_base → p_act → realization) is what reg_01 recovered at machine precision; F_variant and scale enter only indirectly through Term_Lambda. Per the reg_01 pre-registration's own `interpretation_boundary.does_not_adjudicate`, reg_01 does not adjudicate the architectural selection between F_LR and F_2_symmetric for Open Element 14.

**Finding 2 — Item 6 route-selection arbitration (session 15).** F-form adjudication for Open Element 14 has been substantively scoped across three-round Layer 2 engagement plus one Layer 3 substrate-state engagement. The substantive arbitration replaces the five-route articulation (aggregate trajectory comparisons; Ψ-structure analysis; Q-driven base drift; regime-transition timing; repeat-seed designs — committed under item 6 since session 9-10) with a four-way operational structure that distinguishes Phase 4B-compatible work from work outside Phase 4B v1.1's procedural scope:

1. **Phase 4B F-form-relevant characterization** — F-form-relevant macro behavior using substrate-supported aggregate trajectories and transition proxies, mapped primarily to IF1 (F-form × Λ pathway) and IF2 (F-form × density pathway), with IF3 (epoch × F_variant) used only as time/epoch interaction unless Q-form is committed. Tracked as item 6a (closed session 16; execution work is item 15).
2. **Repeat-seed and non-shadow-copied F-form substrate design** — Flight 3a-style substrate work for future variance estimation and cross-probe F_2_symmetric differential analysis. Outside Phase 4B per §7.2 items 1 and 5. Tracked as item 6b.
3. **Ψ/Q-dependent analytical routes** — Deferred until commitments are canonical. Tracked as items 13 (Ψ-operationalization) and 14 (Q-form commitment) with refined component-structure acceptance criteria.
4. **Final Open Element 14 arbitration** — Outside Phase 4B per §7.2 item 5. Waits on sufficient evidence from items 6a (Layer 3 execution outputs via item 15), 6b, 13, 14. Tracked as item 6c.

**Substrate fact load-bearing for finding 2 (shadow-copy structure).** Per Phase 4B v1.1 §13.2 and corroborated by session 16 Q1 follow-up primary-source verification: F_2_symmetric files for probe2_starvation and probe3_fusion_residual are byte-identical shadow copies of probe1_overcrowding. Substrate verification at session 16 confirmed SHA-256 byte-identity (F_2_symmetric three files at hash `5d8f54921b6d91c784e2a1b9c30f81d4a6e8c7104b2a10d9f48123c5a69123b0`; F_LR three files at three distinct hashes) plus `flight2_production.py` execution-loop logic (tuple-length-driven invocation of `make_shadow_copies` for F_2_symmetric configurations only; F_LR bypasses the shadow-copy code path entirely). F-form-by-probe comparisons involving F_2_symmetric shadow-copied files yield zero deltas because the underlying data is the same. This fact constrains the executable surface of any analytical work depending on cross-probe F_2_symmetric differential behavior; item 6a pre-registration's shadow-copy handling rule and data-validity mask structurally restrict analysis to the substrate-distinct probe1_overcrowding partition. Item 6b becomes load-bearing for any future cross-probe F-form adjudication.

**Finding 3 — Item 6a pre-registration committed (session 16).** Pre-registration committed under `phase_4b/pre_registrations/item_6a_f_form_characterization.{yaml,md}` as a Reading A+ document pair with the eight-field YAML schema per Phase 4B v1.1 §4.4 plus a Markdown wrapper providing EDA/confirmatory partition, seven-trigger escalation rule (E1-E7; E7 added v2 per Layer 2 revision 1 catching calibration non-identifiability or degeneracy), and seven `does_not_adjudicate` clauses including the transition-proxy non-equivalence to true regime transition clause (added v2 per Layer 2 revision 2). Primary interactions: IF1 + IF2 (per Mike's session 16 scope arbitration); IF5 added as sensitivity-version (per Mike's arbitration on Layer 2 revision 6, Option B); IF3, IF4, and IF5-primary explicitly excluded with rationale. Outcome variable `logit(p_base)` per §4.1 O2 with deterministic-reconstruction framing (η-floor inversion is a closed-form transformation of substrate variables, not new telemetry; Rule 7 protection per Layer 2 revision 4). Layer 2 full cycle completed clean (substantive review + v2-acceptance). Layer 3 execution routing in hand. Item 6a is the third substantive finding insofar as it commits the canonical pre-registration that frames Phase 4B's F-form characterization work; the *empirical* characterization findings will follow from item 15 execution.

**Phase 4B v1.1 procedural scope.** Phase 4B v1.1 explicitly classifies final F-form arbitration (Open Element 14 selection) as `outside_phase_4b_scope` (§7.2 item 5); the four-way structure aligns item 6c with Phase 4B v1.1's own scope discipline. Items 6a (now closed; succeeded by item 15 for execution) and 13 may produce work within Phase 4B procedures; items 6b, 6c, and 14's architectural commitment component are outside Phase 4B and route through other workstreams.

---

## Section 3: Open items

**As of session 16 (2026-05-20):**

All active deferred items live in `STANDING_ITEMS.md` with explicit trigger conditions and acceptance criteria. Currently open (as of session 16 close):

### Stage 5 items (Phase 4B analytical work resumption)

- **Item 15 — Item 6a Layer 3 execution.** Eligible immediately. Six-component acceptance covering Stage 1 EDA implementation script + execution outputs, EDA→Confirmatory checkpoint (Layer 1 + Layer 2 review with Mike's arbitration), Stage 2 confirmatory implementation script + execution outputs, two-field classification population. Layer 3 produces Stage 1 (EDA) implementation script as first deliverable; Layer 1 pre-execution review; Mike arbitrates execution proceed. Binding EDA→Confirmatory checkpoint enforces Reading A+ structure.
- **Item 6b — Repeat-seed and non-shadow-copied F-form substrate design.** Triggered when future F-form arbitration work requires repeat-seed variance estimation or independent F_2_symmetric probe-differential data. Outside Phase 4B; substrate-generation workstream.
- **Item 6c — Final Open Element 14 arbitration.** Triggered when item 6a Phase 4B characterization is complete (item 15 Layer 3 execution outputs with confirmatory findings) and items 6b, 13, 14 are sufficiently advanced per the evidence basis the arbitration requires.
- **Item 13 — Ψ operationalization commitment.** Three-component acceptance (non-spatial Ψ operationalization; spatial Ψ diagnostics implementation; T2.5 outputs). Triggered when Phase 4B analytical work requires Ψ-structure analysis (likely surfaces during item 15 Layer 3 execution if Ψ-structure is invoked, or during item 6c arbitration if Ψ evidence is load-bearing).
- **Item 14 — Q-form commitment.** Two-component acceptance (Delta-demand analysis basis; Q-form architectural commitment). Triggered when Phase 4B analytical work requires Q-driven base drift analysis or item 6c arbitration requires Q-form evidence.

### Cross-session items

- **Item 7 — F multiplicativity commitment verification.** Independent trigger (v1.5 Overview revision work surfaces from Phil's timeline).
- **Item 10 — ChatGPT and Gemini onboarding under session-9 framework.** Triggered when fresh ChatGPT or Gemini instances are needed for substantive work and prior-cycle primers are inadequate.
- **Item 12 — flight2_outputs naming resolution.** Triggered when substantive operation against `flight2_outputs/` surfaces friction, or when restructure attention returns to top-level directory naming.

### Items closed during session 16

- **Item 6a — Phase 4B F-form-relevant characterization.** All seven acceptance components met: pre-registration v2 draft pair committed using §4.4 schema with v1.1 tier/IF vocabulary (components 1-5); Layer 2 full cycle complete with substantive review (seven revisions integrated, R6 arbitrated by Mike as Option B) plus v2-acceptance clean accept across all five questions (component 6); Layer 3 execution routing in hand (component 7). Q1 follow-up substrate verification corroborated the shadow-copy structural claim at the primary-source layer; escalation rule E4 did not fire. Item 6a closes on component 7's literal wording per Mike's session 16 arbitration; Layer 3 *execution* work becomes new item 15.

### Cross-session items not in STANDING_ITEMS

- **Manuscript implications.** Phil's manuscript work is independent of Phase 4B's analytical phase. Whether and when reg_01 finding, the item 6 route-selection arbitration, and item 6a pre-registration land in the v1.5 Overview is Phil's call.
- **Foundational set maintenance.** Each session-end checks for kit-revision triggers per Rule 2.

---

## Section 4: Next anticipated work

**As of session 16 (2026-05-20):**

Next session (session 17):

- Item 15 Stage 1 (EDA) Layer 3 routing executes: Layer 3 produces Stage 1 implementation script per the session 16 execution routing's specification; Layer 1 pre-execution review of the script; Mike arbitrates execution proceed; Layer 3 executes Stage 1 against F_LR 20×20 and F_2_symmetric 20×20 calibration data; EDA outputs return for the EDA→Confirmatory checkpoint.
- Layer 1 review of EDA outputs against v2 pre-registration specification; Layer 2 review of calibration_locked.yaml if locking succeeded; Mike arbitrates proceed to Stage 2 OR confirm escalation.
- If escalation fires (any of E1-E7 triggers): closure of Stage 1 with escalation report; second confirmatory pre-registration drafting under `phase_4b/pre_registrations/item_6a_f_form_characterization/confirmatory_v2.{yaml,md}` with its own Layer 2 full cycle.

Several sessions out:

- Item 15 Stage 2 (confirmatory) execution: Layer 3 produces Stage 2 implementation script; Layer 1 pre-execution review; Mike arbitrates; Layer 3 executes against F_LR 40×40 and F_2_symmetric 40×40 confirmatory data; primary IF1 + primary IF2 + transition-proxy + cross-scale + IF5 sensitivity regressions plus pre-registered sensitivities; Markdown report + structured CSVs per §4.5.
- Substantive findings from item 15 execution receive two-field classification per Phase 4B v1.1 §6; findings become load-bearing for item 6c arbitration.
- Item 13 work may advance independently (non-spatial Ψ operationalization can be committed without spatial T2.5 implementation; the three components advance in sequence or in parallel per Layer 3 routing capacity).
- Item 14 component 1 (Delta-demand analysis basis) may advance independently (Q-effect decomposition CSV implementation per §3.4); component 2 (Q-form architectural commitment) waits on substantive theoretical work.
- Item 6b substrate work surfaces when item 6c arbitration requires it.
- Items 7, 10, 12 surface per their independent triggers.

Stage 5 (resume Phase 4B analytical work) is in progress; item 6a closure plus Layer 3 execution routing in hand are the second substantive Stage 5 milestones (after session 15's item 6 arbitration); item 15 execution is the next substantive Stage 5 work and the first that produces empirical findings rather than architectural commitments.

---

## Section 5: Working-pattern state

**As of session 16 (2026-05-20):**

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
- **Filename-canonicalization verification.** Session 16 surfaced a guessed-filename propagation pattern: Layer 1's Q1 follow-up routing guessed canonical filenames (`probe3_fusion` vs the actual `probe3_fusion_residual`); Gemini's return corrected; downstream documents would have inherited the guessed names without the verification step. A one-time `Get-ChildItem flight2_outputs/` substrate read early in any session producing canonical-path-referencing artifacts would catch the propagation hazard before it requires correction.
- **Layer 1 → Layer 3 → Layer 2 → Mike sequencing validated.** Session 16's full Layer 2 cycle (substantive review + v2-acceptance) followed the corrected sequencing surfaced in session 15: Layer 3 substrate-state engagement (Q1 routing) preceded Layer 2 substantive engagement; Layer 2 substantive review operated against substrate-verified ground from the start. The convergence to clean v2-acceptance across all five questions with only seven required revisions (vs session 15's three Layer 2 rounds) is consistent with the substrate-grounded-ground efficiency the sequencing was meant to produce. The pattern: substantive arbitrations benefit when Layer 2 sees Layer 3 substrate state in hand at the substantive review's start.
- **Closure on acceptance-component wording per literal reading.** Item 6a's component 7 ("Layer 3 routing in hand for execution against Flight 2 canonical substrate") closed on the routing being drafted, not on execution completing. Pattern: STANDING_ITEMS acceptance criteria's literal wording is binding; closure follows the wording, not paraphrases. The Layer 3 *execution* work becomes a new tracked item (item 15) when the routing-in-hand criterion is met; this preserves both the closure discipline (item 6a closes cleanly) and the operational continuity (item 15 inherits the execution scope).

---

## Section 6: Protocol state

**As of session 16 (2026-05-20):**

- HEAD at session 16 open: `05f06e0` (session 15 closure cluster). Advances through session 16 closure commit cluster.
- Layer assignments: Claude = Layer 1 (central node), ChatGPT = Layer 2 (substantive review), Gemini = Layer 3 (implementation/execution). Mike arbitrates.
- Foundational document set: pairs 1-3 committed during session 9; three new documents (`theoretical_context.md`, `personal_context.md`, `environment_reference.md`) and updates committed during session 10 as part of item 9 reconciliation. This document and STANDING_ITEMS.md updated session 15 absorbing item 6 arbitration and items 13/14 additions; updated session 16 absorbing item 6a closure and item 15 addition.
- Instantiation kit: kit-revision-4 (committed session 14, `06df20d`). Future kit-revision-N anticipated to absorb session 15 working-pattern observations (substrate-state-vs-interpretation framing; substrate-verification-before-Mike-question discipline; Layer 1 → Layer 3 → Layer 2 → Mike sequence; Layer 3 quality-assessment pattern) plus session 16 working-pattern observations (file-contents-default-to-chat-attachment symmetric discipline; sequential Set-Clipboard requires intervening chat paste; routing-package vs artifact-attachment verification; filename-canonicalization verification; Layer 1 → Layer 3 → Layer 2 → Mike sequencing validation; closure on acceptance-component wording per literal reading).
- Routing convention: full Layer 2 cycle for protocol-infrastructure routings includes v2-acceptance pass before commit (per `protocol_primer.md` Section 3); other full-cycle routings commit after Layer 1 incorporation. Session 16 used the protocol-infrastructure routing convention for item 6a pre-registration: substantive review with seven required revisions (R1-R5, R7 mechanical; R6 arbitrated by Mike as Option B); v2-acceptance pass returning clean accept across all five v2-acceptance questions; Layer 1 verified artifact correspondence (R1-R7 present in v2 files) per Layer 2's stated condition for closure.

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

— Drafted by Claude as Layer 1 central node, Stage 1 pair-3 of repository restructure, session 9. v2 incorporates Layer 2 review (Open Element 14 label removed and restated in committed terms; completed Section 15 lift item removed from open items; "confirmed" replaced with "verified by primary-source review"). Session 10 update: Stage-1 framing updated, cross-references to new foundational documents added, session 10 substantive work reflected, session 10 as deliverable 3 of item 9 reconciliation. Session 15 update: item 6 substantive arbitration absorbed (route-selection result; four-way structure replacing five-route articulation; items 6a/6b/6c open; items 13/14 added with refined component-structure acceptance); Stage 4 closure and Stage 5 in-progress reflected; session 15 working-pattern observations folded into Section 5. Session 16 update: item 6a closure absorbed (pre-registration v2 draft pair committed; Layer 2 full cycle clean; Layer 3 execution routing in hand; Q1 follow-up substrate verification corroborating shadow-copy claim); item 15 added for Layer 3 execution work; session 16 working-pattern observations folded into Section 5 (file-contents-default-to-chat-attachment; Set-Clipboard sequencing; routing-package vs artifact-attachment; filename-canonicalization; sequencing validation; literal-wording closure).
