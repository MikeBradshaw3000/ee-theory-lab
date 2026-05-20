# PRIOR_CYCLE_RECONCILIATION_PLAN.md

**Document role.** Reconciliation plan for prior-cycle canonical material inventoried in `PRIOR_CYCLE_INVENTORY.md`. Deliverable 2 of 3 for STANDING_ITEMS item 9. For each inventoried item: a determination of supersession status, a target action, and a target location. One-time task-shaped artifact; not ongoing canonical reference. Pairs with the inventory (deliverable 1) and drives the canonical record update (deliverable 3).

**Authority.** Authoritative for the per-item determination of *current status* and *target action*. The execution of the actions (file creation, content moves, in-directory READMEs, current_state updates) is deliverable 3.

**Decision-rights structure.** Determinations in this plan come from Layer 1 analysis of the inventoried material. Mike arbitrates each determination; arbitration questions are surfaced inline where my read isn't load-bearing. After Mike's arbitration, deliverable 3 executes against the arbitrated plan.

**Method.** Three determination categories per the item 9 acceptance criteria:
- **Superseded** — current session-9 foundational material covers this; the prior-cycle item is preserved as historical record but is not currently authoritative.
- **Still authoritative** — current session-9 foundational material does not cover this, and the prior-cycle item remains in force. Either through preservation as-is or through carry-forward into the foundational set.
- **Requires structural integration** — substantive content not currently in canonical material; needs a new or updated canonical location.

---

## Section 1: `protocols/onboarding/` directory disposition

### 1.1 Directory-level determination

**Status: Superseded as cold-start primer surface.** Session-9 kit-revision-3 plus the foundational set together carry the cold-start primer function for fresh Claude instances. The kit's structural form (compressed surface over canonical foundational set) is the current shape of that function.

**Action.** Add `protocols/onboarding/README.md` marking the directory as prior-cycle. README explains the supersession, points at the foundational set and kit as current cold-start surface, preserves the four files in place as historical record.

**Open arbitration question.** The four primer documents predate ChatGPT and Gemini onboarding under the session-9 framework. The session-9 foundational set is Claude-focused; there's no equivalent ChatGPT or Gemini primer in the foundational set. Two paths:

A. Keep the ChatGPT and Gemini primers as still-authoritative documents (move them out of `protocols/onboarding/` to canonical locations) while marking the Claude primer as superseded.
B. Mark all four as superseded and accept that ChatGPT/Gemini onboarding currently has no foundational-set equivalent (deferred problem, surfaced as a new STANDING_ITEMS entry).

**My lean: B.** The primers as written are anchored to Cycle 2 Round 1 Post-Flight-2-Closure state — content that has moved substantially since. Salvaging them as still-authoritative would require substantial rewriting against current state, which is reconciliation-creep beyond item 9's scope. Cleaner to mark superseded and surface ChatGPT/Gemini onboarding as a deferred item.

**Mike arbitrates A vs. B.**

### 1.2 Substantive content carry-forwards from primer documents

Per inventory Section 4, the primer documents carry substantive content not engaged by session-9 foundational set. These carry-forwards are independent of the directory-level disposition: regardless of whether the primer files stay or move, the substantive content needs a canonical home.

See Section 4 below for each content carry-forward determination.

---

## Section 2: `protocols/architectural_reviews/` directory disposition

### 2.1 Directory-level determination

**Status: Still authoritative as historical record of Layer 1 review outputs.** Operations logs preserve session-by-session operational record per the README's honest-record principle; architectural reviews are the parallel record of Layer 1 review outputs. Both directories serve the methodology paper's reproducibility commitment.

The session-9 foundational set does not name this directory or document the Layer 1 review-output form. This is a gap, not a supersession.

**Action.** Add `protocols/architectural_reviews/README.md` documenting the directory's role: Layer 1 architectural review outputs, parallel to operations logs, preserved per honest-record principle. README explicitly notes the directory is open for new entries (Layer 1 architectural reviews of future substrate/analysis code).

Update `protocols/foundational/canonical_artifacts_index.md` to reference the directory and document its authority.

### 2.2 Substantive carry-forward: v1_1_divergence_review footnote precedent

The footnote in `2026-05-14_v1_1_divergence_review.md` is precedent material for what session 9 surfaced as the "path-space land grab" framing. The discipline note ("when routing notes pre-frame an arbitration, the architectural review should first verify the framing's premise before engaging the substantive options") is closely related to the session-9 discipline ("Layer 1 self-review should check name-and-location collision when drafting canonical infrastructure").

**Action.** When Rule 7.4 expansion fires in kit-revision-4 (per prior-Claude's confirmation), reference the v1_1_divergence_review footnote as precedent. Not a deliverable-3 action — this is a kit-revision-4 note carried forward.

---

## Section 3: `operations_log/` directory disposition

### 3.1 README disposition

**Status of directory conventions content: Still authoritative.** The filename format, authorship, honest-record principle, and discipline-notes conventions are not duplicated in session-9 foundational material and remain in force.

**Status of "five standing rules" content: Superseded by `protocols/foundational/standing_rules.md` Rule 1-10.** The five-rule list is historical content from the rule system's origin event (the emulation discovery on 14 May 2026); the current rule system extends and supersedes it.

**Action.** Update `operations_log/README.md`:
- Preserve the directory conventions section as-is.
- Replace the "Standing rules (current as of 14 May 2026)" section with a pointer: "The standing rules current as of session 9 onward are in `protocols/foundational/standing_rules.md` (Rule 1-10). The five-rule list originally in this README documented the rule system as it existed 14 May 2026; that content is preserved in `operations_log/2026-05-14_emulation_discovery.md` as historical record of the rule system's origin event."
- Add a Cross-references entry pointing at `protocols/foundational/`.

### 3.2 Operations logs (16 prior-cycle entries) disposition

**Status: Still authoritative as historical record.** Per the README's honest-record principle, operations logs are not retroactively edited. The prior-cycle logs are by-construction immune to supersession at the content level — they record what happened on the date they cover.

**Action.** No action required. The logs stay in place. Optional addition: a one-line Cycle-1-to-Cycle-2 boundary marker in the directory README ("operations logs span Cycle 2 Round 1 opening through Phase 4B session 9; see operations_log/2026-05-14_emulation_discovery.md for the Cycle 2 Round 1 opening event").

**Open arbitration question.** Whether the boundary marker is worth adding, given that the file-date sequence already makes the boundary visible. **My lean: skip it.** Reader-friendly but adds maintenance load (would need updating each time the boundary shifts).

---

## Section 4: Substantive content carry-forward determinations

Each item from inventory Section 4 gets a determination here.

### 4.1 Two-paper structure framing

**Status: Requires structural integration.** Three primer documents independently treat this as load-bearing for role definitions and theoretical context. Session-9 foundational set has no equivalent framing.

**Substantive content to carry forward.** AMR paper (Phil leading, mean-field foundation, Four Grand Challenges) and methodology/substrate paper (Cycle 2 substrate work, spatial frontier beyond MFA), with the relationship being deliberately two-layer: A3 baseline (global ρ, mean-field) is the limit of v1.1's spatial substrate; the "divergence" between them is the architectural relationship between the foundation paper and forward work.

**Target location.** `protocols/foundational/current_state.md`. Add a new Section 2.5 (or wherever fits) titled "The two-paper structure." Brief — three to five paragraphs covering the relationship between Document 1 (AMR foundation paper) and Document 2 (methodology/substrate paper), with the mean-field-vs-spatial-substrate distinction.

**Open arbitration question.** Whether this is `current_state.md` content (which my read says yes — it's state-of-the-program), or whether it belongs in `protocol_primer.md` (which says role context for Claude, ChatGPT, Gemini). **My lean: `current_state.md`.** The two-paper structure is about the project's state; the protocol primer is about how the AI partners operate within that state.

### 4.2 Four Grand Challenges

**Status: Requires structural integration.** Theoretical content named in multiple prior-cycle documents (the new_chat_primer, the v1_1_divergence_review footnote). Session-9 material engages "Grand Challenge 1 (nucleation)" implicitly in the empirical context but does not name the full four challenges or treat them as canonical theoretical scope.

**Substantive content to carry forward.** The AMR paper hands four challenges to the research community: (1) Nucleation / spatial seeding dynamics, (2) Network Topology, (3) Narrative Dynamics, (4) Empirical Calibration. v1.1's spatial substrate operationalizes these computationally.

**Target location.** `protocols/foundational/current_state.md`, paired with or adjacent to the two-paper structure content. Treat the Four Grand Challenges as the open-questions structure of the AMR paper, which the methodology paper's substrate work engages.

### 4.3 Cycle 1 / Cycle 2 framework

**Status: Requires structural integration with mapping to current session numbering.** The Cycle 1 / Cycle 2 framework is load-bearing in prior-cycle documents; session-9 material uses "session N" without engaging the cycle framework. Both are real organizing structures.

**Substantive content to carry forward.** Cycle 1 produced theory v1.1 through v1.7, multi-AI protocol through Round 1 + Round 2 (Flights 1-2), substrate spec v1.1, M2 architectural specification, and discovered the substrate-drift problem during Flight 6 Phase 4B work. Apparatus reset closed Cycle 1; Cycle 2 Round 1 opens with fresh Mesa, fresh ChatGPT, fresh Gemini, while Cycle 1 discoveries informed Cycle 2 discipline structures.

The session 1-9 sequence in current session numbering maps to Cycle 2: session 1 is Cycle 2 Round 1 opening (with the 14 May emulation-discovery event likely being part of session 1's content); session 9 is the current end-state.

**Target location and form.** `protocols/foundational/current_state.md` Section 1 (or wherever the current project history sits) — add a Cycle-1-then-Cycle-2 history with explicit mapping from cycle/round/flight framework to session numbering.

**Open arbitration question.** Whether mapping should be a structural inline addition (cycles and sessions are different organizing levels, both kept) or unification (sessions become the canonical organizing level, cycles archived as Cycle 1 closure history). **My lean: structural inline addition.** Cycles correspond to substantive program structure (apparatus reset, fresh start); sessions correspond to chat-instantiation discipline. They serve different purposes.

### 4.4 Original five standing rules

**Status: Superseded by Rule 1-10 with explicit historical mapping needed.** The relationship is real but underdocumented.

**Substantive content to carry forward.** Original five rules (no past-tense for unexecuted actions; no synthetic telemetry; execution-verification at parity moments; asymmetric execution channel acknowledgment; gate-closing artifacts route to all reviewing AIs) originated at the 14 May 2026 emulation discovery. The current Rule 1-10 system extends and supersedes the original five.

The session-9 `standing_rules.md` Rule 7 (Section 15 prohibitions lift, with sub-rules 7.1-7.7 covering aggregate completion claims, schema-emulation, synthetic metadata, memory-reconstruction, partial-completion framing, missing-telemetry imputation, required affirmations) covers most of the original-five rule 2 (synthetic telemetry) and 4 (asymmetric execution channel) content at a more granular level. But the relationship is not 1:1 — original rule 1 (past-tense verbs) does not appear to have a direct successor in Rule 1-10, and original rule 5 (gate-closing artifacts route to all reviewing AIs) appears to be operational practice rather than codified rule in the current system.

**Action.** Add a section to `protocols/foundational/standing_rules.md` titled "Historical lineage: from the original five standing rules to Rule 1-10." Brief mapping section documenting:
- The 14 May 2026 emulation-discovery event as rule-system origin.
- Per-rule mapping from original five to Rule 1-10 (or noting where mapping is partial or pending).
- The principle that operations_log records remain the substantive source of the rule system's evolution.

**Open arbitration question.** Whether the mapping is best done as a section in `standing_rules.md` (my lean — content-adjacent) or as a separate document `protocols/foundational/standing_rules_lineage.md` (separates historical from current). **My lean: section in `standing_rules.md`.** The mapping is short; a separate document feels overweight.

### 4.5 A3 reference baseline

**Status: Still authoritative; requires structural integration into foundational set as canonical theoretical reference.** A3 is locked Cycle 1 reference baseline; not superseded; not currently named in session-9 foundational set.

**Substantive content to carry forward.** A3 parameters: α=4, β=3, δ=4, γ=4, η=0.01. 20×20 torus. Synchronous two-phase update. Ceiling ρ≈0.57 at Λ=1.0 under 500-tick equilibrium averaging (200 ticks discarded as transient, 300-tick average). Analytical fixed point at γ=4 is ρ* ≈ 0.5952. The three candidates A1 (logistic, eliminated for bistability), A2 (saturating exponential, eliminated for worse bistability), A3 (counter-regulated quadratic crowding penalty, retained).

**Target location.** `protocols/foundational/current_state.md` Section 2 (theoretical architecture current state) — add a subsection "Reference baseline" documenting A3 parameters and ceiling.

### 4.6 Personal-context discipline

**Status: Still authoritative; requires structural integration.** Prior-cycle primer carries personal-context content (Mokie note plus physics-study paragraph plus contemplative-practice paragraph); session-9 foundational set has no equivalent provision.

**Substantive content to carry forward.** All three paragraphs from `new_chat_primer.md`'s "What Mike has shared about himself" section, with the "Do not bring this up unprompted" discipline preserved.

**Target location.** Per your "I think it is very nice and quite accurate. I know you don't need to know it, but why not leave it?" response, the content stays. Two location options:

A. New file `protocols/foundational/personal_context.md`. Standalone file makes the carry-forward clean and gives the content its own canonical home.
B. Section in `protocols/foundational/protocol_primer.md`. Folds personal context into the primer that defines AI-partner roles.

**My lean: A (new file).** The content is genuinely separate from protocol mechanics. Mixing them in `protocol_primer.md` risks future Claude reading the primer as architectural infrastructure and skimming over the personal-context section, when the discipline ("do not bring this up unprompted") is exactly the kind of thing that needs its own visible home. Standalone file is more legible.

**Mike arbitrates A vs. B.**

### 4.7 Vocabulary additions

**Status: Mixed.** Two separable items.

**"Eligibility" prohibition.** Not in session-9 `vocabulary_quarantine.md` Section 1. Status: requires structural integration.
**Action.** Add to `protocols/foundational/vocabulary_quarantine.md` Section 1 (Hard prohibitions): "'eligibility' (gatekeeping connotation; architecture has no gatekeeper — cleaner: 'action streams that project onto the bases')."

**Damasio/Haken scrub history.** Named explicitly in primers as historical scrubs (Damasio biological language wrapper scrubbed early in the project; Haken laser source scrubbed — invoke the structural pattern, not the laser as source). Session-9 material engages Haken at the approach level but does not document the source-domain scrub history. Status: requires structural integration.
**Action.** Add to `protocols/foundational/vocabulary_quarantine.md` a new section "Source-domain scrubs" documenting the Damasio and Haken scrubs and the principle (invoke the structural pattern without importing the source-domain language).

### 4.8 Open Element 14

**Status: Documentation gap.** The label `chatgpt_new_chat_primer.md` Section 8 uses ("Open Element 14") is the canonical example of drift-prone vocabulary in session-9 `vocabulary_quarantine.md` Section 3. Whether the quarantine was drafted with awareness of the primer's prior use, or whether it surfaced independently, is not documented.

**Action.** Update `protocols/foundational/vocabulary_quarantine.md` Section 3 to cross-reference the prior-cycle primer use: "The Open Element 14 example used in this section originates in pre-session-9 prior-cycle work where the label appears in `protocols/onboarding/chatgpt_new_chat_primer.md` Section 8. The label is preserved as historical canonical example of drift-prone vocabulary; the quarantine instructs that such non-canonical numeric labels be restated in committed terms when drafting new material."

### 4.9 Environment and toolchain detail

**Status: Still authoritative as operational reference; requires structural integration.** Production-machine environment details and dependency versions are not in session-9 foundational set but are load-bearing for substrate work.

**Substantive content to carry forward.** Workspace: `C:\Users\vkz244\EE_Theory_Lab\`. PowerShell. venv at `.\venv\`. Python 3.12+ (or 3.14.4 per `new_chat_primer.md`). Core dependencies: mesa, solara, networkx, pandas, matplotlib, altair, numpy, pyarrow. Mesa 3.x flat namespace and activation pattern. Notepad-UTF8-BOM hazard. `np.RankWarning` → `np.exceptions.RankWarning` API change. Distribution via Python+base64 scripts as minimum-thumb-work pattern.

**Open arbitration question.** Two location candidates:

A. New file `protocols/foundational/environment_reference.md` — gives the content its own canonical home, parallels other foundational documents.
B. Section in `protocols/foundational/current_state.md` — folds environment detail into project current state.

**My lean: A (new file).** Environment reference is operational, not state-of-the-program. Lives more naturally as standalone reference, the way Mike points at it ("the Mesa setup guide in the repo documents environment-specific hazards and idioms" per `gemini_new_chat_primer.md` Section 10).

**Mike arbitrates A vs. B.**

---

## Section 5: Updated foundational documents (summary by destination)

Pulling together the determinations above, this section enumerates the session-9 foundational documents that need updates as part of deliverable 3, plus the new documents required.

### 5.1 `protocols/foundational/current_state.md`

Updates required:
- **Section 1 (project history):** Cycle 1 / Cycle 2 framework with session-numbering mapping (per 4.3).
- **Section 2 (theoretical architecture):** Add subsections for two-paper structure (4.1), Four Grand Challenges (4.2), and A3 reference baseline (4.5).
- Update "Stage 1 complete" framing (per session-9 addendum) to "Stage 1 complete after reconciliation" — language change in any current_state.md references to Stage 1 completion.

### 5.2 `protocols/foundational/standing_rules.md`

Updates required:
- Add section on historical lineage from original five rules to Rule 1-10 (per 4.4).

### 5.3 `protocols/foundational/vocabulary_quarantine.md`

Updates required:
- Section 1 (Hard prohibitions): Add "eligibility" (per 4.7).
- Add new section "Source-domain scrubs" for Damasio/Haken history (per 4.7).
- Section 3 (Drift-prone): Cross-reference prior-cycle use of Open Element 14 (per 4.8).

### 5.4 `protocols/foundational/canonical_artifacts_index.md`

Updates required:
- Add `protocols/architectural_reviews/` as canonical-record-shaped directory (per 2.1).
- Add `operations_log/` (and its README) as canonical-record-shaped directory if not already there.
- Add new canonical foundational documents per 5.6 below.
- Reference `PRIOR_CYCLE_INVENTORY.md` and `PRIOR_CYCLE_RECONCILIATION_PLAN.md` as one-time deliverables for item 9 (workspace root, finite life, close out when reconciliation completes).

### 5.5 `protocols/foundational/protocol_primer.md`

No updates required from this reconciliation plan. Mike arbitrates 4.6 personal-context location; if option B (section in protocol_primer.md), then primer gets a new section.

### 5.6 New foundational documents

Pending arbitration on 4.6 (personal-context) and 4.9 (environment-reference):
- `protocols/foundational/personal_context.md` — if Mike chooses 4.6 option A.
- `protocols/foundational/environment_reference.md` — if Mike chooses 4.9 option A.

### 5.7 In-directory READMEs (new files)

- `protocols/onboarding/README.md` — marks directory as prior-cycle (per 1.1).
- `protocols/architectural_reviews/README.md` — documents directory role (per 2.1).

### 5.8 `operations_log/README.md`

Update per 3.1: preserve directory conventions, replace five-rules section with pointer to `standing_rules.md` and historical-record explanation.

---

## Section 6: Out-of-scope items surfaced for future-session arbitration

Items where reconciliation work would expand item 9's scope beyond what fits this session. Surfacing here for STANDING_ITEMS additions.

### 6.1 ChatGPT and Gemini onboarding under session-9 framework

If Mike's arbitration on 1.1 selects option B (mark all four primer documents as superseded), then ChatGPT and Gemini onboarding has no foundational-set equivalent. This is a deferred item to surface as a new STANDING_ITEMS entry.

### 6.2 Kit-revision-4

Per prior-Claude's confirmation in the post-revert note, kit-revision-4 is the appropriate location for incorporating:
- The "path-space land grab" framing into Rule 7.4.
- The "any copy-target, not just PS" principle for fenced-block discipline.
- The "informational content does not need a copy-pane" principle.
- The v1_1_divergence_review footnote as precedent material (per 2.2).

Kit-revision-4 fires post-item-9 closure. Not part of deliverable 3.

### 6.3 Cycle 2 substrate work resumption

The session 1-9 sequence has been heavily restructure-focused. Per the prior-cycle primer documents, the substrate-work agenda includes Path A (close Round 1 → Phase 4B opens) or Path B (open Flight 3 with one of three candidate questions). Whether the substrate-work agenda is currently active, paused, or superseded is not clear from session-9 material; this is a deferred item to surface for future arbitration. Not in scope for item 9 reconciliation.

---

## Section 7: Deliverable 3 scope statement

Deliverable 3 executes against this plan after Mike's arbitration on the open questions. Specifically:

1. Mike arbitrates Sections 1.1 (A vs B), 4.3 (mapping form), 4.4 (location), 4.6 (location), 4.9 (location).
2. Layer 1 produces the deliverable-3 file set: updated foundational documents per Section 5, new files per Section 5.6 (as arbitrated), in-directory READMEs per Section 5.7.
3. Layer 1 routes deliverable 3 for Layer 2 sanity scan (per the foundational-set discipline that substantive foundational updates get Layer 2 review).
4. Deliverable 3 commits along with `PRIOR_CYCLE_INVENTORY.md` and `PRIOR_CYCLE_RECONCILIATION_PLAN.md`. Item 9 closes.
5. STANDING_ITEMS item 9 removes; items 1 and 2 become first-eligible.

**Estimated scope of deliverable 3.** Substantial. The deliverable updates four existing foundational documents, creates up to four new files (two foundational, two READMEs), and updates one operations_log README. Whether deliverable 3 fits the remaining context-window budget of this session, or whether session 10 closes with deliverables 1-2 committed and deliverable 3 deferred to session 11, is at Mike's arbitration.

---

— Drafted by Claude as Layer 1 central node, session 10, item 9 deliverable 2 of 3. Reconciliation plan ready for Mike's review and arbitration.
