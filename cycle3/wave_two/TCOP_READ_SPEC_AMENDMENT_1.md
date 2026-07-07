# TCOP read spec — Amendment 1 (CANONICAL; Mike-arbitrated 2026-07-06)

**Status: CANONICAL AMENDMENT to TCOP_READ_SPEC.md (placement digest 56AAD2CF…93C0). Completes the spec's Section 7 path-(a) rule. Lineage: L1 drafted tcop_read.py per the canonical spec → Mike routed the script to L2 for a pre-execution hostile build review (a safety step beyond the spec's required sequence) → L2 verdict: reject-as-execution-ready; one blocker (B1) + six amendments (D1–D6) + claims 1/7/8 hardening → the B1 blocker exposed an internal tension in the ratified spec text itself: Section 7's preamble ("outcome is evaluated only inside bins where G1–G4 pass and G3 eligibility holds") versus the path-(a) sentence's use of the global Section 3.2 setting-onset flag → resolution is a spec clarification, not a code accommodation → joint L1+L2 recommendation for the bin-qualified reading → Mike arbitrated 2026-07-06: option (i), bin-qualified. This amendment governs; on any discrepancy with the placed spec's Section 7 path-(a) sentence, this amendment wins.**

## Amendment text (replaces the operational content of the Section 7 path-(a) failure rule)

The Section 3.2 setting-level onset flag remains the global flag, computed from all nine primary windows per row across the seed set, and is reported for every setting. It is necessary but NOT sufficient for a path-(a) risky-form failure.

A c = 0 setting-level risky-form failure under path (a), on an axis, requires jointly:

1. the Section 3.2 setting-level onset flag at (tier > 0, c = 0) on that axis;
2. verified common-mode lift for that tier (all five c = 0 seed rows pass G1; per-row results reported);
3. the onset evidence represented inside at least one G3-ELIGIBLE path-(a) bin — that is, at least one exceeding primary window from the flagged c = 0 setting lies in an eligible bin of a path-(a) comparison pair, where the contributing rows pass G4 and (being nonzero-tier) G1 per the outcome-bin gate fencing.

Sentinel c = 0 events remain surfaced separately and unsuppressed; each is tagged G3_eligible = true iff it lies in an eligible path-(a) bin. A sentinel alone never constitutes the setting-level failure. Windows from gate-failed rows, out-of-support bins, count-failed bins, seed-failed bins, or phase-confounded bins are apparatus limits and never count toward a path-(a) failure — consistent with the spec's own rule that gate-failed regions are never evidence for or against.

## Grounds on record

(L2, the blocker) the as-drafted code could label a path-(a) risky-form failure from windows that were out-of-support, phase-confounded, count-failed, or from G4-failed rows, violating the outcome-bin fence. (L1, concurring) the global reading is internally inconsistent with the spec's "gate-failed regions are never evidence for or against"; the sentinel layer already preserves every raw event, so the qualification hides nothing. Convergence-tracking note: joint L1+L2 recommendation; Mike arbitrated with full authority to take the global reading and chose the bin-qualified rule.

## What this amendment does not do

Does not alter any threshold, floor, bin rule, dominance rule, onset flag definition, or comparison universe; does not weaken the sentinel record; does not execute the read or authorize execution; does not reclassify Comparator 0; does not move L4; does not touch CM-2, Rule E B/C, or the 9-window earned-window open item.
