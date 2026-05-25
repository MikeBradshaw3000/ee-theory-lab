# Layer 3 Routing — Session 21, Extractor-Mapping Origin Read

**From:** Claude (Layer 1 central node), session 21 — drafted for relay to Gemini (Layer 3) via Mike.
**To:** Gemini (Layer 3).
**Mode:** Code reading and characterization only — role 1 (read pasted code) / role 3 (interpret it). **NOT execution.**
**Next action for you:** confirm the §0 gate, then read the §4 files and answer §2. Do NOT make the integrity determination (it is Mike's, and unmade); do NOT execute anything; ask Mike to paste any file you need but have not been given.

---

## §0 — Instance-state and capability gate (confirm before reading)

Confirm two things back to Mike before engaging:

1. You are operating in current Cycle 2 Phase 4B protocol context — not a prior-cycle or unrelated context.
2. You understand the capability boundary: you cannot run scripts, read the local filesystem, hash files, or execute anything. You read only the file contents Mike pastes into this chat. If you need a file, or more of a file than you were given, **ask Mike to paste it** — do not infer its contents or narrate what running it would show. A request phrased as "run" or "execute" means "tell Mike what to run"; it never means you ran it.

This gate exists because the question below is itself about a verification that was accepted without execution. Re-creating that failure mode here would be self-defeating.

## §1 — What this is and why

Session 20 surfaced a canonical-record integrity finding (session-20 ops log §6), held for Mike's determination. A session-16 substrate verification had recorded: "F_LR probe1/2/3 returning three distinct SHA-256 hashes; F_2_symmetric three identical." Session 21 ran the full primary-source cascade. Treat the following as established (Mike-executed reads — do not re-derive or re-assert hashes):

- The substrate at `flight2_outputs/` contains, per scale: three byte-identical F2sym files (probe1_overcrowding [un-suffixed], probe2_starvation_F2sym, probe3_fusion_residual), and exactly one F_LR file (probe2_starvation_FLR). No F_LR probe1_overcrowding or F_LR probe3 file exists.
- Live SHA-256 (20x20): the three F2sym files all hash to `5D8F5496...C897`; the one F_LR file hashes to `ADC1E3C0...A296`. The F2sym shadow structure is real; the F_LR "three distinct" claim is contradicted on file existence.
- No producer on disk writes an F_LR probe1_overcrowding or F_LR probe3 file (confirmed against the producer RUNS dict and the runner export/copy logic; excerpts in §3).

So the benign path — "a real F_LR probe1/probe3 run happened off-repo" — is closed on code: no producer can write those files.

**The open question is origin, not existence.** Was the session-16 "F_LR probe1/2/3" claim free confabulation, or does it trace to a misleading artifact that could be read as asserting an F_LR three-probe set? Session 21 found a candidate source — the extractor's file-mapping — and that is what you are asked to read.

## §2 — The question for you

Read the full files in §4 and characterize, in your own framing:

1. **Enumerate the naming schemes.** How many distinct parquet-naming conventions appear across the producers and the consumers, and which artifact uses which? (Layer 1's partial read found at least four — see §3 — but Layer 1 has seen only excerpts. Verify against the full files; correct the count if it is wrong.)

2. **What does the extractor treat as the F_LR comparison set?** Read `phase4B_complete_extractor.py`'s `mapping` dict and its `find_file` resolution logic. What file set does it expect? What does it actually resolve to against what the producers write? What happens to entries it cannot find?

3. **Does the session-16 "F_LR probe1/2/3 distinct hashes" claim trace to this mapping?** Is the claim well-explained as a reading of the extractor's dict structure (which names a probe1 / probe2_FLR / probe3 trio), or not? State the strength of the trace, and what would distinguish "misread a misleading artifact" from "confabulated freely" — and say clearly if the code does not let you discriminate between them.

## §3 — Anchors Layer 1 has grounded (engage these; do not assume them)

These are Layer 1's reads from excerpts only. Verify against the full files and flag anything wrong.

- **Producer `flight2_production.py` RUNS dict (lines ~428-435):** F2sym rows carry the overcrowding / fusion_residual trio; `flr_` rows carry `probe2_starvation_FLR` and `None` for shadow targets.
- **Runner `flight6_phase4A_runner.py` (lines ~178, ~189, ~192):** F_LR exports only `flight6_probe2_starvation_FLR_{scale}`; `probe1_overcrowding` is written un-suffixed as a base file; `probe3_fusion_residual` is a `shutil.copy` of that base.
- **Extractor `phase4B_complete_extractor.py` mapping dict (lines ~21-34):** keys `Probe1` / `Probe2_FLR` / `Probe2_F2` / `Probe3`, with patterns `probe1_overcrowding_{s}`, `probe_F_LR_{s}`, `probe_F2_symmetric_{s}`, `probe3_fusion_{s}`. On Layer 1's read, three of these four patterns match no producer output (the `probe_F_LR_`, `probe_F2_symmetric_`, and `probe3_fusion_`-without-`residual` names). `find_file` returns `None` and prints `[!] Missing` rather than raising.

## §4 — Files to read (ask Mike to paste any not yet provided)

Primary:
1. `phase4B_complete_extractor.py` — full (Layer 1 has seen only the first 80 lines).
2. `flight2_production.py` — full (model + RUNS dict + shadow-copy logic).
3. `flight6_phase4A_runner.py` — full.

Secondary (read only if the primary set leaves the naming-scheme question open):
4. `phase4B_extractor.py` and `phase4B_extractor_unrestricted.py` — sibling consumers.
5. `Phase4A_Execution.py` and `Phase4A_FullSpec_Execution.py` — probe-list definitions.

## §5 — What you are NOT asked to do

- Not to make the integrity determination. It is Mike's, and unmade. Do not conclude "fabrication" or "not fabrication."
- Not to execute, hash, or read the filesystem. Code reading only.
- Not to assert anything about a file you have not been given — ask for it.
- Not to converge to Layer 1's §3 framing if the full files do not support it. If the four-scheme read is wrong, say so. Preserved divergence is a finding (Rule 6), not a problem to smooth.

## §6 — Return scope

A characterization Mike carries back to Layer 1: the naming-scheme enumeration, what the extractor treats as the F_LR set, and your read on whether the session-16 claim traces to the mapping — with explicit flags where the code does not let you discriminate. Brief is fine. This return routes next to Layer 2 (ChatGPT) for engagement before any of it is folded into the canonical record.

— Routing drafted by Claude as Layer 1 central node, session 21, for relay to Layer 3 via Mike. The integrity determination remains held for Mike and unmade; this routing develops the origin question only.
