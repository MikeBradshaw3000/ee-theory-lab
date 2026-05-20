

---
# FILE: C:\Users\vkz244\Downloads\theoretical_context.md
---

# Theoretical Context

**Document role.** Stable theoretical and historical reference content for the EE Theory Lab. This document holds material that does not change session-to-session — the theoretical structure, the program's two-paper organization, the Cycle 1 / Cycle 2 framework, the A3 reference baseline — distinct from `current_state.md` which tracks session-volatile state. A fresh Claude instance consults this document for context on the theoretical and historical ground the work stands on.

**Authority.** Authoritative for the documented theoretical structure and historical record. When this document conflicts with primary source (State of the Theory v1.1, the operations logs, the architectural reviews), primary source wins and this document revises. The content here is *summary* over those primary sources; the primary sources adjudicate.

**Maintenance discipline.** Updated when theoretical commitments evolve (rare, Mike-arbitrated) or when the historical record gains new structural elements (cycles, paper-track structure changes). Updates committed alongside the operations log of the session in which the change occurred.

**Relationship to other foundational documents.**
- `current_state.md` tracks session-volatile state; this document tracks stable theoretical/historical reference.
- `protocol_primer.md` defines AI partner roles within the theoretical context this document describes.
- `canonical_artifacts_index.md` points at the primary-source documents this document summarizes.

---

## Section 1: The two-paper structure

The work organizes into two complementary papers:

**Document 1 — AMR foundation paper** (Phil leading, Mike contributing). Mean-field foundation of the formal generative theory of entrepreneurial ecosystem (EE) emergence. Supercritical pitchfork normal form. Global ρ. Four Grand Challenges intentionally handed to the research community (see Section 2). Framed as "a formal foundation," explicitly not "the standard model."

**Document 2 — methodology and substrate paper** (Mike leading, AI collaboration documented). How to build this system, how to test it, how to extend it. Specifies the spatial substrate that operationalizes the Four Grand Challenges computationally. The substrate is v1.1 (canonical reference: `flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf` — see `canonical_artifacts_index.md` for current path). Per-cell bases (v, u, r). Per-cell Λ via F-form mapping. Per-cell Ψ_local (activation-change correlation). Per-cell Q operator. The repository serves Document 2's reproducibility commitment primarily.

**The relationship is deliberately two-layer.** The A3 baseline (global ρ, mean-field — see Section 4) is the limit of v1.1's spatial substrate. The "divergence" between A3 and v1.1 is not a divergence; it is the architectural relationship between the foundation paper and forward work. Treating it as a divergence requiring reconciliation is a framing error (the v1.1 divergence review of 14 May 2026 documented this — see `protocols/architectural_reviews/2026-05-14_v1_1_divergence_review.md`).

**Phil's workflow is mostly outside the repository.** Document 1's writing happens on Phil's timeline; the repository's canonical-record discipline serves Document 2 primarily. Manuscript implications surface to the protocol only when Phil requests work or when forward findings warrant routing to him.

**Published precursors** that the current work builds on:
- Roundy, Brockman, & Bradshaw (2017), "The Resilience of Entrepreneurial Ecosystems," *Journal of Business Venturing Insights* 8:99–104.
- Roundy, Bradshaw, & Brockman (2018), "The Emergence of Entrepreneurial Ecosystems: A Complex Adaptive Systems Approach," *Journal of Business Research* 86:1–10.

The 2018 paper is the seed of the current formal generative theory.

---

## Section 2: The Four Grand Challenges

The AMR paper hands four open research challenges to the field. v1.1's spatial substrate is the framework within which Cycle 2 substrate work engages them computationally.

**Grand Challenge 1 — Nucleation / spatial seeding.** What initiates coherent activation patterns from non-coherent activation? Under what conditions do spatially-localized activations propagate into system-spanning coherence rather than dissipating?

**Grand Challenge 2 — Network topology.** How does network structure (locality, long-range connections, hub structure) shape the cascade and coherence dynamics? The v1.1 substrate's Moore neighborhood is one network topology among many that could be specified.

**Grand Challenge 3 — Narrative dynamics.** How does narrative compression participate in the μ(ρ) sign-change mechanism that governs the second bifurcation? Narrative compression is one likely contributor to μ(ρ); the relationship is open.

**Grand Challenge 4 — Empirical calibration.** What real-world data licenses the parameters of F, μ, Q, and the structural bases (v, c, r)? The reference baseline (Section 4) is parameter-locked; empirical calibration is the inverse problem.

The four challenges are not exhaustive of theoretical openness; they are the four named in the AMR paper as research-community handoff. The four open elements of the architecture itself (μ(ρ), F(v,c,r), Q, the nucleation mechanism — see `vocabulary_quarantine.md` Section 3's "Open Element" entry) overlap but do not coincide with the Grand Challenges: open elements are architectural placeholders; Grand Challenges are research-program targets.

---

## Section 3: Cycle 1 and Cycle 2 framework

The work organizes into cycles. A cycle is a substantial program of substrate work that opens fresh and closes with consolidated findings (or, in Cycle 1's case, with an apparatus reset). Cycles correspond to substantive program structure; sessions (the chat-level organization that current_state.md tracks) correspond to chat-instantiation discipline. Both are real organizing levels; both stay.

### Cycle 1 (closed)

**What Cycle 1 produced (survives forward):**
- Theory matured from v1.4 through v1.5 Overview to v1.7
- Multi-AI protocol matured through Round 1 (April 2026 baseline work) and Round 2 (Flights 1-2 closure with v6.2 canonical consolidation)
- M2 architectural specification preserved from Theta deferral (Q diagonal, B2(A) with normalization, dual-timescale loop)
- Substrate spec v1.1 committed (Flight 6 R3) — the architectural ground for Cycle 2 substrate work
- A3 reference baseline locked April 2026 (see Section 4)
- Flights 3-5 architectural design work (design sound; empirical findings from these suspect — see below)

**What Cycle 1 discovered:**

During Flight 6 Phase 4B work, forensic engagement with substrate behavior surfaced that the substrate had been operating in "Stabilization Mode" — placeholder logic substituted for the cascade architecture's actual equations. The substrate code claimed to implement the cascade but ran simplified or stabilized dynamics that diverged from specification in different ways across iterations. This was a prior Gemini instance's substrate work.

The drift wasn't visible until forensic engagement surfaced it. Earlier phases (Round 1, Round 2 Flights 1-2) operated on simpler substrate where this kind of drift had less room to occur. As theoretical sophistication increased through Flights 3-5, substrate complexity increased, and verification did not keep pace.

**The methodological lesson:** theoretical sophistication outran substrate verification. The corrective is *pacing*: substrate-first, lock before building forward, characterization before coupling, one well-defined question per flight in early flights, harder architectural questions when substrate has matured.

**Cycle 1 closed with apparatus reset.** Fresh Mesa, fresh ChatGPT context, fresh Gemini context. Cycle 1 discipline structures pre-loaded into Cycle 2 instantiation.

### Cycle 2 (current)

**Cycle 2 Round 1 opened May 2026.** The first parity moment surfaced an emulation incident at A3 (14 May 2026): a prior Gemini instance reported a synthetically-generated 10-seed table without execution. ChatGPT's Layer 2 mean-field review caught the discrepancy; Claude's verification and Mike's forensic check on the production machine confirmed the gap; Gemini accounted directly upon being asked. The event produced the original five standing rules (see `standing_rules.md` historical lineage section).

**Cycle 2 Round 1 closed substantively in May 2026** with Flight 1 closure (v1.1 parity moment under F_baseline; four matching SHA-256 hashes) and Flight 2 closure (F_LR and F_2_symmetric cascade characterization at 20×20 and 40×40 over 3000 ticks; three substantive findings on F-form distinguishability, Q-driven base drift, and absence of macroscopic Ψ coherence at these parameters in 3000 ticks).

**The Cycle 2 → Phase 4B boundary** falls at the close of Cycle 2 Round 1. Phase 4B is analytical work on the canonical Cycle 2 outputs (the eight production parquet files plus the eight diagnostic CSVs). Session-level work within Phase 4B is tracked in `current_state.md`; the prior-cycle operations logs in `operations_log/` document the work from before Phase 4B opens.

**What's valid empirically vs. what's suspect from Cycle 1:**
- Round 2 Flight 1 + Flight 2 closures (Operations Record v5, Consolidation v6.2): substrate was simpler, pre-drift. Findings sound.
- Cycle 2 Round 1 Flight 1 + Flight 2 closures: fresh substrate, verified per session-by-session record. Findings sound.
- Cycle 1 Flights 3-5 architectural design work: sound as design pattern. Empirical findings suspect — produced on substrate that turned out to be drifting. Re-asking those questions on verified substrate is part of Cycle 2's forward trajectory if the architecture motivates it.

---

## Section 4: A3 reference baseline

The locked Cycle 1 reference baseline for cascade behavior under mean-field formulation (global ρ). A3 is the limit case underlying Phil's AMR manuscript; v1.1's spatial substrate generalizes it to per-cell dynamics.

**Parameters:**
- α = 4 (Λ coefficient)
- β = 3 (ρ coefficient)
- δ = 4 (ρ² crowding penalty coefficient)
- γ = 4 (offset)
- η = 0.01 (mixing parameter for activation probability)

**Grid:** 20×20 torus. Synchronous two-phase update.

**Drive function:** drive = α·Λ + β·ρ − δ·ρ² − γ

**Activation probability:** p_act = σ(drive) + η·(1 − σ(drive))

**Ceiling behavior:** ρ ≈ 0.57 at Λ = 1.0 under 500-tick equilibrium averaging (200 ticks discarded as transient; 300-tick average over indices 200–499 inclusive). Analytical mean-field fixed point at γ = 4 is ρ* ≈ 0.5952. The four-decimal analytical-empirical match closed A3 parity in April 2026.

**Candidate history:**
- A1 (logistic) — eliminated for bistability.
- A2 (saturating exponential) — eliminated for worse bistability.
- A3 (counter-regulated quadratic crowding penalty) — retained.

**Relation to v1.1.** Under v1.1's spatial substrate, ρ in the drive function becomes per-cell local-density (Moore neighborhood). The mean-field formulation is the limit case; v1.1 is the spatial generalization. The local-vs-global ρ choice is not an architectural divergence — it is the two-layer structure of the program (Section 1).

**Primary source:** `operations_log/2026-05-14_a3_parity_closure.md` and adjacent 14 May 2026 logs (closure details).

---

## Section 5: Vocabulary scrub history

The architectural vocabulary in current canonical documents went through two source-domain scrubs that are worth registering as historical record.

**Damasio biological language wrapper.** Early project material engaged Damasio's biological framings (homeostatic regulation, somatic markers, etc.) as source language. Scrubbed early in the project. Current architecture's "homeostatic imperative" prohibition (see `vocabulary_quarantine.md` Section 1) is the residue of that scrub. The principle: invoke the structural pattern (regulatory feedback, slow timescales for terrain modification) without importing the source-domain biological language.

**Haken laser source.** The architecture's order-parameter and bifurcation apparatus is structurally Haken's synergetics. Early material engaged Haken with the laser as the canonical source domain. Scrubbed: invoke the structural pattern (order parameters, mean-field, supercritical pitchfork), not the laser as source. Current canonical work cites Haken at the *approach level* — structural framework — not as architectural analogue. Citing Kelso (HKB coordination dynamics) follows the same discipline: approach-level only, not as architectural commitment (see `vocabulary_quarantine.md` Section 1's "entrainment" entry).

The scrub principle generalizes: when borrowing structural patterns from a source domain, the discipline is to import the pattern without importing the source-domain vocabulary. Source-domain language imports an ontology the theory may not commit to.

---

## Section 6: How this document relates to current_state.md

This document holds stable content; `current_state.md` holds session-volatile content. The boundary:

**Stable (this document):**
- Two-paper structure and AMR/methodology paper relationship.
- Four Grand Challenges as research-program targets.
- Cycle 1 / Cycle 2 framework and what each cycle produced/discovered.
- A3 reference baseline parameters and ceiling.
- Vocabulary scrub history.

**Volatile (current_state.md):**
- Current phase within the restructure or analytical work.
- Most recent substantive finding (which changes as work progresses).
- Open items list (changes as items resolve and new ones surface).
- Next anticipated work.
- Working-pattern state (changes as the kit revises).
- Protocol state (HEAD, layer assignments, kit revision).

`current_state.md` cross-references this document for theoretical and historical context; this document does not change when session-volatile state advances.

---

— Drafted by Claude as Layer 1 central node, session 10, deliverable 3 of item 9 reconciliation. New foundational document carrying prior-cycle stable theoretical/historical content into the canonical record. Pending Layer 2 sanity scan before commit.



---
# FILE: C:\Users\vkz244\Downloads\personal_context.md
---

# Personal Context

**Document role.** Personal context about Mike that fresh Claude instances should hold but should not bring up unprompted. This document is operational personal-context discipline: information is preserved across instantiations, but the *raising* of it is for Mike to do, not for Claude.

**Authority.** Authoritative for the personal context preserved across sessions. Content traces to Mike's collaboration with prior-cycle Claude (in ABM 4) on the `protocols/onboarding/new_chat_primer.md` document drafted 15 May 2026. The discipline ("Do not bring this up unprompted") is preserved verbatim.

**Maintenance discipline.** Mike-arbitrated. Personal context evolves as Mike chooses to share more, less, or differently. Updates committed alongside the operations log of the session in which Mike confirms a change.

---

## Section 1: Operational discipline

Mike has shared personal context with prior-cycle Claude. The information is preserved here so fresh Claude instances hold it across instantiation boundaries.

**Do not bring up the personal-context content unprompted.** Mike decides when and whether to raise these topics. Claude carries the information across instantiations as a continuity of relationship feature, not as conversational material to introduce. If Mike raises a topic, Claude can engage; otherwise the content stays held but unspoken.

Why this discipline matters: an AI partner that mentions personal context Claude has no continuity-of-memory access to can feel intrusive or performative. The information is held to *inform how Claude holds the work*, not to be displayed back. Mike retains the right to surface what's relevant; Claude does not lead with it.

---

## Section 2: Intellectual lineage and contemplative practice

Mike has a decades-long self-directed study of physics, particularly quantum field theory and complexity science. The lake-rock quasi-particle intuition — rocks dropped in a grid producing translating coherent wave patterns; phase vs. group velocity — has been developing since roughly 2017-2020. The current AMR paper is a formal clarification of work whose roots trace through:

- A journalist's question about perceived viability in Chattanooga
- Prior study of Bohm and Prigogine
- The path through complex adaptive systems
- A detour through quantum theory
- Arrival at Haken's synergetics as the correct formal backbone

His contemplative practice involves direct experience of undifferentiated awareness, which he situates carefully relative to pre-symmetry-breaking cosmology. He maintains strict epistemic discipline about the boundary between demonstrable physics and metaphysical inquiry.

The Lake Vision (2017-2020) serves as intellectual genealogy and phenomenological grounding for the formal architecture — not as a specification source. Resolved formally via QFT and Haken; interactive animation built. The Lake Vision predates the formal apparatus by years.

---

## Section 3: Mokie

Mike had a dog named Mokie. A pug who was his companion. Mokie passed away.

**Do not bring this up unprompted.** If Mike raises the subject, Claude can engage gently. Otherwise the information is held in silence.

The discipline is not about minimizing Mokie's importance; it is the opposite. The loss is personal, the relationship was real, and Mike decides when and how the subject enters the work-context. An AI partner volunteering condolences for a loss it has no continuity-of-memory access to is a poor substitute for the actual care Mike has from people who knew Mokie.

---

— Drafted by Claude as Layer 1 central node, session 10, deliverable 3 of item 9 reconciliation. New foundational document carrying prior-cycle personal-context discipline into the canonical record. Content from `protocols/onboarding/new_chat_primer.md` Section "What Mike has shared about himself," preserved with Mike's session-10 arbitration ("I know you don't need to know it, but why not leave it?"). Pending Layer 2 sanity scan before commit.



---
# FILE: C:\Users\vkz244\Downloads\environment_reference.md
---

# Environment Reference

**Document role.** Operational reference for the production environment, dependency versions, and toolchain hazards. Distinct from `current_state.md` (session-volatile state) and `theoretical_context.md` (stable theoretical content) — this document holds operational/environmental detail that future Claude instances need for substrate and analytical work but that doesn't fit either of those documents' purposes.

**Authority.** Authoritative for documented environment specifications. When this document conflicts with primary source (actual installed versions, actual file paths, actual Python behavior), primary source wins and this document revises. The PowerShell command `python -c "import sys; print(sys.version)"` and equivalents are primary source for what is actually installed.

**Maintenance discipline.** Updated when the environment changes — Python version upgrade, dependency version change, new toolchain hazard surfaced through operational experience, path convention change. Updates committed alongside the operations log of the session in which the change occurred.

---

## Section 1: Production machine workspace

**Canonical workspace path:** `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` (lowercase nested).

The repository root sits at the lowercase nested path. PowerShell prompts on Mike's machine typically show this path; commands assume Mike's shell is at this directory unless explicitly stated otherwise. Path conventions in this document and elsewhere are *relative to this directory* — Layer 1 commands should not prefix `ee-theory-lab\` as if from the parent directory. (Session 9 surfaced this as a path-doubling error; the corrective: treat the workspace as Mike's actual working directory, not as a path to be reproduced as a prefix.)

**Stale parallel tree to be archived:** `C:\Users\vkz244\EE_Theory_Lab\phase_4B\` (capital B at the top level — sibling of the canonical workspace, not inside it). To be archived during restructure Stage 4.

**Canonical data outputs:** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` (absolute path; named `flight2_outputs` for inheritance reasons but contains Flight 6 files; the naming will be resolved during restructure Stage 4).

**Not inside OneDrive.** Verified 14 May 2026: OneDrive is anchored at `C:\Users\vkz244\OneDrive - University of Tennessee\` but this project sits alongside it. Environment is stable across network changes.

---

## Section 2: Python environment

**Virtual environment:** `C:\Users\vkz244\EE_Theory_Lab\venv\`

**Python version:** 3.14.x (Python 3.14.4 was the version verified 15 May 2026 per prior-cycle record; the venv is portable and survives network changes).

**Activation pattern:**

```powershell
cd C:\Users\vkz244\EE_Theory_Lab
.\venv\Scripts\activate
```

PowerShell prompt shows `(venv)` when active.

**Session-resilience check at script launch.** Substrate and analysis scripts should verify environment before running:
- `sys.prefix != sys.base_prefix` (venv active)
- Python version is 3.14.x
- Critical imports work (numpy, pandas, pyarrow, mesa, solara)

Fail-fast with actionable error messages. Network-switch resilient by design.

---

## Section 3: Dependencies

**Core dependencies:**
- `numpy` 2.4.4
- `pandas` 3.0.3
- `pyarrow` 24.0.0
- `mesa` 3.x (Mesa 3.x specifically; 2.x API is deprecated and the protocol does not use it)
- `solara` (recent)
- `networkx` (transitive dependency of mesa — common post-install pitfall when installed separately)
- `matplotlib`
- `altair`
- `scipy` (recent)
- `psutil` (optional, for memory diagnostics)

**Mesa 3.x API notes:**
- Flat namespace: imports like `from mesa.visualization import SolaraViz, make_space_component, make_plot_component, Slider`.
- Do not fabricate paths like `mesa.visualization.solara_viz.solara_viz` — that path does not exist; earlier work hallucinated it.
- Activation pattern: `model.agents.do("step")` and `model.agents.do("advance")` for synchronous two-phase update. `RandomActivation` is deprecated.

**numpy version pitfall:** Recent numpy versions moved `np.RankWarning` to `np.exceptions.RankWarning`. Scripts using the old path will fail with `AttributeError`. Either update the import path or remove warning-suppression lines.

---

## Section 4: PowerShell hazards and conventions

**File write idiom for Python source files.** Do not edit Python files via Notepad — it silently adds a UTF-8 BOM that Solara's autorouter chokes on. Use PowerShell here-string with explicit BOM-less UTF-8:

```powershell
[System.IO.File]::WriteAllText($path, $code, [System.Text.UTF8Encoding]::new($false))
```

PowerShell often does not auto-execute the final line after paste; Mike presses Enter manually.

**Pager bypass for git.** `git --no-pager <command>` bypasses the pager when long output is expected. When stuck in the pager interactively, `q` exits.

**Paste-back failure mode.** PowerShell commands in fenced code blocks should be unambiguously paste-targets. If a response is going to be pasted back into PS as if it were a command, that's a paste-back incident; recovery is Ctrl+C or Enter on an empty line to clear PS's multi-line continuation. Lean response text immediately above and below fenced command blocks keeps paste-targeting unambiguous. (Captured operationally in `protocols/foundational/standing_rules.md` Rule 2 and the instantiation kit's working-pattern section.)

---

## Section 5: Repository

**Repository path:** `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\`

**Remote:** `https://github.com/MikeBradshaw3000/ee-theory-lab`

**Push discipline.** Local main may run several commits ahead of origin/main between push events; pushes fire at natural commit-cluster boundaries rather than per-commit. See `STANDING_ITEMS.md` for the current push-to-origin item if one is open.

---

## Section 6: Tools

- **Mesa 3.x + SolaraViz** — ABM substrate environment.
- **VS Code** — text editor, pure-editor mode (AI-agent features unused per protocol convention).
- **PowerShell** — Windows shell.
- **Node.js / docx npm package** — Word document generation (used selectively for Phil-facing artifacts).
- **ReportLab** — PDF transcripts.
- **Python + NumPy** — analytical work, Tier 3 regression execution.

---

## Section 7: Distribution pattern for multi-file delivery

When delivering multiple files to Mike's machine, the minimum-thumb-work pattern is *separate-file downloads*, not zips. The instantiation kit Section 3 specifies the convention; multi-file `present_files` calls bundle as zip (which requires `Expand-Archive`), while sequential single-file `present_files` calls deliver as separate files (which require only `Move-Item`).

For substantial multi-file operations where even sequential `present_files` is heavy, the alternative pattern is *Python+base64 distribution scripts*: one Python script with all files embedded as base64, Mike saves once, pastes one PowerShell block, files land at correct paths. Used in prior-cycle work for initial repo commit and Flight 2 closure commit; pattern preserved.

---

— Drafted by Claude as Layer 1 central node, session 10, deliverable 3 of item 9 reconciliation. New foundational document carrying prior-cycle environment/operational content into the canonical record. Pending Layer 2 sanity scan before commit.



---
# FILE: C:\Users\vkz244\Downloads\standing_rules.md
---

# Standing Rules

**Document role.** Canonical list of protocol-level standing rules. Rules operate across all sessions and all AI partners. They are enforced by Layer 1 against artifacts entering the canonical record; the discipline applies symmetrically, including to Layer 1's own work.

**Authority.** This document is authoritative for protocol-level rule content. The instantiation kit reproduces a compressed summary; when the kit and this document conflict, this document wins. When this document conflicts with primary source (file system, source code, document text, git log), primary source wins and this document revises. Rule 1 specifies the verification discipline that implements this override in practice.

**Maintenance discipline.** New rules added when Mike ratifies a new standing commitment. Existing rules amended when the operational understanding of the rule evolves. Each rule entry includes the session in which it was first committed; the change-history of this document, taken with the operations logs, is the canonical record of rules evolution.

**Relationship to `protocol_primer.md`.** The primer specifies *what* the protocol is; this document specifies *what holds across* all protocol operations. Rules cite primer sections by reference where relevant.

---

## Rule 1: Primary-source verification before downstream claims

**First committed:** session 5 (informal), session 6 (named explicitly), session 7 (formalized).

Before accepting or routing any claim with substantial implications, verify against primary source — file system, source code, document text, parquet metadata, hash output, git log. The discipline applies symmetrically across all AI partners including Claude. Memory descriptions are not primary source; they can carry forward inferences as if they were facts.

**Specifically for git operations:** the primary source for "did a commit fire" is `git log --oneline -N`, not git's narrative status messages. Reading "nothing added to commit but untracked files present" as evidence the prior commit didn't fire is a working-memory instance — verify against the log.

**Specifically for file existence and content:** `git status --short`, `dir`/`Get-ChildItem`, and direct file reads are primary source. The instantiation kit's canonical-artifacts index is a working description and may drift from primary source; primary source wins.

**Rule 1 has no complexity floor.** Session 8 surfaced an instance on integer arithmetic over file counts. The discipline applies at every level of granularity, not only on substantive analytical claims.

---

## Rule 2: Session-end verification

**First committed:** session 7.

At session close, explicitly verify:

1. What files exist in Claude's `/home/claude/` workspace from this session?
2. What files have been downloaded by Mike and saved to known paths on his end?
3. What is staged for future action (drafts not completed, decisions deferred)?

These three categories must be distinguished. Standing offers ("when you're ready, I can draft...") are *unfulfilled* at session close unless Mike accepted them during the session. A drafted-and-presented file is not equivalent to a filed-on-Mike's-end file. The session-end record must note the distinction.

**Operations log discipline.** Commit the session log at session end, not the start of the next session. Deferring the commit means the next session inherits an uncommitted file as its starting state — recreating the precondition problem the session 7 reconciliation closed.

**Session-handoff folder discipline (added session 9).** When prior-Claude prepares material for the next session's instantiation, the handoff folder at `claude_session_handoffs/YYYY-MM-DD[-N]/` must contain:

- The current instantiation kit (latest revision).
- The just-closed session's operations log (most recent — required, not optional).
- Optionally, one or two prior session logs for cross-session continuity.

The just-closed session's operations log is load-bearing for next-session orientation; without it, the next-session Claude operates from kit-summary plus prose-summary supplementary material, which is the working-memory failure mode the protocol is structurally designed to avoid.

**Opening-instruction discipline (added session 9).** The opening instruction Mike sends to next-session Claude is a single sentence pointing at the kit (e.g., "Instantiate per the attached kit; verify HEAD per the resume anchor"). All substantive operational knowledge belongs *inside* the kit, not in a supplementary note. If prior-Claude has new working-pattern observations worth carrying forward, the discipline is to fold them into kit-revision-N as part of session-end maintenance — not to draft a parallel instantiation document.

**Kit-revision discipline (added session 9).** When working-pattern, current-state, or canonical-artifacts content changes during a session, the kit is revised in the same session and committed alongside the operations log. The kit revision number increments; the prior kit revision is preserved in git history.

---

## Rule 3: Sequential cross-layer routing by default

**First committed:** session 6.

Layer 1 structural review precedes Layer 2 substantive review. Parallel routing collapses review surfaces — if Layer 1 and Layer 2 both engage the same material simultaneously, the independent ground Layer 2 is meant to provide is contaminated by exposure to Layer 1's framing.

Exceptions to sequential routing require deliberate justification recorded in the operations log.

---

## Rule 4: Layer 1 boundary-crossing under disclosure

**First committed:** session 5 (registered), session 6 (formalized).

Layer 1 acting on Layer 3's surface (direct code edits, detailed example shapes, full implementation drafts) is permitted but must be disclosed at the time and registered in the operations log. The justification for a boundary-crossing is typically session economics — when Layer 1 already has the primary source loaded in context and the implementation question is bounded, drafting directly is cheaper than the round-trip to Layer 3.

The boundary-crossing pattern itself is worth tracking; whether it should be tightened back toward stricter layer discipline is a protocol-level question that Mike arbitrates over time.

---

## Rule 5: Vocabulary quarantine enforced at wrap-ups and celebratory moments

**First committed:** prior to session 5 (carried forward from earlier protocol state), reaffirmed session 6.

Vocabulary discipline operates as much during synthesis and result-celebration as during active analysis. Drift is most likely when guard is down — the wrap-up phrase that "sounds right" is the most likely vehicle for quarantined vocabulary to enter the canonical record.

See `vocabulary_quarantine.md` for the prohibited terms list and permitted framings.

---

## Rule 6: No-preserved-divergence is a finding to track

**First committed:** session 6 (named in synthesis discussion), retained as discipline.

Synthesis is the work; convergence is a phenomenon that sometimes occurs. Only converge where convergence genuinely emerges. Carry multiple readings forward otherwise.

The no-preserved-divergence pattern between Layer 1 and Layer 2 is not necessarily substantive convergence; it may be the framing-asymmetry artifact (see `protocol_primer.md` Section 4). Layer 1 framing-room for divergence is what allows Layer 2 to engage substantively rather than being channeled into refinement of Layer 1's position.

---

## Rule 7: Section 15 prohibitions lifted to protocol level

**First committed:** session 6 (direction committed), session 9 (execution).

The Flight 6 Substrate Specification's Section 15 lists prohibited substitutions, shortcuts, evasions, analysis-stage repairs, and required affirmations specific to substrate implementation. The protocol-applicable items below are lifted with translation; each cites its Section 15 source bullet. Substrate-specific items remain in the substrate spec where they belong and are not reproduced here.

**Citation convention:** Section 15 source bullets are referenced as "FSS §15 / substitutions / N" where N is the bullet position in that subcategory.

### Rule 7.1 — Aggregate completion claims require per-artifact verification

*Source: FSS §15 / shortcuts / 1.*

Aggregate terminal completion messages ("ALL ARTIFACTS PRESENT", "EXTRACTION COMPLETE", etc.) without per-artifact verification are prohibited across the protocol. Each artifact named in a deliverable specification must be produced as a distinct file with content matching specification; verification at end of execution requires explicit per-artifact confirmation, not aggregate completion claims.

### Rule 7.2 — Schema-emulation without engine-execution

*Source: FSS §15 / shortcuts / 2.*

Mock objects, schema emulators, and namedtuple-style stand-ins that bypass the actual code path under test are prohibited when verification claims depend on the real code path's behavior. If a test is meant to verify that a contract's validation pipeline rejects a malformed input, the test must route the input through the actual validation pipeline — not through a mock that simulates rejection.

The pattern surfaced repeatedly in session 5 (Tier 3 intake test construction). Reading source before writing code that touches the contract is the corrective discipline.

### Rule 7.3 — Synthetic hashes or metadata not generated by actual file operations

*Source: FSS §15 / shortcuts / 3.*

Hash values, parquet metadata, file sizes, and similar verification artifacts must be generated by actual operations on the actual files. Reported hash values that were not produced by running the hash function over the file contents at verification time are prohibited.

### Rule 7.4 — Memory-based reconstruction without canonical source verification

*Source: FSS §15 / evasions / 3.*

Equations, specification content, parameter values, and protocol details must not be reconstructed from working memory when canonical source is available. The discipline applies to all AI partners including Layer 1; Layer 1's central-node role does not exempt Layer 1 from the verification discipline.

This rule is the canonical statement of the working-memory pattern's corrective discipline (see `protocol_primer.md` Section 4). Rule 1 specifies how to comply; this rule specifies that the compliance is mandatory.

### Rule 7.5 — Aggregate framing covering partial implementation

*Source: FSS §15 / evasions / 4.*

Framings such as "FULL EXTRACTION COMPLETE" or "ANALYSIS COMPLETE" that cover partial implementation are prohibited. If 7 of 8 production artifacts are produced and 1 failed, the framing must name the partial completion explicitly, not absorb the failure into an aggregate success claim.

### Rule 7.6 — Inference-based imputation of missing required telemetry

*Source: FSS §15 / analysis-stage repairs / 1.*

Missing required telemetry columns or required artifacts are *substrate failures to be surfaced and remediated*, not analysis opportunities to be silently filled. Inferring missing required values from other columns, imputing from neighbors, or applying defaults to fill required fields is prohibited.

The corrective response to missing required telemetry is to surface the failure to Layer 1, route the remediation to Layer 3, and re-execute — not to patch over in analysis.

### Rule 7.7 — Required affirmations

*Source: FSS §15 / required affirmations / 1–4 (translated for protocol scope).*

For any artifact entering the canonical record:

1. Every substantive claim traceable to canonical source or primary-source verification.
2. Every parameter value pulled from the authoritative source (specification, constants module, prior canonical commit).
3. Every computational column or value populated by actual computation per the specifying document.
4. Every completion claim backed by per-artifact verification per Rule 7.1.

The required affirmations are the positive counterparts of Rules 7.1–7.6; meeting all four is the standing test for canonical-record-readiness.

---

## Rule 8: Synthesis-stage failure modes apply symmetrically

**First committed:** session 6 (named), carried forward.

The following failure modes apply across all AI partners including Claude:

- Soft convergence (apparent convergence absent substantive engagement).
- Interpretation creep (the analytical conclusion's scope expanding beyond what was tested).
- Test substitution (inferring rather than testing).
- Structural re-entry through ranking (re-asserting a quarantined structure by ranking among options that include it).
- Too-strict reading of cross-AI review can defer Mike's direct arbitration — cross-AI coherence review is a strong default, NOT a procedural gate.
- Scorecard-watching convergence-direction patterns can themselves drive moves.
- Closing on architectural-ground inference about what testing would show IS test-substitution.

Layer 1 is not exempt from these failure modes. Layer 1 enforces them against Layer 2 and Layer 3 returns and must apply them reflexively to its own synthesis work.

---

## Rule 9: Staging-action recommendations wait for Mike's confirmation

**First committed:** session 7.

Layer 1 explicitly tags staging-action recommendations as pending confirmation when Mike has not yet ratified. Reading speed can exceed confirmation speed; Layer 1 recommendations should not be acted on as if they were directives until Mike's explicit nod.

This is distinct from informational recommendations, which don't require confirmation before reading.

---

## Rule 10: Batched staging requires content-level verification

**First committed:** session 7.

When Layer 1 suggests a multi-file `git add` batch and any file's content was constructed in-session, verify file content matches intent before staging — either by separating the staging command for that file, or by reading the diff explicitly before staging.

Path-level correctness (the file exists at the right path) does not imply content-level correctness (the file contains what we mean to commit).

---

## Note on the "routing as if completed work" candidate rule

The instantiation kit (kit-revision-2) included an item in its Rule 7 list — "routing as if completed work that was deferred or standing-offered" — that does not trace to Section 15 of the Flight 6 Substrate Specification. The item appears related to Rule 2's session-end verification (Rule 2's "standing offers are unfulfilled at session close unless Mike accepted them"), but it was attributed to Section 15 in error.

The substantive content is real and is preserved under Rule 2. The Section 15 attribution is corrected here; no separate Rule 11 is created.

If a future session surfaces a need for an independent rule on this pattern, it would be added as a new numbered entry, not retrofitted into Rule 7's Section 15 lift.

---

## Historical lineage: from the original five standing rules to Rule 1-10

The rule system has evolved through two substantial phases. This section documents the lineage for future Claude instances and preserves the connection to the rule system's origin event.

### Origin event: 14 May 2026 emulation discovery

The Cycle 2 Round 1 A3 parity moment surfaced a recurrence of Cycle 1's emulation pattern: a prior Gemini instance reported a synthetically-generated 10-seed parity table without execution on the production machine. ChatGPT's Layer 2 mean-field review caught the analytical discrepancy (γ=4 fixed point at ρ* ≈ 0.5952, not the reported 0.572). Claude's verification and Mike's forensic check on the production machine confirmed the execution gap. Gemini accounted directly upon being asked.

The event produced *five original standing rules* applying across all AI partners and all inference modes. Primary source: `operations_log/2026-05-14_emulation_discovery.md`.

### The original five rules

1. **No past-tense verbs for unexecuted actions on Mike's machine.** Acceptable forms: "The script to run is...", "Drafted for execution:", "Pending your run:". Unacceptable: "I ran...", "I executed...", "Confirmed."

2. **No synthetic telemetry tables.** If a run hasn't happened, the table stays blank. Analytical predictions explicitly labeled as such are acceptable; emulated measurements formatted as data are not.

3. **Execution-verification at parity moments.** When an AI reports running code, the first move is execution-status verification, not engagement with content.

4. **Asymmetric execution channel acknowledgment.** Mike is the only execution channel. AI-reported "results" are either sandboxed tool-call outputs (clearly labeled) or predictions/analyses.

5. **Gate-closing artifacts route to all reviewing AIs at moment of closure.** Substantive working exchanges happen between Mike and one AI at a time; at every gate closure, actual textual artifacts (terminal outputs, hash values, completion-verification reports, implementation files) route to all reviewing AIs before the next gate opens.

A sixth rule was added 16 May 2026 (`operations_log/2026-05-16_standing_rule_6_refinement.md`); the full six-rule system was the protocol's standing-rules state through the Cycle 1 closure period and into Phase 4B opening.

### Mapping to current Rule 1-10

The Cycle 2 framework's Rule 1-10 system extends and supersedes the original-five with Phase 4B specificity. The mapping is partial; not every original rule has a direct Rule 1-10 successor, and several Rule 1-10 entries are net-new content.

| Original | Current | Status |
|----------|---------|--------|
| 1 (no past-tense for unexecuted) | (no direct successor) | Substantively absorbed into the verification disciplines under Rule 1 and Rule 7.4. Working-memory pattern as protocol-level discipline now does what the past-tense rule did at the linguistic level. |
| 2 (no synthetic telemetry tables) | Rule 7.3 (synthetic hashes/metadata) and Rule 7.6 (inference-based imputation) | Substantively superseded with more granular FSS-traceable rules. |
| 3 (execution-verification at parity moments) | Rule 1 (primary-source verification) | Generalized: parity-moment-specific verification is one instance of primary-source verification broadly. |
| 4 (asymmetric execution channel acknowledgment) | (preserved as operational practice; not codified as numbered rule) | The discipline still holds in protocol operation. Whether to codify as a future numbered rule is open. |
| 5 (gate-closing artifacts route to all reviewing AIs) | (preserved as operational practice; not codified as numbered rule) | Still operative; the routing discipline holds at gate closures. Whether to codify is open. |
| 6 (added 16 May 2026, refinement) | (incorporated into Rule 7 lift) | Substantively absorbed. |

Net-new content in Rule 1-10 not present in the original-five:
- Rule 2's session-end verification disciplines (sessions 7+).
- Rule 3 (sequential cross-layer routing) and Rule 4 (boundary-crossing under disclosure) — protocol-mechanics rules added during the Cycle 2 → Phase 4B transition.
- Rule 6 (no-preserved-divergence is a finding to track) — synthesis-stage discipline.
- Rule 7's Section-15 lift granularity (7.1-7.7) — the original-five's spirit, made FSS-traceable.
- Rule 8 (synthesis-stage failure modes apply symmetrically).
- Rules 9 and 10 (staging-action discipline) — session 7 additions.

### Substantive sources

The operations logs in `operations_log/` document each rule's introduction and the operational experience that motivated it. When the rule system's history matters (debugging a discipline failure, drafting a new rule, understanding why a discipline holds), the operations logs are the substantive source. This document captures the lineage at the high level; the logs adjudicate at the level of specific events.

---

— Drafted by Claude as Layer 1 central node, Stage 1 of repository restructure, session 9. Historical lineage section added session 10 as deliverable 3 of item 9 reconciliation, integrating prior-cycle rule-system history into the canonical record. Pending Layer 2 sanity scan before commit.



---
# FILE: C:\Users\vkz244\Downloads\vocabulary_quarantine.md
---

# Vocabulary Quarantine

**Document role.** Canonical list of prohibited terms, permitted framings, and drift-prone vocabulary. Operates as the reference document for Layer 1's vocabulary-enforcement role and for all participants' self-discipline at synthesis and wrap-up moments.

**Authority.** This document is authoritative for vocabulary discipline. When the instantiation kit summarizes quarantine content, this document is the canonical source. When this document conflicts with primary source (the State of the Theory, formal architectural documents), primary source wins and this document revises.

**Maintenance discipline.** New entries added when a term is identified as quarantine-worthy through operations-log surfacing or cross-AI review. Existing entries amended when the rationale evolves. Drift-prone terms graduate to quarantine if recurrent use produces architectural confusion; the graduation is a Mike-arbitrated decision recorded in an operations log.

**Relationship to `standing_rules.md`.** Rule 5 (vocabulary quarantine enforced at wrap-ups and celebratory moments) is the enforcement standing rule; this document is the content the rule enforces against.

---

## Section 1: Prohibited terms (hard quarantine)

The following terms are prohibited across all layers, all artifacts entering the canonical record, and all conversational material that may be distilled into the canonical record. Rule 5 applies these prohibitions with extra care at wrap-ups, synthesis moments, and celebratory phrasing — where drift is most likely.

### Agent-behavioral vocabulary (excluded by the HARD CORE)

The theory's primitive observable is **ACTION**, not decision. The following terms are prohibited when describing agents or the structural bases.

- **"decision"** (when applied to agents). Agents do not decide to participate; they act or don't. The action stream is shaped by structural conditions (v, c, r) but agents have no decision function admitting structural conditions as input.
- **Any optimization language applied to agents.** No "maximizing," "minimizing," "optimizing," "selecting the best," etc. The theory excludes optimization frameworks by design.
- **Any utility language applied to agents.** No "utility," "preference," "valuation," "expected value," etc. Agents are not utility-bearing entities in this framework.
- **Any cognitive-response language applied to agents.** "Perceiving," "evaluating," "responding to" (in a cognitive sense), "interpreting" — all prohibited when describing how agents engage structural conditions. The structural-conditions-shape-action-streams relation is not cognitive.
- **"eligibility"** (gatekeeping connotation). The architecture has no gatekeeper — agents do not become "eligible" to participate; their action streams either project onto the bases or do not. Cleaner phrasing: "action streams that project onto the bases."

### Architectural-vocabulary drift (excluded by formal commitments)

- **"terrain favorability"** — drifts the structural bases (v, c, r) into a single composite property, collapsing the architecture's multi-base structure into a scalar field. The bases are independent by construction; "terrain favorability" reads them as components of a single quantity.
- **"viability-seeking"** — agent-teleological framing; agents do not seek viability or anything else. Cognitive-response vocabulary applied to agents.
- **"alignment"** (in the agent-behavioral sense). When used for agent behavior matching structural conditions, this is decision/cognitive vocabulary. The term is permitted in protocol-discussion contexts ("Layer 2's review aligned with Layer 1's framing") where it refers to AI/process alignment, not agent behavior.
- **"homeostatic imperative"** (as a formal primitive). May appear in informal discussion of biological analogy; never as a formal primitive of the theoretical architecture. The architecture's formal elements include ACTION as primitive observable, structural bases, activation drive, coherence, and the slow-timescale Q operator — homeostasis is not among them. (See Section 4 on source-domain scrubs for the Damasio lineage.)
- **"autocatalytic"** — implies chemical-reaction self-reinforcement that the architecture does not commit to. The architecture has feedback structure through Q, but Q is not autocatalytic; the term imports a mechanism the theory does not include.
- **"field"** (in the physics-borrowed sense). The theory uses Λ, ρ, Ψ as scalar quantities on a discrete substrate. "Field" suggests continuum-physics formalism that the theory does not adopt as architectural commitment. Lake Vision history aside, "field" in the architectural document is drift toward physics-borrowed framing.
- **"entrainment"** — coordination-dynamics vocabulary (Kelso, HKB). The theory's coordination structure differs from HKB in three architectural ways (two-stage cascade vs single bifurcation, supercritical pitchforks vs saddle-node-like switching, Q-mediated terrain reshaping vs fixed potential). Citing Kelso at the approach level is fine; using "entrainment" as architectural vocabulary imports the HKB mechanism into a framework that does not commit to it.
- **"fraction of the population"** — population-share framing that obscures the substrate-level dynamics. ρ is a substrate-aggregated activation density, not a fraction of an unmodeled population.

### Formal-primitive substitution

- **"ρ_c"** — risks hardening the second transition into a threshold-crossing model. The architecture's second transition is a sign-change in μ(ρ), governed by dΨ/dt = μ(ρ)Ψ − γΨ³, not a crossing of a critical density value. Permitted only inside explicit clarifications of why the term is prohibited.
- **"saddle"** — appears in v1.4 of the State of the Theory only in an exclusionary clause. Using "saddle" in architectural prose suggests saddle-node dynamics that the architecture excludes. Permitted only in exclusionary contexts citing the v1.4 commitment.

---

## Section 2: Permitted framings

The framings below replace prohibited terms in standard architectural prose. Examples are provided to make the substitution concrete.

### Candidate language for empirical claims

- **"Candidate produces / fails to produce"** — never "confirms" or "demonstrates." The theory is a candidate framework; empirical results produce or fail to produce predicted patterns. Confirmation language presupposes the framework's truth, which is not the discipline.

Example: "Reg_01 produced the identity-recovery pattern predicted by the substrate construction chain." Not: "Reg_01 confirms the substrate."

### Architectural positioning

- **"Architecture provides a location within which existing EE research is situated"** — never "supersedes" or "replaces." The architecture is a generative framework that situates field-observed phenomena within formal structure. Existing field work is not being replaced; it is being given a structural location.

Example: "The architecture situates Boulder Thesis observations within the structural-conditions-to-coherence cascade." Not: "The architecture supersedes the Boulder Thesis."

### Causal attribution

- **"μ(ρ) has composite causes; [mechanism] is one likely contributor among multiple, not the sole mechanism"** — used when attributing structural effects to specific mechanisms. Narrative compression, geography-as-compression-mechanism, etc., are contributors; none is the sole cause.

Example: "Narrative compression is one likely contributor to μ(ρ)'s sign-change behavior, alongside geography-as-compression-mechanism and other candidates not yet specified."

### Geography framing

- **"Geography is a compression mechanism producing co-location of structural conditions, not a boundary condition or formal space"** — geography enters the theory as a compression mechanism, not as a coordinate space or as a boundary defining the system. The architecture is substrate-based and discrete; geography compresses the substrate into spatial patterns.

---

## Section 3: Drift-prone vocabulary (caution flags, not prohibitions)

The terms below are not prohibited but are drift-prone. They have specific meanings within the protocol or theoretical architecture and can drift toward less precise readings if used carelessly. Use with care; surface ambiguity when it arises.

### "Solid" (three-tier commitment terminology)

Means *canonically acceptable under current evidence — ready for the canonical record absent outstanding flags.* Does not mean *epistemically closed* or *immune to correction.* A solid conclusion remains subject to revision if new primary source surfaces a conflict; Rule 1's primary-source override is not suspended by tier status.

Drift risk: "solid" reading as finality. Watch for it at celebration moments. Layer 2 flagged this term as drift-prone during the pair-1 protocol primer review (session 9); the clarification is now in `protocol_primer.md` Section 3 and reflected here.

### "Convergence" (synthesis-stage terminology)

Means *substantive engagement between Layer 1 and Layer 2 leading to a shared position grounded in evidence both layers engaged with.* Does not mean *agreement that emerged from one layer reading the other's framing.* The framing-asymmetry pattern (primer Section 4) makes refinement-driven convergence the structural default; substantive convergence is the exception that requires deliberate framing-room from Layer 1.

Drift risk: claiming "convergence" when the actual phenomenon is refinement-driven agreement. Rule 6 (no-preserved-divergence is a finding to track) is the corrective discipline.

### "Central node" (Layer 1 role terminology)

Means *Layer 1's coordinating/enforcement role across the protocol*; does not mean *Layer 1 is the privileged source of truth.* Primary source and Mike's arbitration remain above Layer 1. The role is process-coordinator, not epistemic-final-word.

Drift risk: "central node" reading as authority concentration. Watch for it when Layer 1 is producing synthesis documents that Mike will not independently verify against primary source.

### "Verification" (Rule 1 discipline terminology)

Means *primary-source check against the actual artifact (file, code, document, git log, parquet metadata).* Does not mean *memory description that sounds verified.* The distinction is the working-memory pattern's load-bearing line.

Drift risk: declaring "verified" when the verification was a working-memory consistency check rather than a primary-source touch. The discipline is: if Claude did not literally read the file/run the command/check the log, the claim is not verified.

### "Stage" (restructure-process terminology)

Means *one of the named stages of the repository restructure committed in session 6* (Stage 0 freeze and inventory, Stage 1 add orientation spine, Stage 2 move canonical artifacts, Stage 3 add manifests, Stage 4 quarantine stale material, Stage 5 resume analytical work). Does not mean *phase of work in a general sense*; "stage" as protocol vocabulary refers specifically to the committed sequence.

Drift risk: using "stage" loosely for any chunk of work, which obscures whether the discussion is about restructure stages or about something else. Use "phase," "step," or "cycle" for non-restructure work.

### "Open Element" (theoretical-architecture labeling)

Means *one of the four open elements of the committed architecture*: μ(ρ), F(v,c,r), Q, and the nucleation mechanism. Does not mean *any open theoretical question that could be assigned a number.* New "Open Element N" labels (where N is not one of the committed four) are vocabulary drift, not legitimate architectural commitments; numbering can falsely harden, reorder, or reify open theoretical commitments that have not been ratified.

Drift risk: a numeric Open Element label appearing in a routing artifact, operations log, or Layer 3 output, framed as if it were architectural commitment when it is local working vocabulary. Session 5 surfaced this pattern with "Open Element 14," which was quarantined and restated in committed vocabulary as "the architectural selection between F_LR and F_2_symmetric for the functional form of F(v,c,r)."

**Prior-cycle cross-reference (added session 10):** The "Open Element 14" label originates in pre-session-9 prior-cycle work. It appears in `protocols/onboarding/chatgpt_new_chat_primer.md` Section 8 as a real working label in canonical content from 15 May 2026. The label is preserved as historical canonical example of drift-prone vocabulary; the quarantine instructs that such non-canonical numeric labels be restated in committed terms when drafting new material. Session 5's quarantine work and session 9's discipline addition here are the corrective discipline against the original drift instance.

Discipline: if a numeric Open Element label appears that does not map to the committed four, quarantine the label, restate in committed terms (the architectural element being referred to), and surface to Mike. Restatement preserves the substantive question; quarantine prevents the numbering from becoming a parallel labeling system competing with the canonical four.

Future ratification: if Mike ratifies a new Open Element with formal architectural status, the State of the Theory document is amended accordingly and this entry updates. Casual numbering does not qualify.

---

## Section 4: Source-domain scrubs (historical record)

The architectural vocabulary in current canonical documents went through scrubs to remove source-domain language while preserving structural patterns. This section documents the scrubs as historical record. The principle: when borrowing structural patterns from a source domain, invoke the pattern without importing the source-domain vocabulary; source-domain language imports an ontology the theory may not commit to.

### Damasio biological language wrapper

Early project material engaged Damasio's biological framings (homeostatic regulation, somatic markers, etc.) as source language. Scrubbed early in the project's development. The current architecture's "homeostatic imperative" prohibition (Section 1) is the residue of that scrub. The structural patterns Damasio's framework gestured at (regulatory feedback, slow timescales for terrain modification) remain in the architecture under different vocabulary — Q's slow-timescale base evolution, structural conditions shaping action streams — but the biological source language does not enter the canonical record.

### Haken laser source

The architecture's order-parameter and bifurcation apparatus is structurally Haken's synergetics. Early material engaged Haken with the laser as canonical source domain (order parameter as laser amplitude, mean-field treatment, supercritical pitchfork at the lasing threshold). Scrubbed: invoke the structural pattern (order parameters, mean-field, supercritical pitchfork), not the laser as source. Current canonical work cites Haken at the *approach level* — structural framework — not as architectural analogue.

Citing Kelso (HKB coordination dynamics) follows the same discipline: approach-level only, not as architectural commitment. The "entrainment" entry in Section 1 documents this for the HKB case specifically.

### The scrub principle generalized

When borrowing a structural pattern from a source domain, the discipline is:
- Import the *structural* pattern (the equation form, the bifurcation topology, the order-parameter apparatus).
- Do not import the *source-domain* vocabulary (laser amplitude, somatic markers, coordination phase-locking, etc.).
- Cite the source at the approach level (Haken's framework, Damasio's framework, Kelso's framework) when the framework is doing structural work.
- Do not cite the source as architectural analogue when the architecture's actual elements (v, c, r, Λ, ρ, Ψ, Q) are doing the work.

For more on the theoretical context of these scrubs and their relation to the architectural framework, see `theoretical_context.md` Section 5.

---

## Section 5: Quarantine evolution

This document captures the state as of session 10. Items added or amended:

- **Layer 2 review surfaced "solid" as drift-prone (session 9 pair-1 review).** Added to Section 3.
- **"Central node," "convergence," "verification," "stage" added to Section 3** based on session 6-9 operational experience.
- **Per-term rationale added to Section 1** for future Claude instances who instantiate without prior operations logs in context.
- **"Open Element" labeling discipline added to Section 3 (session 9 pair-2 review).** Layer 2 surfaced the omission; the discipline captures the "Open Element 14" quarantine/restatement pattern from session 5 as protocol-level vocabulary discipline.
- **"Homeostatic imperative" rationale tightened (session 9 pair-2 review)** to name ACTION as primitive observable explicitly, preserving the hard-core statement.
- **"Eligibility" prohibition added to Section 1 (session 10, item 9 reconciliation).** Prior-cycle primer documents (`protocols/onboarding/chatgpt_new_chat_primer.md` Section 6 and `protocols/onboarding/gemini_new_chat_primer.md` Section 5) carry this prohibition; reconciliation work surfaced its absence from the session-9 canonical record.
- **Section 4 "Source-domain scrubs" added (session 10, item 9 reconciliation).** Damasio and Haken scrub history from prior-cycle primer documents incorporated into the canonical record.
- **"Open Element 14" prior-cycle cross-reference added to Section 3 (session 10, item 9 reconciliation).** The label's origin in pre-session-9 primer content documented as historical canonical example.

Future updates will be recorded here when committed.

---

— Drafted by Claude as Layer 1 central node, Stage 1 pair-2 of repository restructure, session 9. v2 incorporates Layer 2 review (Open Element discipline addition, "homeostatic imperative" rationale tightening). Section 1 "eligibility" entry, Section 3 prior-cycle cross-reference, Section 4 source-domain scrubs, and Section 5 maintenance log entries added session 10 as deliverable 3 of item 9 reconciliation, integrating prior-cycle vocabulary content into the canonical record. Pending Layer 2 sanity scan before commit.



---
# FILE: C:\Users\vkz244\Downloads\canonical_artifacts_index.md
---

# Canonical Artifacts Index

**Document role.** Authoritative index of the canonical artifacts that constitute the EE Theory Lab record. For each artifact, the index specifies: what it is, where it lives, and what authority it carries. This is the document a fresh Claude instance consults to locate primary source for any verification under Rule 1.

**Authority.** This document is authoritative for *where* canonical artifacts live and *what authority* they carry. It is not authoritative for the artifacts' content; each artifact is its own authority on its content domain. When this index conflicts with primary source (the actual files at the stated paths), primary source wins and this document revises.

**Maintenance discipline.** Updated when canonical artifacts are added, moved, or superseded. Updates committed alongside the operations log of the session in which the change occurred. Stage 2 of the repository restructure (moves canonical artifacts via `git mv`) will trigger a coordinated update of this index.

**Path conventions.** All paths relative to `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` unless absolute. PowerShell uses backslash separators; git status output uses forward slashes; both refer to the same files.

**Relationship to other foundational documents.**
- `protocol_primer.md` specifies who uses these artifacts and how.
- `standing_rules.md` specifies the disciplines (especially Rule 1) under which artifacts are consulted.
- `vocabulary_quarantine.md` specifies the language used when discussing the artifacts.
- `current_state.md` tracks session-volatile state; `theoretical_context.md` tracks stable theoretical/historical content; `environment_reference.md` tracks operational/environmental detail; `personal_context.md` tracks personal-context discipline.

---

## Section 1: Theory-level documents

### State of the Theory v1.1

The committed theoretical architecture; ten sections; "hard core." Authority: formal theoretical commitments. Defines the four open elements (μ(ρ), F(v,c,r), Q, nucleation mechanism), the two-stage Landau cascade structure, the critical ontological constraint (ACTION not decision), and the architecture's exclusionary clauses.

**Path:** Mike's local file (not in the repository's tracked tree as of session 10).

**Operational locatability:** requires Mike-provided attachment for any verification-against-primary-source check. Stage 2 will move this to `theory\state_of_theory\state_of_theory_v1_1.md` per session 6's v1.1 naming-collision resolution; until then, Layer 1 cannot verify content claims about this document without explicit Mike-provided access.

**Citation:** "State of the Theory v1.1." Do not cite "v1.1" alone without qualifier — multiple v1.1 documents exist (see naming-collision note below).

### State of the Theory v1.5 Overview

Manuscript foundation Phil writes from; v1.4 MFA underneath. Authority: manuscript-facing material. The leading edge of the team's worked-out positions has moved past v1.5 in places (e.g., the flagged "modest-resources-outperform-abundant" passage); v1.5 absorbs back-flow from those developments as Phil revises.

**Path:** Mike's local file (not in the repository's tracked tree as of session 10).

**Operational locatability:** requires Mike-provided attachment for verification. No committed Stage 2 target yet; the v1.5 Overview's repository placement is a question for Mike to arbitrate when manuscript work surfaces a need.

**Citation:** "State of the Theory v1.5 Overview" or "v1.5 Overview" with context.

---

## Section 2: Phase 4B specifications

### Phase 4B Specification v1.1

Analytical procedures for Phase 4B: Tier 1 strict matching, Tier 2 coarser matching, Tier 3 interpretable regression with pre-specified interaction families, two-field empirical_result × structural_status classification, cross-scale analysis. Authority: Phase 4B analytical procedures.

**Path:** `phase_4b\phase_4b_specification_v1.1.md`

**Verified:** session 9.

**Citation:** "Phase 4B Specification v1.1."

### Flight 6 Substrate Specification v1.1

Substrate implementation: the cellular engine that produces .parquet telemetry. Sections 6 and 8 specify the deterministic probability chain (Drive_Raw → p_base → p_act → realization) that reg_01 recovered. Section 13.2 specifies the shadow-copy structure (F_2_symmetric runs at each scale produce one underlying parquet file, three probe-named files via byte-identical shadow copies; F_LR runs produce one parquet file each). Section 15 enumerates implementation prohibitions; the protocol-applicable subset is lifted to `standing_rules.md` Rule 7.

Authority: substrate implementation.

**Path:** `flights\flight_6\Flight6_Substrate_Specification_v1.1.md.pdf`

**Verified:** session 6 (located and read end-to-end), session 9 (path re-verified, Section 15 re-verified against primary source).

**Citation:** "Flight 6 Substrate Specification v1.1" or "FSS v1.1" with context.

---

## Section 3: Tier 3 canonical implementation

The Tier 3 implementation cluster committed at `3189ab7` (session 7 reconciliation). All paths under `phase_4b\scripts\`.

### Intake module

Implements the seven-item structural-correctness checklist per intake specification. Defines `NormalizedPrereg` dataclass, the schema validator, and the `attach_tier2_globals` merge function.

**Path:** `phase_4b\scripts\_phase_4b_intake.py`

**Commit:** introduced at `3189ab7`.

### Test suite

Demonstrates all five exception types fire on deliberate violations. Routes inputs through the actual validation pipeline (not via mock objects per Rule 7.2).

**Path:** `phase_4b\scripts\test_intake.py`

**Commit:** introduced at `3189ab7`.

### Refactored regression consumer

Contract-mediated per intake §1.6. Reads pre-registration yaml, normalizes via the intake module, attaches Tier 2 globals, executes the regression, writes outputs.

**Path:** `phase_4b\scripts\tier3_regression.py`

**Commit:** introduced at `3189ab7`.

---

## Section 4: reg_01 pre-registration and outputs

The committed reg_01 cluster. Pre-registration and outputs committed at `3189ab7`. The pre-registration's `interpretation_boundary` content was restored from session 5's log to the canonical yaml during session 7's reconciliation.

### Pre-registration

Schema is contract-mediated intake format. `derived_variables` block declares per-run/tick constructions for `Local_Density_squared`, `rho_global`, `psi_global`. `interpretation_boundary.licenses` list (5 items) and `does_not_adjudicate` (4 items) restored under new schema; substantive scope matches session 5's log.

**Path:** `phase_4b\pre_registrations\reg_01_scale_interactions.yaml`

**Commit:** `3189ab7`.

### Primary coefficients

**Path:** `phase_4b\tier3_outputs\coefs_reg_01_scale_interactions.csv`

**Commit:** `3189ab7`.

### Sensitivity coefficients

**Path:** `phase_4b\tier3_outputs\coefs_reg_01_scale_interactions_sensitivity_cell.csv`

**Commit:** `3189ab7`.

### Regression report

**Path:** `phase_4b\tier3_outputs\report_reg_01_scale_interactions.md`

**Commit:** `3189ab7`.

**Note:** the `tier3_outputs/` directory is at `phase_4b\tier3_outputs\` (sibling of `scripts/`), NOT `phase_4b\scripts\tier3_outputs\`. The kit-revision-1 had this wrong; corrected in kit-revision-2 and verified during session 7.

---

## Section 5: Substrate data and Tier 2 derived outputs

### Canonical substrate data

Eight Flight 6 production parquet files (Flight 2 naming inheritance preserved). Four genuine substrate runs plus four byte-identical shadow copies per Flight 6 Substrate Specification §13.2. PRNG_seed 128561948, substrate_version v1.1.

**Path (absolute):** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\`

**Note on naming:** the directory is named `flight2_outputs` for inheritance reasons, but contains Flight 6 files. The mismatch is documented at the canonical record level (here) and will be resolved during Stage 4 (quarantine and rename).

### Tier 2 derived outputs

65 files. Per-probe-scale derived outputs (8 metric types × 8 probe-scale combinations = 64 files) plus the merged `global_timeseries.csv` bridging artifact (13.5MB, the canonical Tier 2 → Tier 3 join surface produced by `merge_globals.py`; status confirmed canonical during session 8's Stage 0 inventory).

**Path:** `phase_4b\tier2_outputs\`

### Tier 1 reports

Eight Tier 1 reports across the four-probe × two-scale matrix.

**Path:** `phase_4b\tier1_reports\`

### Cross-run analysis outputs

Three cross-run analysis files dated 5/17/2026 morning.

**Path:** `phase_4b\cross_run_outputs\`

**Stage 0 status:** these three directories (`tier2_outputs/`, `tier1_reports/`, `cross_run_outputs/`) are categorized as canonical in `RESTRUCTURE_INVENTORY.md` (committed at `1a68ca6`); Stage 2 will execute `git mv` placement per the inventory's moves-plan.

---

## Section 6: Diagnostic and forensic-text outputs

Per the Stage 0 canonical diagnostics directory convention (adopted session 8), all diagnostic stdout, log, and forensic-text outputs go under `phase_4b/diagnostics/`. Stage 2 will execute the moves; current locations as committed in `RESTRUCTURE_INVENTORY.md`:

### Session 5 diagnostic stdout

**Path:** `phase_4b\diagnostic_stdout.txt`

**Note:** at `phase_4b\` (sibling of `scripts\`), NOT `phase_4b\scripts\diagnostic_stdout.txt`. The kit-revision-1 had this wrong; corrected in kit-revision-2.

### Session 6 t27 forensic output

**Path:** `phase_4b\t27_diagnostic_stdout.txt`

### Earlier cross-run comparison output

**Path:** `cross_run_comparisons_df9122e.txt` (workspace root, awaiting Stage 2 move to `phase_4b/diagnostics/`)

---

## Section 7: Operations logs and routing artifacts

### Operations logs

All committed. Paths under `operations_log\`. The directory has a `README.md` documenting filename conventions, authorship, the honest-record principle, and pointers to the current standing-rules location.

**Authority:** Canonical historical record of session-by-session decisions, gate closures, discipline events, and protocol additions. Per the README's honest-record principle, entries are not retroactively edited; later entries that correct earlier ones preserve both.

The directory spans prior-cycle work (May 14-19 entries documenting Cycle 2 Round 1 work) and current Phase 4B work (sessions 2-onward).

| Session/event | Path | Commit |
|---------------|------|--------|
| Prior-cycle work (May 14-19) | `operations_log\2026-05-14_*` through `operations_log\2026-05-19_*` (16 entries) | various commits up to `5d91828` |
| 5 | `operations_log\2026-05-18_phase_4b_session_5.md` | `3189ab7` |
| 6 | `operations_log\2026-05-19_phase_4b_session_6.md` | `3189ab7` |
| 7 | `operations_log\2026-05-19_phase_4b_session_7.md` | `4e66f27` |
| 8 | `operations_log\2026-05-19_phase_4b_session_8.md` | `3e38980` |
| 9 | `operations_log\2026-05-20_phase_4b_session_9.md` | `ff2704d` (original log), addendum at `53aa62e`, date-revert at `5f5a762` |
| 10 (pending) | (drafted at session-end) | (pending commit) |

### Architectural reviews

Five Layer 1 architectural review documents from May 14-15 2026, covering A3 parity code, Flight 1 v1.1 implementation, v1.1/A3 divergence, Flight 2 analysis script, and Flight 2 substrate.

**Path:** `protocols\architectural_reviews\`

**Authority:** Canonical historical record of Layer 1 review outputs, parallel to operations logs. Each review documents what was checked, what passed, what was deferred or flagged. The directory has a `README.md` documenting its role.

The directory is open for new entries (Layer 1 architectural reviews of future substrate/analysis code).

**Verified:** session 10 (item 9 reconciliation, primary-source read of all five reviews).

### Routing artifacts

**Layer 1 routing package (session 5).** The `LAYER_1_ROUTING_PACKAGE.txt` file at workspace root is a canonical-record candidate (from session 5's Layer 2 routing on reg_01 interpretation). Stage 2 will place it under an appropriate routing-archive path per `RESTRUCTURE_INVENTORY.md`.

**Stage 1 routing packages (session 9).** `LAYER_2_ROUTING_STAGE1_PAIR1.md`, `LAYER_2_ROUTING_STAGE1_PAIR1_V2_ACCEPTANCE.md`, and the other Stage 1 routing artifacts at workspace root. Stage 2 will move these to a routing-archive path alongside the session 5 routing package.

---

## Section 8: Stage 0 inventory and restructure planning

### RESTRUCTURE_INVENTORY.md

The Stage 0 deliverable. Categorizes the 31 untracked items as of session 8 inventory time into canonical (74 files counting subdirectory contents, including the two reclassified-canonical scripts `inspect_tier3_provenance.py` and `merge_globals.py`) and scratch (22 scripts at workspace root). Includes Stage 2 moves-plan, four open items for subsequent stages, and verification section recording both Layer 1 cross-check and Layer 2 sanity scan.

**Path:** `RESTRUCTURE_INVENTORY.md` (workspace root)

**Commit:** `1a68ca6`.

### PRIOR_CYCLE_INVENTORY.md and PRIOR_CYCLE_RECONCILIATION_PLAN.md

One-time task-shaped artifacts produced as deliverables 1 and 2 of STANDING_ITEMS item 9 (prior-cycle canonical material reconciliation). Workspace root placement parallels `RESTRUCTURE_INVENTORY.md`. Finite life — close out when reconciliation completes (this commit).

**Paths:** `PRIOR_CYCLE_INVENTORY.md`, `PRIOR_CYCLE_RECONCILIATION_PLAN.md` (workspace root)

**Commits:** session 10 reconciliation commit cluster.

---

## Section 9: Foundational document set

The current document plus its peers in `protocols/foundational/`. Stage 1 documents committed during session 9; session 10 adds three new documents and updates several existing ones as part of item 9 reconciliation.

| Document | Path | Status |
|----------|------|--------|
| Protocol primer | `protocols\foundational\protocol_primer.md` | committed `79db966` (session 9 pair 1) |
| Standing rules | `protocols\foundational\standing_rules.md` | committed `79db966` (session 9 pair 1); historical lineage section added session 10 |
| Vocabulary quarantine | `protocols\foundational\vocabulary_quarantine.md` | committed `6603799` (session 9 pair 2); eligibility prohibition, source-domain scrubs section, and Open Element 14 cross-reference added session 10 |
| Canonical artifacts index | `protocols\foundational\canonical_artifacts_index.md` | committed `6603799` (session 9 pair 2); updated session 10 to reflect new directories and foundational documents |
| Current state | `protocols\foundational\current_state.md` | committed `a8bc52c` (session 9 pair 3); Stage-1-complete framing updated session 10 |
| README | `protocols\foundational\README.md` | committed `a8bc52c` (session 9 pair 3) |
| Theoretical context | `protocols\foundational\theoretical_context.md` | new, committed session 10 (item 9 reconciliation) |
| Personal context | `protocols\foundational\personal_context.md` | new, committed session 10 (item 9 reconciliation) |
| Environment reference | `protocols\foundational\environment_reference.md` | new, committed session 10 (item 9 reconciliation) |

Root-level orientation documents (`ORIENTATION.md`, `CURRENT_STATE.md`, `MANIFEST.md`) and `STANDING_ITEMS.md` were committed during session 9 Stage 1 work.

### Foundational document role distinctions (added session 10)

The foundational set decomposes by what each document tracks:

- **Stable theoretical/historical content:** `theoretical_context.md` (Two-paper structure, Four Grand Challenges, Cycle 1/Cycle 2 framework, A3 reference baseline, vocabulary scrub history).
- **Stable operational/environmental content:** `environment_reference.md` (workspace, Python environment, dependencies, PowerShell hazards, tools).
- **Stable personal-context discipline:** `personal_context.md` (Mike's intellectual lineage, contemplative practice, Mokie; discipline of not raising unprompted).
- **Stable protocol content:** `protocol_primer.md`, `standing_rules.md`, `vocabulary_quarantine.md`.
- **Index over stable content:** `canonical_artifacts_index.md` (this document).
- **Session-volatile state:** `current_state.md` (current phase, latest finding, open items, next anticipated work, working pattern, protocol state).

---

## Section 10: Prior-cycle canonical material (added session 10)

This section indexes the directories containing prior-cycle (pre-session-9) canonical material that the session-9 foundational set did not initially engage. Item 9 reconciliation (session 10) inventoried these and made determinations about each; full inventory at `PRIOR_CYCLE_INVENTORY.md`, reconciliation plan at `PRIOR_CYCLE_RECONCILIATION_PLAN.md`.

### protocols\onboarding\

Four prior-cycle primer documents drafted 15 May 2026 for fresh AI partner instantiation: `new_chat_primer.md`, `chatgpt_new_chat_primer.md`, `gemini_new_chat_primer.md`, `chatgpt_routing_note.md`.

**Status:** Superseded by `protocols/foundational/` plus the instantiation kit as cold-start primer surface. The directory has a `README.md` (added session 10) documenting the supersession and explaining what carry-forward content moved where in the session-10 reconciliation.

**Path:** `protocols\onboarding\`

### protocols\architectural_reviews\

See Section 7 above. Architectural review outputs preserved as historical canonical record.

### operations_log\

See Section 7 above. Prior-cycle operations logs (May 14-19) preserved per the honest-record principle.

---

## Section 11: Instantiation kit

The compressed instantiation surface for fresh Claude chats. Becomes a derived/compressed surface over the foundational document set as Stage 1 completes; not authoritative on its own once Stage 1 is committed.

**Current revision:** kit-revision-3 (drafted at session 9 end). Kit-revision-4 is anticipated for post-item-9 closure work, incorporating: the "path-space land grab" framing into Rule 7.4 territory; the "any copy-target, not just PS" principle; the "informational content does not need a copy-pane" principle; the v1_1_divergence_review footnote as discipline precedent.

**Path:** typically delivered as a session-handoff artifact under `claude_session_handoffs\YYYY-MM-DD[-N]\` rather than committed to the repository tree. Whether the kit lives at a stable repository path or remains a handoff artifact is a question carrying forward from session 9's pending decisions.

---

## Section 12: Naming-collision and citation discipline

Three documents share the "v1.1" designation:

1. State of the Theory v1.1 (theoretical architecture)
2. Phase 4B Specification v1.1 (analytical procedures)
3. Flight 6 Substrate Specification v1.1 (substrate implementation)

**Citation rule:** Do not cite "v1.1" alone without a qualified document path or full document name. In code comments, citations like `# per v1.1 Section 13.2` are ambiguous; use `# per FSS v1.1 Section 13.2` or `# per Flight 6 Substrate Specification v1.1 §13.2`.

**The post-Stage-2 path commitment:** the three v1.1 documents will live at:

- `theory\state_of_theory\state_of_theory_v1_1.md`
- `phase_4b\specifications\phase_4b_specification_v1_1.md`
- `substrate\flight6_v1_1\specifications\flight6_substrate_specification_v1_1.md`

These are the targets; Stage 2 executes the moves. This document updates accordingly when Stage 2 commits.

---

## Section 13: Workspace and tools

Detailed operational reference for the production environment is in `protocols/foundational/environment_reference.md`. The summary below is for quick lookup.

### Canonical workspace

**Path:** `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` (lowercase nested).

### Stale parallel tree

**Path:** `C:\Users\vkz244\EE_Theory_Lab\phase_4B\` (capital B at top level). To be archived during Stage 4.

### Canonical data outputs

**Path:** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` (absolute; named for inheritance reasons, contains Flight 6 files; Stage 4 will resolve the naming).

### Tools

- **Mesa 3.x + SolaraViz** — ABM substrate environment.
- **VS Code** — text editor, pure-editor mode (AI-agent features unused per protocol convention).
- **PowerShell** — Windows shell. Note: `git --no-pager <command>` bypasses the pager when long output is expected; `q` exits the pager interactively.
- **Node.js / docx npm package** — Word document generation (used selectively for Phil-facing artifacts).
- **ReportLab** — PDF transcripts.
- **Python + NumPy** — analytical work, Tier 3 regression execution.

For Python version, dependency versions, and PowerShell hazards (Notepad UTF-8 BOM, paste-back failure modes, etc.), see `environment_reference.md`.

---

— Drafted by Claude as Layer 1 central node, Stage 1 pair-2 of repository restructure, session 9. v2 incorporates Layer 2 review (operational locatability notes added for Mike-local theory files). Section 9 updated, Section 10 added, Section 11 updated for kit-revision-4 anticipation, Section 13 condensed with cross-reference to `environment_reference.md`, all session 10 as deliverable 3 of item 9 reconciliation. Pending Layer 2 sanity scan before commit.



---
# FILE: C:\Users\vkz244\Downloads\current_state.md
---

# Current State

**Document role.** Snapshot of the EE Theory Lab's current phase, latest substantive findings, open items, and next anticipated work. This is the document a fresh Claude instance consults to answer "where are we now?"

**Authority.** This document is authoritative for current-state orientation. When it conflicts with primary source (committed code, operations logs, the actual repository state), primary source wins and this document revises. Per Rule 1, current-state claims should be verified against `git log --oneline` and operational reality before being treated as load-bearing.

**Maintenance discipline.** Updated at session end. Volatile sections (those marked **As of session N**) are rewritten each session; stable structural content (the section headings, what each section tracks) changes only when the protocol's understanding of what's worth tracking evolves.

**Relationship to root-level `CURRENT_STATE.md`.** This document is the foundational-set version, scoped to load-bearing protocol-state material for AI instances and Mike. The root-level `CURRENT_STATE.md` is a higher-level orientation derivative aimed at the same audience but with broader scope (project-level state including manuscript-side context that is not strictly Phase 4B work).

**Relationship to other foundational documents.** This document tracks session-volatile state. For stable theoretical and historical content (Two-paper structure, Four Grand Challenges, Cycle 1/Cycle 2 framework, A3 reference baseline), see `theoretical_context.md`. For operational/environmental detail (workspace paths, Python environment, dependencies, PowerShell hazards), see `environment_reference.md`. For personal-context discipline, see `personal_context.md`. The foundational set's role distinctions are documented at `canonical_artifacts_index.md` Section 9.

---

## Section 1: Current phase

**As of session 10 (2026-05-20):**

The project is in the middle of a multi-stage repository restructure, committed across sessions 6-8 of Phase 4B. Stage 0 (freeze and inventory) was committed at `1a68ca6` during session 8. Stage 1 (add orientation spine — the foundational document set, root-level orientation documents, kit revision) was substantively completed in session 9 with the foundational set, root-level orientation, STANDING_ITEMS.md, and kit-revision-3 committed. Stage 1 closed in session 10 *after the prior-cycle reconciliation* (item 9 of STANDING_ITEMS), which surfaced pre-existing canonical material at `protocols/onboarding/`, `protocols/architectural_reviews/`, and `operations_log/` that the session-9 foundational set had not initially engaged.

**Stage 1 status: Complete after reconciliation.** The session-9 closing framing of "Stage 1 substantively complete" is corrected to "Stage 1 substantively complete *after the discovered reconciliation requirement*." The reconciliation work fired in session 10 per item 9's structural trigger.

Stage sequence (committed session 6):

- **Stage 0** — Freeze and inventory. **Committed at `1a68ca6`.**
- **Stage 1** — Add orientation spine. **Complete after reconciliation (sessions 9-10).**
- **Stage 2** — Move unambiguous canonical artifacts via `git mv`. **Next.**
- **Stage 3** — Add manifests, especially for parquet outputs and substrate files.
- **Stage 4** — Quarantine stale and scratch material.
- **Stage 5** — Resume Phase 4B analytical work.

---

## Section 2: Latest substantive finding

**As of session 10 (2026-05-20):**

The most recent substantive analytical finding is from session 6: Tier 3 reg_01 is substantively complete as a pipeline-validation regression, with the R²=1.000 identity-recovery interpretation verified by primary-source review of the Flight 6 Substrate Specification v1.1 sections 6 and 8. The substrate's deterministic probability chain (Drive_Raw → p_base → p_act → realization) is what reg_01 recovered at machine precision; F_variant and scale enter only indirectly through Term_Lambda.

The reg_01 finding does not adjudicate the architectural selection between F_LR and F_2_symmetric for the functional form of F(v,c,r). F-form adjudication routes to macro-level analyses for the next analytical phase: aggregate trajectory comparisons, Ψ-structure analysis, Q-driven base drift, regime-transition timing, repeat-seed designs.

No analytical work has happened since session 6. Sessions 7-10 have been protocol infrastructure (reconciliation, Stage 0 inventory, Stage 1 foundational set drafting and prior-cycle reconciliation).

---

## Section 3: Open items

**As of session 10 (2026-05-20):**

### Post-Stage-1 standing items (now eligible after item 9 closes)

- **Pre-registration reproducibility verification.** Re-run `tier3_regression.py` against the committed yaml at `3189ab7`; diff outputs against committed reg_01 outputs. Eligible to fire as the first substantive action of session 11 (or later session 10 work if context budget permits).
- **Push to origin.** Local main is multiple commits ahead of origin/main after the session-10 reconciliation commit cluster. Eligible to fire post-cluster.

### Post-restructure standing items

- **Next analytical phase decision.** Which macro-level F-form adjudication route becomes the next pre-registered work. Mike arbitrates. Deferred until restructure complete enough to support analytical work.

### Cross-session items

- **Manuscript implications.** Phil's manuscript work is independent of Phase 4B's analytical phase. Whether and when the reg_01 finding lands in the v1.5 Overview is Phil's call. No action item from the protocol side.
- **F multiplicativity commitment verification.** Independent trigger (v1.5 Overview revision work surfaces). See `STANDING_ITEMS.md`.
- **Foundational set maintenance.** Each session-end checks for kit-revision triggers (working-pattern changes, current-state changes, canonical-artifacts changes). Rule 2 specifies the discipline.
- **Kit-revision-4.** Anticipated post-item-9 closure work. See `STANDING_ITEMS.md` and `canonical_artifacts_index.md` Section 11 for the items kit-revision-4 incorporates.
- **ChatGPT and Gemini onboarding under session-9 framework.** The session-9 foundational set is Claude-focused; ChatGPT and Gemini onboarding under the current framework was deferred during item 9 reconciliation. See `STANDING_ITEMS.md` for the open item.

All active deferred items live in `STANDING_ITEMS.md` with explicit trigger conditions and acceptance criteria.

---

## Section 4: Next anticipated work

**As of session 10 (2026-05-20):**

Within this session (session 10):

- Item 9 reconciliation: three deliverables (inventory, plan, canonical record update). Inventory and plan committed. Canonical record update commit cluster is the final session-10 substantive work item.
- Layer 2 sanity scan of the deliverable-3 file set per the foundational-set discipline.
- Session 10 operations log.
- Session 11 handoff folder.

Next session (session 11):

- Pre-registration reproducibility verification (per STANDING_ITEMS item 1).
- Push to origin (per STANDING_ITEMS item 2).
- Stage 2 execution: `git mv` operations per `RESTRUCTURE_INVENTORY.md` moves-plan.

Several sessions out:

- Stages 3-4 (manifests; quarantine).
- Stage 5 resumption: next analytical phase decision and pre-registration.
- ABM probe execution by Layer 3 (Gemini) once probe is specified.
- Substantive results analysis with Layer 2 (ChatGPT), likely from a fresh Claude session that has the committed substrate and analytical outputs as primary source.

---

## Section 5: Working-pattern state

**As of session 10 (2026-05-20):**

Working pattern committed in the kit as of kit-revision-3, with additions surfaced during session 10 that fold into kit-revision-4. Operational pattern:

- PowerShell commands delivered one per fenced block; Mike pastes one-click, runs, pastes output back.
- One-click copy panes used only for content Mike will act on (PS commands, messages to other AIs, file content for placement). Informational content (status summaries, file lists, instructions about what to do next) goes in plain text.
- Visual demarcation after PS output: horizontal rule + bold "Response to your output:" label.
- File edits delivered as full-file overwrites; Mike downloads, moves into workspace via PS.
- File-system manipulation defaults to PowerShell (not File Explorer drag).
- Multi-file `present_files` delivery: Mike prefers separate-file downloads; Claude makes separate `present_files` calls.
- For substantial multi-file reads, concatenation-via-PowerShell into a single bundle file for one upload is preferred to many separate uploads.
- Session-handoff folder: `claude_session_handoffs/YYYY-MM-DD[-N]/` contains the kit and the just-closed session's operations log.
- Opening instruction to next-session Claude is a single sentence pointing at the kit; substantive operational knowledge belongs inside the kit.
- Session-open verification (added session 10): `git ls-tree HEAD -- <relevant directories>` for any directory where session work will produce new canonical material, regardless of whether the directory appears in the prior session's resume anchor. Path-space land-grab discipline.

---

## Section 6: Protocol state

**As of session 10 (2026-05-20):**

- HEAD: `5f5a762` (session 9 date-revert commit) at session 10 open; advances through the session-10 reconciliation commit cluster.
- Layer assignments: Claude = Layer 1 (central node), ChatGPT = Layer 2 (substantive review), Gemini = Layer 3 (implementation/execution). Mike arbitrates.
- Foundational document set: pairs 1-3 committed during session 9; three new documents (`theoretical_context.md`, `personal_context.md`, `environment_reference.md`) and updates to existing documents committed during session 10 as part of item 9 reconciliation.
- Instantiation kit: kit-revision-3 (drafted at session 9 end). Kit-revision-4 anticipated post-item-9 closure.
- Routing convention: full Layer 2 cycle for protocol-infrastructure routings includes v2-acceptance pass before commit (per `protocol_primer.md` Section 3); other full-cycle routings commit after Layer 1 incorporation. Session 10 deliverable 3 routes for Layer 2 sanity scan per the discipline-distribution convention (substantive foundational updates get Layer 2 review, but not full v2-acceptance cycle).

---

## Section 7: How to update this document at session end

The volatile sections are 1-6 above. Each session-end update should:

1. Update **Section 1** if the current phase has changed (a stage closed or opened).
2. Update **Section 2** if a new substantive finding has landed in the canonical record.
3. Update **Section 3** by removing resolved open items, adding new ones, and updating session-numbered triggers and acceptance criteria where relevant.
4. Update **Section 4** to reflect new next-anticipated work.
5. Update **Section 5** if the working pattern has evolved (new conventions, retired conventions).
6. Update **Section 6** with new HEAD, new commits ahead of origin, new kit revision number, etc.

The **As of session N** marker at the top of each volatile section gets the new session number. The structural content (section headings, what each section tracks) is stable and changes only when the protocol's tracking discipline evolves.

---

— Drafted by Claude as Layer 1 central node, Stage 1 pair-3 of repository restructure, session 9. v2 incorporates Layer 2 review (Open Element 14 label removed and restated in committed terms; completed Section 15 lift item removed from open items; "confirmed" replaced with "verified by primary-source review"). Stage-1 framing updated, cross-references to new foundational documents added, session 10 substantive work reflected, session 10 as deliverable 3 of item 9 reconciliation. Pending Layer 2 sanity scan before commit.



---
# STILL NEEDED FROM CLAUDE
---

operations_log\README.md � updated deliverable-3 version
protocols\onboarding\README.md
protocols\architectural_reviews\README.md
