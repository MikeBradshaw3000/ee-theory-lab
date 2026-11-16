# Flight 9 — Freeze Record (Contract F9 v0.7)

**Ratified by:** Mike, 2026-11-15, in two statements: "11.2 ratified if you agree. I think we can leave gemini out of this for now." and, to L1's two questions (the remaining PROPOSED values as a block; his word to draft this record for v0.7), "Yes yes". L1 agreed, with the two statements of §3.3. **Drafted by:** L1, at Mike's word, the same day. **Effective:** on the commit that places this file, whose message names the contract FROZEN. The contract README in this directory cites this record.

## 1. The frozen object

| Item | Identity (SHA-256) |
|---|---|
| `FLIGHT_9_CONTRACT_v0_7.md` — **the frozen contract** | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` |
| Committed at | `b925537dab451f8c5630c896df2881564cfe7b67` (`main` when this record was written; fresh clone) |
| `arith_v0_3/` to `arith_v0_7/` — the scripts and outputs the contract's numbers were written from | identities in the contract's Appendix A.9 |

The text is frozen as committed, markers included. Where it marks a value PROPOSED, §3 of this record is what makes the value of record. Step 0 of the contract's job table is met: Appendix A is computed (container values; see §4), and the declarations, the generator transformations and the calibration estimators are fixed in the text.

**One editorial slip is frozen with the text and changes nothing.** The heading of §11 reads "what goes to L2 in round 5"; the round was 6, as the header and §11.3 say. L2 noted it in round 6 as not blocking.

## 2. Review chain the freeze rests on

- **Design.** Design note v0.1 to v0.3 (`8d82e319d79402f8`), L2's design consultation (`65d95bc3a907cf04`), the pre-probe declaration v1.0 (`473a2a165fd5cb4e`) and the probe record of 2026-11-12, all under `flights/mfa_fidelity/design/flight9/`.
- **L2 (adversarial contract review), six rounds, 2026-11-13 to 2026-11-15.** Informal advice on L1's questions (`a79dbb22de2a6fb0`); round 1 on v0.2, R1–R10 (`1473d63371701c06`), with a discussion exchange (`4cfcb442b7499b35`); round 2 on v0.3, F1–F7 (`f3c2b07d546869ff`); round 3 on v0.4, R3-1 and R3-2 (`04934a2ec28d763a`); round 4 on v0.5, R4-1 (`1131f4ae845473a6`); round 5 on v0.6, R5-1 and R5-2 (`693a0ba0dc20768b`); **round 6 on v0.7: FREEZABLE AS A CONTRACT CANDIDATE** (`L2_F9_CONTRACT_V0_7_ROUND6_REVIEW_2026-11-15_RECEIVED.md`, `33310f3b810e046d`), every repair closed and no further blocker identified. L2's clearance is of the contract as a declaration. It states that no instrument exists and that no calibration, qualification or scoring has passed.
- **Gemini (read-only corpus audit): not invoked.** The contract's status line names the audit on its review path. Mike decided on 2026-11-15 to leave it out for now. Gemini commission v3.1 stays held. No audit finding exists for this contract, favourable or adverse.
- **Mike's rulings of record carried into the contract** (its §11.1): 2026-11-12 (the claim grammar of the pre-probe declaration; terrains TB and TD on L1's step-1 recommendations); 2026-11-13 ("i rule as recommended" on L2's advice; "I rule affirmative to all" under the stated principle; "f3 descriptive and proceed directly"); 2026-11-14 ("I accept your recommendation": B scoped to the registered family; and again: the constant-map state capped away from θ, the near band reported); 2026-11-15 ("proceed as stated"; this ratification).

## 3. PROPOSED values ratified (each is of record from the freeze commit)

**3.1 The seven items of the contract's §11.2, ratified by name.**

| # | Item | Ratified as |
|---|---|---|
| 1 | Skeleton survival criterion | s ≥ 36 of 40 |
| 2 | Calibration stop paths | fewer than 3 levels with an edge for any required arm; median per-cell standard error of the scored map above 0.02; the typed stops of the calibration transformations (fewer than 5 non-empty bins; zero pooled residual variance; ρ₁ ≥ 0.99). Each stops the stage and requires a new instrument version |
| 3 | T0 exercise values | hysteresis bracket 0.0754 with the fine-grid eligibility rule; continuity criterion on J normalized to an interval of 0.10; the high-initialization skeleton as proxy for the low sweep's variance; f_J = 0.25 and ρ₀ = 0.02, both carried from Contract F8. The exercise gates nothing |
| 4 | Assumption register | §1.5, entries A1–A7 and A9 as written (A8 withdrawn in v0.4) |
| 5 | Evaluator cost | about 9 to 11 hours per θ per panel at prototype speed, beside about 19.5 hours of dynamics, *as a planning figure only* (see §3.3) |
| 6 | Comparison arrays | §3.4: the latent t on TA and TD, u on TC, each index's own array on TB, each rounded to 12 decimal places; endpoint B scoped to their registered families |
| 7 | Qualification contents of v0.5 to v0.7 | the strip fixture; the COMPATIBLE, ADVERSE and low-information arm constructions; the B and D flight constructions; the band "0" = [0, 0.5]; at most 10,000 candidates per stratum, then `stratum not populated`; the four unavailable-state recipes (constant map on [0.03, 0.40] assigned by population value; saturated on [0.60, 1.00]; the low map 0.03 + 0.05·z; the constant index); four quotas of 50 within 2,500 candidates each; row 15's error event with the harness's reference state; the half-width 0.06 of the reported band near θ |

**3.2 The remaining PROPOSED values, ratified as a block.**

| # | Value | Ratified as |
|---|---|---|
| 8 | κ grid | 0.75; 1.00 to 2.00 in steps of 0.05; 2.25; 2.50; 3.00 (25 levels, integer micro-units) |
| 9 | Horizon and recording tail | T = 3,000 ticks; last 1,000 recorded |
| 10 | Occupancy threshold | θ = 0.20 scored; 0.10 and 0.30 reported |
| 11 | Edge and component conventions | 4-neighbour bonds with periodic wrapping, each at its midpoint and of equal weight; every connected boundary piece of the post-estimator region; the corner rule of a 4-connected region |
| 12 | Informative level | at least 100 cells on each side; at least 40 bonds |
| 13 | Component resolution | m = 40 bonds |
| 14 | Permitted discrepancy | ε = 2.0 cells |
| 15 | Site-closure solver | start at p = 1 (skeleton) or p = π₁ (realization); tolerance 1e-12 in max norm; at most 200,000 iterations |
| 16 | Identity procedure | §3.4 as written: serialization; comparison arrays rounded to 12 places; cross-platform agreement to 1e-12; canonical objects of record built at step 1 |
| 17 | Reported-item schemas | §5.7 as written |
| 18 | Instrument version string | `f9_stage1_v1` |
| 19 | The contents and sizes of §6 not named in item 7 | the known-answer corpus, classes 1 to 24; the generator declaration of §6.2 (seed-map law, population mean, level-case maps and the generic sweep); the bands; 200 accepted cases per stratum in each ensemble; 23 capped strata, each at cap 0.10 by one-sided 95% Clopper–Pearson (at most 12 errors); the calibration transformations for σ_seed and ℓ_c |

Items 3 (as to f_J and ρ₀) and 19 were not spelled out in the table L1 put to Mike on 2026-11-15, which listed eleven values. The contract marks them PROPOSED ("T0 … values PROPOSED"; "§6 … contents and sizes PROPOSED"), so they are named here. L1 told Mike of this before placement; his word to place this record covers them.

**3.3 L1's two statements at ratification (recorded at Mike's condition "if you agree"; neither is a condition on the freeze).**
- *Item 5 understates the cost.* The figure was measured before v0.5 to v0.7 added the brute-force certification of arm and flight candidates, with up to 10,000 candidates per stratum. That work is not priced. The cost of record is whatever step 10 (`resource_benchmark`) measures on the canonical machine; assumption A4 governs if it is not affordable.
- *Item 7 can close the qualification stage.* Whether every stratum fills under calibration-derived noise has not been tested; L1's checks are at zero noise or use illustrative noise. A stratum that does not fill records `stratum not populated` and closes the stage, with no same-stage repair. This is the declared design.

**Already RULED before this record (not re-ratified here):** L = 100, N = 10,000; P = `F_canonical`, H = `F_baseline` as rival only; η₀ = −ln(0.99), μ = 0.2, Δt = 1; bases frozen, g swept, κ = g/g_spec,X; 40 seeds; every run on its own stream; terrains T0, TA, TC, TB (r = 0.3) and the four TD variants, with their roles; the scored map; the complete contour family and its registered scope; the joint discrepancy S; the 950-of-1,000 bootstrap-support rule; the arm and flight rules for B and D; no headline word; the persistence diagnostic without a coupling claim; contour constancy descriptive only; the margin cuts 0.10, 0.20, 0.30; the job order of §8.

## 4. Derived values at this freeze

None is fixed here. The contract carries no value marked DERIVED@FREEZE. Appendix A's numbers (spectral values, family sizes, closure estimates, array hashes) are container values (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1) and are provisional by the contract's §3.4. The canonical arrays, families and spectral values are built at step 1 (`build_identities`) and are of record from there. σ_seed(·) and ℓ_c are derived at step 4 by the transformations this freeze fixes.

## 5. What this freeze does not do

It authorizes no build and no run. Every step of the contract's §8 from 1 to 16 needs its own authorization from Mike naming the stage and the jobs. No instrument exists under this contract. No master has been drawn. TB with r = 0.3 and the four TD variants have never been run. The boundary endpoint has not been seen by L1: no occupancy map was rendered from probe output, nothing from probe output was computed against λ contours, and no edge was extracted from it. The probe array archive stays unopened for any boundary purpose.

The frozen text is never edited. A change is a new versioned contract under a new review.

Still held and not authorized: Gemini commission v3.1; the two next-touch repairs (`test_f8_m6.py` docstring, `test_f8_mp1.py` comment); the third-order lattice-versus-ODE comparison; onset continuity; the PD7-versus-floor correspondence.

## 6. Lessons bound at this freeze (added to the record's running list)

- A statement that something can be computed, built or afforded is computed before it is written. Three of this register's repairs came from the opposite: a cost objection that was never measured (round 1), strata that no canonical terrain can carry (R3-2), and an acceptance rule that no case of its own row could meet (R4-1).
- A claim about "every level set" names the array it is complete for. Agreement of scalars, identity of masks and completeness over a family are three properties (R3-1).
- A rule that implements a ruling is applied to the quantity the ruling is about. The near-θ split was ruled for the population map and first written on the pre-noise constant (R5-1).
- New declaration text is read against every row it governs before it goes to review (R4-1, R5-2).
- Before a placement kit is built, `main` is checked from a fresh clone, and the kit is rebuilt if `main` has moved. The script's refusal is the backstop, not the check (the v0.5 placement, 2026-11-14).

*Written by L1 2026-11-15 at Mike's word. Mike rules.*
