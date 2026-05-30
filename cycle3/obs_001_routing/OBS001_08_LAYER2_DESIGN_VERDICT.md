# OBS001_08 - Layer 2 design verdict (accept-with-edits)

Source: Layer 2 (ChatGPT), responding verbatim to OBS001_07.

---

# Layer 2 substantive review - wave-one design menu A+B

## Verdict

**Accept-with-edits.**

The v2 design menu is substantively strong enough to proceed to a code-production contract after two bounded edits are folded into that contract. I do **not** think this needs a v3 design-menu round-trip to Layer 3 before code drafting. The edits are telemetry/criterion refinements, not a rejection of the A+B design.

The two required edits are:

1. **Add an explicit low/low degeneracy diagnostic** before code production. The design must distinguish saturation low/low, extinction low/low, and lifted non-degenerate low/low. This distinction cannot remain merely implicit.

2. **Expand Rule A's meaningful-failure criterion** so Rule A fails not only if it produces a divergent high/low or low/high signature, but also if it produces a lifted, non-degenerate low/low Regime-II-candidate signature on 5/5 seeds. Rule A is the both-agree sanity baseline; if it produces the Regime-II-candidate signature reliably, that is just as important as if it produces a divergent signature.

Everything else can advance.

---

## 1. Overall design-menu assessment

The v2 menu satisfies the main contract shape. It keeps the A+B scope Mike ratified, preserves Rule A as the both-agree baseline, keeps Rule B as the first divergence probe, defers Rule C, preserves the co-equal-pair guard, and keeps L4 interpretation empty. The design also correctly attaches ENV/CTL/SS to the run classes rather than treating precondition clearance as theory support.

I also agree that this is a **design menu**, not code, and that a separate code-production contract is the next step after Layer 2 clearance. That framing is important and is correctly stated in the package.

---

## 2. Item 1 - Rule A endpoint picture

Layer 3's substrate-grounded picture is analytically plausible enough to use as the wave-one expectation:

* low tau_A -> uniform saturation;
* intermediate tau_A -> locked/static structures if active mass survives;
* high tau_A -> extinction.

The most important claim is preserved: Rule A is **non-discriminating** across Lambda_A. It is expected to move the two observables together, not to produce either the divergent signature or the Regime-II-candidate signature.

The endpoint correction is worth recording. The older "high tau_A -> locked clusters" description was too coarse. At high enough tau_A, extinction is the natural outcome because a cell needs many active neighbors to remain or become active. Locked clusters live more plausibly in the intermediate range, not the high end.

One nuance: tau_A = 5 may not reliably be a locked-cluster region at starting rho ~ 0.10. It may sometimes extinguish. That is not a design defect because the full tau_A in {1,...,8} sweep is explicitly intended to let the substrate adjudicate where the regimes actually fall. But the expected-outcome language should remain "expected/falsifiable," not become a pre-judgment.

### Recommendation

Accept the Rule A endpoint amendment as a close-out record correction. No design re-route needed.

---

## 3. Item 2 - explicit degeneracy diagnostic is required

This is the main required edit.

The v2 menu distinguishes three low/low states:

* saturation: rho ~ 1, low/low degenerate;
* extinction: rho ~ 0, low/low degenerate;
* Regime-II-candidate: rho lifted with low/low **non-degenerate** coherence signatures.

That distinction is too important to leave implicit. The `Lifted_Activation_Candidate` flag is one-sided, so saturation will also pass "lifted" even though it is not a Regime-II-candidate low/low state. The file itself names this concern: distinguishing Regime-II-candidate from saturation requires a non-degeneracy diagnostic.

### Required telemetry additions

Add per-window diagnostics:

1. `mean_active_state_variance`
   Mean over ticks of the spatial variance of per-cell active-state values. For binary values this is equivalent to mean of rho_t(1-rho_t), but computing it from the matrix is clearer.

2. `persistence_variance` or `P_std`
   Spatial variance or standard deviation of the persistence grid. This detects uniform persistence degeneracy.

3. `extinction_degenerate`
   Suggested definition: `mean_rho <= 0.05`, matching the existing lifted threshold.

4. `saturation_degenerate`
   Suggested first-pass definition: `mean_rho >= 0.95` **or** `mean_active_state_variance` below a small epsilon. I would report both the thresholded flag and the underlying continuous value.

5. `lowlow_nondegenerate_candidate`
   A descriptive flag, not an L4 interpretation:

   * lifted activation true;
   * not extinction;
   * not saturation;
   * low/near-null `Psi_meanI_state`;
   * low/near-null `Psi_persistence_I`;
   * active-state variance not degenerate.

Do **not** call this `Regime_II`. It should be an apparatus-level label such as:

`LowLow_Nondegenerate_Candidate`

or

`Lifted_LowLow_Nondegenerate`

This preserves the distinction between measurement classification and manuscript interpretation.

### Why this is required before code

Without this diagnostic, saturation and genuine lifted non-degenerate low/low can both appear as "lifted low/low." That is exactly the kind of interpretive slide Cycle 3 was designed to prevent.

So: accept-with-edits, and the edit should be in the code-production contract.

---

## 4. Rule A meaningful-failure criterion needs one addition

The current Rule A meaningful-failure criterion says Rule A fails if any Lambda_A value produces a divergent joint signature on 5/5 seeds. That is necessary but incomplete.

Rule A is supposed to be the non-discriminating sanity baseline. The design also explicitly expects no Regime-II-candidate signature from Sweep A.

So the failure criterion should become:

> Rule A meaningful failure occurs if any tau_A value produces either (a) a divergent high/low or low/high signature on 5/5 seeds in earned steady-state windows, or (b) a lifted, low/low, non-degenerate candidate signature on 5/5 seeds in earned steady-state windows.

Reason: if Rule A produces the Regime-II-candidate signature reliably, it is no longer serving as the baseline the design claims it is.

This is a contract edit, not a new design round.

---

## 5. Sweep B expectations

The Sweep B expectations are acceptable as hypotheses for a first wave:

* `[2,4]` as the candidate lifted low/low / "boiling" regime;
* `[2,3]` as the expected moving-structure divergent regime;
* `[1,2]` and `[3,4]` as boundary cases.

I would phrase `[2,4]` carefully. It is **expected** to produce a Regime-II-candidate signature, but this is exactly what the run must test. It should not be treated as pre-classified.

For code-production, the key is that the outputs should allow `[2,4]` to fail cleanly:

* it may become high/high;
* it may become high/low;
* it may freeze;
* it may extinguish;
* it may produce no earned windows.

All are valid outcomes.

### Are the bands well-spaced?

Good enough for wave one. The set `{[1,2], [2,3], [3,4], [2,4]}` gives a short feedback loop and samples low, middle, high, and wider-band behavior. It is not exhaustive, but it is appropriate before bringing in Rule C or broader band sweeps.

---

## 6. Five seeds and 60 runs

Five seeds per parameter value is sufficient for a **first design wave**, not for final statistical inference.

The design uses 60 runs: 8 tau_A values + 4 Rule B bands, each with 5 seeds. That is a reasonable short feedback loop.

I would add one interpretive discipline:

> 5/5 is a hard meaningful-failure rule, but 3/5 or 4/5 should be treated as a design signal requiring review, not ignored.

This prevents an overly binary interpretation of the first wave. A 4/5 divergent outcome under Rule A, for example, would still matter even if it does not meet the hard-fail criterion.

---

## 7. Gate attachment and four-level structure

Accept.

The gate attachment is clean: ENV licenses implementation environment, CTL licenses observable math and grid-local nulls, SS licenses earned-window and lifted-window classification. The design correctly leaves L4 empty and holds interpretation for Mike / Layer 1.

The co-equal-pair guard is also clean. Neither observable is named theoretical Psi; SS flags remain independent; CTL Case D divergence remains measurement-validity data, not an ontological tiebreaker.

---

## 8. Framing and vocabulary

Accept.

The package holds the right framing discipline: candidates produce or fail to produce; no "confirms," no "demonstrates," no L2-clearance claim by Layer 3.

Vocabulary discipline is also clean in the v2 menu. No issue.

---

## Final verdict

**Accept-with-edits.**

No v3 design-menu round-trip is needed. Layer 1 can incorporate these edits into the code-production contract.

Required edits before code production:

1. Add explicit low/low degeneracy diagnostics:

   * mean active-state variance;
   * persistence-grid variance or `P_std`;
   * extinction-degenerate flag;
   * saturation-degenerate flag;
   * lifted low/low non-degenerate candidate flag.

2. Expand Rule A meaningful-failure criterion:

   * failure if divergent signature on 5/5 seeds;
   * failure also if lifted low/low non-degenerate candidate signature on 5/5 seeds.

3. Add record/contract note:

   * Rule A endpoint description amended: high tau_A tends toward extinction, with locked clusters expected in the intermediate range if active mass survives. Main non-discriminating baseline claim stands.

Optional but recommended:

4. Treat 3/5 or 4/5 off-expectation outcomes as design signals requiring review, even if 5/5 remains the hard meaningful-failure threshold.

After those edits, proceed to a separate code-production contract.
