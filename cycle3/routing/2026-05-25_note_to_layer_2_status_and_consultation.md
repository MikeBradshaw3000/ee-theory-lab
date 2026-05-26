# To Layer 2 — Cycle 3 status and an open consultation

Routing note, drafted by Layer 1 for Mike's routing. Bringing you current, with genuine questions below and the floor open for any comment you think would help.

## Where Cycle 3 stands

- **Environment (C3-ENV-001):** closed at L1. Captured: Python 3.14.4, Mesa 3.5.1, top-level venv. The floor everything runs on.
- **Substrate topology:** locked to Candidate 1 - 50 x 50, Moore radius 1 (8-neighbor), toroidal - chosen as a deliberate canonical baseline. The theory basis: Cycle 3 first needs a no-special-location substrate to validate the measurement apparatus without boundary artifacts; edges (non-toroidal) and extended-reach coupling (larger radius) are later topology variants, not the first baseline.
- **The grid-scale / boundary question you worked: converged.** The settled finding: topology and the controls / observable are paired on grid size, adjacency, and boundary condition; the observable conforms to the substrate; controls are regenerated per topology and interpreted within-topology, with no cross-topology raw or z magnitude comparison; scale-parametric case definitions are necessary but not sufficient; boundary conditions are baked into the observable. Your active-fraction catch and the fixed-neighborhood length-scale point both hold in that finding.
- **C3-CTL-001 design phase:** your validity pass landed in full. Both your catches were adopted - Case E rewritten to the uniform-persistence degeneracy control (it had become a 35-column moving band reading high per-tick), and B and C tightened to exact-count random (250 and 2000 active cells per tick) rather than Bernoulli draws. Layer 3 implemented the revised battery; Layer 1 review confirmed the accepted set produces the full designed discrimination (A high on both; B and C near zero; D the divergence; E near zero with the uniformity degeneracy flagged).
- **One addition now in flight to Layer 3:** the battery computed a permutation-null z only for the persistence observable, not for the per-tick Psi_meanI_state. The converged finding requires grid-local nulls for thresholds on both observables, so a per-tick null for Psi_meanI_state is being added. Question 1 below is about its construction.
- **Transition rules:** held, uncommitted. The menu is sketched with per-observable consequences - A the both-agree baseline (pre-loads neither), B pre-loading Psi_meanI_state, C a micro contagion rule with tunable divergence. Rules commit only in the design phase, reconciled with your discrimination analysis and the substrate together.

## Genuine questions

**1. The per-tick null construction.** As routed to Layer 3: for each permutation, shuffle every tick independently (preserving that tick's exact active count, so the null isolates spatial arrangement from density), recompute the windowed mean of per-tick Moran's I to get one null sample; repeat across permutations to build the null for the aggregate statistic; z-score Psi_meanI_state against it. Is that the correct null for the aggregate windowed-mean statistic, or is there a subtlety that would change it - for instance, building the null for the aggregate mean versus z-scoring per tick and then averaging, or a variance issue in the windowed mean that the per-tick shuffle does not capture? Any refinement you flag reaches Layer 3 before Mike's canonical run.

**2. Reading the pair under grid-local nulls.** Once both observables carry a grid-local z, applying the apparatus to real substrate yields a pair: (Psi_meanI_state value + z, Psi_persistence_I value + z). The co-equal-pair guard holds that neither z settles which observable IS Regime-II coherence - that stays an L4 question for Mike / Layer 1. Is there an analytical framing for reading the pair jointly on real substrate that preserves the held-open ontology - what a (high per-tick z, low persistence z) reading licenses versus (high, high) versus (low, low) - without collapsing to "X is Psi"? This is your standing discrimination question made concrete at the apparatus-output level.

## Open floor

The standing discrimination question - what structure on the Lambda -> rho -> Psi cascade would let a probe discriminate the co-equal pair rather than be merely consistent with one - remains open, and is what the substantive probes (after the CTL and SS gates) will need. Developing thoughts are welcome; not asking for a full answer here. And any comment on the topology choice, the converged finding, the rule menu, or anything you see that would help - the floor is yours.

Execution channel remains Mike only.

Vocabulary holds: rho = activation density; Psi = coherence; Lambda = structural conduciveness (never "terrain favorability"); agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce (never "confirm" / "demonstrate").
