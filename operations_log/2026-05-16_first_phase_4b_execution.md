# Operations Log: 2026-05-16 — First Phase 4B Execution Session

**Date:** 2026-05-16
**HEAD at session start:** `0c1a98f` (rule #6 refinement)
**HEAD at session end:** `99782b9` (Tier 1 V8 tick-0 patch + Tier 2 regime caveat)
**Session anchor for resume:** `99782b9`

## Session arc

Started with Gemini's revised cycle 5+6 distribution builder following the prior session's fabrication incident and rule #6 refinement. Ended with all eight Flight 2 parquet files Tier 1 verified, all eight Tier 2 output sets generated, and cross-run comparisons produced with one known issue routed for next session.

## Commits this session

In chronological order:

1. **`89b85f4`** — Phase 4B cycle 5+6 implementation pipeline (5 files, 569 insertions). Five scripts: `_phase_4b_common.py`, `tier1_verify.py`, `tier2_analyze.py`, `tier3_regression.py`, `cross_run_comparisons.py`. Both layers (Claude Layer 1, ChatGPT Layer 2) cleared after several revision cycles addressing Tier 2 completeness, column-name corrections, and tick-0 ds computation from is_active.

2. **`6f61fbe`** — Phase 4B Tier 2 patch: T2.2 epoch_summary variance correction; ddof=0 caveat in terminal output (1 file changed, 21 insertions, 16 deletions). Layer 2 ChatGPT substantively reviewed the committed pipeline and identified that T2.2 was computing the epoch-level mean of already-aggregated per-tick standard deviations rather than the standard deviation of tick-level means across the epoch. Cross-scale `variance_reducing_only` verdict depends on the corrected statistic. Layer 1 (Claude) independently caught the same issue while drafting the ChatGPT routing. Both layers converged on a single targeted Tier 2 patch.

3. **`99782b9`** — Phase 4B Tier 1 V8 patch: skip tick-0 Psi reconstruction (substrate uses unpersisted pre-step state); add Tier 2 regime caveat (2 files changed, 21 insertions, 3 deletions). First Tier 1 execution returned FAIL with 187 V8 mismatches. Three-stage diagnostic chain plus substrate generator code inspection (at `C:\Users\vkz244\EE_Theory_Lab\Flight_6\flight6_phase4A_runner.py`) localized the finding: substrate computes tick-0 Psi from `state_history` deque storing initial pre-step activation state, which is consumed by deque rotation and not persisted to parquet. The verifier's "tick 0 Psi must be 0" assumption was wrong. Verifier needed to skip tick 0 reconstruction; substrate is correct. Both layers cleared the patch.

## Execution results

**Tier 1 verification:** all eight Flight 2 parquet files PASS after V8 patch.

| File | Scale | F-form | Result |
|---|---|---|---|
| flight6_probe1_overcrowding_20x20 | 20x20 | F_2_symmetric | PASS |
| flight6_probe1_overcrowding_40x40 | 40x40 | F_2_symmetric | PASS |
| flight6_probe2_starvation_F2sym_20x20 | 20x20 | F_2_symmetric | PASS |
| flight6_probe2_starvation_F2sym_40x40 | 40x40 | F_2_symmetric | PASS |
| flight6_probe2_starvation_FLR_20x20 | 20x20 | F_LR | PASS |
| flight6_probe2_starvation_FLR_40x40 | 40x40 | F_LR | PASS |
| flight6_probe3_fusion_residual_20x20 | 20x20 | F_2_symmetric | PASS |
| flight6_probe3_fusion_residual_40x40 | 40x40 | F_2_symmetric | PASS |

Approximately 14 million rows of telemetry verified against V1-V8 invariants. Reports at `phase_4b/tier1_reports/` (local only, not committed). Substrate v1.1 is mathematically clean.

**Tier 2 analysis:** all eight files processed. 64 output CSVs generated at `phase_4b/tier2_outputs_test/` (local only). T2.1-T2.8 plus Q-effect extension. Test directory naming pending decision on canonical output convention.

**Cross-run comparisons:** ran clean. Three files at `phase_4b/cross_run_outputs_test/`: `cross_scale_metrics.csv`, `fform_comparison.csv`, `cross_scale_report.md`.

## Substantive preliminary findings

These are preliminary pending the cross-run probe-mixing fix (see next section). Even after that fix, the dominant pattern below should hold.

**Variance-reducing-only verdict dominates.** All cross-scale comparisons (F_LR and F_2_symmetric, all seven epochs) return `variance_reducing_only` verdict: mean ρ stability within ±5% across scales, ρ standard deviation reduction below 0.95 ratio (40x40 vs 20x20). The signature is consistent with finite-size scaling — temporal fluctuations decrease with system size while mean trajectory is preserved.

**Epoch 0 shows weaker scale reduction.** F_LR epoch 0 std ratio = 0.797 (modest reduction); F_2_symmetric epoch 0 std ratio = 0.946 (very small reduction). Later epochs (1-6) drop to 0.48-0.55 range for both F-forms. The initialization-driven variance shows less scale-dependence than the steady-state dynamics that emerge after epoch 0. This is consistent with the tick-0 observability caveat: initialization variance reflects the deque-init pattern, while steady-state variance reflects intrinsic dynamics.

**F_LR vs F_2_symmetric ρ levels diverge substantively.** F_LR runs steady-state ρ around 0.22-0.30; F_2_symmetric runs steady-state ρ around 0.066-0.085. F_LR maintains 3-4x higher activation density than F_2_symmetric at the same parameters.

These findings should not yet be cited authoritatively — the probe-mixing in cross-run merges affects rep counts but not individual verdict assignments. After the fix, individual probe-by-probe cross-scale comparisons will produce the clean dataset for substantive interpretation.

## Pending Layer 1 finding (next session)

**Probe-mixing in cross_run_comparisons.py merges.**

The cross-scale merge joins on `['f_variant', 'epoch']` only:

```python
scale_merged = pd.merge(df_20, df_40, on=['f_variant', 'epoch'], suffixes=('_20', '_40'))
```

When multiple probes share an `f_variant` (three F_2_symmetric probes: overcrowding, starvation_F2sym, fusion_residual), the merge produces a cartesian join across probes within that f_variant. F_2_symmetric outputs show 9 rows per (epoch, f_variant) combination (3 probes × 3 probes) instead of 3.

The cross-F-form merge has the analogous issue on `['scale', 'epoch']`:

```python
ff_merged = pd.merge(df_f2, df_flr, on=['scale', 'epoch'], suffixes=('_f2', '_flr'))
```

Fix: introduce a `probe_id` column derived by stripping the scale suffix from `run_id`. Then:

- Cross-scale merge on `['probe_id', 'f_variant', 'epoch']`
- Cross-F-form merge on `['probe_id', 'scale', 'epoch']`

The `probe_id` should preserve probe identity across scales: `flight6_probe1_overcrowding_20x20` → `flight6_probe1_overcrowding`, same probe_id for the 40x40 variant.

This routes to Gemini for a small `cross_run_comparisons.py` patch with both Layer 1 and Layer 2 review of the diff.

## Pending decisions (next session)

1. **Probe-mixing fix** — Layer 1 → cross-layer review → patch → both layers re-review → commit on top of `99782b9` → re-run cross-run script.
2. **Canonical output directory convention.** Tier 2 outputs and cross-run outputs currently sit in `_test` directories. Either rename them to canonical paths or commit to the test convention. Probably canonical names (`phase_4b/tier2_outputs/` and `phase_4b/cross_run_outputs/`) once probe-mixing fix is in.
3. **Tier 3 pre-registration.** Once cross-run is clean, the next layer is regression. First pre-registration YAML goes at `phase_4b/pre_registrations/`. Topic and outcome to be decided.

## Process observations

**The protocol worked end-to-end.** First Tier 1 execution surfaced a real verifier-substrate observability gap. The diagnostic chain (split V8 sub-checks → pattern analysis → formula testing → substrate code inspection) followed rule #6 discipline: canonical record first, then code inspection, then cross-layer review before patching. Mike's "I don't remember" response at the right moment prevented unilateral guessing.

**Three substantive findings caught by cross-layer review this session:**

1. T2.2 variance formula (Layer 2 ChatGPT independent catch)
2. V8 tick-0 observability (Layer 1 Claude diagnostic chain)
3. Cross-run probe-mixing (Layer 1 Claude at output inspection)

Each was a real issue caught before it contaminated downstream analysis. Each was patched (or routed for next-session patching) under both-layer clearance.

**Chat-rendering ghost.** Gemini iterated twice on a Tier 3 markdown syntax line that *appeared* broken in chat rendering but was correct on disk. The protocol-level resolution: file content verification via `Get-Content + Select-String` reading directly from disk is the canonical-record check; chat rendering is not. Gemini accepted this and stopped iterating after explicit Layer 1 explanation.

**Distribution-builder pattern proved efficient for minimum thumb work.** Files saved to outputs by Claude → downloaded by Mike → moved into repo by single PowerShell command → run with single PowerShell command. Replaces hand-pasting code via Notepad. The pattern handled three distinct builders this session without copy-paste errors.

## Resume anchor for next session

When this conversation resumes (this chat or a new one):

1. Verify HEAD: `git rev-parse HEAD` should return `99782b9`.
2. Verify clean working tree, no uncommitted changes (the local-only output directories shouldn't be in git).
3. Read this log entry: `Get-Content operations_log/2026-05-16_first_phase_4b_execution.md`.
4. First action: route the cross-run probe-mixing fix to Gemini. Specification is in the Pending Layer 1 Finding section above.

— Mike (drafted with Claude, session-end operations log entry, post-execution canonical-record orientation)
