# F9 M6 placement note (prepared 2026-11-23)

**Module.** Flight 9 instrument module M6, part 1: the reports of Contract F9 v0.7 that are statistics of a level's maps (`f9/reports.py`): contour constancy (§5.7 row 1; §1.3 b), measured margins (§5.7 row 2; §1.3 d, measured side), flicker distributions (§5.7 row 3; §2.11; §1.3 c) and TC's suppression contrast (§1.3 e). Built at Mike's word "build m6" and placed at his word "place m6", both 2026-11-23, against `main` at `67aa10ca5958e0c07855441fbeab4a71a66e51f5` (the governance records placement), checked against the remote before the kit was built.

**Everything in M6 is reported only.** Nothing in it is scored, enters B or D, or gates anything. It holds no master, runs no dynamics and reads no run record.

**Placed (instrument), both NEW; no placed file is edited:**

| File | SHA-256 |
|---|---|
| `mfa_instrument/f9/reports.py` | `f42f93c586288ee14ee11dfe8e2430e544e81529a2eaba17e73b0bf4345a92de` |
| `tests/test_f9_m6.py` (26 tests) | `74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56` |

These are the bytes of L2's round-2 packet (`f9_m6_build_round2_L2.zip`, `e9271469bbc10d90e21c87cf3a9f87c1ea05d2fcf3c621e70ad683e569e50f73`), which L2 cleared.

**Declaration digest in the placed source:** `169a8d62bb568388729d88f7cd80c4750fbe7cdb7955a67285fea490607aa1d9` (round 1 was `56bc9a108afdc347bcdae98f254de7f3072e091a46d607ed40a118ae887945d2`; the between-width record checks and the flicker floor references entered the declaration). It identifies the declaration, not the implementation.

**Review history (every L2 return a byte copy, `_RECEIVED`):**

| Round | L1 document | L2 return | Verdict |
|---|---|---|---|
| 1 | `L1_TO_L2_F9_M6_BUILD_PACKET_2026-11-23.md` `4bae93832659dc52a120bb1256f3408fa06392be457809819373cc03c2f8b81e` (packet `552a5cf3535e733b9776b2cd71de0d7e03dc846b45ea1b848dc3265af551e112`) | `L2_F9_M6_ROUND1_REVIEW_2026-11-23_RECEIVED.md` `17bf871af75e5aa96a3b67662740b177f77ecfc749e51847f26a5253e6e7e979` | NOT SOUND: D1, D2, D3 (below). Constancy, margins, the single-width flicker checks, the flicker statistic and TC's geometry accepted; M6-1 to M6-5 acceptable; the split acceptable |
| 2 | `L1_TO_L2_F9_M6_ROUND2_RESPONSE_2026-11-23.md` `83c8439ceedce2ed64c2f8e5371cf1c435a8604cae3dc073e35673689470d818` (packet `e9271469…`) | `L2_F9_M6_ROUND2_REVIEW_2026-11-23_RECEIVED.md` `2287afecc3b9eee634d0b42ffa7b6e26c2cac0f4a2e2f370888c35025c5f5bcd` | **SOUND** within the map-statistic module boundary: D1, D2, D3 closed; M6-6 to M6-10 and the eight readings acceptable; no accepted calculation changed |

The round-1 source (`6e886549559b8ec2724c3a1539f07d8198f712285d31043f3850f17c9c02b146`), test (`b4cae42d19f29d1ec8728d13a2d69cff4428ff005df10aac4a30d33bf52da8c5`) and mutation script (`9eef3e2d968a80830c62491572f2229ba707dc0db0241dace9814d631842e55c`) are not committed; they are in both packets. The committed `f9_m6_mutation_check.py` is round 2's.

**The three round-1 findings. All were L1's errors.**
- **D1.** The flicker input check tested each window width alone and never tested the widths against each other, so a cell inactive at every tick at W = 1 and active in every window at W = 10 and 100 was accepted. The placed parser already had the between-width relations. One of L1's own tests asserted acceptance of an impossible record. Repaired: the parser's relations on the pairs (1, 10), (1, 100), (10, 100).
- **D2.** The flicker record omitted the W-specific floor references (0.0523, 0.1342, 0.6496) that the pre-probe declaration §6 point 3 requires and §2.11 incorporates unchanged. L1 read §5.7's table and missed the inherited item. Repaired: carried at the top level of the record with a label saying they are window occupancies, not durations.
- **D3.** M6-8 said that asserting TC's two set sizes refuses any other array. It does not: TC's u shifted by one cell has the same sizes. Repaired in wording only; a test now asserts the shifted array is accepted.

**The limit L2 put on the verdict, to be kept visible.** An accepted flicker stack has passed the specified consistency checks. It has NOT been shown to be the record of one tick sequence. L2's round-2 example: (20, 1, True, False) at W = 1, (20, 1, True, False) at W = 10 and (2, 1, True, False) at W = 100 passes every check and is impossible (the W = 1 record forces (2, 1, True, False) and (1, 1, True, False) at the coarser widths). The forged stack reports medians 980, 800, 800 ticks; the true one 980, 980, 900. L1 reproduced it (`f9_m6_l2_round2_limit_on_round2_2026-11-23.txt`). L2: this does not reopen D1, whose repair was parity with the placed parser's available relations, stated as necessary and not sufficient. Complete-record parsing, the relations against the count series, provenance, seed, arm, level and object membership, and canonical-array binding are the runner's. Likewise the TC set sizes authenticate nothing; the runner binds u to the identity bundle.

**Mike's decisions on the round-1 return (2026-11-23): "I accept your recommendations. Make the repairs, rerun, and draft l2 round 2 packet."** The recommendations were L1's: accept D1 to D3 and the smaller repairs, and
1. **TC contrast coverage:** the runner reports it for realization runs, both TC arms, every level (the pre-probe declaration's R-6). A skeleton contrast would be an addition and is not made. The function is neutral to the object. The contrast is a named component of one of the six step-15 reports; which one is the runner's build choice.
2. **Design-side margin summaries (§1.3 d, §3.2),** which neither of L1's round-1 lists assigned (L2 found the gap): they go to the second reports module, at the assembly of the margin report, with the three §3.2 columns the identity record does not carry (the 10–90% base-step band count, band/core, the largest neighbouring base step).
Both are for the governance record.

**The split is L1's choice of boundary, accepted by L2 as a module boundary.** Deferred to a second reports module, not built: the evaluator's full output at θ = 0.10 and 0.30 (§1.3 f); the skeleton boundary (§1.3 g); component coverage (§1.3 h); the fidelity uncertainties of §5.7 row 4; the design-side margins; the assembly of the persistence report. L2's round-1 §8 and round-2 §7 tables are the coverage ledger for it, including: all 40 seeds with zeros after extinction for the skeleton boundary; both sides' component counts, resolution flags and per-component distances; reports of T0's outcome citing Interpretation 001; an unavailable comparator reported for the arm, object and level it was measured on, with no blanket statement from Disclosure 001. A missing mandatory report prevents a claim of complete reporting; it is not a failure of B or D.

**Declarations M6-1 to M6-10 and eight readings, found acceptable by L2, await Mike's ratification with the governance record.** The readings, in the numbering of the round-2 response and of the module's docstring: (1) the counts at the cut 0.20 are the pair #{p̃ ≥ 0.20} and #{0.10 ≤ p̃ < 0.20} with their ratio; (2) quartiles by linear interpolation between order statistics, the module's choice where §5.7 names none; (3) possibly censored records counted among all records of a band; (4) possibly censored records with a defined value included in the quantiles; (5) no defined record gives None for each quantile; (6) tie blocks are equal stored values of ω, no tolerance; (7) TC coverage and hosting as decided above; (8) each bin's cell count beside its ω range.

**Two wording notes from L2's round 2, nonblocking, for the next touch of `test_f9_m6.py` (not repaired here, so the placed bytes are the cleared bytes).**
1. The docstring of `test_records_at_different_widths_must_be_of_one_sequence` says a stack whose widths contradict each other "is refused". That holds for the listed necessary relations only; it is not a realizability guarantee.
2. In `test_flicker_named_cases` the comment "no defined record anywhere; three empty bands" stands over a loop that also covers the all-inactive pattern, where every record is defined. The assertions under it are correct.

**L1's test boundary.** The M6 tests make no lattice run, and L1 has computed none of these reports on output of the rule. L2: appropriate for these component tests, and more restrictive than the binding on probe output requires. Nothing in M6 checks the path from a run record to a persisted report; that is the runner's and its review's.

**What was run, and by whom.**
- L2, round 2 (Python 3.12.14, numpy 2.3.5): the M6 test file, 26 passed in 8.43 s; the mutation script, 30 of 33 caught; its round-1 program on both rounds; 45 valid fixtures compared between the round-1 and round-2 implementations with no numerical difference; 5,136 constructed histories (400,000 records per width) accepted; a 70-digit check of the three floor references. L2 did **not** rerun the six-file suite and did not fetch the remote; the pin is L1's statement, checked by L1.
- L1's container (Python 3.13.18, numpy 2.5.3): M6 alone, 26 passed in 8.42 s (`f9_m6_module_container_round2_2026-11-23.txt`); the six Flight 9 test files in one process, 276 passed in 963.85 s (`f9_m1_to_m6_container_round2_2026-11-23.txt`; the mutation check shared the machine for part of that time); the mutation check, 30 of 33, the three survivors being equivalent forms (the censor count among defined records; R₀ nesting, implied by the R_a relation and the end implications; the pair (1, 100), implied by the two adjacent pairs).
- The canonical machine: the six Flight 9 test files in one process on the placed bytes, before anything is staged (`f9_m1_to_m6_canonical_2026-11-23.txt`, written by the placement script; its identity of record is measured from a fresh clone after the push). If that run happens on a later day than the file's name says, the next note records the true date.

**Also now true.** `test_f9_m6.py` holds the LF identities of the thirteen earlier `f9` sources, so M5's `closure.py` and `t0.py` are pinned by content in a test for the first time. Its folder check is in subset form and will not fail when a later module is placed.

**Carried, unchanged by this placement.** The second reports module; qualification (§6); the runner with the authorization kit (L2's ten checks; binding of run records, bundle, canonical arrays and evaluator identities; the persisted encoding of report records; calibration completeness); the governance record (carrying the ratification of M1-1 to M5-11 of 2026-11-19, and M6-1 to M6-10 with the readings when Mike ratifies them); L2's two optional parser bounds at the next touch of `dynamics.py`; M3's cause strings at the next touch of `evaluator.py`; the two Flight 8 test notes. Held, nothing authorized: Gemini commission v3.1; the third-order lattice-versus-ODE comparison; onset continuity; the PD7-versus-floor correspondence.

**Placement authorizes no run.** No job has been run, no master has been drawn, and no report has been computed on output of the rule.
