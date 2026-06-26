# Operations log - 2026-06-12e - Rule E first pass: spec, build, seed, run, read, arbitration

**Session:** 2026-06-12 (fifth segment, slug 2026-06-12e)
**Layer 1:** Claude (architectural guardian, vocabulary enforcer, routing-note author)
**Execution channel:** Mike (sole; all PowerShell run by Mike, Claude drafts and routes)
**Layer 2:** ChatGPT (mean-field substantive review / arbitration)
**Layer 3:** Gemini (Mesa implementation; realizability / recording / substrate only)
**Entry HEAD:** 4bf8aa0 (Rule E design contract canonical, opens 1-6 resolved, tau_rho-at-base verified, NOT seeded)
**Exit HEAD:** ab51d36 (Rule E first-pass run committed: window CSV, block CSV, 50 state NPZs); result-recording bundle drafted, committed in the following segment
**Result:** Rule E first pass RESTS on a SCOPED NEGATIVE for the predeclared design; mechanism class NOT closed

## What this session did

Starting from the build-ready Rule E design state (contract canonical, opens 1-6 resolved, coupled-base lag premise verified at tau_rho=2.86), this session ran the full arc from implementation spec to an arbitrated result: spec review, build, build review, the seed, the run, the read, and Layer 2 arbitration.

## Spec -> Layer 2 review -> canonical spec (59b4bd6)

The implementation spec was drafted to honor the contract (2f3ce0e), the opens resolution (65a7265), the F3 alpha-zero bypass constraint, the Layer 3 Q1 recording structure (separate per-run block CSV joined on run_id), and the Q5 leak-surface variable-space separations. Layer 2 reviewed and accepted with corrections: the alpha table was corrected (realized-displacement tiers by logit inversion, not linear division); burn-in / M_0 / run-length forks were ruled; sign-local classification was fixed; sigma_M was placed at block scale. Corrections folded in; canonical spec committed at 59b4bd6.

## Layer 3 build -> Layer 1 build review -> revised build (build committed 3738157)

Layer 3 produced the build. Layer 1 build review returned three corrections: (1) F3 must verify against the committed Rule C M2 script, not a mock - a seed-blocking requirement, since an alpha=0 bypass that reproduces a mock proves nothing about parity with the real base; (2) run_id and NPZ filename tokens must be sanitized; (3) the conditioning logit term must be applied uniformly across tiers. Layer 3 revised. Layer 1 re-reviewed: corrections satisfied, bit-exactness of the alpha=0 path verified by walking the RNG streams rather than accepting the build's claim (sufficiency-tested-not-asserted). One residual import-path question (P-vs-V on the F3 import) was deferred; Mike chose P - self-catching at pre-flight rather than silent guard. Build script committed pre-run at 3738157.

## First run FAILED at F3 (path bug) -> one-line fix (3abf8dd)

The first run failed LOUDLY at F3 verification before any data was written - vindicating the P choice (pre-flight self-catch). The cause was NOT the deferred import-side-effect question; it was a simpler wrong-directory bug: sys.path pointed at cycle3, but c3_w2_rule_c_m2.py lives in cycle3/wave_two. Mike arbitrated A: Layer 1 patches the single line, shown transparently, because it is a filesystem path with exactly one correct value - not a mechanism choice that would require a re-spec. The one-line path fix was committed at 3abf8dd.

## The seed and the run -> outputs (ab51d36)

The re-run was the seed. It ran clean. F3 passed bit-exact across all seeds and both base signs over a full 400-tick trajectory. Split pre-registered constants were measured at block scale on the alpha=0 baseline: M_ref_plus=0.3714 / sigma_M_plus=0.0025; M_ref_minus=0.4187 / sigma_M_minus=0.0017. Outputs committed at ab51d36: window CSV, block CSV, and 50 state NPZs (5 d-tiers x 5 seeds x 2 base signs).

## The read -> Layer 2 synthesis -> arbitration -> result

The read was per-(setting, seed) on the window CSV and the block CSV, routed to Layer 2 for synthesis and arbitration. The arbitrated result: the Rule E first pass FAILS TO PRODUCE a substantive multiscale near-null under the locked topology and the predeclared first-pass design. It rests on a scoped negative; it does NOT close the Rule E mechanism class.

Two-sided outcome. Positive base (c=+0.35): conditioning drives extinction at all nonzero alpha tiers (block_rho ~0, extinction_degenerate) - degenerate, not candidate. Negative base (c=-0.35): window-level lifted near-null flags (mean_rho~0.326, LowLow_Nondegenerate_Candidate=True on ~all post-burn-in windows), BUT the block record shows a 25-tick-cadence saturate/extinct oscillation (block_rho rings ~0.02 <-> ~0.63; ~50% of post-burn-in blocks <0.05, ~50% >0.60; raw block meanI sign-alternates 5/5 runs). The window mean is the midpoint of a ring no tick is near. Rejected by the lag-dynamics guard as a temporal-cancellation artifact. The operative rejection is the guard, NOT a reach failure.

Failure mechanism: over-driven feedback, not inertness. sigma_M was measured un-conditioned (~0.0017); once conditioning perturbs rho, the standardized g_E divides the conditioned excursion by the tiny un-conditioned sigma_M, reaching +/-230, and the conditioning term reaches +/-100 logits against the intended |d|<=0.10 displacement. The feedback rails. This is the run-time realization of the contract's honest-scope bound (tau_rho did not certify conditioned dynamics), and the predeclared lag-dynamics guard was the catch. It caught it.

## Layer 1 error owned: the refuted inert-channel hypothesis

During the read, Layer 1 hypothesized from the window CSV that the macro channel was inert (effectively constant effective-Lambda, observationally equivalent to fixed-Lambda). The block CSV REFUTED this: the channel was not inert but over-driven, ringing violently at the block cadence. The hypothesis was wrong and is recorded as wrong. This is pessimistic-on-passing applied to Layer 1's own read, not only to probes - and the block-resolved instrument, not Layer 1's first reading, is what caught it. The block-resolved recording requirement (contract Section 5) is strongly vindicated by this: window-level data alone would have misread the negative-base run as the first substantive lifted near-null the program has sought.

## Hygiene audits (pure read; all passed before recording)

Three findings-hygiene audits passed on integrity-verified data: (1) run_id / file collision - 50 runs, window CSV == block CSV == NPZ run_id sets, 50 unique NPZ filenames, uniform rows-per-run, no collisions despite byte-identical negative tiers; (2) alpha / sign mapping - zero mismatches across run_id token, base_sign, kappa-sign, and alpha column; the byte-identical negative tiers are genuinely-different-alpha railed dynamics, not mislabeling; (3) railing audit - alpha=0 baselines clean, positive nonzero pinned at extinction, negative nonzero ringing, confirming the three-regime read.

## L4 status

Not moved. The sign-asymmetric over-driven lag-feedback finding is apparatus-level only, fenced exactly as the Rule D R3 single-axis finding was fenced. Neither Psi_meanI_state nor Psi_persistence_I is named theoretical Psi; LowLow_Nondegenerate_Candidate remains an apparatus-level flag.

## Named-not-triggered follow-up (Mike's call only)

Rule E bounded-gain / recalibrated macro-gain pass: bound the realized conditioning term directly (constrain |alpha * g_E(M)|) or recalibrate the alpha ladder against the observed conditioned rho excursion scale rather than the un-conditioned sigma_M, so the sweep realizes the intended |d| tiers. NOT opened. A recalibrated pass is a separately-named next instrument, not a silent rerun of this grid. This is the one place Layer 3 would genuinely contribute again if opened - bounding gain is a substrate-design question.

## Commit record

Spec 59b4bd6; build 3738157; one-line path fix 3abf8dd; run outputs ab51d36 (window CSV, block CSV, 50 NPZs). The result-recording bundle - this ops log, RULE_E_FIRST_PASS_FINDINGS.md, and the anchor refresh - is committed in the following segment.

Drafting partner: Layer 1 (Claude), routed and executed by Mike.
