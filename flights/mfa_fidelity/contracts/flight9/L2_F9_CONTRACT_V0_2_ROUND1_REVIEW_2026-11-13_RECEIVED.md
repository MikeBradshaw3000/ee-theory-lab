| Receipt check | Verified value | Result |
|---|---|---|
| Archive | `f9_contract_v0_2_review_L2_v1.zip` | Received |
| Archive SHA-256 | `77bc63c6ece5c47be08f948342d7a2c67c7c2e635c44a8484002828fc5bd5d93` | MATCH — supplied digest |
| File count | **31 payload files + MANIFEST.txt = 32 files** | MATCH |
| Manifest entries / matching payload hashes | **31 / 31** | PASS |
| MANIFEST.txt SHA-256 | `c1256b7fc22df1284a978f1ad673b16d28c88857ce591a68c825662bb44ffd6d` | Computed; not self-listed |
| Missing, unlisted or duplicate payload paths | None | PASS |
| ZIP CRC integrity | Verified | PASS |

| # | Payload file | Computed SHA-256 | Against MANIFEST.txt |
|---|---|---|---|
| 1 | `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_2_REVIEW_2026-11-13.md` | `08cfa22064ecf2e2eccb0a2570fd47a0321319eff61ca10a581562a80154f787` | MATCH |
| 2 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_2.md` | `8dd4b4e6a5b161a79adcfd8e21b3f1734c9fbdc9e9c2b07ecad327b1b3e6c187` | MATCH |
| 3 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_1.md` | `5f08acf6dcae509d20bd653619cd6ce6b2e45cb0381f30abc3bfd9de1e864837` | MATCH |
| 4 | `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_QUESTIONS_ADVICE_2026-11-13_RECEIVED.md` | `a79dbb22de2a6fb06d7ccd6a22753c1d0cf15f5fa902a527a99fb5c4c9336396` | MATCH |
| 5 | `flights/mfa_fidelity/contracts/flight9/arith/contract_arith.json` | `733d6b8ade0762313b6ba8c55efe1464be858fea8948f93e0c06154cdad57562` | MATCH |
| 6 | `flights/mfa_fidelity/contracts/flight9/arith/f9_contract_arith.py` | `57ccd322431bb2a7c1ade0cbe220c83f0e41984f353353db5a8aa02d47ac3237` | MATCH |
| 7 | `flights/mfa_fidelity/contracts/flight9/arith/f9_step1.py` | `d195c94015d6a6670097e88898a77df1c992c2345c250fc62428fb83d2d1b47f` | MATCH |
| 8 | `flights/mfa_fidelity/contracts/flight9/arith/smooth_check.py` | `d36b325cb793700286ab693ac16a9df80d2357eab769de4d9fa41468a2b232c3` | MATCH |
| 9 | `flights/mfa_fidelity/contracts/flight9/arith/step1.json` | `ba59630c43d6741a5fc1b46487092ce5e8aa647f43d33b538e6aae67086c287a` | MATCH |
| 10 | `flights/mfa_fidelity/contracts/flight9/arith/tb_r0.py` | `d53947dd9f506a46ad66528724ddf9da2c3b43a7387299a2f11c6dece0b3a301` | MATCH |
| 11 | `flights/mfa_fidelity/contracts/flight9/arith/td_counts.py` | `86ca016b219ba1aaac4dad39f213caee34dc1e6f027188c61e236223bdaf4050` | MATCH |
| 12 | `flights/mfa_fidelity/contracts/flight9/arith/td_final.json` | `82b8d83ac7a68503803da2c3f09baefaaa7b830d15748d457ce933b213580422` | MATCH |
| 13 | `flights/mfa_fidelity/contracts/flight9/arith/td_final.py` | `ca0076012b8bbc0e5b9e6214388aa895429cc0d9c9336376a7bfbfce41fb64fe` | MATCH |
| 14 | `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_3.md` | `8d82e319d79402f89ea27690d64af23da2296d2c462fed7944a07ee6ebda4ac1` | MATCH |
| 15 | `flights/mfa_fidelity/design/flight9/L2_F9_DESIGN_CONSULTATION_2026-11-12_RECEIVED.md` | `65d95bc3a907cf047b3a7c851da3fb680769b6fa1c4e5657a51ebbaa023e3e25` | MATCH |
| 16 | `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | `473a2a165fd5cb4e38ddb064dc14c24880af8998a21b9ffad1aa7c065551016c` | MATCH |
| 17 | `flights/mfa_fidelity/design/flight9/probe/F9_PROBE_RECORD_2026-11-12.md` | `f3affc05de26f0d7ecc4c54cb888ade5d8fabcaf7cc68f2e264bd1a8b5614f3d` | MATCH |
| 18 | `flights/mfa_fidelity/design/flight9/probe/F9_PROBE_REPORT_2026-11-12.json` | `59cfce5ffbd24512a1301da67748eda8a5ced8efec32efed5eebd8b464a51679` | MATCH |
| 19 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |
| 20 | `flights/mfa_fidelity/design/flight9/probe/f9_probe_report.py` | `1f2f8cfae79267fc3ddd63ea9984604d40780fb360e08a2ca3d1c63cf8103680` | MATCH |
| 21 | `flights/mfa_fidelity/design/flight9/probe/F9_PROBE_IDENTITIES.json` | `3a4e1399b935310f4b9828a101eb7d9595e92a55cfe17b496e3f7c5c7115b60f` | MATCH |
| 22 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | MATCH |
| 23 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` | MATCH |
| 24 | `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md` | `194886e89f55a4c7fff1413db767975d892660163a530f581e2131ec5121272d` | MATCH |
| 25 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md` | `69d173f370d5ce6d86858142783eab6dfc1918aeb197eab5fd50b497d9e1c975` | MATCH |
| 26 | `flights/mfa_fidelity/rulings/PD_PARTICIPATION_RULINGS_PD1_PD7.md` | `f239b8f7444e38395341acb2ccec23dfee0632596eab3080019ee5ec175fe4ee` | MATCH |
| 27 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_1.md` | `ec63fdb0e2060110b99116605d7673bc61d4d63ca79f0c3a6b41365848d39524` | MATCH |
| 28 | `flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md` | `39f66673657b0f429691c908142f889d9ef3d463a8372455cba95db7c486f52a` | MATCH |
| 29 | `theory/overview/EE_emergence_overview_v1_8_1.md` | `b2d67fac5efa3c73fe8f76ea3ba7d18f88023f468f648c2a36532bd69522b41c` | MATCH |
| 30 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 31 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |

# L2 → L1 — Flight 9 Contract v0.2, round 1

**Date:** 2026-11-13. **Register:** contract review. **Decision authority:** Mike. **Reviewer:** L2.

**Object reviewed:** `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_2.md`, SHA-256 `8dd4b4e6a5b161a79adcfd8e21b3f1734c9fbdc9e9c2b07ecad327b1b3e6c187`.

**Packet pin:** `ee-theory-lab` main at `d7c8312b7255b5bb4a927e1d97824d53ddaf056d`, as identified in the instruction document. The receipt verifies the supplied bytes against the supplied manifest; the review uses that packet as the committed record. The instruction document was read first. Receipt was returned separately, and substantive review began only after Mike's “execute.”

## 1. Overall finding and question dispositions

**The scientific architecture is acceptable, but the candidate requires changes before freeze.** The main deficiencies are mismatches between the declared boundary claim and its discrepancy, undefined evaluator cases, conflicting aggregation instructions, an overstated interpretation of diagnostic K, and incomplete qualification and execution dependencies. These are contract defects that would let reasonable implementations produce different decisions from the same observations.

The supplied arithmetic is substantially sound. All six arithmetic scripts execute successfully, and all three regenerated JSON files are byte-identical to the supplied files. Numerical reproduction does not resolve the procedural defects below. One supporting run-count field disagrees with the current job list. Section 12 records the checks and their limits.

| Question | Disposition | Principal finding |
|---|---|---|
| Q1 — Claim grammar | ACCEPTABLE | B and D are appropriately conditional and separate; the operational boundary is expressly an instrument declaration. The implementation still needs the repairs below. |
| Q2 — Fixed occupancy criterion | ACCEPTABLE | θ = 0.20 may stand as a disclosed post-probe design choice, frozen before fresh canonical observations; it is not a blind prediction. |
| Q3 — Estimator and edge | REQUIRES CHANGE | The smoothed-mean target and periodic bond edge are defensible; class 10 does not adequately exercise smoothing's deterministic effects. |
| Q4 — Discrepancy, free level and ε | REQUIRES CHANGE | D95 can ignore a whole component; 99 cuts do not automatically exhaust the claimed contour family; candidate conventions are incomplete. |
| Q5 — Uncertainty | REQUIRES CHANGE | The treatment of up to 5% invalid resamples is undefined; the target and qualification of nominal percentile bounds need completion. |
| Q6 — Aggregation and precedence | REQUIRES CHANGE | One per-level outcome is missing, and the two-adverse-level rule conflicts with the fewer-than-three-levels precedence rule. |
| Q7 — Diagnostic K | REQUIRES CHANGE | A coupled-skeleton persistence profile is not yet a coupling effect estimate; its grid bracket is not sampling uncertainty. |
| Q8 — Qualification | REQUIRES CHANGE | Some supposed known answers are not truths of the fitted statistic; generator, error predicates and decision-unit coverage remain underdetermined. |
| Q9 — Other freeze blockers | REQUIRES CHANGE | Repair ordering and identity dependencies; complete T0 and mandatory reporting specifications; reconcile identity timing and supporting arithmetic. |

Mike's recorded scope stands: terrain and composition, between-cell heterogeneity, no Regime II, Ψ, coherence endpoint or onset-continuity experiment. The changes recommended here remain within that scope. No Flight 8 or E1 determination is reopened. A recommendation that changes a ruled choice is submitted for Mike's ruling; this review does not itself amend the contract or authorize a run. [I, register and authority; C §§11–13]

**Source notation.** References such as `[C §5.5, step 9]` identify exact packet documents, not outside sources. The source key is in §13; all their full digests are in the receipt above. Calculations identified as review checks were made from closed-form inputs or separate synthetic examples, never from probe boundary output.

## 2. Q1 — Claim grammar

**Disposition: ACCEPTABLE.**

The draft implements the central correction of the design consultation. B asks whether a declared operational occupancy boundary is compatible with a contour of the prescribed index. D asks whether the two prescribed rules yield distinguishable contour consequences on the designated terrain. Neither selects a true ecosystem composition, and whole-map contour constancy is explicitly a stronger, reported-only proposition. The bridge from PD7 to the measured boundary is identified as this instrument's declaration; it is neither the skeleton's persistence threshold nor an assertion of an abrupt spatial change. [C §§1.1–1.4; D §§3.3–3.4; L2-D §§3.1–3.4]

The terrain roles are correct. On TA and TD, P = t³ and H = t. On TC, P = 0.81u and H = (1.8 + u)/3. These are increasing transformations on their respective terrains, so their contour families agree. TB supplies the intended geometric distinction. Keeping TC's observed suppression difference descriptive is appropriate given both this algebra and the probe disclosure. The correction from thirteen required arms to seven per composition, fourteen in total, is correct. [C §§1.0, 3.1–3.3, 11.2]

The independent-response alternative remains a real limit: cells whose stationary occupancy is a function of local λ can satisfy both geometric claims without neighborhood interaction. The draft properly preserves that limitation. The positive floor also prevents TC from serving as literal zero-collapse validation. No third scientific arm is required to make the narrowed B/D claims. [C §1.4; D §§3.4, 3.8; L2-D §3.3]

Two interpretation qualifications must accompany this acceptance:

1. **These are unoriented edges.** E(R) = E(Rᶜ). Thus the same boundary can result with the occupied side reversed. Add to §1.4 that B/D do not establish which side is occupied, increasing occupancy with λ, or whole-map scalar sufficiency; “follows own” means geometric compatibility under the declared rule. This completes the direction declaration requested in L2-D §3.4 without adding an endpoint.
2. **The admissible claim is the one the completed discrepancy actually supports.** The D95 and finite-candidate issues in Q4 affect the meaning of “represented by a level set.” Acceptance of the two-question architecture does not clear those details.

## 3. Q2 — Occupancy criterion and θ's standing

**Disposition: ACCEPTABLE.**

A single fixed scored threshold is a coherent structure. It gives occupancy one operational meaning across arms, terrains and levels. Running the full evaluator at 0.10 and 0.30 beside θ = 0.20 is useful sensitivity reporting, provided those outputs never replace or rescue the registered scored result. No argument in the packet makes 0.20 a unique theoretical threshold, and none is needed for an explicitly declared operational boundary. [C §§1.2″, 1.3(f), 5.5, steps 1–2]

The provenance is acceptable **as disclosed**. The pre-probe declaration allowed feasibility information and prohibited an edge rule chosen because it rescued or improved an observed result. The record says R-3 occupancy percentiles were seen and the boundary endpoint was not. That supports treating θ as a post-probe design choice; it does not support calling it a pre-probe independent prediction. I cannot independently establish the author's motivation or prove the absence of unrecorded computations from the supplied files. No probe arrays are included, and none was requested or inspected for this review. [PP §4; I disclosures 4–5; C §1.0]

The standing to preserve is precise: Mike ratifies θ and the complete evaluator before fresh canonical observations; canonical inference remains conditional on the disclosed selection; all registered sensitivity results are published; changing θ later creates a new instrument/validation boundary. The statement that probe output “enters no gate” must mean that probe observations are not reused as scoring or calibration data, not that they supplied no design information. The surrounding disclosures already make that distinction possible. [C §§1.0, 5.5, 7–8]

I do not recommend changing the number simply to give it an appearance of blindness. Nor do I recommend an additional probe calculation of edges to justify it. Whether the new TB/H and TD arms offer usable edges at this threshold remains a future observation; a wholly uninformative required arm must retain its ND consequence.

## 4. Q3 — Estimator, edge and informative-level counts

**Disposition: REQUIRES CHANGE.**

### R1 — Qualify the declared smoothing target, including deterministic changes to shape

The 3×3 mean can remain as part of an explicitly defined occupancy estimand. Section 5.5 now identifies the boundary of the smoothed seed-mean map, rather than a typical individual-run boundary. The periodic four-neighbour bond representation is also coherent. The graph used to represent a raster boundary need not be identical to the Moore graph used by the dynamics. Applying the same bond construction to observed and predicted regions is the relevant consistency requirement. [C §5.5, steps 1–4]

The limitation is that smoothing can erase components, fill holes and move edges before the “include every component” rule operates. For a deterministic example at θ = 0.20, take a one-cell-wide vertical stripe of 100 cells, occupancy 0.30 inside and 0.05 outside. Its raw region has 100 cells and 200 edge bonds. After the 3×3 mean, its maximum occupancy is

\[
(0.30+2\times0.05)/3=0.1333\ldots<0.20,
\]

so the stripe disappears. Conversely, a one-cell-wide 0.05 gap in a 0.30 map is filled because its smoothed value is 0.2167. These are consequences of the declared estimator, not implementation errors. They demonstrate why “every component” must mean every component of the **post-estimator** region. [C §5.5, steps 1–3; deterministic calculation]

Known-answer class 10 tests noisy compatibility at a calibration amplitude. It does not test these deterministic topology changes, curvature effects, low-gradient crossings or the fact that smoothing h(λ) need not remain a scalar function of λ on a heterogeneous terrain. The supplied half-height disc check verifies exactly its six symmetric examples, not general preservation at the scored occupancy threshold. [C §6.1, class 10; AR, `smooth_check.py`; review verification §12]

**Required repair.** Retain the estimator if Mike wishes, state its post-estimator scope, and add controlled known-answer cases for thin components/channels, holes, curved and asymmetric profiles, and near-threshold plateaus. Certify the expected outcomes for the complete post-estimator target. A case need not preserve the raw edge to pass an implementation check; it must return the correct declared result after the transformation. Keep these deterministic cases separate from speckle/noise qualification.

The proposed global counts—100 cells on each side and 40 edge bonds—are reasonable candidate resolution declarations. They do not guarantee adequate precision, protect every component, or supply 100 independent observations. Their sensitivity consequences belong in qualification, with the seed map remaining the independent unit.

## 5. Q4 — Discrepancy, fitted level and ε

**Disposition: REQUIRES CHANGE.**

### R2 — Reconcile the robust distance with the missing-component claim

The symmetric 95th-percentile discrepancy is a well-defined robust comparison once its numerical conventions are fixed. It is not a guarantee that every predicted component affects the decision. A missing component contributing less than approximately 5% of contour length can disappear from the 95th percentile altogether. Equal weight for every bond does not prevent this. [C §5.5, steps 3 and 6]

A separate synthetic geometry check on the declared 100×100 torus gives a concrete counterexample:

| Object | Construction or value |
|---|---|
| Observed region | Five full-height, five-cell-wide stripes at x = 0–4, 20–24, 40–44, 60–64 and 80–84 |
| Observed region and boundary | 2,500 cells; 1,000 bonds |
| Predicted region | The same stripes plus a separate 10×10 island at x = 8–17, y = 20–29 |
| Missing component | 100 cells; 40 bonds |
| Predicted boundary | 1,040 bonds |
| Missing fraction of predicted bonds | 40/1,040 = 3.846% |
| Both directed 95th-percentile distances | 0 |
| Symmetric D95 | **0** |
| Maximum nearest-boundary distance | Approximately 7.51665 cells |

All global area and edge-count minima are satisfied. This is a defect in the universal explanation of the functional; it is not evidence that such a result occurs on a canonical terrain. Class 9's missing one of four equal discs does not cover this small-perimeter case.

**Required repair.** Decide which claim is intended. If every resolved component must affect scoring, add a component-sensitive coverage/discrepancy rule with a declared per-component resolution and qualify it. If D95 is retained alone, state the narrower perimeter-weighted meaning, remove the universal missing-component assertion, and report component coverage explicitly. The latter accepts that an entire small component may be ignored by the scored functional. Mike must rule on that meaning; it cannot be hidden in an implementation choice. Update §§1.2, 5.5 and 6 together.

### R3 — Complete and correctly scope the contour search

**Finite candidate coverage.** A compatible result against one candidate witnesses the existence of a suitable contour. An adverse result against 99 percentile cuts does not, without more, establish failure against every level set omitted from that list. The draft's general “some level set” language and the algorithm's restricted search therefore differ on the adverse side. [C §§1.2(B), 5.5, steps 5–8]

Before freeze, either enumerate all distinct eligible superlevel masks on the finite lattice, establish a sufficient coverage result for the retained candidates at the declared resolution, or narrow the adverse statement to the registered candidate family. The first choice has a resource cost; the third has a claim cost. A coverage argument cannot simply assume a triangle inequality for this quantile discrepancy.

**Empty and duplicate candidates are present in this packet's terrains.** Using the supplied arithmetic convention, TD-1-2 has 228 cells exactly at its rounded floor. Its first and second percentile cuts produce a full superlevel region and hence an empty contour, under both compositions. T0 has no nonempty contour at any of the 99 cuts. TB/H has only 51 distinct candidate masks, and TC's 98th and 99th cuts coincide. These findings use terrain arrays only. [AR, `f9_contract_arith.py`; review verification §12]

The arithmetic script makes distance to an empty edge infinite, but the contract does not adopt that convention. It also leaves the percentile interpolation method, duplicate handling, minimizing-level tie break, and all-candidates-empty result unstated. These choices affect executable behavior and the reported λ*.

**Required repair.** Freeze the torus distance norm (the supplied script uses Euclidean distance), quantile method, candidate eligibility, empty-set and duplicate conventions, deterministic minimizer selection, and all named unavailable states. Distinguish an absent observed edge from an existing observed edge with no eligible predicted contour. Bind the resulting candidate levels/masks to their recorded identities. A T0 spatial edge should not accidentally be treated as a meaningful constant-index contour comparison.

### The free level and two-cell resolution can remain

Fitting the level is appropriate for an existential contour claim when location belongs to fidelity. There is no automatic requirement to divide an error level by 99. The full fitted statistic, including candidate search, must be recomputed in each resample and qualified against rival and neither-family cases. Reporting the selected λ* does not turn its location into a scored prediction. [C §5.5, steps 7–9; L2-D §3.2]

I accept **ε = 2.0 cells as a proposed declared resolution**, once the distance and claim are completed. The argument based on interaction scale and raster representation supplies a design convention, not a theorem that smoothing error is at most two cells. The symmetric-disc calculation does not provide that theorem either. Qualification must price the complete estimator and discrepancy around ε; poor precision must continue to yield unresolved results rather than an enlarged tolerance.

## 6. Q5 — Resampling and uncertainty

**Disposition: REQUIRES CHANGE.**

### R4 — Define the statistical target and every bootstrap outcome

Resampling whole seed maps is the correct structure for the declared independent runs. Recomputing the mean, spatial averaging, threshold, edge and fitted distance on each draw is also appropriate. The point that needs repair is the inference attached to that procedure. [C §§2.5, 5.5, steps 1 and 9]

**The invalid-draw branch is incomplete.** More than 5% of 1,000 resamples failing step 4 makes the level uninformative. The contract says nothing about one through fifty failures, including exactly fifty. An empty/full replicate has no observed edge, and a replicate failing the minimum counts lies outside the informative domain. Dropping it, assigning infinity or conditioning on valid draws gives different quantiles. The coincidence between a 5% failure allowance and a 95th-percentile bound makes this consequential. [C §5.5, steps 4 and 9; §7, row 5]

**Required repair.** Give every draw a typed result; persist valid/invalid counts and reasons; prescribe the treatment of the failure mass and the exactly-5% case. Do not silently redraw until 1,000 valid samples exist. One conservative, executable option is: more than fifty failures → unstable edge; one through fifty → retain the point-estimate information but withhold a decisive uncertainty classification; zero → apply the declared percentile rule. If L1 instead proposes conditional-on-valid quantiles to retain sensitivity, name that conditional target and qualify the selection procedure explicitly. Assigning an absent edge infinite scientific discrepancy is not a neutral convention.

**Name the population target.** A natural target is the contour discrepancy of the edge of the spatially smoothed **population mean finite-tail occupancy** on this fixed terrain, object and horizon. It is neither the mean of per-seed discrepancies nor a statement about the typical seed's edge. This distinction should appear with the confidence procedure, not only in the map description.

**Treat 95% as nominal until qualified.** Thresholding, topology changes, quantiles and minimization make the statistic nonsmooth at some of the very configurations the evaluator must handle. Twenty independent maps and 1,000 resamples do not establish 95% coverage by themselves. More resamples reduce simulation error in the bootstrap calculation; they do not create additional independent lattice realizations.

I do not reject percentile resampling categorically. It is a candidate procedure whose full decision behavior must be qualified, including near-θ plateaus, varying slopes, changing components, competing minimizing contours and informativeness selection. Use the same resampled occupancy map for the two index comparisons within a level; respect the declared independence between runs at different arms/levels. Keep any empirical guarantee restricted to the declared ensembles. [C §6.2; L2-D §4]

## 7. Q6 — Aggregation and failure precedence

**Disposition: REQUIRES CHANGE.**

### R5 — Make the level, arm and flight rules total and mutually consistent

The principal structure is sound: a conjunction over all seven required arms per composition, D on TB, separate B/D outputs, and retention of every required arm even when it supplies no usable edge. A no-edge arm is ND for this conditional boundary question on every required terrain. The contract does not separately predict that an occupied region must exist at θ. Consequently, wholesale absence of an edge need not be an adverse boundary-shape observation. Partial absence of a predicted component when an informative edge remains is a different case, addressed in R2. [C §§1.2, 3.3, 5.6–5.7]

Three repairs are required:

**First, complete the per-level table.** The case **own adverse / rival unresolved** is absent. It must preserve adverse evidence about the own family while recording that the rival has not been established. It is neither “follows rival” nor “follows neither.” A separate B status and discrimination status avoid losing that information. [C §5.6, per-level table]

**Second, resolve a direct precedence conflict.** Suppose exactly two levels are informative, adjacent and own-adverse. Section 5.6 makes the arm ADVERSE. Section 7's higher-priority row 6 makes it ND because fewer than three levels are informative. Both cannot govern the same record.

I recommend making three levels the minimum for **affirmative compatibility**, while allowing the declared two-level adverse condition to decide the arm before the insufficient-levels-for-support branch. Then give level, arm and flight states separate precedence rules. Alternatively Mike may require three informative levels for all arm adjudication, but that is a change to §5.6's adverse rule and must be stated. The isolated-adverse row already says “unless rule 9 applies”; I do not claim that particular proviso is absent. [C §5.6, arm rule; §7, rows 6–9]

**Third, define adjacency and prerequisite propagation.** I recommend adjacent positions in the original registered κ grid, both informative, without bridging an intervening uninformative level. Freeze this convention. State how missing/corrupt mandatory input affects both B and D and distinguish a prerequisite failure from scientific ND. The flight-level table already recognizes “no qualified scientific determination”; that state needs consistent application to D and to the record graph. [C §§5.6–5.9, 7–8]

The two-adjacent-level condition is defensible as a prospective replication requirement. It does not independently establish a flight-wide error rate: it searches across levels and arms, with overlapping adjacent pairs. Its operating behavior must be qualified at the decision units actually reported. Preserve an isolated adverse level explicitly even if the arm-level result is ND; the statement that adverse results are never recast needs to distinguish the retained level finding from the arm's stricter confirmation rule.

D's current wording requires three witnessing levels in **each** TB arm; it does not require the same three κ values in both arms or compatibility at every other level. I accept that limited existential reading if it is made explicit and the witness sets are reported. D can therefore be distinguished while B fails elsewhere. If matched κ witnesses are intended, write that different rule before qualification. In either case, qualify the complete two-arm D decision, including its search over levels.

Similarly, a B pass should identify the realized informative domain. Passing all informative levels is not evidence that every one of the fifteen levels yielded a usable boundary. The predeclared information filter may be applied mechanically; it may not be changed to discard an adverse observation.

## 8. Q7 — Diagnostic K

**Disposition: REQUIRES CHANGE.**

### R6 — Separate finite-horizon persistence from an estimated coupling effect

K as drafted is a useful persistence profile of the coupled skeleton. It is not yet the effect estimate and uncertainty requested in the advice. No intervention, matched independent-response comparator, value of d₀, or signed difference estimand is declared. Counts, a selected threshold and a bracket from the coupled arm alone cannot answer how much a coupling intervention changes the result. [C §§1.3(a), 5.4; A §2]

The justification also conflates two different thresholds. Independent cells with activation hazard g d₀ λᵢ have no absorbing all-zero state when g, d₀ and λᵢ are positive. They can nevertheless have a **finite-horizon survival-probability crossing**. For those independent chains,

\[
a_i(g)=1-e^{-g d_0\lambda_i\Delta t},\qquad
p_i(g)=\frac{a_i(g)}{a_i(g)+q},\qquad
P(\text{all zero at a stationary tick})=\prod_i(1-p_i(g)).
\]

The probability of remaining nonempty over a finite tail varies with gain, initialization, population size and horizon. It can cross the instrument's 18-of-20 criterion without the all-zero state being absorbing. Conversely, the finite coupled skeleton is eventually absorbed at finite gain; its reported threshold is itself a finite-design persistence statistic. Thus “no absorbing state” does not imply “cannot reproduce a finite-tail persistence crossing.” [C §§1.3(a), 5.4; F8 §1.1′; L2-D §3.3; derivation from the supplied two-state rule]

The reported bracket is also **grid resolution, not sampling uncertainty**. Eighteen survivors out of twenty is an operational count rule, not proof that the population survival probability is at least 0.9. Even twenty successes out of twenty have a one-sided exact 95% lower bound of 0.05^(1/20) ≈ 0.8609. A bracket formed from observed counts does not incorporate that sampling uncertainty.

**Recommended scope-preserving repair.** Keep mandatory, non-gating K, name it a skeleton persistence diagnostic, and remove the claim that it excludes the independent-response alternative. Report s/20 with a frozen binomial interval procedure and confidence level, explicitly pointwise unless a simultaneous procedure is specified. Retain κ̂_c and its grid bracket as operational panel summaries. Define censored/no crossings, the four curve descriptions and nonmonotone precedence using the same 18/20 criterion throughout. A stable suffix must not erase an earlier nonmonotonicity. Preserve the disclosure that the general pattern was already seen in the probe. [C §§1.0, 1.3(a), 5.4]

If Mike wishes to retain the stronger purpose “coupling contrast,” the alternative repair is a specified comparison/intervention, matching rule, effect estimand and uncertainty procedure. That is a prospective scientific choice. It is not required merely to retain the narrowed B/D claims, and a favorable K result must not silently enter their conjunction.

## 9. Q8 — Known-answer and statistical qualification

**Disposition: REQUIRES CHANGE.**

### R7 — Freeze truths and error predicates for the actual complete procedure

Separating implementation qualification from statistical qualification, retaining independent seed maps, using design and held-out ensembles, counting halts, and closing the stage on failed qualification are sound protections. The six named risks are the right risks. Their present descriptions do not yet define executable, independently known truth or the promised arm/flight error targets. [C §6; D §10.1; L2-D §4]

**Known-answer class 8 is not valid as a general construction.** “An edge displaced 4 cells from a contour” need not be adverse when the fitting level is free: that edge may be exactly another eligible contour of the same index, with minimized discrepancy zero. A uniform location change was expressly assigned to fidelity in the prior consultation. Construct the adverse control beyond ε from **every eligible contour**, and certify its minimized target independently. A displacement from one chosen reference contour does not establish that truth. [C §6.1, class 8; §5.5, step 7; L2-D §3.2]

Classes 1–3 likewise need specified h functions and truths for the smoothed target; class 4 needs a defined periodic rotation/resampling construction and certified separation from both families. Add the estimator, small-component, empty-candidate, invalid-bootstrap and aggregation cases identified in R1–R5. Their exact labels and causes should be determined by the registered definitions, not chosen because the evaluator happened to return them.

**The statistical generator needs a frozen declaration.** Specify the h functions or ranges, occupancy slopes and crossings, noise distribution and covariance, treatment at 0/1, and the estimators converting calibration data to per-seed amplitude and correlation length. Distinguish variation among individual seed maps from the standard error of their mean. Freeze those transformations before calibration output exists; derived numerical parameter values can then be committed at build. A statement that parameters are “taken from calibration” leaves too much discretion. [C §6.2; §8, job 0]

For every capped class or declared mixture, a table must give:

| Required declaration | What must be fixed |
|---|---|
| Case generator | Terrain/family, h, noise law and parameter ranges, calibrated transformations |
| Decision unit | One level, whole arm, seven-arm B composition, or complete two-arm D |
| Truth | Post-estimator target and its relation to the eligible family/ε; any intended unavailable cause |
| Sampling | Number of independent cases; subcase counts or mixture weights; design/held-out roles |
| Error | Exact numerator, denominator, forbidden outputs, and wrong-cause/halts treatment |
| Acceptance | Cap, confidence construction, completeness and join predicates |

The six risks are not interchangeable case types. In particular, include false compatibility on neither-family maps, sensitivity on adequately separated alternatives, and the full D search across both arms. A seven-arm B conjunction alone does not qualify D. If 200 cases apply to a mixed risk class, state the mixture and limit the guarantee to it; that does not automatically bound each rare subcase. No expansion to a particular number of strata is imposed here, but the allocation and the scope of each cap must be unambiguous.

**Near ε, price uncertainty rather than demand impossible uniform resolution.** Specify which outputs are errors at displacements 1.0, 1.5, 2.0, 2.5 and 3.0. Sensitivity targets should apply at declared separation margins. At the boundary, an unresolved result is not automatically an error; report its rate and specify the false-decisive-error target. Reporting rates alone is insufficient if the contract also claims a cap without identifying which rate is capped.

The stated binomial cutoff is correct: the one-sided 95% Clopper–Pearson upper bound is approximately **0.0954014 at 12/200 errors** and **0.1013570 at 13/200**. Thus the 0.10 cap permits at most twelve errors. This is a per-declared-class/mixture guarantee, not automatically simultaneous over classes or transferable to canonical lattice data. [C §6.2; independent calculation]

Finally, class 10's calibration dependence and the held-out-master timing must be reconciled with the job order. Those execution defects are addressed in R8.

## 10. Q9 — Remaining conditions before freeze

**Disposition: REQUIRES CHANGE.**

### R8 — Repair the job order and make record dependencies explicit

The job list and carried distinction between completeness and readiness are appropriate. The ordering has a direct calibration conflict and an unresolved master-draw dependency:

1. Section 8 orders the known-answer corpus before masters and calibration, but §6.1 class 10 requires the calibration amplitude.
2. The blanket “masters drawn” step precedes calibration, while §6.2 requires the held-out master only after the generator is frozen; that generator's numerical noise parameters come from calibration. If the blanket step includes held-out before the complete generator is sealed, it conflicts with that requirement. If “frozen generator” means a previously frozen function of later calibration inputs, that meaning and the permitted derivation must instead be explicit.

**Required repair.** Either make the implementation corpus fully independent of calibration, or put its calibration-dependent cases after the calibration record. Separate the calibration, design, held-out, evaluator and scientific master-draw stages. An admissible sequence is: freeze declarations and calibration estimators; build and verify the rule/recorder; seal canonical arrays; draw and run calibration; enforce its stop condition and seal derived generator parameters; run the completed implementation corpus; freeze the qualification declaration; draw/run design; draw/run held-out under the stated restrictions; join qualification; then run authorized scientific jobs. This is a dependency recommendation, not authorization to execute it. [C §§6.1–6.2, 7–8]

For each job, declare its outputs, prerequisite identities, whether each prerequisite requires passage or valid completion, and its failure consequence. Section 5.9's “every record” binding must distinguish a preexisting **qualification protocol identity** from a subsequent **qualification result identity**. Calibration and qualification records cannot be required to cite a future result without an expressly defined schema. The present wording is ambiguous, rather than proof that a particular implementation already contains a cycle.

Make the resource benchmark cover the evaluator and qualification as well as lattice dynamics. Under the literal 99-candidate/1,000-resample design, fourteen realization arms at fifteen informative levels require up to **41,580,000 bootstrap candidate comparisons per θ**; three θ values make **124,740,000**, before stability and qualification. These are comparison counts, not a runtime estimate; caching may substantially reduce work. The probe's per-run lattice cost does not price that part of the program. [C §§5.5, 6, 8; arithmetic]

### R9 — Finish the T0 and mandatory-reporting specifications

**T0 remains a non-gating scientific consistency exercise.** The constant-array step reduction is the apparatus check. The current separation is correct, and repetition of the four tests does not resolve entering-interval onset continuity. [C §§5.1, 5.8; CL §3; L2-D §11.7]

The T0 numbers reproduce, but the grid rule needs completion. The κ grid has gaps of 0.10, 0.25 and 0.50, whereas Δκ uses 0.10 as the carried spacing term. Retain 0.1254 only with an explicit fine-grid applicability/unevaluable rule, or define the relevant local-gap rule prospectively. If it is simply a nominal declared tolerance rather than a discretization allowance for the entire grid, say so. I do not require automatically substituting the largest gap. State the actual slope normalization for f_J on nonuniform intervals, the test domains, and the calibration-band formula and object-specific inputs being redeclared. “Flight 8's four tests” plus an unnamed new band is not a fully resolved changed-grid procedure. [C §§2.9, 5.8; Appendix A.4; F8 §§3.4, 4.11]

Name T0's reference explicitly. If “T0's measured boundary” means its control-axis persistence threshold κ̂_c,T0, write that, with its sampling and absent/nonmonotone cases. T0's constant spatial index has no nonempty level-set contour; a noise-generated spatial occupancy edge is a different object. [C §§1.2′, 4.3, 5.8]

The existing mandatory reports also need a compact frozen schema:

| Report | Missing specification to complete |
|---|---|
| Whole-map contour constancy | Raw or smoothed occupancy target; contour-bin construction, ties, minimum membership, weighting and the zero-total-variance result |
| Measured margins | Exact band/core definitions and numerator/denominator, cell weighting, W and seed aggregation, and empty-denominator states; fixed cut values alone do not define a ratio |
| Flicker distributions | Occupancy-band membership and aggregation across cells/seeds, while retaining the already declared counters, censoring and undefined states |
| Fidelity comparisons | Actual uncertainty recipes for shifts, edge-local m, occupancy discrepancies and fitted levels; distinguish grid brackets from sampling bounds |
| Skeleton boundary report | Whether the map is unconditional across all twenty seeds or conditioned on survival, and how finite tails of extinct runs enter it |

These complete existing reporting obligations. They do not introduce new scored science. The previous design requirement about bins is not discharged by §5.5's 99 **contour candidates**, which are a different construction from bins in the whole-map variance report. A missing required reporting record must prevent a completeness claim, without turning an unfavorable reported value into failure of B or D. [C §§1.2′–1.3, 5.7, 12; D §§5, 10.1–10.3; L2-D §§11.2, 11.4; I004]

Also preserve the distinction between finite-tail lattice means and the closure fixed point. Their comparison is legitimate fidelity reporting, but its discrepancy includes finite-time/nonequilibrium effects and cannot automatically be called isolated stationary closure error. No additional convergence experiment is required merely to state this limitation. [C §4.2; L2-D §9.3]

### R10 — Reconcile array identities and the supporting arithmetic record

Section 3.4 first says the freeze commits base-array hashes, then says the canonical hashes of record are derived at build; §9 follows the latter. Replace this with one ordered procedure: freeze formulas, parameters, serialization and numerical comparison rules; keep container hashes explicitly provisional; build, commit and bind the canonical arrays and derived contours before their use. State which numerical spectral values are normative and how cross-environment recomputations are checked.

The array-byte convention must name shape, dtype, byte order, axis ordering and concatenation order. The supplied base hash concatenates C-contiguous native float64 bytes in v/u/r order. Explicit serialization removes dependence on unstated platform defaults. A per-element 10⁻¹² tolerance checks numerical agreement; it does not guarantee identical threshold masks near ties or identical categorical decisions. Bind the canonical masks/levels used in scoring and qualify the comparison convention. [C §§2.8, 3.4, 5.9; AR]

The current contract's job counts are correct. The supporting script and `contract_arith.json`, however, still report **stability = 9,000**, whereas §8 job 5 specifies **8,400** non-T0 runs. Correct the supporting script/output or clearly label that field as superseded. Appendix A.6's generic full-panel count of 9,000 is correct; it is not the erroneous field.

Three smaller corrections belong in the same arithmetic/provenance repair:

- `monotone_related` claims to check identical weak orderings but does not enforce constancy within ties. The arrays [0,0] and [0,1] pass its bidirectional check despite different contour families. The present terrain-role classifications are independently justified by their formulas; repair the helper before making it the procedure of record.
- `td_final.py` writes `td_final.json` in its working directory, ignoring the purported second output-path argument. Correct the instruction or script interface.
- Update the header's “none committed yet” statement for the arithmetic scripts to match the packet's committed provenance, while keeping freeze status distinct from mere repository placement.

None of these observations authorizes modifying historical records. L1 should submit revised contract/supporting bytes and their new identities through the next review packet.

## 11. Check of the contract's requirements trace

The trace in C §12 names appropriate locations, but several rows indicate only partial discharge. The table below distinguishes accepted design choices from unfinished implementation declarations.

| Earlier design-consultation requirement | Round-1 finding |
|---|---|
| Q1: two conditional tests, boundary versus whole map, independent edge, nonvacuity, alternative, roles and labels | Claim architecture accepted. Complete the discrepancy, case table and explicit unoriented-edge limitation under R1–R5. |
| Q2: six-risk statistical qualification, independent units, untouched held-out | Architecture accepted; generator, decision units, error table and ordering require R7–R8. |
| Q3: rival status, effective-gain reduction, untested candidates | Substantively discharged by C §§1.1′, 2.2 and 5.1. The reduction remains a future build check. |
| Q4: spectral normalization and rule-specific equivalence | Substantively discharged by C §§2.8 and 10. Complete numerical identity conventions under R10. |
| Q5: flicker estimand, windows, censoring, floor reference and levels | The prospective recording obligation is explicitly resolved by PP §6 and carried in C §2.11. Finish reporting aggregation under R9. |
| Q6: onset continuity left open | Discharged; no new onset experiment is required here. |
| Q7: skeleton spectral comparison, local benchmark, matched estimand, solver and T0 | Main distinctions repaired; uncertainty, T0 object and finite-tail/fixed-point qualification need R6/R9. |
| Q8: probe provenance and prospective timing | Disclosures and ratified pre-probe timing are present. Preserve the stated selection limits and the distinction between attestation and independent verification. |
| Q9 §11.1: TC and the ungated floor | Discharged as near-face suppression with the exact-face limitation stated. |
| Q9 §11.2: contours, bins, membership, contrast and seed aggregation | Seed-mean choice is explicit. Candidate conventions and the separate whole-map binning report remain open under R1/R3/R9. |
| Q9 §11.3: spatial scale, TD geometry, fixed cuts | Scale and design geometry are explicit and reproduced. Complete the measured-side definitions under R9. |
| Q9 §11.4: own record graph and mandatory reports | Principles and jobs are present; complete type-specific dependencies, identities and reporting predicates under R8/R9. |
| Q9 §11.5: fresh calibration and stream dependence | Independent runs and separate calibration role are declared. Freeze calibration estimators and their derived uses under R7–R9. |
| Q9 §11.6: adverse/unavailable paths and precedence | Partial; resolve invalid resamples, missing table entries and the two-level contradiction under R3–R5. |
| Q9 §11.7: T0 reduction versus replication | Role separation accepted. Complete its changed-grid and band definitions under R9. |

The append-only notation rows proposed in C §10 are appropriate. Their placement in the governing notation record remains part of freeze; this review does not rewrite existing rows. [N §§1, 2a]

## 12. Verification record

### 12.1 What was executed

The archive, manifest and all payload identities were checked, including coverage, duplicates and CRC integrity. The arithmetic review used separate output directories and preserved the received source bytes. No canonical lattice job, new terrain probe, probe-output boundary analysis, instrument qualification or Flight 9 build test suite was executed.

All six supplied arithmetic scripts were inspected and run on their terrain/spectral/closed-form paths:

| Script | Result |
|---|---|
| `f9_step1.py` | Exit 0; reproduced `step1.json` |
| `tb_r0.py` | Exit 0; reproduced its arithmetic output |
| `td_counts.py` | Exit 0; reproduced its geometry output |
| `td_final.py` | Exit 0; reproduced `td_final.json` in an isolated working directory |
| `f9_contract_arith.py` | Exit 0; reproduced `contract_arith.json` |
| `smooth_check.py` | Exit 0; all six supplied half-height disc checks reproduce |

**Review environment:** Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, Linux x86_64 with glibc 2.41. This differs from L1's disclosed Python 3.13.18 / NumPy 2.5.3 / SciPy 1.18.1 environment. Nevertheless, the three JSON outputs are byte-identical, not merely within tolerance:

| Reproduced JSON | SHA-256, equal to received file |
|---|---|
| `contract_arith.json` | `733d6b8ade0762313b6ba8c55efe1464be858fea8948f93e0c06154cdad57562` |
| `step1.json` | `ba59630c43d6741a5fc1b46487092ce5e8aa647f43d33b538e6aae67086c287a` |
| `td_final.json` | `82b8d83ac7a68503803da2c3f09baefaaa7b830d15748d457ce933b213580422` |

Independent checks covered the TB variance decomposition, sparse-matrix spectral calculation, the finite-size upper-term inversion, the Clopper–Pearson cutoff, candidate emptiness/duplicates, and the separate missing-component example. These are arithmetic or synthetic checks, not observations of a Flight 9 lattice response.

### 12.2 Principal numerical results

| Item | Reproduced result and interpretation |
|---|---|
| TB product variance shares | x = 0.5172726278353565; y = 0.48272737216464306; interaction ≈ 3.89×10⁻¹⁶ |
| TB H max/min | 1.1590909090909092, matching 1.16 |
| TD core sizes | Exactly 2,000 cells in all four variants |
| TD lattice perimeters | 200, 200, 416, 416 |
| TD 10–90% band counts | 676, 1,376, 1,424, 2,816; ratios 0.338, 0.688, 0.712, 1.408 |
| TD edge clearance | Closest cell approximately 0.0314 cells for the one-disc geometry and 0.0603 for the four-disc geometry, both above 0.03 |
| Appendix A.1 | All supplied array hashes and spectral values reproduce; independently constructed symmetric sparse operators agree at the table's printed precision |
| Independent spectral comparison | Largest difference from the supplied iteration ≈ 2.28×10⁻¹², on TC/H; this is a scalar solver comparison, not a violation of the per-element array tolerance |
| TB decile separations | All eighteen values reproduce; minima 14.2778483 cells P-to-H and 14.0288690 H-to-P; same-family examples reproduce zero at the tested deciles |
| Deactivation and floor | q = 0.18126924692201818; π₁ = 0.052282320137314486; 1/q = 5.516655566126993 |
| Any-activity floor references | W=1: 0.0522823201; W=10: 0.1342435537; W=100: 0.6496006856 |
| T0 finite-size arithmetic | Lower term 0.0254051377395; upper term 0.00548314285140; with nominal 0.10 spacing, Δκ = 0.1254051377395 |
| Independent-chain mean-map SE approximation | 0.00484096, 0.00633916, 0.00791285, 0.00840207, 0.00751387 at the five stated occupancies; these are the stated approximation, not lattice precision evidence |
| CP cap | 12/200 errors clears 0.10; 13/200 does not |

The contract's listed dynamics counts total **26,700**: calibration 9,000; T0 900; non-T0 skeleton 4,200; non-T0 realization 4,200; stability 8,400. Qualification activity and resource benchmarks are additional. The approximately two-hour estimate for a 9,000-run panel is consistent with the existing probe runtime table; it is a projection from that environment, not a canonical-machine measurement. [C §8; PR, runtime report; AR]

No substantive numerical discrepancy was found in the draft's printed Appendix A values. The stale supporting stability field, implicit conventions and T0 spacing interpretation remain the repairs identified above. Exact reproduction of precursor arithmetic does not establish the statistical properties of the future evaluator.

### 12.3 Limits of this review

The packet contains no built Flight 9 evaluator or canonical observations to validate. The review assesses a contract candidate, independently reproduces its supplied arithmetic, and tests several definitions with analytic/synthetic counterexamples. It does not certify future implementation, calibration precision, qualification passage, usable edges on TB/TD, or any scientific endpoint.

L1's statement that no probe edge endpoint was inspected is retained as a provenance disclosure. The supplied packet cannot independently prove a negative about unrecorded activity. This review neither assumes an undisclosed violation nor upgrades the disclosure into forensic verification. No outside source or absent Annex material was used.

## 13. Source key

The receipt row identifies the exact full path and SHA-256. Section references throughout use those received bytes.

| Key | Source | Receipt row |
|---|---|---:|
| I | L1 contract-review instruction, 2026-11-13 | 1 |
| C | `FLIGHT_9_CONTRACT_v0_2.md` | 2 |
| A | L2 advice on contract questions, as received 2026-11-13 | 4 |
| AR | Six arithmetic scripts and three supplied JSON outputs | 5–13 |
| D | `FLIGHT_9_DESIGN_NOTE_v0_3.md` | 14 |
| L2-D | L2 design consultation, as received 2026-11-12 | 15 |
| PP | Ratified pre-probe declaration v1.0 | 16 |
| PR | Probe record and report; probe functions/identities where specifically identified | 17–21 |
| F8 | Frozen Contract F8 v0.8.4 | 22 |
| CL | Flight 8 stage-1 close record v1.0 | 24 |
| I004 | Interpretation 004, flicker reporting obligation | 25 |
| PD | Participation rulings PD1–PD7 | 26 |
| N | Notation-scope ruling v1.1 | 27 |
| S | Frozen merge specification v0.4 | 28 |
| O | Overview v1.8.1 | 29 |

The placed scalar dynamics/configuration files are receipt rows 30–31. They support the declared reduction target; no Flight 8 source was modified.

## 14. Required return before reconsidering freeze

| Repair | Concrete closure needed |
|---|---|
| R1 | Post-estimator component scope and deterministic estimator cases, with certified outcomes |
| R2 | One explicit choice about D95's perimeter-weighted claim versus component-sensitive scoring |
| R3 | Complete contour/quantile/empty/tie rules and a claim that matches the searched family |
| R4 | Named bootstrap target, complete invalid-draw treatment and qualified nominal bounds |
| R5 | Complete level table, consistent arm/flight precedence and fixed adjacency/prerequisite propagation |
| R6 | Honest persistence-only K, or a specified coupling effect; sampling uncertainty and all crossing cases |
| R7 | Frozen generator/error table, valid known answers, and complete B/D qualification units |
| R8 | Acyclic execution dependencies, explicit master timing and type-specific identity bindings |
| R9 | Completed T0 grid/band rules, reference object, reporting schema and fidelity qualifications |
| R10 | Consistent canonical-array identity procedure and corrected supporting arithmetic/provenance |

The accepted design choices can remain while these changes are made: separate B/D claims, the disclosed fixed θ, seed-mean occupancy with an explicitly qualified spatial mean, periodic bond edges, free contour location, a declared two-cell resolution, the full TD crossing, independent streams and fresh validation. The next packet should identify Mike's rulings on the substantive alternatives and show how the revised clauses, qualification declaration and trace agree. Nothing in this review authorizes freeze, build, a master draw or a scientific run.

CONTRACT DISPOSITION: NOT YET FREEZABLE
