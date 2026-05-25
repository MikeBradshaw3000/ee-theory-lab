# CYCLE 2 — Closure Record

**Closed:** 2026-05-24 (closure executed 2026-05-25)
**Closed by:** Layer 1, on Mike's arbitration. Execution channel: Mike only.
**Boundary marker:** git tag `cycle2-close` on the final closure commit.

This is a deliberate, committed closure — the boundary artifact Cycle 1 never received. Cycle 1's prior-cycle material was not reconciled at its boundary; it was *discovered* mid-Cycle-2 at session 9 (commit `53aa62e`) and repaired retrospectively under STANDING_ITEMS item 9 (closed session 10, commit `960dfdb`). The apparatus caught and fully discharged that unclean boundary — which is a recorded strength, not a failure. This closure applies item 9's own method *proactively*, at the boundary, so Cycle 3 inherits a settled record rather than a discovery.

---

## 1. What Cycle 2 produced

Cycle 2 succeeded by revealing why the inherited substrate and the `Psi_local` diagnostic could not carry the manuscript-facing claim. In brief (full account in the 2026-05-24 continuity note):

- `Psi_local` is a transition / susceptibility statistic on activation-state *changes*, not the coherence order parameter Ψ. It reads ≈ 0 for a stable coherent configuration that has stopped switching.
- An admissible Ψ observable must be state-based, density-adjusted, and able to separate persistent coherence from transient spatial organization.
- Steady-state windows are earned by explicit diagnostics, never assumed.
- Positive controls are required before any output is interpreted.
- The substrate must be built around the "baked in" defense from the start, not retrofitted from legacy telemetry.

These lessons are Cycle 3's inputs. Cycle 3 is not a repudiation of Cycle 2.

## 2. Committed Cycle 2 session record

Sessions **9–25** (handoff logs + operations logs + reviews). [^mapping]

[^mapping]: This records the *committed handoff span*, which runs session 9 (the earliest handoff on disk, and the prior-cycle-discovery point) through session 25. Note a tension to preserve, not resolve here: `PRIOR_CYCLE_RECONCILIATION_PLAN.md` §4.3 maps session 1 as the Cycle 2 Round 1 opening, which would place Cycle 2's *start* earlier than the committed handoff span. The boundary metaphysics (when Cycle 2 began) is left to Mike; this document asserts only what the repo contains.

## 3. Triage of Cycle 2 closing artifacts (item-9 method)

Three populations, each with determination and disposition as executed.

### Population A — session handoff logs and routing/synthesis notes
**Determination: still-authoritative as historical record.** Per the operations-log honest-record principle (reconciliation plan §3.2): logs are by-construction immune to content-level supersession; they record what happened on their date.
**Disposition:** committed. 31 files in commit 1 (`Cycle 2 closure (1/3)`), including the dated session logs, the Layer 3 routing and three-layer synthesis notes, `GOAL_ANCHOR.md`, `INSTANTIATION_PROMPT_new_claude.md`, `L1_audit_read_psi_local.md`, `coherence_observable_L1_L2_synthesis.md`, `defeat_baked_in.md`, and `resume_sequence_for_kit.md`. Minor in-folder redundancy (duplicate session_17/18/23 logs across dated folders) committed as-is: faithful historical record, not canonical proliferation.

### Population B — duplicated canonical artifacts inside the handoff tree
**Determination: superseded copies — deliberately NOT committed (anti-proliferation).** Nineteen files: sixteen `claude_instantiation_kit_v3/v4/v5/v5_1.md` copies, one `STANDING_ITEMS.md` copy (in `2026-05-22/`), `flight2_production.py`, and `item_6a_stage1_eda.py`. Each has a live canonical ancestor.
**The exclusion is a decision, not an oversight.** It is recorded so a future instance does not read the omission as loss. Live canonical locations:
- Instantiation kit → repo root (`claude_instantiation_kit_v4.md`, `_v5.md`, `_v5_1.md`).
- `STANDING_ITEMS.md` → repo root.
- `flight2_production.py` / `item_6a_stage1_eda.py` → their canonical script locations in the tree (verify path before any future reference; do not restore from the handoff copies).
**Disposition:** left untracked on disk. See §6 for final handling (gitignore or delete).

### Population C — phase_4b corrected-observable work
**Determination: still-authoritative as the closing state of Cycle 2's corrected-observable work.**
**Disposition:** committed. 7 files in commit 2 (`Cycle 2 closure (2/3)`): `phase_4b/scripts/psi_state_spatial_v2.py` and two output directories, `psi_state_spatial_v2_smoke/` and `psi_state_spatial_v2_smoke_patch/` (each: `sampled_timeseries_*.csv`, `window_scan_*.csv`, `synthetic_controls_summary.csv`).

#### The two smoke directories — precise relationship
`_smoke_patch` is a single-cell correction of `_smoke`. The two `synthetic_controls_summary.csv` files are byte-identical across all five control cases **except Case D** (the transient-wave divergence test):

| | `_smoke` | `_smoke_patch` |
|---|---|---|
| Case_D `Psi_persistence_I` | 1.0 | 0.0 |

For a moving wave, the expected pattern is `Psi_meanI_state` high-positive and `Psi_persistence_I` ≈ 0 (per-tick organization present; no *persistent* clustering, because the structure moves). The `_smoke` run produced `Psi_persistence_I = 1.0` — wrong for a transient. The `_smoke_patch` run produces `0.0`, restoring the expected ≈ 0. **`_smoke_patch` is operative; `_smoke` is preserved as the pre-patch record.**

#### What the control battery produced (L1/L2 only)
On the five synthetic controls (no parquet — the controls sidestep substrate trust by construction), the corrected `v2` script *produces* the designed discrimination:
- **Case A (positive control, stable cluster):** both observables high (`Psi_meanI_state ≈ 0.767`, `Psi_persistence_I ≈ 0.767`).
- **Case B (negative, random low-ρ) and Case C (negative, random high-ρ):** both observables near zero.
- **Case D (transient wave):** `Psi_meanI_state ≈ 0.706` (high) while `Psi_persistence_I = 0.0` — the two candidates *produce the designed divergence*. This is the case the continuity note flagged where the co-equal pair may genuinely diverge; the divergence is data, recorded as such, not smoothed to one reading.
- **Case E (degeneracy check, uniform high persistence):** both observables near zero — the uniform-persistence misreading is correctly flagged, not mistaken for incoherence.

## 4. Interpretation boundary

Everything in Population C is **L1/L2**: the `v2` script computes the intended state-based, density-adjusted quantities and discriminates correctly on synthetic controls. This says nothing about **L4** — what any *Flight 6* (real-substrate) value means for Regime-II-as-structural. Interpretation on the real substrate remains **withheld** (continuity note: window did not earn steady-state status; uncertain-authority parquet not reopened). The control battery is recorded here as working machinery, not as evidence for Regime-II-as-structural.

The load-bearing ontological question — which observable, if either, *is* Regime-II coherence — is carried into Cycle 3 open, to be settled by Mike / Layer 1 on coherence-as-relational-mutual-reinforcement grounds, not by statistic robustness or script naming. The two candidates remain a co-equal pair.

## 5. Apparatus-integrity note

Cycle 2's record includes the apparatus catching its own failure: the session-16 SHA-256 claim was determined a fabrication-family event (commit `61629bd`), with a formal protocol record at `protocols/architectural_reviews/2026-05-23_session_16_fabrication_family_protocol_record.md`. Preserved as evidence the protocol detects and records integrity failures rather than absorbing them silently.

## 6. Follow-ups (not done in this closure; surfaced, not buried)

1. **Population B disposition.** The 19 duplicate copies remain untracked on disk. Decide: add to `.gitignore` (preserve on disk, keep out of git) or delete (the canonical originals are tracked). A deliberate act, not part of this closure.
2. **Manuscript canonical home.** `EE_emergence_overview_v1_71.docx` and the architecture companion are committed inside `claude_session_handoffs/2026-05-24/`. v1.71 is past the v1.5 Overview the foundational set records (expected back-flow). These need a canonical home so they are not as hard to locate later as the B2 source was. Flagged for Mike.
3. **Three-folder cycle structure.** Target: top-level `cycle1/`, `cycle2/`, `cycle3/`, one per cycle. `cycle3/` exists; `cycle2/` is created by this document. `cycle1/` is **not** created here — populating it means relocating historical artifacts, a separate deliberate act.
4. **Filename typo.** `Artchitecture_companion_to_architecture_of_emergence.docx` committed faithfully with its typo. Rename later if desired; not corrected mid-closure.

## 7. Vocabulary (binding, including at closure)

ρ = activation density; Ψ = coherence; Λ = structural conduciveness (never "terrain favorability"); agents *act* (no decision/optimization/utility/cognitive language); "the point(s) at which μ(ρ) = 0" (never `ρ_c`); "per-cell active-state values" (never "field"); candidates **produce** or **fail to produce** (never "confirm"/"demonstrate"); synthesis is the work, convergence is a phenomenon that sometimes occurs.
