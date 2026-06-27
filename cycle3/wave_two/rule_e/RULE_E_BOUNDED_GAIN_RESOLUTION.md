# Rule E bounded-gain - design resolution (modified Candidate A selected; NON-SEEDING)

**Status: DESIGN RESOLUTION. NON-SEEDING. Resolves the bounded-gain conditioning-function construction at the design level: modified Candidate A selected as the first bounded-gain follow-up construction; Candidates B and C held as conditionally-admissible named alternatives under a formal freeze discipline. Layer 2-reviewed and -recommended; Mike-arbitrated. Does NOT seed a run, does NOT draft an implementation spec, does NOT authorize Layer 3.** This resolves the open left by the bounded-gain design-resolution memo (the proposal that routed three candidate gain-control constructions to Layer 2). It selects the construction; it authorizes no probe.

Governing documents: cycle3/wave_two/rule_e/RULE_E_DESIGN_CONTRACT.md (governs Rule E design; this resolution selects a construction within it, amends nothing in the contract), cycle3/wave_two/rule_e/RULE_E_OPENS_RESOLUTION.md (the first-pass opens resolution), cycle3/wave_two/rule_e/RULE_E_FIRST_PASS_FINDINGS.md (the scoped-negative result this construction responds to). On any discrepancy, those govern.

Lineage: bounded-gain proposal memo (three candidates, non-seeding, routed to L2) -> L2 review (accepts memo as admissible artifact; recommends modified Candidate A; holds B/C; catches the tier-specific bound defect) -> this resolution (Mike arbitrates modified-A in). Drafted by Layer 1; Layer 2-recommended; Mike-arbitrated.

---

## 1. What is resolved

The first bounded-gain follow-up construction is **modified Candidate A: a smooth, tier-specific bound on the realized conditioning term.** This selects the conditioning-function form (contract Section 7 open 1) and the gain-control construction of the alpha grid (open 2) FOR A BOUNDED-GAIN FOLLOW-UP INSTRUMENT. It does not seed that instrument, does not fix a final grid count, and does not draft its spec.

Candidates B (recalibrated alpha ladder against a conditioned-excursion scale) and C (two-scale standardization with a frozen conditioned-scale denominator) are NOT selected for the first follow-up. They are recorded as conditionally-admissible named alternatives, held under the formal freeze discipline in Section 4, available if modified-A produces or fails to produce in a way that motivates them.

## 2. The selected construction (modified Candidate A)

Same Rule C M2 base, same 25-tick non-overlapping block-lag, same Lambda-configuration locus on the becoming-active channel, same block-resolved recording and lag-dynamics guard as the first pass. The ONLY change from the first pass is the conditioning term: the unbounded standardized term is replaced by a smooth, tier-specific bounded term.

Construction:
- For each target effective-Lambda displacement tier d_j (the intended probability-space tiers, e.g. {0, +/-0.0125, +/-0.025, +/-0.05, +/-0.10} as specified in the first-pass opens resolution), compute its corresponding maximum logit displacement Delta_j by LOGIT INVERSION at base p_Lambda = 0.40. Delta_j is the per-tier maximum; it is NOT a single global d_max shared across tiers.
- Bound the realized conditioning term for tier j by a smooth saturating function of its own Delta_j, e.g.

      cond_term_j = Delta_j * tanh( alpha_j * g_E(M) / Delta_j )

  so the realized term cannot exceed +/-|Delta_j| for that tier, saturates smoothly (tanh, not hard clip), and preserves a graded response near zero.
- alpha = 0 (the d_0 tier) bypasses the conditioning arithmetic entirely and calls the un-conditioned base update path exactly (Section 4 separability; the F3 alpha-zero bypass constraint carries unchanged - exact recovery verified at build/runtime parity, not by floating-point cancellation).
- g_E(M) retains M_ref as the pre-registered un-conditioned reference; the standardization denominator is not the locus of this construction's repair (the bound is), so the first pass's split pre-registered M_ref carries; the construction does NOT introduce a conditioned-scale denominator (that is Candidates B/C).

**Why tier-specific, not global (Layer 2's catch, recorded):** Layer 1's proposal memo specified a single global d_max for all tiers. Layer 2 caught that a global bound reproduces the first-pass identical-tiers pathology in bounded form - if every nonzero tier is bounded only by the maximum |d|=0.10 displacement, small tiers saturate to the same maximum as large tiers whenever g_E is large, collapsing the tier distinction exactly as the railed first pass did. The tier-specific bound (each tier capped at its OWN Delta_j) is the fix: the tier itself determines its maximum realized displacement, so the tiers stay distinct under saturation. This is recorded as an L2 catch on a Layer 1 construction defect, in the lineage of the Rule D R3 saturation catch (L3-surfaced) and the lag upper-bound correction (L2, 2026-06-05).

**Why smooth (tanh) over hard clip (Layer 2-recommended):** hard clipping creates flat plateaus and turns the macro channel into a discontinuous relay; tanh saturates while preserving a graded response near zero and a less brittle transition. The first bounded pass uses the smooth form. (Hard clip is not fenced; it is simply not the selected first-pass shape. Whether saturation SHAPE matters for reaching a substantive near-null is an open empirical question, not resolved here.)

## 3. Required diagnostics (binding on any future bounded-A run record, additional to the contract Section 5 block-resolved requirement)

A bounded-A run record must additionally record, block-resolved: raw g_E(M); the PRE-bound conditioning term (alpha_j * g_E(M)); the POST-bound conditioning term (cond_term_j); effective (conditioned) Lambda; and the fraction of blocks in which the bound is active or near-active. These are additional to the contract Section 5 requirements (macro block signal, effective Lambda, rho, raw Psi_meanI_state, raw Psi_persistence_I, window-level candidate flags) and the F3 bit-exact alpha-zero check, all of which carry.

**Saturated-channel-candidate flag (Layer 2-required):** if a candidate near-null appears only while the bound is active nearly all the time, it is recorded as a SATURATED-CHANNEL candidate, not a clean responsive-channel candidate, pending audit. A bound that is active almost everywhere means the channel is operating at its rail, which is the bounded analogue of the first-pass over-drive; a near-null produced under a near-always-active bound has not demonstrated responsive conditioning and is fenced from clean candidate status until audited. This is a new discriminator specific to the bounded construction; it sits alongside the lag-dynamics guard and the inert-channel guard, not replacing either.

## 4. Candidates B and C - held conditionally admissible under formal freeze discipline

B and C are NOT selected for the first follow-up, for two substantive reasons (Layer 2, Mike-concurred): (1) both require a separate characterization run to pre-register a conditioned-excursion scale - itself a later seeding decision and an added ambiguity surface; (2) both retain a linear-gain mis-sizing risk - a conditioned-excursion scale measured at one low pilot alpha may mis-size the gain at higher tiers because the macro feedback is nonlinear, so they may fix the denominator at one scale yet rail or underdrive at another. Candidate C additionally retains the UNBOUNDED linear form (it changes the denominator but does not bound the realized term), so it inherits the first pass's main structural risk and is the highest-risk of the three; the first-pass failure precision (calibration-internal to the UNBOUNDED standardized-gain construction) argues specifically against another unbounded linear standardized pass as the next instrument.

They are NOT dismissed. Layer 2 confirmed B and C do NOT collapse into dynamic centering merely by using a conditioned-scale constant, PROVIDED a strict, formal freeze discipline holds. The freeze discipline, recorded here as the gate on any future B or C selection (all seven binding):

1. M_ref stays the pre-registered un-conditioned reference (never a conditioned mean).
2. The conditioned scale is measured in a SEPARATE characterization run.
3. The conditioned scale is FROZEN before the swept run.
4. It is not recomputed by seed, window, tier, candidate flag, or running rho.
5. The characterization run is not tuned against observables or LowLow outcomes.
6. The scale is used ONLY in the becoming-active Lambda-configuration channel.
7. alpha = 0 still bypasses conditioning and recovers the un-conditioned base rule exactly.

Under all seven, B/C are calibrated scale choices, not dynamic centering. The margin is thin and the discipline must be FORMAL, not informal: if the center or scale tracks the current run, or if the pilot is iteratively adjusted after seeing candidate behavior, it becomes fenced dynamic rho-feedback / target tuning. If B or C is ever selected, its characterization run must be separately authorized and tightly fenced as a calibration measurement ONLY - it measures a macro-excursion scale, does not classify candidates, does not inspect LowLow, does not tune on observables, and does not adapt constants inside the swept run.

## 5. The first-pass finding is not moved; the failure-precision is carried

This resolution does NOT reopen or move the first-pass scoped-negative finding, which stands: scoped negative for the predeclared standardized-gain design, mechanism class not closed, block-resolved guard vindicated. The precision Layer 2 added is carried forward: the first-pass failure was calibration-internal to the UNBOUNDED standardized-gain construction and exposed an over-driven feedback mode; it does not close Rule E, but it argues against another unbounded linear standardized pass as the next instrument. Modified-A is selected precisely because it bounds the realized term rather than re-scaling an unbounded one.

## 6. Synthesis note (recorded honestly)

The convergence on modified-A is recorded as genuine-with-a-caveat. Layer 2's selection of A over B/C rests on substantive grounds independent of Layer 1's framing - the unbounded-linear-risk argument against C, and the characterization-seed economy of A - AND it caught a real defect in Layer 1's A (the global-d_max identical-tiers pathology), which is independent evidence of substantive engagement rather than soft agreement. The caveat: Layer 1's proposal memo (Section 4) had already framed A as the simplicity / seeding-economy option, so part of L2's preference for A may be Layer 1 framing returning through L2. This does not overturn the selection - L2's tier-specific catch and unbounded-linear-risk argument go beyond Layer 1's simplicity point - but it is recorded so the selection is not treated as fully independent arbitration. B and C are held as genuinely admissible-under-discipline (the freeze was HARDENED by L2 into seven formal conditions, not waved off), not as rejected.

## 7. What this resolution does not do

- It does not seed a probe (neither a characterization run - modified-A needs none - nor a swept run).
- It does not draft an implementation spec.
- It does not authorize Layer 3 implementation.
- It does not specify a final alpha-tier count or run length beyond pointing at the first-pass tiers and the contract Section 5 recording-adequacy minimum (>= 12 post-burn-in conditioned macro blocks).
- It does not amend the Rule E design contract or any rested arc; it selects a construction within the contract.
- It does not touch the L4 ontological question; no part of modified-A reads an observable back into the rule, and the observable-feedback exclusion continues to protect it.

The natural next artifact, when and if Mike opens it, is the bounded-A implementation spec - which would honor this resolution, the contract, the opens resolution, the F3 alpha-zero bypass constraint, the additional diagnostics and saturated-channel flag of Section 3, and the Layer 3 recording structure. Drafting that spec is Mike's call; seeding its run is a further separate call.

- Layer 1 (Claude); Layer 2-recommended; Mike-arbitrated
