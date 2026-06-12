# Rule E (lagged-Lambda conditioning) - design contract

**Status: DESIGN CONTRACT. NON-SEEDING. Layer 2-reviewed; precision amendments of 2026-06-12 incorporated.** This contract formalizes the Rule E mechanism class, the canonical lag construction, the separability requirement, the contrastive success criterion, and the block-resolved recording requirement, so that any future Rule E probe is designed against fixed criteria. It does NOT seed a probe, does NOT specify a final alpha grid, and does NOT authorize Layer 3 implementation. Opening any run remains Mike's call, gated on resolution of the named opens in Section 7.

Governing upstream document: cycle3/wave_two/RULE_E_SCOPING_RESULT.md (the scoping result). On any discrepancy between this contract and the scoping result regarding admissibility, the scoping result governs until this contract is committed as canonical; after commitment, this contract governs Rule E design and the scoping result governs admissibility rationale.

Drafted by Layer 1; Layer 2-concurred with amendments; Mike arbitrates commitment.

---

## 1. Mechanism class (fixed)

Rule E is **lagged-Lambda conditioning**: a slow, block-lagged macro activation-density signal conditions the locally-configured Lambda each cell sees. This is the first wave-two-adjacent mechanism in which a macro signal acts back on the local update; in Rules C and D, rho is an emergent readout that never re-enters the rule.

Two admissibility conditions, both binding (scoping result):

1. **Slow / block-lagged.** The macro signal must be slow enough relative to the becoming-active update to constitute a genuinely exogenous conditioning input for the block it conditions, not a disguised reading of the rule's own current output. Precision (Layer 2 amendment): the macro signal is **historically endogenous but target-block-separated** - it is computed from the system's own prior activity, so it is not exogenous in origin; its exogeneity is relative to the target block, secured by the completed-prior-block construction and the measured separation of timescales. This places Rule E on the legitimate slow macro-to-local channel rather than the prohibited fast rho-on-its-own-rule channel.
2. **Lambda-configuration locus only, becoming-active channel only.** The macro signal may condition only the locally-configured Lambda, and the conditioned (effective) Lambda enters ONLY the becoming-active / Lambda-configuration channel. Precision (Layer 2 amendment): conditioned Lambda must NOT leak into survival or turnover - where the base rule parameterizes survival from Lambda (as Rule C ties s_Lambda to the Lambda anchor), survival and any turnover hazard continue to operate on the UN-conditioned base Lambda configuration. A construction in which effective Lambda implicitly propagates into s_Lambda or theta_turnover is a breach of this clause, not an implementation detail.

**Inadmissible forms (the four fenced forms, carried verbatim from the scoping result):**

- **One-tick lagged rho feedback** - the cosmetic-lag form; disguised instantaneous feedback when rho_{t-1} ~= rho_t.
- **Dynamic centering against rho** - the committed construction fence holds; a proposed form not distinguishable from dynamic centering is inadmissible.
- **kappa modulation** - macro-conditioning the Rule C coupling coefficient is not an admissible locus.
- **Observable feedback** - Psi_meanI_state or Psi_persistence_I re-entering the rule is inadmissible; this also breaches the L4 fence.

**Derived exclusions (consequences of condition 2, not additions to the fence list):** because the Lambda-configuration locus on the becoming-active channel is the ONLY admissible route, macro-conditioning of survival (s_Lambda or any survival term) and macro-conditioning of any turnover hazard (theta_turnover or analogues) are excluded - whether direct (a macro term in the survival or turnover expression) or indirect (conditioned effective Lambda propagating into a Lambda-parameterized survival or turnover term, per condition 2). These follow from the only-clause; they are stated here so no implementation reads silence as latitude.

## 2. Macro signal and canonical lag construction (fixed)

The canonical Rule E lag is the **non-overlapping 25-tick block-lag**:

- Macro activation density is averaged over a completed prior 25-tick block (block m-1).
- The resulting macro signal conditions the locally-configured Lambda on the becoming-active channel (Section 1, condition 2).
- That signal is held fixed over the next 25-tick local-update block (block m).
- No same-block, same-tick, or one-tick-lag rho feedback of any kind.

**Block averaging is load-bearing for admissibility, not optional.** A point-lagged rho(t - L) is too close to the prohibited one-tick form and too sensitive to single-tick noise; it is NOT the canonical Rule E form and is not authorized by this contract.

## 3. Admissibility basis (recorded; measured, not asserted)

- **Lower bound (anti-circularity): cleared with measured margin.** Governing tau_rho = 1.66 ticks (pure-read diagnostic on the Rule C M2 kappa=0 L=0.40 trajectories; worst case across estimators and all five seeds; diagnostic retained at cycle3/wave_two/tau_rho_diagnostic.py). A 25-tick block averages over ~15 autocorrelation times, so the prior-block mean is a target-block-separated summary (Section 1, condition 1) for the next block's update.
- **Upper bound: cadence-permits-variation, NOT a length ceiling.** The upper-bound failure mode is observational equivalence to a fixed-Lambda run - a macro channel that is admissible but inert. The conditioning signal must be able to vary and act within the observation structure. (Recording-alignment fact, not an admissibility bound: a 100-tick SS-001 observation window contains four 25-tick blocks, which is what makes block-resolved recording per Section 5 well defined against the inherited window structure.)
- **Honest scope bound (carried).** tau_rho = 1.66 is measured for the UN-conditioned local rule. Conditioned dynamics could in principle lengthen their own autocorrelation. The measurement sizes the block against the correct baseline (the un-conditioned rule) but does not certify that conditioned dynamics stay fast; the lag-dynamics guard (Section 5) is the run-time catch for a conditioned slow-down. This contract does NOT treat the lower-bound clearance as a certification of conditioned-dynamics behavior.

## 4. Separability (fixed)

The macro-conditioning coefficient (working name alpha; final symbol resolvable at implementation without changing this clause) must have an exact zero point:

**alpha = 0 recovers the un-conditioned local base rule EXACTLY** - by construction, and confirmed empirically before any conditioned setting is read (as kappa = 0 was confirmed to recover Lambda-only in Rule C M2).

alpha is a SUBSTRATE parameter. Neither alpha nor its zero point is an operationalization of the point(s) at which mu(rho) = 0, and no Rule E artifact (identifier, comment, column, prose) may frame it as one.

## 5. Lag-dynamics guard and block-resolved recording requirement (fixed)

With a 25-tick cadence, a 100-tick observation window spans four macro-conditioned phases. An apparent near-null window could therefore arise from temporal cancellation of signed subblocks, oscillation across blocks, or hysteresis, rather than from a genuine near-null regime. A near-null produced by lag dynamics is not a substantive multiscale regime, and the design must be able to tell the difference from the record alone.

Precision (Layer 2 amendment): **"artifact" here means artifact FOR RULE E CANDIDATE STATUS, not meaningless dynamics.** Oscillation, hysteresis, or temporal cancellation across macro blocks are real dynamical behaviors of the conditioned system and are recorded as such; the guard's classification governs candidate eligibility only. A window excluded by the guard is fenced from candidate status, not erased from the record.

**Recording requirement (binding on any Rule E run record):** block-resolved trajectories of

1. the macro block signal,
2. effective (conditioned) Lambda,
3. rho,
4. Psi_meanI_state_z,
5. Psi_persistence_I_z,
6. candidate flags by aligned observation window.

A candidate near-null window is read against its block-resolved record; if the within-window block structure shows signed subblocks cancelling, oscillation, or hysteresis, the window is classified as a lag-dynamics artifact for candidate-status purposes, not a candidate. The Steady_State_Candidate and Lifted_Activation_Candidate flags remain INDEPENDENT at every stage, and LowLow_Nondegenerate_Candidate remains an apparatus-level flag.

## 6. Contrastive success criterion (fixed; pessimistic-on-passing)

Candidate status for a substantive multiscale near-null requires ALL of:

1. **Separability at zero conditioning** (Section 4) confirmed empirically.
2. **Signed-regime reach**: the sweep demonstrably reaches signed structure at responsive conditioning strength, so any LowLow is not rule-forced by default.
3. **Near-null away from the unconditioned floor**: a substantive LowLow must appear at responsive conditioning strength, bracketed by signed regimes - not only in the weak-conditioning neighborhood of the un-conditioned rule (which would relocate the Rule C A-prime outcome rather than produce a new one).
4. **Lag-dynamics guard passed**: the block-resolved record (Section 5) excludes temporal cancellation, oscillation, and hysteresis as the source of the near-null.

Criteria 1-3 must each hold lifted and non-degenerate (rho lifted, no degeneracy flags) for the rows on which they are evaluated. Rule E will PRODUCE or FAIL TO PRODUCE under these criteria. No Rule E outcome confirms the theory by construction; a scoped negative rests the arc without closing the mechanism class unless an endpoint is reached and recorded as such.

## 7. Named opens (resolution required before any seeding; resolution does not itself seed)

1. **Conditioning function h**: the exact functional form by which the macro block signal conditions locally-configured Lambda (locus and sign conventions per Sections 1-2; form not yet fixed).
2. **alpha range and grid density**: bounds and spacing for the conditioning-strength sweep; final grid is NOT specified by this contract.
3. **Base rule**: which un-conditioned local base Rule E layers onto (the alpha = 0 recovery target of Section 4).
4. **Lambda anchors**: whether the first pass runs one anchor or more.
5. **Reserved audits**: whether any reserved audits are promoted into the Rule E first pass.
6. **Run length / block count**: whether the inherited SS-001 structure suffices for lag-dynamics resolution at the 25-tick cadence, or a longer record (more blocks) is required for the Section 5 guard to discriminate.

## 8. What this contract does not do

- It does not seed a probe.
- It does not specify a final alpha grid.
- It does not authorize Layer 3 implementation.
- It does not alter any rested arc (Rule C M2 on A-prime; Comparator 0; Comparator epsilon; Rule D R3), any cleared gate, or the locked topology.
- It does not touch the L4 ontological question, which rides forward unsettled; the observable-feedback exclusion (Section 1) protects it.

Rule E advances from scoped admissibility to a committed design contract. No probe is seeded. The purpose of this contract is to define a macro-conditioned local-interaction mechanism that can later produce or fail to produce under fixed contrastive criteria.

- Layer 1 (Claude), Layer 2-concurred with amendments; Mike arbitrates commitment
