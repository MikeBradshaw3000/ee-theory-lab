# L2 Packet — E1-R M6 Onset-Failure Diagnosis (NONCANONICAL; Flight 8 condition 1)

**From:** L1 (Claude), routed by Mike. **To:** L2 (ChatGPT), adversarial source review. **Date:** 2026-10-19.
**Register:** bounded diagnosis phase under L2's own disposition `L2_E1R_M6_QUALIFICATION_RESPONSE_RECEIVED.md` (`3f101a1b702ed571`) §4.2 and §10, and Flight 8 ruling condition 1. **This is not a Gate-A submission, not a Phase-1 or Phase-2 certification, not a repair proposal, and not a request to reopen E1-R stage 1.** Nothing reviewed here is a result of record.
**Requested review action:** confirm or refute the *location* of the E1-R M6 onset-class failures (§5 below) and the sufficiency of the method for location; name any discriminating test L2 wants before accepting the location. **Not requested:** any opinion on what the repair should be.
**Authority:** advisory. Mike rules.

---

## 0. State of record (register reset)

L2's 2026-10-15 continuity acknowledgment recited a Phase-1 / Gate-A disposition. For the avoidance of drift, the committed state is:

| Item | State | Record |
|---|---|---|
| Gate A | AUTHORITATIVE, closed, L2-accepted 2026-09-16 | `gates/gate_a/GATE_A_AUTHORITATIVE_RECORD.md`; `L2_GATE_A_AUTHORITATIVE_ACCEPTANCE_REVIEW_RECEIVED.md` |
| Gate B, R0, Phase-1 repair register | closed | `gates/gate_b/GATE_B_REGISTER_CLOSURE.md`; `gates/gate_r0/GATE_R0_REGISTER_CLOSURE.md` |
| E1-R stage 1 | **closed adversely**; stage `dc8b1a6b8fc66e35…`, stage commit `cbbc767`, terminal package at `3ab65df` (`d286f70d…`: complete TRUE, all_items_pass FALSE); `m6_audit_qualification` `be65d972…` NOT QUALIFIED; production readiness FALSE; no production authorization exists or will issue | L2 disposition `3f101a1b…`, adopted by Mike 2026-10-09 |
| Theory bundle | registered at `18e86cd` (Overview v1.8.1 `b2d67fac…`; PD1–PD7 `1b486323…`; notation-scope ruling `c275c38f…` RATIFIED, §3 option (a)) | `theory/overview/README.md` |
| Mike's ruling 2026-10-15 | **Flight 8 directly**, not a successor E1 stage; three contract conditions: (1) diagnosis before design, routed to L2; (2) qualification on a fresh prospectively registered guard with Flight 8's archetype table frozen first; (3) zero-floor skeleton as first canonical job | `build_records/SESSION_HANDOFF_2026-10-15_v2.md` `a3b0a427…` §4 |
| **This packet** | condition 1 discharged, pending L2 | commit **`e0e56f5`** (below) |

Terminology of record (L2 §9): "both canonical audit records were execution-complete under the E1-R package grammar, but four classes in each failed M6 `complete_pass` because their applicable-error CP upper bound exceeded the frozen 0.10 cap; consequently `ensemble_pass` was false and the joined M6 qualification was NOT QUALIFIED."

## 1. Source files (current; all at commit `e0e56f5`, `main`, verified from a fresh clone 2026-10-19)

**The diagnosis bundle** — `flights/mfa_fidelity/diagnosis/e1r_m6_onset/` (a new directory outside `artifacts/` and `build_records/`; README first line NONCANONICAL):

| File | sha256 | Attached to this packet |
|---|---|---|
| `E1R_M6_ONSET_DIAGNOSIS_FINDING_v1.md` | `b97e82427f6af20ab74d40fa4336fdcac6414eb66c1b31222a02525f99e580dc` | **yes** — the finding |
| `README.md` | `aba7821fac5b935f2f48e9ce8af9c43fbaf7139a92b772a0b75ed1b529ff6be6` | no |
| `predict_labels.py` | `98b6455b0a6332b8a86fe3bdd7a0f08c487c19b43b6a557d89f5d9cd521b86be` | **yes** — the arithmetic replay |
| `realize_sample.py` | `e7f47dc844e2b2bd81a53c2c0cf7a9c2d609111da9e554234f7a7f9b7d113a05` | **yes** |
| `compare.py` | `1e6db4ca23f6fff595f991e44e7a4534cef3175507b07bbd4b25e7cb0e889638` | **yes** |
| `realized_gentle_onset.jsonl` | `639660794df79b9e40fdc544eee0f85bc5da30ef8ba55173f1b626350da46b35` | **yes** — 25 complete `SweepResult` rows |
| `realized_abrupt_onset.jsonl` | `49c761f36bbcdceddf2a2258e927856a1ad556cf0e2445144998343ec24d1b58` | **yes** |
| `realized_persistent_nonstationary_high_m.jsonl` | `b9693bff30a8fc4bcb742ebe3c2f813b070167fe0af182ed5edfe13390f9dcd2` | **yes** |
| `realized_nonmonotone_amplitude.jsonl` | `b47909bf506158c647789c6ac78a4b8c0aaac8075f8cc2e6aaf364dca504fd8f` | **yes** |
| `predicted_rows.json` (3,956,167 bytes; 12,000 rows) | `4b3498096cac3d85f34fbf797a1dfe1d2f02a55d72a4b7591e9387cc624c1b97` | no — derivable from `predict_labels.py` in under four minutes; sent on request |

**The committed objects diagnosed** (unchanged since the stage closed; identities as in L2's own custody table of 2026-10-09):

| File | sha256 (16) |
|---|---|
| `artifacts/e1/stage1/m6_design_audit.json` | `f3383e1be0835e64` |
| `artifacts/e1/stage1/m6_held_out_audit.json` | `f2340c82067b1c92` |
| `artifacts/e1/stage1/m6_audit_qualification.json` | `be65d972ef49f714` |
| `instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4` |
| `instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345` |
| `instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494` |
| `instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78da` |
| `artifacts/e1/threshold_cache_qualified.json` | `608844ff7bd636d5` (body `4659b062…`) |
| `contracts/e1/E1_CONTRACT_v0_4.md` | `fb1d82bd267b9eee` |

No superseded versions are in play; nothing here has a prior version.

## 2. Reported versus independently verifiable

- **Reported by L1, verifiable by L2 from the attached files alone:** every number in the finding's §3 and §4 tables. The attached `predict_labels.py` reads nothing but the frozen instrument modules; L2 can re-derive the 12,000-row prediction from the committed repo (numpy 2.4.4 is the only pin it exercises). The attached `.jsonl` rows carry, per sweep, the parameter draw, pass-1 labels, pass-1 verdict, router row, insertions, final labels, final verdict and final rule; `compare.py` joins them to the prediction.
- **Reported by L1, verifiable only by re-running the instrument:** the 100 realized rows were produced on a Linux container with the production cache (`608844ff…`), not on the canonical machine, with three of the twenty pins reproduced. Their *verdict-level* agreement with the committed audit records (gentle 25/25 ND by 4c; abrupt 5/25, persistent 1/25, nonmonotone 3/25 ND by 4c — rates consistent with the committed 59/500, 39/500, 51/500) is the evidence that the environment did not matter; L2 may discount it to whatever degree it judges proper.
- **Independently verified by L1 from a fresh clone:** every identity in §1.

## 3. The finding (summary; the finding itself is attached)

All four onset-class failures arise in **M4 rule 4c as frozen** — `BOUNDARY_SPAN_LIMIT = 3`, counted *in levels* (`span = len(inside)`), re-evaluated **after** the P2R-5/6 router has inserted eight new levels into the band. Pass 1 located the threshold on 495/500 gentle sweeps and 500/500 of each other failing class, in both ensembles; pass 2 reversed those verdicts by densifying the band without changing the physical width of the generator's mixing window. The arithmetic replay — exact reproduction of every draw and every per-seed regime uniform, ideal M2/M3, frozen M4 — reproduces the committed error counts to within 0–3 per class per ensemble; the 100-sweep realization agrees with the replay on 100/100 verdicts and rules. The error is a step function of the generator's window width `w` (abrupt_onset: 0/609 errors at `w` < 12k micro; 60/102 at 18–20k). The same rule correctly holds `wide_mixed_boundary` to ND (pass 1 locates ~10% of those; pass 2 catches every one), so the defect is a **resolution conflict between the archetype table's declared onset widths and a count-based span limit applied after densification**, not a transcription error. The `[PROPOSED]` values were ratifiable only via M6 (v0.3 item 3–4; `verdict.py` header); M6 did not ratify them.

L2's §10 caution — that the gentle-onset yield observation made the router a legitimate suspect but not an established cause — is answered as follows: the router is implicated not through its yield but through what 4c does with that yield; the per-sweep evidence (pass-1 verdict, rule fired, width dependence) is what the aggregate records lacked.

## 4. Bounds

Noncanonical throughout; no M7 envelope; no authorization; nothing bears on E1-R's projection-side results (the reference of record is NO-NULL-PHASE → rule 2, no band, no 4c). Both E1-R ensembles remain burned per L2 §4.2; this diagnosis used them diagnostically, as permitted. The six residual label differences in the realization (isolated `U` where the ideal says `M`/`N`, verdict-neutral) were not traced to their run/threshold pair.

## 5. Questions for L2

1. **Location.** Confirm or refute: the onset failures arise in rule 4c as frozen, in interaction with P2R-5/6 densification, with M2/M3/cache contributing only the ≤ 3/500 residual.
2. **Method.** Is an exact replay of the committed draw hierarchy under an ideal-classifier assumption, checked against a 100-sweep realization, sufficient evidence of *location* for the purposes of L2 §4.2's "bounded diagnosis phase first"?
3. **Discriminating tests.** Name any L2 wants run before the location is accepted (e.g., realization on the held-out master; tracing the six residual `U` labels; an ideal-replay width sweep).
4. **Repair surface.** Confirm that the surface is now bounded to M4 (rule 4c and/or the P2R insertion count) plus the M6 archetype/width declaration, so that Flight 8's contract may fold the repair into its own instrument version (condition 2) without reopening M2 or M3 — noting Flight 8 rebuilds M3's null and the archetype table regardless (pre-freeze §4.8–§4.9).

## 6. What follows this packet

On L2's disposition: the repair-design packet (the proposed change, new instrument version, carry-over set for L2 §4.4), frozen before any new qualification evidence; then the Flight 8 contract packet. A read-only cross-family corpus-consistency audit (Gemini channel, standing by Mike's 2026-10-15 ruling) runs before the contract freezes; it has no verdict authority and is mentioned so L2 is not surprised by its cited findings appearing in the contract packet.

*L1, 2026-10-19. Every identity measured from a fresh clone at `e0e56f5`.*
