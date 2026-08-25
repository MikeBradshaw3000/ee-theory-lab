# Contract E1 — Fixed-Terrain Activation Threshold (Cascade Existence, First Transition)
## Draft v0.2 (redrafted against L2's adversarial review + correction; for Mike's review, then L2 re-review)

**Status:** DRAFT. No production run is authorized by this document at any version. **[PROPOSED]** marks L1 values open to review; all become frozen commitments at contract freeze, which precedes production per the §8 sequence. Instrument: Merge Specification v0.4 FROZEN. Telling: E1_NARRATIVE_TELLING.md as amended and accepted.

**Threshold-object ruling (Mike, 2026-08-21, of record):** E1's object is the **fixed-terrain activation threshold**: Γ_Ψ = Γ_ρ = 0, no base-update arithmetic executed, bases fixed within-run; the sweep varies the frozen initial base-distribution between runs; R1 compares against a fixed-Λ mean-field reference with an independently specified projection map. The **coupled-system ignition boundary** is registered as a **named future object**, sequenced after E4 has exercised and characterized the Q channel (or as a named successor contract with declared Γ provenance); its preconditions are recorded — motivated Q coefficients and a located Λ* to measure departures against. It is scheduled by its dependencies, not suppressed.

---

## §1 Question, object, and claim tier

**Street question:** do conditions gate activity — is there a line on the ground?
**Formal object:** a threshold **bracket [Λ₋, Λ₊]** in the frozen initial-condition control, separating a phase with no sustained activation from a phase with sustained activation, under: the frozen F (F_canonical), the frozen base-distribution family, the frozen initialization, and the frozen local dynamics. The result is a threshold under those freezes — **never an unqualified universal scalar**.
**Initialization scope (travels with every claim):** activity initializes Bernoulli(0.5); E1 locates a boundary for *sustaining activation after the frozen initial perturbation*. It does not locate a nucleation threshold, does not prove loss of stability from arbitrarily small ρ, and does not establish independence from initial activation density.
**Claim tier:** P1, core-architecture jeopardy per the jeopardy split; verdict rules require neither continuity nor reversibility (E5's jurisdiction) and impose no onset-shape content (§5's line-not-drama rule).
**Verdict grammar:** produce / fail to produce; never confirm.

## §2 Configuration (frozen at contract freeze)

- rule_mode = symmetric_chain. **Q fully frozen: Γ_Ψ = 0 and Γ_ρ = 0, with no base-update arithmetic executed** — bases fixed for the full run; Ψ-family telemetry computed and emitted but writing to nothing. (Per L2's ruling: Γ_ρ = 0 accepted only as part of the complete freeze.)
- Local channel: **A's committed density and overcrowding terms** (the symmetric_chain construction; κ is become_survive's symbol and does not appear in E1's configuration — naming corrected per review item 12). u_t = 0. η_MFA amplitude 0 (no-draw bypass).
- F dispatch = **F_canonical** (accepted primary). **F_2_symmetric: [PROPOSED] NAME-DEFERRED** — not run in E1; registered as a named robustness question for a successor or for E5's form work. (L2's alternative — a frozen robustness arm whose result cannot replace, rescue, or veto the canonical verdict — remains available at Mike's word, but deferral keeps the compound budget and resource envelope clean at the core rung.)
- Grid/run length: 50×50 / 3000 ticks. Init: bernoulli_p, Gate-A algorithmic lineage; bases per §3's distribution control; u_base symbol used throughout (never bare u).

## §3 Sweep-variable definitions (exact separation, per review item 7)

Four named objects, never interchanged:
1. **Control variable m** — the base-distribution interval center. Bases v, u_base, r ~ U(m − w/2, m + w/2) i.i.d. per cell per base, with **fixed width w [PROPOSED] = 0.3** (the ancestor's 0.6–0.9 width) at every level. **Level admissibility rule: m ± w/2 must lie within [0, 1] — no clipping, silent or otherwise**; the admissible m-range is [w/2, 1 − w/2], and the sweep is confined to it so the distributional family is form-identical across levels.
2. **Theoretical level label E[Λ](m)** = E[F_canonical(v, u_base, r)] = (E[v])³-free exact product of independent uniform means = m³ under the symmetric family — computed exactly, recorded per level as a label.
3. **Realized initial grid mean Λ̄₀** — computed and persisted per run from the realized draw.
4. **Reported bracket [Λ₋, Λ₊]** — stated in the control m (with E[Λ] labels alongside), per §5.
Sweep design: **[PROPOSED]** 24 first-pass m-levels spanning the admissible range's relevant interior (endpoints per the §5 range guards), two-pass refinement of 8 levels per the bracket rule (§5), placement by rule only.
**Seed panel [PROPOSED]:** one panel of 20 seeds, drawn once, published in run_config pre-production, **reused across all levels** — comparisons across levels are therefore **paired by seed**, and all resampling respects pairing (§4.4).

## §4 Run-level and level-level classification

### 4.1 Run statuses (mutually exclusive, exhaustive)
- **SUSTAINED:** the persistence criterion passes AND tail activation exceeds the frozen null criterion (§4.3). **Persistence ≠ stationarity:** the criterion is material presence through the predeclared tail interval **[PROPOSED]** t ∈ [2000, 3000] — operationalized as: every consecutive sub-window of length **[PROPOSED]** 100 ticks within the tail has mean ρ above the null criterion. Bounded oscillation, slow variation, and other nonstationary-but-enduring activation SUSTAIN. No equilibrium is required.
- **NO SUSTAINED ACTIVATION:** the extinction/terminal-floor criterion passes — **[PROPOSED]** ρ(t) at or below the null criterion for every tick in a terminal window of 300 ticks, or exact extinction (ρ = 0) at any tick (absorbing under the frozen dynamics with u_t = 0 — verified against the frozen rule at freeze, else this clause is struck).
- **UNRESOLVED:** neither criterion earned within the horizon. **UNRESOLVED runs remain UNRESOLVED — they are never imputed to the floor, never assigned a numerical level, and enter level classification only as counts.**
The B-derived steady-state classifier runs on every SUSTAINED run as a **committed secondary diagnostic only**: it flags settled vs. unsettled persistence and gates which runs contribute to R1-T1's equilibrium estimate. It has no run-status role.

### 4.2 The null criterion (exact object, per review item 8)
The floor is the **upper [PROPOSED] 99th percentile of the frozen null ensemble**: the distribution of tail-window mean ρ under the **null dynamics object** — the frozen single-cell no-neighbor activation chain (sigmoid baseline at the level's parameters + η_floor, persistence under the symmetric rule, zero density terms) — extended to grid scale as 2500 independent such cells, with the window-length variance handled by the ensemble being computed over the exact tail-window statistic (analytically where the chain admits it; otherwise by **[PROPOSED]** 10⁵ Monte Carlo draws from the null chain on the analysis RNG, pre-production). No multiplier appears; the quantile is the design choice and is named as such. **The null is a no-interaction reference, and is named as that** — it is not a claim about low-density lattice behavior. **Null audit:** before freeze, the null and both run criteria are audited on constructed known-answer series (§7.2).
Level-dependence: the null is computed **per level** (its parameters enter the chain).

### 4.3 Level classification (per review item 4)
Per level, from 20 paired runs: counts (n_sus, n_no, n_unr).
- **LEVEL-SUSTAINED:** n_sus ≥ **[PROPOSED]** 16 and n_no ≤ 2.
- **LEVEL-NO-SUSTAINED:** n_no ≥ 16 and n_sus ≤ 2.
- **LEVEL-MIXED:** n_sus ≥ 4 and n_no ≥ 4 (a real composition finding, reported as counts, never averaged away).
- **LEVEL-UNDISTINGUISHED:** anything else (typically unresolved-heavy).
Uncertainty machinery **[PROPOSED]:** resampling unit = seed (respecting pairing); bootstrap = seed-level resampling with 10⁴ resamples on a dedicated analysis Generator (seed published pre-production); used only for reporting interval summaries on level compositions — **level classification is by the count rules above, not by interval overlap** (per review item 6: no adjacent-CI gate exists anywhere in this contract).

### 4.4 Amplitude reporting
ρ̄_sus (tail mean) is reported for SUSTAINED runs with median/IQR per level — **descriptive only**; no verdict rule consumes amplitude, its monotonicity, or its slope. (Spearman gate removed per review item 6; no r_s statistic appears in this contract.)

## §5 Verdict map (exhaustive, non-overlapping; bracket output)

**Precedence order: range guards → boundary census → verdict.** Applied to the level-classification sequence over the swept range:

**Range guards (checked first; either failing preempts all other verdicts):**
- **Bottom guard:** the lowest swept level must classify LEVEL-NO-SUSTAINED. Endpoint selection at freeze uses a prediction **in activation units**: the lowest m is chosen so the null-chain sustained-activation probability (the same frozen null object, full-run horizon) bounds the interacting system's from above there under a pre-registered dominance argument — or, failing an honest argument, by a pre-registered pilot-free structural margin; the guard then *tests* the choice. Failure → **NOT DISTINGUISHED (range: bottom)**.
- **Top guard:** the highest swept level must classify LEVEL-SUSTAINED. Symmetric construction. Failure → **NOT DISTINGUISHED (range: top)** — an all-floor profile is never allowed to mean "no sustained phase" when the sweep may simply not have gone high enough.

**Boundary census (guards passed):** enumerate maximal contiguous phase intervals from the level sequence (MIXED and UNDISTINGUISHED levels are boundary-resolution limits, not phases). A **transition bracket** is a pair (last confidently NO-SUSTAINED level Λ₋, first confidently SUSTAINED level Λ₊) with only MIXED/UNDISTINGUISHED levels (if any) between them.

**Verdicts:**
- **LOCATED THRESHOLD:** exactly one transition bracket; no phase reversion above it (every level above Λ₊ is SUSTAINED or, at worst, isolated UNDISTINGUISHED **[PROPOSED]** ≤ 2 non-adjacent). Output: [Λ₋, Λ₊] in m, with E[Λ] labels, at pass-2 resolution. **Line-not-drama (binding):** no criterion anywhere in this map references jump size, slope, amplitude monotonicity, or adjacent-level separation; arbitrarily gentle onset above a locatable boundary is LOCATED. Λ* passes to E2 as search-region input and nothing else.
- **P1 FIRST TRANSITION NOT PRODUCED** (core severity): guards passed and any of — (a) multiple resolved transition brackets; (b) resolved phase reversion (SUSTAINED levels followed by confidently NO-SUSTAINED levels above); (c) no transition bracket exists despite both guards passing (a resolvable but boundary-less profile). Multiple resolved crossings are a **substantive adverse finding** against the single-first-transition architecture, not an instrument limit. Verdict statement per the jurisdiction discipline: "E1 failed to produce the predicted single first transition in these worlds under this instrument and declared search surface" — permanently adverse at this jurisdiction.
- **NOT DISTINGUISHED** (instrument limit, named): a range guard failed; or the census is blocked by MIXED/UNDISTINGUISHED spans too wide to bracket at pass-2 resolution **[PROPOSED]** (> 3 contiguous non-classifiable levels at the candidate boundary); or unresolved-heavy levels prevent confident classification where it matters. Licenses a named successor with declared differences; licenses nothing else.
Exhaustiveness check at freeze: the synthetic morphology audit (§7.2) must map every audit morphology to exactly one verdict.

**Never-relax:** no criterion, count rule, window, null quantile, range endpoint, or resolution above may change after any production data exist.

## §6 R1 calibration section (fenced; executable per review item 11)

Verdict-independent from §5 in both directions. **Scope:** with Q frozen, E1-R1 tests **activation-level mean-field recovery under fixed structural conditions only**; recovery of Q's local-to-aggregate write behavior is E4-adjacent and is not tested here.

**Reference object:** the **candidate MFA working-form dynamics used for the registered MFP recovery test** (working-hypothesis status explicit; nothing herein is "committed MFA dynamics").
**Projection/parameter map (frozen before production, all five elements):** (1) tick↔time: one substrate tick = one MFA time unit, dt = 1 forward integration **[PROPOSED]**, scheme frozen (RK4, step 1); (2) parameter map: the mean-field closure is **derived pre-production from the frozen microscopic rule** — the single-site activation/persistence chain under mean-field density substitution (neighbor density → ρ), yielding the ρ̇ equation's coefficients from A's committed constants algebraically, derivation published and frozen; (3) the Λ entering the reference = E[Λ](m) per level (fixed within-run by the object ruling); (4) MFA initial condition ρ(0) = 0.5 (the substrate's Bernoulli mean); (5) **Λ*_MFA determined from the closure alone** (the derived ρ̇ equation's bifurcation point, computed analytically/numerically from the frozen closure before any E1 data — never fitted from E1 curves).
**Targets [PROPOSED]:** T1 equilibrium agreement (SUSTAINED-and-settled runs only, per §4.1's diagnostic gate) within tolerance τ_eq; T2 |bracket midpoint − Λ*_MFA| ≤ bracket half-width + pass-2 spacing, **evaluated only on LOCATED**; T3 trajectory-distance on the pre-tail approach within τ_traj.
**Tolerances:** τ_eq, τ_traj derived from a **constructed-null method** frozen pre-production — the null-ensemble and independent-cell variance arithmetic corrected for tick autocorrelation by a pre-registered effective-sample estimator on *null-chain* series (never on production data); the method, not just the numbers, freezes.
**Departure surface (target-specific, per the review):** the near-threshold zone **[PROPOSED]** (levels within one pass-2 spacing of the bracket) qualifies **T1 and T3 only** — departures there score against the declared surface. **T2 is never exempted**: it operates at the threshold by construction and a T2 miss is an R1 failure. **Asymmetry:** R0 passed, an R1 failure outside the declared surface is evidence against the stream-level realization; no post-hoc MFP refuge.

## §7 Evaluability section (eight components; controls and audit rebuilt)

1. **Tier:** P1, single primary claim, no stacking.
2. **Controls (constructed, known-answer — replacing the withdrawn theory-presupposing pair):** the classification machinery (persistence criterion, extinction criterion, null threshold, level rules, verdict census) is certified pre-freeze on **constructed series with algebraically known answers**: stable-above-null tails; extinct/decayed series; persistent bounded-oscillation series; slow-drift persistent series; unresolved (still-relaxing) series; near-null hoverers. A dynamics-level harness control **[PROPOSED]** runs the built instrument with **externally fixed activation probabilities** (a forced configuration whose sustained/extinct behavior follows algebraically, independent of P1's truth) to certify the pipeline end-to-end. High- and low-m production endpoints are **part of the scientific search surface** (they are §5's range guards), never apparatus controls.
3. **Compound budget:** false-classification rates per component estimated pre-freeze from the constructed-series ensemble and the null machinery; compound false-NOT-DISTINGUISHED forecast must clear **[PROPOSED]** 10% at freeze or the gate set thins **at freeze**.
4. **Falsifiable evaluability forecast:** "the production sweep yields a §5 verdict other than NOT DISTINGUISHED with forecast probability ≥ **[PROPOSED]** 80%," scored after the fact; two successive failures across E1 and its named successor escalate to Mike.
5. **Calibration tranche [PROPOSED — retained under strict quarantine]:** 3 seeds × 5 levels post-freeze, pre-production; an **automated quarantine** exposes only: telemetry-integrity pass/fail, invariant pass/fail, wall-clock and storage actuals. **No activation profiles, no ρ values, no classification outputs are human-readable from the tranche**; it cannot alter thresholds, windows, ranges, seed panels, or pass-2 placement. Tranche runs excluded from all verdict inputs.
6. **Claim ladder + anti-salvage:** outputs are the §5 verdict, the level-composition table, and the fenced R1 results — nothing else; no secondary observable promotes to a claim; structure feeds successor design as question-shaping only.
7. **Jurisdiction:** verdicts are about these worlds and this instrument; the field outranks the model; within jurisdiction verdicts stand un-relaxed.
8. **Halt rules:** *Apparatus* — telemetry invariant failure, gate regression, harness-control failure discovered mid-production → halt, fix, restart from clean state, discard logged. *Evaluability* — mid-production checks are **operational-fact-based only** (missing data, failed invariants, exhausted samples); production outcome patterns may never recompute budgets or thin gates → breach yields NOT DISTINGUISHED with the breach named. *Anomaly* — behavior outside the §7.2 audit's morphology space at any level → halt, report to Mike, no verdict, successor designed with the anomaly declared. (Pervasive nonstationary persistence is **not** an anomaly — it is SUSTAINED by §4.1.)

**Synthetic morphology audit (pre-freeze, binding):** the full §4–§5 machinery runs on synthetic profiles spanning **all admissible morphologies**: gentle continuous onset; abrupt onset; persistent nonstationary activation; nonmonotone active-phase amplitude; no sustained phase anywhere; no inactive phase anywhere; multiple phase crossings; reentrant loss; mixed-seed boundary compositions. Each must map to exactly one intended verdict; any miss redesigns the machinery **before freeze**.

## §8 Sequencing (four stages, per review item 10)

1. **Build & non-scientific qualification:** instrument built per frozen spec; Gates A, B, R0 passed; constructed-series and harness controls passed; telemetry checks; **wall-clock, storage, and I/O benchmark** measured on the built instrument.
2. **Contract freeze (Mike's word):** every [PROPOSED] resolved; ranges, panels, nulls, budgets, R1 map, and arm decisions fixed. Freeze requires the §7.2 audit passed and the resource forecast (§9) accepted.
3. **Post-freeze calibration tranche** under the automated quarantine (if retained at freeze).
4. **Production authorization (Mike's word) and production sweep.**
"Seeding" in prior documents reads **"production run"** throughout this contract. Downstream: LOCATED → Λ* to E2 as search-region input and nothing else. NOT PRODUCED → ladder halts at Mike's direction, verdict standing. NOT DISTINGUISHED → named-successor path only.

## §9 Resource pricing (owed at freeze, per review item 13)

Primary arm: (24 + 8) × 20 = **640 production runs**; at 7.5M rows/run ≈ **4.8B telemetry rows** before controls, tranche, retries, and R1 derivatives. F₂ deferral (§2) holds production at 640. **Owed from the §8.1 benchmark before freeze:** wall-clock/run and total; disk and I/O totals with margin; parquet count and partitioning; hashing/readback cost; restart granularity; capacity margin ≥ **[PROPOSED]** 30%.

## §10 Open items

| # | Item | Holder |
|---|---|---|
| 1 | All [PROPOSED] values | Mike, with L2 re-review |
| 2 | F₂ name-deferral vs. frozen robustness arm | Mike |
| 3 | Extinction-absorbing clause verification against frozen rule | L1, at build |
| 4 | Mean-field closure derivation (R1 map element 2) + Λ*_MFA | L1, pre-freeze, published |
| 5 | Resource benchmark | L1, at build stage 1 |

*End of draft v0.2. Sequence: Mike's review → L2 re-review → revision → freeze (§8.2) → stages 3–4.*
