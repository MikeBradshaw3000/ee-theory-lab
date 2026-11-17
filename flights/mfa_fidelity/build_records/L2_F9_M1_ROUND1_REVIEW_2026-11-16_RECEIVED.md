| Receipt check | Verified result | Status |
|---|---|---|
| Archive | `f9_m1_build_round1_L2.zip` | Received |
| Archive SHA-256 | `58bc4f4f72158f41bd50db332e3265c6f15c3fe267e56f4b0fad3ab6a56e73d3` | MATCH — user-supplied digest |
| File count | **59 payload files + MANIFEST.txt = 60 files** | Verified |
| Manifest entries | 59 | Verified |
| Payload hashes | **59/59 match MANIFEST.txt** | PASS |
| Missing / unlisted payloads | 0 / 0 | PASS |
| Duplicate archive / manifest paths | 0 / 0 | PASS |
| ZIP CRC verification | All files passed | PASS |
| Receipt and authorization | Receipt completed before review; Mike subsequently instructed “Execute” | Review authorized |

| # | File (path within archive) | Computed SHA-256 | Against MANIFEST.txt |
|---:|---|---|---|
| — | `MANIFEST.txt` | `fffbf1a9d448f215bf78e63582cc741a31547dd158552e41e3462e3e8a9a2241` | Not self-listed; digest recorded |
| 1 | `flights/mfa_fidelity/build_records/L1_TO_L2_F9_M1_BUILD_PACKET_2026-11-16.md` | `8a745405a978c67ceb545827ade6ee614577ff00d0587ed0be597d0d7e24b205` | MATCH |
| 2 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/__init__.py` | `7bc7272e9c9226abced656ecda88f05f843565ffce52f2ad0730d227c5ed914e` | MATCH |
| 3 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/config.py` | `4d285b1ffab2ac224439ff9f8f9afd3d9475e4648a4edb5bd0814f7a955b7d19` | MATCH |
| 4 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/terrain.py` | `3d9143c1c2aed79aa9821370ae00cd5502233ab4f1ece6a5b1f4a0b616e29c3e` | MATCH |
| 5 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/geometry.py` | `122a0f74b52f6714438f02904a136b8e4802fdddce84bb2c69215d6d2d3a7971` | MATCH |
| 6 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/family.py` | `51d7a1783cd9fff73d6c7baf75213d1bff00a98f3d9d44f4eae8690f0e05f347` | MATCH |
| 7 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/spectral.py` | `218a93851c68a1f43ffe3f8d7856643e3964dbe8ad0249b9c4d726aab4508743` | MATCH |
| 8 | `flights/mfa_fidelity/instrument/mfa_instrument/f9/identities.py` | `f8911aec56589d0f693121a4f30fd03a42a01fe5107612c94b91d3ae71693146` | MATCH |
| 9 | `flights/mfa_fidelity/instrument/tests/test_f9_m1.py` | `5666155776988248fb99da9987f732ffb15a3d6ca2ad69318b312e6ad4600497` | MATCH |
| 10 | `flights/mfa_fidelity/build_records/f9_m1_module_container_2026-11-16.txt` | `8e7864968bbd7224047f7f48b4291ddf79a947b4abf65a64af84cb3d4873f8bd` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/F9_M1_IDENTITIES_CONTAINER_2026-11-16.json` | `46809209f690843e021182a39857a9a4ff05abdaaf1ad20c4bb72155a748cc91` | MATCH |
| 12 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` | `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168` | MATCH |
| 13 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` | `66fa3d31263b61dc6a44fe4c8e3eb0b1d8971c273f9d2ccf7c793741add3e19c` | MATCH |
| 14 | `flights/mfa_fidelity/contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` | `799030e6c7d95079b9466afbd24dab41bda2b1324c67db562fedc9621121d6c3` | MATCH |
| 15 | `flights/mfa_fidelity/contracts/flight9/README.md` | `f016dc6cb5e3011cae6dfeb6d16718d63b46f61ab6b96af09e145839aafacc76` | MATCH |
| 16 | `flights/mfa_fidelity/contracts/flight9/L2_F9_CONTRACT_V0_7_ROUND6_REVIEW_2026-11-15_RECEIVED.md` | `33310f3b810e046da05d52be01b8740bfe89a0bfe9f10e216755a382205a599b` | MATCH |
| 17 | `flights/mfa_fidelity/contracts/flight9/arith_v0_4/f9_evaluator_proto_v4.py` | `dc934c2716a69caa68c6a471010e26bfa06c93c94e63bb81f8b71bafbff4813a` | MATCH |
| 18 | `flights/mfa_fidelity/contracts/flight9/arith_v0_4/f9_compare.py` | `7fedb347cd40ba5f41c5e096919cb8ce56f3cbf7bd3c09fb801ea94298270fa2` | MATCH |
| 19 | `flights/mfa_fidelity/contracts/flight9/arith_v0_4/l2_appendix_r.py` | `afe6b99f62afeefc11c93b57a36c3cbdcb4f5cd3dae6b7db7938ad8c7f1abee8` | MATCH |
| 20 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_2.md` | `6d2570d3e1c0a131927e62ba7008ac9ec9b1a4916c68f548ae4a2e9fc79729b0` | MATCH |
| 21 | `flights/mfa_fidelity/design/flight9/probe/f9_probe.py` | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` | MATCH |
| 22 | `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 23 | `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| 24 | `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| 25 | `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| 26 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 27 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| 28 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| 29 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| 30 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| 31 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| 32 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| 33 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| 34 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 35 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 36 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 37 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 38 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 39 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 40 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 41 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 42 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 43 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| 44 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 45 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| 46 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| 47 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| 48 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| 49 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| 50 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| 51 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| 52 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| 53 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| 54 | `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| 55 | `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| 56 | `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| 57 | `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| 58 | `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| 59 | `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |

# L2 — Flight 9 M1 build review, round 1

**Date:** 2026-11-16. **Reviewer:** L2. **Decision authority:** Mike. **Register:** module build review. **Declared repository pin:** `b2a567415bd0a7af1a71c7e8531f536f1950aa69`.

## 1. Disposition and scope

**M1 requires repair before placement.** There are three repair groups: the component identity omits component membership; the bundle's deep verifier accepts incomplete or contract-inconsistent records; and the production preflight does not check the excluded numerical η₀ against its declared rule. R1 also includes a contained correction to the promised little-endian serialization of family levels. These are implementation repairs under the existing frozen contract. I identify no contract ambiguity requiring a new ruling from Mike. [C §3.4, §5.5; F `family_summary`; I `verify_bundle_deep`; K `verify_frozen_identity`.]

The present terrain formulas, comparison-array construction, edge tracer, family enumeration and spectral computation on the fifteen declared arms passed the checks described below. **All 67 supplied M1 tests passed**, including the SciPy comparison. The disposition rests on additional counterexamples that those tests do not cover. The actual submitted η₀ is correct; R3 concerns the preflight's missing rule-to-value check. [T; G; F; S; K; U; independent checks in §§3–5 and Appendix R.]

This review uses the attached bytes and the governing records in the packet. The repository pin is the packet's declared provenance; I have not independently fetched that commit. Contract v0.7 is treated as frozen by its freeze record, despite the retained draft labels in the contract text. The review does not reopen the round-6 contract clearance. All 59 extracted payload files were rehashed after the work and remained unchanged. [P introduction; FR §§1–4; R6 §1; receipt above.]

No source repair, placement, canonical job, master draw, dynamics run, calibration or boundary-endpoint calculation was performed. Bundle builds below are noncanonical test fixtures of the kind the packet authorizes. L1 repairs; Mike remains the decision authority. [P §§1–3, 7; C §8.]

### Source keys

Paths below are relative to `flights/mfa_fidelity/`. Their exact SHA-256 identities are in the receipt table.

| Key | Source |
|---|---|
| P | `build_records/L1_TO_L2_F9_M1_BUILD_PACKET_2026-11-16.md` |
| C | `contracts/flight9/FLIGHT_9_CONTRACT_v0_7.md` |
| FR | `contracts/flight9/FLIGHT_9_FREEZE_RECORD.md` |
| FA | `contracts/flight9/FLIGHT_9_FREEZE_RECORD_ADDENDUM_1.md` |
| N | `rulings/NOTATION_SCOPE_RULING_v1_2.md` |
| R6 | `contracts/flight9/L2_F9_CONTRACT_V0_7_ROUND6_REVIEW_2026-11-15_RECEIVED.md` |
| K, T, G, F, S, I | Respectively `config.py`, `terrain.py`, `geometry.py`, `family.py`, `spectral.py`, `identities.py` under `instrument/mfa_instrument/f9/` |
| U | `instrument/tests/test_f9_m1.py` |
| PR | `design/flight9/probe/f9_probe.py` |
| IR | `build_records/F9_M1_IDENTITIES_CONTAINER_2026-11-16.json` — noncanonical evidence |

## 2. Q1 — Computation and verification findings

### 2.1 Supplied tests and review environment

The supplied command, run from `flights/mfa_fidelity/instrument/`, completed as:

```text
python -m pytest tests/test_f9_m1.py -q
67 passed in 51.26s
```

The review runtime was Python **3.12.14**, NumPy **2.3.5**, SciPy **1.17.0**, on little-endian Linux. Pytest was supplied through an existing local dependency directory, with third-party plugin autoload disabled; no submitted test or source was changed. SciPy was present, so the all-arm Lanczos check was executed. This is a review-environment result, not a canonical-machine result. [U; L2 execution record.]

### 2.2 Independent positive checks

| Object | Independent check and result |
|---|---|
| All eight terrain bases | Compared all **240,000** entries against scalar implementations of the frozen formulas. Largest absolute difference: **2.220446049250313e-16**. All eight full base-array hashes also equal IR's values on this runtime. |
| TD cores | Independently derived membership with integer squared-distance inequalities. All **40,000** mask entries across the four variants agree; each core has exactly **2,000 cells**. Minimum edge clearances are **0.031442463013444666** cells for the single-disc cores and **0.060321687985828376** for the four-disc cores, both above 0.03. |
| TB roles | Product variance shares are **0.5172726278353567** along x and **0.48272737216464323** along y. Largest fall of H along increasing P is **0.08756097840204707**. |
| Same-family relation | TA, TC and all four TD variants use the prescribed shared latent array. Largest raw-index fall is **zero** in every composition. Largest recorded spread inside a rounded level class is **9.828249325494198e-13**. |
| Edge tracer | An independent directed-edge loop walk agreed on every canonical midpoint and every canonical component label in **1,551 cases**: all 512 local 3×3 binary patterns at three placements, including seams, plus 15 full-grid random masks. |
| Registered families | The supplied exhaustive-level checks and source inspection establish the prescribed distinct levels other than the minimum, inclusive threshold ties, proper masks and strict nesting. T0's constant comparison array has an empty family. |
| Spectral routine | The M1 routine and the committed probe function returned **exactly equal floats on all fifteen declared arms**. Independent Lanczos comparisons were within approximately **3.01e-12 relative**, comfortably below 1e-9. Details are in §7. |

These results support the formulas, geometry and declared numerical domain. They do not establish the completeness of the verifier; the independent negative checks in R1–R3 address that different obligation. [C §§2.8, 3.1–3.4, 5.5(3–5); T; G; F; S; U; PR; IR; L2 independent checks.]

### 2.3 Family counts on this runtime

The registered counts and the proper-level counts before rounding match the provisional container figures here:

| Comparison array | Registered contours | Proper levels before rounding |
|---|---:|---:|
| TA.shared | 1,300 | 2,221 |
| TC.shared | 1,180 | 1,389 |
| TD-1-2.shared | 681 | 861 |
| TD-1-4.shared | 920 | 920 |
| TD-4-2.shared | 250 | 250 |
| TD-4-4.shared | 250 | 250 |
| TB.P | 2,600 | 3,840 |
| TB.H | 50 | 59 |

This agreement is an observed result, not a new exact-count requirement for the canonical machine. [C §3.4(1,3,5); FR §4; U `test_container_values_are_reported`; L2 test output.]

## 3. R1 — Bind the traced component partition and honor the declared byte order

**Status: REQUIRES CHANGE before placement.**

**Affected declaration:** M1-2. **Affected source:** F `family_summary`. **Contract basis:** C §3.4(4) binds the contour families with their traced components; §5.5(3) defines those components; §5.5(6) uses each resolved component's member bonds separately.

### 3.1 Component counts and sizes do not identify membership

The submitted component digest hashes, for each level, only:

```python
(e.n_bonds, len(sizes)) + sizes
```

It does not hash `e.component`, the assignment of each canonical bond to its component. Different partitions with the same ordered sizes therefore have the same serialized input to the hash. This is missing information, not a cryptographic collision. [F `family_summary`; G `Edge`.]

The discriminating witness holds the comparison array, masks, levels and canonical bond points fixed:

```python
x, y = np.indices((100, 100))
omega = ((x // 10 + y // 10) % 2).astype(np.float64)
mask = omega >= 1
```

The correct tracer on `mask` and the complement's corner pairing on the same boundary bonds give:

| Property | Observed result |
|---|---|
| Canonical bond points | Identical |
| Bond count | 2,000 in both |
| Component count | 50 in both |
| Ordered component sizes | `(40,) * 50` in both |
| Canonical bond labels that differ | **1,500** |
| Resolved components at m = 40 | Every component |

When only the tracer's returned partition is substituted inside `family_summary`, **the entire summary remains identical for the same original `omega`**. Its component digest under both partitions is:

```text
072ee418624df7043a2bb83433764981c3b5ccbd79d2fdacd492e6d0f31ec55f
```

This does not allege that `geometry.edge` currently uses the wrong corner rule; the independent tracer confirms that it uses the correct one. It shows that the identity cannot distinguish the correct traced object from a different partition of the same bonds. Because the component term of S operates on those member sets, their identity must bind membership. [C §5.5(3,6); G; F; Appendix R, component witness.]

**Repair:** hash the complete per-bond component-label vector in M1-1's canonical bond order and component numbering, with explicit integer byte order. Counts and sizes may remain as metadata. The family/mask identity plus the declared enumeration already determines the bond locations; including the locations in the component identity is also acceptable. Do not change the corner rule. Update the declaration and noncanonical identity evidence to the repaired serialization. [P M1-1–M1-2; C §3.4(4).]

**Closure test:** the fixed-input witness must retain identical masks and points while producing different component identities. Keep the exact-partition geometry checks so a correct digest does not substitute for a correct tracer.

### 3.2 The family-level scalar does not preserve requested endian order

The family hash currently serializes a level with:

```python
np.float64(ell).astype("<f8").tobytes()
```

A NumPy scalar does not retain the requested nonnative byte order in this operation. On the review's little-endian runtime, requesting big-endian bytes demonstrates the issue:

```text
np.float64(1.25).astype(">f8").tobytes().hex()
    000000000000f43f
np.asarray([1.25], dtype=">f8").tobytes().hex()
    3ff4000000000000
```

Thus the current implementation satisfies the promised little-endian level encoding on this runtime, but the expression does not implement that promise independently of host byte order. No big-endian machine was used in the review, and no failure on Mike's canonical machine is claimed. [F `family_summary`; P M1-2; L2 byte-order probe.]

**Contained repair:** use `struct.pack("<d", ell)` or `np.asarray([ell], dtype="<f8").tobytes()`. This belongs in the M1-2 repair; it changes no scientific convention and leaves the existing little-endian level bytes unchanged.

## 4. R2 — Make deep bundle verification check the declared objects and their relationships

**Status: REQUIRES CHANGE before placement.**

**Affected declaration:** M1-3. **Affected source:** I `load_bundle`, `verify_bundle_deep`, and the inputs trusted by `compare_bundles`. **Contract basis:** C §2.8, §3.4(3–5), and §8 step 1. The submitted deep verifier explicitly promises to establish that the recorded families and spectral values follow from the stored arrays. [I function documentation.]

### 4.1 Four independent inconsistent records were accepted

Starting from a valid bundle produced by the unmodified M1 test fixture, I made separate copies and applied the changes below. Every case was written as canonical JSON and passed the **unmodified** `verify_bundle_deep`.

| Case | Change from the valid bundle | Observed outcome |
|---|---|---|
| Missing required records | Set `arms`, `families` and `same_family` to empty dictionaries; retain all 32 declared array files and their hashes. | **Accepted** with no arm or family verification. |
| Incorrect spectral gain | Change only TB.H's `g_spec` from **0.35601091903804205** to **0.7120218380760841**. | **Accepted**, although g_spec is doubled and spr and the bases are unchanged. |
| Wrong comparison array | Replace `omega/TB.H.f64` with TB.P's bytes; update its array hash and replace TB.H's family summary with TB.P's summary. Keep H's raw-index and spectral data unchanged. | **Accepted**, although the H comparator now uses P's registered family. |
| Wrong arm-to-family binding | Change only TC.H's `omega_key` to `TB.P`; leave every array byte unchanged. | **Accepted**, although TC.H no longer points to its required shared-u family. |

The first case succeeds because the deep checks iterate over whatever dictionaries the record supplies. The second succeeds because only spr is checked, not g_spec. The third succeeds because each stored comparison array is checked against its own hash and summary, without checking the prescribed relationship to its stored bases. The fourth succeeds because the arm's key, terrain, composition and family reference are not reconciled with the fixed arm table. [I `load_bundle`, `verify_bundle_deep`; K `F9_ARMS`, `F9_SAME_FAMILY_LATENT`; T `comparison_array`; Appendix R.]

The third case is especially material: TB's two distinct comparison families are the basis of the declared discrimination endpoint. A semantically wrong H family must not pass the verifier merely because its own hashes have been updated consistently. No endpoint was evaluated to establish this defect. [C §§3.3, 3.4(3), 5.5(5); Appendix R.]

### 4.2 Required repair

The checked bundle interface must enforce these invariants from the frozen declarations and stored bytes:

1. **Complete domains.** Require exactly the declared terrains, fifteen arms, eight comparison families and six same-family terrains. Require the associated fields and valid types. Checks must range over the required domain, not only supplied entries.
2. **Correct references.** Each arm key must agree with its terrain, composition and expected `omega_key`. Preserve T0's separate constant/empty-family case. Check the same-family references and recorded assertions against the actual required shared objects.
3. **Comparison-array derivation.** Recover TA/TD's common base, TC's u, or TB's raw composition from the stored bases; apply the prescribed 12-place comparison rule; verify the corresponding stored ω. Do this from the stored bases, without regenerating terrain through `cos` or `tanh`.
4. **Spectral relationships.** Check both spr and g_spec, including `g_spec = q / (Δt * spr)`, under the declared same-machine and cross-platform numerical policy. Validate the fixed metadata and derived scientific fields that downstream jobs are permitted to trust.
5. **Trusted comparison inputs.** Make `compare_bundles` operate on semantically verified bundles, or give it an explicit checked-input contract. Unchecked record assertions about masks must not be presented as independently verified mask agreement.

The repair may distinguish a lightweight loader from the full semantic verifier. It need not repeat every expensive check on every read if the runner later binds a previously verified immutable object. What is required now is one complete, truthful M1 verification path and clear guarantees for its callers. [C §3.4; I module/function declarations; P Q5.]

### 4.3 Boundary with the future runner

These probes deliberately change the record's hash. They do **not** show that a trusted external digest can be bypassed, and they are not a request for M1 to authenticate a job authorization. The future runner may bind the authorized record identity, source identity and atomic publication. M1-9 legitimately defers that work. [P M1-9; C §§5.9, 8.]

The present defect is narrower: M1's existing semantic verifier accepts a record that is incomplete or contradicts the declared mathematical relationships. A coherent replacement that satisfies all frozen relationships is a different issue from the four invalid cases above. External authenticity and internal consistency are separate obligations.

**Closure tests:** require rejection of each of the four cases separately; retain successful exact round-trip, repeated build, canonical JSON, array-tamper and cross-platform-tolerance checks. Include an explicit unchanged-valid-bundle control. Update the documentation to describe precisely what the loader, deep verifier and runner each establish.

## 5. R3 — Bind the excluded numerical η₀ to its recorded rule

**Status: REQUIRES CHANGE before placement; narrower than R1 and R2.**

**Affected declaration:** M1-5. **Affected source:** K `F9_ETA0`, `F9_DECLARATION`, `verify_frozen_identity`. **Basis:** the frozen floor rule and M1's own promise to check frozen literals against their rules. [C §2.6; FR §3, “Already RULED”; K module and preflight documentation.]

Representing η₀ in the declaration digest by `"-ln(1 - 0.01)"` is acceptable. It avoids making a declaration identity depend on a possible libm rounding difference. The missing step is checking that the numerical `F9_ETA0` actually follows that bound rule. The preflight currently checks neither that relationship nor the excluded value. [K `F9_DECLARATION`, `verify_frozen_identity`; P disclosure 5.]

In an in-memory copy of the config source, changing only:

```python
F9_ETA0 = -math.log(1.0 - 0.01)
```

to:

```python
F9_ETA0 = -math.log(1.0 - 0.02)
```

produced this result:

| Item | Observed value |
|---|---|
| Submitted η₀ | `0.01005033585350145` |
| Altered η₀ | `0.020202707317519466` |
| `verify_frozen_identity()` | **Accepted** |
| Declaration SHA-256 | Unchanged: `5784276492bdcc195562ed9e144cb599b7f6911ecf15027f0504e0045a4af30c` |

As a control, a source change to the captured μ literal is rejected by the existing digest. The failure is the deliberate float exemption without a compensating rule-to-value check. No packet file was edited. [K; Appendix R.]

The current submitted η₀ is correct, and the existing `test_declared_values_are_the_freeze_records` would detect the altered expression when the test suite runs. This finding is not a claim that the current instrument uses the wrong floor, nor a demand that M1 detect arbitrary source tampering. It is a gap in the production preflight used by `build_identity_record`. [U named test; I `build_identity_record`.]

**Repair:** retain the rule-based digest and verify the actual η₀ against the frozen expression recomputed on the same runtime. Alternatively, bind the underlying probability literal once and derive the value through one checked expression. Do not replace the rule with a universal hardcoded libm result.

**Closure test:** changing the actual η₀ while keeping the rule unchanged must fail preflight. The unchanged declaration must continue to pass on the local runtime, and its digest must not become dependent on the platform's η₀ float representation.

## 6. Q2 — Declarations M1-1 through M1-10

| Declaration | L2 disposition | Reason / required action |
|---|---|---|
| M1-1 — canonical bond order and component numbering | **ACCEPTABLE** | Explicit and reproducible; independent midpoint and partition checks agree. |
| M1-2 — family, mask and component identities | **REQUIRES CHANGE** | R1: bind per-bond component membership; use unambiguous little-endian level bytes. Family and mask content conventions are otherwise appropriate. |
| M1-3 — stored-array bundle and canonical record | **REQUIRES CHANGE** | Storage design is sound, but R2 must complete semantic verification and caller guarantees. |
| M1-4 — committed probe spectral routine | **ACCEPTABLE** | Exact returned-float agreement on all fifteen arms; correct the stopping-rule description as noted in §9. |
| M1-5 — η₀ digested by rule | **REQUIRES CHANGE** | The identity convention is acceptable; R3 must bind its actual value to that rule in preflight. |
| M1-6 — platform policy of the tests | **ACCEPTABLE** | Container sizes are provisional; numerical agreement and canonical mask identity are distinct checks. |
| M1-7 — same-family verification | **ACCEPTABLE** | The build correctly checks shared-array and mask identities and records the raw-index relation. R2 must preserve those relationships in loaded records; clarify the fall-only bound in documentation. |
| M1-8 — `is_informative` in geometry | **ACCEPTABLE** | It implements the inclusive cell and bond thresholds for the supplied region and corresponding edge; its placement does not alter the evaluator order. |
| M1-9 — deferred masters, streams, dynamics and atomic publication | **ACCEPTABLE** | These belong to later modules/runner work. This deferral does not defer the present identity and semantic-verification repairs. |
| M1-10 — environment included in the record | **ACCEPTABLE** | Environment-dependent record identities are appropriate. The environment is descriptive provenance, not proof that a bundle is the authorized canonical one. |

[P §5; C §§2.8, 3.4, 5.5, 5.9, 8; K–I; verification and counterexamples above.]

## 7. Q3 — Spectral routine and the meaning of the committed value

**Carrying the probe's routine is the correct reading of the frozen clause. No new interpretation is needed.** The M1 iteration and its imported Moore-sum helper preserve the probe's eight offsets and accumulation order. Independent comparison extracted only the probe function definitions; it did not execute the probe program or read its output arrays. Returned floats agree exactly on every declared arm. [C §2.8; PR `moore_sum`, `spectral_radius`; S `spectral_radius`; package-root `dynamics._moore_sum_a`; L2 comparison.]

The largest independently measured relative deficit against Lanczos was on TC.P:

| Quantity | L2 result |
|---|---:|
| M1/probe value | 0.728366587719911 |
| Lanczos reference | 0.7283665877221026 |
| Relative deficit | 3.0088972881966184e-12 |
| Reference eigenvector residual norm | 1.0865667508257143e-15 |

The reference used the symmetric operator, a deterministic uniform starting vector, `eigsh(tol=1e-14, ncv=40, maxiter=20000)`. All fifteen results were within 1e-9 relative. This supports the disclosed numerical accuracy on these fixed arrays. [S; U `test_routine_agrees_with_lanczos_on_every_arm`; L2 independent comparison.]

Section 2.8 identifies the canonical build's result under the committed routine as the value of record. Its 1e-9 provision governs recomputation elsewhere, with a discrepancy recorded otherwise. It does not impose a certified bound against the mathematical eigenvalue. The Lanczos comparison is additional evidence; it is not a proof of a universal error bound. A different certified solver should not be substituted silently. [C §2.8; P disclosure 2.]

The accuracy conclusion is limited to the declared F9 terrains. The routine's broad nonnegative-square-array docstring overstates what its Rayleigh-change stop guarantees. For example, an 8×8 zero array with unit entries at `(3,3)`, `(2,2)`, `(2,4)` and `(4,3)` has a K1,3 support graph: its spectral radius is `sqrt(3)/8 = 0.21650635094610965`, while the routine returns approximately `0.1875`. This synthetic matrix is outside F9's fixed positive terrain menu. It is a reason to scope the documentation accurately, not a fourth registered-arm numerical blocker or a reason to change the committed iteration. [S `spectral_radius`; K `F9_ARMS`; L2 synthetic linear-algebra check.]

## 8. Q4 and Q5 — Platform policy and the bundle design

### Q4 — Platform-dependent families

**The test policy is acceptable.** Exact provisional container sizes and transcendental-array hashes must not become undeclared canonical gates. Rounding can merge or separate values near a decimal boundary even when base arrays agree within 1e-12. The contract explicitly keeps numerical agreement, mask identity and family completeness separate. [C §3.4(1,3–5); FR §4; P disclosure 3; U module documentation.]

The existing record retains the arrays, rounded-array identities, family and mask identities, counts before and after rounding, minimum level gaps, spectral values and environment. That is sufficient evidence to investigate a platform difference once R1 and R2 make the identities and checks faithful. The canonical job should record its own objects and counts; later jobs must use those objects. A different local family is a reported comparison result, not permission to replace the canonical family. [I `build_identity_record`, `write_bundle`, `compare_bundles`; C §3.4.]

Optional diagnostic improvements are per-array deviation maxima and their locations, identities of both compared records, and witnesses identifying cells or levels responsible for a family difference. They are not additional placement conditions. The stored arrays already make those diagnostics recoverable.

### Q5 — Storing and reconstructing the canonical objects

**Storing the base and comparison-array bytes is a sound design.** Persisted ω permits exact reconstruction of its levels and masks without rerunning `cos` or `tanh`. It is not necessary to duplicate every mask in a separate file if reconstruction is deterministic and the resulting complete masks and traced components are fully bound and verified. [C §3.4(2–4), §5.5(5); T `serialize`, `deserialize`; F `Family`; I `write_bundle`.]

**The current `verify_bundle_deep` is incomplete.** R1 and R2 identify the missing checks. Once repaired, the arrangement can satisfy the canonical-object requirement while keeping storage compact. The authorized canonical record's externally trusted identity, the instrument source identity and atomic job publication remain the future runner's responsibilities. No new execution authority follows from accepting this storage design. [P M1-3, M1-9; C §§5.9, 8.]

## 9. Q6 — Conforming documentation and closure conditions

Make these documentation corrections with the repair, without changing the frozen numerical or scientific conventions:

1. **State the actual spectral stop.** It is `abs(ray - last) <= tol * max(1.0, abs(ray))`. On the registered arms, where ray is below 1, that is an absolute 1e-14 change threshold. Describing it as purely relative is inaccurate. Preserve the committed expression. [S module documentation and `spectral_radius`; K `F9_SPR_TOL`; P disclosure 2.]
2. **State which raw-index statistic is bounded.** The build records largest fall and within-level spread but enforces the 1e-12 bound on the fall, as P disclosure 4 says. I's introduction should not say both are enforced. This review does not invent an additional spread gate. [I module documentation and `_same_family_relation`; C §3.4(3).]
3. **State the loader's identity guarantee accurately.** Canonical JSON and array cross-references do not establish that the record matches an externally authorized digest. The introductory claim that the loader checks a record against “its own identity” should be replaced with the implemented guarantee and the deferred external binding responsibility. No self-referential hash field is required. [I module documentation, `load_bundle`, `record_identity`; P M1-9.]

As optional API hygiene, `terrain.level_label` could reject undeclared compositions and unknown names beginning with `TD`. Existing internal callers use declared arms, and these labels decide nothing, so this is not a placement blocker. Likewise, this review does not demand general protection against arbitrary runtime rebinding of Python globals; R3 is the specific unchecked value excluded by the chosen digest design. [T `level_label`; C §3.4(3); K.]

### Required next return

L1 should return repaired source, tests and updated noncanonical evidence for R1–R3, with each changed file identified. Closure requires the component-partition witness to be distinguished, all four invalid bundle cases to be refused, and the η₀ rule/value mismatch to fail preflight, while the valid build and the current 67 tests continue to pass. The contained byte-order and documentation corrections should accompany those repairs. No additional canonical or scientific run is requested. [P review register and §7; repair requirements above.]

## Appendix R — Reproducible negative checks

The following program reproduces the three repair groups without editing submitted source. Save the code as a scratch Python script and pass the root of the extracted packet as its only argument. It builds a temporary **noncanonical** bundle, verifies the unchanged control, and then changes separate copies. It runs no dynamics and draws no stage master. On the reviewed bytes, the four bundle cases print `ACCEPTED`, the component summaries print as equal, and the altered η₀ preflight prints `ACCEPTED`. A repaired implementation should reverse those indicated outcomes.

```python
from pathlib import Path
import copy
import hashlib
import json
import shutil
import sys
import tempfile

import numpy as np

packet = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(packet / "flights/mfa_fidelity/instrument"))
from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import family as F
from mfa_instrument.f9 import geometry as G
from mfa_instrument.f9 import identities as I


def outcome(call):
    try:
        call()
        return "ACCEPTED"
    except C.F9ConfigError:
        return "REJECTED"


# R1: fixed omega, fixed canonical bond points, different component membership.
x, y = np.indices((100, 100))
omega = ((x // 10 + y // 10) % 2).astype(np.float64)
mask = omega >= 1
correct = G.edge(mask)
other = G.edge(~mask)
assert np.array_equal(correct.points, other.points)
assert correct.component_sizes() == other.component_sizes() == (40,) * 50
assert not np.array_equal(correct.component, other.component)
a = F.family_summary(omega)
original_edge = G.edge
try:
    G.edge = lambda m: original_edge(~m)
    b = F.family_summary(omega)
finally:
    G.edge = original_edge
print("R1", json.dumps({
    "bonds": correct.n_bonds,
    "components": correct.n_components,
    "different_labels": int(np.count_nonzero(correct.component != other.component)),
    "summaries_equal": a == b,
    "component_hashes_equal": a["components_sha256"] == b["components_sha256"],
}))

# R1 endian witness; the review host is little endian.
print("byteorder", sys.byteorder)
print("scalar_requested_big_endian",
      np.float64(1.25).astype(">f8").tobytes().hex())
print("array_requested_big_endian",
      np.asarray([1.25], dtype=">f8").tobytes().hex())

# R3: in-memory altered source, unchanged bound rule; original files untouched.
source = Path(C.__file__).read_text()
old = "F9_ETA0 = -math.log(1.0 - 0.01)"
new = "F9_ETA0 = -math.log(1.0 - 0.02)"
assert source.count(old) == 1
scope = {
    "__name__": "mfa_instrument.f9._l2_eta_probe",
    "__package__": "mfa_instrument.f9",
}
exec(compile(source.replace(old, new), "<L2 in-memory eta0 probe>", "exec"), scope)
try:
    checked = scope["verify_frozen_identity"]()
    eta_result = {
        "outcome": "ACCEPTED",
        "eta0": scope["F9_ETA0"],
        "declaration_unchanged":
            checked["declaration_sha256"] == C.F9_DECLARATION_SHA256_LITERAL,
    }
except scope["F9ConfigError"]:
    eta_result = {"outcome": "REJECTED"}
print("R3", json.dumps(eta_result))


def empty_coverage(r, directory):
    r["arms"] = {}
    r["families"] = {}
    r["same_family"] = {}


def wrong_gain(r, directory):
    r["arms"]["TB.H"]["g_spec"] *= 2.0


def wrong_comparison(r, directory):
    raw = (directory / "omega/TB.P.f64").read_bytes()
    (directory / "omega/TB.H.f64").write_bytes(raw)
    r["arrays"]["omega/TB.H.f64"] = hashlib.sha256(raw).hexdigest()
    r["families"]["TB.H"] = copy.deepcopy(r["families"]["TB.P"])


def wrong_arm_binding(r, directory):
    r["arms"]["TC.H"]["omega_key"] = "TB.P"


with tempfile.TemporaryDirectory(prefix="l2_f9_m1_review_") as work:
    work = Path(work)
    control = work / "control"
    I.write_bundle(str(control))
    I.verify_bundle_deep(str(control))
    print("R2 unchanged control: ACCEPTED")
    for name, mutate in (
        ("empty_coverage", empty_coverage),
        ("wrong_gain", wrong_gain),
        ("wrong_comparison", wrong_comparison),
        ("wrong_arm_binding", wrong_arm_binding),
    ):
        directory = work / name
        shutil.copytree(control, directory)
        record = json.loads((directory / I.RECORD_NAME).read_bytes())
        mutate(record, directory)
        (directory / I.RECORD_NAME).write_bytes(I.canonical_json(record))
        print("R2", name, outcome(lambda: I.verify_bundle_deep(str(directory))))
```

FINAL VERDICT: DEFECT-WITH-REPAIR
