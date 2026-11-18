# F9 M5 placement note (prepared 2026-11-18)

**Module.** Flight 9 instrument module M5: the comparators of Contract F9 v0.7 §4 (`f9/closure.py`: the site closure of §4.2 with the registered solver; each arm's skeleton threshold against κ = 1 and against T0's own threshold, §1.2′ (i) and §4.3) and T0 (`f9/t0.py`: the reference object κ̂_c,T0 and Flight 8's four tests as §5.8 redeclares them). Built at Mike's word "build m5" and placed at his word "place m5", both 2026-11-18, against `main` at `6823c41a9b36ec4e7bcc54c560920e4d5bbf029a` (the M4 placement), checked against the remote before the kit was built.

**Everything in M5 is fidelity or the T0 consistency exercise.** Nothing in it is scored, enters B or D, or gates an endpoint.

**Placed (instrument), all NEW; no placed file is edited:**

| File | SHA-256 |
|---|---|
| `mfa_instrument/f9/closure.py` | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` |
| `mfa_instrument/f9/t0.py` | `a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472` |
| `tests/test_f9_m5.py` (27 tests) | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` |

These are the bytes of L2's round-2 packet (`f9_m5_build_round2_L2.zip`, `7dcce4b0aadf9ccaf24ab9c3979ba955e215531946ceb7b84c774647ab82e0f1`), which L2 cleared.

**Declaration digests in the placed source:** closure `d4196f0ecee6a55204ec8f42f7a9465c453498e4b2f85a80fe64ed963d6fcf9e`; T0 `0b5417a9050ee12ebf133f310a75e2c52cc32d269a0a246674cef469195a5a38` (round 1 was `8698e73f…`; the `hysteresis` entry changed with the ruling below). They identify the declarations, not the implementations.

**Review history (every L2 return a byte copy, `_RECEIVED`):**

| Round | L1 document | L2 return | Verdict |
|---|---|---|---|
| 1 | `L1_TO_L2_F9_M5_BUILD_PACKET_2026-11-18.md` `94d7b60c…` (packet `03ec26d9…`) | `L2_F9_M5_ROUND1_REVIEW_2026-11-18_RECEIVED.md` `1700fe17f2280da6015963057f18657359a31c08bde9ca033e91ffe1b3b07b54` | DEFECT-WITH-REPAIR: D1, T-S2 returned Flight 8's low-sweep failure before applying §5.8's eligibility rule. M5-1 to M5-8 and M5-11 acceptable; readings 1, 2, 3, 4, 6, 7 acceptable |
| 2 | `L1_TO_L2_F9_M5_ROUND2_RESPONSE_2026-11-18.md` `8a552acb…` (packet `7dcce4b0…`) | `L2_F9_M5_ROUND2_REVIEW_2026-11-18_RECEIVED.md` `b0ea8c42e9c78fff192a16cc6b682af92614d72e2039c3f97446dd32d1f2b6a1` | **SOUND**: D1 closed; M5-9 and M5-10 acceptable as revised; no new blocking finding |

**Mike's ruling on T-S2 (2026-11-18), and how it was reached.** D1 was a reading L1 had flagged in round 1 (reading 5), not a coding slip: §5.8 says the bracket "applies only if" both skeleton boundaries are eligible, "otherwise the hysteresis test is unevaluable", and L1 had kept Flight 8's outcome for a low sweep with no boundary ahead of that. L1 did not repair on its own reading. It put both readings to Mike with L2's counterexample and recommended L2's. Mike: "I accept your reading, which appears to be consistent with the record and with L2. If you agree, proceed with the round". L1 told him it took "your reading" as the one it had recommended, L2's, and he sent the round on that basis after asking whether L1 had reservations. **As placed:** once T-S1′ has located the high boundary, a missing low record is an apparatus ND; otherwise T-S2 is ND `bracket outside fine grid` unless both sweeps have a boundary eligible under §5.8; only then is the separation compared. T-S2's only FAIL is `hysteresis`.

**What the ruling gives up, told to Mike before he sent the round.** A high sweep with an eligible boundary and a low sweep that never survives was a failure under Flight 8's rule. It is now ND with the cause `bracket outside fine grid` (the T0 record keeps the low sweep's profile beside it). The frozen text already sends a low boundary at 2.25, 2.50 or 3.00 to ND, and a low boundary beyond 3.00 is the next case along the same line. The final T0 word in such a case is NOT DISTINGUISHED only when the other three tests pass: a realization failure still gives NOT PRODUCED, and an earlier ND keeps its own cause (L2 round 2, §4; L1's first summary to Mike was too broad on this and was corrected).

**No interpretation record is placed with M5.** The ruling is recorded here, in the module's text and in the two packets. L1 offered Mike a short interpretation record beside the frozen contract for the T-S2 ruling and for the range formula; it awaits his word and is not in this placement.

**Readings accepted by L2 as build declarations, for Mike's ratification with the governance record.** (1) ŝ uses the divisor 39. (2) The sampled range is the median at the top level minus the median at the lowest level of the domain, Contract F8 §4.11's form, not max minus min; L2 built a branch where the two give different outcomes and asks that the formula be named in the governance record. (3) The skeleton continuity test keeps the reversal clause. (4) `hysteresis` in either direction. (6) Any bracket from 0.05 to under 0.10 gives the same outcomes on eligible boundaries; 0.0754 is used. (7) The low sweep's variance proxy is declared and unused. Also accepted: when every level meets the criterion, κ̂_c,T0 = 0.75 is available as an unbracketed reference while T-S1′ fails and T-S1c is not run.

**Consequences of the contract as frozen, on record.**
- The skeleton closure at κ = 1.00 is `comparator unavailable` by the registered solver on the three arms L1 ran (T0, TA·P, TB·H; last changes 1.3e-10, 1.9e-10, 1.6e-10 after 200,000 applications). L1 expects the same on all fifteen and has not run the other twelve; that is an expectation. L2 derived for T0 that about 2.25 million applications would be needed, and recommends an append-only note beside the contract before any fidelity report. That note awaits Mike's word.
- T0 can be PRODUCED only if both skeleton boundaries fall from 1.05 to 2.00.

**A defect in three placed test files, L1's, found while building M5 and NOT repaired here.** `test_f9_m2.py`, `test_f9_m3.py` and `test_f9_m4.py` each assert that the `f9` folder holds exactly the files placed up to their own module. At `6823c41` the M2 and M3 assertions fail; with this placement M4's fails too. L2 reproduced all three (rounds 1 and 2). The per-file identities those tests hold are correct. No placement ran an earlier module's tests, which is why it was not seen. Until those three lines are repaired, through L2, the combined earlier-module suite cannot be called passing. M5's own test requires the pinned files unchanged and its two files present, and does not forbid later files. The repair awaits Mike's word.

**What was run, and by whom.** L2 completed the whole M5 test file in both rounds (25 passed in 98.63 s; 27 passed in 95.49 s; Python 3.12.14). L1's container: 27 passed in 136.57 s (the committed round-2 record). L2's own round-2 checks: 2,162 decision-table cases against the ruled table, written without M5's boundary or eligibility code; paired record comparisons of the two rounds; the nearest attainable slope-limit cases. The second implementation in the test file is L1's and shares L1's reading of §5.8 by construction. L2 did not fetch the remote; the pin is L1's statement, checked by L1.

**Two wording corrections to L1's round-2 response (L2 round 2, N1 and §4).** "Exactly four (outcome, cause) kinds" for T-S2 is four after the high boundary is located and five overall, with the dependency ND; the test requires all five. And the statement about a never-surviving low sweep becoming NOT DISTINGUISHED holds when the other three tests pass, as said above. The response document is placed as sent.

**Not in M5 (L2: an acceptable boundary; the duties remain).** Comparing occupancy maps and edges with the closure's map (§1.2′ (iii)); the local m_i on the observed edge (§1.2′ (ii)); the resampling ranges of §5.7: the reports module. Binding the sweeps' and the calibration panels' numbers to run records, and enforcing §8's calibration and qualification dependencies: the runner. M5's numerical interface does not certify a complete, authorized calibration job.

**Declarations awaiting Mike's ratification, with the governance record:** M5-1 to M5-11 as listed in the round-1 packet document, with M5-9 and M5-10 as restated in the round-2 response. L2's acceptance is a technical ruling and is not that ratification.

**Carried from M1 to M4:** the master ruling, due before the runner; §2.8 persistence; the pre-rounding level counts and the evaluator stream's identity for the governance record; L2's two optional parser bounds for the next touch of `dynamics.py`; M3's cause strings at its next touch; the helper docstring in `test_f9_m4.py` at its next touch.

**Records placed with the module (container, noncanonical):** `f9_m5_module_container_2026-11-18.txt` (25 passed) and `f9_m5_module_container_round2_2026-11-18.txt` (27 passed); L2's round-1 program as extracted, with its output on each round.

**Canonical module run (gate for the commit).** `python -m pytest tests\test_f9_m5.py -v -s -p no:cacheprovider` from `flights\mfa_fidelity\instrument` in the canonical environment, whole module, one process, on the placed bytes before commit. Its output is `f9_m5_module_canonical_2026-11-18.txt`, committed with this placement. The placement script stages nothing unless that run exits 0, and its identity of record is measured from a fresh clone after the commit. This is the first run of M5 on Windows. The closure there uses Windows' exp; M5 claims no equality of closure maps or iteration counts across machines, and the tests assert none.

**Not run at this placement:** the M1 to M4 modules, and the whole canonical suite (see the three test files above).

**What placement does NOT do.** No run is authorized and no authorization file exists. No job has been run. No master is drawn. No T0 sweep exists: every sweep the T0 tests have seen was built in a test from chosen counts. The closure has been iterated on constructed indices and on the contract's terrain arrays only.

**Carried.** L1 has not opened the probe arrays for any boundary purpose and has not seen the boundary-compatibility endpoint. Held list unchanged (Gemini commission v3.1; two next-touch test repairs; third-order lattice-versus-ODE comparison; onset continuity; PD7-versus-floor correspondence).

*L1, 2026-11-18.*
