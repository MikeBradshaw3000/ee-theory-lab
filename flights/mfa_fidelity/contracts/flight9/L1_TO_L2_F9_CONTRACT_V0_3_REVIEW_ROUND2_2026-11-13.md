# L1 → L2 — Flight 9: contract review of Contract F9 v0.3 (round 2)

**Register.** Contract review, round 2. No instrument, master or canonical data exists for Flight 9. **Pinned to:** `ee-theory-lab` `main` at `dd17b53b6888a12db603d36522a9f67d441e0e07`. Every file in this packet except this document was extracted from that commit (fresh clone); this document is new and is committed with your return.
**Authority.** Mike rules. His rulings recorded in the draft stand unless he changes them on your return. Nothing is authorized by this packet.
**Scope fixed by Mike, not open here.** Terrain and composition; between-cell heterogeneity only; no Regime II, Ψ or coherence observable; onset continuity is not in Flight 9.
**Review against the committed record only.** The packet contains no Annex material.

## 1. Packet contents (at repository paths)

| Path | Why it is here |
|---|---|
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_3_REVIEW_ROUND2_2026-11-13.md` | this document |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_3.md` | **the object reviewed** |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_2.md` | the version you reviewed in round 1 |
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_2_REVIEW_2026-11-13.md` | the round-1 instruction document, as shipped |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_2_ROUND1_REVIEW_2026-11-13_RECEIVED.md` | your round-1 review, as committed |
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_2_DISCUSSION_2026-11-13.md` | L1's discussion message, recorded as drafted (§2 item 1) |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_2_DISCUSSION_RESPONSE_2026-11-13_RECEIVED.md` | your discussion response, as committed |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_3/` (six scripts, four JSON outputs) | every number new to v0.3, and the prototype evaluator |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_3.md` | the governing design text |
| `flights/mfa_fidelity/design/flight9/L2_F9_DESIGN_CONSULTATION_2026-11-12_RECEIVED.md` | your design consultation |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | the claim grammar fixed before any data |
| `flights/mfa_fidelity/design/flight9/probe/F9_PROBE_RECORD_2026-11-12.md`, `F9_PROBE_REPORT_2026-11-12.json`, `F9_PROBE_IDENTITIES.json` | what the probe showed and what L1 has seen |
| `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | terrain formulas and the spectral routine; the arith scripts take its path as their first argument |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md`, `FLIGHT_8_FREEZE_RECORD.md` | the frozen predecessor |
| `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md` | the close and its obligations forward |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md`, `PD_PARTICIPATION_RULINGS_PD1_PD7.md`, `NOTATION_SCOPE_RULING_v1_1.md` | flicker obligation; PD5, PD7; the translation table |
| `flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md` | the committed F labels |
| `theory/overview/EE_emergence_overview_v1_8_1.md` | the statement of record |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py`, `config.py` | the placed scalar step |
| `MANIFEST.txt` | SHA-256 of every file above |

The v0.2 `arith/` directory and v0.1 are not in this packet; v0.3 supersedes them. The probe's array files are not in the repository.

**First part of your reply:** a receipt table (file count, and each file's hash against the manifest). Then wait for Mike's "execute".

## 2. Disclosures

1. **L1's discussion message is recorded as drafted.** Mike relayed it in your round-1 chat. If the text you received differs from the committed file, say so.
2. **Mike's ruling and the principle it was given under.** After your discussion response Mike set a principle (contract v0.3 header) and ruled "I rule affirmative to all" on L1's recommendations. Under that principle L1 changed three of its own earlier positions: it scores against the complete contour family where it had conceded a registered subset; it blocks D when any level follows the rival; and it gives the contour-constancy report a noise reference. Your discussion response accepted the registered subset with a narrowed claim; v0.3 does not narrow the claim, so your counter on R3 is answered differently from how you left it.
3. **Three design changes were made on a site-closure estimate** (contract §1.0, Appendix A.8): the κ step is halved, r on TB is 0.3, and the panel is 40 seeds. No lattice was run and no probe output was read. No closure map was compared with a λ contour.
4. **A prototype evaluator exists** (`arith_v0_3/f9_evaluator_proto.py`). It was run on synthetic maps only, to measure cost and to check definitions against your counterexamples. It is not an instrument module.
5. **L1 has still not seen the boundary endpoint.** No occupancy map was rendered from probe output, nothing from probe output was computed against λ contours, and no edge was extracted from it. Please do not ask for any such computation.
6. **TB with r = 0.3 and all four TD variants have never been run.**
7. **Contract §11.2 lists five consequences of the ruling that Mike has not ruled on by name.** Treat them as proposed.
8. **Reproduction notes.** `f9_contract_arith_v3.py <path to f9_probe.py> <out.json>` reproduces `contract_arith_v3.json` byte for byte in L1's container. `proto_checks.py <path to f9_probe.py> <out.json>` must be run as a script from its own directory without the interpreter's isolated mode; its `sec_per_draw` and `brute_sec` fields are machine timings and will differ, and its other fields are deterministic (seeded). It takes about two minutes. The two closure scripts use the v0.2 grid and r, on purpose: they record what informed the ruling.
9. **Numbers are container values** (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1); array hashes are provisional (contract §3.4).

## 3. Questions

**Q1. Closure of the round-1 repairs.** For each of R1 to R10 and the Q1 addition, say **CLOSED**, **CLOSED WITH NOTE**, or **NOT CLOSED** (say what remains). Contract §12.1 gives the section for each.

For Q2 to Q10 please give a plain disposition: **ACCEPTABLE**, **REQUIRES CHANGE** (say what), or **REJECT** (say why and what instead).

**Q2. The pruning argument (§5.5 step 7; `f9_evaluator_proto.py::Family.admissible`).** Is it exact for the decision Δ ≤ ε as stated, including the linearly interpolated quantile, the joint statistic and the tie rule? Is the build obligation (pruned and unpruned decisions agree on the whole known-answer corpus) sufficient?

**Q3. m = 40 bonds and its strata (§5.5 step 6; §6.1 class 16; §6.2).** You accepted the structure and no number.

**Q4. The component convention (§5.5 step 3):** bonds between one 4-connected component of the region and one 8-connected component of its complement.

**Q5. Contour constancy with a noise reference (§1.3 b, §5.7).** Is the noise reference sound? Is the stated reading (variation within contours beyond noise is evidence against the uncoupled alternative; its absence is not evidence for it; bin width inflates the ratio) careful enough? Does reporting it risk a claim the instrument cannot support?

**Q6. The assumption register and the calibration stop path on informative-level counts (§1.5 A1, §7).** Does counting edges at θ in the calibration census, before canonical scoring, compromise the scored endpoint? Is each register entry a test declared before its data?

**Q7. The error table (§6.2):** decision units, certified truths, which outputs are errors, and the two sensitivity strata.

**Q8. The persistence diagnostic (§1.3 a, §5.4):** description precedence, the 36-of-40 criterion and the two-sided pointwise interval.

**Q9. Identities and the tie rule (§3.4, §3.3).** Rounding to 12 places makes the two families on a same-family terrain differ in a few plateau members (1,179 against 1,164 on TC). Roles are declared by formula. Is that adequate, and does the tie rule create any decision that depends on rounding?

**Q10. The three design changes made on a closure estimate (disclosure 3).** Do they damage the prospective standing of the claim grammar? Is the disclosure in §1.0 sufficient?

**Q11. Anything else that would prevent a freeze**, including any number in v0.3 that the `arith_v0_3` scripts do not reproduce.

## 4. What happens next

Mike rules on your return. Before freeze Mike may invoke the Gemini corpus audit. Nothing is authorized by this packet.

**Return format.** One downloadable `.md` file, receipt table first. End with one overall line, plain at column 0, in one of these forms:
`CONTRACT DISPOSITION: FREEZABLE AS A CONTRACT CANDIDATE`
`CONTRACT DISPOSITION: NOT YET FREEZABLE`

*L1, 2026-11-13. Nothing placed beyond the fifteen files of this commit; no run; nothing in `f8` or `e1` modified.*
