# Flight 8 — Design Note v0.1 (design chamber; not a contract)

**Status.** L1 design draft, 2026-10-20, at Mike's word ("draft flight 8 design"). Repository `main` at `3cc30fe`. This note is the design chamber's proposal for the successor mechanism class; it binds nothing. Its §6 is the material of the **repair-design packet** L2 permitted on 2026-10-20 (`L2_E1R_M6_ONSET_DIAGNOSIS_DISPOSITION_RECEIVED.md`, `eaa694a98c7063e4`: "a separately reviewed repair-design packet … followed by Flight 8's prospective guard and qualification requirements"). The contract is drafted only after Mike rules on §9 and L2 disposes of §6.
**Register.** Design evidence in §6 was computed on the two burned E1-R ensembles (L2 §4.2) and is **design evidence only**; it qualifies nothing. Every number in this note that is not a committed identity was computed by a script named in §10, not by hand.
**Notation (ruling §3 option (a); table governs).** This note uses the contract names of the amendment §9: **μ is the deactivation rate** — the Overview's lapse rate β; *not* the Overview's coherence coefficient μ(ρ). **g** is the feedback gain (the Overview's g₀), **h** the spontaneous-action floor (the Overview's spontaneous term; the frozen specification's η_floor is its symmetric-chain image), **ξ_ρ(t)** the fluctuation term (the specification's η_MFA), **λ_i** per-cell conduciveness (the Overview's Λ at the cell), **d_i** the Moore-neighbourhood active fraction (`density/8`, D2 ruling). The specification's β (density-coupling coefficient) does not appear in Flight 8's rule.

---

## 1. What binds this design before a line is written

| Source | What it fixes |
|---|---|
| E1-R amendment §6 (`04058b21…`) | Flight 8 is a separate successor contract, not a patch to E1; **E1 data must not tune its gates**. |
| Amendment §7, pre-freeze §4.7 (`314b56cc…`) | Primary P1 object is **structural**: a fixed-point/stability change in the zero-floor closure at the pre-registered Jacobian crossing, with the positive-floor realization showing the predicted rounded continuation. A null-relative detection boundary may remain a secondary finite-design observable; it is never P1's definition. |
| Amendment §8, pre-freeze §4.3 | Two objects: **zero-floor structural skeleton** (h = 0; exact crossing) and **positive-floor committed realization** (h > 0; rounded unfolding). No claim of an exact transcritical crossing in the positive-floor system. |
| Pre-freeze §4.1–§4.2 | An **exact discrete-time rule** must be frozen before any normal form is asserted; the discrete crossing is pre-registered, the continuous equation is its limit. |
| Pre-freeze §4.4, §4.6 | All terrain dependence relevant to the crossing explicit; the null retains everything except endogenous feedback; for the primary flight: bases frozen, Q disabled, exogenous drive zero, noise off, timing and topology fixed; low- and high-activity initializations as a hysteresis diagnostic. |
| Pre-freeze §4.5 | Projection-level bracket and lattice-level spectral prediction pre-registered as related but distinct objects. |
| Pre-freeze §4.8 | The null is rebuilt as independent two-state Markov chains; E1's M3 convolution of independent ticks **cannot be reused**; S_min needs a certified joint construction, a conservative familywise bound, or a separately qualified simulation threshold. |
| Pre-freeze §4.9 | Carry-over by module (M1 scaffolding may; transition rule may not; M3 redesigned; M6 architecture carries, calibration rerun; cache rebuilt). |
| L2 disposition 2026-10-09 (`3f101a1b…`) §4.2 | Both E1-R ensembles burned as guards; fresh prospectively registered guard; new instrument version and stage identity; qualification passage before production. |
| L2 disposition 2026-10-20 (`eaa694a9…`) | Repair surface bounded to M4's 4c/router resolution relation and the M6 archetype-width declaration; no threshold, count or width pre-approved; M2/M3 not pre-approved unchanged under the new instrument. |
| Mike's ruling 2026-10-15, three conditions | (1) diagnosis before design — **discharged** (`bd5f16e`); (2) qualification on a fresh guard with the archetype table frozen first; (3) zero-floor skeleton as the first canonical scientific job. |
| PD1–PD7 (`1b486323…`) | Participation grammar; W is a declaration per PD5 (one tick in E1; Flight 8 declares its own); the first transition is a statement about persistence under coupling (PD7). |
| Notation-scope ruling (`c275c38f…`) | §3 option (a); the table governs; Flight 8 adds rows, rewrites none. |
| Amendment §10 | The third-order lattice-versus-ODE comparison stays **held** until the discrete-to-continuous bridge (§3 below is the candidate) and the successor rule (§2) are settled. |

## 2. The substrate rule (exact, discrete time)

Per cell *i* on the frozen L×L Moore lattice, state x_i(t) ∈ {0, 1}, tick length Δt = 1. Synchronous two-phase advance as in the frozen skeleton (spec v0.4 §1.2): read phase computes every cell's probabilities from the state at *t*; one full-grid uniform draw; simultaneous advance.

- **Conduciveness** λ_i = F(v_i, u_i, r_i), the frozen F dispatch, per cell, from bases frozen for the whole run (Q disabled; Γ = 0; exogenous drive u_t = 0).
- **Local density** d_i(t) = active fraction of the eight Moore neighbours (`density/8`).
- **Activation** (x_i = 0 → 1): P = 1 − exp(−[h + g·λ_i·d_i(t)]·Δt).
- **Deactivation** (x_i = 1 → 0): P = 1 − exp(−μ·Δt).
- **Nothing else.** No overcrowding term, no γ_offset, no σ(drive) chain: the symmetric chain's probability construction is not layered under this rule (the spec's own warning against inferred layering, §1.2, applies in the other direction here). Noise off for the primary flight (ξ_ρ ≡ 0).

**Terrain dependence.** All conduciveness enters through the feedback channel g·λ_i·d_i (pre-freeze §4.4 option 1). At h = 0 the all-inactive state is therefore exactly absorbing on every terrain, which is what makes the skeleton's crossing exact. A terrain-only activation drive is excluded from the primary flight by construction, not by argument.

**Two committed objects.** The **skeleton**: h = 0. The **realization**: h = h₀ > 0, a value declared in the contract (candidate: the value that makes the hazard floor's single-tick probability equal the symmetric chain's η_floor = 0.01, i.e. h₀ = −ln(1 − 0.01) ≈ 0.01005; stated so the Overview's spontaneous term has one committed image — Mike's declaration, §9).

**Participation grammar.** A cell active at a tick *registers* at that tick (PD7: an event); W = one tick is the instrument's declaration of the participation window (PD5), stated in the contract as a declaration, not an architectural truth; density ρ counts registrations; persistence is the fourth question and is what the crossing is about.

**Null (g = 0).** Identical rule with the feedback term removed: activation P = 1 − e^(−h·Δt), deactivation P = 1 − e^(−μ·Δt), same h, same μ, same initialization, same timing, same bases (which now do nothing), same drive state. Each cell is an independent two-state Markov chain. At h = 0 the null is the absorbing all-inactive state (trivial); the null that matters is the realization's, h = h₀.

## 3. The closure: mean-field map, crossing, and what is pre-registered

**Homogeneous mean-field map** (every cell sees d_i = ρ; λ_i = λ̄):

ρ_{t+1} = (1 − ρ_t)·[1 − e^(−(h + gλ̄ρ_t)Δt)] + ρ_t·e^(−μΔt).

**Skeleton (h = 0).** ρ = 0 is a fixed point. Its multiplier is J₀ = e^(−μΔt) + gλ̄Δt. **Pre-registered crossing:** J₀ = 1, i.e. **gλ̄Δt = 1 − e^(−μΔt)**. Define the dimensionless crossing coordinate

**m := gλ̄Δt / (1 − e^(−μΔt))**,

so the skeleton predicts: for m < 1 the inactive state is stable (ρ* = 0, perturbations decay as J₀^t); for m > 1 it loses stability and a positive fixed point ρ*(m) appears continuously from zero. This is the transcritical form of Overview v1.8.1 §10 in discrete time; gλ̄ ≈ μ (Λ* = β/g₀ in the Overview's letters) is its small-Δt limit, not the substrate equation. The map's positive branch is computed numerically from the fixed-point equation and pre-registered as a table over m.

**Realization (h = h₀).** ρ = 0 is not a fixed point; the branch is rounded. Pre-registered: ρ*(m; h₀) from the same map — small and non-accumulating below m = 1, rising steeply through it, with the width of the rounding set by h₀ (the Overview's "imperfection parameter"). The rounding width is a derived quantity the contract states numerically; it is what the instrument's resolution (§6) must be set against.

**Lattice-level prediction** (pre-freeze §4.5). On the heterogeneous lattice the linearization at the absorbing state is governed by the leading eigenvalue of g·Δt·diag(λ_i)·A/8 + e^(−μΔt)·I, where A is the Moore adjacency; the crossing is where that eigenvalue reaches 1. For the primary flight the bases are frozen **homogeneous** (λ_i = λ̄ for all i), so the projection-level and lattice-level crossings coincide exactly and the spectral object is pre-registered as the comparator for the later heterogeneous run, not as a second P1 test. (Design choice, §9.)

**Control parameter and sweep.** The sweep variable is m, realized by holding μ, g and Δt fixed and setting λ̄ through the frozen homogeneous bases (one F dispatch, one base triple per level). Levels in exact integer micro-units as in E1 (the M1 scaffolding carries). The sweep spans m ∈ [m_min, m_max] with the crossing interior and the skeleton's positive branch resolvable above it.

**Finite-size and run-length.** The skeleton's inactive state is absorbing, so a finite lattice initialized active *always* dies out eventually for m < 1 and survives for a time growing with L for m > 1; the pre-registered observable below m = 1 is the decay rate (J₀^t), above it the quasi-stationary density over the tail window. Tail and window lengths are declared (M2's `TAIL_LEN`, `WINDOW` carry as scaffolding; values re-declared).

**P1 tests, pre-registered (structural).**
- **T-S1 (skeleton crossing).** The measured stability boundary — the m at which the tail-window quasi-stationary density departs from the absorbing state — lies within a declared bracket of m = 1. Tolerance Δm declared from the map's own finite-size prediction, not from data.
- **T-S2 (no hysteresis).** Low- and high-activity initializations produce the same boundary within Δm; a saddle-node signature (two boundaries) fails P1.
- **T-R1 (rounded continuation).** The realization's ρ*(m) agrees with the map's h₀-rounded branch within a declared tolerance band across the sweep.
- **Secondary (finite-design):** the null-relative detection boundary located by the instrument (§6) — the successor of E1's LOCATED — and Mike's held run-length probe candidate (flicker run-length statistics near m = 1 invariant across W; PD rulings record, "noted, not ruled"): both observables, neither a P1 definition.

**The bridge.** This §3 is the candidate discrete-to-continuous bridge amendment §10 holds the third-order lattice-versus-ODE comparison against: the map is exact for the homogeneous closure; the ODE dρ/dt = gλ̄ρ(1−ρ) − μρ + h(1−ρ) is its Δt → 0 limit. The comparison stays held until Mike accepts this bridge and L2 has reviewed the rule.

## 4. The Markov null and the threshold object

Under g = 0 each cell is the two-state chain with a_i = 1 − e^(−h₀Δt), q_i = 1 − e^(−μΔt), homogeneous across cells in the primary flight. Frozen with it: initialization (the chain's stationary distribution, π₁ = a/(a+q), so no burn-in is needed — or the all-inactive state with a declared burn-in; §9), transition timing, and the fact that a_i, q_i do not depend on the bases.

**What E1's M3 cannot give.** The per-seed conditional null of E1 convolved independent per-tick Bernoulli counts; here ticks are correlated within a cell, so the window occupancy of one cell is a Markov-binomial and the ten window totals are jointly correlated.

**Design choice (for L2).** Three admissible routes per pre-freeze §4.8:
- (a) **certified joint construction** — a transfer-matrix / dynamic-programming computation of the joint law of the ten window totals (exact for one cell; across N = L² independent cells a convolution; feasible since the per-cell transfer matrix is 2×2 and the window total ranges over 0..WINDOW);
- (b) **conservative familywise bound** — per-window exact marginal thresholds with a Bonferroni-type correction over ten windows;
- (c) **separately qualified simulation threshold** with explicit finite-sample coverage, the route E1's cache qualification already exercised.

Recommendation: **(a) for θ_T** (terminal-window statistic: single window, exact) **and (b) or (c) for θ_P** (S_min over ten windows), stated as the M3 declaration with its identity. Thresholds cached per level as before (the cache artifact is rebuilt; the production/slice role discipline and the qualification record carry).

## 5. Instrument: what carries, what is rebuilt, what is repaired

| Module | Carry-over (pre-freeze §4.9 + diagnosis) | Flight 8 |
|---|---|---|
| M1 grid/config | Scaffolding, level grid in micro-units, seed-panel derivation rule | **New rule** (§2); new parity gates for the hazard construction; new frozen identity |
| M2 run status / level label | Statistics carry (S_min, S_term over tail windows; 16/2/4 label counts) **if retained** | Retained as the secondary-observable classifier; null calibration changes (§4); not pre-approved unchanged (L2) — it is re-qualified under M6 like everything else |
| M3 null | **Redesigned** (§4) | Markov null; new cache |
| M4 verdict / router | Rules 1–3, 4a, 4b, router rows, collision fallback carry **as transcribed** (diagnosis: none implicated) | **Rule 4c replaced** (§6); router insertion count re-declared |
| M5 closure | Framework carries | Equations, census, tolerances, predictions rebuilt from §3 |
| M6 morphology audit | Architecture carries (design + held-out, CP cap, qualification join) | Archetype table rebuilt (§6.4); fresh masters (§7); null generation per §4 |
| M7 records / package | Grammar carries unchanged (adverse-but-valid; package completion and production readiness as separate derived states) | New stage identity; new instrument version string |

New instrument version: a new package namespace (`mfa_instrument/f8/`) beside `e1/`, nothing in `e1/` modified; the frozen E1 identities stay what they are.

## 6. The repair: rule 4c, the router, and the archetype-width declaration

### 6.1 The defect, restated from the accepted diagnosis
Rule 4c as frozen rejects a band whose *interior level count* after pass 2 exceeds 3, while P2R-5/6 insert 8 levels into that band. The count is therefore a limit on the *physical width* of the mixing region relative to the band — a steepness criterion in all but name, which the contract's binding line-not-drama clause forbids. The accepted location: 4c in interaction with P2R-5/6 densification and the M6 archetype widths. L2 bounded the repair surface to exactly these three.

### 6.2 Pricing of candidate rules (design evidence only; burned ensembles; ideal M2/M3)
Rules 1–3, 4a, 4b, the router and the generator held frozen; only the 4c criterion varied; all 12,000 committed sweeps replayed (`replay_full.py`, `price.py`). Errors per class, design/held-out; the cap allows at most **38/500** (CP upper 95% of 38/500 = 0.0984; 39/500 = 0.1006).

| Candidate 4c | gentle_onset | abrupt-kind (3 classes) | wide_mixed_boundary | unresolved_heavy | others | passes cap? |
|---|---|---|---|---|---|---|
| **count > 3** (frozen) | 500/500 | 59/54, 37/38, 50/58 | 0/0 | 0/0 | ≤ 2 | **no** (the committed result) |
| count > 4 | 500/500 | 9/10, 8/5, 10/3 | 0/0 | 0/0 | ≤ 2 | no |
| count > 6 | 438/444 | 0 | 0/0 | 0/0 | ≤ 3 | no |
| count > 8 | 170/188 | 0 | 1/0 | 0/0 | ≤ 7 | no |
| count > 10 | 2/4 | 0 | **55/58** | 8/4 | ≤ 7 | no |
| count > 12 | 0/0 | 0 | 337/335 | 110/105 | ≤ 7 | no |
| pass-1 count > 3 | 5/5 | 0 | 52/59 | 0/0 | ≤ 7 | no |
| **physical width > 100k** | 33/42 | 0 | 11/5 | 0/0 | ≤ 7 | no (42) |
| **physical width > 110k** | **7/8** | **0** | **32/36** | **0/0** | ≤ 7 | **yes** — barely |
| physical width > 120k | 2/4 | 0 | 55/58 | 0/0 | ≤ 7 | no |
| physical width > 130k | 0/1 | 0 | 75/81 | 0/0 | ≤ 7 | no |

(Physical width = m of the lowest confident S minus m of the highest confident N after pass 2, in micro-units.)

### 6.3 What the pricing says
1. **No count-based limit works at any value.** The count that frees gentle_onset (≥ 10) is the count that starts failing wide_mixed_boundary. The form, not the number, is wrong.
2. **A physical-width limit is the right form** — it is a declared instrument resolution, independent of how many levels the router inserts, and it passes line-not-drama by construction: an onset of any gentleness narrower than the declared resolution is LOCATED.
3. **But the E1 archetype table defeats even the right form.** `gentle_onset` (mixing window 60–120k) and `wide_mixed_boundary` (150–250k) are the *same generator at different widths*, and their post-pass-2 bands overlap: gentle reaches 135k, wide starts at 76k. A single width threshold separates them only at W ≈ 110k, and only just (7/8 vs 32/36 against a budget of 38). The table draws the locatable/unresolvable line *inside the instrument's own resolution*. That is the second half of the defect, and it is the half L2's disposition named as "the M6 archetype-width contract".

### 6.4 The repair proposed for Flight 8 (for L2's review; nothing pre-approved)
**(R1) Rule 4c becomes a declared physical resolution.** "NOT DISTINGUISHED (boundary unresolved) iff, after pass 2, the uncertain extent of the band — m(lowest confident S) − m(highest confident N) — exceeds **W_res**, a width in micro-units declared in the contract." Rules 1–3, 4a, 4b and their precedence unchanged. The router's insertion count stays 8 (P2R-5/6) unless L2 prefers it re-derived from W_res; the count no longer interacts with the verdict.

**(R2) W_res is set from the theory, not from the audit.** Flight 8's predicted morphology is the h₀-rounded transcritical crossing (§3). The contract computes the rounding width w_round from the committed h₀ and the map, and declares **W_res = c · w_round** with the multiplier c (candidate: 2) stated and justified before any ensemble is drawn. E1 data play no part (amendment §6).

**(R3) The archetype table is rebuilt with a guard gap.** Locatable scientific archetypes have mixing widths ≤ W_res/(1+γ); unresolvable ones ≥ W_res·(1+γ), with the gap γ (candidate: 0.5) set from the pass-2 resolution (one insertion spacing each side). The E1 pair gentle/wide-mixed is replaced by: `crossing_onset` (the §3 realization's own rounded profile, drawn with width w_round·U[0.5, 1]), `gentle_onset` (linear ramp, widths up to W_res/(1+γ)), `abrupt_onset`, `nonmonotone_amplitude`, `persistent_nonstationary_high_m`; the ND side keeps `wide_mixed_boundary` (widths ≥ W_res(1+γ)), `unresolved_heavy_boundary`, `off_band_mixture`, `off_band_unresolved`; the NP side keeps the four of E1 with `no_null_consistent_anywhere` reinterpreted for the absorbing skeleton. Widths in the table are in the same micro-units as W_res, so the table and the rule are checkable against each other by inspection.

**(R4) Line-not-drama restated for the successor.** "No criterion references jump size, slope, amplitude monotonicity or adjacent-level separation; the only width-bearing criterion is the declared resolution W_res, which bounds what the instrument can resolve, not what the theory may produce; any onset narrower than W_res is LOCATED regardless of its steepness." The resolution declaration has the same status as W (PD5): existence committed, value declared.

**(R5) What the pricing is and is not.** It establishes the *form* of the rule and the *fact* that the table must carry a gap. It does **not** set W_res — the number comes from §3's rounding width, which does not exist until the rule (§2) and h₀ are committed. No value in §6.2 is proposed as Flight 8's.

### 6.5 Rejected alternatives (recorded)
- *Lower the insertion count* (e.g. 2): fewer levels inside the band so count-3 passes — hides the defect by reducing resolution; the bracket gets worse, not the rule.
- *Narrow the archetype widths to fit count-3* (gentle ≤ 40k): redefines the morphology to suit the instrument; violates line-not-drama.
- *Evaluate 4c on pass-1 only*: priced above (5/5 gentle, 52/59 wide) — the wide class leaks because ~10% of its sweeps happen to straddle ≤ 3 pass-1 levels; a count form again.
- *Keep count-3 and declare the four failing classes out of scope*: L2's rank-3 rejection, in other clothes.

## 7. Qualification plan (condition 2)

1. **Freeze order.** Contract text (rule, map, predictions, W_res, archetype table with gap, M3 route, cap 0.10, CP one-sided 95%, 500 sweeps/class) → instrument version identity → **then** the guard masters are drawn by a declared rule from a declared seed, their identities committed, before any sweep runs. Both E1 masters (202609221/2) are retired and never reused.
2. **M6 design and held-out audits** on the fresh masters, through the Flight 8 instrument with the production Markov-null cache; qualification joined mechanically as in E1 (`m6_audit_qualification`); **passage required** before any canonical scientific job.
3. **Governance grammar** carries from E1-R unchanged: adverse-but-valid; package completion and production readiness computed separately; an adverse M6 closes the stage, as it did E1-R's — no same-stage repair.
4. **Gemini corpus audit** (commission v3, `c59f235`) runs on the contract draft before the freeze; its cited findings are triaged by L1 and go to Mike; it has no verdict authority.

## 8. Canonical job sequence (after qualification passes)

| # | Job | Object | Condition 3 |
|---|---|---|---|
| 1 | `skeleton_census` | h = 0, homogeneous bases, sweep over m, low and high initializations; T-S1, T-S2 | **first canonical scientific job** — if the instrument misses the exact crossing it is known here |
| 2 | `skeleton_stability` | alternative templates / seed panels; class reproduced? | as E1's reference_stability |
| 3 | `realization_census` | h = h₀, same sweep; T-R1; secondary detection boundary | |
| 4 | `realization_stability`, tolerance program, resource benchmark, tranche, package | as E1-R's grammar | |
| held | heterogeneous-base run (spectral comparator), third-order lattice-vs-ODE comparison | after amendment §10's conditions are discharged | |

Cost scale from E1-R on Mike's machine: dense reference 33 min; stability 4.2 h; audits ~1.3 h each; package replay 13 h. The hazard rule is cheaper per tick than the symmetric chain (no σ, no quadratic term); M3's transfer-matrix route is cheap; expect the same order of magnitude overall.

## 9. Rulings needed from Mike before the contract is drafted

1. **The rule (§2) as the successor substrate rule** — the hazard form, synchronous timing, all terrain through the feedback channel, noise off for the primary flight.
2. **h₀** — the committed floor of the realization (candidate: the hazard that reproduces η_floor = 0.01 per tick).
3. **Homogeneous bases for the primary flight**, with the heterogeneous/spectral run held as a successor job.
4. **The bridge (§3)** as the discrete-to-continuous bridge amendment §10 asks for — or hold it.
5. **M3 route** (§4): (a) exact transfer matrix for θ_T, (b)/(c) for θ_P — or route the choice to L2 first.
6. **W_res as a declaration** with the status of W (PD5), and the multiplier c and gap γ as contract values.
7. **Null initialization**: stationary start (no burn-in) vs all-inactive with burn-in.
8. **Order of packets**: §6 to L2 as the repair-design packet now (L1's recommendation), contract packet after L2's disposition and Gemini's audit.

## 10. Files (design evidence, NONCANONICAL; proposed home `flights/mfa_fidelity/diagnosis/e1r_m6_onset/design/` or beside the Flight 8 contract draft, Mike's call)

| File | What |
|---|---|
| `FLIGHT_8_DESIGN_NOTE_v0_1.md` | this note |
| `replay_full.py` | ideal-M2/M3 replay of the 12,000 committed sweeps storing final label/level sequences |
| `replay_rows.json` | its rows |
| `price.py` | prices candidate 4c criteria against the frozen cap; produced §6.2 |

## 11. What this note is not
Not a contract; not an authorization; not a repair approval; not a result. It proposes a rule, a closure, a null, a repair and a qualification plan for Mike to rule on and L2 to review. E1-R stage 1 remains closed adversely; its ensembles remain burned; no production exists or is implied.

*L1, 2026-10-20.*
