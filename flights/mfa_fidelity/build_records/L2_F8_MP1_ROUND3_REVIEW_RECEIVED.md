# L2 — Flight 8 M-P1, round 3: receipt and V1 ruling

**Date:** 2026-10-29  
**Scope:** The omitted development known-answer record and its bindings; the associated response correction. This round supplements the accepted round-2 implementation review.

## 1. Receipt — six files

All paths in this table are relative to `flights/mfa_fidelity/` inside `f8_mp1_round3_L2.zip`. SHA-256 prefixes are 16 hexadecimal characters; full identities appear in §7.

| Received file | Bytes | SHA-256 prefix | Receipt finding |
|---|---:|---|---|
| `build_records/L1_TO_L2_F8_MP1_ROUND3_RESPONSE_2026-10-29.md` | 2,826 | `ffa500a098b3df45` | Matches the stated identity. |
| `build_records/F8_MP1_KNOWN_ANSWER_CONTAINER_2026-10-29.json` | 1,784 | `1dd9a61fc0fa1ea5` | Matches; the omitted record is received. |
| `build_records/L1_TO_L2_F8_MP1_ROUND2_RESPONSE_2026-10-29.md` | 10,381 | `5d1086dd6b27eec4` | Matches; the text change is checked in §5. |
| `build_records/L2_F8_MP1_ROUND2_REVIEW_RECEIVED.md` | 22,362 | `1ad8439d0e0a16f9` | Byte-identical to L2's delivered round-2 review. |
| `instrument/mfa_instrument/f8/evaluator.py` | 46,561 | `61179c7670ea8db3` | Byte-identical to the accepted round-2 source. |
| `instrument/tests/test_f8_mp1.py` | 34,102 | `f9abdd8e657ba917` | Byte-identical to the accepted round-2 tests. |

The archive contains exactly **6 regular files**. Its CRC check passes, and its inventory contains no duplicate member names, unsafe paths or symbolic links. Archive SHA-256:

`a1bf04470b9196f75a408dd56974e064cda6dbc0ad66bdcaa2a884852f5fdc26`

## 2. Verdict

**SOUND — V1 CLOSED.**

The supplied record satisfies every item of the round-2 review's §7 repair requirement. It supplies the complete declared nine-class qualification summary, binds the accepted evaluator source and declaration, identifies the declared synthetic census, carries the execution metadata, and has the expected qualification result identity. L2 independently recomputed the relevant identities and the passage predicate from the supplied fields. [R2 §7; R3 “The record”; Q3; E3 `KnownAnswerQualification`, `known_answer_qualification`]

**The V1 placement hold is lifted. No remaining defect or further repair is identified in this review's scope.** D1–D7 are closed, including D5's renewed development-corpus evidence requirement. The round-2 acceptances of the D4 interpretation, the §6.3 repairs, MP1-3 and MP1-7 remain in force; the earlier declaration acceptances also stand. [R2 §§3–8]

This is acceptance of the supplied development execution record and its checked bindings. The later M7-issued qualification of record on the canonical machine remains a separate contract obligation. [R3 “The record”; Q3 `role`; R2 §7]

## 3. Qualification record and passage

### 3.1 All declared classes and named causes are present

The JSON contains all nine classes exactly once, in the declared `KA_CLASSES` order. Each intended determination and cause prefix agrees with the corresponding return in the accepted `known_answer_case` implementation. Each row has **100 exact matches, 0 cross-trigger failures and 100 total cases**. [Q3 `per_class`; E3 `KA_CLASSES`, `known_answer_case`]

| Class | Intended determination | Required cause prefix | Exact / total | Cross-triggers |
|---|---|---|---:|---:|
| `pass_crossing_0.8` | PRODUCED | No cause | 100 / 100 | 0 |
| `pass_crossing_1.0` | PRODUCED | No cause | 100 / 100 | 0 |
| `pass_crossing_1.25` | PRODUCED | No cause | 100 / 100 | 0 |
| `fail_no_inactive_phase` | NOT PRODUCED | `no inactive phase in sweep` | 100 / 100 | 0 |
| `fail_no_active_phase` | NOT PRODUCED | `no active phase in sweep` | 100 / 100 | 0 |
| `nd_steep_continuous` | NOT DISTINGUISHED | `continuity unresolved at grid resolution` | 100 / 100 | 0 |
| `fail_hysteresis` | NOT PRODUCED | `hysteresis` | 100 / 100 | 0 |
| `fail_realization_extinct` | NOT PRODUCED | `realization extinct` | 100 / 100 | 0 |
| `nd_injected_reversal` | NOT DISTINGUISHED | `non-monotone at finite sample` | 100 / 100 | 0 |
| **Total** | | | **900 / 900** | **0** |

“Exact” follows the accepted counter's definition: the determination must match, and the cause must begin with the named prefix; for a passing class, the cause must be absent. A correct determination with the wrong cause is counted separately as a cross-trigger and earns no exact-match credit. Level-specific suffixes remain permitted by the cause-prefix rule. [E3 `known_answer_qualification`]

The requirement is **at least 95 exact matches in each class**, with the declared experiment settings. An aggregate total alone would not establish passage. All nine supplied rows meet that per-class requirement. The repaired steep-continuous class is included at 100/100, so the renewed full-corpus evidence requirement attached to D5 is discharged. [R2 §§3 D5, 7; Q3 `per_class`]

### 3.2 The complete qualification predicate recomputes to True

| Predicate component | Verified value |
|---|---|
| Master | `520261028`, equal to `KNOWN_ANSWER_MASTER` |
| Class set and order | Exactly `KA_CLASSES` |
| Replicates per class | `100`, equal to `KNOWN_ANSWER_SWEEPS` |
| Passage minimum | `95`, equal to `KNOWN_ANSWER_PASS_MIN` |
| Per-class exact matches | Every class has `100 >= 95` |
| Declared census binding | Received census identity equals the independently reconstructed default synthetic census identity |
| Recorded declared-census flag | Boolean `true`, consistent with the checked census identity |
| Recomputed passage | Boolean `true`, equal to the received `passed` field |

Thus `passed: true` and `census_is_declared_synthetic: true` are supported by the record's counts and checked bindings. They are not being accepted solely because the JSON asserts them. [Q3; E3 `known_answer_qualification`; L2 round-3 verification]

## 4. Source, declaration, census and result identities

### 4.1 Accepted source and live declarations

Both included Python files are byte-identical to the round-2 files. The JSON's evaluator source digest equals the SHA-256 of the received `evaluator.py` bytes. L2 recomputed the evaluator and closure declaration digests from their declaration tuples and ran `verify_frozen_identity()` successfully against the accepted implementation and retained dependencies. Both recomputed declaration identities equal the record's fields. [Q3; E3 `EVALUATOR_DECLARATION`, `verify_frozen_identity`; C2 `CLOSURE_DECLARATION`; L2 byte comparison]

| Binding | Verified SHA-256 prefix |
|---|---|
| Evaluator source | `61179c7670ea8db3` |
| Evaluator declaration | `cc1f176eb12dde34` |
| Placed M5 closure declaration | `11074edcacbe26d2` |
| Declared synthetic census | `c2ed98a5382bb1b8` |
| Qualification result | `58b338861232b286` |

### 4.2 Census independently reconstructed

L2 rebuilt the default declared census with `synthetic_census()` and validated it through M5's `validate_calibration_census`. Its role is `derived_provisional`, and its reconstructed content identity is:

`c2ed98a5382bb1b8828cd527fd2d1b6e7492a94bdfb80f758528aeb4eec099e2`

This equals the JSON's census field and the independently constructed identity recorded in round 2. The received evidence therefore binds the declared synthetic census required by the accepted D6 repair. [E3 `synthetic_census`; C2 `validate_calibration_census`; Q3 `census_sha256`; R2 §3 D6]

### 4.3 Result identity independently recomputed

L2 reconstructed the `KnownAnswerQualification` fields from the JSON, mapping `evaluator_declaration_sha256` to the dataclass's `declaration_sha256`. Recomputing the identity through the accepted method, and separately by serializing the identity payload with sorted keys and compact JSON separators, gives:

`58b338861232b2860e425060c75b4c2bd9a87e7691ef14d7793af0de34f24a11`

It equals the supplied complete `result_sha256` and extends the result prefix reported in round 2. [Q3 `result_sha256`; E3 `KnownAnswerQualification.identity`; R2 §7]

The two relevant digests have different scopes. The qualification result digest covers the qualification object's fields, including counters, settings, census binding and evaluator declaration. The JSON file digest covers the complete delivered envelope, which additionally includes the evaluator source digest, closure declaration, role and execution metadata. Both identities have been checked; neither is described here as an independent rerun of the historical execution.

## 5. Response correction and execution metadata

**The §5(b) text correction is accepted.** A direct diff against the received round-2 response shows that only the §6.3 paragraph changed. It now correctly identifies **0.543478, index 3**, as the level caught by the below-domain rise test, and identifies the fixture as an all-survivor, direct test of the supplied domain index. This matches the correction requested by L2. [R2 §5(b); R2a §6.3(b); E3 test companion `test_f8_mp1.py`]

The stale test comment is deferred until the test file's next edit, as the round-2 review expressly permitted. Its retention is not an open V1 defect and does not require changing the accepted test identity. [R2 §5(b); R3 “Text corrections”]

The JSON records the development execution environment as:

| Field | Recorded value |
|---|---|
| Platform | `Linux-6.18.44-fc-v185-x86_64-with-glibc2.39` |
| Python | `3.13.18` |
| NumPy | `2.5.3` |
| Elapsed time | `813.3` seconds |

The round-3 response explicitly corrects the older response's “Python 3.12” heading as a transcription error. The correction and the JSON agree. These are L1's reported historical execution metadata; L2's current identity and census checks ran with Python 3.12.14 and NumPy 2.3.5. [Q3 execution fields; R3 “The record”; L2 round-3 verification]

## 6. Verification scope and disposition

This round checked the archive receipt, byte equality with the accepted source and tests, the received prior review's identity, the response diff, the nine qualification rows and named expectations, all qualification settings, the declared-census comparison, the live declarations, the passage predicate and the complete result digest.

**L2 did not rerun the 900-case corpus or repeat the unchanged 35-test module in round 3.** The record is accepted as the supplied development execution evidence. Round-2 review §7 explicitly allowed the existing record to be supplied without regeneration when it belonged to the accepted source; that condition is now satisfied. [R2 §7; R3 “The record”]

The prior independently observed module result remains **35 passed in 69.35 seconds, exit 0**, for the byte-identical evaluator and tests. Its retained log SHA-256 is:

`ed28d471775c05df031b6f00cff1a4989e5ad343ce96aec61520be7963dca337`

[R2 §2 and retained L2 module log]

| Item | Round-3 disposition |
|---|---|
| V1: omitted corrected known-answer record | **CLOSED** — received and verified against the specified requirements |
| D5: renewed complete development-corpus evidence | **DISCHARGED** through V1 closure |
| D1–D7 implementation repairs | **CLOSED** — round-2 acceptance stands |
| D4 interpretation record | **ACCEPTED** — round-2 ruling stands |
| §6.3 items | **ACCEPTED** — the requested response correction is now supplied |
| MP1-3 and MP1-7 | **ACCEPTED** — round-2 rulings stand |
| Other MP1 declaration rulings | Prior acceptances stand |
| Remaining defects or repairs in this scope | **None** |
| Overall M-P1 review verdict | **SOUND** — prior V1 placement hold lifted |

M7's canonical qualification and apparatus prerequisites retain their separate jurisdiction. The present disposition closes L2's M-P1 review for the identified source and declaration. [R2 §7; R3 “The record”]

## 7. Full identity register and source key

### Received files

```text
L1_TO_L2_F8_MP1_ROUND3_RESPONSE_2026-10-29.md
ffa500a098b3df45ae371a83d6194042039c885a260185faa06bafa4faf3ff3d

F8_MP1_KNOWN_ANSWER_CONTAINER_2026-10-29.json
1dd9a61fc0fa1ea59462b33c12b68cf0678ef8fb2870ad0cd4c2f8e56e19a997

L1_TO_L2_F8_MP1_ROUND2_RESPONSE_2026-10-29.md
5d1086dd6b27eec4c00fdeefe3bc81ca9fd19198a68657b9fd4f8efe0f25f892

L2_F8_MP1_ROUND2_REVIEW_RECEIVED.md
1ad8439d0e0a16f9c3ec1e94b9864b24df95e1e7a2cc610099ca8498bee4f460

evaluator.py
61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a

test_f8_mp1.py
f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d
```

### Qualification bindings

```text
Evaluator declaration
cc1f176eb12dde347351f77ddf661dfa7fdb6f9662d83be28906155687a5d86f

Closure declaration
11074edcacbe26d2fe3b33eff4f7fca4a328a5d7b9dcd84786d2f115206ce204

Declared synthetic census
c2ed98a5382bb1b8828cd527fd2d1b6e7492a94bdfb80f758528aeb4eec099e2

Known-answer qualification result
58b338861232b2860e425060c75b4c2bd9a87e7691ef14d7793af0de34f24a11
```

### Source key

- **R3:** Received round-3 response, identified in §1.
- **Q3:** Received known-answer JSON, identified in §1.
- **R2a:** Amended round-2 response, identified in §1.
- **R2:** L2's round-2 review, supplied byte-identically as the received review in §1.
- **E3:** Received evaluator source, byte-identical to the accepted round-2 evaluator, with its unchanged test companion.
- **C2:** Retained accepted round-2 M5 `instrument/mfa_instrument/f8/closure.py`; its declaration identity is reproduced above.

*L2, 2026-10-29. Evidence-only round-3 review complete.*
