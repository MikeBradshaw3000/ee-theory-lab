# Operations log â€” 2026-06-01 wave-two Comparator 0 run

**Session:** Cycle 3 wave two, design phase. Comparator 0 (Lambda-only apparatus-null floor) implemented, reviewed, run, and committed.
**Layer:** Layer 1 (Claude), drafting and routing; Layer 2 (ChatGPT) mean-field review; Layer 3 (Gemini) Mesa implementation; Mike sole execution channel.
**Opened from:** HEAD ba9517b (pre-seeding resolution memo + its ops log committed earlier same day).
**Closed at:** HEAD 8abb917, origin current.
**Outcome:** Comparator 0 script + results committed; apparatus-null floor established by observation; NO Rule C probe seeded.

This is the second 2026-06-01 ops entry (distinct slug from `2026-06-01_wave-two-preseeding-resolution.md`).

---

## Sequence

Cold-start grounding clean (HEAD ead9c08 at session open, before the day's two prior commits). Read anchor and contract. Layer 2 directed opening only the pre-seeding resolution substep (Comparator 0 first, then kappa-grid in realized-contrast space, seeding held closed); Mike concurred. Resolution memo drafted, placed (ff7a904), ops-logged (ba9517b). Then Comparator 0 was routed to Layer 3, reviewed, corrected, consulted to Layer 2, run, and committed â€” detail below.

## Layer 3 implementation and Layer 1 review

Routed Comparator 0 to Layer 3 as a self-contained note ("what the run will produce"; Lambda-only; rho-lift / non-degeneracy the sole calibration target; observables as outputs; L3 never declares its own clearance). The Lambda baseline parameterization was left to L3 on rho / SS-001 grounds, surfaced to Mike as latitude rather than handed a number.

Layer 1 reviewed L3's first delivery against the committed wave-one substrate `cycle3/c3_obs_001_battery.py` (pulled and diffed directly, not from memory). Observable math (`calculate_morans_i_toroidal_8`, `batch_morans_i_toroidal_8`, both nulls) was byte-for-byte parity; an initial Layer-1 worry about the in-loop null draws off the global RNG was WITHDRAWN after reading the wave-one code, which does exactly the same â€” matching the convention is the requirement. Four defects survived contact with the record and were routed back as a correction note:

1. (disqualifying) degeneracy apparatus missing â€” `VAR_EPSILON = 1e-3`, `mean_active_state_variance`, `persistence_std`, `extinction_degenerate`, `saturation_degenerate` absent; "non-degenerate" is load-bearing in the protocol. Restored verbatim. `LowLow_Nondegenerate_Candidate` deliberately NOT emitted (Comparator 0 is a floor, not a candidate).
2. (disqualifying) parity asserted in a docstring, not tested â€” restored the runtime `run_parity_check()` against the battery modules plus pre-flight env guards (sufficiency-tested-not-asserted).
3. CSV column parity â€” restored the wave-one diagnostic columns, swapped `rule`/`lambda_id` for `Lambda`, omitted the candidate flag and rule-specific tick diagnostics.
4. initial-condition departure named, not silent â€” Comparator 0 has no transition rule, so rho is exogenous at Lambda from tick 0 (the stationary distribution), a floor-appropriate departure from wave one's fixed-rho-0.10-then-evolve init.

L3 returned a corrected script addressing all four; Layer 1 confirmed the corrections line-by-line (VAR_EPSILON present, both degeneracy flags recorded, parity check called before sweep, LowLow absent, clean single-draw init loop) and had no remaining apparatus objection.

## Layer 2 pre-run consultation (continuing context)

Before the run, consulted Layer 2 on whether the BUILT object honored the split, on three points. Layer 2's read: the build honors the split, with corrections that sharpened the reading (taken, not deferred to):

- **Lambda sweep** {0.10..0.50} accepted as clean floor-documentation across density levels, not tuning (Lambda admitted on rho-lift / non-degeneracy grounds only; z-scores never used to select Lambda). Caveat recorded: do NOT collapse the Comparator 0 floor-atlas job and the downstream Rule C baseline-scale job; the kappa-grid / realized-contrast design may still need one or more accepted Lambda baseline scales later.
- **Near-null-by-construction reframe** made canonical-in-reading: Comparator 0 is primarily an apparatus-null-behavior calibration under lifted i.i.d. input, NOT a substantive floor for candidate mechanisms. It establishes the Section 4 item-1 trivial-stochastic reference (defined narrowly as lifted rho with locally independent activity) and nothing wider. Comparator epsilon, not Comparator 0, tests sensitivity to weak nonzero local coupling. Not circular: nothing is tuned against the z-band; the process is specified independently of the observables.
- **Stop condition** refined: halt downstream INTERPRETATION (not execution forever, not re-tuning) only on a SYSTEMATIC, repeated signed pattern across eligible rows. A single marginal |z|>2 is expected finite-sample tail behavior â€” inspect, don't halt. The read is whether the z-distribution is centered near zero with no systematic sign drift, not merely whether every row sits inside LOW_Z_THRESH.

## Run

Placed the reviewed script to Downloads, confirmed single clean source by size (12617 bytes). Ran under the canonical venv (`& Activate.ps1`; verified `$env:VIRTUAL_ENV`) with cwd at repo root (relative `cycle3/...` paths + parity-check import resolve from cwd). First run attempt died on a PowerShell parser error (the if/else | Set-Clipboard scope bug â€” pipe attached to the else brace; the script never executed); recovered by building `$msg` in a variable and piping after the if/else. Re-run completed exit 0 (pre-flight + parity both passed, since they raise on failure). CPU confirmed climbing across two checks (273 -> 307 -> 486 s) to rule out an import hang; the meanI-state permutation null is the cost driver. CSV written to `cycle3/data_out/c3_w2_comparator_0_results.csv`, 75 rows (5 Lambda x 5 seeds x 3 windows).

Noted for the horizon (NOT acted on): the meanI-state null does a full (100x2500) argsort 199x per window; if Rule C's kappa sweep runs many more settings, this is a possible optimization target for the instrument runs â€” correctness is fine, it is a cost note only.

## Read (against Layer 2's criterion)

- All 75 rows lifted and non-degenerate (no extinction, no saturation anywhere). Lambda=0.10 rows mostly not Steady_State_Candidate (rho_range_over_mean ~0.27-0.37 over the 0.25 threshold â€” expected at low density); still eligible lifted-non-degenerate floor readings. Lambda>=0.20 steady almost everywhere.
- meanI-z centered near zero, bulk within +/-1, range ~[-1.83, +2.06]. ONE row over 2.0 (Lambda=0.50, seed 42, window 25 at +2.063) â€” isolated marginal exceedance, inspected (no neighbor windows in its group exceed; its persistence-z is unremarkable at +0.56), read as finite-sample tail per Layer 2, NOT a halt.
- persistence-z centered near zero, range ~[-1.94, +1.96], ZERO rows over +/-2.0. No systematic sign drift on either axis across Lambda or seed.

Reading: top row of Layer 2's severity table â€” both axes near-null across eligible Lambda; apparatus-null behavior well-behaved; the null convention correctly registers genuine i.i.d. input as near-null and does NOT manufacture structure from noise; Section 4 item-1 reference is sound. The expected-and-now-observed near-null, established by observation rather than assumed. Nothing halts; no re-run, no re-tune.

## Commit

Script homed in `cycle3/wave_two/` (per the anchor's intent for that subdir; Mike's call); CSV in `cycle3/data_out/`. Verified script size at destination (12617) and CSV presence before staging. Staged both with explicit paths; `git diff --cached --name-only` confirmed exactly the two files. Commit 8abb917 (2 files, create-mode). Push confirmed `ba9517b..8abb917  main -> main`.

## State at close

- HEAD 8abb917, origin current, tree otherwise clean (untracked `read_obs001_nearnull_scale.py` at root unchanged).
- Wave-two design phase open; contract frozen at a925475; pre-seeding resolution at ff7a904; Comparator 0 committed at 8abb917.
- Comparator 0 result: apparatus-null floor sound by observation; Section 4 item-1 reference established; meanI near-null scale now OBSERVED (not set from wave one). Interpretive finding deliberately NOT formalized in a canonical findings note this session (Mike's call) â€” to be formalized at the next anchor refresh or when it feeds the kappa-grid baseline-scale step, where Layer 2's floor-atlas-vs-baseline-scale caution bites.
- NO Rule C probe seeded. Seeding remains Mike's call to open.
- Remaining wave-two path: set kappa-grid density against the realized-contrast scale (using one or more accepted Lambda baseline scales, kept distinct from the floor atlas); then Comparator epsilon as the weak-coupling audit; then seeding.
- L4 ontological question rides forward unsettled.

Drafting partner: Layer 1 (Claude).
