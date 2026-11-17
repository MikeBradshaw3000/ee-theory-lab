# L1 → L2 — Flight 9 M2 build review, round 1: streams, the per-cell-index rule, the run record

**Date:** 2026-11-17. **Register:** module build review (receipt first). Not a run authorization. No master is drawn; M2 holds no master.
**Repository pin:** `ee-theory-lab` `main` at `7af50941e47249965dc6c8b2a502d06166e08866` (the M1 placement, checked against the remote before this packet was built). Nothing of M2 is committed. Every file in this zip that exists at the pin is a byte copy of it.
**Decision authority:** Mike. He said "build m2" on 2026-11-17, after M1 was placed with your round-3 SOUND.
**M1 on the canonical machine:** the whole M1 module passed there before the placement commit (102 passed, Python 3.14.4; `build_records/f9_m1_module_canonical_2026-11-17.txt`). That run is the first off Linux.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's digest against `MANIFEST.txt`. Then wait for Mike's "execute".

## 1. What M2 is

Contract F9 v0.7 §5.1 (N1) without the terrain builder, which is M1: the stream of §2.5, the rule of §2.4 with a per-cell index, the three declared starts, one run, the run's record (§5.1 and the §2.11 window record), a serialization of that record, and the comparison the `reduction_check` job of §8 step 2 will make. Three new files; no placed file is edited.

| File | SHA-256 | Contents |
|---|---|---|
| `mfa_instrument/f9/streams.py` | `1d1bbc48abe1df54fed25c072402d64ced71a2b3b85a44cf818fb783b90afaec` | codes, the key, the two generators, what a master may not be; its own declaration digest `f7ba30034d74f23e0a1e586228064407ad1b236a2a6425d9c924caae003ba77e` |
| `mfa_instrument/f9/dynamics.py` | `11ad2ef15ef30520018ee15501cd43d5f7bd126c4e268e398c85ed7ad9cafed3` | `step`, `arm_context`, `F9RunSpec`, `initial_state`, `run`, `serialize_run`, `parse_run`, `replay_equals`, `reduction_check` |
| `tests/test_f9_m2.py` | `c8c3e1f9a01b2193a9e4a5fe9dc10afb9220e35bcb8d5a7018e5042c7fb9c59c` | 59 tests |

Not in M2, deferred to named later modules: jobs and their records, file layout and atomic writing, authorization and master handling (runner); the §2.11 statistic and every report (reports); closure comparators (N5); the evaluator (N-E).

## 2. Declarations (for your review; Mike ratifies with the governance record)

| # | Declaration | Where |
|---|---|---|
| M2-1 | **The key.** The contract's tuple in its order as seven non-negative integers: (master, terrain code, composition code, object code, initialization code, κ in micro-units, seed index). Codes: terrains 0–7 in the order of `F9_TERRAINS`; P 0, H 1; realization 0, skeleton 1; stationary_floor 0, all_active 1, low 2. The tick stream is `Generator(PCG64(SeedSequence(key)))`. | `streams.py` |
| M2-2 | **Starts.** Realization: each cell active with probability π₁, decided by the tick stream's first full-grid uniform. Skeleton all-active: nothing drawn. Skeleton low (T0 only, §5.8): exactly round(N·0.02) = 200 cells by `choice` without replacement from a separate initialization-pattern stream, `SeedSequence(key + (1,))`. These are the conventions of the placed Flight 8 module, carried; the contract states the starts but not their draws. | `streams.py`, `dynamics.initial_state` |
| M2-3 | **No master in the module.** The contract draws masters by stage (§8), so a master is an argument. Declared: a master is an integer in [1, 2⁶⁴); the five retired masters (E1, Flight 8's three, the probe's) are refused; masters below 10⁶ are test masters, reported as `master_class: "test"` in every record. Refusing a test master in a job of record is the runner's. | `streams.py` |
| M2-4 | **Seeds.** Seed index 0–39 is the last key element. There is no seed panel. | `streams.py` |
| M2-5 | **The arm context.** A run takes its index from the STORED bases of an M1 identity bundle (composed, hashed, and required to equal the identity record's `index_sha256` for the arm) and g_spec and spr from the record. g = κ·g_spec by M1's `spectral.gain`. The context does not establish that the bundle was verified or is canonical. | `dynamics.arm_context` |
| M2-6 | **The run's record.** counts[0..T] with counts[0] after initialization; extinction tick (skeleton only: first tick with zero active cells; the run then stops advancing and drawing, and its later counts and tail states are zero); survival = count > 0 at every tail tick; per W and cell: A, R₀, first and last window states, accumulated tick by tick. | `dynamics.run`, `_Windows` |
| M2-7 | **Serialization.** 8-byte magic, 4-byte little-endian header length, canonical-JSON header, then counts (int32), and per W: A, R₀ (uint16), first, last (packed bits). The header carries no libm value: the floor is its probability literal and rule, deactivation is μ. | `dynamics.serialize_run` |
| M2-8 | **What validates a record.** `parse_run` checks form, declarations, array hashes and the relations every record satisfies. It cannot know the trajectory. `replay_equals` reruns the record's run on the same machine and compares bytes. | `dynamics.parse_run`, `replay_equals` |
| M2-9 | **Reduction.** Twelve fixed (η, g, λ̄) cases, 200 ticks each at L = 100, from a declared apparatus stream `SeedSequence([9, 5, 1, case])` that is not a run key; each tick compared with the placed Flight 8 step in two forms: same g and λ̄, and g = 1 with λ̄ = g·λ (the effective gain as one number). With T0's g_spec from an identity record, all 25 levels of T0 at both floors are added (62 cases). The job and its record are the runner's. | `dynamics.reduction_check` |
| M2-10 | **Platform.** The activation probability passes through exp. A trajectory is reproducible on one machine and environment and is not claimed across platforms. The tests compare with a re-simulation, never with a stored hash. | docstrings |

## 3. Evidence

- `build_records/f9_m2_module_container_2026-11-17.txt` — **59 passed in 38.85 s** in L1's container (Python 3.13.18, NumPy 2.5.3).
- What the tests establish, by group: the key and codes, 31,000 declared runs with distinct keys, refusals of undeclared runs, keys and masters; the stream equals the 53-bit uniforms of PCG64's raw words; `step` equals a cell-by-cell implementation written from the contract's sentences on a heterogeneous index (with a check that no decision sits within 1e-12 of its threshold); two-phase timing and periodic wrap on a hand case; the floor is not gated; the reduction, and that the reduction check reports a one-cell difference; the three starts; five full runs (two realization, three skeleton, on T0, TB under H and TC under P), each compared with an independent driver that keeps the whole tail and applies the probe's window formula; the window accumulator on hand-counted sequences; round trip, 29 header changes and 7 array changes refused (the array changes also with every hash restated); a consistent forgery that the parser accepts and replay refuses; and that the M1 files, the root, `e1`, `f8` and `gates` hash to their placed identities.

## 4. Disclosures

1. **How a master is drawn is not stated in the contract, and M2 does not decide it.** §2.10 and §8 say when each master is drawn and that it is fresh. They do not say by what procedure a value is produced or where it is recorded. L1 will put this to Mike as a ruling before the runner is built.
2. **The tests run the rule under test masters.** Five full runs and a few starts, in the container. L1 looked at their mechanics only: counts, extinction ticks, draw counts, and the window record against the re-simulation. No occupancy map was rendered and nothing was computed against an index contour. One skeleton run goes extinct and two do not; the tests need both branches and say nothing about why.
3. **`choice` without replacement and `Generator.random` are numpy algorithms.** PCG64's raw stream is stable; numpy does not promise that the methods built on it never change between versions. The canonical environment pins numpy. The uniform is tested against the raw words; the low-start pattern is not pinned to a stored value.
4. **Size.** One serialized run is 141,581 bytes at most in the tests (header about 2 kB). At the contract's 89,000 runs that is about 12.6 GB uncompressed. L1 computed this figure; it has not been priced on the canonical machine. Compression and layout are the runner's.
5. **§5.9 binding is partial at this level.** A run record binds the contract, the configuration declaration (which carries θ, ε and m), the stream declaration, the identity record, the arm's index hash, spr, g_spec and g, the lattice, horizon, tail and windows, and the stream key. It does not bind an evaluator identity or a qualification protocol identity: neither exists in M2. L1 reads "every record binds what exists when it is written" as leaving those to the runner's record around the run. Q4 asks whether that reading holds.
6. **The header's spr is not checked against g_spec by the parser**, because that relation needs q, which passes through libm. `arm_context` checks it against the identity record's own q. The parser checks that g follows from the level and g_spec.
7. **`ArmContext` is an ordinary dataclass.** A caller can construct one by hand with any array. `run` checks only that its terrain and composition are the run's. Restricting runs of record to contexts built from the verified canonical bundle is the runner's.
8. **Speed.** About 0.9 s per realization run and 1.0 s per surviving skeleton run in the container, the same order as the probe's figures in §8.
9. **L1 has still not seen the boundary endpoint** and M2 reads no probe output. The probe's source was read for its step, stream form and window formula.

## 5. Questions

**Q1.** Does `step` execute §2.4 and §2.5 exactly, and does `reduction_check` test the reduction requirement of §5.1 as written ("equal state, effective gain, floor, μ, timing and uniforms")?
**Q2.** Declarations M2-1 to M2-10: for each, ACCEPTABLE, REQUIRES CHANGE (say what), or REJECT.
**Q3.** The run record against §5.1 and §2.11: is anything the contract requires per run missing, and is the window accumulator's R₀ the "observed inactive segments" of the pre-probe declaration §6?
**Q4.** Disclosure 5: is the binding carried by a run record sufficient at this level under §5.9?
**Q5.** Is there a serialized record that should be refused and that `parse_run` accepts, other than the kind M2-8 names (consistent but not the trajectory)? Is there one that `replay_equals` accepts?
**Q6.** Anything else to repair before placement, and any contract ambiguity that should go to Mike as a ruling and not be settled in the module.

## 6. Return format

One downloadable `.md` file, receipt table first. If you find a defect, include a program that reproduces it on the packet's bytes. End with exactly one line, plain, at column 0, with no bold and no trailing text:
`FINAL VERDICT: SOUND`
`FINAL VERDICT: DEFECT-WITH-REPAIR`

*L1, 2026-11-17. Nothing placed; no run on the canonical machine; no placed file modified.*
