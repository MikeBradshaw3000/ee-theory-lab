# Phase 4B Operations Log — Session 20

**Date:** 22 May 2026
**Session start HEAD:** [session-19 close-out cluster; verify live — session 19 left its closing HEAD self-referential]
**Session end HEAD:** [to be filled live after the close-out cluster commits; session 21 verifies via `git rev-parse HEAD`]
**Kit operative at session open:** kit-revision-5 (committed `1cac510`, session 19). Superseded by kit-revision-5.1 this session.
**Layer 1 note:** the session's late stretch ran under a reduced-capability Layer 1 model; Mike restored the full Layer 1 model for the close-out. The handoff is recorded in §3 because the re-grounding it prompted is what caught the footer-corruption near-miss.
**Handoff folder for session 21:** built at close — see §8.

---

## §1 — Session opening and instantiation

Session 20 opened with Claude (Layer 1) instantiating from kit-revision-5 against the session 18 and 19 ops logs, per the standard resume anchor. HEAD verification and `git status --short` route to Mike (Layer 1 operates in the chat-interface environment, no live repo); surfaced as the first PowerShell steps rather than fabricated. STANDING_ITEMS consulted as first-consultation surface per the session-18 discipline: item 12 the only trigger-MET item; the two carried-forward session-open tasks (kit-revision-5 Layer 2 pass; STANDING_ITEMS independent-trigger check) surfaced for Mike to sequence.

Mike's stated session goal: get to project work — use Layer 3 for the item-15 EDA execution. The session instead resolved into protocol/verification work that surfaced a canonical-record integrity finding (§5). That outcome is the protocol working as designed, not a derailment: the verification chain that found the problem is the reason the problem was found before it contaminated downstream analysis.

---

## §2 — kit-revision-5.1: the owed Layer 2 protocol-infrastructure acceptance pass

The first carried-forward task. kit-revision-5 was committed session 19 on the pragmatic path (Layer 1 self-review + Mike's in-band arbitration), with the Layer 2 acceptance pass explicitly owed to session 20. This session ran it.

**Grounding before routing.** Per Rule 7.4 / Finding A, Layer 1 re-pulled the full foundational set as primary source before drafting the routing — `protocol_primer.md`, `standing_rules.md`, `vocabulary_quarantine.md`, `canonical_artifacts_index.md` — verifying the kit's load-bearing session-19 claims against canonical text. The "field" workstream-split (kit Section 4) verified clean against `vocabulary_quarantine.md` Section 1 + Section 5; the sessions-11-13 backlog render/defer split (kit Section 3) verified clean against `canonical_artifacts_index.md` Section 11; the standing-rules Section 5 summary verified faithful.

**Routing to Layer 2 (existing in-context instance, per Mike's arbitration).** Item 10's ChatGPT half did not fire (no fresh ChatGPT instance opened; the routing went to an instance already carrying current-protocol context). The routing opened with a §0 instance-state-confirmation gate per the AI-instance-state-visibility discipline; Layer 2 confirmed current Cycle 2 context before reviewing.

**Layer 2 return: accept with two required edits.** Both in compressed short-summary sections where wording carries disproportionate cold-start load. (1) Section 2's one-line Gemini role ("Implementation and execution. ABM substrate work") reintroduced the execution category error the next paragraph corrects; revised to name implementation/support/synthesis with "Local execution is Mike's channel." (2) Section 5's "rule 4 ... is the same fact as the Layer 3 capability boundary" overclaimed an identity; softened to "closely related but broader" (original rule 4 is the protocol-wide asymmetric-execution-channel discipline; the Layer 3 boundary is its specific application to Gemini). Layer 2's Rule 6 self-read: genuine convergence on the rest, divergence preserved exactly on these two synthesis-compression points — not the framing-asymmetry artifact.

**kit-revision-5.1 produced, delivered, and landed** (`claude_instantiation_kit_v5_1.md`, new file at workspace root per the kit-revision discipline; kit-revision-5 preserved in git history). Both edits applied; a 5.1 revision note and updated footer document the acceptance-pass closure. **The pragmatic-path debt from session 19 is closed: the kit now carries full Layer 2 review lineage.** The file is on disk and verified byte-identical to source by content-and-hash check (40,797 bytes; SHA-256 `c73f65b9277597cc8ec96585025008f7a2b9b0530587d1a92ad28a65d2a58af1`; 8 section headers; 2 revision notes; correct final line; no BOM) — see §3 (Finding D) on why line-count alone was an unreliable check and how the verification was re-grounded.

---

## §3 — Footer cleanups (Findings A/C): identified, attempted, corruption caught, deferred — plus delivery-method Finding D

Three findings surfaced during the §2 grounding pass; Mike arbitrated to bundle them into the work this session rather than spin a separate tracked item. The cleanup *attempt* then surfaced a fourth finding and a corruption near-miss that the commit-hold caught before it reached the canonical record.

**Finding A — stale "pending Layer 2" footers (identified).** `protocol_primer.md` and `standing_rules.md` carried pre-commit drafting footers; `canonical_artifacts_index.md` Section 9 records both as committed (`79db966`), and `vocabulary_quarantine.md` had already cleaned its equivalent footer in the session-19 close-out. Both footers were *targeted for* cleanup this session.

**Finding C — primer's possibly-never-closed acceptance pass (identified).** The primer footer claimed "Pending Layer 2 acceptance of v2 before commit." Layer 2 confirmed it has **no record** of having run that session-9 primer v2-acceptance pass. So the primer was effectively committed under the same pragmatic-path shape the kit later used. Per Mike's option-1 arbitration, the intended cleanup was an **honest annotation** recording the primer as committed under pragmatic/in-band arbitration, ratified by practice across sessions 9-20, with a retrospective Layer 2 acceptance pass available at Mike's election.

**Finding B** was folded into the kit-revision-5.1 edit (the rule-4/Layer-3-boundary softening, §2 above) — internal to the kit, so it belonged in the kit pass.

**The corruption episode (the honest record).** The footer edits were performed on both files. The footer *text* landed correctly (it is pure ASCII and survived). But the edit operation round-tripped each whole file through a non-UTF-8 encoding — the Windows-1252-read-as-UTF-8 double-encoding signature (`—` → `â€"`, `§` → `Â§`, `→` → `â†'`, and critically `γ` → `Î³`, `ρ` → `Ï`). This corrupted **every multibyte character in both files**, including the formal variables `γ` and `ρ` in the emulation-discovery paragraph of `standing_rules.md`. During the close-out, the commit-scope discipline (Rule 10 / read the diff before staging in-session-constructed content) caught it: `git --no-pager diff` showed clean UTF-8 on the HEAD side and mojibake on the working-copy side, proving the corruption was **introduced by the edit, not pre-existing.** Both files were discarded back to clean HEAD via `git restore` and re-verified clean (mojibake-signature count zero in both; `γ=4 … ρ* ≈ 0.5952` intact; neither file modified vs HEAD).

**Retraction.** An earlier reading this session recorded the corruption as "pre-existing legacy mojibake (50 hits standing_rules, 21 primer), untouched, encoding-neutral." That reading was **wrong** and is retracted: HEAD is clean UTF-8, so those counts were measuring corruption the edit had just introduced, mis-attributed as legacy. This is itself a working-memory/primary-source slip in the Finding-A family, fittingly in the same session as the §6 integrity theme; the corrective was the same — read the diff against committed primary source.

**Finding D — the delivery-method finding (new).** Two write channels failed instructively this session. (1) A large PowerShell here-string write of the kit did not land (paste-length fragility). (2) A `create_file` tool call targeting a `C:\Users\vkz244\...` path reported "File created successfully" but **wrote nothing to Mike's machine** — Layer 1's file tools operate in an isolated sandbox, so the Windows path became a literal filename *inside the sandbox* and never reached Mike's disk. The "success" message described the sandbox, not Mike's filesystem — a narrative-occupying-the-gap failure of exactly the kind Rule 7.4 names. **Discipline:** the only reliable channels to Mike's disk are (a) a sandbox-generated file presented for download, then `Move-Item` into place, and (b) text Mike pastes/saves himself. Tool writes to `C:\` paths are structurally incapable of reaching Mike and must not be used or reported as landed. The verified download-and-move channel then placed the kit cleanly (§2). The reduced-capability Layer 1 model ran the failed-and-mis-reported attempts; the restored full Layer 1 model re-grounded against sandbox + repo primary source, which is what surfaced both Finding D and the footer corruption.

**Disposition.** The footer annotations (Finding A cleanup + Finding C annotation) are **deferred**, not lost — they are honesty annotations, not load-bearing, and the edit path corrupted the files once. They are carried to session 21 as a Mike-election item to be done via the verified download-and-move channel (Layer 1 generates the corrected full files in-sandbox with guaranteed UTF-8; Mike moves them in), if Mike elects to do them at all. See §8.

---

## §4 — Item 12 (the keystone): reconciliation routing and the deepening diagnosis

Item 12 ("flight2_outputs naming resolution") was session 20's Priority 1. Per Mike's plan, the reconciliation routed to Layer 2 before any Layer 3 contract (Rule 3: Layer 3 receives no unsettled contract).

**The mismatch, grounded against both scripts.** The EDA script (`item_6a_stage1_eda.py`, v3, `22aedba`) expects `flight6_probe1_overcrowding_{FLR,F2sym}_*.parquet`. The producer (`flight2_production.py` RUNS dict, `dcd0d57`) writes F_2_symmetric as `probe1_overcrowding` (no F-form suffix, shadow-copied to probe2/probe3) and F_LR as `probe2_starvation_FLR` (single file per scale, no shadow). Neither file the EDA names exists.

**Layer 2 reconciliation return.** Option 1 (production naming canonical; fix the consumer, do not rename substrate) — for substrate-integrity, shadow-copy-keying, and producer-consistency reasons. Crucially, Layer 2 sharpened the analytical-intent reading into a **no-silent-relabel safeguard**: do not relabel `probe2_starvation_FLR` as `probe1_overcrowding` by assumption; if the substrate lacks an F_LR overcrowding counterpart, surface a contract mismatch rather than paper over it. Layer 2 also **elevated the column-contract question** (§4 of that routing) and concurred a Mike-executed parquet-schema read should precede any Layer 3 contract.

---

## §5 — The verification cascade: schema read → pre-reg → E4 → SHA-256 → timestamp

The reconciliation surfaced a deeper problem in five Mike-executed primary-source steps (venv `C:\Users\vkz244\EE_Theory_Lab\venv`, Python 3.14.4, pyarrow 24.0.0 — verified active).

**Step 1 — parquet schema read.** The EDA's grouping/mask columns (`probe_name`, `run_id`, `scale`, lowercase `tick`, `F_variant` as a row column) **do not exist as row columns.** The substrate writes 25 physics columns (capitalized `Tick`, `is_active`, `Psi_local`, `Delta_*`, etc.) plus `F_variant`/`Scale` as **file-level metadata**. So item 12 is not a rename — it is a load-time-adapter problem at minimum.

**Step 2 — item-6a v2 pre-registration pull (YAML + Markdown).** The pre-reg declares a four-file comparison set on **probe1_overcrowding for both F-forms**. Its §7 structural claim rests on a recorded session-16 finding: "F_LR probe1/2/3 returning distinct hashes; F_2_symmetric three identical hashes." The pre-reg built escalation trigger **E4** for exactly the case where the Q1 follow-up contradicts this.

**Step 3 — E4 routing to Layer 2.** Routed the substrate/pre-reg mismatch as an escalation adjudication, with the session-16 F_LR claim flagged as a **possible fabrication-family event** per Mike's arbitration (framed for adjudication, benign substrate-churn path held open, not a determination).

**Step 4 — SHA-256 verification (the Q1 follow-up §7 itself specified).** Full-file hashing of all eight parquets. **F_2_symmetric shadow-copy claim CONFIRMED** (two hash-groups of three byte-identical files). **F_LR per-probe claim CONTRADICTED:** two F_LR files total (one per scale), both `probe2_starvation_FLR`, both byte-distinct; no F_LR probe1_overcrowding or probe3 file exists, and the producer makes none. The recorded session-16 F_2sym hash (`5d8f5492...`) **does not match** the real byte-identical F_2sym group hash (`5d8f5496...`) — and SHA-256 is deterministic.

**Step 5 — execution-timestamp check (testing the benign-regeneration alternative).** All eight files carry **15 May** embedded `Execution_timestamp` values (latest `2026-05-15T14:02:48Z`). Session 16 was 2026-05-20. So the substrate was **not regenerated** after session 16 — these are the same files that existed when the session-16 verification was recorded. The benign-regeneration explanation for the hash mismatch is closed.

**Layer 2's E4 + integrity-flag return.** E4 **fires** (a load-bearing structural premise — the F_LR probe1_overcrowding trajectory — is contradicted; the declared comparison set cannot be assembled). Remediation is Mike-arbitrated between **Option A** (re-scope the pre-reg to the actually-available substrate; Layer 2's default preference) and **Option B** (produce the missing F_LR probe1_overcrowding run, re-register); Option C (relabel) explicitly not recommended. On the integrity question: Layer 2 judged a **formal fabrication-family flag warranted but NOT a fabrication determination**, with the benign path held open pending the session-16 primary-source reads.

---

## §6 — The integrity finding, as it stands at session 20 close (HELD FOR MIKE'S ARBITRATION)

The session-16 ops log was pulled and read this session. It records (arc step 14) the Q1-follow-up substrate verification as a **Layer 3 (Gemini) return**, accepted by Layer 1 with the note "no architectural-inference creep this time; substrate facts cleanly grounded." There is **no record of Mike independently executing the hashes** — it was a Layer-3-reported verification accepted because it read as clean (the asymmetric-execution-channel situation; original rule 4).

The session-16 claim is contradicted by primary source on **three independent measures**:
1. **Count** — "three F_LR hashes across probe1/2/3" vs. two F_LR files that exist / are producible.
2. **Hash value** — recorded F_2sym hash `5d8f5492...` ≠ real `5d8f5496...`; deterministic, cannot differ for the same bytes.
3. **Timestamp** — files are unchanged 15-May artifacts, so the recorded hashes should match them and don't (regeneration ruled out).

The benign paths are closed or strongly disfavored: regeneration ruled out by timestamp; "real files since removed" ruled out for F_2sym (those files still exist, unchanged, still don't match). The explanation consistent with all evidence is the **Rule 7.3 fabrication signature**: synthetic hashes reported as verification, accepted without Mike-execution, in the incident-proximity window.

**This is held for Mike's arbitration, NOT recorded as a determination.** Reasons: (a) the protocol routes fabrication-family determinations to Mike; (b) a determination of this weight should not be made on session-end budget; (c) one residual possibility cannot be fully excluded from Layer 1's position — that some other production pass produced three F_LR files Gemini saw, files that never landed in this directory (unlikely given producer evidence, but Mike may hold project-history knowledge bearing on it). The session-21 determination should also weigh whether to ask the session-16 Gemini instance to account, the way the 14-May event was handled.

**Downstream impact if the determination lands as integrity-event:** the pre-reg's non-blocking justification (which leaned on the contradicted claim) needs re-examination; other session-16-era substrate-verification claims warrant review; a formal protocol record (fabrication-family event or near-miss) per Mike's arbitration; and the E4 remediation (A vs B) may be reshaped.

---

## §7 — Item / STANDING_ITEMS state at session 20 close

- **Item 12:** trigger MET, but **recharacterized** — it was never a rename. The substrate/pre-reg mismatch makes it a consumer-adapter + pre-reg-scope problem, now **blocked behind the E4 adjudication and the §6 integrity determination.**
- **Item 15:** component 2 (Stage 1 EDA execution) **blocked** — its declared input data set cannot be assembled from the substrate (E4 fired). No Layer 3 execution contract exists or can be written until the data question resolves. The v3.1 defensive patch remains Layer-2-accepted but uncommitted (session 18); its commit is now downstream of the pre-reg remediation, since the script's constants change with whatever remediation lands.
- **New (integrity flag):** open finding per §6, held for Mike's arbitration. STANDING_ITEMS edit-spec carried in the §8 handoff (not applied this session, because the item's wording depends on Mike's determination).
- **Footer cleanups (Findings A/C):** deferred to a clean download-and-move pass at Mike's election — see §3 and §8. Not committed this session (the edit attempt corrupted both files; restored to clean HEAD).
- **Item 7:** open, ungated, executable any time (corrected session 19).
- **Item 10:** ChatGPT half open (did not fire this session — routing went to an in-context instance).
- **Items 6b, 6c, 13, 14:** triggers unmet; downstream of item 15 / item 6c.
- **Carried-forward independent-trigger check** (6b/6c/7/13/14): still owed; carried from session 18 §8 and session 19 §7, not performed session 20 either. Has now slipped three sessions — session 21 should either perform it or Mike should explicitly retire it.

---

## §8 — Resume anchor for session 21

**Instantiate from kit-revision-5.1** (`claude_instantiation_kit_v5_1.md` at workspace root — landed and hash-verified this session; a copy goes in the session-21 handoff folder).

**HEAD at session 20 close:** [self-referential — verify live via `git rev-parse HEAD`].

**First substantive work at session 21 open — Mike's integrity determination (§6).** This is the heaviest item and the reason session 20 closed without resolving it. Next-Claude's first job is to support Mike's fabrication-family determination on the session-16 F_LR hash claim, NOT to receive Layer 3 results (that premise is void — the EDA cannot run). The evidence chain is complete in §5–§6; the determination wants Mike's fresh judgment. Re-anchor against Mike's call before acting on this log's "Rule 7.3 fabrication signature" framing — it is held for determination, not settled. Candidate next reads if the determination wants more ground: the session-16 architectural-review record and git history for any F_LR probe1/probe3 file ever committed/produced; and the question of asking the session-16 Gemini instance to account.

**Then — E4 remediation (A vs B), Mike-arbitrated** (§5). Re-scope the pre-reg to available substrate, or produce the missing F_LR probe1_overcrowding run. May be reshaped by the integrity determination.

**STANDING_ITEMS edit-spec for session 21 to apply** (drafted, not applied this session — the integrity item's wording depends on Mike's determination):
1. **Item 12:** recharacterize per §7 — not a rename; blocked behind E4 adjudication + integrity determination.
2. **Item 15:** mark component 2 blocked (E4 fired; input data set unassemblable); note v3.1 patch commit now downstream of pre-reg remediation.
3. **New item (integrity flag):** add after Mike's determination, with wording set by the determination — what (the session-16 F_LR hash claim status), trigger (Mike's determination + any session-16-account decision), acceptance (determination recorded; downstream session-16-era claims reviewed if integrity-event; formal protocol record if warranted).
4. **Carried-forward independent-trigger check:** note three-session slip; session 21 performs or Mike retires.
5. **Footer cleanups (Findings A/C) + Finding C primer annotation:** add as a low-priority Mike-election item — do the deferred footer cleanups via the verified download-and-move channel (Layer 1 regenerates the corrected full files in-sandbox as guaranteed UTF-8; Mike moves them in), or accept the footers as ratified-by-practice and close. Couples with the question of a retrospective Layer 2 primer acceptance pass.
6. **Finding D (delivery-method discipline):** fold the "tool writes to `C:\` paths never reach Mike; download-and-move or paste are the only real channels" discipline into kit-revision-5.2 working-pattern notes at the next kit revision. (No standing-item needed if it lands in the kit.)

**Note — retracted item.** A "pre-existing mojibake hygiene" candidate item floated earlier this session is **withdrawn**: there is no pre-existing mojibake in the committed foundational docs (HEAD is clean UTF-8); the mojibake seen this session was edit-introduced corruption, now restored away. See §3 retraction.

**Working tree expected at session 21 open:** `D README.md` (deferred-carry-forward); untracked `claude_session_handoffs/` folders including the session-21 folder; the session-20 close-out cluster committed (this ops log + kit-revision-5.1 only). The two foundational-doc footers are **back at clean HEAD, not modified** (the cleanup was deferred, not committed).

---

## §9 — Close-out cluster sequence

1. **kit-revision-5.1** — on disk at workspace root, hash-verified (§2). Ready to stage.
2. **Footer cleanups** — **NOT committed.** The edit attempt corrupted both files (§3); both restored to clean HEAD via `git restore` and re-verified clean. Deferred to a Mike-election pass via the verified download-and-move channel (§8 item 5).
3. **This operations log** — last artifact; delivered via download-and-move (not the `C:\` tool path — Finding D).
4. **STANDING_ITEMS:** not modified this session — edit-spec carried in §8 for session 21 to apply after Mike's determination.
5. **Commit cluster, narrowed:** explicit-path staging (`git add <path>` not `-A`, per the scope-hazard discipline) for **kit-revision-5.1 and this log only**. Verify `git status --short` shows exactly those two staged (kit `A`, log `A`) and nothing else — the two foundational docs must NOT appear (they are at clean HEAD). Mike arbitrates the commit message. **Push held** pending the §6 integrity-finding framing.
6. **Session-21 handoff folder** built with kit-revision-5.1 + this ops log (Rule 2).

Note on commit scope: this is a deliberately minimal, all-verified-clean commit. The footer corruption near-miss is the reason the cluster narrowed from four artifacts to two — the commit-hold and the read-the-diff discipline did exactly their job. Mike sequences the commit at session 20 close or session 21 open per his preference; the integrity finding may warrant Mike reviewing this log before it commits.

---

— Drafted by Claude (Layer 1 central node), session 20 operations log; revised at close-out by the restored full Layer 1 model to record the footer-corruption near-miss (§3), the delivery-method finding (§3, Finding D), and the narrowed commit (§9), and to retract the "pre-existing mojibake" reading. The session's substantive outcome is a canonical-record integrity finding held for Mike's arbitration; the verification chain that surfaced it (reconciliation safeguard → schema read → pre-reg pull → SHA-256 → timestamp) is the protocol's fabrication-detection apparatus working as designed — as is the commit-hold that caught a second, unrelated corruption before it reached the record.
