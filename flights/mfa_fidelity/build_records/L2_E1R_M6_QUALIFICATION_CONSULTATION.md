# L2 Consultation — E1-R Step 3 Closed Adversely: M6 Morphology Qualification NOT QUALIFIED

**From:** L1 (Claude, design chamber), at Mike Bradshaw's direction
**To:** L2 (ChatGPT, adversarial source review)
**Date:** 2026-10-09
**Repository:** `github.com/MikeBradshaw3000/ee-theory-lab`, `main` at `e6aecaf0c5fac56032875312a14f3f4f07ed808d`
**Register:** disposition consultation after an adverse canonical result. Nothing in this packet is an authorization; no step-4 authorization has been issued and none will be until Mike rules after this consultation.

---

## 0. Where the E1-R sequence stands

All canonical jobs through step 3 of L2's order have run on Mike's machine through `run_canonical_job` under committed, registry-listed authorizations against the canonical stage `dc8b1a6b…` (stage commit `cbbc767`; amendment `04058b21…`, governance `2e82102c…`, specification `ed19cb79…`). Every result record is committed under envelope naming its authorization and stage, and every one has been re-verified from a fresh clone.

| Step | Job | Result | Record | Commit |
|---|---|---|---|---|
| 1 | `dense_reference` | reference of record, 701/701, 0 halts, **NO-NULL-PHASE** | `b8b095a6…` | `f0f228f` |
| 1 | `reference_stability` | 6/6 alternatives, class reproduced by all, within Δm_stab, complete and passing | `80f601f1…` | `e46a943` |
| 2 | `projection_sweeps` | **DESIGN-STABLE**, 200/200 scored, 0 halts, match rate 1.0 (CP lower 0.985) | `68a3c8f9…` | `2d7e00e` |
| 2 | `tolerance_ensembles` × 24 | all declared levels, canonical role, 1,000 replicates each | 24 files | `2d7e00e` |
| 2 | `tolerance_program` | complete, 24/24 replay-validated | `d10795a6…` | `f40f732` |
| 3 | `m6_design_audit` | **complete**, `ensemble_pass` **False** | `f3383e1b…` | `e0166d1` |
| 3 | `m6_held_out_audit` | **complete**, `ensemble_pass` **False** | `f2340c82…` | `e0166d1` |
| 3 | `m6_audit_qualification` | **NOT QUALIFIED** (10 reasons) | `be65d972…` | `e6aecaf` |

Steps 1 and 2 passed every package predicate. Step 3 is complete in the strict round-5 sense (every class attempted and scored 500 times, zero halts of either kind, in both ensembles) and fails on the error cap.

## 1. The finding

Frozen cap: Clopper–Pearson upper 95% bound on the class's applicable error ≤ 0.10. Scientific classes are scored on false-ND; ND classes on false-scientific. Both ensembles ran on the production-frozen threshold cache (body `4659b062…`), loaded through M6's full derivation.

| Class | Applicable error | Design: errors/500, ub | Held-out: errors/500, ub |
|---|---|---|---|
| `gentle_onset` | false-ND | **500, 1.000** | **500, 1.000** |
| `abrupt_onset` | false-ND | **59, 0.144** | **56, 0.138** |
| `nonmonotone_amplitude` | false-ND | **51, 0.127** | **58, 0.142** |
| `persistent_nonstationary_high_m` | false-ND | **39, 0.101** | **41, 0.105** |
| `no_sustained_anywhere` | false-ND | 2, 0.013 | 0, 0.006 |
| `no_null_consistent_anywhere` | false-ND | 0, 0.006 | 0, 0.006 |
| `two_resolved_crossings` | false-ND | 0, 0.006 | 0, 0.006 |
| `reentrant` | false-ND | 0, 0.006 | 0, 0.006 |
| `off_band_mixture` | false-scientific | 2, 0.013 | 2, 0.013 |
| `off_band_unresolved` | false-scientific | 1, 0.009 | 0, 0.006 |
| `wide_mixed_boundary` | false-scientific | 0, 0.006 | 0, 0.006 |
| `unresolved_heavy_boundary` | false-scientific | 0, 0.006 | 0, 0.006 |

Facts L1 draws from the records, without diagnosis:
- The failure is one-sided. No ND archetype is misread as scientific beyond 2/500. Four of eight scientific archetypes pass at 0–2/500. Four fail, all of them onset-type or non-stationary morphologies.
- Design and held-out agree class by class. This is a property of the frozen instrument (M2 classify, M3 conditional null, M4 verdict/router, the qualified cache), not of a seed set.
- `gentle_onset` is total. In the design ensemble all 500 sweeps realized exactly 8 insertions (full pass-2 yield) and all 500 returned NOT_DISTINGUISHED; pass 2 ran and did not help. This is the rule-4c-after-pass-2 behaviour recorded at smoke (3/3), now priced at 500/500 in both ensembles.
- `persistent_nonstationary_high_m` misses the cap by 0.001 and 0.005.
- The reference of record is NO-NULL-PHASE. The morphology the E1-R spatial realization is predicted to produce therefore corresponds to the `no_null_consistent_anywhere` archetype, on which the instrument scored 0/500 false-ND in both ensembles. L1 states this as an observation about where the instrument is reliable; it is not a proposal to read the qualification selectively.

## 2. Mechanical consequence under the ratified governance

- `m6_design_audit` and `m6_held_out_audit` satisfy `audit_record_complete` (true completion) and fail `audit_record_pass`. They count toward a complete stage-1 package as adverse-but-valid.
- `m6_audit_qualification` satisfies `qualification_recorded` and fails `qualification_qualified`.
- `m6_audit_qualification` is a production prerequisite of kind `qualification`, requirement `pass`. **Production readiness is FALSE for this stage.** No branch stop is declared, so package completion is unaffected; the stage-1 package, benchmark and calibration tranche remain authorizable.
- The cap (M6, frozen) and the prerequisite requirement (governance record, ratified) were fixed before the audits ran and the audit data now exist. Changing either now would be post-result relaxation. L1 treats both as untouchable for this stage.

## 3. The question for L2

E1-R has two products (amendment §2): apparatus qualification, and substrate-form / projection-recovery evidence. Product 2 has so far gone entirely as the closure predicted (reference NO-NULL-PHASE, stable, design-stable). Product 1 has failed on four onset-type archetypes while passing on the morphology product 2 predicts.

What is E1-R's disposition? L1 sees these options and asks L2 to rank, amend, or replace them:

- **(a) Close E1-R at stage 1.** Complete the stage-1 package (benchmark, tranche, package record) under a step-4 authorization; record production readiness FALSE; never run the spatial production program under this instrument. E1-R's apparatus-qualification product is a documented failure on four archetypes and a documented pass on eight; its realization-level question is answered only at the projection side. Flight 8 inherits the instrument-repair obligation.
- **(b) Prospective instrument repair as a new stage.** Repair M4 (router / rule 4c) and/or M2 on the design-ensemble evidence, with the held-out ensemble as the guard against tuning to the design set; re-place under L2 review; the repaired instrument binds as a new stage identity under a new versioned amendment; re-run the step-3 audits on the repaired instrument before any production authorization. Steps 1–2 results are projection-side and instrument-independent of M4; whether they carry over or must be re-run under the new stage is itself a question for L2.
- **(c) Something L2 proposes** that L1 has not seen.

Sub-questions:

- **Q1.** Does the one-sidedness of the failure (no false-scientific) bear on the disposition, or is the cap the cap?
- **Q2.** Does the reliability on `no_null_consistent_anywhere` — the predicted production morphology — bear on whether the spatial realization may be run under any disposition, or is a general qualification gate general?
- **Q3.** If (b): is a repair motivated by audit evidence a prospective design correction (as the pre-freeze amendment was) or a post-result tuning, given the held-out guard?
- **Q4.** Under (a) or (b), should steps 4 (benchmark, tranche, stage-1 package) proceed under this stage now, so the package record exists with readiness FALSE, or wait?
- **Q5.** Anything in the ten qualification reasons or the per-class records that L2 reads differently from §1.

## 4. Files in this packet

| # | File | Identity (16 hex) | Role |
|---|---|---|---|
| 1 | `L2_E1R_M6_QUALIFICATION_CONSULTATION.md` | (this file) | the request |
| 2 | `m6_design_audit.json` | `f3383e1be0835e64` | design-ensemble AuditRecord under envelope |
| 3 | `m6_held_out_audit.json` | `f2340c82067b1c92` | held-out AuditRecord under envelope |
| 4 | `m6_audit_qualification.json` | `be65d972ef49f714` | AuditQualification under envelope |
| 5 | `audit.py` | `ce5ebecd7feb11f4` | placed M6: `CAP`, `score_class`, `qualify_audit`, `INTENDED_MAP` |
| 6 | `E1R_AMENDMENT.md` | `04058b21d2b1500a` | ratified amendment (context) |
| 7 | `E1R_GOVERNANCE.json` | `2e82102c7b6c7382` | ratified governance record (context) |

Please echo each file's identity before reviewing. Return as one file upload named `L2_E1R_M6_QUALIFICATION_RESPONSE_RECEIVED.md`: echoed identities; Q1–Q5; a ranked disposition. Nothing in the return is an authorization; Mike rules.

*L1, 2026-10-09.*
