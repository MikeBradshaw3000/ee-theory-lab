| Receipt check | Result | Status |
|---|---|---|
| Archive | `f9_m4_build_round1_L2.zip` | RECEIVED |
| Archive SHA-256 | `05abf794965f4b785069806671963fc57f401cb899dfbb4046de9b5976b19fa4` | MATCH — supplied hash |
| File count | 63 payload files + `MANIFEST.txt` = 64 files | MATCH |
| Manifest entries / full payload hashes | 63 entries; 63/63 full SHA-256 digests match | PASS |
| Missing, unlisted, duplicate or unsafe archive paths | None | PASS |
| ZIP integrity | CRC checks passed | PASS |
| `MANIFEST.txt` SHA-256 | `60a02dd0ac9dac00ebdfd2c03088dc011466ba21a6de194e397171d202aca68b` | COMPUTED — no separate expected hash supplied |
| Review authorization | Receipt returned before review; Mike then said “execute” | SATISFIED |

| # | Payload file | Computed SHA-256 | Against MANIFEST.txt |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M4_BUILD_PACKET_2026-11-17.md` | `674d1acc269f0d0e64b23be50aa16485e479165bc284764dd39b1b44c01bd848` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` | `6523da486b8bd9af02e3635e80e1f67434eb7cc8995caa3f8f6a5247bc7319c7` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` | `c379c3a2756e7b58bda07177a039488babf7ba2510f51a4491fcd0fd08d0f345` | MATCH |
| 4 | `flights/mfa_fidelity/build_records/f9_m4_module_container_2026-11-17.txt` | `e6fbe3c584a82b8d5c89374f96e1dcab1cbe6dfb9628b2a52342b5e71a906e68` | MATCH |
| 5 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 6 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 7 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 8 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 9 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 10 | `flights/mfa_fidelity/build_records/F9_M3_PLACEMENT_NOTE_2026-11-17.md` | `2df87fe689368752f92f5e5bd90f09ccef819255b2e5b44c4b1a6526314898f7` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/L2_F9_M3_ROUND2_REVIEW_2026-11-17_RECEIVED.md` | `939dca526bdbcdbf52880e5c0b93ca988f0364d24af151f60e478cf8a219ccfe` | MATCH |
| 12 | `flights/mfa_fidelity/build_records/f9_m3_module_canonical_2026-11-17.txt` | `21c64723af05a3f767cd7f8fdb43fbd116a81efcb1b722f2d2478ab99b4c2010` | MATCH |
| 13 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` | MATCH |
| 14 | `flights/mfa_fidelity/instrument/tests/test_f9_m2.py` | `1fa1d769a384f40befc0b1be66c65d29e3baad18e074a84c2fb593482ba9cca1` | MATCH |
| 15 | `flights/mfa_fidelity/instrument/tests/test_f9_m3.py` | `7480595d2aee36d5790af405e53a0816635be2ebca5213d819a8d428c38296b2` | MATCH |
| 16 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 17 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 18 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 19 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 20 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 21 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 22 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 23 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 24 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 25 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 26 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 27 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 28 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 29 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 30 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 31 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 32 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 33 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/dynamics.py` | `34bc6843c9a354746a2cccd4f32c7422456aff9acc17b1cb6df1b48a21d1f82e` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` | `73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/streams.py` | `5e6bb8afad20530d06a91f2cf6d0c937ac22aa004b207c0c14ce4f00d0981b06` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 60 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 61 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 62 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 63 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 M4 build review, round 1

**Review date:** 2026-11-18. **Reviewer role:** L2, adversarial instrument-build review. **Decision authority:** Mike. **Packet date:** 2026-11-17. **Packet-declared repository pin:** `80306ab3d7ce4cd9712ec8bd3604a27e725f9772`.

## 1. Disposition and scope

**Repair is required before placement. There is one blocking finding: D1, incomplete arm-record consistency validation.** A purported COMPATIBLE arm can say that an informative, follows-own level is apparatus-unevaluable because its record is missing. `_check_arm` accepts that contradictory record, and `flight_b` returns PRODUCED. The same validator also ignores several other malformed or contradictory cause fields. This directly contradicts declaration M4-9 and the contract's apparatus precedence. It is an internal consistency failure within M4's declared responsibility. [P §2 M4-9; C §§5.6, 7; O `_check_arm`, `flight_b`]

The full supplied M4 test file completed: **20 passed, 1 warning in 8.94 seconds; exit code 0**. Those passing tests do not cover D1. For valid records in the declared domain, the level, arm, B, D, and persistence decision rules checked here agree with the frozen contract. M4-1 through M4-8 and M4-10 are acceptable as stated below; **M4-9 requires change**.

The review covers the two new M4 files and their declared boundaries with placed M3. The packet's reduction of M4 to outcome records and persistence is explicit. Closure comparators, T0's four scientific tests, reporting schemas, run-record survival counting, persistence/binding by the runner, and qualification remain separate work. Their omission does not invalidate this narrower M4 review, and this review does not clear their implementation. [P §1]

No packet source was edited. Only the supplied unit tests and constructed-label/count probes were executed. No lattice flight, calibration, qualification, canonical scoring, master draw, or probe-array inspection was performed. The repository pin is reported from the packet; remote HEAD was not independently fetched.

### Source register

All source citations below refer to the packet members verified in the receipt tables above. Paths are relative to the archive root.

| Citation | Source |
|---|---|
| P | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M4_BUILD_PACKET_2026-11-17.md` |
| C | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` |
| F | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` and `FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` in the same directory |
| O | `flights/mfa_fidelity/instrument/mfa_instrument/f9/outcomes.py` |
| T | `flights/mfa_fidelity/instrument/tests/test_f9_m4.py` |
| E | `flights/mfa_fidelity/instrument/mfa_instrument/f9/evaluator.py` |

The contract's retained DRAFT/PROPOSED text is interpreted through F's freeze and ratification record. This review does not reopen those frozen choices. The outcome declaration recomputed to the advertised full SHA-256, `c94ec4bd7c9aa532264ab2adc91ab6d4948ebff652b5b58380e1befb54a35407`. [F §§1, 3; O `verify_outcome_declaration`]

## 2. Execution and evidence

The whole `tests/test_f9_m4.py` was run in one pytest process from the extracted packet's `flights/mfa_fidelity/instrument` directory. The command was:

```bash
python -m pytest -vv -ra -p no:cacheprovider tests/test_f9_m4.py
```

The packet's instrument directory and an isolated pytest dependency directory were supplied on `PYTHONPATH`. The runtime was Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pytest 9.2.0, and pluggy 1.7.0. Pytest was installed outside the packet. The one warning was an existing AnyIO pytest-plugin deprecation concerning `CallSpec2`; there were no failed or skipped M4 tests.

```text
collecting ... collected 20 items
======================== 20 passed, 1 warning in 8.94s =========================
EXIT_CODE 0
```

| Evidence | Result and limit |
|---|---|
| Entire supplied M4 test file | 20/20 passed, including its declaration/label checks, outcome tables, missing-input checks, randomized sweeps, persistence checks, and placed-file identity checks |
| Flight B enumeration in the supplied tests | All 4^7 arm-determination combinations, each with qualification true and false: 32,768 evaluations |
| Other supplied sweep checks | 6,000 arm sweeps; 1,500 D sweep pairs; 4,000 persistence sweeps |
| D1 independent probes | Five malformed or contradictory COMPATIBLE arm variants were accepted and produced B = PRODUCED; a sixth apparatus arm with its causes erased was also accepted |
| Clopper–Pearson independent comparison | All 41 possible survivor counts, both bounds, checked against beta-quantile values; maximum absolute difference 4.440892098500626e-16 |
| Persistence logic | A case partition over the criterion sequence establishes the four branches for all binary profiles on the registered grid; targeted first/last-boundary and non-monotone cases also checked |
| Payload integrity after review | Every one of the 63 payload files still matches the receipt manifest; source/test bytes were unchanged |

The enumeration and randomized coverage above describe the executed test program, not independent canonical scientific observations. M1–M3 were not rerun as whole modules, and this is not a new canonical-machine or whole-repository regression claim. [T]

## 3. D1 — Arm-record cause fields can contradict the accepted determination

**Status: BLOCKING; repair within M4.**

`arm_tier` writes both the B-status partition of the informative levels and a `level_causes` map derived from the constituent level records. Its A1 branch derives the arm's apparatus causes from the unevaluable levels; A2 and A3 emit an empty top-level cause list; A4 derives its three possible causes from the informative-level partition. [O `arm_tier`]

`_check_arm` validates the registered-level lists, their partition, adjacent adverse pairs, the determination/rule pair, COMPATIBLE's supporting levels, and A4's top-level causes. It **never requires or inspects `level_causes`**, and it gives the top-level `causes` field no semantic check for A1, A2, or A3. `flight_b` then trusts the accepted determination. [O `_check_arm`, `flight_b`]

### Concrete contradiction and effect

Start with a genuine COMPATIBLE TA arm produced by `arm_tier`, whose 25 levels all follow own. At κ = 0.75, set:

```python
bad["level_causes"][750000] = [
    "apparatus unevaluable (missing level record)"
]
```

The same dictionary still says:

```text
750000 is in informative_levels
750000 is in follows_own_levels
unevaluable_levels == []
determination == "COMPATIBLE"
rule == "A3"
```

The packet accepts that record and returns PRODUCED when it occupies TA's required slot beside six genuine compatible arms. No output of `arm_tier` can contain this combination of fields. An apparatus-unevaluable level cannot simultaneously be the informative support for A3; a corrupt mandatory arm cannot support a qualified scientific flight determination. [C §5.6 arm/flight tiers; C §7 L1, A1 and Flight; P M4-9]

This finding does not assert that an actual run has produced the contradictory record. It establishes that the promised validation boundary accepts one and allows a favorable scientific label. The counterexample requires no change to M4's code, no substitution of a master, and no question about whether an otherwise consistent evaluation has real provenance.

### Other confirmed manifestations of the same defect

| Mutation to a genuine record | Observed behavior |
|---|---|
| Apparatus cause in `level_causes[k]`, while `k` remains informative and follows-own | Accepted; B = PRODUCED |
| Apparatus cause in a COMPATIBLE arm's top-level `causes` | Accepted; B = PRODUCED |
| Own-adverse cause in `level_causes[k]`, while `k` remains follows-own | Accepted; B = PRODUCED |
| Delete `level_causes` | Accepted; B = PRODUCED |
| Replace `level_causes` with integer `1` | Accepted; B = PRODUCED |
| Erase both cause structures from an arm with unevaluable levels and an A1 determination | Accepted |

These are one incomplete-validation finding, not six independent changes to the contract. The supplied negative-record test checks several other forged fields, but none of these omitted relationships. [T `test_an_arm_record_that_contradicts_itself_is_refused`]

### Required repair

Validate the complete arm representation and its cause relationships before accepting it. A satisfactory repair must:

1. Require `level_causes` with its declared mapping shape, registered integer level keys, and valid nonempty cause lists. Require the remaining fields appropriate to the arm's rule; do not silently ignore malformed required evidence.
2. Make apparatus causes and `unevaluable_levels` agree in both directions, and derive/check A1's top-level causes against the apparatus causes actually recorded at those levels.
3. Check the recorded causes against the informative-level B-status partition and the uninformative/unevaluable levels. An own-adverse cause cannot belong to a follows-own level; an informative level cannot carry an apparatus or no-edge cause. Preserve the legitimate case in which a follows-own level carries `finite resolution` because its rival is unresolved.
4. Require empty top-level causes for A2/A3 and retain A4's exact derivation in the contract's listing order. Keep COMPATIBLE's supporting-level list and field types consistent with its informative levels.
5. Reject contradictory records through the declared typed error boundary. The eventual runner must propagate that apparatus failure as required by §7. Do not select one conflicting field and silently rewrite the evidence into a scientific result.

A reconstruction/normalization design is also acceptable if it validates all the original fields against the reconstructed record before acceptance. Merely dropping `level_causes`, checking for one particular apparatus string, or deleting the contradictory cause is insufficient.

Add discriminating negatives for the six reproduced cases and the corresponding A1–A4 cause/schema relationships. Retain positive tests for all genuine arm shapes, including follows-own with rival unresolved, own-adverse with rival unresolved, multiple A4 causes, and legitimate A1 causes. The repair belongs in the two unplaced M4 files; no change to the frozen contract or placed M3 is needed for D1.

## 4. Q1 — Outcome tables and precedence

**Answer:** The rules produce the contract's decisions for valid records in their declared domain. The broader claim that every accepted input yields a qualified, internally consistent record is false because of D1. [C §§5.6, 7; O]

| Rule checked | Finding |
|---|---|
| Level result table | All six explicit own/rival rows match; the unresolved-own/any-rival row is correctly expanded into three cases |
| Same-family levels | Own and rival must agree; the discrimination status is always `not adjudicable here`, including adverse/adverse and unresolved/unresolved |
| L1 apparatus and missing levels | Explicit apparatus level records and missing registered levels correctly force A1 |
| L2 before L3–L5 on T0 | The adapter correctly returns `no eligible contour` even if M3's unavailable-map cause is no edge, under-resolved, or unstable |
| Unavailable-index agreement | One-index-only unavailability, or disagreeing unavailable causes, is refused; no declared arm needs such a combination |
| A2 adjacency | The test is adjacency on the entire 25-level grid. κ = 0.75 and 1.00 are neighbors; adverse levels separated by any registered level are not |
| A3 and A4 | At least three informative levels and all follows-own give COMPATIBLE; otherwise, after A1/A2, NOT DISTINGUISHED with the applicable causes |
| Flight B | Prerequisite failure precedes scientific labels; then any ADVERSE gives NOT PRODUCED, any remaining ND gives NOT DISTINGUISHED, and all seven COMPATIBLE give PRODUCED with domain/resolution |
| Flight D | At least three own-with-rival-excluded witnesses in each TB arm, no informative follows-rival level in either arm, and prerequisites passed; the two witness sets are retained separately |

Two details must survive the repair. First, own adverse/rival unresolved retains the adverse own status while recording both the own-adverse and finite-resolution causes; L6 does not erase the table's explicit own-adverse result. Second, D does not require each TB arm to be COMPATIBLE for B. Three witnesses plus adjacent levels that follow neither can make a TB arm ADVERSE for B while leaving D DISTINGUISHED, provided there is no follows-rival level. Adding a compatible-arm requirement to D would change the frozen contract. [C §5.6 level table and D rule; O `level_tier`, `flight_d`]

## 5. Q2 — Disposition of M4-1 through M4-10

| Declaration | Disposition | Reason / condition |
|---|---|---|
| M4-1 — Labels | ACCEPTABLE | Governed classification, cause and profile labels match the contract. Concrete apparatus keys and explanatory diagnostics are understood as disclosed explanatory wording |
| M4-2 — Level tier | ACCEPTABLE | Exact own/rival table, correct same-family restriction, and appropriate preservation of simultaneous causes |
| M4-3 — Precedence L1–L5 | ACCEPTABLE | Correct handling of declared arms, T0's constant-index override, and unavailable-pair agreement |
| M4-4 — Evaluator-cause translation | ACCEPTABLE | Explicit normalization yields the canonical labels without changing cleared M3 bytes; see Q4 |
| M4-5 — Arm tier | ACCEPTABLE | A1–A4 and registered-grid adjacency match the contract |
| M4-6 — Multiple ND causes | ACCEPTABLE | All applicable causes can be retained in listing order without adding a decision priority; see Q3 |
| M4-7 — Flight B | ACCEPTABLE | The conjunction, precedence, and PRODUCED domain/resolution are correct. Placement remains blocked by D1 at its arm-input validator |
| M4-8 — Flight D | ACCEPTABLE | The witness minimum, follows-rival veto, independent witness sets, and derivation from the same level inputs are correct |
| M4-9 — Records check themselves | REQUIRES CHANGE | D1 disproves the arm-record guarantee. The level-record reconstruction/check did not exhibit an analogous contradiction in this review |
| M4-10 — Persistence | ACCEPTABLE | Complete contracted sweep inputs yield the correct profile, threshold, bracket, endpoint treatment, and pointwise intervals; see Q5 |

These are L2 technical dispositions. Mike's ordinary governance ratification remains his decision. [P §2]

## 6. Q3 — Recording every applicable NOT DISTINGUISHED cause

**Accept M4-6. No separate scientific ruling is needed to choose a primary cause.** The contract lists three A4 causes but supplies no priority among them. Returning every cause that holds preserves the stated evidence and leaves the arm's scientific determination unchanged. [C §5.6 arm tier; C §7 A4]

The meanings used here are appropriate after A1–A3 have failed: fewer than three informative levels; an own-adverse level without the adjacent-adverse replication needed for A2; and an own-unresolved informative level. Two separated informative levels, one adverse and one unresolved, can therefore carry all three causes. The qualification row with exactly two compatible informative levels still carries only `insufficient informative levels`, as required. [C §6.2 row 19; O `arm_tier`; T arm-sweep tests]

The ordinary ratification of M4-6 should record the all-causes/listing-order convention. A future decision to designate one cause as primary would be an additional schema choice; it is not required to repair this build.

## 7. Q4 — The placed M3 cause strings

**The declared translation is sufficient now. Do not require a change to the cleared M3 bytes for this M4 review.**

| M3 label | Canonical M4 label |
|---|---|
| `no edge at theta` | `no edge at θ` |
| `below the informative minimum` | `under-resolved` |
| `unstable edge` | `unstable edge` |
| `no eligible contour` | `no eligible contour` |

The table is part of the outcome declaration, the adapter rejects unknown unavailable causes, and T0's override restores the contract's constant-index precedence. The mismatch is resolved at the consumer boundary that constructs the canonical outcome record. [E `evaluate_level`; O `EVALUATOR_CAUSES`, `level_from_evaluation`; C §7]

Qualification and outcome reporting must use the normalized M4 level state/cause when comparing with the contract's canonical outcome labels. The raw evaluator record can remain preserved as evidence. At M3's next touch, coordinate any cause renaming with this adapter and its tests: the current adapter deliberately recognizes the placed M3 spellings. This is an integration obligation, not a request to alter frozen or cleared files in this round.

## 8. Q5 — Persistence profile, threshold, bracket and endpoint records

**No defect was found on the contracted input domain: the registered 25 levels, exact integer counts from 0 through 40, criterion s ≥ 36, and fixed two-sided 95% intervals.** [C §1.3(a), §5.4; O `persistence_record`, `clopper_pearson`]

Let m_j be true exactly when the count at registered level j is at least 36. The implementation is exhaustive because:

1. If some true m_i precedes a higher false m_j, the profile is non-monotone. The implementation tests this exact condition first and withholds κ̂_c and a crossing bracket.
2. Otherwise, an all-true sequence meets the criterion everywhere, and an all-false sequence meets it nowhere.
3. Every remaining sequence must be a nonempty false prefix followed by a nonempty true suffix. Its first true level and immediate registered predecessor are precisely the contract's κ̂_c and bracket.

This establishes the profile partition for all 2^25 binary criterion sequences. Monotonicity of the raw survivor counts is not required: 40 followed by 36 still meets the criterion at both levels. A non-monotone profile's terminal passing suffix is reported separately and never promoted into a monotone crossing. [O `persistence_record`]

| Checked case | Correct record returned |
|---|---|
| All counts zero | Valid observation; criterion met at no level; no κ̂_c or bracket |
| All counts 40 | κ̂_c = 0.75, upper endpoint at 0.75, and explicit unavailable lower-side cause |
| Count 35 at 0.75, then 36 everywhere | κ̂_c = 1.00; bracket [0.75, 1.00] |
| Count 35 at the first 24 levels, then 36 | κ̂_c = 3.00; bracket [2.50, 3.00] |
| Passing level, later failure, then a passing terminal suffix | Non-monotone; κ̂_c/bracket unavailable; suffix reported descriptively |
| Passing levels followed by failure at the last level | Non-monotone; no suffix; explicit unavailable causes |
| Any missing registered level or `None` count | Apparatus missing-record result; no scientific profile |

The wider end spacings are legitimate persistence brackets. T0's separate fine-grid eligibility rule for its hysteresis exercise is not imported into §5.4. Every complete sweep retains the pointwise interval at every level, so a non-monotone suffix's descriptive interval remains available in the level map even when there is no bracket endpoint. [C §§5.4, 5.8; O `persistence_record`]

The Clopper–Pearson calculation correctly solves the lower binomial-tail equation and obtains the upper bound by binomial complementation, with exact boundary assignments at s = 0 and s = 40. All 41 count cases agreed with the beta-quantile comparison to the numerical accuracy reported in §2. For 36 of 40 the interval was approximately [0.7633626001, 0.9720745847]. The criterion uses the count, not whether an interval establishes a survival probability of at least 0.9. None of these intervals enters B or D. [C §1.3(a); O `_binom_tail_ge`, `_clopper_pearson`, `persistence_record`; T `test_clopper_pearson`]

## 9. Q6 — Accepted contradictions

**Yes, at the arm boundary: D1.** Both the omitted `level_causes` checks and the unchecked non-A4 top-level causes violate the advertised mutual consistency of an accepted arm's determination, rule, causes and level lists.

For the level boundary, `_check_level` reconstructs the record through `level_tier` or `level_apparatus`, requires the expected fields, and compares content and field types. This review found no corresponding accepted contradiction in that check. That is a scoped finding, not a claim of formal verification of arbitrary Python objects. [O `_check_level`; T level-record negatives]

Binding a consistent record to a real evaluation, terrain, composition and run remains the runner's responsibility as disclosed. D1 does not ask M4 to acquire those provenance responsibilities; it asks M4 to make its already-present fields agree. [P disclosure 6; C §5.9]

## 10. Q7 — Other matters and closure requirements

**No additional blocking contract ambiguity was identified.** Preserve the declared module boundary: closure comparators and T0's tests still need their later implementation/review; the runner still needs complete record retention and identity/error binding; and the qualification stage must use the normalized outcome records. This review supplies no authorization for those jobs. [P §1; C §§5.8, 5.9, 8]

One **nonblocking helper-domain observation** is recorded for accuracy. The public `clopper_pearson` helper exposes an optional `tail` argument without validating its domain. On these bytes, `clopper_pearson(20, 40, float("inf"))` returns `(1.0, 0.0)`, and a tail of 0.75 produces reversed bounds. The contracted persistence entry always calls the helper at the frozen tail 0.025, so no valid persistence sweep reaches this behavior. This does not change M4-10's disposition. A general-purpose version of the helper should validate a finite real tail strictly between 0 and 0.5, or remove that public option. [O `clopper_pearson`, `_clopper_pearson`, `persistence_record`]

For the next build-review round, return the changed M4 source and test identities, D1's rejection evidence through the public `flight_b` boundary, the expanded discriminating negative and positive tests, and a complete M4 test-file result. Keep the scientific tables, normalized-cause convention, frozen contract, and placed M3 identity intact unless a further change is separately disclosed. All six counterexamples below must cease to be accepted as valid arm records, and genuine constructor-produced records must continue to pass.

## Appendix A — Executable D1 reproduction

Save the following program as `reproduce_f9_m4_r1.py` and run it with the unpacked packet root as its one argument. It checks the original M4 source digest before importing it. All inputs are constructed level labels; it does not execute the lattice rule.

```bash
python reproduce_f9_m4_r1.py /path/to/unpacked-packet
```

```python
"""Reproduce D1 against an unpacked Flight 9 M4 round-1 packet.

Usage: python reproduce_f9_m4_r1.py /path/to/unpacked-packet
Only constructed level labels and dictionaries are used.
"""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import sys

packet = Path(sys.argv[1]).resolve()
instrument = packet / "flights/mfa_fidelity/instrument"
source = instrument / "mfa_instrument/f9/outcomes.py"
expected = "6523da486b8bd9af02e3635e80e1f67434eb7cc8995caa3f8f6a5247bc7319c7"
assert sha256(source.read_bytes()).hexdigest() == expected, "wrong M4 source bytes"
sys.path.insert(0, str(instrument))
from mfa_instrument.f9 import config as C, outcomes as O

assert O.verify_outcome_declaration() == (
    "c94ec4bd7c9aa532264ab2adc91ab6d4948ebff652b5b58380e1befb54a35407"
)
good_arms = {
    terrain: O.arm_tier({
        level: O.level_tier("compatible", "compatible", O.is_same_family(terrain))
        for level in C.F9_LEVELS_MICRO
    })
    for terrain in C.F9_REQUIRED_TERRAINS
}
assert O.flight_b("P", good_arms, True)["B"] == "PRODUCED"
k = C.F9_LEVELS_MICRO[0]
base = good_arms["TA"]
variants = {}

bad = deepcopy(base)
bad["level_causes"][k] = ["apparatus unevaluable (missing level record)"]
assert k in bad["informative_levels"] and k in bad["follows_own_levels"]
assert bad["unevaluable_levels"] == [] and bad["determination"] == "COMPATIBLE"
variants["apparatus level cause but COMPATIBLE"] = bad

bad = deepcopy(base)
bad["causes"] = ["apparatus unevaluable (missing level record)"]
variants["apparatus arm cause but COMPATIBLE"] = bad

bad = deepcopy(base)
bad["level_causes"][k] = ["no registered contour of own index within ε"]
variants["own-adverse cause but follows-own level"] = bad

bad = deepcopy(base)
del bad["level_causes"]
variants["missing level_causes"] = bad

bad = deepcopy(base)
bad["level_causes"] = 1
variants["non-dict level_causes"] = bad

for label, bad in variants.items():
    arms = deepcopy(good_arms)
    arms["TA"] = bad
    accepted = O._check_arm(bad) is bad
    result = O.flight_b("P", arms, True)["B"]
    assert accepted and result == "PRODUCED"
    print(f"{label}: accepted={accepted}, B={result}")

bad = O.arm_tier({level: O.level_apparatus("missing") for level in C.F9_LEVELS_MICRO})
bad["causes"] = []
bad["level_causes"] = {}
assert O._check_arm(bad) is bad
print("apparatus arm without any cause: accepted=True")
```

Observed output on the verified round-1 bytes:

```text
apparatus level cause but COMPATIBLE: accepted=True, B=PRODUCED
apparatus arm cause but COMPATIBLE: accepted=True, B=PRODUCED
own-adverse cause but follows-own level: accepted=True, B=PRODUCED
missing level_causes: accepted=True, B=PRODUCED
non-dict level_causes: accepted=True, B=PRODUCED
apparatus arm without any cause: accepted=True
```

The program's assertions are intentionally evidence assertions for the defective round-1 bytes. After repair, the corresponding regression tests must instead require typed rejection of the altered records, with positive controls for valid records.

FINAL VERDICT: DEFECT-WITH-REPAIR
