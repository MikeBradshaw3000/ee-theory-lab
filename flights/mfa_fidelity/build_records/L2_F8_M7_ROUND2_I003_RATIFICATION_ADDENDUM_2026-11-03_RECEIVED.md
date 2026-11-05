# L2 — Flight 8 M7 round 2: Interpretation 003 ratification addendum

FINAL VERDICT: DEFECT-WITH-REPAIR

**Date:** 2026-11-03 (America/New_York). **Register:** module build review. **Reviewer:** L2. **Decision authority:** Mike.

**Revision 2 — ratified file verified.** This revision closes the source-verification boundary in the notice-based version, whose SHA-256 was `ba85f4b8a3492f3c96fecfc085ff198d514dc57b30332254ea52baa40841d037`.

This addendum applies Mike's ratification notice and the now-verified ratified I003 attachment to the completed round-2 review. It supersedes that review's pending-ratification wording and the drafting observations identified below. The seven numbered implementation findings remain open on the unchanged submitted ZIP. No change to Interpretation 003 is required by this addendum.

## 1. Receipt and authority basis

| Item | Identity or verification status |
| --- | --- |
| Reviewed submission | `f8_m7_build_round2_L2.zip` |
| Archive SHA-256, recomputed for this addendum | `200e66081a26847f4800ff997db135631559a8459a226387ea6f79439ed9b583` |
| Archive receipt | 77 payload files plus `MANIFEST.txt`: 78 entries. Original receipt: 77/77 payload digests match the manifest. This addendum rehashed all 78 extracted files; all remain equal to the receipted bytes. |
| Submitted repository baseline | `ee-theory-lab 2c8827b`, as declared in the round-2 submission |
| I003 draft inside the submitted ZIP, recomputed | `822ad8d88ad093c906fe1a8d74cc802fecc5799b5b132594054b96997b7d6187` |
| Ratified I003 authority | Ratified 2026-11-03; `ee-theory-lab` commit `1978a01`, as identified by Mike; repository path `flights/mfa_fidelity/rulings/F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md` |
| Verified attachment | `F8_INTERPRETATION_003_RATIFIED_1978a01.md`; expected 9,154 bytes, actual 9,154 bytes — MATCH. The filename was changed for attachment delivery only. |
| Declared ratified-file SHA-256 | `6ebf0ad3efbe8e0e74b45e63d5f6ba550441897f3ff6898749230c064c993e9e` |
| Computed ratified-file SHA-256 | `6ebf0ad3efbe8e0e74b45e63d5f6ba550441897f3ff6898749230c064c993e9e` — MATCH |
| Complete draft comparison | Both files contain 37 lines. Only the status paragraph, Part 1's source-citation paragraph, point 2, and ratification footer differ. All other lines, including points 7 and 8, are byte-for-byte identical. |
| Prior L2 review | `L2_F8_M7_ROUND2_REVIEW_2026-11-03.md`, SHA-256 `f5c61978c7f183d7de8ec1af2f602cbc87629f668bf1b43f3571a36c71977e1a` |
| Prior evidence bundle | `L2_F8_M7_ROUND2_EVIDENCE_2026-11-03.zip`, SHA-256 `2407fa62a33ca787560de3aa38e7db842583aada4efdead8bd0b08c7db44a24e` |

**File-level verification complete.** L2 read the entire attached ratified text, recomputed its byte count and full SHA-256, and compared its bytes with the draft in the round-2 ZIP. The result confirms the three notified drafting corrections plus replacement of the blank footer by the completed ratification record. A second reviewer independently confirmed the same receipt and comparison. Git commit `1978a01` and its association with the repository path remain Mike-supplied provenance; no independent inspection of the remote Git history is claimed.

The later ruling identity does not relabel the submitted code as a build at `1978a01`, and it does not replace the draft within the receipted archive. The build under review remains the original round-2 ZIP. The ratified authority controls the affected interpretation passages, as Mike instructed.

## 2. Effect of the three drafting corrections

### 2.1 Status and the authorized M1 touch — observation closed

The verified ratified status sentence reads:

> **One placed module changes under this record: M1** (`f8/config.py` and `tests/test_f8_m1.py`, the third seed panel of pt 6, Mike's "a′"), placed with M7 after L2's SOUND on both; no other placed module changes.

This resolves the earlier broad status sentence's inconsistency with the specific a′ authorization. The review no longer requests a correction to that sentence or a repeat decision on the touch. Its scope remains the authorized third-panel change to M1's config and test module. The unrelated declaration-check regression identified in R2-7 remains subject to repair.

### 2.2 Morphology fields and predicates — alignment observations closed

The fields and predicates in the verified ratified point 2 match the submitted runner's actual schema and derivation:

| Verified ratified name | Submitted implementation |
| --- | --- |
| `final_set_identical_to_pass1` | `MorphologyRecord` boolean; `_morphology_from_rows` sets it true iff the router requests no insertion. |
| `final_set_obligation` | `"discharged_identically"` when there are no requested insertions; otherwise `"open"`. |
| `matches_expectation` | Descriptive comparison with the expected `NOT_PRODUCED` / `no_null_consistent_phase` result. |
| `morphology_pass1_evaluated` | The submitted pass-1 report predicate, used with full record validation/replay. |
| `morphology_final_set_identical` | Requires final-set identity and the `"discharged_identically"` obligation value. |

The previous request to add or align the draft-only names `insertions_evaluable` and `morphology_final_set_obligation` is superseded. No redundant alias or additional top-level obligation field is required on that basis. The substantive H1 limitation remains: insertion-requesting reports carry an open final-set obligation, and morphology does not enter P1.

**Source:** submitted `instrument/mfa_instrument/f8/runner.py`, `MorphologyRecord`, `_morphology_from_rows`, `validate_morphology`, and the two morphology predicates. Runner SHA-256: `9d8b8378efb51ac403acf746dbe0640205f6a9bbfe2edc7436d40d7769df332b`.

### 2.3 The `f8_run_spec` source citation — correction accepted

The corrected citation identifies the pre-touch `f8/config.py`, SHA-256 `43ea8de23c0d718b246936c7ff6f18e4f8e5243f77ddb240d896e5d00bdf0e07`. That is the previously established config identity discussed by the ruling. The earlier `cc663dd3…` identity belongs to `f8/dynamics.py`.

This is a source-attribution correction. It changes neither the historical production-shape restriction nor the authorized third-panel design. It was not a separate numbered build blocker.

### 2.4 Ratification status — previous pending wording superseded

Mike has notified L2 that ratification and commitment have occurred. The verified file's completed footer records ratification on 2026-11-03, the three corrections after the Gemini audit, and the identified-successor requirement. Ratification is therefore no longer described as an outstanding Mike decision in this review. The old draft footer and the response's contemporaneous “once ratified” wording are not treated as defects in the submitted historical record.

The remaining R2-4 question is whether the submitted executable implementation binds and requires the ratified authority. Ratifying the document does not itself change the runner's placeholder or its conditional omission of that document.

## 3. Updated disposition of the seven implementation findings

| Finding | Disposition after notice and file verification | Required repair on the submitted build |
| --- | --- | --- |
| **R2-1 — readiness dependency coverage** | **OPEN, unchanged.** The drafting corrections do not affect the warm/cold dependency counterexample. | Constrain dependencies to the declared hashed tree or include the complete resolved dependency and commitment surface in readiness validation and memo identity. |
| **R2-2 — public direct production entry** | **OPEN, unchanged.** The direct route still accepts predecessor envelopes without establishing their semantic contents. | Enforce the same semantic predecessor gate before execution through both public production routes, or restrict the lower path to a controlled internal interface with fresh validated context. |
| **R2-3 — clearance parsing** | **OPEN, unchanged.** Historical positive markers in Markdown code material still satisfy the submitted parser. | Require an unambiguous current disposition and reject quoted-only positives and conflicting/malformed dispositions. |
| **R2-4 — I003 identity binding** | **OPEN as an implementation defect.** The ratified file's identity is now verified; the code still contains `PLACEHOLDER_UNTIL_RATIFIED` and omits I003 from `_fixed_records` while that placeholder is present. | Bind the exact ratified I003 identity verified above, require its committed bytes, and refuse canonical use when the authority is absent, altered, uncommitted, or represented by a placeholder. Re-establish affected source/declaration identities through the next submitted repair. |
| **R2-5 — stability comparison** | **OPEN.** Point 8 is byte-for-byte unchanged; its same-index criterion remains the criterion to implement. | Require the same crossing-interval index when both crossings exist, retaining the declared matching-adverse branch. The existing separation-within-Δm calculation may remain descriptive. |
| **R2-6 — committed census before stability** | **OPEN.** Point 7, including its commitment requirement, is byte-for-byte unchanged. | Require the corresponding canonical census output records to match committed bytes before either stability entry point executes; exercise that boundary in the successful chain. |
| **R2-7 — M1 declaration identity** | **OPEN.** The explicit a′ scope does not justify skipping frozen-identity verification when the literal contains `PENDING`. | Restore unconditional declaration-digest equality and reject sentinel/malformed values while retaining the authorized third panel. |

R2-4's original probe remains evidence of the unchanged omission branch: canonical derivation accepted an absent, exact-draft, or arbitrarily altered ruling without changing its identity. It is not presented as a new probe against the ratified file's bytes. The required target is now the ratified identity, not the old `822ad8d8…` draft identity.

For R2-5, the existing diagnostic still distinguishes the two criteria: indices 12 and 13 are different even though their separation, `0.09782599999999997`, lies below Δm, `0.120126265992375`. The unchanged code reports reproduction. The verified point 8 retains the same-index criterion; the two criteria remain distinct.

For R2-6, the completed live-chain observation remains relevant: both stability outputs were produced while their corresponding census output records were absent from HEAD and untracked. The notice changes none of those submitted execution guards.

## 4. Test and evidence continuity

The submitted executable bytes have not changed. The completed local test results remain:

| Test run | Existing completed result | Exit |
| --- | --- | ---: |
| M7 | 32 passed in 4790.54 seconds (1:19:50) | 0 |
| M1 | 70 passed in 4.49 seconds | 0 |
| M2/M3, M4, M5, M-P1, M6 | 171 passed in 955.23 seconds (15:55) | 0 |

These are the earlier completed runs, not fresh runs against a different build. The initial addendum verification recomputed the archive hash, rechecked all 78 extracted file identities, and inspected the code affected by the notice. Revision 2 additionally verifies the 9,154-byte ratified attachment and the complete comparison with the submitted draft. The original review and evidence bundle retain the test commands, fixture limitations, runtime, diagnostic programs, and observed counterexamples. No new scientific or production qualification is claimed.

The previous round-1 closure matrix, acceptance of H1's restricted scope, acceptance of H2's independent-panel design and authorized a′ scope, M3-touch disposition, 29-item package assessment, and 3,360 lattice-run count stand. The independent 70-versus-69 test-count observation and realization-report producer/timing observation retain their nonblocking status; they are not an eighth required repair.

## 5. Disposition and successor rule

**The unchanged round-2 ZIP remains DEFECT-WITH-REPAIR.** Its required work is R2-1 through R2-7. The verified ratified drafting corrections close the earlier nonblocking status/schema/citation observations and supersede the pending-ratification wording.

This disposition requires implementation changes to conform to the identified ruling. It does not require an amendment to ratified Interpretation 003. If a later L2 finding establishes that the ruling itself must change, that change must proceed through an identified successor, as Mike directs; the ratified record is not silently edited.

**The outstanding file-level source verification is closed.** The attached ratified file matches the declared byte count and full digest, and its corrected passages have been read and compared with the draft. The separate provenance limit concerning remote Git-history inspection is stated in §1; it is not a request for another attachment.

## References

- [Verified ratified Interpretation 003 attachment](https://chatgpt.com/library?file_id=libfile_b93b98491754819189789699743f0ff5&account_id=personal), 9,154 bytes; full digest verified in §1.
- [Completed L2 round-2 review](https://chatgpt.com/library?file_id=libfile_3860548c0f5c8191a3d31b7e691ee7af&account_id=personal).
- [Round-2 evidence bundle](https://chatgpt.com/library?file_id=libfile_4e83da1b3f988191952423a1e77a103d&account_id=personal).
- [Gemini audit triage](https://chatgpt.com/library?file_id=libfile_e80de88b395c81918812d88c509eff62&account_id=personal), a pre-ratification audit record. Mike's later notice establishes the chronology of the three corrections.
- Mike's ratification notice in this conversation, 2026-11-03: ratification date, commit, full digest, three drafting corrections, unchanged substance, and identified-successor requirement.

*L2, 2026-11-03.*
