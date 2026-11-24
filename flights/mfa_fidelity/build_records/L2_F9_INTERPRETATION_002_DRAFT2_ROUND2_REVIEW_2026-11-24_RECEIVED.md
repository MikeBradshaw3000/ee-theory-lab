# L2 → L1 — Flight 9 Interpretation 002, draft 2: round-2 review

**Date:** 2026-11-24  
**Reviewer:** L2  
**Decision authority:** Mike  
**Object reviewed:** the draft interpretation record for the Flight 9 fidelity summaries, not an implementation or a scientific result.

**Archive:** f9_interpretation_002_round2_L2.zip  
**Archive SHA-256:** `6b0963a971c44dedf7d13600c167443647f6576ef092a2ace6e6f49756d3830e`

## 1. Disposition and scope

**Draft 2 is sound as a proposed interpretation record.** The blocking draw-trigger defect D1 from round 1 is closed. The regional-count dependency is now explicit and consistent; the closure fit and signed fitted-level difference have the requested gates; the full compatible-draw range is translated correctly; and the complete change between drafts contains no unannounced reversal of a previously accepted point. Mike's recorded “yes” settles the one additional inclusion reserved to him. No further substantive choice is needed for this interpretation beyond his acceptance of the corrected record. [D2, authority statement, Points 5–9 and Consequences; P2 §§2–4; R1 §§2–6.]

This disposition does not itself make the draft binding. Draft 2 expressly requires Mike's acceptance after L2 review. It also leaves the reports implementation, its build declarations, dependency identities and ordinary review gates to their subsequent work. The packet states that no code for these new summaries exists. The findings below therefore establish the adequacy and consistency of the specification; they do not certify a future implementation, grant a job authorization or assert a canonical timing result. [P2 §§0–1; D2, authority statement and Consequences; F §5.]

### Answers to L1's six questions

| Question | Answer |
|---|---|
| **Q1 — Is D1 closed in both named states?** | **Yes.** With the declared stream identity and key held fixed, observed-value availability cannot change the shared draw matrix or suppress applicable stochastic summaries. A fixed closure-side failure of step 4 blocks the direct edge statistics on every draw and is recorded as “not assessed on the draws.” It is not reported as 1,000 assessed draws with no defined values. |
| **Q2 — Are the regional counts consistent, and whose choice are they?** | **Yes.** They are explicitly lattice-only, zero is defined, and their ranges survive closure unavailability. This is the completion R1 expressly left to L1, now disclosed in the text. It requires no separate scientific decision by Mike beyond accepting the record. |
| **Q3 — Are the fit gates and signed difference complete?** | **Yes.** Each fitted label depends on its own map and family. The difference is lattice minus closure for the same index, arm, object and level. Its compatible-draw range is a constant translation with the original compatible-draw count. No further scientific choice about the retained fits is missing. |
| **Q4 — Did a repair reverse an accepted point?** | **No unannounced reversal was found.** The regional-count dependency is a disclosed choice between the alternatives R1 allowed. The other changes implement the requested repairs, clarifications and editorial corrections or record Mike's inclusion decision. |
| **Q5 — Is another word from Mike needed?** | **Only acceptance of this corrected interpretation record at this stage.** Later build review, declarations and job authorizations retain their existing requirements. The closure-fit inclusion need not be put to him again. |
| **Q6 — Anything else?** | **No additional blocker.** Section 7 identifies the important implementation consequences and limits of this review. They follow from the accepted wording and are not new scientific choices. |

The supporting analysis and precise source references follow.

## 2. Identity, provenance and sources

### 2.1 Independent packet checks

| Item | Independently checked result |
|---|---|
| Archive SHA-256 | `6b0963a971c44dedf7d13600c167443647f6576ef092a2ace6e6f49756d3830e` — matches the value supplied by Mike. |
| Manifest payload count | **18 files**, plus MANIFEST.txt itself: **19 regular files**. The ZIP's directory entries are not payload files. |
| Manifest verification | All 18 listed paths and computed SHA-256 digests match; no duplicate, missing or unlisted regular file. |
| MANIFEST.txt SHA-256 | `9ad9b98b81b9d9dcca4d551dba568f951ec8a3e8d01ca721c38d13271047013e` |
| Draft 2 SHA-256 | `c7d8b54901f021dcdbcaf69b5aa17abee2ae2e7d98c921259e80c6f910cbdb63` |
| Received round-1 review SHA-256 | `3d892d6ebbbbcecbb3c9241c7acd0d510232a806a22cef445a9684b895efa2d9` |
| Supplied and recomputed complete diff SHA-256 | `a8952884d30a75ee3dca92897a5948b6cf9868ecf021e92dd78636d755d2b11a` — ordinary diff output is byte-for-byte identical. |
| Frozen contract SHA-256 | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` — matches the freeze record's identified contract. |

The received round-1 review also matches the separately uploaded copy byte-for-byte. It is the review of archive `b489e5d703d592343f319ff164b19ddd27d3e37a4a27168026ffa7033490224b`, not an M6 build review. Draft 1 in packet_only/draft1/ has the identity recorded in that review. These checks establish the review lineage and the bytes assessed here.

P2 reports repository pin `c6c21c497366d3ca71e0487127c774aacfd14ba1` and describes the reference files as copies of that pin. This review verifies the supplied archive and its internal relationships; it does not independently attest to a fresh remote checkout. P2 also identifies the evaluator as the placed reference version whose separate precedence repair is cleared and awaiting placement. The present interpretation does not depend on the ordering changed by that repair. [P2, opening provenance statement; D2, Consequences.]

### 2.2 Citation key

References below identify material inside this archive. Section and Point references are to the named document; function references are to the named source file.

| Key | Archive path |
|---|---|
| **P2** | L1_TO_L2_F9_INTERPRETATION_002_ROUND2_RESPONSE_2026-11-24.md |
| **D2** | flights/mfa_fidelity/rulings_draft/F9_INTERPRETATION_002_FIDELITY_SUMMARIES_DRAFT_2.md |
| **D1** | packet_only/draft1/F9_INTERPRETATION_002_FIDELITY_SUMMARIES_DRAFT_1.md |
| **Δ** | draft1_to_draft2.diff |
| **R1** | review/L2_F9_INTERPRETATION_002_DRAFT1_ROUND1_REVIEW_2026-11-23_RECEIVED.md |
| **C** | flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md |
| **F** | flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md |
| **I001** | flights/mfa_fidelity/rulings/F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md |
| **D001** | flights/mfa_fidelity/rulings/F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md |
| **E** | flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py |
| **CL** | flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py |
| **SP** | flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py |
| **W** | review/l2_i002_draw_gate_witness.py |

## 3. D1 is closed: draw generation and dependency accounting

### 3.1 The operative rule now has one reading

Round 1 found that draft 1's draw trigger could be read as requiring an available observed summary before drawing. That allowed two implementations to disagree when the observed lattice map had no edge and the closure was unavailable, even though a replacement draw could have an edge and define local-m summaries. The required repair was to separate coverage, fixed dependencies, observed values and draw-specific definition. [R1 §2.]

Draft 2 supplies that separation:

1. Point 8 binds one shared 1,000-draw matrix per covered arm, object and level. Its generation does not require an observed edge, an observed summary value or a contour fit.
2. “When the draws are made” requires the draws for applicable summaries with complete valid inputs and explicitly names the original non-T0 witness state.
3. “Fixed dependencies” distinguishes a field blocked on every draw from a field actually assessed on 1,000 draws but defined on none. Blocking one field cannot suppress the others.
4. Point 9 says its geometric rows describe observed values, while Point 8 governs draw availability; its general fixed-dependency row reinforces the distinction.
5. The new summary draws do not create any extra family fits or item-(iv) draw labels when the evaluator did not resample.

These provisions jointly close the old gate. “Same draws” means the same matrix under the same declared stream, bound source identity and key. It does not leave an implementation free to replace a stream or invent new evaluator fits. The skeleton dependency is bound to the ultimately accepted M6B declaration before output, as discussed in section 7. [D2, Points 8–10 and Consequences; E, resample_multiplicities and evaluate_level.]

### 3.2 Original witness: absent observed edge and unavailable closure

The supplied witness was copied outside the packet and rerun without changing its bytes. It constructs 40 integer tail-count maps on a 100 × 100 lattice: 19 maps have occupancy 400/1,000 on a 20 × 20 patch and 21 maps are zero. A valid replacement draw doubles one patch map and omits one zero map, giving 20 patch-map occurrences. Periodic 3 × 3 smoothing and the tie-inclusive threshold yield:

| Quantity | Observed mean | Constructed replacement draw |
|---|---:|---:|
| Patch-map occurrences | 19 | 20 |
| Maximum integer box numerator | 68,400 | 72,000 |
| Threshold numerator | 72,000 | 72,000 |
| Occupied region cells | 0 | 324 |
| Complement cells | 10,000 | 9,676 |
| Boundary bonds | 0 | 72 |
| Distinct inside edge cells | 0 | 68 |
| Distinct outside edge cells | 0 | 72 |
| Passes step 4 | No | Yes |

These are reproduced numerical outputs of W, whose computed SHA-256 is `87bdcb0239f4cec07e494775b0b34a37b3a2b9d6223875a96dc161ff551331af`. They show a possible draw with positive support under whole-seed replacement sampling. They do **not** assert that a particular canonical 1,000-draw matrix contains that draw. Closure unavailability is stipulated for the logical witness; no closure solver was run. [W; C §5.5 steps 1–4.]

For that state, assuming valid lattice inputs and the required fixed local-m field, draft 2 determines the following:

| Field or operation | Required treatment |
|---|---|
| Shared resampling matrix | Generate the declared 1,000 draws. The absent observed edge and unavailable closure do not cancel the matrix. |
| Point 2 edge-cell summaries | Observed values have no edge. Assess all draws using each draw's own region and endpoint sets; a draw with an edge can define them, including below the step-4 minimum. |
| Point 3 median contrast against 1 | Assess on the same draw endpoint sets. It has no closure dependency. |
| Point 3 contrast against T0 | Assess if the fixed T0 reference exists. If it does not, record reference unavailability and “not assessed on the draws” for this contrast alone. |
| Point 5 residual statistics | Comparator unavailable; not assessed on the draws. No unconverged iterate is substituted. |
| Point 5 regional counts | Retain 0 and 10,000 at the observed point. Both count fields remain defined on every draw. |
| Point 6 closure geometry and fit | Unavailable with the fixed closure cause. |
| Point 7 direct S and global terms | Blocked by the closure dependency; not assessed on the draws. |
| Point 7 fitted-level difference and translated range | Unavailable because no closure label exists. Preserve any independent lattice fit information actually supplied by the evaluator. |
| Existing item-(iv) resampling | The observed map fails step 4, so the new summary draws do not create the draw fits that the evaluator skipped. |

This accounting follows D2 Points 4–9. It rejects both previous divergent implementations: skipping all draws because no observed edge exists, and suppressing edge-cell draws because the closure is absent. It also preserves the contract's narrower applicability for the evaluator's own step-9 fits. [D2, Points 4–9; C §5.5 step 9; E, evaluate_level.]

### 3.3 A closure edge exists but fails step 4

This second state is also determined. Point 7 requires **both maps** to pass step 4 for the direct edge comparison. The closure geometry is fixed across seed draws. Its failed gate is therefore a fixed dependency failure for S and its reported global terms, even though the converged probability map and a nonempty edge exist. Point 9's fixed-dependency row applies to any scalar blocked on every draw, not just to a nonconverged closure. Point 8 expressly includes the closure's geometry and fit among its fixed dependencies. [D2, Points 6–9.]

Accordingly, S and its global terms are **not assessed on the draws**, with the closure-side under-resolution cause. Reporting them as assessed on all 1,000 draws with zero defined values would contradict the general rule. The other fields keep their own domains:

| Field | Consequence of fixed closure geometry failing step 4 |
|---|---|
| Whole-lattice occupancy residuals | Remain available: the converged probability map exists. |
| Regional occupancy residuals | Remain available on each nonempty lattice subset, including draw-specific subsets. |
| Lattice regional counts | Remain available, with both counts defined on all draws. |
| Local-m summaries and contrasts | Follow their lattice-edge and reference requirements; the closure gate does not control them. |
| Closure fitted level | Unavailable because its own step-4 prerequisite fails, regardless of what the low-level fit helper could return. |
| Fitted-level difference and translated range | Unavailable because the fixed closure fitted level is absent. |
| Lattice fitted level and existing compatible-draw range | Retained whenever independently supplied under the evaluator's rules. |

As a separate geometry check, a floating probability map equal to 0.4 on a 10 × 10 square and zero elsewhere gives **96 occupied cells and 40 boundary bonds** after the declared smoothing and threshold. Its edge exists, but its region fails the 100-cell minimum. This illustrates the distinction between “map and edge exist” and “map passes step 4.” It is a constructed geometry example, not a claim that a registered closure solver returns that particular map. [Independent geometry calculation; C §5.5 steps 1–4.]

**D1 disposition: closed.** No further wording repair is required to obtain this treatment; it follows from the combined operative rules.

## 4. Regional counts and uncertainty domains

Point 5 now makes the two counts `n_R = |R|` and `N − n_R` lattice-only fields. It distinguishes them from the three residual statistics on R and its complement. Zero is a defined count; an empty subset has no residual statistic. Point 8 includes both count fields in its ranges, explicitly including zero. Point 9 limits comparator unavailability to the residual statistics and separately preserves the count fields and their ranges. These statements agree. [D2, Points 5, 8 and 9.]

For a covered non-T0 panel with complete valid lattice inputs, both counts are consequently defined on all 1,000 draws. Their ranges are not conditional on a nonempty region. If every draw has zero occupied cells, `[0, 0]` is a legitimate occupied-count range. That is different from an edge statistic with no defined draw values, for which no endpoints exist. The complementary count is similarly defined when the region is full. Each draw reconstructs R before assigning regional residuals or counts; the observed partition is not held fixed. [D2, Points 5 and 8.]

This is an explicit dependency choice, not a claim that draft 1 already unambiguously said the same thing. Draft 1's broad comparator-unavailable row could cover the whole Point 5 block. R1 §3.1 expressly allowed L1 to keep the counts independently of the closure if the text said so and applied the draw rule to them. R1 §5 treated the count ranges as acceptable without another scientific approval. Draft 2 identifies L1's completion instead of attributing an unrecorded choice to Mike. [D1, Point 9; R1 §§3.1 and 5; P2 §3; D2, Point 5.]

Coverage remains constrained. Regional fields apply to the non-T0 realization and skeleton-high panels named in the coverage table. T0 remains whole-lattice occupancy comparison only; it acquires no regional, edge or fit fields. Skeleton-low remains outside this fidelity block. Non-T0 skeleton means continue to use all 40 recorded tails, including zeros after extinction. [D2, constraints 3–4 and Point 8; C §§4.3 and 5.7.]

For the new stochastic scalar summaries, the 2.5–97.5 percentile endpoints use their defined draw values, accompanied by the 1,000-attempt accounting, number defined and undefined causes. No draw replacement, imputation or new minimum-defined count is allowed. These are conditional empirical ranges, not confidence intervals or a substitute for the scored 950-of-1,000 support rule. The reference contrast holds the T0 threshold fixed and displays its separate persistence information; it does not claim to propagate uncertainty in that reference. [D2, Points 3 and 8; C §§5.4–5.5 and 5.7.]

The treatment of an unavailable or non-monotone T0 reference remains consistent with the frozen persistence rules and the existing T0 record. A descriptive suffix statistic is not promoted to a threshold. An available all-levels-met threshold remains identified as lower-unbracketed. Nothing here reopens Interpretation 001's hysteresis or sampled-range decisions. [D2, Points 3 and 10; C §5.4; I001, Consequences.]

## 5. Retained fits, signed difference and compatible-draw range

### 5.1 Each fit belongs to its own map

The closure's fitted level for index Y requires its own map to pass step 4, a nonempty registered family for Y and a within-ε fit. Draft 2 now states all three requirements and notes that the low-level fit function does not enforce step 4 itself. That is the necessary guard: E.fit handles a supplied edge and family, while E.evaluate_map supplies the geometry gate before fitting a lattice map. An empty family returns no within-ε fit. [D2, Point 6; E, fit and evaluate_map; C §5.5 steps 4–7.]

The lattice label likewise requires its own step-4 pass and within-ε point fit. Its availability does not depend on the closure's geometry. Conversely, a closure label can survive an uninformative lattice map. Neither label depends on a final compatible scored outcome: the point fit and the result of resampling are distinct records. Point 9 correctly retains independently defined fidelity values beside unstable, unresolved or adverse results. [D2, Points 7 and 9; E, evaluate_map and evaluate_level.]

Direct edge S has a separate domain: both operational maps pass step 4, but neither needs a fitted family label. Thus an outside-ε family fit does not erase a separately available S. Equally, an unavailable two-map comparison does not erase a valid fit to one map. All applicable causes remain visible if several dependencies fail. [D2, Points 7 and 9.]

### 5.2 Sign, matching and range are fixed

The observed difference is explicitly:

`d_Y = λ*_(lattice,Y) − λ*_(closure,Y)`

The labels have the same index Y, arm, level and object. Even on a shared geometric family, the comparison cannot subtract P's label from H's. Both observed labels must exist before an observed difference is reported. These are the sign and matching rules requested in round 1. [D2, Point 7; R1 §3.2.]

Let `c_Y` be the fixed closure label and `[L_Y, U_Y]` the existing full min–max range over compatible lattice draws. Point 8 specifies:

`[L_Y − c_Y, U_Y − c_Y]`, with the same compatible-draw count.

This is the complete range of the shifted labels because subtracting a fixed constant preserves their ordering. It is not the new summaries' percentile recipe. For example, compatible labels 0.3, 0.5 and 0.8 with closure label 0.4 give the difference range `[−0.1, 0.4]` and count 3. An exact-fraction arithmetic check confirms these endpoints. [D2, Point 8; C §5.7, fidelity-uncertainty row; independent arithmetic.]

The range can exist without an observed difference. A concrete allowed situation is an informative observed lattice map whose point fit is outside ε, while the evaluator's actual resampling produces compatible fitted labels. If the closure label exists, those labels still have a translated range. This does not authorize a range for the earlier no-observed-edge witness: there the evaluator did not perform its fits, and the new summary matrix supplies no replacement labels. Draft 2 preserves that distinction explicitly. [D2, Points 8 and 10; E, evaluate_level.]

If the closure label is absent, neither the difference nor its translated range is supplied. If the evaluator assessed its draws but none was compatible, its no-compatible-resample state remains. If it did not resample, that different state remains. A descriptive least S among contours examined is neither a fitted label nor necessarily the minimum over the whole family. [D2, Points 6–10; C §5.5 step 7.]

**Q3 disposition:** the retained fits are sufficiently determined for this interpretation. Future build declarations still specify representation and the bounded numerical details discussed below, but no unresolved scientific inclusion, sign, fit gate or uncertainty target remains.

## 6. Complete-diff review and round-1 closure ledger

The ordinary diff computed directly from the supplied drafts is byte-identical to Δ. A line comparison identifies 16 changed spans. The following ledger groups the substantive completions; its rows are not a count of diff spans.

| Round-1 issue or request | Draft-2 treatment | Disposition |
|---|---|---|
| D1: observed-value draw gate | Point 8 separates coverage, observed values, fixed dependencies and per-draw definition; Point 9 reinforces the distinction. | Closed. |
| Regional zero counts and closure dependency | Points 5, 8 and 9 explicitly retain lattice-only counts and their ranges, zero included. | Consistent completion of the alternative left to L1. |
| Own-map fit gates | Point 6 explicitly guards the closure fit; Point 7 separates the lattice and closure labels. | Closed. |
| Signed fitted-level difference | Point 7 gives lattice minus closure with matched index, arm, level and object. | Closed. |
| Translated range and absent point value | Point 8 gives the full shifted compatible range and count; it permits that range without an observed difference. | Closed. |
| Sole inclusion needing Mike | The authority statement records his “yes”; the conditional strike recipe is removed because the fits are retained. | Decided. |
| Stream and source binding | Point 8 and Consequences bind accepted declarations and source identities before output; silent later migration is forbidden. | Closed at specification level. |
| Bounds on build declarations | Consequences preserve the contract's internal S interpolation, named causes, availability domains and uncertainty targets. | Closed. |
| Cost wording | Consequences forbid additional family searches for these summaries while retaining the evaluator's existing step-9 work; no timing claim is made. | Closed. |
| Complete §5.7 quotation | The full fidelity-uncertainty table cell is quoted exactly, including the conditional λ* range qualification. | Exact text equality independently checked. |
| Descriptive least S | Point 10 says “among the contours examined,” which need not be the family minimum and is not λ*. | Closed. |
| Geometry recomputation and extinction wording | Point 8 says geometry is rebuilt where the summary needs it; constraint 3 retains zeros after extinction. | Closed without enlarging T0 coverage. |
| §5.9 identity completeness | Consequences require all applicable identities existing at the record's stage; the displayed list is explicitly nonexhaustive. | Closed. |

Sources: Δ; R1 §§2–7; D2, authority statement, constraints, Points 5–10 and Consequences; P2 §§2–3.

The unchanged accepted substance includes distinct inside and outside endpoint-cell sets with equal cell weights; raw local-m values from the declared gain and raw index; the fixed T0 benchmark; availability of local-m summaries below the step-4 minimum when an edge exists; unsmoothed occupancy residuals; draw-specific regional selection; and the complete direct S with both global terms and all resolved-component terms. The θ, ε and m settings, the all-level coverage, the absence of T0 edge comparisons and the separation from scored B and D also remain intact. [Δ; D2, Points 1–8; C §§1.2′, 4.3 and 5.5; SP, local_m.]

The comparison preserves the closure's numerical status as well. Direct geometry uses the floating closure map under its own smoothing and threshold; it does not manufacture seed counts. The threshold-near-cell count is descriptive and does not certify threshold stability. The solver's last change remains a convergence diagnostic rather than a bound on distance to the fixed point. No cap, tolerance or comparator-unavailable rule is altered. [D2, Point 6; C §4.2; CL, iterate.]

Disclosure 001 remains conditional on the arms actually measured or subsequently observed: an unavailable skeleton closure at the crossing stays unavailable, while an arm that converges has a comparator. This review has not extended the disclosure's measured scope or run additional arms. The retained lattice-only summaries are consistent with reporting comparator unavailability without dropping the level. [D001, “What is disclosed” and “What follows”; D2, Points 8–9.]

## 7. Authority, implementation consequences and verification limits

### 7.1 Authority is now complete for acceptance

R1 identified the closure's own family fit and fitted-level difference as the only additional substantive inclusion requiring Mike's decision. P2 §2 records his affirmative answer on 2026-11-24; the current user transmittal confirms that answer; and D2 carries it into its authority statement. The count-field completion was expressly left to L1. There is no remaining reason to request another choice about either inclusion. [R1 §5; P2 §2; D2, authority statement and Point 5.]

Mike's acceptance of this revised record remains necessary because the draft says it is not yet binding. Later build declarations and stage authorizations continue to apply to their own objects. This is a statement of the record's existing status, not an additional condition introduced by this review. [D2, authority statement and Consequences; F §5.]

### 7.2 What the later build must preserve

The accepted specification has concrete implementation consequences:

- Bind the ultimately accepted skeleton stream declaration and source identity, and the accepted evaluator identity, before output. Use the same declared matrix for the summaries that share an arm, object and level. Do not treat the reference packet's older dependency bytes as clearance for a future build.
- Keep fixed-dependency blocks separate from 1,000 assessed draws with zero defined values. In particular, a fixed closure-side step-4 failure blocks S, while an absent family fit alone does not block S.
- Preserve regional zero counts on every applicable draw and rebuild the partition on each draw. Empty subsets affect residual statistics, not the existence of their count fields.
- Preserve the independence of each map's fit, the same-index subtraction, and the translated compatible range even when the observed difference is absent. Do not create fitted labels where the evaluator did not resample.
- Reuse the existing threshold-fidelity and item-(iv) records with their availability distinctions. Do not replace them with a new uncertainty recipe or relabel an examined-contour descriptive value as λ*.
- Retain all applicable scientific causes, and keep missing or corrupt required input and runtime faults as apparatus failures. Encode them without changing their meanings.

These are consequences of D2 Points 5–10 and Consequences, not newly proposed gates. The discriminating states in sections 3–5 provide useful cases for the later implementation review.

Build declarations may specify field names, encoding, accumulation order, interpolation for the new spatial quantiles and new ranges, maximum-location ties, caching and accepted dependency bindings. They may not reopen the linear interpolation already fixed inside S, choose different availability domains, replace named causes or change the uncertainty targets. The full §5.9 requirements apply according to which identities exist when a record is written; protocol and qualification-result identities are not interchangeable. [D2, Consequences; C §§5.5 and 5.9.]

The cost statement is appropriately bounded. The additional summary procedure needs no additional family search on every draw; the existing evaluator's searches still occur where its rule requires them. This is an algorithmic scope statement, not evidence of affordable runtime. No narrower level coverage, fewer draws, survivor-only averaging or frozen regional membership is authorized as a cost adjustment. [D2, Point 8 and Consequences; R1 §6.2.]

### 7.3 Checks performed and their limits

The review performed archive and per-file digest verification, identity and review-lineage comparison, a byte comparison of the complete diff, a point-by-point regression review against R1, and source inspection of the relevant contract provisions and supplied functions. It checked the quoted §5.7 fidelity row against the contract exactly. It reran the supplied synthetic draw witness outside the packet and checked the under-resolved float-map geometry and the range-translation arithmetic described above.

No packet file was modified. No closure solver, lattice dynamics, canonical stream, master draw, qualification job or scientific Flight 9 job was run. The synthetic replacement weights are deliberately constructed and are not represented as a registered stream realization. The geometry example is not represented as a computed scientific closure.

No full implementation suite was run for this prose-only review. The packet contains reference source files and states that the new summary implementation does not yet exist; the checks above resolve the interpretation defects without claiming integration coverage. The separately cleared evaluator precedence repair has not been re-adjudicated here. [P2, opening statements and §1; D2, Consequences.]

## 8. Review conclusion

D1 is closed, all requested clarifications are incorporated consistently, and the retained fit inclusion has the recorded decision authority. The complete change preserves the previously accepted definitions and the frozen contract's scoring and uncertainty distinctions. There is no outstanding repair required before Mike considers accepting draft 2 as the interpretation record. Acceptance and subsequent implementation review remain separate acts.

FINAL VERDICT: SOUND
