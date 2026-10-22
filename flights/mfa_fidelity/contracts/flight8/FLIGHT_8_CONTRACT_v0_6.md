# Contract F8 — Flight 8: the first transition under the hazard rule (v0.6, DRAFT)

**v0.6, 2026-10-21 — supersedes v0.5 (`5b2ae13701e12950`, committed at `8882e7a`, retained).** Discharges the open derivation of v0.5 and, on its result, **re-tiers the claim grammar by Mike's ruling of 2026-10-21 (option (a))**:
- **Appendix B is computed.** The pair approximation, derived from §2.4 as written (synchronous, Moore z = 8; equations in Appendix B), gives **m_lat = 1.1414** at μ = 0.2 (1.135–1.143 over μ ∈ [0.05, 0.5]). It is fixed here and recorded.
- **Design evidence (noncanonical, L1's own seeds, pre-freeze; Appendix B §B.4).** A 50×50 skeleton on the lattice itself survives at no level ≤ 1.35, at 1 of 6 seeds at 1.40, at 6 of 6 at 1.45: the lattice crossing is ≈ 1.40–1.45, **above the pair value by 0.26–0.31, more than twice Δm**, and the lattice's quasi-stationary density above the crossing (0.12 at m = 1.5) is well below both closures (mean field 0.31; pair 0.24). The closures predict the structure of the transition correctly and its location and amplitude poorly — the known behaviour of such closures for local stochastic processes.
- **Consequence (option (a)).** **P1 is structural** — a boundary exists inside the sweep, the branch rises continuously from zero, there is no hysteresis, and the floor-rounded realization is continuous and monotone with its steepest ascent above the boundary (§1.2, tests T-S1′, T-S1c, T-S2, T-R1′, T-R2′). The **location and amplitude** comparisons — m̂_c against the closure's 1 and the pair's 1.1414; ρ̂ against both branches — form a pre-registered **closure-fidelity tier** (§1.2′), reported as shifts and never as P1 pass/fail. This reads amendment §7 as written: the pre-registered Jacobian crossing is the closure's; the lattice realizes the structural change. Δm, the calibration census and MDD remain as the tolerances of the fidelity tier.
- L2's three safeguards on Appendix B are honoured: the equations are derived from the synchronous rule, not imported; m_lat is fixed before any canonical data; the known-answer test on pair-generated data is stated to test implementation only, and the lattice check is labelled design evidence, not validation.

**v0.5, 2026-10-21 — supersedes v0.4 (`247133c0f9b1e837`, retained).** Responds to L2's substantive disposition on v0.4 (`L2_FLIGHT8_CONTRACT_V0_4_SUBSTANTIVE_DISPOSITION_RECEIVED.md`, `c408ed30932058f0`: NOT YET FREEZABLE; rule and successor separation accepted in principle; seven mandatory items). Every item is addressed below and in the response; the two blocking defects are discharged with computation, and one further defect L1 found in the course of it is stated openly rather than deferred:
- **(L2-7.1) T-R1.** The exclusion window is withdrawn; §3.4/§4.10 are reconciled: T-R1 scores every level against a band whose realization-side uncertainty comes from a pre-registered **calibration census** under its own master (§7.3 job 0), never from the canonical census; a **separately named near-critical endpoint T-R2** (the location of the realization's steepest ascent against the map's own inflection, m_infl = 1.18 under PROPOSED values, not m = 1) is added with pass/fail criteria. M-P1's algorithm (§4.11) now handles extinction, unevaluable seeds, absent or out-of-sweep crossings and ties, and its known-answer set includes cases that must fail.
- **(L2-7.2) `off_band_mixture`.** L1's "> 0.99" claim was false; the exact binomial risk at π = 0.3 is 0.1071 (L2's figure confirmed). The generator's range is revised to **π ∈ [0.45, 0.55]**, where the risk is ≤ 0.0052 < ε. The other §6.4 non-ramp claims now carry their derivations (§6.4, Appendix A).
- **(L2-7.3) Δ_route.** Certified by an **exhaustive check over every band of the F8 grid** (all 276 pass-1 index pairs) with collided candidates removed — the worst case for gaps, which dominates both fallback moves and drops: for B = 4, 2·max gap = **86,958** (v0.4's 86,956 corrected). Collisions occur only at B ∈ {3, 6, 9}; B ≤ 4 covers every locatable class (§6.2).
- **(L2-7.4) §3.4** is now stated as a **declared design tolerance**, not a coverage guarantee, with the approximation named; the survival criterion is an expectation and is said to be one. Per-level populations and initialization panels for T-S1/T-S2/T-R1/T-R2 are declared (§4.11).
- **(L2-7.5) Appendix A** carries every DERIVED@FREEZE quantity with a value or a procedure that terminates before freeze, including the §6.4 residuals and rule-1 grid coverage (now deterministic by construction of the offset draws).
- **(L2-7.6)** Mike's items are listed in §10 unchanged; no PROPOSED value is represented as approved.
- **(L2-7.7) Cross-references**: the duplicated §4.9 is renumbered (§4.9 detection, §4.10 M7, §4.11 M-P1); §1.2 points to §4.11; "every level" in M-P1 is now correct because the exclusion is gone; §10 and Appendix A state which values are provisional and which must be fixed at ratification; M4's `NOT_PRODUCED` label and P1's `NOT PRODUCED` determination are kept separate by name (§4.7).
- **(L1-5, new, blocking in L1's own judgment) The lattice crossing is not the closure's crossing.** m = 1 is the stability boundary of the *mean-field* closure. On the lattice, spatial correlations shift the absorbing state's stability boundary upward (the contact-process effect; mean field underestimates the threshold), so T-S1 as "within Δm of m = 1" would be expected to fail for a reason unrelated to the theory. v0.5 pre-registers **two crossing objects**, as pre-freeze §4.5 already required: the closure's m = 1 and a **lattice-level prediction m_lat from a pair-approximation closure of the same rule** (Appendix B, procedure stated; value DERIVED@FREEZE, to be computed in v0.6), and T-S1 tests the measured boundary against m_lat with m = 1 recorded as the closure's value and the shift m̂ − 1 as a secondary observable. This is the open derivation that stands between v0.5 and a freeze candidate.

**v0.4, 2026-10-21 — supersedes v0.3 (`694d753e22923054`, retained).** L2's acknowledgment of v0.3 ("REVISIONS SUBSTANTIALLY RESPONSIVE; FREEZABILITY REVIEW REMAINS OPEN") retained three items; all three addressed: (a) **M-P1 tolerances** — §3.4 now gives Δm as an explicit two-sided finite-size procedure with its provisional value (Appendix A), and the T-R1 band's one known weakness (near-critical fluctuation amplification is not modelled by σ_null) is stated with a proposed exclusion window rather than hidden; (b) **gap coverage of non-ramp archetypes** — new §6.4 states, archetype by archetype, which verdict rule adjudicates it and whether the width gap applies; (c) **stray DERIVED@BUILD markers** in §§3–4 re-tagged DERIVED@FREEZE where the quantity needs no instrument. No other change.

**v0.3, 2026-10-21 — supersedes v0.2 (`88bd567c09c33841`, committed at `21db4b8`, retained).** L2's contract review of 2026-10-21 ("DRAFT v0.2 NOT YET FREEZABLE"; three defects and one governance point, all accepted at L1), plus one defect L1 found while repairing them:
- **(L2-1) The guard gap is statistical, not worst-case.** E_min over all seed draws is zero; §6 now uses the exact law of E — with the 16/2/4 rule, E = w·(u₍₁₈₎ − u₍₃₎) and (u₍₁₈₎ − u₍₃₎) ~ **Beta(15, 6)** for 20 i.i.d. uniforms — with declared quantiles at ε = 0.01 (q₀.₀₁ = 0.468, q₀.₉₉ = 0.903), so each side of the gap contributes at most ε to the class error, against a cap of 0.10.
- **(L2-2) Skeleton low initialization** is a declared perturbation (ρ₀ = 0.02 of cells active, uniformly at random, declared seed), not the all-inactive absorbing state, which is the reference.
- **(L2-3) Freeze order.** A new marker **DERIVED@FREEZE** for quantities computable from the contract's closed-form inputs before any build (fixed-point tables, Δm, Δ_route, w_L, w_A, w_U, the gap margins); they are computed, tabulated in Appendix A and committed in the freeze commit; §6.3's refusal is executable. DERIVED@BUILD is kept for what needs the instrument (thresholds, masters).
- **(L2-G) PD5.** The "existence committed, value declared" status of W is the *held* PD5 amendment, not the ratified text; §2.10 and §4.5 now cite PD5 as written and name the amendment as a freeze prerequisite for Mike (§10, item 1).
- **(L1-4) The g = 0 null-relative detection boundary is not a transition detector here.** From §3.1 and §4.3: at μ = 0.2, η₀ ≈ 0.01, the realization's density exceeds the null's θ_P (≈ 0.058) at every sweep level (ρ* = 0.067 at m = 0.25) and meets it only near m ≈ 0.1. The detection boundary detects feedback, not the crossing. Consequences, now written in: the M4 instrument's verdicts are secondary observables with a pre-registered expected morphology (`no null-consistent phase` over the sweep) and **cannot bear on P1**; §4.7's sentence (2) is corrected; the P1 tests get their own evaluator (§4.10) with a known-answer qualification (§5.4); **W_res is a declared grid resolution** (3 pass-1 spacings) rather than a quantity derived from the map, which has no fluctuations to derive it from — design note R2 is revised accordingly; the `crossing_onset` archetype is withdrawn (its mixing width is not computable from the map).

**v0.2, 2026-10-20 — supersedes v0.1 (`696ec25e216fe32c`, committed at `3029f3c`, retained).** Two Gemini pre-freeze audit findings accepted at L1 triage (`GEMINI_F8_AUDIT_2026-10-20_RECEIVED.md`; triage record beside it): (F1) the floor is written **η_floor** throughout, per amendment §9 and the notation-scope table — v0.1's `h` collided with the C-domain reservation of h(t) for an external field; the committed floor value is **η₀**; (F2) w_A, the two-crossing offsets and the reentrant second onset now carry stated procedures or PROPOSED values. No other change.

**Status.** L1 draft v0.1, 2026-10-20, at Mike's word ("contract"). **Not frozen.** Nothing here binds until Mike ratifies a version; no ensemble, master, threshold or run is produced under this document before that. Review path: Gemini corpus audit (commission v3) on this draft → L2 contract packet under its own register → Mike's ruling → freeze.
**Lineage.** Successor mechanism class to Contract E1 (v0.8) and the E1-R amendment (`04058b21…`); governed by amendment §6–§10, L2's pre-freeze consultation §4 (`314b56cc…`), L2's dispositions of 2026-10-09 (`3f101a1b…`), 2026-10-20 diagnosis (`eaa694a9…`) and 2026-10-20 repair design (`7e52670a…`); design chamber record at `flights/mfa_fidelity/design/flight8/` (`ddf076b`). E1-R stage 1 is closed adversely and stays closed; its ensembles are burned; nothing of E1 carries by declaration.
**Markers.** `[RULED]` = Mike's ruling of record; `[PROPOSED]` = L1 value for Mike/L2, ratifies only at freeze; `[DERIVED@FREEZE]` = computed by a declared procedure from the contract's closed-form inputs **before freeze**, tabulated in Appendix A and committed in the freeze commit; `[DERIVED@BUILD]` = computed by a declared procedure when the instrument is built (needs the instrument: thresholds, caches, masters), before any guard master is drawn, committed with its identity.
**Notation.** Contract names per amendment §9; the notation-scope ruling v1 table governs every correspondence. **At first use: μ here is the deactivation rate — the Overview's lapse rate β; not the Overview's coherence coefficient μ(ρ).** g is the feedback gain (Overview g₀); **η_floor** the spontaneous-action floor **as a per-tick hazard** (Overview: the spontaneous term; the specification's η_floor is the per-tick *probability* 0.01 — same name, related by η_floor,C = −ln(1 − η_floor,S), a row added in §9); h(t), reserved for an external deterministic field, does not appear in this flight; ξ_ρ(t) the fluctuation term (specification η_MFA), identically zero in this flight; λ_i per-cell conduciveness (Overview Λ at the cell); d_i the Moore active fraction. Participation vocabulary per PD1–PD7; the Annex is not cited (TDA-000 §3).

---

## 1. Object and claim grammar

**1.1 The object.** Whether a lattice of intermittently participating cells, coupled only through local reinforcement of registration and subject to per-cell deactivation, realizes the first transition of Overview v1.8.1 §10 as a **structural** event: an exchange of stability of the inactive state at a pre-registered point, continuous, without hysteresis (the transcritical form), with the committed spontaneous floor producing the predicted rounded unfolding.

**1.2 P1 (primary endpoint, structural; Mike's ruling 2026-10-21, option (a)).** Five pre-registered tests on the two committed objects, none of which references the location of the crossing in m:
- **T-S1′ (a boundary exists).** In the skeleton-high sweep there is a lowest level m̂_c with surv ≥ 18 of 20 seeds and surv ≥ 18 at every level above it, and surv < 18 at some level below it (both phases inside the sweep).
- **T-S1c (continuity).** Above m̂_c the seed-median quasi-stationary density is non-decreasing in m and no level-to-level increase exceeds a declared fraction f_J = 0.25 `[PROPOSED]` of the branch's total range over the sweep — a jump test in the contract's own line-not-drama sense: it forbids a discontinuity, it does not demand steepness.
- **T-S2 (no hysteresis).** The boundary from the skeleton-low sweep, m̂_low, satisfies |m̂_low − m̂_c| ≤ Δm.
- **T-R1′ (rounded continuation).** In the realization sweep the seed-median density is positive at every level, non-decreasing in m, and continuous in the T-S1c sense; below m̂_c it is small and non-accumulating (≤ a declared fraction of its value at m̂_c + Δm) `[PROPOSED]`.
- **T-R2′ (steepest ascent above the boundary).** The realization's steepest ascent lies at or above m̂_c − Δm.
P1 is **PRODUCED** iff all five pass; **NOT PRODUCED** iff any fails validly (named causes in §4.11); **NOT DISTINGUISHED** iff any is unevaluable. P1 is never defined by a detection boundary. (The scientific determination `NOT PRODUCED` is distinct in name and jurisdiction from the M4 instrument's `NOT_PRODUCED` morphology label, §4.7.)

**1.2′ Closure-fidelity tier (pre-registered; reported, never P1).** (i) the boundary shift m̂_c − 1 (closure) and m̂_c − m_lat (pair, Appendix B); (ii) ρ̂ against ρ*_sk(m) and the pair branch above the boundary, and against ρ*(m; η₀) and the pair realization branch across the sweep, with the calibration-census band of §3.4 as the comparison width; (iii) the realization's steepest-ascent location against the closure's m_infl. Each is recorded as a signed deviation with its band; none passes or fails. These are the comparisons amendment §10 holds the lattice-versus-ODE question behind, and they are the evidence that question will be decided on.

**1.3 Secondary observables (finite-design; never P1).** (a) the morphology verdict of the M4 instrument (§4.4) on the realization sweep against the g = 0 null — **pre-registered expectation: `NOT PRODUCED (no null-consistent phase)`**, because the realization's density exceeds the null's at every sweep level (§4.9); the verdict is recorded and compared with that expectation as a consistency check on the instrument, and no verdict of this instrument bears on P1 (§4.7); (b) flicker run-length statistics near m = 1 across windows W (Mike's held probe candidate, PD rulings record) — recorded, not tested.

**1.4 What no result here may be represented as.** A confirmation or refutation of the theory (candidates produce or fail to produce); a statement about the heterogeneous lattice (§3.5, held); a statement about Regime II or Ψ; a reopening of any E1 verdict.

## 2. The substrate rule (frozen at ratification)

**2.1 Lattice and state.** L×L Moore lattice, L = 50 `[PROPOSED]` (N = 2,500, as E1), periodic boundaries as the frozen specification; x_i(t) ∈ {0,1}; tick Δt = 1.

**2.2 Bases and conduciveness.** v_i, u_i, r_i frozen for the run (Q disabled, Γ = 0; exogenous drive u_t = 0); **homogeneous** across cells `[RULED 2026-10-20]`: v_i = v̄, u_i = ū, r_i = r̄. λ_i = F(v̄, ū, r̄) = λ̄ by the frozen F dispatch, F_2_symmetric `[PROPOSED — the E1 form; Mike may rule F_LR]`.

**2.3 Local density.** d_i(t) = (number of active Moore neighbours of i at t)/8.

**2.4 Transition probabilities, evaluated from the state at t, applied simultaneously.**
- inactive → active: P_i = 1 − exp(−[η_floor + g·λ_i·d_i(t)]·Δt)
- active → inactive: P_i = 1 − exp(−μ·Δt)
No other term. The symmetric chain's drive/σ/overcrowding construction does not execute in this rule mode; that construction is named here as the wrong implementation so it cannot be inferred.

**2.5 Timing.** Synchronous two-phase advance (read all → one full-grid uniform draw → advance all), the frozen skeleton's order; one uniform per cell per tick from the run's RNG stream, derivation rule as E1 (seed-panel master → per-seed stream → per-level identifier under "%.6f" of m).

**2.6 Two committed objects.** Skeleton: **η_floor = 0**. Realization: **η_floor = η₀ = −ln(1 − 0.01) ≈ 0.0100503** `[RULED]`, the per-tick hazard whose single-tick activation probability equals the specification's η_floor = 0.01, so the Overview's spontaneous term has one committed image.

**2.7 Deactivation.** **μ = 0.2** `[PROPOSED]` (mean active persistence 1/(1 − e^(−μ)) ≈ 5.5 ticks; null stationary density a/(a + q) ≈ 5.2% with a, q as §2.9). The contract records the alternative candidates L1 priced (μ ∈ {0.05, 0.1, 0.3, 0.5}) and the fact that the realization's rounding half-width in m is 1.07 / 0.93 / 0.58 / 0.49 at those values and 0.68 at 0.2: the unfolding is soft at every plausible μ because it is governed by η₀/μ. This is a property of the committed theory objects, not a tuning.

**2.8 Feedback gain and the control coordinate.** g is not swept. The control coordinate is **m := g·λ̄·Δt / (1 − e^(−μΔt))** `[RULED via design note §3]`; a sweep level sets λ̄ (through the homogeneous bases) so that m takes the level's value, with g fixed at g = 1 `[PROPOSED]` (any fixed g > 0 is equivalent under the definition of m). The identity of a level is its m in exact integer micro-units.

**2.9 Null (g = 0).** The same rule with the feedback term removed and nothing else changed: activation 1 − e^(−η_floor·Δt), deactivation 1 − e^(−μΔt), same η_floor, same μ, same L, same timing, same seed derivation, same bases (inert). Each cell is an independent two-state Markov chain. Initialization: the chain's stationary distribution π₁ = a/(a + q), a = 1 − e^(−η_floor·Δt), q = 1 − e^(−μΔt), no burn-in `[RULED]`.

**2.10 Participation grammar (PD1–PD7).** A cell active at tick t has *registered* at t (PD7: a realized event); the participation window is **W = 1 tick** (PD5 as ratified: W is an architectural parameter, a declared timescale; the held PD5 amendment — existence committed, value declared — is a freeze prerequisite, §10 item 1); ρ counts registrations over the domain; persistence (the fourth question) is what the crossing is about. The lattice has no activated agent; a region activates.

## 3. The closure and the pre-registered predictions

**3.1 Mean-field map** (homogeneous bases, d_i = ρ):
ρ_{t+1} = (1 − ρ_t)·[1 − e^(−(η_floor + gλ̄ρ_t)Δt)] + ρ_t·e^(−μΔt).

**3.2 Skeleton prediction.** At η_floor = 0, ρ = 0 is a fixed point with multiplier J₀ = e^(−μΔt) + gλ̄Δt. **Crossing: J₀ = 1 ⇔ m = 1.** For m < 1 the inactive state is linearly stable (perturbations decay as J₀^t); for m > 1 it is unstable and a positive fixed point ρ*_sk(m) exists, continuous from zero, computed from the fixed-point equation and committed as a table over the sweep levels `[DERIVED@FREEZE]`. This is Overview §10's transcritical form in discrete time; gλ̄ ≈ μ (Λ* = β/g₀) is its Δt → 0 limit and is not the substrate equation. **Two crossing objects are pre-registered** (pre-freeze §4.5): the closure's crossing m = 1 above, and the **lattice-level crossing m_lat = 1.1414** predicted by the pair-approximation closure of the same rule (Appendix B) `[DERIVED@FREEZE, computed]`, which accounts for nearest-neighbour correlations the mean field ignores. Neither value is a P1 target: the design evidence of Appendix B §B.4 shows the lattice crossing near 1.40–1.45, beyond both. Both are closure-fidelity comparators (§1.2′).

**3.3 Realization prediction.** At η_floor = η₀ the map has a unique positive fixed point ρ*(m; η₀) for every m `[DERIVED@FREEZE]`, committed as a table; its departure from ρ*_sk is the rounding, maximal at m = 1. The branch's **inflection** — the m at which dρ*/dm is maximal — is **m_infl = 1.18** under the PROPOSED values `[DERIVED@FREEZE]`, not m = 1: the rounded transition's steepest ascent is displaced above the closure's crossing by the floor. m_infl is a closure-fidelity comparator (§1.2′); T-R2′ tests only that the steepest ascent lies at or above the boundary.

**3.4 Finite-size tolerances — declared design tolerances, not coverage guarantees (all `[DERIVED@FREEZE]`, Appendix A).** The skeleton's inactive state is absorbing on a finite lattice. The bracket Δm for T-S1/T-S2 is set by two **approximate** finite-size considerations, each named as an approximation:
- **below the boundary**, the linearized decay of the active count from the high initialization, J₀^t·N < 1 before the tail (J₀ = 1 − q(1 − m), q = 1 − e^(−μΔt), T_pre = 2,000): 1 − m ≥ ln N/(q·T_pre) = **0.0216**; this treats the decay as deterministic at its mean-field rate;
- **above the boundary**, a quasi-stationary population large enough that chance extinction within the run is unlikely: N·ρ*_sk(m) ≥ 50 expected active cells `[PROPOSED]` → m − 1 ≥ **0.030**; this is a criterion on an **expectation**, not a bound on survival probability over 3,000 ticks, and is declared as a design tolerance;
- **Δm = max(lower, upper) + one pass-1 spacing s** `[PROPOSED rule]` — provisionally **0.128**. Δm is used by T-S2 (hysteresis), T-R2′ and the fidelity tier; no P1 test brackets a predicted location.
For the **fidelity comparison (ii)** and for T-R1′'s monotonicity allowance, the band is ρ*(m; η₀) ± k_R·ŝ(m)·1.2533/√20, where ŝ(m) is the seed-to-seed standard deviation of the tail density at level m measured in the **calibration census** (§7.3 job 0: realization rule, all 24 levels, 20 seeds, its own master, run and committed before the canonical census and never reused), 1.2533/√20 is the standard error of a median of 20, and k_R = 3 `[PROPOSED]`. The band is therefore realization-side and level-specific, includes the near-critical levels, and is fixed before the canonical census runs; no tolerance is fitted to canonical data. **Precision declaration (fidelity tier):** the minimum resolvable lattice/closure deviation at level m is MDD(m) = k_R·ŝ(m)·1.2533/√20; the contract requires max_m MDD(m) ≤ 0.02 in density `[PROPOSED]`, else L or the window count is enlarged (re-declared) before the canonical census, so that the recorded shifts are informative. For **T-R2′**, the steepest ascent is located on the pass-1 grid by central differences of the seed-median ρ̂.

**3.5 Held.** The lattice-level spectral crossing (leading eigenvalue of gΔt·diag(λ_i)·A/8 + e^(−μΔt)I) coincides with m = 1 under homogeneous bases and is pre-registered here as the comparator for a heterogeneous-base successor job, not as a P1 test. The third-order lattice-versus-ODE comparison stays **held** (amendment §10) until Mike accepts §3.1–§3.2 as the bridge and L2 has reviewed §2.

## 4. The instrument (version `f8`, new package beside `e1`; nothing in `e1` modified)

**4.1 M1 — configuration and levels.** Pass-1 levels: n₁ = 24 `[PROPOSED]` values of m evenly spaced in exact integer micro-units over **[0.25, 2.50]** `[PROPOSED]` (spacing ≈ 0.0978; the crossing m = 1 is interior with ≥ 7 levels on each side; the skeleton's branch reaches ρ*_sk ≈ 0.4 at the top). Seed panel: 20 seeds drawn once by the E1 derivation rule from a new master `[DERIVED@BUILD]`. Run length and tail: T = 3,000 ticks, tail = last 1,000 ticks in 10 non-overlapping windows of 100 `[PROPOSED — E1's values; carried as scaffolding, re-declared here]`. Initializations for the skeleton: **low** = a fraction ρ₀ = 0.02 `[PROPOSED]` of cells active, chosen uniformly at random from a declared stream (the all-inactive state is absorbing at η_floor = 0 and is the *reference*, not an initialization); **high** = all active. Realization: stationary-null start (§2.9).

**4.2 M2 — run status and level label.** Per run: S_min = minimum window-mean density over the 10 tail windows; S_term = terminal-window mean. SUSTAINED iff S_min > θ_P; else NO_SUSTAINED iff S_term ≤ θ_T; else UNRESOLVED. Level label from the 20 seeds: S (≥ 16 sustained, ≤ 2 null), N (the reverse), M (≥ 4 each), else U — the frozen 16/2/4 rule, **retained as the secondary-observable classifier and re-qualified under M6; nothing about it is pre-approved** (L2 2026-10-20 answer 4).

**4.3 M3 — the Markov null and thresholds.** Per level, thresholds from the null of §2.9 at that level's η₀, μ, N, window: **θ_T** by the exact two-state transfer-matrix law of a single window's occupancy, convolved over N independent cells, at the declared quantile 1 − α_T `[PROPOSED α_T = 0.001]`; **θ_P** for S_min over ten windows by the **conservative familywise construction** — the per-window exact marginal threshold at quantile 1 − α_P/10 `[PROPOSED α_P = 0.001]`, so the familywise false-SUSTAINED rate is ≤ α_P `[RULED with L2 2026-10-20]`; its realized conservatism is **priced at qualification** by reporting the empirical null rejection rate against α_P in the M6 record; the named fallback is a separately qualified simulation threshold with explicit coverage, invoked only if M6 shows (b) insufficiently discriminating, and only as a new instrument version. Thresholds are cached per level (production/slice roles and the cache-qualification record as E1), identity committed before any audit.
Note: the null's stationary density is the same at every level (λ̄ is inert at g = 0), so θ_T, θ_P are level-independent in this flight; they are still cached per level so the record grammar carries unchanged.

**4.4 M4 — verdict function and router.** Rules 1, 2, 3, 4a, 4b, precedence 1 > 2 > 3 > 4 and a > b > c > d, router rows P2R-1…P2R-7 with 8 insertions in P2R-5/6 and 4 + 4 in P2R-4, exact integer-micro-unit arithmetic with round-half-to-even, and the collision fallback — **all carried verbatim from E1 v0.4 §5 / v0.8 C–E** (diagnosis: none implicated). **Rule 4c is replaced:**
> **4c (F8).** NOT DISTINGUISHED (boundary unresolved at declared resolution W_res) iff, after pass 2, the measured width of the band — m(lowest confident S) − m(highest confident N) on the final level set — exceeds **W_res** (§4.5). Otherwise 4d: LOCATED, bracket [m₋, m₊].

**4.5 W_res — the declared resolution.** **W_res = 3 pass-1 spacings = 293,478 micro-units of m** `[PROPOSED]` (the resolution E1's count-3 rule intended, stated in physical units and independent of the insertion count). It is a declaration in the sense PD5 gives W: the instrument commits that a transition region narrower than W_res is bracketed and one wider is reported unresolved at this resolution. It is **not** derived from the closure: the map has no fluctuations, so a "predicted mixing window" from it would be fictitious precision (v0.2's §4.5 and design note R2 are withdrawn on this point). No ensemble, sweep or audit enters it.

**4.6 The residual dependence of the width criterion on routing (contract clause; L2 2026-10-20 answer 1).** For a ramp-type morphology with true uncertain extent E (the m-interval over which the 16/2/4 rule applied to the sweep's own seed thresholds yields neither N nor S), the measured width satisfies E ≤ measured ≤ E + δ_N + δ_S, where δ_N, δ_S are the final-level spacings straddling the true endpoints after routing (fallback included). The lower side is exact; the upper holds because inserted levels can only add confident labels inside the band. The relation is proved for the monotone ramp label process (one N→S transition in m); for the DIP classes a separate sufficient condition is used (§6.4); it is not claimed for every M6 morphology. The maximum of δ_N + δ_S over the frozen grid, insertion count and fallback rule is a declared number `[DERIVED@FREEZE]`, and it is the slack the archetype gap (§6.2) absorbs. (Evidence of the form on E1's burned draws: `extent_bound.py`, `1f60bcb0…`, design chamber; it establishes the property of the rule, not any Flight 8 value.)

**4.7 Verdict grammar (line-not-drama, F8 form).** No criterion anywhere in §4 references jump size, slope, amplitude monotonicity or adjacent-level separation. (1) `NOT DISTINGUISHED (boundary unresolved at declared resolution W_res)` is an instrument statement — the band after refinement is wider than the instrument declared it can bracket — never a statement that a transition is absent, never adverse to P1; the package grammar records it valid-but-not-located. (2) **No verdict of the M4 instrument bears on P1 in this flight** (§4.9): P1 is adjudicated by §4.10 alone. Within the M4 instrument, the `NOT_PRODUCED` label (rules 1–3) describes the morphology of the null-relative detection and none of its rules references width; it is compared with the pre-registered expectation of §1.3(a). It is never written `NOT PRODUCED` and never enters the P1 determination. (3) An onset wider than W_res is unresolved at this resolution; the remedy is a finer pass-1 grid or more insertions in a successor stage, not a scientific reading. (4) A different W_res is a different instrument, not a different theory.

**4.8 M5 — closure and census.** The map (§3.1), its two fixed-point tables, the finite-size predictions and tolerances (§3.4), and the dense reference census over the sweep (701 levels `[PROPOSED — E1's count]`) as the reference of record; reference-stability over alternative templates as E1.

**4.10 M7 — records, package, readiness.** The E1-R package grammar **carries unchanged** (amendment §5): completeness = loads, validates, satisfies its declared predicate, adverse content included; *package complete* and *production ready* computed separately; apparatus and qualification prerequisites require passage, scientific prerequisites valid completion; branch stops only if expressly declared (this version declares none). Every record names its authorization, the stage identity and the instrument version.

**4.9 Why the detection boundary is not the transition (stated so no reader infers otherwise).** Under §2.9 the null removes feedback; any g > 0 adds activation and only adds it, so the realization's stationary density exceeds the null's at every m > 0. With the PROPOSED values, the null's stationary density is 0.0523 and its per-window-mean fluctuation ≈ 0.0014, so θ_P ≈ 0.058 at α_P; the realization's branch is 0.067 at m = 0.25 and crosses θ_P near m ≈ 0.1 `[DERIVED@FREEZE, Appendix A]`. The g = 0-null-relative boundary therefore locates the onset of *feedback*, an order of magnitude below the crossing at m = 1, and the M4 instrument's expected verdict over the sweep is rule 2, `no null-consistent phase`. This is the imperfect-bifurcation fact of Overview §10 ("registration occurs at every value of Λ") seen through a feedback-removed null; it is pre-registered here as the expected secondary morphology and is the reason P1 is structural.

**4.11 M-P1 — the structural evaluator (complete algorithm).**
*Populations.* Three sweeps, each 24 levels × 20 seeds from the canonical seed panel, each under its own authorization: skeleton-high (all active), skeleton-low (ρ₀ = 0.02 random, declared stream), realization (stationary-null start). A fourth, the calibration census (§7.3 job 0), uses a separate master and is not scored.
*Per run.* survival = tail-window active count > 0 at every tail window (skeleton; the reference is exact zero, so no floor is needed); ρ̂ = tail-window mean density. A run that goes extinct is a valid observation (survival = 0, ρ̂ = 0), never "missing". A run that halts on an apparatus error is **unevaluable**; a level with any unevaluable seed is unevaluable; an unevaluable level inside a test's domain makes that test NOT DISTINGUISHED (apparatus), recorded with the halt key.
*T-S1′.* For the skeleton-high sweep, surv(m) = number of surviving seeds at level m. m̂_c = the lowest level with surv ≥ 18 `[PROPOSED]` such that surv ≥ 18 at every level above it. Cases: (i) no level has surv ≥ 18 → fails validly, cause `no active phase in sweep`; (ii) surv ≥ 18 at every level including the lowest → fails validly, cause `no inactive phase in sweep`; (iii) surv ≥ 18 at some level but not at every level above it → NOT DISTINGUISHED, cause `non-monotone survival`; (iv) otherwise pass, m̂_c recorded. Ties cannot arise.
*T-S1c.* Above m̂_c, med(m) non-decreasing and every increase ≤ f_J × (med(m_max) − med(m̂_c)); a decrease beyond the calibration band fails validly, cause `non-monotone branch`; a jump fails validly, cause `discontinuity at <level>`.
*T-S2.* Same procedure on the skeleton-low sweep giving m̂_low, same cases; pass iff |m̂_low − m̂_c| ≤ Δm. A saddle-node signature (m̂_low > m̂_c + Δm) fails validly, cause `hysteresis`.
*T-R1′.* For the realization sweep, med(m) = seed-median ρ̂ at level m: positive at every level (cause `realization extinct at <level>` otherwise), non-decreasing within the calibration band ŝ(m)·1.2533/√20 (cause `non-monotone realization`), continuous in the T-S1c sense (cause `discontinuity at <level>`), and med(m) ≤ f_B × med(m̂_c + Δm) for every m < m̂_c − Δm with f_B = 0.5 `[PROPOSED]` (cause `accumulation below the boundary`). The fidelity comparison of med(m) with ρ*(m; η₀) ± k_R·ŝ(m)·1.2533/√20 is recorded per §1.2′ and is not scored.
*T-R2′.* m̂_infl = the pass-1 level at which the central difference [med(m₊) − med(m₋)]/(m₊ − m₋) is maximal (interior levels only; ties → the lower level); pass iff m̂_infl ≥ m̂_c − Δm (cause `steepest ascent below the boundary`); if the maximum is at the sweep's edge, NOT DISTINGUISHED, cause `inflection at sweep edge`. The comparison with m_infl is recorded per §1.2′.
*Known-answer qualification (§5.4).* Synthetic sweeps from the map with declared noise, including: a continuous crossing anywhere in the sweep interior that must pass all five; a crossing outside the sweep (both sides) that must fail T-S1′ with its cause; a branch with a jump of 2·f_J that must fail T-S1c; a hysteretic pair (low/high differing by 2·Δm) that must fail T-S2; a realization that accumulates below the boundary (2·f_B) that must fail T-R1′; a steepest ascent placed 2·Δm below the boundary that must fail T-R2′. These test the evaluator's implementation; they do not validate any closure against the lattice. Pass requires every must-pass case to pass and every must-fail case to fail with its named cause, on ≥ 95 of 100 replicates each `[PROPOSED]`.

## 5. Morphology audit (M6) and the archetype table

**5.1 Architecture carries.** Design and held-out ensembles, 500 sweeps per class `[PROPOSED]`, applicable error (scientific-intent classes: final ND; ND-intent: final LOCATED or NP), one-sided CP upper 95% ≤ **0.10** `[PROPOSED — E1's cap, re-declared]`, class `complete_pass` = 500/500/0 halts and cap clears, `ensemble_pass` = every class complete, qualification = design AND held-out joined mechanically. Generator: regime assignment per seed by fixed per-sweep uniforms against a class-specific profile in m; runs under each regime generated from the **Markov null** (NULL), the realization's own rule at the level's m (SUSTAINED), or the DIP construction (UNRESOLVED) — the generator declaration and its identity are committed before any master is drawn.

**5.2 The archetype table (F8)** — intended verdicts and declared width ranges in micro-units of m. Widths are set by the gap rule of §6.2, which is evaluated analytically before the table is frozen:

| Archetype | Intended | Profile | Declared width range |
|---|---|---|---|
| `gentle_onset` | LOCATED | linear ramp | w ∈ [w_A, 0.9·w_L] `[DERIVED@FREEZE]` |
| `abrupt_onset` | LOCATED | linear ramp | w ∈ [0, w_A], where **w_A = s / q₁₋ε** (the width whose E is below one pass-1 spacing s with probability 1 − ε) `[PROPOSED rule; value DERIVED@FREEZE]` |
| `persistent_nonstationary_high_m` | LOCATED | ramp + drift/oscillation of the sustained level | w ∈ [0, w_A] |
| `nonmonotone_amplitude` | LOCATED | ramp + attenuation above onset | w ∈ [0, w_A] |
| `no_sustained_anywhere` | NOT_PRODUCED (no sustained phase) | null everywhere | — |
| `no_null_consistent_anywhere` | NOT_PRODUCED (no null-consistent phase) | sustained everywhere (reinterpreted: a realization that never decays — the skeleton's absorbing state is never reached) | — |
| `two_resolved_crossings` | NOT_PRODUCED (order violation) | N-S-N-S | second and third crossings at onset + [4, 7] pass-1 spacings `[PROPOSED]` (E1's 110–220k on a 30.4k spacing) |
| `reentrant` | NOT_PRODUCED (order violation) | N-S-N | return to null at onset + U[4, 6] pass-1 spacings `[PROPOSED]` (E1's 120–200k) |
| `off_band_mixture` | NOT_DISTINGUISHED (off-boundary mixture) | ramp + one mixed level below the band | as gentle |
| `off_band_unresolved` | NOT_DISTINGUISHED (off-boundary unresolved) | ramp + three DIP levels below the band | as abrupt |
| `wide_mixed_boundary` | NOT_DISTINGUISHED (boundary unresolved at W_res) | linear ramp | w ∈ [1.1·w_U, 1.6·w_U] `[DERIVED@FREEZE]` |
| `unresolved_heavy_boundary` | NOT_DISTINGUISHED (boundary unresolved at W_res) | DIP across the band | w ∈ [1.1·w_U, 1.6·w_U] |

**5.4 Known-answer qualification of M-P1.** Before any canonical job, M-P1 (§4.10) is run on synthetic sweeps generated from the map itself with declared finite-size noise and declared true crossings m_c ∈ {0.8, 1.0, 1.25} `[PROPOSED]`, 100 sweeps each `[PROPOSED]`; it must recover m_c within Δm on ≥ 95 of 100 and pass T-S2 on all. Recorded as an apparatus prerequisite in the governance record (passage required).

**5.3 Masters.** Two fresh masters (design, held-out) and the pricing master are **drawn by a declared rule from a declared seed after the table, W_res and the generator are frozen**, their values committed with the freeze commit's identity, and never reused across instrument versions. The E1 masters 202609221/2/3 are retired.

## 6. The guard gap (pre-registered, statistical; L2 2026-10-21 finding 1)

**6.1 The law of E.** For a ramp-type archetype of declared width w, with the 16/2/4 label rule a level is confident N while at most 2 of the 20 seeds are sustained and confident S once at least 18 are; the true uncertain extent is therefore E = w·(u₍₁₈₎ − u₍₃₎) for the sweep's 20 i.i.d. regime uniforms, and **(u₍₁₈₎ − u₍₃₎) ~ Beta(15, 6)** exactly (the spacing between the 3rd and 18th order statistics of 20 uniforms). Its ε-quantiles are closed-form; at **ε = 0.01** `[PROPOSED]`: q_ε = 0.4679, q₁₋ε = 0.9025 (mean 0.7143). The worst case over draws is E = 0 and is not usable; the gap is stated in quantiles, and ε is the probability each side contributes to a class's error budget (cap 0.10).

**6.2 The rule.** With s the pass-1 spacing and Δ_route the routing slack bound (§4.6), **certified by exhaustive enumeration** of every band (lo, hi) of the F8 pass-1 grid (276 index pairs): for each, the eight round-half-even interior insertions are computed, candidates that collide with a pass-1 level are removed (the worst case for gaps, dominating both fallback moves and drops), and the largest final-level gap taken; Δ_route(B) = 2 × that maximum for bands of B spacings. Locatable classes have B ≤ ⌊E/s⌋ + 2 ≤ 4 under their declared widths, so **Δ_route = Δ_route(4) = 86,958** (Appendix A lists all B). Collisions occur only at B ∈ {3, 6, 9}, so the fallback branch is live and covered.
- locatable archetypes: **w_L = (W_res − Δ_route) / q₁₋ε** — a ramp of width ≤ w_L has E + Δ_route ≤ W_res with probability ≥ 1 − ε;
- unresolvable archetypes: **w_U = W_res / q_ε** — a ramp of width ≥ w_U has E > W_res with probability ≥ 1 − ε;
- abrupt: **w_A = s / q₁₋ε**.
All `[DERIVED@FREEZE]`, Appendix A. Under the PROPOSED values: s = 97,826 (97,827 at two gaps, by rounding); W_res = 293,478; B = 4; Δ_route = 86,958; **w_L = 228,831 (2.34 s); w_A = 108,394 (1.11 s); w_U = 627,224 (6.41 s); w_U / w_L = 2.74** (provisional, computed with the four-decimal quantiles shown; the freeze value uses the exact quantiles).****

**6.3 Check at freeze.** w_L and w_U are the *boundary* widths; declared archetype ranges sit strictly inside them (locatable ramps ≤ 0.9·w_L; unresolvable ramps ≥ 1.1·w_U `[PROPOSED]`). Appendix A lists the values and the two margins evaluated at the declared range endpoints — M_L = W_res − q₁₋ε·(0.9·w_L) − Δ_route and M_U = q_ε·(1.1·w_U) − W_res — and the freeze commit is refused if either is non-positive or if any declared archetype width falls outside its range. The check uses no ensemble.

**6.4 Coverage of the archetype table by rule (which criterion adjudicates each class; the width gap applies only where stated).**

| Archetype | Adjudicating rule | Width gap applies? |
|---|---|---|
| `gentle_onset`, `abrupt_onset`, `persistent_nonstationary_high_m`, `nonmonotone_amplitude` | 4c/4d on the ramp's band | **yes** — ramp E ~ w·Beta(15, 6); declared widths ≤ 0.9·w_L (gentle) or ≤ w_A (abrupt-kind); the temporal and amplitude modulations act on the sustained runs, not on the regime assignment, so E's law is unchanged |
| `wide_mixed_boundary` | 4c | **yes** — ramp, declared widths ≥ 1.1·w_U |
| `unresolved_heavy_boundary` | 4c | **yes, by a separate sufficient condition** (not the ramp breakpoint definition): every seed's run at every level inside the declared window is DIP, which M2 labels UNRESOLVED and the level rule labels U with certainty; no confident label can occur inside the window, so the post-pass-2 band contains the whole window and its measured width is ≥ w; declared widths ≥ 1.1·w_U > W_res therefore give rule 4c with certainty, independent of the seed uniforms |
| `off_band_mixture` | **4a** (an M level outside the band) | no — the mixed level is M iff 4 ≤ K ≤ 16 of 20 seeds are sustained, K ~ Binomial(20, π). **Exact risk P(K ≤ 3 or K ≥ 17):** 0.1071 at π = 0.3 (v0.4's range was defective; L2's finding), 0.0052 at 0.45, 0.0026 at 0.5. **Declared range π ∈ [0.45, 0.55]** `[PROPOSED]`, worst-case risk 0.0052 ≤ ε; this is the class's only design error source |
| `off_band_unresolved` | **4b** (three adjacent U levels outside the band) | no — the DIP levels are U deterministically |
| `two_resolved_crossings`, `reentrant` | **rule 1** (order violation) | no — adjudicated at pass 1. Crossings are abrupt (width 0), so every pass-1 level is deterministically N or S; with the onset drawn from [m_min + s, m_max − 8s] and offsets of [4, 7] spacings (two crossings) or a return at U[4, 6] spacings (reentrant), every region contains ≥ 1 pass-1 level **with certainty** — coverage is by construction of the draw ranges, probability 1 |
| `no_sustained_anywhere` | **rule 3** (top level confident N) | no |
| `no_null_consistent_anywhere` | **rule 2** (bottom level confident S) | no |

## 7. Qualification, authorization, canonical jobs

**7.1 Order.** Appendix A computed (DERIVED@FREEZE) and §6.3 check passed → freeze (this contract, ratified, Appendix A in the same commit) → instrument version identity → M3 cache built and qualified → M-P1 known-answer qualification (§5.4) → masters drawn (§5.3) → M6 design audit → M6 held-out audit → `m6_audit_qualification` → **passage of both qualifications required** → canonical scientific jobs. An adverse M6 closes the stage, as in E1-R; no same-stage repair.

**7.2 Authorization grammar.** As E1-R: each canonical job runs only under a Mike-issued authorization record naming the stage, the jobs and the tranche flags; the registry is append-only.

**7.3 Canonical jobs, in order (condition 3 of Mike's 2026-10-15 ruling).**
0. `calibration_census` — realization rule, all levels, 20 seeds under a **separate master** declared at freeze; produces ŝ(m) for T-R1's band and the MDD check (§3.4); committed before job 3 runs; never scored, never reused.
1. `skeleton_census` — η_floor = 0, low and high initializations, full sweep; evaluates T-S1′, T-S1c and T-S2; records fidelity tier (i)–(ii). **First canonical scientific job**: if the instrument misses the exact crossing it is known before the realization runs.
2. `skeleton_stability` — alternative templates and seed panels; class reproduced within Δm.
3. `realization_census` — η_floor = η₀, stationary-null start; evaluates T-R1′ and T-R2′; records fidelity tier (ii)–(iii) and the M4 morphology label against §1.3(a).
4. `realization_stability`, `projection_sweeps`, `tolerance_ensembles`, `tolerance_program`, `resource_benchmark`, `calibration_tranche`, `stage1_package` — E1-R's grammar and record kinds.
5. **Held** (successor stage): heterogeneous-base run against §3.5's spectral comparator; third-order lattice-versus-ODE comparison.

**7.4 Readiness.** Production readiness is derived mechanically from the governance record's prerequisites; `m6_audit_qualification` pass is a prerequisite; no production without it.

## 8. Declarations table (to be completed at build; every row carries an identity at freeze)

| Declaration | Value | Marker |
|---|---|---|
| L, N | 50, 2,500 | PROPOSED |
| F dispatch | F_2_symmetric | PROPOSED |
| η₀ (realization floor hazard) | −ln(0.99) ≈ 0.0100503 | RULED |
| μ | 0.2 | PROPOSED |
| g | 1 (not swept) | PROPOSED |
| sweep range in m | [0.25, 2.50] | PROPOSED |
| n₁ pass-1 levels | 24 | PROPOSED |
| T, tail, window | 3,000 / 1,000 / 100 × 10 | PROPOSED |
| W (participation window) | 1 tick | DECLARED (PD5) |
| null initialization | stationary, no burn-in | RULED |
| α_T, α_P | 0.001, 0.001 (familywise) | PROPOSED |
| ρ*_sk(m), ρ*(m; η₀) tables | — | DERIVED@FREEZE (App. A) |
| Δm (T-S1/T-S2 bracket) | max(ln N/(q·T_pre), m−1 at N·ρ*_sk = 50) + s | PROPOSED rule; value DERIVED@FREEZE (0.128 provisional) |
| T-R1 band | ρ* ± k_R·ŝ(m)·1.2533/√20, ŝ from the calibration census | PROPOSED rule |
| MDD ceiling | max_m MDD(m) ≤ 0.02 | PROPOSED |
| m_infl (T-R2 target) | inflection of ρ*(m; η₀) | DERIVED@FREEZE (1.18 provisional) |
| m_lat (fidelity comparator) | pair-approximation closure, Appendix B | DERIVED@FREEZE (1.1414, computed) |
| f_J (continuity jump fraction) | 0.25 | PROPOSED |
| f_B (below-boundary accumulation fraction) | 0.5 | PROPOSED |
| off_band_mixture π range | [0.45, 0.55] | PROPOSED |
| calibration master | drawn at freeze, separate from all others | DERIVED@BUILD |
| QS survival criterion | N·ρ*_sk(m) ≥ 50 | PROPOSED |
| ρ₀ (skeleton low initialization) | 0.02 | PROPOSED |
| k_R (T-R1 band multiplier) | 3 | PROPOSED |
| W_res | 3 pass-1 spacings = 293,478 | PROPOSED (declared resolution) |
| ε (gap quantile) | 0.01 | PROPOSED |
| Δ_route | exhaustive grid enumeration, B = 4 → 86,958 | DERIVED@FREEZE (certified) |
| w_L, w_A, w_U; declared ranges; margins | 228,831 / 108,394 / 627,224; gentle ≤ 205,948, wide ≥ 689,946; M_L = 20,652, M_U = 29,348 | DERIVED@FREEZE (§6.2–6.3) |
| M-P1 known-answer: m_c set, sweeps, pass rule | {0.8, 1.0, 1.25}; 100; ≥ 95/100 and T-S2 on all | PROPOSED |
| two-crossing offsets; reentrant return | [4, 7] spacings; U[4, 6] spacings | PROPOSED |
| cap, CP confidence, sweeps/class | 0.10, 0.95 one-sided, 500 | PROPOSED |
| masters (design, held-out, pricing) | drawn after freeze | DERIVED@BUILD |
| instrument version string | `f8_stage1_v1` | PROPOSED |

## 9. Notation rows added to the translation table (append-only; the table governs)

| Object | O — Overview v1.8.1 | C — this contract | S — frozen spec v0.4 | Nature |
|---|---|---|---|---|
| Control coordinate | Λ/Λ* (implicit) | m = gλ̄Δt/(1 − e^(−μΔt)) | (none) | C-only; m = 1 ⇔ Λ = Λ* in the homogeneous closure |
| Spontaneous floor (this flight) | spontaneous term | **η_floor**, a per-tick hazard; committed value η₀ | **η_floor** = 0.01, a per-tick probability | identity of meaning, name shared, units differ: η_floor,C = −ln(1 − η_floor,S) |
| Skeleton / realization | spontaneous term removed / restored | η_floor = 0 / η_floor = η₀ | — / η_floor = 0.01 | identity of meaning |
| Resolution | — | W_res (declared, §4.5) | — | C-only; the status PD5's held amendment would give W |

## 10. Freeze prerequisites outside this document (for Mike)
1. **PD5 amendment**: ratify the held amendment (W: existence committed, value declared) — or strike §4.5's analogy and leave W_res as a bare declaration. L1 recommends ratifying; it was Mike's own held candidate of 2026-10-10.
2. **Notation table rows (§9)** appended to `NOTATION_SCOPE_RULING_v1.md` as v1.1 (append-only) in the freeze commit or before it.
3. **Appendix A** computed and committed in the freeze commit. *Provisional versus fixed:* every value in Appendix A marked "provisional" is shown for review under the PROPOSED inputs and becomes fixed only when the freeze commit's Appendix A names it; m_lat (Appendix B) has no provisional value yet and is the one quantity whose derivation is still open.
4. **Appendix B** computed (v0.6); L2's review of it and of the re-tiered claim grammar precedes the freeze candidate.

## 11. What this contract does not claim

Nothing about the heterogeneous lattice, Regime II, Ψ, Q, or any E1 verdict. No value in §8 marked PROPOSED or DERIVED@BUILD is of record until the freeze commit names it. The design chamber's pricing on E1's burned ensembles established the form of 4c and the need for a gap; no number from it appears here. Mike rules; L2 reviews; Gemini audits for consistency only.

## Appendix A — DERIVED@FREEZE table (to be computed by the declared procedures and committed in the freeze commit; provisional values under the PROPOSED inputs shown for review, not of record)

| Quantity | Procedure | Provisional value |
|---|---|---|
| s (pass-1 spacing) | (2.50 − 0.25)/23 in micro-units | 97,826 |
| ρ*_sk(m) | fixed point of §3.1 at η_floor = 0 | 0 for m ≤ 1; 0.305 (1.5), 0.457 (2.0), 0.548 (2.5) |
| ρ*(m; η₀) | fixed point at η₀ | 0.067 (0.25), 0.091 (0.5), 0.199 (1.0), 0.362 (1.5), 0.482 (2.0), 0.562 (2.5) |
| null stationary density, σ_null | a/(a+q); Markov-chain window-mean variance at N = 2,500, window 100 | 0.0523; ≈ 0.0014 |
| θ_P (familywise, α_P = 0.001) | §4.3 | ≈ 0.058 (provisional Gaussian; exact at build) |
| m at which ρ*(m; η₀) = θ_P | §4.9 | ≈ 0.1 (below the sweep) |
| Δm | §3.4: max(0.0216, 0.030) + s | **0.128** (1.3 s); bracket [0.872, 1.128] |
| Beta(15, 6) quantiles, ε = 0.01 | closed form | 0.4679 / 0.9025 |
| Δ_route(B), B = 1…9 | §6.2 exhaustive | 21,740; 43,480; 65,218; **86,958**; 108,696; 130,436; 152,174; 173,914; 195,654 (collisions at B = 3, 6, 9) |
| m_infl | argmax dρ*/dm | 1.18 (provisional) |
| m_lat | Appendix B | 1.1414 (μ = 0.2) |
| off_band_mixture risk | P(K ≤ 3 or K ≥ 17), π ∈ [0.45, 0.55] | ≤ 0.0052 |
| rule-1 class grid coverage | by construction of draw ranges | 1 |
| w_L, w_A, w_U | §6.2 | 228,831; 108,394; 627,224 |
| margins M_L, M_U | §6.3 at the declared range endpoints | M_L = 293,478 − 0.9025·205,948 − 86,958 = 20,652 > 0; M_U = 0.4679·689,946 − 293,478 = 29,348 > 0 |

## Appendix B — the pair-approximation closure and the lattice crossing (computed; `pair_approx.py` `85909320…`, `lattice_check.py` `92a3e8d4…`)

**B.1 Why a second closure.** The map of §3.1 assumes every cell sees the global density. On the Moore lattice an active cell's neighbours are more likely active than average (its own offspring), so the effective feedback near the absorbing state is weaker than mean field assumes and the stability boundary sits above m = 1.

**B.2 Derivation from §2.4 (synchronous, z = 8).** Variables ρ = P(active), p_AA = P(Moore pair both active); pair closure q_{A|A} = p_AA/ρ, q_{A|I} = (ρ − p_AA)/(1 − ρ); p_AI = ρ − p_AA, p_II = 1 − 2ρ + p_AA; a_k = 1 − exp(−(η_floor + gλ̄·k/8)); q_d = 1 − e^(−μ). One synchronous tick, all draws independent given the state:
- ρ′ = ρ(1 − q_d) + (1 − ρ)·E[a_K], K ~ Bin(8, q_{A|I});
- p_AA′ = p_AA(1 − q_d)² + 2·p_AI·(1 − q_d)·E[a_{1+K₇}] + p_II·(E[a_{K₇}])², K₇ ~ Bin(7, q_{A|I}) — (A,A) both survive; (A,I) the active survives and the inactive, with its partner known active and seven others, activates; (I,I) both activate with seven others each, neighbour sets treated as independent (the closure).
At η_floor = 0 the absorbing state (0, 0) is fixed; linearizing with a₁ = 1 − exp(−gλ̄/8): ρ′ = (1 − q_d + 8a₁)ρ − 8a₁p_AA; p_AA′ = 2(1 − q_d)a₁ρ + [(1 − q_d)² − 2(1 − q_d)a₁]p_AA. **m_lat** is the m (gλ̄ = m·q_d) at which the leading multiplier of this 2×2 map equals 1, by bisection. The nonlinear map's fixed points give the pair branches.

**B.3 Values (μ = 0.2, η₀ = −ln 0.99).** m_lat = **1.1414** (multiplier 0.9789 at m = 1); over μ ∈ {0.05, 0.1, 0.3, 0.5}: 1.1428, 1.1425, 1.1398, 1.1353. Pair skeleton branch ρ* = 0.051 (1.2), 0.242 (1.5), 0.423 (2.0), 0.526 (2.5) against mean-field 0 / 0.305 / 0.457 / 0.548; pair realization branch 0.066 (0.25), 0.088 (0.5), 0.176 (1.0), 0.328 (1.5), 0.457 (2.0), 0.544 (2.5).

**B.4 Design evidence — the lattice itself (NONCANONICAL; L1's own seeds 0–5; not a validation, not a calibration; pre-freeze).** Skeleton on the 50×50 periodic Moore lattice, synchronous, high initialization, T = 3,000, tail 1,000: survival 0/6 at m ∈ {1.00, 1.10, 1.15, 1.20, 1.30, 1.35}; **1/6 at 1.40** (tail densities 0.033, 0.008, else 0); **6/6 at 1.45** (0.040–0.081); 6/6 at 1.50 (0.110–0.131). The lattice crossing is ≈ 1.40–1.45: above the pair value by 0.26–0.31 (> 2Δm) and above the closure's 1 by ≈ 0.4; the lattice's density at m = 1.5 (≈ 0.12) is far below both branches. **This is why neither closure is a P1 target** (Mike's ruling 2026-10-21, option (a)): the closures capture the structure — continuous exchange of stability from an absorbing state, no jump — and not the location or amplitude, as is known for pair closures of local stochastic processes. The shifts are the closure-fidelity tier's object (§1.2′). This evidence enters no gate, no tolerance and no archetype; it decided the claim grammar before freeze and is recorded for that reason.

**B.5 Known-answer scope.** M-P1's synthetic sweeps are generated from the map (or the pair map) with declared noise; they test the evaluator's implementation only and establish nothing about either closure's accuracy on the lattice.

*L1, v0.1 and v0.2 2026-10-20; v0.3–v0.6 2026-10-21.*
