# L1 → L2 — Flight 9 evaluator repair: the cause precedence of a constant index (your M6B round-1 finding D1), round 1

**Date:** 2026-11-23. **Register:** repair of placed, cleared bytes (receipt first). Not a run authorization. No job has been run and no master has been drawn.
**Responds to:** your M6B round-1 review (`L2_F9_M6B_ROUND1_REVIEW_2026-11-23_RECEIVED.md`, `31fd32e258482f81d3fc8762271fc4f722ac69d6ae77a73a97b30fb7c58dd78f`, in this packet as received), finding D1 and its required repair, item 1.
**Repository pin:** `ee-theory-lab` `main` at `c6c21c497366d3ca71e0487127c774aacfd14ba1` (the M6 part 1 placement), checked against the remote before this packet was built. The five changed files are not committed. Every other file in this zip that exists at the pin is a byte copy of it; the five files as they stand at the pin are under `packet_only/before/`.
**Contract:** `FLIGHT_9_CONTRACT_v0_7.md`, FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`. Unchanged.
**Decision authority:** Mike. On your finding he ruled, 2026-11-23: "1. Repair 2. Evaluator repair is its own cycle 3. Defer 2 cause strings".

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: NOT SOUND` (no bold, no backticks, nothing after it).

## 1. The defect, and whose it is

`evaluator.evaluate_level` (module M3, placed at `80306ab`, cleared by your M3 round 2) tested whether the observed map is informative before it tested whether the index's family is empty. For a constant index on a map that is empty, full or under-resolved it returned the map's cause. Contract §7 ranks the constant index (L2, `no eligible contour`) above L3 and L4, and §6.2 row 15 says "For the constant index the cause does not depend on the sample, and every output other than `no eligible contour` is an error."

The error is L1's, made in the M3 build. M3's unavailable-state test crossed a constant family only with an informative map, so it could not see it. L1 reproduced all twelve routes of your Appendix R on the M6B packet bytes before changing anything.

**What it affected.** The cause string of a constant index in those crossed states, in the level record's `indices`. No compatible, adverse or unresolved result, no typed draw, no point record and no stream is involved. On the declared panel the only constant index is T0's, which is never scored (§5.8); in qualification it is row 15's constant-index quota.

## 2. The change, in full

Mike ruled the repair is its own cycle, ahead of M6 part 2, and that it changes the ordering and nothing else. Five placed files change. `build_records/f9_evaluator_precedence_repair_2026-11-23.diff` is the whole of it (162 lines of unified diff).

| File | At the pin | Repaired | What changed |
|---|---|---|---|
| `mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | `ddfa49b11955de42d5b6638d892af4c75756ff6b1b5f35ea0884c4de7b2a07a1` | In `evaluate_level`, the two branches of the per-index test are exchanged, so `len(fam) == 0` is tested first (with a comment naming §7). In the module docstring, four lines are added after the sentence on unavailable states, stating the precedence and that the point record still describes the map. Nothing else. |
| `tests/test_f9_m3.py` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` | `d167f77229fa87cd4aca2fe06dfc051182d068cd95699e2a710f2ac19da312f5` | One test and one helper added (`test_a_constant_index_outranks_the_maps_state_l2_m6b_round1_d1`, `_same_point`). No existing line changed. 38 tests (was 37). |
| `tests/test_f9_m4.py` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` | `751c808680521a0ac7ae088cd0edd1635a48eda7d5f7fabd15fec179fca1ab61` | The pinned identity of `evaluator.py` in `PLACED`, and the comment on the `PLACED` line. |
| `tests/test_f9_m5.py` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` | `5843bec1a35be64da87b31fb72eb223d54cbf323b8db02177d218ba716532954` | The same two lines. |
| `tests/test_f9_m6.py` | `74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56` | `606b079793b064b646a3c2565486566d00e4464fd90574f57fea4493a4c6e16b` | The same two lines; **and** the two wording notes of your M6 round-2 review, which the M6 placement note carried "for the next touch of `test_f9_m6.py`": the comment over the all-active and all-inactive loop, and the docstring of `test_records_at_different_widths_must_be_of_one_sequence`, which now says the relations are necessary and not sufficient and cites your round-2 stack. No assertion changed. |

**Unchanged, and tested unchanged:** the evaluator's declaration tuple and its digest (`79e93ccade624ec4…`, verified equal to its literal after the edit); the stream; every constant; the cause strings.

**Not in this repair, by Mike's ruling (3):** M3's two cause strings (`no edge at theta`, `below the informative minimum`) keep their present wording. They were carried "to the next touch of `evaluator.py`" and this is that touch. Changing them would also change the placed `outcomes.py`, which translates them to the contract's `no edge at θ` and `under-resolved` (M4-4). Mike deferred them again so that this repair is the ordering alone. They remain a carried item.

**Not in this repair, by Mike's ruling (2):** M6 part 2. Its orchestration copy still has the old ordering and its packet stands at NOT SOUND. Its round 2 follows this repair's placement, pinned to the new `main`, with the copy synchronized and the crossed-state regressions on its own routes.

## 3. The new test

`test_a_constant_index_outranks_the_maps_state_l2_m6b_round1_d1` crosses five maps (all zero; uniformly below θ; all 1,000; an 81-cell block; your `[10:16, 10:16]` patch, checked at 60 cells and 32 bonds) with four family sets:

- T0's two constant families: both indices must be exactly `{"result": "not informative", "cause": "no eligible contour", "resampled": False}`, with the point record still not informative and carrying the map's reason;
- TA's non-constant families: the map's cause, as before;
- a mixed set, P constant and H TB's: each index its own cause;
- the mixed set the other way round.

It also requires the point record to be the same whichever families are supplied. Run against the evaluator at the pin, it fails (L1 ran it: one failure, at the first constant-family assertion). The existing `test_unavailable_states` is untouched and still passes.

## 4. Consequences L1 can see

1. **Downstream of the level record.** `outcomes.level_from_evaluation` (M4) already applies §7's order itself on T0: when either index is not informative and the terrain is T0, it returns the not-scored state with `no eligible contour` "whatever the map" (its comment: "L2 precedes L3 to L5"), without reading which unavailable cause the evaluator gave. So M4's level record for T0 is the same before and after this repair, and M4 was hiding the evaluator's error on the declared panel. For any other terrain M4 refuses `no eligible contour`. The repair therefore changes the evaluator's own level record and whatever reads it directly (the reports of M6 part 2; the qualification harness, not yet built). **Please check this independently (Q3).**
2. **Records made before the repair.** None exist: no job has been run.
3. **The qualification.** Row 15's reference state is computed by §7's order with the evaluator's cause "not an input to the reference". With the old ordering, a constant-index case whose sample map was not informative would have been counted an error. The repair removes that; it changes no qualification rule.
4. **Identity pins.** Four later test files pin `evaluator.py`'s identity, so three of them change with it (the fourth, M6 part 2's, is not placed). This is the pins working as designed, and it is why one two-branch exchange touches five files.

## 5. Evidence

- `build_records/f9_m1_to_m6_container_evaluator_repair_2026-11-23.txt` (`a87b028d1f9c89e80d3e2ff0e696c22c559fd76715f727b9008ef9bf675f87e9`) — the six placed Flight 9 test files in one process on the repaired bytes, in L1's container (Python 3.13.18, numpy 2.5.3): **277 passed in 726.87 s (276 as placed, and the one new test)**.
- `build_records/f9_evaluator_precedence_repair_2026-11-23.diff` (`4b3868853455e9027171e6e2276ae53c0028e292bf85d38710010ca54646793c`) — `git diff` of the working tree against the pin.
- `build_records/l2_m6b_round1_reproduce.py` (`6c93b4ba29f784547b0b7bbc87c7f5974e1e875aa4dbc6e1dde8eb501ea4cb98`) — your Appendix R, extracted byte for byte from the received review. It needs M6 part 2's module, which is not in this packet's instrument tree; `build_records/f9_evaluator_repair_placed_routes_2026-11-23.txt` (`21abdef71dd9fed456eb031946b9f343c21aa097b2eaf72ec130d1c893a58839`) is L1's run of its three maps through the placed route only (`evaluate_level`, T0 families), before and after: before, the map's cause on all three; after, `no eligible contour` on all three, with the same point cells and bonds.
- To run: from `flights/mfa_fidelity/instrument`, `python -B -m pytest tests/test_f9_m3.py -v -p no:cacheprovider` (38 tests; it builds the identity bundle and takes some minutes).

## 6. Questions

**Q1. The change boundary.** Is the change in each of the five files confined to what §2 states? An inverse-edit reconstruction of the five pinned identities from the repaired bytes would settle it; `packet_only/before/` has the pin's bytes.
**Q2.** Is the repaired ordering §7's for the level tier as far as `evaluate_level` decides it (L2 before L3 and L4; apparatus validation before any returned record)? Is there another place in the placed evaluator, or in `evaluate_map`, where a constant index can receive a cause other than `no eligible contour`?
**Q3.** Does the repair change any result, typed draw, point record or stream on any input, other than the cause of an empty-family index on a non-informative map? Does anything in the placed `outcomes.py`, `closure.py`, `t0.py` or `reports.py` behave differently because of it?
**Q4.** Is the new test discriminating and complete for the crossed states? Is a state missing (for example an empty family on a level that would be unstable, L5, where the family is empty and no draw is made)?
**Q5.** Is the deferral of the two cause strings, as stated, consistent with the repair being sound on its own?
**Q6.** The two wording repairs in `test_f9_m6.py`: do they say what your M6 round-2 notes asked?
**Q7.** Anything else.
