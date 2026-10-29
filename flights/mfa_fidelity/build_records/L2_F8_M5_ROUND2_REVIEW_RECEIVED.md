# L2 — Flight 8 M5 Build Review, Round 2

**Date:** 2026-10-28  
**Register:** Instrument build review, Contract F8 v0.8.4 FROZEN (`e87277a2d11e948f`); no placement or canonical run authorized.  
**Instruction source:** `L1_TO_L2_F8_M5_ROUND2_RESPONSE_2026-10-28.md` (`fe34be217d828d56`).  
**Changed sources verified:** `f8/closure.py` SHA-256 `5bc6b2704c2fdb6d451d2b4afc1f5e16b4c4ea6ae369c4b4fafc334cc64c0eba`; `tests/test_f8_m5.py` SHA-256 `72466d3f4f25d56df9571d9402a6d18ca9e74e9a9a8436304b063e715c41c19f`.

## Verdict: DEFECT-WITH-REPAIR

D1's identity/master/recomputation defect and D2's unbound-array defect have been substantially repaired. D3 now has an explicit proposed mapping and can be taken to governance for ratification. **One remaining D1 qualification-semantic defect prevents SOUND:** an incomplete two-sweep analysis subset is explicitly marked `evaluable=True` and `design_stable=True`, in contradiction with the module's own declared 200-sweep qualification ensemble and the `DesignStability.evaluable` field comment. The tests affirm rather than reject this condition (`test_design_stability_roles_halts_and_cp`). A consumer that reads those fields rather than cross-checking the `role` could mistake subset evidence for positive qualification.

## Execution evidence

Executed from `flights/mfa_fidelity/instrument`:

- `python -m pytest tests/test_f8_m5.py -q`: printed 24 progress dots but **timed out**; no 28-pass result established.
- `python -m pytest tests/test_f8_m5.py -q -k 'not replay and not roles_halts'`: **23 passed, 1 failed, 4 deselected, 30.13 s**. The sole failure was `test_f8_m5_does_not_touch_e1`, during module import of `mfa_instrument.e1.config`, because this review environment lacks `pyarrow`. This is an environmental missing dependency, not evidence of source disagreement; it does not constitute a passing full-suite record.

## D1 — Design-stability repair: PARTIAL; remaining D1-R2 defect

The new `validate_projection_sweep_structure` rejects the wrong `PROJECTION_MASTER`, wrong declaration identity, threshold mismatch, stale content hash, wrong grid, undeclared halt category and verdict/cause/rule/class inconsistency. `validate_sweep_set` verifies reference identity, duplicate indices, each sweep's structural consistency and optional independent replay. Canonical role requires the reference of record, 200 distinct exact indices 0–199 and zero halts. `validate_design_stability` checks record identity and recomputation. These address the concrete round-1 wrong-master and altered-content attack paths.

**D1-R2 — Subset described as qualified.** `design_stability` currently sets `evaluable = halted == 0 and attempted > 0` and `stable = matching == attempted` whenever evaluable. This gives a two-sweep `analysis_subset` a truthy `evaluable` and `design_stable`; the test at lines 254–257 explicitly expects this. However the dataclass states `evaluable` requires zero halts **and the attempted count to equal the declared ensemble**, and the contract's 200-sweep design-stability qualification must not silently be conflated with subset diagnostics. **Required repair:** reserve the `evaluable` and `design_stable` *qualification fields* for a complete, canonical, no-halt ensemble (e.g. `evaluable = canonical`; `design_stable = matching == attempted if canonical else None`). Preserve subset matching rates, attempted denominators and Clopper–Pearson bounds as descriptive diagnostics. Update the two-sweep positive test to assert `evaluable=False` and `design_stable is None`; add a 200-sweep wrong-index-set negative demonstrating nonqualification even with zero halts and all classes matching. If the governance grammar deliberately assigns `evaluable` the meaning 'subset arithmetically scorable', that different meaning must be explicitly distinguished from *qualification* via a separate fail-closed field and ratified before acceptance.

This distinction is not a finding that a two-sweep subset receives `role='canonical'`: it correctly receives `analysis_subset`. It is a field-level qualification ambiguity that matters to M7 consumption.

## D2 — Calibration provenance: REPAIR ACCEPTED at M5 boundary, subject to M7

`calibration_run` accepts M1 run results only after reconstructing the production-shape, calibration-panel spec and matching `spec_hash` and `stream_key`. `calibration_census` takes only `CalibrationRun` records, requires the exact 24 × 20 × 2 key set, checks duplicate and panel/object/spec discrepancies, stores run hashes and per-run density identities and computes the two SD/MDD families and ceiling stop. It issues only `derived_provisional`; issuance of canonical job-0 provenance, including the actual authorization, execution stage and persisted run authenticity, is explicitly reserved to M7. `validate_calibration_census` rederives spec hashes and arithmetic and checks content identity. This meets the conditional alternative accepted in the round-1 repair specification. **M7 must enforce** authorized job-0 issuance and run/density provenance; M5's hash-bearing records alone do not prove an actual authorized execution.

## D3 — Governance record-kind mapping: ACCEPT AS A PROPOSED MAPPING, NOT SELF-RATIFYING

The response explicitly retains separate `ToleranceEnsemble` (one per pass-1 level, with each object's 20-member calibration panel, SD/MDD, spec hashes and census reference) and `ToleranceProgram` (full-level completion, ceilings and stop path). Proposed dependency: authorized job-0 calibration census; proposed completion: all required per-level ensembles present and all 24 levels evaluated; proposed timing: job 0 before any canonical scientific census. This resolves M5's silent record-kind omission **provided Mike formally adopts the mapping** notwithstanding §7.3's literal job-4 placement. Do not treat these names as two independent scientific jobs, double count the census, or silently rewrite the frozen contract. M7's package grammar and governance record must encode the ratified interpretation and completion predicates; until then this is a governance proposal rather than enacted authority.

## M5 declarations and disposition

| Declaration | Round-2 ruling |
|---|---|
| **M5-1:** 701 dense positions | **Conditionally accepted**; count and non-coincidence with pass-1 levels must be ratified/disclosed as previously ruled. |
| **M5-2:** 200 sweeps, master 420261028 | **Conditionally accepted**; master/indices are now enforced for canonical role, but D1-R2 field-level qualification must be repaired. |
| **M5-3:** no template axis | **Conditionally accepted**; governance must record grid-resolution and solver-independence interpretation of carried §4.8 language. |
| **M5-4:** stationary start | **Accepted**, unchanged. |
| **M5-5:** tolerance record kinds | **Mapping accepted for governance consideration**, subject to Mike's formal ratification and M7 grammar enforcement. |

**Final disposition: DEFECT-WITH-REPAIR.** Submit the small D1-R2 field-semantic repair and negative tests, plus a full 28-test canonical-environment record. D2 does not require a further M5 source repair. D3 requires governance ratification, not an unapproved contract edit. No placement or canonical run is authorized by this review.
