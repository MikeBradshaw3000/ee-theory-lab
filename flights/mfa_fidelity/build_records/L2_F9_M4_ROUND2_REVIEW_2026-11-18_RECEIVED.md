| Receipt check | Result | Status |
|---|---|---|
| Archive | `f9_m4_build_round2_L2.zip` | RECEIVED |
| Archive SHA-256 | `74dac92809504ddd67200a2eb73e5400ac007e4023f0c5769c2715c537996721` | MATCH — supplied hash |
| File count | 75 payload files + `MANIFEST.txt` = 76 files | MATCH |
| Manifest entries / payload hashes | 75 valid entries; 75/75 full SHA-256 digests match | PASS |
| Missing, unlisted, duplicate, malformed or unsafe entries | None | PASS |
| ZIP integrity | All CRC checks passed | PASS |
| `MANIFEST.txt` SHA-256 | `367bb5e13f16a8808769f676b557eea1826b14902fd6d3ea9116f31e962f9a1d` | COMPUTED — no separate expected hash supplied |
| Receipt row 57 | `f9/spectral.py`; corrected and recomputed directly from the archive before review | MATCH |
| Review authorization | Receipt and row-57 correction returned; Mike then said “execute” | SATISFIED |

| # | Payload file | Computed SHA-256 | Against MANIFEST.txt |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M4_ROUND2_RESPONSE_2026-11-18.md` | `bb4b54255d51ea865482d1b892511f4725f799d4012433673fce944da03c8185` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` | MATCH |
| 4 | `flights/mfa_fidelity/build_records/L2_F9_M4_ROUND1_REVIEW_2026-11-18_RECEIVED.md` | `5b6eeab9cb6f65820232d2e3d95f73ba4fa152506219631564e2b8e153fc901d` | MATCH |
| 5 | `flights/mfa_fidelity/build_records/f9_m4_module_container_round2_2026-11-18.txt` | `e25e7367fee8f990b332528d47c8f97cefbd2500e953c29679dd4f39bbc21828` | MATCH |
| 6 | `flights/mfa_fidelity/build_records/l2_m4_round1_reproduce.py` | `4c9604689b746c2e02f10c65f0c923aa176bc7dc06de1ec67e065f6364e72c9e` | MATCH |
| 7 | `flights/mfa_fidelity/build_records/f9_m4_l2_round1_reproduce_on_round1_2026-11-18.txt` | `64f1692207e137cf6070b15047ae434e9fd0d05348d200778a3134ed4af60edf` | MATCH |
| 8 | `flights/mfa_fidelity/build_records/l1_m4_round2_d1_outcomes.py` | `d7dade5290c0bf24daeca5a3986cb06012431a862ae75e0e6f57775c83f9444d` | MATCH |
| 9 | `flights/mfa_fidelity/build_records/f9_m4_d1_outcomes_on_round1_2026-11-18.txt` | `30e2ed6171fa34a0895d91e7a56a50b03d734b239884fcee6cd91461223ea168` | MATCH |
| 10 | `flights/mfa_fidelity/build_records/f9_m4_d1_outcomes_on_round2_2026-11-18.txt` | `7252482d0f41e31fe4ceab7fe54e1463c7ec7ef1f9006ae316f80c5e289d4975` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/l1_m4_round2_fuzz.py` | `4ce07d6f2ce15c905ec4849aefdf7a46c82e2a72e8f2b623e9a58ddb06418368` | MATCH |
| 12 | `flights/mfa_fidelity/build_records/f9_m4_fuzz_round2_2026-11-18.txt` | `50580de78fba05416faa551eade3d2296219173ca040a6fd511aecd566d2b8a6` | MATCH |
| 13 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M4_BUILD_PACKET_2026-11-17.md` | `674d1acc269f0d0e64b23be50aa16485e479165bc284764dd39b1b44c01bd848` | MATCH |
| 14 | `flights/mfa_fidelity/build_records/f9_m4_module_container_2026-11-17.txt` | `e6fbe3c584a82b8d5c89374f96e1dcab1cbe6dfb9628b2a52342b5e71a906e68` | MATCH |
| 15 | `packet_only/round1/outcomes.py` | `6523da486b8bd9af02e3635e80e1f67434eb7cc8995caa3f8f6a5247bc7319c7` | MATCH |
| 16 | `packet_only/round1/test_f9_m4.py` | `c379c3a2756e7b58bda07177a039488babf7ba2510f51a4491fcd0fd08d0f345` | MATCH |
| 17 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 18 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 19 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 20 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 21 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 22 | `flights/mfa_fidelity/build_records/F9_M3_PLACEMENT_NOTE_2026-11-17.md` | `2df87fe689368752f92f5e5bd90f09ccef819255b2e5b44c4b1a6526314898f7` | MATCH |
| 23 | `flights/mfa_fidelity/build_records/L2_F9_M3_ROUND2_REVIEW_2026-11-17_RECEIVED.md` | `939dca526bdbcdbf52880e5c0b93ca988f0364d24af151f60e478cf8a219ccfe` | MATCH |
| 24 | `flights/mfa_fidelity/build_records/f9_m3_module_canonical_2026-11-17.txt` | `21c64723af05a3f767cd7f8fdb43fbd116a81efcb1b722f2d2478ab99b4c2010` | MATCH |
| 25 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 26 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` | MATCH |
| 27 | `flights/mfa_fidelity/instrument/tests/test_f9_m3.py` | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` | MATCH |
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
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 72 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 73 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 74 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 75 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 M4 build review, round 2

**Date:** 2026-11-18. **Role:** L2, adversarial instrument-build review. **Decision authority:** Mike.

**Archive reviewed:** `f9_m4_build_round2_L2.zip`, SHA-256 `74dac92809504ddd67200a2eb73e5400ac007e4023f0c5769c2715c537996721`.

**Packet-declared repository pin:** `80306ab3d7ce4cd9712ec8bd3604a27e725f9772`. This review binds the supplied archive bytes. Remote HEAD was not independently fetched.

## 1. Disposition

**D1 is CLOSED. M4-9 is ACCEPTABLE as repaired. No further blocking M4 defect was found.** The repaired arm validator recomputes the arm from its 25 retained level records and compares the entire supplied record with that result, recursively by value and type. The cause structures that escaped validation in round 1 are now included in that comparison. All six original counterexamples fail at both `_check_arm` and the public `flight_b` boundary, with `F9OutcomeError` in every case. [P2 §§1–2; O `_check_arm`, `_arm_tier`, `_same_typed`; D1 execution]

The **complete round-2 M4 test file passed: 21 passed, 1 warning in 60.24 seconds; exit code 0**. No test was deselected, skipped, or stopped early. In particular, the exhaustive Flight B test completed. Independent positive, mutation, copy-isolation, and round-to-round numerical checks also passed, as detailed below.

The arm decision rules are preserved. Carrying the level records supports the contract's requirement to retain lower-tier records and provides the information required for consistency validation. The Clopper–Pearson public interface now fixes the declared confidence level, and all 41 contracted count cases have exactly the same bounds as in round 1. [C §§1.3(a), 5.4, 5.6; O; source comparison]

This is technical clearance of the reviewed M4 build. Mike retains authority over declaration ratification and placement. No lattice flight, calibration, qualification, canonical scoring, master draw, or probe-array inspection was performed in this review. No packet source was edited.

### Receipt correction

The earlier chat receipt mistakenly repeated `f9/identities.py` at row 57. At Mike's request, entry 57 was recomputed directly from the archive and corrected before execution was authorized. It is `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py`, SHA-256 `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3`. The full receipt above is generated from the verified manifest records and includes that corrected entry exactly once among the payload rows.

### Source register

The following citations refer to packet members whose full digests appear in the receipt. Paths are relative to the archive root.

| Citation | Source |
|---|---|
| P2 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M4_ROUND2_RESPONSE_2026-11-18.md` |
| R1 | `flights/mfa_fidelity/build_records/L2_F9_M4_ROUND1_REVIEW_2026-11-18_RECEIVED.md` |
| O | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` |
| T | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` |
| O1 / T1 | `packet_only/round1/outcomes.py` and `packet_only/round1/test_f9_m4.py` |
| C | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md`, read with its freeze record and addendum in the same directory |
| D1 program | `flights/mfa_fidelity/build_records/l1_m4_round2_d1_outcomes.py` |
| L1 fuzz evidence | `flights/mfa_fidelity/build_records/l1_m4_round2_fuzz.py` and `f9_m4_fuzz_round2_2026-11-18.txt` in the same directory |

## 2. Identities, preserved evidence, and change boundary

| Reviewed object | SHA-256 |
|---|---|
| Round-2 M4 source | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` |
| Round-2 M4 tests | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` |
| Outcome declaration, recomputed | `c94ec4bd7c9aa532264ab2adc91ab6d4948ebff652b5b58380e1befb54a35407` |
| Frozen contract | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` |
| Received round-1 review, 36,236 bytes | `5b6eeab9cb6f65820232d2e3d95f73ba4fa152506219631564e2b8e153fc901d` |
| Included original L2 reproduction program | `4c9604689b746c2e02f10c65f0c923aa176bc7dc06de1ec67e065f6364e72c9e` |

The preserved round-1 source and test files are byte-identical to the actual round-1 packet copies. The received review is byte-identical to the review issued by L2. `l2_m4_round1_reproduce.py` matches both the Python code block in that review's Appendix A and the original local reproduction program. L1's statement that the program was extracted unchanged is confirmed.

The original reproduction correctly retains its round-1 source-hash guard. It is evidence for the round-1 bytes; it is not an appropriate unchanged executable acceptance test for round 2. L1's adapted outcome program retains the same six record mutations, prints the current source/declaration identities, and reports acceptance or rejection at both boundaries. That adaptation was inspected and executed against round 2. [P2 §§1, 4; D1 program]

An independent parsed-definition comparison agrees with P2's change inventory:

| Area | Confirmed change |
|---|---|
| Existing source functions | `_check_level`, `arm_tier`, `_check_arm`, and `clopper_pearson` changed |
| New source functions | `_arm_tier` and `_same_typed` added |
| Removed source definitions | None |
| Module documentation | Three lines added to describe retained levels and recomputation |
| Source assignments and declarations | Unchanged |
| Level, B, D, and persistence rules | `level_tier`, `level_apparatus`, `level_from_evaluation`, `flight_b`, `flight_d`, `_witnesses`, and `persistence_record` parse identically |
| Numerical internals | `_binom_tail_ge` and `_clopper_pearson` parse identically |
| Arm-rule body | The former `arm_tier` body matches `_arm_tier` after removing the new `levels` output field; declaration verification remains in the public wrapper |
| Test inventory | 20 becomes 21: the previous arm-record rejection test is replaced by a stronger rejection test and a new genuine-record acceptance test; the declared helpers, fixed mutation count, `_tb` extension, and two confidence-tail assertions account for the other changes |

The unchanged declaration digest is appropriate: the declared scientific values and rules remain the same. The new source digest separately identifies the changed representation and validation implementation. This review does not treat the declaration digest as an implementation hash. [P2 §§2–3; O `OUTCOME_DECLARATION`, `verify_outcome_declaration`]

## 3. Executed verification

### Complete module test file

From the extracted packet's `flights/mfa_fidelity/instrument` directory, the complete file was run in one process:

```bash
python -B -m pytest tests/test_f9_m4.py -vv -ra -p no:cacheprovider
```

The instrument and isolated pytest dependency directories were on `PYTHONPATH`. Environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pytest 9.2.0, pluggy 1.7.0. The sole warning was the installed AnyIO pytest plugin's `CallSpec2` deprecation, unrelated to M4's assertions.

```text
collecting ... collected 21 items
=================== 21 passed, 1 warning in 60.24s (0:01:00) ===================
EXIT_CODE 0
```

The completed file includes the 32,768 Flight B evaluations over all 4^7 seven-arm determination combinations with qualification both true and false; the 6,000 arm sweeps, 1,500 D sweep pairs, and 4,000 persistence sweeps; the new 17 genuine-arm controls; the 367 changed-record matrix checked at both boundaries; the numerical and unavailable-input tests; and the unchanged placed-file identity checks. [T]

### Additional L2 checks

| Check | Observed result |
|---|---|
| Original six D1 mutations on round 2 | 12/12 boundary calls refused; 0 accepted; every refusal `F9OutcomeError` |
| Independently constructed canonical level forms | All 17 forms accepted: nine separate-family result pairs, three equal-result same-family forms, four unavailable causes, and an apparatus record |
| Independent genuine-arm controls | 37 arms accepted at `_check_arm` and `flight_b` |
| Independent ordinary-value/type mutations | 592 altered records rejected at both boundaries: 1,184 typed refusals |
| Constructor/idempotence checks | 68 checks over the 17 level forms and four input-mapping patterns passed |
| Copy isolation | Input dictionary/cause-list mutations did not alter returned arms; shared input records were copied independently at each retained level |
| Retained-evidence mutation | A change to a retained level without the corresponding aggregate changes was refused |
| Additional A4 positive controls | Both two-cause combinations absent from the 17 named fixtures passed at both boundaries and returned NOT DISTINGUISHED |
| Confidence intervals across rounds | All 41 count cases, 82 floating-point bounds, were exactly equal |
| Payload integrity after review | All 75 payload files still match the manifest |

**Coverage precision.** The 17 named positive fixtures contain five distinct A4 cause sets. Their helper's phrase “each set of A4 causes” is broader than those named fixtures alone: `insufficient informative levels` plus `isolated adverse level`, and `insufficient informative levels` plus `finite resolution`, are absent from that set of 17. The unchanged 6,000-sweep test asserts that all seven nonempty A4 cause sets occur. L2 also constructed the two missing combinations explicitly and verified that both pass `_check_arm` and `flight_b`. This is a nonblocking clarification of the fixture description; no behavior repair is required. [T `_genuine_arms`, `test_arm_rule_against_the_reference_on_many_sweeps`; supplementary positive checks]

L1's broader fuzz program and supplied transcript were inspected. Its reported 112,062 arm-boundary refusals and 616 level-record refusals remain **L1's execution evidence**; that entire fuzz run was not repeated by L2. The independent mutation counts above are L2's separate executed checks. No whole-repository, M1–M3 rerun, canonical-machine test, or scientific qualification is claimed here.

## 4. Q1 — Is D1 closed?

**Yes.** Each original cause/schema counterexample is now refused at both the private check and the public flight boundary:

| Original round-1 counterexample | `_check_arm` | `flight_b` |
|---|---|---|
| Apparatus cause at a level still listed as informative/follows-own | `F9OutcomeError` | `F9OutcomeError` |
| Apparatus top-level cause on a COMPATIBLE arm | `F9OutcomeError` | `F9OutcomeError` |
| Own-adverse cause at a follows-own level | `F9OutcomeError` | `F9OutcomeError` |
| Missing `level_causes` | `F9OutcomeError` | `F9OutcomeError` |
| Nonmapping `level_causes` | `F9OutcomeError` | `F9OutcomeError` |
| Apparatus arm with both cause structures erased | `F9OutcomeError` | `F9OutcomeError` |

The successful genuine-arm control still returns PRODUCED where all seven arms are compatible. Thus the changed behavior is not a blanket rejection of otherwise usable arms. It rejects the contradictions that previously reached the scientific result. [D1 execution; T new acceptance/rejection tests]

The repair also rejects variants involving missing or mistyped retained levels, inconsistent nested records, extra fields, list/tuple substitutions, float/text level keys, boolean/integer substitutions, and contradictions in the informative lists or adjacency evidence. All ordinary contradictory variants constructed in this review failed as required.

## 5. Q2 — Can an accepted record be outside the constructors' outputs?

**No such arm or level record was found in the contract-shaped dictionary/list/scalar domain.** For arms, there is now a direct construction argument:

1. `_check_arm` requires a `levels` mapping containing exactly the 25 registered keys, each an actual Python `int`, with no `None` level value.
2. `_arm_tier` validates every carried level through `_check_level` and derives the aggregates, cause structures, rule, determination, and supporting levels from those records.
3. `_check_arm` compares the entire supplied arm with that recomputed output.
4. `_same_typed` checks recursive value equality, container/scalar types, and typed dictionary key sets. Missing, extra, or mistyped evidence cannot be skipped merely because the determination label looks plausible.

Under the unchanged frozen declarations, an accepted arm is therefore the constructor result for the 25 level records it carries. This addresses the reason D1 existed: in round 1 there was no checked connection between `level_causes` and the other fields. In round 2 both are reconstructed from the same retained evidence and included in the complete comparison. [O `_check_arm`, `_arm_tier`, `_same_typed`]

For levels, the check retains its reconstruction through `level_tier` or `level_apparatus`, fixed field set, content comparison, and field-type checks. The changed key-set test preserves the required string keys while avoiding a mixed-type sort. The level forms and nested mutations examined here produced no accepted contradiction. The recursive whole-record comparison is the arm mechanism; this review does not incorrectly attribute that implementation to `_check_level`. [O `_check_level`]

A consistent replacement of both the retained levels and all their derived fields can still pass. That is appropriate: it is another record the constructor can produce. Establishing that the retained levels belong to the actual terrain, composition, evaluation and run remains the runner's provenance obligation. The present clearance concerns data consistency under the frozen declarations, not arbitrary executable Python objects or mutable module behavior. [P2 §§1–2; C §5.9]

## 6. Q3 — Are genuine constructor outputs refused?

**None were found.** The reconstruction is idempotent for the declared record domain:

- On entry, a missing registered level or `None` becomes an explicit apparatus level record.
- The returned arm retains the complete 25-level mapping and computes its aggregates in registered-grid order.
- Recomputing from that retained mapping encounters the same level states, causes, B statuses and order, and therefore produces the same arm record.

The 17 supplied positive fixtures, independent 37-arm controls, 68 constructor checks, and two additional cause-combination controls support this argument. They cover complete and partial inputs, missing/unevaluable states, all level forms, the arm rules, and the legitimate cases where an unresolved rival contributes finite resolution to a follows-own or own-adverse level. [T `test_genuine_arm_records_are_accepted`; O `arm_tier`, `_arm_tier`; L2 independent checks]

The copying behavior is also appropriate. Each retained level dictionary and its mutable `causes` list is copied. Reusing the same input level object across multiple levels does not make the returned levels share those mutable objects. Mutating the caller's input after construction leaves the arm unchanged. A later internal mutation that makes the retained level evidence disagree with the arm summary is rejected. No new provenance requirement is inferred from those defensive copies.

## 7. Q4 — Is carrying the level records compatible with §§5.6 and 5.7?

**Yes. The representation is acceptable.** Section 5.6 requires the lower tier's record to be kept and requires a COMPATIBLE arm to state the informative levels supporting it. It does not limit an arm record to aggregate fields. Retaining the records from which the arm is computed directly supports those requirements and permits a complete consistency check. [C §5.6]

The new `levels` field belongs to the mandatory outcome record. The descriptive reporting items listed separately in §5.7 still have their stated role: reporting completeness and validity do not become scientific B/D tests. Checking that a required arm outcome is internally valid implements the existing §7 apparatus rule; it adds no condition based on contour constancy, measured margins, flicker, fidelity uncertainties, skeleton-boundary reporting, or component-coverage reporting. [C §§5.7, 7]

No level, arm, B or D threshold changed. The all-causes A4 convention and the normalized M3 cause strings remain accepted. The arm representation still needs the later runner's binding and persistence, and it does not by itself complete §5.7's reports or §5.9's record graph. [P2 §2; R1 Q3–Q4; C §5.9]

## 8. Q5 — Other changed definitions and observations

### Mixed-type level keys

Replacing the sorted-key comparison with a typed key-set comparison is acceptable. A malformed mapping containing both string and integer keys now fails with the module's `F9OutcomeError`, rather than raising Python's sorting `TypeError`. The required key set remains unchanged. Both the supplied regression and independent nested-key mutations exercised this behavior. [O `_check_level`; T D1 test]

### Fixed Clopper–Pearson confidence level

Removing the public `tail` argument is acceptable and closes the nonblocking round-1 helper-domain observation. The public function now accepts the survivor count and sample size and always passes the declared 0.025 tail to the unchanged numerical helper. Positional and named attempts to supply a tail fail at the Python signature. [O `clopper_pearson`; T `test_clopper_pearson`]

The private numerical helper may remain parameterized internally; the contracted persistence path calls the fixed public interface. All 41 default count cases were compared between the preserved round-1 and new source and were bit-for-bit equal in this environment. The persistence implementation and its profile/input tests parse identically, and all completed in the full test run. M4-10 remains acceptable. [O1/O comparison; C §§1.3(a), 5.4]

### Reconstruction cost

Retain the full recomputation for this placement. The complete test file finished in 60.24 seconds here, including the unusually repetitive 32,768-call Flight B enumeration. This establishes that the full file completed in this review; it is not a cross-platform performance guarantee or a price for a future scientific job. No cache or performance-driven weakening of the consistency check is required. Operational optimization can be reviewed separately if measured use later warrants it. [P2 §1, cost disclosure; T Flight B enumeration; L2 test transcript]

### Declaration dispositions

| Declaration / finding | Round-2 disposition |
|---|---|
| D1 | CLOSED |
| M4-9, revised retained-level/reconstruction guarantee | ACCEPTABLE |
| M4-10, fixed public confidence level | ACCEPTABLE |
| M4-1 through M4-8 | Prior ACCEPTABLE dispositions carried forward; their scientific rules are unchanged |
| Mixed-key typed refusal repair | ACCEPTABLE |
| Named-fixture coverage wording | Nonblocking clarification in §3 above |

No additional contract ambiguity requiring Mike's scientific ruling was identified in these changes. The original scope boundaries remain: closure comparators, T0's scientific tests, the separate reports, qualification, and runner provenance/persistence still require their own work and review. The present verdict makes no determination about those unfinished modules or any scientific endpoint.

## Appendix — Repeating the packet's D1 boundary check

From `flights/mfa_fidelity/instrument` in the unpacked round-2 packet:

```bash
python -B ../build_records/l1_m4_round2_d1_outcomes.py .
```

The execution inspected in this review printed the reviewed source and declaration hashes, the genuine seven-compatible-arm result, twelve `F9OutcomeError` refusals for the six changed records, and:

```text
genuine arms: B = PRODUCED
acceptances: 0 of 12
```

The complete module command and result are recorded in §3. All 75 payload digests were rechecked after execution and remained unchanged.

FINAL VERDICT: SOUND
