# Layer 2 substantive review request - wave-one design menu (A + B)

From: Layer 1, 2026-05-28.
To: Layer 2.
Purpose: substantive analytical review of Layer 3's revised wave-one design menu, per contract Section 7 step 2. Layer 1 has completed implementation review of v1 and v2; the v2 menu is clean on Layer 1's review criteria. Two items are surfaced for your substantive attention rather than as Layer 1 corrections. Your verdict is the gate before any code-production contract.

This package is self-contained. Section 2 carries the Layer 3 contract verbatim; Section 3 carries the v2 design menu verbatim; Section 4 summarizes what Layer 3 corrected v1->v2; Section 5 names the two items for your attention; Section 6 names what is and is not being asked; Section 7 routes after your verdict.

---

## Section 1 - Routing history

All events 2026-05-28, this session.

1. Pre-drafting consultation on scope fork (A+B vs B alone vs all three) routed to you; your recommendation A+B with grounds returned and was ratified by Mike.
2. Layer 1 drafted design-menu contract for Layer 3, scoped to A+B, carrying the corrected menu and both Layer-1 corrections from 2026-05-25 forward (Rule A pre-loads neither; Rule C - deferred to wave two - does not import mu(rho)).
3. Layer 3 returned v1 design menu.
4. Layer 1 implementation review of v1 found six items requiring correction.
5. Layer 3 returned v2 design menu addressing all six items.
6. Layer 1 second implementation review found v2 clean on contract criteria. Two items surfaced for Layer 2's substantive attention rather than for Layer 3 correction.
7. **This step - Layer 2 substantive review.**

---

## Section 2 - The Layer 3 design-menu contract (Layer 1 -> Layer 3, what Layer 3 was asked to fulfill)

### Frame

The contract asked Layer 3 for a design menu, not code. Eight deliverables (5.1-5.8). The contract anticipated the last-session Layer 3 framing-slip (declaring L2 clearance in its own voice) and required framing as "what the design specifies" or "what the rule is expected to produce." Candidates produce or fail to produce; never confirm or demonstrate.

### State at contract-open (carried forward into the package as context)

Three Cycle 3 precondition gates cleared: C3-ENV-001 (passed-L1), C3-CTL-001 (valid-L2), C3-SS-001 (valid-L2). Topology locked: 50x50, Moore radius 1 (8-neighbor), toroidal. The two-dimensional coherence signature (Psi_meanI_state, Psi_persistence_I) is a co-equal pair; neither is named theoretical Psi; regime assignment is L4. The two SS-001 flags (Steady_State_Candidate, Lifted_Activation_Candidate) remain independent at every stage.

### Scope (the A+B ratified by Mike on your recommendation)

- Rule A - both-agree baseline; pre-loads neither; relaxes to fixed points / uniform states; no sustained motion.
- Rule B - pre-loads Psi_meanI_state; range-bound / Life-like; shifting structures.
- Rule C - micro contagion with tunable divergence. Deferred to wave two.

### Two Layer-1 corrections carried forward (from 2026-05-25)

**Correction 1 (Rule A).** A strict lower-threshold activation rule with no upper / overcrowding bound moves the two observables together, not apart: at low threshold it fills toward uniform (both low or degenerate); at high threshold it freezes into locked clusters (both high). Across Lambda it produces no divergence. A is the least-discriminating rule, the both-agree sanity baseline. (Note: this primary-source endpoint pairing is amended by Layer 3's substrate-grounded resolution in v2; see Section 5 Item 1.)

**Correction 2 (Rule C, deferred).** mu(rho) is a mean-field coefficient; a micro contagion rule does not contain it. The micro-rule-to-mu(rho) relationship is derived by your mean-field analysis, not asserted by a rule sketch. This applies forward whenever C is described.

### The eight design deliverables Layer 3 was asked to provide

5.1 Local-rule specification - per-cell, per-tick definition of A and B in comparable notation; A has no upper bound; B is range-bound (band specified).
5.2 Lambda-like parameter for each rule - named, with range and rule-level interpretation.
5.3 Telemetry schema - per-tick and per-window quantities, including both observables with grid-local-permutation-null z-scores, all four SS-001 diagnostics, the two independent SS-001 flags, and rule-specific pathology diagnostics.
5.4 Minimal Lambda sweep - short feedback loop, with meaningful-failure criterion for each rule.
5.5 Expected joint-signature outcomes - per Lambda value, framed as expected and falsifiable.
5.6 Gate attachment - what ENV/CTL/SS licenses and does not license.
5.7 Four-level distinction per run-class - L1 implementation, L2 measurement validity, L3 steady-state-window eligibility (per SS-001), L4 manuscript interpretation (empty by design; held for Mike / Layer 1).
5.8 Co-equal-pair guard - neither observable named theoretical Psi; two flags independent; Case D divergence is data, not tiebreaker.

### Framing discipline (contract Section 6)

Forbidden in deliverables: "the run demonstrates," "Rule A confirms," "L2 sufficiency check passed," "the design clears L2." L2 clearance is a Layer 1 judgment. If a deliverable seems to require a stronger claim than the framing allows, weaken the claim, not the framing.

### Routing after design returns (contract Section 7)

1. Layer 1 implementation review.
2. Layer 2 substantive review.
3. Only after Layer 2 clearance - a separate code-production contract.

---

## Section 3 - Layer 3's revised (v2) design menu

The v2 deliverable verbatim follows. Layer 3 opened by re-acknowledging that no execution has occurred and that L2 clearance remains a Layer 1 judgment.

### 5.1 Local-rule specification

Both rules operate on the locked 50x50 toroidal grid, evaluating Moore radius 1 (8-neighbor) active-neighbor count for each cell at tick t to determine how the agent acts at tick t+1.

- **Initial condition (both rules).** Grid seeded at t=0 by per-cell active-state values (1 active, 0 inactive) assigned uniformly at random to achieve a target starting rho (e.g., 0.10).
- **Rule A (strict lower threshold).** An agent acts at t+1 if the count of active neighbors at t is >= tau_A. If the count is < tau_A, the agent deactivates. No upper/overcrowding bound.
- **Rule B (range-bound / Life-like).** An agent acts at t+1 if the count of active neighbors at t falls within a closed interval [tau_B,min, tau_B,max]. If below or above, the agent deactivates.

### 5.2 Lambda-like parameter for each rule

- **Rule A (Lambda_A).** Maps inversely to the strict lower threshold tau_A. To resolve the seam between primary source and substrate physics, the design adopts the fully pessimistic-on-passing path: sweeping the full integer range tau_A in {1, 2, 3, 4, 5, 6, 7, 8}. This allows the substrate to adjudicate where the uniform-fill, locked-cluster, and extinction regimes live without prematurely asserting their boundaries.
- **Rule B (Lambda_B).** Maps to the position and width of the activation band. The design specifies shifting the band: [tau_B,min, tau_B,max] in {[1,2], [2,3], [3,4], [2,4]}.

### 5.3 Telemetry schema

- **Per-tick records.** rho(t) (scalar mean of per-cell active-state values); the complete 50x50 matrix of per-cell active-state values.
- **Per-window records (100-tick windows, 25-tick sliding step).** Psi_meanI_state and its grid-local permutation null z-score; Psi_persistence_I and its grid-local permutation null z-score; the four SS-001 diagnostics (relative_drift, rho_cv, rho_range_over_mean, mean_rho); the two independent SS-001 flags (Steady_State_Candidate against 0.10/0.10/0.25; Lifted_Activation_Candidate against 0.05).
- **Rule-specific diagnostics (per run).** Tick_to_Freeze (tick index at which delta-states = 0 for 10 consecutive ticks); Tick_to_Zero (tick index at which rho(t) precisely equals 0.0).
- **Storage.** Per-tick active-state matrices in Parquet or compressed NPZ; windowed telemetry and diagnostics in a flat CSV.

### 5.4 Minimal Lambda sweep

- Sweep A: tau_A in {1, 2, 3, 4, 5, 6, 7, 8} (8 values).
- Sweep B: Band in {[1,2], [2,3], [3,4], [2,4]} (4 values).
- 5 random seeds per parameter value; 200 ticks per run (5 candidate steady-state windows per run).
- Total: 60 runs (12 parameter sets x 5 seeds).
- **Meaningful failure (Rule A).** If any Lambda value in Sweep A produces a divergent joint signature (high meanI / low persistence, or low meanI / high persistence) on 5/5 seeds in earned steady-state windows, the design fails at the micro-rule level - Rule A is intended to be non-discriminating.
- **Meaningful failure (Rule B).** If a parameter value designed to produce shifting structures produces Tick_to_Freeze < 200 on 5/5 seeds, the rule has structurally failed to force sustained motion.

### 5.5 Expected joint-signature outcomes

**Sweep A expectations (non-discriminating baseline).** No Lambda value in Sweep A is expected to produce the Regime-II-candidate signature (lifted rho with low/low non-degenerate coherence) or the divergent signature. Rule A is expected to move the observables together.

- tau_A in {1, 2}: expected to run away to uniform saturation (rho -> 1.0). Expected outcome: low/low (degenerate) due to zero spatial variance.
- tau_A in {3, 4, 5}: expected to freeze into static structures. Expected outcome: high/high (high Psi_meanI_state / high Psi_persistence_I).
- tau_A in {6, 7, 8}: expected to extinguish (rho -> 0). Expected outcome: low/low (degenerate).

**Sweep B expectations (probe for Regime-II-candidate and divergence).**

- Band [2,4]: wide band expected to produce unstructured "boiling" dynamics. Expected outcome: lifted rho with low Psi_meanI_state / low Psi_persistence_I. *This is explicitly the Regime-II-candidate regime.*
- Band [2,3]: narrow classic Life-like band expected to produce sustained moving structures. Expected outcome: lifted rho with high Psi_meanI_state / low Psi_persistence_I. *This is the divergent signature.*
- Bands [1,2] and [3,4]: expected to serve as boundary cases, likely tending toward noisy saturation (low/low) or extinction (low/low), framing the structural behavior of the middle bands.

### 5.6 Gate attachment

- C3-ENV-001: locked Python/Mesa/NumPy execution boundary; licenses L1 implementation success.
- C3-CTL-001: validated observable math (8-neighbor toroidal Moran's I) and grid-local permutation null functions; licenses L2 measurement validity.
- C3-SS-001: windowing logic and exact thresholds for filter diagnostics; licenses classification of an "earned steady-state window" and a "lifted activation" window as independent apparatus-grounded facts.

### 5.7 Four-level distinction per run-class

- **L1 (implementation).** Script executes without error, updating per-cell active-state values according to the specified rule and topology, writing well-formed outputs.
- **L2 (measurement-validity).** Computed observables accurately represent the spatial structure of the grid for that specific run, with grid-local nulls separating spatial organization from density.
- **L3 (steady-state-eligibility).** The two SS-001 flags (Steady_State_Candidate and Lifted_Activation_Candidate) are computed and reported independently for a 100-tick window. The window earns its classification for each flag separately; they are not conjoined into a single passing grade at the L3 level.
- **L4 (interpretation).** Empty by design. What the returned values mean for Regime-II-as-structural is strictly held for Layer 1 / Mike.

### 5.8 Co-equal-pair guard

The design holds Psi_meanI_state and Psi_persistence_I as a co-equal pair. Neither observable is named or treated as theoretical Psi. The SS-001 flags remain independent. The CTL-001 Case D divergence is an empirical baseline for measurement validity, not an ontological tiebreaker.

---

## Section 4 - What Layer 3 corrected v1 -> v2

Six items found in v1 by Layer 1 review; all six resolved in v2.

1. **tau_A range internal inconsistency** (v1 Section 5.2 said {1,2,3,4}; v1 Section 5.4 said {1,2,3,4,8}). Resolved: v2 uses {1,...,8} throughout (also implements path-iii reconciliation for Issue 2 - see below).
2. **Rule A dynamics endpoint inversion vs primary source.** v1 paired low tau_A with locked clusters and high tau_A with extinction; primary source paired low tau_A with uniform fill and high tau_A with locked clusters. Three reconciliation paths were offered; Layer 3 adopted path (iii) - full integer sweep, let the substrate adjudicate. The substrate-grounded picture in v2 Section 5.5: low tau_A -> uniform saturation (low/low degenerate); intermediate tau_A -> locked clusters (high/high); high tau_A -> extinction (low/low degenerate). See Section 5 Item 1 below.
3. **Per-Lambda expected outcomes missing.** v1 stated rule-level outcomes; contract Section 5.5 required per-Lambda outcomes. Resolved: v2 gives per-value expectations for all 8 tau_A values and all 4 bands.
4. **Regime-II-candidate regime not identified.** v1 did not name which Lambda values were expected to produce lifted rho with low coherence. Resolved: v2 names Band [2,4] as the Regime-II-candidate regime explicitly; v2 also explicitly states that no Lambda value in Sweep A is expected to produce the Regime-II-candidate signature.
5. **Rule A failure criterion missing.** v1 had a criterion only for Rule B. Resolved: v2 adds a Rule A criterion (5/5 divergent-signature seeds = structural failure).
6. **Section 5.7 L3 wording ambiguous on flag independence.** v1's wording could be read as conjoining the two SS-001 flags. Resolved: v2 Section 5.7 reads unambiguously as "computed and reported independently...not conjoined into a single passing grade at the L3 level."

---

## Section 5 - Items surfaced for Layer 2's substantive attention

These are not Layer 1 corrections. Layer 1 considers v2 clean on the contract's review criteria. Both items are open for your substantive engagement on grounds Layer 2 holds better than Layer 1.

### Item 1 - primary source endpoint pairing has been substrate-amended

Path (iii) authorized the substrate to adjudicate the endpoint pairing for Rule A. Layer 3's substrate-grounded reasoning lands at:

- Low tau_A (high Lambda_A): uniform saturation (rho -> 1.0); low/low degenerate.
- Intermediate tau_A: locked clusters; high/high.
- High tau_A (low Lambda_A): extinction (rho -> 0); low/low degenerate.

Locked clusters live in the middle of the tau_A range. Primary source (carried in the contract Section 4.1 and quoted at Section 2 of this package) had: low tau_A -> uniform fill (correct on this side); high tau_A -> locked clusters (the substrate-grounded picture places this at intermediate tau_A, with extinction at the high end).

The main claim in primary source - Rule A is non-discriminating across Lambda - is preserved: every tau_A produces a non-divergent signature. But the endpoint description was imprecise on substrate-dynamics grounds.

For your engagement: does the substrate-grounded picture in v2 Section 5.5 hold up under analytical inspection? If so, primary source's high-tau_A endpoint description warrants a small amendment in the wave-one close-out cluster (a record-keeping matter; the main claim stands). If your analytical view differs from Layer 3's substrate-grounded picture, surface where.

### Item 2 - degeneracy diagnostic for low/low signatures not explicit

The design distinguishes three low/low states with very different theoretical content:

- **Saturation:** rho ~ 1.0, near-zero spatial variance, the observables computed but on near-uniform data. Marked as low/low (degenerate) in v2 Section 5.5 for tau_A in {1, 2}.
- **Extinction:** rho ~ 0, no active cells. Marked as low/low (degenerate) in v2 Section 5.5 for tau_A in {6, 7, 8}.
- **Regime-II-candidate:** rho lifted with spatial variance present but neither moving structures nor persistent clusters. Marked as low/low (non-degenerate) in v2 Section 5.5 for Band [2,4].

The design's telemetry implicitly distinguishes via rho(t) and the SS-001 lifted-activation flag, but no explicit degeneracy diagnostic is specified. Some adjacent observations the design implicitly relies on:

- The SS-001 Lifted_Activation_Candidate threshold is one-sided (mean_rho > 0.05). A saturated substrate (mean_rho ~ 1.0) would also pass this flag. Whether the flag's "lifted" semantics catches both lifted-not-saturated and saturated depends on what the design intends - apparatus-grounded, the flag means "rho above the floor" and the non-degeneracy distinction is downstream.
- Distinguishing Regime-II-candidate from saturation requires a non-degeneracy diagnostic - spatial variance in the per-cell active-state matrix, or a check that mean_rho is bounded away from 1.0 as well as 0.0.
- The CTL-001 observables compute the grid-local-permutation-null z-scores, which would themselves degenerate on a uniform field - possibly providing an implicit degeneracy detector, but worth making explicit.

For your engagement: is the implicit degeneracy distinction adequate for the wave-one design, or does it warrant an explicit diagnostic (e.g., a non-degeneracy upper bound on mean_rho, or a per-window spatial-variance threshold)? If explicit, propose its form so it can be added to the telemetry schema before code production.

---

## Section 6 - What you are asked to engage; what you are not

**Asked:**
- Substantive analytical review of the v2 design menu against the contract.
- Engagement on the two items in Section 5.
- Discrimination analysis - does the sweep, as proposed, discriminate the regimes the design names? Are 5 seeds per Lambda value sufficient for the meaningful-failure criteria? Is the run count (60) sized correctly for the feedback loop?
- Rule-level reasoning - do the per-Lambda expected outcomes follow from the local-rule specifications under the substrate dynamics? Are the band choices for Sweep B well-spaced for the discrimination they aim to produce?
- Expected-signature reasoning - is the Regime-II-candidate identification (Band [2,4]) substantively defensible? Is the divergent-signature identification (Band [2,3]) substantively defensible?
- Gate attachment - are ENV/CTL/SS gates properly leveraged at v2's Section 5.6?
- Framing discipline check, vocabulary check, co-equal-pair guard check.
- Verdict: accept | accept-with-edits | reject-with-feedback.

**Not asked:**
- Not asked to write or specify code; the runnable artifact is a separate code-production contract after your clearance.
- Not asked to commit which observable is theoretical Psi - the pair stays co-equal, regime assignment is L4.
- Not asked to arbitrate L4. Mike does that on coherence-as-relational-mutual-reinforcement grounds when the wave-one results return.
- Not asked to ratify the primary-source amendment indicated by Section 5 Item 1 - that is a Mike arbitration in the close-out cluster. Just flag if your analytical view differs from Layer 3's substrate-grounded picture.

---

## Section 7 - Routing after your verdict

- Verdict returns to Layer 1.
- Layer 1 synthesis to the canonical record.
- **Accept** -> separate code-production contract drafted by Layer 1 and routed to Layer 3.
- **Accept-with-edits** -> edits applied by Layer 1 (or routed back to Layer 3 if substantive), brief re-review for clean, then code-production contract.
- **Reject-with-feedback** -> revise and re-route, same shape as v1 -> v2.

No code production from this review pass. Frame remains: what the design specifies and what each rule is expected to produce under the proposed sweep. Candidates produce or fail to produce.

---

## Section 8 - Vocabulary (binding)

- rho = activation density
- Psi = coherence (neither observable in the pair named theoretical Psi)
- Lambda = structural conduciveness (never "terrain favorability")
- Agents act - no decision / optimization / utility / cognitive language
- "The point(s) at which mu(rho) = 0" - never rho_c
- "Per-cell active-state values" - never "field" as explanatory mechanism
- Candidates produce or fail to produce - never "confirm" or "demonstrate"
- "Earned steady-state window" - the SS-001-validated criterion, apparatus-grounded
- The two SS-001 flags Steady_State_Candidate and Lifted_Activation_Candidate remain independent at every stage

Vocabulary discipline holds throughout, including at any verdict-celebrating framing.
