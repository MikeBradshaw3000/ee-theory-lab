# Phase 4B Operations Log — Session 21 (INTERIM — PARKED MID-DETERMINATION)

**Date:** 22 May 2026
**Session start HEAD:** `b77959db4fabaab77a33ed6e2e2fc0c478f6fddb` (Mike-executed via `git rev-parse HEAD`; stable across three reads this session. Layer 1 did not and cannot independently verify — the anchor is Mike's execution reaching Layer 1 as a paste, per the asymmetric-execution-channel discipline.)
**Session park HEAD:** [self-referential — committing this log changes HEAD; verify live next session via `git rev-parse HEAD`].
**Kit operative:** kit-revision-5.1 (`claude_instantiation_kit_v5_1.md`).

**Status: PARKED MID-DETERMINATION.** The session-16 F_LR / F2sym integrity question is **held for Mike's determination and UNMADE.** This log is a parking record so the next reader works from current state rather than the session-20 §6 "Rule 7.3 fabrication signature" framing, which the completed evidence chain materially refines (§4).

**Next action (Mike's, and it IS the determination):** the recollection check on a real out-of-repo F_LR run, done away from the keyboard. **Do NOT** draft the STANDING_ITEMS integrity item, the E4 reshape, the formal record, or any characterization-as-conclusion from this log's contents alone. Re-anchor against Mike's call first; only then draft what the determination sets.

---

## §1 — What this log is

Session 21 opened from kit-revision-5.1 against the session-20 log to support Mike's first-substantive-work item: the session-16 F_LR hash integrity determination (session-20 §6), held for Mike's arbitration. Session 21 ran the complete primary-source verification cascade the session-20 resume anchor named, plus live SHA-256 reads. The repo has now given up everything it holds on the question; no further repo read would move it. The remaining unknowns are not in the repo — Mike's recollection of an out-of-repo F_LR run, and an optional account from the session-16 Gemini instance.

Mike elected to park the state in a committed durable record and do the recollection check away from the keyboard. This is an interim log, not a close-out: the session's heaviest item is open by design.

## §2 — Verification cascade completed this session (Mike-executed reads)

Every value below is Mike's pasted execution against the repo / substrate. Layer 1 operates in the chat sandbox and cannot reach either; none of these are Layer-1 verifications.

**Read 1 — HEAD.** `git rev-parse HEAD` -> `b77959db4fabaab77a33ed6e2e2fc0c478f6fddb`, three times, stable. (At session open Layer 1 declined to confirm the supplied `b77959d` prefix from assertion, surfacing it as a Mike-executed read instead — the same asymmetric-execution-channel discipline at issue in the finding itself.)

**Read 2 — F_LR overcrowding production footprint.** `git log --all -S "probe1_overcrowding_FLR"` -> three hits: EDA script `22aedba` (consumer), session-18 closure `0eb92a5` (documents the mismatch), session-16 closure `1d07d7f` (the claim's origin). The producer commit `dcd0d57` does NOT appear. The token's entire tracked lifetime is declared-by-claim -> consumed-by-EDA -> flagged-missing; never produced. Rules out a committed producer run on any branch; cannot rule out an uncommitted scratch run (the §93 residual).

**Read 3 — session-16 Q1 follow-up content (`1d07d7f` tree).** The token lives in (a) the pre-reg `data_files:` block declaring four `probe1_overcrowding` files for both F-forms — a declaration already mismatched against the producer at pre-reg stage, so the E4 structural problem is present at origin, not a later discovery; and (b) the Q1 follow-up routing note, which is a **leading prompt**: it states the expected answer ("the three F_LR files should produce three distinct hashes...") before requesting it, and invites filename adjustment for files that do not exist. A grounding instrument built to confirm, not to discriminate.

**Read 4 — the session-16 return (`5d8f549` grep at HEAD).** The committed return is arc step 14 of the session-16 ops log — Layer-1's one-paragraph paraphrase. It records F2sym as `5d8f54921b6d91c784e2a1b9c30f81d4a6e8c7104b2a10d9f48123c5a69123b0` and F_LR as "three distinct hashes across probe1/2/3" with **no actual F_LR hash strings**. It also offered a "canonical filename" `flight6_probe3_fusion_residual_*.parquet` as a correction — for an F_LR probe3 that does not exist. (This read also confirmed the session-20 log snapshot is faithful on its §5/§6 lines; the close-out cluster did commit the session-20 log.)

**Read 5 — live SHA-256 of 20x20 substrate.** `Get-FileHash` on `flight2_outputs\*20x20*.parquet`:
- Three byte-identical files = `5D8F54966A1FF5B8328B6524752EA92C858C09EFCBA07B3B3451AD1DA3D0C897`: `flight6_probe1_overcrowding_20x20` (the F2sym probe1, written without an F-form suffix by the producer), `flight6_probe2_starvation_F2sym_20x20`, `flight6_probe3_fusion_residual_20x20`. F2sym shadow-copy structure confirmed real on live execution; the session-20 Step-4 "real" prefix `5d8f5496` confirmed as the full string.
- One F_LR file: `flight6_probe2_starvation_FLR_20x20` = `ADC1E3C0089777F3559AFD1BF04F4499F700D8382162F564C0325C3FDB59A296`. No F_LR `probe1_overcrowding`, no F_LR `probe3` at this scale. F_LR count claim contradicted on live execution.

**Read 6 — provenance (`ls-tree` of `phase_4b/reviews/layer3/`).** Three files, all outbound Layer-1 -> Gemini routing notes; **no raw Gemini return artifact.** The session-16 return exists only as Layer-1's paraphrase. The origin of the F2sym recorded-value discrepancy — Gemini's return vs. Layer-1's transcription — is therefore unrecoverable from primary source.

## §3 — The finding as it stands (CHARACTERIZATION, NOT DETERMINATION)

The three strands below are Layer 1's reading offered to support Mike's determination. They are not the determination. Fact (live read) is separated from interpretation in each.

**F2sym strand.** *Fact:* structure real and confirmed live (three byte-identical files, `5D8F5496...C897`); the session-16 recorded value (`5d8f5492 1b6d...`) shares only the 7-char prefix `5d8f549`, then diverges entirely. *Interpretation:* not this file's hash mistyped (the whole tail differs), and not a from-scratch invention (the shared prefix is too hard to land by chance, ~1 in 16^7) — best fit is a real value, garbled, that preserved the prefix. Author of the error (Gemini return vs. Layer-1 transcription) is **unassignable** — no raw return was committed. Under-determined, and now established as such.

**F_LR strand.** *Fact:* one F_LR file at 20x20, not three; no `probe1_overcrowding`, no `probe3`; producer makes none; no F_LR hash strings were ever recorded; the offered `fusion_residual` filename is a real F2sym shadow-copy name mis-attached to a non-existent F_LR probe3. *Interpretation:* consistent with a working-memory narrative occupying the gap (Rule 7.4), and the mis-attached filename propagated into STANDING_ITEMS (session-16 arc step 16). Benign path: a real, out-of-repo, uncommitted F_LR `probe1_overcrowding` / `probe3` run Mike recollects. **This strand turns entirely on Mike's recollection check — which is why that check is the determination.**

**Process strand.** *Fact:* the session-16 substrate return was never committed and is unrecoverable; Layer-1 accepted a paraphrase as "cleanly grounded" while watching for the wrong failure mode (architectural inference). *Interpretation:* true regardless of how F2sym and F_LR resolve; points at a protocol fix (raw substrate returns get committed, not paraphrased) more than at a person, and is arguably the most actionable durable output of the cascade.

## §4 — Relation to the session-20 §6 framing

Session-20 §6 read the evidence as a single "Rule 7.3 fabrication signature" across three independent measures. The completed cascade refines this: the measures are not equally strong and do not point one way. Measure 2 (F2sym hash mismatch) is prefix-preserving — which weakens from-scratch fabrication for that strand and pairs with a confirmed-real F2sym structure. Measure 1 (F_LR count) is the strand carrying weight and is recollection-gated. Measure 3 (timestamp) is a gate that closed the regeneration path, not an independent strike.

Net: complete primary source does not support a flat fabrication determination; it supports a bifurcated-plus-process shape. The *direction* — that something in the session-16 verification reached the canonical record wrongly — is well-supported; the disagreement with the session-20 framing is about *kind and author*, not *whether*. **This is Layer 1's characterization; Mike's determination governs.**

## §5 — Held / not done at park

- **Determination** — held for Mike, UNMADE, not pre-written.
- **STANDING_ITEMS** — no edits applied this session. The session-20 §8 edit-spec remains queued; the integrity-item wording waits on the determination, and per §3-§4 the shape it should take is three-limbed (F2sym under-determined / author-unassignable; F_LR recollection-gated; process gap), not a flat fabrication item.
- **E4 remediation (A vs B)** — untouched; may be reshaped by the determination (session-20 §8).
- **Item 12 / item 15** — unchanged from session-20 §7 (item 12 recharacterized, blocked behind E4 + determination; item 15 component 2 blocked, input set unassemblable).
- **EDA** — not runnable; no Layer 3 execution contract exists or can be written. Premise void.
- **`b77959d` and this log's commit** — push held; local-only until Mike says otherwise.
- **Carried-forward independent-trigger check** (6b/6c/7/13/14) — still owed; now slipped to session 21 as well.

## §6 — Resume anchor

**Next action is Mike's, and it is the determination:** the recollection check on a real out-of-repo F_LR `probe1_overcrowding` / `probe3` run — done away from the keyboard, honestly distinguishing remembering from wishing, and (per the project's own memory-vs-primary-source discipline) treated as weak if nothing but the impression supports it, and as real if an artifact corroborates it (a scratch script, a console log, a dated note, a stray parquet with an F_LR overcrowding name and a real timestamp).

**On Mike's return, do NOT act on §3-§4 characterization as the determination.** Re-anchor against Mike's call. Then, and only then, draft what the determination sets: the three-limbed STANDING_ITEMS integrity item in final wording; the E4 remediation framing (A vs B); the formal protocol record (fabrication-family event, near-miss, or process-finding) if Mike judges it warranted; and the session-20 §8 edit-spec items.

**The evidence chain is complete; no further repo read will move it.** The optional remaining lever — asking the session-16 Gemini instance to account — is low-diagnostic now (leading prompt + uncommitted, unrecoverable raw return) and is Mike's election.

**HEAD at park:** [self-referential — verify live next session].

---

— Drafted by Claude (Layer 1 central node), session 21, as an interim parking record at Mike's instruction. The session completed the session-16 integrity verification cascade to the limit of repo primary source; the determination is held for Mike and unmade. Committed (push held) so the next reader works from current state rather than the session-20 §6 framing.
