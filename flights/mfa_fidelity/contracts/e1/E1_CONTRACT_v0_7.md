# Contract E1 — Fixed-Terrain Activation Threshold (Cascade Existence, First Transition)
## Draft v0.7 (resolves all five v0.6 items; for Mike's review, then L2 re-review)

**Status:** DRAFT. No production run authorized. Carries v0.6 in full except the amendments below. Production architecture and T2-S structure bridge (accepted) untouched.

---

## A. Dense-grid claim and stability-audit grammar (items 1, 2)

**A.1 Claim corrected (L2's wording adopted in substance):** common ranks and common replicate uniforms **couple the reference construction across m and remove independent template and independent-seed jitter. They do not by themselves guarantee mathematical smoothness or threshold stability** — the realized thresholds are empirical order statistics of thresholded uniforms and remain stepwise; local classification changes are still possible. **The pointwise precision halt and the pre-freeze dense-grid stability audit jointly establish whether the resulting reference structure is stable enough to use.** The construction mirrors production's across-m common-random-number *principle*, not its ensemble — production carries twenty seed-specific templates; the reference carries one registered template. All stronger claims are withdrawn.

**A.2 Stability-audit grammar (total across classes):** for each alternative construction (3 templates × 2 replicate-seed sets):
- Primary reference class **UNIQUE-THRESHOLD:** require structure-class agreement **and** endpoint displacement of both m₋ᴿ, m₊ᴿ within the frozen stability scale (**[PROPOSED]** ≤ Δm_R).
- Primary class **adverse** (NO-SUSTAINED / NO-NULL / ORDER-VIOLATING) or **REFERENCE-UNRESOLVED:** require structure-class agreement only — no bracket-displacement statistic exists.
- **Any structure-class change under any alternative → freeze blocked** (construction revision, prospective, then full re-audit).
- **Every alternative calculation must itself clear the §4.2 pointwise quantile-precision requirement** before its classification counts — a class change from an inadequately estimated alternative threshold is a precision failure, not a stability finding.

## B. T2-L envelope-informativeness gate (items 3, 4)

**Two distinct requirements, named as distinct epistemic quantities** (per L2; they may share a numerical value at freeze but are never conflated): *estimation precision* (§D's bootstrap CI halt — do we know the endpoints?) and *design-location resolution* (this gate — is the interval a target?).

**Informativeness rule (frozen before production):** with envelope [L_env, U_env] and deterministic reference bracket [m₋ᴿ, m₊ᴿ], require
**m₋ᴿ − L_env ≤ Δm_L and U_env − m₊ᴿ ≤ Δm_L** (equivalently U_env − L_env ≤ (m₊ᴿ − m₋ᴿ) + 2·Δm_L),
where **Δm_L [PROPOSED] = one pass-1 spacing** — a Mike-level design value, flagged as such; it prices the finite design's actual ability to localize the reference line and is deliberately distinct from Δm_R's two prior roles (reference-construction stability; endpoint-estimation precision), which themselves remain distinct quantities that currently share a proposed value and may be set independently at freeze.

**Disposition on failure [PROPOSED — Mike's choice, both coherent per L2]:** **T2-L → NOT EVALUABLE (design-location resolution insufficient)** — the T2-S structural result is retained in full force; the resolution limit is recorded as a design finding informing successor design. (The alternative — freeze blocked pending prospective design improvement — remains available at Mike's word; the proposed disposition keeps the structural bridge's verdict while refusing to let an uninformative interval manufacture location recovery.) Under failure, **bracket overlap may not yield RECOVERED under any circumstances.** The gate is adjudicated in stage 1 from the frozen ensemble, before production.

## C. Six-decimal collision algorithm (item 5, completed)

The fallback is fully deterministic, or provably unreachable — one of the two, established at freeze:
1. **Proof path (preferred if it closes):** mechanical pre-freeze check that no P2R output under the frozen six-decimal pass-1 grid can produce a collision (all refinement-interval widths and insertion arithmetic enumerated); if proven, the fallback is removed as unreachable.
2. **Fallback (if not proven), frozen completely:** candidate insertions processed in **ascending nominal m**; midpoints rounded at six decimals by **round-half-to-even [PROPOSED]**; **accepted moved points are eligible neighbors for subsequently processed candidates**; a moved value must remain **strictly interior to its original P2R refinement interval and preserve strict sorted order** against all accepted levels — failing either, the candidate is **dropped**; every move and drop is recorded in the run record and **mirrored identically** in the projection-side full-design sweeps, null instantiation, resource accounting, and final run record. Two conforming implementations produce identical level lists by construction.

## D. Stage-1 package (consolidated additions)

Adds: the corrected construction claim and class-total stability grammar with alternative-precision compliance (A); the envelope-informativeness adjudication, reported separately from endpoint-estimation precision (B); the collision proof or deterministic-fallback test (C); final ensemble sizes after all prospective increases; all prior deliverables carried.

*End of draft v0.7. Sequence: Mike's review (Δm_L value and the failure disposition are the two Mike-level calls) → L2 re-review → stage-1 freeze qualification.*
