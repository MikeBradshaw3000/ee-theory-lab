# Cycle 2 Round 1 Flight 1 — Closure: v1.1 Parity Verified

**Date:** 14 May 2026
**Phase:** Cycle 2 Round 1 Flight 1 — CLOSED
**Status:** Substrate trust floor for v1.1 established under F_baseline. Flight 2 design opens next. Five deferred remediations fold into Flight 2 preparation.

---

## Closure summary

The v1.1 NumPy substrate implementation (`v1_1_parity_check.py`) passes the parity check protocol specified in v1.1 Section 12. Four SHA-256 hashes match between Run A (telemetry disabled) and Run B (telemetry enabled) under F_baseline, 20×20 grid, 1000 ticks, matched PRNG seed (0x7A9B31C). Production output (`flight6_parity_RunB.parquet`) contains 400,000 rows, 25 columns, tick range 0–999, 400 unique cells.

Architectural review by Claude (Layer 1) passes the implementation against v1.1's primitive compliance, vocabulary quarantine, drive function specification, Ψ_local computation, Q diagonal discipline, telemetry capture, and Section 15 prohibitions. Layer 2 (ChatGPT) review of the deferred-remediation list pending at time of writing.

## Empirical artifacts

```
v/u/r matrices hash:   a1e82728ffe7f11c79341ea2823c7d81874b9f7243030f3902ce40ad21502f77 (Match: True)
is_active matrix hash: 6dc5a0358f2c846198aaa190a2ee44100e4b3288a79206c538ddbebb710aa251 (Match: True)
rho(t) series hash:    dcac2be383c91af01d767cb3aa935dc4843293ecea4e951f82c29090e728ec1f (Match: True)
psi(t) series hash:    56bda7b221a789efcefebdfc75bb0bc946a5f95745788d1bb66a38703e6dcda4 (Match: True)
PARITY_CHECK: PASS
```

Clipping summary across 1000 ticks: v=75, u=18, r=27.

In-memory invariant check: 0 mismatches across 400,000 rows (tautological — see deferred remediation 1).

## Implementation environment

- Machine: production (Mike's workstation)
- Path: `C:\Users\vkz244\EE_Theory_Lab\`
- Implementation: pure NumPy substrate (Mesa parallel implementation deferred per Section 4 alternative-implementation note)
- Dependencies: numpy, pandas, hashlib, time, pyarrow
- Script file: `v1_1_parity_check.py` (canonical Flight 1 substrate; commits to repo)
- Output file: `flight6_parity_RunB.parquet`

## What the architectural review verified

Per v1.1 Section 11 telemetry table, all 25 required columns present with spec-matching names: Tick, Agent_X, Agent_Y, b_i_v, b_i_u, b_i_r, limiting_base_argmin, Lambda_multiplicative, Lambda_additive, Lambda_total, Local_Density, Drive_Raw, Term_Density_Pos, Term_Overcrowding, Term_Offset, p_base, p_act, PRNG_draw, is_active, Psi_local, gamma_coef, Delta_v, Delta_u, Delta_r, Term_Lambda.

Per v1.1 Section 15, all twelve prohibitions cleared: no global Λ substitution, no uniform base values, no sinusoidal Ψ formulas, no density-only Ψ proxies, no two-base Q updates, no scaled Lambda_multiplicative, no two-value indicator placeholders, no schema-emulation, no telemetry vectors fewer than 25 columns, no mid-execution substrate substitution, no Stabilization Mode placeholders, no emergency simplified substrate.

The PRNG-state-sharing structure between Run A and Run B is correctly designed: the telemetry write path consumes no PRNG draws, so the call sequence is identical between A and B. This is the load-bearing property for parity, and it holds.

## Five deferred remediations (Flight 2 preparation, not Flight 1 blockers)

These items were caught in architectural review but do not block Flight 1 closure. They fold into Flight 2 preparation.

**1. Realization-invariant verification is currently tautological.**

The in-memory check in the current implementation:

```python
invariant_matrix = (next_state == True) == (prng_draw < p_act)
self.invariant_mismatches += np.sum(~invariant_matrix)
```

evaluates `next_state` against its own definition (`next_state` was assigned `prng_draw < p_act` two lines earlier). It reports zero mismatches by construction, regardless of whether the spec's invariant is genuinely held.

v1.1 Section 14.2's intended check is on persisted parquet values: read back the PRNG_draw, p_act, is_active columns from the .parquet file, verify `is_active = (PRNG_draw < p_act)` across all rows. This needs to be implemented as a separate post-execution verification step before Flight 2 production runs (1.2M rows at 20×20, 4.8M rows at 40×40), where Section 14.2 requires full per-(cell, tick) verification as default.

For Flight 1 (channel-test parity under F_baseline per Section 12.4), the four-way hash match is the load-bearing parity verification. Flight 1's parity verdict is sound (the hash match is real); the invariant-verification piece is a Section 14.2 requirement that gets fully honored at Flight 2.

**2. Mesa-NumPy parity-comparison artifact deferred.**

v1.1 Section 4 anticipated both Mesa and NumPy implementations with cross-comparison verification ("Verified to produce identical telemetry to Mesa implementation under matched PRNG seed"). Practical Mesa issues (3.x API regressions, performance freezes) led to NumPy-only as canonical baseline. Honest accounting of this is in the implementation file's opening comment. Acceptable on practical grounds. Recorded so that if Mesa parallel implementation ever becomes feasible, the cross-comparison can be done.

**3. Execution timestamp missing from parquet metadata.**

v1.1 Section 13.4 lists six required metadata fields: F_variant ✓, Scale ✓, PRNG seed ✓, Substrate specification version ✓, Total tick count ✓, **Execution timestamp** (missing). Trivial fix: `time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())`. Add before Flight 2 production runs.

**4. File size missing from completion-verification output.**

v1.1 Section 14.1 calls for "File size: X bytes" in the per-file verification block. Trivial fix. Add before Flight 2.

**5. Stale internal comment.**

The initialization loop carries a comment "Match Mesa's cell-by-cell PRNG draw sequence exactly" referencing a now-abandoned Mesa parallel implementation. Cleanup item; not behavior-affecting.

## What Flight 1 closes

- **Substrate trust floor for v1.1 under F_baseline** is established. Telemetry is listen-only (hash-identity between Run A and Run B). All 25 columns populated by real computation per spec. Q diagonal discipline honored.
- **`v1_1_parity_check.py` becomes the canonical Flight 1 substrate.** Flight 2's F_LR and F_2_symmetric implementations extend it, not replace it.
- **The committed v1.1 spec is operational.** No spec revisions surfaced through implementation; the spec is internally implementable as written.

## What Flight 1 does not close

- **Substantive cascade behavior under F_LR and F_2_symmetric.** Flight 2's question.
- **Production-grade realization-invariant verification.** Per deferred remediation 1.
- **Full provenance metadata.** Per deferred remediation 3.

## What opens next

Flight 2 design — F_LR and F_2_symmetric cascade behavior at 20×20 and 40×40 scales over 3000 ticks each, producing the four production .parquet files specified in v1.1 Section 13. Flight 2 substrate extends Flight 1's implementation with the F-form selection mechanism (Section 7.4), incorporates the deferred remediations 1, 3, 4, cleans up remediation 5, and acknowledges remediation 2 in its declaration.

— Mike (drafted with Claude's architectural review)
