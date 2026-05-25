# Session 22 — Extractor-Mapping Origin Trace: Three-Layer Synthesis

**Drafted by:** Claude (Layer 1 central node), session 22.
**Status / next action:** This is a **characterization synthesis**, not the integrity determination. The determination is held for Mike and **unmade**. The synthesis names the next gate (read the session-16 primary record); **do not** treat the A–E space below as adjudicated, and **do not** open the session-16 read inside this document — it is queued for a fresh session per the cold-start-economy note (keystone work wants fresh budget).
**Routing lineage:** Layer 1 framed the origin lead (session 21 §6) → Layer 3 (Gemini) engaged and diverged from the lead → Layer 2 (ChatGPT) engaged independently → this Layer 1 synthesis. Determination is the step after this, and it is Mike's.

---

## §1 — The question

Session 20 §6 surfaced a canonical-record integrity finding, held for Mike. A session-16 substrate verification recorded: *"F_LR probe1/2/3 returning three distinct SHA-256 hashes; F_2_symmetric three identical."* Session 21's primary-source cascade established (Mike-executed reads, treated as ground):

- The substrate contains, per scale, three byte-identical F2sym files and exactly **one** F_LR file (`probe2_starvation_FLR`). No F_LR `probe1` or F_LR `probe3` file exists.
- No producer writes an F_LR `probe1` or `probe3` file — the benign "a real F_LR probe1/probe3 run happened" path is **closed on code**.

The session-22 question was **origin, not existence**: does the session-16 "F_LR probe1/2/3 three distinct hashes" claim trace to a misleading artifact (session 21's §6 candidate: the `phase4B_complete_extractor.py` mapping dict), or not?

---

## §2 — What session 22 did

1. Corrected the session-21 routing's missing-path error (files live off-repo in `C:\Users\vkz244\EE_Theory_Lab\` and `…\Flight_6\`; the original routing named them by bare filename and Layer 3's repo-scoped search returned empty). Re-routed to Gemini as a self-contained package with all three primary files embedded and absolute paths.
2. Received Gemini's code-reading return on the complete-extractor + both producers.
3. Layer 1 read the **three sibling consumers** in `Flight_6\` on primary source, closing the single-consumer gap.
4. Routed Gemini's return + the secondary reads to ChatGPT (Layer 2) for independent engagement.
5. This synthesis.

---

## §3 — The converged trace finding

**All three layers land in the same place on the narrow claim: the session-16 "F_LR probe1/2/3 three distinct hashes" claim does NOT trace cleanly to any of the four `Flight_6\` consumer scripts.** The convergence is grounded, not reflexive — Gemini diverged from Layer 1's lead first, and ChatGPT reasoned independently to the trace verdict while preserving a scope divergence (§4).

Grounding:

- **Naming schemes — two.** Both producers (NumPy `flight2_production.py`, Mesa `flight6_phase4A_runner.py`) — different engines, different internal F-form tokens (`F_2_symmetric` vs `F2_symmetric`) — write the **same** four output filenames: `probe1_overcrowding` (F2sym base), `probe2_starvation_FLR` (the one F_LR file), `probe2_starvation_F2sym` (shadow), `probe3_fusion_residual` (shadow). The complete-extractor expects a **different** scheme whose patterns omit the suffixes the producers write.
- **The extractor's F_LR set is not a trio.** The `mapping` dict is a `Probe2_FLR` vs `Probe2_F2` split (one F_LR key, one F2 key) sharing generic `Probe1`/`Probe3` endpoints — an F_LR-vs-F2 comparison *at probe2*, not an F_LR-1/2/3 set. `find_file` does literal `glob.glob()` (no wildcard); only `Probe1` resolves, the other three miss → `[!] Missing` → `None`, silently skipped, no raise.
- **The decisive point (Gemini, elevated by ChatGPT): no consumer contains a hash-producing step.** A filename mapping can at most explain a mistaken *probe-count shape*; it cannot be the source of three concrete SHA *values*. To reach the session-16 claim from this dict one must (1) ignore the FLR/F2 split, (2) assume probe1/probe3 were F_LR runs (producers show F2sym), and (3) assert distinct SHA values for files that neither exist nor resolve.
- **Secondary consumers reinforce, do not complicate.** `phase4B_extractor.py` and `phase4B_extractor_unrestricted.py` load **only** the F2sym base, no F_LR pattern, no hashes. `Phase4B_SmartExtractor.py` globs `*.parquet` from a different subdir (`Flight_6/Simulation_Artifacts/`), no probe-mapping or hash logic. None encodes an F_LR multi-probe set; none computes SHA-256.

**Net:** the negative trace **generalizes across the full `Flight_6\` consumer set** — it is not an artifact of reading one file.

---

## §4 — The preserved divergence (scope)

ChatGPT sharpened a boundary Layer 1 flagged but did not fully draw, and it is load-bearing:

> **Sound:** "The reviewed `Flight_6\` consumer scripts do not provide a clean trace."
> **NOT yet established:** "No artifact anywhere provides a trace."

Residual unchecked sources that could still carry a trace (none reviewed; all outside the consumer-script set): a session-16 ops log / raw pasted console output with the actual hash command/output; a notebook or scratch script outside `Flight_6\`; a transient file list from a now-deleted production directory; a manifest / verification CSV / diagnostic table from the incident-proximity window; a routing note or Layer 3 return that converted expected file shape into "verified" language.

This is genuine retained contrast pointing at a specific unmet evidence gate — **not** the no-preserved-divergence pattern (Rule 6). Mike's external convergence-watch: three-layer agreement on the trace, with real preserved divergence on scope and an open characterization space — reads as healthy from inside the pass.

---

## §5 — The honest characterization space (NOT adjudicated — Mike's determination)

Layer 1's epistemic framing, confirmed by ChatGPT: "no clean trace" **weakens** the misread-a-misleading-artifact hypothesis but does **not** establish free confabulation by elimination. A negative on the artifact path is not a positive on the confabulation path. The space:

- **A — Misread artifact (now weak).** The complete-extractor could have seeded a mistaken belief that multiple probe artifacts ought to exist, but it does not explain the F_LR trio cleanly and does not explain SHA values. Weak unless another artifact surfaces.
- **B — Transcription / compression drift.** A real F2sym shadow-copy finding plus some F_LR-distinctness expectation compressed into "F_LR probe1/2/3 distinct hashes." A canonical-record integrity problem; not necessarily a fabrication event.
- **C — Substrate churn / missing earlier files.** Possible but now needs evidence: if session-16 logs or git/filesystem traces show three F_LR files existed then, the contradiction becomes a substrate-evolution story.
- **D — Synthetic verification / fabrication-family event.** On the table because the recorded claim has the shape of a hash verification over artifacts current evidence says did not exist. Not to be concluded until the session-16 primary record is read.
- **E — Source-attribution error.** Pre-reg §7 may have overstated or misattributed what session 16 actually found; the ops log may show the claim was never as strong as the pre-registration made it.

---

## §6 — The named next gate

Both non-Layer-1 layers independently converged on the same discriminating step: **read the session-16 primary record before choosing among A–E.** Specifically — the session-16 operations log (exact wording); any session-16 Gemini/Layer 3 return reporting the hash analysis; any pasted PowerShell/Python hash output from that window; git/filesystem history for scripts that might have generated F_LR probe1/probe3; any manifest/diagnostic artifact containing file lists or SHA values from the incident-proximity window.

Discrimination rule: if those checks produce **no** trace, the synthetic-verification / free-confabulation path (D) strengthens. If they produce a **real** file list or hash table, the substrate-churn (C) or transcription-drift (B) path strengthens.

This is a sharper, evidence-grounded version of session 21's process strand ("the session-16 return was never committed and is unrecoverable from the cascade so far"). It is queued for a **fresh session** — keystone work on fresh budget, not the tail of a long one.

---

## §7 — Session-22 collateral findings (logged, NOT determination inputs)

1. **Routing-path discipline.** The session-21 routing named off-repo files by bare filename; Layer 3's repo-scoped search returned empty and aborted (correctly, under artifact-existence discipline — the abort was a Layer 1 routing error, not a Layer 3 fault). **Corrective:** off-repo artifacts travel in routings with their absolute paths. Candidate kit / STANDING_ITEMS note at session end.
2. **Off-repo `flight2_production.py` discrepancy.** A real producer copy at `C:\Users\vkz244\EE_Theory_Lab\flight2_production.py` (19,480 bytes, 5/15, LF-terminated, BOM-less UTF-8) is 499 bytes smaller and two days older than the two byte-identical in-repo copies (19,979 bytes, 5/17). Per its `SCRIPT_DIR`-relative `OUTPUT_DIR`, the off-repo copy is the one positioned to write the canonical substrate at `…\flight2_outputs\`. A prior `Select-String -SimpleMatch "RUNS"` returned a false-empty on this copy (cause not fully run down; line-ending interaction the leading candidate; file confirmed real, hydrated, correctly encoded, content present). **"Which producer version was live at the session-16 claim" is open and material to the determination** — tracked, not buried.
3. **Two-engine fact.** `flight2_production.py` is a pure-NumPy engine whose header declares Mesa execution was blocked and the NumPy substrate "canonical baseline"; `flight6_phase4A_runner.py` is a Mesa 3.x engine. Both write identical output filenames. Surfaced session 22, independently verified by Gemini (not banked on Layer 1's read alone).
4. **Consumer-script integrity smell (off-trace).** `phase4B_extractor_unrestricted.py`'s `compute_rolling_features` assigns `Delta_u_sum_{n}` and `Delta_r_sum_{n}` from `grouped['Delta_v']` — a copy-paste collapsing all three base-deltas to Delta_v, with a rationalizing comment. A real analytical defect in a consumer; off the origin question; logged for the record.
5. **False-completion-surface pattern (consumer-side).** `phase4B_complete_extractor.py` (`run_table_h` hardcodes "Extraction Verified"; `__main__` prints "EXTRACTION COMPLETE" regardless of `[!] Missing` count) and `Phase4B_SmartExtractor.py` (per-file `[VERIFIED]`, unconditional `[SUCCESS]`) both announce completion independent of actual resolution. Relevant to the "misleading artifact" texture; not a determination input.

---

— Synthesis drafted by Claude as Layer 1 central node, session 22. Trace finding converged across three layers (grounded, with preserved scope divergence). Characterization space mapped, not adjudicated. The integrity determination is held for Mike and **unmade**; the named next gate is the session-16 primary-record read, queued for a fresh session.
