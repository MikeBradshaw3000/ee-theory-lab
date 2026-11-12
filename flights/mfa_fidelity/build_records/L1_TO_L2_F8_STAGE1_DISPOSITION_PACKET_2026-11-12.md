# L1 → L2 — Flight 8 stage 1: disposition consultation on the committed stage package

**From:** L1 (Claude, design chamber), at Mike Bradshaw's direction
**To:** L2 (ChatGPT, adversarial source review)
**Date:** 2026-11-12
**Repository:** `github.com/MikeBradshaw3000/ee-theory-lab`, `main` at `abb927995d92faa37ca654ee8f3651c48a27f2e2` (`abb9279`)
**Register:** disposition consultation after a completed canonical stage. Nothing in this packet is a ruling or an authorization. The stage's disposition is Mike's; he has asked for L2's ranked disposition first, as at E1-R's close.

---

## 0. Receipt first

Verify the archive SHA-256 against Mike's value, the file count against his message, and every payload file against `MANIFEST.txt`. Report the receipt table and stop until Mike says "execute". If your disposition takes the form of a clearance verdict, write the verdict line plainly, once, with no decoration.

## 1. What is asked

1. **Soundness of the chain.** Is the committed stage-1 record a sound execution of frozen Contract F8 v0.8.4 as interpreted (Interpretations 001–003) and governed (`F8_GOVERNANCE.json`, `PACKAGE_SPECIFICATION.json`, authorizations 001–003)? Name any defect in the order of acts, the bindings, or the evaluation that would make the P1 determination unsafe to rely on.
2. **Adversarial reading of the result.** Attack the determination. In particular examine T-S1c on the numbers in §3 (the skeleton goes from 0/20 survival at m = 1.326087, through a partial-survival level at 1.423913, to 20/20 at 1.521739), and say whether "consistent with a continuous onset at grid resolution" is the correct outcome of the frozen rule on these data, or whether the frozen rule required NOT DISTINGUISHED.
3. **A ranked disposition** for Mike: the options you consider available for closing stage 1, ranked, each with its conditions and what it would and would not license the program to say.
4. **The open items in §5.** For each, say whether it bears on the determination, on the disposition, or on neither, and what must be of record before close.
5. **Claim language.** State the strongest sentence about this result that the record supports, and the nearest sentence it does not.

L1 gives no recommendation on items 2, 3 and 5. The packet is written to be attacked.

## 2. The record

Every canonical job ran on the canonical machine (Windows 11, Python 3.14.4, NumPy 2.4.4) through M7's `run_canonical_job` or `run_tranche`, under a committed, registry-listed authorization, against the canonical stage `6c0a5ec3df673924…` (stage commit `e8e86d0`; governance `889a76646c4d8eb5…`; package specification `0738d35ee0a30aef…`; adapter body `df0834078c0343f0…`). Each record was committed as it landed; where M7 requires a committed predecessor (each census before its stability job, the manifest before production) it enforced that itself. File identities and commits below were measured by L1 from a fresh clone at `abb9279`.

| Record (under `governance/f8_stage1/`) | Result as committed | File SHA-256 | Commit |
|---|---|---|---|
| `AUTHORIZATION_001.json` | authorization v1: the §7.1 qualification jobs | `fd7ae15748982f06…` | `5b9e40f` |
| `prerequisites/package/mp1_known_answer.json` | `mp1_known_answer`: PASSED, 9 classes × 100, every class 100/100 exact, 0 cross-triggers | `12d983544f653dbc…` | `812a243` |
| `prerequisites/package/m6_design_audit.json` | `m6_design_audit`: `ensemble_pass` True, 12/12 classes, 6,000 sweeps, 0 halts; errors only `off_band_unresolved` 3/500; max CP upper 0.0154 (cap 0.10) | `96a1e497027b491a…` | `c2859b4` |
| `prerequisites/package/m6_held_out_audit.json` | `m6_held_out_audit`: `ensemble_pass` True, 12/12 classes, 0 halts; errors `off_band_mixture` 4/500, `off_band_unresolved` 2/500; max CP upper 0.0182 | `002d276c0033ab47…` | `ce44269` |
| `prerequisites/package/m6_audit_qualification.json` | `m6_audit_qualification`: QUALIFIED, reasons none | `29168ab78238e7b6…` | `3a08cde` |
| `AUTHORIZATION_002.json` | authorization v2: apparatus jobs + calibration tranche (5 levels × 3 seeds); production false | `111c5ee83d6c30a3…` | `18df7c4` |
| `prerequisites/package/m6_price.json` | `m6_price`: 0 S_min rejections in 10,000 NULL replicates (CP upper 0.00030; nominal α_P 0.001); S_term NO_SUSTAINED 9,991/10,000 | `0cad5161eb35f8fd…` | `ddd4f6d` |
| `prerequisites/package/calibration_census.json` | `calibration_census` (job 0): ceilings met, stop path not triggered; max MDD 0.0122 (skeleton_high, m = 1.423913) vs 0.02; ŝ_sk = 0 at the twelve levels m ≤ 1.326087 | `91aebc07a80fab79…` | `ae02bf5` |
| `prerequisites/package/tolerance_program.json` | `tolerance_program`: complete, 24 ensembles, ceilings met | `22d8e24c6a53d818…` | `fbc42b6` |
| `prerequisites/package/dense_reference.json` | `dense_reference`: reference of record, 701/701 S, NO-NULL-PHASE, 0 halts | `5d6d1ffb00497d93…` | `18319ed` |
| `prerequisites/package/reference_stability.json` | `reference_stability`: grids 351 and 1,401 agree; fixed points agree (1.73e-13 vs tol 1e-11) | `980ae201d4d01fc4…` | `57b84dd` |
| `prerequisites/package/projection_sweeps.json` | `projection_sweeps`: DESIGN-STABLE, 200/200 scored and matching, 0 halts (CP lower 0.985) | `d0459cc79b722b70…` | `39bd366` |
| `prerequisites/package/resource_benchmark.json` | `resource_benchmark`: fits with margin (projected 10,304 s, 99.5 MB) | `1356aeea7148b520…` | `b918f87` |
| `prerequisites/calibration_tranche.json` | calibration tranche: 15/15 runs, cleanup proven, PASSED | `c156c20439e321f1…` | `5d566ce` |
| `PRODUCTION_PREREQUISITES.json` | production prerequisite manifest: the governance record's seven prerequisites, each loaded through M7's reader before the write | `e03084c3dbdd59b6…` | `2dd54b5` |
| `AUTHORIZATION_003.json` | authorization v3: all 17 jobs, production true, bound to the manifest (see disclosure D1) | `1413d3b74731e7ea…` | `d7af16c` |
| `prerequisites/package/skeleton_assessment.json` | `skeleton_census`: T-S1′ PASS (m̂_c = 1.521739, index 13), T-S1c PASS, T-S2 PASS (m̂_low = m̂_c) | `c86c41d767c64e44…` | `00b2b3d` |
| `prerequisites/package/skeleton_stability.json` | `skeleton_stability`: stability panel m̂_c = 1.521739, same index; reproduced True | `33882615a5fe57fe…` | `52ab62a` |
| `prerequisites/package/realization_morphology.json` | `realization_census`: morphology all 24 levels S; M4 verdict NOT_PRODUCED / no_null_consistent_phase (the §1.3(a) pre-registered expectation; `matches_expectation` True); router row P2R-1, no insertions; `final_set_obligation` discharged_identically | `ea8a64ec5b4e2f0b…` | `56d3b87` |
| `prerequisites/package/realization_stability.json` | `realization_stability`: T-R1′ PASS on canonical and stability sweeps; no crossing on either; reproduced True | `37068b2e99d4fbae…` | `974bf8b` |
| `prerequisites/package/p1_evaluation.json` | `p1_evaluation`: determination **PRODUCED**, cause none; four tests PASS | `51489c7e97730ae0…` | `5e7cf09` |
| `prerequisites/package/stage1_package.json` | `stage1_package`: complete True, all_items_pass True, 29 items | `71ffee2bbc6db0f9…` | `abb9279` |

The level directories under `prerequisites/package/` hold the run artifacts: 168 level directories (calibration 48, canonical 72, stability 48), 20 runs each, 3,360 production-shape runs, 6,720 run files and 168 level records. They are committed but **not in this zip** (size); the five sweep records in the zip carry every run's tail density, survival flag, spec hash and ρ-table hash.

As far as the session record shows, each canonical job ran exactly once; no job's output was produced twice, and no record was replaced after it existed.

## 3. The determination and the data under it

`p1_evaluation.json` (record result `42faa231c1aeee47…`): determination **PRODUCED**, cause none.

| Test | Outcome | Detail as recorded |
|---|---|---|
| T-S1′ | PASS | m̂_c = 1.521739, grid index 13 |
| T-S1c | PASS | "consistency with a continuous onset at resolution s (s1.1')" |
| T-S2 | PASS | m̂_low = 1.521739 = m̂_c; separation 0.0; Δm = 0.120126265992375 |
| T-R1′ | PASS | no detail |

Claim strength as the record states it: "finite-horizon persistence at the declared N, T, panel and resolution (s1.1'); never a thermodynamic critical point".

**Per-level data.** Each cell is survivors out of 20 and the plain mean of the 20 runs' tail densities ρ̂. The means are L1's arithmetic from the committed sweep records, given for orientation; the records' own estimators govern.

| m | skeleton_high (canonical) | skeleton_low (canonical) | realization (canonical) | skeleton_high (stability panel) | realization (stability panel) |
|---|---|---|---|---|---|
| 0.250000 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.0666 | 0/20, 0.0000 | 20/20, 0.0662 |
| 0.347826 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.0735 | 0/20, 0.0000 | 20/20, 0.0736 |
| 0.445652 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.0820 | 0/20, 0.0000 | 20/20, 0.0823 |
| 0.543478 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.0918 | 0/20, 0.0000 | 20/20, 0.0918 |
| 0.641304 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.1041 | 0/20, 0.0000 | 20/20, 0.1043 |
| 0.739130 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.1179 | 0/20, 0.0000 | 20/20, 0.1182 |
| 0.836957 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.1340 | 0/20, 0.0000 | 20/20, 0.1345 |
| 0.934783 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.1536 | 0/20, 0.0000 | 20/20, 0.1532 |
| 1.032609 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.1750 | 0/20, 0.0000 | 20/20, 0.1749 |
| 1.130435 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.2004 | 0/20, 0.0000 | 20/20, 0.2007 |
| 1.228261 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.2281 | 0/20, 0.0000 | 20/20, 0.2291 |
| 1.326087 | 0/20, 0.0000 | 0/20, 0.0000 | 20/20, 0.2570 | 0/20, 0.0000 | 20/20, 0.2571 |
| 1.423913 | 7/20, 0.0098 | 4/20, 0.0083 | 20/20, 0.2873 | 4/20, 0.0075 | 20/20, 0.2872 |
| 1.521739 | 20/20, 0.1487 | 20/20, 0.1456 | 20/20, 0.3162 | 20/20, 0.1475 | 20/20, 0.3168 |
| 1.619565 | 20/20, 0.2262 | 20/20, 0.2256 | 20/20, 0.3464 | 20/20, 0.2251 | 20/20, 0.3461 |
| 1.717391 | 20/20, 0.2825 | 20/20, 0.2828 | 20/20, 0.3736 | 20/20, 0.2842 | 20/20, 0.3733 |
| 1.815217 | 20/20, 0.3297 | 20/20, 0.3290 | 20/20, 0.3996 | 20/20, 0.3289 | 20/20, 0.4001 |
| 1.913043 | 20/20, 0.3678 | 20/20, 0.3680 | 20/20, 0.4238 | 20/20, 0.3671 | 20/20, 0.4238 |
| 2.010870 | 20/20, 0.3996 | 20/20, 0.4004 | 20/20, 0.4471 | 20/20, 0.4005 | 20/20, 0.4478 |
| 2.108696 | 20/20, 0.4294 | 20/20, 0.4295 | 20/20, 0.4680 | 20/20, 0.4291 | 20/20, 0.4683 |
| 2.206522 | 20/20, 0.4538 | 20/20, 0.4549 | 20/20, 0.4874 | 20/20, 0.4543 | 20/20, 0.4876 |
| 2.304348 | 20/20, 0.4769 | 20/20, 0.4774 | 20/20, 0.5055 | 20/20, 0.4768 | 20/20, 0.5058 |
| 2.402174 | 20/20, 0.4978 | 20/20, 0.4973 | 20/20, 0.5223 | 20/20, 0.4973 | 20/20, 0.5221 |
| 2.500000 | 20/20, 0.5159 | 20/20, 0.5161 | 20/20, 0.5379 | 20/20, 0.5154 | 20/20, 0.5368 |

No level in any of the five sweeps is unevaluable or carries a halt key.

**Fidelity tier (reported, never scored).** Shift of m̂_c against the closure's m = 1: 0.521739. Against the pair value m_lat: 0.380291. Skeleton density at the crossing, as the record reports it: 0.146934, against 0.313988 (closure) and 0.252376 (pair). Realization steepest ascent m̂_infl = 1.423913 (not at a sweep edge), 0.097826 below m̂_c and 0.247413 above the closure's m_infl. The full tables are in `p1_evaluation.json`.

**Calibration census at the transition (job 0, its own seed panel).** ŝ_sk = 0.014543 and MDD_sk = 0.012227 at m = 1.423913 (the largest MDD in the census; ceiling 0.02); ŝ_sk = 0.010093 at 1.521739; max MDD_re = 0.001860.

## 4. What L1 replayed off the canonical machine, and what it could not

On a Linux container, from a fresh clone at `abb9279`:

- **Replayed, equal.** L1 decoded the three committed canonical sweeps and the committed census and re-ran M-P1's four test functions. All four `TestResult` objects equal the committed ones, and the determination is PRODUCED. `evaluate_p1` as a whole returns the same determination, m̂_c, shifts and m̂_infl.
- **Replayed, different in exp-derived fields only.** The container's `evaluate_p1` differs from the committed record in the two closure-comparison tables (`skeleton_vs_rho_sk`, `realization_vs_rho_re`), hence in the closure publication identity (`7293211a…` on the container, `be823912…` committed) and the record's result identity. This is the cross-platform `exp` effect disclosed at M5's placement. `run_pricing` on the container equals the committed `m6_price.json` in every field except `construction_bound`, which differs at the tenth significant digit.
- **Not replayable off-platform.** The committed adapter record does not replay on the container (`validate_adapter` refuses it), and every record is bound to the canonical stage identity, so M7's reader refuses all of them under a non-canonical stage. L1's checks of the remaining records are blob identities and decoded field values, not replays. The lattice runs themselves were not re-run anywhere.
- **Package check.** All 29 items in `stage1_package.json` are marked complete and passing, and all 29 item files are committed at the identities the package records.

L2 has the same boundary: you can decode and recompute from the committed sweeps, and you cannot load records through M7's reader.

## 5. Open items and disclosures

**D1. AUTHORIZATION_003 was written before the ruling.** The file was written on the canonical machine on 2026-11-09 16:43, after the probe and before Mike's word. Mike ratified it "as drafted" on 2026-11-10 and chose to commit the bytes on disk; the commit (`d7af16c`) was made after the ruling and its message discloses the timing. The record's issue date is 2026-11-09. No job ran under it before the commit.

**D2. Contract §1.3(b) is not discharged.** The contract lists "flicker run-length statistics near the measured boundary m̂_c across windows W" as "recorded, not tested". No placed F8 module records them: M1 persists per-tick global density and run summaries, never per-cell states. Mike ruled on 2026-11-08 to note the omission in an interpretation record (F8 Interpretation 004, drafted, **not placed**) and carry the observable to the successor flight. Neither the ruling nor the draft is of record in the repository at `abb9279`.

**D3. The job-0 comparison supplement does not exist.** Generator declaration v0.3 §8 (M6-10; Interpretation 002 pt 9b) freezes a descriptive supplement comparing the lattice realization's census with the E surrogate at n_cmp = 200, "attached to the M6 governance entry when available", "not a prerequisite for the M6 audits". The census has existed since `ae02bf5`; the supplement has not been produced. It is not a package item.

**D4. Two commit-message errors (messages, not records).** `2dd54b5` names the manifest `PRODUCTION_PREREQUISITE_MANIFEST.json`; the file is `PRODUCTION_PREREQUISITES.json` (identity as stated). `ddd4f6d` says the container's construction bound differs "at the 12th significant digit"; it is the tenth.

**D5. Next-touch obligations still outstanding.** Ratification record v1.0 §E item 8 (two test docstring/comment repairs in `test_f8_m6.py` and `test_f8_mp1.py`). Items 3 and 4 were discharged at M7's placement.

**D6. Canonical suite.** 859 passed, 3 skipped. The third skip is not identified in the `-q` output; the symlink test is the expected candidate. Wall time 6:53, cause not established.

**D7. Working tree.** The canonical machine's working tree carried roughly 115 unrelated, pre-existing uncommitted or untracked paths throughout (legacy `cycle3/` and E1 artifact leftovers). M7's committed-state checks cover the governance and prerequisite trees it reads.

**D8. The M4 verdict.** `realization_morphology.json` and `dense_reference.json` both carry NOT_PRODUCED / no_null_consistent_phase. This is the §1.3(a) pre-registered expectation and never bears on P1 (§4.7); it is stated here so the two uses of "NOT PRODUCED" in the record are not confused.

## 6. Files in this zip

The packet; the frozen contract, freeze record and Appendix A; Interpretations 001–003; both ratification records; every file under `governance/f8_stage1/` except level directories, the 168 level records and the benchmark artifacts; the M7 placement note and the generator declaration v0.3; the whole `mfa_instrument` package and the F8 tests as placed; `GIT_LOG_d4994a5_to_abb9279.txt` (generated by L1 with `git log`; not a committed file).
