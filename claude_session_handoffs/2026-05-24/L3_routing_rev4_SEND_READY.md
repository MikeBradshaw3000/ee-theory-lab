# Layer 3 Routing (rev 4, send-ready) — Confirm the `Psi_local` read, answer Q1/Q2, design the corrected coherence observable

**From:** Layer 1 (Claude, central node), on Mike's behalf.
**To:** Layer 3 (Gemini) — bounded design + analysis pass, code-and-design, zero execution.
**Type:** Scoping design pass. Not an execution request. Mike is the sole execution channel. This supersedes rev 3: the §1 audit has been substantially answered, so the task is now narrower and downstream of it.

**Why this supersedes rev 3.** The `Psi_local` computation was located and read by Layer 1 (architectural) and Layer 2 (mean-field), independently. Both conclude: `Psi_local` = mean over cells of (ds_a × Σ-over-neighbors ds_n), where ds = activation-state change — i.e. a signed nearest-neighbor correlation of activation *changes*, a transition/susceptibility statistic, **not** the sustained-state coherence order parameter Ψ. It does not bake in the second normal form (it passes the a/b/c gate), but it avoids doing so by measuring a different object. rev 3's "compute the aggregate over `Psi_local`" is therefore the wrong next step. This pass confirms that read against the code, settles two substrate facts, and designs the corrected observable.

## §0 — Gate (restate on return)
Reconfirm: (1) capability boundary — you write code/designs and analyze pasted outputs; you do not execute against the substrate, assert file existence/contents, read the local filesystem, or choose canonical copies; (2) instance/mode state; (3) inputs-on-hand — you design against the facts in §1–§3 and the code Mike supplies, not independent inspection or conversational-memory recall of prior scripts.

## §1 — Files supplied with this routing (audit the supplied code; do not recall from memory)
The following are supplied. If any is missing, stop and request it; do not infer from persisted columns or from prior-session memory (stale-source discipline — the same gate you correctly invoked before).
- `Flight_6/flight6_phase4A_runner.py` — the `Flight6Model(f3.EEModel)` override; contains the `local_psi` computation (~lines 85–95) and the telemetry-record assembly (~line 140).
- `Flight_6/flight3_final_remediation.py` — the **Flight 6 copy** (`EEAgent`/`EEModel`), base activation dynamics. NOTE: a different file of the same name at the repo root defines `EcosystemAgent`/`EcosystemModel` (different lineage, different hash) — that is **not** the audit target; do not use it.
- The analysis script that computes the flight catalog's B2(A) and B2(C) autocorrelations (for Q2 below) — supply the actual current file, not a recalled version.

## §2 — Confirm or correct the read (your formal §1 deliverable, on the located code)
Read the supplied `local_psi` computation directly and return your own audit call — passes / fails / ambiguous against the three disqualifiers (a: takes ρ/aggregate density as input; b: density-keyed sign-changing coefficient; c: hard neighbor-count threshold vs. continuous neighbor-weighted accumulation) — and your own characterization of what the statistic is. Do not defer to the Layer 1/Layer 2 read; confirm or correct it. This is the discrimination that carries the most weight, so read it, do not infer it.

## §3 — Two substrate facts to settle
- **Q1 (positions).** Are cell positions — or a stable cell index that maps to grid coordinates — persisted alongside `is_active` in the Flight 6 parquet? Answer from the telemetry-record assembly in the supplied runner (the block that builds each persisted row), naming the exact columns. This determines whether a spatial autocorrelation observable is computable from the existing telemetry without a new run.
- **Q2 (B2 input).** What per-cell column do the flights' B2(A)/B2(C) autocorrelations read as input — `is_active` (sustained state) or `Psi_local` (transition)? Answer from the supplied analysis script, naming the column. If B2 reads the state, the catalog may already be close to the right object; if it reads `Psi_local`, it inherits the transition-correlation flaw.

## §4 — Design the corrected coherence observable (gated on Q1)
The admissible Ψ observable must thread two failure directions: it must be **state-based** (survive steady state — a change-based measure reads ≈ 0 once switching stops) AND **density-adjusted** (not reconstructible from ρ — a raw co-activation measure reads high from density alone, the ρ-redundancy/B1 failure).

Requirements:
1. Built on the per-cell active-state values x_i ∈ {0,1}, not the activation-change values Δx_i.
2. Density-adjusted (organization beyond what ρ predicts).
3. Persistence-weighted (candidate): co-activation that persists over a window, so transient clusters do not read as coherence.
4. Passes the positive control (§5).

Candidate families (from Layer 2; minimal admissible, NOT committed — propose the form, do not fix it):
- A — centered spatial autocorrelation ⟨(x_i−ρ)(x_j−ρ)⟩ over neighbors.
- B — density-adjusted co-activation M(t) − ρ².
- C — A or B weighted by temporal persistence over a window W.
These map onto B2(A) (spatial) and B2(C) (temporal, lag τ); the right observable plausibly lives in that space, density-adjusted.

Deliver, conditioned on Q1:
- **If Q1 is affirmative:** the exact column operations to compute the corrected observable from the **existing** Flight 6 parquet (`is_active` + positions), as a runnable artifact for Mike — no new run.
- **If Q1 is negative:** state the minimal additional persistence a new run would need (what to record, at what resolution) to make the corrected observable computable, as a runnable artifact for Mike.

## §5 — Discrimination (pessimistic-on-passing)
The corrected observable must be shown to discriminate, not merely to produce a number. State and test:
- **Positive control:** a stable mutually-reinforcing active cluster reads high; a random configuration at the same ρ reads ≈ 0; a high-ρ unstructured configuration does NOT read high; a transient synchronized-switching wave does NOT read as persistent Ψ.
- **Steady state:** the Regime-II signature (ρ lifted, Ψ ≈ 0) and the Regime-III signature (ρ lifted, Ψ high) must be persistent at steady state, not transient.
- **Not ρ-redundant:** the observable must separate from ρ — a divergence between ρ and the observable that survives density adjustment.

## §6 — Boundaries
- Vocabulary: ρ = activation density; Ψ = coherence; Λ = structural conduciveness (NOT "terrain favorability"). Use "per-cell active-state values" / "active-state configuration," not "field." Agents *act*; no decision/optimization/utility/cognitive language. Do not introduce `ρ_c`; the committed formulation is "the point(s) at which μ(ρ) = 0."
- Design pass. Any "run/execute" means "prepare the runnable artifact for Mike."
- Strategic adequacy — whether the corrected observable defeats "baked in" to a reviewer, and the reframe-vs-new-substrate commit — is NOT a Layer 3 question; it returns to Layer 1 / Mike / the manuscript. Stay on the audit-confirm, the two facts, and the observable design.
