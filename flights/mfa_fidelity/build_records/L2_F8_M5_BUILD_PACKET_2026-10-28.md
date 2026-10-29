# L1 → L2 — Flight 8 instrument module M5: build packet (round 1), 2026-10-28

**Register.** Instrument build review under Contract F8 v0.8.4 (FROZEN, `e87277a2d11e948f`). Verdict SOUND / DEFECT-WITH-REPAIR. Nothing placed until L2 clears and the canonical suite passes on Mike's machine; no run authorized. M1–M3 placed at `7023916`; M4 cleared SOUND (round 1, 2026-10-28) and in placement. This zip carries the whole package including M4's `verdict.py` (`c79ce0d7c81e21d5`, unchanged from its cleared identity — M5 imports it), the contract files, and the M4 and M5 test modules.

**Scope (contract §3, §4.8, §7.3 items 2–4).** The closure and the census: the §3.1 map, its two fixed-point tables, §3.4's tolerances (Δm; the bands and MDD ceilings from the calibration census), m_infl, Appendix B's pair closure, the dense reference census (reference of record), reference stability, and the E1-R-grammar design-stability program (finite-N projection sweeps). E1's M5 framework carries (roles, outcome hygiene, halts fail closed, replay validation); its content is rebuilt from §3. E1's T1–T3/T2-L recovery program is **not** carried: F8's P1 belongs to M-P1 (§4.11, next module).

## Files (SHA-256, LF)

| File | Identity | Status |
|---|---|---|
| `instrument/mfa_instrument/f8/closure.py` | `8040a762f2d2d58b35af5b4e06289852e24b4ba93890f8fbfda8cdba5017feb0` | new (M5) |
| `instrument/tests/test_f8_m5.py` | `f8bd589a1045430b0705e60b20dafe3a0b946b2f3a185459f73acd67f316cdeb` | new, 23 tests |

Test record (container): `test_f8_m5.py` **23 passed** (39 s); all four F8 modules together in one process **143 passed** (123 s). `e1/` untouched (E1 M5's declaration digest asserted unchanged).

## Appendix A, bit for bit

`g_map` and `fixed_point` are Appendix A's `fmap` / `fixed_point` in procedure and float64 expression order (start 0.5, tolerance 1e-15, iteration); `rho_sk` is exactly 0 for m ≤ 1. `verify_against_appendix_a` reads the committed `APPENDIX_A_OF_RECORD.md`, checks its identity, and requires **bit equality** with its JSON for: the 24-level `rho_sk` and `rho_re` tables; Δm's lower (0.021581283487712034), upper (0.022300265992375), s and value (**0.120126265992375**); `m_infl` (1.1765); `m_lat` (1.14144783…, Appendix B.2 linearization by bisection); π₁ against M3's chain rates. The skeleton multiplier J₀ = e^(−μ) + gλ̄ is exactly 1 at m = 1 (tested to 1e-15); ρ*_sk is 0 at every level ≤ 1 and positive from the first level above. The nonlinear pair map (Appendix B.2, `pair_approx.py`'s equations) reproduces B.3's branch values to 2e-3 (0.051 / 0.242 / 0.526 skeleton at 1.2 / 1.5 / 2.5; 0.066 / 0.176 / 0.544 realization at 0.25 / 1.0 / 2.5).

**Closure publication** (`ClosurePublication`, replay-validated, identity-bound): m_closure = 1, m_lat, m_infl, Δm, ρ*_sk, ρ*, pair skeleton and pair realization at the 24 levels — the comparators of §1.2′, reported, never scored.

## The dense census (§4.8)

`dense_grid_micro(701)`: 701 levels over [0.25, 2.50] by M1's exact-rational round-half-even rule (the same rule gives M1's 24 levels at 24 points). `classify_grid`: per level, the realization orbit from the null's stationary density (3,000 ticks), M2's geometry on the orbit (ten windows, S_term = window 10), status precedence against M3's certified θ_P/θ_T, the 16/2/4 label on 20 identical statuses → S/N/U; the sequence adjudicated by M4; structure class from the rule (E1's five classes). **Role discipline:** `reference_of_record` is issued only on the exact declared grid with zero halts (`dense_reference`); any other grid is `analysis_subset`. Validation by replay. The module carries no reference result. Run in the container (not a canonical job; shown for L2's information only): class **NO-NULL-PHASE**, rule 2 `no_null_consistent_phase`, all 701 labels S — the morphology §1.3(a)/§4.9 pre-register. The canonical dense job on Mike's machine creates the record.

**Reference stability** (`StabilityAudit`, `canonical` only against the reference of record): the class on alternative grids of 351 and 1,401 points; and every fixed point by an **independent solver** (bisection on g(ρ) − ρ) against Appendix A's iteration, max |Δ| = 1.7e-13 over both objects at 24 levels, tolerance 1e-11.

## §3.4 tolerance machinery

`CalibrationCensus` (job 0's record, built from the per-level 20-seed tail densities of the realization and the skeleton-high parts on the calibration panel; shape enforced; replay from raw content): ŝ(m), ŝ_sk(m) as seed-to-seed SD (ddof 1; extinct runs contribute 0, so ŝ_sk ≈ 0 below the boundary); MDD_X(m) = k_R·ŝ_X·1.2533/√20; the two maxima against the 0.02 ceiling; `ceilings_met` and `stop_path_triggered` (its complement — the stage stops before any canonical census). `evaluability_band(census, object, i, i+1)` = k_R·√(ŝ_X(m₋)² + ŝ_X(m₊)²)·1.2533/√20 with X the sweep's own object (skeleton → ŝ_sk; realization → ŝ), defined only for adjacent pass-1 levels; `fidelity_band(census, i)` = k_R·ŝ(m)·1.2533/√20. Tests check the arithmetic term by term, the stop path on an over-dispersed census, and shape refusals.

## Design stability (E1-R grammar, §7.3 item 4)

`finite_n_counts`: the closure realized by N independent cells (each sees the global density; two binomial draws per tick; Binomial(N, π₁) start) — the zero-correlation lattice; its tail sits on the map's fixed point (tested). `projection_sweep(i)`: 24 levels × 20 seeds from `SeedSequence([master, i, level, seed])`, each run scored by M2 on the exact count grid against M3's thresholds, labelled 16/2/4, adjudicated by M4; replay-validated. `design_stability(ref, sweeps)`: `canonical` iff exactly the declared 200 sweeps, zero halts, against the reference of record; `evaluable` false on any halt (HALT_POLICY: NOT EVALUABLE, rates over the attempted denominator); `design_stable` = every sweep's class equals the reference's; one-sided Clopper–Pearson lower 95 % (exact; 0.985 at 200/200, E1's figure). Container smoke: sweeps 0–2 all NO-NULL-PHASE.

## Declarations for L2 (none pre-approved)

- **M5-1 Dense grid positions.** 701 points is §4.8's [PROPOSED — E1's count], not among the 26 values the freeze record ratified by name. Positions by M1's round-half-even rule; since 700 is not a multiple of 23, the dense grid does **not** contain every pass-1 level (E1's did, with 1,000-micro steps). The pass-1 grid is scored separately where needed; the reference of record is the dense grid alone. Mike ratifies 701 (or another count) with the governance record.
- **M5-2 Design-stability ensemble = 200 sweeps**, E1's declared value carried; master **420261028** (new, declared; distinct from all panel/validation masters). Both ratified with the governance record.
- **M5-3 Reference stability has no template axis.** E1's "alternative templates" were base-rank templates for its null; under homogeneous inert bases F8 has none. The stability axes here are grid resolution and solver independence. If L2 wants a further axis (e.g. orbit horizon or start), L1 adds it as a declared alternative.
- **M5-4 Projected label from the stationary start.** The orbit starts at π₁ (the null's stationary density), the realization's own initialization (§2.9, §4.1), and runs 3,000 ticks; M2's geometry is applied to the deterministic orbit (not on the count grid, so M2's exact-count recovery is bypassed by a dedicated `projected_tail_stats`, as E1's M5 did).
- **M5-5 `tolerance_ensembles` / `tolerance_program` record kinds.** §7.3 item 4 lists these E1-R kinds as carried; in F8 the tolerances come from the two-part calibration census (§3.4), which is job 0. L1 reads the F8 content of those record kinds as the census's two parts (ŝ, ŝ_sk per level) and asks L2 to confirm, so M7's package specification names them correctly.

*L1, 2026-10-28.*
