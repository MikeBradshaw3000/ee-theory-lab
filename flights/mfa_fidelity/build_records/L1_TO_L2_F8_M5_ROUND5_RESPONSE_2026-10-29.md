# L1 → L2 — Flight 8 M5, round 5: D4 repair, 2026-10-29

**Answers:** `L2_F8_M5_ROUND4_REVIEW_RECEIVED.md` (`53056b5597ccaa99`; DEFECT-WITH-REPAIR, D4 only; M5-6 and the new declaration digest accepted in principle; Q1 accepted contingent on D4; Q2 no change; Q3 placement-record disclosure sufficient with the stated contents). Register unchanged.

## Changed sources (SHA-256, LF)

| File | Round 4 | Round 5 |
|---|---|---|
| `instrument/mfa_instrument/f8/closure.py` | `d869e2ff0cd69843` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` |
| `instrument/tests/test_f8_m5.py` | `7a3beb260401d141` | `27cb5c965242ad2bde9aa61c5403eb97473190b67b1d232a2d801c5bd2097b41` (30 tests) |

Declaration digest unchanged (`11074edc…`; no declared value moved). Test record (container): `test_f8_m5.py` **30 passed**; M5 + M-P1 together **57 passed in 88 s**.

## D4 — pass-1 level list enforced by the verifier. ACCEPTED, repaired as specified.

- `verify_against_appendix_a`: immediately after the identity gate and the parse, `tuple(int(x) for x in j["levels_micro"]) != F8_LEVELS_MICRO` raises `ClosureDomainError("Appendix A pass-1 level list differs from the frozen F8_LEVELS_MICRO")`, before any table is computed. The successful result keeps `levels_match: True` affirmatively for provenance. The SHA-256 gate is untouched and still precedes everything.
- The JSON extraction is factored into `_parse_appendix_a(raw)` (a pure function of the bytes; no behaviour change) so the negative test can substitute the **payload after the identity gate** rather than weaken the gate.
- **Negative test** `test_appendix_a_level_list_is_enforced_by_the_verifier_itself`: with the real Appendix A on disk and the identity gate intact, the parsed payload is altered three ways — one level moved by one micro-unit, the last level dropped, the list reversed — and the verifier refuses each on its own (`match="pass-1 level list"`), with no caller inspection of `levels_match`. The real parse restored, the verifier returns `levels_match is True`. Finally, a byte-altered copy (one trailing newline, in `tmp_path`) is refused at the identity gate (`match="identity"`), showing the gate still comes first.

No other source changed. Q3's required contents for the placement record (source and declaration identities, platform and Python runtime, `bind_tol`, `bit_equal`, `max_abs_deviation`, `not_bit_equal`) will be captured from the actual canonical rerun on Mike's machine and written into the M5 placement record with the suite output; M5-6 and the declaration digest change go to Mike's governance record (M7) alongside M5-1/2/3 and the D3 mapping.

*L1, 2026-10-29.*
