# L2 — Flight 8 M7 module build review, round 4

FINAL VERDICT: DEFECT-WITH-REPAIR

**Register:** Module build review; decision authority Mike. **Repository pin declared:** `1978a01`; M7 and M1 touch unplaced. **Receipt:** `f8_m7_build_round4_L2.zip`, SHA-256 `704c664b8313d4dfb94bd1ce057f493ee00d9e861d3338455b34722c80c35a58`; 86 payloads plus MANIFEST.txt; all 86 declared payload digests matched. Full file-level receipt is in `F8_M7_ROUND4_RECEIPT.md`.

**Reviewed source identities:** `instrument/mfa_instrument/f8/runner.py` SHA-256 `ef93cedbf5a3d8be55815c09782fc0f2bbf6f0973b4ce8a4fbf975756f826f31`; `instrument/tests/test_f8_m7.py` SHA-256 `843a528045b9ee74ecec78f1c0091908188c415a120f68043987658354ff9ca8`. The submitted round-3 review identity is `57894473179ae92c90689aed378696c4c720cfc456ec6d5c9edb3e25f11e0f7e`.

## Disposition

- **R3-1 — provisionally repaired in source, not fully test-qualified.** `_walk_no_links` rejects file/directory aliases below traversed roots; `_real_file` checks path components. The dedicated integration test includes cold-memo refusal and control restoration. The complete dedicated test did not finish in this review environment. No final R3-1 qualification is claimed.
- **R3-2 — DEFECT REMAINS (new concrete clearance bypass).** The repair correctly tracks the opening fence character and minimum closing length, but `_current_dispositions` recognizes a fence opener at **any indentation**, whereas CommonMark fences can be indented at most three spaces. A four-space-indented backtick line is indented code, not a fence opener. As a result, an unquoted adverse current verdict can be suppressed after an apparent indented opener. The exact submitted function returns `['FINAL VERDICT: SOUND']` for:

  ```text
  FINAL VERDICT: SOUND
      ```
  FINAL VERDICT: DEFECT-WITH-REPAIR
      ```
  ```

  In this example the four-space-indented backtick lines are indented-code material, so the intervening column-zero adverse disposition is current and must conflict. The parser instead enters a fence at the first indented backtick line, suppresses the adverse line, and closes at the second. This is a direct false-clearance counterexample, demonstrated by calling the unmodified submitted `_current_dispositions` function. Since `verify_placement` accepts precisely the singleton `['FINAL VERDICT: SOUND']` when its other checks are satisfied, this is a clearance-gate defect. **Repair:** recognize opening fences only with indentation 0–3, and distinguish indented-code lines from fenced-code lines. Add a discriminating `verify_placement` test using committed review bytes, the exact witness above, and a valid positive control. Test mixed indentation and closing fence conditions as well.
- **R3-3 — provisionally repaired in source, not fully test-qualified.** The named-output mapping and binding check appear at the shared dependency gate and loader; the dedicated test exercises the cross-object substitution and direct/public routes. The dedicated test did not complete locally. No full R3-3 qualification is claimed.

## Execution evidence and limitations

Source was inspected directly from the verified archive. The focused invocation was `python -m pytest tests/test_f8_m7.py -q -k 'r3_1 or r3_2 or r3_3' --disable-warnings --maxfail=1` from `flights/mfa_fidelity/instrument`. One test passed before the execution tool timed out; no completed pytest summary, final exit status, or complete M7 test pass is claimed. The independent R3-2 parser witness ran to completion and produced the singleton positive disposition above. No canonical suite or actual placement was executed. The round-3 M1 a′ component disposition is not reopened; no new independent verification of the unchanged M1 bytes is claimed here.

**Required next submission:** correct R3-2's opening-fence indentation grammar and provide a committed clearance-path negative and positive control, with source identities and complete test evidence. Retain R3-1 and R3-3 protections. **No placement clearance is granted.**
