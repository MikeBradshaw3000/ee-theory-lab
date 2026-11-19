# L1 → L2 — Flight 9 test repair: the folder-listing assertion in three placed test files

**Date:** 2026-11-18. **Register:** repair of placed, L2-cleared test bytes (receipt first). Not a run authorization. No source file of the instrument is touched.
**Repository pin:** `ee-theory-lab` `main` at `068b5b390f0b5e70565546fe530e1273cd780627` (the M5 placement), checked against the remote before this packet was built. Nothing of this repair is committed. Every file in this zip that exists at the pin and is not one of the three repaired files is a byte copy of it.
**Decision authority:** Mike. Made at his word "test repair first" (2026-11-18).

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: DEFECT-WITH-REPAIR`.

## 1. The defect (L1's; you reproduced it in M5 rounds 1 and 2)

`test_f9_m2.py`, `test_f9_m3.py` and `test_f9_m4.py` each assert that the `f9` folder holds exactly the files placed up to their own module. Each assertion fails once a later module is placed. At the pin all three fail. No placement reran an earlier module's tests, so it was not seen until M5.

## 2. The repair

| File | At the pin | Repaired |
|---|---|---|
| `tests/test_f9_m2.py` | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` | `e505cd6bd302c1e005b37f4bc4ad364300b83fd4ab40bb73ac6ef18c0084073a` |
| `tests/test_f9_m3.py` | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` |
| `tests/test_f9_m4.py` | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` |

The whole change is `build_records/f9_test_repair_2026-11-18.diff` (`d86c30ada62d7c3b…`), 13 lines added and 5 removed. The three files as they are at the pin are in the packet under `packet_only/before/` (not for placement).

**In each file, one assertion.** The line that required the folder's `.py` files to EQUAL the pinned files plus the module's own is replaced by one that requires them to be PRESENT (a subset test), with a two-line comment saying why. This is the form M5's own test has, which you accepted. Every per-file digest assertion is kept as it was: the `PLACED` dictionaries, the loop over them, and the digest of the package root, `e1`, `f8` and `gates` are untouched.

**In `test_f9_m4.py`, one docstring as well.** Your M4 round-2 review (§3) noted that the helper `_genuine_arms` says its fixtures cover "each set of A4 causes" when they cover five of the seven. The M4 placement note held that wording for the file's next touch. This is that touch. The docstring now names the five sets and says the two missing pairs occur in the 6,000-sweep test. No fixture and no assertion is changed.

By comparison of the parsed top-level definitions before and after: `test_f9_m2.py` — `test_m1_e1_and_f8_are_byte_unchanged` only; `test_f9_m3.py` — `test_everything_placed_before_m3_is_byte_unchanged` only; `test_f9_m4.py` — `test_everything_placed_before_m4_is_byte_unchanged` and `_genuine_arms` (its docstring) only. No test is added or removed: 63, 37 and 21 tests as before.

## 3. What the repair gives up, stated plainly

The old line also asserted that no OTHER file was in the folder at the module's own placement. That check is gone from these three files. It was only ever true at one commit. What remains checked: every file the module depends on is present and byte-identical to its placed identity. A stray or altered file is caught where it matters: an altered pinned file fails its digest, and the packets' manifests and the placement scripts fix what is placed.

## 4. Evidence

- `build_records/f9_m1_to_m5_container_2026-11-18.txt` (`ae5a515e90222090…`) — the five module test files in one process on the repaired bytes at the pin: **250 passed in 876.47 s** in L1's container (Python 3.13.18): 102 + 63 + 37 + 21 + 27. This is the first time the five have been run together.
- Before the repair, at the pin, the three named tests fail and nothing else in M2 to M4 does (your M5 round-2 §6; L1 reran the three and saw the same).
- The packet carries `flights/mfa_fidelity/design/flight9/probe/f9_probe.py`, which one M2 test reads as source text. No probe output is in the packet.

To run: from `flights/mfa_fidelity/instrument`, `python -B -m pytest tests/test_f9_m1.py tests/test_f9_m2.py tests/test_f9_m3.py tests/test_f9_m4.py tests/test_f9_m5.py -v -p no:cacheprovider`. It takes about 15 minutes here; M1 is the longest. If that exceeds your execution window, say which files you completed.

## 5. Not in this repair

Nothing else held for a "next touch" is in these three files. The items held for other files stay held: M3's two cause strings (`evaluator.py`), the two optional parser bounds (`dynamics.py`), and the two Flight 8 test notes (`test_f8_m6.py`, `test_f8_mp1.py`).

## 6. Questions

1. Is the change in each file confined to what §2 states? An inverse-edit reconstruction of the three pinned identities from the repaired bytes would settle it.
2. Is the subset form an acceptable replacement, and is §3 a fair statement of what is no longer checked?
3. Is the new `_genuine_arms` docstring accurate?
4. Do the five module files pass together on your machine?
5. Anything else.
