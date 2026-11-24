# L2 → L1 and Mike — Flight 9 Interpretation 002, draft 1, round 1 review

**Date:** 2026-11-23  
**Register:** Review of a proposed interpretation record for the fidelity summaries of Contract F9 v0.7 §1.2′(ii)–(iii).  
**Decision authority:** Mike.

**Archive reviewed:** `f9_interpretation_002_round1_L2.zip`  
**Archive SHA-256:** `b489e5d703d592343f319ff164b19ddd27d3e37a4a27168026ffa7033490224b`  
**Draft reviewed:** `flights/mfa_fidelity/rulings_draft/F9_INTERPRETATION_002_FIDELITY_SUMMARIES_DRAFT_1.md`  
**Draft SHA-256:** `b2efdeda1d063ccb6d46d66e0c8d0881d5131015221d1e4f20fb6bed943d1a07`

## 1. Disposition and evidence boundary

**Draft 1 needs one contained repair before acceptance: Point 8 must make draw generation independent of the availability of an observed summary.** Its current trigger leaves room for two implementations that produce materially different reports. One can omit defined resampled local-m summaries when the observed boundary is absent and the closure is unavailable. The draft's own subsequent sentence, and the consultation package Mike adopted, require those draw values to be considered. Finding D1 below gives an exact constructed example and a narrow repair. [D, Point 8, lines 107–113; A, §3.G, lines 190–198 and §6, line 317]

The selected statistics otherwise substantially reproduce the consultation advice. The seven restated constraints conform to the frozen contract. The optional closure-to-family fits and fitted-level differences remain the one additional substantive choice correctly marked for Mike's confirmation. That visible pending choice is not itself a defect in a draft submitted for review. The smaller clarifications below should make the revised record easier to implement without changing its selected report. [D, lines 3–28, 77, 92; A, §6, lines 310–319]

I computed the archive and all payload digests, completed the receipt before review, and reverified them after “execute.” The archive contains exactly **14 manifest-listed payloads plus MANIFEST.txt**; all 14 payload digests match, with no missing, additional or duplicate payload entries. Appendix A contains the full digest table and defines the source keys used throughout this review. The received consultation advice is also byte-identical to the earlier response available in this workspace, with SHA-256 `c9df277a8d38449b2c37417e167a1aa6971f2fd8081a4283cac0f9cdf8b0156b`.

This assessment concerns the supplied draft as a governance record. I read the review packet first, compared the draft with the received advice, frozen contract, freeze record and existing rulings, and inspected the relevant reference functions. I executed the synthetic arithmetic witness described below. No implementation of the proposed reports, Flight 9 job, master drawing, probe-array inspection or repository placement was performed. The packet's assertion that its reference files come from pin `c6c21c497366d3ca71e0487127c774aacfd14ba1` is recorded as L1's provenance statement; I did not independently fetch that remote pin. [P, lines 3–6]

## 2. D1 — Point availability must not gate the draw set

### 2.1 The conflicting readings

Point 8 says, “The draws are made whenever any summary of the level is defined.” It then says that definition is assessed on each draw independently, and that an unavailable observed value can coexist with a range. The consultation explicitly recommended this independence. [D, lines 107, 109–113; A, lines 194–198]

The first sentence does not expressly command skipping when all point values are unavailable. Its problem is that it leaves that implementation open. One builder can read “defined” as a property of an **observed** summary and use it as the bootstrap eligibility test. Another can generate the declared draws for an applicable statistic and evaluate its definition on each draw. These procedures disagree in a state the draft is supposed to handle.

Consider a non-T0 realization level with valid seed maps and a valid fixed local-m field. Its observed region is empty, and its matching closure is recorded as nonconverged. Under Points 4 and 9, the observed edge-cell summaries are absent and the closure-dependent summaries are unavailable. The placed evaluator also does not supply an item-(iv) bootstrap at an uninformative observed point. Nevertheless, some replacement draws can have an edge and therefore define Point 2 and the against-1 contrast in Point 3. [D, lines 56, 123–125, 138; EV, lines 421–434]

An unavailable comparator is an allowed scientific state, not an excuse to suppress a quantity that does not use that comparator. This is exactly why the consultation separated field dependencies and point availability from draw availability. [C, §4.2 and §7; A, lines 196, 219–234]

### 2.2 Exact constructed witness

I constructed 40 integer tail-count maps on the registered 100×100 lattice. Nineteen maps have count 400 on a 20×20 patch and zero elsewhere; the other 21 maps are zero. Counts are over a 1,000-tick tail. The observed mean on the patch is therefore 0.19, below θ = 0.20 even at the maximum of its 3×3 mean.

A valid 40-occurrence replacement draw repeats one patch-bearing map and omits one zero map. It has 20 patch-bearing occurrences and 20 zero occurrences. Its interior patch mean is exactly 0.20. Because ties are included, smoothing leaves an 18×18 occupied region. The computations use integer box sums, so the threshold comparison does not depend on a floating-point approximation to 0.20. This implements the declared geometry for this witness. [C, §5.5 steps 1–4; EV, lines 150–162]

| Quantity | Observed map | Valid replacement draw |
|---|---:|---:|
| Patch-bearing map occurrences | 19 | 20 |
| Zero-map occurrences | 21 | 20 |
| Maximum unsmoothed mean | 0.19 | 0.20 |
| Maximum integer 3×3 numerator | 68,400 | 72,000 |
| Included threshold numerator | 72,000 | 72,000 |
| Region cells | 0 | 324 |
| Complement cells | 10,000 | 9,676 |
| Boundary bonds | 0 | 72 |
| Distinct inside edge cells | 0 | 68 |
| Distinct outside edge cells | 0 | 72 |
| Passes step 4 | No | Yes |

Thus the draw supplies both endpoint sets and their fixed-field m statistics, even though the point supplies neither. Closure unavailability is an assumed dependency state in this example; no closure solver was run and no claim is made that a canonical realization produced these maps or that a particular declared stream contains this exact draw. The draw has positive support under replacement sampling. That is sufficient to show that point absence does not imply draw absence. The executed witness and its limits are reproduced in Appendix B.

### 2.3 Required repair

Replace the eligibility sentence with an explicit rule based on the **applicability and fixed dependencies of each selected statistic**, not its observed value. For example:

> For complete valid inputs, make the declared 1,000 draws for each applicable stochastic summary independently of whether its observed value exists. In particular, the edge-cell summaries of every covered non-T0 realization level receive those draws even when the observed region is empty or full and the matching closure is unavailable. A field's dependencies that are fixed across draws remain fixed; the absence of an observed edge is not such a dependency.

Then specify the accounting for fields blocked on every draw by a fixed dependency: distinguish a field not attempted for that reason from a field assessed on 1,000 draws with zero defined values. An unavailable closure must not prevent drawing for other applicable fields. Where a matrix is already generated for those fields, the closure-dependent fields retain their static cause; no replacement matrix is made. A uniform policy of generating the matrix for every complete valid covered panel is also determinate, but is not necessary to repair this case.

The implementation must reuse the declared matrix within the arm/object/level. It must not introduce new contour fits for item (iv) when the placed evaluator did not resample. The fidelity calculation and the scored evaluator retain their different applicability domains. The supplied generator can produce the multiplicities independently of point geometry or family availability, so this clarification requires no change to the placed evaluator. [D, lines 107, 117, 138; EV, lines 382–388, 425–434; C, §5.5 step 9]

This repairs the expression of the already adopted independent-draw rule. It does not need a new scientific choice from Mike. If L1 instead wants to condition these ranges on having an available point summary, that is a different reading and must be put before Mike explicitly; it cannot be introduced as a build convention. [A, lines 196, 297–308, 317]

## 3. Q1 and Q2 — Advice fidelity and determinacy of Points 1–10

The answer to Q1 is **substantially yes, with D1 as the material weakening**. The answer to Q2 is that the reductions are largely determinate once the explicitly deferred conventions are declared, but Point 8 does not yet pass the two-builder test. The following table identifies the remaining boundaries precisely.

| Point | Assessment against the advice and determinacy for a build |
|---|---|
| **1 — Edge cells** | Accurate and determinate. Use two distinct endpoint sets, with equal weight within each; include endpoints of all components. This changes neither bond weighting in S nor the corner convention. [D, lines 30–36; A, lines 50–60] |
| **2 — m summaries** | Accurate and determinate after the spatial-quantile convention is declared. “Six numbers” means count plus minimum, Q25, median, Q75 and maximum. Raw local m, its actual persisted artifact and the rounded contour comparison array are correctly distinguished. The placed arithmetic from recorded gain resolves the earlier algebraic-versus-bitwise issue. [D, lines 38–42, 109; A, lines 62–80; SP, lines 73–81] |
| **3 — Benchmarks** | Accurate and determinate. The two median differences, micro-unit conversion, fixed T0 reference, conditional uncertainty and separate persistence description are explicit. An all-levels-met T0 reference can remain available and lower-unbracketed; it is not contingent on T0 receiving a favorable scientific outcome. [D, lines 44–48; A, lines 84–96; I001, line 42; O, lines 471–473] |
| **4 — Edge-summary availability** | Accurate adoption of the recommended reading. A nonempty non-T0 realization boundary supports m summaries even below the informative minimum; empty/full regions do not. Final adverse, unresolved or unstable labels do not erase defined point values. [D, lines 50–56; A, lines 204–213] |
| **5 — Occupancy residuals** | The unsmoothed errors, three losses, whole-map priority, regional reselection and point-only maximum location are determinate. Clarify that the regional counts are cardinalities, with zero a defined count when a subset is empty; the three residual statistics on that empty subset are unavailable. Preserve the chosen closure dependency as discussed below. [D, lines 58–69, 109; A, lines 98–121] |
| **6 — Closure map** | Deterministic geometry and the non-gating nearness diagnostic follow the advice. The closure fit is visibly conditional on Mike's inclusion. If retained, spell out its own step-4 gate before calling the low-level fit helper; the helper itself does not apply that gate. [D, lines 71–77; A, lines 123–135; EV, lines 333–364] |
| **7 — Edge comparison** | Direct S is determinate: both maps informative, the complete joint discrepancy, two global terms and every resolved-component term, with no family-fit or final-label gate. For the optional fitted-level difference, give an explicit sign and translated range. Each fit's availability is independent of the opposite map's geometry. [D, lines 79–92, 117; A, lines 137–163, 202] |
| **8 — Coverage and ranges** | Coverage, sampling unit, fixed fields, defined-draw percentiles, component treatment and λ*'s exception follow the advice. **The draw-generation trigger requires D1's repair.** Its correctness cannot be delegated to a helper's point eligibility. [D, lines 94–117; A, lines 169–213] |
| **9 — Unavailable states** | The per-field principle is sound. Label the geometry rows explicitly as point-value availability; draw availability follows Point 8 independently. Keep static dependency failures and apparatus failures distinct, and retain all applicable causes when several fail. [D, lines 119–134; A, lines 215–236] |
| **10 — Existing items** | Correct as an assembly/reuse instruction. The source supplies the threshold-fidelity ingredients and the evaluator's typed fitted-level outputs. This is not certification of an assembled report. Keep the qualification that an adverse fit's diagnostic is the least S **among contours examined**, which may not be the family minimum. [D, lines 136–138; A, lines 238–258; CL, lines 176–219; EV, lines 351–353, 451–462] |

### 3.1 Regional counts: do not condition away zero

Write the two selected count statistics as (n_R(b)=|R_b|) and (n_{\bar R}(b)=N-|R_b|). On a draw with an empty region, the first count is zero and the second is N; bias, RMSE and maximum over the empty region do not exist. Treating that zero count as missing would instead report a count range conditional on nonemptiness, which is a different statistic. The count definition should be explicit when Point 8 adds ranges to these fields. [D, lines 60–65, 109; A, lines 112–117, 194–200]

For a minimal revision, retain Point 9's current scope: when the comparator is unavailable, Point 5 as a closure-comparison block is unavailable, including its attached counts. If L1 intends to retain those counts independently of the closure, say so as a lattice-only field and apply the draw rule to it. Do not let one builder retain them and another suppress them through different container-level null handling. This is a small completion of the record; the existing count language and static-dependency language should be made consistent before implementation. It does not justify striking the count ranges.

### 3.2 Optional fits: state the inherited gates and the signed quantity

If Mike includes the fitted-level diagnostic, use an explicit formula such as

\[
d_\lambda=\lambda^*_{\mathrm{lattice},Y}-\lambda^*_{\mathrm{closure},Y},\qquad
[L_Y,U_Y]\longmapsto[L_Y-c_Y,U_Y-c_Y],
\quad c_Y=\lambda^*_{\mathrm{closure},Y}.
\]

Each fitted level requires **its own** map to pass step 4, an applicable nonempty registered family, and its own fit within ε. The labels must be for the same index Y on the same arm/object/level, as the draft correctly says. A closure fit need not disappear because the lattice map is uninformative; the lattice fit need not disappear because the closure is absent. The point difference needs both point labels. Its translated range can exist without a point difference if the existing lattice evaluator supplies compatible-draw labels and the closure label exists. [D, lines 77, 92, 111, 117, 123–128; C, §5.5 steps 4–9; A, lines 153–159, 196, 202]

These sentences make the incorporated §5.5 rule explicit. I do not infer that the draft authorizes fitting an under-resolved map merely because it names `fit`: Point 6 already imports steps 1–4. The clarification matters because `fit` is a lower-level function; `evaluate_map` supplies the actual step-4 guard. [EV, lines 333–364]

## 4. Q3 — The seven constraints preserve the frozen contract

All seven constraints are substantively conformant. The freeze record makes the unchanged contract's remaining PROPOSED markers values of record; the historical DRAFT heading does not reopen them. [FR, lines 9–15, 38–61]

| Constraint in the draft | Frozen basis and assessment |
|---|---|
| **1. Operational region, edge and components** | Correct: realization seed mean, periodic 3×3 smoothing, θ = 0.20 with included ties, periodic four-neighbour boundary bonds and the prescribed corner convention. Point 1's distinct-cell weighting is a separately selected reduction of m, not a change to S's equal-bond geometry. [C, §1.2″; §5.5 steps 1–3] |
| **2. 1,000 resamples of 40 seeds** | Correct. Point 8 supplies whole seed maps and replacement sampling. Neither the 950-of-1,000 scored rule nor the number of draws is changed. D1 concerns the new report's applicability, not the scored algorithm. [C, §2.10; §5.5 step 9; §5.7 row 4] |
| **3. Unconditional skeleton mean** | Correct. All 40 runs contribute their recorded tails. Restore the contract's explicit phrase “zeros after extinction” for complete restatement; the present text does not authorize survivor-only averaging. [C, §1.3(g); §5.7 skeleton-boundary row; D, lines 24, 101] |
| **4. T0 exclusion** | Correct. T0 has whole-lattice occupancy comparisons and no new region, edge or fitted-level diagnostic. This preserves the explicit prohibition on comparing its spatial edge and follows the advised T0 coverage. [C, §4.3; A, lines 175–180; D, lines 25, 102] |
| **5. Local m** | Correct. Use the raw index and recorded gain under terrain-based normalization, persist m itself, and do not normalize by observed dynamics. Naming its actual artifact is a runner-build obligation. [C, §2.8; D, lines 26, 40–42] |
| **6. λ* uncertainty** | Correct. It is the full min–max range over compatible draws, with their count, not the generic percentile range. The draft preserves the distinctions among point fit, draw fit and final evaluator label. [C, §5.5 steps 7 and 9; §5.7 row 4; D, lines 27, 117, 138] |
| **7. All levels and unavailable states** | Correct. The 25 registered levels remain; closure and T0-reference unavailability keep their named states; extinct skeleton runs remain observations. Missing or corrupt inputs remain apparatus failures. [C, §2.9; §4.2; §5.8; §7; D, lines 28, 119–134] |

No point changes θ, ε, the component resolution m, the solver cap or tolerance, the contour family, the scored estimator or the endpoint rules. The new under-resolved-edge m summaries and direct closure–lattice S are expressly fidelity outputs. Their existence does not give the direct comparison the evaluator's qualification, a calibrated agreement probability, or an oriented occupancy interpretation. [D, lines 10, 56, 73–90, 113; C, §1.2′; §1.4; §5.5; A, line 149]

The draft also leaves the existing adjacent records intact. It does not replace Interpretation 001's T0 readings, and its arm/object/level-specific closure-unavailability row does not promote Disclosure 001's three measured κ = 1 cases into an all-arm finding. The solver remains registered as written. [I001, Points 1–2 and line 42; D001, lines 14–25; D, lines 48, 123]

## 5. Q4 and Q5 — Extensions and authority

### 5.1 Disposition of the packet's five identified additions

| Packet §3 item | Disposition | Reason |
|---|---|---|
| **1. Closure-family fits and fitted-level differences** | **Mike's explicit confirmation remains required before these become binding.** Keep the proposal marked, or remove it if he declines. | The consultation repeatedly calls these optional. The recorded “include” concerns direct edge comparison; it does not independently settle the fitted-level addition. [P, line 25; D, line 77; A, lines 129–135, 288, 303, 314] |
| **2. Skeleton Points 6 and 7** | **Acceptable in the record as the adopted package's coverage.** | The advice assigns item (iii) to the nonflat skeleton-high arms and adopts direct F. Applying it to the matched zero-floor, start-1 closure and unconditional seed mean is a consistent specification. This does not add skeleton item (ii). [A, lines 173–178, 315–317; D, line 101] |
| **3. Regional count ranges** | **Acceptable; clarify zero counts and their static dependency as in §3.1.** | They are numeric scalars of the reselected region. Their variability belongs to the selected seed bootstrap. The choice need not be struck or escalated into a separate scientific approval. [A, lines 112, 186–200; D, lines 65–66, 109] |
| **4. Draws for T0 whole-lattice Point 5** | **Already follows the adopted coverage and uncertainty recipe.** | T0 occupancy varies across seed maps even though no edge comparison or index fit is allowed. The advice explicitly retains whole-map T0 comparisons and requires their uncertainty when the evaluator skips resampling. D1 repairs the broader trigger; it does not remove this obligation. [A, lines 175–190; D, lines 102, 107] |
| **5. Matters left to build declarations** | **Acceptable within the bounds in §6 below.** | They closely follow the consultation's distinction between statistical readings and numerical/serialization/source conventions. A build declaration implements the ruled statistic; it cannot choose a different availability domain or uncertainty target. [A, lines 299–308; D, line 143] |

### 5.2 The authority statement is appropriately conditional

As recorded in this packet, Mike adopted the advised package, included the direct edge comparison and requested L2 review. The draft accurately distinguishes that decision from acceptance of this particular text, and it separately identifies the optional fitted-level addition. L2's review is not Mike's ruling and cannot supply his missing selection. [P, lines 18–29; D, lines 3–8]

**Point 6 is the only additional substantive inclusion choice identified by this review.** There are also the already stated acceptance of the corrected record and the later build's ordinary review/ratification steps. D1's repair, making counts explicit, and bounding numerical conventions do not require inventing further standalone approvals for parts of the package already adopted.

If Mike declines the optional fits, the deletion recipe needs one small completion: remove the confirmation paragraph in Point 6, the fitted-level paragraph in Point 7 **and the fitted-difference sentence in Point 8**. Keep item (iv)'s existing lattice λ* report and its own uncertainty recipe. Otherwise the record retains an uncertainty instruction for a quantity it has just removed. [D, lines 77, 92, 117, 138]

## 6. Q6 — Consequences and the unplaced skeleton-stream dependency

### 6.1 The stated dependency exists, but its eventual identity must be bound

The supplied second reports module declares the skeleton key as

`(master, terrain code, composition code, κ in micro-units, skeleton object code)`

with skeleton object code 1. Its `skeleton_level_key` constructs that five-element key; `skeleton_boundary` delegates to the placed evaluator using it. The module explicitly identifies this stream choice as reading 3, among L1's readings awaiting ratification. The draft is therefore accurate in calling it an in-review, unplaced dependency. [ER, lines 29–38, 79–89, 110, 249–264; D, lines 107, 144]

Tighten “If that declaration changes, Point 8 follows it” to mean the **declaration ultimately reviewed, accepted and identified before this report's output**. It must not authorize a silent migration to a later stream after results exist. Suggested wording:

> The skeleton draw matrix uses the stream declaration accepted for the second reports module. The third module's build record binds that declaration and its source identity before output. A subsequent change does not silently change this report's stream.

This is an ordinary prospective dependency, not a demand to approve the current unplaced copy merely to review Interpretation 002. The contract freezes streams and draw counts and forbids reruns to move a label; the draft itself also prohibits changing readings after output. [C, §5.5 step 9; D, line 147]

The key constructors contain no T0-specific exclusion: the realization constructor validates a realization/stationary-floor identity, and the skeleton constructor validates a skeleton/all-active identity. The generator itself needs only a valid key to make multiplicities. Thus T0's whole-map fidelity bootstrap does not require creating a contour fit or changing the evaluator's T0 behavior. The imported `streams.check_run_identity` implementation is absent from this packet, so this is a source-structure conclusion, not an executed integration test of that omitted dependency. [EV, lines 376–388, 485–490; ER, lines 249–264; C, §8, line 418]

### 6.2 The cost statement is sound for the additional calculations

No additional family search on every draw is needed for the newly selected reductions:

- Local-m summaries reselect endpoint cells over a fixed m field.
- Occupancy losses reform the mean and, where needed, the regional partition against a fixed closure map.
- Direct S compares two traced edges; the closure geometry is fixed and no registered-family minimization is involved.
- A retained closure fit is performed once per arm/object/level/index.
- The fitted-level difference translates the **existing** compatible-draw labels or range.

The already required evaluator still has its own per-draw fit work wherever its step-9 rule applies. The draft's cost sentence must be understood as avoiding additional searches for these summaries, not as eliminating those existing searches or supplying new λ* draws where the evaluator has none. [D, lines 117, 138, 145; A, lines 268–293; EV, lines 253–263, 439–462]

For direct S, the no-early-exit instruction is important and correct: the optional bound in `joint_discrepancy` can return without the full value. The new report needs its complete S and terms. Nothing in this record demonstrates a timing or affordability result for a future build. [D, line 87; EV, lines 253–263]

### 6.3 Bound the remaining build declarations and preserve all record obligations

Arithmetic accumulation order, the new spatial-summary and percentile interpolation conventions, maximum-location ties, encoding, exact stream/source bindings and caching belong in the build declarations. However:

- The linear interpolation already fixed for the (Q_{0.95}) terms **inside S** remains fixed; a general reference to percentile interpolation cannot reopen it. [C, §5.5 step 6; D, line 143]
- “Exact cause strings” means encoding the ruled dependency taxonomy and adding detail where unspecified. It does not permit replacing the contract's fixed unavailable causes or recasting an apparatus fault. [C, §7; D, lines 28, 119–134, 143]
- The shortened identity list in Consequences is not an exhaustive replacement for §5.9. Say that all applicable §5.9 bindings remain, including the summary schema, qualification protocol identity and qualification result identity when it exists at that stage. Do not demand identities before they exist. [C, §5.9; A, line 264; D, line 146]

“Nothing placed changes” is sound as the scope of this interpretation: the intended work is a new reports module through its own review. It neither clears the reference-only M6B source nor undoes or re-reviews the separately handled evaluator-precedence repair. The eventual build must bind the accepted dependency identities, rather than treating the reference files in this packet as an authorization to use obsolete or unaccepted bytes. [P, lines 3–4, 38; D, lines 142–146]

## 7. Q7 — Remaining cleanup and closure of this round

The required change is D1. The smaller completions identified above should accompany it: explicit regional zero-count behavior, own-map fit gates and the signed optional difference, point-versus-draw availability wording, and a bounded dependency/source declaration. They do not amount to new endpoint rules or separate fundamental objections to the selected summaries.

Three additional editorial corrections are straightforward:

1. **Quote accurately or label a paraphrase.** The quotation of §5.7 row 4 at D line 18 shortens and rephrases its ending without marking that fact. Use the exact text or identify it as a summary. Its scientific meaning is otherwise retained in Point 8. [C, line 266]
2. **Keep the adverse-fit limitation explicit.** Replace “a least-S contour outside ε” with “the least S among the contours examined, which need not be the family minimum.” It is not λ*. [D, line 138; C, line 217; EV, lines 351–353]
3. **Make recomputation coverage-dependent.** Point 8's list of re-formed geometry should say “where required by the selected summary.” T0's row remains whole-map only, and edge-cell m summaries remain realization-only. Restore “zeros after extinction” to the unconditional skeleton description. [D, lines 24, 101–107]

The contract and the substantive consultation package need not be rewritten. A revised draft should remove the observed-value gate, make these narrow definitions explicit, and carry Mike's optional-fit decision when he gives it. L1 should then build only the accepted record.

### Verification performed for this review

- Archive SHA-256, exact payload membership and all 14 payload digests independently computed and matched.
- Received advice matched byte for byte to the earlier response available locally.
- Draft compared with the frozen rules and relevant existing interpretation/disclosure; relevant evaluator, closure, spectral, outcome and stream-declaration source inspected.
- D1's integer-map witness executed and its region, bond and endpoint counts verified.
- All 14 extracted payloads and MANIFEST.txt rehashed after inspection; no source byte changed.

No full instrument test suite was needed to decide this prose-level ambiguity. These checks do not certify a future implementation, execute a scientific stage, or clear a source dependency that is explicitly outside this review.

## Appendix A. Verified identities and source keys

Source citations use the keys below, followed by sections or one-based lines in the exact supplied files. Every computed payload SHA-256 below equals its MANIFEST.txt entry.

| Receipt item | Expected | Independently computed / observed | Result |
|---|---|---|---|
| Archive SHA-256 | `b489e5d703d592343f319ff164b19ddd27d3e37a4a27168026ffa7033490224b` | `b489e5d703d592343f319ff164b19ddd27d3e37a4a27168026ffa7033490224b` | MATCH |
| Manifest-listed payload files | 14 | 14 | MATCH |
| Regular archive files including MANIFEST.txt | 15 | 15 | MATCH |
| Payload membership | Exactly the manifest entries | No missing, extra or duplicate payload entries | MATCH |

| Key | Payload path | Computed SHA-256 | Manifest comparison |
|---|---|---|---|
| P | `L1_TO_L2_F9_INTERPRETATION_002_REVIEW_PACKET_2026-11-23.md` | `2a27b5dcfc6e373ed760ba7fe88bb513f7d52bfea7316e8e90076726efd1cd24` | MATCH |
| D | `flights/mfa_fidelity/rulings_draft/F9_INTERPRETATION_002_FIDELITY_SUMMARIES_DRAFT_1.md` | `b2efdeda1d063ccb6d46d66e0c8d0881d5131015221d1e4f20fb6bed943d1a07` | MATCH |
| Q | `consultation/L1_TO_L2_F9_FIDELITY_SUMMARIES_CONSULTATION_2026-11-23.md` | `5811f97b2f2c9022db034cd3bcf359c62f2a932055550ee2bd30778d904b7f18` | MATCH |
| A | `consultation/L2_F9_FIDELITY_SUMMARIES_CONSULTATION_RESPONSE_2026-11-23_RECEIVED.md` | `c9df277a8d38449b2c37417e167a1aa6971f2fd8081a4283cac0f9cdf8b0156b` | MATCH |
| C | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| FR | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| CL | `flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py` | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` | MATCH |
| EV | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | MATCH |
| GEO | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| O | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` | MATCH |
| SP | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| D001 | `flights/mfa_fidelity/rulings/F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` | `bc5fac1d53fd57ac0923fb759e465e8783389d92cb1188e297c185c5b91ac78d` | MATCH |
| I001 | `flights/mfa_fidelity/rulings/F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` | `b38a4ff6eaa3e2118a9ae723cff63a3336fb178a35932071c3dc43c4478c50a6` | MATCH |
| ER | `packet_only/m6b_in_review/evaluator_reports.py` | `7978581182a64f77682facdc573c55ea2356077d6d6bddb935cbac5d13d1e393` | MATCH |

MANIFEST.txt itself is not one of its 14 payload entries. Its independently computed SHA-256 is `cbd6f00434e02a8f682e9060d8c89b00083ea28118fdfc09d5c96ec3b12f80d1`; there is no self-digest entry to compare.

## Appendix B. Executed synthetic witness

The following is the complete executed witness. Save it as a Python file and run it with NumPy available; it writes its result beside itself as `draw_gate_witness.json`. It constructs only integer test maps, uses one explicit replacement multiplicity vector, and invokes no project module, random generator, closure solver or scientific job. Its source SHA-256 is `87bdcb0239f4cec07e494775b0b34a37b3a2b9d6223875a96dc161ff551331af`.

```python
"""Synthetic domain witness for I002 draft1 Point8; no scientific data or job."""
import hashlib
import json
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
counts = np.zeros((40, 100, 100), dtype=np.int64)
counts[:19, 30:50, 30:50] = 400
observed_weights = np.ones(40, dtype=np.int64)
draw_weights = observed_weights.copy()
draw_weights[0] = 2  # one active-map occurrence repeated
# 19 active maps now have 20 occurrences; 21 zero maps have 20 occurrences.
draw_weights[19] = 0
assert int(draw_weights.sum()) == 40
assert np.all(draw_weights >= 0)
THRESHOLD_NUMERATOR = 40 * 1000 * 9 // 5  # theta=1/5, on integer box sums

def inspect(weights):
    weighted_counts = np.tensordot(weights, counts, axes=(0, 0))
    box_sum = sum(np.roll(np.roll(weighted_counts, dy, axis=0), dx, axis=1)
                  for dy in (-1, 0, 1) for dx in (-1, 0, 1))
    region = box_sum >= THRESHOLD_NUMERATOR
    neighbors = [np.roll(region, k, axis=ax) for ax in (0,1) for k in (-1,1)]
    inside = region & np.logical_or.reduce([~m for m in neighbors])
    outside = ~region & np.logical_or.reduce(neighbors)
    bonds = sum(int(np.count_nonzero(region != np.roll(region, 1, axis=ax)))
                for ax in (0,1))
    return {
        'active_map_occurrences': int(weights[:19].sum()),
        'zero_map_occurrences': int(weights[19:].sum()),
        'maximum_unsmoothed_mean': int(weighted_counts.max()) / 40000,
        'maximum_box_numerator': int(box_sum.max()),
        'threshold_numerator': THRESHOLD_NUMERATOR,
        'region_cells': int(region.sum()),
        'complement_cells': int((~region).sum()),
        'boundary_bonds': bonds,
        'distinct_inside_edge_cells': int(inside.sum()),
        'distinct_outside_edge_cells': int(outside.sum()),
        'step4_informative': bool(region.sum() >= 100 and (~region).sum() >= 100 and bonds >= 40),
    }

point = inspect(observed_weights)
draw = inspect(draw_weights)
assert point['maximum_box_numerator'] == 68400
assert point['region_cells'] == point['boundary_bonds'] == 0
assert draw['maximum_box_numerator'] == 72000
assert (draw['region_cells'],draw['boundary_bonds']) == (324,72)
assert (draw['distinct_inside_edge_cells'],draw['distinct_outside_edge_cells']) == (68,72)
assert draw['step4_informative']
result = {
    'purpose': 'Positive-support synthetic witness that a draw can define edge-cell statistics while the observed map cannot.',
    'data_origin': 'Constructed integer arrays only; no scientific job, probe array, master draw, or source modification.',
    'maps': '40 maps on 100x100; first19 have400/1000 occupancy on a20x20 patch; other21 are zero.',
    'point': point,
    'valid_draw': draw,
    'draw_weights': draw_weights.tolist(),
    'closure_dependency_for_case': 'Nonconverged/unavailable by hypothesis; no closure solver run.',
    'case': 'Point2/3 edge-cell summaries absent at point; Point5/6/7 closure-dependent summaries absent by hypothesis. Yet Point2 and the minus1 contrast in Point3 are numerically defined on the valid draw. A draw trigger requiring any observed summary can omit conditional ranges.',
    'limits': 'One possible replacement draw, not a claim about which draws a canonical stream produces; no proposed extension of scored step9 applicability.',
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(OUT/'draw_gate_witness.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
```

The assertions passed. The observed mask is empty; the constructed draw has 324 region cells, 72 bonds, 68 distinct inside endpoint cells and 72 distinct outside endpoint cells. Closure nonconvergence is a hypothesized allowed dependency state, not an output of this program. The program demonstrates the availability distinction that Point 8 must settle; it neither estimates its frequency in a declared stream nor changes scored step-9 applicability.

FINAL VERDICT: NOT SOUND