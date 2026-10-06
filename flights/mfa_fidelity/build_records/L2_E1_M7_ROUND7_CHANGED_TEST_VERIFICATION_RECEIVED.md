# L2 Changed-Test Verification — E1 Stage-1 Module M7, Round 7

**From:** L2 (ChatGPT)  
**To:** L1, routed by Mike  
**Register:** Phase-2 incremental source-level review, bounded post-clearance test-only reopening  
**Reviewed packet:** `L2_E1_M7_ROUND7_PACKET.md`  
**Packet SHA-256:** `b7d8bccc08e8a2e5f0b450609ef77ea27c100c85d8cfd4ec1ab1895a23837e12`  
**Comparison base:** cleared Round-6 `tests/test_e1_m7.py`  
**Scope:** test-order dependency only; `runner.py` is not reopened  
**Overall disposition:** **SOUND — ROUND 7 IS CLEARED. THE REVISED M7 TEST FILE MAY PLACE WITH THE UNCHANGED ROUND-6 RUNNER FOR THE RENEWED CANONICAL WINDOWS SUITE.**

The Round-7 packet is exactly the narrow test-only repair represented by L1.

- The packet identity reproduces.
- The cumulative Round-7 test identity reproduces.
- The standing Round-6 runner identity remains unchanged and is not returned.
- The actual Round-6 → Round-7 test diff contains exactly **nine changed source lines: five additions and four deletions**.
- The sequence of those nine changed lines is identical to the changed-lines diff carried in the packet.
- Every call to a helper that must run below production shape now uses the dedicated `SMOKE = (8, 60)` shape.
- Every remaining `SMALL = (10, 60)` use is intentional: rehearsal, conformance, or the chain fixture’s stand-in production path.
- No M7 scientific, governance, authorization, prerequisite, package, production, tranche, benchmark, router, or tolerance-program assertion changed.

The test-order defect is closed in source. The complete Windows suite remains the required placement proof.

---

# 1. Independent custody

## 1.1 Round-7 packet

L2 independently hashed the uploaded packet bytes:

`b7d8bccc08e8a2e5f0b450609ef77ea27c100c85d8cfd4ec1ab1895a23837e12`

This equals L1’s declared packet identity.

## 1.2 Round-7 cumulative test source

L2 extracted the sole `python` fenced block, restored the source-final LF, compiled it, and independently obtained:

- `tests/test_e1_m7.py`  
  `252ef6b7d444a83c1cb085c4a91f7f9ba03b1f8ec16d29555afc4229f53b502a`

This equals L1’s declared identity.

## 1.3 Cleared Round-6 comparison source

L2 extracted the cumulative Round-6 test block from the actual Round-6 packet and independently reproduced:

- cleared Round-6 `tests/test_e1_m7.py`  
  `23bd6e69a0ab37d0316e8e8407dc9c9e5211ef7849054959221b272c35030785`

The standing runner identity independently reproduced from that packet remains:

- `mfa_instrument/e1/runner.py`  
  `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769`

The Round-7 comparison therefore uses the actual cleared Round-6 bytes, not a reconstruction from prose.

---

# 2. Exact diff verification

L2 computed a fresh zero-context unified diff between the cleared Round-6 test source and the Round-7 test source.

Result:

```text
5 added lines
4 deleted lines
9 changed source lines total
```

L2 separately extracted the packet’s carried `diff` block and compared its changed lines, in order, with the independently computed diff.

Result:

```text
carried changed lines: 9
actual changed lines:  9
sequence equality:     exact
```

There is no unreported test change.

## 2.1 The nine lines are confined to the represented repair

They are:

1. addition of:
   ```python
   SMOKE = dict(grid=8, ticks=60)
   ```
2. replacement of the earlier literal `grid=8, ticks=60` tranche call with `**SMOKE`;
3. replacement of `**SMALL` with `**SMOKE` in `test_benchmark_file_facts_rederived`;
4. replacement of `**SMALL` with `**SMOKE` in `test_tranche_quarantine_fail_closed_and_failed_is_ineligible`;
5. replacement of `**SMALL` with `**SMOKE` in `test_r5_benchmark_manifest_exact`.

No assertion or expected result changed.

---

# 3. Cause adjudication

## DISPOSITION: **THE PACKET’S DIAGNOSIS IS CORRECT**

The test module defines:

```text
SMALL = (10, 60)
```

The module-scoped `chain` fixture monkeypatches:

```text
R.E1_GRID  = 10
R.E1_TICKS = 60
```

and remains active from its first use until module teardown.

The below-production helpers correctly refuse when their requested shape equals the current `R.E1_GRID, R.E1_TICKS` production shape:

- `_tranche_for_tests(...)`
- `run_benchmark_smoke(...)`

In the whole-module Windows run, the affected tests executed after the chain fixture had installed the stand-in production shape. Their previous `**SMALL` arguments therefore asked a below-production helper to run at production shape. Refusal was correct.

The earlier grouped container runs separated the affected tests from the module-scoped fixture and therefore concealed the ordering dependency.

This is a test defect. No runner guard should be weakened.

---

# 4. `SMOKE` distinctness

## DISPOSITION: **INTEGRATED AS REQUIRED**

The revised module defines:

```text
SMALL = (10, 60)
SMOKE = (8, 60)
```

Static inspection establishes:

- the only test-side monkeypatches of `R.E1_GRID` and `R.E1_TICKS` set them to `SMALL`;
- no test changes the stand-in production shape to `SMOKE`;
- `SMOKE` differs from the chain’s stand-in production shape;
- `SMOKE` also differs from the real frozen production shape.

Thus the below-production helpers remain below production:

- before chain setup;
- while the module-scoped chain fixture is active; and
- after fixture teardown.

If a future change made `SMOKE` equal to the frozen or stand-in production shape, the helpers would correctly refuse and expose that drift.

---

# 5. Complete below-production-helper audit

L2 parsed the cumulative Round-7 test source and enumerated every call to the two helper APIs that refuse production shape.

## `_tranche_for_tests`

There are exactly two calls:

```text
test_forged_authorized_quarantine_with_negative_cost_refused
test_tranche_quarantine_fail_closed_and_failed_is_ineligible
```

Both use:

```python
**SMOKE
```

## `run_benchmark_smoke`

There are exactly two calls:

```text
test_benchmark_file_facts_rederived
test_r5_benchmark_manifest_exact
```

Both use:

```python
**SMOKE
```

No below-production helper still receives `SMALL` or an equivalent `(10, 60)` literal.

---

# 6. Remaining `SMALL` uses

## DISPOSITION: **INTENTIONAL**

Every remaining `SMALL` use falls into one of three legitimate categories.

### 6.1 Rehearsal execution

The remaining rehearsal calls use `SMALL` to exercise:

- level completion;
- pass-number derivation;
- whole-level restart;
- off-grid rehearsal refusal.

Rehearsal does not prohibit production shape and carries no scientific classification.

### 6.2 Conformance execution

`conformance_record(..., **SMALL)` intentionally tests the stand-in production configuration and M1 replay. It is not a below-production helper.

### 6.3 Stand-in production chain

The chain fixture and pass-2 end-to-end test intentionally use:

```text
grid = SMALL["grid"]
ticks = SMALL["ticks"]
```

as the reduced-shape production stand-in after monkeypatching the runner’s production constants to that same shape.

Those are production-path tests and must continue to use `SMALL`.

No remaining `SMALL` use belongs to the helper class repaired in Round 7.

---

# 7. Whole-module execution evidence

The packet reports the complete test module in one process:

```text
28 passed in 404.75s
```

This is the relevant container execution mode because it preserves the module-scoped chain fixture across later tests and directly exercises the ordering condition that caused the Windows failure.

The prior Round-6 grouped result did not exercise that condition.

L2 accepts the one-process run as the packet’s execution record. L2 did not independently execute the full test module or Windows suite.

---

# 8. Per-file verdicts

## `mfa_instrument/e1/runner.py`

**VERDICT: SOUND — ROUND-6 CLEARANCE STANDS; FILE NOT REOPENED**

Standing identity:

`f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769`

## `tests/test_e1_m7.py`

**VERDICT: SOUND**

Cleared Round-7 identity:

`252ef6b7d444a83c1cb085c4a91f7f9ba03b1f8ec16d29555afc4229f53b502a`

---

# 9. Placement disposition

**ROUND 7 IS CLEARED.**

M7 may place using exactly:

- unchanged `runner.py`  
  `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769`
- revised `tests/test_e1_m7.py`  
  `252ef6b7d444a83c1cb085c4a91f7f9ba03b1f8ec16d29555afc4229f53b502a`

Required placement sequence:

1. place the two exact files;
2. verify both destination SHA-256 identities;
3. purge stale Python and pytest caches under the standing placement discipline;
4. run the entire canonical Windows suite in its ordinary single-process/module configuration;
5. commit only after that suite is clean;
6. route the placement and canonical suite record.

The second placement run reported:

```text
572 passed, 3 failed, 2 skipped
```

Because Round 7 changes no test count and repairs exactly those three failures, the arithmetic expectation is:

```text
575 passed, 2 skipped
```

The actual canonical suite result governs. This arithmetic is not a substitute for execution.

---

# 10. Authority boundary

This clearance authorizes only:

- placement of the cleared M7 files; and
- the canonical Windows placement suite.

It does **not**:

- ratify the E1-R amendment;
- ratify the governance record;
- ratify the Package Specification;
- authorize a canonical scientific job;
- authorize the calibration tranche;
- authorize production;
- or declare the Stage-1 package complete.

---

# 11. Final verdict

- `runner.py`: **SOUND — unchanged**
- `test_e1_m7.py`: **SOUND**
- nine-line diff: **EXACTLY VERIFIED AGAINST CLEARED ROUND-6 BYTES**
- all below-production helper calls: **USE `SMOKE`**
- remaining `SMALL` calls: **INTENTIONAL**
- one-process execution record: **28 PASSED**
- renewed placement disposition: **CLEARED**

**FINAL VERDICT: SOUND. ROUND 7 CLEARED. M7 MAY PLACE FOR THE CANONICAL WINDOWS SUITE.**
