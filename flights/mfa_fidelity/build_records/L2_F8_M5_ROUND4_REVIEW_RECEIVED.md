# L2 — Flight 8 M5 Round 4 repair review (2026-10-29)

**Register:** Instrument build review, frozen Contract F8 v0.8.4 (`e87277a2d11e948f`); no placement or run authorized by this review.

**Verdict: DEFECT-WITH-REPAIR.** The tolerance repair itself is directionally correct, but an exact pass-1-level identity obligation is not enforced as an acceptance condition (D4). This is a narrow, actionable source defect.

## 1. Archive reconciliation and identities

Archive `f8_m5_round4_L2.zip` contains **42 regular files** (all 42 listed archive entries are files). The previous 41-file count was incorrect; there is no missing file. The last listed file is `flights/mfa_fidelity/build_records/f8_m5_diag.py` (entry 42). The round-4 packet is `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M5_ROUND4_RESPONSE_2026-10-29.md`.

The packet declares SHA-256 `d869e2ff0cd69843b0e7b15fd811e5e917b6b7674fcd862708600ebd645b1441` for `closure.py` and `7a3beb260401d14183dc24e54e99e11079a31aa5ff63ea87c807b7bb9b6acef0` for `test_f8_m5.py`; the review uses these enclosed sources.

## 2. Independent test and digest evidence

Ran, from `flights/mfa_fidelity/instrument`:

```sh
python -m pytest tests/test_f8_m5.py -q -k 'appendix_a or tolerance or identity or tamper'
```

**9 passed, 20 deselected, 7.36 s**. The new `test_appendix_a_tolerance_is_operative_in_both_directions` passes in this environment (inside-tolerance `+5e-13`, outside-tolerance `+2e-12`, and exact `m_infl` negative). This is a targeted selection, *not* evidence for a full 29-test module or a canonical Windows execution.

Recomputed `hashlib.sha256(repr(CLOSURE_DECLARATION).encode()).hexdigest()` independently, obtaining:

`11074edcacbe26d2fe3b33eff4f7fca4a328a5d7b9dcd84786d2f115206ce204`

This matches `CLOSURE_SHA256_LITERAL` exactly. `verify_frozen_identity()` also completed without error.

## 3. Repair assessment

- **Appendix A identity:** Exact SHA-256 comparison of the file bytes against the frozen `F8_APPENDIX_A_SHA256` is maintained before parsing or accepting its values. **SOUND.**
- **Tables and scalar tolerance:** Both 24-key `rho_sk` and `rho_re` tables reject key-set mismatches and test each value against absolute `APPENDIX_A_BIND_TOL`; all four fields `delta_m.lower`, `.upper`, `.s`, `.value` and `m_lat` likewise use this tolerance. Exceedance raises with offending metric names. The returned `bind_tol`, `max_abs_deviation`, `not_bit_equal`, and `bit_equal` expose deviations. **SOUND as to those comparisons.**
- **`m_infl` and π₁:** Both are compared by exact floating-point equality; a one-ulp `m_infl` mutation is rejected by the new negative test. **SOUND.**
- **Pass-1 levels:** `tuple(int(x) for x in j['levels_micro']) == F8_LEVELS_MICRO` is merely returned as `levels_match`; it is **not checked as a precondition for successful binding**. This contrasts with the function's stated requirement that pass-1 levels be equal exactly. **D4.** The frozen Appendix A hash reduces practical exposure to this omission, but it does not make the advertised verifier predicate complete, nor does it justify a successful return carrying `levels_match=False`.

### D4 — Enforce exact pass-1-level identity as a binding predicate

**Finding:** `verify_against_appendix_a` can return successfully even when its computed `levels_match` is false. A caller that does not separately enforce the diagnostic flag would treat the bind as successful. The test currently checks `levels_match` at its own call site, but the function must itself enforce the claimed obligation.

**Required minimal repair:** After parsing Appendix A and before any successful return, require `tuple(int(x) for x in j['levels_micro']) == F8_LEVELS_MICRO` and raise `ClosureDomainError` on mismatch. Preserve an affirmative `levels_match=True` in the successful result, if desired for provenance. Add a discriminating negative test that supplies a level mismatch *after an otherwise valid identity gate* (e.g. mocking the approved parse payload in an isolated test rather than weakening frozen identity verification), and verify a failure from the verifier itself. Do not relax the SHA-256 gate. No unrelated source changes are requested.

## 4. Answers to L1 questions

**Q1 — 1e-12 refusal tolerance:** **Accepted for M5-6, contingent on D4.** A declared absolute tolerance is appropriate for cross-platform `math.exp` variations, and the independent test's `max_abs_deviation <= 1e-15` asserts a much stricter ordinary-platform replay expectation. The 1e-12 bound is a refusal limit, not a claim that routine differences are that large. Do not describe it as bitwise Appendix A equality. The tolerance and changed declaration identity must be registered explicitly in governance.

**Q2 — M1 and M3:** **No corresponding source change required by this M5 finding.** M1's Appendix A comparison was already tolerance-based on Δm with exact pass-1 levels, and M3's exact π₁ comparison passed on both reported platforms. This ruling does not authorize relaxing those existing checks. If future cross-platform evidence shows a mismatch there, route it as a distinct review, not a silent consistency edit.

**Q3 — Provenance disclosure:** **Placement-record disclosure is sufficient**, provided that the canonical record is immutable/retained alongside the placement and includes the source/declaration identities, platform and Python runtime, `bind_tol`, `bit_equal`, `max_abs_deviation`, and `not_bit_equal`. There is no present requirement to change the closure publication's content identity for host-libm differences; the publication is a replayable machine result and the placement record is the proper provenance carrier. If the placement record is not durably linked to that publication and canonical job, then that linkage and disclosure must be added before placement. The Windows outcome described by L1 must be captured from the actual canonical rerun, not copied as assumed evidence.

## 5. Disposition

**DEFECT-WITH-REPAIR — D4 only.** M5-6 tolerance and digest accepted in principle; exact pass-1-level enforcement is the remaining correction. D1–D3's previous rulings are unchanged. No placement or canonical execution is authorized by this review. Return a minimal D4 repair and a negative test for L2 re-verification.
