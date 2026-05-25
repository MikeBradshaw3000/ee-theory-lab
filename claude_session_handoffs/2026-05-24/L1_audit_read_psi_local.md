# Layer 1 Architectural Read — the `Psi_local` Computation (Flight 6)

**Status.** Layer 1 / architectural-guardian read of the located primary source, for
cross-check. **NOT a closed determination.** The formal §1 audit remains Gemini's
against the code; whether the measure can serve as Ψ is a mean-field / operationalization
question for ChatGPT (Layer 2); Mike arbitrates.

## The located rule (primary source)
- `Flight_6/flight6_phase4A_runner.py`, `class Flight6Model(f3.EEModel)`, `step()`,
  lines ~85–95 — the coherence computation.
- `Flight_6/flight3_final_remediation.py` — base `EEAgent` / `EEModel` (activation
  dynamics only; inherits only Mesa `Agent`/`Model`, no further project layer). The base
  model's `step` just runs the agents; `psi_history` is an empty slot the runner fills.
- Persisted `Psi_local` column = per-agent `local_psi`.
- Canonical-copy note: a second `flight3_final_remediation.py` exists at the repo root
  defining differently-named classes (`EcosystemAgent`/`EcosystemModel`, different MD5).
  The runner imports by bare name from its own directory, so the **Flight 6 copy**
  (`EEAgent`/`EEModel`) is the one that ran. The root copy is a different lineage and is
  not the audit target.

Computation, per tick, after agents act:
```
ds_x = state_history[-1] − state_history[-2]        # ∈ {−1, 0, +1}
local_psi(a) = ds_a × Σ over Moore-neighbors ( ds_n )
current_psi  = mean of local_psi over agents
```
In words: a cell's `Psi_local` is its own activation-state change times the summed
activation-state changes of its eight neighbors — positive when cell and neighbors switch
the same way together, negative when oppositely, zero when the cell itself did not switch.

## §1 audit verdict (a / b / c): PASSES
- **(a) No global/aggregate density input.** Uses only own and neighbor state-changes;
  `current_rho` is computed afterward and never fed in. `local_density` exists but is not
  consumed by the coherence rule.
- **(b) No coefficient.** No density-keyed, sign-changing term; not a discretization of
  dΨ/dt = μ(ρ)Ψ − γΨ³.
- **(c) Continuous neighbor-weighted accumulation.** The `if ds_a != 0` guard is a no-op
  (gates on the cell's own change, not a neighbor count); no hard "≥ N active neighbors"
  threshold.

**Consequence — the good news for "baked in":** the substrate does not install the
second-stage coherence transition. Coherence is *measured* as a spatial co-movement
statistic on the activation field, not imposed by a normal form. A divergence appearing
here cannot be the discretized second equation, because there is no second equation. This
is the measure-don't-impose posture `defeat_baked_in.md` asks for.

## Pessimistic-on-passing — necessary, not sufficient: the operationalization gap
Passing (a/b/c) screens for baked-in-ness. It does not establish that `Psi_local` is
coherence-as-Ψ. Two concerns, both §5.3/§5.4 of `defeat_baked_in.md`:

1. **Transition-correlation, not sustained order parameter.** The measure is built on
   state *changes* (`ds`), so it is closer to a fluctuation/susceptibility statistic than
   to the theory's Ψ, which is a sustained order parameter — high and persistent in the
   coherent regime. Whether it stays high in Regime III and near-zero in a *persistent*
   Regime II must be tested, not assumed. Positive-control requirement: a configuration
   known to be coherent must read high Ψ; a transition-correlation may read ≈ 0 when the
   coherent state is quiet.
2. **Signed mean → cancellation.** Positively- and negatively-co-switching regions can
   cancel in the aggregate, masking spatial structure. The prescribed fix is already in
   `defeat_baked_in.md` §5.3: a spatial-autocorrelation (B2(A)) framing that registers
   mutual-reinforcement structure, not a naive signed mean.

## The mystery, landed
The `Psi_local` column that the Phase-4B substrate-trust, schema, and adapter work was
hardened around is this 4A-era co-movement-of-transitions statistic. The custodial period
verified, schematized, and protected the column without re-deriving whether it
operationalizes the theory's Ψ. Leading the resume with Regime-II-as-structural and
gating the routing on the audit is what forced the re-examination — the goal-anchor
reorientation paying out concretely.

## What this is NOT
Not a verdict that the substrate is unusable. The measure-don't-impose architecture is
right for "baked in." The live question is narrow and resolvable: is
co-movement-of-transitions an acceptable operationalization of coherence, and does it show
a *persistent* Regime-II signature under a spatial-autocorrelation aggregate with a
positive control?

## Routing
- **Gemini (Layer 3):** run the formal §1 audit on the located code (runner lines ~85–95
  + base module), confirm or correct this read; only then address §3 measurement. Add to
  §3: does `Psi_local` pass a positive control and a steady-state persistence check
  (`defeat_baked_in.md` §5.3–5.4)?
- **ChatGPT (Layer 2):** mean-field question — can a co-movement-of-activation-transitions
  statistic serve as the coherence order parameter Ψ, or does Ψ require a sustained-state
  measure? Coherence operationalization is an open element; this is where it is adjudicated.
- **Mike:** arbitrates whether to (i) reframe the aggregate (spatial autocorrelation +
  positive control, possibly salvaging existing runs) or (ii) commission a new substrate
  with a coherence measure that behaves as a sustained order parameter.
