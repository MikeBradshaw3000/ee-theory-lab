# Merge Specification — MFA-Fidelity Flight Instrument
## Draft v0.2 (Mike's item rulings integrated; routed to L2 for adversarial review, with §8.1's bypass as the named review question)

**Status:** DRAFT v0.2. Nothing herein authorizes seeding, implementation, or code change. Mike has ruled open items 1–5 (markers below updated to **[RULED — Mike, 2026-08-19]**); item 6 (§8.1 Gate-A bypass) is the **named L2 review question** for this routing. Remaining **[PROPOSED]** markers are L1 design choices open to L2 challenge. All committed values are cited to Verified Substrate Facts v1.1 (commit `4d9a622`) or to a ruling record.

**Governing framing (L2, pre-committed under Brief 3):** this specification defines **a new experimental instrument with two ancestor witnesses.** It is not an interpolation between Lineage A and Lineage B; it is a new instrument whose relationship to each ancestor is certified by named, independent gates.

**Authority chain:** Purpose and Orientation (canonical) > this specification > implementation. Where implementation and specification diverge, the divergence is surfaced, never absorbed. Phenomenology outranks formalism; any trade of phenomenological capability for formal elegance is flagged and arbitrated.

---

## §1 Architecture ruling and execution model

Per the Brief 3 ruling: **one unified execution path.**

1.1 **RNG regime:** a single explicit NumPy Generator (`np.random.default_rng(seed)`), Lineage A's regime. The legacy-global regime is not carried. All stochastic consumption — initialization, per-tick realization, observable permutation nulls, and (if enabled) the noise stream's master-seed derivation — draws from explicitly managed Generator objects. Lineage B's null machinery is rebuilt onto Generator draws (facts v1.1 S1(c)(5), consolidated observation 5); the rebuild is certified by the B rule-equivalence gate (§8.2), not by preservation.

1.2 **Update-rule framework:** synchronous two-phase advance, one rule framework with two dispatch-labeled rule modes:
- `rule_mode = "symmetric_chain"` — Lineage A's 13-step chain: pre-Q base copy → Λ (F dispatch) → Moore density/8 → drive → p_base = σ(drive) → p_act = p_base + η_floor(1−p_base), clipped → one full-grid draw → simultaneous advance → ds → Ψ_local → telemetry → Q base update, clipped, clip counters (v1.1 S1(b)).
- `rule_mode = "become_survive"` — Lineage B's asymmetric rule: p_become at the logit on inactive cells; survival of active cells at bare p_Λ, invariant to drive and coupling (v1.1 S1(b)).
The two rule modes are different dynamical rules, not parameterizations of one rule (S1(c)(2)); no code path may silently translate between them.

1.3 **State vector:** per-cell v, u, r (float64) + boolean is_active — Lineage A's full state. In `become_survive` mode, bases may be frozen and Λ fixed to realize B-comparable conditions; frozen-bases is a configuration, not a reduced state vector.

1.4 **Naming note (binding):** u is the cost-complement base, u_base ≡ 1−c. The exogenous drive is u_t. These never share a symbol in code, telemetry, or prose. η_floor is A's nucleation floor constant (0.01); η_MFA is the Landau noise term (§6). No η symbol reuse.

## §2 Λ and the F dispatch

2.1 **Committed F-candidates** (string dispatch, per v1.1 S3(a)): `F_baseline` = (v+u+r)/3; `F_LR` = min(v,u,r); `F_2_symmetric` = (v·u·r)·(W_V·v + W_U·u + W_R·r); and per D3 (slot-addition, ruled): **`F_canonical` = v·u·r.** F_canonical and F_2_symmetric are distinct dispatch labels; conflation is the named defect class.

2.2 **[RULED — Mike, 2026-08-19] F_baseline: CARRIED, marked legacy-unused.** No contract may select it without arbitration; silent presence resolved by explicit carry (v1.1 consolidated observation 3 closed).

2.3 **F guards (L2 refinement, accepted):** domain guards on all F forms — inputs clipped-in-[0,1] verified at entry in debug/preflight; zero-collapse behavior of multiplicative forms documented at the dispatch site as architectural (V3), not defect.

2.4 Λ is locally configured per cell. Aggregate Λ is a theorist-level descriptor only (V1); no agent-facing or Q-facing code reads an aggregate Λ. Vocabulary: "structural conduciveness Λ" in all prose; bare "terrain" is house usage; "terrain favorability" is quarantined.

## §3 The drive and coupling channels

3.1 **Common channel:** exogenous drive u_t enters additively and ungated (the E2-frozen implementation). Block-ramp schedule machinery is carried from B (BLOCK_LENGTH, levels {0, u/2, u}) as a configurable schedule object; production schedules are contract-frozen per flight.

3.2 **Local channel:** Moore-neighborhood coupling. In `symmetric_chain` mode: density/8 with quadratic overcrowding (A's β, δ terms). In `become_survive` mode: centered fraction g_q = 2q−1, linear at the logit with κ (B's form). The two normalizations are properties of their rule modes, not selectable across them (S1(c)(7)).

3.3 **Configuration-gated drive** (Claim B's refinement) is a **named refinement outside this specification** — neither implemented nor foreclosed; the E2 frozen scope language governs. The known implementation surface (drive-arithmetic modification + one telemetry column, no PRNG changes — R4, L3-confirmed) is recorded for the successor.

## §4 Q — the slow channel (per the D2 ruling)

4.1 **Committed Q core:** post-telemetry base update, delta_b = Γ_Q · Ψ_local per base, clip [0,1], per-base clip counters (v1.1 S2(a)) — extended per D2 with an activation term:

**Q reads (activation_input, Ψ_local), with activation_input selected by `Q_read ∈ {local, global}`.**

- `Q_read = "local"` (**PRIMARY** — P4's headline verdict attaches here): activation_input = Local_Density (Moore active fraction /8, already computed and persisted; S2(b)).
- `Q_read = "global"` (**COMMITTED COMPARATOR** — the mimicry/control realization): activation_input = rho_global, the pre-update grid mean of is_active, computed per tick and persisted (one new per-tick scalar; S2(b)).

4.2 **Causal timing (L2's construction, adopted):** activation_input is computed **pre-update** at tick t; Q applies **post-update** at tick t; the modified bases first affect dynamics at t+1.

4.3 **[RULED — Mike, 2026-08-19] Extended-Q functional form: the minimal linear form is committed.** **delta_b = (Γ_Ψ · Ψ_local + Γ_ρ · activation_input) per base** — two committed coefficients, uniform across bases, preserving Q's diagonal structure (base independence as architectural product). Regime-dependence (P4's mechanism) lives in the joint behavior of the two terms across regimes and is adjudicated by E4, not embedded in the form. Ψ-gated or switching forms are rejected as embedding P4's answer.

4.4 **Telemetry decomposition (L2, binding):** separated per-row columns for the Ψ-term and ρ-term contributions to each base's delta (Delta_from_Psi, Delta_from_rho — final names at ledger entry), plus Q_read mode recorded per run in the manifest. In global mode, rho_global is persisted per tick (in-row or tick table — **[PROPOSED]** tick-level table, avoiding 2,499 redundant copies per tick).

4.5 Ψ_local remains **mechanism** telemetry; its aggregate is a committed secondary observable (D5 ruling, attachment 3). No code path uses Ψ_local's aggregate as a regime classifier input.

## §5 Initialization

5.1 D6 stands: **i.i.d. initialization** — bases ~ U(0.6, 0.9) per cell, sequential per-cell draws (A's sequence-preserving order). Activity initialization: **[PROPOSED]** both ancestors' schemes carried as configurations — `init_activity ∈ {bernoulli_p, fixed_count}` (A's Bernoulli(0.5); B's exact-count placement rebuilt on Generator permutation) — because E-ladder rungs need both low-ρ seeding and generic starts. Fixed-count placement uses `Generator.permutation`, a committed draw-order element.

5.2 D6's protective scope, narrowed per L2: i.i.d. suppresses spatial signatures of organized base arrangement, **not** configuration-dependent response heterogeneity, which is visible and legitimate.

## §6 Noise architecture (D4, L2's accepted design)

6.1 If a run enables η_MFA: an **independent deterministic stream** derived from the master seed (`Generator(spawn)` or documented-equivalent derivation), never interleaved with the dynamics stream.

6.2 **Zero-amplitude no-draw bypass:** at η_MFA amplitude 0, no draws occur on the noise stream and no code path touches it — preserving the conditional bit-exact A gate (§8.1) exactly.

6.3 Telemetry per L2's set: Noise_Draw column when enabled; amplitude in the run manifest; the drive-decomposition verification family gains the noise term (S4(b)).

## §7 Telemetry and verification philosophy

7.1 The instrument owes **both ancestors' verification styles** (S1(c)(6)): full per-cell per-tick rows (A's philosophy — the 25-column family, extended by the Q decomposition, Q_read/rule_mode manifest fields, and conditional Noise_Draw/rho_global) **and** window/block aggregate summaries with steady/lifted classification (B's philosophy, rebuilt).

7.2 **Row-level recomputation (Tier-1)** remains the verification spine: realization invariant (is_active == (PRNG_draw < p_act)) streamed post-run; drive decomposition recomputation; Q decomposition recomputation from the separated columns; Λ recomputation per dispatch label.

7.3 **[RULED — Mike, 2026-08-19] Hash emission: the Flight 6 marked points are formally SUPERSEDED** by a single end-of-run manifest hash — SHA-256 over the telemetry parquet(s) + config JSON, recorded in the run manifest (v1.1 consolidated observation 2 closed by explicit supersession, not omission).

7.4 **Environment:** venv mandatory (hard fail). **[RULED — Mike, 2026-08-19, procedure accepted]** Python pin and package pins are asserted in the frozen spec after L1 reads `cycle3/requirements.lock.txt` via the commit-pinned clone channel — a standing L1 action blocking §7 freeze (the file has carried "exists, unread" through two records; it does not survive a third). A's 3.14.x hard-fail is the working assumption pending that read.

## §8 Parity section — three independent certification gates

**Rule (L2, binding): the gates are genuinely separate; passing one cannot compensate for failure of another.**

8.1 **Gate A — Lineage A preservation (BIT-EXACT, conditional).** Configuration: `rule_mode=symmetric_chain`, κ-coupling as A's committed terms, u_t = 0, η_MFA disabled (no-draw bypass), Q_read exercising only the committed Ψ_local term (Γ_ρ = 0 with a no-read bypass symmetrical to the noise bypass — **NAMED L2 REVIEW QUESTION, see §12**), A's constants and init. Requirement: identical draw sequence and identical telemetry to `flight2_production.py` at matched seed (PRNG_SEED = 0x7A9B31C), per S6(a). Fallback on structural impossibility: per-tick aggregate parity + distributional match, but any added draw is a gate failure first and a documented supersession second — never a silent fallback.

8.2 **Gate B — Lineage B preservation (RULE-EQUIVALENCE, L2's standard).** The `become_survive` branch reproduces B's p_become and survival values at matched inputs against B's own preflight-verifier pattern (`run_parity_check`, `c3_w2_rule_c_m2.py` L181–240), plus aggregate/distributional parity on ρ trajectories at matched seeds. **Commit `4d9a622` is Lineage B's canonical executable reference** (Brief 3 ruling, attachment 2). Bit-exact B is not attempted (S6(b), impossibility as recast — rule difference + RNG regime difference).

8.3 **Gate R — MFP recovery bridge (PROJECTION-LEVEL, pre-seeded).** Per ratified MFP v1.1 §4: predeclared projection-level recovery targets, frozen before any relevant data are seen. Minimum exposure set (L2's conditions, D2 record): the local quantity Q reads; aggregate ρ(t) against the mean-field curve; population-aggregated Q response; declared departures; distributional/spatial telemetry sufficient to attribute failed recovery to heterogeneity/correlation rather than hide it in the average. Target *values and tolerances* are contract-level commitments (E1's contract is the natural home for the first frozen target set) — **[RULED — Mike, 2026-08-19: deferral to contract level ratified]** — this specification commits the *machinery and the exposure surface*, and the rule that no target may be set or adjusted after relevant data exist. The asymmetry binds: failed recovery is evidence against the stream-level realization; no post-hoc MFP refuge.

## §9 Run configuration surface

9.1 **[RULED — Mike, 2026-08-19] Merged grid and run length:** grid parameterized as in A (`grid_scale`); **50×50 / 3000 ticks committed as the production default** — B's spatial extent with A's temporal depth; 7.5M rows/run under full telemetry (S5(b)). Wall-clock forecast owed at contract time per rung, measured on the new instrument (S5(a): no committed anchor exists).

9.2 Run manifest (JSON, per run): seed, rule_mode, Q_read, F dispatch label, all constants, schedule object, init scheme, noise amplitude, environment pins, manifest hash (§7.3 if adopted). Wrong-values-under-right-names guard: the manifest is written *before* the run from the config object the run actually consumes — one object, no transcription.

## §10 Naming-ledger additions (for L2 review with this spec)

- `Q_read ∈ {local, global}` — Q's activation-input selector; "local primary" is verdict grammar, never a code-level default that could be confused with correctness.
- `rule_mode ∈ {symmetric_chain, become_survive}` — dispatch labels for the two ancestor rules.
- `F_canonical` = v·u·r (≠ F_2_symmetric); `F_baseline` carried-legacy-unused **[if 2.2 adopted]**.
- Observable roles: `Psi_persistence` (PRIMARY), `Psi_state` (committed secondary), `Psi_local_agg` (committed secondary, mechanism-adjacent). Role names travel with the observables in all documents; role drift is a ledger violation.
- `rho_global` — the global activation mean (Q comparator input); never called ρ_c (quarantined symbol).
- `Delta_from_Psi`, `Delta_from_rho` — Q decomposition columns (final form at ledger entry).

## §11 What this specification does not do

No contract content: no thresholds, gates, tolerances, regime definitions, or verdict rules for E1–E5 (contract-level, each under the pre-seed evaluability audit, each preceded by its narrative telling). No exploratory-shelf content. No manuscript content. No field-program content. The E2 frozen scope language, the jeopardy split, and all ruling attachments (stain discriminator, E4 evaluability forecast, persistence guard forecast against the frozen TCOP audit) bind at contract time and are recorded here only as forward obligations.

## §12 Open items consolidated

| # | Item | Status |
|---|---|---|
| 1 | F_baseline (§2.2) | RULED: carried, legacy-unused |
| 2 | Extended-Q form (§4.3) | RULED: minimal linear form committed |
| 3 | Hash points (§7.3) | RULED: superseded by manifest hash |
| 4 | Python pin / lock-file (§7.4) | Procedure ruled; L1 lock-file read blocks §7 freeze |
| 5 | Grid/run length (§9.1) | RULED: 50×50 / 3000 default |
| 6 | **Gate-A Γ_ρ no-read bypass (§8.1)** | **NAMED L2 REVIEW QUESTION — this routing** |

**The §12.6 question, stated for L2:** Gate A's bit-exact certification requires that the extended Q (§4.3's committed linear form) add no draws and no floating-point divergence in the channels-zeroed limit. The proposed mechanism mirrors the D4 noise bypass: at Γ_ρ = 0, no activation-input read occurs and no ρ-term arithmetic executes — the code path is absent, not merely zero-valued — so the A-limit computation is bit-identical to the ancestor's, not merely numerically equal. Review requested: (i) is the absent-not-zero construction sufficient for the bit-exact claim, or does the extended-Q refactoring itself (even with the Ψ-term only) risk sequence or FP divergence that the bypass does not address (sufficiency-tested-not-asserted applies — the original S6(a) criterion, not the refactoring's claim about itself); (ii) does the bypass require its own preflight verification element in Gate A's harness, and if so, its shape; (iii) any defect in the symmetry claim between this bypass and the D4 noise bypass. Adversarial review of the full specification is welcome beyond the named question per standing practice.

*End of draft v0.2. Sequence: L2 adversarial review (named question §12.6 + general) → v0.3 integration → freeze at Mike's word.*
