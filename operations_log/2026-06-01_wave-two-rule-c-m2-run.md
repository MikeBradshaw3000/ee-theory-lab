# Operations log â€” 2026-06-01 wave-two Rule C M2 run

**Session:** Cycle 3 wave two, design phase. Rule C M2 baseline-scale/grid designed, implemented, run, arbitrated, and committed.
**Layer:** Layer 1 (Claude) drafting/routing; Layer 2 (ChatGPT) mean-field review; Layer 3 (Gemini) Mesa implementation; Mike sole execution channel and arbiter.
**Opened from:** HEAD ba9517b (Comparator 0 committed earlier same day).
**Closed at:** HEAD d150de7, origin current.
**Outcome:** Rule C M2 first-pass behavioral map committed (script + CSV + 150 NPZs + findings note); arbitrated reading A-prime (floor-adjacent weak-coupling low/low, not substantive candidate); NO further probe seeded.

Third 2026-06-01 ops entry (distinct slug from `2026-06-01_wave-two-preseeding-resolution.md` and `2026-06-01_wave-two-comparator0-run.md`).

---

## Sequence

After Comparator 0 (HEAD ba9517b), Mike opened the baseline-scale / kappa-grid step. Routed the anchoring design to Layer 2; Layer 2 returned M2 (two co-primary anchors). Layer 1 verified the grid math in-sandbox; routed the concrete grid values to Layer 2 for sign-off; routed Rule C implementation to Layer 3; reviewed and made one edit; ran; routed the map reading to Layer 2; committed under the arbitrated reading. Detail below.

## Baseline-scale / kappa-grid design (Layer 2 -> M2)

Routed Layer 2 the anchoring question: Design S (single baseline) vs M (multiple), with Layer 1's lean toward M stated as a lean (the contract's bracketing spine wants density-robustness, which S cannot give). Layer 2 returned **M2**: two co-primary anchors Lambda = 0.20 and 0.40, NOT all-baselines. 0.10 excluded (rho-variability, weaker anchor); 0.30 reserved as midpoint audit if anchors disagree; 0.50 reserved as centering/symmetry audit (g(q)=2q-1 makes half-density structurally special, so a 0.50-only low/low cannot carry first-pass weight). Layer 2's load-bearing construction point: the grid is **common in realized-contrast targets, NOT common in nominal kappa** â€” define shared c_j, invert to baseline-specific kappa at each anchor, so the anchors are comparable. Layer 2's reasons density is a substantive axis (not a rescaling): nonlinear endpoint-contrast in p_Lambda (slope ~2 p_Lambda(1-p_Lambda) near zero), density-dependent realized-q distribution, and Comparator 0's density-dependent rho-stability. Comparator epsilon forced to run at each primary anchor (per-baseline pbar_Lambda), structure not magnitude.

## Grid verification (Layer 1, in-sandbox, design-time)

Verified the inversion Delta_p(kappa; p_Lambda) = c_j at both anchors. Findings: Delta_p reaches 1.0 at both anchors (no solvability wall; Layer 1's earlier saturation-ceiling worry checked and WITHDRAWN). Near-zero slope confirmed at Layer 2's 2 p_Lambda(1-p_Lambda) (0.32 at 0.20, 0.48 at 0.40); 0.40 leaves the floor ~1.5x faster, so common contrast needs larger kappa at 0.20 â€” confirming common-in-contrast is load-bearing. Both anchors flatten above |Delta_p|~0.92 (kappa~4): the large-|kappa| degeneracy zone. Proposed c_j set and routed to Layer 2 for sign-off.

## Grid sign-off (Layer 2)

Layer 2 signed off as-is: c_j in {0, +/-0.05, +/-0.10, +/-0.20, +/-0.35, +/-0.50, +/-0.60, +/-0.80}, c_max=0.60 responsive ceiling, +/-0.80 sparse boundary/degeneracy probe (NOT presupposed to reach degeneracy â€” if it doesn't, that's a result), no +/-0.025 or +/-0.92 first-pass (densify only on conditional triggers; below 0.05 overlaps Comparator epsilon's job). kappa constants accepted as precomputed (4dp), realized_delta_p recorded per setting.

## Rule C implementation (Layer 3) and Layer 1 review

Routed Rule C to Layer 3 (Rule C only; not epsilon â€” Mike's call). Canonical form fixed, survival explicitly NOT neighbor-conditioned (two distinct transition probabilities, only becoming-active carrying kappa), kappa constants as precomputed (no scipy), all fences, mandatory realized-contrast tracking, fixed-rho-0.10 init (Rule C has a transition rule, unlike Comparator 0). Layer 3 returned a script; Layer 1 reviewed against the contract and wave-one substrate. Verified in-sandbox: survival neighbor-independent (mechanism-class fence holds); kappa=0 collapses exactly to Comparator 0 (separability); grid structure 15 settings/anchor, single zero, symmetric, kappa=0 separability exact. No fence or apparatus objection. ONE Layer-1 edit: enabled the commented-out NPZ state save (Mike chose option a, full auditability) and sanitized the NPZ filename (sign+4dp encoded m/p/_) â€” verified 150 unique collision-free names; only deviation from Layer 3's logic, data identical.

## Run

Placed reviewed script to Downloads (single clean source, 16282 bytes). First run attempt died on the if/else | Set-Clipboard scope bug AGAIN (Layer 1 error; pipe attached to else brace) â€” recovered by building $msg then piping after the branch. Re-run under canonical venv (verified $env:VIRTUAL_ENV), cwd at repo root, completed exit 0 (pre-flight + parity passed). ~40+ min wall-clock (150 runs x meanI-state null); CPU confirmed climbing to rule out hang. Wrote CSV (450 rows) + 150 NPZs to cycle3/data_out.

## Map reading (Layer 2 -> A-prime)

Read the CSV against the four-way criterion. Routed Layer 2 TWO readings without pre-deciding (Layer 1's lean A: near-zero low/low is the floor; literal-contract counter B: bracketed near-null band could clear item 4), explicitly flagging that Layer 1's own framing produced A and inviting independent test. Layer 2 returned **A-prime**, sharper than A: the map DID produce a lifted non-degenerate near-null band, so the phrasing is narrow â€” NOT "Rule C produced no low/low" but "no AWAY-FROM-FLOOR substantive low/low." Floor-adjacent weak-coupling low/low band, dissolving into signed regimes as coupling becomes responsive. Layer 2 corrected Layer 1's discriminating test: nonzero width is NOT the test (any continuous update has width near zero under hard LOW_Z_THRESH); the test is whether LowLow persists OUTSIDE the weak-coupling zone at realized contrast beyond epsilon-scale. First-pass threshold: |realized_delta_p| >= 0.20 is genuinely responsive, |c| <= 0.10 floor-adjacent. The map fires LowLow only through |c| <= 0.10 -> floor-adjacent, decisively not item-4. Four patterns that would make a substantive reading live recorded (none present). Comparator epsilon's role sharpened: formalize the weak-coupling floor zone, NOT retroactively rescue a candidate.

Reach result (positive content): signed regimes reached decisively at BOTH anchors (negative kappa -> positive meanI / negative persistence; positive kappa -> positive meanI / positive persistence; degenerate endpoint at 0.20 c=+0.8). Density-stable: both anchors same structure, no away-from-zero low/low pocket â€” M2 payoff delivered. Map-texture cautions fenced: 0.20 high-positive-kappa positive-meanI is on a collapsing population (degenerate-boundary, not clean signed regime); persistence-sign cross-anchor mismatch is downstream texture.

## Commit

Findings note authored (`cycle3/wave_two/RULE_C_M2_FIRST_PASS_FINDINGS.md`, BOM-less single LF), recording A-prime attributed to Layer 2 arbitration, the reach result, the discriminating test + threshold, the four future-pass patterns, epsilon's sharpened role, the map-texture cautions. Script homed in `cycle3/wave_two/`. Staged by explicit pathspec: two named files + CSV + directory-scoped NPZ glob (honors no `git add -A`); verified staged count 153 (= 3 + 150) and confirmed the three non-NPZ entries by name before commit. Commit d150de7 (153 files, create-mode). Push confirmed `6f9db70..d150de7  main -> main`, 16.29 MiB.

## State at close

- HEAD d150de7, origin current, tree otherwise clean (untracked read_obs001_nearnull_scale.py at root unchanged).
- Wave-two design phase open; contract frozen at a925475; pre-seeding resolution at ff7a904; Comparator 0 at 8abb917; Rule C M2 map + findings at d150de7.
- Rule C M2 first-pass: behavioral-map reach satisfied at both anchors; low/low floor-adjacent (|c| <= 0.10), density-stable; classified A-prime (Layer 2) as weak-coupling tolerance, NOT substantive candidate. A clean negative on the specific substantive-low/low question plus a positive reach result.
- NEXT instrument: Comparator epsilon â€” bounds the weak-coupling floor zone, runs at both primary anchors (per-baseline ceiling), formalizes the boundary; does NOT rescue a candidate by construction. Its magnitude is set after this map (now read); seeding remains Mike's call.
- Reserved audits if triggered: Lambda=0.30 (midpoint, if anchors disagree â€” they did not), Lambda=0.50 (centering/symmetry), +/-0.92 and +/-0.025 grid densification (conditional triggers, not met first-pass).
- L4 ontological question rides forward unsettled.

Drafting partner: Layer 1 (Claude).
