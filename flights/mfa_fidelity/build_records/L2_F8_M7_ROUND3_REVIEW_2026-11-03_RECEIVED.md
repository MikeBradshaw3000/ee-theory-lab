# L2 — Flight 8 M7 build review, round 3

FINAL VERDICT: DEFECT-WITH-REPAIR

**Date:** 2026-11-03 (UTC). **Register:** module build review. **Reviewer:** L2. **Decision authority:** Mike. **Declared repository pin:** `ee-theory-lab 1978a01` (the supplied container record expands it to `1978a017cbbfaacfeda0568770621e3194e76588`). Ratified Interpretation 003 is placed; M7 and the M1 touch are submitted for review and remain unplaced.

**Submission:** `f8_m7_build_round3_L2.zip`, 606,884 bytes, SHA-256 `a666a2b385016d3e2c3d1b374dab616e9c4e3e9dbea7d795b4fff98eead5a29a`. **Bundle count:** 83 payload files plus `MANIFEST.txt`, 84 file entries. All 83 full payload digests match the manifest. Receipt was completed before Mike's instruction to execute.

**Instruction source, read first:** `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M7_ROUND3_RESPONSE_2026-11-03.md`, SHA-256 `d281b3fdebbddd196150330d7e714b79db29a5374e97ec6000b32344ed9017a0`.

## 1. Disposition

M7 is **DEFECT-WITH-REPAIR**. The original absolute manifest dependency, null-body direct-entry, ordinary quoted-verdict, ruling-identity, crossing-index, commitment, and declaration-sentinel witnesses have been addressed in the submitted code. However, the cache completeness and clearance obligations remain unsatisfied by concrete counterexamples detailed below. A third counterexample establishes missing object association at the shared predecessor gate: a replay-valid skeleton-high sweep is accepted in the realization sweep slot even with the dependency memo empty.

The submitted **M1 touch is SOUND within the authorized a′ scope**, and R2-7 is closed. Both touched M1 files are identified in §2.1. Its 73 tests pass within the 244-test regression run, and the full disclosed touch reconstructs exactly from the identified predecessors. Its placement remains coupled to M7 under I003; this component disposition does not authorize placing it alone.

Mike's H1(a), H2(a), and a′ dispositions stand. Ratified Interpretation 003 is the governing record; its three corrected passages are applied as ratified. **No change to Interpretation 003 is required by this review.** There is no new scientific passage condition, no reopening of the independent stability panel, and no demand that failed reproduction become a P1 stop.

This review establishes build evidence using temporary repositories and disclosed fixtures. It grants no project production authorization and does not certify Mike's canonical Gate-B environment or repository-wide suite. The real repository history at `1978a01` was not independently cloned; the submitted identified records and Mike's provenance are the authority used here.

## 2. Source and evidence record

### 2.1 Exact reviewed identities

Paths in the following table are relative to `flights/mfa_fidelity/`. Source references such as R:745 identify one-based lines of the exact submitted file, not a later checkout.

| Ref | File | Full SHA-256 |
| --- | --- | --- |
| R | `instrument/mfa_instrument/f8/runner.py` | `da0b6e58623c947fd24ef4448469eccf682866514eb46586adcd86b2b1b9f473` |
| T | `instrument/tests/test_f8_m7.py` | `309e063fa24fb1b9457ed0663a12e5fb0f6cfbadc13345569bee8b3c3dbcbf66` |
| M1 | `instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` |
| T1 | `instrument/tests/test_f8_m1.py` | `ca9a547286290aabc497fc228e10dd845711cd1b359bc21fcb125d92e8285007` |
| M3 | `instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` |
| C | `contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` |
| I003 | `rulings/F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md` | `6ebf0ad3efbe8e0e74b45e63d5f6ba550441897f3ff6898749230c064c993e9e` |
| R2 | `build_records/L2_F8_M7_ROUND2_REVIEW_2026-11-03_RECEIVED.md` | `f5c61978c7f183d7de8ec1af2f602cbc87629f668bf1b43f3571a36c71977e1a` |
| A2 | `build_records/L2_F8_M7_ROUND2_I003_RATIFICATION_ADDENDUM_2026-11-03_RECEIVED.md` | `ec26e21e82d7e4c9daa605b3abe73e9dc8ae31c6645fc7d731bcacd6307bf55a` |
| DN | `build_records/F8_M7_DESIGN_NOTE_2026-11-02.md` | `3cd03a097c562d8ff51bc2e6f78a5f4ebe99ae0cb7b6b37a601ae3be68472572` |

Only four Python files differ from round 2: R, T, M1, and T1. M3 and all other common submitted Python files retain their round-2 identities. The supplied M1 touch diff, SHA-256 `c880b82e8344843d060f5fa5eb0b32f3353db2b0fad60e14ddaea5bdf90c2a20`, reconstructs M1 and T1 byte-for-byte from the identified placed predecessors `43ea8de23c0d718b246936c7ff6f18e4f8e5243f77ddb240d896e5d00bdf0e07` and `23d4260f5a2d996b56e748aada1e7ed5d5b6d35e57bc41be9fdc53b34b04bff0`. The source comparison and diff reconstruction are captured in the evidence bundle.

### 2.2 Local test execution

| Local execution | Result | Status and timing |
| --- | --- | --- |
| Submitted M7 module, 37 tests collected | **19 PASSED observed; run incomplete** | The complete integration chain and census replay tests passed. The executor lost the process during `test_chain_package_replays_and_refuses_forgery`; no final exit status or pytest summary was written. Started 20:08:25 UTC; absence confirmed 21:01:37 UTC. |
| M1, M2/M3, M4, M5, M-P1, M6 regression modules | **244 passed** | Exit 0; pytest reports **867.36 seconds**. |
| M1 component within that regression run | **73 passed** | Included in the 244, not an additional run. |

The remaining regression counts are M2/M3 34, M4 17, M5 30, M-P1 35, and M6 55. The supplied L1 record separately reports 37 M7 passes in 3627.84 seconds; that is L1's result, not a completed local L2 result.

The submitted test runs were started without source edits, from `flights/mfa_fidelity/instrument`, with `-vv -p no:cacheprovider --durations=12 --tb=short`. The M7 invocation names `tests/test_f8_m7.py`. The regression invocation names M1, M2/M3, M4, M5, M-P1, and M6 test modules. `run_tests.py` records each exact argument vector, working directory, and start time, and writes end time and exit status on normal completion; only the regression run reached that final write. Third-party pytest plugin autoload was disabled; no submitted test was skipped or substituted by the review harness. The M7 process interruption leaves the original log and status record unchanged. `m7_interruption_observation.json` records the last running-session observation, the executor's unknown-process response, absence of the pytest and wrapper processes, the 19 completed passes, and both captured-file digests. The termination cause and exit code were unavailable. The interrupted package test and the remaining tests have no completed result from this invocation. No M7 test failure is inferred from this infrastructure event, and no full local 37-test pass is claimed. The three completed counterexample probes independently establish the adverse build disposition.

The local interpreter is CPython 3.12.14 with NumPy 2.3.5, SciPy 1.17.0, pytest 9.2.0, and PyArrow 26.0.0, on Linux/glibc 2.39. Review-only dependencies are isolated on `PYTHONPATH`. This is distinct from L1's submitted container record and from the canonical qualified machine.

The successful-chain fixture's scope is as disclosed by T: production-shaped structural integration with the lattice stepper, M6 audit producer, known-answer producer, and M5 finite-N projection count process replaced consistently by deterministic test fixtures. The real M6 pricing experiment and replay remain in the suite. Test results demonstrate the exercised controls, not a production scientific result or completeness beyond the tested cases.

### 2.3 Probe boundaries

The cache counterexample uses real stage binding, Git/history, committed authorizations, canonical serialization, manifest validation, all 48 calibration LevelRecords and 960 kept run artifacts, census derivation, and both cache implementations. Its environment and numerical stand-ins are exactly identified in §4.1. No readiness, census, artifact-replay, or dependency-gate validator is replaced. A sentinel stops the first execution call of the attempted scientific job.

The clearance counterexample uses unmodified `_current_dispositions` and `verify_placement`, real Git, exact submitted runner/test bytes, and a synthetic suite record used solely as a parser fixture. It does not claim the canonical suite ran.

The I003 probe uses real stage/placement/adapter/governance machinery with the supplied environmental-conformity stand-in. The stability probe uses diagnostic observations and the actual M-P1 comparison functions; it claims no lattice trajectories. M1/M7 sentinel probes change in-memory literal values only and restore them. The object-association follow-up uses a private committed snapshot of the completed realization-census fixture, with all record, readiness, gate, authorization, and commitment validators unmodified. It calls no public production entry point. Its exact fixture substitutions and the separate isolated route evidence are distinguished in R3-3.

## 3. Disposition of R2-1 through R2-7

| Round-2 item | Round-3 disposition | Basis |
| --- | --- | --- |
| **R2-1 — readiness dependencies** | **PARTIAL; R3-1 remains.** | Absolute/Windows/traversal/unnormalized manifest paths refuse; ordinary named dependency edits invalidate warm readiness; missing pinned roots fail before cache lookup. Accepted implicit calibration artifact paths can still leave both keyed trees through a directory alias. |
| **R2-2 — direct production predecessors** | **PARTIAL; R3-1 remains. R3-3 also remains.** | Both public routes now call the semantic loader and refuse the original wrong-schema and null-body envelopes. The new shared cache can suppress replay after a consumed artifact changes. A canonical, fully replayed skeleton-high sweep is accepted in the realization predecessor slot on a cold dependency gate. |
| **R2-3 — current clearance** | **PARTIAL; R3-2 remains.** | The original three-backtick witness now refuses; source also implements the added indented/quoted/malformed-marker checks. Longer fences and invalid closing-marker lines still turn historical SOUND into clearance while suppressing the current adverse line. |
| **R2-4 — I003 binding** | **CLOSED.** | The exact ratified record is unconditional, must match committed bytes, enters stage identity/memo coverage, and is required by typed governance. Missing, altered, uncommitted, draft, and placeholder cases refuse. |
| **R2-5 — same crossing index** | **CLOSED.** | The original 12→13 counterexample now records nonreproduction; identical indices and adverse-outcome branches follow point 8; the validator rejects flipped results. |
| **R2-6 — committed census** | **CLOSED on the commitment condition.** | Both stability routes enforce committed-equals-working for the corresponding census outputs. The chain contains both commit boundaries. An independent read-only observer also confirmed both census-to-stability boundaries with matching working and HEAD blob digests. This does not clear the distinct cache or semantic-slot defects. |
| **R2-7 — M1 declaration sentinel** | **CLOSED.** | Unconditional exact digest equality and 64-hex validation are restored in M1 and applied in M7. Sentinel/malformed/wrong-digest negatives refuse; the authorized third panel remains unchanged. |

Closures are specific to the repaired obligations and exact bytes. They do not convert the overall M7 disposition into placement clearance.

## 4. Required repairs

### R3-1 — Accepted artifact-directory aliases escape both cache dependency surfaces

**Continues:** R2-1 and R2-2's complete replay-cache requirement; directly answers round-3 disclosures 2 and 3. **Sources:** R:745–756, 1491–1516, 2378–2406; actual readers at R:1039–1043, 1231–1243, 2318–2346; production calls at R:1202 and 2448.

`_readiness_surface_digest` and `_dependency_surface_digest` walk directory trees without following directory symlinks. The record loaders, however, open the per-level artifact paths normally and follow such links. `_manifest_files_digest` covers explicitly named record files and dependencies, not all the implicit raw artifacts consumed by their validators. This creates an accepted read dependency absent from both outer keys.

The counterexample starts from a real temporary repository with a canonical fixture stage and a passing canonical calibration census derived from 48 LevelRecords / 960 kept run records. All manifest entries and explicit dependencies are regular committed files. It moves:

```text
flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/0.250000.skeleton_high.calibration
```

to:

```text
raw_artifact_targets/0.250000.skeleton_high.calibration
```

and leaves a relative directory symlink at the original path. The target stays inside the disposable repository. After this arrangement is committed, fresh readiness and dependency validation accept it. A public production `run_level` control reaches the first-execution sentinel.

The probe then appends one newline, without committing, to:

```text
raw_artifact_targets/0.250000.skeleton_high.calibration/s3655077383.skeleton_high.run.json
```

| Check after that one-byte change | Observed result |
| --- | --- |
| Fresh stage validation | Accepts |
| Readiness surface digest | Unchanged |
| Explicit manifest-file digest | Unchanged |
| Dependency surface digest | Unchanged |
| Authorization/history surface digest | Unchanged |
| Warm readiness | Returns the same cached object with `production_ready=True` |
| Warm shared dependency gate | Accepts |
| Warm public production `run_level` | Reaches `_execute_run`; sentinel stops it before any run |
| Clear only the dependency memo, leaving readiness warm | Rejects: `run record is not in canonical byte form` |
| Clear readiness too | Same rejection |
| Cold public production route | Refuses before execution |

Thus this is not merely a helper mismatch: both caches independently preserve invalid evidence, and the actual direct production path passes their stale results. The altered JSON is deliberately a minimal uncommitted corruption; rejection comes from the real canonical-byte reader. A second reviewer reproduced the result with `_ARTIFACT_REPLAY_MEMO` empty before the initial READY control and again before the post-edit warm calls. The lower artifact replay memo therefore does not explain the stale acceptance. The filesystem demonstration used a Linux directory symlink; Windows reparse variants were not tested.

**Fixture disclosure:** environment conformity and the deterministic lattice stepper are the submitted test stand-ins. The submitted inexpensive known-answer producer is used, and audit records are constructed using the submitted `_fake_audit` helper. The actual audit producer is not patched. No Git, stage, authorization, serialization, census, readiness, artifact-replay, or gate helper is replaced. The probe executes no project scientific job; the final route call is stopped before its first run.

**Repair:** ensure both cache lookups cover every resolved file their validators may read. A coherent repair may reject directory aliases/reparse paths in the relevant path components before any cached success, or include the exact resolved artifact files and path resolution state in the key. Apply the boundary to implicit per-level and benchmark artifacts as well as manifest-named records. Retain the effective relative-path grammar and fresh stage check. This finding does not impose a new commitment rule on every raw artifact.

**Required discriminating regression:** the original valid linked arrangement must either be refused before warming or invalidate both memoized paths after a target edit/deletion. Preserve an ordinary valid directory control, the named dependency-edit negative, missing-pinned-root negative, and authorization-history negative. Test the shared gate with readiness deliberately left warm to prove that its own key is repaired.

**Evidence:** `review_round3/memo/memo_surface_probe.py` and `.jsonl`; the independent repeat is `review_round3/science/memo_surface_independent_probe.py` and `memo_surface_probe.independent.jsonl`.

A separate check found an imprecise first-line parse in `_clean_tracked_set`, but the proposed commit-B/restore-A stale-cache scenario is defeated by HEAD in `_authorization_surface_digest`. It is not counted as a separate demonstrated execution bypass. Its negative result is retained to distinguish a suspected implementation issue from an established blocker.

### R3-2 — Fence parsing still accepts a historical positive over a current adverse disposition

**Continues:** R2-3 / round-1 D8. **Sources:** R:597–611 and 614–624. **Submitted test:** T:593–620.

The parser stores only the first three fence characters and closes whenever a stripped line starts with those characters. It does not retain the opening fence's length or require a syntactically valid closing line. A shorter fence inside a longer quotation therefore closes its internal state prematurely. The real closing fence then opens a new internal block that hides the current adverse disposition.

Here is the exact substantive body of the four-backtick witness; the probe also supplies the exact submitted runner/test digests in its header:

`````text
The following is a historical quotation, not a clearance.

````text
```
FINAL VERDICT: SOUND
````

FINAL VERDICT: DEFECT-WITH-REPAIR
`````

The positive line is wholly inside the four-backtick code quotation. The only current disposition is the adverse column-zero line after it. Nevertheless:

```text
_current_dispositions(text) = ['FINAL VERDICT: SOUND']
verify_placement(...) = ACCEPTED
clearance_committed = True
```

The same result occurs with a four-tilde fence containing a three-tilde line, and with a three-backtick block containing a line beginning with three backticks followed by `example`. All three complete witness documents, exact file digests, and parser/placement returns are included. A genuine current positive control is accepted, and the original simple three-backtick historical quotation is now rejected.

The syntax distinction is defined by [CommonMark 0.31.2 §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks): a closing fence uses the opening character, is at least as long as the opener, and permits only spaces/tabs after the fence. The specification is cited only for Markdown syntax, not as Flight 8 scientific or governance authority.

**Repair:** retain and correctly interpret the opening fence character/length and valid closing-line form, and preserve unambiguous current-disposition checks outside quotations. Alternatively, define a typed clearance field bound to the exact review bytes. Every historical-only positive and every conflicting current disposition must refuse; genuine current positive controls must continue to pass.

**Required discriminating regression:** the three exact witnesses above, their current-positive counterparts, and the already-repaired ordinary fenced/indented/quoted/malformed cases. Check through `verify_placement`, with committed review bytes and source identities, rather than just testing the helper's string output.

**Evidence:** `review_round3/auth/clearance_fence_probe.py`, `.out`, and its five `.md` fixture documents. The placement validator, canonical record checks, and Git checks are unmodified; the suite record is an explicitly synthetic parser input.

### R3-3 — A predecessor sweep is not bound to the object its filename denotes

**Continues:** R2-2's semantic predecessor requirement; implements I003 point 7's existing same-object condition. **Sources:** R:952–970, 2011–2026, 2041, 2398–2406, 2431–2434, 2501–2506, 2560–2565. **Later object check:** R:1924.

`load_record` verifies canonical bytes, schema, type, stage, authorization, and the envelope's producing job. Its `SweepRecord` validator enforces canonical role, the frozen grid, and replay using the body's own `obj`. The dependency gate supplies a prescribed filename/type/job but discards the returned record. Neither that boundary nor `_load_input` binds the named realization output to `obj == "realization"`.

The offline probe takes a private local Git snapshot of the submitted test chain after the realization census is committed. Its correct realization-sweep control first passes fresh readiness and the cold dependency gate. It then substitutes the actual, complete canonical skeleton-high sweep into `realization_sweep.json`, using the valid authorization envelope for `realization_census`, and commits only that replacement in the private clone. The correct realization morphology, canonical calibration census, and all underlying level records remain present. The source fixture is read-only.

| Offline validation after substitution | Observed result |
| --- | --- |
| Named output | `realization_sweep.json` |
| Envelope job | `realization_census` |
| Decoded body object | `skeleton_high` |
| Body role / level count | `canonical` / all 24 frozen levels |
| Unevaluable levels | 0 |
| Working replacement equals its committed Git object | True |
| Fresh production readiness | True |
| Actual sweep replay validator | Accepts |
| Actual realization morphology and calibration validators | Accept |
| `require_job_dependencies("realization_stability", ...)`, dependency memo initially empty | Accepts |

The original realization output has SHA-256 `a40a6a0def1e80f71d03758a8bf16b598b55a6982d826c1f1f9215bbafc29874`. The source skeleton-high output has SHA-256 `eeed4693c6bac6ba9dd9b310dd6aa459aba85d965243081253e28fe589ccb7f5`. The committed replacement realization-slot file has SHA-256 `223259d28c896c4b8f5de9f949cee4f2c1a6f6fe447d715a8be171a80e374924`. The captured output also carries the unchanged morphology and calibration file digests. The probe exits 0 in 218.685 seconds.

This establishes the missing filename-to-object association with full fixture-record replay. The substitution is a deliberate record-input test; it does not show the normal realization census producer writing the wrong object. The canonical role and frozen grid already validate, and the substituted sweep has no unevaluable levels. The repair therefore requires an object association, not a new scientific success criterion or an additional all-levels-evaluable gate.

**Execution boundary:** the offline probe calls no public production entry point. The separate `production_gate_boundary_probe.py` reaches the first-execution sentinel on both public routes for the same wrong-object class, using stage/READY/adapter stand-ins, a real replay-valid 24-level skeleton-high sweep whose missing level records are represented as halts, and stood-in morphology/calibration validators. The full-replay offline case removes those validator stand-ins at the cold shared gate. These are distinct pieces of evidence and are not represented as a full unmodified production execution.

There is an existing later check: `validate_stability_record` requires `canonical_sweep.obj == r.obj`. In the wrapper, however, `levels(obj, "stability")` runs at R:2503 before the comparison record is constructed/persisted at R:2506. That later check can reject the wrong comparison after work has begun; it does not enforce the required predecessor association before execution. No accepted wrong final stability record or complete invalid package is claimed.

**Fixture disclosure:** the offline clone uses the submitted `_ConformingEnv`, `_synthetic_run`, `_fake_known_answer`, `_fake_finite_n_counts`, and `_fake_audit` fixtures, matching the successful-chain test's disclosed environment/numerical producers. Stage, authorization/history, canonical loader, sweep replay, morphology, calibration, readiness, dependency memo/gate, and commitment validators are unmodified. The first attempt exited during Git checkout with status 128 before any validation. Its exact script, output, and status are retained; the completed retry changed only Git error reporting. This setup failure is not an M7 finding.

**Repair:** bind each named `SweepRecord` output to the object denoted by `SWEEP_FILES`, including `realization_sweep.json → "realization"`, before the shared predecessor gate returns or caches success. Use the same association when loading the named input. Preserve envelope, authorization, canonical-role, frozen-grid, replay, and commitment checks. A genuine adverse record for the expected object remains admissible under the existing scientific rules.

**Required discriminating regression:** retain the correct-object control and the original wrong-schema/null-body refusals; reject the complete replay-valid skeleton-high substitution in the realization slot on a cold gate and both public entry routes before their first execution call. Retain the existing synthetic-role and committed-census controls. No new morphology hash field or I003 amendment is required by this witness.

**Evidence:** `review_round3/auth/record_slot_validation_probe.py`, `.out`, and `record_slot_validation_status.json`; the private-snapshot driver is `review_round3/await_slot_snapshot.py`. The separately isolated two-route witness is in `production_gate_boundary_probe.py` and `.out`.


## 5. Closed interpretation and M1 repairs

### 5.1 Ratified I003 identity

R now includes I003 as the seventh `CONTRACT_RECORDS` entry, without conditional membership in `_fixed_records`. Stage derivation verifies its exact hash and committed bytes; the record enters the stage's carried contract identities and memo surface. `F8Governance.interpretation_003_sha256` participates in the typed record identity and must equal the ratified value. [R:117–125, 404–420, 475–516, 636–691.]

The independent probe accepts exact committed bytes and rejects changed-uncommitted, missing-working, changed-committed, missing-committed, and exact-but-uncommitted cases on warm and cold paths. Restoring and committing the authority restores canonical fixture binding. Rehashed governance carrying the draft digest, zero digest, or placeholder refuses. Missing/placeholder contract entries refuse preflight. R2-4 is closed.

The addendum's three drafting observations remain closed: the status sentence identifies the M1 touch; point 2 uses the actual fields and predicates; the `f8_run_spec` citation identifies the pre-touch config. No alias for the superseded draft-only names is required.

### 5.2 Stability reproduction

The same-index rule is now implemented directly at R:1904–1917 and re-derived at R:1920–1927. In the independent probe, both diagnostic sweeps pass the actual M-P1 T-S1′ function. Indices 12 and 13 differ, separation is `0.09782599999999997`, and Δm is `0.120126265992375`; round 3 correctly returns `reproduced=False`. The reverse pair fails reproduction, and identical indices pass.

Fifteen diagnostic cases exercise identical/adjacent located crossings, equal/different adverse outcomes and causes, mixed located/adverse cases, and realization T-R1′ comparisons. Every returned record validates, and every rehashed flipped `reproduced` field refuses. The actual M-P1 test functions are used, not patched return values. These are observation fixtures rather than trajectory claims. R2-5 is closed; separation and Δm remain descriptive, and reproduction remains outside P1.

### 5.3 Committed canonical census

`COMMITTED_DEPENDENCIES` requires skeleton census before skeleton stability and realization census before realization stability. `require_job_dependencies` checks each corresponding output against its committed object, and both public routes call the shared function. The isolated real-Git probe rejects uncommitted outputs, reaches the execution sentinel after those exact outputs are committed, and rejects later uncommitted modifications for both objects on both routes. This isolated control-flow probe retains real Git, authorization and commitment checks on both public routes. It supplies stage, READY and adapter stand-ins and replaces `load_record` with a return stub for the commitment cases. The unmodified chain explicitly refuses the uncommitted skeleton census on both routes before committing it (T:400–407), then refuses the uncommitted realization census before its commit (T:409–412). A separate read-only observer began while neither stability output existed. When `skeleton_stability.json` first appeared at 20:34:58 UTC, both skeleton sweeps and the skeleton assessment each matched their HEAD object. When `realization_stability.json` appeared at 20:41:59 UTC, the realization sweep and morphology each matched their HEAD object. All five full working/committed digests and both stability-file digests are captured in `commit_boundary_observer.jsonl`; the observer exited 0 and performed no job or mutation.

This closes the missing commitment condition itself. It does not certify other contents merely because a file is committed, and it does not override R3-1 or R3-3's missing object association.

### 5.4 M1 touch and declaration identity

M1's declaration equality is unconditional again, preceded by explicit 64-lowercase-hex validation. M7's analogous sentinel exception is removed as well. Independent `PENDING_M7_ROUND2`, `PENDING`, empty, `None`, and wrong-64-hex cases refuse in both modules; exact controls pass. [M1:253–256; R:248–251; T1's added parametrized negatives.]

The established identities recompute:

| Declared quantity | Full SHA-256 |
| --- | --- |
| M1 declaration | `dfd8badf916aaf0a8e040e2ef90fbf23c931053ed3ddff226fe9c9a1c4093f9d` |
| Stability seed panel | `c54f734570a58427c02626e9e031d7848886111e5853ef8a7f9cb0158803c956` |
| M7 declaration | `0ce2e7b5eaca1804b10cc68706380bd93f5efe007c34c7fe74a6eb878cd8b4b8` |

The stability master remains `920261102`; the twenty stability seeds remain the authorized panel. The canonical and calibration panels are unchanged. Relative to round 2, M1 changes only the guard and explanatory comment, with three additional test parameters. The supplied full touch diff remains faithful to both identified placed predecessor files. R2-7 is closed.

## 6. Reporting and carried obligations

The design note now reconciles the requested producer/timing account: realization census emits its sweep and morphology; realization stability evaluates T-R1′ on both sweeps; P1 evaluates T-R1′ again with realization fidelity and the steepest-ascent diagnostic. The contract item-3 reporting is complete when the `p1_evaluation` record is written, regardless of its determination. This is the disclosure requested by the prior review, not a new scientific output. [DN §5; response §3; R:2489–2512; evaluator:387–428, 451–480.]

H1's restricted pass-1 morphology report and explicit open final-set obligation remain as accepted in the ratification addendum. H2's independent panel and the 3,360-run lattice count remain unchanged. The earlier accepted M3 touch retains identical bytes; no M3 repair is requested in this round. The 29-item package proposal, later I002 §9(b)/M6-10 lattice-versus-surrogate obligation, and existing next-edit prose obligations retain their prior dispositions.

Two old design-note phrases can be corrected with the next repair response: the jobs row still names removed `require_dependency_outputs`, and the older memo paragraph still says five memos although §6 discloses the new gate. These are documentation residues, not additional numbered build blockers.

## 7. Return requested from L1

Repair the demonstrated cache and clearance boundaries and the named-sweep object association on identified new bytes, preserve the closed repairs, and return a response by finding with discriminating tests and re-established affected identities. The cache repair must cover both readiness and the shared dependency gate. The clearance repair must classify the actual current disposition. Bind each named sweep to its expected object before predecessor acceptance, preserving valid adverse scientific records and the existing role, grid, replay, authorization, and commitment checks.

The M1 panel does not need redrawing, and I003 does not need editing. Joint placement remains governed by Mike's existing requirement for L2 SOUND on the build and the canonical suite on his machine. This return supplies neither production authorization nor placement.

## Appendix A. Receipt and final submitted-byte check

After the regression run and independent probes completed, and the M7 process interruption was recorded, L2 rehashed the submitted archive and compared every extracted file byte-for-byte with its ZIP entry. **84/84 files remain identical; the submitted payload was not modified.** The outer archive retains SHA-256 `a666a2b385016d3e2c3d1b374dab616e9c4e3e9dbea7d795b4fff98eead5a29a`. The complete receipt table follows; the verification script and its full per-file JSON output are included in the evidence bundle.

Paths are the exact archive paths. For each payload row, MATCH means the full computed SHA-256 shown equals the full MANIFEST.txt value for that path. MANIFEST.txt is separately hashed because it does not self-list.

| # | Archive file | Full computed SHA-256 | Manifest comparison |
| ---: | --- | --- | --- |
| 1 | `MANIFEST.txt` | `fc2710e96266685fc1acaebf379fb4dbbaabb80658b16b9a13323070508c0a85` | SELF-HASH; not self-listed |
| 2 | `flights/mfa_fidelity/build_records/F8_M1_M7_TOUCH_DIFF.txt` | `c880b82e8344843d060f5fa5eb0b32f3353db2b0fad60e14ddaea5bdf90c2a20` | MATCH |
| 3 | `flights/mfa_fidelity/build_records/F8_M3_M7_TOUCH_DIFF.txt` | `be385acfeb5a48def068190fed2e2442805007fe832cde3fdfb1aa373e9df055` | MATCH |
| 4 | `flights/mfa_fidelity/build_records/F8_M3_NULL_VALIDATION_ATTEMPT1_FAILED_2026-10-27.json` | `a95509d3e809d70ba1d8977735ff88868d02ea3ac961305a70886f1128ce28ff` | MATCH |
| 5 | `flights/mfa_fidelity/build_records/F8_M3_NULL_VALIDATION_ATTEMPT2_2026-10-28.json` | `b10a9d5a89e43978a756d704e2e730bb8cba69953f82d03fa52e3e715dc4741e` | MATCH |
| 6 | `flights/mfa_fidelity/build_records/F8_M3_NULL_VALIDATION_PROTOCOL_ATTEMPT2_RATIFIED_2026-10-27.json` | `834a788bd39ee77123260d1023bc29f9343c684725004f36339a0be97ee2bfa4` | MATCH |
| 7 | `flights/mfa_fidelity/build_records/F8_M6_GENERATOR_DECLARATION_v0_3.md` | `c73980585fc238209453ebadb4707d961e41d77b7970435e8ce4113298868e47` | MATCH |
| 8 | `flights/mfa_fidelity/build_records/F8_M7_DESIGN_NOTE_2026-11-02.md` | `3cd03a097c562d8ff51bc2e6f78a5f4ebe99ae0cb7b6b37a601ae3be68472572` | MATCH |
| 9 | `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M7_BUILD_PACKET_2026-11-02.md` | `12b744b3a3875a834082a66bd279ae125952f2c20e939a8e56290ddb5fd55e4f` | MATCH |
| 10 | `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M7_ROUND2_RESPONSE_2026-11-02.md` | `f21892053e5f3093ecd461ec817b2d6f8a160e4feba9486d04c06995cec72317` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M7_ROUND3_RESPONSE_2026-11-03.md` | `d281b3fdebbddd196150330d7e714b79db29a5374e97ec6000b32344ed9017a0` | MATCH |
| 12 | `flights/mfa_fidelity/build_records/L2_F8_M7_ROUND1_REVIEW_2026-11-02_RECEIVED.md` | `c92fc0803f870ba6e76ecb33f9ff8ec38b02b334772317bf1043d24b7a4d2410` | MATCH |
| 13 | `flights/mfa_fidelity/build_records/L2_F8_M7_ROUND2_I003_RATIFICATION_ADDENDUM_2026-11-03_RECEIVED.md` | `ec26e21e82d7e4c9daa605b3abe73e9dc8ae31c6645fc7d731bcacd6307bf55a` | MATCH |
| 14 | `flights/mfa_fidelity/build_records/L2_F8_M7_ROUND2_REVIEW_2026-11-03_RECEIVED.md` | `f5c61978c7f183d7de8ec1af2f602cbc87629f668bf1b43f3571a36c71977e1a` | MATCH |
| 15 | `flights/mfa_fidelity/build_records/f8_m7_module_container_round2_2026-11-02.txt` | `c8313580ed15ff3a8554d57d9a1602f50c2859226999e47711e11b31b2a05424` | MATCH |
| 16 | `flights/mfa_fidelity/build_records/f8_m7_module_container_round3_2026-11-03.txt` | `572e2dff43a2fb67fdb4ef26c776e8bc53e18dc52e81e43b18eac06b9fa15650` | MATCH |
| 17 | `flights/mfa_fidelity/contracts/flight8/APPENDIX_A_OF_RECORD.md` | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` | MATCH |
| 18 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | MATCH |
| 19 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` | MATCH |
| 20 | `flights/mfa_fidelity/contracts/flight8/appendix_a.py` | `bc3e4f05f48e0840eddd5e61b8ea653411e4468900c098e801e5e13506fe0903` | MATCH |
| 21 | `flights/mfa_fidelity/gates/gate_a/GATE_A_AUTHORITATIVE_RECORD.md` | `719a9706f34e6c08119993f1826242939e6a2331fc77cf50a61c769d2710ca74` | MATCH |
| 22 | `flights/mfa_fidelity/gates/gate_b/GATE_B_AUTHORITATIVE_CERTIFICATION_RECORD.md` | `940d88a426d9530449d4c9d93d4a23085d354b678e2229edcf849806f6685883` | MATCH |
| 23 | `flights/mfa_fidelity/gates/gate_r0/GATE_R0_REGISTER_CLOSURE.md` | `59fd2a54a344f994346001eab2ec14b03357018536e3386318138df079e6e741` | MATCH |
| 24 | `flights/mfa_fidelity/governance/e1_stage1/AUTHORIZATION_001.json` | `aa2a05e5ec9cd5da5be4056b363625ec937d6db0caee1db36eae48fa2dcd0ca4` | MATCH |
| 25 | `flights/mfa_fidelity/governance/e1_stage1/AUTHORIZATION_002.json` | `175d37765c537a6b010c8a32d223b99db85c286422f00037e776ea0501f47d9f` | MATCH |
| 26 | `flights/mfa_fidelity/governance/e1_stage1/AUTHORIZATION_003.json` | `846c0e59ef4e47b8103a96bbb1270b3c360cf38b7f325d1353a5332a6b9ef509` | MATCH |
| 27 | `flights/mfa_fidelity/governance/e1_stage1/AUTHORIZATION_004.json` | `071223ce8222e5e45c2b4531cb38cfa4c45eb76b9f2a325f837aab7322183351` | MATCH |
| 28 | `flights/mfa_fidelity/governance/e1_stage1/AUTHORIZATION_REGISTRY.json` | `1223e17bb34c12a6c3c70748ff4a7dc2041d32b92a407c1a251cd741a1d373cf` | MATCH |
| 29 | `flights/mfa_fidelity/governance/e1_stage1/E1R_AMENDMENT.md` | `04058b21d2b1500afe18ee0a1daae54477f9896f9542b0a9e670040867334181` | MATCH |
| 30 | `flights/mfa_fidelity/governance/e1_stage1/E1R_GOVERNANCE.json` | `2e82102c7b6c738216351f0676751385840ba8b3a2a8f3e74d4c80f03e232a2f` | MATCH |
| 31 | `flights/mfa_fidelity/governance/e1_stage1/M7_PLACEMENT_RECORD.json` | `8cdfc320c01bb74b80880b897001e4c87e18b33b20632abe644c45d5e6b5856f` | MATCH |
| 32 | `flights/mfa_fidelity/governance/e1_stage1/M7_SUITE_RECORD.json` | `7d87ef2c7d5d8b898d8a69de967b8865289d33e2b25c78ea0bf5f63fd43231ab` | MATCH |
| 33 | `flights/mfa_fidelity/governance/e1_stage1/PACKAGE_SPECIFICATION.json` | `ed19cb79b3369b6b6a13d6bdae81205fef0ae583e1dacc66407cdd9b18977386` | MATCH |
| 34 | `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_RATIFICATION_RECORD_v1_0.md` | `cdedfcb4540d950be69695b589b3f8cc8b5164278b7d57e850eb7ff8b601346b` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `da0b6e58623c947fd24ef4448469eccf682866514eb46586adcd86b2b1b9f473` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 72 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |
| 73 | `flights/mfa_fidelity/instrument/tests/test_f8_m1.py` | `ca9a547286290aabc497fc228e10dd845711cd1b359bc21fcb125d92e8285007` | MATCH |
| 74 | `flights/mfa_fidelity/instrument/tests/test_f8_m2_m3.py` | `d0d26e75280dffef269e05f95e391b1db775a0f4712a5b3eac2f31ff50336460` | MATCH |
| 75 | `flights/mfa_fidelity/instrument/tests/test_f8_m4.py` | `8b8976b2c3602e0cc3932676cc6a091c69569af515bc183c374208578afa6d12` | MATCH |
| 76 | `flights/mfa_fidelity/instrument/tests/test_f8_m5.py` | `27cb5c965242ad2bde9aa61c5403eb97473190b67b1d232a2d801c5bd2097b41` | MATCH |
| 77 | `flights/mfa_fidelity/instrument/tests/test_f8_m6.py` | `808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca` | MATCH |
| 78 | `flights/mfa_fidelity/instrument/tests/test_f8_m7.py` | `309e063fa24fb1b9457ed0663a12e5fb0f6cfbadc13345569bee8b3c3dbcbf66` | MATCH |
| 79 | `flights/mfa_fidelity/instrument/tests/test_f8_mp1.py` | `f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d` | MATCH |
| 80 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86` | MATCH |
| 81 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md` | `198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034` | MATCH |
| 82 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md` | `6ebf0ad3efbe8e0e74b45e63d5f6ba550441897f3ff6898749230c064c993e9e` | MATCH |
| 83 | `protocols/audit/GEMINI_F8_INTERPRETATION_003_AUDIT_2026-11-03_RECEIVED.md` | `123f4af0bc078922e1a1fc8f024832c0d941fbd42430648c496da1f21708c34b` | MATCH |
| 84 | `protocols/audit/GEMINI_F8_INTERPRETATION_003_AUDIT_TRIAGE_2026-11-03.md` | `1db51a6343071e36e5519ac68bd7279b9ae493507465c71a55ccb75c7819daf5` | MATCH |

## Appendix B. Reproduction and evidence ledger

`L2_F8_M7_ROUND3_EVIDENCE_2026-11-03.zip` contains **47 payloads plus `MANIFEST.txt`, 48 file entries**. The bundle's `README.md` gives runtime/source selection, reproduction commands, and each probe's scope. Temporary fixture paths, commits, and timings vary between executions. The captured outputs identify this execution. No supplied build source, numerical artifact corpus, or dependency installation is included in the evidence ZIP; use the receipted build archive and regenerate fixtures with the supplied tests/probes.

The ledger below hashes all supporting payloads, including the README and captured logs. The final review is omitted from its own internal ledger to avoid a self-hash; it is included in the ZIP manifest. The archive's outer digest and the final review's digest are supplied in the delivery message.

| Evidence file | Bytes | Full SHA-256 |
| --- | ---: | --- |
| `L2_F8_M7_ROUND3_RECEIPT_2026-11-03.md` | 14,656 | `fc3402da509d35c88a93da9e13b60ce5501f7bdba61c90a959aa05f149981453` |
| `README.md` | 8,545 | `17bd7117246d76065f407e426a4105a3745b602e22982f78f29b04e6cddbaa5b` |
| `f8_m7_round3_receipt_verified.json` | 28,181 | `f088f985dbc82bccc455be5ccce42d57b6d95878958e563ec6cb5aa47f6c49f6` |
| `review_round3/auth/clearance_fence_probe.out` | 2,283 | `3f5641a49e5f81ded715ccb91b82750450bc080d14588a3cad1da73e76db0339` |
| `review_round3/auth/clearance_fence_probe.py` | 5,505 | `b5b8b422cd6e8d733a0e3d6d09d9e00972f7255b49408b503d42d46420879f44` |
| `review_round3/auth/control_current_sound.md` | 205 | `4c9606b538bee11043d8719b24fa8c96c19ce8ab7efae722b522374f00b84ce2` |
| `review_round3/auth/four_backticks_shorter_fence_inside.md` | 317 | `562604079960c066cbe3f6f63b9a5c4be4c6f7d3b14cc29fada25ef44bcea099` |
| `review_round3/auth/four_tildes_shorter_fence_inside.md` | 317 | `ff117ace6eb5b2de2586c8a75eccd7a65d69be205f2c44c69dcd98e1141b764b` |
| `review_round3/auth/original_three_backtick_quote.md` | 311 | `2f72c9142ed0decf15cb23a22fc07b5878e391a3e3378a3a06d31b68ad36cf36` |
| `review_round3/auth/production_gate_boundary_probe.out` | 4,558 | `84e7b345b327556fe797757413bd37fc480d089fe1eb60ff2822ecc5a392423b` |
| `review_round3/auth/production_gate_boundary_probe.py` | 9,818 | `0b35031c884cf49350b301bc1d06ac898e3856c8d99f9c8bbb08063828d1036a` |
| `review_round3/auth/record_slot_validation_probe.attempt1.out` | 935 | `b85320a24ae1f98d9ba09b3b8909a151b11af332ae29e86139c042dc4811359f` |
| `review_round3/auth/record_slot_validation_probe.attempt1.py` | 5,700 | `29d63572e84818bf1a6f86660de7ba8e15a4966e5195f57f05421ee4c92291fa` |
| `review_round3/auth/record_slot_validation_probe.out` | 1,371 | `2ed2f7b272765c5ded9d17960674a4bd241b7073e828ed7b4b9794b8a90a3eb8` |
| `review_round3/auth/record_slot_validation_probe.py` | 5,830 | `bd3f4139d2be1e8d75d12d4b8c145c14369e334bbf7746cb39e5fd9ec2cf7ed3` |
| `review_round3/auth/record_slot_validation_status.attempt1.json` | 574 | `a20a13620e50ff5dec916d6b7e1173cb462e3d9a4c8a44665240c4f2785efb49` |
| `review_round3/auth/record_slot_validation_status.json` | 574 | `73ed5f1ec71a24baf091ec9440f82809bcfdeff3bde42ec474398b1dc5c810b1` |
| `review_round3/auth/three_backticks_nonclosing_info_string.md` | 322 | `21a2637cac3f60fc37853a78f178a95606a28ed91fa21206996ebb1bd3fdfef1` |
| `review_round3/await_slot_snapshot.py` | 2,400 | `e5ce0d9be46b0b0960ff446370a4ae994ce83f9ab66fcc70e9f688a2eb5a270e` |
| `review_round3/commit_boundary_observer.jsonl` | 2,209 | `f90c491ce002dcf1e5613f42b9f3232fa053c0c40d3125f078816a196a0dd06e` |
| `review_round3/environment.json` | 452 | `d96e666a87278f58116dc7c893e1a4f5c025954e825305a292351f896cf5513d` |
| `review_round3/frozen_identity_probe.out` | 3,723 | `188d39b97ba4f3ec418e0eb0e5341ebde2c051dc367c8a86e0d7804ba5ba72e9` |
| `review_round3/frozen_identity_probe.py` | 1,907 | `ff2b9012e9be1f02a3f6d95a767c5784c56ee7eba282eeff23c4948bb9940f93` |
| `review_round3/memo/git_clean_key_probe.jsonl` | 248 | `b9d026dac2ff1ab8cafdbdde21f0b27d0d440dee0f19605c0beea99f79592afa` |
| `review_round3/memo/git_clean_key_probe.py` | 2,046 | `c0e69dd1340b02a90608654db6f3d5d5b5fad10bd7baba6a5799300b9c90c034` |
| `review_round3/memo/memo_surface_probe.jsonl` | 4,657 | `a13f305fe88c2ccc874f4c6ca4728395c30600804165a83587e9edf0b56dccc0` |
| `review_round3/memo/memo_surface_probe.py` | 10,963 | `a9a5706533d6b5674c32c2c4578dfbba93d3735a9f6c6084c51aac951990cf90` |
| `review_round3/observe_commit_boundaries.py` | 2,096 | `7393416b8be65f3bc49d470f1a776ce9d8726faae3c51fd2062c28df7e17f12c` |
| `review_round3/post_review_identity_check.json` | 18,427 | `39a3ffc29bd6f26acd2a94e13cd3aaea07c0417f98b9ed54543794fe0cd3791f` |
| `review_round3/post_review_identity_check.py` | 1,146 | `547aa3f9640ae3299c3e8ccc7877ed3f8f1ac86565da605a5b5479448a2190f9` |
| `review_round3/r2_to_r3_changes.json` | 3,388 | `b20777ffef2c33f68375a8426032b45edac22a33c79f0c043757655b91011cb0` |
| `review_round3/r2_to_r3_source.diff` | 52,982 | `5c57c215870f73b829c7822b0caea7b4482e16a46ffbaaa503b6a7c86559f385` |
| `review_round3/run_tests.py` | 1,779 | `a85adda62afeffa884d74770c7a8a60b0d31fb436281e2909d80740880411421` |
| `review_round3/science/i003_binding_probe.out` | 4,458 | `7764919d903d196b99e0ac8351c58ef5bc805f1d10ee652f020f3a75e7fe0754` |
| `review_round3/science/i003_binding_probe.py` | 5,267 | `73334fdb1e93a3ab40b636042dbd3306cc54418116a49106fbf0137bce9fe536` |
| `review_round3/science/memo_surface_independent_probe.py` | 11,525 | `fc12ef219e97f4022f312e42fae5229ac3a22930b18cd9f383ed5a0e7312ec9a` |
| `review_round3/science/memo_surface_probe.independent.jsonl` | 5,111 | `0d4e3cace37cf4c80629bb8505293176d611fc17433b92eb0af9522789e2c8a2` |
| `review_round3/science/stability_comparison_probe.out` | 5,898 | `ecf80a8b1218eff3407918014fc73c2b1a11f23e9f0b5591f624923cb9cf4b6a` |
| `review_round3/science/stability_comparison_probe.py` | 5,031 | `9894ac2150fc604508c5241528466fb7e2266f82c48035abca943aba707b1203` |
| `review_round3/tests/m7_interruption_observation.json` | 949 | `f1929ebdf0274f43761fdf1a6fd8c2dfc40c9e08f355dcaddd65458be372cdad` |
| `review_round3/tests/m7_pytest.log` | 2,149 | `2fd243d49c4d05c9663b777661dbe269198a5d886f9f87d4b95fbddba99bfd60` |
| `review_round3/tests/m7_status.json` | 729 | `fa2c2a8eec9dc512ab5ae9bb3d6c2c522ae96a884e8da20845236b24fa6bea0e` |
| `review_round3/tests/regression_pytest.log` | 25,821 | `b11fa9fc20592e9fe3d9294c1a2b61407cb14ad09b1cfb50b7968f8964e76a83` |
| `review_round3/tests/regression_status.json` | 988 | `f9e4ba3b2775e609ba1fe00a5e4d18d81913fb985dbfb4db0991ecd29ad25ace` |
| `review_round3/verify_m1_touch_diff.out` | 761 | `2a3d754973786d4e05a2eabbadd2e477a3313ce8eadfbd9943b6fe600d441f23` |
| `review_round3/verify_m1_touch_diff.py` | 1,703 | `e68dcd3c6ebbca216f95c3f70607bafc6e3d9e96642a4b5054d2866ed3381c45` |
