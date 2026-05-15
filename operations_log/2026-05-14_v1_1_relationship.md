# Cycle 2 Round 1 — v1.1 / A3 Relationship Clarified; No Arbitration Required

**Date:** 14 May 2026
**Phase:** Cycle 2 Round 1, post H-suite closure, pre Flight 1
**Status:** v1.1 "divergence" arbitration item resolved as not-a-divergence. Cycle 2 Round 1 Flight 1 opened against v1.1 implementation as the next substrate gate.

---

## What needed reconciling

A perceived divergence between the locked Cycle 1 A3 baseline (global ρ in the drive function) and Substrate Spec v1.1 (local Moore-neighborhood density in the drive function) was surfaced by prior Claude (ABM 4) as an arbitration item before Cycle 2 Round 1 Flight 1 design. The framing presupposed that v1.1 and A3 were two specifications at the same architectural level that needed to be reconciled, with Claude's architectural review recommending an amendment in one direction or the other.

Reading v1.1 in full alongside the project-level context resolved the framing rather than the arbitration.

## What v1.1 actually is

v1.1 is a fully spatial substrate specification: per-cell bases (v, u, r), per-cell Λ_i = F(b_i), local Moore-neighborhood density in the drive function, per-cell Ψ_local (activation-change correlation), per-cell Q updates (Δv_i = Δu_i = Δr_i = γ_Q · Ψ_local_i), and 25-column telemetry capturing the full per-cell per-tick state. Produced through Layer 2 (ChatGPT) and Layer 3 (Claude) cross-review at Cycle 1 close with Mike's three explicit arbitrations integrated. Eight cross-review items resolved in Section 16.2. No substantive architectural divergence between layers at the time of commit.

v1.1's local-density formulation is a deliberate committed architectural choice consistent with v1.1's whole-substrate spatial commitment — not an isolated parameter that diverges from A3, but one element of a coherent spatial framework.

## What the Cycle 1 A3 baseline actually is

The A3 baseline is the mean-field core that grounds Phil's AMR manuscript. Global ρ, supercritical pitchfork normal form, scalar response curve. The Cycle 2 parity moment and H-suite re-baseline verified that this mean-field substrate produces what mean-field theory predicts to four-decimal precision. That work is sound and remains the analytical foundation of the AMR paper.

A3 is the mean-field limit of the spatial substrate v1.1 specifies, not a competing architectural commitment at the same level.

## The structural relationship

The AMR paper (Phil's manuscript) presents the mean-field foundation. Its commitments: supercritical pitchfork normal form, global-ρ response, "a formal foundation" framing, Four Grand Challenges intentionally handed to the research community as boundaries.

Cycle 2 substrate work is the **frontier beyond the MFA**. The Four Grand Challenges (nucleation/spatial seeding, network topology, narrative dynamics, empirical calibration) are the architectural agenda for forward work, and v1.1 is the substrate that operationalizes them computationally.

The relationship is a two-layer structure:
- **AMR paper / A3 baseline:** mean-field foundation. Settled, verified, sound.
- **Cycle 2 / v1.1 substrate:** spatial extension that engages the Four Grand Challenges directly. Forward work.

This is the project's deliberate two-paper structure (MFA paper → next paper) realized at the substrate level.

## What does not require arbitration

- **v1.1 stays as committed.** No amendment to global ρ. No relitigating the eight cross-review items resolved in Section 16.2. The spatial substrate is what Cycle 2 forward work is built on.
- **A3 baseline stays as the mean-field foundation.** No expansion of A3 to incorporate spatial structure. The mean-field is what the AMR paper grounds itself in.
- **The Cycle 1 archaeology question (0.572 vs. 0.595)** stays parked as an open item about Cycle 1's record. Not affected by this structural clarification.

## What this clarification enables

- **Cycle 2 Round 1 Flight 1 opens against v1.1 implementation as the next substrate gate.** Per pacing discipline (substrate-first, lock before building forward, one well-defined question per flight in early flights), Flight 1's question is the v1.1 parity moment: does an implementation of v1.1 produce the 25-column telemetry, satisfy the realization invariant at full per-(cell, tick) granularity, and pass the F_baseline parity check (telemetry-enabled vs telemetry-disabled runs hash-identical)? This is the substrate trust floor for spatial forward work, parallel to the role A3 parity served for mean-field work.
- **The architectural questions previously framed as risks under local density become substantive forward research questions.** Whether v1.1's spatial substrate produces bistability at intermediate Λ under A3 parameters, whether spatial Ψ_local clusters before population aggregates, how Q-driven terrain heterogeneity develops over runs — these are now empirical questions to answer with v1.1, not architectural concerns to manage by amending it.

## Failure mode caught and recorded

This arbitration item was surfaced under a framing inherited from prior Claude's reading of v1.1, which treated the local-density formulation as a deviation from A3 needing reconciliation. The architectural review (this Claude) initially propagated that framing and produced a recommendation to amend v1.1 to global ρ — a recommendation that would have undone months of Cycle 1-close cross-review work based on a misread of the structural relationship between AMR and Cycle 2.

The catch came from Mike's project-level context ("this decision does not yet affect the manuscript; we are working on the frontier beyond the MFA paper Phil is working on") rather than from Claude's architectural review of v1.1. The framing-asymmetry observation applies here in a sharper form than previously recorded: **pre-structured routing notes can transmit a wrong starting premise that propagates through architectural analysis without the analysis catching it.** Architectural review reads structure under whatever framing it receives; it does not by default check whether the framing itself is correct.

Discipline note for future Claude work: when routing notes pre-frame an arbitration ("update X to match Y, or amend Y to match X"), the architectural review should first verify the framing's premise (that X and Y are at the same architectural level and require reconciliation) before engaging the substantive options.

## What is preserved

- All Cycle 2 Round 1 parity and H-suite closures stand.
- The standing protocol additions from the emulation discovery (no past-tense for unexecuted actions; no synthetic telemetry tables; execution-verification at parity moments; asymmetric execution channel acknowledgment).
- The three-layer discipline structure.
- The Cycle 1 archaeology question (parked).
- The framing-asymmetry observation (Mike-Claude calibration; now with sharper corollary about pre-structured routings).

— Mike (drafted with Claude)
