# Contract F8 — Flight 8: the first transition under the hazard rule (v0.1, DRAFT)

**Status.** L1 draft v0.1, 2026-10-20, at Mike's word ("contract"). **Not frozen.** Nothing here binds until Mike ratifies a version; no ensemble, master, threshold or run is produced under this document before that. Review path: Gemini corpus audit (commission v3) on this draft → L2 contract packet under its own register → Mike's ruling → freeze.
**Lineage.** Successor mechanism class to Contract E1 (v0.8) and the E1-R amendment (`04058b21…`); governed by amendment §6–§10, L2's pre-freeze consultation §4 (`314b56cc…`), L2's dispositions of 2026-10-09 (`3f101a1b…`), 2026-10-20 diagnosis (`eaa694a9…`) and 2026-10-20 repair design (`7e52670a…`); design chamber record at `flights/mfa_fidelity/design/flight8/` (`ddf076b`). E1-R stage 1 is closed adversely and stays closed; its ensembles are burned; nothing of E1 carries by declaration.
**Markers.** `[RULED]` = Mike's ruling of record; `[PROPOSED]` = L1 value for Mike/L2, ratifies only at freeze; `[DERIVED@BUILD]` = computed by a declared procedure from `[RULED]`/`[PROPOSED]` inputs when the instrument is built, before any guard master is drawn, and committed with its identity.
**Notation.** Contract names per amendment §9; the notation-scope ruling v1 table governs every correspondence. **At first use: μ here is the deactivation rate — the Overview's lapse rate β; not the Overview's coherence coefficient μ(ρ).** g is the feedback gain (Overview g₀); h the spontaneous-action floor (Overview: the spontaneous term; specification: η_floor's image); ξ_ρ(t) the fluctuation term (specification η_MFA), identically zero in this flight; λ_i per-cell conduciveness (Overview Λ at the cell); d_i the Moore active fraction. Participation vocabulary per PD1–PD7; the Annex is not cited (TDA-000 §3).

---

## 1. Object and claim grammar

**1.1 The object.** Whether a lattice of intermittently participating cells, coupled only through local reinforcement of registration and subject to per-cell deactivation, realizes the first transition of Overview v1.8.1 §10 as a **structural** event: an exchange of stability of the inactive state at a pre-registered point, continuous, without hysteresis (the transcritical form), with the committed spontaneous floor producing the predicted rounded unfolding.

**1.2 P1 (primary endpoint, structural)** — three pre-registered tests on two committed objects:
- **Skeleton** (h = 0): **T-S1** the inactive state loses stability at m = 1 within a declared bracket Δm; **T-S2** the boundary is the same from low- and high-activity initializations within Δm (no hysteresis; a saddle-node signature fails).
- **Realization** (h = h₀): **T-R1** the measured quasi-stationary density ρ̂(m) lies within a declared tolerance band of the map's h₀-rounded branch ρ*(m; h₀) across the sweep.
P1 is **PRODUCED** iff T-S1, T-S2 and T-R1 all pass; **NOT PRODUCED** iff any fails validly; **NOT DISTINGUISHED** iff any is unevaluable at the declared resolution (§4.6). P1 is never defined by a detection boundary.

**1.3 Secondary observables (finite-design; never P1).** (a) the null-relative detection boundary located by the morphology instrument (§4), the successor of E1's LOCATED; (b) flicker run-length statistics near m = 1 across windows W (Mike's held probe candidate, PD rulings record) — recorded, not tested.

**1.4 What no result here may be represented as.** A confirmation or refutation of the theory (candidates produce or fail to produce); a statement about the heterogeneous lattice (§3.5, held); a statement about Regime II or Ψ; a reopening of any E1 verdict.

## 2. The substrate rule (frozen at ratification)

**2.1 Lattice and state.** L×L Moore lattice, L = 50 `[PROPOSED]` (N = 2,500, as E1), periodic boundaries as the frozen specification; x_i(t) ∈ {0,1}; tick Δt = 1.

**2.2 Bases and conduciveness.** v_i, u_i, r_i frozen for the run (Q disabled, Γ = 0; exogenous drive u_t = 0); **homogeneous** across cells `[RULED 2026-10-20]`: v_i = v̄, u_i = ū, r_i = r̄. λ_i = F(v̄, ū, r̄) = λ̄ by the frozen F dispatch, F_2_symmetric `[PROPOSED — the E1 form; Mike may rule F_LR]`.

**2.3 Local density.** d_i(t) = (number of active Moore neighbours of i at t)/8.

**2.4 Transition probabilities, evaluated from the state at t, applied simultaneously.**
- inactive → active: P_i = 1 − exp(−[h + g·λ_i·d_i(t)]·Δt)
- active → inactive: P_i = 1 − exp(−μ·Δt)
No other term. The symmetric chain's drive/σ/overcrowding construction does not execute in this rule mode; that construction is named here as the wrong implementation so it cannot be inferred.

**2.5 Timing.** Synchronous two-phase advance (read all → one full-grid uniform draw → advance all), the frozen skeleton's order; one uniform per cell per tick from the run's RNG stream, derivation rule as E1 (seed-panel master → per-seed stream → per-level identifier under "%.6f" of m).

**2.6 Two committed objects.** Skeleton: **h = 0**. Realization: **h = h₀ = −ln(1 − 0.01) ≈ 0.0100503** `[RULED]`, the per-tick hazard whose single-tick activation probability equals the specification's η_floor = 0.01, so the Overview's spontaneous term has one committed image.

**2.7 Deactivation.** **μ = 0.2** `[PROPOSED]` (mean active persistence 1/(1 − e^(−μ)) ≈ 5.5 ticks; null stationary density h₀/(h₀ + μ-equivalent) ≈ 5.2%). The contract records the alternative candidates L1 priced (μ ∈ {0.05, 0.1, 0.3, 0.5}) and the fact that the realization's rounding half-width in m is 1.07 / 0.93 / 0.58 / 0.49 at those values and 0.68 at 0.2: the unfolding is soft at every plausible μ because it is governed by h₀/μ. This is a property of the committed theory objects, not a tuning.

**2.8 Feedback gain and the control coordinate.** g is not swept. The control coordinate is **m := g·λ̄·Δt / (1 − e^(−μΔt))** `[RULED via design note §3]`; a sweep level sets λ̄ (through the homogeneous bases) so that m takes the level's value, with g fixed at g = 1 `[PROPOSED]` (any fixed g > 0 is equivalent under the definition of m). The identity of a level is its m in exact integer micro-units.

**2.9 Null (g = 0).** The same rule with the feedback term removed and nothing else changed: activation 1 − e^(−hΔt), deactivation 1 − e^(−μΔt), same h, same μ, same L, same timing, same seed derivation, same bases (inert). Each cell is an independent two-state Markov chain. Initialization: the chain's stationary distribution π₁ = a/(a + q), a = 1 − e^(−hΔt), q = 1 − e^(−μΔt), no burn-in `[RULED]`.

**2.10 Participation grammar (PD1–PD7).** A cell active at tick t has *registered* at t (PD7: a realized event); the participation window is **W = 1 tick, declared** (PD5: existence committed, value declared); ρ counts registrations over the domain; persistence (the fourth question) is what the crossing is about. The lattice has no activated agent; a region activates.

## 3. The closure and the pre-registered predictions

**3.1 Mean-field map** (homogeneous bases, d_i = ρ):
ρ_{t+1} = (1 − ρ_t)·[1 − e^(−(h + gλ̄ρ_t)Δt)] + ρ_t·e^(−μΔt).

**3.2 Skeleton prediction.** At h = 0, ρ = 0 is a fixed point with multiplier J₀ = e^(−μΔt) + gλ̄Δt. **Crossing: J₀ = 1 ⇔ m = 1.** For m < 1 the inactive state is linearly stable (perturbations decay as J₀^t); for m > 1 it is unstable and a positive fixed point ρ*_sk(m) exists, continuous from zero, computed from the fixed-point equation and committed as a table over the sweep levels `[DERIVED@BUILD]`. This is Overview §10's transcritical form in discrete time; gλ̄ ≈ μ (Λ* = β/g₀) is its Δt → 0 limit and is not the substrate equation.

**3.3 Realization prediction.** At h = h₀ the map has a unique positive fixed point ρ*(m; h₀) for every m `[DERIVED@BUILD]`, committed as a table; its departure from ρ*_sk is the rounding, maximal at m = 1.

**3.4 Finite-size predictions and tolerances.** The skeleton's inactive state is absorbing on a finite lattice, so (i) below m = 1 every run reaches the absorbing state and the pre-registered observable is the decay rate of the active count against J₀^t over the declared tail; (ii) above m = 1 the quasi-stationary density over the tail window is the observable, and its expected extinction time (from the map's linearization at ρ*_sk and the committed run length) is computed `[DERIVED@BUILD]`; the bracket **Δm** for T-S1/T-S2 is the m-interval over which that extinction time is shorter than the run — i.e. the finite-size smear of the crossing — plus one pass-1 spacing `[PROPOSED]`. The tolerance band for T-R1 is the map's ρ*(m; h₀) ± a declared fluctuation width computed from the null's finite-sample density variance at N cells and the window length `[DERIVED@BUILD]`, times a multiplier k_R = 3 `[PROPOSED]`. No tolerance is set from any sweep.

**3.5 Held.** The lattice-level spectral crossing (leading eigenvalue of gΔt·diag(λ_i)·A/8 + e^(−μΔt)I) coincides with m = 1 under homogeneous bases and is pre-registered here as the comparator for a heterogeneous-base successor job, not as a P1 test. The third-order lattice-versus-ODE comparison stays **held** (amendment §10) until Mike accepts §3.1–§3.2 as the bridge and L2 has reviewed §2.

## 4. The instrument (version `f8`, new package beside `e1`; nothing in `e1` modified)

**4.1 M1 — configuration and levels.** Pass-1 levels: n₁ = 24 `[PROPOSED]` values of m evenly spaced in exact integer micro-units over **[0.25, 2.50]** `[PROPOSED]` (spacing ≈ 0.0978; the crossing m = 1 is interior with ≥ 7 levels on each side; the skeleton's branch reaches ρ*_sk ≈ 0.4 at the top). Seed panel: 20 seeds drawn once by the E1 derivation rule from a new master `[DERIVED@BUILD]`. Run length and tail: T = 3,000 ticks, tail = last 1,000 ticks in 10 non-overlapping windows of 100 `[PROPOSED — E1's values; carried as scaffolding, re-declared here]`. Initializations: low (all inactive, floor-seeded) and high (all active) for the skeleton; stationary-null start for the realization.

**4.2 M2 — run status and level label.** Per run: S_min = minimum window-mean density over the 10 tail windows; S_term = terminal-window mean. SUSTAINED iff S_min > θ_P; else NO_SUSTAINED iff S_term ≤ θ_T; else UNRESOLVED. Level label from the 20 seeds: S (≥ 16 sustained, ≤ 2 null), N (the reverse), M (≥ 4 each), else U — the frozen 16/2/4 rule, **retained as the secondary-observable classifier and re-qualified under M6; nothing about it is pre-approved** (L2 2026-10-20 answer 4).

**4.3 M3 — the Markov null and thresholds.** Per level, thresholds from the null of §2.9 at that level's h₀, μ, N, window: **θ_T** by the exact two-state transfer-matrix law of a single window's occupancy, convolved over N independent cells, at the declared quantile 1 − α_T `[PROPOSED α_T = 0.001]`; **θ_P** for S_min over ten windows by the **conservative familywise construction** — the per-window exact marginal threshold at quantile 1 − α_P/10 `[PROPOSED α_P = 0.001]`, so the familywise false-SUSTAINED rate is ≤ α_P `[RULED with L2 2026-10-20]`; its realized conservatism is **priced at qualification** by reporting the empirical null rejection rate against α_P in the M6 record; the named fallback is a separately qualified simulation threshold with explicit coverage, invoked only if M6 shows (b) insufficiently discriminating, and only as a new instrument version. Thresholds are cached per level (production/slice roles and the cache-qualification record as E1), identity committed before any audit.
Note: the null's stationary density is the same at every level (λ̄ is inert at g = 0), so θ_T, θ_P are level-independent in this flight; they are still cached per level so the record grammar carries unchanged.

**4.4 M4 — verdict function and router.** Rules 1, 2, 3, 4a, 4b, precedence 1 > 2 > 3 > 4 and a > b > c > d, router rows P2R-1…P2R-7 with 8 insertions in P2R-5/6 and 4 + 4 in P2R-4, exact integer-micro-unit arithmetic with round-half-to-even, and the collision fallback — **all carried verbatim from E1 v0.4 §5 / v0.8 C–E** (diagnosis: none implicated). **Rule 4c is replaced:**
> **4c (F8).** NOT DISTINGUISHED (boundary unresolved at declared resolution W_res) iff, after pass 2, the measured width of the band — m(lowest confident S) − m(highest confident N) on the final level set — exceeds **W_res** (§4.5). Otherwise 4d: LOCATED, bracket [m₋, m₊].

**4.5 W_res — the declared resolution (status of W under PD5: existence committed, value declared).** `[DERIVED@BUILD]` by this procedure, committed with its inputs: (i) from §3.3 and §4.3, compute the **predicted mixing window** w_mix = the m-interval over which the realization's ρ*(m; h₀), with the null's finite-sample density fluctuation at N cells added and subtracted (the same width as §3.4's band at k = 1), straddles θ_P — i.e. the m-range over which a seed's SUSTAINED/NO_SUSTAINED status is undecided by the map alone; (ii) **W_res = c·w_mix, c = 2** `[PROPOSED]`; (iii) W_res is stated in integer micro-units and must exceed two pass-1 spacings, else the pass-1 grid is re-declared finer before freeze. No ensemble, sweep or audit enters the computation.

**4.6 The residual dependence of the width criterion on routing (contract clause; L2 2026-10-20 answer 1).** For a ramp-type morphology with true uncertain extent E (the m-interval over which the 16/2/4 rule applied to the sweep's own seed thresholds yields neither N nor S), the measured width satisfies E ≤ measured ≤ E + δ_N + δ_S, where δ_N, δ_S are the final-level spacings straddling the true endpoints after routing (fallback included). The lower side is exact; the upper holds because inserted levels can only add confident labels inside the band. The maximum of δ_N + δ_S over the frozen grid, insertion count and fallback rule is a declared number `[DERIVED@BUILD]`, and it is the slack the archetype gap (§6.2) absorbs. (Evidence of the form on E1's burned draws: `extent_bound.py`, `1f60bcb0…`, design chamber; it establishes the property of the rule, not any Flight 8 value.)

**4.7 Verdict grammar (line-not-drama, F8 form).** No criterion anywhere in §4 references jump size, slope, amplitude monotonicity or adjacent-level separation. (1) `NOT DISTINGUISHED (boundary unresolved at declared resolution W_res)` is an instrument statement — the band after refinement is wider than the instrument declared it can bracket — never a statement that a transition is absent, never adverse to P1; the package grammar records it valid-but-not-located. (2) Only `NOT PRODUCED` verdicts (rules 1–3) bear on the theory, and none references width. (3) An onset wider than W_res is unresolved at this resolution; the remedy is a finer pass-1 grid or more insertions in a successor stage, not a scientific reading. (4) A different W_res is a different instrument, not a different theory.

**4.8 M5 — closure and census.** The map (§3.1), its two fixed-point tables, the finite-size predictions and tolerances (§3.4), and the dense reference census over the sweep (701 levels `[PROPOSED — E1's count]`) as the reference of record; reference-stability over alternative templates as E1.

**4.9 M7 — records, package, readiness.** The E1-R package grammar **carries unchanged** (amendment §5): completeness = loads, validates, satisfies its declared predicate, adverse content included; *package complete* and *production ready* computed separately; apparatus and qualification prerequisites require passage, scientific prerequisites valid completion; branch stops only if expressly declared (this version declares none). Every record names its authorization, the stage identity and the instrument version.

## 5. Morphology audit (M6) and the archetype table

**5.1 Architecture carries.** Design and held-out ensembles, 500 sweeps per class `[PROPOSED]`, applicable error (scientific-intent classes: final ND; ND-intent: final LOCATED or NP), one-sided CP upper 95% ≤ **0.10** `[PROPOSED — E1's cap, re-declared]`, class `complete_pass` = 500/500/0 halts and cap clears, `ensemble_pass` = every class complete, qualification = design AND held-out joined mechanically. Generator: regime assignment per seed by fixed per-sweep uniforms against a class-specific profile in m; runs under each regime generated from the **Markov null** (NULL), the realization's own rule at the level's m (SUSTAINED), or the DIP construction (UNRESOLVED) — the generator declaration and its identity are committed before any master is drawn.

**5.2 The archetype table (F8)** — intended verdicts and declared width ranges in micro-units of m. Widths are set by the gap rule of §6.2, which is evaluated analytically before the table is frozen:

| Archetype | Intended | Profile | Declared width range |
|---|---|---|---|
| `crossing_onset` | LOCATED | the realization's own ρ*(m; h₀) profile, onset drawn from the sweep interior | w ∈ w_mix·[0.5, 1.0] |
| `gentle_onset` | LOCATED | linear ramp | w ∈ [0, w_L] `[DERIVED@BUILD]` |
| `abrupt_onset` | LOCATED | linear ramp | w ∈ [0, w_A], w_A ≪ w_L `[DERIVED@BUILD]` |
| `persistent_nonstationary_high_m` | LOCATED | ramp + drift/oscillation of the sustained level | w ∈ [0, w_A] |
| `nonmonotone_amplitude` | LOCATED | ramp + attenuation above onset | w ∈ [0, w_A] |
| `no_sustained_anywhere` | NOT_PRODUCED (no sustained phase) | null everywhere | — |
| `no_null_consistent_anywhere` | NOT_PRODUCED (no null-consistent phase) | sustained everywhere (reinterpreted: a realization that never decays — the skeleton's absorbing state is never reached) | — |
| `two_resolved_crossings` | NOT_PRODUCED (order violation) | N-S-N-S | offsets `[DERIVED@BUILD]` |
| `reentrant` | NOT_PRODUCED (order violation) | N-S-N | second onset `[DERIVED@BUILD]` |
| `off_band_mixture` | NOT_DISTINGUISHED (off-boundary mixture) | ramp + one mixed level below the band | as gentle |
| `off_band_unresolved` | NOT_DISTINGUISHED (off-boundary unresolved) | ramp + three DIP levels below the band | as abrupt |
| `wide_mixed_boundary` | NOT_DISTINGUISHED (boundary unresolved at W_res) | linear ramp | w ∈ [w_U, w_U·1.67] `[DERIVED@BUILD]` |
| `unresolved_heavy_boundary` | NOT_DISTINGUISHED (boundary unresolved at W_res) | DIP across the band | w ∈ [w_U, w_U·1.67] |

**5.3 Masters.** Two fresh masters (design, held-out) and the pricing master are **drawn by a declared rule from a declared seed after the table, W_res and the generator are frozen**, their values committed with the freeze commit's identity, and never reused across instrument versions. The E1 masters 202609221/2/3 are retired.

## 6. The guard gap (pre-registered separation; L2 2026-10-20 answer 2)

**6.1 Quantities.** For each ramp-type archetype, the true uncertain extent E (§4.6) is a deterministic function of the declared width w and the 20 seed uniforms; its supremum E_max(w) and infimum E_min(w) over all seed-panel draws are the extreme breakpoint configurations under the 16/2/4 rule and are computed analytically. Δ_route = max(δ_N + δ_S) from §4.6.

**6.2 The rule.** Locatable archetypes: **E_max(w_L) + Δ_route ≤ W_res**. Unresolvable archetypes: **E_min(w_U) > W_res**. w_L and w_U are the largest and smallest widths satisfying these, rounded inward to integer micro-units `[DERIVED@BUILD]`; the resulting ratio w_U/w_L is stated in the declaration table. No sample extremum from any ensemble enters.

**6.3 Check at freeze.** The declaration table lists E_max(w_L), E_min(w_U), Δ_route, W_res and the two inequalities with their margins; freeze is refused if either margin is ≤ 0.

## 7. Qualification, authorization, canonical jobs

**7.1 Order.** Freeze (this contract, ratified) → instrument version identity → M3 cache built and qualified → masters drawn (§5.3) → M6 design audit → M6 held-out audit → `m6_audit_qualification` → **passage required** → canonical scientific jobs. An adverse M6 closes the stage, as in E1-R; no same-stage repair.

**7.2 Authorization grammar.** As E1-R: each canonical job runs only under a Mike-issued authorization record naming the stage, the jobs and the tranche flags; the registry is append-only.

**7.3 Canonical jobs, in order (condition 3 of Mike's 2026-10-15 ruling).**
1. `skeleton_census` — h = 0, low and high initializations, full sweep; evaluates T-S1 and T-S2. **First canonical scientific job**: if the instrument misses the exact crossing it is known before the realization runs.
2. `skeleton_stability` — alternative templates and seed panels; class reproduced within Δm.
3. `realization_census` — h = h₀, stationary-null start; evaluates T-R1; records the secondary detection boundary through M4.
4. `realization_stability`, `projection_sweeps`, `tolerance_ensembles`, `tolerance_program`, `resource_benchmark`, `calibration_tranche`, `stage1_package` — E1-R's grammar and record kinds.
5. **Held** (successor stage): heterogeneous-base run against §3.5's spectral comparator; third-order lattice-versus-ODE comparison.

**7.4 Readiness.** Production readiness is derived mechanically from the governance record's prerequisites; `m6_audit_qualification` pass is a prerequisite; no production without it.

## 8. Declarations table (to be completed at build; every row carries an identity at freeze)

| Declaration | Value | Marker |
|---|---|---|
| L, N | 50, 2,500 | PROPOSED |
| F dispatch | F_2_symmetric | PROPOSED |
| h₀ | −ln(0.99) ≈ 0.0100503 | RULED |
| μ | 0.2 | PROPOSED |
| g | 1 (not swept) | PROPOSED |
| sweep range in m | [0.25, 2.50] | PROPOSED |
| n₁ pass-1 levels | 24 | PROPOSED |
| T, tail, window | 3,000 / 1,000 / 100 × 10 | PROPOSED |
| W (participation window) | 1 tick | DECLARED (PD5) |
| null initialization | stationary, no burn-in | RULED |
| α_T, α_P | 0.001, 0.001 (familywise) | PROPOSED |
| ρ*_sk(m), ρ*(m; h₀) tables | — | DERIVED@BUILD |
| Δm (T-S1/T-S2 bracket) | finite-size smear + 1 spacing | PROPOSED rule; value DERIVED@BUILD |
| k_R (T-R1 band multiplier) | 3 | PROPOSED |
| w_mix, W_res (c = 2) | — | DERIVED@BUILD |
| Δ_route | — | DERIVED@BUILD |
| w_L, w_A, w_U; E_max(w_L), E_min(w_U); margins | — | DERIVED@BUILD |
| cap, CP confidence, sweeps/class | 0.10, 0.95 one-sided, 500 | PROPOSED |
| masters (design, held-out, pricing) | drawn after freeze | DERIVED@BUILD |
| instrument version string | `f8_stage1_v1` | PROPOSED |

## 9. Notation rows added to the translation table (append-only; the table governs)

| Object | O — Overview v1.8.1 | C — this contract | S — frozen spec v0.4 | Nature |
|---|---|---|---|---|
| Control coordinate | Λ/Λ* (implicit) | m = gλ̄Δt/(1 − e^(−μΔt)) | (none) | C-only; m = 1 ⇔ Λ = Λ* in the homogeneous closure |
| Skeleton / realization | spontaneous term removed / restored | h = 0 / h = h₀ | — / η_floor = 0.01 | identity of meaning |
| Rounding width | "imperfection parameter" | w_mix (§4.5) | — | C-only |
| Resolution | — | W_res | — | C-only; status of W (PD5) |

## 10. What this contract does not claim

Nothing about the heterogeneous lattice, Regime II, Ψ, Q, or any E1 verdict. No value in §8 marked PROPOSED or DERIVED@BUILD is of record until the freeze commit names it. The design chamber's pricing on E1's burned ensembles established the form of 4c and the need for a gap; no number from it appears here. Mike rules; L2 reviews; Gemini audits for consistency only.

*L1, v0.1, 2026-10-20.*
