# L1 → L2 — Flight 9 M5 build review, round 1: the comparators of §4 and T0 (§4.3, §5.8)

**Date:** 2026-11-18. **Register:** module build review (receipt first). Not a run authorization. M5 holds no master, runs no dynamics, reads no run record and computes nothing against any probe output.
**Repository pin:** `ee-theory-lab` `main` at `6823c41a9b36ec4e7bcc54c560920e4d5bbf029a` (the M4 placement), checked against the remote before this packet was built. Nothing of M5 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Contract:** `FLIGHT_9_CONTRACT_v0_7.md`, FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`. §5.8 redeclares tests of Contract F8 v0.8.4 (§1.2, §3.4, §4.11), which is in the packet with the placed Flight 8 evaluator (`mfa_instrument/f8/evaluator.py`).
**Decision authority:** Mike. Built at his word "build m5".

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: DEFECT-WITH-REPAIR`.

## 1. What M5 is

Two new source files and one test file. No placed file is edited.

| File | SHA-256 | What it holds |
|---|---|---|
| `mfa_instrument/f9/closure.py` | `df9bfb22b3e0f2c76f1ffd94ff6f789d116758b2bf025adb102b7e7bbd318aee` | §4.1, §4.2 and the threshold comparison of §1.2′ (i) with §4.3's reference. Declaration digest `d4196f0ecee6a55204ec8f42f7a9465c453498e4b2f85a80fe64ed963d6fcf9e` |
| `mfa_instrument/f9/t0.py` | `afb16e81575c9ea39357d141c04c7feff40b9590935a127a9064bdb0e9eb688f` | §4.3's reference object and §5.8's four tests. Declaration digest `8698e73fbd544a3299ef74b4fe744540ee7c04a10b152e948e6a4b1531c2a093` |
| `tests/test_f9_m5.py` (25 tests) | `55b22704bb4e22160566ffc256e6e03c3915458822d9070f6a452b0d15f6a4dd` | |

Everything in M5 is fidelity or the T0 consistency exercise. Nothing in it is scored, enters B or D, or gates an endpoint.

**Not in M5, by L1's choice of boundary:** the comparison of occupancy maps and edges with the closure's map (§1.2′ (iii)), the local m_i on the observed edge (§1.2′ (ii)) and the resampling ranges of §5.7. They need the evaluator's maps and go to the reports module. Binding the sweeps' numbers to run records is the runner's. §6 places no qualification duty on T0's tests (Contract F8 did, §5.4 there); M5's known-answer cases are in its test file and are not a job.

## 2. Declarations (for Mike's ratification with the governance record; your disposition on each)

| # | Declaration |
|---|---|
| M5-1 | **The map.** §4.2's formula with the placed `dynamics.activation_probability` and `dynamics.local_density` applied to probabilities, and q, Δt, η₀ and λ as the lattice rule has them. Start p = 1 (skeleton) or p = π₁ (realization) at every cell. |
| M5-2 | **The stop rule.** After the k-th application, r_k = max\|p′ − p\|. Converged at the first k with r_k ≤ 1e-12; the map of record is the later iterate. If r_k > 1e-12 at k = 200,000 the record is `comparator unavailable` and carries the count, the last change and **no map**. The contract says "tolerance 1e-12 in max norm, at most 200,000 iterations"; "≤", "applications" and "the later iterate" are L1's. |
| M5-3 | **What converged means.** A change of at most 1e-12 in one application, not a bound on the distance to the fixed point. In the skeleton below the crossing the converged map is small and positive (about 2e-11 at κ = 0.75 on T0), not zero. |
| M5-4 | **Across machines.** exp is the platform's. The number of applications and the map's last digits may differ between machines; the map's SHA-256 in a record identifies that computation only. No equality across machines is claimed and no tolerance for one is declared in M5. |
| M5-5 | **Threshold against the crossing (§1.2′ (i)).** κ̂_c and its bracket by M4's `persistence_record`, computed inside from survivor counts (no persistence record is accepted). Normalized shift κ̂_c − 1 in integer micro-units; raw-g shift (κ̂_c − 1)·g_spec with g(κ̂_c) and g_spec beside it. The bracket's lower level gets the same two shifts, as κ̂_c's stated uncertainty (§5.7 "κ̂_c: per §5.4"). |
| M5-6 | **Against T0 (§4.3).** κ̂_c − κ̂_c,T0 in micro-units, with both raw gains beside it; no raw-g difference between an arm and T0 is formed (their indices differ in scale). κ̂_c,T0 is available when T0's §5.4 record has a κ̂_c: both phases observed, or every level meeting the criterion (then unbracketed). Otherwise, or when T0's counts are not supplied, `reference unavailable`. A non-monotone profile's suffix statistic is never used as a threshold. |
| M5-7 | **T0 inputs.** Per level and seed: survival (bool) and the tail active-count sum (int). A surviving run with a tail sum under 1,000, or a non-surviving run with one over 999 × 10,000, is refused as impossible. An absent or None level is a missing record. |
| M5-8 | **Arithmetic.** Every T0 decision is on integers or exact rationals: the median as the sum of the 20th and 21st sorted tail sums, ŝ² as an exact variance, the band compared squared, the slope criterion cross-multiplied. Floats appear in the record for reading only. |
| M5-9 | **The four tests and their order** as the placed Flight 8 evaluator applies them (its `_boundary`, `_monotone_and_continuity`, `t_s2`, `t_r1_prime`, `evaluate_p1`, `p1_determination`), with §5.8's redeclarations. T-S1c and T-S2 are ND `not evaluable: T-S1′ did not locate a boundary (…)` when T-S1′ does not pass. PRODUCED iff all four pass; NOT PRODUCED iff any fails; otherwise NOT DISTINGUISHED. |
| M5-10 | **Seven readings**, listed in `t0.py`'s docstring under "READINGS THIS MODULE MAKES" and in §3 below. |
| M5-11 | **Calibration panels** enter as tail sums (40 per level, skeleton-high and realization), and ŝ is computed from them here. A missing calibration level matters only where a reversal has to be judged; then the test is ND, apparatus, before any reversal is judged. |

## 3. The readings (M5-10). Each is a place where L1 had to read the contract; say for each whether it is acceptable as a build declaration or is a ruling for Mike

1. **ŝ_X's divisor is 39.** §5.8 names "the seed-to-seed standard deviation" and no divisor. Flight 8's census used ddof = 1.
2. **"The branch's sampled range" is med(top) − med(lowest level of the domain)**, Contract F8 §4.11's form, not max − min. §5.8 says "the skeleton medians' range over those levels". The endpoint form is never the larger of the two, so it never allows more increase.
3. **The skeleton continuity test keeps the reversal clause.** §5.8 says of the realization test that it "keeps Flight 8's reversal rule" and does not say it of the skeleton test; Contract F8 §4.11 has the clause in both.
4. **`hysteresis` in either direction.** T-S2 fails when the two boundaries differ by more than the bracket, whichever is higher, as the placed Flight 8 evaluator does. Contract F8 §4.11 states the pass condition with an absolute value and names the cause for the low boundary lying above.
5. **No low boundary: Flight 8's outcome, not `bracket outside fine grid`.** When skeleton-low has no boundary, T-S2 returns skeleton-low's own outcome and cause. §5.8's "otherwise the hysteresis test is unevaluable" could be read to cover that case too.
6. **The bracket's value does not move any outcome within [0.05, 0.10).** Eligible boundaries lie on the 0.05 grid from 1.05 to 2.00, so two of them pass exactly when they are the same level or neighbours. The registered 0.0754 is used; the test file recomputes A.4's two terms (0.0254 and 0.0055).
7. **The proxy is declared and unused.** No test compares medians of the low sweep, so the high-initialization ŝ never stands in for it.

One more point of the same kind, inside M5-9: when every level meets the criterion, §5.4 gives κ̂_c,T0 = 0.75 (unbracketed) and M5 reports the reference as available, while T-S1′ fails with `no inactive phase in sweep` and T-S1c is not run. §5.8 says the continuity comparison "runs over levels at and above κ̂_c,T0"; M5 follows Flight 8's orchestration, where it runs only from a boundary T-S1′ located.

## 4. Disclosures

1. **The skeleton closure at κ = 1.00 is `comparator unavailable` by the registered solver on every arm L1 tried.** At the crossing the zero-floor map decays like 1/k. On T0, TA·P and TB·H the change after 200,000 applications was 1.3e-10, 1.9e-10 and 1.6e-10. L1 expects the same on all fifteen arms and has not run the other twelve. Each such level costs 60 to 120 s in the container. This is what §4.2's solver gives; M5 does not alter the solver.
2. **Skeleton closures just above the crossing converge slowly**: 2,177 to 3,337 applications at κ = 1.05 on the three arms, under a second each.
3. **T0 can be PRODUCED only if both skeleton boundaries fall from 1.05 to 2.00.** A boundary at 1.00 or at 2.25 and above makes T-S2 ND by §5.8's eligibility rule. That is the contract's rule, stated here so it is not met as a surprise.
4. **The second implementation in the test file is L1's.** It is written from the contract's sentences on Fractions and the statistics library, and it agrees with the module on 4,000 random sweep sets covering 23 named (test, outcome, cause) branches. It shares L1's reading of §5.8 by construction; it cannot find a misreading.
5. **A defect in three placed test files, found while building M5. It is L1's.** `test_f9_m2.py`, `test_f9_m3.py` and `test_f9_m4.py` each assert that the `f9` folder holds exactly the files placed up to their own module. Each such assertion fails once a later module is placed: at the pin, `test_m1_e1_and_f8_are_byte_unchanged` (M2) and `test_everything_placed_before_m3_is_byte_unchanged` (M3) fail, and M4's will fail when M5 is placed. No placement ran an earlier module's tests, so it was not seen. The digests those tests hold are correct; only the folder-listing line is wrong. M5 does not touch those files. Its own test requires the pinned files unchanged and M5's two files present, and does not require the folder to hold nothing else. The repair of the three placed files is reported to Mike as a separate item.
6. **No T0 record is accepted on its word.** `threshold_fidelity` takes survivor counts and computes both persistence records. `evaluate_t0`'s output is an end product; M5 has no validator for it and nothing in M5 consumes one.

## 5. Evidence

- `build_records/f9_m5_module_container_2026-11-18.txt` (`3e571590bb1b39b1…`) — **25 passed in 140.37 s** in L1's container (Python 3.13.18). Three tests take most of it: the contract-arm nonconvergence case (about 60 s), the 4,000 random sweep sets (about 38 s) and the small-lattice nonconvergence case (about 27 s).
- To run: from `flights/mfa_fidelity/instrument`, `python -B -m pytest tests/test_f9_m5.py -v -p no:cacheprovider`. If the whole file exceeds your execution window, say which tests you ran; `--deselect tests/test_f9_m5.py::test_skeleton_closure_at_the_crossing_is_unavailable_on_t0` removes the longest.
- The first test that uses a contract arm builds the identity bundle (about 10 s).

## 6. Questions

**Q1.** `closure.py`: is the map §4.2's, and is the stop rule (M5-2) an acceptable reading of "tolerance 1e-12 in max norm, at most 200,000 iterations"? Is withholding the map on nonconvergence right?
**Q2.** Declarations M5-1 to M5-11: for each, ACCEPTABLE, REQUIRES CHANGE (say what), or REJECT.
**Q3.** The seven readings of §3 and the point under them: for each, acceptable as a build declaration, or a ruling for Mike? Where you think the other reading is the contract's, say so.
**Q4.** `t0.py` against the placed Flight 8 evaluator: does any branch, order or cause differ from Flight 8's in a way §5.8 does not redeclare?
**Q5.** Exact arithmetic (M5-8): can you construct tail sums for which a decision in `t0.py` differs from the same rule evaluated in exact arithmetic from the contract's formulas?
**Q6.** Inputs: can you construct a sweep or calibration input that is accepted and impossible, or refused and possible (M5-7)?
**Q7.** Is any of M5's scope boundary (§1, "Not in M5") a gap that must be closed in this module?
**Q8.** Disclosure 1: is `comparator unavailable` at κ = 1.00 for the skeleton something you want recorded beside the contract before any fidelity report is built, or is the record's own statement enough?
**Q9.** Anything else.
