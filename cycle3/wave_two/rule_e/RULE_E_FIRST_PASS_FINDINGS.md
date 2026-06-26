# Rule E first pass - findings (scoped negative for the predeclared design)

**Status: FINDINGS. Layer 2-arbitrated 2026-06-12; Mike-concurred. Governs the Rule E first-pass result.** The Rule E first pass executed the committed design (contract 2f3ce0e, opens resolution 65a7265, spec 59b4bd6 / build 3abf8dd) and is committed at ab51d36 (window CSV, block CSV, 50 state NPZs). This file records what the predeclared first pass produced. It is read against the contract's contrastive criterion and the two guards; the CSVs are primary source over this restatement.

## Result

**Rule E first pass FAILS TO PRODUCE a substantive multiscale near-null under the locked topology and the predeclared first-pass design.** The failure mode is not inertness; it is over-driven block-lag feedback producing extinction on one base sign and block-cadence oscillation / temporal cancellation on the other. This is a scoped negative for the predeclared design. It does NOT close the Rule E mechanism class.

Pre-run gates passed: F3 alpha=0 reproduced committed Rule C M2 bit-exactly over a full 400-tick trajectory at (Lambda=0.40, kappa=+/-0.7599, every seed). Split pre-registered constants measured at block scale on the alpha=0 baseline: M_ref_plus=0.3714 / sigma_M_plus=0.0025; M_ref_minus=0.4187 / sigma_M_minus=0.0017.

## The two-sided outcome (per-(setting, seed); window CSV + block CSV)

| Base sign | First-pass outcome | Candidate status |
| --- | --- | --- |
| Positive (c=+0.35, kappa=+0.7599) | extinction at all nonzero alpha tiers (block_rho ~0.000, extinction_degenerate=True; cond_logit_term pinned -3 to -60 logits driving p_become->0) | degenerate; not candidate |
| Negative (c=-0.35, kappa=-0.7599) | window-level lifted near-null flags (mean_rho~0.326, LowLow_Nondegenerate_Candidate=True on ~all post-burn-in windows), BUT block record shows a 25-tick-cadence saturate/extinct oscillation (block_rho rings ~0.02 <-> ~0.63; ~50% of post-burn-in blocks <0.05 and ~50% >0.60) | lag-dynamics artifact; not candidate |

## Why the negative-base flags are rejected (the operative rejection: lag-dynamics guard)

The negative-base window-level LowLow_Nondegenerate_Candidate=True flags are NOT valid Rule E candidates. The window mean_rho~0.326 is the AVERAGE of a violent 25-tick-cadence oscillation between near-saturation (~0.63) and near-extinction (~0.02) - a value no tick is near. The block-resolved record shows raw_Psi_meanI_state_block sign-alternation in 5/5 negative-base runs at every conditioned tier. Per the contract (Section 5), a window whose apparent near-null is produced by temporal cancellation / oscillation across macro blocks is classified as a lag-dynamics artifact for candidate-status purposes, not a candidate. The operative rejection is the lag-dynamics guard, NOT a reach failure; once the guard fires, window-level reach analysis is moot for those windows.

For the positive base the rejection is simpler: degenerate extinction.

## Failure mechanism (calibration / runaway feedback; diagnosis, not a separate finding)

The channel was over-driven, not inert (the inert-channel hypothesis was raised during the read and REFUTED by the block CSV - recorded for honesty). The alpha grid was scaled by sigma_M measured on the UN-CONDITIONED baseline (~0.0017). Once conditioning perturbs rho, rho feeds the next block's macro signal M; the standardized g_E = (M - M_ref)/sigma_M divides the conditioned excursion by the tiny un-conditioned sigma_M, so g_E reaches +/-230 and the conditioning term reaches +/-100 logits - orders of magnitude beyond the intended |d|<=0.10 probability displacement. The feedback rails: extinction (positive) or block-cadence ring (negative). The negative tiers m0_1054 / m0_2136 / m0_4418 produce byte-identical block_rho trajectories because once g_E saturates the logit, larger alpha cannot change the railed per-block outcome.

This is the run-time realization of the contract's honest-scope bound: tau_rho=1.66 (un-conditioned) / 2.86 (coupled base) did NOT certify conditioned dynamics, and the lag-dynamics guard was the predeclared run-time catch for exactly this. The guard caught it.

## What is vindicated

The block-resolved recording requirement (contract Section 5) is strongly vindicated. Without block-level data the negative-base run would have been misread at the window level as the first substantive lifted near-null regime the program has sought. With it, the system correctly classifies the window-level LowLow flags as false positives of the lagged-feedback measurement structure. Future L4 interpretation cannot rest on window-level z-scores alone in macro-feedback settings - a window-level joint near-null can be manufactured by block-phase cancellation over violently structured block dynamics.

## L4 status (fenced)

This does NOT resolve or move the L4 ontological question. The structural finding - positive-base conditioning drives extinction; negative-base conditioning drives block-cadence saturate/extinct oscillation; the response is sign-asymmetric and over-driven rather than inert - is apparatus-level only, fenced exactly as the Rule D R3 single-axis finding was fenced. It identifies neither Psi_meanI_state nor Psi_persistence_I as theoretical Psi. The two observables remain co-equal apparatus observables; LowLow_Nondegenerate_Candidate remains an apparatus-level flag; no outcome confirms / validates / proves Regime II by construction. If anything, the result reinforces the L4 caution.

## Findings-hygiene audits (pure read; passed before recording)

1. run_id / file collision: 50 runs, window CSV == block CSV == NPZ run_id sets, 50 unique NPZ filenames, uniform rows-per-run (13 windows / 16 blocks). No collisions despite byte-identical negative tiers. (50 runs = 5 d-tiers x 5 seeds x 2 signs; the d=0 tier is one alpha=0 run per sign.)
2. alpha / sign mapping: zero mismatches (run_id token vs base_sign, kappa-sign, alpha token vs alpha column); alpha values sign-consistent per tier. The identical tiers are genuinely-different-alpha railed dynamics, not mislabeling.
3. railing audit: alpha=0 baselines clean (no rail); positive nonzero pinned at extinction (frac<0.05 = 1.00); negative nonzero ringing (frac<0.05 ~0.50 AND frac>0.60 ~0.50). Confirms the three-regime read on integrity-verified data.

## Mechanism class NOT closed; follow-up named-not-triggered

The broader Rule E (lagged-Lambda conditioning) mechanism class is NOT closed by this scoped negative. The first pass did not fail to execute; it exposed that the standardized macro-gain construction is dynamically unstable once the conditioning channel feeds back on its own macro signal under the un-conditioned sigma_M scaling.

**Named-not-triggered follow-up (Mike's call only; analogous to the Rule D stronger-turnover endpoint extension): Rule E bounded-gain / recalibrated macro-gain pass.** Purpose: test whether lagged-Lambda conditioning can remain responsive without railing into extinction or block-cadence oscillation. A predeclared correction would bound the realized conditioning term directly (e.g. constrain |alpha * g_E(M)|, or use a smaller alpha ladder calibrated against the observed CONDITIONED rho excursion scale rather than the un-conditioned sigma_M) so the sweep realizes the intended |d| tiers. NOT opened here; recorded as a named follow-up, not a substitute for this finding. A recalibrated pass is a separately-named next instrument, not a silent rerun of this grid.

- Layer 1 (Claude); Layer 2-arbitrated; Mike-concurred
