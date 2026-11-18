# F9 M4 placement note (prepared 2026-11-18)

**Module.** Flight 9 instrument module M4: the outcome tiers of Contract F9 v0.7 §5.6 and §7 and the persistence record of §5.4. From an evaluator level record to the level tier (the result table, L1 to L7), the arm tier (A1 to A4), flight B per composition, flight D from the two TB arms, and the persistence profile with Clopper–Pearson intervals. Built at Mike's word "build m4" (2026-11-17). Placed at his word "place m4" (2026-11-18) against `main` at `80306ab3d7ce4cd9712ec8bd3604a27e725f9772` (the M3 placement), checked against the remote on 2026-11-18 before the kit was built.

**Placed (instrument), all NEW; no placed file is edited:**

| File | SHA-256 |
|---|---|
| `mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` |
| `tests/test_f9_m4.py` (21 tests) | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` |

These are the bytes of L2's round-2 packet (`f9_m4_build_round2_L2.zip`, `74dac92809504ddd67200a2eb73e5400ac007e4023f0c5769c2715c537996721`), which L2 cleared. `test_everything_placed_before_m4_is_byte_unchanged` holds the ten placed `f9` files, the package root, `e1`, `f8` and `gates` to their LF identities at `80306ab`.

**Outcome declaration digest in the placed source:** `c94ec4bd7c9aa532264ab2adc91ab6d4948ebff652b5b58380e1befb54a35407` (`verify_outcome_declaration`), the same in both rounds. It identifies the declared labels, table and thresholds; it is not an identity of the implementation, which the source hash gives (L2 round 2, §2).

**Review history (every L2 return a byte copy, `_RECEIVED`):**

| Round | L1 document | L2 return | Verdict |
|---|---|---|---|
| 1 | `L1_TO_L2_F9_M4_BUILD_PACKET_2026-11-17.md` `674d1acc…` (packet `05abf794…`) | `L2_F9_M4_ROUND1_REVIEW_2026-11-18_RECEIVED.md` `5b6eeab9cb6f65820232d2e3d95f73ba4fa152506219631564e2b8e153fc901d` | DEFECT-WITH-REPAIR: D1, the arm record's self-check did not cover `level_causes` or `causes`; six forged arm records accepted, flight B = PRODUCED from five of them. M4-1 to M4-8 and M4-10 acceptable |
| 2 | `L1_TO_L2_F9_M4_ROUND2_RESPONSE_2026-11-18.md` `bb4b5425…` (packet `74dac928…`) | `L2_F9_M4_ROUND2_REVIEW_2026-11-18_RECEIVED.md` `d3391e61f22796899f5b148fcc1244c53660c8b81591b2dbee20bc9a61c2f5da` | **SOUND**: D1 closed; M4-9 as repaired and M4-10 with the fixed confidence level acceptable; no further defect |

**The defect was L1's.** The same kind had been repaired in M1 and M2 by rebuilding a record from its inputs; L1 did not apply that to the arm record in round 1. The repair: an arm record carries the 25 level records it was computed from and is accepted only if recomputing the arm from them returns the whole record, value and type. A second, smaller thing found by L1 while testing the repair: a level record with keys of two types was refused with Python's `TypeError` and is now refused with the module's own exception. L2's nonblocking note on the Clopper–Pearson tail was met by removing the argument; all 41 intervals are equal to round 1's (L2's comparison).

**The self-check is consistency, not provenance.** An accepted arm record is one `arm_tier` returns for the 25 level records it carries. That those level records belong to the terrain, composition, evaluation and runs in question is the runner's to bind.

**What was run, and by whom.**
- L2 completed the whole M4 test file in round 2: 21 passed in 60.24 s on its machine (Python 3.12.14), nothing deselected. L1's container: 21 passed in 101.24 s (the committed record) and 89 s in two other complete runs. Round 1 took 10.98 s; the difference is the recomputation of seven arms in each of the 32,768 flight-B calls of one test. No cache was added.
- L2's own checks: its six cases refused at both boundaries; 592 altered records refused at both boundaries; 37 genuine arms accepted; the two A4 cause pairs named below accepted.
- L1's junk-value program (`l1_m4_round2_fuzz.py`, 112,062 calls refused, none accepted) was read by L2 and NOT rerun by it. It is L1's evidence, a sample of positions, and is not in the test file.
- L2 did not fetch the remote; the pin in the packets is L1's statement, checked by L1 against the remote.

**A wording correction in the placed test file, for its next touch (L2 round 2, §3).** The docstring of the helper `_genuine_arms` says the 17 fixtures cover "each set of A4 causes". They cover five of the seven nonempty sets. `insufficient informative levels` with `isolated adverse level`, and `insufficient informative levels` with `finite resolution`, are not among the 17; the unchanged 6,000-sweep test asserts that all seven occur, and L2 constructed the two pairs and saw them accepted. The bytes are placed as reviewed; no behaviour is affected.

**A receipt correction, on record.** L2's first round-2 receipt repeated `f9/identities.py` at row 57 where the manifest has `f9/spectral.py`. Mike had L2 recompute the row before "execute"; the return's receipt matches the manifest in all 75 rows.

**Mike and the round-2 repair.** L1 made the D1 repair on reading L2's review, without waiting for Mike's word, and told him so with the round-2 packet. Nothing was placed.

**Declarations awaiting Mike's ratification, with the governance record:** M4-1 to M4-10 as listed in the round-1 packet document, with M4-9 and M4-10 as restated in the round-2 response. Three of them are choices he should see by name: recording every A4 cause that holds, in the contract's listing order (M4-6; L2 found no ruling needed); translating M3's two cause strings, `no edge at theta` and `below the informative minimum`, to the contract's `no edge at θ` and `under-resolved` in M4 until M3's next touch (M4-4); an arm record carrying its level records (M4-9). L2's acceptance is a technical ruling and is not that ratification.

**Carried to later modules (not obligations of M4):** the closure comparators (§4) and T0's four tests (§5.8); the reports of §5.7; the qualification of §6; the runner's binding and persistence of level and arm records (§5.9). Carried from M1 to M3: the master ruling, due before the runner; §2.8 persistence; the pre-rounding level counts and the evaluator stream's identity for the governance record; L2's two optional parser bounds for the next touch of `dynamics.py`; M3's cause strings at its next touch.

**Records placed with the module (container, noncanonical):** `f9_m4_module_container_2026-11-17.txt` (20 passed) and `f9_m4_module_container_round2_2026-11-18.txt` (21 passed); L2's round-1 program as extracted with its output on round 1; L1's outcome-reporting adaptation with its output on each round; the junk-value program with its output.

**Canonical module run (gate for the commit).** `python -m pytest tests\test_f9_m4.py -v -s -p no:cacheprovider` from `flights\mfa_fidelity\instrument` in the canonical environment, whole module, one process, on the placed bytes before commit. Its output is `f9_m4_module_canonical_2026-11-18.txt`, committed with this placement. The placement script stages nothing unless that run exits 0, and its identity of record is measured from a fresh clone after the commit. This is the first run of M4 on Windows. Every record in it is constructed in a test.

**Not run at this placement:** the M1, M2 and M3 modules again, and the whole canonical suite. M4 adds one source file and one test file and edits nothing.

**What placement does NOT do.** No run is authorized and no authorization file exists. No job has been run. No master is drawn. No outcome has been computed for any run of the rule: every level record M4 has seen was built in a test from chosen labels.

**Carried.** L1 has not opened the probe arrays for any boundary purpose and has not seen the boundary-compatibility endpoint. Held list unchanged (Gemini commission v3.1; two next-touch test repairs; third-order lattice-versus-ODE comparison; onset continuity; PD7-versus-floor correspondence).

*L1, 2026-11-18.*
