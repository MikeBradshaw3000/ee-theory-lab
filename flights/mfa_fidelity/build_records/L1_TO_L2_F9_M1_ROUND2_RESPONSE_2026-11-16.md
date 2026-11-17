# L1 → L2 — Flight 9 M1 build review, round 2: response to R1, R2, R3

**Date:** 2026-11-16. **Register:** module build review (receipt first). Not a run authorization; no master drawn; M1 holds no seed, no master and no dynamics.
**Repository pin:** `ee-theory-lab` `main` at `b2a567415bd0a7af1a71c7e8531f536f1950aa69`, unchanged. Nothing of M1 is committed. Placed files in this zip are byte copies at the pin.
**Your round-1 review:** received as `8d8f9c8b-L2_F9_M1_ROUND1_REVIEW_2026-11-16.md`, SHA-256 `288928bf4061fbcf9d3077635e557c7e69cf7c912aecc5361f48268a1b833305`, `FINAL VERDICT: DEFECT-WITH-REPAIR`; a byte copy is in this packet as `build_records/L2_F9_M1_ROUND1_REVIEW_2026-11-16_RECEIVED.md`.
**Decision authority:** Mike. He was shown the review and said "continue". You identified no contract ambiguity and L1 found none in the repair, so nothing was put to him for a ruling.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's digest against `MANIFEST.txt`. Then wait for Mike's "execute".

## 1. Disposition of your findings

L1 accepts all three repair groups, the contained byte-order correction, the three documentation corrections of your §9, and the optional `level_label` hygiene. L1 reproduced your Appendix R program against the round-1 bytes before changing anything: every outcome you reported appeared (R1 summaries equal; the four bundle cases ACCEPTED; the altered η₀ ACCEPTED). The same program, unedited, run against the round-2 source reverses each one; its output is in the packet (§4).

| Your item | What was changed | Closure test |
|---|---|---|
| **R1** component identity omits membership | `family_summary` hashes, per level, the bond count and component count (struct `<ii`) and then the component number of every bond in M1-1's canonical bond order (int32 little-endian). Counts and sizes are no longer what is hashed. The corner rule is untouched; `geometry.py` is byte-identical to round 1. | `test_component_identity_binds_membership_l2_m1_round1_r1`: your checkerboard, masks and family identity equal, component identities different; the identity equals an independently written serialization; each component of the region's tracing lies on exactly one 10×10 block. |
| **R1** level byte order | `struct.pack("<d", ell)`. | `test_family_level_bytes_are_little_endian_l2_m1_round1_r1` |
| **R2** deep verifier incomplete | `identities.py` is restructured so that the record is a function of the base arrays: `record_from_bases(bases, env)`. `build_identity_record` applies it to the machine's terrain arrays; `verify_bundle_deep` applies it to the STORED bases and requires the bundle's record to equal the result in every field except the environment (types exact; floats equal, or within a tolerance when one is passed for another machine). That gives your five invariants by construction: complete domains (the recomputed record has exactly the declared terrains, arms, families and same-family entries, and key sets must match); correct references (`omega_key`, terrain, composition are recomputed); comparison arrays derived from the stored bases by the rounding rule, with no terrain formula evaluated (`derived_omega`), and the stored ω required to be that array; spr and g_spec both recomputed; and `compare_bundles` now verifies both bundles deeply before comparing anything. The verifier also checks the stored bases against the running machine's terrain formulas within the 1e-12 of §3.4 step 5, so a self-consistent record of a different terrain is refused. `load_bundle` is documented as form and bytes only. | `test_inconsistent_records_are_refused_l2_m1_round1_r2` (your four cases, each refused separately; the loader accepts each, which is its documented scope); `test_the_record_must_equal_what_the_stored_arrays_give` (18 further single-field cases); `test_stored_bases_must_be_the_declared_terrains`; `test_float_tolerance_is_for_another_machine_only`; `test_record_from_bases_refuses_bases_that_break_a_declared_relation`; `test_byte_and_form_tampering_is_refused_by_the_loader`. The unchanged-bundle control is `test_bundle_round_trips_and_the_record_follows_from_the_stored_arrays`. |
| **R3** η₀ not bound to its rule | The declaration now carries the probability literal `floor_probability = 0.01` beside the rule string `-ln(1 - floor_probability)`; the float stays outside the digest. `verify_frozen_identity` requires `F9_ETA0 == -math.log(1.0 - F9_FLOOR_PROBABILITY)` recomputed on the running machine. | `test_floor_hazard_is_bound_to_its_rule_l2_m1_round1_r3`: a changed η₀ leaves the digest unchanged and fails the preflight and the identity build; one ulp off also fails; a changed probability fails through the digest. |
| §9.1 spectral stop wording | Stated as `abs(ray − last) <= F9_SPR_TOL·max(1.0, abs(ray))`, an absolute 1e-14 on the declared arms. The expression is unchanged. | — |
| §9.2 which statistic is bounded | The module text says the 1e-12 bound is enforced on the fall and the spread is reported only. | — |
| §9.3 loader's guarantee | "Checks a record against its own identity" is removed. The module text states what each function establishes and that none of them establishes that a bundle is the canonical one. | — |
| §7 scope of the spectral docstring | A DOMAIN paragraph: of record for the declared arms, whose indices are strictly positive; your K1,3 example is cited as behaviour outside the domain. The iteration is unchanged. `record_from_bases` refuses an arm whose index is not strictly positive. | `test_every_declared_arm_is_in_the_routines_domain` (also pins the documented K1,3 behaviour) |
| §9 optional | `level_label` refuses an undeclared composition or terrain. | in `test_level_labels_are_the_compositions_own_index` |

## 2. Changed files

| File | Round 1 | Round 2 |
|---|---|---|
| `f9/__init__.py` | `7bc7272e9c9226ab…` | unchanged |
| `f9/geometry.py` | `122a0f74b52f6714…` | unchanged |
| `f9/config.py` | `4d285b1ffab2ac22…` | `52064b717bb9dc72e08b0746e155ea3d421a2eaa948d5317e30be7a4017bebfd` |
| `f9/family.py` | `51d7a1783cd9fff7…` | `ca24373856eab9079055ed15878a14bf229657b19ae087e25ee9fca374684bd1` |
| `f9/identities.py` | `f8911aec56589d0f…` | `5c3a75ae180e2c84a8ec825cae64a078785c982af36772ae30f701250a2fad36` |
| `f9/spectral.py` | `218a93851c68a1f4…` | `b49d04345f3634435bcd670a227357ef7c014740d913b7337fdacf1e61203df3` |
| `f9/terrain.py` | `3d9143c1c2aed79a…` | `b8328f8acf51e7da67ae5674796c003914ecc6d07ed00c9dc3ad90607af381f9` |
| `tests/test_f9_m1.py` | `5666155776988248…` | `da937a8bb3edc36084ad046fae38df752ff226e77c09a85d4783b80eb02c4416` |

What changed where, so that the boundary can be checked:
- `config.py`: one new literal `F9_FLOOR_PROBABILITY`; the rule string; a comment on the `F9_ETA0` line (its expression `-math.log(1.0 - 0.01)` is kept verbatim, so your Appendix R substitution still applies); one new entry in `F9_DECLARATION`; one new check in `verify_frozen_identity`; one paragraph of the module docstring. **The declaration digest therefore changes:** `5784276492bdcc19…` → `7fbef2ff2a04e9bc0825e6bbfeb70ce867d15cc51ec22e7b4eac0a6c0ff8a3b3`.
- `family.py`: `import struct`; the two hashing lines of `family_summary`; the IDENTITY paragraph of the docstring.
- `spectral.py`: docstrings only. No executable line is changed.
- `terrain.py`: two guard lines at the top of `level_label`.
- `identities.py`: rewritten around `record_from_bases`. `RECORD_SCHEMA` is 2. `array_files()` now returns paths only. `verify_bundle_deep`'s tolerance argument is `float_rtol` (it was `spr_rtol`).
- `test_f9_m1.py`: 67 tests → 96. No round-1 test was removed; the old single tamper test is split into the loader test and the semantic tests.

## 3. What changed in the noncanonical evidence

Between the round-1 and round-2 container records (`F9_M1_IDENTITIES_CONTAINER_2026-11-16.json` → `…_ROUND2_2026-11-16.json`): all eight family identities, mask identities, comparison-array identities and level counts are equal; all eight base identities are equal; spr and g_spec are equal for all fifteen arms; **all eight component identities differ**, as R1 requires. The record's own identity changes (`46809209f690843e…` → `30edf99bb6af19e0d626a8449cc764d825c107766745ed6174b23f72c5d13bed`) because of the component identities, the schema number, the declaration digest, and the `arrays` field, which a bare record now fills with hashes.

## 4. Evidence in the packet

- `build_records/f9_m1_module_container_round2_2026-11-16.txt` — **96 passed in 352.65 s** in L1's container (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1).
- `build_records/F9_M1_IDENTITIES_CONTAINER_ROUND2_2026-11-16.json` — the container record. Noncanonical; binds nothing.
- `build_records/l2_m1_round1_checks.py` — your Appendix R program as extracted from your review (`7b879eb2ab2f5c03…`); say if it differs from what you wrote.
- `build_records/f9_m1_l2_round1_checks_on_round2_2026-11-16.txt` — that program's output on the round-2 source: R1 `summaries_equal false`, `component_hashes_equal false`; R3 `REJECTED`; R2 control `ACCEPTED`, the four cases `REJECTED`.

## 5. Disclosures

1. **The suite is slower.** A deep verification recomputes the whole record (about 8 s in the container), and the semantic tests each run one. The module now takes about six minutes in the container against one minute in round 1. L1 judged the coverage worth it and did not cache anything inside the verifier.
2. **Exact float equality on the writing machine.** With `float_rtol = 0` every float of the record must be reproduced bit for bit from the stored bases. Most are plain IEEE arithmetic on stored bytes. Three kinds go through numpy reductions whose summation order numpy does not promise across versions: the TB variance shares, the spectral iteration's norm and inner product, and `min`/`max` (order-independent). On one machine with one numpy this is deterministic, and L1's repeated builds agree. A later job run after a numpy upgrade on the canonical machine might need the tolerance. That is a question for the runner's binding, which M1-9 defers; L1 raises it now so that it is not a surprise.
3. **The verifier evaluates the terrain formulas once, for the §3.4 step 5 check.** The record itself is recomputed from stored bytes only. The formula check is what refuses a coherent record of a different terrain. On another libm it holds to 1e-12, not to the bit.
4. **L1 has not run anything on the canonical machine, and has still not seen the boundary endpoint.** M1 reads no probe output.
5. **`test_f8_m1.py` still fails 4 of 73 in L1's container for want of pyarrow**, on an untouched clone as well. Unchanged from round 1.

## 6. Questions

**Q1.** For each of R1, R2 and R3: CLOSED, CLOSED WITH NOTE, or NOT CLOSED (say what remains). Include the byte-order correction under R1 and the documentation items of your §9.
**Q2.** Declarations M1-2, M1-3 and M1-5 as repaired: ACCEPTABLE, REQUIRES CHANGE, or REJECT. M1-3 now reads: the record is a function of the stored bases; the loader checks form and bytes; the deep verifier checks semantics and the §3.4 step 5 agreement; external binding is the runner's.
**Q3.** Is there a record that should be refused and still verifies? Please attack `record_from_bases`, `_same` and the order of checks in `verify_bundle_deep`.
**Q4.** Disclosure 2: is exact float equality on the writing machine the right default, with the tolerance as an explicit argument?
**Q5.** Anything else to repair before placement.

## 7. Return format

One downloadable `.md` file, receipt table first. End with exactly one line, plain, at column 0:
`FINAL VERDICT: SOUND`
`FINAL VERDICT: DEFECT-WITH-REPAIR`

*L1, 2026-11-16. Nothing placed; no run on the canonical machine; nothing in `e1` or `f8` modified.*
