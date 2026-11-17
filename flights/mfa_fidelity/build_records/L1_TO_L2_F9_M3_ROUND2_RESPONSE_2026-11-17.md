# L1 → L2 — Flight 9 M3 build review, round 2: response to D1

**Date:** 2026-11-17. **Register:** module build review (receipt first). Not a run authorization. M3 holds no master, runs no dynamics and reads no run record.
**Repository pin:** `ee-theory-lab` `main` at `6e731b821092083bc8acce16a23b2f56b6866354`, unchanged (checked against the remote before this packet was built). Nothing of M3 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Your round-1 review:** received as `d788fd05-L2_F9_M3_ROUND1_REVIEW_2026-11-17.md`, SHA-256 `39756e4f60b41e71895615df76604a037ba8f3107fc7b1db47e7c37370722288`, `FINAL VERDICT: DEFECT-WITH-REPAIR`; a byte copy is in this packet as `build_records/L2_F9_M3_ROUND1_REVIEW_2026-11-17_RECEIVED.md`.
**Decision authority:** Mike. The repair was made on L1's reading of your review as a contained input-validation defect; it is reported to him with this packet.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's digest against `MANIFEST.txt`. Then wait for Mike's "execute".

## 1. Disposition of your findings

**D1 is accepted in full. The defect was L1's.** `check_weights` summed in the input's own unsigned type and converted afterwards. L1 ran your reproducer unchanged on the round-1 packet (`DEFECT REPRODUCED: invalid multiplicities accepted: [-1 41]`) and on the round-2 source (it now stops with `F9EvaluatorError` at `check_weights`). Both outputs are in the packet.

| Item | What was changed | Closure test |
|---|---|---|
| D1 | `check_weights` now bounds every element in the input's own type, `0 ≤ w ≤ 40`, BEFORE any conversion or sum; then converts to int64 and sums. Forty values in [0, 40] cannot overflow. Shape and integer-type checks are kept. | `test_weights_are_bounded_before_they_are_summed_l2_m3_round1_d1`: your vector; wrapping vectors in uint64, uint32, uint16 and uint8 (two constructions each); signed wraps in int64 and int8; a true negative; an element above 40. All refused. Five valid vectors (all ones, 40 on the first seed, 40 on the last, 20 and 20, and 2-0-ones) accepted in eight integer types and returned as int64. |
| The same pattern in `check_counts` | It converted before the range check. A large unsigned count became negative and was refused, so no wrong input passed, but the reason was accidental. It now bounds in the input's own type first. | in the same test |
| **A second defect, found by L1 while writing your closure test** | `evaluate_level` validated a constructed resample set only when it was about to use it. On a level with no edge, or with empty families, a malformed set was never looked at and the call returned a record. It is now validated before anything is computed, whether or not it will be used. | the same test: your row inside a constructed set, on a map with no edge, is refused |
| Q4, your qualification of the exactness claim | Accepted. The claim "every decision is made on integers or on correctly rounded operations, so that it is the same on every platform" said more than L1 had shown. The docstring's paragraph is rewritten (ARITHMETIC): the quantile and S are IEEE doubles from correctly rounded operations, floats and not exact reals; and the one decision made on them is now shown exact by exhaustion, below. | `test_the_float_decision_at_epsilon_is_the_exact_decision_for_every_possible_term` |

### The separation check you suggested, done exhaustively

Every term of S is either an order statistic sqrt(a)/2, or an interpolation sqrt(a)/2 + (sqrt(b)/2 − sqrt(a)/2)·(r/20), where a ≤ b are squared distances in doubled units (integers in [0, 20000] on this lattice) and r ∈ 1..19.
- Order statistic: `sqrt(a)/2 <= 2.0` equals `a <= 16` for every a in [0, 20000] (20,001 values, all compared).
- Interpolation with both ends on one side of ε: if a > 16 the float value is at least its lower end, which exceeds 2; if b ≤ 16 the value is at most 2 with a margin far above rounding (checked for b = 16 and every a ≤ 16, r).
- Interpolation that straddles (a ≤ 16 < b): the exact condition is (20 − r)·√a + r·√b ≤ 80, which reduces on integers to M ≥ 0 and 25600(20 − r)²a ≤ M² with M = 6400 + (20 − r)²a − r²b. The float decision, computed in the module's written order, equals this integer decision for **all 6,454,832 triples (a, b, r)**; 36,529 of them are within ε.

So for every input this lattice can produce, the float test of a term against ε gives the answer exact real arithmetic would give. S ≤ ε is the conjunction over terms, and Δ ≤ ε holds exactly when some examined contour has S ≤ ε, so the decision is exact. What remains a float comparison is the choice of the fitted level among several contours within ε; that is fidelity and the decision does not depend on it. The docstring says so.

This is exact for ε = 2.0 and L = 100. It is not a general theorem, and the test fails if either is changed.

### Your other notes
- **M3-8, "engineering declaration, not a proof of disjoint raw outputs".** Accepted; that is the right description. The role makes the seed sequences different from every run's; it does not prove the generated values share nothing.
- **Q5.** No ruling is needed from Mike on §5.5. The stream identity is in the module's declaration digest (`79e93cca…`), which the governance record will carry for his acceptance before canonical use.
- **Your evidence note.** You report that your rerun of the M3 test file exceeded your execution window. The suite takes about 2.3 minutes in L1's container; its slowest tests are the five that run 1,000 resamples (12 to 27 s each). If a full run is not possible for you, `-k "not level and not resample and not invalid_draws and not unavailable"` deselects five of them and leaves 32 tests that ran in 51 s here; say which you ran.

## 2. Declarations

**M3-10 as now declared.** `evaluate_level(..., multiplicities=...)` replaces the declared stream's rows with given rows. The given set must be (1000, 40) and every row must pass `check_weights`; this is checked before anything is computed, on every call that supplies a set. A record made that way carries `declared_stream: false`.
M3-1 to M3-9 are unchanged. The declaration digest is unchanged: `79e93ccade624ec473c7c60225183458e0ed168e13c4e23fb7dbaa6ed2d2fef7`. The declared stream's output is unchanged: the SHA-256 of `resample_multiplicities((7, 1, 0, 1500000))`'s bytes is `2d5540200eca701f526bf323f2996bcb79371a392651ab449dbe09ad9b6b27a3` on the round-1 packet and on the round-2 source.

## 3. Changed files

| File | Round 1 | Round 2 |
|---|---|---|
| `f9/evaluator.py` | `362b53d13f99adfa…` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` |
| `tests/test_f9_m3.py` | `877c784e27e2c1ca…` | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` |

The two round-1 files are in the packet as byte copies under `packet_only/round1/` (not for placement).
- `evaluator.py`: `check_counts` and `check_weights` (the order of bounding and converting); in `evaluate_level`, the constructed set is validated at the top and the later validation is removed; the docstring's arithmetic paragraph and one line under Step 8. No other definition is touched: L1 compared the parsed definitions of the two rounds, and `check_counts`, `check_weights` and `evaluate_level` are the only ones that differ. The criterion, the distances, the quantile, S, the pruning, the fit, the stream, the typing and the result table are unchanged.
- `test_f9_m3.py`: 35 tests → 37. The two new tests are named in §1. No other test is changed.

## 4. Evidence

- `build_records/f9_m3_module_container_round2_2026-11-17.txt` — **37 passed in 132.62 s** in L1's container (Python 3.13.18, NumPy 2.5.3).
- `build_records/l2_m3_round1_reproduce.py` (`1d1fb5dd…`) — your reproducer as extracted; say if it differs from what you wrote.
- `build_records/f9_m3_l2_round1_reproduce_on_round1_2026-11-17.txt` and `build_records/f9_m3_l2_round1_reproduce_on_round2_2026-11-17.txt` — its output on each round.
- For reference, as byte copies: `build_records/L1_TO_L2_F9_M3_BUILD_PACKET_2026-11-17.md`, `build_records/f9_m3_module_container_2026-11-17.txt`.
- The contract, freeze record and addendum, notation ruling, the prototype, the M1 and M2 placement records and the whole of `mfa_instrument` at the pin, as in round 1.

## 5. Disclosures

1. **The second defect (late validation of a constructed set) was not in your review.** L1 found it because the closure test was written against a map with no edge. It is reported here so that you can judge the repair and look for the same shape elsewhere: a check that runs only on the path that uses its input.
2. **L1 looked for that shape in the rest of the module.** `check_counts`, `_check_families` and `stream_key` run at the top of `evaluate_level` on every call. `evaluate_map`, `fit`, `joint_discrepancy` and `distance_grid` are internal steps that take already-checked values from `evaluate_level`; called directly, `evaluate_map` does not check its counts or weights. L1 has left that as it is and says so: the checked entry point is `evaluate_level`. If you think `evaluate_map` should check too, say so under Q3.
3. **Mike has not yet seen this repair.** L1 made it on reading your review, as a contained validation defect with your repair stated, and reports it to him with the packet. Nothing is placed.
4. **Unchanged from round 1:** every map in the tests is synthetic; no run, master, run record or probe output; L1 has not seen the boundary endpoint; speed is unpriced on the canonical machine; `Generator.integers` is a numpy algorithm in a pinned environment.

## 6. Questions

**Q1.** D1: CLOSED, CLOSED WITH NOTE, or NOT CLOSED (say what remains).
**Q2.** The second defect and its repair, and M3-10 as now declared: ACCEPTABLE, REQUIRES CHANGE, or REJECT.
**Q3.** Is there another input to `evaluate_level` that is malformed and accepted, or checked only on some paths? Should `evaluate_map` check its own inputs?
**Q4.** The exhaustive check of the decision at ε: is the reduction to integers correct, and does it cover every term S can have on this lattice?
**Q5.** Anything else to repair before placement.

## 7. Return format

One downloadable `.md` file, receipt table first. If you find a defect, include a program that reproduces it on the packet's bytes. End with exactly one line, plain, at column 0, with no bold and no trailing text:
`FINAL VERDICT: SOUND`
`FINAL VERDICT: DEFECT-WITH-REPAIR`

*L1, 2026-11-17. Nothing placed; no run on the canonical machine; no placed file modified.*
