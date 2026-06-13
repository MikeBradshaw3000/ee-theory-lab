# Rule E implementation spec - L2-reviewed, build-ready (non-seeding)

**Status: IMPLEMENTATION SPEC. NON-SEEDING. Layer 2-reviewed 2026-06-12 (accept with one required correction + two precisions, all incorporated); Mike-arbitrated.** This spec operationalizes the committed Rule E design (contract 2f3ce0e + opens resolution 65a7265 + coupled-base tau_rho verification 4bf8aa0) into a buildable specification. It authorizes Layer 3 to BUILD to it for a subsequent build review; it does NOT seed a run. Seeding remains Mike's separate call after the build is reviewed.

Governing documents: cycle3/wave_two/rule_e/RULE_E_DESIGN_CONTRACT.md (contract), RULE_E_OPENS_RESOLUTION.md (opens), operations_log/2026-06-12b (F3 constraint). On any discrepancy, those govern over this spec; this spec governs the build.

---

## 0. Apparatus this layers onto (confirmed from c3_w2_rule_c_m2.py)

GRID_SIZE=50, Moore-radius-1 toroidal, N_CELLS=2500. Rule C M2 step: q = active-neighbor-count/8; p_become = sigma(logit(p_Lambda) + kappa*(2q-1)); rand_grid = np.random.rand(50,50) drawn ONCE per tick; become_active = (grid==0) & (rand_grid < p_become); stay_active = (grid==1) & (rand_grid < p_Lambda); next = become_active | stay_active. Survival uses bare p_Lambda and the SAME rand_grid draw. Observables per window: Psi_meanI_state = mean over window ticks of per-tick Moran's I (batch_morans_i_toroidal_8 then mean); Psi_persistence_I = Moran's I of the time-averaged grid (mean over ticks, then calculate_morans_i_toroidal_8); z via compute_meanI_state_null / compute_persistence_null. Constants: LOW_Z_THRESH=2.0, LIFTED_THRESHOLD=0.05, VAR_EPSILON=1e-3, TARGET_RHO_INIT=0.10.

## 1. The Rule E step (conditioning implementation)

For tick t in conditioning block m, base sign s (= sign of kappa):

    M_m        = mean activation density over the COMPLETED PRIOR block (m-1), scalar, fixed across all 25 ticks of block m
    g_E(M_m)   = (M_m - M_ref_s) / sigma_M_s
    logit_eff  = logit(p_Lambda) + alpha * g_E(M_m)
    p_become_eff = sigma( logit_eff + kappa*(2q - 1) )

Survival is UNCHANGED and UN-CONDITIONED:

    stay_active = (grid==1) & (rand_grid < p_Lambda)      # bare p_Lambda; never p_become_eff, never an effective-Lambda

**Leak-surface discipline (L3 Q5, binding).** The conditioning adds the alpha*g_E term INSIDE the becoming-active logit only. No single shared Lambda variable is updated and passed to both transitions; the survival line reads bare p_Lambda. No "effective p_Lambda" object is formed that the stay_active line could read. The Rule C step already separates these two lines; Rule E preserves that separation.

**F3 bit-exact bypass (ops log 2026-06-12b, binding).** When alpha == 0.0 the step calls the un-conditioned Rule C path - the alpha*g_E term is bypassed by branch, not multiplied by zero - so the becoming-active logit is byte-identical to Rule C and the rand_grid draw order is preserved. The build verifies alpha=0 recovery against a Rule C reference run at matched (Lambda, kappa, seed) before any conditioned setting is read.

## 2. Block / window / run structure (open 6, resolved; forks L2-ruled)

- **Block cadence:** non-overlapping 25-tick conditioning blocks. M_m = mean rho over block m-1.
- **First block (L2-ruled):** M_0 = M_ref_s, giving zero standardized macro signal in block 0 (a neutral bootstrap, not an invented prior-block read); the completed-prior-block rule is active from block 1 onward. Preserves the block-lag fence without an initial shock.
- **Conditioning runs THROUGHOUT, including burn-in (L2-ruled).** The burn-in settles the CONDITIONED Rule E dynamics, not the un-conditioned baseline; switching conditioning on at tick 100 would create a transition artifact at the start of the candidate-eligible period. (alpha=0 runs are un-conditioned throughout by definition - the F3 bypass - and serve as the recovery reference and the constant-measurement baseline.)
- **Run length (L2-ruled):** TICKS_PER_RUN = 400 = 100-tick burn-in + 300 post-burn-in ticks = 12 post-burn-in conditioning blocks exactly (the open-6 resolved minimum). No preemptive margin; if a candidate's block record is ambiguous between drift/oscillation/hysteresis, that motivates a NAMED extension, not a heavier first pass.
- **Observation windows:** WINDOW_LENGTH=100, WINDOW_STEP=25 (inherited SS-001). At 400 ticks the loop yields windows at w_start = 0,25,...,300 (13 windows); candidate-eligible windows are the post-burn-in ones (w_start >= 100). Window-level z and flags computed exactly as Rule C M2 (100-tick null; unchanged).

## 3. Recording layout (contract Section 5 + L3 Q1, resolved)

TWO outputs per run:

1. **Window-level CSV** (existing Rule C M2 schema, unchanged) - one row per observation window: Psi_meanI_state, Psi_meanI_state_z, Psi_persistence_I, Psi_persistence_I_z, SS flags, degeneracy flags, LowLow_Nondegenerate_Candidate, mean_rho, plus Rule E identifiers (alpha, target tier d, kappa, base sign s, seed). z-scores and candidate flags live ONLY here (100-tick null).

2. **Block-level CSV** (new; separate per-run file, joined on run_id) - one row per 25-tick block: run_id, block_idx, M_block (the signal conditioning THIS block = prior-block mean), g_E_value, cond_logit_term (= alpha*g_E), realized_block_rho, raw_Psi_meanI_state_block (mean per-tick Moran's I over the 25 ticks), raw_Psi_persistence_I_block (Moran's I of the 25-tick-averaged grid). Block observables are RAW: no z-scores, no block-level LowLow flag (contract Section 5 amendment). This CSV is the lag-dynamics-guard and inert-channel-guard instrument; it must record enough to report within-window variation in g_E, alpha*g_E, and effective Lambda.

NPZ state output retained as in Rule C M2 (per-run full state array). Filename token extends the Rule C scheme with an alpha encoding; the run_id in the block CSV must align with the NPZ name. Exact token form is Layer 3's at build (reported as "what the build produces").

## 4. Pre-registered constants (split per sign; measured before any conditioned run)

M_ref_plus, sigma_M_plus  - from the un-conditioned (alpha=0) c=+0.35, L0.4 baseline.
M_ref_minus, sigma_M_minus - from the un-conditioned (alpha=0) c=-0.35, L0.4 baseline.

Split is required: the signed baselines differ materially in mean block density (~0.372 at c=+0.35 vs ~0.418 at c=-0.35; Part-A tau_rho-at-base measurement). Constants are measured from the alpha=0 baseline run (also the F3 recovery reference), FIXED before any conditioned setting is read, never recomputed from running rho (dynamic-centering fence).

**Measurement scale (L2-confirmed, binding):** sigma_M_s is the BLOCK-to-block standard deviation of the 25-tick mean rho, NOT the per-tick rho sd (~0.010). M_ref_s is the block-mean. Both measured at the 25-tick block scale on the alpha=0 baseline, pooled across the five seeds.

**Ill-conditioned guard (L2 addition, build hygiene):** if sigma_M_s is extremely small or zero for either sign, the build HALTS and reports an ill-conditioned macro channel rather than silently producing enormous standardized g_E values. Not expected from the reported baseline; the guard belongs in implementation.

## 5. The alpha grid (open 2, resolved; corrected arithmetic)

Target realized effective-Lambda probability displacement tiers per one baseline block-sigma of macro movement, |d| in {0, 0.0125, 0.025, 0.05, 0.10}, both signs, via LOGIT INVERSION:

    alpha_+(d) = logit(p_Lambda + d) - logit(p_Lambda)
    alpha_-(d) = logit(p_Lambda - d) - logit(p_Lambda)

Because g_E is standardized to unit baseline block-sigma, these logit increments ARE the alpha values directly - NO second division by sigma_M (sigma_M is already inside g_E).

**Worked values at p_Lambda = 0.40 (logit(0.40) = -0.4055), L2-corrected and independently recomputed by Layer 1:**

    d=0.0125 -> alpha+ = +0.0518   alpha- = -0.0524
    d=0.025  -> alpha+ = +0.1032   alpha- = -0.1054
    d=0.05   -> alpha+ = +0.2048   alpha- = -0.2136
    d=0.10   -> alpha+ = +0.4055   alpha- = -0.4418
    d=0      -> alpha = 0 exactly (F3 bypass)

Values are NOT sign-symmetric (the logit scale is nonlinear around p=0.40). The build recomputes them from the formula; this table is the verification reference. (The earlier draft's linear-space table - alpha~12.5 - was wrong and is superseded; this corrects it.)

Grid: 9 alpha values (0, +/-4 tiers) x 2 base signs (c=+/-0.35) x 5 seeds = 90 runs. The 0.10 tier is the degeneracy probe, not the evidentiary center.

## 6. Classification logic (contract Section 6 + guards; sign-local)

A post-burn-in window is a substantive multiscale near-null CANDIDATE only if ALL hold:

1. **alpha=0 separability** confirmed (alpha=0 runs reproduce the signed Rule C baseline at each sign) - a once-checked precondition, not per-window.
2. **Signed-regime reach** (sign-local): across the alpha sweep AT THE SAME BASE SIGN, window observables demonstrably reach signed (non-near-null) structure at responsive alpha.
3. **Near-null away from the alpha=0 baseline** (criterion-3 restatement): the window is jointly near-null (both |z| < 2.0), lifted, non-degenerate, at responsive nonzero alpha, bracketed along the alpha axis by non-near-null regimes - not the trivial alpha=0 neighborhood.
4. **Lag-dynamics guard passed:** the window's 4-block raw-Psi record (block CSV) does not show the near-null arising from signed-subblock cancellation, oscillation, or hysteresis.
5. **Inert-channel guard passed:** effective Lambda is not effectively constant over the window (block CSV shows g_E actually varied); an observationally-fixed-Lambda window is not a Rule E candidate without a separate fixed-Lambda audit.

**Sign-locality (L2 precision, binding):** candidate classification, signed-regime reach, and bracketing are evaluated SIGN-LOCALLY. A candidate at c=+0.35 is evaluated against the c=+0.35 sweep and its own split constants; a candidate at c=-0.35 against the c=-0.35 sweep and its own constants. Reach from one base sign NEVER rescues or brackets a candidate in the other. The split constants already imply this; it is stated explicitly here.

LowLow_Nondegenerate_Candidate fires at the WINDOW level exactly as in Rule C M2 (apparatus-level flag); guards 4-5 are additional Rule E classification filters applied in the read, recorded, never renamed Regime_II.

## 7. Build-level latitude (reported back as "what the build produces", not design)

Filename token form for alpha; module/function factoring; block-CSV column dtypes and run_id format; whether block observables compute in-loop or from the saved NPZ post-run (either acceptable if values match Section 3). None is a mechanism choice.

## 8. What this spec does not do

Does not seed a run. Authorizes a Layer 3 BUILD for subsequent build review, not a run. Does not alter any rested arc, gate, the locked topology, or the L4 fence. The runnable build, once reviewed, is seeded only at Mike's separate call.

- Layer 1 (Claude); Layer 2-reviewed with corrections incorporated; Mike arbitrates commitment and seeding
