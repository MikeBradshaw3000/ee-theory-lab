# Verified Substrate Facts S1–S7 — MFA-Fidelity Flight Design (Consolidated Record v1.1)

**Provenance:** Extracted by L1 from the repository at commit `4d9a622`; verified by L3 (fresh session) against complete provided sources (`flight2_production.py`, 499 lines; `c3_w2_rule_c_m2.py`, 397 lines; `c3_w2_tcop.py`, 700 lines); disputes adjudicated by L1 against the commit-pinned clone with mechanical recounts; reviewed by L2 with one material scope correction, accepted and folded in below, marked **[RECAST per L2 review]**. Two L3 disputes were upheld and are folded in, marked **[CORRECTED per L3 verification]**. All other cited claims stand CONFIRMED by quotation. Items resting on materials outside the three verified sources (the Flight 6 specification PDF, `requirements.lock.txt`, ops logs) carry their original marks and remain unverified by L3.

**Status:** This document supersedes the initial facts extraction and is the citable substrate-facts record for merge-specification and contract drafting. It is facts only; the open arbitrations (D2 read-locality; D5 observable) remain with Mike, pending L2's adversarial inputs. Nothing here authorizes seeding, implementation, or code change.

**Audience:** L2 (design review inputs, notably S6 and S4 bearing on rulings in flight) and L3 (confirmation that the verification is integrated as adjudicated).

---

## S1 — Lineage inventory and merge surface

**(a) Executable cores.**
- **Lineage A (full cascade):** `flights/cycle2_round1/02_flight_1_v1_1_parity/flight2_production.py` (499 lines). Self-declares (header): *"NumPy substrate implementation of locked Mesa-equivalent dynamics"* — Mesa 3.x API regressions and performance blocked physical execution; the pure NumPy implementation is established as the canonical baseline substrate. Companion: `flight2_analysis.py`. Governing spec: `flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf` (outside verified sources).
- **Lineage B (probe apparatus):** `cycle3/wave_two/c3_w2_rule_c_m2.py` (397 lines) — observables, steady-state machinery, preflight parity harness; `cycle3/wave_two/c3_w2_tcop.py` (700 lines) — CM-1/CM-0 update core and frozen drive schedule.

**(b) Side-by-side committed values.** (All verified by quotation except where marked.)

| Property | Lineage A | Lineage B |
|---|---|---|
| Grid | Parameterized `grid_scale`; run names `probe1_20x20` etc.; 40×40 memory handling per header | `GRID_SIZE = 50`, `N_CELLS = 2500` (L53–54); toroidal Moore radius 1 (L5) |
| Run length | `TICKS_PRODUCTION = 3000` (L45) | `TICKS_PER_RUN = 200` (L55) |
| State per cell | v, u, r float64 + boolean `is_active` (L117–121) | Binary active/inactive only; no bases |
| Initialization | Per-cell sequential PRNG draws, bases ~ U(0.6, 0.9), activity Bernoulli(0.5); "Section 5.2: sequence preservation via cell-by-cell PRNG draws" (L123–129) | Fixed-ρ 0.10: exactly 250 active cells (header L14), placement via `np.random.permutation` |
| Update semantics | Synchronous two-phase, 13 labeled steps: pre-Q base copy → Λ (F dispatch) → Moore density/8 → drive (αΛ + βd − δd² − γ) → p_base = σ(drive) → p_act = p_base + η(1−p_base), clipped → one full-grid draw → simultaneous advance → ds → Ψ_local = ds·MooreSum(ds) → telemetry row (pre-Q bases) → base update with clip [0,1] and clip counters (L146–252) | Become/survive: `p_become = sigmoid(LOGIT_L + u_t + κ·g_q)` on inactive cells only; survival of active cells at bare p_Λ, invariant to u_t and κ, preflight-enforced (`c3_w2_tcop.py` L263–272, L342–352) |
| Constants | PRNG_SEED = 0x7A9B31C; α=4.0, β=3.0, δ=4.0, γ_offset=4.0, η=0.01, γ_Q=0.001; W_V=W_U=0.33, W_R=0.34; init range 0.6–0.9 (L44–56); CHUNK_TICKS=500 | κ ladders as (c_j, κ) tables, 0.20/0.40 anchors, sign-mirrored (L76–97); block ramp BLOCK_LENGTH=25, levels {0, u/2, u} (`c3_w2_tcop.py` L47–48, L282) |
| RNG regime | **Single explicit Generator:** `self.prng = np.random.default_rng(PRNG_SEED)` (L115); all draws — initialization and per-tick — from this one stream; no other stochastic source | **Legacy global RNG throughout.** **[CORRECTED per L3 verification]** Production runs seed the global stream **once per run** (`c3_w2_rule_c_m2.py` L312; `c3_w2_tcop.py` L488); observable nulls then consume that stream without re-seeding; the repeated `PARITY_SEED` re-seeds (L189–228; tcop L182–216) occur **in the preflight parity harnesses only**, not during production |
| Telemetry | **[CORRECTED per L3 verification]** Per-cell per-tick parquet rows, **25 columns**, mechanically recounted from the committed row dictionary: Tick, Agent_X, Agent_Y, b_i_v, b_i_u, b_i_r, limiting_base_argmin, Lambda_multiplicative, Lambda_additive, Lambda_total, Local_Density, Drive_Raw, Term_Density_Pos, Term_Overcrowding, Term_Offset, p_base, p_act, PRNG_draw, is_active, Psi_local, gamma_coef, Delta_v, Delta_u, Delta_r, Term_Lambda; streamed in CHUNK_TICKS=500 chunks via pyarrow | Window/block CSV summaries (relative drift, ρ-CV, range-over-mean, mean ρ, steady/lifted flags; thresholds at L60–67, evaluator L165–180) + Moran's I state and persistence observables with permutation nulls (L103–163); grid histories per apparatus convention |
| Preflight | Venv mandatory (hard fail); Python pinned 3.14.x (hard fail); numpy/pandas/pyarrow versions printed (L66–86) | Reimplementation-vs-apparatus parity vs. `c3_ctl_001_battery`/`c3_ss_001_battery` at PARITY_SEED=7; hard fail on divergence (L181–240) |
| Post-run checks | Realization invariant `is_active == (PRNG_draw < p_act)` streamed over full parquet (L273–300) | Steady-state/lifted window classification (L165–180) |

**(c) Incompatibilities a merged environment must arbitrate** (verified both-sides against sources; item 4's grid values partly rest on run configuration outside the update cores):
1. **RNG regime.** A: single `default_rng` Generator, sequence-preserving. B: legacy global `np.random`, seeded once per production run, consumed by dynamics and observable nulls alike. **[RECAST per L2 review]** The lineage-native RNG regimes are incompatible **within a single shared execution path**. A merged contract must either select and port to one regime for the experimental mode, or preserve explicit lineage-native compatibility modes; the source record compels the incompatibility, not the resolution.
2. **Update rule shape.** A: one symmetric probability chain governing activation and persistence. B: asymmetric become/survive with survival invariant to coupling and drive. Different dynamical rules, not parameterizations of one rule.
3. **State vector.** A: bases + activity. B: activity only, Λ fixed. B's channels (u_t, κ) entering A's drive chain — or A's bases entering B's logit — is a committed decision, not a default.
4. **Run length and grid.** 3000 ticks / 20×20–40×40 vs. 200 ticks / 50×50. No committed merged values exist.
5. **Initialization.** Bernoulli(0.5) random density vs. fixed-count ρ = 0.10 seeding. Different ancestors for parity purposes.
6. **Telemetry philosophy.** A: full per-cell rows for Tier-1 row-level recomputation. B: aggregate windows/blocks plus grid snapshots. A merged environment owing both verification styles must emit both.
7. **Coupling normalization.** A: density/8 in a drive with quadratic overcrowding. B: centered neighbor fraction g_q = 2q−1, linear at the logit, no overcrowding term. Same neighborhood, different functional roles.

## S2 — Q extension surfaces (D2)

**(a) Committed Q as implemented** (L200–205, L235–252): after Ψ_local, `delta_v = delta_u = delta_r = GAMMA_Q · psi_local`; bases updated post-telemetry, clipped to [0,1], per-base clip counters. Input: **local Ψ_local only**; no activation input exists.
**(b) Read-variant surfaces.** *Local activation read:* `Local_Density` (Moore active fraction /8) is computed every tick and persisted — a local ρ-input to Q requires no new computation or storage, only entry into the Q expression. *Global aggregate read:* mean of `is_active` is a one-line per-tick reduction, negligible compute, **not currently computed or persisted** — one new per-tick scalar plus a telemetry surface required.
**(c) Tier-1 recomputation columns per variant.** Local: existing columns suffice for the activation term; new columns needed only for the extended Q's coefficient(s) and separated Delta components. Global: a per-tick `rho_global` value must be persisted (in-row or tick-level table) for row-level recomputation, plus the same coefficient/Delta columns. Both await the extended-Q functional form's commitment before columns can be named.

## S3 — F_canonical addition (D3)

**(a)** F-candidates via string dispatch (L163–171): `F_baseline` = (v+u+r)/3; `F_LR` = min(v,u,r); `F_2_symmetric` = (v·u·r)·(W_V·v + W_U·u + W_R·r). **A third committed selectable form (`F_baseline`) exists beyond the two carried in the design record.** `Lambda_multiplicative = v·u·r` is computed every tick and persisted (L160, column list above) but is **not selectable** as the governing form.
**(b) Verdict: SLOT-ADDITION.** A fourth dispatch branch returning the already-computed product is a strict candidate-slot addition. Exact expression in substrate variables: **Λ = v · u · r** (u ≡ 1−c per the cost-complement convention). Tier-1 family recomputes from existing columns.

## S4 — Stochastic content and the noise question (D4)

**(a) Randomness entry points, Lineage A:** (i) base initialization, three sequential draws per cell (L123–127); (ii) activity initialization, one per cell (L128); (iii) one full-grid uniform draw per tick for realization (L191). All from the single Generator. **No other stochastic term exists; the drive is deterministic given state.** Lineage B: per-run seed; initialization permutation; per-tick `rand_grid`; permutation draws inside observable nulls — all legacy-global from the one per-run seed (preflight harness re-seeds excepted, per the S1 correction).
**(b) Additive drive-noise surfaces.** An explicit η_MFA(t) term in the drive requires additional PRNG draws (per cell per tick, or per tick, per the committed form) — **a draw-order change that breaks bit-exact ancestor parity for Lineage A at matched seed**; a `Noise_Draw` telemetry column for Tier-1 drive recomputation; one added term in the drive-decomposition verification family. The realization-invariant check is untouched. The existing Bernoulli realization against p_act is the only fluctuation channel in the committed dynamics.

## S5 — Compute envelope

**(a)** Stage 2 rung wall-clock/config facts: **NOT IN SEARCHED RECORD** at `cycle3/calibration/*.md|json`. Ops logs elsewhere may hold them; not extracted. The ~7-day final-rung figure is **CONVERSATIONAL ONLY** and is not a fact of record. (L3: mark usage confirmed; no fact asserted.)
**(b)** Scaling arithmetic lacks a committed wall-clock anchor: **INPUT NOT IN RECORD.** Row-volume arithmetic the record does support: Lineage A telemetry at 20×20 × 3000 ticks = 1.2M rows/run; 40×40 = 4.8M rows/run; a merged environment at 50×50 × 3000 ticks under A's telemetry philosophy = 7.5M rows/run, × (sweep × seeds) per the eventual committed matrix.

## S6 — Ancestor-reproduction (parity) surfaces

**(a) Channels-zeroed limit → Lineage A target.** Bit-exact reproduction **POSSIBLE, CONDITIONAL**: the merged implementation must preserve A's exact draw order (sequential cell-by-cell init, then one grid draw per tick) and add **no** draws when κ = 0, u = 0, and any noise term is disabled. Any structurally added draw breaks the sequence; fallback is per-tick aggregate parity (ρ series, Ψ_local sums) plus distributional match at matched seed.
**(b) Bases-frozen, Λ-fixed limit → Lineage B target.** **IMPOSSIBLE BIT-EXACT** as committed: different update rule (asymmetric become/survive at the logit vs. A's symmetric chain) and legacy-global RNG regime with no draw-order alignment to preserve. **[CORRECTED per L3 verification]** The impossibility rests on the regime difference and the rule difference — not on mid-run re-seeding, which occurs only in preflight harnesses; production B seeds once per run. Strongest achievable: rule-level equivalence (merged become/survive branch reproduces B's `p_become`/survival values against B's own preflight verifier pattern in `run_parity_check` at matched inputs) plus aggregate/distributional parity on ρ trajectories at matched seeds.
**(c) [RECAST per L2 review]** Conditional consequence: **if** the merged environment requires one unified update path and one RNG regime, it carries one conditional bit-exact A gate and one B rule-equivalence gate. **If** explicit lineage-native compatibility modes are permitted (A-native and B-native modes preserving each ancestor's rule, RNG, initialization, and draw order exactly, alongside an experimental merged mode), a second bit-exact B gate remains an architectural option not ruled out by the source record. The prior statement “cannot carry two bit-exact gates” was a design conclusion, not a source-compelled fact, and is withdrawn as fact. The unified-path-vs-compatibility-modes choice is an architectural arbitration (Mike's), to be made in the merge specification.

## S7 — Environment and stack

Verified from sources: venv mandatory, hard fail (L69–73); **Python pinned 3.14.x**, hard fail (L74–78); numpy/pandas/pyarrow imported, versions printed at preflight (L81); pure-NumPy substrate declared canonical under the spec's equivalence clause, Mesa physical execution recorded as blocked (header L38–41); streaming parquet, chunked (L62, L254–268); psutil optional (L90–99). Version *pins*: **NOT IN SEARCHED RECORD** in the sources (printed, not asserted); `cycle3/requirements.lock.txt` exists, unread this pass. **Standing discrepancy note:** the design record has carried "Mesa 3.x two-phase" as the implementation; the committed canonical substrate is pure NumPy under the equivalence clause. A Mesa-vs-NumPy identical-telemetry verification artifact was **UNOBSERVED IN FILE** and not located.

## Consolidated substrate observations (facts-adjacent; separated from the record)

1. `Local_Density` existing per-row makes the local-read Q variant mechanically near-zero-cost; the global variant costs one persisted scalar per tick. Cost does not decide the D2 arbitration; recorded for completeness.
2. The absence of hash-emission code in the canonical Lineage A implementation, against the specification's marked hash-emission points, is a spec-vs-implementation gap requiring an explicit decision in the merged specification: implement the marked hashes or supersede them.
3. The undocumented third F-form (`F_baseline`) must be either carried into the merged candidate list or formally retired; silent presence is the named defect class.
4. Per S6(c), the parity section of the merged specification is writable now: one bit-exact gate (target: Lineage A at matched seed, zeroed channels), one rule-equivalence gate (target: B's preflight-verifier pattern), named targets, no open dependencies.
5. B's observable nulls consume the global stream; in a merged single-Generator environment the null machinery must be rebuilt onto Generator draws regardless of which update rule wins — simplified (per the S1 correction) by the fact that production B is single-seed, so the port is one stream, not an untangling.

---

**Record note for all layers.** The L2 scope correction (S1(c)(1) and S6(c) recast conditionally; “two bit-exact gates impossible” withdrawn as fact) and the two upheld L3 disputes (telemetry count 25, not 22 as first extracted; B's re-seeding confined to preflight harnesses, production single-seed per run) were adjudicated by mechanical recount and grep against the pinned clone; the corrections strengthen rather than weaken the downstream conclusions they touch. This is the verification loop functioning as designed: extraction by one lineage, hostile checking by a second, scope review by a third, adjudication against source, consolidation into a single citable record. Merge-specification and contract drafting cite this document; v1.0 and the initial extraction are superseded and should not be cited.

*End of consolidated record.*
