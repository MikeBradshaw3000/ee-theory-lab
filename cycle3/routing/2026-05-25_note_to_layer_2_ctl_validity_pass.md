# To Layer 2 — independent validity pass on the C3-CTL-001 control-battery draft

Routing note, drafted by Layer 1 for Mike's routing. The C3-CTL-001 design phase is open. Layer 3 has drafted the scale-parametric synthetic control battery at the locked topology. This is the L2 measurement-validity pass the design phase calls for — an independent review against the pre-registered criteria. The ask is at the end.

## Topology (locked) and apparatus

50 x 50, Moore radius 1 (8-neighbor), toroidal. Because this matches the Cycle 2 observable encoding, the observable carries over: Psi_meanI_state and Psi_persistence_I, both Moran's-I-based on the 8-neighbor toroidal adjacency, parametric in grid size. They are a co-equal pair; which one (if either) IS Regime-II coherence is an open L4 question and is not in scope here.

## Pre-registered acceptance criteria (the target the draft must meet)

Stated before the draft, per case, on BOTH observables:
- Case A (positive, stable cluster): both observables high.
- Case B (negative, random low-rho): both observables near zero.
- Case C (negative, random high-rho): both observables near zero.
- Case D (transient wave, the divergence case): Psi_meanI_state high, Psi_persistence_I near zero — the divergence, recorded as data.
- Case E (degeneracy, uniform high persistence): both observables near zero, with the permutation-null z / P_std separating the uniformity degeneracy.

All "high / near-zero / significant" thresholds taken from this grid's own null distribution; no cross-scale magnitude comparison. Case definitions must be scale-parametric (proportions / fractional widths, not fixed cell counts). Co-equal-pair guard: nothing should pre-load one observable, and Case D's divergence must be genuinely produced.

## Layer 3's draft (under review — verbatim)

Global apparatus: 50 x 50 (N = 2500), Moore radius 1, toroidal, window 100 ticks, 199 permutations. Layer 3's rationale: a 100-tick window is divisible by the 50-column dimension so moving structures wrap an integer number of times without partial-sweep artifacts; 199 permutations give ~0.005 p-resolution.

- **Case A — stable cluster (positive).** Target rho 0.10. A contiguous 10 x 25 block set active, static across all 100 ticks. Layer 3 expects Psi_meanI_state high (contiguous block) and Psi_persistence_I high (binary 1.0/0.0 persistence map, maximal clustering).

- **Case B — random low-rho (negative).** Target rho 0.10. Each tick, per-cell active-state values assigned independently at probability 0.10. Layer 3 expects Psi_meanI_state near zero (random per tick) and Psi_persistence_I near zero (time-averaged map uniformly noisy).

- **Case C — random high-rho (negative).** Target rho 0.80. Each tick, per-cell values assigned independently at probability 0.80. Layer 3 expects both observables near zero, confirming the apparatus isolates structure from density.

- **Case D — transient wave (divergence case).** Target rho 0.10. A continuous vertical band exactly 5 columns wide (0.10 x 50), advancing 1 column per tick, wrapping toroidally; it traverses the 50 columns exactly twice in 100 ticks, so every cell is active exactly 10 of 100 ticks. Layer 3 expects Psi_meanI_state high at every tick (structured 5-column band) and Psi_persistence_I near zero / degenerate (persistence value of every cell exactly 0.10 -> uniform map -> zero spatial variance).

- **Case E — uniform high persistence (degeneracy check).** Target rho 0.70. A continuous vertical band exactly 35 columns wide (0.70 x 50), advancing 1 column per tick, wrapping toroidally; every cell is active exactly 70 of 100 ticks. Layer 3 expects the persistence map perfectly uniform (every cell 0.70), spatial variance zero, P_std dropping to zero and correctly flagging the uniformity degeneracy — testing the statistical safeguard at high rho without a fully saturated rho = 1.0 grid.

## The ask — independent L2 validity pass

For each of the five cases as drafted, does the construction actually produce its pre-registered expected output on BOTH observables, under the 8-neighbor toroidal Moran's I at 50 x 50? Verify rather than assume: reason through (or compute) what each case's Psi_meanI_state and Psi_persistence_I would actually be as constructed, and flag any case where the construction would not meet its criterion. Confirm the scale-parametric definitions are valid at this topology, that thresholds are correctly local to this grid's null, and that the co-equal-pair guard holds (Case D's divergence genuinely produced; nothing quietly pre-loading one observable). A finding that any case fails its criterion, or that any case is not distinct from another, is the point of the pass — report it.

Execution channel remains Mike only.

Vocabulary holds: rho = activation density; Psi = coherence; Lambda = structural conduciveness (never "terrain favorability"); agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce (never "confirm" / "demonstrate").
