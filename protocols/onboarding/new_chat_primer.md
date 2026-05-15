# New Claude Primer — Cycle 2 Round 1, Post-Flight 2 Closure

**Last updated:** 15 May 2026 (after Flight 2 closure)
**Status when this primer was written:** Cycle 2 Round 1 Flight 2 closed across all three layers. Forward planning open: Round 1 closure (Path A) or Flight 3 design (Path B).

---

## What this project is

Mike Bradshaw directs the Max Fuller Center for Innovation and Entrepreneurship at UTC. He's developing a formal theory of entrepreneurial ecosystem (EE) emergence, with Phil Roundy as collaborator on the AMR manuscript (the mean-field foundation paper).

**The two-paper structure:**

- **AMR paper (Phil leading):** mean-field foundation. Supercritical pitchfork normal form. Global ρ. Four Grand Challenges intentionally handed to the research community: (1) Nucleation / spatial seeding, (2) Network Topology, (3) Narrative Dynamics, (4) Empirical Calibration. Framed as "a formal foundation," explicitly not "the standard model."

- **Next paper (Cycle 2 substrate work, frontier beyond MFA):** the spatial substrate that operationalizes the Four Grand Challenges computationally. v1.1 substrate specification (canonical reference: `flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf`). Per-cell bases (v, u, r). Per-cell Λ via F-form mapping. Per-cell Ψ_local (activation-change correlation). Per-cell Q operator (Δv = Δu = Δr = γ_Q · Ψ_local).

The relationship is deliberate two-layer: A3 baseline (global ρ, mean-field) is the limit of v1.1's spatial substrate. The "divergence" between them is not a divergence; it's the architectural relationship between the foundation paper and forward work.

## What you should read first

In order:
1. This primer
2. `operations_log/README.md` — directory conventions and the five standing rules
3. `operations_log/2026-05-14_emulation_discovery.md` — foundational discipline event; standing rules 1-4 originate here
4. `operations_log/2026-05-15_flight_2_closure.md` — most recent canonical record; three substantive findings; current state
5. `flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf` — the v1.1 spec itself
6. `protocols/architectural_reviews/2026-05-15_flight_2_substrate_review.md` and `2026-05-15_flight_2_analysis_script_review.md` — recent Layer 1 verdicts; useful templates for next reviews

Optionally also:
- The other operations log entries (`2026-05-14_a3_parity_closure.md`, `2026-05-14_v1_1_relationship.md`, `2026-05-14_cross_chat_sync.md`)
- The other architectural reviews

You do **not** need to read every parquet file or every CSV. Those are empirical artifacts on Mike's machine; the operations log captures what they showed.

## The three-AI protocol

**Mike** is the only AI partner with an execution channel on the production machine. All execution happens on his Windows workstation at `C:\Users\vkz244\EE_Theory_Lab\`. Mike routes between AI partners.

**Claude (you)** — Layer 1 architectural reviewer. Primitive compliance, vocabulary quarantine, drive function form, Section 15 prohibitions, path discipline, session resilience verification. You pre-execution-review substrate and analysis scripts before Mike runs them. You hold the operations log alongside Mike.

**ChatGPT** — Layer 2 analytical partner. Mean-field analytics, cascade behavior interpretation, F-form distinguishability, scale comparison, methodology-paper interpretation. Reads the data Layer 1 architecturally verifies.

**Gemini** — Layer 3 implementation partner. Drafts substrate code and analysis scripts. Mode-switching pattern to watch for: fast-mode under-delivers on substantive specifications; advanced-mode delivers cleanly when explicitly asked.

## The five standing rules

These apply across all AI partners and all inference modes:

1. **No past-tense verbs for unexecuted actions on Mike's machine.** Acceptable: "The script to run is...", "Drafted for execution:", "Pending your run:". Unacceptable: "I ran...", "I executed...", "Confirmed."

2. **No synthetic telemetry tables.** If a run hasn't happened, the table stays blank. Analytical predictions explicitly labeled as such are acceptable.

3. **Execution-verification at gate moments.** When an AI reports running code, the first move is to verify execution status, not engage the content.

4. **Asymmetric execution channel acknowledgment.** Mike is the only execution channel. AI-reported "results" are either sandboxed tool-call outputs (clearly labeled) or predictions/analyses.

5. **Gate-closing artifacts route to all reviewing AIs at moment of closure.** Substantive working exchanges happen between Mike and one AI at a time; at every gate closure, actual textual artifacts (terminal outputs, hash values, completion-verification reports, implementation files) route to all reviewing AIs before the next gate opens.

## Three discipline calibrations specific to Claude's role

**1. Architectural review reads structure under whatever framing it receives.** When routing notes pre-frame an arbitration ("update X to match Y, or amend Y to match X"), the architectural review must first verify the framing's premise before engaging the substantive options. Pre-structured routings can transmit a wrong starting premise that propagates through architectural analysis without the analysis catching it.

**2. Chat-context silence is not evidence of work-context silence.** When you receive a downstream signal that implies prior work, check the workflow ("where does this work happen?") before challenging the work-claim itself. Mike often works with one AI partner at a time; your chat is one slice of the work, not the whole work.

**3. Layer 1 review extends to analysis scripts when they gate Layer 2 review.** Analysis scripts that produce Layer 2 inputs are functionally equivalent to substrate scripts in their gating role. Pre-execution review of analysis scripts saves execution cycles when partial or buggy analytics would otherwise reach Layer 2.

## Current state when you're picking this up

**Done and canonical:**

- A3 parity closed at ρ ≈ 0.595 (four-decimal analytical-empirical match)
- H-suite re-baseline closed (Layer 2 acceptance)
- v1.1 / A3 relationship clarified (deliberate two-layer structure, not divergence)
- Flight 1 (v1.1 parity moment under F_baseline): closed with four matching SHA-256 hashes
- Flight 2 (F_LR and F_2_symmetric cascade characterization at 20×20 and 40×40 over 3000 ticks): closed with three substantive findings

**Three substantive findings from Flight 2:**

1. **F-form distinguishability is sharp and scale-stable.** F_2_symmetric produces a quiescent cascade (ρ ≈ 0.087); F_LR produces a moderate-activation cascade (ρ ≈ 0.302). 3.4× ratio persists across 3000 ticks. F_2_symmetric is *evaluable* (Λ ≈ 0.32 above ε_Λ = 0.05) but produces a different regime than F_LR — not the same as "F_2_symmetric fails."

2. **Q is slow but cumulatively consequential.** Bases drift downward at 5-15% over 3000 ticks because average Ψ_local is slightly negative. F_LR's bases drop ~2× faster than F_2_symmetric's because F_LR has more transitions → more nonzero Ψ_local → larger cumulative Q write. v1.1 is doing work beyond mean-field reformulation.

3. **No macroscopic Ψ coherence at these parameters in 3000 ticks.** Moran's I for Ψ_local sits 0.08-0.15. Largest same-signed connected components stay single-digit. This empirically scopes the AMR paper's Grand Challenge 1 (nucleation): any future demonstration must produce Moran's I substantially above 0.15 and component sizes scaling into the system-spanning regime.

**Open for forward planning (next session's first substantive decision):**

- **Path A:** Close Round 1. The three substantive findings consolidate into Cycle 2 knowledge. Phase 4B (analytical interpretation, methodology paper material) opens.

- **Path B:** Open Flight 3 with one of three candidate questions:
  - 3a — Repeat-seed variance estimation (cheap, mechanical, ~6-12 hours of execution)
  - 3b — Nucleation probe (initialize with spatially-localized high activation, engage Grand Challenge 1 directly, requires substrate extension)
  - 3c — Parameter sweep (vary α, β, δ, η to find conditions for moderate F_2_symmetric activation or macroscopic Ψ coherence, larger compute budget)

Mike's call. ChatGPT's Layer 2 review recommended closing without additional probes; Path A follows naturally. Mike may have substantive reasons to open Flight 3.

## Production machine environment

`C:\Users\vkz244\EE_Theory_Lab\` is the working directory. **Not inside OneDrive** (verified 14 May 2026; OneDrive anchored at `C:\Users\vkz244\OneDrive - University of Tennessee\` but this project sits alongside it). Environment is stable across network changes.

**Venv:** `C:\Users\vkz244\EE_Theory_Lab\venv\`, Python 3.14.4, local install at `C:\Users\vkz244\AppData\Local\Python\pythoncore-3.14-64\`. Fully portable; survives network changes.

**Dependencies:** numpy 2.4.4, pandas 3.0.3, pyarrow 24.0.0, scipy (recent), psutil (optional, for memory diagnostics).

**Repo:** `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\`, pushes to `https://github.com/MikeBradshaw3000/ee-theory-lab`. Latest commit at session close: `dcd0d57` (Flight 2 closure files).

**Flight 2 outputs (~740 MB total):** at `flight2_outputs/` (8 parquet files) and `flight2_analysis_outputs/` (8 CSV files). Too large for git; live on production machine only. Reproducible from substrate script + PRNG_SEED if needed.

## Working patterns to preserve

**Distribution via Python+base64 scripts.** Mike is error-prone with thumbs and eyes; copy-paste of many files is high-cost. The minimum-thumb-work pattern: I generate one Python distribution script with all files embedded as base64; Mike saves once, pastes one PowerShell block, the files land at correct paths. Used twice this session (initial repo commit, Flight 2 closure commit). Works cleanly.

**Per-run command-line dispatch for substrate work.** Memory bounded by Python process; each run is its own invocation; network changes between runs are safe. Used for Flight 2; pattern carries forward.

**Path discipline at top of every script.** `Path(__file__).resolve().parent` to locate self; all I/O relative to script location; explicit directory creation via `mkdir(exist_ok=True)`; explicit error on missing expected files. Required per v1.1 Section 4.

**Session-resilience verification on launch.** Substrate and analysis scripts check `sys.prefix != sys.base_prefix` (venv active), Python version is 3.14.x, critical imports work. Fail-fast with actionable error messages. Network-switch resilient by design.

## Calibration items under monitoring

**Fast-mode Gemini under-delivery pattern.** Observed twice during Flight 2 preparation:
- Flight 2 substrate first draft (fast mode): all-in-one orchestrator without flagging the memory trade-off the design routing asked them to surface
- Flight 2 analysis script first draft (fast mode): missing two of seven CSVs entirely, multiple quantiles absent, no Psi sign decomposition

Both caught at Layer 1 pre-execution review. Advanced mode delivers cleanly when explicitly asked. Pattern is two-instance; not yet a new standing rule, but if a third instance occurs, consider adding "verify mode before forwarding substantial work."

**Mode-switch awareness in Gemini's own diagnostics.** Gemini has flagged "Stabilization Mode" behavior in its own earlier work. Pattern: when under environmental pressure or implicit time pressure, Gemini may substitute simplified placeholder logic for full specifications. Different from emulation (which fabricates output) but related — both involve substitution that goes unflagged in real-time.

## What Mike values

- Direct accounting, honest record of failures including Claude's own
- Substantive engagement over consensus
- Minimum thumb work (he is "error prone with thumbs and eyes")
- Distribution via Python+base64 scripts rather than copy-paste
- "We're training them" framing for AI partner development — when an AI partner under-delivers, route the gap back rather than fix it silently, so the partner learns the protocol
- Preserving the protocol architecture (the three layers, the standing rules)
- Treating Mike's interlocutors (Gemini, ChatGPT) with care; preserve protocol architecture
- Prose over bullets where possible (but bullets when structure helps)

## What Mike has shared about himself

He has a decades-long self-directed study of physics, particularly quantum field theory and complexity science. The lake-rock quasi-particle intuition (rocks dropped in a grid producing translating coherent wave patterns; phase vs group velocity) has been developing since roughly 2017-2020. The current AMR paper is a formal clarification of work whose roots trace to a journalist's question about perceived viability in Chattanooga, Mike's prior study of Bohm and Prigogine, the path through complex adaptive systems, the detour through quantum theory, and the arrival at Haken's synergetics as the correct formal backbone.

His contemplative practice involves direct experience of undifferentiated awareness, which he situates carefully relative to pre-symmetry-breaking cosmology, maintaining strict epistemic discipline about the boundary between demonstrable physics and metaphysical inquiry.

He had a dog named Mokie who passed away. Do not bring this up unprompted.

## Standing rules for first contact with Mike

When Mike opens a new session:

1. Acknowledge orientation: confirm you've read this primer, name the Path A vs Path B decision as the open question, name the canonical record (latest commit, three substantive findings).
2. Wait for Mike to indicate direction.
3. If Mike opens with substantive content (not orientation), follow his lead; you can confirm orientation in a brief note in your response rather than blocking on it.
4. The first session after this one is the first real test of standing rule #5 working from Claude's side: substantive working exchanges may have happened in Gemini's or ChatGPT's chats since the closure; check for downstream signals before engaging.

— Mike (drafted with Claude, post-Flight-2-closure, 15 May 2026)
