# Flight 9 — Design Note v0.1 (design chamber; not a contract)

**Status.** L1 design draft, 2026-11-12, at Mike's word ("kick off Flight 9 design", then "go"). Repository `main` at `9d3a23bac0691c39ee74a7e9eeedc111574bf82a`, read from a fresh clone. This note binds nothing. No contract text is drafted until Mike rules on §11.
**Register.** No lattice run, probe or ensemble was made for this note. The only computed numbers are two constants of the frozen Flight 8 rule (§7), computed by script from μ = 0.2 and η₀. Every Flight 8 figure is quoted from the close record (`F8_STAGE1_CLOSE_RECORD_v1_0.md`, `194886e89f55a4c7…`).
**Scope, fixed by Mike.** Flight 9 is terrain and composition. Regime II, Ψ and any coherence observable wait for Flight 10. The order is not open.
**Release of the hold.** Contract F8 §7.3 item 5 held the heterogeneous-base run for "a successor stage". L2's consultation of 2026-11-12 says the Flight 8 close is not "automatic clearance" of that work. Mike's instruction of 2026-11-12 is recorded here as the release for design only. The third-order lattice-versus-ODE comparison stays held (contract F8 §3.5).
**Notation.** Contract F8 names carry: μ is the deactivation rate (the Overview's lapse rate β, not the Overview's μ(ρ)); g the feedback gain; η_floor the spontaneous floor as a per-tick hazard, committed value η₀; λ_i per-cell conduciveness; d_i the Moore active fraction; q = 1 − e^(−μΔt). The bases are written v, u, r as in the frozen specification.

---

## 1. Mike's held items for Flight 9 (the note's fixed points)

**H1. The composition claim is adjudicated, not illustrated.** Both compositions are tested on terrains where activation following the product's sheet and activation following a height-like index give different predictions.

**H2. Terrains carry varied margin-to-core ratios**, so that the margins hypothesis (coherence carried by the flickering margin) stays testable in Flight 10. That hypothesis is never built into the instrument.

**H3. The boundary of this flight.** Heterogeneity is between cells only: one action stream per cell, bases differing from cell to cell. Many streams per cell is its own later flight. Within-cell heterogeneity stays reserved.

Everything below serves these three, plus the three obligations from the Flight 8 close (§7, §8, §9).

## 2. What Flight 8 leaves, and what it does not

| Source | What it fixes or leaves open for Flight 9 |
|---|---|
| Close record §2 | P1 PRODUCED on the homogeneous 50×50 lattice; finite-horizon persistence boundary m̂_c = 1.521739. |
| Close record §3 | T-S1c's domain starts at m̂_c; continuity through the onset is untested. Fidelity: m̂_c is 0.521739 above the closure's m = 1. |
| Close record §7 | Three obligations forward: the flicker observable (Interpretation 004); two next-touch repairs (held); the onset-continuity question, "nothing here authorizes it". |
| Interpretation 004, point 4 | The successor contract must declare, before any data: the statistic's definition, the window set W, the levels at which it is taken, and what the instrument persists. |
| Contract F8 §2.4 | The hazard rule. All conduciveness enters through g·λ_i·d_i; the floor does not depend on the bases. |
| Contract F8 §3.5 | The spectral crossing (leading eigenvalue of gΔt·diag(λ_i)·A/8 + e^(−μΔt)·I reaching 1) is pre-registered as the comparator for the heterogeneous run, not as a P1 test. |
| E1-R diagnosis | F is inert under homogeneous bases. Flight 8 said nothing about how the bases compose. |
| Placed `f8/dynamics.py` | The step takes one scalar `lambda_bar`, and the config refuses anything but homogeneous bases. Flight 9 needs a new rule module with a per-cell λ array. |
| Frozen spec v0.4 §2.1 | Four committed F labels: `F_canonical` = v·u·r; `F_2_symmetric` = (v·u·r)·(weighted mean), Flight 8's label; `F_LR` = min(v, u, r); `F_baseline` = (v + u + r)/3, "legacy-unused; no contract selects it without arbitration". |

## 3. The composition claim: what a lattice can and cannot adjudicate

**3.1 The difficulty, stated first.** F is an input to the rule. If the instrument runs the product rule, each cell's activation hazard follows the product at that cell by construction. A test that only checks "activation follows the composition we coded" can be passed without the lattice doing anything. Under the program's pessimistic-on-passing principle that test is not strong enough, and H1 asks for more than it.

**3.2 What is not by construction.** Activation of a cell depends on its own λ_i and on its neighbours' activity. The realized active region is therefore a collective outcome. It can depart from a level set of λ in at least three ways: the edge sits at a local value above the closure's (Flight 8's shift); a convex stretch of edge has fewer active neighbours than a concave one, so the edge need not follow a contour where the contour bends; a small or isolated high-λ patch can fail to persist at all. Whether, and down to what terrain scale, the realized activation surface is a level set of the composed quantity is a question the lattice answers and can answer adversely.

**3.3 Two candidate readings of "the composition claim" (for ruling, R2).**
- **(a) Discrimination.** Run the rule under each composition on the same terrain. On a discriminating terrain the two runs must yield different activation patterns, each ordered by its own composition and not by the other. This establishes that the collective record distinguishes a product-composed lattice from a height-composed one, and it identifies the signature that does so. Its failure indicts the instrument or the terrain more than the theory.
- **(b) Level-set claim.** Under a given rule, the realized activation surface is a level set of that rule's λ within a declared resolution. This is PD7's "the boundary is the activation surface Λ = Λ*" read at the lattice level. It can fail validly.

L1's recommendation: score both, as separate tests, with (b) the substantive one. Reading (a) alone would be close to illustration.

**3.4 Which two compositions (R1).** The committed record does not name them. L1's proposal:
- **Product:** `F_canonical` = v·u·r. It is the plain product of Mike's phrase, and it carries the Overview's zero-collapse property (any base at zero gives λ = 0). `F_2_symmetric` was Flight 8's label, but F was inert there, so nothing in Flight 8 depends on the choice.
- **Height-like index:** `F_baseline` = (v + u + r)/3. It is compensatory: a base at zero does not annihilate. It contradicts zero-collapse and enters as the rival index, not as a candidate of the theory. The spec bars selecting it "without arbitration"; Mike's ruling on R1 would be that arbitration, for use as a rival only.
- `F_LR` (min) is zero-collapsing but not height-like. It could be a third arm later. L1 does not recommend it for Flight 9.

**3.5 Discriminating terrains.** A terrain discriminates where the two indices order cells differently. By script: (0.9, 0.9, 0.1) has product 0.081 and height 0.633; (0.5, 0.5, 0.5) has product 0.125 and height 0.5. The first cell is higher, the second has the larger product. Proposed terrain types, all smooth, periodic and closed-form (R3):
- **T0, flat.** Homogeneous bases. Flight 9's own reference on its own instrument and lattice size.
- **TA, concordant.** All three bases rise and fall together, so both indices order cells identically. A negative control: the composition tests must return "not adjudicable here". An instrument that names a winner on TA is defective.
- **TB, cross-gradient.** r constant; v + u varies along one axis and v − u along the other. Height contours are straight lines; product contours bend away from the imbalanced cells. Opposite predictions for cells of equal height and unequal balance.
- **TC, zero-collapse.** One base near zero over a patch whose other two bases are high. The height rule predicts an active patch; the product rule predicts a hole.
- **TD, margin variants.** See §5.

**3.6 Form of the scored tests (R4).** Following Flight 8's option (a), the scored tests are structural and the locations are fidelity. Proposed observable: per-cell tail occupancy (fraction of tail ticks active), seed-median per cell. Proposed statistic: constancy of occupancy along pre-declared contours of each index. Under rule X on TB, occupancy should be constant along X's contours and vary along the other index's. Outcomes per terrain and rule: follows own index / follows the rival / follows neither / not distinguished. "Follows the rival" and "follows neither" are valid adverse outcomes. Estimator, resolution and bands are contract matters.

## 4. The control coordinate on a terrain (R5)

In Flight 8 a level set λ̄ through the homogeneous base and g stayed at 1. On a terrain, scaling the bases is not a uniform scaling of λ: scaling every base by c multiplies the product by c³ and the height by c, so the terrain's shape would change with the level and differently per composition.

Proposal: **the terrain's bases are frozen and the sweep variable is g.** The rule depends on g and λ only through g·λ_i, so this is the same family of rules. Each cell then has a local coordinate m_i = g·λ_i·Δt/q at each level. A notation row is needed, because the Overview holds g₀ fixed and moves Λ; the table would record that sweeping g is equivalent in this rule.

Open inside R5: the two compositions give different λ ranges on the same bases, so their sweeps need a declared common normalization (candidates: equal spectral crossing; equal mean λ).

## 5. Margins: terrains laid for Flight 10, nothing built in (R6)

**5.1 What "never built into the instrument" means here.** No criterion, threshold, evaluator branch, terrain-selection rule or stopping rule refers to the margins hypothesis. The instrument records the same per-cell summaries for every cell. Any core/margin partition is computed afterwards from declared cuts, and is reported under more than one declared cut so that no single partition is privileged.

**5.2 Design-side ratio (from terrain geometry only).** Two knobs: the length of the edge relative to the enclosed area (compact patch, elongated patch, several small patches of equal total area), and the steepness of λ across the edge (a gentle slope gives a wide band of intermediate local m_i; a steep one gives a narrow band). Terrain family TD varies both, at fixed total core area.

**5.3 Measured-side ratio.** From the per-cell tail summaries of §7. Reported, never tested in Flight 9: there is no coherence observable to relate it to.

**5.4 For Flight 10.** Terrain identities (formula, parameters, hash of the base arrays) are committed at freeze so Flight 10 can reuse the same terrains.

## 6. Confirming the boundary (R7)

One stream per cell. Heterogeneity is in the frozen bases between cells and nowhere else. Bases frozen in time, Q off, Γ = 0, drive zero, noise off, synchronous Moore timing, W = 1 tick as the participation window: all carried from Contract F8 §2. No per-cell stream count, no within-cell heterogeneity.

## 7. Flicker observable — discharge of Interpretation 004 (R8)

**7.1 Mike's intent.** Discharge it cheaply: persist per-cell tail summaries (time active, number of switches), not state histories; declare one run-length statistic from them, recorded and not tested; no further design effort unless the theory gives it a prediction; the same summaries serve as the measured margin.

**7.2 A fact about the frozen rule that bears on this.** Deactivation is a constant hazard, the same for every cell at every level (contract F8 §2.4). At W = 1 tick, the lengths of a cell's active spells are therefore geometric with mean 1/q = 5.517 ticks (by script) everywhere on every terrain. Three consequences:
- At W = 1 every cell switches constantly. There is no set of cells that flickers while others do not. The margin is not "where cells flicker"; it is where occupancy is intermediate.
- The number of switches adds little to time active: in expectation the number of active spells is occupancy × q × tail length. The mean active-spell length from the two summaries (time active ÷ spells) is a check that the instrument implements the rule, not a scientific observable.
- The information at W = 1 is in the inactive spells, whose mean is (tail − time active) ÷ spells.

**7.3 The W question.** Contract F8 §1.3(b) reads "across windows W", and the PD record's held candidate is that run-length statistics be resolution-invariant across a range of W near Λ*. Summaries at W = 1 alone meet Interpretation 004's letter (the window set is declared as the single tick) and make the held candidate untestable from Flight 9's record. At coarser W the picture changes: a high-occupancy cell is active in nearly every window and stops switching, and a low-occupancy cell does not. That is where a margin that "flickers" could be seen.

**7.4 Options.**
- **(a)** W = {1 tick} only, as Mike stated. Cheapest. The held probe candidate stays held and unserved.
- **(b)** The same two summaries at a small declared window set, proposed W ∈ {1, 10, 100} ticks (100 is the existing tail window). Per cell and run: windows with any activity, and switches of the windowed series. Six integers per cell per run. Still summaries, no state history.

L1's recommendation: (b). The added cost is storage of a few integers; it keeps the held candidate servable without any design effort now, and it gives the measured margin at more than one resolution. The declared statistic under either option: per-cell mean inactive-spell length at each W, reported as its distribution over cells by occupancy band. Recorded, not tested. Taken at every level and run, since "near the boundary" on a terrain is a place present at every level. No further design effort unless the theory gives it a prediction.

## 8. Onset continuity (R9)

T-S1c never tested the rise into m̂_c (close record §3). Put to Mike: does Flight 9 carry a prospective onset-continuity test, or is it left to its own flight?

- **(a) In Flight 9**, as extra levels on the flat terrain T0 over a declared domain around m̂_c.
- **(b) Its own stage on the homogeneous instrument** (Contract F8 §1.2 already names the remedy: "a finer grid in a successor stage").
- **(c) Its own later flight.**

L1's recommendation: not in Flight 9; (b) or (c), timing at Mike's word. Reasons:
1. On a terrain the onset is spread out, because cells cross at different levels. Terrain runs cannot answer the question, so only the flat arm could, and it would be a second experiment inside the contract.
2. A finer grid alone does not settle it. On a finite absorbing lattice the fraction of surviving seeds rises from 0 to 20 of 20 over a band of levels (0 and 7 of 20 at the two levels below m̂_c, 20 of 20 at m̂_c), and seed medians mix extinct and surviving runs there. An honest test needs a declared treatment of survivors and probably more than one lattice size. That is real design work of a different kind from terrain work.
3. Nothing in Flight 9 or Flight 10 depends on its answer.

## 9. Fidelity: what "the predicted boundary" means on a terrain (R10)

In Flight 8 the closure gave one number, m = 1, and the lattice boundary sat 0.521739 above it. On a terrain the closure no longer gives one number. "The boundary" divides into two objects:

- **A threshold in the control:** the level at which anything persists. The closure's value is the spectral crossing of contract F8 §3.5, one number per terrain and composition. On a terrain it is governed by the best patch.
- **A surface in space at each level:** the edge of the active region. The closure's prediction is the fixed point of the site-by-site mean-field map (each cell's density from its own λ_i and its neighbours' densities), which is a predicted occupancy map, not a number. Its simplest summary is the contour m_i = 1.

Proposed fidelity tier, reported with signs and bands and never scored:
1. measured onset level against the spectral crossing;
2. the distribution of local m_i over the cells on the measured edge, against 1 (closure) and against the flat arm's own measured boundary on the Flight 9 instrument;
3. per-cell occupancy against the site mean-field map.

L1 proposes the flat arm T0 as the lattice reference in item 2, not Flight 8's 1.521739. It is measured on the same instrument and lattice size, it is declared before any data, and it keeps Flight 8's data out of Flight 9's comparators. The composition tests of §3.6 use orderings and contours only and do not depend on this tier.

## 10. Instrument, objects, size, review (R11–R15)

**10.1 Carry-over (R11).** New package `f9` beside `f8`; nothing in `f8` or `e1` modified. Proposed:

| Flight 8 module | Flight 9 |
|---|---|
| M1 rule and levels | New rule module with per-cell λ; terrain builder with committed identities; per-cell tail summaries (§7) |
| M2, M4, M6 (detection classifier, verdict router, morphology audit) | **Not carried.** In Flight 8 no verdict of this apparatus bore on P1 and its expected label was fixed in advance. Rebuilding and re-qualifying it for terrains would have no effect on any Flight 9 claim. |
| M3 null | Carried as the reference occupancy (the floor-only chain; stationary density 0.0523) |
| M5 closure | Extended: site mean-field map and spectral crossing per terrain |
| M-P1 evaluator | Replaced by a composition evaluator with its own known-answer corpus (must-pass, must-fail, must-yield-ND, cross-trigger rule) |
| M7 records and package | Grammar carried unchanged |

**10.2 Objects (R12).** Skeleton (η_floor = 0) and realization (η₀). On a terrain the active population can be a few hundred cells, so chance extinction of the skeleton within the horizon is far more likely than in Flight 8. Proposal: the realization is the primary object for the composition tests; the skeleton runs as a structural reference with extinction a valid observation. Whether Flight 8's four tests are rerun on T0 as a regression of the new instrument is part of this item; L1 recommends yes, on T0 only.

**10.3 Size, horizon, seeds (R13).** Smooth terrains with distinct patches and varied edges are cramped at L = 50. Proposal: price L = 100 against L = 50 in the contract draft before choosing. Terrains are deterministic; the 20 seeds vary the dynamics only. Fresh masters; none of Flight 8's reused.

**10.4 A pre-contract probe (R14).** Flight 8's claim grammar was decided after a noncanonical probe whose result was known before the ruling (contract F8 §1.0). For Flight 9, Mike rules in advance whether L1 may run a noncanonical terrain probe to size terrains and check that TB and TC separate, with the same provenance discipline, or whether the contract is drafted without one.

**10.5 Review path (R15).** As Flight 8: this note → Mike's rulings → contract register → L2 contract packets → Gemini audit before freeze (commission v3 in force; v3.1 held) → freeze. The triage's note on authorization records (`authorized_jobs` reads as the whole grant) stays held with v3.1.

## 11. Rulings needed from Mike before the contract is drafted

| # | Item | L1's recommendation |
|---|---|---|
| R1 | The two compositions (§3.4) | `F_canonical` as the product; `F_baseline` as the height-like rival, arbitrated for rival use only |
| R2 | What "the composition claim" is (§3.3) | Score both discrimination and the level-set claim, separately; the level-set claim is the substantive one |
| R3 | Terrain family T0, TA, TB, TC, TD; smooth, periodic, closed-form (§3.5) | As proposed |
| R4 | Structural scored tests on orderings and contours; locations to fidelity (§3.6) | As proposed |
| R5 | Bases frozen, sweep g; local coordinate m_i; common normalization across compositions (§4) | Sweep g; normalization priced in the contract draft |
| R6 | Margin-to-core: geometry-defined on the design side, summary-defined on the measured side, several cuts, nothing tested (§5) | As proposed |
| R7 | Boundary: between-cell heterogeneity only (§6) | Confirm |
| R8 | Flicker discharge: W = {1} or W = {1, 10, 100}; the declared statistic (§7) | W = {1, 10, 100}; mean inactive-spell length; recorded, not tested |
| R9 | Onset continuity: in Flight 9, its own stage, or its own flight (§8) | Not in Flight 9 |
| R10 | Fidelity on a terrain: two objects, three reported comparisons, flat arm as lattice reference (§9) | As proposed |
| R11 | Carry-over; M2/M4/M6 not carried (§10.1) | As proposed; L2 will be asked to attack the omission |
| R12 | Realization primary, skeleton as reference; Flight 8's four tests rerun on T0 (§10.2) | As proposed |
| R13 | Lattice size priced at 50 and 100; deterministic terrains; fresh masters (§10.3) | As proposed |
| R14 | Pre-contract noncanonical terrain probe: allowed or not (§10.4) | Allowed, with a dated provenance paragraph in the contract |
| R15 | Review path (§10.5) | As Flight 8 |

## 12. Held, nothing authorized by this note

Gemini commission v3.1. The two next-touch repairs of close record §7.2: the direct-DIP docstring in `test_f8_m6.py` and the stale comment in `test_f8_mp1.py`. The third-order lattice-versus-ODE comparison. Overview v1.8.2.

## 13. What this note is not

Not a contract, not an authorization, not a result. It proposes readings, terrains and tests for Mike to rule on and L2 to review. It makes no statement about Regime II, Ψ or coherence. Flight 8 stage 1 stays closed as recorded.

*L1, 2026-11-12.*
