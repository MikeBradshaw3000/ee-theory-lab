# L1 → L2 — Flight 8 instrument modules M2 and M3: build packet (round 1), 2026-10-27

**Register.** Instrument build review under Contract F8 v0.8.4 (FROZEN, `e87277a2d11e948f`). Verdict SOUND / DEFECT-WITH-REPAIR. Nothing placed until L2 clears and the canonical suite passes on Mike's machine; no run authorized. M1 is placed at `0f30400` (L2 SOUND, round 2). The zip carries the whole `mfa_instrument` package, the contract, freeze record and Appendix A at repository paths, so the tests run in isolation (`pyarrow` is needed by three E1-import tests, as before).

**Scope.** M2 — run status and level label (contract §4.2). M3 — the Markov null and the threshold object (§2.9, §4.3; Mike/L2 ruling 2026-10-20: route (a) for θ_T, route (b) for θ_P, route (c) the named fallback). One disclosed change to the placed M1 (`dynamics.py`, below).

## Files (SHA-256, LF)

| File | Identity | Status |
|---|---|---|
| `instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | new (M2) |
| `instrument/mfa_instrument/f8/null.py` | `b18b935fb5d1657e7ea5073fc10087adea91b85cded8b25ea09921bf81fabf8a` | new (M3) |
| `instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | **changed** from placed `4d886e6acb51d331` (M1-r3, one function) |
| `instrument/tests/test_f8_m1.py` | `23d4260f5a2d996b56e748aada1e7ed5d5b6d35e57bc41be9fdc53b34b04bff0` | changed from placed `7cea440c282b369a` (expectations for M1-r3) |
| `instrument/tests/test_f8_m2_m3.py` | `86bb33610ae31ffc0e98f386fe4712d57c1dbeea8dbc33819e4312e53b3812ca` | new, 28 tests |

Test record (container): `test_f8_m2_m3.py` **28 passed** (69 s); `test_f8_m1.py` 69 passed; E1's M1/M2/M3 modules unchanged and passing. `config.py` and `__init__.py` unchanged from placement.

## M1-r3 — a disclosed change to the placed module (for L2)

Building M2 exposed that M1's `F8RunResult.tail_window_means` was a float64 mean over 100 densities while M2's statistic of record is one integer count sum over 250,000; the two differed by one ulp on a real record, so the record would have carried two values for one quantity. `dynamics.run` now computes window means and the tail mean on the count grid, exactly as M2 does (one sum, one division), and the M1 tests state that form. No rule, draw, record length, survival, or identity changes; the digest literals are untouched. L2 is asked to clear this as a round-3 changed-source identity for M1 together with M2/M3.

## M2 — what it does (E1 M2 carried; F8 record convention)

Tail = the last 1,000 post-advance ticks (2001..3000) in ten windows of 100, on the count grid (counts recovered from ρ exactly and verified by reconstruction; off-grid records refused). Statuses SUSTAINED (S_min > θ_P) → NO_SUSTAINED (S_term ≤ θ_T) → UNRESOLVED; labels S/N/M/U by the frozen 16/2/4 rule, carried verbatim, re-qualified under M6, nothing pre-approved (§4.2). Tests: geometry and tamper (incl. live count globals); tick 2000 excluded / 2001 included; precedence and threshold domain; all 231 (n_sus, n_no) pairs against the rule's text; seed-keyed statuses must be exactly the canonical panel; seven known-answer controls bit-exact against independently frozen rationals (a new one, `terminal_collapse_no_sustained`, exercises the single-window S_term); a real stepper record at m = 2.5 classifies SUSTAINED.

**Declaration M2-1 (for L2): S_term is the single terminal window.** Contract §4.2: "S_term = terminal-window mean"; §4.3: θ_T "by the exact two-state transfer-matrix law of **a single window's** occupancy". E1 used the terminal 300 ticks (three windows). The F8 text is singular in both places and θ_T's law is a one-window law, so M2 scores S_term on window 10 alone. If L2 reads §4.2 as E1's three windows, θ_T's law changes with it (a 300-tick occupancy), and that is a contract reading L1 would want ruled before M4.

## M3 — what it does

**The law.** For a stationary two-state cell (a = 1 − e^(−η₀), q = 1 − e^(−μ), π₁ = a/(a+q) — computed by the stepper's own functions), the 100-tick window occupancy pmf by the transfer-matrix DP; the window count over N = 2,500 cells by the N-fold convolution (FFT power on the exact support 0..250,000). By stationarity every window, the terminal one included, has this marginal law, and λ̄ is inert, so the thresholds are level-independent and cached per level (§4.3 note).

**Thresholds.** θ_T = inf{x : F_W(x) ≥ 0.999} (route a); θ_P = the per-window marginal at 1 − α_P/10 = 0.9999 (route b), giving P_null(S_min > θ_P) ≤ 10·(1 − F_W(θ_P)) ≤ α_P; the realized conservatism is priced by `validate_on_stepper` (below). Values: **θ_P = 0.057364** (14,341/250,000), **θ_T = 0.056484** (14,121/250,000). Appendix A's provisional Gaussian θ_P was 0.0573; its π₁ = 0.0522823… and σ_null = 0.0013366… are reproduced by the exact law to 1e-9.

**Three independent paths for the law, all in the tests.** (1) The per-cell DP in float64 against the same DP in exact rational arithmetic on the stepper's float64 a, q (exact for the realized law): L1 distance 1.9e-16; and against brute-force enumeration of every path at window lengths 1–8 (exact equality for the rational DP; < 1e-14 for float). The stationary mean W·π₁ and the exact autocorrelation variance match to 1e-12 / 1e-10. (2) The N-fold FFT law against an exact rational 4-fold convolution (< 1e-13) and, at N = 2,500, against a truncated direct-convolution path (max |ΔCDF| 1.8e-12; discarded mass 3e-28; both quantile crossings agree). (3) The F8 stepper itself at g = 0: 400 replicates at full N on the declared validation shape — DKW sup-deviation 0.0159 ≤ 0.0215 (α = 0.05, 4,000 windows); empirical mean 0.052302 vs π₁ 0.052282 (1 SE); empirical σ 0.0013395 vs 0.0013366; 0.99-quantile exceedance 1.05%; exceedance of θ_T 0/4,000 (expected ≈ 3.6; P(0) ≈ 0.03 — reported, not asserted); **familywise price: S_min > θ_P in 0/400 replicates against the α_P = 0.001 nominal.** The test module runs the smoke-scale and a 10-replicate full-N version; the 400-replicate run is a qualification job, recorded in the governance record when M7 binds it.

**Certificates (E1 M3 grammar carried).** Per-cell and window pmf certificates (imaginary residual, negative mass, normalisation error, clip correction; L1 bounds: factor bound = max(floor 1e-9, 1000 × measured residuals, 1000 × the exact-rational distance); sum bound = N × factor + own). Quantile certificates with both-margin certification and the conservative certified coverage threshold k_safe = min{k : F̂(k) − ε ≥ q} when the ordinary crossing does not certify; ε = 2.5e-6 (the floor × N dominates — the measured residuals are 1e-12–1e-16). Both thresholds select in **conservative-coverage mode**, displacement 2 grid steps for θ_P (8e-6 in density) and 1 for θ_T (4e-6), reported as E1's were, never asserted globally. Every object validates fail-closed at construction and on `dataclasses.replace` (tested field by field); the cache (`ThresholdCache`, production = exactly the 24 levels, slice = any subset) validates only by replay and round-trips through canonical JSON.

## Declarations for L2 (none pre-approved)

- **M3-1 Validation shape.** Null validation on the stepper runs at full N = 2,500 with 1,100 ticks (ten tail windows), never at the production shape: replicate seeds are not panel seeds and claim no production identity (M1's panel policy, D1/D2). The null is stationary from t = 0, so the pre-tail ticks do not enter the law.
- **M3-2 Replicate master 220261026** for null validation, declared in the null declaration; distinct from both panel masters and E1's.
- **M3-3 Error-bound floor.** E1's 1e-9 per-factor floor, multiplied by N, is what forces conservative-coverage mode here (true residuals are four to seven orders smaller). L1 carried the rule unchanged rather than tune it; the displacement is ≤ 2 grid steps. L2 may prefer a per-sum floor; L1 would make that change only on L2's word and as a declared successor identity.
- **M3-4 One law, two quantiles.** θ_P and θ_T are two quantiles of the same window-count CDF, so θ_P > θ_T is an invariant and is enforced.
- **M3-5 Price of route (b) stated nominally.** 10·(1 − F_W(θ_P)) = 0.00097 ≤ α_P. The realized rate (0/400) is the qualification price; M6 decides whether (b) discriminates, and (c) is invoked only as a new instrument version (§4.3).

*L1, 2026-10-27.*
