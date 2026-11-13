# Contract F9 — Flight 9: terrain and composition under the hazard rule (v0.1, DRAFT)

**Status.** L1 draft v0.1, 2026-11-12, at Mike's word ("contract"; step 2 of his instruction of that date). **Not frozen. Not yet seen by L2.** Nothing here binds until Mike ratifies a version; no instrument, master, threshold, ensemble or run is produced under this document before that. Repository `main` at `a7d3a5d7a4b1c3e46f24a44083f37a0aa50534e7` when written (fresh clone). Review path: Mike's rulings on §11 → L2 contract packet under its own register → Gemini corpus audit (commission v3) → Mike's ratification → freeze.
**Lineage.** Successor to Contract F8 v0.8.4 (`e87277a2d11e948f…`, frozen; stage 1 CLOSED, qualified, at `9d3a23b`). Governed by Design Note v0.3 (`8d82e319d79402f8…`), L2's design consultation (`65d95bc3a907cf04…`), the ratified pre-probe declaration v1.0 (`473a2a165fd5cb4e…`) and the probe record (`f3affc05de26f0d7…`). Flight 8 stays closed as recorded; nothing in `f8` or `e1` is modified.
**Markers.** `[RULED]` = Mike's ruling of record; `[PROPOSED]` = L1 value for Mike and L2, ratified only at freeze; `[DERIVED@FREEZE]` = computed by a declared procedure from closed-form inputs before freeze, tabulated in Appendix A and committed in the freeze commit; `[DERIVED@BUILD]` = computed by the built instrument before any canonical master is drawn, committed with its identity.
**Notation.** Contract F8 names carry; the notation-scope table governs. **At first use: μ here is the deactivation rate (the Overview's lapse rate β), not the Overview's μ(ρ).** g is the feedback gain; η_floor the spontaneous floor as a per-tick hazard, committed value η₀ = −ln(0.99); λ_i per-cell conduciveness; d_i the Moore active fraction; q = 1 − e^(−μΔt). Bases are v, u, r. New here: κ, the spectral-relative gain (§2.8); P and H, the two compositions (§2.2). Participation vocabulary per PD1–PD7. The Annex is not cited.
**Numbers.** Every number in this draft was written from a script (`f9_step1.py` `d195c94015d6a667…`, `td_final.py` `ca0076012b8bbc0e…`, `f9_contract_arith.py` `57ccd322431bb2a7…`, `smooth_check.py` `d36b325cb7937002…`; none committed yet), run in L1's container (Python 3.13.18, NumPy 2.5.3) on terrain arrays, the Moore adjacency and closed-form rule constants only. Array hashes are container identities and are provisional (§3.4).

---

## 1. Object and claim grammar

**1.0 Provenance (dated record).** The claim grammar of §1.2 was fixed in the pre-probe declaration §1, ratified by Mike on 2026-11-12 before any Flight 9 lattice output existed. A noncanonical probe then ran once (896 runs, 4 seeds, master 9920261112, retired). What it showed, and what was decided because of it, is in the probe record §3–§5. Stated here so that no reader infers otherwise:
- **Selection.** L = 100, the finer κ grid, the retention of T0, TA and TC and the respecification of TB were decided with probe output known. Inference on these terrains is conditional on that selection.
- **Known before this contract.** At 4 seeds the skeleton was extinct at κ ≤ 1.25 and survived at κ ≥ 1.75 on every probed arm. The coupling contrast of §1.2 (E-K) therefore cannot be represented as independent of the probe.
- **Not seen.** L1 has rendered no occupancy map, computed nothing against λ contours and extracted no edge from probe output. The array files have not been opened for this draft. L1 has seen the probe report's across-cell occupancy percentiles (R-3), map correlations (R-4), the TB x-only variance fraction (R-5) and the TC inside/outside ratio (R-6). The edge rule, tolerances and aggregation rules of §5.5 were written from lattice geometry and sampling arithmetic, and each is marked PROPOSED so that L2 can test that statement.
- **New TB and TD have never been run.** The canonical run meets them fresh (Mike's ruling 3 on the probe record; TD was never in the probe).
- Probe output enters no gate, tolerance, calibration or qualification, and never becomes a canonical observation.

**1.1 The object.** On a lattice whose bases differ from cell to cell and are frozen in time, with one action stream per cell, coupled only through local reinforcement of registration: (i) whether the two prescribed compositions give spatial output that can be told apart at declared resolution, and (ii) whether, under each prescribed composition, an observed boundary defined without reference to λ can be represented by a level set of that composition's local λ.

**1.1′ What the finite instrument can claim.** One lattice size (N = 10,000), one horizon, a 20-seed dynamics panel on deterministic terrains, a declared spatial resolution. Twenty seeds on a fixed terrain are not twenty terrains. Results hold for the declared rule, terrain, object, size, horizon and resolution. No lattice result selects which composition describes entrepreneurial ecosystems. `F_LR` and `F_2_symmetric` are untested; a product-against-mean contrast does not select multiplication among zero-collapsing functions. One lattice size is not a scaling study.

**1.2 Endpoints (each keeps its own record; they are not forced into one label).**

- **E-B, conditional boundary compatibility — the scored substantive endpoint `[RULED]`.** For each composition X and each terrain, in the realization: the observed boundary of §5.5 is, or is not, within the equivalence tolerance of some level set of λ^X. Arm-level outcomes and their aggregation are in §5.5–§5.6. A pass is compatibility within the declared scope. A valid failure says the local-scalar description fails for that rule, terrain, object, size, horizon and resolution.
- **E-A, conditional discriminability `[RULED]`.** On terrains whose two contour families differ (§3.3), each arm's observed boundary is compared with both families. E-A is DISTINGUISHED on a terrain iff, in both arms, the boundary follows the arm's own family and the rival family is excluded (§5.6). A pass establishes a distinguishable output consequence of changing the composition in the instrument and nothing about which composition describes ecosystems. A non-pass can mean an uninformative terrain, insufficient resolution or indistinguishable output.
- **E-K, coupling contrast `[PROPOSED — L1's proposal, not yet seen by L2; Mike's ruling 3 on the consultation]`.** In the skeleton (η_floor = 0, all cells active at t = 0), each terrain arm's sweep contains a level at which fewer than 18 of 20 seeds survive and a higher level at and above which at least 18 survive. Independent two-state cells with activation hazard g·d₀·λ_i have no absorbing state and no such threshold; the coupled rule has both. E-K is recorded per arm as PRESENT, ABSENT (survival at every level, or at none) or NOT DISTINGUISHED (non-monotone survival). It is recorded beside E-B and qualifies how a pass of E-B may be described; it is not conjoined with it.

**1.2″ The bridge from PD7 to the observed boundary (instrument-level; stated as required by L2 Q1).** PD7 commits the activation surface Λ = Λ*. This contract operationalizes "an observed boundary" as an iso-occupancy contour of the realization's seed-mean occupancy map, at a split chosen from the occupancy values alone (§5.5). That contour is an instrument object. It is not the persistence threshold of the skeleton, and on a smooth terrain it need not mark any abrupt change. E-B tests whether that contour is a λ level set. The bridge is this contract's declaration, not a commitment of the theory.

**1.2′ Fidelity tier (pre-registered in full; reported with uncertainty in every record, favorable or not; never scored).** (i) Skeleton finite-horizon persistence threshold κ̂_c per arm against the spectral crossing κ = 1, as normalized and raw-g shifts; against T0's own κ̂_c. (ii) Local m_i = g·λ_i·Δt/q on the observed edge, against 1 (a local homogeneous benchmark) and against T0's measured boundary; neither is a pointwise prediction. (iii) Seed-mean occupancy against the site closure's fixed-point probabilities (§4.2), matched in object and floor; where edges are compared, the §5.5 rule is applied to both maps. (iv) The fitted level λ*_X of §5.5 at each level. A poor comparison is published as such and never becomes a scored failure.

**1.3 Reported only (never scored, never tested).** (a) Whole-map contour constancy, p_i = h(λ_i): the fraction of across-cell occupancy variance carried by contour-bin means, per arm and level. (b) The flicker record of §2.11. (c) Design-side and measured-side margin summaries (§3.2 TD; §5.7). (d) On TC, mean occupancy inside and outside the patch, defined by terrain geometry. (e) The skeleton's boundary under the §5.5 rule where a surviving map has one.

**1.4 What no result here may be represented as.** A confirmation or refutation of the theory (candidates produce or fail to produce). A selection of the true composition. Evidence of collective reinforcement from E-A or E-B alone: an uncoupled independent-response process passes both (Design Note v0.3 §3.4). Evidence for literal zero-collapse: TC is near-face feedback suppression, the floor does not depend on the bases, and at exactly λ = 0 a realization cell has stationary occupancy 0.0523. A statement about Regime II, Ψ, coherence or the margins hypothesis. A resolution of onset continuity. A reopening of any Flight 8 or E1 verdict.

## 2. The substrate rule (frozen at ratification)

**2.1 Lattice and state.** L×L Moore lattice, **L = 100** `[RULED 2026-11-12, probe record §5 item 1]` (N = 10,000), periodic; x_i(t) ∈ {0, 1}; Δt = 1. L = 100 refines the same unit-torus terrain that the probe ran at L = 50: features double in lattice units relative to the one-cell interaction range.

**2.2 Bases and compositions.** v_i, u_i, r_i frozen for the run; Q off, Γ = 0, drive 0, noise off. Heterogeneity is between cells only `[RULED, H3]`. Two compositions `[RULED R1]`: **P** = `F_canonical` = v·u·r; **H** = `F_baseline` = (v + u + r)/3, selected under the specification's arbitration clause for rival use only, a compensatory comparator never presented as satisfying zero-collapse.

**2.3 Local density.** d_i(t) = (active Moore neighbours of i at t)/8.

**2.4 Transition probabilities, from the state at t, applied simultaneously (Contract F8 §2.4 with a per-cell λ).**
- inactive → active: 1 − exp(−[η_floor + g·λ_i·d_i(t)]·Δt)
- active → inactive: 1 − exp(−μ·Δt)
No other term. The floor is not gated by any base, and floor-generated events are not masked out of density `[RULED, ruling 7]`.

**2.5 Timing and streams.** Synchronous two-phase advance, one uniform per cell per tick. **Every run has its own derived stream**, keyed by (panel master, terrain, composition, object, initialization, κ in integer micro-units, seed index); nothing is paired between arms, objects or levels `[PROPOSED]`. The uncertainty method of §5.5 assumes exactly this.

**2.6 Objects.** Realization: η_floor = η₀, stationary floor-only start; the primary object for E-A and E-B `[RULED R12]`. Skeleton: η_floor = 0, all cells active at t = 0; the structural reference and the object of E-K. Extinction is a valid observation.

**2.7 Deactivation.** μ = 0.2 (q = 0.181269; mean complete active spell 1/q = 5.5167 ticks at every cell and level, which makes that mean an implementation check and not an observable).

**2.8 Control.** Bases frozen, g swept `[RULED R5]`. For composition X on a fixed terrain, with A the Moore adjacency: B_X = diag(λ^X)·A/8; g_spec,X = q/(Δt·spr(B_X)); **κ = g/g_spec,X** `[RULED, spectral-relative gain]`. Conditions, all binding: computed from terrain arrays and adjacency before any dynamic data; raw bases, raw λ, spr, g_spec, g, κ and local m_i all persisted; never normalized by an observed onset, occupancy or fitted edge; if spr = 0 there is no finite crossing, no division and no level; raw-g values reported beside κ; the normalization is fixed for scored analysis. The crossing at κ = 1 is true by definition and is not a result. The equivalence of sweeping g and scaling λ is specific to this rule: in the Overview the spontaneous term also scales with Λ and here the floor is fixed (notation row, §10).

**2.9 Levels.** 15 values of κ in integer micro-units `[PROPOSED; range and refinement RULED, probe record §5 item 2]`: 0.75; 1.00 to 2.00 in steps of 0.10; 2.25; 2.50; 3.00. The same grid for every arm. No level is added, dropped or selected after any canonical output exists.

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
- **TB.** The product is r·(s(x)² − d(y)²), exactly additive in x and y. Criterion `[RULED]`: the product's x-share of across-cell variance lies in [0.40, 0.60], measured from the arrays. Measured: **0.5173 along x, 0.4827 along y**, interaction below 1e-15 (as probed: 0.9932 along x). The height index (2s + r)/3 varies along x only. Disclosed cost: the height index's max/min on TB is 1.16 (as probed, 1.50). Whether the H arm offers an informative boundary on TB is not known; "no informative contrast" there is a declared outcome (§7), not a defect.
- **TD `[RULED]`.** The core C is a fixed set of cells given in closed form, with no reference to λ, g or either composition: the union of n equal discs centred on cell corners, **|C| = 2,000 cells exactly** in every variant. n = 1: centre (49.5, 49.5), R = 25.3 cells. n = 4: centres (24.5 or 74.5, 24.5 or 74.5), R = 12.65 cells. No cell centre lies within 0.03 cells of the edge. Four variants, n ∈ {1, 4} × w ∈ {2, 4} cells:

| Variant | Lattice perimeter of C | Band cells (10–90% of the base step) | Band / core | Largest base step per cell |
|---|---|---|---|---|
| TD-1-2 | 200 | 676 | 0.338 | 0.146 |
| TD-1-4 | 200 | 1,376 | 0.688 | 0.074 |
| TD-4-2 | 416 | 1,424 | 0.712 | 0.143 |
| TD-4-4 | 416 | 2,816 | 1.408 | 0.074 |

  Continuum perimeters 159.0 and 317.9 cells. For both compositions C equals the set of cells whose index is at least its value at the half-height base (checked for every variant). Under P the index t³ is not symmetric across the edge. The distance function has a crease midway between discs, where the base is within 0.5% of its floor. In TD-4-4 the plateau reaches 99.75% of full height. No criterion, threshold, evaluator branch or stopping rule refers to the margins hypothesis `[RULED, H2]`.

**3.3 Which terrains can adjudicate E-A (computed from the arrays).** Two indices have the same contour family when each is a monotone function of the other across cells.

| Terrain | Same contour family for P and H? | E-A |
|---|---|---|
| T0 | trivially (both constant) | not applicable |
| TA | yes | not adjudicable here |
| **TB** | **no** | adjudicable |
| TC | **yes** — both indices are increasing functions of u alone | not adjudicable here |
| TD (all four) | yes | not adjudicable here |

On TB, a P contour lies between 14.3 and 31.5 cells from the nearest H contour, and an H contour between 14.0 and 25.0 cells from the nearest P contour (§5.5 distance; deciles of each index; Appendix A). **E-A therefore rests on TB alone.** The difference the probe saw on TC (R-6) was a difference of amplitude between the arms, and amplitudes may not be substituted for contours (Design Note v0.3 §3.6; L2 Q1 §3.5). This is item 1 of §11.

**3.4 Identities.** For every terrain the freeze commits the formula, parameters, λ ranges, spr and g_spec for both compositions, and the SHA-256 of the base arrays (Appendix A; Flight 10 may reuse the terrains). The formulas pass through cos, tanh and sqrt, and Windows and Linux math libraries are known to differ by up to one unit in the last place. **Array hashes of record are measured on the canonical machine at build `[DERIVED@BUILD]`; the container values in Appendix A are provisional, and cross-platform agreement is bound by a declared tolerance of 1e-12 per element with the deviation recorded** `[PROPOSED; the M5-6 precedent]`. The set C of TD is exact on both platforms.

## 4. Comparators (fidelity; never scored)

**4.1 Spectral crossing.** κ = 1 by construction; g_spec per arm in Appendix A. It is the zero-floor site-closure comparator; its lattice counterpart is the skeleton's finite-horizon persistence threshold κ̂_c (§5.4). The realization has activity at g = 0 and has no absorbing-state onset. The crossing is set by the leading mode of the spatial feedback operator, which may localize on a high-λ region.

**4.2 Site closure.** p_i′ = (1 − p_i)·[1 − exp(−Δt·(η_floor + g·λ_i·Σ_j A_ij·p_j/8))] + (1 − q)·p_i, iterated from p = 1 (skeleton) or p = π₁ (realization) to a fixed point: tolerance 1e-12 in max norm, at most 200,000 iterations `[PROPOSED]`. Nonconvergence is recorded as "fidelity comparator unavailable" for that arm and level and affects no endpoint. m_i = 1 is a local homogeneous benchmark, not the closure's edge.

**4.3 T0 as the lattice reference.** Flight 9's own flat arm at L = 100 on the §2.9 grid with a fresh panel, with its uncertainty and its unavailable-boundary case. Flight 8's 1.521739 is not used as a constant. T0's measured value never retunes a scored tolerance.

## 5. The instrument (package `f9`, new beside `f8`; nothing in `f8` or `e1` modified)

**5.1 N1 — rule, terrains, levels, record.** Per-cell-λ step; terrain builder with committed identities; the §2.11 record; per-tick global active count; extinction tick; survival. **Reduction requirement (apparatus):** with a constant λ array the step returns exactly the placed Flight 8 scalar step's array at equal state, effective gain, floor, μ, timing and uniforms; initialization, stream identity and observables are checked separately. M2, M4 and M6 are not carried `[RULED R11]`.

**5.2 N3 — null reference.** The floor-only stationary occupancy π₁ = 0.0523 carries analytically. No Flight 8 band, tolerance or threshold is carried.

**5.3 N5 — closure.** §4.1–§4.2 per arm.

**5.4 Skeleton survival and E-K.** survival = active count > 0 at every tail tick. κ̂_c = the lowest level with ≥ 18 of 20 surviving such that every higher level also has ≥ 18 `[PROPOSED, carried]`. E-K per §1.2.

**5.5 N-E — the composition evaluator (complete algorithm; every numbered value `[PROPOSED]`).** Applied to each realization arm at each level.
1. **Map.** p̄_i = mean over the 20 seeds of A_i(W = 1)/1,000. The endpoint scores the seed-mean map; per-seed maps are preserved and are the resampling units. (The alternative, summarizing per-seed scores, is not used: one seed's 1,000-tick map has per-cell noise several times the seed-mean map's.)
2. **Smoothing.** p̃ = the 3×3 periodic box mean of p̄ (the rule's own interaction range).
3. **Split, from occupancy alone.** θ = the split of the values {p̃_i} that maximizes between-class variance (Otsu's criterion, evaluated exactly over the sorted values). High class = {p̃_i ≥ θ}. λ, g, κ and the terrain enter nowhere in steps 1–5.
4. **Islands.** Connected components (4-neighbour, periodic) of either class with fewer than 25 cells are reassigned to the surrounding class.
5. **Edge.** E = the set of 4-neighbour bonds joining a high cell to a low cell, each represented by its midpoint.
6. **Informative-level conditions (all required; each failure has its named cause, §7).** Class means differ by at least k_C·ŝ_cell, with k_C = 5 and ŝ_cell the calibration census's median per-cell standard error of p̃ for that arm and level (§8 job 0); each class has at least 100 cells; E has at least 40 bonds.
7. **Contours.** For index Y ∈ {P, H}: candidate levels are the 99 interior percentiles of λ^Y over cells; C_Y(ℓ) = the bonds joining a cell with λ^Y ≥ ℓ to one with λ^Y < ℓ. This is where λ is thresholded: to draw the predicted contour, never the observed edge.
8. **Distance.** D(E, C) = max(95th percentile over E of the torus distance to the nearest point of C; 95th percentile over C of the distance to the nearest point of E), in cells. The distance is symmetric: an edge covering only part of a contour is not that contour.
9. **Fit.** D_Y = min over candidate levels ℓ of D(E, C_Y(ℓ)); the minimizing level is λ*_Y (fidelity, §1.2′ iv). The level is free because location is fidelity, not structure.
10. **Uncertainty.** 1,000 resamples of the 20 seed maps with replacement, from a declared evaluator stream; steps 1–9 recomputed on each. A resample failing step 6 is counted. "Within" for index Y iff the 95th percentile of resampled D_Y ≤ τ_eq = 2.0 cells. "Excluded" iff the 5th percentile > τ_ex = 4.0 cells. Otherwise "unresolved". If more than 5% of resamples fail step 6 the level is not informative (cause `unstable edge`).
11. **Why these two numbers.** One cell is the interaction range; a bond midpoint lies half a cell from either cell centre; on the noise-free TD discs (radii 12.65 and 25.3 cells) the 3×3 mean leaves the half-level contour unmoved (0.0 cells, by script). Two cells is that resolution with a margin; four cells is twice it, leaving a band in which nothing is concluded. Under an independent-chain approximation the per-cell standard error of p̄ is 0.005 to 0.008 for occupancies from 0.05 to 0.5 (Appendix A); the real value comes from the calibration census. These are declared resolutions in the sense W_res was in Contract F8 §4.5. A different pair is a different instrument.

**5.6 Outcome records and aggregation.**
- **Per arm and informative level (own = the arm's composition; rival = the other):**

| Own | Rival | Record |
|---|---|---|
| within | excluded | follows own; rival excluded |
| within | within or unresolved | follows own; identification not distinguished (or, on a same-family terrain, not adjudicable here) |
| excluded | within | follows rival (only where the families differ, §3.3) |
| excluded | excluded | follows neither |
| unresolved | any | not distinguished |

  On same-family terrains D_P = D_H up to percentile placement, and the rival column is recorded as "not adjudicable here" without computation of a verdict.
- **Arm-level E-B.** COMPATIBLE iff at least 3 levels are informative and the own record is "within" at every informative level. ADVERSE iff the own record is "excluded" at two or more adjacent informative levels. NOT DISTINGUISHED otherwise, with cause. Failure to reject is not equivalence; failure to establish either fit is not "neither".
- **Flight-level E-B, per composition X.** PRODUCED iff the arm is COMPATIBLE on TB and on at least four of the six other terrain arms (TA, TC, four TD) and ADVERSE on none. NOT PRODUCED iff ADVERSE on any terrain arm. NOT DISTINGUISHED otherwise. Every arm's record is published whatever the flight-level word.
- **E-A on TB.** DISTINGUISHED iff in both arms at least 3 informative levels carry "follows own; rival excluded" and none carries "follows rival". Otherwise NOT DISTINGUISHED with cause. "Follows rival" in an arm is published as that arm's adverse E-B record.
- **Multiplicity.** With 15 levels, 14 terrain arms and two indices, per-level error rates compound. The aggregation rules above are what the statistical qualification of §6.2 prices; the qualification's error targets are stated at the arm level and the flight level, not per level.

**5.7 Reported items (package reporting items with coverage and validity checks; values gate nothing; a missing required record prevents a claim of complete reporting).** The fidelity tier of §1.2′; the items of §1.3; the flicker record with range checks and counts of all-active and all-inactive cell-records per W; margin summaries computed afterwards from declared occupancy cuts 0.25, 0.50 and 0.75 of the map's own range, every cut reported `[PROPOSED]`, beside the W-specific floor reference.

**5.8 T0.** (i) The reduction of §5.1 is the apparatus check. (ii) Flight 8's four tests are rerun on T0 as a scientific consistency exercise with redeclared values `[PROPOSED]`: skeleton-high, skeleton-low (ρ₀ = 0.02) and realization sweeps on the §2.9 grid; survival threshold 18 of 20; f_J = 0.25 applied to increases per unit κ scaled to the 0.10 spacing; Δκ = max(0.0254, 0.0055) + 0.10 = **0.1254** (Contract F8 §3.4's procedure at N = 10,000; Appendix A); evaluability band from this flight's calibration census. Its record is PRODUCED, NOT PRODUCED or NOT DISTINGUISHED for T0 alone. An adverse or ND result there is not automatically a coding defect, gates no endpoint, and does not resolve onset continuity. If T0's boundary is unavailable, every T0-referenced fidelity item is recorded "reference unavailable".

**5.9 N7 — records, package, readiness.** The principles of Contract F8 §4.10 carry: completeness against readiness computed separately; valid adverse records; apparatus and qualification prerequisites require passage, scientific prerequisites valid completion; identity and authorization binding. The record graph is Flight 9's own (§8). Every record binds: terrain formula and base-array identity, composition, g, κ, g_spec and spr, lattice geometry, object and floor, horizon and tail, seed and stream identity, window convention, summary schema, evaluator identity and qualification identity.

## 6. Qualification of the evaluator (before any canonical scoring)

**6.1 Known-answer corpus (implementation).** Synthetic seed-map sets with constrained noise; every class returns exactly its named record and cause on ≥ 95 of 100 `[PROPOSED]`; **cross-trigger rule**: the right record with the wrong cause fails. Classes: (1) p = h(λ^P) on TB → follows own, rival excluded (P arm); (2) the same maps scored as the H arm → follows rival; (3) p = h(λ^H) on TB, both ways likewise; (4) p = h(a third function, the TB product rotated by 45°) → follows neither; (5) TA → own within, not adjudicable here; (6) constant map → `no contrast`; (7) a high class of 50 cells → `under-resolved`; (8) an edge displaced 3 cells from a contour → not distinguished; (9) noise raised until the edge fails resampling → `unstable edge`. An independent-response map (class 1) is correctly a pass: it satisfies the tested property (§1.4).

**6.2 Statistical qualification (design and held-out ensembles) `[RULED in principle, ruling 4; sizes PROPOSED]`.** Generator truth independent of the evaluator: 20 seed maps per case, each h(index) plus spatially correlated noise whose per-cell amplitude and correlation length are taken from the calibration census `[DERIVED@BUILD]`. The independent unit is the seed map. The six risks of Design Note v0.3 §10.1 are the classes: false identification (TA-type and rival-generated cases); vacuous support (constant, empty-edge, saturated, singleton-contour, low-contrast); false adverse (truly compatible maps under correlated noise at the calibration amplitude and at 1.5 times it); improper ND (sufficiently discriminating cases must keep their record); aggregation (whole synthetic sweeps of 15 levels scored by §5.6's arm rule, and whole synthetic flights by the flight rule); wrong cause. 200 cases per class in each ensemble; applicable error per class with one-sided 95% Clopper–Pearson upper bound ≤ 0.10 (at most 12 errors in 200); halts counted as errors; design AND held-out joined mechanically; the held-out master is drawn only after the generator, classes, counts and caps are frozen. A failed qualification closes the stage; no same-stage repair. Guarantees hold for the declared ensembles only and do not transfer automatically to the lattice.

## 7. Failure paths, with precedence (highest first)

| # | State | Kind | Cause label | Effect |
|---|---|---|---|---|
| 1 | Run halts; record missing, corrupt or out of range | apparatus | `apparatus unevaluable (<key>)` | level unevaluable; arm NOT DISTINGUISHED (apparatus); never adverse |
| 2 | Skeleton run extinct | valid observation | — | enters E-K and κ̂_c; never "missing" |
| 3 | Class means closer than k_C·ŝ_cell (includes floor-dominated and saturated maps) | scientific ND | `no contrast` | level not informative |
| 4 | A class under 100 cells, or under 40 edge bonds | scientific ND | `under-resolved` | level not informative |
| 5 | Over 5% of resamples fail step 6 | scientific ND | `unstable edge` | level not informative |
| 6 | Fewer than 3 informative levels | scientific ND | `insufficient informative levels` | arm NOT DISTINGUISHED |
| 7 | Own unresolved | scientific ND | `finite resolution` | level not distinguished |
| 8 | Own excluded at one isolated level | scientific ND | `isolated exclusion` | arm NOT DISTINGUISHED unless rule 9 applies |
| 9 | Own excluded at two or more adjacent informative levels | scientific adverse | `boundary not a level set of own index` | arm ADVERSE |
| 10 | Site closure does not converge | fidelity unavailable | `comparator unavailable` | fidelity item only |
| 11 | T0 boundary unavailable | fidelity unavailable | `reference unavailable` | T0-referenced fidelity items only |

No failed terrain is dropped, no level is selected after the fact, and every state is preserved in the package. An adverse result is never recast as fidelity or ND. Precision ceiling and stop path `[PROPOSED]`: if the calibration census shows ŝ_cell > 0.02 at any arm and level, the stage stops before any canonical census and a new instrument version is declared; the sample size of this stage is never changed after data exist.

## 8. Jobs, order, authorizations

Order: Appendix A computed → freeze → instrument version identity → reduction check → known-answer corpus → masters drawn → job 0 → statistical qualification (design, then held-out, then joined) → **passage required** → canonical scientific jobs. Each job runs only under a Mike-issued authorization naming the stage and the jobs; one authorization per step; the registry is append-only; each authorization file gets one commit.

| # | Job | Kind | Content |
|---|---|---|---|
| 0 | `calibration_census` | apparatus prerequisite, never scored, never reused | all 15 arms × 2 objects × 15 levels × 20 seeds under its own master (9,000 runs); gives ŝ_cell, the noise parameters of §6.2 and the §7 ceiling |
| 1 | `evaluator_known_answer`, `evaluator_design_audit`, `evaluator_held_out_audit`, `evaluator_qualification` | qualification | §6 |
| 2 | `t0_census` | scientific (consistency) | T0, three sweeps (900 runs); §5.8 |
| 3 | `skeleton_census` | scientific | 14 terrain arms, skeleton (4,200 runs); E-K, κ̂_c |
| 4 | `realization_census` | scientific | 14 terrain arms, realization (4,200 runs); E-A, E-B |
| 5 | `census_stability` | scientific | jobs 3–4 on an independent panel (8,400 runs); arm-level records reproduced or not, reported |
| 6 | `fidelity_report`, `flicker_report`, `margin_report` | reporting | §1.2′, §1.3, §5.7 |
| 7 | `resource_benchmark`, `stage1_package` | apparatus / package | as Flight 8's grammar |

Arms: T0·P, and P and H on each of TA, TB, TC, TD-1-2, TD-1-4, TD-4-2, TD-4-4 (15). In the container probe at L = 100 a realization run took 0.96 s and a skeleton run 0.62 s on average, so the 9,000-run census set is about 2.0 hours there; the canonical machine is unmeasured `[DERIVED@BUILD, resource benchmark]`. Instrument version string `f9_stage1_v1` `[PROPOSED]`.

## 9. Declarations table

| Declaration | Value | Marker |
|---|---|---|
| L, N | 100; 10,000 | RULED |
| Compositions | P = `F_canonical`; H = `F_baseline` (rival only) | RULED |
| η₀; μ; Δt | −ln(0.99); 0.2; 1 | RULED (carried) |
| Control | bases frozen, g swept, κ = g/g_spec,X | RULED |
| κ grid | 0.75; 1.00–2.00 by 0.10; 2.25; 2.50; 3.00 (15) | PROPOSED (range and refinement RULED) |
| T, tail; seeds | 3,000 / 1,000; 20 | PROPOSED (carried) |
| Streams | every run its own; nothing paired | PROPOSED |
| Terrains T0, TA, TC | probed formulas | RULED |
| TB | §3.1; x-share criterion [0.40, 0.60]; measured 0.5173 | RULED |
| TD | §3.2; \|C\| = 2,000; n ∈ {1, 4} × w ∈ {2, 4}; concordant | RULED |
| Flicker record | §2.11 | RULED (pre-probe declaration §6) |
| Scored map | seed-mean W = 1 occupancy, 3×3 mean | PROPOSED |
| Split; islands | Otsu on occupancy; components < 25 cells reassigned | PROPOSED |
| Informative level | k_C = 5; ≥ 100 cells per class; ≥ 40 bonds | PROPOSED |
| Contour candidates; distance | 99 percentiles; symmetric 95th-percentile distance | PROPOSED |
| τ_eq, τ_ex | 2.0, 4.0 cells | PROPOSED |
| Resamples; one-sided level; instability limit | 1,000; 95%; 5% | PROPOSED |
| Arm rule | ≥ 3 informative levels; ADVERSE at two adjacent exclusions | PROPOSED |
| Flight rule for E-B | TB and ≥ 4 of 6 others COMPATIBLE, none ADVERSE | PROPOSED |
| E-A | TB only; ≥ 3 levels "follows own; rival excluded" in both arms | PROPOSED |
| E-K | skeleton, 18 of 20; recorded beside E-B | PROPOSED |
| T0 exercise | Δκ = 0.1254; f_J = 0.25; ρ₀ = 0.02 | PROPOSED |
| Known-answer; qualification | ≥ 95/100, cross-trigger; 200 per class, cap 0.10, CP 95% | PROPOSED |
| Precision ceiling | ŝ_cell ≤ 0.02, stop path | PROPOSED |
| Site closure solver | start p = 1 or π₁; 1e-12; 200,000 iterations | PROPOSED |
| Array identity tolerance | 1e-12 per element across platforms; canonical hashes of record | PROPOSED |
| Margin cuts | 0.25, 0.50, 0.75 of the map's range | PROPOSED |
| g_spec, spr, λ ranges, base-array hashes | Appendix A | DERIVED@FREEZE (hashes DERIVED@BUILD) |
| Masters (calibration, canonical, stability, design, held-out, evaluator) | drawn after freeze | DERIVED@BUILD |
| Instrument version | `f9_stage1_v1` | PROPOSED |

## 10. Notation rows to append (append-only; the table governs)

| Object | O — Overview v1.8.1 | C — this contract | Nature |
|---|---|---|---|
| Spectral-relative gain | Λ/Λ* (implicit) | κ = g/g_spec,X; equals Flight 8's m on a flat terrain | C-only |
| Sweeping g against scaling Λ | the spontaneous term scales with Λ | the floor is fixed; g and λ enter only as g·λ_i | rule-specific equivalence; not interchangeable in every channel |
| Observed boundary | activation surface Λ = Λ* (PD7) | iso-occupancy contour of §5.5 | instrument-level bridge, C-only |
| Compositions | F (open) | P = `F_canonical`, H = `F_baseline` (rival only) | prescribed inputs; no selection claimed |

## 11. For Mike's ruling before this draft goes to L2

1. **TC cannot adjudicate E-A; E-A rests on TB alone (§3.3).** Recommended: keep the grammar as fixed; TC serves E-B and the reported near-face contrast. The alternatives are a declared amplitude endpoint for TC, which would be an outcome-informed redesign needing your ruling and a fresh validation boundary, or a second two-profile terrain, which would be unprobed.
2. **E-K's standing (§1.2):** recorded beside E-B and not conjoined, as drafted; or conjoined; or reported only.
3. **The bridge of §1.2″:** the observed boundary is an iso-occupancy contour at a split chosen from occupancy alone.
4. **The edge rule of §5.5 steps 1–6:** seed-mean map, 3×3 mean, Otsu split, 25-cell islands, the informative-level conditions.
5. **The distance, the free level, and τ_eq = 2.0, τ_ex = 4.0 cells (§5.5 steps 7–11).**
6. **Uncertainty by resampling seeds, 1,000 resamples, one-sided 95%.**
7. **Aggregation (§5.6):** the arm rule, the flight rule for E-B, and E-A's rule.
8. **The κ grid of 15 levels (§2.9).**
9. **Independent streams everywhere; score the seed-mean map (§2.5, §5.5 step 1).**
10. **Qualification sizes (§6):** nine known-answer classes at ≥ 95/100; 200 cases per class, cap 0.10.
11. **Failure-path precedence and the ŝ_cell ≤ 0.02 stop path (§7).**
12. **The T0 exercise as redeclared (§5.8), Δκ = 0.1254, gating nothing.**
13. **The job list and `census_stability` on an independent panel (§8).**
14. **Array identities: canonical-machine hashes of record with a 1e-12 cross-platform tolerance (§3.4).**
15. **Both compositions run on all four TD variants** (eight arms that cannot adjudicate E-A), as drafted; or P only on TD.
16. **Reported-only items and the margin cuts (§1.3, §5.7).**
17. **Carried values re-declared here:** T = 3,000, tail 1,000, 20 seeds, survival 18 of 20, version string.

## 12. Requirements carried from L2's consultation (every REQUIRES CHANGE item)

| L2 item | Where |
|---|---|
| Q1 two conditional tests; boundary against whole map; independent edge; no vacuous support; uncoupled alternative disclosed; TA's role; six labels | §1.2, §1.3(a), §1.4, §5.5–§5.6, §7 |
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

T0 is run under P only; its H row is shown for completeness.

**A.2 TB contour separation (§5.5 distance, cells; nearest contour of the other index).** P contour at its deciles 10…90: 31.5, 24.2, 20.5, 19.0, 18.0, 14.5, 14.3, 17.6, 24.6. H contour at its deciles: 25.0, 23.0, 21.3, 20.0, 19.0, 16.5, 14.0, 15.0, 16.6. On TA, TC and TD-4-2 the same computation gives 0.0 at every decile.

**A.3 Rule constants.** q = 0.181269; a = 0.01; π₁ = 0.052282; 1/q = 5.516656; floor-only probability of any activity in W ticks: 0.052282 (W = 1), 0.134244 (10), 0.649601 (100).

**A.4 T0 bracket at N = 10,000.** Lower term ln N/(q·2,000) = 0.0254; upper term (N·ρ*_sk ≥ 50, bisection on the Flight 8 map) = 0.0055; Δκ = 0.0254 + 0.10 = 0.1254.

**A.5 Per-cell standard error of p̄, independent-chain approximation only (20 seeds × 1,000 ticks).** 0.0048 at p = 0.0523; 0.0063 at 0.1; 0.0079 at 0.2; 0.0084 at 0.3; 0.0075 at 0.5. The calibration census replaces these.

**A.6 Run counts.** 15 arms × 2 objects × 15 levels × 20 seeds = 9,000 per full panel; T0 low-initialization sweep 300.

*L1 (Claude Fable 5.2), v0.1, 2026-11-12.*
