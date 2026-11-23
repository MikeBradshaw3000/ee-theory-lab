| Receipt item | Expected / reference | Independently verified result |
|---|---|---|
| Archive | `f9_m6_build_round1_L2.zip` | Same archive |
| Archive SHA-256 | `552a5cf3535e733b9776b2cd71de0d7e03dc846b45ea1b848dc3265af551e112` | `552a5cf3535e733b9776b2cd71de0d7e03dc846b45ea1b848dc3265af551e112` — MATCH |
| Files listed in MANIFEST.txt | 78 | 78 — MATCH |
| Archive files, excluding directory entries | 78 payload files plus MANIFEST.txt | 79 — MATCH |
| Payload digests | Every listed file must match | 78/78 MATCH; zero mismatches |
| Missing / unlisted payload files | 0 / 0 | 0 / 0 |
| Duplicate manifest / archive file paths | 0 / 0 | 0 / 0 |
| MANIFEST.txt SHA-256 | No supplied reference; not self-listed | `f9451f1682bcfbe46561122f50f2e17329553cfdd2eda9b1d1614f046beb435b` |
| Receipt gate | Review only after Mike's execute | Receipt delivered first; execute received before review |
| End-of-review preservation | Original packet bytes retained | All 78 payload files and MANIFEST.txt unchanged |

| # | Archive-relative path | Computed full SHA-256 | Against MANIFEST.txt |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M6_BUILD_PACKET_2026-11-23.md` | `4bae93832659dc52a120bb1256f3408fa06392be457809819373cc03c2f8b81e` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/reports.py` | `6e886549559b8ec2724c3a1539f07d8198f712285d31043f3850f17c9c02b146` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/tests/test_f9_m6.py` | `b4cae42d19f29d1ec8728d13a2d69cff4428ff005df10aac4a30d33bf52da8c5` | MATCH |
| 4 | `flights/mfa_fidelity/build_records/f9_m6_module_container_2026-11-23.txt` | `5f75f11ce965001dfccf8bbb0774dc562a62d1e98a302ef8182e1f7778d5a607` | MATCH |
| 5 | `flights/mfa_fidelity/build_records/f9_m1_to_m6_container_2026-11-23.txt` | `75df38495df48377d1975e138a4ebab5e3686c96a1b0c2f8225732936310f767` | MATCH |
| 6 | `flights/mfa_fidelity/build_records/f9_m6_mutation_check.py` | `9eef3e2d968a80830c62491572f2229ba707dc0db0241dace9814d631842e55c` | MATCH |
| 7 | `flights/mfa_fidelity/build_records/f9_m6_mutation_check_2026-11-23.txt` | `0aa0e268cd656ce816a63757c17a07f456b4f8a399d25d3c6738d835f7947771` | MATCH |
| 8 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 9 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 10 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 11 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 12 | `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | `473a2a165fd5cb4e38ddb064dc14c24880af8998a21b9ffad1aa7c065551016c` | MATCH |
| 13 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |
| 14 | `flights/mfa_fidelity/rulings/F9_MASTER_RULING_RECORD.md` | `02b98378057e776769b48150059a2b9323737fd5ab437f907ae4d62c3fc27b75` | MATCH |
| 15 | `flights/mfa_fidelity/rulings/F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` | `b38a4ff6eaa3e2118a9ae723cff63a3336fb178a35932071c3dc43c4478c50a6` | MATCH |
| 16 | `flights/mfa_fidelity/rulings/F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` | `bc5fac1d53fd57ac0923fb759e465e8783389d92cb1188e297c185c5b91ac78d` | MATCH |
| 17 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 18 | `flights/mfa_fidelity/build_records/F9_M5_PLACEMENT_NOTE_2026-11-18.md` | `41dfe671983e295f01696a9b1d9c7fb20f0006be6e695b0d5a42ebd647de6e17` | MATCH |
| 19 | `flights/mfa_fidelity/build_records/F9_TEST_REPAIR_PLACEMENT_NOTE_2026-11-18.md` | `ba35214dbb2d1e23d0d7931fb96b571aaf2c05b42f1320a48d6a8b52e9045d6b` | MATCH |
| 20 | `flights/mfa_fidelity/build_records/F9_GOVERNANCE_RECORDS_PLACEMENT_NOTE_2026-11-20.md` | `5aecde9c514b12000005169ed889f1daa01c935b377d482b654ee72724df9c20` | MATCH |
| 21 | `flights/mfa_fidelity/build_records/L2_F9_GOVERNANCE_RECORDS_ROUND2_REVIEW_2026-11-20_RECEIVED.md` | `4ac4e07b5e40a1cf41d624878467d6be0303ab32cb5dd341d1674709f8e5b92d` | MATCH |
| 22 | `flights/mfa_fidelity/build_records/f9_m1_to_m5_canonical_2026-11-18.txt` | `1f79b9aa1160c7cb7f7f96ef6e54f30028409b170a66474459b847e31dd88cba` | MATCH |
| 23 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 24 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `e505cd6bd302c1e005b37f4bc4ad364300b83fd4ab40bb73ac6ef18c0084073a` | MATCH |
| 25 | `flights/mfa_fidelity/instrument/tests/test_f9_m3.py` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` | MATCH |
| 26 | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` | MATCH |
| 27 | `flights/mfa_fidelity/instrument/tests/test_f9_m5.py` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` | MATCH |
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
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py` | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/t0.py` | `a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 72 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 73 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 74 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 75 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 76 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 77 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 78 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 M6 build review, round 1

**Date:** 2026-11-23. **Reviewer role:** L2, adversarial module-build review. **Decision authority:** Mike.

**Reviewed archive:** `f9_m6_build_round1_L2.zip`.

**Archive SHA-256:** `552a5cf3535e733b9776b2cd71de0d7e03dc846b45ea1b848dc3265af551e112`.

**Assessment: NOT SOUND in its submitted form.** Two contained repairs are needed in the flicker reporting path: reject mutually inconsistent summaries at different window widths, and include the already-required floor reference for each width. The declaration that TC set cardinalities reject every other array also requires correction. The constancy and measured-margin calculations passed the independent checks described below; the TC calculation is correct when supplied the authenticated canonical TC base array.

This disposition concerns the submitted module, tests, and declarations. It is not a scientific result for Flight 9, a qualification result, a placement authorization, or a run authorization.

## 1. Review basis and boundaries

The receipt above records 78 matching payload digests, the manifest digest, and the matching archive digest. The instruction document was read first, and substantive review began only after Mike's `execute`.

The repository pin stated in the packet is `67aa10ca5958e0c07855441fbeab4a71a66e51f5`. This review verifies the supplied archive and its internal identities; it does not independently attest the remote repository's HEAD. The supplied placed-file identity test passed, and a final comparison found every original extracted payload byte unchanged from the archive.

The frozen contract is `FLIGHT_9_CONTRACT_v0_7.md`, SHA-256 `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`. Its retained draft/proposed markers do not reopen it: the Freeze Record ratifies the values and §5.7 schemas while preserving the contract bytes. [FR §1 and §3, especially item 17.]

### Source references used below

Paths in this table are relative to `flights/mfa_fidelity/` inside the reviewed archive. Line references are to those exact bytes. Every source's full SHA-256 appears in the receipt.

| Key | Source |
|---|---|
| P | `build_records/L1_TO_L2_F9_M6_BUILD_PACKET_2026-11-23.md` |
| C | `contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` |
| FR | `contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` |
| PP | `design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` |
| PROBE | `design/flight9/probe/f9_probe.py` — source only; no probe output was read |
| R | `instrument/mfa_instrument/f9/reports.py` |
| TEST | `instrument/tests/test_f9_m6.py` |
| D | `instrument/mfa_instrument/f9/dynamics.py` |
| E | `instrument/mfa_instrument/f9/evaluator.py` |
| T | `instrument/mfa_instrument/f9/terrain.py` |
| ID | `instrument/mfa_instrument/f9/identities.py` |
| MR | `rulings/F9_MASTER_RULING_RECORD.md` |
| I001 | `rulings/F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` |
| D001 | `rulings/F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` |

The implementation reviewed is `reports.py`, SHA-256 `6e886549559b8ec2724c3a1539f07d8198f712285d31043f3850f17c9c02b146`; its test file has SHA-256 `b4cae42d19f29d1ec8728d13a2d69cff4428ff005df10aac4a30d33bf52da8c5`. The declared reports digest verifies as `56bc9a108afdc347bcdae98f254de7f3072e091a46d607ed40a118ae887945d2`.

## 2. Required repairs

| Finding | Disposition | Required action |
|---|---|---|
| D1 — Missing consistency checks between window widths | Code and test repair; blocks soundness | Apply the placed parser's nested-width relations to the supplied stack before computing flicker statistics; repair the existing impossible positive fixture. |
| D2 — Missing W-specific floor references | Reporting-schema and test repair; blocks soundness | Return the three bound floor-only active-window occupancy references, associated with their correct widths. |
| D3 — TC cardinality check described as array authentication | Declaration repair | Replace the universal refusal claim with the actual cardinality check and the existing obligation to obtain u from the authenticated canonical bundle. |

The reading-number alignment, null representation, and report-ownership clarifications in §§6–8 are also required before the affected declarations are ratified. They are distinguished below from the two computational/report-completeness blockers.

### D1. M6 accepts an impossible combination of fine and coarse window records

The three window widths describe the same cell and seed over the same aligned tail. A coarse window is active if any constituent tick is active. Those facts impose relationships between widths, not merely validity conditions within each width. [C §2.11, line 131; PP §6 points 1–2.]

`_check_windows` checks the type, shape, bounds, and alternating-segment relations for each W independently. It then returns the stack without checking the relationships between widths. The placed parser already checks those relationships, and every quantity needed for them is present in M6's input. [R lines 226–250; D lines 397–415 and 450–458.]

**Reproduced counterexample.** Give every one of the 40 × 100 × 100 records the following values:

| W | Number of windows n | A | R₀ | First | Last |
|---:|---:|---:|---:|---|---|
| 1 | 1,000 | 0 | 1 | inactive | inactive |
| 10 | 100 | 100 | 0 | active | active |
| 100 | 10 | 10 | 0 | active | active |

Every row separately satisfies M6's checks. `flicker` accepts the combined stack. Its output puts all 10,000 cells in the zero-to-0.10 occupancy band, reports 400,000 defined durations of 1,000 ticks at W = 1, and reports 400,000 undefined, all-active records at each of W = 10 and W = 100. This is impossible: a cell inactive at every tick cannot be active in any coarse window. Appendix R reproduces this directly on the submitted bytes.

**The required checks are already specified in the placed parser.** For every pair Wₛ < Wₗ with k = Wₗ/Wₛ, define Rₐ = R₀ − 1 + first + last and require, cell by cell and seed by seed:

\[
A_l\le A_s\le kA_l,\qquad
R_{0,l}\le R_{0,s},\qquad
R_{a,l}\le R_{a,s},
\]

\[
\mathrm{first}_s\Rightarrow\mathrm{first}_l,
\qquad
\mathrm{last}_s\Rightarrow\mathrm{last}_l.
\]

Apply them to (1, 10), (1, 100), and (10, 100), before producing any distribution. Retain the existing bounds-before-conversion behavior. Reject a contradiction as malformed report input; do not turn it into a scientific B or D outcome. [D lines 450–458; C §5.7 opening.]

**The supplied test contains an impossible positive.** TEST lines 504–505 change only a W = 1 tuple to `(A=2, R0=1, first=True, last=True)` and assert acceptance. In the supplied deterministic fixture, the selected cell was `(seed=0, i=2, j=38)`:

| W | Original tuple (A, R₀, first, last) | After the test's edit |
|---:|---|---|
| 1 | `(628, 3, True, True)` | `(2, 1, True, True)` |
| 10 | `(66, 3, True, True)` | unchanged |
| 100 | `(8, 1, True, True)` | unchanged |

Two active fine ticks cannot create 66 active ten-tick windows or eight active hundred-tick windows. The ten-tick segment counts also violate the placed parser's nesting conditions. Replace this positive with a record constructed from one common tick sequence at all widths, or make the current stack a negative. For example, a sequence active only at its first and last tick gives `(2, 1, True, True)` at all three widths and is a valid positive.

The independent checks additionally exercised all six written predicates. Five cases isolate one predicate each; an increase in R₀ cannot be isolated from both active-segment monotonicity and the endpoint implications. Indeed,

\[
R_{a,l}-R_{a,s}=(R_{0,l}-R_{0,s})+(f_l-f_s)+(l_l-l_s).
\]

When both endpoint implications hold, the last two terms are nonnegative. A test requirement that independently kills the R₀ check while all three of those other conditions hold would therefore be impossible. Appendix R supplies the six useful negative constructions without imposing that requirement.

**Scope of this repair.** The runner remains responsible for complete-record parsing, global-count relations, provenance, arm/level/object/seed membership, and canonical-array binding. Those require information absent from this API. D1 concerns a contradiction within the arrays already supplied to M6. Adding the parser's available nesting checks does not claim that these summary checks reconstruct or authenticate an entire trajectory; the placed parser itself describes its checks as necessary, not sufficient. [D lines 397–415; P M6-1 and disclosure 7.]

### D2. The flicker report omits its bound floor references

The reporting obligation is explicit in the incorporated declaration. PP §6 point 3 requires the distribution by occupancy band **with the W-specific floor reference**, and names `(0.0523, 0.1342, 0.6496)`. PP §6's opening says the section binds Flight 9. C §2.11 incorporates that section unchanged. These are existing requirements, even though §5.7's short table does not repeat the numbers. [PP lines 90–98; C line 131.]

`flicker` returns no floor reference at any level of its record. On a valid all-inactive constructed stack, the top-level fields are `record`, `kind`, `statistic`, `bands_by`, `bands`, `note`, and `declaration_sha256`; each W entry contains counts and quantiles only. M6's scope claims §1.3(c), and neither its implemented list nor its deferred list allocates this missing obligation elsewhere. [R lines 265–288; P §§1–2.]

**Required addition:** carry this mapping in the flicker output, with an explicit label identifying its meaning:

| W, ticks | Registered floor-only active-window occupancy reference |
|---:|---:|
| 1 | 0.0523 |
| 10 | 0.1342 |
| 100 | 0.6496 |

These are occupancy probabilities, not inactive-segment durations in ticks. The label must prevent that confusion. Their presence does not change band membership, the duration statistic, censoring, or any decision.

The analytic check uses a = 1 − exp(−η₀Δt), π₁ = a/(a + q), and

\[
\Pr(\text{any activity in W ticks})
=1-(1-\pi_1)(1-a)^{W-1}.
\]

The independently computed values were approximately 0.0522823201, 0.1342435537, and 0.6496006856, reproducing the registered four-place references and the contract's Appendix A.3. This calculation uses rule constants only and requires no dynamics run. [C §§2.4, 5.2 and Appendix A.3; D lines 107–110; Appendix R.]

Add tests that verify all three fields and their W association, including a valid empty/no-defined-band case. Add the mapping and its meaning to the build declaration/digest as appropriate. Do not edit the frozen contract to remove an inherited reporting item.

### D3. TC set sizes do not authenticate TC's base array

The TC mask calculation is correct on its intended input. The defect is the stronger assertion in M6-8 that checking the two sizes means “any other array is refused.” The function checks finite float64 shape and the two mask cardinalities. Many different arrays satisfy those checks. [P M6-8; R lines 292–299.]

An independent check supplied `np.roll(u, 1, axis=0)`. The function accepted it, although 54 inside-mask memberships and 102 outside-mask memberships differed from the correct masks. An entirely fabricated array with the same cardinalities also passed.

To show that the distinction affects the reported quantity, construct counts of 1,000 on the correct inside set, 100 on the correct outside set, and zero on the intermediate set:

| Supplied u | Mean inside | Mean outside | Inside/outside |
|---|---:|---:|---:|
| Correct TC u | 1 | 1/10 | 10 |
| TC u shifted by one cell | 518/545 | 3896/39215 | 2031337/212332 ≈ 9.5667963378 |

**Required declaration repair:** describe the assertions as geometry/cardinality sanity checks and state that u must be the TC base array from the authenticated canonical bundle. The existing M6-1 division of responsibility can remain. This finding does not require the pure statistic function to authenticate an entire bundle, nor does it warrant replacing stored u with newly recomputed terrain arrays. The future runner must test the actual binding obligation; size equality cannot discharge it. [C §3.4 steps 4–5; P M6-1 and disclosure 7.]

## 3. Q1 — constancy binning and exact variances

**The implementation agrees with §5.7 row 1 on the declared domain. No arithmetic counterexample was found.**

Stable ascending sorting gives the specified flat-index order within ties. The implementation adds whole equality blocks, closes a bin at at least 100 cells, and merges a final shorter remainder into the preceding bin. Independent checks covered 29 structures: all 16 terrain/composition combinations available from the terrain builder, including the redundant T0/H comparison, and 13 synthetic tie, distinct-value, and remainder constructions. These checks do not add T0/H as a scientific arm. [C §5.7 row 1; R lines 145–169.]

For n = 40, T = 1,000, D = nT = 40,000, t = Σₛcₛ, and N = 10,000,

\[
\bar p=t/D,\qquad X_s-\bar p=(nc_s-t)/D.
\]

Linearity of within-bin centering P gives

\[
V_{\rm within}=\frac{\|Pt\|^2}{D^2N},\qquad
V_{\rm noise}=\frac{\sum_s\|P(nc_s-t)\|^2}{D^2n(n-1)N}.
\]

These are exactly the code's denominators and the contract's quantities. There is no missing or extra factor of 40. Production computes each bin contribution as Σx² − (Σx)²/n_b. The independent reference used explicit centered integer residuals, Σ(n_bx_i − Σx)²/n_b², before applying the divisors. All 12 exact-rational fixtures agreed. [R lines 172–203; C line 263.]

| Discriminating constructed case | V_within | V_noise | Difference |
|---|---:|---:|---:|
| One seed, one cell at 1,000 ticks, in a 100-cell bin | 99/1600000000 | 99/1600000000 | 0 |
| Each seed map spatially constant, with different constants across seeds | 0 | 0 | 0 |
| Complementary checkerboard seed maps, constant comparison array | 0 | 1/156 | −1/156 |

The negative difference is retained; the exact zero flag is correct; no variance ratio is introduced. Those behaviors preserve the descriptive-only interpretation. Neither a small nor a large difference becomes evidence about the uncoupled alternative. [R lines 198–203; C §§1.3(b), 1.4 and 5.7.]

Integer overflow is excluded on the declared input domain. The checked counts lie in 0…1,000; t_i ≤ 40,000; and |40cₛ,ᵢ − t_i| ≤ 39,000. A sum of 10,000 squared values is at most 1.6 × 10¹³, within signed 64-bit capacity. Bin sums are converted to Python integers before their squares are accumulated, and Fraction handles the rational arithmetic. [E lines 124–131; R lines 172–197.]

The packet's phrase “bit-equal” is more literal than the implementation, which uses numerical equality of the stored values. For canonical comparison arrays this makes no difference. The contract calls for equality on the stored rounded ω, without an added tolerance; no bit-pattern comparison or signed-zero special case is needed here.

## 4. Q2 — measured margins and cut boundaries

**The margin counts and ratios implement the contract's exact inequalities. No count counterexample was found.**

The smoothed occupancy is Bᵢ/360,000, where B is the periodic 3×3 sum of the seed totals. The three predicates reduce to:

| Cut | Exact integer condition |
|---|---|
| 0.10 | Bᵢ ≥ 36,000 |
| 0.20 | Bᵢ ≥ 72,000 |
| 0.30 | Bᵢ ≥ 108,000 |

All 1,080,003 comparisons over B = 0…360,000 and the three cuts agreed. The largest product in `_at_least` is 3.6 × 10¹¹, safely within int64. The lower band edge is inclusive and its upper edge exclusive. The band/core ratio is exact when the core is nonempty and is `"undefined"` when empty. [R lines 133–141 and 207–222; C line 264.]

Fourteen full margin fixtures were checked using explicit periodic neighbor indices rather than the placed `box_sum`. On a uniform map exactly at a cut, decreasing one seed's single cell count by one moves precisely its nine periodic neighborhoods below that cut. At 0.20 this gives 9,991 core cells and nine band cells at the 0.20 cut; at 0.30 it gives the same counts at the 0.30 cut. Exact equality puts all 10,000 cells into the corresponding core. These cases discriminate strict/inclusive and smoothing errors.

The single floor reference carried with the paired margin summaries is present and correct. D2 concerns the separate flicker output, which currently carries none.

## 5. Q3 and Q4 — sound calculations within the corrected input boundary

### Q3. Flicker

The answer to “exactly the placed parser's relations, neither more nor fewer?” is **no**, because of D1. However, the individual-width checks themselves are correct. Exhaustive enumeration of all 1,024 length-10 binary sequences gives 92 realizable `(A, R₀, first, last)` tuples. Among all 484 candidate tuples with A and R₀ in 0…10, exactly those same 92 satisfy the declared per-width relations: no false positives and no false negatives.

This also has a direct explanation. The endpoint values fix the alternating arrangement of R₀ inactive segments and Rₐ active segments. Each existing segment needs at least one window; the inequalities ensure enough active and inactive windows to allocate positive lengths. They characterize a single width, not simultaneous coarse-grainings of a common sequence. [R lines 237–248; D lines 405–415.]

For valid, mutually consistent input, the remaining arithmetic is correct:

- Occupancy bands use the unsmoothed W = 1 seed mean with integer cut comparisons.
- W(n − A)/R₀ is the total number of observed inactive-window ticks divided by the number of observed inactive segments.
- R₀ = 0 identifies the all-active undefined case.
- A record is possibly censored if either end is inactive.
- Quantiles include every defined value, including possibly censored values, and use the declared linear interpolation.
- Empty/no-defined bands retain counts and return null quantiles.

[C §2.11 and §5.7 row 3; R lines 253–288.]

The per-record numerator is at most 1,000 and the denominator is a positive integer at most 1,000. Thus these operands are represented exactly before the floating division. No ratio of sums across records replaces the required distribution of per-record ratios.

### Q4. TC geometry and contrast

Deriving bump from authenticated stored u is acceptable. The terrain equation is u = 0.9 − 0.85·bump, so the reconstruction uses the same geometry specified by the contract and R-6. Independent comparison with `PROBE::tc_bump(100)` found identical inside and outside masks, of sizes 545 and 7,843. This involved the source's closed-form geometry only. [C §3.1 TC row; PP R-6; T lines 85–87; R lines 292–310.]

The minimum distances from the direct bump to the thresholds were approximately 0.0013001666 at 0.5 and 0.0004448986 at 0.05. The largest reconstruction difference was approximately 1.11 × 10⁻¹⁶. The thresholds therefore have ample separation in the checked geometry. There is no reason to replace the stored canonical object with a new platform-dependent cosine computation. [Independent geometry check; C §3.4.]

The means use exact totals over the two specified sets, and the ratio is inside divided by outside. Intermediate cells enter neither mean. A zero outside mean produces `"undefined"`. The report's near-face/zero-collapse limitation is correct. D3 concerns authentication language and the caller's obligation, not a numerical failure on canonical u. [R lines 303–313; C §§1.3(e), 1.4.]

## 6. Q5 — disposition of M6-1 through M6-10

| Declaration | L2 disposition | Reason / required change |
|---|---|---|
| M6-1 — inputs and binding boundary | ACCEPTABLE | A pure map-statistic API may rely on the runner for full records, seed/arm/level/object identity, and canonical bundle binding. Its locally checkable stack constraints still need D1. These output dictionaries are components of eventual §5.9 records, not complete bound job records by themselves. |
| M6-2 — integer occupancy and cuts | ACCEPTABLE | Correct denominators, integer comparisons, and ties. Verified at every possible box-sum value for the three cuts. |
| M6-3 — constancy bins | ACCEPTABLE | Whole ties, ≥100 rule, and final merge implement §5.7 exactly. |
| M6-4 — exact variances | ACCEPTABLE | Correct projected residuals and divisors; exact zero test; negative differences preserved; no ratio. |
| M6-5 — margins | ACCEPTABLE | Correct core/band counts, exact ratio, empty-core handling, and floor reference. The additional 0.20 pair is acceptable as disclosed. |
| M6-6 — flicker record checks | REQUIRES CHANGE | Add the nested-width relations that the placed parser enforces and that M6 can check from its own inputs. Correct the impossible positive fixture. Distinguish these from unavailable global-count/provenance checks. |
| M6-7 — flicker statistic/report | REQUIRES CHANGE | Preserve the statistic, bands, counts, and quantile behavior, which are acceptable. Complete the declared output with the inherited W-specific floor references under D2. |
| M6-8 — TC sets | REQUIRES CHANGE | Keep the mask formula and exact means; replace “any other array is refused” with the actual sanity-check guarantee and the canonical-u caller obligation under D3. |
| M6-9 — seven readings | REQUIRES CHANGE | Align the two numbered lists, or provide one explicit identifier mapping. The substantive dispositions are in §7. The mismatch is traceability, not a hidden computational omission. |
| M6-10 — plain records | REQUIRES CHANGE | Include null/`None` in the type description, because valid flicker records contain it. Keep the reported-only kind and declaration identity, and extend the representation test to flicker. Wire-key encoding belongs to the later persistence declaration. |

For M6-9, P §3 makes inclusion of censored values reading 4 and treats bin cell counts as an unnumbered addition. R's numbered docstring makes empty quantiles item 4, ties item 5, TC job allocation item 6, and bin counts item 7. Censored inclusion is present in ordinary docstring prose, so the behavior is visible; the numbered ratification target is simply inconsistent. [P §3; R lines 35–66.]

For M6-10, JSON serialization succeeds, but integer W keys become strings on JSON reload. The supplied exact-roundtrip test includes the other three reports and excludes flicker. This is not a newly invented requirement that the Python API survive JSON reload with identical key types. State the actual schema, include the null case, and specify key encoding when the runner persists it. [R lines 275–285; TEST lines 591–599.]

## 7. Q6 — each reading and the additional bin counts

The following dispositions use the numbering in **P §3**. Acceptable build declarations should be recorded with the build's ratification; that is distinct from asking L2 to resolve a competing scientific interpretation on Mike's behalf.

| Item | Disposition | Basis |
|---|---|---|
| 1. The 0.20 cut carries both counts and their ratio | Acceptable build declaration | The required ≥0.20 count is present under either proposed reading. The companion band and ratio are transparent descriptive additions and change no criterion. |
| 2. Linear-interpolated quartiles | Acceptable build declaration | §5.7 leaves the convention unstated. The selected deterministic convention is reasonable and consistent with the linear interpolation used in §5.5. Do not say §5.5 explicitly imposes it on §5.7. |
| 3. Censored records counted among all records | Acceptable; equivalent counting domain on valid input | An undefined all-active record has both ends active and cannot be censored. Restricting the censor count to defined records gives the same number. |
| 4. Censored defined records included in quantiles | Acceptable and required by the existing wording | §5.7 says all records with a defined value; it supplies no censor-exclusion rule. |
| 5. No defined value means null quantiles | Acceptable build declaration | It records absence without inventing a zero duration; the counts distinguish an empty band from an all-active one. Correct M6-10's type list accordingly. |
| 6. Ties use stored rounded ω without tolerance | Acceptable; contract-conforming | §3.4 defines that comparison array and §5.7 bins by it. Another tolerance would change the partition. Prefer “equal stored values” to literal “bit-equal.” |
| 7. TC object and job allocation left to the runner | Acceptable module boundary; record the coverage choice before runner placement | The function can be object-neutral. The runner must bind which object it uses, cover both TC arms and registered levels, and allocate the mandatory record within step 15. A binding interpretation that narrows ambiguous object coverage is Mike's decision. |
| Addition: each bin's cell count | Acceptable build addition | Makes bin size and final merging inspectable, without changing the statistic or its status. |

**Reading 7 requires a precise distinction.** C §1.3(e) fixes TC's arms, levels, sets, means, and ratio; its R-6 cross-reference explicitly names the sets. R-6 itself describes realization runs. That makes realization coverage well grounded, but the wording should not be overstated as an unambiguous command about every possible object's coverage. An economical declaration is realization contrasts for both TC arms at every registered level, with any additional skeleton contrasts separately labeled. If that declaration is intended to settle a competing interpretation as realization-only, obtain Mike's ruling in the governance record; L2 does not supply it here. [C line 85; PP line 84.]

The absence of a job named `suppression_report` does not remove the obligation or require a seventh job. The contrast can be a named component of an existing step-15 report, with explicit coverage and validity accounting. The exact hosting field is a runner/build choice, not a reason to defer the numerical function. [C §8 step 15, line 415.]

## 8. Q7 — module split and reporting coverage

**The split is acceptable.** The contract does not require all reporting functions to occupy one file or one build round. Separating pure map statistics from evaluator-dependent reports is a reasonable implementation boundary. No currently implemented statistic must wait for the second module.

The complete coverage ledger should be:

| Requirement | Current or deferred owner / status |
|---|---|
| §1.3(a), §5.4 persistence profile, intervals, threshold and bracket | Persistence report assembly may be deferred, using the placed M5 calculations and all typed profile cases. |
| §1.3(b), §5.7 row 1 constancy | Present M6; numerical implementation accepted. |
| §1.3(c), §2.11 and §5.7 row 3 flicker | Present M6; D1 and D2 required. Preserve every-run/every-level coverage in the runner. |
| §1.3(d) measured margins, §5.7 row 2 | Present M6; accepted. |
| §1.3(d) design-side margins, §3.2 | Not allocated by either packet list; assign explicitly to final margin-report assembly. |
| §1.3(e) TC contrast | Present numerical function; correct D3 and declare runner object/job coverage. |
| §1.3(f), full evaluator outputs at θ = 0.10 and 0.30 | May be deferred to the second reports module; they must not replace or rescue the scored result. |
| §1.3(g), §5.7 row 5 skeleton boundary | May be deferred; use all 40 seeds and their unconditional recorded tails, including zeros after extinction. |
| §1.3(h), §5.7 row 6 component coverage | May be deferred; preserve both sides' component counts, resolution flags, and per-component distances. |
| §1.2′ and §5.7 row 4 fidelity comparisons and uncertainty | May be deferred; include local m, matched-object/floor closure comparisons, compatible-resample λ* ranges and their counts, persistence shifts/references, and declared unavailable cases. |

**Two missing assignments need attention.** The W-specific flicker reference is part of the report currently being built and should be supplied with it under D2. The design-side margin summaries need an explicit assembly owner, but need not be added to the pure map-statistic API.

For the design side, the canonical identity record already carries TD core count, perimeter, components, and geometric clearance. It does not contain every §3.2 summary column: the 10–90% base-step band count, band/core, and largest neighboring base step still need to be included in the report's coverage. [C §1.3(d) and §3.2; ID lines 197–203.]

The deferred fidelity/persistence work must also respect the placed records: reports stating T0's outcome cite I001, and a closure that does not converge produces unavailable comparator-dependent items for the actual affected arm/level. D001's measured examples do not license a blanket claim that all unmeasured arms fail. [I001 line 44; D001 lines 22–25.]

P's explanation that all five deferred groups need another θ or another evaluator map is broader than necessary: persistence assembly primarily joins existing records. That wording does not undermine the split itself. Deferral must remain explicit, and a missing mandatory report must prevent a claim of complete reporting without becoming a B or D failure. [C §5.7 opening; P §1.]

## 9. Q8 — the no-run disclosure and what remains unverified

The synthetic-map and constructed-sequence approach is appropriate for these numerical component tests. It is more restrictive than the specific prohibition on reusing or exposing probe output, and it should be described as the chosen test boundary rather than as a universal ban on testing record ingestion.

The governing restrictions have distinct purposes:

1. The probe's provenance and boundary exposure remain as disclosed. Probe observations cannot become calibration, qualification, canonical, or gate observations by relabeling; the probe array archive is held closed for boundary purposes. [C §1.0, lines 57–65; FR §5, line 69.]
2. Scientific and stage jobs require the authorizations of §8 and the master-governance record. A module-build review does not authorize such a job or permit previewing a stage's master. [C §8; MR points 6–8.]

Neither statement forbids a constructed binary sequence, a fabricated record parser test, or every isolated synthetic code check. PP §7 itself distinguishes its flat-array reduction test and synthetic window/report tests from terrain runs. [PP lines 103–104.]

This review used only source inspection, closed-form geometry/constants, constructed arrays, and the supplied synthetic tests. No lattice-rule run was made, no stage master was generated, and no probe or canonical run output was used. Accordingly, the review does not certify the path from complete run records to a persisted report. The future runner/integration review must establish that path, including complete seeds, record parsing, all-width consistency, canonical arrays, object/arm/level identity, and output coverage.

## 10. Q9 — evidence, limitations, and closure requirements

### Independently executed verification

| Check | Result |
|---|---|
| Archive and manifest verification | Supplied archive digest matched; 78/78 payload digests matched; no missing, extra payload, or duplicate file paths. |
| Supplied M6 test file | **22 passed** in 6.98 seconds; exit code 0. |
| Runtime for the supplied test execution | Python 3.12.14; NumPy 2.3.5; SciPy 1.17.0; pytest 9.2.0, Linux x86_64. |
| Independent bin construction | 29 structures matched. |
| Independent exact constancy arithmetic | 12 fixtures matched direct-centered rational references. |
| Exact margin predicates | All 1,080,003 comparisons matched. |
| Complete periodic margin fixtures | 14 matched an independently indexed neighborhood sum. |
| Single-width tuple realizability | 1,024 sequences and 484 candidate tuples; exactly 92 realizable/accepted tuples, no discrepancy. |
| Cross-width adversarial records | Main counterexample and six targeted cases accepted by the submitted module, establishing D1. |
| Existing supplied positive fixture | Its accepted W=1-only mutation contradicted W=10 and W=100, as detailed under D1. |
| TC geometry | Canonical masks equaled the direct probe-source formula; shifted/fabricated equal-cardinality arrays were accepted, establishing D3's wording defect. |
| Flicker report fields on valid input | Required W-specific references absent, establishing D2. |
| Original packet bytes after verification | All 78 extracted payload files and the manifest remained byte-identical to the archive. |

The test command was run from the extracted `flights/mfa_fidelity/instrument` directory:

```bash
python -B -m pytest tests/test_f9_m6.py -v -p no:cacheprovider
```

The available runtime initially lacked pytest; it was installed into an isolated review-dependency directory. No instrument or test source was edited. The run emitted one third-party pytest-plugin deprecation warning, not a packet test failure.

### Supplied evidence kept distinct from independent execution

L1's M6 log reports 22 passes in 6.05 seconds. L1's combined log reports 272 passes in 790.31 seconds. Its mutation log reports 22 of 23 mutations caught. Those records were inspected; the combined suite and mutation script were not rerun by L2 in this review. Their stated results are therefore L1 evidence, not additional L2 executions. [P §5 and the three corresponding manifest-listed logs.]

The uncaught mutation restricts the censor count to defined records. Its survival is expected because a valid undefined record cannot be censored. It is not a missing discriminating test. Conversely, passing all 22 supplied tests does not close D1 or D2: the suite lacks the nesting checks, includes the impossible positive, and does not assert the inherited floor fields. [Mutation script lines 17–18; TEST lines 471–522; R lines 265–288.]

The exact arithmetic conclusions apply to the declared 40-seed, 100×100, 1,000-tick domain. The checks are not a qualification of the reporting runner or a comparison of actual report bytes across canonical platforms. No scientific endpoint follows from them.

### What is needed for a sound resubmission

1. Implement D1's nested-width validation in the new reports module, preserve valid common-sequence cases, and replace the impossible positive test.
2. Implement D2's three correctly labeled W-specific references, with tests and declared identity coverage.
3. Correct M6-8's authentication claim; retain the clear runner obligation to bind canonical TC u.
4. Reconcile M6-9's reading identifiers, include null in M6-10, and cover flicker in the plain-data test under an explicitly stated representation policy.
5. Assign design-side margin reporting and record the intended TC object/job coverage. The second reports module may remain deferred as stated in §8.
6. Return updated source/test/declaration identities and evidence for the contained changes. The submitted frozen contract and previously placed modules need no change to perform these repairs.

## Appendix R — runnable reproduction of the blocking cases and TC claim

Save the following block as `reproduce_m6_findings.py` and run it against the extracted instrument directory:

```bash
python -B reproduce_m6_findings.py /path/to/extracted/flights/mfa_fidelity/instrument
```

It uses constructed records, TC's formula, and rule constants. It neither runs the lattice nor reads probe output. Against this round-1 archive it reports the impossible-stack acceptance and all six targeted acceptances as true, floor-reference presence as false, and the TC ratios as 10/1 and 2031337/212332. These outputs describe the submitted implementation, not the required behavior after repair.

```python
"""L2 synthetic reproducer for Flight 9 M6 round 1.

Run: python -B reproduce_m6_findings.py PATH_TO_EXTRACTED_INSTRUMENT
No lattice dynamics, master, or probe-output file is used.
This reports the submitted module's behavior; it does not alter the module.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import dynamics as D
from mfa_instrument.f9 import reports as R
from mfa_instrument.f9 import terrain as T

SHAPE = (40, 100, 100)


def record(values):
    a, r, first, last = values
    return {
        "A": np.full(SHAPE, a, dtype=np.int64),
        "R0": np.full(SHAPE, r, dtype=np.int64),
        "first": np.full(SHAPE, first, dtype=np.bool_),
        "last": np.full(SHAPE, last, dtype=np.bool_),
    }


def accepted(tuples):
    try:
        result = R.flicker({w: record(v) for w, v in tuples.items()})
        return True, result
    except R.F9ReportError as exc:
        return False, str(exc)


out = {"declaration_sha256": R.verify_reports_declaration()}
bad = {
    1: (0, 1, False, False),
    10: (100, 0, True, True),
    100: (10, 0, True, True),
}
ok, result = accepted(bad)
out["D1_impossible_stack_accepted"] = ok
if ok:
    out["D1_low_occupancy_band"] = result["bands"][0]

# Five cases isolate individual missing predicates. The inactive-segment
# increase also violates the active-segment condition, necessarily so when
# both endpoint implications hold.
cases = {
    "coarse_A_exceeds_fine_A": ((10, 1, True, False), (11, 1, True, False)),
    "fine_A_exceeds_10_times_coarse_A": ((111, 1, True, False), (11, 1, True, False)),
    "coarse_R0_exceeds_fine_R0": ((20, 1, True, False), (20, 2, True, False)),
    "coarse_Ra_exceeds_fine_Ra": ((20, 2, False, False), (20, 2, True, False)),
    "first_endpoint_implication_fails": ((20, 1, True, False), (20, 1, False, True)),
    "last_endpoint_implication_fails": ((20, 1, False, True), (20, 1, True, False)),
}
out["D1_targeted_cases_accepted"] = {
    name: accepted({1: fine, 10: coarse, 100: (10, 0, True, True)})[0]
    for name, (fine, coarse) in cases.items()
}

# This stack is realizable: no cell is ever active at any of the 1,000 ticks.
valid = {w: record((0, 1, False, False)) for w in (1, 10, 100)}
rep = R.flicker(valid)
out["D2_flicker_top_level_keys"] = list(rep)
out["D2_flicker_per_window_keys"] = list(rep["bands"][0]["windows"][1])
out["D2_floor_reference_present"] = "floor" in json.dumps(rep).lower()
pi1 = D.stationary_pi1(C.F9_ETA0)
a = 1.0 - math.exp(-C.F9_ETA0 * C.F9_DT)
out["D2_analytic_floor_window_occupancy"] = {
    w: 1.0 - (1.0 - pi1) * (1.0 - a) ** (w - 1)
    for w in (1, 10, 100)
}

u = T.bases("TC")[1]
inside, outside = R.tc_patch_sets(u)
shifted = np.roll(u, 1, axis=0)
shifted_inside, shifted_outside = R.tc_patch_sets(shifted)
counts = np.zeros(SHAPE, dtype=np.int64)
counts[:, inside] = 1000
counts[:, outside] = 100
out["D3_shifted_u_accepted"] = True
out["D3_mask_symmetric_differences"] = [
    int(np.count_nonzero(inside != shifted_inside)),
    int(np.count_nonzero(outside != shifted_outside)),
]
out["D3_correct_ratio"] = R.suppression_contrast(counts, u)["inside_over_outside"]
out["D3_shifted_ratio"] = R.suppression_contrast(counts, shifted)["inside_over_outside"]
out["schema_empty_quantiles"] = [rep["bands"][1]["windows"][w]["median"] for w in (1, 10, 100)]
out["schema_json_roundtrip_preserves_python_keys"] = json.loads(json.dumps(rep)) == rep

print(json.dumps(out, indent=2))
```

FINAL VERDICT: NOT SOUND
