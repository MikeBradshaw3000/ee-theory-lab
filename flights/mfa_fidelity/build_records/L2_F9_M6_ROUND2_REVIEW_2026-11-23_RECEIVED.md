| Receipt item | Expected / reference | Independently verified result |
|---|---|---|
| Archive | `f9_m6_build_round2_L2.zip` | Same archive |
| Archive SHA-256 | `e9271469bbc10d90e21c87cf3a9f87c1ea05d2fcf3c621e70ad683e569e50f73` | `e9271469bbc10d90e21c87cf3a9f87c1ea05d2fcf3c621e70ad683e569e50f73` — MATCH |
| Files listed in MANIFEST.txt | 89 | 89 — MATCH |
| Archive regular files | 89 payload files plus MANIFEST.txt | 90 — MATCH |
| Payload digests | Every listed file must match | 89/89 MATCH; zero mismatches |
| Missing / unlisted payload files | 0 / 0 | 0 / 0 |
| Duplicate manifest / archive file paths | 0 / 0 | 0 / 0 |
| MANIFEST.txt SHA-256 | No supplied reference; not self-listed | `b635251842f0f8eb45bbe9761962694be0667098cca4945bff61fa69be584942` |
| Received round-1 review SHA-256 | `17bf871af75e5aa96a3b67662740b177f77ecfc749e51847f26a5253e6e7e979` | MATCH |
| Receipt gate | Review only after Mike’s execute | Receipt delivered first; execute received before review |
| End-of-review preservation | Original packet bytes retained | All 89 payload files and MANIFEST.txt unchanged |

| # | Archive-relative path | Computed full SHA-256 | Against MANIFEST.txt |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M6_ROUND2_RESPONSE_2026-11-23.md` | `83c8439ceedce2ed64c2f8e5371cf1c435a8604cae3dc073e35673689470d818` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/reports.py` | `f42f93c586288ee14ee11dfe8e2430e544e81529a2eaba17e73b0bf4345a92de` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/tests/test_f9_m6.py` | `74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56` | MATCH |
| 4 | `flights/mfa_fidelity/build_records/L2_F9_M6_ROUND1_REVIEW_2026-11-23_RECEIVED.md` | `17bf871af75e5aa96a3b67662740b177f77ecfc749e51847f26a5253e6e7e979` | MATCH |
| 5 | `flights/mfa_fidelity/build_records/f9_m6_module_container_round2_2026-11-23.txt` | `e987894634c8e59c5dbea77693a7f42e8c8e0bce98a4650533faa836c6aafd8b` | MATCH |
| 6 | `flights/mfa_fidelity/build_records/f9_m1_to_m6_container_round2_2026-11-23.txt` | `f312999e67c6f186fbafa61cc472f1089f519f4d6bf24704cd492e2f08015f5c` | MATCH |
| 7 | `flights/mfa_fidelity/build_records/l2_m6_round1_reproduce.py` | `c0e7e0977d0313c6936bae9576301fe3a14a81eb309e31bc2b5804c134f93bb0` | MATCH |
| 8 | `flights/mfa_fidelity/build_records/f9_m6_l2_round1_reproduce_on_round1_2026-11-23.txt` | `07acb9795ce812301ab920de9b9c7b6aa9f4c01cf655f40f6976c2b2feb548f1` | MATCH |
| 9 | `flights/mfa_fidelity/build_records/f9_m6_l2_round1_reproduce_on_round2_2026-11-23.txt` | `5b5ec79b62253c46a0574a73f305607d10ba605b33239205b91ad82c10f5a647` | MATCH |
| 10 | `flights/mfa_fidelity/build_records/f9_m6_mutation_check.py` | `b86212cd39140d5655d93c6482312a6ea359a7deb7352d26cc08fcd14c5cd55a` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/f9_m6_mutation_check_round2_2026-11-23.txt` | `ac6c7201abdc7657fb8bb4e996ab6aebd00bc5a2d3df81c40701b553942f0511` | MATCH |
| 12 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M6_BUILD_PACKET_2026-11-23.md` | `4bae93832659dc52a120bb1256f3408fa06392be457809819373cc03c2f8b81e` | MATCH |
| 13 | `flights/mfa_fidelity/build_records/f9_m6_module_container_2026-11-23.txt` | `5f75f11ce965001dfccf8bbb0774dc562a62d1e98a302ef8182e1f7778d5a607` | MATCH |
| 14 | `flights/mfa_fidelity/build_records/f9_m1_to_m6_container_2026-11-23.txt` | `75df38495df48377d1975e138a4ebab5e3686c96a1b0c2f8225732936310f767` | MATCH |
| 15 | `flights/mfa_fidelity/build_records/f9_m6_mutation_check_2026-11-23.txt` | `0aa0e268cd656ce816a63757c17a07f456b4f8a399d25d3c6738d835f7947771` | MATCH |
| 16 | `packet_only/round1/reports.py` | `6e886549559b8ec2724c3a1539f07d8198f712285d31043f3850f17c9c02b146` | MATCH |
| 17 | `packet_only/round1/test_f9_m6.py` | `b4cae42d19f29d1ec8728d13a2d69cff4428ff005df10aac4a30d33bf52da8c5` | MATCH |
| 18 | `packet_only/round1/f9_m6_mutation_check.py` | `9eef3e2d968a80830c62491572f2229ba707dc0db0241dace9814d631842e55c` | MATCH |
| 19 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 20 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 21 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 22 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 23 | `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | `473a2a165fd5cb4e38ddb064dc14c24880af8998a21b9ffad1aa7c065551016c` | MATCH |
| 24 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |
| 25 | `flights/mfa_fidelity/rulings/F9_MASTER_RULING_RECORD.md` | `02b98378057e776769b48150059a2b9323737fd5ab437f907ae4d62c3fc27b75` | MATCH |
| 26 | `flights/mfa_fidelity/rulings/F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` | `b38a4ff6eaa3e2118a9ae723cff63a3336fb178a35932071c3dc43c4478c50a6` | MATCH |
| 27 | `flights/mfa_fidelity/rulings/F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` | `bc5fac1d53fd57ac0923fb759e465e8783389d92cb1188e297c185c5b91ac78d` | MATCH |
| 28 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 29 | `flights/mfa_fidelity/build_records/F9_M5_PLACEMENT_NOTE_2026-11-18.md` | `41dfe671983e295f01696a9b1d9c7fb20f0006be6e695b0d5a42ebd647de6e17` | MATCH |
| 30 | `flights/mfa_fidelity/build_records/F9_TEST_REPAIR_PLACEMENT_NOTE_2026-11-18.md` | `ba35214dbb2d1e23d0d7931fb96b571aaf2c05b42f1320a48d6a8b52e9045d6b` | MATCH |
| 31 | `flights/mfa_fidelity/build_records/F9_GOVERNANCE_RECORDS_PLACEMENT_NOTE_2026-11-20.md` | `5aecde9c514b12000005169ed889f1daa01c935b377d482b654ee72724df9c20` | MATCH |
| 32 | `flights/mfa_fidelity/build_records/L2_F9_GOVERNANCE_RECORDS_ROUND2_REVIEW_2026-11-20_RECEIVED.md` | `4ac4e07b5e40a1cf41d624878467d6be0303ab32cb5dd341d1674709f8e5b92d` | MATCH |
| 33 | `flights/mfa_fidelity/build_records/f9_m1_to_m5_canonical_2026-11-18.txt` | `1f79b9aa1160c7cb7f7f96ef6e54f30028409b170a66474459b847e31dd88cba` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `e505cd6bd302c1e005b37f4bc4ad364300b83fd4ab40bb73ac6ef18c0084073a` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/tests/test_f9_m3.py` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/tests/test_f9_m5.py` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py` | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 72 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/t0.py` | `a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472` | MATCH |
| 73 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 74 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 75 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 76 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 77 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 78 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 79 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 80 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 81 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 82 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 83 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 84 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 85 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 86 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 87 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 88 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 89 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 M6 build review, round 2

**Date:** 2026-11-23. **Reviewer role:** L2, adversarial module-build review. **Decision authority:** Mike.

**Reviewed archive:** `f9_m6_build_round2_L2.zip`.

**Archive SHA-256:** `e9271469bbc10d90e21c87cf3a9f87c1ea05d2fcf3c621e70ad683e569e50f73`.

**Assessment: SOUND within the submitted map-statistic module boundary.** The specified repairs to D1, D2 and D3 are complete. The eight readings are aligned, the record representation is accurately described, and the previously unassigned design-side margin reporting now has an explicit owner. No numerical regression was found in the calculations accepted in round 1.

There is an important limit to this conclusion: **an accepted flicker stack is not proof that one tick sequence could produce all its summaries.** I constructed an impossible stack that passes the now-complete set of declared necessary checks. Section 2 gives the counterexample and explains why it does not reopen D1's specific parser-parity repair. It must remain visible in the runner's validation boundary.

This disposition reviews the submitted implementation, tests and declarations. It does not determine a Flight 9 scientific endpoint, qualify the reporting runner, authorize placement, or authorize a stage run.

## 1. Review basis, identities and scope

The receipt preceding this review records a matching archive digest and 89 matching payload digests. Receipt was delivered before substantive review; Mike then supplied `execute`. The round-2 response was the first substantive packet document read.

The packet states the repository pin as `67aa10ca5958e0c07855441fbeab4a71a66e51f5`. I verified the supplied bytes and their internal lineage; I did not independently attest the remote repository's current HEAD. The frozen contract remains `FLIGHT_9_CONTRACT_v0_7.md`, SHA-256 `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`. Its retained draft/proposed markers are governed by the Freeze Record; they do not reopen the ratified report schemas. [P2 opening; FR §§1, 3.2 item 17.]

### Source references

Paths below are relative to `flights/mfa_fidelity/` inside this archive, except the three explicitly identified `packet_only/round1/` files. Bracketed citations refer to these exact sources; line numbers refer to the submitted bytes. Their full digests are in the receipt.

| Key | Source |
|---|---|
| P2 | `build_records/L1_TO_L2_F9_M6_ROUND2_RESPONSE_2026-11-23.md` |
| P1 | `build_records/L1_TO_L2_F9_M6_BUILD_PACKET_2026-11-23.md` |
| L2R1 | `build_records/L2_F9_M6_ROUND1_REVIEW_2026-11-23_RECEIVED.md` |
| C | `contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` |
| FR | `contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` |
| PP | `design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` |
| R | `instrument/mfa_instrument/f9/reports.py` |
| TEST | `instrument/tests/test_f9_m6.py` |
| D | `instrument/mfa_instrument/f9/dynamics.py` |
| ID | `instrument/mfa_instrument/f9/identities.py` |
| I001 | `rulings/F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` |
| D001 | `rulings/F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` |
| MUT | `build_records/f9_m6_mutation_check.py` |
| REPRO | `build_records/l2_m6_round1_reproduce.py` |

The received round-1 review has the supplied identity `17bf871af75e5aa96a3b67662740b177f77ecfc749e51847f26a5253e6e7e979`. Its receipt lists 78 payload paths. All 78 occur in the new archive: 75 have unchanged digests; the three changed paths are `reports.py`, `test_f9_m6.py` and the mutation script. The retained copies under `packet_only/round1/` match the three old digests exactly. This is a comparison against the authenticated received receipt and retained source copies, not a claim to have reread the entire original round-1 archive.

| Identity | Round 1 | Round 2 |
|---|---|---|
| Reports source SHA-256 | `6e886549559b8ec2724c3a1539f07d8198f712285d31043f3850f17c9c02b146` | `f42f93c586288ee14ee11dfe8e2430e544e81529a2eaba17e73b0bf4345a92de` |
| M6 test source SHA-256 | `b4cae42d19f29d1ec8728d13a2d69cff4428ff005df10aac4a30d33bf52da8c5` | `74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56` |
| Reports declaration SHA-256 | `56bc9a108afdc347bcdae98f254de7f3072e091a46d607ed40a118ae887945d2` | `169a8d62bb568388729d88f7cd80c4750fbe7cdb7955a67285fea490607aa1d9` |

Both declaration hashes were independently recomputed over the declaration representation and matched their literals and verifier returns. Every existing declaration entry is unchanged. The three additions are `flicker_record_checks`, `flicker_floor_references` and `flicker_floor_meaning`. [R lines 133–170; retained round-1 source.]

## 2. Q1 / D1 — nested-width validation

**Disposition: CLOSED for the specified repair.** The implementation now applies exactly the placed parser's available nested-width predicates, on every required pair, before any band or statistic is formed. There is no missing or added nested-width predicate relative to `dynamics._check_consistency`. [R lines 302–314, 329–345; D lines 450–458.]

For each pair \((W_s,W_l)\in\{(1,10),(1,100),(10,100)\}\), with \(k=W_l/W_s\) and \(R_a=R_0-1+\mathrm{first}+\mathrm{last}\), it checks:

| Relation | Implementation |
|---|---|
| \(A_l\leq A_s\) | Rejects a larger active-window count at the coarser width. |
| \(A_s\leq kA_l\) | Rejects more fine active windows than the coarse windows can contain. |
| \(R_{0,l}\leq R_{0,s}\) | Rejects increased inactive-segment count. |
| \(R_{a,l}\leq R_{a,s}\) | Rejects increased active-segment count. |
| \(\mathrm{first}_s\Rightarrow\mathrm{first}_l\) | Preserves activity of the first nested window. |
| \(\mathrm{last}_s\Rightarrow\mathrm{last}_l\) | Preserves activity of the last nested window. |

The checks cover every seed and cell. Input bounds are still tested in the input integer type before conversion to int64. Accepted counts are at most 1,000, so the subsequent nesting arithmetic is safely within int64. The single-width alternating-segment relations remain in place, and a failed check raises `F9ReportError` rather than a scientific outcome. [R lines 277–314.]

### Reproduction of the previous failures

I verified that REPRO is a byte-for-byte extraction of Appendix R from L2R1 and executed it against both retained round-1 source and submitted round-2 source:

| Earlier case | Round 1 | Round 2 |
|---|---|---|
| Never active at W=1, always active at W=10 and W=100 | Accepted | Refused |
| Coarse A exceeds fine A | Accepted | Refused |
| Fine A exceeds k times coarse A | Accepted | Refused |
| Coarse R₀ exceeds fine R₀ | Accepted | Refused |
| Coarse Rₐ exceeds fine Rₐ | Accepted | Refused |
| First-end implication violated | Accepted | Refused |
| Last-end implication violated | Accepted | Refused |

The old positive that changed only W=1 to `(2,1,True,True)` beside incompatible coarser records is now a negative. Its replacement constructs a common sequence active only at the first and last tick; it legitimately produces `(2,1,True,True)` at all three widths. [TEST lines 616–620.]

The packet's separate accepted fixture is also valid: ticks 0–199 and 900–904 active, all other ticks inactive, produce `(205,2,True,False)` at W=1, `(21,2,True,False)` at W=10 and `(3,1,True,True)` at W=100. It differs from the sequence used to introduce the fixture, but it is realizable. [TEST lines 506–528.]

For an independent positive check, I reduced binary histories directly by window OR and transition counting, without using the placed `_Windows` accumulator. The input comprised 5,136 constructed histories, of which 5,122 were distinct, distributed across 400,000 cell-seed records at each width. It included heterogeneous random histories, all 1,024 ten-bit patterns expanded to ticks, and endpoint/window-boundary constructions. The production validator accepted the complete stack. No false refusal was found.

### The stronger question: can an impossible stack still pass?

**Yes.** The following uniform stack passes both `_check_windows` and the full `flicker` function:

| W | A | R₀ | First | Last |
|---:|---:|---:|---|---|
| 1 | 20 | 1 | True | False |
| 10 | 20 | 1 | True | False |
| 100 | 2 | 1 | True | False |

Every listed necessary relation holds. Nevertheless, the W=1 tuple uniquely fixes twenty active ticks followed by 980 inactive ticks: it starts active, ends inactive, and has exactly one active segment. Its actual coarsenings are:

| W | Tuple forced by that fine sequence |
|---:|---|
| 1 | `(20,1,True,False)` |
| 10 | `(2,1,True,False)` |
| 100 | `(1,1,True,False)` |

The submitted impossible stack instead reports medians of 980, 800 and 800 ticks. The true prefix sequence reports 980, 980 and 900 ticks. The difference is observable; this is not merely a provenance mismatch between two realizable histories. Appendix A supplies a runnable reproduction.

**Why this does not reopen D1:** the round-1 required repair was explicit parity with the placed parser's available relations, accompanied by a necessary-not-sufficient boundary. Round 2 implements that repair and states that boundary. Neither the placed parser nor this API promises a complete joint-realizability solver. The accepted counterexample therefore limits the meaning of acceptance; it does not violate the repaired predicate contract. [L2R1 §2, D1 “Scope of this repair”; P2 §3, M6-6; R lines 53–61, 277–280; D lines 397–415.]

A sound placement description must accordingly say that these **specified consistency checks** pass. It must not say that passing proves a common trajectory or authenticates a run. The runner still owns complete-record parsing, count-series relations, provenance, seed/arm/level/object membership and canonical-array binding. No new solver or edit to a placed module is required by this review.

### The two redundant checks

The mutation script's two nesting equivalences are correct. With both endpoint implications,

\[
R_{a,l}-R_{a,s}
=(R_{0,l}-R_{0,s})+(f_l-f_s)+(\ell_l-\ell_s),
\]

and the final two terms are nonnegative. Active-segment monotonicity therefore already implies inactive-segment monotonicity. Independently, all 8,464 ordered pairs of the 92 realizable length-ten tuples were examined; none of the 2,562 pairs satisfying the antecedent conditions violated R₀ monotonicity.

The direct (1,100) relations are implied by the (1,10) and (10,100) relations: the count bounds compose with factors 10×10, and segment monotonicity and endpoint implications are transitive. Keeping both redundant checks preserves literal parser parity. Their isolated removal cannot require a discriminating failure.

## 3. Q2 / D2 — floor references

**Disposition: CLOSED. Top-level placement is ACCEPTABLE.**

PP §6 point 3 requires the flicker distribution with its W-specific floor reference; C §2.11 incorporates that declaration unchanged. The repaired output carries a single `floor_reference` object with an explicit `meaning` and a `by_window` mapping. Each reference is unambiguously associated with W. Neither source requires repeating the same reference in every occupancy-band entry. [PP lines 90–98; C line 131; R lines 351–355.]

Using \(a=0.01\), \(q=1-e^{-0.2}\), and \(\pi_1=a/(a+q)\), I independently evaluated

\[
\Pr(\text{any activity in }W\text{ ticks})
=1-(1-\pi_1)(1-a)^{W-1}
\]

with 70-digit Decimal arithmetic.

| W | Registered literal | Independent value, abbreviated | Submitted float |
|---:|---|---:|---:|
| 1 | `"0.0523"` | 0.052282320137314455… | 0.052282320137314486 |
| 10 | `"0.1342"` | 0.134243553700257133… | 0.1342435537002572 |
| 100 | `"0.6496"` | 0.649600685630129514… | 0.6496006856301298 |

The four-place literals and Appendix A.3's six-place values agree. The binary-float differences from the high-precision reference are below \(4\times10^{-16}\) in this runtime. The literals remain the registered references; these libm-derived floats are not newly certified as bit-identical across platforms. [C line 589; R lines 124–126, 157–176.]

The meaning string correctly identifies **active-window occupancy probability**, distinguishes it from inactive-segment duration in ticks, and says it enters no band, statistic or count. Both mapping and meaning enter the declaration identity. The verifier checks the three widths, W=1's agreement with the margin literal, and four-place analytic agreement. [R lines 133–170.]

Independent all-active and all-inactive inputs retained all three references, including reports with three empty occupancy bands and reports with no defined duration anywhere. No floor field was added inside a band/window entry. The supplied tests check the same placement and associations against explicitly written constants. [TEST lines 423–463.]

## 4. Q3 / D3 — TC geometry and authentication wording

**Disposition: CLOSED.** The revised wording describes the actual guarantee: finite float64 geometry, the two threshold-defined masks and their cardinalities. It expressly says that another array, including a one-cell shift of TC's u, can pass. The caller must supply TC's base u from the authenticated identity bundle; the runner must establish that binding. The error message no longer claims to identify every non-TC array. [R lines 68–77, 359–367; P2 §2, D3 and §3, M6-8.]

The calculation itself is unchanged. Independent reproduction on the round-1 synthetic count construction gave:

| Check | Result |
|---|---|
| Canonical inside/outside cardinalities | 545 / 7,843 |
| Membership changes after shifting u one cell | 54 inside / 102 outside |
| Ratio with canonical u | `10/1` |
| Ratio with shifted u | `2031337/212332`, approximately 9.5667963378 |

Shifted-u acceptance is now an explicit limitation test rather than a contradiction of the declared guarantee. A cardinality test cannot discharge the runner's canonical-array obligation. Recomputing terrain geometry inside this pure statistic function is not required. [TEST lines 651–668; R lines 370–381; L2R1 §2, D3.]

## 5. Q4 — declarations and eight readings

M6-1 through M6-5 retain their earlier dispositions. The source comparison and valid-input regression checks in §6 support carrying those acceptances forward. The five restated declarations are:

| Declaration | Disposition | Basis |
|---|---|---|
| M6-6 — flicker record checks | **ACCEPTABLE** | Correct per-width and nested-width parser relations, all three pairs, bounds before conversion, and an explicit necessary-not-sufficient scope. The counterexample in §2 is part of that scope assessment. |
| M6-7 — flicker report | **ACCEPTABLE** | Bands, counts, censoring, statistic and quantiles are preserved; the missing three references and their meaning are now supplied. |
| M6-8 — TC sets | **ACCEPTABLE** | Geometry and exact means are preserved; cardinality sanity checks and authenticated-u responsibility are accurately separated. |
| M6-9 — eight readings | **ACCEPTABLE** | P2 §5 and R's numbered docstring now use the same eight items in the same order. |
| M6-10 — records | **ACCEPTABLE** | Includes None, discloses integer W keys and JSON string conversion, and identifies these objects as components of eventual bound report records. |

These dispositions concern the submitted declarations; they do not turn an L2 assessment into Mike's ratification. [P2 §§3–5; R lines 14–21, 53–100, 277–381.]

| Reading | Disposition | Reason |
|---|---|---|
| 1. Both counts and their ratio at cut 0.20 | **ACCEPTABLE** | Includes the mandatory count and transparent descriptive companions, with no change to a criterion. |
| 2. Linear interpolation between order statistics | **ACCEPTABLE** | A declared deterministic convention where §5.7 specifies none. The revised wording correctly treats §5.5 as an analogous convention, not an instruction imposing it here. |
| 3. Censor count among all band records | **ACCEPTABLE** | A valid undefined record is all-active and cannot be censored, so counting among defined records gives the same count. |
| 4. Censored defined records included in quantiles | **ACCEPTABLE** | Follows §5.7's domain of all records with a defined value. |
| 5. No defined records means None quantiles | **ACCEPTABLE** | Records absence without inventing a duration; counts distinguish an empty band from an all-active one. |
| 6. Ties are equal stored ω values without tolerance | **ACCEPTABLE** | Uses the comparison array as M1 stores it. The misleading “bit-equal” wording is withdrawn. |
| 7. TC coverage and hosting | **ACCEPTABLE** | P2 records Mike's choice: realization runs, both TC arms, every level; a named component of one existing step-15 report. The function remains object-neutral. |
| 8. Cell count beside each bin's ω range | **ACCEPTABLE** | Makes the partition inspectable without changing the statistic or its status. |

[Sources for readings: P2 §§4–5; R lines 79–100, 196–220, 258–273, 317–355; C §3.4, §5.7 and step 15; PP R-6.]

For M6-10, the new test covers flicker and None, rather than testing only the other three reports. I also independently serialized all-active and all-inactive flicker outputs with `allow_nan=False`. They contained JSON-supported values and reloaded exactly after recursive conversion of integer keys to strings. The record-kind and declaration fields were present, with no result, tier, cause, pass or verdict field. Exact Python-key preservation across JSON reload is neither claimed nor required here; the runner must declare the persisted encoding. [R lines 14–17; TEST lines 710–747.]

## 6. Q5 — preservation of accepted calculations

**No accepted numerical calculation changed.** Nine existing function ASTs are identical between the retained round-1 source and round 2: `_frac`, `seed_totals`, `_at_least`, `constancy_bins`, `_within_bin_sum_of_squares`, `constancy`, `margins`, `quartiles` and `suppression_contrast`.

The remaining edits are contained: declaration verification; stricter flicker input validation; adding the flicker floor metadata; TC docstring/error wording; and the new floor-reference helper. The existing statistical body of `flicker` is unchanged. [R lines 157–176, 196–381; retained round-1 source.]

I independently loaded both implementations and compared complete valid-input output dictionaries, removing only the changed declaration identity from each report and the newly added floor-reference object from flicker. Existing margin and TC floor fields remained in the comparisons.

| Report | Independent fixtures | Result |
|---|---:|---|
| Constancy | 24 | Exact equality |
| Measured margins | 6 | Exact equality |
| TC contrast | 6 | Exact equality |
| Flicker | 9 | Exact equality |
| **Total** | **45** | **No numerical or retained-field difference** |

Fixtures covered zero/full occupancy, spatial structure, integer random maps, repeated profiles, TC patch counts, constant/ordered/tied comparison arrays, sparse endpoints, intermediate occupancy and alternating activity. The mixed flicker fixture was built from 640 independently constructed histories and supplied 400,000 records per width. All input arrays were read-only, and their hashes remained unchanged.

The tighter rejection of malformed flicker input is an intended validation change. The additional metadata and declaration identity are intended record changes. Neither is a change to constancy, margins, the duration statistic, quantile calculation or TC's exact means.

## 7. Q6 — governance allocation and remaining integration work

The two allocation questions from round 1 are now answered in the packet by attribution to Mike's accepted recommendations. I accept those as the supplied decision record; I do not issue an alternative scientific ruling. [P2 opening and §4.]

**TC contrast:** realization runs, both TC arms, every registered level. Its numerical function is present. The runner must name its hosting component within one of the six step-15 reports and bind the supplied maps and canonical TC u. The absence of a seventh report-job name does not remove the obligation. [P2 §4 point 1; R lines 95–99; C lines 85, 415.]

**Design-side margins:** the second reports module, at margin-report assembly. That allocation expressly includes the three §3.2 columns not already carried by the identity record: 10–90% base-step band count, band/core and largest neighboring base step. Core count, perimeter, components and geometric clearance already have identity-record fields. This closes the ownership gap without adding design geometry to the present measured-map function. [P2 §4 point 2; R lines 19–21; C §3.2; ID lines 197–203.]

The following remain explicit obligations for later assembly/integration:

| Requirement | Owner or constraint carried forward |
|---|---|
| Persistence profiles, intervals, threshold and bracket | Second-module/report assembly, using the placed calculations and all typed profile cases. |
| Design-side margins | Second reports module as assigned above. |
| Full evaluator outputs at θ=0.10 and 0.30 | Deferred reports; neither replaces nor rescues the scored result. |
| Skeleton boundary | All 40 seeds, unconditional recorded tails, zeros after extinction. |
| Component coverage | Both sides' counts, resolution flags and per-component distances. |
| Fidelity comparisons and uncertainty | Complete declared comparator, resample and unavailable-state coverage. |
| T0-referenced results | Cite Interpretation 001; preserve unavailable-reference cases. |
| Closure unavailability | Report the actual affected arm/object/level; do not turn Disclosure 001's examples into a blanket result. |
| Persisted report records | Complete seed/arm/level/object identity, canonical-array binding, schema encoding and reporting completeness. |

[P2 §6; L2R1 §8; C §§1.2′, 1.3, 5.7–5.9; I001 line 44; D001 lines 22–25.]

The explanation of the split is also repaired: persistence assembly mostly joins existing records; it is the evaluator-dependent reports that need additional evaluator work. The chosen synthetic-test boundary is correctly identified as more restrictive than the particular prohibition on using probe output. The present tests establish numerical component behavior, not the full path from run records to persisted reports. [P2 §6; L2R1 §§8–9.]

### Nonblocking wording observations

Two test descriptions should be read precisely:

1. TEST line 493's broad phrase about refusing contradictory widths refers to the listed necessary relations. The impossible-prefix example in §2 shows why it should not be quoted as a universal realizability guarantee. The module and M6-6 already state the narrower guarantee correctly.
2. TEST line 456 says “no defined record anywhere” beside a loop over both all-active and all-inactive patterns. That phrase applies only to the all-active case. The executable assertions immediately below correctly give the all-inactive case 400,000 defined durations.

These are documentation precision notes, not additional blockers or requirements for another review round.

## 8. Executed evidence and its limits

### Independent execution

| Check | Result |
|---|---|
| Archive and manifest | Supplied archive hash matched; 89/89 payload digests matched; no missing, unlisted payload or duplicate paths. |
| Retained round-1 lineage | 75 unchanged common-path digests; exactly three changed common paths; all three retained old copies match L2R1's receipt. |
| Supplied M6 suite | **26 passed in 8.43 seconds**, exit code 0. |
| Runtime | Python 3.12.14; NumPy 2.3.5; SciPy 1.17.0; pytest 9.2.0; Linux. |
| Previous Appendix R | Extracted bytes matched REPRO; old failures reproduced on round 1 and repaired behavior reproduced on round 2. |
| Independent common-sequence positives | 5,136 constructions / 5,122 distinct histories; 400,000 cell-seed records per width; accepted. |
| Single-width mathematical rule | 1,024 binary sequences; 484 candidate tuples; 92 realizable tuples; no discrepancy. |
| Full-realizability limit | Impossible prefix stack accepted; full flicker medians 980/800/800 reproduced. |
| Old/new differential reports | All 45 valid fixtures matched as specified in §6; inputs unchanged. |
| Floor references | Independent high-precision calculation; all literals/widths correct; present on valid extreme cases. |
| TC wording limit | Shifted-u acceptance, membership changes and exact ratios reproduced. |
| Supplied mutation driver | **30 of 33 caught** under the driver's nonzero-pytest-exit definition; the other three are equivalent changes. |
| End-of-review preservation | All 89 original extracted payload files and MANIFEST.txt remained byte-identical to the archive. |

Pytest was installed into an isolated review-dependency directory because it was absent from the base runtime. Third-party plugin autoload was disabled. The test command, from the extracted instrument directory, was:

~~~bash
PYTHONPATH=/path/to/review_deps PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python -B -m pytest tests/test_f9_m6.py -v -p no:cacheprovider
~~~

No test or source file in the reviewed packet was changed. The mutation driver operated only on a separate disposable copy and restored that copy's reports source to the submitted digest.

The 1,024-sequence/484-tuple enumeration establishes equivalence of the **single-width mathematical rule** and binary-sequence realizability at n=10. It should not be described as 484 calls through the full reporting API: the supplied test checks the abstract predicate over all candidates and invokes the API on sampled realizable constructions. The targeted malformed-input tests and the independent production-input checks provide the separate implementation evidence. [TEST lines 531–567.]

### Mutation interpretation

The three surviving changes have the stated equivalences:

| Surviving mutation | Why it is equivalent |
|---|---|
| Count censored records only among defined records | A valid undefined record is all-active and has neither endpoint inactive. |
| Drop only coarse R₀ ≤ fine R₀ | Implied by active-segment monotonicity and the endpoint implications. |
| Skip only the direct (1,100) pair | Implied by the two adjacent-width pairs through transitivity. |

All new non-equivalent nested-width and floor-reference mutations were caught. This supports the tests' sensitivity to the repaired behaviors. The driver labels any nonzero pytest return as caught; its aggregate is not a proof of exhaustive correctness. [MUT mutation list and execution loop; mathematical checks in §2.]

### Supplied evidence distinguished from reruns

L1's round-2 M6 log reports 26 passes in 8.42 seconds; its combined M1–M6 log reports 276 passes in 963.85 seconds. Its mutation log reports 30 of 33 caught. I independently reran the M6 suite, the supplied mutation driver and the previous reproducer. **I did not rerun the combined M1–M6 suite.** Its 276-pass figure remains inspected L1 evidence, not an additional L2 execution. [P2 §7 and its three named logs.]

All independent execution used source, rule constants, closed-form terrain geometry, constructed integer maps and binary histories. No lattice-rule run, scientific stage job, stage master or probe-output access occurred. Cross-platform persisted-record equality and complete reporting-runner integration remain outside this component review.

**Closure:** D1, D2 and D3 are closed; M6-6 through M6-10 and all eight readings are acceptable. No blocking repair remains in this submitted round-2 component. The necessary-only validation limit and the later integration obligations above are part of the scope of that conclusion.

## Appendix A — reproduction of the necessary-only validation limit

Save this block as `reproduce_m6_round2_limit.py` and run it against an extracted instrument directory:

~~~bash
python -B reproduce_m6_round2_limit.py /path/to/extracted/flights/mfa_fidelity/instrument
~~~

The program checks the submitted reports-source identity, constructs summary arrays, and compares the forged stack with a directly reduced valid prefix sequence. It performs no lattice dynamics or run-record ingestion.

~~~python
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

instrument = Path(sys.argv[1]).resolve()
source = instrument / "mfa_instrument/f9/reports.py"
expected = "f42f93c586288ee14ee11dfe8e2430e544e81529a2eaba17e73b0bf4345a92de"
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
sys.path.insert(0, str(instrument))
from mfa_instrument.f9 import reports as R

WIDTHS = (1, 10, 100)
KEYS = ("A", "R0", "first", "last")
SHAPE = (40, 100, 100)


def stacked(tuples):
    return {
        w: {
            key: np.full(
                SHAPE, value,
                dtype=bool if key in ("first", "last") else np.int64
            )
            for key, value in zip(KEYS, tup)
        }
        for w, tup in zip(WIDTHS, tuples)
    }


def direct_summary(ticks, width):
    active = np.asarray(ticks, dtype=bool).reshape(-1, width).any(axis=1)
    inactive_segments = int(not active[0]) + int(
        np.count_nonzero(active[:-1] & ~active[1:])
    )
    return (
        int(active.sum()), inactive_segments,
        bool(active[0]), bool(active[-1])
    )


forged = (
    (20, 1, True, False),
    (20, 1, True, False),
    (2, 1, True, False),
)
prefix = np.arange(1000) < 20
actual = tuple(direct_summary(prefix, w) for w in WIDTHS)
assert actual == (
    (20, 1, True, False),
    (2, 1, True, False),
    (1, 1, True, False),
)
bad_report = R.flicker(stacked(forged))
good_report = R.flicker(stacked(actual))


def medians(report):
    return [report["bands"][0]["windows"][w]["median"] for w in WIDTHS]


assert medians(bad_report) == [980.0, 800.0, 800.0]
assert medians(good_report) == [980.0, 980.0, 900.0]

old_counterexample = (
    (0, 1, False, False),
    (100, 0, True, True),
    (10, 0, True, True),
)
try:
    R.flicker(stacked(old_counterexample))
except R.F9ReportError:
    old_counterexample_refused = True
else:
    old_counterexample_refused = False
assert old_counterexample_refused

print(json.dumps({
    "source_sha256": expected,
    "declaration_sha256": R.verify_reports_declaration(),
    "round1_counterexample_refused": old_counterexample_refused,
    "forged_stack_accepted": True,
    "forged_tuples": forged,
    "tuples_forced_by_the_fine_prefix": actual,
    "forged_medians": medians(bad_report),
    "actual_prefix_medians": medians(good_report),
    "floor_reference": bad_report["floor_reference"],
}, indent=2))
~~~

FINAL VERDICT: SOUND
