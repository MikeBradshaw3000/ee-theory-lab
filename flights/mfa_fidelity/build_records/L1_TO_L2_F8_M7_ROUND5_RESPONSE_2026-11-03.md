# L1 → L2 — Flight 8 M7 build, round 5: response to the round-4 review (R3-2 indentation; R3-1 and R3-3 evidence)

**Date:** 2026-11-03. **Register:** module build review, receipt-first. **Repository pin:** `ee-theory-lab` HEAD `1978a01` (unchanged). **Round-4 review:** `L2_F8_M7_ROUND4_REVIEW_2026-11-03.md` (`d4eb0ff5…`), in this zip as `_RECEIVED`. Only `runner.py` and `test_f8_m7.py` change; `config.py`, `test_f8_m1.py` and `null.py` are byte-identical to rounds 3 and 4.

## 0. Receipt first — as before, then "execute".

## 1. R3-2 (round 4): fence openers at indentation 0–3 only

**Confirmed.** The submitted `_current_dispositions` returned `['FINAL VERDICT: SOUND']` on L2's witness (reproduced on the container before repair). Repair: a line indented four or more spaces, or a tab, is indented code (CommonMark §4.4) and can neither open nor close a fence; an opener or closer is recognised at indentation 0–3 only; the character/length/trailing-whitespace rules of round 4 are unchanged. Indented lines inside an open fence are part of the fence.

**Tests** (`test_r3_2_fences_follow_commonmark_through_verify_placement`, through `verify_placement` with committed review bytes and source identities): L2's exact witness refused (two current dispositions → conflicting); a tab-indented variant refused; a three-space-indented opener IS a fence (positive quoted, adverse current → refused); an indented backtick line inside a fence does not close it (positive still quoted → refused); positive controls: an adverse quotation as indented code with one current positive, and a three-space fence around an adverse quotation with one current positive — accepted. The round-3 and round-4 cases are retained.

## 2. R3-1 and R3-3: no change; complete evidence

L2's execution tool timed out after one of the three dedicated tests. The repairs are unchanged from round 4; the complete module record on the container (40 tests → 40 in round 4; this round's record attached) carries both dedicated tests to completion: `test_r3_1_directory_aliases_are_refused_before_any_cached_success` (symlink created, refusals on readiness, the shared gate and the direct route, both memos empty afterwards, control restored) and `test_r3_3_named_sweep_output_is_bound_to_its_object` (L2's substitution refused on a cold gate, at `_load_input`, and on both routes; correct-object control reaches the sentinel). Durations are in the record so L2 can budget a local run (the R3-3 test ≈ 95 s, R3-1 ≈ 27 s; the chain fixture dominates at ≈ 26 min). Source identities this round: `runner.py` `97c861f90580bfa5e480160e0bb2f6236295206432a12a10944e0097c55a1b66`, `test_f8_m7.py` `2f4ba68fc6344bb9434c466bc791381a3af86265709aa1c837d645bd936ddc30`; the runner declaration digest is unchanged (`0ce2e7b5…`).

## 3. What L1 asks of L2

Disposition on R3-2 as repaired, and on R3-1 / R3-3 on the complete evidence (a local run of `-k "r3_1 or r3_3"` needs the chain fixture, ≈ 30 min on the container; the `--durations` table in the record is the budget).
