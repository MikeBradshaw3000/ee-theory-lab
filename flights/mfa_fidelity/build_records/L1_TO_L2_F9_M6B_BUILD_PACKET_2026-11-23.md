# L1 → L2 — Flight 9 M6 part 2 build review, round 1: the evaluator-derived and assembled reports (§1.3 a, d design side, f, g, h)

**Date:** 2026-11-23. **Register:** module build review (receipt first). Not a run authorization. The module holds no master, runs no dynamics, reads no run record and was computed against no output of the rule, probe or otherwise.
**Repository pin:** `ee-theory-lab` `main` at `c6c21c497366d3ca71e0487127c774aacfd14ba1` (the M6 part 1 placement), checked against the remote before this packet was built. Nothing of part 2 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Contract:** `FLIGHT_9_CONTRACT_v0_7.md`, FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`.
**Decision authority:** Mike. Built at his word "build m6 part 2", after he accepted four recommendations of L1's (§2 below).

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: NOT SOUND` (no bold, no backticks, nothing after it).

## 1. What this module is

One new source file and one test file. **No placed file is edited; in particular `evaluator.py` is untouched** and the test file pins its identity with the thirteen other placed `f9` sources.

| File | SHA-256 | What it holds |
|---|---|---|
| `mfa_instrument/f9/evaluator_reports.py` | `7978581182a64f77682facdc573c55ea2356077d6d6bddb935cbac5d13d1e393` | The evaluator's full output at θ = 0.10 and 0.30 (§1.3 f); the skeleton's boundary (§1.3 g); component coverage (§1.3 h); design-side margins (§1.3 d, §3.2); the persistence diagnostic assembled over the fifteen arms (§1.3 a). Declaration digest `f3fe3fcf1954bb6addd18e94a793593490fef18cb77910f94dda1c25b799337e` |
| `tests/test_f9_m6b.py` (13 tests) | `697d4e2a7425af6badb2170a36ddb6b4ed600be807c8820ed64f7265ff9ad53e` | |

Everything in it is reported only. A level's scored record is the placed `evaluator.evaluate_level`, and nothing here produces, replaces or alters it.

**Not in this module:** the fidelity items of §1.2′ (ii) and (iii) with their uncertainties (§5.7 row 4): local m on the observed edge, and occupancy and edges against the closure's map. The contract names them and does not fix which cells are "on the edge" or which summary is reported. Mike accepted L1's recommendation to take those to you as a readings consultation before any code, and to build them as a third module. That consultation is a separate document; it is not part of this review.

## 2. The four decisions Mike took before the build (2026-11-23: "I accept all of your recommendations")

1. **How θ = 0.10 and 0.30 are reached: a wrapper, not an edit.** The placed evaluator holds θ = 0.20 in one function, `occupied_region`; nothing after it takes θ. L1 put three options: (A) re-write the two orchestration functions in the new module with θ as an argument, calling the placed building blocks unchanged, with a test that at θ = 0.20 the copy returns the placed record field for field; (B) change the registered constant at run time around a call to the placed evaluator; (C) edit the placed evaluator to take θ. Mike accepted A. B could leave a scored evaluation running at the wrong θ; C touches cleared, scored bytes.
2. **Resamples at the reported thresholds:** the scored evaluation's declared stream for the same arm and level, so the three thresholds are evaluated on the same 1,000 resampled maps.
3. **"The §5.5 rule" for the skeleton's boundary** is the whole of it, steps 1 to 9, at θ = 0.20.
4. **The split** described under "Not in this module".

These are recorded as Mike's acceptance of L1's recommendations, for ratification with the governance record. Say if you think any of them is not open to a build declaration.

## 3. Declarations (for Mike's ratification with the governance record; your disposition on each)

| # | Declaration |
|---|---|
| M6B-1 | **The criterion at θ.** `occupied_region_at` is `box_sum · 10⁶ ≥ θ_micro · 9 · n_seeds · tail`, the placed criterion with θ as an argument. θ is accepted only as the integer 100,000, 200,000 or 300,000; 200,000 exists for the equality test and is never the scored path. |
| M6B-2 | **The orchestration copies.** `evaluate_map_at` and `evaluate_level_at` are the placed `evaluate_map` and `evaluate_level` with θ threaded through and the constructed-resamples argument removed. They call the placed `box_sum`, `geometry.edge`, `step4`, `_Traced`, `fit`, `resample_multiplicities`, `result_from_counts`, `check_counts`, `_check_families`, `stream_key` unchanged. The step-4 minimums, ε, m, the family, the pruning and the result table are the registered ones at every θ. |
| M6B-3 | **Reported thresholds.** `reported_thresholds(counts, families, key)` returns the two records keyed by θ in micro-units, with `key` the scored evaluation's (`evaluator.arm_level_key`). |
| M6B-4 | **Skeleton boundary.** `skeleton_boundary(counts, families, key)` is the placed `evaluate_level` on the 40 skeleton maps (an extinct run's map is its recorded tail). Its key must be a skeleton key: `skeleton_level_key` = the arm-and-level key with the skeleton's object code (1) appended, validated as a declared skeleton run (`all_active`). A realization key is refused. |
| M6B-5 | **Component coverage** is computed from the level's maps by the placed steps 1 to 7 on the observed map; no evaluation record is accepted. Per index: every component of the observed edge and of the contour the fit reports, each with bonds, resolved (≥ 40 bonds), and the 0.95 quantile of its bonds' distances to the whole opposite edge (the placed `q95` on the placed distance grid). |
| M6B-6 | **Design-side margins** for the four TD variants from the stored base v and `terrain.td_core`: core cells, perimeter, components; band = cells with 0.1 < (v − 0.3)/0.6 < 0.9, split inside and outside the core; band/core exact; largest base step between 4-neighbours. §3.2's table (perimeter, band cells, band/core and step to three places) is in the declaration and asserted on every call, with the core checked against the base's upper half. These are sanity checks and authenticate nothing; the runner binds v to the bundle. |
| M6B-7 | **Persistence report.** For the fifteen arms, the placed `outcomes.persistence_record` computed from survivor counts; no persistence record is accepted. An absent arm is listed as missing and an arm with a missing level is listed; `complete` is true only with neither. |
| M6B-8 | **Records.** The evaluation records are the placed evaluator's and carry its numpy arrays; the others are plain data. Each report has `"kind": "reported only; never scored"` and the declaration digest. They are components of the eventual §5.9 records; the persisted encoding is the runner's. |
| M6B-9 | **Seven readings**, listed in the module docstring and in §4. |

## 4. The readings (M6B-9). Say for each whether it is acceptable as a build declaration or is a ruling for Mike

1. θ = 0.10 and 0.30 use the scored evaluation's resample stream (Mike, decision 2).
2. The skeleton's boundary is steps 1 to 9 (Mike, decision 3). Its compatible, adverse or unresolved word describes the skeleton map and is not B.
3. **The skeleton's resample stream is its own:** the arm-and-level key with the skeleton's object code appended. The contract names no stream for it. The alternative is to reuse the realization key of the same arm and level.
4. **Component coverage gives every component its quantile, resolved or not.** §1.3 (h) says "each one's 95th-percentile distance" after "how many are resolved". A resolved component's value is the term the evaluator used (tested equal); an unresolved one's entered no decision.
5. **Component coverage uses the contour the fit reports:** the minimizing contour when Δ ≤ ε; otherwise the least-S contour among those examined, labelled as §5.5 step 7 labels it. With no contour examined, an empty family or a level that is not informative, the observed side's counts are reported and the rest carries its cause.
6. **The design-side band is strict at both ends,** as `arith/td_final.py` computed it. On the four declared bases no cell is within 1e-4 of either limit (in S), so strict and inclusive give the same counts; the mutation record shows it.
7. **The persistence report covers the fifteen arms of §8** (T0 under P only) and the high-initialization skeleton sweep. T0's low sweep belongs to T0's own record (§5.8).

## 5. Disclosures

1. **The orchestration is duplicated.** About sixty lines of `evaluate_map` and `evaluate_level` exist twice. If the placed evaluator is ever touched, the copy must be touched with it; the equality test at θ = 0.20 fails if they drift. That is the cost of decision 1.
2. **The module calls three private names of the placed evaluator** (`_Traced`, `_cells`, `_check_families`). They are pinned by the evaluator's identity in the test file.
3. **How the wrapper is tested at 0.10 and 0.30: the placed evaluator is the oracle.** On integers, B(c) ≥ 36,000 ⇔ B(2c) ≥ 72,000, and B(3k) ≥ 108,000 ⇔ B(2k) ≥ 72,000, for the observed map and for every resampled map alike. So θ = 0.10 on 3k must equal, field for field, the placed θ = 0.20 on 6k, and θ = 0.30 on 3k the placed θ = 0.20 on 2k (same key, so the same resamples). The test does this on one constructed TA level (counts k ≤ 166) where all three regions are informative and different, including every typed draw, Δ and level index. It covers one family structure at the reported thresholds; the θ = 0.20 equality is also run on TB's two families and on four unavailable states.
4. **No lattice run is made in the tests** and L1 has computed none of these reports on output of the rule; every map is constructed. Nothing here checks the path from a run record to a report.
5. **Cost, measured on constructed maps in L1's container.** One level evaluation took 13 to 16 s where the resampled edges are stable. A constructed skeleton map with ten of forty seeds extinct took about 250 s per evaluation (499 s for two), because the resampled edges move and the contour cache misses. The reported thresholds add two evaluations per realization level and the skeleton boundary one per skeleton level; near a skeleton's threshold the second kind may be the slow kind. These are costs for the runner's budget, not properties of the rule.
6. **The module does not know what it is given**: which arm's maps, which object, which bundle. `skeleton_boundary` checks only that its key has the skeleton form. Binding is the runner's.
7. **Mutation check.** `build_records/f9_m6b_mutation_check.py` applies 25 single-fragment mutations; because the evaluator tests take minutes, each mutation is run against the tests that bear on it (named in the output). 24 are caught. The one that is not is reading 6's equivalence (an inclusive band gives the same counts on the four declared bases).

## 6. Evidence

- `build_records/f9_m6b_module_container_2026-11-23.txt` (`7140166e35a84a918e7b518ef1709098d48223552a6ce00a785386cba7646104`) — **13 passed in 282.90 s** in L1's container (Python 3.13.18, numpy 2.5.3). The three runs of this section shared a two-core machine, so the times are longer than a run alone: the module alone took 182.83 s on an earlier pass with one test fewer.
- `build_records/f9_m1_to_m6b_container_2026-11-23.txt` (`6f9612a7c6ee7d873b5880f5ed8619797e03f96b3819f39318ac0f5d8c27daf6`) — the seven Flight 9 test files in one process: **289 passed in 1112.30 s (276 from the six placed files, 13 from this module)**.
- `build_records/f9_m6b_mutation_check_2026-11-23.txt` (`fddced58f349e62a775cbd829a3ffae670c9055961bb516b8281b1847902631f`) with its script (`6b9d64e25b73ba5aee2ab5aa6648dddab341817cc5208f64c288d42cb5aa9d9e`).
- To run: from `flights/mfa_fidelity/instrument`, `python -B -m pytest tests/test_f9_m6b.py -v -p no:cacheprovider`. It needs no identity bundle. Three tests take most of the time (the TA fixture, the TB case, the skeleton case). If the whole file exceeds your window, say which tests you ran; `-k "criterion or coverage or forty or design or persistence or declaration or one_way or byte_unchanged"` runs the fast ones in under 5 s.

## 7. Questions

**Q1.** The wrapper (M6B-1, M6B-2): compare `evaluate_map_at` and `evaluate_level_at` with the placed `evaluate_map` and `evaluate_level` line by line. Is there any difference other than θ and the removed constructed-resamples argument? Can you construct seed maps for which the wrapper at θ = 0.20 and the placed evaluator differ in any field?
**Q2.** Is the scaling oracle of disclosure 3 valid as stated (for the observed map and every resampled map)? Does it leave a part of the wrapper at 0.10 or 0.30 unexercised that a different construction would reach?
**Q3.** Is there any way a call into this module can change what the scored path computes: the registered θ, a family's cache in a way that changes a result, the stream?
**Q4.** Skeleton boundary (M6B-4; readings 2 and 3): is the record §1.3 (g)'s? Is a separate stream the right declaration, or should it be the realization key's?
**Q5.** Component coverage (M6B-5; readings 4 and 5): is this §1.3 (h)'s content? Is recomputing from the maps, and not from the scored record, right? Is anything §1.3 (h) asks for missing?
**Q6.** Design-side margins (M6B-6; reading 6): are the definitions §3.2's? Is asserting the contract's table on every call acceptable?
**Q7.** Persistence report (M6B-7; reading 7): is anything §1.3 (a) or §5.4 requires missing from the assembled record?
**Q8.** Declarations M6B-1 to M6B-9 and the seven readings: for each, ACCEPTABLE, REQUIRES CHANGE (say what), or REJECT; and for each reading, build declaration or ruling for Mike.
**Q9.** Coverage: with part 1 placed and this module, which mandatory item of §1.3 or §5.7 is still unowned, other than the §1.2′ (ii) and (iii) items deferred to the third module?
**Q10.** Anything else.
