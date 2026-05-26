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

**Date run:** 2026-05-25 _(session date per operations_log/2026-05-25_c3_ctl_001_closure.md; confirm exact run date if it differed)_
**Machine / environment:** Captured C3-ENV-001 environment - top-level venv, Python 3.14.4, Mesa 3.5.1, numpy pinned 2.4.4. _(confirm venv interpreter path per MESA_ENVIRONMENT_REPRODUCTION)_
**Actual command run:**
```
python cycle3\c3_ctl_001_battery.py
```
> _(Reconstructed from script structure: the battery runs via its `__main__` entry, which sets `np.random.seed(42)` and calls `run_battery()`; it writes to the relative path `cycle3/data_out/`, so it is run from the repo root. Confirm the verbatim invocation if it differed - e.g. an explicit interpreter path.)_

> Run parameters (from cycle3/c3_ctl_001_battery.py): seed = 42; window = 100 ticks; permutation count = 199; grid 50x50, 8-neighbor toroidal Moore-1 adjacency. Case definitions are literal at 50x50 (Case A a 10x25 = 250-cell block at rho 0.10; B 250 active cells at rho 0.10; C 2000 active cells at rho 0.80; D a 5-wide band advancing one column per tick; E every cell active 70 of 100 ticks, independently shuffled) - correct proportions for this grid, not carried from 20x20, and read within-topology only. The script is a per-topology instrument; the constants are fixed to 50x50, not written as fractions, so regenerating controls at a different topology means editing those constants.

**Output files generated:**
> `cycle3/data_out/c3_ctl_001_results.csv` - the five-case controls summary (Case, Mean_Rho, Psi_meanI_state, MeanI_Z, Psi_persistence_I, P_std, Persistence_Z), one row per case. Well-formed; committed at 1c35283.

---

## Post-execution (write after running)

**Highest level cleared:** L2
> Beyond "script ran" (L1): the battery produces the full designed five-case discrimination, with both observables grounded against their own grid-local permutation nulls (a per-tick within-tick-shuffle null for Psi_meanI_state; a persistence-map null for Psi_persistence_I).

**Result summary:**
> The apparatus produces the designed five-case discrimination at 50x50 toroidal Moore-1. Each value below is read against its own grid-local null (z-scores from this grid's permutation distribution; no cross-topology magnitude comparison):
> - Case A (stable cluster, positive control, rho 0.10): Psi_meanI_state 0.8856 (MeanI_Z 914.45), Psi_persistence_I 0.8856 (Persistence_Z 91.29). Both observables produce a high-positive signal. A static block reads identically per-tick and in the persistence map, so the two observables agree by construction here.
> - Case B (random low-rho, negative control, rho 0.10 - rho-matched to A): Psi_meanI_state -0.0021 (MeanI_Z -1.70), Psi_persistence_I 0.0014 (Persistence_Z 0.22). Both near null. The shared rho with A isolates structure from density: same activation density, no signal.
> - Case C (random high-rho, negative control, rho 0.80): Psi_meanI_state -0.0011 (MeanI_Z -0.59), Psi_persistence_I -0.0144 (Persistence_Z -1.50). Both near null.
> - Case D (transient wave, divergence case, rho 0.10): Psi_meanI_state 0.8333 (MeanI_Z 833.69) - high; Psi_persistence_I 0.0 (P_std 0.0, Persistence_Z 0.0) - degenerate. The two candidates produce the designed divergence: per-tick spatial organization is present and strong, while the time-averaged persistence map is spatially uniform (the band visits every column as it advances, so no cell is persistently clustered) and reads zero.
> - Case E (uniform high persistence, degeneracy control, rho 0.70): Psi_meanI_state 0.0007 (MeanI_Z 1.17), Psi_persistence_I 0.0 (P_std 0.0, Persistence_Z 0.0). Both near null, with P_std = 0.0 flagging the uniformity degeneracy. Cleanly separated from Case D on MeanI_Z (~1.17 vs ~833.69): the uniform-persistence misreading is caught, not mistaken for coherence.

**Control outcomes:**
- Positive control (Case A): produces - both observables high-positive (z 914.45 / 91.29) against this grid's null.
- Negative controls (Cases B, C, E): all produce near-null on both observables. B and C are the random scrambles (rho-matched and high-rho); E is the degeneracy check, with P_std = 0.0 separating uniform persistence from true signal. The negatives distinguish "no coherence" from a measurement artifact.

**Steady-state eligibility outcome (if applicable):**
> Not applicable - synthetic battery. No steady-state window is earned by construction; that is C3-SS-001's gate, not this one.

**Interpretation (L4 - Mike / Layer 1 only):**
> Withheld. This test is machinery validation, not interpretation. It establishes that the observable apparatus computes the intended state-based, density-adjusted quantities and discriminates correctly on synthetic controls at this topology. It establishes nothing about real-substrate values, steady-state eligibility, or Regime-II-as-structural, and it does not settle which observable IS Regime-II coherence.

**Divergence note (co-equal pair):**
> Case D is the expected-divergence case and it produced the divergence: Psi_meanI_state 0.8333 (high) vs Psi_persistence_I 0.0 (degenerate). Recorded as data on the co-equal pair - per-tick organization that does not persist as fixed-location clustering. NOT collapsed to one reading and NOT a tiebreaker on the ontological question (which observable, if either, IS Regime-II coherence - L4, Mike / Layer 1, on relational-mutual-reinforcement grounds).

**Follow-up decision:**
> L2 pass. The apparatus is validated at 50x50 toroidal Moore-1, which unlocks real-substrate measurement at this topology - but only after C3-SS-001 (steady-state eligibility) clears, the last precondition before any real-substrate value can be read as Regime II. Registry row advanced to valid-L2 (committed at 1c35283). Transition rules and probe-design inputs remain held, uncommitted.

**Registry status at close:** valid-L2
