# L2 → L1 / Mike — Flight 8 M6 generator consultation disposition

**Date:** 2026-10-30  
**Register:** bounded pre-build consultation on the meaning of Contract F8 v0.8.4 §5.1. This is not an M6 module review or a run authorization.  
**Disposition:** **Do not adopt A as stated. Recommend reading E below: the finite-N, current-density closure already embodied in M5.** A remains a possible, narrower synthetic generator only if Mike explicitly chooses its additional approximations.  
**Decision authority:** Mike. L1 records the resulting identified interpretation and completes the generator declaration before building and routing the source for review.

**Instruction source:** `L1_TO_L2_F8_M6_GENERATOR_CONSULTATION_2026-10-30.md`, SHA-256 prefix `7f7acc6bf6881381`.  
**Archive:** `f8_m6_consultation_L2.zip`, SHA-256 `89611df9e1ac0cdce4c50d146eec2d341ab7ba97a8ce04c628e6e7883577ac02`.  
**Packet's stated repository pin:** `ee-theory-lab` HEAD `5dd1afa`. The supplied bytes were verified against the manifest; this consultation does not independently attest a remote Git checkout.  
**Frozen contract:** SHA-256 `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182`. Its status comes from the supplied ratification/freeze record, despite the historical draft wording retained in the contract header.

## 1. Answers to the four questions

| Question | L2 disposition |
|---|---|
| 1. Is A sound as the interpretation, or which reading instead? | **A is a coherent equilibrium-calibrated Markov surrogate, but it is not the dynamic §3.1 closure described in its justification. Recommend E:** replace local density by the current global density, retain the hazard transition and stationary-null start, and simulate the aggregate count. The mathematical construction is already present in `f8/closure.py::finite_n_counts`. Mike must explicitly authorize this M6-only closure substitution; existing M5 placement does not itself settle §5.1. |
| 2. Is the proposed disclosure/pricing adequate? | **The descriptive approach is appropriate; the proposed description is incomplete.** Compare matching 1,000-tick tail statistics, include mean discrepancies, identify the dependence and initialization differences, and keep the later job-0 comparison separate from the §4.3 null price required at qualification. No new pass criterion is imposed here. |
| 3. Does modulation on excess satisfy the generator constraint? | **Acceptable as a parameterization, insufficient as the complete rule.** Declare its transition law, legal domain, timing and actual morphology; preserve regime assignment; distinguish target margins from stochastic run-status guarantees. The §4.11 half-band constraint belongs to M-P1 and is not imported into M6. |
| 4. What would be a build-review DEFECT? | The preventable failures are enumerated in §7: misidentifying the generator law, incorrect probability/hazard inversion, inadequate modulation preflight or outcome-conditioned sampling, a verbatim E1 DIP, incomplete pass-2 threshold support, wrong trace/RNG provenance, and incorrect pricing or freeze order. These are prospective review criteria, not findings against unsubmitted M6 code. |

The principal reason to prefer E is substantive: **the packet's cost argument motivates avoiding a full lattice, but does not require freezing density feedback at its equilibrium.** A current-density count process avoids the lattice operations too, and preserves more of the rule that §5.1 names. [R1 §2; R2 §§2.3–2.5, 3.1, 5.1; R9, `finite_n_counts`]

## 2. What A does correctly, and what its justification omits

Let

$$
q=1-e^{-\mu\Delta t},\qquad
r_*=\rho^*(m;\eta_0),\qquad
a_*=1-e^{-(\eta_0+g\bar\lambda r_*)\Delta t}.
$$

The fixed-point equation gives

$$
(1-r_*)a_*=q r_*,
\qquad
\frac{a_*}{a_*+q}=r_*.
$$

Therefore A's independent chains, initialized with active probability \(r_*\), really do have stationary density \(r_*\). That part of the proposal is sound. Setting the feedback coefficient to zero and using the corresponding stationary initialization recovers the §2.9 Markov null in distribution. [R2 §§2.4, 2.9, 3.1; R9, `g_map`, `fixed_point`]

Three distinctions prevent the stronger identification in the packet:

1. **The lattice uses the current local density.** Its activation depends on \(d_i(t)\), the active fraction of the eight Moore neighbours.
2. **The dynamic closure uses the current density.** Section 3.1 replaces \(d_i(t)\) with \(\rho_t\). A replaces it with the constant \(r_*\), a further approximation.
3. **The committed realization starts at the null equilibrium.** Section 4.1 and the placed stepper initialize the realization at \(\pi_1\), whereas A starts it at its own equilibrium \(r_*\). [R2 §§2.3–2.5, 3.1, 4.1; R8, `initial_state`]

The lost feedback changes temporal response even before spatial structure is considered. For A, deviations relax with

$$
r_A=1-a_*-q.
$$

The derivative of the §3.1 map \(F_m\) at the same equilibrium is

$$
F_m'(r_*)=
1-a_*-q+
(1-r_*)g\bar\lambda\Delta t
e^{-(\eta_0+g\bar\lambda r_*)\Delta t}.
$$

The added term is positive for the present positive-gain levels. For example, deterministic evaluation at \(m=1\) gives \(r_A=0.773590579\) and \(F_m'(r_*)=0.912168291\). A consequently removes collective feedback response as well as spatial dependence. Its equilibrium mean agrees with the map; its fluctuation dynamics do not reproduce that map.

Thus “no spatial correlation” is incomplete disclosure. Likewise, “M3's null with g restored” is exact only for the specifically declared surrogate law, not a demonstration that the Moore-neighbour realization has been restored.

The pricing and run-count figures require narrower language too. The stated \(12\times500\times32\times20=3{,}840{,}000\) is an upper-bound run count using eight insertions for every sweep. At 1.3 seconds each it gives 1,386.7 serial hours. This confirms the arithmetic, not the timing on this environment, the exact number of reached levels, or the claimed half-share of SUSTAINED work. The supplied timing script was inspected but not executed. The configuration restriction is real, including its separate production seed-panel restriction; it is a present interface constraint, not a mathematical impossibility theorem. [R7, `f8_run_spec`; R13]

## 3. Recommended reading E: current-density finite-N closure

### 3.1 The generator law

Let \(K_t\) be the active-cell count and \(N=2500\). For an unmodulated SUSTAINED regime at level \(m\), use

$$
a_m(k)=1-e^{-(\eta_0+g\bar\lambda\,k/N)\Delta t},
$$

$$
K_0\sim\operatorname{Binomial}(N,\pi_1),
$$

$$
K_{t+1}
=
U_t+V_t,\qquad
U_t\mid K_t\sim\operatorname{Binomial}(K_t,1-q),\qquad
V_t\mid K_t\sim\operatorname{Binomial}(N-K_t,a_m(K_t)),
$$

where \(U_t,V_t\) are independent conditional on the current count. Retain the level relation \(g\bar\lambda\Delta t=mq\).

This is the mathematical construction already implemented by `f8/closure.py::finite_n_counts`, with its default stationary-null start, and used by `projection_sweep`. Its conditional expectation is exactly

$$
E[K_{t+1}/N\mid K_t/N=x]
=
x(1-q)+(1-x)\{1-e^{-(\eta_0+g\bar\lambda x)\Delta t}\}
=
F_m(x).
$$

This is the direct dynamic bridge to §3.1 that A's fixed-point substitution lacks. [R9, `finite_n_counts`, `projection_sweep`; R2 §§3.1, 4.1]

E is still a **well-mixed count closure**, not the lattice. Cell transitions are conditionally independent given the count; their paths are coupled through the evolving count. The interpretation should say this precisely rather than carry the loose “INDEPENDENT cells” wording in the existing function's docstring. This consultation does not request an M5 source change.

E also does **not** have a finite-N stationary mean exactly equal to \(r_*\). In general \(E[F_m(X)]\ne F_m(E[X])\). Here, writing \(b=g\bar\lambda\Delta t>0\),

$$
F_m''(x)=-b\,e^{-(\eta_0\Delta t+bx)}[2+b(1-x)]<0.
$$

The finite-N stationary fluctuations therefore introduce a mean shift relative to the deterministic fixed point. That is part of the declared stochastic closure, not a reason to reset or condition its samples.

### 3.2 Computational consequence and alternatives

An exact aggregate sampler for A also uses two conditional binomial draws per tick, with constant \(a_*\). E adds evaluation of the current-density activation probability. Both avoid explicit Moore-neighbour operations and per-cell state arrays. This establishes an efficient architecture, **not a measured runtime or a promise of E1's 1.3-hour audit**. Sequential temporal dependence must be retained; independent binomial draws at each tick would implement C instead.

| Reading | Assessment for this ruling |
|---|---|
| A | Usable as a deliberately narrower, equilibrium-calibrated synthetic control; loses evolving feedback and changes initialization. |
| B | As proposed, remains undefined off-grid and changes sampling dependence through reuse. Requires additional design beyond an interpretation. |
| C | Drops the Markov temporal dependence central to the new null and thresholds; no reason to prefer it. |
| D | Most literal substrate execution, with the stated resource burden and current production-interface restrictions. |
| **E** | **Preferred:** already represented mathematically in placed M5, preserves the dynamic conditional closure and null start, and supports an aggregate-count implementation. |

The comparison with B–D is not a proof that no other implementation could work. It identifies the best supported reading in the supplied packet.

### 3.3 Scope of the identified interpretation

A suitable decision for Mike would expressly authorize, **for M6's synthetic SUSTAINED controls only**, the substitution \(d_i(t)\mapsto K_t/N\), with the count process above and separately declared synthetic modulations. It should identify the generator version and the source/record identities that M7 will carry.

That ruling would leave the §2 lattice mechanism, canonical realizations, M-P1, and the frozen audit grammar intact. Qualification would establish the instrument's performance on this declared synthetic ensemble; it would not establish the same error rate on spatial lattice runs.

Interpretation 001 supplies a procedural precedent for an identified ruling beside unchanged contract bytes. It resolved two conflicting descriptions of one observable. It is not substantive proof that either A or E already means “the realization's own rule” without Mike's decision. E's closure substitution must be acknowledged explicitly. [R5; R2 §§1.3, 4.7, 5.1]

If Mike chooses A instead, the ruling must explicitly accept fixed-equilibrium feedback, independent cell paths, and the changed start. These concessions should not be hidden under the phrase “the contract's own closure.”

## 4. Disclosure and the two distinct prices

### 4.1 The later lattice/surrogate comparison

Descriptive comparison against job 0 is appropriate, provided its method is declared before audit outcomes and its scope is stated accurately.

Contract §3.4 defines \(\hat s(m)\) as the sample SD **across 20 calibration seeds of the full 1,000-tick tail mean**. M5 implements it with `ddof=1`. It is not the SD of individual 100-tick classification windows. Interpretation 001 fixes the meaning of tail density throughout these records. [R2 §3.4; R5; R9, `CalibrationCensus`, `_sd`, `calibration_census`]

For each common pass-1 level, the descriptive table should identify:

- The lattice and surrogate means of the same tail observable, their signed difference, and the estimator or analytic calculation used.
- The lattice \(\hat s(m)\) and the surrogate SD of that same observable, with a signed difference or a clearly defined ratio.
- Population size, horizon, averaging interval, initialization, number of independent replicates, and the uncertainty or limitations of the estimates.
- The missing spatial dependence; for A, the additional lost feedback response and different initialization.

A ratio needs an explicit undefined case if its denominator is zero. Comparing A's exact distribution SD with a 20-seed sample estimate is legitimate if the two roles are labelled; they are not equally precise measurements.

Do not assert that the surrogate's variance is below the lattice's at every level. The packet does not establish that universal inequality. Likewise, a variance table alone cannot represent a mean-amplitude mismatch or certify transfer of classifier error rates. The supplied contract already acknowledges lattice/closure amplitude discrepancies as a separate fidelity issue. [R2 §1.2′ and Appendix B.4]

For stationary A, a useful exact reference is

$$
\operatorname{Var}(\bar\rho_H)=
\frac{r_*(1-r_*)}{NH^2}
\left[H+2\sum_{j=1}^{H-1}(H-j)(1-a_*-q)^j\right].
$$

At \(m=0.25\), its SD is \(0.001488102377\) for \(H=100\), but \(0.000480667376\) for \(H=1000\). **Only the second is directly comparable to job 0's \(\hat s(m)\).** These independent-chain formulas must not be used as E's stochastic variance.

Job-0 values are not supplied here. Freeze the comparison method, mark the values pending, and attach an identified descriptive supplement when separately authorized job 0 is available. Do not make that pending comparison an undeclared prerequisite for M6 or use it to retune the frozen generator. Sections 7.1–7.4 retain their qualification and authorization requirements; this consultation creates no exception permitting an early production calibration. The comparison does not independently cover lattice behavior at insertion levels absent from job 0.

### 4.2 The §4.3 null price at qualification

This is a separate requirement. It prices the realized conservatism of \(\theta_P\) through

$$
P_{\rm null}(S_{\min}>\theta_P),
$$

using complete, temporally correlated ten-window null runs. With feedback removed, E and the correctly initialized A both reduce to the independent-chain null. The M6 implementation's draw order and provenance still need their own declaration.

Report the rejection count, independent-run count, empirical rate, nominal \(\alpha_P\), and an uncertainty statement or Monte Carlo resolution. Zero observed rejections is not proof of zero probability. This remains the contract's descriptive price, not a newly invented pass condition.

Two concrete source details matter:

- E1 `run_pricing` counts terminal-statistic exceedances of \(\theta_T\). Copying it would price the wrong F8 event.
- The supplied F8 source records the required event as `NullValidation.s_min_rejection_rate`, computed by `validate_on_stepper`. The consultation and module docstring mention `price_familywise`, but no function of that name is defined in the supplied `f8/null.py`. Cite the actual validation record and field. No prior numerical pricing record is independently re-certified by this consultation. [R6, `run_pricing`; R10, `NullValidation`, `validate_on_stepper`]

The later lattice/surrogate table cannot substitute for this qualification-time price.

## 5. Modulation on excess: acceptable parameterization, incomplete law

### 5.1 What is preserved

Use a declared target such as

$$
r_{\rm tar}(m,t)
=
\pi_1+\kappa(m,t)[r_*(m)-\pi_1].
$$

Applying modulation within SUSTAINED regimes while retaining the same per-sweep regime uniforms and profiles is consistent with §6.4. The latent ramp extent law remains \(w(u_{(18)}-u_{(3)})\). It does **not** follow that every measured label obeys that law exactly: stochastic run-status errors can affect labels and routing, and those errors remain inside the existing audit. [R2 §§5.1, 6.1, 6.4]

The exact \(\kappa\) formula, parameter distributions, onset conventions, time origin, phase and legal domain must be in the generator declaration.

### 5.2 Probability is not hazard

The stationary inversion is

$$
a_{\rm tar}=\frac{q\,r_{\rm tar}}{1-r_{\rm tar}},
\qquad
H_{\rm tar}=-\frac{\log(1-a_{\rm tar})}{\Delta t}.
$$

The first expression gives an **activation probability**, not a hazard. The consultation's phrase “hazard is re-solved” must include the second step. Passing the first expression directly as a hazard would produce the wrong stationary density.

For a finite nonnegative hazard, require \(0\le a_{\rm tar}<1\), hence \(0\le r_{\rm tar}<1/(1+q)\). Preserving at least the spontaneous-floor activation additionally requires \(r_{\rm tar}\ge\pi_1\). Reject invalid parameter draws under the declared preflight; silent clipping changes the generator.

For E, one coherent synthetic modulation, offered as a specification option rather than approved code, is

$$
c_{\rm tar}(m,t)
=
\frac{H_{\rm tar}(m,t)-\eta_0}{r_{\rm tar}(m,t)},
$$

$$
a_t(k)
=
1-e^{-(\eta_0+c_{\rm tar}(m,t)\,k/N)\Delta t}.
$$

At the unmodulated \(r_*(m)\), \(c_{\rm tar}=g\bar\lambda\). Modulation then changes the **synthetic feedback coefficient**, while retaining the floor and deactivation. It must be named as such; it does not change the canonical fixed-\(g\) rule.

L1 may specify another coherent modulation, but an excess target alone does not determine how the count process evolves.

### 5.3 A moving target is not the realized mean

Even in A, setting \(a_t=q r_{\rm tar}(t)/(1-r_{\rm tar}(t))\) gives an instantaneous equilibrium target. Its actual mean obeys

$$
p_{t+1}=a_t+(1-a_t-q)p_t.
$$

A changing \(r_{\rm tar}(t)\) generally differs from \(p_t\). There is no single stationary distribution for arbitrary drift or oscillation. E additionally has nonlinear finite-N feedback.

Declare the initialization and modulation timing, inspect the resulting nominal temporal behavior, and preserve the actual dynamics. Do not reset independent counts to each target, erase lag, or call the target trajectory the exact mean. For recommended E, retain the stationary-null start and full declared horizon, with the modulation's onset and tail phase explicitly specified.

### 5.4 The low-level margin does not prove stochastic success

Using the packet's reported \(\theta_P=0.057364\), the frozen constants give

$$
\pi_1=0.0522823201373,\qquad
r_*(0.25)=0.0669030341510.
$$

At this level, merely keeping the target mean above \(\theta_P\) requires

$$
\kappa>
\frac{\theta_P-\pi_1}{r_*(0.25)-\pi_1}
=
0.3475671474.
$$

For constant-target A, the following deterministic calculations show why excess modulation alone is insufficient:

| Excess factor | Target density | A's 100-tick SD | Target–threshold gap / A SD |
|---:|---:|---:|---:|
| 1.00 | 0.0669030342 | 0.0014881024 | 6.410 |
| 0.75 | 0.0632478556 | 0.0014526983 | 4.050 |
| 0.50 | 0.0595926771 | 0.0014157424 | 1.574 |

The packet's “about seven SD” uses the null SD. It is not the variance of A at the SUSTAINED density, much less a proof about all ten realized windows. These calculations use the supplied threshold value; they are not a new M3 threshold qualification. They are also **A calculations**, not an error estimate for E.

A parameter preflight may certify legal probabilities, target margins and the declared feature. It cannot certify that every unrestricted random trajectory will receive its intended status. Do not redraw NULL or SUSTAINED traces until the classifier returns the desired label. That conditions away the errors the audit must observe.

### 5.5 Named morphology must actually be present

A decreasing excess multiplier does not necessarily create a decreasing resulting amplitude, because \(r_*(m)\) itself rises with \(m\). The `nonmonotone_amplitude` declaration and preflight must examine the resulting above-onset profile, not just the sign of the attenuation factor. Similarly, temporal parameters must instantiate the declared drift or oscillation over the observation schedule rather than a constant or effectively absent feature.

E1's `archetype_preflight` primarily checks geometric placement. It cannot simply be copied and represented as proving these new amplitude and dynamic conditions. Freeze the parameter checks and bounded redraw rule before masters are drawn; retain apparatus halts in the completion accounting. [R6, `archetype_preflight`, `draw_params`, `regime_at`]

No numerical safety factor or new class error cap is ratified by this consultation.

## 6. Two concrete integration issues beyond the A/E choice

### 6.1 DIP must be adapted to F8's terminal statistic

E1's `DIP_WINDOWS` and `gen_dip_run` permit the zeroed window to be any of the ten, including window 9. F8 explicitly defines \(S_{\rm term}\) as **that single final window**, whereas E1 used a different terminal statistic. A terminal zeroed DIP therefore has \(S_{\min}=S_{\rm term}=0\) and is classified NO_SUSTAINED. It is not UNRESOLVED. [R6, `DIP_WINDOWS`, `gen_dip_run`; R11, `tail_stats`, `run_status`]

Section 6.4 requires the DIP-driven levels to be U deterministically. The declared F8 DIP must therefore enforce

$$
S_{\min}\le\theta_P,\qquad S_{\rm term}>\theta_T
$$

on the exact count grid. Excluding the terminal dip is necessary for the zero-window construction, but an unrestricted stochastic final window still does not establish the second condition with certainty.

A deliberate synthetic DIP may use a nonterminal zero window and a terminal segment with declared support strictly above \(\theta_T\). Such a construction must be specified before sampling. Its designed constraints belong to the separately named DIP regime; they must not become hidden post-classification repairs to ordinary SUSTAINED traces. The corresponding build evidence should exercise terminal placement and threshold equality explicitly.

### 6.2 A generator at insertion levels does not complete the scoring path

M1's production run guard is not the only relevant restriction:

- `f8/config.py::f8_run_spec` restricts production-shape runs to pass-1 levels and the declared canonical/calibration panels.
- `f8/null.py::null_thresholds` also rejects off-grid levels.
- `build_threshold_cache` restricts both cache roles to pass-1 levels, and its production cache to exactly the 24 frozen pass-1 levels. [R7; R10]

A or E may generate at an insertion \(m\), but M6 must still have a declared, validated way to score that level.

The repair is an identified M6 reachable-level cache or adapter that binds the actual router's reachable micro-unit surface to the existing certified, level-independent null law and threshold payload. Missing reachable keys must fail closed. Its identity and completeness must be established before audits; it must not silently promote a slice, relabel an off-grid object as an existing M3 object, or weaken M1's run-spec guard. A separately reviewed change to an existing module would require its own disclosure.

The placed `reachable_router_cases` and E1's carried reachable-cache architecture provide the relevant structural pattern. This is an M6 integration requirement, not a retrospective reversal of the placed M1 or M3 scope. [R12, `reachable_router_cases`; R6, `reachable_pass2_levels`, cache qualification/loading]

## 7. Prospective build-review DEFECT conditions

The following are the bounded defects to design out. Their repairs are specified above; this table does not assert that unsubmitted M6 source already contains them.

| ID | I would mark DEFECT if the build… | Required repair/evidence |
|---|---|---|
| D1 — generator identity | Calls A the evolving §3.1 process, calls either surrogate the spatial lattice, or changes its start without identifying it. | Adopt Mike's precisely scoped E ruling, or explicitly identify A's extra approximations and initialization. Bind the implemented law and interpretation identity. |
| D2 — transition and modulation law | Uses \(q r/(1-r)\) as a hazard; clips illegal rates; treats a moving equilibrium target as an exact mean; or substitutes independent ticks for Markov evolution. | Explicit probability/hazard conversion, domain checks, state transition, start and timing; demonstrate the unmodulated law and g=0 reduction. |
| D3 — generator truth and sampling | Uses excess modulation without validating the named feature/margin, or rejects realized NULL/SUSTAINED paths based on classifier outcomes. | Declared parameter-level preflight and recorded redraw/halts; retain unconditioned path noise and its resulting audit errors. |
| D4 — DIP | Carries E1's terminal-window dip or claims deterministic U from an unbounded stochastic terminal segment. | A declared count-grid construction satisfying both F8 run-statistic inequalities by its support. |
| D5 — insertion-level support | Generates pass-2 runs but cannot obtain validated thresholds at their exact identities, or bypasses current production guards. | Complete, identified reachable-level mapping to the certified F8 null; missing-key refusal and correct provenance. |
| D6 — traces and streams | Carries E1's 3,000-entry array, misaligns the tail, pads a synthetic record while representing it as an M1 trajectory, or reuses whole paths as independent realizations. | F8's 3,001-entry convention, scored ticks 2001–3000, exact count-grid arithmetic, explicit synthetic provenance and declared RNG hierarchy. |
| D7 — pricing and governance | Prices \(\theta_T\) instead of the §4.3 event, conflates the later job-0 comparison with qualification, draws masters before full generator freeze, or changes the frozen audit grammar. | Correct event/denominator, separately identified descriptive comparison, source/declaration freeze before masters, and unchanged qualification/stop rules. |

The count sampler reproduces an aggregate law; it is not byte-identical to M1's one-uniform-per-cell stream. The M6 declaration must specify its own draw order and stream separation. Shared per-seed **regime-assignment uniforms** across levels are prescribed by §5.1; they do not authorize copying stochastic trajectories across levels or sweeps.

M6's qualification is the frozen applicable-error test: scientific-intent classes count final ND; ND-intent classes count final LOCATED or NOT_PRODUCED. Exact intended-verdict/cause recognition is descriptive within that M6 grammar. **Do not import M-P1's exact-cause qualification or half-band noise condition.** Retain 500 attempted/scored sweeps per class, zero halts, the one-sided 95% CP upper cap 0.10, the mechanical design/held-out join, and the adverse-stage stop path. [R2 §§5.1, 5.4, 7.1; R6, audit declaration and scoring]

## 8. Disposition of the adjacent items

**“Two-part generator.”** On the supplied record, agree with L1: this is a handoff gloss. The contract's binding two-part object is job 0's realization-plus-skeleton calibration census. No skeleton M6 generator is added by this consultation. [R1 §3; R2 §7.3]

**Masters.** Agree that the M6 masters are DERIVED@BUILD after the table, resolution and **complete generator** are frozen. Freezing only the label “A” or “E” is insufficient. Commit the declared derivation rule and seed, draw the fresh values once, and bind the implementation, generator declaration, contract freeze and interpretation identities. Preserve §7.1's M3/M-P1 qualification ordering and the retired-master restrictions. Do not choose or replace masters after seeing audit outcomes. [R2 §§5.1, 5.3, 7.1; R3 §5]

**`no_null_consistent_anywhere`.** Interpret it operationally as SUSTAINED-regime assignment at every level. At positive floor, zero is **not absorbing**; it is not mathematically unreachable. The wording must not become a zero-truncation or path-resampling rule. This control's intended morphology is not proof that every stochastic run must receive SUSTAINED. [R2 §§2.6, 5.2]

**Decision now available to Mike.** Prefer E as the M6-only current-density closure reading. If he instead selects A, record the additional approximations explicitly and apply the same disclosure, modulation, DIP, pass-2 and qualification requirements. L1 can then record `F8_INTERPRETATION_002`, complete the declaration and build, and submit the source under the normal receipt-first module-review process. This consultation does not place that ruling or supply module clearance.

## 9. Verification performed and limits

The receipt established **42 manifested payload files plus MANIFEST.txt = 43 files**, excluding 12 directory entries. All 42 full file digests matched the manifest; the archive matched the supplied full digest. The extracted payload identities were rechecked during preparation of this response and remained unchanged.

The consultation used the supplied contract, freeze record, Appendix A, interpretation record and source. Independent mathematical cross-checks examined the contract reading, stochastic generator and carried audit mechanics. Deterministic calculations checked the fixed-point relation, relaxation factors, stationary A variances, low-level excess margins and run-count arithmetic.

No M6 code was proposed or placed. No packet source was modified. No masters were drawn. No audit, lattice benchmark, job-0 census, canonical job or module test suite was executed. Runtime estimates and the quoted M3 threshold remain attributed to the packet; neither is represented as a new execution result.

## Source register

All paths below are within the verified archive. SHA-256 prefixes are the first 16 hex digits; comparisons against the manifest used full digests. References to functions and contract sections in the body identify the supporting source without importing material from other workstreams.

| Ref | File | SHA-256 prefix |
|---|---|---|
| R1 | `L1_TO_L2_F8_M6_GENERATOR_CONSULTATION_2026-10-30.md` | `7f7acc6bf6881381` |
| R2 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f` |
| R3 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139` |
| R4 | `flights/mfa_fidelity/contracts/flight8/APPENDIX_A_OF_RECORD.md` | `94d527624beafa7c` |
| R5 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c` |
| R6 | `flights/mfa_fidelity/instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4` |
| R7 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `43ea8de23c0d718b` |
| R8 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8` |
| R9 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350ab` |
| R10 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `4ee3f239b27f772b` |
| R11 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783f` |
| R12 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5` |
| R13 | `tools/time_one_run.py` | `289b3ce5dae0e987` |

**L2 return:** recommend E for Mike's ruling; A's equivalence claim is not accepted as stated. Contract bytes remain unchanged. The M6 build and its qualification remain pending.

