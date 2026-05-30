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

## 7. Wave-one substrate-observed amendment (C3-OBS-001, 2026-05-28)

**Status:** appended after wave-one A+B closed at apparatus level. Sections 1-6 above are preserved as held v1 design input (Layer 2, 2026-05-25); this section records what the wave-one substrate produced and amends the framework where the substrate exceeded what the v1 quadrant scheme could represent. Apparatus-level only; regime assignment remains L4 (Mike / Layer 1). Source: C3-OBS-001 canonical CSV and the Layer 2 accept-with-required-amendments verdict.

### 7.1 The 2x2 high/low quadrant scheme is too coarse

Section 2's quadrant readings assume each axis is either "high" (structured) or "low," with "low" implicitly meaning near-null (z near zero). The wave-one substrate did not respect that assumption. Rule B's eligible-or-near-eligible bands produced significantly NEGATIVE Psi_persistence_I z-scores (anti-clustered persistence: the persistence map is LESS neighbor-clustered than the grid-local permutation null), not near-null. And the non-eligible band [3,4] produced strongly POSITIVE persistence. The persistence axis therefore occupies three distinct regions the 2x2 has no cells for: positive (clustered), near-null, and negative (anti-clustered). A "low persistence" cell that conflates near-null with anti-clustered erases a real substrate distinction.

### 7.2 Amendment: signed three-level framework per axis

Replace the 2x2 high/low quadrant scheme with a signed three-level classification on EACH observable axis, read against that observable's grid-local permutation null:

- **positive / structured** — z significantly above null (organized, or clustered, depending on the axis).
- **near-null** — z near zero, no detectable structure against the null.
- **negative / anti-structured** — z significantly below null (anti-organized, or anti-clustered).

The amendment's load-bearing move is distinguishing **near-null from negative-anti-structured on both axes**. The v1 scheme could not name the difference between "no detectable persistence structure" and "persistence actively anti-clustered relative to null"; the signed scheme can. This is a measurement / interpretation scaffold, not a committed regime map; it does not name either observable as theoretical Psi, and it does not assign regimes.

### 7.3 The wave-one Rule B earned-window signature

The eligible-or-near-eligible Rule B bands ([1,2], [2,3], [2,4]) produced the same signed signature over their earned (or near-earned) windows:

> **positive meanI / negative persistence** — per-tick spatial organization of active-state configurations, with anti-clustered persistence.

This is NOT "high meanI / low persistence" in the v1 sense. The persistence signal is genuinely negative (anti-clustered), not merely small. Recording it as "low persistence" under the v1 scheme would mislocate it as near-null. The signed scheme places it correctly: positive on the meanI axis, negative on the persistence axis.

Per-band detail (apparatus-level, from the C3-OBS-001 CSV): [2,3] robust (multiple earned windows on all 5 seeds); [2,4] earned-but-heterogeneous (5/5 seed-level occurrence, but multi-window on 3 seeds and single-window on 2); [1,2] boundary / near-steady (1/5 seed-level occurrence). The positive-meanI / negative-persistence sign holds across all three.

### 7.4 The [3,4] non-eligible contrast (the other end of the persistence axis)

Band [3,4] is non-eligible / unstable and earned essentially no clean steady windows. Its z-scores are positive meanI and strongly POSITIVE persistence — the opposite persistence sign from the eligible bands. This is recorded as a non-eligible contrast observation, NOT an earned-window signature, and is fenced from the signature in 7.3. Its design relevance: it shows the persistence axis does not merely weaken outside the eligible window — it REVERSES under the unstable band. The signed three-level framework is what makes that reversal nameable; the v1 2x2 could not represent it. (Eligibility gates signature-status, not measurement-validity: the [3,4] z-score retains its ordinary meaning against the null, but the windows it is computed over are mostly non-eligible, so the sign describes the band's behavior without earning steady-state-signature status.)

### 7.5 Seed-level occurrence vs window-count robustness (a reading lens for band comparison)

Wave one surfaced a distinction worth carrying into future probe design and band comparison:

- **Seed-level occurrence** — whether a seed produced at least one earned steady-state window.
- **Window-count robustness** — how many earned windows each seed produced.

Because the SS-001-validated apparatus is explicitly about earned steady-state windows, window-count is the load-bearing measure of band robustness, not isolated seed-level occurrence. A ">=1 window per seed" criterion smooths over the difference between a band that repeatedly earns windows (e.g. [2,3]) and one that barely crosses the gate on some seeds (e.g. [2,4]). Future band-comparison probes should report both levels.

### 7.6 What this amendment does NOT do

It does not loosen LOW_Z_THRESH (= 2.0); the LowLow_Nondegenerate_Candidate flag was False on all 300 wave-one rows, and that is recorded as a negative apparatus-level finding, not a reason to relax the threshold. It does not name either observable theoretical Psi. It does not assign regimes. It does not revise the candidate regime map in Section 5 (that map's "low/low" cell still means near-null on both axes; the signed scheme simply makes "low" precise as near-null and distinguishes it from negative). The Section 5 candidate map and the Section 4 sequence remain the held design targets for subsequent waves.

---

Vocabulary: rho = activation density; Psi = coherence; Lambda = structural conduciveness; agents act (no decision / optimization / utility / cognitive language); "the point(s) at which mu(rho) = 0" (never rho_c); "per-cell active-state values" (never "field"); candidates produce or fail to produce.
