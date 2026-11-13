# L1 → L2 — Flight 9: contract review of Contract F9 v0.2 (first contract packet)

**Register.** Contract review, round 1. No instrument, code, master or canonical data exists for Flight 9. **Pinned to:** `ee-theory-lab` `main` at `d7c8312b7255b5bb4a927e1d97824d53ddaf056d`. Every file in this packet except this document was extracted from that commit (fresh clone); this document is new and is committed with your return.
**Authority.** Mike rules. His rulings recorded in the draft (marked RULED) stand unless he changes them on your return. L1 asks you for a disposition he can rule on. Nothing is authorized by this packet.
**Scope fixed by Mike, not open here.** Flight 9 is terrain and composition. Regime II, Ψ and any coherence observable wait for Flight 10. Heterogeneity is between cells only. Onset continuity is not in Flight 9.
**Review against the committed record only.** The packet contains no Annex material.

## 1. Packet contents (at repository paths)

| Path | Why it is here |
|---|---|
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_2_REVIEW_2026-11-13.md` | this document |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_2.md` | **the object reviewed** |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_1.md` | the draft Mike first read; superseded |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_QUESTIONS_ADVICE_2026-11-13_RECEIVED.md` | your advice of 2026-11-13 to Mike, as he attached it (§2 item 1 below) |
| `flights/mfa_fidelity/contracts/flight9/arith/` (six scripts, three JSON outputs) | every number in the draft; terrain arrays, Moore adjacency and closed-form constants only |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_3.md` | the governing design text with Mike's rulings on your design consultation |
| `flights/mfa_fidelity/design/flight9/L2_F9_DESIGN_CONSULTATION_2026-11-12_RECEIVED.md` | your design consultation, as committed |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | the claim grammar fixed before any data; what the probe may not adapt |
| `flights/mfa_fidelity/design/flight9/probe/F9_PROBE_RECORD_2026-11-12.md`, `F9_PROBE_REPORT_2026-11-12.json` | what the probe showed and what L1 has seen |
| `flights/mfa_fidelity/design/flight9/probe/f9_probe.py`, `f9_probe_report.py`, `F9_PROBE_IDENTITIES.json` | the probe's terrain formulas and spectral routine (the arith scripts import `f9_probe.py`); the declared report |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md`, `FLIGHT_8_FREEZE_RECORD.md` | the frozen predecessor and the pattern |
| `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md` | the close and its obligations forward |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md`, `PD_PARTICIPATION_RULINGS_PD1_PD7.md`, `NOTATION_SCOPE_RULING_v1_1.md` | flicker obligation; PD5, PD7; the translation table |
| `flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md` | the committed F labels |
| `theory/overview/EE_emergence_overview_v1_8_1.md` | the statement of record |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py`, `config.py` | the placed scalar step the new rule must reduce to |
| `MANIFEST.txt` | SHA-256 of every file above |

The probe's array files and its 450 KB manifest are not in the packet. The arrays are not in the repository.

**First part of your reply:** a receipt table (file count, and each file's hash against the manifest). Then the review.

## 2. Disclosures

1. **Your advice of 2026-11-13 was given without the draft.** Mike consulted you outside a packet on v0.1's ruling questions; you said you had neither the §11 wording nor the complete draft, and you did not have the probe record. Mike then told L1 to accept what it wanted of that advice and recommend on the rest, and ruled "as recommended". v0.2 is the result. Treat that advice as yours to revise now that you have the text.
2. **L1 departed from that advice in one place:** the 3×3 mean is kept as part of the occupancy estimator (contract §5.5 step 1). Island removal was dropped as you advised.
3. **L1 did not adopt a scored suppression contrast on TC.** Your advice left room for one. The probe had already shown that contrast (probe record §3 item 4), so it would not be prospective. It is reported only.
4. **θ = 0.20 was not chosen blind.** L1 had seen the probe report's occupancy percentiles (R-3) when proposing it (contract §1.0).
5. **L1 has not seen the boundary endpoint.** No occupancy map was rendered, nothing was computed against λ contours and no edge was extracted from probe output. Please do not ask for any such computation on probe output before the edge and tolerance rules are frozen.
6. **Two errors of L1's are recorded in the draft:** the probe record's statement that TC gives the two rules different spatial output (it was a difference of amplitude; contract §1.0, §3.3), and a wrong count in the recommendation Mike ruled on (contract v0.2 header, §11.2).
7. **The respecified TB and all four TD variants have never been run.** No evidence exists that either offers a usable edge at θ.
8. **Numbers are container values** (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1); array hashes are provisional (contract §3.4). The arith scripts take the path of `f9_probe.py` as their first argument and an output path as their second where they write JSON.

## 3. Questions

Please give each a plain disposition: **ACCEPTABLE**, **REQUIRES CHANGE** (say what), or **REJECT** (say why and what instead).

**Q1. Claim grammar as written (§1.1–§1.4, §3.3).** Do endpoints B and D, the bridge of §1.2″ and the limits of §1.4 implement what your design consultation required under Q1? Is anything claimed that the instrument cannot support?

**Q2. The occupancy criterion (§5.5 steps 1–2; §1.0).** A fixed θ = 0.20 for every arm, terrain and level, with 0.10 and 0.30 reported. Is a single scored threshold the right structure? Given disclosure 4, is θ's standing acceptable, and what would you require to make it so?

**Q3. The estimator and the edge (§5.5 steps 1, 3, 4).** The 3×3 mean kept; every component included; 4-neighbour bonds in place of Moore boundary cells; the informative-level counts. Does known-answer class 10 (§6.1) adequately test the departure of disclosure 2?

**Q4. The discrepancy and ε (§5.5 steps 5–8).** The symmetric 95th-percentile distance, the free level, and ε = 2.0 cells with its stated meaning, units, purpose and place in the rule. Is the definition sound? Is the value defensible on the stated basis? Does a free level over 99 candidates make compatibility too easy, and how should that be priced?

**Q5. Uncertainty (§5.5 step 9).** Percentile bounds from 1,000 resamples of 20 seed maps, one-sided 95%. Is this sound for a quantile-distance statistic minimized over a level, with 20 independent units?

**Q6. Aggregation (§5.6, §7).** The arm rule, including the two-adjacent-levels condition for ADVERSE; the conjunction over seven required arms per composition; D on TB alone; a required arm with no edge at θ recorded NOT DISTINGUISHED. Does the precedence table of §7 cover the cases your Q9 §11.6 listed?

**Q7. Diagnostic K (§1.3 a, §5.4).** The skeleton form is L1's proposal and you have not seen it before. Is it a coupling-sensitive contrast against the independent-response alternative of your consultation §3.3? Do survival counts, κ̂_c and its bracket meet your "effect estimate and uncertainty"? Disclosure: its outcome at 4 seeds is known from the probe (§1.0).

**Q8. Qualification (§6).** The eleven known-answer classes; the statistical qualification's classes, sizes and cap; the pricing of behaviour near ε. What is missing against the six risks of your consultation Q2?

**Q9. Anything else that would prevent a freeze.** Including: any REQUIRES CHANGE item of your design consultation that §12's trace table places wrongly or not at all; the T0 exercise (§5.8); the job list and record graph (§5.9, §8); array identities (§3.4); any number in the draft or Appendix A that the arith scripts do not reproduce.

## 4. What happens next

Mike rules on your return. L1 revises the contract for your next round. Before freeze Mike may invoke the Gemini corpus audit. Nothing is authorized by this packet.

**Return format.** One downloadable `.md` file, receipt table first. End with one overall line, plain at column 0, in one of these forms:
`CONTRACT DISPOSITION: FREEZABLE AS A CONTRACT CANDIDATE`
`CONTRACT DISPOSITION: NOT YET FREEZABLE`

*L1, 2026-11-13. Nothing placed beyond the twelve files at `d7c8312`; no run; nothing in `f8` or `e1` modified.*
