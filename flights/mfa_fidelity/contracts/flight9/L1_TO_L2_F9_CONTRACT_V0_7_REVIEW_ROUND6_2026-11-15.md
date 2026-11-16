# L1 → L2 — Flight 9: contract review of Contract F9 v0.7 (round 6)

**Register.** Contract review, round 6. No instrument, master or canonical data exists for Flight 9. **Pinned to:** `ee-theory-lab` `main` at `b925537dab451f8c5630c896df2881564cfe7b67`. Every file in this packet except this document was extracted from that commit (fresh clone); this document is new and is committed with your return.
**Authority.** Mike rules. His rulings recorded in the draft stand unless he changes them on your return. Nothing is authorized by this packet.
**Scope fixed by Mike, not open here.** Terrain and composition; between-cell heterogeneity only; no Regime II, Ψ or coherence observable; onset continuity is not in Flight 9.
**Review against the committed record only.** The packet contains no Annex material.

## 1. Packet contents (at repository paths)

| Path | Why it is here |
|---|---|
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_7_REVIEW_ROUND6_2026-11-15.md` | this document |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | **the object reviewed** |
| `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_6.md` | the version you reviewed in round 5 |
| `flights/mfa_fidelity/contracts/flight9/L1_TO_L2_F9_CONTRACT_V0_6_REVIEW_ROUND5_2026-11-15.md` | the round-5 instruction document, as shipped |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_6_ROUND5_REVIEW_2026-11-15_RECEIVED.md` | your round-5 review, as committed |
| `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_5_ROUND4_REVIEW_2026-11-14_RECEIVED.md`, `L2_F9_CONTRACT_V0_4_ROUND3_REVIEW_2026-11-14_RECEIVED.md`, `L2_F9_CONTRACT_V0_3_ROUND2_REVIEW_2026-11-13_RECEIVED.md`, `L2_F9_CONTRACT_V0_2_ROUND1_REVIEW_2026-11-13_RECEIVED.md`, `L1_TO_L2_F9_CONTRACT_V0_2_DISCUSSION_2026-11-13.md`, `L2_F9_CONTRACT_V0_2_DISCUSSION_RESPONSE_2026-11-13_RECEIVED.md` | rounds 1 to 4, for the trace of §12 |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_7/` (two scripts, one JSON output) | the scalar support checks of the routing and of the error event; your round-5 Appendix R program as extracted |
| `flights/mfa_fidelity/contracts/flight9/arith_v0_6/`, `arith_v0_5/`, `arith_v0_4/`, `arith_v0_3/` | the earlier arithmetic, which v0.7 still cites |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_3.md` | the governing design text |
| `flights/mfa_fidelity/design/flight9/L2_F9_DESIGN_CONSULTATION_2026-11-12_RECEIVED.md` | your design consultation |
| `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | the claim grammar fixed before any data |
| `flights/mfa_fidelity/design/flight9/probe/F9_PROBE_RECORD_2026-11-12.md`, `F9_PROBE_REPORT_2026-11-12.json`, `F9_PROBE_IDENTITIES.json`, `f9_probe.py` | what the probe showed and what L1 has seen; terrain formulas |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md`, `FLIGHT_8_FREEZE_RECORD.md` | the frozen predecessor |
| `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md` | the close and its obligations forward |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md`, `PD_PARTICIPATION_RULINGS_PD1_PD7.md`, `NOTATION_SCOPE_RULING_v1_1.md` | flicker obligation; PD5, PD7; the translation table |
| `flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md` | the committed F labels |
| `theory/overview/EE_emergence_overview_v1_8_2.md`, `README.md`, `EE_emergence_overview_v1_8_1.md` | the statement of record, the directory's register, and the previous version |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py`, `config.py` | the placed scalar step |
| `MANIFEST.txt` | SHA-256 of every file above |

**First part of your reply:** a receipt table (file count, and each file's hash against the manifest). Then wait for Mike's "execute".

## 2. Disclosures

1. **Mike's ruling on your round-5 return (2026-11-15):** "proceed as stated". L1 agreed with both findings, ran your Appendix R program (every figure reproduced), and recommended taking both repairs as you stated them, including your concrete option for R5-1. L1 told Mike that R5-1 needs no new ruling in substance, since it applies his ruling of 2026-11-14 to the quantity that ruling is about, and that R5-2 is stricter than what L1 had written.
2. **Your Appendix R program is committed as `arith_v0_7/l2_round5_checks.py`**, extracted from the fenced block of your review. If it differs from what you wrote, say so.
3. **R5-1 as implemented (§6.2, unavailable-state cases).** For every candidate of the row-15 constant quota or of row 25, c is drawn uniformly on [0.03, 0.40]; a(c) is the declared clipped mean at m = c and σ = σ_seed(c); the constant quota accepts |a(c) − θ| ≥ 0.06 and row 25 accepts |a(c) − θ| < 0.06; a candidate outside its row's domain is discarded and counted as `outside population domain`; no candidate and no unused budget passes between the rows. Budgets are unchanged (50 within 2,500; 200 within 10,000). One point L1 added that you did not state: the contract writes σ = σ_seed(c) for these rows. The general declaration has σ_i = c_σ·σ_seed(μ⁰_i) with c_σ = 1 unless a stratum says otherwise, and neither row says otherwise, so the two agree; say if you would rather the factor were written out.
4. **R5-2 as implemented (§6.2, the paragraph after the table).** Your three conditions, with the union counted once per case. For condition 3 the contract says how the reference state is obtained: the qualification harness computes it by §7's order from the comparison family (empty or not), the sample region's cell counts and bond count as recomputed from the sample by the certifying code of §6.0, and the persisted counts of invalid, compatible and adverse resamples; the evaluator's cause field is not an input. That mechanism is L1's addition. The resample counts are taken as persisted, as you wrote; they are not regenerated independently.
5. **What L1 computed, and its limit** (`routing_checks_v7.json`; scalar arithmetic only). At σ = 0 the routing gives v0.6's split on a grid of step 1e-5. Your two witnesses are assigned by their population values. With a single σ applied at every c, for seven values from 0 to 0.35, between 50% and 68% of the proposal falls in the capped domain and the rest in the reported band, against 2% needed by each row. Those σ are illustrations and say nothing about σ_seed(·), which may vary with c. On the saturated range the population value stays at or above 0.584 for σ up to 0.35. The error event is applied to nine sample descriptions with a simplified single-index reference; it is a check of the event's logic, not of a harness.
6. **Not changed, and why.** The saturated and empty-region states keep the typed certificate alone, with no distance condition, since your finding and Mike's ruling concern the constant state. If you hold that the same condition should apply to either, say so.
7. **L1 has still not seen the boundary endpoint.** No occupancy map was rendered from probe output, nothing from probe output was computed against λ contours, and no edge was extracted from it. Please do not ask for any such computation.
8. **TB with r = 0.3 and all four TD variants have never been run.**
9. **Reproduction notes.** `routing_checks_v7.py` takes one argument, `<out.json>`, imports nothing from the other directories, and reproduces its JSON byte for byte in L1's container from a fresh clone. Its floating-point outputs may differ in the last digits on another platform.
10. **Numbers are container values** (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1); array hashes are provisional (contract §3.4).
11. **v0.7 was produced from v0.6 by replacement of the affected passages.** Changed: the title and header; §1.0 (errors list); §1.5 A7; §6.2 (the constant-map recipe, which now covers rows 15 and 25 and replaces the separate near-θ recipe; one sentence of "Assignment by certified truth"; one sentence of the candidate budget; rows 15 and 25 of the table; the row-15 paragraph after the table); §11; the round table and labels at the head of §12; Appendix A.9 and A.10; the closing line. Every other passage is byte-identical to v0.6.

## 3. Questions

**Q1. Closure.** Say **CLOSED**, **CLOSED WITH NOTE**, or **NOT CLOSED** (say what remains) for each of R5-1 and R5-2, and then for R4-1, R3-2 and F4, which you held open through them.

For Q2 and Q3 please give a plain disposition: **ACCEPTABLE**, **REQUIRES CHANGE** (say what), or **REJECT** (say why and what instead).

**Q2. Routing by population value (§6.2: the constant-map recipe; assignment; candidate budget; rows 15 and 25; §1.5 A7).** Is the rule complete for both rows: proposal, acceptance, the equality convention at 0.06, budgets, no transfer? Are the linked descriptions consistent with it?

**Q3. Row 15's error event and the reference state (§6.2, the paragraph after the table).** Is the event the one you specified? Is the reference state defined well enough to build, and is taking the resample counts as persisted acceptable?

**Q4. Anything else that would prevent a freeze.**

## 4. What happens next

Mike rules on your return. Before freeze Mike may invoke the Gemini corpus audit. Nothing is authorized by this packet.

**Return format.** One downloadable `.md` file, receipt table first. End with one overall line, plain at column 0, in one of these forms:
`CONTRACT DISPOSITION: FREEZABLE AS A CONTRACT CANDIDATE`
`CONTRACT DISPOSITION: NOT YET FREEZABLE`

*L1, 2026-11-15. Nothing placed beyond the six files of this commit; no run; nothing in `f8` or `e1` modified.*
