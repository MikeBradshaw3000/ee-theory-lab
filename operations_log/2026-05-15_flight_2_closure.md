# Cycle 2 Round 1 Flight 2 — Closure: Substantive Cascade Characterization Under v1.1

**Date:** 15 May 2026
**Phase:** Cycle 2 Round 1 Flight 2 — CLOSED
**Status:** Substantive cascade behavior under F_LR and F_2_symmetric characterized at 20×20 and 40×40 over 3000 ticks. Three findings carried forward. Forward planning open for Round 1 closure or Flight 3 design.

---

## Closure summary

Flight 2 produced eight parquet files (four independent production runs, four byte-identical shadow copies per v1.1 Section 13.2) and eight diagnostic CSVs (one per ChatGPT's analytical section). Layer 1 architectural review (Claude): PASS, with all five Flight 1 deferred remediations resolved. Layer 2 substantive review (ChatGPT): PASS, no substrate anomalies, characterization complete, recommended closure without additional probes.

The substrate produces what v1.1 specifies. The F-form characterization that Flight 2 was designed to engage is now empirically grounded.

## Empirical artifacts

**Production runs** (production machine, `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\`):
- F_2_symmetric 20×20: `flight6_probe1_overcrowding_20x20.parquet`, 28.2 MB, 1,200,000 rows
- F_2_symmetric 40×40: `flight6_probe1_overcrowding_40x40.parquet`, 126.6 MB, 4,800,000 rows
- F_LR 20×20: `flight6_probe2_starvation_FLR_20x20.parquet`, 46.2 MB, 1,200,000 rows
- F_LR 40×40: `flight6_probe2_starvation_FLR_40x40.parquet`, 232.7 MB, 4,800,000 rows
- Plus four shadow copies (probe2_starvation_F2sym and probe3_fusion_residual at each scale) per v1.1 Section 13.2

**Diagnostic CSVs** (production machine, `C:\Users\vkz244\EE_Theory_Lab\flight2_analysis_outputs\`):
- `global_timeseries.csv` (3.2 MB) — per-tick aggregates, 17-column schema, 12,000 rows
- `epoch_summary.csv` (18 KB) — 7-epoch summaries with mean/std/min/max, 28 rows
- `selected_tick_distributions.csv` (58 KB) — distribution stats with 11 quantiles at 8 selected ticks
- `psi_sign_decomposition.csv` (2.8 KB) — Ψ_local negative/zero/positive counts and conditional means
- `psi_spatial_diagnostics.csv` (4.7 KB) — Moran's I, same-sign share, connected component stats
- `base_boundary_summary.csv` (5.3 KB) — boundary counts and min/max bases at selected ticks
- `fform_comparison.csv` (2.2 KB) — F_2_symmetric minus F_LR deltas per epoch and scale
- `compression_fingerprint.csv` (1.0 KB) — per-column compressed sizes and cardinality counts

**Realization invariant satisfied at full per-(cell, tick) granularity:** 0 mismatches across 12,000,000 total row-level checks. Section 14.2 properly honored via post-execution persistence-layer verification, not the tautological in-memory check from Flight 1's first draft.

## Three substantive findings carried forward

**Finding 1: F-form distinguishability is sharp and scale-stable.**

Under matched PRNG seed and locked A3 parameters (α=4, β=3, δ=4, γ=4, η=0.01), F_2_symmetric and F_LR produce distinct cascade regimes that persist across 3000 ticks at both 20×20 and 40×40 scales.

| Metric | F_2_symmetric | F_LR | Ratio |
|---|---|---|---|
| ρ, epoch 0-99 (40×40) | 0.089 | 0.305 | 3.4× |
| ρ, epoch 2500-2999 (40×40) | 0.067 | 0.226 | 3.4× |
| Λ, epoch 0-99 (40×40) | 0.322 | 0.674 | 2.1× |
| drive, epoch 0-99 (20×20) | -2.53 | -0.87 | -- |
| p_act, epoch 0-99 (20×20) | 0.087 | 0.305 | 3.5× |

The mechanism: F_2_symmetric's multiplicative gate `v·u·r ≈ 0.42` with bases ~0.75 multiplied by the weighted-additive term `0.33v+0.33u+0.34r ≈ 0.75` yields Λ ≈ 0.32. F_LR's `min(v,u,r)` with three iid U(0.6, 0.9) bases yields E[min] = 0.6 + 0.3/4 = 0.675. The ~2× Λ difference flows directly into drive (term_Lambda = α·Λ), then through sigmoid into p_act, then into ρ via realization. Both Λ values match analytical mean-field predictions from the base distribution within ~1% — substrate produces what mean-field theory predicts at the population aggregate.

Scale comparison: 40×40 reproduces the 20×20 means with expected variance reduction (ρ_std drops by ~50% as N quadruples — consistent with finite-size scaling on uncorrelated tick-by-tick stochasticity). The F-form ratios are scale-invariant within 1%.

**Theoretical implication:** F_2_symmetric is *evaluable* (Λ ≈ 0.32 far above ε_Λ = 0.05) but produces a quiescent cascade rather than a moderate-activation cascade. Flight 5's framing of F_2_symmetric as "leading reformulation candidate" for Open Element 14 is not contradicted — F_2_symmetric remains a valid candidate — but the specific property of "evaluability" is now distinguished from "activation-generating at parity with F_LR" as separate questions. Future F-form arbitration must engage both distinctly.

**Finding 2: Q operates on a slow timescale relative to the cascade but is cumulatively consequential over 3000 ticks.**

Bases drift downward in all four runs because average Ψ_local is slightly negative across all epochs (slightly more correlated deactivations than correlated activations):

| Run | mean_v, t=0 | mean_v, t=2999 | drift | rate per tick |
|---|---|---|---|---|
| F_LR 40×40 | 0.7502 | 0.6503 | -0.10 | -3.3 × 10⁻⁵ |
| F_LR 20×20 | 0.748 | (similar pattern) | -- | -- |
| F_2_symmetric 40×40 | 0.7513 | 0.7052 | -0.05 | -1.6 × 10⁻⁵ |
| F_2_symmetric 20×20 | 0.7489 | (similar pattern) | -- | -- |

The mechanism: F_LR's higher activation turnover produces more nonzero Ψ_local events per tick. Average Ψ_local accumulates more negative magnitude per tick under F_LR than under F_2_symmetric. Q (Δv = Δu = Δr = γ_Q · Ψ_local with γ_Q = 0.001) writes that history into bases. F_LR's bases decline ~2× faster than F_2_symmetric's.

**Theoretical implication:** The final-epoch cascade is being driven by Λ values 5-15% lower than the initial cascade. The system has memory. v1.1 is operationally doing work beyond the AMR paper's mean-field reformulation: Q-driven terrain evolution is a real architectural mechanism producing dynamics distinct from fixed-base mean-field intuition. This empirically validates the "frontier beyond MFA" framing of Cycle 2 substrate work.

**Finding 3: No macroscopic Ψ coherence emergence at these parameters and 3000-tick horizon.**

Moran's I for Ψ_local sits in the 0.08-0.15 range across runs and ticks after the initialization transient — modest positive spatial autocorrelation, not strong spatial ordering. Largest same-signed connected component stays in single digits. Moran's I for is_active stays near zero, meaning activation state itself does not form large spatial patches; the modest Ψ_local correlation reflects local transition events, not persistent activation regions.

Ψ_local participation: F_2_symmetric has roughly 1450-1500 of 1600 cells with zero Ψ_local at any sampled tick at 40×40; F_LR has roughly 400-500 nonzero. F_LR's larger participation reflects its higher activation turnover but does not produce coherent system-spanning regions.

**Theoretical implication:** The AMR paper's Grand Challenge 1 (nucleation/spatial seeding dynamics) names this question as future work. Flight 2 data says it does not happen at A3 parameters and U(0.6, 0.9) initialization in 3000 ticks. This is a substantive empirical scoping of what counts as the Grand Challenge: any future demonstration of nucleation must produce conditions where Moran's I rises substantially above 0.15 and component sizes scale into the system-spanning regime. Flight 2 establishes the empirical baseline against which nucleation-demonstration work must register.

## Five Flight 1 deferred remediations: fully resolved

1. **Realization invariant on persisted parquet values** — implemented as separate post-execution verification reading PRNG_draw, p_act, is_active columns from .parquet. Section 14.2 honored at full per-(cell, tick) granularity. Zero mismatches across 12,000,000 row-level checks.
2. **Mesa-NumPy parity-comparison artifact** — deferred indefinitely on practical grounds (Mesa 3.x API/performance issues). NumPy declared canonical baseline per v1.1 Section 4 alternative-implementation note.
3. **Execution timestamp in parquet metadata** — present in all four production parquet files as ISO 8601 UTC.
4. **File size in completion-verification output** — present in all four post-execution verification blocks.
5. **Stale Mesa comment** — removed from substrate.

## What Flight 2 establishes

- The substrate trust floor extends from Flight 1's channel verification (F_baseline parity) to Flight 2's signal verification (F_LR and F_2_symmetric cascade behavior). Both are empirically grounded.
- v1.1's spatial substrate is operational across both scales the spec requires.
- The eight production parquet files become the canonical empirical record for any subsequent analytical work (Phase 4B, methodology paper, next paper).
- The three substantive findings become Cycle 2 Round 1's contribution to Cycle 2 knowledge, separable from any forward Flight 3 work.

## What Flight 2 does not establish

- Variance across PRNG seeds at fixed parameters (single-seed runs; repeat-seed analysis is candidate Flight 3a work).
- Whether macroscopic Ψ coherence can emerge under different parameters, initial conditions, or longer timescales (candidate Flight 3b, 3c work).
- Long-time behavior beyond 3000 ticks where Q-driven base drift may reach boundary regimes.

These are forward research questions, not Flight 2 gaps.

## Process notes

**Two mode-switching incidents with Gemini observed during Flight 2 preparation:**
1. Flight 2 substrate first draft (fast mode): all-in-one orchestrator without flagging the memory trade-off that Mike's 16 GB system would surface at 40×40. Caught in Layer 1 pre-execution review. Patched directly by Claude with chunked streaming writes and per-run CLI dispatch.
2. Flight 2 analysis script first draft (fast mode): incomplete delivery against ChatGPT's seven-section specification (missing epoch_summary.csv entirely, missing fform_comparison.csv entirely, multiple section-3 quantiles absent). Caught in Layer 1 pre-execution review. Rewrite requested in advanced mode; advanced-mode rewrite delivered all seven sections; three targeted patches further requested (probe1 sort, defensive column access, methodological caveats); patches honored.

Pattern: fast-mode Gemini under-delivers on substantive specifications, particularly on routine-but-load-bearing aggregation work that doesn't appear as visibly-interesting computation. Advanced-mode Gemini delivers cleanly when explicitly asked. Worth monitoring as a calibration item; not yet a new standing rule, but if a third instance occurs, consider adding a "verify mode before forwarding substantive work" check at routing-out steps.

**Layer 1 pre-execution review extended to analysis scripts**, not just substrate scripts. This is an extension of standing rule #3 (execution-verification at parity moments). Analysis scripts that produce Layer 2 inputs are functionally equivalent to substrate scripts in their gating role; Layer 1 review of analysis scripts before execution prevents waste from incomplete or buggy analytics reaching Layer 2 review.

**Standing rule #5 (gate-closing artifacts route to all reviewing AIs)** held cleanly across Flight 2 execution. Both the Flight 2 production outputs and the Flight 2 analysis CSVs reached both reviewing AIs at the moment of closure, with raw artifacts (terminal outputs, file sizes, row counts, sample CSV rows) rather than summary status.

— Mike (drafted with Claude, Cycle 2 Round 1 Flight 2 closure)
