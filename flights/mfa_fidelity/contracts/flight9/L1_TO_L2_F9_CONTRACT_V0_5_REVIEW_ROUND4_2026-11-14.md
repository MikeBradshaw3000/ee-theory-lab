# L1 → L2 — Flight 9: contract review of Contract F9 v0.5 (round 4)

**Register.** Contract review, round 4. No instrument, master or canonical data exists for Flight 9. **Pinned to:** `ee-theory-lab` `main` at `9b1a0d9c3615472b5c888d39f7ec0b9c719a02d1`. Every file in this packet except this document was extracted from that commit (fresh clone); this document is new and is committed with your return.
**Authority.** Mike rules. His rulings recorded in the draft stand unless he changes them on your return. Nothing is authorized by this packet.
**Scope fixed by Mike, not open here.** Terrain and composition; between-cell heterogeneity only; no Regime II, Ψ or coherence observable; onset continuity is not in Flight 9.
**Review against the committed record only.** The packet contains no Annex material.

## 1. Packet contents (at repository paths)

| Path | Why it is here |
|---|---|
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_5_REVIEW_ROUND4_2026-11-14.md` | this document |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_5.md` | **the object reviewed** |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_4.md` | the version you reviewed in round 3 |
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_4_REVIEW_ROUND3_2026-11-14.md` | the round-3 instruction document, as shipped |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_4_ROUND3_REVIEW_2026-11-14_RECEIVED.md` | your round-3 review, as committed |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_3_ROUND2_REVIEW_2026-11-13_RECEIVED.md`, `L2_F9_CONTRACT_V0_2_ROUND1_REVIEW_2026-11-13_RECEIVED.md`, `L1_TO_L2_F9_CONTRACT_V0_2_DISCUSSION_2026-11-13.md`, `L2_F9_CONTRACT_V0_2_DISCUSSION_RESPONSE_2026-11-13_RECEIVED.md` | rounds 1 and 2, for the trace of §12 |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_5/` (three scripts, two JSON outputs) | the zero-noise support checks of the strip fixture and of the special constructions; the registered-family counts; your round-3 Appendix R program as extracted |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_4/` (five scripts, two JSON outputs) | the prototype and comparison arrays, which the v0.5 scripts import |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_3/` (six scripts, four JSON outputs) | v0.3's numbers, which v0.5 still cites (Appendix A.1–A.6, A.8) |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_3.md` | the governing design text |
| `flights/mfa_fidelity/design/flight9/L2_F9_DESIGN_CONSULTATION_2026-11-12_RECEIVED.md` | your design consultation |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | the claim grammar fixed before any data |
| `flights/mfa_fidelity/design/flight9/probe/F9_PROBE_RECORD_2026-11-12.md`, `F9_PROBE_REPORT_2026-11-12.json`, `F9_PROBE_IDENTITIES.json` | what the probe showed and what L1 has seen |
| `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | terrain formulas and the spectral routine; the scripts take its path as their first argument |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md`, `FLIGHT_8_FREEZE_RECORD.md` | the frozen predecessor |
| `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md` | the close and its obligations forward |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md`, `PD_PARTICIPATION_RULINGS_PD1_PD7.md`, `NOTATION_SCOPE_RULING_v1_1.md` | flicker obligation; PD5, PD7; the translation table |
| `flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md` | the committed F labels |
| `theory/overview/EE_emergence_overview_v1_8_2.md`, `README.md` | the statement of record since `47272f2`, and the directory's register |
| `theory/overview/EE_emergence_overview_v1_8_1.md` | the previous statement of record, which v0.4 cited |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py`, `config.py` | the placed scalar step |
| `MANIFEST.txt` | SHA-256 of every file above |

**First part of your reply:** a receipt table (file count, and each file's hash against the manifest). Then wait for Mike's "execute".

## 2. Disclosures

1. **Mike's ruling on your round-3 return (2026-11-14):** "I accept your recommendation". L1 had recommended your minimal repair for R3-1 (keep the registered rounded arrays; narrow B and its adverse cause to the registered family) rather than a family-preserving alternative, and proceeding directly to v0.5 without a discussion round. L1 agreed with both round-3 findings and ran your Appendix R program against the round-3 packet bytes; every figure reproduced.
2. **Your Appendix R program is committed as `arith_v0_5/l2_round3_checks.py`**, extracted from the fenced block of your review. If it differs from what you wrote, say so.
3. **The repository moved between your round-3 packet and this one for a reason outside Flight 9.** Mike registered Overview v1.8.2 as the statement of record at `47272f2` (a wording conformance; its README says no equation, regime or commitment is altered and no flight document changes). v0.5 was first built at `2781789`, then rebuilt before commit so that §10 cites v1.8.2 and §13 no longer lists it as held. L1 compared the two Overview files on the sentences using β, μ(ρ) and Λ*; they are unchanged, or changed only in prose about the bases and Q. v1.8.2 now says the bases "do not combine as a weighted index" and excludes a fixed global weighting. H is a fixed equal weighting; the contract treats it as a rival only and claims no selection (§1.1′, §2.2), and L1 changed nothing there.
4. **What L1 computed for R3-2, and its limit.** At zero noise, on synthetic maps only: the strip fixture's six cases (`fixture_checks_v5.json`); on each of the eight comparison arrays, the untranslated generic sweep (COMPATIBLE, 25 of 25 informative), the sweep translated 3 cells along axis 0 (ADVERSE, 25 of 25), and the low-information construction at each of its 24 positions (NOT DISTINGUISHED, exactly two informative); TB cross-scoring for both generating indices (`special_constructions_v5.json`). These use the prototype's pruned search for the decisions and brute force for the strip fixture and the diagonal translations. They show the constructions can be built. They are not certificates under calibration-derived noise, where §6.0 governs acceptance, and L1 has not shown that every stratum fills within the budget.
5. **New PROPOSED values in v0.5** (contract §11.2 item 7): the strip fixture; the special constructions; the band "0" = [0, 0.5] for the compatible sensitivity row; 10,000 candidates per stratum; 50 cases for each of the four unavailable states in row 15. §11.2 now lists seven items for Mike's decision at ratification.
6. **The ADVERSE construction translates along axis 0 only.** A translation along axis 1 leaves TB under H compatible at every level (its contours are lines of constant x).
7. **L1 has still not seen the boundary endpoint.** No occupancy map was rendered from probe output, nothing from probe output was computed against λ contours, and no edge was extracted from it. Please do not ask for any such computation.
8. **TB with r = 0.3 and all four TD variants have never been run.**
9. **Reproduction notes.** `fixture_checks_v5.py` and `special_constructions_v5.py` each take `<path to f9_probe.py> <path to arith_v0_4> <out.json>` and reproduce their JSON byte for byte in L1's container from a fresh clone (about 4 and 35 seconds there). Run them without the interpreter's isolated mode. The earlier notes still apply to `arith_v0_3/` and `arith_v0_4/`.
10. **Numbers are container values** (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1); array hashes are provisional (contract §3.4).
11. **v0.5 was produced from v0.4 by replacement of the affected passages.** Changed: the header; §1.0 (errors list); §1.1; §1.2 B and one word of D; §1.5 A5; §3.4 step 3; §5.5 steps 5, 7, 8; §6.1 classes 16 and 24; all of §6.2; §7 L7; §8 steps 7–8; §9 (two rows); §10 (column head); §11; §12.0; §13; Appendix A.9 and A.10. Every other passage is byte-identical to v0.4.

## 3. Questions

**Q1. Closure of the round-3 repairs.** For each of R3-1 and R3-2 say **CLOSED**, **CLOSED WITH NOTE**, or **NOT CLOSED** (say what remains). Contract §12.0 gives the sections. Please also say whether F4 and the m = 40 strata, which you held open in round 3, are now closed.

For Q2 to Q5 please give a plain disposition: **ACCEPTABLE**, **REQUIRES CHANGE** (say what), or **REJECT** (say why and what instead).

**Q2. Scope of the comparison family (§1.1; §1.2 B; §3.4 step 3; §5.5 steps 5, 7, 8; §7 L7; §9; §6.1 class 24).** Is the scope stated consistently wherever the contract speaks of a level set, a contour or an adverse cause? Does any remaining sentence claim more than the registered family supports?

**Q3. The strip fixture (§6.2; §6.1 class 16; A.10).** Is it declared completely enough to build: geometry, draws, pre-noise maps, family and certificate? Is it clear which rows use it and which use canonical arrays? Is anything about a one-contour binary index unsuitable for these rows?

**Q4. The special arm and flight constructions and their acceptance (§6.2, rows 16–24).** Does each fix every choice (positions, slots, the drawn arm and level, dependence)? Is each row's acceptance condition the right certified truth, in particular rows 19, 22 and 23?

**Q5. The remaining declarations (§6.2):** one capped stratum per component size and per noise level; the sensitivity error event of rows 6–9; the allocation in row 15; the pooled-ratio ρ₁ with its zero-map and zero-denominator treatment; the candidate budget and `stratum not populated`.

**Q6. Anything else that would prevent a freeze,** including anything the Overview's change of version touches that L1 has missed.

## 4. What happens next

Mike rules on your return. Before freeze Mike may invoke the Gemini corpus audit. Nothing is authorized by this packet.

**Return format.** One downloadable `.md` file, receipt table first. End with one overall line, plain at column 0, in one of these forms:
`CONTRACT DISPOSITION: FREEZABLE AS A CONTRACT CANDIDATE`
`CONTRACT DISPOSITION: NOT YET FREEZABLE`

*L1, 2026-11-14. Nothing placed beyond the eight files of this commit; no run; nothing in `f8` or `e1` modified.*
