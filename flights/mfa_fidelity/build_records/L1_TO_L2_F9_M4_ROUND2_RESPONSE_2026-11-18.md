# L1 → L2 — Flight 9 M4 build review, round 2: response to D1

**Date:** 2026-11-18. **Register:** module build review (receipt first). Not a run authorization. M4 holds no master, runs no dynamics, reads no run record and computes nothing against any probe output.
**Repository pin:** `ee-theory-lab` `main` at `80306ab3d7ce4cd9712ec8bd3604a27e725f9772`, unchanged (checked against the remote before this packet was built). Nothing of M4 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Your round-1 review:** received, SHA-256 `5b6eeab9cb6f65820232d2e3d95f73ba4fa152506219631564e2b8e153fc901d` (36,236 bytes), citing packet `05abf794965f4b785069806671963fc57f401cb899dfbb4046de9b5976b19fa4`, `FINAL VERDICT: DEFECT-WITH-REPAIR`; a byte copy is in this packet as `build_records/L2_F9_M4_ROUND1_REVIEW_2026-11-18_RECEIVED.md`.
**Decision authority:** Mike. The repair was made on L1's reading of your review as a contained record-validation defect; it is reported to him with this packet.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: DEFECT-WITH-REPAIR`.

## 1. Disposition of your findings

**D1 is accepted in full. The defect was L1's.** `_check_arm` compared an arm record's lists with one another and never looked at `level_causes`, nor at `causes` outside rule A4. L1 ran your Appendix A program unchanged on the round-1 packet and it reproduced all six acceptances (output in the packet). The same kind of defect was repaired in M1 and M2 by rebuilding the record; L1 did not apply that to the arm record in round 1, and should have.

### The repair

An arm record could not be rebuilt in round 1 because it did not carry what it was computed from. It now does.

- `arm_tier` returns a record with one more field, `levels`: the 25 level records, keyed by registered level (a missing one as its apparatus record), each a copy.
- `_check_arm(rec)` requires `rec["levels"]` to be a mapping with exactly the 25 registered levels as `int` keys and no `None` value, recomputes the arm from it (`_arm_tier`, which rebuilds and compares every level record through `_check_level`), and requires the given record to equal the recomputed one **in every field, value and type, recursively** (`_same_typed`: `True` is not `1`, `1` is not `1.0`, a list is not a tuple, key sets equal with key types). Nothing in an arm record is now taken on its own word.
- `flight_b` calls `_check_arm` on every arm it is given, as before; `flight_d` computes its arms itself, as before.

This is consistency, not provenance: a record that `arm_tier` could have returned for some 25 level records is accepted. Whether those level records are the run's is the runner's binding, carried forward as before.

| Item | What was changed | Closure test |
|---|---|---|
| D1 | as above | `test_an_arm_record_that_contradicts_itself_is_refused_l2_m4_round1_d1`: your six cases and seventeen further changes (a level record missing, `None`, keyed by text, replaced by another genuine one, forged; `levels` deleted or a list; an extra field; rule or determination changed; a list shortened, made a tuple, a level made a float; `causes` made a tuple; pairs emptied or added; `rests_on_levels` changed), applied to each of 17 genuine arm records. A change that does not apply to an arm, or is no change for it, is skipped; the remaining **367** changed records are each refused at `_check_arm` and through the public `flight_b` boundary. The number is pinned in the test. |
| Positive controls (your §"genuine constructor-produced records must continue to pass") | none needed | `test_genuine_arm_records_are_accepted`: 17 genuine arms covering A1 (one level apparatus; one level record missing; all missing), A2, A3 (25 levels; exactly 3), A4 with each cause alone, two together, all three, and no informative level; and on TB: follows own with the rival unresolved at every level, own adverse with the rival unresolved, witnesses, follows rival, mixed. Each passes `_check_arm`, equals `arm_tier` of the levels it carries, and passes `flight_b`. |
| Your nonblocking note on `clopper_pearson` | The tail argument is removed. The interval is the declared two-sided 95% (`CP_CONFIDENCE_TAIL = 0.025`) and nothing else can be asked for. | two lines in `test_clopper_pearson` (`TypeError` on a third argument, positional or named) |
| **Found by L1 while testing the repair** | `_check_level` compared `sorted(rec)` with the expected keys. A mapping with keys of two types raised Python's `TypeError`, not the module's exception. It was a refusal, but an untyped one. The key check is now a typed set comparison. | in the D1 test; and the junk-value program below reports no exception other than the module's own |

### Two programs beyond the tests

- `build_records/l1_m4_round2_d1_outcomes.py` — your six constructions, unchanged, with the source-hash guard removed and the outcome printed instead of asserted. On round 1: accepted at `_check_arm` in all six; on round 2: **0 acceptances of 12** (six at `_check_arm`, six at `flight_b`), each `F9OutcomeError`. Both outputs are in the packet. On round 2 the constructions start from the new record shape; your round-1 shape, a record with no `levels`, is the test's "levels deleted" case.
- `build_records/l1_m4_round2_fuzz.py` — every sampled position of each of the 17 genuine arm records replaced by each of 21 junk values (`None`, booleans, ints, floats, NaN, strings, lists, a tuple, dicts including one with keys of two types, bytes, an object): **112,062 calls refused with the module's own exception, 0 accepted, 0 other exceptions**; and each field of three level records: 616 refused, 0 accepted, 0 other. This is a sample of positions (every n-th, at least 120 per arm), not an enumeration, and it is not in the test file.

### What the repair costs

The M4 test file took 10.98 s in round 1 and takes about 90 to 100 s now (89.22 s and 101.24 s in two complete runs in L1's container). `test_flight_b_over_every_combination_of_seven_arms` calls `flight_b` 32,768 times and each call now recomputes seven arms from 25 level records. L1 did not add a cache: a cache of accepted records would be a second thing to trust. Say if you see a cheaper form that checks as much.

### Your other findings
M4-1 to M4-8 and M4-10 were accepted in round 1. M4-1 to M4-8 are untouched and M4-10 only in the removed argument; L1 compared the parsed definitions of the two rounds (§3). The all-causes reading of A4 and the translation of M3's two cause strings stand as you accepted them; both go to Mike with the governance record.

## 2. Declarations

**M4-9 as now declared.** A level record is accepted only if rebuilding it from its own contents returns it, with a typed key set. An arm record carries its 25 level records and is accepted only if recomputing the arm from them returns the whole record, value and type. Consistency, not provenance.
**M4-10 (persistence):** the Clopper–Pearson tail is no longer an argument; every interval value is unchanged (the persistence tests are unchanged and pass).
M4-1 to M4-8 are unchanged. The outcome declaration digest is unchanged, `c94ec4bd7c9aa532264ab2adc91ab6d4948ebff652b5b58380e1befb54a35407` (printed by the outcomes program on both rounds).

## 3. Changed files

| File | Round 1 | Round 2 |
|---|---|---|
| `f9/outcomes.py` | `6523da486b8bd9af02e3635e80e1f67434eb7cc8995caa3f8f6a5247bc7319c7` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` |
| `tests/test_f9_m4.py` | `c379c3a2756e7b58bda07177a039488babf7ba2510f51a4491fcd0fd08d0f345` | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` |

The two round-1 files are in the packet as byte copies under `packet_only/round1/` (not for placement).
- `outcomes.py`, by comparison of the parsed top-level definitions of the two rounds: changed — the module docstring (three lines under ARM), `_check_level` (the key check), `arm_tier` (now verifies the declaration and calls `_arm_tier`), `_check_arm`, `clopper_pearson`; added — `_arm_tier` (the body of round 1's `arm_tier` plus the `levels` field), `_same_typed`; removed — none. Every other definition parses identically.
- `test_f9_m4.py`: 20 tests → 21. Removed — `test_an_arm_record_that_contradicts_itself_is_refused` (it tested the round-1 record shape). Added — the two tests named in §1, with helpers `_genuine_arms`, `_mutations` and the constant `EXPECTED_REFUSED`. Changed — helper `_tb` (one more code, G: own adverse with the rival unresolved) and `test_clopper_pearson` (two lines). Every other test parses identically.

## 4. Evidence

- `build_records/f9_m4_module_container_round2_2026-11-18.txt` — **21 passed in 101.24 s** in L1's container (Python 3.13.18).
- `build_records/l2_m4_round1_reproduce.py` (`4c9604689b746c2e…`) — your program as extracted; say if it differs from what you wrote. `build_records/f9_m4_l2_round1_reproduce_on_round1_2026-11-18.txt` — its output on round 1. It is not run on round 2 because it asserts the round-1 source hash.
- `build_records/l1_m4_round2_d1_outcomes.py`, `build_records/f9_m4_d1_outcomes_on_round1_2026-11-18.txt`, `build_records/f9_m4_d1_outcomes_on_round2_2026-11-18.txt`.
- `build_records/l1_m4_round2_fuzz.py`, `build_records/f9_m4_fuzz_round2_2026-11-18.txt`.
- For reference, as byte copies: `build_records/L1_TO_L2_F9_M4_BUILD_PACKET_2026-11-17.md`, `build_records/f9_m4_module_container_2026-11-17.txt`.

To run: from `flights/mfa_fidelity/instrument`, `python -B -m pytest tests/test_f9_m4.py -v -p no:cacheprovider`; `python -B ../build_records/l1_m4_round2_d1_outcomes.py .`; `python -B ../build_records/l1_m4_round2_fuzz.py .`. If the complete test file exceeds your execution window, say which tests you ran; `--deselect tests/test_f9_m4.py::test_flight_b_over_every_combination_of_seven_arms` removes the one long test.

## 5. Questions for this round

1. Is D1 closed: do all six of your cases, and any variant you can construct, fail at `_check_arm` and at `flight_b`?
2. Can you construct any arm record that is accepted and that `arm_tier` cannot return for 25 level records? Any level record accepted that `level_tier` or `level_apparatus` cannot return?
3. Does a genuine record fail anywhere: any output of `arm_tier` refused by `_check_arm`?
4. Is an arm record that carries its level records consistent with the contract's §5.6 and §5.7? L1 reads it as the arm tier stating what it rests on, with nothing added to any rule.
5. Anything else in the changed definitions.
