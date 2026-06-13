# Operations log - 2026-06-12 (d) - Rule E implementation spec (L2-reviewed, build-ready)

**Session date:** 2026-06-12 (fourth session of the day)
**HEAD at session start:** 056b195 (anchor refresh to 4bf8aa0)
**HEAD at session end:** 59b4bd6 (Rule E implementation spec)
**Layer 1:** Claude. **Execution channel:** Mike.

## What this session did

1. **Layer-involvement timing assessed (Mike's question).** Several commits had accumulated since the last layer contact. Layer 1's read: most decisions since carried prior L2 review/arbitration; the genuinely unreviewed items were narrow (the tau_rho-at-base 2.86 result, the split-M_ref consequence). Layer 1 declined to route a standalone tau_rho backfill as unnecessary (pure-read confirmation of an existing premise) but held firm that the implementation spec must get L2 review BEFORE any build/seed - the same gate that caught the Rule D saturation bug. Mike concurred; deferred to Layer 1 on necessity, and Layer 1 pushed back on the part that was not necessary rather than accepting the deference wholesale.

2. **Primary-source reads before drafting (no reconstruction).** Layer 1 read the committed Rule C M2 script (c3_w2_rule_c_m2.py): step_rule_c (becoming-active + survival on shared rand_grid, survival on bare p_Lambda), the kappa filename token ({kappa:+.4f}, m/p/_; c=0.35 -> kp0_7599/km0_7599 - decoded from KAPPA_CONSTANTS_0_40, not inferred), the observable computation (Psi_meanI_state = mean per-tick Moran's I; Psi_persistence_I = Moran's I of the time-averaged grid), and the constants (TICKS_PER_RUN=200, WINDOW_LENGTH=100, WINDOW_STEP=25, LOW_Z_THRESH=2.0, etc.). These pinned the spec exactly.

3. **Spec drafted and routed to L2 as a self-contained packet** (L2 GitHub fetch still down): Part A folded in the unseen tau_rho-at-base 2.86 result; Part B was the implementation spec. Seven questions put to L2.

4. **L2 review: accept with one required correction + two precisions, all incorporated.**
   - **Required correction (build-blocking): the worked alpha table.** The draft's worked logit-increment values at p_Lambda=0.40 were wrong (Layer 1 had mis-paired signs / rounded loosely; the linear-space alpha~12.5 had already been superseded, but the replacement table was also wrong). Layer 1 INDEPENDENTLY RECOMPUTED rather than banking L2's table: logit(0.40)=-0.4055; d=0.0125 -> +0.0518/-0.0524; d=0.025 -> +0.1032/-0.1054; d=0.05 -> +0.2048/-0.2136; d=0.10 -> +0.4055/-0.4418. Independent compute matched L2 exactly - verified, not deferred. Values are sign-asymmetric (logit nonlinear at p=0.40). Layer 1's draft table was the error; owned in the spec text.
   - **Burn-in fork (L2-ruled): conditioning runs THROUGHOUT, including burn-in; M_0 = M_ref_s.** Burn-in settles the conditioned dynamics; switching on at tick 100 would create a transition artifact. M_0=M_ref_s is a neutral zero-signal bootstrap for the first block.
   - **Run length (L2-ruled): TICKS_PER_RUN=400** (100 burn-in + 300 post-burn-in = 12 post-burn-in blocks, the open-6 minimum). No preemptive margin; ambiguity in a candidate's block record would motivate a named extension.
   - **sigma_M scale (L2-confirmed, binding): the 25-tick BLOCK-to-block SD, not the per-tick rho sd (~0.010).** Measured at block scale on the alpha=0 baseline, split by sign, before any conditioned run.
   - **Sign-local classification (L2 precision, binding):** candidate classification, signed-regime reach, and bracketing evaluated sign-locally; reach from one base sign never rescues a candidate in the other.
   - **Ill-conditioned-sigma_M halt guard (L2 addition, build hygiene):** build halts and reports if sigma_M_s is near-zero for either sign, rather than producing enormous standardized g_E.

5. **Part A concurrence:** L2 concurred the 2.86 coupled-base tau_rho leaves the 25-tick block premise intact; no return for block-length redesign; canonical 25-tick block carries.

6. **Canonical spec committed.** Corrected alpha table, four forks resolved as decisions, two precisions incorporated, status upgraded to build-ready (authorizes a Layer 3 BUILD for subsequent build review; NOT a seed). Placed at cycle3/wave_two/rule_e/RULE_E_IMPLEMENTATION_SPEC.md (11073 bytes; byte-verified 11073 / 23 20 52 / 67 0A). Committed 59b4bd6; pushed 056b195..59b4bd6 main -> main.

## Decisions of record

- Rule E implementation spec CANONICAL at 59b4bd6. Build-ready: authorizes Layer 3 to build to it for a subsequent build review. NOT a seed; seeding remains Mike's separate call after the build is reviewed.
- The spec governs the build; the contract (2f3ce0e), opens resolution (65a7265), and F3 constraint (ops 2026-06-12b) govern over the spec on any discrepancy.
- Conditioning runs through burn-in; M_0=M_ref_s; TICKS_PER_RUN=400; 90 runs (9 alpha x 2 signs x 5 seeds); two CSV outputs (window-level unchanged + block-level raw, joined on run_id); split per-sign pre-registered constants measured at block scale on the alpha=0 baseline; five sign-local candidate conditions + lag-dynamics and inert-channel guards.
- tau_rho-at-base 2.86: L2-concurred, block premise intact (closes the unreviewed-result loop from 4bf8aa0).
- All rested arcs, gates, locked topology, L4 fence unchanged. Rule E NOT seeded.

## Process notes

- Download channel intermittently failed to deliver again (empty Get-ChildItem -> Set-Clipboard null error on the canonical-named pull); cleared by re-presenting under a fresh transit name (RULE_E_IMPL_SPEC_056b195.md), same md5, then copying to the canonical name. Same workaround as the anchor refresh earlier today.
- Alpha-table error caught by L2 and independently re-derived by Layer 1 (pessimistic-on-passing applied symmetrically: did not bank L2's numbers without recompute).
- Spec built from primary-source reads of the committed Rule C M2 script, not from memory.

## State at session end

HEAD 59b4bd6, origin current. Anchor (RESUME_2026-05-30.md, refreshed at 056b195) is now one state stale: it lists the implementation spec as the "natural next artifact" on the horizon, whereas the spec now EXISTS and is build-ready at 59b4bd6. Minor staleness (horizon item realized); refresh deferred to Mike's call - this log and the committed spec govern. Untracked read_obs001_nearnull_scale.py remains at root. Next eligible moves, all Mike's call: route the spec to Layer 3 to BUILD (framed as "what the build will produce"; returns through Layer 1 for build review, then Mike arbitrates seeding); anchor refresh; or rest. Seeding is gated behind the build review. Nothing is pending.

Drafting partner: Layer 1 (Claude).
