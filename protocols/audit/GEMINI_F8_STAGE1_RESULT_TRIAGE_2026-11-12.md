# Gemini audit of the F8 stage-1 result — L1 triage of both returns (2026-11-12)

**Commission:** v3 (`83122094…`): read-only cross-document consistency audit; no verdict authority. **Triage by:** L1, against a fresh clone at `abb927995d92faa37ca654ee8f3651c48a27f2e2`. **Decision authority:** Mike.

## Return 1 — on bundle v1 (`4718d7b0…`, 48 files, L1's disposition packet included)

`GEMINI_F8_STAGE1_RESULT_RETURN_2026-11-12_RECEIVED.txt`, `739f07e0d0218b8025c88eb799cfaf7821ee77b821642d6e8283cf2c38e6c47b` (LF identity of record; as received with CRLF line ends: `6ec84207a0ace8bd154160c2ba7afc3b111302fdf1d80b94ec31934a41ecd609`).

| Item | Triage | Basis |
|---|---|---|
| Answers to the questions in L1's packet | Out of commission | The packet was in the bundle as evidence; the commission asks for consistency findings, not answers |
| Recommendation to reject P1 | Out of commission; not adopted | No verdict authority. It rests on a seed median read as 0 where the record gives 0.004849 at m = 1.423913, and on per-level means where the tests score medians |
| T-S1c does not score the increment entering m̂_c | Accurate; already L2's finding | Adopted in the close record, section 3 |

Cause on L1's side: the bundle carried a document that asks questions. Bundle v2 omits it.

## Return 2 — on bundle v2 (`76f835bc…`, 47 files, no packet)

`GEMINI_F8_STAGE1_RESULT_RETURN_2_2026-11-12_RECEIVED.txt`, `6f664a44fbdf7a07210647c1bbb65935107f438f0ce527ad06a4229990e33ae4` (LF identity of record; as received with CRLF line ends: `d47159667ed94679efc4d5324ffff6ae7e76c1802f4ea1e91154de058a7fc364`).
Completeness receipt (47 of 47 files): `GEMINI_F8_STAGE1_RESULT_RETURN_2_COMPLETENESS_2026-11-12_RECEIVED.txt`, `fbcb564c097ef5d2067addc55e7fd09f8ebb80999b34500b363ccaae8f6aa3b1` (LF identity of record; as received with CRLF line ends: `08cc49a900385458aaa91f0bb17c7572d50b0b55a12f7d49e57a23547ca96f91`).

| Item | Triage | Basis |
|---|---|---|
| "Authorization Scope Violation (`calibration_tranche`)": the tranche ran under Authorization 002, whose `authorized_jobs` does not list it | Quotation accurate; not a defect | See below |
| Header counts, conforming-collisions section, coverage statement | Absent | Commission v3 requires them; without a coverage statement the return says nothing about files it does not mention |

**The tranche's authority.** `AUTHORIZATION_002.json` (`111c5ee8…`) lists 11 `authorized_jobs`, none of them `calibration_tranche`. It also carries `tranche_authorized: true`, `tranche_levels_micro [250000, 836957, 1423913, 2010870, 2500000]` and `tranche_seeds [2601517389, 3379839832, 1589273066]`. In placed `runner.py` (`703c2029…`) the tranche is not one of the 17 `CANONICAL_JOBS`; `GOVERNANCE_JOBS = ("production", "calibration_tranche")`, the grant for it is `a.tranche_authorized`, and `run_tranche` raises unless that field is true, then runs exactly the record's levels and seeds. The committed `calibration_tranche.json` (`c156c204…`) names authorization version 2 and the same levels and seeds. The job was authorized, by the field the design provides for it.

**What the finding does show.** A reader of the authorization alone, without the runner, can take `authorized_jobs` for the whole grant. A successor flight's authorization format could say so in the record. Held with commission v3.1; no stage-1 change.

## Standing of the two returns

Neither return identifies a defect in the committed chain. Neither is a clean audit: the first was out of commission and the second reports no coverage. The close record cites them as received, not as clearance.
