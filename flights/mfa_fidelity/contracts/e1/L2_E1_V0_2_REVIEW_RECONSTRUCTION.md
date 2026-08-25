# L2 Re-Review — Contract E1 Draft v0.2

> **Archival re-export status:** The exact original turn is unavailable. This file preserves the operative twelve-blocker register reconstructed from the v0.3–v0.8 fold history. It does not invent a new adjudication.

## Overall verdict

**SUBSTANTIALLY IMPROVED, BUT NOT READY TO FREEZE — TWELVE BLOCKERS REMAIN.**

v0.2 accepts the central v0.1 architecture: total Q freeze, persistence separated from stationarity, three-way run status, threshold brackets, no slope/jump requirement, constructed controls, and fenced R1. The remaining defects are chiefly formal completeness and executable scoring.

## Blocker 1 — Fixed-terrain execution is not yet mechanically defined

The contract says Q is frozen, but the production configuration and verification obligation must state the whole condition: `Gamma_Psi=0`, `Gamma_rho=0`, no Q arithmetic, no clipping path, and bitwise base identity over every expected cell/tick row. A prose zero is insufficient.

## Blocker 2 — One “floor” is still serving three different objects

The draft uses related null language for:

1. a run's tail activation level;
2. a level's seed-wise sustained fraction; and
3. the profile boundary/threshold decision.

Those are different statistics with different null distributions. Freeze a named null and decision rule for each, or derive the latter two explicitly from the first. No threshold may migrate between units.

## Blocker 3 — Exact extinction is not an absorbing expectation

Under the symmetric rule with nonzero `eta_floor`, exact all-zero activity need not remain zero. A clause that treats exact extinction as the canonical inactive state can misclassify lawful spontaneous floor activity as sustained or unresolved.

The inactive reference must be a stochastic low-activation object under the frozen dynamics, not an absorbing-zero assumption.

## Blocker 4 — The null ensemble is not fully generative

The contract names a constructed null but does not yet freeze all ingredients required to reproduce it: initialization, seed panel or seed-generation rule, horizon, tail window, local terms retained/removed, number of replicates, analysis RNG, quantile method, and finite-sample uncertainty.

A null is not predeclared merely because its verbal purpose is predeclared.

## Blocker 5 — Run-level S/N/U classification remains incomplete

The run router must be total and mutually exclusive. It needs exact conditions for:

- SUSTAINED;
- NO SUSTAINED ACTIVATION; and
- UNRESOLVED,

including the handling of persistent nonstationarity, late growth, late decay, switching, missing telemetry, and horizon exhaustion. Stationarity may annotate but not control the primary category.

## Blocker 6 — Level aggregation remains under-specified

The contract must freeze how the common seed panel produces a level status, including:

- paired versus unpaired treatment;
- minimum evidence for S and N;
- maximum tolerated U;
- interval method and confidence level;
- bootstrap/resampling unit and analysis seed; and
- the result of mixed S/N seeds.

Median activation alone cannot stand in for a level category.

## Blocker 7 — Pass-two placement is not a deterministic total router

“Insert levels in the bracket” is incomplete when coarse data contain:

- no bracket;
- more than one bracket;
- an unresolved level between N and S;
- endpoint-only evidence;
- duplicate transformed labels; or
- a bracket narrower than representable spacing.

The pass-two rule must map every pass-one classification pattern to either one deterministic level set or a named terminal verdict, using only predeclared inputs.

## Blocker 8 — Endpoint/range jurisprudence still overlaps science and instrument limits

All-S and all-N profiles cannot be called P1 failure unless endpoint adequacy was prospectively established. Conversely, once endpoint adequacy is established, those resolved profiles cannot be diverted to NOT DISTINGUISHED merely because the expected phase is absent.

Freeze independent low- and high-end adequacy rules and use them before the scientific verdict router.

## Blocker 9 — The threshold object is still conflated with a point estimate

The primary scientific object is a bracket in the control coordinate, with corresponding derived labels in `E[Lambda]` and realized `Lambda_bar_0`. `Lambda_star_cand` must not ambiguously name a level, midpoint, first-S level, or fitted point.

Define the inherited E2 object and its uncertainty exactly.

## Blocker 10 — R1 lacks a frozen microscopic-to-MFA projection map

The candidate MFA working form cannot be evaluated until the contract freezes the parameter map, time map, initial condition, aggregate control coordinate, numerical integration scheme, threshold target provenance, and tolerance construction.

The R1 target may not be estimated from the production curve it evaluates.

## Blocker 11 — Evaluability arithmetic is still not executable

The proposed “false-NOT-DISTINGUISHED” forecast must be computed end-to-end on admissible synthetic morphologies. Per-component false-block rates or a product of marginals cannot price dependencies among run classification, level aggregation, endpoint guards, pass-two routing, and the profile verdict.

Freeze morphology menu, replicate count/precision rule, escalation ladder, and confidence-bound decision against the proposed 10%/80% values.

## Blocker 12 — Production surface and resource/arm decision remain open

Before freeze, resolve the exact first-pass levels, refinement count/spacing, seed panel, tail window, storage/I/O plan, restart granularity, and whether `F_2_symmetric` runs. “If the budget admits it” is not a frozen design.

If the secondary F arm runs, its verdict is a committed sensitivity result and cannot rescue or veto `F_canonical`.

## Disposition

**FREEZE MAY NOT PROCEED.**

A focused v0.3 should make the null/classifier/router and R1 bridge executable, not reopen the accepted E1 architecture.
