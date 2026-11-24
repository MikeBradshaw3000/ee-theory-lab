# L1 → L2 — Flight 9 consultation: the fidelity summaries of §1.2′ (ii) and (iii), before any code

**Date:** 2026-11-23. **Register:** consultation on readings, at Mike's word. Not a build review, not a verdict request, not a run authorization. No code for these items exists and none will be written until Mike has ruled on what you and L1 put to him.
**Contract:** `FLIGHT_9_CONTRACT_v0_7.md`, FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`. Nothing here changes it. Whatever Mike rules is recorded beside it as readings for the governance record.
**Why now.** No Flight 9 job has been run and no master has been drawn. Each summary below is a choice that could otherwise be made after seeing output. L1 has not opened the probe arrays and has computed nothing of this kind on any output of the rule.

## 1. What the contract fixes and what it leaves open

§1.2′ pre-registers the fidelity tier "in full" and §5.7 row 4 gives the uncertainty recipes:

- (ii) "Local m_i = g·λ_i·Δt/q on the observed edge, against 1 (a local homogeneous benchmark) and against κ̂_c,T0; neither is a pointwise prediction."
- (iii) "Seed-mean occupancy against the site closure's fixed-point probabilities (§4.2), matched in object and floor; where edges are compared, the §5.5 rule is applied to both maps."
- §5.7 row 4: "Occupancy-based items: 2.5–97.5 percentile range over 1,000 seed resamples."

Fixed: the quantities (m_i; p̄ against the closure's p*), the comparators (1; κ̂_c,T0; the matched closure), the rule for edges (§5.5), the resample count and the percentile range.

Not fixed, as L1 reads it:

| # | Open point |
|---|---|
| A | Which cells are "on the observed edge". An edge is a set of bonds, each between a cell of the region and a 4-neighbour outside it. |
| B | What is reported of m over those cells: every value, or a summary, and which. |
| C | What "against 1" and "against κ̂_c,T0" are as numbers. |
| D | What is reported of p̄ − p* over the lattice: which summary. |
| E | How the §5.5 rule is applied to the closure's map, which is one float map and has no seeds. |
| F | What "edges are compared" yields: which discrepancy, and between what. |
| G | Which maps and levels these items cover, and what the 1,000 resamples are applied to. |
| H | What is recorded when a piece is unavailable. |

## 2. L1's proposals (each is a proposal; none is built)

**A. Edge cells.** The inside edge cells are the distinct cells of the region that have a bond of E; the outside edge cells are the distinct cells outside the region that have a bond of E. Both sets are reported, separately. A cell is counted once however many bonds it has.

**B. Summary of m.** For each of the two sets: the number of cells, and the minimum, 0.25, 0.50, 0.75 quantiles and maximum of m_i over the set (linear interpolation between order statistics). m_i = κ·λ_i/ρ(Λ) with the arm's own raw index λ and spectral radius, which is g·λ_i·Δt/q exactly as the instrument defines g. No per-cell list is persisted in the report (the map and the index are in the bundle and the run records).

**C. Against the benchmarks.** The median of each set minus 1, and minus κ̂_c,T0 expressed as a κ value (micro-units divided by 10⁶). Where κ̂_c,T0 is unavailable the second is `reference unavailable`. Both are labelled as §1.2′ labels them: not a pointwise prediction.

**D. Occupancy against the closure.** On the unsmoothed seed-mean map p̄ and the closure's converged map p* for the same arm, level, object and floor: the mean of p̄ − p*, the root mean square of p̄ − p*, and the largest |p̄ − p*| with its cell. Also the same three restricted to the cells of the observed region and to its complement, when the level has a region. With the note the contract already gives: a finite-tail mean against a fixed point, not an isolated closure error.

**E. The §5.5 rule on the closure's map.** Steps 1 to 8 with the closure's p* in place of p̄: the 3×3 periodic mean of p*, the region {p̃* ≥ 0.20}, its edge and components, the step-4 minimums, and the fit to the arm's registered families. Step 9 does not apply (there are no seeds); the record says so. The threshold is decided on floats, since p* is a float map. L1 would report beside the region the number of cells whose p̃* lies within 1e-9 of θ, so that a decision resting on a rounding is visible; that count gates nothing.

**F. Edges compared.** When both the lattice map and the closure map are informative at a level: the joint discrepancy S of §5.5 step 6 between the lattice edge and the closure edge (its two global terms and its per-resolved-component terms), and whether S ≤ ε, labelled as fidelity. Beside it, each edge's own fitted level λ* where it has one, and their difference. No word of the scored vocabulary (compatible, adverse) is used for it.

**G. Coverage and resamples.**
- Realization: every arm and level, items (ii) and (iii), with the realization closure (η₀ floor, start π₁).
- Skeleton: item (iii) only, every arm and level, with the skeleton closure (no floor, start 1) against the unconditional 40-seed mean. Item (ii) is not computed for the skeleton (§1.2′ (ii) speaks of "the observed edge", which §1.2″ defines in the realization).
- Resamples: the scored evaluation's declared stream for the arm and level (for the skeleton, the skeleton stream of M6 part 2). On each resample the lattice map is re-formed; the closure map does not change. For every summary of B, C, D and F the report gives the observed value and the 2.5 and 97.5 percentiles over the resamples on which it is defined, with the number of such resamples. A resample with no informative edge contributes to D and not to B, C or F.

**H. Unavailable states.** Closure not converged: every item that needs p* is `comparator unavailable` for that arm, object and level, as measured there. No informative lattice edge: B, C and F carry the evaluator's cause; D is still reported. Closure map without an informative edge: F carries that cause. κ̂_c,T0 absent: `reference unavailable`.

## 3. What L1 asks of you

For each of A to H:

1. Is the point open in the frozen text, or does the contract already fix it (say where)?
2. Is L1's proposal a sound reading? If not, what would you put in its place, and why?
3. Is there a reading you consider equally supported that would give a materially different report? Mike should see it.

And three further questions:

4. **Is anything in §1.2′ or §5.7 row 4 not covered by A to H?** In particular (i) and (iv): L1 takes (i) as done by the placed `closure.threshold_fidelity` and (iv) as done by the evaluator's `lambda_star` and `lambda_star_range`, with assembly only remaining.
5. **Cost.** F and the resampled summaries need the evaluator's steps on 1,000 resampled maps per level and object. One evaluation of that size took 13 to 16 s on constructed maps in L1's container, and about 250 s on a constructed map with ten of forty seeds extinct. Is there a part of G you consider not required by "occupancy-based items: 2.5–97.5 percentile range over 1,000 seed resamples", so that it should not be computed?
6. **Is any of this a matter for an interpretation record beside the contract** (as Interpretation 001 was), and not for build declarations ratified with the governance record?

Please return your advice as one `.md` upload. No verdict line is needed. Mike rules; L1 builds only what he rules.
