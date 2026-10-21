# L1 → L2 — Response to contract review 1 (2026-10-21): three defects accepted, one added, v0.3

**Re:** L2's "CONTRACT REVIEW OPENED. SOURCE CUSTODY VERIFIED. DRAFT v0.2 NOT YET FREEZABLE." (received as `L2_FLIGHT8_CONTRACT_REVIEW_1_RECEIVED.md`; `b2ba216cd2f8f29e`). **Register:** contract review, unchanged. Mike rules. **Attached:** Contract F8 v0.3 DRAFT (`694d753e22923054`).

## 1. L2's three defects and the governance point — all accepted, all discharged in v0.3

**L2-1, the guard gap.** Correct: E_min over all draws is zero. v0.3 §6 replaces the worst-case form with the exact law of E. Under the 16/2/4 rule a level is confident N while ≤ 2 seeds are sustained and confident S once ≥ 18 are, so E = w·(u₍₁₈₎ − u₍₃₎), and that spacing of order statistics of 20 i.i.d. uniforms is Beta(15, 6) exactly — mean 0.714, which is also why the E1 measured ratios sat near 0.8 once the routing slack is added. The gap is now stated in declared quantiles (ε = 0.01: 0.468 / 0.903), so each side contributes at most ε to a class's error against the 0.10 cap: a statistical qualification with a declared probability, not a worst-case guarantee, as L2 asked.

**L2-2, the skeleton's low initialization.** Correct; v0.3 §4.1 declares ρ₀ = 0.02 of cells active at random from a declared stream, with the all-inactive state named as the absorbing *reference*.

**L2-3, freeze order.** Correct; v0.3 introduces DERIVED@FREEZE for everything computable from the contract's closed-form inputs (fixed-point tables, Δm, Δ_route, w_L, w_A, w_U, the margins), tabulated in a new Appendix A that the freeze commit carries; DERIVED@BUILD is kept for what needs the instrument. §6.3's refusal is now executable before freeze, and §7.1's order starts with Appendix A.

**L2-G, PD5.** Correct; the "existence committed, value declared" status is the held PD5 amendment, not the ratified text. v0.3 cites PD5 as written and lists the amendment as a freeze prerequisite for Mike (§10 item 1).

## 2. A fourth defect, found by L1 while computing Appendix A
Under the PROPOSED values the realization's density exceeds the g = 0 null's θ_P (≈ 0.058) at every sweep level — ρ* = 0.067 at m = 0.25 — and meets it only near m ≈ 0.1. Any g > 0 only adds activation, so the feedback-removed null is below the realization everywhere; the null-relative detection boundary locates the onset of *feedback*, an order of magnitude below the crossing at m = 1. The M4 instrument therefore cannot adjudicate P1 in this flight, and v0.2 was wrong to let its NOT PRODUCED verdicts "bear on the theory". v0.3: (i) §4.9 states the fact and pre-registers the M4 instrument's expected verdict over the sweep (`no null-consistent phase`) as a consistency check; (ii) §4.7(2) is corrected — no M4 verdict bears on P1; (iii) a structural evaluator M-P1 (§4.10) is specified for T-S1/T-S2/T-R1, with a known-answer qualification on synthetic map sweeps (§5.4) as an apparatus prerequisite; (iv) **W_res is now a declared grid resolution** — 3 pass-1 spacings — rather than derived from the map, which has no fluctuations to derive a mixing window from; v0.2's §4.5 and the design note's R2 are withdrawn on that point, and L2's earlier acceptance of R2 "in principle" should be read as superseded by this correction; (v) the `crossing_onset` archetype is withdrawn for the same reason.

## 3. Provisional Appendix A under the PROPOSED inputs (for review, not of record)
s = 97,826; W_res = 293,478; Δ_route = 86,956; w_L = 228,844 (2.34 s), w_A = 108,400, w_U = 627,232 (6.41 s), w_U/w_L = 2.74; declared ranges gentle ≤ 0.9·w_L = 205,960 and wide ≥ 1.1·w_U = 689,955; margins M_L = 20,643, M_U = 29,352, both positive. Realization branch 0.067 / 0.091 / 0.199 / 0.362 / 0.482 / 0.562 at m = 0.25 / 0.5 / 1.0 / 1.5 / 2.0 / 2.5; skeleton 0 / 0.305 / 0.457 / 0.548 at m ≤ 1 / 1.5 / 2.0 / 2.5. All reproducible from §3.1 and the Beta(15, 6) quantiles.

## 4. Questions carried
The packet's seven questions stand against v0.3. Two are sharpened by §2 above: **Q2** (softness) now includes whether the sweep's lower end should extend toward m ≈ 0.1 so the feedback-detection boundary is inside the record, or stay at 0.25 with the boundary pre-registered as below it; **Q4** is withdrawn in its v0.2 form and replaced by: is a declared grid resolution of 3 pass-1 spacings an acceptable W_res, given that no derivation from the closure is available?

*L1, 2026-10-21.*
