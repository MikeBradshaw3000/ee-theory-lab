# L1 → L2 — Flight 9: contract review of Contract F9 v0.6 (round 5)

**Register.** Contract review, round 5. No instrument, master or canonical data exists for Flight 9. **Pinned to:** `ee-theory-lab` `main` at `5d426c6ef086b4ff9fb02337956e9769a3203011`. Every file in this packet except this document was extracted from that commit (fresh clone); this document is new and is committed with your return.
**Authority.** Mike rules. His rulings recorded in the draft stand unless he changes them on your return. Nothing is authorized by this packet.
**Scope fixed by Mike, not open here.** Terrain and composition; between-cell heterogeneity only; no Regime II, Ψ or coherence observable; onset continuity is not in Flight 9.
**Review against the committed record only.** The packet contains no Annex material.

## 1. Packet contents (at repository paths)

| Path | Why it is here |
|---|---|
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_6_REVIEW_ROUND5_2026-11-15.md` | this document |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_6.md` | **the object reviewed** |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_5.md` | the version you reviewed in round 4 |
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_5_REVIEW_ROUND4_2026-11-14.md` | the round-4 instruction document, as shipped |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_5_ROUND4_REVIEW_2026-11-14_RECEIVED.md` | your round-4 review, as committed |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_4_ROUND3_REVIEW_2026-11-14_RECEIVED.md`, `L2_F9_CONTRACT_V0_3_ROUND2_REVIEW_2026-11-13_RECEIVED.md`, `L2_F9_CONTRACT_V0_2_ROUND1_REVIEW_2026-11-13_RECEIVED.md`, `L1_TO_L2_F9_CONTRACT_V0_2_DISCUSSION_2026-11-13.md`, `L2_F9_CONTRACT_V0_2_DISCUSSION_RESPONSE_2026-11-13_RECEIVED.md` | rounds 1 to 3, for the trace of §12 |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_6/` (one script, one JSON output) | the zero-noise support check of the four unavailable-state recipes |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_5/` (three scripts, two JSON outputs) | the fixture and special-construction checks you reproduced in round 4 |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_4/` (five scripts, two JSON outputs) | the prototype and comparison arrays, which the later scripts import |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_3/` (six scripts, four JSON outputs) | v0.3's numbers, which v0.6 still cites (Appendix A.1–A.6, A.8) |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_3.md` | the governing design text |
| `flights/mfa_fidelity/design/flight9/L2_F9_DESIGN_CONSULTATION_2026-11-12_RECEIVED.md` | your design consultation |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | the claim grammar fixed before any data |
| `flights/mfa_fidelity/design/flight9/probe/F9_PROBE_RECORD_2026-11-12.md`, `F9_PROBE_REPORT_2026-11-12.json`, `F9_PROBE_IDENTITIES.json` | what the probe showed and what L1 has seen |
| `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | terrain formulas and the spectral routine; the scripts take its path as their first argument |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md`, `FLIGHT_8_FREEZE_RECORD.md` | the frozen predecessor |
| `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md` | the close and its obligations forward |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md`, `PD_PARTICIPATION_RULINGS_PD1_PD7.md`, `NOTATION_SCOPE_RULING_v1_1.md` | flicker obligation; PD5, PD7; the translation table |
| `flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md` | the committed F labels |
| `theory/overview/EE_emergence_overview_v1_8_2.md`, `README.md`, `EE_emergence_overview_v1_8_1.md` | the statement of record, the directory's register, and the previous version |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py`, `config.py` | the placed scalar step |
| `MANIFEST.txt` | SHA-256 of every file above |

**First part of your reply:** a receipt table (file count, and each file's hash against the manifest). Then wait for Mike's "execute".

## 2. Disclosures

1. **Mike's ruling on your round-4 return (2026-11-14):** "I accept your recommendation". L1 had put one choice to him: whether the constant-map unavailable state is capped at every value including θ, or capped away from θ with a band near θ run and reported without a cap. L1 recommended the second, on the ground that no required arm has a flat population map (only T0, which §5.5 never scores), so a cap at θ could close the stage over a case the flight cannot meet, while the near-θ behaviour is still measured and published. He accepted that and directed v0.6 without a discussion round. L1 agreed with R4-1 as you stated it: the informative requirement L1 wrote into v0.5 made row 15 impossible to fill.
2. **One reading in v0.6 that you did not ask for, and may not accept.** You asked that wrong-cause and halt accounting be retained in row 15. v0.6 counts as an error, for the constant, saturated and empty states, a decisive record (compatible or adverse, for either index) or a halt. It does not count an unresolved record or a not-informative record under a cause other than `no edge at θ`: sample fluctuation can give a sample map a small or unstable region, and `under-resolved` or `unstable edge` is then a correct description of that sample. The counts of every output are reported per state. For the constant index, where the cause cannot depend on the sample, every output other than `no eligible contour` is an error. L1 took this from your round-3 remark that a correctly diagnosed sample-edge loss is not automatically a wrong cause. Mike has been told of this reading and that it goes to you as a question. If you hold that the named cause must be required, say what the error event should be.
3. **The saturated state is a constant map on [0.60, 1.00].** It differs from the constant state only in range. L1 kept it as a separate quota because you named four states; if you consider it redundant, say so.
4. **What L1 computed for R4-1, and its limit** (`unavailable_states_v6.json`; zero noise, synthetic maps only): a constant map has an empty region across [0.03, 0.14] and a full one across [0.26, 0.40] and [0.60, 1.00]; the low map is empty on each of the eight comparison arrays; the constant array's family is empty; the generic level map is informative on each of the eight arrays at the four corners of its coefficient ranges. The last check is at corners only, not over the whole coefficient rectangle. Under calibration noise the typed state is certified on the clipped population map.
5. **New PROPOSED values in v0.6** (contract §11.2 item 7): the four recipes and their ranges; the four quotas of 50 with 2,500 candidates each; row 15's error event; the half-width 0.06 of the band near θ (three times the 0.02 standard-error ceiling of §1.5 A2). The treatment of that band, reported and not capped, is ruled.
6. **L1 has still not seen the boundary endpoint.** No occupancy map was rendered from probe output, nothing from probe output was computed against λ contours, and no edge was extracted from it. Please do not ask for any such computation.
7. **TB with r = 0.3 and all four TD variants have never been run.**
8. **Reproduction notes.** `unavailable_states_v6.py` takes `<path to f9_probe.py> <path to arith_v0_4> <out.json>` and reproduces its JSON byte for byte in L1's container from a fresh clone. Run it without the interpreter's isolated mode. The earlier notes still apply to the earlier directories.
9. **Numbers are container values** (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1); array hashes are provisional (contract §3.4).
10. **v0.6 was produced from v0.5 by replacement of the affected passages.** Changed: the title and header; §1.0 (errors list); §1.5 A7; §6.2 (a new paragraph of unavailable-state recipes; the informative sentence in "Assignment by certified truth"; the candidate budget; the table's preamble, row 15 and a new row 25; the paragraph after the table); §9 (qualification row); §11; the head of §12; Appendix A.9 and A.10; the closing line. Every other passage is byte-identical to v0.5.

## 3. Questions

**Q1. Closure.** Say **CLOSED**, **CLOSED WITH NOTE**, or **NOT CLOSED** (say what remains) for R4-1, and with it for R3-2 and F4, which you held open for row 15 alone.

For Q2 to Q4 please give a plain disposition: **ACCEPTABLE**, **REQUIRES CHANGE** (say what), or **REJECT** (say why and what instead).

**Q2. The four recipes (§6.2, unavailable-state cases).** Is each complete: comparison array, pre-noise map, draw law, noise, expected cause? Does the constant-index recipe avoid every division by a zero range? Is any range poorly chosen?

**Q3. Typed truth and the error event (§6.2: assignment by certified truth; row 15; the paragraph after the table).** Is the certificate stated correctly against §7's precedence? Is the informative requirement still in force for every row whose truth needs an informative boundary? Is the error event of disclosure 2 acceptable?

**Q4. Quotas, budget and row 25.** Are the four quotas bound to the budget so that no state can replace another? Is the uncapped row 25 declared completely enough to build and report?

**Q5. Anything else that would prevent a freeze.**

## 4. What happens next

Mike rules on your return. Before freeze Mike may invoke the Gemini corpus audit. Nothing is authorized by this packet.

**Return format.** One downloadable `.md` file, receipt table first. End with one overall line, plain at column 0, in one of these forms:
`CONTRACT DISPOSITION: FREEZABLE AS A CONTRACT CANDIDATE`
`CONTRACT DISPOSITION: NOT YET FREEZABLE`

*L1, 2026-11-15. Nothing placed beyond the five files of this commit; no run; nothing in `f8` or `e1` modified.*
