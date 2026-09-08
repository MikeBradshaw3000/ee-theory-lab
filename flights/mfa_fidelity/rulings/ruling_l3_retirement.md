# Ruling: Retirement of L3 as a Standing Role; Restatement of the Blind-Rebuild Exercise

**Status: Ratified by Mike, 2026-09-06. Drafted off-protocol; enters the program record on commit. Prior records referring to "L3" remain unedited — they are historical and correct for their time.**

---

## 1. Ruling

**L3 is retired as a standing role.** No reserve instance is maintained, addressed, or referenced in ongoing governance. The three-layer naming (L1/L2/L3) in standing documents reduces, going forward, to L1 (design) and L2 (adversarial review), with Mike as sole execution channel and arbiter.

**The blind-rebuild exercise is retained**, renamed from its L3 association, and restated in Section 3. It remains named-not-triggered, sequenced at Mike's discretion.

## 2. Grounds

The role's purpose — preserving the ability to build the identical substrate in any environment for future researchers — is carried entirely by artifacts, not by an instance: the frozen specification (MERGE_SPECIFICATION_v0_4_FROZEN), the environment manifest, the sequence-preservation discipline, and Gate A as certification machinery. All are committed to a public repository (visibility made public by deliberate decision, May 2026). A sequestered instance adds nothing to this preservation: the operative asset was never a warm context but a commitment about what a future builder's context would contain — a procedural commitment, enforceable at commissioning time, requiring no standing party in the interim.

## 3. The exercise, restated

**Name:** the blind rebuild.
**Object:** demonstrate spec-canonicality — that the specification, not any codebase, determines the instrument — by having an independent builder produce the substrate from the specification and environment manifest alone, with bit-identity under the frozen environment as the verification target.
**Builder:** selected at commissioning, not maintained in advance. The builder's context contains the frozen specification and the environment manifest, and nothing else from the repository.
**Two-tier claim discipline:** the specification alone guarantees rebuild of the same dynamics in any environment (equivalence); the specification plus the frozen environment manifest guarantees the same numbers to the last bit (identity). All statements of the preservation mission use this two-tier phrasing; "identical in any environment" unqualified overstates what floating-point arithmetic supports.

## 4. Caveat recorded: procedural blindness in a public-repo era

Because the repository is public, any future AI builder may carry training exposure to the implementation. This does not void the exercise — procedural blindness (a commissioning context containing only the specification and manifest) remains meaningful and is the operative standard — but it weakens the strongest reading of "blind." The maximally clean form of the exercise is a human builder with the specification and no repository access; this option is recorded as available, and the choice of builder class is Mike's at commissioning. Any eventual write-up of the exercise states which form was run and what its blindness standard was.

## 5. Consequential edits

- TDA-000 (Annex protocol) §3 restated as channel-and-citation rules; the clause "L2 and L3 never receive Annex material" is superseded (amended this date).
- Standing governance descriptions (instantiation kits, orientation documents) drop L3 from the active-role list at their next natural revision; no retroactive edits to committed records.
- The NotebookLM briefing's governance summary is superseded on this point by this ruling wherever they differ.
