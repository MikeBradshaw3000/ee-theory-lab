# Contract F9 — Flight 9: terrain and composition under the hazard rule (v0.3, DRAFT)

**v0.3, 2026-11-13 — supersedes v0.2 (`8dd4b4e6a5b161a7`, committed at `d7c8312`, retained).** Answers L2's round-1 contract review (`L2_F9_CONTRACT_V0_2_ROUND1_REVIEW_2026-11-13_RECEIVED.md`, `1473d63371701c06…`: **NOT YET FREEZABLE**, ten repairs R1–R10; Q1 and Q2 ACCEPTABLE) and the discussion that followed (L1's message, `L1_TO_L2_F9_CONTRACT_V0_2_DISCUSSION_2026-11-13.md`; L2's response, `L2_F9_CONTRACT_V0_2_DISCUSSION_RESPONSE_2026-11-13_RECEIVED.md`, `4cfcb442b7499b35…`), and records Mike's ruling of 2026-11-13 ("I rule affirmative to all") on L1's recommendations. L1 re-ran every counterexample in both L2 documents; all hold.

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

**Status.** L1 draft. **Not frozen.** Nothing here binds until Mike ratifies a version; no instrument, master, threshold, ensemble or run is produced under this document before that. Repository `main` at `d7c8312b7255b5bb4a927e1d97824d53ddaf056d` when written (fresh clone). Review path: L2 round 2 → Gemini corpus audit (commission v3) → Mike's ratification → freeze.
**Lineage.** Successor to Contract F8 v0.8.4 (`e87277a2d11e948f…`, frozen; stage 1 CLOSED, qualified, at `9d3a23b`). Governed by Design Note v0.3 (`8d82e319d79402f8…`), L2's design consultation (`65d95bc3a907cf04…`), the ratified pre-probe declaration v1.0 (`473a2a165fd5cb4e…`) and the probe record (`f3affc05de26f0d7…`). Nothing in `f8` or `e1` is modified.
**Markers.** `[RULED]` = Mike's ruling of record; `[PROPOSED]` = L1 value for Mike and L2, ratified only at freeze; `[DERIVED@FREEZE]` = computed by a declared procedure from closed-form inputs before freeze; `[DERIVED@BUILD]` = computed by the built instrument before the master it precedes is drawn, committed with its identity. Where Mike has ruled a structure and its number still goes to L2, the structure is RULED and the number PROPOSED.
**Notation.** Contract F8 names carry; the notation-scope table governs. **At first use: μ here is the deactivation rate (the Overview's lapse rate β), not the Overview's μ(ρ).** g is the feedback gain; η_floor the spontaneous floor as a per-tick hazard, committed value η₀ = −ln(0.99); λ_i per-cell conduciveness; d_i the Moore active fraction; q = 1 − e^(−μΔt). Bases are v, u, r. New here: κ (§2.8); P and H (§2.2); θ, ε, m, S and Δ (§5.5). The Annex is not cited.
**Numbers.** Every number new to this version was written from the scripts in `arith_v0_3/` (committed with this version; identities in Appendix A.9), run in L1's container (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1) on terrain arrays, the Moore adjacency, closed-form constants, the site closure and synthetic maps. Array hashes are container values and provisional (§3.4).

---

## 1. Object and claim grammar

**1.0 Provenance (dated record).** The claim grammar was fixed in the pre-probe declaration §1, ratified by Mike on 2026-11-12 before any Flight 9 lattice output existed. A noncanonical probe then ran once (896 runs, 4 seeds, master 9920261112, retired). Stated here so that no reader infers otherwise:
- **Selection.** L = 100, the finer κ grid, the retention of T0, TA and TC and the respecification of TB were decided with probe output known. Inference on these terrains is conditional on that selection.
- **Known before this contract.** At 4 seeds the skeleton was extinct at κ ≤ 1.25 and survived at κ ≥ 1.75 on every probed arm. On TC the inside-to-outside occupancy ratio was 0.26–0.34 under P and 0.68–0.73 under H for κ from 1.25 to 2.00. Neither the persistence diagnostic nor TC's suppression contrast (§1.3) is independent of the probe.
- **Not seen.** L1 has rendered no occupancy map from probe output, computed nothing from probe output against λ contours and extracted no edge from it. The array files have not been opened. L1 has seen the probe report's occupancy percentiles (R-3), map correlations (R-4), the TB x-only variance fraction (R-5) and the TC ratio (R-6).
- **θ's standing (L2 round 1, Q2: acceptable as disclosed).** θ = 0.20 is a post-probe design choice, frozen before fresh canonical observations. It is not a blind prediction. "Probe output enters no gate" means probe observations are not reused as scoring or calibration data; it does not mean the probe supplied no design information. Canonical inference is conditional on the disclosed selection; every registered sensitivity result is published; changing θ later is a new instrument.
- **Closure estimates computed for this version.** L1 iterated the site closure of §4.2 on the contract terrains and counted, per arm and level, whether the closure's map has an edge at θ (Appendix A.8). No lattice was run and no probe output was read. The closure is a mean-field object with a known bias: on T0 it gives occupancy 0.199 at κ = 1.0 where the probe's flat arm measured 0.168. These estimates led to three rulings (grid step, r on TB, seeds). They are design information of the feasibility kind, disclosed as such. No closure map was compared with any λ contour.
- **Never run:** the respecified TB (now with r = 0.3) and all four TD variants.
- **Errors of L1's recorded in this register:** the probe record's statement that TC "gives the two rules different spatial output" (it was a difference of amplitude; §3.3); a wrong count in a recommendation Mike ruled on (v0.2 header); the coupling claim for the skeleton diagnostic (R6); a missing-component claim the statistic did not support (R2); a cost objection made without measuring the cost (R3).
- Probe observations enter no gate, tolerance, calibration or qualification, and never become canonical observations.

**1.1 The object.** On a lattice whose bases differ from cell to cell and are frozen in time, with one action stream per cell, coupled only through local reinforcement of registration: (i) whether the two prescribed compositions give spatial output that can be told apart at declared resolution, and (ii) whether, under each prescribed composition, an observed boundary defined without reference to λ can be represented by a level set of that composition's local λ.

**1.1′ What the finite instrument can claim.** One lattice size (N = 10,000), one horizon, a 40-seed dynamics panel on deterministic terrains, a declared spatial resolution. Forty seeds on a fixed terrain are not forty terrains. Results hold for the declared rule, terrain, object, size, horizon and resolution. No lattice result selects which composition describes entrepreneurial ecosystems. `F_LR` and `F_2_symmetric` are untested; a product-against-mean contrast does not select multiplication among zero-collapsing functions. One lattice size is not a scaling study.

**1.2 Endpoints (two results, each with its own record; no headline word is derived from them `[RULED]`).**

- **B, conditional boundary compatibility — the scored substantive endpoint `[RULED]`.** For each composition X and each required terrain (§3.3), in the realization: the operational occupancy boundary of §5.5 is, or is not, within the permitted discrepancy ε of some level set of λ^X, under the joint discrepancy of §5.5 over the complete contour family. A pass is geometric compatibility within the declared scope. A valid failure says that no level set of that index represents the boundary at that resolution, for that rule, terrain, object, size and horizon.
- **D, conditional discrimination `[RULED]`.** On the terrain designated for it (TB), each arm's boundary is compared with both contour families. D is DISTINGUISHED under the rule of §5.6. A pass establishes a distinguishable output consequence of changing the composition in the instrument and nothing about which composition describes ecosystems. A non-pass can mean an uninformative terrain, insufficient resolution or indistinguishable output.

**1.2″ The bridge from PD7 to the observed boundary (instrument-level) `[RULED]`.** PD7 commits the activation surface Λ = Λ*. This contract operationalizes "an observed boundary" as the **operational occupancy boundary**: the edge of the region where the spatially averaged seed-mean occupancy of the realization is at least a fixed θ (§5.5). It is an instrument object. It is not the skeleton's persistence threshold, and on a smooth terrain it need not mark any abrupt change. The bridge is this contract's declaration, not a commitment of the theory.

**1.2′ Fidelity tier (pre-registered in full; reported with uncertainty in every record, favorable or not; never scored).** (i) Skeleton finite-horizon persistence threshold κ̂_c per arm against the spectral crossing κ = 1, as normalized and raw-g shifts; against T0's own κ̂_c. (ii) Local m_i = g·λ_i·Δt/q on the observed edge, against 1 (a local homogeneous benchmark) and against κ̂_c,T0; neither is a pointwise prediction. (iii) Seed-mean occupancy against the site closure's fixed-point probabilities (§4.2), matched in object and floor; where edges are compared, the §5.5 rule is applied to both maps. The lattice map is a finite-tail mean and the closure a fixed point, so their difference includes finite-time effects and is not an isolated stationary closure error. (iv) The fitted level λ*_X of §5.5 at each level. Uncertainty recipes are in §5.7. A poor comparison is published as such and never becomes a scored failure.

**1.3 Reported only (mandatory reporting items; never scored, never tested; none enters B or D).**
- **(a) Skeleton persistence diagnostic `[RULED 2026-11-13]`.** For every terrain arm, in the skeleton (η_floor = 0, all cells active at t = 0): the surviving seeds s of 40 at each of the 25 levels, each with a two-sided 95% Clopper–Pearson interval for the survival probability (pointwise; not a simultaneous band and not an interval for κ̂_c); κ̂_c (§5.4) and its grid bracket, named as panel summaries; and which description holds, with this precedence: non-monotone survival (some level with s ≥ 36 lies below a level with s < 36); survival at every level; survival at none; both phases inside the sweep. A stable upper stretch does not erase an earlier non-monotonicity. **It makes no claim about coupling.** Independent cells with a fixed activation hazard can also cross a finite-horizon survival criterion, so a persistence profile does not exclude them.
- **(b) Whole-map contour constancy, with a noise reference `[RULED 2026-11-13]`.** Defined in §5.7. The uncoupled independent-response alternative says occupancy is a function of local λ alone. Variation of occupancy within contours beyond sampling noise is evidence against that alternative; its absence is not evidence for it. Reported with its interval; no pass mark.
- **(c) The flicker record** of §2.11.
- **(d) Margin summaries**, design side (§3.2) and measured side (§5.7).
- **(e) TC's suppression contrast:** mean occupancy over cells inside the patch (bump ≥ 0.5) and outside it (bump ≤ 0.05), and their ratio, per arm and level; the sets are those of the pre-probe declaration (R-6).
- **(f) The evaluator's full output at θ = 0.10 and θ = 0.30.** These never replace or rescue the scored result.
- **(g) The skeleton's boundary** under the §5.5 rule, on the unconditional seed-mean map of all 40 seeds (extinct runs contribute zeros), where that map has an edge.
- **(h) Component coverage:** for every scored level, the number of components on each side, how many are resolved, and each one's 95th-percentile distance.

**1.4 What no result here may be represented as.** A confirmation or refutation of the theory (candidates produce or fail to produce). A selection of the true composition. Evidence of collective reinforcement from D or B: an uncoupled independent-response process passes both, and Flight 9 has no scored coupling-sensitive contrast. A statement about which side of a boundary is occupied, that occupancy increases with λ, or that occupancy is a function of λ alone: the edges are unoriented, and "follows own" means geometric compatibility only. A one-to-one matching of components or preserved topology: a narrow bridge or a small hole can be indistinguishable at ε. Evidence for literal zero-collapse: TC is near-face feedback suppression, the floor does not depend on the bases, and at exactly λ = 0 a realization cell has stationary occupancy 0.0523. A statement about Regime II, Ψ, coherence or the margins hypothesis. A resolution of onset continuity. A reopening of any Flight 8 or E1 verdict.

**1.5 Assumptions, and how each is tested `[RULED in principle 2026-11-13; entries PROPOSED]`.** Each test is declared here before its data exist, runs on its own master where it uses lattice data, is never scored, and has a consequence fixed in advance.

| # | Assumed | Basis now | Test | Consequence declared in advance |
|---|---|---|---|---|
| A1 | Every required arm has at least 3 levels with an edge at θ | closure estimate: 23–24 of 25 for twelve arms, 7 for TC·H, 5 for TB·H (A.8) | `calibration_census`: count of informative levels per arm at θ (edge existence only; nothing is compared with a contour) | reported; if any required arm has fewer than 3, the stage stops before any canonical census and a new instrument version is declared |
| A2 | Per-cell sampling error is small | independent-chain approximation: 0.003–0.006 at 40 seeds (A.5) | `calibration_census` measures it | ceiling 0.02 with the same stop path (§7) |
| A3 | Edge position is stable enough to resolve at ε on low-contrast arms | rough estimate only: about 1.3 cells of wander on TB·H | qualification with calibration-derived noise (§6.2); in canonical scoring a failure of this is "unresolved", never a pass | none beyond the declared outcome |
| A4 | Scoring against the complete contour family is affordable | prototype: 0.05–0.21 s per draw for both indices (A.7) | `resource_benchmark` on the canonical machine, evaluator included | if unaffordable, a new instrument version with a registered sub-family and both endpoints' adverse statements narrowed to it, before any canonical scoring |
| A5 | m = 40 protects resolved features without calling noise a component | none beyond its match to the informative-level minimum | qualification strata at component sizes 38, 40 and 42 bonds, both error directions (§6.2) | a failed qualification closes the stage |
| A6 | The 3×3 mean does not manufacture or erase the features scored | six symmetric disc checks only | deterministic known-answer cases (§6.1 classes 12–16) | implementation corpus must pass |
| A7 | The 950-of-1,000 rule behaves at its nominal level | none | qualification of the complete procedure (§6.2) | a failed qualification closes the stage |
| A8 | Occupancy depends on more than local λ | none; this is what distinguishes the coupled rule from the uncoupled alternative | contour-constancy report with noise reference (§1.3 b) | reported only |
| A9 | Terrain arrays agree across platforms to 1e-12 | container values | canonical build (§3.4) | canonical arrays and masks are the identities of record |

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
- **TB.** The product is r·(s(x)² − d(y)²), exactly additive in x and y. Criterion `[RULED]`: the product's x-share of across-cell variance lies in [0.40, 0.60]. Measured: **0.5173 along x, 0.4827 along y**; r scales the product uniformly and does not change the shares. The height index (2s + r)/3 varies along x only. **r = 0.3 `[RULED 2026-11-13, replacing 0.8 of 2026-11-12]`** raises the height index's max/min from 1.16 to **1.22**. Reason: under the closure estimate the H arm had an edge at θ at only 2 of 15 levels as first ruled; with r = 0.3 and the halved step it has 5 of 25 (A.8). TB·H remains the weakest arm. If it does not yield three informative levels, that arm is NOT DISTINGUISHED and with it D and B for composition H.
- **TD `[RULED]`.** The core C is a fixed set of cells given in closed form, with no reference to λ, g or either composition: the union of n equal discs centred on cell corners, **|C| = 2,000 cells exactly** in every variant. n = 1: centre (49.5, 49.5), R = 25.3 cells. n = 4: centres (24.5 or 74.5, 24.5 or 74.5), R = 12.65 cells. No cell centre lies within 0.03 cells of the edge. Four variants, n ∈ {1, 4} × w ∈ {2, 4} cells:

| Variant | Lattice perimeter of C | Band cells (10–90% of the base step) | Band / core | Largest base step per cell |
|---|---|---|---|---|
| TD-1-2 | 200 | 676 | 0.338 | 0.146 |
| TD-1-4 | 200 | 1,376 | 0.688 | 0.074 |
| TD-4-2 | 416 | 1,424 | 0.712 | 0.143 |
| TD-4-4 | 416 | 2,816 | 1.408 | 0.074 |

  Each disc of the four-disc core has 104 edge bonds. No criterion, threshold, evaluator branch or stopping rule refers to the margins hypothesis `[RULED, H2]`.

**3.3 Terrain roles `[RULED]`.** Two indices have the same contour family when each is an increasing function of the other. That holds by formula on TA and TD (P = t³, H = t) and on TC (P = 0.81·u, H = (1.8 + u)/3). Checked on the arrays: on those terrains no pair of cells is ordered oppositely by the two indices beyond 4e-16; on TB cells are ordered oppositely by as much as 0.088. Roles are declared by formula. After the tie rule of §3.4 the two quantized families on a same-family terrain can differ in a few members deep in a saturated plateau (for example 1,179 against 1,164 on TC); that is rounding, not geometry.

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
3. **Tie rule.** Every index array is rounded to 12 decimal places before any ranking or thresholding. A level set is {λ ≥ ℓ} on the rounded array.
4. **At build, before any master is drawn:** the canonical machine builds the base arrays, the rounded index arrays, the complete contour family of each (§5.5 step 5) and the spectral values, and commits their identities. These canonical objects are the ones every later job uses and binds.
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

**5.4 Skeleton survival.** survival = active count > 0 at every tail tick. κ̂_c = the lowest level with s ≥ 36 of 40 such that every higher level also has s ≥ 36 `[PROPOSED: Flight 8's 18 of 20 at the same proportion]`. Its bracket is the highest level with s < 36 and κ̂_c; that is grid resolution, not sampling uncertainty.

**5.5 N-E — the composition evaluator (complete algorithm).** Applied to each realization arm at each level, for each index Y ∈ {P, H}. The order is binding: occupancy estimate, occupancy criterion, edge, comparison. λ, g, κ and the terrain enter nowhere in steps 1–4.

1. **Occupancy estimate `[RULED]`.** p̄_i = mean over the 40 seeds of A_i(W = 1)/1,000. p̃ = the 3×3 periodic box mean of p̄. **The population target** is the edge, at θ, of the 3×3-averaged population-mean finite-tail occupancy on this fixed terrain, object and horizon. It is not the mean of per-seed discrepancies and says nothing about a typical seed's edge.
2. **Occupancy criterion `[structure RULED; value PROPOSED]`.** The operational occupied region is R = {i : p̃_i ≥ θ}, ties included, **θ = 0.20** for every arm, terrain and level (an excess of 0.148 over the floor reference).
3. **Edge and components `[RULED; conventions PROPOSED]`.** E = the set of unit boundary segments between a cell of R and a 4-neighbour outside R, with periodic wrapping, each represented by its midpoint ("bond"). Every bond has equal weight. **Every component is included**, where a component is defined on the post-estimator region R: the set of bonds lying between one 4-connected component of R and one 8-connected component of its complement. Two cells of R touching only at a corner are separate components; a hole has its own component. The 3×3 mean can remove a one-cell-wide feature or fill a one-cell-wide gap before this step; that is a property of the declared estimator and is tested as such (§6.1).
4. **Informative level `[RULED; counts PROPOSED]`.** R and its complement each have at least 100 cells, and E has at least 40 bonds. An empty or full R is `no edge at θ`. These are resolution declarations; they are not 100 independent observations.
5. **The contour family `[RULED 2026-11-13: complete family]`.** For index Y, on the rounded array of §3.4: the family 𝒞_Y is every set {λ^Y ≥ ℓ} for ℓ a distinct value of the array other than its minimum. Each is non-empty and proper by construction, no two are equal, and the family is every level set the index has on this lattice. The contour C(ℓ) is that set's edge with its components, by step 3. Sizes: 50 (TB under H) to 2,600 (TB under P) (A.7). A constant index has an empty family: `no eligible contour`, an unavailable state distinct from an absent observed edge.
6. **Joint discrepancy `[RULED 2026-11-13; m PROPOSED]`.** With d(·,·) the Euclidean distance on the torus between bond midpoints, Q₀.₉₅ the 0.95 quantile with linear interpolation between order statistics, and K_m(·) the components with at least **m = 40 bonds**:

   S(E, C) = max{ Q₀.₉₅ of d(e, C) over e ∈ E; Q₀.₉₅ of d(c, E) over c ∈ C; for every K ∈ K_m(E), Q₀.₉₅ of d(e, C) over e ∈ K; for every H ∈ K_m(C), Q₀.₉₅ of d(c, E) over c ∈ H }.

   Distances are to the whole opposite edge set. If a side has no resolved component, that side adds no term, and the record says no resolved component was checked there. Components under m bonds stay in E or C, in the two global terms and in the record; they are not erased, merged or down-weighted. The claim this supports: **every resolved component receives its own geometric check.** It does not support "a missing component of any size cannot be overlooked". m = 40 equals the informative-level bond minimum: a component is resolved when it could stand as an edge by itself. Each TD disc (104 bonds) is resolved.
7. **Fit, and the exact decision `[RULED]`.** Δ_Y = min over C ∈ 𝒞_Y of S(E, C). **One contour must satisfy the whole of S.** The decision uses only whether Δ_Y ≤ ε. An implementation may skip any contour that cannot satisfy the first term: a bond of C within ε of a bond e has both its cells within ε + 0.5 of e, so ℓ lies between the least and greatest index value over those cells; a level outside that interval for more than the allowed share of E has S > ε. This pruning is exact for the decision, and the build must show, on the known-answer corpus, that pruned and unpruned decisions agree in every case. The fitted level λ*_Y is the minimizing ℓ (the lowest if several tie), reported when Δ_Y ≤ ε; otherwise the record says "no contour within ε" and reports the least S among the contours examined, labelled as a lower-effort descriptive value. λ* is fidelity; its location is never scored.
8. **Permitted discrepancy `[structure RULED; value PROPOSED]`.** **ε = 2.0 cells.** It controls how far, in lattice cells, the operational occupancy boundary and each of its resolved components may lie from a level set and still be called represented by it. One cell is the interaction range and a bond midpoint lies half a cell from either cell centre; two cells is that resolution with a margin. This is a design convention, not a bound on the estimator's error; the qualification prices the complete procedure around it. A different ε is a different instrument. ε is never enlarged because precision is poor.
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
| Contour constancy with noise reference (§1.3 b) | On the **unsmoothed** p̄. Cells are ranked by the rounded λ^X and cut into 100 bins of 100 cells, a bin boundary moving up to the next distinct value so tied cells stay together. V_within = the cell-weighted mean of within-bin variance of p̄. V_noise = the mean over cells of (variance of the per-seed occupancy across the 40 seeds)/40. Reported: V_within, V_noise, their ratio, and the 2.5–97.5 percentile range of the ratio over 1,000 seed resamples. A bin of one distinct λ value under an occupancy that is a function of λ alone has expected ratio 1; bins wider than one value add the spread of that function, so the ratio is read beside the bin widths, which are reported. Zero total variance: "undefined". |
| Measured margins (§1.3 d) | On p̃ at W = 1. Core = cells with p̃ ≥ 0.30; band = cells with 0.10 ≤ p̃ < 0.30. Reported: both counts and band/core; "undefined" if the core is empty. Also the counts at the cut 0.20. Beside each, the floor reference 0.0523. |
| Flicker distributions (§1.3 c) | Cells are placed in occupancy bands [0, 0.10), [0.10, 0.20), [0.20, 0.30), [0.30, 1] by p̄. Per band and W: the median and quartiles of the statistic over all (cell, seed) records with a defined value, and the counts of undefined and of possibly censored records. |
| Fidelity uncertainties (§1.2′) | Occupancy-based items: 2.5–97.5 percentile range over 1,000 seed resamples. κ̂_c: its grid bracket, named as resolution, with the Clopper–Pearson intervals of the bracketing levels. λ*: its range over the valid resamples. |
| Skeleton boundary (§1.3 g) | Unconditional seed-mean map over all 40 seeds; an extinct run contributes its recorded tail, zeros after extinction. |
| Component coverage (§1.3 h) | As stated there. |

**5.8 T0 `[RULED; values PROPOSED]`.** (i) The reduction of §5.1 is the apparatus check. (ii) Flight 8's four tests are rerun on T0 as a scientific consistency exercise, redeclared as follows. Sweeps: skeleton-high, skeleton-low (ρ₀ = 0.02) and realization on the §2.9 grid. Survival threshold 36 of 40. **Hysteresis bracket** Δκ = max(0.0254, 0.0055) + 0.05 = **0.0754** (Contract F8 §3.4's procedure at N = 10,000 with the fine-grid spacing; A.4). It applies only if, for each of the two skeleton boundaries, the level just below the boundary and the boundary level are both in the fine grid and 0.05 apart; a boundary at κ = 1.00 does not qualify because the level below it is 0.75. Otherwise the hysteresis test is unevaluable, cause `bracket outside fine grid`, and the other tests stand. **Continuity criterion:** for adjacent levels j, j+1 above the boundary, J_j = 0.10·(med_{j+1} − med_j)/(κ_{j+1} − κ_j); an excess of J_j over f_J = 0.25 of the branch's sampled range returns NOT DISTINGUISHED. This is a slope criterion on a non-uniform grid, at Flight 8's scale of roughly one tenth of κ. **Evaluability band:** 3·√(ŝ_X(κ₋)² + ŝ_X(κ₊)²)·1.2533/√40, ŝ_X the calibration census's seed-to-seed standard deviation of tail density for the sweep's own object. T0's record is PRODUCED, NOT PRODUCED or NOT DISTINGUISHED for T0 alone. It gates no endpoint, an adverse or ND result there is not automatically a coding defect, and it does not resolve onset continuity. If κ̂_c,T0 is unavailable, every T0-referenced fidelity item is recorded "reference unavailable".

**5.9 N7 — records, package, readiness.** The principles of Contract F8 §4.10 carry: completeness against readiness computed separately; valid adverse records; apparatus and qualification prerequisites require passage, scientific prerequisites valid completion; identity and authorization binding. The record graph is Flight 9's own (§8). Every record binds what exists when it is written: terrain and family identities, composition, g, κ, g_spec and spr, lattice geometry, object and floor, horizon and tail, seed and stream identity, window convention, summary schema, θ, ε and m, evaluator identity, and the **qualification protocol identity**. Only records written after qualification bind the **qualification result identity**. No record is required to cite an identity that does not yet exist.

## 6. Qualification of the evaluator (before any canonical scoring) `[RULED in structure; contents and sizes PROPOSED]`

**6.1 Known-answer corpus (implementation).** Every class returns exactly its named record and cause on ≥ 95 of 100; **cross-trigger rule**: the right record with the wrong cause fails. The expected answer of every class is certified independently of the evaluator, for the complete post-estimator target: the true Δ is computed by brute force over the complete family on the noise-free smoothed map. A deterministic class has one case and must be exact. h(z) = 0.06 + 0.40·z with z the index scaled to [0, 1] on its terrain `[PROPOSED]`.

| # | Class | Expected |
|---|---|---|
| 1 | p = h(λ^P) on TB, scored as the P arm | own compatible; rival adverse |
| 2 | the same maps scored as the H arm | own adverse; rival compatible (follows rival) |
| 3 | p = h(λ^H) on TB, scored both ways | as 1 and 2 with indices exchanged |
| 4 | p = h of the TB product with x and y exchanged by the periodic map (x, y) → (x + y, y − x) | adverse against both families (truth certified > ε for each) |
| 5 | p = h(λ) on TA | own compatible; not adjudicable here |
| 6 | a map everywhere below θ; one everywhere above | `no edge at θ` |
| 7 | a region of 50 cells | `under-resolved` |
| 8 | an edge with certified true Δ ≤ 1.0 against the complete family; one with certified true Δ ≥ 3.0 | compatible; adverse |
| 9 | the TD four-disc pattern with one disc absent | adverse |
| 10 | L2's five strips with a 10×10 island in the contour and not in the map | adverse (S = 6.57 by the prototype) |
| 11 | L2's patch that has lost a quarter of its area | adverse (S = 5.0 by the prototype) |
| 12 | a one-cell-wide stripe at 0.30 on 0.05 | the stripe is absent after the estimator; record per the remaining map |
| 13 | a one-cell-wide gap at 0.05 in a 0.30 region | the gap is filled after the estimator |
| 14 | a three-cell-wide channel; a 3×3 hole; an asymmetric profile across an edge; a plateau within 0.005 of θ | each as certified on the post-estimator map |
| 15 | two blocks touching at a corner; a block with a hole | two components each, of the certified sizes |
| 16 | components of 38, 40 and 42 bonds absent from the map | 38: not checked as a component; 40 and 42: adverse |
| 17 | a constant index | `no eligible contour` |
| 18 | resample sets built to give exactly 50 and exactly 51 invalid draws; 950/0/50, 949/1/50, 0/950/50 | compatible or per the table of §5.5 step 9; 51 → `unstable edge` |
| 19 | whole synthetic sweeps exercising each arm rule, including exactly two informative adjacent adverse levels | ADVERSE in that case; each other as certified |
| 20 | pruned against unpruned decision on every case above | identical |

Classes that need calibration-derived noise are run after the calibration record (§8); the deterministic classes are run before it.

**6.2 Statistical qualification (design and held-out ensembles).**

*Generator declaration (frozen at freeze; numerical parameters derived at build by the fixed transformations below).* A case is 40 seed maps. Each seed map is h(index) + noise, clipped to [0, 1]. h is drawn from a declared family (the affine h of §6.1 with slope in [0.2, 0.6] and offset in [0.03, 0.10]). The noise is a stationary Gaussian array with per-cell standard deviation σ_seed and a separable exponential correlation of length ℓ_c. **Transformations, fixed before any calibration output exists:** σ_seed(p) = the calibration census's median, over cells with seed-mean occupancy within 0.02 of p, of the across-seed standard deviation of per-seed occupancy; ℓ_c = the lag at which the calibration census's mean spatial autocorrelation of per-seed residuals first falls below 1/e. The standard error of a mean map is σ_seed/√40 and is never used in place of σ_seed.

*Error table (every capped stratum has 200 independent cases in each ensemble; cap 0.10 by one-sided 95% Clopper–Pearson upper bound, at most 12 errors; halts and wrong causes count as errors; each cap is per stratum, not simultaneous).*

| Stratum | Decision unit | Certified truth | Output counted as error |
|---|---|---|---|
| Near ε, Δ* = 1.0 | level | Δ* of the population target, by brute force | adverse |
| Near ε, Δ* = 1.5 | level | as above | adverse |
| Near ε, Δ* = 2.0 | level | as above | adverse |
| Near ε, Δ* = 2.5 | level | as above | compatible |
| Near ε, Δ* = 3.0 | level | as above | compatible |
| Sensitivity, safely compatible (Δ* ≤ 1.0, informative, calibration noise) | level | as above | adverse **or unresolved** |
| Sensitivity, safely adverse (Δ* ≥ 3.0, informative, calibration noise) | level | as above | compatible **or unresolved** |
| False identification: rival-generated maps on TB | level | own Δ* > 3.0, rival Δ* ≤ 1.0 | "follows own" |
| False compatibility: neither-family maps (class 4 generator) | level | both Δ* > 3.0 | compatible for either index |
| Vacuous support: constant, saturated, empty-edge, single-contour maps | level | the named unavailable cause | any decisive record |
| Component sizes 38, 40, 42 bonds, present and absent | level | as certified | 40 and 42 absent: compatible; 38, 40, 42 present and matching: adverse |
| Arm, truly compatible sweep (25 levels, calibration noise, and at 1.5 times it) | arm | every informative level Δ* ≤ 1.0 | ADVERSE |
| Arm, truly adverse sweep | arm | every informative level Δ* ≥ 3.0 | COMPATIBLE |
| Flight B, seven truly compatible arms | flight | as the arms | NOT PRODUCED |
| Flight B, six compatible arms and one truly adverse | flight | as the arms | PRODUCED |
| Flight D, own-generated maps in both TB arms | flight | own Δ* ≤ 1.0, rival Δ* ≥ 3.0 | (reported: rate of DISTINGUISHED; capped: none) |
| Flight D, both TB arms generated from one index | flight | one arm follows rival | DISTINGUISHED |

Where an exact Δ* is not attainable on the raster, a predeclared stratum on the correct side with certified values is used and its values are recorded. Near ε an unresolved result is allowed and its rate is reported; a wrong decisive answer is capped. Unresolved is an error only in the two sensitivity strata. Design AND held-out are joined mechanically. A failed qualification closes the stage; no same-stage repair. Guarantees hold for the declared ensembles and decision units only; five distances do not bound the error at all distances, and nothing transfers automatically to the lattice.

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
| L7 | n_A ≥ 950 for the own index | scientific adverse at the level | `no level set of own index within ε` | own adverse at this level |

**Arm.** A1 apparatus at any level → no qualified determination. A2 two neighbouring informative levels own-adverse → ADVERSE. A3 at least 3 informative levels, all "follows own" → COMPATIBLE. A4 otherwise NOT DISTINGUISHED (`insufficient informative levels`; `isolated adverse level`; `finite resolution`).

**Flight.** As the tables of §5.6. A missing or corrupt mandatory input propagates as "no qualified scientific determination" to both B and D where it touches a required arm; it is a prerequisite failure, not a scientific ND.

**Other.** Skeleton run extinct: a valid observation, never "missing". Site closure not converged: `comparator unavailable`, fidelity only. κ̂_c,T0 unavailable: `reference unavailable`, fidelity only.

No failed terrain is dropped, no level is selected after the fact, no role is changed, and every state is preserved. A required arm that lacks information does not disappear: it is NOT DISTINGUISHED and enters the conjunction as such. The contract does not predict that an occupied region exists at θ, so the wholesale absence of an edge is ND, not adverse. An adverse record is never recast as fidelity or ND at its own tier. **Stop paths `[PROPOSED]`:** if the calibration census shows a median per-cell standard error of p̃ above 0.02 at any arm and level, or fewer than 3 informative levels at θ for any required arm (§1.5 A1, A2), the stage stops before any canonical census and a new instrument version is declared; the sample size, grid and θ of this stage are never changed after data exist.

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
| 7 | draw design master; `evaluator_design_audit` | qualification | 6 | design record | stage closes |
| 8 | draw held-out master; `evaluator_held_out_audit` | qualification | 7 (C) | held-out record | stage closes |
| 9 | `evaluator_qualification` | qualification | 7, 8 | **qualification result identity** | stage closes |
| 10 | `resource_benchmark` | apparatus | 1 | cost of dynamics, evaluator and qualification on the canonical machine | §1.5 A4 |
| 11 | draw canonical master; `t0_census` | scientific (consistency) | 9 (P) | T0 record; κ̂_c,T0 | recorded |
| 12 | `skeleton_census` | scientific | 9 (P) | persistence diagnostic; κ̂_c | recorded |
| 13 | `realization_census` | scientific | 9 (P) | level, arm and flight records for B and D | recorded |
| 14 | draw stability master; `census_stability` | scientific | 12, 13 (C) | arm records reproduced or not, reported | recorded |
| 15 | `fidelity_report`, `persistence_report`, `constancy_report`, `flicker_report`, `margin_report`, `component_report` | reporting | 11–13 (C) | §1.2′, §1.3, §5.7 | incomplete reporting |
| 16 | `stage1_package` | package | all | completeness and readiness, computed separately | — |

Arms: T0·P, and P and H on each of TA, TB, TC, TD-1-2, TD-1-4, TD-4-2, TD-4-4 (15). Runs: calibration 30,000; T0 3,000; skeleton 14,000; realization 14,000; stability 28,000; **89,000 in all**, about 19.5 hours at the container's probe speed (0.96 s per realization run, 0.62 s per skeleton run at L = 100). The evaluator is extra: at the prototype's 0.05–0.21 s per draw, 1,000 draws at each of 350 arm-levels is 5 to 20 hours per θ per panel before any optimization. The canonical machine is unmeasured; step 10 prices it, and if the complete paired design proves too expensive the claimed scope is reduced prospectively with paired comparisons kept on what remains. Instrument version string `f9_stage1_v1` `[PROPOSED]`.

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
| Edge; components | 4-neighbour bonds, periodic; every component of the post-estimator region; 4-connected region, 8-connected complement | RULED; convention PROPOSED |
| Informative level | ≥ 100 cells each side; ≥ 40 bonds | RULED; counts PROPOSED |
| Contour family | complete: every distinct proper level set of the rounded index | RULED 2026-11-13 |
| Discrepancy | joint S; Euclidean torus distance; linear-interpolated 0.95 quantile; m = 40 bonds | RULED; m PROPOSED |
| Permitted discrepancy | ε = 2.0 cells | structure RULED; value PROPOSED |
| Uncertainty | 1,000 seed resamples; 950 supporting; over 50 invalid = unstable | RULED 2026-11-13 |
| Arm rule | two neighbouring adverse → ADVERSE; ≥ 3 informative all "follows own" → COMPATIBLE | RULED |
| Flight rule, B | conjunction over seven required arms per composition | RULED |
| D | TB; ≥ 3 witnessing levels per arm; no "follows rival" level in either arm | RULED 2026-11-13 |
| Headline word | none | RULED |
| Persistence diagnostic | 36 of 40; two-sided 95% Clopper–Pearson, pointwise; no coupling claim | RULED 2026-11-13 |
| Contour constancy | noise reference; reported only | RULED 2026-11-13 |
| TC suppression contrast | reported only | RULED |
| T0 exercise | bracket 0.0754 with fine-grid eligibility; f_J = 0.25 on J normalized to 0.10; ρ₀ = 0.02; gates nothing | RULED; values PROPOSED |
| Qualification | §6; 200 per stratum; cap 0.10; CP 95% one-sided | RULED in structure; contents PROPOSED |
| Stop paths | standard error ≤ 0.02; ≥ 3 informative levels per required arm in calibration | PROPOSED |
| Site closure solver | start p = 1 or π₁; 1e-12; 200,000 iterations | PROPOSED |
| Identities | §3.4; rounding to 12 places; 1e-12 cross-platform; canonical objects of record | PROPOSED |
| Margin cuts | 0.10, 0.20, 0.30 | RULED |
| Masters | drawn by stage (§8) | DERIVED@BUILD |
| Instrument version | `f9_stage1_v1` | PROPOSED |

## 10. Notation rows to append (append-only; the table governs)

| Object | O — Overview v1.8.1 | C — this contract | Nature |
|---|---|---|---|
| Spectral-relative gain | Λ/Λ* (implicit) | κ = g/g_spec,X; equals Flight 8's m on a flat terrain | C-only |
| Sweeping g against scaling Λ | the spontaneous term scales with Λ | the floor is fixed; g and λ enter only as g·λ_i | rule-specific equivalence |
| Observed boundary | activation surface Λ = Λ* (PD7) | operational occupancy boundary: edge of {p̃ ≥ θ} | instrument-level bridge, C-only |
| Permitted discrepancy; component resolution | — | ε in cells; m in bonds | C-only; declared resolutions |
| Compositions | F (open) | P = `F_canonical`, H = `F_baseline` (rival only) | prescribed inputs; no selection claimed |

## 11. Rulings of record, and what goes to L2 in round 2

**11.1 Mike's ruling, 2026-11-13: "I rule affirmative to all"**, given on the condition that L1 agreed the principle stated in this version's header, which L1 did. It covers L1's ten recommendations on the round-1 repairs, the three revisions L1 made under the principle (complete contour family; D blocked by a "follows rival" level; a noise reference on contour constancy), and the four closure-based recommendations (θ kept at 0.20; κ step halved; r = 0.3 on TB; 40 seeds).

**11.2 For Mike's acknowledgment (consequences of the ruling that he did not rule on by name).**
1. **Survival threshold 36 of 40**, the same proportion as 18 of 20.
2. **A second calibration stop path**: fewer than 3 informative levels for any required arm stops the stage before any canonical census (§1.5 A1).
3. **The T0 continuity criterion is normalized to an interval of 0.10** and the bracket to the 0.05 spacing (0.0754).
4. **The assumption register of §1.5** as the form in which the principle is written into the contract.
5. **The evaluator's cost**: 5 to 20 hours per θ per panel at prototype speed, beside 19.5 hours of dynamics.

**11.3 Open points for L2, round 2.**
1. The pruning argument of §5.5 step 7: is it exact as stated, including the interpolated quantile?
2. m = 40 and the strata 38, 40, 42 (L2 accepted the structure, not a number).
3. The component convention (4-connected region, 8-connected complement) as written.
4. The contour-constancy report as a quantity bearing on the uncoupled alternative: is the noise reference sound, and is the reading of the ratio stated carefully enough?
5. The calibration stop path on informative-level counts: does counting edges in calibration compromise the scored endpoint?
6. The error table of §6.2: decision units, truths and which outputs are errors.
7. The persistence diagnostic's description precedence and interval choice.
8. The identity procedure and tie rule of §3.4, given that rounding makes the two families on a same-family terrain differ in a few plateau members.
9. Whether anything in the three design changes (grid, r on TB, seeds), made on a closure estimate, damages the prospective standing of the claim grammar.

## 12. Trace of requirements

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

Nothing about Regime II, Ψ, coherence, the margins hypothesis, within-cell heterogeneity, many streams per cell or onset continuity. No value marked PROPOSED or DERIVED is of record until the freeze commit names it. Held and not authorized here: Gemini commission v3.1; the two next-touch repairs (`test_f8_m6.py` docstring, `test_f8_mp1.py` comment); the third-order lattice-versus-ODE comparison; Overview v1.8.2; onset continuity; the PD7-versus-floor correspondence. Mike rules; L2 reviews; Gemini audits for consistency only.

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

**A.7 Complete contour families and the prototype (synthetic maps only).**

| Terrain | Family size P / H | Prototype seconds per draw, both indices | Contours examined after pruning (own / rival, mean) | Pruned decision equals brute force |
|---|---|---|---|---|
| TA | 1,300 / 1,300 | 0.205 | 77 / 77 | yes |
| TB | 2,600 / 50 | 0.138 (P arm); 0.046 (H arm) | 131 / 0 (P arm); 4 / 0 (H arm) | yes |
| TC | 1,179 / 1,164 | 0.081 | 35 / 35 | yes |
| TD-1-2 | 650 / 681 | not timed | — | — |
| TD-1-4 | 919 / 920 | not timed | — | — |
| TD-4-2 | 250 / 250 | 0.124 | 32 / 32 | yes |
| TD-4-4 | 250 / 250 | not timed | — | — |

On the five timed cases the minimized S from the pruned search equals the brute-force minimum over the whole family (0.71, 1.0, 0.71, 0.0, 0.71). L2's two examples under the joint statistic: missing island, S = 6.57; partial patch, S = 5.0. The prototype is not an instrument module.

**A.8 Closure-estimated levels with an edge (site closure; no lattice run; biased as §1.0 says).** On the 25-level grid with r = 0.3 on TB, of 25:

| Arm | θ = 0.10 | θ = 0.20 | θ = 0.30 |
|---|---|---|---|
| TA·P / TA·H | 25 / 14 | 24 / 23 | 18 / 18 |
| TB·P / **TB·H** | 23 / **0** | 24 / **5** | 18 / **6** |
| TC·P / **TC·H** | 25 / **1** | 23 / **7** | 17 / **9** |
| TD, four variants, P | 25 | 24 | 18 |
| TD, four variants, H | 14–15 | 23 | 18 |

As first drafted (15 levels, r = 0.8 on TB): TB·H 0 / 2 / 2 and TC·H 1 / 3 / 4 (`closure_windows.json`). The closure's map on TB·H spans about 0.048 in occupancy at r = 0.8.

**A.9 Scripts of this version (`arith_v0_3/`).** `f9_terrains.py` `ce2bd1e11b2d501c…`; `f9_contract_arith_v3.py` `0eddac8a843633e8…` → `contract_arith_v3.json` `2cff426249eddc43…`; `f9_evaluator_proto.py` `c940b7438d6a8db7…`; `proto_checks.py` `1613c4e82d27be4f…` → `proto_checks.json` `12cadfdc093969ea…`; `closure_windows.py` `0e6e41957df2233e…` → `closure_windows.json` `dd02bdb33ff06698…`; `closure_tb_options.py` `f313b8b13af505b9…` → `closure_tb_options.json` `9273214224ecb494…`. The two closure scripts record what informed the ruling and use the v0.2 grid and r.

*L1 (Claude Fable 5.2), v0.1 2026-11-12, v0.2 and v0.3 2026-11-13.*
