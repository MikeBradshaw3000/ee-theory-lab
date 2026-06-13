# Operations log - 2026-06-12 (c) - Rule E opens 1-5 resolved

**Session date:** 2026-06-12 (third session of the day)
**HEAD at session start:** df06646 (ops log: Rule E realizability consultation + amendment)
**HEAD at session end:** 65a7265 (Rule E opens 1-5 resolved)
**Layer 1:** Claude. **Execution channel:** Mike.

## What this session did

1. **Spec request reframed to a resolution round (fork surfaced, not folded).** Mike asked for the implementation spec. Layer 1 surfaced that a runnable spec cannot be drafted without first resolving opens 1-3 (base rule, conditioning function h, alpha grid), and that resolving them is its own routed step, not something to encode silently into a spec skeleton's slot structure. Fork put to Mike: skeleton-now (S) vs resolution-round-first (R). Mike (and Layer 2 independently) chose R. No skeleton was drafted.

2. **GitHub access note routed to Layer 2 (prior-session draft).** Layer 2 tested direct fetch and reported it non-functional this session (cache/fetch errors on repo page, raw URL, and API endpoint); Layer 2 correctly declined to claim direct read and asked for pasted/uploaded canonical content - exactly the fallback the access note specifies. Consequence for this session: the opens memo was routed to Layer 2 as a self-contained combined file (routing header + memo + full canonical contract text at 2f3ce0e, 27058 bytes) so review was against canonical text, not carried state.

3. **Opens-resolution memo drafted with two architectural considerations as its core**, then arbitrated by Layer 2 with Mike's concurrence:
   - Consideration (I): scalar macro conditioning over a spatially uniform base cannot create spatial structure - drove rejection of a Lambda-only base (3A) as failing signed-regime reach by construction.
   - Consideration (II): the baseline block signal barely varies (block-to-block sd ~0.004 at the anchor), so conditioning risks acting only through a DC component - the upper-bound inert-channel failure - shaping the open-1 and open-2 candidates so DC and fluctuating components are separable in the record.

4. **Resolutions of record (opens 1-5; open 6 was already resolved at 2f3ce0e):**
   - **Open 3 = Rule C M2 base at fixed kappa, BOTH signs, c = +/-0.35, Lambda = 0.40.** Not a kappa sweep - two fixed signed base regimes. 0.35 over 0.20 (cleaner signed anchor, clear of the floor-adjacent band, Rule D R3 matched-coupling precedent); both signs over one (Rule C/D sign-asymmetry findings make a one-sign screen too easy to overread). 3A and 3C rejected for the first pass.
   - **Criterion-3 = precision restatement, not amendment (Layer 2-ruled).** Under a signed base, alpha=0 recovers the signed baseline, not the Lambda-only floor; candidate near-null must occur away from the alpha=0 baseline and be bracketed along the alpha axis. Principle: not inherited from zero-conditioning baseline, not absence of coupling, not temporal cancellation, not degeneration.
   - **Open 1 = logit-additive with fixed standardized reference**, g_E(M) = (M - M_ref)/sigma_M, M_ref and sigma_M pre-registered from the un-conditioned base setting actually used (same Lambda, same kappa sign, topology, block structure), pooled across baseline seeds, never recomputed from running rho. Pooled-or-split (plus/minus) decided from the baseline measurement. Dynamic-centering fence satisfied (constant fixed before run). F3 bypass binds regardless of form. 1A-i / 1B / 1C rejected with reasons.
   - **Open 2 = realized effective-Lambda displacement tiers {0, +/-0.0125, +/-0.025, +/-0.05, +/-0.10} per baseline block-sigma, both signs, five seeds; alpha computed by LOGIT INVERSION, not linear division (Layer 2 correction, accepted).** The draft's linear-space alpha~12.5 illustration was superseded. 0.10 tier is a degeneracy probe, not the center. Per-block record adds realized M, g_E(M), p_Lambda_eff on top of the Section 5 six-item minimum.
   - **Inert-channel guard (Layer 2 addition, accepted, binding):** a candidate cannot rest on an inert macro channel; if effective Lambda is effectively constant over the candidate window and observationally equivalent to fixed-Lambda, it is not a Rule E candidate without a separate fixed-Lambda audit. Operates alongside the lag-dynamics guard.
   - **Opens 4-5 (severable, accepted now): Lambda = 0.40 only; no reserved audits promoted.**

5. **Pre-spec tau_rho-at-base verification requirement added (Layer 1, pessimistic-on-passing).** Resolving open 3 to a COUPLED base partially un-grounds the lag-realizability premise as measured: tau_rho = 1.66 was measured on kappa=0 trajectories, but the resolved un-conditioned baselines are c = +/-0.35, whose autocorrelation is unmeasured. Distinct from the contract's honest-scope bound (which concerns CONDITIONED dynamics, caught at run time) - here the design premise itself now refers to an unmeasured object. Requirement: re-run the pure-read tau_rho diagnostic (unchanged) on the existing committed Rule C M2 c = +/-0.35, L0.4 NPZs before the spec finalizes the block premise; if the coupled-base tau_rho compresses the 25-tick margin, the block-length premise returns to Layer 2 with the measurement before any spec. Pure read of committed data; seeds nothing. This addition is new relative to Layer 2's arbitration; Mike concurred to commit it with the memo (in-lane for Layer 1: it enforces an existing committed premise rather than adding a criterion); Layer 2 sees it when the committed memo next routes.

6. **Committed and pushed.** Memo placed at cycle3/wave_two/rule_e/RULE_E_OPENS_RESOLUTION.md (10277 bytes; single Downloads copy, exact size; byte-verified at destination 10277 / 23 20 52 / 74 0A). Explicit pathspec staged; one file verified; committed 65a7265; pushed df06646..65a7265 main -> main. (One re-send needed when a verification command pasted to console instead of executing; resolved by re-sending alone.)

## Decisions of record

- Rule E opens 1-5 RESOLVED and canonical at 65a7265 (RULE_E_OPENS_RESOLUTION.md). With open 6 (2f3ce0e), all named opens are resolved. The contract's pre-seeding requirements are complete EXCEPT (a) the pre-spec tau_rho-at-base verification, (b) the implementation spec, (c) seeding (Mike's separate call).
- The runnable implementation spec is the next artifact; it must honor this memo, the contract, the F3 bypass, the Layer 3 Q1 recording structure (separate per-run block CSV), and the Q5 leak-surface variable-space separations.
- Layer 2 direct GitHub fetch non-functional this session; canonical content must be pasted/uploaded to Layer 2 until fetch works. The access note remains valid for when it does.
- All rested arcs, cleared gates, locked topology, L4 fence unchanged. Rule E remains NOT seeded.

## State at session end

HEAD 65a7265, origin current. Anchor (RESUME_2026-05-30.md) is now THREE Rule E states stale (says "no contract"; predates the contract, the Section 5 amendment + open-6 resolution, and now the opens 1-5 resolution); refresh increasingly worthwhile but deferred to Mike's call - this log plus the committed contract and resolution memo govern. Untracked read_obs001_nearnull_scale.py remains at root. Next eligible moves, all Mike's call: anchor refresh (recommended - three-state drift); the pre-spec tau_rho-at-base verification (pure read, routed through Mike); implementation-spec drafting (after the tau_rho verification clears the block premise). Nothing is pending.

Drafting partner: Layer 1 (Claude).
