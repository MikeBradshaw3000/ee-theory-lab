# L1 → L2 — Flight 8 M5, round 4: placement finding and repair of the Appendix A binding, 2026-10-29

**Why this round exists.** L2 cleared M5 SOUND in round 3 (`L2_F8_M5_ROUND3_REVIEW_RECEIVED.md`, `7f5eb9ea…`). At placement, the canonical suite on Mike's machine (Windows 11, Python 3.14.4, HEAD `2f5b17e` + the eight M5 paths) returned **1 failed, 722 passed, 2 skipped** (suite output `f8_m5_suite_2026-10-28.txt`). The failure is `test_m5_binds_to_appendix_a_bitwise`: `verify_against_appendix_a` raised *"Appendix A rho_sk table differs from M5 (bitwise)"*. Nothing was committed. Per protocol a source change after SOUND returns to L2 before placement; this is that packet. Register unchanged.

## The finding (diagnostic run on the canonical machine, `f8_m5_diag.py`)

| Quantity | Result on Mike's machine vs the committed Appendix A |
|---|---|
| `rho_sk` table (24 levels) | **1 level differs**: m = 1.619565, M5 `0.3502605538099093` vs A `0.35026055380990934`, |Δ| = 5.551e-17 (one ulp) |
| `rho_re` table (24 levels) | 0 levels differ |
| Δm lower / upper / s / value | all four equal; value `0.120126265992375` |
| m_infl, m_lat | equal (`1.1765`, `1.1414478323100217`) |
| `math.exp(-0.2)`, `math.exp(-0.01)` | repr identical to the container |

**Cause.** The fixed point iterates `g_map` through `math.exp`, which is the platform's C library — glibc in the container that produced Appendix A and runs L1's tests, Microsoft UCRT on the canonical machine. Correctly-rounded `exp` is not guaranteed by either; for some arguments they differ by one ulp. Appendix A's iteration stops at |Δ| < 1e-15, so a one-ulp difference inside the loop can surface as a one-ulp difference in the returned iterate. The procedure and float64 expression order are the same; the claim "bit for bit" was L1's overstatement — it is true on the producing platform and ≤ 1 ulp elsewhere, and the instrument must say what is true on every platform it may run on.

**What was not affected.** Every §3.4 quantity, Δm, m_lat, m_infl, the closure publication's content, and all other 722 tests. The deviation is 5.6e-17 on a density of 0.35 — eleven orders below the smallest band the instrument will ever compare against (ŝ ≈ 0.01 → band ≈ 0.012).

## The repair (SHA-256, LF)

| File | Round 3 (cleared) | Round 4 |
|---|---|---|
| `instrument/mfa_instrument/f8/closure.py` | `3d4dd9df96780e57` | `d869e2ff0cd69843b0e7b15fd811e5e917b6b7674fcd862708600ebd645b1441` |
| `instrument/tests/test_f8_m5.py` | `213a4cc8cd1037b9` | `7a3beb260401d14183dc24e54e99e11079a31aa5ff63ea87c807b7bb9b6acef0` (29 tests) |

1. **New declared constant `APPENDIX_A_BIND_TOL = 1e-12`** (absolute), entered in `CLOSURE_DECLARATION` as `appendix_a_bind_tol` and checked live; the declaration digest therefore moves (`e2c48a1b…` → `11074edc…`). This is a new declaration, **M5-6**, for L2 and for Mike's governance record.
2. **`verify_against_appendix_a`**: the Appendix A **identity stays exact** (frozen SHA-256). The `rho_sk` and `rho_re` tables (keys must be the same 24 levels), Δm's four fields and m_lat must agree within `APPENDIX_A_BIND_TOL`; **m_infl (a grid value) and π₁ stay exact**. The result now reports `bind_tol`, `max_abs_deviation`, `not_bit_equal` (the keys that differ at all) and `bit_equal`, so a placement record states what the machine saw instead of a bare pass. A deviation beyond the tolerance raises with the offending keys named.
3. **Tests.** The binding test asserts identity, levels, Δm within tolerance, m_infl exact, and `max_abs_deviation ≤ 1e-15` (a few ulp on any platform's libm — far tighter than the declared 1e-12, so a real arithmetic change is still caught; the 1e-12 is the instrument's refusal line, the 1e-15 is the test's). A new test proves the tolerance is operative in both directions on any platform: a +5e-13 perturbation of `rho_sk` above m = 1.5 binds with `bit_equal = False` and the perturbed keys listed; +2e-12 is refused with the keys named; a one-ulp perturbation of m_infl is refused (exact). The perturbation is confined to m > 1.5 so Δm's bisection (near m ≈ 1.02) is untouched and the measured deviation is the injected one.

Test record (container): `test_f8_m5.py` **29 passed**; M1 + M4 + M5 + M-P1 together **142 passed in 90 s**. In the container the binding reports `bit_equal = True, max_abs_deviation = 0.0`; on Mike's machine the placement record will carry `bit_equal = False`, one `rho_sk` key, 5.551e-17 — both are passes under the same declared rule.

## Questions for L2

- **Q1.** Is 1e-12 the right refusal line, or should the declared tolerance be tied to the fixed-point stopping tolerance (e.g. 10 × FP_TOL = 1e-14)? L1 chose 1e-12 as a round value that is still ~10⁹ below any band the instrument compares against, with the test's 1e-15 as the tight check; L2 may prefer the tighter declared value.
- **Q2.** Does L2 want the same disclosure extended to M1's `verify_against_appendix_a` (which checks Δm to 5e-5 and the level list exactly — already tolerance-based) or M3's π₁ row (exact; passed on both platforms)? L1 reads both as already correct.
- **Q3.** Should `bit_equal` and `max_abs_deviation` be carried into the closure publication's record so the canonical job's provenance names the platform's libm behaviour, or is the placement record's statement sufficient?

Nothing else in `closure.py` changed; M-P1 (`evaluator.py`, not yet routed) imports the new `closure.py` and its 27 tests pass against it; its packet will be re-issued with the new identity before routing.

*L1, 2026-10-29.*
