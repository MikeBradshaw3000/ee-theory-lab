# L2 — Flight 8 M-P1 Round 2 Review

**Date:** 2026-10-29  
**Register:** Instrument build review under frozen Contract F8 v0.8.4  
**Response reviewed:** `L1_TO_L2_F8_MP1_ROUND2_RESPONSE_2026-10-29.md`, `aef176cb818cc90a`  
**Archive reviewed:** `f8_mp1_round2_L2_v2.zip`, 46 regular files  
**Verdict: DEFECT-WITH-REPAIR — one evidence item remains open (V1).**

**The D1–D7 implementation repairs are accepted. No remaining source defect was found in this scoped round-2 review.** The requested module passed **35 tests in 69.35 seconds**, exit 0. MP1-3's repaired construction and the new MP1-7 reporting convention are accepted. The identified D4 interpretation satisfies all three required points and covers both relevant contract clauses.

The sole blocking item is documentary: **the complete corrected known-answer JSON named by the response and amended packet is absent from the archive.** The round-1 review expressly required that record after the generator and census-binding repairs. The 35-test result and focused checks establish the repairs; they do not establish execution of the complete corrected 900-case corpus.

This is an evidence hold, not a demand for another source redesign. D5's implementation repair is closed; its renewed full-run evidence requirement remains open as V1. Placement clearance remains withheld until V1 is resolved. No canonical scientific job is authorized by this review.

## 1. Scope and byte identity

The review authority is the supplied frozen contract, its freeze record and Appendix A, the round-1 review as received, and Mike's identified D4 interpretation. This round examines the stated D1–D7 repairs, their discriminating regressions, the round-1 §6.3 follow-up items, MP1-3, and MP1-7. It does not reopen unrelated placed modules or add new scientific criteria.

Archive SHA-256:

`7f0c45475b3de3a3c5a65003619abc5ac8770109db30427e1a9d3003be7323cd`

Reference keys below use paths relative to `flights/mfa_fidelity/`. Prefixes contain the first 16 SHA-256 hexadecimal characters.

| Key | File | SHA-256 prefix |
|---|---|---|
| R2 | `build_records/L1_TO_L2_F8_MP1_ROUND2_RESPONSE_2026-10-29.md` | `aef176cb818cc90a` |
| P2 | `build_records/L2_F8_MP1_BUILD_PACKET_2026-10-29.md` | `a7c5c60b25e53b16` |
| R1 | `build_records/L2_F8_MP1_ROUND1_REVIEW_RECEIVED.md` | `1a9dd1a2980847c5` |
| I001 | `rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c` |
| E2 | `instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db3` |
| T2 | `instrument/tests/test_f8_mp1.py` | `f9abdd8e657ba917` |
| C | `contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f` |
| F | `contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139` |
| A | `contracts/flight8/APPENDIX_A_OF_RECORD.md` | `94d527624beafa7c` |
| D | `instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8` |
| CL | `instrument/mfa_instrument/f8/closure.py` | `9452dd11396350ab` |

Full identities of the changed source and its declaration:

```text
evaluator.py
61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a

test_f8_mp1.py
f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d

Evaluator declaration, independently recomputed from repr(EVALUATOR_DECLARATION)
cc1f176eb12dde347351f77ddf661dfa7fdb6f9662d83be28906155687a5d86f
```

The computed declaration digest equals the source literal. The new convention is included in the declaration and checked against its live value.

Direct comparison with the round-1 archive found exactly three changed common files: the build packet, `evaluator.py`, and `test_f8_mp1.py`. Three files were added: the response, the received round-1 review, and the D4 interpretation. No prior member was removed. The included round-1 review is byte-identical to the review delivered by L2.

The frozen contract, freeze record, Appendix A, M1/M5 dependencies, configuration, and all supplied E1 files are byte-identical to their round-1 counterparts. After execution and inspection, all 46 submitted files still matched their archive bytes. The reported repository placement commit was not independently retrieved; these are archive-to-archive and archive-to-extracted-file checks.

## 2. Test execution

From the extracted `flights/mfa_fidelity/instrument` directory:

```console
python -m pytest tests/test_f8_mp1.py -q
...................................                                      [100%]
35 passed in 69.35s (0:01:09)
```

**Exit code: 0.** The isolated dependency directory prepared for round 1 was supplied through `PYTHONPATH`. The submitted test file and production source were unchanged.

| Environment item | Observed value |
|---|---|
| Python | 3.12.14 |
| Platform | Linux x86_64, glibc 2.39 |
| NumPy | 2.3.5 |
| pytest | 9.2.0 |
| pyarrow | 26.0.0 |

SHA-256 of the captured output:

`ed28d471775c05df031b6f00cff1a4989e5ad343ce96aec61520be7963dca337`

The source review was supplemented by focused checks of repaired branches, including observation identity, late extinction through actual M1 summary code, the corrected steep rise, and the real qualification gate with controlled outputs. Constructed records and forced trajectories are diagnostic fixtures, not M7-issued scientific evidence. Controlled-output gate checks are not 900-case corpus executions.

## 3. Disposition of D1–D7

### D1 — Frozen publication and Δm enforcement: CLOSED

`evaluate_p1` no longer accepts `delta_m`. It validates the supplied or default publication through M5's replay validator before the structural tests and reads Δm only from that validated publication. The same path serves both synthetic and canonical roles. [E2:451–470]

The regression tests the original two bypasses directly: an override keyword raises `TypeError`; altered publications are refused with either stale or recomputed identities. The one-spacing case passes, the two-spacing case fails with `hysteresis`, and the operative test bracket agrees with the fidelity record and publication. [T2:198–209]

The primitive `t_s2` still takes a bracket argument so its arithmetic can be tested independently. The relevant invariant is that the evaluation entry point always supplies the validated frozen value. This is satisfied; the primitive's existence does not recreate the entry-point bypass.

### D2 — Continuity for nonpositive endpoint range: CLOSED

The shared predicate now reads:

```python
if d > 0.0 and d > F_J * rng:
```

Every positive increment is tested even when the endpoint range is zero or negative; non-increases stay under the reversal rule. This is the exact repair required in round 1. [E2:300–322]

The regression contains the 0.300/0.305 bump, zero and negative skeleton endpoint ranges, the zero-range realization, constant and only-decreasing controls, and full propagation to `NOT DISTINGUISHED`, with no scientific FAIL. [T2:145–165]

An additional focused negative-range realization check also returned the required continuity ND at 1.423913, with increase `0.0050000000000000044` and threshold `-0.0002500000000000002`. The supplied regression is therefore supported by inspection of the common code path and an independently checked counterpart.

### D3 — Observation identity and recomputation: CLOSED

The repaired input path enforces the boundary requested in R1:

- Actual M1 `F8RunResult` objects, canonical specification reconstruction, and object/level/seed/stream checks.
- An `int64` active-count vector of the full production length, with values in range.
- A `float64` density vector of the same length, exactly equal to counts divided by cell count.
- Recalculated survival, tail mean, and window means using M1's count-grid arithmetic; cached summaries must agree.
- Absorbing continuation and first-extinction-tick checks for the skeleton.
- Per-run density identities alongside spec identities, and explicit replay validation when original run records and halt map are supplied. [E2:167–260]

The supplied tests discriminate against truncated traces, stale summaries, inconsistent density/count records, non-M1 objects, changed observations, and replay against changed records. The existing real-run construction test now performs both structural and replay validation. [T2:281–317]

A focused check changed a pre-tail count at tick 1000 while preserving every tail summary. The new density hashes and sweep identity changed; replay of the original sweep against the changed records was refused. Thus the identity binds the full recorded density observation, not merely the scored summaries.

This closes the demonstrated observation-integrity defect. It does not claim stochastic-trajectory replay or authentication by the specification hash alone. M7 continues to own authorization and issuance.

### D4 — Late extinction and interpretation: CLOSED

The interpretation record is accepted; its three points are assessed separately in §4 below. The implementation follows them. It removes the false requirement that positive tail mean implies survival and retains the true implication that survival implies a positive tail mean. Trace recomputation preserves pre-extinction activity and subsequent zeros. [I001; E2:167–191, 249–251]

The regression covers extinction before the tail, early inside the tail, inside the final window, and no extinction. It also rejects resurrection in an absorbing trace and an incorrect cached extinction tick. [T2:319–346]

To check the interface independently of the test helper's copied summary arithmetic, actual M1 `D.run` was exercised with only its step function replaced by deterministic trajectories. These were diagnostic substitutions, not stochastic experiments:

| First zero tick | M1 survival | M1 tail mean | Round-2 ingestion and replay |
|---:|---|---:|---|
| 1501 | False | 0.00 | Accepted |
| 2051 | False | 0.05 | Accepted |
| 2991 | False | 0.99 | Accepted |
| None | True | 1.00 | Accepted |

The early-tail example retains window means `(0.5, 0, …, 0)`. No whole-run zeroing or survivor-only averaging is introduced.

### D5 — Exact steep-continuous construction: IMPLEMENTATION CLOSED; full-run evidence held under V1

`steep_continuous_branch` leaves the boundary anchor unchanged, sets the first rise to `J = 2*f_J*R`, and distributes only the remaining range above the next level. The continuous interpolation is explicitly declared as piecewise linear. [E2:534–547, 578–580]

Direct evaluation gives:

| Quantity | Observed value |
|---|---:|
| Range R | `0.5193009605316091` |
| Declared first rise | `0.25965048026580456` |
| Actual first rise | `0.25965048026580456` |
| Rise divided by range | `0.5` |
| Endpoint difference | `-1.1102230246251565e-16` |
| Largest later rise | `0.03787363083690498` |
| Allowed ordinary rise | `0.12982524013290228` |

The regression checks the first rise, preserved endpoint within stated floating-point tolerance, monotonicity, absence of another excessive rise, and three generated continuity-ND outcomes with no FAIL. [T2:355–366]

**The source mismatch is repaired and MP1-3 is accepted.** The renewed complete qualification record required by R1 §8 is a separate evidence obligation, still open as V1.

### D6 — Declared synthetic census and actual counter: CLOSED

The qualification function validates the supplied census, refuses canonical-role input, compares the validated identity with the deterministic declared synthetic census, records that comparison, and requires it for passage. Alternative valid synthetic censuses remain usable for explicitly nonqualifying development records. [E2:613–641]

The regressions test the default census, an alternative valid census with s_hat 0.005, and refusal of canonical-role input. Crucially, the actual final gate is also exercised with every class/count/master setting otherwise correct and controlled correct outputs: the alternative census still cannot pass. [T2:377–403]

Focused checks of that same production gate gave:

| Controlled-output condition | Declared-census flag | Passage |
|---|---|---|
| Default census; every class 100 exact | True | True |
| Alternative valid census; every class 100 exact | False | False |
| Canonical-role census | Refused before qualification | — |

The independently constructed declared synthetic census on this environment has identity:

`c2ed98a5382bb1b8828cd527fd2d1b6e7492a94bdfb80f758528aeb4eec099e2`

This verifies the census-binding repair. It does not verify the absent development record's claimed census identity or its 900 actual outcomes.

### D7 — Explicit fidelity reporting: CLOSED

Density-comparison rows now retain the observations, both comparators, and the existing calibrated width while explicitly recording both signed residuals. Ratio reporting now identifies the actual denominator level, median and width; each numerator row records its median, ratio and width. Unavailable ratios carry a named reason. [E2:365–428]

The regression checks positive and negative residuals, the standard reference at **1.228261** for boundary **1.032609**, ratio arithmetic and component widths, four unavailability conditions, and unchanged four-test outcomes when fidelity agreement changes. [T2:233–256]

A focused check also exercised the fifth branch, where no level lies below the boundary-minus-Δm threshold: ratios were empty, the reason was explicit, and the available denominator record was retained.

P1 remains determined from the four test results before fidelity is attached. The new residuals, ratio components and edge diagnostic do not enter the decision. [E2:478–483]

## 4. D4 interpretation record: ACCEPTED

I001 has full identity:

`6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86`

It records Mike's ruling A, expressly binds **both §3.4 and §4.11**, and states all three requested points:

| Required point | Assessment |
|---|---|
| Mean over the entire declared tail, including zeros after extinction | Explicit in binding point 1; count-grid arithmetic and the full denominator are named. |
| Entirely inactive tail gives zero; late extinction can give survival False and positive mean | Explicit in binding point 2; the parenthetical shorthand is reconciled with the full-tail definition, and neither observable is coerced into the other. |
| Verify both measurements from the trace using placed M1 arithmetic, with extinction regressions | Explicit in binding point 3 and implemented/tested as recorded in D3/D4 above. |

The frozen contract's bytes and identity are unchanged, as are the placed M1/M5 arithmetic and Appendix A. The record directs M7 to carry its identity with governance. That later linkage remains an M7 obligation; it is not a reason to hold this interpretation's acceptance.

The ruling supplies the authority that was pending in the first round-2 delivery. D4 is therefore resolved in both interpretation and implementation.

## 5. Disposition of the round-1 §6.3 follow-up items

### (a) Clean above-sweep control — ACCEPTED

The above-sweep class retains an inactive skeleton but uses the ordinary realization branch. The unrelated realization continuity ND is removed, and the parameterized regression explicitly checks T-R1′ PASS. [E2:574–577; T2:368–375]

The resulting test vector is T-S1′ FAIL `no active phase in sweep`, T-S1c/T-S2 dependent ND because no boundary exists, and T-R1′ PASS. The final cause remains the intended no-active-phase cause. The dependent ND results are expected dependency records, not unwanted independent triggers.

### (b) Actual below-domain rise test — ACCEPTED AS A DIRECT DOMAIN TEST; two nonblocking text corrections

The revised test injects a real 0.2 rise at indices 2→3. It passes when the supplied domain starts at index 8 and yields continuity ND when the supplied domain starts at index 2. This discriminates the helper's domain selection and fixes the earlier no-op test. [T2:137–143]

Two descriptions should be corrected:

1. R2 names **1.130435** as the caught level. The actual rise and the test's correct assertion identify **0.543478**, the level at index 3.
2. The test comment says survival stays zero there, but its fixture sets 20 survivors at every level. Consequently, it is a direct test of a supplied domain index, not an end-to-end demonstration that T-S1′ located index 8 on that same fixture.

These do not expose a remaining source-domain defect and do not block source acceptance. Correct the response's description; the stale test comment should be synchronized when that file is next edited. No test-source edit is required solely to resolve V1.

### (c) Actual counter regression — ACCEPTED

The replacement regression passes controlled outputs through the actual qualification function and checks separate exact-match and wrong-cause counts. **95 exact plus 5 wrong-cause cases passes; 94 plus 6 does not.** It also verifies that an alternative census cannot qualify even when all controlled outputs are correct. [T2:389–403]

This directly fixes the earlier hand-written-row regression. Controlled outputs here are appropriate for isolating the counter and gate; they must not be described as actual 900-case generator outcomes.

### (d) Boundary-absent fidelity wording — ACCEPTED VIA EXPLICIT AMENDMENT

The amended packet's opening note expressly corrects the earlier blanket statement and makes the round-2 response govern where the retained body differs. R2 likewise states that boundary-independent realization comparisons and the steepest-ascent diagnostic are preserved. The regression verifies all 24 realization rows and an available steepest-ascent value when no skeleton boundary is found. [P2 opening amendment; R2 §6.3(d); T2:271–277]

The older body wording remains historically visible, but its supersession is explicit. The accepted behavior retains available evidence and marks only boundary-dependent fields unavailable.

## 6. Declaration rulings

### MP1-3 — ACCEPTED AS RE-PRESENTED

The repaired normalized first rise is exactly the declared `2*f_J*R` to the stated arithmetic precision, the endpoint is preserved up to floating-point roundoff, and the continuous construction is specified. D5's implementation condition is discharged. The complete corrected corpus execution evidence remains V1.

### MP1-7 — ACCEPTED

The convention reports the numerator and reference medians' **existing calibrated density widths separately**. It claims no propagated ratio interval, confidence coverage or covariance assumption. This matches the fields now recorded and supplies the limited reporting convention requested in D7. [E2:88–100, 122, 365–428]

The convention is declaration-bound and included in live identity checking; its tampering negative is part of the passing module. It introduces no P1 gate or new scientific threshold. MP1-4's prior condition that the actual ratio reference and uncertainty components be recorded is now discharged. The earlier acceptances of MP1-1, MP1-2, MP1-5 and MP1-6 stand.

## 7. V1 — Missing complete corrected known-answer record

**Status: OPEN — the sole blocking item.**  
**Authority:** R1 §8 and its D5 closure requirement; R2 test-record section; P2's amended known-answer result claim.

The response and amended packet name:

`F8_MP1_KNOWN_ANSWER_CONTAINER_2026-10-29.json`

P2 reports **900 cases, 813 seconds, every class 100/100 exact, zero cross-triggers, declared census bound, passed True**, and result identity prefix **`58b338861232b286`**. Those are reported claims. The corresponding record is not supplied.

Direct archive inspection found:

| Archive | Regular files | JSON members | Members containing “known” |
|---|---:|---:|---:|
| Earlier round-2 zip, `5061b47086e0a368` | 45 | 0 | 0 |
| Current round-2 v2 zip, `7f0c45475b3de3a3` | 46 | 0 | 0 |

The current archive's 46-file count is correct. Its three additions over round 1 are the response, received review and interpretation record. The promised JSON would be an additional file; it is not present under a different path or alternative JSON name.

Therefore this review cannot verify the complete corrected per-class outcomes, recorded census and source bindings, or claimed result identity. The source repair and the 35-test passage do not establish that separate execution claim. The full corpus was not independently rerun during this round-2 review.

### Required repair for V1

Supply the existing complete JSON record for the **exact source bytes reviewed here**, with its SHA-256 identity. It should expose or accompany enough metadata to verify:

- All nine named classes, 100 replicates per class, exact-match and cross-trigger counts, and the declared passage minimum 95.
- Master `520261028` and the corrected evaluator source/declaration identities.
- The actual census identity and `census_is_declared_synthetic = True`.
- The resulting passage value and complete result identity, including the reported `58b338861232b286…` identity if that is the record being supplied.
- The execution environment and source binding needed to distinguish the development run from another build or a controlled-output gate test.

The record need not be regenerated merely because it was omitted. If the stated record exists and binds the reviewed source, providing it is the repair. If it does not exist or belongs to different source, rerun the declared corpus against these corrected bytes and report the actual resulting identities and outcomes.

**No new source change is requested by V1.** The next review can be confined to the missing record and its bindings unless that evidence exposes a new substantive issue. The later M7-issued qualification of record, canonical suite and production-readiness prerequisites remain separate obligations.

## 8. Final disposition

**D1, D2, D3, D4, D6 and D7: CLOSED. D5: implementation CLOSED; full-run evidence remains V1.**  
**D4 interpretation: ACCEPTED. MP1-3: ACCEPTED. MP1-7: ACCEPTED.**  
**Requested test module: 35 passed, exit 0.**  
**Overall verdict: DEFECT-WITH-REPAIR — V1 evidence hold only.**

The repaired implementation is accepted within this round's scope. Final placement clearance awaits the omitted corrected known-answer record; the source repairs should not be reopened merely to supply it. This review authorizes no canonical scientific execution.
