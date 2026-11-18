| Receipt check | Computed result | Verification |
|---|---|---|
| Archive | `f9_m5_build_round1_L2.zip` | Received |
| Archive SHA-256 | `03ec26d9cd7665ff2fec83b9a84ed539f6e0cd665a1751fd86d12bf5bd954558` | MATCH — supplied archive digest |
| Payload files | 67 | MATCH — expected 67 |
| Total files | 68: 67 payload files + `MANIFEST.txt` | MATCH |
| Manifest entries | 67 | MATCH — one entry per payload file |
| `MANIFEST.txt` SHA-256 | `d9120e559e70ebc8aa627bc73b83a25c2634fc8dafdd27965fb162736fca34e8` | Computed independently; manifest does not list itself |
| Payload digests | 67 of 67 match | PASS |
| Missing or unlisted payload files | None | PASS |
| Duplicate archive names or manifest paths | None | PASS |
| ZIP integrity | All members passed CRC validation | PASS |

| # | File (manifest order) | Computed SHA-256 (full) | Against `MANIFEST.txt` |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M5_BUILD_PACKET_2026-11-18.md` | `94d7b60cce9918185e0544cd10ff7d84bdcd24feed75c43b624d1809397a88ca` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py` | `df9bfb22b3e0f2c76f1ffd94ff6f789d116758b2bf025adb102b7e7bbd318aee` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/t0.py` | `afb16e81575c9ea39357d141c04c7feff40b9590935a127a9064bdb0e9eb688f` | MATCH |
| 4 | `flights/mfa_fidelity/instrument/tests/test_f9_m5.py` | `55b22704bb4e22160566ffc256e6e03c3915458822d9070f6a452b0d15f6a4dd` | MATCH |
| 5 | `flights/mfa_fidelity/build_records/f9_m5_module_container_2026-11-18.txt` | `3e571590bb1b39b1fa0f3801bd7d552b0a690d5b4f43112e2b03fa55146aee63` | MATCH |
| 6 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 7 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 8 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 9 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 10 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | MATCH |
| 11 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 12 | `flights/mfa_fidelity/build_records/F9_M4_PLACEMENT_NOTE_2026-11-18.md` | `b6004b9281aedc276b37244550baf9775853d5e678f7a1581b79fff754284839` | MATCH |
| 13 | `flights/mfa_fidelity/build_records/L2_F9_M4_ROUND2_REVIEW_2026-11-18_RECEIVED.md` | `d3391e61f22796899f5b148fcc1244c53660c8b81591b2dbee20bc9a61c2f5da` | MATCH |
| 14 | `flights/mfa_fidelity/build_records/f9_m4_module_canonical_2026-11-18.txt` | `eacdbcedbf269fc841676b201343a7cd38d8eafc9b8f04f6fbce5e630be0cb9b` | MATCH |
| 15 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 16 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` | MATCH |
| 17 | `flights/mfa_fidelity/instrument/tests/test_f9_m3.py` | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` | MATCH |
| 18 | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` | `bd51d0cd310f047f3bcd1c2d3e05d14f6ebb64ebd486b2f50398698b8002245e` | MATCH |
| 19 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 20 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 21 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 22 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 23 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 24 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 25 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 26 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 27 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 28 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 29 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 30 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 31 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 32 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 33 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 M5 build review, round 1

**Date:** 2026-11-18. **Register:** instrument build review. **Decision authority:** Mike.

**Reviewed archive:** `f9_m5_build_round1_L2.zip`, SHA-256 `03ec26d9cd7665ff2fec83b9a84ed539f6e0cd665a1751fd86d12bf5bd954558`.

**Disposition:** one contained blocking finding, **D1**, in the precedence of T0's hysteresis test. The implementation can return a scientific failure before applying Flight 9's expressly redeclared fine-grid eligibility rule. The closure map, registered stopping rule, threshold-reference arithmetic, exact T0 arithmetic, and aggregate-input bounds passed the checks described below. The other declared interpretations are accepted with the explanations in §4.

The complete M5 test file passed: **25 passed in 98.63 seconds**, with nothing deselected. Passing those tests does not close D1: the supplied second implementation uses the same disputed precedence, as L1 explicitly discloses. This review identifies a contract-conformance issue, not a disagreement between those two implementations.

The receipt above was completed before Mike's `execute`. The archive and all 67 payload digests were rechecked before extraction. The repository pin `6823c41a9b36ec4e7bcc54c560920e4d5bbf029a` is the packet's stated provenance; L2 did not independently fetch the remote repository. No packet source was edited, no flight job was authorized or run, no master was drawn, and no probe output was used. Computation was confined to module tests, identity fixtures, closure calculations, and constructed evaluator inputs.

## 1. Sources and identities

All source references below identify files in the verified archive. Section references refer to the documents themselves; code references use their original line numbers.

| Key | Archive path |
|---|---|
| P | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M5_BUILD_PACKET_2026-11-18.md` |
| C9 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` |
| FR | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` |
| C8 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` |
| CL | `flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py` |
| T0 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/t0.py` |
| D9 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` |
| O9 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` |
| E8 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` |
| CL8 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` |
| T5 | `flights/mfa_fidelity/instrument/tests/test_f9_m5.py` |

C9 is the frozen object identified by FR, notwithstanding the retained DRAFT/PROPOSED language in its bytes. The solver and T0 values are ratified by FR §3, items 3, 8, 9, and 15. The notation addendum changes no rule relevant to this finding. [FR §§1–3; `FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md`, §3.]

| Reviewed implementation or declaration | Recomputed SHA-256 |
|---|---|
| CL source | `df9bfb22b3e0f2c76f1ffd94ff6f789d116758b2bf025adb102b7e7bbd318aee` |
| T0 source | `afb16e81575c9ea39357d141c04c7feff40b9590935a127a9064bdb0e9eb688f` |
| T5 test file | `55b22704bb4e22160566ffc256e6e03c3915458822d9070f6a452b0d15f6a4dd` |
| Closure declaration | `d4196f0ecee6a55204ec8f42f7a9465c453498e4b2f85a80fe64ed963d6fcf9e` |
| T0 declaration | `8698e73fbd544a3299ef74b4fe744540ee7c04a10b152e948e6a4b1531c2a093` |

Both declaration digests recomputed to their literals. They identify the declarations; the source digests identify the implementations. A declaration digest alone does not establish source identity.

## 2. D1 — T-S2 applies an inherited phase failure before F9's eligibility rule

**Status: REQUIRES CHANGE.** This is the sole blocking finding of this review.

### 2.1 Governing requirement and implementation

C9 §5.8 makes the hysteresis bracket conditional on both boundaries having their preceding level and boundary level in the fine grid, exactly 0.05 apart. It expressly excludes a boundary at κ = 1.00 because the preceding level is 0.75. It then states: “Otherwise the hysteresis test is unevaluable, cause `bracket outside fine grid`, and the other tests stand.” FR item 3 ratifies this eligibility rule.

T0 first computes the low-sweep boundary result. If no low boundary was located, lines 310–311 return that result immediately. The eligibility check occurs only later, at line 315, after both boundaries have been located. The docstring makes the additional restriction explicit with “With both boundaries” at lines 42–45. Thus a low-sweep phase failure bypasses even an already established, explicitly named F9 ineligibility. [T0:302–317.]

This faithfully preserves Flight 8's low-sweep fallback at E8:336–339. However, Flight 9 expressly redeclares the hysteresis test's evaluability. Preserving the older fallback does not establish its precedence over that new rule.

### 2.2 Reproduced counterexample

Construct complete observations on all 25 registered levels:

- **Skeleton-high:** zero survivors and zero tail sums at 0.75; all 40 survive at every level from 1.00 upward, each with tail sum 1,000,000.
- **Skeleton-low:** zero survivors and zero tail sums at every level.
- **Realization:** all 40 survive at every level, each with tail sum 1,000,000.
- **Calibration:** both objects, all levels, 40 tail sums of 1,000,000 at each level.

These are accepted aggregate inputs. There is no missing record, calibration gap, reversal, or excess increase. The high boundary is exactly 1.00, with persistence bracket [0.75, 1.00], so `_eligible` is false.

| Record | Observed from reviewed bytes | Required under C9 §5.8 |
|---|---|---|
| T-S1′ | PASS | PASS |
| T-S1c | PASS | PASS |
| T-S2 | **FAIL**, `no active phase in sweep` | **ND**, `bracket outside fine grid` |
| T-R1′ | PASS | PASS |
| T0 determination | **NOT PRODUCED** | **NOT DISTINGUISHED** |

L2 reproduced this both in an independent reading fixture and in the minimal program in Appendix A. It is not a floating-point boundary case. It changes T0's scientific determination, although T0 gates neither B nor D. [C9 §5.8; T0:310–332.]

### 2.3 Required repair and acceptance evidence

The conforming repair is to make F9's two-boundary eligibility requirement govern T-S2 once the high-sweep boundary prerequisite has passed. Preserve malformed-input refusal and missing-record apparatus handling; retain both persistence records so that no low-sweep phase information is lost.

The repaired precedence should be explicit:

| Condition | T-S2 result |
|---|---|
| T-S1′ did not locate a two-phase high boundary | Retain the inherited dependency-ND result; see §4's additional point |
| A required low-sweep observation is missing or otherwise apparatus-unevaluable | Retain the apparatus result |
| Complete sweeps do not supply two boundaries eligible under §5.8 | ND, `bracket outside fine grid`; preserve the individual persistence profiles |
| Both boundaries eligible and absolute separation ≤ 75,400 micro-units | PASS |
| Both boundaries eligible and absolute separation > 75,400 micro-units | FAIL, `hysteresis` |

In particular, a complete low sweep with no eligible boundary must not reintroduce a scientific FAIL before the eligibility condition is met. This is the recommended reading of F9's test-level “otherwise”; it is not a proposal to change the numerical bracket or the survival criterion.

Update the source, the M5-9/M5-10 wording, the docstring, and affected expected outcomes in both the named tests and the second implementation. Add distinguishing tests for the counterexample above, the no-inactive low profile, a non-monotone low profile, and high boundaries outside the fine grid on both sides. Include a missing-low-record case to show that the repair does not relabel apparatus failure as a scientific eligibility result. Preserve the already correct eligible-boundary PASS/FAIL cases and high-sweep prerequisite behavior.

**If L1 proposes to retain the current precedence, that requires an explicit ruling from Mike**, naming the competition between C9 §5.8 and the inherited C8 phase cases and the outcomes in the distinguishing examples. It cannot be closed merely by restating reading 5 or pointing to the passing randomized test. L2 recommends the conforming repair above; this review does not ratify an exception to the frozen wording.

## 3. Q1 and Q2 — Closure and declarations M5-1 through M5-11

### Q1: closure map and stopping rule

**ACCEPTABLE.** `closure_step` implements the §4.2 map with the placed Moore-density and activation functions. The skeleton uses floor zero and starts at one; the realization uses η₀ and starts at the stationary floor-only probability. The loop counts applications from 1 through 200,000, stops at the first max-norm change ≤ 1e-12, and returns the later iterate. On nonconvergence it returns no map and records the count, last change, and `comparator unavailable`. [CL:108–167; D9:97–110; C9 §§4.2, 5.3, 7; FR item 15.]

The stopping criterion bounds one successive change, not distance to an exact fixed point. Withholding the unconverged map is correct. It avoids exposing an unfinished iterate as a usable comparator. The subcritical skeleton's tiny positive stopping map is consistent with the declared finite-tolerance rule.

An independent stopping-count check used zero gain, where the skeleton recurrence is exactly $p_n=(1-q)^n$. The first qualifying application is 131. The implementation returned 131, last change `9.26120720574579e-13`, and later-iterate value `4.182968307488716e-12`; the preceding change exceeds tolerance.

### Q2: declaration table

| Declaration | Disposition | Reason and required treatment |
|---|---|---|
| **M5-1 — map and starts** | **ACCEPTABLE** | Correct §4.2 map, parameters, periodic Moore average, floors, and initial probabilities. |
| **M5-2 — stop rule** | **ACCEPTABLE** | Inclusive tolerance, counting applications, first qualifying step, later iterate, and withholding the map at the cap make the frozen rule operational without changing it. |
| **M5-3 — meaning of convergence** | **ACCEPTABLE** | Correct distinction between successive change and fixed-point error. |
| **M5-4 — cross-machine meaning** | **ACCEPTABLE** | The map hash identifies a computation. The contract's numerical base-array tolerance does not silently impose a bitwise closure-map guarantee. |
| **M5-5 — spectral comparison** | **ACCEPTABLE** | Recomputes persistence from counts, reports integer normalized shifts and raw gains, and retains the lower bracket endpoint. The implemented raw subtraction `g(κ̂_c) − g_spec` is mathematically equivalent to the declared product; ordinary last-place float differences do not enter a decision. |
| **M5-6 — T0 comparison** | **ACCEPTABLE** | Reference availability follows §5.4, including the all-met unbracketed case. Non-monotone suffix statistics never become thresholds. Both complete persistence records remain available for uncertainty reporting. |
| **M5-7 — T0 input bounds** | **ACCEPTABLE** | The survival/tail-total bounds are necessary and sufficient at the declared aggregate level. See §5. |
| **M5-8 — exact arithmetic** | **ACCEPTABLE** | Integer and rational decisions agree with independent calculations, including exact equality cases. See §5. |
| **M5-9 — four tests and order** | **REQUIRES CHANGE** | Correct apart from D1's low-boundary/eligibility precedence. Preserve the accepted high-sweep prerequisite and the FAIL-before-ND final aggregation. |
| **M5-10 — seven readings** | **REQUIRES CHANGE** | Reading 5 requires D1's repair or an explicit Mike ruling. Readings 1, 2, 3, 4, 6, and 7 are acceptable on the bases in §4. |
| **M5-11 — calibration panels** | **ACCEPTABLE within M5's numerical interface** | Needed reversal-band inputs cannot be omitted silently. Unused calibration levels do not affect the calculation. Completion and identity of the required calibration job remain runner prerequisites, not facts certified by this function. |

No declaration is rejected in principle. These are L2's technical dispositions; Mike's governance ratification remains his action.

## 4. Q3 and Q4 — The readings and comparison with Flight 8

### Q3: each reading

| Reading | Disposition | Explanation |
|---|---|---|
| **1. Divisor 39** | **Acceptable build declaration** | Sample variance across 40 seeds uses 39. The placed F8 census uses `ddof=1`; F9 does not redeclare the divisor. [CL8:534, 572; T0:105, 213–217.] |
| **2. Endpoint difference as sampled range** | **Acceptable build declaration** | C8 §4.11 supplies the explicit endpoint formula. C9 §5.8 imports those domains and redeclares the slope normalization, without expressly replacing the range formula with max−min. Acceptance rests on that lineage, not on a claim that extra restriction is automatically preferable. State the formula explicitly in the governance record. |
| **3. Skeleton reversal clause retained** | **Acceptable build declaration** | F8 applies its evaluability rule to every monotonicity clause. F9's express reminder for realization does not repeal the skeleton clause. [C8 §4.11; C9 §5.8.] |
| **4. Hysteresis in either direction** | **Acceptable build declaration** | The inherited pass condition is absolute separation. The placed F8 evaluator fails either sign beyond the bracket. F9 changes the bracket and its eligibility, not the absolute comparison. [E8:336–344; T0:313–317.] |
| **5. No low boundary retains F8's outcome before eligibility** | **Requires repair; a ruling for Mike if retained** | The declared unconditional precedence bypasses F9's express eligibility outcome. D1 gives a complete, exact counterexample and the recommended repair. |
| **6. Brackets in [0.05, 0.10) give the same eligible-boundary decisions** | **Acceptable mathematical observation** | Eligible boundaries are 1.05 through 2.00 in steps of 0.05. Their separations are multiples of 0.05, so only the same or adjacent levels pass at 0.0754. This establishes equivalence of those discrete decisions; it does not authorize changing the frozen value. |
| **7. The low-sweep variance proxy is unused** | **Acceptable build declaration** | The inherited tests compare medians for skeleton-high and realization. Skeleton-low supplies survival counts for T-S2. There is no low-median test requiring the proxy. [T0:91, 302–325.] |

**Reading 2 is not decision-neutral.** L2 constructed a branch whose medians rise from 0.10 at 1.50 to 0.20 at 2.00, then fall to 0.18, 0.16, and 0.15 at 2.25, 2.50, and 3.00. Calibration bands were wide enough to disregard those reversals. Its endpoint difference is 0.05, its max−min range is 0.10, and its largest normalized increase is 0.02. The implemented endpoint allowance is 0.0125, giving continuity ND; a max−min allowance would be 0.025 and would pass. This is why the formula should be named explicitly. The accepted rule is the inherited endpoint formula; the alternative is a different test. [C8 §4.11; E8:307–320; T0:277–284.]

**Additional point — every high level meets the criterion:** **ACCEPTABLE inherited orchestration**, with an explicit explanation in M5-9's ratification. C9 §5.4 supplies an unbracketed descriptive reference κ̂_c,T0 = 0.75, but T-S1′ has not located two criterion phases inside the sweep. The reference can therefore be available while the onset test's prerequisite fails. C9 §5.8 specifies the continuity domain; it does not expressly remove that prerequisite. Retaining T-S1c's dependency-ND result is reasonable and does not change T-S1′'s valid failure or the final NOT PRODUCED determination. [C9 §§4.3, 5.4, 5.8; E8:471–476; T0:244–245, 288–306.]

L2 also verified the distinction computationally: a constant, all-surviving high sweep supplies the 0.75 reference and reports T-S1c dependency-ND, while directly applying the continuity body to that entire sweep returns PASS. That calculation alone does not establish that an onset was observed. No second blocking repair is imposed for this point.

### Q4: branch, order, and cause comparison

On complete valid inputs, the implementation carries the placed F8 order: missing sweep observations precede scientific decisions; phase cases retain their order; beyond-band reversals precede excess increases; the lowest offending pair is named; realization positivity precedes its continuity checks; and the first FAIL in test order outranks all ND results in the final determination. Positive increases are checked even when the endpoint difference is zero or negative. [E8:281–353, 451–479; T0:234–332.]

The explicit F9 redeclarations are implemented correctly: 40 seeds, 36 survivors, the 25-level grid, slope scaling to 0.10, the denominator √40, and the fixed 0.0754 bracket when the comparison reaches the eligibility branch. **D1 is the exception to the claim of satisfactory adaptation to §5.8.** It is faithful to old F8 code but fails to give the newer eligibility rule its required effect.

There is also an intentional interface difference: F8 validates a complete calibration census before evaluation, whereas M5 permits missing calibration levels that no reversal uses. L2 confirmed that monotone sweeps with `{"skeleton": {}, "realization": {}}` can return PRODUCED. This is acceptable for the disclosed numerical interface, but that return does not certify a complete, authorized calibration job. The runner must enforce C9 §8's calibration and qualification dependencies. [E8:465; T0:187–201, 268–271; C9 §8, steps 4–11.]

## 5. Q5 and Q6 — Exact arithmetic and possible inputs

### Q5: no arithmetic counterexample found

Let $D=1,000\times10,000=10,000,000$, and let $x_i$ be a seed's integer tail sum. The implemented statistics are:

\[
\operatorname{median}(\hat\rho)
=\frac{x_{(20)}+x_{(21)}}{2D},\qquad
\hat s^2=\frac{40\sum_i x_i^2-(\sum_i x_i)^2}{40\cdot39\,D^2}.
\]

The squared band is exactly

\[
b^2=\frac{9}{40}(\hat s_-^2+\hat s_+^2)
\left(\frac{12533}{10000}\right)^2.
\]

The positive reversal is compared to this by squaring; equality is disregarded as required. The slope comparison converts integer κ micro-units correctly and uses exact cross multiplication. Hysteresis separation and the survivor criterion also use integers. Floats written to the record do not feed these decisions. [T0:205–222, 272–284, 313–317.]

L2 independently compared **300** 40-seed panels with `statistics.median` and `statistics.variance` on `Fraction` densities; all agreed. Two exact boundary checks are particularly discriminating:

| Check | Construction | Observed outcomes |
|---|---|---|
| Reversal-band equality | One calibration panel is `[1_000_000] * 40`; the adjacent panel is `[1_000_000] * 39 + [1_200_000]`. Their band is exactly `37_599 / (2D)`. | Reversals of 37,598 and 37,599 units of twice the median tail sum pass; 37,600 produces reversal ND. |
| Slope equality | Endpoint difference in twice-median units is 4,000,000. Across 1.00 → 1.05, the increase is 500,000 such units, exactly the allowed slope after normalizing by 0.10. | One unit below and equality pass; one unit above returns continuity ND at `1.050000`. |

The reversal witness names `(1.450000, 1.500000)` when it exceeds the band. These exercise exact attainable median increments, rather than relying on a floating approximation to a threshold.

**Answer:** no decision disagreement was found against exact arithmetic for the same rule. D1 concerns which branch is allowed to decide, and the range example concerns which formula is declared; neither is an arithmetic error.

### Q6: no accepted-impossible or refused-possible aggregate input found

For a tail of 1,000 ticks and 10,000 cells:

| Survival flag | Necessary tail-sum range |
|---|---:|
| True | 1,000 through 10,000,000 |
| False | 0 through 9,990,000 |

These are exactly M5's bounds. A survivor has at least one active cell at every tail tick. A non-survivor has at least one empty tick. In particular, a non-survivor with tail sum 9,990,000 is possible: 999 fully active tail ticks followed by an empty tick. Zero absorption does not justify rejecting it. [C9 §§2.1, 2.4, 2.10, 5.4; T0:158–184.]

The bounds are sufficient at the aggregate level as well. Every admitted surviving total can be distributed over a nonincreasing sequence of 1,000 positive counts at most 10,000. Every admitted non-surviving total can be distributed over at most 999 such counts followed by zero; nested active sets can realize the decreases without requiring births after extinction. The summary interface does not claim to authenticate which actual trajectory generated the total.

L2 checked **18 endpoint and adjacent-value cases**: both survival values with totals −1, 0, 1, 999, 1,000, 9,990,000, 9,990,001, 10,000,000, and 10,000,001. Every acceptance or refusal matched the bounds. Exact 40-element lengths, native `bool`/`int` types, registered level keys, and the two observation fields are enforced. Rejecting NumPy scalars at this declared native-type interface is not evidence that a possible observation is forbidden.

Missing or `None` levels remain missing. Each present calibration level must contain exactly 40 bounded integer tail sums. A missing level needed by any reversal in the test's domain causes apparatus ND before a reversal is judged; missing unused levels do not substitute a fictitious variance. [T0:164–201, 268–276.]

## 6. Executed verification and the disclosed earlier-test defect

**Environment:** Python 3.12.14; pytest 9.2.0; NumPy 2.3.5; SciPy 1.17.0; Linux. The initial invocation found that pytest was absent from the primary runtime. L2 supplied an existing local pytest dependency directory, disabled plugin auto-loading, and ran the unmodified tests. That setup attempt collected no tests and is not a module failure.

| Verification | Result |
|---|---|
| Archive and manifest verification | Archive digest matches; exact 67-payload inventory; all 67 full digests match; no duplicate or extra path; ZIP CRCs valid |
| Complete M5 file | **25 passed in 98.63 s**; no deselection |
| Earlier F9 module files M1–M4 | **219 passed, 4 failed in 580.12 s (223 collected); failures classified below** |
| Independent exact statistics | 300 panels agree with an exact reference |
| Independent aggregate-input boundary checks | 18 cases give the expected acceptance/refusal |
| Independent monotone persistence profiles | All 26 ordered criterion profiles agree at the 35/36 boundary, including all-met and none-met cases |
| Declaration checks | Both recomputed declarations match their stated full digests |
| Contract-reading witnesses | D1 reproduced; endpoint/max−min distinction reproduced; all-met reference/prerequisite distinction reproduced |

The substantive test commands, run from `flights/mfa_fidelity/instrument`, were:

```bash
python -B -m pytest tests/test_f9_m5.py -v -p no:cacheprovider
python -B -m pytest tests/test_f9_m1.py tests/test_f9_m2.py tests/test_f9_m3.py tests/test_f9_m4.py -v -p no:cacheprovider
```

Each invocation used its own temporary directory. These were module tests and constructed fixtures, not the authorized scientific jobs of C9 §8. M5's full run includes the 200,000-application T0 nonconvergence check and the 4,000 randomized sweep-set comparison. The latter provides useful implementation evidence for the selected rules, while P §4.4 correctly states its shared-reading limitation.

**Earlier-test maintenance finding, separately disclosed by L1:** the M2, M3, and M4 preservation tests require the `f9` folder to equal the set of files present at their own module placement. Later additive modules necessarily violate those assertions:

| Test | Failing folder-list assertion |
|---|---|
| `test_f9_m2.py::test_m1_e1_and_f8_are_byte_unchanged` | `test_f9_m2.py`, line 659 |
| `test_f9_m3.py::test_everything_placed_before_m3_is_byte_unchanged` | `test_f9_m3.py`, line 534 |
| `test_f9_m4.py::test_everything_placed_before_m4_is_byte_unchanged` | `test_f9_m4.py`, line 559 |

All three failures reproduced exactly at these folder-list assertions. Each test had first passed its preceding per-file digest checks. No additional numerical or record-processing failure appeared in the completed earlier-module run.

**The fourth failure is a packet dependency limitation:** `test_f9_m2.py::test_every_earlier_master_is_refused_l2_m2_round1_r2` raises `FileNotFoundError` while opening `flights/mfa_fidelity/design/flight9/probe/f9_probe.py`. That source is not among the 67 manifest payloads. The failure occurs at the source-grounding assertion, before the test reaches its retired-master refusal checks; it does not show that a retired master was accepted. L2 did not import outside bytes to make this packet appear self-contained. This check must be rerun in the full pinned checkout, or with that dependency supplied under a verified identity, before claiming complete earlier-module regression passage. [`test_f9_m2.py`:115–142.]

The appropriate separate repair retains every historical per-file digest assertion and tests required membership without forbidding later module files, as M5's own preservation test already does. These are not evidence of altered earlier source bytes or a second M5 numerical defect. They do prevent a claim that the combined test suite is green. Any repair to those placed test files should be disclosed with its new identities and validation. [P §4.5; T5:693–724.]

## 7. Q7 — Module boundary and outstanding downstream duties

**The stated module boundary is acceptable.** No duty identified here must be moved into M5. C9 §5.3 assigns it the closure comparators. The following remain mandatory obligations of later modules:

- Comparing the finite-tail lattice occupancy map with the matching-object closure map, and applying the declared edge rule when edges are compared.
- Reporting local $m_i$ on the observed edge against the stated references.
- Producing the occupancy-based resampling ranges and the other uncertainty reports of §5.7.
- Binding numerical inputs and outputs to authentic run records, canonical terrain/spectral identities, the calibration and qualification records, and the authorized job graph.

These are retained obligations under C9 §§1.2′, 5.7, 5.9 and §8 step 15. M5's acceptance on its local calculations would not discharge them.

`ArmContext` is a trusted internal context constructed from the verified identity bundle. The placed dynamics module explicitly assigns canonical provenance to the caller and runner; M5's use of that interface does not newly promise to validate a forged context. Similarly, survivor counts are recomputed into persistence records but are not authenticated as measurements here. [D9:24–29, 231–239; CL:145–153, 176–218; T0:10–16.]

There is no basis in F9 §6 to import F8's separate qualification job for the T0 tests. M5's synthetic known-answer tests remain implementation evidence; they are not a newly authorized job.

## 8. Q8 and Q9 — Nonconvergence disclosure and remaining notes

### Q8: record the known limitation beside the contract

**Recommendation: yes.** Add an append-only implementation/disclosure note before fidelity reporting, identifying the registered solver's nonconvergence at the skeleton crossing. The per-computation `comparator unavailable` record already satisfies the algorithmic rule, so this is not an additional build blocker and does not call for changing the frozen cap or tolerance. [C9 §§4.2, 7; FR item 15; CL:129–136, 160–166.]

For T0 there is a direct explanation. At κ = 1 the uniform zero-floor map has the expansion

\[
f(p)=p-\left(q+\frac{q^2}{2}\right)p^2+O(p^3).
\]

Writing $a=q+q^2/2\approx0.1976985169$, the late decay behaves as $p_n\sim1/(an)$, so the successive change behaves as $1/(an^2)$. At 200,000 applications that estimate is about $1.26455\times10^{-10}$, above the frozen tolerance; the asymptotic estimate for reaching $10^{-12}$ is approximately 2.249 million applications. This explains the observed unit-test behavior without treating the absence as an apparatus failure. It is not a proposal to run a longer solver.

L2 completed the supplied T0 check. The analytical explanation is for T0; it is not numerical verification that all fifteen arms fail at κ = 1. L1's untested-arm expectation should remain labeled as an expectation. The closure's unavailability affects fidelity reporting only.

### Q9: one nonblocking interface-documentation correction

CL:180–181 says that, for T0 itself, passing T0's counts as `survivors` gives a zero self-comparison. In fact, CL:201–204 requires both `t0_survivors` and `t0_g_spec` as well; omitting them returns `reference unavailable`. The test at T5:239–241 correctly supplies the counts and gain in both roles.

Clarify the docstring to say that the same T0 counts and gain must also be passed as the reference arguments. The implemented missing-reference behavior is acceptable; the current description is incomplete. This is not another blocking finding.

## 9. Closure requirements for this round

D1 remains open. A return should supply the revised T0 source and tests, revised declaration/reading text and identities as applicable, and evidence for the distinguishing cases in §2.3. If Mike chooses a different precedence by explicit ruling, include that governing record and verify the implementation against it.

The accepted closure, arithmetic, input-bound, scope, and other interpretation findings need not be reopened unless their bytes or governing requirements change. The separate earlier-test maintenance issue must be accurately reported until repaired. Nothing in this review grants run authorization or constitutes Mike's ratification of the module declarations.

## Appendix A — Minimal D1 reproducer

Run from `flights/mfa_fidelity/instrument` on the reviewed packet. It uses only constructed aggregate observations.

```python
from mfa_instrument.f9 import config as C, t0 as T

def obs(survives, total):
    return {"survival": [survives] * 40, "tail_sum": [total] * 40}

grid = C.F9_LEVELS_MICRO
high = {
    k: obs(k >= 1_000_000, 1_000_000 if k >= 1_000_000 else 0)
    for k in grid
}
low = {k: obs(False, 0) for k in grid}
realization = {k: obs(True, 1_000_000) for k in grid}
calibration = {
    obj: {k: [1_000_000] * 40 for k in grid}
    for obj in ("skeleton", "realization")
}

r = T.evaluate_t0(high, low, realization, calibration)
print("high boundary:", r["reference"]["kappa_c_t0_micro"])
print("high eligible:", T._eligible(grid.index(1_000_000)))
for test in r["tests"]:
    print(test["test"], test["outcome"], test["cause"])
print("T0:", r["determination"], r["cause"])
```

Observed output from the reviewed bytes:

```text
high boundary: 1000000
high eligible: False
T-S1′ PASS None
T-S1c PASS None
T-S2 FAIL no active phase in sweep
T-R1′ PASS None
T0: NOT PRODUCED no active phase in sweep
```

The conforming repaired output changes T-S2 to `ND bracket outside fine grid` and the T0 determination to `NOT DISTINGUISHED bracket outside fine grid`; the other three tests remain PASS.

FINAL VERDICT: DEFECT-WITH-REPAIR
