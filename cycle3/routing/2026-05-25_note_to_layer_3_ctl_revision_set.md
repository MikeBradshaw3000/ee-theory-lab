# To Layer 3 — C3-CTL-001 revision set accepted: revise B, C, E; keep A and D

Routing note, drafted by Layer 1 for Mike's routing. The L2 validity pass converged with Layer 1's review. A and D stand exactly as you drafted them; B, C, and E revise. Implement the revised battery as runnable, for Layer 1 review and then Mike's execution.

## On the magnitudes you may have seen

The validity review included computed Moran's I magnitudes (for orientation, roughly 0.886, 0.833, 0.929 across cases). Those are analytical predictions, not run outputs. They are not results and must not be recorded or cited as results anywhere. The battery's actual values come only from execution, which is Mike's channel; the test record's pass is earned there, not from a reasoned magnitude.

## Accepted as drafted — do not change

- Global apparatus: 50 x 50 toroidal Moore-1, 100-tick window, 199 permutations. Your window / permutation rationale stands (100 divisible by the 50-column width; 199 giving ~0.005 resolution).
- Case A (stable cluster, positive): the static 10 x 25 block at rho 0.10. Stands.
- Case D (transient wave, divergence case): the 5-column band advancing 1 column per tick, wrapping, every cell active exactly 10 of 100 ticks. Stands. This is the case that genuinely produces the co-equal-pair divergence; leave it intact.

## Revisions

### Case B — tighten to exact-count random

Replace the per-cell Bernoulli(0.10) with exact-count random placement: exactly 250 active cells per tick (250 / 2500 = 0.10 exactly), randomly placed each tick. Bernoulli reaches rho 0.10 only in expectation; the exact count holds the density identical to Case A, and that shared exact rho is what makes B the structure-versus-density control.

### Case C — tighten to exact-count random

Same change: exactly 2000 active cells per tick (2000 / 2500 = 0.80 exactly), randomly placed each tick.

### Case E — rewrite to the uniform-persistence degeneracy control (not a moving band)

The drafted 35-column moving band fails the pre-registered criterion. Per tick it is a highly structured two-region split (35 active columns against 15 inactive), so Psi_meanI_state reads high, not near zero — it is a second high-rho transient-band case, not the degeneracy control, and it collapses into a wide twin of Case D.

Rewrite E to the uniform-persistence logic: every cell active in exactly 70 of 100 ticks, with each cell's active ticks independently shuffled. That produces a uniform persistence map (P_i = 0.70 for every cell, so persistence-grid variance is zero and Psi_persistence_I is degenerate) AND unstructured per-tick configurations (so Psi_meanI_state is near zero). Both observables near zero, with P_std flagging the uniformity — the genuine degeneracy control.

(Exact per-tick rho = 0.70 is optional. A balanced random matrix would give it, and you may choose that for consistency with the exact-count discipline applied to B and C. The essential requirement is uniform cell-level persistence with no spatial structure at individual ticks.)

## Co-equal-pair guard

After the E rewrite, D and E are properly distinct: D is the transient-structure divergence (per-tick organization high, persistence zero because the structure moves); E is the degeneracy case (both observables near zero, persistence zero because the map is uniform, flagged by P_std). Neither pre-loads one observable. Keep them distinct — that distinction is what the battery needs.

## Deliverable

Implement the revised battery as a runnable script at 50 x 50 toroidal Moore-1. The observable carries over from the Cycle 2 v2 encoding (8-neighbor toroidal Moran's I, parametric in grid size) — write the Cycle 3 battery fresh; do not overwrite that canonical file. Deliver the runnable script for Layer 1 review prior to Mike's execution; execution is Mike's channel. This is C3-CTL-001; it clears L1 / L2 only by construction.

Execution channel remains Mike only.

Vocabulary holds: rho = activation density; Psi = coherence; Lambda = structural conduciveness (never "terrain favorability"); agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce (never "confirm" / "demonstrate").
