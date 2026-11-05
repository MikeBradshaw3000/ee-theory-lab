# L1 → L2 — Flight 8 M7 build, round 6: a canonical-suite finding after the round-5 SOUND (Windows rename refusal), one contained repair

**Date:** 2026-11-04. **Register:** module build review, receipt-first. **Repository pin:** `ee-theory-lab` HEAD `1978a01` (unchanged; the round-5 bytes were placed in the working tree and staged, NOT committed — a placement commit is made only on a passing canonical suite). **Round-5 review:** `L2_F8_M7_ROUND5_REVIEW_2026-11-03_RECEIVED.md` (`e0abb753…`), in this zip as `_RECEIVED` beside its superseded first issue (`…FIRST_ISSUE_RECEIVED.md`, `66984d3c…`, both verdict lines bold; `_current_dispositions` returns two malformed dispositions on it, so L2 re-issued with one plain line). Only `runner.py` and `test_f8_m7.py` change; `config.py`, `test_f8_m1.py`, `null.py` are byte-identical to rounds 3–5.

## 0. Receipt first — as before, then "execute".

## 1. What the canonical suite found

On the round-5 bytes (`runner.py` `97c861f9…`, cleared SOUND), the canonical suite on the canonical machine (Windows 11, py3.14.4, np2.4.4) ended **841 passed, 2 skipped, 18 errors in 1:41:49** (errors section and summary line attached as `f8_m7_suite_2026-11-04_FAILED_errors.txt`, as Mike extracted it from the suite output). All 18 are the M7 chain fixture: its first production level after the prerequisites commit, `run_level(2.402174, skeleton_low, canonical)`, raised `PermissionError: [WinError 5] Access is denied` at `os.replace(partial, level_dir)` — the all-or-nothing rename of the finished `.partial` level directory to its final name (`runner.py` line 1248 of the round-5 bytes). Twenty-four calibration levels had renamed the same way moments earlier; E1 M7 uses the identical pattern and has passed on this machine.

**Cause, measured, not inferred:** a probe with no instrument code (`rename_probe.py`, attached) writes 20 parquet + 20 json files into a `.partial` directory and renames it, 60 times. On the canonical machine: **1 refusal in 60, `PermissionError (5)`, retry succeeded after 0.10 s**; on the container 0 in 60. Windows refuses to rename a directory while any handle is open inside it; a real-time scanner briefly holds a freshly written file. The bytes in the directory are not at issue.

## 2. The repair (`runner.py`)

`_seal_level_dir(partial, level_dir)` replaces the one bare `os.replace` in `run_level`: it retries the rename on `PermissionError` only, every 0.1 s, for a bounded 10 s, and otherwise raises exactly as before (any other exception at once; `PermissionError` after the bound). The rename is still all-or-nothing; nothing written, hashed, validated or memoised changes; no other rename site exists in the runner, and the `shutil.rmtree` sites are unchanged (none failed). The declaration tuple is unchanged (`0ce2e7b5…`; `verify_frozen_identity` passes on the submitted bytes).

**Test** (`test_p1_level_seal_retries_a_transient_rename_refusal_and_bounds_it`): with `os.replace` refusing three times then succeeding, the seal succeeds on the fourth call and the directory contents are intact; with a refusal that never clears, `PermissionError` is raised after the bound (≈10 s; the `.partial` directory is still there, nothing half-renamed); a `FileNotFoundError` is not retried. The module record on the container (41 tests) is attached.

## 3. What L1 asks of L2

Disposition on the repair as a contained change to cleared bytes (one function, one call site), and whether the retry's bound and its scope (`PermissionError` only) are the right ones. The canonical suite will be run again on the submitted bytes before any commit; Mike's suite record will be the evidence of record for the machine.
