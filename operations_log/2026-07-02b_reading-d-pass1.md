# Operations log - 2026-07-02b - Reading-D pure-read pass 1: run, arbitration, findings

**Session:** 2026-07-02 (second segment, slug 2026-07-02b_reading-d-pass1)
**Layer 1:** Claude; **Execution channel:** Mike (sole); **Layer 2:** ChatGPT (arbitration); **Layer 3:** not engaged
**Entry HEAD:** 99a1649 (pattern synthesis committed; pure-read program opened)
**Exit HEAD:** this commit (findings + this ops log + anchor refresh)
**Result:** POSITIVE DISCRIMINATION - Readings B and D jointly confirmed (propensity / measurement levels), jointly sufficient for the invariant; Reading A bounded near-empty at the tested base; no class closed; L4 untouched

## The pass

Layer 1 drafted the pass-1 pure-read script keyed to the real NPZ inventory (a discovery listing surfaced two scope limits recorded in the findings: no Comparator 0 NPZs - kappa=0 anchors the floor; no Rule D NPZs). Two execution defects were caught and fixed in-flight, both Layer 1's: (1) the Rule C filename token omitted the _s seed prefix (Layer 1's inventory grouping masked the wave-two naming; MISSING rows surfaced it); (2) the M2 family is 200-tick (wave-one structure), not the assumed 400 - the first floor read crashed on an empty window slice; per-family windows fixed (single t>=100 window for 200-tick files, same length and convention). Corrected script run clean: 12 settings x 5 seeds, raw effects + C1/C2/C3 controls + propensity-surface autocorrelation. A whole-window time shuffle was rejected at design time as invariant for both observables; the informative per-cell independent form was predeclared instead.

## Results and arbitration

Floor: all axes at shuffle floors, prop_I ~ 0 (constant surface at kappa=0). Live mechanisms: prop_I ~ +0.38 both signs; raw meanI ~ +0.004-0.011 (~1-3% retention); raw persistence ~ |0.05-0.07| (~13-18% retention; the measured axis asymmetry); C3 collapses meanI everywhere (genuine synchrony). Committed z ~ 4-12 on raw ~0.005. E1 oscillatory tier prop_I ~ 0 (railed channel flattens the surface). RC rows reproduce E1 baselines exactly (free F3-level read consistency check).

Routing note: L2's first return was a technical-fault artifact - a from-memory restatement of the already-committed pattern synthesis (its uploads had expired), not an engagement with pass 1. Caught by the genuine-engagement tell (no contact with the specific numbers); the self-contained packet was re-routed and the real review returned. The restatement itself confirmed the committed synthesis unchanged; recorded here, no canonical action.

The genuine review: decomposition CONCURRED (three stages sufficient for the invariant; floor contrast causal; sign-independence confirms [b'_eff]^2 specifically; controls stand). Reading-A bound (L2 technical assessment): admissible Rule E acts THROUGH the propensity surface, whose autocorrelation is geometric at nonzero effective slope - the clean-responsive form is bounded near-empty at the tested base; B/C stays HELD; disposition Mike's. Recording refinements (L2): quantified per-family attenuation ratios; persistence-integrates-more recorded as measured; explicit L4 fence (behavior measured, not identity). Mike concurred.

## Committed this bundle (one commit)

READING_D_PASS1_FINDINGS.md (canonical at cycle3/wave_two/; governs the pass-1 result), this ops log, anchor refresh. Read scripts were Downloads-side transit tools (repo tree untouched; no gitignore needed).

## What remains Mike's call

The wave-two CONTINUE-OR-REST arbitration - now equipped with the B+D decomposition and the Reading-A bound. B/C held. Cross-direction extension, Rule D turnover extension, Rule C object (b) unchanged named-not-triggered. Manuscript back-flow to v1.5 (and a Phil-facing summary of the wave-two record) named as parallel work.

Drafting partner: Layer 1 (Claude), routed and executed by Mike.
