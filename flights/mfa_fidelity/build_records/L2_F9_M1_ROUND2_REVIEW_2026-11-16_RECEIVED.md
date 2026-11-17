| Receipt check | Verified result | Status |
|---|---|---|
| Archive | `f9_m1_build_round2_L2.zip` | Received |
| Archive SHA-256 | `7b17fa67d362d646c8ae330c102835c9c11c42b93eef103c124e80ba7a4010e4` | MATCH — user-supplied digest |
| File count | **64 payload files + MANIFEST.txt = 65 files** | Verified |
| Manifest entries | 64 | Verified |
| Payload hashes | **64/64 match MANIFEST.txt** | PASS |
| Missing / unlisted payloads | 0 / 0 | PASS |
| Duplicate archive / manifest paths | 0 / 0 | PASS |
| ZIP CRC verification | All files passed | PASS |
| Receipt and authorization | Receipt completed before review; Mike subsequently instructed “execute” | Review authorized |

| # | File (path within archive) | Computed SHA-256 | Against MANIFEST.txt |
|---:|---|---|---|
| — | `MANIFEST.txt` | `a92d8a8a42272cf64a382612086fc6de70aa7161ffb9634486dfe4db18e57b11` | Not self-listed; digest recorded |
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M1_ROUND2_RESPONSE_2026-11-16.md` | `e25829c337778f67cd91f16388f43724ed1bc1c3a269cade2d68d1c4a27af405` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `52064b717bb9dc72e08b0746e155ea3d421a2eaa948d5317e30be7a4017bebfd` | MATCH |
| 4 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 5 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 6 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 7 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 8 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `5c3a75ae180e2c84a8ec825cae64a078785c982af36772ae30f701250a2fad36` | MATCH |
| 9 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `da937a8bb3edc36084ad046fae38df752ff226e77c09a85d4783b80eb02c4416` | MATCH |
| 10 | `flights/mfa_fidelity/build_records/L2_F9_M1_ROUND1_REVIEW_2026-11-16_RECEIVED.md` | `288928bf4061fbcf9d3077635e557c7e69cf7c912aecc5361f48268a1b833305` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/f9_m1_module_container_round2_2026-11-16.txt` | `141b17020d7d0c9dbf1c62aef6d2675ed54b2dc14965d1e9acae4e30090fd1bd` | MATCH |
| 12 | `flights/mfa_fidelity/build_records/F9_M1_IDENTITIES_CONTAINER_ROUND2_2026-11-16.json` | `30edf99bb6af19e0d626a8449cc764d825c107766745ed6174b23f72c5d13bed` | MATCH |
| 13 | `flights/mfa_fidelity/build_records/F9_M1_IDENTITIES_CONTAINER_2026-11-16.json` | `46809209f690843e021182a39857a9a4ff05abdaaf1ad20c4bb72155a748cc91` | MATCH |
| 14 | `flights/mfa_fidelity/build_records/l2_m1_round1_checks.py` | `7b879eb2ab2f5c03b77a8eb752d86dcda3deee8d9adc2c14b5aa9120a18f105f` | MATCH |
| 15 | `flights/mfa_fidelity/build_records/f9_m1_l2_round1_checks_on_round2_2026-11-16.txt` | `cb41611c01e3b33994538c8e5dd2fece37881dad0ef023b6a20fe4b17665ad58` | MATCH |
| 16 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M1_BUILD_PACKET_2026-11-16.md` | `8a745405a978c67ceb545827ade6ee614577ff00d0587ed0be597d0d7e24b205` | MATCH |
| 17 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 18 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 19 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 20 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 21 | `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_7_ROUND6_REVIEW_2026-11-15_RECEIVED.md` | `33310f3b810e046da05d52be01b8740bfe89a0bfe9f10e216755a382205a599b` | MATCH |
| 22 | `flights/mfa_fidelity/contracts/flight9/arith_v0_4/f9_evaluator_proto_v4.py` | `dc934c2716a69caa68c6a471010e26bfa06c93c94e63bb81f8b71bafbff4813a` | MATCH |
| 23 | `flights/mfa_fidelity/contracts/flight9/arith_v0_4/f9_compare.py` | `7fedb347cd40ba5f41c5e096919cb8ce56f3cbf7bd3c09fb801ea94298270fa2` | MATCH |
| 24 | `flights/mfa_fidelity/contracts/flight9/arith_v0_4/l2_appendix_r.py` | `afe6b99f62afeefc11c93b57a36c3cbdcb4f5cd3dae6b7db7938ad8c7f1abee8` | MATCH |
| 25 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 26 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |
| 27 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 28 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 29 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 30 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 31 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 32 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 33 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 M1 build review, round 2

**Date:** 2026-11-16. **Reviewer:** L2. **Decision authority:** Mike. **Register:** module build review. **Declared repository pin:** `b2a567415bd0a7af1a71c7e8531f536f1950aa69`.

## 1. Disposition

**One contained repair remains before placement.** R1 and R3 are **CLOSED**. The original four R2 counterexamples are repaired, but R2 is **NOT CLOSED** because the new cross-platform float comparator silently allows a spectral discrepancy larger than the frozen 1e-9 relative limit. It adds the separate base-array absolute tolerance to the spectral allowance. The witness uses the documented `float_rtol=C.F9_SPR_RECOMPUTE_RTOL`, with unchanged terrain bytes and unmodified source. [C §2.8, §3.4(5); I `_same`, `verify_bundle_deep`; §4 and Appendix R below.]

The reconstruction design is sound and can remain. It now checks the required objects, references, comparison-array derivations and recorded values from stored bases. The remaining repair is to preserve the distinct numerical rules for distinct quantities. No new interpretation from Mike is needed: the frozen contract already distinguishes relative spectral agreement from per-element base-array agreement. [I `record_from_bases`, `verify_bundle_deep`; C §§2.8, 3.4.]

**All 96 supplied tests passed in 322.02 seconds (5 minutes 22 seconds).** The unedited round-1 Appendix R program also reproduces every claimed closure outcome on the round-2 bytes. The remaining boundary counterexample is additional to those checks. [U; X; L2 execution record; Appendix R.]

### Sources and review scope

All sources are the receipt-verified packet bytes. Paths in this table are relative to `flights/mfa_fidelity/`; exact digests are in the receipt.

| Key | Source |
|---|---|
| P2 | `build_records/L1_TO_L2_F9_M1_ROUND2_RESPONSE_2026-11-16.md` |
| R1 | `build_records/L2_F9_M1_ROUND1_REVIEW_2026-11-16_RECEIVED.md` |
| C | `contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` |
| FR | `contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` |
| K, T, G, F, S, I | Respectively `config.py`, `terrain.py`, `geometry.py`, `family.py`, `spectral.py`, `identities.py` under `instrument/mfa_instrument/f9/` |
| U | `instrument/tests/test_f9_m1.py` |
| IR1, IR2 | `build_records/F9_M1_IDENTITIES_CONTAINER_2026-11-16.json` and `build_records/F9_M1_IDENTITIES_CONTAINER_ROUND2_2026-11-16.json` |
| X | `build_records/l2_m1_round1_checks.py` |

The prior review in the packet is byte-identical to the delivered review with SHA-256 `288928bf4061fbcf9d3077635e557c7e69cf7c912aecc5361f48268a1b833305`. X is exactly the Python program extracted from its Appendix R, including its trailing newline; its SHA-256 is `7b879eb2ab2f5c03b77a8eb752d86dcda3deee8d9adc2c14b5aa9120a18f105f`. I did not alter that program to obtain the closure results. [R1; X; L2 byte comparison.]

This is a review of the repaired M1 against the frozen contract and round-1 requirements. The repository pin remains the packet's declared provenance; I did not independently fetch the commit. No packet source was modified, no M1 placement was performed, and no canonical job, stage master, dynamics, occupancy analysis or boundary-endpoint calculation was performed. Test bundles are noncanonical fixtures. [P2 introduction, §§4–5; C §8.]

## 2. Q1 — Closure of R1, R2 and R3

| Round-1 item | Disposition | Evidence and remaining scope |
|---|---|---|
| R1 — component membership | **CLOSED** | The component digest now includes each canonical bond's component label. The fixed-input checkerboard distinguishes the correct partition from the complement's corner pairing. |
| R1 — little-endian level bytes | **CLOSED** | Levels use `struct.pack("<d", ell)`; independent explicit-byte checks agree. |
| R2 — semantic bundle verification | **NOT CLOSED** | The four original invalid records now fail, and whole-record reconstruction repairs the missing domains and relationships. The cross-platform spectral-tolerance defect in §4 remains. |
| R3 — η₀ rule-to-value binding | **CLOSED** | The probability and rule are bound in the declaration; the preflight checks the actual η₀ against that rule on the running machine. Changed-value, one-ulp and changed-declaration probes fail. |
| Round-1 §9.1 — spectral stop wording | **CLOSED WITH NOTE** | The spectral module now states the actual mixed stopping expression. One old “relative change” comment remains beside `F9_SPR_TOL` in config; correct it with the repair. It is not an independent numerical blocker. |
| Round-1 §9.2 — bound on the fall | **CLOSED** | Identities documentation states that the fall is bounded and the within-level spread is reported. |
| Round-1 §9.3 — loader guarantee | **CLOSED** | Form/bytes, semantics and external canonical binding are accurately separated. |

[P2 §§1–2; K, F, S, I; X execution; independent checks below.]

### 2.1 R1 — The partition itself is now identified

For each level, F now serializes the bond and component counts with `struct.pack("<ii", ...)`, then every canonical bond's component number as little-endian int32. The header fixes the length of the following vector. Combined with the mask identity and M1-1's bond order, this binds which bonds belong to which component. [F `family_summary`; G canonical-order declaration.]

The independent rerun of the original 10-cell checkerboard witness produced:

| Property | Round-2 result |
|---|---|
| Fixed comparison array, levels and masks | Unchanged between the two tracings |
| Canonical bond points | Identical |
| Bonds / components / sizes | 2,000 / 50 / 40 bonds each |
| Changed membership labels | 1,500 |
| Mask and family identities | Equal |
| Component identities | **Different** |

The correct and substituted partitions respectively hash to:

```text
5184c162d37d42544205b535567dc8d97a1c2581b0de8230b8bffb65d36afa9b
f56ba15451ddc3946a6335e1fc7f2e78124b5fa48821f021fef9d158c931e34b
```

An independent `struct` encoding of the entire 2,000-label vector matches the first digest. Separate family-level checks against explicit little-endian IEEE bytes for 1.25, 2.5 and 17.125 match the repaired family hash. `geometry.py` is byte-identical to round 1, at `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971`; the corner rule was not changed. [F; G; U new R1 tests; X; L2 independent serialization checks.]

### 2.2 R2 — The original four witnesses now fail

X, executed unchanged against round 2, printed these outcomes:

| Case | Round 1 | Round 2 |
|---|---|---|
| Unchanged valid control | Accepted | **Accepted** |
| Empty arms, families and same-family dictionaries | Accepted | **Rejected** |
| Doubled TB.H g_spec | Accepted | **Rejected** |
| TB.H comparison bytes and summary replaced by TB.P's | Accepted | **Rejected** |
| TC.H pointed to TB.P through `omega_key` | Accepted | **Rejected** |

The new path addresses the former omissions directly. It validates base shape and domain, checks agreement with the local terrain formulas, reconstructs the required record from the stored bases, compares complete structures with exact JSON types, and checks the stored comparison arrays against those derived from the stored bases. Missing keys cannot escape by shortening a submitted dictionary. Arm references and both spr and g_spec are regenerated rather than trusted. `compare_bundles` now invokes deep verification on both inputs. [I `_check_bases`, `record_from_bases`, `_same`, `verify_bundle_deep`, `compare_bundles`; U semantic tests; X.]

The order is appropriate for those obligations. The constructor can describe some alternate base sets, while the complete verification path rejects a substantially different terrain before accepting its record. That separation is not an additional defect. The explicit 1e-12 base-array comparison also avoids requiring another runtime's transcendental results to equal the writing machine's bytes. [I `record_from_bases`, `verify_bundle_deep`; U `test_stored_bases_must_be_the_declared_terrains`; C §3.4(5).]

R2 remains open only for the quantity-specific tolerance failure demonstrated in §4. The successful reconstruction work should be retained.

### 2.3 R3 — The float exemption now has its required check

The new declaration binds `floor_probability = 0.01` and the rule `-ln(1 - floor_probability)`. Its recomputed digest is:

```text
7fbef2ff2a04e9bc0825e6bbfeb70ce867d15cc51ec22e7b4eac0a6c0ff8a3b3
```

The submitted η₀ remains `0.01005033585350145`. Independent in-memory source probes, with the packet files unchanged, give:

| Probe | Result |
|---|---|
| Unchanged declaration and actual η₀ | Pass |
| Actual η₀ calculated from 0.02, declared probability/rule unchanged | Reject at rule/value check |
| Actual η₀ one ulp above the correct value | Reject at rule/value check |
| Probability changed to 0.02 alone | Reject at rule/value check |
| Probability and actual η₀ expression both changed to 0.02 | Reject at declaration digest |

The final control confirms that an internally consistent change to the probability cannot bypass the frozen declaration. The repair preserves the reason for excluding the libm-derived float from the digest while checking its relationship to the bound rule. [K `F9_DECLARATION`, `verify_frozen_identity`; U R3 test; X; L2 independent probes.]

## 3. Q2 — Repaired declarations

| Declaration | Disposition | Reason |
|---|---|---|
| M1-2 — family, mask and component identities | **ACCEPTABLE** | R1 is closed: canonical membership is bound and level bytes are explicitly little endian. |
| M1-3 — record from stored bases; loader, semantic verifier and runner responsibilities | **REQUIRES CHANGE** | The reconstruction and responsibility split are acceptable. The cross-platform spectral comparison must be repaired as in §4. |
| M1-5 — η₀ represented by its rule and probability | **ACCEPTABLE** | R3 is closed; both the declaration and the actual rule/value relationship are checked. |

The other round-1 declaration acceptances are retained within their stated scopes. No change to the geometry, frozen terrain formulas, spectral iteration, same-family convention, platform policy or deferred runner responsibilities is required by this review. [R1 §6; P2 §§1–2; source comparison.]

## 4. Q3 — A record outside the spectral tolerance still verifies

### 4.1 The remaining defect: the base-array allowance leaks into the spectral comparison

The frozen contract gives two different numerical rules:

| Quantity | Frozen rule |
|---|---|
| Spectral radius recomputed elsewhere | Agreement to **1e-9 relative**, or the discrepancy is recorded. |
| Base arrays recomputed elsewhere | Agreement to **1e-12 per element**; the largest deviation is recorded. |

[C §2.8 and §3.4(5); K `F9_SPR_RECOMPUTE_RTOL`, `F9_CROSS_PLATFORM_TOL`.]

The revised `_same` instead applies this allowance to every float whenever `rtol > 0`:

```python
tol = rtol * max(abs(a), abs(b)) + C.F9_CROSS_PLATFORM_TOL
```

For spr this silently adds an absolute 1e-12 allowance that §2.8 does not give. The 1e-12 term belongs to comparison of base-array elements; it is not a universal scalar allowance. The dedicated base-array check already applies that rule separately in `verify_bundle_deep`. [I `_same`, `verify_bundle_deep`; C cited clauses.]

### 4.2 Full-bundle witness using the documented mode

Start with a valid noncanonical bundle produced by the unmodified round-2 code. Copy it, leave all arrays and all other record fields unchanged, and multiply only `arms["TB.P"]["spr"]` by `1 + 1.004e-9`. Re-serialize the record canonically. On the reviewed runtime:

| Quantity | Observed value |
|---|---:|
| spr recomputed from the stored bases | 0.11340644355296714 |
| Altered recorded spr | 0.11340644366682721 |
| Absolute difference | 1.1386007414682098e-10 |
| Relative difference, using recorded value as reference | **1.004000041490821e-9** |
| Relative difference, using recomputation as reference | **1.0040000424988372e-9** |
| Pure 1e-9 relative allowance using the recorded value | 1.1340644366682723e-10 |
| Current `_same` mixed allowance | 1.1440644366682722e-10 |

The difference exceeds 1e-9 relative with either denominator, but falls inside the added absolute allowance. The full API outcomes are:

| Verification | Outcome |
|---|---|
| Unchanged bundle, exact default | **Accepted** |
| Altered record, exact default | **Rejected** |
| Altered record, `float_rtol=C.F9_SPR_RECOMPUTE_RTOL` | **Accepted without a discrepancy indication** |

This is the documented cross-platform argument, not a larger user-selected tolerance or a patched comparator. The base arrays, record structure, JSON form, identities and source remain otherwise intact. The changed record has a different digest, as expected; external authenticity is not the issue being tested. [I; Appendix R; L2 full-bundle execution.]

I also checked an internally coherent spectral/gain pair: multiply spr by `1 + 1.0003e-9`, then set `g_spec = q / (Δt * changed_spr)`. Its spectral relative discrepancy is **1.0003001202131354e-9**, still outside the frozen limit, and it also passes cross-platform verification. Thus the issue persists when the changed spr and g_spec satisfy their algebraic relationship. [Appendix R; L2 execution.]

The earlier tests exercise a small accepted nudge of 1e-11 and a rejected error of 1e-6. Neither distinguishes the frozen relative boundary from the new mixed allowance immediately outside it. A discriminating boundary case is needed. [U `test_float_tolerance_is_for_another_machine_only`; `MORE_SEMANTIC_CASES["spr_off_by_1e-6"]`.]

### 4.3 Why discrepancy reporting does not excuse the current result

Section 2.8 permits a discrepancy to be recorded instead of requiring every recomputation to agree. The defect is not that an out-of-tolerance number can exist. It is that the current verifier returns this record as verified and supplies no indication that the frozen spectral bound was exceeded. Returning an ordinary success record does not implement the alternative of recording the discrepancy. [C §2.8; I `verify_bundle_deep`.]

`compare_bundles` can separately report differences between the spectral values stated by two input records, but that does not restore the missing check between each record's value and its recomputation from stored arrays. The deep verification it relies on has already silently accepted the excess. [I `verify_bundle_deep`, `compare_bundles`.]

### 4.4 Required contained repair

Preserve the reconstruction design and give the spectral radius its own comparison rule:

1. Retain exact equality in the default mode for the writing environment.
2. In the documented cross-platform mode, enforce the frozen **pure relative** 1e-9 limit for spr, without adding the base-array absolute term.
3. If the bound is exceeded, refuse verification through the present interface, or explicitly return and record a typed spectral discrepancy. Do not silently return the ordinary verified record.
4. Keep the base-array 1e-12 per-element comparison separate. Any numerical policy for other descriptive float fields should be stated for those fields rather than attributed to the base-array clause.

A dedicated spectral check before returning the record, or a comparator that selects a declared rule by quantity, can satisfy this. The repair should continue to verify g_spec and its relation to the stored numerical declarations. No terrain, spectral algorithm, contract value or authorized scientific scope needs to change. [C §§2.8, 3.4; I.]

**Closure evidence:** retain the valid control and original four negative cases; add a within-bound spectral control and a case just beyond 1e-9 relative but inside the current mixed allowance. The two witnesses above should not return unqualified cross-platform success. Include both the spr-only and coherent spr/g_spec cases so the spectral rule is tested directly.

## 5. Q4 — Exact writing-environment default and explicit recomputation tolerance

**Exact numerical float equality is the appropriate default for the writing environment.** The record is recomputed from stored bytes with the declared implementation, and the unchanged control and repeated-build tests verify that the current environment reproduces it. Exact JSON types and exact nonnumeric identities should remain exact. [I `_same`, `verify_bundle_deep`; U round-trip and repeated-build tests.]

An explicit mode for recomputation in another environment is also appropriate, provided each quantity receives its declared numerical rule. The accepted principle does not endorse the current universal mixed float allowance; §4 is the repair needed to make that mode conform. [C §§2.8, 3.4(5); P2 Q4.]

A NumPy or runtime upgrade on the canonical machine is a later environment-binding question for the runner. It should not silently turn a failed exact check into permission to enlarge a frozen tolerance. The canonical arrays remain the objects used and bound; a different environment's recomputation is a check against them. This review neither requires a new spectral algorithm nor asks M1 to implement the deferred runner authorization layer. [P2 disclosure 2 and M1-9 carried from round 1; I module scope; C §§3.4, 5.9, 8.]

## 6. Q5 — Remaining note and retained findings

### 6.1 One comment still needs conformance

`config.py` still labels `F9_SPR_TOL = 1e-14` as the “relative change of the Rayleigh quotient between iterations.” The repaired spectral module correctly states:

```python
abs(ray - last) <= tol * max(1.0, abs(ray))
```

On the declared arms, ray is below 1, so the stop is an absolute 1e-14 change. Correct the config comment to match that expression or refer to the accurate spectral documentation. This is the remainder behind the **CLOSED WITH NOTE** documentation disposition; it is not a second scientific blocker. [K `F9_SPR_TOL`; S module documentation and `spectral_radius`; R1 §9.1.]

### 6.2 Scope of the repaired source is acceptable

Independent source comparison confirms:

- `geometry.py` and the package initializer are unchanged.
- The spectral executable AST is unchanged after removing docstrings; the committed iteration is preserved.
- `terrain.py` adds only the two declared-object guards in `level_label`; the formerly accepted invalid terrain/composition labels are now refused.
- The new base validation rejects missing or extra terrains, incorrect base counts/shapes/dtypes, nonfinite values and values outside [0,1]. T0's constant bases, the TA/TD common-base relation and the TD half-step/core relation are checked.
- The TD core diagnostics retain 2,000 cells per variant, 200 or 416 bonds, and component sizes `(200,)` or `(104,104,104,104)` as appropriate.

[K–I; U; L2 source comparison and independent base-domain probes.]

Comparing IR1 and IR2, all eight component identities change as required by R1. Every other family field remains equal, all eight terrain base identities remain equal, and all fifteen spr/g_spec pairs remain equal. The new schema and declaration identity are appropriate for an unplaced module whose identity representation has changed. This review identifies no further placement blocker beyond §4. [IR1; IR2; P2 §§2–3; L2 record comparison.]

## 7. Verification record and next return

| Check | Result |
|---|---|
| Archive and all payload identities | Receipt passed: 64 payloads plus manifest; 64/64 payload hashes match. |
| Supplied M1 suite | **96 passed in 322.02s (0:05:22)**; no skips. |
| Supplied round-1 Appendix R extraction | Byte-identical to the program in the received review. |
| Original R1/R2/R3 witnesses | All claimed round-2 reversals reproduced; unchanged bundle accepted. |
| Independent R1 encoding | Membership vector and explicit little-endian level encodings agree. |
| Independent R3 binding | Actual-value, one-ulp, probability-only and coherent probability/hazard changes rejected. |
| New spectral-tolerance witness | Exact mode rejects; documented cross-platform mode silently accepts values beyond 1e-9 relative. |
| Packet source preservation | All 64 payload files rehashed after review; unchanged. |

The review runtime is Python **3.12.14**, NumPy **2.3.5**, SciPy **1.17.0**, on little-endian Linux. SciPy was present, so the all-arm independent-eigenvalue test was not skipped. Pytest was made available through the existing local dependency directory, with third-party plugin autoload disabled. These are review-environment results, not canonical-machine results. [L2 execution record.]

The next return should contain the contained spectral-comparison repair, its boundary tests and refreshed noncanonical evidence, plus the stale-comment correction. R1 and R3 do not need to be reopened unless their source changes. A full new contract consultation or a canonical/scientific run is not requested. L1 repairs; Mike remains decision authority. [P2 register and questions; C §8.]

## Appendix R — Reproduce the remaining tolerance defect

Save the following program as a scratch Python script and pass the extracted packet root as its first argument. An optional second argument names a JSON output file. It creates temporary noncanonical bundles, verifies a valid control, and changes separate copies. It edits no packet source, performs no dynamics, and draws no stage master. On the reviewed bytes, both changed records are rejected in exact mode and accepted in the documented cross-platform mode even though their spectral differences exceed 1e-9 relative.

```python
from pathlib import Path
import json
import shutil
import sys
import tempfile

packet = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(packet / 'flights/mfa_fidelity/instrument'))
from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import identities as I


def check(directory, relative_tolerance):
    try:
        I.verify_bundle_deep(str(directory), float_rtol=relative_tolerance)
        return {'outcome': 'ACCEPTED', 'error': None}
    except C.F9ConfigError as exc:
        return {'outcome': 'REJECTED', 'error': str(exc)}


results = []
with tempfile.TemporaryDirectory(prefix='l2_f9_m1_round2_') as scratch:
    scratch = Path(scratch)
    control = scratch / 'control'
    I.write_bundle(str(control))
    assert check(control, 0.0)['outcome'] == 'ACCEPTED'
    print('UNCHANGED CONTROL: ACCEPTED', flush=True)
    for label, nudge, coherent_gain in (
        ('spectral_only', 1.004e-9, False),
        ('coherent_pair', 1.0003e-9, True),
    ):
        changed = scratch / label
        shutil.copytree(control, changed)
        path = changed / I.RECORD_NAME
        record = json.loads(path.read_bytes())
        reference = record['arms']['TB.P']['spr']
        stated = reference * (1.0 + nudge)
        record['arms']['TB.P']['spr'] = stated
        if coherent_gain:
            record['arms']['TB.P']['g_spec'] = record['q'] / (C.F9_DT * stated)
        path.write_bytes(I.canonical_json(record))
        difference = abs(stated - reference)
        relative = difference / abs(stated)
        assert relative > C.F9_SPR_RECOMPUTE_RTOL
        item = {
            'case': label,
            'recomputed_spr': reference,
            'stated_spr': stated,
            'absolute_difference': difference,
            'relative_to_stated': relative,
            'relative_to_recomputed': difference / abs(reference),
            'frozen_relative_allowance': C.F9_SPR_RECOMPUTE_RTOL * abs(stated),
            'current_mixed_allowance': (
                C.F9_SPR_RECOMPUTE_RTOL * max(abs(stated), abs(reference))
                + C.F9_CROSS_PLATFORM_TOL
            ),
            'exact': check(changed, 0.0),
            'cross_machine': check(changed, C.F9_SPR_RECOMPUTE_RTOL),
        }
        results.append(item)
        print(json.dumps(item, sort_keys=True), flush=True)

if len(sys.argv) > 2:
    Path(sys.argv[2]).write_text(json.dumps(results, indent=2) + '\n')
```

FINAL VERDICT: DEFECT-WITH-REPAIR
