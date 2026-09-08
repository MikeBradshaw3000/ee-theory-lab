# L2 Gate B v0.4 Changed-Text Verification and Freeze-Readiness Verdict

**From:** L2 (ChatGPT)  
**To:** L1, routed by Mike  
**Register:** Phase-2, packet 4, closed changed-text verification  
**Source:** `L2_GATE_B_V0_4_PACKET.md`  
**Scope:** v0.4 Amendments 4R and 6R only, plus the routed canonical-environment rerun record. Amendments 1, 2, 3, 5, 7, 8, and 9 are not reopened.  
**Overall disposition:** **ALL FOUR REPAIR ITEMS CORRECTED AS REQUIRED. FREEZE MAY PROCEED.**

## Source custody

L2 independently recomputed the uploaded packet's SHA-256 as:

`8de02ac1c351df567e71c87ca69412c4d1041912d21208561d44381db07232fd`

This matches the digest prefix supplied in the routing request.

The canonical rerun is accepted as the record routed by Mike/L1 with this request:

- Python `3.14.4`
- NumPy `2.4.4`
- TOST all-eight pass: `4000/4000`
- repaired-screen no-alarm: `3977/4000`
- complete-gate pass: `3977/4000`
- power against the declared `0.005` mean divergence: `4000/4000` fail

L2 did not independently execute the canonical runner or recompute its source digest. This verification adjudicates the supplied record and the frozen algorithm; the downstream source-review obligations remain in force.

---

# 1. Repair item 1 — tie-valid gross-divergence screen

**VERDICT: CORRECTED AS REQUIRED.**

Amendment 4R removes the defective stable-order construction completely and replaces it with a tie-invariant statistic and an exact conditional randomization distribution.

For two samples of size 20, at any unique pooled value \(v\),

\[
\widehat F_C(v)-\widehat F_R(v)
  = \frac{a}{20}-\frac{s-a}{20}
  = \frac{2a-s}{20},
\]

where \(a\) is the number of candidate-role observations at or below \(v\), and \(s\) is the pooled number at or below \(v\). Thus

\[
D_{\mathrm{int}}=\max_v |2a-s|
\]

is exactly 20 times the ordinary equal-sample two-sided KS distance evaluated at the pooled support.

The repair is tie-valid because:

1. the statistic is evaluated only after complete equal-value blocks, using the right-continuous empirical CDF;
2. no within-tie ordering enters \(a\), \(s\), or \(D_{\mathrm{int}}\);
3. conditional on the pooled multiset, the null distribution enumerates all \(\binom{40}{20}\) fixed-size label assignments;
4. block allocations receive the correct multiplicity weight \(\prod_i \binom{b_i}{c_i}\); and
5. the tail probability includes the observed statistic, \(P(D_{\mathrm{int}}\ge D_{\mathrm{obs}})\), yielding a conservative-or-exact finite-sample permutation test.

The degenerate identity case is now correct: identical empirical samples give \(D_{\mathrm{int}}=0\), and every permutation has statistic at least zero, so \(p=1\). The screen no longer manufactures an alarm from arbitrary tie ordering.

The specification-level algorithm is sufficiently frozen for implementation review: empirical-CDF convention, support points, conditional null, dynamic-programming state, transition weights, tail direction, and inclusive alarm boundary are all stated.

---

# 2. Repair item 2 — repricing under the tie-valid screen

**VERDICT: CORRECTED AS REQUIRED.**

The per-cell alarm level is frozen at

\[
\alpha_{\mathrm{KS}}=\frac{0.01}{8}=0.00125.
\]

Because each conditional permutation test has null rejection probability no greater than \(0.00125\), Bonferroni gives an unconditional eight-cell familywise alarm probability no greater than \(0.01\), regardless of dependence among cells.

L2 independently recomputed the no-tie reduction. With 20 observations per group and all pooled values distinct,

\[
P(D_{\mathrm{int}}\ge 12)
 = \frac{153{,}809{,}370}{\binom{40}{20}}
 = 0.0011158015462314926.
\]

Therefore the stated `0.0011158` value is correct, and the inclusive \(p\le0.00125\) rule alarms at \(D_{\mathrm{int}}\ge12\) in the no-tie case. Amendment 4R genuinely extends the earlier no-tie pricing to tied samples rather than replacing it with an unrelated threshold.

The empirical tie incidence—3,759 of 4,000 forecast experiments—also confirms that tie handling is operationally load-bearing rather than a measure-zero refinement.

---

# 3. Repair item 3 — repaired complete-gate forecast

**VERDICT: CORRECTED AS REQUIRED.**

Amendment 6R recomputes the forecast under the repaired screen rather than carrying forward the v0.3 result by label. The forecast traverses the complete frozen acceptance family jointly:

- all eight Welch-TOST decisions;
- all eight repaired gross-divergence screens;
- disjoint 20-versus-20 role panels within each pseudo-experiment; and
- the same selected panel across all eight cells, preserving cross-cell dependence rather than multiplying marginal pass rates.

The integer record is internally coherent:

- TOST all-eight pass: `4000/4000`;
- screen no-alarm: `3977/4000`;
- complete-gate pass: `3977/4000`;
- total cell alarms: `50/32000`;
- experiments containing at least one tie block: `3759/4000`; and
- declared-divergence power: `4000/4000` failures.

The exact complete-gate pass fraction is

\[
3977/4000 = 0.99425.
\]

The displayed `0.9942` is a four-decimal presentation of the integer record; the integers remain controlling. The forecast therefore prices the actual repaired gate and shows that the alarm layer does not create the compound-conservatism failure that the earlier review required the design to test.

The routed canonical rerun reproduces every controlling integer from the provisional run. That discharges Amendment 6R's pre-freeze canonical-environment condition.

---

# 4. Repair item 4 — reproducible forecast record

**VERDICT: CORRECTED AS REQUIRED.**

Amendment 6R freezes the information needed to reproduce the forecast rather than leaving “4,000 resamples” underspecified:

- runner-source identity;
- analysis RNG family and seed: NumPy `default_rng(0x7A9B31C)`, PCG64;
- panel draw: `choice(200, 40, replace=False)`;
- role assignment: first 20 candidate-role, last 20 reference-role;
- one shared panel across all eight cells;
- the previously frozen Welch-TOST implementation;
- the full Amendment-4R screen;
- integer pass, alarm, and failure counts;
- environment stamp; and
- in-run verification of the pinned ancestor digest.

The canonical rerun in Python 3.14.4 / NumPy 2.4.4, reported with every integer identical to the provisional record, supplies the required cross-environment confirmation. The provisional record remains correctly labeled provisional and is not retrospectively promoted.

At implementation/source review, L2 still expects the actual runner bytes, complete source identity, dynamic-programming implementation, and emitted canonical record to match these frozen statements. That is the already-held downstream obligation, not a defect in the specification's reproducibility definition.

---

# 5. Repair-introduced defects

**NONE FOUND within the changed-text scope.**

The v0.3 stable-order rule and its measure-zero premise are expressly withdrawn rather than left as an alternative implementation. Amendment 6R points only to the repaired screen. No dual acceptance rule, silent fallback, or ambiguity over which forecast controls survives in v0.4.

Mike's prior narrowing of the B2 claim remains intact: Gate B2 positively certifies terminal-window ensemble-mean equivalence under the frozen TOST and carries this exact test only as a priced gross-divergence screen. Passing it does not become a claim of full distributional equivalence.

---

# 6. Freeze-readiness disposition

**FREEZE MAY PROCEED.**

No specification-level blocker remains in the four-item v0.4 repair surface. Mike may freeze Gate B Specification v0.4 and its comparator/acceptance grammar.

This verdict does **not** authorize an AUTHORITATIVE Gate-B execution. The previously recorded downstream implementation preconditions remain unchanged and mandatory:

- source review of the executable wrapper;
- the ten-run wrapper bit-identity record;
- qualification against the complete negative battery with per-mutant attribution;
- recorded FP-witness uint64 patterns;
- prospective solved-offset enumeration before qualification;
- mutant-30 frozen-input determinism and window-coverage proof; and
- source-level verification that the conditional-permutation dynamic program and canonical forecast record implement the frozen v0.4 algorithm exactly.

Those obligations are implementation gates after specification freeze. They are not grounds to withhold the v0.4 specification freeze now.

**Final L2 verdict: ALL FOUR REPAIRS CORRECTED AS REQUIRED; FREEZE MAY PROCEED.**
