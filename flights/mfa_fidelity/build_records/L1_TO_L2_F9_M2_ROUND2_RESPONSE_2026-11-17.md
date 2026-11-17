# L1 → L2 — Flight 9 M2 build review, round 2: response to R1 and R2

**Date:** 2026-11-17. **Register:** module build review (receipt first). Not a run authorization. No master is drawn; M2 holds no master.
**Repository pin:** `ee-theory-lab` `main` at `7af50941e47249965dc6c8b2a502d06166e08866`, unchanged (checked against the remote before this packet was built). Nothing of M2 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Your round-1 review:** received as `cdc53166-L2_F9_M2_ROUND1_REVIEW_2026-11-17.md`, SHA-256 `7ba22c09dc86efe94d40148dc965f94256e748e259dacb3061e1dd86d43c7e5a`, `FINAL VERDICT: DEFECT-WITH-REPAIR`; a byte copy is in this packet as `build_records/L2_F9_M2_ROUND1_REVIEW_2026-11-17_RECEIVED.md`.
**Decision authority:** Mike. He was shown the review and L1's recommendation on the scope of R2 (exclude the whole earlier inventory, not only the three) and said "continue" without choosing otherwise. L1 proceeded on its recommendation and says so to him with this packet.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's digest against `MANIFEST.txt`. Then wait for Mike's "execute".

## 1. Disposition of your findings

L1 accepts R1, R2 and the M2-7 wording correction in full. Both defects were L1's. L1 extracted your two programs (hashes equal to the ones you state), ran Appendix A against the round-1 packet and got your output line for line, and ran Appendix B against both rounds (9,216 histories pass on each).

Appendix A stops at its own source-hash guard on round-2 bytes, as you said it would. So that the reversal can be seen with your constructions unchanged, L1 wrote `build_records/l1_m2_round1_witnesses_adapted.py`: your program with the hash guards removed and each acceptance assertion replaced by a printed outcome. Its output on each round is in the packet:

| Witness | Round 1 | Round 2 |
|---|---|---|
| Masters 202609221, 202609222, 202609223 | ACCEPTED | REFUSED (retired) |
| Unaltered control | parses; replay True | parses; replay True |
| R1a first endpoint | ACCEPTED | REFUSED: the first window's mask against the counts of its ticks |
| R1a last endpoint | ACCEPTED | REFUSED: the last window's mask against the counts of its ticks |
| R1b nested windows | ACCEPTED | REFUSED: active windows are not nested (W = 10 and 100) |
| R1c float stream key | ACCEPTED | REFUSED |
| R1c bool window | ACCEPTED | REFUSED |

### R1 — what the parser now checks

Your four required items, and relations of the same kind that L1 added so that the next witness of this class is not left for a third round. All are relations between quantities already stored; none reconstructs a trajectory. The list is the docstring of `_check_consistency`.

| Relation | Source |
|---|---|
| At W = 1 the first and last masks have exactly counts[first tail tick] and counts[T] cells | your item 1 |
| For every nested pair Ws < Wl (k = Wl/Ws), cell by cell: A_l ≤ A_s ≤ k·A_l, and an active fine end window implies an active coarse end window. Applies to (1, 10), (1, 100) and (10, 100) | your item 2 |
| `stream_key` and `windows` are lists of exact integers (no bool, no float) of the declared length and values | your item 3 |
| For every nested pair: R0_l ≤ R0_s and Ra_l ≤ Ra_s, with Ra = R0 − 1 + first + last the active segments. Distinct coarse segments lie in distinct fine segments | L1 |
| Per W, with c_t the tail counts: Σ_j max_{t∈j} c_t ≤ ΣA ≤ Σ c_t, and the first and last masks' cardinalities lie between the max and the sum of c_t over their window (equality at W = 1, which is your item 1) | L1 |
| At W = 1: A ≤ the number of tail ticks with a positive count; at least max c_t cells have A > 0; at most min c_t cells have A = n | L1 |
| The header holds no NaN or infinity (`json.loads` reads them; `canonical_json` raising on them was not caught in round 1); every array hash in the header is a 64-hex string | L1 |

L1 checked the whole set two ways: the five full test runs' unaltered records still parse, and a new test (`test_consistency_relations_hold_on_arbitrary_tails`) computes the summaries of eight synthetic binary tails by the probe's formula (independent cells, persistent cells, flicker, sparse, empty, full, a tail that dies part-way, isolated bursts) and requires every relation to hold on each. The relations remain necessary and not sufficient, and the module docstring now says so under WHAT VALIDATES A RECORD, with parsing, replay and authentication as three separate things. The replay-only forgery test is kept: moving one active tail tick between two cells still parses and is still refused by replay.

### R2 — the retired list

`RETIRED_MASTERS` now holds 21 values: every master declared in the placed E1 and Flight 8 source, and the probe's. L1 confirmed each from the fresh clone before listing it.

| Source | Values |
|---|---|
| `e1/config.py` | 20260917 |
| `e1/null.py` | 202609171, 202609172 |
| `e1/audit.py` (named retired in `f8/audit.py`) | 202609221, 202609222, 202609223 |
| `e1/projection.py` | 202609301, 202609302, 202609303, 202609304 |
| `f8/config.py` | 20261026, 120261026, 920261102 |
| `f8/null.py` | 220261026, 320261027 |
| `f8/closure.py` | 420261028 |
| `f8/evaluator.py` | 520261028 |
| `f8/audit.py` (prefixes 6, 7, 8 on placement date 20261102) | 620261102, 720261102, 820261102 |
| `design/flight9/probe/f9_probe.py` | 9920261112 |

This is the wider scope of your second table, taken now. L1's reason: every value was a declared master of an earlier instrument, excluding one costs nothing, and "fresh masters throughout" is simpler to hold with the whole inventory out. If Mike's later master-governance ruling narrows or widens the list, that is a reviewed change to this declaration. Stage-to-stage uniqueness within Flight 9 is stated in the docstring as the runner's; a static list cannot give it.

The stream declaration digest changes: `f7ba30034d74f23e…` → `3274f728c79b6d44b3b2b0b685a4d7526ab0f4cd16f1d5e0e1bc72407e231832`. The preflight now requires the list to have exactly 21 distinct entries, each a stage-class integer.

The test no longer iterates the list under test. `test_every_earlier_master_is_refused_l2_m2_round1_r2` holds a table of (placed source file, integer literals that must appear in it, masters they give), parses each file with `ast`, requires the literals to be there, and requires the grounded set to equal `RETIRED_MASTERS`. Each of the 21 is then refused by `check_master`, `master_class`, `check_run_identity`, `stream_key`, `F9RunSpec.check`, `F9RunSpec.stream_key`, `generator_from_key` and `init_pattern_generator`. Six fresh values, including neighbours of retired ones, are accepted as controls.

### M2-7 — wording

The docstring's sentence "The header carries no value that passes through libm" is replaced. It now says: the writing machine's η₀ and q are not serialized (the floor is its probability literal and rule, deactivation is μ); the header does carry the arm's spr and g_spec as the identity record states them and g = κ·g_spec; g_spec derives from the identity record's q, which passed through exp on the machine that built the bundle. The encoding is unchanged.

**M2-7 as now declared.** 8-byte magic, 4-byte little-endian header length, canonical-JSON header, then counts (int32), and per W: A, R₀ (uint16), first, last (packed bits). η₀ and q are stated by rule, not by value; spr, g_spec and g are the identity record's values and what follows from them.
**M2-8 as now declared.** `parse_run`: form with exact JSON types, declarations, array hashes, and the necessary relations listed in `_check_consistency`. `replay_equals`: same-machine rerun to the same bytes under a given arm context. Authentication of the context and of the record is the runner's.
**M2-3 as now declared.** As in round 1, with the 21-value exclusion.

## 2. Changed files

| File | Round 1 | Round 2 |
|---|---|---|
| `f9/streams.py` | `1d1bbc48abe1df54…` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` |
| `f9/dynamics.py` | `11ad2ef15ef30520…` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` |
| `tests/test_f9_m2.py` | `c8c3e1f9a01b2193…` | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` |

The three round-1 files are in the packet as byte copies under `packet_only/round1/` (not for placement).
- `streams.py`: the retired list and its comment lines; the docstring's sentence on what a master may not be; the 21-entry preflight condition; the digest literal. Nothing else.
- `dynamics.py`: the SERIALIZATION paragraph of the docstring and the new WHAT VALIDATES A RECORD paragraph; in `parse_run`, the header read (non-finite values), the two typed list comparisons through the new `_int_list_is`, and the hex check on array hashes; `_check_consistency` rewritten with its docstring. `step`, `local_density`, `activation_probability`, `arm_context`, `F9RunSpec`, `initial_state`, `_Windows`, `run`, `run_header`, `serialize_run`, `replay_equals` and `reduction_check` are untouched. `RUN_SCHEMA` stays 1: no byte of a serialized record changed.
- `test_f9_m2.py`: 59 tests → 63. New: the R2 test above; the synthetic-tail test named in §1; `test_impossible_summaries_are_refused_by_the_parser_l2_m2_round1_r1` (your R1a and R1b constructions, a nested-segment case that only the segment relation can refuse, a coarse-end case, and activity recorded after extinction; each asserted refused for its intended reason, with the unaltered record as control); `test_undeclared_json_types_are_refused_l2_m2_round1_r1c` (your two witnesses, seven more type and length cases, and the three non-finite tokens). Changed: `test_undeclared_runs_and_masters_are_refused` no longer iterates `R.RETIRED_MASTERS`. Two imports added.

## 3. Evidence

- `build_records/f9_m2_module_container_round2_2026-11-17.txt` — **63 passed in 36.52 s** in L1's container (Python 3.13.18, NumPy 2.5.3).
- `build_records/l2_m2_round1_reproduce.py` (`27f4a324…`) and `build_records/l2_m2_round1_check_windows.py` (`da087bbc…`) — your programs as extracted; say if either differs from what you wrote.
- `build_records/f9_m2_l2_round1_reproduce_on_round1_2026-11-17.txt` — Appendix A's output on the round-1 packet.
- `build_records/f9_m2_l2_round1_check_windows_on_round2_2026-11-17.txt` — Appendix B's output on the round-2 source.
- `build_records/l1_m2_round1_witnesses_adapted.py` with `build_records/f9_m2_l1_adapted_witnesses_on_round1_2026-11-17.txt` and `build_records/f9_m2_l1_adapted_witnesses_on_round2_2026-11-17.txt` — the table of §1.
- For reference, as byte copies: `build_records/L1_TO_L2_F9_M2_BUILD_PACKET_2026-11-17.md`, `build_records/f9_m2_module_container_2026-11-17.txt`.
- The contract, freeze record and addendum, notation ruling, pre-probe declaration, probe source, the M1 placement records and the whole of `mfa_instrument` at the pin, as in round 1.

## 4. Disclosures

1. **Mike did not state a choice on the scope of R2.** L1 offered two (all earlier masters, or the minimum of the three) with a recommendation for the first; his reply was "continue". The wider list is L1's recommendation carried out, and it is reported to him as such.
2. **The added relations are L1's reasoning, not derived by exhaustive search.** Each is argued in the `_check_consistency` docstring and holds on every record the tests produce and on the eight synthetic tails. L1 has not shown the set complete, and a parser cannot be: Q3 asks you to attack both directions, a true record refused and an impossible one accepted.
3. **A relation that is wrong would refuse true records of record.** That would stop a job, visibly. The five full runs (realization and skeleton, extinct and surviving, three arms) all parse, and the synthetic tails satisfy every relation. That is evidence, not proof.
4. **Carried from your round 1, for the runner and not for M2:** the master-draw procedure goes to Mike before the runner is built; §2.8's persistence of the raw index and the local margin (once per arm and arm/level); the runner envelope binding the whole serialized run's digest, the authorized bundle, the source, and the evaluator and qualification identities once they exist. L1 has recorded these and will carry them into the runner's design.
5. **Unchanged from round 1:** test masters only; no occupancy map rendered and nothing computed against an index contour; L1 has not seen the boundary endpoint; size about 141.6 kB per run, about 12.6 GB at 89,000 runs, unpriced on the canonical machine.

## 5. Questions

**Q1.** R1 and R2: CLOSED, CLOSED WITH NOTE, or NOT CLOSED (say what remains). Include the M2-7 wording.
**Q2.** Declarations M2-3, M2-7 and M2-8 as now stated: ACCEPTABLE, REQUIRES CHANGE, or REJECT.
**Q3.** `_check_consistency`: is any listed relation false for some record the rule can produce (a true record refused)? Is there still a record that contradicts its own stored quantities and parses?
**Q4.** The retired list: is any master declared in the packet's source missing from it, and is any entry not grounded in that source?
**Q5.** Anything else to repair before placement.

## 6. Return format

One downloadable `.md` file, receipt table first. If you find a defect, include a program that reproduces it on the packet's bytes. End with exactly one line, plain, at column 0, with no bold and no trailing text:
`FINAL VERDICT: SOUND`
`FINAL VERDICT: DEFECT-WITH-REPAIR`

*L1, 2026-11-17. Nothing placed; no run on the canonical machine; no placed file modified.*
