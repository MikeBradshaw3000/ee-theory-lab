# Layer 2 Routing Package — Stage 1 Foundational Documents Review (Pair 2 of N)

**Routing date:** 2026-05-20
**Originating session:** EE Theory Lab session 9
**Originating layer:** Layer 1 (Claude, central node)
**Target layer:** Layer 2 (ChatGPT)
**Routing type:** Full cycle review (followed by v2-acceptance pass per protocol-infrastructure routing convention)

---

## Context framing

This is the second pair of Stage 1 foundational documents. Pair 1 (`protocol_primer.md` and `standing_rules.md`) was committed at `79db966` after full-cycle review + v2-acceptance. Pair 2 covers:

- `vocabulary_quarantine.md` — prohibited terms, permitted framings, and drift-prone vocabulary
- `canonical_artifacts_index.md` — authoritative index of canonical artifacts and where they live

Pairing rationale: the artifacts index references documents that the vocabulary quarantine governs (specifications use quarantined-or-permitted vocabulary; the index points at them; the quarantine specifies what's prohibited). Coupled review surfaces any vocabulary-vs-citation drift in one cycle.

These documents are protocol-infrastructure, not categorization deliverables. Full Layer 2 cycle applies; v2-acceptance pass follows per `protocol_primer.md` Section 3.

---

## What Layer 2 is being asked to do

Same two-part shape as pair-1: architectural correctness review plus framing-asymmetry scan. With pair-specific scope additions noted below.

### Part A — Architectural correctness

- **Factual errors.** Any claim about quarantined terms, permitted framings, file paths, commits, or canonical-artifact authority that does not match operational reality. Specifically for the artifacts index: paths can be verified against primary source if needed (the kit has had path drift before — sessions 7 and 9 surfaced and corrected entries). Layer 2 should flag any path that reads suspicious.
- **Internal contradictions.** Between the two documents, between either document and pair-1 (`protocol_primer.md`, `standing_rules.md`), or within a single document.
- **Omissions of substantive material.** Anything operationally load-bearing that should be in these documents but isn't.
- **Vocabulary quarantine violations.** This is recursive — `vocabulary_quarantine.md` itself must not use quarantined terms except in explicit exclusionary or example contexts. Verify carefully.
- **Critical ontological constraint check.** ACTION not decision; agent-behavioral vocabulary must be excluded. Both documents touch theoretical material indirectly.

**Pair-2-specific Part A items:**

- **Per-term rationale check (vocabulary_quarantine.md Section 1).** Each quarantined term has a one-sentence rationale attached. Layer 2 should verify the rationales are accurate and don't introduce new architectural commitments not already in the State of the Theory v1.1 or related canonical documents.
- **Drift-prone vocabulary section (vocabulary_quarantine.md Section 3).** This is a new structure not in the kit. Five terms flagged ("solid," "convergence," "central node," "verification," "stage"). Layer 2 should assess whether the flagged terms genuinely warrant caution-flag status and whether other terms should be added.
- **Citation discipline (canonical_artifacts_index.md Section 11).** The "v1.1" naming-collision discipline is committed in session 6 and reproduced here. Layer 2 should verify the citation rule is operational as stated.

### Part B — Framing-asymmetry scan

- **Are there positions Layer 1's framing precludes that should be surfaced?**
- **Are there claims that read as committed because of how Layer 1 has framed them, but should be open questions?**
- **Compression-driven oversimplification?** Layer 1 has compressed substantial vocabulary discipline and the entire canonical artifacts landscape into two documents; some compression is structurally required, but Layer 2 should surface places where the compression has obscured tension.
- **Vocabulary scan beyond literal quarantine.** Particularly relevant for these documents — they ARE the quarantine. Layer 2 should surface terms or framings operationally drift-prone in either document, including terms in Section 3 of the quarantine itself that might warrant graduation to Section 1.

**Pair-2-specific Part B items:**

- **Authority hierarchy clarity.** Both documents claim authority over their content domains and subordinate themselves to primary source. Is the authority hierarchy as specified the right one, or are there alternative framings? (E.g., is `canonical_artifacts_index.md` an authoritative index or a working description? The current draft says authoritative for *where* and *what authority*, not authoritative on *content*.)
- **The Open Element vocabulary discipline.** `vocabulary_quarantine.md` does not currently address the Open Element numbering pattern (the kit Section 3 has a paragraph about Open Element 14 quarantine and restatement). Should this discipline be in the quarantine document, or is it appropriate elsewhere?

---

## Out of scope

- **Protocol revision proposals.** Pair-1 already established the protocol structure.
- **Style polish.**
- **Other Stage 1 documents (3-N in the sequence).**
- **Re-litigation of pair-1.** `protocol_primer.md` and `standing_rules.md` are committed canonical material now. Cross-references from pair-2 to pair-1 are in scope; revisiting pair-1's content is not.

---

## Output format expected

Same as pair-1:

1. **Part A findings.** One bullet per finding; cite document and section.
2. **Part B findings.** One paragraph per finding; explain the alternative framing or obscured tension.
3. **Aggregate assessment.** Ready to commit / ready with specified revisions / needs substantial rework.
4. **No-divergence note.** Per Rule 6.

---

## Material under review

Two documents, attached below in full.

[Attach: `vocabulary_quarantine.md`]

[Attach: `canonical_artifacts_index.md`]

---

## Provenance

- Drafted by Claude (Layer 1) during session 9, 2026-05-20.
- Routed to ChatGPT (Layer 2) per pair-1's full-cycle convention.
- Layer 2 return will be incorporated into a v2 draft; v2 routes back for acceptance before commit per protocol-infrastructure routing convention.

— Layer 1 Routing Package, pair 2 of Stage 1 foundational document review
