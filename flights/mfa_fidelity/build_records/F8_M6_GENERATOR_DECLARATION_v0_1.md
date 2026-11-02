# Flight 8 — M6 generator declaration, v0.1 (DRAFT for Mike's ratification and L2's build review)

**Status.** L1 draft, 2026-10-30, at Mike's word ("go") after F8 Interpretation 002 (`F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md`, SHA-256 `198d2991dd12168c…`, committed at `d474f7f`). **Not frozen.** Every value marked `[PROPOSED]` ratifies only when Mike names it; no master is drawn under this document until the complete generator — this declaration, the M6 source and its tests — is identified and placed (Interpretation 002 point 8; contract §5.3, §7.1).
**Governs.** Contract F8 v0.8.4 (`e87277a2d11e948f…`) §5.1–§5.4, §6.1–§6.4, §4.3 (the qualification-time price), §7.1 (order). Interpretation 001 (`6bf7304fd3ee287c…`) fixes the meaning of tail density wherever it appears here; Interpretation 002 fixes the SUSTAINED source and its guards.
**Placed modules this declaration binds to (identities measured from a fresh clone at `d474f7f`):** `f8/config.py` `43ea8de23c0d718b…` (M1), `f8/dynamics.py` `cc663dd3c14197a8…` (M1), `f8/classify.py` `42daeb4663c5783f…` (M2), `f8/null.py` `4ee3f239b27f772b…` (M3), `f8/verdict.py` `c79ce0d7c81e21d5…` (M4), `f8/closure.py` `9452dd11396350ab…` (M5); the carried framework `e1/audit.py` `ce5ebecd7feb11f4…` (E1 M6: declarations, Clopper–Pearson, cache role, completion, qualification). Nothing in any of them is modified by M6.
**Numbers.** Every number below was computed by script from the placed modules on 2026-10-30 (container, Linux glibc; the M3 threshold indices are integers and platform-independent; the fixed-point values are quoted to six decimals and bind through Appendix A, not through this document). Where a number is a proposal it is marked.

---

## 1. Inherited frozen objects (carried, not re-declared)

From contract §5.1, §5.4, §7.1 and E1 M6's framework, unchanged: two ensembles (design, held-out) under distinct masters; **500 sweeps per class** `[ratified, freeze item 23]`; the **applicable error** — scientific-intent classes (intended LOCATED or NOT_PRODUCED) count a final verdict of NOT_DISTINGUISHED; ND-intent classes count a final verdict of LOCATED or NOT_PRODUCED; **one-sided 95 % Clopper–Pearson upper bound ≤ 0.10** `[item 23]`; class `complete_pass` = attempted == scored == 500, zero evaluability halts, zero generator halts, cap clears; `ensemble_pass` = every class complete on a production-role threshold mapping; **`m6_audit_qualification`** = the design and held-out records mechanically joined (distinct masters, same threshold-mapping identity, exact class set, every class complete in both, distinct record identities); an adverse M6 closes the stage with no same-stage repair. Exact intended-verdict-and-cause agreement is **descriptive** and never enters a pass. M-P1's exact-cause criterion and half-band noise condition are M-P1's and are not imported (Interpretation 002 point 10).

The scoring path per sweep is E1's, verbatim in structure: for each pass-1 level, 20 runs (one per canonical seed index) → M2 `run_status` against (θ_P, θ_T) → 20 statuses → M2 `level_label` (16/2/4) → 24 labels → M4 `evaluate` (pass-1 verdict, descriptive) and M4 `route` → the router's insertions (post-fallback) → the same per-level procedure at each inserted level → final level set (pass-1 levels plus kept insertions, merged in m-order) → M4 `evaluate` on the final set = the sweep's final verdict, the one the applicable error is scored on (M7 obligation: verdict of record on the final level set).

## 2. The archetype table with F8 parameters

Widths and gaps from Appendix A of record (`94d527624beafa7c…`): s = 97,826; W_res = 293,478; Δ_route(4) = 86,958; w_A = 108,400; w_L = 228,842; w_U = 627,232; declared ranges gentle ≤ 205,958, wide ≥ 689,956 (contract §6.2–§6.3; freeze record §4). All m-quantities are exact integer micro-units; m_min = 250,000, m_max = 2,500,000.

| # | Archetype | Intended (M4 `ARCHETYPE_TABLE`, `f1e1f09f00ab2386…`) | Width class | Width draw (micro) | Onset draw (micro) | Other parameters |
|---|---|---|---|---|---|---|
| 0 | `gentle_onset` | LOCATED | gentle | U_int[108,400, 205,958] | U_int[m_min + s, m_max − s] | — |
| 1 | `abrupt_onset` | LOCATED | abrupt | U_int[0, 108,400] | same | — |
| 2 | `persistent_nonstationary_high_m` | LOCATED | abrupt | U_int[0, 108,400] | same | temporal ∈ {drift, oscillation} by one uniform (< 0.5 → drift); D ~ U[−0.10, 0.10]; A_osc ~ U[0.05, 0.25]; P ~ U_int[50, 400] ticks `[PROPOSED — E1's ranges]` |
| 3 | `nonmonotone_amplitude` | LOCATED | abrupt | U_int[0, 108,400] | same | A_att ~ U[0.5, 0.9]; M_sc ~ U[0.2, 0.4] in m `[PROPOSED]` |
| 4 | `no_sustained_anywhere` | NOT_PRODUCED (no sustained phase) | — | — | — | NULL at every level |
| 5 | `no_null_consistent_anywhere` | NOT_PRODUCED (no null-consistent phase) | — | — | — | SUSTAINED at every level (Interpretation 002 point 7) |
| 6 | `two_resolved_crossings` | NOT_PRODUCED (order violation) | abrupt (width 0) | 0 | U_int[m_min + s, m_max − 8s] = U_int[347,826, 1,717,392] | second crossing at onset + 4s = onset + 391,304; third at onset + 7s = onset + 684,782 `[contract §5.2: "[4, 7] pass-1 spacings"; read as the pair (4s, 7s) — Mike to confirm]` |
| 7 | `reentrant` | NOT_PRODUCED (order violation) | abrupt (width 0) | 0 | U_int[m_min + s, m_max − 7s] | return to NULL at onset + rhe(U[4, 6]·s) ∈ [391,304, 586,956] |
| 8 | `off_band_mixture` | NOT_DISTINGUISHED (off-boundary mixture) | gentle | as gentle | as gentle | extra level = pass-1 index U_int[0, 3]; mixture π ~ U[0.45, 0.55] `[item 14]` |
| 9 | `off_band_unresolved` | NOT_DISTINGUISHED (off-boundary unresolved) | abrupt | as abrupt | as abrupt | three adjacent DIP levels at pass-1 indices k, k+1, k+2 with k ~ U_int[0, 3] |
| 10 | `wide_mixed_boundary` | NOT_DISTINGUISHED (boundary unresolved at W_res) | wide | U_int[689,956, 1,003,571] (1.1·w_U to ⌊1.6·w_U⌋) | same as gentle | — |
| 11 | `unresolved_heavy_boundary` | NOT_DISTINGUISHED (boundary unresolved at W_res) | wide | as wide | as gentle | DIP at every level inside [lo, hi) |

Class index = row number (the RNG hierarchy keys on it). Profile for the ramp classes (0–3, 8, 10): lo = onset − ⌊w/2⌋, hi = onset + ⌊w/2⌋ (for w = 0, lo = hi = onset); regime at level m for seed index j: SUSTAINED iff u_j < frac(m), frac = 0 for m < lo, 1 for m ≥ hi, (m − lo)/(hi − lo) between — the E = w·(u₍₁₈₎ − u₍₃₎) ~ w·Beta(15, 6) law of §6.1 is unchanged. Rows 6–7: regime deterministic in m (no uniform consulted). Row 9: the three extra levels are DIP; elsewhere the ramp rule. Row 11: DIP inside [lo, hi), NULL below, SUSTAINED at and above hi. Row 8: at the extra level SUSTAINED iff u_j < π, elsewhere the ramp rule.

**Geometric preflight (carried from E1 `archetype_preflight`, applied to F8's grid):** ramp classes need ≥ 1 pass-1 level < lo and ≥ 1 pass-1 level ≥ hi; row 6 needs ≥ 1 pass-1 level in each of the four regions; row 7 needs levels below the onset, inside the sustained region and at or above the return; rows 8–9 need the extra level(s) strictly below lo. These are placement checks; §4's amplitude and temporal checks are additional, per L2 §5.5.

## 3. The three regime sources

All three produce one **active-count series** K[0..3000] of 3,001 entries (M1's record convention: K[0] the state at t = 0, K[t] after tick t), N = 2,500, on which M2 operates as `rho = K / N` (float64, exactly on the count grid, so M2's `recover_counts` reconstruction verifies). A synthetic record is never represented as an M1 trajectory: provenance fields name the regime source, the class, the sweep, the level and the seed index.

**3.1 NULL — the §2.9 Markov null as an aggregate count process.** K₀ ~ Binomial(N, π₁); K_{t+1} = U_t + V_t, U_t | K_t ~ Binomial(K_t, 1 − q), V_t | K_t ~ Binomial(N − K_t, a), with a = 1 − e^(−η₀Δt) = 0.010000000000000009 (as M1's `activation_probability` evaluates it), q = 1 − e^(−μΔt) = 0.18126924692201818, π₁ = a/(a + q) = 0.052282320137314486 — M3's `chain_rates()`. This is E at feedback coefficient zero (Interpretation 002 point 2); in distribution it is the law M3's thresholds were certified against. Draw order per tick: U_t then V_t, from the run's own stream (§5).

**3.2 SUSTAINED — the finite-N current-density closure E (Interpretation 002 point 1).** K₀ ~ Binomial(N, π₁) (stationary-null start, as the committed realization is started); K_{t+1} = U_t + V_t with U_t | K_t ~ Binomial(K_t, 1 − q) and V_t | K_t ~ Binomial(N − K_t, a_t(K_t)), a_t(k) = 1 − e^(−(η₀ + c(m, t)·k/N)Δt). Unmodulated (rows 0, 1, 4–11 and the constant case): c(m, t) = gλ̄ = m·q/Δt (M5 `lambda_bar`), so that E[K_{t+1}/N | K_t/N = x] = F_m(x), the §3.1 map. Modulated (rows 2–3): c(m, t) = c_tar(m, t) of §4. The construction is M5's `finite_n_counts` with c in place of gλ̄; M6 carries its own copy (the M6 source names the identity it was copied from and `test` asserts bit-equality of the unmodulated path against `finite_n_counts` on a shared stream), so that M5 is not modified and M6's law is in M6's own file.

**3.3 DIP — the UNRESOLVED construction (Interpretation 002 point 5).** The run is the unmodulated E process of §3.2 at the level's m, with two declared modifications stated before sampling: (i) the counts of one **nonterminal** tail window w ~ U_int[0, 8] (ticks 2001 + 100w … 2100 + 100w) are set to 0; (ii) in the **terminal** window (ticks 2901 … 3000) each count is K_t ← max(K_t, k_floor) with **k_floor = ⌊idx_T / 100⌋ + 1 = 142**, idx_T = 14,121 being M3's θ_T window-count index (θ_T = 14,121/250,000 = 0.056484, conservative-coverage mode). Then S_min = 0 ≤ θ_P and S_term ≥ 14,200/250,000 = 0.0568 > θ_T **by support**, so M2 returns UNRESOLVED with certainty and §6.4's "U deterministically" holds. The floor is a declared part of the DIP regime's definition; it is never applied to a NULL or SUSTAINED trace. The build evidence includes a DIP at w = 8 (adjacent to the terminal window), a terminal window whose unmodified counts all lie below k_floor, and the equality case K_t = k_floor.

## 4. Modulation law (rows 2–3)

**4.1 Target → probability → hazard → coefficient (L2 §5.2; Interpretation 002 point 3).** A schedule gives a target density r_tar(m, t). The stationary activation probability that would hold the independent-chain equilibrium at r_tar is a_tar = q·r_tar/(1 − r_tar); its hazard is H_tar = −ln(1 − a_tar)/Δt; the synthetic feedback coefficient is c_tar(m, t) = (H_tar − η₀)/r_tar, and E runs with a_t(k) = 1 − e^(−(η₀ + c_tar·k/N)Δt). At r_tar = ρ*(m; η₀) this gives c_tar = gλ̄ exactly (checked in `test` at every pass-1 level to 1e-12 relative). The target is a target: the realized mean of a time-varying schedule lags it and is never asserted to equal it; the process is never reset to the target.

**4.2 Legal domain and floor.** For every (m, t) in the schedule's domain: **r_floor ≤ r_tar(m, t) < 1/(1 + q) = 0.84655**, where **r_floor = ρ*(m_min; η₀) = 0.066903** `[PROPOSED]` — the unmodulated realization's density at the bottom of the sweep, the lowest density any unmodulated SUSTAINED run in this generator is targeted at. The upper bound is the finite-hazard condition (a_tar < 1); the lower bound preserves the spontaneous floor (r_tar ≥ π₁ = 0.052282 follows) and keeps modulated targets no lower than the generator's own lowest unmodulated target. A draw violating either bound is **refused at preflight and redrawn** (§4.5); nothing is clipped. Design evidence for the floor, not a guarantee (L2 §5.4): 40 unmodulated E runs at m = m_min on a container stream gave tail-mean density 0.06695 (seed-to-seed SD 0.00072), within-run window-mean SD 0.0017, min S_min = 0.06066 > θ_P = 0.057364, 40/40 SUSTAINED; the target–threshold gap at the floor is 0.00954. Whether a trajectory receives its intended status remains a stochastic outcome scored by the audit.

**4.3 Schedules.**
- **Constant** (default): r_tar ≡ ρ*(m; η₀), i.e. c = gλ̄; no target machinery is invoked.
- **Drift** (row 2, temporal = drift): r_tar(m, t) = ρ*(m; η₀)·(1 + D·(t/T − ½)), T = 3,000, t = 0 … 3,000 (time origin t = 0, the whole horizon, so the tail sees the schedule's last third). D ~ U[−0.10, 0.10].
- **Oscillation** (row 2, temporal = oscillation): r_tar(m, t) = ρ*(m; η₀)·(1 + A_osc·sin(2πt/P)), A_osc ~ U[0.05, 0.25], P ~ U_int[50, 400] ticks, phase 0 at t = 0.
- **Attenuation** (row 3): r_tar(m) = max(r_floor, π₁ + κ(m)·[ρ*(m; η₀) − π₁]), κ(m) = 1 − A_att·max(0, (m − m_onset)/M_sc), A_att ~ U[0.5, 0.9], M_sc ~ U[0.2, 0.4] (in m); constant in t. The max(·) is part of the declared schedule (the floor binds by design at high m), not a clip of an illegal rate.
Rows 2–3 apply the schedule in SUSTAINED-assigned runs only; NULL and DIP runs at the same levels are unmodulated.

**4.4 Morphology preflight (L2 §5.5).** Beyond §2's placement checks, a parameter draw passes only if:
- row 2, drift: |D| ≥ 0.02 and min over t of r_tar ≥ r_floor at every SUSTAINED-eligible level (every pass-1 level ≥ lo) — the drift is actually present (≥ 2 % end-to-end) and legal;
- row 2, oscillation: A_osc ≥ 0.05 (always, by range), P ≤ 400 so ≥ 2.5 periods fall inside the tail, and ρ*(m; η₀)·(1 − A_osc) ≥ r_floor at every SUSTAINED-eligible level (computed: admissible lowest level m = 0.348 at A_osc = 0.05, 0.446 at 0.15, 0.543 at 0.25, so the check binds for low onsets);
- row 3: at least two pass-1 levels ≥ hi; the resulting r_tar profile over the pass-1 levels ≥ hi is strictly decreasing from the first to the second and non-increasing thereafter (the **resulting** profile, with ρ*(m; η₀)'s rise included — a decreasing κ alone does not suffice); r_floor ≤ r_tar < 1/(1 + q) everywhere. Feasibility under the proposed ranges, by script: 88.9 % of 2,000 uniform draws pass.
A failing draw is redrawn from the dedicated parameter stream (§5), up to **MAX_REDRAWS = 64** `[PROPOSED — E1's budget]`; exhaustion is a **generator halt** (apparatus failure, counted in the class's completion accounting, never a classifier error). The attempt count is recorded per sweep.

**4.5 What preflight does not do.** It never looks at a sampled trajectory or at M2's status. No NULL, SUSTAINED or DIP path is redrawn or discarded on account of its classification (Interpretation 002 point 4).

## 5. RNG hierarchy, draw order, trace convention

- Regime uniforms: `SeedSequence([master, class_index, sweep_index, 0])` → 20 uniforms u_0 … u_19, one per canonical seed index, **shared across every level of the sweep** (contract §5.1).
- Parameter draws: `SeedSequence([master, class_index, sweep_index, 2, attempt])`, attempt = 0, 1, …; within an attempt the draw order is fixed: onset, width, temporal selector, D, A_osc, P, A_att, M_sc, π, return offset, extra index (every stream draws all of them whether or not the class uses them, so a class's parameter identity never depends on which fields it reads).
- Run streams: `SeedSequence([master, class_index, sweep_index, 1, level_micro, seed_index])` — one per (level, seed index), keyed by the level's exact micro-unit identity, so an inserted level's runs have the same stream whether it is reached by P2R-5 or P2R-6 and whatever the order in which levels are processed. Per run the draw order is K₀, then per tick U_t, V_t, then (DIP only) the window selector w from the same stream after the series. No stream is shared between levels or sweeps; no trajectory is copied (Interpretation 002 point 4).
- Trace: 3,001 int64 counts; M2 scores ticks 2001–3000; `rho = K / 2500` passed to M2 as float64. The series is not M1's one-uniform-per-cell stream and claims no M1 identity.
- Implementation latitude: runs may be executed in any order or batched across seeds; identity is fixed by the per-run streams above, and `test` asserts that batched and sequential execution give bit-identical series.
- Measured, not promised: one unmodulated E run of 3,000 ticks took 6.6 ms on the container (10-run mean). The upper-bound run count per ensemble is unchanged at 12 × 500 × 32 × 20 = 3,840,000; the realized count depends on routing.

## 6. The reachable-level threshold adapter (Interpretation 002 point 6)

- The reachable pass-2 surface is derived from the placed router: `route()` post-fallback over the 276 canonical band witnesses of M4's `reachable_router_cases` (N at and below i, U between, S at and above j), yielding **338 distinct insertion levels** off the pass-1 grid (reachable rows: P2R-5 and P2R-6 only; P2R-3/4/7 are dead on this surface, M4 `dead_rows`). With the 24 pass-1 levels the adapter has **362 keys**.
- The §4.3 law is level-independent (M3 docstring; contract §4.3 note). The adapter maps every key to the **one** M3 payload: `null_thresholds(F8_LEVELS_MICRO[0])`, θ_P = 14,341/250,000 = 0.057364 (conservative coverage), θ_T = 14,121/250,000 = 0.056484 (conservative coverage), payload identity `597e39bd5093e51d…` as computed on the container (the payload carries float64 certificate fields through `exp`; the identity is re-measured on the canonical machine at placement and the record states what the machine saw, as M5's Appendix A binding does).
- The adapter is an M6 object with its own declaration digest and a committed JSON artifact: header (M3 declaration digest, M4 declaration digest, reachable-surface identity = SHA-256 of ("m4", M4 digest, the 338 levels)), the 362 keys in canonical order, each row (level_micro, theta_p, theta_t, payload identity). Role `production_frozen` is granted only by a loader that re-derives the surface from `route()`, re-derives the thresholds from M3, and requires both the body and the file digest to equal source literals; a missing key at scoring time is an **apparatus halt** (the sweep is HALTED, the class incomplete), never an on-demand derivation. Slice role for tests only.
- Nothing in M1's run-spec guard or M3's level domain changes; the adapter does not relabel an off-grid level as an M3 object — it records that M3's level-independent payload is the scoring object at that key.

## 7. The §4.3 qualification-time price (Interpretation 002 point 9a)

Under the **pricing master**, **n_price = 10,000** `[PROPOSED]` complete 3,000-tick NULL runs of §3.1 (streams `SeedSequence([pricing_master, 0, replicate])`), each scored by M2 at the adapter's (θ_P, θ_T); report the count and rate of S_min > θ_P (nominal ≤ α_P = 0.001; the construction's own bound is N_WINDOWS·(1 − F_W(θ_P)) = 0.000971), the exact one-sided 95 % Clopper–Pearson upper bound on the rate, and, descriptively, the count of S_term ≤ θ_T (nominal ≈ 1 − α_T). Zero rejections is reported with its CP upper bound (at 0 of 10,000: 0.0003), never as "zero probability". This is the contract's descriptive price; it is not a pass condition. The separate stepper-based price already of record — M3 attempt 2's `s_min_rejection_rate` on the actual F8 stepper (`validate_on_stepper`, n = 1,000, master 320261027) — is cited beside it, not replaced. E1's `run_pricing` (θ_T exceedances) is not carried. Docstring defect of record: `null.py` names `price_familywise`, which does not exist; M7 lists its repair.

## 8. The job-0 comparison method (frozen now; values pending; Interpretation 002 point 9b)

When the two-part calibration census exists under its own authorization, a descriptive supplement with its own identity reports, per pass-1 level: (a) the lattice realization's tail density (ρ̂ as Interpretation 001 fixes it: mean over the 1,000-tick tail) — seed-mean over the 20 calibration seeds — against the E surrogate's tail-density mean over **n_cmp = 200** `[PROPOSED]` unmodulated runs at the same level under a declared comparison stream (`SeedSequence([pricing_master, 1, level_micro, replicate])`), with the signed difference lattice − surrogate; (b) ŝ(m) (ddof = 1, 20 seeds) against the surrogate's SD of the same observable (ddof = 1, 200 runs), with the signed difference and the ratio surrogate/lattice, "undefined" when ŝ(m) = 0; (c) the two estimators' standard errors; (d) a fixed-text statement that the surrogate lacks spatial dependence and that the lattice/closure amplitude mismatch is the fidelity tier's object (§1.2′, Appendix B.4). Insertion levels are not covered. The supplement is attached to the M6 governance entry when available; it is not a prerequisite for the M6 audits, never retunes the generator, and makes no claim that surrogate variance bounds lattice variance.

## 9. Masters (DERIVED@BUILD; drawn once, after the complete generator is placed)

`[PROPOSED rule]` Following the placed pattern (`F8_SEED_PANEL_MASTER` 20261026, calibration 120261026, null-validation attempt 2 320261027, projection 420261028, M-P1 synthetic census 520261028 — a role prefix followed by the build date): **design = 6YYYYMMDD, held-out = 7YYYYMMDD, pricing = 8YYYYMMDD**, with YYYYMMDD the date of the commit that places the complete generator. The three values are literals in the M6 source, distinct from each other and from every declared master (20261026, 120261026, 220261026, 320261027, 420261028, 520261028) and from E1's retired 202609221/2/3; `verify_frozen_identity` checks the whole collision set. They are never replaced after any audit outcome.

## 10. Declarations for ratification (with the governance record)

| # | Declaration | Value |
|---|---|---|
| M6-1 | SUSTAINED source | reading E per Interpretation 002 (ruled; restated here as the executable law of §3.2) |
| M6-2 | NULL source | the aggregate count process of §3.1 (E at zero feedback), M6's own draw order |
| M6-3 | DIP construction | nonterminal zero window w ∈ [0, 8]; terminal floor k_floor = 142 per tick |
| M6-4 | modulation floor | r_floor = ρ*(m_min; η₀) = 0.066903 |
| M6-5 | modulation ranges | D ∈ [−0.10, 0.10]; A_osc ∈ [0.05, 0.25]; P ∈ [50, 400]; A_att ∈ [0.5, 0.9]; M_sc ∈ [0.2, 0.4]; drift minimum 2 % end-to-end |
| M6-6 | redraw budget | 64 per sweep |
| M6-7 | two-crossing offsets | the fixed pair (4s, 7s) = (391,304, 684,782) micro |
| M6-8 | reachable adapter | 362 keys (24 + 338) bound to the single M3 payload; fail-closed |
| M6-9 | §4.3 price | 10,000 NULL replicates under the pricing master; event S_min > θ_P; exact CP |
| M6-10 | job-0 comparison | method of §8; n_cmp = 200; values pending job 0 |
| M6-11 | masters rule | 6/7/8 + placement date |
| M6-12 | wide upper bound | ⌊1.6·w_U⌋ = 1,003,571 micro |

## 11. What this declaration does not do

It draws no master, runs no audit, and prices nothing; no figure in §4.2's design evidence or §5's timing is an instrument result. It does not modify M1–M5 or M-P1. It does not claim that M6 qualification measures the instrument's error rate on lattice runs (Interpretation 002 point 10). It does not import M-P1's qualification criteria. Where it reads a contract clause (the "[4, 7] spacings" pair, the floor, the ranges), the reading is marked for Mike; L2 reviews the built source against this document and the contract.

*L1, 2026-10-30, v0.1.*
