# Architectural Review — v1.1 / A3 Drive Function "Divergence"

**Date:** 14 May 2026
**Reviewer:** Claude (Layer 1, architectural analysis)
**Question under review:** Whether Substrate Spec v1.1's local-density formulation of ρ in the drive function and the locked Cycle 1 A3 baseline's global ρ constitute an architectural divergence requiring arbitration

---

## ⚠ Footnote (added 14 May 2026, post-review)

**The framing this review was conducted under was wrong.** The routing note that surfaced the arbitration item (drafted by prior Claude, ABM 4) presupposed that v1.1 and A3 were two specifications at the same architectural level needing reconciliation. The review below propagated that framing and produced a confident recommendation to amend v1.1 to global ρ — a recommendation that would have undone months of Cycle 1-close cross-review work based on a misread of the structural relationship between the AMR paper (mean-field foundation) and Cycle 2 substrate work (spatial frontier beyond MFA).

**The architectural analysis below is correct on its terms.** The structural implications of local-density formulations (spatial bistability risk, Stage 2 Ψ extraction questions, Q operator timescale separation) are real and would matter if v1.1 were a deviation needing reconciliation. But v1.1 isn't a deviation — it is the deliberate spatial substrate that operationalizes the Four Grand Challenges (nucleation/spatial seeding, network topology, narrative dynamics, empirical calibration) computationally, while the A3 baseline is the mean-field limit underlying Phil's manuscript.

**The catch came from Mike's project-level context, not from Claude's architectural review.** Mike's clarification ("this decision does not yet affect the manuscript; we are working on the frontier beyond the MFA paper Phil is working on") resolved the framing rather than the arbitration.

Discipline note for future Claude work: when routing notes pre-frame an arbitration ("update X to match Y, or amend Y to match X"), the architectural review should first verify the framing's premise (that X and Y are at the same architectural level and require reconciliation) before engaging the substantive options.

See `operations_log/2026-05-14_v1_1_relationship.md` for the resolution.

The review below stands as written — the analysis of local-density structural implications becomes substantive forward research content for Cycle 2 work under v1.1 (questions to *answer with* the spatial substrate, not risks to *avoid by* amending it).

---

## Two caveats stated at the time of review

**1.** Claude was taking the H-suite closure on the routing note's word; the actual H-suite output hadn't reached Claude's chat. If interrogating H-suite results on their merits becomes necessary later, the data will need to be in front of Claude.

**2.** Claude had not read v1.1's text directly at the time of writing this review (read it subsequently, after Mike attached the PDF). The "divergence" framing came from prior Claude (ABM 4) based on their reading. Before final arbitration, that reading should be verified against v1.1's actual text. The architectural analysis stands regardless of what v1.1 says; the arbitration depends on what v1.1 actually says.

## 1. Layer 1 theoretical implications of global ρ vs. local ρ in the drive function

The shift is not a parameter choice. It changes the architectural identity of the model in three substantive ways.

**Mean-field vs. spatial bifurcation structure.** Stage 1 as committed is `dρ/dt = μρ − γρ³` (supercritical pitchfork normal form). Global ρ produces this cleanly: agents read a single scalar; dynamics reduce to a 1D map on the macro variable; the Stage 1 transition is a transition of the macro variable as such. Local ρ collapses the macro-variable structure. There is no longer one ρ that bifurcates — each agent reads a neighborhood statistic, the system becomes a coupled lattice of locally-driven sites, and bifurcation analysis applies at a different level (spatial mean-field with correlation corrections, finite-cluster expansions, or directed-percolation universality).

**This is an architectural shift, not an implementation refinement.** It changes what kind of theory Stage 1 is: a mean-field theory of macro-variable bifurcation, or a spatial pattern-formation theory of locally-coupled action streams. Both are defensible; they are different theories.

**Action-not-decision primitive is preserved under either formulation.** Local ρ doesn't reintroduce decision or optimization vocabulary at the agent level — the agent still reads a local statistic and projects stochastically.

**Λ-as-theorist-level-construct.** Under global ρ, agents encounter only a scalar (whole-grid mean). Under local ρ, agents encounter a spatially-varying observable, and the question of whether this is "a field" in the quarantined sense becomes live. Local ρ as a neighborhood statistic is probably not "a field" in the gauge-field-quarantine sense, but it's a closer call than the global case.

## 2. Subcritical / bistable risk under local ρ

**Under global ρ at A3 parameters: monostable.** Verified analytically and empirically. The δ=4 quadratic crowding penalty at η=0.01 keeps the mean-field map's single fixed point smooth through the steepest-slope region around Λ ≈ 0.67. Cycle 1 eliminated A1 and A2 because they produced subcritical/bistable structure violating the committed supercritical-pitchfork commitment.

**Under local ρ: monostability guarantee no longer follows automatically from δ=4.** In local ρ, each agent's drive depends on its neighborhood density. Spatial fluctuations matter. The system can develop spatial clustering (active regions sustain locally even when global ρ is low), effective bistability from spatial structure (coexisting phases at same Λ), and a distinct bifurcation structure (directed percolation transition or Ising-like first-order transition, depending on coupling).

**The architectural risk is real.** Whether it manifests is empirical and would require a fresh H-suite under local ρ to characterize.

**This isn't automatically a reason to reject local ρ.** Under local ρ, bistability between spatial phases is a different phenomenon (spatial coexistence, not Stage 1 hysteresis in the mean-field sense). The question becomes whether the committed architecture allows for spatially-coexisting phases.

## 3. Implications for Stage 2 (Ψ extraction) and Q operator

**Stage 2 (Ψ extraction).** Under global ρ, ρ is a scalar with a clean temporal derivative; Ψ extraction operates on a well-defined macro variable. Under local ρ, ρ becomes a field-like spatial object, and Stage 2 must specify whether Ψ is coherence in the global-ρ time derivative, in some integrated/projected measure of the local-ρ field, or something else.

**Q operator and timescale separation.** Q reads macro state (ρ, Ψ) and writes to v, c, r. Under global ρ: Q reads scalars, writes to scalars. Under local ρ: Q must decide whether it reads the global average of the local-ρ field or the local-ρ field itself.

## 4. Architectural verdict (at time of original review)

**Global ρ is architecturally cleaner** for mean-field-foundation purposes. **Local ρ is a more substantial theory with significant unresolved structural questions** that would need empirical engagement.

Original recommendation was to amend v1.1 to global ρ. The footnote above corrects this: under the corrected framing (v1.1 is the spatial substrate for forward work, not a deviation from A3), the structural questions become forward research content rather than risks to manage.

## What this review surfaces for forward Cycle 2 work

Under the corrected framing, the analysis above becomes the question set for Cycle 2 substrate work on v1.1:

- Does v1.1's spatial substrate produce bistability at intermediate Λ under A3 parameters? *Empirical question for H-suite under v1.1.*
- What does Stage 2 / Ψ_local look like as a spatial field? *v1.1 commits to per-cell Ψ_local with global Ψ as aggregate; Cycle 2 work characterizes the spatial structure.*
- How does Q acting on per-cell Ψ_local produce terrain heterogeneity in v, c, r? *v1.1's diagonal local-input Q produces spatial heterogeneity; Cycle 2 work characterizes the evolution.*
- How do the Four Grand Challenges map onto v1.1's substrate? *All four engageable empirically.*

— Claude (Layer 1 architectural review)
