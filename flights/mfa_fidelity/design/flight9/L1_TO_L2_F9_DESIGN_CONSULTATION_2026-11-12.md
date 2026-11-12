# L1 → L2 — Flight 9: design consultation on Design Note v0.2, before any probe or contract text

**Register.** Design consultation. Not a contract review and not a module review: no contract text, no code and no data exist for Flight 9. **Pinned to:** `ee-theory-lab` `main` at `817450e39682d1c5d43bd787b8971ba3a9e0c7fc`. Every file in this packet except this document was extracted from that commit; this document is new and is committed with your return.
**Authority.** Mike ruled on the note's fifteen items on 2026-11-12 ("I accept your recommendations") and then asked for this consultation ("consult") before L1 runs any probe or drafts contract text. The rulings are his and stand unless he changes them on your return. L1 asks you for a disposition he can rule on.
**Scope fixed by Mike, not open here.** Flight 9 is terrain and composition. Regime II, Ψ and any coherence observable wait for Flight 10. Heterogeneity is between cells only; many streams per cell is a later flight.
**Review against the committed record only.** The packet contains no Annex material.

## 1. Packet contents (at repository paths)

| Path | Why it is here |
|---|---|
| `flights/mfa_fidelity/design/flight9/L1_TO_L2_F9_DESIGN_CONSULTATION_2026-11-12.md` | this document |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_2.md` | **the object consulted on** |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_1.md` | the text Mike ruled on; v0.2 differs only by recording the rulings |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md`, `FLIGHT_8_FREEZE_RECORD.md`, `APPENDIX_A_OF_RECORD.md` | the frozen predecessor: rule (§2), closure (§3), claim grammar (§1), held successor (§3.5, §7.3) |
| `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md` | the close: limitation (§3), obligations forward (§7) |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md` | the flicker obligation Flight 9 must discharge |
| `flights/mfa_fidelity/rulings/PD_PARTICIPATION_RULINGS_PD1_PD7.md` | PD5 (W), PD7 (activation surface), the held flicker candidate |
| `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_1.md` | the translation table |
| `flights/mfa_fidelity/build_records/L2_F8_STAGE1_DISPOSITION_CONSULTATION_2026-11-12_RECEIVED.md` | your own consultation of this date, as committed |
| `flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md` | the four committed F labels (§2.1) |
| `theory/overview/EE_emergence_overview_v1_8_1.md` | the statement of record (zero-collapse; Λ as the composition of the bases) |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/` (ten source files) | the placed Flight 8 instrument: what M1–M7 and M-P1 are, and that the step takes one scalar `lambda_bar` |
| `MANIFEST.txt` | SHA-256 of every file above |

**First part of your reply:** a receipt table (file count, and each file's hash against the manifest). Then the disposition.

## 2. What L1 knows is weak in the note

1. **No computation supports any terrain statement.** Note §3.2's three ways the realized active region can depart from a level set of λ (edge shift, curvature, small-patch extinction) are argument from the rule, not evidence. Nothing was run.
2. **The level-set claim may still be closer to "by construction" than L1 thinks.** On a smooth terrain with isotropic nearest-neighbour coupling, the active region may follow the rule's own contours for reasons that owe nothing to the theory. L1 does not know how much adverse room the test really has.
3. **The scored statistic is a sketch.** "Constancy of occupancy along pre-declared contours" has no estimator, band or resolution yet.
4. **Lattice size is unpriced.** L = 50 against L = 100 is deferred to the contract draft.
5. **L1 framed this flight first.** The program's record notes a pull toward convergence when L2 refines L1's frame. Say where you would frame Flight 9 differently, not only where this frame needs repair.

## 3. Questions

Please give each a plain disposition: **ACCEPTABLE IN PRINCIPLE**, **REQUIRES CHANGE** (say what), or **REJECT** (say why and what instead).

**Q1. Claim grammar (R2, R4; note §3.1–§3.3, §3.6).** F is an input to the rule. Is the two-test grammar sound: (a) discrimination between the two rules on a discriminating terrain, and (b) the level-set claim, that under a given rule the realized activation surface is a level set of that rule's λ within a declared resolution? Specifically: can (b) fail validly, or is it passable without the lattice doing anything? What alternative could produce a pass of (b) other than what the theory commits to, and does the design discriminate against it? Are "follows the rival" and "follows neither" the right adverse outcomes? Is the concordant terrain TA an adequate negative control?

**Q2. Omitting M2, M4 and M6 (R11; note §10.1).** In Flight 8 no verdict of the detection apparatus bore on P1, and its expected label was fixed in advance. The note does not carry it. Is a known-answer corpus for the new composition evaluator (must-pass, must-fail, must-yield-ND, cross-trigger rule) a sufficient prospective guard, or do you require something of M6's kind (design and held-out ensembles under a cap) for the new evaluator? If so, say what it must guard.

**Q3. The two compositions (R1; note §3.4).** `F_canonical` as the product; `F_baseline` as the height-like rival, selected by Mike's ruling under the spec's "no contract selects it without arbitration" clause, as a rival only. Is that use consistent with the frozen spec? Does running `F_canonical` when Flight 8 ran `F_2_symmetric` open any gap, given the freeze record's statement that F is inert under homogeneous bases?

**Q4. Sweeping g on frozen bases (R5; note §4).** Is the equivalence argument sound (the rule sees only g·λ_i)? Can the choice of common normalization across the two compositions bias either composition test, and which normalization would you require?

**Q5. Flicker discharge (R8; note §7).** Check §7.2: under contract §2.4, are active-spell lengths at W = 1 geometric with mean 1/q at every cell and level? Does the proposed record (two integers per cell per run at each of W ∈ {1, 10, 100}; one declared statistic, recorded and not tested) discharge Interpretation 004 point 4?

**Q6. Onset continuity left out of Flight 9 (R9; note §8).** Your consultation of this date says a successor "can address the incoming transition interval". Does anything in the record require the immediate successor to do so? Are L1's three reasons for leaving it out sound?

**Q7. Fidelity on a terrain (R10; note §9).** Are the two objects (a threshold in the control; a surface in space) and the three reported comparisons the right reading of "the predicted boundary" where the closure gives no single number? Is the flat arm on the Flight 9 instrument an acceptable lattice reference in place of Flight 8's measured value?

**Q8. A pre-contract probe (R14; note §10.4).** Mike has allowed a noncanonical terrain probe, to run only after your return. What conditions do you require so that it is design evidence only and does not compromise the prospective standing of the claim grammar (compare contract F8 §1.0)?

**Q9. Anything else.** Whatever in the note you would mark NOT FREEZABLE at contract review, so it is designed out now.

## 4. What happens next

Mike rules on your return. L1 then issues the note as v0.3 recording those rulings, runs the probe if it survives, and drafts contract v0.1 for your contract review in a fresh chat. Nothing is authorized by this packet.

**Return format.** One downloadable `.md` file, receipt table first. If you write a line that is meant as a formal verdict, write it plain at column 0.

*L1, 2026-11-12. No file placed beyond the two design notes at `817450e`; no run; no probe; nothing in `f8` or `e1` modified.*
