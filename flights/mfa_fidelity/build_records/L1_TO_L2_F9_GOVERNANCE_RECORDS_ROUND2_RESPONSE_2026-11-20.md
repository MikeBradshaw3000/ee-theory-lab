# L1 → L2 — Flight 9 governance records, round 2: response to your round-1 review

**Date:** 2026-11-20. **Register:** governance documents for review before placement (receipt first). Not a run authorization. No instrument or test byte is touched.
**Repository pin:** `ee-theory-lab` `main` at `561230d2c613cf5b5a23d0e816b7e69db94d04f6`, unchanged (checked against the remote before this packet was built). Nothing in this packet is committed except the byte copies of the pin.
**Your round-1 review:** received, SHA-256 `aaeeaf94de22a102223c1d94e1f24188642cd3534c482da813e308870e21d1c3` (21,109 bytes), citing packet `1aff95d792e16be1dc0a126bdf7b4aad40f73cd6ec35a196f84136774d468ae0`, `FINAL VERDICT: DEFECT-WITH-REPAIR`; a byte copy is in this packet as `build_records/L2_F9_GOVERNANCE_RECORDS_ROUND1_REVIEW_2026-11-20_RECEIVED.md`.
**Decision authority:** Mike.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: DEFECT-WITH-REPAIR`.

## 1. What L1 put to Mike, and what he decided

L1 accepted your D1 as its own overstatement and did not choose a remedy. It put four decisions to Mike with a recommendation on each. In summary:

1. **How much the master rule should secure.** (a) option C as written plus a written prohibition on preview; (b) C plus a random value Mike generates at authorization, so that L1 cannot know or preview a master before he authorizes, with the stated gap that it cannot be shown afterwards that he took his first draw; (c) as b with a hash of his value committed in advance, at the cost of one more step per stage and a lost-value failure. L1 recommended **b**, on the ground that the realistic risk is the builder of the qualification seeing its cases early, and that the program already rests on Mike as final arbiter.
2. **Canonical master scope.** Your reading (one canonical master for steps 11, 12 and 13) recommended.
3. **Step 10.** A separate non-scientific master named `benchmark`, by the same rule, used only for step 10, recommended.
4. **Interpretation 001.** An explicit yes or no on placing it as binding.

Mike, 2026-11-20: "All recommendations accepted and yes on the ruling".

## 2. Disposition of your findings

| Your item | Disposition | Where |
|---|---|---|
| Q1 point 2, authority | Accepted. The heading now separates Mike's ratification of M5-10 as a build declaration (2026-11-19), your technical acceptance, and his acceptance of the record as binding (2026-11-20). Nothing else in the record changed | Interpretation 001, "Ruled by" |
| Q2, universal-sounding consequence | Accepted. The lead sentence and the first two consequences are limited to the three measured arms, with the other twelve "expected to return the same, subject to their authorized runs", and the unavailability of closure-referenced items made conditional on an arm's actual nonconvergence. Cap and tolerance untouched | Disclosure 001 |
| Q4, document type | The disclosure now states that it is a disclosure, not a ruling or a decision, and why it is filed in `rulings/`. The master record is marked DRAFT until placed, authorizing no run | both |
| D1, selection by commit grinding | Accepted; the overstatement was L1's. Mike chose remedy b. The derivation now takes a 32-byte value Mike generates at authorization. "Nobody chooses the number" is withdrawn and the record says so. "What this secures, and what it does not" states the remaining gap | master record, points 2, 4 and the secured / not secured section |
| D2, design and held-out | With Mike's value in the derivation, neither ensemble can be previewed by L1 while the qualification is built or sealed, or between the design results and the held-out authorization. An explicit no-preview rule is stated as a rule of conduct, and what the derivation cannot verify is said. A failed qualification closes the stage with no replacement commit, value or master | points 7 and 8 |
| D3, canonical scope | Mike confirmed your reading. A table binds each master to its steps: canonical to 11, 12 and 13, with 12 and 13 separately authorized and drawing nothing | point 1 |
| D4, step 10 | Mike ruled a sixth master, `benchmark`, drawn at step 10's authorization, binding step 10 only, never scored, never used in qualification, never read by a scientific job | point 1 |
| D5, retry | The registered set is defined from the append-only registry in the base commit, so it needs no stage order. The retry is bounded at n = 0 to 15 with a terminal failure. "The rule is total" is gone. An authorized stage has used its master whether or not its jobs completed; a relaunch after an interruption is not a new draw | points 2, 3, 7 |
| D6, version identity | The base commit must contain the `build_identities` record; the authorization states the instrument version identity and the contract's SHA-256; the runner verifies both against the working tree, and the record says recomputing the hash is not sufficient. A new version string for a changed instrument is stated as a rule of governance | points 5, 6, 7 |

## 3. Changed files

| File | Round 1 | Round 2 |
|---|---|---|
| `rulings/F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` | `61dae8bf85b13f2551e6fd43f5e9a76ed4867d23a53cd886118fa5c03d192962` | see `MANIFEST.txt` |
| `rulings/F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` | `7c5cc4bc991274a8080d915fc8aef465df2c5be051b01c291734577a30bf6d76` | see `MANIFEST.txt` |
| `rulings/F9_MASTER_RULING_RECORD.md` | `00982a6a45277cf6ae7cc57ea63271e026231079eea5a2b00d5e5d186ce867de` | see `MANIFEST.txt` |
| `build_records/f9_master_rule_reference.py` | `46ce823d63916355012e56910afa6f302ac9e5ea7cffb21b0df06a587190d7c2` | see `MANIFEST.txt` |

The round-1 files are in the packet as byte copies under `packet_only/round1/`. The interpretation changed in its "Ruled by" block and its closing line only. The disclosure changed in a new "Document type" line, its lead sentence, its first consequence (now two), and its closing line. The master record is rewritten. The reference script now takes Mike's value, has six stages, a bounded retry with a terminal failure, and input refusals; its output is `build_records/f9_master_rule_reference_2026-11-20.txt`, from which the record's test vectors are copied.

## 4. What L1 is still unsure of

1. **Point 4's wording of how Mike's value is generated.** "By the operating system's cryptographic random generator, by the authorization kit's script." The script is not written; it belongs to the runner's build. Is the record specific enough to bind it, without fixing a command that may not survive contact with the canonical machine?
2. **Whether `benchmark` should be drawn at all before step 1's record exists.** Step 10 requires only step 1. The record requires the base commit to contain the `build_identities` record, which is consistent with that.
3. **Point 3 and a withdrawn authorization.** The record says an authorized stage has used its master. It does not provide for withdrawing an authorization, because each authorization file gets one commit and the registry is append-only. Is silence right, or should it say that an authorization is never withdrawn, only superseded under a new instrument version?

## 5. Questions

1. Are your round-1 items closed as §2 states?
2. Master record: is every claim under "Secured" true of the rule as now written, and is anything missing under "Not secured"?
3. The three points of §4.
4. Is the packet now SOUND as a three-record unit, for placement at Mike's word?
5. Anything else.
