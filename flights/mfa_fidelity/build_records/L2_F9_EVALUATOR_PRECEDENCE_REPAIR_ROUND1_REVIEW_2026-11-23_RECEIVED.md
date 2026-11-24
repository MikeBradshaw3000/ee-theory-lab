| Receipt item | Independently computed | Comparison / result |
|---|---|---|
| Archive | f9_evaluator_repair_round1_L2.zip | Attached copy verified |
| Archive SHA-256 | `e82a62ed1dacd0d79cfbf72a9f866ae38002791d53d1220253f094e97dcf37f9` | MATCH — user-supplied digest |
| Manifest-listed payload files | 85 | MATCH — supplied count 85 |
| Regular archive files | 86 | 85 payload files plus MANIFEST.txt |
| Missing / extra payload files / duplicate paths | 0 / 0 / 0 | PASS |
| MANIFEST.txt SHA-256 | `bd08e095f1d13a77a79a54a2ddc78ec4d3f89ea33e09d620ed4b6a65b82145a3` | Computed separately; not self-listed |
| Payload digests | 85 of 85 match | Full computed digests in manifest order below |
| Source preservation after review | All 85 extracted payload digests still match | No packet source edited |

| # | Manifest-listed file | Independently computed SHA-256 | Against MANIFEST.txt |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_EVALUATOR_PRECEDENCE_REPAIR_PACKET_2026-11-23.md` | `265d3ea3e2658c7f53445c775cecd845aa68e968f1216d2d06f8af65e4d2c5f8` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` | `ddfa49b11955de42d5b6638d892af4c75756ff6b1b5f35ea0884c4de7b2a07a1` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/tests/test_f9_m3.py` | `d167f77229fa87cd4aca2fe06dfc051182d068cd95699e2a710f2ac19da312f5` | MATCH |
| 4 | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` | `751c808680521a0ac7ae088cd0edd1635a48eda7d5f7fabd15fec179fca1ab61` | MATCH |
| 5 | `flights/mfa_fidelity/instrument/tests/test_f9_m5.py` | `5843bec1a35be64da87b31fb72eb223d54cbf323b8db02177d218ba716532954` | MATCH |
| 6 | `flights/mfa_fidelity/instrument/tests/test_f9_m6.py` | `606b079793b064b646a3c2565486566d00e4464fd90574f57fea4493a4c6e16b` | MATCH |
| 7 | `flights/mfa_fidelity/build_records/f9_evaluator_precedence_repair_2026-11-23.diff` | `4b3868853455e9027171e6e2276ae53c0028e292bf85d38710010ca54646793c` | MATCH |
| 8 | `flights/mfa_fidelity/build_records/f9_m1_to_m6_container_evaluator_repair_2026-11-23.txt` | `a87b028d1f9c89e80d3e2ff0e696c22c559fd76715f727b9008ef9bf675f87e9` | MATCH |
| 9 | `flights/mfa_fidelity/build_records/f9_evaluator_repair_placed_routes_2026-11-23.txt` | `21abdef71dd9fed456eb031946b9f343c21aa097b2eaf72ec130d1c893a58839` | MATCH |
| 10 | `flights/mfa_fidelity/build_records/l2_m6b_round1_reproduce.py` | `6c93b4ba29f784547b0b7bbc87c7f5974e1e875aa4dbc6e1dde8eb501ea4cb98` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/L2_F9_M6B_ROUND1_REVIEW_2026-11-23_RECEIVED.md` | `31fd32e258482f81d3fc8762271fc4f722ac69d6ae77a73a97b30fb7c58dd78f` | MATCH |
| 12 | `packet_only/before/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | MATCH |
| 13 | `packet_only/before/test_f9_m3.py` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` | MATCH |
| 14 | `packet_only/before/test_f9_m4.py` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` | MATCH |
| 15 | `packet_only/before/test_f9_m5.py` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` | MATCH |
| 16 | `packet_only/before/test_f9_m6.py` | `74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56` | MATCH |
| 17 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 18 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 19 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 20 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 21 | `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | `473a2a165fd5cb4e38ddb064dc14c24880af8998a21b9ffad1aa7c065551016c` | MATCH |
| 22 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |
| 23 | `flights/mfa_fidelity/rulings/F9_MASTER_RULING_RECORD.md` | `02b98378057e776769b48150059a2b9323737fd5ab437f907ae4d62c3fc27b75` | MATCH |
| 24 | `flights/mfa_fidelity/rulings/F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` | `b38a4ff6eaa3e2118a9ae723cff63a3336fb178a35932071c3dc43c4478c50a6` | MATCH |
| 25 | `flights/mfa_fidelity/rulings/F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` | `bc5fac1d53fd57ac0923fb759e465e8783389d92cb1188e297c185c5b91ac78d` | MATCH |
| 26 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 27 | `flights/mfa_fidelity/build_records/F9_M3_PLACEMENT_NOTE_2026-11-17.md` | `2df87fe689368752f92f5e5bd90f09ccef819255b2e5b44c4b1a6526314898f7` | MATCH |
| 28 | `flights/mfa_fidelity/build_records/L2_F9_M3_ROUND2_REVIEW_2026-11-17_RECEIVED.md` | `939dca526bdbcdbf52880e5c0b93ca988f0364d24af151f60e478cf8a219ccfe` | MATCH |
| 29 | `flights/mfa_fidelity/build_records/F9_M4_PLACEMENT_NOTE_2026-11-18.md` | `b6004b9281aedc276b37244550baf9775853d5e678f7a1581b79fff754284839` | MATCH |
| 30 | `flights/mfa_fidelity/build_records/F9_M6_PLACEMENT_NOTE_2026-11-23.md` | `c904a70978f5b32efc0b715c3e474d7e2931f6aab36603b8898f9bc9af20382b` | MATCH |
| 31 | `flights/mfa_fidelity/build_records/L2_F9_M6_ROUND2_REVIEW_2026-11-23_RECEIVED.md` | `2287afecc3b9eee634d0b42ffa7b6e26c2cac0f4a2e2f370888c35025c5f5bcd` | MATCH |
| 32 | `flights/mfa_fidelity/build_records/f9_m1_to_m6_canonical_2026-11-23.txt` | `4508d91c3f49346d1977fa56b53229875506c4e6788aaade07bfe86c5519b974` | MATCH |
| 33 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `e505cd6bd302c1e005b37f4bc4ad364300b83fd4ab40bb73ac6ef18c0084073a` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py` | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/reports.py` | `f42f93c586288ee14ee11dfe8e2430e544e81529a2eaba17e73b0bf4345a92de` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/t0.py` | `a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 72 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 73 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 74 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 75 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 76 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 77 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 78 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 79 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 80 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 81 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 82 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 83 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 84 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 85 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 evaluator precedence repair, round 1

**Date:** 2026-11-23. **Role:** L2, adversarial reviewer. **Decision authority:** Mike.

**Reviewed archive:** f9_evaluator_repair_round1_L2.zip  
**Archive SHA-256:** e82a62ed1dacd0d79cfbf72a9f866ae38002791d53d1220253f094e97dcf37f9

**Scope:** The separately authorized repair of the placed evaluator's constant-index cause precedence, its new regression, the three downstream evaluator-identity pins, and the two carried M6 test-description corrections. The requested five-file inverse reconstruction is included in §2 and executable Appendix A.

## 1. Disposition and evidence boundary

**The scoped repair is sound.** The changed evaluator gives an empty comparison family the required “no eligible contour” cause before considering the observed map's empty/full or under-resolved state. Input validation remains ahead of returned scientific/unavailable records. The geometric point record remains intact. The new regression distinguishes the repaired evaluator from the pinned one, and the five repaired files reverse exactly to their supplied pinned identities. [P §§1–3; C §7 L1–L4; C §6.2 row 15; E 417–437; §2 and §5 below]

One qualification matters for Q3: invariance of the downstream outcome record holds for **correctly bound declared terrain/family inputs**. It does not hold for every synthetic or mislabeled record that the previous implementation happened to accept. A constant-family evaluation labelled as a non-T0 terrain can now be rejected by the existing outcome validator, because the repaired cause exposes the invalid binding. This is expected enforcement of the existing domain, not a blocker in the repair. [O 231–257; §4.2 below]

This disposition covers the dependency repair as its own cycle, following Mike's ruling recorded in P. It does not clear the absent M6B orchestration copy, withdraw the earlier M6B disposition, certify qualification, establish canonical placement, or authorize a scientific-stage job. The copy and its own route regressions remain for the separate M6B return. [P header, §2; PRIOR §2]

### Source locator key

The locators below are relative to the received archive's flights/mfa_fidelity/ directory. Line numbers refer to the received repaired bytes unless explicitly labelled “before.” The opening receipt binds the full source identities.

| Key | Packet source |
|---|---|
| P | build_records/L1_TO_L2_F9_EVALUATOR_PRECEDENCE_REPAIR_PACKET_2026-11-23.md |
| C | contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md |
| FREEZE | contracts/flight9/FLIGHT_9_FREEZE_RECORD.md and FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md |
| E | instrument/mfa_instrument/f9/evaluator.py |
| T3, T4, T5, T6 | instrument/tests/test_f9_m3.py through test_f9_m6.py |
| O | instrument/mfa_instrument/f9/outcomes.py |
| CL | instrument/mfa_instrument/f9/closure.py |
| T0 | instrument/mfa_instrument/f9/t0.py |
| R | instrument/mfa_instrument/f9/reports.py |
| DIFF | build_records/f9_evaluator_precedence_repair_2026-11-23.diff |
| PRIOR | build_records/L2_F9_M6B_ROUND1_REVIEW_2026-11-23_RECEIVED.md |
| M6R2 | build_records/L2_F9_M6_ROUND2_REVIEW_2026-11-23_RECEIVED.md |
| M6PLACE | build_records/F9_M6_PLACEMENT_NOTE_2026-11-23.md |
| M3PLACE | build_records/F9_M3_PLACEMENT_NOTE_2026-11-17.md |

The frozen contract identity is 60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168. FREEZE supplies the authority for those bytes despite the contract's retained historical draft header.

The stated repository pin is c6c21c497366d3ca71e0487127c774aacfd14ba1. This review verifies the supplied repaired bytes, the supplied before copies and their named identities. It does **not** claim an independent remote-Git authentication of that commit or of every unchanged file at that commit. The package's identity checks and the exact five-file reconstructions are the evidence actually established here.

## 2. Q1 — Exact change boundary and inverse-edit reconstruction

**Yes. Each of the five changes is confined to P §2.** I used two complementary inverse procedures:

1. Explicitly undo the named edits in the repaired files: restore the branch order and docstring; remove the added test/helper block; restore each evaluator pin and its annotation; restore the two M6 wording passages. All reconstructed files were written before the before copies were opened for comparison.
2. Independently reverse every hunk of the supplied unified diff against the repaired archive bytes, checking every context/added line at its stated repaired-file position. Only afterward compare the reconstructed files with the before copies. Appendix A is the complete, executed reproducer for this second method.

Both methods reproduced all five prior byte sequences. The before copies were comparison oracles, not replacement sources. A whole-file hash comparison alone would not establish this reconstruction; the executed inverse operations do.

### Reconstructed identities

| File (relative to instrument/) | Repaired SHA-256 | Reconstructed prior SHA-256 | Against before copy and named pin |
|---|---|---|---|
| `mfa_instrument/f9/evaluator.py` | `ddfa49b11955de42d5b6638d892af4c75756ff6b1b5f35ea0884c4de7b2a07a1` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | EXACT BYTE MATCH |
| `tests/test_f9_m3.py` | `d167f77229fa87cd4aca2fe06dfc051182d068cd95699e2a710f2ac19da312f5` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` | EXACT BYTE MATCH |
| `tests/test_f9_m4.py` | `751c808680521a0ac7ae088cd0edd1635a48eda7d5f7fabd15fec179fca1ab61` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` | EXACT BYTE MATCH |
| `tests/test_f9_m5.py` | `5843bec1a35be64da87b31fb72eb223d54cbf323b8db02177d218ba716532954` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` | EXACT BYTE MATCH |
| `tests/test_f9_m6.py` | `606b079793b064b646a3c2565486566d00e4464fd90574f57fea4493a4c6e16b` | `74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56` | EXACT BYTE MATCH |

### Exact edits established

| File | Complete observed change |
|---|---|
| evaluator.py | The module docstring expands by four net lines. In evaluate_level, the existing empty-family and noninformative-point branches exchange order, with an explanatory comment. No other source edit. |
| test_f9_m3.py | One 33-line addition: the new crossed-state test, its _same_point helper, and separation lines. Every pre-existing line is retained. |
| test_f9_m4.py | The evaluator SHA-256 in PLACED changes to the repaired identity, and the PLACED comment gains the repair annotation. |
| test_f9_m5.py | The same pin and annotation changes. |
| test_f9_m6.py | The same pin and annotation changes, plus the all-active/all-inactive loop comment and the cross-width test docstring. No assertion or other executable test logic changes. |

[E 57–61, 430–434; T3 490–522; T4 540, 550; T5 765, 775; T6 456, 493–495, 765, 775]

The 162-line supplied diff has SHA-256 4b3868853455e9027171e6e2276ae53c0028e292bf85d38710010ca54646793c. Regenerating the complete diffs of all five file pairs matched its hunk coordinates, context lines, removals and additions. Only Git metadata and the descriptive suffix after each hunk header were excluded from that textual comparison; the old/new Git blob prefixes were checked separately and matched. The independent reversal in Appendix A also succeeded without offsets or fuzzy matching.

The M6 module ASTs are identical after normalizing the one evaluator hash and omitting docstrings; comments are absent from the AST. This corroborates that the two wording repairs do not alter assertions or test execution.

The evaluator declaration tuple and its literal digest remain unchanged:

79e93ccade624ec473c7c60225183458e0ed168e13c4e23fb7dbaa6ed2d2fef7

The changed source identity is correctly distinct from that unchanged declaration identity. The branch repair changes implementation bytes; it does not change the registered numerical constants, declared stream construction or support-count rule. [E declaration; DIFF; T3 declaration verification]

## 3. Q2 — Precedence and the other evaluator paths

### The checked entry point

The repaired order is:

1. Verify the evaluator declaration and validate counts, the family mapping and the stream key.
2. Validate every supplied constructed-resample row, even when no bootstrap will ultimately run.
3. Compute the observed point record.
4. For each index, return the empty-family cause first; otherwise return a noninformative map's cause; otherwise include that index in the bootstrap.

[E 417–438]

This implements §7's L2-before-L3/L4 requirement while preserving L1 apparatus priority. The contract also states explicitly that the constant-index cause does not depend on the sample. No change to the frozen rule is needed or made. [C 358, 370, 378–382]

Focused checks with constant families confirmed rejection of malformed count shape/type/range, invalid stream keys and malformed supplied multiplicities. A separate family-type check also raised. These failures are not converted into “no eligible contour.” Existing declaration and validation tests remain part of the executed M3 suite.

### evaluate_map and fit

There is no second competing per-index cause in these paths:

- With noninformative point geometry, evaluate_map returns the map's reason and an empty indices mapping. It has not assigned that map reason as an index-level unavailable cause.
- With informative geometry, evaluate_map calls fit. For an empty family, fit immediately returns status “no eligible contour.”
- evaluate_level retains the point record but assigns its own outer per-index result using the corrected precedence.

[E 337–340, 361–376, 425–437]

Thus a record may correctly contain both a point reason such as “the region is empty” and an index cause of “no eligible contour.” The former describes the map; the latter states the higher-priority reason the comparison index is not scored. Replacing the point reason would lose valid diagnostic information.

evaluate_map remains the previously disclosed internal helper accepting already-checked inputs. This repair does not change that interface or imply that it independently performs evaluate_level's apparatus validation. [M3PLACE, “An unchecked internal entry”; E 361–376]

## 4. Q3 — What changes, and what downstream consumers see

### 4.1 Exact evaluator change domain

For valid evaluator inputs, the behavior can be partitioned completely:

| Family | Observed point geometry | Before → repaired outer index record |
|---|---|---|
| Empty | Noninformative | Same result “not informative” and resampled=False; cause changes from the map cause to “no eligible contour” |
| Empty | Informative | Unchanged: “no eligible contour,” no resampling for that index |
| Nonempty | Noninformative | Unchanged: map cause, no resampling |
| Nonempty | Informative | Unchanged: same applicable index and bootstrap path |

The applicable-family predicate is nonempty family AND informative point in both versions. Consequently the same indices enter the same loop, in the same order, with the same counts, key and supplied/generated multiplicities. Nothing changes the point calculation, stream generator, draw typing, fitted level, discrepancy, count aggregation or final supported result for those indices. The only returned evaluator field changed in the crossed defect state is the affected outer index's cause. [E 425–468; DIFF]

This conclusion follows from the exhaustive branch partition and the exact source boundary, with the relevant regression and focused probes providing execution evidence. It is not an empirical claim to have enumerated every possible array.

### 4.2 Downstream invariance has a domain

| Consumer | Result on correctly bound declared inputs |
|---|---|
| outcomes.level_from_evaluation | Unchanged. T0's existing branch already emits the constant-index unavailable state whatever its map; non-T0 declared families are nonempty, so their evaluator record does not change. |
| closure.py | Unchanged. It does not consume evaluator level causes; its outcome-module calls concern persistence records. |
| t0.py | Unchanged. Its consistency calculations do not depend on the repaired branch. |
| reports.py | Unchanged. Its evaluator calls use check_counts and box_sum, both unchanged. |

[O 231–257; CL 176–219; T0 outcome references; R 186, 262]

**The literal “any input” extension needs qualification.** I took an empty-map evaluation with two constant families and supplied it to outcomes.level_from_evaluation as terrain TA, composition P:

| Evaluator record supplied | Existing outcome consumer's behavior |
|---|---|
| Before: both index causes are the map cause | Accepts the record as scientific ND/no edge |
| Repaired: both index causes are “no eligible contour” | Raises F9OutcomeError: that constant-index state belongs to T0 only |

The latter rejection is the existing guard at O 254. A mixed constant/nonconstant record can similarly reveal unequal unavailable causes and be rejected by O 250–251. These synthetic bindings are outside the declared terrain/family domain assumed by the outcome layer. The repaired cause exposes an inconsistency previously masked by the map cause; it does not invalidate the repair.

For the same correctly labelled T0 input, the before and repaired outcome records were exactly equal. The review therefore accepts L1's declared-panel conclusion while declining a universal downstream-invariance claim for arbitrary synthetic or mislabeled records.

The qualification harness is not supplied or built in this packet. The correction makes the evaluator's constant-index cause conform to the existing row-15 oracle; it does not establish that a qualification run has passed. [C §6.2 row 15; P §§4–5]

## 5. Q4 — Discrimination, coverage and the proposed L5 case

### The new regression is discriminating

The submitted test crosses five map constructions with four family sets: two constant, two nonconstant, constant P/nonconstant H, and the reverse. It checks the exact constant-index record, ordinary map causes, separate point diagnostics and the original small patch's 60 cells/32 bonds. [T3 490–520]

I invoked the **unchanged submitted test function** with direct synthetic IndexFamily fixtures:

- Repaired evaluator: the complete test passed.
- Pinned evaluator: expected assertion failure at T3 506 on the first “empty” construction. Both constant indices incorrectly returned “no edge at theta.”

Only the fixture construction was substituted to avoid a second identity-bundle build; the test function and its assertions were unchanged. The ordinary pytest suite also executes that test with its supplied fixture. This is a genuine before/after discriminator rather than a passing check of repaired bytes alone.

### Existing coverage and useful additional crosses

The maintained suite already tests informative geometry with constant families, informative mixed families where the nonconstant index continues to resampling, and the 50/51 invalid-draw boundary for ordinary families. [T3 473–487, 523–543]

The new test does not itself cover every cross. I specifically checked the three most relevant omissions:

| Focused construction | Observed repaired behavior |
|---|---|
| Constant families with a small complement | Point: 9,951 region cells, 28 bonds, complement-under-100 reason. Both outer index causes: “no eligible contour.” |
| Malformed input with constant families | Eight count/key/multiplicity cases were refused before unavailable records; separate family-type validation also refused malformed input. |
| Informative map with constant families and a resample-generator failure spy | No resample-generator call; constant-family records returned normally. |
| Constant index beside a nonconstant index with 51 invalid constructed draws | Constant: no eligible contour, resampled=False, no draw-count arrays. Nonconstant sibling: 949 compatible, 0 adverse, 51 invalid, “unstable edge.” |

The last probe uses the supported constructed-multiplicity testing interface and correctly records declared_stream=False. It is not presented as a canonical stream result.

**An empty-family index cannot itself become L5 in this implementation.** It is excluded from applicable before the draw loop. The meaningful cross is an index that remains L2 while a nonconstant sibling becomes L5; the focused probe demonstrates exactly that. No new precedence branch is required.

I regard the new regression, existing coverage, direct source argument and additional checks as sufficient for this contained repair. Adding the small-complement, constant/malformed-input and mixed-L5 cases to the maintained suite would improve future regression coverage, but their absence from the submitted new function is not a blocker here.

## 6. Q5 — Deferral of the two cause strings

**The deferral is consistent with this repair being sound on its own.** Mike's ruling, as recorded in P, explicitly defers changing “no edge at theta” and “below the informative minimum.” Their existing translation in outcomes.EVALUATOR_CAUSES remains intact:

| Raw evaluator cause | Outcome/contract label |
|---|---|
| no edge at theta | no edge at θ |
| below the informative minimum | under-resolved |
| no eligible contour | no eligible contour |
| unstable edge | unstable edge |

[P header and §2; O 144–147, 241–245]

The corrected constant-family cause already has the required wording. Renaming the two other strings is unnecessary to enforce its precedence and would expand the dependency repair into the translator and its declarations. The explicit renewed deferral supersedes the earlier next-touch wording; that carried item remains open rather than being silently marked repaired.

## 7. Q6 — The two M6 wording repairs

**Both satisfy the earlier notes.** Their source identities and exact inverse edits are included in §2.

### All-active and all-inactive comment

The new comment correctly says that each case leaves three occupancy bands empty, while all-active has no defined duration records and all-inactive has every duration record defined. The adjacent assertions are unchanged: the all-active case has zero defined durations; the all-inactive case has 40 × 10,000 = 400,000 defined, possibly censored durations per W. [T6 456–463; M6R2, “Nonblocking wording observations”; M6PLACE, next-touch notes]

### Cross-width consistency docstring

The new docstring limits rejection to violation of the declared between-width relations, explicitly says those relations are necessary rather than sufficient, and gives the exact impossible stack from the preceding review:

| Width | (A, R₀, first, last) |
|---:|---|
| 1 | (20, 1, True, False) |
| 10 | (20, 1, True, False) |
| 100 | (2, 1, True, False) |

At W=1, the tuple forces an active prefix of twenty ticks followed by the inactive remainder. That sequence has A=2 at W=10 and A=1 at W=100, not the proposed coarser counts. The example therefore supports precisely the stated limitation. [T6 493–495; M6R2 §2; M6PLACE, “The limit L2 put on the verdict”]

The test function's historical name remains, but the revised docstring now prevents the broad refusal sentence from being cited as a universal realizability guarantee. No new realizability claim or functional repair is introduced.

## 8. Q7 — Verification, limitations and remaining handoff

### Independent execution

**61 tests passed in 253.97 seconds; process exit code 0.** This was one process containing the complete M3 suite (38 tests), the complete M4 suite (21 tests), and the M5 and M6 identity checks (one each).

The environment was Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and task-local pytest 9.2.0. The command was run from the supplied instrument directory:

~~~text
python3 -B -m pytest tests/test_f9_m3.py tests/test_f9_m4.py tests/test_f9_m5.py::test_everything_placed_before_m5_is_byte_unchanged tests/test_f9_m6.py::test_everything_placed_before_m6_is_byte_unchanged -v -p no:cacheprovider --durations=10
~~~

Plugin autoload and bytecode writing were disabled; OPENBLAS_NUM_THREADS and OMP_NUM_THREADS were set to 1. The task-local pytest dependency directory was supplied through PYTHONPATH. No submitted test was edited to obtain this suite result.

| L2 check | Result |
|---|---|
| Complete M3 suite | 38 passed, including declaration verification, criterion/geometry, pruning, resampling, unavailable states and the new precedence regression |
| Complete M4 suite | 21 passed, including level conversion, cause translation and arm/flight aggregation |
| Downstream M5/M6 identity checks | 2 passed |
| Exact submitted new test against repaired evaluator with direct synthetic family fixtures | PASS |
| Same test against the pinned evaluator | EXPECTED FAILURE at the first constant-family/empty-map assertion |
| Constant-family small-complement, malformed-input and no-draw checks | PASS |
| Mixed constant/nonconstant family with constructed L5 sibling | PASS; constant remains L2, sibling has 949 C / 0 A / 51 I |
| Declared T0 downstream record before/after | Exactly equal |
| Synthetic constant-family record labelled TA | Old accepted ND; repaired rejected by the existing domain guard |
| Explicit five-file inverse edits and independent exact diff reversal | All five prior byte sequences and full hashes reproduced |
| Received source preservation after execution | All 85 payload hashes unchanged |

The old-evaluator failure is an intentional negative control, not a failure of the repaired suite. Initial focused-harness attempts could not import pytest until the dependency path was supplied; no submitted test executed in those setup failures. The subsequent exact-test comparisons and the 61-test suite completed as recorded.

The focused state and semantic probes, exact-test before/after comparison, explicit inverse edits and exact diff reversal all completed successfully. Appendix A includes the executable inverse reconstruction so that the five prior identities can be reproduced from the same archive without relying on this workspace.

### L1 evidence inspected, distinguished from L2 execution

The supplied combined M1–M6 log reports **277 passed in 726.87 seconds** in L1's Python 3.13.18/NumPy 2.5.3 environment. The supplied placed-route log records the original three crossed states before and after the repair. Those are L1's executions. I independently ran the focused module/downstream checks identified above; I did not repeat all six complete test files or the absent M6B routes. [P §5; build_records/f9_m1_to_m6_container_evaluator_repair_2026-11-23.txt; build_records/f9_evaluator_repair_placed_routes_2026-11-23.txt]

### Remaining boundary

No additional blocking defect was established. The Q3 domain qualification and the suggested additional maintained regressions are recorded above. The semantic-string deferral remains a carried item.

M6B still needs its own synchronized copy, identity updates and crossed-state regressions on its reported-threshold and skeleton routes. The current packet does not include that source and this review does not clear it. Splitting the dependency repair from that return is the supplied Mike ruling, so it is not an unfinished obligation within this repair's own cycle. [P §2; PRIOR §2]

All independent numerical work used source-defined constants, closed-form or synthetic comparison arrays, constructed seed maps and temporary test fixtures. No probe arrays, lattice-rule output, calibration data or canonical panel were opened or used. No scientific Flight 9 job, stage-master draw or remote placement was performed. The source-preservation check after testing is recorded in the opening receipt.

## Appendix A — Executed inverse-edit reconstruction from the archive

Save the following code as reconstruct_from_archive.py and invoke it with the received ZIP path and an empty output directory. It verifies the archive and all manifest digests, reverses each exact diff hunk from the repaired bytes, writes all five reconstructions, and only then uses the before copies to confirm byte equality and the declared prior hashes.

Example invocation:

~~~text
python3 reconstruct_from_archive.py f9_evaluator_repair_round1_L2.zip reconstructed
~~~

The program was executed in this review. All five reconstructed digests are those in §2. It creates reconstructed source copies and results.json in the selected output directory; it does not edit the archive or the repaired source tree.

~~~python
"""Reverse the packet's exact diff from repaired ZIP bytes; verify all five pins.

Usage: python3 reconstruct_from_archive.py ARCHIVE.zip OUTPUT_DIRECTORY
The before/ copies are used only after every reconstruction has been written.
"""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

EXPECTED_ARCHIVE = "e82a62ed1dacd0d79cfbf72a9f866ae38002791d53d1220253f094e97dcf37f9"
DIFF = "flights/mfa_fidelity/build_records/f9_evaluator_precedence_repair_2026-11-23.diff"
BASE = "flights/mfa_fidelity/instrument/"
FILES = {
    BASE + "mfa_instrument/f9/evaluator.py":
        "73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc",
    BASE + "tests/test_f9_m3.py":
        "b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6",
    BASE + "tests/test_f9_m4.py":
        "ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b",
    BASE + "tests/test_f9_m5.py":
        "bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8",
    BASE + "tests/test_f9_m6.py":
        "74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56",
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

archive, out = Path(sys.argv[1]), Path(sys.argv[2])
assert sha(archive.read_bytes()) == EXPECTED_ARCHIVE
out.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(archive) as z:
    manifest = {}
    for line in z.read("MANIFEST.txt").decode().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        assert re.fullmatch("[0-9a-f]{64}", digest)
        assert name not in manifest
        manifest[name] = digest
    assert len(manifest) == 85
    # Hashing before/ for receipt does not use it to construct any source.
    for name, digest in manifest.items():
        assert sha(z.read(name)) == digest, name

    sections = re.split(rb"(?=^diff --git )", z.read(DIFF), flags=re.M)
    sections = [s for s in sections if s]
    assert len(sections) == 5
    restored, repaired = {}, {}
    for section in sections:
        lines = section.splitlines(keepends=True)
        header = re.fullmatch(rb"diff --git a/(.+) b/(.+)\n", lines[0])
        assert header and header[1] == header[2]
        name = header[1].decode()
        assert name in FILES and name not in restored
        current = z.read(name)
        source = current.splitlines(keepends=True)
        result, cursor, i = [], 0, 1
        while i < len(lines):
            if not lines[i].startswith(b"@@ "):
                i += 1
                continue
            h = re.match(rb"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", lines[i])
            assert h
            old_at, old_n = int(h[1]) - 1, int(h[2] or b"1")
            new_at, new_n = int(h[3]) - 1, int(h[4] or b"1")
            old, new = [], []
            i += 1
            while i < len(lines) and not lines[i].startswith(b"@@ "):
                prefix, data = lines[i][:1], lines[i][1:]
                assert prefix in (b" ", b"+", b"-"), (name, lines[i])
                if prefix in (b" ", b"-"):
                    old.append(data)
                if prefix in (b" ", b"+"):
                    new.append(data)
                i += 1
            assert len(old) == old_n and len(new) == new_n
            assert new_at >= cursor
            assert source[new_at:new_at + new_n] == new, name
            result.extend(source[cursor:new_at])
            assert len(result) == old_at
            result.extend(old)
            cursor = new_at + new_n
        result.extend(source[cursor:])
        prior = b"".join(result)
        assert sha(prior) == FILES[name], name
        repaired[name], restored[name] = current, prior
        (out / Path(name).name).write_bytes(prior)

    assert set(restored) == set(FILES)
    rows = []
    # Only now compare reconstructed sources with the packet's before/ copies.
    for name, expected in FILES.items():
        prior = restored[name]
        before = z.read("packet_only/before/" + Path(name).name)
        assert prior == before
        assert sha(prior) == sha(before) == expected
        rows.append({
            "file": name,
            "repaired_sha256": sha(repaired[name]),
            "reconstructed_sha256": sha(prior),
            "before_sha256": sha(before),
            "byte_equal": prior == before,
        })
result = {"archive_sha256": EXPECTED_ARCHIVE, "reconstructions": rows}
(out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
~~~

## Appendix B — Evidence identities

These hashes bind the independently generated review evidence. The substantive results and the inverse-reconstruction program are included above; this appendix does not substitute hashes for an explanation of what was executed.

| Evidence | SHA-256 |
|---|---|
| Explicit inverse-edit program | `5cb13e96b9da6bd28ee80147e35081cf9bf60deef3137d9fc63e2ede3c2507f9` |
| Explicit inverse-edit results | `aab9decde3e864ab950046b8eb7eeb0871b3c536d4fb5df9fefde4677eee2e5e` |
| Appendix A reconstruction program | `8cb5e4134442f71f301c414588db9a70c9537489469fde7ea059044e36125397` |
| Independent diff-reversal results | `a16afe66090a54ef772f41c8a912411b92f85558777243b32219f1475e2075d8` |
| M3/M4 and downstream-pin test transcript | `db65e5c1eb585090d5c7f598df76fb86ac31e0b0c49226908e952483ba59d534` |
| Focused precedence-state program | `1e64f8b7de10e860abf1eb1d661f75a7e90f0fe099306cc315a01a700d5426b4` |
| Focused precedence-state results | `f18c0699d4ab0016c4c0424439b9347a7f05f6483a5db53a093124e37f475b04` |
| Exact new-test before/after program | `578ff7f46507304f9ac6e8d28668c122598c4ea52ca20e2ed803e1d2e03bde04` |
| Exact new-test before/after results | `a6f747961436433299f5abe1e719923bd1ab6aec2de13ef2716f1575e334d2c7` |
| Downstream/validation semantic probe | `396532fa3e295faa75a1ec532276c97e3337689e3f415aa987c8c02b182b7d2d` |
| Downstream/validation results | `20b43be7fad56fbe340ea4cfd36b0ea528e9e537be1785294cf6b2190d48d6ae` |
| Post-review source-preservation result | `685e355bf46a70325f6c5ed87c7fcfab0aebae3efb624788fcb4314056ca27ca` |

FINAL VERDICT: SOUND