# Note to L2 — Substrate Build Plan: Scoped Pre-Implementation Review Request

**From:** L1, routed by Mike
**Register:** closed, scoped. This is a pre-implementation review of a sequencing artifact, not a reopening of anything frozen or accepted. The Merge Specification v0.4 (FROZEN) and Contract E1 v0.8 (all textual blockers cleared, advancing to stage-1 qualification) govern; the build plan adds nothing normative — it sequences their implementation. The plan is carried verbatim below the rule.

## Scope of review (three questions; nothing else solicited)

1. **Sequencing soundness:** is the Gate-A-first build order (§2) sound — specifically, does certifying the ancestor-faithful core before any other component exists correctly exploit the gate architecture, or does any dependency in the phase order undermine a frozen certification's meaning? Legal answers: SOUND / DEFECT with location.
2. **Module-boundary defect surface:** does any module boundary or cross-cutting rule in §1 create a wrong-values-under-right-names surface, a state-sharing surface, or a stochastic-consumption path inconsistent with the frozen instrument's single-Generator regime and naming ledger? Legal answers: NONE FOUND / DEFECT with location.
3. **Silent divergence check:** does anything in the plan quietly diverge from the frozen specification or the E1 contract as verified — including the §3 execution split (L1 drafts, Mike executes and arbitrates, L3 closed-register verification only, L2 receives the stage-1 package) and the §5.4 pre-check arrangement (L1 runs Gate A against its own pinned clone as an error-catching pre-check, with the authoritative pass recorded on Mike's machine)? Legal answers: NO DIVERGENCE / DIVERGENCE with location.

**Out of scope, explicitly:** redesign proposals; re-review of any frozen or accepted provision; the stage-1 package itself (which comes to you separately, per standing practice, before contract freeze); resource questions (stage-1 deliverables). If review surfaces something outside the three questions that you judge implementation-blocking, name it as a BLOCKER with location rather than as commentary.

## Disposition requested

PROCEED TO CODE (with any per-question findings integrated), or BLOCKED with the named item. On PROCEED, first deliverables per §5 draft immediately; the plan is a living implementation document under Mike's control and is not frozen — findings from this review are integrated at Mike's word without a further verification round unless a finding is itself architectural.

---
# Substrate Build Plan — MFA-Fidelity Flight Instrument
## v0.1 (L1, for Mike's review; implementation follows the frozen Merge Specification v0.4 and serves Contract E1 v0.8's stage-1 qualification)

**Governing rule:** the frozen specification governs; this plan sequences its implementation and adds nothing to it. Where implementation work surfaces any divergence from the frozen spec, the divergence is surfaced to Mike (versioned spec successor if needed) — never absorbed. No production run is authorized by anything in this plan.

---

## §1 Module map (one package, `mfa_instrument/`)

| Module | Contents | Spec anchor |
|---|---|---|
| `config.py` | run-configuration dataclass (the single consumed object); canonical JSON serialization; run_config.json freeze + hash; run_record.json emission | §7.3, §9.2 |
| `rng.py` | master Generator; spawn derivation (noise stream, analysis streams, null streams); seed-derivation rules incl. six-decimal level keys | §1.1, D4, E1 §4.2 |
| `init.py` | Gate-A-lineage initialization (sequential cell-by-cell scalar draws, exact ancestor order, dtype discipline); fixed_count mode (Generator.permutation, declared order) | §5.1 |
| `dynamics.py` | the common execution skeleton; probability-construction dispatch (`symmetric_chain` computed as A's 13-step chain; `become_survive` computed directly); F dispatch (4 candidates incl. F_baseline legacy-unused); Q with Γ_Ψ/Γ_ρ and both bypasses (no-draw, no-read — code paths absent at zero, not zero-valued) | §§1.2, 2, 4, 6 |
| `telemetry.py` | 25-column family + Delta_from_Psi/Delta_from_rho + conditional Noise_Draw + rho_global tick table; chunked parquet streaming; telemetry digest (canonical byte construction) | §7.1–7.3 |
| `observables.py` | B-derived window/block machinery rebuilt on Generator draws; steady-state classifier (secondary diagnostic); Ψ-family emission | §7.1, S1(c)(5) |
| `verify.py` | Tier-1 row-level recomputation: realization invariant, drive decomposition, Q decomposition, Λ per dispatch; E1's bit-identity base check | §7.2, E1 §2 |
| `gates/gate_a.py` | structural preflight (six assertions) + behavioral bit-exact comparison vs `flight2_production.py` at matched seed | §8.1 |
| `gates/gate_b.py` | B1 deterministic rule equivalence vs `run_parity_check` pattern; B2 declared-ensemble distributional comparison | §8.2 |
| `gates/gate_r0.py` | projection-quantity correctness on constructed known-answer cases | §8.3 |
| `bridge/closure.py` | G_m derivation artifacts: quadrature over D_m, map iteration, fixed-point diagnostic, dense-grid reference classification (N/S/U + structure classes) | E1 §6, C.1 |
| `bridge/ensembles.py` | finite-N projection realizations; full-design projection sweeps (paired seeds, count rules, P2R router, bracket logic); envelope + informativeness computation | E1 C.3, v0.6 §C–D |
| `e1/nulls.py` | common-rank template; common replicate uniforms across m; per-level θ_P/θ_T with order-statistic CIs and precision halts; stability audit runner | E1 §4.2, v0.6 §B, v0.8 |
| `e1/classify.py` | run statuses (S_min/S_term precedence); level counts; the total verdict function; P2R router; collision proof/fallback | E1 §§4–5, v0.8 §E |
| `e1/audit.py` | constructed-series controls; forced-probability harness; morphology generators; held-out re-score; Clopper–Pearson caps | E1 §7 |
| `e1/sweep.py` | production sweep executor (level list, paired panel, tranche quarantine) — **built last; runs only after freeze + authorization** | E1 §8 |

Cross-cutting: every module consumes the config object; no module reads global state; all stochastic consumption via injected Generators; naming per the frozen ledger (u_base, Q_read, rule_mode, P2R-n, Δm_stab/est/loc, Δm_R).

## §2 Build order (dependency-driven, gate-first)

**Phase 1 — ancestor-faithful core (Gate A is the definition of done).**
1. `config`, `rng`, `init`, `dynamics` (symmetric_chain path only), `telemetry` minimal.
2. Gate-A structural preflight; then behavioral comparison against `flight2_production.py` cloned at `4d9a622`. **Bit-exact or halt:** any divergence is diagnosed via the preflight's separation (bypass violation vs. refactoring divergence) before proceeding. Nothing else builds until Gate A passes — every later component inherits its guarantee.
3. `verify` Tier-1 invariants streamed over the Gate-A run.

**Phase 2 — second witness.** `become_survive` dispatch; `observables` null-machinery rebuild; Gate B1 (deterministic, seedless) then B2 (ensemble). Definition of done: both layers pass at their frozen standards.

**Phase 3 — bridge machinery.** `bridge/closure` (G_m derivation **published as a stage-1 artifact** with the fixed-point diagnostic); Gate R0 on constructed cases; dense-grid reference classification with the stabilized null construction; stability audit (3 templates × 2 seed sets, primary-relative displacement vs. Δm_stab).

**Phase 4 — E1 qualification battery.** `e1/nulls` with precision halts; `e1/classify` with property-based totality tests and the collision proof attempt; `e1/audit` (controls → morphology audit → held-out re-score → caps); `bridge/ensembles` (T2-S design stability, T2-L envelope, informativeness gate e_L/e_U); total-Q-disable conformance preflight; resource benchmarks (wall-clock, storage, I/O, null-method cost) → **the complete stage-1 package assembles**.

**Phase 5 — freeze qualification.** Package to Mike (and to L2 per standing practice); every [PROPOSED] resolves; **Mike's freeze word**; then tranche; then production authorization. `e1/sweep` is exercised against synthetic config only until then.

## §3 Execution architecture (who does what)

- **L1** drafts all code as reviewable artifacts (full files, one per destination), plus the test harnesses and the closure derivation.
- **Mike** executes on the repo machine (canonical venv, pins per frozen §7.4), reviews, commits under the standing digest/commit discipline, arbitrates all halts.
- **L3** enters at Mike's discretion for substrate-level execution/verification tasks in closed register (e.g., independent recomputation checks, source-packet verifications) — consistent with the settled fact that the instrument is **pure NumPy**; Mesa on the machine stays unused.
- **L2** receives the stage-1 package for adversarial review before freeze; earlier consultation only if a spec divergence surfaces.
- Ops logs per session; L1 errors enumerated; every artifact digest-gated to the repo.

## §4 Verification posture (applied to our own build)

Pessimistic-on-passing governs the harnesses themselves: Gate A's preflight exists to make failure diagnosable, not to substitute for the behavioral gate; property-based tests verify the written verdict rules and create nothing; the morphology audit's held-out re-score guards against optimizing the classifier to its design examples; and any test that could pass for a reason other than the one it certifies is redesigned before it runs (the sed-verification lesson, standing).

## §5 First code deliverables (next session, in order)

1. `config.py` + `rng.py` + canonical-serialization tests.
2. `init.py` with the Gate-A draw-order discipline and its unit harness.
3. `dynamics.py` symmetric_chain path.
4. Gate-A preflight + comparison harness (requires the `4d9a622` clone on the repo machine — or I run it against my own pinned clone first as a pre-check, with the authoritative pass recorded on your machine).

*End of build plan v0.1. Mike's review; amendments at his word; then code.*
