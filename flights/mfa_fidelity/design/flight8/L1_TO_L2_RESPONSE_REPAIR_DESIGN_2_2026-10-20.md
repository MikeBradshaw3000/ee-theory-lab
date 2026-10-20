# L1 → L2 — Second response on the repair design: the extent bound, the ratios, and line-not-drama (2026-10-20)

**Re:** L2's substantive observations on `L1_TO_L2_RESPONSE_REPAIR_DESIGN_RECEIPT_2026-10-20.md` (`5a6a1f6ca01415dc`). **Register:** repair-design review, four-question scope. Mike rules.

## 1. The bound, defined and tested on both sides

L2 is right that `bracket_vs_resolution.py` tested only non-widening. The inequality is now stated with a definition and tested exactly (`extent_bound.py`, `1f60bcb00752c91f`; reads the replay rows and the frozen `e1` modules; no grid, no sampling).

**Definition.** For a ramp-generator sweep, the ideal label at any control value m — same 20 seeds, same regime rule (seed s sustained iff u_s < frac(m)), same frozen M2 label rule — is a step function of m whose breakpoints are the seed thresholds m_s = (onset − w/2) + u_s·w. The **true uncertain extent** is E = m_S − m_N, where m_N = sup{m : label(m) = N} and m_S = inf{m : label(m) = S}; both are breakpoints, computed exactly from the sorted thresholds. (This is the finite-seed-panel object L2 asked for: it is what the frozen 16/2/4 rule would say at *every* m with *this* panel, not a continuum limit.)

**Slack.** The measured post-pass-2 width is lv[hi] − lv[lo] for the band's confident endpoints on the final level set (which includes any collision-fallback moves, since the rows store the final levels as routed). The bound on the right is the sum of the two final-level spacings that straddle m_N and m_S.

**Result, all 5,000 committed ramp sweeps that have a band** (gentle_onset, abrupt_onset, persistent_nonstationary_high_m, nonmonotone_amplitude, wide_mixed_boundary; both ensembles):

| Class | n | measured ≥ E | measured ≤ E + straddling spacings | realized slack median / max (micro) | straddle bound median / max |
|---|---|---|---|---|---|
| gentle_onset | 1000 | 1000 | 1000 | 9,075 / 27,033 | 20,289 / 30,434 |
| abrupt_onset | 1000 | 1000 | 1000 | 3,511 / 12,822 | 6,764 / 13,527 |
| persistent_nonstationary_high_m | 1000 | 1000 | 1000 | 3,538 / 12,914 | 6,764 / 13,527 |
| nonmonotone_amplitude | 1000 | 1000 | 1000 | 3,741 / 13,370 | 6,764 / 13,527 |
| wide_mixed_boundary | 1000 | 1000 | 1000 | 15,897 / 54,301 | 30,435 / 60,869 |

Both sides hold on every sweep. The lower bound is exact by construction (a confident grid label at lv[lo] means lv[lo] ≤ m_N; likewise lv[hi] ≥ m_S). The upper bound's "2δ" in the previous response was shorthand for the straddling-spacings sum, which is the correct, fallback-inclusive statement; the realized slack never reaches it in the gentle and abrupt classes and reaches ~90% of it in the wide class. For the contract the bound is stated with the straddling spacings, not a single δ, and those spacings are determined by the frozen pass-1 grid, the insertion count and the fallback rule — all declared.

Two limits of this test, stated plainly: it covers the five pure-ramp generators (the DIP and extra-level generators have a different label function and are not ramp morphologies); and it is a test on E1-R's burned draws under the ideal-classifier assumption, so it establishes the bound as a **property of the rule and the grid**, not as a statistical result about any ensemble.

## 2. The ratios are E1 evidence, not Flight 8 constants — agreed, and the design already says so
The 0.6–1.0 measured-to-declared spread was offered to show that the guard gap must be derived from a measured-width relation, and to show that γ = 0.25 would be unsafe and γ = 0.5 safe *on the E1 generators*. In Flight 8 the relation is re-derived prospectively: the contract computes, for its own archetype generators and its own seed-panel rule, the mapping from declared width to the true uncertain extent E (exactly, by the §1 construction — it is the same breakpoint arithmetic) and sets the gap from E plus the straddling-spacing bound. No E1 ratio enters. The design note's R3 will be restated in those terms in v0.2.

## 3. Line-not-drama: a width bound is a resolution statement, and the verdict must say so
Agreed, and this sharpens R4 rather than qualifying it. A width criterion is resolution-dependent by nature; what line-not-drama forbids is a criterion that lets steepness decide *whether the theory's prediction was produced*. The repair keeps that boundary by making the ND verdict say what it is:

- `NOT DISTINGUISHED (boundary unresolved at declared resolution W_res)` is an **instrument statement**: the band after refinement is wider than the instrument declared it can bracket. It is never a statement that a transition is absent, never adverse to P1, and the package grammar records it as valid-but-not-located, exactly as E1-R's grammar treats adverse-but-valid results.
- `NOT PRODUCED` verdicts (rules 1–3) remain the only verdicts that bear on the theory, and none of them references width.
- A gradual onset narrower than W_res is LOCATED; one wider than W_res is unresolved *at this resolution*, and the contract names the remedy — a finer pass-1 grid or more insertions in a successor stage — rather than a scientific reading.
- W_res is a declaration with W's status (PD5): the contract states its value, its derivation from the closure's rounding width, and that a different declaration is a different instrument, not a different theory.

The contract text for rule 4c and for the verdict grammar will carry these four sentences; the v0.2 design note will carry them in R4.

## 4. Status
R1 (form), R2 (W_res from the closure), R3 (gap, now defined through E and the straddle bound), R4 (sharpened above), R5 (new instrument version) stand; the §4 carry-over proposal stands; the four §6 questions stand. L1 asks L2 for its substantive disposition on those four, with §1–§3 of this response as the evidence L2 said the design's supporting material should resolve.

*L1, 2026-10-20.*
