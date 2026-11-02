# L1 → L2 — Flight 8 M6 build packet (round 1): the morphology audit under F8 Interpretation 002 (reading E)

**Date:** 2026-10-30. **Register:** module build review (receipt-first), the normal register of the M1–M5 and M-P1 reviews. Not a run authorization; no master has been drawn.
**Repository pin:** `ee-theory-lab` HEAD `d474f7f` (`RECORD F8 Interpretation 002 …`). Every placed file in this zip is a byte copy from a fresh clone at that commit; the three NEW objects are not yet in the repository.
**Decision authority:** Mike. L2 reviews; L1 repairs; placement follows L2's SOUND.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count (**54 payload files + MANIFEST.txt = 55**, directories excluded), and every file's digest against `MANIFEST.txt` (full digests). Then "execute".

## 1. What is in the packet

NEW (for review):
- `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` — M6. Generator (NULL / SUSTAINED-E / DIP count processes; modulation target→probability→hazard→coefficient; preflight; redraw budget; streams), the reachable-level threshold adapter, the sweep, scoring/records/qualification (E1 M6's grammar carried), the §4.3 price, the surrogate side of the job-0 comparison.
- `flights/mfa_fidelity/instrument/tests/test_f8_m6.py` — 42 tests.
- `flights/mfa_fidelity/build_records/F8_M6_GENERATOR_DECLARATION_v0_2.md` — the generator declaration conformed to the build (v0.1, the pre-build draft, retained beside it). Twelve declarations M6-1…12 for Mike's ratification with the governance record.
- `flights/mfa_fidelity/build_records/f8_m6_module_container_2026-10-30.txt` — the container run: 42 passed (200.9 s); the other F8 modules on the same working copy 180 passed, 5 skipped.

PLACED (context, byte copies at `d474f7f`): the contract v0.8.4, freeze record, Appendix A; Interpretations 001 and 002; your consultation disposition (as `_RECEIVED`) and L1's consultation packet; the whole `mfa_instrument` package (e1 and f8, nothing modified) and the F8 test modules M1–M5, M-P1.

## 2. How to run

From `flights/mfa_fidelity/instrument/`: `python -m pytest tests/test_f8_m6.py -q` (numpy only; no pyarrow needed for this module; ≈ 3.5 min, of which the smoke audit — two ensembles × 12 classes × 1 sweep under smoke masters — is ≈ 2 min). The M3 law is computed once (≈ 1 s) on first use.

## 3. The build against your §7 prospective DEFECT table

| L2 §7 | Where it is designed out | Evidence |
|---|---|---|
| D1 generator identity | Module docstring and `GENERATOR_DECLARATION`: SUSTAINED = reading E, named as the finite-N current-density closure, never the lattice, never A; start Bin(N, π₁). Interpretation 002's identity is a literal in every record (`INTERPRETATION_002_SHA256`). | `test_unmodulated_sustained_source_is_bit_equal_to_m5_finite_n_counts` (4 levels); `test_conditional_expectation_is_the_contract_map` |
| D2 transition/modulation law | `target_to_coefficient`: a_tar = q·r/(1−r) → H = −ln(1−a_tar)/Δt → c = (H−η₀)/r; domain [r_floor, 1/(1+q)) **refused**, no clipping; Markov evolution retained (`_count_process` sequential, two conditional binomials per tick); g = 0 reduction = `gen_null_run`. | `test_coefficient_at_the_fixed_point_is_lambda_bar_and_conversion_is_two_steps`; `test_illegal_targets_are_refused_never_clipped`; `test_legal_domain_boundaries`; `test_null_source_is_e_at_zero_feedback_and_matches_m3_law_on_the_terminal_window` (DKW at n = 200 on the designated window) |
| D3 generator truth and sampling | `archetype_preflight` checks placement AND the resulting morphology (drift minimum; oscillation legality at every eligible level; attenuation's **resulting** profile strictly decreasing first→second and non-increasing after, floor by declared max()); `draw_params` redraws from a dedicated stream, records attempts, halts at 64; no path is ever redrawn on its status. | `test_preflight_geometry_and_morphology`; `test_preflight_never_consults_a_trajectory`; `test_draw_params_is_deterministic_records_attempts_and_halts_on_exhaustion`; `test_generator_halt_is_recorded_in_completion` |
| D4 DIP | `gen_dip_run`: nonterminal zero window w ∈ [0, 8]; terminal floor k_floor = ⌊idx_T/100⌋+1 = 142 per tick → S_min = 0 ≤ θ_P, S_term ≥ 14,200/250,000 > θ_T by support; E1's terminal dip not carried. | `test_dip_is_unresolved_by_support_and_e1_terminal_dip_would_not_be` (20 streams; the all-empty equality case; E1's construction shown NO_SUSTAINED) |
| D5 insertion-level support | `ThresholdAdapter`: 24 + 338 keys from `route()` over M4's 276 witnesses post-fallback, bound to the one M3 payload; production role only by rebuild; `adapter.get` before any draw; missing key → `apparatus:` halt, class incomplete; M1/M3 untouched. | `test_adapter_covers_the_reachable_surface_and_binds_the_one_payload`; `test_adapter_json_tamper_is_caught`; `test_missing_adapter_key_is_an_apparatus_halt_not_a_derivation` |
| D6 traces and streams | 3,001-entry int64 counts, `rho = K/N` on the exact grid (M2's `recover_counts` verifies); streams per (level_micro, seed index), regime uniforms shared across levels, parameters on a dedicated stream in one draw order; no trajectory reuse; explicit synthetic provenance; no M1 identity claimed. | `test_rho_record_is_on_the_count_grid_and_m2_accepts_it`; `test_run_streams_are_per_level_and_seed_and_order_independent` |
| D7 pricing and governance | `run_pricing` scores S_min > θ_P (never θ_T), exact CP upper, construction bound reported; the job-0 comparison is a separate object (`surrogate_level_stats`, values pending job 0); masters derive from `PLACEMENT_DATE` (None until the placement commit) and every production path refuses while unset; audit grammar carried unchanged (500 / cap 0.10 / CP 0.95 / mechanical join / adverse close). | `test_price_is_the_s_min_event_with_exact_cp_and_the_full_run_is_gated`; `test_masters_are_derived_from_the_placement_date_and_refused_while_unset`; `test_smoke_audit_record_validates_and_production_paths_are_refused`; `test_clopper_pearson_known_values` |

## 4. Disclosures L1 wants in front of you

1. **Runtime.** 6.6 ms per E run; 5.3–5.7 s per eight-insertion sweep on the container; a 500-sweep ensemble ≈ 7–8 h serial, the pair ≈ 15 h. E1's audit was 1.3 h. Identity is per-run stream, so a runner may batch across seeds without changing any record; L1 has not built that runner and the figure is a measurement, not a promise for Mike's machine.
2. **Payload identity is platform-sensitive.** `ThresholdAdapter.payload_identity` is M3's `NullThresholds.payload_identity()`, which hashes float64 certificate fields computed through `exp`; the container value is `597e39bd5093e51d…`. `is_production_adapter` therefore checks the **integer** indices (14,341 / 14,121) and replay, not that string; the string is recorded as what the canonical machine saw at placement (the M5 Appendix A discipline). The declaration §6 says so.
3. **Preflight conditions the parameter distribution of rows 2–3.** Oscillation draws with a large amplitude and a low onset are refused (the floor), as are attenuation draws whose resulting profile does not decrease; the realized onset/amplitude distribution of those classes is therefore the declared ranges **conditioned on preflight**, recorded per sweep in `preflight_attempts`. L1 reads this as parameter-level conditioning of the kind your §5.5 asks for, distinct from the outcome conditioning your §5.4 forbids; if you see it as a hidden narrowing of the class, say so and L1 will state the conditioned distribution explicitly in the declaration.
4. **The "[4, 7] spacings" of §5.2** is implemented as the fixed pair (4s, 7s) = (391,304, 684,782) (M6-7), marked for Mike's confirmation.
5. **`PLACEMENT_DATE` sentinel.** The placement commit will set one source line (`PLACEMENT_DATE = None` → the date); the masters then follow the declared rule. This is a disclosed post-review source change of exactly one literal, of the same kind as E1's `PRODUCTION_CACHE_*` literals; L2 may prefer the date be fixed before review, in which case Mike names it and L1 sets it now.
6. **`null.py` docstring `price_familywise`** — defect of record (Interpretation 002 pt 9a), not repaired in this packet (M3 untouched); on M7's obligation list.
7. **Descriptive only:** one sweep per class under smoke master 999 returned every intended verdict and cause (§11 of the declaration). It enters no pass.

## 5. What L1 asks of L2

A disposition in the usual form (SOUND / DEFECT-WITH-REPAIR, numbered), on the M6 source and tests against the contract, Interpretation 002 and the declaration v0.2 — in particular on the three places where L1 turned your consultation into executable rules: the floor r_floor = ρ*(m_min; η₀) (M6-4), the attenuation morphology rule (strict first-to-second decrease, non-increasing after), and the DIP terminal floor (M6-3). Nothing here asks you to re-decide the ruling.
