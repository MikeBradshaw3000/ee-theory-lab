# Ruling: Retirement of Mesa-Equivalence; Elevation of Spec-Canonicality

**Status: Ratified by Mike in off-protocol discussion, 2026-09-05 ("correct on all counts"; formalization directed before completion of the next contract). Enters the program record on commit. Prior records referring to the equivalence clause remain unedited — historical and correct for their time.**

## 1. Ruling

The equivalence clause's two components are given separate fates:

**Mesa-equivalence is retired as a live obligation.** Equivalence *to Mesa specifically* enforces nothing the program needs. The Mesa twin never needs to exist; the identical-telemetry artifact is never commissioned; "matches what Mesa would have done" adds no epistemic content. Mesa was a dependency of the development history, never of the dynamics (see the substrate-trajectory record).

**Spec-canonicality is retained and elevated as the program's governing principle:** the specification is canonical, and any implementation producing the locked dynamics is a legal realization. Where spec language next touches the equivalence clause, it is renamed accordingly — "spec-canonicality" or equivalent — dropping the Mesa framing.

## 2. Grounds

1. The blind rebuild depends on spec-canonicality entirely: bit-identity as a verification target is meaningful only if the specification, not the artifact, is the referent.
2. The sequence-preserving discipline (cell-by-cell initialization draws; one grid draw per tick) survives on its own merits: it is what allows differently structured implementations to consume the identical PRNG stream, independent of Mesa.
3. The principle guards the program's most dangerous defect class — wrong-values-under-right-names — which is detectable only against an authority outside the code. Collapsing spec into artifact would make such a defect correct by definition.

## 3. Consequential edits

- Next spec revision touching the equivalence clause renames it and drops Mesa framing (same spirit as the v1.1 correction of "implemented in Mesa 3.x").
- Any future blind-rebuild commissioning document inherits this framing: the spec is the referent; Mesa does not appear. (See also the L3-retirement ruling, 2026-09-06, for the exercise's current form.)
- No retroactive edits to committed records.
