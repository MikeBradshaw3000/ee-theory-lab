# Two-channel ordering probe - design resolution (CM-1 primary; probe named-not-triggered)

**Status: DESIGN RESOLUTION. Layer 2-reviewed twice (v1 accept-with-amendments; v2 return pass accept-with-precision-amendments, both 2026-07-04); Mike-arbitrated 2026-07-04 (CM-1 primary, CM-2 held, CM-0 comparator, no seeding). NON-SEEDING. The ordering probe remains NAMED-NOT-TRIGGERED: a design contract stage begins only on Mike's separate, explicit opening.** This document governs the two-channel ordering probe's design resolution. It does not seed a probe, does not draft an implementation spec, does not engage Layer 3, does not reclassify Comparator 0, does not move L4, and does not open or close Rule E B/C. TWO_CHANNEL_PROPOSAL.md governs the proposal's standing (its named-instrument class wording is amended by Section 2 below, Mike-ratified); READING_D_PASS1_FINDINGS.md and WAVE_TWO_PATTERN_SYNTHESIS.md govern the committed results. On any discrepancy with committed findings files, those files win.

## 1. The discriminating question (fixed; verbatim binding on any contract)

Can common-mode lift raise rho without spatial organization, while organization onset tracks the differential channel rather than rho level itself?

Operational form of the proposal's ordering prediction (L2-ruled risky-and-falsifiable): under common-mode lift with swept differential coupling, organization onset should track the differential channel's strength at roughly constant lifted rho.

## 2. The resolved construction (Mike-arbitrated)

**Primary: CM-1 - exogenous frozen deterministic common-mode driver, with differential-channel sweep.**

**Instrument renaming (Mike-ratified amendment):** the probe is named **"Two-channel ordering probe: exogenous common-mode lift with differential-channel sweep."** This amends the named instrument's class wording in TWO_CHANNEL_PROPOSAL.md ("admissible Rule E class, uniform conditioning"): the primary construction is NOT Rule E-class conditioning and is NOT recorded as a Rule E continuation. It is an exogenous common-mode driver. Lineage: proposed in v1 as a fork, L2-recommended, Mike-ratified in this resolution; the proposal file stands as committed history.

Construction: p_become = sigma(logit(p_Lambda) + u_t + kappa*(2q-1)), with:
- u_t a predeclared, frozen, bounded, DETERMINISTIC block waveform (block-constant on the canonical 25-tick cadence; |u_t| <= u_max predeclared), identical at every cell (fence 7 enforced by construction), identical across ALL seeds (one shared schedule; per-seed schedules deferred to a later robustness audit only - L2). u_t depends on no run observable: no feedback of any kind; the observable-feedback fence is intact trivially; the bounded-A argument-scale pathology cannot arise.
- kappa the Rule C differential coupling, unchanged in form, swept as a SUBSTRATE parameter from kappa = 0 through the responsive range (grid at contract stage; subset of the committed M2 realized-contrast grid, dense at the small-|c| end).
- Survival Lambda-only and neighbor-independent, untouched; the driven Lambda-configuration does not leak into survival or turnover.

Schedule form (L2-recommended, adopted): deterministic frozen waveform, identifiability first, realism second. Stochastic (narrative-like) schedules are a later variant only, opened by design resolution if stochasticity becomes theoretically load-bearing. Waveform specifics (stepped square/triangle vs low-amplitude sinusoid; period; u_max; tier count) are contract-stage opens under binding guidance:
- The waveform must sit below compression and must not itself induce saturation (fence 5 applies to the driver, not only the read).
- **Cadence-aliasing constraint (L1 addition, L2-broadened, adopted):** choose the schedule period for identifiability, not realism - long enough to produce measurable zero-mode imprint, short enough to provide multiple cycles in the run record, and NOT equal to the known 2-block artifact cadence (the committed Rule E saturate/extinct ring signature) or a trivial alias of the 4-block / 100-tick observation-window structure. CM-1 has no feedback and is not expected to reproduce the Rule E artifact; the constraint is interpretive hygiene - a block-level pattern in the read must never need disentangling from a known artifact cadence or a window-alignment artifact. (Exact window structure is verified from the committed scripts at contract stage; the committed script is primary source.)

**Comparator: CM-0** - static uniform offset u_t = u constant, matched-rho row. Fails fence 4 by construction (the relabeling case); retained ONLY as the within-design contrast for what temporal structure adds, and as the reference expectation for gate G1. Never a driver.

**Held: CM-2** - uniform endogenous macro conditioning (the Rule E-class construction the proposal originally named). NOT selected (L2-recommended, Mike-arbitrated): relay-lift would confound the ordering read - an outcome could be a finding about common-mode ordering or another finding about lagged-feedback relay dynamics, and the program just established relay dynamics as a major failure mode. CM-2 is HELD as a later endogenous-common-mode variant requiring its OWN design resolution before any opening (framing: endogenous relay-lift vs clean-responsive common-mode conditioning). This hold is SEPARATE from the Rule E B/C hold; neither hold touches the other.

## 3. Binding fences (carried into any contract verbatim)

1. **No floor reclassification.** Comparator 0 remains the trivial stochastic floor / common-mode-compatible pattern; never retroactively recorded as Regime II.
2. **No L4 movement.** Apparatus-level driver channels and observable behavior only; neither observable named theoretical Psi at any stage.
3. **No kappa-as-mu(rho) language.** kappa substrate-swept; "dominance" outcome language only, in the read, never in the construction.
4. **Common-mode distinguishable from i.i.d.** Zero-mode temporal structure required: rho_t overdispersion, autocorrelation, or block-timescale modulation beyond static i.i.d. Lambda - and under CM-1, direct cross-correlation of rho_t against the known frozen schedule.
5. **Matched-rho / below-compression.** Operating band below logit-slope compression; matched-rho comparisons mandatory; slope audit mandatory.
6. **Differential diagnostics mandatory.** prop_I, raw observable effects, z-scores, zero-mode dynamics, controls; raw effects always travel with z (Reading-D lesson, binding).
7. **Pure common-mode loading.** The common term is identical at every cell by construction; spatially correlated susceptibility would make it a differential common-signal channel and is excluded. The empirical-world caveat travels to the manuscript side.

Standing fences inherited unchanged: observable feedback excluded; driven Lambda does not leak into survival/turnover; survival Lambda-only, neighbor-independent; no dynamic centering; no kappa modulation by the common channel.

## 4. Validity gates (a run failing a gate is not interpretable; recorded as apparatus limit, not evidence)

- **G1 - schedule imprint (hard requirement; L2 amendment adopted, with the return-pass precision):** a CM-1 run is not interpretable as common-mode lift unless rho_t significantly tracks the frozen schedule, AND the imprint exceeds static-i.i.d. / CM-0 expectation at the same mean rho - driver imprint, not ordinary stochastic tracking. No rho_t schedule imprint above that reference, no common-mode-lift claim. (Imprint statistic and threshold: contract-stage open, fixed from committed data and CM-0 rows before any interpretive read.)
- **G2 - differential reach at the propensity level:** the kappa sweep must demonstrably activate the differential channel - prop_I rising with kappa toward the committed base values (prop_I ~ +0.38 at |c| = 0.35) - within the operating band. If prop_I fails to rise with kappa, the probe FAILED TO ACTIVATE the differential channel; no ordering falsification is readable from that run.
- **G3 - matched-rho overlap:** the ordering read is valid only for settings whose realized rho distributions overlap sufficiently to support matched-rho comparison (overlap criterion predeclared at contract stage). Non-overlapping regions are excluded from the ordering claim and reported as apparatus limits.
- **G4 - slope audit:** mean p_become and an effective-slope proxy per setting; rows inside the band but failing the compression audit are fenced.

## 5. The read (outcome language; predeclared)

Per (schedule-tier, kappa, seed), mandatory diagnostics: raw Moran for both co-equal observables; existing z-scores alongside; prop_I computed on the FULL becoming-active propensity surface per tick/block, with the decomposition read (L2 amendment, adopted): common-only contribution (spatially constant by construction; prop_I ~ 0 identically - verified, not assumed), differential/full-surface contribution (should rise with kappa), and realized state/persistence observables (should track the differential component if the hypothesis is right). The decomposition is the core of the instrument. Controls: the per-cell independent time-shuffle (the informative control; whole-window time shuffles are invariant for both co-equal observables and are excluded). Zero-mode diagnostics: rho_t overdispersion, autocorrelation, block-timescale modulation, schedule cross-correlation.

**Stratified ordering read (L2 amendment, adopted):** organization is reported as a function of BOTH rho and prop_I; the primary ordering comparison is matched or stratified by rho. A kappa-tracking claim is never read off a sweep in which rho drifts with kappa un-stratified.

**Three reading categories (L2 addition, adopted; fence wording per the L2 return pass):**
- **zero-mode driver imprint** (primary label; equivalently "global-count driver imprint"): global-count modulation or temporal structure in rho_t that follows the frozen schedule. This is apparatus-level driver response only. It is not coherence, not synchrony in the theoretical sense, not Regime II, and it does not bear on whether either observable is theoretical Psi. If the phrase "zero-mode temporal coordination" is ever used, it is always qualified as "apparatus-level zero-mode temporal coordination of the global activity count"; unqualified "synchrony" is excluded from all records.
- spatial organization (the meanI axis and its raw/controlled residue);
- persistence organization (the persistence axis).
The common-mode channel is EXPECTED to light up the first and not the second. "Lift without organization" is therefore always written precisely: lift without SPATIAL/DIFFERENTIAL organization, not lift without any collective structure.

Onset criteria: predeclared joint criterion on raw effect plus control-surviving residue, prop_I as the mechanistic anchor, z reported but never sufficient alone. Thresholds fixed at contract stage FROM COMMITTED DATA ONLY (floor prop_I ~ 0; base prop_I ~ +0.38; committed raw Moran ~0.004-0.011 meanI, ~0.05-0.07 persistence); nothing tuned on probe output.

Calibration discipline: schedule-tier amplitudes calibrated on rho-lift and non-degeneracy ALONE (Comparator-0 discipline); the observables are outputs, never tuning targets.

## 6. Falsification conditions (fixed; L2 tightenings incorporated)

Within the matched-rho band, with G1-G4 passed:

- **The ordering hypothesis is SUPPORTED (the probe PRODUCES the predicted structure) if:** organization onset moves with kappa at matched rho, AND fails to appear at kappa ~ 0 under verified common-mode lift (G1 passed; lifted rho; prop_I ~ 0; realized organization at floor).
- **The ordering hypothesis FAILS TO PRODUCE (falsified in its risky form) if:**
  (a) organization appears under common-mode lift at kappa ~ 0 within the band, with raw effect above the predeclared onset threshold AND control-surviving residue (never a marginal z blip alone); OR
  (b) the differential propensity channel demonstrably activates (G2), matched-rho holds (G3), and realized organization still does not track the differential channel.
  Sub-reading under (b): if differential prop_I rises but realized organization does not, the WELDING claim (substrate couples lift to organization at the realized level) weakens - recorded as bearing on Reading B's realized-level content, distinct from the ordering claim.
- **Under-determined / gate-failed:** any G1-G4 failure region - recorded as apparatus limits, never as evidence for or against.
- **Secondary diagnostic (L2, adopted):** local factorization prop_I(u, kappa) ~ f(u) * g(kappa) is an EXPECTED DIAGNOSTIC in the non-compressed operating band, not a required success criterion. Departures are informative, recorded, never automatic failure.

No outcome reclassifies Comparator 0, moves L4, closes the Rule E B/C question, closes the CM-2 hold, or closes any mechanism class.

## 7. Contract-stage opens (deferred by design; none block this resolution)

1. Waveform specifics: stepped vs sinusoid, period (subject to the cadence-aliasing constraint), u_max, schedule-tier count.
2. Lambda anchor (0.40 first-pass parity vs both committed anchors) and the [rho_lo, rho_hi] band values.
3. kappa grid (M2-subset; density near small |c|).
4. Predeclared thresholds: G1 imprint statistic and driver-imprint-above-CM-0 threshold; G3 overlap criterion; Section 5 onset criteria - all fixed from committed data before any run.
5. Seeds (default: the canonical five).
6. Window-structure verification against the committed scripts (primary source) for the aliasing constraint.

## 8. What this resolution does not do

Does not seed a run. Does not draft an implementation spec or engage Layer 3. Does not reclassify Comparator 0 or any rested arc. Does not move L4. Does not open CM-2 (held; own design resolution required). Does not open or close Rule E B/C (held; separate). The probe remains NAMED-NOT-TRIGGERED; a design contract stage begins only on Mike's separate, explicit opening.

## 9. Attribution record

v1 (Layer 1): candidate constructions compared not picked; CM-1 recommended; fences 1-7 fixed from the arbitration direction; matched-rho operationalization; falsification frame. Layer 2 v1 review: CM-1-primary concurrence (recorded as refinement-driven convergence under the framing asymmetry - L1 framed first - with independent grounds: relay-confound argument); instrument renaming; relay-lift rejection for the primary; schedule-imprint hard requirement; rho/prop_I stratified read; prop_I full-surface decomposition; both falsification tightenings; factorization demotion; deterministic-shared-schedule preference; the zero-mode reading category (L1's v1 missed it). Layer 1 v2 additions: the L4-adjacency fence; the cadence-aliasing constraint. Layer 2 return pass: "zero-mode driver imprint" primary label and the qualified-wording rule; aliasing constraint broadened to window-structure aliases; G1 driver-imprint-above-CM-0 precision. Mike: arbitrated CM-1 primary / CM-2 held / CM-0 comparator / no seeding, and ratified the instrument renaming.

- Layer 1 (Claude), drafting partner; Layer 2-reviewed (twice); Mike-arbitrated
