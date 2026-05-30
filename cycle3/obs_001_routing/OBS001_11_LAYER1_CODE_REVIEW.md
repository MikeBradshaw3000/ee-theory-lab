# Layer 1 implementation review of wave-one code - corrections required

From: Layer 1, 2026-05-28.
To: Layer 3.
Purpose: implementation review of the wave-one (A+B) code. Four corrections required before packaging. Per the modified delivery flow, the corrected code returns to Layer 1 for a quick re-review against this same list; if clean, Layer 1 packages and delivers to Mike.

The code is substantively correct. The corrections are refinements; the substrate logic, sweep structure, telemetry schema, and degeneracy diagnostics are all correctly implemented and do not need to be revisited.

---

## What works (preserved; do not revise)

- **Substrate logic.** Rule A (neighbor count >= tau_A; no upper bound) and Rule B (closed interval [tau_B,min, tau_B,max]) are correctly implemented over toroidal Moore-radius-1 via np.roll. Initial condition seeds exactly 250 active cells uniformly random per the contract.
- **Sweep structure.** Sweep A (8 tau_A values x 5 seeds) and Sweep B (4 bands x 5 seeds); 60 runs total; 5 candidate windows per run at start in {0, 25, 50, 75, 100}. Matches contract Section 5.4.
- **Determinism.** np.random.seed and random.seed set inside the per-run loop. Substrate dynamics consume no random state. Reruns at identical (rule, lambda_id, seed) will produce byte-identical outputs.
- **Telemetry schema.** All 20 contract Section 6 columns present. Per-tick state matrices written as compressed NPZ at the canonical path with the canonical filename pattern. VAR_EPSILON = 1e-3 justified with grid-arithmetic reasoning. LOW_Z_THRESH = 2.0 grounded in the CTL-001 null distribution.
- **Degeneracy diagnostics (Edit 1.a-e).** All five present and correctly computed. The `LowLow_Nondegenerate_Candidate` conjunction matches Layer 2's specification.
- **Naming discipline.** No `Regime_II` anywhere - flag name, column name, comment, or docstring. Apparatus-level naming preserved throughout.
- **Vocabulary discipline.** No "demonstrates," "confirms" in substantive prose. `rho`, `Psi_meanI_state`, `Psi_persistence_I`, `Lambda` used correctly. The expected-outcome language in the top docstring is correctly framed as "expected to produce" / "expected to be tested for."
- **Co-equal-pair guard.** Neither observable favored or named theoretical Psi.
- **Pre-flight verification.** venv-active check, Python 3.14.x check, numpy 2.4.4 pin check, cycle3 reachability check. Fail-fast structure correct.
- **Approach (c) justification.** Top docstring justifies the reimplementation-with-parity-check choice. NPZ format justified with substrate-shape reasoning.

**Layer 1 verified against primary source.** The parity check's function-name and signature assumptions match c3_ctl_001_battery.py and c3_ss_001_battery.py at primary source. Null computations (`compute_persistence_null`, `compute_meanI_state_null`) are algorithmically byte-identical between wave-one and CTL-001 by line-by-line comparison. The reimplemented `evaluate_window_ss` returns a tuple whose indexed values match SS-001's dict values on the three load-bearing keys.

---

## Corrections required (four items)

### Issue 1 - parity check is non-deterministic

`test_grids = np.random.randint(0, 2, size=(100, 50, 50))` uses unseeded global state. The parity test inputs vary across pre-flight invocations. If parity ever fails intermittently - a real possibility if either apparatus script is ever updated - there is no reproducible failure case to debug from.

**Action.** Seed the parity check with a constant at its top. Suggested: `PARITY_SEED = 7` (a constant outside the substrate-run seed set {42, 137, 256, 1024, 31415} so there is no observability collision between the parity test and the substrate runs). Layer 3 may choose a different constant outside the substrate-run seed set.

### Issue 2 - docstring claim-language softening

The top docstring uses "*proving* byte-for-byte mathematical equivalence"; `run_parity_check`'s docstring uses "*Validates* local reimplementations."

These are claim-stronger than the framing discipline allows. The parity check *tests* whether the reimplementations produce identical values on a deterministic test input; it does not *prove* mathematical equivalence in the formal sense, and it does not *validate* the reimplementations - the apparatus battery's own validity stands on its own gate clearance (CTL-001 valid-L2, SS-001 valid-L2). Framing discipline applies in docstrings as much as in user-facing prose.

**Action.** Replace "proving" with "tests"; replace "Validates" with "Tests." Any adjacent claim-language ("guarantees byte-for-byte," etc.) similarly softened.

### Issue 3 - `mesa` import in pre-flight but unused in the script

The substrate is implemented in plain numpy via np.roll, not Mesa. The script imports Mesa in pre-flight and aborts if Mesa fails to import, despite not actually using Mesa anywhere in the substrate logic.

Two acceptable resolutions; Layer 3 chooses:

(a) Drop the Mesa import from pre-flight. The wave-one script does not need it.

(b) Document explicitly why the Mesa import is defensively required, in a comment near the import. Acceptable rationale: C3-ENV-001 names Mesa 3.5.1 as a pinned dependency; if it fails to import, the environment itself is compromised regardless of whether this specific script uses it.

Either is fine. If (b), the comment must state the rationale; an unexplained "defensive" import is not enough.

### Issue 4 - parity check does not cover the null functions

The parity check covers `calculate_morans_i_toroidal_8`, `batch_morans_i_toroidal_8`, and `evaluate_window` from the SS-001 apparatus. It does NOT cover `compute_persistence_null` or `compute_meanI_state_null`, both of which were reimplemented in wave-one and produce z-scores in the wave-one CSV.

Forward-discipline gap: if CTL-001's null functions are ever modified (different permutation count, different RNG convention, different formula), the parity check would not catch the resulting drift in wave-one's z-scores. The wave-one script would silently produce z-scores that no longer match what CTL-001 would compute on the same input.

**Action.** Extend the parity check to cover both null functions. The seed-reset between each pair of calls is the load-bearing detail - both functions consume random state via np.random.permutation / np.random.rand, so identical random state on entry is required for byte-identical z-scores.

Suggested pattern (Layer 3 may refine):

```python
# Persistence null parity
np.random.seed(PARITY_SEED)
test_grid_2d = np.random.randint(0, 2, size=(50, 50))
actual_I_persist = calculate_morans_i_toroidal_8(test_grid_2d)

np.random.seed(PARITY_SEED)
local_z_persist = compute_persistence_null(test_grid_2d, actual_I_persist)
np.random.seed(PARITY_SEED)
ctl_z_persist, _ = ctl.compute_persistence_null(test_grid_2d, actual_I_persist)
assert np.isclose(local_z_persist, ctl_z_persist), \
    "PRE-FLIGHT FAIL: persistence null parity broken."

# meanI_state null parity
np.random.seed(PARITY_SEED)
test_grids_3d = np.random.randint(0, 2, size=(100, 50, 50))
actual_meanI = np.mean(batch_morans_i_toroidal_8(test_grids_3d))

np.random.seed(PARITY_SEED)
local_z_meanI = compute_meanI_state_null(test_grids_3d, actual_meanI)
np.random.seed(PARITY_SEED)
ctl_z_meanI, _ = ctl.compute_meanI_state_null(test_grids_3d, actual_meanI)
assert np.isclose(local_z_meanI, ctl_z_meanI), \
    "PRE-FLIGHT FAIL: meanI_state null parity broken."
```

Note: CTL-001's null functions return tuples (z_score, null_std), unpack the z_score for comparison. Wave-one's local null functions return just z_score.

The requirement is that the parity check fails if and only if wave-one's nulls diverge from CTL-001's nulls on identical inputs. Layer 3 may refine the test-input shapes or test multiple seeds; the seed-reset pattern between paired calls is the binding constraint.

---

## What is NOT changing

To prevent inadvertent rewrite of working code: the substrate logic (Rule A and Rule B implementations) stands. The sweep structure (8 tau_A x 5 seeds for A; 4 bands x 5 seeds for B; 60 runs total) stands. The telemetry schema is correctly implemented per contract Section 6. The degeneracy diagnostics (Edit 1.a-e) are correctly computed. The `LowLow_Nondegenerate_Candidate` flag is correctly named. The output paths and formats are correct. The pre-flight structure (venv, Python 3.14.x, numpy 2.4.4, cycle3 reachability) stands. Approach (c)'s justification stands.

Touch only the four items above.

---

## Routing after corrections

1. Layer 3 returns the corrected code with the four refinements above.
2. Layer 1 quick re-review against this list of four items.
3. If clean: Layer 1 packages the script as a self-contained file via present_files, drafts one-pane PS commands for Move-Item placement, line-count and last-line verification, and execution; then routes to Mike.
4. Mike's canonical run is the result of record. No execution from Layer 3.

Frame remains: the code is what it is. L1/L2 judgments are made at Layer 1 implementation review. Layer 3 does not declare L1 or L2 clearance. Candidates **produce or fail to produce**; never "confirm" or "demonstrate."

---

## Vocabulary (binding)

- `rho` = activation density
- `Psi_meanI_state`, `Psi_persistence_I` - the two co-equal observables; neither named theoretical Psi
- `Lambda` (or `Lambda_A`, `Lambda_B`) = structural conduciveness
- `LowLow_Nondegenerate_Candidate` - apparatus-level flag; never `Regime_II`
- Agents act - no decision / optimization / utility / cognitive language
- "the point(s) at which mu(rho) = 0" - never `rho_c`
- "per-cell active-state values" - never "field" as explanatory mechanism
- Candidates **produce** or **fail to produce** - never "confirm," "demonstrate," "prove," or "validate" (the last two introduced as drift in the v1 docstrings; see Issue 2)
- "earned steady-state window" - the SS-001-validated criterion, apparatus-grounded
- The two SS-001 flags `Steady_State_Candidate` and `Lifted_Activation_Candidate` remain independent
