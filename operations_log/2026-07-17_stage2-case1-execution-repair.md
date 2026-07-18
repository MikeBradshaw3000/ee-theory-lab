# Operations log - 2026-07-17 - Stage 2 Case 1 execution session: cold start, preflight halt, v4->v5 harness repair

**Session:** Stage 2 Case 1 (TCOP) execution session, first stage call.
**Layer 1:** Claude. **Execution channel and arbiter:** Mike.
**HEAD at cold start:** 0e32250 (confirmed from disk; origin current; tree clean).

## Cold start and grounding

Cold-start checks confirmed HEAD = origin/main = 0e32250, tree clean (first git command ran outside the repo directory - benign, re-run from repo root). Source ingestion ran on the commit-pinned clone channel: clone at 0e32250 in L1's container, permitted grounding files read (anchor with 2026-07-09 supersession header governing; STAGE2_MINI_CONTRACT.md + AMENDMENT_1; STAGE2_CASE1_IMPLEMENTATION_SPEC.md; STAGE2_CASE1_REVIEW_RECORD.md; the harness, digest-verified at e033471c...4b8 before reading), held-out files catalogued for avoidance and never opened, clone destroyed with confirmation. Canonical venv activated and verified.

## L1 error 1 (owned): if/else pipe-scope violation

L1's first drafted command of the session piped Set-Clipboard inside the else branch of an if/else - the exact documented pipe-scope bug the standing learnings prohibit. Consequence: the venv activation succeeded but wrote nothing to the clipboard, so Mike's paste returned the command itself twice before L1 recognized its own error. Corrected to the binding form ($msg assigned in branches, piped after the block); venv then confirmed. The rule was restated during grounding and violated in the first command - recorded plainly.

## Preflight call and HALT (loud, fail-closed - the fence working)

Mike called preflight (first-ever execution of the v4 harness). HALT at the first permitted-input existence check: FAIL CLOSED on a doubled path segment (cycle3/cycle3/data_out/c3_w2_null_extension_states_L0.4_k0_0000_s1024.npz). No manifest written; no computation; no held-out contact. Treated as a finding and routed to Mike per the fail-closed discipline; no patch-and-rerun.

## Diagnosis: wrong-values-under-right-names in the accepted v4

v4 line 38 computed REPO with dirname x3 from <repo>/cycle3/calibration/stage2/, landing at <repo>/cycle3; every derived path doubled the cycle3 segment. Survived four L2 review rounds because all rounds were code-reading, golden tests are path-free, and the file was never executed against the real tree. Side effect: spurious empty cycle3/cycle3/calibration/stage2 tree from the pre-check makedirs (inspected and removed at placement).

## L1 error 2 (owned): grounding read-through of the defect

L1 read the harness in full at grounding - including line 38 - verified its digest, and did not catch that three dirname calls from a four-deep location cannot reach the repo root. The defect was caught by Mike's execution, not by L1's read. Pessimistic-on-passing failed at the grounding read and is recorded as such.

## Fork to Mike; Option A arbitrated

Fork surfaced explicitly: (A) expedited L2 delta review of the one-line fix vs (B) fix-and-commit without L2. Mike arbitrated A.

## Delta build (v5) and L1 error 3 (owned, self-caught)

v5 built from the committed v4 (re-cloned at 0e32250, harness extracted alone, digest re-verified, clone destroyed). Two hunks, both disclosed: line 38 dirname x3 -> x4; docstring version line bumped for label honesty. L1's first docstring draft said "line 39" where the fix sits at line 38 - a wrong number inside the fix documenting a wrong-value defect; caught by L1 self-review before routing and corrected. Verification: single-occurrence replacement both hunks; diff exactly two hunks; AST clean; path arithmetic proven on a synthetic tree (v4 -> repo/cycle3, v5 -> repo). v5 sha256 3ef443ea4d301f604d0755c3a1e48cf233b475c449f26ed881bb2d27bef4946f, 54385 bytes.

## L2 delta review: ACCEPT

Self-contained routing packet (state re-grounding, halt evidence, diagnosis, two-hunk diff, digest gate, verification record incl. the line-39 self-catch disclosure, full v5 text) routed by Mike. L2 ACCEPTED: four-parent root calculation confirmed correct for the canonical location; uploaded source matched declared byte count and digest, parsed cleanly; no hidden dependency on the erroneous v4 root; existing fail-closed checks sufficient for the narrow repair; repository-root sentinel hardening named as a separate non-blocking consideration (not opened). Disposition: place and commit v5, restart from full preflight; execution remains gated on Mike's explicit stage calls.

## Placement and commit

Spurious cycle3/cycle3 tree inspected (empty) and removed. v5 placed by size-keyed Downloads selection, digest + size verified at destination (3ef443ea..., 54385 bytes). Committed with this ops log and the updated review record; explicit-path staging; git diff --cached verified pre-commit; push confirmed by the <old>..<new> main -> main line.

## Standing-state notes

- Anchor refresh deferred to session end by design (one header capturing the whole session rather than a mid-arc churn); until then the anchor's e033471c harness digest is superseded by the review record per the anchor's own committed-file-wins rule.
- TCOP result untouched and permanent (under-determined both co-equal axes; apparatus limits, not evidence; ordering hypothesis open). Held-out record never opened this session. No calibration output exists. Amendment remains RATIFIED-PENDING-CALIBRATION.
- Session L1 error ledger: three substantive items (pipe-scope violation; grounding read-through of the path defect; line-39 docstring error, self-caught) - all engaged above.

Drafting partner: Claude (Layer 1); execution and arbitration: Mike.
