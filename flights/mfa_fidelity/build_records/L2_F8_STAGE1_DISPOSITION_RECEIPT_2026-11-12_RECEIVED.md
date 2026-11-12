# L2 — Flight 8 Stage 1 Disposition Consultation: Receipt

Date: 2026-11-12

RECEIPT STATUS: VERIFIED

Scope: archive receipt and byte-identity verification only. The supplied repository pin is `ee-theory-lab abb9279`; this receipt does not independently verify the repository commit or the asserted committed state. Decision authority remains with Mike.

The newly supplied archive completes the previously incomplete receipt. No substantive review has been performed, no packaged code has been executed, and no tests have been run. Review remains pending the user's explicit “execute.”

## Receipt summary

| Check | Expected | Observed | Result |
|---|---|---|---|
| Archive | `f8_stage1_disposition_L2.zip` | Received; 920,037 bytes | MATCH |
| Archive SHA-256 | Declared digest below | Exact match | MATCH |
| Total ZIP entries | 105 | 105 | MATCH |
| File entries | 104 payload files + `MANIFEST.txt` | 105 files | MATCH |
| Directory entries | Excluded from payload count | 0 | VERIFIED |
| Manifest SHA-256 | Declared digest below | Exact match | MATCH |
| Parsed manifest records | 104 | 104 | MATCH |
| Payload hashes | Every payload matches its manifest digest | 104 / 104 match | MATCH |
| Hash mismatches | 0 | 0 | MATCH |
| Missing payload paths | 0 | 0 | MATCH |
| Unlisted payload paths | 0 | 0 | MATCH |
| Duplicate ZIP paths | 0 | 0 | MATCH |
| Duplicate manifest paths | 0 | 0 | MATCH |
| Malformed manifest records | 0 | 0 | MATCH |
| Instruction packet identity | Declared packet digest below | Exact match | MATCH |
| Packaged instruction versus earlier standalone attachment | Same bytes | Direct byte equality confirmed | MATCH |

## Archive, manifest, and instruction identities

| Item | Bytes | Declared SHA-256 | Computed SHA-256 | Result |
|---|---:|---|---|---|
| `f8_stage1_disposition_L2.zip` | 920037 | `656cc29e5bc9197c0b14147c6add42efba703fdf63e90f9685ba6dbe8f0378ae` | `656cc29e5bc9197c0b14147c6add42efba703fdf63e90f9685ba6dbe8f0378ae` | MATCH |
| `MANIFEST.txt` | 14320 | `04d8248371a5ca44dbdec6d09e48459f8fdd963aae2630d7e9ba49b133dea6e1` | `04d8248371a5ca44dbdec6d09e48459f8fdd963aae2630d7e9ba49b133dea6e1` | MATCH |
| `flights/mfa_fidelity/build_records/L1_TO_L2_F8_STAGE1_DISPOSITION_PACKET_2026-11-12.md` | 16549 | `e162b1b5d2640f66eea505ffb97c0d9f1a6d6b93109cf01333ba3cbf75013afd` | `e162b1b5d2640f66eea505ffb97c0d9f1a6d6b93109cf01333ba3cbf75013afd` | MATCH |

The 104 manifest records cover the 104 payload files exactly. `MANIFEST.txt` is outside that payload list and was checked separately against the manifest digest supplied by the user. The packaged instruction is also byte-for-byte identical to the earlier standalone attachment.

## Complete payload receipt table

Paths are archive-relative. Every computed digest below was calculated from the decompressed bytes of the corresponding ZIP member and compared with its own manifest record. Rows preserve manifest order.

| # | Payload path | Bytes | Manifest SHA-256 | Computed SHA-256 | Result |
|---:|---|---:|---|---|---|
| 1 | `GIT_LOG_d4994a5_to_abb9279.txt` | 7269 | `3012b5893dca1b4edfce4d3e4a4ba7d8e5d1ade1c73fc5600453274ee9bcc704` | `3012b5893dca1b4edfce4d3e4a4ba7d8e5d1ade1c73fc5600453274ee9bcc704` | MATCH |
| 2 | `flights/mfa_fidelity/build_records/F8_M6_GENERATOR_DECLARATION_v0_3.md` | 31878 | `c73980585fc238209453ebadb4707d961e41d77b7970435e8ce4113298868e47` | `c73980585fc238209453ebadb4707d961e41d77b7970435e8ce4113298868e47` | MATCH |
| 3 | `flights/mfa_fidelity/build_records/F8_M7_PLACEMENT_NOTE_2026-11-04.md` | 6388 | `bbef0dd9f22aa579be98fcdef43836743b436a1379c72ad08fc6e9548d7343a9` | `bbef0dd9f22aa579be98fcdef43836743b436a1379c72ad08fc6e9548d7343a9` | MATCH |
| 4 | `flights/mfa_fidelity/build_records/L1_TO_L2_F8_STAGE1_DISPOSITION_PACKET_2026-11-12.md` | 16549 | `e162b1b5d2640f66eea505ffb97c0d9f1a6d6b93109cf01333ba3cbf75013afd` | `e162b1b5d2640f66eea505ffb97c0d9f1a6d6b93109cf01333ba3cbf75013afd` | MATCH |
| 5 | `flights/mfa_fidelity/contracts/flight8/APPENDIX_A_OF_RECORD.md` | 5577 | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` | MATCH |
| 6 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | 79550 | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | MATCH |
| 7 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | 7544 | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` | MATCH |
| 8 | `flights/mfa_fidelity/contracts/flight8/appendix_a.py` | 11966 | `bc3e4f05f48e0840eddd5e61b8ea653411e4468900c098e801e5e13506fe0903` | `bc3e4f05f48e0840eddd5e61b8ea653411e4468900c098e801e5e13506fe0903` | MATCH |
| 9 | `flights/mfa_fidelity/governance/f8_stage1/AUTHORIZATION_001.json` | 683 | `fd7ae15748982f0620eb9637979b2d9dd5586987385ade17f1501f2ad1f3d0a3` | `fd7ae15748982f0620eb9637979b2d9dd5586987385ade17f1501f2ad1f3d0a3` | MATCH |
| 10 | `flights/mfa_fidelity/governance/f8_stage1/AUTHORIZATION_002.json` | 884 | `111c5ee83d6c30a36220af6ecf48d45507c459124cdf21b044f76c7a78b5852c` | `111c5ee83d6c30a36220af6ecf48d45507c459124cdf21b044f76c7a78b5852c` | MATCH |
| 11 | `flights/mfa_fidelity/governance/f8_stage1/AUTHORIZATION_003.json` | 1064 | `1413d3b74731e7ea96b1825b5ff1acf5ce9a0a5f01d718aa2d91d925acbee7bb` | `1413d3b74731e7ea96b1825b5ff1acf5ce9a0a5f01d718aa2d91d925acbee7bb` | MATCH |
| 12 | `flights/mfa_fidelity/governance/f8_stage1/AUTHORIZATION_REGISTRY.json` | 355 | `ba7abe73d734e4006e503e231d2b2840e26b45492aa99194f9dc7935ba51f52a` | `ba7abe73d734e4006e503e231d2b2840e26b45492aa99194f9dc7935ba51f52a` | MATCH |
| 13 | `flights/mfa_fidelity/governance/f8_stage1/F8_GOVERNANCE.json` | 4969 | `889a76646c4d8eb5590b1631d43de4c91b14d0a735d300723271779a6c9cfba5` | `889a76646c4d8eb5590b1631d43de4c91b14d0a735d300723271779a6c9cfba5` | MATCH |
| 14 | `flights/mfa_fidelity/governance/f8_stage1/F8_GOVERNANCE_RATIFICATION_RECORD_v1_0.md` | 6677 | `e38b37553f261ab1ff03c0be6857688384c891fe4cbf038eae5adf18dd940dd1` | `e38b37553f261ab1ff03c0be6857688384c891fe4cbf038eae5adf18dd940dd1` | MATCH |
| 15 | `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_RATIFICATION_RECORD_v1_0.md` | 10992 | `cdedfcb4540d950be69695b589b3f8cc8b5164278b7d57e850eb7ff8b601346b` | `cdedfcb4540d950be69695b589b3f8cc8b5164278b7d57e850eb7ff8b601346b` | MATCH |
| 16 | `flights/mfa_fidelity/governance/f8_stage1/F8_THRESHOLD_ADAPTER.json` | 3467 | `b47d7b4a19f21c57c218e0cf4b2e4039ce2507bf729af713cf79994b081906e9` | `b47d7b4a19f21c57c218e0cf4b2e4039ce2507bf729af713cf79994b081906e9` | MATCH |
| 17 | `flights/mfa_fidelity/governance/f8_stage1/M7_PLACEMENT_RECORD.json` | 636 | `6f463d30a23daa304760fbf4f8c1d6858dfa52cc0e0d4cd21426aa615e191370` | `6f463d30a23daa304760fbf4f8c1d6858dfa52cc0e0d4cd21426aa615e191370` | MATCH |
| 18 | `flights/mfa_fidelity/governance/f8_stage1/M7_SUITE_RECORD.json` | 445 | `b4ce66f6dd594fcde54c5dc43d9c1b3d25bdb1c587b1008e47409038eb12f27c` | `b4ce66f6dd594fcde54c5dc43d9c1b3d25bdb1c587b1008e47409038eb12f27c` | MATCH |
| 19 | `flights/mfa_fidelity/governance/f8_stage1/PACKAGE_SPECIFICATION.json` | 7632 | `0738d35ee0a30aefbc69b30476a7e486ba3a99f2cd8511fa10a523dff5a1cd4e` | `0738d35ee0a30aefbc69b30476a7e486ba3a99f2cd8511fa10a523dff5a1cd4e` | MATCH |
| 20 | `flights/mfa_fidelity/governance/f8_stage1/PRODUCTION_PREREQUISITES.json` | 2883 | `e03084c3dbdd59b6281abf32c7e96a6385b7d5fa404613d0f09d9c7f710b8592` | `e03084c3dbdd59b6281abf32c7e96a6385b7d5fa404613d0f09d9c7f710b8592` | MATCH |
| 21 | `flights/mfa_fidelity/governance/f8_stage1/make_f8_authorization_001.py` | 3203 | `9ab4a1878e552b9bf55bed4e7c188f27e2a9a0e9089a3470bba1be7ddd02a01f` | `9ab4a1878e552b9bf55bed4e7c188f27e2a9a0e9089a3470bba1be7ddd02a01f` | MATCH |
| 22 | `flights/mfa_fidelity/governance/f8_stage1/make_f8_authorization_002.py` | 4162 | `f4e8810abd8f3291961589cb3fb362a8666c4bbd8d9073b5765e251502f87c81` | `f4e8810abd8f3291961589cb3fb362a8666c4bbd8d9073b5765e251502f87c81` | MATCH |
| 23 | `flights/mfa_fidelity/governance/f8_stage1/make_f8_authorization_003.py` | 4502 | `c81a637ba57e0d1ba5a7636c7f89d3539cfeca2f3d2c072c995620989c6fb07b` | `c81a637ba57e0d1ba5a7636c7f89d3539cfeca2f3d2c072c995620989c6fb07b` | MATCH |
| 24 | `flights/mfa_fidelity/governance/f8_stage1/make_f8_governance.py` | 9112 | `f0f21bc7afa9bdfc7f8f98bab7f45cfa71051f6e601b88900f312af7ab371683` | `f0f21bc7afa9bdfc7f8f98bab7f45cfa71051f6e601b88900f312af7ab371683` | MATCH |
| 25 | `flights/mfa_fidelity/governance/f8_stage1/make_f8_prereq_manifest.py` | 3788 | `a3b0cf1b144b773f1ae5c6610ad179d86e62821181ba9cd005ef65197c847a9f` | `a3b0cf1b144b773f1ae5c6610ad179d86e62821181ba9cd005ef65197c847a9f` | MATCH |
| 26 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/calibration_tranche.json` | 4163 | `c156c20439e321f15834f23850e268490c0b590a9e53a54b44fd7ab8516b4d92` | `c156c20439e321f15834f23850e268490c0b590a9e53a54b44fd7ab8516b4d92` | MATCH |
| 27 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/calibration_census.json` | 139910 | `91aebc07a80fab79a852f4bb701570b15b7409f8b785928821f91cd17ac5721c` | `91aebc07a80fab79a852f4bb701570b15b7409f8b785928821f91cd17ac5721c` | MATCH |
| 28 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/dense_reference.json` | 9171 | `5d6d1ffb00497d930c3192ab623975cc1378708603b716d26f2a36bbab6493b4` | `5d6d1ffb00497d930c3192ab623975cc1378708603b716d26f2a36bbab6493b4` | MATCH |
| 29 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/derived.closure_publication.json` | 1001 | `4f2d5cfc2e46acb2c2c276c14ebc6fd78f4e2f248b5aba599bc559fcd01ddc58` | `4f2d5cfc2e46acb2c2c276c14ebc6fd78f4e2f248b5aba599bc559fcd01ddc58` | MATCH |
| 30 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/derived.conformance_preflight.json` | 910 | `6d6a3c65350533a011fd5bda3c1400aee68c18bed9777c1f3349ac842017fb8d` | `6d6a3c65350533a011fd5bda3c1400aee68c18bed9777c1f3349ac842017fb8d` | MATCH |
| 31 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/derived.ensemble_sizes.json` | 828 | `476b1f60ad916661f656440e8cb6e8050bf6ee3cf11bd6629eac1765805cc945` | `476b1f60ad916661f656440e8cb6e8050bf6ee3cf11bd6629eac1765805cc945` | MATCH |
| 32 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/derived.level_list_and_spacings.json` | 1053 | `84e4e249532a2cbefb69a6e9262efa651dd4fba57a590739f135aa62d34d4e1a` | `84e4e249532a2cbefb69a6e9262efa651dd4fba57a590739f135aa62d34d4e1a` | MATCH |
| 33 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/derived.null_law.json` | 993 | `e04d3d4786a73cd60a3f024d3ccf95b5a82f54c1e5883f765c1b08b93db7f76c` | `e04d3d4786a73cd60a3f024d3ccf95b5a82f54c1e5883f765c1b08b93db7f76c` | MATCH |
| 34 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/derived.router_collision_record.json` | 808 | `eecef2248e2694373a07da5c1e4ef4d1963a10b43afe0c720e8ad8ee079318e0` | `eecef2248e2694373a07da5c1e4ef4d1963a10b43afe0c720e8ad8ee079318e0` | MATCH |
| 35 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/m6_audit_qualification.json` | 1264 | `29168ab78238e7b6eb848f122b32e35adbd5073864ea600f0283261dd4f76959` | `29168ab78238e7b6eb848f122b32e35adbd5073864ea600f0283261dd4f76959` | MATCH |
| 36 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/m6_design_audit.json` | 7053 | `96a1e497027b491af6e78ad51268191b39650e069883cdeae3a25695f4937475` | `96a1e497027b491af6e78ad51268191b39650e069883cdeae3a25695f4937475` | MATCH |
| 37 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/m6_held_out_audit.json` | 7079 | `002d276c0033ab47da82ff2f63e8077d2f32fd53ea10416b0f7f6ec57deb3b39` | `002d276c0033ab47da82ff2f63e8077d2f32fd53ea10416b0f7f6ec57deb3b39` | MATCH |
| 38 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/m6_price.json` | 848 | `0cad5161eb35f8fd3d7d465db252bf8905a73ed59df9a277a0919898d89edfb6` | `0cad5161eb35f8fd3d7d465db252bf8905a73ed59df9a277a0919898d89edfb6` | MATCH |
| 39 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/mp1_known_answer.json` | 1492 | `12d983544f653dbc290225f5db7da5eac3a8ef2bbd2af993ad2d9ce1f5adf598` | `12d983544f653dbc290225f5db7da5eac3a8ef2bbd2af993ad2d9ce1f5adf598` | MATCH |
| 40 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/p1_evaluation.json` | 7667 | `51489c7e97730ae0f51c0bc5007219f3ea7e46ec7317dc963247f9ba70440063` | `51489c7e97730ae0f51c0bc5007219f3ea7e46ec7317dc963247f9ba70440063` | MATCH |
| 41 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/projection_sweeps.ensemble.json` | 152866 | `430b5a0da48e79784644175a74fe5afdceef16df2b537530d37f67c2facd55d8` | `430b5a0da48e79784644175a74fe5afdceef16df2b537530d37f67c2facd55d8` | MATCH |
| 42 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/projection_sweeps.json` | 14396 | `d0459cc79b722b7008458e4c91684c73765af2e113a5e8464cd6919230b1572f` | `d0459cc79b722b7008458e4c91684c73765af2e113a5e8464cd6919230b1572f` | MATCH |
| 43 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/realization_morphology.json` | 4643 | `ea8a64ec5b4e2f0b9037ab2e19913f81076ef8a38af127f21eebfa066ba084aa` | `ea8a64ec5b4e2f0b9037ab2e19913f81076ef8a38af127f21eebfa066ba084aa` | MATCH |
| 44 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/realization_stability.json` | 1162 | `37068b2e99d4fbaec33547cb1cdb6f96bc0984468225cd88927123c087d2e870` | `37068b2e99d4fbaec33547cb1cdb6f96bc0984468225cd88927123c087d2e870` | MATCH |
| 45 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/realization_stability_sweep.json` | 80054 | `0e656b7b45498cbbf5088aa80539bfa03c0600f8a6829ac0563af16a2faba7b8` | `0e656b7b45498cbbf5088aa80539bfa03c0600f8a6829ac0563af16a2faba7b8` | MATCH |
| 46 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/realization_sweep.json` | 75909 | `cea7a4adf1acb4930c8a2bbf7535679559ee4caf17b53e47cb46f6447231aec7` | `cea7a4adf1acb4930c8a2bbf7535679559ee4caf17b53e47cb46f6447231aec7` | MATCH |
| 47 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/reference_stability.json` | 967 | `980ae201d4d01fc4790c867fe40044da00789c65d28eef4458dff53d94e62cb7` | `980ae201d4d01fc4790c867fe40044da00789c65d28eef4458dff53d94e62cb7` | MATCH |
| 48 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/resource_benchmark.json` | 2235 | `1356aeea7148b520e06b089b51d97f5bb08ae5610b3aa5976d7905c93a9fc87f` | `1356aeea7148b520e06b089b51d97f5bb08ae5610b3aa5976d7905c93a9fc87f` | MATCH |
| 49 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/skeleton_assessment.json` | 3097 | `c86c41d767c64e44170a1a3f0263d68c9641ce6db5c14ce567a6792e924056a5` | `c86c41d767c64e44170a1a3f0263d68c9641ce6db5c14ce567a6792e924056a5` | MATCH |
| 50 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/skeleton_high_sweep.json` | 74749 | `5971275f9692da6874286328b747b23d5350aea3eca52fae7ac78311654388c8` | `5971275f9692da6874286328b747b23d5350aea3eca52fae7ac78311654388c8` | MATCH |
| 51 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/skeleton_low_sweep.json` | 74725 | `764b3025c5f3708b024a933f421b598ba37f9327666320b34d55f356d98b0e79` | `764b3025c5f3708b024a933f421b598ba37f9327666320b34d55f356d98b0e79` | MATCH |
| 52 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/skeleton_stability.json` | 1172 | `33882615a5fe57fed1680f7e7871a19a760ddb325c30697c66c21b7c9fb85026` | `33882615a5fe57fed1680f7e7871a19a760ddb325c30697c66c21b7c9fb85026` | MATCH |
| 53 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/skeleton_stability_sweep.json` | 78881 | `d17520c1c93f91cc69383df6321e4f71b37ab93363e39b2d53d37a22a05d60d0` | `d17520c1c93f91cc69383df6321e4f71b37ab93363e39b2d53d37a22a05d60d0` | MATCH |
| 54 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/stage1_package.json` | 7297 | `71ffee2bbc6db0f99227311471f9cb41b2574e472d1fdc953a644d6595cc050e` | `71ffee2bbc6db0f99227311471f9cb41b2574e472d1fdc953a644d6595cc050e` | MATCH |
| 55 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/tolerance_ensembles.json` | 81600 | `4e99b1c9d6f083c01d83821d0f1f14481a7d43ceae2d54bd8dd900a81b3965d3` | `4e99b1c9d6f083c01d83821d0f1f14481a7d43ceae2d54bd8dd900a81b3965d3` | MATCH |
| 56 | `flights/mfa_fidelity/governance/f8_stage1/prerequisites/package/tolerance_program.json` | 856 | `22d8e24c6a53d818babd7579a2c9b53f0454e6395e93ef0caf6e1063aed60b95` | `22d8e24c6a53d818babd7579a2c9b53f0454e6395e93ef0caf6e1063aed60b95` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | 10709 | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | 10658 | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | 15781 | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | 70535 | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | 21017 | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 64 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | 23168 | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 65 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | 63877 | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 66 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | 70711 | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 67 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | 148653 | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 68 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | 25520 | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 69 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | 561 | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 70 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | 67551 | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 71 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | 17097 | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 72 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | 49592 | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 73 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | 26552 | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 74 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | 8782 | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 75 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | 46561 | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 76 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | 45048 | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 77 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | 209594 | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 78 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | 28619 | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 79 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 80 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | 12032 | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 81 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 82 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | 30477 | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 83 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | 41677 | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 84 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | 3839 | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 85 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | 6151 | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 86 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | 45326 | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 87 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | 11726 | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 88 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | 3288 | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 89 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | 66542 | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 90 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | 6076 | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 91 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | 6260 | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 92 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | 2228 | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 93 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | 9732 | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 94 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | 26324 | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |
| 95 | `flights/mfa_fidelity/instrument/tests/test_f8_m1.py` | 21544 | `ca9a547286290aabc497fc228e10dd845711cd1b359bc21fcb125d92e8285007` | `ca9a547286290aabc497fc228e10dd845711cd1b359bc21fcb125d92e8285007` | MATCH |
| 96 | `flights/mfa_fidelity/instrument/tests/test_f8_m2_m3.py` | 22505 | `d0d26e75280dffef269e05f95e391b1db775a0f4712a5b3eac2f31ff50336460` | `d0d26e75280dffef269e05f95e391b1db775a0f4712a5b3eac2f31ff50336460` | MATCH |
| 97 | `flights/mfa_fidelity/instrument/tests/test_f8_m4.py` | 10673 | `8b8976b2c3602e0cc3932676cc6a091c69569af515bc183c374208578afa6d12` | `8b8976b2c3602e0cc3932676cc6a091c69569af515bc183c374208578afa6d12` | MATCH |
| 98 | `flights/mfa_fidelity/instrument/tests/test_f8_m5.py` | 25374 | `27cb5c965242ad2bde9aa61c5403eb97473190b67b1d232a2d801c5bd2097b41` | `27cb5c965242ad2bde9aa61c5403eb97473190b67b1d232a2d801c5bd2097b41` | MATCH |
| 99 | `flights/mfa_fidelity/instrument/tests/test_f8_m6.py` | 29979 | `808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca` | `808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca` | MATCH |
| 100 | `flights/mfa_fidelity/instrument/tests/test_f8_m7.py` | 86462 | `47b7a25c814390dc493f194ef1ba2ab6f97251559c8cb9f9e7df2d67f786b29e` | `47b7a25c814390dc493f194ef1ba2ab6f97251559c8cb9f9e7df2d67f786b29e` | MATCH |
| 101 | `flights/mfa_fidelity/instrument/tests/test_f8_mp1.py` | 34102 | `f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d` | `f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d` | MATCH |
| 102 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | 3849 | `6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86` | `6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86` | MATCH |
| 103 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md` | 12439 | `198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034` | `198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034` | MATCH |
| 104 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md` | 9154 | `6ebf0ad3efbe8e0e74b45e63d5f6ba550441897f3ff6898749230c064c993e9e` | `6ebf0ad3efbe8e0e74b45e63d5f6ba550441897f3ff6898749230c064c993e9e` | MATCH |

## Verification boundary and next step

This receipt establishes agreement with the user-supplied archive and manifest identities, complete payload coverage, and a match for every payload hash. Soundness of the chain, the P1 determination including T-S1c, the ranked disposition, Section 5 open items, and claim language have not been reviewed.

Stopped after receipt verification. Awaiting “execute.”
