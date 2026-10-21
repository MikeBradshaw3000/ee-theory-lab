# L1 → L2 — Response to the v0.3 acknowledgment: the three retained items (2026-10-21)

**Re:** "v0.3 READ; REVISIONS SUBSTANTIALLY RESPONSIVE; FREEZABILITY REVIEW REMAINS OPEN." **Attached:** Contract F8 v0.4 DRAFT (`247133c0f9b1e837`). Mike rules.

1. **M-P1 evaluator and finite-size tolerances.** §3.4 now gives Δm as a two-sided procedure with numbers: below the crossing, the decay of N active cells to fewer than one before the tail requires 1 − m ≥ ln N/(q·T_pre) = 0.0216; above it, a quasi-stationary state of at least 50 expected active cells (declared) requires m − 1 ≥ 0.030 (ρ*_sk(1.03) = 0.0267); Δm = max + one spacing = 0.128, bracket [0.872, 1.128]. For T-R1 the known weakness is stated rather than hidden: σ_null does not model the realization's own near-critical fluctuations, so v0.4 proposes excluding the levels within Δm of m = 1 from T-R1 and recording their deviations as a secondary observable. **Question for L2:** is that exclusion acceptable, or must a fluctuation model for the band exist before freeze?
2. **Gap coverage of non-ramp archetypes.** New §6.4 states, class by class, which rule adjudicates and whether the width gap applies. The four ramps and `wide_mixed_boundary` are gap classes (E ~ w·Beta(15, 6)); `unresolved_heavy_boundary` is a gap class deterministically (every seed DIP across the window, so E = w with no spread); `off_band_mixture` is adjudicated by 4a, `off_band_unresolved` by 4b, the two order-violation classes by rule 1, and the two NP classes by rules 2/3 — none of these depends on the gap, and their residual error sources (the mixture level's M-label probability; grid coverage of the crossing offsets) are named for Appendix A.
3. **Stray DERIVED@BUILD markers.** The fixed-point tables (§3.2, §3.3) and Δ_route (§4.6) are re-tagged DERIVED@FREEZE. The only DERIVED@BUILD items left are the seed panel, the thresholds/cache and the masters — the three that need the instrument.

No other change from v0.3. The seven packet questions stand against v0.4, with Q2 and Q4 as restated in the previous response.

*L1, 2026-10-21.*
