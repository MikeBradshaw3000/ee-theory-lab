# Contract E1 — Cascade Existence (Threshold Location)
## Draft v0.1 (L1, for Mike's review, then L2 adversarial review; freezes before any E1 data exist)

**Status:** DRAFT. No seeding is authorized by this document at any version; seeding is authorized only by Mike's word after this contract freezes and Gates A, B, and R0 have passed on the built instrument. **[PROPOSED]** marks L1 values open to review; all become frozen commitments at contract freeze. Instrument: Merge Specification v0.4 FROZEN (digest 39f66673…f52a). Telling: E1_NARRATIVE_TELLING.md as amended and accepted by Mike; the claims herein are consistent with its thin-mapping admissions, and the line-not-drama constraint it records is binding on §5.

---

## §1 Question and claim tier

**Street question (per the telling):** do conditions gate activity — is there a line on the ground?
**Formal question:** does sustained activation exhibit a locatable threshold Λ* in the sweep variable, separating a no-sustained-activation phase from a sustained-activation phase?
**Claim tier:** P1 (ordered cascade, first transition) — **core-architecture jeopardy** per the L2 jeopardy split. E1's gates, parameterization, and verdict rules do not require continuous or reversible behavior (E5's jurisdiction).
**Verdict grammar:** E1 produces or fails to produce a located threshold; it never confirms, demonstrates, or proves.

## §2 Configuration (all values frozen at contract freeze)

- rule_mode = symmetric_chain; Q_read = local (PRIMARY per D2; the comparator mode is not exercised in E1); Γ_ρ **[PROPOSED]** = 0 for E1 (the activation channel of Q is not needed to ask the gating question, and Γ_ρ = 0 keeps E1's dynamics closest to ancestor-certified ground; the extended channel enters at E4 where its claim lives — L2 review invited on this choice).
- F dispatch **[PROPOSED]** = F_canonical (Λ = v·u·r), the D3 committed form; F_2_symmetric runs as a committed secondary sweep arm if the evaluability budget (§7) admits it, else named-deferred.
- u_t = 0 throughout (house light off, per the telling); κ-coupling at the committed symmetric_chain terms — present as committed dynamics, not arranged as a driver.
- η_MFA amplitude 0 (no-draw bypass active).
- Grid/run length: 50×50 / 3000 ticks (frozen spec §9.1). Init: bernoulli_p, Gate-A algorithmic lineage.
- **Sweep variable:** the base-initialization interval's center, moved so that E[Λ] traverses **[PROPOSED]** 24 levels from hopeless to favorable (exact level list frozen at freeze; spacing refined near candidate threshold by the pre-declared two-pass rule in §4 — second-pass levels are chosen by rule, not by inspection of outcomes beyond the rule's inputs).
- **Seeds:** **[PROPOSED]** 20 seeds per level, drawn once, published in run_config before any run.

## §3 Observables

- Primary: sustained activation level ρ̄_sus per run (operationalized §4), aggregated per level across seeds (median and IQR; mean recorded).
- Committed secondaries: full ρ(t) curves (R1 inputs); transient peak and decay records; Ψ-family observables emitted per the frozen spec but **carrying no E1 verdict role** (regime classification is E2's business; emission here is telemetry continuity only).
- All telemetry per frozen §7; rho_global persisted (Gate-R run; §7.2 dual condition).

## §4 Operationalizations (pre-declared)

**Sustained vs. transient (the held/rented rule):** a run's sustained level ρ̄_sus is the mean of ρ(t) over the assessment window **[PROPOSED]** t ∈ [2000, 3000], accepted as "sustained" only if the window passes the steady-state classification rebuilt from Lineage B's machinery (relative drift, CV, and range-over-mean thresholds **[PROPOSED]** carried at B's committed values from the pinned commit, re-anchored to the merged instrument's window length at freeze). A run failing steady-state classification contributes "no sustained level" (ρ̄_sus recorded as floor), not a lower number — decay is not a small answer, it is a different answer.
**Floor:** ρ̄_sus ≤ ρ_floor **[PROPOSED]** = 2× the closed-form single-cell spontaneous-activation expectation under the level's parameters (computed pre-seed from the committed dynamics; exact expression frozen at freeze) counts as "no sustained activation." The floor is derived from mechanism arithmetic, not tuned.
**Two-pass sweep rule:** pass 1 runs all first-pass levels; if the coarse profile brackets a candidate transition (pre-declared bracket rule: adjacent levels straddling floor-to-above-floor), pass 2 inserts **[PROPOSED]** 8 levels uniformly within the bracket. The rule's only input is which coarse interval brackets; no other outcome feature may steer placement.

## §5 Classification rules (the verdict machinery; line-not-drama binding)

Pre-declared, exhaustive, applied to the level-aggregated ρ̄_sus profile:

- **LOCATED THRESHOLD:** there exists a level Λ*_cand such that (i) all levels below it (within pass-2 resolution) classify no-sustained (floor), (ii) levels above it show sustained activation exceeding floor with level-monotone central tendency **[PROPOSED]** (Spearman ρ ≥ 0.8 across the above-threshold arm), and (iii) the below/above separation holds under the seed-level uncertainty rule **[PROPOSED]** (non-overlap of bootstrap 95% intervals for the levels adjacent to Λ*_cand). **Binding constraint (Mike's catch, from the telling):** growth *rate* above Λ*_cand is not a criterion. Arbitrarily gentle growth from floor above a locatable onset point satisfies LOCATED. No criterion in this contract may demand a jump, a minimum step size, or a minimum slope — any such criterion would refute the theory for behaving as its own working form predicts.
- **NO THRESHOLD (P1 fails to be produced):** sustained activation exceeds floor at the lowest levels of the sweep, or rises from floor without any point satisfying the LOCATED separation at pass-2 resolution — i.e., holding begins at no locatable point within the swept range. Verdict statement, per the jurisdiction discipline: "E1 failed to produce the predicted first transition in these worlds under this instrument and declared search surface" — core-level severity, permanently adverse at this jurisdiction, not diluted to absence-of-evidence.
- **NOT DISTINGUISHED:** the profile satisfies neither rule (e.g., separation fails the uncertainty rule at pass-2 resolution; non-monotone above-arm). This is an instrument-limits verdict, named as such; it licenses a *named* successor (finer resolution, more seeds) with declared differences, and licenses nothing else.
- **Range guard:** if the sweep's lowest level is not confidently in the no-sustained phase (lowest level exceeds floor), the sweep range was wrong; verdict is NOT DISTINGUISHED with the range defect named. The bottom of the sweep is chosen at freeze to make this unlikely by construction (E[Λ] at the bottom **[PROPOSED]** below the closed-form floor's activation expectation by a margin fixed at freeze).

**Never-relax:** no threshold, floor, window, resolution, or statistic above may be adjusted after any E1 production data exist. NOT DISTINGUISHED does not license relaxation; it licenses a named successor contract.

## §6 The R1 calibration section (fenced: instrument-calibration, not science)

Per the telling: this section answers no street question and its outcomes are verdict-independent from §5 — no R1 result modifies, strengthens, or weakens an E1 classification, and vice versa.

**R1 targets (first frozen set, per frozen spec §8.3), frozen at contract freeze:** for each sweep level, the mean-field prediction ρ_MFA(t; Λ) is computed from the committed MFA dynamics at the level's parameters (closed-form or numerically integrated; the integration scheme itself frozen). Targets: **[PROPOSED]** (T1) equilibrium agreement — |ρ̄_sus − ρ_MFA(∞)| within a tolerance band τ_eq set at freeze from pre-registered finite-size arithmetic (N = 2500), not from observed runs; (T2) threshold-location agreement — |Λ*_cand − Λ*_MFA| within pass-2 resolution, evaluated only if §5 returns LOCATED; (T3) trajectory-shape agreement on the approach — pre-declared functional-distance statistic between mean ρ(t) and ρ_MFA(t) over the pre-window, with tolerance from the same finite-size arithmetic. **Declared departure surface:** near-threshold levels are pre-registered as the expected mean-field failure zone (correlations grow near criticality — the projection's own known limit); departures there are recorded against the declared surface, not counted as R1 failures. **Attribution telemetry** per frozen §8.3 exposure set. **Asymmetry (ratified MFP):** R0 having passed, an R1 failure outside the declared departure surface is evidence against the stream-level realization; MFP is not invocable as post-hoc refuge.

## §7 Evaluability section (the eight components, ratified audit standard)

1. **Target claim tier:** P1, core jeopardy; single primary claim; no claim stacking.
2. **Positive control:** a pre-registered parameter set deep in the sustained phase (E[Λ] high) must classify sustained under §4's machinery; **negative control:** a set deep in the hopeless phase must classify no-sustained. Both run before the sweep is examined; either control failing halts per component 8 (category: apparatus).
3. **Compound conservatism budget:** the verdict requires jointly: steady-state classification (per run) + floor rule + separation rule + monotone-arm rule + range guard. Budget arithmetic **[PROPOSED]**: per-component false-block rates estimated pre-seed from the controls' seed ensemble and the bootstrap machinery on synthetic profiles; the compound false-NOT-DISTINGUISHED rate must forecast below **[PROPOSED]** 10% or the gate set is thinned *at freeze* (TCOP's lesson applied before, never after).
4. **Falsifiable evaluability forecast:** pre-seed statement: "under the committed dynamics with the frozen parameters, the instrument will produce a §5-classifiable profile (LOCATED or NO THRESHOLD) with forecast probability ≥ **[PROPOSED]** 80%." A NOT DISTINGUISHED outcome scores against this forecast; two successive failed forecasts across E1 and its named successor escalate to Mike as an instrument-program question.
5. **Calibration tranche option:** **[PROPOSED]** exercised — 3 seeds × 5 levels run first solely to verify telemetry integrity, steady-state machinery function, and wall-clock (the S5 forecast obligation); tranche outputs are quarantined from all §5 inputs and from pass-2 placement; tranche runs are excluded from the verdict ensemble.
6. **Claim ladder with anti-salvage guard:** the only claims this contract can output are the three §5 verdicts plus the fenced R1 results. No secondary observable (Ψ-family, transient structure) may be promoted to a claim; interesting structure is recorded for E2+ design as question-shaping only.
7. **Jurisdiction statement:** all verdicts are about simplified worlds and this instrument; the field outranks the model; within jurisdiction, verdicts stand un-relaxed.
8. **Halt rules (three-category taxonomy):** *Apparatus* (control failure, telemetry invariant failure, Gate-A/B/R0 regression discovered mid-flight) → halt, fix, restart sweep from clean state; partial data discarded, discard logged. *Evaluability* (compound budget breached by pre-registered mid-flight check) → halt, verdict NOT DISTINGUISHED with the breach named; no relaxation. *Anomaly* (behavior outside the pre-registered outcome space, e.g., non-stationarity the steady-state machinery cannot classify at any level) → halt, report to Mike, no verdict issued, successor designed with the anomaly declared.

## §8 Execution preconditions and downstream

**Before any E1 seeding:** contract frozen by Mike; instrument built; Gate A passed (bit-exact); Gate B passed (B1+B2); R0 passed (bridge correctness on constructed cases); calibration tranche (if exercised) complete and clean; positive/negative controls passed. **Downstream inheritance:** on LOCATED, Λ* passes to E2 as search-region input **and nothing else** — no E2 gate, tolerance, or regime definition derives from E1 outcomes. On NO THRESHOLD, the ladder halts at Mike's direction with the core-severity verdict standing. On NOT DISTINGUISHED, the named-successor path opens; nothing else does.

## §9 Open items for this draft

| # | Item | Holder |
|---|---|---|
| 1 | All [PROPOSED] numeric values (§§2, 4, 5, 6, 7) | Mike, with L2 adversarial review |
| 2 | Γ_ρ = 0 for E1 (design choice, §2) | Mike; flagged for L2 |
| 3 | F_2_symmetric secondary arm: run or defer | Mike, after §7.3 budget arithmetic |
| 4 | Wall-clock forecast (owed at freeze, measured on built instrument) | L1, after build |

*End of draft v0.1. Sequence: Mike's review → L2 adversarial review (full, first-pass) → revision → freeze at Mike's word → build-gate preconditions → seeding at Mike's word only.*
