# TEST RECORD - C3-CTL-001 Synthetic control battery (positive + negative + degeneracy)

> Copy of TEST_RECORD_TEMPLATE.md, filled for C3-CTL-001. Pre-execution block written at design-phase open; execution and post-execution blocks left for Mike. Execution channel is Mike only; no layer executes.

---

## Pre-execution (write before running)

**Test ID:** C3-CTL-001
**Test name:** Synthetic control battery (positive + negative + degeneracy)
**Registry status at open:** planned -> ready
**Date opened:** 2026-05-25

**Purpose - the question this test answers:**
> Does the Cycle 3 observable apparatus, at the locked 50x50 toroidal Moore-1 topology, produce the designed five-case discrimination on synthetic arrays with no substrate dependence? (The possible "no": if it fails to produce the discrimination, the apparatus is not validated and no real-substrate value may be interpreted.)

**Theoretical target - which part of Regime-II-as-structural this bears on:**
> Measurement-validity precondition: no real-substrate value is interpreted before the battery passes at the substrate's own topology. It bears on the co-equal observable pair but does NOT presuppose which candidate is Psi. The transient-wave case (Case D) is where the pair diverges by design; that divergence is recorded as data, not as a tiebreaker.

**Level this test is designed to address:** L1 and L2.
> By construction it cannot reach L3 or L4: the cases are synthetic arrays with no steady-state window to earn, and nothing is interpreted for Regime-II-as-structural.

**Inputs and parameters:**
> Topology: 50x50 grid, Moore radius 1 (8-neighbor), toroidal. No substrate / no parquet - synthetic arrays by construction. Observable: Psi_meanI_state and Psi_persistence_I, both Moran's-I-based, computed with the 8-neighbor toroidal adjacency that matches this substrate (the Cycle 2 encoding carries over, being parametric in grid size). Five cases, scale-parametric at this topology - the case STRUCTURE and target regimes are fixed here; the exact proportions, window length, and permutation count are set by Layer 3's draft (Cycle 2 reference values given for orientation, to confirm or revise with justification, never to copy as cross-scale-comparable):
> - Case A (positive - stable cluster): contiguous block at a fixed FRACTION of the grid (Cycle 2 ref ~0.1225), held constant across the window.
> - Case B (negative - random low-rho): random placement at the SAME rho as A. The shared rho is load-bearing - it isolates structure from density.
> - Case C (negative - random high-rho): random placement at high rho (Cycle 2 ref ~0.80).
> - Case D (transient wave): a moving band of fixed FRACTIONAL width, wrapping (toroidal-admissible), advancing per tick.
> - Case E (degeneracy - uniform high persistence): every cell active in a fixed high fraction of ticks (Cycle 2 ref ~0.70), independently shuffled.
> Window length, permutation count (Cycle 2 refs: 100 ticks, 199 permutations), and seed(s) to be set by Layer 3 / recorded at run.

**Script name and version:**
> New to Cycle 3 - a fresh scale-parametric battery at 50x50 toroidal Moore-1, drafted by Layer 3 and reviewed by Layer 2. NOT phase_4b/scripts/psi_state_spatial_v2.py - that is the inherited reference structure, not to be overwritten or treated as the Cycle 3 canonical. Path and version tag at draft.

**Expected data produced:**
> Per-case observable values (Psi_meanI_state, Psi_persistence_I) and their permutation-null z-scores, a controls summary, and the case definitions as generated. Output directory under cycle3/ (path at draft).

**Expected output / pass criterion - stated per level:**
- L1 (implementation): the battery runs without error at 50x50; outputs finite and well-formed.
- L2 (measurement validity):
  - Case A: both observables high-positive.
  - Cases B and C: both observables near zero.
  - Case D: Psi_meanI_state high-positive while Psi_persistence_I near zero - the designed divergence, recorded as data, NOT a failure.
  - Case E: both observables near zero, with the permutation-null z separating the uniformity degeneracy from true signal (low P_std flagging the degeneracy).
  - All thresholds ("high," "near zero," "significant") set from THIS grid's own null distribution. No comparison to 20x20 raw or z magnitudes.
  - Case definitions verified as scale-parametric (proportions / fractional widths, not fixed cell counts carried from 20x20).
- L3 (steady-state eligibility): not applicable by construction.
- L4 (interpretation): not applicable - the battery is machinery, not evidence for Regime-II-as-structural.

**Positive control:**
> Case A (stable cluster) - must produce a clear signal on both observables before any output is interpreted.

**Negative control:**
> Cases B and C (rho-matched and high-rho random scrambles) near zero; Case E (uniform high persistence) as the degeneracy check, near zero with permutation-null z separation. These distinguish "no coherence" from a measurement artifact.

**Interpretation boundary - declared in advance:**
> A pass establishes that the observable apparatus, at 50x50 toroidal Moore-1, computes the intended state-based, density-adjusted quantities and discriminates correctly on synthetic controls. It does NOT establish anything about real-substrate values, steady-state eligibility, or Regime-II-as-structural. It does NOT settle which observable is Psi - the Case D divergence is data on the co-equal pair. Seam: implementation / measurement (Layer 3 / Layer 2) vs meaning (Mike / Layer 1).

---

## Execution (Mike only)

**Date run:**
**Machine / environment:** _(confirm venv interpreter path per MESA_ENVIRONMENT_REPRODUCTION)_
**Actual command run:**
```
<paste verbatim>
```

**Output files generated:**
> Paths + brief note that each is well-formed.

---

## Post-execution (write after running)

**Highest level cleared:** L1 / L2
> "Script ran" = L1 only. L2 requires the full discrimination above, with controls.

**Result summary:**
> What the battery produced, in vocabulary-disciplined terms. Candidates produce or fail to produce. Report each value with its control.

**Control outcomes:**
- Positive control (Case A):
- Negative controls (Cases B, C, E):

**Steady-state eligibility outcome (if applicable):**
> Not applicable - synthetic battery.

**Interpretation (L4 - Mike / Layer 1 only):**
> Expected to remain withheld: this test is machinery validation, not interpretation.

**Divergence note (co-equal pair):**
> Case D is the expected-divergence case. Record the Psi_meanI_state / Psi_persistence_I disagreement as data; do not collapse it to one reading.

**Follow-up decision:**
> On L2 pass: the apparatus is validated at this topology, unlocking real-substrate measurement at 50x50 toroidal Moore-1. Update the registry row.

**Registry status at close:**
