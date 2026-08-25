# Substrate Build Plan — MFA-Fidelity Flight Instrument
## v0.2 (L2 pre-implementation findings 1–9 integrated; living implementation document under Mike's control; PROCEED TO CODE granted on this basis)

**Governing rule unchanged:** the frozen Merge Specification v0.4 and Contract E1 v0.8 govern; this plan sequences; divergences surface to Mike.

---

## §1 Module map (corrected boundaries)

| Module | Contents | Key boundary rules (L2 findings A–E) |
|---|---|---|
| `config.py` | run-configuration as **deeply immutable** frozen dataclasses; validation at construction; **no module mutates, normalizes, or defaults into it post-validation**; canonical JSON serialized from the exact immutable object; run-derived state lives in a separate run context / run_record, never in config | C |
| `rng.py` | **immutable seed provenance**: root SeedSequence registry; **role-specific named streams** — `dynamics_rng`, `noise_rng`, `observable_null_rng`, `null_generation_rng`, `audit_rng`, `bootstrap_rng`, `projection_ensemble_rng` — each derived from immutable seed material, **never by consuming draws from another stream**; typed handles so a module cannot receive the wrong role; all derivations recorded prospectively in run_config; under the Gate-A configuration, non-ancestor roles are **absent, not idle** | B |
| `init.py` | Gate-A-lineage initialization (sequential scalar draws, ancestor order, dtype discipline); fixed_count mode | — |
| `dynamics.py` | common skeleton; probability-construction dispatch; F dispatch; Q with both bypasses (paths absent at zero); **sole owner of mutable v/u_base/r/is_active state** — all other modules receive immutable snapshots or read-only views, never writeable aliases; **owns the single authoritative causal Ψ_local computation** (mechanism side; built in Phase 1) | A, D |
| `telemetry.py` | full column family; chunked parquet; digests; consumes read-only state | D |
| `observables.py` | aggregate/state/persistence Ψ families and B-derived window machinery — **measurement only: consumes dynamics' read-only Ψ_local output; never supplies any value back to Q; no second Ψ_local implementation exists anywhere** | A |
| `verify.py` | Tier-1 recomputation; E1 bit-identity check | — |
| `gates/` | gate_a (structural preflight + behavioral comparison), gate_b (B1, B2), gate_r0 | — |
| `bridge/closure.py` | G_m derivation, iteration, fixed-point diagnostic | — |
| `e1/nulls.py` | **the one authoritative null API** (template, common uniforms, θ computation, precision halts) used by production classification, dense-grid reference work, audits, and ensembles alike | E |
| `e1/classify.py` | **pure, authoritative functions** for run status, level status, P2R routing, final verdict, collision proof/fallback — the only implementation; every consumer calls these functions; no copied thresholds, counts, precedence, or bracket logic anywhere | E |
| `bridge/ensembles.py` | finite-N realizations and full-design projection sweeps — **calls e1/classify and e1/nulls directly**; envelope, informativeness (e_L/e_U) | E |
| `e1/audit.py` | constructed controls, forced-probability harness, morphology generators, held-out re-score, caps — calls the authoritative functions | E |
| `e1/sweep.py` | production orchestration (levels, panel, tranche quarantine, restart, hashing) — **built in Phase 8, hard-locked to synthetic/qualification configurations**; the lock releases only at post-freeze tranche (quarantined) and production authorization | — |

**Instrument provenance wording (finding 8, corrected):** the *dynamics substrate* is pure NumPy; Mesa is present-unused; telemetry, parquet emission, and verification use the frozen pinned pandas/pyarrow stack per spec §7.4.

## §2 Build order (corrected sequence; Gate A provisional-then-authoritative)

1. **Core:** config, rng, init, dynamics **including causal Ψ_local**, ancestor-comparable telemetry.
2. **Initial Gate-A integration checkpoint (PROVISIONAL)** + Tier-1 verification. Explicitly non-certifying: a checkpoint, not the certification. **Gate A reruns after every change to any Gate-A-reachable component** (config, rng, init, dynamics, Ψ_local, telemetry, and any instrumentation executing in the Gate-A configuration) — cheap regression, run habitually.
3. become_survive branch; observables (measurement-side); Gate B (B1 then B2).
4. Closure; Gate R0.
5. **e1/nulls and e1/classify** (the authoritative implementations, with property-based totality tests and the collision proof attempt).
6. Dense-grid reference classification and reference-stability audit (now correctly *after* their null/classifier dependencies).
7. Morphology audit + held-out re-score; full-design projection ensembles (T2-S stability, T2-L envelope, informativeness).
8. **Qualification-locked e1/sweep** — the actual orchestration/telemetry/restart/hashing/level-run path exercised on synthetic configs — then **resource benchmarks measured on that real path**.
9. **FINAL AUTHORITATIVE Gate A / Gate B / R0 regression on the complete integrated stage-1 commit.** This run, and only this run, is the certification the stage-1 package reports.
10. Stage-1 package assembly → Mike (and L2 per standing practice) → every [PROPOSED] resolves → **Mike's freeze word** → tranche → production authorization.

## §3 Execution architecture (finding-9 conditions integrated)

L1 drafts all code as reviewable full-file artifacts. Mike executes on the repo machine (canonical venv, frozen pins), reviews, commits, arbitrates. L3: closed-register verification at Mike's discretion. L2: receives the stage-1 package before freeze; earlier only on spec divergence.
**L1 pre-check (bounded per L2's four conditions):** L1 may run Gate-A comparisons against its own clone pinned at `4d9a622` strictly as a **documented non-authoritative pre-check** — labeled as such; environment, code digest, seed, and comparison scope recorded; **incapable of satisfying or partially satisfying Gate A in the official record**; the authoritative pass occurs on Mike's machine, canonical venv, against the complete integrated stage-1 commit (step 9).

## §4 Verification posture (unchanged, plus)

Pessimistic-on-passing applied to our tooling; property-based tests verify written rules; held-out re-scores guard classifier optimization; **and the provisional/authoritative Gate-A distinction is itself a pessimistic-on-passing instance** — a pass obtained on a partial instrument is treated as evidence of nothing about the whole.

## §5 First deliverables (drafting now)

1. `config.py` — immutable configuration + canonical serialization + validation tests.
2. `rng.py` — seed registry + role streams + provenance recording + tests.
3. `init.py`, then `dynamics.py` with causal Ψ_local, then the provisional Gate-A harness.

*End of v0.2. Living document; amendments at Mike's word.*
