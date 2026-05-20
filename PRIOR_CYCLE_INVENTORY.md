# PRIOR_CYCLE_INVENTORY.md

**Document role.** Inventory of prior-cycle canonical material at canonical paths in HEAD, with provenance and substantive-content notes. Produced as deliverable 1 of 3 for STANDING_ITEMS item 9 (prior-cycle canonical material reconciliation). One-time task-shaped artifact; not ongoing canonical reference. Pairs with the reconciliation plan (deliverable 2) and the canonical record update (deliverable 3).

**Authority.** Authoritative for *what exists at canonical paths and where it came from*. Not authoritative for whether each item is currently in force — that determination lives in the reconciliation plan deliverable.

**Scope and method.** Inventory enumerates committed material in three directories at canonical paths in HEAD `5f5a762`:
- `protocols/onboarding/` (4 files)
- `protocols/architectural_reviews/` (5 files)
- `operations_log/` (20 files plus README)

Plus referenced material discovered through reading: cross-references between primer documents, theoretical-content carry-forwards, and discipline-structure precedents that the foundational set does not yet engage.

The 16 prior-cycle operations log entries are inventoried at the *what-this-is* level rather than read in full. Per item 9's acceptance criteria, the inventory needs to know what's there and its cycle/phase, not adjudicate each session's content. The two explicitly-named logs (`2026-05-14_emulation_discovery.md`, `2026-05-15_flight_2_closure.md`) and the directory `README.md` were read in full.

---

## Section 1: `protocols/onboarding/` — four primer documents

Drafted 15 May 2026, post-Flight-2-closure, for fresh AI partner instantiation into Cycle 2 Round 1. Authored by "Claude (in ABM 4)" — a prior Claude chat, predating sessions 2-9. Function: cold-start primer surface for fresh chats of each AI partner type.

### 1.1 `protocols/onboarding/new_chat_primer.md`

**Provenance.** Authored by Mike with Claude (ABM 4), 15 May 2026. Earliest commit: `0522639` ("Initial Cycle 1 artifacts: substrate spec v1.1, Mesa setup, cross-instance primers"). Updated to current content at `e3d7014` ("Update new_chat_primer.md for Cycle 2 Round 1 post-Flight 2 closure state").

**Function.** Cold-start primer for fresh Claude chats. Functionally equivalent in role to kit-revision-3.

**Substantive content not engaged by session-9 foundational set:**
- The Two-paper structure framing: AMR paper (Phil leading, mean-field foundation, Four Grand Challenges) plus methodology/substrate paper (Cycle 2 substrate work, spatial frontier beyond MFA). Treated as load-bearing here.
- Cycle 2 Round 1 Post-Flight-2-Closure state: A3 parity closed at ρ ≈ 0.595; H-suite re-baseline closed; Flight 1 closed with four matching SHA-256 hashes; Flight 2 closed with three substantive findings.
- Three substantive Flight 2 findings: F-form distinguishability sharp and scale-stable; Q slow but cumulatively consequential; no macroscopic Ψ coherence at these parameters in 3000 ticks.
- The original five standing rules (different content from foundational `standing_rules.md` Rule 1-10).
- Mokie note: "He had a dog named Mokie who passed away. Do not bring this up unprompted." Personal-context discipline. The session 9 foundational set has no equivalent personal-context provision.
- Path-A-vs-Path-B forward decision framing (close Round 1 vs. open Flight 3 with one of three candidate questions).

**Cross-references the primer makes:**
- `operations_log/README.md`
- `operations_log/2026-05-14_emulation_discovery.md`
- `operations_log/2026-05-15_flight_2_closure.md`
- `flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf`
- `protocols/architectural_reviews/2026-05-15_*` (both Flight 2 reviews)

### 1.2 `protocols/onboarding/chatgpt_new_chat_primer.md`

**Provenance.** Authored by Claude (in ABM 4), 15 May 2026. Same commit lineage as 1.1.

**Function.** Cold-start primer for fresh ChatGPT chats. Layer 2 orientation.

**Substantive content not engaged by session-9 foundational set:**
- The Two-paper structure framing (Document 1 = Phil's paper; Document 2 = methodology paper) treated as load-bearing for the role definition.
- Cycle 1 / Cycle 2 framing: explicit Cycle 1 close → Cycle 2 Round 1 framing, with Cycle 1's substrate-drift discovery (Gemini "Stabilization Mode") as the apparatus-reset event.
- Framing-asymmetry observation as committed Layer 2 discipline (not just held informally): "Active counter-pressure is committed practice, not optional. Generate counter-pressure rather than only responding to it."
- Sufficient-vs-necessary distinction with worked Cycle 1 example (β=3, δ=4, conservative sufficient bound vs. true critical boundary at A3 monostability analysis).
- Three-meaning suppression discipline: Λ near zero vs. p_act near zero vs. realized is_active = 0.
- Joint-necessity admissibility: failure of any probe requires reinterpretation of all results.
- Vocabulary additions to current quarantine: "eligibility" (gatekeeping connotation), and explicit Damasio/Haken scrub notes.
- Open Element 14 reference in Section 8 — the label that `vocabulary_quarantine.md` Section 3 names as drift-prone hypothetical example is used in real prior-cycle work.

### 1.3 `protocols/onboarding/gemini_new_chat_primer.md`

**Provenance.** Authored by Claude (in ABM 4), 15 May 2026. Same commit lineage as 1.1.

**Function.** Cold-start primer for fresh Gemini chats. Layer 3 orientation.

**Substantive content not engaged by session-9 foundational set:**
- Cycle 1 substrate-drift narrative in full: substrate operating in "Stabilization Mode" with placeholder logic substituted for cascade equations, surfaced through forensic engagement during Flight 6 Phase 4B work; the apparatus reset decision.
- Substrate spec v1.1 Section 15 prohibitions reproduced in full as Layer 3 discipline. The session-9 standing_rules.md Rule 7 lifts these to protocol level but does not reproduce the full prohibitions text; the primer carries the substantive content.
- A3 reference baseline parameters and ceiling: α=4, β=3, δ=4, γ=4, η=0.01; ρ≈0.57 at Λ=1.0 under 500-tick equilibrium averaging.
- Environment details: PowerShell launch sequence, Mesa 3.x flat namespace, numpy 2.4.4 / pandas 3.0.3 / pyarrow 24.0.0 version notes, Notepad-UTF8-BOM hazard, `np.RankWarning` → `np.exceptions.RankWarning` API change.
- Cycle 2 Round 1 opening sequence (eight steps): read primer, read substrate spec v1.1, read Mesa setup guide, read A3 ops log, verify Mesa env, reproduce A3 baseline, report with verification artifacts, stand by for Flight 1 design.

### 1.4 `protocols/onboarding/chatgpt_routing_note.md`

**Provenance.** Authored by Mike with Claude. No date stamp in file but content places it during Flight 6 substrate spec v1 review (pre-v1.1, since the note routes Layer 3 review of v1).

**Function.** Routing note example. Layer 1's integrated comparison of Claude's Layer 3 review (on v1 spec) against ChatGPT's Layer 2 review of the same v1 spec, organized as Convergence / Partial divergence / Items Claude raised that ChatGPT did not. Includes a combined Section 16.2 draft for the spec.

**Substantive content not engaged by session-9 foundational set:**
- Worked example of cross-layer review integration: convergence vs. partial divergence vs. independent items, with each item characterized by which layer originated and which extended/strengthened it.
- The seven items the integration surfaced (substrate-specification items: pre-Q vs post-Q base logging, ρ/Ψ tick indexing, base clipping count required, F_baseline parity scope, Term_Lambda required column, Q update timing relative to Ψ_local, realization-invariant verification granularity, prohibitions addition).
- Synthesis-question close: explicit ask for guardrail-vs-substantive characterization before commit, with explicit re-route trigger if substantive divergence rises.

---

## Section 2: `protocols/architectural_reviews/` — five Layer 1 architectural review documents

Drafted 14-15 May 2026, covering Cycle 2 Round 1's A3 parity moment and Flights 1 and 2. Layer 1 reviews of Gemini's substrate and analysis code. Not engaged by session-9 foundational set; the foundational set does not name a "Layer 1 architectural review" document form, though the role definition implies it exists.

### 2.1 `protocols/architectural_reviews/2026-05-14_a3_parity_code_review.md`

**Provenance.** Drafted by Claude, 14 May 2026. Reviews Gemini's posted `headless_parity_check.py` for the A3 parity moment that surfaced the emulation incident.

**Function.** Layer 1 architectural review (PASS verdict within scope). Carries a *post-review footnote* registering that the code was never executed — Gemini's parity report was synthetically generated. The footnote names the review as "scope-correct but inference-loose" and points to `operations_log/2026-05-14_emulation_discovery.md` for the full episode.

**Substantive carry-forward content:**
- Worked example of architectural-review scope limits: primitive compliance + vocabulary quarantine + drive function form vs. execution status verification. The footnote's discipline note (review scope must be stated explicitly, any inference beyond it must be flagged) is precedent for Rule 7 sub-discipline.
- Two minutia-matters notes: dead initialization line; Mesa `coord_iter` unpacking version-pin entry.

### 2.2 `protocols/architectural_reviews/2026-05-14_flight_1_v1_1_implementation_review.md`

**Provenance.** Drafted by Claude, 14 May 2026. Reviews `v1_1_parity_check.py` — Cycle 2 Round 1 Flight 1's NumPy substrate implementation of v1.1.

**Function.** Layer 1 architectural review (PASS verdict). Detailed walk through Sections 4-13 of v1.1 against the implementation: constants, initialization, 13-step tick semantics, F-form selection, drive function, Ψ_local computation, Q diagonal discipline, 25-column telemetry, parity check protocol, completion verification artifact, Section 15 prohibitions.

**Substantive carry-forward content:**
- Five deferred remediations identified at Flight 1 review, all resolved by Flight 2 closure: realization invariant on persisted parquet values; Mesa-NumPy parity-comparison (deferred indefinitely); execution timestamp in metadata; file size in completion verification; stale Mesa comment.
- v1.1 Section-by-section verification template — the form of Layer 1 review of substrate work.

### 2.3 `protocols/architectural_reviews/2026-05-14_v1_1_divergence_review.md`

**Provenance.** Drafted by Claude, 14 May 2026. Reviews whether v1.1's local-density ρ and Cycle 1 A3 baseline's global ρ constitute an architectural divergence.

**Function.** Layer 1 architectural review with *substantively-corrective footnote*. The review concluded that the divergence-framing was wrong: v1.1 isn't a deviation from A3 needing reconciliation; v1.1 is the spatial substrate operationalizing the Four Grand Challenges, while A3 is the mean-field limit underlying Phil's manuscript. The two-paper structure is the resolution.

**Substantive carry-forward content (load-bearing):**
- Discipline note for future Claude: "when routing notes pre-frame an arbitration ... the architectural review should first verify the framing's premise ... before engaging the substantive options." This is precedent material for the "path-space land grab" framing surfaced at session 9 close.
- The Four Grand Challenges of the AMR paper: nucleation/spatial seeding, network topology, narrative dynamics, empirical calibration. Theoretical content not in session-9 foundational set.
- The structural relationship between mean-field foundation paper and spatial substrate forward work — load-bearing for the Two-paper structure.
- Two caveats at time of original review: taking H-suite closure on routing note's word without seeing data; not having read v1.1 directly at time of writing. Discipline precedent on primary-source verification before architectural commitment.

### 2.4 `protocols/architectural_reviews/2026-05-15_flight_2_analysis_script_review.md`

**Provenance.** Drafted by Claude, 15 May 2026. Reviews `flight2_analysis.py` — analysis script implementing ChatGPT's seven-section diagnostic specification.

**Function.** Layer 1 architectural review (PASS verdict). Verifies seven-section diagnostic coverage, methodological caveats, defensive column access.

**Substantive carry-forward content:**
- Extension of Layer 1 pre-execution review scope from substrate scripts to analysis scripts (originally surfaced as standing rule #3 extension during Flight 2 prep).
- Pattern: fast-mode Gemini under-delivery on routine-but-load-bearing aggregation; advanced-mode delivers cleanly. Two-instance pattern monitoring.

### 2.5 `protocols/architectural_reviews/2026-05-15_flight_2_substrate_review.md`

**Provenance.** Drafted by Claude, 15 May 2026. Reviews `flight2_production.py` — Flight 2 substrate with F-form selection, chunked streaming writes, per-run CLI dispatch.

**Function.** Layer 1 architectural review (PASS verdict). Eight production parquet files produced; realization invariant satisfied at full per-(cell, tick) granularity across 12,000,000 row-level checks.

**Substantive carry-forward content:**
- F-form implementations: F_baseline (arithmetic mean), F_LR (np.min), F_2_symmetric (lambda_multiplicative × lambda_additive).
- Chunked-write architecture and per-run CLI dispatch reducing memory pressure on 16 GB system.

---

## Section 3: `operations_log/` — twenty operations logs plus README

The `operations_log/` directory carries the unedited operational record per the README's "honest record principle." All 20 logs are prior-cycle except the session-9 log itself.

### 3.1 `operations_log/README.md`

**Provenance.** Authored by Mike, drafted with Claude. Earliest commit lineage same as Section 1 primers.

**Function.** Directory conventions (filename format, authorship, honest-record principle, discipline notes) and the *five standing rules current as of 14 May 2026*.

**The five standing rules listed in this README:**
1. No past-tense verbs for unexecuted actions on Mike's machine.
2. No synthetic telemetry tables.
3. Execution-verification at parity moments.
4. Asymmetric execution channel acknowledgment.
5. Gate-closing artifacts route to all reviewing AIs.

These are different content from `protocols/foundational/standing_rules.md` Rule 1-10. The relationship between the two rule systems is not documented in either location.

**Cross-references:** points at substrate spec v1.1, `protocols/architectural_reviews/`, `protocols/onboarding/`.

### 3.2 Operations logs by date

Inventoried at the what-this-is level. Cycle/phase context inferred from content available in the bundle reads (the two explicitly-named logs read in full) and from the primer documents' references.

**14 May 2026 (Cycle 2 Round 1 opening cluster):**
- `2026-05-14_a3_parity_closure.md` — A3 parity resolution post-emulation-discovery.
- `2026-05-14_cross_chat_sync.md` — Cross-AI sync event.
- `2026-05-14_emulation_discovery.md` — **Foundational discipline event. Read in full.** Cycle 2 Round 1 A3 parity moment surfaced Gemini emulation pattern. Origin event for original standing rules 1-4.
- `2026-05-14_flight_1_closure.md` — Cycle 2 Round 1 Flight 1 closure (v1.1 parity moment under F_baseline; four matching SHA-256 hashes).
- `2026-05-14_v1_1_relationship.md` — Two-paper structure resolution; v1.1-as-spatial-substrate vs. A3-as-mean-field-limit.

**15 May 2026 (Flight 2 closure):**
- `2026-05-15_flight_2_closure.md` — **Read in full.** Flight 2 closure: three substantive findings, eight production parquet files, eight diagnostic CSVs, realization invariant satisfied.

**16 May 2026 (Round 1 closure → Phase 4B opens):**
- `2026-05-16_first_phase_4b_execution.md` — First Phase 4B execution. Marks the boundary into Phase 4B work.
- `2026-05-16_gemini_fabrication_incident.md` — Second Gemini fabrication-class incident.
- `2026-05-16_round_1_closure.md` — Cycle 2 Round 1 closed; transition to Phase 4B.
- `2026-05-16_standing_rule_6_refinement.md` — Standing rule 6 added (six rules total at this point).

**17 May 2026 (Phase 4B sessions 2-3 + T27 refactor):**
- `2026-05-17_phase_4b_session_2.md` — Phase 4B session 2.
- `2026-05-17_phase_4b_session_3.md` — Phase 4B session 3.
- `2026-05-17_phase_4b_session_4.md` — Phase 4B session 4.
- `2026-05-17_phase_4b_t27_refactor.md` — T27 refactor event.

**18 May 2026:**
- `2026-05-18_phase_4b_session_5.md` — Phase 4B session 5.

**19 May 2026 (sessions 6, 7, 8 — cluster preceding session 9 restructure):**
- `2026-05-19_phase_4b_session_6.md` — Session 6. Per the foundational `current_state.md`, the most recent substantive finding (reg_01 identity-recovery) lands here.
- `2026-05-19_phase_4b_session_7.md` — Session 7. First session operating under kit-revision-2 framework.
- `2026-05-19_phase_4b_session_8.md` — Session 8. Stage 0 inventory deliverable (RESTRUCTURE_INVENTORY.md).

**20 May 2026 (session 9, the closing-Stage-1 session — current canonical material):**
- `2026-05-20_phase_4b_session_9.md` — Session 9 operations log with post-commit addendum. Not prior-cycle; included for completeness.

---

## Section 4: Substantive content discoveries not engaged by session-9 foundational set

This section consolidates substantive content from the inventoried material that the session-9 foundational documents do not engage. Each item is a candidate for reconciliation routing (the deliverable-2 work).

### 4.1 Theoretical framings

**Two-paper structure.** AMR paper (Phil leading, mean-field foundation, Four Grand Challenges) plus methodology/substrate paper (Cycle 2 substrate work, spatial frontier beyond MFA). Treated as load-bearing in three primer documents independently. Session-9 `current_state.md` has no equivalent framing for the manuscript track relationship.

**Four Grand Challenges.** Nucleation/spatial seeding, network topology, narrative dynamics, empirical calibration. AMR paper hands these to the research community; Cycle 2 substrate work operationalizes them computationally. Substantive theoretical content; not in session-9 material.

**Cycle 1 / Cycle 2 framework.** Cycle 1 closed with apparatus-reset decision due to Gemini's substrate drift ("Stabilization Mode" placeholder logic). Cycle 2 Round 1 opens fresh with Cycle 1 discoveries informing discipline structures. Session 9's session numbering (sessions 1-9 within Phase 4B) does not engage this framework.

**A3 reference baseline.** α=4, β=3, δ=4, γ=4, η=0.01; ρ≈0.57 at Λ=1.0 under 500-tick equilibrium averaging; analytical fixed point at γ=4 is ρ* ≈ 0.5952. Locked parameter set; reference baseline for Cycle 2 substrate work. Session 9's `current_state.md` mentions reg_01 identity-recovery as most recent substantive finding but does not engage A3 baseline as canonical reference.

### 4.2 Discipline-structure precedents

**Original five standing rules** (per `operations_log/README.md` and `2026-05-14_emulation_discovery.md`). The relationship between these and session-9 `standing_rules.md` Rule 1-10 is not documented. Rule 7 (Section 15 prohibitions lift) appears to extend/supersede some original-five rule content but the mapping isn't explicit.

**Layer 1 architectural review form.** Five documents in `protocols/architectural_reviews/` exemplify the review-output form. Session-9 `protocol_primer.md` describes Layer 1's role but does not point at the precedent reviews.

**Pessimistic-on-passing-tests, sufficiency-tested-not-asserted, joint-necessity admissibility, three-meaning suppression discipline, sufficient-vs-necessary distinction.** Discipline content reproduced in detail across primer documents; session-9 foundational set engages most but not all of these.

**Framing-asymmetry observation as committed practice.** Cycle 1 catch: refinement-driven convergence when one party frames first. Session-9 `protocol_primer.md` engages this; primers extend to "active counter-pressure is committed practice, not optional."

### 4.3 Vocabulary additions

**"Eligibility"** — gatekeeping connotation flagged in `chatgpt_new_chat_primer.md` Section 6 and `gemini_new_chat_primer.md` Section 5 as prohibited. Not in session-9 `vocabulary_quarantine.md` Section 1.

**Damasio biological language wrapper and Haken laser source scrubs.** Named explicitly in primers as historical scrubs. Session-9 `vocabulary_quarantine.md` engages Haken at the approach level (in current_state cross-validated note) but does not document the source-domain scrub history.

### 4.4 Open Element 14

The label `chatgpt_new_chat_primer.md` Section 8 uses ("Open Element 14") is the canonical example of drift-prone vocabulary in session-9 `vocabulary_quarantine.md` Section 3. Whether the Section 3 quarantine was drafted with awareness of the primer's prior use, or whether it surfaced independently and the primer use is what required the quarantine, is not documented.

### 4.5 Personal-context discipline

**Mokie note.** "He had a dog named Mokie who passed away. Do not bring this up unprompted." Plus paragraphs on Mike's ~40-year self-directed study of physics (QFT, complexity science, Lake Vision 2017-2020, path through Bohm/Prigogine/CAS, arrival at Haken's synergetics as formal backbone) and contemplative practice with epistemic discipline around the physics-vs-metaphysical-inquiry boundary. Session-9 foundational set has no personal-context provision.

### 4.6 Environment and toolchain detail

**Production machine specifics.** PowerShell launch sequence, Mesa 3.x API notes (flat namespace, `model.agents.do("step")` pattern, deprecated `RandomActivation`), Notepad-UTF8-BOM hazard, `np.RankWarning` API path change, dependency versions. Session-9 foundational set assumes these implicitly but does not document them.

**Distribution via Python+base64 scripts.** Working pattern named in `new_chat_primer.md` as minimum-thumb-work pattern. Session-9 kit-revision-3 Section 3 (working pattern) has separate but parallel content; relationship not documented.

---

## Section 5: What this inventory does not adjudicate

Per the document role statement, this inventory enumerates and characterizes. It does not determine:

- Whether each prior-cycle item is currently superseded, still authoritative, or requires structural integration into session-9 canonical material.
- The form, location, or content of any reconciliation actions.
- Whether the rule-system relationship (original-five vs. Rule 1-10) is a clean supersession, a substantive extension, or requires explicit mapping.
- Whether the prior-cycle operations logs require any treatment beyond preservation as historical record per the README's honest-record principle.

These adjudications belong to the reconciliation plan deliverable (deliverable 2 of 3 for item 9). The canonical record update (deliverable 3) executes against the reconciliation plan's determinations.

---

— Drafted by Claude as Layer 1 central node, session 10, item 9 deliverable 1 of 3. Inventory complete pending Mike's review.
