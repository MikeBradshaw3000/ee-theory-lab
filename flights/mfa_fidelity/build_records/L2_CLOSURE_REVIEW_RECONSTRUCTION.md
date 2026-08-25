# L2 Phase-1 Closure Review — Bounded Hardening Items 1–8

> **Archival re-export status:** This is the operative closure-review packet reconstructed from the subsequent hardening return, which reproduced all eight required items and the prescribed closure battery.

## Overall disposition

**CLOSURE HELD — ONE BOUNDED HARDENING PASS REQUIRED.**

The minimum repair set materially corrected the first source package. The remaining work was not a reopening of architecture or an invitation to opportunistic hardening. It was the following closed set.

## 1. Raw-storage Gate-A comparator

Replace numeric array equality as the basis of the bit-exact claim with one comparator that requires:

- equal shape;
- equal dtype; and
- identical C-order bytes.

Use it for all four state arrays and every Gate-A telemetry column. Add a negative test showing `np.array_equal(+0.0, -0.0)` can pass while the raw comparator rejects.

## 2. Explicit pinned-repository integration input

Delete the hard-coded `/home/claude/repo` path. Use a named external integration input such as `MFA_PINNED_REPO_ROOT`. Tests requiring the clone must skip with an explicit reason when it is absent; authoritative execution must supply it.

Run a static source/test path scan.

## 3. Tier-1 file-global identity coverage

Per-tick row counts cannot detect removal of one row and duplication of another from the same tick. Maintain a ledger over every expected `(Tick, Agent_X, Agent_Y)` key across all batches. Count duplicates on arrival and require every key at completion.

## 4. E1 identity file-global coverage

Apply the same exact-key discipline to the E1 base-bit identity verifier. Structural coverage and value identity are independent obligations: unchanged duplicated values cannot substitute for a missing cell.

## 5. Discriminating negatives

Add tests constructed to pass weaker checks:

- same-size duplicate-for-missing with duplicate copies in different verifier batches;
- E1 duplicate-for-missing where base bits are unchanged, so only key coverage catches it; and
- malformed rho schema that fails closed rather than raising during column indexing.

Assertions must demonstrate that ordinary total/per-tick count checks remain clean in the first case.

## 6. Neutral normative schema contract

Move the column ledger into a neutral specification-level module imported by both writer and verifier. The verifier may not obtain the expected schema from the output-producing module; otherwise one shared edit can move defect and expectation together.

## 7. Fail-closed rho handling

On rho-table schema mismatch, record failure and return before indexing or constructing the tick map. Malformed evidence must not crash or partially verify.

## 8. Independently frozen ancestor digest

Place the expected ancestor SHA-256 in an independently established, provenance-commented constant. The frozen identity must come from the commit-pinned object, not from the reference file at verification time. AUTHORITATIVE must raise if no expectation is supplied.

The governing rule is **verify, never establish**.

## Deliberately deferred hardening

A stronger verifier could reconstruct pre-update activity, `Local_Density`, `ds`, `Psi_local`, and `rho_global` independently from activity telemetry. That is legitimate later hardening, but it is outside this bounded closure register and must not expand it.

## Prescribed closure battery

The return must report:

1. the full suite with all new discriminating tests;
2. provisional Gate A for every ancestor-existing F form, with ancestor digest verification active;
3. static path scan over package and tests; and
4. a statement separating provisional success from the later authoritative frozen-environment run.

## L2 disposition

**PHASE 1 IS NOT YET CLOSED.**

Return only items 1–8 and the battery above. No other source broadening is requested.
