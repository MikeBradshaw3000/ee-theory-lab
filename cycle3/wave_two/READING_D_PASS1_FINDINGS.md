# Reading-D pure-read pass 1 - findings (positive discrimination: B and D jointly confirmed)

**Status: FINDINGS. Layer 2-arbitrated 2026-07-02; Mike-concurred. Governs the Reading-D pass-1 result.** Executed per the predeclared design in WAVE_TWO_PATTERN_SYNTHESIS.md (which governs the program); pure read of committed NPZs; no seed, no Layer 3. Scope limits held and recorded: Comparator 0 saved no NPZs (the Rule C kappa=0 Lambda-only setting anchors the floor, M2-confirmed equivalent); Rule D R3 saved no NPZs (outside this spatial pass); Rule E first-pass positive nonzero tiers excluded as extinction-degenerate. Read-level consistency check passed free: Rule C +/-0.7599 raw columns reproduce the Rule E alpha=0 baselines exactly (F3 bit-exactness visible at the read level).

## Result

**The pass PRODUCES a positive discrimination. Readings B and D are JOINTLY CONFIRMED, at the propensity and measurement levels respectively, and are jointly sufficient for the wave-one/wave-two invariant.** The three-stage decomposition:

1. **Propensity level (Reading B, confirmed):** every live local mechanism builds a strongly spatially autocorrelated birth-propensity surface - prop_I ~ +0.38 at the c=+/-0.35 base, UNDER BOTH COUPLING SIGNS (the sign-independence the [b'_eff]^2 pair-level argument requires), and prop_I ~ 0 at the kappa=0 floor where the propensity surface is constant by construction. The floor contrast identifies the propensity surface as the causal variable. The pair-level mechanism is directly measured, not conjectured.
2. **Realization attenuation (measured):** Bernoulli realization erases most of the propensity structure in the state field. Per-family attenuation ratios (raw realized Moran / propensity Moran): per-tick Psi_meanI_state retains ~1-3% (raw ~+0.004 to +0.011 against prop_I ~0.38); Psi_persistence_I retains ~13-18% (raw ~|0.05-0.07|) - **persistence integrates more of the propensity structure than the per-tick state; the measured axis asymmetry.** C3 (per-cell time shuffle, persistence-grid-preserving) collapses meanI to its floor everywhere: the per-tick residue is genuine cross-cell synchronous patterning, not static heterogeneity.
3. **Measurement level (Reading D, confirmed):** the committed z ~ 4-12 sits on raw Moran effects of ~0.005; the grid-local permutation null is overpowered relative to raw realized effect size. The invariant "everything lifted is organized, hugely significantly" decomposes exactly as: real-but-small realized residue of a large propensity structure, detected by a powerful null.

Limit case (interpretable): the Rule E first-pass oscillatory tier shows prop_I ~ 0 - the railed +/-50-logit channel pins p_become uniformly, flattening the propensity surface itself. Railing destroys the structure the pair-level argument is about.

## Reading A bounded (Layer 2 technical assessment; disposition Mike's)

Every admissible Rule E construction conditions locally-configured Lambda on the becoming-active channel - it acts THROUGH the propensity surface. A clean-responsive channel changes how that surface moves over time; it cannot decouple lifted activation from propensity autocorrelation, which is geometric (shared Moore neighborhoods) whenever the local rule has nonzero effective slope at lifted density. The measured prop_I ~ 0.38 at the c=+/-0.35 base is what any conditioned variant inherits. **Reading A's remaining live form (the clean-responsive rescaled channel) is therefore bounded to near-empty at the tested base:** such a pass could be run, but its plausible ceiling on realized joint near-null is set by the same structure that produced every prior scoped negative. The B/C design question remains HELD; whether it is worth opening under this bound is Mike's arbitration.

## Reading C (measurement component) and L4

The measurement component of Reading C is partly answered: the co-equal pair detects REAL organization (C1/C2/C3 controls confirm the residues are genuine); it detects very little of it very significantly. **The L4 component is untouched and fenced:** this pass measured how the observables BEHAVE under lift, not what they ARE. Neither observable is named theoretical Psi; nothing here bears on Regime-II identification.

## What this pass does not do

Closes no mechanism class (all wave-two rests stand as scoped negatives, unreclassified). Does not resolve L4. Does not decide wave two's continuation - the continue-or-rest arbitration is Mike's, now equipped with the B+D decomposition and the Reading-A bound. Does not harden the weak-form Rule B prior beyond its measured propensity-level content. The read scripts (read_d_pass1.py / read_d_pass1b.py) were Downloads-side pure-read tools; the committed NPZs and this file are the record.

- Layer 1 (Claude); Layer 2-arbitrated (decomposition concurred; Reading-A bound is an L2 technical assessment; recording refinements - quantified attenuation, axis asymmetry, explicit L4 fence - are L2 contributions); Mike-concurred
