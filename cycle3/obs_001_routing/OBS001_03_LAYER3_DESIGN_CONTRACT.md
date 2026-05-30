# Layer 3 design-menu contract - C3-OBS / C3-INT wave one (A + B)

From: Layer 1, 2026-05-28.
To: Layer 3.
Purpose: open wave one of the Cycle 3 substantive probe-design phase. This contract asks for a DESIGN MENU, not code. The design menu, when returned, routes through Layer 1 review and Layer 2 substantive review before any code-production contract is issued.

---

## 1. What this contract asks for, and what it does NOT

Asks for: a design menu specifying Rule A and Rule B at the local-rule level, the Lambda-like parameter for each, the telemetry schema, a minimal Lambda sweep, expected joint-signature outcomes under that sweep, ENV / CTL / SS gate attachment, and the four-level distinction applied to each run-class. Eight items, detailed in Section 5.

Does NOT ask for: code, executable scripts, parameter values that have not been justified at the rule level, execution claims, interpretation of runs that have not happened, or any judgment that the design has cleared Layer 2. L2 clearance is a Layer 1 judgment at implementation review; never a Layer 3 declaration.

Frame all deliverables as **what the design specifies** or **what the rule is expected to produce under the proposed sweep**. No past-tense execution language. No "the run demonstrates," "Rule A confirms," "L2 sufficiency check passed," or "the design clears L2." Candidates **produce or fail to produce**.

## 2. State at contract-open

Three Cycle 3 precondition gates cleared and not under reopen:

- **C3-ENV-001 - passed-L1.** Canonical environment: top-level venv, Python 3.14.4, Mesa 3.5.1, numpy pinned 2.4.4.
- **C3-CTL-001 - valid-L2.** Synthetic control battery on five cases; both observables Psi_meanI_state and Psi_persistence_I grounded against grid-local permutation nulls.
- **C3-SS-001 - valid-L2.** Synthetic steady-state battery; the earned-steady-state-window criterion is apparatus-grounded, not an assertion. Two independent flags: Steady_State_Candidate and Lifted_Activation_Candidate. These remain independent and are NOT collapsed into a single "Regime-II-ready" flag at any stage.

Topology locked: **50 x 50, Moore radius 1 (8-neighbor), toroidal.** Cycle 3 baseline. The observable's adjacency must match.

The two-dimensional coherence signature (Psi_meanI_state, Psi_persistence_I) is a co-equal pair. Neither is named theoretical Psi. Regime assignment is L4 (Mike / Layer 1).

## 3. Scope: A + B in wave one; C deferred to wave two

The transition-rule menu, in committed form:

- **A** - both-agree baseline; pre-loads neither; relaxes to fixed points / uniform states; no sustained motion.
- **B** - pre-loads Psi_meanI_state; range-bound / Life-like; shifting structures.
- **C** - micro contagion with tunable divergence. **Deferred to wave two.** Do not design C in this contract; do not include C in the sweep; do not assume what C will be in wave two beyond what Section 4.2 below preserves.

Wave one tests whether the same topology and measurement apparatus can produce a non-divergent baseline under A AND a divergent co-equal-observable signature under B, with the load-bearing Lambda-varying sequence visible.

## 4. Two Layer-1 corrections carried forward (still in force)

These corrections were issued to Layer 3 on 2026-05-25 and are committed primary source. They stay in force in this contract.

**4.1. Rule A pre-loads neither.** The first sketch labeled A as pre-loading Psi_persistence_I. A strict lower-threshold activation rule with no upper / overcrowding bound moves both observables TOGETHER, not apart: at low threshold it fills toward uniform (both observables low or degenerate); at high threshold it freezes into locked clusters (both observables high). Across Lambda it produces no divergence, because it has no mechanism for sustained motion of structure - it relaxes to fixed points or uniform states. A is therefore the least-discriminating rule, the both-agree sanity baseline. **Design A as a lower-threshold-style rule with no upper / overcrowding bound.** Do not re-introduce an upper bound that would convert A into a range-bound rule; that is Rule B's design space.

**4.2. Rule C (when wave two opens) stays at the micro-rule level.** A prior sketch attributed C's divergence to "the point(s) at which mu(rho) = 0." mu(rho) is a mean-field (coarse-grained) coefficient; a micro contagion rule does not contain it. The micro-rule-to-mu(rho) relationship is what the mean-field analysis derives, not what a rule sketch asserts. This applies forward whenever C is described.

## 5. The design menu - eight deliverables

For each deliverable, frame in terms of what the design specifies or what the rule is expected to produce. Not what runs have done - no runs have happened.

**5.1. Local-rule specification.** Define Rule A and Rule B precisely at the per-cell, per-tick level: what each cell evaluates over its 8-neighbor Moore neighborhood, the activation / persistence / deactivation conditions, and the initial-condition convention. Specify both rules in the same notation so they are directly comparable. Per Section 4.1, A has no upper / overcrowding bound. B is range-bound / Life-like - specify the band precisely.

**5.2. Lambda-like parameter.** Identify the structural-conduciveness parameter Lambda for each rule - the parameter that, when varied, is expected to drive rho through inactive -> lifted -> coherent. Name the parameter, its range, and its rule-level interpretation. The mapping of micro-rule parameters to Lambda is a design specification; it is not a claim that the micro rule contains Lambda in the architectural sense. State explicitly what aspect of structural conduciveness each rule's Lambda represents (threshold? excitation band? something else?).

**5.3. Telemetry.** State the per-tick and per-window quantities the runs will record. At minimum: rho(t), per-cell active-state values for the window, the Psi_meanI_state and Psi_persistence_I observables (as in CTL-001), and the four SS-001 diagnostics (drift, cv, range_over_mean, lifted). Plus any rule-specific diagnostics needed to detect rule-pathologies (degenerate fills, locked-cluster freezes, etc.).

**5.4. Minimal Lambda-sweep.** Propose a minimal sweep for each rule: which Lambda values, how many seeds per value, the steady-state-window candidate windows, and the total run count. Bias for shortness - first feedback loop should be as short as possible while still able to fail meaningfully.

**5.5. Expected joint-signature outcomes.** For each Lambda value in each rule's sweep, state the **expected** joint-signature outcome (low/low, high/high, high meanI / low persistence, low meanI / high persistence), and the reasoning grounded in the local-rule specification. Frame as expected, not asserted. The expectation is what would falsify the design if the run produces something else - it is not what the design will produce.

**5.6. Gate attachment.** Specify how ENV / CTL / SS gates attach to the proposed runs: which gate cleared what, what the runs inherit from each cleared gate, what each gate licenses and does not license. The runs read rho(t) windows on the apparatus-grounded earned-steady-state-window criterion (SS-001); they read the coherence observables on the CTL-001-validated apparatus; they execute in the C3-ENV-001 canonical environment.

**5.7. Four-level distinction per run-class.** State, for each rule and each Lambda value, what would count as:
- L1 - implementation result (does the script compute what it claims, without error);
- L2 - measurement-validity result (is the quantity the quantity intended);
- L3 - steady-state-window-eligibility result (did the window earn its label);
- L4 - manuscript-facing interpretation (what does the value mean for Regime-II-as-structural).

The L4 column stays empty for any run-class until Mike / Layer 1 settles the ontology. The design does not propose L4 readings; it specifies what would feed an L4 judgment.

**5.8. Co-equal-pair guard.** Confirm in the design that neither Psi_meanI_state nor Psi_persistence_I is named theoretical Psi. The two SS-001 flags stay independent. CTL-001 Case D divergence (Psi_meanI_state high, Psi_persistence_I = 0 on the transient wave) is recorded data on the pair, not a tiebreaker.

## 6. Framing discipline

The design menu describes what runs WILL specify. No run has happened. No measurement has been made. Frame:
- "Rule A, under the specified sweep, is expected to produce..."
- "The design specifies that..."
- "Telemetry recorded per the schema in Section 5.3..."

NOT:
- "The run demonstrates..."
- "Rule A confirms..."
- "L2 sufficiency check passed..."
- "The design clears L2..."

L2 clearance is a Layer 1 judgment at implementation review of the design. Layer 3 does not declare it.

## 7. Routing after this contract

When the design menu returns:
1. Layer 1 implementation review of the design (consistency with primary source, the two corrections from Section 4, the co-equal-pair guard, vocabulary discipline, framing discipline);
2. Layer 2 substantive analytical review (discrimination analysis, rule-level reasoning, expected-signature reasoning, gate attachment);
3. Only after Layer 2 returns: a SEPARATE code-production contract for the runnable artifacts.

There is no implicit promotion from design menu to code. The contract for code production is a separate routing.

## 8. Vocabulary (binding)

rho = activation density. Psi = coherence (with neither observable in the pair named theoretical Psi). Lambda = structural conduciveness. Agents act (no decision / optimization / utility / cognitive language). "The point(s) at which mu(rho) = 0" - never rho_c. "Per-cell active-state values" - never "field" as explanatory mechanism. Candidates produce or fail to produce - never "confirm" or "demonstrate." "Earned steady-state window" - the SS-001-validated criterion, apparatus-grounded.
