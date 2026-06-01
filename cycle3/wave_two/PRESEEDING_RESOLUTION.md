# Wave-two pre-seeding resolution

**Status:** CANONICAL. Resolves the two pre-seeding opens named in `cycle3/wave_two/DESIGN_CONTRACT.md` (Section 10): Comparator 0 observation protocol, and kappa-grid density against the realized-contrast scale. The contract remains frozen as placed (commit a925475); this memo references it and governs only the resolution substep. NOT a seeding step â€” no wave-two probe is seeded from this memo. Seeding remains Mike's call to open.

**Phase:** Cycle 3 wave two, design phase, pre-seeding resolution substep. Opened by Mike under Layer 2 direction (2026-06-01); Comparator 0 first, then kappa-grid density in realized-contrast space, with probe seeding held closed.

**Inherited locks (unchanged):** topology 50x50 Moore radius 1 toroidal; SS-001 earned-window criterion; `LOW_Z_THRESH` = 2.0; the co-equal pair `Psi_meanI_state` / `Psi_persistence_I`, neither named theoretical Psi; the L4 ontological question rides forward unsettled and is NOT resolved by anything here.

---

## 0. Ordering (carried from contract Section 10)

1. Comparator 0 (Lambda-only) read first â€” Section A below.
2. kappa-grid density set from the realized-contrast scale induced by the accepted Comparator 0 Lambda baseline â€” Section B below.
3. Comparator epsilon specified and read as a weak-coupling audit around the floor â€” after A, not before.
4. Seeding is Mike's call to open.

Comparator epsilon is NOT used to define the floor and is NOT specified until Comparator 0 is read. Its weak-neighbor magnitude is bounded by the predeclared realized-contrast ceiling of contract Section 6.2, never against any observable z-score. This memo does not re-specify epsilon; it preserves the contract's epsilon definition and fixes only the ordering (epsilon after Comparator 0).

---

## A. Comparator 0 observation protocol

Comparator 0 is Lambda-only: no neighbor term, no weak coupling, no epsilon perturbation. Its purpose is not to produce a candidate. Its purpose is to answer the floor question:

> Under lifted, non-degenerate activation density, what do the two observables do when local coupling is absent?

**Calibration target: rho-lift and non-degeneracy ALONE.** `Psi_meanI_state_z` and `Psi_persistence_I_z` are recorded OUTPUTS, never tuning targets.

Protocol:

- Tune ONLY the Lambda baseline until the run produces lifted, non-degenerate rho under SS-001 eligibility.
- Then record `Psi_meanI_state_z` and `Psi_persistence_I_z` as observed.
- Do NOT adjust Lambda or introduce any neighbor coupling to force either observable into `[-2, 2]`. The earlier single-comparator wording that would "choose the magnitude so the comparator lifts rho while holding `Psi_meanI_state_z` inside +/-2.0" is rejected and stays rejected (contract Section 6.3). Near-null must be OBSERVED, not imposed.
- Whatever signed pattern Comparator 0 produces is a finding about the apparatus floor, not a tuning failure to be corrected by targeting the z-band.

This keeps the comparator from becoming self-licensing: the floor is read, not selected against the criterion it is later meant to floor.

### A.1 Comparator 0 outcome readings

The observable axes are read on the signed three-level framework (held-inputs Section 7; wave-one refinement 2): each axis is positive-structured / near-null / negative-anti-structured. The persistence axis is read symmetrically â€” positive persistence is not excluded a priori (wave one's [3,4] non-eligible contrast showed strongly positive persistence under instability), so the table below does not collapse to a negative-only persistence lean.

| Comparator 0 outcome (lifted, non-degenerate unless noted) | Reading |
| --- | --- |
| near-null `Psi_meanI_state` / near-null `Psi_persistence_I` | clean trivial-stochastic apparatus floor; supplies the Section 4 item-1 reference |
| positive `Psi_meanI_state` | lifted independent activation alone organizes meanI under this apparatus; near-null is NOT the apparatus's default floor on the meanI axis â€” a finding (consistent in shape with the wave-one meanI absence, contract Section 5.1), NOT a tuning failure |
| negative `Psi_persistence_I` | anti-clustered persistence can arise on the floor without any local coupling; the floor itself is signed on the persistence axis â€” a finding to carry into how Rule C persistence readings are situated |
| positive `Psi_persistence_I` | clustered persistence can arise on the floor without local coupling; the floor is signed positive on the persistence axis â€” a finding to carry into how Rule C persistence readings are situated |
| lifted but degenerate | not an eligible floor; revisit the Lambda baseline on rho / SS-001 grounds ONLY, never on observable z-scores |
| not lifted | Lambda baseline insufficient; adjust Lambda ONLY |

The two SS-001 flags `Steady_State_Candidate` and `Lifted_Activation_Candidate` remain independent at every stage of this read. Per-(parameter-setting, seed) boolean flag counts, not per-parameter means (contract Section 7).

The meanI half of the comparator near-null scale is therefore OBSERVED from Comparator 0, not set from wave one (wave one has no lifted-near-null meanI, contract Section 5.1). The persistence half has a wave-one primary-source cross-reference only: the 6 near-null persistence rows (z ~ -1.85 to -0.06, mean ~ -1.43).

---

## B. kappa-grid construction rule

The grid is set in realized-contrast space, not raw-kappa space, and only AFTER the Comparator 0 Lambda baseline scale is accepted.

For Rule C in the canonical form (contract Section 2.1)

    p_become,i = sigma( logit(p_Lambda,i) + kappa * (2 q_i - 1) )

the endpoint realized neighbor contrast at fixed p_Lambda is

    delta_p(kappa; p_Lambda) = sigma( logit(p_Lambda) + kappa ) - sigma( logit(p_Lambda) - kappa )

This is the scale for grid design. The same nominal kappa implies different realized probability contrast depending on the Lambda baseline, which is why the grid is set after the Comparator 0 baseline scale is known, not before.

Construction rule:

- Take p_Lambda from the accepted Comparator 0 Lambda baseline scale.
- Include kappa = 0 exactly (coefficient-null separability: the exact Lambda-only point, contract Section 2.1).
- Use symmetric positive and negative kappa values (positive contagion-dominant, negative divergence-dominant).
- Make the grid denser near zero.
- Extend far enough to reach realized-contrast saturation / the large-|kappa| degeneracy boundary (contract Section 5; large-|kappa| is a degeneracy probe, NOT the evidentiary center).
- Record realized contrast `delta_p` alongside kappa for EVERY setting (contract Section 7 realized-contrast tracking).
- Do NOT choose grid endpoints or spacing because they are expected to produce low/low, or against any observable z-score.

This preserves the contract's core protection (Section 4 item 2, Section 7): a low/low point cannot earn substantive-candidate status merely because nominal kappa is nonzero while the realized neighbor contrast it induces is negligible. Grid density is set by probability contrast, not by expected z-score behavior.

The realized-contrast quantity `delta_p` here is the same measure that defines Comparator epsilon's admissibility ceiling (contract Section 6.2): one consistent measure across instrument and comparator.

---

## C. What this memo does NOT do

- Does not seed any probe (seeding is Mike's call to open).
- Does not specify Comparator epsilon's magnitude or run it (epsilon is specified after Comparator 0 is read; its ceiling is the contract's predeclared realized-contrast ceiling, never an observable z-score).
- Does not set numeric grid endpoints or spacing (these follow from the accepted Comparator 0 baseline scale, Section B).
- Does not tune any comparator against `Psi_meanI_state_z` in `[-2, 2]`.
- Does not predict whether Rule C reaches lifted-near-null meanI (held open, contract Section 5.1).
- Does not reinterpret either observable as theoretical Psi, and does not resolve the L4 ontological question by statistical robustness or by which observable a script names.
- Does not harden the weak-form Rule B prior (contract Section 8).
- Does not promote the untracked `read_obs001_nearnull_scale.py` into the canonical record.

---

## D. Routing from here

1. Layer 3 (Gemini) implementation of Comparator 0 (Lambda-only) is the natural next routing once Mike opens it; framed as "what the run will produce," and Layer 3 never declares its own L2 clearance.
2. Read Comparator 0 against Section A.1.
3. Set the kappa grid against Section B from the accepted baseline scale.
4. Specify and run Comparator epsilon as the weak-coupling audit.
5. Seeding is Mike's call to open.
