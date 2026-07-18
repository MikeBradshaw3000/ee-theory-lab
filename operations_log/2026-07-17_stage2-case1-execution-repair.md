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

## Second preflight call and second HALT; v6 repair (same session)

Mike re-called preflight on the committed v5. HALT again, loud and fail-closed, at the permitted-input existence check - at the CORRECT path level this time (no doubled segment), confirming the v5 repair in execution. Diagnosis: line 45's null-extension NPZ filename template read k0_0000; the committed token is kp0_0000 ({kappa:+.4f} rule). Second wrong-values-under-right-names defect in the harness, same survival mechanism; the v4 build inferred the token instead of decoding it from the run script - the standing filename-token rule violated at build time, caught by the fence at first file contact.

Pessimistic-on-passing applied forward: before any fix, L1 audited EVERY path reference in the harness against tree 54dfb8c in one pass (blob-less clone; no held-out content extracted; clone destroyed). Result: all 8 permitted paths, all 4 deny paths, and 315 held-out prefix NPZs exist exactly as named; line 45 was the only defective reference - no serial-halt tail. v6 built from the committed v5 blob (digest-confirmed identical to transit), two disclosed hunks (line 45 token fix + docstring bump), template cross-checked against all five committed filenames, AST clean. v6 sha256 310d0dc525a179fffbce31827d4aff35abc3529e9bcbcebbbd6985c306826214, 54449 bytes. Mike confirmed the same expedited-delta path; L2 ACCEPTED (byte counts, digests, AST, exactly two hunks confirmed; permitted-read set and F3-analog gate now point at the committed null-extension family; no fence or scoring semantics changed). v6 placed by size-keyed digest-gated transit and committed with the updated review record and this amended ops log; restart from full preflight, Mike-gated.

## Third preflight call, third HALT; v7 repair (same session)

Third preflight call confirmed the v5 and v6 fixes in execution (existence loop + all permitted digest checks passed), then halted when the I/O self-audit ran for the first time and fired on its own docstring/comment/halt-message strings; its pandas substring check was also always-true against its own source. AST ground truth showed the harness's real I/O discipline clean - two raw calls, both guarded. L1's deep static audit also found the next halt in advance: the exec-safety _static_module_check misapplied at preflight to the never-executed c3_w2_tcop.py (digest-verified, AST-literal-only; its committed top level carries the run script's own pre-flight block). The audit then exhausted the statically-discoverable class: constant values cross-verified against tcop_read.py at digest (L1's tuple-extractor false alarms disclosed and corrected in-pass); computed constructions character-identical; offset bisection arithmetic replicated deterministically to <=5.6e-16; golden-fixture semantics confirmed. Container work was static/AST/arithmetic only - no simulation, no calibration RNG, no canonical seeds, no NPZ access, no calibration artifact; execution remains Mike's alone.

v7 delta: self_audit_io rewritten AST-based (self-tested: passes on v7, fires on four injected violations with line/function attribution; pandas as import check); the misapplied gate call removed with in-place rationale (gate unchanged on tcop_read.py); docstring bumped. v7 sha256 654aa1f35b63e83f32e74505b0b2c8be1d84850719f7603e5ff79a87433278d0, 55403 bytes. L2 ACCEPTED (three hunks confirmed; audit-correctness and fence-scope confirmed; no remaining blocker). Placed by size-keyed digest-gated transit and committed with the updated review record and this amended ops log. Named fold item (not opened, Mike's): whether execution-ready verdicts should require a Mike-executed smoke stage - three first-execution defects, one shared cause: no round ever ran the file. Restart from full preflight, Mike-gated; the F3-analog gate is the remaining first-execution step, whose first execution is the test by design.

## Fourth preflight call, fourth HALT; v8 repair (session continues past midnight, 2026-07-18)

Fourth call reached deepest yet - digest loop, AST self-audit, frozen-source verification, kappa extraction, offset reproduction all passed live on Mike's machine - then halted at the golden precision fixture: precision_gate leaked np.bool_ on its False branch (numpy scalars from wilson's arithmetic; `and` returns the first falsy operand unwrapped). Real defect beyond the fixture: np.bool_ is not JSON-serializable and feeds geometry/forecast summary writes. L1 owned that its prior math-module replica verified the value and was blind to the type. Gap closed by method upgrade: the entire preflight body executed as a container replica against v8 under canonical numpy 2.4.4 (committed blobs in a synthetic tree; zero-byte NPZ placeholders never read; F3-analog gate excluded by design; no calibration artifact; tree destroyed). All components PASS including the full 28-fixture golden suite, executed. v8 = bool() wrap in precision_gate + docstring bump; sha256 41413911916297e77bf8ec85f33b6415a5fbf2526d97367265610328f51b5817, 55717 bytes. L2 ACCEPTED (real defect, value unchanged, replica method adequate). Placed by size-keyed digest-gated transit and committed with the updated review record and this amended ops log. Also this arc: a truncated-paste continuation hang (Ctrl+C, commands split shorter thereafter), a fresh console losing repo cwd and venv (both re-established), and two stray files ('0', '=' - captured console debris from the mangled paste) inspected via [System.IO.File]::ReadAllText with -LiteralPath semantics and removed. After v8 every preflight component except the F3-analog gate has executed successfully somewhere; the gate is the sole remaining first-execution step, by design. Restart from complete preflight, Mike-gated.

## Fifth preflight call, fifth HALT - the F3-analog gate, working as designed; v9 repair (2026-07-18)

Fifth call passed every pre-gate component live on Mike's machine (digest loop, AST self-audit, verify_frozen, kappa, offsets, full 28-fixture golden suite - first live pass), then the F3-analog gate ran its first genuine simulation and halted: F3-ANALOG FAIL seed 42 - Engine A not bit-exact against the committed null-extension record. The substantive halt of the night, and the gate producing exactly the fidelity finding it exists for. Diagnosis: INIT_ACTIVE = round(0.40*N_CELLS) conflated initial density with the Lambda=0.40 anchor; committed convention is TARGET_RHO_INIT=0.10 in both committed run scripts. states[0] is stored before the first update, so the wrong initial density broke bit-exactness at tick 0. All other Engine-A discipline verified faithful. Fifth wrong-values-under-right-names defect.

Decisive verification (canonical numpy 2.4.4): committed seed-42 tick-0 active count = 250 (from data); INIT=250 replica bit-exact across 400 ticks at all five seeds; complete preflight replica on v9 with the F3 gate included against the real committed NPZs - every component PASS end-to-end. Provenance: diagnosis read committed-but-not-permitted c3_w2_null_extension.py for L1 analysis only (harness input partition unchanged; not consumed by the harness); canonical seeds used only to reproduce permitted null-extension data via the gate's own comparison; no held-out file touched. v9 = INIT_ACTIVE -> round(0.10*N_CELLS) + docstring; sha256 214fb99389c04be1d5526ad32782c7b03d94a3780e048d6ed00dfb1d2dad6b00, 55963 bytes. L2 ACCEPTED (independently confirmed the tick-0 store-before-update mechanism; fix correct at both simulator sites; diagnosis-only script consult does not alter partition or evidence). Placed by size-keyed digest-gated transit, committed with the updated review record and this amended ops log.

## Session close-out state (2026-07-18)

Five preflight halts, five L2-accepted single-focus repairs, five clean commits: 0e32250 (inherited) -> 54dfb8c (v5, REPO path depth) -> 3a225ad (v6, null-ext filename token) -> c869d97 (v7, AST self-audit + exec-gate scope) -> f680a7e (v8, precision_gate bool wrap) -> [v9 commit, INIT_ACTIVE density, hash recorded at commit]. All five defects were the wrong-values-under-right-names class in the L2-accepted v4, each surfaced only by execution because no build-review round ever ran the file - the named fold item (Mike's call): whether execution-ready verdicts should require a Mike-executed smoke stage. The complete preflight is now verified end-to-end in a canonical-numpy replica including the F3-analog gate at all five seeds; the first genuine CALIBRATION simulation is the geometry stage, on Mike's explicit call. TCOP result untouched and permanent; held-out record never opened; no calibration artifact produced; amendment remains RATIFIED-PENDING-CALIBRATION. Anchor refresh (deferred through the repair arc by design) is the one remaining housekeeping item before geometry, on Mike's call. L1 error ledger for the session: the pipe-scope violation (twice-formed early), the grounding read-through of the v5 path defect, the line-39 docstring slip (self-caught), and the math-module replica that was blind to the np.bool_ type (method upgraded to canonical-numpy replica thereafter) - all owned in place.

Drafting partner: Claude (Layer 1); execution and arbitration: Mike.
