# Gemini return — pre-freeze corpus audit of Contract F8 v0.8.1 (commission v3), 2026-10-22

**Provenance.** Run 3 of 2026-10-22. Invoked by Mike in a fresh Gemini chat with the invocation note (commission v3 embedded verbatim) and the 11 corpus bundles pinned to `00c576d7117ea45af7c45de4c717e6b72d518724` delivered as one zip archive. The receipt table was returned first and checked by L1 against the declared counts before the audit was executed. Received by L1 as pasted text through Mike; transcribed below verbatim. The triage record is beside this file. Runs 1 and 2 of the same day are void invocations and are recorded in the triage record, not here.

---

Repository: github.com/MikeBradshaw3000/ee-theory-lab
Branch: main
Audited Commit Hash: 00c576d7117ea45af7c45de4c717e6b72d518724
Date: 2026-10-22

Bundle Delivery Status

| Bundle Name | Declared Count | Received Count |
|---|---|---|
| gemini_00c576d_tier1_1of7.txt | 24 | 24 |
| gemini_00c576d_tier1_2of7.txt | 31 | 31 |
| gemini_00c576d_tier1_3of7.txt | 16 | 16 |
| gemini_00c576d_tier1_4of7.txt | 23 | 23 |
| gemini_00c576d_tier1_5of7.txt | 23 | 23 |
| gemini_00c576d_tier1_6of7.txt | 47 | 47 |
| gemini_00c576d_tier1_7of7.txt | 10 | 10 |
| gemini_00c576d_tier2_1of4.txt | 24 | 24 |
| gemini_00c576d_tier2_2of4.txt | 36 | 36 |
| gemini_00c576d_tier2_3of4.txt | 24 | 24 |
| gemini_00c576d_tier2_4of4.txt | 30 | 30 |

* Vocabulary quarantine violation.
* File: flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_1.md
* Quotation: > A saddle-node signature (m̂_low > m̂_c + Δm) fails validly, cause hysteresis.
* Conflicting source: protocols/foundational/vocabulary_quarantine.md Section 1 prohibits the term "saddle" unless explicitly citing the v1.4 commitment, stating: > Permitted only in exclusionary contexts citing the v1.4 commitment.
* Classification: mechanical defect
* Severity: blocking-grade

* Cross-document fact contradiction regarding revision scope.
* Files: flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_1.md, flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8.md, flights/mfa_fidelity/contracts/flight8/L1_TO_L2_RESPONSE_CONTRACT_REVIEW_8_2026-10-22.md
* Quotation: > Nothing else changes.
* Conflicting source: FLIGHT_8_CONTRACT_v0_8.md defines w_L = 228,844, w_A = 108,400, w_U = 627,232, and Δ_route = 86,956 in Sections 6.2, 8, and Appendix A. In FLIGHT_8_CONTRACT_v0_8_1.md, these values revert to w_L = 228,831, w_A = 108,394, w_U = 627,224, and Δ_route = 86,958 respectively, contradicting the changelog assertion that the diff was exclusively limited to one clause in §4.11, the changelog entry, and the footer.
* Classification: mechanical defect
* Severity: blocking-grade

Conforming-collisions section

The contract candidate FLIGHT_8_CONTRACT_v0_8_1.md conforms to flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1.md on the following governed collisions:

* The deliberate reuse of μ and β. The contract includes the exact mandated reminder at first use: > μ here is the deactivation rate — the Overview's lapse rate β; not the Overview's coherence coefficient μ(ρ).
* The isolated use of η_floor as a per-tick hazard is defined directly against its formal translated relationship to the spontaneous term: > identity of meaning, name shared, units differ: η_floor,C = −ln(1 − η_floor,S)

Coverage statement

* Read in full: All 11 delivered Tier 1 and Tier 2 bundles, encompassing the theory/, protocols/, flights/, operations_log/, and claude_session_handoffs/ directories.
* Sampled: None.
* Not read: None.
