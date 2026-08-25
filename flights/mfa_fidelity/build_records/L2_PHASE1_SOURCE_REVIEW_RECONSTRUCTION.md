# L2 Phase-1 Source Review — D/V/N Findings and Minimum Repair Set

> **Archival re-export status:** Reconstructed from the complete Phase-1 repair packet and the later bounded-hardening return. The operative defect and repair register is preserved; this is not claimed to be byte-verbatim.

## Overall verdict

**PHASE 1 NOT COMPLETE — MINIMUM REPAIR SET 1–10 REQUIRED.**

The source review found that several first-audit defects were repaired in direction, but the package still did not earn closure. The governing finding register is below.

## D findings — dynamics/configuration

### D1(a) — live-state alias surface

`Dynamics` must own private copies of all four mutable state arrays. Caller-retained initialization arrays may not remain live aliases.

### D1(b) — sink-to-Q alias surface

Telemetry must receive a copy of the delta. No sink-controlled array may feed the Step-12 Q update.

### D2 — base-draw policy

Initialization policy must be immutable, config-bound, serialized, and cross-validated. A runner-side `draw_bases` argument is prohibited. The negative test must compare the post-initialization generator state/output, not merely the initialized arrays.

### D5 — Gate-A gate semantics

Gate-A labels must be closed. `behavioral_bit_exact` must remain distinct from the stronger `gate_passed`; `passed` may not expose the weak result under the strong name. AUTHORITATIVE requires both environment conformance and an independently supplied expected ancestor digest.

## N findings — new/integration surfaces

### N1/N2 — `rho_global`

Emission must be independent of Q's read mode, persisted as a tick-level artifact, hashed with the cell telemetry, and verified for schema and exact tick coverage. An E1 total-Q-disable local-primary run must still be able to emit it for Gate R.

### N3 — unsupported Q in `become_survive`

Silently ignoring nonzero Q is prohibited. Until the common-Q branch is implemented, construction must reject that configuration. The permanent choice belongs to the later integration phase.

### N4/N5 — reference and label provenance

The gate must report the ancestor digest, reject unknown labels, and require the expected digest for authoritative certification. Verification may check a frozen identity; it may not establish that identity from the file under test.

## V findings — verification

### V1 — schema obligation

Expected columns must be derived from the consumed configuration and a neutral normative schema contract, not from the writer whose output is being checked. Missing and forbidden columns both fail before recomputation.

### V2 — global-Q recomputation

For global mode, verify `Delta_from_rho == gamma_rho * rho_global(t)` by joining each cell row to the persisted tick table. A planted tiny defect must be detected.

### V3 — file completeness

Empty input, zero rows, truncation, dropped ticks, dropped rows, duplicate rows, and duplicate-for-missing substitutions must fail. Exact total and per-tick counts are necessary but not sufficient; a file-global key ledger is required.

### V4 — E1 base identity

The E1 total-Q-disable check must compare float64 raw bits, require tick-0 baselines for every cell, reject late anchoring, and require exact key coverage. Numeric equality is insufficient because `+0.0` and `-0.0` differ in storage.

### V5 — formula coverage

The verifier must include `Term_Offset`, `gamma_coef`, `Delta_from_Psi == 0` where `Gamma_Psi == 0`, global `Delta_from_rho`, and the rho table's own schema/coverage.

### V6 — portable imports

All tests and modules must be repository-relative or use an explicit integration input. `/home/claude/repo` or any other machine-local source path is a defect.

### V7 — discriminating negative matrix

At minimum include planted failures for missing/forbidden schema, empty and truncated files, dropped/duplicated rows, cross-batch duplicate-for-missing, malformed rho schema, missing rho artifact, global-Q arithmetic, `Term_Offset`, `gamma_coef`, ulp-level bit identity, missing tick-0, and hostile ownership attacks.

## Minimum repair set 1–10

1. **Private state ownership and telemetry-copy isolation.**
2. **Config-bound base initialization mode; runner switch removed; post-init RNG-state test.**
3. **Closed Gate-A labels, strong `passed` semantics, mandatory authoritative ancestor provenance.**
4. **`rho_global` emission decoupled from Q read, persisted, hashed, and verified.**
5. **Reject unsupported nonzero-Q `become_survive` configurations.**
6. **Independent schema and exact completeness enforcement.**
7. **Global-Q tick-join recomputation with planted-defect test.**
8. **Bitwise, tick-0-anchored E1 identity with complete key coverage.**
9. **Remove machine-specific imports and paths.**
10. **Complete the discriminating negative matrix and V5 formula checks.**

## Required return grammar

For each item: **REPAIRED AS REQUIRED** or **REPAIR DEFECT**, followed by **NONE FOUND** or a new-defect register, and a Phase-1 closure disposition.

## L2 disposition

**PHASE 1 REMAINS OPEN PENDING SOURCE-LEVEL REPAIR VERIFICATION AND THE FINAL AUTHORITATIVE REGRESSION REQUIRED BY THE BUILD PLAN.**
