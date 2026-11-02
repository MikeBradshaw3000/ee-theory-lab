# L2 → L1 / Mike — Flight 8 M6 build review, round 1

**Date:** 2026-10-30  
**Register:** receipt-first module build review, executed after the verified receipt.  
**Disposition:** **DEFECT-WITH-REPAIR. Four numbered repairs are required before SOUND.**  
**Decision authority:** Mike. L2 reviews; L1 repairs and resubmits.  
**Scope:** the submitted M6 source, tests, and generator declaration v0.2 against the frozen Contract F8 v0.8.4, its freeze record, and Interpretations 001 and 002. Interpretation 002's adoption of E is retained.

**Instruction source:** root `L1_TO_L2_F8_M6_BUILD_PACKET_2026-10-30.md`, SHA-256 `d9b76839719b3ab02d9496d8147bfc7c86de514031c163138b1a3d027608e99f`.  
**Archive:** `f8_m6_build_round1_L2.zip`, SHA-256 `81c29ad1f69f8e10b068d9159a21257c738af258712976e815b29f586fd63717`.  
**Repository pin:** `d474f7f`, as declared in the packet. This review verifies the supplied bytes and their manifest; it does not independently attest a remote Git checkout.

The received M6 test module passes **42 tests**, but its tests do not detect the four findings below. The current-density E process, probability-to-hazard conversion, DIP support construction, reachable-level adapter, and applicable-error/qualification arithmetic are technically acceptable within the stated synthetic-ensemble scope. Build clearance is withheld on the specific repairs in §3.

This is a pre-placement build disposition. The smoke reproduction of a halt is not an adverse production M6 qualification and does not close the stage. No production audit, full pricing job, or canonical scientific job was run. No packet source or test was edited.

## 1. Receipt and source identities

The archive hash matches Mike's declaration. It contains **54 payload files plus `MANIFEST.txt`, 55 files total**, with 13 directory entries excluded. All 54 payload files match their declared **full** SHA-256 digests. There are no missing, extra, or duplicate payload paths. The manifest's own computed SHA-256 is `8f9bbfcdfe1b7a687b19952cf08539fa68120df55a3352b3a0cfcae47dfc5af1`; it is not self-listed. The complete per-file receipt appears in Appendix A and was posted before substantive review.

All 55 received files were rehashed after verification and remained unchanged.

The following source labels are used in the review. Paths other than the root instruction are relative to `flights/mfa_fidelity/`; the full identities are in Appendix A.

| Label | Source | SHA-256, first 16 |
|---|---|---|
| P | Root instruction file named above | `d9b76839719b3ab0` |
| C | `contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f` |
| F | `contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139` |
| I1 | `rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c` |
| I2 | `rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md` | `198d2991dd12168c` |
| L | `build_records/L2_F8_M6_GENERATOR_CONSULTATION_RESPONSE_RECEIVED.md` | `be77f7631b383163` |
| D | `build_records/F8_M6_GENERATOR_DECLARATION_v0_2.md` | `9ea6fa3edd187175` |
| S | `instrument/mfa_instrument/f8/audit.py` | `260f614054819c80` |
| T | `instrument/tests/test_f8_m6.py` | `0eb8d8a75f3b3121` |
| M2 | `instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783f` |
| M3 | `instrument/mfa_instrument/f8/null.py` | `4ee3f239b27f772b` |
| M4 | `instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5` |
| M5 | `instrument/mfa_instrument/f8/closure.py` | `9452dd11396350ab` |

The contract's frozen status follows F; its retained historical draft header is not treated as permission to change its operative clauses.

## 2. Verification performed

### 2.1 Supplied module tests

From the received `flights/mfa_fidelity/instrument/` directory, L2 executed:

```text
python -m pytest tests/test_f8_m6.py -q --durations=10 -p no:cacheprovider
```

**Result: `42 passed in 133.43s (0:02:13)`, exit 0.** Python 3.12.14, NumPy 2.3.5, pytest 9.2.0. Pytest was supplied through an existing dependency directory; plugin autoload and bytecode writing were disabled. No received source change was needed. The captured pytest output has SHA-256 `b7f75130827ebe88c8e33be2ce161a5896f0af346f47814729b674a9f20f25c5`.

The packet's separate report of 180 passed / 5 skipped for other F8 modules remains L1-supplied evidence. L2 did not repeat that wider suite or claim a canonical repository-suite pass in this round.

### 2.2 Adversarial checks

In addition to source and authority review, L2 performed bounded smoke/parameter checks for D1, D3, and D4; a test-date dispatch check with sentries before production sampling for D2; direct DIP support and exact terminal-threshold checks; adapter replay/tamper checks; and numerical CP boundary checks. The critical reproductions are specified below.

The production source remains `PLACEMENT_DATE = None`. D2 used only the hypothetical date already present in T, set temporarily in a separate process and restored. No production sweep was generated and no pricing PRNG was constructed in that probe.

## 3. Required repairs

| ID | Finding | Required correction |
|---|---|---|
| D1 | Temporal preflight checks pass-1 levels but can accept a target illegal at an actual pass-2 insertion. | Certify the entire structurally reachable SUSTAINED-eligible domain before trajectory sampling. |
| D2 | The disclosed placement-date edit turns two refusal tests into full production executions and breaks a third test's assertion. | Make unset-state tests establish that state locally; test established-date dispatch with no-draw sentries or synthetic callbacks. |
| D3 | Odd declared widths realize `w − 1`, contradicting the exact nominal-width law. | Preserve `hi − lo = w` for every integer width and declare the odd-width endpoint convention. |
| D4 | The reentrant onset distribution extends to `m_max − 7s`, beyond the frozen `m_max − 8s` support. | Restore the frozen range in source and declaration, with its identity and a range regression. |

### D1 — Preflight does not cover inserted-level target legality

**Authority:** I2 point 3; D §§4.2 and 4.4; L §§5.2 and 5.5. Illegal parameter candidates must be rejected during parameter preflight, before trajectories are sampled. D's proposed legal domain is `R_FLOOR ≤ r_tar < R_UPPER` for every `(m,t)` in the schedule's domain.

**Source:** S, `archetype_preflight` constructs its temporal `eligible` list only from `F8_LEVELS_MICRO`. S, `generate_run` and `run_sweep` subsequently apply the same target schedule at the router's inserted levels. The target conversion can therefore raise after a draw has passed preflight and after pass-1 trajectories have already been generated.

An ordinary, unmodified smoke sweep reproduces this:

```python
from mfa_instrument.f8 import audit as A

adapter = A.build_adapter("production")
r = A.run_sweep("persistent_nonstationary_high_m", 302, 999, adapter)
```

Here `999` is the supplied smoke master, not an established production master. The adapter's production role identifies its complete scoring surface; building it does not run an audit.

| Quantity | Observed value |
|---|---:|
| Preflight attempts | 1 |
| Onset / declared width, micro-units | 457729 / 14827 |
| `lo` / `hi` in received source | 450316 / 465142 |
| Temporal mode | oscillation |
| Amplitude / period | 0.23318631999240286 / 348 |
| Lowest eligible pass-1 level | 543478 |
| Minimum target at that pass-1 level | 0.07403612220368971 |
| First actual insertion | 456522 |
| Minimum target at that insertion | 0.0657460081957902 |
| Required `R_FLOOR` | 0.06690303415097656 |

The pass-1 labels are three `N`s followed by 21 `S`s, and M4 returns P2R-6 with insertions `456522, 467391, 478261, 489130, 500000, 510869, 521739, 532608`. At `456522`, the ramp fraction is approximately `0.4185889653`; seed index 2 has uniform `0.3700922167` and is assigned SUSTAINED. Its target conversion fails. The actual returned result is:

```text
final_verdict = HALTED
generator_halt = None
evaluability_halt = apparatus:target density outside the legal domain [0.066903, 0.846547)
```

The target remains above the necessary spontaneous-floor bound `π₁`; it violates M6's deliberately stronger proposed floor. That distinction does not excuse the failure: the source accepts the candidate at preflight and later refuses its ordinary use. This is not an unfavorable stochastic M2 classification. The apparatus halt is recorded correctly, but correct halt accounting does not make the generator preflight complete. [S: `target_to_coefficient`, `archetype_preflight`, `generate_run`, `run_sweep`]

**Minimum repair.** Check all structurally reachable SUSTAINED-eligible levels, including pass-2 keys, or implement a proved sufficient bound covering that domain. The check must depend only on parameters and the frozen reachable surface, not on observed labels, trajectories, or the route a sampled sweep happened to take. Reject and redraw the complete parameter candidate under the existing 64-attempt rule. Do not clip the target, repair a trajectory, or redraw a sweep after classification.

Conform D's pass-1-only wording. Preserve the accepted first-attempt parameters above as a regression: they must be refused before any trajectory call. Also verify that a returned accepted candidate has legal schedules on the applicable reachable domain and that the repaired smoke path completes normally. The original 42-test suite examines pass-1 legality and a small smoke set; it does not test this accepted insertion case.

### D2 — Placement changes the refusal tests into production work

**Authority:** P §4.5 and D §9 disclose a one-line placement change from `PLACEMENT_DATE = None` to the placement date. C §§5.3 and 7.1 and I2 point 8 preserve the later freeze/master/audit sequence. This build review is not a production run authorization.

Three tests depend on the current live source sentinel:

| Test | Dependency on the live unset date | Behavior after the disclosed placement edit |
|---|---|---|
| `test_masters_are_derived_from_the_placement_date_and_refused_while_unset` | Begins by asserting `A.PLACEMENT_DATE is None`. | The assertion fails. |
| `test_smoke_audit_record_validates_and_production_paths_are_refused` | Expects `A.run_audit("design", adapter)` to raise. | The default 500-sweep-per-class design audit enters generation under its established master. |
| `test_price_is_the_s_min_event_with_exact_cp_and_the_full_run_is_gated` | Expects `A.run_pricing(adapter)` to raise. | The default 10,000-replicate pricing job enters generation under its established master. |

The last two calls use a complete production adapter and no master override. Once the date is set, their expected refusal has disappeared by design. With normal pytest continuation, the first failed assertion does not prevent the later tests from attempting those jobs. [T: the three named tests; S: `run_audit`, `run_pricing`, `production_masters`]

**Safe reproduction.** In a separate process, L2 built the adapter, set the test-only date `20261101` already used in T, and installed a custom exception sentry at `A.run_sweep`, before any parameter or trajectory generation. Calling `A.run_audit("design", adapter)` reached that sentry. A second sentry replaced `A.np.random.default_rng`; calling `A.run_pricing(adapter)` reached it before constructing the first pricing generator. All patched objects and the date were restored.

```text
date_assertion_passes_after_placement = False
audit_entry_reached = True
pricing_rng_entry_reached = True
production_sweeps_generated = 0
pricing_prngs_created = 0
```

**Minimum repair.** Every unset-state refusal test must set `PLACEMENT_DATE` to `None` with its own `monkeypatch` fixture. Its premise must not depend on the source still being pre-placement. Cover the established-date branch using sentries or synthetic callbacks that verify identity and dispatch without generating production observations. The test module must remain safe whether the received source literal is unset or established.

The eventual one-literal placement change still requires its disclosed identity/changed-source verification. This finding calls for a local test repair; it does not ask L1 to invent a new runtime authorization system or to select a placement date now.

### D3 — Odd nominal widths violate the stated exact width identity

**Authority:** C §6.1 and D §2 identify the ramp extent as `E = w·(u_(18) − u_(3))`, with the uniform spacing distributed as Beta(15,6). The submitted endpoint convention does not preserve the declared integer `w`.

S, `SweepParams.lo` and `SweepParams.hi`, use:

```python
lo = onset_micro - width_micro // 2
hi = onset_micro + width_micro // 2
```

Thus the actual support width is `hi − lo = 2·floor(w/2)`. For odd `w`, it is `w − 1`; `w = 1` collapses to a zero-width step. S, `regime_at`, divides by this actual endpoint difference. Its latent extent law therefore uses that effective width, rather than the asserted nominal one.

A parameter-only reproduction from an ordinary accepted draw is:

```python
p, attempts = A.draw_params("gentle_onset", 999, 0, 7)
```

| Quantity | Observed value |
|---|---:|
| Attempts | 1 |
| Onset | 1485901 |
| Declared width | 192863 |
| `lo` / `hi` | 1389470 / 1582332 |
| Actual width | 192862 |

**Magnitude and scope.** This is a narrow exact-conformance defect. It does not demonstrate a reversed guard-gap margin or a measured error-rate failure. The reduction is at most one micro-unit, and the frozen lower width endpoints are even. The effective widths stay within the class ranges. Nevertheless, the implementation and declaration currently assert different exact laws.

**Preferred minimum repair.** Preserve the integer width:

```python
lo = onset_micro - width_micro // 2
hi = lo + width_micro
```

Declare the resulting endpoint convention: for an odd width, the midpoint is half a micro-unit above the integer onset parameter. Preserve the zero-width branch, and test odd and even widths, including `1`, `108401`, and `689957`, with `hi − lo == width_micro` as a conformance assertion. Update the declaration and all affected identities. Merely retaining the old formula while continuing to claim the nominal-width equality is not a repair. [S: `SweepParams`, `regime_at`; D §2; C §6.1]

### D4 — Reentrant onset support is wider than frozen §6.4 permits

**Authority:** C §6.4's shared `two_resolved_crossings`, `reentrant` row gives onset support `[m_min + s, m_max − 8s]`, then distinguishes the two-crossing offsets from the reentrant return offset. Neither I2 nor F supplies a separate wider reentrant onset range.

S's `GENERATOR_DECLARATION` and `_draw_once`, and D §2's reentrant row, instead use `[m_min + s, m_max − 7s]`. D does not identify that as a change to the frozen sampling support. The pre-build draft's repetition of the same range is not an intervening ruling.

| Bound | Micro-units |
|---|---:|
| Frozen lower bound | 347826 |
| Frozen upper bound, `m_max − 8s` | 1717392 |
| Implemented upper bound, `m_max − 7s` | 1815218 |
| Added interval | 97826 |

An accepted parameter draw demonstrates the difference without generating a trajectory:

```python
p, attempts = A.draw_params("reentrant", 999, 7, 24)
```

It passes preflight on attempt 1 with onset `1742590`, return offset `511578`, and return location `2254168`. The onset exceeds the frozen upper bound by `25198` micro-units.

The expanded support still preserves the three-region geometric coverage: even its greatest onset plus greatest return offset leaves a final null region. **That geometric sufficiency does not authorize a different frozen sampling distribution.** This finding is about contract conformance, not a claim that the wider range loses a region. [C §6.4; F item 22; S: `GENERATOR_DECLARATION`, `_draw_once`; D §2]

**Minimum repair.** Restore `m_max − 8s` for `reentrant` in the declaration tuple and parameter draw, conform D, regenerate the affected identity, and add a regression against the frozen onset support. Retaining the wider range would require an identified ruling that is absent from this packet; restoring the frozen range is the direct repair.

## 4. Dispositions on the three specifically requested executable rules

### 4.1 M6-4: `r_floor = ρ*(m_min; η₀)`

**Technically acceptable as an explicitly proposed design restriction; implementation subject to D1; ratification remains Mike's.** It is stricter than I2's necessary `π₁` lower bound and has a clear reference: the lowest unmodulated target in the declared sweep. The computed value is `0.06690303415097656`, above `π₁ = 0.052282320137314486`.

This is a target constraint, not a guarantee that every stochastic realization will be SUSTAINED. The E process remains unrestricted within its declared law, retains its stationary-null start, and is not resampled to obtain an intended M2 status. The supplied design observations at the floor are not promoted to an audit qualification. [D §§4.2–4.5; I2 points 2–4; S: `R_FLOOR`, `target_to_coefficient`]

### 4.2 Attenuation: strict first decrease, non-increase thereafter

**Technically acceptable as the declared finite-pass-1-grid morphology check.** The code examines the resulting target profile, including the rising `ρ*(m)`, rather than merely checking that its multiplier decreases. It requires two above-onset pass-1 observations, a strict decrease from the first to the second, and no subsequent increase on that grid. This addresses the received consultation's counterexample.

The `max(R_FLOOR, …)` is an explicit part of the attenuation schedule and permits a declared plateau. It does not inspect or repair sampled trajectories. This finite-grid check must not be described as proving monotonic decrease at every intermediate real-valued `m`, or as guaranteeing a particular stochastic run status. [D §§4.3–4.5; L §5.5; S: `target_schedule`, `archetype_preflight`]

### 4.3 M6-3: nonterminal DIP and terminal floor

**Technically acceptable.** With `index_t = 14121` and `WINDOW = 100`, the source uses `k_floor = 14121 // 100 + 1 = 142`. A nonterminal zero window makes `S_min = 0`, while the terminal support gives:

```text
terminal count sum ≥ 14200
S_term ≥ 14200 / 250000 = 0.0568
theta_T = 14121 / 250000 = 0.056484
```

Hence `S_term > theta_T` strictly, and M2 returns UNRESOLVED by support. This is a declared construction confined to DIP; no SUSTAINED trace is repaired after classification. [I2 point 5; S: `dip_terminal_floor`, `gen_dip_run`; M2: `run_status`]

L2 exercised the actual `gen_dip_run` with an all-zero count-process substitute and a forced last nonterminal window `w = 8`. The function itself produced terminal counts of 142 and UNRESOLVED. L2 also checked the exact terminal threshold on count-grid traces with a separate nonterminal zero window:

| Terminal sum | `S_term` | M2 status |
|---|---:|---|
| 14121, exactly the threshold | 0.056484 | NO_SUSTAINED |
| 14122, one count above | 0.056488 | UNRESOLVED |
| 14200, the DIP's minimum support | 0.056800 | UNRESOLVED |

The supplied all-empty test manually constructs its floored segment. The direct-function case above is useful regression coverage for L1 to retain; no source defect was found in the DIP implementation.

## 5. Other findings and declaration dispositions

### 5.1 Accepted mechanics

**E and NULL sources.** The sequential two-binomial count process implements I2's current-density closure with the stationary-null start. The supplied tests establish unmodulated bit equality with M5 at four levels and the conditional-expectation identity. Zero feedback gives the aggregate Markov null. The 200-run terminal-window DKW check is smoke evidence, not a replacement M3 qualification. The source does not claim spatial-lattice or M1 stream identity. [I2 points 1–2; S: `_count_process`; T: the source-identity and conditional-expectation tests]

**Conversion and temporal dynamics.** The target is converted to activation probability, then hazard, then feedback coefficient. The process evolves sequentially through that coefficient; it is not reset to the target or described as having the target as its exact time-varying mean. D1 concerns the completeness of legality preflight, not this conversion formula. [S: `target_to_coefficient`, `target_schedule`, `_count_process`; I2 point 3]

**Adapter.** The 276 canonical router witnesses produce 338 distinct insertion keys; with 24 pass-1 keys the adapter has 362. M4's confident-order-violation check makes P2R-4 dead on this surface, so there is no omitted live two-interval family. The adapter rebuilds the surface and M3 payload and checks content, not merely a production label. Independent tamper checks that recomputed a modified object's self-hash still failed replay when a threshold, key set, payload identity, or slice role was altered. Missing keys are checked before run sampling and halt the sweep. [S: `reachable_pass2_levels`, `validate_adapter`, `is_production_adapter`; M4: `route`, `dead_rows`]

**Streams and scoring.** Regime uniforms are shared across levels, while count trajectories use distinct level/seed streams and parameters use a separate role/attempt stream. Pass-1 and inserted observations are merged before the verdict of record is evaluated. No classifier-outcome-conditioned resampling was found. [S: `draw_params`, `run_stream`, `regime_uniforms`, `run_sweep`]

**Completion and qualification.** Scientific-intent classes count final NOT_DISTINGUISHED; ND-intent classes count final LOCATED or NOT_PRODUCED. Exact verdict-and-cause agreement remains descriptive. Completion requires 500 attempted, 500 scored, zero apparatus and generator halts, and the CP cap. The validators recompute the error count, bound, completion, record identities, and mechanical design/held-out join. The current unset date prevents a production-qualified result. [C §5.1; I2 point 10; S: `score_class`, `validate_class_score`, `validate_audit_record`, `qualify_audit`]

As a numerical boundary check, the one-sided 95% CP upper is `0.09842821540078545` at 38 errors in 500 and `0.10064973078409462` at 39. Thus 38 clears the 0.10 cap and 39 does not. At zero of 10,000 it is `0.0002995283597757026`, agreeing with the closed form `1 − 0.05^(1/10000)` to floating precision. These are deterministic arithmetic checks, not audit outcomes.

**Pricing and job 0.** Pricing uses complete NULL trajectories and the required `S_min > theta_P` event with count, denominator, nominal rate, construction bound, and exact upper uncertainty bound. It is descriptive and does not enter qualification. The surrogate comparison uses the same 1,000-tick tail observable, sample SD with `ddof = 1`, and declared comparison streams at pass-1 levels. The lattice side remains pending separately authorized job 0; no early calibration or insertion-level comparison is inferred. [I2 point 9; D §§7–8; S: `run_pricing`, `surrogate_level_stats`]

### 5.2 Parameter conditioning and evidence wording

The packet openly discloses preflight conditioning, and the source checks parameters rather than trajectories. L2 does not find concealed outcome conditioning. The accepted joint distribution is the nominal proposal law conditioned on **all** preflight checks, including geometric checks in classes beyond rows 2–3. For the temporal class, the retained drift/oscillation mix need not remain 50/50 because the two proposals have different acceptance conditions. D's final wording should distinguish proposal marginals from the accepted joint distribution and retain bounded-exhaustion accounting. This clarifies the already disclosed method; it does not call for a new sampling algorithm. [P §4.3; D §§2, 4–5; S: `_draw_once`, `draw_params`]

D §5 also says a test asserts batched-versus-sequential series identity. The submitted stream test establishes repeatability and independence from intervening call order; no separate batched runner is supplied, as P §4.1 acknowledges. Conform that evidence sentence to what was actually tested. This is an evidence-description correction, not a fifth source defect or a demand to build a batching runner.

### 5.3 M6-1 through M6-12

“Technically acceptable” below is L2's disposition on the specification/implementation named; it does not ratify a PROPOSED value or grant module placement while D1–D4 remain open.

| Declaration | L2 disposition |
|---|---|
| M6-1 — E source | Technically acceptable; conforms to the adopted I2 law. |
| M6-2 — NULL source | Technically acceptable; zero-feedback aggregate Markov law and declared draw order. |
| M6-3 — DIP | Technically acceptable; strict terminal support established in §4.3. |
| M6-4 — modulation floor | Technically acceptable as a proposal; D1 must enforce it throughout the reachable domain. |
| M6-5 — modulation ranges | Technically coherent proposal; D1 and explicit conditional-distribution wording apply. |
| M6-6 — redraw budget | Technically acceptable: 64 parameter attempts, exhaustion retained as a generator halt. |
| M6-7 — fixed two-crossing pair | Technically coherent as the disclosed `(4s, 7s)` reading; Mike's named confirmation remains required as the packet states. This does not approve D4's separate reentrant onset change. |
| M6-8 — reachable adapter | Technically acceptable: complete 24 + 338 surface and replay binding. D1 is a generator-domain issue, not a missing adapter key. |
| M6-9 — price | Correct event and exact upper uncertainty bound; the proposed 10,000 count remains for ratification. D2 must make the full-price refusal test safe after placement. |
| M6-10 — job-0 comparison | Technically acceptable method and surrogate side; proposed 200 replicates and later lattice values retain their declared status. |
| M6-11 — master rule | Coherent disclosed proposal and effective current sentinel; D2 and eventual changed-source verification apply. |
| M6-12 — wide upper bound | The integer endpoint 1003571 implements `floor(1.6·w_U)`; D3 must preserve the drawn width itself. |

## 6. Required return and scope of clearance

L1 should return repaired M6 source and tests, the conformed generator declaration, all affected identities, and new module-test evidence addressing D1–D4. The discriminating cases above provide bounded regression fixtures; no production ensemble is needed to establish any repair.

The repair boundary is local: complete the parameter domain check; make tests independent of the live placement sentinel; preserve integer widths; and restore the frozen reentrant onset support. No change to placed M1–M5, M-P1, the frozen contract, the adopted E law, or the applicable-error cap is requested by these findings.

After SOUND on the repaired bytes, placement and master establishment retain their declared order, the disclosed date-literal change is identity-checked, and production qualification remains a future step. M7 must still carry the interpretation and declaration identities, master derivation, adapter identity measured on the canonical platform, and the already recorded M3 `price_familywise` docstring obligation. The later job-0 comparison remains separate.

**Final disposition: DEFECT-WITH-REPAIR — D1, D2, D3, D4. No M6 placement clearance or production run authorization is issued by this review.**

## Appendix A. Complete full-digest receipt

All payload comparisons below use the full 64 hexadecimal characters. Paths are repository-relative except the root instruction and `MANIFEST.txt`. The manifest's own digest is recorded without a self-comparison.

| File | Computed full SHA-256 | Comparison with MANIFEST.txt |
|---|---|---|
| `L1_TO_L2_F8_M6_BUILD_PACKET_2026-10-30.md` | `d9b76839719b3ab02d9496d8147bfc7c86de514031c163138b1a3d027608e99f` | MATCH |
| `MANIFEST.txt` | `8f9bbfcdfe1b7a687b19952cf08539fa68120df55a3352b3a0cfcae47dfc5af1` | Computed; not self-listed |
| `flights/mfa_fidelity/build_records/F8_M6_GENERATOR_DECLARATION_v0_1.md` | `eb9e71b9363c5af33bff0ecc17852622768b39fcc7126e3b4826231a712f7994` | MATCH |
| `flights/mfa_fidelity/build_records/F8_M6_GENERATOR_DECLARATION_v0_2.md` | `9ea6fa3edd18717593e090a39ddb57b2eaa75c76f20fbdc300515056b139c9d8` | MATCH |
| `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M6_GENERATOR_CONSULTATION_2026-10-30.md` | `7f7acc6bf6881381d27b98abfe5a2014105f50d277a375845b3abf32abdf2241` | MATCH |
| `flights/mfa_fidelity/build_records/L2_F8_M6_GENERATOR_CONSULTATION_RESPONSE_RECEIVED.md` | `be77f7631b383163192fbcfaee9c032a83a21730a365c627dcf593fe161e5dd6` | MATCH |
| `flights/mfa_fidelity/build_records/f8_m6_module_container_2026-10-30.txt` | `c17d3bc7250906d4fa3f498fe73cf3ecfe313c521ecf3daedb8e5b16082f17a1` | MATCH |
| `flights/mfa_fidelity/contracts/flight8/APPENDIX_A_OF_RECORD.md` | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` | MATCH |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | MATCH |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/bridge.py` | `0f9d9292c14fa69139e9e0867a881f9736a6ddbb4991a6d7c63b59d180cf395e` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/config.py` | `f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/dynamics.py` | `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/e1/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4408190adf4864efa27138f3194e1276ad920f1167f2999c3` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494a6eaa64719f3c5240e2971be70ce4d12bafe663ad607ddd3` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/e1/config.py` | `934634593eb82914b1f69361ebd896151082937261b01113c1a72a751225bf22` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78dabef69edd0e5ffa17b861f9696deccff92d85e186777f56fa` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/e1/projection.py` | `29dba5002462062495393da35c7216ccb779d13ffba91ccd24da45481591c3a2` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/e1/runner.py` | `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345d5c43724fc6b9a002d67d2d495f10d32268910ad5f033bbf` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `260f614054819c80b2242d220c6ec468202d557263c97c4c63d48906daf73753` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `43ea8de23c0d718b246936c7ff6f18e4f8e5243f77ddb240d896e5d00bdf0e07` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `4ee3f239b27f772b64a3f31a6dfff73112c40386904e3bda50e826766cef0121` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_a.py` | `a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b1.py` | `5794f2b74ae66f17affbbf03cbc9fb417bbf3e0255da52a9b9b019ec0350fa99` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/b2.py` | `c7e27ad8e73d74df81ff2390ba0a6f8e91e30349e1b9c8c66f802985fa1f0a83` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/comparators.py` | `5f20b981abed25c598d575acab01b116d40efbc5a4e5586b73bce1692d51f90d` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/qualification.py` | `fdb6209c7723e8c237dfdadc387cc6d65b82631dc20120a86b9c97631b919c43` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/reference.py` | `085715260e03e6e5c5c4468e3570c73efc3784f0dc1f1d36ba662de0ff30964d` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_b/stub.py` | `9a42239d08409fde2e25b2b8c3fd5f0f7cd3e624933ce65d86d633c5ad32a9f6` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/gates/gate_r0.py` | `4b4c7e5a1c06dfac362e3a2c29a795249b4f4a783c2c5de7fcf18a7fa46a638f` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/init.py` | `43e6f829962ca3e91ce6d5ec379b033bf44a060a47bc52681c3eb7fc21f49f18` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/rng.py` | `fcde29c6975bd0107398aff8dffd6c21aa5d325fbc1e70fd7501daba84bf8d62` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/schema_contract.py` | `e6cb5e8464452cb5e7107383b581a8d886005787eb088f1dd6c9d8a8824128fc` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/telemetry.py` | `5073a6fd64bc37d6b9e214805834b91cce5c07ee6c9d9b5489a2d01bc7684725` | MATCH |
| `flights/mfa_fidelity/instrument/mfa_instrument/verify.py` | `9944489ebc2eace4c0627f1ee3194879d594aaee158e120dd7200f3c34a3d66d` | MATCH |
| `flights/mfa_fidelity/instrument/tests/test_f8_m1.py` | `23d4260f5a2d996b56e748aada1e7ed5d5b6d35e57bc41be9fdc53b34b04bff0` | MATCH |
| `flights/mfa_fidelity/instrument/tests/test_f8_m2_m3.py` | `d0d26e75280dffef269e05f95e391b1db775a0f4712a5b3eac2f31ff50336460` | MATCH |
| `flights/mfa_fidelity/instrument/tests/test_f8_m4.py` | `8b8976b2c3602e0cc3932676cc6a091c69569af515bc183c374208578afa6d12` | MATCH |
| `flights/mfa_fidelity/instrument/tests/test_f8_m5.py` | `27cb5c965242ad2bde9aa61c5403eb97473190b67b1d232a2d801c5bd2097b41` | MATCH |
| `flights/mfa_fidelity/instrument/tests/test_f8_m6.py` | `0eb8d8a75f3b31217d06389b98fca2f49eb2ca9082b6cd5c7897136affb0a529` | MATCH |
| `flights/mfa_fidelity/instrument/tests/test_f8_mp1.py` | `f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d` | MATCH |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86` | MATCH |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md` | `198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034` | MATCH |

## Appendix B. Independent verification evidence identities

These are L2's newly generated verification artifacts, distinct from the received manifest. Their substantive results and reproductions are included in this review.

| Evidence | Full SHA-256 |
|---|---|
| `m6_pytest_output.txt` | `b7f75130827ebe88c8e33be2ce161a5896f0af346f47814729b674a9f20f25c5` |
| `m6_pytest_record.json` | `4a476650ae66141d2f157b715e49cfa24c8019b7dc63c2b9a410072e053c8908` |
| `independent_checks.py` | `61a81df226accc5d0a324334d04da7eb88339f8b92062dc7d6c26c6035f9bfd9` |
| `independent_checks.json` | `febc14ce1fdf54d96746d09905a51344b42254bc59c670677f5661be23152312` |
| `dip_threshold_boundary.json` | `615cbae6a6e7f06e0523f7af02229bb3e634010c49a2e0f539f5eb608e421ed8` |

### Captured supplied-test output

```text
..........................................                               [100%]
============================= slowest 10 durations =============================
81.89s call     tests/test_f8_m6.py::test_smoke_audit_record_validates_and_production_paths_are_refused
41.70s setup    tests/test_f8_m6.py::test_one_sweep_per_class_is_well_formed_and_scored_on_the_final_level_set
3.85s call     tests/test_f8_m6.py::test_missing_adapter_key_is_an_apparatus_halt_not_a_derivation
2.43s call     tests/test_f8_m6.py::test_adapter_covers_the_reachable_surface_and_binds_the_one_payload
1.86s call     tests/test_f8_m6.py::test_null_source_is_e_at_zero_feedback_and_matches_m3_law_on_the_terminal_window
0.74s call     tests/test_f8_m6.py::test_price_is_the_s_min_event_with_exact_cp_and_the_full_run_is_gated
0.40s setup    tests/test_f8_m6.py::test_dip_is_unresolved_by_support_and_e1_terminal_dip_would_not_be
0.15s call     tests/test_f8_m6.py::test_dip_is_unresolved_by_support_and_e1_terminal_dip_would_not_be
0.06s call     tests/test_f8_m6.py::test_surrogate_level_stats_is_interpretation_001_tail_density
0.02s call     tests/test_f8_m6.py::test_run_streams_are_per_level_and_seed_and_order_independent
42 passed in 133.43s (0:02:13)
```
