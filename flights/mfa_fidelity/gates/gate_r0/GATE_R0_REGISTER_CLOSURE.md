# Gate R0 — Register Closure
**Status:** L2-ACCEPTED / AUTHORITATIVE / CLOSED, 2026-09-17. **Source:** `d17929e` (cleared identities: `bridge.py` `0f9d9292…`, `gate_r0.py` `4b4c7e5a…`), test repair `168cb80` (`test_gate_r0.py` `ddc515ad…`), design note `08a503ec…` (cited by `R0_GOVERNING`). **Run of record:** `6e7e683` — qualification `4099b5c0…`, AUTHORITATIVE report `b7786742…`, 28 mutant artifacts each bound by digest to its committed blob; no identity amendment. **Acceptance review of record:** `L2_GATE_R0_AUTHORITATIVE_ACCEPTANCE_REVIEW_RECEIVED.md`, placed beside this document. **Recorded by:** L1.

## 1. Permanent register statement (L2's text, verbatim)

> **Gate R0 — PASSED under AUTHORITATIVE conditions.**
> On the cleared instrument in the frozen canonical environment, formal qualification rejected and correctly attributed all 28 declared mutants, and the AUTHORITATIVE R0 run completed the exact frozen case map, comparator ledger, and refusal surface. The instrument and projection bridge computed the four Merge-Specification §8.3 projection quantities bit-exactly against independent exact-rational expectations on constructed cases: the local read, pre-update aggregate ρ(t) including tick-table persistence, the decomposed Q response with base updates and clip accounting, and the declared departure statistics. The gate also refused the three declared undefined-statistic cases. This is implementation validation only; it makes no claim about R1 recovery, targets, tolerances, Ψ, Regime II, or any E-rung phenomenology.

## 2. E1 precondition register (L2's text, verbatim)

> **Gates A, B, and R0 are AUTHORITATIVE and closed.** Certification preconditions for E1 are complete; E1 construction, contract freeze, and explicit seeding authorization remain outstanding.

## 3. Binding citation precisions (L2 §11–12)

1. **Stage qualifier mandatory.** The accepted object is *Gate R0 — projection-bridge implementation correctness*. "Gate R passed" without the stage qualifier is not a permitted citation. Gate R1 is a contract-level scientific recovery analysis, not a completed certification gate; MFP's adverse-evidence asymmetry becomes operative at R1 only after R1's targets and tolerances are frozen and the recovery experiment is run.
2. **Certification completion is not contract completion.** Completion of the three gates does not authorize E1 seeding.

## 4. Departure-statistic set of record (DECLARED by Mike, 2026-09-16; design note §4)

One statistic per mean-field move: local-read dispersion (population variance of `Local_Density` about `rho_global`); configuration–neighbourhood correlation (Pearson, across cells) together with Moran's I of `is_active` under toroidal Moore weights; per-base population mean and variance of (v, u_base, r). Measurement-side only; no target or tolerance — those are E1 §6's, frozen with the contract. R0 certifies their computation; R1 will use them as the attribution surface.

## 5. Forward obligations ledger (open; none blocks this closure)

| item | owner | due |
|---|---|---|
| **Dirty-path list or clean worktree** for future AUTHORITATIVE runs (L2 §9; also on the Gate B ledger) | L1 (runners) | next AUTHORITATIVE run |
| **Newline hardening** of the three Gate B atomic writers (`b1.py`, `b2.py`, `qualification.py`) — R0's writers were LF from day one and needed no amendment; the Gate B writers still do | L1 → L2 bounded review | before the next AUTHORITATIVE artifact-producing certification on those gates |
| **Gate A report environment embedding; ancestor read from the git object** (Gate A ledger) | L1 → L2 | unscheduled hardening |
| **Identity audit** of the three older pinned-ancestor tests | separately routed | unscheduled |
| **Item-4 O2/O3** (writer config single-source; `init_grid` provenance) | integration layer | when built |
| **E1 machinery** — steady-state observables, §5 classifier, controls, bootstrap, floor computation, compound-conservatism forecast; then stage-1 freeze qualification | L1 → L2 | next construction |
| **E1 contract** — evaluability and resource work; all values and verdict rules resolved and frozen; Mike's freeze act; Mike's separate seeding authorization | Mike (freeze, seeding); L1 (drafting) | after the machinery |

## 6. What the closure means

Three gates, three registers closed: the instrument reproduces Lineage A exactly, reproduces Lineage B's rule exactly and its ensembles equivalently, and computes the quantities the projection reads exactly and refuses what is undefined. It has been certified fit. It has asked nothing. The next construction is the machinery with which the first question — E1, the line on the ground — will be asked; and the first act of that construction, as with every gate before it, is reading the contract from the record.
