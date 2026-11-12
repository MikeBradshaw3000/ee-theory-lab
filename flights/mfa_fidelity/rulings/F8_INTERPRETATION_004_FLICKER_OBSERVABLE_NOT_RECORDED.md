# Ruling Record — F8 Interpretation 004: the flicker run-length observable of Contract F8 v0.8.4 §1.3(b) was not recorded in stage 1

**Ruled by:** Mike, Theory Architect, 2026-11-08 ("1 and 3": record the omission in an interpretation record, and carry the observable to the successor flight; "it can wait for the next flight"), on L1's report that no placed F8 module records the observable. Confirmed for placement on 2026-11-12 with the stage-1 disposition (L2's consultation of that date, item D2, recommends placing this decision before close).
**Status:** an identified interpretation of the FROZEN contract (`FLIGHT_8_CONTRACT_v0_8_4.md`, SHA-256 `e87277a2d11e948f…`). The contract's bytes and identity are unchanged. No placed module, no canonical record and no scored criterion changes under this record. Interpretations 001 (`6bf7304f…`), 002 (`198d2991…`) and 003 (`6ebf0ad3…`) stand.
**Decision authority:** Mike. **Drafted by:** L1.
**Ratified:** by Mike, 2026-11-12 ("ratify"), as drafted.

## The sentence

§1.3 lists the secondary observables, "finite-design; never P1". Item (b) reads: "flicker run-length statistics near the measured boundary m̂_c across windows W (Mike's held probe candidate, PD rulings record) — recorded, not tested."

## The fact

No flicker run-length statistic exists in the Flight 8 stage-1 record, and none can be derived from it.

- Placed M1 (`f8/dynamics.py`, `cc663dd3c14197a8…`) persists, per run, the per-tick global density (the `rho_global` table), the tail-window means and run summaries. It never writes per-cell states. A run-length statistic is a property of individual cells' on and off spells; global densities do not determine it.
- No placed module defines the statistic: there is no declared estimator, no window set W, no output field and no record type for it. The package specification's 29 items do not include it.
- As far as the committed record shows, the omission was not noticed at the contract freeze, in any module's build review, or at governance. L1 found it on 2026-11-08, after the calibration census and before any scientific job ran.

## The interpretation (binding)

1. **The §1.3(b) observable was not recorded in stage 1. This is an omission against the contract's reporting list, accepted as such by Mike.** "Recorded, not tested" made the observable untested; it did not make it optional. The stage-1 record must not be described as having fulfilled every reporting item of the contract.
2. **The omission bears on nothing that was scored.** §1.3 makes its items secondary and "never P1". The four P1 tests, the qualifications, the package predicates and the M4 morphology report do not read the observable.
3. **No claim about flicker statistics is available from Flight 8 stage 1** — none about their presence, absence, scale, or behaviour across windows near m̂_c. No aggregate quantity in the record is to be offered as a substitute.
4. **The observable is carried to the successor flight.** Its contract must declare, before any data: the statistic's definition, the window set W, the levels at which it is taken, and what the instrument persists so that it can be computed. It enters that contract as a design obligation, not as a result owed by Flight 8.
5. **Replay is declined, not foreclosed.** Every stage-1 run is reproducible from its committed stream key and spec hash, so a noncanonical recorder could regenerate per-cell states for the runs near m̂_c. Mike has chosen not to do this now. If it is done later it is a new, separately declared noncanonical act; its output would be descriptive, would carry its own identity, and would change nothing in the stage-1 record.

## Consequences

- No change to placed M1–M7, M-P1, the governance records, the authorizations, or any canonical record.
- The stage-1 close record names this interpretation and lists §1.3(b) among the reporting items not fulfilled.
- The PD rulings record's held probe candidate (flicker run-length statistics across W near the boundary) remains held and untested.

*Drafted by L1, 2026-11-12, from Mike's ruling of 2026-11-08 and against the committed contract and source at `abb9279`.*
