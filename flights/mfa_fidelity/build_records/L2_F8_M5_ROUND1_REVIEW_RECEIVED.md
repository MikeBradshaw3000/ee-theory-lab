# L2 — Flight 8 M5 Build Review, Round 1

**Date:** 2026-10-28  
**Register:** Contract F8 v0.8.4 FROZEN (`e87277a2d11e948f`); M5 source review; no placement or run authorized.  
**Packet:** `L2_F8_M5_BUILD_PACKET_2026-10-28.md` (`ccdde073a1eb9b44`).  
**Verdict: DEFECT-WITH-REPAIR.**

## Test execution

Extracted the supplied archive at repository-relative paths. Ran `python -m pytest tests/test_f8_m5.py -q` from `flights/mfa_fidelity/instrument`. The invocation printed `......................F` but did not terminate within the execution limit; **23 passed is NOT independently established**. A second invocation excluding the E1 import test printed `22 passed, 1 deselected in 32.97s`, although the tool reported a subsequent timeout. Thus 22 test assertions were reported successful; the exact full-suite expectation is not verified. Do not interpret this environmental/runtime limit as a successful 23-test run.

## Contract and mathematical review

- **§3.1 / Appendix A:** `g_map` implements `(1-rho)*(1-exp(-(eta+lambda_bar*rho)*dt)) + rho*exp(-mu*dt)` in the Appendix A expression order. `fixed_point` uses 0.5, tolerance 1e-15, and 400,000 iterations. The source's `verify_against_appendix_a` and tests enforce exact float comparison with the committed JSON; its tests reported passing. The skeleton's zero branch at m <= 1, delta-m terms, `m_infl`, and the pair leading multiplier/branch are explicitly reproduced. This is a **positive source-and-test binding**, not a separate byte dump of every computed float.
- **§4.8 dense census:** 701-point exact-fraction/round-half-even grid; canonical `reference_of_record` role restricted to the declared grid and zero halts, with replay checking. It does not contain every one of the 24 pass-1 levels, a disclosed consequence of the chosen count. `projected_label` applies M2 window geometry, M3 thresholds, M2 run-status precedence and 16/2/4 aggregation, then M4 routing. Its deterministic starting density is the stationary null value. The source does not embed a reference result. Tests report the expected NO-NULL-PHASE/rule-2 morphology. Canonical outcome remains dependent on the authorized job.
- **§3.4 / §7.3:** separate realization and skeleton calibration SDs, ddof=1, MDD = 3*SD*1.2533/sqrt(20), ceiling 0.02 for each object; adjacent-level bands use the root-sum-square of the appropriate object's SDs; fidelity band uses realization SD. An exceeded ceiling marks the stop path. The arithmetic is correct **for the supplied density arrays**, but construction currently does not establish that those arrays came from the authorized calibration execution (see D2).
- **Appendix B:** pair branch and leading-multiplier procedures are present and test-covered. Independent-source audit found no demonstrated contradiction in the arithmetic; full 23-test evidence remains outstanding.
- **E1-R design stability:** finite-N two-binomial per-tick closure sampling and 24 x 20 level/seed sweeps, M2/M3/M4 evaluation, exact one-sided Clopper–Pearson calculation, attempted-denominator reporting, and a zero-halt requirement for canonical role are implemented. However, qualification provenance is not enforced (D1).

## Defects requiring repair

**D1 — Canonical design-stability role accepts wrong projection master and unvalidated sweep content.** `design_stability()` checks 200 indices, zero halts and reference role, but never checks `s.master == PROJECTION_MASTER`, `s.declaration_sha256`, `s.threshold_identity`, or that each input's `result_sha256 == s.identity()`; it also does not replay or validate the reference. `validate_design_stability()` just recomputes the same aggregation, so it cannot reject an adulterated sweep whose own record has not been validated. A full list of sweeps created with `projection_sweep(i, master=other)` can therefore be labeled `canonical`, contrary to the declared E1-R ensemble and master identity. **Repair:** before granting canonical role, validate the reference of record; validate each sweep's identity, frozen identity, threshold identity and declared master (replay if required by the contract); reject duplicate/wrong index sets or mixed masters. Add negatives proving that a 200-sweep wrong-master ensemble and a mutated sweep cannot obtain canonical/evaluable qualification. To avoid an expensive 200-sweep negative, test a factored pure validator with minimal fixtures and separately test its integration.

**D2 — Calibration-census input provenance is not established by the M5 record.** `calibration_census()` accepts arbitrary correctly shaped [0,1] matrices, labels them with the frozen calibration-panel SHA and computes valid bands/stop flags. `validate_calibration_census()` checks only replay from those same arrays, not the level/seed derivation, skeleton-high initialization, realization stationary start or distinct job-0 master. As a result, a non-calibration input may be presented as the authoritative job-0 tolerance record without the module detecting it. **Repair:** bind the census to a separately validated job-0 source record naming authorization, master, seed/level provenance, realization/skeleton modes, and tail-density calculation; make the canonical census record's validation fail if that provenance is missing or mismatched. It is acceptable for M5 to remain a pure arithmetic reducer **only if** the future M7 validator is explicitly the sole issuer of canonical job-0 records and the M5 object is explicitly marked provisional/derived, not self-certifying. Add wrong-master, swapped-object and wrong-start negative tests.

**D3 — Declared record-kind ambiguity remains open.** Contract §7.3 explicitly names `tolerance_ensembles` and `tolerance_program` as record kinds in job 4. Reinterpreting them as the two halves of job-0 `calibration_census` without a recorded governance mapping risks silent omission of required records. **Repair:** preserve both separately named record kinds in M7's package grammar, or obtain a formally recorded interpretation/change with their completion predicates, source dependencies and timing identified. Do not count the job-0 record twice as two independent completed jobs without an authorized mapping.

## Rulings on the five declarations

| Declaration | L2 ruling | Basis / condition |
|---|---|---|
| **M5-1** — 701 dense positions | **CONDITIONALLY ACCEPT** | The count is explicitly PROPOSED in §4.8 and round-half-even placement is reproducible. Mike must ratify it; the missing pass-1 coincidences must remain disclosed. |
| **M5-2** — 200 sweeps and master 420261028 | **CONDITIONALLY ACCEPT; implementation DEFECT D1** | These are identifiable prospective declarations and can be ratified, but current canonical-role checks do not enforce the master. |
| **M5-3** — no template axis | **CONDITIONALLY ACCEPT** | Homogeneous inert bases offer no variable base-rank template; alternative grid resolution and independent solver are meaningful axes. Governance should explicitly resolve §4.8's carried E1 template language rather than silently dropping it. |
| **M5-4** — stationary-start projected label | **ACCEPT** | Consistent with §2.9/§4.9; deterministic projection needs the dedicated floating-orbit window geometry rather than count-grid recovery. No P1 inference permitted. |
| **M5-5** — tolerance record kinds | **NOT ACCEPTED AS CURRENTLY STATED (D3)** | Job-0's two calibration objects cannot silently replace the two separately named job-4 records. Specify their governance mapping and M7 predicates. |

## Disposition

**DEFECT-WITH-REPAIR.** D1 and D2 are qualification/provenance defects; D3 is a contract-to-record-grammar defect. Return targeted repairs and tests, plus a completed 23-test run on the canonical environment. No placement, canonical run, or retrospective alteration of the frozen contract is authorized by this review.
