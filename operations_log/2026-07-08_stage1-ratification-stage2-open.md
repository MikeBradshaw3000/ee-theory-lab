# Operations log - Stage 1 ratification and Stage 2 open (pre-seed evaluability audit arc)

**Date:** 2026-07-08
**Session type:** ratification / stage-open commit session (no substantive Stage-2 work performed)
**HEAD at session open:** bdbbb26 (origin current, tree clean)
**Arbiter:** Mike (sole execution channel)
**Drafting partner:** Claude (Layer 1)

## Grounding

Cold-start grounding completed clean: HEAD and origin/main both at bdbbb26; `git status --porcelain` empty; anchor read in full with its newest committed supersession header at 2026-07-06b (the TCOP read cluster). The anchor reading one commit behind the Stage-1 amendment commit was expected per the prior session's handoff, not a discrepancy: bdbbb26 was committed as a self-contained unit (amendment + review record + Stage-1 ops log) without an anchor edit, and the Stage-1 ops log operations_log/2026-07-07_preseed-evaluability-audit-stage1.md was the governing record for the arc's state.

One stale line noted during grounding, corrected this session: the anchor's "Who you are" section still carried the earlier-cycle layer identities (Layer 2 = ChatGPT, Layer 3 = Gemini as active implementer). The Cycle 3 architecture is Layer 2 = separate Claude instance (adversarial review), Layer 3 historical/as-needed. Corrected in this refresh.

## Arbitration record

Layer 1 presented the single live act (ratification arbitration on PRESEED_EVALUABILITY_AUDIT.md) with three options: (1) ratify as-is; (2) ratify and open Stage 2; (3) reject or amend (fresh L2 fidelity required on any change). Mike arbitrated **option 2**:

1. **RATIFIED:** PRESEED_EVALUABILITY_AUDIT.md v3 (sha256 d2f12fada35d726a5039696cb06caa4687e5b6506e26749318577c1d601c432a, 32057 bytes). Stage 1 of the protocol-amendment arc is fully closed - the complete adoption path (L1 draft -> L2 attack -> full-acceptance merge -> L2 fidelity clean -> Mike ratifies) is discharged.
2. **STAGE 2 OPENED:** the retrodictive calibration arc, with its own mini-contract, TCOP first, and both fences (hindsight contamination - pre-TCOP provenance only; temptation quarantine - calibration outputs inform the amendment's machinery only, never citable as substrate evidence) required in the mini-contract before anything runs.

**Governing precision, recorded at ratification:** ratification does NOT make the amendment govern prospective designs yet. Per the amendment's own adoption path, it governs its first prospective design only after surviving Stage-2 calibration against wave two's committed record and Mike's ratification of the fold. Status: **RATIFIED-PENDING-CALIBRATION.**

**Epistemic line, restated as binding on Stage 2:** the calibration is of the new machinery with wave two as ground truth - never a re-read of any probe. The TCOP under-determined result stands permanently; retroactively applied rules cannot issue findings; tcop_read_results.json is compared-against, never computed-from.

No forks arose this session; the arbitration was Mike's single call between predeclared options, not a manufactured consultation.

## Files placed this session

1. cycle3/RESUME_2026-05-30.md - anchor refresh (full-file overwrite): new supersession header (latest, 2026-07-08) recording the bdbbb26 Stage-1 commit, the ratification, the RATIFIED-PENDING-CALIBRATION status, and the Stage-2 open with its fences, sequencing, case set, and primary sources; 2026-07-06b header demoted to carried; "Who you are" layer identities corrected to the Cycle 3 architecture; "How Mike Works" updated with the hung-commit recovery procedure and the L2 verdict-language / state-re-grounding / empty-attachment rules from the Stage-1 arc; vocabulary section updated with the bounded-A outcome-language precision (saturated-relay / non-responsive bounded-channel, never "over-driven"); cold-start sequence updated (step 1 expectation, protocol-amendment and TCOP presence checks, Stage-2 branch at step 4). All other content carried verbatim.
2. operations_log/2026-07-08_stage1-ratification-stage2-open.md - this file.

SHA-256 digests published in-session before placement and verified at destination by size + digest per standing transit-fidelity discipline.

## State at session close

- Amendment: RATIFIED-PENDING-CALIBRATION.
- Stage 2: OPEN. First artifact is the Stage-2 mini-contract, to be drafted in a fresh session per the standing recommendation; sequencing: draft mini-contract -> L2 attack -> Mike arbitrates -> run calibration (Mike-executed) -> fold lessons into the amendment -> L2 fidelity on the fold -> Mike ratifies the fold.
- Carried unchanged: attenuation-allowance and matched-rho geometry design questions (Mike's, named-not-triggered; calibration may inform, never decide); 9-window earned-window rule unverified; CM-2 held; Rule E B/C held; L4 untouched; Comparator 0 unreclassified; Lambda=0.20 named-not-triggered; no density-stability claim.
- Manuscript: v1.5 Move B surgical fix remains pending, Phil-facing, separate track, Mike's call.

Drafting partner: Claude (Layer 1)
