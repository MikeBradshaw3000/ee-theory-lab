# Cycle 3 — Probe-phase design inputs (HELD, not committed)

**Status:** held design input for the substantive-probe phase, which is deliberately unseeded until the C3-CTL-001 and C3-SS-001 gates clear. This note preserves Layer 2's forward analytical contribution so the probe phase inherits it rather than re-deriving it. It sits alongside the held transition-rule menu and the converged measurement-validity finding. It is NOT folded into C3-CTL-001, and it commits nothing. Regime assignment is L4 (Mike / Layer 1).

**Source:** Layer 2 analytical contribution, 2026-05-25, in reply to the Layer 1 consultation. Recorded here as design input.

---

## 1. The two-dimensional coherence signature

Read the co-equal observables jointly as a pair, preserving the distinction rather than collapsing it:

(z_meanI_state, z_persistence_I) — z-scores against each observable's own grid-local null, preferred over raw values for reading across runs within the same topology.

The two ask different questions:
- Psi_meanI_state: are active-state configurations spatially organized at each tick, sustained across the window as a repeated property?
- Psi_persistence_I: are the same cells persistently active in spatially clustered ways across the window?

Neither dimension is asserted to be theoretical Psi. The pair is a measurement / interpretation scaffold, not a committed regime map.

## 2. Quadrant readings (allowed reading / forbidden interpretation)

- **high meanI, low persistence** — dynamic spatial organization without same-cell persistence (moving bands, waves, circulating or oscillatory organized configurations). This is NOT "no coherence." Forbidden: "therefore Psi is high" or "therefore Psi is low" — that depends on whether Regime-II coherence requires same-location persistence, which is L4.
- **high meanI, high persistence** — stable spatial organization with persistent clustered participation by the same cells. The strongest "both agree" candidate high-coherence signature. Forbidden: "therefore Regime III" absent an earned steady-state window and the Lambda / rho context.
- **low meanI, low persistence** — no spatially organized configuration per tick and no persistent clustered activation. Forbidden: "therefore Regime II" absent lifted rho and an earned steady-state window. Low-low alone is not Regime II.
- **low meanI, high persistence** — the persistence map is spatially clustered but instantaneous configurations are not strongly organized: localized propensity (where activation recurs) without per-tick organization. Forbidden: "therefore Psi equals persistence." Theoretically interesting because it separates where activation recurs from whether each moment is organized.

## 3. Relationship to mu(rho)

The pair is an observable signature, NOT mu(rho). mu(rho) is the mean-field coefficient governing whether Psi can grow (dPsi/dt = mu(rho) Psi - gamma Psi^3); it is not directly observed in the ABM. What is observable is whether candidate Psi signatures remain near null or become organized / persistent under varying rho and Lambda. The micro-rule-to-mu(rho) relationship is derived by the mean-field analysis, not read off a signature.

## 4. The Lambda-varying probe sequence (the load-bearing design point)

The substantive probe must not simply ask "do we see Psi?" It must vary Lambda and look for a SEQUENCE:

1. Lambda changes.
2. rho becomes nonzero / lifts.
3. coherence signatures remain low over an earned steady-state window.
4. only under other conditions do one or both coherence signatures lift.

This is the ABM analog of Lambda -> rho -> mu(rho) -> Psi. The pattern that bears on the "baked in" objection is not merely low Psi — it is this sequence: the ABM producing activation without coherence before any coherence transition is read. The probe question is "across controlled structural-conduciveness conditions, does rho lift before either coherence signature lifts?"

## 5. Candidate regime map (CANDIDATE signatures only — regime assignment is L4)

- lifted rho + low/low signature -> candidate Regime II
- lifted rho + high/high signature -> candidate Regime III
- lifted rho + high meanI / low persistence -> dynamic-organization regime, ontologically unresolved
- lifted rho + low meanI / high persistence -> localized-propensity regime, ontologically unresolved

Held as candidate signatures with forbidden interpretations attached, not as a committed map. This avoids forcing the ABM result prematurely into a one-dimensional Psi reading.

## 6. One Layer 2 recommendation explicitly NOT adopted for C3-CTL-001

Layer 2 recommended routing a joint-classification table (meanI_z_high? / persistence_z_high? / joint_signature / allowed_reading / forbidden_interpretation) to Layer 3 as part of C3-CTL-001. That is declined for the control gate: it would pull real-substrate interpretation structure into the synthetic battery, whose job is to validate the discrimination on five known cases, not to carry real-substrate reading-rules. The classification-table structure is preserved here as probe-phase input, to be taken up when the probe phase opens — not in the control battery.

---

Vocabulary: rho = activation density; Psi = coherence; Lambda = structural conduciveness; agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce.
