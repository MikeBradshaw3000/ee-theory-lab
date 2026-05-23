# Current State

**Document role.** Snapshot of the EE Theory Lab's current phase, latest substantive findings, open items, and next anticipated work. This is the document a fresh Claude instance consults to answer "where are we now?"

**Authority.** This document is authoritative for current-state orientation. When it conflicts with primary source (committed code, operations logs, the actual repository state), primary source wins and this document revises. Per Rule 1, current-state claims should be verified against `git log --oneline` and operational reality before being treated as load-bearing.

**Maintenance discipline.** Updated at session end. Volatile sections (those marked **As of session N**) are rewritten each session; stable structural content (the section headings, what each section tracks) changes only when the protocol's understanding of what's worth tracking evolves.

> **⚠ SESSION-23 SURGICAL-UPDATE NOTICE (sessions 19–22 gap NOT backfilled).** This document was stamped "As of session 18" through session 22 — sessions 19, 20, 21, and 22 never updated it. Session 23 applied a **surgical** update (Mike's arbitration, Option A): it absorbs the session-23 fabrication-family **determination** (new Finding 6; the session-16 claim flagged contradicted in Section 2; item 16 in Section 3; protocol-state current in Section 6) but does **NOT** backfill the full 19–22 narrative. Specifically NOT yet reflected here as full findings: kit-revision-5.1's Layer 2 acceptance pass and the footer-corruption near-miss (session 20); the three-layer extractor-origin trace (sessions 21–22). Those live in the session 19/20/21/22 ops logs as primary source. Full reconciliation is tracked as **STANDING_ITEMS item 17**. Until item 17 closes, treat Sections 1/2/4/5 as session-18-current except where a session-23 marker appears.

**Relationship to root-level `CURRENT_STATE.md`.** This document is the foundational-set version, scoped to load-bearing protocol-state material for AI instances and Mike. The root-level `CURRENT_STATE.md` is a higher-level orientation derivative aimed at the same audience but with broader scope (project-level state including manuscript-side context that is not strictly Phase 4B work).

**Relationship to other foundational documents.** This document tracks session-volatile state. For stable theoretical and historical content (Two-paper structure, Four Grand Challenges, Cycle 1/Cycle 2 framework, A3 reference baseline), see `theoretical_context.md`. For operational/environmental detail (workspace paths, Python environment, dependencies, PowerShell hazards), see `environment_reference.md`. For personal-context discipline, see `personal_context.md`. The foundational set's role distinctions are documented at `canonical_artifacts_index.md` Section 9.

---

## Section 1: Current phase

**As of session 18 (2026-05-21); partial session-23 markers below.**

Phase 4B repository restructure substantively complete (Stages 0-4 closed sessions 8-14). Stage 5 (resume Phase 4B analytical work) is in progress; item 6 route-selection arbitrated session 15; item 6a pre-registration drafting and Layer 2 full cycle completed session 16; Layer 3 execution routing for item 6a in hand session 16; item 15 component 1 (Stage 1 EDA implementation script) closed session 17 with v3 committed at `22aedba`; item 15 component 2 (Stage 1 EDA execution) reframed at session 18 — v3.1 defensive execution patch architecturally Layer-2-accepted but execution blocked pending item 12 resolution (substrate path/filename mismatch surfaced during attempted execution).

> **Session-23 update.** Stage 5 analytical execution is **blocked** and the reason is no longer merely operational (item 12 friction). Sessions 20–23 established a canonical-record integrity finding and, session 23, **determined** it: the session-16 SHA-256 verification claim that the item-6a pre-registration leaned on is a fabrication-family event (see Finding 6, item 16). Item 15 component 2's declared input data set cannot be assembled from the substrate (no F_LR `probe1_overcrowding` file exists). Analytical execution does not resume until item 16's E4 remediation settles the pre-reg scope.

Stage sequence:

- **Stages 0-4** — closed sessions 8-14 (unchanged from session 16 framing)
- **Stage 5** — In progress but blocked behind item 16 E4 remediation (session 23). (Item 6 arbitration session 15; item 6a closure + Layer 3 routing session 16; item 15 component 1 closure session 17; item 15 component 2 architectural acceptance + execution-prerequisite friction session 18; integrity cascade + determination sessions 20–23.)

Session 17 produced the v3 Stage 1 EDA implementation script after full Layer 1 + Layer 2 substantive review cycle (R1-R6 + S1b integrated; Layer 2 v3-acceptance clean). Session 18 produced: routing v1→v2→v2.1→re-route arc for execution component; Layer 3 capability category-error finding (Layer 3 = code generation + analytical synthesis on pasted outputs; NOT local execution); Layer 2 multi-surface review resolving the category-error via five-role protocol taxonomy; v3.1 patch through full review cycle; execution attempt revealing path+filename mismatch surfaced as item 12's canonical content; substrate existence verified at out-of-repo path with file signatures consistent with real production but uncertain-trust due to incident-proximity timeframe.

---

## Section 2: Latest substantive finding

**As of session 18 (2026-05-21); Finding 6 added session 23.**

Six substantive findings canonical (Findings 1–5 as of session 18; Finding 6 session 23):

**Findings 1-3 (reg_01 identity-recovery; Item 6 route-selection arbitration; Item 6a pre-registration committed):** Unchanged from session 16 framing. Reference the session 16 version of this document (in the session 16 ops log / handoff) for full detail. Summary: reg_01 is a pipeline-validation regression recovering the substrate's deterministic probability chain at machine precision, not adjudicating F-form selection; item 6 route-selection replaced the five-route articulation with a four-way operational structure (items 6a/6b/6c + items 13/14); item 6a pre-registration committed under `phase_4b/pre_registrations/item_6a_f_form_characterization.{yaml,md}` as a Reading A+ document pair with eight-field YAML schema, seven-trigger escalation rule, IF1+IF2 primary with IF5 sensitivity.

> **Session-23 correction to Finding 2's load-bearing premise.** Finding 2 (and the item-6a pre-registration §7) recorded the F_2_symmetric shadow-copy fact as corroborated by a session-16 SHA-256 analysis. That SHA-256 corroboration is **determined a fabrication-family event** (session 23; Finding 6, item 16). The **shadow-copy structure itself remains real** — independently confirmed in producer code (sessions 21–22) and by the session-20 hashing (two byte-identical F2sym groups of three). What is contradicted is the SHA *verification* as recorded and the **F_LR per-probe distinct-hash claim** (no F_LR probe1/probe3 file exists; the producer writes none). So Finding 2's substantive claim (shadow-copy substrate fact) stands on other evidence; its recorded SHA-256 corroboration does not.

**Finding 4 — v3 Stage 1 EDA implementation script committed (session 17).** Script at `phase_4b/scripts/item_6a_stage1_eda.py` (332 lines), commit `22aedba`. v3 after full Layer 1 + Layer 2 review cycle (R1/R2a/R3/S1 → v2; R4/R5/R6 → v3; Layer 2 v3-acceptance clean). Item 15 acceptance component 1 closes. Components 2-6 active at session 18 (component 2 later blocked — see Finding 6 / Section 3).

**Finding 5 — v3.1 defensive execution patch architecturally accepted; execution blocked by item 12 friction (session 18).** Patch covers required-file assertion (preventing false E1 escalation) and full-condition keying through `base_evals` and perturbation lookup (completing R5's pipeline-wide trajectory-isolation invariant). Layer-2-accepted, not file-committed at session 18 close (content in session 18 transcript). Execution blocked operationally by item 12 friction. Substrate exists at `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\`; eight files dated 15 May 2026 with signatures consistent with real production but produced in incident-proximity timeframe — uncertain-trust as authoritative baseline. Layer 3 capability category-error resolved by Layer 2's five-role taxonomy.

**Finding 6 — Session-16 SHA-256 verification claim determined a fabrication-family event (session 23, Mike's arbitration).** The session-16 ops log (arc step 14) recorded a Q1-follow-up substrate verification — "F_LR probe1/2/3 three distinct SHA-256 hashes; F_2_symmetric three identical, value `5d8f5492…`" — originating as a **Layer 3 (Gemini) return accepted by Layer 1 without Mike-execution** in the incident-proximity window. Session 20's verification cascade (parquet schema read → pre-reg pull → E4 → SHA-256 → timestamp) contradicted it on **three independent measures**: **count** (two F_LR files exist/are producible, both `probe2_starvation_FLR`, no probe1/probe3, producer writes none); **hash value** (recorded F2sym `5d8f5492…` ≠ real `5d8f5496…`, SHA-256 deterministic); **timestamp** (15-May files unchanged after the 20-May claim, regeneration ruled out). Sessions 21–22 established the claim does not trace to any consumer/extractor script and characterized the §14 record as a Layer-1 paraphrase of the Gemini return. Session 23 read the session-16 and session-20 primary records, ran two Layer 2 routings, closed the last benign residual (Mike: no other production pass generated three F_LR files), and Mike made the determination. **Subtype: verification-dressing over a real structural fact** — the F2sym shadow-copy structure is genuine; the SHA verification form and F_LR per-probe structure were not produced by any computation that occurred. **Caught by the protocol's own verification apparatus** (the session-20 cascade), not by external chance. Remediation tracked as STANDING_ITEMS item 16 (downstream-claims review scoped to a future session; E4 remediation and formal protocol-record register open at Mike's arbitration).

---

## Section 3: Open items

**As of session 18 (2026-05-21); items 16/17 and block-status added session 23.**

All active deferred items live in `STANDING_ITEMS.md` with explicit trigger conditions and acceptance criteria. Currently open (session-23 view):

### Stage 5 items (Phase 4B analytical work resumption)

- **Item 15 — Item 6a Layer 3 execution.** Component 1 closed session 17 (`22aedba`). **Component 2 BLOCKED (session 20, confirmed session 23)** behind item 16's E4 remediation — its declared input data set cannot be assembled (no F_LR `probe1_overcrowding`). v3.1 patch remains Layer-2-accepted, uncommitted, and downstream of the pre-reg remediation. Components 3-6 follow component 2.
- **Item 16 — Session-16 fabrication-family event remediation (NEW, session 23).** Determination made (component 1 met). Component 2 (downstream session-16-era-claims review) scoped to a future session. Component 3 (E4 remediation A vs B) and component 4 (formal protocol record) open at Mike's arbitration. Blocks item 12 and item 15 component 2.
- **Item 12 — flight2_outputs naming resolution.** Recharacterized session 20 (not a rename — consumer-adapter + pre-reg-scope problem); re-blocked session 23 behind item 16's E4-remediation component.
- **Item 6b — Repeat-seed and non-shadow-copied F-form substrate design.** Trigger unmet. Outside Phase 4B.
- **Item 6c — Final Open Element 14 arbitration.** Trigger unmet (downstream of item 15 outputs + items 6b/13/14).
- **Item 13 — Ψ operationalization commitment.** Three-component acceptance. Trigger unmet.
- **Item 14 — Q-form commitment.** Two-component acceptance. Trigger unmet.

### Cross-session items

- **Item 7 — F multiplicativity commitment verification.** Ungated (corrected session 19 — NOT gated by Phil's timeline). Executable any time.
- **Item 10 — ChatGPT onboarding under session-9 framework.** Gemini half closed session 19; ChatGPT half open (fires when a fresh ChatGPT instance is opened for substantive work). Session-23 addition: acceptance now includes empty-body-attachment guidance.
- **Item 17 — current_state.md reconciliation (NEW, session 23).** This document is stale across sessions 19–22; surgical session-23 patch applied; full reconciliation tracked here.

### Cross-session items not in STANDING_ITEMS

- **Manuscript implications.** Phil's manuscript work is independent of Phase 4B's analytical phase.
- **Substrate reproduction-for-authority decision.** Session 18 surfaced uncertain-trust on the 15-May substrate. Session-23 note: the integrity determination (Finding 6) sharpens this — the substrate *files* are real (timestamps, byte-identity verified session 20); it was a *verification claim about them* that was fabricated. The reproduction-for-authority question is separable from the integrity determination.
- **Footer cleanups (Findings A/C, session 20).** Deferred Mike-election item (regenerate `protocol_primer.md` / `standing_rules.md` footers via download-and-move as clean UTF-8, or accept as ratified-by-practice). Carried from session 20 §8; not a STANDING_ITEMS item.
- **Carried-forward independent-trigger check (6b/6c/7/13/14).** Owed ≥5 sessions; STANDING note added to the maintenance log session 23 (honest account of why it keeps deferring; future session performs or Mike retires).
- **Foundational set maintenance.** Kit-revision candidates pending for a future revision: the UTF-8-clipboard-read idiom for file-content retrieval (session 23); off-repo-artifacts-travel-with-absolute-paths (session 22); Finding D (`C:\` tool-writes never reach Mike — download-and-move or paste only, session 20).

---

## Section 4: Next anticipated work

**As of session 18 (2026-05-21); session-23 reordering below.**

> **Session-23 next-work (supersedes the session-18 priority list below for the immediate horizon).**
> - **Item 16 component 3 — E4 remediation (A vs B):** the substantive unblocker. Re-scope the item-6a pre-reg to the available substrate (Option A, Layer 2's default) or produce the missing F_LR probe1_overcrowding run (Option B). Settles item 12 and item 15 component 2.
> - **Item 16 component 2 — downstream-claims review:** keystone-sized, its own session — review other session-16-era Layer-3-reported verification claims accepted without Mike-execution for the same signature.
> - **Item 16 component 4 — formal protocol-record register:** Mike's call on 14-May-class vs apparatus-caught-in-record.
> - **Item 17 — current_state full 19–22 reconciliation** when a session has budget.
> - The session-18 priority list (item 12 as rename, substrate reproduction, v3.1 commit, EDA execution) is **superseded** — item 12 is recharacterized and the EDA premise is void until E4 remediation lands.

The session-18 list, retained for reference: Priority 1 item 12 resolution; Priority 2 substrate reproduction-for-authority; Priority 3 v3.1 commit; Priority 4 item 15 component 2 execution; Priority 5 STANDING_ITEMS independent-trigger check. (Several of these are now reshaped by the integrity determination — see the session-23 block above.)

Several sessions out: item 15 components 3-6 (once execution unblocks); items 13/14 per triggers; items 6b/6c per triggers; item 7 ungated.

---

## Section 5: Working-pattern state

**As of session 18 (2026-05-21); session-23 additions flagged.**

(Session-18-and-earlier working-pattern content unchanged; the kit-revision-5.1 update absorbed sessions 15–18 observations — see Section 6. The entries below are session-23 additions awaiting a future kit revision.)

Working pattern committed in the kit as of kit-revision-5.1 (session 20). The session-15-through-18 working-pattern observations (substrate-state-vs-interpretation framing; Layer 1 → Layer 3 → Layer 2 → Mike sequencing; file-contents-default-to-chat-attachment; Set-Clipboard sequencing; routing-package-vs-artifact-attachment; filename-canonicalization; literal-wording closure; one-click affordance; primary-source re-grounding; five-role taxonomy; cross-cycle awareness; pessimistic-on-passing; rapid-reframe-iteration; AI-instance-state visibility) are now folded into the kit through revision 5.1. See the kit and Section 6.

### Working-pattern observations from session 23 (kit-revision candidates):

- **UTF-8-clipboard-read idiom for file-content retrieval.** To get a file's true bytes into chat for *regeneration* (not just reading), use `[System.IO.File]::ReadAllText("$PWD\path", [System.Text.UTF8Encoding]::new($false)) | Set-Clipboard` then paste — this preserves multibyte glyphs (Ψ/ρ/Δ/§) that a normal console paste mangles. The distinction that drives it: a mojibake'd paste is fine when Layer 1 only needs to *read* a file for analysis, but is corrupting when Layer 1 will *regenerate* a full-file overwrite from it (it reintroduces exactly the session-20 footer-corruption signature). Read-from-paste is acceptable; regenerate-from-paste needs true bytes (UTF-8-clipboard idiom or a chat attachment of the real file).
- **Grep-committed-source-before-re-deriving.** Session 23 nearly re-ran a discriminator (re-hash) that session 20 had already executed, and reached for a probabilistic argument (hash-prefix collision) that session 20's timestamp check already beat. A cheap `git grep` of committed primary source first surfaced that sessions 20–21 had done the work, avoiding the re-derivation. Pattern: before proposing a forensic step, grep the committed record for whether a prior session already ran it — the compressed-memory-vs-primary-source pattern (Finding A family) applies to "what work is already done," not just "what is true."
- **Layer-1-stall pattern ("does everything but does nothing until it has everything").** Mike named this session 23: Layer 1 absorbing work the layers were built to share and gating progress on its own verification-completeness. The corrective is the kit's existing load-sharing note (Section 2) made operational — route to the layers to *drive* (not just to review a Layer-1 frame), and hand the open state rather than a pre-formed conclusion. Session 23's "you drive" Layer 2 routing is the worked example.

---

## Section 6: Protocol state

**As of session 18 (2026-05-21); session-23 markers below.**

- HEAD at session 17 close: `ddea343`. HEAD at session 18 close: left self-referential per Mike's arbitration.
  > **Session-23 protocol-state note.** Live HEAD at session 23 open was `c8bfae72…` — identical to session 22's *start* HEAD, meaning the **session-22 close-out commit never ran**: the session-22 ops log and `phase_4b/reviews/synthesis/` were sitting uncommitted on disk (a Rule-2 session-end gap, found at the session-23 HEAD check). Session 23's close-out commits the session-22 deliverables alongside the session-23 cluster. kit-revision-5.1 (`1cac510`-era; committed session 20) is the operative kit.
- Layer assignments: Claude = Layer 1 (central node), ChatGPT = Layer 2 (substantive review), Gemini = Layer 3 (implementation + analytical synthesis on pasted outputs; NOT local execution — Mike is the only execution channel). Layer 2's five-role taxonomy is canonical.
- Foundational document set: structurally unchanged. `STANDING_ITEMS.md` updated session 23 (items 16, 17 added; item 12 re-blocked; item 15 component-2 block confirmed; item 10 ChatGPT-half acceptance amended; carried-forward-check STANDING note). `current_state.md` surgically updated session 23 (this update; full 19–22 reconciliation tracked as item 17).
- Instantiation kit: kit-revision-5.1 (committed session 20). Session-23 kit-revision candidates (Section 5): UTF-8-clipboard-read idiom; grep-committed-source-before-re-deriving; Layer-1-stall corrective; plus the session-20/22 candidates (Finding D `C:\`-tool-write boundary; off-repo-absolute-paths) if not already folded.
- Routing convention: full Layer 2 cycle for protocol-infrastructure routings includes a v2-acceptance pass before commit. Session 23 validated bidirectional Layer 2 use — routing Layer 2 to *drive* (propose the next Layer 3 contract, name what it needs) rather than only to review a Layer-1 frame, with Mike carrying questions both directions.

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

> **Session-23 maintenance note.** This document carries a surgical-update banner (top) and per-section session-23 markers because Option A was chosen (determination absorbed; 19–22 narrative NOT backfilled). When STANDING_ITEMS item 17 (full reconciliation) executes, remove the banner, the per-section markers, and this note, and re-stamp all sections to the reconciling session.

---

— Drafted by Claude as Layer 1 central node, session 9; v2 Layer 2 review incorporated. Session 10, 15, 16, 18 updates as previously recorded (see prior footer history in the session-18 version of this document, preserved in the session-18 ops log / handoff). **Session 23 surgical update:** absorbed the session-16 fabrication-family determination (Finding 6; Section 2 Finding-2 correction; item 16; Sections 1/3/4/6 markers) per Mike's Option-A arbitration; the full sessions 19–22 reconciliation is deferred to STANDING_ITEMS item 17 and explicitly NOT performed here, to avoid memory-reconstructing four sessions of narrative not read in full this session. The 19–22 ops logs are the primary source for that reconciliation.
