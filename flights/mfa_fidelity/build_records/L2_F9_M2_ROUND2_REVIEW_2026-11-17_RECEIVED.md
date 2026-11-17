| Receipt check | Computed value | Result |
|---|---|---|
| Archive SHA-256 | `2d162cd2f893fdb58dc531087c11c4fa031b96307dabcd4bccddb1cf236eb030` | MATCH — user-supplied digest |
| Payload files | 74 | MATCH — declared count and manifest |
| Total files | 75 (74 payload files + `MANIFEST.txt`) | MATCH |
| `MANIFEST.txt` SHA-256 | `88c0c8cd8898d26eb839372404724ac94ca69077120dee5e8508b5e5fd96d512` | Computed; not self-listed |
| Payload digest verification | 74 / 74 | MATCH |
| Missing / unlisted payload files | 0 / 0 | PASS |
| Duplicate archive / manifest paths | 0 / 0 | PASS |
| Unsafe archive paths | 0 | PASS |
| ZIP CRC verification | All 75 files | PASS |
| Receipt / review sequence | Receipt completed first; review began after Mike’s “execute” | Authorized sequence observed |

| # | Payload file | Computed SHA-256 | Against `MANIFEST.txt` |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M2_ROUND2_RESPONSE_2026-11-17.md` | `c474d189864d77fa5f9d31530ed41674173e3509ac6134d99fd398bbe2acffa7` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` | MATCH |
| 4 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` | MATCH |
| 5 | `flights/mfa_fidelity/build_records/L2_F9_M2_ROUND1_REVIEW_2026-11-17_RECEIVED.md` | `7ba22c09dc86efe94d40148dc965f94256e748e259dacb3061e1dd86d43c7e5a` | MATCH |
| 6 | `flights/mfa_fidelity/build_records/f9_m2_module_container_round2_2026-11-17.txt` | `f31028d625f07720e3412d32a7880f14f528414fae8d869906acc766d1d5ec16` | MATCH |
| 7 | `flights/mfa_fidelity/build_records/l2_m2_round1_reproduce.py` | `27f4a324158f1a1e0cfdcda7066c44b2fef949a2d6f9582e74394003731be8c7` | MATCH |
| 8 | `flights/mfa_fidelity/build_records/l2_m2_round1_check_windows.py` | `da087bbc2a394a72df3e33539b2dc731a885ecaf3337da04624c9f83591bbf53` | MATCH |
| 9 | `flights/mfa_fidelity/build_records/f9_m2_l2_round1_reproduce_on_round1_2026-11-17.txt` | `2c8f7a5600c8d20c9e5ea92d4293ecb54169397ff80d8473546f0bca46ca6866` | MATCH |
| 10 | `flights/mfa_fidelity/build_records/f9_m2_l2_round1_check_windows_on_round2_2026-11-17.txt` | `e268019f83c4543761e9bad90bbba350848f5dfbc46bf16b22ed23e02605df3f` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/l1_m2_round1_witnesses_adapted.py` | `81182fc3a94861bd29b607e5f3b2cd205f2a3029dbd5b2751855dadbf86f9912` | MATCH |
| 12 | `flights/mfa_fidelity/build_records/f9_m2_l1_adapted_witnesses_on_round1_2026-11-17.txt` | `97836619dfc4abf4ab82f550d4dc5d37f3472259acbf1231b4c74165a3751228` | MATCH |
| 13 | `flights/mfa_fidelity/build_records/f9_m2_l1_adapted_witnesses_on_round2_2026-11-17.txt` | `b90d7c9cb3ef740615be3e748b0aaec93c4bcb335dc055c14df415e2c7e1a900` | MATCH |
| 14 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M2_BUILD_PACKET_2026-11-17.md` | `18db1d6ee9e02a0a7c4a0309f7d28999ecbffe988d9d644b34f093e5a03acdfa` | MATCH |
| 15 | `flights/mfa_fidelity/build_records/f9_m2_module_container_2026-11-17.txt` | `06c550e80d52fb2bbaecdcd409076feb8451e88c73519514d7e58f78072d3cef` | MATCH |
| 16 | `packet_only/round1/streams.py` | `1d1bbc48abe1df54fed25c072402d64ced71a2b3b85a44cf818fb783b90afaec` | MATCH |
| 17 | `packet_only/round1/dynamics.py` | `11ad2ef15ef30520018ee15501cd43d5f7bd126c4e268e398c85ed7ad9cafed3` | MATCH |
| 18 | `packet_only/round1/test_f9_m2.py` | `c8c3e1f9a01b2193a9e4a5fe9dc10afb9220e35bcb8d5a7018e5042c7fb9c59c` | MATCH |
| 19 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 20 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 21 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 22 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 23 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 24 | `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | `473a2a165fd5cb4e38ddb064dc14c24880af8998a21b9ffad1aa7c065551016c` | MATCH |
| 25 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |
| 26 | `flights/mfa_fidelity/build_records/F9_M1_PLACEMENT_NOTE_2026-11-17.md` | `2a7955690815cc4cef6b8bbc7d83acfbade50acfff4f8afc6a737487b455c2a2` | MATCH |
| 27 | `flights/mfa_fidelity/build_records/L2_F9_M1_ROUND3_REVIEW_2026-11-16_RECEIVED.md` | `e90e59bc411c67aed5a3fdb8aec8045d4d9c7ef47128fff35fc7dacdb448d0e2` | MATCH |
| 28 | `flights/mfa_fidelity/build_records/f9_m1_module_canonical_2026-11-17.txt` | `24898dd0e7a6deab6705de2763efeed5b6f28e50eaa299780a28d64e3b26e96c` | MATCH |
| 29 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 30 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 31 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 32 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 33 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 72 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 73 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 74 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 M2 build review, round 2

**Date:** 2026-11-17. **Reviewer:** L2. **Decision authority:** Mike.  
**Register:** module build review, after receipt verification and Mike's “execute”.  
**Instruction:** `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M2_ROUND2_RESPONSE_2026-11-17.md`.  
**Declared repository pin:** `ee-theory-lab` `main` at `7af50941e47249965dc6c8b2a502d06166e08866`.  
**Reviewed object:** the received round-2 archive and the exact source identities in the receipt above. The remote repository pin was not independently queried.

## 1. Disposition and limits

**The round-1 repairs are closed, with the scope notes below. M2-3, M2-7 and M2-8 are acceptable as now declared. No additional placement-blocking source repair was established.** The supplied M2 suite passes all 63 tests. The five original parser witnesses are now refused, the original unaltered control still parses and replays, and all 21 declared historical masters are independently grounded and excluded. [R2 §§1–3; R1 §§2–3; D; S; T; E1–E4 below]

**Q3 has a positive finding that must not be lost in that clearance:** an internally impossible record can still pass `parse_run`. Appendix A reproduces two such records on these exact bytes. Neither violates a relation that revised M2-8 promises to check. The revised declaration enumerates necessary conditions and explicitly disclaims sufficiency; the prior review likewise did not require complete trajectory-feasibility validation. Accordingly, these are documented limits of the accepted parser, not newly imposed placement gates. A parser pass does not establish that all stored summaries arise from any common binary history, still less the specified seeded run. [R2 §1, M2-8 and Q3; R1 §2, “Required repair and closure evidence”; D, “WHAT VALIDATES A RECORD” and `_check_consistency`; Appendix A]

This clearance concerns the module build and its bounded declarations. It is not a production-record authentication certificate, stage authorization, master-draw decision, qualification result or scientific determination. Tests used test masters and deterministic apparatus inputs. The additional Q3 constructions used no dynamics or random draws. No canonical job, new stage master, occupancy-to-contour comparison or boundary adjudication was performed. Packet source bytes were preserved. [R2 register and §4; C §§5.9, 8; E1–E5]

### Evidence and source notation

Paths are relative to the extracted packet root. Packet identities are given in full in the receipt. Bracketed keys cite those sources or the execution evidence identified in §7.

| Key | Source |
|---|---|
| C | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md`, with `FLIGHT_9_FREEZE_RECORD.md` and `FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` in that directory |
| R2 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M2_ROUND2_RESPONSE_2026-11-17.md` |
| R1 | `flights/mfa_fidelity/build_records/L2_F9_M2_ROUND1_REVIEW_2026-11-17_RECEIVED.md` |
| P1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M2_BUILD_PACKET_2026-11-17.md` |
| D | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` |
| S | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` |
| T | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` |
| I / CFG | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` and `config.py` |
| W | `flights/mfa_fidelity/build_records/l1_m2_round1_witnesses_adapted.py` and the two supplied `f9_m2_l1_adapted_witnesses_on_round1/round2_2026-11-17.txt` outputs |
| E1–E5 | Independent executions and source comparisons described in §7; E5 is reproduced completely in Appendix A |

The frozen contract's retained DRAFT/PROPOSED markers are read through the freeze record; they do not reopen its ratified rules or values. [C, freeze record §§1, 3]

## 2. Q1 — closure of R1, R2 and the M2-7 wording

| Item | Disposition | Findings |
|---|---|---|
| R1a — W=1 endpoint cardinalities | **CLOSED** | The first and last masks are checked against the first and last tail counts. The original first-endpoint and last-endpoint alterations are refused for the intended reason. |
| R1b — all nested widths and endpoint implications | **CLOSED** | The loop checks (1,10), (1,100) and (10,100), enforcing both active-window bounds and finer-to-coarser endpoint implications. The original 63-versus-3 witness is refused. |
| R1c — nested JSON integer types | **CLOSED** | `_int_list_is` requires a list of the declared length with exact integer elements. Boolean and floating substitutions are rejected even when Python value equality would regard them as equal. |
| R1 negative/control evidence and overall closure | **CLOSED WITH NOTE** | The supplied negatives discriminate the repaired checks; the accepted control and replay-only forgery remain. Closure is of the required checks, not a claim of complete logical consistency or trajectory feasibility. See Q3. |
| R2 — historical masters | **CLOSED WITH NOTE** | All 21 historical declarations are grounded and rejected through eight public paths. The note preserves the remaining runner and governance responsibilities; it does not require another permission round for this review. |
| M2-7 — libm wording | **CLOSED** | The source and response now accurately distinguish omitted machine-local η₀/q values from serialized spectral/gain metadata derived from the identity record's q. |

[D, `_int_list_is`, `parse_run`, `_check_consistency`; S, `RETIRED_MASTERS`; T, new round-1-repair tests; E1–E4]

### The original witnesses reverse as required

The supplied L2 programs exactly match the corresponding Python blocks in the received round-1 review. The original reproducer was executed against an isolated round-1 source view reconstructed from the three exact `packet_only/round1/` copies. The adapted reproducer was then executed against both source views. Its outputs match the packet's supplied evidence byte for byte. [R1 Appendices A–B; R2 §3; E2]

| Witness | Round-1 source view | Submitted round-2 source |
|---|---|---|
| Unaltered T0/P test record | Parses; replay True | Parses; replay True |
| First W=1 endpoint total 3,199 while count at tick 2001 is 3,200 | Parses | Refused: first-window mask versus tick counts |
| Last W=1 endpoint total 3,159 while count at tick 3000 is 3,160 | Parses | Refused: last-window mask versus tick counts |
| Cell (0,0): A₁=285, A₁₀=63, A₁₀₀=3 | Parses | Refused: W=10 and W=100 not nested |
| Floating-point `stream_key` elements | Parses | Refused: stream key does not follow from run identity |
| Boolean first element of `windows` | Parses | Refused: declared windows do not match |
| Masters 202609221, 202609222, 202609223 | Accepted as masters | Refused as retired |

[E2; W]

The current tests also exercise the newly added segment-order relation, a coarse endpoint alteration, exact-type/length cases, non-finite JSON tokens and eight synthetic tail families. Those are useful additional checks. Passing them is evidence for their stated conditions and does not make the collection complete. [T, `test_impossible_summaries_are_refused_by_the_parser_l2_m2_round1_r1`, `test_undeclared_json_types_are_refused_l2_m2_round1_r1c`, `test_consistency_relations_hold_on_arbitrary_tails`; E1]

## 3. Q2 — the three revised declarations

| Declaration | Disposition | Accepted meaning and limits |
|---|---|---|
| **M2-3 — masters** | **ACCEPTABLE** | A caller supplies the master; the allowed integer domain and test/stage classification remain. The 21 listed historical masters are excluded. This static list establishes historical exclusion, not fresh-stage authorization or uniqueness across later Flight 9 stages. |
| **M2-7 — serialization** | **ACCEPTABLE** | The existing magic, header-length prefix, canonical JSON and fixed array encoding remain. η₀ and q are represented by the stated rule/probability and μ; spr, g_spec and g are present as described. Encoding stability is distinct from identity stability: the changed stream-declaration digest changes serialized header bytes. |
| **M2-8 — validation** | **ACCEPTABLE as expressly bounded** | Parsing checks form, declarations, array hashes and the enumerated necessary relations. Same-machine replay tests exact reproduction under a supplied context. Canonical-context and job provenance authentication belong to the runner. Parser acceptance alone establishes neither a common binary history nor the seeded trajectory. |

[R2 §1; D docstring, `run_header`, `parse_run`, `replay_equals`; S; I; C §§2.10, 5.9, 8]

The unchanged declarations and functions are not silently redefined by this review. The round-1 acceptance of the rule, starts, stream identity, record accumulation and reduction remains within its original scope; the changed-source comparison supports that continuity. [R1 §§4–7; R2 §2; E4]

## 4. Q3 — are the new relations necessary, and can an impossible record still parse?

### 4.1 No false listed relation was identified

Let a cell's binary window sequence be z₀,…,zₙ₋₁; let A count active windows, R₀ inactive segments and Rₐ active segments. Let cₜ count active cells at tail tick t. The following arguments establish necessity for arbitrary binary histories, including the histories the frozen rule can produce. They do not assert that the conjunction is sufficient. [C §2.11; D, `_check_consistency`]

| Implemented relation | Why it is necessary |
|---|---|
| Sum of W=1 A equals sum of tail counts | These are the same sum of cell-by-tick activity indicators taken in opposite orders. |
| Rₐ = R₀ − 1 + first + last | Active and inactive segments alternate; the endpoints determine which segment type has one extra member. |
| R₀ ≤ n−A and Rₐ ≤ A, with the zero-segment equivalences | Every segment contains at least one window of its own state. A sequence has no inactive segment exactly when all windows are active, and conversely for active segments. |
| For each time block, maximum tick count ≤ active-mask cardinality ≤ sum of tick counts | The window mask is the union of the cells active at its constituent ticks. The union contains each constituent set and cannot contain more elements than their summed sizes. |
| W=1 endpoint equalities | A one-tick endpoint window is exactly that tick's state. |
| A₁ ≤ number of tail ticks with cₜ>0 | No cell can be active at a tick when the global count is zero. |
| Ever-active cells ≥ max cₜ; always-active cells ≤ min cₜ | The union contains each tick's active set; the intersection is contained in each one. |
| A_large ≤ A_small ≤ k·A_large for a coarse block of k fine blocks | An active coarse block contains between one and k active fine blocks. |
| R₀,large ≤ R₀,small | Distinct inactive coarse runs contain fine inactive runs separated by a coarse active block, which contains a fine active block. They therefore correspond to distinct fine inactive runs. |
| Rₐ,large ≤ Rₐ,small | Distinct active coarse runs contain fine active runs separated by a wholly inactive coarse block. |
| Fine endpoint active implies coarse endpoint active | The fine endpoint block is contained in the corresponding coarse endpoint block. |

The count-domain, skeleton absorption/start, tick/draw accounting, survival and tail-sum checks also agree with the declared run mechanics. The code performs these comparisons after decoding count arrays to int64 and endpoint masks to booleans and enforcing header types. No false rejection was found in this mathematical audit or the executed controls. This is not an exhaustive enumeration of all seeded dynamic runs. [D, `run` and `_check_consistency`; C §§2.5–2.11; E1–E3]

### 4.2 Yes: two internally impossible records still parse

Appendix A constructs a skeleton history in which all N=10,000 cells are active through tick 2500 and all are inactive from tick 2501 onward. The recording tail is ticks 2001–3000. The count vector therefore forces every cell's tail: 500 active ticks followed by 500 inactive ticks. The control has, per cell:

| W | A | R₀ | First | Last |
|---:|---:|---:|---|---|
| 1 | 500 | 1 | True | False |
| 10 | 50 | 1 | True | False |
| 100 | 5 | 1 | True | False |

The control's extinction tick, advanced ticks, draws and survival flag agree with that construction, and the control parses. It is an internally consistent constructed history, not a claim that test master 7 selects it. A local M1 test bundle supplies the arm context; no dynamic run or random draw is used to construct the examples. [Appendix A; E5]

**Q3-A — coarse activity outside the support of the counts.** Starting from the control, change only `A_W100[0,0]` from 5 to 6 and serialize with the submitted serializer. The resulting canonical, correctly hashed record parses. Only five 100-tick blocks have any positive count anywhere, so no cell can be active in six such blocks. The altered total A₁₀₀ is 50,001, whereas the maximum possible total is 50,000. [Appendix A; E5]

**Q3-B — inactive segments contradict states forced by the counts.** Starting again from the control, change only `R0_W1[0,0]` from 1 to 2 and serialize. That record also parses. Counts of either N or zero fix every cell's state; every cell has exactly one inactive segment in this tail. The altered total R₀ is 10,001, whereas the counts permit at most 10,000. [Appendix A; E5]

Both mutations satisfy all currently enumerated checks. Q3-A exploits a bound that is present only for W=1 and a loose aggregate upper bound. Q3-B exploits untested information in the ordering of global counts. The witnesses demonstrate logical impossibility without reconstructing a seeded trajectory. They do not demonstrate an error in `run`, `_Windows`, a listed inequality, or seeded replay. No replay result is claimed for these constructed examples. [D, `_check_consistency`; Appendix A]

### 4.3 Why these findings do not reopen the repaired R1 gate

Round-1 R1 required four specified actions: endpoint cardinality checks; all nested-width and endpoint relations; exact nested integer types; and discriminating negative/control evidence. It expressly did not require solving every trajectory-feasibility constraint. Those repairs are present. Revised M2-8 now names the checks listed in `_check_consistency` and states they are necessary, not sufficient. Neither Q3 witness falsifies that promise. [R1 §2; R2 §1; D docstring]

Q3 requests an adversarial answer about what can still pass. The answer is **yes**, with the limits exhibited above. That request does not itself turn an explicitly bounded necessary-condition parser into a complete feasibility certifier. Making every newly discovered necessary inequality a further placement condition would expand the review obligation after the stated repairs were met. This review does not do that. [L2 scope determination from R1, R2 and C §5.1]

The operative interpretation of “consistency” in this clearance is therefore **satisfaction of the enumerated necessary relations**. It must not be cited as a proof that the retained quantities admit a common history. The module's existing separation of parsing, replay and authentication remains essential; downstream acceptance must preserve it. A future promise that parsing proves full realizability would need a different implementation and review. [D, “WHAT VALIDATES A RECORD”; R1 §7; C §5.9]

### 4.4 Optional bounded improvements, not conditions of this clearance

If L1 later elects to strengthen the parser, these direct bounds would catch the demonstrated cases. For width W, write bⱼ for the sum of tick counts in block j. Then every cell obeys A_W ≤ number of blocks with bⱼ>0, and the aggregate obeys:

\[
\sum_i A_{W,i}\leq\sum_j\min(N,b_j).
\]

For W=1, writing c₀ for the first tail count, each later inactive segment begins with an active-to-inactive transition. Thus:

\[
\sum_i R_{0,i}\leq N-c_0+\sum_{t=1}^{999}\min(c_{t-1},N-c_t).
\]

These bounds follow respectively from unions within blocks and the maximum number of active-to-inactive transitions allowed by two consecutive counts. They remain necessary conditions, not a complete characterization. They are recommendations for an explicitly declared future change; they are not required repairs on these bytes. [L2 derivation from C §2.11; E5]

## 5. Q4 — retired-master inventory and grounding

**No master in the declared historical scope is missing, and no listed entry is ungrounded.** Independent inspection used named assignments and the actual Flight 8 date/prefix construction, rather than treating membership in the list under test as evidence. The resulting set contains exactly 21 distinct integers and equals `RETIRED_MASTERS`. [S; sources below; E3]

| Source under `flights/mfa_fidelity/instrument/mfa_instrument/` unless stated | Grounding | Values |
|---|---|---|
| `e1/config.py` | `E1_SEED_PANEL_MASTER` | 20260917 |
| `e1/null.py` | `NULL_TEMPLATE_MASTER`; `VALIDATION_REPLICATE_MASTER` | 202609171, 202609172 |
| `e1/audit.py` | `AUDIT_MASTER`; `HELD_OUT_MASTER`; `PRICING_MASTER` | 202609221, 202609222, 202609223 |
| `e1/projection.py` | Projection, tolerance, stability and bootstrap master declarations | 202609301, 202609302, 202609303, 202609304 |
| `f8/config.py` | Canonical, calibration and stability declarations | 20261026, 120261026, 920261102 |
| `f8/null.py` | Validation attempt 1 and `VALIDATION_PROTOCOL_ATTEMPT_2.replicate_master` | 220261026, 320261027 |
| `f8/closure.py` | `PROJECTION_MASTER` | 420261028 |
| `f8/evaluator.py` | `KNOWN_ANSWER_MASTER` | 520261028 |
| `f8/audit.py` | Placement date 20261102, prefixes 6/7/8, `masters_for_date` | 620261102, 720261102, 820261102 |
| `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `PROBE_MASTER` | 9920261112 |

Derived seed-panel members, apparatus role keys and arbitrary test seeds are not additional historical master declarations under M2-3's stated scope. No broader claim about unseen repository history is made. [S docstring; E3]

The stream declaration's independently recomputed SHA-256 is:

`3274f728c79b6d44b3b2b0b685a4d7526ab0f4cd16f1d5e0e1bc72407e231832`

It equals both the literal and `verify_stream_declaration()`'s result. There were **168 successful refusals**: each of 21 values through `check_master`, `master_class`, `check_run_identity`, `stream_key`, `F9RunSpec.check`, `F9RunSpec.stream_key`, `generator_from_key` and `init_pattern_generator`. The generator paths refuse before constructing a generator. Six accepted identity/key controls were 7, 999999, 1000000, 202609224, 9920261113 and 18446744073709551615, with the expected test/stage classification. No stage draw was made. [S; T, `test_every_earlier_master_is_refused_l2_m2_round1_r2`; E3]

The new test's external inventory is materially stronger than iterating the implementation list. Its AST literal-presence check alone would not prove a literal's semantic role, but independent source inspection establishes those roles in the submitted bytes. That limitation of the test technique does not leave a defect in this inventory. [T; E3]

L1 disclosed that Mike said “continue” after the recommendation to exclude the full inventory; the response does not claim a separate explicit selection that did not occur. The wider exclusion is technically acceptable and consistent with fresh masters. This review supplies technical acceptance, while the eventual master-draw procedure, authorization binding, test-master refusal in production and stage-to-stage uniqueness remain the runner's obligations under Mike's authority. No new permission gate is introduced here. [R2 §§1, 4; R1 §§3, 7; C §§2.10, 8]

## 6. Q5 — remaining corrections and placement scope

### 6.1 No additional blocking source repair; one wording correction

R2 §2 says, “no byte of a serialized record changed.” That sentence is inaccurate if read as record identity. `run_header` includes `stream_declaration_sha256`; expanding the retired-master declaration changes that field from the round-1 digest to the round-2 digest. The complete serialized header and record digest therefore change for the same otherwise accepted run. Round-1 records remain bound to their old declaration and are refused by the round-2 declaration-equality check. [R2 §2; D, `run_header` and `parse_run`; S]

The accurate formulation is: **the serialization schema, array encoding and record layout are unchanged; the stream-declaration identity in the header changes.** `RUN_SCHEMA = 1` need not change for this, because the declared identity already distinguishes the versions. This is a nonblocking correction to the response's description, not a request to alter the submitted encoding or rewrite previously issued evidence. [D; E4]

Similarly, any later description of parser “consistency” should retain the explicit qualification in §4.3. The source's detailed necessary/not-sufficient declaration is the accepted guarantee. [D; R2 M2-8]

### 6.2 Changed-source verification

The three changed source/test files have exactly the received round-2 identities. Their differences from the included round-1 copies agree with the response's functional scope:

| File | Independently observed change |
|---|---|
| `f9/streams.py` | Historical-scope text and retired-master tuple; declaration digest; preflight cardinality/domain check. `verify_stream_declaration` is the only changed function. |
| `f9/dynamics.py` | Serialization/validation documentation; changed `parse_run`; new `_int_list_is`; rewritten `_check_consistency`. |
| `tests/test_f9_m2.py` | Four new test functions and their helpers/imports; the older master-refusal test stops deriving expectations by iterating the implementation list. |

[E4; R2 §2]

The advertised unchanged definitions—`step`, `local_density`, `activation_probability`, `arm_context`, `F9RunSpec`, `initial_state`, `_Windows`, `run`, `run_header`, `serialize_run`, `replay_equals` and `reduction_check`—are byte-identical between the source views. No definition was removed, and `RUN_SCHEMA` remains 1. The supplied unchanged-source assertions pass. This establishes packet-local continuity; it is not an independent remote-repository attestation. [E1, E4]

### 6.3 Obligations carried forward without expansion

The round-1 runner obligations remain: Mike's master-draw procedure before the runner is built; uniqueness across stages and refusal of test masters for jobs of record; binding the complete serialized payload to the authorized bundle, source and applicable evaluator/qualification identities; and persistence of raw λ and local mᵢ under §2.8 at the appropriate arm and arm/level scope. These were already carried in R2 §4. They are not newly assigned to each M2 payload and are not reopened repairs to M1. [R1 §7; R2 §4; C §§2.8, 5.9, 8]

## 7. Execution evidence and limits

| Evidence | Independently observed result | Scope |
|---|---|---|
| Receipt | Archive digest matches; 74/74 payload hashes match; 75 files total; exact manifest membership; CRC passes | Input identity |
| **E1 — M2 suite** | **63 passed in 39.27 s**, exit 0 | Submitted `tests/test_f9_m2.py`, including five run fixtures, replay, reduction, changed negatives, synthetic-tail checks and unchanged-source assertions |
| **E1 — M1 regression** | **102 passed in 580.62 s**, exit 0 | Submitted `tests/test_f9_m1.py`; container result, not canonical-machine evidence |
| **E2 — original round-1 reproducer** | Exit 0; output byte-identical to supplied round-1 evidence | Isolated source view using the packet's exact round-1 copies |
| **E2 — adapted witnesses** | Both rounds exit 0; both outputs byte-identical to supplied evidence | Original constructions before/after repair; accepted control retained |
| **E2 — window accumulator** | All **9,216** enumerated histories pass; output byte-identical to supplied evidence | 4,096 at W=1, 4,096 at W=10, 1,024 at W=100; deterministic mechanics |
| **E3 — historical-master inventory** | 21/21 grounded; no missing or ungrounded value; 168/168 public-path refusals; six accepted controls | No stage draws; declaration digest independently recomputed |
| **E4 — changed-source comparison** | Disclosed functional scope confirmed; 12 named dynamics definitions unchanged; original L2 programs match received code blocks | Exact packet-local source comparison |
| **E5 — Q3 constructions** | Control and both impossible altered records parse | Deterministic construction; full program and observed output in Appendix A |

The supplied-suite environment was Linux, Python **3.12.14**, NumPy **2.3.5**, SciPy **1.17.0**, and pytest **9.2.0**. The suites used the primary Python runtime with the existing pytest dependency directory on a process-scoped import path; plugin autoload was disabled and no packages or submitted sources were changed. Both supplied suites completed without failures, skips or reported warnings. These are L2 container results, not L1's supplied timings or evidence from the canonical machine. No full legacy canonical suite was rerun. [E1–E4]

With pytest available, the two supplied-suite commands from `flights/mfa_fidelity/instrument` are:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p no:cacheprovider tests/test_f9_m2.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p no:cacheprovider tests/test_f9_m1.py
```

For the supplied programs, pass the extracted packet root as their argument. The original round-1 reproducer deliberately guards round-1 source hashes, so it belongs on the isolated round-1 view; the adapted witness program and window checker can be used on the round-2 packet. These guard differences were respected. [R2 §3; E2]

### Execution evidence identities

These are identities of the L2 execution records used above. The substantive results are reported in this file; the complete new Q3 construction and output are included in Appendix A.

| Evidence | SHA-256 |
|---|---|
| E1 — M2 suite | `966179221d57610db80c8e03580a47078e207d206b3dca3f0b34dbb51154d83b` |
| E1 — M1 regression | `9ed22db9fd7723d9b1bd6c7b79acfd362d1da9f06e013f790246d8ad6572aaa2` |
| E2 — original round-1 reproducer | `2c8f7a5600c8d20c9e5ea92d4293ecb54169397ff80d8473546f0bca46ca6866` |
| E2 — adapted round-1 witnesses | `97836619dfc4abf4ab82f550d4dc5d37f3472259acbf1231b4c74165a3751228` |
| E2 — adapted round-2 witnesses | `b90d7c9cb3ef740615be3e748b0aaec93c4bcb335dc055c14df415e2c7e1a900` |
| E2 — round-2 accumulator check | `e268019f83c4543761e9bad90bbba350848f5dfbc46bf16b22ed23e02605df3f` |
| E3 — independent inventory record | `1eefd24bb1fcf50ad797082ffad574fe17ef698698dd0f9ee5b45f00c640ce32` |
| E4 — source-difference record | `5f03eff46f5451bb631fe1fff4029e8453fc72973cf6a0e3b7918e9afa19f3d6` |

## Appendix A — reproducible Q3 limitations on the exact round-2 bytes

Save the following Python block as `q3_witness.py` and run:

```bash
python q3_witness.py /path/to/extracted_round2_packet
```

It checks the submitted dynamics and streams identities, creates and removes a local M1 test bundle, and uses the submitted serializer and parser. It constructs an internally consistent control and two altered summaries. It neither runs the dynamics nor draws a master. The reproduced program's SHA-256 is `d9ec51fcc1ee5154222cbd0114df4152ffc4a2e470d562eb4d7577adcf7a941d`. [E5]

```python
"""Deterministic F9 M2 round-2 stored-quantity witnesses; no dynamics or RNG.

Usage: python q3_witness.py /path/to/extracted_packet
The control is a constructed, internally consistent skeleton history, not a
claim about the trajectory selected by test master 7.
"""
from dataclasses import replace
from itertools import groupby
from pathlib import Path
import hashlib
import json
import sys
import tempfile

import numpy as np

packet = Path(sys.argv[1]).resolve()
instrument = packet / "flights/mfa_fidelity/instrument"
sys.path.insert(0, str(instrument))
from mfa_instrument.f9 import config as C, dynamics as D, identities as I

expected = {
    "mfa_instrument/f9/dynamics.py": "34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e",
    "mfa_instrument/f9/streams.py": "5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06",
}
for rel, digest in expected.items():
    assert hashlib.sha256((instrument / rel).read_bytes()).hexdigest() == digest, rel

with tempfile.TemporaryDirectory(prefix="bundle_", dir=Path(__file__).parent) as temp:
    I.write_bundle(temp)
    identity, arrays = I.load_bundle(temp)
    arm = D.arm_context(identity, arrays, "T0", "P")

N, T, tail, L = C.F9_N_CELLS, C.F9_TICKS, C.F9_TAIL_TICKS, C.F9_GRID
assert (N, T, tail, L) == (10000, 3000, 1000, 100)
spec = D.F9RunSpec(7, "T0", "P", "skeleton", "all_active", 1500000, 0)
# All N cells are active through tick 2500 and inactive from tick 2501.
# Counts of 0 or N force every cell's state at every tick.
counts = np.full(T + 1, N, dtype=np.int64)
counts[2501:] = 0
states = counts[T - tail + 1:] != 0
windows = {}
for W in C.F9_FLICKER_WINDOWS:
    z = states.reshape(tail // W, W).any(axis=1)
    r0 = sum(1 for value, run in groupby(z) if not value)
    windows[W] = {
        "A": np.full((L, L), int(z.sum()), dtype=np.int64),
        "R0": np.full((L, L), r0, dtype=np.int64),
        "first": np.full((L, L), bool(z[0]), dtype=bool),
        "last": np.full((L, L), bool(z[-1]), dtype=bool),
    }
result = D.F9RunResult(spec, arm, 1.5 * arm.g_spec, counts, 2501, 2501, 2501, False, windows)

def emit(case, **facts):
    print(json.dumps({"case": case, **facts}, sort_keys=True), flush=True)

def altered():
    return {W: {name: data.copy() for name, data in fields.items()}
            for W, fields in windows.items()}

control = D.serialize_run(result)
D.parse_run(control)
emit("constructed_consistent_control", parse="ACCEPTED", extinction_tick=2501,
     counts_values=[0, N], A_per_cell=[500, 50, 5], R0_per_cell=[1, 1, 1])

# A cell cannot occupy six W=100 windows when only five windows have any
# active tick anywhere in the lattice.
w = altered()
w[100]["A"][0, 0] = 6
forged = D.serialize_run(replace(result, windows=w))
D.parse_run(forged)
positive_blocks = int((counts[T-tail+1:].reshape(10, 100).sum(axis=1) > 0).sum())
assert positive_blocks == 5 and int(w[100]["A"][0, 0]) == 6
emit("coarse_activity_outside_count_support", parse="ACCEPTED", W=100,
     cell=[0, 0], A=6, maximum_possible_A=positive_blocks,
     total_A=int(w[100]["A"].sum()),
     maximum_possible_total_A=int(np.minimum(N, counts[T-tail+1:].reshape(10, 100).sum(axis=1)).sum()))

# Counts 0 or N force one inactive segment per cell; increase one R0 only.
w = altered()
w[1]["R0"][0, 0] = 2
forged = D.serialize_run(replace(result, windows=w))
D.parse_run(forged)
tc = counts[T-tail+1:]
max_total_R0 = int(N-tc[0] + np.minimum(tc[:-1], N-tc[1:]).sum())
assert max_total_R0 == N and int(w[1]["R0"].sum()) == N+1
emit("inactive_segments_contradict_forced_states", parse="ACCEPTED", W=1,
     cell=[0, 0], R0=2, forced_R0=1,
     total_R0=int(w[1]["R0"].sum()), maximum_possible_total_R0=max_total_R0)
```

Observed output, exit status 0:

```json
{"A_per_cell": [500, 50, 5], "R0_per_cell": [1, 1, 1], "case": "constructed_consistent_control", "counts_values": [0, 10000], "extinction_tick": 2501, "parse": "ACCEPTED"}
{"A": 6, "W": 100, "case": "coarse_activity_outside_count_support", "cell": [0, 0], "maximum_possible_A": 5, "maximum_possible_total_A": 50000, "parse": "ACCEPTED", "total_A": 50001}
{"R0": 2, "W": 1, "case": "inactive_segments_contradict_forced_states", "cell": [0, 0], "forced_R0": 1, "maximum_possible_total_R0": 10000, "parse": "ACCEPTED", "total_R0": 10001}
```

The two accepted alterations are the nonblocking limitations adjudicated in §4. They must not be described as feasible histories or outputs of the specified seeded run.

FINAL VERDICT: SOUND
