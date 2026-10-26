# Flight 8 — Freeze Record (Contract F8 v0.8.4)

**Ratified by:** Mike, 2026-10-23 ("Ratified" — F_2_symmetric retained on L1's recommendation; the other twenty-five PROPOSED values as a block). **Drafted by:** L1, at Mike's word, the same day. **Effective:** on the commit that places this file, whose message names the contract FROZEN. The contract README cites this record; Flight 8's governance record (to be written with the instrument, M7 grammar) cites it by identity.

## 1. The frozen object

| Item | Identity (SHA-256) |
|---|---|
| `FLIGHT_8_CONTRACT_v0_8_4.md` — **the frozen contract** | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` |
| `appendix_a.py` (v2) — Appendix A procedure of record | `bc3e4f05f48e0840eddd5e61b8ea653411e4468900c098e801e5e13506fe0903` |
| `APPENDIX_A_OF_RECORD.md` — Appendix A values of record (its JSON block is the object) | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` |
| `NOTATION_SCOPE_RULING_v1_1.md` — notation table v1.1, **ratified by this same commit** (contract §10 item 2 discharged) | named in the freeze commit |
| `appendix_a_v1_defective.py` — the v0.8.3 script, retained as evidence of the defect L2 exposed (not a procedure of record) | `9de52a9411802d88f00f10cd5b057737bf323ab2da8b0d689a9b8392259be733` |

The §6.3 check is satisfied at freeze: M_L = 20,652 > 0, M_U = 29,348 > 0, every declared archetype width inside its range (Appendix A). The freeze is therefore not refused.

## 2. Review chain the freeze rests on

- **L2 (adversarial source review).** Contract register v0.1 → v0.8.4, 2026-10-20 to 2026-10-23: v0.4 substantive disposition (`c408ed30`), v0.6 consolidated disposition (`3bd0a33f`), v0.7 and v0.8 reviews, v0.8.1 FREEZABLE AS A CONTRACT CANDIDATE, v0.8.2 vocabulary confirmation (`b0a4e1db`), v0.8.3 review (two findings; `L2_FLIGHT8_V0_8_3_REVIEW_RECEIVED.md`), **v0.8.4 FREEZABLE AS A CONTRACT CANDIDATE** (`L2_FLIGHT8_V0_8_4_FREEZABILITY_RECEIVED.md`). L2 independently reproduced Appendix A from the script, byte for byte, and ran the defective and corrected scripts side by side.
- **Gemini (read-only corpus audit, commission v3).** Run of 2026-10-22 against the placed candidate at `00c576d`: one finding accepted (quarantined term, discharged at v0.8.2), one rejected at triage (`protocols/audit/GEMINI_F8_AUDIT_2026-10-22_RECEIVED.md`, `..._TRIAGE_2026-10-22.md`). The freeze candidate's text since then changed only by L2-reviewed numerical conformance (v0.8.3, v0.8.4); no new Gemini run was commissioned for those, by Mike's standing (the audit is invoked at Mike's word).
- **Mike's rulings of record carried into the contract:** 2026-10-15 (Flight 8 directly; three conditions), 2026-10-20 (design note §9, "all recommended"), 2026-10-21 (option (a): P1 structural, closure fidelity a reported tier), 2026-10-22 (PD5 amendment ratified at `50c6003`; "use v0.8.3"), 2026-10-23 (this ratification).

## 3. PROPOSED values ratified by name (contract §8; each is of record from this commit)

| # | Value | Ratified as |
|---|---|---|
| 1 | L, N | 50; 2,500 |
| 2 | F dispatch | **F_2_symmetric** — *with the statement that under homogeneous bases F is inert to P1 (every cell carries λ̄ and each level sets λ̄ through the bases to reach its m); this ratification does not bear on the theory's open F element, which is decided, if at all, in the heterogeneous-base successor (§3.5, §7.3 job 5)* |
| 3 | μ (deactivation rate) | 0.2 |
| 4 | g | 1, not swept |
| 5 | sweep range in m | [0.25, 2.50] |
| 6 | n₁ pass-1 levels | 24 |
| 7 | T, tail, window | 3,000 / 1,000 / 100 × 10 |
| 8 | α_T, α_P | 0.001, 0.001 (familywise) |
| 9 | Δm rule and value | max(lower, upper) + s = **0.1201** (Appendix A; **a prospective change of T-S2's operative threshold from the hand value 0.128**, acknowledged as such at L2's requirement; fixed before any data exist; L2's observation that on the 24-level grid no measured separation can fall between the two values is noted) |
| 10 | evaluability band rule | k_R·√(ŝ_X(m₋)² + ŝ_X(m₊)²)·1.2533/√20, X the sweep's own object |
| 11 | fidelity band rule | k_R·ŝ(m)·1.2533/√20 |
| 12 | MDD ceilings | max_m MDD_X ≤ 0.02, both objects; stop path (new instrument version before any canonical census) |
| 13 | f_J | 0.25 (ND branch only) |
| 14 | off_band_mixture π range | [0.45, 0.55] |
| 15 | QS survival criterion | N·ρ*_sk ≥ 50 (a declared design tolerance) |
| 16 | ρ₀ (skeleton low initialization) | 0.02 |
| 17 | k_R | 3 |
| 18 | W_res | 3 pass-1 spacings = 293,478 micro-units (declared resolution; PD5-as-amended status) |
| 19 | ε | 0.01 |
| 20 | declared-range factors | 0.9 (locatable), 1.1 (unresolvable) |
| 21 | M-P1 known-answer | m_c ∈ {0.8, 1.0, 1.25}; 100 sweeps per class; every class returns its named verdict and cause on ≥ 95/100; cross-trigger rule |
| 22 | two-crossing offsets; reentrant return | [4, 7] spacings; U[4, 6] spacings |
| 23 | cap, CP confidence, sweeps per class | 0.10; 0.95 one-sided; 500 |
| 24 | surv threshold for m̂_c | 18 of 20 |
| 25 | instrument version string | `f8_stage1_v1` |
| 26 | skeleton evaluability ŝ source | the skeleton part of the two-part calibration census |

Already RULED before this record (not re-ratified here): η₀ = −ln(0.99); homogeneous bases; m as the control coordinate; stationary null start, no burn-in; the θ_P familywise construction (with L2); PD1–PD7 with PD5 as amended 2026-10-22; option (a), P1 structural.

## 4. DERIVED values fixed by Appendix A at this freeze

s = 97,826 (two gaps 97,827); W_res = 293,478; Δm = 0.1201; Beta(15, 6) quantiles 0.467894 / 0.902458; Δ_route(B) = 21,740 / 43,480 / 65,218 / **86,958** / 108,696 / 130,436 / 152,174 / 173,914 / 195,654 for B = 1…9, maximum over B ≤ 4 at B = 4; w_L = 228,842, w_A = 108,400, w_U = 627,232; gentle ≤ 205,958, wide ≥ 689,956; M_L = 20,652, M_U = 29,348; m_infl = 1.1765; m_lat = 1.1414; off_band_mixture risk 0.0052; θ_P ≈ 0.0573 (Gaussian provisional, exact at build); the 24-level fixed-point tables ρ*_sk(m), ρ*(m; η₀) in the JSON.

## 5. What this freeze does not do

It authorizes no run. DERIVED@BUILD quantities (thresholds, caches, masters, the calibration master) are produced only by the built instrument, each committed with its identity, before any guard master is drawn (contract §7.1). Production readiness is derived mechanically from the governance record's prerequisites; `m6_audit_qualification` passage is required. E1-R stays closed adversely. The heterogeneous-base run and the third-order lattice-versus-ODE comparison stay held (§3.5, §7.3 job 5).

## 6. Lessons bound at this freeze (added to the record's running list)

- A script that overrides certified values is itself a claim to be checked: where a script and a certified value disagree, find which is wrong before replacing either (v0.8.3's false Δ_route "correction", caught by L2).
- Every claim that a change leaves "no test unchanged" is checked threshold by threshold before it is written (Δm).
- A hand total in an appendix is a hand total; Appendix A is computed by its committed script, nothing else (Δm's 0.030).
- Multi-file deliveries to Gemini go as one zip; the receipt table is a separate first reply; the audited version is named in the invocation (Gemini triage 2026-10-22, lessons (a)–(d); a commission v3.1 codifying them is recommended before the next standing occasion).

*Written by L1 2026-10-23 at Mike's word. Mike rules.*
