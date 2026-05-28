# Layer 3 - C3-SS-001 deliverables follow-up

Layer 3, thank you for the CSV interpretation. Two things before the deliverables list.

## Provenance acknowledged; framing needs adjustment

Layer 1 understands the CSV was an actual run output Mike pasted to you for interpretation, not Layer 3 narrating execution. That is role 3 (Layer 3 output interpretation) in the five-role taxonomy, and it is the correct channel for this work.

The issue is the L2-clearance framing. The response declared the apparatus "passed" L2 and that the gates are "ready." L2 clearance is a Layer 1 judgment at implementation review - after sufficiency-testing the actual CSV against a predicted output that Layer 1 has separately - not a Layer 3 declaration. The substantive finding is welcome and correct; the role-appropriate framing for it is something like:

> "The pasted CSV matches the predicted discrimination patterns at every (case, window) row. The apparatus produces the designed discrimination on the actual run, subject to Layer 1 implementation review and Layer 2 substantive review."

Candidates **produce** or **fail to produce**. The apparatus produced the designed discrimination on the synthetic battery. That is the substantive finding, framed for the role.

L2 clearance and registry advancement happen at Layer 1's node, after the implementation review, not in Layer 3's voice.

## Deliverables status

The contract specified four. Current state:

**1. The script `cycle3/c3_ss_001_battery.py`.** Not yet routed back. Please provide the full file content. Layer 1 needs to read the implementation directly before the implementation review can proceed. The CSV is run-of-record only if the script Layer 1 reviews is the script that produced it - please confirm the file content you provide matches what Mike ran.

**2. Proposed Pre-execution-block content for `cycle3/TEST_RECORD_C3-SS-001.md`.** Not provided. The existing test record (placed on disk; Layer 1 drafted it from the contract at design-phase open) carries the design intent through "Expected output / pass criterion," with the Layer-3-settled parameters marked "to be set by Layer 3's draft per the design contract." Your draft populates those design-side fields:

- **Script name and version:** path is `cycle3/c3_ss_001_battery.py`; provide your version tag or short SHA reference.
- **Inputs and parameters:** explicit values for trajectory length, window length, sliding step, seed; the four threshold values; specific trajectory-shape parameters per case (slope magnitude for Case 2, wobble amplitude for Case 3, step magnitude for Case 6, plateau levels for Case 6 pre-step and post-step).
- **Expected data produced:** confirm the CSV columns produced match the contract's required schema; note any added diagnostic columns.

Layer 1 writes the final test record; your draft populates the design-side fields.

**3. Design rationale for the open parameters.** Partial. The CSV interpretation named two threshold values (0.10 for `relative_drift`, 0.05 for lifted activation) but did not state the `rho_cv` or `rho_range_over_mean` thresholds, and did not provide reasoning for any of the four. Layer 2 needs this rationale to review the design on validity grounds. Specifically:

- **Mathematical definitions** of `relative_drift`, `rho_cv`, `rho_range_over_mean` exactly as implemented in the script (do not just restate the contract's suggested forms - state what the code computes).
- **All four threshold values** named explicitly (drift, cv, range_over_mean, lifted) and the reasoning for each. Why these specific values? How were they chosen to exercise the filters at - but clearly beyond - the boundary between admissible and inadmissible windows? What discriminating margin does each threshold leave between Case 1's filter readings and the thresholds, and between the failing cases' filter readings and the thresholds?
- **Trajectory length, window length, sliding step** with reasoning. The contract suggested 200 / 100 / 25 - did you adopt those values, refine them, or replace them, and why?
- **Trajectory-shape parameters per case** - the specific values (slope, amplitude, plateau levels, step magnitude) and how they were chosen so the discrimination is robust without being artificially easy.

**4. Expected per-case discrimination output.** Substantively provided in the CSV interpretation - but framed as confirmation rather than prediction. Please restate it as the prediction Layer 1 will sufficiency-test against, in the form of a structured table (one row per (case, window_start)) with the expected filter values and the expected candidate flags. The values can be those you read from the actual CSV; the framing is what changes - this is the prediction Layer 1 compares the canonical run to at review.

## Routing

Return all four deliverables to Mike. Layer 1 reviews the implementation (sufficiency-tested against the prediction at deliverable 4, not asserted), Layer 2 reviews the design on validity grounds, then the test record's Pre-execution block can be finalized and the registry's script column can advance from `c3_ss_001_battery.py (Layer 3 draft pending)` to `c3_ss_001_battery.py`.

A note on what comes next, for orientation: if all three reviews clear and Mike's canonical run on the captured C3-ENV-001 environment matches the prediction row-by-row, the test record's Post-execution block fills, the registry advances to `valid-L2`, and SS-001 joins ENV-001 and CTL-001 as a cleared precondition. At that point the three Cycle 3 precondition gates are cleared and the substantive probe phase can open - which draws on the held probe-design inputs at `cycle3/PROBE_DESIGN_INPUTS_HELD.md` (off the shelf only when that phase opens; not before).
