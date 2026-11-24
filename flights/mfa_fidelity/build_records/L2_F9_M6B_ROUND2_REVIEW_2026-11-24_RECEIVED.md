# L2 → L1 and Mike — Flight 9 M6 part 2 build review, round 2

**Date:** 2026-11-24  
**Role:** L2, adversarial module-build reviewer  
**Decision authority:** Mike  
**Scope:** the M6B repair of round-1 D1, with regression review of the complete change.

**Reviewed archive:** f9_m6b_build_round2_L2.zip  
**Archive SHA-256:** `f63a181b9f7b57b18ff287a188007710737b30ebe30187d90494358b65d965e6`

## 1. Disposition

**The submitted round-2 build is sound within the reviewed module boundary. D1 is closed.** The threshold orchestration now gives an empty comparison family its required higher-priority `no eligible contour` cause while preserving the observed-map record. Both reported thresholds use that corrected orchestration. The unchanged skeleton wrapper delegates to the separately repaired evaluator. The new regression catches the old error and also catches an overbroad repair that assigns the constant-index cause to an ordinary nonconstant family. [X, evaluate_level_at, reported_thresholds and skeleton_boundary; T, test_a_constant_index_outranks_the_maps_state_on_every_route; C §7; independent execution in §8.]

The inverse diff reconstructs both round-1 files exactly. No change outside the disclosed hunks was found. The full supplied M6B suite passes independently: **14 passed in 163.05 seconds**. Additional constructed-input checks preserve apparatus validation, point diagnostics, and a constant index's record beside a nonconstant sibling with an unstable bootstrap result. [Δ; §3; §4; §8.]

**M6B-2, M6B-3 and M6B-4 now receive ACCEPTABLE dispositions.** The prior ACCEPTABLE dispositions on M6B-1, M6B-5 through M6B-9, and all seven readings stand. These are L2 review dispositions; Mike retains authority for ratification and placement. The already completed evaluator repair and accepted Interpretation 002 are dependencies and context for this review. [R1 §5; P2 §§1–4; X, declaration and readings; §6 below.]

This review establishes neither a qualification result nor completion of runner/package integration. No scientific-stage job or stage-master draw was performed. All independent numerical execution used constructed arrays, fixed test keys or synthetic records. [P2, opening scope; X, module documentation; §8.]

### Direct answers to the six questions

| Question | Answer |
|---|---|
| **Q1 — Is D1 closed on every named route, with the point intact? Does the θ=.20 copy differ from the repaired evaluator?** | **D1 is closed.** No successful returned-record divergence was found for valid declared inputs on the ordinary declared-stream path. The documented additional preflight checks can refuse a damaged declaration that the evaluator alone does not consult; that distinction remains explicit. |
| **Q2 — Is the diff complete, and do the old identities reconstruct?** | **Yes.** All nine hunks reverse without offset or fuzz and recover the two exact round-1 SHA-256 identities. The complete source/test comparison finds only the changes disclosed in P2 §3. |
| **Q3 — Is the declaration entry sufficient, and what happens to M6B-2/3/4?** | **The entry is accurate and sufficient; all three are ACCEPTABLE.** The digest is not the only observable change: affected index causes are corrected, the source pin changes, and report envelopes carry the new declaration digest. No additional numerical or stream rule changes. |
| **Q4 — Does the new test discriminate, and what does it leave out?** | **It satisfies the required repair regression and discriminates independently of oracle equality.** It adds the small-complement cross. It does not exhaust reversed mixed-family orientation, malformed-input combinations or informative mixed-family bootstrap outcomes. Section 5 distinguishes those limits from the additional L2 probes and the carried M3 suggestions. |
| **Q5 — Do the earlier dispositions stand?** | **Yes.** The accepted calculations, original test bodies and seven readings are unchanged. The shared declaration metadata deliberately changes on enclosing reports. |
| **Q6 — Anything else?** | **No remaining blocker was established.** The two deferred cause-string changes, carried M3 test suggestions, source synchronization obligation and runner binding requirements remain recorded in §7. |

## 2. Receipt, identities and evidence boundary

### 2.1 Independent receipt and preservation

| Check | Result |
|---|---|
| Archive SHA-256 | `f63a181b9f7b57b18ff287a188007710737b30ebe30187d90494358b65d965e6` — matches Mike's supplied value. |
| Manifest-listed payloads | **89**, all independently hashed and matching MANIFEST.txt. |
| ZIP regular files | **90**, including MANIFEST.txt; no directory entries. |
| Inventory and ordering | No duplicate, missing or unlisted payload path; ZIP payload order equals manifest order. |
| MANIFEST.txt SHA-256 | `84b2170393f14f0d2da98e2647cedf0763a1ef048e8eaaf891e6c73acc4dad50` |
| Preservation after execution | All 89 extracted payload hashes still match; the packet still contains exactly its 90 regular files. |
| Frozen contract SHA-256 | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` |
| Received M6B round-1 review SHA-256 | `31fd32e258482f81d3fc8762271fc4f722ac69d6ae77a73a97b30fb7c58dd78f` |
| Complete M6B round-1-to-round-2 diff SHA-256 | `fa87500ebf6074b530c9387084ee8c4f2717e03930eb354653bfa598b4725116` |

The receipt was returned before execution authorization. This review answers D1 in the review of archive `6a00972c7a753d420b6a2e3724b209355e63723051b7067cd6b0e53e3f9ebc19`. It is the second review of **M6 part 2**, distinct from the previously completed M6 part-1 and Interpretation 002 reviews. [P2, opening identity and §1; R1, scope.]

P2 reports repository pin `ff136d70b1c6862b52d0cca270e1163c5c0e5a63`, with the evaluator repair placed at `7a1094ad3e62d51142712243b9a3be1a89e311ca`. I verified the packet bytes, included pins and internal lineage. I did not fetch the remote or independently attest to the repository's current head. The accepted dependency review and placement evidence were inspected within that boundary. [P2 §1; EP.]

### 2.2 Source key

All paths in this table are relative to **flights/mfa_fidelity/** inside the reviewed archive, except the two old-file copies explicitly identified in §3.

| Key | Source |
|---|---|
| **P2** | build_records/L1_TO_L2_F9_M6B_ROUND2_RESPONSE_2026-11-24.md |
| **R1** | build_records/L2_F9_M6B_ROUND1_REVIEW_2026-11-23_RECEIVED.md |
| **X** | instrument/mfa_instrument/f9/evaluator_reports.py |
| **T** | instrument/tests/test_f9_m6b.py |
| **E** | instrument/mfa_instrument/f9/evaluator.py |
| **O** | instrument/mfa_instrument/f9/outcomes.py |
| **C** | contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md, read with FLIGHT_9_FREEZE_RECORD.md and its addendum |
| **Δ** | build_records/f9_m6b_round1_to_round2.diff |
| **ER** | build_records/L2_F9_EVALUATOR_PRECEDENCE_REPAIR_ROUND1_REVIEW_2026-11-23_RECEIVED.md |
| **EP** | build_records/F9_EVALUATOR_PRECEDENCE_REPAIR_PLACEMENT_NOTE_2026-11-23.md |
| **I002** | rulings/F9_INTERPRETATION_002_FIDELITY_SUMMARIES.md |
| **REPRO** | build_records/f9_m6b_round1_d1_routes_after_repair.py |
| **MUT** | build_records/f9_m6b_mutation_check.py and f9_m6b_mutation_check_round2_2026-11-24.txt |

Function and section references below identify the relevant evidence in those exact received files. Independently executed results are reported in §§4, 5 and 8.

## 3. Q2 — Complete change and inverse reconstruction

I copied the two round-2 files to isolated scratch and reversed Δ with `patch --reverse --batch --fuzz=0 -p1`. All nine hunks applied with **no offset and no fuzz**. The reconstructed files match the supplied packet_only/round1/ copies byte for byte:

| File | Reviewed round-2 SHA-256 | Reconstructed round-1 SHA-256 |
|---|---|---|
| evaluator_reports.py | `9c60717553a8419fd248f587845499792e79c73b97f5728f662ab1ca58521606` | `7978581182a64f77682facdc573c55ea2356077d6d6bddb935cbac5d13d1e393` |
| test_f9_m6b.py | `e279ca0647519a3dff990a69d3c0cadc4dfbcbf86df560910c35d639d0875463` | `697d4e2a7425af6badb2170a36ddb6b4ed600be807c8820ed64f7265ff9ad53e` |

Those old hashes also equal the identities declared in P2 and recorded in R1. The reconstruction therefore checks the change against identified earlier bytes, rather than accepting a description of what was intended to change.

### Hunk audit

| Hunk | Change | Assessment |
|---:|---|---|
| 1 | Documents the wrapper's existing extra preflight and the corrected constant-family precedence. | Matches P2 §3's Q1 note and repair item 2. |
| 2 | Corrects the skeleton/T0 cause description. | Matches the repaired dependency and the frozen precedence. |
| 3 | Updates the deferred fidelity-module paragraph to cite accepted I002 and its skeleton-stream dependency. | Context update; no calculation or stream change. |
| 4 | Adds the single unavailable-precedence declaration entry. | Accurate description of the repair. |
| 5 | Updates the report declaration digest. | Exactly the digest consequence of that added entry. |
| 6 | Exchanges the empty-family and noninformative-map branches. | The sole source-function logic change. |
| 7 | Adds one regression test covering the requested routes and crossed states. | Assessed in §5. |
| 8 | Updates the comment identifying the placement pin. | Accurate within the supplied placement record. |
| 9 | Updates the evaluator source pin to the separately repaired bytes. | Matches the actual evaluator in this archive. |

The structural comparisons support the textual audit. **Twelve of thirteen source functions are byte-identical**; only evaluate_level_at changes. Exchanging those two branches in the old function's syntax tree makes it equal to the new function's normalized tree. **All thirteen original test definitions and all eight existing helper/fixture definitions are byte-identical.** The added regression is the only new function in the test file. Removing that test and restoring the old pin makes the remaining test-module syntax identical. [Δ; X; T; independent inverse and structural comparisons.]

The seven-reading block is verbatim unchanged. Of fourteen PLACED pins, only evaluator.py changes; the other thirteen pins and the aggregate non-f9 digest remain unchanged. The complete comparison found no edit outside the hunks or outside P2 §3's stated scope. This is consistent with retaining the accepted round-1 calculations while revising their common declaration metadata. [T, PLACED and UNTOUCHED; X, declaration and readings; R1 §5.]

## 4. Q1 — Closure of the precedence defect

### 4.1 Why the branch exchange is sufficient

The frozen level precedence puts apparatus failure first, constant index second, empty/full region third and under-resolution fourth. Its qualification explanation independently requires a constant index's cause to be independent of the sample. The repair implements that existing requirement. [C §7, L1–L4; C §6.2, row-15 explanation.]

The wrapper still validates declarations, θ, counts, families and the key before producing a returned scientific/unavailable record. It computes the point record before entering the per-index loop. Within that loop, it now tests `len(fam) == 0` before examining the point's informative flag. The point dictionary is not rewritten. [X, verify_evaluator_reports_declaration and evaluate_level_at.]

The old and new branches can differ only when **both** the family is empty and the point is noninformative:

| Family | Observed point | Round-2 index treatment | Effect of repair |
|---|---|---|---|
| Empty | Noninformative | Not informative, `no eligible contour`, not resampled | Corrects D1's former map-dependent cause. |
| Empty | Informative | Same constant-index unavailable record | Already correct in round 1. |
| Nonempty | Noninformative | The appropriate empty/full or under-minimum map cause, not resampled | Unchanged. |
| Nonempty | Informative | Enters the existing evaluator draw procedure | Unchanged. |

The applicable draw set remains exactly the nonempty families at an informative point. Consequently, the branch repair does not add resampling to a constant index, alter draw counts for an eligible sibling, change the point fit or move the support-count decision boundaries. With two empty families, no resampling occurs. With one empty family, the sibling follows its own eligibility and draw result. [X, evaluate_level_at; E, evaluate_level.]

Both outputs of reported_thresholds call the repaired wrapper. skeleton_boundary remains a direct call to the repaired placed evaluator, using all 40 supplied maps at the registered θ and its existing skeleton key. No separate cause rewrite or second skeleton implementation has been introduced. [X, reported_thresholds, skeleton_level_key and skeleton_boundary.]

### 4.2 Original witness and expanded route regression

I independently reran REPRO, which converts R1's Appendix R into the prescribed equality check. All twelve original state/route combinations now give both indices:

~~~python
{"result": "not informative", "cause": "no eligible contour", "resampled": False}
~~~

The diagnostic point still reports the map. The complete local output is byte-identical to the supplied repaired-route output, SHA-256 `6dcb67d0460c778e37f855736fbd71b5d7ad268642a80e9d5467fab053c4c72e`. This equality is the result of a fresh execution.

The new test extends those checks to four states and five routes: placed θ=.20, copy θ=.20, skeleton θ=.20, and reported θ=.10 and .30. The independent geometry expectations are:

| Constructed map | θ=.10 cells / bonds | θ=.20 cells / bonds | θ=.30 cells / bonds |
|---|---:|---:|---:|
| All counts zero | 0 / 0 | 0 / 0 | 0 / 0 |
| All counts 1,000 | 10,000 / 0 | 10,000 / 0 | 10,000 / 0 |
| Counts 1,000 only on the 6 × 6 patch at [10:16, 10:16] | 64 / 32 | 60 / 32 | 52 / 32 |
| Full map with that patch removed | 9,984 / 16 | 9,984 / 16 | 9,984 / 16 |

Both empty families receive the constant-index cause on all twenty combinations. Mixed-family checks retain that cause for constant P while nonconstant H receives the appropriate map cause. Ordinary TB-family controls retain their map causes. The full-record equality assertions compare the θ=.20 copy with the repaired evaluator, including nested records and array contents. [T, new regression and _same; independent full-suite execution.]

### 4.3 Additional checks of point preservation and apparatus priority

Four additional constructions—a narrow periodic strip, an informative half-strip, two separated patches and a uniform count-200 map—were passed through the copy, skeleton and both reported thresholds. All sixteen route results retained the exact constant-index record. Each point record matched direct map evaluation at its own threshold, and the input bytes remained unchanged. The uniform map is full at θ=.20 and empty at θ=.30; its point correctly changes while the index cause stays fixed. [Independent probes; X, evaluate_map_at and evaluate_level_at.]

Five malformed-count constructions were also tested with constant families through the placed evaluator, copy, reported-threshold wrapper and skeleton wrapper: wrong shape, floating counts, a negative count, a count above 1,000 and an overflowing unsigned value. **All twenty calls raised F9EvaluatorError.** None returned a scientific/unavailable record in place of an apparatus-input rejection. The branch swap therefore preserves the priority of validation. [Independent probes; E, check_counts; X, evaluate_level_at and skeleton_boundary.]

### 4.4 Constant index beside an unstable sibling

A further construction exercised the path omitted by the new regression's noninformative maps. Its forty seed maps comprise twenty-one maps with count 400 on half the lattice and nineteen zero maps. The mean has 4,800 occupied cells and 200 bonds at θ=.20. A synthetic mixed family contains empty P and a nonconstant H with one contour. The observed point is informative, so H actually enters the full 1,000-draw procedure.

| Route | P record | H: compatible / adverse / invalid draws | H result |
|---|---|---:|---|
| Placed θ=.20 | Constant-index record, not resampled | 684 / 0 / 316 | Not informative; unstable edge |
| Copy θ=.20 | Identical P record | 684 / 0 / 316 | Identical full record to placed |
| Skeleton θ=.20 | Identical P record | 673 / 0 / 327 | Not informative; unstable edge |

The different skeleton counts follow its separate declared key. The constant index is excluded from the applicable bootstrap set and remains intact when the sibling becomes unstable. An empty-family index cannot itself reach the unstable-edge branch.

For reproducibility, the nonconstant comparison array is zero except `omega[1:49, :] = 1`; it is wrapped as H's synthetic IndexFamily. Counts are zero except `counts[:21, :50, :] = 400`. The keys use test master 777, TB.H and level 1,000,000 micro-units; the skeleton key appends its object code through skeleton_level_key. This is engineering test geometry, not a declared mixed-family terrain arm. It supplies no authorization to bind such a record as canonical TB. [Independent probe; P2 §5.1; EP, discussion of M4's existing guard.]

### 4.5 Equality and the documented preflight distinction

I found no valid-input successful-record counterexample to θ=.20 equality. A structural comparison of the two level functions gives nineteen identical normalized body statements after accounting for the disclosed θ threading, E namespace, report preflight, local resample-count alias and the evaluator's optional constructed-resample argument. At the registered θ, the occupied-region arithmetic is the same. The full supplied suite retains the informative-map and two-family equality checks. [X, occupied_region_at, evaluate_map_at and evaluate_level_at; E, corresponding functions; T, equality and scaling tests.]

The equality claim concerns the ordinary declared-stream path. The evaluator additionally accepts deliberately constructed multiplicities for its qualification interface; this wrapper does not expose that argument. The wrapper also checks outcome and stream declarations through its own preflight. In isolated memory-only checks, corrupting either declaration made the three M6B routes refuse while the evaluator alone still returned its original valid constant-family record. Restoring the declarations restored successful wrapper equality. This confirms P2's corrected admission-domain disclosure. It does not produce two different successful records for the same valid declared inputs. [P2 §3, Q1 note; X, module documentation and verification function; independent preflight checks.]

## 5. Q4 — Regression discrimination and coverage limits

The new test meets every element of R1 §2's required item 3: constant family crossed with empty, full and under-minimum maps; all five evaluation/report routes; mixed constant/nonconstant families; and ordinary nonconstant controls. The small-complement construction adds coverage beyond the original three maps. Its expected constant-index record is written independently of the evaluator's result, so a shared oracle error is no longer sufficient to make this test pass. [R1 §2, Required repair; T, new regression.]

### Independently checked mutations

I inspected MUT, extracted only its two new mutations and ran the unchanged new regression in isolated copies. Packet source files were not edited.

| Isolated case | Independent result | Meaning |
|---|---|---|
| Unmodified round-2 source | 1 passed, 13 deselected | Baseline succeeds. |
| Restore the old precedence behavior | Expected assertion failure on the empty map through the θ=.20 copy | Detects recurrence of D1. |
| Give an ordinary no-edge index the constant-index cause | Expected assertion failure for H in the mixed-family empty-map case | Detects an overbroad correction. |

Both failures occurred at semantic assertions in the new test. They were not import, collection, declaration-digest or pin failures. The complete 27-mutation campaign was inspected but not rerun; its reported 26/27 result remains L1 evidence. The documented surviving inclusive-band mutation remains equivalent on the four declared TD bases. [MUT; independent isolated executions; R1 §§4 and 7.]

### What the new function does not cover

The test is sufficient for the requested contained repair, but its name should not be taken as an exhaustive Cartesian coverage claim:

- It uses **P constant/H nonconstant** for the mixed case. It does not separately reverse the orientation to H constant/P nonconstant. The implementation branches generically over families without a P/H-specific case.
- Its four mixed-family maps are noninformative. It does not itself exercise an informative mixed point whose sibling proceeds to compatible, adverse, unresolved or unstable bootstrap output. Section 4.4 independently checks the unstable-sibling case for the placed evaluator, θ=.20 copy and skeleton route.
- It does not add a full malformed-input cross across the public report routes. Existing tests already reject float counts and an invalid key with constant families on the copy; section 4.3 adds independent shape/range/type probes across the routes.
- It independently asserts point noninformativeness, occupied-cell counts and bond counts, but not every exact point-reason string. The unchanged point-building code, full-record equality, REPRO's output and the direct-map comparisons establish preservation in this review.

These limits do not establish another defect. The corresponding broader M3 suggestions were already classified as nonblocking and carried to that test file's next touch. The present packet adds the small-complement cross to M6B; it does not silently complete or remove the outstanding M3 suggestions. [EP, carried tests; P2 §5.3; T, new regression and existing unavailable-state test.]

## 6. Q3 and Q5 — Declarations and standing dispositions

### 6.1 Declaration identity

The new entry states:

> an empty family first (no eligible contour), then a non-informative map's cause: contract section 7, L2 above L3 and L4

That is an accurate statement of returned-cause precedence after apparatus validation. It does not move a scientific unavailable state ahead of corrupt-input rejection. Independently recomputing the declaration gives:

`a9227f81c1b088dfdcd86d625747b3b2c26323cf25c3092cbc4d4e6fe071e979`

Removing only the new unavailable_precedence entry recovers the exact old digest:

`f3fe3fcf1954bb6addd18e94a793593490fef18cb77910f94dda1c25b799337e`

No other declaration entry changes. The evaluator's own declaration digest remains `79e93ccade624ec473c7c60225183458e0ed168e13c4e23fb7dbaa6ed2d2fef7`. Its source identity is correctly pinned to `ddfa49b11955de42d5b6638d892af4c75756ff6b1b5f35ea0884c4de7b2a07a1`. The previous source pin was `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc`. [X, declaration; T, PLACED; EP; independent digest checks.]

The intended observable consequences extend beyond the digest: index causes change in the D1 states, and every enclosing report using this declaration carries its new digest. Record shapes, thresholds, step-4 minima, ε, m, streams, key construction, support counts and scoring rules do not change. It would therefore be inaccurate to promise whole-record byte equality between old and new enclosing reports merely because their numerical calculation is unchanged.

### 6.2 All nine declarations

| Declaration | Round-2 disposition | Basis |
|---|---|---|
| **M6B-1 — criterion at θ** | **ACCEPTABLE; standing** | Exact integer criterion, included ties and accepted θ values unchanged. |
| **M6B-2 — orchestration copies** | **ACCEPTABLE; D1 repaired** | Correct per-index order, preserved point record and validation, full-record θ=.20 equality, explicit preflight disclosure. |
| **M6B-3 — reported thresholds** | **ACCEPTABLE; D1 repaired** | Both thresholds now receive corrected records; thresholds and shared realization stream unchanged. |
| **M6B-4 — skeleton boundary** | **ACCEPTABLE; D1 repaired** | Unchanged all-40 delegation receives the repaired evaluator's causes; registered θ and separate skeleton key retained. |
| **M6B-5 — component coverage** | **ACCEPTABLE; standing** | Component and distance calculations byte-identical; existing tests pass. |
| **M6B-6 — design margins** | **ACCEPTABLE; standing** | Geometry, constants and table assertions unchanged; existing tests pass. |
| **M6B-7 — persistence assembly** | **ACCEPTABLE; standing** | Required arms, placed persistence records and incompleteness treatment unchanged; existing tests pass. |
| **M6B-8 — records** | **ACCEPTABLE; standing** | Record structures unchanged; common declaration metadata intentionally updated. |
| **M6B-9 — readings** | **ACCEPTABLE; standing** | All seven readings verbatim unchanged and consistent with the repair. |

[R1 §5; Δ; X; T; independent full-suite execution.]

The seven readings retain their previous classifications: the common realization stream is an accepted build declaration; whole-rule skeleton evaluation is the substantive reading already supplied as Mike's acceptance; the separate skeleton stream is a prospective build declaration; every-component quantiles and use of the fit's reported contour clarify the explicit report content; strict design-band bounds and the fifteen-arm skeleton-high panel remain build declarations. No new contract ruling is needed to enforce the existing cause precedence. [R1 §5; X, readings.]

The earlier limitations also stand. Component-coverage point diagnostics are not index-level outcomes. Design-table assertions do not authenticate a whole base array. Partial persistence reports retain the placed function's limitations and cannot be called complete. Encoding the NumPy-bearing evaluation records and binding inputs to their runs remain runner obligations. [R1 §§4–6; X, module documentation and report functions; C §§5.7–5.9.]

## 7. Q6 — Dependency boundaries and carried items

The separate evaluator repair is closed context for this review. Its received review identity is `009a86f178f31021d91cd334bf7bf03a9d504e1985d79b2ee6b5f7c351daa944`; its included repaired source matches the new pin. This review checks that M6B follows that accepted dependency. It does not reopen the separate review or purport to repeat its complete validation. [P2 §1; ER; EP.]

I002, identity `be9fae842c04e9088e47a0c398db78c88ab93bd208e4b7a5c13149cfb5f7636e`, records Mike's acceptance on 2026-11-24. The docstring's new reference accurately assigns those fidelity summaries to a third module and carries forward its dependency on the accepted M6B skeleton stream. The interpretation explicitly requires the ultimately accepted declaration and source identity to be bound before output. It does not bind obsolete in-review bytes or import its expanded fidelity-summary draw applicability into these §1.3(f) threshold reports. [I002, authority, Point 8 and Consequences; X, NOT HERE paragraph.]

The following items remain carried:

| Item | Status after this round |
|---|---|
| Literal causes `no edge at theta` and `below the informative minimum` | Still deferred by Mike's explicit ruling. This repair changes priority, not those strings or their translation in O. |
| Additional M3 regression suggestions | Still carried to the next touch of test_f9_m3.py. Independent L2 probes here do not change that committed test file. |
| Duplicated orchestration | Still a maintenance obligation. Future evaluator changes must be reflected and checked in the copy, with independent cause expectations as well as equality tests. |
| Runner/package integration | Still owns authenticated input binding, persisted encoding, coverage/validity accounting, §5.9 completeness/readiness and job records. |

[P2 §5; EP, deferred and carried items; R1 §§6–7; C §§5.7–5.9.]

The mixed-family construction remains explicitly synthetic. On the declared terrain families, T0 has two empty families and the other terrains have nonempty families. The existing outcome guard can refuse a constant-family result falsely bound to a non-T0 terrain. Preserving that guard is consistent with the repaired cause exposing the bad binding; this review authorizes no workaround. [P2 §5.1; EP, M4 consequence; O, level_from_evaluation.]

No additional repair request or substantive interpretation choice is required by this round.

## 8. Verification record

### 8.1 Independently executed

The local environment was **Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and pytest 9.2.0**. The full M6B suite ran from the received instrument directory, with task-local pytest on PYTHONPATH, bytecode writing disabled, pytest plugin autoload disabled and its cache provider disabled:

~~~text
python3 -B -m pytest tests/test_f9_m6b.py -v -p no:cacheprovider --durations=14

14 passed in 163.05s (0:02:43)
~~~

The new precedence regression's call took 0.10 seconds in this run. The test log's SHA-256 is `f859337ea790f3bba717b326146572a4132b241491733a31626c358cc05f9330`. This timing describes this test execution; it is not a canonical resource benchmark.

| Independent check | Result |
|---|---|
| Archive, inventory and all payload digests | Exact match; all packet bytes still match after execution. |
| Reverse patch and byte comparison | Both round-1 source/test identities recovered with no fuzz or offset. |
| Structural change audit | Sole source-function logic change is the branch exchange; original thirteen tests and eight helpers unchanged. |
| Declaration and dependency pins | New and old declaration digests verified; only the evaluator source pin changes. |
| Full M6B suite | 14 passed. |
| Original repaired witness | All twelve route/state combinations correct; output matches the supplied repaired transcript byte for byte. |
| Extra constant-family maps | Sixteen route results correct; point records and input bytes preserved. |
| Malformed counts with constant families | Twenty calls reject as apparatus-input errors. |
| Mixed informative point and unstable sibling | Constant record retained; θ=.20 copy equals placed; skeleton follows its distinct key. |
| Additional preflight checks | Damaged outcome/stream declarations refused by the report routes; restoration returns them to agreement. |
| Two new mutations | Both caught by the intended semantic assertions. |

### 8.2 Inspected supplied evidence

The following are supplied records, distinguished from the independent executions above:

| Supplied record | Reported result |
|---|---|
| f9_m6b_module_container_round2_2026-11-24.txt | L1's module run: 14 passed in 181.98 seconds. |
| f9_m1_to_m6b_container_round2_2026-11-24.txt | L1's combined seven-file run: 291 passed in 988.40 seconds. |
| f9_m1_to_m6_canonical_2026-11-24.txt | Canonical six-file dependency run: 277 passed in 1060.87 seconds. |
| f9_m6b_mutation_check_round2_2026-11-24.txt | L1's complete campaign: 26 of 27 mutations caught, with the disclosed equivalent design-band mutation surviving. |

These files are under build_records/ and were included in the verified manifest. I did not rerun the complete seven-file suite or all twenty-seven mutations. The full M6B suite, exact change reconstruction and focused adversarial checks resolve the concrete risk of this contained repair without representing the supplied broader logs as new L2 runs.

No packet file was edited. Mutations, inverse reconstruction and in-memory preflight changes were confined to isolated review work and restored or discarded there. No probe output was opened, no lattice dynamics were run, and no calibration, qualification, canonical census or scientific-stage job occurred.

## 9. Closure

The identified D1 repair is complete in the submitted M6B source and its reviewed dependency relationship. The new test closes the specific shared-oracle gap that allowed the original error to pass. The exact inverse reconstruction, independent execution and unchanged accepted calculations support acceptance of these round-2 bytes, with the existing carried items and integration boundaries preserved.

FINAL VERDICT: SOUND
