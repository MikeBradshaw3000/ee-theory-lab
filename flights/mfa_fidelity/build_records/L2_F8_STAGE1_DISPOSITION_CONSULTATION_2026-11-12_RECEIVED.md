# L2 → L1 — Flight 8 stage 1: disposition consultation

**Date:** 2026-11-12
**Reviewer:** L2, adversarial source review
**Decision authority:** Mike Bradshaw
**Register:** disposition consultation on the supplied stage package; this document does not issue Mike's disposition, grant placement clearance, authorize new runs, or amend a frozen rule.
**Repository pin supplied:** `ee-theory-lab abb927995d92faa37ca654ee8f3651c48a27f2e2` (`abb9279`).

## 1. L2 finding and recommendation

**Retain the recorded P1 determination, PRODUCED. The frozen rule does not require NOT DISTINGUISHED on these data.** All four scored TestResult objects recompute exactly from the supplied canonical sweeps and calibration census. No internal identity mismatch or demonstrated execution-order violation was found within the supplied evidence. This is a qualified finding about the authenticated package and the computations it exposes; the ZIP does not permit an independent reconstruction of the complete canonical execution.

**The principal scientific limitation is T-S1c's registered domain.** It tests the sampled skeleton branch from the selected persistence boundary m̂_c upward. It does not test the substantial density increment entering that boundary. Its formal pass is correct; an assertion that this stage resolved continuity through the onset is unsupported. The domain was explicit before these data, in the contract, Interpretation 001, ratified declaration MP1-5, source, and tests. [C §§1.1′, 1.2, 4.11; I1 Consequences; R §C, MP1-5; E; T]

**My first-ranked disposition is qualified closure after narrow reporting and provenance completion:** preserve P1 PRODUCED and the existing canonical bytes; place the reported decision on the missing flicker observable; preferably complete the frozen M6 comparison supplement; clarify authorization 003's effective approval date; record the clerical corrections and remaining evidence limits. Mike can instead explicitly defer the comparison supplement and close with that additional reporting obligation carried forward. Neither choice retrospectively changes P1.

| Consultation request | L2 answer |
|---|---|
| Soundness of the chain | Internally coherent on the supplied bytes and declared dependencies; no determination-invalidating defect demonstrated. Full canonical provenance and trajectory replay remain outside this ZIP's evidence scope. |
| P1 / T-S1c challenge | PRODUCED is the correct frozen operational result. The incoming transition increment is outside T-S1c's domain. |
| Ranked disposition | Rank 1: qualified close after reporting completion; rank 2: qualified close with explicit additional deferral; rank 3: hold administrative closure without recoding P1. |
| Section 5 open items | D1 requires provenance clarification; D2 and D3 remain reporting obligations; D4 is clerical; D5 is next-touch maintenance; D6/D7 require precise evidence qualifications; D8 is the expected secondary morphology. |
| Claim language | A finite-design operational four-test result, with an explicit above-boundary continuity-test scope. No resolved continuity through onset, thermodynamic critical point, theory confirmation, or transferred lattice error-rate claim. |

## 2. Receipt, authority, and review scope

The receipt completed before execution verified the archive, its exact count of 104 payload files plus MANIFEST.txt, the manifest identity, and every payload hash. There were no missing, unlisted, duplicate, malformed, or mismatched payload entries. The packaged instruction is byte-identical to the earlier standalone attachment. The full 104-row receipt is `L2_F8_STAGE1_DISPOSITION_RECEIPT_2026-11-12.md` (SHA-256 `c85691f33811e7885a4868424b2dbdcc1d942c8879884b165cd5ddb26a0e328e`).

| Received object | SHA-256 |
|---|---|
| `f8_stage1_disposition_L2.zip` | `656cc29e5bc9197c0b14147c6add42efba703fdf63e90f9685ba6dbe8f0378ae` |
| `MANIFEST.txt` | `04d8248371a5ca44dbdec6d09e48459f8fdd963aae2630d7e9ba49b133dea6e1` |
| Disposition instruction packet [P] | `e162b1b5d2640f66eea505ffb97c0d9f1a6d6b93109cf01333ba3cbf75013afd` |

The operative authority is frozen Contract F8 v0.8.4, its freeze record, Interpretations 001–003, the build and governance ratification records, and the supplied governance/specification/authorization records. Historical revision notes within the contract do not override its operative sections. The unplaced Interpretation 004 described in the packet is not an identified committed authority at the reviewed pin. No unrelated Paper-project discussion or prior conversational assessment was used as a substitute for these sources.

Local computation used Python 3.12.14 and NumPy 2.3.5. It consisted of structural validators, identity and dependency checks, direct numerical replay, independent median/increment calculations, and independent audit-bound arithmetic. No canonical job, lattice simulation, or full pytest suite was run. Pytest was unavailable in the local runtime. The 859-pass canonical suite is existing supplied evidence, not a new L2 test run.

## 3. Soundness of the chain

### 3.1 Checks completed

| Check | Result |
|---|---|
| M7 BOUND_SOURCES: source/test files against cleared literals | 43/43 match |
| Separate runner and M7-test identities against placement | Both match |
| Authorization files against registry, and authorization body hashes | 3/3 match |
| Result envelopes: canonical encoding, schema, stage identity, authorization binding, granted job, decoded type | 31/31 match |
| Package items: filenames, file hashes, record-identity links, types, producer filenames, completeness/pass predicates | 29/29 agree |
| Production prerequisites, including their declared dependency bindings | 7/7 agree |
| Required prerequisite set against governance | Exact match |
| Authorization 003 binding to production-prerequisite manifest | Exact match |
| Governance/declaration, package-specification, registry, manifest, suite and placement internal validators | Pass |
| Stage-package body digest | Recomputes |
| Fixed gate/contract/declaration records available in the ZIP | 8/8 supplied records match; six other fixed records are absent from the ZIP |

The common stage identity carried by the authorizations and all 31 result envelopes is `6c0a5ec3df673924d3b37183a82c0f5d8573540ea36fdbf248f29b2090c71d01`. The package body identity is `905157cbda1f7561832dde87933291a0188c8a8a1a52b0e6f6c43c532e6baa94`. Matching a record-identity field to a package link is not the same operation as regenerating the underlying observations. [M7; GV; PS; AU1–AU3; PM; PK]

### 3.2 Order of acts

The supplied one-line Git-log export reports the following order, consistent with M7's declared dependency edges:

1. Placement/suite → governance, specification and adapter → authorization 001.
2. Canonical M-P1 known-answer qualification → M6 design → held-out → joined qualification.
3. Authorization 002 → apparatus work, calibration census and required supporting records → calibration tranche → production-prerequisite manifest.
4. Authorization 003 → skeleton census → skeleton stability → realization census → realization stability → P1 evaluation → stage package.

M7 checks the authorization, production prerequisites and predecessor jobs before execution. It specifically requires the corresponding canonical census to be committed before its stability job. The supplied binding records and chronology expose no contrary order. The chronology is supported by an L1-generated log export, rather than independently inspected Git objects. [H; M7 JOB_GRAPH and require_job_dependencies, source lines 2061–2078 and 2454–2515]

The audit-master numbers were prospectively fixed by the ratified role-prefix/date rule. `masters_for_date` performs integer arithmetic and collision checks; it does not consume an RNG stream. M7 gates audit execution after the required qualification/predecessor records. I therefore find no demonstrated violation from the master numbers being known prospectively. The precise statement is that the values were fixed prospectively and the reported first authorized audit consumption followed M-P1 qualification. The ZIP does not establish the absence of all earlier off-route stream use. [R A7/D-date; D §9; M6 source lines 195–208, 606–716, 882–896]

The packet's statement that each job ran once remains a session-history attestation. Final files and this one-line log cannot establish absence of earlier executions or replacements; the source supports output writing and whole-level reexecution. I found no evidence of outcome selection or unauthorized reruns. No such allegation follows from this evidence boundary.

### 3.3 Qualification and precision checks

The committed M-P1 qualification reports all nine classes at 100/100 exact verdict-and-cause matches, with zero cross-triggers. M6 reports 6,000 scored sweeps in each ensemble, all twelve classes complete and no halts. Recalculated one-sided binomial upper bounds agree with the reported values to floating-point precision:

| Quantity | Committed result / independent arithmetic check |
|---|---|
| Design: largest applicable-error upper bound | 0.01543373487675287, from 3/500 in off_band_unresolved |
| Held-out: largest applicable-error upper bound | 0.0182128517961066, from 4/500 in off_band_mixture |
| Held-out off_band_unresolved | 2/500; upper bound 0.012537605409670693 |
| Declared M6 cap | 0.10 |
| Pricing | 0 S_min rejections / 10,000; CP-95 upper approximately 0.00029952836, against nominal α_P = 0.001 |
| Skeleton calibration maximum MDD | 0.01222667281887262 |
| Realization calibration maximum MDD | 0.0018600974543979438 |
| Both MDD ceilings | 0.02; neither stop path triggers |

These are checks of reported counters, predicates and arithmetic; the 12,000 audit sweeps and 10,000 pricing simulations were not rerun. M6's applicable-error metric is not identical to exact verdict-and-cause agreement in every trial. Its qualification applies to the declared synthetic ensemble, not an established identical error rate on the spatial lattice. Zero observed pricing rejections also does not mean a zero underlying rejection probability. [KA; AD; AH; AQ; AP; CA; I2 point 10]

### 3.4 What the package's green flags establish

`complete=True` and `all_items_pass=True` implement the declared package predicates. The ratified specification uses `p1_recorded` for both completeness and pass of the P1 package item; M7 defines that predicate as canonical role, rather than a PRODUCED determination. Complete skeleton assessments can contain PASS, FAIL or ND. This intentionally permits valid packages with adverse scientific content. [C §4.10; GR G7; PS; M7 source lines 2206–2211]

The present P1 result is supported by the four-test replay, not inferred from the package flag. The flag also cannot discharge reporting obligations absent from the package alphabet, including D2 and D3.

### 3.5 Limits on an end-to-end assurance

Beyond the disclosed run files, level records and benchmark artifacts, the ZIP omits three authoritative gate records, three null-validation attempt/protocol records, the round-6 L2 clearance named by the placement record, actual Git objects, the pinned lock blob and installed canonical environment, and a full StageIdentity object. Appendix B lists the fixed missing inputs and their declared identities.

M7 derives the stage body from those inputs as well as the source/governance/adapter bindings; the supplied result envelopes carry its hash. Consequently, this review cannot independently reconstruct the canonical stage identity, establish append-only Git history, recompute observations from the omitted trajectories, or claim successful M7 canonical-reader acceptance. Direct decoding was used within that boundary. Absence from this ZIP is not evidence of absence from the canonical repository. [M7 source lines 350–469, 520–531, 957–1005]

**Chain ruling:** no determination-invalidating binding or order defect is demonstrated by the supplied record. Reliance on the frozen four-test computation is supported. An unqualified statement that L2 independently reproduced the complete canonical execution is not supported.

## 4. Adversarial reading of P1

### 4.1 Exact scored-result replay

| Test | Recomputed result |
|---|---|
| T-S1′ | PASS; m̂_c = 1.521739, grid index 13 |
| T-S1c | PASS; exact equality with committed TestResult |
| T-S2 | PASS; m̂_low = 1.521739; separation 0; Δm = 0.120126265992375 |
| T-R1′ | PASS; exact equality with committed TestResult |
| P1 | PRODUCED; cause None |

The three canonical sweep structural validators and the calibration-census validator pass. The committed P1 result's internal content hash also recomputes. These results use the supplied per-run survival/tail-density summaries; the absent trajectories prevent independent regeneration of those summaries. [SH; SL; RE; CA; EV; E]

### 4.2 The estimator and the partial-survival level

The packet's orientation table reports plain means. T-S1c scores seed medians. The relevant canonical skeleton-high values are:

| m | Survivors / 20 | Mean tail density | Median tail density |
|---:|---:|---:|---:|
| 1.326087 | 0 | 0 | 0 |
| 1.423913 | 7 | 0.00982912 | 0.004849 |
| 1.521739 | 20 | 0.14874434 | 0.1469342 |
| 1.619565 | 20 | 0.22624736 | 0.2260976 |
| 2.500000 | 20 | — | 0.5157292 |

At 1.423913, seven tail densities are zero and six non-surviving runs have positive tail density. That is compatible with Interpretation 001: extinction during the tail preserves positive pre-extinction contributions to the mean over the entire tail. Non-survival is not a license to coerce those observations to zero. [SH; I1 points 1–3]

T-S1′ requires at least 18 survivors at the selected level and every higher level. The 7/20 level therefore does not become the selected boundary. Both declared initializations select 1.521739; the low-initialization sweep has 4/20 survivors at 1.423913 and 20/20 from 1.521739 upward. This establishes the frozen sample criterion, not equality of underlying survival probabilities or the exact location of a thermodynamic critical point.

### 4.3 T-S1c on its frozen domain

Contract §4.11 specifies the range `med(m_max) − med(m̂_c)`. Ratified MP1-5 explicitly fixes the domain as m̂_c through m_max inclusive. The comparisons therefore begin with the pair m̂_c → the next level, not the pair entering m̂_c. Interpretation 001's Consequences expressly excludes a skeleton level with fewer than eighteen survivors. The source and its pre-existing domain test implement this scope. [C §4.11; R MP1-5; I1; E source lines 300–333; T source lines 128–143]

The exact canonical arithmetic is:

$$R = 0.5157292 - 0.1469342 = 0.368795,$$

$$f_J R = 0.25(0.368795) = 0.09219875.$$

The largest scored increase is the first one above the selected boundary:

$$0.2260976 - 0.1469342 = 0.0791634.$$

It is 0.21465421168942095 of the scored range, below 0.25, with headroom 0.01303535. Every scored increment is positive; the smallest is 0.0179752. No decrease is being disregarded by a calibration band. Those bands govern reversals, and no band is added to the upward-increase allowance.

**T-S1c therefore passes the frozen rule.** Describing that outcome with the contract's operational label, “consistent with a continuous onset at resolution s,” is correct only when its restricted domain and inferential limits accompany the label.

### 4.4 The strongest attack: the incoming rise is not tested

The conspicuous entering increment is:

$$0.1469342 - 0.004849 = 0.1420852.$$

That exceeds the frozen upper-branch allowance and is approximately 0.385269 of that branch's range. It is also approximately 0.275504 of the full-sweep median range. The apparent issue is not removed by choosing the median instead of the packet's orientation mean.

As a diagnostic only, I applied the same arithmetic starting one level earlier, at 1.423913. Even after enlarging the range, the allowance becomes 0.12772005, still below 0.1420852. That altered-domain diagnostic returns `ND: continuity unresolved at grid resolution (1.521739)`.

**This counterfactual is not a rescore of the committed stage.** It identifies a limitation in the frozen assay: the entry interval that attracts the continuity question is outside the test's domain. Substituting the enlarged domain after seeing the data would change the instrument. Nor does the diagnostic establish a discontinuity; a steep continuous rise could give the same result. A future test of continuity through onset needs a prospectively declared domain and resolution.

### 4.5 Other tests and the stability panel

The realization's medians are positive and strictly increasing across all 24 levels. Its minimum median is 0.0665394; the endpoint is 0.5380014; the range is 0.471462. The permitted increase is 0.1178655, whereas the largest observed increase is 0.0303636, from 1.326087 to 1.423913. Its range fraction is 0.0644030696005191, with headroom 0.0875019. There are no reversals. Thus T-R1′ passes without any reversal being disregarded. [RE; E]

T-S2 passes because the two selected skeleton boundaries coincide, well within Δm. Its interpretation remains restricted to the two declared initializations, horizon and panel. It is not used as a proof of continuity or absence of bistability across all states. [C §1.1′ and §4.11; SL; EV]

The independent stability skeleton-high panel reproduces index 13 / 1.521739, and the stability realization returns T-R1′ PASS. Those are the registered Interpretation 003 criteria. Skeleton-low is not separately replicated on that panel, so this is not a second independent execution of the entire four-test P1 conjunction. [I3 points 6–8; SS; RS]

### 4.6 Fidelity evidence stays visible

The reported boundary shift is +0.521739 from the homogeneous mean-field crossing and approximately +0.380291 from the pair value. At the selected boundary, the skeleton median is approximately 0.146934, compared with approximately 0.313988 and 0.252376 for the two closure branches. The realization's steepest-ascent level is 1.423913, 0.097826 below the selected skeleton boundary and approximately 0.247413 above the closure inflection. These are reported fidelity comparisons and do not gate P1. [EV; C §1.2′]

These discrepancies must not be described as independent discovery or confirmation of a lattice/closure mismatch already exposed in the pre-freeze probe. The frozen provenance paragraph explicitly records that prior knowledge and the resulting claim-grammar decision. [C §1.0]

## 5. Cross-platform replay qualification

Full `evaluate_p1` reproduces the four tests, determination, selected boundary, Δm, boundary shifts and steepest-ascent diagnostic. It does not reproduce the entire canonical evaluation record byte-for-byte. The only changed top-level fields are `fidelity`, `publication_sha256`, and `result_sha256`. Within fidelity, only the two closure-comparison tables differ; each has two differing numerical entries.

| Table | Maximum absolute local/canonical difference |
|---|---:|
| `skeleton_vs_rho_sk` | 5.551115123125783 × 10⁻¹⁷ |
| `realization_vs_rho_re` | 1.1102230246251565 × 10⁻¹⁶ |

| Identity | Canonical record | Local recomputation |
|---|---|---|
| Closure publication | `be8239128b62b87f24909082626c8c77ef28000acdbb0aa85358b3ac56e10e6b` | `7293211a9013bf3d4b9494c666a77f0c786f431ee9c97895034191f4003148aa` |
| P1 result | `42faa231c1aeee4775a5161354a2e1cbd6ead1656af57a7d361d35d653fced43` | `7521e9ea0fc01c3b1c38c0c66cc6068920eb097cd9f79dd901e50d31dc901ea9` |

These differences agree with the disclosed exp-derived platform sensitivity; they occur in non-gating comparisons. On this machine, M5's Appendix A binding check passes with maximum absolute deviation 0.0 against the supplied Appendix A. Ratified M5-6 allows the stated 1e-12 absolute binding tolerance for the designated numerical fields while retaining exact identity/level requirements. No canonical record was replaced with the local result. [R M5-6 and §E.9; CL; EV; P §4]

## 6. Rulings on packet §5

The closure requirements below are recommendations for an accurate stage disposition. They do not add retrospective P1 predicates.

| Item | Bears on P1 determination? | Bears on disposition / record? | Required treatment for the recommended close |
|---|---|---|---|
| D1: authorization 003 prepared before ruling | No invalidation demonstrated, conditional on approval and commitment preceding use | Yes: authority provenance | Preserve bytes; identify drafting, actual ratification, commitment and first authorized use in an append-only note |
| D2: flicker statistics absent | No: explicitly secondary, never P1 | Yes: frozen reporting duty remains unfulfilled | Place the reported omission/deferral ruling and a traceable successor obligation; make no flicker claim |
| D3: job-0 lattice/E supplement absent | No: not an M6 qualification prerequisite, P1 condition, or package predicate | Yes: outstanding reporting commitment | Prefer completing the frozen supplement; alternatively record Mike's explicit deferral/waiver |
| D4: commit-message errors | Neither changes scoring nor bound data | Clerical clarity | Append errata; retain historical records |
| D5: next-touch comment/docstring repairs | No | Carry-forward maintenance only | Preserve the exact next-edit obligations; perform them when those files are next edited |
| D6: suite skips/runtime | No demonstrated failed gate or scoring defect | Evidence qualification | Preserve the formal suite result and unknown skip identity; resolve if stronger test-execution assurance is claimed |
| D7: unrelated dirty paths | No defect demonstrated from global dirt alone | Provenance qualification | State the protected read surfaces and limits; do not claim the entire tree was clean |
| D8: M4 NOT_PRODUCED | No effect by explicit jurisdiction | Reporting distinction | Keep the secondary label separate from P1; note no insertion/final-set obligation remains in this case |

### D1 — preserve the authorization; clarify when authority became effective

The packet says authorization 003 was written November 9, ratified “as drafted” November 10, committed thereafter at d7af16c, and unused before commit. Advance preparation is compatible with later valid approval. However, `AUTHORIZATION_003.json` has `issued=2026-11-09`, and its helper source explicitly labels November 9 as “Mike's ruling.” That is a provenance discrepancy, not merely an operating-system file timestamp. The one-line log confirms a November 10 authorization commit before the scientific-record commits, but does not expose the claimed explanatory full commit body. [P D1; AU3; A3SRC source lines 18–19; H]

Before the recommended close, bind an append-only clarification to authorization file SHA-256 `1413d3b74731e7ea96b1825b5ff1acf5ce9a0a5f01d718aa2d91d925acbee7bb`, distinguish draft/issue-field date from actual approval, and identify the approval → commit → use sequence. If the full commit body already does this, cite it explicitly. Do not edit the authorization or registry to make their historical bytes look cleaner. On the disclosed sequence, no rerun or change to P1 is warranted.

### D2 — an omitted required observation remains an omission

Contract §1.3(b) says the flicker run-length statistics are recorded, not tested. “Not tested” does not mean optional. Placed M1 stores global counts/densities and summaries; those aggregates do not determine individual cell run lengths. No placed flicker-statistic definition, output field, or record exists in this package. An improvised aggregate substitute would not discharge the named observable. [C §1.3; DY source lines 94–103, 146–151]

The packet reports Mike's November 8 decision to carry the observable to a successor through an unplaced Interpretation 004. The disposition should put that decision of record as an explicit accepted omission/deferral: identify the missing observable, its lack of a P1 predicate, the unavailable inference, and its successor treatment. It must not retroactively declare the statistic present or all contract reporting fulfilled. This documentation can leave the frozen contract and scored records intact.

### D3 — complete or explicitly defer the frozen descriptive comparison

Interpretation 002 point 9(b), generator declaration §8, and ratified M6-10 freeze the comparison method and n_cmp=200. The job-0 realization census now supplies the lattice inputs. The supplement itself is absent. The wording gives no explicit hard stage-close deadline and expressly makes it non-prerequisite for M6 audits; I do not invent a hidden scoring or package gate. It nevertheless remains a reporting commitment. [I2; D §8; R M6-10]

The preferred supplement covers all 24 common pass-1 levels, comparing the 20-seed lattice realization's 1,000-tick tail mean and sample SD with 200 unmodulated E replicates per level. It reports signed mean and SD differences, surrogate/lattice SD ratio with an explicit undefined case, estimator precision, and the lack of spatial dependence in E. The declared stream is `SeedSequence([820261102, 1, level_micro, replicate])`. The source provides the surrogate-side method at `audit.py::surrogate_level_stats`; the joined report must demonstrate those exact frozen settings. It supplies no new universal variance bound, insertion-level coverage, or license to retune the generator. [D §8; M6 source lines 1014–1037]

If Mike chooses closure before this supplement, the close must expressly defer or waive it, identify its owner/successor treatment, and retain the original obligation's provenance. The M6 synthetic audit result cannot substitute for a missing lattice/E comparison.

### D4 — append errata

The manifest's correct filename is `PRODUCTION_PREREQUISITES.json`; commit 2dd54b5's message uses a different name. The actual file and its bound identity agree. Commit ddd4f6d's message says the cross-platform construction-bound difference begins at the twelfth significant digit; the packet corrects that to the tenth. I did not rerun pricing and do not independently certify that digit position; carry the latter as L1's explicit correction. Neither erratum changes a threshold, hash binding or P1 result. Preserve the old commits and add an erratum. [H; PM; P D4]

### D5 — retain the actual next-touch conditions

Ratification §E.8 requires correction at the next edit of each named test file. The M6 direct-DIP test still overstates that it forces w=8; the M-P1 below-boundary-rise test still contains a stale zero-survival comment while its constructed case uses twenty survivors. Their executable behavior is not changed by those comments. The supplied placement history identifies other files as the intervening touches and exposes no triggered-but-ignored next-edit event for these two files. Carry the obligations; do not force an otherwise unnecessary source edit merely to close this stage. [R §E.8; T; TM6; PL]

### D6 — record what the suite evidence actually says

The supplied suite record reports 859 passed, 3 skipped and zero failed on the placed runner/test identities. Its validator permits nonnegative skips and does not require a zero-skip suite. The placement note records zero errors and 24,788.21 seconds (6:53:08). The full transcript and skipped node IDs are not in the ZIP. The directory-symlink test is a plausible third skip because its source explicitly skips when symlink creation is unavailable; that is not an established identification of the historical skip. The runtime's cause is also unknown. [SU; PL; M7 source lines 571–575; TM7 source lines 849–857]

Preserve those limits. If a close claims that every critical check executed, recover the original skip identities/reasons or obtain focused canonical evidence for the unresolved check, clearly labelled as new evidence. An automatic seven-hour full-suite rerun is not warranted solely by this gap. This review does not replace the supplied canonical suite attestation.

### D7 — the rule protects a specified surface

M7 checks a named source/governance/fixed-record/clearance surface for committed byte equality; authorization history and prerequisite/dependency reads have additional protections. It does not require a globally clean repository. The approximately 115 unrelated legacy paths therefore do not by themselves invalidate P1. The environment gate reads its lock from a pinned Git blob, rather than trusting a dirty working-copy mirror. [M7 source lines 386–469, 492–496, 902–919, 1584–1616; ENV]

The historical inventory and its nonintersection cannot be independently reconstructed from this ZIP. Record the qualified account that those paths did not alter the protected read surfaces. Do not demand deletion of unrelated work or say that the whole tree was clean.

### D8 — the expected secondary morphology is present

The realization morphology is `NOT_PRODUCED / no_null_consistent_phase`, rule 2, with all 24 pass-1 levels S, router P2R-1, and no insertions. Its `final_set_identical_to_pass1=True` and `final_set_obligation=discharged_identically` implement Interpretation 003 exactly. The dense reference is likewise all-S / NO-NULL-PHASE. [MO; DR; I3 points 1–3]

Contract §1.3(a) preregisters that expectation; §4.7 explicitly bars using M4 to determine P1. Retain the underscore-bearing M4 label and the separate P1 PRODUCED result. There is no unresolved insertion obligation for these observations and no remedial run follows from this secondary label.

## 7. Ranked dispositions for Mike

### Rank 1 — retain P1 and close after narrow reporting completion

Accept the frozen operational determination and complete a qualified administrative close after placing the D2 omission/deferral decision, producing the D3 descriptive supplement, and recording D1's authority chronology and D4's corrections. Carry D5's next-touch obligations and the precise D6/D7 evidence qualifications. Identify the original package and this consultation by hash.

This provides the fullest available reporting record without changing the scientific experiment. It licenses the finite-design four-test claim and the reported secondary morphology/fidelity comparisons. Because D2 remains an accepted omission, it still does not license “every original contract deliverable was fulfilled.” It also does not resolve continuity through onset.

### Rank 2 — qualified close with the D3 supplement explicitly carried forward

If Mike elects not to wait for the supplement, close with the same P1 result and claim limits, plus an express disposition of D3 as deferred or waived. Preserve both missing reporting commitments by name and identify their successor treatment. This is available because neither is a P1 predicate and the D3 text does not impose a hard closure deadline.

The P1 claim is unchanged. The reporting record is less complete about how the audit surrogate compares with the spatial lattice. The close must not imply that the missing comparison was performed or that the synthetic qualification transfers its error rate to lattice runs.

### Rank 3 — hold administrative closure while retaining the recorded result

If Mike requires resolution of the reporting or provenance gaps before accepting any qualified close, hold closure while those records are obtained. An unqualified independent execution assurance would additionally require the omitted provenance/run evidence and the canonical environment or an appropriately defined audit. This hold is an administrative/evidentiary status; it is not a replacement P1 determination.

A successor can address the incoming transition interval, resolution, horizon or size dependence with prospective criteria and fresh authorization. No such work is authorized by this consultation.

### Dispositions unsupported by this record

- Replacing P1 with NOT DISTINGUISHED by expanding T-S1c's domain after observing these data.
- Replacing P1 with NOT PRODUCED because a non-gating secondary observable is missing or because M4 carries its expected NOT_PRODUCED label.
- Treating the package's all-items-pass flag as full contract discharge, proof of onset continuity, or confirmation of the theory.
- Treating acceptance of a finite operational signature as automatic clearance of held heterogeneous, Regime II/Ψ, or lattice-versus-ODE work.

## 8. Claim language

### Strongest supported sentence

> Under Flight 8's frozen four-test rule, the homogeneous 50×50 lattice at a 3,000-tick horizon, 1,000-tick tail, declared twenty-seed canonical panel and twenty-four-level grid returned P1 PRODUCED: both declared skeleton initializations selected the finite-horizon persistence boundary m̂_c=1.521739, the sampled skeleton branch from that boundary upward satisfied the registered continuity-compatibility criterion, and the positive-floor realization satisfied its registered positivity, monotonicity and continuity-compatibility criteria across the sweep.

The following companion limitation should travel with that sentence:

> T-S1c does not test the density increment entering the selected boundary; its pass does not establish continuity through the onset.

### Nearest stronger sentence not supported

> Flight 8 resolved the skeleton's onset from zero through m=1.521739 as continuous at this grid resolution.

That sentence attributes discrimination to the incoming interval the frozen test does not score. A still stronger statement that the lattice has demonstrated a continuous transcritical critical point is also unavailable: the selected value is a finite-horizon sample criterion, without the registered size-scaling, infinite-time or geometry evidence such a statement would require.

Any paper-facing account must also preserve the pre-freeze knowledge disclosure, publish the signed closure-fidelity discrepancies, identify D2/D3's reporting status, and keep M6's surrogate qualification in its synthetic-ensemble scope. The contract expressly excludes theory confirmation/refutation, heterogeneous-lattice claims, Regime II/Ψ conclusions and reopening E1 verdicts. [C §§1.0, 1.1′, 1.2′, 1.4; I2 point 10]

## 9. Recommended close record

The next concrete record should identify this consultation, the original stage package and P1 identities; record Mike's selected disposition; state P1 PRODUCED with the domain limitation; distinguish package completion from discharge of all reporting duties; and record D1–D8's dispositions. Under Rank 1 it should attach the identified comparison supplement and place the reported flicker deferral. It should preserve the canonical output files and all frozen criteria.

No scored repair, same-stage retuning, or scientific-result replacement is supported by this review. The remaining decision is Mike's choice of administrative disposition and acceptance or resolution of the stated reporting/evidence limits.

## Appendix A. Source register

All paths below are relative to `flights/mfa_fidelity/`, except H, which is at the archive root. Bracketed source codes throughout this report refer to this register. These are the reviewed bytes; the receipt separately enumerates all 104 payload identities.

| Code | Reviewed path | SHA-256 |
|---|---|---|
| C | `contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` |
| F | `contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` |
| I1 | `rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` | `6bf7304fd3ee287c799a4bd3a2692bb0857655861984b87cd46bf8408fde8d86` |
| I2 | `rulings/F8_INTERPRETATION_002_M6_SUSTAINED_GENERATOR.md` | `198d2991dd12168cd192d604e39e9192cceddae7a93812477fc72a4dfeb21034` |
| I3 | `rulings/F8_INTERPRETATION_003_MORPHOLOGY_SCOPE_AND_STABILITY_PANELS.md` | `6ebf0ad3efbe8e0e74b45e63d5f6ba550441897f3ff6898749230c064c993e9e` |
| R | `governance/f8_stage1/F8_STAGE1_RATIFICATION_RECORD_v1_0.md` | `cdedfcb4540d950be69695b589b3f8cc8b5164278b7d57e850eb7ff8b601346b` |
| GR | `governance/f8_stage1/F8_GOVERNANCE_RATIFICATION_RECORD_v1_0.md` | `e38b37553f261ab1ff03c0be6857688384c891fe4cbf038eae5adf18dd940dd1` |
| D | `build_records/F8_M6_GENERATOR_DECLARATION_v0_3.md` | `c73980585fc238209453ebadb4707d961e41d77b7970435e8ce4113298868e47` |
| P | `build_records/L1_TO_L2_F8_STAGE1_DISPOSITION_PACKET_2026-11-12.md` | `e162b1b5d2640f66eea505ffb97c0d9f1a6d6b93109cf01333ba3cbf75013afd` |
| M7 | `instrument/mfa_instrument/f8/runner.py` | `703c20292a0ffb1eec3325063021b4f0b80a417d01a4eaccc52d4cd1473cf1de` |
| E | `instrument/mfa_instrument/f8/evaluator.py` | `61179c7670ea8db30471d0087baaffb287868258a28bfa0181e25f7648499c3a` |
| CL | `instrument/mfa_instrument/f8/closure.py` | `9452dd11396350abfcbff4c48133a49cf31bac65879c34a254142d97300f3278` |
| DY | `instrument/mfa_instrument/f8/dynamics.py` | `cc663dd3c14197a8b0fdd92c8421a9a0fc13b9d41e32043266f243a0c827d72b` |
| M6 | `instrument/mfa_instrument/f8/audit.py` | `81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e` |
| T | `instrument/tests/test_f8_mp1.py` | `f9abdd8e657ba917d22e665488de16b8cef80d4a5db2c511861905b551667e1d` |
| TM6 | `instrument/tests/test_f8_m6.py` | `808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca` |
| TM7 | `instrument/tests/test_f8_m7.py` | `47b7a25c814390dc493f194ef1ba2ab6f97251559c8cb9f9e7df2d67f786b29e` |
| ENV | `instrument/mfa_instrument/gates/gate_b/environment.py` | `d81b49cea301f031f0a5c94bae91a27c13bb4fde06b63d5d6f1484acc9726c87` |
| GV | `governance/f8_stage1/F8_GOVERNANCE.json` | `889a76646c4d8eb5590b1631d43de4c91b14d0a735d300723271779a6c9cfba5` |
| PS | `governance/f8_stage1/PACKAGE_SPECIFICATION.json` | `0738d35ee0a30aefbc69b30476a7e486ba3a99f2cd8511fa10a523dff5a1cd4e` |
| AU1 | `governance/f8_stage1/AUTHORIZATION_001.json` | `fd7ae15748982f0620eb9637979b2d9dd5586987385ade17f1501f2ad1f3d0a3` |
| AU2 | `governance/f8_stage1/AUTHORIZATION_002.json` | `111c5ee83d6c30a36220af6ecf48d45507c459124cdf21b044f76c7a78b5852c` |
| AU3 | `governance/f8_stage1/AUTHORIZATION_003.json` | `1413d3b74731e7ea96b1825b5ff1acf5ce9a0a5f01d718aa2d91d925acbee7bb` |
| A3SRC | `governance/f8_stage1/make_f8_authorization_003.py` | `c81a637ba57e0d1ba5a7636c7f89d3539cfeca2f3d2c072c995620989c6fb07b` |
| PM | `governance/f8_stage1/PRODUCTION_PREREQUISITES.json` | `e03084c3dbdd59b6281abf32c7e96a6385b7d5fa404613d0f09d9c7f710b8592` |
| PK | `governance/f8_stage1/prerequisites/package/stage1_package.json` | `71ffee2bbc6db0f99227311471f9cb41b2574e472d1fdc953a644d6595cc050e` |
| KA | `governance/f8_stage1/prerequisites/package/mp1_known_answer.json` | `12d983544f653dbc290225f5db7da5eac3a8ef2bbd2af993ad2d9ce1f5adf598` |
| AD | `governance/f8_stage1/prerequisites/package/m6_design_audit.json` | `96a1e497027b491af6e78ad51268191b39650e069883cdeae3a25695f4937475` |
| AH | `governance/f8_stage1/prerequisites/package/m6_held_out_audit.json` | `002d276c0033ab47da82ff2f63e8077d2f32fd53ea10416b0f7f6ec57deb3b39` |
| AQ | `governance/f8_stage1/prerequisites/package/m6_audit_qualification.json` | `29168ab78238e7b6eb848f122b32e35adbd5073864ea600f0283261dd4f76959` |
| AP | `governance/f8_stage1/prerequisites/package/m6_price.json` | `0cad5161eb35f8fd3d7d465db252bf8905a73ed59df9a277a0919898d89edfb6` |
| CA | `governance/f8_stage1/prerequisites/package/calibration_census.json` | `91aebc07a80fab79a852f4bb701570b15b7409f8b785928821f91cd17ac5721c` |
| SH | `governance/f8_stage1/prerequisites/package/skeleton_high_sweep.json` | `5971275f9692da6874286328b747b23d5350aea3eca52fae7ac78311654388c8` |
| SL | `governance/f8_stage1/prerequisites/package/skeleton_low_sweep.json` | `764b3025c5f3708b024a933f421b598ba37f9327666320b34d55f356d98b0e79` |
| RE | `governance/f8_stage1/prerequisites/package/realization_sweep.json` | `cea7a4adf1acb4930c8a2bbf7535679559ee4caf17b53e47cb46f6447231aec7` |
| EV | `governance/f8_stage1/prerequisites/package/p1_evaluation.json` | `51489c7e97730ae0f51c0bc5007219f3ea7e46ec7317dc963247f9ba70440063` |
| SS | `governance/f8_stage1/prerequisites/package/skeleton_stability.json` | `33882615a5fe57fed1680f7e7871a19a760ddb325c30697c66c21b7c9fb85026` |
| RS | `governance/f8_stage1/prerequisites/package/realization_stability.json` | `37068b2e99d4fbaec33547cb1cdb6f96bc0984468225cd88927123c087d2e870` |
| MO | `governance/f8_stage1/prerequisites/package/realization_morphology.json` | `ea8a64ec5b4e2f0b9037ab2e19913f81076ef8a38af127f21eebfa066ba084aa` |
| DR | `governance/f8_stage1/prerequisites/package/dense_reference.json` | `5d6d1ffb00497d930c3192ab623975cc1378708603b716d26f2a36bbab6493b4` |
| PL | `build_records/F8_M7_PLACEMENT_NOTE_2026-11-04.md` | `bbef0dd9f22aa579be98fcdef43836743b436a1379c72ad08fc6e9548d7343a9` |
| SU | `governance/f8_stage1/M7_SUITE_RECORD.json` | `b4ce66f6dd594fcde54c5dc43d9c1b3d25bdb1c587b1008e47409038eb12f27c` |
| H | `GIT_LOG_d4994a5_to_abb9279.txt` | `3012b5893dca1b4edfce4d3e4a4ba7d8e5d1ade1c73fc5600453274ee9bcc704` |

## Appendix B. Fixed inputs not supplied in this review ZIP

The following identities are declarations found in the supplied source/placement record, not hashes newly verified from those absent files.

| Repository-relative input | Declared SHA-256 |
|---|---|
| `flights/mfa_fidelity/gates/gate_a/GATE_A_AUTHORITATIVE_RECORD.md` | `719a9706f34e6c08119993f1826242939e6a2331fc77cf50a61c769d2710ca74` |
| `flights/mfa_fidelity/gates/gate_b/GATE_B_AUTHORITATIVE_CERTIFICATION_RECORD.md` | `940d88a426d9530449d4c9d93d4a23085d354b678e2229edcf849806f6685883` |
| `flights/mfa_fidelity/gates/gate_r0/GATE_R0_REGISTER_CLOSURE.md` | `59fd2a54a344f994346001eab2ec14b03357018536e3386318138df079e6e741` |
| `flights/mfa_fidelity/build_records/F8_M3_NULL_VALIDATION_ATTEMPT1_FAILED_2026-10-27.json` | `a95509d3e809d70ba1d8977735ff88868d02ea3ac961305a70886f1128ce28ff` |
| `flights/mfa_fidelity/build_records/F8_M3_NULL_VALIDATION_PROTOCOL_ATTEMPT2_RATIFIED_2026-10-27.json` | `834a788bd39ee77123260d1023bc29f9343c684725004f36339a0be97ee2bfa4` |
| `flights/mfa_fidelity/build_records/F8_M3_NULL_VALIDATION_ATTEMPT2_2026-10-28.json` | `b10a9d5a89e43978a756d704e2e730bb8cba69953f82d03fa52e3e715dc4741e` |
| `flights/mfa_fidelity/build_records/L2_F8_M7_ROUND6_REVIEW_2026-11-04_RECEIVED.md` | `a02cfd037db766c89ec8240cedba77a744b022f9de7a7d2880016913c283e2be` |
| Git blob `4d9a622:cycle3/requirements.lock.txt` | `c10e02c5db497570ffeb45dc92857fcc633cb38364858a35458096950d02de7c` |

Other absent execution evidence includes the full canonical StageIdentity body, Git objects, the installed pinned environment, 168 level records, 6,720 run files, benchmark artifacts, and the full suite transcript/skip list. Their absence bounds this consultation; it does not establish a canonical failure.

## Appendix C. Computation record

Executed: archive/manifest receipt; source and record-binding validators; all supplied envelope/package/prerequisite cross-checks; canonical sweep and calibration structural validators; the four P1 functions and full evaluate_p1; independent survival/median/increment calculations including the clearly marked altered-domain diagnostic; M5 Appendix A binding; independent CP-bound arithmetic from committed audit counters.

Not executed: canonical M7-reader acceptance, lattice runs, M6 ensembles, pricing simulations, known-answer qualification simulations, the canonical pytest suite, or independent Git/history/environment reconstruction. No original package file or frozen rule was changed.

End of L2 disposition consultation. Decision authority remains with Mike.

