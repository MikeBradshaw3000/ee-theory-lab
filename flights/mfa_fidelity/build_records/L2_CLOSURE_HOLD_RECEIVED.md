# L2 Phase-1 Closure Hold — One E1 Coordinate-Identity Repair

## Closed-register verdict

Items 1–3 and 5–8 of the bounded hardening packet are **REPAIRED AS REQUIRED**. The closure battery is otherwise satisfactory. One defect remains in the E1 identity verifier.

**PHASE 1 CLOSURE IS HELD ON THIS ITEM ONLY.**

## Defect — flattened-key range validation permits coordinate aliasing

The E1 verifier formed the flattened cell key before independently validating both coordinate components. A row with an invalid coordinate pair can nevertheless produce a flattened integer inside the legal key range.

Discriminating example on a 6×6 grid:

```text
Agent_X = -1
Agent_Y = 6
flattened key = (-1 * 6) + 6 = 0
```

That invalid row aliases the legitimate cell `(0, 0)`. A check that accepts `0 <= key < 36` therefore does not establish that either coordinate was legal. The row can enter the seen ledger, tick-0 baseline map, or identity comparison under another cell's identity.

This is a real closure defect because exact `(Tick, Agent_X, Agent_Y)` ownership is the point of the E1 file-global ledger.

## Required repair

1. Compute an independent row mask:

```text
0 <= Agent_X < grid_scale
0 <= Agent_Y < grid_scale
```

2. Accumulate and report a `coordinate_range` failure count.
3. Define the valid ledger/indexing mask as `in_range_tick AND xy_ok`.
4. Gate every seen-ledger operation, tick-0 baseline insertion, and flattened-key index behind that mask.
5. Invalid coordinates must fail the report but must never index, alias a legal key, or raise an indexing exception.
6. Apply the same discipline wherever E1 identity makes cell-indexed operations.

## Required discriminating negatives

- Plant `(-1, 6)` on a 6×6 grid so the old flattened-key-only check would alias legal key 0.
- Plant at least one gross out-of-range coordinate to prove fail-closed behavior without exception.
- Assert `coordinate_range` fails and the report does not pass.

## Scope fence

No other source is reopened. No opportunistic hardening is requested. The global seen ledger and the other closure repairs stand.

## Disposition

**CLOSURE HOLD — RETURN THE TWO-FILE LOCAL REPAIR (`verify.py`, `tests/test_verify.py`) AND NOTHING ELSE.**
