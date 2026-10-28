# L2 → L1 — Flight 8 M2/M3 Round-2 Build Review — 2026-10-27

**Register:** instrument build review, frozen Contract F8 v0.8.4 (`e87277a2d11e948f`), freeze record (`16869692a043b139`). **Verdict: DEFECT-WITH-REPAIR (qualification hold; D1 and D2 source repairs accepted).** No placement, production run, or acceptance of the failed validation is authorized by this review. Mike retains decision authority.

## 1. Received identities

Round-2 response `ba4f4deac0cf230a`, `f8/null.py` `349cfa77ddd24fcd`, `tests/test_f8_m2_m3.py` `e4a3752e97525fd0`, frozen contract `e87277a2d11e948f`, all independently recomputed SHA-256 prefixes. The archive has 41 files (excluding directory entries). The change statement reports `classify.py`, `dynamics.py`, and `test_f8_m1.py` unchanged.

## 2. Independent execution

From `flights/mfa_fidelity/instrument` in the extracted archive:


**Repeat execution note (same archive, this request):** A fresh invocation of `python -m pytest tests/test_f8_m2_m3.py -q` was attempted but reached the execution time limit after 14 progress dots; this partial execution is not counted as a complete run. A fresh `python -m pytest tests/test_f8_m1.py -q` completed with **65 passed, 4 failed in 1.94 s**, reproducing precisely the four `pyarrow`-dependency failures described below. The 29/1 M2/M3 figure below is from the earlier completed execution of this same extracted archive, not from the timed-out repeat.


- `python -m pytest tests/test_f8_m2_m3.py -q`: **29 passed, 1 failed in 61.06 s**. The failure is `test_f8_m2_m3_do_not_touch_e1`, importing `mfa_instrument/e1/config.py`, because **`pyarrow` is not installed**. The 29 passing tests include the D1/D2 checks. Expected 30/30 is **not independently established**.
- `python -m pytest tests/test_f8_m1.py -q`: **65 passed, 4 failed in 2.36 s**. Failures: `test_e1_frozen_panel_is_not_reused`, `test_rho_table_roundtrip`, `test_f8_does_not_touch_e1_identities`, `test_d4_panels_checked_against_the_actual_retired_e1_panel`. All show `ModuleNotFoundError: No module named 'pyarrow'` (direct use in Parquet writing or import of E1 config). Expected 69/69 is **not independently established**.

These five environmental failures are not source nonconformance findings. Canonical execution with dependencies installed and both suites passing remains an acceptance condition.

## 3. D1 repair — ACCEPTED as an implementation repair

The earlier invalid assumption was that 10 consecutive windows from the same Markov trajectory furnished 10 independent observations. The revised `validate_on_stepper` now computes:

1. **Designated terminal window:** one independently seeded replicate observation per trajectory, DKW threshold `sqrt(log(2/0.05)/(2*n_replicates))`.
2. **Ten-window union diagnostic:** ten separately calculated empirical CDF deviations, each from the *same-index window across independent replicates*, with per-index threshold `sqrt(log(2/(0.05/10))/(2*n_replicates))`. The union bound requires no independence between window indices.
3. **Pooled deviation:** explicitly descriptive and unbounded; it is no longer falsely called i.i.d.-DKW qualification.

`NullValidation.__post_init__` rejects the earlier pooled `10*n_replicates` DKW bound, inconsistent pass flags, p-value and union bound. The updated tests discriminate these cases and demonstrate nonzero adjacent-window dependence. These changes repair the Round-1 D1 computational/statistical defect.

**Precision of interpretation:** `dkw_p_value` is the DKW *upper bound* on a null tail probability, not an exact p-value; a value around 0.0073 suffices to reject at nominal 0.05 but cannot be called an exact probability. For the joint rule 'both tests pass,' do **not** claim a combined 0.05 false-failure rate: the individual tests each have up-to-0.05 false-failure guarantees and the simple upper bound for their union is 0.10. If the program wants an overall 0.05 simultaneous goodness-of-fit criterion, allocate alpha between checks prospectively or use one test as the prespecified primary gate and the other as supplementary evidence.

## 4. D2 repair — ACCEPTED

For grid < 50 the code now derives `theta_p_used` and `theta_t_used` from the **scaled-grid** CDF and its conservative error allowance, rather than applying full N=2500 cutoffs to a reduced-grid null. Its `thresholds_scope` is `smoke_scaled_grid`; the production path uses cached thresholds and `production_cache`. `is_qualification_evidence()` excludes smoke scope. Regression tests require scope/quantile differences and refuse forged scope. This addresses D2 without changing production-grid thresholds. **A scope-eligible record is not automatically a passing qualification record:** `is_qualification_evidence()` currently signals only production scope.

## 5. The decisive qualification-statistic ruling

For the **already observed 400-replicate record**, the predesignated terminal-window DKW comparison is the primary inferential check of the terminal statistic `S_term`. The ten-window union comparison is a valid, useful **additional** inferential check of all ten marginals, but it is not a post hoc replacement for a failed primary test. This preserves the predesignated terminal window and prevents outcome-conditioned selection of the more permissive test. The following must all remain on the record:

| Statistic | Observed | Threshold | Ruling |
|---|---:|---:|---|
| Designated terminal-window DKW | 0.0837 | 0.0679 | **FAIL** (reported bound p ≈ 0.0073) |
| Ten-window per-index union | max ≈ 0.084 | 0.0865 | **PASS** |
| All-windows pooled deviation | 0.0159 | None | Descriptive only |

The **400-replicate validation as submitted FAILS qualification**. The passing union result cannot erase the failing designated result. The contract (§2.9 and §4.3) defines the null and thresholds and the freeze record requires an M3 cache to be built and qualified before downstream execution; neither grants permission to switch the qualification decision after observing data. The exact transfer-matrix/independent-cell law and its conservative familywise bound do **not** thereby become invalid, nor does this constitute an adverse finding on the theory. This is a failure of the submitted finite-sample validation qualification, not necessarily of the null law.

**Prospective policy recommendation:** Treat the designated-window comparison as the **primary pass/fail statistic**, with the union check a separately reported auxiliary check; a failed union check would also deserve investigation, but do not describe a two-check intersection as a single α=0.05 test. If Mike instead prospectively requires **both** for future qualification, that is a defensible stricter acceptance policy *provided its joint error interpretation is correct and the requirement is fixed before a new dataset*. Under either primary-designated or both-required policy, the already observed 400-replicate record fails. Union-only retroactive acceptance is rejected.

## 6. Outstanding hold and narrowly defined repairs

**H1 — Failed qualification (blocking):** Keep master `220261026`, n=400, the terminal-window FAIL and union PASS as an immutable disclosed record. Do not replace, silently pool, reclassify, or rerun it as though it never occurred. If qualification is to be retried, approve **before executing** a new validation identity and fixed protocol (sample size, master/derivation, test statistic(s), alpha/error budget, reporting convention, decision rule, treatment of the original failed attempt). A proposed n=1000 validation must be genuinely new and prospectively registered; using the same master to extend the already inspected sample does not by itself create an independent clean confirmatory test. Report any new outcome, pass or fail, and retain the earlier failure. An alternative is a separately justified deterministic/exact-law validation route, again approved before reliance on it.

**H2 — Canonical regression verification (blocking):** Execute 30/30 M2/M3 and 69/69 M1 tests in an environment with `pyarrow`; record the environment and command outputs. No source changes are demanded for the five dependency failures observed here.

**H3 — Qualification record grammar:** In subsequent governance/ready checks, explicitly distinguish `production_scope_eligible` from `qualification_passed`; require the chosen registered statistical decision and supporting validation identity. The existing `is_qualification_evidence()` method must not be misused to imply passage merely because `grid == 50`. This is an integration/acceptance safeguard, not a claim that D1/D2 source repair failed.

## 7. Final disposition

**DEFECT-WITH-REPAIR**, limited to the **failed qualification/acceptance evidence and pending full-environment test verification**, not a rejection of the D1/D2 source patches. D1: repaired. D2: repaired. M1-r3/M2-1 prior substantive clearance unchanged. M3 remains **not qualified** on the reported 400-replicate record. No placement and no canonical scientific run authorized. A future SOUND review requires a valid precommitted qualification passage and complete canonical regression evidence; no silent seed change or reinterpretation of the failed designated statistic is permitted.
