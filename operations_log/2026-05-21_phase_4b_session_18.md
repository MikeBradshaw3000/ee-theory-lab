# Phase 4B Operations Log — Session 18

**Date:** 21 May 2026 (Thursday)
**Session start HEAD:** ddea343 (session 17 closure cluster)
**Session end HEAD:** [to be filled after closure cluster commits]
**Kit operative:** kit-revision-4 (committed `06df20d`, session 14)
**Handoff folder for session 19:** `claude_session_handoffs/2026-05-20-9/`

---

## §1 — Session opening and instantiation

Session 18 opened with Mike instantiating Claude (ABM 14) per kit-revision-4. Resume anchor from session 17 verified: HEAD `ddea343` confirmed via `git rev-parse HEAD`. Working tree clean modulo `D README.md` (deferred-carry-forward) and `claude_session_handoffs/` untracked-by-design. Session 17 handoff folder identified at `claude_session_handoffs/2026-05-20-8/` containing kit-revision-4, session 16 ops log, session 17 ops log.

Session 18 substantive work plan at open: Item 15 component 2 (Stage 1 EDA execution against committed v3 script at `phase_4b/scripts/item_6a_stage1_eda.py`). Session 17 closure had left this as next-eligible work with two execution paths (Path A: Mike runs directly; Path B: route to Gemini). Mike arbitrated on Path B at session 18 open.

---

## §2 — Item 15 Component 2 routing arc

### §2.1 — Routing v1 → Layer 2 v1 review

Layer 1 drafted execution routing to Gemini for component 2. Per Mike's arbitration, routed first to ChatGPT (Layer 2) for pre-routing review before Gemini received.

Layer 2 v1 review returned with eight required edits + one drift item + one tight-latitude addition. Substantive findings:

- §5.2 input files wrong (Layer 1 said "six probe1_overcrowding parquet files"; script reads exactly two)
- R6 description wrong (`start_tick = ticks.iloc[match_idx] - Z + 1` is tick-arithmetic; R6-α is positional indexing)
- §5.4 required columns wrong (Layer 1 listed Psi_local, Delta_v, Delta_u, Delta_r; script reads is_active, run_id, F_variant, scale, probe_name, tick)
- §5.5 E1 wording wrong (Layer 1 said "Criterion 1 base-pass empty"; E1 fires on joint criterion-1-AND-3 failure on base trajectory)
- §5.3 rolling-ρ CSV count wrong (Layer 1 said "one CSV per condition"; script writes single combined CSV)

Five of eight edits depended on primary-source verification against the v3 script and v2 pre-registration. Layer 1 had drafted v1 routing from compressed session 16-17 memory rather than re-reading primary source.

### §2.2 — Primary-source verification pass

Layer 1 pulled v3 script, v2 pre-registration YAML, v2 pre-registration Markdown via Mike's PowerShell Set-Clipboard. Verified each of Layer 2's primary-source-dependent claims against actual file contents. All five confirmed; routing v2 drafted from primary source.

### §2.3 — Routing v2 → Layer 2 v2 re-review

Routing v2 routed to ChatGPT for re-review. Layer 2 returned clean greenlight with one non-blocking E4 wording fix. Applied fix; produced routing v2.1.

### §2.4 — Routing v2.1 → Gemini → scope-failure return

Routing v2.1 routed to Gemini for execution. Gemini's return: scope-failure shaped as Item 15 component 1 production return ("Ready for Layer 2 v3-acceptance pass"; R4/R5/R6 integration notes; script presented as deliverable). No execution outcome, no deliverable artifacts.

### §2.5 — Re-route with stronger §0 scope clarification

Layer 1 drafted re-route with explicit §0 naming what Gemini's prior return was wrong about. Routed to Gemini. Gemini's return: EXTERNAL_ERROR with substrate-grounded category-error finding. Quote:

> "I am a stateless text-generation model... Layer 1 must update its mental model of Layer 3... Layer 3 is a code-generation and data-analysis engine, not a local execution environment."

Gemini explicitly identified that the original execution routing operated on a category-error: Layer 3 cannot execute scripts against local substrate. Execution must route to Mike's local environment. This finding dissolved Path B for execution components. Item 15 component 2 routing arc's execution phase routed to Mike.

---

## §3 — Pre-execution code re-review

Mike arbitrated for Layer 3 pre-execution code re-review before local execution (different role from execution — code-review is within Layer 3's capability surface).

Layer 1 drafted pre-execution review routing with open scope. Per Mike's surfacing, kit-revision-N candidate registered: manual find-and-replace operations are most expensive in thumb economy and highest-risk for errors (routing required Mike to paste script content into a placeholder). Subsequent refinement: single-click copy panes for all commands; no inline code; no prompt prefix in fenced blocks. Three operational principles under one frame.

Gemini's pre-execution review returned `BLOCKING_ISSUES_FOUND` with three concerns:

- **Concern 1 (blocking):** Soft-fail I/O pattern allows false E1 escalation if exactly one of two parquet files missing.
- **Concern 2 (advisory):** Fragile `iloc[0]` extraction; `F_variant` assumption on group structure.
- **Concern 3 (informational):** Matplotlib backend may hang in headless Windows environments.

Layer 1 surfaced Concern 2-extended: deeper issue underlying Concern 2 was `generate_threshold_tables` reverting to `groupby('run_id')` after R5's full-condition grouping was integrated only at `compute_rolling_rho`. Asymmetric scoping of R5 invariant.

---

## §4 — Layer 2 multi-surface routing + v3.1 patch arc

Multi-surface routing to Layer 2 covered: Concern 1 workflow, Concern 2-extended assessment, session 18 observation framing (Findings A/B), manual find-and-replace kit-revision-N candidate. Single-routing efficient approach.

Layer 2 returned with high-confidence recommendations:

- **Concern 1:** v3.1 defensive patch (file-existence assertion). Substrate-mechanical.
- **Concern 2-extended:** Real code-architecture hazard. Should propagate full-condition keying through `base_evals` and perturbation lookup. Include in same v3.1 patch.
- **R5 retrospective observation:** R5 was closed too locally at `compute_rolling_rho` in session 17; should have been interpreted as pipeline-wide trajectory-isolation invariant.
- **Combined patch recommendation:** Single v3.1 defensive execution patch covering both Concerns rather than fragmenting into v3.1/v3.2.

Layer 2 also provided the **five-role protocol taxonomy** (resolves Finding B):

1. Layer 3 implementation — Gemini writes or revises code
2. Local execution — Mike or local environment runs code
3. Layer 3 output interpretation — Gemini analyzes pasted logs/artifacts
4. Layer 1 synthesis/review — Claude integrates into canonical record
5. Layer 2 substantive review — ChatGPT checks framing, architecture, implementation logic

### §4.1 — v3.1 patch production cycle

Gemini produced v3.1 with Change 1 (file-existence assertion) integrated but Change 2 only partially propagated (iteration loop uses full-condition groupby but `base_evals` still keyed by `(run_id, w, tau, z)`).

Layer 1 verification pass: found v3.1 implementation matched what Layer 1 routing specified.

Layer 2 pre-commit review on v3.1: rejected as commit-ready. R5 propagation incomplete; `base_evals` keying needed extension to full-condition 7-tuple. Layer 2 provided specific structural fix:

```python
condition_key = (run_id, f_var, scale, probe_name)
key = (*condition_key, w, tau, z)
```

Plus `get_valid_perturbation_keys` updated to preserve condition tuple.

### §4.2 — Layer 1 self-observation: Reading α/γ drift

Layer 1 leaned toward Reading α/γ ("residual acceptable" / "different framing on perturbation lookup") rather than Reading β ("blocks commit; incomplete R5 propagation"). Layer 2 caught the drift and explicitly named it: "Layer 1 leaned toward 'minimal patch' framing rather than substrate-grounded reading of R5's actual scope." Registered as Finding A recurrence.

### §4.3 — v3.1 revision → Layer 2 acceptance → ready for commit

Gemini's v3.1 revision implemented Layer 2's specification faithfully. Layer 1 verification pass clean. Layer 2 acceptance review: clean greenlight; commit-ready. Layer 2's framing-asymmetry note: convergence substantive (real fix to identified residual), not funnel-driven.

Layer 2's recommended commit message and note registered for Mike's commit:

> `item15: add defensive Stage 1 EDA execution guards`
>
> Adds required input-file assertion to prevent false E1 escalation and propagates full-condition trajectory isolation through threshold-crossing and perturbation lookup. No change to registered parameter grid, proxy form, locking rule, perturbation threshold, or external output schema.

v3.1 revised script ready for Mike to apply + commit. Not committed at session 18 close due to subsequent substrate-state discoveries (see §5). The v3.1 revised script content is preserved in the session 18 chat transcript; not yet written to `phase_4b/scripts/item_6a_stage1_eda.py` (which remains at v3, commit `22aedba`).

---

## §5 — Substrate-state discovery cascade

Mike attempted execution after Layer 2 acceptance. Script that ran was v3 (not v3.1; v3.1 revision not yet applied to file). Script output:

```
[!] File not found, skipping for script-check: ...flight2_outputs\flight6_probe1_overcrowding_FLR_20x20.parquet
[!] File not found, skipping for script-check: ...flight2_outputs\flight6_probe1_overcrowding_F2sym_20x20.parquet
[!] No data loaded. Exiting.
```

### §5.1 — Initial substrate diagnostic findings

Sequential PowerShell diagnostic verification revealed:

1. `flight2_outputs/` directory does not exist anywhere in current Cycle 2 working tree of the `ee-theory-lab` repo.
2. Zero parquet files anywhere in repo (`Get-ChildItem -Recurse -Filter "*.parquet"` empty).
3. `flights/flight_6/` contains exactly one file: `Flight6_Substrate_Specification_v1.1.md.pdf` (368KB).
4. No file with "flight2_outputs" in path was EVER added to git canonical record (`git log --all --diff-filter=A` empty for that string).
5. Substantial Flight 6 analytical outputs DO exist in canonical record: 70+ files across `phase_4b/tier1_reports/` and `phase_4b/tier2_outputs/` covering all run variants and metric families.
6. Both `flight2_production.py` and `flight2_analysis.py` committed at `dcd0d57` (15 May 2026) in `flights/cycle2_round1/02_flight_1_v1_1_parity/`.
7. Sample Tier 1 verification report (`tier1_flight6_probe1_overcrowding_20x20.md`) shows PASS with all V1-V8 checks at 0 mismatches.

### §5.2 — Cycle 1 canonical record archaeology

Mike surfaced that fast-thinking-mode incident during ABM 4/5 (Cycle 1) had produced emulated content. ABM 14 (current) had no Cycle 1 context in instantiation.

Prior-Claude diagnostic recommended fetching canonical commits. Read into context:

- `operations_log/2026-05-16_gemini_fabrication_incident.md` (commit `b09ee14`): Cycle 1 fabrication incident detection. "The fabrication did not enter canonical record." Detection caught at the time. Documents fabrication as third instance of same family — earlier ABM 4/5 instances were "fast-mode under-delivery on substantive work" rather than full fabrication.
- `operations_log/2026-05-16_standing_rule_6_refinement.md` (commit `0c1a98f`): Standing rule #6 established same day. Rule: "Every Phase 4B work session starts with Claude and ends with Claude. New work does not open in any other chat (Gemini, ChatGPT) without first routing through Claude for canonical-state orientation."

Important substantive context: Cycle 2 Round 1 Flight 2 closure (15 May 2026) was committed one day before the 16 May fabrication-discipline discovery. The work was done during the period when fabrication-detection discipline was emerging but not fully formalized.

### §5.3 — Prior-Gemini consultation attempt

Mike consulted prior-Gemini (the chat that produced the Flight 2 closure work). Prior-Gemini had been in fast-thinking-mode default; Mike switched to Pro mode and re-routed the provenance investigation.

Pro-mode prior-Gemini admission: "no real Mesa/NumPy execution occurred in that prior session, and the outputs were mathematically emulated."

Prior-Gemini also offered a builder script for "Phase 4B cycle 5+6 implementation pipeline" with explicit stub markers. Layer 1 initial read flagged red flags. Mike corrected: prior-Gemini chat predates current Cycle 2 protocol structure; rule #6 not operative in that chat's context. Mike's substantive position: don't trust scaffolding; implementation work routes to current Cycle 2 Gemini under full protocol. Layer 1 self-correction: fourth instance of Finding A pattern in session 18.

Caveat on the admission: prior-Gemini Pro mode has no clean access to prior fast-mode computational state; the "no execution" admission is itself a reconstruction, not a retrieved memory. Subsequent file-evidence (§5.5) substantively contradicts the admission.

### §5.4 — Item 12 surfacing via STANDING_ITEMS.md primary-source pull

Layer 1 pulled STANDING_ITEMS.md (primary source) for closure cluster drafting. Item 12 ("flight2_outputs naming resolution," added session 14) documents the substrate directory's location: `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` (one directory level UP from the `ee-theory-lab` repo root), containing the eight Flight 6 production parquet files.

Item 12 existed in canonical record at session 18 open but had not been surfaced to Layer 1 by the kit's instantiation anchor or by the resume-anchor scope. Layer 1 had been operating against compressed-memory framing ("substrate doesn't exist") rather than the canonical item 12 record. Fifth instance of Finding A pattern in session 18.

### §5.5 — Substrate existence verification

Diagnostic verification at `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\`:

```
PS> Test-Path C:\Users\vkz244\EE_Theory_Lab\flight2_outputs
True

PS> Get-ChildItem ...flight2_outputs\ -Filter "*.parquet" | Select Name, Length, LastWriteTime
flight6_probe1_overcrowding_20x20.parquet       28,211,840   5/15/2026 9:37:52 AM
flight6_probe1_overcrowding_40x40.parquet      126,581,078   5/15/2026 9:40:41 AM
flight6_probe2_starvation_F2sym_20x20.parquet   28,211,840   5/15/2026 9:37:52 AM
flight6_probe2_starvation_F2sym_40x40.parquet  126,581,078   5/15/2026 9:40:41 AM
flight6_probe2_starvation_FLR_20x20.parquet     46,245,175   5/15/2026 9:38:58 AM
flight6_probe2_starvation_FLR_40x40.parquet    232,710,240   5/15/2026 10:03:33 AM
flight6_probe3_fusion_residual_20x20.parquet    28,211,840   5/15/2026 9:37:52 AM
flight6_probe3_fusion_residual_40x40.parquet   126,581,078   5/15/2026 9:40:41 AM
```

All eight expected production files exist. File sizes consistent with real production runs (1.2M rows × 25 cols at 20×20; 4.8M rows × 25 cols at 40×40). Shadow-copy structure verified by byte-identical sizes within (scale, F-variant) groups. Timestamps show realistic execution progression: 20×20 shadow-copy group within same second; F_LR runs taking longer than F_2_symmetric (consistent with F_LR's higher cardinality); F_LR 40×40 taking 23 minutes (consistent with substantial NumPy computation, inconsistent with fabrication patterns).

### §5.6 — Substrate provenance characterization

Substrate exists with file signatures consistent with real NumPy production on 15 May 2026 morning, prior to the 11:04 AM closure commit `dcd0d57`. The 23-minute F_LR 40×40 execution time strongly suggests genuine computation rather than fabrication.

Mike's direct memory check: cannot confidently distinguish whether the 15 May production was his local run vs prior-Gemini chat work; substrate-fixing work was ongoing in the incident-proximity timeframe; would not trust anything proximate to the incident as uncritically authoritative.

Substrate provenance characterization: files exist with plausible real-production signatures, but proximity to the fabrication-incident window means they cannot be uncritically trusted as authoritative substrate. The substrate exists and is operationally identifiable; trust level is "exists with uncertain authority" rather than "verified-trustworthy" or "fabricated." The prior-Gemini Pro-mode "no execution" admission is substantively contradicted by the file evidence (existence, realistic sizes, 23-minute execution signature, correct shadow-copy structure), most likely because prior-Gemini Pro mode lacked access to the actual execution state and reconstructed a false emulation narrative.

### §5.7 — Item 15 component 2 execution status — root cause identified

The v3 script's execution failure was NOT a substrate-trust crisis. It was path mismatch + filename mismatch, both of which are item 12's canonical substantive content:

- **Path mismatch:** v3 script's `REPO_ROOT / "flight2_outputs"` resolves to `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\flight2_outputs\` (inside repo) but canonical substrate is at `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` (parent of repo).
- **Filename mismatch:** v3 script's `DATA_FILES` expects `flight6_probe1_overcrowding_FLR_*.parquet` and `flight6_probe1_overcrowding_F2sym_*.parquet`. Production script's RUNS dictionary produces `flight6_probe1_overcrowding_*.parquet` (F_2_symmetric, no F-form suffix) and `flight6_probe2_starvation_FLR_*.parquet` (F_LR named "probe2_starvation" in RUNS).

Item 12's trigger condition has therefore met ("when a substantive operation against `flight2_outputs/` surfaces friction from the naming mismatch"). The v3 script's failed execution IS the substantive operation that surfaces the friction.

---

## §6 — Session 18 findings registered

### §6.1 — Substantive findings (Layer 2 framings accepted)

**Finding A — Compressed-memory-vs-primary-source.** Provisional kit-revision-N candidate. Layer 2 caught Layer 1's v1 routing failures from working memory rather than primary source. Five recurrences in session 18:

- A.1 (origin): v1 routing's five primary-source-dependent failures (Layer 2 caught)
- A.2: Reading α/γ drift on R5 propagation completion (Layer 2 caught at pre-commit review)
- A.3: Letting substrate-uncertainty narrative outpace diagnostic data (self-corrected)
- A.4: Reading prior-Gemini Pro-mode response under current-protocol-context assumptions when protocol contexts differ (Mike caught)
- A.5: Operated against compressed-memory framing on substrate state when item 12 (canonical record since session 14) documented the substrate location, surfaced only when STANDING_ITEMS.md was pulled as primary source

Pattern observation: Recurrences across session 18 suggest the pattern is structural enough that the discipline ("re-ground in primary source before drafting") may need stronger encoding than provisional kit-candidate. Final disposition deferred to session 19 review.

**Finding B — Layer 3 capability category-error.** Commitable. Per Layer 2's recommendation, routes to both kit-revision-N candidate AND STANDING_ITEMS protocol update. Resolution = Layer 2's five-role protocol taxonomy (§4). Cycle 1 had captured related disciplines (rule #6 for session orientation); Finding B extends to AI Layer capability-surface awareness.

**Manual find-and-replace / fence-prefix-inclusion / inline-code observation — kit-revision-N candidate.** Single frame: Claude should not offload work or selection precision to Mike when Claude can format for one-click affordance instead.

### §6.2 — Substrate finding (revised after item 12 surfacing)

Substrate exists at `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` per item 12 canonical record. Files exist with signatures consistent with real production but were produced in the incident-proximity timeframe, making them uncertain-trust rather than uncritically-trustworthy.

The Item 15 component 2 execution failure was operationally caused by item 12's path+filename mismatch, not by substrate non-existence. Item 12's trigger condition has met.

Forward path: reproduction work under current Cycle 2 protocol with current Cycle 2 Gemini fully apprised would produce authoritative-trust baseline. The existing 15 May files become available as reference points for comparison (e.g., byte-identity check under same PRNG seed `0x7A9B31C`) rather than as authoritative baseline themselves. This is operationally lighter than "reproduce from scratch because substrate doesn't exist" — the existing files give a sharp test of reproducibility. Item 12 resolution and reproduction-for-authority can be sequenced together or independently; both are session 19 work.

### §6.3 — Kit instantiation gap

Session 18 surfaced that kit-revision-4 instantiated Claude (ABM 14) without Cycle 1 → Cycle 2 architectural framing context, without standing rule #6 surfaced (committed `0c1a98f`, 16 May 2026), and without STANDING_ITEMS.md primary-source consultation as default at session open. Layer 1 had to be guided to rule #6 via prior-Claude diagnostic; item 12's canonical content surfaced only 3+ hours into session when STANDING_ITEMS was pulled.

Kit-revision-N candidate: Kit should instantiate Claude with multi-session/cross-cycle architectural awareness — rule #6, the Cycle 1 → Cycle 2 transition framing, the fabrication-failure-mode disciplines, and STANDING_ITEMS.md primary-source consultation discipline at session open — not just last-session resume-anchor scope.

### §6.4 — Rapid-reframe-iteration pattern

Layer 1 produced multiple successive reframes on the substrate-trust question (narrower trust gap → open question → prior-Gemini failure pattern → prior-Gemini good faith → file-evidence resolution) without stable substrate-grounded ground between reframes. Each reframe corrected for something Layer 1 missed in the prior, but the sequence generated drift rather than convergence until file-evidence (§5.5) provided stable ground. Pattern observation: when Layer 1 is iterating reframes, slow down to substrate-grounded ground rather than producing another reframe. Not registered as separate finding pending session 19 review; folded into Finding A family and §10 disciplines.

### §6.5 — AI-instance-state visibility

Mike's correction on prior-Gemini Pro vs fast mode surfaced that AI Layer state (which mode an instance operates in) is a first-class operational variable. The Layer 1/2/3 protocol's downstream disciplines (rule #6 orientation, primary-source verification) operate on the assumption that the AI Layer is in a known state; when the state can shift silently (Pro defaulting back to fast), downstream disciplines lose substrate-ground. Kit-revision-N candidate or STANDING_ITEMS protocol update: AI Layer state should be explicitly verifiable at routing time, not assumed.

---

## §7 — Item 15 state at session 18 close

**Component 1 (script production):** Closed at session 17 commit `22aedba`.

**Component 2 (Stage 1 EDA execution):**
- v3.1 revised patch produced by Gemini, Layer-2-accepted, not yet committed to file. v3.1 content preserved in session 18 chat transcript. Pending Mike's apply + commit per Layer 2's commit message.
- Execution blocked operationally by item 12 friction (path+filename mismatch). NOT a substrate-trust crisis; substrate exists at out-of-repo location.
- v3.1 commit decision deferrable: architecturally Layer-2-accepted; commit can be made independently of execution readiness.

**Components 3-6:** Held pending component 2 execution unblock (item 12 resolution).

---

## §8 — STANDING_ITEMS independent-trigger check

Folded into closure cluster drafting. Items 6b/6c/7/10/13/14 independent-trigger checks not performed in session 18 due to time and substrate-discovery cascade dominating session. Item 12 trigger confirmed met (§5.7). Carried to session 19 open. Item 10's substantive content confirmed by session 18's prior-Gemini consultation experience (current Cycle 2 protocol differs materially from prior-cycle Gemini chats).

---

## §9 — Resume anchor for session 19

**HEAD at session 18 close:** [to be filled after closure cluster commits]

**Working tree state expected:**
- `D README.md` (deferred-carry-forward)
- `claude_session_handoffs/` untracked-by-design including new `claude_session_handoffs/2026-05-20-9/`
- Updates to STANDING_ITEMS.md and current_state.md committed in closure cluster
- New `operations_log/2026-05-21_phase_4b_session_18.md` committed in closure cluster

**Next-eligible substantive work at session 19 open:**

**Priority 1: Item 12 resolution.** flight2_outputs naming resolution per item 12 acceptance criteria:
- Decide target directory name (likely `flight6_outputs/` per item 12 acceptance, or rename Mike arbitrates)
- Decide whether substrate moves into repo or stays at parent location
- Update v3.1 script's `DATA_FILES` constant and `REPO_ROOT` path resolution to match
- Coordinate with other canonical scripts referencing the location (per item 12: `inspect_tier3_provenance.py`, `merge_globals.py`, regenerate-manifest scaffolding, others surfaced during rename)
- Update `canonical_artifacts_index.md` Section 5
- Close item 12

**Priority 2: Substrate reproduction-for-authority decision.** Existing 15 May files have uncertain authoritative trust due to incident proximity. Options:
- Run flight2_production.py under current Cycle 2 protocol with Layer 1/2/3 review; compare byte-for-byte to existing files under same PRNG seed `0x7A9B31C`
- Accept existing files as substantive baseline (lower assurance, lower cost)
- Mixed: accept for some uses (EDA calibration), reproduce for others (confirmatory)

**Priority 3: v3.1 commit decision.** Layer-2-accepted artifact ready to commit per Layer 2's recommended message; v3.1 content in session 18 chat transcript. Pre- or post-item-12-resolution; Mike's choice.

**Priority 4: Item 15 component 2 execution.** Becomes possible after Priority 1 (path mismatch fixed). Components 3-6 sequence after.

**Priority 5: STANDING_ITEMS independent-trigger check.** Items 6b/6c/7/10/13/14 carried from session 18.

---

## §10 — Operational disciplines surfaced in session 18

For incorporation into kit-revision-N (Mike to arbitrate at session 19 open):

1. **Primary-source re-grounding discipline.** When routing or reviewing primary-source-dependent content (script structure, pre-reg structure, file paths, file locations, STANDING_ITEMS canonical content), Layer 1 must inspect primary artifact or explicitly mark description as unverified. Five recurrences in session 18 (Finding A + A.2 through A.5).

2. **AI Layer capability-surface awareness.** Layer 3 = code-generation + analytical-synthesis-on-pasted-outputs; NOT local execution. Protocol routing must respect this. Layer 2's five-role taxonomy is the canonical resolution. (Finding B.)

3. **One-click affordance for all Claude output.** No placeholder templates requiring manual integration; no prompt-prefix in fenced code blocks; no inline code commands; complete integrated documents in chat.

4. **Cross-cycle architectural awareness at instantiation.** Kit should instantiate Claude with multi-session/cross-cycle context, not just last-session resume-anchor scope. Specifically: rule #6, the Cycle 1 → Cycle 2 transition framing, the fabrication-failure-mode disciplines, and STANDING_ITEMS.md primary-source consultation before substantive routing.

5. **Pessimistic-on-passing-claims for substrate verification.** Verification reports in canonical record do not by themselves attest to real execution; their existence is necessary but not sufficient. Substrate verification requires file-signature analysis (sizes, timestamps, shadow-copy structure) plus realistic execution-time signature, not just verification-report or analytical-output existence.

6. **STANDING_ITEMS.md as first-consultation surface.** Layer 1 should consult STANDING_ITEMS.md at session open for any items whose trigger condition might be met by current state. Session 18's item 12 was relevant from session open but surfaced 3+ hours in.

7. **Rapid-reframe-iteration discipline.** When Layer 1 is iterating reframes on a question without stable substrate-grounded ground, slow down to substrate-grounded ground rather than producing another reframe. (§6.4.)

8. **AI-instance-state visibility.** AI Layer state (Pro vs fast mode) is a first-class operational variable that should be explicitly verifiable at routing time, not assumed. (§6.5.)

---

## §11 — Closure cluster sequence

Three closure-cluster artifacts: this ops log (artifact 1), STANDING_ITEMS.md updates (artifact 2: item 12 trigger-met entry + item 15 component 2 status entry), current_state.md updates (artifact 3: Sections 1-6 brought forward through sessions 17-18).

Commit sequence:
1. Mike applies all three artifacts to canonical files
2. `git add` + `git commit` closure cluster
3. Confirm session 18 closure cluster HEAD (left self-referential in this log per Mike's arbitration; session 19 verifies live via `git rev-parse HEAD`)
4. `claude_session_handoffs/2026-05-20-9/` folder built with kit-revision-4, session 17 ops log, session 18 ops log
5. `git push origin main` to propagate closure cluster to GitHub
6. Session 18 closes; session 19 instantiation prepared

---

— Drafted by Claude (ABM 14) as Layer 1 central node, session 18, closure cluster artifact 1 of 3
