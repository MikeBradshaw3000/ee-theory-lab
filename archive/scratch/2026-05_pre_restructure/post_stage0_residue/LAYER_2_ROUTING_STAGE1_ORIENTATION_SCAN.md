# Layer 2 Routing Package — Stage 1 Root-Level Orientation Documents (Sanity Scan)

**Routing date:** 2026-05-20
**Originating session:** EE Theory Lab session 9
**Originating layer:** Layer 1 (Claude, central node)
**Target layer:** Layer 2 (ChatGPT)
**Routing type:** Layer 2 sanity scan (lighter than full cycle; appropriate for derivative orientation material)

---

## Context framing

`protocols/foundational/` is complete after pairs 1, 2, and 3 (committed at `79db966`, `6603799`, `a8bc52c`). The current routing covers the three root-level orientation documents that are derivative of the foundational set: they compress and surface foundational-set material for higher-level orientation, without introducing new architectural commitments.

Three documents:

- `ORIENTATION.md` — repository entry point; what to read first depending on who you are; what the repository contains; authority hierarchy.
- `CURRENT_STATE.md` (root-level) — project-level current state; theoretical-architecture, manuscript-side, cross-workstream content. **Complementary** to `protocols/foundational/current_state.md` (Phase-4B-and-protocol scoped) with explicit cross-pointers.
- `MANIFEST.md` — top-level directory listing; what's canonical, what's pending Stage 2-4 of the restructure.

These are derivative material. The routing shape is sanity scan, not full cycle. The scope is narrower than pair-1/2/3 reviews.

---

## What Layer 2 is being asked to do

A focused sanity scan, not a full architectural review. Three specific things to check:

### 1. Coverage and consistency check

Do the three documents collectively cover what a fresh reader (Claude or human) needs at orientation level? And are they internally consistent — both with each other and with the now-committed foundational set?

Specific inspection points:

- **`ORIENTATION.md`'s "What to read first" section** lists four reader types (fresh Claude, anyone wanting protocol structure, anyone wanting current state, anyone wanting top-level layout) with pointers. Is the coverage complete? Is any audience missing or misrouted?
- **`CURRENT_STATE.md`'s complementary-not-duplicative claim.** The root-level CURRENT_STATE.md explicitly delegates Phase 4B and protocol state to `protocols/foundational/current_state.md`. Does the delegation work cleanly, or does the document leave gaps in project-level coverage by deferring too much?
- **`MANIFEST.md`'s top-level listing.** Does it accurately reflect the current directory layout? Does it correctly distinguish committed canonical material from pending Stage 2-4 material?

### 2. Vocabulary discipline check

Especially relevant given the pair-3 vocabulary violation (Open Element 14 label in current_state.md v1) that surfaced in the prior cycle. Layer 1's self-review failed to catch it; Layer 2's review caught it on first pass. The same self-review failure mode could be operating on these three documents.

Quick scan for:
- Quarantined terms (per `vocabulary_quarantine.md` Section 1): agent-behavioral decision/optimization/utility/cognitive-response language; architectural drift terms (terrain favorability, autocatalytic, field in the physics sense, entrainment, fraction of the population); formal-primitive substitutions (ρ_c, saddle in non-exclusionary use); Open Element labeling that doesn't map to the committed four.
- Drift-prone terms used carelessly (per `vocabulary_quarantine.md` Section 3): solid, convergence, central node, verification, stage, Open Element labeling.

### 3. Cross-pointer integrity check

These documents include many cross-pointers to the foundational set. Are the pointers accurate? For example:

- `ORIENTATION.md` Section "What to read first" points to `protocols/foundational/README.md` as the protocol entry. Correct?
- `CURRENT_STATE.md` Section 4 defers to `protocols/foundational/current_state.md` Sections 1-4 by number. Are those section numbers correct?
- `MANIFEST.md` cross-refers to `canonical_artifacts_index.md` Sections 2-6 and Section 11. Correct?

Flag any pointer that doesn't resolve to canonical material at the cited location.

---

## What Layer 2 is NOT being asked to do

- **Not a full architectural review.** These are derivative documents; the architecture is already committed in the foundational set.
- **Not a framing-asymmetry scan.** The Part B exercise from pair-1/2/3 is not applicable here — these documents are not establishing new positions, only surfacing existing committed material.
- **Not style polish.**
- **Not a v2 acceptance pass.** Sanity scan output goes directly to Layer 1 for incorporation; if no findings surface, commit follows directly. If findings surface, Layer 1 incorporates and commits without a second routing (since the material is derivative, not load-bearing on its own).

---

## Output format expected

A short return with three sections:

1. **Coverage and consistency findings.** Anything missing, mismatched, or contradictory.
2. **Vocabulary findings.** Quarantine violations (hard) or drift-prone-vocabulary cautions (soft).
3. **Cross-pointer findings.** Any pointer that doesn't resolve.

Plus an aggregate assessment: **ready to commit** / **ready with specified patches** / **needs reconsideration**.

If no findings, name the all-clear explicitly: "Sanity scan clear; orientation batch ready to commit."

---

## Material under review

Three documents, attached below.

[Attach: `ORIENTATION.md`]

[Attach: `CURRENT_STATE.md` (root-level)]

[Attach: `MANIFEST.md`]

---

## Provenance

- Drafted by Claude (Layer 1) during session 9, 2026-05-20.
- Routed to ChatGPT (Layer 2) per the lighter sanity-scan convention for derivative orientation material agreed by Mike.
- Layer 2 return will be incorporated directly; no v2-acceptance pass (the material is derivative and not load-bearing on its own).

— Layer 1 Routing Package, Stage 1 root-level orientation sanity scan
