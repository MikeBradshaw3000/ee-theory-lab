# Current State

**Document role.** Snapshot of the EE Theory Lab's current phase, latest substantive findings, open items, and next anticipated work. This is the document a fresh Claude instance consults to answer "where are we now?"

**Authority.** This document is authoritative for current-state orientation. When it conflicts with primary source (committed code, operations logs, the actual repository state), primary source wins and this document revises. Per Rule 1, current-state claims should be verified against `git log --oneline` and operational reality before being treated as load-bearing.

**Maintenance discipline.** Updated at session end. Volatile sections (those marked **As of session N**) are rewritten each session; stable structural content (the section headings, what each section tracks) changes only when the protocol's understanding of what's worth tracking evolves.

**Relationship to root-level `CURRENT_STATE.md`.** This document is the foundational-set version, scoped to load-bearing protocol-state material for AI instances and Mike. The root-level `CURRENT_STATE.md` is a higher-level orientation derivative aimed at the same audience but with broader scope (project-level state including manuscript-side context that is not strictly Phase 4B work).

**Relationship to other foundational documents.** This document tracks session-volatile state. For stable theoretical and historical content (Two-paper structure, Four Grand Challenges, Cycle 1/Cycle 2 framework, A3 reference baseline), see `theoretical_context.md`. For operational/environmental detail (workspace paths, Python environment, dependencies, PowerShell hazards), see `environment_reference.md`. For personal-context discipline, see `personal_context.md`. The foundational set's role distinctions are documented at `canonical_artifacts_index.md` Section 9.

---

## Section 1: Current phase

**As of session 15 (2026-05-20):**

Phase 4B repository restructure is substantively complete. Stages 0-4 all closed across sessions 8-14. Stage 5 (resume Phase 4B analytical work) is the current phase, with item 6 route-selection substantively arbitrated during session 15.

Stage sequence (committed session 6; closures committed across sessions 8-14):

- **Stage 0** — Freeze and inventory. **Closed at `1a68ca6`** (session 8).
- **Stage 1** — Add orientation spine (foundational document set, root-level orientation, STANDING_ITEMS.md, kit-revision-3). **Closed at sessions 9-10** with item 9 reconciliation cluster.
- **Stage 2** — Move unambiguous canonical artifacts. **Closed at session 12** (commits `919db5b`, `adfdb28`).
- **Stage 3** — Manifests for parquet outputs. **Closed at session 13** (commit `fc9d4c4`).
- **Stage 4** — Quarantine stale and scratch material. **Closed at session 14** (commit `9944f44`).
- **Stage 5** — Resume Phase 4B analytical work. **In progress** (item 6 route-selection substantively arbitrated session 15; items 6a/6b/6c open).

Session 15 produced item 6 substantive arbitration across three-round Layer 2 engagement plus one Layer 3 substrate-state engagement; the route-selection result is canonical, items 6a/6b/6c are open with explicit acceptance criteria per STANDING_ITEMS.md. Kit-revision-4 was committed during session 14; session 15 closure cluster commits the item 6 arbitration into the canonical record.

---

## Section 2: Latest substantive finding

**As of session 15 (2026-05-20):**

Two substantive findings are canonical as of session 15:

**Finding 1 — reg_01 identity-recovery (session 6).** Tier 3 reg_01 is substantively complete as a pipeline-validation regression, with the R²=1.000 identity-recovery interpretation verified by primary-source review of the Flight 6 Substrate Specification v1.1 sections 6 and 8. The substrate's deterministic probability chain (Drive_Raw → p_base → p_act → realization) is what reg_01 recovered at machine precision; F_variant and scale enter only indirectly through Term_Lambda. Per the reg_01 pre-registration's own `interpretation_boundary.does_not_adjudicate`, reg_01 does not adjudicate the architectural selection between F_LR and F_2_symmetric for Open Element 14.

**Finding 2 — Item 6 route-selection arbitration (session 15).** F-form adjudication for Open Element 14 has been substantively scoped across three-round Layer 2 engagement plus one Layer 3 substrate-state engagement. The substantive arbitration replaces the five-route articulation (aggregate trajectory comparisons; Ψ-structure analysis; Q-driven base drift; regime-transition timing; repeat-seed designs — committed under item 6 since session 9-10) with a four-way operational structure that distinguishes Phase 4B-compatible work from work outside Phase 4B v1.1's procedural scope:

1. **Phase 4B F-form-relevant characterization** — F-form-relevant macro behavior using substrate-supported aggregate trajectories and transition proxies, mapped primarily to IF1 (F-form × Λ pathway) and IF2 (F-form × density pathway), with IF3 (epoch × F_variant) used only as time/epoch interaction unless Q-form is committed. Tracked as item 6a.
2. **Repeat-seed and non-shadow-copied F-form substrate design** — Flight 3a-style substrate work for future variance estimation and cross-probe F_2_symmetric differential analysis. Outside Phase 4B per §7.2 items 1 and 5. Tracked as item 6b.
3. **Ψ/Q-dependent analytical routes** — Deferred until commitments are canonical. Tracked as items 13 (Ψ-operationalization) and 14 (Q-form commitment) with refined component-structure acceptance criteria.
4. **Final Open Element 14 arbitration** — Outside Phase 4B per §7.2 item 5. Waits on sufficient evidence from items 6a, 6b, 13, 14. Tracked as item 6c.

**Substrate fact load-bearing for finding 2 (shadow-copy structure).** Per Phase 4B v1.1 §13.2 (substrate-designed, not data quality issue): F_2_symmetric files for probe2_starvation and probe3_fusion are byte-identical shadow copies of probe1_overcrowding. F-form-by-probe comparisons involving F_2_symmetric shadow-copied files yield zero deltas because the underlying data is the same. This fact constrains the executable surface of any analytical work depending on cross-probe F_2_symmetric differential behavior; item 6a pre-registration acceptance includes explicit shadow-copy handling rule. Item 6b becomes load-bearing for any future cross-probe F-form adjudication.

**Phase 4B v1.1 procedural scope.** Phase 4B v1.1 explicitly classifies final F-form arbitration (Open Element 14 selection) as `outside_phase_4b_scope` (§7.2 item 5); the four-way structure aligns item 6c with Phase 4B v1.1's own scope discipline. Items 6a and 13 may produce work within Phase 4B procedures; items 6b, 6c, and 14's architectural commitment component are outside Phase 4B and route through other workstreams.

---

## Section 3: Open items

**As of session 15 (2026-05-20):**

All active deferred items live in `STANDING_ITEMS.md` with explicit trigger conditions and acceptance criteria. Currently open (as of session 15 close):

### Stage 5 items (Phase 4B analytical work resumption)

- **Item 6a — Phase 4B F-form-relevant characterization.** Pre-registration drafting under `phase_4b/pre_registrations/` is the next-eligible substantive work. Acceptance covers seven components including the eight-field YAML schema, interpretation_boundary discipline, shadow-copy handling rule, calibration-vs-confirmatory discipline for transition-proxy parameters, substrate-supported comparison scope, Layer 2 full cycle, and Layer 3 routing for execution.
- **Item 6b — Repeat-seed and non-shadow-copied F-form substrate design.** Triggered when future F-form arbitration work requires repeat-seed variance estimation or independent F_2_symmetric probe-differential data. Outside Phase 4B; substrate-generation workstream.
- **Item 6c — Final Open Element 14 arbitration.** Triggered when item 6a is complete and items 6b, 13, 14 are sufficiently advanced per the evidence basis the arbitration requires.
- **Item 13 — Ψ operationalization commitment.** Three-component acceptance (non-spatial Ψ operationalization; spatial Ψ diagnostics implementation; T2.5 outputs). Triggered when Phase 4B analytical work requires Ψ-structure analysis.
- **Item 14 — Q-form commitment.** Two-component acceptance (Delta-demand analysis basis; Q-form architectural commitment). Triggered when Phase 4B analytical work requires Q-driven base drift analysis or item 6c arbitration requires Q-form evidence.

### Cross-session items

- **Item 7 — F multiplicativity commitment verification.** Independent trigger (v1.5 Overview revision work surfaces from Phil's timeline).
- **Item 10 — ChatGPT and Gemini onboarding under session-9 framework.** Triggered when fresh ChatGPT or Gemini instances are needed for substantive work and prior-cycle primers are inadequate.
- **Item 12 — flight2_outputs naming resolution.** Triggered when substantive operation against `flight2_outputs/` surfaces friction, or when restructure attention returns to top-level directory naming.

### Items closed during session 15

- **Item 6 — Stage 5 transition.** Substantively resolved at the route-selection level; replaced by items 6a/6b/6c with explicit acceptance criteria. The four-way structure replaces the five-route articulation as canonical operational framing for F-form work.

### Cross-session items not in STANDING_ITEMS

- **Manuscript implications.** Phil's manuscript work is independent of Phase 4B's analytical phase. Whether and when reg_01 finding and the item 6 route-selection arbitration land in the v1.5 Overview is Phil's call.
- **Foundational set maintenance.** Each session-end checks for kit-revision triggers per Rule 2.

---

## Section 4: Next anticipated work

**As of session 15 (2026-05-20):**

Next session (session 16):

- Item 6a pre-registration drafting against Layer 2 round-3 framing (substrate-supported aggregate trajectories and transition proxies; IF1/IF2 primary mapping; IF3 as time/epoch interaction without Q-form claims; shadow-copy handling; calibration-vs-confirmatory discipline).
- Layer 2 full cycle on the item 6a pre-registration draft (substantive review + v2-acceptance per protocol-infrastructure routing convention).
- Layer 3 routing for execution against Flight 2 canonical substrate.

Several sessions out:

- Item 6a execution: Layer 3 runs the pre-registered analysis; results return to Layer 1 for review; substantive findings receive two-field classification per Phase 4B v1.1 §6.
- Item 13 work may advance independently (non-spatial Ψ operationalization can be committed without spatial T2.5 implementation; the three components advance in sequence or in parallel per Layer 3 routing capacity).
- Item 14 component 1 (Delta-demand analysis basis) may advance independently (Q-effect decomposition CSV implementation per §3.4); component 2 (Q-form architectural commitment) waits on substantive theoretical work.
- Item 6b substrate work surfaces when item 6c arbitration requires it.
- Items 7, 10, 12 surface per their independent triggers.

Stage 5 (resume Phase 4B analytical work) is in progress; the route-selection arbitration is the first substantive Stage 5 work; item 6a pre-registration drafting and execution are the next substantive Stage 5 work.

---

## Section 5: Working-pattern state

**As of session 15 (2026-05-20):**

Working pattern committed in the kit as of kit-revision-4 (session 14). Operational pattern through session 15:

- PowerShell commands delivered one per fenced block; Mike pastes one-click, runs, pastes output back.
- One-click copy panes used only for content Mike will act on (PS commands, messages to other AIs, file content for placement). Informational content (status summaries, file lists, instructions about what to do next) goes in plain text.
- Visual demarcation after PS output: horizontal rule + bold "Response to your output:" label.
- File edits delivered as full-file overwrites; Mike downloads, moves into workspace via PS.
- File-system manipulation defaults to PowerShell (not File Explorer drag).
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

---

## Section 6: Protocol state

**As of session 15 (2026-05-20):**

- HEAD at session 15 open: `622c6a5` (session 14 ops log addendum). Advances through session 15 closure commit cluster.
- Layer assignments: Claude = Layer 1 (central node), ChatGPT = Layer 2 (substantive review), Gemini = Layer 3 (implementation/execution). Mike arbitrates.
- Foundational document set: pairs 1-3 committed during session 9; three new documents (`theoretical_context.md`, `personal_context.md`, `environment_reference.md`) and updates committed during session 10 as part of item 9 reconciliation. This document and STANDING_ITEMS.md updated session 15 absorbing item 6 arbitration and items 13/14 additions.
- Instantiation kit: kit-revision-4 (committed session 14, `06df20d`). Future kit-revision-N anticipated to absorb session 15 working-pattern observations (substrate-state-vs-interpretation framing; substrate-verification-before-Mike-question discipline; Layer 1 → Layer 3 → Layer 2 → Mike sequence; Layer 3 quality-assessment pattern).
- Routing convention: full Layer 2 cycle for protocol-infrastructure routings includes v2-acceptance pass before commit (per `protocol_primer.md` Section 3); other full-cycle routings commit after Layer 1 incorporation. Session 15 used three-round Layer 2 substantive engagement for item 6 arbitration with central-node Layer 1 review between rounds; Layer 3 substrate-state engagement routed Layer 1 → Layer 3 → Layer 1 → Layer 2 → Mike with the central-node discipline preserving review at each transition.

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

— Drafted by Claude as Layer 1 central node, Stage 1 pair-3 of repository restructure, session 9. v2 incorporates Layer 2 review (Open Element 14 label removed and restated in committed terms; completed Section 15 lift item removed from open items; "confirmed" replaced with "verified by primary-source review"). Session 10 update: Stage-1 framing updated, cross-references to new foundational documents added, session 10 substantive work reflected, session 10 as deliverable 3 of item 9 reconciliation. Session 15 update: item 6 substantive arbitration absorbed (route-selection result; four-way structure replacing five-route articulation; items 6a/6b/6c open; items 13/14 added with refined component-structure acceptance); Stage 4 closure and Stage 5 in-progress reflected; session 15 working-pattern observations folded into Section 5.
