# L1 Triage of the Gemini Pre-Freeze Audit of Contract F8 v0.1

**Status.** L1 primary-source verification of Gemini's return of 2026-10-20 (commission v3, pinned commit `3029f3c`, six Tier-1 bundles, 133 files; completeness check passed on all six parts — the first run under the ≤400 KB rule and the first with no ingestion loss). Every quotation checked against the clone at `3029f3c`. Dispositions are proposals; Mike rules.

## Findings

**F1 — `h` for the spontaneous-action floor collides with the C-domain reservations. ACCEPTED; fixed in v0.2.**
Both quotations verified verbatim in the draft. Amendment §9 (`04058b21…`) reserves `η_floor` for the deterministic spontaneous-action floor and `h(t)` for an external deterministic field; the notation-scope table (`c275c38f…`) carries both rows for domain C. The draft took `h` from L2's pre-freeze sketch (§4.1, where the symbols were declared illustrative) and so contradicted a ratified ruling in the very domain the contract writes in. Severity: Gemini's blocking-grade is calibrated correctly under commission §6 — a draft about to be frozen is a currently-governing document for that purpose. **Fix (v0.2):** the floor is `η_floor` throughout, as a per-tick hazard; the committed realization value is `η₀ = −ln(1 − 0.01)`; the skeleton is `η_floor = 0`; §9 adds a row making the C/S relation explicit (same name, hazard in C, probability in S, η_floor,C = −ln(1 − η_floor,S)); `h(t)` is noted as not appearing in this flight.

**F2 — three `[DERIVED@BUILD]` markers without a procedure. ACCEPTED; fixed in v0.2.**
All three quotations verified. The "conflicting source" quotation ("every DERIVED@BUILD item must have a stated procedure from [RULED]/[PROPOSED] inputs") is from L1's routing message (d), not from the contract's text — a minor misattribution of the kind the channel is known for; the contract's Markers line says the same thing in its own words, so the finding stands on the contract alone. **Fix (v0.2):** `w_A` = the largest width with E_max(w_A) ≤ one pass-1 spacing (PROPOSED rule, value derived by §6.1); two-crossing offsets at onset + [4, 7] pass-1 spacings and the reentrant return at onset + U[4, 6] spacings, both re-marked PROPOSED with values (E1's analogues were 110–220k and 120–200k on a 30.4k spacing).

**Score: 2 of 2 accepted; both blocking-grade survive triage as pre-freeze defects; both discharged in v0.2 (`88bd567c09c33841`).**

## Channel notes
- Completeness check executed and reported per part, all six matching — the §2 repair works. The routing instruction to count only true delimiters (column 1, 40-hex blob) was needed: several delivered documents quote the delimiter format in their text.
- Zero invented text; one wrong source attribution (F2's quotation source). Pattern unchanged: strings reliable, addresses re-verified at L1.
- The conforming-collisions section correctly recognized the μ/β reminder and did not flag the governed collision.
- Gemini returned text in chat, not a file; recorded here as `_CONVERSATION_RECOVERED` per the provenance tiering. Future routing messages should ask for the report as a downloadable file so the return can carry a `_RECEIVED` identity.

## Not found by this run (for Mike's awareness, not Gemini's fault)
Nothing else surfaced; the four draft-specific checks (cross-references, §9 rows, vocabulary, marker tracing) returned no further findings. L2's contract review is the next layer.

*L1, 2026-10-20.*
