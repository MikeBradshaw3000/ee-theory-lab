# Rule C M2 first-pass findings

**Status:** CANONICAL. Records the arbitrated reading of the Rule C M2 first-pass behavioral map (`cycle3/data_out/c3_w2_rule_c_m2_results.csv`, script `cycle3/wave_two/c3_w2_rule_c_m2.py`, per-tick states `cycle3/data_out/c3_w2_rule_c_m2_states_*.npz`). The classification below is the Layer 2-arbitrated reading (A-prime), reached after Layer 1 routed two competing readings without pre-deciding. This note is a finding record, not a design document; the contract (`cycle3/wave_two/DESIGN_CONTRACT.md`) governs design.

**Run:** Rule C M2, anchors Lambda = 0.20 and 0.40, common realized-contrast grid c_j in {0, +/-0.05, +/-0.10, +/-0.20, +/-0.35, +/-0.50, +/-0.60, +/-0.80}, baseline-specific kappa constants, seeds 42/137/256/1024/31415, wave-one window structure. 450 rows; 150 per-tick state NPZs. Ran at parity (pre-flight + runtime parity check passed).

---

## 1. The finding (A-prime, Layer 2-arbitrated)

> Rule C M2 first pass produced a complete behavioral map with signed-regime reach at both Lambda anchors. The low/low rows are concentrated at kappa = 0 and the smallest realized-contrast settings (roughly |c| <= 0.10) and disappear as coupling enters the responsive regime. This is recorded as a **floor-adjacent weak-coupling low/low band**, NOT as an away-from-floor substantive low/low candidate. The run gives a clean negative on the specific question of whether Rule C first pass produced a substantive low/low region under nontrivial coupling, while positively establishing that the Rule C family reaches both required signed regimes and a degenerate boundary.

This is a real result, not a failed run. The phrasing is deliberately narrow: NOT "Rule C did not produce low/low" (it produced a lifted, non-degenerate near-null band), but "Rule C first pass did not produce an AWAY-FROM-FLOOR substantive low/low."

## 2. What the map shows (observation)

- **Realized-contrast tracking honest.** Every setting's realized_delta_p matches its target_c exactly; no nominally-nonzero kappa hides a negligible neighbor effect.
- **kappa = 0 reproduces the Comparator 0 floor** at both anchors (near-null / near-null, LowLow firing on essentially all eligible windows). Coefficient-null separability confirmed empirically: kappa = 0 IS Lambda-only.
- **Reach satisfied (precondition met).** The sweep reaches both required signed quadrants at BOTH anchors:
  - negative kappa -> positive meanI / NEGATIVE persistence (large: |c|>=0.5 gives meanI-z +30 to +120 at 0.20, +30 to +60 at 0.40; persistence-z -7 to -11);
  - positive kappa -> positive meanI / POSITIVE persistence (e.g. 0.40 c=+0.8: meanI-z ~+59, persistence-z ~+37);
  - degenerate endpoint reached (0.20 c=+0.8 fires extinction_degenerate, rho ~0.02).
  Because reach is met, any low/low the map emits is NOT rule-forced-by-default.
- **LowLow location:** fires at kappa = 0 and the small flanking settings (|c| <= 0.10), stops as |kappa| grows and observables go signed. The low/low region is centered on kappa = 0, monotone in |kappa|, confined to the smallest contrast settings.
- **Density (M2 payoff):** both anchors show the SAME structure. The agreement is specifically that both reproduce the near-zero-only low/low; density variation did NOT reveal an away-from-zero low/low pocket. M2 did its job; the floor neighborhood is density-stable across the two anchors.

## 3. Why A-prime and not the literal-bracketing reading (B)

The contract's literal four-way text (a near-null band flanked by signed regimes could read as item 4) is necessary but not sufficient by itself. Bracketing protects against a rule whose ONLY behavior is low/low; it does not by itself distinguish a null neighborhood around the OFF-STATE from a mechanism-produced near-null regime. The trivial-stochastic case (item 1) is DEFINED as near-null because nothing is locally coupled. Both clauses read together.

Arbitrated classification rule (Layer 2):

> "Contains kappa = 0" is NOT by itself sufficient to classify a band as floor. But a band centered on kappa = 0, monotone in |kappa|, confined to the smallest contrast settings, AND reproduced at both density anchors should be read as floor-adjacent UNLESS it survives beyond a predeclared weak-coupling zone.

The current map is exactly that band, so it reads floor-adjacent.

## 4. The discriminating test (Layer 2-arbitrated)

Nonzero low/low WIDTH around kappa = 0 is NOT the test — almost any continuous stochastic update has nonzero width near zero under a hard LOW_Z_THRESH = 2.0. Width proves weak-coupling tolerance, not substantive candidacy. The test is:

> Does LowLow persist OUTSIDE the independently-defined weak-coupling zone, at realized-contrast values large enough that the neighbor term is no longer a Comparator-epsilon-scale perturbation?

First-pass interpretation thresholds (derived from the grid design, NOT universal theoretical constants):

    |c| = 0      exact Comparator 0 / Lambda-only point
    |c| = 0.05   floor-neighborhood / tiny departure
    |c| = 0.10   weak-coupling tolerance zone
    |c| = 0.20   first clearly responsive Rule C setting
    |c| >= 0.35  substantive coupling / signed-regime map
    |c| = 0.80   boundary / degeneracy probe

Working first-pass threshold: **|realized_delta_p| >= 0.20 is the minimum for "genuinely responsive coupling"; |c| <= 0.10 is floor-adjacent** unless Comparator epsilon later establishes a stricter ceiling. LowLow fires only through |c| <= 0.10 here, so it is floor-adjacent.

## 5. What WOULD make a substantive reading live (carried for future passes)

A full substantive low/low reading would require one of:
- a near-null pocket AWAY from zero, not contiguous with the Lambda-only point;
- a near-null plateau extending past the weak-coupling zone into |c| >= 0.20;
- a non-monotone return to near-null AFTER signed structure appears;
- density-specific structure where one anchor produces a nonzero-coupling low/low region the other does not.

The current map shows NONE of these.

## 6. Comparator epsilon's role, sharpened by this finding

Comparator epsilon is the next instrument: it FORMALIZES the weak-coupling floor zone (how much weak nonzero local coupling the apparatus-null floor absorbs before signed structure appears), NOT a retroactive rescue of a candidate reading. If epsilon later shows even |c| = 0.05 is above the weak-coupling ceiling, the 0.05 / 0.10 rows become more interesting — but because the band is centered on zero and monotone outward, they would be labeled weak-coupling low/low SURVIVAL, not yet a full substantive low/low regime. Epsilon does not convert floor-adjacent into substantive by construction.

## 7. Map-texture cautions (downstream reading; not part of the central call)

- At Lambda = 0.20, high positive coupling produces positive meanI while rho collapses toward extinction (organization on a vanishing population). Fence as degenerate-endpoint / boundary contrast, NOT a clean eligible signed regime where earned-window diagnostics fail there. The positive/positive regime at lower positive contrast (c = +0.20) is the more important reach evidence (responsive region, not high-curvature endpoint).
- Persistence-sign at matched positive coupling is not identical across anchors in places. Downstream signed-map texture; does NOT change the A-prime call.

## 8. What this finding does NOT do

- Does not resolve the L4 ontological question; neither observable is named theoretical Psi.
- Does not harden the weak-form Rule B prior.
- Does not close Rule C as a mechanism (first pass; the future-pass patterns in Section 5 remain open).
- Does not specify or run Comparator epsilon (next instrument; Section 6 is its sharpened role, not its spec).
- Does not seed any further probe; seeding remains Mike's call.

## 9. Registry-form summary

> **Rule C M2:** behavioral-map reach satisfied at both Lambda anchors. LowLow appears only in the near-zero / weak-coupling neighborhood of the Lambda-only point (|c| <= 0.10) and is density-stable across anchors. Classified (Layer 2-arbitrated, A-prime) as floor-adjacent weak-coupling tolerance, NOT item-4 substantive-candidate low/low. Comparator epsilon remains the next instrument for bounding the weak-coupling floor zone.
