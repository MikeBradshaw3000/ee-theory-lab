# L1 → L2 — Flight 9 M6 part 2 build review, round 2: response to round 1 (D1, constant-index cause precedence)

**Date:** 2026-11-24. **Register:** module build review, repair round (receipt first). Not a run authorization. The module holds no master, runs no dynamics, reads no run record and was computed against no output of the rule, probe or otherwise.
**Repository pin:** `ee-theory-lab` `main` at `ff136d70b1c6862b52d0cca270e1163c5c0e5a63`, checked against the remote before this packet was built. Nothing of part 2 is committed. Every file in this zip under `flights/` that exists at the pin is a byte copy of it.
**Contract:** `FLIGHT_9_CONTRACT_v0_7.md`, FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`.
**Answers:** your round-1 review, `L2_F9_M6B_ROUND1_REVIEW_2026-11-23_RECEIVED.md` (`31fd32e258482f81d3fc8762271fc4f722ac69d6ae77a73a97b30fb7c58dd78f`, in this zip as committed), of archive `6a00972c7a753d420b6a2e3724b209355e63723051b7067cd6b0e53e3f9ebc19`.
**Decision authority:** Mike. On your round-1 return he ruled: "1. Repair 2. Evaluator repair is its own cycle 3. Defer 2 cause strings".

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: NOT SOUND` (no bold, no backticks, nothing after it).

## 1. What happened since round 1

Your D1 was a defect in two places: the placed evaluator's per-index cause order, and this module's copy of it. They were repaired in two cycles, as Mike ruled.

1. **The placed evaluator, its own cycle (closed).** Packet `f9_evaluator_repair_round1_L2.zip` (`e82a62ed1dacd0d79cfbf72a9f866ae38002791d53d1220253f094e97dcf37f9`); your review of it (`009a86f178f31021d91cd334bf7bf03a9d504e1985d79b2ee6b5f7c351daa944`), SOUND, with your inverse-edit reconstruction of the prior identities. Placed at `7a1094ad3e62d51142712243b9a3be1a89e311ca` after the canonical six-file run on Mike's machine (277 passed in 1060.87 s; `f9_m1_to_m6_canonical_2026-11-24.txt`, `7fa2b96916255d1b5683d5d239e14f1cd9144cf8b89843dbdd70305170bf7edc`). `evaluator.py` is now `ddfa49b11955de42d5b6638d892af4c75756ff6b1b5f35ea0884c4de7b2a07a1` (was `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc`); its declaration digest did not change. That review, the placement note and the diff are in this zip as committed. They are context here and not under review again.
2. **F9 Interpretation 002** (the fidelity summaries of §1.2′ (ii) and (iii)) was placed at `ff136d7` after your two rounds on it. It is in this zip as committed because the module's docstring now cites it; it is not under review here. Its point on the skeleton's resample stream names the declaration of this module (reading 3), which is unchanged from round 1.
3. **This packet** is the second half of D1: the copy, its tests, and the identity pin.

## 2. The files under review

| File | Round 1 | Round 2 |
|---|---|---|
| `instrument/mfa_instrument/f9/evaluator_reports.py` | `7978581182a64f77682facdc573c55ea2356077d6d6bddb935cbac5d13d1e393` | `9c60717553a8419fd248f587845499792e79c73b97f5728f662ab1ca58521606` |
| `instrument/tests/test_f9_m6b.py` | `697d4e2a7425af6badb2170a36ddb6b4ed600be807c8820ed64f7265ff9ad53e` (13 tests) | `e279ca0647519a3dff990a69d3c0cadc4dfbcbf86df560910c35d639d0875463` (14 tests) |
| Declaration digest | `f3fe3fcf1954bb6addd18e94a793593490fef18cb77910f94dda1c25b799337e` | `a9227f81c1b088dfdcd86d625747b3b2c26323cf25c3092cbc4d4e6fe071e979` |

The round-1 bytes of both files and the round-1 packet document are under `packet_only/round1/` (they were never committed). `build_records/f9_m6b_round1_to_round2.diff` (`fa87500ebf6074b530c9387084ee8c4f2717e03930eb354653bfa598b4725116`) is the whole change, made with `diff -u` from those bytes. **Please reconstruct the two round-1 identities from the round-2 bytes by inverting the diff, as you did for the evaluator repair, and say whether anything outside the hunks listed in §3 changed.**

## 3. Every change, by your required-repair item

**Item 1 (the placed evaluator's precedence): done in its own cycle,** §1 point 1.

**Item 2 (synchronize the threshold orchestration; keep the θ = 0.20 equality; the skeleton report keeps calling the placed evaluator).**

- `evaluate_level_at`: the two branches are exchanged. An index whose family is empty gets `no eligible contour` first; only then does a non-informative map give its cause. The point record is built before the loop and is not touched. This is the one executable change in the source.
- `skeleton_boundary` is unchanged: it still calls the placed `evaluator.evaluate_level` on all 40 maps at the registered θ, and now receives the repaired order from it.
- The θ = 0.20 equality tests are kept as they were, and the new test adds equality on the crossed states (below).
- Declaration: one entry added, `("unavailable_precedence", "an empty family first (no eligible contour), then a non-informative map's cause: contract section 7, L2 above L3 and L4")`. Hence the new digest. No other entry changed. This adds to M6B-2's text; M6B-3 and M6B-4 are worded as before and change only in what their records now carry.
- Docstring: a "Cause precedence" paragraph under (f); the (g) sentence about T0 rewritten (round 1's sentence did not say which cause governs when the family is empty and the map has no edge); the "NOT HERE" paragraph now cites Interpretation 002.

**Item 3 (discriminating regressions).** One new test, `test_a_constant_index_outranks_the_maps_state_on_every_route`:

- Maps: your three (empty, full, the `[10:16, 10:16]` patch) and a fourth, a full map with that patch removed (complement under 100 cells).
- Routes, with T0's two empty families: the placed evaluator at 0.20, the copy at 0.20, the skeleton boundary, and both reported thresholds. Every index entry must be exactly `{"result": "not informative", "cause": "no eligible contour", "resampled": False}`.
- The point is asserted to keep describing the map: not informative, with (cells, bonds) (0, 0); (10,000, 0); (64, 32), (60, 32), (52, 32) at θ = 0.10, 0.20, 0.30 for the patch (your table's values); (9,984, 16) for the fourth map.
- Mixed families (P empty, H = TB's 50 contours), through both reported thresholds, the skeleton boundary and the copy at 0.20: P gets `no eligible contour`, H gets the map's cause; and the copy at 0.20 equals the placed evaluator on the same input.
- Non-constant families (TB's two) through both reported thresholds keep the map's cause (`no edge at theta` or `below the informative minimum`).

**Item 4 (identified changed bytes; identity assertions; disclosures).** §2's table; the test's `PLACED` pin for `evaluator.py` is now the repaired identity, with its comment naming `ff136d7` and `7a1094a`. The other thirteen pins are unchanged, as is the digest over the non-`f9` instrument sources.

**Your Q1 note (the wrapper's preflight).** Accepted. Round 1's packet said the copy differs from the placed orchestration only in θ and the removed constructed-resamples argument. It also verifies this module's declaration (and through it the evaluator's, the outcome module's and the stream's) and validates θ before anything else, so what is refused can differ from the placed evaluator; no returned record differs. The module docstring now says so under (f).

## 4. What did not change

Everything else in both files: the criterion at θ, `evaluate_map_at`, `reported_thresholds`, the skeleton key and boundary functions, component coverage, design margins, the persistence report, the seven readings, and the thirteen round-1 tests. Your round-1 dispositions on M6B-1, 5, 6, 7, 8, 9 and on the seven readings are taken as standing unless the diff shows you otherwise.

## 5. Disclosures

1. **The mixed-family case is a constructed input.** On the eight terrains only T0 has an empty family, and there both are empty (family sizes P, H: T0 0, 0; TA 1300, 1300; TB 2600, 50; TC 1180, 1180; TD-1-2 681, 681; TD-1-4 920, 920; TD-4-2 250, 250; TD-4-4 250, 250, computed from the placed sources). So no declared arm has one empty and one non-empty family; the test builds one from T0's P family and TB's H family under a TB key, as you asked, to show each index gets its own cause. As you noted on the evaluator repair, M4's guard refuses a constant-family record that is labelled non-T0, so the outcome module refuses such a record. Nothing here touches that guard.
2. **The duplicated orchestration remains** (round-1 disclosure 1). This round is the first time it cost something: the placed evaluator changed and the copy had to follow. Left alone, the copy would differ from the repaired evaluator on the crossed states, which you found no round-1 test reaches; the new test binds the two there (the mutation record's "round-1 order" line).
3. **Carried by Mike's ruling, not addressed here:** the two cause strings `no edge at theta` and `below the informative minimum` in the placed evaluator ("Defer 2 cause strings"); your three further crossed-state tests for `test_f9_m3.py` (constant family × small complement; × malformed input; constant index beside an unstable sibling), held for the next touch of that file. This module's new test does cover constant family × small complement on its own routes and on the placed evaluator.
4. **Mutation check.** Two mutations added: the round-1 order restored in the copy, and a map with no edge labelled as a constant index. 27 single-fragment mutations, each run against the tests that bear on it: 26 caught. The one that is not is unchanged from round 1, reading 6's equivalence (an inclusive design band gives the same counts on the four declared bases).
5. **No lattice run** is made in the tests; every map is constructed. Costs are as round 1 reported; the new test adds under a second (no resampling occurs on a map that is not informative).
6. Round-1 disclosures 2 to 6 stand unchanged.

## 6. Evidence (L1's container: Python 3.13.18, numpy 2.5.3; two cores, runs overlapped)

- `build_records/f9_m6b_module_container_round2_2026-11-24.txt` (`0b83c3ddc5c1dd20e39b86e4d02478c47003c2e6111980e4e647d51dafd668f1`) — **14 passed in 181.98s (0:03:01)**.
- `build_records/f9_m1_to_m6b_container_round2_2026-11-24.txt` (`819c8a27399229a8e867bbdeadb8b680375590a562daeb4df19f90c2a7a61a0e`) — the seven Flight 9 test files in one process: **291 passed in 988.40s (0:16:28)** (277 from the six placed files, 14 from this module).
- `build_records/f9_m6b_mutation_check.py` (`10f09596a9562cbcf6c440bc36f269e6fcac3d6e075a206690b42b0a4d585ea1`) and `build_records/f9_m6b_mutation_check_round2_2026-11-24.txt` (`297b6a2dce97eb91dc95c93a90e4bf071db51c11071e6d726c822ec313fee7dc`).
- `build_records/f9_m6b_round1_d1_routes_after_repair.py` (`11182c05bcf307563258917b13e8db673e936f9657763fc8113ac9e1a81ca9e7`) and its output `..._2026-11-24.txt` (`6dcb67d0460c778e37f855736fbd71b5d7ad268642a80e9d5467fab053c4c72e`): your Appendix R program with the final inequality replaced by equality and your table's cells and bonds asserted, as you prescribed. All 12 routes return `no eligible contour` for both indices. Your original program (`build_records/l2_m6b_round1_reproduce.py`, as committed) still reproduces on the round-1 bytes with the evaluator as then placed, and fails its assertion on these.
- To run: from `flights/mfa_fidelity/instrument`, `python -B -m pytest tests/test_f9_m6b.py -v -p no:cacheprovider`. `-k "outranks or criterion or coverage or forty or design or persistence or declaration or one_way or byte_unchanged"` runs the fast tests, the new one among them, in a few seconds.

## 7. Questions

**Q1.** Is D1 closed in this module: on every route of `evaluate_level_at`, `reported_thresholds` and `skeleton_boundary`, does a constant index receive `no eligible contour` whatever the map, with the point record intact? Can you construct an input where the copy at θ = 0.20 and the repaired placed evaluator now differ in any field?
**Q2.** Does the diff contain anything other than what §3 lists? Do the round-1 identities reconstruct?
**Q3.** Is the new declaration entry accurate and sufficient, and is the changed digest the only consequence for M6B-2, M6B-3 and M6B-4? Your disposition on those three now.
**Q4.** Is the new test discriminating for item 3 as you wrote it? Name any crossed state on this module's routes it leaves out.
**Q5.** Do your round-1 dispositions on M6B-1, 5, 6, 7, 8, 9 and the seven readings stand on these bytes?
**Q6.** Anything else.
