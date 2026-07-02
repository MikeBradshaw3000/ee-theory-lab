# Rule E bounded-gain (modified Candidate A) implementation spec - non-seeding

**Status: IMPLEMENTATION SPEC. NON-SEEDING. Drafted by Layer 1 from the committed bounded-gain design resolution; Layer 2-reviewed 2026-06-27 (accept with precision amendments, all incorporated); Mike arbitrates commitment and build authorization.** This spec operationalizes the bounded-gain design resolution (modified Candidate A: smooth tier-specific bounded realized conditioning term) into a buildable specification. On Mike's arbitration it authorizes Layer 3 to BUILD to it for a subsequent build review; it does NOT seed a run. Seeding remains Mike's separate call after the build is reviewed. L2 review confirmed the cond_term_j = Delta_j*tanh(g_E) operationalization as the intended modified-A form (no separate gain parameter in the first bounded pass), corrected the one-sigma prose (Delta_j is the saturation cap / nominal scale, not an exactly realized one-sigma displacement), set the saturated-channel thresholds (per-block bound_active at bound_ratio >= 0.90; window-level saturated-channel at >= 3/4 blocks; 2/4 mixed), and required the d=0 division-by-zero guard. **Amended 2026-07-01 (Mike-arbitrated): Section 5 grid count corrected from the predeclared 90 to the as-built 50 (own-direction tiers per base sign, first-pass parity); cross-direction extension named-not-triggered. See Section 5.**

Governing documents: cycle3/wave_two/rule_e/RULE_E_BOUNDED_GAIN_RESOLUTION.md (the construction resolution; governs this spec's conditioning form and diagnostics), RULE_E_DESIGN_CONTRACT.md (contract; governs admissibility and recording), RULE_E_OPENS_RESOLUTION.md (opens; governs block/window/run structure and the alpha-tier construction), RULE_E_FIRST_PASS_FINDINGS.md (the scoped-negative result this construction responds to), operations_log/2026-06-12b (F3 constraint). This spec deliberately mirrors the first-pass RULE_E_IMPLEMENTATION_SPEC.md structure and changes ONLY the conditioning term (Section 1), the alpha/bound construction (Section 5), and the recording and classification additions the bounded construction requires (Sections 3, 6). On any discrepancy, the governing documents govern over this spec; this spec governs the build.

---

## 0. Apparatus this layers onto (unchanged from the first pass)

GRID_SIZE=50, Moore-radius-1 toroidal, N_CELLS=2500. Rule C M2 step: q = active-neighbor-count/8; p_become = sigma(logit(p_Lambda) + kappa*(2q-1)); rand_grid = np.random.rand(50,50) drawn ONCE per tick; become_active = (grid==0) & (rand_grid < p_become); stay_active = (grid==1) & (rand_grid < p_Lambda); next = become_active | stay_active. Survival uses bare p_Lambda and the SAME rand_grid draw. Observables per window: Psi_meanI_state = mean over window ticks of per-tick Moran's I; Psi_persistence_I = Moran's I of the time-averaged grid; z via compute_meanI_state_null / compute_persistence_null. Constants: LOW_Z_THRESH=2.0, LIFTED_THRESHOLD=0.05, VAR_EPSILON=1e-3, TARGET_RHO_INIT=0.10. This is identical to the first-pass apparatus; the bounded construction changes only how the becoming-active logit is conditioned.

## 1. The Rule E bounded step (the only mechanism change from the first pass)

For tick t in conditioning block m, base sign s (= sign of kappa), target tier d_j with per-tier logit displacement Delta_j (Section 5):

    M_m         = mean activation density over the COMPLETED PRIOR block (m-1), scalar, fixed across all 25 ticks of block m
    g_E(M_m)    = (M_m - M_ref_s) / sigma_M_s
    cond_term_j = Delta_j * tanh( g_E(M_m) )              # SMOOTH TIER-SPECIFIC BOUNDED REALIZED TERM
    logit_eff   = logit(p_Lambda) + cond_term_j
    p_become_eff = sigma( logit_eff + kappa*(2q - 1) )

**The bounded term (the modified-A construction, from the resolution).** The first pass used the UNBOUNDED term cond_term = alpha_j * g_E, where alpha_j was the per-tier logit increment from logit inversion. Under railing, alpha_j * g_E reached +/-100 logits. Modified-A replaces it with a smooth saturating term whose magnitude cannot exceed the tier's own logit displacement Delta_j:

    cond_term_j = Delta_j * tanh( g_E(M_m) )

so |cond_term_j| < |Delta_j| for all M_m, saturating smoothly as g_E grows. At |g_E| = 1 (one baseline block-sigma of macro movement) the realized term is Delta_j * tanh(1) ~= 0.762 * Delta_j - approximately 76% of the cap, NOT approximately the full cap. Thus **Delta_j is the tier-specific saturation cap and nominal displacement scale, not an exactly realized one-sigma displacement in the bounded construction.** Near g_E = 0 the response is approximately linear with slope Delta_j (tanh(x) ~ x), preserving responsiveness in the near-zero regime; at large |g_E| it approaches the tier-specific cap smoothly. The bound is TIER-SPECIFIC: each tier saturates at its OWN Delta_j, so the tier distinction is preserved under saturation - which is the whole point of the resolution's correction of the global-d_max form (a single global bound would let small tiers saturate to the same maximum as large tiers, reproducing the first-pass identical-tiers pathology in bounded form).

**Construction note (binding on the build): alpha_j and Delta_j are the SAME logit-inversion quantity; do not reintroduce a second alpha factor.** Under modified-A the tier's target displacement Delta_j is both the saturation bound AND the scale of the argument. The argument of tanh is g_E ALONE (unit-standardized macro movement), NOT alpha_j * g_E / Delta_j with a separately carried alpha_j - because alpha_j = Delta_j, the ratio alpha_j/Delta_j = 1 and the argument reduces to g_E. Writing it as Delta_j * tanh(alpha_j * g_E / Delta_j) with alpha_j = Delta_j is mathematically identical but invites a build error if alpha_j is sourced from a different table than Delta_j; the canonical form for the build is cond_term_j = Delta_j * tanh(g_E), with Delta_j the per-tier logit displacement from Section 5.

Survival is UNCHANGED and UN-CONDITIONED:

    stay_active = (grid==1) & (rand_grid < p_Lambda)      # bare p_Lambda; never p_become_eff, never a conditioned effective-Lambda

**Leak-surface discipline (contract Section 1.2, binding; unchanged from first pass).** The conditioning adds the bounded cond_term_j INSIDE the becoming-active logit only. No single shared Lambda variable is updated and passed to both transitions; the survival line reads bare p_Lambda. No "effective p_Lambda" object is formed that the stay_active line could read. Rule C separates these two lines; the bounded construction preserves that separation exactly as the first pass did.

**F3 bit-exact bypass (ops log 2026-06-12b, binding; unchanged).** When d_j == 0 (the alpha=0 / Delta_j=0 tier) the step calls the un-conditioned Rule C path by BRANCH - cond_term is bypassed, not computed as Delta_j*tanh(g_E) with Delta_j=0 - so the becoming-active logit is byte-identical to Rule C and the rand_grid draw order is preserved. (Delta_0 = 0 would make tanh give exactly 0, but the branch is retained for bit-exactness and rand-draw-order guarantees, matching the first-pass build.) The build verifies d=0 recovery against a Rule C reference run at matched (Lambda, kappa, seed) before any conditioned setting is read, exactly as verify_f3_bypass did in the first pass.

## 2. Block / window / run structure (unchanged from the first pass)

- **Block cadence:** non-overlapping 25-tick conditioning blocks. M_m = mean rho over block m-1.
- **First block:** M_0 = M_ref_s, giving zero standardized macro signal in block 0 (g_E=0, so cond_term_0 = Delta_j*tanh(0) = 0 - a neutral bootstrap); the completed-prior-block rule is active from block 1 onward.
- **Conditioning runs THROUGHOUT, including burn-in.** The burn-in settles the CONDITIONED bounded dynamics; d=0 runs are un-conditioned throughout by the F3 bypass and serve as the recovery reference and the constant-measurement baseline.
- **Run length:** TICKS_PER_RUN = 400 = 100-tick burn-in + 300 post-burn-in ticks = 12 post-burn-in conditioning blocks exactly (open-6 minimum). No preemptive margin; an ambiguous block record motivates a NAMED extension, not a heavier first pass.
- **Observation windows:** WINDOW_LENGTH=100, WINDOW_STEP=25 (inherited SS-001). 13 windows at w_start = 0,25,...,300; candidate-eligible windows are post-burn-in (w_start >= 100). Window-level z and flags computed exactly as Rule C M2 (100-tick null; unchanged).

## 3. Recording layout (first-pass layout + the resolution's additional diagnostics)

TWO outputs per run, as in the first pass; the block-level CSV gains the bounded-construction diagnostics the resolution requires.

1. **Window-level CSV** (unchanged from first pass) - one row per observation window: Psi_meanI_state, Psi_meanI_state_z, Psi_persistence_I, Psi_persistence_I_z, SS flags, degeneracy flags, LowLow_Nondegenerate_Candidate, mean_rho, plus Rule E identifiers (target tier d, Delta_j, kappa, base sign s, seed). z-scores and candidate flags live ONLY here (100-tick null). One addition: a window-level saturated_channel_flag (Section 6).

2. **Block-level CSV** (first-pass columns + bounded diagnostics) - one row per 25-tick block: run_id, block_idx, M_block (the signal conditioning THIS block = prior-block mean), g_E_value, realized_block_rho, raw_Psi_meanI_state_block, raw_Psi_persistence_I_block, AND the bounded-construction additions required by the resolution:
   - **pre_bound_term** = Delta_j * g_E(M_m) = the COUNTERFACTUAL unbounded same-tier term the first pass would have applied (alpha_j * g_E under alpha_j=Delta_j). Recorded so the read can verify whether this bounded pass WOULD have railed under the first-pass form - the direct repair-verification diagnostic.
   - **post_bound_term** = cond_term_j = Delta_j * tanh(g_E(M_m)) = the term actually applied.
   - **Delta_j** = the tier's logit displacement = the per-tier saturation cap / nominal scale for this run.
   - **bound_ratio** = |post_bound_term| / |Delta_j|. For the d=0 tier, bound_ratio = 0 (or NA) by definition - the F3 bypass branch computes no conditioning arithmetic, so Delta_j=0 never enters a denominator. (Build hygiene, L2-required: the d=0 branch must not evaluate |post_bound_term|/|Delta_j| = 0/0; it sets bound_ratio and bound_active directly.)
   - **bound_active** (per-block, L2-set) = True when bound_ratio >= 0.90, i.e. the post-bound term reaches at least 90% of that tier's cap (equivalently |g_E| >= atanh(0.90) ~= 1.472). For d=0, bound_active = False by definition. Recorded per block so the read computes bound-activation frequency over each window.

   Additionally, at the WINDOW level (recorded on the window-level CSV, Section 6): **bound_active_count_in_window** (integer 0-4, the count of the window's four constituent 25-tick blocks with bound_active=True) and **bound_active_fraction_in_window** (that count / 4). A setting-level summary is also reported in the read: the post-burn-in bound_active fraction across all 12 post-burn-in blocks (a setting with >= 0.75 post-burn-in bound-active is described as globally saturated, though candidate classification remains window-level).

   Block observables remain RAW: no z-scores, no block-level LowLow flag (contract Section 5). This CSV is the lag-dynamics-guard, inert-channel-guard, AND saturated-channel-guard instrument.

NPZ state output retained as in the first pass (per-run full state array). run_id aligns across window CSV, block CSV, and NPZ. Filename token and run_id format are Layer 3's at build (reported as "what the build produces"); the block CSV run_id must join to the window CSV and NPZ.

## 4. Pre-registered constants (unchanged from the first pass; already measured)

M_ref_plus, sigma_M_plus  - from the un-conditioned (d=0) c=+0.35, L0.4 baseline.
M_ref_minus, sigma_M_minus - from the un-conditioned (d=0) c=-0.35, L0.4 baseline.

The first pass measured these at block scale on the alpha=0 baseline: M_ref_plus=0.3714 / sigma_M_plus=0.0025; M_ref_minus=0.4187 / sigma_M_minus=0.0017. **The bounded construction uses the SAME split pre-registered constants** - modified-A does NOT change the denominator of g_E (that is Candidates B/C, not selected); it bounds the realized term. sigma_M_s remains the BLOCK-to-block standard deviation of the 25-tick mean rho, M_ref_s the block-mean, measured at 25-tick block scale on the d=0 baseline, pooled across the five seeds, FIXED before any conditioned setting is read, never recomputed from running rho (dynamic-centering fence). The build re-measures them by the same procedure and verifies against these values (they are the verification reference, not a hard-coded input, so the measurement path stays the source of truth).

**Ill-conditioned guard (unchanged, binding):** if sigma_M_s < 1e-6 for either sign the build HALTS and reports an ill-conditioned macro channel. (Not expected; sigma_M_minus ~0.0017 is small but well clear of the guard. Note the bounded construction is FAR more tolerant of small sigma_M than the first pass was: the small denominator still makes g_E large under conditioned excursion, but tanh saturates the realized term at Delta_j regardless of how large g_E grows - which is precisely the first-pass failure this construction repairs.)

## 5. The tier / bound construction (open 2 + the resolution's tier-specific bound)

Target realized effective-Lambda probability displacement tiers, |d| in {0, 0.0125, 0.025, 0.05, 0.10}, both signs, via LOGIT INVERSION at p_Lambda = 0.40. The per-tier logit displacement Delta_j is exactly the first pass's alpha_j (same quantity, same formula):

    Delta_+(d) = logit(p_Lambda + d) - logit(p_Lambda)
    Delta_-(d) = logit(p_Lambda - d) - logit(p_Lambda)

**Worked values at p_Lambda = 0.40 (logit(0.40) = -0.4055), identical to the first-pass table:**

    d=0.0125 -> Delta+ = +0.0518   Delta- = -0.0524
    d=0.025  -> Delta+ = +0.1032   Delta- = -0.1054
    d=0.05   -> Delta+ = +0.2048   Delta- = -0.2136
    d=0.10   -> Delta+ = +0.4055   Delta- = -0.4418
    d=0      -> Delta = 0 exactly (F3 bypass branch)

Values are NOT sign-symmetric (nonlinear logit scale around p=0.40). The build recomputes them from the formula; this table is the verification reference.

**The bound.** Delta_j is used TWO ways in the bounded construction, both from this single quantity: (1) as the saturation CAP - the realized term cannot exceed |Delta_j|; (2) as the nominal displacement SCALE - the argument of tanh is g_E (unit-standardized), so cond_term_j = Delta_j*tanh(g_E) is approximately linear with slope Delta_j near zero, reaches ~0.762*Delta_j at |g_E|=1, and approaches the cap Delta_j smoothly beyond. Delta_j is therefore the cap and nominal scale, NOT an exactly realized one-sigma displacement. There is NO separate alpha table and NO second division; Section 1's construction note is binding here.

Grid: 50 runs = 5 tiers (d=0 plus the 4 own-direction displacement tiers per base sign) x 2 base signs (c=+/-0.35) x 5 seeds - matching the first-pass grid AS BUILT AND AS RUN exactly (the committed first-pass findings record "50 runs = 5 d-tiers x 5 seeds x 2 signs"). **Grid-count correction (2026-07-01, Mike-arbitrated):** this spec as L2-reviewed stated "9 tiers x 2 signs x 5 seeds = 90 runs" - a predeclared line that NEITHER pass's build matched: both the first pass and the bounded build sweep each base sign across its OWN-direction displacement tiers only (positive base with positive displacements, negative with negative), yielding 50. The divergence traces to the first pass, was carried into this spec by inheritance, and was missed twice in L1 review; it surfaced at the bounded seed. Arbitration: the 50-run as-built form IS the instrument - first-pass parity ("same grid, only the term bounded") is literal only at 50, and the classification logic (sign-local reach; bracketing along the tier axis) was written for the own-direction ladder. The 0.10 tier remains the degeneracy probe, not the evidentiary center. **Cross-direction extension - NAMED, NOT TRIGGERED:** the 40 cross-direction cells (positive base with negative-displacement tiers and vice versa) remain AVAILABLE as a separately named instrument, but are NOT scoped by this spec - what a cross-direction cell tests, and how sign-local bracketing reads across mixed directions, requires a design resolution before any such cell is run. Opening it is Mike's call only. (The first pass's byte-identical negative tiers arose because the unbounded term railed; under the bound, tiers that previously railed to identical extinction/oscillation should now separate, because each saturates at its own Delta_j - whether they do is part of what the run tests.)

## 6. Classification logic (first-pass criteria + the saturated-channel guard)

A post-burn-in window is a substantive multiscale near-null CANDIDATE only if ALL hold (criteria 1-5 unchanged from the first pass, sign-local):

1. **d=0 separability** confirmed (d=0 runs reproduce the signed Rule C baseline at each sign) - a once-checked precondition, not per-window.
2. **Signed-regime reach** (sign-local): across the tier sweep AT THE SAME BASE SIGN, window observables demonstrably reach signed (non-near-null) structure at responsive tiers.
3. **Near-null away from the d=0 baseline** (criterion-3 restatement): the window is jointly near-null (both |z| < 2.0), lifted, non-degenerate, at a responsive nonzero tier, bracketed along the tier axis by non-near-null regimes - not the trivial d=0 neighborhood.
4. **Lag-dynamics guard passed:** the window's 4-block raw-Psi record does not show the near-null arising from signed-subblock cancellation, oscillation, or hysteresis.
5. **Inert-channel guard passed:** effective Lambda is not effectively constant over the window (block CSV shows g_E actually varied); an observationally-fixed-Lambda window is not a candidate without a separate fixed-Lambda audit.

**6. Saturated-channel guard (NEW; the resolution's addition, L2-set threshold, binding).** A candidate window is classified as SATURATED-CHANNEL, not clean-responsive, if at least 3 of its 4 constituent 25-tick blocks have bound_active=True (bound_active_count_in_window >= 3). Such a window does not satisfy clean Rule E candidate status without a separately opened saturated-channel audit. The intermediate case 2/4 is recorded as BOUND-INVOLVED / MIXED - not automatically rejected, but explicitly reported in the read (a yellow flag, especially if a candidate appears there); 0/4 or 1/4 is eligible for a clean-responsive reading if all other guards pass. Rationale (resolution Section 3): a bound active in nearly all blocks means the channel is operating at its rail, the bounded analogue of the first-pass over-drive; a near-null produced under a near-always-active bound has not demonstrated RESPONSIVE conditioning. This guard sits ALONGSIDE guards 4 and 5 and does NOT replace the lag-dynamics guard - a window can be BOTH saturated and oscillatory, and if EITHER guard rejects it, it is not a clean candidate. Guard 5 (inert-channel) catches a channel that never moved; guard 6 (saturated-channel) catches a channel pinned at its rail - opposite failure modes of "responsive conditioning." The bounded construction fixes runaway AMPLITUDE (guard against the first-pass fault); it does not by itself guarantee clean responsive conditioning (guard 6 is what determines whether the bounded channel is responsive or mostly railed).

**Sign-locality (binding, unchanged):** candidate classification, signed-regime reach, and bracketing are evaluated SIGN-LOCALLY, each candidate against its own base-sign sweep and its own split constants. Reach from one base sign NEVER rescues or brackets a candidate in the other.

LowLow_Nondegenerate_Candidate fires at the WINDOW level exactly as in Rule C M2 (apparatus-level flag); guards 4-6 are additional Rule E classification filters applied in the read, recorded, never renamed Regime_II.

## 7. Build-level latitude (reported back as "what the build produces", not design)

Filename token form; module/function factoring; block-CSV column dtypes and run_id format; whether block observables compute in-loop or from the saved NPZ post-run (either acceptable if values match Section 3). None is a mechanism choice. The tanh construction, the tier-specific bound (each tier capped at its own Delta_j), the split constants, the F3 branch bypass, the block-active threshold (bound_ratio >= 0.90) and window-level saturated-channel threshold (>= 3/4 blocks) now SET by L2, the diagnostic definitions (Section 3), and the six-guard classification are NOT latitude - they are the design.

## 8. What this spec does not do

Does not seed a run. On Layer 2 acceptance and Mike's arbitration it authorizes a Layer 3 BUILD for subsequent build review, not a run. Does not alter any rested arc, gate, the locked topology, or the L4 fence. Does not move the first-pass scoped-negative finding, which stands. The runnable build, once reviewed, is seeded only at Mike's separate call.

- Layer 1 (Claude); Layer 2-reviewed with precision amendments incorporated; Mike arbitrates commitment, build authorization, and seeding
