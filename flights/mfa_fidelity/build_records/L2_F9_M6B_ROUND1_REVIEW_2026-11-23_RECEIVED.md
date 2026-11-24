| Receipt item | Independently computed | Comparison / result |
|---|---|---|
| Archive | `f9_m6b_build_round1_L2.zip` | Received packet |
| Archive SHA-256 | `6a00972c7a753d420b6a2e3724b209355e63723051b7067cd6b0e53e3f9ebc19` | MATCH — user-supplied archive digest |
| Manifest-listed payload files | 80 | MATCH — supplied count |
| Regular files in ZIP | 81 | 80 payload files plus MANIFEST.txt |
| Missing / unlisted payload files / duplicate paths | 0 / 0 / 0 | PASS |
| MANIFEST.txt SHA-256 | `fa6b73cabd6d9c31fbe164a996399b10aa3daae22976dd19190a2883e061352b` | Computed separately; manifest does not list itself |
| Payload digests | 80 of 80 match | Each entry verified in manifest order below |
| Received source preservation | All 80 extracted payload digests still match | Checked after review execution |

| # | Manifest path | Independently computed full SHA-256 | Against MANIFEST.txt |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M6B_BUILD_PACKET_2026-11-23.md` | `a05fccac24f744c5626443c7e88415782a53cdb8cb39492593ea0916d45ca9f8` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator_reports.py` | `7978581182a64f77682facdc573c55ea2356077d6d6bddb935cbac5d13d1e393` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/tests/test_f9_m6b.py` | `697d4e2a7425af6badb2170a36ddb6b4ed600be807c8820ed64f7265ff9ad53e` | MATCH |
| 4 | `flights/mfa_fidelity/build_records/f9_m6b_module_container_2026-11-23.txt` | `7140166e35a84a918e7b518ef1709098d48223552a6ce00a785386cba7646104` | MATCH |
| 5 | `flights/mfa_fidelity/build_records/f9_m1_to_m6b_container_2026-11-23.txt` | `6f9612a7c6ee7d873b5880f5ed8619797e03f96b3819f39318ac0f5d8c27daf6` | MATCH |
| 6 | `flights/mfa_fidelity/build_records/f9_m6b_mutation_check.py` | `6b9d64e25b73ba5aee2ab5aa6648dddab341817cc5208f64c288d42cb5aa9d9e` | MATCH |
| 7 | `flights/mfa_fidelity/build_records/f9_m6b_mutation_check_2026-11-23.txt` | `fddced58f349e62a775cbd829a3ffae670c9055961bb516b8281b1847902631f` | MATCH |
| 8 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 9 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 10 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 11 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 12 | `flights/mfa_fidelity/contracts/flight9/arith/td_final.py` | `ca0076012b8bbc0e5b9e6214388aa895429cc0d9c9336376a7bfbfce41fb64fe` | MATCH |
| 13 | `flights/mfa_fidelity/design/flight9/FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` | `473a2a165fd5cb4e38ddb064dc14c24880af8998a21b9ffad1aa7c065551016c` | MATCH |
| 14 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |
| 15 | `flights/mfa_fidelity/rulings/F9_MASTER_RULING_RECORD.md` | `02b98378057e776769b48150059a2b9323737fd5ab437f907ae4d62c3fc27b75` | MATCH |
| 16 | `flights/mfa_fidelity/rulings/F9_INTERPRETATION_001_T0_HYSTERESIS_ELIGIBILITY_AND_SAMPLED_RANGE.md` | `b38a4ff6eaa3e2118a9ae723cff63a3336fb178a35932071c3dc43c4478c50a6` | MATCH |
| 17 | `flights/mfa_fidelity/rulings/F9_DISCLOSURE_001_SKELETON_CLOSURE_AT_THE_CROSSING.md` | `bc5fac1d53fd57ac0923fb759e465e8783389d92cb1188e297c185c5b91ac78d` | MATCH |
| 18 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 19 | `flights/mfa_fidelity/build_records/F9_M6_PLACEMENT_NOTE_2026-11-23.md` | `c904a70978f5b32efc0b715c3e474d7e2931f6aab36603b8898f9bc9af20382b` | MATCH |
| 20 | `flights/mfa_fidelity/build_records/L2_F9_M6_ROUND1_REVIEW_2026-11-23_RECEIVED.md` | `17bf871af75e5aa96a3b67662740b177f77ecfc749e51847f26a5253e6e7e979` | MATCH |
| 21 | `flights/mfa_fidelity/build_records/L2_F9_M6_ROUND2_REVIEW_2026-11-23_RECEIVED.md` | `2287afecc3b9eee634d0b42ffa7b6e26c2cac0f4a2e2f370888c35025c5f5bcd` | MATCH |
| 22 | `flights/mfa_fidelity/build_records/f9_m1_to_m6_canonical_2026-11-23.txt` | `4508d91c3f49346d1977fa56b53229875506c4e6788aaade07bfe86c5519b974` | MATCH |
| 23 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 24 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `e505cd6bd302c1e005b37f4bc4ad364300b83fd4ab40bb73ac6ef18c0084073a` | MATCH |
| 25 | `flights/mfa_fidelity/instrument/tests/test_f9_m3.py` | `b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6` | MATCH |
| 26 | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` | `ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b` | MATCH |
| 27 | `flights/mfa_fidelity/instrument/tests/test_f9_m5.py` | `bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8` | MATCH |
| 28 | `flights/mfa_fidelity/instrument/tests/test_f9_m6.py` | `74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56` | MATCH |
| 29 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 30 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 31 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 32 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 33 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/closure.py` | `7c20206595b7a518a149fa170a9c9f8b1e28bbfd395582b7859c72b2bfc9aef9` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `fac54ebd8de0953ce3c87d362b5a2263919af43d44eea85599f22ae73c1898d1` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/reports.py` | `f42f93c586288ee14ee11dfe8e2430e544e81529a2eaba17e73b0bf4345a92de` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/t0.py` | `a2ce76e8b3e8c5b9319414f5fdfdcf7d3341a69b05f38240ef5bc3320f63a472` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 72 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 73 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 74 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 75 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 76 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 77 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 78 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 79 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 80 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 M6 part 2 build review, round 1

**Date:** 2026-11-23. **Role:** L2, adversarial module-build reviewer. **Decision authority:** Mike.

**Reviewed archive:** `f9_m6b_build_round1_L2.zip`.

**Archive SHA-256:** `6a00972c7a753d420b6a2e3724b209355e63723051b7067cd6b0e53e3f9ebc19`.

**Scope:** evaluator-derived and assembled reports for §1.3(a), (d) design side, (f), (g), and (h). This is the new M6B round-1 review. It is not the already placed M6 part-1 round-2 review, a fidelity-summaries consultation, a qualification result, or an authorization to run a scientific stage.

## 1. Disposition and evidence boundary

**The submitted build is not sound. One contained blocking defect, D1, remains:** a constant comparison index loses the higher-priority `no eligible contour` cause when the observed map is also empty, full, or under-resolved. The new threshold orchestration copies this error from the placed evaluator; the new skeleton-boundary report calls the placed evaluator and inherits it. The frozen contract explicitly requires the opposite precedence. [C §7, L2–L4; C §6.2, row 15 and its explanatory paragraph; X lines 194–202, 256–264; E lines 424–432.]

This finding does not show a false compatible or adverse answer, a change to B or D, or a threshold-wrapper divergence from the placed evaluator at θ = 0.20. It shows a wrong mandatory unavailable cause in both implementations. The supplied equality oracle cannot detect an error shared by its two sides. [Appendix R; TEST lines 114–158.]

The threshold arithmetic, scaling argument, declared stream choices, component-distance calculations, design-margin calculations, persistence assembly, and stated division of reporting ownership are otherwise acceptable within the component boundary assessed here. The seven readings are acceptable; none authorizes departure from the frozen cause precedence. The correction belongs in the implementation and its regression tests. Mike remains the authority for accepting and recording declarations. [Sections 3–6 below.]

The archive receipt was completed before review authorization. It contains 80 manifest-listed payload files and `MANIFEST.txt`; all 80 independently computed payload digests match. The archive and manifest identities are recorded in the opening receipt tables. The repository pin `c6c21c497366d3ca71e0487127c774aacfd14ba1` is the packet's stated pin. This review verifies the supplied bytes and the included identity assertions; it does not claim an independent remote-Git comparison. [P header; TEST lines 354–386.]

### Source locator key

All source locators below are relative to the archive directory `flights/mfa_fidelity/`. Line numbers refer to the received bytes. These locators and the receipt hashes identify the evidence without depending on the review workspace.

| Key | Archive-relative source |
|---|---|
| P | `build_records/L1_TO_L2_F9_M6B_BUILD_PACKET_2026-11-23.md` |
| C | `contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` |
| FREEZE | `contracts/flight9/FLIGHT_9_FREEZE_RECORD.md`, with `FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` |
| X | `instrument/mfa_instrument/f9/evaluator_reports.py` |
| E | `instrument/mfa_instrument/f9/evaluator.py` |
| TEST | `instrument/tests/test_f9_m6b.py` |
| TEST3 | `instrument/tests/test_f9_m3.py` |
| O | `instrument/mfa_instrument/f9/outcomes.py` |
| R | `instrument/mfa_instrument/f9/streams.py` |
| T | `instrument/mfa_instrument/f9/terrain.py` |
| REPORTS | `instrument/mfa_instrument/f9/reports.py` |
| CL | `instrument/mfa_instrument/f9/closure.py` |
| TD-ARITH | `contracts/flight9/arith/td_final.py` |

The contract file retains its historical draft header; FREEZE is the authority establishing that these exact contract bytes were frozen. Its SHA-256 is `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`. The reviewed new source is `7978581182a64f77682facdc573c55ea2356077d6d6bddb935cbac5d13d1e393`, the test file is `697d4e2a7425af6badb2170a36ddb6b4ed600be807c8820ed64f7265ff9ad53e`, and the report declaration digest is `f3fe3fcf1954bb6addd18e94a793593490fef18cb77910f94dda1c25b799337e`. [Receipt; FREEZE; X line 133.]

## 2. D1 — Constant-index precedence is wrong in the copied and delegated level records

### Requirement

Contract §7 specifies level precedence from highest to lowest. Apparatus failure is L1; a constant index and its `no eligible contour` cause are L2; an empty/full observed region is L3; under-resolution is L4. The §6.2 row-15 explanation separately states that a constant index's cause does not depend on the sample and counts every other cause as an error. This is an explicit frozen requirement, not an unspecified reading for this build. [C lines 370, 372–381.]

### Received behavior

`evaluate_level_at` first asks whether the point is informative, assigning the map cause if it is not, and checks whether the family is empty only afterward. The placed `evaluate_level` has the same ordering. `skeleton_boundary` delegates to that placed function. The new module's statement that T0 receives `no eligible contour` therefore fails on the combinations below. [X lines 37–38, 195–200, 262; E lines 425–430.]

I used the actual closed-form T0 comparison array, legal integer counts with shape `(40, 100, 100)`, test key master 777, and registered κ = 1.00. Every seed has the same constructed map. No lattice dynamics or run output is involved. [Appendix R.]

| Construction | Evaluation route | Point cells / bonds | Returned index cause | Required index cause |
|---|---|---:|---|---|
| All counts zero | Placed θ=.20; skeleton θ=.20; reported θ=.10 and .30 | 0 / 0 | `no edge at theta` | `no eligible contour` |
| All counts 1,000 | Same four routes | 10,000 / 0 | `no edge at theta` | `no eligible contour` |
| Counts 1,000 only on `[10:16, 10:16]` | Placed θ=.20; skeleton θ=.20 | 60 / 32 | `below the informative minimum` | `no eligible contour` |
| Same small patch | Reported θ=.10 | 64 / 32 | `below the informative minimum` | `no eligible contour` |
| Same small patch | Reported θ=.30 | 52 / 32 | `below the informative minimum` | `no eligible contour` |

Both index entries receive the wrong cause in these examples. All return `result="not informative"` and `resampled=False`; no bootstrap is required to reproduce the problem. The small patch has an actual edge, so §1.3(g)'s phrase “where that map has an edge” does not remove this example from consideration. [Appendix R; C §1.3(g).]

The **point diagnostics are correct and should remain**. A point can truthfully describe an empty, full, or under-minimum region while an index-level record gives the higher-priority absence of any eligible comparison contour. The repair must preserve that distinction.

### Why the delivered tests pass this defect

The unavailable-state tests separate the conditions. TEST3 uses empty/full/small maps with nonconstant TA and a constant T0 family with an informative strip. TEST repeats that arrangement. Neither tests a constant family together with an empty, full, or under-minimum map. The θ=.20 equality and scaling tests also compare two implementations that share this ordering. [TEST3 lines 473–487; TEST lines 142–158, 180–183.]

### Required repair

1. **Correct the placed evaluator's per-index precedence through an explicit dependency repair.** After validating inputs, preserve the observed point record, then test `len(fam) == 0` before assigning a point's noninformative cause. Apparatus validation must still precede these returned scientific/unavailable records.
2. **Synchronize the new threshold orchestration** with that repaired ordering. Keep the θ=.20 equality requirement. The skeleton report should continue to call the corrected placed evaluator, retaining all 40 maps and the registered θ.
3. **Add discriminating regressions** for constant family × empty/full/under-minimum maps; cover the placed evaluator, θ=.20 copy, both reported thresholds, and skeleton boundary. Add a mixed constant/nonconstant-family case so each index receives its own appropriate cause. Keep tests showing that ordinary nonconstant families still receive the correct map causes.
4. **Return identified changed bytes for review**, including the dependency source/test identities and the new module/test identities. Update affected identity assertions and placement disclosures. The present packet's no-placed-edit boundary is factual; this review has changed no packet source. It cannot be preserved by leaving a known dependency error in place or by silently making the new copy differ from its oracle.

No change to θ, ε, m, the family, the support-count table, or the scientific claim grammar is required. The appropriate correction enforces the existing contract. These examples do not establish that a stage has failed qualification, because no qualification job was run here. They establish an implementation error that the contract's cause-reference rule would recognize. [C §5.5; C §6.2 row 15; C §7.]

## 3. Answers to Q1–Q3: wrapper, oracle, and non-interference

### Q1. Comparison with the placed orchestration

**No successful-record divergence at θ=.20 was found for valid inputs with the declared dependencies.** The map and level orchestration match structurally after accounting for θ threading, removal of the constructed-multiplicities argument, qualification of placed names with `E.`, the traced-edge local rename, and `n = E.N_RESAMPLES`. `declared_stream=True` is the placed default case `multiplicities=None`. A normalized AST comparison confirmed this correspondence. [X lines 160–235; E lines 158–162, 357–372, 407–464.]

There is one additional preflight difference worth stating accurately: the wrapper verifies its own declaration, including outcome and stream declarations, and explicitly validates θ. Therefore rejection behavior can differ if those declarations are damaged. That does not change a successful record under the declared module identities. The packet's shorthand “θ and the removed constructed-resamples argument” should be read with these preflight and namespace changes included. [X lines 140–156, 185–189.]

D1 is shared behavior, not a failure of the θ=.20 copying requirement. The dependency and the copy need to be repaired together.

### Q2. Scaling oracle and its coverage

**The oracle is valid as stated, subject to its valid-count bounds.** Let `B_w(c)` denote the integer box sum after aggregation with any observed or bootstrap multiplicity vector `w`. Both operations are linear, so `B_w(a*c) = a*B_w(c)`.

The common denominator is `9*40*1000 = 360000`. Consequently:

- θ=.10 on `3k` requires `3*B_w(k) >= 36000`; θ=.20 on `6k` requires `6*B_w(k) >= 72000`. These are equivalent, including ties.
- θ=.30 on `3k` requires `3*B_w(k) >= 108000`; θ=.20 on `2k` requires `2*B_w(k) >= 72000`. These are also equivalent.

The same key regenerates the same 1,000 weight rows. Equal masks enter the same downstream geometry, family search, typed draws and aggregation, establishing full-record equality. With counts in `[0,1000]` and weights summing to 40, `B <= 360000` and `1000000*B <= 3.6e11`, within signed int64. The supplied `k <= 166` restriction keeps every scaled map legal. [E lines 124–162, 382–388; X lines 160–235; TEST lines 103–132.]

The delivered TA fixture is finite coverage: one shared-family construction at the reported thresholds. It does not by itself exercise all count residues, distinct families, component structures, or mixtures of compatible, adverse and invalid draws. The separate criterion test checks arbitrary integer counts and cutoff ties; the TB differential test exercises two distinct families at θ=.20. [TEST lines 77–99, 134–160.]

An additional L2 construction used independent horizontal and vertical one-contour families, 21 nonzero seed maps, and 19 zero maps. At θ=.10 the nonzero counts were 198 and the scaled oracle used 396; at θ=.30 they were 600 and the oracle used 400. The two observed regions each had 4,800 cells and were informative. Full records matched their scaled placed-evaluator oracles, including all typed arrays, Δ arrays and level indices:

| θ | Index | n_C | n_A | n_I | Returned result / cause |
|---:|---|---:|---:|---:|---|
| .10 | P | 544 | 0 | 456 | not informative / unstable edge |
| .10 | H | 0 | 544 | 456 | not informative / unstable edge |
| .30 | P | 667 | 0 | 333 | not informative / unstable edge |
| .30 | H | 0 | 667 | 333 | not informative / unstable edge |

These synthetic families are test geometry, not replacements for the canonical TB families. The added construction exercises distinct-family and invalid-draw paths at both reported thresholds. It does not turn a finite oracle test into exhaustive contract verification. D1 demonstrates the remaining shared-error limitation.

### Q3. Can reporting alter the scored computation?

**No scored-path interference was found under the declared valid-input model.** θ is passed explicitly; the new module does not assign the scored constant. The evaluator creates a fresh local random generator from the key on each resampling call, so reporting does not advance a shared random state. Contour-cache writes insert, reorder or evict deterministic traced contours; candidate traversal and tie resolution do not depend on cache order. The new report code reads cached geometry and distances without modifying them. [X lines 160–264, 267–310; E lines 319–354, 382–388.]

In the additional two-family probe, input byte hashes, θ=200000, and regenerated multiplicity arrays remained unchanged. Scored map records agreed before reporting, after reporting with warmed families, and with newly constructed families. The supplied tests also verify the one-way dependency and source identities. [TEST lines 338–386.]

This assessment concerns computation using the declared objects. Authenticating which arm, object, bundle and run produced the inputs remains the runner's obligation, as the packet discloses.

## 4. Answers to Q4–Q7: report content

### Q4. Skeleton boundary and its stream

**The declared construction is appropriate; its delivered unavailable causes require D1's repair.** Applying the whole placed evaluator at θ=.20 to all 40 maps implements Mike's supplied reading. Extinct seeds are not dropped and the map is not renormalized by survivors. A survivor's or extinct run's supplied tail remains its input. The resulting word describes the skeleton map and does not become B. [P §2, decisions 2–3; C §1.3(g), §5.7; X lines 249–264.]

The separate skeleton key is an acceptable prospective build declaration. The contract requires a declared evaluator stream without requiring shared realization/skeleton multiplicities. Appending skeleton object code 1 specifies the choice deterministically; reusing the realization key is not required. Keep the chosen stream fixed and bind it in the eventual record. [C §5.5 step 9; X lines 249–253; TEST lines 165–171.]

`skeleton_level_key` validates a declared skeleton/all-active identity. `skeleton_boundary` itself checks the generic tuple, length and final object code; it does not revalidate every field or prove that the arrays belong to that key. This matches the explicit disclosure, and the runner must use and bind the validated identity. [P §5, disclosure 6; X lines 249–262.]

### Q5. Component coverage

**Acceptable.** Recomputing the point and fit from the level's maps is a suitable interface. It supplies observed and contour component counts, resolved counts, each component's bond count and q95 distance to the whole opposite edge, explicit no-resolved-component flags, and the identity/status of the contour actually reported. The runner must still bind these inputs to the scored level. [C §1.3(h), §5.5 steps 3, 6–7; X lines 267–310.]

The within-ε contour is the fitted minimum. Outside ε the code preserves the placed fit's descriptive least-S-examined contour and labels the limitation. When a comparison cannot be made, it retains observed counts and an unavailable reason instead of inventing quantiles against a nonexistent edge. Resolved component values agree with the evaluator's terms; unresolved components remain reported without becoming extra decision terms. [X lines 295–307; TEST lines 197–275.]

An additional construction placed six separated 3×3 fully active blocks in each seed map. At θ=.20 the post-estimator region had 126 cells, six 20-bond components and 120 bonds. Against one synthetic contour identical to that region, coverage returned six components and zero resolved components on each side, both no-resolved flags true, all 12 per-component q95 values zero, and S=0. Thus unresolved components remain present even when neither side has a resolved component.

I found no independent component-coverage defect. Its noninformative point diagnostic is not an index-level decision and is not a second instance of D1.

### Q6. Design-side margins

**Acceptable.** The fixed TD core, strict 10–90% base-step band, periodic four-neighbour maximum step, perimeter and component measures reproduce §3.2 and its arithmetic. An independent reconstruction directly from torus coordinates, centres/radii and the tanh formula gave:

| Variant | Core cells | Perimeter | Band cells | Band inside / outside core | Exact band/core | Largest base step |
|---|---:|---:|---:|---:|---|---:|
| TD-1-2 | 2,000 | 200 | 676 | 328 / 348 | 169/500 | 0.14548030289294434 |
| TD-1-4 | 2,000 | 200 | 1,376 | 620 / 756 | 86/125 | 0.07419898001067304 |
| TD-4-2 | 2,000 | 416 | 1,424 | 672 / 752 | 89/125 | 0.1424694872775394 |
| TD-4-4 | 2,000 | 416 | 2,816 | 1,168 / 1,648 | 176/125 | 0.0739669210234557 |

[C §3.2; TD-ARITH lines 15–23; X lines 314–339; independent constructed-geometry execution.]

The smallest distance of a base's S value from either band limit was approximately `0.00018145796039489848`; strict and inclusive limits therefore produce the same counts on all four declared bases. That supports the disclosed equivalent surviving mutation. [P §5, disclosure 7; mutation log; independent geometric reconstruction.]

Asserting the fixed table on every call is acceptable. These checks establish conformance to declared summary geometry; they neither test the margins hypothesis nor authenticate the entire base array. The supplied base still requires canonical-bundle binding. An invalid supplied array is an apparatus/input problem, not a scientific margin failure. [X lines 54–63, 319–332.]

### Q7. Persistence assembly

**Acceptable within §1.3(a) and §5.4.** The module iterates over the 15 declared arms, including T0.P, and recomputes the placed persistence record from survivor counts. Complete arms retain all 25 survivor counts, the 36-of-40 criterion, pointwise two-sided 95% Clopper–Pearson intervals, the four profile cases, κ̂_c/brackets where defined, descriptive nonmonotone suffixes, endpoint intervals and unavailable causes. Missing arms and missing levels are distinguished, and `complete` requires neither. [X lines 343–365; O lines 422–480; C §1.3(a), §5.4, §8.]

Additional synthetic sweeps at exactly 35 and 36 survivors exercised all-met, none-met, an ordinary crossing at 1.20 with bracket `[1.15,1.20]`, nonmonotonicity with and without a terminal suffix, and a missing TB.H level. The records retained their required meanings and incompleteness flags.

The high-initialization scope is correct; T0's low sweep belongs to the T0 record. A partial arm inherits `levels=None` from the placed persistence function, so the runner must retain the underlying available run/count records separately. The module correctly refuses to call that report complete. [O lines 444–457; C §5.8; X lines 88–89, 348–365.]

## 5. Q8 — Disposition of all declarations and readings

### M6B declarations

| Declaration | Disposition | Reason |
|---|---|---|
| M6B-1 — criterion at θ | ACCEPTABLE | Exact integer criterion, included ties, and restricted integer θ values agree with the declaration. |
| M6B-2 — orchestration copies | REQUIRES CHANGE | Copying parity holds, but the copied cause ordering violates frozen precedence. Repair D1 in the dependency and copy together. |
| M6B-3 — reported thresholds | REQUIRES CHANGE | The two thresholds and common realization stream are acceptable; their emitted level records inherit D1. |
| M6B-4 — skeleton boundary | REQUIRES CHANGE | All-40, whole-rule application and the declared key are acceptable; the delegated index cause requires D1's dependency repair. |
| M6B-5 — component coverage | ACCEPTABLE | Required counts, resolution flags, per-component distances and contour status are present where defined. |
| M6B-6 — design margins | ACCEPTABLE | Fixed geometry and table checks reproduce §3.2; authentication is explicitly left to the runner. |
| M6B-7 — persistence assembly | ACCEPTABLE | Required arms, level records and incompleteness accounting are preserved. |
| M6B-8 — records | ACCEPTABLE | Outer report kind/declaration fields and the disclosed NumPy/plain-data split fit the component interface; persisted encoding remains to be declared. |
| M6B-9 — seven readings | ACCEPTABLE | Individual classifications are below. None permits D1's cause-order departure. |

These are dispositions of the submitted declarations and implementations; they do not themselves ratify the governance record. The low-level θ evaluation helpers intentionally retain the placed evaluator's record shape; the enclosing public report carries `kind` and declaration metadata. [P §§2–4; X lines 70–89, 118–150, 238–365.]

### Seven readings

| Reading | Disposition | Build declaration or ruling | Assessment |
|---|---|---|---|
| 1. The two reported thresholds use the scored stream | ACCEPTABLE | Build declaration; Mike's acceptance is already supplied | A prospective common-resample choice under the declared-stream requirement. Freeze and bind it. |
| 2. Skeleton boundary uses steps 1–9 | ACCEPTABLE | Substantive reading supplied as Mike's ruling/acceptance | The packet records that decision. Preserve the whole evaluator and keep the resulting word descriptive. D1 remains an implementation defect. |
| 3. Skeleton has its own stream | ACCEPTABLE | Build declaration | The contract leaves the concrete stream to declaration and does not require cross-object common multiplicities. |
| 4. Every component gets its quantile | ACCEPTABLE | Build clarification of explicit content | Includes unresolved components in the report while retaining the registered component decision rule. |
| 5. Use the contour the fit reports | ACCEPTABLE | Build clarification following §5.5 step 7 | Preserve the fitted/descriptive distinction and causes when no comparison contour is available. |
| 6. Strict design-band limits | ACCEPTABLE | Build declaration implementing the cited arithmetic | Supported by TD-ARITH; inclusive limits are equivalent for these four fixed bases. |
| 7. Fifteen arms, skeleton-high; T0-low separate | ACCEPTABLE | Build declaration implementing the registered panel | Matches §1.3(a), §5.4 and §8; §5.8 owns T0-low. |

The four pre-build decisions in P §2 are acceptable. The wrapper is an implementation choice; common resampling is a declared-stream choice; the whole-rule skeleton reading is already assigned to Mike; the split into a later fidelity module is an implementation schedule that preserves mandatory obligations. No new contract rule is required to repair D1. A choice to reverse or waive §7's precedence would be a different matter and is not recommended or authorized by this review.

## 6. Q9 — Remaining reporting ownership

At the component-function level, no additional §1.3 item is unowned after part 1 plus this proposed module. D1 prevents acceptance of the affected implementations; it does not create an unidentified owner. The following mapping distinguishes component ownership from completed reporting integration.

| Required content | Component owner / status |
|---|---|
| §1.3(a), persistence | `outcomes.persistence_record` plus `evaluator_reports.persistence_report` |
| §1.3(b); §5.7 row 1, constancy | `reports.constancy` |
| §1.3(c); §5.7 row 3, flicker | Placed run observables plus `reports.flicker`, including part 1's floor references |
| §1.3(d), design margins | `evaluator_reports.design_margins` |
| §1.3(d); §5.7 row 2, measured margins | `reports.margins` |
| §1.3(e), TC suppression | `reports.suppression_contrast` |
| §1.3(f), θ=.10/.30 outputs | `evaluator_reports.reported_thresholds`; D1 repair required |
| §1.3(g); §5.7 row 5, skeleton boundary | `evaluator_reports.skeleton_boundary`; D1 dependency repair required |
| §1.3(h); §5.7 row 6, component coverage | `evaluator_reports.component_coverage` |
| §1.2′(i), persistence fidelity and its uncertainty | `closure.threshold_fidelity` with `outcomes.persistence_record` |
| §1.2′(iv), λ* and its conditional range | `evaluator.evaluate_map` and `evaluate_level` |
| §1.2′(ii)/(iii) and occupancy-based percentile ranges | Explicitly deferred to the third reports module |

[C §§1.2′, 1.3, 5.7; REPORTS public report functions; X public report functions; CL lines 176–219; E lines 357–372, 453–463.]

In particular, threshold fidelity is already owned: `closure.threshold_fidelity` computes normalized and raw-g shifts against κ=1, bracket-endpoint shifts, T0 comparisons and typed unavailable-reference states. The fitted-level range is already reported conditionally on compatible resamples. Neither should be counted as an omitted new M6B calculation. [CL lines 176–219; E lines 458–462.]

Still to be completed at runner/package integration are the step-15 jobs, full coverage/validity accounting, binding of inputs to run/object/arm/level and canonical identities, persisted encoding, and §5.9 completeness/readiness. The component functions do not establish those properties. A missing mandatory report prevents complete reporting and does not become a failure of B or D. [C §5.7 opening, §5.9, §8 steps 15–16; P §5, disclosures 4 and 6.]

## 7. Q10 — Other findings and verification record

### Independent execution

The L2 environment used Python 3.12.14, NumPy 2.3.5 and task-local pytest 9.2.0. The supplied M6B suite was invoked from the instrument directory with:

```text
python -B -m pytest tests/test_f9_m6b.py -v -p no:cacheprovider --durations=13
```

`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and the task-local pytest directory were supplied in the environment. No test source was changed.

**Supplied suite result: 13 passed in 221.01 seconds, exit code 0.** The suite's passing result coexists with D1 because it lacks the crossed unavailable-state cases described in §2.

| Independent check | Observed result |
|---|---|
| Archive and all payload hashes | Exact match to the supplied archive identity and all 80 manifest entries |
| Source comparison | Orchestration copies correspond after the declared θ/stream/preflight changes |
| Constant-index crossed states | D1 reproduced in all 12 map/route combinations in Appendix R, for both index entries |
| Two distinct synthetic families at both reported thresholds | Full-record scaling equality, including compatible/adverse/invalid draw types and unstable-edge outcomes |
| Non-interference probe | Input hashes, scored θ and resample rows unchanged; scored point records agree across call order and cache state |
| Components with no resolved component on either side | All components and q95 values retained; both no-resolved flags correct |
| TD geometry reconstructed directly | All four design tables and strict/inclusive equivalence reproduced |
| Synthetic 35/36-survivor panels | Four profile cases, nonmonotone suffix states and missing-level handling reproduced |

### Inspected L1 evidence, distinguished from L2 execution

The supplied module log reports 13 passes in 282.90 seconds; the combined M1–M6B log reports 289 passes in 1112.30 seconds. The mutation log reports 24 of 25 mutations caught, with the inclusive-band mutation surviving because it is equivalent on the declared bases. I inspected this evidence. **I did not independently rerun the combined seven-file suite or the full mutation campaign.** Their counts are L1 evidence, not additional L2 executions. [P §6; `build_records/f9_m6b_module_container_2026-11-23.txt`; `build_records/f9_m1_to_m6b_container_2026-11-23.txt`; `build_records/f9_m6b_mutation_check_2026-11-23.txt`.]

No additional blocking defect was established. The disclosed duplicated orchestration remains a maintenance obligation: a reviewed change in the placed evaluator must be reflected and verified in the copy. Private helper dependencies are pinned by the delivered identity tests. The reported evaluation costs remain inputs to the later resource benchmark, not measurements of the rule or evidence of scientific behavior. [P §5; TEST lines 354–386; C §8 step 10.]

All independent execution used source constants, closed-form geometry, constructed seed maps and synthetic survivor counts. No lattice-rule run, probe-output access, stage-master draw, calibration, qualification, canonical census or scientific-stage job occurred. No packet file was edited. The verdict is confined to the received module and its directly exercised dependencies.

## Appendix R — Reproducer for D1

Run this Python program with the received `flights/mfa_fidelity/instrument` directory on `PYTHONPATH`, or from that directory. It uses the actual T0 comparison array and constructs all input counts. It prints 12 rows: three map states through four evaluation routes. It asserts the observed defect, so successful execution against this received packet means the defect reproduced; it is not a passing contract-conformance test.

```python
import numpy as np
from mfa_instrument.f9 import evaluator as E
from mfa_instrument.f9 import evaluator_reports as X
from mfa_instrument.f9 import terrain as T

f = E.IndexFamily(T.comparison_array("T0", "P"), "T0", "P")
families = {"P": f, "H": f.shared_with("H")}
assert len(f) == 0
key = E.arm_level_key(777, "T0", "P", 1_000_000)
skeleton_key = X.skeleton_level_key(777, "T0", "P", 1_000_000)
expected = {
    "result": "not informative",
    "cause": "no eligible contour",
    "resampled": False,
}

empty = np.zeros((40, 100, 100), dtype=np.int64)
full = np.full_like(empty, 1000)
small = empty.copy()
small[:, 10:16, 10:16] = 1000

for state, counts in (("empty", empty), ("full", full),
                      ("under_minimum", small)):
    records = {
        "placed_020": E.evaluate_level(counts, families, key),
        "skeleton_020": X.skeleton_boundary(
            counts, families, skeleton_key
        )["evaluation"],
    }
    reports = X.reported_thresholds(counts, families, key)
    for theta, record in reports["theta_micro"].items():
        records[f"reported_{theta}"] = record
    for route, record in records.items():
        point = record["point"]
        causes = {name: entry["cause"]
                  for name, entry in record["indices"].items()}
        print(state, route, point["region_cells"], point["bonds"], causes)
        assert record["resampled"] is False
        assert all(entry != expected
                   for entry in record["indices"].values())

print("Reproduced: all 12 routes violate constant-index cause precedence.")
```

For the repair regression, replace the final per-entry inequality assertion with equality and retain the independent assertions about point cells, bonds and map causes. The required index result is `no eligible contour`; useful observed-map diagnostics should survive the correction.

**Required next return:** an identified, reviewed dependency-precedence repair together with the synchronized M6B copy and discriminating tests. The remaining component declarations and seven readings receive the dispositions stated above.

FINAL VERDICT: NOT SOUND
