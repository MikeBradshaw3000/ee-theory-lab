# Merge Specification — MFA-Fidelity Flight Instrument
## v0.4 — FROZEN (Mike, 2026-08-21) — the governing instrument specification

**Status: FROZEN by Mike's word, 2026-08-21, under L2's FREEZE MAY PROCEED (final changed-text verification; no blocker standing). This document governs the substrate implementation. Frozen digest: c48f36828a53fd58ae96f7a6fa138764a9396dbefb8f1936d34978a3af17156f (19,609 bytes, pre-freeze-stamp). Amendment after freeze is by Mike's explicit act only, producing a versioned successor — never in-place edit.** Seeding remains contract-gated: this freeze authorizes implementation of the instrument, not execution of any experiment. v0.2's ruled items stand unchanged; the deltas from v0.2 are L2's nine required refinements, each marked **[v0.3/L2-n]**; the deltas from v0.3 are the two wording corrections from L2's source-level integration verification (eight INTEGRATED AS REQUIRED at first pass; §5.1 and §6.2 blockers corrected here, marked **[v0.4/blocker-n]**). Freeze is Mike's act, pending L2's changed-text verification of the two corrected passages.

**Governing framing (L2, pre-committed):** this specification defines **a new experimental instrument with two ancestor witnesses** — not an interpolation; a new instrument whose relationship to each ancestor is certified by named, independent gates.

**Authority chain:** Purpose and Orientation (canonical) > this specification > implementation. Divergence is surfaced, never absorbed. Phenomenology outranks formalism.

---

## §1 Architecture and execution model

Per the Brief 3 ruling: **one unified execution path.**

1.1 **RNG regime:** a single explicit NumPy Generator regime (`np.random.default_rng`), Lineage A's. The legacy-global regime is not carried. All stochastic consumption — initialization, per-tick realization, observable permutation nulls, and (if enabled) the noise stream — draws from explicitly managed Generator objects. B's null machinery is rebuilt onto Generator draws (facts v1.1 S1(c)(5)); the rebuild is certified by Gate B, not by preservation.

1.2 **Execution skeleton and rule-mode dispatch [v0.3/L2-4].** The unified framework is a synchronous two-phase advance with a **common execution skeleton** and a **dispatched probability construction**:

*Common skeleton (both rule modes):* pre-Q base copy → Λ (F dispatch) → Moore-neighborhood read → **[PROBABILITY CONSTRUCTION — dispatched]** → one full-grid uniform draw → simultaneous advance → ds → Ψ_local → telemetry emission → Q base update, clip, clip counters.

*Dispatch replaces the probability construction wholesale:*
- `rule_mode = "symmetric_chain"`: A's construction — drive = αΛ + β·(density/8) − δ·(density/8)² − γ_offset; p_base = σ(drive); p_act = p_base + η_floor(1−p_base), clipped. One probability governs activation and persistence symmetrically.
- `rule_mode = "become_survive"`: B's construction computed **directly** — p_become = σ(LOGIT_L + u_t + κ·g_q) on inactive cells, with g_q = 2q−1; survival of active cells at bare p_Λ, invariant to u_t and κ. **B's probabilities are NOT layered onto A's p_base→p_act chain**; the dispatch point is upstream of that chain, and in become_survive mode A's chain does not execute. This is the rule-equivalent implementation Gate B certifies; the alternative construction (become/survive layered on A's chain) is named here as the wrong implementation so it cannot be inferred innocently.

The two rule modes are different dynamical rules (S1(c)(2)); no code path translates between them.

1.3 **State vector:** per-cell v, u, r (float64) + boolean is_active. Frozen-bases with fixed Λ is a configuration realizing B-comparable conditions, not a reduced state vector.

1.4 **Naming (binding):** u_base ≡ 1−c; exogenous drive is u_t; η_floor is A's nucleation floor (0.01); η_MFA is the Landau noise term. No symbol reuse.

## §2 Λ and the F dispatch

2.1 **Committed F-candidates:** `F_baseline` = (v+u+r)/3 **[RULED: carried, legacy-unused; no contract selects it without arbitration]**; `F_LR` = min(v,u,r); `F_2_symmetric` = (v·u·r)·(W_V·v + W_U·u + W_R·r); `F_canonical` = v·u·r (D3 slot-addition). F_canonical ≠ F_2_symmetric by dispatch label.

2.2 **F guards:** domain guards (inputs in [0,1]) verified at entry in preflight/debug; multiplicative zero-collapse documented at the dispatch site as architectural (V3).

2.3 Λ is locally configured per cell; aggregate Λ is theorist-level only (V1). Prose: "structural conduciveness Λ."

## §3 Drive and coupling channels

3.1 **Common channel:** u_t additive and ungated (the E2-frozen implementation). Block-ramp schedule machinery carried as a configurable schedule object; production schedules contract-frozen.

3.2 **Local channel:** Moore neighborhood. symmetric_chain: density/8 with quadratic overcrowding. become_survive: centered g_q, linear at the logit. Normalizations are properties of their rule modes, not selectable across them (S1(c)(7)).

3.3 **Configuration-gated drive:** named refinement outside this specification; E2 frozen scope language governs; implementation surface recorded for the successor (R4).

## §4 Q — the slow channel

4.1 **Committed extended-Q form [RULED]:** post-telemetry, per base: **delta_b = Γ_Ψ · Ψ_local + Γ_ρ · activation_input**, clip [0,1], per-base clip counters. activation_input by `Q_read ∈ {local, global}`: local (PRIMARY) = Local_Density; global (COMMITTED COMPARATOR) = rho_global, the pre-update grid mean.

4.2 **Causal timing:** activation_input computed pre-update at t; Q applies post-update at t; modified bases first act at t+1.

4.3 **Diagonal structure — exact meaning [v0.3/L2-3].** "Q's diagonal structure" means precisely: **no base value enters another base's update equation as an input.** It does **not** mean statistically independent base trajectories: the common drivers (Ψ_local, activation_input) applied to all three bases can and will generate correlation among their changes. That correlation is common-cause correlation, not coupling — the Base-Space Registration v1.1 distinction applies to Q's own outputs: correlated base movement under a shared driver is permitted and predicted; a cross-base input term would be coupling and is excluded. Claim language anywhere downstream must not read correlated base trajectories as a diagonality violation.

4.4 **Coordinate orientation [v0.3/L2-3].** Q operates on substrate coordinates: **u_base = 1−c.** All Γ signs, telemetry columns, and prose interpretations are stated in the (v, u, r) system, in which ecosystem-improving Q moves all three bases **upward**. The corresponding MFA statement in (v, c, r) moves c downward; the translation is mechanical (δu = −δc) and is stated here once so no contract reasons in c while code updates u. Any document mixing the systems must carry the conversion explicitly.

4.5 **Telemetry decomposition:** separated columns Delta_from_Psi, Delta_from_rho per base-update; Q_read in the run configuration (§9). rho_global persistence per §7.2.

4.6 Ψ_local is mechanism telemetry; its aggregate is a committed secondary observable; no regime classifier consumes it (D5).

## §5 Initialization

5.1 **D6 stands:** i.i.d. initialization. **Algorithmic lineage vs. parameter choice [v0.3/L2-5]:** the configuration surface distinguishes *which scheme* from *which algorithm implements it*. `init_activity ∈ {bernoulli_p, fixed_count}`:
- `bernoulli_p` in its **Gate-A configuration** is A's exact algorithm, frozen: sequential per-cell iteration; per cell, three base draws (v, u, r ~ U(0.6, 0.9)) then one activity draw (Bernoulli 0.5), in that order, cell-by-cell (v1.1 S1(b) "sequence preservation via cell-by-cell PRNG draws"); Generator call shapes identical to the ancestor's (scalar-per-draw, not vectorized); dtype float64 throughout with no intermediate coercion. Gate A freezes this entire description, not the scheme label.
- `fixed_count` is **a new merged-instrument implementation — not bit-exact preservation of B's legacy initialization procedure, RNG realization, or seedwise stochastic history** — using `Generator.permutation` with declared draw order. Its dynamical behavior is assessed under Gate B2 (§8.2), which remains the test of distributional behavioral equivalence with ancestor B; bit-exactness is never claimed for it. **[v0.4/blocker-1]**

5.2 D6's protective scope, narrowed per L2: suppresses spatial signatures of organized base arrangement, not configuration-dependent response heterogeneity.

## §6 Noise architecture (D4)

6.1 η_MFA, when enabled: independent deterministic stream derived from the master seed (spawn or documented-equivalent), never interleaved with the dynamics stream.

6.2 **Zero-amplitude no-draw bypass:** at amplitude 0, no noise-stream construction, no draws, and no noise arithmetic occur — **removing η_MFA as a source of Gate-A divergence. Gate A's complete behavioral comparison alone certifies bit-exact preservation** (§8.1's necessary-not-sufficient discipline applies to this bypass identically). **[v0.4/blocker-2]**

6.3 Telemetry: Noise_Draw column when enabled; amplitude in run configuration; drive-decomposition family gains the noise term.

## §7 Telemetry and verification

7.1 Both ancestors' verification styles are owed: full per-cell per-tick rows (A's 25-column family + Delta_from_Psi/Delta_from_rho + conditional columns per 7.2) and window/block aggregate summaries with steady/lifted classification (B's, rebuilt).

7.2 **Column conditions, stated separately [v0.3/L2-9]:** `Noise_Draw` is conditional on η_MFA enabled. **`rho_global` is NOT merely Q-conditional: it is required whenever Q_read = global AND whenever Gate R (§8.3) is exercised — including local-primary runs — because aggregate ρ(t) is a recovery quantity and local→aggregate recovery is the question.** Persistence: tick-level table (avoiding per-row duplication). A local-primary MFP run without rho_global telemetry is a specification violation.

7.3 **Hash construction, canonical [v0.3/L2-6] [RULED: supersedes Flight 6 marked points].** Two files, epistemically separated **[v0.3/L2-6, reconciling §9's manifest timing]:**
- **`run_config.json`** — written and frozen **before execution** from the config object the run actually consumes (one object, no transcription); serialized canonically (UTF-8, sorted keys, no insignificant whitespace, LF); its SHA-256 computed at freeze and recorded in the run record. The implementation may not rewrite it after execution.
- **`run_record.json`** — emitted **after execution**: references the config hash; records the telemetry digest, environment report, completion metadata.
- **Telemetry digest, canonical bytes:** SHA-256 over the concatenation of the telemetry parquet files' raw bytes in ascending lexicographic filename order, each preceded by its filename as a UTF-8 line (`<name>\n`); filenames therefore enter the digest; the run record itself is outside every digest it reports. Two semantically identical runs hash identically or the construction is defective.

7.4 **Environment [v0.3/lockfile-read, 2026-08-21]:** venv mandatory (hard fail). **The lock-file read is complete** (L1, commit-pinned clone at `4d9a622`): `cycle3/requirements.lock.txt` pins, asserted for the merged instrument — **numpy==2.4.4, pandas==3.0.3, pyarrow==24.0.0, scipy==1.17.1, psutil==7.2.2, pytest==9.0.3** (full twenty-package list per the lock file, which is the citable source; Mesa==3.5.1 is present in the environment and unused by the canonical substrate per the equivalence clause). Two recorded findings: the lock file carries a UTF-8 BOM (relevant to any programmatic parse); it contains no Python-interpreter pin, so **Python 3.14.x rests on the executable's preflight hard-fail (v1.1 S7) as its sole committed source** and is asserted here on that basis. §7 is no longer read-blocked.

## §8 Parity — three independent certification gates

**Rule (L2, binding): the gates are genuinely separate; passing one cannot compensate for failure of another.**

### 8.1 Gate A — Lineage A preservation (BIT-EXACT, conditional) **[v0.3/L2-1, L2-2]**

Configuration: rule_mode=symmetric_chain, A's constants and committed coupling terms, u_t = 0, η_MFA disabled (no-draw bypass), Γ_ρ = 0 with the no-read bypass, A's exact initialization algorithm (§5.1), PRNG_SEED = 0x7A9B31C.

**The Γ_ρ bypass, correctly claimed:** at Γ_ρ = 0, no activation-input read occurs and no ρ-term arithmetic executes — the code path is absent, not zero-valued. **This bypass is NECESSARY but NOT SUFFICIENT** (L2 verdict, adopted): it removes the activation extension as a source of Gate-A divergence; **bit-exact preservation remains an empirical property of the complete channels-zeroed merged execution path and is established only by Gate A itself.** Refactoring can break bit identity without changing PRNG consumption, on four independent surfaces: (1) PRNG sequence (init + realization draws identical); (2) floating-point operation ordering in the surviving Ψ-Q calculation; (3) state/update ordering (Q and clipping at exactly the ancestor locations); (4) instrumentation side effects (added telemetry must not alter state, evaluation order, dtype, or stochastic consumption).

**Two-level harness (L2's design, adopted):**
- **Structural preflight (diagnostic, not a substitute):** with Γ_ρ = 0 and η_MFA = 0, verify before the full comparison that: the activation-read function is never invoked; no rho_global computation is requested for Q; **no additional Q-side local-density read or computation is introduced beyond A's own ordinary drive-side density read** (A already reads local density for its drive — the preflight requirement is no *added* Q-side access, not "never read"); Delta_from_rho is structurally absent from Gate-A comparison output (or emitted as telemetry-only exact zero outside the state-update expression); no noise-stream construction or draw occurs; dynamics-stream draw count and order equal the ancestor's expected consumption.
- **Behavioral certification (the actual gate):** complete matched-seed ancestor comparison against `flight2_production.py`; bit-exact state and telemetry equality over the specified Gate-A horizon. The preflight's purpose is diagnostic separation: on a Gate-A failure, it distinguishes bypass violation from other refactoring divergence.

**Bypass-principle wording (L2's, replacing "symmetrical"):** the Γ_ρ bypass applies **the same zero-channel structural-bypass principle used for η_MFA, applied here to a deterministic arithmetic/read extension.** The two bypasses guard different failure modes (η_MFA: PRNG isolation and noise arithmetic; Γ_ρ: arithmetic and data-access identity, no PRNG content) and are not symmetrical.

Fallback on structural impossibility: per-tick aggregate parity + distributional match — but any added draw is a gate failure first and a documented supersession second, never a silent fallback.

### 8.2 Gate B — Lineage B preservation (rule-equivalence, two layers) **[v0.3/L2-7]**

**B1 — deterministic rule equivalence:** at matched input states, the become_survive branch reproduces B's p_become and p_survive values exactly, verified against B's own preflight-verifier pattern (`run_parity_check`, `c3_w2_rule_c_m2.py` L181–240). Deterministic, seedless, per-state.

**B2 — dynamical distributional equivalence:** over a **declared seed ensemble**, predeclared aggregate/distributional agreement of ρ behavior between the merged instrument (become_survive configuration) and ancestor B. **No seedwise trajectory pairing is claimed or implied:** B's RNG regime has been deliberately rebuilt, so matched seed values do not create matched stochastic histories; "matched seeds" language is retired from this gate. Ensemble size and agreement statistics are predeclared at the Gate-B harness level.

**Commit `4d9a622` is Lineage B's canonical executable reference** (Brief 3 ruling). Bit-exact B is not attempted (S6(b) as recast).

### 8.3 Gate R — MFP recovery bridge (projection-level, two stages) **[v0.3/L2-8]**

**R0 — bridge implementation correctness (precedes all scientific evaluation):** the implementation proves it correctly computes the projection quantities — the local quantity Q reads; aggregate ρ(t); the population-aggregated Q response; the declared departure statistics — against constructed cases with known answers. R0 is instrument validation, adjudicated before any recovery question is asked.

**R1 — scientific recovery:** against predeclared projection-level targets and tolerances, frozen at contract level (E1 the natural home) before any relevant data exist, per ratified MFP v1.1 §4. Exposure surface per L2's conditions (D2 record): the read quantity, aggregate ρ(t) against the mean-field curve, aggregated Q response, declared departures, and distributional/spatial telemetry sufficient to attribute failed recovery to heterogeneity/correlation rather than hide it in the average.

**The R0/R1 separation is load-bearing:** without it, a failed recovery is ambiguous between "the stream-level realization failed" and "the bridge was implemented incorrectly" — an ambiguity MFP's status cannot tolerate. The asymmetry binds at R1 only after R0 has passed: failed recovery is then evidence against the stream-level realization, no post-hoc MFP refuge.

## §9 Run configuration surface

9.1 **[RULED]** Grid parameterized (`grid_scale`); production default **50×50 / 3000 ticks**; 7.5M rows/run under full telemetry. Wall-clock forecast owed at contract time per rung, measured on the new instrument.

9.2 **Configuration/record separation [v0.3/L2-6]:** `run_config.json` per §7.3 — seed, rule_mode, Q_read, F dispatch label, all constants, schedule object, init scheme + algorithmic-lineage flag (§5.1), noise amplitude, environment pins — frozen pre-run from the consumed object. `run_record.json` post-run per §7.3. The wrong-values-under-right-names guard is the one-object rule plus the immutable-config boundary.

## §10 Naming-ledger additions

- `Q_read ∈ {local, global}` — "local primary" is verdict grammar, never a correctness default.
- `rule_mode ∈ {symmetric_chain, become_survive}` — dispatch replaces the probability construction wholesale (§1.2).
- `F_canonical` = v·u·r (≠ F_2_symmetric); `F_baseline` carried, legacy-unused.
- Observable roles: `Psi_persistence` (PRIMARY), `Psi_state` (committed secondary), `Psi_local_agg` (committed secondary, mechanism-adjacent). Role drift is a ledger violation.
- `rho_global` — required per §7.2's dual condition; never ρ_c.
- `Delta_from_Psi`, `Delta_from_rho`; `run_config` / `run_record` (§7.3); Gate layers `B1`, `B2`, `R0`, `R1`.

## §11 What this specification does not do

No contract content (thresholds, gates, tolerances, regime definitions, verdict rules — each contract's business, under the pre-seed audit, preceded by its narrative telling). No exploratory-shelf content, no manuscript content, no field-program content. Forward obligations recorded: E2 frozen scope language; jeopardy split; stain discriminator; E4 evaluability forecast; persistence guard forecast against the frozen TCOP audit; R1 target freeze at E1. L2's non-challenge is recorded: the deferral structure is correct and pulling scoring into this spec would weaken outcome hygiene.

## §12 Disposition

All nine L2 refinements verified at source: L2-1 through L2-4 and L2-6 through L2-9 INTEGRATED AS REQUIRED; L2-5's §5.1 defect and the §6.2 cross-section defect corrected in this version per L2's required substance. §7.4 lock-file addition: NONE FOUND within L2's scoped review. Verification history complete: source-level pass (eight INTEGRATED AS REQUIRED; two defects) → v0.4 corrections (both CORRECTED AS REQUIRED) → header provenance corrected → FREEZE MAY PROCEED → FROZEN. Next: frozen document to L2 for record; E1 narrative telling; substrate implementation per §§1–9.

*End of draft v0.3.*
