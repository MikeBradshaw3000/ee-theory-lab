# F9 M3 placement note (prepared 2026-11-17)

**Module.** Flight 9 instrument module M3: the composition evaluator N-E of Contract F9 v0.7 §5.5, steps 1 to 9, for one level of one arm. From the 40 seed maps (integer tail-tick counts) to the observed map's record and, per index, the typed resample counts and the result. Built at Mike's word "build m3" (2026-11-17). Placed against `main` at `6e731b821092083bc8acce16a23b2f56b6866354` (the M2 placement), checked against the remote on 2026-11-17 before the kit was built.

**Placed (instrument), all NEW; no placed file is edited:**

| File | SHA-256 |
|---|---|
| `mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` |
| `tests/test_f9_m3.py` (37 tests) | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` |

These are the bytes of L2's round-2 packet (`f9_m3_build_round2_L2.zip`, `9e687e5cac0ac742f56ce4975b7cb826afaa57b93dadd827ed6189bedf3f71f2`), which L2 cleared. `test_everything_placed_before_m3_is_byte_unchanged` holds the nine placed `f9` files, the package root, `e1`, `f8` and `gates` to their LF identities at `6e731b8`.

**Evaluator declaration digest in the placed source:** `79e93ccade624ec473c7c60225183458e0ed168e13c4e23fb7dbaa6ed2d2fef7` (`verify_evaluator_declaration`). It binds the resample count and thresholds, the quantile as 19/20, the evaluator stream's role (2^64 + 905), seed rule and draw, and the stated rules of the criterion, the distance, the quantile, the pruning, the minimum and the result order. The stream's identity is a build declaration under the contract's "a declared evaluator stream"; it is for Mike's acceptance with the governance record before canonical use (L2 rounds 1 and 2). The role makes an evaluator stream's seed sequence differ from every run's; that is an engineering declaration and not a proof that generated values are disjoint (L2 round 1, M3-8).

**Review history (every L2 return a byte copy, `_RECEIVED`):**

| Round | L1 document | L2 return | Verdict |
|---|---|---|---|
| 1 | `L1_TO_L2_F9_M3_BUILD_PACKET_2026-11-17.md` `2eca9a95…` (packet `0b4fa4cb…`) | `L2_F9_M3_ROUND1_REVIEW_2026-11-17_RECEIVED.md` `39756e4f60b41e71895615df76604a037ba8f3107fc7b1db47e7c37370722288` | DEFECT-WITH-REPAIR: D1, `check_weights` accepted an unsigned multiplicity vector whose sum wraps to 40; and a qualification of L1's exactness claim |
| 2 | `L1_TO_L2_F9_M3_ROUND2_RESPONSE_2026-11-17.md` `ba02827a…` (packet `9e687e5c…`) | `L2_F9_M3_ROUND2_REVIEW_2026-11-17_RECEIVED.md` `939dca526bdbcdbf52880e5c0b93ca988f0364d24af151f60e478cf8a219ccfe` | **SOUND**: D1 closed; the late-validation defect closed; the exhaustive decision check accepted for this lattice and ε; no further source repair |

Two defects, both L1's. D1 was found by L2. The second (a constructed resample set was validated only on the path that used it) was found by L1 while writing D1's closure test, and reported to L2 in round 2. L2's round-1 reproducer is committed as extracted (`l2_m3_round1_reproduce.py` `1d1fb5dd…`) with its output on each round.

**A limit of the clearance, on record.** L2 did not complete the M3 test file in either round: its runs exceeded its execution window (round 2: 24 of 37 tests shown before the window closed), and it says this is not to be read as a pass. What L2 executed to completion was the two new tests, with source inspection and the algebra of the decision check. The 37-test pass in the packets is L1's, in the container. The canonical run below is therefore the first complete run of this module by anyone other than L1, and it gates the commit.

**The arithmetic claim, as accepted.** Steps 1 to 4 and the distances are decided on integers. The quantile and S are IEEE doubles from correctly rounded operations: floats, not exact reals. The one decision made on them, S ≤ ε, equals the exact-real decision for every term this lattice can produce, shown by enumerating all 6,454,832 straddling triples (a, b, r) against an integer inequality. This holds for L = 100 and ε = 2.0; it is not a general guarantee, and the test fails if either changes. The fitted level among several contours within ε is chosen by float comparison; that is fidelity and the decision does not depend on it.

**An unchecked internal entry, on record (L2 round 2, Q3).** `evaluate_level` is the checked entry point. `evaluate_map` takes already-checked values from it and does not check its own inputs. L2 does not require a check there for this placement; if `evaluate_map` is later called from outside, validation must be added at that boundary.

**Mike and the round-2 repair.** L1 made the D1 repair on reading L2's review, without waiting for Mike's word, and told him so with the round-2 packet. Nothing was placed.

**Declarations awaiting Mike's ratification, with the governance record:** M3-1 to M3-10 as listed in the round-1 packet document, with M3-10 as restated in the round-2 response. L2's acceptance is a technical ruling and is not that ratification.

**Carried to later modules (not obligations of M3):** combining indices, levels and arms (§5.6); the reports of §5.7; building the seed maps from 40 run records, and persisting and binding level records (runner); the known-answer corpus and the qualification of §6, which call this evaluator; pricing on the canonical machine (`resource_benchmark`, §8 step 10). Carried from M1 and M2: the master ruling; §2.8 persistence; the pre-rounding level counts for the governance record; L2's two optional parser bounds for the next touch of `dynamics.py`.

**Records placed with the module (container, noncanonical):** `f9_m3_module_container_2026-11-17.txt` (35 passed) and `f9_m3_module_container_round2_2026-11-17.txt` (37 passed); the reproducer's two outputs.

**Canonical module run (gate for the commit).** `python -m pytest tests\test_f9_m3.py -v -s -p no:cacheprovider` from `flights\mfa_fidelity\instrument` in the canonical environment, whole module, one process, on the placed bytes before commit. Its output is `f9_m3_module_canonical_2026-11-17.txt`, committed with this placement. The placement script stages nothing unless that run exits 0, and its identity of record is measured from a fresh clone after the commit. This is the first run of M3 off Linux. Every map in it is synthetic.

**Not run at this placement:** the M1 and M2 modules again, and the whole canonical suite. M3 adds one source file and one test file and edits nothing.

**What placement does NOT do.** No run is authorized and no authorization file exists. No job has been run. No master is drawn. The evaluator has been applied to no run of the rule: every map it has seen was built in a test from a chosen region.

**Carried.** L1 has not opened the probe arrays for any boundary purpose and has not seen the boundary-compatibility endpoint. Held list unchanged (Gemini commission v3.1; two next-touch test repairs; third-order lattice-versus-ODE comparison; onset continuity; PD7-versus-floor correspondence).

*L1, 2026-11-17.*
