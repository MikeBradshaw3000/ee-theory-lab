# To Layer 3 — C3-CTL-001 design phase open: build the paired control battery at 50 x 50 toroidal Moore-1

Routing note, drafted by Layer 1 for Mike's routing. The CTL design phase is open. This is substrate-led design: Layer 1 states the settled acceptance criteria as the target; the genuinely open parametric choices are yours; Layer 2 reviews validity against these criteria.

## One correction carried from your last message

You referred to the rule-menu consequence corrections as "L4 corrections" and acted "per the L4 mandate." That mislabels the level. L4 is reserved for what a VALUE means for Regime-II-as-structural, and is Mike / Layer 1 only. The mapping from a transition rule to its expected per-observable consequence is L1 / L2 design reasoning — your domain, with Layer 1 on intent — that FEEDS the eventual L4 ontology question without being L4 itself. Engage rule-consequence reasoning as your own design work; do not defer it as off-limits. Only the question of which observable, if either, IS Regime-II coherence is L4.

## What is settled (the target — do not redesign these)

Topology is locked: 50 x 50, Moore radius 1 (8-neighbor), toroidal. Because this matches the Cycle 2 observable encoding, the observable computation (Psi_meanI_state, Psi_persistence_I) carries over — it is already 8-neighbor toroidal and parametric in grid size, so no observable rebuild is needed for this topology. Your task is the control battery that validates that observable at this scale.

The acceptance criteria (full detail pre-registered in the C3-CTL-001 test record):
- Five cases: A stable cluster (positive), B random at the same rho as A (negative), C random high-rho (negative), D transient wave (the divergence case), E uniform high persistence (degeneracy).
- L1: runs at 50 x 50, output finite and well-formed.
- L2: A both observables high; B and C both near zero; D produces the divergence — Psi_meanI_state high while Psi_persistence_I near zero; E near zero with the permutation-null z separating the uniformity degeneracy (low P_std flagging it).
- All "high / near-zero / significant" thresholds come from THIS grid's own null distribution. No comparison to 20 x 20 raw or z magnitudes.
- Case definitions must be scale-parametric — proportions and fractional widths, not fixed cell counts carried from 20 x 20.

## The co-equal-pair guard (the one place to be most careful)

Case D is where the two candidate observables diverge by design, and it is the case a careless scale-parametric rewrite can quietly weaken. The divergence — per-tick organization present (Psi_meanI_state high), no persistent clustering (Psi_persistence_I near zero) — must be preserved at 50 x 50. The wave must genuinely MOVE such that no cell is persistently active across the window; if the fractional-width rewrite makes the band wide or slow enough that cells stay active too long, Psi_persistence_I will rise and the divergence will be lost. Build Case D so the divergence is produced, and report it as data — not as evidence for either observable being Psi.

## What is yours (the open parametric choices)

- The exact proportion for Case A's contiguous cluster at 50 x 50 (Cycle 2 used ~0.1225 as a fraction; confirm or revise).
- The fractional width of Case D's moving band and how it advances per tick, sized so the divergence above is preserved.
- The high-rho value for Case C (Cycle 2 used ~0.80) and the persistence fraction for Case E (Cycle 2 used ~0.70).
- Window length and permutation count (Cycle 2 used 100 ticks, 199 permutations) — confirm or revise with justification.

Use the Cycle 2 values as orientation, not as cross-scale-portable numbers; the magnitudes do not transfer, only the case logic does.

## Deliverable shape

A DRAFT of the five scale-parametric cases plus the controls summary at 50 x 50 toroidal Moore-1, for Layer 1 / Layer 2 review against the criteria above — not an executed final. Execution is Mike's channel; review precedes any run. State your parametric choices explicitly with their rationale so Layer 2 can check validity against the stated criteria rather than reconstruct it after.

This is C3-CTL-001 (test record pre-registered, registry row moving planned -> ready). It clears L1 / L2 only by construction.

Execution channel remains Mike only.

Vocabulary holds: rho = activation density; Psi = coherence; Lambda = structural conduciveness (never "terrain favorability"); agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce (never "confirm" / "demonstrate").
