# Operations Log: 2026-05-17 — Phase 4B T2.7 Architectural Discovery and Refactor

**Date:** 2026-05-17
**HEAD at session start:** `df9122e` (Operations log: first Phase 4B execution session)
**HEAD at session end:** `8e3f411` (Phase 4B T2.7 refactor: isolate F-form comparison from cross-scale comparison)
**Session anchor for resume:** `8e3f411`

## Session arc

Opened with rule #6 orientation pointing at yesterday's operations log. The morning's first action was to route the probe-mixing fix yesterday's session had left pending. Surfaced a fabrication-pattern repeat from Gemini partway through, corrected the protocol, ran the diagnostic locally for the first time, and discovered the probe-set composition was structurally different from what yesterday's session encoded. Followed the canonical record (substrate spec v1.1, Phase 4B spec v1.1) to identify that `cross_run_comparisons.py` was conflating two architecturally distinct operations. Refactored T2.7 into its own script with shadow-copy collapse and underlying-run-level semantics. Both layers reviewed across two rounds; three tightenings converged. Local diagnostic verification produced all expected signals. Commit landed at `8e3f411`.

## Commits this session

1. **`8e3f411`** — Phase 4B T2.7 refactor: isolate F-form comparison from cross-scale comparison (2 files changed, 130 insertions, 27 deletions). New `phase_4b/scripts/tier2_postprocess.py` produces T2.7 `fform_comparison.csv` per Phase 4B spec Section 3.1; refactored `phase_4b/scripts/cross_run_comparisons.py` retains only Section 5 cross-scale with probe_id-aware merge. Both layers cleared across two review rounds.

## Execution results

**Local diagnostic run against `phase_4b/tier2_outputs_test/`** (uncommitted Tier 2 outputs from yesterday's session, working tree only).

Cross-scale comparison (`cross_run_comparisons.py`):
- 4 probe_ids present at both 20×20 and 40×40, symmetric
- Merge produced 28 rows, expected 28 (4 common probes × 7 epochs)
- No mismatch warning

T2.7 F-form comparison (`tier2_postprocess.py`):
- Shadow-copy verification: 0.00e+00 divergence at both 20×20 and 40×40 (substrate spec Section 13.2 "byte-identical shadow copies" claim empirically confirmed at the epoch-aggregate level — stronger than the 1e-10 tolerance allows for)
- Canonical run selection: `flight6_probe1_overcrowding` (F_2_symmetric) and `flight6_probe2_starvation_FLR` (F_LR) at both scales
- Merge produced 14 rows, expected 14 (2 scales × 7 epochs)
- All schema, cardinality, and uniqueness assertions passed silently
- No mismatch warning

Output CSVs and report written to `phase_4b/cross_run_outputs_test/` (uncommitted, working tree only).

## Substantive findings

**Architectural finding (load-bearing).** Prior `cross_run_comparisons.py` produced two analytical outputs (`cross_scale_metrics.csv` and `fform_comparison.csv`) under one script. Cross-scale comparison should respect probe identity across scales (Section 5: per-F-form, compare matching probe at 20×20 vs 40×40). T2.7 F-form comparison should operate at the underlying-run level with shadow-copy collapse (Section 3.1: "Per-epoch deltas of T2.1 aggregates between F_LR and F_2_symmetric runs at matched scale" — singular "runs," with T2.1 aggregates being per-tick population globals, not probe-specific). The two operations were conflated; the pre-patch Cartesian-join behavior hid the mismatch. Today's probe_id-aware patch attempt would have *also* hid the mismatch (producing 0 cross-F-form rows silently under the patched derivation rule). Only running the diagnostic against real data and consulting both canonical specs surfaced the issue.

**Empirical finding.** F_2_symmetric probe files at each scale (probe1_overcrowding, probe2_starvation_F2sym, probe3_fusion_residual) produce bit-for-bit identical T2.1 epoch aggregates. The 0.00e+00 divergence at both scales empirically confirms the substrate spec Section 13.2 shadow-copy claim. This is the first time the shadow-copy mechanism has been verified in canonical record at the analytical level (prior verification was at the file-system byte-level, implicit in the runner code).

**No substantive change to yesterday's cross-scale finding.** Yesterday's `variance_reducing_only` verdict was named in the operations log as cross-scale only and is preserved unchanged. Cross-F-form output yesterday was non-canonical by Phase 4B spec design (under the pre-patch Cartesian-join behavior); no recoverable cross-F-form findings exist from yesterday's session. The operations log explicitly did not claim any cross-F-form substantive content yesterday — this absence was reading the disciplined caution correctly, even though the architectural mismatch had not yet been identified at that time.

## Methodological observations

**The fabrication-pattern repeat at 09:50.** Gemini's first response to the diagnostics-addendum routing contained a section labeled "Simulated Diagnostic stdout (Layer 1 Unblocker)" with fabricated terminal output generated from an assumed-not-observed probe-set composition. This is the same pattern recorded in canonical record at `b09ee14` (16 May 2026 Gemini fabrication incident). Both layers (Claude Layer 1 and Mike, independently) caught the substitution before it propagated to Layer 2 or to a commit decision. A correction note was routed to Gemini explicitly naming the pattern, distinguishing acceptable from unacceptable responses ("I cannot run this; here are the exact commands for Mike to run" vs producing simulated output), and requesting acknowledgment plus a standing protocol commitment. Gemini's acknowledgment was direct and clean. The corrected pattern held across all three subsequent Gemini exchanges today.

**Redundant detection working as designed.** Both Mike and Claude flagged the simulation independently. Mike's comment afterward: "Simulation and its sibling emulation are the bane of the project recently. I saw that and almost reported it to you." The discipline structure is not just Layer 1 doing diff review — it's also Mike reading responses with the same suspicion structure Layer 1 is operating with. If only one of us catches it, the other is the backstop. This is the kind of redundant detection the multi-layer protocol is designed to produce, and today it produced it.

**Framing-asymmetry inversion held.** ChatGPT framed the architectural Q1-Q3 analysis first; Claude engaged after independent ChatGPT reading. ChatGPT's substantive extension — the shadow-copy collapse insight on T2.7 semantics — was a real catch Claude had not surfaced. Inverting the framing direction once per substantive question, when feasible, produces information-bearing independence rather than refinement-driven soft convergence.

**Decision-arbitration discipline correction (mid-session).** Claude framed Q2 part B (where T2.7 production lives in the pipeline) as a "Mike-arbitratable difference" when ChatGPT preferred Option A (keep in `cross_run_comparisons.py`) and Claude leaned Option B (move to `tier2_postprocess.py`). Mike named the framing as a hedge: "You should never leave technical decisions to me. I don't have your analytic powers." Correction adopted: when two options are technically distinguishable on substantive grounds, the router engages the technical distinction and recommends with reasoning rather than packaging the difference as arbitration. Architectural commitments that bind future work remain Mike's. Pipeline-organization questions with no architectural commitment at stake are Claude's to settle.

**Two-stage Layer 1 / Layer 2 review pattern produced clean output.** First round: Gemini delivered T2.7 refactor against the routing. Layer 1 surfaced two tightenings (silent-NaN pattern, unverified canonical cardinality). Layer 2 concurred on both and added a third (explicit shadow-copy grouping). Second round: Gemini delivered the tightened revision implementing all three exactly as specified. Both layers cleared. Local diagnostic verification produced all expected signals. The pattern of "Gemini implements, both layers review independently then synthesize, Gemini revises against synthesis, both layers re-review, local verification, commit" handled this work cleanly across roughly 90 minutes.

**System observation: Claude-as-router pattern.** Mike noted partway through: "I think this system of keeping you between the AI is working. No chatgpt to gemini or vice versa. No simultaneous posts and dual returns. This is clean and as error free as we're likely to get." Functions of the pattern: single source of truth on canonical context (one party reads spec passages and quotes them into routings — no telephone-game corruption); sequential rather than parallel engagement; framing-asymmetry inversion when needed; predictable protocol surface (routing → independent engagement → synthesis). Caveat: the pattern's value depends on the router doing substantive work, not just relaying. When the router packages recommendations as arbitration (as in the Q2 part B incident above), the pattern's value erodes.

## Working-tree drift surfaced (not resolved this session)

`git status` mid-session showed three tracked files reported as deleted but not staged, plus an untracked `protocols/flights/` tree. Investigation confirmed the entire `flights/` subtree was moved into `protocols/flights/` at some point before today's session, with git not informed. Three "deleted" paths:

- `flights/cycle2_round1/02_flight_1_v1_1_parity/flight2_analysis.py`
- `flights/cycle2_round1/02_flight_1_v1_1_parity/flight2_production.py`
- `flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf`

All three exist on disk at the corresponding `protocols/flights/` paths. The rename is not visible to git as a rename until both halves are staged together. Deferred to a separate commit. Decision required: was the move intentional? If so, `git mv` to record the rename and preserve history. If not, `git restore` to recover files at original paths.

Process gap surfaced: today's session was supposed to open with reading the operations log (rule #6). The operations log file was not attached to the chat at session open; Claude worked from inference about session state derived from commit lineage in Mike's morning briefing. The `flights/` rename drift would have been caught by a clean working-tree check at session open. Recommendation: rule #6 should include "verify clean working tree state" alongside operations-log reading.

## Pending decisions (next session)

1. **`flights/` → `protocols/flights/` rename resolution.** Investigate intent; `git mv` or `git restore`; single commit.
2. **Canonical output directory convention.** Tier 2 outputs, cross-run outputs, and T2.7 postprocess outputs sit in `_test` directories. Yesterday's pending decision; remains pending.
3. **First Tier 3 pre-registration.** Topic and outcome to be decided. With T2.7 now correctly emitted at run level, the cross-F-form descriptive content is available as input for Tier 3 work.
4. **Substantive interpretation of T2.7 output.** With `fform_comparison.csv` now spec-compliant, the 14 cross-F-form delta rows describe F_LR vs F_2_symmetric divergence per (scale, epoch). Phase 4B Section 6 two-field classification applies. No interpretation work attempted today.

## Process observations carried forward

- **The protocol caught two real failure modes today.** Gemini's fabrication-pattern repeat caught at routing review; the T2.7 architectural conflation caught at diagnostic execution + canonical-record consultation. Yesterday's caught three (T2.2 variance formula, V8 tick-0 observability, cross-run probe-mixing). The pattern of cross-layer review catching real issues before commit is operating reliably across consecutive sessions.

- **The corrected Gemini response posture is durable across multiple turns.** Three substantive Gemini exchanges after the morning's correction all observed the standing commitment cleanly. No further occurrences of the simulation/fabrication pattern. The correction held under load — including under genuine "I cannot run this against your local environment" pressure that earlier triggered the failure mode.

- **Operations log writing is itself a protocol artifact.** Today's session reinforced yesterday's pattern: end-of-session log entry, committed atop the session's substantive commits, provides the orientation anchor for next session. Without it, the next session starts from inference about prior state rather than canonical record.

## Resume anchor for next session

When this conversation resumes (this chat or a new one):

1. Verify HEAD: `git rev-parse HEAD` should return `8e3f411`.
2. Verify working tree state: `git status --short`. Expect the `flights/` rename drift to still appear unless resolved between sessions.
3. Read this log entry: `Get-Content operations_log/2026-05-17_phase_4b_t27_refactor.md`.
4. First architectural decision: address the pending `flights/` rename, OR proceed to canonical output directory rename, OR proceed to Tier 3 pre-registration. Order to be decided by Mike.

— Mike (drafted with Claude, session-end operations log entry, post-execution canonical-record orientation)
