

---
# FILE: C:\Users\vkz244\Downloads\operations_log_README.md
---

# Operations Log

This directory holds the operational record of decisions, gate closures, discipline events, and protocol additions across the project's history. Originally opened during Cycle 2 substrate work in May 2026; continues forward through Phase 4B and beyond.

## Entry conventions

- **Filename format:** `YYYY-MM-DD_topic.md`. Date is the date of the event, not the date of writing.
- **Authorship:** Entries are drafted by AI partners in collaboration with Mike, with the drafting partner noted at the bottom of each entry.
- **Honest record principle:** Entries reflect the operational record at the time of writing, including failures, miscalibrations, and corrections. Entries are not curated history. When a later entry corrects an earlier one, both stay in the log — the earlier entry is not retroactively edited.
- **Discipline notes:** Many entries include explicit notes on what the discipline structure caught and what it missed. These are part of the record, not editorial commentary.

## Cross-references

- **Foundational document set:** `../protocols/foundational/` — entry point at `README.md`. Contains the protocol primer, standing rules, vocabulary quarantine, canonical artifacts index, current state, theoretical context, environment reference, and personal context.
- **Substrate Spec v1.1:** `../flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf`
- **Architectural reviews:** `../protocols/architectural_reviews/` — Layer 1 architectural review outputs, parallel to operations logs.
- **Prior-cycle onboarding primers:** `../protocols/onboarding/` — superseded by foundational set; preserved as historical record.

## Standing rules

The standing rules current as of session 9 onward are documented in `../protocols/foundational/standing_rules.md` (Rule 1 through Rule 10).

A *five-rule list* originally appeared in this README and documented the rule system as it existed 14 May 2026. The five-rule list was the protocol's standing-rules state at the close of Cycle 1 / opening of Cycle 2. That historical content is preserved at two locations:

- `2026-05-14_emulation_discovery.md` — the operations log entry documenting the rule system's origin event (the Cycle 2 Round 1 A3 parity moment that surfaced Gemini's synthetic 10-seed table) and the rules' formulation.
- `../protocols/foundational/standing_rules.md` — historical lineage section at the document's end, including the original five-rule list verbatim and the mapping to current Rule 1-10.

For current rule content (Rule 1 through Rule 10), consult `../protocols/foundational/standing_rules.md`. For rule-system history, consult both locations above plus the operations logs from 14-16 May 2026 (which document the rules' formation and subsequent refinement).

## Directory scope

This directory contains operations logs across the project's history. Some entries predate the session-numbering convention currently used in Phase 4B work; those use date-and-topic naming (e.g., `2026-05-14_emulation_discovery.md`, `2026-05-15_flight_2_closure.md`). Session-numbered entries (`2026-05-18_phase_4b_session_5.md` and forward) follow the session-numbering convention adopted as Phase 4B opened. Both naming patterns are operative; the date is always the date of the event.



---
# FILE: C:\Users\vkz244\Downloads\onboarding_README.md
---

# protocols/onboarding/ — Prior-Cycle Material (Superseded)

This directory contains prior-cycle primer documents drafted 15 May 2026 for fresh AI partner instantiation into Cycle 2 Round 1. The four documents are:

- `new_chat_primer.md` — Claude primer
- `chatgpt_new_chat_primer.md` — ChatGPT primer
- `gemini_new_chat_primer.md` — Gemini primer
- `chatgpt_routing_note.md` — routing-note exemplar

**Status: Superseded as cold-start primer surface.** The current cold-start surface for fresh Claude instances is the instantiation kit (kit-revision-3 or later) plus the foundational document set at `../foundational/`. The four files in this directory are preserved as historical canonical record per the honest-record principle (see `../../operations_log/README.md`).

**Why the directory exists.** Session 10's item 9 reconciliation (`PRIOR_CYCLE_INVENTORY.md` and `PRIOR_CYCLE_RECONCILIATION_PLAN.md` at workspace root) surfaced these documents as prior-cycle canonical material that the session-9 foundational set did not initially engage. The reconciliation determined the directory's status as superseded and migrated substantive carry-forward content to the foundational set; the original documents stay in place as historical record.

## Substantive content migrated to the foundational set

The four primer documents carried substantive content not present in the session-9 foundational set. Session 10's reconciliation migrated that content into the canonical record at the following locations:

- **Two-paper structure** (AMR foundation paper + methodology/substrate paper) → `../foundational/theoretical_context.md` Section 1.
- **Four Grand Challenges** (nucleation, network topology, narrative dynamics, empirical calibration) → `../foundational/theoretical_context.md` Section 2.
- **Cycle 1 / Cycle 2 framework** → `../foundational/theoretical_context.md` Section 3.
- **A3 reference baseline** (parameters, ceiling, candidate history) → `../foundational/theoretical_context.md` Section 4.
- **Vocabulary scrub history** (Damasio, Haken) → `../foundational/vocabulary_quarantine.md` Section 4 and `../foundational/theoretical_context.md` Section 5.
- **Original five standing rules** and their lineage to current Rule 1-10 → `../foundational/standing_rules.md` "Historical lineage" section.
- **"Eligibility" prohibition** → `../foundational/vocabulary_quarantine.md` Section 1.
- **Open Element 14 historical reference** → `../foundational/vocabulary_quarantine.md` Section 3.
- **Personal context** (intellectual lineage, contemplative practice, Mokie) → `../foundational/personal_context.md`.
- **Environment/toolchain detail** (workspace, Python version, dependencies, PowerShell hazards) → `../foundational/environment_reference.md`.

## Deferred items

**ChatGPT and Gemini onboarding under session-9 framework.** The session-9 foundational set is Claude-focused; the original ChatGPT and Gemini primer documents in this directory are anchored to Cycle 2 Round 1 Post-Flight-2-Closure state, which has moved substantially since. Salvaging them as still-authoritative would require substantial rewriting against current state, which was reconciliation-creep beyond item 9's scope. ChatGPT and Gemini onboarding under the current framework is a deferred item; see `../../STANDING_ITEMS.md` for the open item if registered.

## Authority

The four documents in this directory are *historical canonical record*, not current authoritative material. When their content conflicts with current foundational documents, the current foundational documents win. When the content is preserved unchanged in foundational documents (e.g., the original five standing rules in `../foundational/standing_rules.md`'s historical lineage section), the foundational document is the citation-target for active work.

For current orientation, see `../foundational/README.md` (foundational set entry point) and the instantiation kit (delivered via session-handoff folder).



---
# FILE: C:\Users\vkz244\Downloads\architectural_reviews_README.md
---

# protocols/architectural_reviews/

This directory holds Layer 1 architectural review outputs — Claude's pre-execution reviews of substrate code, analysis scripts, and architectural artifacts. The directory is open for new entries as future Layer 1 review work fires.

## Authority and role

The architectural reviews are *historical canonical record* of Layer 1's structural reviews. Each review documents what was checked, what passed, what was deferred or flagged. The directory is parallel to `../../operations_log/` (which holds session-by-session decisions and discipline events); architectural reviews focus on code/artifact verification.

Per the honest-record principle (see `../../operations_log/README.md`), entries are not retroactively edited. When a later review corrects or supplements an earlier one, the earlier entry is preserved; the correction lives in a new entry or in a footnote on the original (e.g., `2026-05-14_a3_parity_code_review.md` carries a post-review footnote registering that the code reviewed was never executed on the production machine).

Layer 1 review scope is *primitive compliance, vocabulary quarantine, drive function form, structural compliance with specifications* — not execution status. Reviews state their scope explicitly; what's outside scope is not implicitly verified. Where execution status is verified separately (e.g., per standing Rule 1's primary-source-check discipline), the verification is logged separately.

## Filename conventions

`YYYY-MM-DD_topic.md` matching the operations log convention. Date is the date of the review, not the date of writing.

## Cross-references

- **Foundational document set:** `../foundational/` — entry point at `README.md`. Defines Layer 1's role (`protocol_primer.md`), the standing rules under which reviews operate (`standing_rules.md`), and the vocabulary discipline (`vocabulary_quarantine.md`).
- **Operations logs:** `../../operations_log/` — session-by-session record. Architectural reviews are cross-referenced from operations logs when the review's findings affected session work.

## Current entries

As of session 10:

- `2026-05-14_a3_parity_code_review.md` — Cycle 2 Round 1 A3 parity moment review (PASS within scope; footnote registers post-review discovery that the code was never executed).
- `2026-05-14_flight_1_v1_1_implementation_review.md` — Flight 1 NumPy v1.1 substrate review (PASS; five deferred remediations identified).
- `2026-05-14_v1_1_divergence_review.md` — v1.1 / A3 drive function "divergence" review (analysis correct, framing wrong; footnote documents the framing correction).
- `2026-05-15_flight_2_analysis_script_review.md` — Flight 2 analysis script review (PASS).
- `2026-05-15_flight_2_substrate_review.md` — Flight 2 production substrate review (PASS).

Future reviews land in this directory as Layer 1 review work fires.

