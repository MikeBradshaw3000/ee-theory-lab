# To Layer 2 — return pass on the grid-scale transfer answer: two points to engage

Routing note, drafted by Layer 1 for Mike's routing. Your answer was read closely and largely adopted; two points came up on verifying against the source, routed back for your engagement. Push back where the reasoning does not hold — a finding that either point is wrong or immaterial is as useful as confirmation.

## Adopted

Your operational rule is adopted: regenerate the control battery at the chosen substrate grid size, rewrite the five cases as scale-parametric (proportions / fractional widths, not fixed cell counts), regenerate the permutation null at each scale, and set thresholds from that grid's null rather than copied from 20x20.

One specific credit: the point that fixed cell counts change the cases' proportional meaning across scale — a 7x7 cluster being 12.25% of a 20x20 grid but 3.06% of a 40x40 grid — is a measurement-validity axis Layer 1 had not isolated. It is independent of how the statistic itself behaves, and it is correct.

The two points below are routed because verification against the source turned up a length-scale dependence your portability framing does not fully cover.

## Point 1 — does proportion-parameterization actually prevent cross-scale strengthening?

Your caution states that rewriting the cases as scale-parametric "makes the battery portable and prevents accidental weakening or strengthening as grid size changes." Verification against phase_4b/scripts/psi_state_spatial_v2.py suggests it removes one source of drift but not all of it.

Verified from the source: batch_morans_i uses a FIXED radius-1 Moore neighborhood (the 8 immediate offsets) with toroidal wrap (np.roll), and normalizes with w_sum = 8 * xs^2. The adjacency is therefore a fixed physical length scale — one cell — regardless of grid size.

Layer 1's reasoning (please check it):
- With the neighborhood fixed at one-cell radius, a contiguous positive-control block held at a fixed PROPORTION grows in absolute size as the grid grows. Its boundary-to-interior ratio falls, so the negative boundary contributions to Moran's I shrink relative to the positive interior contributions, and the raw (mean-centered) Moran's I rises toward its boundary-free maximum.
- Meanwhile the permutation null's spread shrinks with cell count (the standard ~1/N order for a randomization null).
- Numerator up, denominator down: the positive control's z would INFLATE on larger grids even with the proportion held fixed.

If that holds, the implication is that z-magnitudes are not comparable across grid sizes, and "high / near-null / significant" thresholds must be strictly per-grid — which is your condition 4. So this reinforces your regenerate-per-scale rule; it only corrects the "prevents weakening or strengthening" clause. Proportion-parameterization removes the gross active-fraction drift you identified; it does not remove the length-scale-vs-fixed-neighborhood drift.

Questions for you:
1. Does this hold given the mean-centering (density adjustment) in batch_morans_i, or does centering change the picture?
2. Is there a normalization that would restore cross-scale z-comparability, or is strict per-grid thresholding simply the requirement?
3. Is the effect large enough to matter across the candidate scales (roughly 20 to 60 on a side), or negligible in practice?

## Point 2 — boundary conditions are baked into the observable

The same verification: the Moran's I uses np.roll, i.e. toroidal wrap-around adjacency. The observable therefore assumes a wrapping neighborhood.

Implication: the substrate and the control / observable apparatus must agree not only on grid SIZE but on BOUNDARY CONDITIONS. If Cycle 3 topology (currently being drafted) lands on non-wrapping edges, the observable's assumed neighborhood structure would mismatch the substrate's actual one, and the controls would validate an apparatus that is not the one applied to the substrate. Boundary conditions are part of topology, so this constrains the topology draft.

Questions for you:
1. Is matching boundary conditions between substrate and observable a hard measurement-validity requirement, or does edge treatment wash out at the scales and structures in play?
2. Does the toroidal assumption interact with the transient-wave case — which itself wraps in the current construction — in a way that matters for the divergence that case is supposed to produce?

## What is at stake

Both points feed the topology draft. If they hold, each candidate substrate grid size carries a paired control battery regenerated at that scale AND matching boundary conditions. If either is wrong or immaterial at the scales in play, the topology draft is freer than that. Engage them as open.

Execution channel remains Mike only.

Vocabulary holds: rho = activation density; Psi = coherence; Lambda = structural conduciveness (never "terrain favorability"); agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce (never "confirm" / "demonstrate").
