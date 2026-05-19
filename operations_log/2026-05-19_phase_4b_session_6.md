# Operations Log: 2026-05-19 — Session 6: Forensic Chain Resolution; Substrate Specification Confirmation; Repository Restructuring Decisions

**Date:** 2026-05-19
**HEAD at session start:** unchanged from session 5 end (no commits between sessions)
**HEAD at session end:** unchanged (this log not yet committed; awaiting Stage 0 inventory)
**Session anchor for resume:** HEAD after this log commits, pending the restructure's Stage 0 inventory session

## Session arc

Sixth session. Opened with Mike's pre-commit caution flagging the t27 diagnostic file before any commits proceeded. The forensic chain that followed resolved several layered findings about Phase 4B canonical inputs and produced two substantial routing cycles (Gemini on substrate-specification reconciliation, ChatGPT on repository restructuring). Closed with reg_01 substantively complete, restructuring direction committed, and a foundational document set integrated into the restructure's Stage 1.

The session produced the third complete instance of the multi-layer protocol functioning on a substantive analytical question, and the first instance of the protocol surfacing what may be the deepest version of the working-memory pattern Phase 4B has encountered.

## Substantive findings

**Tier 3 reg_01 is substantively complete as a pipeline-validation regression.** The R²=1.000 identity-recovery interpretation from session 5 is confirmed by primary-source verification of the Flight 6 Substrate Specification v1.1 (located at `ee-theory-lab/flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf`). The substrate's deterministic probability chain (`Drive_Raw = Term_Lambda + Term_Density_Pos + Term_Overcrowding + Term_Offset`, `p_base = sigmoid(Drive_Raw)`, `p_act = p_base + eta * (1 - p_base)`) is specified at Sections 6 and 8 of that document. F_variant and scale enter `p_act` only indirectly through Term_Lambda; this is the construction reg_01 recovered at machine precision.

**The shadow-copy structure is specified, not drift.** Section 13.2 of the Flight 6 Substrate Specification specifies the shadow-copy structure: F_2_symmetric runs at each scale produce one underlying parquet file, and three probe-named files (probe1_overcrowding, probe2_starvation_F2sym, probe3_fusion_residual) are produced from that single run via byte-identical shadow copies. F_LR runs produce one parquet file each (probe2_starvation_FLR). Total: eight production output files from four underlying substrate runs. The substrate must "explicitly log when files are byte-identical shadow copies versus when they represent independent simulation runs," which is why the t27 diagnostic exists.

This means reg_01's canonical inputs (probe1_overcrowding for F_2_symmetric, probe2_starvation_FLR for F_LR, both scales) drew from the eight production outputs the spec defines. The probe-type labels in filenames are analytical-purpose labels per spec, not separate substrate conditions. The F_variant comparison reg_01 performed is what the spec intends as the substantive cross-variant comparison.

**The R²=1.000 finding's analytical scope, restated precisely.** The regression validates the Tier 3 intake and regression pipeline's ability to recover the substrate's deterministic local activation-probability construction. It does not adjudicate Open Element 14 (F_LR vs F_2_symmetric architectural selection), does not show that F_LR and F_2_symmetric are dynamically equivalent, and does not establish that scale or F-form are substantively irrelevant. The four-runs-no-replication design is sufficient for characterization but not for strong inferential claims about F_variant × scale at the cellular level.

F-form adjudication routes to macro-level analyses for the next analytical phase, per Layer 2's session 5 archival statement: aggregate trajectory comparisons, Ψ-structure analysis, Q-driven base drift, regime-transition timing, and repeat-seed designs if statistical inference becomes the goal. The next analytical phase decision (which route, which pre-registration) remains pending; this session did not engage it.

**Forensic chain that produced these findings.** Documented in detail because the chain itself is a load-bearing protocol record:

1. Mike's pre-commit caution flagged `t27_diagnostic_stdout.txt` as worth inspecting before any commits proceeded. The inspection revealed cross-run output describing a probe-distribution structure different from session 5's `diagnostic_stdout.txt`, suggesting the canonical inputs had not been stable.

2. Layer 1 routed the question to Gemini. Gemini's first diagnosis claimed "F_2_symmetric was never generated; generation was bypassed during cycle 6 hardening." This claim was substantively wrong but internally coherent — a working-memory-pattern instance.

3. Layer 1 verified against primary source via SHA-256 hash analysis of all eight parquet files in `flight2_outputs/`. At each scale, three files had identical hashes; one file (probe2_starvation_FLR) had a distinct hash. This established that shadow-copying exists but not which file was the source.

4. Layer 1 verified via parquet custom metadata that probe1_overcrowding contains F_2_symmetric data, not overcrowding data in some independent sense. Gemini's second diagnosis (that F_2_symmetric files were shadow copies of F_LR) was therefore also wrong — the F_2_symmetric file is its own generation, shadow-copied to other filenames; F_LR is the genuinely-distinct generation.

5. Layer 1 located `flight2_production.py`'s source code containing the `make_shadow_copies` function with explicit docstring `Make byte-identical shadow copies of the F_2_symmetric source for the probe1/probe2-F2sym/probe3 trio per v1.1 Section 13.2.` and a RUNS dictionary defining two genuine substrate generations per scale plus shadow-copy filenames.

6. Layer 1 confirmed that "v1.1" in the docstring refers to a substrate specification document, not the State of the Theory v1.1 (the latter has only 10 sections, no Section 13.2). After search, the Flight 6 Substrate Specification v1.1 was located in `ee-theory-lab/flights/flight_6/`.

7. Mike read Section 13.2 directly from primary source, confirming the shadow-copy structure as deliberate, specified, and serving defined analytical purposes.

8. Layer 1 read the Flight 6 Substrate Specification end-to-end (24 pages) for full context.

The forensic chain was the recurring cost of the unstructured repository. The same hour-plus chain would have been preventable with a properly-structured canonical record that surfaced filename-vs-content correspondences via manifests rather than requiring forensic inference.

## Procedural findings

**The working-memory pattern manifested three times in this cycle.**

Pattern instances during the session:

1. Gemini's first diagnosis (F_2_symmetric never generated): incorrect; primary-source hash analysis surfaced the actual shadow-copy structure.
2. Gemini's second diagnosis (F_2_symmetric files are shadow copies of F_LR): incorrect; primary-source metadata revealed the shadow source is probe1_overcrowding (which contains F_2_symmetric metadata), not F_LR.
3. Earlier session's probe-type confound framing: based on filename inference; primary-source Section 13.2 reading revealed the probe labels are analytical-purpose labels per spec, not distinct substrate conditions.

Each diagnosis was internally coherent and built a story that fit the broad shape of available evidence. None matched what primary source actually showed at the specific level. The corrective discipline — Layer 1 verifies primary source before accepting any Gemini diagnosis with substantial implications — operated successfully each time.

**The structural conclusion.** The working-memory pattern is not specific to particular failure modes (test code construction, fix-script imports, probe-type narrative). It's the same underlying pattern: AI working memory produces coherent narratives that occupy the space between known facts; when the narratives are routed downstream without source verification, they propagate.

The corrective discipline that has worked is the protocol-level commitment to primary-source verification. The discipline applies symmetrically to all AI partners including Layer 1; today's session did not surface a Layer-1-specific working-memory failure, but the discipline's symmetric application is the structural protection against ever encountering one.

**Repository state surfaced more structural issues than expected.**

Findings about the repository's current state, surfaced during forensic work:

1. Two parallel directory trees with confusingly similar names: `EE_Theory_Lab\phase_4B\` (capital B, top level) and `EE_Theory_Lab\ee-theory-lab\phase_4b\` (lowercase, nested). The canonical workspace for current Phase 4B work is the lowercase nested location. The capital-B tree is stale parallel structure.

2. Three documents share the "v1.1" designation: the State of the Theory v1.1 (theoretical-architecture document), the Phase 4B Specification v1.1 (analytical-procedures document), and the Flight 6 Substrate Specification v1.1 (substrate-implementation document). Code citations of "v1.1" do not disambiguate among them.

3. A directory called `flight2_outputs` containing only Flight 6 files. Naming inheritance from the Flight 2 baseline era, not deliberate.

4. A script called `flight2_production.py` that generates Flight 6 outputs. Same naming-inheritance pattern.

5. Filenames in the substrate output directory systematically misalign with content. probe1_overcrowding contains F_2_symmetric data; probe2_starvation_F2sym is a byte-identical copy of probe1_overcrowding; probe3_fusion_residual is another byte-identical copy of the same generation. The misalignment is spec-driven (per Section 13.2) but is not surfaced anywhere in the workspace where a fresh reader would find it without forensic work.

6. Approximately 20 scratch scripts at the workspace root from accumulated sessions, with no documentation explaining purpose or relevance.

7. 111+ uncommitted file changes per VS Code's source control panel, accumulated over multiple sessions without commit hygiene.

These findings were the substantive trigger for the repository restructuring routing to ChatGPT.

**Authorship-attribution finding on the Flight 6 Substrate Specification.**

The document's final authorship line ("Claude, drafted with Mike's three arbitrations and Layer 2/Layer 3 cross-review items embedded") and Section 16.2's layer-role assignments (Claude as Layer 3, ChatGPT as Layer 2) reflect the protocol as it stood on May 17, when the document was drafted. Between May 17 and the current session, Mike elevated Claude to a central-node coordinating role due to Layer 3 issues. The current protocol uses: Claude = Layer 1 (central node, architectural guardian), ChatGPT = Layer 2 (substantive analytical review), Gemini = Layer 3 (implementation and execution).

The substrate spec's content remains authoritative for substrate-implementation questions; the layer-attribution within it reflects a prior protocol state and does not require document revision. Future protocol artifacts use the current convention. This entry serves as the canonical record of the protocol-evolution discontinuity.

## Repository restructuring decisions

**ChatGPT's Layer 2 substantive recommendation adopted as-is.** The structure is phase-first hybrid with cross-phase substrate and protocol directories. The detailed recommended target structure is preserved at `phase_4b/reviews/layer2/2026-05-19_chatgpt_restructure_recommendation.md` (to be moved to canonical location during restructure execution).

**Stage sequence committed:**

- Stage 0: Freeze and inventory. Dedicated session. Produces `RESTRUCTURE_INVENTORY.md` documenting current working-tree state, categorization of each file (canonical / scratch / superseded), and a moves-plan for Stage 2.
- Stage 1: Add orientation spine. Root-level `ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`, and the foundational document set at `protocols/foundational/`.
- Stage 2: Move unambiguous canonical artifacts via `git mv`.
- Stage 3: Add manifests, especially for parquet outputs and substrate files.
- Stage 4: Quarantine stale and scratch material.
- Stage 5: Resume Phase 4B analytical work.

**Foundational document set committed as load-bearing component of Stage 1.** Located at `protocols/foundational/`, contains:

- `README.md` — one-click entry point and reading sequence.
- `protocol_primer.md` — multi-AI protocol, layer assignments, vocabulary discipline, standing rules summary.
- `current_state.md` — current phase, latest substantive finding, open items, next anticipated work. Updated at session end.
- `canonical_artifacts_index.md` — index of authoritative specifications and where they live.
- `vocabulary_quarantine.md` — prohibited terms and permitted framings.
- `standing_rules.md` — rule #6 and other protocol-level commitments.

Maintenance discipline: current-state updated at each session end. Other foundational documents updated when their underlying content changes (protocol evolution, vocabulary additions, new canonical artifacts, standing-rules amendments). Operations log entries explicitly include "Foundational set updates this session: [items]" when applicable.

**Section 15 prohibitions to be lifted to protocol-level standing rules.** The Flight 6 Substrate Specification's Section 15 lists prohibited substitutions, shortcuts, and evasions specific to substrate implementation. Many have direct analogues for protocol-level work (aggregate completion claims without per-artifact verification, memory-based reconstruction without canonical source verification, schema-emulation without engine-execution). These lift to `protocols/standing_rules/` during restructure execution, with citation back to substrate spec Section 15.

**v1.1 naming-collision resolution committed.** Three v1.1 documents will be located at:

- `theory/state_of_theory/state_of_theory_v1_1.md` (the State of the Theory)
- `phase_4b/specifications/phase_4b_specification_v1_1.md` (Phase 4B analytical procedures)
- `substrate/flight6_v1_1/specifications/flight6_substrate_specification_v1_1.md` (Flight 6 substrate spec)

Citation rule: do not cite "v1.1" without a qualified document path. The qualified citation rule becomes part of standing rules.

**Parquet output handling committed.** Manifests now, Git LFS decision later. Manifest format combines ChatGPT's Q4 recommendation with Section 14.1's verification structure from the Flight 6 Substrate Specification — one canonical manifest schema serving both purposes. Located at `phase_4b/outputs/parquet_manifest.csv` with documentation at `phase_4b/outputs/parquet_manifest.md`.

**Operations log naming convention.** ChatGPT recommended `YYYY-MM-DD_short-topic.md`; Layer 1 amended to preserve session sequence within phase. Convention: `YYYY-MM-DD_phase_NX_session_K.md` or similar. Resolution deferred to Stage 0 inventory session when the existing logs are reviewed.

## Items resolved

**Pending decision 1 from session 5 (next analytical phase).** Partially resolved. The route (macro-level analyses) was committed by Layer 2's archival statement. The specific path (which of aggregate trajectory / Ψ-structure / Q-drift / regime-transition / repeat-seed becomes the next pre-registered work) remains deferred until the restructure is complete enough to support the analytical work.

**Pending decision 2 from session 5 (working tree commit sequence).** Reframed and absorbed into the restructure. The Stage 0 inventory will produce the commit sequence as one of its deliverables.

**Pending decision 3 from session 5 (canonical workspace standardization).** Resolved by the restructure decision. The capital-B tree (`EE_Theory_Lab\phase_4B\`) will be moved to `archive/stale_trees/phase_4B/` during Stage 4.

**Pending decision 4 from session 5 (manuscript implications).** Resolved. The reg_01 identity-recovery finding, framed as pipeline validation rather than as F-variant adjudication, is methodologically sound. Phil engages it (or doesn't) per his own manuscript-work timeline. The protocol-correct framing is in hand; no overreach to walk back.

**Pending decision 5 from session 5 (Layer 1 boundary-crossing assessment).** Effectively absorbed into the central-node protocol shift. With Claude operating as Layer 1 central node coordinating across layers, boundary-crossings are an explicit feature of the role rather than deviations from strict layer-discipline. The pattern Mike's memory tracks ("authorship attribution travels when Mike decides it matters") continues to apply.

**Pending decision 6 from session 5 (substrate code as routine artifact for Layer 2 routings).** Resolved by restructure. Substrate code will live at `substrate/flight6_v1_1/source/` as a protected cross-phase canonical artifact. Layer 2 routings on Tier 3+ results can reference it by path; no separate per-routing inclusion needed.

## Items not resolved

**Stage 0 inventory.** Committed as a separate dedicated session. The session has not occurred yet. Pending for next session.

**Operations log entry for protocol-evolution discontinuity.** Mike noted today that he elevated Claude to central-node role due to Layer 3 issues. Stage 0 inventory should locate the operations log entry (if any) that documents the layer-role transition. If no such entry exists, Stage 0 inventory creates one retroactively to ground the protocol-evolution record.

**The next analytical phase decision.** Deferred until after the restructure. Standing entry on the post-restructure queue.

**Manuscript engagement timing.** Phil's manuscript work is independent of Phase 4B's analytical phase. Whether and when the reg_01 finding lands in the v1.5 Overview is Phil's call. No action item from the protocol side.

## Methodological observations

**The forensic chain was load-bearing protocol work.** Each step of the chain (pre-commit caution → t27 inspection → routing to Gemini → hash verification → metadata verification → source code verification → spec location → spec reading) was protocol discipline operating against a substrate problem that would have otherwise produced corrupted canonical record. The chain's substantive output (substrate spec confirmed, reg_01's analytical scope settled) is matched by its methodological output (the working-memory pattern's structural origin clarified, the corrective discipline reinforced).

The chain was expensive. Over an hour of forensic work to resolve questions that should have been answerable in five minutes from a properly-organized canonical record. That hour is the recurring cost of the unstructured repository, and it is exactly what the restructure is designed to eliminate going forward.

**Layer 1 central-node role functioning as intended.** With Mike's elevation of Claude to central-node coordinating role, Layer 1 took on responsibilities for primary-source verification, routing-package drafting, layer-by-layer review, and synthesis across returns. Today's session exercised all of these. The pattern that emerged: Layer 1 catches working-memory issues by demanding source verification before accepting downstream claims; Layer 1 produces routing packages that ask the right substantive questions of Layer 2 and Layer 3; Layer 1 synthesizes returns into actionable arbitration items for Mike.

The role is sustainable if (and only if) the foundational document set and the restructured repository support it. Without those, Layer 1's central-node responsibilities consume the kind of context-window budget that today's forensic work consumed. With them, Layer 1's responsibilities become tractable across sessions.

**The substrate specification's Section 15 prohibitions describe the same pattern class we've been operating against.** Section 15 of the Flight 6 Substrate Specification lists prohibited substitutions ("Schema-emulation without engine-execution," "Aggregate terminal completion messages without per-artifact verification," "Memory-based reconstruction of equations without canonical source verification") that, when read at protocol level, name the working-memory pattern explicitly. The substrate spec internalized the protective discipline for substrate implementation; the protocol needs to internalize it generally.

Lifting Section 15 prohibitions to protocol-level standing rules is therefore not just a cleanup move. It is the formal codification of discipline that has been operating informally across sessions. With it codified, new chats can apply the discipline from message one rather than reconstructing it through experience.

**Foundational document set as protocol infrastructure.** Mike's observation that cold-start cost is unsustainable named the structural problem: each new chat (in any layer) consumes most of its context budget on staging before producing useful work. The foundational set is the structural fix. Five documents at known location, loadable cheaply, sufficient for orientation. Maintenance discipline ensures the set stays current. Together, these reduce cold-start cost from "most of a session" to "first three messages of a session."

This is a substantial improvement in the protocol's session economics. Worth registering as a working-architecture finding alongside the seven-item checklist and the intake contract — another protocol-level instrument that makes the work tractable.

## Pending decisions for session 7

1. **Stage 0 inventory session.** Dedicated session focused exclusively on inventorying the current working-tree state, categorizing each file, and producing the moves-plan for Stage 2. Mike arbitrates session start.

2. **The protocol-evolution operations log location.** Stage 0 task to locate (or create) the operations log entry documenting the layer-role transition when Claude was elevated to central-node role.

3. **The next analytical phase decision.** Deferred until restructure is complete enough to support analytical work. Standing entry.

4. **Operations log naming convention final form.** Resolution deferred to Stage 0 inventory session.

5. **Foundational document set initial draft.** To occur during Stage 1 of the restructure. Each of the five documents in `protocols/foundational/` requires initial content. Layer 1 will draft when Stage 1 begins.

## Resume anchor for session 7

When this conversation resumes:

1. Verify HEAD: `git rev-parse HEAD` should return the commit of this log entry, once committed. Note: this log entry is itself part of the working tree state that Stage 0 inventory will handle.

2. Verify working-tree state: `git status --short` will show extensive uncommitted state. This is expected; the Stage 0 inventory session will produce the moves-plan that resolves it.

3. Read this log entry to orient.

4. First action: open Stage 0 inventory session as a dedicated session. Layer 1 will produce step-by-step inventory steps that work through the workspace systematically.

Standing items that span sessions: foundational document set drafting (Stage 1), the next analytical phase decision (post-restructure), manuscript implications (Phil's timing).

— Mike (drafted with Claude operating as Layer 1 central node, session 6 end operations log entry, post-forensic-chain-resolution and restructuring-direction commitment)
