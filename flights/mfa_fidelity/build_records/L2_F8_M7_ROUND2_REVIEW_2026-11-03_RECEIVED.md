# L2 — Flight 8 M7 build review, round 2

FINAL VERDICT: DEFECT-WITH-REPAIR

**Review date:** 2026-11-03 (America/New_York). **Submission date:** 2026-11-02. **Register:** module build review, following the verified receipt and Mike's instruction to execute. **Reviewer:** L2. **Decision authority:** Mike. **Declared repository pin:** `ee-theory-lab 2c8827b`; M7 remains unplaced.

**Submission:** `f8_m7_build_round2_L2.zip`, SHA-256 `200e66081a26847f4800ff997db135631559a8459a226387ea6f79439ed9b583`. The archive contains 77 payload files and `MANIFEST.txt`; all 77 payload digests match. Appendix A preserves the complete full-digest receipt.

**Instruction source, read first:** `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M7_ROUND2_RESPONSE_2026-11-02.md`, SHA-256 `f21892053e5f3093ecd461ec817b2d6f8a160e4feba9486d04c06995cec72317`. **Read second:** `flights/mfa_fidelity/rulings/F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md`, SHA-256 `822ad8d88ad093c906fe1a8d74cc802fecc5799b5b132594054b96997b7d6187`.

## 1. Disposition

**M7 and the submitted M1 touch are not cleared for placement.** Round 2 repairs most of the round-1 findings, supplies the missing gate records, and substantially improves the integration coverage. Seven concrete repair items remain. Three continue round-1 defects—D1(b), D3(b), and D8—and four concern the implementation or identity binding of Interpretation 003 and the M1 touch.

Mike's **H1(a), H2(a), and a′ decisions are treated as authority**. This review does not reopen the choice of restricted morphology reporting, an independent stability panel, or the disclosed M1 change needed to implement that panel. It checks the submitted implementation against those choices and the identified ruling. No new scientific passage condition is imposed on skeleton results or stability reproduction.

| Repair | Round-1/ruling relationship | Confirmed remaining problem |
| --- | --- | --- |
| R2-1 | D1(b), M7-8 | An accepted prerequisite dependency can lie outside the tree hashed by the readiness memo. Editing that dependency leaves warm READY intact while cold validation refuses. |
| R2-2 | D3(b), disclosure 3 | Public production `run_level` accepts predecessor envelopes with `record: null`, even with a wrong schema identity, and reaches the first execution call. |
| R2-3 | D8 | A historical positive verdict inside a Markdown code quotation can still be accepted as current L2 clearance. |
| R2-4 | Interpretation 003 identity | The submitted placeholder excludes the relied-upon ruling from the bound surface. Missing, exact, and arbitrarily altered ruling files yield the same canonical fixture stage identity. |
| R2-5 | H2 / I003 point 8 | Skeleton stability uses separation ≤ Δm, although the submitted ruling requires the same crossing-interval index. Adjacent different indices are accepted as reproduced. |
| R2-6 | H2 / I003 point 7 | Stability can start before its corresponding canonical census is committed. Neither production entry point enforces this requirement. |
| R2-7 | M1 touch a′ | A newly added `PENDING` exception bypasses M1's previously unconditional declaration-digest equality check. |

The repaired M3 touch remains acceptable. The revised 29-item package proposal is internally complete, and the 3,360 lattice-run count is correct for the five implemented lattice jobs. Those findings are component dispositions; they do not override the remaining execution and identity defects.

This is a build review. Its test repositories, synthetic records, reduced runs, and replay probes are build evidence. It grants no production authorization and certifies no canonical Gate-B suite or scientific outcome.

## 2. Evidence and verification record

### 2.1 Source references

References below identify the exact submitted bytes. Paths in this table are relative to `flights/mfa_fidelity/`. Function names and occasional one-based line positions locate the relevant implementation; Appendix A supplies every payload digest.

| Reference | Source | SHA-256 |
| --- | --- | --- |
| R | `instrument/mfa_instrument/f8/runner.py` | `9d8b8378efb51ac403acf746dbe0640205f6a9bbfe2edc7436d40d7769df332b` |
| T | `instrument/tests/test_f8_m7.py` | `cfe308bb99f2c6f539e091e26d6524f54c1bdf71619e179a6af6d9dcd73dc725` |
| M1 | `instrument/mfa_instrument/f8/config.py` | `f8b25fafb619c849ce229476ea860d8661012710c1933fde459f54d6486f471e` |
| T1 | `instrument/tests/test_f8_m1.py` | `857a1403f603b51bd2eea7ff5480fe5b89ef3b5d8de9c213f9b145540a393d20` |
| C | `contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` |
| RAT | `governance/f8_stage1/F8_STAGE1_RATIFICATION_RECORD_v1_0.md` | `cdedfcb4540d950be69695b589b3f8cc8b5164278b7d57e850eb7ff8b601346b` |
| I003 | `rulings/F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md` | `822ad8d88ad093c906fe1a8d74cc802fecc5799b5b132594054b96997b7d6187` |
| R1 | `build_records/L2_F8_M7_ROUND1_REVIEW_2026-11-02_RECEIVED.md` | `c92fc0803f870ba6e76ecb33f9ff8ec38b02b334772317bf1043d24b7a4d2410` |
| E1 | `instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` |

The received round-1 review is byte-identical to L2's delivered review. Comparing the two archives finds five changed common files: R, T, M1, T1, and the design note. Twelve payloads were added, including the three omitted gate records, the generator/attempt records, the received review, and I003. The earlier container log was replaced by the round-2 log. The submitted M3 file is unchanged from round 1.

The supplied M1 diff reproduces both changed M1 files byte-for-byte when applied to their exact round-1 predecessors. The previous config digest was `43ea8de23c0d718b246936c7ff6f18e4f8e5243f77ddb240d896e5d00bdf0e07`; the previous M1-test digest was `23d4260f5a2d996b56e748aada1e7ed5d5b6d35e57bc41be9fdc53b34b04bff0`. This confirms disclosure completeness; it does not make every disclosed change acceptable.

Repository history at the real declared pin was not independently cloned or certified. Git-dependent probes use explicitly temporary repositories populated from the submitted bytes. The user-supplied packet and its committed-record copies are the review authority; no unrelated project material enters this review.

### 2.2 Local test record

| Local verification | Observed result | Process exit |
| --- | --- | --- |
| Full submitted M7 module | **32 passed in 4790.54s (1:19:50)** | 0 |
| Touched M1 module | **70 passed in 4.49s** | 0 |
| M2/M3, M4, M5, M-P1, and M6 regression against the touched config/M3 | **171 passed in 955.23s (0:15:55)** | 0 |
| Independent diagnostic probes | All completed; positive controls and the seven repair findings are documented below | 0 for each probe |

The M7 invocation was `python -m pytest tests/test_f8_m7.py -vv -p no:cacheprovider --durations=12 --tb=short`. The M1 invocation used `tests/test_f8_m1.py -vv -p no:cacheprovider -o faulthandler_timeout=60 --tb=short --durations=6`. The regression invocation named `tests/test_f8_m2_m3.py tests/test_f8_m4.py tests/test_f8_m5.py tests/test_f8_mp1.py tests/test_f8_m6.py` with `-vv -p no:cacheprovider --durations=8 --tb=short`. All ran from the submitted instrument directory, using the primary Python interpreter and isolated review dependencies.

The full M7 chain is a structural integration test at production shape. As disclosed in T and the response, it replaces M1's lattice stepper, M6's audit producer, the known-answer producer, and M5's finite-N projection process with consistent fixtures. The M6 pricing producer and its replay run through the real implementation with 10,000 replicates. Passing this chain establishes the exercised mechanics. It does not establish production qualification or rule out counterexamples outside the exercised tests.

The local environment is CPython 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pytest 9.2.0, and PyArrow 26.0.0, on Linux with glibc 2.39. Review dependencies were isolated on `PYTHONPATH`. This environment is not presented as the canonical Gate-B-qualified machine.

The response's repeated M1 count of 69 requires a prose correction: the submitted T1 contains an additional parametrized stability-digest negative, and the local result is 70. This is an evidence-description correction, not a failed test.

### 2.3 Probe boundaries

The review used focused probes in addition to the submitted tests. Actual functions under review were retained. Expensive scientific producers or unrelated entry prerequisites were replaced only where needed to isolate a guard, with the substitutions described below.

The readiness counterexample uses real Git, stage binding, file identities, authorization history, canonical envelopes, manifest validation, and readiness derivation. Numerical qualification and census records are explicitly test fixtures. The direct-route counterexample uses real committed authorization/registry checks; stage validity, adapter validity, and an already-READY result are boundary stand-ins. It stops at the first execution sentinel. The placement-parser probe uses unmodified placement validation and actual Git with a synthetic suite record as parser input. The I003 binding probe uses the submitted stage fixture with only environmental conformity stood in.

The stability-comparison probe supplies diagnostic sweeps and calls the actual comparison and validator; it makes no trajectory claim. The isolated commitment probe stands in for scientific record validation to isolate the missing Git check; the submitted chain independently corroborates the missing commit boundary. The M1 sentinel probe changes one in-memory digest literal and leaves submitted files intact. Evidence hashes are recorded in Appendix B.

## 3. Round-1 disposition by subitem

“Closed” below closes the named defect on this submission. Dependencies on remaining repairs are stated explicitly; closure is not overall placement clearance.

| Item | Round-2 disposition | Basis |
| --- | --- | --- |
| V1 | **CLOSED** | Gate A, Gate B, and Gate R0 records are supplied at the exact three required identities. The earlier missing-file barrier is removed. |
| D1(a) | **CLOSED** | The placement-named clearance file is in the stage surface; fresh environment facts enter the memo key. Warm and cold probes agree after clearance edit/deletion, pinned-root loss, and conformity change. |
| D1(b) | **PARTIAL — R2-1 remains** | The original authorization-v1 rewrite/restore history case now refuses on both paths. An external prerequisite dependency remains outside the readiness key. |
| D1(c) | **CLOSED** | Adapter key includes its stored body checksum. Valid/bad/valid gives true/false/true; bad/valid/bad gives false/true/false. |
| D2 | **CLOSED** | One exact job/object/panel mapping governs execution and persisted levels. An independently specified seven-combination allow-list rejects all 53 other combinations before execution. |
| D3(a) | **CLOSED on the prerequisite grammar** | Known-answer passage, M6 qualification passage, and calibration-census passage are mandatory. Missing or weakened job-0 passage is rejected; ceiling failure cannot satisfy that requirement. R2-1 remains a separate cache defect. |
| D3(b) | **PARTIAL — R2-2 remains** | The job route semantically validates predecessors, including assessment and stability. The public direct production route still does not. |
| D3(c) | **CLOSED on assessment production** | Job 1 now issues and replays `SkeletonAssessment` with T-S1′, T-S1c, T-S2, boundary diagnostics, and skeleton fidelity rows before returning. R2-2 still weakens its enforcement on the direct route. |
| D3(d) | **CLOSED on job-route order** | Design requires the known-answer output; held-out requires design. These are loaded and validated before the audit execution call. |
| D4(a) | **CLOSED** | Execution metadata is derived from the spec and trace with exact-type checks. Genuine reduced-run controls pass; independent −17/−23/42 substitutions and integer-valued floats fail in ordinary and re-execution validation. |
| D4(b) | **CLOSED** | Run JSON must have canonical bytes and decode as exact `RunProvenance`; equivalent pretty JSON is rejected. |
| D4(c) | **CLOSED** | Both morphology and the level loader apply the shared `(mode, level, object, panel, job)` slot check. The original one-record-copied-to-24-slots example fails at the second slot. |
| D5(a) | **CLOSED** | The full 29-item specification contains the projection ensemble, validates as a whole, maps to distinct files, and separates design/held-out producers. Removing the ensemble is rejected. |
| D5(b) | **CLOSED** | A distinct `ToleranceEnsembles` collection retains all 24 M5 records and is separately persisted, encoded, replayed, and packaged beside the program. |
| D6 | **CLOSED on the identified validator defect** | Pricing now checks the declared experiment, count domains, source and declaration, arithmetic, and full deterministic replay. Metadata/count counterexamples are refused. See the local integration result in §2.2. |
| D7 | **CLOSED for the original bindings** | Generator Markdown and all attempt/protocol files are fixed by identity. The decision derives from the records; the wrong Markdown hash, reversed default-alpha passage, and recast attempt 1 are refused. R2-4 is the distinct new ruling-binding issue. |
| D8 | **PARTIAL — R2-3 remains** | Exact adverse/duplicate/bare-word cases now refuse, but multiline quoted positive markers still grant clearance. |

The MDD prerequisite and early skeleton assessment do not require a favorable scientific result before realization. The distinction remains between completing the required evidence and obtaining an outcome that supports a scientific proposition. Similarly, a failed stability reproduction is recorded under I003 rather than becoming an invented P1 branch stop.

## 4. Required repairs

### R2-1 — Readiness still caches an incomplete prerequisite dependency surface

**Relationship:** D1(b), M7-8. **Sources:** R `validate_prerequisite_manifest` at 1445; `_readiness_surface_digest` at 727; `validate_prerequisites` at 1466; `_prereq_context` at 1477.

The new authority-history surface repairs the original example. Rewriting authorization v1, committing it, restoring its original bytes, and committing again now makes both warm and cold readiness reject the three-commit version history. That repair is accepted.

A different legal path through the submitted manifest validator still escapes the cache. The main prerequisite `e.file` must be relative. A dependency path `d[1]` is checked for `..`, role, and digest, but not for being absolute. An absolute audit dependency inside the repository therefore passes. `os.path.join(base, rel)` resolves to that absolute path, and `_require_committed` accepts it when its bytes match Git. Yet `_readiness_surface_digest` only hashes the prerequisites subtree.

The diagnostic manifest places the design and held-out audit dependencies under a separate directory inside the same repository. Initial readiness validates and is cached. Appending a newline to the design record without committing then gives:

```text
initial_ready = True
stage_still_valid = True
prerequisite_surface_unchanged = True
authority_surface_unchanged = True
warm_ready = True
warm_same_object = True
cold = RunnerDomainError:
       prerequisite m6_audit_qualification dependency design absent or not the named identity
```

The ordinary stage validation still passes, so this case is not contained by the job entry's separate stage check. The cache can preserve READY after a qualification input ceases to match the committed manifest. The probe establishes that validation failure; it does not execute scientific work.

**Required repair:** enforce a complete dependency boundary before memo use. Either require all dependency paths to be relative and resolve within the declared prerequisite tree, or key readiness on the complete resolved dependency graph and its identity/commitment facts. Account for the target platform's path rules. Adding HEAD alone cannot detect this uncommitted mutation.

**Discriminating test:** accept a valid first call, then edit/delete the dependency or change its commitment state. An external dependency must either have been refused initially or invalidate readiness equally on warm and cold paths. Preserve the repaired authorization-history negative.

A secondary direct-API discrepancy also remains: warming readiness with the correct pinned root, then calling it with a missing pinned root, can return cached READY while cold validation rejects the stage role. Normal production entry points separately validate the stage, so that secondary case is not claimed as a production bypass. Validating fresh stage prerequisites before returning cached readiness is a coherent way to close both API and dependency inconsistencies.

### R2-2 — The direct production route does not establish predecessor evidence

**Relationship:** D3(b), response disclosure 3. **Sources:** R `require_dependency_outputs` at 2309; `require_job_dependencies` at 2324; `run_level` at 1160; `run_canonical_job` at 2363.

The new job route performs semantic predecessor validation. The direct route checks only canonical envelope bytes, advertised type/job/stage, and a committed authorization binding. It does not check the schema identity, decode the body, or invoke the predecessor validator. Authorization to produce a record does not establish that the record was produced.

The probe creates all six envelopes needed before realization, bound to a genuine committed authorization, but sets every body to `null`. With both a wrong schema and the correct schema, the direct guard accepts and public production `run_level` reaches its first `_execute_run` call. The probe stops there.

```text
bad schema + null bodies:
  envelope guard accepts
  public run_level reaches first execution
  job guard refuses: persisted record schema differs from the current schema

correct schema + null bodies:
  envelope guard accepts
  public run_level reaches first execution
  job guard refuses: decoded record type mismatch
```

Disclosure 3 acknowledges a weaker direct check but does not make it adequate. The accepted bodies need not even be well-formed predecessor records. Its defense that the job route alone produces canonical outputs is also too broad: `run_level` itself calls `_persist_canonical` for a production `LevelRecord` at R 1204. The wrapper skips existing level files at R 2378 and can consume direct-route records later. Later validation cannot undo a run taken before the required evidence existed.

**Required repair:** give every public production entry point the same semantic prerequisite gate, or remove direct public production execution and have a controlled internal routine consume a freshly validated dependency context. Adding schema/type checks alone is insufficient because correctly typed but invalid assessments could still pass. Any replay cache must cover the full dependency surface.

**Discriminating test:** for both entry points, supply wrong-schema envelopes, null bodies, and correctly typed but invalid skeleton-assessment/stability records. All must refuse before the first execution sentinel. A valid predecessor set must still permit execution. Negative scientific outcomes remain valid records where the contract permits them; no new favorable-outcome gate is requested.

### R2-3 — A historical code quotation still grants L2 clearance

**Relationship:** D8. **Source:** R `verify_placement`, especially the line parser at 607.

The exact-marker change repairs the original `SOUND withheld` substring failure. It also rejects duplicate markers, a bare SOUND, and a sole decorated marker. But the parser applies `strip()` to every line without tracking Markdown code quotations. A positive marker inside a fenced or indented example can become the sole selected marker.

With real temporary Git history, unchanged submitted runner/test bytes, and committed placement/parser fixtures, unmodified `verify_placement` accepts a document that explicitly describes the positive marker as an earlier quotation and states the current disposition is adverse:

````text
This is a quotation of an earlier decision, not a clearance for these submitted bytes.

```text
FINAL VERDICT: SOUND
```

The current disposition is DEFECT-WITH-REPAIR.
````

The same failure occurs with a bold current adverse field, and with an indented positive code example accompanied by explicit no-clearance prose. There is no current authoritative positive field outside the quoted material. This is within the round-1 requirement to reject quoted earlier verdicts.

**Required repair:** define and parse one unambiguous current disposition outside quoted, fenced, or indented code material, and fail closed on missing, malformed, or conflicting dispositions. A typed clearance field bound to the exact review bytes is another coherent design. Preserve source identities, commitment checks, and the prohibition on substring matching.

**Discriminating test:** keep the repaired negatives and the single genuine current-positive control; add fenced historical positives, indented examples, and quoted positives combined with a current adverse/malformed field. Every historical-only positive must refuse.

### R2-4 — The canonical stage can omit Interpretation 003 entirely

**Relationship:** H1/H2 implementation authority and identity. **Sources:** R `INTERPRETATION_003_SHA256` at 126; `_fixed_records` at 475; `_derive_stage`; T `_base_repo`.

The submitted literal is `PLACEHOLDER_UNTIL_RATIFIED`. `_fixed_records` silently leaves I003 out while the literal contains `PLACEHOLDER`. The stage can become canonical without the ruling that supplies its restricted morphology semantics and independent stability panel. T's canonical fixture copies `_fixed_records`, so it also omits I003.

Using the actual supplied stage/placement/governance helpers, real Git, real adapter construction, and only the supplied environmental-conformity stand-in, the probe observes:

| I003 on disk | Result |
| --- | --- |
| Absent | Canonical stage binds; ruling absent from fixed records. |
| Exact submitted bytes added | Canonical stage; identical stage identity. |
| Replaced with arbitrary text; stage memo cleared | Canonical stage; identical stage identity. |

This is a dependency omitted by the derivation itself, not merely stale caching. The shared stage identity in this fixture was `20df6b14ae00362669a38ad5d57a9fc207fad429adc3e4b28a0bb57eb682ada1`.

**Required repair:** bind the exact finalized I003 identity in the stage surface and require its committed bytes before canonical role or acts depending on it. An unfilled or malformed identity must fail closed. If technical wording is finalized as part of the repair, use the resulting exact file digest and re-establish affected runner/declaration identities through the ordinary review path.

The response's “once ratified” wording and the blank final ratification line should be reconciled with Mike's supplied decisions. They do not justify allowing canonical use without the identified ruling. No repeat decision on H1(a), H2(a), or a′ is requested here.

**Discriminating test:** missing, changed, uncommitted, and placeholder ruling identities must refuse on both warm and cold paths. Exact committed ruling bytes must bind and appear in the carried stage identity surface.

### R2-5 — Skeleton stability uses a wider rule than the identified interpretation

**Relationship:** H2, I003 point 8. **Sources:** R `_stability_from` at 1859, especially 1865; `validate_stability_record` at 1875; I003 part 2.

I003 defines reproduction as the same crossing-interval index, or matching adverse outcome/cause when no crossing is available. R still accepts any two located crossings whose separation is at most Δm. Its docstring treats those criteria as equivalent, but they differ on this grid.

The actual comparison and validator accept the following diagnostic pair:

| Quantity | Observed value |
| --- | --- |
| Canonical crossing index | 12 |
| Stability crossing index | 13 |
| Separation | 0.09782599999999997 |
| Appendix-A Δm | 0.120126265992375 |
| Returned `reproduced` | `True` |

Both sweeps individually pass T-S1′; their indices differ. The validator repeats the same wider derivation and therefore accepts the incorrect reproduction claim. No lattice trajectory is asserted by this fixture.

**Required repair:** implement exact crossing-index equality when both crossings exist, retaining the declared matching-adverse-outcome branch. Separation and Δm may remain descriptive fields. Do not silently substitute the older tolerance rule for the submitted point-8 criterion.

**Discriminating test:** identical index passes; adjacent indices in either direction fail; equal and unequal adverse outcomes/causes follow the declared rule. Test the validator as well as the producer. A failed reproduction is recorded and does not enter P1.

### R2-6 — Stability does not wait for committed canonical census evidence

**Relationship:** H2, I003 point 7. **Sources:** R `require_job_dependencies`, `require_dependency_outputs`, and `load_record`; T's chain after authorization v3.

I003 requires each stability job to follow the corresponding canonical census **committed**. R validates authorized predecessor files but does not require those output files to equal committed Git objects. Committing the authorization is a different requirement from committing the evidence it authorizes.

The submitted chain produces the skeleton census, then skeleton stability, realization census, and realization stability without an intervening commit. It therefore exercises a weaker order than point 7. An isolated real-Git control-flow probe also creates the expected predecessor filenames as untracked outputs, substitutes the expensive scientific validators, and confirms the actual dependency guard returns. That isolated probe establishes the absent commitment check; it does not claim its placeholder contents are scientific evidence.


A read-only observer of the actual submitted chain also captured both stability outputs immediately after their production. At those moments, all three skeleton-census outputs and both realization-census outputs were absent from HEAD and untracked, respectively. This supplies direct integration corroboration beyond the isolated guard probe. The observer did not alter the fixture repository or execute any job. Its timestamped file identities and Git results are in the evidence ledger.

**Required repair:** before either stability entry point executes, require the corresponding canonical census output records to match committed bytes, while retaining their full provenance and dependency validation. Apply the same check on the job and direct-level routes. The condition is committed completion, not a favorable skeleton or realization result. This finding does not prescribe a new storage policy for every raw artifact.

**Discriminating test:** valid but uncommitted census evidence must refuse before the first stability execution sentinel. Committing those exact bytes must permit the same call. Later uncommitted modification must refuse. Update the successful chain to exercise the required commit boundaries.

### R2-7 — The M1 touch weakens its frozen-identity preflight

**Relationship:** disclosed M1 touch a′. **Source:** M1 `verify_frozen_identity` at 253; supplied `F8_M1_M7_TOUCH_DIFF.txt`.

The original M1 declaration digest check was unconditional. The touch adds a condition that skips it whenever the literal contains `PENDING`:

```python
if "PENDING" not in F8_DECLARATION_SHA256_LITERAL and frozen_digest(F8_DECLARATION) != F8_DECLARATION_SHA256_LITERAL:
    raise F8ConfigError(...)
```

The submission already has an established full declaration digest, so this exception is unnecessary for the third-panel implementation. Changing only the in-memory digest literal to `PENDING` makes M1 preflight return that sentinel as its declaration identity and permits construction of a production-shape stability run spec.

This is a regression in M1's own frozen-identity invariant. It is not claimed to bypass every later M7 source/governance identity check. The change is visible in the supplied diff, but it is unrelated to the authorized panel addition and should not be carried into the placed module.

**Required repair:** restore unconditional equality, reject malformed/sentinel digests, and retain the valid panel addition and its established declaration. Add a `PENDING`-containing negative alongside the existing wrong-digest test. Recompute only identities affected by the corrected source; no master redraw or scientific-rule change is needed.

## 5. Mike's dispositions and the M1 touch

### 5.1 H1(a): restricted morphology reporting

The implemented scientific scope now conforms to the selected restriction. `MorphologyRecord` always says `pass-1 level set`. The no-insertion case has `final_set_identical_to_pass1=True` and `final_set_obligation="discharged_identically"`. When the router requests insertions, every insertion receives its halt, the identity flag is false, and the obligation is `"open"`. The eight-insertion round-1 witness now carries eight halts and the open obligation. It can satisfy restricted-report completeness without claiming final-set completion. The final-set-identity predicate is false in that case. These are the intended distinct facts. [R `MorphologyRecord`, `_morphology_from_rows`, `validate_morphology`, and morphology predicates; I003 points 1–5.]

The P1 evaluator remains separate. Morphology completion or agreement with the expected rule-2 result does not alter P1. R2-4 remains necessary to bind the identified authority for this reporting restriction.

There are minor schema/prose alignments: I003 also names `insertions_evaluable`, whereas the implementation exposes the equivalent boolean through `final_set_identical_to_pass1`; the final-set obligation is carried by the hash-bound morphology package item rather than a separate top-level package field. These do not lose the scientific limitation or create another decision hold. Add the promised alias/field or align the technical wording while preserving the decision and the eventual exact identified bytes.

### 5.2 H2(a), executed as a′: independent stability panel

The third-panel design is consistent with the authorized data-role correction. M1 declares twenty hardcoded seeds from master **920261102**, regenerated by its established seed-panel rule and checked for disjointness from canonical, calibration, and retired E1 panels. Production-shaped stability specs restrict seeds and objects to the declared panel and `skeleton_high`/`realization`. Canonical and calibration panel values are unchanged. [M1 declaration, preflight, and `f8_run_spec`; I003 point 6.]

The panel SHA-256 is `c54f734570a58427c02626e9e031d7848886111e5853ef8a7f9cb0158803c956`; the new M1 declaration digest is `dfd8badf916aaf0a8e040e2ef90fbf23c931053ed3ddff226fe9c9a1c4093f9d`. Both recompute. The two stability jobs have their own authorization mapping and readiness gate. `StabilitySweep` preserves the panel, master, level identities, and run provenance; its internal M-P1 sweep uses the supported `synthetic` role and is replayed from the stability LevelRecords. It does not enter P1. [R `JOB_OBJECTS`, `StabilitySweep`, `_stability_sweep_from_records`, and `validate_stability_sweep`.]

Calibration runs are no longer converted into scored stability sweeps: `_sweep_from_level_records` explicitly rejects the calibration panel. Using the calibration census's bands for T-R1′ remains permitted by I003 point 8; it is not the prohibited reuse of calibration trajectories as the alternate scored sweep. The round-1 data-role defect is repaired. The remaining H2 implementation work is R2-4, R2-5, R2-6, and the M1 preflight repair R2-7.

I003's early statement that no placed module changes conflicts with its later specific a′ paragraph. Mike's explicit a′ authorization and the later specific text establish the intended scope. Correct the early sentence during final identification; this does not require a new ruling on whether the touch is authorized.

## 6. Declarations, package completion, and carried obligations

| Declaration | L2 round-2 disposition |
| --- | --- |
| M7-1 — run-artifact grammar | The D4 repairs are accepted: typed execution metadata, canonical run bytes, correct slots, and replay. Overall use remains subject to the execution guards above. |
| M7-2 — job graph | The five lattice jobs and exact mappings are coherent; the early skeleton assessment and ordinary qualification order are repaired. R2-2 and R2-6 prevent full acceptance of execution sequencing. |
| M7-3 — package items | The revised **29-item proposal** is internally complete. The projection ensemble is a real dependency; all 24 tolerance ensembles remain separately retained from the program; held-out and design audits resolve to distinct producers. Mike's exact final specification remains a governance record. |
| M7-4 — morphology scope | Accepted under H1(a), with the explicit open final-set obligation where needed, subject to binding I003. |
| M7-5 — stability reading | Independent-panel data role accepted; same-index and commitment implementation require R2-5 and R2-6. |
| M7-6 — tranche/benchmark | Existing tranche and benchmark panels retained. **3,360** is the correct stated lattice-work count after adding two 480-run stability sweeps. |
| M7-7 — M3 touch | Prior acceptance stands. The submitted M3 bytes equal round 1; the two disclosed obligation repairs, declaration identity, and attempt-2 protocol identity remain as reviewed. |
| M7-8 — memos | Stage and adapter repairs accepted on the identified cases; readiness remains open under R2-1. |
| M7-9 — I003 / independent panel | Mike's decisions acknowledged. Implementation and identity repairs R2-4 through R2-7 remain before clearance. |

The 3,360 count is 960 job-0 runs + 960 skeleton-census runs + 480 realization-census runs + 480 skeleton-stability runs + 480 realization-stability runs. At 1.3 seconds per run, a 960-run job is 20.8 minutes. This is a lattice-work projection, not a total price for the audit, projection, replay, and package machinery. The round-1 arithmetic correction is accepted. [R `PRODUCTION_RUNS`, benchmark projection; response §3; I003 point 10.]

The tolerance collection was independently round-tripped and replayed, with missing, duplicate, reordered, wrong-level, and altered-statistic variants refused after recomputing their digests. This closes the lost-record-kind defect without touching M5. The complete specification maps its 29 items to distinct files. The whole-chain result in §2.2 supplies the integration evidence beyond these isolated checks.

The following obligations remain visible without becoming new scientific gates:

- I002 §9(b) / M6-10's later lattice-versus-surrogate comparison is explicitly carried by the revised design note; it is not converted here into an M7 output.
- RAT §E.8's stale comments in the unchanged M6 and M-P1 test modules remain due at their next edits.
- C §7.3 item 3 assigns T-R1′, steepest-ascent, and realization fidelity reporting to the realization census. The current branch emits a sweep and morphology; T-R1′ appears later in realization stability, and full fidelity later in P1. The final pipeline contains those results. Reconcile the named producer/timing in the design record; this review does not invent absent final scientific content or add it to the seven established blocking repairs.
- The new skeleton fidelity rows match the placed M-P1 convention: realization-side ŝ supplies the fidelity band, while skeleton-specific variance serves its designated evaluability tests. No reopening of that placed convention is warranted.

## 7. Return for the next round

Repair R2-1 through R2-7, retain the closed protections and the authorized H1/H2 semantics, and submit the changed files with exact identities and a response by repair item. Tests should exercise the failed boundaries themselves: warm/cold dependency changes, both production entry points, quoted clearance text, mandatory ruling identity, adjacent crossing indices, uncommitted census evidence, and the M1 sentinel digest.

The successful integration chain must include the commitment boundaries that the ruling actually requires. Source and declaration identities must be re-established on the final submitted bytes. Mike's canonical suite/placement requirements continue to apply after L2's future SOUND; this round supplies no such clearance.

## Appendix A. Full receipt and post-review byte verification

| Receipt fact | Result |
| --- | --- |
| Archive | `f8_m7_build_round2_L2.zip`; 562,769 bytes |
| Declared archive SHA-256 | `200e66081a26847f4800ff997db135631559a8459a226387ea6f79439ed9b583` |
| Computed archive SHA-256 | `200e66081a26847f4800ff997db135631559a8459a226387ea6f79439ed9b583` — MATCH |
| Count | 77 payload files + MANIFEST.txt = 78 regular file entries; zero directories |
| Manifest | 77 well-formed rows; 77/77 payload SHA-256 values match |
| Integrity | No missing, unlisted, duplicate, unsafe, or nonregular entries; all ZIP CRC checks pass |
| MANIFEST.txt SHA-256 | `1218074423255433df519478a27b393346c416351527703e437ecb6eb095eac6`; separately computed, not self-listed |
| Post-review verification | All 78 extracted files still equal the receipted bytes |
| Repository pin | ee-theory-lab 2c8827b, declared; real HEAD not independently certified |

Payload paths below are relative to `flights/mfa_fidelity/`; `MANIFEST.txt` is at the archive root. MATCH means the full computed digest equals the manifest digest for that exact path.

| # | File | Full computed SHA-256 | Manifest comparison |
| ---: | --- | --- | --- |
| 1 | `MANIFEST.txt` | `1218074423255433df519478a27b393346c416351527703e437ecb6eb095eac6` | Self-hash; not self-listed |
| 2 | `build_records/F8_M1_M7_TOUCH_DIFF.txt` | `ff85aee402994361d9b8c24796dc7dbe80910abe7e2e6b571df38600a24cf83c` | MATCH |
| 3 | `build_records/F8_M3_M7_TOUCH_DIFF.txt` | `be385acfeb5a48def068190fed2e2442805007fe832cde3fdfb1aa373e9df055` | MATCH |
| 4 | `build_records/F8_M3_NULL_VALIDATION_ATTEMPT1_FAILED_2026-10-27.json` | `a95509d3e809d70ba1d8977735ff88868d02ea3ac961305a70886f1128ce28ff` | MATCH |
| 5 | `build_records/F8_M3_NULL_VALIDATION_ATTEMPT2_2026-10-28.json` | `b10a9d5a89e43978a756d704e2e730bb8cba69953f82d03fa52e3e715dc4741e` | MATCH |
| 6 | `build_records/F8_M3_NULL_VALIDATION_PROTOCOL_ATTEMPT2_RATIFIED_2026-10-27.json` | `834a788bd39ee77123260d1023bc29f9343c684725004f36339a0be97ee2bfa4` | MATCH |
| 7 | `build_records/F8_M6_GENERATOR_DECLARATION_v0_3.md` | `c73980585fc238209453ebadb4707d961e41d77b7970435e8ce4113298868e47` | MATCH |
| 8 | `build_records/F8_M7_DESIGN_NOTE_2026-11-02.md` | `7c70aa30a1aea71f1ae8e6eb18304c766ce4784469201bc8f0f515def2e383b1` | MATCH |
| 9 | `build_records/L1_TO_L2_F8_M7_BUILD_PACKET_2026-11-02.md` | `12b744b3a3875a834082a66bd279ae125952f2c20e939a8e56290ddb5fd55e4f` | MATCH |
| 10 | `build_records/L1_TO_L2_F8_M7_ROUND2_RESPONSE_2026-11-02.md` | `f21892053e5f3093ecd461ec817b2d6f8a160e4feba9486d04c06995cec72317` | MATCH |
| 11 | `build_records/L2_F8_M7_ROUND1_REVIEW_2026-11-02_RECEIVED.md` | `c92fc0803f870ba6e76ecb33f9ff8ec38b02b334772317bf1043d24b7a4d2410` | MATCH |
| 12 | `build_records/f8_m7_module_container_round2_2026-11-02.txt` | `c8313580ed15ff3a8554d57d9a1602f50c2859226999e47711e11b31b2a05424` | MATCH |
| 13 | `contracts/flight8/APPENDIX_A_OF_RECORD.md` | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` | MATCH |
| 14 | `contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | MATCH |
| 15 | `contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` | MATCH |
| 16 | `contracts/flight8/appendix_a.py` | `bc3e4f05f48e0840eddd5e61b8ea653411e4468900c098e801e5e13506fe0903` | MATCH |
| 17 | `gates/gate_a/GATE_A_AUTHORITATIVE_RECORD.md` | `719a9706f34e6c08119993f1826242939e6a2331fc77cf50a61c769d2710ca74` | MATCH |
| 18 | `gates/gate_b/GATE_B_AUTHORITATIVE_CERTIFICATION_RECORD.md` | `940d88a426d9530449d4c9d93d4a23085d354b678e2229edcf849806f6685883` | MATCH |
| 19 | `gates/gate_r0/GATE_R0_REGISTER_CLOSURE.md` | `59fd2a54a344f994346001eab2ec14b03357018536e3386318138df079e6e741` | MATCH |
| 20 | `governance/e1_stage1/AUTHORIZATION_001.json` | `aa2a05e5ec9cd5da5be4056b363625ec937d6db0caee1db36eae48fa2dcd0ca4` | MATCH |
| 21 | `governance/e1_stage1/AUTHORIZATION_002.json` | `175d37765c537a6b010c8a32d223b99db85c286422f00037e776ea0501f47d9f` | MATCH |
| 22 | `governance/e1_stage1/AUTHORIZATION_003.json` | `846c0e59ef4e47b8103a96bbb1270b3c360cf38b7f325d1353a5332a6b9ef509` | MATCH |
| 23 | `governance/e1_stage1/AUTHORIZATION_004.json` | `071223ce8222e5e45c2b4531cb38cfa4c45eb76b9f2a325f837aab7322183351` | MATCH |
| 24 | `governance/e1_stage1/AUTHORIZATION_REGISTRY.json` | `1223e17bb34c12a6c3c70748ff4a7dc2041d32b92a407c1a251cd741a1d373cf` | MATCH |
| 25 | `governance/e1_stage1/E1R_AMENDMENT.md` | `04058b21d2b1500afe18ee0a1daae54477f9896f9542b0a9e670040867334181` | MATCH |
| 26 | `governance/e1_stage1/E1R_GOVERNANCE.json` | `2e82102c7b6c738216351f0676751385840ba8b3a2a8f3e74d4c80f03e232a2f` | MATCH |
| 27 | `governance/e1_stage1/M7_PLACEMENT_RECORD.json` | `8cdfc320c01bb74b80880b897001e4c87e18b33b20632abe644c45d5e6b5856f` | MATCH |
| 28 | `governance/e1_stage1/M7_SUITE_RECORD.json` | `7d87ef2c7d5d8b898d8a69de967b8865289d33e2b25c78ea0bf5f63fd43231ab` | MATCH |
| 29 | `governance/e1_stage1/PACKAGE_SPECIFICATION.json` | `ed19cb79b3369b6b6a13d6bdae81205fef0ae583e1dacc66407cdd9b18977386` | MATCH |
| 30 | `governance/f8_stage1/F8_STAGE1_RATIFICATION_RECORD_v1_0.md` | `cdedfcb4540d950be69695b589b3f8cc8b5164278b7d57e850eb7ff8b601346b` | MATCH |
| 31 | `instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 32 | `instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 33 | `instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 34 | `instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 35 | `instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 36 | `instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 37 | `instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 38 | `instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 39 | `instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 40 | `instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 41 | `instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 42 | `instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 43 | `instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 44 | `instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 45 | `instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 46 | `instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 47 | `instrument/mfa_instrument/f8/config.py` | `f8b25fafb619c849ce229476ea860d8661012710c1933fde459f54d6486f471e` | MATCH |
| 48 | `instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 49 | `instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 50 | `instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 51 | `instrument/mfa_instrument/f8/runner.py` | `9d8b8378efb51ac403acf746dbe0640205f6a9bbfe2edc7436d40d7769df332b` | MATCH |
| 52 | `instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 53 | `instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 54 | `instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 55 | `instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 56 | `instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 57 | `instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 58 | `instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 59 | `instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 60 | `instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 61 | `instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 62 | `instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 63 | `instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 64 | `instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 65 | `instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 66 | `instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 67 | `instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 68 | `instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |
| 69 | `instrument/tests/test_f8_m1.py` | `857a1403f603b51bd2eea7ff5480fe5b89ef3b5d8de9c213f9b145540a393d20` | MATCH |
| 70 | `instrument/tests/test_f8_m2_m3.py` | `d0d26e75280dffef269e05f95e391b1db775a0f4712a5b3eac2f31ff50336460` | MATCH |
| 71 | `instrument/tests/test_f8_m4.py` | `8b8976b2c3602e0cc3932676cc6a091c69569af515bc183c374208578afa6d12` | MATCH |
| 72 | `instrument/tests/test_f8_m5.py` | `27cb5c965242ad2bde9aa61c5403eb97473190b67b1d232a2d801c5bd2097b41` | MATCH |
| 73 | `instrument/tests/test_f8_m6.py` | `808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca` | MATCH |
| 74 | `instrument/tests/test_f8_m7.py` | `cfe308bb99f2c6f539e091e26d6524f54c1bdf71619e179a6af6d9dcd73dc725` | MATCH |
| 75 | `instrument/tests/test_f8_mp1.py` | `f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d` | MATCH |
| 76 | `rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86` | MATCH |
| 77 | `rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md` | `198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034` | MATCH |
| 78 | `rulings/F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md` | `822ad8d88ad093c906fe1a8d74cc802fecc5799b5b132594054b96997b7d6187` | MATCH |

## Appendix B. Local evidence ledger

These are local build-review records and diagnostic programs, not canonical scientific evidence. The captured counterexamples and fixture limits are stated in the main review. Paths here are relative to the review workspace. Digests identify the exact files inspected.

| Evidence file | SHA-256 |
| --- | --- |
| `review_round2/runtime.json` | `7d6b2d67e9af91ecf9e99bdbe8a6fb53e9e3f03e73e9ab2905fd7e228fbc8167` |
| `review_round2/execution_status.json` | `5345ed1b4edd40c71f262f1ed96fd68ac40ada4a507b1a26ecce770a660adea8` |
| `review_round2/m1_pytest.log` | `a7fe4ee603849e56c5ad26fb03e428ddfeedc99dc93abaf6c463bc120926c03c` |
| `review_round2/m7_pytest.log` | `83c587899af36a300207cb4c03d7ec93190825a923cc4a03688ff744fbce1a37` |
| `review_round2/regression_pytest.log` | `505fb1fb2618ec9799256bdd8b0555477d8aace4ad73fd8eae8f10bd0f09cd9d` |
| `review_round2/memo_repair_probe.py` | `0b72f38ec8d049ba0149597f15bb94f1596125a8b69163b133db00dff00aeef1` |
| `review_round2/memo_repair_probe.out` | `f1f7033f13ae2bea8e5a0313c0442f5fb1aca94f1053dcaabef3d5204fd9ece6` |
| `review_round2/morphology_slot_probe.py` | `14db3b7defaee9a9f808c268b8349afe01af2afd3ec6daa60f614173c19232ce` |
| `review_round2/morphology_slot_probe.out` | `98414473dd9489bafdf94c9e6cf168b63a2a97e0e9a27d86dd66bf64dcbde493` |
| `review_round2/pricing_repair_probe.py` | `83b6dcbcb92fffd7777c68f3ed8f771273e0534b4e301b1196d13911c4027127` |
| `review_round2/pricing_repair_probe.out` | `f257b93f30184a172ac69eb630eb17dc2ec5309e8cac56b861e8897f609d3a40` |
| `review_round2/science_probe.py` | `987deb3a939c5188f593a83cdd17da7a46afa364669788debe9173b843c6f127` |
| `review_round2/science_probe.log` | `2e49b1d1e7d14800592ba71bcd6013b86c4f5bda2e8c9ba183be58c2772b871a` |
| `review_round2/interpretation_binding_probe.py` | `1425462bb4fd14c20df5ee0a6cce2908f898d2d1744409e5fde70d250c8e520d` |
| `review_round2/interpretation_binding_probe.log` | `cb85862a2c8ba6a99a1bbd5b7dc1382a0b480af8dd019ec76db6144544f433a5` |
| `review_round2/auth_probes/closed_repairs_probe.py` | `8b23dfbc398bc9326c16690390455bc930a4d77736a01be5369d8cfd61c1ef9c` |
| `review_round2/auth_probes/closed_repairs_probe.txt` | `328f35d317046766e547b2fc736d893b5477cb65424f8375c44d13d76ee167a3` |
| `review_round2/auth_probes/direct_dependency_probe.py` | `62503de6fbe4741365c6195c88a0930952049520af70ca25ef09cad3cb6fdcde` |
| `review_round2/auth_probes/direct_dependency_probe.txt` | `785d1f73f6c6481a82223f1e3b61a1cb9f349655329b103daba860e86f61d3dc` |
| `review_round2/auth_probes/clearance_probe.py` | `222de0eb0a0139b84a3c157e7476eb4ce3931325b4683308e529de218684e22c` |
| `review_round2/auth_probes/clearance_probe.txt` | `2e5ecea657981afdeb90334db5e9e25d17837ad75a5a489c801b4d6d9b21d9b2` |
| `review_round2/observe_commit_boundary.py` | `0b4d405b52b41c0c6f3c577bbf6bd61f3e3b962a26832294d76a2ac159103b8d` |
| `review_round2/observe_commit_boundary.log` | `acf2d398769361117d58053575a4edb7b5326de1c8e8a91b032c7d6bcd08db30` |
| `review_round2/commit_boundary_observation.json` | `d3a122b10f2e884842e3d14a7a5e354f3fec398bc1a92a26f869e0e1d20b8bd8` |

The completed review is limited to the exact round-2 archive identified above. Changed repair bytes require their own receipt and verification.
