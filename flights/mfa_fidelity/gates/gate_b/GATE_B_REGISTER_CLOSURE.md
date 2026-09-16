# Gate B — Register Closure
**Status:** L2-ACCEPTED / CLOSED, 2026-09-16. **Certification:** `bf6b12d` (record), `cf100c6` (Amendment 1). **Acceptance review of record:** `L2_GATE_B_AUTHORITATIVE_ACCEPTANCE_REVIEW_RECEIVED.md`, placed beside this document. **Recorded by:** L1.

## 1. Permanent register statement (L2's text, verbatim)

> **Gate B — PASSED under AUTHORITATIVE conditions.**
> The merged instrument's `become_survive` path achieved exact deterministic step-level rule equivalence under the frozen B1 comparator battery and satisfied the frozen Path-B ensemble criterion across all eight declared B2 cells: terminal-window ensemble-mean equivalence within ±0.003, with no priced gross-divergence alarm. The certification is limited to the Q-disabled Path-B domain and makes no claim about full distributional equivalence, Ψ, Regime II, ecosystem phenomenology, Gate A, or Gate R.

## 2. Binding citation precisions (L2 §5–6)

1. **Step level.** "Bit-identical" is shorthand only. The exact evidence: `p_become`, ancestor-derived `g_q`, `p_survive`, and schedule `u_t` under raw float64-bit equality; next state under exact logical equality after canonicalizing the ancestor's integer state to the candidate's committed Boolean dtype; the shared declared random grid under exact identity through the counted stub. Cite as: *exact deterministic step-level rule equivalence under the frozen B1 comparators.*
2. **Artifact identities.** Committed LF blobs are the repository identities of record (certification `940d88a4…`, qualification `46d905b3…`, B1 `2a715899…`, B2 `db70e78a…`). The execution-time CRLF digests remain valid provenance of the bytes written on the canonical machine. The per-mutant `artifact_sha256` values inside the qualification record are execution-time identities; Amendment 1 travels with that record whenever they are cited.
3. **"No candidate output consulted"** carries its governance meaning: no candidate output selected or relaxed any element of the frozen grammar. Candidate output was, of course, evaluated by the frozen gate.

## 3. Jurisdiction (L2 O2)

Gate B acceptance is not Gate A preservation, not Gate R recovery, not observables validity, and not evidence for any E-rung phenomenology. The three certification gates remain separate.

## 4. Forward obligations ledger (open; none blocks this closure)

| item | owner | due |
|---|---|---|
| **Newline hardening** — the three atomic writers (`b1.py`, `b2.py`, `qualification.py`) open JSON output without `newline="\n"`; bounded, separately reviewed change | L1 → L2 source review | before the next AUTHORITATIVE artifact-producing certification (L2 §6) |
| **Clean-worktree or dirty-path list** — future AUTHORITATIVE run records emit the full dirty-path list, or run from a clean worktree | L1 (runner) | next AUTHORITATIVE run (L2 O3) |
| **Identity audit** — three pre-existing pinned-ancestor tests import the worktree module without hashing it | separately routed | unscheduled (L2 platform-identity ruling O3) |
| **O2 / O3 from Phase-2 item 4** — writer construction bound single-source to the consumed `RunConfig`; `init_grid` provenance bound to recorded initialization | integration layer consuming the B telemetry family | when that consumer is built |
| **Gate A standing after `dynamics.py` change** — the authorized O1 noise guard (`948a517`) altered `dynamics.py` after Gate A's Phase-1 closure; the guard sits in the B-mode constructor path and the A chain is untouched, and the instrument suite's Gate A tests pass, but whether Gate A's AUTHORITATIVE standing requires a formal re-run is a governance question for Mike, not resolved here | Mike | next session |
| **Phase-2 item 2** — observables rebuild (B's window/block Moran machinery, measurement-side) | L1 | next Phase-2 build |

## 5. What the closure means

The instrument is certified fit to run Lineage B's rule. Under the Q-disabled subset it reproduces that rule exactly at step level and equivalently at ensemble level, in a canonical environment, from the pinned ancestor's committed bytes, under a grammar frozen before any of it ran. It has asked no question of the phenomenology. That is the next thing it does.
