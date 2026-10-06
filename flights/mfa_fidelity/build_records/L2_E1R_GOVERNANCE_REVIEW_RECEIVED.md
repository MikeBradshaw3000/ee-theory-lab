# L2 Governance Review — E1-R Governance Drafts

**From:** L2 (ChatGPT), adversarial source reviewer  
**To:** L1, routed by Mike  
**Register:** E1-R governance value review, pre-ratification  
**Date:** 2026-10-06  
**Requested packet:** `L2_E1R_GOVERNANCE_REVIEW_PACKET.md`  
**Scope:** value review of the E1-R amendment, machine-readable governance record, and Package Specification against the committed consultation record and the cleared M7 grammar. M7 is not reopened.  
**Overall disposition:** **RATIFIABLE WITH THE FOLLOWING EDITS**

No authorization is granted by this review. No canonical scientific job, calibration tranche, or production run is authorized.

---

## 1. Independent byte custody

Before substantive review, L2 independently SHA-256 hashed every uploaded file received in this review.

| File | SHA-256 prefix (16 hex) | Custody result |
|---|---:|---|
| `L2_E1R_GOVERNANCE_REVIEW_PACKET.md` | `0a1f79eec6b91483` | independently reproduced |
| `E1R_AMENDMENT.md` | `bcfa08c4fb86310f` | independently reproduced; matches packet |
| `E1R_GOVERNANCE.json` | `babab53e6a6679c7` | independently reproduced; matches packet |
| `PACKAGE_SPECIFICATION.json` | `036c37c0e2719b32` | independently reproduced; matches packet |
| `L2_E1_PRE_FREEZE_CONSULTATION(1).md` | `dded5adb3fd4e8fb` | independently reproduced; matches packet |
| `L2_E1_PRE_FREEZE_CONSULTATION_RESPONSE_RECEIVED.md` | `314b56cc8dcd20a9` | independently reproduced; matches packet |
| `runner.py` | `f33fbb54c115225c` | independently reproduced; matches cleared M7 identity |
| `L2_E1_M7_ROUND7_CHANGED_TEST_VERIFICATION_RECEIVED.md` | `08da8cbcb5741748` | independently reproduced; matches packet |

`SESSION_HANDOFF_2026-10-06.md` was requested as additional context but was not among the received uploads and was not retrievable as a distinct Library file. I therefore did not reconstruct or infer it. The packet itself labels that handoff “context only, not under review”; its absence does not change the value verdict below.

### 1.1 Draft identity chain

L2 independently checked the current three-draft chain:

- `E1R_GOVERNANCE.json.amendment_sha256` equals the full SHA-256 of the received `E1R_AMENDMENT.md`.
- `PACKAGE_SPECIFICATION.json.governance_sha256` equals the full SHA-256 of the received `E1R_GOVERNANCE.json`.
- the `E1RGovernance.result_sha256` independently recomputes under M7’s `_gov_body` / `_digest` rule;
- the `PackageSpecification.result_sha256` independently recomputes under M7’s `_spec_body` / `_digest` rule.

The current draft chain is therefore internally identity-consistent. The edits required below will intentionally invalidate that chain and require regeneration.

---

# 2. Q1 — Item coverage

## DISPOSITION: **CHANGE**

The amendment substantively covers all nine governance items required by the pre-freeze L2 response:

1. prospective supersession of core-architecture jeopardy;
2. revised E1-R claim and verdict jurisdiction;
3. provisional status of `NO-NULL-PHASE`;
4. retained canonical E1-R work and sequencing;
5. Flight 8 as a successor mechanism class;
6. structural rather than merely detection-boundary P1 object;
7. zero-floor skeleton / positive-floor realization split;
8. notation repair;
9. conditional §10 transcritical rewrite and held third-order comparison.

Sections 6–10 are therefore not extraneous additions. They implement items L2 expressly required Mike’s ruling to state.

There is, however, one literal mismatch in amendment §4. The amendment says **“All canonical jobs retain value … and are named here”**, but its numbered list names the tolerance-ensemble work and omits the distinct canonical `tolerance_program` finalizer that M7 declares in `CANONICAL_JOBS`.

That omission matters because the program-level record is what closes the obligation that every required canonical tolerance ensemble exists and replays.

### Exact amendment edit

Replace §4 item 2:

> `2. projection-sweep (200) and tolerance-ensemble (1,000-replicate) jobs;`

with:

> `2. projection-sweep (200), tolerance-ensemble (1,000-replicate), and tolerance-program finalization jobs;`

Then add immediately after the five-item sequence in §4:

> **Tolerance-program closure.** The tolerance obligation is closed only by a complete canonical `ToleranceProgram` covering the full declared program level set. That record is a required Stage-1 package item. An incomplete tolerance program is an incomplete execution obligation, not an adverse scientific result.

With that correction, Q1 is satisfied.

---

# 3. Q2 — Claim-tier language

## DISPOSITION: **ACCEPT**

`claim_tier = "realization-level jeopardy"` is the correct tier.

Amendment §2 is sufficiently fenced:

- E1-R asks whether the stream-level spatial realization recovers the closure’s structure;
- E1-R expressly does **not** answer whether P1 exists in the architecture;
- `NOT_PRODUCED` is adverse to the substrate’s claim to realize the first transition, not to architectural P1;
- `LOCATED` is expressly a null-relative detection boundary, not a bifurcation claim;
- `NOT_DISTINGUISHED` remains an instrument limit;
- the amendment explicitly prohibits representing any E1-R result as confirming or refuting architectural P1.

I do **not** find residual wording that converts an E1-R result into architectural P1 evidence. The phrase “the substrate’s claim to realize the first transition” is acceptable because the immediately surrounding jurisdiction language fixes the threatened object as the current realization, not the architecture.

No edit is required for Q2.

---

# 4. Q3 — Tolerance program

## DISPOSITION: **CHANGE — OPTION (a), WITH A STRONGER COMPLETION PREDICATE**

The correct disposition is:

> **(a) `tolerance_program` must be a required package item.**

It should **not** be added to `production_prerequisites` independently.

### Reason

The committed pre-freeze L2 response retained the 1,000-replicate tolerance ensembles because they are necessary to interpret T1/T3 and placed the projection-sweep and tolerance work before spatial production. M7 subsequently created a separate canonical `tolerance_program` finalizer precisely so the full multi-level obligation is closed by one replayable program record rather than by a collection of individually valid files.

Leaving `ToleranceProgram` outside the package creates a governance gap:

- each tolerance ensemble remains authorizable;
- the `tolerance_program` finalizer remains authorizable;
- but production readiness can be reached without proving that the full tolerance program was completed.

That would make the amendment’s sequencing normative prose rather than an enforced Stage-1 condition.

The Stage-1 package is already a production prerequisite as `scientific / valid_complete`. Therefore the cleanest governance join is to make the complete `ToleranceProgram` a required package item. A second prerequisite entry is unnecessary and, under the placed M7 grammar, unavailable without changing `PREREQ_VOCAB`.

### Important predicate correction

Do **not** use:

- complete = `tolerance_program_recorded`
- pass = `tolerance_program_complete`

for a required package item.

An incomplete tolerance program is not an adverse-but-valid scientific outcome. It is an unfinished canonical execution obligation. If `tolerance_program_recorded` were the completeness predicate, the Stage-1 package could become `complete=True` while the tolerance program itself carried `complete=False`.

Use instead:

- complete = `tolerance_program_complete`
- pass = `tolerance_program_complete`

### Exact `E1R_GOVERNANCE` changes

Add:

```text
tolerance_program
```

to both:

```text
package_item_vocabulary
required_package_items
```

I recommend placing it immediately after `design_stability` in both tuples.

Do **not** add it to `production_prerequisites`.

### Exact Package Specification item

Add:

```json
{
  "__type__": "PackageItem",
  "fields": {
    "complete_predicate": "tolerance_program_complete",
    "dependencies": [],
    "name": "tolerance_program",
    "pass_predicate": "tolerance_program_complete",
    "producer_job": "tolerance_program",
    "record_type": "ToleranceProgram"
  }
}
```

The final file must of course be regenerated through M7’s canonical encoder rather than hand-edited.

---

# 5. Q4 — Branch stops

## DISPOSITION: **ACCEPT**

`branch_stopping = ()` is the right value for E1-R.

I do not recommend declaring either proposed candidate:

- `dense_reference / reference_resolved`
- `design_stability / design_stable`

as a branch stop.

A `REFERENCE-UNRESOLVED` reference or a `NOT_DESIGN-STABLE` design result is scientifically adverse and may restrict which comparison statements are evaluable, but it does not erase the evidentiary value of running the spatial realization. The committed consultation specifically preserved the spatial production/recovery program and T1/T3 as substantive E1-R work rather than making success of those projection-side scientific results a prerequisite for observing the lattice.

A branch stop would therefore strengthen a scientific pass criterion into an execution gate and would contradict the adopted adverse-but-valid grammar.

No edit is required for Q4.

---

# 6. Q5 — Production prerequisites

## DISPOSITION: **ACCEPT**

The exact four production prerequisites are correct:

```text
stage1_package        scientific     valid_complete
calibration_tranche   apparatus      pass
resource_actuals      apparatus      pass
m6_audit_qualification qualification pass
```

I do **not** recommend adding `dense_reference` or `reference_stability` as independent prerequisites.

Both are already governance-required package items. Once the package is corrected as specified in this review, `stage1_package / scientific / valid_complete` requires their valid completion without converting adverse scientific content into a production veto.

Adding either again as a separate prerequisite would be redundant. Requiring `pass` would be substantively wrong because it would turn a scientifically adverse but valid reference/stability result into a branch stop through the prerequisite mechanism. Requiring `valid_complete` would merely duplicate what the Stage-1 package already proves.

No edit is required for Q5.

---

# 7. Q6 — Predicate choices

## DISPOSITION: **CHANGE**

Most predicate pairs correctly implement the completion/passage distinction. In particular:

- `dense_reference`: `reference_of_record_dense` / `reference_resolved` — correct;
- `reference_stability`: `stability_canonical_complete` / `stability_within` — correct;
- `design_stability`: `design_complete` / `design_stable` — correct;
- `m6_design_audit` and `m6_held_out_audit`: `audit_record_complete` / `audit_record_pass` — correct;
- `m6_audit_qualification`: `qualification_recorded` / `qualification_qualified` — correct because qualification passage is separately required for production;
- `resource_actuals`: `benchmark_canonical` / `benchmark_fits` — correct because benchmark passage is separately required for production;
- `conformance_preflight`: passage required for completion — correct apparatus treatment;
- `projection_sweep_ensemble`: canonical full ensemble required — correct.

Two edits are required.

## 7.1 `tolerance_program`

As stated in Q3:

```text
complete_predicate = tolerance_program_complete
pass_predicate     = tolerance_program_complete
```

An incomplete program is incomplete work, not adverse science.

## 7.2 `null_precision`

Current draft:

```text
complete_predicate = null_precision_dense
pass_predicate     = null_precision_dense_no_halts
```

Change to:

```text
complete_predicate = null_precision_dense_no_halts
pass_predicate     = null_precision_dense_no_halts
```

### Reason

A dense `NullPrecisionRecord` carrying one or more threshold-precision halts is not analogous to a resolved scientific record whose result happens to be adverse. It records failure to obtain the qualified null-precision coverage needed by the instrument. Under the amendment’s own distinction, that belongs on the apparatus/evaluability side of the boundary.

With the current pair, a dense null-precision record with halts can count as valid-complete inside `stage1_package`; because `stage1_package` is required only as `scientific / valid_complete` and `null_precision` is not an independent production prerequisite, production readiness can be reached despite those halts.

That is the wrong side of the completion/passage distinction.

Making `null_precision_dense_no_halts` both completion and passage closes the gap without changing M7 source or adding a new prerequisite kind.

### No change requested for `closure_publication`

`closure_publication` uses:

```text
complete = closure_covers_levels
pass     = exists
```

This is asymmetric, but it does not create the same readiness gap: package completeness already requires coverage, and no stronger scientific “pass” state has been defined for the publication. I do not require a change.

---

# 8. Q7 — Decision-note removal

## DISPOSITION: **ACCEPT, AFTER THE EDITS ABOVE**

The closing “Decision note for Mike” should be removed before ratification exactly as planned.

It is decision-support material, not part of the durable amendment.

Removal will change the amendment file identity. Therefore, after removing the note **and** applying the edits in this review:

1. compute the final amendment SHA-256;
2. regenerate `E1R_GOVERNANCE.json` so `amendment_sha256` names those exact final bytes and its own `result_sha256` recomputes;
3. compute the final governance-file SHA-256;
4. regenerate `PACKAGE_SPECIFICATION.json` so `governance_sha256` names those exact governance bytes and its own `result_sha256` recomputes;
5. validate the final governance/specification join through the placed M7 grammar;
6. route the final identity chain before Mike ratifies it.

No objection remains to the amendment text merely because the decision note is removed.

---

# 9. Exact edit set for one-pass regeneration

L1 can regenerate the chain once if the following changes are made together.

## 9.1 `E1R_AMENDMENT.md`

### Edit A — name the canonical tolerance-program finalizer

Replace §4 item 2 with:

> 2. projection-sweep (200), tolerance-ensemble (1,000-replicate), and tolerance-program finalization jobs;

### Edit B — make program closure explicit

Add immediately after the five-item §4 sequence:

> **Tolerance-program closure.** The tolerance obligation is closed only by a complete canonical `ToleranceProgram` covering the full declared program level set. That record is a required Stage-1 package item. An incomplete tolerance program is an incomplete execution obligation, not an adverse scientific result.

### Edit C — remove the decision note

Remove the entire final section:

```text
## Decision note for Mike (remove before ratification)
...
```

as already planned.

## 9.2 `E1R_GOVERNANCE.json`

Add `tolerance_program` to:

```text
package_item_vocabulary
required_package_items
```

Recommended placement: immediately after `design_stability`.

Leave unchanged:

```text
branch_stopping = []
```

and leave the four `production_prerequisites` unchanged.

## 9.3 `PACKAGE_SPECIFICATION.json`

Add the required item:

```text
name               tolerance_program
record_type        ToleranceProgram
producer_job       tolerance_program
complete_predicate tolerance_program_complete
pass_predicate     tolerance_program_complete
dependencies       ()
```

Change `null_precision` from:

```text
complete_predicate null_precision_dense
pass_predicate     null_precision_dense_no_halts
```

to:

```text
complete_predicate null_precision_dense_no_halts
pass_predicate     null_precision_dense_no_halts
```

No other Package Specification value change is required.

---

# 10. Consolidated dispositions

| Question | L2 disposition |
|---|---|
| Q1 — Item coverage | **CHANGE** — explicitly name `tolerance_program` finalization and its required program closure |
| Q2 — Claim-tier language | **ACCEPT** |
| Q3 — Tolerance program | **CHANGE** — required package item; both complete and pass predicates = `tolerance_program_complete`; not an independent production prerequisite |
| Q4 — Branch stops | **ACCEPT** — none |
| Q5 — Production prerequisites | **ACCEPT** — exact four as drafted |
| Q6 — Predicate choices | **CHANGE** — `null_precision` completion must require `null_precision_dense_no_halts`; add corrected tolerance item |
| Q7 — Decision-note removal | **ACCEPT** after edits and full chain regeneration |

---

# 11. Overall disposition

## **RATIFIABLE WITH THE FOLLOWING EDITS**

The governance architecture is sound and the central scientific boundary is correctly expressed. I find no defect requiring M7 reopening and no reason to reject the E1-R amendment.

Ratification should wait for one regenerated identity chain containing exactly these substantive corrections:

1. make the complete canonical `ToleranceProgram` a required Stage-1 package item;
2. make tolerance-program completion require `tolerance_program_complete`, not mere record existence;
3. make `null_precision` package completion require dense coverage **with zero precision halts**;
4. explicitly name the tolerance-program finalizer in amendment §4;
5. remove the decision note and regenerate the amendment → governance → specification identity chain.

After regeneration, route the final three files and their exact identities for L2 changed-value/identity confirmation before Mike ratifies them.

**No authorization is granted by this review.**
