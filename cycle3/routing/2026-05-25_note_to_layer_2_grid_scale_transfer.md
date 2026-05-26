# To Layer 2 — measurement-validity question: does the control-battery discrimination transfer across grid scale?

Routing note, drafted by Layer 1 for Mike's routing. A concrete analytical question that gates the next implementation step.

## Current-status anchor

- Cycle 2 is closed and tagged (cycle2-close). Cycle 3 is open.
- C3-ENV-001 (environment reproduction) is closed at L1 and is the only gate cleared. C3-CTL-001 (synthetic control battery) and C3-SS-001 (steady-state eligibility apparatus) are planned preconditions; the substantive Regime-II probes are not yet designed.
- The two candidate observables — Psi_meanI_state (per-tick state organization that persists) and Psi_persistence_I (the same cells persistently clustered) — are held as a co-equal pair. Which one, if either, IS Regime-II coherence is an open ontological question for Mike / Layer 1 (L4), settled on relational-mutual-reinforcement grounds — never by statistic robustness or substrate mechanics. Nothing below is asking you to choose between the pair.
- The four-level distinction governs every test: L1 implementation, L2 measurement validity, L3 steady-state eligibility, L4 interpretation. The question below is squarely L2.

This sits under the standing discrimination question already routed to you (what analytical structure on the Lambda -> rho -> Psi cascade would let a probe discriminate between the two candidates rather than merely be consistent with one). It is a concrete sub-question that gates an immediate decision, not a replacement for that larger one.

## The carried-forward control battery

Cycle 3 inherits the Cycle 2 five-case synthetic control battery as its minimum requirement. It uses no ABM substrate by construction — synthetic arrays only — which is how it sidesteps substrate trust. As run in Cycle 2:

- Grid: 20 x 20 (400 cells). Window: 100 ticks. Permutation null: 199 permutations.
- Case A (positive — stable cluster): contiguous 7x7 block, 49 cells, rho = 0.1225.
- Case B (negative — random low-rho): 49 randomly placed cells, rho = 0.1225 — deliberately the SAME rho as A, isolating structure from density.
- Case C (negative — random high-rho): 320 random cells, rho = 0.80.
- Case D (transient wave): a 3-column block shifting one column per tick (wrapping), 60 cells, rho = 0.15.
- Case E (degeneracy — uniform high persistence): every cell active in exactly 70 of 100 ticks, independently shuffled.

It produces the designed discrimination: A high on both observables; B and C near zero on both; D diverges by design (Psi_meanI_state high, Psi_persistence_I near zero) and that divergence is recorded as data; E near zero, with the permutation-null z separating the uniformity degeneracy from true signal.

## The question

Cycle 3's substrate grid size (the lattice scale) is a topology decision not yet committed. The battery was validated at 20 x 20. The purpose of validating the battery is so that the SAME observable apparatus, applied later to real-substrate output, is trusted to measure what it claims.

Does the discrimination the battery produces transfer across grid scale? Two possibilities, laid out without preference:

1. **The permutation-null z standardizes it.** Each observable's z-score is computed against its own permutation null at the given grid size. If that standardization is what carries the discrimination (positive -> high z; negatives and degeneracy -> near-zero z; transient wave -> the designed divergence), then a battery validated at 20 x 20 may license trusting the same apparatus on a substrate of a different size, and the control grid size and substrate grid size can be chosen independently.

2. **The magnitudes and null variances shift with scale.** If the raw observable values and the null distribution's spread move enough with grid size that the discrimination thresholds do not transfer, then the controls must be regenerated at the substrate grid size for the validation to hold, and the two grid sizes must be chosen jointly.

Which holds, and under what conditions? This is symmetric across the co-equal pair — it asks whether the discrimination transfers, for both observables, not which observable is preferred.

## Why this gates the next step

The answer determines whether the substrate grid size (a topology parameter Layer 3 is about to draft) is free, or must be chosen together with the control battery. We are holding substrate/topology drafting until this is settled, so the grid size is not baked in blind to the transfer question.

## What is being asked

Not to ratify a plan — to determine the analytical answer. A finding that the discrimination does NOT transfer cleanly, or transfers only conditionally, is as useful as a positive one; it changes how the battery must be parameterized. If the question is itself mis-posed — if there is a third structure that makes the grid-size dependence the wrong axis to worry about — say so.

For a fuller re-orientation to current state if needed: protocols/foundational/ (current_state.md, theoretical_context.md, vocabulary_quarantine.md).

Execution channel remains Mike only.

Vocabulary holds: rho = activation density; Psi = coherence; Lambda = structural conduciveness (never "terrain favorability"); agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce (never "confirm" / "demonstrate").
