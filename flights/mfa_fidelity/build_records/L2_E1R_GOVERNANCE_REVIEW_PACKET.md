# L2 Review Packet — E1-R Governance Drafts (pre-ratification)

**From:** L1 (Claude, design chamber), at Mike Bradshaw's direction
**To:** L2 (ChatGPT, adversarial source review) — new chat, no prior context assumed
**Date:** 2026-10-06
**Repository:** `github.com/MikeBradshaw3000/ee-theory-lab`, `main` at `f658ea5e7a240fa7012287e8f19490007e1baed3`
**Review type:** VALUE review of three governance drafts before Mike ratifies them. The grammar they must satisfy is the placed M7 (`runner.py` `f33fbb54…`), which L2 cleared SOUND at round 7. M7 is not under review; the drafts are.

---

## 0. Orientation for a fresh L2 chat

Roles: Mike is Theory Architect, sole execution channel, final arbiter of every commit and ruling. L1 drafts; L2 reviews adversarially against the committed record only. Phil Roundy writes the manuscript and does not rule on the theory.

Standing rules this review runs under:
- Never-relax-after-output is in force. No E1 production or canonical data exist, so a prospective amendment is design correction, not relaxation (L2's own §2.2 in the consultation response).
- The committed record governs. Every file in this packet carries its identity; **please echo the 16-hex SHA-256 prefix of each upload before reviewing**, so a stale or mis-served file is caught first.
- L1 cannot execute Windows; Mike's canonical suite (575 passed, 2 declared skips at `7ebb87e`) is the platform proof.

State of the stage: all seven E1 stage-1 modules are placed. M7's suite and placement records were committed at `f658ea5` and verify mechanically (`verify_placement` passes; stage binds `pre_amendment` on Mike's twenty-pin environment). The stage becomes `canonical` only when the three records under review are committed and validate. Nothing is authorized; authorization is a separate act (`AUTHORIZATION_001.json` + registry) that follows ratification.

## 1. Files in this packet and their identities

| # | File | SHA-256 (16 hex) | Role in this review |
|---|---|---|---|
| 1 | `L2_E1R_GOVERNANCE_REVIEW_PACKET.md` | (this file) | the review request |
| 2 | `E1R_AMENDMENT.md` | `bcfa08c4fb86310f` | **under review** — prose half; carries the five contract fields |
| 3 | `E1R_GOVERNANCE.json` | `babab53e6a6679c7` | **under review** — typed values; names the amendment's full digest |
| 4 | `PACKAGE_SPECIFICATION.json` | `036c37c0e2719b32` | **under review** — package mechanics; names the governance record's full digest |
| 5 | `L2_E1_PRE_FREEZE_CONSULTATION.md` | `dded5adb3fd4e8fb` | committed record (`a24fd5e`): Mike's three findings and recommendation |
| 6 | `L2_E1_PRE_FREEZE_CONSULTATION_RESPONSE_RECEIVED.md` | `314b56cc8dcd20a9` | committed record (`a24fd5e`): L2's ruling that E1 becomes E1-R; §7 lists the nine items the amendment must state |
| 7 | `runner.py` | `f33fbb54c115225c` | placed M7: `validate_governance`, `validate_package_spec`, `PREDICATE_IDS`, `PREREQ_VOCAB`, `AMENDMENT_REQUIRED_FIELDS`, `CANONICAL_JOBS` |
| 8 | `L2_E1_M7_ROUND7_CHANGED_TEST_VERIFICATION_RECEIVED.md` | `08da8cbcb5741748` | L2's own round-7 clearance of M7 (context: confirms the enforcing code is the cleared one) |
| 9 | `SESSION_HANDOFF_2026-10-06.md` | — | context only, not under review |

The three drafts are chained: the governance record's `amendment_sha256` is the full digest of file 2; the specification's `governance_sha256` is the full digest of file 3. Any edit to the amendment (including removing its closing decision note) breaks the chain and requires regenerating files 3 and 4 with M7's encoder. The decision note will be removed before ratification; L2 should review it as a decision aid, not as amendment text.

L1 verified on 2026-10-06, from a fresh clone, that: the amendment carries all five required fields, LF only; file 3 decodes canonically and passes `validate_governance`; file 4 passes `validate_package_spec` against file 3, including the round-5 branch-stop join. **Grammar conformance is therefore established; this review is about whether the values are the right values.**

## 2. What the drafts assert (summary; the files govern)

**Amendment (file 2), ten numbered sections mapped to L2 §7's nine items:**
1. Core-architecture jeopardy superseded prospectively; reason of record is L2 §1.3 (memoryless per-cell rule, feedback βd − δd² > 0 for d < 0.75).
2. E1-R claim: does the spatial realization recover the closure's structure; never whether architectural P1 exists. Verdict jurisdiction restated for `NOT_PRODUCED`, `LOCATED`, `NOT_DISTINGUISHED`; T2-S/T1/T3 unchanged in form.
3. NO-NULL-PHASE is provisional; only the canonical 701-point job creates the reference of record.
4. All canonical jobs retain value and are named authorizable in L2's order; the amendment authorizes nothing by itself.
5. Package/production grammar: adverse-but-valid results are complete; package-complete and production-ready are separate derived states; apparatus/qualification prerequisites require passage, scientific ones valid completion; branch stops only if expressly declared — **none declared**.
6–8. Flight 8 is a separate successor contract (no E1 data tune its gates); its P1 endpoint is structural (zero-floor skeleton / positive-floor realization split adopted); exact discrete-time rule first.
9. Notation repair: `η_floor` reserved, noise written ξ_ρ(t), deactivation μ, unlabelled η(t) retired.
10. Overview §10 transcritical rewrite accepted conditionally on the theory track; third-order comparison held.

**Governance record (file 3):** `claim_tier` = "realization-level jeopardy"; vocabulary = required items = the 14 names below; `branch_stopping` = empty; `production_prerequisites` = exactly {`stage1_package` scientific/valid_complete, `calibration_tranche` apparatus/pass, `resource_actuals` apparatus/pass, `m6_audit_qualification` qualification/pass}.

**Package Specification (file 4), 14 items** (name → complete predicate / pass predicate):
`conformance_preflight` → conformance_production_passed / same; `closure_publication` → closure_covers_levels / exists; `null_precision` → null_precision_dense / null_precision_dense_no_halts; `dense_reference` → reference_of_record_dense / reference_resolved; `reference_stability` → stability_canonical_complete / stability_within (dep: primary=dense_reference); `level_list_and_spacings` → exists / exists; `projection_sweep_ensemble` → sweep_ensemble_canonical / same; `design_stability` → design_complete / design_stable (deps: ref, sweeps); `router_collision_record` → exists / exists; `m6_design_audit`, `m6_held_out_audit` → audit_record_complete / audit_record_pass; `m6_audit_qualification` → qualification_recorded / qualification_qualified (deps: design, held_out); `ensemble_sizes` → exists / exists; `resource_actuals` → benchmark_canonical / benchmark_fits.

Note the asymmetry by design: for apparatus items (conformance, sweep ensemble) the complete predicate *is* the pass predicate; for scientific items (dense reference, stability, design stability) completion is weaker than passage, so an adverse-but-valid result still counts toward a complete package.

## 3. Two things that moved under the drafts since 2026-10-03

1. **`audit_record_complete` now means true completion** (M7 round 5): every class attempted and scored 500 times with zero halts, separate from passage. The two M6 audit items are unchanged in value but stricter in meaning. L1's view: this is the intended meaning and no edit is needed; L2 should confirm or object.
2. **No `ToleranceProgram` package item.** M7 carries a `tolerance_program` canonical job, a `ToleranceProgram` record validated only by replay, and the predicates `tolerance_program_recorded` / `tolerance_program_complete`. The drafts omit it from the vocabulary and the package, per the amendment's decision note (tolerances serve T1/T3 after production, so they are not stage-1 package items). L2 said at round 4 that the tolerance-program record is still required to close the tolerance obligation whether or not it is a package item. **This is the one question where L1 expects L2 may want a change** — see Q3.

## 4. Questions for L2

Please answer each with ACCEPT, CHANGE (with the exact change), or DEFECT (with the reason), and finish with a single overall disposition: **RATIFIABLE AS DRAFTED / RATIFIABLE WITH THE FOLLOWING EDITS / NOT RATIFIABLE**.

- **Q1 — Item coverage.** Does the amendment state all nine §7 items at the precision L2 required? Is anything stated that §7 did not ask for and that should not be in a versioned amendment?
- **Q2 — Claim-tier language.** Is "realization-level jeopardy" and the verdict-jurisdiction text in amendment §2 sufficient to prevent any E1-R result from being read as confirming or refuting architectural P1 (L2 §3.3)? Any wording that still leaks a P1 claim?
- **Q3 — Tolerance program.** Should `tolerance_program` (record type `ToleranceProgram`, complete = `tolerance_program_recorded`, pass = `tolerance_program_complete`) be (a) a required package item, (b) a vocabulary item that is authorizable but not required, or (c) left out of the package entirely with the obligation closed by its own canonical-job record, as drafted? If (a) or (b), say whether it belongs in `production_prerequisites` — note `PREREQ_VOCAB` in M7 does not include it, so (a)/(b) would make it a package condition, not a production prerequisite, without a runner change.
- **Q4 — Branch stops.** The drafts declare none. The candidates the decision note names are a REFERENCE-UNRESOLVED dense reference (T2-S cannot speak) and a NOT_DESIGN-STABLE design gate. L2 held at consultation that spatial production and T1/T3 retain value even then. Confirm that no branch stop is the right value, or name the stop(s) to declare and the predicate(s) from `PREDICATE_IDS` to join them to.
- **Q5 — Production prerequisites.** Is the exact set of four, with their kinds and requirements, right? In particular: should `dense_reference` or `reference_stability` (both in `PREREQ_VOCAB`) be production prerequisites in their own right, or is their inclusion in `stage1_package` (scientific, valid_complete) sufficient?
- **Q6 — Predicate choices.** Any item whose complete/pass predicate pair is wrong in kind — e.g. a scientific item whose completion requires passage, or an apparatus item whose completion does not?
- **Q7 — Decision-note removal.** The closing "Decision note for Mike" will be deleted before ratification, changing the amendment digest and forcing regeneration of files 3 and 4. Any objection to the amendment text as it will stand without the note?

## 5. What L2's return should contain

A single file upload (pasted long text can arrive empty on this channel) named `L2_E1R_GOVERNANCE_REVIEW_RECEIVED.md`, stating: the four echoed identities (files 2, 3, 4, 7); answers Q1–Q7; the overall disposition; and, if edits are required, the exact replacement text or values so L1 can regenerate the chain once rather than iterate.

Nothing in this packet is an authorization, and no value in it binds until Mike commits it.

*L1, 2026-10-06.*
