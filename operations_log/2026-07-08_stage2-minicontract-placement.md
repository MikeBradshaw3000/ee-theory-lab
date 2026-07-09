# Operations log - Stage 2 mini-contract arc (draft -> attack -> fork -> merge -> fidelity -> placement)

**Date:** 2026-07-08
**Session type:** Stage-2 mini-contract drafting and placement (continuing the session that committed the ratification / Stage-2 open at c5896b3, which carries its own committed ops log)
**HEAD at arc open:** c5896b3 (origin current, tree clean; re-confirmed after an interleaved Move B exchange)
**Arbiter:** Mike (sole execution channel)
**Drafting partner:** Claude (Layer 1)

## Arc scope note

Mike arbitrated "Reading 1" - this session's design work is the Stage-2 calibration mini-contract, not any prospective substrate probe. L1 surfaced the two readings as a fork before proceeding; the fresh-session recommendation for Stage 2 was noted as advisory and Mike proceeded in-session. A Move B (manuscript) exchange was interleaved earlier in the session; that track returned to hold pending Mike's materials (L1 diagnosis and fix plan delivered in-session, awaiting the v1.5 passage, destination section, and F-multiplicativity status).

## Source verification

PRESEED_EVALUABILITY_AUDIT.md was uploaded by Mike and digest-verified in the container against the committed canonical BEFORE any drafting: sha256 d2f12fada35d726a5039696cb06caa4687e5b6506e26749318577c1d601c432a, 32057 bytes - exact match. The review record was uploaded alongside and read. The mini-contract was drafted from the verified amendment text (all 183 lines read), not from the instantiation handoff's summary.

## Review lineage (full record in STAGE2_MINI_CONTRACT_REVIEW_RECORD.md)

1. **v1 (L1 draft).** Five fences (incl. the procedural-not-epistemic blindness formulation for the known-outcome problem), Case-1 input partition with pre-read-execution reconstruction point, eight-component instantiation procedure, four score items, completion semantics. Routed to L2 with five load-bearing questions.
2. **L2 attack: reject-with-blockers; architecture accepted.** Two concatenated passes, agreeing verdicts, one INTERNAL DIVERGENCE (reconstruction point). Five blockers: two-stage-vs-replay reconstruction; morphology-selection steering; score-item defects (incl. L1's answer-shaped "central estimate <= 1" on S3 - pessimistic-on-passing on L1's own scorecard, caught by the attack); unjustified R >= 100; Case-1-alone insufficiency.
3. **FORK 1 routed to Mike** (the multi-layer arcs' first preserved-divergence fork): Option A full two-stage reconstruction vs Option B single post-Amendment-1 + Section 4 currency-replay item. **Mike arbitrated OPTION B.**
4. **v2 (L1 full-acceptance merge).** All blockers and precision amendments folded, none contested; disclosed refinements D1-D5 reconciling the two passes' wordings. Routed for fidelity with three invited questions.
5. **L2 fidelity: CLEAN.** D1-D5 accepted; currency-replay adequate under Mike's arbitration; dual-floor S4 faithful; no F4 contradiction; no missing blocker, distorted fold, relaxation leak, TCOP reopening, or L4 movement. One non-blocking reminder carried: hostile build-review scrutiny of morphology-menu provenance at the implementation-spec stage.
6. **Mike placement arbitration.** L1 flagged the Section 5 completion-structure constraint on Mike's future option space before the freeze; **Mike explicitly accepted the constraint** ("i accept the constraint on my option space") and placed. The contract is CANONICAL and FROZEN; Case 1 (TCOP) is TRIGGERED.

## Files placed this session (this commit)

1. cycle3/wave_two/STAGE2_MINI_CONTRACT.md - canonical, frozen at placement (v2 content; status block updated to placed lineage).
2. cycle3/wave_two/STAGE2_MINI_CONTRACT_REVIEW_RECORD.md - review record (attack + fork + fidelity + disposition).
3. cycle3/RESUME_2026-05-30.md - anchor refresh: new supersession header (latest, 2026-07-08b) recording the placement, the fork, the score items, and the completion structure; 2026-07-08 demoted to carried; cold-start sequence updated for the calibration arc.
4. operations_log/2026-07-08_stage2-minicontract-placement.md - this file.

SHA-256 digests published in-session before placement, verified at destination by digest + size. Transit artifacts (v1, v2, both routing packets) are route-first artifacts superseded by the canonical contract and this record; not committed.

## State at arc close

- STAGE2_MINI_CONTRACT.md: CANONICAL, FROZEN. Case 1 TRIGGERED. Cases 2-3 named-not-triggered within Stage 2, Mike's call.
- Amendment: RATIFIED-PENDING-CALIBRATION, unchanged.
- Stage 2 completion requires >= 1 under-determined case AND >= 1 speaking case scored, or Mike's explicit recorded severity waiver (constraint Mike-accepted at placement).
- TCOP result: untouched, permanent, as always.
- Next arc: calibration implementation spec + harness; L2 hostile build review (morphology-menu provenance emphasis); Mike-executed. Opens on Mike's explicit call; fresh session recommended.
- Carried: both design questions (Mike's); 9-window rule unverified; CM-2; Rule E B/C; L4; Comparator 0; Lambda=0.20; no density-stability claim; Move B pending Mike's materials.

Drafting partner: Claude (Layer 1)
