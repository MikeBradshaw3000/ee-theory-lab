# Rule E bounded-A - findings (scoped negative for the predeclared 50-run own-direction design)

**Status: FINDINGS. Layer 2-arbitrated 2026-07-01; Mike-concurred. Governs the Rule E bounded-A result.** The bounded-A pass executed the committed design (resolution d0bd184, spec 0ae9458 as grid-corrected at 99c2661, build 4d48e57 + one-line F3 path fix at 99c2661) and is committed at 99c2661 (window CSV, block CSV, 50 state NPZs). This file records what the bounded-A pass produced. It is read against the corrected spec's six-guard classification; the CSVs are primary source over this restatement.

## Result

**Rule E bounded-A FAILS TO PRODUCE a substantive multiscale near-null under the locked topology and the predeclared 50-run own-direction design.** No LowLow_Nondegenerate_Candidate window occurs (0 of 450 post-burn-in windows); criterion 3 fails directly. The amplitude-bounded construction REPAIRS the first-pass runaway pathology - no degeneracy, no extinction, no saturate/extinct ring, no identical-tier collapse, and the macro channel is non-inert - but the channel is SATURATED at every nonzero tested tier: bound_active is true in all post-burn-in blocks and all post-burn-in windows are saturated-channel by construction. **The result therefore tests a bounded saturated relay, not clean-responsive macro conditioning.** Runaway repaired; relay behavior remains. This is a scoped negative for the tested design. It does NOT close the Rule E mechanism class.

Pre-run gates passed: F3 d=0 reproduced committed Rule C M2 bit-exactly over a full 400-tick trajectory at (Lambda=0.40, kappa=+/-0.7599, every seed) - after a one-line wrong-directory import fix of the same class as the first pass's 3abf8dd, caught loudly at F3 before any data was written. Split pre-registered constants reproduced exactly at block scale: M_ref_plus=0.3714 / sigma_M_plus=0.0025; M_ref_minus=0.4187 / sigma_M_minus=0.0017.

## The two-sided outcome (per-(setting, seed); window CSV + block CSV)

| Base sign | Bounded outcome | Candidate status |
| --- | --- | --- |
| Positive (c=+0.35) | The first-pass extinction path is converted by the cap into STABLE SUPPRESSED EQUILIBRIA: g_E pins negative, block_rho steps down monotonically with tier (0.37 -> 0.29 at d=0.10), no degeneracy, all windows lifted and strongly positively signed on both observables (z_mI up to ~12) | no candidate; no LowLow |
| Negative (c=-0.35) | The first-pass catastrophic saturate/extinct ring (0.02 <-> 0.63) is replaced by a BOUNDED block-cadence ring around baseline (0.36 <-> 0.47 at d=0.10; amplitude grows with tier; g_E sign-alternates), no degeneracy, all windows lifted and signed | no candidate; no LowLow |

All tiers DISTINCT within every sign+seed (10/10) - the first-pass identical-tiers pathology is gone; each tier settles at its own level, monotone in Delta_j. The tier-specific bound performed its designed work.

## The central apparatus finding: saturated relay

At every nonzero tier, both signs, all seeds: bound_active = 12/12 post-burn-in blocks; saturated_channel_flag = True on 9/9 post-burn-in windows; |g_E| never below 2.2 even at the smallest tier (activation threshold atanh(0.90) ~= 1.472). The conditioned excursion of M is enormous relative to the UN-conditioned sigma_M (~0.0017-0.0025), so g_E lives deep in tanh saturation and the realized term sits pinned at ~+/-Delta_j. Bounding the OUTPUT amplitude is not enough when the ARGUMENT remains standardized by the un-conditioned block-sigma: Candidate A fixes how large the applied term can get; it does not fix whether the macro signal lives in the graded part of the response curve.

**Responsive-window analysis (Layer 2, quantified):** saturation onsets once the block mean moves only ~1.472 * sigma_M in rho - approximately 0.0037 (positive base) / 0.0025 (negative base). The smallest tested tier already exceeded threshold in every post-burn-in block. For bounded-A with un-conditioned-sigma g_E, the clean-responsive region is likely EMPTY at practical resolution or compressed vanishingly close to zero. The un-conditioned-sigma standardized argument is structurally mis-scaled for conditioned dynamics under this substrate. Consequence for any future pass: rescale the ARGUMENT (the B/C conditioned-scale territory, or a rescaled-argument bounded variant), do not merely shrink the d tiers - "bounded-A with smaller d" is not the indicated first follow-up.

## No candidate; guards diagnostic

d=0 separability passed (F3 bit-exact at trajectory level; d=0 rows clean, bound never active). Signed-regime reach satisfied sign-locally (every window strongly signed, z ~2-12). Criterion 3 unmet on its face (zero LowLow). With no candidate window, guards 4-6 adjudicate nothing; they are diagnostic of the channel state - the lag-dynamics record shows the bounded negative-base ring, the inert-channel guard shows the channel demonstrably non-inert, and the saturated-channel guard shows every conditioned window saturated. Had a near-null appeared, it would have been saturated-channel-fenced by construction.

Completeness note (Layer 2 wording): one negative-base high-tier window shows a single-axis Psi_meanI_state_z dip below 2.0 (~1.92), but Psi_persistence_I_z remains non-near-null, so no joint near-null candidate or near-miss is recorded. The co-equal pair holds.

The wave-one pattern persists under bounded macro conditioning: every lifted window remains non-near-null on at least one co-equal observable, usually both. The lifted-near-null region remains unreached by this instrument.

## L4 status (fenced)

Not moved. The saturated-relay / suppressed-equilibrium / bounded-ring findings are apparatus-level only, fenced exactly as the Rule D single-axis and first-pass lag-feedback findings were fenced. Neither observable is named theoretical Psi; no outcome bears on Regime-II identification. The block-level discipline is again reinforced - macro-conditioned runs can produce dynamics that window-level summaries alone would misread - though here no window-level LowLow fired, so the misread risk was lower than in the first pass.

## Findings-hygiene (pure read; passed before recording)

50 runs; window CSV == block CSV run_id sets; uniform rows-per-run (13 windows / 16 blocks); NPZ filenames align with run_ids and confirm the own-direction grid structure (km paired only with d0/dm tiers, kp only with d0/dp). Grid arbitration recorded in the corrected spec (Section 5): the predeclared "90" matched neither pass's build; 50 IS the instrument (first-pass parity); the 40 cross-direction cells are named-not-triggered pending a design resolution.

## Mechanism class NOT closed; follow-ups named-not-triggered

The broader Rule E mechanism class is NOT closed. The bounded-A result specifically shows the residual failure is the ARGUMENT SCALE, which is exactly what the held Candidates B (recalibrated ladder) and C (conditioned-scale denominator) were designed to address. **Their standing is STRENGTHENED but they are NOT triggered** - more scientifically motivated as follow-ups than before bounded-A, still named, still requiring the seven-condition freeze discipline review before opening, still Mike's call only. A rescaled-argument bounded variant is likewise available as a named construction. This finding does not support the broader claim that block-lagged Lambda conditioning is inherently inert-or-saturated; it supports only the narrower claim about un-conditioned-sigma standardization. The cross-direction extension (40 mixed-direction cells) remains separately named-not-triggered.

- Layer 1 (Claude); Layer 2-arbitrated; Mike-concurred
