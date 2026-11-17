# F9 M1 placement note (prepared 2026-11-17)

**Module.** Flight 9 instrument module M1, the identity build of Contract F9 v0.7 §3.4 step 4 (job `build_identities`, §8 step 1), as a new package `mfa_instrument/f9/` beside `e1` and `f8`. Built at Mike's word "build identities" (2026-11-16), scoped by him to module 1. Placed against `main` at `b2a567415bd0a7af1a71c7e8531f536f1950aa69`, checked from a fresh clone on 2026-11-17 before the kit was built.

**Placed (instrument), all NEW:**

| File | SHA-256 |
|---|---|
| `mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` |
| `mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` |
| `mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` |
| `mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` |
| `mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` |
| `mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` |
| `mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` |
| `tests/test_f9_m1.py` (102 tests) | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` |

These are the bytes of L2's round-3 packet (`f9_m1_build_round3_L2.zip`, `8cabe610de80d4a06addae4a0ba06905fd829b3dbe9c6c10d846abc295930d9a`), which L2 cleared. Nothing in the package root, `e1`, `f8` or `gates` is edited; `test_e1_and_f8_are_byte_unchanged` holds their LF identities at `b2a5674`.

**Declaration digest in the placed source:** `7fbef2ff2a04e9bc0825e6bbfeb70ce867d15cc51ec22e7b4eac0a6c0ff8a3b3` (`f9/config.py`, `verify_frozen_identity`). It binds the contract (`60cf50fc…`) and the freeze record (`66fa3d31…`). It does not bind the two verification tolerances of `identities.py` (`LIBM_ULPS = 2`, `DESCRIPTIVE_VARIANCE_ATOL = 1e-12`); those are bound through the instrument's source identity (L2 round 3, Q4).

**Review history (every L2 return a byte copy, `_RECEIVED`):**

| Round | L1 document | L2 return | Verdict |
|---|---|---|---|
| 1 | `L1_TO_L2_F9_M1_BUILD_PACKET_2026-11-16.md` `8a745405…` (packet `58bc4f4f…`) | `L2_F9_M1_ROUND1_REVIEW_2026-11-16_RECEIVED.md` `288928bf4061fbcf9d3077635e557c7e69cf7c912aecc5361f48268a1b833305` | DEFECT-WITH-REPAIR: R1 component identity omitted membership, and level byte order; R2 the deep verifier accepted four inconsistent records; R3 η₀ not bound to its rule |
| 2 | `L1_TO_L2_F9_M1_ROUND2_RESPONSE_2026-11-16.md` `e25829c3…` (packet `7b17fa67…`) | `L2_F9_M1_ROUND2_REVIEW_2026-11-16_RECEIVED.md` `14dbd122f7a0b9d5b57ad741f7987c1d846a291e31614aa7354a8c8845d97cb7` | DEFECT-WITH-REPAIR: R1, R3 closed; R2 open, the cross-machine comparator added the base-array 1e-12 to the spectral radius |
| 3 | `L1_TO_L2_F9_M1_ROUND3_RESPONSE_2026-11-16.md` `b539f3be…` (packet `8cabe610…`) | `L2_F9_M1_ROUND3_REVIEW_2026-11-16_RECEIVED.md` `e90e59bc411c67aed5a3fdb8aec8045d4d9c7ef47128fff35fc7dacdb448d0e2` | **SOUND**: R2 closed; M1-3 and every row of M1-11 acceptable; no further repair |

All three defects were L1's. L2's reproduction programs are committed as extracted (`l2_m1_round1_checks.py` `7b879eb2…`, `l2_m1_round2_checks.py` `25fe986a…`) with their outputs on the repaired source. L2's two round-3 programs are in its return in full; L1 extracted them (hashes equal to those L2 states) and reproduced its results on the round-3 packet.

**Correction of L1's wording (L2 round 3, Q5).** L1's round-3 response says the all-arm test accepts 0.999e-9 and refuses 1.001e-9 "above and below". The test accepts a value inside the bound on the upper side only; below, it has a refused case and no accepted one. L2 checked both sides independently (its Appendix B). The cleared bytes are placed unchanged.

**Declarations awaiting Mike's ratification, with the governance record:** M1-1 to M1-10 as listed in the round-1 packet document (M1-2, M1-3 and M1-5 as repaired in rounds 2 and 3), and M1-11 (the float rule of each quantity for a verification on another machine; round-3 response §2). L2's acceptance is a technical ruling and is not that ratification.

**Records placed with the module (container, noncanonical; they bind nothing):** `f9_m1_module_container_2026-11-16.txt`, `…_round2_…`, `…_round3_…` (67, 96 and 102 passed); `F9_M1_IDENTITIES_CONTAINER_2026-11-16.json`, `…_ROUND2_…`, `…_ROUND3_…` (round 2 and round 3 differ in `environment.platform` only); the four outputs of L2's programs on the round-2 and round-3 source.

**Canonical module run (gate for the commit).** `python -m pytest tests\test_f9_m1.py -v -s -p no:cacheprovider` from `flights\mfa_fidelity\instrument` in the canonical environment, whole module, one process, on the placed bytes before commit. Its output is `f9_m1_module_canonical_2026-11-17.txt`, committed with this placement. The placement script stages nothing unless that run exits 0, and its identity of record is measured from a fresh clone after the commit. This is the first run of M1 off the container. The registered family sizes it prints are that machine's and are reported, not asserted.

**Not run at this placement: the whole canonical suite** (`tests`, about seven hours at the M7 placement). M1 adds a package and a test file and edits nothing the other tests import. Whether to run it as a separate record is Mike's call.

**What placement does NOT do.** No run is authorized and no authorization file exists. The job `build_identities` has not been run: the tests build noncanonical bundles in temporary directories. No master is drawn; M1 holds no seed and no dynamics. The governance record, the remaining `f9` modules and Authorization 001 come later. The cross-machine rules of M1-11 have been exercised on one platform each, never between two.

**Carried.** L1 has not opened the probe arrays for any boundary purpose and has not seen the boundary-compatibility endpoint. Held list unchanged (Gemini commission v3.1; two next-touch test repairs; third-order lattice-versus-ODE comparison; onset continuity; PD7-versus-floor correspondence).

*L1, 2026-11-17.*
