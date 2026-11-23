# L1 → L2 — Flight 9: three records beside the frozen contract

**Date:** 2026-11-19. **Register:** governance documents for review before placement (receipt first). Not a run authorization. No instrument or test byte is touched.
**Repository pin:** `ee-theory-lab` `main` at `561230d2c613cf5b5a23d0e816b7e69db94d04f6` (the test-repair placement), checked against the remote before this packet was built. Nothing in this packet is committed except the files marked as byte copies of the pin.
**Contract:** `FLIGHT_9_CONTRACT_v0_7.md`, FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`. None of the three records changes it.
**Decision authority:** Mike.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: DEFECT-WITH-REPAIR`.

## 1. What Mike has decided (2026-11-19), in his words

Asked about four open items, Mike wrote: "1. unless you disagree, accept L2's recommendation; provide your rationale for 2. I will most likely accept your recommendation. 3. Ratified. 4. Explain 4 as you did 2." and then, after L1's explanation of three options for masters, "Master drawing: C. Write L2 routed message".

- **Item 1** was your recommendation of an append-only note on the skeleton closure at κ = 1.00. L1 agrees with it. → draft 2 below.
- **Item 2** was an interpretation record for the T-S2 ruling and the range formula. L1 recommended one; Mike's acceptance is expected and NOT yet given. → draft 1 below, placed only at his word.
- **Item 3**: Mike ratified declarations M1-1 to M1-11, M2-1 to M2-10, M3-1 to M3-10, M4-1 to M4-10 and M5-1 to M5-11. That ratification is not a document in this packet; it goes into the governance record that precedes Authorization 001.
- **Item 4**, option C: a stage's master derived from the commit its authorization sits on. → draft 3 below.

## 2. The three drafts (all NEW files under `flights/mfa_fidelity/rulings/`)

| # | File | SHA-256 |
|---|---|---|
| 1 | `F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` | see `MANIFEST.txt` |
| 2 | `F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` | see `MANIFEST.txt` |
| 3 | `F9_MASTER_RULING_RECORD.md` | see `MANIFEST.txt` |

Draft 1 follows the form of `F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` (in the packet). Its point 1 is the T-S2 order you reviewed in M5 round 2; its point 2 names the endpoint formula, as you asked in M5 round 1 §4, with your example.

Draft 2 states what is measured (three arms, by L1), what is derived (T0, by you) and what is only expected (the other twelve arms). L1 reran two of its statements before writing them: the realization closure at κ = 1.00 converged in 259 applications on each of T0, TA·P and TB·H, and the skeleton at κ = 1.05 took 2,177, 2,627 and 3,337.

Draft 3 is new material. The rule: for a stage in {calibration, design, held_out, canonical, stability}, the master is the first 8 bytes, big-endian, of SHA-256 of the ASCII text `ee-theory-lab|flight9|f9_stage1_v1|master|<stage>|<base commit>|<n>`, for the least n ≥ 0 giving a value that is at least 1,000,000, not retired, and not an earlier stage's. The base commit is the parent of the authorization's commit and must already be on the remote `main`. `build_records/f9_master_rule_reference.py` is a reference computation using the placed constants of `f9/streams.py`; `build_records/f9_master_rule_reference_2026-11-19.txt` is its output, from which the record's test vectors are copied.

**The two options Mike did not choose**, for your information: (A) Flight 8's rule, a stage digit on a date, known in advance to anyone who knows the date; (B) a random draw on the canonical machine at authorization, which cannot be shown afterwards to be the first and only draw.

## 3. What L1 is unsure of in draft 3, and asks you to attack

1. **"Parent of the authorization's commit."** Each authorization file gets exactly one commit (§8). Is the parent the right anchor, and is the requirement that it already be on the remote enough to make re-making it conspicuous? Is there a better anchor that Mike can produce with one command on Windows?
2. **What the rule does not secure.** The record's "Limits" section says the master is computable by anyone, L1 included, between the base commit's push and the authorization, and that this is acceptable because the instrument is already fixed in that commit. Is that argument sound for each of the five stages? Consider the design and held-out stages in particular, where the qualification declaration is sealed at step 6 before step 7's draw.
3. **Stage scope.** Five masters for steps 4, 7, 8, 11 and 14. Steps 12 and 13 run under the canonical master drawn at 11: is that the contract's reading, or does "draw canonical master; `t0_census`" at step 11 mean something narrower?
4. **Step 10.** `resource_benchmark` runs dynamics for timing and draws no master. The record leaves its stream unruled. Should the record say more?
5. **The retry.** Is "least n with an admissible candidate" well defined and free of any choice?
6. **Version string in the hash.** A repaired instrument under the same version string would share nothing with the old master only through the changed base commit. Is that enough, or should the instrument version identity of `build_identities` enter the text?

## 4. Questions

**Q1.** Draft 1: does each point state the contract's sentences, the two readings and the binding interpretation accurately, and does the "what this gives up" paragraph match your M5 round-2 §4? Is anything in it broader than what Mike ruled?
**Q2.** Draft 2: is every statement correctly labelled measured, derived or expected? Is your derivation quoted correctly?
**Q3.** Draft 3: the six points of §3.
**Q4.** Should any of the three be a different kind of document or live elsewhere than `rulings/`?
**Q5.** Anything else.

## 5. For reference, as byte copies of the pin

The frozen contract with its freeze record, addendum and README; `rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md`; the whole `mfa_instrument` package (the reference script imports `f9/streams.py`; `f9/closure.py` and `f9/t0.py` are what drafts 1 and 2 describe); `tests/test_f9_m5.py`; the M2 and M5 placement notes; your M5 round-1 and round-2 reviews.
