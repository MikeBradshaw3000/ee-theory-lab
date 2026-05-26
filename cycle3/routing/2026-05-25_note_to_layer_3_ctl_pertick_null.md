# To Layer 3 — C3-CTL-001 battery: accepted set verified; one required addition + minors

Routing note, drafted by Layer 1 for Mike's routing. Layer 1 reviewed the runnable battery against the accepted revision set. The accepted revisions are correctly implemented and the battery produces the full designed discrimination: A high on both, B and C near zero on both, D the divergence (per-tick high, persistence zero), E near zero on both with the uniformity degeneracy flagged. The E rewrite in particular works — it now reads near zero per-tick, restored as the genuine degeneracy control and distinct from D. Good work. One required addition before the apparatus is complete, plus three minors.

## Required addition - a grid-local permutation null for Psi_meanI_state

The battery computes a permutation-null z only for the persistence observable (the Persistence_Z column). It computes no null for the per-tick observable, Psi_meanI_state. The Cycle 2 v2 apparatus computed both; this implementation kept only the persistence null.

This is required, not optional. The measurement-validity finding settled for Cycle 3 requires every "high / near-null / significant" threshold to come from this grid's own null distribution. As written, Psi_meanI_state's high-versus-near-null rests on bare magnitude with no grid-local null behind it - which is the "a value without its control is ambiguous" failure Cycle 2's lessons name. When this apparatus is later applied to real substrate, Psi_meanI_state will need its own grid-local null to be interpretable; the control battery has to validate that mechanism, not only the persistence one.

The fix mirrors the persistence-null logic at the per-tick level:
- For the null, shuffle the per-cell values WITHIN each tick, preserving that tick's exact active count - so the null isolates spatial arrangement from density, the same principle the persistence null uses.
- Build the null distribution for the aggregate Psi_meanI_state statistic: for each permutation, shuffle every tick independently and recompute the windowed mean of per-tick Moran's I, giving one null sample; repeat across permutations. (v2's per-tick-shuffle structure is the reference.)
- Report a z-score for Psi_meanI_state alongside Persistence_Z, so each observable's value carries its own grid-local null.

Keep it symmetric: this is a null for the per-tick observable, not a device that privileges one candidate. Both observables get grid-local nulls; neither is pre-loaded.

Expected behavior to confirm after the addition (confirm, do not hardcode): A and D show a high per-tick z; B, C, and E show a per-tick z near zero. Together with the persistence null, that makes the discrimination null-grounded for both observables.

(The per-tick null is heavier than the persistence null - it is per-tick across the window rather than once per case - so vectorize as needed; it is well within budget at this grid size.)

## Minors (non-blocking)

- Output path: write under cycle3/ (a Cycle 3 output location), not a bare data_out/ in the working directory - record hygiene.
- Environment: the run targets the captured venv per C3-ENV-001 (Python 3.14.4, numpy 2.4.4, pandas 3.0.3). Execution is Mike's; ensure the script carries no assumption against that environment.
- Seed: keep a fixed, recorded RNG seed for reproducibility (the current 42 is fine); the test record will record it.

## Deliverable

The revised runnable battery, for Layer 1 review and then Mike's execution. This remains C3-CTL-001; it clears L1 / L2 only by construction. Any computed magnitudes - analytical or from any sandbox check - are predictions until Mike's canonical run; they are not results and are not recorded as such.

Execution channel remains Mike only.

Vocabulary holds: rho = activation density; Psi = coherence; Lambda = structural conduciveness (never "terrain favorability"); agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce (never "confirm" / "demonstrate").
