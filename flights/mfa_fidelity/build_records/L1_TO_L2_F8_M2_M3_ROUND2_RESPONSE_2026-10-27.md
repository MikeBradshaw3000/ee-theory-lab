# L1 → L2 — Flight 8 M2/M3, round 2: response to the round-1 review and changed-source packet, 2026-10-27

**Answers:** `L2_F8_M2_M3_ROUND1_REVIEW_RECEIVED.md` (`9f85b8c59c89ddb1`; DEFECT-WITH-REPAIR, D1–D2; M1-r3 and M2-1 cleared subject to regression; M3-1…M3-5 qualified). Register unchanged. This zip carries the whole package, the contract files and both test modules, as before.

## Changed sources (SHA-256, LF)

| File | Round 1 | Round 2 |
|---|---|---|
| `instrument/mfa_instrument/f8/null.py` | `b18b935fb5d1657e` | `349cfa77ddd24fcd2d5d1ad1edfc791590d1afeafdcf812d70b2ff1d3914b86a` |
| `instrument/tests/test_f8_m2_m3.py` | `86bb33610ae31ffc` | `e4a3752e97525fd0927359d280ebce70f5cbc29576c81474a8e694c101810b9b` |
| `instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783f` | unchanged |
| `instrument/mfa_instrument/f8/dynamics.py` (M1-r3) | `cc663dd3c14197a8` | unchanged |
| `instrument/tests/test_f8_m1.py` | `23d4260f5a2d996b` | unchanged |

Test record (container): `test_f8_m2_m3.py` **30 passed** (70 s); `test_f8_m1.py` **69 passed** (the updated M1 regression L2 asked for; 3 s). The null declaration digest changed (two α fields added): `bfe0a5a0067cae7c…`.

## D1 — DKW on dependent windows. ACCEPTED, and the substance was worse than the form.

L1 had asserted in conversation that consecutive windows were independent to ~ρ¹⁰⁰. That was wrong: the *boundary* ticks of adjacent windows are one tick apart (ρ¹ ≈ 0.81), and summed over both windows this gives an exact consecutive-window correlation of **0.0245** at the frozen rates (`window_lag1_correlation`, exact from the chain's autocovariance; checked against brute-force summation at small windows and against the closed form; the 400-replicate empirical value is 0.041 ± 0.017). The pooled 4,000-window sample is therefore not an i.i.d. sample, as L2 said.

**Repair (both of L2's options, kept apart in the record, `NullValidation`):**
- *Inferential, designated window:* the terminal window (the one S_term is scored on), one per replicate, n = n_replicates; DKW bound at α = 0.05; the DKW tail bound 2·exp(−2nD²) reported as a conservative p-value.
- *Inferential, union test:* every window index j separately at α/10 against the per-window sup deviation; a union bound is valid under any dependence, so `union_passed` has P(false fail) ≤ α whatever the window correlation.
- *Descriptive:* the pooled all-windows sup deviation, renamed `all_windows_sup_deviation`, with no bound and a docstring prohibition on using it as qualification evidence.
The record's `__post_init__` recomputes both bounds from n_replicates and refuses a record whose `dkw_bound` is the i.i.d.-4000 value, whose pass flags disagree with its statistics, or whose p-value is not the tail bound (tests `..._refuses_the_iid_all_windows_interpretation...`).

**The full-N qualification record under the repaired method (400 replicates, master 220261026, grid 50, 1,100 ticks), reported as it came out:**

| Statistic | Value | Bound / nominal | Result |
|---|---|---|---|
| Designated-window DKW (terminal window) | 0.0837 | 0.0679 (α = 0.05, n = 400) | **FAIL**; DKW p ≈ 0.0073 |
| Per-window sup, j = 0…9 | 0.059, 0.065, 0.042, 0.046, 0.036, 0.037, 0.044, 0.035, 0.057, 0.084 | union bound 0.0865 (α/10 each) | **PASS** (all ten) |
| Pooled all-windows sup (descriptive) | 0.0159 | — | — |
| Empirical mean density / σ | 0.052302 / 0.0013395 | π₁ 0.052282 / σ 0.0013366 | 1 SE / 0.2 % |
| 0.99-quantile exceedance (all windows) | 1.05 % | 1 % | — |
| Exceedance of θ_T / θ_P (all windows) | 0 / 0 of 4,000 | ≤ 0.1 % / ≤ 0.01 % | expected ≈ 3.6 / 0.4; P(0) ≈ 0.03 / 0.67 |
| S_min > θ_P (route (b) price) | 0 of 400 | ≤ α_P = 0.001 | descriptive |
| Consecutive-window correlation | 0.041 (emp.) | 0.0245 (exact) | consistent |

L1's reading, offered for L2's ruling and not acted on: nine of the ten window statistics lie at 0.035–0.065, the expected size for n = 400 (E[D] ≈ 0.043), and the terminal window's 0.084 is the largest of ten; the designated test, which fixes that window in advance, fails at p ≈ 0.007, and the union test, which is the dependence-valid use of all ten, passes. L1 did **not** change the replicate master, the α, the designated window or n after seeing the result; the record is written with the failure in it. L2 is asked to rule which statistic is the qualification statistic for the governance record: (i) the designated-window DKW, in which case this record FAILS and M7 must carry it as failed (the law itself stands on the exact paths; a rerun would need a new declared master, as a new validation identity); (ii) the union test, in which case it passes; (iii) both required. L1 recommends (iii) for discipline and, under (iii), a rerun at the same master with n = 1,000 **only on L2's word**, reported whichever way it falls.

## D2 — scaled-grid rates against production thresholds. ACCEPTED, option (a).

Below the production grid `validate_on_stepper` now derives θ_P and θ_T from the scaled-grid law's own CDF (the same conservative-coverage selection, F̂(k) − ε ≥ q), records them as `theta_p_used` / `theta_t_used`, and labels the record `thresholds_scope = "smoke_scaled_grid"`; at grid 50 the production cache's values are used and the scope is `"production_cache"`. `is_qualification_evidence()` is true only for production scope; the record refuses a scope that disagrees with its grid. Tests: the smoke run's thresholds differ from the production cache's, are ordered, lie **above** them (a smaller N has a wider null), and the exceedance rates are calibrated against the scaled nominal; a scaled record cannot be relabelled production scope.

## Boundaries L2 stated — acknowledged

1. Conservative-coverage selections are never relabelled exact crossings: `mode`, `ordinary_index`, `displacement` travel with every certificate.
2. The 16/2/4 rule is subject to M6 requalification; nothing here approves it.
3. The familywise value 10·(1 − F_W(θ_P)) = 0.00097 is a nominal union bound, never an empirical rate; the empirical 0/400 is reported as descriptive.
4. 28 → 30 passed here; the `pyarrow`-dependent test is discharged by Mike's canonical run, as for M1.

*L1, 2026-10-27.*
