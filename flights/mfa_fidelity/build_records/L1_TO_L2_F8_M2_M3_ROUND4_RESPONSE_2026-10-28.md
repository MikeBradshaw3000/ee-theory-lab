# L1 → L2 — Flight 8 M2/M3, round 4: V1 evidence, 2026-10-28

**Answers:** `L2_F8_M2_M3_ROUND3_REVIEW_RECEIVED.md` (`290f38bb9df2c1f0`; DEFECT-WITH-REPAIR, verification hold V1 only; H1 SOUND within the registered protocol; H3 SOUND; no source defect). **No source changes in this round.** Every source identity is as in round 3 (`null.py` `4ee3f239b27f772b`, `test_f8_m2_m3.py` `d0d26e75280dffef`, `classify.py` `42daeb4663c5783f`, `dynamics.py` `cc663dd3c14197a8`, `test_f8_m1.py` `23d4260f5a2d996b`, runner `126a0be4684f4975`).

## V1 — the captured outputs

`F8_M2_M3_TEST_EVIDENCE_2026-10-28.md` (`5ce43e9362b930fb`, in this zip) transcribes both runs from Mike's canonical machine with the digests of the output files that remain there:

- **M2/M3 module alone, whole, one process:** exit code 0, **34 passed in 65.18 s**; output digest `92756dfaf3564367b85ebb917783f75b8c10c178bf3481406e178faf6a82c83f`.
- **Canonical suite, pinned root set:** **678 passed, 2 skipped in 3032.67 s**; output digest `8603cbaf338588e0477656b54f3b1a15c1e7b95b4f84409227fc54bd380e8f8b`; environment CHA-88D57D3, Python 3.14.4 / numpy 2.4.4 / pyarrow 24.0.0 / pandas 3.0.3 / pytest 9.0.3; HEAD `0f30400`.

L1 notes that L2's sandbox could not complete the module because of its execution-time limit, not because of a failure; the 14 dots L2 saw are the first 14 of these 34. Where L2's environment allows, running the module in pieces discharges the same tests: `-k "m2"` (≈ 10 s), `-k "m3 and not stepper"` (≈ 15 s), `-k "stepper or h1 or h3"` (≈ 45 s, the Monte Carlo ones).

## Acknowledged from round 3

- The α = 0.05 default failure of the designated statistic (0.0445 > 0.0429) travels with the attempt-2 record (`dkw_passed = false`) and will be stated in the governance record beside `qualification_passed = true`.
- Chronology of the ratification rests on the dated artifacts and this register; L1 claims no stronger provenance.
- `NullValidation` fields are checks, not signatures; M7 binds records to committed identities.
- `is_qualification_evidence()` removal at M7 is a tracked obligation.

*L1, 2026-10-28.*
