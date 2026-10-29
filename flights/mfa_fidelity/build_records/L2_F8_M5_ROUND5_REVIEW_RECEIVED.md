# L2 — Flight 8 M5 Round 5, independent repeat verification

**Register:** F8 instrument build, Contract F8 v0.8.4 (frozen). **Scope:** D4 repair only. **Verdict: SOUND.** This is an independent inspection of the newly supplied `f8_m5_round5_L2(1).zip`, not a new authorization for placement or execution.

## 1. Receipt

42 regular archive entries. SHA-256 prefixes, calculated directly from archive members:

| Repo-relative member | SHA-256, first 16 hex | Result |
|---|---|---|
| `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M5_ROUND5_RESPONSE_2026-10-29.md` | `0f90aad0281d4f69` | Received/read |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350ab` | Matches response |
| `flights/mfa_fidelity/instrument/tests/test_f8_m5.py` | `27cb5c965242ad2b` | Matches response |

## 2. Tests

From `flights/mfa_fidelity/instrument` after extracting the supplied archive:

```console
python -m pytest tests/test_f8_m5.py -q -k "appendix_a or tolerance or identity or tamper or level_list"
..........                                                               [100%]
10 passed, 20 deselected in 9.39s
```

This is direct evidence for the requested selection, **not** independent execution of the full 30 tests. L1 reports the full 30 passed on its container.

## 3. D4 source inspection

`verify_against_appendix_a` checks the raw Appendix A bytes' SHA-256 against the frozen identity **before** `_parse_appendix_a(raw)`. Immediately after parsing it compares the entire parsed `levels_micro` sequence, converted to integers, against `F8_LEVELS_MICRO` as an exact tuple. Any mismatch raises `ClosureDomainError` with text identifying the *pass-1 level list*, before the tables and tolerance comparison. A successful call reports `levels_match: True` only after enforcing that predicate.

The negative regression `test_appendix_a_level_list_is_enforced_by_the_verifier_itself` temporarily substitutes the parsed payload **after** the unmodified SHA gate, testing (i) a one-micro-unit level modification, (ii) a dropped final level, and (iii) reversed level order. Each must raise the verifier's own `ClosureDomainError`. It then restores real parsing and checks a valid call succeeds, and confirms an altered on-disk Appendix A is rejected by the identity gate first. These are discriminating negatives for the precise Round-4 finding.

The numerical guard remains scoped as previously accepted: `APPENDIX_A_BIND_TOL = 1e-12` on the two fixed-point tables, `delta_m` fields (`lower`, `upper`, `s`, `value`) and `m_lat`; `m_infl` and `null.pi1` remain exact checks. The new level-list guard is independent of that tolerance.

Independently recomputed `sha256(repr(CLOSURE_DECLARATION).encode())`:

`11074edcacbe26d2fe3b33eff4f7fca4a328a5d7b9dcd84786d2f115206ce204`

This equals `CLOSURE_SHA256_LITERAL`; the declaration identity is unchanged.

## 4. Verdict and boundary

**D4 CLOSED — SOUND.** The substantive defect (reporting but not enforcing exact pass-1 levels) is repaired and tested. No new source defect was found in this narrow review. Earlier Q1/Q2/Q3 rulings stand, including actual-platform disclosure requirements for the placement record. Full canonical suite evidence, governance ratification and placement/integration controls remain separate obligations. **This review does not authorize placement or production execution.**
