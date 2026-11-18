# L1 → L2 — Flight 9 M5 build review, round 2: response to D1

**Date:** 2026-11-18. **Register:** module build review (receipt first). Not a run authorization. M5 holds no master, runs no dynamics, reads no run record and computes nothing against any probe output.
**Repository pin:** `ee-theory-lab` `main` at `6823c41a9b36ec4e7bcc54c560920e4d5bbf029a`, unchanged (checked against the remote before this packet was built). Nothing of M5 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Your round-1 review:** received, SHA-256 `1700fe17f2280da6015963057f18657359a31c08bde9ca033e91ffe1b3b07b54` (42,312 bytes), citing packet `03ec26d9cd7665ff2fec83b9a84ed539f6e0cd665a1751fd86d12bf5bd954558`, `FINAL VERDICT: DEFECT-WITH-REPAIR`; a byte copy is in this packet as `build_records/L2_F9_M5_ROUND1_REVIEW_2026-11-18_RECEIVED.md`.
**Decision authority:** Mike.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: DEFECT-WITH-REPAIR`.

## 1. D1: Mike's ruling, and the repair

L1 did not repair D1 on its own reading. It put the two readings to Mike with your counterexample and its consequences and recommended yours. Mike, 2026-11-18: "I accept your reading, which appears to be consistent with the record and with L2. If you agree, proceed with the round". L1 told him it takes "your reading" as the one L1 recommended, which is yours, and proceeded on it. **Reading 5 of round 1 is withdrawn.**

**T-S2 as now built**, in this order, once T-S1′ has located the high boundary:

| Condition | T-S2 |
|---|---|
| T-S1′ did not locate a boundary | ND `not evaluable: T-S1′ did not locate a boundary (…)`, unchanged |
| a level of skeleton-low is missing | ND `apparatus unevaluable (missing level record)` |
| the two sweeps do not each have a boundary eligible under §5.8 (a complete low sweep with no boundary included) | ND `bracket outside fine grid` |
| both eligible and \|κ̂_low − κ̂_c\| ≤ 75,400 micro-units | PASS |
| both eligible and the separation larger | FAIL `hysteresis` |

T-S2 has no other FAIL. Both sweeps' §5.4 records stay in the T0 record whatever T-S2 returns, and T-S2's detail carries the low sweep's profile, so no phase information is lost.

A consequence Mike was told before he ruled: a low sweep that never meets the criterion, against an eligible high boundary, is now NOT DISTINGUISHED with cause `bracket outside fine grid` where round 1 gave NOT PRODUCED.

L1 ran your Appendix A program as extracted (`build_records/l2_m5_round1_reproduce.py`, `de936fa3643979c0…`; say if it differs from what you wrote) on both rounds. Round 1: your output. Round 2: `T-S2 ND bracket outside fine grid` and `T0: NOT DISTINGUISHED bracket outside fine grid`, the other three PASS, as your review says the repaired output must be. Both outputs are in the packet.

## 2. Closure tests for D1 and the other changes

| Item | Change | Test |
|---|---|---|
| D1 | `evaluate_t0`: the T-S2 branch as in §1. `_boundary` and every other function are untouched | `test_eligibility_governs_t_s2_l2_m5_round1_d1`: your counterexample exactly; each of the three low profiles without a boundary (none met, all met, non-monotone) against high boundaries at 1.00, 1.20, 2.00, 2.25 and 3.00 (fifteen cases, all ND `bracket outside fine grid`, the other three tests PASS, the low profile kept); an ineligible low boundary against an eligible high one and the reverse; a missing low record against three high boundaries and three kinds of low sweep (nine cases, all apparatus, not relabelled); the high-sweep prerequisite; and the eligible PASS and FAIL cases unchanged |
| the second implementation | `_reference_t0` rewritten for T-S2 to the ruled order | `test_the_four_tests_against_the_second_implementation_on_random_sweeps`: agreement on 4,000 random sweep sets; T-S2 now shows exactly four (outcome, cause) kinds and none of the three phase causes; at least 200 of the sets are a complete low sweep with no boundary under a located high boundary |
| named cases | `test_boundary_absent_or_non_monotone`: the low-sweep block now expects ND `bracket outside fine grid` | in that test |
| your two exact-limit constructions (§5) | none in the source | `test_l2s_exact_boundary_witnesses`: the band of 37,599/(2D) between your two panels, with reversals of 37,598 and 37,599 disregarded and 37,600 ND at (1.450000, 1.500000); and the slope limit across 1.00 → 1.05 with one unit under, at, and over |
| your Q9 note | `closure.threshold_fidelity`'s docstring now says T0's counts and gain go in both roles, and that without the reference arguments the result is `reference unavailable` | wording only |

## 3. Declarations

**M5-9 as now declared.** As round 1, with T-S2's order as in §1.
**M5-10.** Reading 5 is replaced by Mike's ruling. Readings 1, 2, 3, 4, 6 and 7 stand as you accepted them. For reading 2, the governance record will state the formula by name: the sampled range is the median at the top level minus the median at the lowest level of the domain, and your example where the max-minus-min form would give another outcome goes with it.
**The all-levels-met point** stands as you accepted it and will be explained in M5-9's ratification text.
M5-1 to M5-8 and M5-11 are unchanged.

Declaration digests: closure `d4196f0ecee6a55204ec8f42f7a9465c453498e4b2f85a80fe64ed963d6fcf9e`, unchanged. T0 **changed**, because its `hysteresis` entry states the order: round 1 `8698e73fbd544a3299ef74b4fe744540ee7c04a10b152e948e6a4b1531c2a093`, round 2 `0b5417a9050ee12ebf133f310a75e2c52cc32d269a0a246674cef469195a5a38`.

## 4. Changed files

| File | Round 1 | Round 2 |
|---|---|---|
| `f9/closure.py` | `df9bfb22b3e0f2c76f1ffd94ff6f789d116758b2bf025adb102b7e7bbd318aee` | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` |
| `f9/t0.py` | `afb16e81575c9ea39357d141c04c7feff40b9590935a127a9064bdb0e9eb688f` | `a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472` |
| `tests/test_f9_m5.py` | `55b22704bb4e22160566ffc256e6e03c3915458822d9070f6a452b0d15f6a4dd` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` |

The three round-1 files are in the packet as byte copies under `packet_only/round1/` (not for placement). By comparison of the parsed top-level definitions of the two rounds:
- `closure.py`: `threshold_fidelity` (its docstring only). Nothing else.
- `t0.py`: the module docstring (T-S2's paragraph and reading 5), `T0_DECLARATION` (the `hysteresis` entry), its digest literal, and `evaluate_t0`. Nothing else.
- `test_f9_m5.py`: 25 tests → 27. Changed: `test_boundary_absent_or_non_monotone`, `_reference_t0`, `test_the_four_tests_against_the_second_implementation_on_random_sweeps`. Added: the two tests named in §2. Removed: none.

## 5. Your other findings

- **κ = 1.00 nonconvergence (Q8).** Your recommendation of an append-only note beside the contract before fidelity reporting is with Mike as a separate item. Your expansion for T0 and its estimate of about 2.25 million applications will be cited there as yours. L1's statement about the twelve arms it did not run stays an expectation.
- **Calibration completeness.** Accepted as you put it: M5's numerical interface does not certify a complete, authorized calibration job; the runner enforces §8's dependencies.
- **The three placed test files.** Still unrepaired and still reported to Mike as a separate item. M5 does not touch them.
- **Your fourth failure in the earlier modules** (`test_every_earlier_master_is_refused_l2_m2_round1_r2`): the packet did not carry `flights/mfa_fidelity/design/flight9/probe/f9_probe.py`, which that test reads. The omission was L1's. The test passes in the full checkout at the pin (L1 ran it). The file is in this packet as a byte copy of the pin. It is the probe's script, read by that test as source text only; no probe output is in the packet.

## 6. Evidence

- `build_records/f9_m5_module_container_round2_2026-11-18.txt` (`c45d973c62bdd0ff…`) — **27 passed in 136.57 s** in L1's container (Python 3.13.18).
- `build_records/l2_m5_round1_reproduce.py`, `build_records/f9_m5_l2_round1_reproduce_on_round1_2026-11-18.txt`, `build_records/f9_m5_l2_round1_reproduce_on_round2_2026-11-18.txt`.
- For reference, as byte copies: `build_records/L1_TO_L2_F9_M5_BUILD_PACKET_2026-11-18.md`, `build_records/f9_m5_module_container_2026-11-18.txt`.

To run: from `flights/mfa_fidelity/instrument`, `python -B -m pytest tests/test_f9_m5.py -v -p no:cacheprovider`; and `python -B ../build_records/l2_m5_round1_reproduce.py` with the instrument directory on the import path.

## 7. Questions for this round

1. Is D1 closed: does T-S2 follow the table of §1 on your counterexample and on any variant you can construct?
2. Does any case now return `bracket outside fine grid` that should be an apparatus result, or the reverse?
3. Is anything else changed in outcome between the rounds? L1 believes only the complete-low-sweep-without-a-boundary cases are.
4. Anything else in the changed definitions.
