# L1 → L2 — Flight 9 M6 build review, round 2: response to round 1

**Date:** 2026-11-23. **Register:** module build review (receipt first). Not a run authorization.
**Responds to:** `L2_F9_M6_ROUND1_REVIEW_2026-11-23_RECEIVED.md`, SHA-256 `17bf871af75e5aa96a3b67662740b177f77ecfc749e51847f26a5253e6e7e979`, your review of archive `552a5cf3535e733b9776b2cd71de0d7e03dc846b45ea1b848dc3265af551e112` (FINAL VERDICT: NOT SOUND). It is in this packet as received.
**Repository pin:** `ee-theory-lab` `main` at `67aa10ca5958e0c07855441fbeab4a71a66e51f5`, checked against the remote before this packet was built. Nothing of M6 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Contract:** `FLIGHT_9_CONTRACT_v0_7.md`, FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`. Unchanged. No placed module is edited.
**Decision authority:** Mike. On your round-1 return he wrote: "I accept your recommendations. Make the repairs, rerun, and draft l2 round 2 packet." The recommendations were L1's, to accept D1, D2 and D3 and the smaller repairs, and the two in §4 below.

## 0. Receipt first

As in round 1: a receipt table before any review content (archive SHA-256 against the value Mike gives you, file count as the manifest lists it, every file's full digest against `MANIFEST.txt`), then wait for Mike's "execute". Return the review as one `.md` upload that cites this archive's SHA-256 and ends with exactly one plain line at column 0, `FINAL VERDICT: SOUND` or `FINAL VERDICT: NOT SOUND`.

## 1. Identities

| File | Round 1 | Round 2 |
|---|---|---|
| `mfa_instrument/f9/reports.py` | `6e886549559b8ec2724c3a1539f07d8198f712285d31043f3850f17c9c02b146` | `f42f93c586288ee14ee11dfe8e2430e544e81529a2eaba17e73b0bf4345a92de` |
| `tests/test_f9_m6.py` | `b4cae42d19f29d1ec8728d13a2d69cff4428ff005df10aac4a30d33bf52da8c5` (22 tests) | `74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56` (26 tests) |
| Reports declaration digest | `56bc9a108afdc347bcdae98f254de7f3072e091a46d607ed40a118ae887945d2` | `169a8d62bb568388729d88f7cd80c4750fbe7cdb7955a67285fea490607aa1d9` |

The round-1 source, test and mutation script are under `packet_only/round1/` for comparison. The declaration digest changed because the between-width relations and the floor references entered the declaration.

## 2. Your findings

All three were L1's errors and all three reproduced on the round-1 bytes before anything was changed.

**D1 — accepted and repaired.** `_check_windows` now applies, after the per-width relations, the placed parser's between-width relations to the pairs (1, 10), (1, 100) and (10, 100), cell by cell and seed by seed: A_l ≤ A_s ≤ k·A_l; R₀,l ≤ R₀,s; R_a,l ≤ R_a,s; first_s ⇒ first_l; last_s ⇒ last_l. A contradiction raises `F9ReportError` before any distribution is formed. Bounds are still tested in the input's own type before conversion. The docstring says these are necessary conditions, that the parser's relations against the per-tick count series are not available to this API, and that a refusal is malformed input and never an outcome.

Tests:
- `test_records_at_different_widths_must_be_of_one_sequence`: your counterexample and your six targeted cases are refused. The relations are also exercised between W = 10 and W = 100 beside records of one real sequence, with each forged tuple first shown to be possible at its own width. Three stacks built from one tick sequence are accepted.
- `test_the_single_width_relations_are_exactly_realizability`: your enumeration, reproduced (1,024 sequences, 484 candidates, 92 tuples, rule and realizability agree on every candidate).
- `test_each_single_width_relation_refuses_on_its_own`: for each of five per-width relations, a forged W = 100 tuple that breaks that relation alone and passes every between-width relation against real W = 1 and W = 10 records. Round 1's per-width negatives edited one width only; with D1's repair they would be refused for the between-width reason as well, so these were added to keep each per-width relation separately tested.
- **The impossible positive is now a negative.** The W = 1 edit to (2, 1, True, True) beside that cell's unchanged W = 10 record is asserted refused. The positive is your suggestion: a sequence active at its first and last tick only, which gives (2, 1, True, True) at all three widths.
- The 40 constructed runs of the fixture (400,000 records at each width, through the placed `_Windows`) are accepted, as before.

One stack in the first test is asserted *accepted* on purpose: W = 100 = (3, 1, True, True) beside W = 1 = (205, 2, True, False) and W = 10 = (21, 2, True, False). It is not the record of the sequence the two finer tuples were taken from, but a different sequence has all three summaries, so the arrays cannot show a contradiction. It is there to mark the edge of what these checks can do.

**D2 — accepted and repaired.** The flicker record now carries `floor_reference`: a `meaning` string and `by_window` = {1, 10, 100}, each with the registered literal (`"0.0523"`, `"0.1342"`, `"0.6496"`) and the value computed from the rule's constants, 1 − (1 − π₁)(1 − a)^(W − 1). The meaning string says it is the floor-only probability that a window of W ticks holds any activity, an occupancy of windows and not a duration in ticks, and that it enters no band, statistic or count. The three literals and the meaning are in the declaration; `verify_reports_declaration` checks each literal against the computed value to four places and that the W = 1 literal is the margins report's. Tests check the three fields, their W association, the four-place literals, Appendix A.3's six-place values, presence in the all-active and all-inactive cases (three empty bands each), and that no band entry carries a floor field.

The computed values pass through the platform's exp and may differ in the last digit between machines; the literals are the registered references. The same is true of π₁ in the margins record. No equality across machines is claimed for these floats.

**D3 — accepted; declaration repaired.** The docstring and M6-8 now say the two sizes are a sanity check of the geometry, that they do not authenticate the array, that TC's u shifted by one cell is accepted, and that u must be TC's base from the authenticated identity bundle with the binding left to the runner. The error message no longer says "the array is not TC's base u". A test asserts that the shifted array **is accepted**, with your symmetric differences (54 and 102), so the limit is on the record. The calculation is unchanged.

## 3. Declarations as they now stand

M6-1 to M6-5 are unchanged from round 1 (you found them acceptable). The others:

| # | Declaration, round 2 |
|---|---|
| M6-6 | **Flicker record checks.** Per width, with R_a = R₀ − 1 + first + last: 0 ≤ A ≤ n; 0 ≤ R₀ ≤ n − A; R₀ = 0 iff A = n; 0 ≤ R_a ≤ A; R_a = 0 iff A = 0. Per pair W_s < W_l = k·W_s among (1, 10), (1, 100), (10, 100): A_l ≤ A_s ≤ k·A_l; R₀,l ≤ R₀,s; R_a,l ≤ R_a,s; first_s ⇒ first_l; last_s ⇒ last_l. Bounds in the input's own type before conversion. These are the placed parser's relations that the stacked arrays alone can show; they are necessary and not sufficient, and the parser's relations against the count series, provenance and membership are the runner's. |
| M6-7 | **Flicker report.** As round 1 (bands by p̄ from the W = 1 record; W·(n − A)/R₀; undefined iff R₀ = 0; possibly censored iff an end window is inactive; records, defined, undefined, possibly censored, q25, median, q75 per band and W), **and** the W-specific floor references 0.0523, 0.1342, 0.6496 with their meaning (pre-probe declaration §6 point 3). |
| M6-8 | **TC's sets.** bump = (0.9 − u)/0.85 from the u it is given; inside = bump ≥ 0.5; outside = bump ≤ 0.05; exact means; ratio `"undefined"` when the outside mean is 0. The sizes 545 and 7,843 are asserted as a sanity check of the geometry only. u must be TC's base from the authenticated identity bundle; the runner binds it. |
| M6-9 | **Eight readings**, numbered identically in `reports.py`'s docstring and in §5 below. |
| M6-10 | **Records** hold str, int, float, bool, None, list and dict. None is a quantile that does not exist. The flicker record's per-width dicts are keyed by the integer W; a JSON writer makes those keys strings, and the persisted encoding is the runner's to declare. Each record has `"kind": "reported only; never scored"` and the declaration digest, and none has a result, tier or cause field. They are components of the eventual §5.9 records, not bound job records. |

## 4. Two points Mike decided

1. **TC contrast coverage (reading 7).** Mike accepted L1's recommendation, for the governance record: the runner reports the contrast for realization runs, both TC arms, every level (R-6). A skeleton contrast would be an addition and is not made. The function stays neutral to the object. The contrast is a named component of one of the six step-15 reports; which one is left to the runner's build.
2. **Design-side margin summaries (§1.3 d, §3.2).** You found them unassigned. Mike accepted L1's recommendation: they go to the second reports module, at the assembly of the margin report. They are index geometry; the three §3.2 columns the identity record does not carry (the 10–90% base-step band count, band/core, and the largest neighbouring base step) are computed there. The docstring's NOT HERE paragraph records the assignment.

## 5. The readings, one numbering (M6-9)

1. "Also the counts at the cut 0.20": the same pair with 0.20 in place of 0.30, and their ratio.
2. "The median and quartiles": linear interpolation between order statistics. §5.7 names no convention; this is the module's choice. It is the kind §5.5 step 6 names for its own quantile; nothing says §5.5 imposes it on §5.7.
3. Possibly censored records are counted among all records of the band (the same number as among defined records).
4. Possibly censored records with a defined value are included in the quantiles.
5. No cell, or no defined record: counts and None for each quantile.
6. Tie blocks are equal stored values of ω as M1 stores it; no tolerance. ("Bit-equal" is withdrawn.)
7. TC's contrast: the function is object-neutral; coverage and hosting as in §4 point 1.
8. Each bin's cell count is reported beside its ω range.

## 6. Smaller corrections you asked for

- **The reason for the split** was stated too broadly. Persistence assembly mostly joins existing records and does not need another θ; the evaluator-dependent reports are what need it. The split stands on your §8.
- **Disclosure 1** is L1's chosen test boundary and more restrictive than the binding on probe output requires. It is kept. Nothing in M6 checks the path from a run record to a report; that is the runner's and its review's.
- **Coverage ledger.** Your §8 table is taken as the ledger for the second module, including: all 40 seeds with zeros after extinction for the skeleton boundary; both sides' component counts, resolution flags and per-component distances; T0 reports citing Interpretation 001; an unavailable comparator reported for the arm and level it was measured on, with no blanket statement from Disclosure 001.

## 7. Evidence

- `build_records/f9_m6_module_container_round2_2026-11-23.txt` (`e987894634c8e59c5dbea77693a7f42e8c8e0bce98a4650533faa836c6aafd8b`) — **26 passed in 8.42 s** (Python 3.13.18, numpy 2.5.3).
- `build_records/f9_m1_to_m6_container_round2_2026-11-23.txt` (`f312999e67c6f186fbafa61cc472f1089f519f4d6bf24704cd492e2f08015f5c`) — the six Flight 9 test files in one process: **276 passed in 963.85 s (250 from the five placed files, 26 from M6; the mutation check was running beside it for part of that time)**.
- `build_records/l2_m6_round1_reproduce.py` (`c0e7e0977d0313c6936bae9576301fe3a14a81eb309e31bc2b5804c134f93bb0`) — your Appendix R, extracted byte for byte from the received review. Its output on the round-1 bytes (`07acb9795ce812301ab920de9b9c7b6aa9f4c01cf655f40f6976c2b2feb548f1`): impossible stack accepted, six targeted cases accepted, floor reference absent. On the round-2 bytes (`5b5ec79b62253c46a0574a73f305607d10ba605b33239205b91ad82c10f5a647`): impossible stack **refused**, all six **refused**, floor reference **present**. On both: shifted u accepted with ratio 2031337/212332 (unchanged by design, D3), and the JSON reload does not preserve integer keys (unchanged by design, M6-10).
- `build_records/f9_m6_mutation_check_round2_2026-11-23.txt` (`ac6c7201abdc7657fb8bb4e996ab6aebd00bc5a2d3df81c40701b553942f0511`) with its script (`b86212cd39140d5655d93c6482312a6ea359a7deb7352d26cc08fcd14c5cd55a`) — 33 mutations, **30 caught**. The three not caught are labelled equivalent in the script: the censor count among defined records; R₀,l ≤ R₀,s dropped (implied by the R_a relation and the two end implications, as you showed); and the pair (1, 100) skipped (implied by (1, 10) and (10, 100), every relation being transitive). The two redundant checks are kept because the placed parser has them and you asked for all three pairs.

To run: from `flights/mfa_fidelity/instrument`, `python -B -m pytest tests/test_f9_m6.py -v -p no:cacheprovider`.

## 8. Questions

**Q1.** D1: are the between-width relations now exactly the placed parser's, on all three pairs, with no relation added or missing? Can you construct a stack that is accepted and contradicts itself, or one from a single tick sequence that is refused?
**Q2.** D2: is the floor reference carried as you required (three values, correct widths, labelled as window occupancy)? Is its place at the top level of the record, with no copy in the band entries, acceptable?
**Q3.** D3: does the wording now claim only what the check does?
**Q4.** M6-6 to M6-10 as restated in §3, and the eight readings of §5: for each, ACCEPTABLE, REQUIRES CHANGE, or REJECT.
**Q5.** Did any repair change a calculation you accepted in round 1 (constancy, margins, the flicker statistic and quantiles, TC's means)? `packet_only/round1/` has the round-1 bytes.
**Q6.** Anything else.
