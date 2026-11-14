# L1 → L2 — Flight 9: contract review of Contract F9 v0.4 (round 3)

**Register.** Contract review, round 3. No instrument, master or canonical data exists for Flight 9. **Pinned to:** `ee-theory-lab` `main` at `2781789af93047e834eb873c3390e5ef9ba0c5a6`. Every file in this packet except this document was extracted from that commit (fresh clone); this document is new and is committed with your return.
**Authority.** Mike rules. His rulings recorded in the draft stand unless he changes them on your return. Nothing is authorized by this packet.
**Scope fixed by Mike, not open here.** Terrain and composition; between-cell heterogeneity only; no Regime II, Ψ or coherence observable; onset continuity is not in Flight 9.
**Review against the committed record only.** The packet contains no Annex material.

## 1. Packet contents (at repository paths)

| Path | Why it is here |
|---|---|
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_4_REVIEW_ROUND3_2026-11-14.md` | this document |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_4.md` | **the object reviewed** |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_3.md` | the version you reviewed in round 2 |
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_3_REVIEW_ROUND2_2026-11-13.md` | the round-2 instruction document, as shipped |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_3_ROUND2_REVIEW_2026-11-13_RECEIVED.md` | your round-2 review, as committed |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_2_ROUND1_REVIEW_2026-11-13_RECEIVED.md`, `L1_TO_L2_F9_CONTRACT_V0_2_DISCUSSION_2026-11-13.md`, `L2_F9_CONTRACT_V0_2_DISCUSSION_RESPONSE_2026-11-13_RECEIVED.md` | round 1 and its discussion, for the trace of §12.1 |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_4/` (five scripts, two JSON outputs) | the v0.4 prototype with traced components, the comparison arrays, the checks against your counterexamples, and your Appendix R program as extracted |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_3/` (six scripts, four JSON outputs) | v0.3's numbers, which v0.4 still cites (Appendix A.1–A.6, A.8) |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_3.md` | the governing design text |
| `flights/mfa_fidelity/design/flight9/L2_F9_DESIGN_CONSULTATION_2026-11-12_RECEIVED.md` | your design consultation |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | the claim grammar fixed before any data |
| `flights/mfa_fidelity/design/flight9/probe/F9_PROBE_RECORD_2026-11-12.md`, `F9_PROBE_REPORT_2026-11-12.json`, `F9_PROBE_IDENTITIES.json` | what the probe showed and what L1 has seen |
| `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | terrain formulas and the spectral routine; the scripts take its path as their first argument |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md`, `FLIGHT_8_FREEZE_RECORD.md` | the frozen predecessor |
| `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md` | the close and its obligations forward |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md`, `PD_PARTICIPATION_RULINGS_PD1_PD7.md`, `NOTATION_SCOPE_RULING_v1_1.md` | flicker obligation; PD5, PD7; the translation table |
| `flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md` | the committed F labels |
| `theory/overview/EE_emergence_overview_v1_8_1.md` | the statement of record |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py`, `config.py` | the placed scalar step |
| `MANIFEST.txt` | SHA-256 of every file above |

**First part of your reply:** a receipt table (file count, and each file's hash against the manifest). Then wait for Mike's "execute".

## 2. Disclosures

1. **Mike's ruling on your round-2 return:** "f3 descriptive and proceed directly". The contour-constancy report is descriptive only, and v0.4 was written without a discussion round. L1 agreed with every round-2 finding and re-ran your Appendix R program against the packet bytes; both counterexamples reproduced.
2. **Your Appendix R program is committed as `arith_v0_4/l2_appendix_r.py`**, extracted from your review with the four-space indentation removed. If it differs from what you wrote, say so.
3. **F1 and F2 were repaired and then tested against your cases on synthetic maps** (`proto_checks_v4.json`): the displaced loop scores 10.0 where v0.3 scored 0; the TC translation is compatible under both P and H at 2.0. The v0.4 prototype is not an instrument module.
4. **The near-ε strata changed.** A compatible map translated k cells has certified Δ* = k (`strata_attainability.json`), so 1.5 and 2.5 are not attainable by integer translation. v0.4 uses bands: "1.0", "between 1 and 2", "2.0", "between 2 and 3", "3.0", filled by certified truth. L1 has not computed which values diagonal translations give.
5. **Contract §11.2 lists six items proposed for Mike's decision at ratification.** The sixth, the comparison arrays, is new in v0.4.
6. **L1 has still not seen the boundary endpoint.** No occupancy map was rendered from probe output, nothing from probe output was computed against λ contours, and no edge was extracted from it. Please do not ask for any such computation.
7. **TB with r = 0.3 and all four TD variants have never been run.**
8. **Reproduction notes.** `proto_checks_v4.py <path to f9_probe.py> <out.json>` reproduces `proto_checks_v4.json` byte for byte in L1's container; it contains one seeded Monte Carlo value (`clip_mean_monte_carlo`) that could differ under another NumPy. `strata_attainability.py` takes about four minutes and its `timing` block is machine-dependent. Run the v0.4 scripts from their own directory without the interpreter's isolated mode. The v0.3 notes still apply to `arith_v0_3/`.
9. **Numbers are container values** (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1); array hashes are provisional (contract §3.4).
10. **v0.4 was produced from v0.3 by replacement of the affected passages.** Passages you cleared in round 2 and that no repair touched are byte-identical to v0.3; the v0.3 change list is retained in the header as history.

## 3. Questions

**Q1. Closure of the round-2 repairs.** For each of F1 to F7, and for your Q3 points on m = 40, say **CLOSED**, **CLOSED WITH NOTE**, or **NOT CLOSED** (say what remains). Contract §12.0 gives the section for each. Please also say whether R2, R5, R6, R7, R9 and R10 of round 1, which you held open in round 2, are now closed.

For Q2 to Q7 please give a plain disposition: **ACCEPTABLE**, **REQUIRES CHANGE** (say what), or **REJECT** (say why and what instead).

**Q2. The traced component convention (§5.5 step 3; `f9_evaluator_proto_v4.py::edge`).** Is "connected piece of the boundary" with the stated corner rule well defined on the torus, and does the prototype implement it? Is the pruning argument unaffected?

**Q3. The comparison arrays (§3.3; §3.4 steps 3–4; §5.5 step 5).** Do they remove the dependence of any decision on separate rounding? Is the stated relation between ω and the raw index used by the dynamics sufficient, and is rounding ω to 12 places itself able to change a decision in a way that matters?

**Q4. The qualification declaration (§6.0–§6.2):** the truth definition; the clipped-mean certification; the sampling laws; the strata bands and assignment by certified truth; the sweep and flight constructions; the calibration transformations with their fallbacks and typed stops; the error table.

**Q5. The descriptive constancy report (§1.3 b; §5.7).** Does it now claim only what it can support? Is the matched noise estimate stated correctly?

**Q6. The persistence profile table (§5.4)** and the markers on the 36-of-40 count.

**Q7. The conforming repairs of F6 and the provenance repairs of F7:** is anything still inconsistent or unprovenanced?

**Q8. Anything else that would prevent a freeze.**

## 4. What happens next

Mike rules on your return. Before freeze Mike may invoke the Gemini corpus audit. Nothing is authorized by this packet.

**Return format.** One downloadable `.md` file, receipt table first. End with one overall line, plain at column 0, in one of these forms:
`CONTRACT DISPOSITION: FREEZABLE AS A CONTRACT CANDIDATE`
`CONTRACT DISPOSITION: NOT YET FREEZABLE`

*L1, 2026-11-14. Nothing placed beyond the ten files of this commit; no run; nothing in `f8` or `e1` modified.*
