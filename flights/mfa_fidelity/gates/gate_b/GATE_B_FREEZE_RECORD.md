# Freeze Record — Gate B Specification v0.4, Comparator Set and Acceptance Grammar
**Frozen by:** Mike Bradshaw, Theory Architect. **Date of freeze:** 2026-09-04. **Recorded by:** L1 (third succession), 2026-09-04. **Status:** RATIFIED by Mike, 2026-09-04. Never-relax-after-output is in force from this date.

## 1. What is frozen

**Gate B Specification v0.4** — the v0.4 changed-text layer over v0.3, carrying v0.3 in full except Amendments 4 and 6, which v0.4 replaces with 4R and 6R.

- Frozen document: `flights/mfa_fidelity/gates/gate_b/GATE_B_SPECIFICATION_v0_4.md`, committed at `32dd0ef`, sha256
  `e2f06bb1ad0aaa7ff05cc3da4b69c4b87bbad5c54bb7cafc4e78d4ee029e7fbd`.
- The v0.3 layer it amends and the v0.1/v0.2 lineage remain the record of how the frozen text was reached; on any discrepancy the frozen v0.4 text governs.

### 1.1 Comparator set (frozen)

- `p_become` arrays, scalar `p_survive`, and `g_q`: **raw float64 bit equality** — shape and dtype asserted first, then elementwise `uint64`-view comparison, signed-zero discriminating. Candidate `p_survive` must share the bits of ancestor `LAMBDA`. (OPEN-1 ruling of 2026-08-25, implemented at v0.2, unreopened through three subsequent reviews.)
- Next state: ancestor output asserted binary integer {0,1}; candidate asserted the frozen boolean dtype; exact logical equality after canonicalization. The candidate never abandons its committed dtype to pass.
- The ancestor-pattern `allclose` is computed and reported as diagnostic only; it is not a comparator.

### 1.2 Acceptance grammar (frozen)

- **Mean equivalence (positive certification):** per cell, Welch two-one-sided tests on per-run terminal-window mean ρ (ticks 300–399); equivalence margin **δ = 0.003**; α_cell = 0.05/8 (Bonferroni across the eight-cell family, familywise 0.05); the 98.75% Welch interval of the candidate−reference mean difference must lie entirely within ±δ; **all eight cells must pass**.
- **Gross-divergence screen (priced, failure-triggering):** tie-invariant ECDF statistic D_int = max over unique pooled values of |2a − s|; exact conditional permutation null **given the observed tie-block sizes**, enumerated by dynamic programming with weights ∏ C(b_i, c_i); alarm iff **p = P(D_int ≥ D_obs | tie blocks) ≤ α_KS = 0.00125**, boundary inclusive; familywise KS budget 0.01 by Bonferroni across the eight cells. No-tie reduction verified exactly: P(D_int ≥ 12) = 153,809,370 / C(40,20) = 0.0011158015462314926 — recomputed independently by L2.
- **Ensembles:** eight cells (six CM-0, two CM-1, both κ signs in both arms); 20 runs per side; reference certification seeds 201–220, candidate certification roots 301–320, disjoint from the calibration pool 101–120 and the forecast pool 401–600.
- **Feasibility bound implied by this grammar:** s < δ / (t₀.₉₉₃₇₅,df · √(2/20)) ≈ 0.00362 at equal SDs. Observed reference SDs: max 0.001841 (calibration), 0.001084 (forecast pool).
- **Block means** are diagnostic-only; any promotion to acceptance is a versioned amendment with its own power record.

### 1.3 Certified claim (frozen, per Mike's Path-B ruling of 2026-08-26)

Gate B2 certifies **terminal-window ensemble-mean equivalence plus the priced gross-divergence screen, and nothing more**. It does not certify distributional equivalence; a genuine distributional-equivalence criterion is a named future object conditioned on an ensemble size that would give it real discriminating power. Every Gate-B report carries this claim statement verbatim.

## 2. What supports the freeze

- **Canonical calibration record** (`44125c64d935992d…`), committed at `32dd0ef`: eight cells, canonical environment, feasibility satisfied in every cell.
- **Canonical joint-forecast record** (`22e6808009593381…`), committed at `32dd0ef`: complete frozen family traversed jointly with cross-cell dependence preserved — TOST 4000/4000, screen no-alarm 3977/4000, full-gate 3977/4000, power against a 0.005 mean divergence 4000/4000 fail; every integer identical to the provisional record, discharging Amendment 6R's canonical-rerun condition.
- **L2 verdict of record** (`81287e53afd10f8d…`, 2026-09-04): all four v0.4 repairs corrected as required; no repair-introduced defect; **FREEZE MAY PROCEED**. L2 independently recomputed both the packet digest and the no-tie tail probability.
- **Review lineage:** v0.1 → four L2 rounds (thirteen freeze items, ten OPEN-2 items, four freeze blockers, four v0.4 repair items) → v0.4. The OPEN-1 comparator ruling and Mike's Path-B claim ruling are of record in the repository.

## 3. What freeze binds

**Never-relax-after-output takes effect at ratification.** From this moment nothing in the comparator set or acceptance grammar may be derived from, adjusted in light of, or reinterpreted because of any certification output. Thresholds, margins, seed pools, cell definitions, and the screen algorithm are fixed. A gate that could be loosened after seeing a result is not a gate; if the frozen grammar proves wrong, the remedy is a recorded, versioned, pre-output amendment by Mike's explicit act — never an adjustment.

## 4. What freeze does NOT authorize

No AUTHORITATIVE Gate B execution. Seven implementation preconditions stand between this freeze and any candidate run, all mandatory and all held open:

1. source review of the executable B2 wrapper;
2. the ten-run wrapper bit-identity record against pinned `execute_run` (one canonical run per B2 cell, plus seed 137 in both CM-1 cells);
3. qualification against the complete 30-mutant negative battery with **per-mutant attribution** (which comparator or structural check rejects each);
4. recorded FP-witness uint64 bit patterns for the logit-association mutant;
5. prospective solved-offset enumeration before qualification;
6. mutant-30 frozen-input determinism and window-coverage proof;
7. source-level verification that the conditional-permutation dynamic program and the canonical forecast record implement the frozen v0.4 algorithm exactly.

Also held open and not absorbed by this freeze: **O2** (writer/runner construction bound single-source to the consumed `RunConfig`) and **O3** (`init_grid` provenance bound to recorded run initialization), both due at the runner/Gate-B2 integration packet.

## 5. Ratification

Ratified by Mike's word of 2026-09-04, given after reading this record in full. It commits to `flights/mfa_fidelity/gates/gate_b/` beside the specification and the canonical records, and the L2 verdict is placed alongside it as `L2_GATE_B_V0_4_CHANGED_TEXT_VERIFICATION_RECEIVED.md`.
