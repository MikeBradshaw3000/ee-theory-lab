# L2 → L1 — Flight 9 design consultation on Design Note v0.2

## 1. Receipt — completed before substantive review

**Receipt: PASS.** The archive contains exactly **23 payload files plus `MANIFEST.txt`: 24 regular files**, with no directory entries. Every payload file matches its manifest SHA-256. The manifest covers every payload exactly once; there are no missing, extra or duplicate file paths.

| Receipt item | Verified result |
|---|---|
| Archive | `f9_design_consultation_L2_v1.zip` |
| Archive SHA-256, computed | `433dfded65d6cf96102e4142347010e0bf90ee7b2c9ecac02ca60e2442a6bd6d` |
| Payload files | 23 expected; 23 received; 23 hash matches |
| Total regular files | 24 expected; 24 received |
| Directory entries | 0 |
| `MANIFEST.txt` SHA-256, computed | `e3c5da5d9af2c1a381081530efce448f4e8d3dbbe9f3bf4993d9d1b331212998` |
| Manifest coverage | All 23 payload paths, once each; no omissions or additions |
| Stated repository pin | `ee-theory-lab`, `main`, `817450e39682d1c5d43bd787b8971ba3a9e0c7fc` |

The archive and manifest digests above are observed identities: no independent expected digest for either was supplied in the request. `MANIFEST.txt` does not list itself. The checks below establish payload agreement with the supplied manifest; the ZIP is not an independent Git-history authentication of the stated pin. The instruction document expressly identifies itself as new, to be committed with this return; it identifies the other payloads as extracted from the pin.

### 1.1 Every payload, in manifest order

The SHA-256 column is the independently computed full digest. **MATCH** means it equals the full digest recorded for that exact path in `MANIFEST.txt`.

| # | Repository-relative payload path | Computed SHA-256 | Against manifest |
|---:|---|---|---|
| 1 | `flights/mfa_fidelity/design/flight9/L1_TO_L2_F9_DESIGN_CONSULTATION_2026-11-12.md` | `d1078117a5fc21d38905e08d9fdd9249367bf37909dbda5f3de7fe968c554c12` | MATCH |
| 2 | `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_2.md` | `aabd30fcd53477bf8c5e8534c44f3f3cca6f95c99f4f2dfee2a55d829e40f3ac` | MATCH |
| 3 | `flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_1.md` | `c7dddb544a7f180fcd655acb96729efc2f34d6daf6051c2af92a56a8fea0bcef` | MATCH |
| 4 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` | MATCH |
| 5 | `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` | MATCH |
| 6 | `flights/mfa_fidelity/contracts/flight8/APPENDIX_A_OF_RECORD.md` | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` | MATCH |
| 7 | `flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md` | `194886e89f55a4c7fff1413db767975d892660163a530f581e2131ec5121272d` | MATCH |
| 8 | `flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md` | `69d173f370d5ce6d86858142783eab6dfc1918aeb197eab5fd50b497d9e1c975` | MATCH |
| 9 | `flights/mfa_fidelity/rulings/PD_PARTICIPATION_RULINGS_PD1_PD7.md` | `f239b8f7444e38395341acb2ccec23dfee0632596eab3080019ee5ec175fe4ee` | MATCH |
| 10 | `flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_1.md` | `ec63fdb0e2060110b99116605d7673bc61d4d63ca79f0c3a6b41365848d39524` | MATCH |
| 11 | `flights/mfa_fidelity/build_records/L2_F8_STAGE1_DISPOSITION_CONSULTATION_2026-11-12_RECEIVED.md` | `9eb96103745dc6b395bca65e0e725676fe81d38b821cfbaa8829c4769f19a5f6` | MATCH |
| 12 | `flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md` | `39f66673657b0f429691c908142f889d9ef3d463a8372455cba95db7c486f52a` | MATCH |
| 13 | `theory/overview/EE_emergence_overview_v1_8_1.md` | `b2d67fac5efa3c73fe8f76ea3ba7d18f88023f468f648c2a36532bd69522b41c` | MATCH |
| 14 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f79e99caeb68515257d9739471fcec7253355f553647d9d37d` | MATCH |
| 15 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` | MATCH |
| 16 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/classify.py` | `42daeb4663c5783fbcdb3c03cf894f8d5f10181aa5ab025dbdece6ae44bc5219` | MATCH |
| 17 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` | MATCH |
| 18 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/config.py` | `3b3c8c772937de110345814a2c8367258a1888202d57e344ea0c48a5d6d574e7` | MATCH |
| 19 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` | MATCH |
| 20 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` | MATCH |
| 21 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/null.py` | `2525b1c6df1a5029fa05c08bf2f041680f7fd5220ab8df0b0be41640b3e7d7bb` | MATCH |
| 22 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` | MATCH |
| 23 | `flights/mfa_fidelity/instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | MATCH |

### 1.2 Separately attached instruction file

The standalone `L1_TO_L2_F9_DESIGN_CONSULTATION_2026-11-12.md` has SHA-256 `d1078117a5fc21d38905e08d9fdd9249367bf37909dbda5f3de7fe968c554c12` and is byte-for-byte identical to payload 1. It is a duplicate attachment, not a twenty-fourth payload. I followed the instruction at its repository-relative path inside the verified packet.

---

## 2. Scope, authority and overall disposition

**Date:** 2026-11-12. **Reviewer:** L2, adversarial design reviewer. **Decision authority:** Mike.

DESIGN DISPOSITION: REQUIRES CHANGE

The two composition arms, frozen-base gain sweep, fresh flat reference and descriptive flicker reporting are useful foundations. The design is not yet ready to be translated into a freezable contract. Its main defect is the gap between **a spatial pattern being compatible with an input index** and **that compatibility adjudicating the theory’s collective composition claim**. The proposed statistic also changes the stated hypothesis: constancy of the whole occupancy map on index contours is stronger than one boundary being a level set. These are design decisions to settle before inspecting terrain output. [D §§3.1–3.6; O §§7–8; PD7]

I would frame Flight 9 as asking **what spatial description survives the move from homogeneous to heterogeneous inputs**: can the prescribed rules be distinguished in spatial output, and when does neighborhood context prevent local conduciveness alone from describing the observed boundary? This permits meaningful adverse findings without treating recovery of a coded input as selection of the theory’s true composition. The Overview leaves the exact function F open. [O §8]

This consultation respects the fixed scope: terrain and composition; one stream per cell; heterogeneity between cells; no Regime II, Ψ or coherence observable. Mike’s recorded rulings stand unless he changes them on this return. Recommendations below identify changes for him to rule on; they do not amend those rulings, authorize a probe, alter Flight 8 or clear a contract or build. [P opening, §4; D §§1, 11–13]

### Dispositions at a glance

| Question | Disposition | Principal decision |
|---|---|---|
| Q1 — Claim grammar | **REQUIRES CHANGE** | Retain two conditional tests; align boundary claim and statistic; disclose the independent-response alternative; separate valid failure from non-identifiability and inadequate precision. |
| Q2 — Omit M2/M4/M6 | **REQUIRES CHANGE** | Omit the obsolete morphology apparatus, but add a targeted statistical qualification of the new evaluator beyond its known-answer corpus. |
| Q3 — Two compositions | **ACCEPTABLE IN PRINCIPLE** | R1 supplies rival-only arbitration. Homogeneous equivalence is at matched effective gain, not matched raw base triples. |
| Q4 — Sweep g and normalize | **REQUIRES CHANGE** | Gain sweep is sound for this rule. Correct the base-scaling argument and adopt a prospective normalization with a stated estimand. |
| Q5 — Flicker discharge | **REQUIRES CHANGE** | The uncensored active-spell law is geometric. The proposed two counters do not yet define the inactive-spell statistic; specify censoring, windowing and sufficient records. |
| Q6 — Defer onset continuity | **ACCEPTABLE IN PRINCIPLE** | No supplied record requires Flight 9 to resolve it. Correct the overbroad reasons and preserve the outstanding limitation. |
| Q7 — Terrain fidelity | **REQUIRES CHANGE** | Separate skeleton onset, realization occupancy edge and heterogeneous closure prediction; retain the fresh T0 reference. |
| Q8 — Pre-contract probe | **REQUIRES CHANGE** | Preserve the permission in principle, but require a prospective probe declaration and an explicit resolution of Interpretation 004’s “before any data” obligation. |
| Q9 — Other freeze blockers | **REQUIRES CHANGE** | Resolve the zero-face/floor correspondence, estimands, spatial scale, reporting coverage and new record/dependency schema. |

**Evidence basis.** Only the supplied packet was used. References such as [D §3.6] identify packet documents in the source key at the end. Mathematical counterexamples and calculations below are L2 derivations from that record, not terrain observations or probe results.

## 3. Q1 — Claim grammar

**Disposition: REQUIRES CHANGE.**

### 3.1 Preserve two tests, but state what each can establish

**Test (a): conditional discriminability.** On predeclared informative terrains and control levels, determine whether the spatial records distinguish the two prescribed input rules at the declared resolution. A pass establishes a distinguishable output consequence of changing the composition in the instrument. It does not identify which composition describes entrepreneurial ecosystems. Failure can expose an uninformative terrain, insufficient resolution or a genuinely indistinguishable output; it does not automatically indict the theory. [D §3.3(a); O §8]

**Test (b): conditional boundary compatibility.** Under each prescribed rule, determine whether an independently defined observed boundary can be represented by a level set of that rule’s local conduciveness, at declared spatial and statistical resolution. A valid failure says that this local-scalar description fails for that rule, terrain, object, size, horizon and resolution. A pass establishes compatibility within that scope.

I recommend this boundary formulation for the stated substantive endpoint. If L1 instead wishes to score occupancy constancy over all contours, Mike should explicitly adopt the stronger **occupancy-map** proposition. It should not enter under the name of the narrower boundary claim. PD7 supplies the activation-surface commitment, but mapping it to a finite spatial occupancy boundary remains an instrument-level bridge that must be stated. [D §§3.3(b), 3.6; PD7 and layering; O §§7, 10]

### 3.2 The level-set claim has adverse room, but one proposed example does not

Equal local λ does not imply equal neighbor activity in the carried rule. Equal-λ sites in different neighborhoods can consequently have different occupancies. A measured boundary can contain λ values whose spread exceeds the declared tolerance, or an isolated favorable patch can fail to sustain activity while a less favorable, better-supported region persists. These are possible adverse mechanisms, not evidence that any occurs on the proposed terrains. [C §2.4; D §3.2]

However, **a uniform boundary shift above the closure’s threshold is still a level set**. If location belongs to fidelity, shifting the entire edge from one λ contour to another is a fidelity discrepancy, not failure of level-set structure. Likewise, extinction of an entire run leaves no boundary to test; it is not automatically evidence of a distorted contour. Remove these shortcuts from the justification of adverse room. [D §§3.2, 3.6, 9]

### 3.3 An explicit alternative can pass both proposed tests without coupling

Consider independent two-state cells obtained analytically by replacing the evolving neighbor fraction with a fixed constant \(d_0>0\):

\[
a_i=1-\exp[-(\eta_0+g\,d_0\lambda_i)\Delta t],
\qquad
p_i=\frac{a_i}{a_i+q},
\qquad
q=1-\exp(-\mu\Delta t).
\]

Their stationary occupancy is an increasing function \(p_i=h(\lambda_i)\). It is constant on the input index’s contours and, on a discriminating terrain, can produce different product and height patterns. There is no neighborhood interaction. Both tests can therefore pass without demonstrating the coupling-supported regional activation described in PD7 and the Overview. This is an analytical counterexample derived from the two-state rule, not a simulated rival arm. [C §§2.4, 2.9; PD7; O §10]

The existing floor-only null excludes a constant low-occupancy explanation; it does not exclude this heterogeneous independent response. TA does not exclude it either.

For the narrower conditional boundary claim, disclose this alternative and limit the interpretation. **No third scientific arm is required merely to make that narrower claim.** If a pass is instead to establish specifically collective reinforcement, add a separately declared coupling-sensitive contrast and observable that the independent-response alternative cannot reproduce—for example, a controlled comparison of equal local λ in different neighborhood contexts. Simply labeling independent-response maps “must fail” in a synthetic corpus would be incorrect: they really do satisfy contour constancy.

### 3.4 A boundary and an entire response map are different objects

The boundary statement asks whether a particular observed edge follows a λ contour. Section 3.6 instead asks whether occupancy throughout the domain is a function of λ alone:

\[
p_i=h(\lambda_i).
\]

The second statement implies much more. A boundary can follow one contour even when occupancy varies along other contours. Conversely, a constant map satisfies contour constancy vacuously while exhibiting no informative boundary. A decreasing or nonmonotone function of λ can also be constant on contours while violating the proposed ordering.

Before the probe, select the proposition and its scientific interpretation. Before freeze, declare the independent edge extraction or map estimand, direction of the ordering, minimum contrast, contour construction, weighting, resolution and uncertainty method. Do not define the observed edge by thresholding λ itself: that would make the boundary result an input construction. Empty, full, floor-dominated, saturated or insufficiently resolved maps cannot earn substantive support merely through small contour residuals. [D §§3.3, 3.6, 10.2]

### 3.5 TA and the adverse labels

TA is an appropriate **non-identifiability control for the contour-based comparison between compositions**. If \(v=u=r=t(x)\), product is \(t^3\) and height is \(t\): the contour families and orderings coincide. Test (a) must not select an index on that evidence. Different amplitudes at equal raw g do not license changing the endpoint from contours to amplitudes after observation. [D §3.5]

TA need not return ND for the separate within-rule boundary test. That endpoint can be compatible, adverse or unevaluable on TA. Replace the blanket statement that “the composition tests” must return not adjudicable with this endpoint-specific requirement.

The proposed adverse labels are usable under explicit evidence rules:

| Label | Required meaning |
|---|---|
| Follows own | Own relation lies within a declared equivalence tolerance on an informative domain, with adequate precision. Whether the rival is excluded is a separate determination. |
| Follows rival | Own relation is excluded beyond tolerance; rival relation satisfies its equivalence criterion; the alternatives are identifiable on this domain. |
| Follows neither | Both relations are excluded beyond tolerance on an informative, evaluable domain. |
| Not distinguished | The available evidence cannot separate the alternatives, or declared precision/contrast/resolution is insufficient. |
| Not adjudicable here | Terrain geometry makes the contour predictions equivalent by design, as on TA. |
| Apparatus unevaluable | Required observations or valid records are unavailable; this is not an adverse scientific finding. |

Failure to reject is not equivalence; failure to establish either fit is not proof of “neither.” When both relations fit, identification is ND even though the own-rule compatibility endpoint may pass. Preserve separate endpoint records rather than force all these facts into one exclusive label. [D §§3.3, 3.6; L2 design requirement]

## 4. Q2 — Omitting M2, M4 and M6

**Disposition: REQUIRES CHANGE.**

Omitting Flight 8’s morphology classifier, router and morphology audit is acceptable. Their historical jurisdiction does not justify recreating them for a different scientific endpoint. Flight 8 explicitly states that M4 does not determine P1, and its expected morphology was fixed in advance. [C §§1.3(a), 4.7, 4.9; CL §4.3]

**The known-answer corpus is necessary but insufficient for the proposed new inference.** Flight 8 itself distinguishes implementation qualification—controlled cases with constrained noise and exact verdict/cause checks—from statistical qualification on design and held-out ensembles. It expressly limits the former to testing evaluator implementation. [C §§4.11, 5.1, 5.4]

Require a new, focused qualification before canonical composition scoring. It must guard the following:

| Risk | Required qualification target |
|---|---|
| False identification | No winner on common-contour/TA cases; no false own-index selection when the rival or neither is supported. |
| Vacuous support | Correct treatment of constant, empty-edge, saturated, singleton-contour and low-contrast maps. |
| False adverse finding | A genuinely compatible map is not rejected because the method misprices correlated finite-tail variation. |
| Improper ND | Inadequate information returns its declared cause; sufficiently discriminating cases retain declared sensitivity. |
| Aggregation error | The error target matches decisions across contours, levels, terrains and rules, including any flight-level conjunction or selection. |
| Wrong branch | The right label reached with the wrong cause fails the corresponding known-answer case. |

Freeze an independent generator truth, evaluator, design and held-out ensembles, sample counts, applicable errors, error caps, uncertainty on those errors, halt accounting and failed-qualification path. The held-out ensemble must remain untouched until those choices are fixed. Analytical guarantees can reduce the empirical burden where they actually apply.

The independent units are seed runs producing spatially correlated maps. Cell counts do not turn one run into thousands of independent replications, and finite-tail temporal dependence must enter the observation model. Synthetic generators should stress the dependence and coverage that matter to the selected estimator.

This requires **M6’s protective function**, not its old module, twelve classes, numerical cap or sample count. It is L2’s recommended new safeguard, not a claim that the committed record already requires every successor to copy M6. Any synthetic error guarantee remains limited to its declared ensemble; Flight 8’s close explicitly rejects automatic transfer of those rates to the spatial lattice. [CL §3; L2 §3.3]

Nor can qualification repair Q1’s attribution problem: an independent-response process that truly satisfies the tested contour property is not a statistical false positive for that property. Its existence restricts the claim.

## 5. Q3 — Product and height-like rival

**Disposition: ACCEPTABLE IN PRINCIPLE.**

The frozen specification carries the arithmetic-mean dispatch and prohibits selecting it without arbitration. Mike’s recorded R1 supplies arbitration for **rival-only use**. This is consistent with the specification, provided the contract preserves its status as a compensatory comparator and does not present it as satisfying the zero-collapse architecture. Keep the dispatch identities distinct. [S §2.1; D §11, R1; O §8]

Using the product instead of Flight 8’s symmetric dispatch creates no gap in Flight 8’s P1 conclusion **at matched effective gain \(g\bar\lambda\), equivalently m**. Flight 8 selected homogeneous bases to attain each declared m; the hazard consumed the resulting scalar. That is the freeze record’s precise sense of “F is inert.” It does not mean the formulas agree on identical base triples. With equal bases b, the placed configuration explains that the normalized symmetric dispatch is \(b^4\), whereas the product is \(b^3\). [FR §3 item 2; C §2.8; config.py, homogeneous_base_from_lambda]

At build, require the heterogeneous step with a constant λ array to reduce to Flight 8’s scalar step at equal state, effective gain, floor, deactivation rate, timing and supplied uniform array. Separately check initialization, stream identity and observables. This is a direct implementation bridge; rerunning the four scientific tests is not a substitute for it. [dynamics.py, activation_probability and step]

A product-versus-mean contrast does not select multiplication uniquely among admissible zero-collapsing functions. The minimum and symmetric-product candidates remain untested; that limitation does not require adding a third composition now. [S §2.1; O §8]

## 6. Q4 — Sweeping g and common normalization

**Disposition: REQUIRES CHANGE.**

### 6.1 The rule equivalence is sound; the stated scaling argument is not

With every other channel fixed, the carried activation rule sees g and λ only through \(g\lambda_i\). Preserving that product preserves the transition probabilities and, with the same state and random draws, the update. Freezing the bases and sweeping g is therefore a sound parameterization of this instrument. [C §2.4; dynamics.py, step]

Section 4’s argument about changing terrain shape is incorrect for the two selected compositions. Without clipping, uniform scaling by s gives

\[
F_{\rm canonical}(sv,su,sr)=s^3F_{\rm canonical}(v,u,r),
\qquad
F_{\rm baseline}(sv,su,sr)=sF_{\rm baseline}(v,u,r).
\]

Each is a uniform scalar change across cells; each preserves its own orderings and contour geometry. The powers differ between compositions. Clipping could alter shape, but no clipping supports the note’s stated argument. [D §4; S §§2.1–2.2]

Retain the gain sweep to preserve base-array identities, avoid domain/clipping issues and make the multiplicative control explicit. Qualify the equivalence as **rule-specific**: the Overview’s displayed spontaneous term also scales with Λ, whereas the carried flight floor is fixed. Sweeping g is not interchangeable with changing Λ in every theoretical channel. An appended notation/bridge row is required. [O §10; N §§1, 2a]

### 6.2 Normalization to adopt

For this proposed structural comparison, I recommend **spectral-relative gain**, using the same deterministic normalization procedure and the same normalized grid for both compositions.

For composition X on the fixed terrain, let

\[
B_X=\operatorname{diag}(\lambda^X)A/8,
\qquad
g_{{\rm spec},X}=
\frac{q}{\Delta t\,\operatorname{spr}(B_X)},
\qquad
\kappa=\frac{g}{g_{{\rm spec},X}},
\]

where A is the declared Moore adjacency and spr denotes spectral radius. The skeleton closure linearization is

\[
J_0=(1-q)I+g\Delta t\,B_X.
\]

Its leading multiplier reaches one at \(g_{{\rm spec},X}\), when the spectral radius is positive. On T0, \(\operatorname{spr}(B_X)=\bar\lambda\), so κ reduces to Flight 8’s m. This derives directly from the committed heterogeneous comparator. [C §3.5]

This comparison matches distance from each rule’s **closure instability**, not physical raw gain. Equal-mean λ normalization controls a different quantity and does not generally align heterogeneous feedback operators. No normalization is neutral to every scientific question; this one matches the proposed structural question and must be named as such.

Require these conditions:

1. Compute normalization from fixed terrain arrays and adjacency before dynamic data.
2. Persist raw bases, raw λ, spectral radius, spectral crossing, actual g, κ and local \(m_i=g\lambda_i\Delta t/q\).
3. Never normalize by observed onset, occupancy or fitted edge.
4. Declare the zero-spectral-radius case: no finite spectral crossing, no division by zero and no invented normalized level.
5. Report raw-g crossings alongside normalized quantities. The closure crossing at κ = 1 is true by definition, not a result.
6. Fix the normalization for scored analysis; do not choose between spectral and mean normalization after seeing which separates better.

A positive scalar normalization cannot change an index’s contour family. It **can** change which finite-grid levels fall in informative, floor-dominated, saturated or extinction-prone regimes, and therefore change power and outcomes of either test. That is why normalization is a prospective design choice rather than an inconsequential plotting convention.

## 7. Q5 — Flicker observable and Interpretation 004

**Disposition: REQUIRES CHANGE.**

### 7.1 The active-spell law is correct under a precise meaning

Once an active spell begins, each tick terminates it with probability q, independent of λ and neighbor activity. A complete, uncensored spell has

\[
\Pr(L_{\rm on}=\ell)=(1-q)^{\ell-1}q,\quad \ell\geq1,
\qquad
\mathbb E L_{\rm on}=1/q.
\]

For μ = 0.2 and Δt = 1, direct arithmetic gives \(q=0.181269246922018\) and \(1/q=5.516655566127\) ticks. The law applies at every cell and level conditional on a spell occurring, under the carried rule. It does not make a finite-tail sample mean exact or remove bias from clipped or selected spells. [C §§2.4, 2.7; dynamics.py, step]

Correct “every cell switches constantly.” Skeleton cells can become permanently inactive, and a finite record can contain no switches. In the positive-floor stationary process, activity recurs, but this is not constant switching in every observed cell.

There is also a qualification to the claim that the information lies in mean inactive-spell length. For a recurrent stationary/ergodic cell process with occupancy \(p>0\) and finite spell means, the exit flux is pq, giving

\[
\mathbb E L_{\rm off}=\frac{1-p}{pq}.
\]

Thus the stationary **mean** inactive duration is itself determined by occupancy and q. Inactive-spell distributions and temporal correlations can carry additional information. This identity is not an assertion about finite censored tails or the skeleton’s absorbing stationary state. The proposed mean remains a legitimate descriptive observable, but it is not an independent criticality signature.

### 7.2 The two counters do not yet determine the named statistic

Let a recorded binary window series contain n windows, A active windows and K switches between adjacent windows. The strings “001100” and “100001” both have n = 6, A = 2 and K = 2. Their observed zero-run lengths are respectively (2, 2) and (4), giving means 2 and 4. Therefore active time and switches do not uniquely determine even the mean of clipped inactive runs.

If the endpoints are \(y_1,y_n\), the number of observed zero segments is

\[
R_0=\frac{K+2-y_1-y_n}{2}.
\]

An initial-state bit plus switch parity determines the final state; alternatively record \(R_0\) directly. This is a small repair, not a demand for full state histories.

**Recommended minimum:** declare the statistic as the mean length of **observed inactive segments clipped to the recording tail**. Retain active-window count, record inactive-segment count directly, and retain endpoint bits to identify boundary-touching segments; alternatively retain switches with endpoint bits and derive \(R_0\). For **non-overlapping, equal-width complete windows**, its value is \(W(n-A)/R_0\) ticks. A sliding-window version requires its own declared stride and duration convention. Mark boundary-touching segments as potentially censored; an all-inactive finite record does not estimate the duration of a completed spell. An all-active record has no inactive segments and returns “undefined: no inactive segment,” not a fabricated zero.

If Mike intends the mean of complete uncensored spells instead, persist their completed-duration sum and count, together with the censoring/coverage information needed to interpret them. The statistic’s name must identify which estimand is being reported. The two proposed counters alone are insufficient for that version as well. [D §§7.1–7.4; I4 point 4]

### 7.3 W = {1, 10, 100} is acceptable as a declared reporting set

Freeze block versus sliding windows, alignment, tail endpoints, partial-window handling, the “any activity” reduction, units, occupancy bands, aggregation across cells/seeds and no-spell conventions. Keep the W = 1 participation declaration separate from coarser observation windows; observing the same tick process at W = 100 does not silently change the dynamical rule or establish invariance across operationalizations. [D §§6–7; PD5; C §2.10]

Window occupancy can change substantially even under the floor-only null. In stationarity, with \(a=0.01\) and \(\pi_1=a/(a+q)\),

\[
\Pr(\text{any activity in W consecutive recorded ticks})
=1-(1-\pi_1)(1-a)^{W-1}.
\]

This is approximately 0.05228, 0.13424 and 0.64960 for W = 1, 10 and 100. These are analytical null probabilities, not measured terrain results. A coarse-window “intermediate occupancy” band can therefore include cells driven only by the floor. Record the W-specific reference and avoid interpreting such a band as a demonstrated collective margin. [C §2.9; analytical derivation]

Recording at every declared run and level is a reasonable coverage rule; do not justify it by asserting that every level necessarily contains a spatial boundary. Some maps will have no edge. The set of actual levels must be bound prospectively rather than left as an unspecified future sweep.

**Discharge:** this plan can satisfy Interpretation 004 once the statistic, windows, levels and sufficient persisted information are unambiguously declared, implemented and required as reporting records. It does not discharge the obligation merely by promising six integers. Nor do means preserve full run-length distributions or establish the held resolution-invariance candidate. Interpretation 004 requires prospective reporting, not a successful flicker test; that candidate remains untested. [I4 point 4 and Consequences; PD held candidate]

The pre-probe timing of that declaration is addressed under Q8.

## 8. Q6 — Leaving onset continuity out of Flight 9

**Disposition: ACCEPTABLE IN PRINCIPLE.**

Nothing in the supplied record requires the immediate successor to resolve continuity through the incoming interval. The prior L2 return says a successor **can** address it, and the ratified close makes it a successor design question without authorization or a Flight 9 deadline. Mike’s R9 deferral is consistent with those texts. This differs from the expressly carried flicker obligation. [L2 §7; CL §7; D §11, R9; I4 point 4]

The three reasons need these qualifications:

1. **Terrain complicates the question; it does not make every onset question impossible.** Heterogeneous systems can still have a global persistence or spectral threshold. Local activation spread does not prove the absence of a collective onset. The sound practical reason is that the unresolved *homogeneous* question is more directly isolated by a dedicated flat experiment. T0 could host it, but doing so would add a separately specified experiment to Flight 9.

2. **The finite-design caution is sound.** Extinct/surviving mixtures, initialization, horizon and the estimand matter. A finer grid alone cannot establish the thermodynamic character of a transition. Several sizes are not a logical prerequisite for every modest finite-design question, but stronger limit claims need an appropriate size/horizon design. Conditioning on survivors must be declared; it is not a neutral correction to the unconditional curve. [CL §§2–3; C §1.1′]

3. **No dependency is needed for the narrowed Flight 9 claim.** Do not assert, without a Flight 10 design in this packet, that no future coherence inquiry could depend on it. The defensible statement is that the current Flight 9 endpoints do not require onset continuity to have been resolved, and future claims must preserve that limitation.

Retain the outstanding question by name. Neither the new flat reference nor a repeat of Flight 8’s above-boundary criterion resolves the missing entering interval unless a new test expressly covers it.

## 9. Q7 — Fidelity on a terrain

**Disposition: REQUIRES CHANGE.**

The two-object separation and fresh T0 reference are sound directions. Specify whose threshold, whose edge and which estimand each comparison uses.

### 9.1 The threshold in the control is a skeleton object

The spectral crossing is the **zero-floor site-closure** comparator. Its lattice counterpart is a declared finite-horizon skeleton persistence threshold, with specified initializations, survival criterion, seed panel, grid and treatment of absent or multiple crossings. The positive-floor realization has activity even at g = 0; “the level at which anything persists” is not its literal absorbing-state onset. [C §§1.1′, 2.6, 2.9, 3.2–3.5; D §10.2]

Replace “governed by the best patch” with “determined by the leading mode of the spatial feedback operator, which may localize on a favorable patch.” Peak λ alone does not determine that mode; connectivity, patch size and neighboring values matter.

### 9.2 The heterogeneous closure does not generally predict an edge at local m = 1

The site closure implied by the proposed extension is

\[
p_i^{t+1}
=(1-p_i^t)\left[1-\exp\left(-\Delta t
\left[\eta_{\rm floor}+g\lambda_i\sum_j A_{ij}p_j^t/8\right]\right)\right]
+(1-q)p_i^t.
\]

At a fixed point, occupancy depends on the neighboring probabilities as well as λ. Equal local \(m_i\) need not produce equal occupancy. Accordingly, \(m_i=1\) is a **local homogeneous benchmark**, not the heterogeneous map’s predicted edge. [C §§2.4, 3.1, 3.5; derivation]

Retain the three reported comparisons in this corrected form:

| Comparison | Correct object and interpretation |
|---|---|
| Measured onset versus spectral crossing | Skeleton finite-horizon threshold versus the zero-floor closure crossing; report normalized and raw-g shifts and uncertainty. |
| Local m values on the measured edge | A spatial diagnostic on an explicitly defined edge, against 1 as a homogeneous local benchmark and against T0’s measured boundary. Neither reference is automatically a pointwise terrain prediction. |
| Observed occupancy versus site closure | Match object, floor and estimand. If comparing edges, apply the same declared edge-extraction rule to both maps and report their discrepancy. |

These remain fidelity reports. A poor comparison is published as such and does not become a new scored failure through the back door. [D §9; C §1.2′]

### 9.3 Define the edge and the temporal/statistical comparison

For the realization, declare an occupancy or excess-occupancy edge, connectivity convention, spatial resolution, and handling of empty/full/disconnected maps. A null-relative edge is not automatically the PD7 persistence boundary: Flight 8 already distinguished feedback detection from the transition. [C §4.9]

The deterministic closure predicts mean probabilities. A per-cell seed-median finite-tail map is a different estimand, especially under extinction or intermittent patch mixtures. I recommend reporting the seed-mean occupancy map for direct probability comparison, retaining medians for the separately declared structural endpoint if desired. If medians are compared to the closure, name the estimand discrepancy rather than calling the entire difference closure error.

Also freeze the site solver, selected branch, initialization, convergence tolerance and failure status. Distinguish a fixed-point comparison from comparison to the closure’s finite-time trajectory under matched initialization. A finite tail that has not equilibrated can differ from a fixed point without isolating a stationary closure error.

### 9.4 T0 is acceptable

Use Flight 9’s own flat arm at its declared size, horizon, grid, initializations and fresh panel. Carry its uncertainty and unavailable-boundary cases. Do not substitute Flight 8’s measured 1.521739 as a universal constant, and do not use the newly measured T0 value to retune scored tolerances. [D §9; CL §§2–3]

At matched effective gain, the two compositions on a flat terrain have the same kernel. That provides an implementation check. The newly measured finite-design boundary remains a scientific observation; fresh seeds or a changed size need not reproduce Flight 8’s exact numerical crossing.

## 10. Q8 — A pre-contract, noncanonical terrain probe

**Disposition: REQUIRES CHANGE.**

The probe is acceptable in principle under Mike’s permission, after his ruling on this return. A dated provenance paragraph alone does not preserve prospective claim grammar. Flight 8 §1.0 discloses a result-informed design decision and expressly limits later novelty claims; disclosure does not convert that decision into one made without outcome knowledge. [P §4; D §§10.4–10.5, 11; C §1.0]

### 10.1 Before any probe output

Place a short prospective declaration that fixes:

- the scientific target, structural/fidelity division, adverse outcomes, ND meanings and the claim limits settled under Q1;
- the candidate terrain/size/level/seed menu, purpose, maximum scope, retained outputs and stopping rule;
- which choices the probe may inform—resource pricing, feasibility and whether the specified terrains offer usable contrast—and which scientific rules it may not adapt to favorable results;
- code and terrain identities, stream roles and the complete provenance record to retain.

A resource-only benchmark need not await every numerical scoring detail. A probe inspecting the spatial outcome later scored must not be used to choose contour cuts, equivalence tolerances or aggregation rules because they rescue the observed result. If an outcome-informed scientific redesign is needed, identify it as such, obtain Mike’s ruling and establish a fresh validation boundary. An observed adverse result does not become fidelity or ND simply because it was inconvenient.

### 10.2 Resolve Interpretation 004’s timing explicitly

Point 4 says the successor contract must declare the flicker statistic, W, sampling levels and persisted information **before any data**. It does not say only canonical data. The current sequence—probe first, contract later—therefore requires an explicit resolution.

I recommend a **Mike-ratified pre-probe declaration** fixing those four items and Q5’s necessary censoring/undefined conventions, with Mike identifying its binding incorporation into the successor contract as satisfaction of the prospective obligation. Alternatively, he can make an explicit scoped ruling on the noncanonical probe. L2 should not silently infer an exemption or reduce “any data” to “canonical data.” This narrow requirement does not require the entire Flight 9 contract to be frozen before a design probe. [I4 point 4; D §§7, 10.4–10.5]

### 10.3 After the probe

Preserve every attempted configuration and outcome, including failed separation, with source, environment, terrain-array, stream and result identities. Record what was learned, what changed and why.

Use fresh canonical masters. Probe results remain design evidence and do not become calibration, held-out qualification or canonical observations by relabeling. Selecting terrains because the probe shows separation makes later inference conditional on those selected terrains. Fresh seeds can independently replicate the response on them; they do not make the selected contrast an unanticipated discovery or demonstrate generality across terrains. A broader claim requires genuinely reserved terrain cases or a narrower stated scope. [C §1.0; L2 §8; L2 design recommendation]

## 11. Q9 — Other matters that would prevent freeze

**Disposition: REQUIRES CHANGE.**

The following are additional design requirements, alongside the specific changes in Q1–Q8. Numerical values can be settled in the contract register; the meaning of the claims and the required information cannot remain ambiguous.

### 11.1 TC must distinguish near-face suppression from literal zero-collapse

TC currently uses a base **near** zero. That is not an annihilating face. Whether the product produces a low-occupancy patch while the rival produces an occupied patch depends on g, geometry, object and the declared edge; those outcomes do not follow from the base triples alone. [D §3.5]

At exact λ = 0, the carried realization still activates with probability 0.01 and has stationary occupancy \(a/(a+q)\approx0.0522823\). A literal zero-registration hole therefore does not occur in that rule. This exposes a correspondence that homogeneous positive-base Flight 8 did not adjudicate: PD1/PD7 say registration is impossible on an annihilating face, whereas the flight’s active-state/registration mapping and base-independent floor permit active events there. [C §§2.4, 2.6, 2.9–2.10; PD1, PD7; O §§5, 8, 10]

**Recommended scope:** retain the carried rule and describe TC as a near-face feedback-suppression contrast at declared gains; define “hole” operationally and disclose the exact-face limitation. The skeleton can display absence of reactivation at an exact zero coefficient after any initial activity lapses. That is rule conformance, not new empirical validation of zero collapse.

If literal absence of registration in the positive-floor arm is to be claimed, obtain a prospective rule/translation ruling. Do not quietly gate the floor by a base or mask floor-generated active events out of density; either changes the rule or the registration mapping. PD6 does not supply a free operationalization to do that.

### 11.2 Make discrete contours and replication informative

Smooth formulas sampled on a finite lattice can yield mostly distinct λ values. Treating each exact value as a contour can create singleton groups with zero within-group variance by construction. Freeze the bin/interpolation/tie rule, minimum membership, spatial coverage, weighting and minimum informative contrast.

State whether the endpoint is “score the seed-median map” or “summarize scores from individual seed maps.” They are different. A median map can combine features that no run exhibited. Preserve seed-level summaries sufficient to reconstruct the chosen calculation; do not retain only the final median map. Twenty dynamics seeds on fixed terrains do not constitute twenty sampled terrains. [D §§3.6, 10.3; Q1–Q2 requirements]

### 11.3 Declare spatial scale and margin geometry

For L = 50 versus 100, specify whether the change enlarges the domain, refines a fixed domain, or enlarges patches in lattice units. With a one-step Moore neighborhood, those choices alter terrain scale relative to interaction range. Pricing one larger lattice is not a continuum or finite-size scaling study.

TD’s “fixed total core area” needs a geometry-based definition and reference composition/control, or a composition-independent construction. An \(m_i\)-defined core moves with g and can differ between the two indices. Freeze all proposed occupancy cuts and report every registered cut; a realized margin ratio is a future observation, not guaranteed by the design-side geometry. No coherence claim follows from it. [D §§5, 10.3]

### 11.4 Carry M7’s principles, rebuild its concrete record graph

“Grammar unchanged” is sound for completeness versus readiness, valid adverse scientific records, passage of apparatus prerequisites and identity/authorization binding. It cannot mean reuse of the concrete F8 job graph. The supplied runner imports M2/M4/M6, names F8 paths and binds those modules’ record types and dependencies. [C §4.10; runner.py imports, frozen declaration and JOB_GRAPH]

Specify Flight 9’s own stage, jobs, authorizations, dependencies and record types. Bind terrain formula and base-array identities, composition, raw/effective controls and normalization, lattice geometry, object/floor, horizon/tail, seeds/streams, window convention, summary schema and evaluator/qualification identities.

Make flicker summaries and all required fidelity outputs explicit package reporting items, with coverage and validity checks. Their numerical scientific values do not gate a favorable verdict; missing required records prevent a claim of complete reporting. This is the direct lesson of Interpretation 004, not an optional enhancement. [I4 points 1–4]

### 11.5 Re-establish the statistical references actually used

The floor-only stationary occupancy carries analytically. Flight 8’s global-density bands, calibration tolerances and morphology thresholds do not automatically apply to per-cell terrain maps or a different L. Declare fresh uncertainty/calibration procedures for the chosen endpoints, with role-separated streams and predeclared precision requirements.

Specify whether composition arms or levels use independent streams or intentionally paired random numbers, and make the uncertainty method match that decision. Preserve the random stream identities for reproducibility. “Fresh masters” alone does not specify the dependence structure of the comparison. [D §§10.1, 10.3; C §§2.5, 3.4, 4.11]

### 11.6 Give adverse and unavailable results distinct paths

Before freeze, enumerate no contrast, no edge, saturation, insufficient contour coverage, finite-resolution ND, skeleton extinction, corrupted/missing summaries and closure nonconvergence. Distinguish a scientific adverse finding, scientific ND, unavailable fidelity comparator and apparatus failure.

Declare the precedence and aggregation of these states across all planned terrains, rules and levels. Preserve all of them in the package; do not drop failed terrains or select only favorable levels. Stopping or enlargement follows a prospective rule, not a post-result convenience. [C §4.10 as carried grammar; D §§3.6, 9–10]

### 11.7 Separate T0 implementation regression from scientific replication

The constant-array reduction in Q3 is an apparatus check. Rerunning Flight 8’s four tests under fresh seeds is a scientific consistency exercise whose finite-design tolerances and domain must be redeclared for the chosen grid, size and horizon. Do not silently import every F8 numerical tolerance into a changed design.

Specify its role: a valid adverse or ND scientific result is not automatically evidence of a coding defect, and repeated P1 passage still does not resolve the entering-interval continuity question. If a T0 boundary is unavailable, record the effect on reference-dependent reports explicitly. [D §10.2; FR §3; CL §3]

## 12. Decisions to record before the next stage

The next note should record Mike’s rulings on these recommendations, particularly:

1. The conditional claim wording and the choice between boundary compatibility and the stronger occupancy-map test.
2. The new evaluator’s statistical qualification, while retiring the obsolete morphology apparatus.
3. The gain normalization, floor/zero-face scope and exact flicker estimand.
4. The prospective probe protocol and Interpretation 004 timing resolution.

The contract can then complete the declared estimator, numerical resolutions, error targets, lattice scale, run budget and record graph. Nothing in this return requires adding coherence, within-cell heterogeneity or an onset-continuity experiment to Flight 9. The held third-order lattice-versus-ODE comparison and the two next-touch repairs retain their recorded status. [D §§11–12; CL §7]

## 13. Verification record and source key

### Checks performed

- Independently hashed the archive, manifest and all 23 payloads; checked counts, complete coverage, duplicate paths and the duplicate standalone instruction.
- Read the packet instruction first; compared v0.1 with v0.2 and confirmed that the scientific design text in §§1–9 and §§10.1–10.4 is unchanged.
- Reviewed the design against the included frozen contract, freeze record, relevant rulings, Overview, prior disposition and placed source.
- Calculated only analytical rule constants and finite binary-sequence examples used above. No terrain probe, lattice run, ensemble, qualification, canonical job or pytest suite was executed. No source or historical record in the packet was modified.

The packet contains no Flight 9 code, tests or observations to validate. Requirements for its future implementation are design recommendations, not claims of a completed build review.

### Source key

All paths below are the exact payload paths identified in the receipt table; section references use those received bytes.

| Key | Packet source |
|---|---|
| P | flights/mfa_fidelity/design/flight9/L1_TO_L2_F9_DESIGN_CONSULTATION_2026-11-12.md |
| D | flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_2.md |
| D1 | flights/mfa_fidelity/design/flight9/FLIGHT_9_DESIGN_NOTE_v0_1.md |
| C | flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md |
| FR | flights/mfa_fidelity/contracts/flight8/FLIGHT_8_FREEZE_RECORD.md |
| A | flights/mfa_fidelity/contracts/flight8/APPENDIX_A_OF_RECORD.md |
| CL | flights/mfa_fidelity/governance/f8_stage1/F8_STAGE1_CLOSE_RECORD_v1_0.md |
| I4 | flights/mfa_fidelity/rulings/F8_INTERPRETATION_004_FLICKER_OBSERVABLE_NOT_RECORDED.md |
| PD | flights/mfa_fidelity/rulings/PD_PARTICIPATION_RULINGS_PD1_PD7.md |
| N | flights/mfa_fidelity/rulings/NOTATION_SCOPE_RULING_v1_1.md |
| L2 | flights/mfa_fidelity/build_records/L2_F8_STAGE1_DISPOSITION_CONSULTATION_2026-11-12_RECEIVED.md |
| S | flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md |
| O | theory/overview/EE_emergence_overview_v1_8_1.md |

Source references to config.py, dynamics.py and runner.py denote the corresponding files under flights/mfa_fidelity/instrument/mfa_instrument/f8/ in the receipt. No document merely mentioned inside a payload but absent from this packet was independently consulted.

