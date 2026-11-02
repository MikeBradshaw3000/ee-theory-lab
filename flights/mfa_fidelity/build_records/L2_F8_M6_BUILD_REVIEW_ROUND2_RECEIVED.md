# L2 → L1 / Mike — Flight 8 M6 build review, round 2

**Date:** 2026-10-30  
**Register:** receipt-first module build review; execution followed the complete verified receipt.  
**Disposition:** **SOUND on the submitted round-2 bytes.**  
**Round-1 findings:** **D1, D2, D3, and D4 CLOSED. Both §5.2 clarifications CLOSED.**  
**Decision authority:** Mike. This is L2's technical build clearance; ratification, placement, canonical-suite verification, master establishment, and production qualification retain their recorded order.

**Instruction source:** root `L1_TO_L2_F8_M6_ROUND2_RESPONSE_2026-10-30.md`, SHA-256 `a23859653af2f48cc2005ad0a2776f7aae439c26f2accd7ec4cce13ac8ab8388`.  
**Archive:** `f8_m6_build_round2_L2.zip`, SHA-256 `75420485c801560d4b419002642957a4cbaef2dc909297fe33c2b161d2670b1d`.  
**Repository pin:** `d474f7f`, as declared. The supplied bytes and their continuity with round 1 are verified; no independent remote Git attestation is made.  
**Round-1 review answered:** `L2_F8_M6_BUILD_REVIEW_ROUND1_RECEIVED.md`, SHA-256 `ea6622808407cfeac85d035206cfef0278c5c4181975a65520b12d751838675b`, byte-identical to the review L2 issued.

The full received M6 module passes **55 tests in 150.88 seconds**, exit 0. The original accepted-then-halted smoke case is now rejected at parameter preflight on its first candidate; its second candidate is accepted and the actual sweep completes as LOCATED with no halt. The placement-state tests, integer width law, and frozen reentrant onset support are repaired. No new blocking defect was found in the changed source.

The two evidence notes in §6 clarify what particular records establish. They do not reopen D1–D4 or withhold this SOUND disposition. No received source or test was edited, and no production audit, full production price, or canonical scientific job was run.

## 1. Receipt, identities, and scope of change

### 1.1 Receipt

The archive hash matches Mike's declaration. The archive contains **58 payload files plus `MANIFEST.txt`, 59 files total**; 13 directory entries are excluded. All 58 payload files match their declared full SHA-256 digests, with no missing, extra, or duplicate payload paths. The manifest's own computed digest is `ae66fac2fad33ee79b26278aea084e7887505f2aa028c08993c6453afa3061c7`; it is not self-listed. The full table is in Appendix A and was posted before substantive review.

All 59 received files were rehashed after verification and remained unchanged.

### 1.2 Objects covered by this clearance

Paths below are relative to `flights/mfa_fidelity/` except the root response.

| Object | Full SHA-256 |
|---|---|
| `instrument/mfa_instrument/f8/audit.py` | `246d01a957994f3c55566011f895518dfb9a81066c57d378a5109267be65bf13` |
| `instrument/tests/test_f8_m6.py` | `808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca` |
| `build_records/F8_M6_GENERATOR_DECLARATION_v0_3.md` | `c73980585fc238209453ebadb4707d961e41d77b7970435e8ce4113298868e47` |
| `build_records/f8_m6_module_container_round2_2026-10-30.txt` | `cb7c8203b3a402cb16c462e985bafd20bb9cb0ee680bd9ff90e5588dc6ea45ff` |

The runtime declaration identities also recompute exactly:

| Declaration tuple | SHA-256 | Change |
|---|---|---|
| Audit declaration | `58693fafa1717b01aecac0dc0c568528faff44c402f6f2d2b0fc8a0d2636d89a` | Unchanged |
| Generator declaration | `dd0ff5ec51ff921b5316ffef103ecaa3783d71cba278458613c46767e7db5f57` | Replaces round 1's `e24a9effa336b62b…`; incorporates the corrected reentrant support, width endpoints, and reachable temporal-legality domain |

The generator declaration tuple and the Markdown declaration are distinct identified objects; the table preserves both identities.

### 1.3 Changed-source boundary

Among paths shared with round 1, only M6 `audit.py`, `test_f8_m6.py`, and the manifest differ. **51 same-path files are byte-identical**, including placed modules and retained context. The round-1 root instruction was relocated to `build_records/` without a byte change. The other new payload objects are the round-2 response, declaration v0.3, received round-1 review, and round-2 test record.

The submitted source still has `PLACEMENT_DATE = None`. The count-process law, target-to-probability-to-hazard conversion, DIP construction, adapter replay logic, stream hierarchy, final-level scoring, completion arithmetic, qualification join, and price event are unchanged by this repair round. The new memoized surface and fixed-point values are deterministic functions of the unchanged M4/M5 inputs and consume no RNG state. [Round-2 source diff; `audit.py`: `reachable_surface_keys`, `_rho_re_at`; complete receipt in Appendix A.]

The operative authorities remain Contract F8 v0.8.4 (`e87277a2d11e948f…`), its freeze record (`16869692a043b139…`), Interpretation 001 (`6bf7304fd3ee287c…`), Interpretation 002 (`198d2991dd12168c…`), and the received round-1 disposition. This is a bounded review of the repairs and their consequences.

## 2. Execution evidence and its limits

### 2.1 Full received test module

From the received `flights/mfa_fidelity/instrument/` directory, L2 executed:

```text
python -m pytest tests/test_f8_m6.py -q --durations=10 -p no:cacheprovider
```

**Result: `55 passed in 150.88s (0:02:30)`, exit 0.** Environment: Python 3.12.14, NumPy 2.3.5, pytest 9.2.0. Plugin autoload and bytecode writing were disabled. The packet source remained unchanged. Captured output SHA-256: `ce2c76eb1239f4a7a852a39038295c85eb70b566be4e78b6b5cf62172c385616`.

This run includes the original tests, the D1 counterexample and repaired smoke sweep, the established-date dispatch test, odd-width regressions, reentrant-range checks, and the direct-function DIP floor/threshold checks. Appendix B includes the captured output.

### 2.2 Established-date check

L2 also initialized `A.PLACEMENT_DATE = 20261101` in memory, before pytest, and selected:

```text
-k "masters_are_derived or established_date_dispatches or price_is_the_s_min_event or dip_direct_function"
```

**Result: 4 passed, 51 deselected in 4.75 seconds, exit 0.** The in-memory date remained `20261101` after the tests, confirming that their local monkeypatch fixtures restored the established state they inherited. The source file hash was unchanged.

The supplied container record separately reports full-module runs of **55 passed in 213.70 seconds** with the unset sentinel and **55 passed in 211.17 seconds** with a temporary established-date copy, followed by restoration of the sentinel. Those two full runs are L1-supplied evidence. L2 independently ran all 55 on the received bytes and the four selected tests under an initially established in-memory date; it does not claim a second independent full-module run in that alternate state.

### 2.3 Bounded independent checks

Independent checks reconstructed all 276 router witnesses and the 362-key surface, replayed the original D1 parameter candidate and actual smoke sweep, compared closed-form schedule bounds with full target series, verified the original D3 and D4 reproductions, and exercised a forced-last-nonterminal DIP case. No production ensemble or production pricing observation was generated. The arithmetic and source identities supporting the findings are recorded below and in Appendix B.

The wider canonical repository suite was not rerun by L2 in this round. Its ordinary placement gate remains in force.

## 3. D1–D4 dispositions

| Finding | Round-2 disposition | Principal evidence |
|---|---|---|
| D1 — inserted-level target legality | **CLOSED** | Original candidate refused before trajectories; replacement accepted on attempt 2; actual smoke sweep now completes without a halt. |
| D2 — placement-dependent refusal tests | **CLOSED** | All three refusal tests establish `None` locally; established-date dispatch is intercepted before parameter/trajectory generation; targeted alternate-state tests pass. |
| D3 — odd-width identity | **CLOSED** | `hi = lo + width_micro`; original draw now realizes 192863 exactly; zero, one, even, and odd widths checked. |
| D4 — reentrant onset support | **CLOSED** | Source and declaration use `[347826, 1717392]`; original out-of-support draw now has onset 1649606. |

### 3.1 D1 — legality covers the complete reachable domain

**Authority:** round-1 D1; Interpretation 002 point 3; declaration v0.3 §§4.2–4.4.  
**Repaired source:** `reachable_surface_keys`, `_rho_re_at`, `_schedule_extremes`, and `archetype_preflight`.

The repaired preflight checks every key in the union of the **24 pass-1 levels and 338 reachable post-fallback insertion levels**, restricted to keys at or above the candidate's `lo`. Independent reconstruction through all 276 canonical M4 witnesses gives the same 362 keys as the adapter and the new memoized function. This covers every level at which a normal sweep can invoke a modulated SUSTAINED source.

The schedule bounds are sufficient for the submitted parameter families:

| Schedule | Bound used | Why it covers the sampled schedule |
|---|---|---|
| Drift | Values at `t = 0` and `t = TICKS − 1`, ordered by minimum/maximum | The schedule is linear in time, including for negative drift. |
| Oscillation | `ρ*(m)·(1 − A)` and `ρ*(m)·(1 + A)` | The sine factor lies between −1 and +1. The envelope may reject a candidate whose discrete sampling misses the mathematical extremum; this conservatism is explicitly declared. |
| Attenuation | The declared constant target | The target is constant in time, so both bounds equal the actual value. |

The domain check precedes trajectory generation. It uses candidate parameters and the frozen surface; it does not depend on regime uniforms, sampled labels, the actual route, or a classifier outcome. The existing 64-attempt parameter-redraw procedure is retained. [Source functions above; declaration v0.3 §4.4 and generator tuple `temporal_legality_domain`.]

The original first-attempt candidate reproduces exactly under:

```python
g = np.random.default_rng(np.random.SeedSequence([999, 2, 302, 2, 0]))
p0 = A._draw_once("persistent_nonstationary_high_m", g)
A.archetype_preflight(p0)
```

Observed result:

```text
(False, "target leaves the legal domain at reachable key 456522 (m=0.456522)")
```

Its onset remains `457729`, width `14827`, oscillation amplitude `0.23318631999240286`, and period `348`. The candidate that caused round 1's downstream halt is now refused at the required stage.

`draw_params("persistent_nonstationary_high_m", 999, 2, 302)` accepts **attempt 2**. A sentry at `_count_process` recorded **zero trajectory calls** during the draw. Its replacement candidate has onset `2344442`, width `42967`, and drift `0.08579009990390771`; all actual scheduled values at its 20 eligible reachable keys satisfy the domain bounds.

The actual smoke sweep then returns:

```text
master = 999
class = persistent_nonstationary_high_m
sweep_index = 302
preflight_attempts = 2
final_verdict = LOCATED
final_rule = 4d
final_cause = None
evaluability_halt = None
generator_halt = None
```

Independent checks also compared ten schedule shapes at every reachable key—**3,620 schedule/key pairs, each with a 3,000-entry actual series**—covering both drift signs, odd/even oscillation periods, amplitude endpoints, and attenuation endpoints. All containment assertions passed without a numerical tolerance; drift and attenuation extrema agreed exactly. A separate 2,172-case check confirmed the same containment and equality of memoized fixed points with direct M5 evaluations. These checks substantiate the changed envelope calculation; they are not new audit performance estimates.

**D1 is CLOSED.** The former failure is prevented through parameter rejection, with no trajectory repair or outcome-conditioned resampling.

### 3.2 D2 — tests remain safe after the placement literal changes

**Authority:** round-1 D2; round-2 response §1; declaration v0.3 §§9 and 12.  
**Repaired tests:** the masters/refusal test, smoke-audit-record/refusal test, pricing/refusal test, and the new established-date dispatch test.

Each of the three formerly state-dependent tests now begins by explicitly setting `PLACEMENT_DATE = None` through its own `monkeypatch`. Their expected refusals therefore follow from a locally established test premise. They no longer rely on the live source still being pre-placement.

The new established-date test sets the hypothetical date `20261101` and intercepts the generation paths:

- The `run_sweep` sentry observes design dispatch under `620261101` and held-out dispatch under `720261101`, with the expected production adapter, then raises before parameter or trajectory generation.
- The `gen_null_run` sentry receives the pricing stream derived from `SeedSequence([820261101, 0, 0])` and raises before creating a NULL observation. Explicit master overrides remain refused, and the audit's slice-adapter path remains refused.

The test's precise execution limit matters: its pricing sentry draws one raw test integer to compare with a matching expected-stream integer. It generates **no audit parameters, count trajectories, or pricing observations**. The claimed safety is absence of production observations, rather than absence of every PRNG operation. The supplied date is hypothetical and the source remains unset. [Test `test_established_date_dispatches_production_paths_under_the_derived_masters_without_a_draw`.]

Source inspection, the 55-test run, and the targeted initially-established-date check support the repair. The expensive smoke-record test is also explicitly local-state on inspection and passes in the full received-module run. The source content is unchanged by these tests.

**D2 is CLOSED.** The eventual placement-date literal still requires the previously disclosed changed-source verification; the tests no longer turn that edit into an unintended full audit or price.

### 3.3 D3 — nominal and effective widths now agree

**Authority:** round-1 D3; Contract §6.1; declaration v0.3 §2 and M6-13.  
**Repaired source:** `SweepParams.hi`, with the existing `regime_at` denominator.

The endpoints now satisfy:

```python
lo = onset_micro - width_micro // 2
hi = lo + width_micro
```

Therefore `hi − lo == width_micro` for every nonnegative integer width. The existing ramp uses that endpoint difference, restoring the nominal-width identity in the contract's latent extent law. The zero-width case remains a step. For an odd width, the midpoint is `onset + 1/2 micro-unit`; that convention is now explicit in the declaration and generator tuple.

The original reproduction `A.draw_params("gentle_onset", 999, 0, 7)` gives:

| Quantity | Round 1 | Round 2 |
|---|---:|---:|
| Onset | 1485901 | 1485901 |
| Declared width | 192863 | 192863 |
| `lo` | 1389470 | 1389470 |
| `hi` | 1582332 | 1582333 |
| Actual width | 192862 | **192863** |

Checks cover `0`, `1`, `2`, `108401`, `192863`, `689957`, and `1003571`. The width-one regression distinguishes the former collapse: the onset endpoint is NULL for uniform zero, and the endpoint one micro-unit higher is SUSTAINED for uniform 0.99. This is a discriminating repair test, not merely a restatement of an unrelated property.

**D3 is CLOSED.**

### 3.4 D4 — reentrant onset support conforms to the frozen range

**Authority:** round-1 D4; Contract §6.4's shared two-crossing/reentrant row; declaration v0.3 §2 and M6-14.  
**Repaired source:** `GENERATOR_DECLARATION["onset_range_reentrant"]` and `_draw_once`.

The source uses one branch for the two-crossing and reentrant onset range:

```text
[m_min + s, m_max − 8s] = [347826, 1717392]
```

Declaration v0.3 explicitly withdraws the wider `−7s` support as L1's departure from the contract. It restores the original support without proposing a new interpretation.

The original reproduction `A.draw_params("reentrant", 999, 7, 24)` now has onset **1649606**, return offset **511578**, and preflight `(True, "ok")` on attempt 1. The onset lies within the frozen upper bound **1717392**. The new regression checks 120 draws against the support and confirms a final NULL region in the selected region-coverage checks. The source's shared range branch supplies the general support guarantee; the sampled checks exercise it.

**D4 is CLOSED.** Both the sampling support and the region-coverage requirement are preserved.

## 4. Round-1 §5.2 clarifications

### 4.1 Accepted parameter distributions — CLOSED

Declaration v0.3 §4.4 now says that a class's accepted distribution is its proposal law conditioned on **all** preflight checks, including geometry, legality, and morphology. The ranges are described as proposal marginals. The accepted temporal mixture need not be 50/50, because drift and oscillation candidates face different acceptance conditions. The same qualification is carried in M6-5.

This accurately describes the source's complete-candidate redraw procedure and the new conservative oscillation envelope. The declaration preserves the 64-attempt budget, per-sweep attempt accounting, and generator-halt treatment. All checks depend on parameters and the frozen surface, with no use of sampled trajectories or classifier outcomes. The clarification is sufficient.

### 4.2 Stream-test evidence — CLOSED

Declaration v0.3 §5 withdraws the batched-versus-sequential identity claim. It now states what the supplied stream test establishes: repeated calls for the same level/seed stream produce the same series independently of intervening calls. It also states that no batched runner is supplied. This matches the actual evidence and retains batching as possible future execution machinery, rather than an already tested implementation.

## 5. Standing acceptances and declaration status

Round-1 §4's technical acceptances of **M6-3's DIP support, M6-4's proposed modulation floor, and the finite-grid attenuation rule remain standing**. D1 now implements the proposed floor throughout the structurally reachable scoring domain. The floor remains a target restriction, and the finite-grid attenuation check retains its explicitly limited scope. Individual stochastic classifications remain audit observations.

Round-1 §5.1's accepted mechanics also stand: the E and zero-feedback NULL laws, target conversion, complete adapter/replay binding, per-level/per-seed trajectory streams, shared regime uniforms, final-level verdict, applicable-error partition, 500/500/zero-halt completion rule, CP cap, mechanical design/held-out qualification join, correct `S_min > theta_P` price event, and the separate job-0 comparison method.

The newly listed declaration rows have these dispositions:

| Row | Technical disposition |
|---|---|
| M6-13 — width endpoints | Accepted as the explicit implementation of exact integer width; odd-width midpoint convention is recorded. |
| M6-14 — reentrant onset | Accepted as restoration of the frozen §6.4 support, rather than a new sampling-range choice. |

M6-1 through M6-12 retain the technical dispositions recorded in round 1, with the repair conditions now discharged. Proposed values still require Mike's ratification under the existing process. In particular, the disclosed fixed `(4s, 7s)` interpretation remains for Mike's named confirmation as the packet states. This SOUND review does not itself mark the draft declaration frozen or establish a placement date.

## 6. Nonblocking evidence clarifications

### 6.1 Direct DIP test: what it actually exercises

The new `test_dip_direct_function_with_an_empty_process_and_the_last_nonterminal_window` genuinely calls `gen_dip_run` with the count process replaced by zeros. It verifies that the function imposes the terminal floor, yielding sum **14200** and UNRESOLVED. It also checks terminal sum **14121** at `theta_T` gives NO_SUSTAINED and **14122** gives UNRESOLVED.

Its name/docstring overstates one aspect: it does not explicitly force `w = 8`. With the substituted count process consuming no RNG draws, `default_rng(0).integers(0, 9)` returns **7**. An already all-zero nonterminal fixture also cannot reveal which window was selected. The submitted test should therefore be cited as direct-function floor and threshold-boundary evidence; it does not establish an explicit forced-last-window case by itself.

L2 independently supplied a selector stub returning **8** and observed:

```text
selector call = integers(0, 9)
selected window = 8
terminal sum = 14200
S_min = 0.0
S_term = 0.0568
status = UNRESOLVED
```

Thus the last-nonterminal case also passes. The relevant DIP source is unchanged from its round-1 acceptance. This is an evidence-description correction, not a new source defect or a clearance condition. The exact threshold comparison is at 14121 and one count above it; 14121 is not one count below the 14200 floor total.

### 6.2 Recorded timings

Declaration v0.3 §12 gives prose durations of 210.3 and 207.4 seconds, while the identified captured container record gives **213.70 and 211.17 seconds**. Both report 55 passes in each state. Use the captured record's timings when citing that record. L2's independently captured received-source run is **150.88 seconds** in its own environment. This timing discrepancy does not change the test counts or any finding's disposition.

## 7. Clearance boundary and next step

**M6 round 2 is SOUND on the source, test, and declaration identities specified in §1.2. There is no remaining repair hold from D1–D4 or round-1 §5.2.**

This permits the ordinary build-placement process to proceed, retaining Mike's decision authority, the declared ratification and canonical-suite requirements, and the eventual changed-source verification of the date literal. The corrected generator declaration identity must be carried into the adapter/governance records. The adapter's payload identity remains measured on the canonical platform, as disclosed; this review adds no cross-platform byte-identity claim.

After placement, master establishment and the design/held-out qualification process retain Contract §§5.3 and 7.1 and Interpretation 002's sequence. SOUND establishes build conformance on the reviewed bytes. Applicable-error performance remains to be established by the future frozen synthetic ensembles. The separately authorized job-0 lattice comparison and M7's recorded `price_familywise` docstring obligation remain in their existing places.

No production audit, full production price, or canonical scientific job was run or authorized by this review. All received files remain unchanged.

**Final disposition: SOUND. D1–D4 and both §5.2 clarifications CLOSED.**

## Appendix A. Complete full-digest receipt

All payload comparisons use the full 64 hexadecimal characters. Paths are repository-relative except the root response and manifest.

| File | Computed full SHA-256 | Comparison with MANIFEST.txt |
|---|---|---|
| `L1_TO_L2_F8_M6_ROUND2_RESPONSE_2026-10-30.md` | `a23859653af2f48cc2005ad0a2776f7aae439c26f2accd7ec4cce13ac8ab8388` | MATCH |
| `MANIFEST.txt` | `ae66fac2fad33ee79b26278aea084e7887505f2aa028c08993c6453afa3061c7` | Computed; not self-listed |
| `flights/mfa_fidelity/build_records/F8_M6_GENERATOR_DECLARATION_v0_1.md` | `eb9e71b9363c5af33bff0ecc17852622768b39fcc7126e3b4826231a712f7994` | MATCH |
| `flights/mfa_fidelity/build_records/F8_M6_GENERATOR_DECLARATION_v0_2.md` | `9ea6fa3edd18717593e090a39ddb57b2eaa75c76f20fbdc300515056b139c9d8` | MATCH |
| `flights/mfa_fidelity/build_records/F8_M6_GENERATOR_DECLARATION_v0_3.md` | `c73980585fc238209453ebadb4707d961e41d77b7970435e8ce4113298868e47` | MATCH |
| `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M6_BUILD_PACKET_2026-10-30.md` | `d9b76839719b3ab02d9496d8147bfc7c86de514031c163138b1a3d027608e99f` | MATCH |
| `flights/mfa_fidelity/build_records/L1_TO_L2_F8_M6_GENERATOR_CONSULTATION_2026-10-30.md` | `7f7acc6bf6881381d27b98abfe5a2014105f50d277a375845b3abf32abdf2241` | MATCH |
| `flights/mfa_fidelity/build_records/L2_F8_M6_BUILD_REVIEW_ROUND1_RECEIVED.md` | `ea6622808407cfeac85d035206cfef0278c5c4181975a65520b12d751838675b` | MATCH |
| `flights/mfa_fidelity/build_records/L2_F8_M6_GENERATOR_CONSULTATION_RESPONSE_RECEIVED.md` | `be77f7631b383163192fbcfaee9c032a83a21730a365c627dcf593fe161e5dd6` | MATCH |
| `flights/mfa_fidelity/build_records/f8_m6_module_container_2026-10-30.txt` | `c17d3bc7250906d4fa3f498fe73cf3ecfe313c521ecf3daedb8e5b16082f17a1` | MATCH |
| `flights/mfa_fidelity/build_records/f8_m6_module_container_round2_2026-10-30.txt` | `cb7c8203b3a402cb16c462e985bafd20bb9cb0ee680bd9ff90e5588dc6ea45ff` | MATCH |
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
| `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `246d01a957994f3c55566011f895518dfb9a81066c57d378a5109267be65bf13` | MATCH |
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
| `flights/mfa_fidelity/instrument/tests/test_f8_m6.py` | `808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca` | MATCH |
| `flights/mfa_fidelity/instrument/tests/test_f8_mp1.py` | `f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d` | MATCH |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86` | MATCH |
| `flights/mfa_fidelity/rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md` | `198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034` | MATCH |

## Appendix B. Verification evidence

The following are L2-generated verification artifacts, separate from the received manifest. Their substantive findings and reproduction details are included above. The records/test JSON is an execution summary, not raw pytest stdout.

| Evidence | Full SHA-256 |
|---|---|
| `m6_pytest_output.txt` | `ce2c76eb1239f4a7a852a39038295c85eb70b566be4e78b6b5cf62172c385616` |
| `m6_pytest_record.json` | `686f0a402c1d2ce1cfa78d1f32ff84d7b56c31a9b26567f86137a880e06f28a3` |
| `generator_probes/round2_generator_closure_probe.py` | `94875d868109f15ca111694e8087ea5b76f1b67b65e4a09240910d89cd543bb4` |
| `generator_probes/round2_generator_closure_probe.json` | `55ff9522d4ba61df5fd434dcc0f74478237ee922a17b0ed91f738d58485538b4` |
| `adapter_probes/verify_d1_repair.py` | `fb2c9e2404ce6336614ed7be0b9bd114ccd219a493ba9d2c0184c4bd5d590960` |
| `adapter_probes/verify_d1_repair_result.json` | `11d3c49553e70e7234e8bce88f0e38087fbb9cc1fa7d4e42881d52d5f694795a` |
| `records_probes/d2_targeted_tests_and_dip_execution_summary.json` | `d6e5c26b2dd61ef7739b629122dc2f2549cb5d6b05059d730fd66e8e23621216` |

### Full received-module pytest output

```text
.......................................................                  [100%]
============================= slowest 10 durations =============================
95.26s call     tests/test_f8_m6.py::test_smoke_audit_record_validates_and_production_paths_are_refused
39.86s setup    tests/test_f8_m6.py::test_one_sweep_per_class_is_well_formed_and_scored_on_the_final_level_set
4.27s call     tests/test_f8_m6.py::test_d1_target_legality_is_certified_over_the_reachable_surface_before_any_trajectory
2.96s call     tests/test_f8_m6.py::test_missing_adapter_key_is_an_apparatus_halt_not_a_derivation
2.74s call     tests/test_f8_m6.py::test_established_date_dispatches_production_paths_under_the_derived_masters_without_a_draw
2.10s call     tests/test_f8_m6.py::test_adapter_covers_the_reachable_surface_and_binds_the_one_payload
1.67s call     tests/test_f8_m6.py::test_null_source_is_e_at_zero_feedback_and_matches_m3_law_on_the_terminal_window
0.84s call     tests/test_f8_m6.py::test_price_is_the_s_min_event_with_exact_cp_and_the_full_run_is_gated
0.39s setup    tests/test_f8_m6.py::test_dip_is_unresolved_by_support_and_e1_terminal_dip_would_not_be
0.17s call     tests/test_f8_m6.py::test_preflight_geometry_and_morphology
55 passed in 150.88s (0:02:30)
```
