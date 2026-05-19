# Foundational Document Set

**This directory contains the canonical foundational document set for the EE Theory Lab multi-AI protocol.** New Claude instances instantiate from these documents at the start of each new chat. The set is load-bearing protocol infrastructure: it grounds vocabulary discipline, layer responsibilities, standing rules, and current-state orientation in a stable canonical location, replacing the working-memory reconstruction that earlier sessions had to perform at cold start.

This README is the entry point. It specifies the reading sequence, what each document is for, and how the set is maintained.

---

## Section 1: Reading sequence

For full instantiation against this foundational set, read the documents in the following order. (Note: at actual session open, the instantiation kit is the first read; this sequence is the order within the foundational set itself, consulted as substantive work develops or when the kit's compressed material needs canonical verification.)

1. **`protocol_primer.md`** — multi-AI protocol structure, layer responsibilities, critical patterns. Authoritative for protocol structure. Establishes who Mike, Claude, ChatGPT, and Gemini are in the protocol, what each layer does, and the disciplines that hold across all sessions.

2. **`standing_rules.md`** — protocol-level standing rules. Authoritative for rule content. Rules 1-10 with Rule 7 expanded as 7.1-7.7 (the Section 15 lift from the Flight 6 Substrate Specification). Operates against the protocol structure defined in `protocol_primer.md`.

3. **`vocabulary_quarantine.md`** — prohibited terms, permitted framings, drift-prone vocabulary. Authoritative for vocabulary discipline. Operates against the architectural ontology committed in the State of the Theory documents (which sit outside this set).

4. **`canonical_artifacts_index.md`** — where canonical artifacts live and what authority they carry. Authoritative for artifact locations; not authoritative for artifact content (each artifact is its own authority). The document a fresh Claude consults to locate primary source for any Rule 1 verification.

5. **`current_state.md`** — current phase, latest substantive finding, open items, next anticipated work. Updated at session end. Authoritative for current-state orientation; subject to primary-source verification under Rule 1.

The sequence is designed so each later document operates against the framework the earlier documents establish. Reading out of order is possible but produces uneven orientation — later documents reference disciplines and structures the earlier documents specify.

---

## Section 2: What each document is for

### `protocol_primer.md`

The reference document for any question about what the protocol *is*. Six sections: who is in the protocol; layer responsibilities and boundaries (including the Layer 1 ↔ Mike interface with its thumb-economy constraint); routing across layers (including the full Layer 2 cycle definition and the three-tier commitment structure); critical patterns and disciplines (ACTION not decision, working-memory pattern, framing-asymmetry pattern, honest pushback); the canonical record; protocol evolution.

When to consult: any structural question about layers, routing, or load-bearing disciplines.

### `standing_rules.md`

The reference document for any question about what *holds across* protocol operations. Ten rules with Rule 7's sub-numbering covering the Section 15 lift items. Includes Rule 1 (primary-source verification) and Rule 2 (session-end verification) as the most operationally active rules. Includes Rule 7.1-7.7 covering aggregate completion claims, schema-emulation, synthetic metadata, memory reconstruction, partial-completion framing, missing telemetry imputation, and required affirmations.

When to consult: any question about whether a given action satisfies protocol discipline; any session-end verification check.

### `vocabulary_quarantine.md`

The reference document for what to say and what not to say. Section 1 hard prohibitions (agent-behavioral vocabulary, architectural-drift terms, formal-primitive substitutions). Section 2 permitted framings with examples. Section 3 drift-prone vocabulary (caution flags rather than prohibitions): "solid," "convergence," "central node," "verification," "stage," "Open Element" labeling.

When to consult: any synthesis moment, wrap-up phrasing, celebratory framing, or commitment to canonical-record-bound prose.

### `canonical_artifacts_index.md`

The reference document for *where things live*. Theory-level documents, Phase 4B specifications, Tier 3 canonical implementation, reg_01 cluster, substrate data, Tier 2 derived outputs, diagnostics, operations logs, the foundational document set itself, the instantiation kit, citation discipline for the v1.1 naming collision, workspace and tools.

When to consult: any time Rule 1 primary-source verification requires locating an artifact; any time an artifact's authority status needs checking.

### `current_state.md`

The reference document for *what's happening now*. Current phase, latest substantive finding, open items, next anticipated work, working-pattern state, protocol state. Updated each session end; volatile sections marked **As of session N**.

When to consult: at the start of a session (after reading the kit) to orient on current work; at session-end to update for the next session.

---

## Section 3: Relationship to the instantiation kit

The instantiation kit is a compressed surface over this foundational set, designed for cold-start cost reduction. At session open, a fresh Claude reads the kit first (it's the document Mike attaches to start a chat) and then verifies against the canonical foundational set as needed.

The relationship is:

- **Kit summarizes; foundational set is canonical.** When the kit and a foundational document disagree, the foundational document wins.
- **Kit revises faster; foundational set is more stable.** Kit revisions happen as working-pattern observations accumulate; foundational documents change when canonical content changes.
- **Kit is the cold-start entry; foundational set is the deep reference.** The kit gets Claude operational within the first three messages of a session; the foundational set is consulted as substantive work develops.

Kit-revision-3 (drafted during session 9) absorbs kit-improvement items surfaced during sessions 7-9 and reflects the now-committed foundational set.

---

## Section 4: Maintenance discipline

Each foundational document specifies its own maintenance discipline in its header. The set-level discipline is:

- **Session-end check (Rule 2).** At session close, Layer 1 explicitly considers whether any foundational document needs revision based on the session's events. If yes, the revision is committed alongside the operations log.
- **Volatile-content protocol.** `current_state.md` is the most actively updated document; its **As of session N** markers must be refreshed each session end. The other foundational documents update only when underlying content changes (new standing rule ratified, vocabulary entry added, canonical artifact moved, etc.).
- **Kit revision pattern.** When working-pattern changes surface that the kit should incorporate, the kit revises in the same session as the operations log. Substantive operational knowledge belongs *inside* the kit, not in side-channel notes (per Rule 2's opening-instruction discipline).

---

## Section 5: Adding new documents to the foundational set

The set is intentionally small. Adding a new document requires:

1. Mike ratifies the addition.
2. The new document is drafted by Layer 1.
3. Layer 2 full cycle review (these are load-bearing protocol-infrastructure documents).
4. v2-acceptance pass after Layer 1 incorporation.
5. Commit alongside the operations log of the session in which the addition occurred.
6. This README updated to include the new document in the reading sequence and the per-document summary section.

Removing a document follows the same arbitration discipline: Mike ratifies the removal; the document is archived rather than deleted; this README updates.

---

## Section 6: Audience

This set is read by:

- Future Claude instances at session open.
- Mike, when needing to verify protocol claims against canonical material.
- Layer 2 (ChatGPT) and Layer 3 (Gemini), when their routings require protocol-structure context.

Phil is not the audience for this foundational set. The set is Phase 4B and protocol-infrastructure material; Phil engages it only through Mike's mediation, when relevant to manuscript work. This does not mean Phil is outside the audience for theory-level or manuscript-facing artifacts indexed elsewhere (notably the State of the Theory documents and the v1.5 Overview); those remain Phil-relevant through the manuscript workstream Phil drives directly.

---

## Section 7: Provenance

The foundational document set was committed in Stage 1 of the repository restructure during session 9 (2026-05-20):

- Pair 1 (`protocol_primer.md`, `standing_rules.md`) committed at `79db966`.
- Pair 2 (`vocabulary_quarantine.md`, `canonical_artifacts_index.md`) committed at `6603799`.
- Pair 3 (`current_state.md`, `README.md`) pending Stage 1 commit.

The set's design (cold-start cost reduction; canonical content; maintenance discipline) was committed in session 6 as part of the restructure decisions. The first kit-driven cold start happened in session 7 (kit-revision-2). The canonical Stage 1 production happens in session 9.

---

— Drafted by Claude as Layer 1 central node, Stage 1 pair-3 of repository restructure, session 9. v2 incorporates Layer 2 review (reading-sequence-within-set vs kit-cold-start clarification in Section 1; audience clarification distinguishing foundational set from theory-level material in Section 6). Pending Layer 2 acceptance of v2 before commit per `protocol_primer.md` Section 3's protocol-infrastructure routing convention.
