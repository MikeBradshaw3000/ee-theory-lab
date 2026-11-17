# F9 M2 placement note (prepared 2026-11-17)

**Module.** Flight 9 instrument module M2: the stream of Contract F9 v0.7 §2.5, the hazard rule of §2.4 with a per-cell index, the three declared starts (§2.6, §5.8), one run and its record (§5.1, §2.11), the record's serialization with a parser and a replay check, and the comparison that the `reduction_check` job of §8 step 2 will make. Built at Mike's word "build m2" (2026-11-17). Placed against `main` at `7af50941e47249965dc6c8b2a502d06166e08866` (the M1 placement), checked against the remote on 2026-11-17 before the kit was built.

**Placed (instrument), all NEW; no placed file is edited:**

| File | SHA-256 |
|---|---|
| `mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` |
| `mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` |
| `tests/test_f9_m2.py` (63 tests) | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` |

These are the bytes of L2's round-2 packet (`f9_m2_build_round2_L2.zip`, `2d162cd2f893fdb58dc531087c11c4fa031b96307dabcd4bccddb1cf236eb030`), which L2 cleared. `test_m1_e1_and_f8_are_byte_unchanged` holds the seven M1 files, the package root, `e1`, `f8` and `gates` to their LF identities at `7af5094`.

**Stream declaration digest in the placed source:** `3274f728c79b6d44b3b2b0b685a4d7526ab0f4cd16f1d5e0e1bc72407e231832` (`f9/streams.py`, `verify_stream_declaration`). It binds the key order and codes, the initialization-pattern role, the low start, the 21 retired masters, and the test-master limit. Every serialized run carries it.

**Review history (every L2 return a byte copy, `_RECEIVED`):**

| Round | L1 document | L2 return | Verdict |
|---|---|---|---|
| 1 | `L1_TO_L2_F9_M2_BUILD_PACKET_2026-11-17.md` `18db1d6e…` (packet `a17f5c16…`) | `L2_F9_M2_ROUND1_REVIEW_2026-11-17_RECEIVED.md` `7ba22c09dc86efe94d40148dc965f94256e748e259dacb3061e1dd86d43c7e5a` | DEFECT-WITH-REPAIR: R1 the parser accepted records that contradict their own stored quantities, and floats or booleans in integer lists; R2 the retired-master list omitted masters that earlier instruments declared; M2-7's wording |
| 2 | `L1_TO_L2_F9_M2_ROUND2_RESPONSE_2026-11-17.md` `c474d189…` (packet `2d162cd2…`) | `L2_F9_M2_ROUND2_REVIEW_2026-11-17_RECEIVED.md` `63915ffef47afaf49e23ecc1ff4cb3ec7d50624ee25a1070d1e4a8139387724a` | **SOUND**: R1 and R2 closed; M2-3, M2-7 and M2-8 acceptable as now declared; no further source repair |

Both defects were L1's. L2's two round-1 programs are committed as extracted (`l2_m2_round1_reproduce.py` `27f4a324…`, `l2_m2_round1_check_windows.py` `da087bbc…`) with their outputs, and L1's outcome-reporting adaptation of the first with its output on each round. L2's round-2 program is in its return in full; L1 extracted it (`d9ec51fc…`, equal to the hash L2 states) and reproduced its output on the round-2 packet.

**A limit of the parser, on record (L2 round 2, §4).** `parse_run` checks necessary relations between the stored quantities. It is not a feasibility certifier: L2 exhibits two records that no binary history could produce and that parse (a cell active in six 100-tick windows when five had any activity; an inactive-segment count that the tick counts exclude). The placed docstring says the relations are necessary and not sufficient, and that a record is established by replay. "Consistent" in any later citation of this module means "satisfies the enumerated necessary relations". L2 offers two further bounds (its §4.4) as optional; they are not in the placed bytes and are noted for the next touch of `dynamics.py`.

**Correction of L1's wording (L2 round 2, §6.1).** L1's round-2 response says "no byte of a serialized record changed". That is wrong as a statement about record identity: the header carries the stream declaration digest, which changed with the retired list, so a round-1 record is refused by the placed parser. What is unchanged is the schema, the array encoding and the layout. The cleared bytes are placed unchanged.

**The retired list's scope.** L1 offered Mike two scopes after round 1 (the whole earlier inventory, or the minimum L2 required) and recommended the first. Mike said "continue" and did not state a choice; L1 carried out its recommendation and told him and L2 so. The list of 21 is technically accepted by L2. It remains Mike's to narrow or widen under the master ruling.

**Declarations awaiting Mike's ratification, with the governance record:** M2-1 to M2-10 as listed in the round-1 packet document, with M2-3, M2-7 and M2-8 as restated in the round-2 response. L2's acceptance is a technical ruling and is not that ratification.

**Carried to the runner (L2 rounds 1 and 2; not obligations of M2):** Mike's ruling on how a master is produced and recorded, before the runner is built; refusal of test masters in jobs of record and uniqueness of masters across Flight 9's stages; persistence of the raw index and the local margin under §2.8, once per arm and per arm and level; the runner's record binding each whole serialized run, the authorized bundle, the source, and the evaluator and qualification identities once they exist; restriction of runs of record to arm contexts from the verified canonical bundle.

**Records placed with the module (container, noncanonical):** `f9_m2_module_container_2026-11-17.txt` (59 passed) and `f9_m2_module_container_round2_2026-11-17.txt` (63 passed); the outputs of L2's and L1's witness programs.

**Canonical module run (gate for the commit).** `python -m pytest tests\test_f9_m2.py -v -s -p no:cacheprovider` from `flights\mfa_fidelity\instrument` in the canonical environment, whole module, one process, on the placed bytes before commit. Its output is `f9_m2_module_canonical_2026-11-17.txt`, committed with this placement. The placement script stages nothing unless that run exits 0, and its identity of record is measured from a fresh clone after the commit. This is the first run of M2 off Linux. It runs the rule under test master 7 only.

**Not run at this placement:** the M1 module again, and the whole canonical suite. M2 adds two source files and a test file and edits nothing.

**What placement does NOT do.** No run is authorized and no authorization file exists. No job has been run: `build_identities` and `reduction_check` have not been executed as jobs. No master is drawn and the module holds none. The tests' runs use a test master, and their records are discarded with the tests' temporary directories.

**Carried.** L1 has not opened the probe arrays for any boundary purpose and has not seen the boundary-compatibility endpoint. In building and testing M2, L1 looked at run mechanics only (counts, extinction ticks, draw counts, window records); no occupancy map was rendered and nothing was computed against an index contour. Held list unchanged (Gemini commission v3.1; two next-touch test repairs; third-order lattice-versus-ODE comparison; onset continuity; PD7-versus-floor correspondence). Open from the M1 placement: the canonical machine's pre-rounding level counts differ from the container figures quoted in contract §3.4 step 3; for the governance record.

*L1, 2026-11-17.*
