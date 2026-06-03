# Rule D downstream opens — resolution (D-1 / D-2 / D-3)

**Status:** CANONICAL. Resolves the three downstream design opens left by the Rule D design contract (`cycle3/wave_two/rule_d/RULE_D_DESIGN_CONTRACT.md`, Section 7). Layer 2-concurred 2026-06-02. The contract governs mechanism, fences, coupling reuse, and the bracketing success criterion; this memo fixes only the grid choices the contract deferred, set against the realized scale and justified by the Rule D question — never by a LowLow search. No probe is seeded by this memo; seeding remains Mike's call to open after Layer 3 implementation.

The opens were resolved by Layer 1 against the Rule C M2 primary source (`cycle3/data_out/c3_w2_rule_c_m2_results.csv`), with the D-1 time-scale calibration routed to Layer 2 and concurred. D-2 and D-3 were settled directly from the M2 map and did not require Layer 2 routing.

---

## Resolved settings

- **D-1 — theta_turnover grid:** theta_turnover in {0, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50}. Seven settings. theta=0 is the pure-Rule-C signed reference (the matched lower anchor of each bracket); 0.50 is the churn/floor endpoint.
- **D-2 — responsive coupling:** matched pair at realized contrast c = -0.35 and c = +0.35 (realized_delta_p = +/-0.35), both signs, held fixed across the full theta ladder. One magnitude, both signs.
- **D-3 — Lambda anchor:** Lambda = 0.40 only.

Design space: 7 theta x 2 kappa x 5 seeds (42/137/256/1024/31415) = 70 run-settings, on the inherited 5x25-tick window structure (125 ticks/run), 50x50 Moore-radius-1 toroidal substrate, LOW_Z_THRESH = 2.0, SS-001 earned-window criterion.

---

## Justification against the realized scale (Rule D question, not LowLow search)

### D-2 and D-3 (from M2 primary source)

The Rule D success criterion (contract Section 4) needs a matched responsive kappa that is signed and non-degenerate at theta=0, so the bracket has a signed lower end to start from, and a Lambda anchor with floor headroom so turnover can move rho down without immediately hitting the floor (otherwise the density-confound guard, Section 4.3, cannot discriminate).

The M2 CSV establishes both directly at Lambda = 0.40:
- mean_rho is near-stationary across the responsive band, ~0.42 at negative coupling down to ~0.35 at c = +0.5, with third/fourth-decimal jitter across seeds and windows. rho barely moves with kappa and is nowhere near the extinction floor (contrast Lambda = 0.20, c = +0.8, which hits rho ~0.02). This is the headroom D-3 requires; 0.40 is selected over 0.20 (which runs near extinction under positive coupling) and over promoting reserved 0.30/0.50 (unnecessary headroom for first pass).
- c = +/-0.35 is solidly signed on both axes at both signs and non-degenerate: persistence-z ~ -5 to -6 at c = -0.35, ~ +6 at c = +0.35; extinction/saturation flags False throughout; rho ~0.37-0.42. It sits clear of the |c| <= 0.10 floor-adjacent zone and clear of the |c| = 0.8 degenerate endpoint. Both signs are run because turnover-limited suppression should drive either signed signature (negative-kappa negative-persistence, positive-kappa positive-persistence) toward near-null if the mechanism is real; testing both is a stronger discriminator than one and reads sign-symmetry directly.

D-3 reuses 0.40 rather than promoting reserved anchors because 0.40 is already characterized at theta=0 by M2, giving each bracket's lower end a known signed reference for free.

### D-1 (calibrated against the organization time-scale; Layer 2-concurred)

The mechanism is a time-scale-mismatch claim: turnover suppresses near-null observables only if active sites churn faster than apparatus-level organization accumulates. The ladder must therefore bracket the organization-formation time-scale, not target a guessed near-null point.

Realized-scale anchor (M2 primary source, Lambda = 0.40): per-run rho_range_over_mean is ~0.8-1.2 in the first 25-tick window (window_start 0) and collapses to ~0.10-0.15 for windows 25/50/75/100, with mean_rho near-stationary thereafter. The substrate settles within roughly one 25-tick window and then holds, anchoring the organization time-scale at order ~25 ticks.

Layer 2 concurred that rho-stabilization is acceptable as a first-pass time-scale proxy provided it is treated as an order-of-magnitude anchor (rho is the k=0 mode; the observables are spatial/persistence organization measures, so the relevant relaxation modes can differ — but the ladder is broad enough to cover the plausible mismatch). Layer 2 added the load-bearing correction that the turnover hazard damps pair/persistence structure on a scale closer to 1/(2 theta), not 1/theta, because a pair-like correlation survives only if both relevant active sites survive. The ladder therefore has two readings:

| theta_turnover | single-cell scale 1/theta | pair-correlation scale 1/(2 theta) |
| ---: | ---: | ---: |
| 0.02 | 50 ticks | 25 ticks |
| 0.05 | 20 ticks | 10 ticks |
| 0.10 | 10 ticks | 5 ticks |
| 0.20 | 5 ticks | 2.5 ticks |
| 0.35 | ~3 ticks | ~1.4 ticks |
| 0.50 | 2 ticks | 1 tick |

On the pair-correlation reading, theta = 0.02 is already a plausible first competition point for persistence organization against the ~25-tick anchor; 0.05/0.10 cover the faster local-structure regime; 0.20-0.50 cover churn-dominant / endpoint. The ladder spans longer-than-organization, comparable-to-organization, faster-than-organization, and endpoint-churn regimes on both readings. No lower value (e.g. 0.01) and no higher value are added preemptively: if theta = 0.02 destroys signed structure while theta = 0 is signed, that motivates a later low-theta refinement; if 0.35 and 0.50 both stay signed and non-degenerate, a later high-theta extension can be opened; if 0.50 floors or degenerates, the endpoint job is already done. These are named follow-ups, not first-pass additions.

The ladder is justified by spanning the organization time-scale, NOT by any expectation of where near-null lands. Hardening the ladder around a hoped-for near-null setting would convert the design into a LowLow search and is excluded.

---

## Recorded-diagnostic addition (interpretation hygiene; Layer 2-flagged)

The {1/theta} lifetimes are turnover-ONLY lifetimes. If the base Rule C dynamics carry any implicit deactivation, realized active-site lifetime is shorter than 1/theta. This is not a new design requirement and does not change the rule, fences, grid, or success criterion; it is interpretation hygiene. The run record will therefore preserve the set theta_turnover for every setting AND record realized active-site lifetime / churn rate as an output diagnostic, added to the contract Section 8 output metrics alongside the density-confound (4.3) and live-coupling-exposure (4.4) diagnostics. Output only; no control, no feedback (the construction fence forbids theta_turnover adapting to any observed quantity).

---

## What this memo does NOT do

- Does not seed any probe; seeding remains Mike's call after Layer 3 implementation.
- Does not modify the Rule D mechanism, fences, coupling reuse, or the Section 4 bracketing success criterion.
- Does not reopen or reclassify Rule C M2 / A-prime, and does not alter the Comparator 0 / Comparator epsilon floor findings.
- Does not resolve the L4 ontological question; neither observable is named theoretical Psi.
- Does not harden the weak-form Rule B prior.

---

## Next step

Layer 3 (Gemini) implementation of Rule D against these resolved settings, framed as "what the run will produce"; Layer 3 never declares its own L2 clearance. After implementation and parity, seeding is Mike's call to open.
