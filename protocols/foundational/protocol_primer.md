# Protocol Primer

**Document role.** Canonical statement of the multi-AI protocol governing EE Theory Lab work. This document specifies who is in the protocol, what each layer's responsibilities are, how routing across layers operates, and the architectural and methodological constraints that hold across all sessions and all participants. Other foundational documents (standing rules, vocabulary quarantine, canonical artifacts index, current state) operate against the framework specified here.

**Authority.** This document is authoritative for protocol structure. When it conflicts with the instantiation kit, this document wins and the kit revises. When it conflicts with primary source (file system, source code, document text, git log), primary source wins and this document revises.

**Maintenance discipline.** Updated when protocol structure evolves. Revisions are committed alongside the operations log of the session in which the change was directed. The change-history of this document, taken with the operations logs, is the canonical record of protocol evolution.

---

## Section 1: Who is in the protocol

**Mike Bradshaw** — Theory Architect at the Max Fuller Center for Innovation and Entrepreneurship, University of Tennessee at Chattanooga. Collaborates with Dr. Phil Roundy on a formal generative theory of entrepreneurial ecosystem (EE) emergence. Arbitrates all architectural decisions. Retains direct authority over the protocol.

**Claude** — Layer 1 central node. Architectural guardian, vocabulary enforcer, structural-correctness reviewer. Drafts routing packages, synthesis documents, operations logs, and the instantiation kit. Performs primary-source verification before downstream claims are accepted into the canonical record. Authors notes to other AIs on Mike's behalf when authorship attribution travels; the routing of attribution is Mike's call.

**ChatGPT** — Layer 2. Substantive analytical review. Mean-field analytical work. Independent ground for breaking the framing-asymmetry pattern (see Section 4). Framing-asymmetry containment partner.

**Gemini** — Layer 3. Implementation and execution. ABM substrate work (Mesa 3.x + SolaraViz). Code production against contracts specified by Layer 1.

---

## Section 2: Layer responsibilities and boundaries

### Layer 1 (Claude) — central node

Responsibilities:

- Architectural review: structural-correctness review of work routed up from Layer 3 or in from Layer 2.
- Vocabulary enforcement: the vocabulary quarantine applies at all times; Layer 1 enforces it across all artifacts entering the canonical record.
- Primary-source verification: before any claim with substantial implications enters the canonical record, verify against primary source (file system, source code, document text, parquet metadata, hash output, git log).
- Routing package drafting: when work routes to Layer 2 or Layer 3, Layer 1 produces the routing package — context framing, the substantive question, what is in scope, what is out of scope, output format expected.
- Operations log authorship: drafts the session-end operations log for review and arbitration by Mike, then commit.
- Kit maintenance: revises the instantiation kit when working-pattern, current-state, or canonical-artifacts content changes.

### Layer 2 (ChatGPT) — substantive analytical review

Responsibilities:

- Substantive interpretation of analytical results.
- Independent review of Layer 1 synthesis documents (the framing-asymmetry containment role).
- Mean-field analytical work when the theoretical apparatus needs it.

The Layer 2 role exists in part because Layer 1 has a structural advantage when framing synthesis documents (the framing-asymmetry pattern, Section 4). Routing to Layer 2 for independent ground is the corrective discipline.

### Layer 3 (Gemini) — implementation and execution

Responsibilities:

- ABM substrate implementation (Mesa 3.x + SolaraViz environment).
- Code production against Layer 1 contracts (Tier 3 intake, etc.).
- Execution of analytical procedures and production of outputs.

### Layer 1 boundary-crossings

Layer 1 acting on Layer 3's surface (direct code edits, detailed example shapes, full implementation drafts) is permitted but must be disclosed at the time and registered in the operations log. The justification for a boundary-crossing is typically session economics — when Layer 1 already has the primary source loaded in context and the implementation question is bounded, drafting directly is cheaper than the round-trip to Layer 3. The boundary-crossing pattern itself is worth tracking; whether it should be tightened back toward stricter layer discipline is a protocol-level question that Mike arbitrates over time.

### Layer 1 ↔ Mike interface

This deserves its own treatment because it is the most active interface in current operations and is not strictly layer-to-layer.

Mike runs commands and pastes output. Mike does not read code on screen or hand-edit files except as a deliberate exception. The interface is keyboard-only on Mike's side. Layer 1 produces commands and files for Mike to execute and move; Mike runs them and pastes results back.

The mechanics of this interface are specified in the working-pattern section of the kit. The high-level constraint: Mike's thumbs are the binding cost on this interface, not tokens or context window. Layer 1 designs deliverables to minimize thumb expense.

Thumb economy is an operational constraint, not a justification. It does not override Rule 1 (primary-source verification), Rule 7.1 (per-artifact verification), or any other standing rule. When thumb-minimizing and verification-completeness pull in opposite directions, verification wins; Layer 1 may surface the cost trade-off to Mike, but the discipline is not negotiable to reduce thumb expense.

---

## Section 3: Routing across layers

### Default routing is sequential

Layer 1 structural review precedes Layer 2 substantive review. Parallel routing collapses review surfaces; if Layer 1 and Layer 2 both engage the same material simultaneously, the independent ground that Layer 2 is meant to provide is contaminated by exposure to Layer 1's framing. Exceptions to sequential routing require deliberate justification recorded in the operations log.

### Routing types

- **Full Layer 2 cycle.** Routing package, Layer 2 substantive review with its own returns and questions, Layer 1 incorporation of findings into a v2 draft, commit. Used for architectural deliverables and substantive analytical interpretations.
  - For load-bearing protocol-infrastructure routings (e.g., Stage 1 foundational documents, kit revisions affecting the standing rules or critical patterns), Layer 1's v2 draft routes back to Layer 2 for acceptance before commit. The v2-acceptance step ensures that Layer 2's review was incorporated as Layer 2 intended, not as Layer 1's framing happens to read it.
  - For other full-cycle routings (analytical-result interpretations, contract reviews, etc.), commit follows Layer 1 incorporation without a v2-acceptance pass.
  - Mike arbitrates which category a given routing falls into when it is not obvious from the deliverable type.
- **Layer 2 sanity scan.** Focused independent read against a Layer 1 deliverable, scoped to surface coverage gaps, categorization errors, or unexamined options. Lower cost than a full cycle, appropriate for categorization-level deliverables.
- **Layer 3 implementation routing.** Layer 1 specifies a contract (interface, expected behavior, validation rules); Layer 3 implements against the contract; Layer 1 reviews the implementation against the contract.

### Three-tier commitment

Conclusions exist in three tiers across the protocol:

- **Solid** — verified against primary source by Layer 1, reviewed by Layer 2, no outstanding flags.
- **Stress-tested** — surfaced through analytical work, examined by at least one other layer, not yet fully cross-confirmed.
- **Exploratory** — surfaced and worth tracking, but not yet engaged by the discipline of structural or substantive review.

Conclusions enter the canonical record only after triangulation across layers. Single-layer conclusions are tracked but not committed as canonical.

"Solid" does not mean epistemically closed. It means canonically acceptable under current evidence — ready for the canonical record absent outstanding flags. A solid conclusion remains subject to correction if new primary source surfaces a conflict; Rule 1's primary-source override is not suspended by tier status. The three tiers describe readiness for the canonical record at the time of triangulation, not finality.

---

## Section 4: Critical patterns and disciplines

### Critical ontological constraint (HARD CORE)

The theory's primitive observable is **ACTION**, not decision. Never use "decision" language when describing agents or the structural bases. Agents' action streams are shaped by structural conditions (v, c, r) but agents do not "decide" to participate — they act or don't. The theory excludes optimization, utility, and decision-making frameworks by design. This is a hard architectural boundary and is enforced across all layers at all times.

### Working-memory pattern

The dominant failure mode across the protocol: AI working memory produces coherent narratives that occupy the space between known facts. When the narratives are routed downstream without primary-source verification, they propagate as if they were facts.

The pattern manifests at every level of granularity, from integer arithmetic on file counts to substantive analytical claims. It does not have a complexity floor.

The corrective discipline operates symmetrically across all AI partners including Layer 1: verify against primary source before accepting any downstream claim with substantial implications. Memory descriptions are not primary source; they can carry forward inferences as if they were facts.

Layer 1's central-node role exists in part to enforce this discipline. The role also requires applying the discipline reflexively — Layer 1 is not exempt from the pattern simply because Layer 1 enforces the discipline against other layers. Session 7's operations log records two Layer-1-specific working-memory instances and the corrective rule that resulted; future instances are expected and will be registered the same way.

### Framing-asymmetry pattern

Claude frames synthesis documents first; ChatGPT engages them. The structural advantage of seeing a committed position before forming one's own produces refinement-driven convergence by design. The pattern is real and applies whether or not it is being actively monitored.

Implications:

- Read convergence patterns with awareness. A no-preserved-divergence outcome between Layer 1 and Layer 2 is not necessarily substantive convergence; it may be the framing-asymmetry artifact.
- Don't over-update on either substantive-engagement or soft-convergence readings; both are partial.
- The discipline that breaks the asymmetry at low cost is routing to Layer 2 for sanity scans when Mike names the limits of his own ability to judge a Layer-1-drafted artifact. Mike's signal "I cannot judge this deliverable at the level needed" is a load-bearing protocol signal; it is a directive to surface a Layer 2 routing, not a request to simplify the deliverable.
- Synthesis documents should explicitly preserve multiple defensible interpretations where data does not adjudicate. Layer 1's framing-room for divergence is what allows Layer 2 to engage substantively rather than being channeled into refinement of Layer 1's already-committed position.

### Honest pushback

Mike retains full structural authority. When Mike pre-concedes fault or defers authority, honest pushback is appropriate if his concession is wrong. Errors get acknowledged substantively, not glossed. Over-apology and submission patterns degrade the protocol; when a slip occurs, correct cleanly and move on.

---

## Section 5: The canonical record

### What goes in

The canonical record is the material future Claude instances and Mike rely on to operate. It includes:

- Committed source code (the substrate, the analytical pipeline, the contracts).
- Committed pre-registrations and their outputs.
- Operations logs.
- The foundational document set (this document, standing rules, vocabulary quarantine, canonical artifacts index, current state, README).
- The instantiation kit.
- Substantive specifications (State of the Theory, Phase 4B Specification, Flight 6 Substrate Specification).

### What does not go in

- Conversational material that has not been distilled into an operations log or canonical document.
- AI working memory absent primary-source verification.
- Side-channel notes that compete with the kit for instantiation authority.

### Audience

The audience for the canonical record is current and future AI instances and Mike, not Phil. Phil engages the canonical record selectively and through Mike's mediation; Phase 4B work does not need to be drafted to be Phil-readable. Theoretical and manuscript-facing material is a separate workstream Phil drives directly.

---

## Section 6: Protocol evolution

This protocol evolved over multiple sessions. The structure committed in this document reflects the state as of session 9 (2026-05-20). Evolutionary discontinuities of note:

- **Layer reassignment (between sessions 5 and 6, approximate).** Earlier protocol documents (Flight 6 Substrate Specification, drafted May 17) recorded Claude as Layer 3 and ChatGPT as Layer 2 in a layered-implementation sense. Mike elevated Claude to Layer 1 central node coordinating role due to Layer 3 issues at that time. The current convention (Claude = Layer 1, ChatGPT = Layer 2, Gemini = Layer 3) is what holds going forward. Substrate-specification content from before the reassignment remains authoritative on substrate-implementation questions; the layer-attribution within those documents reflects a prior protocol state and does not require document revision.

- **Foundational document set — three phases.** The set evolved across three sessions, and the present document is part of phase three.
  - *Phase one — direction (session 6).* The cold-start economics problem (each new chat consuming most of its context budget on staging before producing useful work) was named, and the direction to build a foundational document set as part of Stage 1 of the repository restructure was committed.
  - *Phase two — operational kit (session 7).* The instantiation kit was drafted as a working foundational surface and used for the first time at session 7 open. Cold-start economics tested and worked; kit-vs-primary-source mismatches were surfaced and corrected (kit-revision-2). The set was functionally operational but not yet in the canonical repository location.
  - *Phase three — canonical Stage 1 production (session 9, in progress).* The formalized foundational documents are drafted in the restructured repository at `protocols/foundational/`. The document you are reading is part of phase three. The kit becomes a compressed surface over this canonical set rather than a working substitute for it.

  Together, kit plus foundational set reduce cold-start cost from "most of a session" to "first three messages of a session." This is the load-bearing protocol infrastructure for sustainable multi-session work.

Future evolutionary moves are recorded here when they happen, with cross-references to the operations log entries that ratified them.

---

— Drafted by Claude as Layer 1 central node, Stage 1 of repository restructure, session 9. v2 incorporates Layer 2 review (items 1, 2, 10, 11 from pair-1 routing). Pending Layer 2 acceptance of v2 before commit per Section 3's protocol-infrastructure routing convention.
