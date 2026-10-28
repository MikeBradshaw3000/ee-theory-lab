# L2 — Flight 8 M2/M3 Round-4 Final Review (V1)

**Date:** 2026-10-28  
**Register:** Flight 8 instrument-build review; M2 and M3 jointly, including M1-r3 change  
**Final verdict: SOUND — on the submitted evidence-of-record standard, with explicit provenance limitations below.**  
**Scope:** V1 verification-evidence repair only; no source changes proposed or reviewed this round.

## 1. Receipt and identities

Inspected `f8_m2_m3_round4_L2.zip`: **6 regular files**, all readable. SHA-256 prefixes independently computed from their bytes:

| File | SHA-256 first 16 | Check |
|---|---|---|
| L1 round-4 response | `9debc3868607508b` | Matches declaration |
| Test-evidence record | `5ce43e9362b930fb` | Matches declaration |
| L2 round-3 review | `290f38bb9df2c1f0` | Matches round-4 cited identity |
| L1 round-3 response | `043cb2e1f1b23080` | Matches prior packet identity |
| `mfa_instrument/f8/null.py` | `4ee3f239b27f772b` | Unchanged from round 3 |
| `tests/test_f8_m2_m3.py` | `d0d26e75280dffef` | Unchanged from round 3 |

The archive's two included executable files have the declared prior identities. Identities of the other source files referenced by L1 are declarations carried forward, not independently recalculated from this six-file archive.

## 2. V1 — completed module evidence

The evidence record transcribes a canonical-machine run from `flights/mfa_fidelity/instrument`:

`python -m pytest tests\\test_f8_m2_m3.py -q -p no:cacheprovider`

- Claimed **exit code 0** and **34 passed in 65.18 s** (one process, full module).
- Declared output-file SHA-256: `92756dfaf3564367b85ebb917783f75b8c10c178bf3481406e178faf6a82c83f`.
- Environment: Windows 11 host CHA-88D57D3; Python 3.14.4; pytest 9.0.3; named pinned dependencies; HEAD `0f30400d982ff6ec4901084ca5f4c43822518eda` plus staged M2/M3 sources at recorded identities.

This supplies the completed canonical-machine execution evidence requested by V1. **Verification limit:** the original `.txt` stdout file is not in the zip, so its declared SHA-256 cannot be independently verified against the underlying bytes. The text is a signed-off transcription by L1 of Mike's clipboard, not an independently witnessed L2 run.

**Local check attempted:** `python -m pytest tests/test_f8_m2_m3.py -q -p no:cacheprovider` against the extracted round-4 archive failed during collection because this evidence-only archive omits `mfa_instrument.f8.config` and the rest of the source package. That is an **incomplete test environment**, not evidence that the canonical suite fails; the local run cannot corroborate the 34 passes. Round-3 L2 had independently observed 4 targeted H1/H3 passes.

**V1 ruling: DISCHARGED as a documentary/canonical-machine test-evidence obligation; NOT independently reproduced by L2.** If independent verification of raw output hashes or test execution is a separate mandatory gate, that separate gate remains open until raw output files or a complete runnable tree are furnished. No stronger assertion is made here.

## 3. H2 — canonical regression evidence

The evidence record transcribes `python -m pytest tests -q -p no:cacheprovider` with **678 passed, 2 skipped in 3032.67 s** from the pinned-root canonical environment. Declared output SHA-256: `8603cbaf338588e0477656b54f3b1a15c1e7b95b4f84409227fc54bd380e8f8b`. The count reconciles as 575 baseline + 69 M1 + 34 M2/M3, with two recorded skips.

**H2 ruling: ACCEPTED as captured canonical regression evidence.** It is an attested transcription, not a byte-verified original output file or an L2-reproduced 680-outcome run. No regression defect is evidenced by the supplied record.

## 4. H1 and H3 carried forward without source changes

**H1 — SOUND within prospectively registered protocol, subject to chronology provenance.** The attempt-2 registered primary test at alpha 0.025 and auxiliary ten-window union test at total alpha 0.025 both pass as recorded; the combined false-rejection union bound is 0.05. The **default alpha 0.05 designated-window DKW test failed** (0.0445029166 > 0.0429469408; `dkw_passed = false`), notwithstanding `qualification_passed = true` under the registered two-part rule. That adverse outcome must remain prominently paired with any qualification claim. Prior attempt-1 failure remains part of the record. Prospective ratification chronology is evidenced by dated, attested records, not by independently certified timestamps.

**H3 — SOUND in transitional grammar.** `production_scope_eligible` and `qualification_passed` remain distinct. `NullValidation` consistency checks are not cryptographic signatures. Deprecated `is_qualification_evidence()` must not be equated with passage, and its M7 removal remains an obligation.

## 5. Final disposition

**SOUND for M2 and M3 jointly with the M1-r3 change, as a review of the documentary evidence and source identities presented under this register.** Round-3's sole V1 hold is discharged by a complete recorded canonical-machine module run and an identified canonical regression result. There is **no identified source repair** and no authorization to change the frozen contract, retrospectively redefine the failed default-alpha statistic, or erase attempt 1.

**Qualification of clearance:** This verdict does *not* assert L2 reproduced the full suite, independently hashed original stdout files, independently authenticated the ratification timestamp, or inspected source files absent from this round's zip. If the governing placement process requires any of those stronger acts (rather than the attested evidence-of-record standard used here), placement must remain conditional on that separate requirement. The alpha disclosure and M7 deprecation/removal obligation travel with this SOUND ruling.
