# F9 evaluator precedence repair: placement note (prepared 2026-11-23)

**What this is.** A repair of placed, cleared bytes: the Flight 9 composition evaluator (`f9/evaluator.py`, module M3, placed at `80306ab`) gave the wrong unavailable cause for a constant index on a map that is empty, full or under-resolved. Repaired at Mike's ruling of 2026-11-23, "1. Repair 2. Evaluator repair is its own cycle 3. Defer 2 cause strings", against `main` at `c6c21c497366d3ca71e0487127c774aacfd14ba1` (the M6 part 1 placement), checked against the remote before the kit was built. The kit was prepared on 2026-11-23 for placement the next morning; the canonical record's file name carries 2026-11-24. If the run happens on another day, the next note records the true date.

**The defect, and whose it is.** `evaluate_level` tested whether the observed map is informative before it tested whether the index's family is empty. Contract F9 v0.7 §7 ranks the constant index (L2, `no eligible contour`) above an empty or full region (L3) and under-resolution (L4), and §6.2 row 15 says "For the constant index the cause does not depend on the sample, and every output other than `no eligible contour` is an error." The contract is unambiguous; no reading was needed. **The error is L1's, made in the M3 build.** M3's unavailable-state test crossed a constant family only with an informative map and could not see it; L2's M3 review did not find it. L2 found it in its review of M6 part 2 (`L2_F9_M6B_ROUND1_REVIEW_2026-11-23_RECEIVED.md`, `31fd32e258482f81d3fc8762271fc4f722ac69d6ae77a73a97b30fb7c58dd78f`, finding D1), whose orchestration copy had inherited it and whose equality tests could not see an error shared by both sides.

**What it affected.** The cause string of an empty-family index in those crossed states, in the evaluator's level record. No compatible, adverse or unresolved result, no typed draw, no point record and no stream. No job had been run, so no record carries it. On the declared panel the only constant index is T0's, which is never scored.

**Placed (five files, all MODIFIED; these are the bytes L2 cleared in `f9_evaluator_repair_round1_L2.zip`, `e82a62ed1dacd0d79cfbf72a9f866ae38002791d53d1220253f094e97dcf37f9`):**

| File | Before (at `c6c21c4`) | After | Change |
|---|---|---|---|
| `mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | `ddfa49b11955de42d5b6638d892af4c75756ff6b1b5f35ea0884c4de7b2a07a1` | The two per-index branches of `evaluate_level` exchanged, so the empty family is tested first; four docstring lines stating the precedence |
| `tests/test_f9_m3.py` (38 tests, was 37) | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` | `d167f77229fa87cd4aca2fe06dfc051182d068cd95699e2a710f2ac19da312f5` | One test and one helper added; no existing line changed |
| `tests/test_f9_m4.py` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` | `751c808680521a0ac7ae088cd0edd1635a48eda7d5f7fabd15fec179fca1ab61` | The pinned identity of `evaluator.py` and the comment on that table |
| `tests/test_f9_m5.py` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` | `5843bec1a35be64da87b31fb72eb223d54cbf323b8db02177d218ba716532954` | The same |
| `tests/test_f9_m6.py` | `74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56` | `606b079793b064b646a3c2565486566d00e4464fd90574f57fea4493a4c6e16b` | The same; and the two wording notes L2's M6 round 2 left for this file's next touch (a comment and a docstring; no assertion changed) |

`f9_evaluator_precedence_repair_2026-11-23.diff` (`4b3868853455e9027171e6e2276ae53c0028e292bf85d38710010ca54646793c`) is the whole change.

**Unchanged.** The evaluator's declaration tuple and its digest (`79e93ccade624ec473c7c60225183458e0ed168e13c4e23fb7dbaa6ed2d2fef7`); the resample stream; every registered constant; the cause strings; every other placed module.

**Review.** One round. `L1_TO_L2_F9_EVALUATOR_PRECEDENCE_REPAIR_PACKET_2026-11-23.md` (`265d3ea3e2658c7f53445c775cecd845aa68e968f1216d2d06f8af65e4d2c5f8`); L2's return `L2_F9_EVALUATOR_PRECEDENCE_REPAIR_ROUND1_REVIEW_2026-11-23_RECEIVED.md` (`009a86f178f31021d91cd334bf7bf03a9d504e1985d79b2ee6b5f7c351daa944`), a byte copy: **FINAL VERDICT: SOUND**, within the scope of this dependency repair.
- **The change boundary is proven by inverse edit.** L2 undid the named edits by hand, and separately reversed every hunk of the supplied diff against the repaired bytes with no offsets; both reproduced all five prior files byte for byte. `l2_evaluator_repair_reconstruct.py` is L2's Appendix A, extracted byte for byte (`8cb5e4134442f71f301c414588db9a70c9537489469fde7ea059044e36125397`, the value L2's Appendix B gives for it); `f9_evaluator_repair_l2_reconstruct_2026-11-23.txt` is L1's run of it on the packet: five reconstructions, each byte-equal to the pin.
- **The new test discriminates.** L2 ran it unchanged against both evaluators: it passes on the repaired one and fails on the placed one at the first constant-family assertion. L1 saw the same.

**A statement of L1's that L2 narrowed.** The packet said the placed M4 (`outcomes.level_from_evaluation`) gives the same level record before and after. That holds for correctly bound declared inputs: on T0, M4 already returns the not-scored state "whatever the map", so it had been masking the evaluator's error on the declared panel. It does not hold for every input. A constant-family evaluation labelled as a non-T0 terrain was accepted before (as `no edge at θ`) and is now refused by M4's existing guard, because the repaired cause exposes the wrong binding. L2: expected enforcement of the existing domain, not a defect of the repair.

**Deferred by Mike's ruling (3), still carried.** M3's two cause strings (`no edge at theta`, `below the informative minimum`) keep their wording. They were carried "to the next touch of `evaluator.py`"; this was that touch, and Mike deferred them again so that the repair is the ordering alone. Changing them also means changing the placed `outcomes.py`, which translates them (M4-4). L2: the deferral is consistent with the repair being sound on its own.

**Carried to the next touch of `test_f9_m3.py` (L2's suggestions; not blocking, not added here so that the placed bytes are the cleared bytes).** Three crossed states L2 checked and found correct: a constant family with a complement under 100 cells; a constant family with malformed input (refused before any unavailable record); a constant index beside a non-constant sibling made unstable by constructed resamples (the constant stays L2; an empty-family index cannot itself reach L5, since it never enters the draw loop).

**Closed by this placement.** The two wording notes carried for `test_f9_m6.py` in the M6 placement note.

**Not in this repair, by Mike's ruling (2).** M6 part 2 (`f9/evaluator_reports.py`). Its round-1 packet (`6a00972c7a753d420b6a2e3724b209355e63723051b7067cd6b0e53e3f9ebc19`) stands at NOT SOUND on D1. Its round 2 follows this placement, pinned to the new `main`, with its orchestration copy synchronized and the crossed-state regressions on its own routes. L2's review of it is committed here because this repair answers its finding; `l2_m6b_round1_reproduce.py` is its Appendix R, which needs part 2's module and so cannot run on `main` until part 2 is placed. `f9_evaluator_repair_placed_routes_2026-11-23.txt` is L1's run of its three maps through the placed route, before and after.

**What was run, and by whom.**
- L2 (Python 3.12.14, numpy 2.3.5): the M3 and M4 test files in full and the M5 and M6 identity checks, 61 passed in 253.97 s; the new test against both evaluators; the two reconstructions; focused probes. L2 did **not** rerun all six files and did not fetch the remote.
- L1's container (Python 3.13.18, numpy 2.5.3): the six Flight 9 test files in one process on the repaired bytes, 277 passed in 726.87 s (`f9_m1_to_m6_container_evaluator_repair_2026-11-23.txt`).
- The canonical machine: the six files in one process on the placed bytes, before anything is staged (`f9_m1_to_m6_canonical_2026-11-24.txt`, written by the placement script; its identity of record is measured from a fresh clone after the push).

**A lesson for the record.** Pinning earlier sources by content in later tests does what it is for: one exchanged pair of branches in M3 cannot be placed without touching the tests of M4, M5 and M6, and the change is visible in each. The cost is five files for a two-branch repair.

**Placement authorizes no run.** No job has been run and no master has been drawn.
