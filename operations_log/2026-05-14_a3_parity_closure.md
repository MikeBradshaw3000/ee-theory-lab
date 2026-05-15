# Cycle 2 Round 1 — A3 Parity Closure at ρ ≈ 0.595

**Date:** 14 May 2026
**Phase:** Cycle 2 Round 1, A3 Parity Moment — CLOSED
**Status:** Parity floor established at ρ ≈ 0.595 (analytical 0.59520, empirical 0.59507). H-suite reproduction track opened (see `2026-05-14_cross_chat_sync.md` and Flight 1 closure for subsequent work).

---

## Closure summary

The Cycle 2 Round 1 A3 parity moment closed against the analytical mean-field fixed point of the stated A3 equation at γ=4, η=0.01, Λ=1.0, with bit-level reproducibility across two independent machines and four-decimal agreement between empirical and analytical values.

**Parity floor:** ρ ≈ 0.595
- Analytical (mean-field fixed point of stated A3 equation): 0.59520
- Empirical (10-seed parity run on production machine, Mesa 3.5.1): 0.59507
- Independent cross-machine reproduction (Claude's Mesa 3.5.1): 0.59507
- Across-seed SD (both machines): 0.00086
- Intra-run SD (typical): ~0.026

The Cycle 1 record's target value of 0.572 was not reproduced. It falls ~22 across-seed-SD below the empirical mean.

## Empirical data

10-seed parity run, A3 baseline, Λ=1.0, η=0.01, γ=4, β=3, δ=4, α=4, 500 ticks, 200 discarded as transient, equilibrium average over ticks 200–499:

| Seed | eq_ρ     | intra_run_SD |
|------|----------|--------------|
| 0    | 0.594700 | 0.024931     |
| 1    | 0.594658 | 0.026667     |
| 2    | 0.595750 | 0.026193     |
| 3    | 0.593992 | 0.025767     |
| 4    | 0.595233 | 0.025889     |
| 5    | 0.595483 | 0.026285     |
| 6    | 0.593683 | 0.028731     |
| 7    | 0.595342 | 0.026137     |
| 8    | 0.596633 | 0.027451     |
| 9    | 0.595225 | 0.026337     |

## Execution environment

- Machine: production (Mike's workstation)
- Path: `C:\Users\vkz244\EE_Theory_Lab\`
- Cycle 1 venv archived to `venv_cycle1_archive`
- Cycle 2 venv: fresh, created during this session
- Mesa version: 3.x (current at install time)
- Dependencies: mesa, numpy, pandas, networkx
- Script: `headless_parity_check.py` (Claude's patch of Gemini's posted code; single-line patch `self.agents.count` → `len(self.agents)`; primitive/vocabulary/drive-function logic unchanged)
- Script write method: BOM-safe `[System.IO.File]::WriteAllText` with no-BOM UTF8Encoding

## Architectural ground reaffirmed

- A3 equation: `drive_i = α·Λ + β·ρ − δ·ρ² − γ`; `p_act_i = σ(drive_i) + η·(1 − σ(drive_i))`
- σ: standard logistic
- ρ: global (whole-grid fraction active at previous tick)
- Locked parameters: α=4, β=3, δ=4, γ=4, η=0.01
- Grid: 20×20 torus, 400 binary-state agents
- Update: synchronous two-phase
- Equilibrium protocol: 500 ticks, 200 discarded, average over 200–499

This specification is verified internally consistent: substrate produces the analytical fixed point at four-decimal precision.

## H-suite re-baseline closure

After parity closed, the H-suite battery (H1 Λ-sweep, H2 hysteresis, H3 η-sensitivity) was reproduced against analytically-derived expected values at γ=4. Empirical-vs-analytical agreement was within 0.0014 across all 22 measurements (11 Λ values in H1, 6 bidirectional sweep values in H2, 5 η values in H3). Systematic empirical-below-analytical pattern of ~0.001 magnitude was attributed by ChatGPT's Layer 2 review to ordinary finite-size stochastic scaling — sub-agent-scale deviations on a 400-agent grid, consistent with Jensen's-inequality-style finite-size correction to the curved sigmoid response. Monostability empirically supported across all H2 Λ values (gaps < 0.001). η-shift magnitude matched analytical prediction almost exactly (empirical 0.05207 vs analytical 0.05194).

ChatGPT's formal Layer 2 conclusion: "Layer 2 accepts the Cycle 2 A3 substrate as analytically coherent with the stated mean-field map. The H-suite results reproduce the deterministic fixed-point branch, the monostable no-hysteresis prediction, and the η sensitivity structure within expected finite-size stochastic tolerances for a 400-agent grid. No structural anomaly warrants pausing. The Cycle 2 A3 baseline is clean from the Layer 2 mean-field vantage."

## Cycle 1 archaeology question (open, parked)

The Cycle 1 record's H-suite values do not match the analytical predictions of the stated A3 equation:

| Endpoint              | Cycle 1 record | γ=4 analytical | γ=4.135 analytical |
|-----------------------|----------------|----------------|--------------------|
| Λ=0, η=0.01           | ≈ 0.029        | 0.02935        | 0.02683            |
| Λ=0.5, η=0            | ≈ 0.15         | 0.16636        | 0.14344            |
| Λ=0.5, η=0.01         | (not recorded) | 0.17712        | 0.15445            |
| Λ=0.5, η=0.05         | ≈ 0.20         | 0.21830        | 0.19680            |
| Λ=1.0, η=0.01         | 0.572          | 0.59520        | 0.57198            |

The Cycle 1 record is internally consistent under effective γ ≈ 4.135, not γ = 4.0. The fit holds simultaneously across all four data points.

Three readings remain live:

- **(i) Cycle 1 ran γ=4 honestly; 0.572 and the H-suite endpoints are substrate-drift artifacts.** The Stabilization Mode discovery at Cycle 1 close gives this specific support — known substrate drift was active during some portion of Cycle 1.
- **(ii) Cycle 1 ran with effective γ ≈ 4.135 (or equivalent drive offset) in the actual code; the parameter record is inaccurate.** The joint fit across four endpoints under one γ value is too clean to dismiss.
- **(iii) Mixed provenance.** Some Cycle 1 endpoints real, some artifact. The pure Mesa-version-artifact reading is ruled out — two independent Mesa 3.x installs (Claude's and Mike's) produce 0.595, and ChatGPT's non-Mesa finite-N simulation also produces 0.595.

This question is recorded as open and parked. To be revisited when the methodology paper interprets Cycle 1 substrate. Not blocking Cycle 2 forward work.

## What is preserved from before the emulation discovery

- A3 architecture (Cycle 1 commit, not under test)
- Substrate spec v1.1 local-density formulation (subsequently clarified as not-a-divergence; see `2026-05-14_v1_1_relationship.md`)
- Three-layer discipline structure (reinforced)
- Pacing discipline from Cycle 1 close
- The vocabulary quarantine
- The framing-asymmetry observation (Mike-Claude calibration)

## Status of forward work

- A3 parity moment: CLOSED at ρ ≈ 0.595
- H-suite reproduction track: CLOSED via Layer 2 acceptance
- Cycle 1 archaeology: PARKED, three readings recorded
- v1.1 local-density "divergence": resolved as deliberate two-layer structure (see `2026-05-14_v1_1_relationship.md`)

— Mike (drafted with Claude)
