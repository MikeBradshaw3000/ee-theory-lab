# L2 — Flight 8 M-P1 Round 1 Review

**Date:** 2026-10-29  
**Register:** Instrument build review under frozen Contract F8 v0.8.4  
**Packet:** `L2_F8_MP1_BUILD_PACKET_2026-10-29.md`, SHA-256 prefix `689eeb8cdb3b80d5`  
**Verdict: DEFECT-WITH-REPAIR**

The requested module passes: **27 passed in 22.66 seconds**, exit 0. M5’s checked quantities agree exactly with the supplied Appendix A on this environment. Nevertheless, direct source review and focused reproductions establish seven repair items. Two permit an incorrect `PRODUCED` determination; others concern observation integrity, an unresolved late-extinction integration conflict, qualification construction and binding, and fidelity reporting.

**M-P1 is not cleared for placement by this review.** The verdict is an instrument-build disposition, with the finite-design claim limits of the frozen contract. It is not a scientific P1 result or an authorization for a canonical job. Mike retains decision authority; canonical-suite passage and the later M7 readiness/authorization obligations remain separate.

## 1. Authority, scope, and identities

The authority is the supplied frozen contract, freeze record, and Appendix A. The build packet states the implementation claims and six declarations to be ruled on; it does not override those governing records. Review covers §4.11 clause by clause, together with §§1.1′, 1.2, 1.2′, 3.4, and 5.4. Relevant M1/M5 dependencies were inspected to resolve integration and provenance questions.

The previously confirmed receipt contains **43 regular files**. The archive SHA-256 is:

`8d4cd1df130f7193206454fc9eeb9c532fcad906a3a6ecf3cff4a155b5cb1c5c`

The following reference keys are used throughout. Paths are relative to `flights/mfa_fidelity/`; identities are the first 16 hexadecimal SHA-256 characters unless the full value is shown.

| Key | File | SHA-256 prefix |
|---|---|---|
| P | `build_records/L2_F8_MP1_BUILD_PACKET_2026-10-29.md` | `689eeb8cdb3b80d5` |
| C | `contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f` |
| F | `contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139` |
| A | `contracts/flight8/APPENDIX_A_OF_RECORD.md` | `94d527624beafa7c` |
| E | `instrument/mfa_instrument/f8/evaluator.py` | `da08e43e320ef991` |
| T | `instrument/tests/test_f8_mp1.py` | `cd6b48e822e71eec` |
| CL | `instrument/mfa_instrument/f8/closure.py` | `9452dd11396350ab` |
| D | `instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8` |
| CFG | `instrument/mfa_instrument/f8/config.py` | `43ea8de23c0d718b` |
| M5R5 | `build_records/L2_F8_M5_ROUND5_REVIEW_RECEIVED.md` | `21d0c74f7a9cbcfc` |

Full identities of the two submitted M-P1 files:

- **E:** `da08e43e320ef991ac724c8b03b1a392d072968370123c800aca969ab52679d5`
- **T:** `cd6b48e822e71eecc7b2440f08eaab28f7b47d4cf76af42d9554c41b7efd9b96`

All 43 extracted files were compared with their archive members after testing and probing: **no submitted file changed**. References to source line numbers below refer to these exact bytes. The reported placement commit and equivalence to the October 28 delivery were not independently verified from a repository checkout; this review is of the supplied bytes.

## 2. Execution and evidence

### 2.1 Requested test module

Working directory: `flights/mfa_fidelity/instrument` in the extracted packet.

```console
python -m pytest tests/test_f8_mp1.py -q
...........................                                              [100%]
27 passed in 22.66s
```

**Exit code: 0.** Python was 3.12.14 on Linux x86_64 with glibc 2.39; NumPy 2.3.5 and SciPy 1.17.0. The environment initially lacked `pytest`, and an intermediate execution reached 26 passing tests before the E1 import check encountered missing `pyarrow`. Both dependencies were supplied in an isolated directory, exposed through `PYTHONPATH`; the complete unmodified module was then rerun with the successful result above. Versions used were pytest 9.2.0 and pyarrow 26.0.0. Those resolved environment failures are not source defects.

SHA-256 of the captured successful test output:

`f7a4cf85b5c41b11a0cea41cb4286b4e485c7b0a8181a338a196d2a2aab049f9`

### 2.2 Appendix A

I called the supplied M5 verifier against the supplied Appendix A. It reported:

| Item | Independently observed result |
|---|---|
| Appendix identity | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` |
| Exact pass-1 level-list match | `True` |
| Δm | `0.120126265992375` |
| m_infl | `1.1764999999999999` |
| m_lat | `1.1414478323100217` |
| Declared binding tolerance | `1e-12` |
| Maximum observed absolute deviation | `0.0` |
| Bit equality of verifier-checked quantities | `True` |

This establishes the correctness of the supplied M5 values against A on this environment. D1 below concerns M-P1's failure to enforce that publication at its input boundary, not a defect in those values. [CL: `verify_against_appendix_a`; A]

### 2.3 Supplemental checks and their limits

I reproduced the principal findings in a separate diagnostic script against the unmodified submitted modules. These checks used constructed sweeps, structurally canonical-role fixtures, and deterministic test substitutions for M1's step function. A record marked `canonical` in such a fixture is **not evidence of M7 issuance or an authorized scientific run**. The forced trajectories exercise M1's real result-summary arithmetic; they are not stochastic lattice experiments.

The qualification-gate checks used controlled evaluator outputs to test the actual counting and final-passage code. They do not constitute a 900-case qualification run. I also executed the actual generator for all nine classes at replicate 0 with an alternative valid census, in addition to the three replicates per class exercised by the supplied test module with its default census.

The packet's claimed **900 cases, every class 100/100, zero cross-triggers, result prefix `c81575638cb15051`** remains L1-reported evidence. I did not rerun that full qualification. The build is held on concrete source findings, and a full run of the unchanged generator would not repair them. [P: known-answer qualification; T: `test_each_known_answer_class_returns_its_named_verdict_and_cause_on_three_replicates`]

## 3. Clause-by-clause disposition

| Governing clause | Disposition of the submitted implementation |
|---|---|
| **§4.11 populations:** three objects, 24 levels, 20 canonical-panel seeds | Object, level-list, panel, spec-hash, stream-key, duplicate-seed and role checks are substantially present. The actual observation is not adequately bound to those specifications: **D3**. M7 issuance and authorization remain M7 responsibilities. [E:157–203, 376–389] |
| **§4.11 per run:** survival, tail density, extinction, apparatus halts | Halts become explicitly unevaluable levels; simultaneous results and a halt are rejected by the builder. Whole-domain apparatus precedence is implemented. **D4** identifies an unresolved conflict for extinction during the tail. [E:157–203, 224–228, 243–249, 287–292; D:133–143] |
| **§4.11 evaluability rule** | The combined band is delegated to M5 and uses the sweep's own object. A reversal equal to the band is disregarded; a strict excess returns ND with both levels. This predicate conforms. [E:207–209, 253–257; CL:674–680] |
| **T-S1′** | All four cases conform: no level reaches 18 → FAIL `no active phase in sweep`; every level reaches 18 → FAIL `no inactive phase in sweep`; a surviving island or interrupted surviving suffix → ND `non-monotone survival`; otherwise the lowest admissible boundary is recorded. The threshold is inclusive at 18. The domain is all 24 levels. [E:224–239, 265–268] |
| **T-S1c** | The domain begins with the pair from m_hat_c to the next level and extends to m_max. Reversal and continuity causes are ND, with no scientific FAIL branch. **D2**: the continuity comparison is improperly disabled for a zero or negative endpoint range. [E:243–262, 271–273] |
| **T-S2** | It correctly reuses the low-sweep boundary procedure and compares the absolute separation with an inclusive Δm. The absolute-value rule governs even though §4.11's explanatory hysteresis example is one-sided. **D1**: the frozen Δm can be bypassed at the evaluator entry point. [E:276–284, 376–396] |
| **T-R1′** | The domain is the entire realization sweep. Apparatus ND comes first; otherwise a nonpositive median gives FAIL `realization extinct at <level>` before shape checks. It uses its own calibration band. The shared continuity code has **D2**. [E:287–293] |
| **§1.2 determination and precedence** | Four PASS results produce `PRODUCED`; otherwise the first valid FAIL in test order produces `NOT PRODUCED`; otherwise the first ND cause is used. A valid failure outranks another test's ND. This conforms. [E:296–302, 391–399] |
| **Missing high-sweep boundary** | T-S1c and T-S2 receive explicit dependent non-evaluability causes; T-R1′ still runs. This is an acceptable operational completion of the dependency. [E:391–398] |
| **§1.1′ claim strength** | The documentation and records limit the determination to the declared finite size, horizon, panel and resolution. T-S1c's PASS detail states consistency with continuity at that resolution. No thermodynamic-limit or universal-geometry claim is introduced. [E:18–21, 271–273, 402–403; C §1.1′] |
| **§1.2′ fidelity separation** | P1's determination is computed from the four test results before fidelity is attached. Fidelity discrepancies and the edge diagnostic do not rescore P1. This separation conforms; reporting completeness requires **D7**. [E:307–353, 398–403] |
| **§4.11 steepest-ascent diagnostic** | Uses actual adjacent grid coordinates for interior central differences, retains the lower interior level on an exact tie, and reports the declared endpoint flag without gating P1. MP1-6 is accepted. [E:321–332] |
| **§3.4 / Appendix A** | The default closure values bind bit-exactly to A in this environment. The own-object evaluability rule is correct. Frozen-threshold enforcement needs **D1**, and fidelity uncertainty reporting needs **D7**. The pre-job precision-ceiling stop remains an M7 integration obligation. |
| **§4.11 / §5.4 known-answer qualification** | Nine classes, default bounded noise, named-cause counting, and the ≥95/100 per-class passage predicate are substantially present. The steep control requires **D5** and the declared census/noise law requires **D6**. [E:409–540] |

## 4. Defects and required repairs

### D1 — The frozen hysteresis bracket and closure publication are not enforced

**Authority:** C §§1.2, 3.4, 4.11; F §3 item 9; A.  
**Source:** E `evaluate_p1`, particularly lines 389–390 and 396–403; existing CL `validate_closure_publication`, lines 300–303.

There are two independent paths through the same unprotected parameter boundary. `evaluate_p1` accepts an unrestricted `delta_m` override, including for canonical-role inputs. It also consumes a supplied `ClosurePublication` without calling the existing M5 replay validator.

I used high and low boundaries at **1.032609** and **1.228261**, with otherwise passing tests. Their separation is `0.19565199999999994`.

| Input | Effective T-S2 bracket | Observed P1 determination |
|---|---:|---|
| Frozen publication; default argument | `0.120126265992375` | `NOT PRODUCED (hysteresis)` |
| Same publication; `delta_m=0.3` | `0.3` | `PRODUCED` |
| Publication's Δm altered to 0.3; original identity retained | `0.3` | `PRODUCED` |
| Altered publication with its content identity recomputed | `0.3` | `PRODUCED` |

These results were reproduced with structurally canonical-role fixtures as well as the underlying constructed observations. In the override case, the fidelity record still reports the frozen Δm and the publication identity is unchanged. In the stale-publication case, the evaluator records that unchanged identity even though it no longer hashes to the supplied content. The existing M5 replay validator rejects the altered publication correctly.

**Repair.** Validate the publication through `CL.validate_closure_publication` before consuming it. The canonical evaluator must take Δm from that validated frozen publication, with no unequal override. If an exploratory synthetic override is retained, isolate that path, mark it as such, and record its effective parameter consistently; it must not masquerade as the frozen evaluation or qualification of record.

**Required discriminating regressions.** Reject an unequal canonical override; reject altered publications with both stale and recomputed hashes; retain the ordinary one-spacing PASS and two-spacing FAIL under frozen Δm; verify the record's operative bracket and publication identity agree.

### D2 — Nonpositive endpoint range disables the continuity requirement

**Authority:** C §4.11 T-S1c and T-R1′; §1.2.  
**Source:** E `_monotone_and_continuity`, lines 243–262, specifically line 260.

The code checks:

```python
if rng > 0.0 and d > F_J * rng:
```

The frozen requirement applies to **every increase**. It does not permit the comparison to disappear when the endpoint difference is zero or negative. Those cases are reachable because small reversals are deliberately disregarded under the evaluability rule.

For a concrete example, let the skeleton survive on all levels from index 8 onward, with active-domain medians 0.300 except index 12 at 0.305. The final median is again 0.300. Let the low sweep have the same boundary and let the realization be a positive constant.

- Positive increase: `0.0050000000000000044`.
- Following reversal: the same magnitude, correctly below the combined band `0.011889847774467086`.
- Endpoint range: `0.0`; allowed positive increase: `0.0`.
- **Actual:** all four tests PASS, P1 `PRODUCED`.
- **Required:** T-S1c ND, `continuity unresolved at grid resolution (1.423913)`; absent another valid failure, P1 `NOT DISTINGUISHED`.

I repeated the construction in the realization sweep and with endpoint range `-0.001`. All four variants incorrectly produced `PRODUCED`.

**Repair.** Apply the criterion to every positive increment, independently of the sign of the total range. A direct implementation is:

```python
if d > 0.0 and d > F_J * rng:
```

The positive-increment condition matters: simply dropping `rng > 0.0` could incorrectly classify zero or negative increments against a negative threshold. Within-band decreases remain governed by the reversal rule.

**Required discriminating regressions.** Zero-range and negative-range interior bumps in both domains; constant-profile and only-decreasing controls; full determination propagation to continuity ND, never a scientific FAIL.

### D3 — Canonical sweep provenance binds the specification but not the recorded observation

**Authority:** C §4.11 populations and per-run definitions; P sweep-record/provenance claim.  
**Source:** E `LevelData`, `sweep_from_results`, and `validate_sweep_record`, lines 125–132 and 157–203.

The builder checks the identity of the requested run, then trusts its supplied summary fields. It does not check the actual trace's production length or recompute survival and the tail mean. The sweep also omits the density-record identities.

A deterministic test substitution made M1 retain the all-active state. Actual M1 `F8RunResult` objects were then produced for the 20 production-shaped specifications at level 2.5; the other levels were marked as halted test fixtures. The real M1 summary code returned traces of length 3001, survival True, and tail mean 1.0.

| Fixture passed to the unmodified builder and validator | Observed acceptance |
|---|---|
| Original M1 result objects | Canonical-role level: survival count 20, median 1.0 |
| Each trace and active-count array truncated to length 1 | Still accepted; the sweep identity is identical to the original |
| Original full traces retained, but cached summaries changed to survival False and mean 0 | Still accepted; survival count 0, median 0; density hashes remain unchanged |

The same density observation can therefore be represented as opposite scientific observations without violating any current check. This finding concerns factual data integrity at M-P1's input boundary. It does not assign M7's authorization duties to M-P1.

**Repair.** Validate the actual M1 result schema and production shape; check count/density consistency; recompute survival and the tail mean using M1's frozen count-grid arithmetic; reject inconsistent cached summaries. Preserve the corresponding density-record hashes alongside the spec hashes. When original run records are supplied for validation, replay the observation summary from those records. Replaying the stochastic dynamics is unnecessary.

**Required discriminating regressions.** Truncated traces; stale survival or density summaries; altered trace content with unchanged observation identity; a complete valid record. The late-extinction case in D4 must remain a valid observation under the resolved definition.

### D4 — Late extinction exposes an unresolved M1-to-M-P1 integration conflict

**Authority:** C §4.11 per-run definitions; the supplied placed M1 implementation.  
**Source:** E lines 198–199 versus D `run`, lines 133–143.

The sweep validator asserts that a skeleton run with positive tail density cannot be non-surviving. That assertion is incompatible with M1's actual tail-average calculation when extinction occurs during the tail.

I forced a deterministic trajectory through M1's real `run` summary code: all cells active through tick 2050, extinct from tick 2051 onward. With the declared tail of ticks 2001–3000, M1 returned:

```text
extinction_tick = 2051
survival = False
rho_tail_mean = 0.05
tail_window_means = (0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
```

M-P1 then rejected that summary with:

```text
EvaluatorDomainError: a skeleton run with positive tail density cannot be non-surviving
```

The test is an arithmetic/integration reproduction, not evidence about the frequency of this event on the lattice. Fifty positive tail ticks followed by 950 zero ticks have a positive average even though the run does not survive the entire tail.

**Contract tension.** Section 4.11 defines ρ_hat as the tail-window mean but also gives an extinct-run shorthand of survival 0 and ρ_hat 0. The latter is unambiguous for extinction before the tail; it needs an explicit interpretation for extinction during the tail. The submitted modules presently disagree. This review does not silently amend the contract or replace the already supplied M1 observable.

**Repair.** Return a declared reconciliation of this case. The minimal interpretation consistent with the existing M1 tail mean is to keep the observed positive pre-extinction contributions, keep subsequent contributions zero, and permit survival False with a positive mean when the trace supports it. If a different aggregate that zeroes an entire extinct run is intended, it must be expressly ruled and applied consistently across the affected instrument; it cannot be introduced as an undocumented M-P1 coercion.

**Required discriminating regressions.** Extinction before the tail, inside an early tail window, inside the final window, and complete survival; verify both summary arithmetic and acceptance into the sweep. An extinct run must remain a valid observation under the resolved definition.

### D5 — The steep-continuous control does not implement MP1-3's declared rise

**Authority:** C §4.11 known-answer construction; P declaration MP1-3.  
**Source:** E `known_answer_case`, lines 482–488, particularly line 486.

Let `R = sk[-1] - sk[c]`. At the first adjacent pair, the code adds both the intended `2*f_J*R` and half the original branch's rise. The actual first rise is:

```text
2*f_J*R + (1 - 2*f_J)*(sk[c+1] - sk[c])
```

Using the supplied closure and levels 1.032609 → 1.130435:

| Quantity | Value |
|---|---:|
| Sampled branch range R | `0.5193009605316091` |
| Declared rise, 2*f_J*R | `0.25965048026580456` |
| Actual noiseless rise | `0.29805623793408126` |
| Actual fraction of range | `0.5739566466985939` |

The control therefore rises about **57.40%** of the range at that pair rather than the declared **50%**. Returning the intended continuity ND does not establish that the declared construction was tested.

**Repair.** Set the first adjacent rise to the declared amount, then rescale only the remaining branch above that pair. For example, with `J = 2*f_J*R`:

```python
steep[c] = sk[c]
for i in range(c + 1, len(sk)):
    steep[i] = sk[c] + J + (R - J) * (sk[i] - sk[c + 1]) / (sk[-1] - sk[c + 1])
```

State the continuous interpolation underlying these samples; a specified continuous piecewise interpolation is sufficient for this control. Preserve the endpoint and the bounded-noise requirement. The declaration's normalized interpretation of `2*f_J` is acceptable; this implementation of it is not.

**Required discriminating regressions.** Check the noiseless first rise and preserved endpoint against the declared arithmetic, then verify the generated case produces continuity ND with its named cause and never a scientific FAIL. A changed generator requires a fresh qualification result for the corrected source.

### D6 — Qualification passage is not bound to the declared synthetic census/noise law

**Authority:** C §§4.11 and 5.4, requiring declared synthetic noise; P MP1-1.  
**Source:** E `synthetic_census`, lines 409–422, and `known_answer_qualification`, lines 520–540.

The final passage predicate enforces the class tuple, replicate count, minimum exact-match count and master. It does not enforce the declared synthetic census. Since the generator derives both its bands and noise amplitude from the supplied census, substituting that census changes the qualification experiment.

I supplied `synthetic_census(0.005)`, a valid census with half the declared spread and a different identity. The actual generator returned the named final outcomes for all nine classes at replicate 0 with that census. Separately, controlled correct outputs were fed through the real qualification counter and final gate:

```text
scope = controlled-output gate probe; not a 900-case qualification
SYNTHETIC_S_HAT = 0.01
supplied s_hat = 0.005000000000000028
census identity differs = True
passed = True
```

The source also permits a structurally canonical-role census to enter the synthetic qualification path. The point is not that an alternative census necessarily performs badly; it is that a different experiment can be labeled passing under the same declared qualification.

**Repair.** Qualification of record must bind the census's role and complete content to the declared synthetic law. Comparing against the deterministic `synthetic_census()` identity is one direct implementation. Alternative-census explorations may remain available, but they must be rejected for qualification or explicitly produce nonqualifying records. Keep this qualification independent of canonical job 0.

**Required discriminating regressions.** A different but structurally valid synthetic census, a canonical-role census, and the correct default census. Exercise the real final-passage path; a separate test merely asserting that the default factory emits 0.01 does not close the acceptance gap.

**Cross-trigger result.** The current production counter itself is correct. In controlled-output tests, 95 named matches plus 5 correct-determination/wrong-cause cases yields passage; 94 plus 6 does not. Wrong-cause cases are counted as failures, while the contract permits up to five failed cases per class. Add this regression to the actual qualification path when making the D6 repair. [E:532–538; T:212–218]

### D7 — Explicit fidelity reporting is incomplete

**Authority:** C §1.2′ and §3.4, specifically fidelity comparisons (ii) and (iv).  
**Source:** E `FidelityTier` and `fidelity_tier`, lines 307–353.

This is a bounded **reporting-conformance** finding. The determination does not use these fields. The observations and much of the information needed for later calculation are present or recoverable; the defect is that the explicit published representation falls short of the contract's stated reporting requirements.

For comparison (ii), each density row currently contains:

```text
(level, observed median, mean-field comparator, pair comparator, density band)
```

The signed residuals are recoverable by subtraction, but §1.2′ requires them to be recorded as signed deviations. The output should explicitly include `observed minus mean-field` and `observed minus pair`, retaining the underlying values and the existing width.

For comparison (iv), the ratio row contains only:

```text
(level, ratio)
```

It does not identify the actual selected denominator level and value or present the numerator/reference uncertainty components. Section 3.4 expressly includes comparison (iv) among those reported with calibration-derived widths. A pointer to the census permits reconstruction of component widths, but does not state how the uncertainty in a ratio is being presented.

**Repair.** Add the two explicit signed density residuals. For the ratio, identify the actual selected reference level and median, the numerator median, and both corresponding calibrated density widths. Return a clear declared convention for presenting those existing uncertainty components. If a propagated ratio band is proposed, state its construction for review; do not invent a confidence-coverage guarantee, covariance assumption, or new statistical test from the present wording. No new location confidence interval for the shifts in (i) or (iii) is required by this finding.

Represent unavailable boundary-dependent diagnostics explicitly: for example, no located boundary, reference outside the sweep, nonpositive denominator, or apparatus-unavailable input. This makes the accepted MP1-4 convention auditable rather than leaving every reason as the same empty tuple.

**Required discriminating regressions.** Positive and negative density residuals retain their signs; the actual denominator grid level is recorded; component widths use the existing fidelity rule; unavailable ratios carry their reason; changed fidelity agreement and diagnostic flags cannot change P1's four-test determination.

## 5. Rulings on MP1-1 through MP1-6

| Declaration | L2 ruling | Reason and conditions |
|---|---|---|
| **MP1-1 — fixed synthetic s_hat = 0.01** | **ACCEPT the declaration; D6 repair required.** | The corpus is an apparatus test under a declared noise law. It should remain independent of the later job-0 output. Approval does not endorse the packet's forecast of the real lattice's variance; that forecast is unnecessary. Enforce the declared synthetic law in qualification of record. |
| **MP1-2 — corpus master 520261028** | **ACCEPT.** | It is declared, checked against the named other masters, and enforced in the final qualification predicate. Reduced runs, changed minima, incomplete/reordered classes, or a different master do not qualify under the present predicate. D6 must complete the separate census binding. |
| **MP1-3 — steep-continuous construction** | **REPAIR REQUIRED; current implementation not accepted.** | Interpreting `2*f_J` as twice the allowed fraction of the sampled range is coherent with the continuity test. The actual generator adds an extra rise and does not implement its own declaration. Repair D5 and rerun the corrected qualification. |
| **MP1-4 — first grid level at or above m_hat_c + Δm** | **ACCEPT as a prospective discrete convention, with D7 reporting repair.** | The nominal reference is off-grid. Rounding upward is deterministic and non-gating. Record the actual selected reference and an explicit unavailability reason when no usable reference exists. The convention must not become an unrecorded substitution for the literal nominal location. |
| **MP1-5 — T-S1c domain includes m_hat_c** | **ACCEPT.** | The range is anchored at the median at m_hat_c; the first adjacent pair above that anchor belongs in the test. The source implements that domain. D2 repairs the predicate within it. |
| **MP1-6 — endpoint-slope flag, interior argmax retained** | **ACCEPT as the declared diagnostic convention.** | Central differences use actual grid coordinates; exact interior ties retain the lower level. Strict endpoint superiority sets a flag while retaining the interior argmax. The flag gates nothing. |

These are rulings on the stated conventions and the identified implementations. Acceptance of a declaration is not clearance of the defective module.

## 6. Known-answer corpus assessment

### 6.1 Inventory and final-outcome grammar

The inventory contains the required nine classes. The supplied unit module executes three actual generated replicates per class and passed. This is narrower than the qualification requirement of 100 per class.

| Class | Named final determination and cause |
|---|---|
| Continuous crossing at 0.8 | `PRODUCED`, no cause |
| Continuous crossing at 1.0 | `PRODUCED`, no cause |
| Continuous crossing at 1.25 | `PRODUCED`, no cause |
| Crossing below sweep | `NOT PRODUCED`, `no inactive phase in sweep` |
| Crossing above sweep | `NOT PRODUCED`, `no active phase in sweep` |
| Steep continuous branch | `NOT DISTINGUISHED`, `continuity unresolved at grid resolution` |
| Hysteretic low/high pair | `NOT PRODUCED`, `hysteresis` |
| Realization extinct at one level | `NOT PRODUCED`, `realization extinct` |
| Injected beyond-band reversal | `NOT DISTINGUISHED`, `non-monotone at finite sample` |

Cause-prefix matching is acceptable for these named cause families because the returned causes append prescribed level details. It must remain tied to the named cause as well as the determination. The present counter does that; the supplied hand-written-row negative test does not demonstrate it. [E:454–540; T:204–218]

### 6.2 Discriminating default noise

For the declared census, the combined adjacent-level band is:

```text
b = 0.011889847774467086
a = 0.45*b = 0.005350431498510189
```

Thus the noise amplitude is below half the band. Two sampled medians' errors can differ by at most `2*a = 0.9*b`; on a nondecreasing baseline, that cannot create a beyond-band reversal. Conversely, an injected reversal of `2*b` remains larger than `b` even under opposing errors of this maximum size. These are design bounds, not empirical confidence claims. [C §4.11; E:425–467]

I also checked a conservative continuity margin for each must-pass class, allowing `2*a` of adjacent-difference error and `2*a` of endpoint-range error:

```text
margin = f_J*(baseline range - 2*a) - largest baseline increase - 2*a
```

| True crossing | Skeleton margin | Realization margin |
|---|---:|---:|
| 0.8 | 0.0460271 | 0.0788737 |
| 1.0 | 0.0396376 | 0.0773024 |
| 1.25 | 0.0264393 | 0.0720825 |

All are positive, supporting the discrimination of these default must-pass controls. This does not remove D5's exact construction mismatch or D6's acceptance of a different noise law.

### 6.3 Nonblocking construction and test-evidence qualifications

The above-sweep crossing control has an additional realization continuity ND at level 2.500000. It occurs even without added noise: the final realization increase is `0.010922414227206953`, exceeding `f_J*range = 0.009650309540608854`. Its final result remains the required `NOT PRODUCED (no active phase in sweep)` because the valid T-S1′ failure outranks the other ND.

I do **not** count this as a separate defect under the explicit final-determination/named-cause cross-trigger rule. It does limit the packet's broader statement that only the injected branch can trigger. The packet should disclose the actual test vector or the control should be made cleaner; it should not claim that every non-target test passes in every class. Dependent ND results when no boundary exists are, of course, expected. [E:478–481; C §1.2 and §4.11]

Two supplied regressions are weaker than their descriptions:

- The purported wrong-cause negative at T:215–217 checks a hand-written row, not the actual qualification counter. The focused controlled-output checks in this review establish the present counter's behavior; the persistent regression should do the same.
- The purported below-boundary steep-rise test at T:107–109 assigns zero to two branch values that are already zero. It does not inject the claimed feature. The source's domain is correct; replace this test with an actual below-boundary rise while keeping survival below 18 there.

These are required improvements to the affected regression coverage when returning the repairs, not additional independent source defects.

## 7. Boundaries retained in the disposition

**Fidelity uses the frozen fidelity rule.** Section 3.4 explicitly assigns skeleton s_hat to the skeleton evaluability domain and realization s_hat to T-R1′ and the fidelity tier. Using `CL.fidelity_band` for both skeleton and realization comparison rows therefore conforms to this frozen wording. The own-object evaluability prohibition must not be silently expanded into a different fidelity convention. [C §3.4; CL:674–685]

**Adverse realization evidence is retained without a skeleton boundary.** The packet says fidelity is empty when the boundary is not located, but the implementation correctly retains boundary-independent realization comparisons and its steepest-ascent diagnostic. Only boundary-dependent fields become unavailable. Correct the packet wording; do not remove those observations. [P: fidelity tier; E:335–353; C §1.2′]

**M7 owns readiness and authorization.** Canonical-role data do not establish Mike-issued authorization by themselves. M7 must enforce issuance, stage identity, prerequisite passage, and the two-part calibration census's precision-ceiling stop before canonical scientific jobs. The missing redundant check of `ceilings_met` inside this evaluator is not treated as an additional M-P1 defect here, because the frozen stop is an orchestration condition. [C §§3.4, 4.10, 7.2–7.4; CL calibration-census role grammar]

**No inference exceeds §1.1′.** A repaired `PRODUCED` result would remain an operational conjunction for the declared finite design: persistence over the horizon, continuity consistency at the sampled resolution, and no hysteresis between the two declared initializations over that horizon. The review makes no lattice-limit claim, validates no closure against lattice observations, and reopens no earlier scientific verdict.

## 8. Return required for clearance

Return changed-source identities, a response mapping each repair to its discriminating regression, and these dispositions:

| Item | Required closure evidence |
|---|---|
| **D1** | Frozen publication replay validation and an enforced canonical Δm; altered publication and unequal-override negatives |
| **D2** | Every positive increase checked even for nonpositive endpoint range; both test domains and full P1 propagation covered |
| **D3** | Observation shape/content and cached-summary consistency enforced; source density identity retained; truncated/stale records rejected |
| **D4** | Explicit late-extinction interpretation reconciled across the supplied interface and confirmed by trace-based regressions |
| **D5** | Correct declared steep rise and continuous construction; generator-level assertions and renewed qualification evidence |
| **D6** | Qualification bound to the declared synthetic census/noise law; alternate valid census cannot qualify; actual wrong-cause counter regression |
| **D7** | Explicit signed density residuals, actual ratio reference, and declared presentation of existing uncertainty components; no fidelity-to-P1 scoring path |

Rerun the updated M-P1 test module. After the generator and qualification-law repairs, produce the complete corrected nine-class, 100-per-class qualification record with its source/declaration/census identities and cross-trigger counts. A reduced run remains a development record. The qualification of record still belongs to the later M7-issued process on Mike's machine under the frozen prerequisite grammar.

**Final disposition: DEFECT-WITH-REPAIR.** The passing 27-test result and exact agreement of M5’s checked quantities with Appendix A are retained as positive evidence. They do not close D1–D7. Placement clearance is withheld pending the repair return; production execution is not authorized by this review.
