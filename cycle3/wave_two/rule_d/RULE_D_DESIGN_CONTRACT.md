# Rule D design contract — turnover-limited activation

**Status:** Layer 2-reviewed (mean-field coherence cleared; accepted with required precision amendments, all incorporated 2026-06-02: Section 2.3 update-order fence, Section 4.3 density-confound guard, Section 4.4 live-coupling exposure guard, Section 8 metrics, and wording amendments). Placed canonical 2026-06-02 (4a8a688); opens D-1/D-2/D-3 resolved 2026-06-03 (84e4cd9). AMENDED 2026-06-03 for R3 (Sections 2.2, 2.3, 6, 8): active-cell persistence is s_Lambda * (1 - theta_turnover), retaining Rule C's neighbor-independent Lambda-survival with theta_turnover as an ADDITIONAL independent churn hazard, so theta_turnover = 0 recovers Rule C exactly. The original survival-replacement form (persistence = 1 - theta_turnover) was corrected after Layer 3 implementation surfaced that theta_turnover = 0 saturates the lattice (no signed lower anchor); Layer 2 recommended the retain-survival form and confirmed it does not collapse toward Rule B (both factors neighbor-independent). No new Layer 2 pass required (Layer 2's recommendation supplied the mechanism and form). No probe is seeded by this contract; seeding remains Mike's call to open.

**Mechanism-class arc:** Rule D is a NEW mechanism-class design target, NOT a Rule C densification and NOT a Rule C second-pass boundary refinement. Rule C first pass already closed on A-prime (behavioral-map reach satisfied; LowLow only floor-adjacent near kappa=0; no away-from-floor substantive LowLow). Rule D reuses Rule C's becoming-active coupling but tests a different mechanism. It lives under cycle3/wave_two/rule_d/ to keep the record from reading as "more Rule C."

**Inherited locks (unchanged, binding):** topology 50x50 Moore radius 1 toroidal; SS-001 earned-window criterion; LOW_Z_THRESH = 2.0; the co-equal pair Psi_meanI_state / Psi_persistence_I, neither named theoretical Psi; the L4 ontological question rides forward unsettled and is NOT resolved by anything here.

---

## 1. The mechanism class (what Rule D tests)

Rule D tests the **turnover-limited activation** mechanism class:

> Whether lifted, non-degenerate near-null observables can be produced at RESPONSIVE local coupling because independent active-cell turnover prevents apparatus-level spatial / persistence organization from accumulating.

The theoretical bet: at responsive coupling, Rule C produces signed structure (apparatus-level organization accumulates). If active sites churn fast enough — deactivating on a time-scale shorter than that organization needs to form — then near-null observables could appear DESPITE nontrivial local coupling, not because coupling is absent. This is a time-scale-mismatch claim, distinct from the floor-adjacent (coupling-absent) near-null that Rule C and the comparators established.

**Rule D is NOT opened to search for LowLow.** It tests the named turnover-limited mechanism. A near-null result is interesting only if it is mechanism-produced (turnover suppressing organization at live coupling), not floor-adjacent, rule-forced, or degenerate.

## 2. The rule

### 2.1 Becoming-active (UNCHANGED from Rule C)

Rule D reuses Rule C's centered logit-linear signed coupling on the becoming-active transition, with no modification:

    p_become,i = sigma( logit(p_Lambda,i) + kappa * (2 q_i - 1) )

g(q) = 2q - 1 fixed centered; coefficient-null separable (kappa = 0 IS Lambda-only); q is the fraction of active neighbors (local). This is identical to the Rule C canonical form (Rule C contract Section 2.1). Reusing it isolates turnover as the SINGLE new mechanism axis and avoids two confounds: (a) a new coupling form making any result attributable to the coupling rather than turnover; (b) survival becoming neighbor-conditioned and collapsing Rule D toward Rule B.

### 2.2 Turnover (the NEW axis)

Rule D retains Rule C's neighbor-independent Lambda-survival and adds `theta_turnover`, an independent stochastic deactivation hazard, as an ADDITIONAL active-cell hazard on top of it:

    each active cell at tick t first survives with Rule C's neighbor-independent Lambda-survival probability s_Lambda, then independently survives the turnover hazard with probability (1 - theta_turnover);
    net active-cell persistence is s_Lambda * (1 - theta_turnover).

s_Lambda is Rule C's neighbor-independent Lambda-survival probability at the operative Lambda anchor (a flat per-cell survival probability, NOT neighbor-conditioned), carried unchanged from the Rule C M2 substrate. theta_turnover is in [0, 1], FIXED per run-setting, and is a time-scale parameter, not a survival rule in the Rule B sense. At theta_turnover = 0 net persistence is exactly s_Lambda — Rule D recovers Rule C exactly, so theta_turnover = 0 is the known signed Rule C reference, NOT a saturation endpoint. Rule D's turnover side is locally BLIND churn layered on Rule C's neighbor-independent survival, NOT neighbor-conditioned survival — this is what keeps the mechanism class distinct from Rule B (see Section 6).

**Canonical form is the Bernoulli hazard, NOT deterministic fixed lifetime.** Deterministic fixed lifetime can introduce artificial periodicity / age-cohort structure that would confound the near-null signal; it is reserved as a later audit only if the stochastic-hazard result is interesting, never the first Rule D form.

### 2.3 Update order (fence)

Rule D uses synchronous updates computed from the t state. Active cells at t persist to t+1 with probability s_Lambda * (1 - theta_turnover); inactive cells at t become active at t+1 with Rule C's p_become. An active cell that turns over does NOT re-enter (become active) in the same tick — re-entry begins from the next tick.

    x_i(t+1) = [ x_i(t)=1  AND  Bernoulli(s_Lambda * (1 - theta_turnover)) ]
               OR
               [ x_i(t)=0  AND  Bernoulli(p_become,i) ]

Without this fence, theta_turnover is not a clean lifetime hazard: same-tick reactivation would partially erase the meaning of turnover and make high theta_turnover look less like churn than intended. This preserves theta_turnover as a lifetime / churn parameter.

## 3. Construction fences (binding)

`theta_turnover` MUST be independent of all of:
- neighbor count;
- global rho;
- observable values (Psi_meanI_state, Psi_persistence_I, their z-scores);
- seed history;
- current window / SS diagnostics;
- any adaptive feedback or drift toward/away from SS eligibility.

> **Fence: turnover is an exogenous lifetime / churn parameter, not neighbor-conditioned survival and not a global-density controller.**

The fence weakens — and Rule D collapses toward Rule B — if theta_turnover becomes neighbor-conditioned, ties to current global rho, or adapts to whether the run is approaching SS eligibility. The becoming-active side must remain exactly Rule C's (no new neighbor terms beyond q in the existing coupling). All Rule C contract construction fences carry over unchanged (no kappa-on-global-rho, no dynamic centering against rho, no hidden feedback in the Lambda baseline, no piecewise sign-specific form, becoming-active coupling not acquiring extra range dependence).

The kappa-sign-through-zero point remains a SUBSTRATE parameter, NEVER an operationalization of the point(s) at which mu(rho) = 0. theta_turnover is likewise a substrate parameter, never a coherence operationalization.

## 4. Success criterion — turnover-axis bracketing (pessimistic-on-passing, MANDATORY)

A near-null result counts as **turnover-limited** ONLY if it satisfies the matched-coupling bracket:

> At the same Lambda anchor and the same RESPONSIVE nonzero kappa, increasing theta_turnover moves the system FROM signed structure at lower turnover INTO near-null / near-null at intermediate turnover, while rho stays lifted and non-degenerate.

The load-bearing bracket is **lower-turnover signed -> intermediate-turnover near-null at matched coupling.** A higher-turnover endpoint (floor-like or degenerate) is useful but secondary. Without the lower-turnover signed bracket at matched responsive kappa, a near-null result is NOT a turnover-limited candidate.

This is the direct analogue of the Rule C contrastive criterion (low/low earned only inside a map also capable of signed regimes): here, near-null is earned only inside a turnover sweep whose lower end produces signed structure at the same coupling. It keeps the result from being "we increased noise until structure disappeared."

### 4.1 Produce-or-fail-to-produce table

| Outcome | Reading |
| --- | --- |
| Lower turnover at matched responsive kappa is signed; intermediate turnover becomes near-null / near-null while lifted and non-degenerate | PRODUCES a turnover-limited candidate mechanism |
| Near-null appears only at kappa = 0 or epsilon-scale coupling | Floor-adjacent only; FAILS the Rule D target |
| Near-null appears at all theta_turnover values, with no signed lower-turnover bracket | Rule-forced / non-discriminating; FAILS the target |
| Near-null appears only with collapse, saturation, or unstable rho | Degenerate; FAILS the target |
| Responsive coupling remains signed for all theta_turnover until degeneration | FAILS TO PRODUCE the turnover-limited mechanism; counts as a negative result for the mechanism class under the locked topology |

### 4.2 Map requirement (precondition)

As with Rule C, the run must produce a behavioral map that demonstrably REACHES signed regimes and a degenerate endpoint along the relevant axes. Near-null at zero or epsilon-scale coupling does not count toward the target. If the sweep does not reach signed regimes at low turnover, any near-null is non-discriminating by default (the reach precondition is not met).

### 4.3 Density-confound guard (required)

Turnover changes rho. A near-null row at higher theta_turnover could be near-null because density has fallen into a different effective density regime, not because turnover specifically suppresses organization AT HIGH activation. "Lifted and non-degenerate" is necessary but not sufficient. Therefore:

> A turnover-limited candidate must NOT rest on a large density displacement alone. For every matched-coupling bracket, record rho_mean, rho_range_over_mean, and the difference in rho_mean between the lower-turnover signed setting and the intermediate-turnover near-null setting. If the near-null setting is materially lower-density than its signed bracket, the result is a candidate only PROVISIONALLY and requires a density-comparability audit before stronger interpretation.

This does NOT mean dynamically controlling rho (which would violate the fence). It means recording and auditing whether the candidate is actually high-rho / low-observable, rather than lower-rho / low-observable.

### 4.4 Live-coupling exposure guard (required)

Realized endpoint contrast (the kappa-axis tracking in Section 8) proves the rule is CAPABLE of a given local effect; it does not prove the run actually SAMPLED meaningful neighbor exposure. As theta_turnover changes rho, the distribution of observed neighbor fractions q_i can change — so a row could be called "responsive coupling" when the actual substrate exposure made the neighbor term effectively inert. Therefore:

> The near-null row must occur under nontrivial REALIZED local exposure, not merely under nominal responsive kappa. Candidate status requires the run record to show nontrivial realized local coupling exposure at the near-null setting (Section 8 metrics: observed q_i distribution and mean absolute neighbor-induced probability perturbation).

## 5. Interpretive role (fixed before execution)

> **Rule D tests whether independent active-cell turnover can produce lifted, non-degenerate near-null observables at responsive local coupling.** Success (the Section 4 bracket satisfied) SUPPORTS the turnover-limited mechanism class as a candidate. Failure (no bracket; signed structure persists across turnover until degeneration) FAILS TO PRODUCE the turnover-limited mechanism and counts as a negative result for the mechanism class under the locked topology. The run LOCATES behavior on the (kappa, theta_turnover) map; it does not reclassify Rule C's A-prime, does not resolve the L4 ontological question, does not name either observable as theoretical Psi, and does not harden the weak-form Rule B prior.

## 6. Relation to the existing record

- Does NOT reopen or reclassify Rule C M2 / A-prime.
- Does NOT alter the Comparator 0 / Comparator epsilon floor findings.
- Reuses Rule C's becoming-active coupling verbatim; the ONLY new mechanism element is theta_turnover.
- Distinct from Rule B: Rule B's issue was neighbor-CONDITIONED survival. Rule D retains Rule C's Lambda-survival (neighbor-INDEPENDENT — a flat per-cell probability) and multiplies it by an independent turnover hazard; neither factor is neighbor-conditioned, so Rule D does not reintroduce Rule B's pathology. theta_turnover remains the only NEW mechanism element (Lambda-survival is Rule C's, retained not added).
- Distinct from object (b) (Rule C near-zero boundary-refinement) and from a comparator perturbation ladder: those stay on Rule C's axis / a separate-process axis; Rule D is a new mechanism class.

## 7. Downstream design opens (NOT fixed here; set after this contract is reviewed)

The contract fixes the mechanism, fences, coupling reuse, and bracketing criterion ONLY. The following are named opens, to be set against the realized scale AFTER review (the Rule C discipline: grid density set only after function and fences are fixed, never silently inside the mechanism definition):

> **Open D-1 — theta grid.** Range and density of theta_turnover are not fixed here. They must be selected to span low-turnover signed persistence, intermediate-turnover candidate suppression of coherence, and high-turnover floor / degeneration risk, WITHOUT adapting to observable outcomes.

> **Open D-2 — responsive coupling settings.** Rule D must be tested at nonzero responsive Rule C coupling, not at kappa = 0 or epsilon-scale. Specific realized-contrast values deferred; candidate status requires matched-coupling bracketing along theta.

> **Open D-3 — Lambda anchors.** Whether Rule D uses only the existing M2 anchors Lambda = 0.20 / 0.40 or promotes reserved anchors 0.30 / 0.50 is deferred. The choice must be justified by the Rule D question, NOT by a search for LowLow.

## 8. Apparatus / protocol (carried)

- Observables: the co-equal pair Psi_meanI_state / Psi_persistence_I, signed three-level framework (positive structured / near-null / negative anti-structured per axis); neither named theoretical Psi.
- SS-001 flags Steady_State_Candidate and Lifted_Activation_Candidate remain INDEPENDENT at every stage.
- Per-(parameter-setting, seed) boolean flag counts, never per-parameter means.
- Realized-contrast tracking on the kappa axis (record realized delta_p for every setting), same measure as Rule C / Comparator epsilon.
- Record realized theta_turnover (the set hazard) for every setting alongside kappa and delta_p.
- Record the effective active-cell persistence probability s_Lambda * (1 - theta_turnover) for every setting, NOT a total-active-lifetime ladder (1/theta); effective persistence determines realized churn and must be recorded for honest calibration reading.
- Record rho_mean, rho_range_over_mean, and bracket-level delta_rho_mean (difference in rho_mean across theta_turnover at matched Lambda/kappa) — for the density-confound guard (Section 4.3).
- Record realized local coupling exposure at each setting: the observed q_i distribution (mean and variance) and the mean absolute neighbor-induced probability perturbation (mean |p_become,i - p_Lambda| over cells/ticks) — for the live-coupling exposure guard (Section 4.4).
- LowLow_Nondegenerate_Candidate is the apparatus-level flag; NEVER Regime_II in any identifier, comment, column, or prose.
- Layer 3 implements; Layer 3 never declares its own L2 clearance; deliverables framed as "what the run will produce."
- Parity (pre-flight + runtime) required, as with Rule C and the comparators.

## 9. Routing

This draft goes to Layer 2 for mean-field review BEFORE canonical placement. Layer 2 questions: (a) does turnover-limited near-null cohere at the order-parameter / mean-field level — is there a regime where lifted rho coexists with near-null observables under fast churn at live coupling, or does mean-field predict churn drives the system to the floor (kappa-irrelevant) so that "responsive coupling" and "near-null" cannot co-occur except trivially; (b) is the Section 4 bracket sufficient to discriminate turnover-limited from turnover-trivial, or is a further control needed; (c) flag any fence Layer 2 reads as leaky. After Layer 2 review and Mike's placement, the opens D-1/D-2/D-3 are resolved, then Layer 3 implementation, then seeding is Mike's call.
