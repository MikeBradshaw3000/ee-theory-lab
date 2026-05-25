# Cycle 3 — Test Registry

**Purpose:** one master index of every Cycle 3 test. The registry is the table of contents and status board; the full life-cycle of each test lives in its own record built from `TEST_RECORD_TEMPLATE.md`. Nothing is "a test" in Cycle 3 until it has a row here **and** a record file.

**Rule:** a row exists *before* execution (planned), not only after. A test with results but no pre-registered row is a red flag — it means the question was written to fit the answer.

---

## ID convention

`C3-<area>-<nnn>`, where `<area>` is one of:

- `ENV` — environment / substrate construction and verification
- `OBS` — observable definition and measurement-validity tests
- `CTL` — positive / negative control tests
- `SS` — steady-state eligibility tests
- `INT` — integration / end-to-end runs that feed manuscript-facing readings

Example: `C3-OBS-001`. Numbers are not reused; a superseded test keeps its ID and is marked `superseded`, with a pointer to the successor.

## Status vocabulary

`planned` → `ready` (record complete through "expected output") → `run` (executed, output captured) → one of `passed-L1` / `valid-L2` / `eligible-L3` / `interpreted-L4` to record *how far up the four levels it cleared* → `superseded` / `retired`.

A test does not get a single pass/fail flag. It carries the **highest level it cleared**. Clearing L1 (script ran) says nothing about L2/L3/L4. This is the structural guard against confusing "executed" with "theory supported."

## Four-level reminder (see CYCLE3_OVERVIEW §3)

| Level | Clears when | Settled by |
|---|---|---|
| L1 implementation | script runs, output well-formed | Layer 3 / Layer 2 |
| L2 measurement validity | quantity is state-based, density-adjusted, degeneracy-checked | Layer 3 / Layer 2 + Layer 1 intent |
| L3 steady-state eligibility | window earned by explicit diagnostics | diagnostics + Layer 1 |
| L4 manuscript interpretation | meaning for Regime-II-as-structural | Mike / Layer 1 only |

---

## Registry

| ID | Test name | Area | Theoretical target | Script (ver) | Status | Highest level cleared | Record file | Follow-up |
|----|-----------|------|--------------------|--------------|--------|----------------------|-------------|-----------|
| _C3-ENV-001_ | _Environment reproduction + Mesa smoke_ | ENV | _substrate trust precondition_ | _mesa_smoke_test.py_ | planned | — | _TBD_ | _—_ |
| | | | | | | | | |

> Rows above the blank line are illustrative placeholders showing the intended shape. Replace with real entries as the Cycle 3 test plan is written. Keep one row per test; long detail belongs in the record file, not here.

## Co-equal-pair guard

Where a test touches the candidate Ψ observables, the registry row must **not** imply which observable is the theoretical Ψ. The two candidates — per-tick state organization that persists, and the same cells persistently clustered — are held co-equal until the ontological question (CYCLE3_OVERVIEW §4) is settled by Mike / Layer 1. Script names, column names, and registry entries are forbidden from quietly settling it. Genuine divergence between the two (e.g. a transient-wave case) is **data**, recorded as such, not smoothed into one reading.

## Standing exclusions (do not register these as Cycle 3 tests)

- B2-source file hunts — closed.
- Flight 6 parquet substrate-trust forensics — closed absent a new conflict.
- Any additional copy of the Tier 2 analysis script.
