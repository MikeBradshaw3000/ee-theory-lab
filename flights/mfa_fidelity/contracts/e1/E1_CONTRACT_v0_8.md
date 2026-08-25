# Contract E1 — Fixed-Terrain Activation Threshold (Cascade Existence, First Transition)
## Draft v0.8 (changed-text-only; resolves the five v0.7 corrections; for Mike's review, then L2 changed-text verification)

**Status:** DRAFT. No production run authorized. Carries v0.7 in full except the exact passages amended below. No scientific content changes; every amendment is an executable-definition or naming repair.

---

## A. Informativeness rule — false equivalence removed (item 1)

The operative rule is the **two endpoint conditions, and only them**:
**e_L = max(0, m₋ᴿ − L_env) ≤ Δm_loc  and  e_U = max(0, U_env − m₊ᴿ) ≤ Δm_loc.**
The total-width inequality formerly offered as equivalent is **withdrawn as an implementation** — it can pass under one-sided displacement that violates an endpoint bound; it may be mentioned only as a consequence under additional containment conditions, never as the gate. Both e_L and e_U are reported in the stage-1 package.

## B. Three resolution scales, three ledger symbols (item 2)

- **Δm_stab** — alternate-reference endpoint displacement allowance (stability audit).
- **Δm_est** — bootstrap 95% CI half-width allowance on each envelope endpoint estimate (estimation precision).
- **Δm_loc** — envelope outward-expansion allowance (design-location resolution; the §A gate).
The former double-role use of Δm_R for the first two is **retired**; **Δm_R now names exactly one thing: the reference-side departure-zone width** (T1/T3 exemption), its original role. Mike may set two or all of Δm_stab, Δm_est, Δm_loc to equal numerical values; they remain separately named, separately adjudicated, and separately reported (observed displacement vs. Δm_stab; CI half-width vs. Δm_est; e_L, e_U vs. Δm_loc) because equal values do not merge epistemic functions.

## C. Exact spacing conventions (item 3)

All spacing-derived scales resolve to exact six-decimal numbers by named rules:
- **s_P1^nom = round₆(0.70 / 23) = 0.030435** — the nominal pass-1 spacing.
- **s_P1^max = max_j (m_{j+1} − m_j)** over the frozen six-decimal pass-1 level list — the realized maximum spacing (adjacent realized spacings may differ by one unit in the sixth decimal; the frozen list decides).
- **Δm_loc [PROPOSED] = s_P1^max.**
- **Δm_R (departure-zone width) = round₆(s_P1^nom / 9) = 0.003382** — the former "pass-1 spacing / 9" made exact.
- **Δm_stab [PROPOSED] = 0.003382; Δm_est [PROPOSED] = 0.003382** — numerically equal to Δm_R's value at proposal, independently settable at freeze per §B.
Every carried reference to "pass-1 spacing" or fractions of it anywhere in this contract resolves through these named rules and no other way.

## D. Primary-relative displacement, explicit (item 4)

The stability audit's UNIQUE-THRESHOLD condition is stated as equations: for each alternative construction,
**|m₋ᴿ_alt − m₋ᴿ_primary| ≤ Δm_stab  and  |m₊ᴿ_alt − m₊ᴿ_primary| ≤ Δm_stab.**
Adverse/unresolved primary classes: structure-class agreement only, as carried. Class change under any alternative: freeze blocked, as carried.

## E. Collision fallback — completed or removed (item 5)

The proof path carries as preferred, its required coverage now enumerated: all P2R-5 and P2R-6 single-band refinements; each half of P2R-4's 4+4 allocation while that documentary row remains; six-decimal rounding before every collision check; collisions against pass-1 levels and among inserted points. **If the proof closes, the fallback text is removed as unreachable.**
**If the proof fails, the fallback is completed as follows and frozen:**
- Neighbors are **the immediate accepted predecessor strictly below the nominal candidate and the immediate accepted successor strictly above it, both within the candidate's original P2R refinement interval**; if either does not exist, the candidate is dropped.
- All arithmetic in **exact integer micro-units k = m × 10⁶**: midpoint computed in integer coordinates; **round-half-to-even applied explicitly** on the half-unit case; converted back to the six-decimal control value.
- Ascending nominal-m processing, moved-point neighbor eligibility, strict interiority, strict sorted order, drop-on-failure, and full downstream mirroring all carry unchanged from v0.7.
Two conforming implementations produce identical level lists by construction under either branch.

## F. Stage-1 reporting (consolidated)

The package reports, as separately named results: primary and every alternative null calculation vs. the pointwise precision rule; reference structure classes and primary-relative displacements vs. Δm_stab; endpoint CI half-widths vs. Δm_est; e_L and e_U vs. Δm_loc; the exact frozen level list and its realized spacings under §C's conventions; T2-S design-stability bounds; the collision proof or completed-fallback test; final ensemble sizes; and all prior conformance, closure, audit, and resource deliverables.

*End of draft v0.8. Sequence: Mike's review → L2 changed-text verification → freeze qualification (stage 1).*
