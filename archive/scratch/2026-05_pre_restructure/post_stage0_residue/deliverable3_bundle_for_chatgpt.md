

---
# MISSING FILE: protocols\foundational\theoretical_context.md
---



---
# MISSING FILE: protocols\foundational\personal_context.md
---



---
# MISSING FILE: protocols\foundational\environment_reference.md
---



---
# FILE: protocols\foundational\standing_rules.md
---

# Standing Rules

**Document role.** Canonical list of protocol-level standing rules. Rules operate across all sessions and all AI partners. They are enforced by Layer 1 against artifacts entering the canonical record; the discipline applies symmetrically, including to Layer 1's own work.

**Authority.** This document is authoritative for protocol-level rule content. The instantiation kit reproduces a compressed summary; when the kit and this document conflict, this document wins. When this document conflicts with primary source (file system, source code, document text, git log), primary source wins and this document revises. Rule 1 specifies the verification discipline that implements this override in practice.

**Maintenance discipline.** New rules added when Mike ratifies a new standing commitment. Existing rules amended when the operational understanding of the rule evolves. Each rule entry includes the session in which it was first committed; the change-history of this document, taken with the operations logs, is the canonical record of rules evolution.

**Relationship to `protocol_primer.md`.** The primer specifies *what* the protocol is; this document specifies *what holds across* all protocol operations. Rules cite primer sections by reference where relevant.

---

## Rule 1: Primary-source verification before downstream claims

**First committed:** session 5 (informal), session 6 (named explicitly), session 7 (formalized).

Before accepting or routing any claim with substantial implications, verify against primary source — file system, source code, document text, parquet metadata, hash output, git log. The discipline applies symmetrically across all AI partners including Claude. Memory descriptions are not primary source; they can carry forward inferences as if they were facts.

**Specifically for git operations:** the primary source for "did a commit fire" is `git log --oneline -N`, not git's narrative status messages. Reading "nothing added to commit but untracked files present" as evidence the prior commit didn't fire is a working-memory instance — verify against the log.

**Specifically for file existence and content:** `git status --short`, `dir`/`Get-ChildItem`, and direct file reads are primary source. The instantiation kit's canonical-artifacts index is a working description and may drift from primary source; primary source wins.

**Rule 1 has no complexity floor.** Session 8 surfaced an instance on integer arithmetic over file counts. The discipline applies at every level of granularity, not only on substantive analytical claims.

---

## Rule 2: Session-end verification

**First committed:** session 7.

At session close, explicitly verify:

1. What files exist in Claude's `/home/claude/` workspace from this session?
2. What files have been downloaded by Mike and saved to known paths on his end?
3. What is staged for future action (drafts not completed, decisions deferred)?

These three categories must be distinguished. Standing offers ("when you're ready, I can draft...") are *unfulfilled* at session close unless Mike accepted them during the session. A drafted-and-presented file is not equivalent to a filed-on-Mike's-end file. The session-end record must note the distinction.

**Operations log discipline.** Commit the session log at session end, not the start of the next session. Deferring the commit means the next session inherits an uncommitted file as its starting state — recreating the precondition problem the session 7 reconciliation closed.

**Session-handoff folder discipline (added session 9).** When prior-Claude prepares material for the next session's instantiation, the handoff folder at `claude_session_handoffs/YYYY-MM-DD[-N]/` must contain:

- The current instantiation kit (latest revision).
- The just-closed session's operations log (most recent — required, not optional).
- Optionally, one or two prior session logs for cross-session continuity.

The just-closed session's operations log is load-bearing for next-session orientation; without it, the next-session Claude operates from kit-summary plus prose-summary supplementary material, which is the working-memory failure mode the protocol is structurally designed to avoid.

**Opening-instruction discipline (added session 9).** The opening instruction Mike sends to next-session Claude is a single sentence pointing at the kit (e.g., "Instantiate per the attached kit; verify HEAD per the resume anchor"). All substantive operational knowledge belongs *inside* the kit, not in a supplementary note. If prior-Claude has new working-pattern observations worth carrying forward, the discipline is to fold them into kit-revision-N as part of session-end maintenance — not to draft a parallel instantiation document.

**Kit-revision discipline (added session 9).** When working-pattern, current-state, or canonical-artifacts content changes during a session, the kit is revised in the same session and committed alongside the operations log. The kit revision number increments; the prior kit revision is preserved in git history.

---

## Rule 3: Sequential cross-layer routing by default

**First committed:** session 6.

Layer 1 structural review precedes Layer 2 substantive review. Parallel routing collapses review surfaces — if Layer 1 and Layer 2 both engage the same material simultaneously, the independent ground Layer 2 is meant to provide is contaminated by exposure to Layer 1's framing.

Exceptions to sequential routing require deliberate justification recorded in the operations log.

---

## Rule 4: Layer 1 boundary-crossing under disclosure

**First committed:** session 5 (registered), session 6 (formalized).

Layer 1 acting on Layer 3's surface (direct code edits, detailed example shapes, full implementation drafts) is permitted but must be disclosed at the time and registered in the operations log. The justification for a boundary-crossing is typically session economics — when Layer 1 already has the primary source loaded in context and the implementation question is bounded, drafting directly is cheaper than the round-trip to Layer 3.

The boundary-crossing pattern itself is worth tracking; whether it should be tightened back toward stricter layer discipline is a protocol-level question that Mike arbitrates over time.

---

## Rule 5: Vocabulary quarantine enforced at wrap-ups and celebratory moments

**First committed:** prior to session 5 (carried forward from earlier protocol state), reaffirmed session 6.

Vocabulary discipline operates as much during synthesis and result-celebration as during active analysis. Drift is most likely when guard is down — the wrap-up phrase that "sounds right" is the most likely vehicle for quarantined vocabulary to enter the canonical record.

See `vocabulary_quarantine.md` for the prohibited terms list and permitted framings.

---

## Rule 6: No-preserved-divergence is a finding to track

**First committed:** session 6 (named in synthesis discussion), retained as discipline.

Synthesis is the work; convergence is a phenomenon that sometimes occurs. Only converge where convergence genuinely emerges. Carry multiple readings forward otherwise.

The no-preserved-divergence pattern between Layer 1 and Layer 2 is not necessarily substantive convergence; it may be the framing-asymmetry artifact (see `protocol_primer.md` Section 4). Layer 1 framing-room for divergence is what allows Layer 2 to engage substantively rather than being channeled into refinement of Layer 1's position.

---

## Rule 7: Section 15 prohibitions lifted to protocol level

**First committed:** session 6 (direction committed), session 9 (execution).

The Flight 6 Substrate Specification's Section 15 lists prohibited substitutions, shortcuts, evasions, analysis-stage repairs, and required affirmations specific to substrate implementation. The protocol-applicable items below are lifted with translation; each cites its Section 15 source bullet. Substrate-specific items remain in the substrate spec where they belong and are not reproduced here.

**Citation convention:** Section 15 source bullets are referenced as "FSS §15 / substitutions / N" where N is the bullet position in that subcategory.

### Rule 7.1 — Aggregate completion claims require per-artifact verification

*Source: FSS §15 / shortcuts / 1.*

Aggregate terminal completion messages ("ALL ARTIFACTS PRESENT", "EXTRACTION COMPLETE", etc.) without per-artifact verification are prohibited across the protocol. Each artifact named in a deliverable specification must be produced as a distinct file with content matching specification; verification at end of execution requires explicit per-artifact confirmation, not aggregate completion claims.

### Rule 7.2 — Schema-emulation without engine-execution

*Source: FSS §15 / shortcuts / 2.*

Mock objects, schema emulators, and namedtuple-style stand-ins that bypass the actual code path under test are prohibited when verification claims depend on the real code path's behavior. If a test is meant to verify that a contract's validation pipeline rejects a malformed input, the test must route the input through the actual validation pipeline — not through a mock that simulates rejection.

The pattern surfaced repeatedly in session 5 (Tier 3 intake test construction). Reading source before writing code that touches the contract is the corrective discipline.

### Rule 7.3 — Synthetic hashes or metadata not generated by actual file operations

*Source: FSS §15 / shortcuts / 3.*

Hash values, parquet metadata, file sizes, and similar verification artifacts must be generated by actual operations on the actual files. Reported hash values that were not produced by running the hash function over the file contents at verification time are prohibited.

### Rule 7.4 — Memory-based reconstruction without canonical source verification

*Source: FSS §15 / evasions / 3.*

Equations, specification content, parameter values, and protocol details must not be reconstructed from working memory when canonical source is available. The discipline applies to all AI partners including Layer 1; Layer 1's central-node role does not exempt Layer 1 from the verification discipline.

This rule is the canonical statement of the working-memory pattern's corrective discipline (see `protocol_primer.md` Section 4). Rule 1 specifies how to comply; this rule specifies that the compliance is mandatory.

### Rule 7.5 — Aggregate framing covering partial implementation

*Source: FSS §15 / evasions / 4.*

Framings such as "FULL EXTRACTION COMPLETE" or "ANALYSIS COMPLETE" that cover partial implementation are prohibited. If 7 of 8 production artifacts are produced and 1 failed, the framing must name the partial completion explicitly, not absorb the failure into an aggregate success claim.

### Rule 7.6 — Inference-based imputation of missing required telemetry

*Source: FSS §15 / analysis-stage repairs / 1.*

Missing required telemetry columns or required artifacts are *substrate failures to be surfaced and remediated*, not analysis opportunities to be silently filled. Inferring missing required values from other columns, imputing from neighbors, or applying defaults to fill required fields is prohibited.

The corrective response to missing required telemetry is to surface the failure to Layer 1, route the remediation to Layer 3, and re-execute — not to patch over in analysis.

### Rule 7.7 — Required affirmations

*Source: FSS §15 / required affirmations / 1–4 (translated for protocol scope).*

For any artifact entering the canonical record:

1. Every substantive claim traceable to canonical source or primary-source verification.
2. Every parameter value pulled from the authoritative source (specification, constants module, prior canonical commit).
3. Every computational column or value populated by actual computation per the specifying document.
4. Every completion claim backed by per-artifact verification per Rule 7.1.

The required affirmations are the positive counterparts of Rules 7.1–7.6; meeting all four is the standing test for canonical-record-readiness.

---

## Rule 8: Synthesis-stage failure modes apply symmetrically

**First committed:** session 6 (named), carried forward.

The following failure modes apply across all AI partners including Claude:

- Soft convergence (apparent convergence absent substantive engagement).
- Interpretation creep (the analytical conclusion's scope expanding beyond what was tested).
- Test substitution (inferring rather than testing).
- Structural re-entry through ranking (re-asserting a quarantined structure by ranking among options that include it).
- Too-strict reading of cross-AI review can defer Mike's direct arbitration — cross-AI coherence review is a strong default, NOT a procedural gate.
- Scorecard-watching convergence-direction patterns can themselves drive moves.
- Closing on architectural-ground inference about what testing would show IS test-substitution.

Layer 1 is not exempt from these failure modes. Layer 1 enforces them against Layer 2 and Layer 3 returns and must apply them reflexively to its own synthesis work.

---

## Rule 9: Staging-action recommendations wait for Mike's confirmation

**First committed:** session 7.

Layer 1 explicitly tags staging-action recommendations as pending confirmation when Mike has not yet ratified. Reading speed can exceed confirmation speed; Layer 1 recommendations should not be acted on as if they were directives until Mike's explicit nod.

This is distinct from informational recommendations, which don't require confirmation before reading.

---

## Rule 10: Batched staging requires content-level verification

**First committed:** session 7.

When Layer 1 suggests a multi-file `git add` batch and any file's content was constructed in-session, verify file content matches intent before staging — either by separating the staging command for that file, or by reading the diff explicitly before staging.

Path-level correctness (the file exists at the right path) does not imply content-level correctness (the file contains what we mean to commit).

---

## Note on the "routing as if completed work" candidate rule

The instantiation kit (kit-revision-2) included an item in its Rule 7 list — "routing as if completed work that was deferred or standing-offered" — that does not trace to Section 15 of the Flight 6 Substrate Specification. The item appears related to Rule 2's session-end verification (Rule 2's "standing offers are unfulfilled at session close unless Mike accepted them"), but it was attributed to Section 15 in error.

The substantive content is real and is preserved under Rule 2. The Section 15 attribution is corrected here; no separate Rule 11 is created.

If a future session surfaces a need for an independent rule on this pattern, it would be added as a new numbered entry, not retrofitted into Rule 7's Section 15 lift.

---

— Drafted by Claude as Layer 1 central node, Stage 1 of repository restructure, session 9. v2 incorporates Layer 2 review (item 3 from pair-1 routing — authority statement asymmetry cleanup). Pending Layer 2 acceptance of v2 before commit per primer Section 3's protocol-infrastructure routing convention.



---
# FILE: protocols\foundational\vocabulary_quarantine.md
---

# Vocabulary Quarantine

**Document role.** Canonical list of prohibited terms, permitted framings, and drift-prone vocabulary. Operates as the reference document for Layer 1's vocabulary-enforcement role and for all participants' self-discipline at synthesis and wrap-up moments.

**Authority.** This document is authoritative for vocabulary discipline. When the instantiation kit summarizes quarantine content, this document is the canonical source. When this document conflicts with primary source (the State of the Theory, formal architectural documents), primary source wins and this document revises.

**Maintenance discipline.** New entries added when a term is identified as quarantine-worthy through operations-log surfacing or cross-AI review. Existing entries amended when the rationale evolves. Drift-prone terms graduate to quarantine if recurrent use produces architectural confusion; the graduation is a Mike-arbitrated decision recorded in an operations log.

**Relationship to `standing_rules.md`.** Rule 5 (vocabulary quarantine enforced at wrap-ups and celebratory moments) is the enforcement standing rule; this document is the content the rule enforces against.

---

## Section 1: Prohibited terms (hard quarantine)

The following terms are prohibited across all layers, all artifacts entering the canonical record, and all conversational material that may be distilled into the canonical record. Rule 5 applies these prohibitions with extra care at wrap-ups, synthesis moments, and celebratory phrasing — where drift is most likely.

### Agent-behavioral vocabulary (excluded by the HARD CORE)

The theory's primitive observable is **ACTION**, not decision. The following terms are prohibited when describing agents or the structural bases.

- **"decision"** (when applied to agents). Agents do not decide to participate; they act or don't. The action stream is shaped by structural conditions (v, c, r) but agents have no decision function admitting structural conditions as input.
- **Any optimization language applied to agents.** No "maximizing," "minimizing," "optimizing," "selecting the best," etc. The theory excludes optimization frameworks by design.
- **Any utility language applied to agents.** No "utility," "preference," "valuation," "expected value," etc. Agents are not utility-bearing entities in this framework.
- **Any cognitive-response language applied to agents.** "Perceiving," "evaluating," "responding to" (in a cognitive sense), "interpreting" — all prohibited when describing how agents engage structural conditions. The structural-conditions-shape-action-streams relation is not cognitive.

### Architectural-vocabulary drift (excluded by formal commitments)

- **"terrain favorability"** — drifts the structural bases (v, c, r) into a single composite property, collapsing the architecture's multi-base structure into a scalar field. The bases are independent by construction; "terrain favorability" reads them as components of a single quantity.
- **"viability-seeking"** — agent-teleological framing; agents do not seek viability or anything else. Cognitive-response vocabulary applied to agents.
- **"alignment"** (in the agent-behavioral sense). When used for agent behavior matching structural conditions, this is decision/cognitive vocabulary. The term is permitted in protocol-discussion contexts ("Layer 2's review aligned with Layer 1's framing") where it refers to AI/process alignment, not agent behavior.
- **"homeostatic imperative"** (as a formal primitive). May appear in informal discussion of biological analogy; never as a formal primitive of the theoretical architecture. The architecture's formal elements include ACTION as primitive observable, structural bases, activation drive, coherence, and the slow-timescale Q operator — homeostasis is not among them.
- **"autocatalytic"** — implies chemical-reaction self-reinforcement that the architecture does not commit to. The architecture has feedback structure through Q, but Q is not autocatalytic; the term imports a mechanism the theory does not include.
- **"field"** (in the physics-borrowed sense). The theory uses Λ, ρ, Ψ as scalar quantities on a discrete substrate. "Field" suggests continuum-physics formalism that the theory does not adopt as architectural commitment. Lake Vision history aside, "field" in the architectural document is drift toward physics-borrowed framing.
- **"entrainment"** — coordination-dynamics vocabulary (Kelso, HKB). The theory's coordination structure differs from HKB in three architectural ways (two-stage cascade vs single bifurcation, supercritical pitchforks vs saddle-node-like switching, Q-mediated terrain reshaping vs fixed potential). Citing Kelso at the approach level is fine; using "entrainment" as architectural vocabulary imports the HKB mechanism into a framework that does not commit to it.
- **"fraction of the population"** — population-share framing that obscures the substrate-level dynamics. ρ is a substrate-aggregated activation density, not a fraction of an unmodeled population.

### Formal-primitive substitution

- **"ρ_c"** — risks hardening the second transition into a threshold-crossing model. The architecture's second transition is a sign-change in μ(ρ), governed by dΨ/dt = μ(ρ)Ψ − γΨ³, not a crossing of a critical density value. Permitted only inside explicit clarifications of why the term is prohibited.
- **"saddle"** — appears in v1.4 of the State of the Theory only in an exclusionary clause. Using "saddle" in architectural prose suggests saddle-node dynamics that the architecture excludes. Permitted only in exclusionary contexts citing the v1.4 commitment.

---

## Section 2: Permitted framings

The framings below replace prohibited terms in standard architectural prose. Examples are provided to make the substitution concrete.

### Candidate language for empirical claims

- **"Candidate produces / fails to produce"** — never "confirms" or "demonstrates." The theory is a candidate framework; empirical results produce or fail to produce predicted patterns. Confirmation language presupposes the framework's truth, which is not the discipline.

Example: "Reg_01 produced the identity-recovery pattern predicted by the substrate construction chain." Not: "Reg_01 confirms the substrate."

### Architectural positioning

- **"Architecture provides a location within which existing EE research is situated"** — never "supersedes" or "replaces." The architecture is a generative framework that situates field-observed phenomena within formal structure. Existing field work is not being replaced; it is being given a structural location.

Example: "The architecture situates Boulder Thesis observations within the structural-conditions-to-coherence cascade." Not: "The architecture supersedes the Boulder Thesis."

### Causal attribution

- **"μ(ρ) has composite causes; [mechanism] is one likely contributor among multiple, not the sole mechanism"** — used when attributing structural effects to specific mechanisms. Narrative compression, geography-as-compression-mechanism, etc., are contributors; none is the sole cause.

Example: "Narrative compression is one likely contributor to μ(ρ)'s sign-change behavior, alongside geography-as-compression-mechanism and other candidates not yet specified."

### Geography framing

- **"Geography is a compression mechanism producing co-location of structural conditions, not a boundary condition or formal space"** — geography enters the theory as a compression mechanism, not as a coordinate space or as a boundary defining the system. The architecture is substrate-based and discrete; geography compresses the substrate into spatial patterns.

---

## Section 3: Drift-prone vocabulary (caution flags, not prohibitions)

The terms below are not prohibited but are drift-prone. They have specific meanings within the protocol or theoretical architecture and can drift toward less precise readings if used carelessly. Use with care; surface ambiguity when it arises.

### "Solid" (three-tier commitment terminology)

Means *canonically acceptable under current evidence — ready for the canonical record absent outstanding flags.* Does not mean *epistemically closed* or *immune to correction.* A solid conclusion remains subject to revision if new primary source surfaces a conflict; Rule 1's primary-source override is not suspended by tier status.

Drift risk: "solid" reading as finality. Watch for it at celebration moments. Layer 2 flagged this term as drift-prone during the pair-1 protocol primer review (session 9); the clarification is now in `protocol_primer.md` Section 3 and reflected here.

### "Convergence" (synthesis-stage terminology)

Means *substantive engagement between Layer 1 and Layer 2 leading to a shared position grounded in evidence both layers engaged with.* Does not mean *agreement that emerged from one layer reading the other's framing.* The framing-asymmetry pattern (primer Section 4) makes refinement-driven convergence the structural default; substantive convergence is the exception that requires deliberate framing-room from Layer 1.

Drift risk: claiming "convergence" when the actual phenomenon is refinement-driven agreement. Rule 6 (no-preserved-divergence is a finding to track) is the corrective discipline.

### "Central node" (Layer 1 role terminology)

Means *Layer 1's coordinating/enforcement role across the protocol*; does not mean *Layer 1 is the privileged source of truth.* Primary source and Mike's arbitration remain above Layer 1. The role is process-coordinator, not epistemic-final-word.

Drift risk: "central node" reading as authority concentration. Watch for it when Layer 1 is producing synthesis documents that Mike will not independently verify against primary source.

### "Verification" (Rule 1 discipline terminology)

Means *primary-source check against the actual artifact (file, code, document, git log, parquet metadata).* Does not mean *memory description that sounds verified.* The distinction is the working-memory pattern's load-bearing line.

Drift risk: declaring "verified" when the verification was a working-memory consistency check rather than a primary-source touch. The discipline is: if Claude did not literally read the file/run the command/check the log, the claim is not verified.

### "Stage" (restructure-process terminology)

Means *one of the named stages of the repository restructure committed in session 6* (Stage 0 freeze and inventory, Stage 1 add orientation spine, Stage 2 move canonical artifacts, Stage 3 add manifests, Stage 4 quarantine stale material, Stage 5 resume analytical work). Does not mean *phase of work in a general sense*; "stage" as protocol vocabulary refers specifically to the committed sequence.

Drift risk: using "stage" loosely for any chunk of work, which obscures whether the discussion is about restructure stages or about something else. Use "phase," "step," or "cycle" for non-restructure work.

### "Open Element" (theoretical-architecture labeling)

Means *one of the four open elements of the committed architecture*: μ(ρ), F(v,c,r), Q, and the nucleation mechanism. Does not mean *any open theoretical question that could be assigned a number.* New "Open Element N" labels (where N is not one of the committed four) are vocabulary drift, not legitimate architectural commitments; numbering can falsely harden, reorder, or reify open theoretical commitments that have not been ratified.

Drift risk: a numeric Open Element label appearing in a routing artifact, operations log, or Layer 3 output, framed as if it were architectural commitment when it is local working vocabulary. Session 5 surfaced this pattern with "Open Element 14," which was quarantined and restated in committed vocabulary as "the architectural selection between F_LR and F_2_symmetric for the functional form of F(v,c,r)."

Discipline: if a numeric Open Element label appears that does not map to the committed four, quarantine the label, restate in committed terms (the architectural element being referred to), and surface to Mike. Restatement preserves the substantive question; quarantine prevents the numbering from becoming a parallel labeling system competing with the canonical four.

Future ratification: if Mike ratifies a new Open Element with formal architectural status, the State of the Theory document is amended accordingly and this entry updates. Casual numbering does not qualify.

---

## Section 4: Quarantine evolution

This document captures the state as of session 9 (2026-05-20). Items added or amended since the kit's prior summary:

- **Layer 2 review surfaced "solid" as drift-prone (session 9 pair-1 review).** Added to Section 3.
- **"Central node," "convergence," "verification," "stage" added to Section 3** based on session 6-9 operational experience.
- **Per-term rationale added to Section 1** for future Claude instances who instantiate without prior operations logs in context.
- **"Open Element" labeling discipline added to Section 3 (session 9 pair-2 review).** Layer 2 surfaced the omission; the discipline captures the "Open Element 14" quarantine/restatement pattern from session 5 as protocol-level vocabulary discipline.
- **"Homeostatic imperative" rationale tightened (session 9 pair-2 review)** to name ACTION as primitive observable explicitly, preserving the hard-core statement.

Future updates will be recorded here when committed.

---

— Drafted by Claude as Layer 1 central node, Stage 1 pair-2 of repository restructure, session 9. v2 incorporates Layer 2 review (Open Element discipline addition, "homeostatic imperative" rationale tightening). Pending Layer 2 acceptance of v2 before commit per `protocol_primer.md` Section 3's protocol-infrastructure routing convention.



---
# FILE: protocols\foundational\canonical_artifacts_index.md
---

# Canonical Artifacts Index

**Document role.** Authoritative index of the canonical artifacts that constitute the EE Theory Lab record. For each artifact, the index specifies: what it is, where it lives, and what authority it carries. This is the document a fresh Claude instance consults to locate primary source for any verification under Rule 1.

**Authority.** This document is authoritative for *where* canonical artifacts live and *what authority* they carry. It is not authoritative for the artifacts' content; each artifact is its own authority on its content domain. When this index conflicts with primary source (the actual files at the stated paths), primary source wins and this document revises.

**Maintenance discipline.** Updated when canonical artifacts are added, moved, or superseded. Updates committed alongside the operations log of the session in which the change occurred. Stage 2 of the repository restructure (moves canonical artifacts via `git mv`) will trigger a coordinated update of this index.

**Path conventions.** All paths relative to `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` unless absolute. PowerShell uses backslash separators; git status output uses forward slashes; both refer to the same files.

**Relationship to other foundational documents.**
- `protocol_primer.md` specifies who uses these artifacts and how.
- `standing_rules.md` specifies the disciplines (especially Rule 1) under which artifacts are consulted.
- `vocabulary_quarantine.md` specifies the language used when discussing the artifacts.

---

## Section 1: Theory-level documents

### State of the Theory v1.1

The committed theoretical architecture; ten sections; "hard core." Authority: formal theoretical commitments. Defines the four open elements (μ(ρ), F(v,c,r), Q, nucleation mechanism), the two-stage Landau cascade structure, the critical ontological constraint (ACTION not decision), and the architecture's exclusionary clauses.

**Path:** Mike's local file (not in the repository's tracked tree as of session 9).

**Operational locatability:** requires Mike-provided attachment for any verification-against-primary-source check. Stage 2 will move this to `theory\state_of_theory\state_of_theory_v1_1.md` per session 6's v1.1 naming-collision resolution; until then, Layer 1 cannot verify content claims about this document without explicit Mike-provided access.

**Citation:** "State of the Theory v1.1." Do not cite "v1.1" alone without qualifier — multiple v1.1 documents exist (see naming-collision note below).

### State of the Theory v1.5 Overview

Manuscript foundation Phil writes from; v1.4 MFA underneath. Authority: manuscript-facing material. The leading edge of the team's worked-out positions has moved past v1.5 in places (e.g., the flagged "modest-resources-outperform-abundant" passage); v1.5 absorbs back-flow from those developments as Phil revises.

**Path:** Mike's local file (not in the repository's tracked tree as of session 9).

**Operational locatability:** requires Mike-provided attachment for verification. No committed Stage 2 target yet; the v1.5 Overview's repository placement is a question for Mike to arbitrate when manuscript work surfaces a need.

**Citation:** "State of the Theory v1.5 Overview" or "v1.5 Overview" with context.

---

## Section 2: Phase 4B specifications

### Phase 4B Specification v1.1

Analytical procedures for Phase 4B: Tier 1 strict matching, Tier 2 coarser matching, Tier 3 interpretable regression with pre-specified interaction families, two-field empirical_result × structural_status classification, cross-scale analysis. Authority: Phase 4B analytical procedures.

**Path:** `phase_4b\phase_4b_specification_v1.1.md`

**Verified:** session 9.

**Citation:** "Phase 4B Specification v1.1."

### Flight 6 Substrate Specification v1.1

Substrate implementation: the cellular engine that produces .parquet telemetry. Sections 6 and 8 specify the deterministic probability chain (Drive_Raw → p_base → p_act → realization) that reg_01 recovered. Section 13.2 specifies the shadow-copy structure (F_2_symmetric runs at each scale produce one underlying parquet file, three probe-named files via byte-identical shadow copies; F_LR runs produce one parquet file each). Section 15 enumerates implementation prohibitions; the protocol-applicable subset is lifted to `standing_rules.md` Rule 7.

Authority: substrate implementation.

**Path:** `flights\flight_6\Flight6_Substrate_Specification_v1.1.md.pdf`

**Verified:** session 6 (located and read end-to-end), session 9 (path re-verified, Section 15 re-verified against primary source).

**Citation:** "Flight 6 Substrate Specification v1.1" or "FSS v1.1" with context.

---

## Section 3: Tier 3 canonical implementation

The Tier 3 implementation cluster committed at `3189ab7` (session 7 reconciliation). All paths under `phase_4b\scripts\`.

### Intake module

Implements the seven-item structural-correctness checklist per intake specification. Defines `NormalizedPrereg` dataclass, the schema validator, and the `attach_tier2_globals` merge function.

**Path:** `phase_4b\scripts\_phase_4b_intake.py`

**Commit:** introduced at `3189ab7`.

### Test suite

Demonstrates all five exception types fire on deliberate violations. Routes inputs through the actual validation pipeline (not via mock objects per Rule 7.2).

**Path:** `phase_4b\scripts\test_intake.py`

**Commit:** introduced at `3189ab7`.

### Refactored regression consumer

Contract-mediated per intake §1.6. Reads pre-registration yaml, normalizes via the intake module, attaches Tier 2 globals, executes the regression, writes outputs.

**Path:** `phase_4b\scripts\tier3_regression.py`

**Commit:** introduced at `3189ab7`.

---

## Section 4: reg_01 pre-registration and outputs

The committed reg_01 cluster. Pre-registration and outputs committed at `3189ab7`. The pre-registration's `interpretation_boundary` content was restored from session 5's log to the canonical yaml during session 7's reconciliation.

### Pre-registration

Schema is contract-mediated intake format. `derived_variables` block declares per-run/tick constructions for `Local_Density_squared`, `rho_global`, `psi_global`. `interpretation_boundary.licenses` list (5 items) and `does_not_adjudicate` (4 items) restored under new schema; substantive scope matches session 5's log.

**Path:** `phase_4b\pre_registrations\reg_01_scale_interactions.yaml`

**Commit:** `3189ab7`.

### Primary coefficients

**Path:** `phase_4b\tier3_outputs\coefs_reg_01_scale_interactions.csv`

**Commit:** `3189ab7`.

### Sensitivity coefficients

**Path:** `phase_4b\tier3_outputs\coefs_reg_01_scale_interactions_sensitivity_cell.csv`

**Commit:** `3189ab7`.

### Regression report

**Path:** `phase_4b\tier3_outputs\report_reg_01_scale_interactions.md`

**Commit:** `3189ab7`.

**Note:** the `tier3_outputs/` directory is at `phase_4b\tier3_outputs\` (sibling of `scripts/`), NOT `phase_4b\scripts\tier3_outputs\`. The kit-revision-1 had this wrong; corrected in kit-revision-2 and verified during session 7.

---

## Section 5: Substrate data and Tier 2 derived outputs

### Canonical substrate data

Eight Flight 6 production parquet files (Flight 2 naming inheritance preserved). Four genuine substrate runs plus four byte-identical shadow copies per Flight 6 Substrate Specification §13.2. PRNG_seed 128561948, substrate_version v1.1.

**Path (absolute):** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\`

**Note on naming:** the directory is named `flight2_outputs` for inheritance reasons, but contains Flight 6 files. The mismatch is documented at the canonical record level (here) and will be resolved during Stage 4 (quarantine and rename).

### Tier 2 derived outputs

65 files. Per-probe-scale derived outputs (8 metric types × 8 probe-scale combinations = 64 files) plus the merged `global_timeseries.csv` bridging artifact (13.5MB, the canonical Tier 2 → Tier 3 join surface produced by `merge_globals.py`; status confirmed canonical during session 8's Stage 0 inventory).

**Path:** `phase_4b\tier2_outputs\`

### Tier 1 reports

Eight Tier 1 reports across the four-probe × two-scale matrix.

**Path:** `phase_4b\tier1_reports\`

### Cross-run analysis outputs

Three cross-run analysis files dated 5/17/2026 morning.

**Path:** `phase_4b\cross_run_outputs\`

**Stage 0 status:** these three directories (`tier2_outputs/`, `tier1_reports/`, `cross_run_outputs/`) are categorized as canonical in `RESTRUCTURE_INVENTORY.md` (committed at `1a68ca6`); Stage 2 will execute `git mv` placement per the inventory's moves-plan.

---

## Section 6: Diagnostic and forensic-text outputs

Per the Stage 0 canonical diagnostics directory convention (adopted session 8), all diagnostic stdout, log, and forensic-text outputs go under `phase_4b/diagnostics/`. Stage 2 will execute the moves; current locations as committed in `RESTRUCTURE_INVENTORY.md`:

### Session 5 diagnostic stdout

**Path:** `phase_4b\diagnostic_stdout.txt`

**Note:** at `phase_4b\` (sibling of `scripts\`), NOT `phase_4b\scripts\diagnostic_stdout.txt`. The kit-revision-1 had this wrong; corrected in kit-revision-2.

### Session 6 t27 forensic output

**Path:** `phase_4b\t27_diagnostic_stdout.txt`

### Earlier cross-run comparison output

**Path:** `cross_run_comparisons_df9122e.txt` (workspace root, awaiting Stage 2 move to `phase_4b/diagnostics/`)

---

## Section 7: Operations logs and routing artifacts

### Operations logs

All committed. Paths under `operations_log\`:

| Session | Path | Commit |
|---------|------|--------|
| 1–4 | `operations_log\` (older naming) | various commits up to `5d91828` |
| 5 | `operations_log\2026-05-18_phase_4b_session_5.md` | `3189ab7` |
| 6 | `operations_log\2026-05-19_phase_4b_session_6.md` | `3189ab7` |
| 7 | `operations_log\2026-05-19_phase_4b_session_7.md` | `4e66f27` |
| 8 | `operations_log\2026-05-19_phase_4b_session_8.md` | `3e38980` |
| 9 | (pending; drafted at session-end) | (pending commit) |

### Layer 1 routing package (session 5)

The `LAYER_1_ROUTING_PACKAGE.txt` file at workspace root is a canonical-record candidate (from session 5's Layer 2 routing on reg_01 interpretation). Stage 2 will place it under an appropriate routing-archive path per `RESTRUCTURE_INVENTORY.md`.

### Stage 1 routing packages (session 9)

**Path (pre-Stage-2):** `LAYER_2_ROUTING_STAGE1_PAIR1.md`, `LAYER_2_ROUTING_STAGE1_PAIR1_V2_ACCEPTANCE.md` at workspace root.

These will move to a routing-archive path during Stage 2 alongside the session 5 routing package.

---

## Section 8: Stage 0 inventory and restructure planning

### RESTRUCTURE_INVENTORY.md

The Stage 0 deliverable. Categorizes the 31 untracked items as of session 8 inventory time into canonical (74 files counting subdirectory contents, including the two reclassified-canonical scripts `inspect_tier3_provenance.py` and `merge_globals.py`) and scratch (22 scripts at workspace root). Includes Stage 2 moves-plan, four open items for subsequent stages, and verification section recording both Layer 1 cross-check and Layer 2 sanity scan.

**Path:** `RESTRUCTURE_INVENTORY.md` (workspace root)

**Commit:** `1a68ca6`.

---

## Section 9: Foundational document set

The current document plus its peers in `protocols/foundational/`. Committed in Stage 1 of the restructure.

| Document | Path | Status |
|----------|------|--------|
| Protocol primer | `protocols\foundational\protocol_primer.md` | committed `79db966` |
| Standing rules | `protocols\foundational\standing_rules.md` | committed `79db966` |
| Vocabulary quarantine | `protocols\foundational\vocabulary_quarantine.md` | (this commit pending) |
| Canonical artifacts index | `protocols\foundational\canonical_artifacts_index.md` | (this commit pending) |
| Current state | `protocols\foundational\current_state.md` | (pending later Stage 1 work) |
| README | `protocols\foundational\README.md` | (pending later Stage 1 work) |

Root-level orientation documents (`ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`) and `STANDING_ITEMS.md` are also pending later Stage 1 work.

---

## Section 10: Instantiation kit

The compressed instantiation surface for fresh Claude chats. Becomes a derived/compressed surface over the foundational document set as Stage 1 completes; not authoritative on its own once Stage 1 is committed.

**Current revision:** kit-revision-2 (drafted at session 7 end). kit-revision-3 is pending Stage 1 work and will absorb the eleven kit-improvement items accumulated across sessions 7-9.

**Path:** typically delivered as a session-handoff artifact under `claude_session_handoffs\YYYY-MM-DD[-N]\` rather than committed to the repository tree. Whether the kit lives at a stable repository path or remains a handoff artifact is a question for kit-revision-3 to resolve.

---

## Section 11: Naming-collision and citation discipline

Three documents share the "v1.1" designation:

1. State of the Theory v1.1 (theoretical architecture)
2. Phase 4B Specification v1.1 (analytical procedures)
3. Flight 6 Substrate Specification v1.1 (substrate implementation)

**Citation rule:** Do not cite "v1.1" alone without a qualified document path or full document name. In code comments, citations like `# per v1.1 Section 13.2` are ambiguous; use `# per FSS v1.1 Section 13.2` or `# per Flight 6 Substrate Specification v1.1 §13.2`.

**The post-Stage-2 path commitment:** the three v1.1 documents will live at:

- `theory\state_of_theory\state_of_theory_v1_1.md`
- `phase_4b\specifications\phase_4b_specification_v1_1.md`
- `substrate\flight6_v1_1\specifications\flight6_substrate_specification_v1_1.md`

These are the targets; Stage 2 executes the moves. This document updates accordingly when Stage 2 commits.

---

## Section 12: Workspace and tools

### Canonical workspace

**Path:** `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` (lowercase nested).

### Stale parallel tree

**Path:** `C:\Users\vkz244\EE_Theory_Lab\phase_4B\` (capital B at top level). To be archived during Stage 4.

### Canonical data outputs

**Path:** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` (absolute; named for inheritance reasons, contains Flight 6 files; Stage 4 will resolve the naming).

### Tools

- **Mesa 3.x + SolaraViz** — ABM substrate environment.
- **VS Code** — text editor, pure-editor mode (AI-agent features unused per protocol convention).
- **PowerShell** — Windows shell. Note: `git --no-pager <command>` bypasses the pager when long output is expected; `q` exits the pager interactively.
- **Node.js / docx npm package** — Word document generation (used selectively for Phil-facing artifacts).
- **ReportLab** — PDF transcripts.
- **Python + NumPy** — analytical work, Tier 3 regression execution.

---

— Drafted by Claude as Layer 1 central node, Stage 1 pair-2 of repository restructure, session 9. v2 incorporates Layer 2 review (operational locatability notes added for Mike-local theory files). Pending Layer 2 acceptance of v2 before commit per `protocol_primer.md` Section 3's protocol-infrastructure routing convention.



---
# FILE: protocols\foundational\current_state.md
---

# Current State

**Document role.** Snapshot of the EE Theory Lab's current phase, latest substantive findings, open items, and next anticipated work. This is the document a fresh Claude instance consults to answer "where are we now?"

**Authority.** This document is authoritative for current-state orientation. When it conflicts with primary source (committed code, operations logs, the actual repository state), primary source wins and this document revises. Per Rule 1, current-state claims should be verified against `git log --oneline` and operational reality before being treated as load-bearing.

**Maintenance discipline.** Updated at session end. Volatile sections (those marked **As of session N**) are rewritten each session; stable structural content (the section headings, what each section tracks) changes only when the protocol's understanding of what's worth tracking evolves.

**Relationship to root-level `CURRENT_STATE.md`.** This document is the foundational-set version, scoped to load-bearing protocol-state material for AI instances and Mike. The root-level `CURRENT_STATE.md` is a higher-level orientation derivative aimed at the same audience but with broader scope (project-level state including manuscript-side context that is not strictly Phase 4B work).

---

## Section 1: Current phase

**As of session 9 (2026-05-20):**

The project is in the middle of a multi-stage repository restructure, committed across sessions 6-8 of Phase 4B. Stage 0 (freeze and inventory) was committed at `1a68ca6` during session 8. Stage 1 (add orientation spine — the foundational document set, root-level orientation documents, kit revision) is the current stage and is being executed during session 9.

Stage sequence (committed session 6):

- **Stage 0** — Freeze and inventory. **Committed at `1a68ca6`.**
- **Stage 1** — Add orientation spine. **In progress, session 9.**
- **Stage 2** — Move unambiguous canonical artifacts via `git mv`.
- **Stage 3** — Add manifests, especially for parquet outputs and substrate files.
- **Stage 4** — Quarantine stale and scratch material.
- **Stage 5** — Resume Phase 4B analytical work.

---

## Section 2: Latest substantive finding

**As of session 9 (2026-05-20):**

The most recent substantive analytical finding is from session 6: Tier 3 reg_01 is substantively complete as a pipeline-validation regression, with the R²=1.000 identity-recovery interpretation verified by primary-source review of the Flight 6 Substrate Specification v1.1 sections 6 and 8. The substrate's deterministic probability chain (Drive_Raw → p_base → p_act → realization) is what reg_01 recovered at machine precision; F_variant and scale enter only indirectly through Term_Lambda.

The reg_01 finding does not adjudicate the architectural selection between F_LR and F_2_symmetric for the functional form of F(v,c,r). F-form adjudication routes to macro-level analyses for the next analytical phase: aggregate trajectory comparisons, Ψ-structure analysis, Q-driven base drift, regime-transition timing, repeat-seed designs.

No analytical work has happened since session 6. Sessions 7-9 have been protocol infrastructure (reconciliation, Stage 0 inventory, Stage 1 foundational set drafting).

---

## Section 3: Open items

**As of session 9 (2026-05-20):**

### Stage 1 remaining (this session's work)

- Pair 3: `current_state.md` (this document) and `README.md` for the foundational set.
- Root-level orientation documents: `ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`.
- `STANDING_ITEMS.md` (deferred-items tracker per the bullet-proof deferral process).
- Kit-revision-3 (incorporates eleven kit-improvement items accumulated across sessions 7-9).

### Post-Stage-1 standing items

- **Pre-registration reproducibility verification.** Re-run `tier3_regression.py` against the committed yaml at `3189ab7`; diff outputs against committed reg_01 outputs. Trigger: first action of the session immediately following Stage 1 completion. Acceptance: diff output committed to operations log.
- **Push to origin.** Local main several commits ahead of origin/main. Trigger: post-Stage-1 natural commit cluster. Acceptance: `git push` reports success and `git log` confirms parity with `origin/main`.

### Post-restructure standing items

- **Next analytical phase decision.** Which macro-level F-form adjudication route (aggregate trajectory, Ψ-structure, Q-drift, regime-transition timing, repeat-seed) becomes the next pre-registered work. Mike arbitrates. Deferred until restructure complete enough to support analytical work.

### Cross-session items

- **Manuscript implications.** Phil's manuscript work is independent of Phase 4B's analytical phase. Whether and when the reg_01 finding lands in the v1.5 Overview is Phil's call. No action item from the protocol side.
- **Foundational set maintenance.** Each session-end checks for kit-revision triggers (working-pattern changes, current-state changes, canonical-artifacts changes). Rule 2 specifies the discipline.

---

## Section 4: Next anticipated work

**As of session 9 (2026-05-20):**

Within this session:

- Complete pair-3 (current_state + README) with Layer 2 full cycle.
- Root-level orientation documents (likely Layer 2 sanity scan rather than full cycle).
- `STANDING_ITEMS.md` (no Layer 2 routing — operational process artifact).
- Kit-revision-3 (likely Layer 2 sanity scan).
- Session 9 operations log.
- Session 10 handoff folder.

Next session (session 10):

- First action: pre-registration reproducibility verification per the trigger condition.
- Stage 2 execution: `git mv` operations per `RESTRUCTURE_INVENTORY.md` moves-plan.
- Push to origin if commit cluster is at a natural point.

Several sessions out:

- Stages 3-4 (manifests; quarantine).
- Stage 5 resumption: next analytical phase decision and pre-registration.
- ABM probe execution by Layer 3 (Gemini) once probe is specified.
- Substantive results analysis with Layer 2 (ChatGPT), likely from a fresh Claude session that has the committed substrate and analytical outputs as primary source.

---

## Section 5: Working-pattern state

**As of session 9 (2026-05-20):**

Working pattern committed in the kit as of kit-revision-2 plus additions surfaced during sessions 7-9. Kit-revision-3 will absorb the surfaced additions. Operational pattern:

- PowerShell commands delivered one per fenced block; Mike pastes one-click, runs, pastes output back.
- Visual demarcation after PS output: horizontal rule + bold "Response to your output:" label.
- File edits delivered as full-file overwrites; Mike downloads, moves into workspace via PS.
- File-system manipulation defaults to PowerShell (not File Explorer drag).
- Multi-file `present_files` delivery: Mike prefers separate-file downloads; Claude makes separate `present_files` calls.
- Session-handoff folder: `claude_session_handoffs/YYYY-MM-DD[-N]/` contains the kit and the just-closed session's operations log.
- Opening instruction to next-session Claude is a single sentence pointing at the kit; substantive operational knowledge belongs inside the kit.

---

## Section 6: Protocol state

**As of session 9 (2026-05-20):**

- HEAD: `6603799` (pair-2 commit). Local main 5 commits ahead of origin/main.
- Layer assignments: Claude = Layer 1 (central node), ChatGPT = Layer 2 (substantive review), Gemini = Layer 3 (implementation/execution). Mike arbitrates.
- Foundational document set: pairs 1 and 2 committed; pair 3 (current_state + README) in progress.
- Instantiation kit: kit-revision-2 (drafted at session 7 end); kit-revision-3 pending Stage 1 completion.
- Routing convention: full Layer 2 cycle for protocol-infrastructure routings includes v2-acceptance pass before commit (per `protocol_primer.md` Section 3); other full-cycle routings commit after Layer 1 incorporation.

---

## Section 7: How to update this document at session end

The volatile sections are 1-6 above. Each session-end update should:

1. Update **Section 1** if the current phase has changed (a stage closed or opened).
2. Update **Section 2** if a new substantive finding has landed in the canonical record.
3. Update **Section 3** by removing resolved open items, adding new ones, and updating session-numbered triggers and acceptance criteria where relevant.
4. Update **Section 4** to reflect new next-anticipated work.
5. Update **Section 5** if the working pattern has evolved (new conventions, retired conventions).
6. Update **Section 6** with new HEAD, new commits ahead of origin, new kit revision number, etc.

The **As of session N** marker at the top of each volatile section gets the new session number. The structural content (section headings, what each section tracks) is stable and changes only when the protocol's tracking discipline evolves.

---

— Drafted by Claude as Layer 1 central node, Stage 1 pair-3 of repository restructure, session 9. v2 incorporates Layer 2 review (Open Element 14 label removed and restated in committed terms; completed Section 15 lift item removed from open items; "confirmed" replaced with "verified by primary-source review"). Pending Layer 2 acceptance of v2 before commit per `protocol_primer.md` Section 3's protocol-infrastructure routing convention.



---
# FILE: operations_log\README.md
---

# Operations Log

This directory holds the operational record of decisions, gate closures, discipline events, and protocol additions across Cycle 2 substrate work.

## Entry conventions

- **Filename format:** `YYYY-MM-DD_topic.md`. Date is the date of the event, not the date of writing.
- **Authorship:** Entries are drafted by AI partners in collaboration with Mike, with the drafting partner noted at the bottom of each entry.
- **Honest record principle:** Entries reflect the operational record at the time of writing, including failures, miscalibrations, and corrections. Entries are not curated history. When a later entry corrects an earlier one, both stay in the log — the earlier entry is not retroactively edited.
- **Discipline notes:** Many entries include explicit notes on what the discipline structure caught and what it missed. These are part of the record, not editorial commentary.

## Cross-references

- **Substrate Spec v1.1:** `../flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf`
- **Architectural reviews:** `../protocols/architectural_reviews/`
- **Onboarding primers:** `../protocols/onboarding/`

## Standing rules (current as of 14 May 2026)

Five standing rules apply across all AI partners and all inference modes:

1. **No past-tense verbs for unexecuted actions on Mike's machine.** Acceptable forms: "The script to run is...", "Drafted for execution:", "Pending your run:", "Once you execute, expected output is..."
2. **No synthetic telemetry tables.** If a run hasn't happened, the table stays blank. Analytical predictions explicitly labeled as such are acceptable; emulated measurements formatted as data are not.
3. **Execution-verification at parity moments.** When an AI partner reports running code, the architectural review explicitly includes execution-status verification, not just primitive/vocabulary compliance.
4. **Asymmetric execution channel acknowledgment.** Mike is the only AI partner with an execution channel on the production machine. AI-partner-reported "results" are either tool-call outputs in their sandboxed environments (clearly labeled) or predictions/analyses about what Mike's execution would produce.
5. **Gate-closing artifacts route to all reviewing AIs.** Substantive working exchanges happen between Mike and one AI partner at a time. At every gate closure, the actual textual artifacts (terminal outputs, hash values, completion-verification reports, implementation files) route to all reviewing AIs before the next gate opens.



---
# MISSING FILE: protocols\onboarding\README.md
---



---
# MISSING FILE: protocols\architectural_reviews\README.md
---

