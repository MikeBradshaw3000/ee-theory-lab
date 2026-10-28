# L2 → L1 — Flight 8 M2/M3 Build Review, Round 1

**Register:** Instrument build review; F8 v0.8.4 FROZEN (`e87277a2d11e948f`); freeze record `16869692a043b139`; Appendix A `94d527624beafa7c`. M1 placement `0f30400`. **Verdict: DEFECT-WITH-REPAIR.** No placement or production run is authorized by this review.

## Identity and execution

Archive: 39 files (directory entries excluded). Checked packet `44b275a3b8dc45eb`, `f8/classify.py` `42daeb4663c5783f`, `f8/null.py` `b18b935fb5d1657e`, `f8/dynamics.py` `cc663dd3c14197a8`, `test_f8_m1.py` `23d4260f5a2d996b`, `test_f8_m2_m3.py` `86bb33610ae31ffc`; contract and Appendix A identities as above. These are the received source identities, not placement authorization.

Executed `python -m pytest tests/test_f8_m2_m3.py -q` from `flights/mfa_fidelity/instrument`: **27 passed, 1 failed in 58.50 s**. The failed test, `test_f8_m2_m3_do_not_touch_e1`, aborts on `ModuleNotFoundError: No module named 'pyarrow'` when importing unchanged `mfa_instrument/e1/config.py`. This is an **environment dependency**, not evidence of source nonconformance. Installing `pyarrow` was attempted, but network access prevented installation. Thus the claimed **28/28** is **not independently reproduced**; the 27 executable tests passed. Canonical suite passage on the placement machine remains a prerequisite.

## Rulings

| Item | Ruling | Reason |
|---|---|---|
| M1-r3 `dynamics.py` | **SOUND, qualified changed-source clearance** | Count-grid sums and one division replace float64 means; result agrees bitwise with the M2 statistic and keeps the post-advance window geometry. The separate updated M1 regression suite has **not** been run here; require canonical M1 regression before placement. |
| M2-1 | **SOUND** | §4.2 explicitly calls `S_term` the *terminal-window mean*, and §4.3 defines θ_T using a *single window's* occupancy. The tenth 100-tick window is correct; E1's three-window convention does not override F8's frozen words. |
| M3-1 | **SOUND as a shape declaration; qualification diagnostic defect D1 below** | Full N=2500, 1100 ticks, and ten tail windows preserve the stationary-null marginal and avoid production run identity. Shorter validation is not production evidence. |
| M3-2 | **SOUND** | Master `220261026` is explicit and distinct from declared panel/calibration masters; replicate runs are not canonical panel runs. |
| M3-3 | **SOUND as disclosed conservative numerical policy** | The 1e-9 factor floor times 2500 is intentionally conservative; both quantiles move by at most two count-grid steps. Preserve the mode and displacement in every record. This does not certify more numerical precision than the bound actually establishes. |
| M3-4 | **SOUND** | One stationary Markov window-count law gives both marginal quantiles; the implementation enforces `theta_P >= theta_T` (the declared observed outputs are strictly ordered). |
| M3-5 | **SOUND as a nominal upper bound, not evidence of discrimination** | `10 × [1 − F_W(theta_P)] <= alpha_P` is a valid conservative union bound for `S_min > theta_P`, even without independence of windows. `0/400` is a disclosed empirical observation, not a certified realized rejection probability. M6 must price discrimination and fallback (c) requires a new instrument version. |

## Defects requiring repair

### D1 — DKW qualification incorrectly treats serially dependent windows as i.i.d.

**Location:** `f8/null.py`, `validate_on_stepper`, construction of `dkw_bound = sqrt(log(2/alpha)/(2*m))` using `m = 10*n_replicates`, and `dkw_passed`.

**Finding:** DKW's stated distribution-free finite-sample bound applies to an independent sample. The ten sequential 100-tick windows within each replicate are from the **same stationary Markov trajectories**. Stationarity gives correct marginal `F_W` but does not make windows independent. Therefore `dkw_passed` at `m=4000` is not an α=0.05 coverage-qualified test on the stated sampling design. The reported numerical sup deviation is a valid descriptive measure; the inference attached to it is not established.

**Repair:** Prefer an independently justified, conservative validation: draw one designated window per independent replicate and use `n=n_replicates` in DKW, or derive and test a dependence-valid concentration bound for all windows. Alternatively rename the current comparison an explicitly **descriptive heuristic** and prohibit `dkw_passed` from being used as inferential qualification/readiness evidence. Preserve all-window descriptive diagnostics. Add a discriminating test that refuses or distinguishes the erroneous i.i.d.-4000 interpretation. Rerun and disclose the full-N qualification record under the repaired method.

### D2 — scaled-grid validation evaluates rejection rates using full-grid cutoffs

**Location:** `f8/null.py`, `validate_on_stepper`: when `grid < 50`, `cdf`/`denom` are recomputed at `n=grid²`, but `th = null_thresholds(...)` still supplies N=2500 `theta_p` and `theta_t`. The calculations for `exceed_theta_t_rate`, `exceed_theta_p_rate`, `s_min_rejection_rate`, and `s_term_false_no_sustained_rate` then mix **scaled-grid sample statistics** with **production-grid thresholds**.

**Finding:** Such rejection rates are not calibrated tests against the null's scaled-grid nominal quantiles. The current smoke test checks mean and DKW only, leaving this mismatch untested. The correct production-grid qualification path is not affected; the risk is a mislabeled or later-misused validation result.

**Repair:** Either (a) compute grid-specific θ_T and θ_P from the already calculated scaled-grid `cdf` when `grid != 50`, marking their identity and smoke-only scope; or (b) return these four rates as *not applicable* for scaled-grid runs and forbid comparison with nominal α there. Retain production-grid thresholds unchanged. Add a scaled-grid test that detects the present mismatch, and a test preventing smoke diagnostics from being presented as production qualification.

## Additional boundaries and acceptance conditions

1. The primary per-cell occupancy DP, independent rational check, convolution and quantile modes are consistent with the frozen §§2.9/4.3 on inspected paths and within the 27 passing tests. Exact transfer-matrix probabilities concern the marginal law; the reported conservative-coverage selections must not be relabeled exact quantile crossings.
2. F8's `S_term` and θ_T have a coherent single-window pairing. The M2 run classifier respects strict `>` for SUSTAINED, `<=` for NO_SUSTAINED and the declared precedence; the 16/2/4 rule is still **subject to M6 requalification**, not approved by this review as scientifically discriminating.
3. The nominal familywise bound for `min(window means) > theta_P` is mathematically valid, though the min-event is much rarer than the union upper bound can suggest. Do not call the nominal bound an empirical rate.
4. Obtain `28 passed` on an environment with `pyarrow`, rerun the updated M1 regression module (69 expected), and submit changed-source identities and focused regression evidence for D1/D2. L2 review of those changes is required before SOUND and placement.

**Disposition:** **DEFECT-WITH-REPAIR**. The two repairs concern validity and labeling of validation evidence, not a request to alter the frozen contract or production quantiles. M1-r3 and M2-1 are substantively cleared as specified, subject to regression verification; M3-1 through M3-5 are qualified as above. No placement and no canonical run authorized.
