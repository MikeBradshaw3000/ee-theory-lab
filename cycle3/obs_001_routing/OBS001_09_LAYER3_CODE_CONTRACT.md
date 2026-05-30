# Layer 3 code-production contract - wave-one (A + B)

From: Layer 1, 2026-05-28.
To: Layer 3.
Purpose: code production for wave one of the Cycle 3 substantive probe-design phase, scope A+B (ratified by Mike on Layer 2's recommendation; design menu v2 accept-with-edits by Layer 2). This contract folds Layer 2's six edits in and specifies a modified delivery flow for this cycle.

---

## 1. What this contract asks for, and what it does NOT

**Asks for:** a runnable Python script implementing the wave-one (A + B) sweep against the locked topology, consuming the CTL-001 and SS-001 apparatus, producing the telemetry schema specified at Section 6 below.

**Does NOT ask for:**
- Execution. Mike runs the script. Layer 3 does not run the script.
- Packaging or delivery. This cycle, Layer 1 packages the code for Mike (see Section 3). Layer 3 returns code as content, not as a finished deliverable artifact.
- File-system commands (Move-Item, file paths, PS execution commands). The code itself yes; the placement and execution scaffolding no.
- Any declaration that the code passes L1 or L2. L1/L2 judgments are made at Layer 1 implementation review.

**Frame:** the code is what it is. State what the code computes; do not state what runs would demonstrate. Candidates produce or fail to produce. No "this script demonstrates," "the implementation confirms," or "L2 sufficiency check passed."

---

## 2. State at contract-open

- Three Cycle 3 precondition gates cleared: C3-ENV-001 (passed-L1), C3-CTL-001 (valid-L2), C3-SS-001 (valid-L2).
- Topology locked: 50x50, Moore radius 1 (8-neighbor), toroidal.
- The two coherence observables (Psi_meanI_state, Psi_persistence_I) remain a co-equal pair. Neither is named theoretical Psi. Regime assignment is L4 (Mike / Layer 1).
- The two SS-001 flags (Steady_State_Candidate, Lifted_Activation_Candidate) remain independent at every stage; not conjoined into a single Regime-II-ready flag.
- Design menu v2 from Layer 3 stands as the spec, with the six edits in Section 4 below applied to it. Where this contract and the v2 menu diverge, this contract wins.

---

## 3. Modified delivery flow for this cycle

The validated SS-001 routing pattern was: Layer 1 contract -> Layer 3 implementation -> Mike's canonical run -> Layer 3 interpretation -> Layer 1 review + sufficiency-test -> Layer 2 review -> Layer 1 synthesis.

**This cycle modifies one step.** Mike's reasoning (recorded for the carry-forward): Layer 1 is better positioned than Layer 3 to manage thumb economy at the delivery step (one self-contained file per script, one-pane PS commands, line-count verification, BOM-state discipline, canonical filename and destination).

Modified flow:

1. Layer 1 contract (this document) -> Layer 3.
2. Layer 3 returns code as **content**, formatted for Layer 1 to package.
3. **Layer 1 implementation review of the code, BEFORE packaging.** Pessimistic-on-passing: for each computation, what alternative explanation could produce the same output, and does the code discriminate. Sufficiency-tested-not-asserted: any refactor of the spec must be tested for equivalence, not asserted equivalent.
4. If clean: **Layer 1 packages and delivers via present_files**, with separately drafted one-pane PS commands for execution, line-count and last-line verification, and the canonical filename and destination.
5. If not clean: Layer 1 -> Layer 3 correction note, return to step 2.
6. Mike's canonical run -> outputs.
7. Layer 3 interpretation of pasted outputs (frame: "the run has produced," not "the run demonstrates").
8. Layer 1 review + sufficiency-test (predicted output vs actual).
9. Layer 2 substantive review.
10. Layer 1 synthesis to canonical record; test record post-execution block filled; registry advanced.

Layer 3's responsibility under this modification: return code as content. Do not specify Move-Item commands or PS execution commands. Do not declare L1 or L2 clearance.

---

## 4. The six edits from Layer 2's verdict, folded into this contract

Layer 2's accept-with-edits verdict identified six required or recommended edits. All six are folded in here. Where they refine the v2 menu, this contract overrides the v2 menu.

### Edit 1 - Explicit low/low degeneracy diagnostic (required, telemetry additions)

The v2 menu distinguishes three low/low states (saturation, extinction, lifted-non-degenerate) implicitly via rho(t) and Lifted_Activation_Candidate. Layer 2 required an explicit diagnostic. Add the following per-window quantities to the telemetry schema:

a. **`mean_active_state_variance`** - mean over the window's ticks of the spatial variance of the per-cell active-state matrix. For binary values this equals mean over the window of rho_t x (1 - rho_t); compute it directly from the matrix and verify the equivalence. Record both the continuous value and the underlying numpy variance computation; do not pre-compute through the binary identity, as that would hide a substrate detail (cells with values other than 0/1, in case of any future extension).

b. **`persistence_std`** - spatial standard deviation of the per-cell persistence grid (the time-averaged active-state matrix over the window). Detects uniform-persistence degeneracy.

c. **`extinction_degenerate`** - flag, definition: `mean_rho <= 0.05`. Matches the existing SS-001 lifted threshold (extinction is the complement of lifted by construction).

d. **`saturation_degenerate`** - flag, first-pass definition: `mean_rho >= 0.95` OR `mean_active_state_variance < epsilon`. Report BOTH the thresholded flag AND the underlying continuous values (mean_rho and mean_active_state_variance) so the threshold can be re-calibrated downstream if needed. Layer 3 to propose `epsilon` with justification; suggested starting point `epsilon = 1e-3`.

e. **`LowLow_Nondegenerate_Candidate`** - apparatus-level descriptive flag, NOT to be named `Regime_II` (Layer 2's vocabulary discipline; the L3-vs-L4 seam). Conjunction of:
   - `Lifted_Activation_Candidate` true
   - `extinction_degenerate` false
   - `saturation_degenerate` false
   - Psi_meanI_state z-score below a "low" threshold (Layer 3 to propose; suggested |z| < 2.0 grounded in the CTL-001 grid-local permutation null distribution)
   - Psi_persistence_I z-score below the same "low" threshold
   - active-state variance not degenerate (mean_active_state_variance >= epsilon)

   Naming discipline (binding): the flag is `LowLow_Nondegenerate_Candidate`. Acceptable alternative: `Lifted_LowLow_Nondegenerate`. **Never `Regime_II`** in any flag, column, comment, or docstring - that would collapse apparatus classification into manuscript interpretation, exactly the L3-vs-L4 seam the four-level distinction was built to keep clean.

### Edit 2 - Expanded Rule A meaningful-failure criterion (required, criterion refinement)

The v2 menu's Rule A meaningful-failure criterion covered only divergent signatures (5/5 seeds high/low or low/high). Layer 2 caught the gap: Rule A is also expected to produce no Regime-II-candidate signature at any Lambda value. If Rule A reliably produces the Regime-II-candidate signature, it has failed as the both-agree baseline.

**Replacement criterion:** Rule A fails at the micro-rule level if **any** Lambda value in Sweep A produces, on 5/5 seeds in earned steady-state windows, **either**:
- (a) a divergent joint signature (high meanI / low persistence, or low meanI / high persistence), **OR**
- (b) a `LowLow_Nondegenerate_Candidate` signature (lifted, low/low, non-degenerate).

Either outcome reliably reproduced indicates Rule A is not serving as the non-discriminating baseline the design claims.

The code does not implement the failure criterion as a runtime check; the per-seed outcomes are recorded faithfully so the criterion can be evaluated at the analysis stage.

### Edit 3 - Naming discipline (required)

See Edit 1.e. **`LowLow_Nondegenerate_Candidate`** (or `Lifted_LowLow_Nondegenerate`) at the apparatus level. **Never** `Regime_II` in any code-level identifier or comment.

### Edit 4 - Anti-binary interpretive note (recommended; carry into contract)

5/5 seeds remains the hard meaningful-failure threshold for both rules. **But** 3/5 or 4/5 off-expectation outcomes are design signals requiring review, not noise to ignore. This is an interpretive discipline, not a code requirement.

The code's responsibility: record per-seed outcomes faithfully so 3/5 and 4/5 patterns can be read out at analysis. No code-level threshold beyond the per-seed outcome recording.

### Edit 5 - Sweep B language refinement (required, framing)

The v2 menu said: "Band [2,4]: ...expected to produce unstructured 'boiling' dynamics. Expected outcome: lifted rho with low Psi_meanI_state / low Psi_persistence_I. *This is explicitly the Regime-II-candidate regime.*"

Layer 2 noted that this phrasing risks reading as pre-classification rather than expectation-to-be-tested. In code-level comments and docstrings, frame:

- Band [2,4]: the parameter value under which a Regime-II-candidate signature is **expected to be tested for**; the run tests this expectation. Valid outcomes also include high/high, high meanI / low persistence, freezing, extinction, or no earned windows.
- Band [2,3]: the parameter value under which a divergent signature (high meanI / low persistence) is **expected to be tested for**; the run tests this expectation. Similarly bounded valid outcomes.

The code's responsibility: do not encode the expectation as a pre-classification in any output column. Outcomes are read from the telemetry post-run, not pre-asserted in the script's structure.

### Edit 6 - Rule A endpoint amendment carried into contract framing

The substrate-grounded picture (from path-iii resolution of the v1 review's Issue 2):

- low tau_A (high Lambda_A): expected to produce uniform saturation (rho -> 1.0); low/low (degenerate) by `saturation_degenerate`.
- intermediate tau_A: expected to produce locked clusters (if active mass survives); high/high. Note Layer 2's nuance: tau_A = 5 at starting rho ~ 0.10 may sometimes extinguish rather than cluster - the substrate adjudicates.
- high tau_A (low Lambda_A): expected to produce extinction (rho -> 0); low/low (degenerate) by `extinction_degenerate`.

Expected-outcome language in code comments and docstrings remains "expected to produce...", "expected to be tested for...", never "produces" or "demonstrates." The substrate has not yet been observed running A+B at the locked topology - the substrate-grounded picture is hypothesis.

This contract carries the endpoint amendment as a framing input. A separate close-out-cluster amendment to primary source (the 2026-05-25 corrections file and any anchor compression) is a record-keeping move outside this contract's scope; it follows after wave-one results return.

---

## 5. Code requirements

### 5.1. File and location

- **Canonical filename:** `c3_obs_001_battery.py`
- **Canonical destination:** `cycle3/c3_obs_001_battery.py`

(Layer 1 packages and places. Layer 3 does not specify Move-Item commands.)

### 5.2. Pre-flight verification (required at script start)

The script must verify, before any substantive computation, and fail fast with actionable errors if any check fails:

- `sys.prefix != sys.base_prefix` (venv is active)
- `sys.version_info[:2] == (3, 14)` (Python 3.14.x, matching C3-ENV-001)
- Critical imports succeed: numpy (pinned 2.4.4), pandas, mesa 3.5.1, pyarrow or fastparquet, scipy (if needed for variance)
- The cycle3 directory is reachable and the apparatus scripts exist (see Section 5.5).

### 5.3. Determinism

The script must be deterministic for any (rule, Lambda, seed) triple. Set numpy's seed, Python's random seed, and any other stochastic sources from the seed parameter. Two runs with identical (rule, Lambda, seed) must produce byte-identical per-tick active-state matrices and byte-identical telemetry CSV rows.

### 5.4. Sweep structure

- **Sweep A:** tau_A in {1, 2, 3, 4, 5, 6, 7, 8} (8 values).
- **Sweep B:** Band in {[1,2], [2,3], [3,4], [2,4]} (4 values).
- **Seeds per parameter value:** 5 (specify the seed values explicitly; suggested: {42, 137, 256, 1024, 31415} for traceability across reruns).
- **Ticks per run:** 200.
- **Initial condition:** target starting rho = 0.10; uniformly random per-cell active-state values.
- **Total runs:** 60 (12 parameter sets x 5 seeds).

### 5.5. Apparatus consumption (CTL-001 and SS-001)

The wave-one script consumes the cleared CTL-001 and SS-001 apparatus. The observable computations and diagnostic computations must be **byte-identical** to those scripts' computations on identical inputs.

Layer 3 to choose the implementation approach:

(a) **Direct import from `cycle3.c3_ctl_001_battery` and `cycle3.c3_ss_001_battery`** if the relevant functions are importable as-is.

(b) **Refactor extraction:** if the battery scripts have the math nested inside their main() and are not cleanly importable, propose a refactor that extracts the computations into a shared module (`cycle3/c3_observables.py` and `cycle3/c3_ss_diagnostics.py`, suggested names), and have the wave-one script and the existing batteries both import from the shared module. If refactoring, this is a contract sub-step: propose the refactor explicitly in the returned code so Layer 1 can verify (i) the existing batteries remain byte-identical in their outputs, (ii) the shared modules are tested against the existing batteries' frozen outputs. **Refactoring is not authorized to silently change the existing batteries' behavior.**

(c) **Reimplementation with parity check:** reimplement the computations in the wave-one script and include a parity-check function that runs the existing battery on its known synthetic cases and asserts byte-identical results. The parity check runs as part of pre-flight; the script fails fast if parity is broken.

Layer 3 selects (a), (b), or (c) and justifies the choice in the returned code's top docstring. Layer 1 review will check the justification and verify the chosen approach against primary source.

### 5.6. Per-tick computation per run

For each (rule, Lambda, seed):

1. Initialize the 50x50 toroidal grid at t=0 with uniformly random active-state values; total active cells = round(0.10 x 2500) = 250.
2. For t in 1 to 200:
   - Compute the active-neighbor count for each cell over its 8-neighbor Moore neighborhood (toroidal).
   - Apply the rule (A or B) per-cell to produce the t-th active-state matrix.
   - Record rho(t).
   - Record the full 50x50 matrix.
3. Compute Tick_to_Freeze and Tick_to_Zero per-run from the per-tick records.

### 5.7. Per-window computation per run

For each candidate window (start in {0, 25, 50, 75, 100} for a 100-tick window over a 200-tick run; the sliding-step of 25 produces 5 candidate windows):

- Compute Psi_meanI_state, Psi_persistence_I, their z-scores via CTL-001's grid-local permutation null.
- Compute the four SS-001 diagnostics (relative_drift, rho_cv, rho_range_over_mean, mean_rho).
- Compute the two SS-001 flags (Steady_State_Candidate, Lifted_Activation_Candidate).
- Compute the new degeneracy diagnostics (Edit 1.a-e): mean_active_state_variance, persistence_std, extinction_degenerate, saturation_degenerate, LowLow_Nondegenerate_Candidate.

### 5.8. Output

- **Per-tick active-state matrices:** stored in Parquet or compressed NPZ at `cycle3/data_out/c3_obs_001_states_{rule}_{lambda_id}_{seed}.{parquet|npz}`. (Layer 3 may choose Parquet or NPZ; justify.)
- **Per-run rule-specific diagnostics:** Tick_to_Freeze, Tick_to_Zero, and the run's (rule, Lambda, seed) identifiers, one row per run.
- **Per-window telemetry:** flat CSV at `cycle3/data_out/c3_obs_001_results.csv`, one row per (rule, Lambda, seed, window_start), with columns:
  - rule (string: "A" or "B")
  - lambda_id (string: tau_A value as integer-string for A; band as "[min,max]" string for B)
  - seed
  - window_start
  - rho(t)-summary statistics for the window (or the four SS-001 diagnostics, which substantially carry these)
  - Psi_meanI_state, Psi_meanI_state_z
  - Psi_persistence_I, Psi_persistence_I_z
  - relative_drift, rho_cv, rho_range_over_mean, mean_rho
  - Steady_State_Candidate (bool), Lifted_Activation_Candidate (bool)
  - mean_active_state_variance, persistence_std
  - extinction_degenerate (bool), saturation_degenerate (bool), LowLow_Nondegenerate_Candidate (bool)
  - Tick_to_Freeze, Tick_to_Zero (per-run values, repeated per-window-row for the run for join convenience)

(Per-run-rule-specific-diagnostics may live as a separate small CSV or be joined into the per-window CSV; Layer 3 chooses, justify.)

### 5.9. Vocabulary in code

In comments, docstrings, variable names, and any printed output:

- `rho` (or `rho_t`) for activation density; not `density`, `field`, or `rho_c`.
- `Psi_meanI_state`, `Psi_persistence_I` for the observables; never `Psi` unqualified, never `Regime_II` as an identifier.
- `Lambda` (or `Lambda_A`, `Lambda_B`) for structural conduciveness, where the parameter is referenced architecturally; the per-rule local parameter `tau_A` or `tau_B_min`, `tau_B_max` is fine in implementation contexts.
- No "demonstrates," "confirms," "verifies" in docstrings; "computes," "records," "produces" only.
- No "Regime_II" anywhere as a code identifier or comment label. The apparatus-level flag is `LowLow_Nondegenerate_Candidate`.

---

## 6. Telemetry schema (consolidated)

Per-tick (per-run):
- `rho_t` (scalar)
- `state_matrix` (50x50, stored as Parquet or NPZ)

Per-window (per-run-per-window, 100-tick window, 25-tick step):

| Column | Type | Source |
|---|---|---|
| rule | str ("A" or "B") | dispatch |
| lambda_id | str | dispatch |
| seed | int | dispatch |
| window_start | int | dispatch |
| Psi_meanI_state | float | CTL-001 apparatus |
| Psi_meanI_state_z | float | CTL-001 grid-local null |
| Psi_persistence_I | float | CTL-001 apparatus |
| Psi_persistence_I_z | float | CTL-001 grid-local null |
| relative_drift | float | SS-001 diagnostic |
| rho_cv | float | SS-001 diagnostic |
| rho_range_over_mean | float | SS-001 diagnostic |
| mean_rho | float | SS-001 diagnostic |
| Steady_State_Candidate | bool | SS-001 flag |
| Lifted_Activation_Candidate | bool | SS-001 flag |
| mean_active_state_variance | float | NEW (Edit 1.a) |
| persistence_std | float | NEW (Edit 1.b) |
| extinction_degenerate | bool | NEW (Edit 1.c) |
| saturation_degenerate | bool | NEW (Edit 1.d) |
| LowLow_Nondegenerate_Candidate | bool | NEW (Edit 1.e) |
| Tick_to_Freeze | int (per-run, joined) | per-run diagnostic |
| Tick_to_Zero | int (per-run, joined) | per-run diagnostic |

Conventions:
- Tick_to_Freeze and Tick_to_Zero are -1 if not triggered within the 200-tick run.
- All flags are explicit booleans (True/False) in the CSV, written as "True"/"False" strings.
- mean_rho is the SS-001 window-mean of rho_t (the CTL-001 / SS-001 apparatus's own quantity).

---

## 7. What Layer 1 will check at implementation review (before packaging)

This is for Layer 3's awareness; the review is Layer 1's.

1. Pre-flight verification (Section 5.2) present and correct.
2. Determinism (Section 5.3): code seeds numpy and Python random from a per-run seed; no global mutable state across runs.
3. Apparatus consumption (Section 5.5): chosen approach (a/b/c) implemented and justified in the top docstring. If (b), the refactor is reviewed for byte-identity against the existing batteries. If (c), the parity check passes (Layer 1 will inspect; if needed, Mike runs the parity check before any wave-one run).
4. Local rules (Section 5.6) compute correctly. Specifically:
   - Rule A: neighbor count >= tau_A -> active; else inactive. **No upper bound.** Toroidal 8-neighborhood.
   - Rule B: tau_B_min <= neighbor count <= tau_B_max -> active; else inactive. Toroidal 8-neighborhood.
   - Initial condition: 10% active uniformly random.
5. Per-window computations (Section 5.7) call apparatus functions on the right inputs (the per-tick matrices and rho time series for the right window), not on the wrong slice.
6. Degeneracy diagnostics (Edit 1.a-e) computed and named per Section 5.9 vocabulary.
7. Output schema (Section 6) matches.
8. No "Regime_II" in any identifier, comment, or string.
9. No "demonstrates," "confirms," "verifies" in docstrings; framing discipline preserved.
10. Co-equal-pair guard: neither observable is favored or named theoretical Psi in any code-level commentary.

If any check fails: Layer 1 -> Layer 3 correction note. Same shape as the design-menu correction cycle.

If all checks pass: Layer 1 packages the script as a full-file artifact via present_files, drafts the one-pane PS commands for `Move-Item` placement and execution, and routes to Mike. Mike's run is the result of record.

---

## 8. Routing after Layer 3 returns code

1. **Layer 1 implementation review** (per Section 7). Pessimistic-on-passing.
2. If clean: **Layer 1 packages and delivers.** Full-file artifact via present_files; one-pane PS commands for `Move-Item` placement, then for execution; line-count and last-line verification command after placement.
3. **Mike's canonical run** in the C3-ENV-001 environment.
4. **Layer 3 interpretation** of the pasted outputs (CSV, per-tick artifacts, console log). Frame: "the run has produced...", not "the run demonstrates...". Layer 3 does not declare L2 clearance.
5. **Layer 1 review + sufficiency-test:** predicted outputs (from Section 5 expectations) vs actual outputs. Sufficiency-tested-not-asserted on every per-Lambda expectation: did the run produce what the spec predicted, or did it produce something else.
6. **Layer 2 substantive review** of the outputs and Layer 3's interpretation.
7. **Layer 1 synthesis** to canonical record. Test record (TEST_RECORD_C3-OBS-001.md) post-execution block filled from primary source. Registry C3-OBS-001 row advanced.

---

## 9. Vocabulary (binding)

- `rho` = activation density
- `Psi_meanI_state`, `Psi_persistence_I` - the two co-equal observables; neither is named theoretical Psi
- `Lambda` (or `Lambda_A`, `Lambda_B`) = structural conduciveness
- `LowLow_Nondegenerate_Candidate` - apparatus-level flag; never `Regime_II`
- Agents **act** - no decision / optimization / utility / cognitive language
- "the point(s) at which mu(rho) = 0" - never `rho_c`
- "per-cell active-state values" - never "field" as explanatory mechanism
- Candidates **produce** or **fail to produce** - never "confirm" or "demonstrate"
- "earned steady-state window" - the SS-001-validated criterion, apparatus-grounded
- The two SS-001 flags `Steady_State_Candidate` and `Lifted_Activation_Candidate` remain independent at every stage

Vocabulary discipline holds throughout the returned code, including at any docstring or comment that might naturally read as celebratory or claim-making.
