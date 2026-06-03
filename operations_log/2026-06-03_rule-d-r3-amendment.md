# Operations log — 2026-06-03 Rule D amended to R3 (retain Lambda-survival)

**Session:** Cycle 3 wave two. Rule D was carried from opens-resolution through Layer 3 implementation, where the implementation surfaced a structural defect in the contract-specified mechanism (theta_turnover = 0 saturates, leaving the matched-coupling bracket without a signed lower anchor). The mechanism was amended to R3 — retain Rule C's neighbor-independent Lambda-survival, apply theta_turnover as an ADDITIONAL independent churn hazard on top (net persistence s_Lambda * (1 - theta_turnover)) — on Layer 2's recommendation and Mike's arbitration. Contract, resolution memo, and anchor all corrected and committed.
**Layer:** Layer 1 (Claude) routing/drafting/amendment; Layer 3 (Gemini) implementation and the catch; Layer 2 (ChatGPT) mean-field diagnosis and R3 recommendation; Mike sole execution channel, arbiter (ruled R3 in), and router.
**Opened from:** HEAD 7c7a58c (anchor refresh, opens resolved).
**Closed at:** HEAD e3c67e6, origin current after push.
**Outcome:** Rule D mechanism amended to R3 across all canonical artifacts (contract 2d2e281, resolution memo 0b09866, anchor e3c67e6); Layer 3 R3 implementation execution-ready; the run is the next step. Three R3 commits plus this ops log.

---

## Sequence

The L3 routing note (carrying the full Rule D contract) went to Gemini, which had no prior Rule D context. L3 implemented and surfaced three flags before baking in: a window-structure discrepancy, the survival-replacement consequence, and a downstream-delta-computation note. Layer 1 dispositioned all three, routed a PERMUTATIONS scope question and a theta = 0 sanity-confirmation back to L3, and on L3's theta = 0 confirmation recognized a structural problem reaching the mechanism. That went to Layer 2, which diagnosed it and recommended R3. Mike ruled R3 in (no replacement-form version). Layer 1 amended the contract (six edits), regenerated the resolution memo, re-routed L3 for the R3 code, verified L3's s_Lambda and kappa confirmations, and refreshed the anchor. All committed root-first.

## The catch (Layer 3)

L3's theta = 0 sanity confirmation, requested by Layer 1, reported that under the contract-specified rule (active-cell persistence = 1 - theta_turnover, Lambda-survival removed) theta_turnover = 0 makes active cells absorbing: no 1->0 transition, rho rises monotonically toward saturation. That is correct code behavior, and it exposed that theta_turnover = 0 was NOT the signed lower anchor the success criterion (contract Section 4) requires — it was the saturation-degenerate endpoint. The matched-coupling bracket needs a signed lifted-non-degenerate lower end; the as-specified rule did not provide one at theta = 0, and possibly nowhere on the theta axis.

## Two Layer 1 errors (recorded substantively, not glossed)

Both errors share one root: an unexamined assumption that "Rule D at low turnover behaves like Rule C," which the survival-replacement made false.

1. WINDOW STRUCTURE. The L3 routing note stated "5 windows of 25 ticks, 125 ticks/run." This was wrong: the window STEP is 25, the window LENGTH is 100, runs are 200 ticks. The error came from reading the M2 CSV's window_start step (0/25/50/75/100) as the window length when slicing the targeted CSV read during D-1 design. L3 caught it against the hardcoded WINDOW_LENGTH = 100 in the SS-001 apparatus and implemented the true structure to preserve parity. The wrong figure had propagated into the resolution memo and the anchor; both are now corrected.

2. theta = 0 AS "PURE-RULE-C SIGNED REFERENCE." The resolution memo (84e4cd9) described theta_turnover = 0 as the pure-Rule-C signed reference / matched lower anchor. Under the survival-replacement form this was wrong: theta = 0 removed all death and saturated the lattice, the opposite of a signed reference. Same root assumption as the window error. R3 makes the description true (theta = 0 now recovers Rule C exactly), but the memo as first placed asserted it under a rule where it did not hold.

Neither error reached a run — both were caught before execution: error 1 by L3, error 2 by the theta = 0 confirmation Layer 1 requested and then by L2. The catches worked because the confirmations were requested rather than assumed. That is the lesson worth keeping: the theta = 0 sanity-confirmation was the probe that surfaced the second error, and it was only requested because L3's flags had already shown the first.

## Layer 2 diagnosis and R3 recommendation

Layer 2 read the as-specified rule against its own contract-stage density mean-field rho_{t+1} = (1 - theta) rho_t + (1 - rho_t) b_kappa(rho_t), confirming saturation at theta = 0 (death term vanishes). It ruled R2 (no possible signed regime) too strong — for theta > 0 the replacement rule can have an interior non-saturated equilibrium — but noted density mean-field does not guarantee a SIGNED observable regime, so any nonzero-theta anchor under the replacement rule would have to be produced, not inherited (R1-prime). Layer 2 recommended R3 as the cleaner canonical correction: retain Rule C's neighbor-independent Lambda-survival, apply theta_turnover as an additional independent hazard, so theta = 0 recovers Rule C's known signed regime. Layer 2 confirmed R3 does NOT collapse toward Rule B: Lambda-survival is neighbor-INDEPENDENT (flat per-cell), whereas Rule B's pathology was neighbor-CONDITIONED survival; a flat survival probability times an independent turnover hazard is not that. Mike arbitrated R3 in and ruled out keeping the replacement form. No new Layer 2 pass on the amended contract was required — Layer 2's recommendation supplied the mechanism and the persistence form directly.

## Contract amendment and cascade

Contract (RULE_D_DESIGN_CONTRACT.md) amended via six targeted literal replacements: Section 2.2 mechanism (retain s_Lambda, net persistence s_Lambda*(1-theta), theta=0 = Rule C reference, formal s_Lambda definition), Section 2.3 fence prose + formula (Bernoulli(s_Lambda*(1-theta_turnover))), Section 6 Rule B distinction (L2's neighbor-independence argument), Section 8 effective-persistence metric, status header (records the post-placement R3 amendment). Byte-state verified (no BOM, single LF, no CRLF, 15008 -> 16880); diff confirmed six regions, no incidental change; Sections 1/4/5 scanned and confirmed consistent with R3 (no surviving replacement-form language). Commit 2d2e281.

Resolution memo (D_OPENS_RESOLUTION.md) regenerated wholesale (the D-1 calibration logic inverts under R3: the theta ladder is an ADDITIONAL-churn ladder on top of s_Lambda, not a total-lifetime 1/theta ladder): R3 amendment note added, calibration table reframed as added-churn scales, window figure corrected to 200/100/25, theta=0 relabeled as Rule C reference, effective-persistence diagnostic added. Overwrote the tracked file (size 7645 -> 10196, verified at destination by size against the stale earlier copy). Commit 0b09866.

L3 re-route for the R3 code: L3 confirmed s_Lambda from M2 primary source (M2's staying-active line was rand_grid < p_Lambda, so s_Lambda = 0.40 at Lambda = 0.40, parity-faithful, sourced from the validated M2 code not from Layer 1) and that theta = 0 now recovers Rule C and no longer saturates. Layer 1 independently verified the kappa constant: calculate_realized_delta_p(0.40, +/-0.7599) = +/-0.35000 exactly (pessimistic-on-passing applied to L3's constant, not just trusted). Outstanding non-blocking note: theta = 0 reproduces M2's signed REGIME (same rule, same coupling, distributionally) but not bit-identical M2 CSV rows, because the two scripts consume the RNG stream differently — to be flagged so non-matching theta = 0 rows are not mistaken for a bug.

Anchor (RESUME_2026-05-30.md) refreshed: Rule D paragraph and horizon line carry R3 framing, run as next step, window/calibration corrections. Three R3-content edits applied (one direct, two via a helper script to avoid PowerShell paste-limit hangs on long replacement strings — the helper read old/new text from file rather than the paste channel; execution-policy bypass used for the unsigned helper, no system policy change). Byte-state verified (25864 -> 26521). Commit e3c67e6.

## State at close

- HEAD e3c67e6, origin current after push, tree otherwise clean (untracked read_obs001_nearnull_scale.py at root unchanged; transient helper apply_anchor_r3_edits.ps1 sits in Downloads, not the repo).
- Rule D mechanism is R3 across all canonical artifacts: active-cell persistence s_Lambda * (1 - theta_turnover), retaining Rule C's neighbor-independent Lambda-survival with theta_turnover as an additional independent churn hazard. theta_turnover = 0 recovers Rule C exactly.
- Grid unchanged by R3: theta_turnover {0,0.02,0.05,0.10,0.20,0.35,0.50}; c = +/-0.35 matched pair both signs; Lambda = 0.40; seeds 42/137/256/1024/31415; true window structure 200 ticks / 100-tick windows / step 25.
- Layer 3 R3 implementation (c3_w2_rule_d_r3.py) execution-ready: s_Lambda = 0.40, PERMUTATIONS = 199, kappa = +/-0.7599 verified, parity checks and fences intact, s_Lambda + effective_persistence added to output schema. NOT seeded.
- Next step: the RUN (Mike's call to execute), then read the output against the Section 4 matched-coupling bracket and the two guards; then seeding is Mike's call. Filename suffix _r3 retained on script and output CSV (honest about the amendment history; pre-R3 form was never run or committed) — final naming is Mike's call when reading the run.
- Rule C first pass still rests on A-prime; Comparator 0 / epsilon floor findings unchanged; weak-form Rule B prior untouched; L4 ontological question rides forward unsettled.

Drafting partner: Layer 1 (Claude).
