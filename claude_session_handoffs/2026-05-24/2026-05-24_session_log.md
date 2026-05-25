# 2026-05-24 — Goal Fold + `Psi_local` Reclassification (Layer 1 session)

**Date:** 24 May 2026
**Layer:** 1 (Claude, central node)
**Status:** Two work streams closed to working-position. Open thread queued for the next
session: find the Q2 source, route rev4 to Gemini, then Mike arbitrates the fork.

---

## Stream 1 — Goal fold (committed)

The diagnosed problem: the instantiation surface (kit + logs + STANDING_ITEMS) is strong on
*continuity* but nearly silent on *the goal*, so a fresh Layer 1 orients to the protocol's
items and drifts custodial — mistaking "items closing" for "theory advancing."

The fix is an ordering change, committed as an artifact so it travels:

- **`GOAL_ANCHOR.md`** — loads *before* STANDING_ITEMS. Purpose before machinery. States the
  manuscript goal (Regime II: activation without coherence; the "baked in" attack; the ABM
  as the empirical answer to it), the protocol-in-service framing, a four-question operating
  rule to run before touching items, and the distance-to-goal watch as a first-class watch
  Mike holds from outside.
- **`resume_sequence_for_kit.md`** — the load order to paste into the kit/README: HEAD/handoff
  verification → GOAL_ANCHOR → STANDING_ITEMS → four-question rule.

## Stream 2 — `Psi_local` forensics and reclassification (the finding)

Traced where the persisted `Psi_local` column is actually computed:
`Flight_6/flight6_phase4A_runner.py`, `Flight6Model.step()`, lines ~85–95; base
`EEAgent`/`EEModel` in `Flight_6/flight3_final_remediation.py` (the Flight_6 copy — a
different-lineage copy of the same name at the repo root is not the target).

**Finding:** `Psi_local = ds_a × Σ over Moore-neighbors ds_n`, averaged over cells — a signed
nearest-neighbor correlation of activation-state *changes*. It is a transition / fluctuation
/ susceptibility statistic (≈ ⟨Δx_i Δx_j⟩), **not** the sustained-state coherence order
parameter Ψ (≈ ⟨x_i x_j⟩).

- Passes the §1 "baked in" audit: it *measures* rather than *imposes* — there is no
  discretized second normal form in the substrate, so a ρ/Ψ divergence appearing here cannot
  be the assumed equation. Good for the manuscript's central defense.
- But it is the wrong object for Ψ: built on changes, it reads ≈ 0 for a stable coherent
  configuration that has stopped switching → fails the positive control.

Layer 1 (architectural) and Layer 2 (mean-field) reached this independently, with L1's read
withheld from L2 — a genuine cross-check, not a framing artifact. Layer 2's key addition is
the **density confound**: the naive fix (raw active-state co-activation) reads high from ρ
alone. So any admissible Ψ observable must be **both** state-based (survives steady state)
**and** density-adjusted (not reconstructible from ρ). `Psi_local` is reclassified as a
possible secondary susceptibility diagnostic (ties to η(t)) — not discarded.

The custodial drift, made concrete: the Phase-4B substrate-trust, schema, and adapter work
hardened around a column whose status as Ψ had never been adjudicated. Leading the resume
with the goal and gating the routing on the audit is what forced the re-examination — the
goal-anchor reorientation paying out in the same session it was written.

## Open thread (next session)

1. **Find the Q2 source** — which script computes the flights' B2(A)/B2(C) autocorrelations,
   and over which column. A keyword search (`autocorr`/`B2`/`moran`/`lag`) came back empty,
   so those terms are not in the scripts; next probe is to find the data-consuming scripts
   by searching the `.py` files for `read_parquet`.
2. **Route `L3_routing_rev4_SEND_READY.md` to Gemini** with the Flight_6-copy files attached:
   confirm/correct the §1 read in Gemini's own voice; answer **Q1** (are cell positions / a
   stable cell index persisted alongside `is_active`?) and **Q2** (is B2 computed over
   `is_active` (state, near-salvageable) or `Psi_local` (transition, shares the flaw)?); and
   if Q1 is affirmative, design the density-adjusted spatial(+temporal) autocorrelation
   observable + positive control + steady-state test as a runnable artifact.
3. **The fork (Mike arbitrates):** reframe-and-recompute the corrected observable from
   existing Flight 6 parquet (likely if Q1 is affirmative) vs. commission a new substrate.
   Turns on Q1/Q2.

## Grounding caveat

This session grounded from `GOAL_ANCHOR.md` + the two primary-source docx + persisted
memory — **not** from the full kit or the session-25 log (neither was uploaded). Memory
horizon ~Flight 2/3; the live substrate is Flight 6, past that horizon. The substrate
forensics are solid on their own terms, but the next Claude should be given the full kit +
latest log to close the gap.

## Artifacts produced this session

- `GOAL_ANCHOR.md`, `resume_sequence_for_kit.md` (goal fold)
- `defeat_baked_in.md` (discrimination spec — measurement alone can't defeat "baked in")
- `L1_audit_read_psi_local.md`, `L2_routing_can_this_be_psi.md`,
  `coherence_observable_L1_L2_synthesis.md` (the finding)
- `L3_routing_rev4_SEND_READY.md` (queued routing to Gemini)
- `INSTANTIATION_PROMPT_new_claude.md` (handoff prompt for the next Layer 1)

— Mike (drafted with Claude, Layer 1 session, 24 May 2026)
