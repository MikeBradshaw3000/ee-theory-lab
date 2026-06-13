# Rule E opens resolution - opens 1-5 resolved (non-seeding)

**Status: OPENS RESOLUTION. NON-SEEDING. Layer 2-arbitrated, Mike-concurred, 2026-06-12.** This memo records the resolution of the Rule E design contract's named opens 1-5. It seeds nothing, fixes no final run script, and authorizes no Layer 3 implementation. The runnable implementation spec is the next artifact; it must honor this memo, the contract, the F3 alpha-zero bypass constraint (operations_log/2026-06-12b), the Layer 3 Q1 recording structure, and the Q5 leak-surface separations. Seeding remains Mike's separate call after the spec exists.

Governing documents: cycle3/wave_two/rule_e/RULE_E_DESIGN_CONTRACT.md (canonical at 2f3ce0e; open 6 resolved there); cycle3/wave_two/RULE_E_SCOPING_RESULT.md (admissibility rationale). This memo resolves opens 1-5; on any discrepancy about admissibility, the scoping result and contract govern.

---

## Open 3 - base rule: RESOLVED to Rule C M2 base at fixed kappa, both signs, |c| = 0.35

Rule E layers onto the committed Rule C M2 form: p_become = sigma(logit(p_Lambda_eff) + kappa*(2q - 1)), g(q) = 2q - 1 fixed centered; survival = neighbor-independent s_Lambda computed from the UN-conditioned base Lambda (the contract's no-leak clause).

- kappa is FIXED, not swept: two pre-registered signed base settings, realized contrast c = +0.35 and c = -0.35, both at Lambda = 0.40. This is not a kappa sweep; it is two fixed signed base regimes for the same Rule E macro-conditioning question.
- Why 0.35, not 0.20: |c| = 0.20 is the first responsive setting just outside the Rule C floor-adjacent band; a near-null there risks blurring into base-coupling-near-the-boundary. |c| = 0.35 is a clean signed anchor - responsive, not an endpoint, well clear of the near-zero band - and matches the Rule D R3 matched-coupling precedent.
- Why both signs: Rule C and Rule D both showed the two observable axes can behave differently by sign; a one-sign first pass is too easy to overread.
- Rejected: 3A (Lambda-only base) - scalar macro conditioning over a spatially uniform Lambda-only base remains conditionally i.i.d. across cells; signed-regime reach would fail by construction, not by meaningful test. 3C (kappa as a second swept axis) - conflates the rested Rule C map with the Rule E question; named as a possible second pass only.

**Criterion-3 precision restatement (Layer 2-ruled: precision, not amendment).** Under a Rule C M2 base with responsive nonzero kappa, alpha = 0 recovers the un-conditioned SIGNED local-rule baseline, not the Lambda-only floor. A Rule E near-null candidate must therefore occur away from the alpha = 0 baseline neighborhood, at responsive nonzero macro conditioning, and must be bracketed along the alpha axis by non-near-null signed regimes. The principle carried: not inherited from the zero-conditioning baseline; not produced by absence of coupling; not temporal cancellation; not degeneration. The contract's criterion-3 phrase "away from the unconditioned floor" is read, for this base, as "away from the alpha = 0 baseline"; this preserves the contract's intent without reopening it.

## Open 1 - conditioning function h: RESOLVED to logit-additive with fixed standardized reference

Canonical form: logit(p_Lambda_eff) = logit(p_Lambda) + alpha * g_E(M), with

g_E(M) = (M - M_ref) / sigma_M

where M is the completed prior-block (25-tick) mean activation density, and M_ref and sigma_M are PRE-REGISTERED CONSTANTS measured from the un-conditioned baseline record and fixed before any conditioned Rule E run. alpha is thereby a logit-scale effect per one baseline block-sigma of macro-density movement.

Pre-registration discipline (binding):
- M_ref and sigma_M are measured from the un-conditioned base setting ACTUALLY USED: same Lambda (0.40), same kappa sign, same topology, same block structure. Pooled across the predeclared baseline seeds; never chosen per seed; never recomputed inside conditioned runs.
- Because the first pass uses both signs at c = +/-0.35: one pooled (M_ref, sigma_M) pair if the two signed un-conditioned baselines have practically identical block means and sigmas, or separate pre-registered constants (M_ref_plus, sigma_M_plus) and (M_ref_minus, sigma_M_minus) if they differ materially. The choice is made from the baseline measurement, recorded in the spec, before any conditioned run.
- Fence note (Layer 2-concurred): a constant reference fixed before the run from un-conditioned data does NOT violate the dynamic-centering fence; it does not track running rho. Any updating of M_ref or sigma_M from running rho would be dynamic centering and is inadmissible.
- The F3 constraint binds regardless of form: at implementation, alpha == 0 bypasses the conditioning arithmetic entirely and calls the un-conditioned update path; exact recovery verified at build/runtime parity.

Rejected: 1A-i (g_E = 2M - 1) - carries a ~-0.2 standing DC component at the working anchor, conflating static Lambda shift with fluctuation response. 1B (linear-additive with clipping) - the additive-clip form is deliberately the Comparator-epsilon signature; reusing it for a mechanism blurs a committed design distinction. 1C (multiplicative) - no committed precedent; asymmetric around the anchor.

## Open 2 - alpha range and grid density: RESOLVED to realized-displacement tiers via logit inversion

Construction rule (resolved; final numbers instantiated in the spec from the pre-registered baseline measurements):

- Target tiers are realized effective-Lambda PROBABILITY displacements per one baseline block-sigma of macro movement: |d| in {0 (alpha = 0 exactly), 0.0125, 0.025, 0.05, 0.10}, BOTH signs of alpha, five seeds (42 / 137 / 256 / 1024 / 31415).
- **Logit inversion is REQUIRED (Layer 2 correction, accepted):** because the conditioning is logit-additive, alpha constants are computed as logit increments, not linear division. For target probability displacement d from baseline p_Lambda, with the standardized g_E: alpha_plus(d) = logit(p_Lambda + d) - logit(p_Lambda) and alpha_minus(d) = logit(p_Lambda - d) - logit(p_Lambda) (each the logit displacement for a one-sigma macro move). The draft memo's linear-space illustration (alpha ~ 12.5 for the 0.05 tier over unscaled M - M_ref) was linear-probability-space arithmetic and is superseded; with the standardized transform, alpha values are the logit increments directly.
- The 0.10 tier is a boundary / degeneracy probe, not the evidentiary center (committed discipline carried).
- The run record must store, per block: realized M, g_E(M), p_Lambda_eff, alongside the contract Section 5 six-item minimum; and the read must classify whether the macro channel was live, effectively static, saturated, oscillatory, or degenerate over each candidate window. (Additions to, not replacements of, the Section 5 minimum.)

**Inert-channel guard (Layer 2 addition, accepted; binding on candidate classification):** a candidate cannot rest on an inert macro channel. If effective Lambda is effectively constant over the candidate window and observationally equivalent to a fixed-Lambda run, the result is not a Rule E macro-conditioning candidate without a separate fixed-Lambda audit. This guard follows from the named inert-channel risk and operates alongside the lag-dynamics guard.

## Open 4 - Lambda anchors: RESOLVED to Lambda = 0.40 only

First pass at Lambda = 0.40 only - the anchor where lag realizability and tau_rho are grounded and where the Rule C / Rule D baselines are densest. No 0.20, 0.30, or 0.50 anchor promoted. The second anchor is a named extension, not part of the first pass; the density-specific-structure question is deferred, not dropped.

## Open 5 - reserved audits: RESOLVED to none promoted

No reserved audits promoted into the Rule E first pass. The bounded-linear reserved audit and the Lambda = 0.30 / 0.50 reserved audits remain reserved.

---

## Pre-spec verification requirement: tau_rho at the resolved base (Layer 1 addition, pessimistic-on-passing)

Resolving open 3 to a COUPLED base partially un-grounds the lag-realizability premise as measured: governing tau_rho = 1.66 was measured on the kappa = 0, Lambda = 0.40 trajectories, whereas the resolved un-conditioned (alpha = 0) baselines are c = +/-0.35 at Lambda = 0.40, whose autocorrelation time is UNMEASURED. Coupled dynamics could relax more slowly than the uncoupled rule, and the 25-tick block length was sized against the kappa = 0 measurement. This is distinct from the contract's honest-scope bound (CONDITIONED dynamics, caught by the run-time lag-dynamics guard): here the design premise itself - block length cleared against the un-conditioned baseline - now refers to an unmeasured object.

**Requirement (binding before the implementation spec finalizes the block premise):** re-run the pure-read tau_rho diagnostic (cycle3/wave_two/tau_rho_diagnostic.py, unchanged) on the existing committed Rule C M2 state NPZs at c = +0.35 and c = -0.35, Lambda = 0.40 (all five seeds; settled tail; same estimators; worst case governing). This is a pure read of committed data - no grid, no mechanism, nothing seeded.
- If the governing coupled-base tau_rho still leaves the 25-tick block a comfortable multiple of the autocorrelation time, the canonical block carries unchanged and the measured value is recorded in the spec.
- If it does not (the coupled base relaxes slowly enough to compress the margin), the block-length premise returns to Layer 2 with the measurement before any spec is drafted - the canonical 25-tick block is NOT silently assumed adequate for the coupled base.

## What this resolution does and does not do

Opens 1-5 are resolved (open 6 was resolved at 2f3ce0e). The contract's pre-seeding requirements are complete EXCEPT: (a) the pre-spec tau_rho verification above; (b) the implementation spec itself; (c) the act of seeding, which remains Mike's separate call. Nothing here seeds a probe, runs a script (the tau_rho verification is a read of committed data and is itself routed through Mike), or authorizes implementation. All rested arcs, cleared gates, the locked topology, and the L4 fence are unchanged.

- Layer 1 (Claude); Layer 2-arbitrated with amendments; Mike-concurred; Mike arbitrates commitment
