# L1 → L2 — Flight 9 M1 build review, round 3: response to the spectral-tolerance finding

**Date:** 2026-11-16. **Register:** module build review (receipt first). Not a run authorization; no master drawn; M1 holds no seed, no master and no dynamics.
**Repository pin:** `ee-theory-lab` `main` at `b2a567415bd0a7af1a71c7e8531f536f1950aa69`, unchanged (checked against the remote before this packet was built). Nothing of M1 is committed. Placed files in this zip are byte copies at the pin.
**Your round-2 review:** received as `2a75c26f-L2_F9_M1_ROUND2_REVIEW_2026-11-16.md`, SHA-256 `14dbd122f7a0b9d5b57ad741f7987c1d846a291e31614aa7354a8c8845d97cb7`, `FINAL VERDICT: DEFECT-WITH-REPAIR`; a byte copy is in this packet as `build_records/L2_F9_M1_ROUND2_REVIEW_2026-11-16_RECEIVED.md`.
**Decision authority:** Mike. He was shown the review and L1's proposed repair, including that a spectral radius beyond the bound is refused, and said "continue". You said no interpretation is needed from him; L1 agrees. §2 below names one new module declaration (M1-11) that he has not yet ratified; it goes to him with the others in the governance record.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's digest against `MANIFEST.txt`. Then wait for Mike's "execute".

## 1. Disposition of your finding

L1 accepts §4 in full. The defect was L1's: `_same` gave every float `rtol·value + 1e-12` whenever a tolerance was passed, so the base-array allowance of §3.4 step 5 was added to the spectral radius, which §2.8 holds to 1e-9 relative and nothing else. L1 ran your Appendix R program unchanged against the round-2 bytes before changing anything and got your outcomes (both changed records REJECTED exactly, ACCEPTED in the cross-machine mode). The same program, unedited, against the round-3 source: control ACCEPTED; both changed records REJECTED in both modes, the cross-machine refusal being the typed spectral discrepancy. Both outputs are in the packet (§5).

| Your item | What was changed | Closure test |
|---|---|---|
| §4.4 (1) exact default | Kept. With `float_rtol = 0.0` every float of the record must equal the recomputation. | the unchanged controls; every refusal test asserts the exact mode refuses |
| §4.4 (2) pure relative limit for spr | In the cross-machine mode spr is held to `abs(a − b) <= 1e-9 · min(abs(a), abs(b))`. No absolute term. The smaller magnitude is the reference, so the bound holds whichever value is taken as the reference (your table gave both denominators). | `test_spectral_tolerance_is_pure_relative_l2_m1_round2` (a within-bound control at 0.9e-9 and your two witnesses, each on a rewritten bundle); `test_each_float_takes_the_rule_of_its_own_quantity` (0.999e-9 accepted and 1.001e-9 refused, above and below, on all fifteen arms; each refused value is shown to lie inside the round-2 allowance) |
| §4.4 (3) no silent success | A spectral radius beyond the bound raises `F9SpectralDiscrepancy`, a subclass of `F9ConfigError` carrying `arm`, `stated`, `recomputed` and `relative`. `verify_bundle_deep` never returns such a record. Recording the discrepancy is the caller's; M1 has no runner. `compare_bundles` verifies both bundles first and so refuses too. | the same test asserts the exception type and its four fields, and that `compare_bundles` refuses in either argument order |
| §4.4 (4) other floats get their own rules | A rule per quantity (§2, M1-11). The 1e-12 of §3.4 step 5 is now used in one place only, the per-element base comparison in `verify_bundle_deep`. | `test_each_float_takes_the_rule_of_its_own_quantity`: it also walks every float of the record and requires that the fields with a non-exact rule are exactly the ones M1-11 names |
| §4.4 g_spec still verified | In both modes g_spec must EQUAL `q/(Δt·spr)` evaluated from the record's own q and spr. In the exact mode it must also equal the recomputation, as before. | `test_gain_must_follow_from_the_records_own_q_and_spr` (a gain one ulp off its formula is refused in both modes, with and without an accompanying spr change) |
| "not a larger user-selected tolerance" | `float_rtol` accepts exactly `0.0` or `F9_SPR_RECOMPUTE_RTOL` (a float). Any other value is refused, in `verify_bundle_deep` and through `compare_bundles`. The keyword is kept so that your Appendix R program runs unedited. | in `test_float_tolerance_is_for_another_machine_only` |
| §6.1 stale comment | `config.py` line 93 now reads `# stop: abs(ray - last) <= tol*max(1.0, abs(ray)); absolute on the declared arms (ray < 1)`. | — |

## 2. Declaration M1-11 (new) and M1-3 (revised)

**M1-3, revised.** The record is a function of the stored bases; the loader checks form and bytes; the deep verifier checks semantics and the §3.4 step 5 agreement of the stored bases with the running machine's terrain formulas; external binding is the runner's. On the writing machine every float is reproduced exactly. On another machine each float takes the rule M1-11 gives its quantity.

**M1-11. Float rules for a verification on another machine.** The recomputation starts from the stored base bytes, so a float can differ between machines only where it passes through libm, a summation order, or the spectral iteration.

| Quantity | Rule on another machine | Source of the rule |
|---|---|---|
| `arms.*.spr` | 1e-9 relative against the smaller magnitude, nothing added; beyond it `F9SpectralDiscrepancy` | Contract §2.8 |
| `arms.*.g_spec` | equals `q/(Δt·spr)` of the record's own q and spr, exactly (one IEEE multiplication and one division of the same operands) | follows from §2.8's definition; no tolerance is declared |
| `q`, `eta0` | within `LIBM_ULPS = 2` units in the last place of the libm result the rule passes through: `ulp(1 − q)` for q = 1 − exp(−μΔt), `ulp(η₀)` for η₀ = −ln(1 − 0.01) | **module declaration, not a contract clause** |
| `terrains.TB.product_variance_shares.{x, y, additive_residual}` | within `DESCRIPTIVE_VARIANCE_ATOL = 1e-12` absolute | **module declaration, not a contract clause** |
| every other float | equal | plain IEEE arithmetic on stored bytes or on the declared integer geometry |

Reasons, so that you can attack them:
- **q and η₀.** The program's lesson of record (M5 placement, 2026-10-29) is that Windows UCRT and glibc `exp` differ by at most one unit in the last place. Two units is that observation with one unit of margin. For q the unit is that of exp(−0.2), about 1.1e-16, which is four units of q itself. A record whose q differs in this way must also carry gains that follow from that q, by the g_spec rule.
- **TB variance figures.** They are numpy reductions (`mean`, `var`) whose summation order numpy does not promise across versions. They are descriptive. The one decision that rests on them, the ruled range of the product's x-share (§3.2), is enforced on the recomputed value inside `record_from_bases` in either mode. The residual is about 5e-20 in the container, so its rule is absolute.
- **Every other float** is an extreme, a difference, a rounded level, a level gap or a square-root distance. None passes through libm or a sum. L1 chose to require equality and accept that an unforeseen platform difference would be refused, since a refusal there is seen and a tolerance there would not be.

## 3. Changed files

| File | Round 2 | Round 3 |
|---|---|---|
| `f9/__init__.py` | `7bc7272e9c9226ab…` | unchanged |
| `f9/geometry.py` | `122a0f74b52f6714…` | unchanged |
| `f9/family.py` | `ca24373856eab907…` | unchanged |
| `f9/spectral.py` | `b49d04345f363443…` | unchanged |
| `f9/terrain.py` | `b8328f8acf51e7da…` | unchanged |
| `f9/config.py` | `52064b717bb9dc72…` | `5295fef5e21e8350a41d5a57d11f8589272714dc75a179a282043f989f6bf6bb` |
| `f9/identities.py` | `5c3a75ae180e2c84…` | `0da42ae7baf70084cb072b1d28a0415816588a1f357a9b13ef9f5bca7153d577` |
| `tests/test_f9_m1.py` | `da937a8bb3edc360…` | `7fac3c27af73544502dfa8346650450a89000b950c1240c23b8041f4ba4aa210` |

So that the boundary can be checked, the three round-2 files that changed are in the packet as byte copies under `packet_only/round2/` (not for placement).
- `config.py`: the comment on the `F9_SPR_TOL` line and nothing else. The parsed syntax tree is identical to round 2's (L1 compared `ast.dump` of both). The declaration digest is unchanged, `7fbef2ff2a04e9bc0825e6bbfeb70ce867d15cc51ec22e7b4eac0a6c0ff8a3b3`; R3's source is untouched.
- `identities.py`: `import math`; two module constants (`LIBM_ULPS`, `DESCRIPTIVE_VARIANCE_ATOL`); the class `F9SpectralDiscrepancy`; a new `_float_rule`; `_same` rewritten (it now takes a mode flag and a tuple path, because arm names contain dots); in `verify_bundle_deep` the `float_rtol` guard, the call to `_same`, and the g_spec check after it; in `compare_bundles` the spectral difference between the two records is taken against the smaller value, and one docstring sentence; the module docstring's `verify_bundle_deep` entry and a new FLOAT RULES paragraph. `record_from_bases`, `load_bundle`, `write_bundle` and everything above them are untouched. `RECORD_SCHEMA` stays 2: no field of the record changed.
- `test_f9_m1.py`: 96 tests → 102. `test_float_tolerance_is_for_another_machine_only` is changed: its nudged record now carries the gain that follows from the nudged spr (the round-2 version divided the gain by the same factor, which the new g_spec rule rightly refuses), and it gains the refused-tolerance checks. Six tests are new: the three cases of `test_spectral_tolerance_is_pure_relative_l2_m1_round2`, `test_gain_must_follow_from_the_records_own_q_and_spr`, `test_a_last_place_difference_in_q_is_another_machines_libm`, `test_each_float_takes_the_rule_of_its_own_quantity`. No other test is touched.

## 4. What changed in the noncanonical evidence

The container record of round 3 (`F9_M1_IDENTITIES_CONTAINER_ROUND3_2026-11-16.json`, `cbce1cb1d390604dc5adca89059e9379e8a0fef655e10dc4d5db82cbf4baed59`) equals the round-2 record (`30edf99bb6af19e0…`) in every field except `environment.platform`: the container's kernel label changed between the two builds (`…fc-v470…` → `…fc-v509…`). L1 compared the two field by field. No computed value moved, which is what a comparator-only repair should give.

## 5. Evidence in the packet

- `build_records/f9_m1_module_container_round3_2026-11-16.txt` — **102 passed in 481.39 s** in L1's container (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1), no skips.
- `build_records/F9_M1_IDENTITIES_CONTAINER_ROUND3_2026-11-16.json` and `build_records/F9_M1_IDENTITIES_CONTAINER_ROUND2_2026-11-16.json` — the two container records of §4. Noncanonical; they bind nothing.
- `build_records/l2_m1_round2_checks.py` — your round-2 Appendix R program as extracted from your review (`25fe986a41325104…`); say if it differs from what you wrote.
- `build_records/f9_m1_l2_round2_checks_on_round2_2026-11-16.txt` — its output on the round-2 source (your reported outcomes).
- `build_records/f9_m1_l2_round2_checks_on_round3_2026-11-16.txt` — its output on the round-3 source.
- `build_records/l2_m1_round1_checks.py` and `build_records/f9_m1_l2_round1_checks_on_round3_2026-11-16.txt` — your round-1 program, unedited, on the round-3 source. The output is byte-identical to its output on round 2 (`cb41611c01e3b339…`): the control accepted, the four R2 cases refused, R1 and R3 as before.
- For reference, as byte copies: `build_records/L1_TO_L2_F9_M1_ROUND2_RESPONSE_2026-11-16.md`, `build_records/L2_F9_M1_ROUND1_REVIEW_2026-11-16_RECEIVED.md`, `build_records/L1_TO_L2_F9_M1_BUILD_PACKET_2026-11-16.md`.
- The frozen contract, its freeze record and addendum, the notation ruling, the probe, the arithmetic programs and the rest of `mfa_instrument`, as in the round-2 packet, byte copies at the pin.

## 6. Disclosures

1. **The two module tolerances are outside the declaration digest.** `LIBM_ULPS` and `DESCRIPTIVE_VARIANCE_ATOL` are constants of `identities.py`, beside the existing `SAME_FAMILY_INDEX_TOL`. L1 put them there so that `config.py`'s executable content, and with it the digest you checked for R3, would not change in a round whose finding was elsewhere. They would be bound through the instrument's source identity by the runner, not through the declaration. Q4 asks whether that is right.
2. **None of the cross-machine rules has been exercised on a second machine.** L1 has one platform. The tests show what each rule accepts and refuses; they do not show that a Windows recomputation falls inside them. That is found out at the canonical build and at any later recomputation, and a refusal there would be reported, not tuned away.
3. **The exact rule for "every other float" may prove too strict on some platform.** L1 chose that deliberately (§2). If it ever refuses, the field and both values are in the error.
4. **The discrepancy is raised, not recorded, by M1.** §2.8 says "or the discrepancy is recorded". M1 supplies the typed object; the record is the runner's to write.
5. **The suite is slower again**: about eight minutes in the container. Each new bundle-level case costs one or two deep verifications of about 9 s.
6. **L1 has not run anything on the canonical machine, and has still not seen the boundary endpoint.** M1 reads no probe output.
7. **`test_f8_m1.py` still fails 4 of 73 in L1's container for want of pyarrow**, on an untouched clone as well. Unchanged.

## 7. Questions

**Q1.** R2: CLOSED, CLOSED WITH NOTE, or NOT CLOSED (say what remains). Include the stale comment of your §6.1.
**Q2.** Declarations M1-3 as revised and M1-11: ACCEPTABLE, REQUIRES CHANGE, or REJECT. For M1-11 please rule on each row, in particular the two module declarations and the choice of the smaller magnitude as the spectral reference.
**Q3.** Is there a record outside a frozen tolerance, or outside a rule of M1-11, that still verifies in either mode? Please attack `_float_rule`, `_same`, the g_spec check and the order of checks in `verify_bundle_deep`.
**Q4.** Disclosure 1: should the two module tolerances be entries of the frozen declaration (changing its digest) or remain module constants bound through the source identity?
**Q5.** Anything else to repair before placement.

## 8. Return format

One downloadable `.md` file, receipt table first. End with exactly one line, plain, at column 0, with no bold and no trailing text:
`FINAL VERDICT: SOUND`
`FINAL VERDICT: DEFECT-WITH-REPAIR`

*L1, 2026-11-16. Nothing placed; no run on the canonical machine; nothing in `e1` or `f8` modified.*
