# Contract E1 — Fixed-Terrain Activation Threshold (Cascade Existence, First Transition)
## Draft v0.5 (resolves all eight v0.4 items; for Mike's review, then L2 re-review)

**Status:** DRAFT. No production run authorized. Carries v0.4 in full except the sections amended below; the accepted production-side verdict architecture (§5) is untouched apart from the router rename and inheritance wording.

---

## A. Naming and inheritance corrections (items 7, 8, + ancillaries)

- **Router rows renamed P2R-1 … P2R-7** (formerly R1–R7); no document of this program uses bare "R1" for the router again — Gate R0/R1 keep exclusive claim to those labels (wrong-values-under-right-names surface closed).
- **Downstream inheritance reworded:** "On LOCATED, the frozen production bracket **[m₋, m₊]** and its transformed Λ-space companion **[m₋³, m₊³]** pass to E2 **solely as search-region inputs.**" No unqualified scalar Λ* exists anywhere downstream.
- **Level identity made exact:** the frozen level list is **generated at six-decimal precision** — the six-decimal value *is* the control value the run consumes, so the seed-key serialization is exact by construction; the frozen list is mechanically verified injective under the format at freeze.
- **T1 renamed "orbit-tail agreement"** (formerly equilibrium agreement) — accurate under cyclic or nonstationary reference orbits.

## B. Null construction amendment — common-rank template (item 5)

§4.2's per-level independent base realizations are **replaced by a common standardized template** (L2's option 1, adopted): one 2500 × 3 matrix of uniform ranks is drawn **once** from the dedicated null-generation Generator and frozen; at every level (production and dense reference grid alike), null bases = (m − w/2) + w · rank. Consequences, stated: (i) the null reference varies **smoothly in m by construction** — m-to-m roughness, artificial U islands, and template-induced crossings are excluded at the source rather than audited away; (ii) the construction mirrors the production sweep's own common paired seed panel; (iii) the conditional-reference ontology stands — thresholds remain conditional on the registered template, and the §7 audit still prices production-to-reference variability. Replicate stochasticity (chain draws) remains per-replicate on level-keyed derived seeds. A **light reference-grid stability spot-check** is retained in the pre-freeze package: threshold structure recomputed under **[PROPOSED]** 3 alternative templates must reproduce the reference structure class (not the exact bracket), else the template sensitivity is escalated to Mike before freeze.

## C. R1-T2 rebuilt (items 1–4)

### C.1 Reference-side classifier (total; item 3)
On the frozen dense grid, each m receives exactly one deterministic label by the frozen production criteria applied to the iterated G_m trajectory, in precedence: **S** (S_min > θ_P), else **N** (S_term ≤ θ_T), else **U**. The reference profile then receives exactly one **structure class**:
1. **ORDER-VIOLATING / MULTIPLE:** any S at strictly lower m than any N.
2. **NO-SUSTAINED-PHASE:** no S anywhere (and ≥ 1 N).
3. **NO-NULL-PHASE:** no N anywhere (and ≥ 1 S).
4. **REFERENCE-UNRESOLVED:** no S and no N (all U), **or** the reference null fails its own §4.2 precision requirement at grid instantiation.
5. **UNIQUE-THRESHOLD:** both phases present, order respected → reference bracket **m₋ᴿ = max{m : label N}, m₊ᴿ = min{m : label S}** (U levels between them are interior uncertainty and are spanned — N,N,U,U,S,S yields the evident bracket).
Classes 1–5 are exhaustive and mutually exclusive; totality verified by the same property-based machinery as §5's.

### C.2 T2-S — threshold-structure recovery (items 1, 2)
Compares the reference structure class with E1's verdict; grammar {RECOVERED / NOT RECOVERED / NOT EVALUABLE}, **total by the frozen table**:

| Reference | E1 result | T2-S |
|---|---|---|
| UNIQUE-THRESHOLD | LOCATED | proceed to T2-L |
| UNIQUE-THRESHOLD | NOT PRODUCED (any category) | **NOT RECOVERED** |
| NO-SUSTAINED-PHASE | LOCATED | **NOT RECOVERED** |
| NO-NULL-PHASE | LOCATED | **NOT RECOVERED** |
| ORDER-VIOLATING/MULTIPLE | LOCATED | **NOT RECOVERED** |
| NO-SUSTAINED-PHASE | NOT PRODUCED (no sustained phase) | RECOVERED (adverse-structure agreement) |
| NO-NULL-PHASE | NOT PRODUCED (no null-consistent phase) | RECOVERED (adverse-structure agreement) |
| ORDER-VIOLATING/MULTIPLE | NOT PRODUCED (order violation) | RECOVERED (adverse-structure agreement) |
| any adverse reference class | NOT PRODUCED of a *different* category | **NOT RECOVERED** (mismatched adverse structures) |
| REFERENCE-UNRESOLVED | any E1 result | NOT EVALUABLE (reference cannot speak; recorded as a reference-structure finding) |
| any reference class | NOT DISTINGUISHED | NOT EVALUABLE |

**The asymmetry is thereby enforced where it was leaking:** a projection threshold that production fails to produce is **NOT RECOVERED** — evidence against the stream-level realization, never non-evaluability; structural mismatches in either direction likewise. NOT EVALUABLE is confined to genuine inability to compare (production instrument limit; reference's own unresolvedness or precision failure).

### C.3 T2-L — threshold-location recovery (item 4)
Evaluated only on the table's first row. **The one-grid-spacing expansion is withdrawn** (non-unique after pass 2; prices resolution but not stochastic bracket displacement). Replacement — a **prospectively derived design-resolution envelope**: the finite-N projection machinery generates **[PROPOSED] 200 complete synthetic projection-side sweeps under the full frozen E1 design** — per level, 20 stochastic finite-N realizations of G_m (2500 independent cells at the map's per-tick probability), classified by the frozen run criteria against the frozen nulls, aggregated by the frozen 16/2/4 count rules, refined by the frozen P2R router, bracketed by the frozen §5 logic. From the replicate brackets: **envelope = [q_2.5 of replicate m₋, q_97.5 of replicate m₊]** **[PROPOSED]** around the deterministic reference bracket. **T2-L RECOVERED** iff the production bracket [m₋, m₊] overlaps the envelope; **NOT RECOVERED** otherwise; **NOT EVALUABLE** iff more than **[PROPOSED]** 20% of replicate sweeps themselves fail to yield a unique bracket (design-resolution limit, recorded — and itself informative: the frozen design cannot reliably resolve its own projection's line). Envelope quantile conventions and replicate seeds frozen pre-production; the ensemble joins the stage-1 package (item 12).

## D. Morphology-cap scoring rule (item 6)
For every audited morphology class, freeze: interval method = **[PROPOSED]** one-sided Clopper–Pearson; confidence level = **[PROPOSED]** 95%; and the pass rule: **the one-sided 95% upper confidence bound on the applicable error rate must be ≤ 10%** (false-ND for scientific-verdict classes; false-scientific-verdict for ND-intended classes). The held-out audit must satisfy the bound; failure **blocks freeze** or triggers prospective gate revision followed by a **fresh held-out audit** (the evaluability analogue of the §4.2 precision halt, symmetry deliberate). Point estimates below cap never suffice.

## E. Stage-1 package additions (item 12)
The pre-freeze deliverables add: the T2-L finite-N full-design sweep ensemble; the template stability spot-check (§B); the dense-grid reference classification and structure class publication. All else carries.

*End of draft v0.5. Sequence: Mike's review → L2 re-review → freeze qualification.*
