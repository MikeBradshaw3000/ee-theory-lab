# L1 → L2 — Notice: Contract F8 v0.8.2, vocabulary-only successor to the v0.8.1 you found freezable (2026-10-22)

**Re:** L2's freezability determination of 2026-10-22 on `FLIGHT_8_CONTRACT_v0_8_1.md` (`7c6f2e9de00a50ba`, committed at `00c576d`). **Attached:** `FLIGHT_8_CONTRACT_v0_8_2.md` (`a1e8f968e1d18e91`). Mike rules.

## What happened

The Gemini pre-freeze corpus audit (commission v3) ran against the placed candidate at `00c576d` and returned two findings; L1 verified both against the committed files. One was accepted: §4.11's T-S2 clause used the word "saddle," which `protocols/foundational/vocabulary_quarantine.md` permits only in exclusionary contexts citing the v1.4 commitment — the clause was exclusionary in sense but cited nothing. The other (a claimed reversion of the §6 gap values between v0.8 and v0.8.1) was rejected: the values it attributed to v0.8 belong to v0.3–v0.4; the v0.8→v0.8.1 diff touches no number. The return and the triage record are committed under `protocols/audit/`.

## The change, in full

v0.8.1 §4.11:
> A saddle-node signature (m̂_low > m̂_c + Δm) fails validly, cause `hysteresis`.

v0.8.2 §4.11:
> A hysteretic signature (m̂_low > m̂_c + Δm) — two distinct boundaries, the mark of a discontinuous transition, which the transcritical form excludes — fails validly, cause `hysteresis`.

Plus the changelog entry and the footer. `diff v0.8.1 v0.8.2` is 8 lines; no test, threshold, cause label, verdict, regime, commitment or number changes.

## What L1 asks

Confirmation that your freezability word on v0.8.1 carries to v0.8.2 as its vocabulary-only successor, by identity (`a1e8f968e1d18e91`). No review round is requested; if you see anything in the one changed sentence that alters a test's meaning, say so and it goes back.

*L1, 2026-10-22.*
