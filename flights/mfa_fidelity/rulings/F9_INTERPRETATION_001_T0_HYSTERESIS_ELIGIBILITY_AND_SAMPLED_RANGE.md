# Ruling Record — F9 Interpretation 001: T0's hysteresis test and the sampled range (Contract F9 v0.7 §5.8)

**Ruled by:** Mike, Theory Architect.
- **Point 1:** ruled 2026-11-18, on L2's finding D1 in its M5 round-1 review (`L2_F9_M5_ROUND1_REVIEW_2026-11-18_RECEIVED.md`, `1700fe17f2280da6…`) and L1's recommendation of L2's reading.
- **Point 2:** on 2026-11-19 Mike ratified M5-10 as a BUILD DECLARATION ("Ratified."), which is not a ruling on this record. L2 accepted the formula technically (M5 round 1, §4) and said so again when it reviewed this record's first draft.
- **This record as a binding interpretation, both points:** accepted by Mike on 2026-11-20 ("All recommendations accepted and yes on the ruling"), after L2's review of the first draft pointed out that his acceptance had not yet been given.
**Status:** an identified interpretation of the FROZEN contract (`FLIGHT_9_CONTRACT_v0_7.md`, SHA-256 `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`). The contract's bytes and identity are unchanged. This record resolves two places where §5.8 can be read in two ways and binds every instrument module and report that reads either.
**Scope.** T0 only. T0 is never scored by §5.5; its record gates no endpoint (§5.8). Nothing here touches B, D, any scored tolerance or any arm other than T0.

## Point 1 — when the hysteresis test is unevaluable

**The sentences (§5.8).** "It [the hysteresis bracket] applies only if, for each of the two skeleton boundaries, the level just below the boundary and the boundary level are both in the fine grid and 0.05 apart; a boundary at κ = 1.00 does not qualify because the level below it is 0.75. Otherwise the hysteresis test is unevaluable, cause `bracket outside fine grid`, and the other tests stand."

**The two readings.** Flight 8's evaluator, which §5.8 reruns "redeclared as follows", returns the low sweep's own outcome when skeleton-low has no boundary: FAIL `no active phase in sweep`, FAIL `no inactive phase in sweep`, or ND `non-monotone survival`. Reading A keeps that outcome ahead of the eligibility rule, on the ground that the bracket compares two boundaries and there are not two. Reading B takes "otherwise" to cover every case in which the two sweeps do not each supply an eligible boundary, a low sweep with no boundary included. M5 round 1 was built on A; L2 showed a complete, valid input (high boundary at 1.00, low sweep never surviving) on which A returns NOT PRODUCED where the sentence as written gives NOT DISTINGUISHED.

**The interpretation (binding): reading B.** Once T-S1′ has located the skeleton-high boundary, T-S2 is decided in this order:

| Condition | T-S2 |
|---|---|
| a level of skeleton-low has no record | ND `apparatus unevaluable (missing level record)` |
| the two sweeps do not each have a boundary whose level and the level just below it are both in the fine grid (1.00 to 2.00) and 0.05 apart. A complete skeleton-low sweep with no boundary (no level meeting the criterion, every level meeting it, or a non-monotone profile) supplies none | ND `bracket outside fine grid` |
| both eligible and \|κ̂_low − κ̂_c\| ≤ 0.0754 | PASS |
| both eligible and the separation larger, in either direction | FAIL `hysteresis` |

When T-S1′ does not locate a high boundary, T-S2 is ND `not evaluable: T-S1′ did not locate a boundary (…)`, as in Flight 8. **T-S2 has no FAIL other than `hysteresis`.** Both sweeps' §5.4 persistence records are kept in the T0 record whatever T-S2 returns.

**What this gives up, stated before the ruling and accepted.** A skeleton-high sweep with an eligible boundary and a skeleton-low sweep that never meets the criterion was a failure under Flight 8's rule and is, under this interpretation, ND with the cause `bracket outside fine grid`. The cause label does not describe that case well; the low sweep's profile, carried beside it in T-S2's detail and in the persistence record, does. The frozen sentence already sends a low boundary at 2.25, 2.50 or 3.00 to ND; a low boundary beyond 3.00 is the next case on the same line. The T0 record in such a case is NOT DISTINGUISHED only if the other three tests pass: a realization failure still gives NOT PRODUCED, and an earlier ND keeps its own cause.

**A consequence of the frozen text, not of this interpretation.** T0 can be PRODUCED only if both skeleton boundaries fall from 1.05 to 2.00.

## Point 2 — "the branch's sampled range"

**The sentences (§5.8).** "an excess of J_j over f_J = 0.25 of the branch's sampled range returns NOT DISTINGUISHED … Domains follow Contract F8 §4.11: the skeleton continuity comparison runs over levels at and above κ̂_c,T0, its sampled range being the skeleton medians' range over those levels; the realization test runs over the whole grid with the realization medians' range over the whole grid".

**The two readings.** "Range" as the largest median minus the smallest over the domain; or as Contract F8 §4.11's endpoint form, the median at the top level minus the median at the lowest level of the domain. They agree on a monotone branch. They can differ when the medians fall after a peak: L2 built a branch (M5 round 1, §4) rising from 0.10 at 1.50 to 0.20 at 2.00 and falling to 0.15 at 3.00, with the reversals inside the band, where the endpoint form returns ND and max-minus-min would pass.

**The interpretation (binding): the endpoint form.** The sampled range is **med(top level of the grid) − med(lowest level of the test's domain)**: for the skeleton test, the median at 3.00 minus the median at the boundary level; for the realization test, the median at 3.00 minus the median at 0.75. Every increase between adjacent levels is compared with f_J times that range whatever the range's sign, as in the placed Flight 8 evaluator. The basis is the lineage: §5.8 imports its domains from Contract F8 §4.11, which states this formula, and redeclares the slope normalization without replacing the range. The endpoint form is never the larger of the two.

## Consequences

- Placed M5 (`f9/t0.py` `a2ce76e8b3e8c5b9…`, L2 SOUND round 2, at `068b5b3`) already implements both points; no placed byte changes. Its docstring's reading 5 and reading 2 are these two points.
- The other readings M5 declared (the divisor 39 in ŝ; the skeleton test keeping the reversal clause; `hysteresis` in either direction; the unused low-sweep proxy; the all-levels-met case where κ̂_c,T0 = 0.75 is an available unbracketed reference while T-S1′ fails) were accepted by L2 as build declarations and ratified by Mike on 2026-11-19 with M5-1 to M5-11. They are not interpretations of competing sentences and are not restated here.
- Adopting the other reading of either point later would be a change to placed M5, through its own L2 round.
- The reports of §8 step 15 cite this record where they state T0's outcome.

*Drafted by L1 from Mike's rulings, 2026-11-19, and revised 2026-11-20 for the authority statement above (L2 governance round 1, Q1); the table of point 1 follows L2's M5 round-1 §2.3.*
