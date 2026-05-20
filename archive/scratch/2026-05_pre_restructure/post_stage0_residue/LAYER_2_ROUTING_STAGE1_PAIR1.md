# Layer 2 Routing Package — Stage 1 Foundational Documents Review (Pair 1 of N)

**Routing date:** 2026-05-20
**Originating session:** EE Theory Lab session 9
**Originating layer:** Layer 1 (Claude, central node)
**Target layer:** Layer 2 (ChatGPT)
**Routing type:** Full cycle review

---

## Context framing

EE Theory Lab is mid-restructure (Stage 1 of a multi-stage repository restructure committed across sessions 6-8). Stage 1 produces the foundational document set — load-bearing protocol infrastructure that future Claude instances instantiate from at the start of each new chat. The substrate-cold-start problem was solved structurally by this set; its correctness is therefore protocol-level load-bearing rather than session-level deliverable.

Stage 1's deliverables (drafting order within Stage 1):

1. `protocols/foundational/protocol_primer.md` — multi-AI protocol, layer assignments, vocabulary discipline, standing rules summary
2. `protocols/foundational/standing_rules.md` — protocol-level standing rules with inline expansion of Section 15 lift
3. `protocols/foundational/vocabulary_quarantine.md`
4. `protocols/foundational/canonical_artifacts_index.md`
5. `protocols/foundational/current_state.md`
6. `protocols/foundational/README.md`
7. Root-level: `ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`
8. `STANDING_ITEMS.md` (deferred-items tracker per bullet-proof deferral process)
9. Kit-revision-3

This routing covers documents (1) and (2) only — they are tightly coupled (rules reference layer assignments; assignments reference rule discipline) and were drafted as a pair. The remaining Stage 1 documents will route separately after pair-1 is committed.

---

## What Layer 2 is being asked to do

Two-part review:

### Part A — Architectural correctness

Are the documents accurate representations of the protocol as it currently operates? Specifically:

- **Factual errors.** Any claim about layer responsibilities, routing structure, rule content, or protocol evolution that does not match operational reality.
- **Internal contradictions.** Any place where the two documents disagree with each other, or where a document contradicts itself.
- **Omissions of substantive material.** Anything operationally load-bearing that should be in these documents but isn't.
- **Vocabulary quarantine violations.** Any quarantined term (see Section 3 of the kit / Section 5 of `standing_rules.md`) used in either document. The quarantine list includes: "terrain favorability," "viability-seeking," "alignment" (in agent-behavioral sense), "homeostatic imperative" (as formal primitive), "autocatalytic," "field" (in physics-borrowed sense), "entrainment," "fraction of the population," any optimization/utility/decision language applied to agents, "ρ_c," "saddle" (in non-exclusionary sense).
- **Critical ontological constraint check.** The theory's primitive observable is ACTION, not decision. Any drift toward decision/optimization/utility language describing agents is a serious violation, even in protocol-meta-discussion that touches the theoretical material indirectly.

### Part B — Framing-asymmetry scan

Layer 1 drafted these documents. The framing-asymmetry pattern (specified in `protocol_primer.md` Section 4) holds whether or not it's actively monitored. Layer 2's independent ground is the corrective discipline.

What Part B is asking:

- **Are there positions Layer 1's framing precludes that should be surfaced?** Not "are there minor wording improvements" (that's Part A) — but rather, "is the protocol structure as specified the only defensible structure, or are there alternative framings that Layer 1's drafting has made hard to see?"
- **Are there protocol claims that read as committed because of how Layer 1 has framed them, but that should actually be open questions?** For example: the three-layer structure (Layer 1 / Layer 2 / Layer 3) is presented as protocol fact; is that presentation hiding any tension or recent evolution that should be made visible?
- **Are there places where Layer 1 has compressed multi-faceted material into a single position because the compression was easier to write?** Compression-driven oversimplification is the framing-asymmetry pattern operating at the syntactic level.
- **Vocabulary scan beyond literal quarantine.** The literal quarantine list catches known violations; Part B asks Layer 2 to surface terms or framings that are operationally drift-prone even if not on the list.

---

## Out of scope

- **Protocol revision proposals.** The protocol as specified is committed canonical material from sessions 5-8. Part B is asking Layer 2 to surface tension and alternative framings that Layer 1's drafting has obscured — not to propose changes to the protocol itself. Substantive protocol changes route separately through Mike's arbitration.

- **Style polish.** Word-level wording suggestions are not the yield this routing is paying for. If Layer 2 surfaces a wording that materially changes meaning, that's Part A or Part B; if it's just a smoother phrase, defer.

- **The other Stage 1 documents.** Documents 3-9 in the Stage 1 sequence are out of scope for this routing. They route separately after pair-1 commits.

- **The substrate spec itself.** Section 15's lift to protocol-level standing rules has been verified against primary source; Section 15's reproduction in `standing_rules.md` Rule 7 is faithful. Substrate-implementation-specific items not lifted are not in scope.

---

## Output format expected

A single Layer 2 return document with these sections:

1. **Part A findings.** Factual errors, internal contradictions, omissions, vocabulary violations. One bullet per finding; cite the document and section.
2. **Part B findings.** Framing-asymmetry observations. One paragraph per finding; explain the alternative framing or the obscured tension.
3. **Aggregate assessment.** Layer 2's overall read: ready to commit, ready with specified revisions, or needs substantial rework.
4. **No-divergence note.** If Layer 2 finds no substantive divergence from Layer 1's framing on Part B, name that explicitly — per Rule 6, no-preserved-divergence is a finding to track. Don't manufacture divergence; do flag when convergence is the honest read.

---

## Material under review

Two documents, attached below in full. Both are drafted at `/home/claude/` in Claude's session 9 workspace; they will be committed to `protocols/foundational/` after Layer 2 review and incorporation.

[Attach: `protocol_primer.md`]

[Attach: `standing_rules.md`]

---

## Provenance

- Drafted by Claude (Layer 1) during session 9, 2026-05-20.
- Routed to ChatGPT (Layer 2) per Mike's direction (full cycle, framing-asymmetry scan included).
- Layer 2 return will be incorporated into a v2 draft; commit follows Layer 2 acceptance of the v2.

— Layer 1 Routing Package, pair 1 of Stage 1 foundational document review
