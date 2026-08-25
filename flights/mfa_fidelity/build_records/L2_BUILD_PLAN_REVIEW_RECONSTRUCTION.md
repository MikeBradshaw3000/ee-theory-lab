# L2 Review — MFA-Fidelity Instrument Build Plan v0.1

> **Archival re-export status:** The operative L2 ruling is reconstructed from the successor build record and the later Phase-1 source-review packets. The original turn is not available byte-for-byte in the active record. No new ruling is introduced here.

## Overall disposition

**VERDICT: PROCEED TO CODE, SUBJECT TO THE NINE FINDINGS BELOW.**

The plan is sound in its governing architecture: build a new instrument, keep the two ancestor witnesses separate, preserve the frozen merge specification as the source of truth, and make verification part of construction rather than a downstream report. It was not, however, sufficient as written to support a later claim that Phase 1 was complete. The defects below had to be folded before or during implementation.

No part of this review authorizes execution of E1, seeding, or contract freeze.

## Findings 1–9

### 1. Package decomposition and ancestor-witness structure

**SOUND.**

The plan correctly separates configuration, RNG, initialization, dynamics, telemetry, verification, and ancestor-gate code. Gate A, Gate B, and Gate R are different certification objects and must remain different modules and reports. Passing one can never compensate for another.

### 2. Build order

**DEFECT.**

The proposed sequence treated some supposedly later components as if they could be added after the dynamics core without affecting the core. That is not safe. The first Phase-1 slice must already contain:

- the single authoritative causal `Psi_local` computation;
- the Q update location and timing, even where a channel is disabled;
- the role-separated RNG registry and zero-channel bypasses;
- the telemetry fields needed to prove the execution order; and
- the exact initialization algorithm used by Gate A.

Dense-grid references, production runners, and higher-level classifiers should follow only after those dependencies are fixed.

### 3. Gate-A lifecycle

**DEFECT.**

The plan did not sharply enough separate a build-time checkpoint from the authoritative certification. Every Gate-A run during construction is **PROVISIONAL**. The authoritative Gate A occurs only on the complete integrated Phase-1 commit, on Mike's execution machine, in the frozen environment, against the independently frozen ancestor digest.

Any change touching initialization, draw order, dynamics arithmetic, state ownership, telemetry, schema, or Gate-A harness code invalidates the prior checkpoint and requires the provisional comparison to be rerun. The final authoritative regression is a closure precondition, not an early milestone that later code may inherit.

### 4. RNG ownership and derivation

**DEFECT.**

The plan needed a stronger ownership rule:

- one explicitly managed dynamics stream;
- separately derived role streams for noise and analysis/null work;
- no role stream constructed when its amplitude/channel is zero;
- no seed derivation may consume the dynamics generator;
- derivation provenance must be recordable; and
- the Gate-A registry must mechanically forbid non-ancestor streams.

Documentation that streams “should not” interfere is insufficient. The code must make interference impossible or fail closed.

### 5. Configuration immutability and consumed-object identity

**DEFECT.**

Every behavior-changing choice must be represented in the immutable configuration object that the run actually consumes. Runner-only switches, defaulted arguments, or unrecorded policy flags are prohibited, especially where they alter initialization or RNG consumption.

The pre-run `run_config` must be serialized from that same object. No transcription layer may create a second set of values under the same names.

### 6. Mutable-state and mechanism ownership

**DEFECT.**

The build plan needed one exclusive owner of mutable `v`, `u_base`, `r`, and `is_active` state: the dynamics object. The object receiving initialized arrays must take private ownership. Telemetry consumers receive copies or read-only values and can never feed values back into Q.

Likewise, `Psi_local` must have one authoritative causal implementation. A separate “telemetry Psi” and “mechanism Psi” would create a wrong-values-under-right-names surface.

### 7. Classifier/null implementation ownership

**DEFECT.**

The plan allowed too much risk of duplicated logic between production code, bridge code, audit code, and tests. Any null, classifier, or projection quantity that later carries a verdict must have one normative implementation or one normative specification-level contract, with independent known-answer verification.

A verifier may not learn its expected schema or formula from the same mutable implementation whose output it verifies.

### 8. E1 qualification path and resource measurement

**DEFECT.**

The E1 qualification path must exist before resource estimates are treated as binding. A benchmark on a reduced or differently instrumented path does not price the production object. The build must first support the frozen E1 configuration, including total-Q disable and `rho_global` emission for Gate R; then wall-clock, storage, hashing, and readback costs can be measured.

The contract, not the runner, decides which F arm and seed/level design is production.

### 9. Closure standard

**SOUND, WITH REQUIRED PRECISION.**

The plan is correct that Phase 1 closes only after source review, repair verification, discriminating negatives, and final ancestor regression. The closure statement must distinguish:

- unit/integration suite pass;
- provisional Gate-A checkpoints;
- authoritative Gate-A certification;
- unresolved later-phase work; and
- items deliberately deferred outside the closed Phase-1 register.

“Tests pass” alone is not a closure verdict.

## Required build-plan fold

The successor plan should therefore state explicitly:

1. construction begins with immutable config and role-separated RNG;
2. dynamics owns all mutable state and the causal `Psi_local`;
3. telemetry is observational only;
4. Gate A is provisional until final integrated regression;
5. Gate B and Gate R remain separate certification layers;
6. every behavior-changing mode is configuration-bound;
7. E1 qualification exists before production resource pricing; and
8. Phase 1 cannot close on self-reported implementation success.

## Final L2 disposition

**BUILD PLAN MAY ADVANCE TO CODE WITH THESE FINDINGS BINDING.**

This is permission to construct and review the instrument, not permission to run E1 or seed any flight.
