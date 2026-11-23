# L1 → L2 — Flight 9 M6 build review, round 1: the map-statistic reports (§5.7 rows 1 to 3; §1.3 b, c, d, e)

**Date:** 2026-11-23. **Register:** module build review (receipt first). Not a run authorization. M6 holds no master, runs no dynamics, reads no run record and was computed against no output of the rule, probe or otherwise.
**Repository pin:** `ee-theory-lab` `main` at `67aa10ca5958e0c07855441fbeab4a71a66e51f5` (the governance records placement), checked against the remote before this packet was built. Nothing of M6 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Contract:** `FLIGHT_9_CONTRACT_v0_7.md`, FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`.
**Decision authority:** Mike. Built at his word "build m6".

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: NOT SOUND` (no bold, no backticks, nothing after it).

## 1. What M6 is, and what it is not

One new source file and one test file. No placed file is edited.

| File | SHA-256 | What it holds |
|---|---|---|
| `mfa_instrument/f9/reports.py` | `6e886549559b8ec2724c3a1539f07d8198f712285d31043f3850f17c9c02b146` | Contour constancy, measured margins, flicker distributions, TC's suppression contrast. Declaration digest `56bc9a108afdc347bcdae98f254de7f3072e091a46d607ed40a118ae887945d2` |
| `tests/test_f9_m6.py` (22 tests) | `b4cae42d19f29d1ec8728d13a2d69cff4428ff005df10aac4a30d33bf52da8c5` | |

Everything in it is reported only. Nothing is scored, enters B or D, or gates anything.

**L1 split §5.7 and built the first part. This is L1's choice of boundary and is for your comment (Q7).** This packet has the reports that are statistics of a level's maps and need nothing from the evaluator beyond its integer box sum. Deferred to a second reports module, not built:

- the evaluator's full output at θ = 0.10 and 0.30 (§1.3 f);
- the skeleton boundary under §5.5's rule on the unconditional seed-mean map (§1.3 g; §5.7 row 5);
- component coverage (§1.3 h; §5.7 row 6);
- the fidelity uncertainties of §5.7 row 4: local m on the observed edge, occupancy against the closure's map, the range of λ* over compatible resamples;
- the assembly of the persistence report.

The reason for the split: those five need the evaluator at thresholds other than 0.20 or on other maps, and the placed `evaluator.occupied_region` holds θ = 0.20 as a constant. The second module has to reach the evaluator's steps at another θ without editing cleared bytes, and that deserves its own review. The four reports here do not touch that question.

## 2. Declarations (for Mike's ratification with the governance record; your disposition on each)

| # | Declaration |
|---|---|
| M6-1 | **Inputs.** A level's 40 seed maps as integer tail counts (0..1,000), checked by the placed `evaluator.check_counts`. For flicker, the §2.11 record of the same 40 runs at each W, stacked: `{W: {"A", "R0": integer (40, L, L); "first", "last": bool}}`. For constancy, the arm's comparison array ω. For TC, TC's stored base u. The module reads no run record and takes no arm, level, object or master: binding the arrays to runs and to the bundle is the runner's. |
| M6-2 | **Occupancy on integers.** t_i = Σ_s counts; p̄_i = t_i/40,000; p̃_i = B_i/360,000 with B the placed `evaluator.box_sum` of t. Every count, band and cut is decided by integer comparison (`x·10⁶ ≥ micro·denominator`). Ties go up: p̃ = 0.30 exactly is core, p̄ = 0.10 exactly is in [0.10, 0.20). |
| M6-3 | **Constancy bins** as §5.7 row 1 states them: sort by ω, ties by flat index; whole tie blocks are added until the bin holds at least 100 cells; a final bin under 100 is merged into the one before. Reported per bin: cell count, least and greatest ω. |
| M6-4 | **Constancy variances are exact rationals.** ‖Px‖² = Σ_bins [Σx² − (Σx)²/n_b] on integers; V_within from t, V_noise from 40·counts_s − t, with the divisors 40,000²·N and 40,000²·40·39·N. Each is reported as a float (one correctly rounded conversion) and as numerator/denominator. `V_noise_is_zero` is the exact test. No ratio is formed anywhere. V_within − V_noise can be negative and is reported as it is. |
| M6-5 | **Margins.** Core = #{p̃ ≥ 0.30}, band = #{0.10 ≤ p̃ < 0.30}, band/core exact, `"undefined"` when the core is empty. The floor reference is carried as the literal `0.0523` with π₁ from the placed `dynamics.stationary_pi1` beside it. |
| M6-6 | **Flicker record checks.** Before any statistic the stacked record is refused unless every (cell, seed) satisfies the relations the placed parser requires of a run: 0 ≤ A ≤ n; 0 ≤ R₀ ≤ n − A; R₀ = 0 iff A = n; with R_a = R₀ − 1 + first + last, 0 ≤ R_a ≤ A and R_a = 0 iff A = 0. Bounds are tested in the input's own integer type before conversion. |
| M6-7 | **Flicker statistic.** Bands by p̄ computed from the W = 1 record (its A is the tail count). Per record: W·(n − A)/R₀ as one float division of integers; undefined iff R₀ = 0; possibly censored iff the first or the last window is inactive. Per band and W: records, defined, undefined, possibly censored, q25, median, q75. |
| M6-8 | **TC's sets.** bump = (0.9 − u)/0.85 from TC's stored u; inside = bump ≥ 0.5; outside = bump ≤ 0.05. The sizes 545 and 7,843 are constants of the declaration and are asserted on every call, so any other array is refused. Means are exact; the ratio is `"undefined"` when the outside mean is 0. |
| M6-9 | **Seven readings**, listed in `reports.py`'s docstring under "READINGS THIS MODULE MAKES" and in §3 below. |
| M6-10 | **Records** are plain data (str, int, float, bool, list, dict), each with `"kind": "reported only; never scored"` and the declaration digest, and none with a result, tier or cause field. |

## 3. The readings (M6-9). Say for each whether it is acceptable as a build declaration or is a ruling for Mike

1. **"Also the counts at the cut 0.20"** (§5.7 row 2). Read as the same pair with 0.20 in place of 0.30: #{p̃ ≥ 0.20} and #{0.10 ≤ p̃ < 0.20}, with their ratio. Another reading is a single count #{p̃ ≥ 0.20}; the record contains it either way.
2. **"The median and quartiles"** (§5.7 row 3). The 0.25, 0.50 and 0.75 quantiles with linear interpolation between order statistics, the convention §5.5 step 6 names for Q₀.₉₅. §5.7 names no convention.
3. **"Possibly censored records"** are counted among all records of the band. An all-active record has no inactive segment and both ends active, so it is never censored; counting among defined records gives the same number (the mutation record shows the two are indistinguishable).
4. **Possibly censored records are included in the median and quartiles.** §5.7 says "over all (cell, seed) records with a defined value" and does not exclude them.
5. **An empty band, or one with no defined record,** reports its counts and `None` for the three quantiles.
6. **Tie blocks are bit-equal values of ω as M1 stores it** (rounded to 12 places). No tolerance is applied.
7. **TC's contrast and §8.** §1.3 (e) says "per arm and level"; the pre-probe declaration's R-6 says "(realization)". §8 step 15 names six report jobs and none is named for (e). M6 computes the contrast on whatever maps it is given; the object and the job are left to the runner. If you think the contract fixes either, say which.

One addition beyond the contract's list: each bin's cell count is reported beside its ω range.

## 4. Disclosures

1. **No lattice run is made in the tests, and L1 has computed none of these reports on output of the rule.** The binding on probe output is read to cover constancy in particular (it is a computation against λ contours). Every map and flicker record in the tests is constructed. The consequence: nothing in M6 checks the path from a run record to a report. That path is the runner's and qualification's.
2. **The flicker statistic is checked through the placed parser.** Forty constructed runs of 1,000 ticks (two-state chains per cell, plus always-active and never-active rows) are fed through the placed `dynamics._Windows`; for 1,512 sampled (cell, seed, W) records (504 at each W) the record equals a direct reading of the tick sequence and W·(n − A)/R₀ equals the mean length in ticks of the observed inactive segments, as exact rationals.
3. **The second implementations in the test file are L1's**: a cell-by-cell binning loop, a float and a value-by-value rational version of the variances, a rational margins count on a padded box sum, a record-by-record flicker reference with numpy's quantile, and TC's bump from the contract's formula. They share L1's reading of §5.7 by construction and cannot find a misreading.
4. **Mutation check.** `build_records/f9_m6_mutation_check.py` applies 23 single-fragment mutations to `reports.py`; the test file fails on 22. The one it passes is reading 3's equivalence. The script is L1's and is evidence about the tests only.
5. **One statistical test.** `test_v_noise_estimates_the_seed_noise_of_the_mean` asserts V_noise within 2% of its expectation and |V_within − V_noise| within 10% of it for binomial seeds about a profile constant within bins. It uses a fixed generator and is deterministic; the tolerances are L1's.
6. **Floats.** The variances' floats come from exact rationals and are platform-independent. The flicker quantiles are IEEE divisions, a sort and one interpolation, with no libm call. L1 expects identical values across machines and has measured that on the container only.
7. **The module does not know what it is given.** A caller can pass the maps of one arm with the comparison array of another, or skeleton maps to the suppression contrast. Only TC's u is checked (by set sizes). M6-1 puts this on the runner.

## 5. Evidence

- `build_records/f9_m6_module_container_2026-11-23.txt` (`5f75f11ce965001dfccf8bbb0774dc562a62d1e98a302ef8182e1f7778d5a607`) — **22 passed in 6.05 s** in L1's container (Python 3.13.18, numpy 2.5.3).
- `build_records/f9_m1_to_m6_container_2026-11-23.txt` (`75df38495df48377d1975e138a4ebab5e3686c96a1b0c2f8225732936310f767`) — the six Flight 9 test files in one process: **272 passed in 790.31 s (250 from the five placed files, 22 from M6)**.
- `build_records/f9_m6_mutation_check_2026-11-23.txt` (`0aa0e268cd656ce816a63757c17a07f456b4f8a399d25d3c6738d835f7947771`) with its script (`9eef3e2d968a80830c62491572f2229ba707dc0db0241dace9814d631842e55c`).
- To run: from `flights/mfa_fidelity/instrument`, `python -B -m pytest tests/test_f9_m6.py -v -p no:cacheprovider`. It needs no identity bundle and takes seconds.

## 6. Questions

**Q1.** Constancy: is the binning §5.7 row 1's, including the merge? Are V_within and V_noise the contract's formulas (M6-3, M6-4)? Can you construct integer maps and an ω for which the reported exact value differs from the formula evaluated in exact arithmetic?
**Q2.** Margins and bands: can you construct maps for which a count differs from the contract's inequality evaluated exactly, at or near a cut (M6-2, M6-5)?
**Q3.** Flicker: are the record checks (M6-6) exactly the placed parser's relations, neither more nor fewer? Can you construct a stacked record that is accepted and impossible, or refused and possible? Is the statistic §2.11's?
**Q4.** TC: are the two sets the pre-probe declaration's (R-6) and the probe script's `tc_bump` sets? Is deriving bump from the stored u, with the sizes asserted, acceptable, or should the sets be built from the terrain formula directly?
**Q5.** Declarations M6-1 to M6-10: for each, ACCEPTABLE, REQUIRES CHANGE (say what), or REJECT.
**Q6.** The seven readings of §3 and the addition under them: for each, acceptable as a build declaration, or a ruling for Mike?
**Q7.** The split (§1): is anything deferred that must be in this module, or anything here that should wait for the second? Is there a report in §5.7 or §1.3 that neither list names?
**Q8.** Disclosure 1: is the absence of any run in M6's tests the right side of the binding, or is it more restrictive than the binding requires?
**Q9.** Anything else.
