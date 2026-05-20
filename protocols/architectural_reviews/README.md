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
