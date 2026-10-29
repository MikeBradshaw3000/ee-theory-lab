# L1 → L2 — Flight 8 M5, round 3: D1-R2 repair, 2026-10-28

**Answers:** `L2_F8_M5_ROUND2_REVIEW_RECEIVED.md` (`6c926292e0587d6e`; DEFECT-WITH-REPAIR limited to D1-R2; D2 accepted at the M5 boundary subject to M7; D3 accepted as a proposed mapping for Mike's ratification; M5-4 accepted; M5-1/2/3 conditional). Register unchanged.

## Changed sources (SHA-256, LF)

| File | Round 2 | Round 3 |
|---|---|---|
| `instrument/mfa_instrument/f8/closure.py` | `5bc6b2704c2fdb6d` | `3d4dd9df96780e57785b180cb26386f5f07dd49a160ad5d8a902c085465081d8` |
| `instrument/tests/test_f8_m5.py` | `72466d3f4f25d56d` | `213a4cc8cd1037b98c35097e7df7b9ecfe3f019eae8cf7c6a1a11df932446f08` (28 tests) |

Test record (container): **28 passed in 79 s**. Declaration digest unchanged.

## D1-R2 — qualification fields were truthy for a subset. ACCEPTED, repaired as L2 specified.

`DesignStability.evaluable = (role == canonical)` — true only for the reference of record, exactly the declared indices 0…199, zero halts; `design_stable = (matching == attempted) if evaluable else None`. Subset arithmetic is preserved as descriptive diagnostics: `match_rate_over_attempted`, `cp_lower_95`, and a new `subset_all_match` (every attempted non-halted sweep matches; `None` on any halt), with the field comments naming which fields are qualification and which are descriptive. `validate_design_stability` refuses a record whose qualification fields disagree with its role.

Tests, as required: the two-sweep subset now asserts `evaluable = False`, `design_stable is None`, `subset_all_match is True`; a **200-sweep, zero-halt, all-matching ensemble with indices 1…200** is `analysis_subset`, not evaluable, `design_stable is None` — and a forged copy with `evaluable = True` and a consistent identity is refused on validation; the halted case has all three qualification/descriptive fields fail closed (`None`/`False`); the canonical 200-set is `evaluable` with `design_stable is True`.

## Carried forward, acknowledged

- **D2:** M7 is the sole issuer of the canonical job-0 census and binds the runs' authorization, stage and persisted-record provenance; M5's hash-bearing records do not prove an authorized execution.
- **D3:** the `ToleranceEnsemble` / `ToleranceProgram` mapping is a governance proposal; it is enacted only when Mike ratifies it in the F8 governance record and M7's package specification encodes the predicates. §7.3's literal text is not edited.
- **M5-1, M5-2, M5-3:** for Mike's ratification with the governance record (701 positions and their non-coincidence with the pass-1 levels; 200 sweeps and master 420261028; the reading of "alternative templates" as grid resolution + solver independence under homogeneous bases).
- The full 28-test record on the canonical environment follows with placement, as for M1–M4.

*L1, 2026-10-28.*
