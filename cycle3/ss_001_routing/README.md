# SS-001 routing archive

Multi-layer routing artifacts from the C3-SS-001 design and review cycle. C3-SS-001 closed at valid-L2 in commit `7285903`; all three Cycle 3 precondition gates (ENV-001, CTL-001, SS-001) now stand cleared.

This folder preserves the full substantive content of each layer's contribution to the apparatus design and review. The test record at `cycle3/TEST_RECORD_C3-SS-001.md` synthesizes the relevant findings into the canonical gate-closure record; this folder is for any future need to trace specific design choices, threshold values, or review reasoning back to source.

## Contents (chronological)

1. **`SS001_01_LAYER3_CONTRACT.md`** - Design / implementation contract from Layer 1 to Layer 3. Specifies the apparatus, the six minimum cases with expected pass/fail patterns, fixed conventions (script path, output CSV path, BOM-less UTF-8), open design parameters Layer 3 was to propose with justification (filter mathematical definitions, threshold values, trajectory/window/step parameters, lifted threshold, trajectory-shape specifics per case), the four required deliverables, and the interpretation boundary.

2. **`SS001_02_LAYER3_FOLLOWUP.md`** - Follow-up to Layer 3 after their initial response declared "L2 passed" in Layer 3's voice and provided only partial deliverables. Required two adjustments: (a) reframe L2-clearance language because L2 clearance is a Layer 1 judgment at implementation review, not a Layer 3 declaration, and (b) provide the four complete deliverables per the contract (script, Pre-execution-block proposal, design rationale, predicted output table for sufficiency-testing).

3. **`SS001_03_LAYER3_DELIVERABLES.md`** - Layer 3's complete four-deliverables response after the follow-up. Contains the full script content, the proposed Pre-execution-block content, the design rationale with all four threshold values and case-shape choices explicitly justified, and the expected per-case discrimination output table that Layer 1 used as the prediction in row-by-row sufficiency-testing.

4. **`SS001_04_LAYER2_REVIEW_REQUEST.md`** - Layer 1's substantive-review routing package to Layer 2 after the canonical run completed and Layer 1's implementation and sufficiency reviews cleared. Contains the script (load-bearing portions embedded), the canonical 30-row CSV, the Layer 1 sufficiency-test verdict (30/30 flag alignment), three flagged concerns (filter coupling in Cases 2 and 3, Case 4 margin tightness, battery-extension question), and four specific questions for Layer 2.

5. **`SS001_05_LAYER2_VERDICT.md`** - Layer 2's substantive review verdict, verbatim. Recommended outcome (a): accept as-is. Filter coupling judged desirable not flaw; Case 4 margins adequate for the canonical seeded run; battery extension noted as optional future enhancement, not required. Layer 2 also flagged three forward items: (a) the window interval convention should be explicit (`[Window_Start, Window_End)` half-open), (b) the two output flags must remain independent (not combined into a single "Regime-II eligible" flag at any downstream stage), (c) no L4 leakage - the gate says nothing about Regime II itself.

## What is NOT archived here

- Layer 3's first response to the contract, which declared "L2 passed" in Layer 3's voice and required the framing-correction follow-up at SS001_02. The framing-correction event is preserved in SS001_02; the original mis-framed response itself is not preserved.
- The canonical script `cycle3/c3_ss_001_battery.py` (lives in its canonical path; the version archived inside SS001_03 differs only on three documentation/UX points and is not the run-of-record).
- The canonical CSV `cycle3/data_out/c3_ss_001_results.csv` (lives in its canonical path; embedded in SS001_04 for self-contained review-package reading).

## Vocabulary

These files were drafted under the binding vocabulary discipline: rho = activation density; Psi = coherence; Lambda = structural conduciveness; agents act; candidates produce or fail to produce; no decision/optimization/utility/cognitive language. Pure ASCII is used throughout (Greek letters and em-dashes from any source pastes are rendered as their ASCII equivalents).
