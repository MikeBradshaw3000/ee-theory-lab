# To Layer 3 — Cycle 2 closed, Cycle 3 substrate built fresh

Routing note, drafted by Layer 1 for Mike's routing. Operational state and the discipline every Cycle 3 run routes through.

## What just happened

Cycle 2 is closed with a committed boundary (git tag `cycle2-close`) and a triage record (`cycle2/CYCLE2_CLOSURE.md`). Your v2 work — `phase_4b/scripts/psi_state_spatial_v2.py` plus the `psi_state_spatial_v2_smoke/` and `psi_state_spatial_v2_smoke_patch/` output directories — is committed as Cycle 2's **closing state**. It is preserved as the leading edge of the corrected-observable work, not as Cycle 3's foundation. Cycle 3 does not retrofit it.

One precise note on the two smoke directories, now in the closure record: `_smoke_patch` is a single-cell correction of `_smoke` — Case D (transient wave) `Psi_persistence_I` went 1.0 → 0.0, restoring the expected ≈ 0 for a moving structure. `_smoke_patch` is operative; `_smoke` is preserved as the pre-patch record. Clean catch.

## The Cycle 3 operational mandate

The central Cycle 2 lesson for implementation: **the substrate is built around the "baked in" defense from the start, not retrofitted from legacy telemetry.** Retrofitting a defense onto inherited telemetry is precisely what failed. Cycle 3's substrate is designed fresh so the admissible Ψ observable — state-based, density-adjusted, able to separate persistent coherence from transient organization — is a first-class product of the model, not something reconstructed from columns that happened to be persisted.

The Flight 6 parquet and the `Psi_local` column are not the Cycle 3 substrate. They are closed Cycle 2 artifacts. Do not build Cycle 3 on them.

## The carried-forward control battery

Your five-case synthetic control generator (stable cluster / random low-ρ / random high-ρ / transient wave / uniform-high-persistence) is the model for Cycle 3's standing control requirement (registry test `C3-CTL-001`). It uses **no parquet** — that is the point; it sidesteps substrate trust by construction. Cycle 3 keeps this structure as the minimum battery and may extend it. The permutation-null z-score stays as the degeneracy separator.

## New discipline — every Cycle 3 test is documented before and after

Cycle 3 introduces a per-test documentation requirement. The structure is in `cycle3/` (`CYCLE3_OVERVIEW.md`, `CYCLE3_TEST_REGISTRY.md`, `TEST_RECORD_TEMPLATE.md`). The core of it, which bears directly on implementation work:

Every test carries the **four-level distinction** and never collapses it:
- **L1 implementation** — does the script run, output well-formed? (your domain)
- **L2 measurement validity** — is the quantity the intended one: state-based, density-adjusted, degeneracy-checked? (your domain, with Layer 1 on intent)
- **L3 steady-state eligibility** — did the window earn the label by explicit diagnostics?
- **L4 interpretation** — what it means for Regime-II-as-structural (Mike / Layer 1 only)

A test records the **highest level it cleared**, not a single pass/fail. "The script executed" is L1 only and must never be reported as theory support. This is the structural guard the whole Cycle 3 documentation exists to enforce. When you return implementation work, frame results at the level they actually reach — L1/L2 — and leave L3/L4 to the apparatus and to Mike.

Execution channel remains **Mike only**.

## What is and isn't being asked yet

The Cycle 3 substantive probes are **not** designed. Only three precondition gates are seeded (environment reproduction, the control battery, the steady-state apparatus). The substrate design and probe structure are the open design-phase question — and the Flight 2 experience suggests substrate-led design produced cleaner probe structure than architecture-led. So this is an invitation to shape the Cycle 3 substrate, not a spec to implement.

First operational step when ready: `MESA_ENVIRONMENT_REPRODUCTION.md` in `cycle3/` carries `« FILL »` blocks for the verified environment (Python version, interpreter path, Mesa version, full freeze). Capturing those from the known-good machine is `C3-ENV-001` and the foundation everything else runs on.

Vocabulary discipline binds (ρ/Ψ/Λ — Λ never "terrain favorability"; agents *act*, no decision/optimization/utility/cognitive language; "per-cell active-state values," never "field"; candidates *produce*, never *confirm*).
