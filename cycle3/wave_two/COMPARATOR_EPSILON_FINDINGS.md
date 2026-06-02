# Comparator epsilon findings

**Status:** CANONICAL. Records the reading of the Comparator epsilon weak-neighbor floor audit (`cycle3/data_out/c3_w2_comparator_eps_results.csv`, script `cycle3/wave_two/c3_w2_comparator_eps.py`, per-tick states `cycle3/data_out/c3_w2_comparator_eps_states_*.npz`). The reading below is the outcome Layer 2 PRE-SPECIFIED in A-prime ("if Comparator epsilon remains near-null under its weak perturbation, it supports the A-prime language that the Rule C near-zero band is floor-adjacent weak-coupling tolerance"); this note records that the result matches that anticipated outcome. It is a finding record, not a design document; the contract governs design.

**Run:** Comparator epsilon (contract object a, separate weak-neighbor process), anchors Lambda = 0.20 and 0.40, predeclared weakness epsilon = 0.05, per-anchor additive coefficients a = 0.00500 / 0.01000, seeds 42/137/256/1024/31415, wave-one window structure. 20 rows; 10 per-tick state NPZs. Ran at parity (pre-flight + runtime parity check passed).

---

## 1. The finding

> Under a deliberately weak fixed neighbor perturbation (realized delta_p = 0.0100 at Lambda = 0.20, 0.0200 at Lambda = 0.40 â€” both well below the Rule C smallest nonzero setting |c| = 0.05), the apparatus floor remains near-null / near-null at both anchors. This SUPPORTS the language that the Rule C near-zero band is floor-adjacent weak-coupling tolerance: the floor is stable to minimal local coupling and does not go signed under barely-there coupling.

This is the outcome Layer 2 named in A-prime as the supporting case. It is recorded as confirmation of an anticipated reading, not as a new arbitration.

## 2. What the run produced (observation)

- **Realized contrast confirmed:** realized_delta_p = 0.0100 (0.20) and 0.0200 (0.40) on all rows, matching the per-anchor ceiling epsilon * p_Lambda exactly.
- **Eligibility:** all 20 rows lifted (mean_rho ~0.197 at 0.20, ~0.398 at 0.40) and non-degenerate (no extinction, no saturation). Window_start=0 rows mostly non-steady (rho_range_over_mean over 0.25, the low-density Poisson-noise effect seen in Comparator 0); steady almost everywhere else. Eligible floor readings throughout.
- **Psi_meanI_state_z:** centered near zero, range ~[-1.50, +2.36]. ONE row over 2.0 (Lambda=0.40, seed 137, window 75, +2.36) â€” isolated, no neighbor windows in its group exceed, its persistence-z unremarkable (-0.29). Finite-sample tail, inspect-not-halt.
- **Psi_persistence_I_z:** centered near zero, range ~[-1.48, +2.09]. ONE row over 2.0 (Lambda=0.20, seed 31415, window 0, +2.09) â€” isolated, marginal, its meanI-z +0.36. Finite-sample tail.
- Two isolated marginal exceedances out of 40 axis-readings (20 rows x 2 axes), neither replicated within its group, neither with a signed partner. No systematic sign drift on either axis at either anchor.

Reading against the Comparator-style severity convention: both axes near-null across eligible rows at both anchors; the apparatus floor is stable to the minimal perturbation; the two marginal exceedances are finite-sample tail behavior, not a halt condition. Nothing halted; no re-run, no re-tune.

## 3. The binding constraint (held)

Per the Layer 2 scope resolution, this result calibrates the LANGUAGE "weak-coupling floor-adjacent." It does NOT:
- reclassify any Rule C row as substantive;
- locate the Rule C near-zero transition point;
- move the Rule C-axis thresholds (|c| <= 0.10 floor-adjacent, |c| >= 0.20 responsive).

The two ceilings stay distinct axes: the Comparator epsilon ceiling (realized delta_p <= 0.02, separate-process perturbation scale) and the Rule C near-zero boundary (|c| <= 0.10, Rule C realized-contrast axis) are related calibration facts, NOT interchangeable. Comparator epsilon confirms the floor tolerates coupling well BELOW where the Rule C band sits; it does not speak to where the Rule C band ends.

## 4. What this means together with the Rule C finding

- Comparator 0: lifted i.i.d. floor is near-null (apparatus-null behavior well-behaved).
- Comparator epsilon: the floor remains near-null under minimal nonzero local coupling (floor stable to weak coupling).
- Rule C M2 (A-prime): the low/low band is floor-adjacent through |c| <= 0.10, dissolving into signed regimes as coupling becomes responsive; reach satisfied at both anchors; classified floor-adjacent weak-coupling tolerance, NOT substantive candidate.

Together: the near-null/near-null region in this apparatus is the floor and its weak-coupling neighborhood, confirmed from two independent directions (the i.i.d. floor and the weak-perturbation floor), and the Rule C near-zero LowLow band sits within that floor-adjacent regime rather than constituting an away-from-floor substantive low/low. The weak-form Rule B prior remains untouched.

## 5. What WOULD have complicated this reading (did not occur)

Per A-prime, if Comparator epsilon had produced signed structure under this tiny perturbation, the finding would have been that the apparatus floor is highly sensitive to weak coupling â€” which would have made the Rule C near-zero band more interesting and might have motivated a Rule C near-zero densification (object b). It did NOT: the floor is stable. So object (b) (Rule C near-zero densification) is not motivated by this result; it remains a held, optional follow-up, opened only at Mike's call if a sharper Rule C boundary statement is wanted.

## 6. What this finding does NOT do

- Does not resolve the L4 ontological question; neither observable named theoretical Psi.
- Does not harden the weak-form Rule B prior.
- Does not reclassify Rule C or move the Rule C thresholds (Section 3).
- Does not open Rule C near-zero densification (object b; not motivated by this result).
- Does not seed any further probe; seeding remains Mike's call.

## 7. Registry-form summary

> **Comparator epsilon:** weak-neighbor floor audit (epsilon = 0.05, realized delta_p 0.0100 / 0.0200 per anchor). Floor remains near-null / near-null at both anchors under minimal coupling; two isolated marginal exceedances read as finite-sample tail. Supports the A-prime language that the Rule C near-zero band is floor-adjacent weak-coupling tolerance. Comparator epsilon ceiling and Rule C near-zero boundary kept distinct. Rule C near-zero densification (object b) not motivated.
