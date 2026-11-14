# Contract F9 — Flight 9: terrain and composition under the hazard rule (v0.5, DRAFT)

**v0.5, 2026-11-14 — supersedes v0.4 (`7a00117979ccad3e`, committed at `2781789`, retained).** Answers L2's round-3 review (`L2_F9_CONTRACT_V0_4_ROUND3_REVIEW_2026-11-14_RECEIVED.md`, `04934a2ec28d763a…`: **NOT YET FREEZABLE**, two repairs R3-1 and R3-2, and by L2's statement no third independent blocker; F1, F3, F5 and F6 closed; F2 and F7 closed with a note; the traced components, the pruning rule, the descriptive constancy report and the persistence table accepted). L1 ran L2's Appendix R program against the packet bytes; every figure reproduces. Mike ruled on 2026-11-14 on L1's recommendation (narrow the wording to the registered family; proceed directly to v0.5): "I accept your recommendation". Changes from v0.4:
- **(R3-1) B is scoped to the registered family `[RULED 2026-11-14]`.** v0.4 said a valid failure means "no level set of that index" represents the boundary, and that the family was "every level set the index has on this lattice". The family is the complete set of level sets of the comparison array, which is rounded to 12 places. Rounding removes level sets of the raw index and can change a decision: on TD-1-2, L2 built a boundary that is exactly a raw-H level set and lies 19.5 cells from every registered contour. The arrays and the rounding are kept. The claim is narrowed to what they support (§1.1, §1.2 B, §3.4 step 3, §5.5 steps 5, 7 and 8, §7 L7, §9), and L2's case becomes known-answer class 24.
- **(R3-2) The qualification declaration is completed (§6.2).** v0.4 declared component strata that no canonical terrain can carry (a 40-bond component under 5% of the perimeter needs a contour of more than 800 bonds; the longest canonical contour has 768), and named arm and flight truths without constructions for them. v0.5 declares: a synthetic **strip fixture** for the component strata; a construction for each special arm and flight row, with fixed slots, positions and draws; acceptance by certified truth for every row; separate capped strata for each component size and each noise level; the sensitivity error event (every output other than the certified decisive label); the exact lag-one estimator; and a bounded candidate budget with the typed failure `stratum not populated`. L1 checked at zero noise that every construction gives its named truth on all eight comparison arrays (`arith_v0_5/`; Appendix A.10).
- **Overview citation.** Mike registered Overview v1.8.2 (`9c77bcd47385714c`) as the statement of record at `47272f2` on 2026-11-14, while this version was being written. §10 now cites it and §13 no longer lists it as held. v1.8.2 is a wording conformance; the Overview's uses of β, μ(ρ) and Λ* that this contract's notation refers to are in sentences v1.8.2 leaves as they were, or changes only in prose about the bases and Q (L1's comparison of the two files).
- Nothing else is changed: no rule of the dynamics, no terrain, ε, m, θ, the arm and flight rules, the error caps and the job order are as in v0.4.

**v0.4, 2026-11-13 — superseded v0.3 (`949c5200eb6721e1`, committed at `dd17b53`, retained).** Answers L2's round-2 review (`L2_F9_CONTRACT_V0_3_ROUND2_REVIEW_2026-11-13_RECEIVED.md`, `f3c2b07d546869ff…`: **NOT YET FREEZABLE**, seven repairs F1–F7; the pruning argument and the three closure-informed design changes ACCEPTABLE; R4 and the unoriented-edges addition CLOSED). L1 ran L2's Appendix R program against the packet bytes; both counterexamples reproduce. Mike ruled on 2026-11-13: "f3 descriptive and proceed directly". Changes from v0.3:
- **(F1) Components are connected pieces of the boundary.** v0.3 defined a component by the pair of regions it separates. On a torus one pair can share two disconnected loops, and L2's example scores 0 with a 100-bond loop displaced ten cells. Components are now traced as connected boundary pieces (§5.5 step 3); that example scores 10.
- **(F2) Same-family terrains use one comparison array for both compositions.** v0.3 rounded each index separately and called the resulting difference between the two families "rounding, not geometry". That was wrong: in this evaluator the mask is the geometry, and on the actual TC arrays L2 built a valid panel labelled compatible under P and adverse under H. Both compositions now take their contours from the same array on TA, TC and TD (§3.4 step 3), so they cannot disagree there.
- **(F3) Contour constancy is descriptive only `[RULED 2026-11-13]`.** v0.3's noise reference did not estimate the noise in its own numerator, and bins spanning several λ values contain legitimate variation under the very alternative the report was meant to bear on (L2's example gives a ratio of 54 there). The claim that the report is evidence against the uncoupled alternative is withdrawn. Flight 9 has no quantity, scored or reported, that bears on collective reinforcement.
- **(F4) The qualification declaration is completed:** truth certified on the actual population map after clipping; sampling laws, calibration transformations, fallbacks and stops fixed here; component strata that exercise the component term; single-contour and decision-unit truths corrected (§6).
- **(F5) The calibration stop path is defined exactly** (geometric feasibility, §5.5 steps 1–4 only) and the standard-error estimator is stated; register entries A3 and A6–A9 are corrected (§1.5, §7).
- **(F6) Conforming repairs:** the TB sentence in §3.2 that contradicted the arm rule; typed persistence outputs where no bracket exists (§5.4); the fitted level's range conditional on compatible draws (§5.7); extinct-run wording (§1.3 g); T0 domains and its calibration proxy (§5.8); PROPOSED markers on the five §11.2 items.
- **(F7) Provenance:** the ordering figures of §3.3 and the TD base steps are now emitted by a committed script; two base steps were double-rounded in v0.3 (0.146 and 0.143; they are 0.145 and 0.142); the 1.3-cell wander figure of A3 was an uncomputed heuristic and is removed; A6's basis cites the committed script it came from.
- **m = 40** keeps its value; the statement that such a component "could stand as an edge by itself" was too strong and is removed (§5.5 step 6).

**v0.3, 2026-11-13 — superseded v0.2 (`8dd4b4e6a5b161a7`, committed at `d7c8312`, retained).** Answers L2's round-1 contract review (`L2_F9_CONTRACT_V0_2_ROUND1_REVIEW_2026-11-13_RECEIVED.md`, `1473d63371701c06…`: **NOT YET FREEZABLE**, ten repairs R1–R10; Q1 and Q2 ACCEPTABLE) and the discussion that followed (L1's message, `L1_TO_L2_F9_CONTRACT_V0_2_DISCUSSION_2026-11-13.md`; L2's response, `L2_F9_CONTRACT_V0_2_DISCUSSION_RESPONSE_2026-11-13_RECEIVED.md`, `4cfcb442b7499b35…`), and records Mike's ruling of 2026-11-13 ("I rule affirmative to all") on L1's recommendations. L1 re-ran every counterexample in both L2 documents; all hold.

**The principle Mike ruled under (2026-11-13), binding on this draft.** Be restrictive wherever there is a risk of an unearned positive result, and not restrictive for its own sake. Where a choice trades scientific usefulness against restriction, examine the trade closely. Do not assume a fact that an experiment can test: design the test, declare it and its consequence before its data exist, and do not damage the experiment's integrity in either direction. §1.5 is the register of what this contract assumes and how each assumption is tested.

**Changes from v0.2.**
- **(R2) The discrepancy is a joint statistic.** v0.2's 95th-percentile distance could ignore an entire missing component (L2's example gives 0 with a 40-bond island absent) while §5.5 claimed otherwise. The statistic is now the larger of the global distance and the 95th-percentile distance of every resolved component on both sides, and one contour must satisfy all of it (§5.5 step 6). L1's first repair, a per-component median, was also too weak (L2's second example); the component 95th percentile is used.
- **(R3) The contour family is complete, not 99 percentile cuts.** v0.2 searched 99 cuts and called a failure "not a level set"; some cuts were empty or duplicated. L1 at first declined full enumeration on a cost it had not measured ("up to 10,000 contours"). Measured, the complete families hold 50 to 2,600 contours, and an exact pruning rule makes scoring against all of them affordable (§5.5 step 7; Appendix A.7). The claim is therefore not narrowed to a registered subset.
- **(R4) Resampling uses a support count.** 950 of 1,000 draws, failed draws supporting neither decision (§5.5 step 9). This is a changed numerical rule, not a clarification: it differs from v0.2's interpolated percentile.
- **(R5) Level, arm and flight rules are total and consistent.** The missing row is added; two adjacent adverse levels decide an arm before the insufficient-levels branch; adjacency is defined; precedence is stated per tier (§5.6, §7).
- **(R5, tightened by L1 under the principle) Discrimination is blocked by a contradicting level.** v0.2 let D be declared while some level recorded "follows rival". It no longer can (§5.6).
- **(R6) The coupling contrast is withdrawn; the error was L1's.** L1 argued that independent cells have no absorbing state and so no persistence threshold. They can still cross a finite-horizon survival criterion, at a gain that depends on a free parameter of the alternative. The diagnostic is now a skeleton persistence diagnostic and claims nothing against the uncoupled alternative (§1.3 a).
- **(New, under the principle) A reported quantity that does bear on the uncoupled alternative.** Whole-map contour constancy is given a sampling-noise reference (§1.3 b, §5.7). Reported only.
- **(R1) "Every component" means every component of the post-estimator region**, and the 3×3 mean's deterministic effects get their own known-answer cases (§5.5 step 3, §6.1).
- **(R7) Qualification is rewritten:** certified truths for the complete procedure, a generator declaration, an error table by decision unit, caps on wrong decisive answers on both sides of ε, and a separate sensitivity requirement (§6).
- **(R8) Job order and dependencies are repaired** (§8). **(R9) T0 and the reporting schemas are completed** (§5.7, §5.8). **(R10) Array identities follow one ordered procedure**, with explicit serialization and a tie rule (§3.4).
- **Three design changes ruled on a site-closure estimate** (no lattice run, no probe output; §1.0, Appendix A.8): the κ step between 1.0 and 2.0 is halved (25 levels); r on TB is 0.3 instead of 0.8; the panel is 40 seeds instead of 20. θ stays 0.20.
- **Q1 addition:** edges are unoriented (§1.4).
- v0.2's supporting `arith/contract_arith.json` carries a stale field (`stability` 9,000; the job list said 8,400) and its helper `monotone_related` did not check ties. Both are superseded by `arith_v0_3/`; the v0.2 files are left as committed.

**Status.** L1 draft. **Not frozen.** Nothing here binds until Mike ratifies a version; no instrument, master, threshold, ensemble or run is produced under this document before that. Repository `main` at `47272f232da136af0bbb7f4e2285b7f17458231c` when written (fresh clone; v0.4 was committed at `2781789`, and `47272f2` registers Overview v1.8.2 and changes no flight document). Review path: L2 round 4 → Gemini corpus audit (commission v3) → Mike's ratification → freeze.
**Lineage.** Successor to Contract F8 v0.8.4 (`e87277a2d11e948f…`, frozen; stage 1 CLOSED, qualified, at `9d3a23b`). Governed by Design Note v0.3 (`8d82e319d79402f8…`), L2's design consultation (`65d95bc3a907cf04…`), the ratified pre-probe declaration v1.0 (`473a2a165fd5cb4e…`) and the probe record (`f3affc05de26f0d7…`). Nothing in `f8` or `e1` is modified.
**Markers.** `[RULED]` = Mike's ruling of record; `[PROPOSED]` = L1 value for Mike and L2, ratified only at freeze; `[DERIVED@FREEZE]` = computed by a declared procedure from closed-form inputs before freeze; `[DERIVED@BUILD]` = computed by the built instrument before the master it precedes is drawn, committed with its identity. Where Mike has ruled a structure and its number still goes to L2, the structure is RULED and the number PROPOSED.
**Notation.** Contract F8 names carry; the notation-scope table governs. **At first use: μ here is the deactivation rate (the Overview's lapse rate β), not the Overview's μ(ρ).** g is the feedback gain; η_floor the spontaneous floor as a per-tick hazard, committed value η₀ = −ln(0.99); λ_i per-cell conduciveness; d_i the Moore active fraction; q = 1 − e^(−μΔt). Bases are v, u, r. New here: κ (§2.8); P and H (§2.2); θ, ε, m, S and Δ (§5.5). The Annex is not cited.
**Numbers.** Every number new to this version was written from the scripts in `arith_v0_3/` (committed at `dd17b53`), `arith_v0_4/` (committed at `2781789`) and `arith_v0_5/` (committed with this version; identities in Appendix A.9), run in L1's container (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1) on terrain arrays, the Moore adjacency, closed-form constants, the site closure and synthetic maps. Array hashes are container values and provisional (§3.4).

---

## 1. Object and claim grammar

**1.0 Provenance (dated record).** The claim grammar was fixed in the pre-probe declaration §1, ratified by Mike on 2026-11-12 before any Flight 9 lattice output existed. A noncanonical probe then ran once (896 runs, 4 seeds, master 9920261112, retired). Stated here so that no reader infers otherwise:
- **Selection.** L = 100, the finer κ grid, the retention of T0, TA and TC and the respecification of TB were decided with probe output known. Inference on these terrains is conditional on that selection.
- **Known before this contract.** At 4 seeds the skeleton was extinct at κ ≤ 1.25 and survived at κ ≥ 1.75 on every probed arm. On TC the inside-to-outside occupancy ratio was 0.26–0.34 under P and 0.68–0.73 under H for κ from 1.25 to 2.00. Neither the persistence diagnostic nor TC's suppression contrast (§1.3) is independent of the probe.
- **Not seen.** L1 has rendered no occupancy map from probe output, computed nothing from probe output against λ contours and extracted no edge from it. The array files have not been opened. L1 has seen the probe report's occupancy percentiles (R-3), map correlations (R-4), the TB x-only variance fraction (R-5) and the TC ratio (R-6).
- **θ's standing (L2 round 1, Q2: acceptable as disclosed).** θ = 0.20 is a post-probe design choice, frozen before fresh canonical observations. It is not a blind prediction. "Probe output enters no gate" means probe observations are not reused as scoring or calibration data; it does not mean the probe supplied no design information. Canonical inference is conditional on the disclosed selection; every registered sensitivity result is published; changing θ later is a new instrument.
- **Closure estimates computed for this version.** L1 iterated the site closure of §4.2 on the contract terrains and counted, per arm and level, whether the closure's map has an edge at θ (Appendix A.8). No lattice was run and no probe output was read. The closure is a mean-field object with a known bias: on T0 it gives occupancy 0.199 at κ = 1.0 where the probe's flat arm measured 0.168. These estimates led to three rulings (grid step, r on TB, seeds). They are design information of the feasibility kind, disclosed as such. No closure map was compared with any λ contour.
- **Never run:** the respecified TB (now with r = 0.3) and all four TD variants.
- **Errors of L1's recorded in this register:** the probe record's statement that TC "gives the two rules different spatial output" (it was a difference of amplitude; §3.3); a wrong count in a recommendation Mike ruled on (v0.2 header); the coupling claim for the skeleton diagnostic (R6); a missing-component claim the statistic did not support (R2); a cost objection made without measuring the cost (R3); a component definition that merged disconnected loops (F1); the statement that a difference between the two rounded families was "rounding, not geometry" (F2); a noise reference that did not match its numerator and an inference it could not support (F3); two table values rounded twice (F7); a statement about every level set of an index, where the rounded family supports a statement about its own members only (R3-1); qualification strata declared without checking that they could be built, which on the canonical terrains they cannot (R3-2).
- Probe observations enter no gate, tolerance, calibration or qualification, and never become canonical observations.

**1.1 The object.** On a lattice whose bases differ from cell to cell and are frozen in time, with one action stream per cell, coupled only through local reinforcement of registration: (i) whether the two prescribed compositions give spatial output that can be told apart at declared resolution, and (ii) whether, under each prescribed composition, an observed boundary defined without reference to λ can be represented by a level set of that composition's local λ. Operationally the level sets examined are the registered family of §3.4, and the scored statements are about that family (§1.2 B).

**1.1′ What the finite instrument can claim.** One lattice size (N = 10,000), one horizon, a 40-seed dynamics panel on deterministic terrains, a declared spatial resolution. Forty seeds on a fixed terrain are not forty terrains. Results hold for the declared rule, terrain, object, size, horizon and resolution. No lattice result selects which composition describes entrepreneurial ecosystems. `F_LR` and `F_2_symmetric` are untested; a product-against-mean contrast does not select multiplication among zero-collapsing functions. One lattice size is not a scaling study.

**1.2 Endpoints (two results, each with its own record; no headline word is derived from them `[RULED]`).**

- **B, conditional boundary compatibility — the scored substantive endpoint `[RULED; scope RULED 2026-11-14]`.** For each composition X and each required terrain (§3.3), in the realization: the operational occupancy boundary of §5.5 is, or is not, within the permitted discrepancy ε of some contour of the **registered family** of λ^X, under the joint discrepancy of §5.5. The registered family is the complete set of level sets of the comparison array of §3.4, which is resolved to 12 decimal places. A pass is geometric compatibility within the declared scope. A valid failure says that no registered contour represents the boundary at that resolution, for that rule, terrain, object, size and horizon. **It does not establish that no level set of the raw index does.** Rounding merges values that differ below the twelfth decimal place, which removes some raw level sets, and a removed level set can decide differently: on TD-1-2 a boundary that is exactly a raw-H level set (raw discrepancy 0) lies 19.5 cells from every registered contour, and the two index values that separate it differ by 5.6e-17 (L2 round 3; §6.1 class 24).
- **D, conditional discrimination `[RULED]`.** On the terrain designated for it (TB), each arm's boundary is compared with both registered contour families. D is DISTINGUISHED under the rule of §5.6. A pass establishes a distinguishable output consequence of changing the composition in the instrument and nothing about which composition describes ecosystems. A non-pass can mean an uninformative terrain, insufficient resolution or indistinguishable output.

**1.2″ The bridge from PD7 to the observed boundary (instrument-level) `[RULED]`.** PD7 commits the activation surface Λ = Λ*. This contract operationalizes "an observed boundary" as the **operational occupancy boundary**: the edge of the region where the spatially averaged seed-mean occupancy of the realization is at least a fixed θ (§5.5). It is an instrument object. It is not the skeleton's persistence threshold, and on a smooth terrain it need not mark any abrupt change. The bridge is this contract's declaration, not a commitment of the theory.

**1.2′ Fidelity tier (pre-registered in full; reported with uncertainty in every record, favorable or not; never scored).** (i) Skeleton finite-horizon persistence threshold κ̂_c per arm against the spectral crossing κ = 1, as normalized and raw-g shifts; against T0's own κ̂_c. (ii) Local m_i = g·λ_i·Δt/q on the observed edge, against 1 (a local homogeneous benchmark) and against κ̂_c,T0; neither is a pointwise prediction. (iii) Seed-mean occupancy against the site closure's fixed-point probabilities (§4.2), matched in object and floor; where edges are compared, the §5.5 rule is applied to both maps. The lattice map is a finite-tail mean and the closure a fixed point, so their difference includes finite-time effects and is not an isolated stationary closure error. (iv) The fitted level λ*_X of §5.5 at each level. Uncertainty recipes are in §5.7. A poor comparison is published as such and never becomes a scored failure.

**1.3 Reported only (mandatory reporting items; never scored, never tested; none enters B or D).**
- **(a) Skeleton persistence diagnostic `[RULED 2026-11-13; the 36-of-40 count PROPOSED]`.** For every terrain arm, in the skeleton (η_floor = 0, all cells active at t = 0): the surviving seeds s of 40 at each of the 25 levels, each with a two-sided 95% Clopper–Pearson interval for the survival probability (pointwise; not a simultaneous band and not an interval for κ̂_c); and the profile description, κ̂_c and bracket of §5.4's table. A level "meets the criterion" when s ≥ 36; that is a panel criterion, not a statement that the survival probability is at least 0.9. **It makes no claim about coupling.** Independent cells with a fixed activation hazard can also cross a finite-horizon survival criterion, so a persistence profile does not exclude them.
- **(b) Whole-map contour constancy — descriptive only `[RULED 2026-11-13]`.** Defined in §5.7: how much of the across-cell variation of occupancy lies within coarse contour bins, beside an estimate of the sampling noise in that same quantity. **It is not evidence for or against the uncoupled alternative.** A bin spanning several λ values contains variation of occupancy even when occupancy is a function of λ alone, and the report does not separate that from anything else.
- **(c) The flicker record** of §2.11.
- **(d) Margin summaries**, design side (§3.2) and measured side (§5.7).
- **(e) TC's suppression contrast:** mean occupancy over cells inside the patch (bump ≥ 0.5) and outside it (bump ≤ 0.05), and their ratio, per arm and level; the sets are those of the pre-probe declaration (R-6).
- **(f) The evaluator's full output at θ = 0.10 and θ = 0.30.** These never replace or rescue the scored result.
- **(g) The skeleton's boundary** under the §5.5 rule, on the unconditional seed-mean map of all 40 seeds (an extinct run contributes its recorded tail, zeros after extinction), where that map has an edge.
- **(h) Component coverage:** for every scored level, the number of components on each side, how many are resolved, and each one's 95th-percentile distance.

**1.4 What no result here may be represented as.** A confirmation or refutation of the theory (candidates produce or fail to produce). A selection of the true composition. Evidence of collective reinforcement from D or B: an uncoupled independent-response process passes both, and Flight 9 has no coupling-sensitive contrast, scored or reported. A statement about which side of a boundary is occupied, that occupancy increases with λ, or that occupancy is a function of λ alone: the edges are unoriented, and "follows own" means geometric compatibility only. A one-to-one matching of components or preserved topology: a narrow bridge or a small hole can be indistinguishable at ε. Evidence for literal zero-collapse: TC is near-face feedback suppression, the floor does not depend on the bases, and at exactly λ = 0 a realization cell has stationary occupancy 0.0523. A statement about Regime II, Ψ, coherence or the margins hypothesis. A resolution of onset continuity. A reopening of any Flight 8 or E1 verdict.

**1.5 Assumptions, and how each is tested `[RULED in principle 2026-11-13; entries PROPOSED]`.** Each test is declared here before its own data exist, runs on its own master where it uses lattice data, is never scored, and has a consequence fixed in advance. The "basis now" column is prior design information (the probe's summaries, closure estimates, prototype timings); it is not blind, and it is kept distinct from the fresh measurement that tests each entry.

| # | Assumed | Basis now | Test | Consequence declared in advance |
|---|---|---|---|---|
| A1 | Every required arm has at least 3 levels with an edge at θ | closure estimate: 23–24 of 25 for twelve arms, 7 for TC·H, 5 for TB·H (A.8) | `calibration_census`: for each arm and level, §5.5 steps 1–4 applied to the calibration panel's 40-seed map; the count of levels passing step 4. No resampling and no contour enter this count | reported; if any required arm has fewer than 3, the stage stops before any canonical census and a new instrument version is declared. Every stopped attempt and its cause is published. Passing does not guarantee the canonical panel the same levels |
| A2 | The sampling error of the scored map is small | independent-chain approximation for the unsmoothed map: 0.003–0.006 at 40 seeds (A.5) | `calibration_census`: per cell, the standard deviation (divisor 39) across seeds of the individually 3×3-averaged seed maps, divided by √40; its median over cells, per arm and level | ceiling 0.02 on that median with the same stop path (§7) |
| A3 | Edge position is stable enough to resolve at ε on low-contrast arms | none; no estimate is offered | qualification with calibration-derived noise (§6.2); in canonical scoring a failure of this is "unresolved", never a pass | none beyond the declared outcome |
| A4 | Scoring against the complete contour family is affordable | prototype: 0.09–0.11 s per draw for both indices on three terrains (A.7) | `resource_benchmark` on the canonical machine, evaluator included | if unaffordable, a new instrument version with a registered sub-family and both endpoints' adverse statements narrowed to it, before any canonical scoring |
| A5 | m = 40 is a workable component resolution | none; it is a declared resolution | qualification strata at component sizes 38, 40 and 42 bonds on the strip fixture, each size its own stratum, both error directions and sensitivity (§6.2) | a failed qualification closes the stage |
| A6 | The implementation produces the declared post-estimator geometry, including a stripe erased and a gap filled by the 3×3 mean | `arith/smooth_check.py` (`d36b325cb7937002…`, committed at `d7c8312`): six disc cases unmoved | deterministic known-answer cases (§6.1 classes 12–16) | implementation corpus must pass |
| A7 | The complete procedure meets the declared error and sensitivity caps | none; the 950-of-1,000 rule has no established coverage | qualification (§6.2), cap 0.10 | a failed qualification closes the stage |
| A8 | (withdrawn in v0.4) | — | — | the contour-constancy report is descriptive and tests nothing |
| A9 | A recomputation of the terrain arrays elsewhere agrees with the canonical arrays to 1e-12 | container values | canonical build (§3.4): a numerical comparison only | the canonical arrays and masks are the identities of record; the comparison does not establish that separate computations give identical masks |

## 2. The substrate rule (frozen at ratification)

**2.1 Lattice and state.** L×L Moore lattice, **L = 100** `[RULED]` (N = 10,000), periodic; x_i(t) ∈ {0, 1}; Δt = 1. L = 100 refines the same unit-torus terrain the probe ran at L = 50: features double in lattice units relative to the one-cell interaction range.

**2.2 Bases and compositions.** v_i, u_i, r_i frozen for the run; Q off, Γ = 0, drive 0, noise off. Heterogeneity is between cells only `[RULED, H3]`. Two compositions `[RULED R1]`: **P** = `F_canonical` = v·u·r; **H** = `F_baseline` = (v + u + r)/3, selected under the specification's arbitration clause for rival use only, a compensatory comparator never presented as satisfying zero-collapse.

**2.3 Local density.** d_i(t) = (active Moore neighbours of i at t)/8.

**2.4 Transition probabilities, from the state at t, applied simultaneously (Contract F8 §2.4 with a per-cell λ).**
- inactive → active: 1 − exp(−[η_floor + g·λ_i·d_i(t)]·Δt)
- active → inactive: 1 − exp(−μ·Δt)
No other term. The floor is not gated by any base, and floor-generated events are not masked out of density `[RULED]`.

**2.5 Timing and streams.** Synchronous two-phase advance, one uniform per cell per tick. **Every run has its own derived stream**, keyed by (panel master, terrain, composition, object, initialization, κ in integer micro-units, seed index); nothing is paired between arms, objects or levels `[RULED]`.

**2.6 Objects.** Realization: η_floor = η₀, stationary floor-only start; the primary object for B and D `[RULED R12]`. Skeleton: η_floor = 0, all cells active at t = 0; the structural reference and the object of the persistence diagnostic. Extinction is a valid observation.

**2.7 Deactivation.** μ = 0.2 (q = 0.181269; mean complete active spell 1/q = 5.5167 ticks at every cell and level, an implementation check and not an observable).

**2.8 Control.** Bases frozen, g swept `[RULED R5]`. For composition X on a fixed terrain, with A the Moore adjacency: B_X = diag(λ^X)·A/8; g_spec,X = q/(Δt·spr(B_X)); **κ = g/g_spec,X** `[RULED]`. Conditions, all binding: computed from terrain arrays and adjacency before any dynamic data; raw bases, raw λ, spr, g_spec, g, κ and local m_i all persisted; never normalized by an observed onset, occupancy or fitted edge; if spr = 0 there is no finite crossing, no division and no level; raw-g values reported beside κ; the normalization is fixed for scored analysis. The crossing at κ = 1 is true by definition. The equivalence of sweeping g and scaling λ is specific to this rule (notation row, §10). The spectral radius of record is the value the canonical build computes by the committed routine; a recomputation elsewhere agrees to 1e-9 relative or the discrepancy is recorded `[PROPOSED]`.

**2.9 Levels.** 25 values of κ in integer micro-units `[RULED 2026-11-13; values PROPOSED until freeze]`: 0.75; 1.00 to 2.00 in steps of 0.05; 2.25; 2.50; 3.00. The same grid for every arm. No level is added, dropped or selected after any canonical output exists.

**2.10 Horizon and panel.** T = 3,000 ticks; recording tail = last 1,000 `[PROPOSED, carried]`. **40 seeds per configuration** `[RULED 2026-11-13]`. Fresh masters throughout, drawn in the stages of §8 `[DERIVED@BUILD]`.

**2.11 Flicker record (pre-probe declaration §6, incorporated unchanged; discharges Interpretation 004 point 4).** Windows W ∈ {1, 10, 100} ticks, non-overlapping complete blocks aligned to the first tick of the tail; a window is active if the cell is active at any tick in it. Persisted per cell, per run, per W: A (active windows), R₀ (observed inactive segments), first and last window states. Statistic: W·(n − A)/R₀ ticks; an all-active record returns "undefined: no inactive segment"; segments touching either end are flagged as possibly censored. Coverage: every run at every level of §2.9. Recorded, not tested. Reporting aggregation is in §5.7. The window set is left as declared `[RULED]`. The participation window stays W = 1 tick (PD5).

## 3. Terrains (all closed-form on the unit torus; cell (i, j) at x = i/L, y = j/L)

**3.1 The family `[RULED]`.** With c(z) = cos(2πz):

| Terrain | Definition |
|---|---|
| T0 flat | v = u = r = 0.8 |
| TA concordant | v = u = r = 0.6 + 0.15·(c(x) + c(y)) |
| TB cross-gradient | s = 0.55 + 0.07·c(x); d = 0.19 + 0.19·c(y); v = s + d; u = s − d; **r = 0.3** |
| TC near-face | bump = ((1 + c(x − ½))/2)⁴·((1 + c(y − ½))/2)⁴; v = r = 0.9; u = 0.9 − 0.85·bump |
| TD margin variants | v = u = r = 0.3 + 0.6·½·(1 + tanh(δ/w)), δ the distance in cells to the edge of the core C, positive inside |

**3.2 TB and TD as ruled.**
- **TB.** The product is r·(s(x)² − d(y)²), exactly additive in x and y. Criterion `[RULED]`: the product's x-share of across-cell variance lies in [0.40, 0.60]. Measured: **0.5173 along x, 0.4827 along y**; r scales the product uniformly and does not change the shares. The height index (2s + r)/3 varies along x only. **r = 0.3 `[RULED 2026-11-13, replacing 0.8 of 2026-11-12]`** raises the height index's max/min from 1.16 to **1.22**. Reason: under the closure estimate the H arm had an edge at θ at only 2 of 15 levels as first ruled; with r = 0.3 and the halved step it has 5 of 25 (A.8). TB·H remains the weakest arm. Its record follows from §5.6 and §7 like any other arm's. If the calibration census finds fewer than three levels with an edge there, the stage stops (§7).
- **TD `[RULED]`.** The core C is a fixed set of cells given in closed form, with no reference to λ, g or either composition: the union of n equal discs centred on cell corners, **|C| = 2,000 cells exactly** in every variant. n = 1: centre (49.5, 49.5), R = 25.3 cells. n = 4: centres (24.5 or 74.5, 24.5 or 74.5), R = 12.65 cells. No cell centre lies within 0.03 cells of the edge. Four variants, n ∈ {1, 4} × w ∈ {2, 4} cells:

| Variant | Lattice perimeter of C | Band cells (10–90% of the base step) | Band / core | Largest base step per cell |
|---|---|---|---|---|
| TD-1-2 | 200 | 676 | 0.338 | 0.145 |
| TD-1-4 | 200 | 1,376 | 0.688 | 0.074 |
| TD-4-2 | 416 | 1,424 | 0.712 | 0.142 |
| TD-4-4 | 416 | 2,816 | 1.408 | 0.074 |

  Each disc of the four-disc core has 104 edge bonds. No criterion, threshold, evaluator branch or stopping rule refers to the margins hypothesis `[RULED, H2]`.

**3.3 Terrain roles `[RULED]`.** Two indices have the same contour family when each is an increasing function of the other. That holds by formula on TA and TD (P = t³, H = t, t the common base) and on TC (P = 0.81·u, H = (1.8 + u)/3). On those terrains both compositions take their contours from one array (§3.4 step 3), so their families are identical as sets of masks, by construction. On TB the families differ: following cells in order of increasing P, H falls by as much as 0.0876; on every other terrain it never falls by more than 2.3e-16 (`proto_checks_v4.json`).

| Terrain | Same contour family? | Role |
|---|---|---|
| T0 | both indices constant: no contour exists | implementation and fidelity reference; not a required case; never scored by §5.5 |
| TA | yes | non-identifiability control for D; required case for B |
| **TB** | **no** | **required case for D**; required case for B |
| TC | yes | required case for B; suppression contrast reported |
| TD (all four) | yes | required cases for B (a stress family across geometries); margins descriptive |

Both compositions run on every terrain except T0 `[RULED]`. Per composition there are **seven required arms for B**; across both, fourteen. On TB, a P contour at its deciles lies 14.3 to 31.6 cells from the nearest H contour of the complete family, and an H contour 14.0 to 24.7 cells from the nearest P contour (global distance; A.2). **D rests on TB alone.** Amplitudes may not be substituted for contours. A role is never changed after any canonical output exists.

**3.4 Identities — one ordered procedure (R10) `[PROPOSED]`.**
1. **At freeze:** formulas, parameters, the serialization and the comparison rules below are committed. Container hashes in Appendix A are explicitly provisional.
2. **Serialization.** A base array is shape (100, 100), axis 0 the x index, little-endian IEEE float64, C-contiguous. A terrain's base identity is the SHA-256 of the bytes of v, then u, then r.
3. **Comparison arrays and the tie rule.** Contours are level sets of a **comparison array** ω, rounded to 12 decimal places before any ranking or thresholding; a level set is {ω ≥ ℓ}. On a same-family terrain ω is one array for both compositions: the common base t on TA and TD, and u on TC. On TB each composition has its own: ω = λ^P or λ^H. The composition's own index value on a contour is carried as a label for fidelity (t³ or t; 0.81·u or (1.8 + u)/3) and decides nothing. The dynamics and the spectral normalization use the raw index λ^X, not ω. On a same-family terrain the raw index is a non-decreasing function of ω to within 1e-12 (checked). That relates the two orderings and establishes nothing further. **The registered family is complete for ω, not for the raw index.** Rounding removes level sets (distinct proper level sets before rounding against registered: TA 2,221 / 1,300; TC 1,389 / 1,180; TD-1-2 861 / 681; TB under P 3,840 / 2,600; TB under H 59 / 50; none removed on TD-1-4, TD-4-2 and TD-4-4), and a removed level set can lie far from every registered one (§1.2 B). Agreement of scalars to 1e-12, identity of masks, and completeness over a named family are three different properties. This contract claims the second for the two compositions on same-family terrains, and the third for ω only.
4. **At build, before any master is drawn:** the canonical machine builds the base arrays, the comparison arrays, the complete contour family of each (§5.5 step 5) with its traced components, and the spectral values, and commits their identities. It verifies that on every same-family terrain the two compositions' families are the same set of masks. These canonical objects are the ones every later job uses and binds.
5. **Cross-platform check.** A recomputation elsewhere must agree with the canonical base arrays to 1e-12 per element; the largest deviation is recorded. That tolerance checks numerical agreement only. It does not guarantee identical masks, which is why the canonical masks themselves are bound.
The core C of TD is exact on both platforms.

## 4. Comparators (fidelity; never scored)

**4.1 Spectral crossing.** κ = 1 by construction; g_spec per arm in Appendix A. It is the zero-floor site-closure comparator; its lattice counterpart is the skeleton's finite-horizon persistence threshold κ̂_c. The realization has activity at g = 0 and has no absorbing-state onset.

**4.2 Site closure.** p_i′ = (1 − p_i)·[1 − exp(−Δt·(η_floor + g·λ_i·Σ_j A_ij·p_j/8))] + (1 − q)·p_i, iterated from p = 1 (skeleton) or p = π₁ (realization) to a fixed point: tolerance 1e-12 in max norm, at most 200,000 iterations `[PROPOSED]`. Nonconvergence is recorded "comparator unavailable" for that arm and level and affects no endpoint. m_i = 1 is a local homogeneous benchmark, not the closure's edge.

**4.3 T0 as the lattice reference.** The reference object is **κ̂_c,T0**, T0's control-axis persistence threshold from its own skeleton-high sweep at L = 100 on the §2.9 grid, with its survival counts and its absent or non-monotone cases. T0's index is constant and has no level-set contour; a spatial occupancy edge on T0 would be noise and is never compared with anything. Flight 8's 1.521739 is not used as a constant. T0's measured value never retunes a scored tolerance.

## 5. The instrument (package `f9`, new beside `f8`; nothing in `f8` or `e1` modified)

**5.1 N1 — rule, terrains, levels, record.** Per-cell-λ step; terrain builder per §3.4; the §2.11 record; per-tick global active count; extinction tick; survival. **Reduction requirement (apparatus):** with a constant λ array the step returns exactly the placed Flight 8 scalar step's array at equal state, effective gain, floor, μ, timing and uniforms; initialization, stream identity and observables are checked separately. M2, M4 and M6 are not carried `[RULED R11]`.

**5.2 N3 — null reference.** The floor-only stationary occupancy π₁ = 0.0523 carries analytically. No Flight 8 band, tolerance or threshold is carried.

**5.3 N5 — closure.** §4.1–§4.2 per arm.

**5.4 Skeleton survival and the persistence record.** survival = active count > 0 at every tail tick. A level meets the criterion when s ≥ 36 of 40 `[PROPOSED: Flight 8's 18 of 20 at the same proportion]`. The profile is described, and κ̂_c and its bracket recorded, by the first row that applies. Every bound is a panel and grid description, never a population confidence bound.

| Observed profile | Description | κ̂_c and bracket |
|---|---|---|
| Some level meets the criterion and a higher level fails it | "non-monotone criterion profile" | if a terminal stretch meets the criterion, its lowest level is recorded as a descriptive suffix statistic; otherwise unavailable. Never a monotone-crossing claim |
| Every tested level meets the criterion | "criterion met at all tested levels" | κ̂_c = the lowest tested level; unbracketed on the lower side |
| No tested level meets the criterion | "criterion met at no tested level" | unavailable |
| A failing lower stretch, then a terminal stretch meeting the criterion | "both criterion phases observed" | κ̂_c = the first level of the terminal stretch; bracket = the failing level just below it and κ̂_c |

Interval records are supplied for the endpoints that exist; an absent endpoint has its unavailable cause.

**5.5 N-E — the composition evaluator (complete algorithm).** Applied to each realization arm at each level, for each index Y ∈ {P, H}. The order is binding: occupancy estimate, occupancy criterion, edge, comparison. λ, g, κ and the terrain enter nowhere in steps 1–4.

1. **Occupancy estimate `[RULED]`.** p̄_i = mean over the 40 seeds of A_i(W = 1)/1,000. p̃ = the 3×3 periodic box mean of p̄. **The population target** is the edge, at θ, of the 3×3-averaged population-mean finite-tail occupancy on this fixed terrain, object and horizon. It is not the mean of per-seed discrepancies and says nothing about a typical seed's edge.
2. **Occupancy criterion `[structure RULED; value PROPOSED]`.** The operational occupied region is R = {i : p̃_i ≥ θ}, ties included, **θ = 0.20** for every arm, terrain and level (an excess of 0.148 over the floor reference).
3. **Edge and components `[RULED; conventions PROPOSED]`.** E = the set of unit boundary segments between a cell of R and a 4-neighbour outside R, with periodic wrapping, each represented by its midpoint ("bond"). Every bond has equal weight. **Every component is included**, where a component is defined on the post-estimator region R as a **connected piece of the boundary**: two segments belong to the same component when they meet at a cell corner. Where four segments meet at one corner (two cells of R touching only at that corner), each of those cells' own two segments are joined to each other and not to the other cell's; this is the convention of a 4-connected region and an 8-connected complement. So two cells touching only at a corner have separate boundaries, a hole has its own component, and a strip that wraps the torus has two. Components are not matched one-to-one across the two sides and no topology is claimed. The 3×3 mean can remove a one-cell-wide feature or fill a one-cell-wide gap before this step; that is a property of the declared estimator and is tested as such (§6.1).
4. **Informative level `[RULED; counts PROPOSED]`.** R and its complement each have at least 100 cells, and E has at least 40 bonds. An empty or full R is `no edge at θ`. These are resolution declarations; they are not 100 independent observations.
5. **The contour family `[RULED 2026-11-13: complete family]`.** For index Y, on its comparison array ω of §3.4: the family 𝒞_Y is every set {ω ≥ ℓ} for ℓ a distinct value of ω other than its minimum. Each is non-empty and proper by construction, no two are equal, and the family is every level set of ω. It is the **registered family**: complete for ω, and not for the raw index (§3.4 step 3). The contour C(ℓ) is that set's edge with its components, by step 3. Sizes: 50 (TB under H) to 2,600 (TB under P) (A.7). A single eligible contour is a valid family, and an edge may match it. A constant index has an empty family: `no eligible contour`, an unavailable state distinct from an absent observed edge.
6. **Joint discrepancy `[RULED 2026-11-13; m PROPOSED]`.** With d(·,·) the Euclidean distance on the torus between bond midpoints, Q₀.₉₅ the 0.95 quantile with linear interpolation between order statistics, and K_m(·) the components with at least **m = 40 bonds**:

   S(E, C) = max{ Q₀.₉₅ of d(e, C) over e ∈ E; Q₀.₉₅ of d(c, E) over c ∈ C; for every K ∈ K_m(E), Q₀.₉₅ of d(e, C) over e ∈ K; for every H ∈ K_m(C), Q₀.₉₅ of d(c, E) over c ∈ H }.

   Distances are to the whole opposite edge set. If a side has no resolved component, that side adds no term, and the record says no resolved component was checked there. Components under m bonds stay in E or C, in the two global terms and in the record; they are not erased, merged or down-weighted. The claim this supports: **every resolved component receives its own geometric check.** It does not support "a missing component of any size cannot be overlooked". m = 40 matches the bond-count part of the informative-level minimum and is otherwise a declared resolution with no further justification (a 1×19 strip has 40 bonds and only 19 cells, so it is resolved here and would not be an informative region). Each TD disc (104 bonds) is resolved.
7. **Fit, and the exact decision `[RULED]`.** Δ_Y = min over C ∈ 𝒞_Y of S(E, C). **One contour must satisfy the whole of S.** The decision uses only whether Δ_Y ≤ ε. An implementation may skip any contour that cannot satisfy the first term: a bond of C within ε of a bond e has both its cells within ε + 0.5 of e, so ℓ lies between the least and greatest index value over those cells; a level outside that interval for more than the allowed share of E has S > ε. This pruning is exact for the decision, and the build must show, on the known-answer corpus, that pruned and unpruned decisions agree in every case. The fitted level λ*_Y is the composition's index label at the minimizing ℓ (the lowest ℓ if several tie), reported only for a map or draw with Δ_Y ≤ ε; otherwise the record says "no registered contour within ε" and reports the least S among the contours examined with the contour it belongs to, labelled as a descriptive value that need not be the family minimum. If no contour was examined, the record says so. λ* is fidelity; its location is never scored.
8. **Permitted discrepancy `[structure RULED; value PROPOSED]`.** **ε = 2.0 cells.** It controls how far, in lattice cells, the operational occupancy boundary and each of its resolved components may lie from a registered contour and still be called represented by it. One cell is the interaction range and a bond midpoint lies half a cell from either cell centre; two cells is that resolution with a margin. This is a design convention, not a bound on the estimator's error; the qualification prices the complete procedure around it. A different ε is a different instrument. ε is never enlarged because precision is poor.
9. **Uncertainty: an empirical bootstrap-support rule `[RULED 2026-11-13]`.** Applied only when the observed level is informative and 𝒞_Y is non-empty. 1,000 resamples of the 40 seed maps with replacement, from a declared evaluator stream; steps 1–7 recomputed in full on each, the same resampled map serving both indices. Each draw is typed: valid with Δ ≤ ε; valid with Δ > ε; or invalid (it fails step 4), with its reason. Counts n_C, n_A, n_I are persisted. No draw is replaced.

   | Condition, in this order | Result for index Y |
   |---|---|
   | n_I > 50 | not informative, cause `unstable edge` |
   | n_C ≥ 950 | compatible |
   | n_A ≥ 950 | adverse |
   | otherwise | unresolved |

   The denominator is always 1,000. An invalid draw supports neither decision and is never assigned a zero or infinite discrepancy. A runtime fault or corrupt input is an apparatus failure (§7), not an invalid draw. The rule is not a calibrated 95% confidence statement: thresholding, component changes, quantiles and minimization make the statistic non-smooth, and 40 maps do not establish coverage. Its operating behaviour is what §6.2 qualifies. The stream and the draw count are frozen; no rerun is made to move a label.
10. **Sampling arithmetic.** Under an independent-chain approximation the per-cell standard error of p̄ at 40 seeds is 0.003 to 0.006 for occupancies from 0.05 to 0.5 (A.5). The calibration census replaces these.

**5.6 Outcome records and aggregation `[RULED]`.** Three tiers, each with its own rule. A lower tier's record is always kept.

- **Level tier (own = the arm's composition; rival = the other).** Two statuses are recorded separately.

| Own | Rival | B status at the level | Discrimination status at the level |
|---|---|---|---|
| compatible | adverse | follows own | rival excluded |
| compatible | compatible | follows own | not distinguished (same-family terrain: not adjudicable here) |
| compatible | unresolved | follows own | rival not established |
| adverse | compatible | own adverse | follows rival |
| adverse | adverse | own adverse | follows neither |
| adverse | unresolved | own adverse | rival not established |
| unresolved | any | not distinguished | not distinguished |

  On a same-family terrain the two indices share one family, so own and rival statuses are equal by construction; the discrimination status there is always recorded "not adjudicable here".
- **Arm tier (B).** Rules in this order. (1) Any level unevaluable for an apparatus reason: the arm has **no qualified determination**. (2) "Own adverse" at two levels that are neighbours on the registered grid of §2.9, both informative, with no level between them: **ADVERSE**. This applies even if only two levels are informative. (3) At least 3 informative levels and "follows own" at every informative level: **COMPATIBLE**. (4) Otherwise **NOT DISTINGUISHED**, with cause (`insufficient informative levels`, `isolated adverse level`, `finite resolution`). An isolated adverse level is kept in the record as adverse at its level; the arm rule asks for replication before the arm is called ADVERSE. A COMPATIBLE record states the informative levels it rests on; passing every informative level is not evidence about the others.
- **Flight tier, B per composition X — a conjunction over the seven required arms; no vote across terrains.**

| Situation, in this order | B for composition X |
|---|---|
| Qualification not passed, or any required arm without a qualified determination | no qualified scientific determination |
| At least one required arm ADVERSE | **NOT PRODUCED** |
| No required arm ADVERSE, at least one NOT DISTINGUISHED | **NOT DISTINGUISHED** |
| All seven required arms COMPATIBLE | **PRODUCED**, with domain and resolution stated |

- **Flight tier, D, on TB.** (1) Qualification not passed, or either TB arm without a qualified determination: no qualified scientific determination. (2) **DISTINGUISHED** iff in each TB arm at least 3 informative levels carry "follows own" with "rival excluded", **and no informative level in either arm carries "follows rival"**. The witnessing levels need not be the same in the two arms; both witness sets are reported. (3) Otherwise NOT DISTINGUISHED, with cause. D can be DISTINGUISHED while B is not PRODUCED on other terrains.
- **Multiplicity.** With 25 levels, 14 terrain arms and two indices, per-level error rates compound, and both the two-adjacent rule and D search across levels. §6.2 states its error targets at the arm and flight decision units for exactly that reason.

**5.7 Reported items: schemas `[PROPOSED]`.** Package reporting items with coverage and validity checks; values gate nothing; a missing required record prevents a claim of complete reporting and does not turn into a failure of B or D.

| Report | Definition |
|---|---|
| Contour constancy, descriptive (§1.3 b) | On the **unsmoothed** per-seed occupancy maps X_s and their mean p̄. Bins: cells are ordered by the comparison array ω (ties by flat index); tie blocks are kept whole and added to the current bin until it holds at least 100 cells, when a new bin starts; a final bin under 100 cells is merged into the one before. With P the operation that subtracts each bin's mean from its cells and N = 10,000: V_within = ‖P p̄‖²/N. Its sampling-noise part is estimated by V_noise = Σ_s ‖P(X_s − p̄)‖² / (40·39·N), which applies the same within-bin centring to the seed residuals. Reported: V_within, V_noise, V_within − V_noise, the number of bins and each bin's range of ω. If V_noise = 0 the report says so; a ratio is not reported. The difference includes the variation of occupancy across the λ values inside each bin and is not attributed to anything. |
| Measured margins (§1.3 d) | On p̃ at W = 1. Core = cells with p̃ ≥ 0.30; band = cells with 0.10 ≤ p̃ < 0.30. Reported: both counts and band/core; "undefined" if the core is empty. Also the counts at the cut 0.20. Beside each, the floor reference 0.0523. |
| Flicker distributions (§1.3 c) | Cells are placed in occupancy bands [0, 0.10), [0.10, 0.20), [0.20, 0.30), [0.30, 1] by p̄. Per band and W: the median and quartiles of the statistic over all (cell, seed) records with a defined value, and the counts of undefined and of possibly censored records. |
| Fidelity uncertainties (§1.2′) | Occupancy-based items: 2.5–97.5 percentile range over 1,000 seed resamples. κ̂_c: per §5.4. λ*: its range over the resamples with Δ ≤ ε, with the number of such resamples; "no compatible resample" if there is none. That range is conditional on compatibility and is not a confidence interval. |
| Skeleton boundary (§1.3 g) | Unconditional seed-mean map over all 40 seeds; an extinct run contributes its recorded tail, zeros after extinction. |
| Component coverage (§1.3 h) | As stated there. |

**5.8 T0 `[RULED; values PROPOSED]`.** (i) The reduction of §5.1 is the apparatus check. (ii) Flight 8's four tests are rerun on T0 as a scientific consistency exercise, redeclared as follows. Sweeps: skeleton-high, skeleton-low (ρ₀ = 0.02) and realization on the §2.9 grid. Survival threshold 36 of 40. **Hysteresis bracket** Δκ = max(0.0254, 0.0055) + 0.05 = **0.0754** (Contract F8 §3.4's procedure at N = 10,000 with the fine-grid spacing; A.4). It applies only if, for each of the two skeleton boundaries, the level just below the boundary and the boundary level are both in the fine grid and 0.05 apart; a boundary at κ = 1.00 does not qualify because the level below it is 0.75. Otherwise the hysteresis test is unevaluable, cause `bracket outside fine grid`, and the other tests stand. **Continuity criterion:** for adjacent levels j, j+1 above the boundary, J_j = 0.10·(med_{j+1} − med_j)/(κ_{j+1} − κ_j); an excess of J_j over f_J = 0.25 of the branch's sampled range returns NOT DISTINGUISHED. This is a slope criterion on a non-uniform grid, at Flight 8's scale of roughly one tenth of κ. Domains follow Contract F8 §4.11: the skeleton continuity comparison runs over levels at and above κ̂_c,T0, its sampled range being the skeleton medians' range over those levels; the realization test runs over the whole grid with the realization medians' range over the whole grid, and keeps Flight 8's reversal rule. **Evaluability band:** 3·√(ŝ_X(κ₋)² + ŝ_X(κ₊)²)·1.2533/√40, ŝ_X the calibration census's seed-to-seed standard deviation of tail density for the sweep's object. The calibration census has no low-initialization skeleton panel; the high-initialization skeleton's ŝ is used as the declared proxy for the low sweep, and equal variance across initializations is not established. T0's record is PRODUCED, NOT PRODUCED or NOT DISTINGUISHED for T0 alone. It gates no endpoint, an adverse or ND result there is not automatically a coding defect, and it does not resolve onset continuity. If κ̂_c,T0 is unavailable, every T0-referenced fidelity item is recorded "reference unavailable".

**5.9 N7 — records, package, readiness.** The principles of Contract F8 §4.10 carry: completeness against readiness computed separately; valid adverse records; apparatus and qualification prerequisites require passage, scientific prerequisites valid completion; identity and authorization binding. The record graph is Flight 9's own (§8). Every record binds what exists when it is written: terrain and family identities, composition, g, κ, g_spec and spr, lattice geometry, object and floor, horizon and tail, seed and stream identity, window convention, summary schema, θ, ε and m, evaluator identity, and the **qualification protocol identity**. Only records written after qualification bind the **qualification result identity**. No record is required to cite an identity that does not yet exist. Records written before step 6 of §8 bind the frozen contract and its fixed transformations; records from step 6 on bind the sealed protocol.

## 6. Qualification of the evaluator (before any canonical scoring) `[RULED in structure; contents and sizes PROPOSED]`

**6.0 Truth.** Wherever this section says "certified", the truth is the joint discrepancy Δ* of §5.5 for the **population target of the generator as actually defined**: the generator's population-mean map (after any clipping), 3×3-averaged, thresholded at θ, traced into components, and minimized by brute force over the complete family of the index's comparison array. A nominal shift, an injected displacement or the name of the index a map was generated from is not the truth. Certification is done by code independent of the evaluator's pruned search.

**6.1 Known-answer corpus (implementation).** Every class returns exactly its named record and cause on ≥ 95 of 100; **cross-trigger rule**: the right record with the wrong cause fails. A deterministic class has one case and must be exact. h(z) = 0.06 + 0.40·z with z the comparison array scaled to [0, 1] on its terrain.

| # | Class | Expected |
|---|---|---|
| 1 | p = h(ω_P) on TB, scored as the P arm | own compatible; rival adverse |
| 2 | the same maps scored as the H arm | own adverse; rival compatible (follows rival) |
| 3 | p = h(ω_H) on TB, scored both ways | as 1 and 2 with indices exchanged |
| 4 | p = h of the TB product array under the periodic map (x, y) → (x + y, y − x) | adverse against both families (each truth certified > ε) |
| 5 | p = h(ω) on TA | own compatible; not adjudicable here |
| 6 | a map everywhere below θ; one everywhere above | `no edge at θ` |
| 7 | a region of 50 cells | `under-resolved` |
| 8 | a compatible map translated 1 cell (certified Δ* = 1.0); translated 3 cells (certified Δ* = 3.0) | compatible; adverse |
| 9 | the TD four-disc pattern with one disc absent | adverse |
| 10 | L2's five strips with a 10×10 island in the contour and not in the map | adverse (S = 6.57) |
| 11 | L2's patch that has lost a quarter of its area | adverse (S = 5.0) |
| 12 | a one-cell-wide stripe at 0.30 on 0.05 | the stripe is absent after the estimator; record per the remaining map |
| 13 | a one-cell-wide gap at 0.05 in a 0.30 region | the gap is filled after the estimator |
| 14 | a three-cell-wide channel; a 3×3 hole; an asymmetric profile across an edge; a plateau within 0.005 of θ | each as certified on the post-estimator map |
| 15 | two blocks touching at a corner; a block with a hole; a strip wrapping the torus | two components each, of the certified sizes |
| 16 | **on the strip fixture of §6.2** (island in the first gap, y₀ = 20; map 0.30 on the occupied set and 0.10 elsewhere): the island of 38, 40 or 42 bonds absent from the map; then present in it. The island is 3.66%, 3.85% or 4.03% of the contour's perimeter and 3 cells from the nearest strip side | absent, 40: adverse through the component term alone (S = 6.569; both global terms 0); absent, 42: the same (S = 6.519); absent, 38: compatible (S = 0), with "not checked as a component"; present, 40 and 42: compatible (S = 0.707; the estimator removes the island's four corner cells); present, 38: compatible (S = 0) |
| 17 | a constant index | `no eligible contour` |
| 18 | resample sets built to give exactly 50 and exactly 51 invalid draws; 950/0/50, 949/1/50, 0/950/50 | per the table of §5.5 step 9; 51 → `unstable edge` |
| 19 | whole synthetic sweeps exercising each arm rule, including exactly two informative adjacent adverse levels, and a sweep with two informative compatible levels | ADVERSE; NOT DISTINGUISHED (`insufficient informative levels`); each other as certified |
| 20 | pruned against unpruned search, on every point map and every valid resample of every class | the same decision in each; the same minimizer where Δ ≤ ε |
| 21 | **L2's displaced loop:** predicted {a(y) ≤ x < 60}, observed {a(y) ≤ x < 70}, a(y) = 2 for even y and 40 for odd y | components of 3,900 and 100 bonds on each side; the 100-bond term is 10; adverse |
| 22 | **L2's TC case:** the highest contour of TC translated two cells along axis 0, built as integer occupancy counts | the same record under P and under H (S = 2.0 for both) |
| 23 | a family with one eligible contour, matched by the map; equality at ε; the strict and inclusive level endpoints of the pruning rule; periodic wrapping; no admissible contour; a lowest-level tie | compatible; compatible; each as certified |
| 24 | **L2's TD-1-2 raw cut:** R = {raw λ^H ≥ its second-smallest value} (9,772 cells, one 88-bond component); integer occupancy counts whose 3×3 mean is 0.201 inside R and 0.199 outside, the same for all 40 seeds | adverse under P and under H alike (registered minimum S = 19.506, at ω = 0.300000000001). The case checks the declared scope: R is a level set of the raw index and is not in the registered family |

Classes that need calibration-derived noise are run after the calibration record (§8); the deterministic classes are run before it.

**6.2 Statistical qualification (design and held-out ensembles).**

*Generator declaration (everything below is fixed at freeze; only the numbers σ_seed(·) and ℓ_c are derived at build, by the transformations stated).*
- **A level case** is 40 seed maps for one comparison array and one pre-noise map. Seed map: X_s = clip(μ⁰ + σ·Z_s, 0, 1) cell by cell, where μ⁰ is the case's pre-noise map, σ_i = c_σ·σ_seed(μ⁰_i) with c_σ = 1 unless a stratum says 1.5, and Z_s are independent draws of a stationary Gaussian array with unit variance and correlation exp(−(|Δx| + |Δy|)/ℓ_c) in wrapped lags, generated by exact circulant factorization. The noise is therefore not stationary in variance. ℓ_c is not scaled by c_σ.
- **Population mean, for certification:** μ_i = m·[Φ(b) − Φ(a)] − σ·[φ(b) − φ(a)] + 1 − Φ(b), with m = μ⁰_i, σ = σ_i, a = −m/σ, b = (1 − m)/σ (the mean of a normal variable clipped to [0, 1]; at m = 0.03, σ = 0.10 it is 0.0567, not 0.03). Truth is certified on this μ per §6.0. Where σ_i = 0, μ_i = μ⁰_i.
- **Two kinds of comparison array.** (i) *Canonical:* the eight comparison arrays of §3.4 (TA, TC and the four TD variants, each shared by both compositions; TB under P; TB under H). "Drawn from the canonical arms" means: a composition uniformly from {P, H}, then a terrain uniformly from the seven required terrains; the array is that terrain's for that composition. (ii) *The strip fixture*, used by the component strata and by nothing else. No canonical contour can carry those strata (the longest has 768 bonds; a 40-bond component under 5% of the perimeter needs more than 800), and changing the occupancy map cannot lengthen the contour it is compared with.
- **The strip fixture.** A synthetic index ω_F(g, y₀, b) on the same 100×100 torus: 1 on five full-height strips {20j ≤ x < 20j + 5}, j = 0…4, and on an island {20g + 8 ≤ x < 20g + 17, y₀ ≤ y < y₀ + b, y taken modulo 100}; 0 elsewhere. g is drawn uniformly from {0, …, 4} and y₀ uniformly from {0, …, 99}. The island is 9 cells wide and b cells tall: b = 10, 11, 12 gives 38, 40, 42 bonds. The family of ω_F has one contour: ten strip sides of 100 bonds each and the island (3.66%, 3.85%, 4.03% of the perimeter), the island 3 cells from the nearest strip side. Pre-noise maps: *present*, μ⁰ = 0.10 + 0.20·ω_F; *absent*, μ⁰ = 0.10 + 0.20 on the strips only. Noise as for every case. At zero noise the certified values are those of §6.1 class 16 (Appendix A.10).
- **Pre-noise maps on canonical arrays (level cases).** μ⁰ = h(ω′), h(z) = c₀ + c₁·z with c₁ uniform on [0.2, 0.6] and c₀ uniform on [0.03, 0.10], z the array ω′ scaled to [0, 1]. ω′ is the comparison array drawn from the canonical arms, transformed by the stratum's rule: for the discrepancy strata, a periodic translation by (a, b) cells with a, b drawn uniformly from {0, …, 4}; for the untranslated stratum, no translation; for neither-family maps, class 4's map; for rival-generated maps on TB, the other composition's TB array, untranslated.
- **Arm cases.** An arm case is 25 synthetic levels k = 1…25 on one comparison array, with independent noise at every level. The *generic sweep* has pre-noise map h_k(ω′) at level k, c₀ rising linearly from 0.03 to 0.10 and c₁ from 0.2 to 0.6 across the 25 levels, with one transformation ω′ for the whole sweep. Three constructions:
  - *COMPATIBLE:* the generic sweep, untranslated, on an array drawn from the canonical arms.
  - *ADVERSE:* the generic sweep translated 3 cells along axis 0, on an array drawn from the canonical arms.
  - *Low-information:* a position j is drawn uniformly from {1, …, 24}. Levels j and j + 1 take the untranslated generic maps h_j and h_{j+1}. Every other level takes the map 0.03 + 0.05·z, whose largest value is 0.08, on an array drawn from the canonical arms.

  The certified truth of an arm case is the arm record that §5.6 gives when every level takes its certified level truth, including which levels are informative.
- **Flight cases, B.** One composition is drawn uniformly from {P, H} for the whole flight. The flight has seven slots in the fixed order TA, TB, TC, TD-1-2, TD-1-4, TD-4-2, TD-4-4; slot i is an independent arm case on that terrain's comparison array for the drawn composition. No terrain is drawn at random and none repeats. *All compatible:* every slot is the COMPATIBLE construction. *One adverse:* a slot is drawn uniformly from the seven and is the ADVERSE construction; the other six are COMPATIBLE constructions.
- **Flight cases, D.** Two arms, TB·P and TB·H, each scored against both TB families as in §5.6. *One index:* an index G is drawn uniformly from {P, H}; both arms are untranslated generic sweeps of G's TB array. *One rival level:* each arm is an untranslated generic sweep of its own TB array, except that an arm is drawn uniformly from the two and a level k uniformly from {1, …, 25}, and at that level that arm's pre-noise map is h_k of the other composition's TB array. *Own-generated:* each arm is an untranslated generic sweep of its own TB array.
- **Dependence.** Within a case the noise is independent across seed maps, levels and arms. The draws stated above (array, translation, positions, slots, index, level) are made once per case and shared as stated. Cases are independent.
- **Assignment by certified truth — every row.** A candidate case is generated by its row's construction and its truth is certified: Δ* per §6.0 at each level; the arm record of §5.6 on the certified level truths; the flight record on the certified arm and level truths. A candidate is accepted into its stratum only if its certified truth is the one the row names. Otherwise it is discarded and counted, with the reason. This holds for the special rows as for the bands: an untranslated or own-generated pre-noise map is not by itself a certificate, because σ depends on the cell and clipping moves the mean. Bands for level cases: "0" = [0, 0.5]; "1.0" = [0.9, 1.1]; "between 1 and 2" = (1.1, 1.9); "2.0" = [1.9, 2.0]; "between 2 and 3" = (2.0, 2.9); "3.0" = [2.9, 3.5]. A level case must also be informative on its population map. Integer translations attain 1.0, 2.0 and 3.0; the diagonal translations (1, 1), (2, 1) and (2, 2) attain 1.41, 2.12 and 2.83 (`strata_attainability.json`; Appendix A.10). Those are attainability checks at one map, not a guarantee that every stratum fills under calibration noise.
- **Candidate budget and typed failure `[PROPOSED: 10,000]`.** For each stratum in each ensemble, at most 10,000 candidates are generated. If fewer than 200 have been accepted when the budget is spent, the stratum's record is `stratum not populated` and the qualification attempt closes as a failed qualification does (§8). No band is widened, no row is dropped, no construction or noise transformation is changed within the stage. The counts of candidates, acceptances and discards by reason are published for every stratum.
- **Streams.** Every case, level and seed map has its own stream derived from the ensemble master.
- **Calibration transformations (fixed here, before any calibration output).** Pool: every realization arm and level of the calibration census. σ_seed(p): cells are grouped by seed-mean occupancy into 50 bins of width 0.02; the bin's value is the median, over its cells in the pool, of the standard deviation (divisor 39) across seeds of the per-seed occupancy; an empty bin takes the linear interpolation of its nearest non-empty neighbours, or the nearest non-empty bin's value beyond the occupied range; σ_seed(p) is the value of p's bin. **ρ₁ is a pooled ratio.** For each pool element (arm, level) and seed s, the residual map is r_s = X_s − p̄, with X_s the unsmoothed per-seed occupancy map and p̄ that element's mean over its 40 seeds. Then

  ρ₁ = Σ r_s(i)·[r_s(i + e_x) + r_s(i + e_y)] / (2·Σ r_s(i)²),

  both sums over all cells i, all seeds and all pool elements, with periodic neighbours i + e_x and i + e_y. No spatial mean is subtracted from a residual map (the residuals are already centred across seeds at each cell). A residual map that is identically zero adds zero to both sums and is not otherwise treated. ℓ_c = −1/ln ρ₁ if 0 < ρ₁ < 0.99, and 0 (independent cells) if ρ₁ ≤ 0. **Typed stops:** fewer than 5 non-empty bins; a zero denominator in ρ₁ (zero pooled residual variance); ρ₁ ≥ 0.99. Each stops the stage like the stop paths of §7. The standard error of a mean map is never used in place of σ_seed.

*Error table. Every capped row is its own stratum of 200 accepted independent cases in each ensemble; cap 0.10 by one-sided 95% Clopper–Pearson upper bound, at most 12 errors. No two rows share a cap, no row mixes component sizes or noise levels, caps are never pooled and are not simultaneous. Halts and wrong causes count as errors in every row. Noise is at c_σ = 1 unless the row says otherwise.*

| # | Stratum | Unit | Array | Certified truth required for acceptance | Output counted as error |
|---|---|---|---|---|---|
| 1 | Δ* in "1.0" | level | canonical | band | adverse |
| 2 | Δ* in "between 1 and 2" | level | canonical | band | adverse |
| 3 | Δ* in "2.0" | level | canonical | band | adverse |
| 4 | Δ* in "between 2 and 3" | level | canonical | band | compatible |
| 5 | Δ* in "3.0" | level | canonical | band | compatible |
| 6 | **Sensitivity, compatible:** untranslated | level | canonical | Δ* in "0" | **every output other than compatible** |
| 7 | **Sensitivity, adverse:** translated | level | canonical | Δ* in "3.0" | **every output other than adverse** |
| 8 | **Sensitivity, 40-bond component absent** | level | strip fixture, b = 11 | S > ε with both global terms ≤ ε | **every output other than adverse** |
| 9 | **Sensitivity, 42-bond component absent** | level | strip fixture, b = 12 | as row 8 | **every output other than adverse** |
| 10 | 38-bond component absent | level | strip fixture, b = 10 | Δ* ≤ 1.1, with no component term for the island | adverse |
| 11 | 40-bond component present | level | strip fixture, b = 11 | Δ* ≤ 1.1 | adverse |
| 12 | 42-bond component present | level | strip fixture, b = 12 | Δ* ≤ 1.1 | adverse |
| 13 | False identification: rival-generated maps on TB | level | TB, both families | own Δ* ≥ 2.9 and rival Δ* ≤ 1.1 | "follows own" |
| 14 | False compatibility: neither-family maps | level | TB, both families | both Δ* ≥ 2.9 | compatible for either index |
| 15 | Unavailable states: constant map, saturated map, empty region, constant index (50 cases each) | level | canonical; constant index | the named cause | any decisive record |
| 16 | Arm, COMPATIBLE construction | arm | canonical | COMPATIBLE | ADVERSE |
| 17 | Arm, COMPATIBLE construction, c_σ = 1.5 | arm | canonical | COMPATIBLE | ADVERSE |
| 18 | Arm, ADVERSE construction | arm | canonical | ADVERSE | COMPATIBLE |
| 19 | Arm, low-information construction | arm | canonical | NOT DISTINGUISHED, `insufficient informative levels`, exactly two informative levels | COMPATIBLE |
| 20 | Flight B, all compatible | flight | seven slots | all seven arms COMPATIBLE | NOT PRODUCED |
| 21 | Flight B, one adverse | flight | seven slots | the drawn slot ADVERSE, the other six COMPATIBLE | PRODUCED |
| 22 | Flight D, one index | flight | TB | the arm whose composition is not G carries "follows rival" at an informative level | DISTINGUISHED |
| 23 | Flight D, one rival level | flight | TB | the drawn level is informative and carries "follows rival" in the drawn arm; without that level both arms would witness | DISTINGUISHED |
| 24 | Flight D, own-generated | flight | TB | DISTINGUISHED | none capped; the rate of DISTINGUISHED is reported. A declared choice: the qualification does not guarantee D's sensitivity |

In rows 6 to 9 the error event is every output other than the certified decisive label: the opposite label, unresolved, not informative under any cause (`no edge at θ`, `under-resolved`, `unstable edge`), and any halt. In rows 1 to 5 and 10 to 14 an unresolved or not-informative output is allowed and its rate is reported; the wrong decisive answer is capped. Row 10's truth at zero noise is compatible; if a candidate's certified truth is otherwise it is discarded like any other. Design AND held-out are joined mechanically. A failed qualification, or a stratum not populated, closes the stage; no same-stage repair. Certifying arm and flight candidates takes a brute-force search at every level of every candidate; its cost is part of what step 10 of §8 prices. Guarantees hold for the declared ensembles and decision units only; a handful of distance bands does not bound the error at all distances, the strip fixture is not a terrain of the flight, and nothing transfers automatically to the lattice.

## 7. Failure paths, with precedence per tier (highest first) `[RULED; R5]`

**Level.**

| # | State | Kind | Cause label | Effect |
|---|---|---|---|---|
| L1 | Run halted; record missing, corrupt or out of range; evaluator fault | apparatus | `apparatus unevaluable (<key>)` | level unevaluable |
| L2 | Constant index | unavailable | `no eligible contour` | index not scored at any level |
| L3 | R at θ empty or full | scientific ND | `no edge at θ` | level not informative |
| L4 | R or complement under 100 cells, or under 40 bonds | scientific ND | `under-resolved` | level not informative |
| L5 | More than 50 invalid draws | scientific ND | `unstable edge` | level not informative |
| L6 | Neither count reaches 950 | scientific ND | `finite resolution` | own or rival unresolved |
| L7 | n_A ≥ 950 for the own index | scientific adverse at the level | `no registered contour of own index within ε` | own adverse at this level |

**Arm.** A1 apparatus at any level → no qualified determination. A2 two neighbouring informative levels own-adverse → ADVERSE. A3 at least 3 informative levels, all "follows own" → COMPATIBLE. A4 otherwise NOT DISTINGUISHED (`insufficient informative levels`; `isolated adverse level`; `finite resolution`).

**Flight.** As the tables of §5.6. A missing or corrupt mandatory input propagates as "no qualified scientific determination" to both B and D where it touches a required arm; it is a prerequisite failure, not a scientific ND.

**Other.** Skeleton run extinct: a valid observation, never "missing". Site closure not converged: `comparator unavailable`, fidelity only. κ̂_c,T0 unavailable: `reference unavailable`, fidelity only.

No failed terrain is dropped, no level is selected after the fact, no role is changed, and every state is preserved. A required arm that lacks information does not disappear: it is NOT DISTINGUISHED and enters the conjunction as such. The contract does not predict that an occupied region exists at θ, so the wholesale absence of an edge is ND, not adverse. An adverse record is never recast as fidelity or ND at its own tier. **Stop paths `[PROPOSED]`:** if the calibration census shows a median per-cell standard error of p̃ above 0.02 at any arm and level, or fewer than 3 levels passing §5.5 step 4 at θ for any required arm (§1.5 A1, A2, computed exactly as stated there), or a typed stop of §6.2's calibration transformations, the stage stops before any canonical census and a new instrument version is declared; the sample size, grid and θ of this stage are never changed after data exist.

## 8. Jobs, order, authorizations `[RULED; R8]`

Each job runs only under a Mike-issued authorization naming the stage and the jobs; one authorization per step; the registry is append-only; each authorization file gets one commit. Masters are drawn in the stages shown, never all at once.

| Step | Job | Kind | Requires (passage P / valid completion C) | Produces | On failure |
|---|---|---|---|---|---|
| 0 | freeze | — | Appendix A computed; declarations, generator transformations and calibration estimators fixed | frozen contract | — |
| 1 | `build_identities` | apparatus | freeze | instrument version identity; canonical arrays, families, spectral values (§3.4) | stop |
| 2 | `reduction_check` | apparatus | 1 (P) | reduction record | stop |
| 3 | `known_answer_deterministic` | qualification | 1 (P) | corpus record, deterministic classes | stop |
| 4 | draw calibration master; `calibration_census` | apparatus, never scored, never reused | 2, 3 (P) | per-cell standard error; informative-level counts; σ_seed, ℓ_c by the fixed transformations; ŝ_X for T0 | stop paths of §7 → new instrument version |
| 5 | `known_answer_calibrated` | qualification | 4 (C, stop paths clear) | corpus record, remaining classes | stop |
| 6 | seal the qualification declaration | — | 5 (P) | **qualification protocol identity** | — |
| 7 | draw design master; `evaluator_design_audit` | qualification | 6 | design record, or `stratum not populated` | stage closes |
| 8 | draw held-out master; `evaluator_held_out_audit` | qualification | 7 (C) | held-out record, or `stratum not populated` | stage closes |
| 9 | `evaluator_qualification` | qualification | 7, 8 | **qualification result identity** | stage closes |
| 10 | `resource_benchmark` | apparatus | 1 | cost of dynamics, evaluator and qualification on the canonical machine | §1.5 A4 |
| 11 | draw canonical master; `t0_census` | scientific (consistency) | 9 (P) | T0 record; κ̂_c,T0 | recorded |
| 12 | `skeleton_census` | scientific | 9 (P) | persistence diagnostic; κ̂_c | recorded |
| 13 | `realization_census` | scientific | 9 (P) | level, arm and flight records for B and D | recorded |
| 14 | draw stability master; `census_stability` | scientific | 12, 13 (C) | arm records reproduced or not, reported | recorded |
| 15 | `fidelity_report`, `persistence_report`, `constancy_report`, `flicker_report`, `margin_report`, `component_report` | reporting | 11–13 (C) | §1.2′, §1.3, §5.7 | incomplete reporting |
| 16 | `stage1_package` | package | all | completeness and readiness, computed separately | — |

Arms: T0·P, and P and H on each of TA, TB, TC, TD-1-2, TD-1-4, TD-4-2, TD-4-4 (15). Runs: calibration 30,000; T0 3,000; skeleton 14,000; realization 14,000; stability 28,000; **89,000 in all**, about 19.5 hours at the container's probe speed (0.96 s per realization run, 0.62 s per skeleton run at L = 100). The evaluator is extra: at the v0.4 prototype's 0.09–0.11 s per draw (three terrains timed), 1,000 draws at each of 350 arm-levels is about 9 to 11 hours per θ per panel before any optimization. The canonical machine is unmeasured; step 10 prices it, and if the complete paired design proves too expensive the claimed scope is reduced prospectively with paired comparisons kept on what remains. Instrument version string `f9_stage1_v1` `[PROPOSED]`.

## 9. Declarations table

| Declaration | Value | Marker |
|---|---|---|
| L, N | 100; 10,000 | RULED |
| Compositions | P = `F_canonical`; H = `F_baseline` (rival only) | RULED |
| η₀; μ; Δt | −ln(0.99); 0.2; 1 | RULED (carried) |
| Control | bases frozen, g swept, κ = g/g_spec,X | RULED |
| κ grid | 0.75; 1.00–2.00 by 0.05; 2.25; 2.50; 3.00 (25) | RULED 2026-11-13; values PROPOSED |
| T, tail | 3,000 / 1,000 | PROPOSED (carried) |
| Seeds | 40 | RULED 2026-11-13 |
| Survival threshold | 36 of 40 | PROPOSED |
| Streams | every run its own; nothing paired | RULED |
| Terrains T0, TA, TC | probed formulas | RULED |
| TB | §3.1 with r = 0.3; x-share criterion [0.40, 0.60]; measured 0.5173 | RULED 2026-11-13 |
| TD | §3.2; \|C\| = 2,000; n ∈ {1, 4} × w ∈ {2, 4}; both compositions | RULED |
| Terrain roles | §3.3 | RULED |
| Flicker record | §2.11 | RULED |
| Scored map | seed-mean W = 1 occupancy, 3×3 mean | RULED |
| Occupancy criterion | fixed θ; scored 0.20; reported 0.10, 0.30 | structure RULED; values PROPOSED |
| Edge; components | 4-neighbour bonds, periodic; every connected boundary piece of the post-estimator region; corner rule of a 4-connected region | RULED; convention PROPOSED |
| Informative level | ≥ 100 cells each side; ≥ 40 bonds | RULED; counts PROPOSED |
| Contour family | the registered family: every distinct proper level set of the comparison array (complete for that array, not for the raw index); one array for both compositions on same-family terrains | RULED 2026-11-13; scope RULED 2026-11-14; comparison arrays PROPOSED |
| Discrepancy | joint S; Euclidean torus distance; linear-interpolated 0.95 quantile; m = 40 bonds | RULED; m PROPOSED |
| Permitted discrepancy | ε = 2.0 cells | structure RULED; value PROPOSED |
| Uncertainty | 1,000 seed resamples; 950 supporting; over 50 invalid = unstable | RULED 2026-11-13 |
| Arm rule | two neighbouring adverse → ADVERSE; ≥ 3 informative all "follows own" → COMPATIBLE | RULED |
| Flight rule, B | conjunction over seven required arms per composition | RULED |
| D | TB; ≥ 3 witnessing levels per arm; no "follows rival" level in either arm | RULED 2026-11-13 |
| Headline word | none | RULED |
| Persistence diagnostic | two-sided 95% Clopper–Pearson, pointwise; profile table of §5.4; no coupling claim | RULED 2026-11-13; the 36-of-40 count PROPOSED |
| Contour constancy | descriptive only; matched noise estimate; no inference | RULED 2026-11-13 |
| TC suppression contrast | reported only | RULED |
| T0 exercise | bracket 0.0754 with fine-grid eligibility; f_J = 0.25 on J normalized to 0.10; ρ₀ = 0.02; gates nothing | RULED; values PROPOSED |
| Qualification | §6; 200 accepted cases per stratum, 23 capped strata; cap 0.10; CP 95% one-sided; strip fixture for component strata; at most 10,000 candidates per stratum, then `stratum not populated` | RULED in structure; contents PROPOSED |
| Stop paths | standard error ≤ 0.02; ≥ 3 informative levels per required arm in calibration | PROPOSED |
| Site closure solver | start p = 1 or π₁; 1e-12; 200,000 iterations | PROPOSED |
| Identities | §3.4; comparison arrays rounded to 12 places; 1e-12 cross-platform; canonical objects of record | PROPOSED |
| Margin cuts | 0.10, 0.20, 0.30 | RULED |
| Masters | drawn by stage (§8) | DERIVED@BUILD |
| Instrument version | `f9_stage1_v1` | PROPOSED |

## 10. Notation rows to append (append-only; the table governs)

| Object | O — Overview v1.8.2 | C — this contract | Nature |
|---|---|---|---|
| Spectral-relative gain | Λ/Λ* (implicit) | κ = g/g_spec,X; equals Flight 8's m on a flat terrain | C-only |
| Sweeping g against scaling Λ | the spontaneous term scales with Λ | the floor is fixed; g and λ enter only as g·λ_i | rule-specific equivalence |
| Observed boundary | activation surface Λ = Λ* (PD7) | operational occupancy boundary: edge of {p̃ ≥ θ} | instrument-level bridge, C-only |
| Permitted discrepancy; component resolution | — | ε in cells; m in bonds | C-only; declared resolutions |
| Compositions | F (open) | P = `F_canonical`, H = `F_baseline` (rival only) | prescribed inputs; no selection claimed |

## 11. Rulings of record, and what goes to L2 in round 4

**11.1 Mike's rulings, 2026-11-13 and 2026-11-14.** (i) "I rule affirmative to all", given on the condition that L1 agreed the principle stated in the v0.3 header, which L1 did: L1's ten recommendations on the round-1 repairs, the three revisions under the principle (complete contour family; D blocked by a "follows rival" level; a noise reference on contour constancy), and the four closure-based recommendations (θ kept at 0.20; κ step halved; r = 0.3 on TB; 40 seeds). (ii) On L2's round-2 return: **"f3 descriptive and proceed directly"** — the contour-constancy report is descriptive only, which withdraws the third of those revisions, and v0.4 is written without a further discussion round. (iii) On L2's round-3 return, 2026-11-14: **"I accept your recommendation"** — L1 had recommended keeping the rounded comparison arrays and narrowing B's wording to the registered family (rather than removing the rounding), and proceeding directly to v0.5. The ruling settles the wording of the claim. Whether the comparison arrays themselves are adopted remains item 6 below.

**11.2 Proposed, for Mike's decision at ratification (consequences of the rulings that he has not ruled on by name).**
1. **Survival criterion 36 of 40**, the same proportion as 18 of 20.
2. **The calibration stop paths**: fewer than 3 levels with an edge for any required arm; the standard-error ceiling; the typed stops of the calibration transformations.
3. **The T0 continuity criterion normalized to an interval of 0.10**, the bracket 0.0754, and the high-initialization skeleton as proxy for the low sweep's variance.
4. **The assumption register of §1.5** as the form in which the principle is written into the contract.
5. **The evaluator's cost**: about 9 to 11 hours per θ per panel at prototype speed, beside 19.5 hours of dynamics.
6. **The comparison arrays of §3.4** (t on TA and TD, u on TC, each index's own on TB), with B scoped to their registered families as ruled on 2026-11-14.
7. **The qualification contents new in v0.5** (§6.2): the strip fixture; the special arm and flight constructions; the band "0" = [0, 0.5] for the compatible sensitivity row; the budget of 10,000 candidates per stratum and the `stratum not populated` closure.

**11.3 Open points for L2, round 4.**
1. R3-1: is the scope stated consistently wherever the contract speaks of a level set, a contour or an adverse cause (§1.1, §1.2 B, §3.4 step 3, §5.5 steps 5, 7, 8, §7 L7, §9)?
2. R3-2, fixtures: is the strip fixture declared completely enough to build (geometry, draws, maps, family, certificate), and is it clear which rows use it?
3. R3-2, special rows: do the arm and flight constructions fix every choice (positions, slots, the drawn arm and level, dependence), and is each row's acceptance condition the right certified truth?
4. R3-2, remaining declarations: the per-size and per-noise strata, the sensitivity error event, the pooled-ratio ρ₁, and the candidate budget with its typed failure.
5. Anything in §6.2 that still leaves a builder a choice.

## 12. Trace of requirements

**12.0 L2 round 3 (R3-1, R3-2).**

| Repair | Where |
|---|---|
| R3-1 scope of the comparison family | §1.1; §1.2 B; §3.4 step 3; §5.5 steps 5, 7, 8; §7 L7; §9; §6.1 class 24; `arith_v0_5/fixture_checks_v5.py` |
| R3-2 component fixtures | §6.1 class 16; §6.2 (two kinds of comparison array; the strip fixture; rows 8–12); A.10 |
| R3-2 special arm and flight constructions; acceptance by certified truth | §6.2 (arm cases; flight cases; assignment; rows 16–24); `arith_v0_5/special_constructions_v5.py` |
| R3-2 allocations; sensitivity error event; lag-one estimator; bounded generation | §6.2 (error table and the paragraph after it; calibration transformations; candidate budget); §8 steps 7–8 |

**12.0′ L2 round 2 (F1–F7).**

| Repair | Where |
|---|---|
| F1 connected contour components | §5.5 step 3; §6.1 classes 15, 21; `arith_v0_4/f9_evaluator_proto_v4.py` |
| F2 common-family canonicalization | §3.3; §3.4 steps 3–4; §5.5 step 5; §5.6 (level tier note); §6.1 class 22 |
| F3 constancy reference and interpretation | §1.3 b; §1.4; §1.5 A8; §5.7 |
| F4 qualification declaration | §6.0–§6.2 |
| F5 calibration and register | §1.5; §7 stop paths; §8 step 4 |
| F6 total records and conforming prose | §3.2 (TB); §5.4; §5.5 step 7; §5.7 (λ*); §1.3 g; §5.8; §9; §11.2 |
| F7 arithmetic provenance | §3.2 (base steps); §3.3; §1.5 A3, A6; `arith_v0_4/proto_checks_v4.py` |
| Q3 m = 40 rationale and strata | §5.5 step 6; §6.1 class 16; §6.2 |

**12.1 L2 round 1 (R1–R10).**

| Repair | Where |
|---|---|
| R1 post-estimator components; deterministic estimator cases | §5.5 step 3; §6.1 classes 12–16 |
| R2 component-sensitive discrepancy | §5.5 step 6; §1.3 h; §6.1 classes 9–11, 16 |
| R3 contour family, conventions, claim | §5.5 steps 5, 7; §3.4; §1.2 |
| R4 target, invalid draws, nominal bounds | §5.5 steps 1, 9; §6.2 |
| R5 level table, precedence, adjacency, propagation | §5.6; §7 |
| R6 persistence only; sampling uncertainty; crossing cases | §1.3 a; §5.4 |
| R7 truths, generator, error table, decision units | §6 |
| R8 job order, masters, typed identities, benchmark | §8; §5.9 |
| R9 T0 grid and band, reference object, schemas, fidelity qualification | §4.3; §5.7; §5.8; §1.2′ |
| R10 identity procedure; supporting arithmetic | §3.4; `arith_v0_3/`; v0.3 header |
| Q1 addition: unoriented edges | §1.4 |

**12.2 L2 design consultation (every REQUIRES CHANGE item).**

| L2 item | Where |
|---|---|
| Q1 two conditional tests; boundary against whole map; independent edge; no vacuous support; uncoupled alternative disclosed; TA's role; six labels | §1.2, §1.3 b, §1.4, §3.3, §5.5–§5.6, §7 |
| Q2 statistical qualification, six risks, seed as unit, held-out untouched | §6.2, §8 |
| Q3 rival-only status; reduction at matched effective gain; untested candidates | §2.2, §5.1, §1.1′ |
| Q4 normalization and its six conditions; rule-specific equivalence; notation row | §2.8, §10 |
| Q5 flicker estimand, windows, censoring, floor reference, bound level set | §2.11, §2.9, §5.7 |
| Q6 onset continuity left open by name | §1.4, §5.8 |
| Q7 skeleton threshold against spectral crossing; m_i = 1 a benchmark; matched estimand; solver frozen; T0 reference | §1.2′, §4 |
| Q8 probe provenance; selection; Interpretation 004 timing | §1.0, §2.11 |
| Q9 §11.1 TC near-face, floor not gated | §1.4, §2.4 |
| Q9 §11.2 contours, bins, membership, contrast; seed-mean against per-seed | §5.5, §5.7 |
| Q9 §11.3 spatial scale; TD geometry; cuts frozen | §2.1, §3.2, §5.7 |
| Q9 §11.4 own record graph; reporting items | §5.7, §5.9, §8 |
| Q9 §11.5 fresh calibration; stream dependence | §2.5, §6.2, §8 |
| Q9 §11.6 failure paths, precedence, aggregation | §5.6, §7 |
| Q9 §11.7 T0 reduction against replication | §5.8 |

## 13. What this contract does not claim

Nothing about Regime II, Ψ, coherence, the margins hypothesis, within-cell heterogeneity, many streams per cell or onset continuity. No value marked PROPOSED or DERIVED is of record until the freeze commit names it. Held and not authorized here: Gemini commission v3.1; the two next-touch repairs (`test_f8_m6.py` docstring, `test_f8_mp1.py` comment); the third-order lattice-versus-ODE comparison; onset continuity; the PD7-versus-floor correspondence. Overview v1.8.2, held when this contract was begun, was registered by Mike at `47272f2` on 2026-11-14 and is no longer held. Mike rules; L2 reviews; Gemini audits for consistency only.

## Appendix A — provisional values (L1's container; scripts in `arith_v0_3/`)

**A.1 Arms at L = 100.**

| Terrain | Base range | λ^P range | spr_P | g_spec,P | λ^H range | H max/min | spr_H | g_spec,H | Base arrays SHA-256 (container, provisional) |
|---|---|---|---|---|---|---|---|---|---|
| T0 | 0.8 | 0.512 | 0.512000 | 0.354041 | 0.8 | 1.00 | 0.800000 | 0.226587 | `21babaa5c51d9630…` |
| TA | 0.300–0.900 | 0.0270–0.7290 | 0.701413 | 0.258435 | 0.3000–0.9000 | 3.00 | 0.880236 | 0.205933 | `5424742619823a0a…` |
| TB | 0.100–1.000 | 0.0258–0.1153 | 0.113406 | 1.598403 | 0.4200–0.5133 | 1.22 | 0.509168 | 0.356011 | `3f9df297c03093a4…` |
| TC | 0.050–0.900 | 0.0405–0.7290 | 0.728367 | 0.248871 | 0.6167–0.9000 | 1.46 | 0.899373 | 0.201551 | `49f16928ebffe303…` |
| TD-1-2 | 0.300–0.900 | 0.0270–0.7290 | 0.725886 | 0.249721 | 0.3000–0.9000 | 3.00 | 0.896516 | 0.202193 | `6a2b17e61ce2af99…` |
| TD-1-4 | 0.300–0.900 | 0.0270–0.7290 | 0.723752 | 0.250458 | 0.3000–0.9000 | 3.00 | 0.894862 | 0.202567 | `c3785ab6944377a5…` |
| TD-4-2 | 0.300–0.900 | 0.0270–0.7290 | 0.713340 | 0.254113 | 0.3000–0.9000 | 3.00 | 0.884323 | 0.204981 | `79e8778dfdcc9b94…` |
| TD-4-4 | 0.300–0.898 | 0.0270–0.7253 | 0.690069 | 0.262683 | 0.3000–0.8985 | 2.99 | 0.869999 | 0.208356 | `b695cc434cd929c0…` |

T0 is run under P only. TB's product x and y shares are 0.5173 and 0.4827.

**A.2 TB contour separation (global symmetric 0.95-quantile distance, cells; nearest contour of the other index's complete family).** P contour at its deciles 10…90: 31.6, 24.2, 20.5, 19.0, 18.0, 14.5, 14.3, 17.6, 24.6. H contour at its deciles: 24.7, 23.0, 21.0, 19.8, 18.7, 16.5, 14.0, 15.0, 16.6.

**A.3 Rule constants.** q = 0.181269; a = 0.01; π₁ = 0.052282; 1/q = 5.516656; floor-only probability of any activity in W ticks: 0.052282 (W = 1), 0.134244 (10), 0.649601 (100).

**A.4 T0 bracket at N = 10,000.** Lower term ln N/(q·2,000) = 0.0254; upper term (N·ρ*_sk ≥ 50, bisection on the Flight 8 map) = 0.0055; with the 0.05 spacing, 0.0754.

**A.5 Per-cell standard error of p̄, independent-chain approximation only (40 seeds × 1,000 ticks).** 0.0034 at p = 0.0523; 0.0045 at 0.1; 0.0056 at 0.2; 0.0059 at 0.3; 0.0053 at 0.5.

**A.6 Counts and intervals.** Runs as §8. Two-sided 95% Clopper–Pearson intervals at 40 seeds: 0/40 → [0, 0.088]; 20/40 → [0.338, 0.662]; 36/40 → [0.763, 0.972]; 40/40 → [0.912, 1]. One-sided 95% cap of 0.10 at 200 cases: at most 12 errors.

**A.7 Complete contour families and the prototype (synthetic maps only).** Family sizes on the comparison arrays of §3.4:

| Terrain | Family size P / H | One array for both? |
|---|---|---|
| TA | 1,300 / 1,300 | yes |
| TB | 2,600 / 50 | no |
| TC | 1,180 / 1,180 | yes |
| TD-1-2 | 681 / 681 | yes |
| TD-1-4 | 920 / 920 | yes |
| TD-4-2 | 250 / 250 | yes |
| TD-4-4 | 250 / 250 | yes |

v0.4 prototype (`f9_evaluator_proto_v4.py`, traced components), seconds per draw for both indices: TB 0.087; TA 0.110; TD-4-2 0.087. Under it: L2's round-1 missing island, S = 6.57; partial patch, S = 5.0; L2's round-2 displaced loop, components of 3,900 and 100 bonds and S = 10.0 (v0.3's convention gave 0); L2's TC translation, S = 2.0 and compatible under both P and H (v0.3 gave 2.0 and 2.236). A compatible map translated k cells along an axis has certified Δ* = k for k = 0…5 on TD-4-2, TD-1-2 and TC, and on TB under H along x (along y it stays 0, the H contours being lines of constant x). The v0.3 prototype's exactness checks (pruned against brute force on five terrains) are in `arith_v0_3/proto_checks.json`. Neither prototype is an instrument module.

**A.8 Closure-estimated levels with an edge (site closure; no lattice run; biased as §1.0 says).** On the 25-level grid with r = 0.3 on TB, of 25:

| Arm | θ = 0.10 | θ = 0.20 | θ = 0.30 |
|---|---|---|---|
| TA·P / TA·H | 25 / 14 | 24 / 23 | 18 / 18 |
| TB·P / **TB·H** | 23 / **0** | 24 / **5** | 18 / **6** |
| TC·P / **TC·H** | 25 / **1** | 23 / **7** | 17 / **9** |
| TD, four variants, P | 25 | 24 | 18 |
| TD, four variants, H | 14–15 | 23 | 18 |

As first drafted (15 levels, r = 0.8 on TB): TB·H 0 / 2 / 2 and TC·H 1 / 3 / 4 (`closure_windows.json`). The closure's map on TB·H spans about 0.048 in occupancy at r = 0.8.

**A.9 Scripts of this version (`arith_v0_3/`).** `f9_terrains.py` `ce2bd1e11b2d501c…`; `f9_contract_arith_v3.py` `0eddac8a843633e8…` → `contract_arith_v3.json` `2cff426249eddc43…`; `f9_evaluator_proto.py` `c940b7438d6a8db7…`; `proto_checks.py` `1613c4e82d27be4f…` → `proto_checks.json` `12cadfdc093969ea…`; `closure_windows.py` `0e6e41957df2233e…` → `closure_windows.json` `dd02bdb33ff06698…`; `closure_tb_options.py` `f313b8b13af505b9…` → `closure_tb_options.json` `9273214224ecb494…`. The two closure scripts record what informed the ruling and use the v0.2 grid and r. **Added in v0.4 (`arith_v0_4/`):** `f9_compare.py` `7fedb347cd40ba5f…`; `f9_evaluator_proto_v4.py` `dc934c2716a69caa…`; `proto_checks_v4.py` `19493bded8655227…` → `proto_checks_v4.json` `50f8618ee7076992…`; `strata_attainability.py` `e0850ee523a1c393…` → `strata_attainability.json` `004c29574878bab5…` (its timing fields are machine-dependent); `l2_appendix_r.py` `afe6b99f62afeefc…`, L2's round-2 counterexample program as extracted from its review. **Added in v0.5 (`arith_v0_5/`):** `fixture_checks_v5.py` `67dec110c277b9ca…` → `fixture_checks_v5.json` `4f82a08f534b4be8…`; `special_constructions_v5.py` `907cdc2c8102da32…` → `special_constructions_v5.json` `7cfcaaf5cbba1852…`; `l2_round3_checks.py` `963192fab92c1271…`, L2's round-3 Appendix R program as extracted from its review. The two v0.5 scripts import `f9_compare.py` and `f9_evaluator_proto_v4.py` from `arith_v0_4/`.

**A.10 Qualification fixtures and constructions (v0.5; synthetic maps at zero noise; `arith_v0_5/`).**

Strip fixture, island in the first gap at y₀ = 20, map 0.30 on the occupied set and 0.10 elsewhere, θ = 0.20:

| Island | Bonds | Share of contour perimeter | Island absent from the map | Island present in the map |
|---|---|---|---|---|
| 9 × 10 | 38 | 3.66% | S = 0; no component term (under m); compatible | S = 0; compatible |
| 9 × 11 | 40 | 3.85% | S = 6.569, from the island's component term; both global terms 0; adverse | S = 0.707; compatible |
| 9 × 12 | 42 | 4.03% | S = 6.519, the same way; adverse | S = 0.707; compatible |

The contour has ten strip sides of 100 bonds and the island; the island is 3.0 cells from the nearest strip side.

Arm constructions, on each of the eight comparison arrays (TA, TC, four TD, TB under P, TB under H): the untranslated generic sweep is informative and compatible at all 25 levels (arm COMPATIBLE); translated 3 cells along axis 0 it is informative and adverse at all 25 levels (arm ADVERSE); the low-information construction gives exactly two informative levels and NOT DISTINGUISHED at each of its 24 positions. A translation along axis 1 would not serve: on TB under H, whose contours are lines of constant x, it leaves every level compatible. On TB, a generic sweep of either index is compatible with its generating index and adverse against the other at all 25 levels, which is what the D rows rest on. Diagonal translations on TD-4-2: (1, 1) → 1.414; (2, 1) → 2.121; (2, 2) → 2.828; and (3, 0) → 3.0.

Registered-family scope: L2's TD-1-2 case reproduces (raw cut 0.30000000000000004, above the minimum by 5.6e-17; region 9,772 cells; 88 bonds; least S over the 681 registered contours 19.506, at ω = 0.300000000001).

These are support checks that the declared constructions can be built. Under calibration-derived noise, acceptance is by the certified truth of §6.0 and nothing here stands in for it.

*L1 (Claude Fable 5.2), v0.1 2026-11-12, v0.2, v0.3 and v0.4 2026-11-13, v0.5 2026-11-14.*
