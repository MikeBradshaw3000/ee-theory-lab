# Rule E (lagged-Lambda conditioning) - scoping result

**Status: SCOPING RESULT. NON-SEEDING. Lag realizability CLEARED (measured).** This memo records the result of a non-seeding scoping conferral on a macro-conditioned local-interaction mechanism (Rule E, lagged-Lambda conditioning), and a follow-on lag-specification round whose realizability question is now resolved by a pure-read measurement. It does NOT seed a probe, does NOT place a design contract, and does NOT authorize a grid, script, or run. It records an architecture-level admissibility boundary, a canonical lag construction, and places Rule E as a named-not-triggered follow-up. Mike arbitrates whether anything proceeds past this scoping result.

Layer 2-concurred (scoping conferral and lag-specification round, this session).

---

## The mechanism in scope

Rule E (lagged-Lambda conditioning): a mechanism in which a slow, block-lagged macro activation-density signal conditions the locally-configured Lambda each cell sees. The motivating intuition is multiscale - the aggregate conditioning the local rather than the local merely aggregating to a passive macro readout. This would be the first wave-two-adjacent mechanism to let a macro signal act back on the local update; Rules C and D are purely local (neighbor-coupled, churn-limited), with rho an emergent readout that never re-enters the rule.

## Result: conditionally admissible, narrowly

**Rule E is conditionally admissible as a slow block-lagged Lambda-configuration mechanism.** Two conditions, both binding:

1. **Slow / block-lagged.** The lag must satisfy a separation of timescales: the macro signal conditioning the local update must be slow enough relative to the becoming-active update to constitute a genuinely exogenous conditioning input, not a disguised reading of the rule's own current output. This places Rule E on the legitimate macro-to-local channel - the slow, Q-like channel of the theory's hard core - rather than the prohibited fast rho-on-its-own-rule channel.
2. **Lambda-configuration locus only.** The macro signal may condition only the locally-configured Lambda. This is the sole architecture-admissible channel: the only route through which macro state reaches agents is Lambda-as-locally-configured.

## Inadmissible forms (named and fenced)

Rule E is NOT admissible as any of the following:

- **One-tick lagged rho feedback** - the cosmetic-lag form. A one-tick lag in a system whose macro state is near-constant tick-to-tick (rho_{t-1} ~= rho_t) is disguised instantaneous feedback and breaches the no-hidden-feedback fence.
- **Dynamic centering against rho** - already prohibited by the committed construction fences; the fence holds. "Lagged rho conditions the local Lambda configuration" does NOT get to collapse into dynamic centering; if a proposed form is not distinguishable from dynamic centering, it is inadmissible.
- **kappa modulation** - macro-conditioning the Rule C coupling coefficient is not an admissible locus.
- **Observable feedback** - Psi_meanI_state or Psi_persistence_I re-entering the rule is inadmissible. (This also breaches the L4 fence: the observables are not operationalizations of theoretical Psi, and routing them back into the rule would smuggle that resolution.)

So Rule E routes ONLY through slow block-lagged Lambda-configuration - never through survival, the coupling coefficient, or the observables.

## Contrastive success criterion (carried, with one added guard)

The wave-two contrastive structure carries intact:
- **Separability** at zero conditioning strength: the macro-conditioning coefficient swept to zero must recover the un-conditioned local rule (as kappa=0 recovered Lambda-only in Rule C).
- **Signed-regime reach**: the sweep must demonstrably reach signed structure at responsive conditioning strength, so any LowLow is not rule-forced by default.
- **Near-null away from the unconditioned floor**: a substantive multiscale LowLow must appear AWAY from the un-conditioned floor - present at responsive conditioning strength, bracketed by signed regimes - not only in the weak-conditioning neighborhood of the un-conditioned rule (which would relocate the Rule C A-prime outcome).

**Added guard (new to the multiscale case):** the criterion must guard against lag-induced artifacts - oscillation, hysteresis, and temporal cancellation - that could produce an apparent near-null that is neither rule-forced nor substantive-multiscale but an artifact of the lag dynamics themselves. A near-null produced by temporal cancellation or oscillatory averaging is not a substantive multiscale regime.

---

## LAG REALIZABILITY - CLEARED (measured, this session)

The conditional-admissibility result above REQUIRES a separation of timescales but did not, on its own, show one is REALIZABLE under the locked topology and the existing window structure. A follow-on lag-specification round (Layer 2-concurred) tested realizability before any contract is built on it. Result: **realizability clears, with a measured macro autocorrelation time.**

**The two-bound squeeze.** The lag length L_lag (or block-averaging length) is bounded below by anti-circularity (L_lag must exceed the macro autocorrelation time tau_rho, or the conditioning signal is effectively the current tick - the prohibited form) and bounded above by observability. The upper bound is NOT a raw length ceiling below the SS window (a signal held across a full window can still act): the correct upper-bound failure is observational equivalence to a fixed-Lambda run - if the macro signal varies too slowly relative to the observation structure, the macro channel is admissible but INERT. The upper bound is therefore a cadence-permits-variation condition, not a length ceiling. (This corrects the lag-conferral memo's original "shorter than the SS window" framing.)

**Measured tau_rho.** A pure-read diagnostic (no grid, no Rule E mechanism, nothing seeded) on the existing Rule C M2 kappa=0 L=0.40 state trajectories - kappa=0 is the un-conditioned local rule at the working anchor by construction - estimated tau_rho on the settled tail (100-tick burn-in discarded from the 200-tick runs; integrated-autocorrelation and e-folding estimators; worst-case across both estimators and all five seeds taken as governing). Result: **governing tau_rho = 1.66 ticks.** rho sits at ~0.40 with per-tick sd ~0.010; three of five seeds show NEGATIVE lag-1 autocorrelation (anti-persistent, overshoot-and-correct), consistent with the strongly-contracting local dynamics and confirming there is no slow mode for a lag to read. (Source NPZ: c3_w2_rule_c_m2_states_L0.4_kp0_0000_s*.npz; diagnostic is a pure read, committed as a tool only if Mike wants it retained.)

**Canonical lag construction (Layer 2-resolved).** A **non-overlapping 25-tick block-lag**: macro density is averaged over a completed prior 25-tick block, the resulting macro signal conditions the locally-configured Lambda, and that signal is held fixed over the next 25-tick local-update block. At tau_rho = 1.66, a 25-tick block averages over ~15 autocorrelation times, so the prior-block mean is a genuinely exogenous summary for the next block's update - the anti-circularity lower bound is cleared with large margin, quantitatively, not by assertion. A 100-tick observation window contains four such blocks: enough for the conditioning to vary and act without collapsing to one constant offset (clears the upper bound). **Block averaging is load-bearing for admissibility, not optional**; a point-lagged rho(t - L) is too close to the prohibited one-tick form and too sensitive to single-tick noise, and is NOT the canonical Rule E form.

**Scope of the clearance (honest bound).** tau_rho = 1.66 is measured for the UN-conditioned local rule. A Rule E mechanism that conditions Lambda on lagged rho could in principle lengthen its own autocorrelation (feedback can slow relaxation). This measurement therefore clears the lower bound AS THE DESIGN PREMISE - it sizes the block against the un-conditioned baseline, which is the correct object for setting block length - but does not by itself certify that the CONDITIONED dynamics stay fast enough. The lag-dynamics guard (below) is what would catch a conditioned slow-down at run time.

**Lag-dynamics guard becomes a recording requirement.** With a 25-tick cadence a 100-tick window spans four macro-conditioned phases, so a near-null window could arise from temporal cancellation of signed subblocks rather than from a genuine near-null regime. This does not make the lag inadmissible; it means any Rule E contract/run record must carry block-resolved trajectories - macro block signal, effective Lambda, rho, Psi_meanI_state_z, Psi_persistence_I_z, and candidate flags by aligned observation window - so that a candidate near-null can be distinguished from oscillation, hysteresis, or temporal cancellation.

## Status and placement

- Rule E (lagged-Lambda conditioning) is a **named-not-triggered follow-up**. Admissible-under-condition with lag realizability now CLEARED and a canonical 25-tick block-lag construction named; still NOT seeded. No grid, no contract, no run.
- No seeding follows from this scoping result. Opening it is Mike's call, and would require placing a design contract that honors the two admissibility conditions, the canonical lag construction, the contrastive criterion, and the block-resolved recording requirement above.
- The cleared gates, the rested arcs (Rule C M2 on A-prime, Comparator epsilon, Rule D R3), and the existing named-not-triggered follow-ups are all unchanged.
- The L4 ontological question rides forward unsettled; the observable-feedback exclusion above protects it.

- Layer 1 (Claude), Layer 2-concurred
