# L1 triage — Gemini pre-freeze corpus audit of Contract F8 v0.8.1, 2026-10-22

**Return triaged:** `GEMINI_F8_AUDIT_2026-10-22_RECEIVED.md` (beside this file). **Pinned commit:** `00c576d7117ea45af7c45de4c717e6b72d518724`. **Audited object:** `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_1.md` (`7c6f2e9de00a50ba`). Every finding below was verified by L1 against the committed files at the pinned commit from a fresh clone, per commission v3 §1 and §6. Mike rules on the fix-list; L2 confirms the resulting contract identity.

## Receipt check

All 11 bundles reported received at their declared counts (24, 31, 16, 23, 23, 47, 10, 24, 36, 24, 30 — 288 files; Tier 1 and Tier 2 complete, Tier 3 withheld per commission §4). The table was returned before the audit began, on L1's two-step invocation, and matched the generator's counts. Coverage statement: all bundles read in full.

## Findings

### Finding 1 — "saddle" in v0.8.1 §4.11 — VERIFIED, ACCEPTED (mechanical defect, blocking-grade)

- **Quotation verified** at the stated path: v0.8.1 §4.11, T-S2 clause, "A saddle-node signature (m̂_low > m̂_c + Δm) fails validly, cause `hysteresis`."
- **Conflicting source verified:** `protocols/foundational/vocabulary_quarantine.md` §1: *"saddle" — appears in v1.4 of the State of the Theory only in an exclusionary clause. Using "saddle" in architectural prose suggests saddle-node dynamics that the architecture excludes. Permitted only in exclusionary contexts citing the v1.4 commitment.*
- **Assessment.** The contract's use is exclusionary in sense (a saddle-node signature is what T-S2 fails) but cites no commitment, so the permitted-context condition is not met. The quarantine grants a technical-workstream latitude for "field" and none for "saddle"; no exemption applies. Provenance: the term entered at design note v0.1 (§T-S2), apparently echoing L2's pre-freeze consultation (`build_records/L2_E1_PRE_FREEZE_CONSULTATION_RESPONSE_RECEIVED.md`, "saddle-node-like switching" context), and was carried into every contract version v0.1–v0.8.1. Under commission §4 the superseded drafts and design notes are historical and are not retro-flagged; only the freeze candidate is repaired.
- **Severity accepted as blocking-grade:** freezing v0.8.1 would freeze a quarantine violation into a currently-governing document.
- **Fix:** v0.8.2, vocabulary only — the clause names the excluded object descriptively ("a hysteretic signature — two distinct boundaries, the mark of a discontinuous transition, which the transcritical form excludes"); test, threshold, cause label and verdict unchanged. Routed to L2 for identity confirmation as a vocabulary-only successor to the v0.8.1 on which L2's freezability word was given.

### Finding 2 — "values reverted between v0.8 and v0.8.1" — REJECTED (wrong-file attribution; commission §6 defect class)

- **Claim:** v0.8 defines w_L = 228,844, w_A = 108,400, w_U = 627,232, Δ_route = 86,956 and v0.8.1 "reverts" to 228,831 / 108,394 / 627,224 / 86,958, contradicting v0.8.1's "Nothing else changes."
- **Verification (grep over every contract version at the pinned commit):** the four cited values occur **only in v0.3 and v0.4**. v0.5, v0.6, v0.7, v0.8 and v0.8.1 all carry 228,831 / 108,394 / 627,224 / 86,958 identically; the single "86,956" in v0.5 onward is the changelog line recording its correction (L2-7.3). `diff v0.8 v0.8.1` touches **no line containing any of these numbers**; the v0.8.1 scope statement is true.
- **Assessment.** The quotations are real; the attribution to `FLIGHT_8_CONTRACT_v0_8.md` is wrong — the pattern commission §6 names ("quotations have been reliably real; file attributions have not"). No defect; no action.

### Conforming-collisions section — CONFIRMED

Both governed collisions reported conforming (μ/β reminder at first use; η_floor hazard/probability row) are correctly identified and correctly assessed against `NOTATION_SCOPE_RULING_v1.md`.

## Fix-list (for Mike's commit)

1. Place `FLIGHT_8_CONTRACT_v0_8_2.md` (vocabulary-only successor; identity in the placement note) beside v0.8.1 in `contracts/flight8/`.
2. Place this triage record and the `_RECEIVED` return under `protocols/audit/`.
No other document is touched by this audit.

## Void invocations of the same day (recorded for the calibration ledger; commission v3 §2–§3)

- **Run 1.** Bundles delivered without the commission as the instruction source; Gemini returned a project summary and an offer to "proceed to the Flight 8 contract drafting" — a containment breach (commission §3) with no receipt table and a stale factual claim (W_res "derived from the theory's rounding width," withdrawn at v0.5). Not a return; nothing recorded from it.
- **Run 2.** Commission attached, 11 bundles uploaded in one message; only 2 reached the instance (`tier1_4of7`, `tier1_7of7`, as "(2)" duplicate copies) and the instance did not report the gap despite the manifest. It audited v0.6 — the newest contract in the bundles it had — and returned "AUDIT PASSED," a verdict outside its authority. Its one cited path (`flights/mfa_fidelity/rulings/ruling_l3_retirement.md`) was real. Not a return; nothing recorded from it.
- **Lessons bound:** (a) a single-message multi-file upload to Gemini silently drops attachments — deliver the corpus as one zip archive; (b) require the receipt table as a **separate first reply, before any audit**, and confirm it against the generator's counts before issuing the execute word; (c) name the audited object and version in the invocation so the instance cannot settle on an earlier version; (d) clear "(n)" duplicate downloads before upload so the receipt table is checkable by name. The invocation note used for run 3 (`GEMINI_INVOCATION_NOTE_2026-10-22_zip.txt`, commission v3 embedded verbatim from the committed blob) is the template; a commission v3.1 codifying (a)–(d) is recommended before the next standing occasion.

*L1, 2026-10-22.*
