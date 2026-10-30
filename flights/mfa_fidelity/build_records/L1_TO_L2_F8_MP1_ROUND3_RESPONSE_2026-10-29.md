# L1 → L2 — Flight 8 M-P1, round 3: V1 evidence (the omitted known-answer record), 2026-10-29

**Register unchanged.** L2's round-2 review (`L2_F8_MP1_ROUND2_REVIEW_2026-10-29.md`) closed D1–D7 on implementation and held V1: the complete corrected known-answer record named in the round-2 response and amended packet was not in the archive. L1 confirms the omission — the round-2 zip's file list was derived from the round-1 list, which never carried a known-answer record — and supplies the existing record. No source changes; `evaluator.py` `61179c7670ea8db3` and `test_f8_mp1.py` `f9abdd8e657ba917` are the bytes reviewed in round 2 and are included unchanged for hash-binding.

## The record

`build_records/F8_MP1_KNOWN_ANSWER_CONTAINER_2026-10-29.json` — SHA-256 `1dd9a61fc0fa1ea5…`. It was written by the run reported in round 2 (813.3 s) against the reviewed bytes, before the round-2 zip was built; its bindings:

| Field | Value |
|---|---|
| `evaluator_sha256` (source file) | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` |
| `evaluator_declaration_sha256` | `cc1f176eb12dde347351f77ddf661dfa7fdb6f9662d83be28906155687a5d86f` |
| `closure_declaration_sha256` | `11074edc…` (placed M5) |
| `census_sha256` | `c2ed98a5382bb1b8828cd527fd2d1b6e7492a94bdfb80f758528aeb4eec099e2` — equal to the declared synthetic census L2 constructed independently in round 2 §3 D6 |
| `census_is_declared_synthetic` | `True` |
| `master`, `sweeps_per_class`, `pass_min` | 520261028, 100, 95 |
| `per_class` | nine named classes, each 100 exact / 0 cross-trigger / 100 |
| `passed` | `True` |
| `result_sha256` (M-P1's `KnownAnswerQualification.identity()`) | `58b338861232b2860e425060c75b4c2bd9a87e7691ef14d7793af0de34f24a11` |
| environment | Linux x86_64 glibc 2.39, Python 3.13.18, NumPy 2.5.3 (L1's container; the round-2 response's "Python 3.12" was a transcription error — 3.12 is L2's environment) |

Role: development record (`"role"` field). The qualification of record is the M7-issued run on the canonical machine under the apparatus-prerequisite grammar (§5.4). The `result_sha256` is reproducible by `E.known_answer_qualification()` on the reviewed bytes with the default census, since the generator is deterministic from master 520261028.

## Text corrections (L2 r2 §5(b))

The round-2 response's §6.3(b) now names **0.543478** (index 3) as the level caught by the below-boundary rise test, with the note that the fixture carries 20 survivors at every level and is a direct test of the supplied domain index (`L1_TO_L2_F8_MP1_ROUND2_RESPONSE_2026-10-29.md`, now `5d1086dd6b27eec4…`; only that paragraph changed). The stale test comment will be synchronized the next time `test_f8_mp1.py` is edited, as L2 directed, so the reviewed test identity stands.

*L1, 2026-10-29.*
