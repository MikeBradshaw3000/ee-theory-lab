# L2 AUTHORITATIVE Acceptance Review — Gate B

**From:** L2 (ChatGPT)  
**To:** L1, routed by Mike  
**Register:** Phase-2 — Gate B AUTHORITATIVE run of record  
**Reviewed packet:** Gate B AUTHORITATIVE Acceptance Review Request, dated 2026-09-16  
**Repository state represented:** certification bundle at `cf100c6`  
**Overall verdict:** **ACCEPTED — GATE B PASSES UNDER AUTHORITATIVE CONDITIONS. THE GATE B REGISTER MAY CLOSE.**

## Review scope and evidence boundary

This review adjudicates the committed certification record and the supplied structural extracts of:

1. the formal qualification record;
2. the AUTHORITATIVE B1 report; and
3. the AUTHORITATIVE B2 report.

The packet supplies the four committed SHA-256 identities and states that all material was read from committed objects in a fresh clone. The four raw repository artifacts were not separately attached as standalone byte streams, so L2 does **not** claim an independent recomputation of those four artifact digests in this review. L2 did independently parse the three complete JSON extracts carried in the packet and check their internal counts, stages, grammar, and verdict arithmetic.

No contradiction was found between the committed certification narrative and the carried artifact extracts.

---

# 1. Frozen grammar, harness identity, and execution conditions

**VERDICT: ACCEPTED.**

The run is tied to:

- Gate B Specification v0.4, frozen 2026-09-04;
- the cleared harness lineage placed at `b046456`;
- the platform-byte-identity repair placed at `9d1f75f`;
- pinned reference object  
  `4d9a622:cycle3/wave_two/c3_w2_tcop.py`;
- reference blob SHA-256  
  `466455f20550b8c41a984ce40db49ebe0e832ae56c269ab518b521c6ad83b7e7`;
- frozen lock blob SHA-256  
  `c10e02c5db497570ffeb45dc92857fcc633cb38364858a35458096950d02de7c`;
- Python 3.14.4, NumPy 2.4.4, active frozen venv, and all twenty pins conforming; and
- FULL reference loading from the verified Git-object bytes.

The qualification record binds its runtime declaration to its frozen manifest:

```text
frozen_manifest_sha256
= runtime_declaration_sha256
= d9cc5ee06b462076df065173a278964cd05cf032956b4938b896d898eaae65d4
```

It also records the qualification, B1, B2, and candidate-dynamics source identities used by the qualification. The reference and environment identities in B1 and B2 agree with the certification record.

The three acts are separate and non-substitutable. Qualification, B1, and B2 each passed; none is being used to compensate for failure of another gate component.

---

# 2. Formal qualification

**VERDICT: ACCEPTED.**

The formal qualification record is complete on its frozen surface:

- `passed: true`;
- stages completed in order:
  - `manifest_preflight`;
  - `positive_control`;
  - `witnesses`;
  - `mutants`;
- AUTHORITATIVE B1 positive control passed;
- base-invariance witness passed;
- one-tick alignment witness passed;
- floating-point association witness passed with distinct raw patterns;
- solved-offset enumeration passed with source identity verified and no unparsed surfaces;
- all **32 mutants were rejected**;
- all **32 mutants were attributed** to their predeclared checks; and
- mutant IDs are complete and contiguous from 1 through 32.

The record contains 31 non-null per-mutant failure-artifact digests. Mutant 31 is the constructed alignment witness and correctly has no separate B1/schedule failure artifact. The certification record’s description of “31 per-mutant B1/schedule failure artifacts” is therefore exact.

The four identical artifact pairs do not weaken qualification:

- 9 / 11;
- 13 / 14;
- 15 / 16;
- 22 / 23.

Each pair is documented as reaching the same first failing case with the same evidence. Attribution belongs to the qualification record’s mutant-path binding; the underlying B1 failure artifact need not manufacture distinct bytes when the first observed failure is genuinely identical.

---

# 3. AUTHORITATIVE B1

**VERDICT: ACCEPTED.**

The B1 report satisfies the frozen completion object.

## Battery completion

```text
single_step         486
threshold_witness    27
stencil_motif       108
chained              150
schedule_table      4000
                    ----
case bundles        4771
```

The five frozen stages are present in the required order.

## Comparator accounting

The report’s comparator counts are internally exact:

```text
preflight              1
single_step          1944
threshold_witness     108
stencil_motif         432
chained               600
schedule_table       4000
                     ----
total                 7085
```

The allclose diagnostic count is also structurally consistent:

- 771 dynamic case bundles × three float diagnostics = 2,313;
- 4,000 schedule scalar diagnostics;
- one survival scalar diagnostic;

for a total of **6,314**, all true and none false.

The diagnostic never held the verdict. Raw float64 equality and exact state-comparator semantics remained authoritative.

## Environment and provenance

The report records:

- `label: AUTHORITATIVE`;
- environment conformance;
- FULL reference mode;
- verified reference commit and blob;
- candidate commit `9d1f75f...`;
- candidate dynamics digest  
  `483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8`;
- frozen specification digest; and
- the dirty-worktree flag.

The dirty candidate worktree does not invalidate B1. The record identifies the dirtiness as unrelated untracked Stage-2 calibration output, while the operative commit and source identities are separately bound. There is no evidence in the packet of tracked Gate-B source drift.

---

# 4. AUTHORITATIVE B2

**VERDICT: ACCEPTED UNDER THE FROZEN PATH-B CLAIM, AND ONLY THAT CLAIM.**

## Wrapper verification

The executable-reference wrapper passed **10/10** declared comparisons against pinned `execute_run`.

Each carried wrapper result reports:

- identical shape;
- identical `int64` dtype;
- identical state-array bytes; and
- equal SHA-256 values for actual and wrapper output.

The ten-run map covers all eight declared cells at seed 42 and both CM-1 sign arms again at seed 137. This exceeds the earlier minimum wrapper subset and is consistent with the frozen grammar.

## Frozen ensemble grammar

The B2 report carries the correct frozen elements:

- eight declared cells;
- reference seeds 201–220;
- candidate roots 301–320;
- \(n=20\) per side;
- 400 ticks;
- terminal window 300–399;
- equivalence margin \(\delta=0.003\);
- per-cell TOST alpha 0.00625;
- gross-divergence-screen alpha 0.00125;
- both κ signs in CM-0 and CM-1; and
- the complete CM-1 schedule.

## Cell verdicts

Every cell’s 98.75% Welch interval lies wholly inside ±0.003.

From the carried numbers:

- the largest absolute mean difference is approximately **0.000346**;
- the most extreme confidence-limit magnitude is approximately **0.001159**;
- the smallest gross-divergence-screen p-value is approximately **0.1745**; and
- therefore every screen p-value is well above the frozen 0.00125 alarm boundary.

All eight cells correctly report:

- `tost_pass: true`; and
- `alarm: false`.

The report also states that every printed result reproduces the earlier PROVISIONAL container run to the last printed digit, despite the change in environment and reference-load mode. This is supportive replication, not a substitute for the AUTHORITATIVE result.

---

# 5. Certified claim and jurisdiction

**VERDICT: CLAIM BOUNDARY ACCEPTED, WITH ONE BINDING PRECISION FOR FUTURE CITATION.**

The B2 claim is correctly limited to:

> terminal-window ensemble-mean equivalence plus the priced gross-divergence screen.

The record expressly does **not** claim:

- full distributional equivalence;
- seedwise trajectory equivalence;
- Ψ validity;
- Regime-II existence;
- ecosystem phenomenology;
- live-Q behavior under `become_survive`; or
- anything outside the Q-disabled Path-B domain.

That is the correct jurisdiction.

## Step-level wording precision

The certification record describes B1 as “bit-identical to Lineage B at step level.” This is accepted only as shorthand for the **frozen exact-comparator bundle**, not as a claim that every stored object has identical bytes and dtype.

The exact evidence is:

- `p_become`: raw float64-bit equality;
- ancestor-derived `g_q`: raw float64-bit equality;
- `p_survive`: raw float64-bit equality;
- schedule \(u_t\): raw float64-bit equality;
- next state: exact logical equality after canonicalizing the ancestor’s integer state to the candidate’s committed Boolean dtype; and
- shared declared random grid: exact identity under the counted stub.

Future citations should therefore use:

> **exact deterministic step-level rule equivalence under the frozen B1 comparators**

rather than an unqualified assertion of byte identity for every output. This is a wording precision only. It does not alter the B1 verdict.

Likewise, the statement that “no candidate output was consulted in any decision” is accepted in its governance meaning: no candidate output was used to select or relax the frozen grammar, margins, cells, comparators, or verdict rules. Candidate output was, of course, evaluated by the frozen gate.

---

# 6. Amendment 1 — committed versus execution-time artifact identities

**VERDICT: ACCEPTED AS A NON-SUBSTANTIVE IDENTITY AMENDMENT.**

The amendment does not change:

- any JSON value;
- any stage;
- any count;
- any cell result;
- any pass/fail value;
- any claim boundary; or
- any frozen decision.

It corrects which byte representation is named as the repository identity:

- working-tree files at execution: CRLF;
- committed Git blobs: LF;
- committed blobs: identities of record.

The stated relationship is exact and reproducible:

```text
working-tree bytes = committed blob with every LF rendered as CRLF
```

The per-mutant `artifact_sha256` values inside the qualification record remain execution-time identities. They are not silently re-described as committed-blob identities. The Amendment 1 record must therefore travel with the qualification record whenever those internal digests are cited.

This dual-identity repair is acceptable for the completed Gate B run because the execution artifacts existed persistently, the content transformation is fully specified, and the committed verdict objects are now named by their committed SHA-256 values.

## Required forward hardening, non-blocking for Gate B acceptance

The three atomic writers should be repaired under a separately reviewed bounded change to open JSON outputs with an explicit LF newline policy, such as `newline="\n"`.

That hardening is **not** a condition of this Gate B acceptance and must not rewrite the run of record. It should be completed before the next AUTHORITATIVE artifact-producing certification so that future execution-time and committed identities do not require a post-run identity amendment.

---

# 7. Artifact identities accepted for the Gate B register

The following are the identities of record as supplied from the committed bundle:

- certification record, Amendment 1:  
  `940d88a426d9530449d4c9d93d4a23085d354b678e2229edcf849806f6685883`
- formal qualification:  
  `46d905b3a75c283aeb55be3d6cfda854877a1a2eb589abd53234b38fd0823429`
- AUTHORITATIVE B1:  
  `2a715899a91521a225c2562b821287bd7698912609c688e14a3e9789fe0c7b94`
- AUTHORITATIVE B2:  
  `db70e78a1ceedca79ab44f966432ffc548e5b00552cdcb7cdd3c9ce85b9bcb45`

They supersede the corresponding execution-time working-tree digests for repository citation. The working-tree digests remain valid provenance of the bytes written on the canonical machine.

---

# 8. Findings outside the acceptance question

## O1 — newline hardening

Recorded above as a required forward hardening item. It does not reopen the certification result.

## O2 — no promotion beyond Path B

Gate B acceptance must not be cited as Gate A preservation, Gate R recovery, observables validity, or evidence for any E-rung phenomenology. The three certification gates remain genuinely separate.

## O3 — candidate worktree cleanliness

The dirty-worktree condition is acceptable for this run because the dirtiness is identified as unrelated untracked output and operative source identities are separately recorded. Future AUTHORITATIVE runs should preferably use a clean worktree or emit the full dirty-path list in the run record, so the conclusion does not depend on a later narrative classification of the dirty files.

This is prospective hardening, not a defect in the present record.

---

# 9. Final register disposition

**L2 ACCEPTS THE GATE B AUTHORITATIVE CERTIFICATION.**

The permanent register may state:

> **Gate B — PASSED under AUTHORITATIVE conditions.**  
> The merged instrument’s `become_survive` path achieved exact deterministic step-level rule equivalence under the frozen B1 comparator battery and satisfied the frozen Path-B ensemble criterion across all eight declared B2 cells: terminal-window ensemble-mean equivalence within ±0.003, with no priced gross-divergence alarm. The certification is limited to the Q-disabled Path-B domain and makes no claim about full distributional equivalence, Ψ, Regime II, ecosystem phenomenology, Gate A, or Gate R.

**REGISTER STATUS: GATE B L2-ACCEPTED / CLOSED.**
