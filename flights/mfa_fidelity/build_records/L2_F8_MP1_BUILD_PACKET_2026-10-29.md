> **Round 2 (2026-10-29).** This packet is amended for the round-2 return: identities updated to the repaired `evaluator.py` (`61179c7670ea8db3`) and `test_f8_mp1.py` (`f9abdd8e657ba917`, 35 tests), declaration digest `cc1f176eb12dde34…`, known-answer record `F8_MP1_KNOWN_ANSWER_CONTAINER_2026-10-29.json`. The repairs D1–D7 and the new declaration MP1-7 are in `L1_TO_L2_F8_MP1_ROUND2_RESPONSE_2026-10-29.md`, which governs where the two differ. Wording correction (L2 r1 §7): with no located boundary the fidelity tier retains the boundary-independent realization comparisons and the steepest-ascent diagnostic; only boundary-dependent fields are unavailable, with their reason named.

# L1 → L2 — Flight 8 instrument module M-P1: build packet (round 2), 2026-10-29

**Register.** Instrument build review under Contract F8 v0.8.4 (FROZEN, `e87277a2d11e948f`). Verdict SOUND / DEFECT-WITH-REPAIR. Nothing placed until L2 clears and the canonical suite passes on Mike's machine; no run authorized. M1–M5 placed (`e1903fe`); M5's `closure.py` is the placed `9452dd11396350ab` (L2 SOUND rounds 3 and 5 — the round-4/5 Appendix A binding repair, declaration M5-6, changed nothing M-P1 imports: `evaluability_band`, `fidelity_band`, `closure_publication`, `CalibrationCensus`). This packet re-issues the 2026-10-28 packet (`3a063d37c4e98137`) against that identity; `evaluator.py` and its tests are repaired in round 2 (see the round-2 response); the test module passes 35 in the container. The zip carries the whole package, the contract files, and the M5 and M-P1 test modules.

**Scope (contract §1.1′, §1.2, §1.2′, §3.4, §4.11, §5.4).** The structural evaluator: the only module that adjudicates P1 (§4.7(2)). The four tests, the evaluability rule, the per-run grammar (extinction valid, apparatus halts unevaluable), the P1 determination, the fidelity tier, the sweep records and their provenance, and the known-answer qualification corpus. This is the scientific core of the flight; L1 asks L2 to read §4.11 beside the source clause by clause.

## Files (SHA-256, LF)

| File | Identity | Status |
|---|---|---|
| `instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db3` | new (M-P1) |
| `instrument/tests/test_f8_mp1.py` | `f9abdd8e657ba917` | new, 35 tests (round 2) |

Test record (container): **35 passed in 65 s** (round 2). `e1/` untouched.

## The four tests, as implemented (§4.11 wording in the docstring; the code follows it line by line)

- **T-S1′** on the skeleton-high sweep: m̂_c = the lowest level with surv ≥ 18 such that surv ≥ 18 at every level above it. Cases: (i) no level ≥ 18 → FAIL `no active phase in sweep`; (ii) ≥ 18 at every level → FAIL `no inactive phase in sweep`; (iii) ≥ 18 somewhere but survival not monotone above the candidate (a dip above it, or an isolated surviving level below it) → ND `non-monotone survival`; (iv) pass with m̂_c. Any unevaluable level → ND `apparatus (<halt key>)`. Tested case by case, including the threshold being exactly 18 (17 moves the boundary; 18 does not).
- **T-S1c** on levels m̂_c…m_max: a reversal is disregarded iff ≤ the combined band from the **skeleton part** of the census (`closure.evaluability_band(census, "skeleton_high", i, i+1)`); beyond it → ND `non-monotone at finite sample (<m₋>, <m₊>)`; any increase > f_J × (med(m_max) − med(m̂_c)) → ND `continuity unresolved at grid resolution (<level>)`. There is **no FAIL path** in this test (§1.2 R1); a steep rise below m̂_c is outside its domain (tested).
- **T-S2**: T-S1′'s procedure on the skeleton-low sweep gives m̂_low (its own (i)–(iv) and apparatus branches carry through with a `from skeleton-low boundary` note); pass iff |m̂_low − m̂_c| ≤ Δm, with Δm = the closure publication's Appendix A value 0.120126…; m̂_low above by two pass-1 spacings (0.1957) → FAIL `hysteresis`; by one (0.0978) → PASS; below by one → PASS (|·|). Tests show Δm is the operative bracket (at Δm = 0.05 the one-spacing case fails).
- **T-R1′** on the realization sweep, every level: unevaluable → ND apparatus; med(m) not > 0 → FAIL `realization extinct at <level>`; then the shared monotone/continuity body with the **realization part** of the census.
- **Determination**: PRODUCED iff all four PASS; NOT PRODUCED iff any FAIL (the first valid failure's cause in test order — a valid failure outranks an ND, tested); else NOT DISTINGUISHED with the first ND cause. When T-S1′ does not locate a boundary, T-S1c and T-S2 are recorded ND `not evaluable: T-S1′ did not locate a boundary (<cause>)` and T-R1′ still runs. `P1Evaluation.claim_strength` carries §1.1′'s sentence; the record names the census, the closure publication and the three sweeps by identity.

## Evaluability rule and the census

`band(census, obj, i, i+1)` is M5's `evaluability_band` — k_R·√(ŝ_X(m₋)² + ŝ_X(m₊)²)·1.2533/√20 with X the sweep's own object; no cross-object stand-in exists in the code path (the realization sweep cannot be scored with ŝ_sk). A **canonical** evaluation requires the **canonical** (M7-issued) census; synthetic sweeps take a derived census. Tests: a reversal of 0.9 × band is disregarded, 1.1 × band is ND with both levels named; the realization path uses its own band.

## Fidelity tier (§1.2′; recorded, never scored)

(i) m̂_c − 1 and m̂_c − m_lat; (ii) med against ρ*_sk and the pair skeleton branch at and above m̂_c, and against ρ*(m; η₀) and the pair realization branch at every level, each row with the fidelity band k_R·ŝ(m)·1.2533/√20; (iii) m̂_infl by central differences on the pass-1 grid (interior levels, ties → lower; `inflection at sweep edge` when an endpoint's one-sided slope exceeds every interior one), with its shifts against m_infl and m̂_c; (iv) med(m)/med(m̂_c + Δm) over m < m̂_c − Δm (the reference level = the first pass-1 level ≥ m̂_c + Δm). All from the M5 closure publication; empty when the boundary was not located.

## Sweep records and provenance

`SweepRecord` (object ∈ {skeleton_high, skeleton_low, realization}; role canonical | synthetic; 24 `LevelData` — 20 seeds' (survival, ρ̂) in **canonical-panel order**, or `unevaluable` with its halt key). `sweep_from_results(obj, results_by_level, halts_by_level)` builds a canonical record only from M1 `F8RunResult`s whose specs reconstruct on the **canonical panel at production shape** with matching spec hash and stream key; a level gets either exactly the 20 panel results or a halt key, never both; off-panel, smoke-shape or wrong-object results are refused. `validate_sweep_record` re-derives every canonical run's spec hash, checks identity == content, ρ̂ ∈ [0, 1], and that a skeleton run with positive density cannot be non-surviving. (Tested with one real production-shape level of 20 skeleton-high runs plus 23 halted levels — the record's shape, not a result.)

## Known-answer qualification (§4.11, §5.4) — run in the container, reported for information

Synthetic census: ŝ_X(m) = 0.01 at every level, both objects, built as a real `CalibrationCensus` through M5's provenance path (so the band arithmetic is the production path), role `derived_provisional`. Generator: per seed ρ̂ = branch ± U(−a, a) with **a = 0.45 × the smallest applicable band** — below half the band everywhere, so a spurious adjacent reversal is < band and is disregarded; only an injected feature can trigger a branch. Branches are the §3.1 map's, shifted so the crossing sits at m_c; skeleton survival = 20 above m_c, 0 below. Classes (contract's list): continuous crossing at m_c ∈ {0.8, 1.0, 1.25} → PRODUCED; crossing below the sweep (m_c = 0.1) → `no inactive phase in sweep`; above (m_c = 3.0) → `no active phase in sweep`; steep continuous (one rise of 2·f_J × range between adjacent levels, continuous elsewhere) → ND `continuity unresolved at grid resolution`; hysteretic pair (low crossing = m_c + 2Δm) → `hysteresis`; realization extinct at one level → `realization extinct at …`; one injected reversal of 2 × the combined band → ND `non-monotone at finite sample`. **Cross-trigger rule** implemented: a case with the intended determination but a cause not beginning with the named cause is counted separately and never as a pass. Passage requires every class ≥ 95/100 **and** the declared values (9 classes, 100, 95, master 520261028) — a reduced run is a record, not a qualification.

**Container result on the round-2 generator (900 cases, 813 s): every class 100/100 exact, 0 cross-triggers, `census_is_declared_synthetic = True`; `passed = True`; record identity `58b338861232b286…` (`F8_MP1_KNOWN_ANSWER_CONTAINER_2026-10-29.json`; the round-1 record `c81575638cb15051…` is superseded).** The qualification of record is the one M7 runs on Mike's machine under the apparatus-prerequisite grammar (§5.4: passage required).

## Declarations for L2 (none pre-approved)

- **MP1-1 Synthetic census ŝ = 0.01.** The corpus needs a band to be discriminating against; the contract leaves the synthetic noise law to the build ("declared noise"). 0.01 (band ≈ 0.0119; noise amplitude 0.0054) is of the order the real census is expected to produce; it is a declared constant, in the declaration, and L1 asks L2 whether it should instead be tied to the real census once job 0 exists (which would make the qualification depend on job 0's output — L1 recommends not).
- **MP1-2 Corpus master 520261028**, declared; a reduced or differently seeded run cannot be the record of qualification.
- **MP1-3 Steep-continuous construction**: one adjacent rise of exactly 2·f_J × the branch's total range at the first level above m_c, the remaining rise rescaled to keep the endpoint — the contract's "rising 2·f_J between two adjacent levels".
- **MP1-4 Reference level for ratio (iv)**: the first pass-1 level ≥ m̂_c + Δm (the contract writes med(m̂_c + Δm); m̂_c + Δm is not itself a grid point).
- **MP1-5 T-S1c's domain** is m̂_c…m_max inclusive (the contract: "above m̂_c … every increase ≤ f_J × (med(m_max) − med(m̂_c))" — the range anchors at m̂_c, so the adjacent pair (m̂_c, m̂_c + s) is in the domain).
- **MP1-6 Edge flag for m̂_infl**: set when an endpoint's one-sided slope exceeds the best interior central difference; the interior argmax is still reported (the contract says the flag "gates nothing").

*L1, 2026-10-28; re-issued 2026-10-29 against M5 as placed.*
