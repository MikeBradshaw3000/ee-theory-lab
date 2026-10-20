# L2 → L1 — E1-R M6 Onset Diagnosis Disposition

**Date:** 2026-10-20  
**Register:** Flight 8 condition-1 bounded NONCANONICAL diagnosis  
**Disposition:** **ACCEPTED FOR FAILURE LOCATION ONLY; NO REPAIR OR PRODUCTION AUTHORIZATION.**

## Custody — SHA-256 (16 hex)

| Received object | Digest prefix |
|---|---|
| `E1_CONTRACT_v0_4.md` | `fb1d82bd267b9eee` |
| Frozen `verdict.py` (received under a `.crdownload` filename) | `e4600b258072e345` |
| `E1R_M6_ONSET_DIAGNOSIS_FINDING_v1_2.md` | `a4be8c430d43861c` |
| `L1_TO_L2_RESPONSE_DIAGNOSIS_RECEIPT_2026-10-19_v2.md` | `eadb65c4df45a8b1` |

The `.crdownload` bytes are readable Python source and match the declared frozen `verdict.py` digest. V1.2 supersedes v1/v1.1; the earlier versions are preserved as history.

## Source-level check

Contract v0.4 §5 rule 4c rejects a boundary uncertain span greater than three **levels after pass 2**; §5 router R5 and R6 each insert eight interior levels in the band and prescribe evaluating the combined sequence. The frozen source implements this literally: `BOUNDARY_SPAN_LIMIT = 3`; `evaluate()` computes `span = len(inside)` and returns `NOT_DISTINGUISHED / boundary_unresolved / 4c` when exceeded; `route()` distinguishes P2R-5 (nonempty band) from P2R-6 (empty band), requests eight insertion points, calls `_resolve_collisions()`, and returns the inserted levels. There is no physical-width normalization in 4c. This confirms the diagnosis's code/contract transcription of the operative mechanism.

## Answers to L1's four questions

1. **Location — ACCEPTED at the bounded diagnostic standard.** The failure location is the interaction of M4 rule 4c's sample-count span ceiling and P2R-5/6 post-routing densification with the M6 onset archetype widths. The idealized 12,000-sweep replay reported in the packet closely tracks both committed audit ensembles; the 100-sweep realized rows agree at final-verdict and rule level. The finite residual is consistent with M2/M3/cache classification deviations. This does not prove M2/M3/cache are defect-free or establish a universal bound on their error outside the diagnosed records.
2. **Method — SUFFICIENT FOR LOCATION, not qualification.** The ideal-classifier counterfactual isolates the geometry/verdict channel, while realized runs check that replacing run classification with the ideal does not alter those sampled final verdicts. The method does not establish a repair's correctness or transfer to a fresh guard ensemble.
3. **Additional discriminating tests — NONE required to close this bounded diagnosis.** The six isolated U-label deviations are acknowledged as verdict-neutral in the observed realization, not generally proved harmless. A held-out-master end-to-end sample is not required merely for this location decision. Prospective tests belong to repair design and qualification.
4. **Repair surface — BOUNDED FOR PROPOSAL, NOT APPROVED.** The causal locus supports directing the next repair-design proposal to M4's 4c/router resolution relation and the M6 archetype-width contract. It does not authorize a particular 4c threshold, insertion count, or width alteration, nor pre-approve unchanged M2/M3 under the new Flight 8 instrument. Flight 8's independent M3/null and archetype rebuild obligations remain.

## Precision qualifications

- The finding's shorthand that every failure was LOCATED on pass 1 has the explicitly documented exception of five gentle-onset sweeps per ensemble already ND on pass 1. The causal localization includes those exceptions.
- The corrected counts are **1,912 sweeps with fallback moves** and **213 with fallback drops** (212 unresolved-heavy-boundary, one wide-mixed-boundary). The router-row and fallback details make the attribution stronger; fallback itself is not shown to drive the onset failures.
- L2 independently examined supplied source and the realized-row record, but did not execute the complete 12,000-sweep replay or independently regenerate the original canonical audit ensembles. Numerical closeness of the replay to the committed audits is a reported result assessed against supplied evidence, not an independently reproduced canonical certification.

**Governance:** E1-R Stage 1 remains closed adversely, NOT QUALIFIED, production readiness FALSE. Both old ensembles remain burned. This diagnostic finding is NONCANONICAL and not a result of record. L1 may proceed to **a separately reviewed repair-design packet**, subject to Mike's authority, followed by Flight 8's prospective guard and qualification requirements. No production is authorized.
