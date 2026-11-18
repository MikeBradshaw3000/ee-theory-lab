# L1 → L2 — Flight 9 M4 build review, round 1: outcome records (§5.6, §7) and the persistence record (§5.4)

**Date:** 2026-11-17. **Register:** module build review (receipt first). Not a run authorization. M4 runs nothing, draws nothing, holds no master and reads no file.
**Repository pin:** `ee-theory-lab` `main` at `80306ab3d7ce4cd9712ec8bd3604a27e725f9772` (the M3 placement, checked against the remote before this packet was built). Nothing of M4 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Decision authority:** Mike. He said "build m4" on 2026-11-17, after M3 was placed with your round-2 SOUND.
**M3 on the canonical machine:** the whole M3 module passed there before the placement commit (37 passed in 159 s, Python 3.14.4; `build_records/f9_m3_module_canonical_2026-11-17.txt`). That was the first complete run of the M3 test file by anyone other than L1.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's digest against `MANIFEST.txt`. Then wait for Mike's "execute".

## 1. What M4 is

Pure rule, from typed inputs to typed records: the level tier, arm tier, flight B and flight D of §5.6 with the precedence of §7, and the skeleton persistence record of §5.4 and §1.3(a). Two new files; no placed file is edited.

| File | SHA-256 | Contents |
|---|---|---|
| `mfa_instrument/f9/outcomes.py` | `6523da486b8bd9af02e3635e80e1f67434eb7cc8995caa3f8f6a5247bc7319c7` | `level_tier`, `level_apparatus`, `level_from_evaluation`, `arm_tier`, `flight_b`, `flight_d`, `clopper_pearson`, `persistence_record`; its own declaration digest `c94ec4bd7c9aa532264ab2adc91ab6d4948ebff652b5b58380e1befb54a35407` |
| `tests/test_f9_m4.py` | `c379c3a2756e7b58bda07177a039488babf7ba2510f51a4491fcd0fd08d0f345` | 20 tests |

**A change of scope from what L1 told Mike.** L1 described the next module to him as "outcomes and closure: the level, arm and flight tiers, the closure comparators, and T0's tests". M4 is the first part only. The closure comparators of §4 and T0's four tests of §5.8 are a different kind of thing (they compute from run records and carry Flight 8's procedures) and will be their own module. Mike is told with this packet.

Not in M4: the closure comparators and T0's tests (next module); the reports of §5.7; counting survivors from run records, and persisting and binding outcome records (runner); the qualification of §6, which will call these rules.

## 2. Declarations (for your review; Mike ratifies with the governance record)

| # | Declaration | Where |
|---|---|---|
| M4-1 | **Labels.** Every label a record carries is a string of the frozen contract: the level causes of §7 (`no edge at θ`, `under-resolved`, `unstable edge`, `finite resolution`, `no eligible contour`, `no registered contour of own index within ε`, `apparatus unevaluable (<key>)`), the statuses of the §5.6 table, the arm and flight labels, the four profile descriptions. A test finds each in the contract's text. | constants; `test_declaration_verifies_and_the_labels_are_the_contracts` |
| M4-2 | **Level tier.** The nine pairs of results by the contract's table (its seventh row, "unresolved, any", as three). Level causes: `finite resolution` when own or rival is unresolved (L6); the own-adverse cause when own is adverse (L7); both when both hold. On a same-family terrain the discrimination status is always `not adjudicable here`, and unequal results raise. | `level_tier` |
| M4-3 | **Precedence L1 to L5.** Apparatus; then constant index (T0: neither index is scored, whatever the map shows); then no edge; then under-resolved; then unstable edge. The first three map causes belong to the map and so to both indices together; one index unavailable without the other raises. | `level_apparatus`, `level_from_evaluation` |
| M4-4 | **Translation of the evaluator's causes.** M3 emits `no edge at theta` and `below the informative minimum`; §7's labels are `no edge at θ` and `under-resolved`. `level_from_evaluation` translates by a declared table and refuses an unknown cause. M4's records carry the contract's labels only. | `EVALUATOR_CAUSES` |
| M4-5 | **Arm tier.** A1 to A4 in the contract's order. A registered level with no record is an apparatus cause (A1). "Neighbours on the registered grid" are consecutive entries of the 25-level grid, so 0.75 and 1.00 are neighbours and two adverse levels with any level between them are not. | `arm_tier` |
| M4-6 | **The cause of NOT DISTINGUISHED.** The contract names three causes and does not say which is recorded when more than one holds. M4 records every cause that holds, in the contract's listing order: `insufficient informative levels` (fewer than 3 informative), `isolated adverse level` (some informative level is own adverse), `finite resolution` (some informative level is not distinguished). | `arm_tier` |
| M4-7 | **Flight B.** The conjunction over the seven required arms in the table's order. A missing arm record propagates as `no qualified scientific determination` and precedes any scientific label. PRODUCED carries its domain (each arm's informative levels) and resolution (θ, ε, m, L, seeds, tail). | `flight_b` |
| M4-8 | **Flight D.** From the two TB arms' level records; each arm's determination is computed inside by `arm_tier`, so the two cannot disagree. A witness is an informative level with "follows own" and "rival excluded". DISTINGUISHED needs at least 3 witnesses in each arm and no informative "follows rival" in either. The contract names no D causes; the record states what was missing. | `flight_d` |
| M4-9 | **Records check themselves.** A level record is accepted by `arm_tier` and `flight_d` only if it equals what `level_tier` or `level_apparatus` returns for its own contents (it is rebuilt and compared). An arm record is accepted by `flight_b` only if its determination, rule, causes and level lists follow from one another. | `_check_level`, `_check_arm` |
| M4-10 | **Persistence.** s of 40 per level; criterion s ≥ 36; the four profiles by the first row that applies; κ̂_c and bracket as the table states; interval records at the endpoints that exist and a cause at each that does not. Clopper–Pearson by bisection on the binomial tail, with no external library. A missing level makes the whole profile `apparatus unevaluable (missing level record)`. An extinct run is a valid observation. | `persistence_record`, `clopper_pearson` |

## 3. Evidence

- `build_records/f9_m4_module_container_2026-11-17.txt` — **20 passed in 10.98 s** in L1's container (Python 3.13.18, NumPy 2.5.3).
- What the tests establish. Labels: each is found in the frozen contract's text, and the six explicit table rows are matched as the contract prints them. Level: all nine pairs; causes and kinds; same-family; refusals; the adapter from M3's record, for both arms of TB and with own and rival exchanged. Arm: the contract's named sweeps (exactly two informative adjacent adverse levels; two informative compatible levels; 0.75 with 1.00; a level between two adverse levels; apparatus preceding the adverse rule) and 6,000 random sweeps against a second implementation written from the contract's sentences, in which every one of the seven non-empty sets of causes occurs. Flight B: all 4⁷ combinations of arm determinations, with and without qualification, against the table; missing inputs. Flight D: named cases including §6.2 rows 22 and 23 and a case where D is DISTINGUISHED though one TB arm is not COMPATIBLE; 1,500 random sweep pairs against a reference. Forged level and arm records are refused. Persistence: named profiles and 4,000 random sweeps against a reference written with regular expressions; Clopper–Pearson against its defining equations, its closed forms at 0 and 40, symmetry, and the beta-quantile form where scipy is installed. Everything placed before M4 hashes to its placed identity.

## 4. Disclosures

1. **M4-6 is where the contract is silent, and L1 chose not to choose.** Recording every cause that holds adds no precedence of L1's own. But it does mean a NOT DISTINGUISHED arm can carry two or three causes where the contract's wording ("with cause") may have meant one. §6.2 row 19 expects `insufficient informative levels` with exactly two informative levels; that case yields that cause alone here. Q3 asks whether this needs a ruling from Mike.
2. **M3's cause strings are not the contract's (M4-4).** This is a defect of spelling in placed M3 that neither L1 nor your two M3 reviews caught: `no edge at theta` for `no edge at θ`, and `below the informative minimum` for `under-resolved`. L1 has not touched M3's cleared bytes. M4 translates, and the strings are noted for M3's next touch. Say if you would rather M3 be corrected now.
3. **Precedence on T0.** M3 reports an uninformative map's cause before it looks at the family, so on T0 it can say `no edge at theta`. §7 puts the constant index (L2) above the map causes (L3 to L5). `level_from_evaluation` therefore records `no eligible contour` for T0 whatever the map's cause. Nothing else in M4 depends on T0: it is not a required arm.
4. **Flight D's reasons are L1's wording.** The contract says "NOT DISTINGUISHED, with cause" for D and names none. The record states each arm's witness count and every level that follows the rival.
5. **Clopper–Pearson is float arithmetic through `pow`.** The bounds are descriptive and decide nothing. Across platforms they may differ in the last places. The tests hold them to their defining equations at 1e-9 and to scipy's beta quantiles at 1e-10.
6. **The self-check of records (M4-9) is consistency, not provenance.** A level record that passes is one the level rule could have produced; that it was produced from a real evaluation is the runner's to bind. This is the lesson of M2's parser, applied before review.
7. **A result for one index only is refused.** An earlier draft allowed a scored own index with a constant rival. No declared arm can produce that, the contract gives it no status, and L1 removed it. On every declared arm the two indices are scored together or not at all.
8. **Unchanged:** nothing was run for this module. L1 has not seen the boundary endpoint.

## 5. Questions

**Q1.** Do `level_tier`, `arm_tier`, `flight_b` and `flight_d` execute §5.6 with the precedence of §7 exactly? Is there an input for which a record differs from the contract's tables?
**Q2.** Declarations M4-1 to M4-10: for each, ACCEPTABLE, REQUIRES CHANGE (say what), or REJECT.
**Q3.** M4-6: is recording every cause that holds an acceptable reading, or is the cause of a NOT DISTINGUISHED arm a ruling for Mike?
**Q4.** M4-4 and disclosure 2: should M3's cause strings be corrected in M3 now, or is the declared translation sufficient until M3's next touch?
**Q5.** `persistence_record` against §5.4's table and §1.3(a): is any profile, κ̂_c, bracket or endpoint record wrong for some sweep?
**Q6.** Is there a level or arm record that contradicts itself and is accepted (M4-9)?
**Q7.** Anything else to repair before placement, and any other contract ambiguity that should go to Mike.

## 6. Return format

One downloadable `.md` file, receipt table first. If you find a defect, include a program that reproduces it on the packet's bytes. The whole M4 test file runs in about 11 seconds; please run it and say that you did. End with exactly one line, plain, at column 0, with no bold and no trailing text:
`FINAL VERDICT: SOUND`
`FINAL VERDICT: DEFECT-WITH-REPAIR`

*L1, 2026-11-17. Nothing placed; no run on the canonical machine; no placed file modified.*
