# F9 Interpretation 002: placement note (2026-11-24)

**What is placed.** `rulings/F9_INTERPRETATION_002_FIDELITY_SUMMARIES.md` (`be9fae842c04e9088e47a0c398db78c88ab93bd208e4b7a5c13149cfb5f7636e`): an identified interpretation beside the FROZEN Contract F9 v0.7 (`60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`, bytes and identity unchanged), fixing how the fidelity items of §1.2′ (ii) and (iii) are reduced to reported numbers and how their uncertainty is stated (§5.7 row 4). Placed against `main` at `7a1094ad3e62d51142712243b9a3be1a89e311ca` (the evaluator precedence repair), checked against the remote before the kit was built. Documents only: no instrument file is touched and no test is run by this placement.

**Why it exists, and why now.** The contract names these items and their uncertainty recipes and does not fix every reduction of them (which cells are on the edge, which summary of m, which occupancy statistics, what "edges are compared" yields, what the resamples apply to). No Flight 9 job has been run and no master has been drawn; each of these would otherwise be a choice open after output. L1 has not opened the probe arrays and has computed none of these summaries on output of the rule. No code for them exists.

**How it was made, in order.**

| Step | Document | SHA-256 |
|---|---|---|
| L1's consultation: eight open points with a proposal each | `L1_TO_L2_F9_FIDELITY_SUMMARIES_CONSULTATION_2026-11-23.md` | `5811f97b2f2c9022db034cd3bcf359c62f2a932055550ee2bd30778d904b7f18` |
| L2's advice (a six-point package; one smaller supported alternative, occupancy only) | `L2_F9_FIDELITY_SUMMARIES_CONSULTATION_RESPONSE_2026-11-23_RECEIVED.md` | `c9df277a8d38449b2c37417e167a1aa6971f2fd8081a4283cac0f9cdf8b0156b` |
| Mike, 2026-11-23, on L1's three recommendations (adopt the package; include the direct edge comparison; an interpretation reviewed by L2 before any code): "Adopt, include, l2 review" | | |
| Draft 1 and its packet document | `F9_INTERPRETATION_002_FIDELITY_SUMMARIES_DRAFT_1.md`; `L1_TO_L2_F9_INTERPRETATION_002_REVIEW_PACKET_2026-11-23.md` | `b2efdeda1d063ccb6d46d66e0c8d0881d5131015221d1e4f20fb6bed943d1a07`; `2a27b5dcfc6e373ed760ba7fe88bb513f7d52bfea7316e8e90076726efd1cd24` |
| L2 round 1: NOT SOUND on D1 | `L2_F9_INTERPRETATION_002_DRAFT1_ROUND1_REVIEW_2026-11-23_RECEIVED.md`, with its witness `l2_i002_draw_gate_witness.py` | `3d892d6ebbbbcecbb3c9241c7acd0d510232a806a22cef445a9684b895efa2d9`; `87bdcb0239f4cec07e494775b0b34a37b3a2b9d6223875a96dc161ff551331af` |
| Mike, 2026-11-24, on keeping the closure's own fit and the fitted-level difference: "yes" | | |
| Draft 2 and its response document; the diff between the drafts | `F9_INTERPRETATION_002_FIDELITY_SUMMARIES_DRAFT_2.md`; `L1_TO_L2_F9_INTERPRETATION_002_ROUND2_RESPONSE_2026-11-24.md`; `f9_interpretation_002_draft1_to_draft2.diff` | `c7d8b54901f021dcdbcaf69b5aa17abee2ae2e7d98c921259e80c6f910cbdb63`; `4bf07d397456f62956f833eb1b35bcbc0c9b865dc5ea08704ad9b8828d68061d`; `a8952884d30a75ee3dca92897a5948b6cf9868ecf021e92dd78636d755d2b11a` |
| L2 round 2: **SOUND** as a proposed interpretation record | `L2_F9_INTERPRETATION_002_DRAFT2_ROUND2_REVIEW_2026-11-24_RECEIVED.md` | `930642a329cff452b26818b0f2f350d39901d3611e49f0367a191abd46d3f1de` |
| Mike, 2026-11-24: "accept" | | |

Every L2 return is a byte copy. The diff between the drafts is the packet's `draft1_to_draft2.diff` under a longer name, same bytes.

**The placed text is not byte-identical to the draft 2 L2 reviewed.** It differs in the title (the words "DRAFT 2 FOR L2 REVIEW" removed), in the last two entries of the authority statement (which now record L2's round-2 verdict and Mike's acceptance), and in one status line ("Status when accepted" is now "Status"). `f9_interpretation_002_draft2_to_final.diff` is the whole difference: three lines of draft 2 replaced by four. No point, constraint or consequence is touched. L2 has not seen the final bytes; it saw everything in them except those lines.

**The one finding (L2 round 1, D1), which was L1's.** Draft 1 said "The draws are made whenever any summary of the level is defined." That could be read as requiring an observed summary before any resample is drawn, and a build so made would drop defined edge-cell summaries where the observed map has no edge and the closure is unavailable. L2 gave a constructed witness (observed region empty; one valid resample with 324 region cells, 72 bonds, 68 and 72 edge cells), which L1 reproduced. The accepted text makes the draws for every applicable summary whether or not its observed value exists, and records a summary blocked on every draw by a fixed dependency as "not assessed on the draws", distinct from "assessed on 1,000 draws, defined on none".

**Where L2 corrected L1's original proposal, all accepted:** T0's spatial edge is never compared with anything (§4.3); λ*'s uncertainty is its full range over compatible draws and not a percentile range; §2.8 requires local m itself to be persisted; no range is defined for a component across draws. **Where L2 recommended differently, both adopted:** local m is reported wherever a non-T0 boundary exists, flagged when under-resolved; the region is rebuilt on every resample.

**One completion that is L1's.** L2 left it to L1 to state whether the two regional cell counts belong to the closure comparison or to the lattice map. The record makes them lattice fields, reported with their ranges when the closure is unavailable, and says the choice was L1's. L2 round 2: consistent, within what it left open, and needing no separate decision.

**What the record does not do.** It changes nothing placed, scores nothing, and authorizes no build by itself: the summaries are built as a third reports module through its own L2 rounds, whose build record must bind the accepted identities of its day (the evaluator as repaired at `7a1094a`; the skeleton stream declaration of the second reports module once that module is accepted). L2's review was of the specification; no implementation exists and none was run.

**Left to the third module's build declarations, within the bounds the record states:** field names and encoding; floating-point accumulation order; interpolation for the new spatial quantiles and percentile ranges (not the one inside S); the tie rule for a maximum's location; the encoding of causes; stream and source bindings; reuse.

**Carried, unchanged by this placement.** M6 part 2 (round 2 in preparation against `7a1094a`); the third reports module; qualification (§6); the runner with the authorization kit; the governance record (ratifications of M6-1 to M6-10, of M6 part 2's declarations when cleared, and of the build declarations to come); M3's two cause strings; L2's three further crossed-state tests for `test_f9_m3.py`; L2's two optional parser bounds; the two Flight 8 test notes. Held, nothing authorized: Gemini commission v3.1; the third-order lattice-versus-ODE comparison; onset continuity; the PD7-versus-floor correspondence.

**Placement authorizes no run.** No job has been run and no master has been drawn.
