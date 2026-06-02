# Operations log â€” 2026-06-01 wave-two Comparator epsilon run

**Session:** Cycle 3 wave two, design phase. Comparator epsilon scope settled, magnitude set, implemented, run, and committed.
**Layer:** Layer 1 (Claude) drafting/routing; Layer 2 (ChatGPT) mean-field review; Layer 3 (Gemini) Mesa implementation; Mike sole execution channel and arbiter.
**Opened from:** HEAD 28ca2d9 (Rule C M2 ops log; the run-arc continued in the same working session).
**Closed at:** HEAD 208b5c2, origin current.
**Outcome:** Comparator epsilon committed (script + CSV + 10 NPZs + findings note); floor stable to weak coupling, supporting the A-prime floor-adjacent language; NO further probe seeded.

Fourth 2026-06-01 ops entry (distinct slug from preseeding-resolution, comparator0-run, rule-c-m2-run).

---

## Sequence

Mike opened Comparator epsilon. Layer 1 routed a scope question to Layer 2 (is epsilon the contract's separate-process object (a), or did A-prime reframe it into a Rule C near-zero densification (b)?). Layer 2 returned (a), correcting its own A-prime wording. Layer 1 then set the magnitude in-sandbox, routed it to Mike, specced to Layer 3, reviewed, ran, read, and committed. Detail below.

## Scope resolution (Layer 2 -> object a)

Layer 1 flagged a tension between two committed statements: the contract Section 6.2 (epsilon = separate weak-neighbor process, authored before the Rule C run) and A-prime's "epsilon bounds the weak-coupling floor zone" (authored after, readable as Rule C densification). Routed both readings to Layer 2 without pre-deciding. Layer 2 resolved: **epsilon is object (a)**, the separate weak-neighbor comparator; A-prime's wording was too compressed and is corrected to mean the separate-process floor audit, NOT Rule C densification. Object (b) (Rule C near-zero densification) survives as a separate optional follow-up, NOT called epsilon, opened only at Mike's call. The two ceilings kept distinct: Comparator epsilon ceiling (separate-process perturbation scale) != Rule C near-zero boundary (Rule C realized-contrast axis) â€” related calibration facts, not interchangeable. Epsilon calibrates the LANGUAGE "floor-adjacent"; it cannot reclassify Rule C rows or move the Rule C thresholds.

## Magnitude (Layer 1 in-sandbox, Mike ratified)

The contract fixes the ceiling FORM (|delta_p| <= epsilon * pbar_Lambda, epsilon fixed before any z-score, per-anchor pbar_Lambda) but not the value. Layer 1 computed candidate epsilon values in-sandbox against the standard "realized contrast unambiguously below the Rule C smallest setting |c|=0.05." Proposed **epsilon = 0.05**, giving per-anchor realized-contrast ceilings 0.0100 (Lambda=0.20) and 0.0200 (Lambda=0.40) â€” both decisively below 0.05. Surfaced the per-anchor-vs-equal-contrast fork: (a) honor the contract form (ceiling = epsilon*pL, realized contrast differs across anchors), (b) equalize contrast like the Rule C grid. Mike ratified epsilon = 0.05 and **choice (a)** (honor the contract form; per-anchor unequal contrast is correct for a per-density floor-sensitivity audit). Layer 1 then computed the additive coefficients a = ceiling/2 = 0.00500 (0.20) / 0.01000 (0.40), verified realized delta_p = 2a hits the ceiling exactly with no clipping.

## Implementation (Layer 3) and Layer 1 review

Specced epsilon to Layer 3: contract object (a), additive form p_become = clip(p_Lambda + a*g(q), 0, 1) (deliberately distinct from Rule C's logit-linear coupling), g(q)=2q-1 fixed, per-anchor coefficients as precomputed constants, survival Lambda-only (no neighbor term), no LowLow flag (floor not candidate), fixed-rho-0.10 init (has a transition rule), apparatus parity, the binding two-ceilings reading-constraint carried into the docstring. Layer 3 returned a script; Layer 1 reviewed against spec and wave-one substrate, verified in-sandbox: additive form realizes ceiling exactly at both anchors (no clipping), coefficients correct, survival neighbor-independent (fence holds), a=0 reduces to Comparator 0, LowLow absent, 10 NPZs. No apparatus/fence/scope objection. The shared-rand_grid for becoming/staying (same as Rule C) re-scrutinized and clean: survival threshold p_Lambda carries no neighbor information. No Layer-1 edit needed (NPZ save already enabled by Layer 3). No L2 consult before running â€” clean implementation of an already-arbitrated object.

## Run

Placed reviewed script to Downloads (single clean source, 14534 bytes). Ran under canonical venv (verified $env:VIRTUAL_ENV), cwd at repo root, exit 0 (pre-flight + parity passed). Small run (2 anchors x 5 seeds = 10 runs through the null), a few minutes. Wrote CSV (20 rows) + 10 NPZs.

## Read

All 20 rows: realized_delta_p = 0.0100 / 0.0200 (matches ceiling); lifted and non-degenerate; meanI-z and persistence-z centered near zero at both anchors, no systematic sign drift. Two isolated marginal exceedances over 2.0 (meanI Lambda=0.40 seed137 win75 at +2.36; persistence Lambda=0.20 seed31415 win0 at +2.09) â€” both isolated, non-replicated within group, no signed partner; finite-sample tail, inspect-not-halt. Finding: the apparatus floor remains near-null / near-null under the minimal perturbation at both anchors. This is the outcome Layer 2 PRE-SPECIFIED in A-prime as the supporting case, so it SUPPORTS the A-prime language that the Rule C near-zero band is floor-adjacent weak-coupling tolerance. Recorded as confirmation of an anticipated reading, not a new arbitration (hence commit-with-note + Layer 2 update, not a fresh consult â€” Mike's call). Binding constraint held: does not reclassify Rule C, does not move thresholds, ceilings kept distinct. Object (b) NOT motivated (floor stable, not sensitive).

## Commit

Findings note authored (`cycle3/wave_two/COMPARATOR_EPSILON_FINDINGS.md`, BOM-less single LF) attributing the supporting reading to A-prime's pre-specification, holding the two-ceilings constraint, noting object (b) unmotivated. Script homed in `cycle3/wave_two/`. Staged by explicit pathspec: two named files + CSV + directory-scoped NPZ glob; verified staged count 13 (= 3 + 10) and confirmed the three non-NPZ entries by name. Commit 208b5c2 (13 files, create-mode). Push confirmed `28ca2d9..208b5c2  main -> main`.

## State at close

- HEAD 208b5c2, origin current, tree otherwise clean (untracked read_obs001_nearnull_scale.py at root unchanged).
- Wave-two design phase open; contract frozen at a925475. Committed wave-two artifacts: pre-seeding resolution (ff7a904), Comparator 0 (8abb917), Rule C M2 map + findings (d150de7), Comparator epsilon + findings (208b5c2), plus ops logs.
- The three wave-two instruments are run and read: Comparator 0 (i.i.d. floor near-null), Comparator epsilon (floor stable to weak coupling), Rule C M2 (reach satisfied; low/low floor-adjacent, not substantive â€” A-prime). The near-null/near-null region is the floor and its weak-coupling neighborhood, confirmed from two independent directions; the Rule C near-zero band sits within it.
- NO probe seeded beyond these; seeding remains Mike's call. Weak-form Rule B prior untouched.
- Held / optional follow-ups (Mike's call, none motivated by current results): Rule C near-zero densification (object b â€” not motivated, floor stable), reserved audits Lambda=0.30 / 0.50, grid densification +/-0.025 / +/-0.92.
- L4 ontological question rides forward unsettled.
- Pending non-blocking: Layer 2 UPDATE on the epsilon result (commit-with-note path; result matches A-prime's pre-specified supporting case â€” update, not consult).

Drafting partner: Layer 1 (Claude).
