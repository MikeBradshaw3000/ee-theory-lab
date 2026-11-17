# L1 → L2 — Flight 9 M1 build packet (round 1): declarations, terrains, comparison arrays, contour families, spectral values, the identity build

**Date:** 2026-11-16. **Register:** module build review (receipt first), the register of the Flight 8 module reviews. Not a run authorization. No master has been drawn; M1 holds no seed, no master and no dynamics.
**Repository pin:** `ee-theory-lab` `main` at `b2a567415bd0a7af1a71c7e8531f536f1950aa69`. Every placed file in this zip is a byte copy from a fresh clone at that commit. The NEW objects (listed in §1) are not in the repository.
**Decision authority:** Mike. L2 reviews; L1 repairs; placement follows L2's SOUND.
**The governing text is frozen.** Contract F9 v0.7 (`60cf50fc8936abef…`) was frozen on 2026-11-15 by the freeze record (`66fa3d31263b61dc…`) at commit `595ddc8`, after your round-6 clearance. Notation table v1.2 (the contract's §10 rows) was appended afterwards at `b2a5674`; the addendum in this packet records that. This review is of the module against the frozen contract. A contract ambiguity you find is a ruling for Mike, recorded as an interpretation beside the frozen text; it is not to be resolved inside the module.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count (payload files plus `MANIFEST.txt`, as the manifest lists them), and every file's digest against `MANIFEST.txt`. Then wait for Mike's "execute".

## 1. What is in the packet

**NEW, for review** (under `flights/mfa_fidelity/`):

| File | What it is |
|---|---|
| `instrument/mfa_instrument/f9/__init__.py` | package statement |
| `instrument/mfa_instrument/f9/config.py` | the frozen declarations as literals, each cited to its contract section or freeze-record item; the declaration digest; `verify_frozen_identity` |
| `instrument/mfa_instrument/f9/terrain.py` | bases of T0, TA, TB, TC and the four TD variants; the TD core and its §3.2 checks; compositions; comparison arrays; level labels; serialization and base identity |
| `instrument/mfa_instrument/f9/geometry.py` | edge bonds and traced components (§5.5 step 3); the informative-level predicate (§5.5 step 4) |
| `instrument/mfa_instrument/f9/family.py` | the registered family (§5.5 step 5); family, mask and component identities |
| `instrument/mfa_instrument/f9/spectral.py` | spr, g_spec, gain at a level, local m (§2.8) |
| `instrument/mfa_instrument/f9/identities.py` | the build of §3.4 step 4: the record, the bundle writer and loader, the deep verification, the cross-platform comparison of §3.4 step 5 |
| `instrument/tests/test_f9_m1.py` | 67 tests |
| `build_records/f9_m1_module_container_2026-11-16.txt` | the container run: 67 passed in 67.7 s |
| `build_records/F9_M1_IDENTITIES_CONTAINER_2026-11-16.json` | the identity record built in L1's container. **Noncanonical. It binds nothing.** |

**PLACED, for context** (byte copies at the pin): the frozen contract, the freeze record, its addendum and the directory README; notation table v1.2; your round-6 review; the whole `mfa_instrument` package (root, `e1`, `f8`, `gates`; nothing modified); the committed probe script `design/flight9/probe/f9_probe.py` (the source of the spectral routine); and the contract-stage prototypes `contracts/flight9/arith_v0_4/f9_evaluator_proto_v4.py`, `f9_compare.py` and your own `l2_appendix_r.py`.

## 2. How to run

From `flights/mfa_fidelity/instrument/`: `python -m pytest tests/test_f9_m1.py -q`. numpy only. One test (`test_routine_agrees_with_lanczos_on_every_arm`) uses scipy and is skipped without it. No pyarrow is needed. About one minute. `-s` shows the family-size report of §4 item 3.

## 3. What Mike directed

On 2026-11-16 Mike directed the build to follow Flight 8's order: the `f9` package is built module by module beside `f8`, each module reviewed by you before placement; then the governance record; then Authorization 001 naming `build_identities` alone. So the identity code is reviewed and placed now, and the job of record (§8 step 1) runs later, on the canonical machine, under that authorization. Nothing in this packet is that job. Mike also said the canonical machine and environment are unchanged from Flight 8, and approved M1's scope: declarations; terrains with serialization and base identities; compositions and comparison arrays; the registered families with traced components and the same-masks check; spectral values; tests including your counterexamples.

## 4. Disclosures

1. **Agreement with the contract's provisional values, in the container.** All eight base-array hashes equal Appendix A.1's. The eight registered family sizes and the counts before rounding equal §3.4 step 3's (1,300 / 2,221; 1,180 / 1,389; 681 / 861; 920; 250; 250; 2,600 / 3,840; 50 / 59). spr and g_spec agree with A.1 to its six decimals for all fifteen arms. TB's shares are 0.51727 and 0.48273; H's fall along P on TB is 0.08756. The TD table of §3.2 (perimeters 200 and 416, band cells 676 / 1,376 / 1,424 / 2,816, steps 0.145 / 0.074 / 0.142 / 0.074, four discs of 104 bonds) is reproduced by test.
2. **The spectral routine does not certify its own accuracy; L1 measured it.** §2.8 names "the committed routine". The only routine committed at the freeze is the probe's: power iteration on D^(1/2)·(A/8)·D^(1/2) from the uniform vector, stopping when the Rayleigh quotient changes by at most 1e-14 relative. M1 carries it unchanged (`F9_SPR_TOL`, `F9_SPR_MAX_ITER` are the probe's values; the contract does not state them). A stopping rule on the change of the quotient does not bound its error. Collatz–Wielandt bounds from the final iterate are loose (relative width 3e-7 to 6e-5 across the arms), because the vector is not converged to the same accuracy as the quotient. Against an implicitly restarted Lanczos eigenvalue (scipy `eigsh`, tol 1e-14) the routine's value is low by at most **3.0e-12 relative** over the fifteen arms (worst: TC under P), always on the low side. That is inside the contract's 1e-9. L1 kept the routine and added the comparison as a test. If you hold that "the committed routine" should be one with a certified error, that is an interpretation for Mike, and L1 has not pre-empted it.
3. **The registered families may differ on the canonical machine, and the tests do not assert the container's sizes.** cos and tanh go through libm. The smallest gap between adjacent registered levels is one rounding unit (1e-12) on TC and on TD-1-2, and 2e-12 on TD-1-4: in the saturated tails, values that differ at the thirteenth decimal are being separated or merged by the rounding. A one-ulp difference on another libm can move such a value across a rounding boundary and add or remove a level. The contract provides for this (container values provisional; the canonical masks are the objects of record; 1e-12 agreement "does not guarantee identical masks"). So `test_container_values_are_reported` prints the sizes found on the machine running the suite beside the contract's and asserts nothing about them. Exact assertions are made only where no libm is involved (T0, the TD cores, declared literals). L1 has not run anything on the canonical machine.
4. **The record's raw-index relation.** On same-family terrains the raw index never falls along the shared array (largest fall 0 with ties in ω ordered by the index). Inside one level class of ω the raw index spreads by up to 9.8e-13 (a class is 1e-12 wide in the latent, and P = t³). Both numbers are in the record; the 1e-12 bound of §3.4 step 3 is enforced on the fall.
5. **η₀ enters the declaration digest as its rule, not its float.** `-ln(1 - 0.01)` passes through `math.log`, which may differ by an ulp across platforms; a digest over the float could then differ between machines for no change of declaration. The float is used for arithmetic and reported in the record.
6. **The four pre-existing failures of `test_f8_m1.py` in L1's container are not M1's.** That module fails 4 of 73 in the container on an untouched clone at the pin as well (`ModuleNotFoundError: pyarrow`, imported by `e1/config.py`). `test_f9_m1.py` does not need pyarrow.
7. **L1 has still not seen the boundary endpoint.** M1 reads no probe output and no occupancy array. Please do not ask for any such computation.
8. **Contract-stage prototypes are not the instrument.** `geometry.edge` uses the same union-find idea as the prototype's `edge`; it was rewritten with a declared canonical order, and the test file checks it against a second, different algorithm (a loop-walking tracer) on 60 random masks.

## 5. Declarations of this module (for your review; Mike ratifies them with the governance record)

| # | Declaration | Where |
|---|---|---|
| M1-1 | **Canonical bond order and component numbering.** Axis-0 bonds first in row-major order of the lower cell, midpoint (i + 0.5, j); then axis-1 bonds, midpoint (i, j + 0.5); coordinates in [0, L). Components numbered by first appearance in that order. | `geometry.py` docstring; `test_canonical_bond_order_and_midpoints` |
| M1-2 | **Family identities.** Family: per level ascending, the level as little-endian float64 then the mask packed row-major (`numpy.packbits`). Mask identity: the same without the levels. Component identity: per level, bond count, component count and component sizes in component order, int32 little-endian. | `family.py` docstring; `test_family_identities_distinguish_levels_masks_and_components` |
| M1-3 | **The bundle.** The identity build writes the arrays themselves (bases and comparison arrays, §3.4 step 2 serialization) beside the record. Later jobs load those bytes and verify them; they do not recompute a terrain. Paths are declared literals with forward slashes. The record is canonical JSON (sorted keys, compact, ASCII, one trailing LF). A record is never overwritten. | `identities.py`; the bundle tests |
| M1-4 | **The spectral routine** is the probe's, unchanged (disclosure 2). | `spectral.py` |
| M1-5 | **η₀ in the digest by rule** (disclosure 5). | `config.py` |
| M1-6 | **Platform policy of the tests** (disclosure 3). | `test_f9_m1.py` docstring |
| M1-7 | **Same-family verification** is by identity of the two compositions' comparison arrays and of their mask identities, with the raw-index relation recorded (disclosure 4). | `identities.build_identity_record` |
| M1-8 | **`is_informative` lives in `geometry`** as the definition of §5.5 step 4. M1's identity build does not use it; the evaluator module will. | `geometry.py` |
| M1-9 | **Deferred to later modules:** masters and seed panels; stream keys and the terrain, composition and object codes they need; the dynamics; atomic writing of the bundle of record (the runner's). | `config.py` docstring |
| M1-10 | **The record carries the environment** it was built on (platform, Python, numpy), so its identity differs between machines by design. | `identities.environment` |

## 6. Questions

**Q1. Defects.** Does any function compute something other than what the cited contract clause defines? Please attack in particular: the corner rule in `geometry.edge`; the family's level set and nesting; the comparison arrays on TC and TB; the TD core.

**Q2. Declarations M1-1 to M1-10.** For each: ACCEPTABLE, REQUIRES CHANGE (say what), or REJECT.

**Q3. The spectral routine (disclosure 2).** Is carrying the probe's routine the right reading of "the committed routine"? Is the measured error enough, or is an interpretation for Mike needed?

**Q4. Cross-platform families (disclosure 3).** Is the test policy right? Is there anything M1 should record or check now so that a difference between the container and the canonical machine is understood when the job of record runs?

**Q5. The bundle (M1-3).** Is storing the arrays and binding later jobs to the stored bytes a sound reading of "these canonical objects are the ones every later job uses and binds"? Is `verify_bundle_deep` checking the right things?

**Q6. Anything else** that should be repaired before placement.

## 7. Return format

One downloadable `.md` file, receipt table first. End with exactly one line, plain, at column 0, in one of these forms:
`FINAL VERDICT: SOUND`
`FINAL VERDICT: DEFECT-WITH-REPAIR`

*L1, 2026-11-16. Nothing placed; no run on the canonical machine; nothing in `e1` or `f8` modified.*
