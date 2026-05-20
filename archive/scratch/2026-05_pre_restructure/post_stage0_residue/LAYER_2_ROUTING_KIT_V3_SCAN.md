# Layer 2 Routing Package — Kit-Revision-3 (Sanity Scan)

**Routing date:** 2026-05-20
**Originating session:** EE Theory Lab session 9
**Originating layer:** Layer 1 (Claude, central node)
**Target layer:** Layer 2 (ChatGPT)
**Routing type:** Layer 2 sanity scan (lighter than full cycle; appropriate for the kit as a compressed surface over the now-canonical foundational set)

---

## Context framing

The foundational document set at `protocols/foundational/` is committed (pairs 1-3 at `79db966`, `6603799`, `a8bc52c`). The root-level orientation documents are committed (`af59c33`). STANDING_ITEMS.md is committed (`5877486`).

This routing covers **kit-revision-3** — the compressed cold-start surface over the now-canonical foundational set. Kit-revision-2 (drafted at session 7 end) was the canonical surface in the absence of a committed foundational set. Kit-revision-3 is structurally different: it is a compressed pointer, not a canonical surface, and includes a working-pattern section that kit-revision-2 entirely lacked.

The routing shape is sanity scan rather than full cycle for two reasons:

1. The kit compresses material that has already been through full Layer 2 cycle + v2-acceptance (the foundational set, pairs 1-3). The canonical content is already Layer 2-accepted; what changes here is the compression form.
2. The kit's substantive new content (working-pattern section) captures operational mechanics from sessions 7-9 that Mike has been operationally exercising; the content is descriptive of existing practice rather than introducing new architectural commitments.

Eleven kit-improvement items accumulated across sessions 7-9 are absorbed into kit-revision-3. The full list:

1. Working-pattern section missing from kit entirely (now Section 3)
2. Memory 30-cap not mentioned (now Section 3 / Memory cap subsection)
3. PS-output visual demarcation convention (now Section 3 / Visual demarcation subsection)
4. File-delivery method (now Section 3 / File delivery subsection)
5. File-system manipulation defaults to PowerShell (now Section 3 / File-system manipulation subsection)
6. Session-handoff staging folder convention (now Section 3 / Session-handoff subsection)
7. Session-handoff folder must contain the just-closed session's operations log (now Section 1 + Section 3)
8. Opening instruction to next-session Claude is a single sentence (now Section 3 / Opening-instruction subsection)
9. Cold-start cost paid to enable work, not another cold start (now Section 3 / Cold-start economy subsection)
10. Multi-file delivery preference: separate files, not zips (now Section 3 / File delivery subsection)
11. Paste-back failure modes — PS commands as unambiguous paste-targets (now Section 3 / Paste-back failure mode subsection)

---

## What Layer 2 is being asked to do

Same shape as the orientation-documents sanity scan: focused checks, not a full architectural review. Three specific things to check:

### 1. Coverage and compression-fidelity check

The kit is compressed material drawn from canonical documents. Coverage check: does the compression preserve what new Claude needs at cold start? Compression-fidelity check: does the compression distort any canonical content?

Specific inspection points:

- **Section 1 (handoff folder vs canonical paths).** Does the listing of canonical paths match what was committed in pair-2 (`canonical_artifacts_index.md`) and the root-level `MANIFEST.md`? Any paths drifted or missing?
- **Section 2 (protocol summary).** Compressed from `protocol_primer.md`. Does the compression preserve the HARD CORE constraint, layer assignments, routing convention, and working-memory/framing-asymmetry patterns?
- **Section 4 (vocabulary quarantine summary).** Compressed from `vocabulary_quarantine.md`. The Open Element discipline is called out specifically (per the pair-3 vocabulary-violation lesson); does the summary capture the discipline at the right level?
- **Section 5 (standing rules summary).** Compressed from `standing_rules.md`. Ten rules with Rule 7's sub-numbering. One-line summary per rule. Does the compression land?
- **Section 6 (current state summary).** Short. Points to two canonical documents for full content.

### 2. New-content check (Section 3 working pattern)

Section 3 is new content not in kit-revision-2. It captures operational mechanics from sessions 7-9.

Specific inspection points:

- **PS delivery, visual demarcation, file delivery, file-system manipulation, paste-back failure mode, session-handoff convention, opening-instruction convention, cold-start economy, memory cap** — each is a subsection. Are they all operationally accurate?
- **Thumb-economy subordinacy.** The protocol primer Section 2 specifies that thumb economy is an operational constraint, not a justification (per pair-1's incorporation of your Part B item 10). The kit Section 3 captures the working-pattern material that operates under that constraint. Does Section 3 stay within the subordinacy — i.e., does it accurately describe the working pattern without implicitly elevating thumb-expense-minimization above other disciplines?

### 3. Vocabulary discipline check

Same concern as the orientation-documents sanity scan: Layer 1 self-review failed on the pair-3 vocabulary violation. Quick scan of the entire kit for:

- Hard quarantine violations.
- Drift-prone term use (Section 4 caution flags applied to the kit itself).

---

## What Layer 2 is NOT being asked to do

- **Not a full architectural review.** The architecture is already committed in the foundational set.
- **Not a framing-asymmetry scan in the Part B sense.** The kit doesn't establish new positions; it points at existing committed positions.
- **Not style polish.**
- **Not a v2-acceptance pass.** Per the sanity-scan convention, findings go directly to Layer 1 for incorporation and commit.

---

## Output format expected

Same as the orientation-documents sanity scan:

1. **Coverage and compression-fidelity findings.**
2. **New-content findings.** Anything in Section 3 that's operationally inaccurate or stays unclear.
3. **Vocabulary findings.**

Plus aggregate assessment: **ready to commit** / **ready with specified patches** / **needs reconsideration**.

If no findings, name the all-clear explicitly.

---

## Material under review

[Attach: `claude_instantiation_kit_v3.md`]

For context on what the kit compresses, the canonical foundational documents are committed at `protocols/foundational/`. Layer 2 has reviewed all six during sessions 6-9; the canonical content is Layer 2-accepted.

---

## Provenance

- Drafted by Claude (Layer 1) during session 9, 2026-05-20, after the foundational set, root-level orientation, and STANDING_ITEMS.md were committed.
- Eleven kit-improvement items from sessions 7-9 absorbed into kit-revision-3.
- Routed to ChatGPT (Layer 2) per the sanity-scan convention for compressed-surface material.
- Layer 2 return incorporated directly; no v2-acceptance pass.

— Layer 1 Routing Package, Kit-Revision-3 sanity scan
