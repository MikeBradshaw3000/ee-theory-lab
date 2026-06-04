# Operations log — 2026-06-03 Rule D R3 bracket read and findings

**Session:** Cycle 3 wave two (continuation). The Rule D R3 behavioral map (`cycle3/data_out/c3_w2_rule_d_r3_results.csv`, c1ff920) was read against the design contract Section 4 matched-coupling bracket, routed to Layer 2 for reading against its own mean-field prediction, and the conferred call committed to a canonical findings file.
**Layer:** Layer 1 (Claude) the bracket read, the L2 routing note, the findings draft and placement; Layer 2 (ChatGPT) the independent mean-field reading and arbitration on two forks (via Mike); Mike sole execution channel and arbiter (ran the reads, carried the L2 round-trip, set both forks).
**Opened from:** HEAD cbb8277 (R3 run-execution ops log).
**Closed at:** HEAD (this ops-log commit), origin current after push.
**Outcome:** Rule D R3 reads as a scoped negative — fails to produce the turnover-limited near-null mechanism under the locked topology and predeclared R3 grid. Arc rests (does not close). Findings file `cycle3/wave_two/rule_d/RULE_D_R3_FINDINGS.md` placed canonical.

---

## Sequence

Cold-start grounding from anchor + Rule D contract (R3-amended) + resolution memo (R3-corrected) + the R3 run-execution ops log. HEAD was cbb8277, later than the anchor's aeca987 and the instantiation prompt's expected 6857958; the run-execution ops log governed the run state (run complete, CSV committed c1ff920, theta=0 integrity check passed, bracket read deferred to this session). The anchor body's "run is NEXT STEP" line is stale on that one point; HEAD governs.

Full CSV pulled in one pane (350 rows, key columns) and read per-(setting, seed), both signs, settled windows. Layer 1 produced the fail-to-produce call. Routed a self-contained note to Layer 2 (test-not-confirm framing; four questions). Layer 2 concurred via an independent route (density-level R3 recurrence), corrected one scope-word, improved one label, and arbitrated two forks. Findings file drafted to L2's seven-point structure, placed by size-keyed Copy-Item, byte-state verified at destination.

## What the run produced (read from the CSV as primary source)

- Precondition met: `theta_turnover = 0` recovers the Rule C signed lower anchor under R3, both signs (c=-0.35 negative-persistence, c=+0.35 positive-persistence); no saturation; `effective_persistence = 0.40`.
- No candidate: `saturation_degenerate` / `extinction_degenerate` False on all 350 rows; `LowLow_Nondegenerate_Candidate` fires nowhere; `rho` lifted across the ladder; exposure live (`q_mean` ~0.29-0.42, `mean_abs_perturbation` ~0.056-0.077).
- Per-sign: c=-0.35 persistence stays negative, meanI climbs strongly positive (+14 to +22 by theta=0.35-0.50); c=+0.35 persistence stays robustly positive, meanI transits through null into negative. The co-equal pair is never jointly near-null at any theta.
- Bottom row of the Section 4.1 produce-or-fail table: responsive coupling remains signed (jointly never near-null) across the tested ladder, with no degeneration.

## Layer 2 conferral (independent, not deferral)

Layer 2 reached the same fail-to-produce call from its own density-level R3 mean-field recurrence, supplying the generative reason Layer 1's read only described: the becoming-active transition re-injects the q-dependent birth source every tick, so independent turnover shortens residence time without removing live coupling — hence `rho` lifted, exposure live, persistence sign held. Two corrections accepted on the merits:
- Scope-word: Layer 1's "signed through to the endpoint" was loose. Under R3, `theta_turnover = 0.50` only halves `s_Lambda` (0.40 -> 0.20 net persistence); the ladder reaches NO floor or degeneracy endpoint. Correct scope is "fails for the predeclared R3 grid," not an exhaustive mechanism-class closure.
- Label: the observable-decoupling finding is more precisely "single-axis turnover sensitivity with persistence-sign retention," with an order-parameter reading (persistence tracks where activity is regenerated across the window, robust to site churn; meanI tracks the instantaneous configuration, puncturable). Fenced from L4.

## Two forks (Mike arbitrated, via L2 conferral)

- Fork 1 — stronger-turnover endpoint extension: (a) record as named-not-triggered and HOLD. Live as a coherent possible probe (ladder reached theta=0.50 without degeneration) but not seeded. "Triggered" = eligible for Mike's later opening, not auto-seeded. An absolute-lifetime variant would be an endpoint-extension VARIANT, named as such, not run silently as the same R3 grid.
- Fork 2 — close or rest: REST, not close. Strongest warranted claim is the scoped negative for the R3 grid; the broader turnover-limited mechanism class stays open only to the extent the unreached endpoint warrants. Direct analogue of the Rule C first-pass rest on A-prime.

## Errors / precision (this session)

- Layer 1's "endpoint" wording (corrected above) is recorded as a real scope overreach caught by Layer 2's pessimism-on-passing, not glossed. The corrected scope is the one in the findings file.
- No fence leak found in the R3 realization (Layer 2 confirmed: theta_turnover exogenous and neighbor-independent; survival neighbor-blind so no Rule B collapse; becoming-active coupling unchanged; synchronous update with no same-tick re-entry; no observable/rho feedback).

## State at close

- HEAD at this ops-log commit, origin current after push, tree otherwise clean (untracked `read_obs001_nearnull_scale.py` at root unchanged).
- `cycle3/wave_two/rule_d/RULE_D_R3_FINDINGS.md` placed canonical (BOM-less, single trailing LF, 10466 bytes, byte-state verified at destination).
- Rule C first pass still rests on A-prime; Comparator 0 / epsilon floor findings unchanged; weak-form Rule B prior untouched; L4 ontological question rides forward unsettled (the single-axis finding touches it but does not resolve it).
- NEXT STEP: anchor refresh to record Rule D R3 rest + the named-not-triggered follow-up, and a next-session instantiation prompt, at Mike's discretion. Seeding of any further probe (the endpoint extension or any other) remains Mike's call to open.

Drafting partner: Layer 1 (Claude).
