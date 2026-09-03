# Arbitration Brief — N3 Permanent Branch: `become_survive` under nonzero Q
**For:** Mike's ruling. **From:** L1 (third succession), 2026-08-25. **Register:** Phase-2 item 3 (Succession Dossier 2 §3.3).

## The question

The instrument currently **refuses at construction** any `become_survive` configuration with nonzero Q coefficients (Γ_Ψ ≠ 0 or Γ_ρ ≠ 0). This was L2's Phase-1 repair N3: the defect was *silent ignoring* of Q under the B rule; the repair made the unsupported combination raise loudly. The dossier names the permanent choice as yours: implement the common-Q skeleton for `become_survive`, or freeze the mechanical rejection as the supported subset.

## Premise verified against the frozen text

Spec §1.3 states frozen-bases is "a configuration realizing B-comparable conditions, not a reduced state vector." The spec neither commits nor forbids Q under `become_survive` — it is permissive. **Neither option requires a spec amendment.** The choice is an implementation-subset ruling, recorded in the contract layer.

## What Q would do under the B rule — the architectural fact the ruling turns on

The B rule reads no bases: Λ enters as the constant LOGIT_L, not as F(v,u,r). Under `become_survive`, Q would update v, u, r from Ψ_local/ρ while nothing downstream reads them. The bases become **instrumented passengers** — their trajectories observable, their values causally inert to the dynamics. Q under B is instrumentation, not mechanism, and cannot be otherwise without a new hybrid rule mode the spec does not name.

## Option A — implement the common-Q skeleton (passenger bases)

`become_survive` runs the same Q update the symmetric chain runs; the rule itself unchanged.

*For:* base trajectories under B dynamics become observable — a diagnostic comparing Q's response to B-generated activity fields against A-generated ones; keeps the two rule modes structurally parallel; removes a permanent asymmetry from the execution skeleton.
*Against:* new code and tests on a certified, L2-CLOSED module, hence a reopened review surface; a new **misreading hazard** — passenger-base trajectories under B invite interpretation as mechanism, which they are not, and guarding that requires vocabulary and telemetry labeling forever; no committed experiment consumes it — E1 is fixed-terrain, E4 exercises Q under the A chain, and no hybrid mode exists in the spec; Gate B gains nothing (it runs Q-disabled under either ruling).

## Option B — freeze the mechanical rejection as the supported subset

The construction-time refusal becomes permanent: `become_survive` supports Q-disabled configurations only, and says so loudly.

*For:* zero new code on certified modules; the refusal is honest ("not implemented," never "not meaningful"); matches every committed use of the B rule (Gate B, B-comparable observables, all Q-disabled); forecloses the passenger-mechanism misreading at the type level; fully reversible — if a future contract needs instrumented bases under B, the skeleton is implemented *then*, under that contract's review, with the phenomenological question stated first (named-not-triggered, the program's standing pattern for futures).
*Against:* the execution skeleton keeps a permanent asymmetry between rule modes; a future need pays its implementation cost later rather than amortizing it now.

## L1's read

**Option B.** The deciding consideration is phenomenology-outranks-formalism read in reverse: Option A's benefit is structural parallelism — formal elegance — while its cost is a standing misinterpretation surface on the phenomenology side. The program builds instruments for questions it has; the passenger-Q diagnostic answers no question anyone has registered, and the day it does, Option B's reversibility clause is the correct door. The current refusal is already the honest state: it names what is not implemented and halts.

## Ontological analysis (added at Mike's scrutiny before ruling, 2026-08-25)

§1.3 settles that bases exist-held in become_survive mode under either option. Option B mints no new kinds: a held base is a boundary condition (E1's own object rests on this role), and Q is out of jurisdiction, not denied — the refusal is a non-jurisdiction statement. Option A mints two kinds the theory does not license: **causally orphaned state** (bases written by Q, read by nothing — a record of what Q would have done stored as if it were world, where the theory defines bases functionally as the conditions shaping action through Λ) and a **severed-loop Q** (the function without the role: reads macro, writes bases, which configure nothing — the architectural sharpening that Λ-as-locally-configured is the only structure-to-agent channel makes the termination of that chain provable, not incidental). A third shift: Psi_local's standing would become configuration-dependent (mechanism-input in one mode, emission-only in the other) — wrong-values-under-right-names lifted to the kind level. The action primitive is untouched either way, and neither option advances the coupled ignition boundary, which requires bases→Λ closed and must never be narrated as nearer under passenger bases.

## What the ruling binds

Option B: the N3 refusal text gains "permanent supported subset per Mike's ruling of record" with date; the ruling record commits beside this brief; TelemetryWriter's B-field integration (Phase-2 item 4) proceeds against the Q-disabled subset only. Option A: an implementation contract is drafted for L2 review before any code, with the misreading guard specified inside it. Either ruling leaves Gate B untouched.
