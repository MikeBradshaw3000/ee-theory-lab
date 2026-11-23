# F9 governance records placement note (prepared 2026-11-20)

**What this is.** Three records placed beside the frozen Contract F9 v0.7 (`60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`), with their review history. No instrument file, no test file and no byte of the contract is touched. The kit was built on 2026-11-20 at Mike's word, against `main` at `561230d2c613cf5b5a23d0e816b7e69db94d04f6` (the test-repair placement), checked against the remote. The placement is Mike's commit of it; its date is the commit's.

**Placed, all NEW, under `flights/mfa_fidelity/rulings/`:**

| File | SHA-256 | Kind |
|---|---|---|
| `F9_MASTER_RULING_RECORD.md` | `02b98378057e776769b48150059a2b9323737fd5ab437f907ae4d62c3fc27b75` | ruling: how a master is produced and recorded |
| `F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` | `b38a4ff6eaa3e2118a9ae723cff63a3336fb178a35932071c3dc43c4478c50a6` | binding interpretation of §5.8, T0 only |
| `F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` | `bc5fac1d53fd57ac0923fb759e465e8783389d92cb1188e297c185c5b91ac78d` | disclosure; not a ruling |

These are the bytes of L2's round-2 packet (`f9_governance_records_round2_L2.zip`, `1b9651080d03ae9501f656cacf33bfc5f6bdfb168c58e57f2a4b4ef2e2547cb5`), which L2 cleared. With this placement the master record's "DRAFT until placed" has run its course: it is the ruling.

**Review history (every L2 return a byte copy, `_RECEIVED`):**

| Round | L1 document | L2 return | Verdict |
|---|---|---|---|
| 1 | `L1_TO_L2_F9_GOVERNANCE_RECORDS_PACKET_2026-11-19.md` `d253542c…` (packet `1aff95d7…`) | `L2_F9_GOVERNANCE_RECORDS_ROUND1_REVIEW_2026-11-20_RECEIVED.md` `aaeeaf94de22a102223c1d94e1f24188642cd3534c482da813e308870e21d1c3` | DEFECT-WITH-REPAIR: the master record overclaimed (D1) and left stage scope, step 10, the retry and identity binding unresolved (D2 to D6); the interpretation's authority statement ran ahead of Mike; the disclosure's consequence read as flight-wide |
| 2 | `L1_TO_L2_F9_GOVERNANCE_RECORDS_ROUND2_RESPONSE_2026-11-20.md` `12b412c4…` (packet `1b965108…`) | `L2_F9_GOVERNANCE_RECORDS_ROUND2_REVIEW_2026-11-20_RECEIVED.md` `4ac4e07b5e40a1cf41d624878467d6be0303ab32cb5dd341d1674709f8e5b92d` | **SOUND**: D1 to D6 and both wording repairs closed; sound for placement at Mike's word |

The round-1 drafts (`00982a6a…`, `61dae8bf…`, `7c5cc4bc…`) are NOT placed. They exist in the two L2 packets only.

**The overstatement in round 1 was L1's.** The first master record said "Nobody chooses the number" of a rule under which whoever prepares the base commit could compute masters for several candidate commits in private and push the one preferred. L1 prepares every commit's contents. L2 found it (D1). L1 did not choose the remedy: it put three levels of protection to Mike, who chose the second (a 32-byte value he generates at authorization enters the derivation).

**Mike's decisions recorded by these documents, in his words.**
- 2026-11-18, on T-S2 (Interpretation 001, point 1): "I accept your reading, which appears to be consistent with the record and with L2. If you agree, proceed with the round".
- 2026-11-19: "1. unless you disagree, accept L2's recommendation; provide your rationale for 2. I will most likely accept your recommendation. 3. Ratified. 4. Explain 4 as you did 2." and then "Master drawing: C. Write L2 routed message".
- 2026-11-20, on the four points L2's round 1 required him to decide: "All recommendations accepted and yes on the ruling".

**Ratification, entered here because no governance record exists yet to hold it.** On 2026-11-19 Mike ratified ("3. Ratified.") the build declarations of the five placed modules: M1-1 to M1-11, M2-1 to M2-10, M3-1 to M3-10, M4-1 to M4-10 and M5-1 to M5-11, as listed in each module's round-1 packet document and restated in its later responses. L1 had named these to him as included: recording every A4 cause that holds (M4-6); translating M3's two cause strings in M4 until M3's next touch (M4-4); an arm record carrying its 25 level records (M4-9); and M5's accepted readings, the sampled range being the median at the top level minus the median at the lowest level of the domain (M5-10). This note records the ratification; the governance record that precedes Authorization 001 will carry it with the declarations' text.

**What the master ruling secures and what it does not, in one place.** Reproducible by anyone from the authorization file and the repository; bound to the commit that holds the instrument; not knowable before authorization by anyone who does not hold Mike's value, L1 included. Not secured: that Mike generated one value and used the first (the record relies on him for that, and L2 calls it an explicit trust boundary); nothing is hidden after authorization. It is not a cryptographic commitment scheme.

**Carried to the runner and authorization-kit build, from L2's round 2 (not defects of these records).** The kit uses an operating-system cryptographic generator for exactly 32 fresh bytes, written as 64 lower-case hexadecimal characters, recorded once. The kit refuses to delete, replace or reissue an authorization under the same instrument version; a superseding instrument version is a new governed process, not a withdrawal. L2's list for that review: first-value generation and immutable authorization-file creation; one-parent commit and remote-base verification; the complete ancestor registry; duplicate, retired and test master refusal; the sixteen-candidate terminal refusal; relaunch of an interrupted job without redrawing; the canonical master used only at steps 11 to 13; benchmark isolation; contract and `build_identities` source matching; refusal of a second authorization for the same stage and version. Neither the runner nor the kit exists.

**The reference computation** (`f9_master_rule_reference.py` `aa0342d6…`, output `f9_master_rule_reference_2026-11-20.txt` `6740a97b…`) is an implementation target, not the runner. Its test vectors use made-up commits and values. L2 recomputed one vector by hand in round 1 and found the algorithm to match the written rule in round 2.

**A date correction owed from the test-repair placement.** `f9_m1_to_m5_canonical_2026-11-18.txt` and `F9_TEST_REPAIR_PLACEMENT_NOTE_2026-11-18.md` carry 2026-11-18 in their names because the kit was built that day. The canonical run of the five module files (250 passed in 858.01 s) and the commit `561230d` were on **2026-11-19** (commit time 14:03 EST). The record's identity from a fresh clone is `1f79b9aa1160c7cb7f7f96ef6e54f30028409b170a66474459b847e31dd88cba`.

**No test run gates this commit.** It adds documents only. The placement script checks the kit's hash, HEAD and an empty index, refuses if any destination file already exists, writes the bytes, re-hashes them and stages.

**What placement does NOT do.** No run is authorized and no authorization file exists. No master exists: none can until an authorization is written under the placed ruling, by a kit that is not built. No job has been run.

**Still open.** The reports module (§5.7), qualification (§6), the runner with the authorization kit, the governance record and Authorization 001. Held for their files' next touch: M3's two cause strings (`evaluator.py`); the two optional parser bounds (`dynamics.py`); the two Flight 8 test notes. Held list unchanged (Gemini commission v3.1; third-order lattice-versus-ODE comparison; onset continuity; PD7-versus-floor correspondence).

**Carried.** L1 has not opened the probe arrays for any boundary purpose and has not seen the boundary-compatibility endpoint.

*L1, 2026-11-20.*
