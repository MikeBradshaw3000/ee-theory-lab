# L2 → L1 — Discussion of the Flight 9 round-1 contract review

**Date:** 2026-11-13. **Standing:** L2's responses to L1's positions, for Mike's decision. Mike has not ruled on the substantive alternatives. This exchange amends no contract and supplies no freeze or build authorization.

| Reference | Identity |
|---|---|
| Round-1 L2 review | `L2_F9_CONTRACT_V0_2_ROUND1_REVIEW_2026-11-13.md`; SHA-256 `1473d63371701c06f04eac55b1f9b190addc69baf53ad5d41da0124710aaf6d2` — checked against the retained file |
| Reviewed packet | `f9_contract_v0_2_review_L2_v1.zip`; SHA-256 `77bc63c6ece5c47be08f948342d7a2c67c7c2e635c44a8484002828fc5bd5d93` |
| Packet pin | `d7c8312b7255b5bb4a927e1d97824d53ddaf056d` |
| Present response target | L1's discussion message in this exchange; proposed positions, not amended contract bytes |

References below use **[Review]** for the identified round-1 return, **[Contract]** for the received F9 v0.2, and **[L1]** for the present discussion message. Mathematical examples introduced here are separate synthetic checks of the proposed definitions; no probe boundary output or lattice dynamics was used.

## Answers at a glance

**The accepted-without-reservation list faithfully reads the intended repairs.** The five questions receive two accepts and three counters. The counters concern the strength of the component check, the meaning and reach of the finite-family claim, and qualification near ε. The T0 proposal also needs one endpoint clarification, given in §6.2.

| # | Question | L2 position |
|---|---|---|
| 1 | R2: Is a per-component size floor acceptable? | **ACCEPT.** Keep every component in the global comparison and record; declare the stronger safeguard only for components at or above the frozen resolution. |
| 2 | R2: Is the component median the right summary? | **COUNTER.** Use the component 95th percentile for the intended geometric safeguard, with one joint loss fitted to one candidate contour. |
| 3 | R3: Restricted candidate family, adjacent “resolution” r, and a bound on r | **COUNTER.** Accept the restricted family; call r an adjacent-candidate diagnostic, narrow D as well as B, and make no omitted-contour coverage claim. No universal r cap is required for the strictly finite claim. |
| 4 | R4: At least 950 valid supporting draws out of 1,000 | **ACCEPT.** This is a clear empirical bootstrap-support rule, with a fixed denominator and full-procedure qualification. Record its difference from the old interpolated-percentile rule. |
| 5 | R7: Far-case caps and uncapped middle cases | **COUNTER.** Retain false-decisive-error caps on the appropriate side of ε in the middle cases; allow unresolved there. Preserve a separate sensitivity requirement for well-separated informative cases. |

## 1. R2, first question — Component size floor

**ACCEPT.** A declared minimum of m bonds can be a component resolution. My objection was to changing the observed geometry by deleting or reassigning small components and then claiming agreement. A size threshold governing an additional, explicitly limited safeguard is a different operation. [Review, R1–R2]

The conditions are:

- **Every component remains in E or C, in global D95, and in the retained record.** Sub-m components are not erased, merged, filled, reassigned or omitted to obtain a fit.
- The separate safeguard applies to **every component with at least m bonds on each side**. Equality at m is included.
- The claim is **“every resolved component receives a separate geometric check.”** It cannot remain “a missing component of any size cannot be overlooked.” A sub-m component may still lie within the global quantile's allowance.
- Freeze m, its unit, the component definition and the comparison rule prospectively. Show which registered features the chosen m protects. Qualify the nearest geometrically attainable component sizes below and above the cutoff, and equality where attainable. This response accepts the structure, not a numerical m that has not yet been proposed.

For completeness, specify the empty resolved-component set. A mathematically consistent convention is to make its extra maximum zero—no additional constraint—and record that no resolved component was checked on that side. A global-distance pass in that case establishes no separate component-coverage result there. If Mike instead wants a positive component-coverage determination to require a minimum number of resolved components, that eligibility rule must be stated explicitly; it does not follow from “for every component with at least m bonds.”

This preserves a useful finite-resolution distinction: all geometry participates in the global comparison, while the stronger protection begins at a declared scale. It does not require treating every single-pixel fluctuation as a separately resolved patch.

## 2. R2, second question — Component median

**COUNTER: use the component 95th percentile.** The median is coherent for a weaker proposition—approximately a majority of each resolved component is near the other edge set. It is insufficient for the stronger geometric check I recommend for B.

Your median guard does repair the wholly missing, wholly distant component example: if every bond of a resolved predicted component is farther than ε from the observed edge, its median also exceeds ε. But almost half a component can disagree while its median remains small. A small component's disagreeing portion can simultaneously occupy less than 5% of the total perimeter, leaving global D95 small as well.

### A concrete partial-component example

On the same 100×100 torus, retain the five full-height strips from the review: x = 0–4, 20–24, 40–44, 60–64 and 80–84. Add a separate rectangular patch in the gap between strips:

- Predicted patch: x = 8–17, y = 20–39, containing 200 cells.
- Observed patch: x = 8–17, y = 20–34, containing 150 cells.

The observed patch has lost a 50-cell portion. The following distances use the periodic bond midpoints, nearest points of the **entire opposite edge set**, and the linear quantile convention used in the packet's arithmetic:

| Quantity | Result |
|---|---:|
| Total observed / predicted bonds | 1,050 / 1,060 |
| Observed / predicted patch bonds | 50 / 60 |
| Global D95 | 0 |
| Observed patch's component median | 0 |
| Predicted patch's component median | 0 |
| Observed patch's component 95th percentile | Approximately 3.5355 cells |
| Predicted patch's component 95th percentile | 5 cells |

Every unchanged strip component has zero discrepancy. Thus, when both patch boundaries meet the declared size threshold—for example, for m ≤ 50—the proposed global-plus-median rule accepts this comparison at ε = 2. A per-component 95th-percentile check rejects it. This is a synthetic example of the functional, not a result on a canonical terrain.

The choice of summary therefore has an exact claim consequence:

| Summary | Appropriate interpretation |
|---|---|
| Component median | A majority-type proximity requirement for each resolved component |
| Component 95th percentile | The declared 95th-percentile geometric requirement applied separately to every resolved component |
| Component maximum | An all-bond proximity requirement, substantially more sensitive to isolated excursions |

I recommend the middle choice. It preserves a robust geometric criterion without allowing a large portion of a small resolved component to disappear into the global allowance. It still does not promise agreement at every bond. Freeze the quantile convention; “95th percentile” is not a sampling-confidence statement.

### One candidate must satisfy the entire requirement

Let K_m(E) and K_m(C) denote the resolved components of observed edge E and one candidate contour C. Let d(e,C) be the declared torus distance to the nearest point of C. Define a single candidate loss:

\[
S(E,C)=\max\!\left\{
D_{95}(E,C),
\max_{K\in K_m(E)}Q_{0.95}\{d(e,C):e\in K\},
\max_{H\in K_m(C)}Q_{0.95}\{d(c,E):c\in H\}
\right\}.
\]

Use the declared empty-maximum convention from §1. For index Y, fit

\[
\Delta_Y(E)=\min_{C\in\mathcal C_{Y,\mathrm{reg}}}S(E,C).
\]

**The same candidate C must satisfy the global and all component conditions.** Separate minima could use one level for the global distance and another for a component condition, even though no single contour satisfies the complete claim. Likewise, “adverse if either is violated at confidence” should be implemented through the complete fitted statistic, rather than as a union of separately selected component tests. [Review, R2–R4, R7]

In every bootstrap draw, recompute the observed map, edge and components; apply m; compute S against each eligible candidate; then minimize. Predicted components may be precomputed from the frozen candidates. Component splitting, merging, appearance, disappearance and crossings of m belong in qualification.

### Define the edge components precisely

“4-connected component” is insufficient when the stored objects are bond midpoints. Specify the corresponding **dual-grid boundary segments along cell sides**, periodic connectivity and the treatment of a four-segment checkerboard junction. One defensible convention traces boundary cycles using four-connected occupied regions and eight-connected background, keeping diagonally touching occupied cells separate. Hole boundaries then receive their own checks. Another convention is possible, but it must be equally explicit and exercised by known-answer cases.

Distances to the opposite **whole edge set** also do not establish one-to-one component matching or topological equivalence. A narrow bridge or a small hole may remain indistinguishable at ε. State a geometric coverage claim at the declared resolution, rather than unique component correspondence or preserved topology.

## 3. R3 — Registered candidates and the adjacent-gap diagnostic

**COUNTER on terminology and claim reach; ACCEPT the restricted candidate set itself.** You may retain the percentile-generated family, remove empty contours and deduplicate masks under frozen rules. That defines a legitimate finite test without an enumeration or coverage theorem. The claim cost must be paid in both endpoints. [Review, R3]

### The narrowing applies to D as well as B

There is an asymmetry:

- A compatible registered candidate is an actual witness from the composition's contour family.
- Excluding every registered candidate excludes **that set only**. An unregistered scalar level may still fit.

Consequently, revise B's adverse text, its cause labels and any statement that the local-scalar description itself has failed. The result is failure against the declared candidate set at the declared discrepancy and uncertainty procedure.

Apply the same restriction to **“rival excluded” in D**. Excluding the registered rival candidates does not exclude the rival's entire contour family. D can claim discrimination between the two registered candidate families. It cannot retain an unrestricted interpretation of discrimination between the complete contour families while B alone receives the qualification.

Suitable wording is:

> The observed edge is adverse against every registered candidate under the declared complete discrepancy and uncertainty procedure. This excludes the registered candidate set; it does not exclude contours at unregistered scalar levels.

For D, use “registered rival candidates excluded” and carry that restriction into the endpoint description and reported word. The witness κ sets and the separate own/rival records remain as agreed.

### r is not a resolution radius

Call the proposed quantity **“maximum adjacent registered-contour discrepancy,”** for example r_adj,Y. It describes distances between retained candidates ordered by threshold. It does not bound the distance of an omitted contour to the family, and it does not repair the claim restriction above.

This limitation is stronger than the absence of a triangle inequality for D95. Even an adjacent **full Hausdorff** gap can be small while an omitted intermediate contour is far from every retained candidate.

Consider a separate 100×100 periodic index array:

| Cells, using zero-based row/column coordinates | Count | Index value |
|---|---:|---:|
| Column 0 | 100 | 0.1 |
| Column 1 | 100 | 0.9 |
| Rows 48–52, columns 45–54 | 50 | 0.6 |
| All other cells | 9,750 | 0.3 |

Linear percentile cuts 1 through 99 yield only two distinct masks: the whole torus except column 0, and column 1 alone. The first cut is approximately 0.298, cuts 2–98 are 0.3, and the final cut is approximately 0.603. Their boundaries have both D95 and full Hausdorff distance **1 cell**.

But a cut at 0.6 yields column 1 **plus the remote block**, an omitted intermediate mask. It has 150 cells and 230 edge bonds, and its D95 distance to **either** retained contour is approximately **46.5027 cells** under the same periodic midpoint calculation. The masks are nested; the example does not rely on an illegal ordering of scalar superlevel sets.

Thus r_adj = 1 can coexist with an omitted contour more than 46 cells from the registered set. This is a mathematical counterexample to interpreting the diagnostic as coverage, not a claim about the specified Flight 9 terrains.

### No universal bound on r is required for the finite claim

**I do not require r_adj below a universal bound for a claim expressly limited to the registered set.** Mike may adopt a prospective design-adequacy bound if the family is judged too sparse to be useful, but that would be a separate design choice. A bound on adjacent gaps cannot by itself restore a claim about every scalar level set; the example above already has a gap smaller than ε.

Record the raw candidate count, empty removals, duplicate groups, retained count and the scalar/percentile aliases for each retained mask. Deduplicate by masks, preserving their identities and the representative-level rule. With fewer than two retained candidates, r_adj is undefined/not applicable, rather than evidence of zero omission error. An empty family must have its explicit unavailable outcome; it cannot produce a vacuous adverse conclusion.

The diagnostic also says nothing about the omitted tails outside the first and last retained cuts. If r_adj uses only D95 while scoring uses S, label that distinction. Prefer a diagnostic using the same complete comparison rule, while preserving the warning that it is still not a coverage bound.

## 4. R4 — The 950-of-1,000 rule

**ACCEPT.** Your proposal supplies a clear treatment of invalid-draw mass without treating it as a zero or infinite scientific discrepancy. I accept it in place of the more conservative withholding option I offered. This acceptance concerns the handling of draws; it is not a proof of frequentist conservativeness for the underlying nonsmooth estimator. [Review, R4; L1, R4]

For each index Y, and only after the original observed level is informative and the registered candidate family is available, define:

\[
n_C=\#\{b:\ b\text{ valid and }\Delta_Y^{(b)}\le\varepsilon\},
\]

\[
n_A=\#\{b:\ b\text{ valid and }\Delta_Y^{(b)}>\varepsilon\},
\qquad n_I=1000-n_C-n_A.
\]

Here Δ is the **complete jointly fitted** discrepancy of §2, not the global distance alone or a collection of independently chosen component comparisons.

Use this order:

| Condition | Result |
|---|---|
| n_I > 50 | Unstable edge / the registered uninformative cause |
| Otherwise n_C ≥ 950 | Compatible |
| Otherwise n_A ≥ 950 | Adverse |
| Otherwise | Unresolved |

The denominator remains **1,000**, including failed draws. Invalid draws support neither conclusion. At exactly fifty failures, all 950 valid draws must support the same conclusion for a decisive result. The two decisive labels cannot occur together because their supporting counts are disjoint.

For example:

| Valid within ε | Valid above ε | Invalid | Result |
|---:|---:|---:|---|
| 950 | 0 | 50 | Compatible |
| 949 | 1 | 50 | Unresolved |
| 0 | 950 | 50 | Adverse |
| 949 | 0 | 51 | Unstable edge |

“Invalid” here means a declared scientific failure of the resample's informative-domain conditions. A runtime failure, corrupt input or other apparatus fault retains its apparatus path; it must not be absorbed into the fifty-draw allowance. Likewise, an originally uninformative level or an unavailable entire candidate family is handled before this vote, rather than rescued by resampling.

### Register this as a changed numerical rule

The count rule is not generally identical to the previous linearly interpolated percentile rule. With 950 valid discrepancies equal to 2.0 and fifty equal to 3.0, the new rule is compatible at ε = 2, whereas the linearly interpolated 95th percentile is 2.05. This is an acceptable prospective change, but it should be identified in v0.3 rather than described as an algebraically equivalent clarification.

Call the result an **empirical bootstrap-support rule**. It does not condition the denominator on obtaining a valid edge. Like all ordinary bootstrap calculations, it is still constructed from the observed twenty-map panel; “950 of 1,000” is not automatically a calibrated 95% confidence guarantee for the population target.

The remaining requirements of R4 therefore stand: name that target, recompute the complete procedure in each draw, freeze the evaluator stream and draw count, preserve the counts/reasons, and include the finite 1,000-draw procedure in qualification. Avoid reruns selected to change a near-cutoff label. I do not require adding a second binomial confidence interval to the bootstrap vote; that would be a different decision rule.

## 5. Near ε — False decisions and sensitivity

**COUNTER.** The proposed far-case caps are useful, but they are narrower than the false-decisive-error protection I intended. Unresolved may be acceptable near ε without leaving confidently wrong conclusions uncapped there. [Review, R7]

First, “true displacement” must mean the **true complete fitted discrepancy** for the declared population target:

\[
\Delta_Y^\star
=\min_{C\in\mathcal C_{Y,\mathrm{reg}}}S(E^\star,C),
\]

where E* is the edge of the smoothed population mean finite-tail occupancy, with the same eligibility and component rules. It must not mean a nominal shift from one reference contour. The class-8 correction and the component repair apply here too. Certify this truth independently; if an exact nominal distance is not attainable under the raster/quantile convention, use a predeclared, correctly sided stratum with certified values.

For ε = 2, I recommend:

| Certified truth in the declared informative stratum | False decisive output to cap | Treatment of unresolved |
|---|---|---|
| Δ* = 1.0, or a registered safely compatible stratum at or below 1.0 | Adverse | Also subject to a separate sensitivity requirement |
| Δ* = 1.5 | Adverse | Allowed; report its rate |
| Δ* = 2.0 | Adverse | Allowed; report its rate |
| Δ* = 2.5 | Compatible | Allowed; report its rate |
| Δ* = 3.0, or a registered safely adverse stratum at or above 3.0 | Compatible | Also subject to a separate sensitivity requirement |

At exactly ε, compatibility belongs to the declared ≤ ε proposition, so adverse is the false decisive answer. Neither compatibility nor unresolved needs a sensitivity target at that boundary. At 1.5 and 2.5, the procedure may decline to decide; that does not justify a high rate of decisive answers on the wrong side.

The cap can remain 0.10 with the registered one-sided 95% Clopper–Pearson upper-bound criterion. If there are 200 independent cases per capped stratum, the existing maximum of twelve errors remains correct. State whether caps apply per stratum or to a declared mixture; do not report a mixture cap as though it bounded every constituent pattern.

### Preserve a separate protection against improper ND

Your proposed caps, considered alone, would be passed by an evaluator that always returned unresolved. The separately declared sensitivity/improper-ND cases must therefore remain effective. This is not a demand for power arbitrarily close to ε.

For suitably informative, well-separated controls in their declared noise conditions, a concrete declaration would be:

- Safely compatible stratum: require compatible; adverse **and unresolved** count against the sensitivity requirement.
- Safely adverse stratum: require adverse; compatible **and unresolved** count against the sensitivity requirement.

A failure cap of 0.10 under the same uncertainty check is one consistent choice. Mike can choose another prospective target, but a meaningful sensitivity requirement is needed to discharge the previously accepted protection against improper ND. It need not be imposed on every conceivable map merely because its true discrepancy is small or large; its generator, noise conditions and informative domain are part of the declaration.

Thus “unresolved never counts as an error” is appropriate in the middle-case **false-decisive-error** table, not as a universal exemption throughout qualification. If your sentence was intended only in that narrower sense and sensitivity is enforced elsewhere, we agree on the separation. Keep the halt and wrong-cause rules alongside these requirements.

Finally, these empirical bounds concern the registered ensembles and decision units. Five nominal distances do not establish a uniform error bound over all distances, all geometries or canonical lattice output. Level-level checks also do not replace qualification of the arm rule, the seven-arm B conjunction or the full two-arm D search under its newly restricted family meaning.

## 6. The accepted positions and the T0 clarification

### 6.1 No substantive misreading in “accepted without reservation”

The list is faithful to the intended repairs. Acceptance here is agreement about the proposed direction; completed v0.3 bytes and their implementation remain to be reviewed.

| L1 position | L2 readback |
|---|---|
| Q1: unoriented edges | Agreed. Neither occupied-side ordering nor whole-map monotonicity is inferred. The component safeguard also supplies no automatic one-to-one topology claim. |
| R1: post-estimator components and deterministic cases | Agreed. Expected answers must describe the full estimator's output, including legitimate smoothing-induced changes. |
| R5: minimum levels, adjacency, missing outcome and separate precedence | Agreed. Two adjacent adverse levels decide before the insufficient-levels-for-support branch; three informative levels are needed for compatibility. Retain isolated adverse level records. |
| R5: separate D witness sets | Agreed. The two TB arms need not use the same κ witnesses. Qualification must exercise the full search; the meaning of rival exclusion narrows as in §3 above. |
| R6: persistence diagnostic | Agreed. This choice provides no separately specified coupling-sensitive contrast. The independent-response limitation of B/D stands. |
| R7: certified known answers and a complete generator/error table | Agreed. Certify the repaired joint target; retain false compatibility, false adversity and sensitivity protections, with the near-ε treatment above. |
| R8: staged masters, calibration order and typed dependencies | Agreed. Freeze the calibration-to-generator transformations before calibration output; distinguish protocol and result identities. |
| R9: named T0 reference, reporting schemas and finite-tail qualification | Agreed, subject to the explicit fine-grid eligibility below. |
| R10: ordered identities and supporting corrections | Agreed. Canonical masks and levels, their serialization and their use remain bound to the declared procedure. |
| θ provenance | Agreed exactly as stated: a post-probe design choice, frozen before fresh canonical observations; no reuse of probe observations as scoring or calibration data. |

For K, fix the confidence level and whether its pointwise Clopper–Pearson intervals are one- or two-sided. Pointwise probability intervals do not become a simultaneous confidence band or a confidence interval for κ̂_c. Define the four curve descriptions using the registered survival criterion, preserve the counts, and keep nonmonotonicity visible even if a stable suffix exists. The grid bracket remains a panel summary. [Review, R6]

### 6.2 T0: apply the fine-grid condition to the bracket, not just its upper endpoint

**I accept keeping 0.1254 as a fine-grid design tolerance**, with an unevaluable hysteresis branch outside its declared applicability. One detail must be explicit: κ̂_c = 1.0 lies in the numerical interval [1.0,2.0], but its preceding registered level is 0.75. Its entering bracket is 0.25 wide, not 0.10.

Write the eligibility rule in terms of the actual bracketing interval for **each** skeleton boundary. If the bracket is the preceding subcriterion level and the selected stable-suffix level, both endpoints must lie in the fine grid and be separated by 0.10. On the present grid, an upper endpoint at 1.0 does not qualify; upper endpoints 1.1 through 2.0 can qualify when their other phase/validity conditions hold. Absent or nonmonotone crossings retain their distinct causes.

This accepts the reason for avoiding a 0.50 spacing term while preventing the closed lower endpoint from silently importing a coarse bracket. If the eligibility condition fails, preserve the cause and the other T0 test results; T0 remains non-gating for B/D.

For f_J, state the normalization directly, for example the scored adjacent increase

\[
J_j=0.10\,
\frac{\operatorname{med}(\rho_{j+1})-\operatorname{med}(\rho_j)}
{\kappa_{j+1}-\kappa_j},
\]

with the compared range, test domain and reversal/evaluability rule explicitly bound. This is a declared slope-scale criterion on a nonuniform grid. It does not resolve the held question of continuity through the entering interval. [Review, R9; Contract §§2.9, 5.8]

## 7. What should be carried into the next packet

The v0.3 packet should record Mike's choices on the component statistic and m, the restriction of **both** endpoint claims to the registered families where exclusion is asserted, the 950-of-1,000 rule, and the error/sensitivity table. It should then show one consistent definition through the evaluator, qualification truth, outcome labels, aggregation, reporting and record graph.

For this discussion I checked the retained round-1 review identity, calculated the two new synthetic geometry examples, and checked the vote-rule examples and its difference from an interpolated quantile. These checks introduce no canonical observation, probe endpoint or instrument run. No contract or historical review bytes were changed.

These are L2's discussion positions for Mike's ruling. The substantive choices and the repaired contract return for review in the fresh v0.3 packet.
