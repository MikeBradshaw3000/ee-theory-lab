# L2 — Flight 8 M5 Build Review, Round 3

**Date:** 2026-10-28  
**Register:** Instrument build review, frozen Contract F8 v0.8.4 (`e87277a2d11e948f`). **This review does not authorize placement or canonical execution.**  
**Verdict: SOUND** — the remaining round-2 D1-R2 source defect is repaired. This source verdict is not a claim that L2 completed the full 28-test suite in this environment, nor does it ratify outstanding governance decisions.

## Receipt and changed-source identities

Archive: `f8_m5_round3_L2.zip`, **41 regular files**. Independently computed SHA-256:

| File | SHA-256 (full) | Declared prefix |
|---|---|---|
| `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M5_ROUND3_RESPONSE_2026-10-28.md` | `c1cf3c2f8007d8fec4c4731d7441a0c6ea1087241ba44e97e21ca456cdc19ffe` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `3d4dd9df96780e57785b180cb26386f5f07dd49a160ad5d8a902c085465081d8` | MATCH |
| `flights/mfa_fidelity/instrument/tests/test_f8_m5.py` | `213a4cc8cd1037b98c35097e7df7b9ecfe3f019eae8cf7c6a1a11df932446f08` | MATCH |

I compared the two changed source files directly against the corresponding files from the round-2 archive. Changes are confined to the D1-R2 qualification/descriptive field distinction and tests of that distinction; no other changed source was alleged for this round.

## Independent execution evidence

Working directory: `flights/mfa_fidelity/instrument` in the extracted round-3 archive.

- Full `python -m pytest tests/test_f8_m5.py -q`: **timed out** after printing 24 progress dots, without a final pytest summary. It must **not** be represented as 28 passed.
- Prescribed reduced `python -m pytest tests/test_f8_m5.py -q -k 'not replay and not roles_halts'`: also **timed out** after printing 22 progress dots, without a final summary.
- Targeted regressions: `python -m pytest tests/test_f8_m5.py -q -k 'd1_canonical_role_requires_declared_master_and_exact_index_set or design_stability_roles_halts_and_cp'`: **2 passed, 26 deselected**, in 20.60 s, exit 0.

L1 reports **28 passed in 79 s** in its response. That is L1's reported canonical-environment evidence, not an independently reproduced full-suite result. A canonical-environment complete 28-pass record remains necessary under the established placement process.

## D1-R2 adjudication — REPAIR ACCEPTED

The round-2 defect was that an `analysis_subset` with two matching sweeps could report `evaluable=True` and `design_stable=True`, inviting consumption as qualification. The round-3 diff directly addresses this:

1. `design_stability()` now defines `canonical` as **exactly 200 attempted sweeps, zero halts, the reference of record, and exact indices 0–199**; `evaluable = bool(canonical)` and `design_stable = (matching == attempted) if evaluable else None`.
2. New `subset_all_match` preserves the diagnostic all-match result but is expressly **descriptive, never qualification**; it becomes `None` on a halt. Match rate and Clopper–Pearson lower bound remain descriptive.
3. `validate_design_stability()` rejects disagreement between `evaluable` and `role == 'canonical'`, rejects presence of `design_stable` for non-evaluable records, and recomputes the full record from validated input. An attacker cannot turn the two-sweep or shifted-index result into qualification merely by rehashing edited flags.
4. Negative coverage now establishes that (a) two matching sweeps stay non-evaluable; (b) 200 matching, no-halt sweeps with indices 1–200 remain a non-evaluable subset; (c) an identity-consistent forged evaluable flag is rejected; and (d) a halted subset has neither qualification nor all-match descriptive truth. The canonical exact-index positive is retained.

The two directly relevant regression functions passed independently. **The round-2 D1-R2 finding is closed.** No further M5 source repair is required for this finding.

## Carried-forward rulings and boundaries

- **D2:** Accepted at the M5 module boundary in round 2, **subject to M7** enforcing authorized job-0 issuance, stage and persisted-run authenticity. M5 hashes are not proof of an authorized execution.
- **D3:** `ToleranceEnsemble` / `ToleranceProgram` is **accepted as a proposed governance mapping**, **not ratified by L2**. Mike must ratify its record-kind, dependency, timing and completion interpretation and M7 must enforce the resulting grammar; frozen §7.3 is not silently amended.
- **M5-1:** 701 dense positions — conditionally accepted, pending recorded governance ratification/disclosure of their relation to pass-1 levels.
- **M5-2:** 200 sweeps and master 420261028 — source implementation accepted, including D1-R2; declaration remains subject to its noted governance qualification and full canonical test record.
- **M5-3:** homogeneous-base alternative-template interpretation (resolution and solver independence) — conditionally accepted pending governance record.
- **M5-4:** stationary-start projection — accepted, unchanged.
- **M5-5:** tolerance record-kind mapping — accepted **for governance consideration only**, not self-enacting.

## Final disposition

**SOUND (M5 round-3 source review).** D1-R2 is repaired and its targeted negative tests pass. There are **no outstanding M5 source defects** on the issues returned for this round. The full-suite local timeout is an **evidence limitation**, not a passing test claim. All carried-forward governance ratifications, M7 obligations and canonical-environment test/placement prerequisites remain in force. **No placement or canonical run is authorized by this review.**
