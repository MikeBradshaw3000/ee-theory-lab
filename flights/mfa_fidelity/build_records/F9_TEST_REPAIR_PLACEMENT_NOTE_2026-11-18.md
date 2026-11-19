# F9 test repair placement note (prepared 2026-11-18)

**What this is.** A repair of three placed, L2-cleared test files. No source file of the instrument is touched. Made at Mike's word "test repair first" and placed at his word "place the repair. your recommendations are accepted", both 2026-11-18, against `main` at `068b5b390f0b5e70565546fe530e1273cd780627` (the M5 placement), checked against the remote before the kit was built.

**The defect, L1's.** `test_f9_m2.py`, `test_f9_m3.py` and `test_f9_m4.py` each asserted that the `f9` folder held exactly the files placed up to their own module. Each such assertion failed once a later module was placed. From the M3 placement on, `main` carried at least one failing test; at `068b5b3` it carried three. No placement reran an earlier module's tests, so it went unseen until M5 was built. L2 reproduced it in M5 rounds 1 and 2.

**EDITED (three placed files):**

| File | Before (at `068b5b3`) | After |
|---|---|---|
| `tests/test_f9_m2.py` | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` | `e505cd6bd302c1e005b37f4bc4ad364300b83fd4ab40bb73ac6ef18c0084073a` |
| `tests/test_f9_m3.py` | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` |
| `tests/test_f9_m4.py` | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` |

These are the bytes of L2's packet (`f9_test_repair_round1_L2.zip`, `8cdb1fd1ab88753b82cacd9933cb053e626b74d21d8ba01cdcd1386e5f9d8454`), which L2 cleared. The whole change is `f9_test_repair_2026-11-18.diff` (`d86c30ada62d7c3b…`): 13 lines added, 5 removed.

**The change.** In each file, the one assertion that required the folder's `.py` files to equal the pinned files plus the module's own now requires them to be present. Every per-file identity check is as it was. In `test_f9_m4.py`, also the docstring of the helper `_genuine_arms`, the wording L2 flagged in M4 round 2 and the M4 placement note held for this file's next touch: it now says the fixtures cover five of the seven sets of A4 causes and where the other two occur. No fixture, assertion or test count changes (63, 37 and 21 tests).

**Review.** `L1_TO_L2_F9_TEST_REPAIR_PACKET_2026-11-18.md` (`f2d7d695…`) → `L2_F9_TEST_REPAIR_ROUND1_REVIEW_2026-11-18_RECEIVED.md` (`d0de662865335ed3ec5cd203274273db9f63f7757551a91e94a2fbb78db60631`), **SOUND** in one round. L2 rebuilt all three prior identities byte for byte by reversing only the stated edits; ran the old and repaired functions against 30 altered package copies; and ran the five module files in one process: 250 passed in 669.56 s (Python 3.12.14). L1's container: 250 passed in 876.47 s (the committed record).

**What these three tests no longer check, in L2's words (its §3), which L1 adopts.** "These tests continue to verify the LF-normalized identities of their listed prior files and the presence of their own required module names. They now allow additional immediate `.py` names in `f9`; they do not determine whether those additions are authorized. Package completeness and permitted additions remain controlled by the reviewed packet and placement process."

**Two corrections to L1's packet document (L2, nonblocking). The document is placed as sent.**
- Its §3 said a stray or altered file "is caught where it matters" by manifests and placement scripts. L2 does not credit that: no placement script was in the packet, and the subset assertions do not detect a stray `f9` source file. The statement quoted above is the accurate one.
- Its §4 attributed "nothing else in M2 to M4 fails" to L2's M5 round-2 review. That round reran four tests only. The complete earlier run was in M5 round 1 (three folder-listing failures and one missing-file failure, the probe script L1 had not shipped). The attribution was L1's error.

**A limit that was there before and is unchanged (L2 §3).** Each module's own added files are required by NAME in that module's test and by CONTENT in the next module's test. M5's two source files are therefore pinned by content nowhere yet; the next module's test will pin them.

**Canonical run (gate for the commit), at Mike's choice.** The five module files in one process, `python -m pytest tests\test_f9_m1.py tests\test_f9_m2.py tests\test_f9_m3.py tests\test_f9_m4.py tests\test_f9_m5.py -v -s -p no:cacheprovider`, from `flights\mfa_fidelity\instrument` in the canonical environment, on the placed bytes before commit. Its output is `f9_m1_to_m5_canonical_2026-11-18.txt`, committed with this placement. The placement script stages nothing unless that run exits 0, and its identity of record is measured from a fresh clone after the commit. It is the first run of the five together on the canonical machine. If it fails, the three test files are left edited in the working copy and nothing is staged.

**Not in this repair.** Still held for their own files' next touch: M3's two cause strings (`evaluator.py`); the two optional parser bounds (`dynamics.py`); the two Flight 8 test notes (`test_f8_m6.py`, `test_f8_mp1.py`). Still awaiting Mike's word: the note beside the contract on the skeleton closure at κ = 1.00; an interpretation record for the T-S2 ruling and the range formula.

**What placement does NOT do.** No run is authorized and no authorization file exists. No job has been run. No master is drawn. This is not the whole canonical suite of the repository: it is the five Flight 9 module files.

**Carried.** L1 has not opened the probe arrays for any boundary purpose and has not seen the boundary-compatibility endpoint. Held list unchanged (Gemini commission v3.1; two next-touch test repairs; third-order lattice-versus-ODE comparison; onset continuity; PD7-versus-floor correspondence).

*L1, 2026-11-18.*
