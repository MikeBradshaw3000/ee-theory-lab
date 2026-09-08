# Proposal: Theory Development Annex (TDA)

**Status:** Protocol proposal for Mike's ratification. Establishes a storage and scrutiny channel for theory-development material that is firewalled from active flights but retrievable for future instrument design.

---

## 1. Purpose

Off-protocol discussions produce material of lasting value — architectural clarifications, candidate claims, future-instrument questions — that currently has no home. Committing it to the program record would contaminate active flights; leaving it in chat logs loses it. The Annex is the third place: durable, scrutinizable, and inert with respect to everything currently running.

## 2. Structure

A directory in the repository: `theory-annex/`, containing:

- `INDEX.md` — one line per entry: filename, date, one-sentence subject, status.
- Entry files, named `TDA-NNN_short_title.md` (e.g., `TDA-001_two_spaces.md`), numbered in order of admission.

Every entry carries a mandatory header:

```
Status: ANNEX — exploratory tier. Not citable in flight materials.
Origin: off-protocol discussion, YYYY-MM-DD.
Bearing: none on current contracts. Candidate input to future instrument design only.
```

## 3. Firewall rules (channel-and-citation, not epistemic quarantine)

The firewall governs channels and citations, not knowledge states. In a public repository, controlling what any reviewer's provider may have crawled is neither possible nor pretended; what is controlled is what carries standing and what enters a packet.

1. **No flight document may cite, reference, or depend on Annex content.** Contracts, specifications, gate materials, probe designs, and synthesis documents treat the Annex as noncitable. Candidate claims do not harden by citation.
2. **No review packet includes Annex material, and L2 is charged to review against the committed record only.** This preserves the self-containment test — a reviewed artifact must be complete on its own terms, with no background context silently filling gaps. What L2 has otherwise encountered is neither controlled nor relevant; the charge, not the reviewer's memory, defines the review's basis.
3. **Annex entries make no commitments.** Candidate claims inside entries are flagged as such and remain candidates regardless of how long they sit or how polished they read. Age and polish are not promotion.
4. **The specification remains the sole referent for the substrate.** Nothing in the Annex modifies, interprets, or glosses the spec.

## 4. Scrutiny

Annex entries are subject to scrutiny on Mike's initiative, decoupled from the flight cadence:

- **Internal:** revisiting an entry in later off-protocol discussion; revisions are committed as new versions with the old retained (v1 stays in the directory when v2 lands — same provenance discipline as elsewhere in the project).
- **External (optional, per entry):** Mike may route an entry to L2 for adversarial review *as an explicitly off-protocol request*, clearly labeled so the review generates no program record. NotebookLM may hold Annex entries as sources; its comments come to Mike alone, as always.

## 5. Promotion

The only path from Annex to program is explicit promotion, ratified by Mike:

1. Mike designates an entry (or a claim within one) for promotion.
2. The promoted content is rewritten as a proper program document — contract input, spec-change proposal, or architecture note — through the normal drafting channel. The Annex entry itself is never promoted verbatim.
3. The Annex entry's INDEX line is updated: `promoted → <target document>, YYYY-MM-DD`. The entry remains in the Annex unaltered, as provenance.

Natural promotion horizons: instrument design after the current calibration arc closes; the follow-up-paper track; the measurement-theory treatment of the normalization problem.

## 6. Charter entries

On ratification, admit as founding entries:

- `TDA-001_two_spaces.md` — the two-spaces note v2 (geographic space, base-space, action streams; district worked example; resolution-ladder question).
- `TDA-002_action_effects.md` — variable effects of actions on structural conditions (footprint/displacement decomposition; mayor example; the three legal representations — noise term, exogenous forcing, Q-realization; the flagged fourth option of direct micro-to-terrain coupling as a genuine extension). To be drafted from this conversation when Mike wants it.

## 7. What the Annex is not

Not a governance layer, not a shadow spec, not a backlog with implied obligations, not a channel to Phil, and not memory for the AIs — each entry must be self-contained enough to be read cold, because no future reader (human or AI) is guaranteed the conversation that produced it.
