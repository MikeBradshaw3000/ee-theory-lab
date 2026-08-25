# L2 Review — Contract E1 Draft v0.7

> **Archival re-export status:** The five changed-text requirements are preserved from the final v0.7-to-v0.8 correction round.

## Overall verdict

**ALL FIVE v0.6 SUBSTANTIVE ITEMS ARE RESOLVED IN INTENT. FIVE TEXTUAL CORRECTIONS ARE REQUIRED BEFORE FREEZE.**

These are precision corrections, not an architectural reopening.

## Correction 1 — Remove false equivalence in the informativeness rule

The text must not equate “reference classifier is informative” with “reference result matches the expected single-threshold pattern.” Informativeness means the frozen classifier can issue a determinate, interpretable result—including adverse structural nonrecovery. Rewrite the rule so an adverse but determinate T2-S result is informative rather than treated as an instrument failure.

## Correction 2 — Name all three resolution scales distinctly

The document must not use one generic “resolution” for different objects. At minimum distinguish:

1. production pass-one/control-grid resolution;
2. production pass-two threshold-bracket resolution; and
3. MFA reference-grid/stability resolution.

Where both primary and stability reference grids are retained, their symbols must remain distinct within the third family. No tolerance may be defined by an ambiguous bare `Delta`.

## Correction 3 — State exact spacing conventions

For every grid, specify whether spacing means requested rational spacing, exact floating-point values, or spacing after canonical serialization. State endpoint inclusion and the rule for inserted points. Rounded display values are not the normative design.

## Correction 4 — Make T2-L explicitly primary-relative

T2-L must compare the production bracket to the **primary** MFA reference threshold envelope. The stability grid tests whether that primary result is reliable; it does not replace the primary envelope with whichever grid gives the more favorable comparison. State this asymmetry directly.

## Correction 5 — Deterministic collision proof or fallback

The control-value construction must either prove that canonical serialization cannot collapse two distinct requested points or define a deterministic fallback before data. The fallback may increase precision or use exact ordinal IDs, but may not silently deduplicate, perturb values by inspection, or choose a nearby point after seeing results.

## Required return

A v0.8 changed-text packet carrying only these corrections is sufficient. L2 will verify each as **CORRECTED AS REQUIRED** or identify the remaining defect.

## Freeze disposition

**FREEZE MAY NOT YET PROCEED.**

No substantive blocker remains beyond the five textual corrections above.
