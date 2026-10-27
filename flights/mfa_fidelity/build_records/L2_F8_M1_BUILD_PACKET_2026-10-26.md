# L1 → L2 — Flight 8 instrument module M1: build packet (round 1), 2026-10-26

**Register.** Instrument build review under Contract F8 v0.8.4 (FROZEN, `e87277a2d11e948f`; freeze commit `5d8af44`). Same register as E1's M1–M7 builds: L2 reviews the source against the contract and the carried grammar; verdict SOUND / DEFECT-WITH-REPAIR; nothing is placed until L2 clears it and Mike's canonical suite passes on his machine. Nothing here authorizes a run.

**Scope of M1 (contract §4.1; design note v0.3 §5).** Configuration and levels, the seed panel from a new master, the instrument version identity, the frozen-declaration preflight, the stream derivation of §2.5 — and, because the frozen `e1` dynamics do not execute the hazard rule (§2.4, last sentence), the substrate stepper that does. Two source files and one test module, in a new package `mfa_instrument/f8/` beside `e1/`; **nothing in `e1/` is modified** (`git status` shows only the new paths; the E1 M1/M2 test module still passes, 58/58).

## Files (SHA-256, LF)

| File | Identity |
|---|---|
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `afbce4b29272c9a1cda7c9aa0249a99785b5eaeef16423e0e923ed70275b59d4` |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `b854b1360a0c75c6162f396fd2452cbad541cf83a7481ff9eec36ce0846e4ea0` |
| `flights/mfa_fidelity/instrument/tests/test_f8_m1.py` | `4a391b83a074c8d46f649085c76f3dc54ed15994ff114b7862fdc414a5371936` |

Test record (container, not the canonical environment): `python3 -B -m pytest tests/test_f8_m1.py -q -p no:cacheprovider` → **29 passed** in one process. The canonical run is on Mike's machine under the twenty-pin environment, whole module, one process.

## What the build does

1. **Levels.** `F8_LEVELS_MICRO`: 24 values, 250000 … 2500000 by exact rational round-half-even, as a frozen literal **equal to the `levels_micro` list of `APPENDIX_A_OF_RECORD.md`** (`94d527624beafa7c…`). `verify_against_appendix_a` reads the committed Appendix A, checks its identity, and checks its JSON inputs (L, N, mu, eta0, Dt, n1, T, tail, window, W_res spacings, sweep) and its `levels_micro`, `s_micro`, `W_res_micro` against the module. Appendix A carries no `g`; g = 1 is ratified by name (freeze record §3 item 4), not through Appendix A.
2. **Frozen preflight** (`verify_frozen_identity`, E1's pattern carried): every literal recomputed from its rule; three literal digests (levels, canonical panel, calibration panel) and the declaration digest; every live global compared with the declaration field by field and type by type; hard contract values stated a third time independently; W_res = 3 s; every level's λ̄ reachable by homogeneous bases in [0, 1]. Runs inside every `f8_run_spec` construction and every `dynamics.run`. Tamper tests cover each literal and the rule parameters.
3. **Control coordinate.** λ̄(m) = m·(1 − e^(−μΔt))/(gΔt), m = level_micro/10⁶ exactly; m = 1 ⇔ gλ̄Δt = 1 − e^(−μΔt) is tested as an identity. The hazard consumes λ̄ directly. The homogeneous base b = λ̄^(1/4) that F_2_symmetric would need (F(b,b,b) = b⁴ under the frozen weights) is computed and recorded in the spec; the test checks F(b,b,b) = λ̄ to 8 ulp at every level. F is inert (freeze record §3 item 2).
4. **The rule** (`dynamics.py`): activation 1 − exp(−[η_floor + g·λ̄·d]Δt), deactivation 1 − exp(−μΔt), both in the contract's written form; d from the frozen package's `_moore_sum_a` (imported, so the Moore offset order is the specification's); synchronous: all probabilities from the state at t, one full-grid uniform per tick, `where(x, u ≥ p_deact, u < p_act)`. Tests: probabilities equal the written forms; η = 0 and d = 0 gives exactly 0; the all-inactive skeleton state is exactly absorbing under any uniforms; g = 0 outcomes depend only on own state and own uniform; a single active cell activates only its eight Moore neighbours in one tick (synchrony); periodic boundaries; **bit-identity with the committed probe's rule** (`lattice_check.py`, `92a3e8d4…`) over 50 ticks under identical uniforms.
5. **Objects.** `skeleton_high` (η = 0, all active, no init draw), `skeleton_low` (η = 0, exactly 0.02·N cells from a declared INIT_LOW stream), `realization` (η₀ = −ln 0.99, stationary start π₁ = a/(a+q) drawn cell-wise from the run stream, no burn-in), `null` (g = 0, same start). η₀'s single-tick probability equals 0.01 and π₁ equals Appendix A's 0.0522823… to 1e-15 (tested).
6. **Record.** rho[0] at t = 0, rho[t] after tick t; tail = last 1000 post-advance ticks in 10 windows of 100; survival = active count > 0 in every window; an extinct skeleton stops advancing (exactly absorbing) with zeros thereafter and is a valid observation (§4.11). Draw accounting is persisted (`draws_consumed`). `write_rho_table` keeps E1's `["Tick", "rho_global"]` column grammar with the F8 row meaning stated.
7. **Panel policy.** A production-shape run (50×50, 3000 ticks) must use a canonical-panel seed, or a calibration-panel seed for the realization/skeleton-high objects only (§7.3 job 0); below production shape any seed is admissible (controls, smoke).

Smoke at production shape (seed panel[0], container, 0.3–0.5 s per run): realization 0.0673 at m = 0.25 (Appendix A branch 0.0669), 0.1517 at 0.9348; null 0.0526 (π₁ 0.0523); skeleton-high extinct at m = 1.4239, surviving at 1.6196 (0.221) and 2.5 (0.517) — consistent with the closures and the design evidence (§B.4). These are smoke numbers, not results.

## Build declarations for review (L2) and ratification (Mike) — nothing pre-approved

- **B1. Masters.** Canonical panel master **20261026** (the build date, E1's convention); calibration-census master **120261026** (separate from all others, §7.3 job 0). Both DERIVED@BUILD (contract §8); both panels rule-generated by E1's derivation (`SeedSequence(master) → 20 distinct uint32`), hardcoded with digests, disjoint from each other and from E1's retired panel. Of record only when the F8 governance record names this module's identity.
- **B2. Stream key = (seed, OBJECT_CODE, level_micro).** The contract's §2.5 names "seed-panel master → per-seed stream → per-level identifier". The build adds the object code so the skeleton-high, skeleton-low, realization and null runs of one (seed, level) draw from four distinct streams (codes 1–4), and the skeleton-low initialization pattern from a fifth (code 10). This preserves §4.11's independence basis (no draw shared across levels) and extends it across objects, which T-S2's low-vs-high comparison relies on. L2 to say whether the addition is a conforming realization of §2.5 or needs a contract clause.
- **B3. Probabilities in the written form** `1.0 − exp(−h)` rather than `−expm1(−h)`: bit-faithful to §2.4 and to the committed probe; the rounding difference is ~1e-17 and immaterial, but the choice is stated so no reader infers otherwise.
- **B4. λ̄ consumed directly; bases recorded, not executed.** Under homogeneous bases F cannot bear on anything (freeze record §3 item 2); the build records b = λ̄^(1/4) and proves F(b,b,b) = λ̄ in the test rather than routing the hazard through the frozen `Dynamics` F dispatch (whose chain this rule mode does not execute). L2 to confirm this is the right reading of §2.2.
- **B5. Record convention** (rho[t] after tick t; tail = ticks T−999 … T). E1's table carried the pre-update density; the F8 meaning is stated in the module docstring and column grammar is kept.

## What M1 does not do

No thresholds, caches, labels, verdicts, evaluator, audits or records (M2–M7). No contract value is changed; no PROPOSED value is represented as approved beyond the freeze record. The container's library versions (numpy 2.5.3, pyarrow 26.0.0, pandas 3.0.5) are not the canonical twenty pins; the canonical suite is the second execution.

*L1, 2026-10-26.*
