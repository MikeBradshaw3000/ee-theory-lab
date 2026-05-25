# Coherence Observable — L1 / L2 Synthesis and the Replacement Specification

**Status.** Synthesis of the independent Layer 1 (architectural) and Layer 2 (mean-field)
reads. The two converged independently — Layer 1's read was withheld from Layer 2 — so the
core diagnosis is a genuine cross-check, not a framing artifact. The open threads below are
preserved, NOT closed. The architectural commit (reframe-and-recompute vs. new substrate)
remains Mike's.

## The converged diagnosis
The persisted `Psi_local` (= ds_a × Σ over neighbors ds_n, averaged) is **not** the
coherence order parameter Ψ. Both reads independently land on: it is a signed
nearest-neighbor correlation of activation *changes* — a transition / fluctuation /
susceptibility statistic (≈ ⟨Δx_i Δx_j⟩), not a sustained-state order parameter
(≈ ⟨x_i x_j⟩). It does not bake in the second normal form (good) — but it avoids doing so
by measuring a different object.

## Two failure directions now mapped
- **Change-based measure (the current `Psi_local`):** reads ≈ 0 for a stable coherent
  configuration that has stopped switching → false negative at steady state; fails the
  positive control. (Layer 1 + Layer 2.)
- **Raw active-state co-activation (the naive fix):** a high-ρ configuration mechanically
  produces many active–active neighbor pairs, so it reads high from density alone → false
  positive; re-imports ρ into Ψ (ρ-redundancy; the B1 concern, re-arising at the observable
  level). (Layer 2's key addition.)

The admissible observable must thread both: **state-based** (survives steady state) AND
**density-adjusted** (not reconstructible from ρ).

## Requirements on any Ψ observable
1. Built on the per-cell active-state values x_i ∈ {0,1}, not the activation-change values
   Δx_i. (Survives steady state.)
2. Density-adjusted: measures spatial organization beyond what ρ predicts — e.g.
   ⟨(x_i−ρ)(x_j−ρ)⟩ over neighbors, or M(t) − ρ². (Not ρ-redundant.)
3. Persistence-weighted (candidate): spatial co-activation that persists over a window, so
   transient clusters do not read as coherence. (Coherence is sustained.)
4. Passes the positive control: a stable mutually-reinforcing active cluster reads high; a
   random configuration at the same ρ reads ≈ 0; a high-ρ unstructured configuration does
   not read high; a transient synchronized-switching wave does not read as persistent Ψ.
   (`defeat_baked_in.md` §5.3.)

## Candidate families (Layer 2, attributed; minimal admissible, not committed)
- A — centered spatial autocorrelation ⟨(x_i−ρ)(x_j−ρ)⟩ over neighbors.
- B — density-adjusted co-activation M(t) − ρ².
- C — A or B weighted by temporal persistence over a window W.

These map onto the flight catalog's B2(A) (spatial autocorrelation) and B2(C) (temporal
autocorrelation, lag τ). The right Ψ observable plausibly lives in that B2(A)+B2(C) space,
density-adjusted.

## The fork, reframed
What was wrong was the statistic computed and labeled Ψ, not the underlying data. The raw
material is the per-cell active-state values, which the substrate already persists
(`is_active` at cell-tick resolution). If so, a density-adjusted spatial(+temporal)
autocorrelation observable can likely be computed from the **existing** Flight 6 parquet —
no new substrate run. The fork tilts toward reframe-and-recompute over commission-new.

Contingent on two substrate facts Layer 1 cannot verify (past horizon; for Gemini / Mike
against the substrate):
- **Q1:** are cell positions (or a stable cell index → grid coordinates) persisted
  alongside `is_active`, so spatial autocorrelation is computable from existing telemetry?
- **Q2:** what were the flights' B2(A)/B2(C) autocorrelations computed over — `is_active`
  (state) or `Psi_local` (transition)? If state, the catalog's Ψ_B2 is already close to the
  right object and may be near-salvageable; if transition, it shares the flaw.

## Preserved, not collapsed
`Psi_local` is not discarded. As a susceptibility / fluctuation correlation it may be a
legitimate *secondary* diagnostic — fluctuation correlations peak near critical points, and
this connects to η(t) (fluctuations near criticality). Reclassified, not deleted.

## Reclassification language (manuscript / record)
"`Psi_local` is a substrate column name, not a confirmed operationalization of the
theoretical Ψ. It is a local transition-correlation statistic measuring synchronized
activation-state changes among neighboring cells; it may serve as a fluctuation /
susceptibility diagnostic but is not the primary observable for persistent coherence." The
primary coherence observable is defined separately, per the requirements above.

## Routing
- **Gemini (Layer 3):** (a) confirm/correct the §1 read on the located code; (b) answer Q1
  and Q2 against the substrate; (c) if Q1 is affirmative, design the density-adjusted
  spatial(+temporal) autocorrelation observable + positive control + steady-state test,
  computed from the persisted `is_active` values — a runnable artifact for Mike, not
  executed.
- **Mike:** arbitrate the fork once Q1/Q2 return; the answer likely turns on them.
- **Manuscript / Phil:** the reclassification language; the observable requirements as the
  operationalization of Ψ.
