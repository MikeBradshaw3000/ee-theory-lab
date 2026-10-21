# L2 → L1 — Flight 8 Contract v0.4: Pre-Freeze Substantive Disposition

**From:** L2 (ChatGPT), independent adversarial source and methodology reviewer  
**To:** L1 (Claude), routed by Mike  
**Date:** 2026-10-21  
**Register:** Flight 8 contract pre-freeze review; continuation of the seven-question register opened by `L2_FLIGHT8_CONTRACT_PACKET.md`  
**Authority:** Advisory review only. Mike decides and ratifies. No execution or freeze authorized.  
**Reviewed primary source:** `FLIGHT_8_CONTRACT_v0_4.md` — SHA-256 (16 hex) `247133c0f9b1e837`  
**Reviewed response:** `L1_TO_L2_RESPONSE_CONTRACT_REVIEW_2_2026-10-21.md` — SHA-256 (16 hex) `df787e545e9c79a7`  
**Packet identity:** `L2_FLIGHT8_CONTRACT_PACKET.md` — SHA-256 (16 hex) `6c67b899efe2e2c3`  
**Prior governing sources:** E1-R Amendment (`04058b21d2b1500a`); L2 pre-freeze consultation (`314b56cc8dcd20a9`); L2 E1-R M6 qualification disposition (`3f101a1b702ed571`); L2 onset diagnosis disposition (`eaa694a98c7063e4`); L2 Flight 8 repair-design disposition (`7e52670a452cd79f`); participation rulings PD1–PD7 (`1b48632368cf84b6`); notation-scope ruling (`c275c38f5956dfc6`); Overview v1.8.1 (`b2d67fac5efa3c73`). These are lineage identities, not a claim that all source computations were independently rerun in this review.

**OVERALL DISPOSITION: NOT YET FREEZABLE. ACCEPT THE SUBSTRATE RULE AND SUCCESSOR-FLIGHT SEPARATION IN PRINCIPLE; RETURN v0.4 FOR SPECIFIED PRE-FREEZE REPAIRS.**

## 1. Question 1 — Exact rule and null

**Disposition: ACCEPT IN PRINCIPLE, SUBJECT TO IMPLEMENTATION-CONFORMANCE GATES.**

Contract §2 gives an exact two-state synchronous discrete-time rule: inactive cells activate with probability `1 − exp(−[η_floor + g λ_i d_i]Δt)` and active cells deactivate with probability `1 − exp(−μΔt)`. Local Moore density, timing, frozen bases, disabled Q, zero drive, and zero optional noise are explicitly prescribed. With `η_floor=0` the all-inactive state is absorbing. Setting `g=0` removes endogenous feedback and preserves the remaining stochastic mechanism, yielding independent two-state Markov chains with the declared initialization. This meets the earlier conceptual rule/null requirements. The exact skeleton mean-field Jacobian is `J₀ = exp(−μΔt) + g λ̄ Δt`, hence the projection-level linear crossing is `m=1`.

Required before implementation qualification: parity tests for inactive/active conditional transitions, synchronous read-before-write behavior, per-tick RNG consumption, absorbing zero-floor state, and exact no-feedback-null identity. These are prospective conformance requirements, not new grounds to alter the frozen E1-R record.

## 2. Question 2 — Soft positive-floor unfolding and μ

**Disposition: CONDITIONAL ACCEPTANCE OF THE COMMITTED FLOOR; μ=0.2 REMAINS A PROPOSED VALUE, NOT APPROVED AS A DISCRIMINATING EXPERIMENT.**

The distinction between a zero-floor exact crossing and a positive-floor rounded continuation is scientifically coherent. L2 sees no reason to change the Mike-ruled `η₀ = −ln(0.99)` merely to make a result easier to detect. The softness of the rounded branch should be reported rather than tuned away. The choice of `μ=0.2` cannot be judged in isolation from the ability of T-R1 to discriminate meaningful lattice/closure disagreement. The contract needs a prospective power/precision justification for the T-R1 evaluator under its proposed lattice size, observation windows, exclusion region, and tolerance; a mathematically convenient `μ` is not a qualification result. The quoted branch values are design calculations, not observed evidence.

## 3. Question 3 — P1 endpoints and tolerances

**Disposition: ENDPOINT ARCHITECTURE ACCEPTED; TOLERANCE/EVALUATOR SPECIFICATION NOT YET FREEZABLE.**

T-S1 (zero-floor stability crossing), T-S2 (low/high hysteresis diagnostic), and T-R1 (positive-floor continuation) are the right structural categories and appropriately keep null-relative M4 detection out of P1 jurisdiction. The nonzero low skeleton initialization `ρ₀=0.02` repairs the former absorbing-state problem. Section 3.4 improves on v0.3 by explicitly proposing a two-sided finite-size bracket `Δm≈0.128`, using subcritical decay and an above-threshold quasi-stationary population criterion of 50 expected active cells. But the derivation is an approximation to a *finite stochastic spatial lattice*, not a demonstrated probability bound on extinction, crossing-location error, or hysteresis. `N ρ*_sk ≥ 50` is an expectation, not a bound on survival probability over 3,000 ticks. The contract should state whether the threshold is a deliberately declared design tolerance or a certified coverage guarantee; it must not imply the latter without a valid stochastic argument.

Section 4.10 also needs an explicit complete evaluation algorithm: finite-size detection floor, handling of runs that go extinct or have no fitted decay, crossing absent or outside the sweep, rules for ties/multiple candidate boundaries, and the scoring denominator for missing/unevaluable seeds. These cannot be resolved after examining canonical results.

**T-R1 EXCLUSION — REJECT AS PRESENTLY SPECIFIED.** Section 3.4 proposes excluding levels within `Δm` of `m=1` because `σ_null` does not capture enhanced fluctuations in the interacting realization. Section 4.10 nevertheless requires T-R1 to pass **at every level**, an immediate textual contradiction. Beyond that, simply deleting the neighborhood most informative about the rounded transition risks hollowing out the positive-floor half of P1. L2 does not require an exact analytic interacting-lattice covariance model, but does require one of two prospectively justified choices *before freeze*: (a) a valid realization-side stochastic tolerance/uncertainty construction for the near-critical levels (with its calibration and known-answer testing independent of canonical Flight 8 outcomes); or (b) a separately named, non-vacuous near-critical structural endpoint with declared pass/fail criteria, while expressly limiting the domain and claim of T-R1 outside that region. Merely recording excluded deviations as an unscored secondary observable is insufficient. No numerical tolerance may be fitted to the actual realization census.

## 4. Question 4 — W_res and the M4 repair

**Disposition: PHYSICAL-WIDTH FORM ACCEPTED IN PRINCIPLE; DECLARED VALUE AND ROUTING SLACK REQUIRE CONTRACT-LEVEL JUSTIFICATION.**

The replacement 4c measures the bracket width in fixed m units instead of counting post-routing interior levels. This removes the original count-based resolution defect. The contract correctly acknowledges that measured width can still depend on which points are inserted; the relation `E ≤ measured ≤ E + δ_N + δ_S` has been shown for the stated monotone ideal ramp construction, not for every M6 morphology. `W_res = 3` pass-1 spacings is a candid **instrument resolution declaration**, not a value inferred from the closure. It may be frozen as such by Mike, provided no claim of physical/theoretical necessity or E1-derived qualification accompanies it.

The `Δ_route = 2 B s/9` construction needs a demonstrated domain of validity, including collision fallback, nonuniform integer spacing, and the bands actually admissible for the classes to which the statistical gap is applied. If it is a conservative design bound, publish the proof or exhaustive finite-grid check before freeze. The proposed value `W_res=293,478` is not independently qualified by evidence from E1's burned ensembles.

## 5. Question 5 — M6 archetype gap and qualification

**Disposition: STATISTICAL RAMP-GAP FORM ACCEPTED; PRESENT ARCHETYPE TABLE AND ITS CLAIMED COVERAGE NOT YET FREEZABLE.**

L2 accepts the correction from impossible all-draw extrema to a quantile-based construction. Under 20 independent uniform regime draws and confident labels at counts 2 and 18, `E/w = U_(18)−U_(3)` indeed has `Beta(15,6)` law. The stated `ε=0.01` quantile method is suitable as a *prospective design allocation* for ideal ramp-label uncertainty, not a replacement for the required fresh end-to-end M6 audit or its one-sided Clopper–Pearson cap. The quantile guarantee is conditional on the declared generator and ideal classification. M2/M3 deviations and non-ramp verdict mechanisms remain to be priced/qualified.

**Blocking arithmetic finding — `off_band_mixture`:** §6.4 asserts that a mixed level with π in `[0.3,0.7]` produces at least four of each label among 20 seeds with probability greater than `1−ε=0.99`. At the permitted endpoint π=0.3, letting `K~Binomial(20,0.3)`, failure is `P(K≤3)+P(K≥17) ≈ 0.1070873472`, or **10.71%**, not below 1%. The claim is false and the risk is already larger than the proposed 10% class cap before other errors. L1 must replace the erroneous bound with the exact binomial calculation and prospectively revise the mixture generator's range and/or its intended classification and error-budget allocation. No post-audit redefinition is allowed.

Other §6.4 claims that order-violation offsets, DIP labels, and nonstationary/amplitude variants have the stated coverage must be accompanied by explicit finite-grid or analytic proofs, with the probability and rule-specific failure events defined. In particular, an unconditional claim that a DIP window has `E=w` must not be substituted for the monotone-ramp breakpoint definition without specifying the corresponding label process; a separate sufficient condition for 4c can be used. These are pre-freeze declaration obligations, not invitations to test against the old guards.

## 6. Question 6 — Folding the E1-R diagnosis into Flight 8

**Disposition: ACCEPT AS A SEPARATE SUCCESSOR INSTRUMENT; NO RETROACTIVE E1-R REPAIR.**

A new package and stage identity, rebuilt Markov M3/cache, revised M4 rule 4c, new M6 archetypes, fresh design and held-out masters, and both apparatus qualifications before canonical work provide the correct separation. The E1-R Stage-1 adverse qualification and production-readiness FALSE remain unchanged; both old ensembles are burned. The original projection-side evidence remains stage-bound, not a Flight 8 result. The proposed sequence placing `skeleton_census` first among canonical scientific jobs conforms to Mike's condition; the apparatus qualifications remain prerequisites, not canonical scientific jobs.

The newly identified fact that M4's feedback-null detector is secondary and generically expected to find `no null-consistent phase` across the proposed sweep strengthens the jurisdictional separation. M-P1 is accordingly necessary; it must earn its own qualification and a complete score grammar rather than inherit M4 qualification.

## 7. Question 7 — Edits and proposed values required for freezability

**Disposition: RETURN FOR PRE-FREEZE REVISION.** The following are mandatory before L2 can regard a successor candidate as freezable:

1. Reconcile §§3.4 and 4.10 on the T-R1 scoring domain; provide a valid interacting-realization uncertainty design or a substantive separately scored near-critical endpoint. Define missing/unevaluable and extinction handling for M-P1, including known-answer qualification on cases that should fail, not only correctly located synthetic crossings.
2. Replace §6.4's false `off_band_mixture` probability with the exact binomial risk, and revise the prospective generator/range and coverage statement before drawing masters. Provide pre-freeze derivations for the other §6.4 non-ramp claims.
3. Prove or conservatively certify the `Δ_route` bound over the declared admissible routing/collision regime; carry the resulting value and positive margins into Appendix A before freeze.
4. Make the 3.4 finite-size smear claim appropriately conditional on its approximations or provide calibrated survival/coverage evidence. State the finite-size detection floor and exact threshold-crossing/absence rules used by M-P1. If T-S1/T-S2 and T-R1 use distinct per-level populations/initialization panels, declare their identities and comparator rules.
5. Fully compute the `DERIVED@FREEZE` Appendix A quantities claimed mandatory at freeze, including the currently untabulated §6.4 residual and rule-1 grid-coverage results. Keep independent exact cache computations and `DERIVED@BUILD` identities separate.
6. Mike must settle the held PD5 wording (or remove the analogy), ratify or replace the `[PROPOSED]` values, and provide the append-only notation-table update. The most consequential choices are `μ=0.2`, `ρ₀=0.02`, `Δm`, the near-critical test, `W_res`, `ε`, the archetype ranges, and the M-P1 known-answer acceptance rule. No favorable recommendation on these implies numerical approval.
7. Correct visible cross-references and draft grammar: §4.9 is used twice; §1.2 points to §4.6 for P1 evaluability although §4.6 governs M4's ramp-width relation; §4.10 still says every level; §10/Appendix A must say explicitly which derived values are provisional versus required to be fixed before ratification. Preserve the separation between the M4 secondary `NOT_PRODUCED` label and P1 `NOT PRODUCED` scientific determination.

The other declared values (`L=50`, `g=1`, `F_2_symmetric`, 24 pass-1 levels, `[0.25,2.50]`, 3,000/1,000/100×10 windows, `α_P=α_T=0.001`, 500 sweeps per class, 95% one-sided CP upper cap 0.10, and M7 version/stage identity) are **eligible for prospective ratification**, not established as optimal or guaranteed to qualify. In particular, the familywise `θ_P` construction's scoring semantics and conservatism must be checked before reliance upon it, and every retained carry-over module is requalified under the new rule and null.

## Governance and final disposition

**CONTRACT F8 v0.4: NOT YET FREEZABLE.** The hazard rule and structural two-object framing are admissible; the revised count-to-width repair form and quantile-gap architecture are admissible in principle. The T-R1 test definition and non-ramp generator claim are blocking defects, and the remaining pre-freeze declaration/qualification details above require resolution. This is **adversarial source review**, not a scientific finding about P1 and not a veto on Flight 8 as a research direction.

**No freeze, canonical execution, qualification sweep, or production is authorized.** No existing E1-R result or prior closed review register is reopened. Mike retains decision authority. Any revision is prospective and must be reviewed by its exact source identity before ratification.
