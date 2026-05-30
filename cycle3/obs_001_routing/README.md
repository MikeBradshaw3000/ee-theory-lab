# OBS-001 routing archive

Multi-layer routing artifacts from the C3-OBS-001 wave-one (Rules A + B) design, code, run, and interpretation cycle, all conducted 2026-05-28. The wave-one synthesis cluster (test record, registry advance to valid-L2, held-inputs Section 7 amendment) was committed in commits `dd06f38` and `71e51b9`; the anchor was refreshed at `c31918b`. This routing archive is the remaining synthesis piece, built from the verbatim 2026-05-28 scrollback.

This folder preserves the full substantive content of each layer's contribution across the wave-one cycle: the scope consultation, the design-menu round (v1 -> six Layer-1 corrections -> v2 -> Layer-2 accept-with-edits), the code-production round (v1 -> four Layer-1 corrections -> v2, the version that ran), and the interpretation round (Layer-3 apparatus-level interpretation -> Layer-1 sufficiency-test -> Layer-2 accept-with-required-amendments). The test record at `cycle3/TEST_RECORD_C3-OBS-001.md` synthesizes the findings into the canonical record; this folder is for any future need to trace specific design choices, threshold values, code, or review reasoning back to source.

The artifact bodies are transcribed verbatim from the 2026-05-28 session, with encoding normalized to pure ASCII (em-dashes rendered as hyphens, Greek letter names spelled out, smart quotes rendered straight). Superseded vocabulary or phrasing inside a body is preserved as written; the archive is a historical record of what each layer said at the time, not a re-statement under current discipline. Where a body could not be recovered verbatim, the gap is flagged rather than reconstructed (see the note on item 10 below).

## Contents (chronological)

1. **`OBS001_01_LAYER2_SCOPE_CONSULTATION.md`** - Layer 1 -> Layer 2 pre-drafting consultation on the scope fork for the first design-menu contract: one rule, two rules, or all three. Carries the transition-rule menu (A both-agree baseline, B range-bound, C micro contagion) and the two standing Layer-1 corrections (Rule A pre-loads neither; Rule C does not import mu(rho)). Layer 1's lean toward two (A + one of B/C) exposed for framing-asymmetry containment.

2. **`OBS001_02_LAYER2_SCOPE_RESPONSE.md`** - Layer 2's recommendation: two rules, A + B, with C held for wave two. Grounds: A as non-divergent sanity baseline, B as the deliberate divergence probe, C's tunability more useful after the baseline contrast is understood. Includes the eight-point deliverables structure Layer 2 proposed for the Layer 3 contract.

3. **`OBS001_03_LAYER3_DESIGN_CONTRACT.md`** - Layer 1 -> Layer 3 design-menu contract scoped to A + B. Asks for a design menu (eight deliverables, 5.1-5.8), not code. Carries both Layer-1 corrections forward, the locked topology, the co-equal-pair guard, the four-level distinction, and the framing discipline anticipating the Layer-3-declares-L2-clearance failure mode.

4. **`OBS001_04_LAYER3_DESIGN_V1.md`** - Layer 3's v1 design menu. Specifies Rules A and B at the local-rule level, the Lambda-like parameters, telemetry, a minimal sweep (initially tau_A in {1,2,3,4,8}), expected joint-signature outcomes, gate attachment, and the co-equal-pair guard.

5. **`OBS001_05_LAYER1_DESIGN_REVIEW.md`** - Layer 1 implementation review of v1 with six corrections required: tau_A range internal inconsistency; the primary-source-vs-substrate seam on Rule A's dynamics endpoints (three reconciliation paths offered); per-Lambda expected outcomes missing; Regime-II-candidate regime not identified; no Rule A failure criterion; and Section 5.7 L3 wording ambiguous on flag independence.

6. **`OBS001_06_LAYER3_DESIGN_V2.md`** - Layer 3's v2 design menu addressing all six corrections. Adopts path (iii) for the Rule A seam (full integer sweep tau_A in {1..8}, substrate adjudicates), gives per-Lambda expectations for all 8 tau_A values and 4 bands, names Band [2,4] as the Regime-II-candidate regime to be tested for, adds the Rule A failure criterion, and clarifies flag independence at L3.

7. **`OBS001_07_LAYER2_DESIGN_REVIEW_REQUEST.md`** - Layer 1 -> Layer 2 substantive review request, self-contained: carries the contract, the v2 menu verbatim, the v1->v2 correction summary, and two items surfaced for Layer 2's attention (the substrate-amended Rule A endpoint pairing; the missing explicit degeneracy diagnostic for low/low signatures).

8. **`OBS001_08_LAYER2_DESIGN_VERDICT.md`** - Layer 2 accept-with-edits verdict. Two required edits (explicit low/low degeneracy diagnostic; expanded Rule A meaningful-failure criterion to include the lifted non-degenerate low/low signature), the Rule A endpoint amendment as a close-out record correction, and the anti-binary 3/5-4/5 interpretive discipline. No v3 design round needed; edits fold into the code-production contract.

9. **`OBS001_09_LAYER3_CODE_CONTRACT.md`** - Layer 1 -> Layer 3 code-production contract. Folds in Layer 2's six edits (including the full `LowLow_Nondegenerate_Candidate` flag definition and the never-`Regime_II` naming discipline), specifies the modified delivery flow (Layer 1 packages and delivers, not Layer 3), the canonical filename and destination, pre-flight verification, determinism, sweep structure, apparatus-consumption options, and the consolidated telemetry schema.

10. **`OBS001_10_LAYER3_CODE_V1.md`** - VERBATIM GAP FLAGGED. Layer 3's v1 code was attached to the 2026-05-28 session as a file (not pasted inline) and is not recoverable verbatim from the transcript or from conversation search. Per the recovery discipline, the body is flagged as not recoverable rather than reconstructed. The file carries a derived record of the four ways v1 differed from v2 (drawn from the verbatim Layer 1 code review at item 11), and notes how the v1 body could be recovered if the original attachment is located.

11. **`OBS001_11_LAYER1_CODE_REVIEW.md`** - Layer 1 implementation review of the code with four corrections required: non-deterministic parity check (seed it); docstring claim-language softening ("proving"/"Validates" -> "tests"/"Tests"); unused/undocumented mesa import in pre-flight; and parity check not covering the two null functions. The substrate logic, sweep structure, telemetry, and degeneracy diagnostics are confirmed correct and preserved.

12. **`OBS001_12_LAYER3_CODE_V2.md`** - Layer 3's v2 code, the version that ran. The full Python script as it was placed at `cycle3/c3_obs_001_battery.py` (15,851 bytes at the canonical path) and executed in the C3-ENV-001 environment, producing the 60 NPZs and the 300-row CSV. Preserved here in a fenced code block for archival self-containment; the canonical run-of-record is the file at the canonical path.

13. **`OBS001_13_LAYER3_INTERPRETATION_REQUEST.md`** - Layer 1 -> Layer 3 interpretation request after the run completed. Carries the run-time state, the verbatim 300-row CSV, and the five-part interpretation ask (per-Lambda summary, comparison against v2 expectations, 3/5-4/5 patterns, Rule A substrate dynamics, full-sweep flag distribution), with the apparatus-level-only framing and the L4 boundary held.

14. **`OBS001_14_LAYER3_INTERPRETATION.md`** - Layer 3's apparatus-level interpretation. Rule A non-discriminating (saturation at tau_A {1,2,3}, extinction at {4,5,6,7,8}, no locked clusters); Rule B earned-window divergent signatures; `LowLow_Nondegenerate_Candidate` False on all 300 rows. No L4 reading produced.

15. **`OBS001_15_LAYER2_INTERPRETATION_REVIEW_REQUEST.md`** - Layer 1 -> Layer 2 substantive review request, self-contained: the design expectations, the verbatim CSV, Layer 3's interpretation verbatim, the Layer 1 sufficiency-test result, and four items surfaced for Layer 2 (anti-clustered persistence and the quadrant framework; locked clusters not produced; `LowLow_Nondegenerate_Candidate` False everywhere; the divergent signature across three of four Sweep B bands).

16. **`OBS001_16_LAYER2_INTERPRETATION_VERDICT.md`** - Layer 2 accept-with-required-amendments verdict. Five amendments to canonical synthesis: correct the Rule B [1,2] reading (boundary / near-steady, not earned on 5/5); amend the held-inputs framework to a signed three-level structure distinguishing near-null from negative/anti-clustered persistence; record the Rule A endpoint correction; record `LowLow_Nondegenerate_Candidate` False on all rows; preserve the L4 boundary. No code rerun, no gate reopening, no L4 interpretation.

## What is NOT archived here

- The canonical script `cycle3/c3_obs_001_battery.py` and the canonical outputs (`cycle3/data_out/c3_obs_001_results.csv`, the 60 NPZs at `cycle3/data_out/c3_obs_001_states_*.npz`) live at their canonical paths. The v2 code is embedded inside item 12 and the CSV inside items 13 and 15 for self-contained reading; the run-of-record is at the canonical paths.

- Layer 3's v1 code body. It was attached as a file rather than pasted inline in the 2026-05-28 session and is not recoverable verbatim. Item 10 documents the gap and the four-item v1->v2 difference record rather than reconstructing the body.

## Vocabulary

These files were drafted under the binding vocabulary discipline current at 2026-05-28: rho = activation density; Psi_meanI_state and Psi_persistence_I = the two co-equal observables, with neither named theoretical Psi; Lambda = structural conduciveness; agents act (no decision / optimization / utility / cognitive language); `LowLow_Nondegenerate_Candidate` as the apparatus-level flag, never `Regime_II`; candidates produce or fail to produce, never confirm or demonstrate; "earned steady-state window" as the SS-001-validated criterion. Pure ASCII is used throughout (Greek letter names spelled out, em-dashes rendered as hyphens). The two SS-001 flags `Steady_State_Candidate` and `Lifted_Activation_Candidate` remain independent at every stage.
