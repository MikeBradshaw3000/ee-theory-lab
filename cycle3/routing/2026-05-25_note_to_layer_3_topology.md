# To Layer 3 — Fork 2: substrate topology authorized; what to draft, what is held

Routing note, drafted by Layer 1 for Mike's routing. This is the substrate-topology authorization, now carrying a settled measurement-validity constraint.

## Status

C3-ENV-001 is closed (acknowledged on your side). The grid-scale / boundary-condition measurement-validity question has been worked through Layer 2 and converged. This note authorizes topology drafting with the constraints that finding produced. Transition rules remain held — see the last section.

## Authorized now — substrate topology

Draft the substrate's structural layer. For each candidate, specify all three of:

1. **Grid size** (scale). The Cycle 2 proof-of-concept ran at 20 x 20; the measurement-validity analysis considered roughly the 20-to-60 range. Propose and justify your scale; this is a design choice, not a fixed inheritance.
2. **Neighborhood / adjacency** — the relation by which an agent's neighbors are defined (e.g. Moore radius 1).
3. **Boundary condition** — toroidal (wrapping) or non-toroidal (edges).

These three are not incidental detail. They are load-bearing for measurement validity, for the reason in the next section.

## The measurement-validity constraint (settled — Layer 1 / Layer 2 converged)

Topology and the observable / control apparatus must be paired on the same three dimensions: grid size, adjacency, boundary condition.

- **The observable conforms to the substrate, not the reverse.** The co-equal observables (Psi_meanI_state and Psi_persistence_I) are both Moran's-I-based. The Cycle 2 observable encodes a fixed Moore radius-1 neighborhood with toroidal wrap (np.roll). The substrate topology is the primary choice — agents act on it — and the observable's adjacency must be rebuilt to use EXACTLY the substrate's adjacency and boundary. If your substrate is not Moore-radius-1-toroidal, the observable computation must change to match it. A substrate and an observable that disagree on adjacency are measuring different topologies.

- **Controls are paired per topology.** Each candidate substrate topology carries a synthetic control battery regenerated at THAT topology — same size, same adjacency, same boundary. Control success is read qualitatively WITHIN a topology; raw or z magnitudes are NOT compared ACROSS topologies. The reason: with a fixed-cell-radius neighborhood, a fixed-proportion structure has falling boundary-to-interior ratio as the grid grows, so raw Moran's I rises and the permutation null tightens (~1/N) — the same positive control yields a larger z on a larger grid even at fixed proportion. Scale-parametric case definitions (proportions and fractional widths, not fixed cell counts) are therefore necessary but NOT sufficient for portability. Do not build the control battery now — that is the CTL design phase, after topology candidates are on the table. Just carry the paired requirement with each candidate.

- **Boundary-condition consequence to weigh now.** If you choose a non-toroidal substrate, the transient-wave control (which currently wraps) needs a non-wrapping moving-band rule with documented edge behavior (a band reaching an edge stops, reflects, disappears, resets, or re-enters by rule — each is a different control). The divergence that case is designed to produce — per-tick organization high, persistence-grid clustering near zero — must be preserved under whatever boundary you choose. So the boundary choice has a downstream cost in the control battery; factor that into the choice rather than discovering it later.

## The four-level discipline (it governs how you report)

- L1 implementation — does the topology code run, output well-formed? (your domain)
- L2 measurement validity — is the observable the intended quantity under this topology, with adjacency matched? (your domain, with Layer 1 on intent)
- L3 steady-state eligibility — earned by diagnostics.
- L4 — what any value means for Regime-II-as-structural (Mike / Layer 1 only).

Report topology and observable work at the level it reaches — L1/L2 — and leave L3/L4 alone.

## Held for the design phase — transition rules

Do NOT commit transition rules. The reasoning is load-bearing, not procedural caution:

The two candidate observables are a co-equal pair, and which one — if either — IS Regime-II coherence is the open ontological question, settled on relational-mutual-reinforcement grounds by Mike / Layer 1 (L4), not by substrate mechanics. Transition rules are exactly where a substrate can quietly pre-load one observable: rules that naturally produce persistent clustering pre-load Psi_persistence_I; rules that produce shifting per-tick organization pre-load Psi_meanI_state. Committing rules before the discrimination question is worked would let the substrate settle, by default, the ontology the guard exists to keep open.

You MAY sketch a transition-rule MENU: a set of candidate rules, each with its expected consequence for EACH observable made explicit. Keep the options genuinely distinct in their observable consequences — the divergence between what different rules would do to the two observables is the informative content, not noise to be smoothed toward one design. Do NOT commit to a rule set. Rules are committed in the design phase, reconciled with Layer 2's discrimination analysis and your topology together.

## Summary of the ask

Draft candidate substrate topologies, each fully specified on grid size, adjacency, and boundary condition, each carrying (i) the requirement that the observable's adjacency be rebuilt to match it and (ii) a paired control battery at that same topology (to be built in the CTL phase, not now). Optionally sketch a distinct-options transition-rule menu with per-observable consequences. Commit no transition rules.

Execution channel remains Mike only.

Vocabulary holds: rho = activation density; Psi = coherence; Lambda = structural conduciveness (never "terrain favorability"); agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce (never "confirm" / "demonstrate").
