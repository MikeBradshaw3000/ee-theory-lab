# L2 Packet — Contract F8 (Flight 8) v0.2 DRAFT: pre-freeze source review

**From:** L1 (Claude), routed by Mike. **To:** L2. **Date:** 2026-10-20.
**Register:** Flight 8 contract review — a **new register**, the one L2 said it was ready to open on 2026-10-20 ("ready to receive the Flight 8 contract packet under its separate review register"). The diagnosis register (closed: `eaa694a9…`) and the repair-design register (closed: `7e52670a…`, "form acceptable in principle; final contract values and qualification reserved") are not reopened; this packet is where their reserved items — the contract values and the qualification plan — come to L2.
**Requested review action:** adversarial source review of the draft contract **before freeze**: (1) the substrate rule and its null; (2) the closure, the pre-registered predictions and the tolerance procedures; (3) rule 4c(F8), W_res, the §4.6 clause and the §6 gap, as the contract-level realization of the accepted repair form; (4) the qualification order and fresh-guard registration; (5) whether folding the E1-R repair into Flight 8's instrument — rather than a successor E1 stage — is sound (the question L2's 2026-10-09 disposition left for this packet); (6) every value marked PROPOSED. Return explicit verdict language per item, with discriminating tests where needed, and a list of edits required before L2 would regard the text as freezable. **Not requested:** approval of any run, authorization, or production; Mike freezes.
**Authority:** advisory. Mike rules.

## 1. Source files (current; all at `21db4b8`, `main`, fresh-clone verified)

| File | sha256 (16) | Status |
|---|---|---|
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_2.md` | `88bd567c09c33841` | **the object of review** (DRAFT, NOT FROZEN) |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_1.md` | `696ec25e216fe32c` | superseded draft (two Gemini findings), retained |
| `flights/mfa_fidelity/contracts/flight8/README.md` | `25f2d88dcbf1548c` | directory status: DRAFT, NOT FROZEN |
| `protocols/audit/GEMINI_F8_AUDIT_2026-10-20_CONVERSATION_RECOVERED.md` | `f2ec62277a98d169` | Gemini corpus audit of v0.1 (read-only auditor; no verdict authority) |
| `protocols/audit/GEMINI_F8_AUDIT_TRIAGE_2026-10-20.md` | `92ad4a77ddebf09d` | L1 triage: 2 of 2 accepted, discharged in v0.2 |
| `flights/mfa_fidelity/design/flight8/FLIGHT_8_DESIGN_NOTE_v0_3.md` | `28824be51e661967` | design chamber record (context; not under review) |

Governing documents L2 already holds by identity: amendment `04058b21…`; pre-freeze response `314b56cc…`; dispositions `3f101a1b…`, `eaa694a9…`, `7e52670a…`; PD rulings `1b486323…`; notation ruling `c275c38f…`; Overview v1.8.1 `b2d67fac…`. Attached: the contract v0.2, the Gemini return and triage, the design note v0.3.

Superseded and never in play: nothing from E1-R carries by declaration; both E1-R masters are retired in the draft's §5.3.

## 2. Reported versus independently verifiable
- **Verifiable by L2 from the draft alone:** the map (§3.1) and its skeleton crossing (§3.2) are closed-form; the realization branch values L1 quoted in §2.7 (rounding half-widths at five μ) are reproducible from §3.1 by bisection in a few lines, and L2 is invited to reproduce them; the §4.6 inequality's logic is in the text.
- **Reported, design evidence only (burned ensembles, ideal classifier):** the pricing that fixed the *form* of 4c and the extent-bound test — both already before L2 in the repair-design register; no number from them is in the contract.
- **Not yet existing:** every DERIVED@BUILD value (fixed-point tables, Δm, w_mix, W_res, Δ_route, w_L, w_A, w_U, the margins, the masters). The packet asks L2 to review the *procedures* that will produce them, not values.

## 3. What is new since the repair-design register closed
1. **The rule in contract form** (§2): hazard activation 1 − exp(−[η_floor + g·λ_i·d_i]Δt), deactivation 1 − exp(−μΔt), synchronous, all terrain through the feedback channel, homogeneous frozen bases, Q off, drive zero, noise off; null = g → 0 with everything else fixed, stationary start. Two committed objects: skeleton η_floor = 0; realization η_floor = η₀ = −ln(0.99).
2. **The control coordinate** m = gλ̄Δt/(1 − e^(−μΔt)), so the skeleton's pre-registered crossing is m = 1 exactly; the sweep is in m.
3. **P1 as three structural tests** (T-S1 crossing location, T-S2 no hysteresis, T-R1 rounded continuation) with tolerance *procedures* from finite-size and null-fluctuation computations, not from any sweep; the detection boundary demoted to a secondary observable.
4. **μ = 0.2 PROPOSED**, with the design fact stated beside it: at η₀ ≈ 0.01 the realization's unfolding is soft at every plausible μ (half-width 0.5–1.1 in m), because it is governed by η₀/μ. This is where L2's judgement is most wanted (§4 Q2 below).
5. **M3**: θ_T exact by transfer matrix; θ_P by the familywise bound at α_P/10 per window, conservatism priced at qualification, simulation threshold as the named fallback — per L2's answer 3.
6. **Rule 4c(F8), W_res as a procedure (§4.5), the §4.6 residual-dependence clause, the §4.7 verdict grammar, and the §6 gap** as two inequalities with analytic extrema and a freeze refusal on non-positive margin — the contract-level realization of R1–R4.
7. **Archetype table (§5.2)** with `crossing_onset` added, the gentle/wide pair separated by the §6 rule, the NP classes carried with `no_null_consistent_anywhere` reinterpreted for the absorbing skeleton.
8. **Qualification order (§7.1)** and `skeleton_census` first (§7.3), per Mike's conditions 2 and 3.
9. **Notation rows (§9)** proposed for the translation table, including the η_floor hazard/probability row Gemini's F1 required.

## 4. Questions for L2
1. **Rule and null.** Is §2 an exact discrete-time rule in L2's §4.1 sense, with the null of §2.9 retaining everything but endogenous feedback (§4.4)? Any term L2 regards as a terrain-only drive that would break the skeleton's exact absorbing state?
2. **Softness of the unfolding.** Given η₀ ≈ 0.01 per tick, is the realization's rounding (§2.7) acceptable as the committed imperfect unfolding, or does L2 see a reason to commit a different η₀ (which would change the Overview's image) or a larger μ (which shortens persistence)? L1's view: the softness is a property of the theory's two committed objects and should be stated, not tuned away; but it makes T-R1's tolerance band the operative test and L2 should weigh whether §3.4's band procedure is discriminating.
3. **P1 tests and tolerances.** Are T-S1/T-S2/T-R1 the structural endpoint of amendment §7, and are the Δm and k_R procedures of §3.4 pre-registered tightly enough that no post-hoc latitude remains?
4. **W_res procedure (§4.5).** Is "predicted mixing window from the map plus the null's fluctuation width, times c = 2" a sound derivation of the declared resolution from the theory, keeping E1 data out?
5. **Gap (§6).** Do the two inequalities, with E_max/E_min as analytic extrema over seed-panel draws and Δ_route as the routing slack, discharge L2's answer 2 ("actual separation established before the fresh guard is drawn")?
6. **Folding the repair into Flight 8.** Is it sound to repair M4/M6 inside Flight 8's new instrument version rather than in a successor E1 stage, given that Flight 8 rebuilds M3 and the archetype table regardless (pre-freeze §4.8–§4.9) and that E1-R's projection-side result stands on its own?
7. **Freezability.** What must change in the text before L2 would regard it as freezable? (PROPOSED values L2 objects to; procedures L2 finds under-specified; anything in §1.4 or §10 that over- or under-claims.)

## 5. What follows
L2's disposition → contract v0.3 → Mike's ruling on PROPOSED values → freeze commit (RATIFIED named in the message; identity cited by the governance record) → instrument build and DERIVED@BUILD table committed → masters drawn → qualification. Gemini runs again on the freeze candidate only if the text changes materially from v0.2.

*L1, 2026-10-20. Identities from a fresh clone at `21db4b8`.*
