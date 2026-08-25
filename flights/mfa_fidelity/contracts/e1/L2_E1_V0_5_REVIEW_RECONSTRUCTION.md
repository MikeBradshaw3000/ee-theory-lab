# L2 Re-Review — Contract E1 Draft v0.5

> **Archival re-export status:** Reconstructed from the v0.6/v0.7 fold history. The eight operative findings are retained.

## Overall verdict

**CLOSE, BUT NOT FREEZE-READY — EIGHT ITEMS REQUIRE A FOCUSED v0.6.**

## 1. Naming and downstream inheritance

**ACCEPTED.**

The production threshold is now a bracket in `m` with derived labels kept secondary. E2 inherits the bracket/search region and nothing from the E1 verdict machinery.

## 2. Common-rank reference template

**ACCEPTED IN PRINCIPLE; ANALYSIS-SEED ROUGHNESS REMAINS.**

Using common ranks/common random numbers across the reference grid is the correct way to reduce artificial point-to-point Monte Carlo roughness. The contract must nevertheless freeze the analysis seed/stream, replicate count, rank construction, and any escalation rule. A convenient smooth reference cannot be selected after inspection.

## 3. Reference endpoint uncertainty

**BLOCKER.**

The reference classifier still treats endpoint central estimates as if phase membership were known. Low and high endpoint status must be assigned from the same prospective uncertainty discipline used elsewhere. An endpoint whose interval straddles the phase criterion is U, not N or S by its point estimate.

## 4. Off-band U rule

**BLOCKER.**

The draft permits a U point outside the candidate transition band to be ignored too easily. Every reference-grid point participates in the total classifier. Off-band U can make T2-S unstable or nonmatching and must be routed by a frozen rule; it cannot be discarded because it is inconvenient to the expected threshold.

## 5. T2-S finite-design stability

**BLOCKER.**

T2-S must be evaluated on at least the primary reference grid and a predeclared finer/stability grid. The result is RECOVERED only if the single-transition classification and bracket relationship are stable under the declared refinement. Failure of stability is NOT RECOVERED or a separately named reference-instability outcome, not a silent widening.

## 6. T2-L conditioning and envelope precision

**BLOCKER.**

T2-L exists only when production E1 is LOCATED and T2-S is RECOVERED. The location comparison must use a precisely defined relation between the production bracket and the reference threshold envelope. Specify endpoint inclusivity, whether touching counts, and how finite reference resolution expands the envelope.

## 7. Confidence-bound failure and nonmatching rates

**BLOCKER.**

The synthetic audit must compare upper confidence bounds, not observed point rates, to the frozen caps for false scientific verdicts, false NOT DISTINGUISHED, and router nonmatching. Freeze the interval method, confidence level, replicate minimum, and escalation ladder.

## 8. Explicit T2-S result row and collision handling

**BLOCKER.**

The result table needs an explicit T2-S `RECOVERED` row, not only failure branches. The reference grid also needs deterministic handling when rounded/serialized control values collide. Six-decimal labels cannot silently merge distinct requested points or cause spacing-dependent duplicates.

## Disposition

**FREEZE MAY NOT PROCEED.**

v0.6 should resolve only reference-classifier uncertainty, finite-grid stability, T2-L envelope semantics, error-bound precision, and deterministic control-value identity.
