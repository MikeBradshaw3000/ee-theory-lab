# Contract E1 — Fixed-Terrain Activation Threshold (Cascade Existence, First Transition)
## Draft v0.6 (resolves all eight v0.5 items; for Mike's review, then L2 re-review)

**Status:** DRAFT. No production run authorized. Carries v0.5 in full except the amendments below. Production-side architecture (§5, accepted) untouched.

---

## A. Reference-side classifier repairs (items 1, 2, 7)

**A.1 Endpoint jurisprudence (parallel to production, item 1):**
- **NO-SUSTAINED-PHASE:** no S anywhere **and the hard top grid point (m = 0.85) is labeled N.**
- **NO-NULL-PHASE:** no N anywhere **and the hard bottom grid point (m = 0.15) is labeled S.**
- If the missing phase could be hidden by U at the relevant hard endpoint (e.g., N,N,U,U or U,U,S,S) → **REFERENCE-UNRESOLVED.** Uncertainty at the family boundary is never an affirmative absent-phase structure — the production jurisprudence, applied to the projection.

**A.2 Off-band U rule (item 2):** with both phases present and order respected, U strictly between m₋ᴿ and m₊ᴿ is interior threshold uncertainty (spanned, as before). **Off-band U allowance [PROPOSED]:** total off-band U ≤ 7 grid points (~1% of 701) **and** no consecutive off-band run > 3 points → UNIQUE-THRESHOLD stands; beyond either bound → **REFERENCE-UNRESOLVED (off-band unresolved).** The allowance is stability-audited (§B); zero tolerance is adopted instead at freeze if the stabilized null construction (§B) makes off-band U vanish in practice.

**A.3 Table wording (item 7):** first row now reads: UNIQUE-THRESHOLD × LOCATED → **T2-S RECOVERED; proceed to T2-L.** Every row assigns one of the three declared statuses.

## B. Dense-grid null stabilization (item 3)

**Claim corrected:** the common base template removes **independent-template roughness only** — not Monte Carlo roughness in the empirical quantiles. Second amendment, removing the second source at construction:
**Common random numbers across m for replicate draws:** replicate j's chain-draw uniforms are generated from a **replicate-keyed** (not level-keyed) derived seed and **reused identically at every m** — one frozen uniform hypercube per replicate, transformed through each level's chain probabilities. θ_P(m), θ_T(m) then vary smoothly in m by construction on both the base and the draw side; residual roughness is confined to the shared-ensemble sampling error already governed by the §4.2 precision halt. (An analytic/DP evaluation of the null statistics remains the permitted substitution if validated — it removes draw-side error entirely.)
**Stability audit (recording displacement, not just class):** dense-grid classification recomputed under **[PROPOSED]** 3 alternative base templates × 2 alternative replicate-seed sets; each recomputation must reproduce the reference **structure class**, and recorded **reference-bracket displacement** must satisfy a frozen scale: **[PROPOSED]** max displacement of either bracket endpoint ≤ Δm_R (the frozen departure-zone width). Displacement beyond that scale → the location gate is not stable enough to freeze; escalate to Mike (freeze blocked pending construction revision). Exact bracket identity is not required (the reference is conditional by registration); survivability of the T2-L-relevant line is.

## C. T2-S finite-design stability (items 4, 5)

**The deterministic reference is compared with production only through a design-stability gate.** The full-design projection-sweep ensemble (T2-L's machinery, one ensemble serving both targets) estimates, for the deterministic reference's structure class, the rate at which the frozen finite design — 20 paired runs/level, frozen classifiers and nulls, 16/2/4 counts, P2R router, §5 verdict function — returns the **matching E1 structural category** when run on the projection object itself.
- **Design-stable iff the one-sided 95% lower confidence bound (Clopper–Pearson) on the matching-category rate ≥ [PROPOSED] 80%** — equivalently, the upper bound on the nonmatching rate ≤ 20%; the v0.5 point-estimate cutoff is withdrawn and this single confidence-bound rule integrates items 4 and 5.
- **If design-stable:** the C.2 table adjudicates — matching production structure → RECOVERED; conflicting → NOT RECOVERED. The asymmetry binds at full strength.
- **If not design-stable: T2-S → NOT EVALUABLE (design-expression limit)** — the frozen design cannot reliably express the deterministic projection's own structure, so production's disagreement with it is not evidence either way; the limit is recorded as a design finding.
- **This gate applies to every deterministic reference class** (UNIQUE-THRESHOLD, both absent-phase classes, ORDER-VIOLATING/MULTIPLE): each class's "matching E1 category" is fixed by the frozen T2-S table itself; REFERENCE-UNRESOLVED needs no gate (already NOT EVALUABLE).
- **Interpretation fence (L2's wording, adopted):** RECOVERED on an adverse-structure row means *the stream-level experiment recovered the projection's adverse structure* — P1 remains adverse in both systems; nothing is thereby supported.
- Ensemble size **[PROPOSED]** 200 sweeps; if the confidence bounds (this section and §D) cannot clear at 200, replicates increase prospectively; persistent failure leaves the frozen rules' NOT EVALUABLE dispositions in force — never a relaxed bound.

## D. T2-L conditioning and precision (item 6)

- **Conditioning (explicit):** envelope endpoint quantiles are computed **from the subset of projection sweeps that (i) return the matching UNIQUE-THRESHOLD structural category and (ii) yield a unique bracket.** Nonmatching/failed replicates are counted in §C's design-stability rate — never silently discarded, never double-used.
- **Pairing fidelity (explicit):** each synthetic sweep reproduces production's common-random-number structure — twenty sweep-internal seed identities held **common across all levels within that sweep**, mirroring the production panel; independent-seed implementations are non-conforming (they would inflate bracket variance).
- **Envelope-endpoint precision halt:** quantile convention Hyndman–Fan type 7 (as elsewhere); endpoint uncertainty by **[PROPOSED]** bootstrap over conditioned replicates (10⁴ resamples, analysis Generator); requirement: **95% CI half-width on each envelope endpoint ≤ [PROPOSED] Δm_R.** Unmet → replicates increase prospectively; unmet after the declared increase → **freeze blocked** (the §4.2/§D halt symmetry, third instance, deliberate).

## E. Level-identity completion (item 8)

Pass-2 values are **rounded to six decimals before duplicate and interiority checks.** Mechanical collision rule **[PROPOSED]:** a colliding inserted value moves to the six-decimal midpoint of its two nearest non-colliding neighbors (existing levels or accepted insertions); if that midpoint also collides, the point is dropped and the drop recorded in the run record — deterministic, no analyst repair. (Collision is geometrically remote at current spacing; the rule exists so identity is earned, not assumed.)

## F. Stage-1 package (item 8 of L2's list, consolidated)

Additions now enumerated: corrected reference classification (A); stabilized dense-grid construction with displacement-recording stability audit (B); full-design structural-stability rates with confidence bounds for every reference class (C); conditioned, precision-adjudicated T2-L envelope (D); explicit sweep-internal pairing (D); collision-rule verification (E); plus all previously named deliverables (conformance preflight, closure publication, fixed-point diagnostic, null benchmarks, morphology audit with held-out re-score, resource actuals).

*End of draft v0.6. Sequence: Mike's review → L2 re-review → freeze qualification.*
