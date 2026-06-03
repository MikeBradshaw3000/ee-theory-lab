# Rule D downstream opens — resolution (D-1 / D-2 / D-3)

**Status:** CANONICAL. Resolves the three downstream design opens left by the Rule D design contract (`cycle3/wave_two/rule_d/RULE_D_DESIGN_CONTRACT.md`, Section 7). Layer 2-concurred 2026-06-03. The contract governs mechanism, fences, coupling reuse, and the bracketing success criterion; this memo fixes only the grid choices the contract deferred, set against the realized scale and justified by the Rule D question — never by a LowLow search. No probe is seeded by this memo; seeding remains Mike's call to open after Layer 3 implementation.

**R3 amendment note (2026-06-03):** This memo was first placed (84e4cd9) describing theta_turnover = 0 as "the pure-Rule-C signed reference" under the original contract form (persistence = 1 - theta_turnover, Lambda-survival removed). Layer 3 implementation surfaced that under that form theta_turnover = 0 is absorbing and the lattice saturates (rho -> 1), so theta_turnover = 0 was NOT a signed anchor but a saturation-degenerate endpoint. The contract was amended to R3 (2d2e281): active-cell persistence is s_Lambda * (1 - theta_turnover), retaining Rule C's neighbor-independent Lambda-survival with theta_turnover as an ADDITIONAL independent churn hazard, so theta_turnover = 0 NOW recovers Rule C exactly and is a genuine signed reference. This memo is regenerated to match R3. The grid choices (theta values, the c = +/-0.35 kappa pair, Lambda = 0.40, the five seeds) are unchanged; what changed is the calibration interpretation (the theta ladder is an additional-churn ladder on top of s_Lambda, not a total-active-lifetime ladder) and the run-length figure (corrected below).

---

## Resolved settings

- **D-1 — theta_turnover grid:** theta_turnover in {0, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50}. Seven settings. Under R3, theta_turnover = 0 is the exact Rule C reference (net persistence = s_Lambda), the signed lower anchor of each bracket; 0.50 is the high-additional-churn endpoint.
- **D-2 — responsive coupling:** matched pair at realized contrast c = -0.35 and c = +0.35 (realized_delta_p = +/-0.35), both signs, held fixed across the full theta ladder. One magnitude, both signs.
- **D-3 — Lambda anchor:** Lambda = 0.40 only.

Design space: 7 theta x 2 kappa x 5 seeds (42/137/256/1024/31415) = 70 run-settings, on the inherited wave-one window structure: 200-tick runs, 100-tick windows, sliding step 25 (window_start 0/25/.../100), 50x50 Moore-radius-1 toroidal substrate, LOW_Z_THRESH = 2.0, SS-001 earned-window criterion.

---

## Justification against the realized scale (Rule D question, not LowLow search)

### D-2 and D-3 (from M2 primary source)

The Rule D success criterion (contract Section 4) needs a matched responsive kappa that is signed and non-degenerate at theta_turnover = 0, so the bracket has a signed lower end to start from, and a Lambda anchor with floor headroom so added turnover can move rho down without immediately hitting the floor (otherwise the density-confound guard, Section 4.3, cannot discriminate). Under R3, theta_turnover = 0 recovers Rule C exactly, so the signed lower anchor is the KNOWN Rule C regime at the chosen (Lambda, kappa) — no longer something that must be rediscovered.

The M2 CSV establishes both directly at Lambda = 0.40:
- mean_rho is near-stationary across the responsive band, ~0.42 at negative coupling down to ~0.35 at c = +0.5, with third/fourth-decimal jitter across seeds and windows. rho barely moves with kappa and is nowhere near the extinction floor (contrast Lambda = 0.20, c = +0.8, which hits rho ~0.02). This is the headroom D-3 requires; 0.40 is selected over 0.20 (which runs near extinction under positive coupling) and over promoting reserved 0.30/0.50 (unnecessary headroom for first pass).
- c = +/-0.35 is solidly signed on both axes at both signs and non-degenerate: persistence-z ~ -5 to -6 at c = -0.35, ~ +6 at c = +0.35; extinction/saturation flags False throughout; rho ~0.37-0.42. It sits clear of the |c| <= 0.10 floor-adjacent zone and clear of the |c| = 0.8 degenerate endpoint. Both signs are run because turnover-limited suppression should drive either signed signature (negative-kappa negative-persistence, positive-kappa positive-persistence) toward near-null if the mechanism is real; testing both is a stronger discriminator than one and reads sign-symmetry directly.

D-3 reuses 0.40 rather than promoting reserved anchors because, under R3, 0.40 at theta_turnover = 0 IS the M2 Rule C signed regime — the bracket's signed lower end is the M2-characterized state directly.

### D-1 (calibrated against the organization time-scale; Layer 2-concurred)

The mechanism is a time-scale-mismatch claim: added turnover suppresses near-null observables only if active sites churn faster than apparatus-level organization accumulates. Under R3 the theta ladder is an ADDITIONAL-churn ladder layered on Rule C's baseline survival s_Lambda — NOT a total-active-lifetime ladder. The net active-cell persistence at each setting is s_Lambda * (1 - theta_turnover); theta_turnover adds churn on top of whatever deactivation Rule C's survival already produced. The ladder must bracket the organization-formation time-scale via this added churn, not target a guessed near-null point.

Realized-scale anchor (M2 primary source, Lambda = 0.40): per-run rho_range_over_mean is large in the first window and collapses to ~0.10-0.15 over the later 100-tick windows, with mean_rho near-stationary thereafter. The substrate settles within roughly the first window-step (~25 ticks of evolution) and then holds across the 100-tick measurement windows, anchoring the organization time-scale at order ~25 ticks of evolution.

Layer 2 concurred that rho-stabilization is acceptable as a first-pass time-scale proxy provided it is treated as an order-of-magnitude anchor (rho is the k=0 mode; the observables are spatial/persistence organization measures, so the relevant relaxation modes can differ — but the ladder is broad enough to cover the plausible mismatch). Layer 2 added the load-bearing correction that the turnover hazard damps pair/persistence structure on a scale closer to 1/(2 theta), not 1/theta, because a pair-like correlation survives only if both relevant active sites survive. Read as ADDITIONAL churn on top of s_Lambda, the ladder's two scales are:

| theta_turnover | added-churn single-cell scale 1/theta | added-churn pair-correlation scale 1/(2 theta) |
| ---: | ---: | ---: |
| 0.02 | 50 ticks | 25 ticks |
| 0.05 | 20 ticks | 10 ticks |
| 0.10 | 10 ticks | 5 ticks |
| 0.20 | 5 ticks | 2.5 ticks |
| 0.35 | ~3 ticks | ~1.4 ticks |
| 0.50 | 2 ticks | 1 tick |

These are the ADDED-churn time-scales (the rate at which the extra hazard removes active cells beyond Rule C's baseline), not total lifetimes. On the pair-correlation reading, theta_turnover = 0.02 added churn is already a plausible first competition point for persistence organization against the ~25-tick anchor; 0.05/0.10 cover the faster local-structure regime; 0.20-0.50 cover churn-dominant / endpoint. The ladder spans no-added-churn (theta_turnover = 0 = Rule C signed reference), comparable-to-organization, faster-than-organization, and high-added-churn / endpoint regimes. No lower value (e.g. 0.01) and no higher value are added preemptively: if theta_turnover = 0.02 already destroys signed structure relative to theta_turnover = 0, that motivates a later low-theta refinement; if 0.35 and 0.50 both stay signed and non-degenerate, a later high-theta extension can be opened; if 0.50 floors or degenerates, the endpoint job is already done. These are named follow-ups, not first-pass additions.

The ladder is justified by spanning the organization time-scale via added churn, NOT by any expectation of where near-null lands. Hardening the ladder around a hoped-for near-null setting would convert the design into a LowLow search and is excluded.

---

## Recorded diagnostics

Per-(parameter-setting, seed) boolean flag COUNTS, never per-parameter means. The run record preserves, for every setting:

- The set theta_turnover AND the effective active-cell persistence probability s_Lambda * (1 - theta_turnover) (R3: the ladder is an additional-churn ladder, so effective persistence — not theta alone — is the quantity that determines realized churn; record it for honest calibration reading). Record s_Lambda separately as well.
- Realized active-site lifetime / churn rate as an output diagnostic (interpretation hygiene, Layer 2-flagged): the {1/theta} figures are ADDED-churn scales, not total lifetimes; realized total lifetime is shorter still because Rule C's baseline survival also deactivates cells. Record realized churn so the calibration can be read honestly. Output only — no control, no feedback (the construction fence forbids theta_turnover adapting to any observed quantity).
- Density-confound guard (Section 4.3): rho_mean, rho_range_over_mean, and bracket-level delta_rho_mean (difference in rho_mean across theta at matched Lambda/kappa). Audit, NOT control.
- Live-coupling-exposure guard (Section 4.4): observed q_i distribution (mean and variance) and mean absolute neighbor-induced probability perturbation (mean |p_become,i - p_Lambda| over cells/ticks).

---

## What this memo does NOT do

- Does not seed any probe; seeding remains Mike's call after Layer 3 implementation.
- Does not modify the Rule D mechanism, fences, coupling reuse, or the Section 4 bracketing success criterion (the R3 amendment to the mechanism lives in the contract; this memo follows it).
- Does not reopen or reclassify Rule C M2 / A-prime, and does not alter the Comparator 0 / Comparator epsilon floor findings.
- Does not resolve the L4 ontological question; neither observable is named theoretical Psi.
- Does not harden the weak-form Rule B prior.

---

## Next step

Layer 3 (Gemini) re-implementation of Rule D under R3 (active-cell persistence s_Lambda * (1 - theta_turnover)) against these resolved settings, framed as "what the run will produce"; Layer 3 never declares its own L2 clearance. After implementation and parity, seeding is Mike's call to open.
