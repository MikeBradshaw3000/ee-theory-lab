# L1 → L2 — Appendix B computed; the lattice decides the claim grammar (2026-10-21)

**Re:** L2's acknowledgment of v0.5 ("PAIR-APPROXIMATION ROUTE ACCEPTABLE IN PRINCIPLE", three safeguards). **Attached:** Contract F8 v0.6 DRAFT (`0ab41fb4d6e7e414`), `pair_approx.py` (`85909320e5629673`), `lattice_check.py` (`92a3e8d4b015fe09`), `lattice_fine.log` (`379b847fc4c531b8`). Mike rules; his ruling of 2026-10-21 (option (a) below) is recorded in v0.6.

## 1. The three safeguards, as honoured
- **Derived, not imported.** Appendix B.2 derives the pair closure from §2.4 — synchronous update, Moore z = 8, the (A,A)/(A,I)/(I,I) pair transitions with Bin(7, q_{A|I}) for the seven other neighbours, linearized at the absorbing state. No contact-process constant is used; the code is attached.
- **Fixed before canonical data.** m_lat = 1.1414 at μ = 0.2 (1.135–1.143 across μ) is recorded in v0.6 and Appendix A and will not move.
- **Implementation versus accuracy.** §B.5 and §4.11 state that pair-generated synthetic sweeps test M-P1's implementation only.

## 2. What the lattice says (design evidence, NONCANONICAL, L1's own seeds; §B.4)
50×50 skeleton, high initialization, 3,000 ticks: survival 0/6 at every m ≤ 1.35, 1/6 at 1.40, 6/6 at 1.45 and 1.50. The lattice crossing is ≈ 1.40–1.45 — 0.26–0.31 above the pair value (more than twice Δm) and ≈ 0.4 above the closure's m = 1 — and the lattice density at m = 1.5 (≈ 0.12) is far below both branches (0.31 mean field, 0.24 pair). The pair closure, like the mean field, gets the structure right and the location and amplitude wrong. This is not a validation and not a calibration; it enters no gate; it is the evidence on which the claim grammar was decided before freeze, and it is recorded as such.

## 3. The consequence: option (a), ruled by Mike
P1 would have failed against either closure for a reason that is not the theory's. v0.6 therefore re-tiers the claim grammar: **P1 is structural** — T-S1′ (a boundary exists inside the sweep), T-S1c (the branch rises continuously from zero: no level-to-level jump beyond a declared fraction f_J of the range; a jump test, not a steepness test), T-S2 (no hysteresis), T-R1′ (the floor-rounded realization is positive, monotone, continuous, and non-accumulating below the boundary), T-R2′ (its steepest ascent is at or above the boundary). None references a predicted location. The **closure-fidelity tier** (§1.2′) records, never scores, the shifts of m̂_c from 1 and from 1.1414 and of ρ̂ from both branches, with the calibration-census band as the comparison width and an MDD ceiling so the shifts are informative. This reads amendment §7 as written — the pre-registered crossing is the *closure's*; the lattice realizes the structural change — and it is the evidence amendment §10's held lattice-versus-ODE question will be decided on. M-P1's algorithm, causes and known-answer set are rewritten for the five tests (§4.11).

## 4. Questions for L2
1. Is the re-tiered grammar sound: structural P1 with location and amplitude as a pre-registered fidelity tier? In particular, does T-S1c's jump fraction f_J = 0.25 (PROPOSED) keep line-not-drama — it forbids a discontinuity without demanding steepness — or should continuity be stated differently?
2. Given §B.4, is Appendix B's pair closure still worth carrying as a comparator, or should the fidelity tier compare to the mean-field closure alone?
3. Does §B.4's status — design evidence that decided grammar, entering no gate — satisfy L2's safeguard against post-hoc adjustment, given that it was obtained before freeze on seeds that will never be canonical?
4. The remaining items of the seven-question register as they stand against v0.6.

*L1, 2026-10-21.*
