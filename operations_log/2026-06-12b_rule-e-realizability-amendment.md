# Operations log - 2026-06-12 (b) - Rule E realizability consultation + contract amendment

**Session date:** 2026-06-12 (second session of the day)
**HEAD at session start:** 5b77c1b (ops log: Rule E design contract session)
**HEAD at session end:** 2f3ce0e (Rule E contract: raw block records, open-6 resolved)
**Layer 1:** Claude. **Execution channel:** Mike.

## What this session did

1. **Layer 3 (Gemini) realizability consultation routed and returned.** Per the prior session's scope-fenced agreement, Layer 1 drafted a non-implementation consultation note to Layer 3 (five questions: recording data structure; block-resolved observables feasibility; open-6 block count; alpha-zero exactness; leak surfaces). Framing held: what an implementation would record/produce, no code, no L2 clearance declared by Layer 3, mechanism design and grid fenced as opens above Layer 3's lane. Layer 3 responded in lane.

2. **Layer 3 findings (substrate-level):**
   - Q1: separate per-run block CSV (one row per 25-tick block, joined on run_id) preserves the established window-CSV reading conventions; wide-CSV and NPZ-embedded options rejected as reshaping or hiding the guard data.
   - Q2 (substantive): block-resolved z-scores against the inherited 100-tick null are statistically invalid (the null is horizon-scaled); a valid block-level z would need a separately constructed 25-tick null at ~4x permutation cost. Raw block-resolved observable values are fully feasible and require no new apparatus logic.
   - Q3: four blocks per window is insufficient to discriminate oscillation from drift; ~2-3 cycles (8-12 blocks) needed; 400-800 tick records sit trivially inside the memory/runtime envelope (permutation nulls, not state arrays, are the only real cost).
   - Q4: RNG draw-order safe (macro signal is deterministic, consumes no RNG); residual risk is floating-point path through the conditioning function even at zero coefficient; a strict `alpha == 0` branching bypass guarantees bit-exact recovery.
   - Q5: three concrete leak surfaces enumerated in the current code shape (single Lambda variable passed into both becoming-active and survival arguments; mask-computation cross-contamination; scalar-vs-spatial effective-Lambda scope bleed).

3. **Layer 1 synthesis against the contract, three forks surfaced to Mike; Layer 2 arbitrated; Mike ratified by commit.**
   - **F1 (Section 5 z-score validity): = a.** Block-resolved records store RAW Psi_meanI_state and RAW Psi_persistence_I per 25-tick block; window-level z-scores and candidate flags remain at the inherited 100-tick level. Guard does within-record pattern discrimination, not block-level candidate classification. Added guard sentence: no block-level LowLow_Nondegenerate_Candidate unless a future contract constructs and validates a 25-tick null. (Convergence note: Layer 1's pre-routing recommendation and Layer 2's arbitration agreed from the same architectural ground - genuine convergence, not deference; recorded as such per symmetric-skepticism discipline.)
   - **F2 (open 6): = resolve now, as a minimum recording-adequacy requirement.** Rule E runs must record at least 12 post-burn-in conditioned macro blocks at the 25-tick cadence (>=300 post-burn-in ticks; a 400-tick baseline satisfies it). Resolution authorizes no grid and no seed. Layer 1's blocks-per-window correction preserved (the 100-tick window always contains four blocks; what extends is total post-burn-in conditioned blocks). Wording deviation from Layer 2 flagged and arbitrated: Layer 2's text carried two numbers (>=12 preferred, <8 inadequate); committed text binds a single minimum of 12 with the 2-3-cycle reasoning stated as rationale, the redundant 8 dropped. Mike did not revert; commit ratifies the single-number form.
   - **F3 (alpha-zero bypass): = constraint-at-resolution, NOT contract text.** Recorded here as a binding implementation constraint rather than a contract amendment, because the contract already owns the requirement (exact alpha=0 recovery, Section 4) and the bypass is the engineering means: **at implementation, `alpha == 0` must bypass the conditioning arithmetic entirely and call the un-conditioned local update path; exact recovery is verified at build/runtime parity; no reliance is placed on floating-point cancellation or post-hoc equality.** This constraint binds any future Rule E implementation spec.

4. **Contract amended and committed.** Section 5 amended (raw block values + z-score-validity clause + guard sentence + recording-adequacy minimum); Section 7 open 6 marked RESOLVED; status header records amendment provenance. F3 deliberately kept OUT of contract text and recorded in this log. Amended file 13692 bytes; placed by explicit suffixed-name copy (Downloads held three same-named copies: 10013 stale, 11628 prior-commit, 13692 amended as "(2)"); byte-verified at destination (13692, BOM-less 23 20 52, single trailing LF 74 0A). Committed 2f3ce0e; pushed 5b77c1b..2f3ce0e main -> main.

## Decisions of record

- Rule E design contract CANONICAL at 2f3ce0e. Section 5 now fixes raw block-resolved observable recording with window-level z-scores/flags; open 6 resolved as a >=12-post-burn-in-block recording-adequacy minimum. Still NON-SEEDING: no grid, no seed, no Layer 3 implementation authorization.
- F3 alpha-zero branching-bypass constraint binds any future Rule E implementation (recorded above; not in contract text).
- Layer 3 Q5 leak surfaces and Q1 recording structure feed the eventual implementation spec; not acted on now.
- Remaining named opens (1 h, 2 alpha grid, 3 base rule, 4 anchors, 5 reserved audits) UNRESOLVED; open 6 resolved. Scalar-vs-spatial effective Lambda (Q5.3) noted as live within opens 1/3.
- All rested arcs, cleared gates, locked topology, and the L4 fence unchanged. Rule E remains NOT seeded.

## Process notes

- Download channel hiccup: the 13692 amended file initially did not land in Downloads; source verified intact in outputs (13692, md5 6245ea8e...) before re-pull, which then produced the "(2)" copy. Destination size-check caught the absence before any wrong-size placement.
- Absolute-path destination verification used throughout (the size-0 relative-path trap from the prior session did not recur).
- Layer 3 stayed in lane; the one conditional reach toward criteria (Q2's "if the guard can function by raw values") was evaluated independently by Layer 1, not banked as Layer 3 clearance.

## State at session end

HEAD 2f3ce0e, origin current. Anchor (RESUME_2026-05-30.md) remains STALE on the Rule E line (still says "no contract") and now also predates the Section 5 amendment and open-6 resolution; refresh deferred to Mike's call - this log and the committed contract govern in the interim. Untracked read_obs001_nearnull_scale.py remains at root. Next eligible moves, all Mike's call: anchor refresh; resolution of remaining opens (1-5); implementation-spec drafting (would honor the F3 constraint, Q1 structure, Q5 leak surfaces). Nothing is pending.

Drafting partner: Layer 1 (Claude).
