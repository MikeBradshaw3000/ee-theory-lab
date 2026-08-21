# Ops Log — Verification Rounds, Freeze, and Placement
**Session:** 2026-08-21 (continuous with the post-arbitration placement session), successor L1 conversation. Mike executing placement and all routings; L1 drafting and verifying.

## Sequence of record
1. v0.3 verification routing to L2 → **NOT CHECKABLE** (source not carried; see received-record and error 1 below).
2. Corrected self-contained packet (note + verbatim v0.3) → **source-level verification:** eight INTEGRATED AS REQUIRED; §5.1 integration defect (L2-5); §6.2 cross-section defect; two named blockers.
3. v0.4 produced: both corrections per L2's required substance ([v0.4/blocker-1], [v0.4/blocker-2]); changed-text round 1: both CORRECTED AS REQUIRED; new provenance blocker — header miscount "seven" (correct: eight; see error 3).
4. Header corrected; changed-text round 2: CORRECTED AS REQUIRED; **FREEZE MAY PROCEED**, no blocker standing.
5. **Mike froze Merge Specification v0.4, 2026-08-21.** Frozen edition produced (freeze stamp; amendment-by-versioned-successor rule; implementation-not-execution scope note; pre-stamp digest c48f36828a53fd58ae96f7a6fa138764a9396dbefb8f1936d34978a3af17156f preserved in the stamp). Frozen-edition digest: 39f66673657b0f429691c908142f889d9ef3d463a8372455cba95db7c486f52a.
6. This placement.

## Files placed this commit (digest gate published pre-placement; verified at destination)
`flights/mfa_fidelity/spec/`: MERGE_SPECIFICATION_v0_4_FROZEN.md — **the governing instrument specification**.
`flights/mfa_fidelity/routing/`: L2_V0_3_VERIFICATION_REQUEST.md (the defective reference-only routing, kept for the record); L2_V0_3_VERIFICATION_PACKET.md (the corrected self-contained packet); L2_V0_4_CHANGED_TEXT_NOTE.md; L2_V0_3_NOT_CHECKABLE_RECEIVED.md; L2_V0_3_SOURCE_VERIFICATION_RECEIVED.md; L2_V0_4_VERIFICATION_RECEIVED.md.
`flights/mfa_fidelity/`: this ops log.
Note: draft v0.4 (pre-stamp) is not separately placed; its exact bytes are recoverable from the frozen edition minus the stamp edits, and its digest is preserved inside the stamp. v0.2 and v0.3 remain in-repo from commit `4afa756` as provenance.

## Layer-1 errors this session (enumerated)
1. **Reference-not-carry routing.** First v0.3 verification request cited the repo copy instead of carrying the text — against the succession record's explicit channel fact (attachments to L2 unreliable; prefer inline/self-contained). Caught by L2's in-register NOT CHECKABLE refusal. Correction: self-contained packet; standing rule reaffirmed — every L2/L3 verification routing carries its source verbatim.
2. **(Carried from earlier in session, logged in prior ops log)** sed edit verified by wrong-occurrence grep.
3. **Provenance miscount.** Status header recorded "seven INTEGRATED AS REQUIRED" where the count was eight; caught by L2's numerical check at changed-text round 1. Correction applied and verified by zero-match grep on the erroneous word.
Pattern note: all three errors were caught by the verification architecture (L2 twice, direct read once) before any could propagate into a frozen or placed artifact. The catches ran in both directions this session — L1 catching L2's referent gap is not applicable here, but L2's catches of L1 are the adversarial layer functioning as designed.

## State at close
- **Merge Specification v0.4: FROZEN.** The instrument may now be implemented; no experiment may be seeded (contract-gated, per the freeze stamp and §11).
- Verification chain fully archived: v0.2 review → v0.3 source-level → v0.4 rounds 1–2 → freeze clearance.
- Next: E1 narrative telling (standing method, before E1's contract) → E1 contract under the pre-seed evaluability audit (R1 target freeze inside it) → substrate implementation per frozen §§1–9, Gate A first.
- Standing discrepancies unchanged (stage2 uncommitted; `0e32250`) — ABM-track business.
