# Contract E1 — Fixed-Terrain Activation Threshold (Cascade Existence, First Transition)
## Draft v0.3 (resolves all twelve L2 re-review blockers; for Mike's review, then L2 re-review)

**Status:** DRAFT. No production run authorized. **[PROPOSED]** values freeze at contract freeze (§8.2). Instrument: Merge Specification v0.4 FROZEN. Telling: as amended and accepted. Threshold-object ruling (Mike, of record, carried verbatim from v0.2's head): fixed-terrain activation threshold; Γ_Ψ = Γ_ρ = 0; coupled-system ignition boundary a named future object sequenced after E4, preconditions recorded.

---

## §1 Question, object, claim tier

**Street question:** is there a line on the ground?
**Formal object (null-relative, per blocker 3's claim-language requirement):** a threshold bracket **[m₋, m₊]** in the frozen initial-condition control, separating a phase in which tail activation is **consistent with the frozen no-interaction reference** from a phase of **persistent activation exceeding that reference under the interacting lattice** — under the frozen F (F_canonical), frozen base-distribution family, frozen initialization, and frozen local dynamics. Because the symmetric rule supplies positive baseline activation at every finite parameter (η_floor > 0), E1 does not separate "activity exists" from "activity does not exist"; it separates null-consistent from null-exceeding persistence, and every claim is worded so. Never an unqualified universal scalar.
**Initialization scope (travels with every claim):** boundary for sustaining activation after the frozen Bernoulli(0.5) perturbation; not a nucleation threshold; no small-ρ stability claim; no initial-density independence claim.
**Claim tier:** P1, core jeopardy; no continuity, reversibility, or onset-shape content anywhere in the verdict machinery. **Verdict grammar:** produce / fail to produce.

## §2 Configuration

- rule_mode = symmetric_chain; **Q fully disabled: Γ_Ψ = Γ_ρ = 0, no base-update arithmetic executed**; bases fixed within-run; Ψ-telemetry emitted, writing nothing. Local channel: A's committed density and overcrowding terms. u_t = 0; η_MFA = 0 (no-draw bypass). F = F_canonical (accepted primary); F_2_symmetric NAME-DEFERRED (accepted). Grid 50×50, 3000 ticks; init bernoulli_p, Gate-A lineage; u_base throughout.
- **Total-Q-disable conformance preflight (blocker 11), §8 stage 1:** assert in the E1 configuration that (i) no Q-update callback or base-write expression executes; (ii) v, u_base, r are **bit-identical to their initial values at every tick** (streamed check over full telemetry); (iii) no Q clipping or clip counter can alter state; (iv) the disabled-Q configuration is recorded in run_config.json. If the frozen instrument's zero-coefficient branch does not already supply this path, **the divergence is surfaced as a specification question (versioned successor), never implemented informally under this contract.**

## §3 Sweep-variable definitions

Control **m** (base-interval center); v, u_base, r ~ U(m − w/2, m + w/2) i.i.d., **w = 0.3** (accepted in principle); admissible m-range **[0.15, 0.85]**, no clipping ever. Theoretical label **E[Λ](m) = m³** (recorded per level). Realized **Λ̄₀** per run (descriptive). Reported bracket **[m₋, m₊]** — *always in m-space* (blocker 6); Λ-space companion [m₋³, m₊³] reported alongside.
**Pass-1 sweep [PROPOSED]: 24 levels spanning the FULL admissible range** — endpoints at m = 0.15 and m = 0.85 exactly, interior levels evenly spaced (blocker 5's jurisprudence requires the family be exhausted, so the sweep exhausts it by construction).
**Seed panel:** 20 seeds, drawn once, published pre-production, reused at every level (paired); the same panel serves pass-2 levels.

## §4 Run and level classification

### 4.1 Tail statistics and run statuses (statistic-matched nulls; blocker 1)
Tail = ticks 2000–2999 inclusive (1000 ticks, endpoint convention fixed). **Non-overlapping** partition into 10 windows of 100 ticks (overlap eliminated; no familywise pricing needed beyond the exact null of each composite statistic). Named statistics: **S_min** = minimum of the 10 window means; **S_term** = mean over the terminal 300 ticks (windows 8–10).
Statuses, applied in **precedence order** (exclusivity by construction; sensible joint behavior certified by the §7 audit):
1. **SUSTAINED:** S_min > **θ_P**, where θ_P = the **[PROPOSED]** 99th percentile of the frozen null distribution **of S_min itself**. Persistence without stationarity: oscillation, drift, and switching sustain if every window clears the null.
2. else **NO SUSTAINED ACTIVATION (null-consistent):** S_term ≤ **θ_T**, where θ_T = the **[PROPOSED]** 99th percentile of the frozen null distribution **of S_term itself**. (The exact-extinction clause is **STRUCK** — under the frozen rule p_act ≥ η_floor·(1−p_base) + p_base > 0 always, so ρ = 0 is a stochastic snapshot with no absorbing privilege; L2's derivation adopted.)
3. else **UNRESOLVED** — remains UNRESOLVED; enters level classification as a count only.
B steady-state classifier: committed secondary diagnostic; gates R1-T1 inputs only.

### 4.2 The null object (complete generative definition; blocker 3)
**Construction (option 2 of L2's menu, chosen):** per level, one frozen set of 2500 base triples drawn from the level's frozen distribution using a **dedicated null-generation Generator** whose seed derives by a frozen rule (master analysis seed ⊕ level index); triples held fixed across all null replicates for that level (heterogeneity in, redrawn never). Null dynamics per cell: the no-neighbor chain — p_base = σ(α·Λᵢ − γ_offset), p_act = p_base + η_floor(1−p_base), symmetric persistence, zero density terms — 2500 **independent** heterogeneous chains. Activity initialization: each cell starts at its chain's **analytically computed stationary distribution** (two-state chain; closed form), so only the tail is simulated. Replicates: **[PROPOSED]** 10⁴ vectorized tail-only simulations per level on the analysis Generator; from each replicate, S_min and S_term computed exactly as in production; θ_P, θ_T = empirical 99th percentiles with **order-statistic 95% CI frozen alongside** (Monte Carlo uncertainty priced; if the CI half-width exceeds **[PROPOSED]** 2% of the point value, replicates double once, then freeze). Method (analytic stationary init + vectorized tail MC) benchmarked in §9; analytic/DP replacement permitted pre-freeze if validated against the MC on **[PROPOSED]** 3 levels.
**Pass-2 nulls (rule-governed instantiation, L2's discipline verbatim):** the null-generating algorithm, seed-derivation rule, and quantile choices freeze before production; when the router names a pass-2 level, its null is computed **mechanically, before any production run at that level**.
The null is a **no-interaction reference** and is named only as that.

### 4.3 Level classification
From 20 paired runs: (n_sus, n_no, n_unr). **LEVEL-SUSTAINED:** n_sus ≥ 16 ∧ n_no ≤ 2. **LEVEL-NO:** n_no ≥ 16 ∧ n_sus ≤ 2. **LEVEL-MIXED:** n_sus ≥ 4 ∧ n_no ≥ 4. **LEVEL-UNDISTINGUISHED:** otherwise. (Counts not rejected by L2; ratifiable only after the §7 audit prices them — carried as [PROPOSED] pending that audit.) Bootstrap (seed-resampling, pairing-respecting, 10⁴ resamples, dedicated analysis Generator, seed published) reports interval summaries only; **no classification consumes intervals**. Amplitude: descriptive only.

## §5 Verdict map (total, exhaustive; blockers 4, 5, 10)

**The verdict function is TOTAL over {S, N, M, U}^L** — every possible level-label sequence maps to exactly one verdict by the explicit rules below; totality and non-overlap are verified pre-freeze by **exhaustive rule tests over generated label sequences** (property-based), in addition to the archetype audit. Precedence: guards → census → verdict.

**Range guards with exhausted-family jurisprudence (blocker 5):** the sweep's endpoints ARE the hard admissible boundaries (m = 0.15, 0.85), so there is no interior-range case in this contract's first pass:
- Lowest level (m = 0.15) not LEVEL-NO → **no null-consistent phase exists within the exhausted family** → contributes to the census as a substantive finding (see NOT PRODUCED (a) below), not an instrument limit.
- Highest level (m = 0.85) not LEVEL-SUSTAINED → **no sustained phase within the exhausted family** → likewise substantive (NOT PRODUCED (b)).
- (A named-successor E1 with a different frozen family remains available under either finding; the finding within *this* family stands un-relaxed.)
- The v0.2 dominance-bound language is **withdrawn** (unproved; the density and overcrowding terms order differently with ρ); endpoints are justified as the family's exhaustion, full stop.

**Census:** maximal contiguous phase intervals over the level sequence; MIXED/UNDISTINGUISHED are resolution limits, not phases. Transition bracket = (last confidently NO level m₋, first confidently SUSTAINED level m₊) with only M/U levels between.

**Verdicts (each label sequence maps to exactly one):**
- **LOCATED THRESHOLD:** both guards satisfied; exactly one transition bracket; no resolved reversion above it (levels above m₊ are SUSTAINED, allowing **[PROPOSED]** ≤ 2 isolated non-adjacent UNDISTINGUISHED, this allowance priced for hidden-reversion risk in the §7 audit); output [m₋, m₊] with [m₋³, m₊³]. **Line-not-drama binding:** no jump, slope, amplitude-monotonicity, or separation criterion exists anywhere in this map.
- **P1 FIRST TRANSITION NOT PRODUCED** (core severity, within the exhausted family): (a) no null-consistent phase (bottom finding); (b) no sustained phase (top finding); (c) multiple resolved transition brackets; (d) resolved reversion; (e) both phases present but no admissible bracket (resolvable, boundary-less profile). Statement: "E1 failed to produce the predicted single first transition in these worlds under this instrument, family, and declared search surface."
- **NOT DISTINGUISHED** (instrument limit, named): the census is blocked by a contiguous M/U span > **[PROPOSED]** 3 levels at the candidate boundary after pass 2, or unresolved-heavy levels prevent confident classification where the boundary would sit, or (pass-2 router row 6) refinement was foreclosed. Licenses a named successor only.

**Pass-2 placement router (deterministic, complete; blocker 4)** — inputs: pass-1 label sequence; outputs: pass-2 levels (8 total, same seed panel, nulls per §4.2's rule-governed instantiation); resource accounting follows the router:
1. Exactly one candidate transition interval (one maximal NO-block adjacent to or separated by M/U from one SUSTAINED-block) → 8 levels evenly spaced strictly inside the interval [m₋ᶜᵃⁿᵈ, m₊ᶜᵃⁿᵈ].
2. One contiguous M/U span bordering the phases → 8 levels evenly spaced across the span's frozen outer bounds.
3. **Two candidate intervals → 4 + 4, evenly spaced inside each** (fixed allocation; no analyst choice).
4. Three or more candidate intervals → **no refinement**; census runs at pass-1 resolution (typically NOT PRODUCED (c) if resolved, NOT DISTINGUISHED if not).
5. Resolved reversion at pass 1 → **no selective refinement**; census at pass-1 resolution (NOT PRODUCED (d)).
6. Guard-relevant endpoint failure per above → no pass 2; census proceeds (NOT PRODUCED (a)/(b)).
7. No candidate interval and no span (e.g., alternating labels) → no refinement; census at pass-1 resolution.

**Never-relax:** nothing above changes after any production data exist.

## §6 R1 (executable; blockers 6, 7, 8)

Fenced, verdict-independent. **Scope:** activation-level mean-field recovery under fixed structural conditions only.

**R1a — direct discrete mean-field closure (published pre-freeze, primary).** The reference is the **discrete map** ρ_{t+1} = G_m(ρ_t) = E_{Λ~D_m}[η_floor + (1−η_floor)·σ(αΛ + βρ_t − δρ_t² − γ_offset)] — the independence/mean-neighborhood closure of the frozen microscopic rule; exact expression derived from the built rule and published before production; the expectation over D_m evaluated **[PROPOSED]** by fixed-node Gauss–Legendre quadrature on the frozen triple-product distribution, scheme frozen. Iterated directly — **no ODE, no RK4** (v0.2's precommitment withdrawn per L2). **Fixed-point analysis of G_m across m, computed from the closure alone before any E1 data**, with the possibility map frozen: unique threshold m*_MFA (fixed-point structure changes once) → T2 evaluable; no structure change / smooth crossover → **T2 NOT EVALUABLE, recorded as a reference-structure finding**; multiple changes → T2 NOT EVALUABLE (multiplicity recorded); discontinuous change → T2 evaluable at the located discontinuity, character recorded. Absence of a predicted threshold in the closure is a **form finding, never an apparatus failure**.
**R1b — candidate working-form (Landau/supercritical) reduction: NAME-DEFERRED to E5**, where transition-shape jurisdiction lives; E1 commits only R1a. (Failure of the candidate form thereby cannot be misrecorded as failure of mean-field recovery.)

**Targets, each with total grammar {RECOVERED / NOT RECOVERED / NOT EVALUABLE}:**
- **T1** equilibrium agreement — per level, |mean settled-run ρ̄ − G_m's stable fixed point| ≤ τ_eq. NOT EVALUABLE if: settled runs < **[PROPOSED]** 8 at that level; no level settles; or cross-seed settled estimates disagree beyond a pre-registered dispersion bound. (No automatic recovery or failure from non-evaluability.)
- **T2** threshold-location — **coordinates repaired (blocker 6):** compare in Λ-space: Λ*_MFA (from R1a's fixed-point analysis, in Λ) against [m₋³, m₊³]; RECOVERED if Λ*_MFA ∈ [m₋³ − s³ᵉᶠᶠ, m₊³ + s³ᵉᶠᶠ] where sᵉᶠᶠ = pass-2 spacing transformed to Λ-space at the bracket (frozen transform). Evaluated only on LOCATED **and** T2-evaluable reference; else NOT EVALUABLE with cause recorded. **T2 is never exempted by the departure surface.**
- **T3** trajectory distance on the approach (ticks 0–2000), mean production ρ(t) vs. iterated G_m from ρ₀ = 0.5, pre-declared functional distance ≤ τ_traj.
**Tolerances (blocker 8):** τ_eq, τ_traj derived from a **frozen finite-N reference ensemble generated by the projection object itself** — the finite-N stochastic realization of G_m (2500 cells, each activating independently at the map's per-tick probability at the level's parameters), **[PROPOSED]** 10³ replicates per level; tolerances = pre-registered quantiles of that ensemble's own deviation statistics. This prices finite-grid sampling and projection-side stochasticity; spatial-correlation and heterogeneity contributions are declared **unpriced residuals** whose exceedance is exactly what R1a measures. Method frozen pre-production.
**Departure surface (defined under every verdict; blocker 8):** a zone frozen around the *independently derived* threshold — levels with |E[Λ](m) − Λ*_MFA| ≤ **[PROPOSED]** 2·s³ᵉᶠᶠ — qualifies **T1 and T3 only**. If the reference has no unique threshold, the zone is empty and no exemption exists. The zone is reference-anchored, so it exists identically under LOCATED, NOT PRODUCED, and NOT DISTINGUISHED; under the latter two, T2 is NOT EVALUABLE and T1/T3 report per their own grammar. **Asymmetry:** R0 passed, R1 failure outside the declared surface is evidence against the stream-level realization; no post-hoc refuge.

## §7 Evaluability (blockers 9, 10)

1. **Tier:** P1, single claim.
2. **Controls:** constructed known-answer series (stable-above-null; extinct/decayed; bounded-oscillation persistent; slow-drift persistent; still-relaxing unresolved; near-null hoverers) certifying the **entire composite run classifier** (S_min/S_term/precedence jointly, per blocker 1's audit requirement); plus the forced-probability dynamics harness control (externally fixed activation probabilities, algebraically known outcome). Production endpoints are scientific surface, never controls.
3–4. **Evaluability forecasts (probability model defined; blocker 9):** forecasts are **per-morphology**, each over a **declared generative model**: for each archetype class (§7-audit list), a frozen parameterized generator (e.g., gentle onset: G_m-shaped profiles with onset location and noise drawn from declared ranges; abrupt onset; persistent nonstationary; nonmonotone amplitude; no-sustained-anywhere; no-null-anywhere; two crossings; reentrant; mixed-boundary compositions) produces **[PROPOSED]** 500 synthetic sweeps through the full §4–§5 machinery. Reported: per-morphology classifiability (verdict ≠ NOT DISTINGUISHED where the archetype's intended verdict is scientific) and per-morphology false-verdict rates. **Compound cap:** the **worst-case** false-NOT-DISTINGUISHED rate across archetype classes must be ≤ **[PROPOSED]** 10% at freeze, or gates thin at freeze. **No single overall percentage is reported unless morphology weights are frozen and justified; the [PROPOSED] posture is per-morphology reporting with no overall average.** The 16/2/4 counts, ≤2-isolated-U allowance (hidden-reversion risk specifically), and >3-span limit are priced inside this audit and ratify only if it clears. **Gate-thinning is versioned and re-scored against an independently generated held-out audit ensemble** (fresh generator seeds) so the classifier is not optimized to its design examples. Forecast scoring: the production outcome's archetype (as classified post hoc by the frozen rules) is compared against that archetype's forecast; two successive misses across E1 and its named successor escalate to Mike.
5. **Calibration tranche:** accepted as ruled — automated quarantine, integrity/cost outputs only, no redesign channel.
6. **Claim ladder + anti-salvage:** verdict, level-composition table, fenced R1 — nothing else.
7. **Jurisdiction:** as standing.
8. **Halt taxonomy (anomaly narrowed; blocker 10):** *Apparatus/domain halts only:* non-finite telemetry; impossible state values; invariant violations (including the §2 bit-identity assertion); missing/corrupt output; classifier inputs outside declared domains; a contracted statistic mathematically undefined. **Surprising but valid phase patterns are never anomalies** — the total verdict function maps them (three crossings → NOT PRODUCED (c); broad mixed region → NOT DISTINGUISHED; persistent oscillation → SUSTAINED; nonmonotone amplitude → descriptive). *Evaluability halts:* operational facts only. **Archetype→intended-verdict table (written, auditable):** gentle onset → LOCATED; abrupt onset → LOCATED; persistent nonstationary at high m → LOCATED (top guard satisfied); nonmonotone active amplitude → LOCATED; no sustained anywhere → NOT PRODUCED (b); no null-consistent anywhere → NOT PRODUCED (a); two resolved crossings → NOT PRODUCED (c); reentrant → NOT PRODUCED (d); resolvable boundary-less → NOT PRODUCED (e); wide mixed boundary → NOT DISTINGUISHED; unresolved-heavy boundary → NOT DISTINGUISHED. The audit verifies the machinery reproduces this table.

## §8 Sequencing
Unchanged four stages. Stage 1 adds: the §2 total-Q-disable conformance preflight; the null-method benchmark; the finite-N reference-ensemble benchmark. Stage 2 freeze requires: audit passed (held-out re-score included), R1a closure and fixed-point analysis published, resource package (§9) accepted. "Production run" language throughout. Downstream unchanged (Λ* → E2 as search-region input only).

## §9 Resource package (structurally accepted; measured values owed at freeze)
640 production runs ≈ 4.8B rows, plus now itemized: per-level null construction (24 + up to 8 levels × 10⁴ tail-only replicates — vectorized cost benchmarked; analytic/DP substitution if validated); morphology audit (≈ 9 archetypes × 500 sweeps through analysis machinery — synthetic, no substrate runs); R1 finite-N ensembles (≤ 32 levels × 10³ replicates); analysis-table and derived-output storage; **common-seed level rerun cost after partial failure** (restart granularity = whole level **[PROPOSED]**); wall-clock, disk, I/O, parquet partitioning, hash/readback, ≥ 30% margin — all measured at stage 1.

## §10 Open items
| # | Item | Holder |
|---|---|---|
| 1 | All [PROPOSED] values (counts/quantiles ratify only via the §7 audit) | Mike + L2 re-review |
| 2 | R1a closure derivation + fixed-point analysis publication | L1, pre-freeze |
| 3 | Total-Q-disable conformance (or spec-successor surfacing) | L1, stage 1 |
| 4 | Null-method + finite-N ensemble benchmarks; resource actuals | L1, stage 1 |

*End of draft v0.3.*
