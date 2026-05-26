# Cycle 3 - Test Registry

**Purpose:** one master index of every Cycle 3 test. The registry is the table of contents and status board; the full life-cycle of each test lives in its own record built from `TEST_RECORD_TEMPLATE.md`. Nothing is "a test" in Cycle 3 until it has a row here **and** a record file.

**Rule:** a row exists *before* execution (planned), not only after. A test with results but no pre-registered row is a red flag - it means the question was written to fit the answer.

---

## ID convention

`C3-<area>-<nnn>`, where `<area>` is one of:

- `ENV` - environment / substrate construction and verification
- `OBS` - observable definition and measurement-validity tests
- `CTL` - positive / negative control tests
- `SS` - steady-state eligibility tests
- `INT` - integration / end-to-end runs that feed manuscript-facing readings

Example: `C3-OBS-001`. Numbers are not reused; a superseded test keeps its ID and is marked `superseded`, with a pointer to the successor.

## Status vocabulary

`planned` -> `ready` (record complete through "expected output") -> `run` (executed, output captured) -> one of `passed-L1` / `valid-L2` / `eligible-L3` / `interpreted-L4` to record *how far up the four levels it cleared* -> `superseded` / `retired`.

A test does not get a single pass/fail flag. It carries the **highest level it cleared**. Clearing L1 (script ran) says nothing about L2/L3/L4. This is the structural guard against confusing "executed" with "theory supported."

## Four-level reminder (see CYCLE3_OVERVIEW Sec. 3)

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
| C3-ENV-001 | Environment reproduction + Mesa smoke | ENV | substrate-trust precondition (no claim rests on an unverified environment) | mesa_smoke_test.py | passed-L1 | L1 implementation / environment | TEST_RECORD_C3-ENV-001.md | feeds every later test |
| C3-CTL-001 | Synthetic control battery (positive + negative + degeneracy) | CTL | measurement-validity precondition; no real-substrate value interpreted before the battery passes | c3_ctl_001_battery.py | valid-L2 | L2 measurement validity | TEST_RECORD_C3-CTL-001.md | gate for all OBS/INT tests |
| C3-SS-001 | Steady-state eligibility apparatus | SS | steady-state-eligibility precondition; windows earned by explicit diagnostics, never assumed | (Cycle 3 substrate, TBD) | planned | - | TEST_RECORD_C3-SS-001.md | gate for all INT tests |

These three are **precondition tests**: they follow necessarily from the Cycle 2 lessons and are not design choices. Each encodes a Cycle 2 lesson as a standing requirement. None of them, on its own, bears on Regime-II-as-structural; they establish the conditions under which a later test's value becomes interpretable. They must clear before any Cycle 3 substantive probe is interpreted.

### C3-ENV-001 - Environment reproduction + Mesa smoke
**Purpose:** does a fresh environment, rebuilt from `MESA_ENVIRONMENT_REPRODUCTION.md`, run the intended Mesa under the intended interpreter? **Lesson encoded:** substrate trust is a precondition, not an afterthought. **Clears at L1 only** by construction - it says nothing about any observable. **Pass criterion:** smoke test prints `SMOKE TEST OK` under the top-level `venv` interpreter path; Mesa version matches the captured pin. **Gate role:** no Cycle 3 run is credited until the environment it ran in is the reproduced one.

### C3-CTL-001 - Synthetic control battery
**Purpose:** does the Cycle 3 observable apparatus produce the designed discrimination on synthetic cases with NO substrate dependence? **Lesson encoded:** positive controls required before any output is interpreted; a value without its control is not a result. **Carries forward** the Cycle 2 five-case structure (stable cluster / random low-rho / random high-rho / transient wave / uniform-high-persistence degeneracy) as the minimum battery - Cycle 3 may extend it. **Pass criterion stated per level:** L1 the battery runs; L2 positive case produces high signal, negative + degeneracy cases produce near-zero, permutation-null z separates true signal from the uniformity degeneracy. **Co-equal-pair guard:** the transient-wave case is where the two candidate observables may diverge by design; that divergence is recorded as data, not a failure. **Gate role:** the battery passing is the precondition for reading any real-substrate value as a measurement of anything.

### C3-SS-001 - Steady-state eligibility apparatus
**Purpose:** can a window in a Cycle 3 run earn "steady-state candidate" status on explicit diagnostics? **Lesson encoded:** near-zero slope is not eligibility; eligibility is earned by drift, range/mean, and density CV together. **Pass criterion:** the apparatus computes the earned-window filters (relative drift, rho CV, range/mean) and correctly admits/rejects windows on the synthetic controls (whose steady-state status is known by construction). **Gate role:** no integration (INT) test's value is read as Regime II until its window has cleared this apparatus.

> **Not yet seeded, by design:** the `C3-OBS-*` observable-definition tests and the `C3-INT-*` integration runs that bear on Regime-II-as-structural. Those are the substantive design question, handed to the multi-AI design phase. The Flight 2 experience indicates substrate-led design produced cleaner probe structure than architecture-led. Seeding them here would settle by framing what should be settled by engagement. Add them as the design phase produces them.

## Co-equal-pair guard

Where a test touches the candidate Psi observables, the registry row must **not** imply which observable is the theoretical Psi. The two candidates - per-tick state organization that persists, and the same cells persistently clustered - are held co-equal until the ontological question (CYCLE3_OVERVIEW Sec. 4) is settled by Mike / Layer 1. Script names, column names, and registry entries are forbidden from quietly settling it. Genuine divergence between the two (e.g. a transient-wave case) is **data**, recorded as such, not smoothed into one reading.

## Standing exclusions (do not register these as Cycle 3 tests)

- B2-source file hunts - closed.
- Flight 6 parquet substrate-trust forensics - closed absent a new conflict.
- Any additional copy of the Tier 2 analysis script.

