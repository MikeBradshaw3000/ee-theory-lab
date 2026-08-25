# L2 Adversarial Review — Contract E1 Draft v0.1

> **Re-export status:** This review is preserved from the active L2 turn, with Markdown formatting normalized. The final correction carried with the review appears at the end.

## Overall verdict

**NOT READY TO FREEZE — REDRAFT REQUIRED.**

The contract has the right epistemic architecture: it places only the first transition under E1 jeopardy, keeps continuity and reversibility in E5, bars Ψ observables from E1 verdict-making, separates R1 recovery from the street-question verdict, and preserves never-relax and jurisdiction discipline.

The present operational machinery, however, does not yet test the question it names without contamination. The largest defects are:

1. Q is not actually frozen.
2. “Sustained” is made equivalent to “steady-state.”
3. nonstationary runs are converted into floor observations;
4. no seed-to-level classification rule exists;
5. the three verdicts overlap and leave important outcomes unmapped;
6. the monotonicity and confidence requirements import working-form assumptions into the core-rung test;
7. the proposed positive and negative controls can convert substantive theoretical failure into “apparatus failure”; and
8. R1 does not yet contain an executable, outcome-independent MFA projection map.

These are contract defects, not objections to the E1 rung itself.

## 1. E1 must freeze all of Q, not only its activation channel

**VERDICT: BLOCKER.**

The contract proposes `Gamma_rho = 0`, but says nothing about `Gamma_Psi`. Under the frozen instrument:

```text
Delta_b = Gamma_Psi * Psi_local + Gamma_rho * activation_input
```

Setting only `Gamma_rho = 0` leaves the ancestor Ψ-driven write channel active. Bases can change during the run, and those changes alter local Lambda at later ticks.

That defeats the clean E1 question in two ways. First, the sweep no longer holds structural conditions fixed. It sweeps initial conditions followed by endogenous terrain modification, not Lambda as a frozen control. Second, coherence-adjacent mechanism telemetry can causally alter the first-transition result even though Ψ is formally denied an E1 verdict role.

### Required amendment

For E1 production runs:

```text
Gamma_Psi = 0
Gamma_rho = 0
```

No base-update arithmetic executes. Bases remain fixed for the full run. Ψ-family telemetry may still be computed and emitted, but it may not write to `v`, `u_base`, or `r`.

**Ruling on the flagged `Gamma_rho = 0` item:** accepted only as part of a complete Q freeze.

## 2. “Sustained” cannot require steady-state behavior

**VERDICT: BLOCKER.**

The core claim is that an activated regime can be persistent. It does not require that persistent activation settle to a fixed or approximately stationary density. A bounded oscillatory regime, a slowly varying persistent regime, or another nonstationary-but-enduring pattern could satisfy the regime commitment while violating the preferred supercritical fixed-point picture.

The B-derived steady-state classifier may remain a secondary diagnostic or a condition for estimating equilibrium in R1. It cannot be a necessary condition for the scientific category “sustained.”

## 3. A failed steady-state gate cannot be imputed as the floor

**VERDICT: BLOCKER.**

A failed stationarity test can mean decay, slow growth, persistent oscillation, switching, critical slowing, or insufficient horizon. Those are not equivalent to inactivity.

At minimum, each run needs three mutually exclusive statuses:

- **SUSTAINED:** a frozen persistence criterion passes and activation is above the null/floor criterion;
- **NO SUSTAINED ACTIVATION:** a frozen extinction or terminal-floor criterion passes; and
- **UNRESOLVED:** neither conclusion is earned within the horizon.

An UNRESOLVED run remains unresolved. It may not enter the level aggregate as a floor observation. Stationarity travels separately.

## 4. The contract lacks a level-classification rule

**VERDICT: BLOCKER.**

The contract does not say how twenty heterogeneous run statuses become one level status. A median after replacing unresolved/nonstationary runs by the floor hides the composition.

Before freeze, specify:

1. whether the same seed panel is reused across levels;
2. whether comparisons are paired;
3. how sustained/no-sustained/unresolved counts produce a level classification;
4. the exact interval/resampling method and analysis RNG; and
5. how mixed-seed outcomes are reported rather than averaged away.

## 5. The verdict map is contradictory and not exhaustive

**VERDICT: BLOCKER.**

Direct conflicts include:

- lowest-level sustained is called both NO THRESHOLD and a NOT DISTINGUISHED range defect;
- failure of adjacent uncertainty separation appears in both NO THRESHOLD and NOT DISTINGUISHED; and
- nonstationarity is both converted to floor and treated as a no-verdict anomaly.

Unmapped outcomes include no sustained activation anywhere, multiple crossings, reentrant loss, multiple coarse brackets, broad mixed-seed regions, and unresolved top endpoints.

The contract should report a **threshold bracket**, not a falsely precise threshold level:

```text
[Lambda_minus, Lambda_plus]
```

A coherent exhaustive map is:

- **LOCATED THRESHOLD:** exactly one admissible inactive-to-sustained bracket, with no reversion in phase membership;
- **P1 FIRST TRANSITION NOT PRODUCED:** an adequate range is established and no single inactive-to-sustained boundary exists, including no inactive phase, no sustained phase, or multiple/reentrant phase boundaries;
- **NOT DISTINGUISHED:** uncertainty, horizon, seed precision, or inadequate range prevents separation.

Resolved multiple crossings are a substantive adverse result, not automatically an instrument limit.

## 6. Spearman and adjacent-CI conditions import form assumptions

**VERDICT: BOTH PROPOSED CONDITIONS REJECTED.**

A monotone activation amplitude above the boundary is not required to establish entry into a sustained phase. The proposed Spearman condition belongs to form/shape analysis, not the core E1 verdict.

Non-overlap of adjacent 95% bootstrap intervals imposes an implicit minimum detectable jump and conflicts with the line-not-drama rule. Classify each level relative to the independently frozen inactivity criterion and report a bracket. Do not require a jump, slope, monotone active-phase amplitude, or adjacent-CI non-overlap.

## 7. The sweep variable and “Lambda-star” need exact separation

**VERDICT: BLOCKER.**

The experiment sets the center of a base-distribution family, not one scalar Lambda. Freeze and name separately:

- control variable `m`;
- interval width and boundary handling;
- theoretical `E[F(v,u_base,r)]`;
- realized initial grid mean `Lambda_bar_0`; and
- the threshold bracket.

Preserve distribution width and form across levels; silent clipping changes both mean and heterogeneity.

Because activity begins from Bernoulli `p=0.5`, E1 locates a boundary for **sustaining activation after the frozen initial perturbation**. It does not by itself locate a nucleation threshold or prove instability from arbitrarily small rho.

The existing bottom-range sentence also compares quantities in different units. Endpoint adequacy must be expressed in activation/classification terms, and a top range guard is required.

## 8. The proposed floor is not mechanism-derived in the claimed sense

**VERDICT: NOT ACCEPTED AS WRITTEN.**

The single-cell expectation may be derived; the multiplier `2x` is an additional design choice unless independently justified. The null must state whether it includes the sigmoid baseline, `eta_floor`, local-density/overcrowding terms, persistence, and finite grid/window variation.

Freeze one exact null object and name it accurately. A predeclared upper quantile/bound of a constructed null at the production N and tail window is preferable to an unexplained multiplier. Audit the classifier on known-answer synthetic profiles.

## 9. The proposed controls can shield the theory

**VERDICT: BLOCKER.**

A high-conduciveness production configuration that “must” sustain and a low-conduciveness production configuration that “must” fail are not neutral apparatus controls; they are instances of P1. Contrary behavior could be the scientific result.

Use constructed known-answer controls for the classifier: stable-above-null, extinct/decayed, persistent-nonstationary, and unresolved. Any dynamics-level control must be algebraically forced, not a production setting whose expected behavior assumes P1.

## 10. Evaluability and execution sequencing are inconsistent

**VERDICT: BLOCKER.**

The draft proposes estimating false-block rates from controls and thinning gates “at freeze,” while also placing those runs after freeze. It calls tranche/control runs pre-seeding even though they seed E1 configurations. Wall-clock pricing also depends on a built path while the stated sequence freezes earlier.

Separate:

1. instrument build and non-scientific qualification;
2. contract freeze;
3. post-freeze quarantined calibration tranche, if retained; and
4. production authorization/sweep.

Use “before any E1 production run” where intended. Production patterns may never be used to recompute false-block probabilities or thin gates.

## 11. R1 is not executable

**VERDICT: BLOCKER.**

The supercritical MFA equation is a working hypothesis, not core. Call it the candidate MFA working-form dynamics.

Before data, define:

- discrete-tick to MFA-time map;
- microscopic-to-MFA coefficient map;
- which aggregate Lambda enters;
- MFA initial condition;
- independent determination of `Lambda_star_MFA`;
- numerical scheme; and
- finite-size/correlation-aware tolerance method.

A fitted E1 threshold cannot serve as its own independent R1 target. The near-threshold departure zone also cannot silently exempt T2, which is a threshold-location comparison.

With Q frozen, E1-R1 tests activation-level recovery only, not local-Q-to-aggregate-Q recovery.

## 12. Configuration and naming corrections

Replace “kappa-coupling at the committed symmetric-chain terms.” In `symmetric_chain`, the local contribution is A's density and quadratic-overcrowding construction; kappa names the `become_survive` linear coupling.

Use `u_base` wherever bare `u` could be confused with `u_t`.

## 13. Scale and the F2 secondary arm

At 24 first-pass levels, 8 refinement levels, and 20 seeds, the primary maximum is 640 production runs, or 4.8 billion cell-tick rows before controls/tranche/retries. A second arm doubles that to 9.6 billion rows.

Before freeze provide wall-clock, storage/I/O, parquet partition, hash/readback, restart-granularity, and capacity forecasts.

`F_canonical` as headline primary is accepted. `F_2_symmetric` must either be named-deferred or frozen as a separately reported robustness arm that cannot replace, rescue, or veto the canonical verdict.

## Proposed-value rulings

- `Gamma_rho=0`: accepted only with `Gamma_Psi=0` and total Q freeze.
- `F_canonical` primary: accepted.
- `F_2_symmetric`: defer unless resources and arm-specific claim grammar are frozen.
- 24/8 levels and 20 seeds: not rejected, but not ratifiable before evaluability/resource forecasts.
- Tail window `[2000,3000]`: may remain a candidate, but cannot define sustained through stationarity alone.
- B steady-state thresholds: secondary diagnostic only.
- `2x` analytic floor: rejected pending exact null/multiplier derivation.
- Spearman `>=0.8`: rejected from LOCATED.
- adjacent bootstrap-CI non-overlap: rejected from LOCATED.
- 10% false-block and 80% classifiability values: still Mike-level proposals, contingent on a valid synthetic morphology audit.
- calibration tranche: acceptable only under strict quarantine and no outcome-driven redesign.

The morphology audit must include gentle onset, abrupt onset, persistent nonstationary activation, nonmonotone active-phase amplitude, no sustained phase, no inactive phase, and multiple crossings.

## Correction carried with this review

The range rule controls whether an endpoint pattern is scientifically interpretable; it must not pre-label the answer. An all-sustained or all-no-sustained profile is **NOT DISTINGUISHED** when the frozen range has not independently established both endpoint jurisdictions. If endpoint adequacy is established by prospective rules, the same resolved profile may support **P1 FIRST TRANSITION NOT PRODUCED**. The contract must not route the same observed pattern to both categories.

## Freeze disposition

**FREEZE MAY NOT PROCEED.**

The E1 idea is sound. The current draft could both manufacture a line through a floor crossing and miss a real persistent activated phase by demanding steady-state behavior. A full v0.2 redraft is required.
