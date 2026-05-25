# TEST_RECORD_C3-ENV-001 - Environment reproduction + Mesa smoke

## Test identity

- Test ID: C3-ENV-001
- Test name: Environment reproduction + Mesa smoke
- Area: ENV
- Status: passed-L1
- Highest level cleared: L1 implementation / environment
- Record created: 2026-05-25
- Script: cycle3/mesa_smoke_test.py
- Environment snapshot: cycle3/ENVIRONMENT_SNAPSHOT.md
- Lock file: cycle3/requirements.lock.txt

## Purpose

Verify that Cycle 3 ABM work is running under the captured known-good Mesa environment, not system Python, and that Mesa imports at the captured version.

This is an environment / substrate-trust precondition. It clears L1 only. It says nothing about observable validity, steady-state eligibility, or manuscript interpretation.

## Theoretical target

Substrate-trust precondition: no later Cycle 3 claim should rest on an unverified environment.

## Pass criterion

The test clears L1 if:

1. The smoke script runs under the captured known-good environment path.
2. The Python executable is:
   C:\Users\vkz244\EE_Theory_Lab\venv\Scripts\python.exe
3. Mesa imports successfully.
4. Mesa version is 3.5.1.
5. The script prints: SMOKE TEST OK.

## Command run

PowerShell command:

& "C:\Users\vkz244\EE_Theory_Lab\venv\Scripts\python.exe" -m py_compile .\cycle3\mesa_smoke_test.py; & "C:\Users\vkz244\EE_Theory_Lab\venv\Scripts\python.exe" .\cycle3\mesa_smoke_test.py

## Output captured

--- Cycle 3 Mesa smoke test ---
Python executable: C:\Users\vkz244\EE_Theory_Lab\venv\Scripts\python.exe
Python version: 3.14.4
Mesa version: 3.5.1
SMOKE TEST OK

## Result

Passed L1.

The script compiled and executed under the captured known-good top-level venv. The interpreter path, Python version, and Mesa version matched the captured Cycle 3 environment snapshot.

## Interpretation boundary

This result confirms environment reproduction / environment identity only.

It does not establish measurement validity, steady-state eligibility, observable correctness, Regime-II evidence, or manuscript interpretation.

## Follow-up

C3-ENV-001 feeds all later Cycle 3 tests. Later Cycle 3 scripts should be run through the captured venv unless and until Cycle 3 deliberately migrates to a new environment and records that migration.
