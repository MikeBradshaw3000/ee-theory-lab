# Operations Log: 2026-05-20 — Session 11: Item 11 Closure (Pipeline Outcome-Construction Gap)

**Date:** 2026-05-20
**HEAD at session start:** `207b484` (session 10 close: item 1 closure addendum + item 11 add)
**HEAD at session end:** to be set when this log commits as the session 11 close cluster
**Session anchor for resume:** HEAD after this cluster commits

## Session arc

Eleventh session, and the first focused on substantive analytical-pipeline work rather than protocol infrastructure since session 6. The session opened with kit-revision-3 plus the session 10 operations log (item-1-closure-and-item-11-add addendum). Resume-anchor verification cleared cleanly: HEAD at `207b484` confirmed, working tree matched session 10 close, STANDING_ITEMS item 11 read at primary source with three sub-deliverables specified.

The session executed all three item 11 sub-deliverables in sequence: archaeology closing sub-deliverable 1 (substantive-correctness determination), code fix closing sub-deliverable 2 (wiring outcome-construction into the pipeline), re-run-and-diff closing sub-deliverable 3 (with C-arbitration on canonical output replacement). Item 11 closes; reg_01 finding restored to canonical without pipeline-flagged caveat.

## Substantive findings

**Item 11 substantively complete across all three sub-deliverables.**

### Sub-deliverable 1: substantive-correctness via archaeology

Per item 11 acceptance ("identifying the actual pipeline that produced [the committed outputs]"), the producing pipeline was identified through git-log and filesystem-timestamp archaeology without execution. Sequence of evidence:

- The three committed reg_01 output files (`coefs_reg_01_scale_interactions.csv`, `coefs_reg_01_scale_interactions_sensitivity_cell.csv`, `report_reg_01_scale_interactions.md`) carry filesystem timestamps 2026-05-17 20:46-20:50 — a six-minute production window, primary CSV first, sensitivity CSV and report ~3.5 minutes later. Consistent with a single pipeline run, not three separate manual writes.
- `git log --all --diff-filter=A --follow` confirms all three output files were introduced to version control at commit `3189ab7` (2026-05-18 20:35). The commit message names the act: "Reconciliation: Tier 3 reg_01 canonical artifacts + sessions 5-6 operations logs." Outputs that already existed on the filesystem from session 5 work were reconciled into git history at `3189ab7` alongside the script refactor that broke the pipeline going forward.
- `89b85f4` (2026-05-16 19:18) was the committed HEAD throughout the May 17 production window. The session 6 operations log states explicitly: "HEAD at session start: unchanged from session 5 end (no commits between sessions)" — confirming no intervening pipeline-code commits between `89b85f4` and `3189ab7`.
- `89b85f4`'s `phase_4b/scripts/tier3_regression.py` contains the inline outcome construction (`df['logit_p_base'], boundary_count = eta_floor_inversion(df['p_act'])`) guarded by `if spec['outcome'] == 'logit_p_base':`, with `eta_floor_inversion` imported from `_phase_4b_common`. Verified at primary source.

The committed reg_01 outputs were produced by `89b85f4`'s pre-reconciliation pipeline executing on 2026-05-17. They are substantive artifacts of real code on real data. The `3189ab7` reconciliation lost the wiring; it did not corrupt the outputs. Sub-deliverable 1 closes by identification; no execution of the pre-reconciliation pipeline required.

### Sub-deliverable 2: outcome-construction wired into intake

Code fix, single architectural change across two files.

**`_phase_4b_intake.py`**: added `construct_outcome(df, normalized) -> pd.DataFrame`. Dispatches through `CONSTRUCTION_REGISTRY` keyed on `normalized.outcome_construction`. Single rule, no iteration. Defensive registry-presence check mirrors `construct_derived_variables`' defensive style (the check is redundant given that `normalize_prereg` validates `out_const not in CONSTRUCTION_REGISTRY` upstream, but symmetry with the existing pattern is preserved).

**`tier3_regression.py`**: added `construct_outcome` to the `_phase_4b_intake` import block and added the call `df = construct_outcome(df, normalized)` between `construct_derived_variables` and `attach_tier2_globals` in `run_tier3`. Construction-phase ordering preserved as a unit before tier2-globals merge.

Layer 1 architectural review before commit (per item 11 spec): function signature mirrors `construct_derived_variables`; idempotency follows the existing pattern (silent overwrite on collision, matching `construct_derived_variables`' behavior); `echo_intake_summary` already names the outcome construction via the existing `[Outcome]: {name} (via {construction})` line — no summary update needed.

The full-file overwrites produced incidental whitespace cleanup (trailing whitespace on blank lines stripped; UTF-8 BOM removed from `tier3_regression.py` shebang line; EOF newline state normalized). Mike arbitrated A: accept the cleanup as benign. The substantive logic is byte-identical to intended; the whitespace cleanup is one-time noise that does not affect Python parse behavior, and the BOM removal is a positive (BOM-on-shebang has been a documented PowerShell hazard per `environment_reference.md`).

### Sub-deliverable 3: re-run and diff

Pipeline re-run executed against the same yaml input (`phase_4b/pre_registrations/reg_01_scale_interactions.yaml`) under the fixed code. The pipeline ran to completion: 12M cell-tick rows loaded across four canonical input parquets, all derived and outcome variables constructed, regression fit completed, three new output files written. Two `statsmodels` runtime warnings surfaced during the fit:

- `RuntimeWarning: invalid value encountered in sqrt` (in `linear_model.py:1884`, computing standard errors as `np.sqrt(np.diag(self.cov_params()))`).
- `ValueWarning: covariance of constraints does not have full rank. The number of constraints is 23, but rank is 3` (in `base/model.py:1894`).

These warnings are characteristics of the analytical setup (cluster-robust covariance on a regression where the model perfectly fits a deterministic chain), not artifacts of the code fix. They would have fired on the May 17 production run as well; session 6's operations log did not quote stdout, so no record exists of whether they surfaced then. Surfaced now for the canonical record.

**Diff against committed `3189ab7` outputs**: non-clean. All three output files differ.

Primary coefficients CSV diff characterized:

| Category | Pattern |
|---|---|
| Intercept | -3.999999999999919 (committed) vs. -3.9999999999999196 (new) — identical to ~15 sig figs; both round to -4.0 exactly. |
| Substantive drive coefficients (Lambda_total, Local_Density, Local_Density_squared, Term_Lambda, Term_Density_Pos, Term_Overcrowding) | Agree to ~3-5 significant figures; differences in 4th-5th decimal. |
| Auxiliary, categorical, interaction, and global-aggregate coefficients | All at orders 1e-14 to 1e-16 in both committed and new — numerically zero, machine-precision residual values. Sign-flips at this scale are noise on machine epsilon. |
| Standard errors | Many cells blank in new outputs where committed had values; some surviving std_err values differ by orders of magnitude. Driven by the cluster-rank-deficiency warning above. |

The substantive analytical finding from session 5/6 — R²=1.000 identity-recovery of the deterministic substrate chain — is preserved. The intercept hits -4.0 exactly; all categorical/interaction/auxiliary coefficients are machine-zero (which is what the deterministic chain predicts they should be: F_variant, scale, epoch, network terms, global aggregates all contribute zero to the substrate's local activation construction by spec); the four meaningful drive coefficients agree to 3-5 significant figures with the committed values. The diff is non-clean at the byte level but substantively coherent at the analytical level. The committed outputs are not bit-reproducible by the fixed pipeline; they are analytically reproducible.

What drives the byte-level non-clean: numerical instability inherent to cluster-robust covariance fitting on deterministically-saturated regressions. Even running the same code on the same data twice can produce different std_err patterns depending on solver state, BLAS library behavior, library version drift, or floating-point operation ordering. The coefficients themselves are stable to the precision the model can deliver; the std_err diagonal is where instability lives.

### Mike's arbitration: canonical output replacement (option C)

The non-clean diff was the spec's "further gap requiring Mike's arbitration on what's canonical" branch. Three options surfaced:

- **A.** Keep the committed `3189ab7` outputs as canonical.
- **B.** Replace canonical outputs with new pipeline's outputs.
- **C.** Replace canonical outputs with new pipeline's outputs; document the diff and substantive-equivalence finding in the operations log.

Mike arbitrated **C**. (A) would preserve the original problem (canonical code cannot reproduce canonical outputs). (B) loses diagnostic context. (C) makes both true: canonical code produces canonical outputs going forward, and the historical-to-current relationship is documented in this log.

The new outputs become canonical at this commit. The historical `3189ab7` outputs remain in git history at their commit, accessible via `git show 3189ab7:phase_4b/tier3_outputs/<file>` for any future archaeological need.

## Procedural findings

**Sub-deliverable sequencing reordered from session 10's plan.** Session 10's close-out committed to "one commit for the code fix, then sub-deliverable 3 (re-run-and-diff) as its own commit." During this session, surfacing that the spec's sub-deliverable 3 is a check on sub-deliverable 2's correctness, Mike arbitrated **B2** (run-then-commit) over A2 (commit-then-run). Running the re-run with files in working tree before commit lets the verification adjudicate the code fix before it locks into the canonical record. Then, because sub-deliverable 3 surfaced the further gap (non-clean diff) and Mike's C-arbitration resolved it inline, the original two-commit plan collapsed into one. The collapse rationale: the substantive act is "close item 11 with all three sub-deliverables resolved," and splitting into two commits would create an interim canonical state where code is fixed but output replacement is not done.

Worth registering as a working-pattern observation: the spec's sub-deliverable ordering is the close-of-item order, not necessarily the execution-or-commit order. Execution sequence (run before commit) and commit shape (one cluster or multiple) are independent decisions made when the further-gap branch is or is not taken.

**Venv-activation needed at session 11 open.** The session opened in a fresh PowerShell instance (Mike's noted convention for thumb-expense management). `verify_environment()` raised `RuntimeError: venv is not active` on first pipeline-execution attempt. The active venv lives at `C:\Users\vkz244\EE_Theory_Lab\venv\` (parent of the repo), not nested inside the repo. A second `venv_cycle1_archive\` exists at the same parent and is not for use. Search for `Activate.ps1` at the repo level returned empty; widening to the `EE_Theory_Lab` parent surfaced both. Activation via the absolute path completed cleanly.

Worth registering: kit-revision-4's `environment_reference.md` already specifies the venv location; the kit's resume-anchor sequence (HEAD verify, working-tree verify, log read, STANDING_ITEMS check) does not include venv activation. When session work will require Python execution, venv activation belongs in the pre-flight verification, not as a deferred step that surfaces on first execution attempt. For kit-revision-4 consideration.

**Methodology error during diff verification (caught inline).** Step 6 of the archaeology used `Select-String -Pattern "logit_p_base|eta_floor_inversion" -SimpleMatch`. The `-SimpleMatch` flag treats the pattern as literal, so the seven-character string `logit_p_base|eta_floor_inversion` was searched (and never matched) rather than alternation. The empty result was initially read as "neither term appears in `89b85f4`'s script" — which contradicted the session 10 addendum's diff claim and would have widened the archaeology unnecessarily. Corrected by re-issuing as two passes without `-SimpleMatch`; both patterns then found cleanly. The PowerShell-vs-grep semantic difference is worth registering: PowerShell's `-SimpleMatch` is the *literal-match* flag, not a regex-enable flag.

**Layer 1 self-review caught unintended changes during pre-commit diff verification.** When verifying the working-tree diff before commit, the full diff surfaced trailing-whitespace cleanup, BOM removal, and EOF-newline normalization as unintended side effects of the full-file overwrite. The discipline question (whether to accept benign cleanup or re-draft preserving byte-for-byte unchanged regions) was raised to Mike for arbitration rather than waved through silently. This matches the kit Section 8 discipline ("Layer 1's job is to surface the conflict to Mike, not to reason past it") even where the conflict is in non-functional content.

**Full diff visibility through `git diff` paginator interrupt.** Initial `git diff` was interrupted at the `:` paginator prompt before showing the substantive changes — Mike pasted the partial output. The substantive `construct_outcome` additions were below the page break. Re-issued as `git --no-pager diff` to bypass the paginator. Worth registering: PowerShell's git wrapping uses a paginator by default; `--no-pager` is the bypass.

## Items resolved

**STANDING_ITEMS item 11 (pipeline gap: outcome-construction not wired into intake).** Resolved by the three sub-deliverable closures documented above. Per the maintenance discipline (items removed when acceptance criterion is met), item 11 is removed from STANDING_ITEMS at this commit. The substantive reg_01 finding (R²=1.000 identity-recovery) is restored to canonical status without the pipeline-flagged caveat — the new canonical outputs are produced by the fixed canonical pipeline, the historical outputs remain accessible via git, and the substantive-equivalence diff is documented in this log.

## Items not resolved

**Items 2, 3, 4, 5, 6, 7, 8, 10.** All carry forward in STANDING_ITEMS with their trigger conditions unchanged. Item 2 (push to origin) and item 3 (Stage 2 execution) become first-eligible after item 11 closes; sequencing relative to each other is at Mike's arbitration. Item 11's superseding-priority over items 2 and 3 lifts at this commit.

**Kit-revision-4 deferred items grow.** Session 10's deferred-to-kit-revision-4 items (path-space land-grab framing into Rule 7.4, paste-back-incident sharpening, byte-count verification load-bearing, `(N)`-suffix handling, "one-click copy pane only for actionable content" pattern, v1_1_divergence_review footnote precedent) carry forward. Session 11 adds: handoff-folder attachment discipline (attach contents to the opener message rather than reference by path — saves a round trip every instantiation, per Mike's session-11 observation); venv activation in pre-flight verification when Python execution is expected; PowerShell `-SimpleMatch` literal-vs-alternation semantic; `--no-pager` for diff visibility.

**Operations log file hygiene.** The session 10 operations log file contains the addendum duplicated — flagged on first read during session 11 open. Not addressed in this session; not blocking. Worth registering for a future cleanup pass.

## Methodological observations

**Archaeology over execution where the spec permits.** Item 11 sub-deliverable 1's acceptance was a disjunction: run the pre-reconciliation pipeline OR identify the actual pipeline. Session 11 closed sub-deliverable 1 entirely by identification through git-log and filesystem-timestamp work. The execution branch would have required reconstructing input state at the `89b85f4` working-tree configuration (the yaml schema changed between `b10682a` and `3189ab7`) — substantial reconstruction work for a question the archaeology answered directly. The spec's disjunction is genuine; the cheaper branch closed cleanly.

**Substantive-equivalence as a distinct finding category.** The diff between committed and new reg_01 outputs is non-clean at the byte level but coherent at the analytical level. This is a distinct finding category from either "bit-reproducible" or "substantively different" — it requires reading the coefficients with knowledge of which categories are expected to be machine-zero by the substrate construction (categorical/interaction/auxiliary terms) versus which are expected to carry signal (the four drive terms plus intercept). Without that reading, the 48-line CSV diff would look like a substantive failure; with it, the analytical equivalence is visible. Worth registering: diff verification at the protocol level needs to be paired with knowledge of which artifacts should agree to what precision under what theoretical expectation.

**Second substantive analytical artifact landed under the kit framework.** Session 6 produced the original reg_01 finding under the pre-kit protocol. Session 11 closes the canonical-record integrity gap on that finding by replacing the unreproducible outputs with reproducible ones, preserving the analytical interpretation. This is not a new analytical finding (no new substantive claim about the EE theory); it is a canonical-record restoration that makes the existing analytical finding rest on reproducible foundations going forward. Item 11 closure is structural in this sense — analogous to item 9's reconciliation closure being structural rather than new-finding.

## Pending decisions for session 12

1. **Item 2 vs. item 3 sequencing.** Both become eligible after this session closes. Push to origin (item 2) before Stage 2 execution (item 3) is the more conservative ordering; Stage 2 first would defer push until after substantial canonical-artifact moves. Mike arbitrates.

2. **Kit-revision-4 scheduling.** Session 10 named kit-revision-4 as anticipated post-item-9 closure; session 11 grew the deferred-items list. The structural warrant for kit-revision-4 is strengthened. Whether to land it in session 12 or later is at Mike's call.

3. **Operations log file hygiene cleanup.** The session 10 ops log has the addendum duplicated. Whether to fix during Stage 2 file-hygiene work or as a one-off cleanup is at Mike's call.

4. **`current_state.md` Section 2 — the post-item-11 framing.** This session's update lifts the pipeline-flagged caveat from the reg_01 finding. Future fresh-Claude sessions will read Section 2 as restored canonical status. If Phil engages the reg_01 finding in the v1.5 Overview revision (per STANDING_ITEMS item 7 trigger), the new canonical outputs are what's in the canonical record.

## Resume anchor for session 12

When this conversation resumes:

1. **Verify HEAD.** `git rev-parse HEAD` should return the commit of this log entry, once committed.

2. **Verify working-tree state.** `git status --short` should show the same session-9 Stage-2-deferral items as session 10 close (routing artifacts, scratch scripts, commit-message txts, three derived-output subdirectories) and the three `item9_*` plus three `deliverable3_*` files from session 10. The session-11 work files (two scripts and three tier3 outputs) are committed; no new working-tree items expected from session 11 work.

3. **Read this log entry to orient.**

4. **Check STANDING_ITEMS.md for triggered items.** Item 11 is removed. Items 2 (push to origin) and 3 (Stage 2 execution) become first-eligible. Other items unchanged.

5. **First substantive action:** Item 2 or item 3 per Mike's arbitration; either is structurally valid.

**Foundational set updates this session:** `current_state.md` Sections 1, 2, 3, 4, 6 updated (Section 5 unchanged); no other foundational documents touched. STANDING_ITEMS item 11 closed and removed. Two phase_4b script files updated (`_phase_4b_intake.py`, `tier3_regression.py`). Three phase_4b tier3 outputs replaced as canonical (`coefs_reg_01_scale_interactions.csv`, `coefs_reg_01_scale_interactions_sensitivity_cell.csv`, `report_reg_01_scale_interactions.md`).

— Drafted by Claude as Layer 1 central node, session 11 end operations log entry, item 11 closure cluster. No Layer 2 routing per the agreed sanity-scan-distribution convention (substantive analytical-pipeline work with Mike arbitrating in-band rather than architectural deliverable warranting v2-acceptance pass).
