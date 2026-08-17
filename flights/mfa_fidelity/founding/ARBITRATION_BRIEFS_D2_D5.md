# Arbitration Briefs — D2 (Q Read-Locality) and D5 (Coherence Observable)
**Prepared for Mike's rulings. Each brief lays the theory question, L2's adversarial input, the verified substrate facts, and the decision options with their consequences on one page. These are the last two open nodes before merge-specification drafting. A third, smaller arbitration surfaced by L2's review (unified core vs. compatibility modes) is appended as Brief 3.**

---

## Brief 1 — D2: What does Q's activation input read?

**The theory question.** The MFA commits Q(v,c,r; ρ,Ψ): the slow channel reads the activation state as well as coherence, yielding the regime-dependent memory prediction (P4: Regime III imprints deeper than Regime II at matched exposure). The MFA's ρ is a macro aggregate. The substrate must commit *what the implemented Q actually reads* — and the two candidates are different theories of how uncoordinated density stains the ground:

- **Local read:** Q reads the Moore-neighborhood active fraction. Theory: *activity conditions the ground where it occurs* — a locus's conditions improve because action happened around it. Mesoscopic, substrate-honest, consistent with everything else in the architecture being local.
- **Global read:** Q reads the grid-wide activation mean. Theory: *the system-level activation state conditions every locus's ground* — region-wide activity levels reach places no activity touched. Macro-to-local, MFA-literal.

**L2's adversarial input (accepted into the record).** These are not cheap and expensive versions of one mechanism; they are different mechanisms. *"If D2 is intended to test macro influence on local interactions, global ρ is the conceptually correct read. Local density cannot substitute for it merely because it is already available."* L2 further supplies the clean causal timing for the global variant — ρ_global computed from the pre-update state, entering the post-update Q that affects tick t+1, one-tick causal separation — and the telemetry decomposition (separated Q-from-Ψ and Q-from-ρ terms per base) required for Tier-1 recomputation under either choice.

**Verified substrate facts.** Local: `Local_Density` already computed and persisted every tick; zero new computation. Global: one per-tick scalar reduction, negligible compute, one new persisted value. Cost is symmetric to first order and **does not decide the arbitration** (facts record, observation 1).

**Theory-side considerations (L1).** Two points for the scale. First, P4 is an *MFA prediction*, and the MFA's Q reads the macro aggregate; a local-read implementation tests a *substrate-honest analog* of P4, not P4 as written — if the flight's purpose is MFA fidelity, the global read is the faithful instantiation, with the local read as the natural comparator. Second, the channel structure: a global ρ-read gives Q a common-mode input — every locus written by the same scalar — which rhymes with the shared-signal channel and would make the slow channel itself two-channel (local Ψ_local write + common ρ write). That is architecturally elegant and also worth naming *before* choosing, because it means the global read quietly imports the two-channel structure into Q, with interpretive consequences for E4's memory findings.

**Options and consequences.**
- **(a) Global read (L2's recommendation for the fidelity purpose):** faithful to the MFA's Q(ρ,Ψ); P4 tested as written; requires the new scalar + decomposed telemetry; makes Q's activation channel common-mode.
- **(b) Local read:** substrate-honest, fully recomputable today; tests a mesoscopic analog of P4; keeps Q entirely local, uniform with the rest of the architecture.
- **(c) Both, separately switchable (superset):** implements the decomposition L2's telemetry already anticipates; costs contract complexity and evaluability budget; makes the local-vs-global question itself an experimental axis rather than a commitment.

**Decision requested:** (a), (b), or (c), and if (c), which is primary for P4's claim ladder.

---

## Brief 2 — D5: Which observable carries Ψ in the regime determination?

**The theory question.** E2's regime classification — the flight's center — requires a pre-seed commitment of what counts as coherence. The standing record holds two co-equal candidates by explicit reservation (state-based spatial statistic; persistence-based statistic), with the arbitration reserved as ontological — Mike's, never resolved by statistical convenience. The MFA's verbal definition ("compatibility of separately undertaken actions... stabilize and extend a recognizable participation order") is the theory-side anchor and leans persistence-flavored without resolving the question.

**L2's adversarial input (accepted into the record).** The verified sources establish the lineages' observational objects are **non-equivalent on six axes** (primitive input, temporal support, spatial meaning, normalization, null structure, aggregation level): Lineage A's Ψ_local is a local, tick-level *change-coupling* quantity inside the causal update; Lineage B's Moran-state and persistence measures are window-level *spatial-organization* statistics with permutation nulls. Therefore: *"Do not make the merge choose by deletion. Emit both observational families and assign their claim roles explicitly."* And: the safest first merged flight *treats the observational families as distinct and tests their relationship rather than presuming it.*

**Verified substrate facts.** Ψ_local is part of Lineage A's committed update and telemetry (it drives Q) and is recomputable row-level; Moran-state and persistence are the committed Cycle-3 apparatus with their own preflight parity harness. Emitting both is an emission-schema decision, not new science; any *aggregate* of Ψ_local used as a macro read must be separately defined, not presumed equivalent to either Moran statistic.

**Theory-side considerations (L1).** L2's input reframes the arbitration usefully: the question is not "which statistic is Ψ" as a deletion choice, but **role assignment** — which family carries the *claim* in E2's ladder, with the other(s) emitted as committed secondary observables. Three role-relevant facts: (i) Ψ_local cannot be dropped regardless — it is causally inside Q, so it is emitted whatever is ruled; (ii) the MFA anchor and the field program's eventual measurement targets (transition-correlation in action streams, persistence-under-withdrawal) both sit closer to change-coupling and persistence than to static spatial organization; (iii) the E2 evaluability budget prices the choice: co-primary doubles the gate surface, and the Stage 2 lesson (stacked conservative gates consuming evaluability) argues against co-primary unless the compound budget is explicitly forecast and accepted.

**Options and consequences.**
- **(a) Primary: persistence family; Moran-state and Ψ_local-aggregate as committed secondaries.** Closest to the MFA anchor; single-primary keeps E2's evaluability budget tight; regime claims read "activation sustained without persistent coordination."
- **(b) Primary: state family (Moran).** Closest to "spatial organization" as the field intuitively reads it; inherits the drive-imprint and density-artifact guard burden TCOP already mapped.
- **(c) Co-primary (both families).** Strongest claim if both agree; doubled gate surface and compound conservatism budget; TCOP's fate is the cautionary precedent.
- **(d) L2's relational variant:** first merged flight makes *the relationship between the families* an explicit E2 sub-question (do they classify the same runs the same way?), with the primary-role commitment deferred to the second contract, informed by that relationship. Lowest presumption; costs one contract cycle before a regime claim can be made.

**Decision requested:** role assignment (a)–(d). If (d), note that E2's headline claim in the first contract is then about observable concordance, not regime existence — a deliberate sequencing choice worth making eyes-open.

---

## Brief 3 (new, from L2's review) — Merge architecture: unified core or compatibility modes?

**The question L2 surfaced.** The withdrawn "one bit-exact gate" claim exposes a real architectural choice: (a) **one unified execution path** — single RNG regime, single update-rule framework; ancestors verified by one bit-exact A gate plus one B rule-equivalence gate; simplest specification and verification surface; or (b) **compatibility-mode architecture** — `lineage_a_native` and `lineage_b_native` modes preserving each ancestor exactly (two bit-exact gates), plus the experimental merged mode as, in L2's phrase, *"a new experimental instrument with two ancestor witnesses."* Option (b) buys a second bit-exact gate and cleaner ancestor custody at the cost of maintaining two RNG backends and a three-mode specification, with the wrong-values-under-right-names surface tripled.

**L1 note:** (b)'s framing — the merged flight as a new instrument witnessed by both ancestors, not an interpolation between them — is the honest description under either option and should enter the merge specification's language regardless of the ruling.

**Decision requested:** (a) or (b). This ruling is upstream of the parity section's drafting; D2/D5 are independent of it and can be ruled in any order.

*End of briefs.*
