# Flight 9 — Design Note v0.3 (design chamber; not a contract)

**v0.3, 2026-11-12 — supersedes v0.2 (`aabd30fcd53477bf`, retained beside this file).** Records L2's design consultation of 2026-11-12 (`L2_F9_DESIGN_CONSULTATION_2026-11-12_RECEIVED.md`, `65d95bc3a907cf04…`, beside this file; overall disposition REQUIRES CHANGE) and Mike's ruling on it of the same date ("accept all as recommended", on L1's eight recommendations, §12). Sections 3, 4, 5, 7, 8, 9 and 10 are revised accordingly; §13 lists the three errors of L1's that L2 found. Sections 1, 2 and 6 are v0.2's text, with one reading line added under H1.

**Status.** L1 design draft at Mike's word. Repository `main` at `817450e39682d1c5d43bd787b8971ba3a9e0c7fc` when written. This note binds nothing beyond the rulings recorded in §11 and §12. No contract text is drafted and no probe is run until Mike has ratified the pre-probe declaration of §10.4.
**Register.** No lattice run, probe or ensemble has been made for Flight 9. Computed numbers in this note are constants of the frozen Flight 8 rule and analytical null probabilities, by script. Flight 8 figures are quoted from the close record (`194886e89f55a4c7…`).
**Scope, fixed by Mike.** Flight 9 is terrain and composition. Regime II, Ψ and any coherence observable wait for Flight 10. The order is not open.
**Release of the hold.** Contract F8 §7.3 item 5 held the heterogeneous-base run for "a successor stage". Mike's instruction of 2026-11-12 is recorded as the release for design only. The third-order lattice-versus-ODE comparison stays held (contract F8 §3.5).
**Notation.** Contract F8 names carry: μ is the deactivation rate (the Overview's lapse rate β, not the Overview's μ(ρ)); g the feedback gain; η_floor the spontaneous floor as a per-tick hazard, committed value η₀; λ_i per-cell conduciveness; d_i the Moore active fraction; q = 1 − e^(−μΔt). Bases are v, u, r as in the frozen specification. New in this note: κ, the spectral-relative gain (§4).

---

## 1. Mike's held items for Flight 9 (the note's fixed points)

**H1. The composition claim is adjudicated, not illustrated.** Both compositions are tested on terrains where activation following the product's sheet and activation following a height-like index give different predictions.
*Reading ruled 2026-11-12 on L2's return:* what the lattice can adjudicate is the pair of conditional results in §3.3. No lattice result selects which composition describes entrepreneurial ecosystems.

**H2. Terrains carry varied margin-to-core ratios**, so that the margins hypothesis (coherence carried by the flickering margin) stays testable in Flight 10. That hypothesis is never built into the instrument.

**H3. The boundary of this flight.** Heterogeneity is between cells only: one action stream per cell, bases differing from cell to cell. Many streams per cell is its own later flight. Within-cell heterogeneity stays reserved.

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
| Frozen spec v0.4 §2.1 | Four committed F labels: `F_canonical` = v·u·r; `F_2_symmetric`, Flight 8's label; `F_LR` = min(v, u, r); `F_baseline` = (v + u + r)/3, "legacy-unused; no contract selects it without arbitration". |

## 3. The composition claim

**3.1 The difficulty.** F is an input to the rule. A test that only checks "activation follows the composition we coded" can be passed without the lattice doing anything.

**3.2 Where the adverse room is (corrected, L2 Q1).** Equal local λ does not imply equal neighbour activity. Sites of equal λ in different neighbourhoods can have different occupancy; a measured boundary can contain λ values whose spread exceeds a declared tolerance; an isolated high-λ patch can fail to sustain activity while a lower-λ, better-supported region persists. These are possible mechanisms, argued from the rule; nothing has been run. Two items v0.2 listed are withdrawn: a uniform shift of the whole edge is still a level set and belongs to fidelity, and extinction of a whole run leaves no boundary to test.

**3.3 The two conditional tests (ruled).**
- **(a) Conditional discriminability.** On pre-declared informative terrains and levels, the spatial records distinguish the two prescribed input rules at the declared resolution. A pass establishes a distinguishable output consequence of changing the composition in the instrument, and nothing about which composition describes ecosystems. A failure can mean an uninformative terrain, insufficient resolution or a truly indistinguishable output.
- **(b) Conditional boundary compatibility — the scored substantive endpoint.** Under each prescribed rule, an independently defined observed boundary can, or cannot, be represented by a level set of that rule's local λ at declared spatial and statistical resolution. A valid failure says the local-scalar description fails for that rule, terrain, object, size, horizon and resolution. A pass is compatibility within that scope. PD7 supplies the activation-surface commitment; its mapping to a finite occupancy boundary is an instrument-level bridge the contract must state.
- **Reported only:** constancy of the whole occupancy map along contours (p_i = h(λ_i)). It is a stronger proposition than (b), is not a commitment of the theory, and is not scored.

The observed edge is defined independently of λ and never by thresholding λ. Empty, full, floor-dominated, saturated or under-resolved maps earn no support through small residuals.

**3.4 An alternative that passes both tests without coupling (disclosed; L2 Q1).** Independent two-state cells with activation hazard η₀ + g·d₀·λ_i for a fixed constant d₀ > 0 have stationary occupancy that is an increasing function of λ_i alone. Such cells have no neighbourhood interaction, are constant on the index's contours, and give different product and height patterns on a discriminating terrain. A pass of (a) and (b) therefore does not establish coupling-supported regional activation. The floor-only null does not exclude this alternative and neither does terrain TA.
*L1's proposal for the contract, not yet put to L2:* the skeleton arm is the coupling-sensitive contrast. At η_floor = 0 the alternative has no absorbing state and no persistence threshold, and the coupled rule has both. No third scientific arm is added.

**3.5 The two compositions (R1; L2 Q3, acceptable in principle).** Product: `F_canonical` = v·u·r. Rival: `F_baseline` = (v + u + r)/3, selected by Mike's ruling under the spec's arbitration clause for rival use only; it is a compensatory comparator and is never presented as satisfying zero-collapse. Flight 8's homogeneous result carries across dispatch labels at matched effective gain g·λ̄, not at matched base triples (at equal bases b the symmetric dispatch gives b⁴ and the product b³). At build, the heterogeneous step with a constant λ array must reduce to Flight 8's scalar step at equal state, effective gain, floor, deactivation rate, timing and uniform array. A product-versus-mean contrast does not select multiplication uniquely among zero-collapsing functions; `F_LR` and `F_2_symmetric` remain untested.

**3.6 Terrain family (R3), all smooth, periodic and closed-form.**
- **T0, flat.** Homogeneous bases; Flight 9's own reference (§9.4, §10.2).
- **TA, concordant.** All three bases move together, so both indices give the same contours. It is the non-identifiability control for test (a): no index may be selected there, and amplitudes may not be substituted for contours after the fact. Test (b) is not forced to ND on TA; it may return any of its outcomes.
- **TB, cross-gradient.** r constant; v + u varies along one axis and v − u along the other.
- **TC, near-face suppression.** One base near zero over a patch whose other two bases are high. It is a contrast in feedback suppression at declared gains, not a test of literal zero-collapse (§3.8).
- **TD, margin variants.** §5.

**3.7 Outcome records (L2 Q1).** Each endpoint keeps its own record; the facts are not forced into one label.

| Label | Meaning |
|---|---|
| Follows own | Own relation within a declared equivalence tolerance on an informative domain, with adequate precision. Whether the rival is excluded is a separate determination. |
| Follows rival | Own relation excluded beyond tolerance; rival relation meets its equivalence criterion; the two are identifiable on this domain. |
| Follows neither | Both relations excluded beyond tolerance on an informative, evaluable domain. |
| Not distinguished | Evidence cannot separate the alternatives, or declared precision, contrast or resolution is insufficient. |
| Not adjudicable here | Terrain geometry makes the contour predictions equivalent by design (TA). |
| Apparatus unevaluable | Required observations or valid records are unavailable; never an adverse scientific finding. |

Failure to reject is not equivalence, and failure to establish either fit is not "neither".

**3.8 The zero face and the floor (ruled; L2 Q9 §11.1).** The floor does not depend on the bases. At exactly λ = 0 a realization cell still activates with probability 0.01 per tick and has stationary occupancy 0.0523. PD1 and PD7 say registration is impossible on an annihilating face. Flight 8's homogeneous positive bases never met this. For Flight 9 the carried rule is kept: TC is described as near-face feedback suppression, "hole" is defined operationally, and the exact-face limitation is disclosed. The skeleton's absence of reactivation at an exact zero coefficient is rule conformance, not evidence for zero-collapse. The floor is not gated by a base and floor-generated events are not masked out of density. The correspondence between PD7 and the base-independent floor is held as a theory-track item (§14).

## 4. The control coordinate on a terrain (R5; L2 Q4)

**Ruled: the terrain's bases are frozen and the sweep variable is g.** The carried rule sees g and λ only through g·λ_i, so this is a sound parameterization of this instrument. The reasons are: base-array identities are preserved, no base leaves [0, 1], and the multiplicative control is explicit. v0.2's reason is withdrawn (§13). The equivalence is rule-specific: in the Overview the spontaneous term also scales with Λ, and the flight's floor is fixed. An appended notation row is required.

**Normalization (ruled): spectral-relative gain.** For composition X on a fixed terrain, with A the Moore adjacency,

B_X = diag(λ^X)·A/8,  g_spec,X = q / (Δt·spr(B_X)),  κ = g / g_spec,X.

The skeleton closure's leading multiplier reaches one at g_spec,X. On T0, spr(B_X) = λ̄ and κ reduces to Flight 8's m. Both compositions use the same procedure and the same κ grid. This matches distance from each rule's closure instability, not raw gain; no normalization is neutral to every question, and this one is named as the structural choice. Conditions:
1. computed from the fixed terrain arrays and adjacency before any dynamic data;
2. raw bases, raw λ, spectral radius, spectral crossing, actual g, κ and local m_i = g·λ_i·Δt/q all persisted;
3. never normalized by observed onset, occupancy or a fitted edge;
4. the zero-spectral-radius case declared: no finite crossing, no division, no invented level;
5. raw-g crossings reported beside normalized ones (the closure crossing at κ = 1 is true by definition, not a result);
6. the normalization fixed for scored analysis and not chosen after seeing which separates better.

A positive scalar normalization cannot change a contour family. It can change which grid levels are informative, floor-dominated, saturated or extinction-prone, which is why it is declared in advance.

## 5. Margins: terrains laid for Flight 10, nothing built in (R6; L2 Q9 §11.3)

**5.1** No criterion, threshold, evaluator branch, terrain-selection rule or stopping rule refers to the margins hypothesis. The instrument records the same per-cell summaries for every cell. Any core/margin partition is computed afterwards from declared cuts; every registered cut is frozen and reported.

**5.2 Design-side ratio.** Two knobs: edge length relative to enclosed area, and steepness of λ across the edge. TD's "fixed total core area" needs a geometry-based, composition-independent definition, because a core defined by local m_i moves with g and differs between the two indices.

**5.3 Measured-side ratio.** From the summaries of §7. A realized margin ratio is an observation, not something the geometry guarantees. At coarse windows an intermediate-occupancy band can be produced by the floor alone: under the floor-only null the probability of any activity in W consecutive ticks is 0.0523, 0.1342 and 0.6496 for W = 1, 10 and 100 (analytical, by script). The W-specific floor reference is recorded with every band, and no band is read as a collective margin on its face. No coherence claim follows from any of it.

**5.4** Terrain identities (formula, parameters, hash of the base arrays) are committed at freeze so Flight 10 can reuse the terrains.

## 6. Confirming the boundary (R7)

One stream per cell. Heterogeneity is in the frozen bases between cells and nowhere else. Bases frozen in time, Q off, Γ = 0, drive zero, noise off, synchronous Moore timing, W = 1 tick as the participation window: all carried from Contract F8 §2. No per-cell stream count, no within-cell heterogeneity.

## 7. Flicker observable — discharge of Interpretation 004 (R8; L2 Q5)

**7.1 Mike's intent.** Discharge it cheaply: per-cell tail summaries, not state histories; one run-length statistic, recorded and not tested; no further design effort unless the theory gives it a prediction; the same summaries serve as the measured margin.

**7.2 Facts about the frozen rule (corrected).** A complete, uncensored active spell has geometric length with mean 1/q = 5.517 ticks, at every cell and level, conditional on a spell occurring. That makes the active-spell mean a check on the implementation, not a scientific observable. Skeleton cells can become permanently inactive and a finite record can contain no switch. For a recurrent stationary cell with occupancy p, the mean inactive spell is (1 − p)/(p·q): it is determined by occupancy and q. The declared statistic is therefore descriptive and is not an independent signature of anything. Inactive-spell distributions and temporal correlations could carry more; they are not recorded.

**7.3 The record and the statistic (ruled).**
- **Windows:** W ∈ {1, 10, 100} ticks; non-overlapping, equal-width, complete block windows aligned to the start of the recording tail; a window is active if the cell is active at any tick in it. The W = 1 participation declaration (PD5) is separate from these coarser observation windows.
- **Persisted per cell, per run, per W:** the number of active windows A; the number of observed inactive segments R₀; the first and last window states (two bits).
- **Statistic:** the mean length of observed inactive segments clipped to the recording tail, W·(n − A)/R₀ ticks, with n the number of windows. An all-active record returns "undefined: no inactive segment". Segments touching either end of the tail are flagged as possibly censored.
- **Coverage:** every declared run at every declared level. The level set is bound in the contract.
- **Status:** recorded, not tested. The PD record's held candidate (resolution-invariance across W near Λ*) remains held and untested; means do not preserve run-length distributions. No further design effort unless the theory gives it a prediction.
- **Timing:** Interpretation 004 says "before any data". These four items are fixed in the pre-probe declaration (§10.4), which Mike ratifies and which is incorporated into the contract.

The summaries are explicit package reporting items with coverage and validity checks (§10.1).

## 8. Onset continuity (R9; L2 Q6, acceptable in principle)

**Ruled: not in Flight 9.** Nothing in the record requires the immediate successor to resolve it. The reasons, as qualified by L2:
1. The unresolved question is a homogeneous one and is most directly isolated by a dedicated flat experiment. Terrain complicates it; terrain does not make every onset question unanswerable.
2. A finer grid alone cannot establish the character of the transition. Extinct and surviving runs mix near the boundary, and any conditioning on survivors must be declared.
3. Flight 9's endpoints do not require it. No statement is made here about what Flight 10 may need.

The limitation stays open by name: continuity through the entering interval is untested. Neither T0 nor a repeat of Flight 8's above-boundary criterion resolves it. Whether it becomes a successor stage on the homogeneous instrument or a later flight, and when, remain Mike's.

## 9. Fidelity on a terrain (R10; L2 Q7) — reported, never scored

**9.1 The threshold in the control is a skeleton object.** The spectral crossing is the zero-floor site-closure comparator. Its lattice counterpart is a declared finite-horizon skeleton persistence threshold. The realization has activity at g = 0 and has no absorbing-state onset. The crossing is determined by the leading mode of the spatial feedback operator, which may localize on a high-λ patch; peak λ alone does not determine it.

**9.2 The surface in space.** The site closure's fixed point depends on neighbouring probabilities as well as λ_i, so m_i = 1 is a local homogeneous benchmark and not the heterogeneous closure's predicted edge.

**9.3 The three reported comparisons, corrected.**

| Comparison | Object and reading |
|---|---|
| Measured onset against spectral crossing | Skeleton finite-horizon threshold against the zero-floor closure crossing; normalized and raw-g shifts with uncertainty. |
| Local m_i on the measured edge | A spatial diagnostic on an explicitly defined edge, against 1 (local homogeneous benchmark) and against T0's measured boundary. Neither is a pointwise terrain prediction. |
| Observed occupancy against the site closure | Matched object, floor and estimand: seed-mean occupancy maps against the closure's probabilities. If edges are compared, the same edge-extraction rule is applied to both. |

The contract freezes the edge definition (occupancy or excess occupancy, connectivity, resolution, empty/full/disconnected cases), the site solver, branch, initialization, tolerance and failure status. A poor comparison is published as such and never becomes a scored failure.

**9.4 T0 as the lattice reference.** Flight 9's own flat arm at its declared size, horizon, grid and fresh panel, with its uncertainty and its unavailable-boundary case. Flight 8's 1.521739 is not used as a constant, and T0's measured value is never used to retune a scored tolerance.

## 10. Instrument, objects, size, probe, review (R11–R15)

**10.1 Carry-over (R11; L2 Q2, Q9 §11.4–§11.5).** New package `f9` beside `f8`; nothing in `f8` or `e1` modified.

| Flight 8 module | Flight 9 |
|---|---|
| M1 rule and levels | New rule module with per-cell λ; terrain builder with committed identities; per-cell summaries (§7) |
| M2, M4, M6 | Not carried (L2 accepts the omission). |
| M3 null | The floor-only stationary occupancy carries analytically. Flight 8's bands, tolerances and thresholds do not; fresh calibration for the chosen endpoints, with role-separated streams. |
| M5 closure | Site mean-field map and spectral crossing per terrain |
| M-P1 evaluator | New composition evaluator with (i) a known-answer corpus and (ii) **a targeted statistical qualification** on design and held-out ensembles before any canonical scoring |
| M7 | Principles carried (completeness against readiness, valid adverse records, prerequisite passage, identity and authorization binding). The record graph, jobs, dependencies and record types are Flight 9's own. |

The qualification of (ii) guards: false identification; vacuous support (constant, empty-edge, saturated, singleton-contour, low-contrast maps); false adverse findings from mispriced correlated variation; improper ND; aggregation error across contours, levels, terrains and rules; and the right label for the wrong cause. The independent unit is the seed run, not the cell. It is M6's protective function, not its module, classes, cap or counts; it is sized in the contract. It cannot repair §3.4: a process that truly satisfies the tested property is not a false positive for it.

Flicker summaries and all fidelity outputs are explicit package reporting items. Their values gate no verdict; a missing required record prevents a claim of complete reporting.

**10.2 Objects (R12; L2 Q9 §11.7).** The realization is the primary object for the composition tests. The skeleton is the structural reference and, by L1's proposal, the coupling-sensitive contrast (§3.4); extinction is a valid observation. On T0 two things are kept apart: the constant-array reduction (§3.5) is the apparatus check; rerunning Flight 8's four tests under fresh seeds is a scientific consistency exercise whose tolerances and domain are redeclared for the chosen size and horizon. An adverse or ND result there is not automatically a coding defect.

**10.3 Size, seeds, estimands (R13; L2 Q9 §11.2–§11.3, §11.5).** The contract prices L = 50 against L = 100 and states whether the larger lattice enlarges the domain, refines a fixed one, or enlarges patches in lattice units; one larger lattice is not a scaling study. Terrains are deterministic; twenty dynamics seeds on fixed terrains are not twenty sampled terrains. The contract declares whether composition arms and levels use independent or deliberately paired streams, whether the endpoint scores the seed-median map or summarizes per-seed scores, and the contour binning, minimum membership, coverage, weighting and minimum informative contrast. Seed-level summaries are preserved. Fresh masters throughout.

**10.4 The pre-contract probe (R14; L2 Q8).** Allowed in principle. **Before any probe output, Mike ratifies a short pre-probe declaration** that fixes:
- the scientific target, the structural/fidelity division, the adverse outcomes, the ND meanings and the claim limits of §3;
- the candidate terrain, size, level and seed menu; the probe's purpose, maximum scope, retained outputs and stopping rule;
- what the probe may inform (resource pricing, feasibility, whether the specified terrains offer usable contrast) and what it may not adapt (contour cuts, tolerances, aggregation rules);
- code and terrain identities, stream roles and the provenance record;
- the four Interpretation 004 items and §7.3's conventions.

After the probe: every attempted configuration and outcome is preserved, including failed separation. Probe results stay design evidence and never become calibration, qualification or canonical observations. Terrains kept because the probe showed separation make later inference conditional on those terrains.

**10.5 Failure paths (L2 Q9 §11.6).** Before freeze the contract enumerates no contrast, no edge, saturation, insufficient contour coverage, finite-resolution ND, skeleton extinction, corrupted or missing summaries and closure nonconvergence, and distinguishes scientific adverse finding, scientific ND, unavailable fidelity comparator and apparatus failure, with precedence and aggregation across terrains, rules and levels. No failed terrain is dropped and no level is selected after the fact.

**10.6 Review path (R15).** This note → pre-probe declaration, ratified → probe → contract register → L2 contract packets → Gemini audit before freeze (commission v3 in force; v3.1 held) → freeze.

## 11. Rulings of record on R1–R15 (Mike, 2026-11-12: "I accept your recommendations"), as they stand after §12

| # | Item | Standing |
|---|---|---|
| R1 | `F_canonical` as the product; `F_baseline` as rival only | Stands (L2: acceptable in principle) |
| R2 | The composition claim | Amended: two conditional tests; boundary compatibility is the scored substantive endpoint (§3.3) |
| R3 | Terrain family T0, TA, TB, TC, TD | Stands; TA's and TC's roles restated (§3.6, §3.8) |
| R4 | Structural scored tests; locations to fidelity | Amended: boundary endpoint; whole-map contour constancy reported only (§3.3, §3.7) |
| R5 | Bases frozen, sweep g | Stands on corrected reasons; normalization ruled: spectral-relative gain (§4) |
| R6 | Margins: geometry on the design side, summaries on the measured side, nothing tested | Stands, with §5's additions |
| R7 | Between-cell heterogeneity only | Stands |
| R8 | Flicker discharge at W ∈ {1, 10, 100} | Amended: record and estimand of §7.3 |
| R9 | Onset continuity not in Flight 9 | Stands (L2: acceptable in principle), reasons qualified (§8) |
| R10 | Fidelity on a terrain | Amended as §9 |
| R11 | M2/M4/M6 not carried | Stands, with the new evaluator's statistical qualification added (§10.1) |
| R12 | Realization primary; skeleton reference; Flight 8's tests on T0 | Stands, with §10.2's separation |
| R13 | L = 50 against 100 priced; deterministic terrains; fresh masters | Stands, with §10.3's declarations |
| R14 | Pre-contract probe allowed | Stands, conditional on the ratified pre-probe declaration (§10.4) |
| R15 | Review path | As §10.6 |

## 12. L2's consultation and Mike's ruling on it

**Packet:** `f9_design_consultation_L2_v1.zip` (`433dfded65d6cf96…`, 23 files and a manifest, pinned to `817450e`); instruction `L1_TO_L2_F9_DESIGN_CONSULTATION_2026-11-12.md` (`d1078117a5fc21d3…`).
**Return:** `L2_F9_DESIGN_CONSULTATION_2026-11-12_RECEIVED.md` (`65d95bc3a907cf04…`, 50,919 bytes, a byte copy of L2's file). Receipt PASS; L1 re-verified the manifest hash, the arithmetic and the counterexamples by script. Overall: REQUIRES CHANGE. Q3 and Q6 acceptable in principle; Q1, Q2, Q4, Q5, Q7, Q8, Q9 require change; nothing rejected.

**Mike's ruling, 2026-11-12: "accept all as recommended"**, on L1's recommendations:

1. H1 is read as two conditional results; no lattice result selects the true composition (§1, §3.3).
2. The scored endpoint is the boundary; the whole-map statistic is reported only (§3.3).
3. Coupling-sensitive contrast: propose the skeleton arm in the contract; no third arm (§3.4).
4. Targeted statistical qualification of the new evaluator, sized in the contract (§10.1).
5. Spectral-relative gain as the normalization (§4).
6. The flicker estimand and record of §7.3; descriptive only.
7. The carried rule is kept; TC is near-face suppression with the exact-face limit disclosed; the PD7-versus-floor correspondence is held as a theory-track item (§3.8, §14).
8. A pre-probe declaration, drafted by L1 and ratified by Mike, before any probe output (§10.4).

L2's remaining requirements (its qualifications on Q6, the fidelity corrections of Q7, and Q9 §11.2–§11.7) are adopted as contract-level requirements and are written into §§5, 8, 9 and 10.

## 13. Errors of L1's in v0.1 and v0.2, found by L2

1. **§4.** The claim that scaling the bases changes a terrain's shape was wrong. Scaling by s multiplies the product by s³ and the height by s, each uniformly across cells; each keeps its own contours.
2. **§7.** Time active and switch count do not determine the inactive-spell mean ("001100" and "100001" have the same counts and means 2 and 4). At stationarity that mean is fixed by occupancy and q. "Every cell switches constantly" was overstated.
3. **§3.2 and §9.** A uniform edge shift was listed as adverse room for the level-set claim; it is a fidelity matter. The contour m_i = 1 was offered as the closure's edge; it is a local homogeneous benchmark.

## 14. Held, nothing authorized by this note

Gemini commission v3.1. The two next-touch repairs of close record §7.2: the direct-DIP docstring in `test_f8_m6.py` and the stale comment in `test_f8_mp1.py`. The third-order lattice-versus-ODE comparison. Overview v1.8.2. The onset-continuity question (§8). **New, by Mike's ruling 7:** the correspondence between PD7 (registration impossible on an annihilating face) and the flight rule's base-independent floor, as a theory-track item.

## 15. What this note is not

Not a contract, not an authorization, not a result. It makes no statement about Regime II, Ψ or coherence. Flight 8 stage 1 stays closed as recorded.

*L1, v0.1, v0.2 and v0.3 2026-11-12.*
