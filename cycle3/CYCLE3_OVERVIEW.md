# CYCLE 3 — Overview

**Status:** opening
**Owner:** Mike (Layer 1 arbitration; execution channel Mike only)
**Opened:** 2026-05-24 close of Cycle 2 → Cycle 3 begins
**Document set:** `CYCLE3_OVERVIEW.md` (this file) · `MESA_ENVIRONMENT_REPRODUCTION.md` · `CYCLE3_TEST_REGISTRY.md` · `TEST_RECORD_TEMPLATE.md`

---

## 1. What Cycle 3 is

Cycle 3 designs the substrate, observables, controls, and documentation correctly from the start, around the "baked in" defense, rather than retrofitting from legacy telemetry. It is a clean test plan, not continued custodial repair of Cycle 2 artifacts.

Cycle 3 is **not** a repudiation of Cycle 2. Cycle 2 succeeded: it revealed *why* the inherited substrate and the `Psi_local` diagnostic could not carry the manuscript-facing claim. Those lessons are inputs to Cycle 3, not failures to be hidden. The numbering is continuous on purpose.

## 2. What Cycle 2 produced (carried forward, not reopened)

These are settled. They are the reason Cycle 3 exists in the form it does. None of them is to be re-litigated absent a *new* primary-source conflict.

1. **`Psi_local` is not Ψ.** `Psi_local` is a transition / susceptibility statistic built on activation-state *changes* (≈ signed correlation of Δ activation across cells). It reads ≈ 0 for a stable coherent configuration that has stopped switching. It is the right object for the "it measures, doesn't impose" point and the wrong object for sustained coherence.
2. **An admissible Ψ observable must be three things at once:** state-based (survives steady state), density-adjusted (not reconstructible from ρ), and able to separate *persistent* coherence from *transient* spatial organization.
3. **Steady-state windows are earned, not assumed.** Eligibility is established by explicit diagnostics (drift, range/mean, density coefficient of variation), never asserted.
4. **Positive controls are required before any output is interpreted.** A small value with no control is ambiguous between "no coherence" and a measurement degeneracy.
5. **The substrate must be built around the "baked in" defense from the start.** Retrofitting a defense onto legacy telemetry is what failed.
6. **The protocol remains necessary**, but its job is now to move toward a clean Cycle 3 test plan, not to keep repairing Cycle 2 artifacts.

For the full Cycle 2 forensic record (B2 source location, canonical-vs-ancestor finding, proliferation flag, the corrected-observable pair and its withheld interpretation), see the 2026-05-24 continuity note. That note is the closing record of Cycle 2; this set opens Cycle 3.

## 3. The four-level distinction (the spine of all Cycle 3 documentation)

Every test record keeps these four levels separate and never collapses them. A test can clear one and fail the next. "The script executed" is level 1 only.

| Level | Question | Who settles it |
|---|---|---|
| **L1 — Implementation correctness** | Does the script compute what it claims, without error? | Layer 3 / Layer 2 |
| **L2 — Measurement validity** | Is the quantity it computes the quantity we intend (state-based, density-adjusted, degeneracy-checked)? | Layer 3 / Layer 2, with Layer 1 on the intent |
| **L3 — Steady-state eligibility** | Did the window earn the label that makes the value interpretable as Regime II? | Diagnostics decide; Layer 1 confirms the label |
| **L4 — Manuscript interpretation** | What does the value *mean* for Regime-II-as-structural? | Mike / Layer 1 only |

The interpretation seam is sharp and is crossed only deliberately, with Mike arbitrating: "does it compute correctly" is L1/L2; "what it means" is L4. The registry and the per-test template both enforce this seam structurally.

## 4. The load-bearing open question (held open on purpose)

Which observable, if either, *is* Regime-II coherence — per-tick state organization that persists, or the same cells persistently clustered — turns on coherence-as-relational-mutual-reinforcement (the `defeat_baked_in` hinge), **not** on which statistic is more robust. Cycle 3 must not let this be decided by statistic robustness or by script naming. The candidate observables are held as a co-equal pair until Layer 1 / Mike settle the ontology.

## 5. Out of scope for Cycle 3

- Reopening the B2-source file hunt (closed; `tier2_analyze.py` is the located source, pointed to in the canonical record).
- Substrate-trust forensics on the Flight 6 parquet (closed absent a new conflict).
- Spawning further copies of the Tier 2 analysis script. The durable fix is a pointer, not a seventh twin.
- Any reading of a Flight 6 value as "Regime II" without first inheriting the uncertain-authority trust question for that substrate.

## 6. Vocabulary (binding — applies in every Cycle 3 document, including wrap-ups)

- ρ = activation density
- Ψ = coherence
- Λ = structural conduciveness (**never** "terrain favorability")
- Agents **act** — no decision / optimization / utility / cognitive language
- "the point(s) at which μ(ρ) = 0" — **never** `ρ_c`
- "per-cell active-state values" / "active-state configuration" — **never** "field"
- Candidates **produce** or **fail to produce** — **never** "confirm" / "demonstrate"
- Synthesis is the work; convergence is a phenomenon that sometimes occurs (and is recorded as such, not engineered)
