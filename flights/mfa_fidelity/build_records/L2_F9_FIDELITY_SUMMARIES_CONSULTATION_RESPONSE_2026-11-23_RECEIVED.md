# L2 → L1 and Mike — Flight 9 fidelity-summary consultation

**Date:** 2026-11-23  
**Register:** Advice on readings of frozen Contract F9 v0.7, §1.2′(ii)–(iii), with the related uncertainty and assembly questions.  
**Decision authority:** Mike. The recommendations below are proposed readings for his ruling, not adopted requirements.

**Archive reviewed:** f9_fidelity_summaries_consultation_L2.zip  
**Archive SHA-256:** a2abb7191c09c820b7f6dac3e4c26d3b17a3b008555be20180bad82c483b61c0

## 1. Verified receipt and evidence boundary

I computed the archive digest and each payload digest directly from the supplied archive bytes.

| Receipt item | Expected | Computed / observed | Result |
|---|---|---|---|
| Archive SHA-256 | a2abb7191c09c820b7f6dac3e4c26d3b17a3b008555be20180bad82c483b61c0 | a2abb7191c09c820b7f6dac3e4c26d3b17a3b008555be20180bad82c483b61c0 | MATCH |
| Manifest-listed payload files | 5 | 5 | MATCH |
| Regular files including MANIFEST.txt | 6 | 6; directory entries excluded | MATCH |
| Payload membership | Exactly the five manifest entries | No missing or additional payload files | MATCH |

The digest column below is independently computed; each equals its full digest in MANIFEST.txt.

| Source key | Payload path | Computed SHA-256 | Against manifest |
|---|---|---|---|
| Q | consultation/L1_TO_L2_F9_FIDELITY_SUMMARIES_CONSULTATION_2026-11-23.md | 5811f97b2f2c9022db034cd3bcf359c62f2a932055550ee2bd30778d904b7f18 | MATCH |
| C | flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md | 60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168 | MATCH |
| CL | flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py | 7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9 | MATCH |
| EV | flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py | 73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc | MATCH |
| SP | flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py | b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3 | MATCH |

References below use these source keys and contract sections or function names. I read the consultation first after verification, then inspected the contract and supplied reference code. This is a source-based consultation: I did not implement the proposed summaries, run Flight 9 jobs, inspect probe arrays, or verify the larger build and its absent dependencies. In particular, the skeleton stream attributed in Q to M6 part 2 is outside this packet.

## 2. Recommendation

**Adopt the substance of A–F, with the qualifications below, and replace G–H's blanket treatment with explicit rules for each statistic. Record the substantive choices in a short interpretation beside the frozen contract before implementation.**

The contract already determines the quantities, comparators, operational geometry and uncertainty obligations. It does not uniquely determine every reduction of those quantities to report columns. Calling the tier pre-registered “in full” does not make an unspecified cell weighting, loss function or conditioning rule uniquely recoverable from the text. Those choices should be visible in Mike's ruling. [C §1.2′; §5.7]

My recommended primary report uses distinct inside and outside edge-cell sets, L1's five-number m summaries and median differences, unsmoothed occupancy residuals, and direct lattice–closure edge discrepancy at θ = 0.20. I favor retaining the direct edge comparison because it measures a different aspect of fidelity from occupancy error. **An occupancy-only closure comparison is also a supported reading** of “where edges are compared”; Mike should see and choose between them before output exists. [C §1.2′(iii)]

Four constraints are already fixed, rather than choices for the builder:

- T0's spatial edge is excluded from comparison.
- Local m values themselves must satisfy the contract's persistence requirement.
- The λ* uncertainty output is the full range over compatible draws, with their count, rather than the generic percentile range.
- All registered levels and their unavailable states remain in the record. [C §4.3; §2.8; §5.7 row 4; §2.9; §7]

## 3. Answers A–H

### A. Which cells are “on the observed edge”?

**What is fixed.** The region comes from the realization's 3×3 periodic mean of the seed-mean occupancy, thresholded with included ties. E consists of the periodic four-neighbour boundary bonds of that post-estimator region. The inside and outside labels must refer to this region. Neither raw occupancy nor an index contour may redefine it. [C §1.2″; §5.5 steps 1–3]

**What remains open.** A bond does not select a unique cell. The contract does not specify whether the cell-based m distribution uses inside endpoints, outside endpoints, both, or repeated endpoint occurrences.

**Advice on L1's proposal.** Accept the two distinct endpoint sets, reported separately, with **equal weight per distinct cell within each set**. Include cells incident to every edge component, including components below m = 40 bonds; the resolution cutoff does not erase those components. This gives both sides without selecting one side's local values as privileged. It does not make the index boundary an oriented occupancy prediction. [C §5.5 steps 3 and 6; §1.4]

**Material alternative.** Give every bond equal weight and record its inside and outside endpoint values, retaining repeated cells. A cell incident to three bonds then appears three times. That can change medians and quartiles on corners or irregular boundaries. The contract's equal-bond rule governs the edge geometry; it does not expressly settle this new cell-distribution measure. Both constructions are supportable, but they are different statistics. I recommend L1's distinct-cell choice and an explicit ruling.

The availability of m summaries on a nonempty but under-resolved boundary is a separate issue, addressed in G.

### B. What should be reported of m?

**What is fixed.** Use the arm's raw local index and spectral normalization:

\[
m_i=\frac{g\lambda_i\Delta t}{q}
    =\frac{\kappa\lambda_i}{\operatorname{spr}(B_X)},
\qquad B_X=\operatorname{diag}(\lambda^X)A/8.
\]

The comparison array rounded for contour construction is not the raw λ for this calculation. Observed onset, occupancy and fitted edges must not renormalize m. [C §2.8; §3.4; SP: gain, local_m]

**What remains open.** The choice of descriptive summaries over an endpoint set.

**Advice on L1's proposal.** Accept the count, minimum, Q25, median, Q75 and maximum, with the interpolation convention declared. These are **spatial summaries across selected cells**. Their later bootstrap ranges describe variation of each summary across seed resamples; the two kinds of quantile must be labelled separately.

Omitting a per-cell list from the human-readable report is reasonable **provided an identified artifact already persists the per-cell m values**. Section 2.8 explicitly requires local m to be persisted. Persisting λ and coefficients that permit reconstruction is not, by itself, the same requirement. This packet does not establish which existing bundle or run artifact discharges it.

The two formulas above are algebraically identical. That does not guarantee identical final floating-point bits under different evaluation orders. Later implementation should reuse the persisted m array or the placed SP.local_m convention, which evaluates the contract's written expression from the recorded gain. This is a consistency declaration, not a request to change the definition.

**Material alternatives.** A mean and standard deviation, an empirical distribution, or the full cell list could replace or supplement the five-number summary. None is uniquely required by §1.2′. L1's compact distributional summary is a sound choice.

### C. What does “against 1” and “against κ̂_c,T0” mean numerically?

**What is fixed.** These are the stated dimensionless benchmarks. T0 supplies its own measured skeleton-high κ-axis threshold on the registered grid, not a historical Flight 8 value or T0's raw gain. Neither benchmark is a pointwise prediction. [C §1.2′(ii); §4.2–§4.3; §5.8]

**What remains open.** The contrast used to express the comparison.

**Advice on L1's proposal.** Accept, for each side, median(m) − 1 and median(m) − κ̂_c,T0, converting κ micro-units to κ before subtraction. Keep the unshifted spatial summary alongside them.

The uncertainty wording needs one addition: **the occupancy bootstrap holds the recorded T0 threshold fixed**. Its percentile range is conditional on that reference value. For example, subtracting the same reference from every bootstrap median simply shifts the median's bootstrap endpoints by that constant. It does not incorporate uncertainty in the reference threshold.

Retain T0's profile, grid bracket, lower-unbracketed status and unavailable cause beside the reference. Its uncertainty recipe remains §5.4, as directed by §5.7. Those bounds are panel/grid descriptions, not population confidence bounds. A descriptive suffix from a non-monotone profile must not silently become a threshold; the supplied CL explicitly distinguishes them. [C §5.4; §5.7 row 4; CL module documentation and threshold_fidelity]

**Material alternatives.** Ratios, fractions of edge cells above each benchmark, or contrasts at every spatial quantile would give different reports. The text does not choose among them. Median differences are adequate when the distribution in B is also visible. A comparison against each existing T0 bracket endpoint could be added as a separately labelled reference-sensitivity display; it is not a new confidence interval or a mandatory joint bootstrap.

### D. What should summarize occupancy against the closure?

**What is fixed.** Compare the seed-mean finite-tail occupancy with the closure for the same arm, level, object and floor. The closure uses its registered initialization and convergence rule. Their difference includes finite-time effects and must not be described as isolated stationary closure error. [C §1.2′(iii); §2.6; §4.2]

**What remains open.** The error summaries, spatial aggregation sets and diagnostic location convention.

**Advice on L1's proposal.** Accept the unsmoothed residual e_i = p̄_i − p*_i and, on each declared nonempty set U:

\[
\operatorname{bias}_U=\frac{1}{|U|}\sum_{i\in U}e_i,\qquad
\operatorname{RMSE}_U=\sqrt{\frac{1}{|U|}\sum_{i\in U}e_i^2},\qquad
M_U=\max_{i\in U}|e_i|.
\]

These distinguish signed average difference, distributed error magnitude and the largest local discrepancy. The whole-map values should be primary. Region and complement values are useful supplementary views, with both set sizes retained.

Two details need explicit decisions:

1. **Reselect the region on each resample.** For the recommended reading, form R_b from that resample's smoothed mean and compute its regional residual summaries on R_b and its complement. This bootstraps the entire reported selection procedure. Holding the original observed region fixed is an equally plausible reading of “the observed region,” but estimates error conditional on the original partition. It can give materially different ranges. I recommend reselection.
2. **Use subset nonemptiness, not edge informativeness, for these probability summaries.** A subset with fewer than 100 cells can still have a mean, RMSE and maximum. If one subset is empty, that subset is unavailable while the other and the whole map can remain available. [C §5.5 steps 1–4; §5.7]

Report the point maximum's cell under a declared tie rule, such as the lowest C-order flat index, with the coordinate convention. Bootstrap the **maximum magnitude**, not the coordinates or flattened identifier of whichever cell happens to maximize it. An uncertainty display for the maximum's location would be a different statistic.

**Material alternatives.** Mean absolute error, smoothed residuals, fixed observed subsets, closure-selected subsets or design-defined subsets are supportable descriptive choices. They answer different questions. Smoothed-only residuals can conceal discrepancies present in the probabilities themselves; I favor L1's unsmoothed comparison, with smoothing used to define R.

### E. How should §5.5 apply to the closure map?

**What is fixed.** If edges are compared, the same operational estimator and geometric conventions apply to both maps: 3×3 periodic averaging, θ = 0.20 with included ties, boundary tracing, components and the declared resolution. [C §1.2′(iii); §5.5 steps 1–4 and 6–8]

**Advice on L1's proposal.** The proposed deterministic treatment is sound. Apply the smoothing and threshold directly to the recorded converged float map. Declare the accumulation and comparison convention. Do not convert the closure to artificial integer tail counts or manufacture a seed panel by copying it forty times.

Step 9 supplies sampling uncertainty from the lattice seeds; the deterministic closure has no analogous seed uncertainty. If a closure-to-family fit is included, use the registered family, the existing minimization/tie convention, and λ* only when that fit is within ε. A poor fit retains its descriptive diagnostic without being promoted to λ*. [C §5.5 steps 5–9; EV: fit, evaluate_map]

**Separate the geometry from the optional fit.** Extracting the closure edge and comparing it directly with the lattice edge does not require minimizing over an index family. A closure-to-family fit is needed only for the proposed side-by-side fitted-level diagnostic.

The count of cells with |p̃* − θ| ≤ 10⁻⁹ is a reasonable non-gating diagnostic if that convention is fixed now. It is **not a certified bound on numerical edge error**. CL stops on the maximum change of one iteration, not a bound on distance to the limiting fixed point, and explicitly discloses possible machine differences. A zero near-threshold count therefore does not certify numerical robustness. Preserve the closure map identity, iteration count and last change. [C §4.2; CL module documentation, iterate, site_closure]

**Material alternatives.** Use the closure only for D; or compare its operational edge directly without fitting that edge to λ families. Both avoid work that is not necessary for occupancy comparison. Changing the threshold, adding a tolerance to the threshold decision, or changing the smoothing would alter fixed conventions rather than merely select a report.

### F. What should “edges compared” yield?

**What is open.** Section 1.2′(iii) makes the common edge rule binding **where** an edge comparison is made. It does not expressly require an additional closure–lattice edge loss, nor name that loss.

**Advice on L1's proposal.** Adopt direct

\[
S(E_{\mathrm{lattice}},E_{\mathrm{closure}})
\]

using the two directed global terms and every resolved-component term of §5.5 step 6. Retain all edge components in the global terms and the point record. This is a comparison of the two operational edges, not a comparison of their best-fitting index contours.

Report S in lattice-cell units and the descriptive indicator S ≤ 2.0 cells. It is a fidelity comparison; it does not acquire the scored evaluator's qualification or a calibrated agreement probability. Edges remain unoriented, so agreement of their locations does not establish agreement about the occupied side. D supplies the probability-level comparison. [C §1.2′; §1.4; §5.5 steps 3, 6 and 8]

For the primary direct comparison, I recommend requiring **both maps to pass the step-4 geometric minimums**. That is a sound reading of applying the rule to both maps. Do not additionally require a successful index fit or a favorable final evaluator label. An edge can be geometrically informative and disagree with every registered contour.

The three fitted-level fields have their own availability:

- The lattice λ* exists only when its own point fit is within ε.
- The closure λ* exists only when its own fit is within ε.
- Their difference exists only when both exist, and must subtract labels of the **same index** on the same arm, level and object.

On shared-family terrains, geometrically identical families still carry different composition labels; a P label must not be subtracted from an H label. An absent fitted level does not remove an available direct S. [C §3.4; §5.5 step 7; EV: IndexFamily.label, evaluate_map]

**The component uncertainty wording needs repair.** Point component lists are sound. A percentile range for “component 3” across resamples is not defined by those lists: lattice components can split, merge, vanish and be renumbered. The contract supplies no cross-draw component correspondence. For the primary uncertainty report, use S and its two global scalar terms; retain the complete point component terms as the decomposition of S. If Mike wants additional component summaries, define them explicitly—for example, the maximum resolved-component term per side with its own no-resolved-component state. Fixed closure components can retain identities across draws; changing lattice component ordinals cannot. [C §1.4; §5.5 steps 3 and 6]

**Material alternatives.** An occupancy-only closure report is text-supported and cheaper. If edges are included, a report of fitted levels alone would measure a different object from direct S. I favor direct S because it measures closure–lattice geometry even when neither edge fits a registered index contour.

### G. Coverage and the 1,000 resamples

**The broad proposal is reasonable, but “every arm,” “informative,” and “every summary” need the following explicit scope.**

#### Coverage

| Object / arm | Recommended coverage |
|---|---|
| Fourteen nonflat realization arms, every registered level | Item (ii); whole-map and regional D; direct F if adopted; existing item (iv) outputs |
| Fourteen nonflat skeleton-high arms, every registered level | Item (iii), using the unconditional 40-seed mean; the separately required skeleton-boundary report remains |
| T0·P realization and skeleton-high, every registered level | Whole-map occupancy–closure comparison and the applicable threshold/reference records; no spatial-edge comparisons or λ fits |
| θ = 0.10 and 0.30 | Preserve the mandatory full evaluator output; repeating all newly selected (ii)/(iii) summaries is an additional scope choice |

The primary “observed edge” in §1.2″ is the realization edge. Restricting mandatory item (ii) to that object is the better reading. Skeleton m summaries could be an explicitly labelled addition, not an implied requirement. Skeleton occupancy retains every seed's recorded tail, including zeros after extinction. T0's separate low-initialization sweep is a consistency exercise and should not silently enter the skeleton-high fidelity scope. [C §1.2″; §1.3(f)–(g); §2.6; §4.3; §5.7–§5.8]

**T0 is an express exception to L1's “every arm” wording:** its spatial occupancy edge is “never compared with anything.” I recommend whole-map D there, without turning an accidental threshold region into a boundary diagnostic. All 25 registered level rows remain, including unavailable rows. [C §3.3; §4.3; §2.9; §7]

The report's panel scope should also be explicit: the primary fidelity report uses the canonical records supplied by jobs 11–13. The separate stability panel has its own reporting obligation; repeating all new fidelity summaries on it is not automatically required by G's arm/level wording. [C §8, jobs 11–15]

#### What is resampled

Use 1,000 draws of **40 complete seed maps with replacement**, preserving each map's spatial structure. The resample determines a new p̄_b, smoothed map, region and edge wherever needed. The local m field, canonical terrain/spectral quantities and matching closure map stay fixed.

For B/C, uncertainty comes from changing the selected edge cells. Holding the original endpoint sets fixed would make these fixed-field summaries constant across draws and omit that source of variation. For D, use the reselected regions recommended above. Use the same declared draw matrix across summaries of the same arm, object and level, and reuse existing evaluator draws where applicable. Reuse within an object does not create pairing between independently streamed arms, objects or levels. [C §2.5; §5.5 steps 1–4 and 9; §5.7 row 4; EV: resample_multiplicities]

Whole-map D still requires its 1,000 draws when no informative point edge exists. EV.evaluate_level can return without resampling when point geometry fails or no family applies. That evaluator shortcut cannot eliminate uncertainty for a whole-map statistic that remains defined. The separately declared skeleton stream must be identified in the eventual build record; this packet cannot verify it. [EV: evaluate_level; Q §2(G)]

#### Defined values and conditional ranges

For each selected scalar, retain the observed value, the 1,000-draw attempt count, the number of defined values, the undefined causes, and the 2.5th/97.5th percentiles over defined values. State that these are **conditional empirical ranges where definition is conditional**. They are not automatically 95% confidence intervals or simultaneous bands.

For the new summaries, I recommend assessing definition on each draw independently of whether the point statistic exists. Thus an unavailable point value can coexist with a conditional range from draws on which that statistic is defined. Keep both facts; the range supplies no replacement point estimate and changes no scored record. This is a proposed fidelity-report reading, not an instruction to extend the scored evaluator's step-9 applicability.

No replacement draws, zero/infinite imputations, or selective removal of difficult levels. Zero defined values gives an unavailable range, not zero-width precision. A small defined count remains visible; introducing a minimum count that suppresses a range would be another rule requiring a decision. The scored 950-of-1,000 rule is not a new fidelity acceptance rule. [C §1.2′; §5.5 step 9; §5.7]

“Every summary” should mean the selected **numeric statistics**, not identifiers, cause strings, Boolean flags or component positions. B's spatial summaries, C's differences, D's bias/RMSE/maximum magnitude, and F's chosen scalar discrepancies can receive ranges. Point maximum locations and component lists need the distinct treatment above.

**Preserve the λ* exception:** use the full minimum–maximum range over draws with Δ ≤ ε and its count. If a fixed closure λ* exists, I recommend translating that range for the fitted-level difference. An additional percentile range for that derived difference would be supplementary and requires an explicit choice; it must not replace item (iv)'s prescribed range. [C §5.7 row 4; EV: evaluate_level]

#### An open restriction: m on under-resolved edges

L1 excludes B/C whenever the edge is not informative. Section 1.2′(ii) says m on the observed edge; it does not expressly limit that description to a level passing step 4. There are two defensible readings:

- Inherit step-4 minimums for all edge-derived summaries, as L1 proposes.
- Report B/C whenever the non-T0 boundary exists, carrying its under-resolved flag.

**I recommend the second.** A nonempty edge still identifies cells and their m values. Retaining those descriptive values does not authorize a scored claim at that resolution. Empty/full regions still have no edge-cell summary. This differs from my recommendation for F, which compares two edges under the expressly required common geometric rule. Mike should rule this distinction; it must not be chosen implicitly in a helper function.

Under either reading, distinguish point geometry from the final bootstrap label. A geometrically available point summary does not vanish because the final index result is adverse, unresolved or unstable. Publish the applicable instability and definition counts beside it. [C §5.5 steps 4, 7 and 9; §1.2′]

### H. Unavailable states

**What is fixed.** Closure nonconvergence is “comparator unavailable”; absent κ̂_c,T0 is “reference unavailable”; extinction is a valid observation; missing/corrupt input and runtime faults are apparatus failures. [C §4.2; §5.8; §7]

**Advice on L1's proposal.** Keep those states, but apply them to the fields that actually depend on them. The geometry rows below describe point-value availability; draw values follow G's separately stated rule:

| Condition | Appropriate consequence |
|---|---|
| Matching closure not converged | D and closure-dependent F fields unavailable; available B/C and lattice fitted-level information remain |
| T0 threshold unavailable | Only T0-referenced comparisons unavailable; m versus 1 and closure comparisons remain |
| Lattice region empty/full | No B/C or direct F; whole-map D and any nonempty D subset remain |
| Lattice boundary under-resolved | Flag the geometry; retain B/C under the recommended reading; regional D remains defined on nonempty subsets; direct F unavailable |
| Closure edge absent or under-resolved | Direct F unavailable with the closure-side cause; whole-map D remains available |
| Index fit unavailable or outside ε | That λ* and dependent fitted-level difference unavailable; independently defined direct S remains |
| Point geometry available, final evaluator unstable/unresolved/adverse | Preserve available descriptive point values, conditional ranges and existing scored status separately |
| Required numeric summary has no defined draws | No numeric percentile endpoints; retain count and causes, and the point value if available |
| T0 edge item | Not applicable under §4.3, rather than a failed attempted comparison |
| Missing/corrupt required input or computation fault | Preserve the apparatus/input failure; do not recast it as harmless scientific unavailability |

When both sides or multiple dependencies fail, retain the applicable causes rather than allowing one generic null to hide the others. An unavailable scientific comparator is different from an omitted required record: the latter prevents a claim of complete reporting. [C §5.7; §7]

**Alternatives and support.** There is no equally supported replacement for the contract's named unavailable states. Availability domains for the newly selected statistics remain open where identified in G. An all-or-nothing level gate, or a final-stability gate on all fidelity values, would produce a substantially smaller report; I do not recommend either, because it discards defined information for reasons unrelated to the particular statistic.

## 4. Further question 4 — Omissions, and whether (i) and (iv) are already supplied

### Item (i): threshold fidelity

**At the level of the supplied source, L1's assessment is substantially correct.** CL.threshold_fidelity supplies the own persistence record, normalized and raw-g shifts from the spectral crossing, the T0-referenced κ difference, gain values, and typed unavailability. It also retains the own and T0 persistence records. [CL: threshold_fidelity; C §1.2′(i)]

Assembly must preserve the profile, brackets and their absent-endpoint causes, rather than reduce the record to point shifts. Threshold uncertainty remains the §5.4 description; no occupancy-bootstrap threshold interval is required. The contract's explicit normalized/raw-g shift wording concerns the spectral comparison; it does not require inventing a new cross-arm raw-g threshold estimator. [C §4.1–§4.3; §5.4; §5.7 row 4]

This confirms the presence of the ingredients in the supplied function, not the completeness of an assembled build or correctness of dependencies absent from this packet.

### Item (iv): fitted levels

EV supplies point λ* when the point fit is within ε, per-draw compatible types and level indices, their count, and the full conditional min–max range. Reuse those quantities. [EV: evaluate_map, evaluate_level]

Assembly still must preserve several distinctions:

- A point map can lack λ* while some resampled maps have one; retain the compatible-draw range if it exists.
- An adverse, unresolved or unstable final label does not erase those compatible draws.
- A skipped bootstrap is “not resampled/not applicable,” different from 1,000 attempted draws with no compatible resample.
- A descriptive best examined contour outside ε is not λ*.
- Preserve the applicable index labels, family identities and existing own/rival evaluator outputs, including the required sensitivity and skeleton records. [C §5.5 steps 7 and 9; §5.7 row 4; §1.3(f)–(g); EV: fit, evaluate_level]

### What A–H did not yet specify fully

The outstanding matters are mainly **report definition and provenance**, not a missing fifth fidelity item: T0 exclusion; panel and θ coverage; persistence of local m; T0-reference conditioning; the selection rule for regional errors; scalar versus identifier/component uncertainty; and the different geometric, fitted and resampled availability states.

Each assembled record should bind the applicable map/closure identity, raw-index and normalization identities, object/floor, arm/level, seed and resample stream, summary schema, θ/ε/m, evaluator identity, and qualification identities appropriate to its stage. These are existing record obligations, not permission to demand identities that do not yet exist. [C §5.9]

## 5. Further question 5 — Cost and work the contract does not require

**The 1,000 seed resamples do not entail 1,000 new contour-family searches for every fidelity statistic.** L1's timing observations in Q are not measurements reproduced in this consultation, and they do not establish that the same cost attaches to the narrower computations below.

| Quantity | Necessary per-resample operation | Reusable or one-time work |
|---|---|---|
| Whole-map D | Reform p̄_b and summarize its residual against fixed p* | Closure map computed once |
| Regional D | Also form the selected R_b | No contour-family fit required |
| B | Form the threshold region and edge-cell sets; summarize fixed m | Per-level m array fixed |
| C | Translate B's median by the fixed benchmarks | No independent bootstrap needed |
| Direct F | Trace the lattice edge and compute S against the fixed closure edge | Closure geometry and its distance representation fixed; no family minimization |
| Lattice λ* | Use the already required evaluator's compatible-draw labels | EV returns types and level indices |
| Closure λ* | None after its deterministic fit | Fit once per selected arm/object/level/index |
| Fitted-level difference | Translate the lattice labels/range by the fixed closure label | No new fit |

EV.joint_discrepancy operates on two traced edges; it does not require the second to be a registered contour. When reporting direct S and its terms, obtain the complete discrepancy, not merely an early-exit decision at ε. The optional bound in that function can stop before returning those values. [EV: joint_discrepancy, fit]

Sharing resampled means and geometry, reusing the declared draw matrix, and caching fixed closure quantities are valid implementation choices if the selected statistics and their numerical conventions are preserved. The cost question should first be addressed by this reuse, not by altering the estimand.

There are also **prospective scope choices the text leaves open**:

- Omit the additional direct closure-edge comparison, taking item (iii) as occupancy comparison.
- Omit optional closure-to-family fits and fitted-level differences.
- Keep only whole-map occupancy errors rather than the supplementary regional tables.
- Do not extend the new (ii)/(iii) summaries to extra θ values or the stability panel unless Mike selects that coverage.
- Do not invent component-identity bootstraps or argmax-coordinate intervals.

These options are materially different reports and must be selected before results exist. My preference is to retain L1's regional error summaries and direct F, using the reduced computation above. Once a stochastic scalar is selected for the fidelity report, the 1,000-draw recipe applies; cost does not justify fewer draws, survivor-only skeleton means, frozen edge membership, replacement of undefined draws, or dropping inconvenient levels. The separately required full scored evaluator and sensitivity/skeleton outputs retain their own obligations. [C §1.2′; §1.3(f)–(g); §5.5; §5.7; §8]

## 6. Further question 6 — Interpretation record or build declarations?

**Yes: the substantive readings belong in a short interpretation record beside the frozen contract, ruled by Mike.** They determine the statistic, its domain and what its uncertainty means. A builder should not select among materially different reports under the label of implementation detail.

| Put before Mike as readings | Record in the ensuing build declarations |
|---|---|
| Distinct-cell versus bond-weighted endpoint measure; chosen spatial summaries and contrasts | Field names, ordering and serialization |
| Whole-map and regional residual summaries; reselected versus fixed subsets | Numeric accumulation and quantile interpolation conventions |
| Whether direct F and closure fits are included, and the scope of their component detail | Fixed geometry/fit reuse and caching |
| Availability on under-resolved edges; separation from final scored status | Exact cause encoding implementing the ruled dependencies |
| Object, panel and θ coverage, within the contract's T0 exception | Exact stream-key and source-identity bindings |
| Conditional defined-draw ranges; fixed T0 reference; treatment of fitted-level differences | Diagnostic maximum-location tie rule and threshold-nearness count convention |

Restate the **already fixed** restrictions in that record as constraints, not new discretion: the frozen geometry and thresholds, the 1,000 seed draws, the unconditional skeleton mean, T0's edge exclusion, local-m persistence and λ*'s prescribed conditional range. The interpretation must not change them. Any actual departure from a fixed estimator, resolution, resampling count or scored rule must be identified as a change and follow the contract's instrument/version requirements. [C §2.8–§2.10; §4.3; §5.5; §5.7; §7]

For a concrete ruling, I recommend Mike adopt the following package:

1. A–C as proposed, with distinct-cell weighting, persisted raw m values, and C's bootstrap explicitly conditional on the recorded T0 reference.
2. D on unsmoothed probabilities, whole-map primary plus nonempty regional subsets, rebuilding each selected region on every seed resample.
3. E's deterministic closure geometry and non-gating numerical diagnostic; any included closure fit is computed once and kept separate from direct edge comparison.
4. F's direct S at θ = 0.20 for both maps passing step 4; uncertainty for S and the two global terms, full point component decomposition, and no implicit cross-draw component matching.
5. B/C retained on every existing non-T0 boundary with resolution flags; F retains its two-map geometric minimums. Final scored outcomes do not erase defined fidelity values.
6. G–H replaced by the explicit coverage, uncertainty and dependency rules above, including T0's exception and λ*'s separate range recipe.

The supported smaller alternative is an occupancy-only closure report without F and its optional closure fits. Either package can be made concrete before code. Mike's recorded choice determines what L1 builds.
