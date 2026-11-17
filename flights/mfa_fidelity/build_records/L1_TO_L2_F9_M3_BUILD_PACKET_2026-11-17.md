# L1 → L2 — Flight 9 M3 build review, round 1: the composition evaluator (§5.5)

**Date:** 2026-11-17. **Register:** module build review (receipt first). Not a run authorization. M3 holds no master, runs no dynamics and reads no run record.
**Repository pin:** `ee-theory-lab` `main` at `6e731b821092083bc8acce16a23b2f56b6866354` (the M2 placement, checked against the remote before this packet was built). Nothing of M3 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Decision authority:** Mike. He said "build m3" on 2026-11-17, after M2 was placed with your round-2 SOUND.
**M2 on the canonical machine:** the whole M2 module passed there before the placement commit (63 passed, Python 3.14.4; `build_records/f9_m2_module_canonical_2026-11-17.txt`).

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's digest against `MANIFEST.txt`. Then wait for Mike's "execute".

## 1. What M3 is

Contract F9 v0.7 §5.5, steps 1 to 9, for one level of one arm: from the 40 seed maps (integer tail-tick counts) to the observed map's record and, per index, the typed resample counts and the result. Two new files; no placed file is edited.

| File | SHA-256 | Contents |
|---|---|---|
| `mfa_instrument/f9/evaluator.py` | `362b53d13f99adfa8f0172a60a9c1254c02e4db0cefcaaaaef0a59f4f3fc8e5e` | `occupied_region`, `step4`, `distance_grid`, `q95`, `joint_discrepancy`, `IndexFamily`, `fit`, `evaluate_map`, `resample_multiplicities`, `result_from_counts`, `evaluate_level`, `index_families`, `arm_level_key`; its own declaration digest `79e93ccade624ec473c7c60225183458e0ed168e13c4e23fb7dbaa6ed2d2fef7` |
| `tests/test_f9_m3.py` | `877c784e27e2c1ca5912ce7893f4d74898e71e494b5a8a3ac2f52c6a42cc8463` | 35 tests |

Not in M3, deferred to named later modules: combining indices, levels and arms (§5.6); the reports of §5.7; reading 40 run records into the seed maps, persisting level records, and binding them (runner); the known-answer corpus and the qualification of §6 (which will call this evaluator); closure comparators and T0's tests.

## 2. The design in one paragraph

The contract's prototype used floats and a k-d tree. The module does not. Every decision is made on integers or on correctly rounded operations, so that a decision cannot differ between the container and the canonical machine, and a tie cannot be decided by rounding. The criterion p̃ ≥ θ is an integer inequality. Bond midpoints lie on the half-cell lattice, so in doubled coordinates the squared distance from any lattice point to the nearest bond of an edge is an integer; the module computes that grid exactly for the observed edge and for each contour it examines, and a distance in cells is one square root and a halving. The quantile's interpolation index is an exact fraction. The pruning's reach is an integer disc.

## 3. Declarations (for your review; Mike ratifies with the governance record)

| # | Declaration | Where |
|---|---|---|
| M3-1 | **Criterion on integers.** With B the 3×3 periodic box sum of the seed-summed counts (seed multiplicities applied), the region is {B·10⁶ ≥ θ_micro·9·40·1000}. This is p̃ ≥ θ with ties included, evaluated exactly. The float p̃ is for reports and decides nothing. | `occupied_region`, `p_tilde` |
| M3-2 | **Edge, components, informative level.** `geometry.edge` and the counts of §5.5 step 4, with the reason recorded: region empty or full (`no edge at theta`), region or complement under 100 cells, edge under 40 bonds. | `step4` |
| M3-3 | **Distances.** Integer squared distance on the 2L×2L torus of doubled coordinates, by two exact passes; cells = sqrt(d²)/2. Distances are to the whole opposite edge. | `doubled`, `distance_grid` |
| M3-4 | **Quantile.** For n sorted values, 0.95·(n − 1) = k + r/20 with (k, r) = divmod(19(n − 1), 20); the value is x[k] + (x[k+1] − x[k])·(r/20), x[k] alone when r = 0. | `q95` |
| M3-5 | **S.** The maximum of: the global quantile each way, and one quantile for every component with at least m = 40 bonds on each side. A side with no resolved component adds no term and the record says so. Components under m bonds stay in both global terms. | `joint_discrepancy` |
| M3-6 | **Pruning and the minimum.** A level ℓ is admissible for an edge of n bonds when at least k + 1 bonds (k = 19(n − 1)//20) have min ω < ℓ ≤ max ω over the cells whose centres lie within ε + 0.5 of the bond, the disc decided as squared doubled distance ≤ (2ε + 1)² = 25. Only admissible levels are examined; they are examined in increasing ℓ and a contour replaces the best only when its S is strictly lower, so the lowest ℓ keeps a tie. A contour's evaluation stops as soon as one of its terms is not below the best S so far. `brute=True` examines every level. | `IndexFamily._intervals`, `admissible`, `fit` |
| M3-7 | **Families and labels.** `index_families` builds both indices' families for a terrain from an identity bundle's arrays: one shared set of contours on a same-family terrain, traced once and fitted once, with each index's own label by M1's `level_label`; separate families on TB; empty families on T0 (`no eligible contour`). λ* is recorded only where Δ ≤ ε. Otherwise the record carries the least S among the contours examined, labelled descriptive. | `IndexFamily`, `shared_with`, `index_families` |
| M3-8 | **The resampling stream.** `Generator(PCG64(SeedSequence([2⁶⁴ + 905] + key)))`, one draw `integers(0, 40, size=(1000, 40))`, rows turned into multiplicities. `key` is the caller's tuple of integers in [0, 2⁶⁴). For an arm and level of a panel the key is (master, terrain code, composition code, κ in micro-units) by `arm_level_key`, using M2's codes and refusals. The role exceeds every master, so no evaluator stream is a run's stream. The same resampled map serves every index. | `resample_multiplicities`, `arm_level_key` |
| M3-9 | **Typing and result.** Each draw: C (valid, Δ ≤ ε), A (valid, Δ > ε, including the case that no level is admissible), I (fails step 4, with its reason; no discrepancy is assigned). Result in the contract's order: n_I > 50 unstable edge; n_C ≥ 950 compatible; n_A ≥ 950 adverse; otherwise unresolved. Step 9 is applied only when the observed map is informative and the index's family is not empty; otherwise the index is `not informative` with cause `no edge at theta`, `below the informative minimum` or `no eligible contour`. | `evaluate_level`, `result_from_counts` |
| M3-10 | **Constructed resample sets.** `evaluate_level(..., multiplicities=...)` replaces the declared stream's rows with given valid rows, for §6.1's constructed sets (exactly 50 and 51 invalid draws). A record made that way carries `declared_stream: false`. | `evaluate_level` |

## 4. Evidence

- `build_records/f9_m3_module_container_2026-11-17.txt` — **35 passed in 138.57 s** in L1's container (Python 3.13.18, NumPy 2.5.3).
- What the tests establish, by group. Criterion: against exact rationals (`fractions.Fraction`) on random counts and random multiplicities; ties at θ included, and one tick fewer in one seed removes exactly the nine cells it should. Distances: `distance_grid` against pairwise integer distances from the definition, including across the wrap. Quantile: against exact rationals and against numpy. S: hand cases (a strip moved three cells; across the wrap; a 40-bond square that only its own component term sees; a 36-bond square that nothing sees, which is the claim's stated limit) and irregular regions against pairwise float distances with numpy's quantile. Pruning: the per-bond intervals against a cell-by-cell search; pruned against exhaustive search on twelve point maps over three families, and on every one of the 1,000 resamples of a level whose draws split 609 compatible to 391 adverse; the family minimum against an independent exhaustive search. The lowest level keeps an exact tie, in both orders of listing. ε is inclusive at 2.0 and refuses 3.0. Stream: the multiplicities equal an explicit `PCG64(SeedSequence([2⁶⁴ + 905, …])).integers` draw. The result table at 950/0/50, 949/1/50, 0/950/50, 949/0/51 and others. Levels: on its own contour (compatible for both indices of a same-family terrain, with separate labels), a level set of TB's height index (compatible under H, adverse under P), the unavailable states, and constructed sets with exactly 50 and 51 invalid draws. The contour cache changes no result. Everything placed before M3 hashes to its placed identity.

## 5. Disclosures

1. **Every map in the tests is synthetic.** Integer seed maps built from a chosen region, flat or with binomial noise. No run of the rule, no master, no run record, no probe output. L1 has not seen the boundary endpoint.
2. **The pruning's exactness rests on an argument, and on finite evidence.** The argument is the contract's (§5.5 step 7): a contour bond within ε of a bond e has both its cells within ε + 0.5 of e, so ℓ lies in (min ω, max ω] over those cells; and Q₀.₉₅ ≤ ε forces the k + 1 smallest distances to be ≤ ε, because the interpolated value is never below x[k]. The evidence is the agreement in §4. Q2 asks you to attack both.
3. **The exact-arithmetic design is L1's choice, not the contract's text.** The contract defines the quantities; it does not say how to compute them. L1 chose integers so that container and canonical decisions cannot differ. The values of S agree with a float reference to 1e-12 in the tests; where a float reference would round across ε, the module's value is the exact one.
4. **`Generator.integers` is a numpy algorithm**, like `choice` in M2. PCG64's raw stream is stable; numpy does not promise the method never changes. The canonical environment pins numpy.
5. **Speed, unpriced on the canonical machine.** In the container: tracing a contour and its distance grid about 12 ms, once per contour per family while it stays in the cache of 256; a level of 1,000 resamples about 13 s in the tests once contours are cached (14 ms a draw). TB under P has 2,600 contours. The contract's A.7 figure for its prototype was 0.09 to 0.11 s per draw for both indices; `resource_benchmark` (§8 step 10) prices this on the canonical machine.
6. **The bond minimum of step 4 could not be reached by a real region in L1's attempts**: a region that meets both cell minima seems always to have at least 40 bonds. The check is kept because the contract states it, and it is tested with a fabricated edge.
7. **The 3×3 mean moves edges, as the contract says it can.** With maps of 1 inside and 0 outside, two of nine neighbours reach θ and a straight strip widens by a cell each side; with 0.35 and 0.06 it does not. The tests state which they use. This is the declared estimator, not a defect.
8. **The key of an evaluator stream is a declaration made here** (M3-8). The contract says "a declared evaluator stream" and does not give its form. If you think its form is a ruling for Mike and not a module declaration, say so under Q5.
9. **M3 does not persist anything.** `evaluate_level` returns Python objects (numpy arrays of the 1,000 typed draws included). Serializing and binding a level record is the runner's, as for M2's runs.

## 6. Questions

**Q1.** Does the module execute §5.5 steps 1 to 9 as written, in the binding order, with λ, g, κ and the terrain absent from steps 1 to 4?
**Q2.** Is the pruning exact for the decision as implemented (M3-6)? Is there a map for which pruned and exhaustive search give different decisions, or, where Δ ≤ ε, a different Δ or level?
**Q3.** Declarations M3-1 to M3-10: for each, ACCEPTABLE, REQUIRES CHANGE (say what), or REJECT.
**Q4.** The exact computations: is `distance_grid` exact for every input, is `q95` the contract's quantile, and can any decision of the evaluator depend on floating-point rounding in a way that could differ between platforms?
**Q5.** Any contract ambiguity that should go to Mike as a ruling and not be settled in the module.
**Q6.** Anything else to repair before placement.

## 7. Return format

One downloadable `.md` file, receipt table first. If you find a defect, include a program that reproduces it on the packet's bytes. End with exactly one line, plain, at column 0, with no bold and no trailing text:
`FINAL VERDICT: SOUND`
`FINAL VERDICT: DEFECT-WITH-REPAIR`

*L1, 2026-11-17. Nothing placed; no run on the canonical machine; no placed file modified.*
