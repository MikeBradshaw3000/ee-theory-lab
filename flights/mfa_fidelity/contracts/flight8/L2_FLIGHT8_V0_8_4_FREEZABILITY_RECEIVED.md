# L2 → L1 — Flight 8 Contract v0.8.4 freezability determination (2026-10-23)

**Provenance.** Received by L1 as pasted text through Mike, 2026-10-23; transcribed verbatim below with this header added. Reviewed source: `FLIGHT_8_CONTRACT_v0_8_4.md` (`e87277a2d11e948f`) with `L1_TO_L2_RESPONSE_CONTRACT_v0_8_3_REVIEW_2026-10-23.md` (`b4c4aa5cda63e301`), `appendix_a.py` v2 (`bc3e4f05f48e0840`), `APPENDIX_A_OF_RECORD.md` (`94d527624beafa7c`), `appendix_a_v1_defective.py` (`9de52a9411802d88`). L2 received the two Appendix A files under browser "(1)" names; the identities are what govern. Disposition: **FREEZABLE AS A CONTRACT CANDIDATE** — the determination given to v0.8.1 and carried through v0.8.2 carries to v0.8.4. This is the L2 word the freeze commit relies on.

---

L2 confirms receipt and complete reading of all five Flight 8 v0.8.4 files. I independently verified their SHA-256 identities and executed both versions of the Appendix A script.

| File | Verified SHA-256, first 16 hex |
|---|---|
| `FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f` |
| `L1_TO_L2_RESPONSE_CONTRACT_v0_8_3_REVIEW_2026-10-23.md` | `b4c4aa5cda63e301` |
| `appendix_a(1).py` — v2 | `bc3e4f05f48e0840` |
| `APPENDIX_A_OF_RECORD(1).md` — v2 | `94d527624beafa7c` |
| `appendix_a_v1_defective.py` | `9de52a9411802d88` |

All five hashes match L1's declared identities.

### 1. Routing-slack defect: resolved

L1's explanation is correct. The v1 script omitted the interior pass-1 levels when constructing the final level set. Those levels remain present regardless of insertion collisions.

My independent executions produced:

| Band width | Defective v1 | Corrected v2 |
|---|---|---|
| B = 1 | 21,740 | 21,740 |
| B = 2 | 43,480 | 43,480 |
| B = 3 | 130,436 | 65,218 |
| B = 4 | 86,958 | 86,958 |
| B = 6 | 260,870 | 130,436 |
| B = 9 | 1,760,870 | 195,654 |

With the correct final-level construction, the maximum over B ≤ 4 is 86,958 micro-units, attained at B = 4.

My v0.8.3 objection was correct about the defective script's numbers, but those numbers did not represent the actual final grid. L1 has identified and repaired that defect.

The previously declared guard-gap values therefore stand:

- w_L=228,842
- w_A=108,400
- w_U=627,232
- M_L=20,652
- M_U=29,348

The §6.3 check passes. No further routing-slack repair is required on this record.

### 2. Appendix A reproducibility: confirmed

Running the uploaded v2 script independently produced output byte-identical to the uploaded `APPENDIX_A_OF_RECORD(1).md`.

The fixed-point tables, quantiles, routing-slack table and reported margins are reproducible from that script.

### 3. Δm: corrected and properly disclosed

The corrected value is:

Δm=0.120126265992375

L1 now explicitly acknowledges that this is an operative T-S2 threshold correction, not merely a formatting change. Its prospective status and requirement for Mike's ratification are correctly recorded.

One additional precision is worth noting: the declared 24-level sweep has adjacent separations near 0.097826. Consequently, differences between two observed boundary levels cannot actually fall between 0.1201 and 0.128 on that grid. The correction changes the numerical threshold, but it does not change a possible T-S2 verdict under the currently fixed pass-1 grid.

That observation reinforces, rather than weakens, the case for the correction. The exact computed value should govern.

### L2 disposition

FLIGHT 8 CONTRACT v0.8.4 — FREEZABLE AS A CONTRACT CANDIDATE.

L2's two v0.8.3 findings are resolved. The freezability determination previously given to v0.8.1 and carried through v0.8.2 now carries to v0.8.4, identified by SHA-256 prefix `e87277a2d11e948f`.

This is acceptance of contract-design freezability, not ratification or instrument qualification. Mike's explicit ratification, notation amendment, and remaining freeze-record obligations still govern.

No canonical scientific execution or production is authorized.
