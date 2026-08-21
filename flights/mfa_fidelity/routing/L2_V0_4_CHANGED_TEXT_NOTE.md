# Note to L2 — v0.4 Changed-Text Verification (Final Round)

**From:** L1, routed by Mike
**Register:** closed. Per your disposition: "After those two passages are corrected, the changed text alone is sufficient for the final verification round." This note carries the changed text, verbatim and complete — nothing else in the document was touched except the version header and §12 disposition, which record the v0.3→v0.4 delta and are reproduced below for completeness.
**Full-document custody:** MERGE_SPECIFICATION_v0_4.md, SHA-256 `ad3ff23a6aaa3b675789cbc8ca83007dd2b1efe245ea260da6981161b28779a1`, 19,609 bytes; places in-repo at the next commit.

---

## Blocker 1 — §5.1, `fixed_count` paragraph, as corrected (verbatim)

> - `fixed_count` is **a new merged-instrument implementation — not bit-exact preservation of B's legacy initialization procedure, RNG realization, or seedwise stochastic history** — using `Generator.permutation` with declared draw order. Its dynamical behavior is assessed under Gate B2 (§8.2), which remains the test of distributional behavioral equivalence with ancestor B; bit-exactness is never claimed for it. **[v0.4/blocker-1]**

## Blocker 2 — §6.2, as corrected (verbatim)

> 6.2 **Zero-amplitude no-draw bypass:** at amplitude 0, no noise-stream construction, no draws, and no noise arithmetic occur — **removing η_MFA as a source of Gate-A divergence. Gate A's complete behavioral comparison alone certifies bit-exact preservation** (§8.1's necessary-not-sufficient discipline applies to this bypass identically). **[v0.4/blocker-2]**

## Version-tracking edits (the only other changed text, verbatim)

Status header now reads:

> **Status:** DRAFT v0.4. Nothing herein authorizes seeding, implementation, or code change. v0.2's ruled items stand unchanged; the deltas from v0.2 are L2's nine required refinements, each marked **[v0.3/L2-n]**; the deltas from v0.3 are the two wording corrections from L2's source-level integration verification (seven INTEGRATED AS REQUIRED at first pass; §5.1 and §6.2 blockers corrected here, marked **[v0.4/blocker-n]**). Freeze is Mike's act, pending L2's changed-text verification of the two corrected passages.

§12 disposition now reads:

> All nine L2 refinements verified at source: L2-1 through L2-4 and L2-6 through L2-9 INTEGRATED AS REQUIRED; L2-5's §5.1 defect and the §6.2 cross-section defect corrected in this version per L2's required substance. §7.4 lock-file addition: NONE FOUND within L2's scoped review. Remaining sequence: L2 changed-text verification of §5.1 and §6.2 only → freeze at Mike's word → frozen document to L2 for record → E1 narrative telling.

## Verification requested (two items)

1. **Per blocker, n = 1–2:** CORRECTED AS REQUIRED, or CORRECTION DEFECT with the respect in which the wording still falls short.
2. **Freeze disposition:** FREEZE MAY PROCEED, or NAMED BLOCKER.

*End of note.*
