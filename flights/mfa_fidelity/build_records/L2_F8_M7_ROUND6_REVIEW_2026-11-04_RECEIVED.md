# L2 — Flight 8 M7 module build review, round 6

FINAL VERDICT: SOUND

**Date:** 2026-11-04. **Register:** Module build review under frozen Contract F8 v0.8.4. **Decision authority:** Mike. **Repository pin declared by L1:** `ee-theory-lab` `1978a01`, unchanged; submitted working-tree changes not yet committed. **Scope:** the contained directory-seal retry repair following the round-5 clearance and the reported canonical-machine rename refusal.

## 1. Disposition

The submitted round-6 repair is accepted. The change preserves the existing directory-rename operation, retries only `PermissionError`, and propagates exhaustion or any other exception. It introduces no change to scientific computation, run artifacts, authorization checks, record construction, validation, or memoization. Exact reconstruction of both round-5 file identities establishes the disclosed change boundary.

The ten-second monotonic retry budget and 0.1-second pause are reasonable for this operational recovery. Ten seconds is a retry budget, not a strict upper bound on total elapsed time. No blocking source defect was found within the round-6 change.

This clears the named round-6 source and test bytes for the module build review. The fresh canonical-machine suite remains the established gate before a placement commit. This review supplies no scientific-run authorization and does not certify that the repaired Windows suite has already passed. [S1, S2, S3, S4, S8]

## 2. Receipt and evidence identities

The archive SHA-256, file count, and every manifest entry were independently checked before review: **97 files = 96 payloads + `MANIFEST.txt`; 96/96 payload hashes matched; no missing, unlisted, duplicate, or CRC-failing entries.** The 96 extracted payloads were checked against the same manifest again after the independent tests; none had changed.

Paths below are relative to `flights/mfa_fidelity/`, except the archive and root manifest.

| Ref. | Received object | Full SHA-256 |
|---|---|---|
| A | `f8_m7_build_round6_L2.zip` | `ce8a555ae4b3a80b12f2895cd340729a633c35fdfc0c3a13e00d24faf4aa9c37` |
| M | `MANIFEST.txt` | `63daeb4d135e61ac454845463a2cc0002cdb10d04907cba16aed6f5148d70b3c` |
| S1 | `build_records/L1_TO_L2_F8_M7_ROUND6_RESPONSE_2026-11-04.md` | `5e7a403665f96b603c983569391e28748a326edccf5de05e1ea951286e854116` |
| S2 | `instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` |
| S3 | `instrument/tests/test_f8_m7.py` | `47b7a25c814390dc493f194ef1ba2ab6f97251559c8cb9f9e7df2d67f786b29e` |
| S4 | `build_records/L2_F8_M7_ROUND5_REVIEW_2026-11-03_RECEIVED.md` | `e0abb753e0cd34079a69a5ccb7bb64ce7cc09d844b989d2b118a0bad2f0ad72a` |
| S5 | `build_records/f8_m7_suite_2026-11-04_FAILED_errors.txt` | `944331e41a2f7b79c97edb36929eb43e5a01194d3b9ef331c4bbdbd0ea041a9c` |
| S6 | `build_records/rename_probe.py` | `4483e4b4f54556c2098b793a202e1cdc8361fb0792faae87fb34dd26765e89db` |
| S7 | `build_records/f8_m7_module_container_round6_2026-11-04.txt` | `aa072f00246cd01f0d829840bdc5274a6e25d39289ac0b6dcd8efafd60c67ba3` |
| S8 | `contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` |
| S9 | `build_records/F8_M7_PLACEMENT_NOTE_2026-11-04.md` | `efd30727df967ce2965c1e340267760d0ef439cd92ea36fb143d2b4c607bc5ab` |

The corrected round-5 review S4 is the prior clearance of record. Its superseded first issue is present with SHA-256 `66984d3cf80c512098f18df03b945c41544d30d410b037d4e0e117983e6a1976`; it is not substituted for S4.

## 3. Exact change containment

L2 reconstructed the prior files in memory from the received round-6 bytes and compared their full SHA-256 values with the identities recorded in S4.

| File | Inverse edit applied solely for the comparison | Reconstructed round-5 SHA-256 |
|---|---|---|
| F8 `runner.py` | Remove the new helper and its separator at current lines 1082–1097; restore the sole call at current line 1264 to `os.replace(partial, level_dir)`. | `97c861f90580bfa5e480160e0bb2f6236295206432a12a10944e0097c55a1b66` |
| `test_f8_m7.py` | Remove the appended test and its two preceding blank lines, current lines 875–899. | `2f4ba68fc6344bb9434c466bc791381a3af86265709aa1c837d645bd936ddc30` |

**Both reconstructed digests exactly match the cleared round-5 identities.** Thus, within these two files, the helper, its single call-site substitution, and the appended regression test account for every changed byte. No submitted file was edited to perform this comparison. [S2, S3, S4]

The three companion identities expressly carried forward from round 5 also match S4:

| Companion file | Unchanged SHA-256 |
|---|---|
| `instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` |
| `instrument/tests/test_f8_m1.py` | `ca9a547286290aabc497fc228e10dd845711cd1b359bc21fcb125d92e8285007` |
| `instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` |

The runner declaration digest remains `0ce2e7b5eaca1804b10cc68706380bd93f5efe007c34c7fe74a6eb878cd8b4b8`. L2 independently imported the submitted runner and passed `verify_frozen_identity()`; the focused pytest run also passed the declaration and tamper checks. An unchanged declaration digest does not substitute for the new source identity: this clearance binds S2 and S3 explicitly.

## 4. Repair assessment

### R6-1 — Exception scope and failure behavior: accepted

The helper at S2 lines 1082–1095 catches `PermissionError` only. On a successful `os.replace`, it returns immediately. On persistent permission refusal, it re-raises the active exception once the deadline is reached. Other exception types leave the helper immediately.

This is an appropriate recovery boundary. A permanent permission problem can delay failure by the retry budget, but cannot become a successful seal without a successful rename. Broadening the catch to all filesystem errors would be unnecessary; restricting recovery to a particular Windows error number is not needed for correctness here. The helper neither clears an error flag nor reports success while leaving the source directory unsealed. [S2:1089–1095]

### R6-2 — Interval and bound: accepted, with precise timing interpretation

The deadline is computed from `time.monotonic()`, and each retry pause requests 0.1 seconds. The deadline is checked after a failed attempt. Consequently, the final sleep and next rename attempt can extend elapsed time slightly beyond ten seconds; OS-call duration and scheduling can add further delay. A successful attempt after the final sleep is still accepted.

L2's controlled-clock probes reached approximately 10.1 virtual seconds under persistent refusal, illustrating that boundary. The submitted real-time test allows 9.5–20.0 seconds for the failure branch. These facts support a finite operational retry budget, not a hard real-time timeout guarantee.

The reported recovery after 0.10 seconds motivates retrying the operation; it does not establish that ten seconds is an empirically optimal cutoff. Ten seconds is nevertheless a reasonable conservative engineering choice for this contained repair, and no stricter seal deadline is specified by the governing contract. No additional scientific threshold or data-dependent decision rule is introduced. [S1 §2; S2:1090–1095; S3:891–896; S8 §7]

### R6-3 — Directory publication and record integrity: accepted

The helper retains the same `os.replace` operation as the sole directory-rename site in the runner. It adds no file-copy fallback, content rewrite, recalculation, or per-file publication. All twenty runs are produced before the call; `LevelRecord` construction and canonical record persistence remain after the call. Exhaustion therefore propagates before a new successful level record is constructed or persisted. [S2:1256–1272]

The all-or-nothing property concerns publication of the newly completed directory. The existing removal of a previous destination at line 1263 is unchanged; this repair does not create a rollback guarantee for an older destination. That distinction is carried into this clearance without reopening the pre-existing behavior.

The stage, authorization, job/object, prerequisite, production-shape, adapter, and dependency checks remain before execution. Exact byte reconstruction also preserves the post-seal labels, hashes, records, validators, and memo logic. Contract §7.1–§7.4 and the previously cleared scientific decisions remain unaffected. [S2:1232–1252, 1265–1272; S8 §7]

## 5. Independent L2 verification

### 5.1 Focused pytest execution on the submitted module

From `flights/mfa_fidelity/instrument`, L2 ran:

```bash
python -m pytest tests/test_f8_m7.py -q -p no:cacheprovider   -k "level_seal or frozen_identity or tamper_is_caught or rehearsal_level_record or d8_clearance or r3_2"   --durations=12
```

**Result: 11 passed, 30 deselected in 17.63 seconds; exit code 0.**

The selected items comprise the new seal regression, the frozen-declaration test, six declaration-tamper cases, the reduced-shape artifact/replay test, the exact-clearance-marker test, and the round-5 fence/indentation regression through `verify_placement`.

The new seal regression passed in 10.32 seconds total. It exercises three transient refusals followed by success on attempt four; persistent refusal with preservation of the `.partial` directory and absence of the destination; and propagation of `FileNotFoundError`. The artifact/replay test additionally traverses the actual `run_level` call site and validates the resulting artifacts, replay, and tamper rejection. [S3:142–159, 263–279, 593–620, 793–821, 877–899]

**L2 environment:** Linux x86-64, CPython 3.12.14, NumPy 2.3.5, pandas 2.2.3, PyArrow 26.0.1, pytest 9.2.0, SciPy 1.17.0. Missing test dependencies were installed in an isolated review directory; pytest plugin autoload and bytecode writing were disabled. This is an independent noncanonical test run.

The captured command/output/exit-code transcript has SHA-256 `6060081d88f56eea9d5515e40a7da909838bc53e5252c0f7f03fd410ce6f0363`.

### 5.2 Controlled helper checks

Additional L2 checks compiled the exact helper body extracted from S2, with isolated controlled-clock and rename dependencies. These checks establish specific helper behavior; they are not represented as full-module execution.

| Check | Observed result |
|---|---|
| Immediate success | One real directory rename; zero sleeps. |
| Three refusals then success | Four attempts; three 0.1-second sleeps; source `.partial` absent after success. |
| Content preservation | Original file bytes and before/after file hashes matched after a successful seal. |
| Persistent permission refusal | Original exception propagated; source directory and bytes retained; destination absent. |
| Other exception types | `FileNotFoundError`, generic `OSError`, and `RuntimeError` propagated on the first attempt with no sleep in the applicable checks. |

These checks address two limits in the new submitted test: its success assertion checks the filename list rather than the content bytes, and its non-permission assertion checks the exception rather than an explicit one-call count. Neither limit requires a blocking repair given the direct source structure and the independent observations.

## 6. Submitted evidence and its limits

### 6.1 Failed canonical-suite excerpt

S5 contains 120 lines / 12,330 bytes. It shows a complete setup traceback for `test_chain_canonical_jobs_produced_authorized_records`, ending at the old bare rename with `PermissionError: [WinError 5] Access is denied`, then starts the next fixture-error report. It does **not** contain the terminal pytest summary.

Accordingly, **841 passed, 2 skipped, 18 errors in 1:41:49** is treated as L1's reported canonical-suite outcome in S1, not as a total independently recovered from S5. The current test module has eighteen tests using the shared `chain` fixture, consistent with the reported error multiplication, but the excerpt does not display all eighteen reports.

The response's statement that the summary line is attached overstates the supplied raw excerpt. This qualification does not prevent reviewing the demonstrated failing operation or the repair. The fresh canonical-suite record remains necessary for placement. [S1 §1; S3; S5:1–120; S7:11]

### 6.2 Probe outcome and causal attribution

S6 supplies the probe source. L1 reports one refusal in sixty Windows trials, recovered after approximately 0.10 seconds, and no refusals in sixty container trials. A separate captured probe transcript is not included.

Even accepting those reported outcomes, the probe observes refusal and recovery; it does not identify which process held a handle or establish a real-time scanner as the cause. The defensible causal statement is: **the canonical traceback establishes a Windows directory-rename refusal; L1 reports a transient reproduction that recovered on retry; scanner interference is an explanation not independently established by the attached evidence.**

The runner's docstring uses “may,” appropriately. The stronger “Cause, measured, not inferred” language in S1 and the categorical scanner attribution in the new test's docstring exceed the evidence. These are reporting qualifications, not defects in the exception-specific repair. [S1 §1; S2:1083–1086; S3:878–880; S6:9–32]

### 6.3 Full-module record and placement status

S7 binds the submitted runner and test hashes and supplies a completed Linux module record: **41 passed in 2956.20 seconds (49:16)**. Its reported environment is Python 3.13.18 and NumPy 2.5.3 on Linux. This is reviewed L1 execution evidence. L2 independently reproduced the focused eleven-test selection above, not the complete forty-one-test run.

S7 also states that the earlier 244-test touched-module regression was not rerun. That earlier result is not relabelled as round-6 execution.

S9 contains prepared placement/commit wording. This review relies on S1's explicit status: the pin is unchanged, nothing has been committed, and a new canonical-machine suite will precede any placement commit. S9 is not evidence that those future steps have already occurred. [S1 opening and §3; S7:3–28; S9]

## 7. Clearance boundary and next gate

There is no blocking repair request arising from this round. The helper's exception scope, retry budget, and single integration point are accepted; the submitted runner and test identities in S2 and S3 are the cleared objects.

L1 may proceed to the already-required canonical-machine suite on those exact bytes. A passing canonical record, followed by the established placement and governance requirements under Mike's authority, is still required. A source change made in response to that run would need its own disclosed review boundary.

The prior M1 a′ disposition, Interpretation 003, and earlier closed M7 findings are carried forward. This round neither replaces the canonical suite with Linux evidence nor authorizes a production job.

