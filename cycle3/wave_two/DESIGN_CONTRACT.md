# Wave-two design contract (canonical)

**Status:** CANONICAL. Accepted by Mike 2026-05-31 and placed at `cycle3/wave_two/DESIGN_CONTRACT.md`. This is the placed form of review-draft v4 (the draft line v1->v4 is in session history; the function form fixed "within the review-draft line" in v4 is now canonically fixed by this placement). NOT seeded — no wave-two probe is seeded from this contract; seeding is a separate step, Mike's call to open. Next actions on the wave-two path (Section 10): set grid density against the realized-contrast scale; run Comparator 0 then Comparator epsilon; then seeding.

**Phase:** Cycle 3 wave two, design phase. Opened by Mike 2026-05-31 under the conferred-and-arbitrated scope in `cycle3/RESUME_2026-05-30.md`.

**Inherited locks (unchanged):** topology 50x50 Moore radius 1 toroidal; SS-001 earned-window criterion; `LOW_Z_THRESH` = 2.0; the co-equal pair `Psi_meanI_state` / `Psi_persistence_I`, neither named theoretical Psi; the L4 ontological question rides forward unsettled and is NOT resolved by anything here.

---

## 1. The load-bearing question (carried from the arbitrated scope)

NOT "which rule produces low/low." The question is whether a lifted, non-degenerate activation-density regime can be produced WITHOUT per-tick spatial organization or clustered persistence being structurally forced by the update rule — i.e. whether low/low is a genuine earned regime inside a mechanism family that is ALSO capable of producing non-low/low signed regimes, rather than the sole behavior a rule was built to emit.

The design must produce a behavioral map across Rule C's parameter space first, and locate a low/low region inside that map second. A low/low-targeted sweep is the failure mode this contract is built to avoid.

## 2. The instrument: Rule C (contagion / divergence on the becoming-active transition)

Rule C places a single signed coupling coefficient kappa on the **becoming-active** transition, as a function of the fraction of active neighbors. Distinct in mechanism class from Rule B's neighbor-conditioned **survival** (staying-active). Placing divergence on the becoming-active side is the architectural choice that makes Rule C a different mechanism class, not a re-parameterized Rule B.

### 2.1 Function form (canonical; Layer 2-arbitrated)

    p_become,i = sigma( logit(p_Lambda,i) + kappa * g(q_i) )

q_i = n_i / 8 is the active-neighbor fraction; p_Lambda,i the Lambda-only becoming-active probability; g(q) = 2q - 1 a fixed centered monotone transform; sigma the logistic function. Committed property: **coefficient-null separability** — at kappa = 0, p_become,i = p_Lambda,i exactly, no residual neighbor dependence. Positive kappa contagion-dominant, negative divergence-dominant. Fixed centering makes kappa a pure local-contrast term, separating Lambda-driven lift from neighbor-driven organization.

### 2.2 Reserved audit form (Layer 2-originated; not canonical)

    p_become,i = p_Lambda,i + tanh(kappa) * r(p_Lambda,i) * (2 q_i - 1),  r(p) = min(p, 1 - p)

Exact Lambda-only at kappa = 0; deployed only if wave-two results look curvature-driven. An audit, not the center.

## 3. Construction fences

### 3.1 Coupling-sign-through-zero is NOT mu(rho) = 0

kappa = 0 is a per-cell substrate update parameter and the knob that lets the instrument reach signed regimes. NOT an operationalization of the point(s) at which mu(rho) = 0; any correspondence is construction, not finding. The writeup must never treat the kappa = 0 sweep point as the point(s) at which mu(rho) = 0.

### 3.2 Fence-integrity constraints (Layer 2-arbitrated; the fence holds under 2.1 but is fragile)

Prohibited in the instrument: kappa depending on current global rho; the centering term dynamically set to current rho (use FIXED g(q) = 2q - 1); the Lambda baseline containing any hidden rho->Psi or observable-feedback term; a piecewise-different function for kappa > 0 and kappa < 0; treating the kappa = 0 sweep point as the point(s) at which mu(rho) = 0.

### 3.3 Survival must not become a hidden range-bound stabilizer (Layer 2-originated)

Rule C may be monotone in active-neighbor fraction on becoming-active, but the staying-active transition must NOT acquire neighbor-count or range dependence, even indirectly, or Rule C collapses back toward Rule B and the distinct-mechanism-class claim fails.

## 4. The four-way discrimination (contrastive success criterion)

A low/low result is earned only if the design distinguishes these at the point of observation, by where the result sits in the behavioral map:

1. **Trivial-stochastic** — rho lifts, per-cell activity is locally independent noise; near-null because nothing is locally coupled. Comparator 0 (Section 6) is the reference.
2. **Rule-forced** — kappa set where it cannot organize; near-null is a construction artifact.
3. **Degenerate** — rho lifted but outside earned eligibility; SS-001 window not met.
4. **Substantive-candidate** — lifted, non-degenerate, earned windows, both observables near-null, under a kappa whose NEIGHBORING settings produce signed regimes.

Item 4's last clause is the spine: a substantive low/low is BRACKETED by non-low/low signed regimes. An unbracketed low/low does not clear the criterion however clean its near-null observables.

## 5. Behavioral-map reach requirement

The Rule C parameter family must demonstrably produce, somewhere in the sweep, all of: positive `Psi_meanI_state` / negative `Psi_persistence_I` (reachable from the contagion-dominant side); positive `Psi_meanI_state` / positive `Psi_persistence_I` (required as a REACHABLE regime); near-null / near-null (the low/low candidate region); degenerate / failure endpoints.

If the sweep cannot reach the signed regimes, any low/low it emits is rule-forced (Section 4 item 2); reach is a precondition of reading a low/low result.

**Large-|kappa| treatment (Layer 2-arbitrated).** Logistic curvature can make the rule near-threshold at high |kappa|, where signed regimes could come from probability saturation rather than substrate response. Large-|kappa| is an endpoint / degeneracy probe, NOT the evidentiary center.

### 5.1 Sharpened reach target from wave-one primary source (target sharpened by absence; NOT a prediction)

The wave-one CSV read (2026-05-31, `cycle3/data_out/c3_obs_001_results.csv`, 300 rows) establishes as primary-source fact: of the 97 non-degenerate-lifted rows, `Psi_meanI_state_z` is positive on all 97 (min ~139), with ZERO near-null and ZERO negative. The entire wave-one lifted, non-degenerate population under Rules A/B lacks lifted-near-null meanI. (Dual-degeneracy precision note confirmed in the same read: 125 rows fire both degeneracy flags; the 97 is the reconciled non-degenerate-lifted population.)

This sharpens — does NOT answer — the reach requirement. Wave one tested neighbor-conditioned-SURVIVAL rule families; Rule C acts on becoming-active. So:

- What wave one establishes: a strong absence for the tested neighbor-conditioned-survival families, and therefore a sharpened diagnostic target for wave two — sustained lifted rho may be hard to decouple from positive per-tick spatial organization under locally coupled update rules.
- What wave one does NOT establish: whether a becoming-active contagion/divergence rule can or cannot reach lifted-near-null meanI. It has no standing for a directional prediction about Rule C's reachable regimes. Hardening the absence into "Rule C probably cannot reach it" would collapse the mechanism-class distinction wave two is designed to test.

The near-null/near-null corner is the **diagnostically sharp** corner for wave two because it is the one wave one demonstrably did not reach under the tested neighbor-conditioned-survival rules. This is a target sharpened by absence, not a prediction of Rule C difficulty (hard for wave-one survival rules; not known hard for Rule C). Whether a becoming-active contagion/divergence rule can decouple lifted rho from positive `Psi_meanI_state_z` remains open — if Rule C reaches it, that is the substantive content of the becoming-active mechanism class; if it cannot, that is a finding about the rule, not assumed in advance.

## 6. The stochastic comparator(s) — split into a floor and an audit

**Apparatus-scope note.** The arbitrated wave-two scope (`cycle3/RESUME_2026-05-30.md`) names "a Lambda-driven weakly-coupled stochastic comparator," singular. This contract splits it into two objects on Mike's arbitration (2026-05-31), prompted by Layer 2's finding that a single weakly-coupled comparator calibrated to hold meanI near-null is circular (near-null by selection against the band it is meant to floor). This is a design-phase refinement of the arbitrated scope. On placement of this contract, the anchor's wave-two section is touched to reflect the split so a future instance does not read the singular-comparator scope as current and flag this contract as drift.

Both objects are SEPARATE processes from Rule C, sharing no machinery with the instrument they calibrate. Activation is driven by exogenous Lambda. Both have low evidentiary weight on their own; they calibrate, they do not produce candidates.

### 6.1 Comparator 0 — Lambda-only floor

No neighbor term at all. Activation driven by exogenous Lambda as a per-cell independent probability. Calibration: tune the Lambda baseline ALONE so the comparator reaches lifted, non-degenerate rho — the criterion is rho-lift and non-degeneracy, NOT any observable z-score. Then run it and RECORD `Psi_meanI_state_z` and `Psi_persistence_I_z` as observed outputs.

This is the clean trivial-stochastic floor: no local mechanism whatsoever, so whatever it produces is what lifted independent activation produces under this apparatus. Its reading answers the question Comparator 0 exists for:

- If lifted Lambda-only activation gives near-null / near-null, the trivial-stochastic floor is valid and supplies the reference for Section 4 item 1.
- If lifted Lambda-only activation ALREADY gives positive meanI, then near-null is NOT the default floor for lifted density under this apparatus — a finding (consistent in shape with the wave-one meanI absence), NOT a tuning failure to be corrected by targeting the z-band.

### 6.2 Comparator epsilon — weak-neighbor audit

A small FIXED neighbor term added to Comparator 0, included only as an audit perturbation around the floor — NOT itself the floor. Its magnitude is set by a predeclared coupling-weakness ceiling independent of any observable z-score:

    define realized neighbor contrast  delta_p = p(q=1) - p(q=0)
    admissible iff  |delta_p| <= epsilon * pbar_Lambda

where pbar_Lambda is the Lambda-only activation probability scale and epsilon is FIXED before observing `Psi_meanI_state_z`. The comparator is calibrated against coupling weakness (the realized neighbor contrast ceiling), never against the meanI z-band. `Psi_meanI_state_z` is recorded as an output, not a tuning target. Its reading:

- If weak epsilon perturbation keeps near-null / near-null, the floor is stable to minimal local coupling.
- If weak epsilon perturbation generates positive meanI, the apparatus is highly sensitive to local coupling and the comparator should NOT be used as a simple near-null floor — a finding, not a failure.

### 6.3 Why the split resolves the circularity

The single-comparator review-draft wording ("tune the magnitude so the comparator lifts rho while holding `Psi_meanI_state_z` inside +/-2.0") was circular: it made the comparator near-null by selection against the same near-null criterion it was later meant to floor, so it reported only what magnitude was chosen to satisfy the band, not what weakly-coupled lifted activity naturally produces. The split removes the circularity by making near-null meanI an OUTPUT at both objects: Comparator 0's calibration target is rho-lift alone, Comparator epsilon's is a predeclared realized-contrast ceiling. Neither tunes against the z-band. The comparator near-null scale on the meanI axis is therefore not "set" from wave one at all — it is OBSERVED from Comparator 0; the wave-one persistence near-null band (6 rows, z ~ -1.85 to -0.06, mean ~ -1.43) is the primary-source cross-reference for the persistence axis only.

## 7. Sweep structure and run record

- **Seeds:** 42, 137, 256, 1024, 31415 (same as wave one).
- **Aggregation:** per-(rule, parameter-setting, seed) boolean flag counts. NOT per-parameter means.
- **Realized-contrast tracking (Layer 2-arbitrated):** the run record tracks the realized becoming-active probability contrast p(q=1) - p(q=0) alongside kappa, so a low/low result cannot hide behind a nominally-nonzero kappa whose function flattened the real neighbor effect. (The same realized-contrast quantity defines Comparator epsilon's admissibility ceiling, Section 6.2 — one consistent measure across instrument and comparator.)
- **Grid density:** the kappa grid (range and spacing) is set against where the realized contrast saturates (the large-|kappa| degeneracy boundary, Section 5), denser near zero. Set before seeding; informed by the realized-contrast scale, not silently chosen.

## 8. Weak-form Rule B prior (preserved, not hardened)

Rule B structural overproduction of positive `Psi_meanI_state` when it sustains lifted rho is the best WORKING PRIOR — NOT proven by construction. The wave-one read (Section 5.1) is consistent with the prior but does not convert it to proof: it shows A and B coincided lifted-rho with organized meanI, which is the prior's content, not an independent confirmation. The door to Rule B stays open. Candidates produce or fail to produce; they do not confirm or demonstrate.

## 9. What this contract does NOT do

- Does not seed any probe.
- Does not "set" the comparator meanI near-null scale; that is OBSERVED from Comparator 0 (Section 6).
- Does not set grid density (set before seeding, informed by realized-contrast scale, Section 7).
- Does not predict whether Rule C reaches lifted-near-null meanI (held open, Section 5.1).
- Does not resolve the L4 ontological question, and nothing in wave two resolves it by statistical robustness or by which observable a script names.
- Does not harden the weak-form Rule B prior (Section 8).

## 10. Routing sequence from here

1. Set grid density against the realized-contrast scale.
2. Run Comparator 0 (Lambda-only): record whether lifted independent activation gives near-null observables under this apparatus. Run Comparator epsilon as the weak-coupling audit around it.
3. Seeding is Mike's call to open.
