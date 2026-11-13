# Contract F9 — Flight 9: terrain and composition under the hazard rule (v0.2, DRAFT)

**v0.2, 2026-11-13 — supersedes v0.1 (`5f08acf6dcae509d`, retained beside this file).** Records two acts of 2026-11-13 and changes nothing else. (i) Mike consulted L2 on v0.1's §11 questions outside a packet; L2 answered without the draft, the §11 wording or the probe record (`L2_F9_CONTRACT_QUESTIONS_ADVICE_2026-11-13_RECEIVED.md`, `a79dbb22de2a6fb0…`, a byte copy of the reply as Mike attached it). Mike then instructed L1: "Accept what you want of L2's advice and recommend on the others for my ruling." (ii) Mike ruled "i rule as recommended" on L1's seventeen recommendations. The changes:
- **The split is a fixed threshold.** v0.1 split each occupancy map by Otsu's criterion, which finds an edge on any map and gives "occupied" a different meaning on each. The observed boundary is now taken at a fixed occupancy θ declared here (§5.5). It is named the operational occupancy boundary.
- **Every component is included.** v0.1's reassignment of components under 25 cells is withdrawn. The 3×3 mean is kept as part of the declared occupancy estimator; this is L1's one departure from L2's advice and is put to L2 (§11).
- **One permitted discrepancy ε.** v0.1's two tolerances (2.0 and 4.0 cells) left a band in which a true discrepancy was neither accepted nor rejected, which mixed permitted discrepancy with measurement uncertainty. There is now a single ε, and the uncertainty bounds decide compatible, adverse or not distinguished around it (§5.5).
- **Conjunction over required cases.** v0.1's flight rule ("TB and at least four of six others") was a vote across terrains and is withdrawn. Every terrain has a declared role (§3.3) and the flight-level word is a conjunction over required cases (§5.6). No single headline word is derived.
- **The coupling contrast is a diagnostic.** v0.1's endpoint E-K becomes diagnostic K: mandatory, reported whatever it shows, never gating, with survival counts and the threshold bracket in place of a PRESENT/ABSENT word (§1.3).
- **TC's suppression contrast is reported only**, on the geometric sets of the pre-probe declaration. L2's advice left room for a separately scored contrast; L2 did not know the probe had already shown it.
- **Margin cuts are fixed occupancy values**, replacing fractions of each map's own range.
- Endpoint names follow L2: **B** (boundary compatibility) and **D** (discrimination).
- **A correction to the text Mike ruled on.** L1's recommendation 5 said "all 13 required arms". The count was wrong. There are seven required terrain arms per composition (TA, TB, TC and four TD), fourteen across the two compositions. The rule Mike ruled on is unchanged; the number is corrected here and listed for his acknowledgment (§11).

**Status.** L1 draft, at Mike's word ("contract"; step 2 of his instruction of 2026-11-12). **Not frozen. Not yet reviewed by L2 as a contract.** Nothing here binds until Mike ratifies a version; no instrument, master, threshold, ensemble or run is produced under this document before that. Repository `main` at `a7d3a5d7a4b1c3e46f24a44083f37a0aa50534e7` when written (fresh clone, 2026-11-12). Review path: L2 contract packet under its own register → Gemini corpus audit (commission v3) → Mike's ratification → freeze.
**Lineage.** Successor to Contract F8 v0.8.4 (`e87277a2d11e948f…`, frozen; stage 1 CLOSED, qualified, at `9d3a23b`). Governed by Design Note v0.3 (`8d82e319d79402f8…`), L2's design consultation (`65d95bc3a907cf04…`), the ratified pre-probe declaration v1.0 (`473a2a165fd5cb4e…`) and the probe record (`f3affc05de26f0d7…`). Flight 8 stays closed as recorded; nothing in `f8` or `e1` is modified.
**Markers.** `[RULED]` = Mike's ruling of record; `[PROPOSED]` = L1 value for Mike and L2, ratified only at freeze; `[DERIVED@FREEZE]` = computed by a declared procedure from closed-form inputs before freeze, tabulated in Appendix A and committed in the freeze commit; `[DERIVED@BUILD]` = computed by the built instrument before any canonical master is drawn, committed with its identity. Where Mike has ruled a structure and its number still goes to L2, the structure is RULED and the number PROPOSED.
**Notation.** Contract F8 names carry; the notation-scope table governs. **At first use: μ here is the deactivation rate (the Overview's lapse rate β), not the Overview's μ(ρ).** g is the feedback gain; η_floor the spontaneous floor as a per-tick hazard, committed value η₀ = −ln(0.99); λ_i per-cell conduciveness; d_i the Moore active fraction; q = 1 − e^(−μΔt). Bases are v, u, r. New here: κ, the spectral-relative gain (§2.8); P and H, the two compositions (§2.2); θ and ε (§5.5). Participation vocabulary per PD1–PD7. The Annex is not cited.
**Numbers.** Every number in this draft was written from a script (`f9_step1.py` `d195c94015d6a667…`, `td_final.py` `ca0076012b8bbc0e…`, `f9_contract_arith.py` `57ccd322431bb2a7…`, `smooth_check.py` `d36b325cb7937002…`; none committed yet), run in L1's container (Python 3.13.18, NumPy 2.5.3) on terrain arrays, the Moore adjacency and closed-form rule constants only. Array hashes are container identities and are provisional (§3.4).

---

## 1. Object and claim grammar

**1.0 Provenance (dated record).** The claim grammar of §1.2 was fixed in the pre-probe declaration §1, ratified by Mike on 2026-11-12 before any Flight 9 lattice output existed. A noncanonical probe then ran once (896 runs, 4 seeds, master 9920261112, retired). What it showed, and what was decided because of it, is in the probe record §3–§5. Stated here so that no reader infers otherwise:
- **Selection.** L = 100, the finer κ grid, the retention of T0, TA and TC and the respecification of TB were decided with probe output known. Inference on these terrains is conditional on that selection.
- **Known before this contract.** At 4 seeds the skeleton was extinct at κ ≤ 1.25 and survived at κ ≥ 1.75 on every probed arm. Diagnostic K (§1.3) therefore cannot be represented as independent of the probe. On TC the inside-to-outside occupancy ratio was 0.26–0.34 under P and 0.68–0.73 under H for κ from 1.25 to 2.00; TC's suppression contrast (§1.3) is likewise not independent of the probe.
- **Not seen.** L1 has rendered no occupancy map, computed nothing against λ contours and extracted no edge from probe output. The array files have not been opened for this draft. L1 has seen the probe report's across-cell occupancy percentiles (R-3), map correlations (R-4), the TB x-only variance fraction (R-5) and the TC inside/outside ratio (R-6).
- **The threshold θ was not chosen blind.** A fixed occupancy threshold determines which levels have an edge at all, and L1 knew R-3's percentiles when proposing θ = 0.20. The pre-probe declaration permits the probe to inform whether levels are informative and forbids choosing an edge rule because it improves a result. L1's statement is that θ was chosen as a round value inside the occupancy range and not to place any edge; L2 is asked to test that (§11). ε, the distance and the aggregation rules were written from lattice geometry and sampling arithmetic.
- **New TB and TD have never been run.** The canonical run meets them fresh (Mike's ruling 3 on the probe record; TD was never in the probe).
- **An error of L1's in the probe record.** Probe record §3 item 4 says TC "gives the two rules different spatial output". On TC both indices are increasing functions of u alone and have the same contour family (§3.3). What the probe showed there was a difference of amplitude. L1 could have computed this from the formula before writing the item.
- Probe output enters no gate, tolerance, calibration or qualification, and never becomes a canonical observation.

**1.1 The object.** On a lattice whose bases differ from cell to cell and are frozen in time, with one action stream per cell, coupled only through local reinforcement of registration: (i) whether the two prescribed compositions give spatial output that can be told apart at declared resolution, and (ii) whether, under each prescribed composition, an observed boundary defined without reference to λ can be represented by a level set of that composition's local λ.

**1.1′ What the finite instrument can claim.** One lattice size (N = 10,000), one horizon, a 20-seed dynamics panel on deterministic terrains, a declared spatial resolution. Twenty seeds on a fixed terrain are not twenty terrains. Results hold for the declared rule, terrain, object, size, horizon and resolution. No lattice result selects which composition describes entrepreneurial ecosystems. `F_LR` and `F_2_symmetric` are untested; a product-against-mean contrast does not select multiplication among zero-collapsing functions. One lattice size is not a scaling study.

**1.2 Endpoints (two results, each with its own record; no headline word is derived from them `[RULED 2026-11-13]`).**

- **B, conditional boundary compatibility — the scored substantive endpoint `[RULED]`.** For each composition X and each required terrain (§3.3), in the realization: the operational occupancy boundary of §5.5 is, or is not, within the permitted discrepancy ε of some level set of λ^X. Arm-level outcomes and their aggregation are in §5.5–§5.6. A pass is compatibility within the declared scope. A valid failure says the local-scalar description fails for that rule, terrain, object, size, horizon and resolution.
- **D, conditional discrimination `[RULED]`.** On the terrain designated for it (TB; §3.3), each arm's boundary is compared with both contour families. D is DISTINGUISHED iff, in both arms, the boundary is compatible with the arm's own family and adverse against the rival's (§5.6). A pass establishes a distinguishable output consequence of changing the composition in the instrument and nothing about which composition describes ecosystems. A non-pass can mean an uninformative terrain, insufficient resolution or indistinguishable output.

**1.2″ The bridge from PD7 to the observed boundary (instrument-level; required by L2 Q1) `[RULED 2026-11-13]`.** PD7 commits the activation surface Λ = Λ*. This contract operationalizes "an observed boundary" as the **operational occupancy boundary**: the edge of the region where the realization's seed-mean occupancy is at least a fixed threshold θ (§5.5). It is an instrument object. It is not the persistence threshold of the skeleton, and on a smooth terrain it need not mark any abrupt change. B tests whether it is a λ level set. The bridge is this contract's declaration, not a commitment of the theory.

**1.2′ Fidelity tier (pre-registered in full; reported with uncertainty in every record, favorable or not; never scored).** (i) Skeleton finite-horizon persistence threshold κ̂_c per arm against the spectral crossing κ = 1, as normalized and raw-g shifts; against T0's own κ̂_c. (ii) Local m_i = g·λ_i·Δt/q on the observed edge, against 1 (a local homogeneous benchmark) and against T0's measured boundary; neither is a pointwise prediction. (iii) Seed-mean occupancy against the site closure's fixed-point probabilities (§4.2), matched in object and floor; where edges are compared, the §5.5 rule is applied to both maps. (iv) The fitted level λ*_X of §5.5 at each level. A poor comparison is published as such and never becomes a scored failure.

**1.3 Reported only (mandatory reporting items; never scored, never tested; none enters B or D).**
- **(a) Diagnostic K, the coupling contrast `[RULED 2026-11-13: mandatory, separately reported, never gating; the skeleton form is L1's proposal and has not been seen by L2]`.** For every terrain arm, in the skeleton (η_floor = 0, all cells active at t = 0): the number of surviving seeds of 20 at each of the 15 levels, the persistence threshold κ̂_c (§5.4) and its bracket (the highest level with fewer than 18 survivors, and κ̂_c), and which of four descriptions holds: both phases inside the sweep; survival at every level; survival at none; non-monotone survival. Its purpose: independent two-state cells with activation hazard g·d₀·λ_i have no absorbing state and no persistence threshold, and the coupled rule has both. The same protocol is applied to both compositions. It qualifies how a pass of B may be described and determines nothing about B or D.
- **(b) Whole-map contour constancy**, p_i = h(λ_i): the fraction of across-cell occupancy variance carried by contour-bin means, per arm and level.
- **(c) The flicker record** of §2.11.
- **(d) Margin summaries**, design side (§3.2) and measured side (§5.7).
- **(e) TC's suppression contrast `[RULED 2026-11-13: reported only]`:** mean occupancy over cells inside the patch (bump ≥ 0.5) and outside it (bump ≤ 0.05), and their ratio, per arm and level; the sets are defined by terrain geometry and are the pre-probe declaration's (R-6).
- **(f) The evaluator's full output at θ = 0.10 and θ = 0.30** beside the scored θ (§5.5).
- **(g) The skeleton's boundary** under the §5.5 rule where a surviving map has one.

**1.4 What no result here may be represented as.** A confirmation or refutation of the theory (candidates produce or fail to produce). A selection of the true composition. Evidence of collective reinforcement from D or B alone: an uncoupled independent-response process passes both (Design Note v0.3 §3.4). Evidence for literal zero-collapse: TC is near-face feedback suppression, the floor does not depend on the bases, and at exactly λ = 0 a realization cell has stationary occupancy 0.0523. A statement about Regime II, Ψ, coherence or the margins hypothesis. A resolution of onset continuity. A reopening of any Flight 8 or E1 verdict.

## 2. The substrate rule (frozen at ratification)

**2.1 Lattice and state.** L×L Moore lattice, **L = 100** `[RULED 2026-11-12, probe record §5 item 1]` (N = 10,000), periodic; x_i(t) ∈ {0, 1}; Δt = 1. L = 100 refines the same unit-torus terrain that the probe ran at L = 50: features double in lattice units relative to the one-cell interaction range.

**2.2 Bases and compositions.** v_i, u_i, r_i frozen for the run; Q off, Γ = 0, drive 0, noise off. Heterogeneity is between cells only `[RULED, H3]`. Two compositions `[RULED R1]`: **P** = `F_canonical` = v·u·r; **H** = `F_baseline` = (v + u + r)/3, selected under the specification's arbitration clause for rival use only, a compensatory comparator never presented as satisfying zero-collapse.

**2.3 Local density.** d_i(t) = (active Moore neighbours of i at t)/8.

**2.4 Transition probabilities, from the state at t, applied simultaneously (Contract F8 §2.4 with a per-cell λ).**
- inactive → active: 1 − exp(−[η_floor + g·λ_i·d_i(t)]·Δt)
- active → inactive: 1 − exp(−μ·Δt)
No other term. The floor is not gated by any base, and floor-generated events are not masked out of density `[RULED, ruling 7]`.

**2.5 Timing and streams.** Synchronous two-phase advance, one uniform per cell per tick. **Every run has its own derived stream**, keyed by (panel master, terrain, composition, object, initialization, κ in integer micro-units, seed index); nothing is paired between arms, objects or levels `[RULED 2026-11-13]`. The uncertainty method of §5.5 assumes exactly this.

**2.6 Objects.** Realization: η_floor = η₀, stationary floor-only start; the primary object for B and D `[RULED R12]`. Skeleton: η_floor = 0, all cells active at t = 0; the structural reference and the object of diagnostic K. Extinction is a valid observation.

**2.7 Deactivation.** μ = 0.2 (q = 0.181269; mean complete active spell 1/q = 5.5167 ticks at every cell and level, which makes that mean an implementation check and not an observable).

**2.8 Control.** Bases frozen, g swept `[RULED R5]`. For composition X on a fixed terrain, with A the Moore adjacency: B_X = diag(λ^X)·A/8; g_spec,X = q/(Δt·spr(B_X)); **κ = g/g_spec,X** `[RULED, spectral-relative gain]`. Conditions, all binding: computed from terrain arrays and adjacency before any dynamic data; raw bases, raw λ, spr, g_spec, g, κ and local m_i all persisted; never normalized by an observed onset, occupancy or fitted edge; if spr = 0 there is no finite crossing, no division and no level; raw-g values reported beside κ; the normalization is fixed for scored analysis. The crossing at κ = 1 is true by definition and is not a result. The equivalence of sweeping g and scaling λ is specific to this rule: in the Overview the spontaneous term also scales with Λ and here the floor is fixed (notation row, §10).

**2.9 Levels.** 15 values of κ in integer micro-units `[RULED 2026-11-13; value PROPOSED until freeze]`: 0.75; 1.00 to 2.00 in steps of 0.10; 2.25; 2.50; 3.00. The same grid for every arm. No level is added, dropped or selected after any canonical output exists.

**2.10 Horizon and panel.** T = 3,000 ticks; recording tail = last 1,000 `[PROPOSED, carried]`. 20 seeds per configuration `[PROPOSED, carried]`. Fresh masters throughout, drawn by a declared rule after freeze `[DERIVED@BUILD]`.

**2.11 Flicker record (pre-probe declaration §6, incorporated unchanged; discharges Interpretation 004 point 4).** Windows W ∈ {1, 10, 100} ticks, non-overlapping complete blocks aligned to the first tick of the tail; a window is active if the cell is active at any tick in it. Persisted per cell, per run, per W: A (active windows), R₀ (observed inactive segments), first and last window states. Statistic: W·(n − A)/R₀ ticks, the mean length of observed inactive segments clipped to the tail; an all-active record returns "undefined: no inactive segment"; segments touching either end are flagged as possibly censored. Coverage: every run at every level of §2.9. Reported as its distribution over cells by occupancy band beside the W-specific floor reference (0.0523, 0.1342, 0.6496). Recorded, not tested. The probe found that at W = 100 most cells of non-extinct runs are active in all ten windows; the window set is left as declared `[RULED, probe record §5 item 5]`. The participation window stays W = 1 tick (PD5).

## 3. Terrains (all closed-form on the unit torus; cell (i, j) at x = i/L, y = j/L)

**3.1 The family `[RULED R3; TB and TD as ruled 2026-11-12 on L1's step-1 numbers]`.** With c(z) = cos(2πz):

| Terrain | Definition |
|---|---|
| T0 flat | v = u = r = 0.8 |
| TA concordant | v = u = r = 0.6 + 0.15·(c(x) + c(y)) |
| TB cross-gradient | s = 0.55 + 0.07·c(x); d = 0.19 + 0.19·c(y); v = s + d; u = s − d; r = 0.8 |
| TC near-face | bump = ((1 + c(x − ½))/2)⁴·((1 + c(y − ½))/2)⁴; v = r = 0.9; u = 0.9 − 0.85·bump |
| TD margin variants | v = u = r = 0.3 + 0.6·½·(1 + tanh(δ/w)), δ the distance in cells to the edge of the core C, positive inside |

T0, TA and TC are the probed formulas, unchanged `[RULED, probe record §5 item 4]`.

**3.2 TB and TD as ruled.**
- **TB.** The product is r·(s(x)² − d(y)²), exactly additive in x and y. Criterion `[RULED]`: the product's x-share of across-cell variance lies in [0.40, 0.60], measured from the arrays. Measured: **0.5173 along x, 0.4827 along y**, interaction below 1e-15 (as probed: 0.9932 along x). The height index (2s + r)/3 varies along x only. Disclosed cost: the height index's max/min on TB is 1.16 (as probed, 1.50). Whether the H arm offers an edge at θ on TB is not known. If it does not, that arm is NOT DISTINGUISHED and with it D and B for composition H (§5.6). That is a declared outcome, not a defect.
- **TD `[RULED]`.** The core C is a fixed set of cells given in closed form, with no reference to λ, g or either composition: the union of n equal discs centred on cell corners, **|C| = 2,000 cells exactly** in every variant. n = 1: centre (49.5, 49.5), R = 25.3 cells. n = 4: centres (24.5 or 74.5, 24.5 or 74.5), R = 12.65 cells. No cell centre lies within 0.03 cells of the edge. Four variants, n ∈ {1, 4} × w ∈ {2, 4} cells:

| Variant | Lattice perimeter of C | Band cells (10–90% of the base step) | Band / core | Largest base step per cell |
|---|---|---|---|---|
| TD-1-2 | 200 | 676 | 0.338 | 0.146 |
| TD-1-4 | 200 | 1,376 | 0.688 | 0.074 |
| TD-4-2 | 416 | 1,424 | 0.712 | 0.143 |
| TD-4-4 | 416 | 2,816 | 1.408 | 0.074 |

  Continuum perimeters 159.0 and 317.9 cells. For both compositions C equals the set of cells whose index is at least its value at the half-height base (checked for every variant). Under P the index t³ is not symmetric across the edge. The distance function has a crease midway between discs, where the base is within 0.5% of its floor. In TD-4-4 the plateau reaches 99.75% of full height. No criterion, threshold, evaluator branch or stopping rule refers to the margins hypothesis `[RULED, H2]`.

**3.3 Terrain roles `[RULED 2026-11-13]`.** Two indices have the same contour family when each is a monotone function of the other across cells (computed from the arrays).

| Terrain | Same contour family for P and H? | Role |
|---|---|---|
| T0 | trivially (both constant) | implementation and fidelity reference; not a required case |
| TA | yes | non-identifiability control for D; required case for B |
| **TB** | **no** | **required case for D**; required case for B |
| TC | **yes** — both indices are increasing functions of u alone | required case for B; suppression contrast reported (§1.3 e) |
| TD (all four) | yes | required cases for B (a stress family across geometries); margins descriptive |

Both compositions run on every terrain except T0 `[RULED 2026-11-13]`, so geometry and composition are never entangled. Per composition there are **seven required arms for B**; across both, fourteen. On TB, a P contour lies between 14.3 and 31.5 cells from the nearest H contour, and an H contour between 14.0 and 25.0 cells from the nearest P contour (§5.5 distance; deciles of each index; Appendix A). **D rests on TB alone.** Amplitudes may not be substituted for contours (Design Note v0.3 §3.6; L2 Q1 §3.5). A role is never changed after any canonical output exists.

**3.4 Identities.** For every terrain the freeze commits the formula, parameters, λ ranges, spr and g_spec for both compositions, and the SHA-256 of the base arrays (Appendix A; Flight 10 may reuse the terrains). The formulas pass through cos, tanh and sqrt, and Windows and Linux math libraries are known to differ by up to one unit in the last place. **Array hashes of record are measured on the canonical machine at build `[DERIVED@BUILD]`; the container values in Appendix A are provisional, and cross-platform agreement is bound by a declared tolerance of 1e-12 per element with the deviation recorded** `[RULED 2026-11-13; the M5-6 precedent]`. The set C of TD is exact on both platforms.

## 4. Comparators (fidelity; never scored)

**4.1 Spectral crossing.** κ = 1 by construction; g_spec per arm in Appendix A. It is the zero-floor site-closure comparator; its lattice counterpart is the skeleton's finite-horizon persistence threshold κ̂_c (§5.4). The realization has activity at g = 0 and has no absorbing-state onset. The crossing is set by the leading mode of the spatial feedback operator, which may localize on a high-λ region.

**4.2 Site closure.** p_i′ = (1 − p_i)·[1 − exp(−Δt·(η_floor + g·λ_i·Σ_j A_ij·p_j/8))] + (1 − q)·p_i, iterated from p = 1 (skeleton) or p = π₁ (realization) to a fixed point: tolerance 1e-12 in max norm, at most 200,000 iterations `[PROPOSED]`. Nonconvergence is recorded as "fidelity comparator unavailable" for that arm and level and affects no endpoint. m_i = 1 is a local homogeneous benchmark, not the closure's edge.

**4.3 T0 as the lattice reference.** Flight 9's own flat arm at L = 100 on the §2.9 grid with a fresh panel, with its uncertainty and its unavailable-boundary case. Flight 8's 1.521739 is not used as a constant. T0's measured value never retunes a scored tolerance.

## 5. The instrument (package `f9`, new beside `f8`; nothing in `f8` or `e1` modified)

**5.1 N1 — rule, terrains, levels, record.** Per-cell-λ step; terrain builder with committed identities; the §2.11 record; per-tick global active count; extinction tick; survival. **Reduction requirement (apparatus):** with a constant λ array the step returns exactly the placed Flight 8 scalar step's array at equal state, effective gain, floor, μ, timing and uniforms; initialization, stream identity and observables are checked separately. M2, M4 and M6 are not carried `[RULED R11]`.

**5.2 N3 — null reference.** The floor-only stationary occupancy π₁ = 0.0523 carries analytically. No Flight 8 band, tolerance or threshold is carried.

**5.3 N5 — closure.** §4.1–§4.2 per arm.

**5.4 Skeleton survival (diagnostic K and fidelity).** survival = active count > 0 at every tail tick. κ̂_c = the lowest level with ≥ 18 of 20 surviving such that every higher level also has ≥ 18 `[PROPOSED, carried]`.

**5.5 N-E — the composition evaluator (complete algorithm).** Applied to each realization arm at each level. The order is binding: the occupancy estimate, then the occupancy criterion, then the edge, then the comparison. λ, g, κ and the terrain enter nowhere in steps 1–4.
1. **Occupancy estimate `[RULED 2026-11-13]`.** p̄_i = mean over the 20 seeds of A_i(W = 1)/1,000, the seed-mean tail occupancy. Per-seed maps are preserved and are the resampling units. p̃ = the 3×3 periodic box mean of p̄ (the rule's own interaction range). The boundary scored is the boundary of this mean map; it is not the boundary of a median map and not a typical boundary across runs.
2. **Occupancy criterion `[structure RULED 2026-11-13; value PROPOSED]`.** The operational occupied region is {i : p̃_i ≥ θ}, ties included, with **θ = 0.20** for every arm, terrain and level. It is a fixed occupancy, not a fraction of any map's range. For scale: the floor-only reference is 0.0523, so θ is an excess of 0.148 over the floor. The evaluator is also run at θ = 0.10 and θ = 0.30 and its full output reported (§1.3 f); those are not scored.
3. **Edge `[RULED 2026-11-13]`.** E = the set of 4-neighbour bonds, with periodic wrapping, joining a cell inside the region to a cell outside it, each represented by its midpoint. **Every component is included**: no patch or hole is removed, merged or down-weighted, and each bond has equal weight.
4. **Informative level (all required; each failure has its named cause, §7) `[RULED 2026-11-13; counts PROPOSED]`.** At θ the region and its complement each have at least 100 cells, and E has at least 40 bonds. An empty or full region is `no edge at θ`.
5. **Contours.** For index Y ∈ {P, H}: candidate levels are the 99 interior percentiles of λ^Y over cells `[PROPOSED]`; C_Y(ℓ) = the bonds joining a cell with λ^Y ≥ ℓ to one with λ^Y < ℓ, by the same edge rule as step 3. This is where λ is thresholded: to draw the predicted contour, never the observed edge.
6. **Discrepancy `[PROPOSED]`.** D(E, C) = max(95th percentile over E of the torus distance to the nearest point of C; 95th percentile over C of the distance to the nearest point of E), in cells. It is symmetric: an observed edge that covers only part of a contour is not that contour, and a predicted component that never appeared counts against the fit.
7. **Fit.** D_Y = min over candidate levels ℓ of D(E, C_Y(ℓ)); the minimizing level is λ*_Y (fidelity, §1.2′ iv). The level is free because location is fidelity, not structure.
8. **Permitted discrepancy `[structure RULED 2026-11-13; value PROPOSED]`.** **ε = 2.0 cells.** What it controls: how far, in lattice cells, the operational occupancy boundary may lie from a level set of the index and still be called represented by it. Why this amount: one cell is the interaction range, and a bond midpoint lies half a cell from either cell centre; two cells is that resolution with a margin. On the noise-free TD discs (radii 12.65 and 25.3 cells) the 3×3 mean leaves the half-level contour unmoved (0.0 cells, by script). ε is a declared resolution in the sense W_res was in Contract F8 §4.5: a different ε is a different instrument. It is never enlarged because precision is poor.
9. **Uncertainty `[RULED 2026-11-13; counts PROPOSED]`.** 1,000 resamples of the 20 seed maps with replacement, from a declared evaluator stream; steps 1–7 recomputed on each. For index Y: **compatible** iff the 95th percentile of resampled D_Y is ≤ ε; **adverse** iff the 5th percentile is > ε; **unresolved** otherwise. If more than 5% of resamples fail step 4 the level is not informative (cause `unstable edge`). Poor precision gives "unresolved", never a pass.
10. **Sampling arithmetic.** Under an independent-chain approximation the per-cell standard error of p̄ is 0.005 to 0.008 for occupancies from 0.05 to 0.5 (Appendix A). The real value comes from the calibration census (§8 job 0), which also supplies the noise for the qualification of §6.2.

**5.6 Outcome records and aggregation `[RULED 2026-11-13]`.**
- **Per arm and informative level (own = the arm's composition; rival = the other):**

| Own | Rival | Record |
|---|---|---|
| compatible | adverse | follows own; rival excluded |
| compatible | compatible or unresolved | follows own; identification not distinguished (on a same-family terrain: not adjudicable here) |
| adverse | compatible | follows rival (only where the families differ, §3.3) |
| adverse | adverse | follows neither |
| unresolved | any | not distinguished |

- **Arm-level B.** COMPATIBLE iff at least 3 levels are informative and the own record is compatible at every informative level. ADVERSE iff the own record is adverse at two or more adjacent informative levels. NOT DISTINGUISHED otherwise, with cause. The two-adjacent requirement is a replication condition against one noisy level among 15, not a vote; it is put to L2 (§11). Failure to reject is not equivalence; failure to establish either fit is not "neither". A level that is not informative is reported and does not enter the arm rule; an arm with fewer than 3 informative levels cannot be COMPATIBLE.
- **Flight-level B, per composition X — a conjunction over the seven required arms of §3.3, no vote across terrains.**

| Situation | B for composition X |
|---|---|
| Apparatus or qualification requirements fail | no qualified scientific determination |
| At least one required arm is ADVERSE | **NOT PRODUCED** |
| No required arm ADVERSE, at least one NOT DISTINGUISHED | **NOT DISTINGUISHED** |
| All seven required arms COMPATIBLE | **PRODUCED**, with its domain and resolution stated |

  An adverse arm decides the word even when another arm is unresolved; the unresolved arm still appears in the record. Every arm's record is published whatever the flight-level word.
- **D, on TB.** DISTINGUISHED iff in both arms at least 3 informative levels carry "follows own; rival excluded". NOT DISTINGUISHED otherwise, with cause. "Follows rival" in an arm is published and enters that arm's B record as its adverse levels.
- **Multiplicity.** With 15 levels, 14 terrain arms and two indices, per-level error rates compound. The statistical qualification of §6.2 states its error targets at the arm level and the flight level, not per level.

**5.7 Reported items (package reporting items with coverage and validity checks; values gate nothing; a missing required record prevents a claim of complete reporting).** The fidelity tier of §1.2′; every item of §1.3; the flicker record with range checks and counts of all-active and all-inactive cell-records per W; measured-side margin summaries computed afterwards at the fixed occupancy cuts 0.10, 0.20 and 0.30 `[RULED 2026-11-13]`, every cut reported, beside the W-specific floor reference.

**5.8 T0 `[RULED 2026-11-13; values PROPOSED]`.** (i) The reduction of §5.1 is the apparatus check. (ii) Flight 8's four tests are rerun on T0 as a scientific consistency exercise with redeclared values: skeleton-high, skeleton-low (ρ₀ = 0.02) and realization sweeps on the §2.9 grid; survival threshold 18 of 20; f_J = 0.25 applied to increases per unit κ scaled to the 0.10 spacing; Δκ = max(0.0254, 0.0055) + 0.10 = **0.1254** (Contract F8 §3.4's procedure at N = 10,000; Appendix A); evaluability band from this flight's calibration census. Its record is PRODUCED, NOT PRODUCED or NOT DISTINGUISHED for T0 alone. An adverse or ND result there is not automatically a coding defect, gates no endpoint, and does not resolve onset continuity. If T0's boundary is unavailable, every T0-referenced fidelity item is recorded "reference unavailable".

**5.9 N7 — records, package, readiness.** The principles of Contract F8 §4.10 carry: completeness against readiness computed separately; valid adverse records; apparatus and qualification prerequisites require passage, scientific prerequisites valid completion; identity and authorization binding. The record graph is Flight 9's own (§8). Every record binds: terrain formula and base-array identity, composition, g, κ, g_spec and spr, lattice geometry, object and floor, horizon and tail, seed and stream identity, window convention, summary schema, θ and ε, evaluator identity and qualification identity.

## 6. Qualification of the evaluator (before any canonical scoring) `[RULED 2026-11-13; sizes PROPOSED]`

**6.1 Known-answer corpus (implementation).** Synthetic seed-map sets with constrained noise; every class returns exactly its named record and cause on ≥ 95 of 100; **cross-trigger rule**: the right record with the wrong cause fails. Classes:
1. p = h(λ^P) on TB, straddling θ, scored as the P arm → follows own; rival excluded.
2. The same maps scored as the H arm → follows rival.
3. p = h(λ^H) on TB, scored both ways, likewise.
4. p = h(a third function: the TB product rotated by 45°) → follows neither.
5. p = h(λ) on TA → own compatible; not adjudicable here.
6. A map everywhere below θ, and one everywhere above → `no edge at θ`.
7. A region of 50 cells → `under-resolved`.
8. An edge displaced 1 cell from a contour → compatible; displaced 4 cells → adverse.
9. **A missing predicted component:** the TD four-disc pattern with one disc absent from the map → adverse.
10. **Speckle:** a compatible map with per-cell noise at the calibration amplitude, all components included → compatible. This class tests the departure of §5.5 step 1 from L2's advice.
11. Noise raised until over 5% of resamples lose the edge → `unstable edge`.

An independent-response map (class 1) is correctly a pass: it satisfies the tested property (§1.4).

**6.2 Statistical qualification (design and held-out ensembles).** Generator truth independent of the evaluator: 20 seed maps per case, each h(index) plus spatially correlated noise whose per-cell amplitude and correlation length are taken from the calibration census `[DERIVED@BUILD]`. The independent unit is the seed map. The six risks of Design Note v0.3 §10.1 are the classes: false identification (TA-type and rival-generated cases); vacuous support (constant, empty-edge, saturated, singleton-contour cases); false adverse (truly compatible maps under correlated noise at the calibration amplitude and at 1.5 times it); improper ND (sufficiently discriminating cases must keep their record); aggregation (whole synthetic sweeps of 15 levels scored by §5.6's arm rule, and whole synthetic flights of seven arms by the conjunction); wrong cause. **Behaviour near ε is priced, not assumed:** cases with true displacement 1.0, 1.5, 2.0, 2.5 and 3.0 cells, with the rates of compatible, adverse and unresolved reported for each. 200 cases per class in each ensemble; applicable error per class with one-sided 95% Clopper–Pearson upper bound ≤ 0.10 (at most 12 errors in 200); halts counted as errors; design AND held-out joined mechanically; the held-out master is drawn only after the generator, classes, counts and caps are frozen. A failed qualification closes the stage; no same-stage repair. Guarantees hold for the declared ensembles only and do not transfer automatically to the lattice.

## 7. Failure paths, with precedence (highest first) `[RULED 2026-11-13]`

| # | State | Kind | Cause label | Effect |
|---|---|---|---|---|
| 1 | Run halts; record missing, corrupt or out of range | apparatus | `apparatus unevaluable (<key>)` | level unevaluable; arm NOT DISTINGUISHED (apparatus); never adverse |
| 2 | Skeleton run extinct | valid observation | — | enters diagnostic K and κ̂_c; never "missing" |
| 3 | Region at θ empty or full (includes floor-dominated and saturated maps) | scientific ND | `no edge at θ` | level not informative |
| 4 | Region or complement under 100 cells, or under 40 edge bonds | scientific ND | `under-resolved` | level not informative |
| 5 | Over 5% of resamples fail step 4 | scientific ND | `unstable edge` | level not informative |
| 6 | Fewer than 3 informative levels | scientific ND | `insufficient informative levels` | arm NOT DISTINGUISHED |
| 7 | Own unresolved | scientific ND | `finite resolution` | level not distinguished |
| 8 | Own adverse at one isolated level | scientific ND | `isolated adverse level` | arm NOT DISTINGUISHED unless rule 9 applies |
| 9 | Own adverse at two or more adjacent informative levels | scientific adverse | `boundary not a level set of own index` | arm ADVERSE |
| 10 | Site closure does not converge | fidelity unavailable | `comparator unavailable` | fidelity item only |
| 11 | T0 boundary unavailable | fidelity unavailable | `reference unavailable` | T0-referenced fidelity items only |

No failed terrain is dropped, no level is selected after the fact, no role is changed, and every state is preserved in the package. A required arm that lacks information does not disappear: it is NOT DISTINGUISHED and enters the conjunction as such. An adverse result is never recast as fidelity or ND. Precision ceiling and stop path `[PROPOSED]`: if the calibration census shows a median per-cell standard error of p̃ above 0.02 at any arm and level, the stage stops before any canonical census and a new instrument version is declared; the sample size of this stage is never changed after data exist.

## 8. Jobs, order, authorizations `[RULED 2026-11-13]`

Order: Appendix A computed → freeze → instrument version identity → reduction check → known-answer corpus → masters drawn → job 0 → statistical qualification (design, then held-out, then joined) → **passage required** → canonical scientific jobs. Each job runs only under a Mike-issued authorization naming the stage and the jobs; one authorization per step; the registry is append-only; each authorization file gets one commit.

| # | Job | Kind | Content |
|---|---|---|---|
| 0 | `calibration_census` | apparatus prerequisite, never scored, never reused | all 15 arms × 2 objects × 15 levels × 20 seeds under its own master (9,000 runs); gives the per-cell standard error, the noise parameters of §6.2 and the §7 ceiling |
| 1 | `evaluator_known_answer`, `evaluator_design_audit`, `evaluator_held_out_audit`, `evaluator_qualification` | qualification | §6 |
| 2 | `t0_census` | scientific (consistency) | T0, three sweeps (900 runs); §5.8 |
| 3 | `skeleton_census` | scientific | 14 terrain arms, skeleton (4,200 runs); diagnostic K, κ̂_c |
| 4 | `realization_census` | scientific | 14 terrain arms, realization (4,200 runs); B and D |
| 5 | `census_stability` | scientific | jobs 3–4 on an independent panel (8,400 runs); arm-level records reproduced or not, reported |
| 6 | `fidelity_report`, `coupling_diagnostic_report`, `flicker_report`, `margin_report` | reporting | §1.2′, §1.3, §5.7 |
| 7 | `resource_benchmark`, `stage1_package` | apparatus / package | as Flight 8's grammar |

Arms: T0·P, and P and H on each of TA, TB, TC, TD-1-2, TD-1-4, TD-4-2, TD-4-4 (15). In the container probe at L = 100 a realization run took 0.96 s and a skeleton run 0.62 s on average, so one 9,000-run panel is about 2.0 hours there; the canonical machine is unmeasured `[DERIVED@BUILD, resource benchmark]`. The complete paired design is priced here before freeze; if it proves too expensive the claimed scope is reduced prospectively with paired comparisons kept on what remains. Instrument version string `f9_stage1_v1` `[PROPOSED]`.

## 9. Declarations table

| Declaration | Value | Marker |
|---|---|---|
| L, N | 100; 10,000 | RULED |
| Compositions | P = `F_canonical`; H = `F_baseline` (rival only) | RULED |
| η₀; μ; Δt | −ln(0.99); 0.2; 1 | RULED (carried) |
| Control | bases frozen, g swept, κ = g/g_spec,X | RULED |
| κ grid | 0.75; 1.00–2.00 by 0.10; 2.25; 2.50; 3.00 (15) | RULED 2026-11-13; value PROPOSED |
| T, tail; seeds | 3,000 / 1,000; 20 | PROPOSED (carried) |
| Streams | every run its own; nothing paired | RULED 2026-11-13 |
| Terrains T0, TA, TC | probed formulas | RULED |
| TB | §3.1; x-share criterion [0.40, 0.60]; measured 0.5173 | RULED |
| TD | §3.2; \|C\| = 2,000; n ∈ {1, 4} × w ∈ {2, 4}; concordant; both compositions on all four | RULED |
| Terrain roles | §3.3; seven required arms for B per composition; D on TB | RULED 2026-11-13 |
| Flicker record | §2.11 | RULED (pre-probe declaration §6) |
| Scored map | seed-mean W = 1 occupancy, 3×3 mean | RULED 2026-11-13 (3×3 mean put to L2) |
| Occupancy criterion | fixed θ; scored θ = 0.20; reported 0.10 and 0.30 | structure RULED; values PROPOSED |
| Edge | 4-neighbour bonds, periodic; every component included | RULED 2026-11-13 |
| Informative level | ≥ 100 cells each side; ≥ 40 bonds | RULED; counts PROPOSED |
| Contour candidates; discrepancy | 99 percentiles; symmetric 95th-percentile distance | PROPOSED |
| Permitted discrepancy | single ε; ε = 2.0 cells | structure RULED; value PROPOSED |
| Resamples; one-sided level; instability limit | 1,000; 95%; 5% | RULED; counts PROPOSED |
| Arm rule | ≥ 3 informative levels, all compatible; ADVERSE at two adjacent adverse levels | RULED 2026-11-13 (put to L2) |
| Flight rule for B | conjunction over seven required arms per composition | RULED 2026-11-13 |
| D | TB only; ≥ 3 levels "follows own; rival excluded" in both arms | RULED 2026-11-13 |
| Headline word | none | RULED 2026-11-13 |
| Diagnostic K | skeleton, 18 of 20; counts, κ̂_c and bracket; never gating | RULED 2026-11-13 |
| TC suppression contrast | reported only; sets bump ≥ 0.5, bump ≤ 0.05 | RULED 2026-11-13 |
| T0 exercise | Δκ = 0.1254; f_J = 0.25; ρ₀ = 0.02; gates nothing | RULED; values PROPOSED |
| Known-answer; qualification | eleven classes, ≥ 95/100, cross-trigger; 200 per class, cap 0.10, CP 95% | RULED; sizes PROPOSED |
| Precision ceiling | median per-cell standard error ≤ 0.02, stop path | PROPOSED |
| Site closure solver | start p = 1 or π₁; 1e-12; 200,000 iterations | PROPOSED |
| Array identity tolerance | 1e-12 per element across platforms; canonical hashes of record | RULED 2026-11-13 |
| Margin cuts | occupancy 0.10, 0.20, 0.30 | RULED 2026-11-13 |
| g_spec, spr, λ ranges, base-array hashes | Appendix A | DERIVED@FREEZE (hashes DERIVED@BUILD) |
| Masters (calibration, canonical, stability, design, held-out, evaluator) | drawn after freeze | DERIVED@BUILD |
| Instrument version | `f9_stage1_v1` | PROPOSED |

## 10. Notation rows to append (append-only; the table governs)

| Object | O — Overview v1.8.1 | C — this contract | Nature |
|---|---|---|---|
| Spectral-relative gain | Λ/Λ* (implicit) | κ = g/g_spec,X; equals Flight 8's m on a flat terrain | C-only |
| Sweeping g against scaling Λ | the spontaneous term scales with Λ | the floor is fixed; g and λ enter only as g·λ_i | rule-specific equivalence; not interchangeable in every channel |
| Observed boundary | activation surface Λ = Λ* (PD7) | operational occupancy boundary: edge of {p̃ ≥ θ} (§5.5) | instrument-level bridge, C-only |
| Permitted discrepancy | — | ε, in lattice cells (§5.5) | C-only; a declared resolution |
| Compositions | F (open) | P = `F_canonical`, H = `F_baseline` (rival only) | prescribed inputs; no selection claimed |

## 11. Rulings of record on v0.1's §11, and what goes to L2

**11.1 Mike's rulings, 2026-11-13.** "Accept what you want of L2's advice and recommend on the others for my ruling", then "i rule as recommended" on L1's list of that date. As written into this version:

| v0.1 §11 item | Standing |
|---|---|
| 1 TC and discrimination | TC a required case for B; no role in D; suppression contrast reported only (§1.3 e, §3.3) |
| 2 Coupling contrast | diagnostic K, mandatory, never gating (§1.3 a) |
| 3 Bridge | operational occupancy boundary at a fixed θ (§1.2″) |
| 4 Edge rule | seed-mean map, 3×3 mean, θ = 0.20 scored with 0.10 and 0.30 reported, every component, informative-level counts (§5.5 steps 1–4) |
| 5 Distance and tolerance | symmetric distance, free level, single ε = 2.0 cells (§5.5 steps 5–8) |
| 6 Uncertainty | 1,000 seed resamples, one-sided 95% (§5.5 step 9) |
| 7 Aggregation | arm rule; conjunction over required arms; D on TB; no headline word (§5.6) |
| 8 κ grid | 15 levels (§2.9) |
| 9 Streams and map | independent streams; seed-mean map (§2.5, §5.5) |
| 10 Qualification sizes | as drafted, classes rewritten for fixed θ and single ε (§6) |
| 11 Failure paths and stop path | as drafted with `no edge at θ` (§7) |
| 12 T0 exercise | as drafted, gating nothing (§5.8) |
| 13 Jobs | as drafted, including the stability panel (§8) |
| 14 Array identities | canonical hashes of record; 1e-12 tolerance (§3.4) |
| 15 TD arms | both compositions on all four (§3.3) |
| 16 Reported items; margin cuts | §1.3; fixed cuts 0.10, 0.20, 0.30 (§5.7) |
| 17 Carried values | T = 3,000, tail 1,000, 20 seeds, 18 of 20, `f9_stage1_v1` |

L2's reply is committed with this version as a `_RECEIVED` byte copy, described as advice given without the draft.

**11.2 For Mike's acknowledgment (one item).** The count in L1's recommendation 5 was wrong ("13 required arms"). The rule as ruled is a conjunction over the required arms; there are seven per composition (§3.3). No rule changes.

**11.3 Open points put to L2 with the contract packet.**
1. The 3×3 mean kept as part of the occupancy estimator, against L2's preference for no processing; known-answer class 10 tests it.
2. θ = 0.20 proposed by an L1 who had seen the probe's occupancy percentiles (§1.0).
3. ε = 2.0 cells: its meaning, units, purpose and place in the rule are stated in §5.5 step 8, as L2 required before it would consider a value.
4. The two-adjacent-levels condition for an ADVERSE arm.
5. Diagnostic K in its skeleton form, which L2 has not seen; whether "survival counts and bracket" meets L2's "effect estimate and uncertainty".
6. Whether a required arm with no edge at θ at any level should be NOT DISTINGUISHED, as drafted, on every terrain.
7. The bond representation of the edge in place of L2's Moore boundary cells; the same rule is applied to the observed edge and the predicted contour.

## 12. Requirements carried from L2's design consultation (every REQUIRES CHANGE item)

| L2 item | Where |
|---|---|
| Q1 two conditional tests; boundary against whole map; independent edge; no vacuous support; uncoupled alternative disclosed; TA's role; six labels | §1.2, §1.3(b), §1.4, §3.3, §5.5–§5.6, §7 |
| Q2 statistical qualification, six risks, seed as unit, held-out untouched | §6.2 |
| Q3 rival-only status; reduction at matched effective gain; untested candidates | §2.2, §5.1, §1.1′ |
| Q4 normalization and its six conditions; rule-specific equivalence; notation row | §2.8, §10 |
| Q5 flicker estimand, windows, censoring, floor reference, bound level set | §2.11, §2.9 |
| Q6 onset continuity left open by name | §1.4, §5.8 |
| Q7 skeleton threshold against spectral crossing; m_i = 1 a benchmark; matched estimand; solver frozen; T0 reference | §1.2′, §4 |
| Q8 probe provenance; selection; Interpretation 004 timing | §1.0, §2.11 |
| Q9 §11.1 TC near-face, floor not gated | §1.4, §2.4 |
| Q9 §11.2 contour construction, membership, contrast; seed-mean against per-seed | §5.5 |
| Q9 §11.3 spatial scale; TD geometry; cuts frozen | §2.1, §3.2, §5.7 |
| Q9 §11.4 own record graph; reporting items | §5.7, §5.9, §8 |
| Q9 §11.5 fresh calibration; stream dependence | §2.5, §8 job 0 |
| Q9 §11.6 failure paths, precedence, aggregation | §5.6, §7 |
| Q9 §11.7 T0 reduction against replication | §5.8 |

## 13. What this contract does not claim

Nothing about Regime II, Ψ, coherence, the margins hypothesis, within-cell heterogeneity, many streams per cell or onset continuity. No value marked PROPOSED or DERIVED is of record until the freeze commit names it. Held and not authorized here: Gemini commission v3.1; the two next-touch repairs (`test_f8_m6.py` docstring, `test_f8_mp1.py` comment); the third-order lattice-versus-ODE comparison; Overview v1.8.2; onset continuity; the PD7-versus-floor correspondence. Mike rules; L2 reviews; Gemini audits for consistency only.

## Appendix A — provisional values (L1's container; script of record to be committed at freeze)

**A.1 Arms at L = 100.**

| Terrain | Base range | λ^P range | spr_P | g_spec,P | λ^H range | spr_H | g_spec,H | Base arrays SHA-256 (container, provisional) |
|---|---|---|---|---|---|---|---|---|
| T0 | 0.8 | 0.512 | 0.512000 | 0.354041 | 0.8 | 0.800000 | 0.226587 | `21babaa5c51d9630…` |
| TA | 0.300–0.900 | 0.0270–0.7290 | 0.701413 | 0.258435 | 0.3000–0.9000 | 0.880236 | 0.205933 | `5424742619823a0a…` |
| TB | 0.100–1.000 | 0.0688–0.3075 | 0.302417 | 0.599401 | 0.5867–0.6800 | 0.675214 | 0.268462 | `8e01e73fe20bd3dd…` |
| TC | 0.050–0.900 | 0.0405–0.7290 | 0.728367 | 0.248871 | 0.6167–0.9000 | 0.899373 | 0.201551 | `49f16928ebffe303…` |
| TD-1-2 | 0.300–0.900 | 0.0270–0.7290 | 0.725886 | 0.249721 | 0.3000–0.9000 | 0.896516 | 0.202193 | `6a2b17e61ce2af99…` |
| TD-1-4 | 0.300–0.900 | 0.0270–0.7290 | 0.723752 | 0.250458 | 0.3000–0.9000 | 0.894862 | 0.202567 | `c3785ab6944377a5…` |
| TD-4-2 | 0.300–0.900 | 0.0270–0.7290 | 0.713340 | 0.254113 | 0.3000–0.9000 | 0.884323 | 0.204981 | `79e8778dfdcc9b94…` |
| TD-4-4 | 0.300–0.898 | 0.0270–0.7253 | 0.690069 | 0.262683 | 0.3000–0.8985 | 0.869999 | 0.208356 | `b695cc434cd929c0…` |

T0 is run under P only; its H row is shown for completeness. T0, TA and TC reproduce the base-array hashes and g_spec values of the committed `F9_PROBE_IDENTITIES.json` at L = 100.

**A.2 TB contour separation (§5.5 discrepancy, cells; nearest contour of the other index).** P contour at its deciles 10…90: 31.5, 24.2, 20.5, 19.0, 18.0, 14.5, 14.3, 17.6, 24.6. H contour at its deciles: 25.0, 23.0, 21.3, 20.0, 19.0, 16.5, 14.0, 15.0, 16.6. On TA, TC and TD-4-2 the same computation gives 0.0 at every decile.

**A.3 Rule constants.** q = 0.181269; a = 0.01; π₁ = 0.052282; 1/q = 5.516656; floor-only probability of any activity in W ticks: 0.052282 (W = 1), 0.134244 (10), 0.649601 (100).

**A.4 T0 bracket at N = 10,000.** Lower term ln N/(q·2,000) = 0.0254; upper term (N·ρ*_sk ≥ 50, bisection on the Flight 8 map) = 0.0055; Δκ = 0.0254 + 0.10 = 0.1254.

**A.5 Per-cell standard error of p̄, independent-chain approximation only (20 seeds × 1,000 ticks).** 0.0048 at p = 0.0523; 0.0063 at 0.1; 0.0079 at 0.2; 0.0084 at 0.3; 0.0075 at 0.5. The calibration census replaces these.

**A.6 Run counts.** 15 arms × 2 objects × 15 levels × 20 seeds = 9,000 per full panel; T0 low-initialization sweep 300.

*L1 (Claude Fable 5.2), v0.1 2026-11-12, v0.2 2026-11-13.*
