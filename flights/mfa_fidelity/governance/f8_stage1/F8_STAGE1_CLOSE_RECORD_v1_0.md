# Flight 8 stage 1 — close record v1.0

**Disposition selected by Mike, Theory Architect, 2026-11-12:** L2's rank 1 — retain the P1 determination and close the stage, qualified, after narrow reporting completion.
**Repository:** `github.com/MikeBradshaw3000/ee-theory-lab`, `main`; stage package committed at `abb927995d92faa37ca654ee8f3651c48a27f2e2`.
**Status of this document:** ratified by Mike, 2026-11-12 ("ratify", on L1 draft v0.2, whose text this is apart from this status line, the title, the closing line, and the two Gemini returns' identities in section 8, given here as the LF identities of record). Drafted by L1. It changes no canonical record, no frozen criterion and no placed module.

## 1. What is closed

Flight 8 stage 1, instrument `f8_stage1_v1`, under frozen Contract F8 v0.8.4 (`e87277a2d11e948f…`), Interpretations 001–004, governance `889a76646c4d8eb5…`, package specification `0738d35ee0a30aef…`, authorizations 001–003, canonical stage `6c0a5ec3df673924…`.

| Object | File SHA-256 | Record identity | Commit |
|---|---|---|---|
| `stage1_package.json` | `71ffee2bbc6db0f9…` | `905157cbda1f7561…` | `abb9279` |
| `p1_evaluation.json` | `51489c7e97730ae0…` | `42faa231c1aeee47…` | `5e7cf09` |

The stage package is complete with every item passing its declared predicates. Those predicates are package predicates: the P1 item's is that a canonical P1 record exists. The determination below rests on the four-test evaluation, not on the package flag, and the package flag does not discharge reporting items outside the package (sections 4 and 5).

## 2. The determination

**P1: PRODUCED**, cause none, under the frozen four-test rule (contract §4.11), on the canonical panel of 20 seeds, 24 pass-1 levels, a 50×50 lattice, a 3,000-tick horizon and a 1,000-tick tail.

| Test | Outcome | Basis |
|---|---|---|
| T-S1′ | PASS | both phases in the skeleton sweep; m̂_c = 1.521739 (grid index 13), at least 18 of 20 survivors there and at every higher level |
| T-S1c | PASS | on its registered domain m̂_c … m_max (ratified MP1-5): largest scored increase 0.0791634 against an allowance of 0.0921988 (f_J = 0.25 of the scored range 0.368795) |
| T-S2 | PASS | low-start and high-start crossings coincide (separation 0.0; Δm = 0.1201) |
| T-R1′ | PASS | realization positive and increasing at all 24 levels; largest increase 0.0303636 against an allowance of 0.1178655 |

The four test results were recomputed from the committed sweeps and census by L1 (Linux container) and by L2 (independently); both equal the committed results. The independent stability panel reproduces the skeleton crossing index and T-R1′; it does not replicate the low-start skeleton sweep, so it is not a second run of the whole four-test conjunction.

## 3. The limitation that travels with the determination

**T-S1c does not test the density increment entering the selected boundary; its pass does not establish continuity through the onset.**

On the canonical high-start skeleton sweep the seed-median density is 0 at m = 1.326087 (0/20 survivors), 0.004849 at 1.423913 (7/20), and 0.1469342 at m̂_c = 1.521739 (20/20). The increment into the boundary, 0.1420852, is outside the test's registered domain. Applied from one level earlier, the same arithmetic would return NOT DISTINGUISHED (allowance 0.1277201). That is a diagnostic of the frozen assay's reach, not a rescoring: the domain was fixed before any data, and widening it after the data would change the instrument. The diagnostic does not show a discontinuity either; a steep continuous rise at this grid spacing gives the same arithmetic.

**Claim language adopted (L2's, 2026-11-12).** Supported:

> Under Flight 8's frozen four-test rule, the homogeneous 50×50 lattice at a 3,000-tick horizon, 1,000-tick tail, declared twenty-seed canonical panel and twenty-four-level grid returned P1 PRODUCED: both declared skeleton initializations selected the finite-horizon persistence boundary m̂_c = 1.521739, the sampled skeleton branch from that boundary upward satisfied the registered continuity-compatibility criterion, and the positive-floor realization satisfied its registered positivity, monotonicity and continuity-compatibility criteria across the sweep.

Not supported: that Flight 8 resolved the skeleton's onset as continuous; that the lattice has a demonstrated critical point of any kind; that the theory is confirmed or refuted; that the M6 synthetic-ensemble error rates transfer to lattice runs; that the closure-fidelity shifts are a new finding (the pre-freeze probe had already exposed them, contract §1.0).

**Fidelity tier (reported, never scored).** m̂_c is 0.521739 above the closure's m = 1 and 0.380291 above the pair value. Skeleton median at the boundary 0.146934, against 0.313988 (closure) and 0.252376 (pair). Realization steepest ascent at m = 1.423913.

## 4. Reporting items

**4.1 Flicker run-length statistics (contract §1.3(b)): not recorded; accepted omission.** F8 Interpretation 004 (placed with this record) states the omission, bars any flicker claim from stage 1, and carries the observable to the successor flight as a design obligation. Stage 1 did not fulfil every reporting item of the contract.

**4.2 Job-0 comparison supplement (declaration v0.3 §8, M6-10): produced.** `build_records/F8_M6_JOB0_COMPARISON_SUPPLEMENT_2026-11-12.json`, file `048c07dc5945fd6b…`, record identity `999341f0c645c7ab…`, written on the canonical machine by `make_f8_job0_comparison.py` (`e856c2e420af8fa5…`) from the committed census (`91aebc07a80fab79…`) and M6's placed `surrogate_level_stats` at 200 replicates per level under the pricing master. Descriptive only. As measured: the lattice realization's tail density is below the E surrogate's at all 24 levels, by 0.0005 at m = 0.25 rising to 0.0521 at m = 1.423913; the surrogate's SD is between 0.64 and 1.50 times the lattice's. A container run of the same script gives the same lattice columns and surrogate values that differ in the fifth decimal; the cause of that cross-platform difference is not isolated (the two environments differ in operating system, Python and NumPy versions). The canonical machine's file is the record.

**4.3 M4 morphology (contract §1.3(a)): as pre-registered.** NOT_PRODUCED / no_null_consistent_phase on all 24 levels, no insertions; Interpretation 003's final-set obligation is discharged identically. This secondary label never bears on P1.

## 5. Provenance notes and errata (append-only; no historical bytes are altered)

**5.1 Authorization 003: when authority became effective.** Bound to `AUTHORIZATION_003.json`, SHA-256 `1413d3b74731e7ea96b1825b5ff1acf5ce9a0a5f01d718aa2d91d925acbee7bb`.

| Act | When |
|---|---|
| Draft probed on the canonical machine (nothing written) | 2026-11-09, afternoon |
| File and registry written on the canonical machine, before any ruling | 2026-11-09 16:43 |
| Mike's ruling, "as drafted", and his choice to commit the bytes on disk | 2026-11-10, morning |
| Commit `d7af16c` | 2026-11-10 09:34:14 −05:00 |
| First use: `skeleton_census` started | 2026-11-10 09:39:12 |

The record's `issued` field (2026-11-09) is the draft's date. The comment in `make_f8_authorization_003.py` that calls 2026-11-09 "Mike's ruling" is wrong; the ruling was 2026-11-10. Authority was effective from the commit. The full message of `d7af16c` states the same sequence.

**5.2 Commit-message errata.** `2dd54b5` names the manifest `PRODUCTION_PREREQUISITE_MANIFEST.json`; the file is `PRODUCTION_PREREQUISITES.json` (`e03084c3dbdd59b6…`). `ddd4f6d` places the cross-platform difference in the pricing construction bound at the twelfth significant digit; L1's re-run places it at the tenth (0.0009713653336 canonical, 0.0009713653334 container).

**5.3 L1's disposition packet.** Its per-level table gave means; the tests score seed medians. L2's medians, verified by L1, are the figures in section 3.

## 6. Evidence qualifications carried

- **Independent execution.** No one has re-run the lattice. L1 and L2 recomputed the scored tests from committed per-run summaries. Records are bound to the canonical stage and cannot be loaded through M7's reader elsewhere; exp-derived fields are recorded as the canonical machine saw them.
- **Single execution.** That each canonical job ran once is the session record's attestation; the committed files cannot prove the absence of earlier runs. No evidence of reruns or outcome selection was found.
- **Canonical suite.** 859 passed, 3 skipped, 0 failed. The third skip's identity is not in the record. Wall time 6:53:08, cause not established.
- **Working tree.** About 115 unrelated legacy paths were uncommitted or untracked on the canonical machine throughout. M7 protects the surfaces it reads; the tree as a whole was not clean.

## 7. Obligations carried forward

1. Flicker run-length observable: successor flight, per Interpretation 004.
2. Next-touch repairs (ratification record v1.0 §E.8): the direct-DIP docstring in `test_f8_m6.py`; the stale comment in `test_f8_mp1.py`.
3. A prospective test of continuity through the onset (declared domain, finer resolution near m̂_c) is a successor-flight design question. Nothing here authorizes it.

## 8. Reviews of this stage

- **L2 disposition consultation, 2026-11-12** (`L2_F8_STAGE1_DISPOSITION_CONSULTATION_2026-11-12_RECEIVED.md`, `9eb96103745dc6b3…`; receipt `c85691f33811e788…`), on L1's packet (`e162b1b5d2640f66…`): determination retained; no determination-invalidating defect in the chain; ranked dispositions; rulings on the packet's open items, adopted in sections 4–7.
- **Gemini, first return, 2026-11-12** (`739f07e0d0218b80…`): out of commission. It answered the questions in L1's packet, which was in the bundle as evidence, instead of auditing; its recommendation to reject P1 is outside its authority and rests on a median misread as 0 and on means in place of medians. Its observation that T-S1c does not score the entering increment agrees with L2's and is adopted in section 3. L1's bundle design invited the error; the second bundle omits the packet.
- **Gemini, second return, 2026-11-12** (`6f664a44fbdf7a07…`), on the second bundle (`76f835bc…`, 47 files, no L1 packet): one finding, that `calibration_tranche` ran under Authorization 002 without appearing in its `authorized_jobs`. The quotation is accurate and the finding is not a defect. The tranche is a governance job, not one of the 17 canonical jobs; M7 authorizes it through the record's dedicated field (`runner.py`: `GOVERNANCE_JOBS = ("production", "calibration_tranche")`; `run_tranche` refuses unless `tranche_authorized`). `AUTHORIZATION_002.json` (`111c5ee8…`) carries `tranche_authorized: true` with five levels and three seeds, and the committed tranche record (`c156c204…`) names authorization version 2 and the same levels and seeds. Verified by L1 from a fresh clone at `abb9279`. The return omits the commission's header counts, conforming-collisions section and coverage statement, so it is not evidence that the rest of the bundle is consistent. Triage: `GEMINI_F8_STAGE1_RESULT_TRIAGE_2026-11-12.md`.

*v1.0, 2026-11-12. Drafted by L1 from committed objects at `abb9279`, the canonical machine's outputs as pasted by Mike, and L2's consultation.*
