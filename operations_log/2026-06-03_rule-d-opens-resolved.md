# Operations log — 2026-06-03 Rule D opens D-1/D-2/D-3 resolved

**Session:** Cycle 3 wave two. The three Rule D downstream design opens left by the contract (Section 7) were resolved against the realized scale and placed canonical at cycle3/wave_two/rule_d/D_OPENS_RESOLUTION.md. The D-1 theta-grid time-scale calibration was routed to Layer 2 and concurred. NO probe seeded; next step is Layer 3 implementation.
**Layer:** Layer 1 (Claude) reading primary source, drafting, routing; Layer 2 (ChatGPT) mean-field review of the D-1 calibration only; Mike sole execution channel, arbiter, and router. Layer 3 not yet engaged.
**Opened from:** HEAD 2d9cbb4 (anchor re-point to Rule D arc).
**Closed at:** HEAD 84e4cd9, origin current.
**Outcome:** Rule D opens resolution canonical (1 file, 72 lines). D-1/D-2/D-3 fixed; design phase moves to Layer 3 implementation.

---

## Sequence

Grounding from the anchor + Rule D contract confirmed HEAD current at 2d9cbb4 (the anchor's supersession-header hash 95ee9a8 lags the tip; the later commits — contract placement 4a8a688, its ops log a0d8282, anchor re-point 2d9cbb4 — are consistent with the anchor body, so the body governs and we are current). Layer 1 led the first design framing across all three opens, then read primary source (Rule C M2 findings file, then a targeted slice of the M2 CSV) before finalizing. D-2 and D-3 settled directly from the M2 map. D-1 carried a genuine uncertainty (time-scale calibration) that was routed to Layer 2, concurred, and folded in. Resolution memo placed canonical at Mike's call; ops log committed alongside per standing rule.

## The three opens, resolved

- **D-1 — theta_turnover grid:** {0, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50}. Seven settings; theta=0 the pure-Rule-C signed reference, 0.50 the churn/floor endpoint.
- **D-2 — responsive coupling:** matched pair c = -0.35 and c = +0.35 (realized_delta_p +/-0.35), both signs, held fixed across the full theta ladder. One magnitude, both signs (D-2(b)).
- **D-3 — Lambda anchor:** 0.40 only (D-3(a)).

Design space: 7 theta x 2 kappa x 5 seeds = 70 run-settings on the inherited 5x25-tick window structure. Arbitrated by Mike as D-1(a) x D-2(b) x D-3(a).

## Primary-source reads behind the resolution

The M2 findings file gave the kappa-axis scale in full but not the theta-axis (turnover) scale, so a targeted M2 CSV slice was pulled (Lambda=0.40, responsive settings + kappa=0 reference, key columns only). Reads:

- Window length 25 ticks, run length 125 ticks (5 windows: starts 0/25/50/75/100). An early two-row glance had suggested 50 ticks; the fuller slice corrected this to 125.
- At Lambda=0.40, mean_rho is near-stationary across the responsive band (~0.42 at negative coupling down to ~0.35 at c=+0.5), third/fourth-decimal jitter across seeds and windows, nowhere near the extinction floor (contrast Lambda=0.20 c=+0.8 -> rho~0.02). This is the floor headroom D-3 requires; 0.40 selected over 0.20 (near-extinction under positive coupling) and over promoting reserved 0.30/0.50 (unnecessary for first pass).
- c=+/-0.35 is solidly signed both axes/both signs, non-degenerate (persistence-z ~-5 to -6 at -0.35, ~+6 at +0.35; extinction/saturation flags False; rho ~0.37-0.42), clear of the |c|<=0.10 floor-adjacent zone and the |c|=0.8 degenerate endpoint. Both signs run to read turnover-suppression sign-symmetry directly.
- rho_range_over_mean ~0.8-1.2 in window 0, collapsing to ~0.10-0.15 for windows 25+ — the substrate settles within roughly one 25-tick window and then holds, anchoring the organization time-scale at order ~25 ticks. This is the D-1 calibration anchor.

## D-1 routed to Layer 2 (calibration only; concurred)

The D-1 ladder rests on rho-stabilization as a proxy for the organization-formation time-scale. Layer 1 was not confident enough to commit on its own read, because rho-stabilization is not identical to organization-formation (rho is the k=0 mode; the observables are spatial/persistence organization measures, so relaxation modes can differ), and a mis-scaled ladder's worst case is discrimination failure reading as a false negative. That is a mean-field question, Layer 2's domain, so it was routed — a single self-contained calibration question, continuing context (Layer 2 holds full Rule D context from the contract review), no apparatus rebuilt, no contract concatenated.

Layer 2 verdict: commit the ladder as-is, do not shift lower or higher. Concurrence carried one load-bearing correction: the turnover hazard damps pair/persistence structure on a scale closer to 1/(2 theta), not 1/theta, because a pair-like correlation survives only if both relevant active sites survive. On that reading theta=0.02 is already a plausible first competition point for persistence organization against the ~25-tick anchor (1/(2*0.02)=25 ticks); the ladder spans longer-than / comparable-to / faster-than / endpoint-churn on both single-cell and pair-correlation readings. No 0.01 and no higher value added preemptively; both are named follow-ups conditional on first-pass behavior. This tightened the calibration rather than overturning it.

Convergence read: genuine independent engagement. Layer 2 supplied a mean-field correction (the 1/(2 theta) pair-correlation scale) Layer 1 did not have, while confirming the ladder placement. Not soft convergence — the answer could have come back "shift the ladder," and the routing existed precisely to catch that before a 70-setting run.

## Recorded-diagnostic addition (interpretation hygiene)

Layer 2 flagged that the {1/theta} lifetimes are turnover-ONLY; realized active-site lifetime is shorter if the base dynamics carry implicit deactivation. Surfaced as an explicit scope addition (not folded silently): the run record will preserve the set theta_turnover AND record realized active-site lifetime / churn rate as an output diagnostic, added to contract Section 8 alongside the 4.3 density-confound and 4.4 live-coupling-exposure metrics. Output only — no control, no feedback (the fence forbids theta_turnover adapting to any observed quantity). Not a new design requirement; does not change rule, fences, grid, or success criterion.

## Edits and placement

Resolution memo created via create -> present_files -> Mike Move-Item. Byte-state verified at generation (no BOM / single trailing LF / size 7645) and re-verified at destination (BOM False / last3=6E2E0A / size 7645). Downloads held a single candidate at 7645 (no stale same-named copy this time; size-match confirmed regardless). Staged by explicit pathspec; diff --cached one entry. Commit 84e4cd9 (1 file, 72 insertions). Vocabulary discipline held throughout (produce-or-fail-to-produce; theta_turnover not eta; no Regime_II; no LowLow-search justification of the grid).

## State at close

- HEAD 84e4cd9, origin current after push, tree otherwise clean (untracked read_obs001_nearnull_scale.py at root unchanged).
- Rule D opens D-1/D-2/D-3 RESOLVED and canonical at cycle3/wave_two/rule_d/D_OPENS_RESOLUTION.md. Grid: 7 theta x 2 kappa (c=+/-0.35) x Lambda=0.40 x 5 seeds = 70 settings. NOT seeded.
- Next step: Layer 3 (Gemini) implementation of Rule D against the resolved settings, framed as "what the run will produce"; Layer 3 never declares its own L2 clearance. After implementation + parity, seeding is Mike's call.
- Rule C first pass still rests on A-prime; Comparator 0 / epsilon floor findings unchanged; weak-form Rule B prior untouched; L4 ontological question rides forward unsettled.
- Anchor not yet updated to record the opens as resolved — flagged to Mike as the next housekeeping touch (pure pointer edit; Mike's call whether it needs its own ops entry).

Drafting partner: Layer 1 (Claude).
