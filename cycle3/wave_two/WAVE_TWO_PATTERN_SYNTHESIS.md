# Wave-two pattern-level synthesis (four readings carried; Reading-D pure-read program OPENED)

**Status: SYNTHESIS. Layer 2-reviewed 2026-07-02; Mike-arbitrated (synthesis committed AND the Reading-D pure-read program opened in the same motion). NON-SEEDING (the opened program is pure-read on committed data; no run, no Layer 3). Closes NO mechanism class; touches NO L4 question.** Governing findings files govern each arc's result over this restatement. This document records what the accumulated wave-one + wave-two pattern jointly says, the four readings carried forward with L2's weighting, the discrimination criteria, and the predeclared design of the opened pure-read program.

## The pattern (committed record)

Wave one: 97/97 non-degenerate lifted rows positive on Psi_meanI_state_z (min ~139), zero near-null. Comparator 0: the lifted i.i.d. Lambda-only floor reads near-null (near-null is apparatus-reachable; only trivially). Comparator epsilon: the floor is stable to weak separate-process perturbation. Rule C M2: LowLow only floor-adjacent (A-prime). Rule D R3: turnover never produces joint near-null at responsive coupling. Rule E first pass: unbounded gain rails; the one window-level LowLow cluster was a lag-dynamics artifact, guard-rejected. Rule E bounded-A: amplitude repaired, channel saturated at every tier; zero LowLow in 450 windows.

**The invariant (L2-corrected wording; carry this form):** Every lifted, non-degenerate mechanism-produced regime tested so far is NON-NEAR-NULL on the co-equal observable pair, with positive Psi_meanI_state recurring as the most robust axis. Persistence may be positive or negative depending on mechanism and sign (Rule C/D negative-persistence regimes were organized but not positive-both-axes), but joint near-null has not appeared away from the floor or a rejected artifact. **Sub-invariant (stronger, and tied to the pair-level argument): lifted-near-null Psi_meanI_state has essentially never appeared in a valid mechanism-produced regime.**

## The pair-level structural argument (Layer 2 contribution)

On the Moore-radius-1 lattice, adjacent cells have OVERLAPPING neighborhoods, so their local exposure variables q_i, q_j are positively correlated by geometry. First-order around the lifted density, Cov(p_i, p_j) ~ [b'_eff(rho)]^2 * Cov(q_i, q_j): the SQUARE removes the coupling sign, so the birth-propensity surface is positively spatially autocorrelated under BOTH contagion and divergence coupling, whenever a live local rule has nonzero effective slope. This explains the table's shape: Comparator 0 is near-null because there is no local propensity surface; every live local mechanism creates one, and neighborhood overlap converts it into per-tick organization. LIMIT: the argument predicts nonzero positive organization PRESSURE, not the observed magnitude - not necessarily large z, not necessarily positive persistence, not impossibility of cancellation. It is a structural reason for Reading B, not a theorem. Empirical discriminator: the neighbor autocorrelation of the birth-propensity surface p_i (not just the realized active state); if predicted propensity autocorrelation tracks observed Psi_meanI_state across Rule C/D/E settings, Reading B strengthens; if z stays huge where raw propensity autocorrelation is tiny, Readings C/D gain weight.

## The four readings (all carried; L2 weighting, asymmetric)

**A - the search is incomplete.** LIVE, NARROWED to one specific form: the untested CLEAN-RESPONSIVE rescaled Rule E channel (B/C conditioned-scale territory). Bounded-A showed output-amplitude bounding fixes runaway without creating responsiveness; a properly rescaled macro argument has never been tested. A stays live in that form only; availability of an untried instrument is not itself evidence.

**B - the substrate couples lift to organization.** NOW THE STRONGEST WORKING APPARATUS-LEVEL HYPOTHESIS within the tested local / block-lagged families - a working hypothesis, NOT a closure. The pair-level argument supplies structural support; the contract-core hardening warning remains binding (the wave-one absence is not converted into a prediction; the mechanism-class distinction wave two tests stays open).

**C - the signature question.** LIVE, FENCED: the co-equal pair might not be the presentation of the theory's second regime on this substrate. In scope only as a measurement-behavior question (how the observables behave under lift); what they MEAN is the L4 question, Mike's domain, untouched by this synthesis and by any read it opens.

**D - apparatus scale / null sensitivity (L2 addition; Layer 1's framing missed it).** The co-equal observables may be statistically overpowered under lifted mechanism-produced trajectories: the permutation null is grid-local, and very large z may reflect null power rather than large raw organization. Distinct from C (apparatus-level, testable without L4). Comparator 0 already blocks the crude form (high rho alone does not force positive z) but does not settle whether tiny raw correlations become overwhelming z under mechanism-produced lift. Reading D could explain why Reading B looks so strong.

## Discrimination criteria (carry verbatim)

- **A vs B hinges on whether a genuinely responsive mechanism remains possible, not on the count of negatives.** A future B/C rescaled-argument pass is discriminating ONLY IF it occupies the clean-responsive regime (non-inert, non-saturated, non-oscillatory, non-degenerate, sign-local reach retained, effective Lambda varying in the graded part of the response). Clean-responsive + no LowLow -> B gains substantially. Clean-responsive + guarded joint near-null -> A vindicated (prior failures calibration-limited). Saturated/inert/oscillatory again -> distinguishes nothing; Rule E remains hard to calibrate. Raw effects tiny with huge z -> D/C-measurement gains.
- **B vs C/D separates raw spatial effect from z-score significance.** Large visible raw organization across independent diagnostics -> B. Small raw effects with enormous z -> D (and soft-C at measurement level).
- **A vs C separates at measurement-behavior level only:** if many independent spatial diagnostics agree lifted mechanism regimes are organized, A weakens/B strengthens; if the co-equal pair is strongly signed while other diagnostics read near-null/ambiguous, C gains measurement-level weight. None of this resolves L4.

## The Reading-D pure-read program - OPENED (Mike-arbitrated 2026-07-02)

Purpose: separate raw spatial effect size from z-score significance on the EXISTING committed trajectories - no seed, no Layer 3, pure read of committed NPZs across Comparator 0, Rule C M2, Rule D R3, and both Rule E passes. Predeclared diagnostics (per lifted, non-degenerate setting; per-seed aggregation; read against the discrimination criteria above, pessimistic-on-passing):

1. RAW Moran's I effect sizes reported alongside the existing z-scores, for both co-equal observables, with cross-instrument comparison anchored to Comparator 0's raw floor values.
2. Spatial-shuffle control preserving rho_t: per-tick random permutation of cell positions (destroys spatial structure, preserves the density trajectory exactly); recompute both observables. A raw effect that is sizable before shuffling and vanishes under it supports B (real spatial organization); a z-story that survives controls or dwarfs raw effect size supports D.
3. Time-shuffle control preserving per-cell persistence: permute tick order per trajectory (preserves each cell's occupancy fraction, breaks temporal ordering); recompute persistence-axis behavior.
4. Supplementary spatial diagnostics where the primary reads are ambiguous: cluster-size distribution, connected-component count, interface length, pair-correlation length. (Named; computed only if 1-3 under-determine; scope creep fenced.)
5. The pair-level empirical discriminator: neighbor autocorrelation of the reconstructed birth-propensity surface for Rule C/D/E settings, compared against observed Psi_meanI_state.

Predeclared discrimination outcomes: raw-large + shuffle-kills -> B strengthens; raw-tiny + z-huge -> D strengthens (and soft-C at measurement level); propensity autocorrelation tracks meanI -> B strengthens via the structural argument; divergent diagnostics -> recorded as under-determination, not forced. The program PRODUCES or FAILS TO PRODUCE discrimination; no outcome resolves L4, closes a mechanism class, or reclassifies any rested arc's result. Read design and scripts route through Layer 1 drafting and Mike execution; results route to Layer 2 before any synthesis update.

## What this synthesis does not do

Does not seed a run. Does not open B/C or any instrument (the B/C design question is HELD pending the pure-read results, per the A-vs-B hinge). Does not close any mechanism class. Does not resolve or move L4. Does not harden the weak-form Rule B prior. Does not reclassify any rested arc. The arbitration of whether wave two ultimately continues, redirects, or rests remains Mike's, downstream of the pure-read results.

- Layer 1 (Claude); Layer 2-reviewed (pair-level argument, invariant correction, Reading D, and weighting are L2 contributions, recorded as genuine engagement); Mike-arbitrated
