# L2 — Flight 8 M7 build review, round 1

FINAL VERDICT: DEFECT-WITH-REPAIR

**Date:** 2026-11-02. **Register:** module build review, following the completed receipt and Mike's instruction to execute. **Reviewer:** L2. **Decision authority:** Mike. **Submission:** `f8_m7_build_round1_L2.zip`, SHA-256 `05e6b46ae396f3e3bde8a2369130f56201ea2e5e63a904ff4de0c444df22baf3`. **Declared repository pin:** `ee-theory-lab 2c8827b`.

**Instruction packet:** `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M7_BUILD_PACKET_2026-11-02.md`, SHA-256 `12b744b3a3875a834082a66bd279ae125952f2c20e939a8e56290ddb5fd55e4f`.

## 1. Disposition

M7 is **not cleared for placement**. The submission has eight grouped repair items, D1–D8 below, plus two unresolved decisions for Mike, H1–H2. Several defects admit concrete invalid records or let a cached acceptance survive a change that fresh validation rejects. They are not merely missing tests. D8 also establishes that the F8 placement check weakened the supplied E1 clearance rule.

The architecture has useful and substantially implemented parts: explicit authorization records, append-only registry checks, canonical envelopes, reconstruction of observables from persisted traces, replay of the canonical job-0 census, separation of package completion from scientific outcomes, and platform-sensitive adapter handling. Those parts do not overcome the confirmed acceptance and sequencing defects.

The M3 touch, M7-7, is acceptable on source identity and scope: reversing exactly the two disclosed changes reconstructs the placed M3 file. The null declaration and attempt-2 protocol identities remain unchanged. This acceptance is limited to the M3 touch; it does not clear M7.

This review authorizes no canonical job, master draw, production experiment, placement, or change to a frozen interpretation. Diagnostic fixtures and unit tests are build evidence. Mike's pending choices are not decided by this document.

## 2. Evidence, source references, and execution

### 2.1 Source notation

All source references below refer to the submitted bytes. Line numbers are one-based and identify the relevant implementation; the full payload receipt is in Appendix A.

| Reference | Repository-relative source | SHA-256 |
|---|---|---|
| R | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `4fdabf422f17f0c6584d45067cfe2499bbd9e5ae28c0bce634e2ee9d878b098e` |
| T | `flights/mfa_fidelity/instrument/tests/test_f8_m7.py` | `93fdea33755b71a2ce72f4b57fd45ef489a3872194929e5b451b5779a1a04c8e` |
| E1 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` |
| C | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` |
| RAT | `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_RATIFICATION_RECORD_v1_0.md` | `cdedfcb4540d950be69695b589b3f8cc8b5164278b7d57e850eb7ff8b601346b` |
| I001 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86` |
| I002 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md` | `198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034` |

References to `audit.py`, `closure.py`, `evaluator.py`, `dynamics.py`, `config.py`, and `null.py` below mean the F8 files under `flights/mfa_fidelity/instrument/mfa_instrument/f8/`, whose full digests appear in Appendix A. The review relies on the supplied contract and committed-record copies, not prior conversational summaries. Repository history at the declared real pin was not independently cloned or certified. Temporary Git repositories used below are explicitly test fixtures.

### 2.2 Local test record

The local interpreter is CPython 3.12.14 on Linux with glibc 2.39, NumPy 2.3.5, SciPy 1.17.0, pytest 9.2.0, and PyArrow 26.0.0. pytest and PyArrow were installed into an isolated review dependency directory. This is **not** the canonical Gate-B-qualified environment. No local result is presented as the canonical suite record.

Commands ran from `flights/mfa_fidelity/instrument`, with the isolated dependencies on `PYTHONPATH`.

| Check | Local result | Interpretation |
|---|---|---|
| `python -m pytest tests/test_f8_m7.py -q -p no:cacheprovider --tb=short --durations=6` | **6 passed, 4 failed, 13 errors; exit 1; 1.14 s** | All four failures and thirteen errors arise from omitted gate-record files. The full M7 chain was not independently reproduced. |
| M2/M3 regression against the touched `null.py` | **34 passed; exit 0; 140.70 s** | Unmodified submitted module, run separately. |
| M6 regression against the touched `null.py` | **55 passed; exit 0; 363.30 s** | Unmodified submitted module, run separately. |
| Targeted diagnostic probes | Confirmed the counterexamples reported in D1–D8 | Fixture boundaries are stated in §2.3 and Appendix B. |

The separate regression invocations used `-vv -p no:cacheprovider -o faulthandler_timeout=30 --tb=short --durations=6`. The faulthandler setting emits a diagnostic stack for a long test; it does not terminate the test or turn it into a failure. An initial combined M2/M3-plus-M6 attempt was interrupted with exit 130 after its progress log stopped updating; it is not counted as a completed result. Both whole modules were then restarted separately without changing their source.

The submitted L1 container record reports 23 M7 tests passing in 362.50 s and 89 M2/M3-plus-M6 tests passing in 191.72 s. That record is received evidence, not an independently reproduced local result. Its identity is `438f1361aec90bb5534f1ddd949e17a5a804850f2aab81c4e88efdbc673a5a0d`.

**V1 — incomplete executable review packet.** The archive matches its manifest exactly, but the manifest omits three files required by R's `GATE_RECORDS` and T's `_base_repo` (R 112–116; T 37–43):

| Required file | Expected full SHA-256 in submitted R |
|---|---|
| `flights/mfa_fidelity/gates/gate_a/GATE_A_AUTHORITATIVE_RECORD.md` | `719a9706f34e6c08119993f1826242939e6a2331fc77cf50a61c769d2710ca74` |
| `flights/mfa_fidelity/gates/gate_b/GATE_B_AUTHORITATIVE_CERTIFICATION_RECORD.md` | `940d88a426d9530449d4c9d93d4a23085d354b678e2229edcf849806f6685883` |
| `flights/mfa_fidelity/gates/gate_r0/GATE_R0_REGISTER_CLOSURE.md` | `59fd2a54a344f994346001eab2ec14b03357018536e3386318138df079e6e741` |

The observed failure first names the missing Gate A record; static inspection establishes that all three are absent. Supply these exact files in the next receipt-first packet. Do not weaken their checks or substitute invented content. Receipt integrity and test-packet completeness are different questions: receipt integrity passed; executable completeness did not.

### 2.3 What the diagnostic probes establish

The price validator, complete package-specification check, governance validator, M3 reverse-diff check, and adapter-checksum comparison used the actual submitted functions without substituting the behavior under examination. The negative-clearance probe used unmodified placement validation, real temporary Git history, and synthetic placement/suite records clearly designated as fixtures.

The stage-cache probe used the submitted conforming-environment stand-in, omitted the absent gate table in its isolated fixture, and disabled the declaration check only for that fixture alteration. The actual stage derivation, memo logic, placement verification, clearance bytes, and Git checks remained in use. Its observed role was `pre_governance`; the same cache serves canonical stages.

The readiness-history probe used real canonical encoding, committed fixture files, registry/history checks, record loading, and readiness derivation, with stage and qualification-generating inputs supplied as test stand-ins. The authorization-boundary probes stopped at a sentinel before the first lattice execution call. The morphology-slot probe used the submitted synthetic stepper with stage/authorization/readiness stand-ins, but actual adapter construction, artifact writing, per-run replay, M2 labels, and morphology validation. The execution-metadata probe used a genuine reduced 10×10, 1,100-tick realization run and genuine re-execution.

These probes establish the identified control-flow and validation defects. They do not assert that the canonical experiment has run or that the synthetic fixture outcomes are scientific findings.

## 3. Required repairs

### D1. Memo keys omit inputs that change validation results

**Scope:** M7-8. **Sources:** R 327–429, 509–525, 633–675, 747–764, 1320–1375; `audit.py` adapter identity and validation methods.

**D1(a): stage memo.** `_surface_paths()` omits the dynamically named L2 clearance file, although `verify_placement()` reads its contents, identity, and committed state. The key includes the pinned-root path but not its continued existence, availability of the pinned lock object, or freshly checked installed-package/virtual-environment facts. The platform tag is not a replacement for those inputs.

| Change after a successful binding | Warm cache | Fresh derivation |
|---|---|---|
| Delete the pinned directory | Retains `pre_governance`, `environment_conforms=True` | Returns `noncanonical`, conformity false |
| Modify the clearance file in the working tree | Retains accepted `pre_governance` binding | Raises `ApparatusHalt` for absent/uncommitted/wrong-identity clearance |

The demonstration used `pre_governance`; it did not execute a canonical act. Nevertheless, the shared memo can retain an obsolete acceptance because its key does not observe the changed dependency.

**D1(b): readiness memo.** Readiness loads prerequisite-producing authorizations and their registry/history through `load_record`, but its cache key omits that authorization dependency surface. A concrete temporary-repository sequence gave:

```text
INITIAL_READY True
PREREQUISITE_SURFACE_UNCHANGED True
AUTHORIZATION_BYTES_RESTORED True
CURRENT_PRODUCTION_AUTH_V2_VALID True
OLD_AUTH_V1_REFUSED: authorization v1 has 3 commits in its history
WARM_CACHE_READY True
COLD_CACHE_REFUSED: authorization v1 has 3 commits in its history
```

The initial prerequisites were valid under v1. After READY was cached, v1 was changed and then restored in two further commits. Current production authorization v2 remained valid, and all prerequisite bytes were unchanged. The correct immutable-history check rejected v1, but the memo bypassed that check. The current stage's identity excludes descriptive HEAD, so changing only authorization history does not supply the missing dependency indirectly.

**D1(c): production-adapter memo.** Its key uses `a.identity()`, which excludes the stored `body_sha256`; M6's validator checks that checksum. After caching a valid adapter, an otherwise identical adapter with an all-zero checksum returns true through the memo although M6 directly returns false. Conversely, caching the invalid object first causes a subsequent valid object to return false. Normal production callers also compare the stored checksum with the stage's adapter identity, so this particular false positive is not, by itself, a demonstrated canonical-execution bypass. The false rejection and violation of the claimed memo equivalence are established.

**Repair.** Keep mutable authority/environment checks outside reusable numerical caches, or bind the full dependency set explicitly. Resolve the clearance path into the stage surface and observe edits, deletion, and commitment. Recheck the environment/lock inputs. For readiness, include or freshly validate prerequisite-producing authorizations, registry and version history, manifest/dependency commitment, repository identity, and relevant working-tree changes. Adding HEAD alone does not handle an uncommitted authorization edit. For adapters, check the stored checksum before lookup and include it in the complete content key.

**Required tests.** Warm and cold results must agree after each omitted dependency changes. Include restored authorization bytes with altered history, clearance edit/deletion, pinned-root loss, and both adapter cache-order permutations. Retain the existing performance improvement only after this equivalence is demonstrated. No separate concrete defect was established in `_LIVE_ADAPTER_MEMO` under ordinary process-local platform assumptions, or in the artifact memo's file-content key; D4 concerns validation that the artifact memo caches.

### D2. Job authorization does not restrict the run's object

**Scope:** M7-2 and canonical run grammar. **Sources:** R 980–1014, 1017–1061, especially the job/panel guards at 999 and 1032.

`run_level()` checks that a job is a lattice job and that only job 0 uses the calibration panel. It does not enforce the permitted object for that job. Execution-boundary probes reached the first run call for these combinations:

| Sole granted job | Requested object/panel | Result |
|---|---|---|
| `skeleton_census` | `realization` / `canonical` | Reaches execution |
| `realization_census` | `skeleton_high` / `canonical` | Reaches execution |
| `calibration_census` | `null` / `calibration` | Reaches execution |

The calibration-null case has a later validation refusal, but only after the execution loop. Downstream consumers can also reject the wrong scientific job after runs exist. Neither protects the execution boundary.

**Repair.** Use one exact mapping, enforced before any run or artifact creation and on persisted level validation:

| Job | Permitted objects | Panel |
|---|---|---|
| `calibration_census` | `skeleton_high`, `realization` | `calibration` |
| `skeleton_census` | `skeleton_high`, `skeleton_low` | `canonical` |
| `realization_census` | `realization` | `canonical` |

None of these jobs authorizes the `null` object. Test every forbidden cross-combination with an execution sentinel, so rejection is proved to occur before the first run. Apply the same mapping to loading and restart paths.

### D3. Frozen prerequisites and scientific order are not fully enforced

**Scope:** M7-2, readiness, and job semantics. **Sources:** C §3.4, §7.1–§7.4; R 570–607, 1383–1393, 1698–1715, 2024–2094.

**D3(a): job-0 passage is optional in the governance grammar.** The real `validate_governance()` accepts a production-prerequisite set containing only the two qualifications. It does not require the calibration census or both MDD ceilings to pass. It also permits a census requirement of `valid_complete`, although a canonical census can be complete with failed ceilings. Exact equality between the manifest and that permissive governance set cannot restore the missing contract minimum.

C §3.4 requires either ceiling violation to stop the stage before any canonical census. C §7.3 requires job 0 to be committed before job 1. These are frozen requirements, not discretionary additions to the governance record.

**D3(b): realization can start before skeleton work.** The realization branch performs generic authorization/readiness checks and then starts realization levels. Its job-graph dependency tuple is empty. With an otherwise accepted READY state and an empty output directory, the execution-boundary probe reached realization execution before any skeleton output existed.

**D3(c): job 1 does not issue the required skeleton assessment.** `skeleton_census` persists two sweeps but does not evaluate and record T-S1′, T-S1c, T-S2, and the job-1 fidelity outputs. The combined P1 evaluation occurs after realization exists. `skeleton_stability` invokes T-S1′, but does not supply the complete missing assessment. Thus even a manually correct job order does not implement §7.3's requirement that the skeleton result be known before realization runs.

**D3(d): the earlier qualification sequence is also unenforced.** Source inspection shows that R 2041–2042 starts either M6 design or held-out audit without loading the preceding known-answer or design record; the job-graph entries at 1699–1702 supply no such dependency. The subsequent qualification job joins the audits, but that does not enforce §7.1's order before their execution. This observation is based on the submitted control flow; the diagnostic probes did not execute a full qualification sequence.

**Repair.** Make authorized, committed, canonical job-0 census passage—including both ceilings—a mandatory lower bound on production readiness alongside both qualifications. Preserve Mike's ability to add prerequisites. Produce a typed skeleton assessment immediately after the two skeleton sweeps, with the three tests and required fidelity results. Require that checkpoint and the authorized skeleton-stability record before realization execution, including direct `run_level` routes. Enforce dependencies as executable checks rather than descriptive tuples. Apply the same principle to the qualification order explicitly specified by §7.1.

**Required tests.** Reject missing job 0, failed ceilings, a weakened `valid_complete` census requirement, realization before skeleton assessment/stability, and direct-level attempts to bypass those dependencies. Confirm that skeleton tests are recorded before any realization execution call. Check the known-answer-to-design and design-to-held-out ordering with sentinels before audit execution. Do not invent a new scientific-pass condition: the contract requires assessment and order; any additional stop on a negative scientific result needs its own authority.

### D4. Artifact validation does not bind all claimed provenance

**Scope:** M7-1 and morphology replay. **Sources:** R 878–940, 980–1014, 1068–1080, 1609–1621; `dynamics.py` 109–143; `evaluator.py` 167–233.

**D4(a): execution metadata can be false even with replay enabled.** A genuine reduced realization run produced `ticks_advanced=1100`, `draws_consumed=1101`, and `extinction_tick=None`. Rewriting its canonical run JSON and corresponding record to `-17`, `-23`, and `42`, respectively, was accepted by `_check_provenance(..., replay=True)`. The trace was unchanged. The checker reconstructs the observation, but does not derive these execution fields; re-execution compares only the density hash. The same checker is used in production validation.

**D4(b): per-run JSON canonicality is not enforced.** Pretty-printed JSON with a trailing newline is accepted because `_check_provenance` decodes and compares the object without requiring canonical bytes. The advertised per-run canonical grammar therefore differs from the enforced grammar.

**D4(c): morphology does not bind a loaded record to its requested level slot.** One internally valid, production-shaped synthetic realization level at micro-value 250000 was serialized with genuine artifact validation and copied unchanged into all 24 expected slot paths. With fresh artifact validation, `validate_morphology` accepted 24 advertised rows backed by only one distinct actual level, yielding a rule-2 `NOT_PRODUCED` report with `verdict_scope='final level set'`. The ordinary canonical sweep builder rejected the same substitution at 347826 because its reconstructed spec/stream identity did not match.

The morphology validator checks advertised row order, filename hash, and record identity, but does not require the decoded record's level to equal the row's level. Self-consistency for the original level is insufficient evidence for the requested slot.

**Repair.** Derive exact-type execution metadata from the spec and trace: realization/null advance the full horizon, consume the stated initialization-plus-tick draws, and carry no skeleton extinction tick; skeleton fields follow the first zero and absorbing continuation under M1. Compare all claimed execution metadata during re-execution. Load run JSON through the canonical-byte reader and require exact `RunProvenance` type/equality. Bind every loaded morphology record to `(mode='production', level=m, obj='realization', panel='canonical', job='realization_census')`. Reuse a common slot check in `_load_level_results` so errors are rejected immediately.

**Required tests.** Independently corrupt each metadata field while retaining a valid trace and recomputing enclosing identities; reject both ordinary and re-execution validation. Reject equivalent noncanonical JSON bytes. Reject copied level files/artifacts, two-slot swaps, and duplicated-one-level morphology even when legal labels happen to be identical.

### D5. The proposed package is incomplete and cannot validate as declared

**Scope:** M7-3 and the ratified M5-5 record-kind mapping. **Sources:** R 145–155, 1698–1799, 2013–2016, 2136–2152; T 47–70; RAT §B M5-5; `closure.py` 634–673.

**D5(a): missing projection ensemble dependency.** The proposed 24 items include `DesignStability`, whose schema requires both a `ReferenceStructure` and a `SweepEnsemble` item. No `SweepEnsemble` is in the proposed list. A correctly wired specification of those 24 items fails with:

```text
item design_stability: dependency sweeps must be an item of type SweepEnsemble
```

Adding a `projection_sweep_ensemble` item makes that static specification validate. This establishes the missing dependency, not a final approved item count. The existing chain uses 20 items, omits `design_stability`, and excludes `projection_sweeps` from its jobs, so it does not test the advertised package.

**D5(b): the separate tolerance-ensemble kind is absent.** M7 requires the governance mapping `tolerance_ensembles -> ToleranceEnsemble`, but has no registered type, validator, canonical output, or package item for that record kind. M5 produces per-level ensembles; its `ToleranceProgram` only summarizes their count and ceiling/stop facts, and does not retain them. Ratification explicitly keeps the two kinds separate.

**Repair.** Supply a concrete complete package specification with the projection ensemble and its dependencies. Implement canonical persistence/replay for the 24 per-level tolerance ensembles, distinctly from the summary program. A typed collection is possible if it retains and validates each level's ensemble against the canonical census and preserves the ratified mapping. Update the proposed vocabulary, item count, declaration identity, and tests to the actual design.

**Required tests.** Validate and assemble the entire proposed package. Include the projection-ensemble path and separate tolerance records, with missing/duplicate/wrong-level/tampered ensemble negatives. The tests may stub costly numerical generation where clearly disclosed, but must exercise real package dependencies, persistence, and replay. There is no need to run a production scientific experiment to test this grammar.

### D6. Pricing validation checks arithmetic but not the priced experiment

**Scope:** M7 package record derivation. **Sources:** R 1846, 2122–2123; `audit.py` 975–1011; RAT M6-9; I002 §9(a).

The real pricing validator and `price_recorded` predicate accept a 10,000-replicate record with `master=1`, `theta_p=-7.0`, `theta_t=900.0`, nominal alpha 0.8, construction bound −5, terminal count −1, an incorrect source, and an all-zero declaration identity, provided the rejection fraction and CP upper limit are internally consistent. In the probe, zero rejections gave the correctly computed upper bound `0.0002995283597757026`, so the two arithmetic checks passed.

The producer supplies legitimate metadata; the defect is that persisted metadata need not derive from that producer's declared experiment. An envelope's job binding does not validate the unchecked fields. The chain excludes `m6_price`, so its success provides no coverage of this issue.

**Repair.** Validate exact count types/domains, the frozen replicate count and pricing master, stage-adapter thresholds, M3 nominal alpha and construction bound, the declared NULL source, and the generator declaration identity. Re-derive the sampled counts through deterministic replay or sufficient independently checkable retained evidence, consistent with the stated every-record-derives principle. If replay is memoized, bind every input and the complete validated record content.

**Required tests.** A valid production-shaped record validation path with controlled evidence, plus independent alteration of every metadata field and both observed counts. Arithmetic agreement alone must not qualify a record from another experiment.

### D7. Two governance fields are carried without their required semantic binding

**Scope:** ratification §E.5 and §E.7; claimed exact governance binding. **Sources:** R 530–607, particularly 575–587; RAT §E and §F.

The unmodified governance validator accepts both of these changes, with the record identity recomputed:

```text
generator_declaration_markdown_sha256 = 000...000  (64 zeroes)
null_validation_decision = "PASSED at alpha 0.05"
```

The generator Markdown field is checked only for hash shape. The actual declaration file is not in this packet or the stage surface, and its identity is not compared with approved declaration bytes. The tuple declaration digest is correctly compared, but it is a different object. The null-decision field is checked only for the substrings `PASSED` and `0.05`, allowing a statement that reverses the required default-pairing failure disclosure.

**Repair.** Include and bind the approved generator declaration Markdown and its full identity, allowing an approved successor only through its identified record. Retain the tuple digest as its separate identity. Represent the null attempt/protocol/decision and default-pairing disclosure as typed, validated facts or a canonical statement bound to the actual record. Preserve attempt 1's failed record and the disclosed `0.0445 > 0.0429` default comparison; an opposite statement cannot be accepted because it contains the right keywords.

**Required tests.** Reject an arbitrary 64-hex Markdown identity, missing/wrong declaration bytes, an unapproved successor, and the contradictory default-alpha passage string. Correctly bind the accepted attempt-2 protocol and its actual disclosed decision.

### D8. An adverse L2 review can be accepted as placement clearance

**Scope:** carried E1 placement grammar. **Sources:** R 509–525, especially 519; E1 400–420, especially 413.

F8 checks only whether `SOUND` appears anywhere in the clearance text. The supplied E1 implementation instead requires the explicit final-verdict marker. This is a weakening introduced in the F8 carry, despite the packet's claim of verbatim mechanics.

A no-mocks temporary-Git probe used the submitted runner/test bytes and typed committed placement/suite fixtures. A clearance whose final disposition is `DEFECT-WITH-REPAIR` was refused when it contained no `SOUND` keyword, but was **accepted** when the following explanatory sentence was added: `SOUND withheld pending repairs.` Both exact source identities were present. The synthetic suite fixture was solely an input to the parser test, not evidence of a real suite run.

**Repair.** Parse one authoritative current final-disposition field/marker, require its exact value to be `SOUND`, reject conflicting or repeated dispositions, and retain exact source-identity checks. Historical quotations, negations, and explanatory uses of the word cannot grant clearance.

**Required tests.** Reject an explicit adverse verdict accompanied by “SOUND withheld,” “not SOUND,” a quoted earlier positive verdict, or conflicting final markers. Accept one unambiguous current positive verdict naming the correct bytes. This review's authoritative final verdict remains the adverse verdict at the top; the word's appearance in this analysis is not clearance.

## 4. Decisions reserved for Mike

### H1 / M7-4 — pass-1 morphology does not yet discharge the final-level-set obligation

C §4.4/§4.7 and RAT §E.2 require the verdict of record on the final level set. R 1599–1606 computes a pass-1 verdict and records an evaluability halt for every requested insertion. That is honest disclosure of an unexecuted refinement, but it does not supply the required refined verdict.

A concrete label witness—twelve N labels followed by twelve S labels—produces `LOCATED`, eight requested insertions, eight halts, `verdict_scope='pass-1 level set'`, and a true `morphology_pass1_evaluated` predicate. The lack of P1 dependence is correctly preserved, but it does not waive the separate morphology obligation. An expected rule-2 result also cannot waive the obligation for other observations.

**Disposition: HOLD for an identified ruling.** Mike may preserve final-set evaluation and authorize a separately reviewed M1/run-grammar change for insertion levels, or explicitly adopt a restricted secondary pass-1 report and define its completion/pass status when insertions cannot be evaluated. The chosen route must be bound by identity and reflected in code, predicates, tests, and any affected budget. L2 does not treat either choice as already ratified.

### H2 / M7-5 — calibration-panel stability conflicts with the frozen data-role restriction

C §3.4, §4.11 populations, and §7.3 job 0 say the calibration data are “never scored, never reused.” R 1651–1683 assembles those runs into an alternative sweep and scores T-S1′ or T-R1′ to issue stability records. “Never scored for P1” is a narrower restriction introduced by the proposal. RAT M5-3 replaces the template axis with grid-resolution and solver-independence checks; it does not authorize this reuse.

The internal alternative sweep is also given `role='canonical'`, even though it contains calibration-panel provenance that the normal M-P1 canonical-sweep validator would reject. It is not persisted, as disclosed, but its internal role should still state what it is.

**Disposition: HOLD; current-contract conformity is not established.** The direct current-contract repair is an independently declared stability panel with reviewed seed/run-spec permissions and an updated resource count. Alternatively, Mike may explicitly rule on a calibration-reuse exception, stating its limited inferential meaning and the dependence of the realization stability check on data also used to estimate its bands. That would need an identified interpretation/amendment and a truthful data-role implementation.

Mike must also settle what the two stability outcomes mean: the submitted skeleton test compares the T-S1′ boundary or identical adverse cause, while realization stability compares T-R1′ outcome/cause. Those are specific proposed stability definitions, not automatically equivalent to every reading of the contract's reproduced class language.

## 5. Disposition of each build declaration

| Declaration | L2 disposition | Basis |
|---|---|---|
| M7-1: parquet plus canonical run record; trace replay; optional M1 replay and mandatory tranche replay | **Repair required** | Trace-derived observables and I001 are carried correctly; D4 leaves execution metadata, run-byte canonicality, and morphology slot provenance unbound. |
| M7-2: 17-job graph and readiness gate | **Repair required** | Both qualifications are mandatory, but D2 and D3 expose object-authorization, job-0, ordering, and early skeleton-assessment gaps. |
| M7-3: 24 proposed package items | **Repair required; corrected proposal for Mike** | D5: missing projection-ensemble dependency and missing separate tolerance-ensemble implementation. The present complete proposal cannot validate. |
| M7-4: pass-1 morphology scope | **HOLD for Mike** | H1; final-set requirement remains in force until an identified decision changes or discharges it. D4's slot substitution is an independent defect under either choice. |
| M7-5: calibration-panel stability | **HOLD for Mike; conflicts with current frozen restriction** | H2; M5-3 does not grant the proposed reuse. |
| M7-6: tranche/benchmark panels and 2,400 runs | **Coherent proposal, conditional on final stability/refinement design** | 960 job-0 + 960 skeleton + 480 realization runs = 2,400. Any new stability/refinement runs require revised scope/counts. |
| M7-7: M3 touch | **ACCEPTABLE on source scope and identities** | Exactly the two disclosed obligations; reverse-diff and declaration/protocol verification below. Regression execution is separately recorded in §2.2. |
| M7-8: all memo keys include every input | **REJECTED as stated; repair D1** | Warm-versus-cold counterexamples demonstrate omitted authority, environment, and adapter-checksum inputs. |

### 5.1 Accepted or retained mechanisms

Direct `load_authorization` correctly checks committed bytes, registry membership, exact stage/governance/specification binding, append-only registry prefix history, and one-commit-per-version immutability. D1 repairs the cache bypass of those checks; D2 repairs what a granted job permits to execute.

The exact-set prerequisite manifest comparison works relative to its supplied governance set. D3 adds frozen-contract minima that the current governance grammar fails to require. Placing readiness on scientific jobs and making the completed package an end state avoids the disclosed circular prerequisite; that architectural decision is acceptable.

M7's job-0 census issuance reconstructs the two calibration objects from authorized LevelRecords, invokes M5's `derived_provisional` constructor, then issues and replays the canonical role. That basic issuance mechanism is acceptable, subject to the repairs to gates and provenance. M-P1 qualification is produced under its named canonical job and replayed; configurable known-answer parameters do not silently establish passage because M-P1 restricts `passed` to the frozen qualification configuration.

The adapter's cross-platform handling is also acceptable in principle: platform-independent keys, indices, surface and declarations are compared with a local rebuild; canonical role requires payload/body match; `_stage_adapter` refuses a mismatch and uses M6's replaying loader. No independent cross-platform canonical bypass was demonstrated. D1's checksum-cache defect remains separate.

I001's whole-tail mean, including positive contributions before an in-tail extinction, is preserved through the placed observation routine. The examined code does not coerce every non-surviving run's mean to zero.

### 5.2 M3 verification

Reversing only the two hunks in `F8_M3_M7_TOUCH_DIFF.txt` reconstructs the placed file exactly:

| Identity | Full SHA-256 |
|---|---|
| Reconstructed placed `null.py` | `4ee3f239b27f772b64a3f31a6dfff73112c40386904e3bda50e826766cef0121` |
| Submitted touched `null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` |
| Unchanged null declaration | `bfe0a5a0067cae7ca524cc2ba299219ce89007e794d8703a9872869388e9c05c` |
| Unchanged attempt-2 protocol | `20ae18f0a85d9b6ce3972acb2630529bd300a92fbc16e5f6f8b1a48a537abf2a` |
| Submitted M7 runner declaration, recomputed | `7b2ecefdd9b30365c44d94ef8b35115ce0b3c1ac9032b3645772fe77db58303f` |

The deprecated eligibility method is removed and the nonexistent pricing-function name is corrected to the real reported statistic, with the M6 price distinguished. RAT §E.3–4 are discharged by this touch.

### 5.3 Carried items and documentation correction

The two stale-comment obligations in RAT §E.8 remain for the next edit of their respective test files, as disclosed. I002 §9(b)/M6-10's later lattice/surrogate comparison has no completed named M7 output here; explicitly retain that obligation and identify its eventual output/authorization. This review does not invent a new canonical job or treat that later comparison as an unstated M6 prerequisite.

The packet's timing example should be corrected: at 1.3 seconds/run, 960 runs take approximately 20.8 minutes and 480 take 10.4 minutes. The stated 52/52/26 minutes corresponds to about 3.25 seconds/run. This is a documentation arithmetic correction. The 2,400 count describes the three main lattice jobs, not the entire M6 workload or all validation/benchmark/tranche execution.

## 6. Conditions for the next round

Return a receipt-first repair packet identifying the changed runner, tests, declaration/schema identities, and any separately changed placed module. Answer D1–D8 by sub-item, each with the relevant source repair and discriminating negative test. Include the three missing gate records, the actual approved generator declaration Markdown, and a complete concrete package specification exercised by the tests.

Obtain and include Mike's identified dispositions of H1 and H2 before claiming current-contract coverage of morphology and stability. Reconcile package predicates, data roles, execution guards, and resource totals with those decisions. Re-run the full M7 module on the submitted bytes and retain the canonical-suite gate on the canonical machine. A passing subset with the unresolved package paths omitted is insufficient.

Source findings in this review do not depend on the missing gate files being defective; their absence limits executable packet coverage. Supplying them alone does not close D1–D8. Conversely, a source repair does not erase the requirement to reproduce the complete module and satisfy the pending decisions.

## Appendix A. Complete receipt

The archive's full digest matches Mike's supplied value. There are **66 payload files plus `MANIFEST.txt` = 67 regular-file entries**, no directory entries, no missing or unlisted payloads, no duplicate archive/manifest paths, and no ZIP CRC failures. All 66 payload digests match the manifest. The manifest's own computed digest is `6f184bf55d3a55903b7016eac10ff9107bd9ac59a403e671b918532f2aadee31`; it is not self-listed.

Paths are relative to `flights/mfa_fidelity/`, except the root manifest.

| # | File | Full computed SHA-256 | Check |
|---:|---|---|---|
| 1 | `build_records/F8_M3_M7_TOUCH_DIFF.txt` | `be385acfeb5a48def068190fed2e2442805007fe832cde3fdfb1aa373e9df055` | MATCH |
| 2 | `build_records/F8_M7_DESIGN_NOTE_2026-11-02.md` | `99747de81fe52e5b7e13a665d77e137345e06c7f396a2996dbcba36d2b429fa5` | MATCH |
| 3 | `build_records/L1_TO_L2_F8_M7_BUILD_PACKET_2026-11-02.md` | `12b744b3a3875a834082a66bd279ae125952f2c20e939a8e56290ddb5fd55e4f` | MATCH |
| 4 | `build_records/f8_m7_module_container_2026-11-02.txt` | `438f1361aec90bb5534f1ddd949e17a5a804850f2aab81c4e88efdbc673a5a0d` | MATCH |
| 5 | `contracts/flight8/APPENDIX_A_OF_RECORD.md` | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` | MATCH |
| 6 | `contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | MATCH |
| 7 | `contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` | MATCH |
| 8 | `contracts/flight8/appendix_a.py` | `bc3e4f05f48e0840eddd5e61b8ea653411e4468900c098e801e5e13506fe0903` | MATCH |
| 9 | `governance/e1_stage1/AUTHORIZATION_001.json` | `aa2a05e5ec9cd5da5be4056b363625ec937d6db0caee1db36eae48fa2dcd0ca4` | MATCH |
| 10 | `governance/e1_stage1/AUTHORIZATION_002.json` | `175d37765c537a6b010c8a32d223b99db85c286422f00037e776ea0501f47d9f` | MATCH |
| 11 | `governance/e1_stage1/AUTHORIZATION_003.json` | `846c0e59ef4e47b8103a96bbb1270b3c360cf38b7f325d1353a5332a6b9ef509` | MATCH |
| 12 | `governance/e1_stage1/AUTHORIZATION_004.json` | `071223ce8222e5e45c2b4531cb38cfa4c45eb76b9f2a325f837aab7322183351` | MATCH |
| 13 | `governance/e1_stage1/AUTHORIZATION_REGISTRY.json` | `1223e17bb34c12a6c3c70748ff4a7dc2041d32b92a407c1a251cd741a1d373cf` | MATCH |
| 14 | `governance/e1_stage1/E1R_AMENDMENT.md` | `04058b21d2b1500afe18ee0a1daae54477f9896f9542b0a9e670040867334181` | MATCH |
| 15 | `governance/e1_stage1/E1R_GOVERNANCE.json` | `2e82102c7b6c738216351f0676751385840ba8b3a2a8f3e74d4c80f03e232a2f` | MATCH |
| 16 | `governance/e1_stage1/M7_PLACEMENT_RECORD.json` | `8cdfc320c01bb74b80880b897001e4c87e18b33b20632abe644c45d5e6b5856f` | MATCH |
| 17 | `governance/e1_stage1/M7_SUITE_RECORD.json` | `7d87ef2c7d5d8b898d8a69de967b8865289d33e2b25c78ea0bf5f63fd43231ab` | MATCH |
| 18 | `governance/e1_stage1/PACKAGE_SPECIFICATION.json` | `ed19cb79b3369b6b6a13d6bdae81205fef0ae583e1dacc66407cdd9b18977386` | MATCH |
| 19 | `governance/f8_stage1/F8_STAGE1_RATIFICATION_RECORD_v1_0.md` | `cdedfcb4540d950be69695b589b3f8cc8b5164278b7d57e850eb7ff8b601346b` | MATCH |
| 20 | `instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 21 | `instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 22 | `instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 23 | `instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 24 | `instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 25 | `instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 26 | `instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 27 | `instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 28 | `instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 29 | `instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 30 | `instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 31 | `instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 32 | `instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 33 | `instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 34 | `instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 35 | `instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 36 | `instrument/mfa_instrument/f8/config.py` | `43ea8de23c0d718b246936c7ff6f18e4f8e5243f77ddb240d896e5d00bdf0e07` | MATCH |
| 37 | `instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 38 | `instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 39 | `instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 40 | `instrument/mfa_instrument/f8/runner.py` | `4fdabf422f17f0c6584d45067cfe2499bbd9e5ae28c0bce634e2ee9d878b098e` | MATCH |
| 41 | `instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 42 | `instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 43 | `instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 44 | `instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 45 | `instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 46 | `instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 47 | `instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 48 | `instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 49 | `instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 50 | `instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 51 | `instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 52 | `instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 53 | `instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 54 | `instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 55 | `instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 56 | `instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 57 | `instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |
| 58 | `instrument/tests/test_f8_m1.py` | `23d4260f5a2d996b56e748aada1e7ed5d5b6d35e57bc41be9fdc53b34b04bff0` | MATCH |
| 59 | `instrument/tests/test_f8_m2_m3.py` | `d0d26e75280dffef269e05f95e391b1db775a0f4712a5b3eac2f31ff50336460` | MATCH |
| 60 | `instrument/tests/test_f8_m4.py` | `8b8976b2c3602e0cc3932676cc6a091c69569af515bc183c374208578afa6d12` | MATCH |
| 61 | `instrument/tests/test_f8_m5.py` | `27cb5c965242ad2bde9aa61c5403eb97473190b67b1d232a2d801c5bd2097b41` | MATCH |
| 62 | `instrument/tests/test_f8_m6.py` | `808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca` | MATCH |
| 63 | `instrument/tests/test_f8_m7.py` | `93fdea33755b71a2ce72f4b57fd45ef489a3872194929e5b451b5779a1a04c8e` | MATCH |
| 64 | `instrument/tests/test_f8_mp1.py` | `f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d` | MATCH |
| 65 | `rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86` | MATCH |
| 66 | `rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md` | `198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034` | MATCH |
| 67 | `MANIFEST.txt` (archive root) | `6f184bf55d3a55903b7016eac10ff9107bd9ac59a403e671b918532f2aadee31` | Computed; not self-listed |

## Appendix B. Diagnostic evidence ledger

Probe files are review fixtures, not repository changes or scientific records. The ledger identifies the code and captured output supporting each counterexample; the scope of substituted fixture inputs is stated in §2.3 and in the probe code.

| Findings | Diagnostic file | SHA-256 |
|---|---|---|
| D1(a,c), D4(a,b) | `memo_replay_probe.py` | `b3120fa25182313d8f5b61cc3299677a0488f43191ebdb37172f84b19027d677` |
| Captured output | `memo_replay_probe.out` | `fe301ef4b2097f071107af9730aa13a4208180324a8ae6768e79341523f80679` |
| D2, D3(a,b), D7 | `m7_auth_guards_probe.py` | `893430e6f5555a7a8696863702d3eae088f25a7538adbe744cbf2c13152f6f63` |
| Captured output | `m7_auth_guards_probe.out` | `8f0879bca27c142715281fa975400f12e3bf25a775930b69b2cbbf5439059753` |
| D1(b) | `m7_readiness_auth_history_probe.py` | `209f36bd9c6c26c4d9bd8c0f3885c7cb5d7336e74737c7e5a0a44428b15f6811` |
| Captured output | `m7_readiness_auth_history_probe.out` | `e757301b657ca27774a2be75d607dfe5974ec57ff6681b529023fade6636ae16` |
| D4(c) | `morphology_slot_probe.py` | `c86f7f3d47e9f58e29371e986d8ec4dc7e64c1db9b345a14560f5dbc67bc2fc2` |
| Captured output | `morphology_slot_probe.out` | `4e68117571cb2fbd513219d94d605932f6f8696e211665b400f183375e46c27e` |
| D5, D6, H1, M7-7 | `science_package_probe.py` | `9e95175135b391de585df962983169fc40b7a8f7684448c0e960da1b2db2a601` |
| Captured output | `science_package_probe.txt` | `358d4883da53f6717dead623431f318a222a6e5a087cd3d68fb97b83a881764e` |
| D8 | `m7_negative_clearance_probe.py` | `8e99477eb046b4be35e0358478279f8bf9777461daff1e005d16f3372c1e2313` |

### Captured diagnostic outputs

#### D1(a,c), D4(a,b) — memo_replay_probe.py

```text
{"before": "pre_governance", "cold": "noncanonical", "cold_environment_conforms": false, "probe": "stage_pinned_directory_removed", "warm": "pre_governance", "warm_environment_conforms": true}
{"before": "pre_governance", "cold": "ApparatusHalt: placement record does not verify: L2 clearance file absent, uncommitted, or not the named identity", "probe": "stage_clearance_tamper", "warm": "pre_governance"}
Building real production adapter (deterministic apparatus only)
{"bad_cold": false, "bad_direct": false, "bad_warm": true, "probe": "production_adapter_checksum_omitted", "valid_after_bad": false, "valid_first": true}
{"forged": {"draws_consumed": -23, "extinction_tick": 42, "ticks_advanced": -17}, "original": {"draws_consumed": 1101, "extinction_tick": null, "ticks_advanced": 1100}, "probe": "provenance_metadata_tamper", "replay_true": "ACCEPTED"}
{"file_format": "pretty-printed JSON plus newline", "probe": "run_record_noncanonical_json", "validation": "ACCEPTED"}
```

#### D2, D3(a,b), D7 — m7_auth_guards_probe.py

```text
JOB_OBJECT_BOUNDARY
GRANT=skeleton_census; REQUEST=realization/canonical; UNAUTHORIZED_OBJECT_REACHED_EXECUTION=True
GRANT=realization_census; REQUEST=skeleton_high/canonical; UNAUTHORIZED_OBJECT_REACHED_EXECUTION=True
GRANT=calibration_census; REQUEST=null/calibration; UNAUTHORIZED_OBJECT_REACHED_EXECUTION=True
JOB_ORDER_BOUNDARY
EMPTY_OUTPUT_DIR; REALIZATION_REACHED_EXECUTION_BEFORE_SKELETON=True
GOVERNANCE_MINIMUM; REAL_VALIDATOR_NO_PATCHES
TWO_QUALIFICATIONS_ONLY_GOVERNANCE_ACCEPTED=True
CALIBRATION_CENSUS_REQUIRED=False; CALIBRATION_CEILING_STOP_REQUIRED=False
GOVERNANCE_IDENTITY_AND_DECISION_BINDING; REAL_VALIDATOR_NO_PATCHES
ACCEPTED {'generator_declaration_markdown_sha256': '0000000000000000000000000000000000000000000000000000000000000000'}
ACCEPTED {'null_validation_decision': 'PASSED at alpha 0.05'}
```

#### D1(b) — m7_readiness_auth_history_probe.py

```text
INITIAL_READY True CACHE_ENTRIES 1
PREREQUISITE_SURFACE_UNCHANGED True
AUTHORIZATION_BYTES_RESTORED True
CURRENT_PRODUCTION_AUTH_V2_VALID True
OLD_AUTH_V1_REFUSED authorization v1 has 3 commits in its history: versions are append-only and immutable
WARM_CACHE_READY True SAME_OBJECT True
COLD_CACHE_REFUSED authorization v1 has 3 commits in its history: versions are append-only and immutable
```

#### D4(c) — morphology_slot_probe.py

```text
{"actual_distinct_record_levels": 1, "actual_level_micro": 250000, "all_copied_record_label": "S", "morphology_rule": "2", "morphology_scope": "final level set", "morphology_verdict": "NOT_PRODUCED", "probe": "morphology_level_slot_substitution", "real_provenance_replayed": true, "requested_slots": 24, "validation": "ACCEPTED"}
{"probe": "same_substitution_canonical_sweep", "validation": "EvaluatorDomainError: level 347826: spec hash / stream key do not reconstruct"}
```

#### D5, D6, H1, M7-7 — science_package_probe.py

```text
INVALID_PRICE_ACCEPTED True
INVALID_PRICE PricingRecord(replicates=10000, master=1, theta_p=-7.0, theta_t=900.0, s_min_rejections=0, s_min_rejection_rate=0.0, cp_upper_95=0.0002995283597757026, alpha_p_nominal=0.8, construction_bound=-5.0, s_term_no_sustained=-1, source='wrong_source', declaration_sha256='0000000000000000000000000000000000000000000000000000000000000000')
DECLARED_24_ITEM_SPEC_REJECTED item design_stability: dependency sweeps must be an item of type SweepEnsemble
25_ITEM_SPEC_WITH_ENSEMBLE_VALIDATES 25
TOLERANCE_ENSEMBLE_REGISTERED False
TOLERANCE_ENSEMBLE_VALIDATOR False
TOLERANCE_ENSEMBLE_PRODUCER False
MORPHOLOGY_INSERTION_WITNESS {'verdict': 'LOCATED', 'cause': None, 'insertions': 8, 'halts': 8, 'scope': 'pass-1 level set', 'pass_predicate': True}
RECONSTRUCTED_PLACED_M3_SHA256 4ee3f239b27f772b64a3f31a6dfff73112c40386904e3bda50e826766cef0121
NULL_DECLARATION_SHA256 bfe0a5a0067cae7ca524cc2ba299219ce89007e794d8703a9872869388e9c05c
ATTEMPT2_PROTOCOL_SHA256 20ae18f0a85d9b6ce3972acb2630529bd300a92fbc16e5f6f8b1a48a537abf2a
RUNNER_DECLARATION_SHA256 7b2ecefdd9b30365c44d94ef8b35115ce0b3c1ac9032b3645772fe77db58303f
```

#### D8 — negative clearance

The no-mocks probe returned:

```text
negative_without_keyword REFUSED L2 clearance file does not state the SOUND disposition
negative_with_keyword ACCEPTED_AS_CLEARANCE True
FINAL_VERDICT_IN_FIXTURE DEFECT-WITH-REPAIR
E1_REQUIRED_MARKER_PRESENT False
```


## Appendix C. Test-output excerpts and final byte check

### Unmodified M7 module

```text
FileNotFoundError: flights/mfa_fidelity/gates/gate_a/GATE_A_AUTHORITATIVE_RECORD.md
4 failed, 6 passed, 13 errors in 1.14s
exit status: 1
```

All four failures and thirteen setup errors have the same missing-file cause. The other two gate records are also absent from the archive and are required by the same fixture.

### Separate M2/M3 and M6 module regressions

#### M2/M3

```text
============================= slowest 6 durations ==============================
62.33s call     tests/test_f8_m2_m3.py::test_m3_n_fold_law_fft_matches_exact_rational_convolution_at_small_n
18.00s call     tests/test_f8_m2_m3.py::test_m3_validation_record_refuses_the_iid_all_windows_interpretation_and_scope_mismatch
17.62s call     tests/test_f8_m2_m3.py::test_h3_eligibility_is_never_passage_and_unregistered_records_cannot_claim_it
11.47s call     tests/test_f8_m2_m3.py::test_h1_attempt1_is_retained_and_the_ratified_protocol_is_fixed
10.40s call     tests/test_f8_m2_m3.py::test_m3_stepper_null_matches_law_at_reduced_grid_with_scaled_thresholds
6.84s call     tests/test_f8_m2_m3.py::test_h1_ratified_protocol_decides_and_binds_the_record
======================== 34 passed in 140.70s (0:02:20) ========================
exit status: 0
```

#### M6

```text
============================= slowest 6 durations ==============================
280.88s call     tests/test_f8_m6.py::test_smoke_audit_record_validates_and_production_paths_are_refused
56.44s setup    tests/test_f8_m6.py::test_one_sweep_per_class_is_well_formed_and_scored_on_the_final_level_set
5.19s call     tests/test_f8_m6.py::test_null_source_is_e_at_zero_feedback_and_matches_m3_law_on_the_terminal_window
5.16s call     tests/test_f8_m6.py::test_d1_target_legality_is_certified_over_the_reachable_surface_before_any_trajectory
4.36s call     tests/test_f8_m6.py::test_established_date_dispatches_production_paths_under_the_derived_masters_without_a_draw
4.03s call     tests/test_f8_m6.py::test_missing_adapter_key_is_an_apparatus_halt_not_a_derivation
======================== 55 passed in 363.30s (0:06:03) ========================
exit status: 0
```

The separate modules completed all **89** submitted tests (34 + 55). Diagnostic timeout messages in the verbose logs are faulthandler stack dumps during long tests, not test timeouts or failed assertions. The initial combined invocation has no completed test summary and is excluded.

### Captured test-log identities

| Log | Full SHA-256 |
|---|---|
| `m7_pytest.log` | `8815e67a842c44e6a007aefb8383ec06b760ff722c751d322a4452f1e7195eba` |
| `m2_m3_m6_pytest.log` | `d09f0ad06d6e59b908037317d6c044f7ababd3466cb46d5b901cf6f0855baf04` |
| `m2_m3_pytest_retry.log` | `54d715873bd4409be58dd19697cd386efda726a17f77065757df837433dac39c` |
| `m6_pytest_retry.log` | `d23b888392d48e387e7fbf85fe93fb2cba8f3c205d57d022d2ccfb35b242e14d` |

After all tests and diagnostic probes, **66/66 submitted payload files still match their manifest digests**. The reviewed runner, test module, and touched M3 source were not edited. No real repository placement or canonical scientific job was performed.
