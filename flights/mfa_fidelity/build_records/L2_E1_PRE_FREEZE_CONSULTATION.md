# Note to L2 — E1 Pre-Freeze Consultation: Reference-Structure Finding, Claim-Tier Tension, and Proposed Disposition
**From:** L1, routed by Mike. **Register:** design consultation (pre-freeze; no production data exist). **Date:** 2026-10-02.
**Channel reminder:** returns reach L1 intact only as FILE UPLOADS.
**Authority:** everything below is a PROPOSAL under the standing rule and carries no authority until adopted. Nothing here is executed on L1's initiative. Mike's rulings and your review are both prerequisites to any change.

**What is NOT being asked:** no freeze; no production sweep; no change to the frozen constants, seed panel, grid, contract criteria, or any committed artifact; no lattice-to-theory comparison (held, see §4); no reopening of M1–M6 or the cleared M5. Never-relax (v0.2 §5) binds after production data exist; none exist. This is a design consultation at the one time the contract allows design.

---
## 1. The pre-freeze closure result (provisional until the canonical 701-point job)

R1a (v0.3 §6) requires the closure's fixed-point structure to be computed from the closure alone before any E1 data and published pre-freeze, with "absence of a predicted threshold in the closure … a form finding, never an apparatus failure." M5 (cleared SOUND, 2026-10-01) computes exactly that closure:

    G_m(ρ) = E_{Λ~D_m}[ η_floor + (1−η_floor)·σ(αΛ + βρ − δρ² − γ_offset) ],   α=4, β=3, δ=4, γ_offset=4, η_floor=0.01,

16-node Gauss–Legendre on the triple-product cube (converged GL8 = GL16 = GL32 to 1e-17; Monte Carlo agreement to its noise floor; template-mean difference = the measured between-draw variability), iterated directly from ρ₀ = 0.5.

**Sampled census (coarse grids of 5–15 levels; the 701-point reference of record has not run — your outcome-hygiene ruling of 2026-10-01 governs its status):**

| m | orbit tail = projected S_min | reference θ_P | θ_T | null mean | lift over null |
|---|---|---|---|---|---|
| 0.150000 | 0.029622 | 0.027928 | 0.028484 | 0.028046 | 5.6 % |
| 0.300000 | 0.031674 | 0.029700 | 0.030271 | — | — |
| 0.515217 | 0.044733 | 0.040564 | 0.041228 | 0.040697 | 9.9 % |
| 0.700000 | 0.097193 | 0.078724 | 0.079629 | — | — |
| 0.850000 | 0.281034 | 0.191968 | 0.193275 | 0.192869 | 45.7 % |

Every sampled level is labelled S; one stable fixed point at every level; no count change anywhere. Expected structure class **NO-NULL-PHASE** (v0.6 A.1: bottom point S, affirmatively). A single null window mean has sd ≈ √(100·2500·0.028·0.972)/250000 ≈ 3.3e-4, so the closure's S_min sits ≈ **5 null-sd above θ_P at the hard floor** m = 0.15 (admissibility m − w/2 ≥ 0 makes 0.15 a hard floor: no lower endpoint exists to choose).

**Finite-N confirmation on the projection side:** projection sweep #0 — twenty per-seed finite-N realizations of G_m per level from each seed's own replayed bases, scored against each seed's own conditional null through the frozen 16/2/4 counts, the frozen router, and the frozen verdict function — returned **S at all 24 pass-1 levels (20/20 SUSTAINED at m = 0.15)**, verdict NOT_PRODUCED / no_null_consistent_phase, rule 2: the matching E1 category. The interacting chain's variance does not rescue the null.

**The structural reason (the part that is a theorem about the rule, not a measurement):**
- The production null (M3, amended 2026-09-21) keeps the terrain drive αΛ_i − γ_offset and the η_floor and removes only the density terms. The feedback term βd − δd² = d(3 − 4d) is **strictly positive for 0 < d < 0.75**, so the interacting drive exceeds the null's drive at every terrain value; the only question was detectability, answered above.
- The symmetric chain is **memoryless per cell**: p_act_i depends on neighbours' density and never on cell i's own prior state. There is no deactivation process to be overcome. "Sustained activation" under this rule names a density steady state, not persistence of anything, and a threshold where self-reinforcement exceeds decay is not expressible in it.

**Consequence as the contract itself specifies it:** v0.4 §5 rule 2 (placed in M4): confident-S bottom → NOT PRODUCED (no null-consistent phase). v0.5 C.2 / v0.6: production NOT PRODUCED (no null-consistent phase) against reference class NO-NULL-PHASE → T2-S RECOVERED under the interpretation fence ("the stream-level experiment recovered the projection's adverse structure — P1 remains adverse in both systems; nothing is thereby supported"); T2-L never runs; the departure zone is empty; T1/T3 report per their grammar. **E1's predicted verdict is therefore foreordained by the rule's form; production would test only whether the lattice agrees with its closure.**

## 2. The design question (Finding 3): the claim tier and the object disagree

- v0.2 §1: "**Claim tier:** P1, core-architecture jeopardy per the jeopardy split … impose[s] no onset-shape content (§5's line-not-drama rule)."
- v0.2 §5: NOT PRODUCED is "a substantive adverse finding against the single-first-transition architecture, not an instrument limit."
- Line-not-drama makes a located threshold, by construction, a null-relative **detection boundary** at the frozen resolution; the contract never claims it marks a change of dynamical structure, and v0.4 §6 demoted the census — the only instrument that can see such a change — to a diagnostic that "determines nothing about T2."

The tension: if the object is a detection boundary, its absence is a fact about detection under this rule and null and cannot be core-architecture jeopardy; if it is architecture jeopardy, the object must be a change in dynamical structure, which only the census sees. **Proposed resolution for your adjudication:** NOT PRODUCED (no null-consistent phase) under this rule is adverse to *the substrate's claim to realize the first transition* — consistent with the contract's own jurisdiction discipline ("in these worlds under this instrument, family, and declared search surface") — and the P1 claim tier must say so rather than "core-architecture jeopardy." This is a design question; never-relax does not apply.

## 3. Proposed disposition (Mike's, adopted jointly; for your review)

**(a) Reclassify E1 as an instrument-validation flight** and complete it as such: M1–M6 (placed), the exact Poisson-binomial conditional null with its qualified 7,580-threshold cache, M5's closure/recovery machinery (cleared), and the T1–T3 lattice-to-closure recovery, with the P1 claim tier removed. These are the apparatus any successor needs.

**(b) Design a Flight 8 rule that can bear on P1** (not a patch; a new rule, its own contract): per-cell memory with an explicit deactivation probability; Λ-gated feedback; the floor retained as the irreducible spontaneous-action term; **null defined by feedback removal (g₀ = 0)** rather than density-term removal with terrain drive on. Expected closure census: a transcritical crossing at g₀Λ ≈ β, giving a pre-registerable bracket prediction; its absence in the census would be the first genuine adverse finding available to the lab.

**Apparatus cost named now:** per-cell memory changes the null's law. M3's exact construction depends on ticks being independent draws; under a deactivation probability each cell is a two-state Markov chain — still independent across cells under feedback removal, so exact per-tick marginals remain computable, but window sums are no longer convolutions of independent ticks and S_min over ten windows needs the temporal correlation. **M3 and the cache artifact need redesign; M1, M2, M4, M6, and M5's closure machinery carry over essentially intact.**

**Option (c)** — run E1 as specified and downgrade the claim tier in the write-up — is listed for completeness and not preferred: the pre-registration's own language would have to be contradicted after the fact.

## 4. Finding 1 (theory/substrate divergence) — for your view; the ruling is Mike's

The committed Overview v1.72 §10 writes the first transition as a Landau normal form on ρ, dρ/dt = α(Λ − Λ*)ρ − βρ³ + η(t) (§15: supercritical forms are "a committed working hypothesis … [that] could fail while the architecture's deeper commitments survive"); §12 carries Ψ with μ(ρ). Mike's theory work holds ρ in a substrate-level activation equation with a floor (Λ-gated feedback, explicit decay, no overcrowding term) and reserves the cubic for Ψ. The precise statement: both that equation and G_m are substrate-level objects; §10 is the theory's normal form; neither substrate currently has §10 as its normal form. Mike's proposal: since ρ is bounded and nonnegative the cubic's ρ → −ρ symmetry is unphysical, and the generic normal form with a floor is **transcritical**, dρ/dt ≈ (g₀Λ − β)ρ − cρ², with the floor as the imperfection parameter (Λ* = β/g₀); §10 to be rewritten accordingly, the cubic retained at §12. Also for the record: §10's η(t) is unlabelled in v1.72 (Landau convention and §14's "fluctuations near threshold" read it as noise), and it collides by letter with the substrate's η_floor constant.

The third-order lattice-vs-ODE comparison is **held** until §10 is settled: the expansion target depends on it. The activation ODE and the "three-case falsifiability distinction" are not yet in the repository.

## 5. Questions for L2

1. Do you concur that, on the structural argument in §1, NOT PRODUCED is foreordained under the frozen rule and null, independent of the dense census (which will still be run as the reference of record)?
2. Finding 3: do you accept the proposed resolution of the claim-tier/object tension, or rule otherwise?
3. Disposition: any objection to (a) + (b)? Any requirement on how E1's instrument-validation record is to be closed (which canonical jobs — dense census, 200 projection sweeps, tolerance ensembles — retain value under (a))?
4. Flight 8 minimal rule: anything in the four-part specification you would require changed or added before contract drafting begins, including the null-by-feedback-removal definition and the Markov-null cost?
5. Finding 1 / §10: your view on whether the transcritical rewrite is the §15-sanctioned kind of failure of the committed working hypothesis, and on the η(t)/η_floor collision.

**Standing items untouched:** M5 placement (cleared; pending the repo machine); M7 (the stage package binding placed identities) if E1 continues as instrument validation; Mike's open rulings (halt policy; Δm_stab/Δm_est; stability axis 2; T2-L failure disposition; [PROPOSED] values).

---
End of consultation. — L1
