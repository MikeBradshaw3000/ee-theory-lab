# Layer 1 implementation review of wave-one design menu - corrections required

From: Layer 1, 2026-05-28.
To: Layer 3.
Purpose: Layer 1 review of your wave-one design menu, per contract Section 7 step 1, before the menu routes to Layer 2 substantive review. Six items require correction or reconciliation. Per Section 7, the revised menu returns to Layer 1 for re-review before forward routing. No code production until Layer 2 has cleared the corrected menu.

---

## What works (preserved)

The framing discipline held throughout your first response - explicit acknowledgment that no execution has occurred, that L2 clearance is for Layer 1 review and not a Layer 3 declaration, and consistent "expected to produce" / "the design specifies" framing. The category-error failure mode the contract anticipated did not recur.

Vocabulary clean. Co-equal-pair guard explicit at Section 5.8. Telemetry schema (Section 5.3) comprehensive - both observables with grid-local-permutation-null z-scores, all four SS-001 diagnostics, two flags tracked independently, useful rule-specific Tick_to_Freeze and Tick_to_Zero diagnostics. Gate attachment (Section 5.6) and four-level distinction (Section 5.7) clean on structure with L4 correctly held empty.

These items do not require revision. The corrections below preserve them.

## Items requiring correction

### Issue 1 - internal inconsistency in tau_A range (Section 5.2 vs Section 5.4)

Section 5.2 specifies tau_A in {1, 2, 3, 4}. Section 5.4 Sweep A is tau_A in {1, 2, 3, 4, 8}.

Sampling tau_A = 8 (the all-eight-neighbors extreme) is defensible as an endpoint, but it is not declared in Section 5.2. Either Section 5.2 expands or Section 5.4 drops the 8. Expansion is likely the right move - extremes are useful - but the design must be internally consistent.

**Action:** reconcile Section 5.2 and Section 5.4 so the declared tau_A range matches the actual sweep.

### Issue 2 - primary source and Section 5.5 disagree on Rule A's dynamics endpoints

This is the consequential one. There is a seam between primary source and your Section 5.5 expected outcomes.

**Primary source** (contract Section 4.1, faithful to `cycle3/routing/2026-05-25_note_to_layer_3_topology_decision_and_rule_corrections.md`):

> A strict lower-threshold activation rule with no upper / overcrowding bound moves the two observables TOGETHER, not apart: at low threshold it fills toward uniform (both observables low or degenerate); at high threshold it freezes into locked clusters (both observables high).

**Your Section 5.5:**

> As structural conduciveness increases (threshold lowers), the system is expected to transition from inactive (low rho, low/low coherence) to frozen locked clusters.

Both versions agree that Rule A is non-divergent across Lambda. They disagree on the dynamics endpoints:

- Primary source: low tau_A -> uniform fill (low/low or degenerate); high tau_A -> locked clusters (high/high).
- Your version: low tau_A (high Lambda_A) -> frozen locked clusters; high tau_A (low Lambda_A) -> inactive (low/low).

The substrate-grounded picture, on first inspection: at tau_A = 1 with no upper bound, any cell with >= 1 active neighbor activates and persists; this drives rho monotonically toward saturation - uniform fill, not locked clusters. At tau_A = 8, only cells with all eight neighbors active can activate, and from a random initial condition the dynamics extinguish almost everywhere (only saturated regions survive, briefly). Locked clusters (sparse persistent groups meeting a high local-density requirement) plausibly live at intermediate tau_A.

It is possible primary source's endpoint description was itself imprecise - its main claim (Rule A is non-discriminating) does not depend on which end "locked clusters" sits at. But the contract carries Section 4.1 forward as binding on this design, so the seam must be reconciled rather than left silent.

**Action:** propose a substrate-grounded reconciliation. Three paths are open:

(i) Adopt primary source's pairing: tau_A small (high Lambda_A) -> uniform fill; tau_A large (low Lambda_A) -> locked clusters.

(ii) Adopt your pairing and document that primary source's endpoint description was imprecise on the substrate-dynamics side; the main claim (A is non-discriminating) stands, but the endpoint description is amended.

(iii) Sweep the full integer range tau_A in {1, 2, ..., 8} and let the substrate identify where each regime lives, framing expected outcomes as "low/low at one end, high/high at the other, locked clusters somewhere in between" without committing to which end is which. This is the most pessimistic-on-passing path: it does not assume either primary source or your re-derivation is correct; the substrate adjudicates.

Make the case for whichever path you choose, grounded in the substrate dynamics. Mike arbitrates the reconciliation when the revision returns. Whichever path is chosen, the design must be internally consistent on which tau_A produces which dynamics, and that consistency must hold between Section 5.2, Section 5.4, Section 5.5, and the meaningful-failure criterion you will add per Issue 5.

### Issue 3 - expected outcomes not stated per Lambda value (Section 5.5)

Contract Section 5.5 asked for the expected joint-signature outcome **at each Lambda value in each sweep**, not at the rule level. You provided one outcome description per rule, not a per-Lambda mapping.

For Sweep B specifically, the four bands {[1,2], [2,3], [3,4], [2,4]} are expected to produce different rho regimes and possibly different coherence signatures. Without per-band expectations, the falsification structure - the expected being what the run could falsify - does not bind tightly to specific runs.

**Action:** provide a per-Lambda-value expected joint signature for each parameter value in both sweeps. For Sweep A, after Issue 2 reconciles, give expected outcomes at each tau_A value. For Sweep B, give expected outcomes for each band.

### Issue 4 - Regime-II-candidate regime not identified

The contract names the load-bearing test as the Lambda-varying sequence: Lambda changes -> rho lifts -> coherence signatures stay low over an earned steady-state window -> only under other conditions do one or both coherence signatures lift. The middle state - rho lifted AND coherence low (the low/low signature at lifted rho) - is the Regime-II-candidate signature.

Your Section 5.5 does not identify which Lambda values in either sweep are expected to produce this middle state. Without this identification, the sweep may run and produce no parameter values that hit the diagnostic regime, in which case the load-bearing test cannot be read off the runs.

**Action:** for each sweep, identify which Lambda value(s) are expected to produce lifted rho with low coherence - the Regime-II-candidate regime. If the answer is "none expected" for either rule, that is itself a useful design statement and should be made explicitly with reasoning. (For Rule A specifically, the prior version's claim that A is non-discriminating means no Lambda value in Sweep A is expected to produce the Regime-II-candidate signature - Rule A is the substrate-side sanity baseline, not a Regime-II probe. State this explicitly.)

This issue is closely related to Issue 3 - per-Lambda expectations will surface the Regime-II-candidate values directly.

### Issue 5 - no Rule A failure criterion in Section 5.4

You defined a meaningful-failure criterion for Rule B: a parameter value designed to produce shifting structures producing Tick_to_Freeze < 200 on 5/5 seeds is a structural failure of the rule. There is no analogous criterion for Rule A.

**Action:** add a meaningful-failure criterion for Rule A. A candidate, for your consideration: if any Lambda value in Sweep A produces a divergent joint signature (high meanI / low persistence, or low meanI / high persistence) on 5/5 seeds in earned steady-state windows, the design has failed at the micro-rule level - Rule A is meant to be non-discriminating, and a Rule A run producing divergent observables indicates either a rule-implementation error or a rule that does not in fact match the both-agree-baseline architecture. Refine or replace this criterion as your substrate-dynamics reasoning recommends.

### Issue 6 - Section 5.7 L3 wording potentially ambiguous on flag independence

Your Section 5.7 reads: "A 100-tick window within the run independently satisfies the SS-001 criteria for Steady_State_Candidate and Lifted_Activation_Candidate."

This can be read two ways:

(a) Both flags must be satisfied for L3 clearance - i.e., the flags are conjoined into a Regime-II-ready test.
(b) The two flags are computed independently and reported separately; L3 reads them as a pair without conjoining them.

The contract is explicit that the two flags remain independent at every stage and are not collapsed into a single "Regime-II-ready" flag.

**Action:** clarify Section 5.7 so the L3 wording reads unambiguously as (b). The two flags are independent SS-001 outputs at the L3 level; downstream interpretation reads them jointly without combining them.

## Routing after revision

Per contract Section 7:

1. Revised design menu returns to Layer 1 for re-review.
2. If Layer 1 finds the revision clean, the menu then routes to Layer 2 for substantive analytical review.
3. Only after Layer 2 clears the corrected menu: a separate code-production contract.

No code production from this revision. Frame remains: what the design specifies and what each rule is expected to produce under the proposed sweep. Candidates **produce or fail to produce**.

## Framing discipline

The framing discipline that held in your first response continues to apply. No past-tense execution language. L2 clearance is a Layer 1 judgment, never a Layer 3 declaration. If a deliverable seems to require a stronger claim than the framing allows, the right response is to weaken the claim, not the framing.
