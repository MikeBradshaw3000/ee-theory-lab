| Receipt check | Recomputed / observed value | Result |
|---|---|---|
| Uploaded archive | `f9_m5_build_round2_L2(1).zip` | Supplied as Flight 9 M5 round 2 |
| Archive SHA-256 | `7dcce4b0aadf9ccaf24ab9c3979ba955e215531946ceb7b84c774647ab82e0f1` | MATCH to supplied value |
| Payload file count | 77 | MATCH |
| Total file count | 78: 77 payload files plus `MANIFEST.txt` | MATCH |
| Manifest entries and matched payload digests | 77 / 77 | MATCH |
| Missing or unlisted payload files | None | PASS |
| Duplicate ZIP names or manifest paths | None | PASS |
| ZIP integrity | No CRC errors | PASS |
| `MANIFEST.txt` SHA-256 | `97a1aa3f287275b8bfc5c025b2fff42a35d7ac44c11f270ff6d4faf659942fa2` | Computed; manifest does not list itself |
| Receipt gate | Receipt returned first; review executed after Mike's “execute” | SATISFIED |

| # | File, in manifest order | Recomputed full SHA-256 | Against `MANIFEST.txt` |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M5_ROUND2_RESPONSE_2026-11-18.md` | `8a552acb0d8d759f0fe0f35a4e41da69d12b5aca0474d5456863a5d1aab0ff21` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py` | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/t0.py` | `a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472` | MATCH |
| 4 | `flights/mfa_fidelity/instrument/tests/test_f9_m5.py` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` | MATCH |
| 5 | `flights/mfa_fidelity/build_records/L2_F9_M5_ROUND1_REVIEW_2026-11-18_RECEIVED.md` | `1700fe17f2280da6015963057f18657359a31c08bde9ca033e91ffe1b3b07b54` | MATCH |
| 6 | `flights/mfa_fidelity/build_records/f9_m5_module_container_round2_2026-11-18.txt` | `c45d973c62bdd0ff67e7590a1a621ede86712e53c90289149c12e067abe964bd` | MATCH |
| 7 | `flights/mfa_fidelity/build_records/l2_m5_round1_reproduce.py` | `de936fa3643979c05c74e35611fe2113b5b17090b2e35ea4a931c18cdd4ad0a6` | MATCH |
| 8 | `flights/mfa_fidelity/build_records/f9_m5_l2_round1_reproduce_on_round1_2026-11-18.txt` | `f4659f79b8afe00011f6dbd58cbef3e1382c6c5a2f0ce5bbf15ef572c481af81` | MATCH |
| 9 | `flights/mfa_fidelity/build_records/f9_m5_l2_round1_reproduce_on_round2_2026-11-18.txt` | `fe8596745f7bb616b8c407a46554f04f98d47cc00f4a9b9e85475cb6e5627eb4` | MATCH |
| 10 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M5_BUILD_PACKET_2026-11-18.md` | `94d7b60cce9918185e0544cd10ff7d84bdcd24feed75c43b624d1809397a88ca` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/f9_m5_module_container_2026-11-18.txt` | `3e571590bb1b39b1fa0f3801bd7d552b0a690d5b4f43112e2b03fa55146aee63` | MATCH |
| 12 | `packet_only/round1/closure.py` | `df9bfb22b3e0f2c76f1ffd94ff6f789d116758b2bf025adb102b7e7bbd318aee` | MATCH |
| 13 | `packet_only/round1/t0.py` | `afb16e81575c9ea39357d141c04c7feff40b9590935a127a9064bdb0e9eb688f` | MATCH |
| 14 | `packet_only/round1/test_f9_m5.py` | `55b22704bb4e22160566ffc256e6e03c3915458822d9070f6a452b0d15f6a4dd` | MATCH |
| 15 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 16 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 17 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 18 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 19 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | MATCH |
| 20 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 21 | `flights/mfa_fidelity/build_records/F9_M4_PLACEMENT_NOTE_2026-11-18.md` | `b6004b9281aedc276b37244550baf9775853d5e678f7a1581b79fff754284839` | MATCH |
| 22 | `flights/mfa_fidelity/build_records/L2_F9_M4_ROUND2_REVIEW_2026-11-18_RECEIVED.md` | `d3391e61f22796899f5b148fcc1244c53660c8b81591b2dbee20bc9a61c2f5da` | MATCH |
| 23 | `flights/mfa_fidelity/build_records/f9_m4_module_canonical_2026-11-18.txt` | `eacdbcedbf269fc841676b201343a7cd38d8eafc9b8f04f6fbce5e630be0cb9b` | MATCH |
| 24 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 25 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` | MATCH |
| 26 | `flights/mfa_fidelity/instrument/tests/test_f9_m3.py` | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` | MATCH |
| 27 | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` | MATCH |
| 28 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 29 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 30 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 31 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 32 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 33 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 72 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 73 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 74 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 75 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 76 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |
| 77 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |

# L2 — Flight 9 M5 build review, round 2

**Date:** 2026-11-18. **Role:** L2, instrument build reviewer. **Decision authority:** Mike.

**Reviewed archive:** `f9_m5_build_round2_L2.zip`, received as `f9_m5_build_round2_L2(1).zip`. Its recomputed SHA-256 is **`7dcce4b0aadf9ccaf24ab9c3979ba955e215531946ceb7b84c774647ab82e0f1`**.

**D1 is CLOSED.** The revised T-S2 follows the recorded ruling and the required eligibility precedence. The original counterexample now gives the required result; the complete M5 suite passes **27/27**; independent checks found no new blocking defect. M5-9 and M5-10 are acceptable as revised. The earlier accepted declarations retain their dispositions. This conclusion is about the submitted M5 build; the three separately disclosed earlier-module preservation tests remain failing. [P2 §§1–5; R1 §§2–4, 6; verification in §6 below.]

The receipt was returned before review, and review began after Mike's “execute.” The final report repeats the receipt above so that the review and the reviewed bytes travel together.

## 1. Sources, scope, and continuity

Source references below use these keys. Paths in this table are relative to `flights/mfa_fidelity/` unless explicitly marked otherwise; line references refer to the bytes in this archive.

| Key | Source |
|---|---|
| P2 | `build_records/L1_TO_L2_F9_M5_ROUND2_RESPONSE_2026-11-18.md` |
| P1 | `build_records/L1_TO_L2_F9_M5_BUILD_PACKET_2026-11-18.md` |
| R1 | `build_records/L2_F9_M5_ROUND1_REVIEW_2026-11-18_RECEIVED.md` |
| C9 | `contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` |
| FR | `contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` |
| T0 | `instrument/mfa_instrument/f9/t0.py` |
| CL | `instrument/mfa_instrument/f9/closure.py` |
| CFG | `instrument/mfa_instrument/f9/config.py` |
| T5 | `instrument/tests/test_f9_m5.py` |
| T2, T3, T4 | `instrument/tests/test_f9_m2.py`, `instrument/tests/test_f9_m3.py`, and `instrument/tests/test_f9_m4.py` |
| OLD | The three round-1 byte copies under archive-root `packet_only/round1/` |

P2 identifies repository pin `6823c41a9b36ec4e7bcc54c560920e4d5bbf029a` and records Mike's adoption of the reading recommended in R1. I reviewed that supplied ruling record and its implementation. The archive verification and comparisons below establish packet identity and continuity; they do not independently establish the current state of the remote repository. [P2, lines 4, 14–28.]

All **67 round-1 payload paths** recorded in R1's receipt are retained in this packet. **64 have unchanged full hashes; exactly three differ:** CL, T0, and T5. The other **10 payloads are additions**. Each OLD source copy matches its corresponding round-1 identity. Thus the packet supports a precise comparison with the previously reviewed sources. [R1 receipt; current `MANIFEST.txt`; P2 §4.]

| Reviewed object | Recomputed SHA-256 |
|---|---|
| CL, round 2 | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` |
| T0, round 2 | `a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472` |
| T5, round 2 | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` |
| Closure declaration, both rounds | `d4196f0ecee6a55204ec8f42f7a9465c453498e4b2f85a80fe64ed963d6fcf9e` |
| T0 declaration, round 1 | `8698e73fbd544a3299ef74b4fe744540ee7c04a10b152e948e6a4b1531c2a093` |
| T0 declaration, round 2 | `0b5417a9050ee12ebf133f310a75e2c52cc32d269a0a246674cef469195a5a38` |

The declaration hashes were recomputed directly from `repr(declaration).encode("utf-8")`, the canonicalization in CFG, and checked through the declaration-verification functions. The only changed T0 declaration entry is `hysteresis`. Source identity and declaration identity remain distinct. [CFG, lines 143–144; T0, lines 123–157; Appendix B below.]

The AST comparison confirms the disclosed scope:

| File | Actual changes |
|---|---|
| CL | Only the `threshold_fidelity` docstring. The entire module's AST is identical after removing docstrings. |
| T0 | Module docstring; `T0_DECLARATION`'s `hysteresis` entry; its digest literal; the T-S2 branch in `evaluate_t0`. No functions were added or removed. |
| T5 | Three existing definitions changed: `test_boundary_absent_or_non_monotone`, `_reference_t0`, and `test_the_four_tests_against_the_second_implementation_on_random_sweeps`. The two disclosed tests were added; none were removed. Test count: 25 → 27. |

In particular, `_boundary`, `_eligible`, validation, exact statistics, continuity arithmetic, reference construction, and final aggregation are unchanged. The executable production repair is confined to T0's lines 316–325. [OLD versus CL/T0/T5; P2 §4.]

## 2. Q1 — D1 closure

**Answer: yes. D1 is closed on these bytes.**

C9 §5.8 requires two eligible skeleton boundaries before applying the hysteresis bracket. FR item 3 ratifies that condition. R1's repair table distinguished a missing observation from a complete sweep that supplies no eligible boundary. P2 records the withdrawal of the competing round-1 reading and Mike's adoption of that repair. The revised code implements the same order. [C9 §5.8; FR §3, item 3; R1 §2.3; P2 §1.]

| Condition, in order | Revised T-S2 result | Implementation |
|---|---|---|
| T-S1′ does not locate a high boundary | Dependency ND, retaining the high test's cause | T0, lines 308–312 |
| A required low observation is missing | ND `apparatus unevaluable (missing level record)` | T0, lines 316–318 |
| Complete sweeps do not supply two eligible boundaries | ND `bracket outside fine grid` | T0, lines 320–323 |
| Both eligible; absolute separation ≤ 75,400 micro-units | PASS | T0, line 324 |
| Both eligible; absolute separation > 75,400 micro-units | FAIL `hysteresis` | T0, line 325 |

This is more than an expected-output adjustment. The old branch copied the low sweep's phase result whenever `lo_c` was absent. The new branch first separates missing low records, then constructs eligibility even when the complete low sweep supplies no boundary. A complete low phase result can no longer bypass the eligibility rule. The only T-S2 FAIL branch is now `hysteresis`. [OLD/`t0.py`, lines 307–317; T0, lines 313–325.]

### Original counterexample

The supplied `build_records/l2_m5_round1_reproduce.py` is **byte-identical** to R1 Appendix A's Python code block: **763 bytes**, SHA-256 `de936fa3643979c05c74e35611fe2113b5b17090b2e35ea4a931c18cdd4ad0a6`. It does not differ from the program L2 originally supplied.

I executed it against the round-2 module. Its output is byte-identical to the supplied round-2 reproduction evidence:

~~~text
high boundary: 1000000
high eligible: False
T-S1′ PASS None
T-S1c PASS None
T-S2 ND bracket outside fine grid
T-R1′ PASS None
T0: NOT DISTINGUISHED bracket outside fine grid
~~~

The high boundary remains 1.00, with preceding level 0.75, and is correctly ineligible. The low sweep remains complete with no active criterion phase. Its result is now the required grid ND; the other three tests remain PASS. [R1 §§2.2–2.3 and Appendix A; P2 §1; T5, lines 321–334.]

### Independent coverage of the decision table

An independent checker derived the expected T-S2 result from the registered grid, the 36-of-40 criterion, and the ruled table. It did not use the production `_boundary`, `_eligible`, or L1's second implementation. All **2,162 checks passed**:

| Group | Checks |
|---|---:|
| All 24 possible high crossing levels × all 24 low crossing levels | 576 |
| All 24 high crossings × four complete low profiles without a boundary | 96 |
| All 24 high crossings × all 25 missing-low positions × omitted/explicit-None forms | 1,200 |
| Four high profiles without a boundary × 30 low configurations | 120 |
| All 25 missing-high positions × six low configurations | 150 |
| Ten malformed low-observation constructions under eligible and ineligible high boundaries | 20 |
| **Total** | **2,162** |

The four no-boundary profiles were none-met, all-met, non-monotone with a terminal surviving suffix, and non-monotone without one. The checker also verified retained survivor counts in each complete persistence record and apparatus classification in missing-record persistence. Appendix A contains the exact executed checker.

Eligible crossing levels are precisely **1.05 through 2.00** on the registered grid. A boundary at 1.00 lacks a fine-grid predecessor; a boundary at 2.25 or above is outside the fine grid. The all-met low profile can have a descriptive §5.4 reference at 0.75 while supplying no two-phase boundary for T-S1′ or T-S2. That distinction is the previously accepted orchestration, and the repair preserves it. [T0, lines 240–263; C9 §§5.4, 5.8; R1 §4.]

## 3. Q2 — Apparatus versus grid ineligibility

**Answer: no incorrect reclassification was found.**

Once the high-boundary prerequisite is met, both an omitted low key and an explicit `None` yield the missing-record apparatus result before either boundary's eligibility is considered. This remains true when the high boundary is itself ineligible. Conversely, a complete low sweep with none-met, all-met, or non-monotone criterion counts is an observed profile, not a missing observation, and now receives the required grid result. [T0, lines 170–190, 316–325; T5, lines 335–357, 560–561; Appendix A.]

Malformed observations remain refused before classification. The independent checks exercised invalid survival types and lengths, negative, non-integer and excessive tail sums, missing or extra fields, and impossible survival/tail-total combinations. All twenty contexts raised `F9T0Error`. They were not converted to either apparatus ND or grid ND. [T0, lines 164–190, 305–306; Appendix A.]

When the high boundary is unavailable, T-S2 retains the dependency result even if the low sweep is also incomplete. That is the stated first branch, not a failure to apply missing-low precedence. The high test's cause remains visible in the dependency cause, and both persistence records remain present. [P2 §1; T0, lines 308–312, 345–347.]

Missing calibration is a separate issue. T-S2 compares survival boundaries and uses no low-sweep median or variance. Required missing calibration levels still produce apparatus ND in the continuity tests when a reversal needs them. M5's numerical interface still does not certify completion or authorization of the calibration job; that remains the runner's dependency check. The repair neither expands nor weakens that accepted boundary. [T0, lines 266–290, 315, 333; R1 §§4, 7; P2 §5.]

## 4. Q3 — What changes between the rounds

**Answer: scientific outcome/cause changes are confined to a located high boundary combined with a complete low sweep without a T-S1′ boundary. Full record bytes also change in the documented ways below.**

The source comparison supplies an exhaustive partition of accepted inputs:

1. Without a located high boundary, the unchanged prerequisite branch decides T-S2.
2. With a located high boundary and a missing low record, both rounds return the same apparatus outcome and cause.
3. With two located boundaries, the eligibility and integer-separation predicates give the same outcome and cause.
4. With a located high boundary and a complete low sweep lacking a boundary, round 2 replaces the old low-phase result with ND `bracket outside fine grid`.

The other three test records are generated by unchanged code. The final aggregation still gives the first FAIL priority over every ND, and otherwise chooses the first ND in test order. Accordingly, every change in final determination or final cause derives from the repaired T-S2 branch. [OLD/`t0.py` versus T0, lines 308–340.]

### A changed T-S2 result need not change the final word

Six paired full-record witnesses and twelve paired aggregation witnesses confirmed this distinction. Appendix B contains the executed program.

| Low profile and other tests | Round 1 final result | Round 2 final result |
|---|---|---|
| None-met or all-met; other three tests PASS | NOT PRODUCED, low-phase cause | NOT DISTINGUISHED, `bracket outside fine grid` |
| None-met or all-met; realization FAIL | NOT PRODUCED, low-phase cause | NOT PRODUCED remains; cause becomes the realization failure |
| None-met or all-met; T-S1c apparatus ND; realization PASS | NOT PRODUCED, low-phase cause | NOT DISTINGUISHED, earlier T-S1c apparatus cause |
| Non-monotone low; other tests PASS | NOT DISTINGUISHED, `non-monotone survival` | NOT DISTINGUISHED, `bracket outside fine grid` |
| Non-monotone low; an earlier ND or realization FAIL already governs | Earlier ND or realization FAIL determines the final result | Final word and cause can remain identical, despite the changed T-S2 cause |

P2's statement about a no-active low sweep becoming NOT DISTINGUISHED is correct for the counterexample and otherwise passing fixtures. It should not be read as overriding a realization FAIL or the earlier-cause rule. The implementation correctly preserves both. [P2, line 28; T0, lines 335–340; Appendix B.]

### Changes to record details outside that scientific domain

| Situation | Record difference |
|---|---|
| Every T0 evaluation | `declaration_sha256` identifies the revised declaration |
| Two located boundaries, whether the result is PASS, hysteresis FAIL, or grid ND | T-S2 detail adds `low_profile` |
| Missing low record after a located high boundary | Detail `source` changes from `"skeleton-low boundary"` to `"skeleton-low"` |
| No high boundary | No other full-record difference in the paired witness |
| Complete low sweep without a boundary | The copied phase-result detail is replaced with boundary, bracket, eligibility, and low-profile detail; absent low boundary and separation are `None` |

The old duplicate `survivors` array within the low-phase T-S2 detail is no longer copied there. Its counts remain in the unchanged low persistence record. No phase information is lost from the complete T0 record. These detail changes are acceptable, but “unchanged outcomes” must not be represented as byte-identical records. [T0, lines 318–325, 344–352; Appendix B.]

## 5. Q4 — Other findings in the changed definitions

### Declarations and the Q9 docstring

**M5-9: ACCEPTABLE as revised.** The four-test ordering, high prerequisite, missing-record handling, and final aggregation now coexist with the required F9 eligibility rule.

**M5-10: ACCEPTABLE as revised.** Reading 5 is withdrawn and replaced by the recorded ruling. Readings 1, 2, 3, 4, 6, and 7 retain their round-1 acceptance. P2 correctly carries forward the requirement to name the endpoint-difference formula in the governance record and explain the all-levels-met reference/prerequisite distinction. M5-1 through M5-8 and M5-11 retain their accepted dispositions and stated interface limits. [P2 §3; R1 §§3–4.]

**Round-1 Q9 documentation correction: CLOSED.** CL now explicitly requires T0 counts and gain in both the evaluated-arm and reference roles for a self-comparison. It also states that omitting the reference arguments yields `reference unavailable`. The executable implementation is unchanged. [CL, lines 176–205.]

### N1 — Nonblocking precision correction in P2's coverage description

P2 §2 says T-S2 shows “exactly four (outcome, cause) kinds.” There are **four post-prerequisite classes**, and **five normalized classes overall**:

| Scope | T-S2 classes |
|---|---|
| After T-S1′ locates the high boundary | PASS; FAIL `hysteresis`; ND `bracket outside fine grid`; ND apparatus |
| Additional class over the entire input domain | ND because T-S1′ did not locate a boundary |

T5 explicitly requires all five normalized classes. Its dependency cause includes the high failure, so literal full cause strings can be more numerous; normalization deliberately groups them. The three former low-phase causes no longer independently decide T-S2 after the prerequisite passes, although phase words can still occur inside a high-prerequisite explanation. [P2, line 37; T5, lines 733–747; T0, lines 310–312.]

Recommended evidence wording: **“Four post-prerequisite T-S2 classes; five normalized classes overall, including the retained dependency ND.”** This is a reporting clarification. The source and tests already implement the correct behavior; no blocking code repair follows from it.

### Exact-limit witnesses

The added reversal witness reproduces the exact band `37,599/(2D)`, where `D = 10,000,000`. Reversals of 37,598 and 37,599 twice-median units pass; 37,600 yields reversal ND at `(1.450000, 1.500000)`. The added slope witness also tests equality exactly. [T5, lines 365–383.]

For precision, the added slope test's whole-tail-sum increments 249,999 / 250,000 / 250,001 correspond to 499,998 / 500,000 / 500,002 twice-median units. R1's nearest attainable half-count offsets were 499,999 / 500,000 / 500,001. This difference does not invalidate the added equality test. L2 additionally executed those nearest attainable cases, distributing twenty seeds at each of adjacent integer tail sums and keeping the endpoint range at 4,000,000 twice-median units:

| Twice-median increment across 1.00 → 1.05 | Exact J | Exact limit | T-S1c |
|---:|---|---|---|
| 499,999 | 499999/10000000 | 1/20 | PASS |
| 500,000 | 1/20 | 1/20 | PASS |
| 500,001 | 500001/10000000 | 1/20 | ND `continuity unresolved at grid resolution (1.050000)` |

The second implementation agreed in all three cases. No arithmetic defect or additional required repair was found. [R1 §5; T5, lines 378–383, 637–651; independent execution for this review.]

## 6. Executed verification

**Environment:** Linux; Python 3.12.14; pytest 9.2.0; pluggy 1.7.0; NumPy 2.3.5; SciPy 1.17.0. The primary runtime initially lacked pytest. An existing local dependency directory was supplied through `PYTHONPATH`, plugin auto-loading was disabled, and the submitted test files were run unmodified. The initial missing-pytest invocation collected no tests.

| Verification | Result |
|---|---|
| Archive, inventory, manifest, and ZIP integrity | Supplied archive hash matches; exactly 77 payload files plus manifest; all 77 full hashes match; no duplicate, missing, or extra payload; CRC check passes |
| Packet continuity against R1 receipt | 67 old paths retained: 64 unchanged, exactly the disclosed three changed; 10 additions |
| Complete M5 suite | **27 passed in 95.49 s; no deselection** |
| Original Appendix A counterexample | Required repaired result; exact program and output identities verified |
| Independent decision-table checker | **2,162 checks passed**, including malformed-input refusals |
| Paired complete-record comparisons | Six witnesses inspected; differences as in §4 |
| Paired final-aggregation checks | Twelve cases passed; the other three test records remained identical |
| Nearest attainable slope-limit cases | Three cases passed, with matching second-implementation results |
| Declaration recomputation | Both round-2 declarations and the prior T0 declaration match their literals |
| Earlier retired-master test | **PASS** with the supplied source dependency |
| Three earlier preservation tests | **FAIL**, at their disclosed folder-equality assertions |

The complete M5 run includes both nonconvergence tests, the added D1 and exact-limit cases, and the 4,000 randomized sweep-set comparison. That comparison checks every test's outcome and full cause, and the final determination and cause, against the second implementation. It requires at least 200 complete low sweeps without a boundary under a located high boundary. Its arithmetic is separately expressed through `Fraction` and `statistics`. It shares the declared reading of the contract; agreement is implementation evidence for the ruled semantics, not an independent governance ruling. [T5, lines 627–670, 708–749; complete-run result above.]

The substantive M5 command, from `flights/mfa_fidelity/instrument`, was:

~~~bash
python -B -m pytest tests/test_f9_m5.py -v -p no:cacheprovider
~~~

The invocation additionally selected a dedicated temporary directory. Pytest dependencies and the instrument directory were on `PYTHONPATH`; `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` was set.

### Earlier-module evidence and its limit

I reran the four specific earlier tests implicated in R1. The result was **1 passed, 3 failed in 0.67 s**, with four tests collected:

| Test | Observed result |
|---|---|
| T2 `test_every_earlier_master_is_refused_l2_m2_round1_r2` | PASS. The supplied `design/flight9/probe/f9_probe.py` resolves the previously missing dependency. |
| T2 `test_m1_e1_and_f8_are_byte_unchanged` | FAIL at line 659: historical exact folder-membership assertion |
| T3 `test_everything_placed_before_m3_is_byte_unchanged` | FAIL at line 534: historical exact folder-membership assertion |
| T4 `test_everything_placed_before_m4_is_byte_unchanged` | FAIL at line 559: historical exact folder-membership assertion |

The three failures occur after their preceding per-file digest checks pass. They continue to forbid later additive module files, as already disclosed by P1 and R1. M5's own preservation test passes. These are separately tracked test-maintenance defects, and the combined earlier-module suite cannot be described as green. [P1 §4.5; P2 §5; R1 §6; T2:659; T3:534; T4:559; T5, final preservation test.]

The retired-master test reads and parses the probe script as source; the probe was not imported or executed. Its source-grounding and refusal checks now complete on the submitted packet. This closes the earlier packet-dependency limitation for that test. [T2, lines 115–142; P2, line 69.]

The focused command was:

~~~bash
python -B -m pytest \
  tests/test_f9_m2.py::test_every_earlier_master_is_refused_l2_m2_round1_r2 \
  tests/test_f9_m2.py::test_m1_e1_and_f8_are_byte_unchanged \
  tests/test_f9_m3.py::test_everything_placed_before_m3_is_byte_unchanged \
  tests/test_f9_m4.py::test_everything_placed_before_m4_is_byte_unchanged \
  -v -p no:cacheprovider
~~~

The entire earlier M1–M4 suite was not rerun in this round. R1's earlier full-suite results are historical evidence, not newly executed results.

## 7. Disposition and retained obligations

The sole blocking round-1 M5 finding is repaired. The source, declaration, tests, reproducer, and recorded reading now agree. No new blocking M5 finding remains. N1 is a nonblocking clarification of the evidence description.

The three earlier preservation-test repairs remain separate. The recommended append-only disclosure of skeleton nonconvergence at κ = 1.00 remains an item for Mike before fidelity reporting; this review does not treat the untested-arm expectation as measured evidence. The accepted duties for run-record provenance, complete authorized calibration, map/edge comparisons, local m reporting, and uncertainty reporting remain with their downstream modules. [P2 §5; R1 §§6–8; C9 §§1.2′, 5.7–5.9, 8.]

This review gives L2's technical disposition on the submitted build. Placement, declaration ratification, and authorizations for scientific jobs remain Mike's actions. The review used source inspection, module tests, and constructed aggregate fixtures; it did not perform canonical flight jobs or use probe output.

## Appendix A — Independent decision-table checker

The following is the exact executed audit program. Save it as `audit_work/d1_semantics/check_d1.py` beneath the extracted archive root and run `python -B audit_work/d1_semantics/check_d1.py` from that root. It imports the reviewed files from the extracted packet.

Program SHA-256: `6deb834e1a84d980f28c2edc7babc097a5ba58cd9576b68beda66b420be8ef2f`.

```python
from pathlib import Path
import copy, json, sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'flights/mfa_fidelity/instrument'))
from mfa_instrument.f9 import config as C, t0 as T
G = tuple(C.F9_LEVELS_MICRO)

def observation(n):
    return {'survival': [True] * n + [False] * (40-n), 'tail_sum': [1_000_000]*40}

def sweep(met):
    return {k: observation(36 if flag else 35) for k, flag in zip(G, met)}

def crossing(j):
    return sweep([i >= j for i in range(len(G))])

profiles = {
    'none': sweep([False]*25),
    'all': sweep([True]*25),
    'nonmonotone_with_suffix': sweep([False]*4+[True,False]+[True]*19),
    'nonmonotone_no_suffix': sweep([False]*4+[True]+[False]*20),
}
realization={k: observation(40) for k in G}
calibration={o: {k:[1_000_000]*40 for k in G} for o in ('skeleton','realization')}
counts={}

# Independent T-S2 table; no calls to the implementation's boundary or eligibility helpers.
def expected(high,low):
    hm=[high.get(k) is None for k in G]
    hb=[sum(high[k]['survival']) >= 36 for k in G] if not any(hm) else None
    if hb is None or all(hb) or not any(hb) or any(hb[i] and not hb[j] for i in range(25) for j in range(i+1,25)):
        return 'ND','prerequisite'
    if any(low.get(k) is None for k in G):
        return 'ND','apparatus unevaluable (missing level record)'
    lb=[sum(low[k]['survival']) >= 36 for k in G]
    hc=G[hb.index(True)]
    lc=None if all(lb) or not any(lb) or any(lb[i] and not lb[j] for i in range(25) for j in range(i+1,25)) else G[lb.index(True)]
    # Only 1.05...2.00 have an immediately preceding fine-grid level 0.05 below.
    if not (1_050_000 <= hc <= 2_000_000 and lc is not None and 1_050_000 <= lc <= 2_000_000):
        return 'ND','bracket outside fine grid'
    return ('PASS',None) if abs(hc-lc) <= 75_400 else ('FAIL','hysteresis')

def check(group, high, low):
    r=T.evaluate_t0(high,low,realization,calibration)
    got=r['tests'][2]
    exp=expected(high,low)
    if exp[1]=='prerequisite':
        assert got['outcome']=='ND' and got['cause'].startswith('not evaluable: T-S1′ did not locate a boundary ('), (group,got,exp)
    else:
        assert (got['outcome'],got['cause'])==exp,(group,got,exp)
    for name,s in [('skeleton_high',high),('skeleton_low',low)]:
        record=r['persistence'][name]
        if all(s.get(k) is not None for k in G):
            assert {k:record['levels'][k]['survivors'] for k in G} == {k:sum(s[k]['survival']) for k in G}
        else:
            assert record['kind']=='apparatus'
    if exp[1]=='bracket outside fine grid' and low in list(profiles.values()):
        assert got['detail']['low_profile']==r['persistence']['skeleton_low']['profile']
    counts[group]=counts.get(group,0)+1

for i in range(1,25):
    high=crossing(i)
    for j in range(1,25): check('every_boundary_pair',high,crossing(j))
    for low in profiles.values(): check('complete_low_without_boundary',high,low)
    for k in G:
        for form in ('omitted','None'):
            low=crossing(5)
            if form=='omitted': del low[k]
            else: low[k]=None
            check('low_missing_at_every_level',high,low)

for high in profiles.values():
    for low in [crossing(i) for i in range(1,25)] + list(profiles.values()) + [{}, {G[0]:None}]:
        check('high_prerequisite_profiles',high,low)
for k in G:
    high=crossing(5); high[k]=None
    for low in [crossing(1),crossing(5),crossing(24),profiles['none'],profiles['all'],{}]:
        check('high_prerequisite_missing',high,low)

# Valid absence may become bracket ND; malformed observations must still raise, in eligible and ineligible contexts.
invalid=[]
def bad_obs(**changes):
    x=observation(35); x.update(changes); return x
invalid += [bad_obs(survival=[1]*40),bad_obs(survival=[True]*39),bad_obs(tail_sum=[-1]*40),bad_obs(tail_sum=[True]*40),bad_obs(tail_sum=[1.0]*40),bad_obs(tail_sum=[10_000_001]*40)]
x=observation(35); del x['survival']; invalid.append(x)
x=observation(35); x['extra']=0; invalid.append(x)
invalid += [bad_obs(survival=[True]*40,tail_sum=[0]*40),bad_obs(survival=[False]*40,tail_sum=[10_000_000]*40)]
for high in [crossing(1),crossing(5)]:
    for obs in invalid:
        low=copy.deepcopy(profiles['none']); low[G[10]]=obs
        try: T.evaluate_t0(high,low,realization,calibration)
        except T.F9T0Error: counts['malformed_refusals']=counts.get('malformed_refusals',0)+1
        else: raise AssertionError('malformed observation relabelled instead of refused')
print(json.dumps({'status':'PASS','checks':counts,'total':sum(counts.values()),'eligible_boundaries':[k for k in G if 1_050_000 <= k <= 2_000_000]},indent=2))
```

## Appendix B — Paired record and aggregation witnesses

The following is the exact executed audit program. Save it as `audit_work/change_audit/record_witnesses.py` beneath the extracted archive root and run `python -B audit_work/change_audit/record_witnesses.py` from that root. It imports the reviewed files from the extracted packet.

Program SHA-256: `62437dc49eb32478099069d1e83d84656bbb321a0af51c5052673b8f99ceb7e4`.

```python
from pathlib import Path
import copy,hashlib,importlib.util,json,sys
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'flights/mfa_fidelity/instrument'))
from mfa_instrument.f9 import config as C,t0 as new,closure as cl
spec=importlib.util.spec_from_file_location('mfa_instrument.f9.audit_round1_t0',root/'packet_only/round1/t0.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
grid=C.F9_LEVELS_MICRO

def obs(active): return {'survival':[active]*40,'tail_sum':[1_000_000 if active else 0]*40}
def sweep(boundary): return {k:obs(i>=boundary) for i,k in enumerate(grid)}
none=sweep(len(grid)); all_=sweep(0); nm=sweep(10);nm[grid[3]]=obs(True)
lows={'none':none,'all':all_,'nonmonotone':nm}
calibration={o:{k:[1_000_000]*40 for k in grid} for o in ('skeleton','realization')}

def differing(a,b,path=''):
    out=[]
    if isinstance(a,dict) and isinstance(b,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a:out.append({'path':path+'/'+str(k),'before':'<absent>','after':b[k]})
            elif k not in b:out.append({'path':path+'/'+str(k),'before':a[k],'after':'<absent>'})
            else:out+=differing(a[k],b[k],path+'/'+str(k))
    elif isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        for i,(x,y) in enumerate(zip(a,b)):out+=differing(x,y,path+'/'+str(i))
    elif a!=b: out.append({'path':path,'before':a,'after':b})
    return out
cases=[('eligible_pass',sweep(5),sweep(6)),('eligible_fail',sweep(5),sweep(7)),('ineligible',sweep(1),sweep(5)),('low_missing',sweep(5),{**sweep(5),grid[10]:None}),('high_absent',none,sweep(5)),('complete_low_absent',sweep(5),none)]
record=[]
for name,hi,lo in cases:
    a=old.evaluate_t0(hi,lo,sweep(0),calibration);b=new.evaluate_t0(hi,lo,sweep(0),calibration)
    record.append({'case':name,'changes':differing(a,b)})
aggregation=[]
for ln,lo in lows.items():
    for prior_nd in (False,True):
        for realization_fail in (False,True):
            hi=sweep(5);re=sweep(0);cal=copy.deepcopy(calibration)
            if prior_nd:
                hi[grid[10]]={'survival':[True]*40,'tail_sum':[900_000]*40}
                cal['skeleton'][grid[10]]=None
            if realization_fail: re[grid[7]]=obs(False)
            a=old.evaluate_t0(hi,lo,re,cal);b=new.evaluate_t0(hi,lo,re,cal)
            want=('NOT PRODUCED','realization extinct at 1.300000') if realization_fail else ('NOT DISTINGUISHED','apparatus unevaluable (missing calibration level record)' if prior_nd else 'bracket outside fine grid')
            assert (b['determination'],b['cause'])==want,(ln,prior_nd,realization_fail,b['determination'],b['cause'])
            for i in (0,1,3):assert a['tests'][i]==b['tests'][i]
            aggregation.append({'low':ln,'earlier_nd':prior_nd,'realization_fail':realization_fail,'before':(a['determination'],a['cause']),'after':(b['determination'],b['cause'])})
out={'python':sys.version.split()[0],'record_witnesses':record,'aggregation_cases':aggregation,'independent_declaration_sha256':{'closure':hashlib.sha256(repr(cl.CLOSURE_DECLARATION).encode('utf-8')).hexdigest(),'t0_round1':hashlib.sha256(repr(old.T0_DECLARATION).encode('utf-8')).hexdigest(),'t0_round2':hashlib.sha256(repr(new.T0_DECLARATION).encode('utf-8')).hexdigest()}}
print(json.dumps(out,indent=2))
```

FINAL VERDICT: SOUND
