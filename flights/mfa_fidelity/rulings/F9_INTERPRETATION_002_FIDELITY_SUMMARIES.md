# Ruling Record — F9 Interpretation 002: the fidelity summaries of §1.2′ (ii) and (iii) and their uncertainty (Contract F9 v0.7 §1.2′, §5.7 row 4)

**Authority, stated exactly.**
- On 2026-11-23 L1 put eight open points (A to H) and a proposal for each to L2 as a consultation (`L1_TO_L2_F9_FIDELITY_SUMMARIES_CONSULTATION_2026-11-23.md`, `5811f97b2f2c9022db034cd3bcf359c62f2a932055550ee2bd30778d904b7f18`). L2 advised (`L2_F9_FIDELITY_SUMMARIES_CONSULTATION_RESPONSE_2026-11-23_RECEIVED.md`, `c9df277a8d38449b2c37417e167a1aa6971f2fd8081a4283cac0f9cdf8b0156b`), ending in a six-point package (its §6) and one supported smaller alternative (an occupancy-only closure report).
- L1 recommended to Mike: adopt L2's six-point package; include the direct edge comparison; record the readings in an interpretation beside the contract, reviewed by L2, before any code. **Mike, 2026-11-23: "Adopt, include, l2 review".**
- L2 reviewed draft 1 (`b2efdeda1d063ccb6d46d66e0c8d0881d5131015221d1e4f20fb6bed943d1a07`) and returned NOT SOUND on one finding, D1: the sentence saying when the resamples are made left room for two builds that differ (`L2_F9_INTERPRETATION_002_DRAFT1_ROUND1_REVIEW_2026-11-23_RECEIVED.md`, `3d892d6ebbbbcecbb3c9241c7acd0d510232a806a22cef445a9684b895efa2d9`). It asked for five smaller completions and three editorial corrections, and confirmed that one inclusion remained Mike's to decide: the closure's own fit to the registered family and the fitted-level difference.
- **Mike, 2026-11-24, on that inclusion: "yes".** They are kept (Points 6 and 7).
- L2 reviewed draft 2 (`c7d8b54901f021dcdbcaf69b5aa17abee2ae2e7d98c921259e80c6f910cbdb63`) and returned **FINAL VERDICT: SOUND** as a proposed interpretation record (`L2_F9_INTERPRETATION_002_DRAFT2_ROUND2_REVIEW_2026-11-24_RECEIVED.md`, `930642a329cff452b26818b0f2f350d39901d3611e49f0367a191abd46d3f1de`): D1 closed; no accepted point reversed; no further choice needed of Mike other than acceptance. The one completion L2 left to L1 (Point 5, that the regional cell counts are lattice fields) it found consistent and within what it had left open.
- **Mike accepted the record on 2026-11-24 ("accept").** This is the accepted text. It differs from the draft 2 L2 reviewed only in its title, in the last two entries of this authority statement, and in the status line beneath it ("Status when accepted" is now "Status"); `f9_interpretation_002_draft2_to_final.diff` is the whole difference.

**Status:** an identified interpretation of the FROZEN contract (`FLIGHT_9_CONTRACT_v0_7.md`, SHA-256 `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`). The contract's bytes and identity are unchanged.

**Scope.** The fidelity tier only. §1.2′: "pre-registered in full; reported with uncertainty in every record, favorable or not; never scored." Nothing here is scored, enters B or D, gates an endpoint, or changes a scored tolerance, the estimator of §5.5, the resample count or any placed module. A poor comparison is published as such.

**Why before any code.** No Flight 9 job has been run and no master has been drawn. The contract fixes the quantities, comparators, geometry and uncertainty recipes of the fidelity tier. It does not fix every reduction of them to a reported number. Each reduction below is a choice that could otherwise be made after seeing output. L1 has not opened the probe arrays and has computed none of these summaries on any output of the rule.

## The sentences

§1.2′: "(ii) Local m_i = g·λ_i·Δt/q on the observed edge, against 1 (a local homogeneous benchmark) and against κ̂_c,T0; neither is a pointwise prediction. (iii) Seed-mean occupancy against the site closure's fixed-point probabilities (§4.2), matched in object and floor; where edges are compared, the §5.5 rule is applied to both maps. The lattice map is a finite-tail mean and the closure a fixed point, so their difference includes finite-time effects and is not an isolated stationary closure error. (iv) The fitted level λ*_X of §5.5 at each level."

§5.7 row 4, in full: "Occupancy-based items: 2.5–97.5 percentile range over 1,000 seed resamples. κ̂_c: per §5.4. λ*: its range over the resamples with Δ ≤ ε, with the number of such resamples; "no compatible resample" if there is none. That range is conditional on compatibility and is not a confidence interval."

## What is already fixed (restated as constraints; this record gives no discretion over them)

1. The region, edge and components are those of §5.5 steps 1 to 3: the 3×3 periodic mean of the seed-mean occupancy, θ = 0.20 with ties included, the periodic 4-neighbour boundary bonds, every connected boundary piece a component under the contract's corner rule. Neither raw occupancy nor an index contour redefines the region.
2. Uncertainty for occupancy-based items is from 1,000 resamples of the 40 seeds.
3. The skeleton's seed mean is unconditional: all 40 runs, an extinct run contributing its recorded tail, zeros after extinction.
4. **T0's spatial edge "is never compared with anything" (§4.3).** T0 has no edge-based fidelity item.
5. Local m_i is persisted (§2.8), computed from terrain arrays and adjacency before any dynamic data, and never normalized by an observed onset, occupancy or fitted edge.
6. **λ*'s uncertainty is its full range (least to greatest) over the resamples with Δ ≤ ε, with their count** (§5.7 row 4). It is not a percentile range.
7. All 25 registered levels stay in the record with their unavailable states (§2.9, §7). Closure not converged is `comparator unavailable`; κ̂_c,T0 absent is `reference unavailable`; an extinct skeleton run is a valid observation.

## Point 1 — the cells "on the observed edge"

**Open.** An edge is a set of bonds; a bond has two cells. The contract does not say which cells carry the m distribution, or with what weight.

**Readings.** (a) Two sets of distinct cells, the inside endpoints and the outside endpoints of E's bonds, each cell counted once. (b) Every bond counted once, with its inside and outside cell, so a cell on three bonds appears three times. They are different statistics and can give different quartiles on corners and irregular boundaries.

**The interpretation: (a).** The **inside edge cells** are the distinct cells of the region having at least one bond of E; the **outside edge cells** are the distinct cells outside the region having at least one bond of E. They are reported separately, each cell with equal weight. Cells of every component of E are included, whatever the component's size; the 40-bond resolution of §5.5 does not remove them. Neither side is privileged, and the edge stays unoriented (§1.4).

## Point 2 — what is reported of m

**The interpretation.** For each of the two sets: the number of cells, and the minimum, 0.25, 0.50 and 0.75 quantiles and maximum of m_i over the set. m_i is the value the placed `spectral.local_m` gives from the arm's raw index and the level's recorded gain (the contract's written expression g·λ_i·Δt/q); the comparison array rounded for contours is not used. These are **spatial** summaries across cells; the ranges of Point 8 are a different kind of quantile and are labelled apart.

The report does not list per-cell values. §2.8's requirement that local m be persisted is met by an identified artifact of the run record or bundle, which the fidelity record names; which artifact that is belongs to the runner's build.

## Point 3 — "against 1" and "against κ̂_c,T0"

**The interpretation.** For each set, the median of m minus 1, and the median of m minus κ̂_c,T0 expressed as κ (micro-units ÷ 10⁶). Both carry the contract's label: not a pointwise prediction.

**The T0 reference is held fixed.** κ̂_c,T0 is T0's recorded skeleton-high threshold on the registered grid. Across resamples it is the same number, so the range of the second contrast is the range of the median shifted by a constant: it is conditional on the recorded reference and includes none of the reference's own uncertainty. T0's profile, bracket, lower-unbracketed status and unavailable cause are shown beside the contrast; their uncertainty stays §5.4's panel-and-grid description. A descriptive suffix of a non-monotone profile is not a threshold.

## Point 4 — when the edge-cell summaries exist

**Open.** §1.2′ (ii) says "on the observed edge" and does not say whether the level must pass §5.5 step 4.

**Readings.** (a) Only on levels whose edge is informative under step 4. (b) Wherever the region is neither empty nor full, so that an edge and its cells exist, with the level's under-resolved state flagged.

**The interpretation: (b).** Points 1 to 3 are reported for every level of a non-T0 realization arm whose region has at least one bond, with a flag when step 4's minimums are not met. An under-resolved boundary still identifies cells and their m; reporting them authorizes no scored claim at that resolution. A region that is empty or full has no edge cells and the summaries carry `no edge at θ`. The final scored label of the level (adverse, unresolved, unstable) does not remove a defined summary.

## Point 5 — occupancy against the closure

**The interpretation.** With p̄ the **unsmoothed** seed-mean occupancy and p* the converged closure map for the same arm, level, object and floor, e_i = p̄_i − p*_i, and for a non-empty set U of cells:

  bias_U = mean of e over U;  RMSE_U = √(mean of e² over U);  M_U = max over U of |e|.

- **Primary:** U = the whole lattice.
- **Supplementary:** U = the region R (p̃ ≥ 0.20) and U = its complement. A subset needs only to be non-empty; step 4's minimums do not apply to these. The three statistics on an empty subset are unavailable while those on the other subset and on the whole remain.
- **The two regional cell counts,** n_R = |R| and N − n_R, are reported beside them. A count of zero is a defined count, not a missing one. **They are fields of the lattice map alone** and do not depend on the closure: they are reported, with their ranges, when the closure is unavailable. (L2 left this to L1 to state one way or the other; the alternative is to treat the counts as part of the closure comparison and drop them with it. L1 chose this because a count is defined whatever the comparator's state.)
- **On each resample the region is rebuilt** from that resample's smoothed mean, and the regional summaries are taken on R_b and its complement. (The other reading holds the observed region fixed and measures error conditional on that partition. It can give materially different ranges.)
- The cell of the largest |e| is reported for the observed map only, under a declared tie rule. Ranges are for the magnitude M_U, never for a location.

Every such record repeats the contract's caution: a finite-tail mean against a fixed point; not an isolated stationary closure error.

## Point 6 — the §5.5 rule on the closure's map

**The interpretation.** The closure map is one float map with no seeds. Its geometry is §5.5 steps 1 to 4 applied to it directly: the 3×3 periodic mean of p*, the region {p̃* ≥ 0.20} with ties included, its edge, components and step-4 minimums. No tolerance is added to the threshold, the map is not converted to counts, and no seed panel is manufactured from it. Step 9 does not apply and the record says so.

Beside the region the record gives the number of cells with |p̃* − θ| ≤ 1e-9. That count gates nothing and **certifies nothing**: the solver stops on the change of one iteration, which is not a bound on the distance to the fixed point, and machines may differ. The closure map's identity, iteration count and last change are kept.

**The closure's own fit (kept: Mike, 2026-11-24, "yes").** The closure edge is fitted to the arm's registered family, once per arm, object, level and index, by the placed fit and its tie rule. A closure λ* for index Y exists only when all three hold: **the closure map itself passes step 4's minimums**; the family of Y is not empty; and the fit is within ε. (The placed low-level fit applies no step-4 test of its own; the rule here is §5.5's, in which step 4 precedes the fit.) Otherwise its cause is kept, and a least-S diagnostic outside ε is not called λ*.

## Point 7 — "where edges are compared"

**Open.** The sentence binds the common rule where an edge comparison is made. It does not require one, and names no measure.

**Readings.** (a) Compare the two operational edges directly. (b) Report occupancy only (Point 5) and compare no edges. Both are supported; (b) is the smaller report.

**The interpretation: (a), ruled by Mike ("include").** When the lattice map and the closure map **both pass step 4's minimums**:

- S(E_lattice, E_closure) of §5.5 step 6 in full: the two directed global 0.95-quantile terms and the term of every resolved component on each side; S is their maximum. The complete value is computed (no early exit at ε).
- The indicator S ≤ ε = 2.0 cells, as a description. It is a fidelity comparison and takes no word of the scored vocabulary.
- No index fit and no evaluator label is required for it. Two edges can both be informative and fit no registered contour.
- Edges are unoriented: agreement of location says nothing about which side is occupied. Point 5 is the probability-level comparison.

**Fitted levels.** Each fitted level stands on its own map: the lattice λ* for index Y exists when the lattice map passes step 4 and its own point fit is within ε; the closure λ* for Y as in Point 6. Neither depends on the other map's geometry. Their difference, for the **same index Y** on the same arm, level and object (on a shared family, P's label is never subtracted from H's), is

  d_Y = λ*_lattice,Y − λ*_closure,Y,

and exists for the observed map when both labels do. An absent fitted level does not remove an available S, and an absent S does not remove a fitted level.

## Point 8 — coverage and the resamples

**Coverage.**

| Object and arms | Reported |
|---|---|
| Realization, the fourteen arms other than T0, every level | Points 1 to 4; Point 5 whole and regional; Points 6 and 7; item (iv) as the evaluator gives it |
| Skeleton (all cells active at t = 0), the fourteen arms other than T0, every level | Point 5 whole and regional; Points 6 and 7, with the skeleton closure (no floor, start 1) and the unconditional 40-seed mean. Points 1 to 4 are not computed: §1.2″ defines the observed edge in the realization |
| T0·P, realization and skeleton-high, every level | Point 5 on the whole lattice only. No region, no edge item, no fit (§4.3). Edge items are `not applicable`, not failed |
| T0's low-initialization sweep | Not in the fidelity tier (§5.8 owns it) |

At θ = 0.20 only: §1.3 (f)'s full evaluator output at 0.10 and 0.30 stands as it is and these summaries are not repeated there. On the canonical records of §8 steps 11 to 13 only: the stability panel has its own report and these summaries are not repeated on it.

**The resamples.** 1,000 draws of 40 whole seed maps with replacement, by the declared evaluator stream of the arm, object and level. For the realization that is the scored evaluation's stream. For the skeleton it is the stream declaration accepted for the second reports module; the third module's build record binds that declaration and its source identity before any output, and a later change to it does not silently change this report's stream. One draw matrix serves every summary of an arm, object and level; it is generated from the key alone and needs no fit, so it exists for T0 as for any arm.

**When the draws are made (L2 round 1, D1).** For complete valid inputs, the 1,000 draws are made for every summary that applies to the arm, object and level under the coverage table, **whether or not its observed value exists**. In particular the edge-cell summaries of every non-T0 realization level are assessed on all 1,000 draws even when the observed region is empty or full and even when the matching closure is unavailable: a draw can have an edge where the observed map has none. The absence of an observed edge, an observed region or an observed value is never a reason to skip the draws.

**Fixed dependencies.** Some things a summary needs do not change from draw to draw, and two of them can be scientifically unavailable: the closure map (with its own geometry and fit) and κ̂_c,T0. Where one of these is unavailable the summary is blocked on every draw, and its record says **"not assessed on the draws", with the fixed cause**, which is kept distinct from "assessed on 1,000 draws, defined on none". A blocked summary does not stop the draws for the others.

On each draw the lattice mean is re-formed, and, **where the summary needs them**, its smoothed map, region, edge and edge cells. The m field, the terrain and spectral quantities and the closure map are fixed. No contour-family fit is made on a draw for these summaries, and none is added to the evaluator's: where the placed evaluator did not resample a level, item (iv) has no draw labels and none are created here.

**What gets a range.** The numeric scalars: Point 2's six numbers per side; Point 3's two contrasts per side; Point 5's three per set, and the two regional cell counts (zero included); Point 7's S and its two global terms. For each: the observed value, the 1,000 attempts, the number of draws on which it is defined, the causes of the others with their counts, and the 2.5 and 97.5 percentiles over the defined draws.

- Definition is assessed on each draw on its own. An unavailable observed value can stand beside a range from the draws on which the statistic exists; the range is no substitute for the observed value.
- No draw is replaced, imputed or dropped for convenience. No defined draw gives no range (never a zero-width one). There is no minimum count; a small count is shown.
- The ranges are **conditional empirical ranges**. They are not confidence intervals, not simultaneous bands, and the scored 950-of-1,000 rule is not an acceptance rule here.

**What does not.** Identifiers, causes, flags, the location of a maximum, and component lists. Components split, merge and renumber between draws and the contract gives no correspondence between them, so the per-component terms of S are reported for the observed map only.

**λ* keeps its own recipe (constraint 6).** Where the evaluator's draws give index Y a compatible range [L_Y, U_Y] with its count, and the closure label c_Y = λ*_closure,Y exists, the fitted-level difference's uncertainty is that range shifted, [L_Y − c_Y, U_Y − c_Y], with the same count. It can exist where the observed difference d_Y does not (compatible draws beside an observed map without λ*). It is never a percentile range.

## Point 9 — unavailable states, per field

The rows about geometry describe the **observed** value. Whether a summary is assessed on the draws follows Point 8, independently: an observed value that is unavailable for want of an edge can stand beside a range.

| Condition | Consequence |
|---|---|
| The matching closure did not converge | The residual statistics of Point 5, and Points 6 and 7, are `comparator unavailable` for that arm, object and level, as measured there. Points 1 to 4 and the lattice λ* remain |
| κ̂_c,T0 unavailable | Only the contrast against it is `reference unavailable`. The contrast against 1 and everything else remain |
| Lattice region empty or full | No Points 1 to 3, no S (`no edge at θ`). Whole-lattice Point 5 remains; the one non-empty subset remains |
| Lattice edge exists and is under-resolved | Flagged. Points 1 to 3 remain (Point 4). Regional Point 5 remains. S unavailable with the lattice-side cause |
| Closure edge absent or under-resolved | S unavailable with the closure-side cause. Point 5 remains |
| A fit absent or outside ε | That λ* and the fitted-level difference unavailable. S remains |
| Observed geometry available, final evaluator label unstable, unresolved or adverse | Defined fidelity values and ranges remain; the scored status is shown separately |
| A scalar assessed on the draws and defined on none | No percentile endpoints; counts and causes kept; the observed value kept if it exists |
| A scalar blocked on every draw by a fixed dependency | "Not assessed on the draws", with the fixed cause; distinct from the row above |
| Closure unavailable | The regional cell counts of Point 5 remain, with their ranges (they are lattice fields) |
| An edge item on T0 | `not applicable` (§4.3) |
| A required input missing or corrupt, or a computation fault | An apparatus failure, kept as one; never recast as a scientific unavailable state |

Where several dependencies fail, each applicable cause is kept. An unavailable comparator is not an omitted record: an omitted mandatory record prevents a claim of complete reporting (§5.7).

## Point 10 — items (i) and (iv)

No new calculation. (i) is the placed `closure.threshold_fidelity`; its assembly keeps the profile, brackets and absent-endpoint causes beside the shifts, and its uncertainty is §5.4's. (iv) is the placed evaluator's point λ*, typed draws and compatible-draw range; its assembly keeps these apart: a point without λ* beside draws that have one; a final label that is adverse, unresolved or unstable beside compatible draws; a level that was not resampled against one resampled with no compatible draw; the least S among the contours examined when none is within ε, which need not be the family minimum and is not λ*.

## Consequences

- **Nothing placed changes.** These summaries are built as a third reports module, after this record is accepted, through its own L2 rounds.
- **Left to that build's declarations** (ratified with the governance record, not interpretations): field names and encoding; the order of floating-point accumulation in the 3×3 mean of p* and in the summaries; the interpolation rule for the new spatial quantiles and for the new percentile ranges; the tie rule for the location of a maximum; the encoding of causes; the stream-key and source-identity bindings; what is computed once and reused. **Their bounds:** the interpolation already fixed for the 0.95 quantiles inside S (§5.5 step 6) is not reopened; the encoding of causes implements the dependencies ruled here and may add detail, and it replaces no cause the contract names and recasts no apparatus failure; a build declaration cannot choose another availability domain or another uncertainty target.
- **A dependency.** The skeleton stream named in Point 8 is declared in the second reports module, which is in review and not placed. This record binds no particular bytes of it: the third module's build record binds the accepted declaration and its source identity before output (Point 8). The same holds for the evaluator, whose cause precedence was repaired on 2026-11-23 in a separate cycle: the build uses the placed, accepted identities of its day, not the reference copies of any review packet.
- **Cost is not a reason** to use fewer draws, survivor-only skeleton means, frozen edge membership or fewer levels. None of these summaries needs an additional contour-family search per draw; the evaluator's own step-9 work, where it applies, stands as it is. Nothing here is a timing result.
- **Each assembled record carries every binding §5.9 requires that exists at its stage,** among them the map and closure identities, the raw-index and normalization identities, object and floor, arm and level, the seed and resample streams, the summary schema, θ, ε, m, the evaluator identity, and the qualification protocol and result identities once they exist. This list is not a replacement for §5.9.
- The fidelity tier is "pre-registered in full" (§1.2′). Once this record is accepted, another reading of any point is a change to the instrument and is not open to a build after output exists.

*Drafted by L1, 2026-11-23, from L2's consultation advice and Mike's ruling of the same day; draft 2, 2026-11-24, after L2's round-1 review and Mike's word on the closure fit. Points 1, 3 (the fixed reference), 4, 5 (rebuilding the region), 7 (both maps under step 4; no component ranges), 8 and 9 follow L2's advice where it differed from or sharpened L1's proposal. Draft 1's sentence on when the draws are made was L1's and was ambiguous; Point 8 replaces it.*
