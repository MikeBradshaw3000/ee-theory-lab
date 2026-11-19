| Receipt check | Recomputed / observed value | Result |
|---|---|---|
| Archive | `f9_test_repair_round1_L2.zip` | Verified |
| Archive SHA-256 | `8cdb1fd1ab88753b82cacd9933cb053e626b74d21d8ba01cdcd1386e5f9d8454` | MATCH to supplied value |
| Payload file count | 71 | MATCH |
| Total file count | 72: 71 payload files plus `MANIFEST.txt` | MATCH |
| Manifest entries and matched digests | 71 / 71 | MATCH |
| Missing or unlisted payload files | None | PASS |
| Duplicate ZIP names or manifest paths | None | PASS |
| ZIP integrity | No CRC errors | PASS |
| `MANIFEST.txt` SHA-256 | `8e78505cace2c298598b82b7d9ea9839c2b3eb0467c1d3a9f3e2971788634b3c` | Computed; manifest does not list itself |
| Receipt gate | Receipt returned before review; Mike subsequently said “execute” | SATISFIED |

| # | File, in manifest order | Recomputed full SHA-256 | Against `MANIFEST.txt` |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_TEST_REPAIR_PACKET_2026-11-18.md` | `f2d7d6954b317bda27e8b7ec7e4513c413b72857fa96d8c9d042a5d1add351a7` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `e505cd6bd302c1e005b37f4bc4ad364300b83fd4ab40bb73ac6ef18c0084073a` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/tests/test_f9_m3.py` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` | MATCH |
| 4 | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` | MATCH |
| 5 | `flights/mfa_fidelity/build_records/f9_test_repair_2026-11-18.diff` | `d86c30ada62d7c3b22cdb3b8383a8b53fdb260f2577ae774f07f6c8625bba484` | MATCH |
| 6 | `flights/mfa_fidelity/build_records/f9_m1_to_m5_container_2026-11-18.txt` | `ae5a515e902220908914425bf807935263e5fbb0f868e1b0f60f3f5b1debdd74` | MATCH |
| 7 | `packet_only/before/test_f9_m2.py` | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` | MATCH |
| 8 | `packet_only/before/test_f9_m3.py` | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` | MATCH |
| 9 | `packet_only/before/test_f9_m4.py` | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` | MATCH |
| 10 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 11 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 12 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 13 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 14 | `flights/mfa_fidelity/build_records/F9_M5_PLACEMENT_NOTE_2026-11-18.md` | `41dfe671983e295f01696a9b1d9c7fb20f0006be6e695b0d5a42ebd647de6e17` | MATCH |
| 15 | `flights/mfa_fidelity/build_records/L2_F9_M5_ROUND2_REVIEW_2026-11-18_RECEIVED.md` | `b0ea8c42e9c78fff192a16cc6b682af92614d72e2039c3f97446dd32d1f2b6a1` | MATCH |
| 16 | `flights/mfa_fidelity/build_records/F9_M4_PLACEMENT_NOTE_2026-11-18.md` | `b6004b9281aedc276b37244550baf9775853d5e678f7a1581b79fff754284839` | MATCH |
| 17 | `flights/mfa_fidelity/build_records/L2_F9_M4_ROUND2_REVIEW_2026-11-18_RECEIVED.md` | `d3391e61f22796899f5b148fcc1244c53660c8b81591b2dbee20bc9a61c2f5da` | MATCH |
| 18 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 19 | `flights/mfa_fidelity/instrument/tests/test_f9_m5.py` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` | MATCH |
| 20 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |
| 21 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 22 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 23 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 24 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 25 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 26 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 27 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 28 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 29 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 30 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 31 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 32 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 33 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py` | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/t0.py` | `a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 test repair review, round 1

**Date:** 2026-11-18. **Role:** L2, reviewer of the repair to placed test files. **Decision authority:** Mike.

**Reviewed archive:** `f9_test_repair_round1_L2.zip`. Recomputed SHA-256: **`8cdb1fd1ab88753b82cacd9933cb053e626b74d21d8ba01cdcd1386e5f9d8454`**.

**Disposition:** **SOUND.** The three folder-list failures are repaired without changing instrument source or existing digest checks. The M4 helper docstring is accurate, and all five F9 module files pass together: **250 passed**. The scope qualifications in Q2 and the historical evidence-attribution correction in Q5 are nonblocking.

The receipt was returned before review, and this review began after Mike's “execute.” This file repeats the complete receipt above. The technical disposition applies to the submitted test bytes and the verified packet; it does not authorize placement or scientific jobs.

## 1. Source register and scope

The packet identifies repository pin `068b5b390f0b5e70565546fe530e1273cd780627`, the M5 placement. The comparisons here establish the submitted bytes' continuity with the included prior files and the previously reviewed M5 packet. Remote repository HEAD was not independently fetched. [P, introductory metadata.]

References use the following keys. Paths are relative to `flights/mfa_fidelity/` unless otherwise stated.

| Key | Source |
|---|---|
| P | `build_records/L1_TO_L2_F9_TEST_REPAIR_PACKET_2026-11-18.md` |
| D | `build_records/f9_test_repair_2026-11-18.diff` |
| T2 | `instrument/tests/test_f9_m2.py` |
| T3 | `instrument/tests/test_f9_m3.py` |
| T4 | `instrument/tests/test_f9_m4.py` |
| T1, T5 | `instrument/tests/test_f9_m1.py` and `instrument/tests/test_f9_m5.py` |
| BEFORE | Archive-root `packet_only/before/test_f9_m2.py`, `packet_only/before/test_f9_m3.py`, and `packet_only/before/test_f9_m4.py` |
| M4R2 | `build_records/L2_F9_M4_ROUND2_REVIEW_2026-11-18_RECEIVED.md` |
| M5R2 | `build_records/L2_F9_M5_ROUND2_REVIEW_2026-11-18_RECEIVED.md` |
| M4PN, M5PN | `build_records/F9_M4_PLACEMENT_NOTE_2026-11-18.md` and `build_records/F9_M5_PLACEMENT_NOTE_2026-11-18.md` |
| L1LOG | `build_records/f9_m1_to_m5_container_2026-11-18.txt` |

All **51 Python source files** under `instrument/mfa_instrument/` have exactly the same paths and raw bytes as the reviewed M5 round-2 packet. T1 and T5 are also unchanged. The repair changes only T2, T3, and T4; no instrument source is altered. [Current and prior packet manifests; independent raw-byte comparison; P §§2, 5.]

## 2. Q1 — Exact scope and inverse reconstruction

**Answer: the changes are confined exactly to P §2.**

Starting from each repaired file, I reversed only its subset assertion and accompanying two-line comment. For T4 I also reversed the one disclosed `_genuine_arms` docstring replacement. Each result is byte-identical to the corresponding BEFORE file and to that test file in the previous M5 round-2 packet. No other edit was needed.

| File | Reconstructed prior SHA-256 | Repaired SHA-256 |
|---|---|---|
| T2 | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` | `e505cd6bd302c1e005b37f4bc4ad364300b83fd4ab40bb73ac6ef18c0084073a` |
| T3 | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` |
| T4 | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` |

These are exact raw-byte reconstructions. They are stronger than an AST-only comparison and distinct from the existing preservation functions' LF-normalized hashing. The reconstructed hashes agree with P's declared prior identities, the manifest's BEFORE entries, and the earlier verified packet. [P §2; BEFORE; M5R2 receipt.]

The parsed-definition and statement comparisons confirm:

| File | Changed definitions | Executable change |
|---|---|---|
| T2 | `test_m1_e1_and_f8_are_byte_unchanged` | Its folder-membership assertion only; current line 661 |
| T3 | `test_everything_placed_before_m3_is_byte_unchanged` | Its folder-membership assertion only; current line 536 |
| T4 | `test_everything_placed_before_m4_is_byte_unchanged`; `_genuine_arms` | Preservation assertion only, current line 563; helper docstring only, lines 254–257 |

No top-level definition was added or removed. In each preservation function, the number and order of executable statements are unchanged, and the membership assertion is the only changed statement. Each `PLACED` assignment, per-file digest loop, `_sha_lf` helper, `UNTOUCHED` value, and aggregate hashing loop remains identical. [T2:641–667; T3:514–542; T4:540–569; BEFORE comparison.]

D is a faithful representation of the changes: **13 lines added, 5 removed**, SHA-256 `d86c30ada62d7c3b22cdb3b8383a8b53fdb260f2577ae774f07f6c8625bba484`. Its hunks match an independently generated before/after diff, and its Git blob-index prefixes also recompute correctly.

Test inventory is preserved. The distinction between Python test functions and parameter-expanded test items is:

| File | Test functions before → after | Collected test items before → after |
|---|---:|---:|
| T2 | 26 → 26 | 63 → 63 |
| T3 | 26 → 26 | 37 → 37 |
| T4 | 21 → 21 | 21 → 21 |

The decorators and parameter inputs are unchanged. The combined run in §5 independently confirms the repaired files' collected-item counts.

## 3. Q2 — Subset form and the precise protection retained

**Answer: the subset form is acceptable. P §3 fairly identifies the central tradeoff, with the scope qualifications below.**

Each repaired assertion parses as:

~~~python
(pinned_names | current_module_names) <= observed_py_names
~~~

The AST is a single less-than-or-equal comparison whose left operand is the set union. Python therefore compares the complete required set against the observed names. It does not compare only the module's own names before applying the union. [T2:661; T3:536; T4:563.]

| Preservation test | Historical `PLACED` names, individually digest-checked | Own module names required to be present | Total required names |
|---|---:|---|---:|
| M2 | 7 | `dynamics.py`, `streams.py` | 9 |
| M3 | 9 | `evaluator.py` | 10 |
| M4 | 10 | `outcomes.py` | 11 |

The seven M1 names are `__init__.py`, `config.py`, `terrain.py`, `geometry.py`, `family.py`, `spectral.py`, and `identities.py`. M3 additionally pins M2's two sources; M4 additionally pins M3's evaluator. All basenames are distinct, and the pinned names do not overlap each test's own added names. Conversion from lists to sets therefore hides no duplicate-name problem in these submitted declarations. [T2:641–649; T3:514–524; T4:540–551.]

### What remains checked

Every listed `PLACED` member must still exist and match its **LF-normalized** SHA-256. `_sha_lf` replaces CRLF with LF before hashing. The test's own added files remain required by name. They were not content-hashed by that test's old filename-equality assertion, and the repair does not pretend otherwise. Later tests in the current chain supply the corresponding placed identities: M3 pins M2's sources, M4 pins M3's source, and M5 pins M4's source. [T2:653–661; T3:528–536; T4:555–563; T5:765–789.]

The unchanged `UNTOUCHED` guard hashes names and LF-normalized contents of immediate `.py` entries in the package root and the `e1`, `f8`, and `gates` directories. That traversal remains nonrecursive. The repair changes neither its scope nor its hash value. [T2:662–667; T3:537–542; T4:564–569.]

### What the repair intentionally stops checking

The removed equality rejected additional immediate names ending in `.py` in `f9`. It did not reject every possible extra file or recursively police the tree. The new subset assertion accepts such additional names, whether they are later authorized modules or unrelated additions.

That is the appropriate behavior for a historical dependency-preservation test that must continue running after later modules are added. It also means these tests no longer certify the exact current `f9` inventory. M5 already uses this same subset approach. [BEFORE membership assertions; T2:661; T3:536; T4:563; T5:787–789.]

P §3's appeal to manifests and placement scripts describes a separate control. The current archive's manifest was verified, but no placement script is supplied here; this review does not certify a script's enforcement or credit the subset assertions with detecting arbitrary stray `f9` source files.

The precise accepted statement is:

> These tests continue to verify the LF-normalized identities of their listed prior files and the presence of their own required module names. They now allow additional immediate `.py` names in `f9`; they do not determine whether those additions are authorized. Package completeness and permitted additions remain controlled by the reviewed packet and placement process.

This qualifies the disclosure without requiring another code repair.

### Independent mutation witnesses

I executed the original and repaired preservation functions themselves against isolated package copies. All **30 scenarios / 60 function evaluations** behaved as expected. The submitted files were not modified.

| Scenario, repeated for M2, M3, and M4 | Original function | Repaired function |
|---|---|---|
| Current M5 package, including later modules | FAIL | PASS |
| Historical required `.py` names only | PASS | PASS |
| Add `extra_unregistered.py` | FAIL | PASS |
| Add `extra.txt` | PASS | PASS |
| Remove pinned `config.py` | Missing-file failure | Missing-file failure |
| Append bytes to pinned `config.py` | Digest failure | Digest failure |
| Change only pinned `config.py` line endings to CRLF | PASS | PASS |
| Remove a module's own required source file | FAIL | FAIL |
| Append bytes to that module's own source file | PASS in this preservation function | PASS in this preservation function |
| Append bytes to `f8/config.py` | Aggregate-digest failure | Aggregate-digest failure |

The own-file mutation result describes the preservation function's existing limit, not the behavior of the entire five-module test suite. The extra-source witness makes the intentional loss of exact-inventory checking concrete. Appendix A contains the exact executed audit program.

## 4. Q3 — Accuracy of the revised `_genuine_arms` docstring

**Answer: accurate; the deferred wording correction is closed.**

The helper's executable source and AST are unchanged after removing the initial docstring. Calling its prior and repaired versions produces equal nested records for all **17 named fixtures**, covering all four arm rules. The A4 fixtures contain precisely five distinct nonempty cause sets. This agrees with the earlier M4 review and the held item in the placement note. [T4:253–268; M4R2 §3, line 194; M4PN, line 33.]

For the table below, **I** means `insufficient informative levels`, **A** means `isolated adverse level`, and **F** means `finite resolution`.

| A4 cause set | Present in `_genuine_arms`? | Occurrences in the deterministic 6,000-sweep sample |
|---|---:|---:|
| I | Yes | 66 |
| A | Yes | 76 |
| F | Yes | 413 |
| I + A | No | 17 |
| I + F | No | 17 |
| A + F | Yes | 650 |
| I + A + F | Yes | 2 |
| **Total A4 samples** | | **1,241** |

I independently reproduced the test's PCG64 stream from `SeedSequence([4, 4, 4, 1])` and classified the 6,000 generated 25-level strings directly from the arm-rule conditions. The two cause pairs absent from the helper occur seventeen times each. Their first witnesses are:

| Pair | One-based trial | Exact level-code string |
|---|---:|---|
| I + F | 58 | `NNNNNNNNNNNUUNNNNNNNNNNNN` |
| I + A | 235 | `NNNNANNNNNNNNNNNNNANNNNNN` |

One witness for each of the seven A4 cause sets was also checked through the production `arm_tier`; all seven agreed. The other draw counts were A1 = 3,177, A2 = 1,451, and A3 = 131, summing with A4 to 6,000. These are the observed counts in this review's NumPy 2.3.5 environment. [T4:24, 200–213; independent enumeration.]

The new wording accurately distinguishes the helper's five-set fixture coverage from the seven-set coverage of the separate randomized test. No fixture, assertion, mutation count, or scientific rule was changed to obtain that wording.

## 5. Q4 — Combined execution of M1 through M5

**Answer:** **Yes — 250 passed in 669.56 seconds, exit code 0.** No tests were deselected, skipped, or stopped early.

The five test files were run in the requested order in **one pytest process**, from `flights/mfa_fidelity/instrument`:

~~~bash
python -B -m pytest \
  tests/test_f9_m1.py \
  tests/test_f9_m2.py \
  tests/test_f9_m3.py \
  tests/test_f9_m4.py \
  tests/test_f9_m5.py \
  -v -p no:cacheprovider
~~~

The invocation used a dedicated temporary directory, the existing local pytest dependencies and instrument directory on `PYTHONPATH`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, and bytecode writing disabled. It ran the submitted test files unmodified.

**Environment:** Linux; Python 3.12.14; pytest 9.2.0; pluggy 1.7.0; NumPy 2.3.5; SciPy 1.17.0.

| Module test file | Collected | Passed |
|---|---:|---:|
| test_f9_m1.py | 102 | 102 |
| test_f9_m2.py | 63 | 63 |
| test_f9_m3.py | 37 | 37 |
| test_f9_m4.py | 21 | 21 |
| test_f9_m5.py | 27 | 27 |
| **Total, one process** | **250** | **250** |

The exact pytest summary was:

~~~text
======================= 250 passed in 669.56s (0:11:09) ========================
~~~

All three repaired preservation tests passed within this process. The retired-master test and the complete M5 file also passed. The previously reported folder-list failures are therefore closed on these repaired bytes. Appendix C reproduces the complete console transcript.

L1LOG independently reports **250 passed in 876.47 seconds** in L1's Python 3.13.18 environment. Its 250 test identifiers and 250 PASSED results are internally consistent, including one diagnostic printed between a test identifier and its pass status. L2's result above is a separate execution, not a restatement of that supplied log. [P §4; L1LOG.]

## 6. Q5 — Evidence wording and remaining scope

### N1 — Nonblocking correction to the historical test attribution

P §4 attributes “the three named tests fail and nothing else in M2 to M4 does” to M5R2 §6. That prior review documents **four focused earlier tests**, with one pass and three failures. It explicitly states that the entire earlier M1–M4 suite was not rerun in that round. [P, line 38; M5R2, lines 317–341.]

The appropriate distinction is:

- The earlier full run in M5 round 1 found the three folder-list failures and the missing probe-source dependency.
- M5 round 2 reran those four implicated tests. The supplied source dependency resolved the retired-master test; the three folder-list failures remained.
- This review runs all five module files together on the repaired bytes and reports that result in §5.

The packet should not describe the focused M5 round-2 check as a new complete pre-repair M2–M4 execution at the current pin. This is an attribution and recency correction, not evidence of another failing test or a reason to reject the repair.

### Other held items

The instrument source has not changed, and the other held changes remain outside this repair. P §5 names the evaluator cause strings, optional dynamics parser bounds, and two Flight 8 test notes. This review neither closes those items nor imports them into the three repaired files. The M4 helper docstring is the one applicable next-touch item actually addressed here. [P §5; M4PN; M5PN.]

The broad regression result concerns the **five supplied F9 module test files**. It does not claim execution of every test in the wider repository or any canonical scientific job. The probe script was supplied as a source dependency for the retired-master test; probe output was not used.

## 7. Review disposition

The repair is confined to the disclosed assertions and docstring, its inverse edits reconstruct all three prior identities exactly, and its behavior preserves the intended historical digest and required-name checks. The new subset condition deliberately permits later source files; the review records that loss of exact-inventory checking explicitly.

The helper documentation now matches its actual fixtures and the separate seven-set sweep coverage. The complete 250-test combined run passes. No blocking defect remains in this repair. The nonblocking qualifications above concern the description of coverage and prior execution, not an additional required change to these test bytes.

L2 clears the submitted repair technically. Mike retains placement and governance authority; the other held items remain held.

## Appendix A — Executed preservation-function mutation audit

The exact audit program below executes the old and repaired preservation functions against isolated copies. To reproduce it, save it as `audit_work/subset_semantics/check_subset.py` under the extracted archive root, creating the parent directories, and run `python -B audit_work/subset_semantics/check_subset.py` from that root. It uses the standard library and does not alter the submitted package.

Program SHA-256: `d01162c6f924b42d7b93bc6ffa7ae004b0f13ec54913a4cbbdb8f9ff46ef739b`.

```python
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'flights/mfa_fidelity/instrument/mfa_instrument'
TESTS=ROOT/'flights/mfa_fidelity/instrument/tests'
BEFORE=ROOT/'packet_only/before'
FUNCS={2:'test_m1_e1_and_f8_are_byte_unchanged',3:'test_everything_placed_before_m3_is_byte_unchanged',4:'test_everything_placed_before_m4_is_byte_unchanged'}
OWN={2:{'dynamics.py','streams.py'},3:{'evaluator.py'},4:{'outcomes.py'}}


def load_test(path,pkg,fn):
    tree=ast.parse(path.read_text())
    defs=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ('_sha_lf',fn)]
    vals={}
    for x in tree.body:
        if isinstance(x,ast.Assign):
            for t in x.targets:
                if isinstance(t,ast.Name) and t.id in ('PLACED','UNTOUCHED'):
                    vals[t.id]=ast.literal_eval(x.value)
    ns={'hashlib':hashlib,'os':os,'PKG':str(pkg),**vals}
    exec(compile(ast.Module(body=defs,type_ignores=[]),str(path),'exec'),ns)
    return ns[fn], vals, next(d for d in defs if d.name==fn)


def outcome(fn):
    try: fn()
    except (AssertionError,FileNotFoundError) as ex: return type(ex).__name__
    return 'PASS'


results=[]
with tempfile.TemporaryDirectory(prefix='copies_',dir=ROOT/'audit_work/subset_semantics') as td:
    for n,fn in FUNCS.items():
        cp=Path(td)/f'm{n}'; shutil.copytree(PKG,cp)
        new,vals,node=load_test(TESTS/f'test_f9_m{n}.py',cp,fn)
        old,oldvals,_=load_test(BEFORE/f'test_f9_m{n}.py',cp,fn)
        assert vals==oldvals
        expr=next(a.test for a in node.body if isinstance(a,ast.Assert) and isinstance(a.test,ast.Compare) and isinstance(a.test.ops[0],ast.LtE))
        assert len(expr.ops)==1 and isinstance(expr.left,ast.BinOp) and isinstance(expr.left.op,ast.BitOr)
        pinned={p.split('/')[1] for p in vals['PLACED']}
        assert len(pinned)==len(vals['PLACED']) and not pinned & OWN[n]
        expected=pinned|OWN[n]
        scenarios={}
        def check(label,wanted):
            got={'before':outcome(old),'after':outcome(new)}
            assert got==wanted,(n,label,wanted,got)
            scenarios[label]=got
        check('actual_M5_package',{'before':'AssertionError','after':'PASS'})
        for p in (cp/'f9').glob('*.py'):
            if p.name not in expected: p.unlink()
        check('historical_required_names_only',{'before':'PASS','after':'PASS'})
        p=cp/'f9/extra_unregistered.py';p.write_text('# deliberately extra\n')
        check('extra_top_level_py',{'before':'AssertionError','after':'PASS'});p.unlink()
        p=cp/'f9/extra.txt';p.write_text('ignored by both old and new\n')
        check('extra_non_py',{'before':'PASS','after':'PASS'});p.unlink()
        p=cp/'f9/config.py';original=p.read_bytes();p.unlink()
        check('missing_pinned_file',{'before':'FileNotFoundError','after':'FileNotFoundError'});p.write_bytes(original)
        p.write_bytes(original+b'\n# mutation\n')
        check('changed_pinned_file',{'before':'AssertionError','after':'AssertionError'});p.write_bytes(original)
        p.write_bytes(original.replace(b'\n',b'\r\n'))
        check('pinned_CRLF_only_change',{'before':'PASS','after':'PASS'});p.write_bytes(original)
        own=sorted(OWN[n])[0];p=cp/'f9'/own;original=p.read_bytes();p.unlink()
        check('missing_module_own_file',{'before':'AssertionError','after':'AssertionError'});p.write_bytes(original)
        p.write_bytes(original+b'\n# module-own mutation\n')
        check('changed_module_own_file',{'before':'PASS','after':'PASS'});p.write_bytes(original)
        p=cp/'f8/config.py';original=p.read_bytes();p.write_bytes(original+b'\n# inherited-package mutation\n')
        check('changed_f8_top_level_file',{'before':'AssertionError','after':'AssertionError'});p.write_bytes(original)
        results.append({'module':f'M{n}','pinned_count':len(pinned),'pinned_names':sorted(pinned),'own_presence_only':sorted(OWN[n]),'required_count':len(expected),'precedence':'(pinned_names | module_own_names) <= observed_py_names','scenarios':scenarios})
report={'status':'PASS','scope':'isolated copies; only the two original preservation functions executed, no instrument source imported or flight jobs run','modules':results,'scenarios':sum(len(x['scenarios']) for x in results),'function_evaluations':2*sum(len(x['scenarios']) for x in results)}
out=ROOT/'audit_work/subset_semantics/result.json';out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
```

## Appendix B — Verified submitted diff

This is the exact supplied diff, whose hunks and identities were independently checked in Q1. Reversing only these changes reconstructs the three BEFORE identities reported there.

```diff
diff --git a/flights/mfa_fidelity/instrument/tests/test_f9_m2.py b/flights/mfa_fidelity/instrument/tests/test_f9_m2.py
index 8d2de97..dcce06a 100644
--- a/flights/mfa_fidelity/instrument/tests/test_f9_m2.py
+++ b/flights/mfa_fidelity/instrument/tests/test_f9_m2.py
@@ -656,7 +656,9 @@ def _sha_lf(path):
 
 def test_m1_e1_and_f8_are_byte_unchanged():
     for rel, want in PLACED.items(): assert _sha_lf(os.path.join(PKG, *rel.split("/"))) == want, rel
-    assert sorted(fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")) == sorted([r.split("/")[1] for r in PLACED] + ["dynamics.py", "streams.py"])
+    # The files this module added are present beside them. The folder is not required to hold nothing else: this line
+    # first required exactly that and failed as soon as a later module was placed (repaired 2026-11-18).
+    assert {r.split("/")[1] for r in PLACED} | set(["dynamics.py", "streams.py"]) <= {fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")}
     h = hashlib.sha256()
     for sub in ("", "e1", "f8", "gates"):
         d = os.path.join(PKG, sub)
diff --git a/flights/mfa_fidelity/instrument/tests/test_f9_m3.py b/flights/mfa_fidelity/instrument/tests/test_f9_m3.py
index 245f816..b73a70f 100644
--- a/flights/mfa_fidelity/instrument/tests/test_f9_m3.py
+++ b/flights/mfa_fidelity/instrument/tests/test_f9_m3.py
@@ -531,7 +531,9 @@ def _sha_lf(path):
 
 def test_everything_placed_before_m3_is_byte_unchanged():
     for rel, want in PLACED.items(): assert _sha_lf(os.path.join(PKG, *rel.split("/"))) == want, rel
-    assert sorted(fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")) == sorted([r.split("/")[1] for r in PLACED] + ["evaluator.py"])
+    # The files this module added are present beside them. The folder is not required to hold nothing else: this line
+    # first required exactly that and failed as soon as a later module was placed (repaired 2026-11-18).
+    assert {r.split("/")[1] for r in PLACED} | set(["evaluator.py"]) <= {fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")}
     h = hashlib.sha256()
     for sub in ("", "e1", "f8", "gates"):
         d = os.path.join(PKG, sub)
diff --git a/flights/mfa_fidelity/instrument/tests/test_f9_m4.py b/flights/mfa_fidelity/instrument/tests/test_f9_m4.py
index 9c0991e..ba83f91 100644
--- a/flights/mfa_fidelity/instrument/tests/test_f9_m4.py
+++ b/flights/mfa_fidelity/instrument/tests/test_f9_m4.py
@@ -251,8 +251,10 @@ EXPECTED_REFUSED = 367     # 17 genuine arms x 23 changes, less the changes that
 
 
 def _genuine_arms():
-    """Every genuine arm shape: each rule, each set of A4 causes, and the level shapes L2 named (follows own with the
-    rival unresolved; own adverse with the rival unresolved), on TB so that the rival can differ."""
+    """Genuine arm shapes: each rule, five of the seven sets of A4 causes (each cause alone, `isolated adverse level`
+    with `finite resolution`, and all three; the two pairs that join `insufficient informative levels` with one other
+    cause are not here and occur in the 6,000-sweep test), and the level shapes L2 named (follows own with the rival
+    unresolved; own adverse with the rival unresolved), on TB so that the rival can differ."""
     n = "N" * 25
     def tb(codes): return O.arm_tier(_tb(codes))
     return {
@@ -556,7 +558,9 @@ def _sha_lf(path):
 
 def test_everything_placed_before_m4_is_byte_unchanged():
     for rel, want in PLACED.items(): assert _sha_lf(os.path.join(PKG, *rel.split("/"))) == want, rel
-    assert sorted(fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")) == sorted([r.split("/")[1] for r in PLACED] + ["outcomes.py"])
+    # The files this module added are present beside them. The folder is not required to hold nothing else: this line
+    # first required exactly that and failed as soon as a later module was placed (repaired 2026-11-18).
+    assert {r.split("/")[1] for r in PLACED} | set(["outcomes.py"]) <= {fn for fn in os.listdir(os.path.join(PKG, "f9")) if fn.endswith(".py")}
     h = hashlib.sha256()
     for sub in ("", "e1", "f8", "gates"):
         d = os.path.join(PKG, sub)
```

## Appendix C — L2 combined-run console transcript

Raw transcript SHA-256: `084988d3f0cc8306272efd7101d1cc06919feb628469dc25daf6e6abe482344d`. This is L2's execution of the repaired packet, with all five files in one process. The path printed by pytest identifies the local review extraction.

```text
============================= test session starts ==============================
platform linux -- Python 3.12.14, pytest-9.2.0, pluggy-1.7.0 -- /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python
rootdir: /workspace/scratch/29c07668431d/f9_test_repair_round1_review/flights/mfa_fidelity/instrument
collecting ... collected 250 items

tests/test_f9_m1.py::test_frozen_identity_and_the_committed_contract PASSED [  0%]
tests/test_f9_m1.py::test_levels_follow_the_rule_of_section_2_9 PASSED   [  0%]
tests/test_f9_m1.py::test_declared_values_are_the_freeze_records PASSED  [  1%]
tests/test_f9_m1.py::test_a_changed_literal_fails_the_preflight PASSED   [  1%]
tests/test_f9_m1.py::test_floor_hazard_is_bound_to_its_rule_l2_m1_round1_r3 PASSED [  2%]
tests/test_f9_m1.py::test_bases_have_the_declared_form_and_ranges[T0] PASSED [  2%]
tests/test_f9_m1.py::test_bases_have_the_declared_form_and_ranges[TA] PASSED [  2%]
tests/test_f9_m1.py::test_bases_have_the_declared_form_and_ranges[TB] PASSED [  3%]
tests/test_f9_m1.py::test_bases_have_the_declared_form_and_ranges[TC] PASSED [  3%]
tests/test_f9_m1.py::test_bases_have_the_declared_form_and_ranges[TD-1-2] PASSED [  4%]
tests/test_f9_m1.py::test_bases_have_the_declared_form_and_ranges[TD-1-4] PASSED [  4%]
tests/test_f9_m1.py::test_bases_have_the_declared_form_and_ranges[TD-4-2] PASSED [  4%]
tests/test_f9_m1.py::test_bases_have_the_declared_form_and_ranges[TD-4-4] PASSED [  5%]
tests/test_f9_m1.py::test_t0_is_flat_and_its_identity_is_exact PASSED    [  5%]
tests/test_f9_m1.py::test_axis_zero_is_x_and_formulas_match_cell_by_cell PASSED [  6%]
tests/test_f9_m1.py::test_tb_criterion_and_roles PASSED                  [  6%]
tests/test_f9_m1.py::test_td_core_and_margin_table[TD-1-2] PASSED        [  6%]
tests/test_f9_m1.py::test_td_core_and_margin_table[TD-1-4] PASSED        [  7%]
tests/test_f9_m1.py::test_td_core_and_margin_table[TD-4-2] PASSED        [  7%]
tests/test_f9_m1.py::test_td_core_and_margin_table[TD-4-4] PASSED        [  8%]
tests/test_f9_m1.py::test_td_cores_are_fixed_sets_independent_of_w PASSED [  8%]
tests/test_f9_m1.py::test_undeclared_objects_are_refused PASSED          [  8%]
tests/test_f9_m1.py::test_serialization_is_little_endian_c_order_and_round_trips PASSED [  9%]
tests/test_f9_m1.py::test_comparison_arrays_follow_section_3_4_step_3 PASSED [  9%]
tests/test_f9_m1.py::test_level_labels_are_the_compositions_own_index PASSED [ 10%]
tests/test_f9_m1.py::test_fixed_cases_of_the_component_convention PASSED [ 10%]
tests/test_f9_m1.py::test_l2_two_loop_case_has_two_components PASSED     [ 10%]
tests/test_f9_m1.py::test_canonical_bond_order_and_midpoints PASSED      [ 11%]
tests/test_f9_m1.py::test_tracer_agrees_with_an_independent_walk_on_random_masks PASSED [ 11%]
tests/test_f9_m1.py::test_a_region_and_its_complement_share_bonds_not_components PASSED [ 12%]
tests/test_f9_m1.py::test_informative_level_thresholds PASSED            [ 12%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TA-P] PASSED [ 12%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TA-H] PASSED [ 13%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TB-P] PASSED [ 13%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TB-H] PASSED [ 14%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TC-P] PASSED [ 14%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TC-H] PASSED [ 14%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TD-1-2-P] PASSED [ 15%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TD-1-2-H] PASSED [ 15%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TD-1-4-P] PASSED [ 16%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TD-1-4-H] PASSED [ 16%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TD-4-2-P] PASSED [ 16%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TD-4-2-H] PASSED [ 17%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TD-4-4-P] PASSED [ 17%]
tests/test_f9_m1.py::test_family_is_every_level_set_of_the_comparison_array[TD-4-4-H] PASSED [ 18%]
tests/test_f9_m1.py::test_constant_index_has_an_empty_family PASSED      [ 18%]
tests/test_f9_m1.py::test_same_family_terrains_share_masks_and_tb_does_not PASSED [ 18%]
tests/test_f9_m1.py::test_family_identities_distinguish_levels_masks_and_components PASSED [ 19%]
tests/test_f9_m1.py::test_component_identity_binds_membership_l2_m1_round1_r1 PASSED [ 19%]
tests/test_f9_m1.py::test_family_level_bytes_are_little_endian_l2_m1_round1_r1 PASSED [ 20%]
tests/test_f9_m1.py::test_family_refuses_malformed_arrays PASSED         [ 20%]
tests/test_f9_m1.py::test_spectral_values_agree_with_appendix_a[T0] PASSED [ 20%]
tests/test_f9_m1.py::test_spectral_values_agree_with_appendix_a[TA] PASSED [ 21%]
tests/test_f9_m1.py::test_spectral_values_agree_with_appendix_a[TB] PASSED [ 21%]
tests/test_f9_m1.py::test_spectral_values_agree_with_appendix_a[TC] PASSED [ 22%]
tests/test_f9_m1.py::test_spectral_values_agree_with_appendix_a[TD-1-2] PASSED [ 22%]
tests/test_f9_m1.py::test_spectral_values_agree_with_appendix_a[TD-1-4] PASSED [ 22%]
tests/test_f9_m1.py::test_spectral_values_agree_with_appendix_a[TD-4-2] PASSED [ 23%]
tests/test_f9_m1.py::test_spectral_values_agree_with_appendix_a[TD-4-4] PASSED [ 23%]
tests/test_f9_m1.py::test_power_iteration_agrees_with_a_dense_eigenvalue_computation PASSED [ 24%]
tests/test_f9_m1.py::test_routine_agrees_with_lanczos_on_every_arm PASSED [ 24%]
tests/test_f9_m1.py::test_flat_terrain_reduces_to_flight_8s_control PASSED [ 24%]
tests/test_f9_m1.py::test_every_declared_arm_is_in_the_routines_domain PASSED [ 25%]
tests/test_f9_m1.py::test_zero_index_has_no_level PASSED                 [ 25%]
tests/test_f9_m1.py::test_record_covers_every_declared_object PASSED     [ 26%]
tests/test_f9_m1.py::test_bundle_round_trips_and_the_record_follows_from_the_stored_arrays PASSED [ 26%]
tests/test_f9_m1.py::test_a_second_build_gives_the_same_record PASSED    [ 26%]
tests/test_f9_m1.py::test_byte_and_form_tampering_is_refused_by_the_loader PASSED [ 27%]
tests/test_f9_m1.py::test_inconsistent_records_are_refused_l2_m1_round1_r2[empty_coverage] PASSED [ 27%]
tests/test_f9_m1.py::test_inconsistent_records_are_refused_l2_m1_round1_r2[wrong_arm_binding] PASSED [ 28%]
tests/test_f9_m1.py::test_inconsistent_records_are_refused_l2_m1_round1_r2[wrong_comparison] PASSED [ 28%]
tests/test_f9_m1.py::test_inconsistent_records_are_refused_l2_m1_round1_r2[wrong_gain] PASSED [ 28%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[an_extra_arm] PASSED [ 29%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[an_extra_top_level_field] PASSED [ 29%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[arm_composition_field_wrong] PASSED [ 30%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[arm_terrain_field_wrong] PASSED [ 30%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[component_identity_wrong] PASSED [ 30%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[core_cells_wrong] PASSED [ 31%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[environment_not_strings] PASSED [ 31%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[family_count_wrong] PASSED [ 32%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[int_where_a_float_belongs] PASSED [ 32%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[levels_wrong] PASSED [ 32%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[one_arm_missing] PASSED [ 33%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[one_family_missing] PASSED [ 33%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[q_wrong] PASSED [ 34%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[same_family_assertion_false] PASSED [ 34%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[same_family_entry_missing] PASSED [ 34%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[spr_off_by_1e-6] PASSED [ 35%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[t0_given_a_family] PASSED [ 35%]
tests/test_f9_m1.py::test_the_record_must_equal_what_the_stored_arrays_give[tb_listed_as_same_family] PASSED [ 36%]
tests/test_f9_m1.py::test_float_tolerance_is_for_another_machine_only PASSED [ 36%]
tests/test_f9_m1.py::test_spectral_tolerance_is_pure_relative_l2_m1_round2[l2_coherent_pair_1.0003e-9] PASSED [ 36%]
tests/test_f9_m1.py::test_spectral_tolerance_is_pure_relative_l2_m1_round2[l2_spectral_only_1.004e-9] PASSED [ 37%]
tests/test_f9_m1.py::test_spectral_tolerance_is_pure_relative_l2_m1_round2[within_bound_coherent] PASSED [ 37%]
tests/test_f9_m1.py::test_gain_must_follow_from_the_records_own_q_and_spr PASSED [ 38%]
tests/test_f9_m1.py::test_a_last_place_difference_in_q_is_another_machines_libm PASSED [ 38%]
tests/test_f9_m1.py::test_each_float_takes_the_rule_of_its_own_quantity PASSED [ 38%]
tests/test_f9_m1.py::test_stored_bases_must_be_the_declared_terrains PASSED [ 39%]
tests/test_f9_m1.py::test_record_from_bases_refuses_bases_that_break_a_declared_relation PASSED [ 39%]
tests/test_f9_m1.py::test_array_paths_are_declared_literals PASSED       [ 40%]
tests/test_f9_m1.py::test_container_values_are_reported 
F9 M1 registered family sizes (here vs contract, provisional): {"TA.shared": {"contract": [1300, 2221], "equal": true, "here": [1300, 2221]}, "TB.H": {"contract": [50, 59], "equal": true, "here": [50, 59]}, "TB.P": {"contract": [2600, 3840], "equal": true, "here": [2600, 3840]}, "TC.shared": {"contract": [1180, 1389], "equal": true, "here": [1180, 1389]}, "TD-1-2.shared": {"contract": [681, 861], "equal": true, "here": [681, 861]}, "TD-1-4.shared": {"contract": [920, 920], "equal": true, "here": [920, 920]}, "TD-4-2.shared": {"contract": [250, 250], "equal": true, "here": [250, 250]}, "TD-4-4.shared": {"contract": [250, 250], "equal": true, "here": [250, 250]}}
PASSED           [ 40%]
tests/test_f9_m1.py::test_e1_and_f8_are_byte_unchanged PASSED            [ 40%]
tests/test_f9_m2.py::test_stream_declaration_verifies_and_covers_the_frozen_configuration PASSED [ 41%]
tests/test_f9_m2.py::test_a_changed_stream_literal_fails_the_preflight PASSED [ 41%]
tests/test_f9_m2.py::test_the_key_is_the_contracts_tuple_in_order PASSED [ 42%]
tests/test_f9_m2.py::test_every_declared_run_has_its_own_key PASSED      [ 42%]
tests/test_f9_m2.py::test_undeclared_runs_and_masters_are_refused PASSED [ 42%]
tests/test_f9_m2.py::test_every_earlier_master_is_refused_l2_m2_round1_r2 PASSED [ 43%]
tests/test_f9_m2.py::test_the_stream_is_pcg64_of_the_seed_sequence_of_the_key PASSED [ 43%]
tests/test_f9_m2.py::test_step_is_the_written_rule_cell_by_cell[0.0] PASSED [ 44%]
tests/test_f9_m2.py::test_step_is_the_written_rule_cell_by_cell[0.01005033585350145] PASSED [ 44%]
tests/test_f9_m2.py::test_the_step_reads_the_state_at_t_only PASSED      [ 44%]
tests/test_f9_m2.py::test_floor_is_not_gated_and_zero_floor_is_absorbing PASSED [ 45%]
tests/test_f9_m2.py::test_reduction_to_the_placed_flight8_step PASSED    [ 45%]
tests/test_f9_m2.py::test_reduction_check_can_fail PASSED                [ 46%]
tests/test_f9_m2.py::test_arm_context_takes_the_stored_index_and_the_records_gain PASSED [ 46%]
tests/test_f9_m2.py::test_a_runs_record_is_the_rule_re_simulated[T0.P-realization-stationary_floor-1500000] PASSED [ 46%]
tests/test_f9_m2.py::test_a_runs_record_is_the_rule_re_simulated[T0.P-skeleton-all_active-750000] PASSED [ 47%]
tests/test_f9_m2.py::test_a_runs_record_is_the_rule_re_simulated[T0.P-skeleton-low-2000000] PASSED [ 47%]
tests/test_f9_m2.py::test_a_runs_record_is_the_rule_re_simulated[TB.H-skeleton-all_active-1000000] PASSED [ 48%]
tests/test_f9_m2.py::test_a_runs_record_is_the_rule_re_simulated[TC.P-realization-stationary_floor-1000000] PASSED [ 48%]
tests/test_f9_m2.py::test_the_test_runs_cover_extinction_and_survival PASSED [ 48%]
tests/test_f9_m2.py::test_window_record_on_fixed_sequences PASSED        [ 49%]
tests/test_f9_m2.py::test_runs_are_repeatable_and_separate PASSED        [ 49%]
tests/test_f9_m2.py::test_starts PASSED                                  [ 50%]
tests/test_f9_m2.py::test_record_round_trips_and_replays[T0.P-realization-stationary_floor-1500000] PASSED [ 50%]
tests/test_f9_m2.py::test_record_round_trips_and_replays[T0.P-skeleton-all_active-750000] PASSED [ 50%]
tests/test_f9_m2.py::test_record_round_trips_and_replays[T0.P-skeleton-low-2000000] PASSED [ 51%]
tests/test_f9_m2.py::test_record_round_trips_and_replays[TB.H-skeleton-all_active-1000000] PASSED [ 51%]
tests/test_f9_m2.py::test_record_round_trips_and_replays[TC.P-realization-stationary_floor-1000000] PASSED [ 52%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[advanced] PASSED   [ 52%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[array_missing] PASSED [ 52%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[bool_for_int] PASSED [ 53%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[contract] PASSED   [ 53%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[declaration] PASSED [ 54%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[draws] PASSED      [ 54%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[extinction] PASSED [ 54%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[extra_field] PASSED [ 55%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[floor] PASSED      [ 55%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[gain] PASSED       [ 56%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[identity_not_hex] PASSED [ 56%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[int_for_float] PASSED [ 56%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[level_id] PASSED   [ 57%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[master_class] PASSED [ 57%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[missing_field] PASSED [ 58%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[mu] PASSED         [ 58%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[retired_master] PASSED [ 58%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[schema] PASSED     [ 59%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[seed] PASSED       [ 59%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[stream_declaration] PASSED [ 60%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[stream_key] PASSED [ 60%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[survival] PASSED   [ 60%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[tail_sum] PASSED   [ 61%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[terrain] PASSED    [ 61%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[ticks] PASSED      [ 62%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[type] PASSED       [ 62%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[undeclared_level] PASSED [ 62%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[version] PASSED    [ 63%]
tests/test_f9_m2.py::test_a_changed_header_is_refused[windows] PASSED    [ 63%]
tests/test_f9_m2.py::test_changed_bytes_are_refused_with_and_without_restated_hashes PASSED [ 64%]
tests/test_f9_m2.py::test_impossible_summaries_are_refused_by_the_parser_l2_m2_round1_r1 PASSED [ 64%]
tests/test_f9_m2.py::test_undeclared_json_types_are_refused_l2_m2_round1_r1c PASSED [ 64%]
tests/test_f9_m2.py::test_consistency_relations_hold_on_arbitrary_tails PASSED [ 65%]
tests/test_f9_m2.py::test_a_consistent_forgery_is_refused_by_replay_only PASSED [ 65%]
tests/test_f9_m2.py::test_m1_e1_and_f8_are_byte_unchanged PASSED         [ 66%]
tests/test_f9_m3.py::test_declaration_verifies_and_a_changed_literal_fails PASSED [ 66%]
tests/test_f9_m3.py::test_region_is_the_contracts_criterion_in_exact_rationals PASSED [ 66%]
tests/test_f9_m3.py::test_ties_at_theta_are_included_exactly PASSED      [ 67%]
tests/test_f9_m3.py::test_inputs_are_checked PASSED                      [ 67%]
tests/test_f9_m3.py::test_weights_are_bounded_before_they_are_summed_l2_m3_round1_d1 PASSED [ 68%]
tests/test_f9_m3.py::test_the_float_decision_at_epsilon_is_the_exact_decision_for_every_possible_term PASSED [ 68%]
tests/test_f9_m3.py::test_step4_reasons PASSED                           [ 68%]
tests/test_f9_m3.py::test_distance_grid_is_exact PASSED                  [ 69%]
tests/test_f9_m3.py::test_quantile_rule PASSED                           [ 69%]
tests/test_f9_m3.py::test_joint_discrepancy_on_hand_cases PASSED         [ 70%]
tests/test_f9_m3.py::test_joint_discrepancy_against_pairwise_reference PASSED [ 70%]
tests/test_f9_m3.py::test_families_from_the_bundle PASSED                [ 70%]
tests/test_f9_m3.py::test_pruning_intervals_are_the_cells_within_reach PASSED [ 71%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TB.H-exact] PASSED [ 71%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TB.H-grown1] PASSED [ 72%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TB.H-grown2] PASSED [ 72%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TB.H-grown3] PASSED [ 72%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TB.H-noisy] PASSED [ 73%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TB.H-square] PASSED [ 73%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TD-4-2.P-exact] PASSED [ 74%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TD-4-2.P-grown2] PASSED [ 74%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TD-4-2.P-shrunk3] PASSED [ 74%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TD-4-2.P-noisy] PASSED [ 75%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TD-4-2.P-square] PASSED [ 75%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree[TA.P-noisy] PASSED [ 76%]
tests/test_f9_m3.py::test_the_contour_cache_changes_no_result PASSED     [ 76%]
tests/test_f9_m3.py::test_the_family_minimum_against_an_independent_search PASSED [ 76%]
tests/test_f9_m3.py::test_the_lowest_level_keeps_a_tie PASSED            [ 77%]
tests/test_f9_m3.py::test_epsilon_is_inclusive_and_not_enlarged PASSED   [ 77%]
tests/test_f9_m3.py::test_the_resampling_stream_is_the_declared_one PASSED [ 78%]
tests/test_f9_m3.py::test_result_table_at_its_boundaries PASSED          [ 78%]
tests/test_f9_m3.py::test_a_level_on_its_own_contour_is_compatible_for_both_indices PASSED [ 78%]
tests/test_f9_m3.py::test_a_region_off_the_family_is_adverse_and_tb_separates_its_indices PASSED [ 79%]
tests/test_f9_m3.py::test_pruned_and_exhaustive_search_agree_on_every_resample PASSED [ 79%]
tests/test_f9_m3.py::test_unavailable_states PASSED                      [ 80%]
tests/test_f9_m3.py::test_invalid_draws_at_the_boundary_of_fifty PASSED  [ 80%]
tests/test_f9_m3.py::test_everything_placed_before_m3_is_byte_unchanged PASSED [ 80%]
tests/test_f9_m4.py::test_declaration_verifies_and_the_labels_are_the_contracts PASSED [ 81%]
tests/test_f9_m4.py::test_level_table_is_the_contracts_rows PASSED       [ 81%]
tests/test_f9_m4.py::test_level_causes_and_kinds PASSED                  [ 82%]
tests/test_f9_m4.py::test_same_family_levels_are_not_adjudicable_and_must_agree PASSED [ 82%]
tests/test_f9_m4.py::test_level_inputs_are_checked PASSED                [ 82%]
tests/test_f9_m4.py::test_level_from_the_evaluators_record PASSED        [ 83%]
tests/test_f9_m4.py::test_arm_rule_on_the_contracts_named_sweeps PASSED  [ 83%]
tests/test_f9_m4.py::test_arm_rule_against_the_reference_on_many_sweeps PASSED [ 84%]
tests/test_f9_m4.py::test_a_missing_level_record_is_an_apparatus_cause PASSED [ 84%]
tests/test_f9_m4.py::test_a_level_record_that_contradicts_itself_is_refused PASSED [ 84%]
tests/test_f9_m4.py::test_genuine_arm_records_are_accepted PASSED        [ 85%]
tests/test_f9_m4.py::test_an_arm_record_that_contradicts_itself_is_refused_l2_m4_round1_d1 PASSED [ 85%]
tests/test_f9_m4.py::test_flight_b_over_every_combination_of_seven_arms PASSED [ 86%]
tests/test_f9_m4.py::test_flight_b_records_and_missing_inputs PASSED     [ 86%]
tests/test_f9_m4.py::test_flight_d PASSED                                [ 86%]
tests/test_f9_m4.py::test_flight_d_against_a_reference_on_random_sweeps PASSED [ 87%]
tests/test_f9_m4.py::test_clopper_pearson PASSED                         [ 87%]
tests/test_f9_m4.py::test_persistence_profiles_on_named_sweeps PASSED    [ 88%]
tests/test_f9_m4.py::test_persistence_against_the_reference_on_many_sweeps PASSED [ 88%]
tests/test_f9_m4.py::test_persistence_inputs_and_missing_levels PASSED   [ 88%]
tests/test_f9_m4.py::test_everything_placed_before_m4_is_byte_unchanged PASSED [ 89%]
tests/test_f9_m5.py::test_closure_declaration_and_registered_solver_values PASSED [ 89%]
tests/test_f9_m5.py::test_the_map_is_the_contracts_formula PASSED        [ 90%]
tests/test_f9_m5.py::test_flat_index_fixed_points_against_the_scalar_equation PASSED [ 90%]
tests/test_f9_m5.py::test_skeleton_below_the_crossing_converges_to_a_small_positive_map_not_zero PASSED [ 90%]
tests/test_f9_m5.py::test_nonconvergence_is_comparator_unavailable_with_no_map PASSED [ 91%]
tests/test_f9_m5.py::test_the_crossing_is_where_the_zero_floor_map_loses_stability_at_zero PASSED [ 91%]
tests/test_f9_m5.py::test_closure_inputs_are_checked PASSED              [ 92%]
tests/test_f9_m5.py::test_site_closure_records_on_contract_arms PASSED   [ 92%]
tests/test_f9_m5.py::test_skeleton_closure_at_the_crossing_is_unavailable_on_t0 PASSED [ 92%]
tests/test_f9_m5.py::test_threshold_fidelity_cases PASSED                [ 93%]
tests/test_f9_m5.py::test_t0_declaration_and_registered_values PASSED    [ 93%]
tests/test_f9_m5.py::test_the_bracket_is_appendix_a4s_arithmetic PASSED  [ 94%]
tests/test_f9_m5.py::test_bracket_eligibility_is_the_fine_grid_rule PASSED [ 94%]
tests/test_f9_m5.py::test_eligibility_governs_t_s2_l2_m5_round1_d1 PASSED [ 94%]
tests/test_f9_m5.py::test_l2s_exact_boundary_witnesses PASSED            [ 95%]
tests/test_f9_m5.py::test_a_continuous_crossing_inside_the_fine_grid_is_produced PASSED [ 95%]
tests/test_f9_m5.py::test_boundary_absent_or_non_monotone PASSED         [ 96%]
tests/test_f9_m5.py::test_hysteresis_and_the_bracket PASSED              [ 96%]
tests/test_f9_m5.py::test_the_continuity_criterion_is_a_slope_on_the_non_uniform_grid PASSED [ 96%]
tests/test_f9_m5.py::test_a_reversal_within_the_band_is_disregarded_and_one_beyond_it_is_nd PASSED [ 97%]
tests/test_f9_m5.py::test_realization_extinct_and_apparatus PASSED       [ 97%]
tests/test_f9_m5.py::test_t0_inputs_are_checked PASSED                   [ 98%]
tests/test_f9_m5.py::test_exact_statistics_against_the_library PASSED    [ 98%]
tests/test_f9_m5.py::test_reference_object_alone PASSED                  [ 98%]
tests/test_f9_m5.py::test_the_four_tests_against_the_second_implementation_on_random_sweeps PASSED [ 99%]
tests/test_f9_m5.py::test_the_record_is_plain_data_and_states_its_scope PASSED [ 99%]
tests/test_f9_m5.py::test_everything_placed_before_m5_is_byte_unchanged PASSED [100%]

======================= 250 passed in 669.56s (0:11:09) ========================
```

FINAL VERDICT: SOUND
