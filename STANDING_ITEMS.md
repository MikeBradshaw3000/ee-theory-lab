# STANDING_ITEMS

**Document role.** Deferred-items tracker. Operational process artifact for items whose execution is deferred to a specific future condition. Consulted at each session open per the kit's resume-anchor discipline: a fresh Claude checks STANDING_ITEMS.md for items whose trigger conditions are met by current HEAD/working-tree state.

**Authority.** Authoritative for what is deferred and what triggers each item. Not authoritative for the items' substantive content (the operations logs, foundational current_state.md, RESTRUCTURE_INVENTORY.md remain the substantive sources). When this document's trigger condition for an item is met but the item's substantive content has evolved, the substantive sources win.

**Maintenance discipline.**
- Items added when a deferral is committed (typically in an operations log or in-session arbitration by Mike).
- Items removed when their acceptance criterion is met; the removal is committed alongside the operations log of the session in which the item executed.
- The format of each entry is fixed: **what** (the action), **trigger** (the condition under which it executes), **acceptance** (what counts as done).
- Stage-transition items have triggers expressed in terms of the preceding stage's completion, making the stage sequence operationally enforced by this document.

**Relationship to other documents.**
- `protocols/foundational/current_state.md` Section 3 names the open items at the high level; STANDING_ITEMS.md is the operational tracker with explicit trigger and acceptance criteria.
- The kit's resume anchor (kit-revision-3 onward) references this document by path; the check at session open is structural.
- `RESTRUCTURE_INVENTORY.md` is the moves-plan that Stage 2 executes against; the moves-plan is the substantive content, this document tracks the stage as one item.

---

## Items

### 6b. Repeat-seed and non-shadow-copied F-form substrate design

**What.** Specify Flight 3a-style substrate design covering both repeat-seed variance estimation and non-shadow-copied F_2_symmetric probe differentiation. Per Phase 4B v1.1 §7.2 items 1 and 5, this work is `requires_additional_probe` and `outside_phase_4b_scope`; it is substrate-generation work, not Phase 4B analytical work. Item 6b becomes load-bearing for future F-form arbitration that depends on F_2_symmetric differential behavior across probes (which the shadow-copy substrate design in Flight 2 structurally forecloses).

**Trigger.** When future F-form arbitration work requires repeat-seed variance estimation or independent F_2_symmetric probe-differential data. Independent of Phase 4B execution timeline.

**Acceptance.**
1. Substrate design specifies whether new runs produce independent F_2_symmetric data for probe2_starvation and probe3_fusion_residual (vs. shadow-copy continuation).
2. Seed replication design specified (number of seeds; matched-seed or independent-seed structure; per-condition seed budget).
3. Manifests verifying non-shadow-copy identity produced where required (per Stage 3 manifest schema discipline).
4. Variance estimates from executed runs adequate for future F-form arbitration purposes; substrate-state verification by Layer 3 before downstream use.

---

### 6c. Final Open Element 14 arbitration

**What.** Final architectural arbitration of F-form selection (F_LR vs F_2_symmetric) for Open Element 14. Per Phase 4B v1.1 §7.2 item 5, this is `outside_phase_4b_scope` — architectural arbitration is not a Phase 4B procedure. Item 6c waits for sufficient evidence from items 6a, 6b, 13, 14 to inform the arbitration.

**Trigger.** When item 6a Phase 4B characterization is complete (Layer 3 execution complete with confirmatory outputs); item 6b substrate work is in hand (if required); items 13 (Ψ-operationalization) and 14 (Q-form commitment) are sufficiently advanced if their evidence is needed for the arbitration. Mike's substantive read on readiness.

**Acceptance.**
1. Evidence basis assembled from item 6a confirmatory outputs (Phase 4B characterization findings under the interpretation_boundary discipline).
2. Evidence basis assembled from item 6b (repeat-seed / non-shadow-copied substrate findings if generated).
3. Ψ-operationalization (item 13) status documented if the final route uses Ψ-structure analysis.
4. Q-form commitment (item 14) status documented if the final route uses Q-driven base drift analysis.
5. Architectural arbitration recorded in the canonical record (operations log entry + updates to State of the Theory and v1.5 Overview as appropriate).
6. Two-field classification of the arbitration claim per Phase 4B v1.1 §6.

---

### 7. F multiplicativity commitment verification

**What.** Verify the current commitment status of F(v,c,r)'s multiplicativity property. This informs the surgical fix to v1.5 Overview's "modest-resources-outperform-abundant" passage (per project memory: Move A field-observed puzzle is fine; Move B is self-referential and contradicts the situating-not-replacing stance; the multiplicative-composition point should live in technical sections on F rather than in Move B's prose).

**Trigger.** Ungated — executable at any time at Mike's discretion. The verification and the downstream v1.5 surgical fix both run on their own schedule and are NOT gated by Phil's manuscript timeline. (Trigger corrected session 19: the prior trigger read "when v1.5 Overview revision work surfaces from Phil's manuscript timeline"; Mike had previously corrected, verbally and uncontextualized into the record, that Phil's timeline does not gate this work — the whole item, verification and fix, is ungated. The session-19 amendment lands that correction in the canonical text per the stale-trigger-hazard discipline so a fresh Layer 1 does not re-derive the wrong gate.) Independent of restructure stages; not blocking other work.

**Acceptance.** Commitment status documented (either confirmed multiplicative, or specified as one of multiple compatible forms, or specified as open). Documentation written to a substantive location (likely State of the Theory v1.1 amendment if a commitment is locked, or to operations log if status is open). Once status is documented, the v1.5 surgical fix is executable.

---

### 10. ChatGPT onboarding under session-9 framework (Gemini half closed session 19)

**What.** Produce the ChatGPT (Layer 2) onboarding document under the session-9 foundational-set framework (a compressed cold-start surface over the foundational set, analogous to the Claude instantiation kit and to the Gemini surface produced session 19). The prior-cycle primer at `protocols/onboarding/chatgpt_new_chat_primer.md` is anchored to Cycle 2 Round 1 Post-Flight-2-Closure state; substantive content has moved sufficiently since that salvaging it as still-authoritative would require substantial rewriting against current state.

**Gemini half — CLOSED session 19.** The Gemini (Layer 3) onboarding surface was produced, ran a full Layer 2 cycle (engagement → incorporation of six required revisions + Mike's "field" workstream-split arbitration → clean acceptance greenlight), and committed at `protocols/onboarding_current/gemini_onboarding_surface.md` (commit `2793373`). It supersedes the prior-cycle `protocols/onboarding/gemini_new_chat_primer.md`. A fresh Gemini instance instantiated cleanly from it during session 19 and confirmed its capability boundary. The pragmatic-path note: v2 was delivered to Gemini before the Layer 2 acceptance pass ran (out-of-sequence); the acceptance pass was then completed retroactively and returned clean, so the surface carries full review lineage.

Provenance: item 9 reconciliation Section 1.1 (in `PRIOR_CYCLE_RECONCILIATION_PLAN.md`) arbitrated this item to deferred status. The deferral is recorded in `protocols/onboarding/README.md` (the supersession marker added in the session 10 commit cluster). Session 19 closed the Gemini half when a fresh Gemini instance was needed for item 12 routing.

**Trigger (ChatGPT half).** When a fresh ChatGPT instance is needed for substantive work and the existing prior-cycle ChatGPT primer is determined inadequate as cold-start surface. (Session 18's prior-Gemini consultation experience already confirmed the prior-cycle primers materially mismatch current protocol; the ChatGPT half fires when a fresh ChatGPT chat is actually opened for substantive work.)

**Acceptance (ChatGPT half).** ChatGPT onboarding document drafted against current state — a compressed surface over the foundational set with role definitions per `protocol_primer.md`, vocabulary discipline per `vocabulary_quarantine.md`, primary-source verification discipline per `standing_rules.md`. Committed at `protocols/onboarding_current/` alongside the Gemini surface. The Gemini surface is the structural template; the ChatGPT surface adapts it to Layer 2's role (substantive analytical review, mean-field work, framing-asymmetry containment). This entry closes when the ChatGPT half is committed.

---

### 12. flight2_outputs naming resolution

**What.** Resolve the `flight2_outputs/` directory naming inconsistency. The directory at `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` is named for inheritance reasons (Flight 2 lineage in early Phase 4B work) but contains the eight Flight 6 production parquet files. The naming mismatch is documented at `canonical_artifacts_index.md` Section 5 and was previously flagged for Stage 4 resolution per Section 5's earlier text. Item 5's canonical scope (per STANDING_ITEMS at session 14 start) named only the 22 scratch scripts and the capital-B parallel tree; flight2_outputs naming resolution was not in scope. Session 14 closure surfaces this as a discovered gap requiring its own tracked life.

Provenance: discovered during session 14 Stage 4 closure when reading `canonical_artifacts_index.md` Section 5 in preparation for Stage 4 documentation updates. Session 14 ops log records the discovery and the arbitration to promote to a new tracked item rather than expand item 5's scope mid-execution.

**Trigger — MET (session 18).** Session 18's item 15 component 2 execution attempt surfaced the path+filename friction the trigger anticipated. Item 12 is session 20's Priority 1 substantive work (the keystone unblocking item 15 components 2–6). Not blocking in the sense of forbidding other work; flight2_outputs is operationally referenced by absolute path in multiple canonical scripts and the rename requires coordinated script updates.

**Acceptance.** Target directory name selected (likely `flight6_outputs/` for symmetry with the substrate specification, or another name Mike arbitrates); rename executed; canonical scripts updated to reference the new name (`inspect_tier3_provenance.py`, `merge_globals.py`, the regenerate-manifest scaffolding's hardcoded paths, the item 15 Stage 1 EDA script's `REPO_ROOT`/`DATA_FILES` constants, and any others surfaced during the rename); `canonical_artifacts_index.md` Section 5 amended to reflect the resolution; this STANDING_ITEMS entry closes.

---

### 13. Ψ operationalization commitment

**What.** Commit canonical Ψ-operationalization for analytical work. Per Layer 3 substrate-state engagement (session 15): Ψ_local is persisted at cell-tick level in current Flight 2 parquet outputs; non-spatial Ψ aggregates (mean, signed mean, magnitude-weighted, variance) are natively computable from persisted telemetry; spatial Ψ diagnostics (Moran's I, largest same-sign connected component per Phase 4B v1.1 T2.5) require Layer 3 implementation work (spatial weights matrix + graph traversal). Item 13's acceptance distinguishes three components per Layer 2 round-3 framing.

Provenance: surfaced during session 15 substrate verification on Ψ-commitment status (Select-String returned one operational mention in a Tier 1 V8 tick-0 patch context; no commitment event). Layer 2 round-2 named the deferred-but-untracked status; Layer 2 round-3 refined the three-component acceptance criteria per Layer 3 substrate findings.

**Trigger.** When Phase 4B analytical work requires Ψ-structure analysis as a substantive route (likely surfaces during item 6a Layer 3 execution if Ψ-structure is invoked, or during item 6c arbitration if Ψ evidence is load-bearing). Independent of Phase 4B v1.1 procedural Tier 1/2/3 work that uses Ψ_local without requiring committed Ψ-operationalization.

**Acceptance (three components):**
1. **Non-spatial Ψ operationalization committed.** Canonical reconstruction rule for analytical Ψ from persisted Ψ_local (e.g., system-wide signed mean, magnitude-weighted mean, or other rule per Mike's arbitration). Documented in operations log entry; if architectural commitment, also in State of the Theory amendment.
2. **Spatial Ψ diagnostics implemented and validated.** Phase 4B v1.1 T2.5 procedures (Moran's I for Psi_local; same-sign share for Psi_local; largest same-sign connected component for Psi_local) implemented per Layer 3 routing; validated against known-result test cases.
3. **T2.5 outputs generated and checked.** Phase 4B v1.1 T2.5 spatial-diagnostics CSV output (`psi_spatial_diagnostics.csv` schema) produced for all four Flight 2 production runs at the selected ticks per T2.3.

---

### 14. Q-form commitment

**What.** Commit architectural Q-form (the functional shape and dynamical role of Q in terrain reshaping). Per Layer 3 substrate-state engagement (session 15): Delta_v, Delta_u, Delta_r are persisted at cell-tick level per Phase 4B v1.1 V7; the substrate equation Δ = Γ_Q · Ψ_local makes Delta columns structurally collinear with Ψ_local scaled by Γ_Q. Q-effect decomposition (Phase 4B v1.1 §3.4, named first forward Tier 2 schema extension) is fully and natively computable. Item 14's acceptance distinguishes Delta-demand analysis (analytical work supported by current substrate without Q-form commitment) from Q-form dynamics (architectural commitment of how Q's terrain-reshaping operates structurally).

Provenance: surfaced during session 15 substrate verification on Q-commitment status (Select-String returned zero operational mentions of Q-form, Q-operator, Theta scaffold). Layer 2 round-2 named the deferred-but-untracked status; Layer 2 round-3 refined the two-component acceptance criteria per Layer 3 substrate findings.

**Trigger.** When Phase 4B analytical work requires Q-driven base drift analysis as a substantive route, or when item 6c arbitration requires Q-form evidence. Item 14 is independent of item 13 (Ψ-operationalization); the two items may advance independently.

**Acceptance (two components):**
1. **Delta-demand analysis basis documented.** Phase 4B v1.1 §3.4 Q-effect decomposition CSV (`q_effect_decomposition.csv`) implementation specified; Tier 2 analytical work covering magnitude and spatial distribution of intended terrain updates (demand for change) made available through standard Phase 4B procedures. This component does not require Q-form commitment; it operationalizes what current substrate already supports.
2. **Q-form commitment** (architectural). Decision on Q-form: what Q is functionally (committed shape, multiple compatible forms, or open); what Q does dynamically (how Δ updates restructure macro-environment over time, beyond the substrate's Δ = Γ_Q · Ψ_local formula). Documented in operations log entry and State of the Theory amendment as appropriate. Q-form commitment is the precondition for analyzing the systemic *result* of Δ updates (as distinct from the *demand* for change captured in component 1).

---

### 15. Item 6a Layer 3 execution

**What.** Execute the committed item 6a pre-registration (v2 YAML + Markdown pair) against Flight 2 canonical substrate per the Layer 3 execution routing committed session 16. Two-stage execution with binding EDA → Confirmatory checkpoint per Reading A+:

- Stage 1: EDA execution on F_LR 20×20 and F_2_symmetric 20×20 calibration data; rolling-mean ρ trajectory computation; (W, τ, Z) threshold-crossing tables; locking rule application producing calibration_locked.yaml OR escalation report (E1, E7, or any of E2-E6 triggers).
- EDA → Confirmatory checkpoint: Layer 1 + Layer 2 review of EDA outputs; Mike's arbitration; only after explicit arbitration does Stage 2 proceed.
- Stage 2: Confirmatory execution on F_LR 40×40 and F_2_symmetric 40×40 data; primary IF1 + primary IF2 + transition-proxy + cross-scale + IF5 sensitivity regressions; pre-registered sensitivity checks; Markdown report + structured CSVs per §4.5.

Pre-execution review of Layer 3 implementation scripts by Layer 1 per Phase 4B v1.1 §11 item 15 closure convention; two implementation scripts (Stage 1 EDA, Stage 2 confirmatory) as separate deliverables.

Provenance: added session 16 closure cluster. Item 6a's seven acceptance components met (per session 16 closure: components 1-5 by v2 draft pair; component 6 by Layer 2 full cycle clean v2-acceptance; component 7 by Layer 3 execution routing). Item 6a closes on component 7 wording ("Layer 3 routing in hand for execution against Flight 2 canonical substrate") per Mike's session 16 arbitration; the Layer 3 *execution* work becomes this item 15.

**Trigger.** Item 15 component 1 closed session 17 (script committed at `22aedba`). Components 2-6 active; sequencing relative to other open items at Mike's arbitration. Component 2 execution is blocked behind item 12 resolution (the path+filename friction surfaced session 18); the v3.1 defensive patch is Layer-2-accepted but not yet file-committed (content preserved in the session 18 transcript).

**Acceptance (six components mapping to the execution routing's structure):**
1. ~~**Stage 1 EDA implementation script committed** under `phase_4b/scripts/` with Layer 1 pre-execution review passed; Mike's arbitration to proceed recorded in operations log.~~ **CLOSED session 17.** Script at `phase_4b/scripts/item_6a_stage1_eda.py`; v3 after full Layer 1 + Layer 2 substantive review cycle (R1, R2a, R3, S1b in v2; R4, R5, R6 in v3); commit `22aedba`.
2. **Stage 1 EDA execution complete** with canonical outputs committed under `phase_4b/pre_registrations/item_6a_f_form_characterization/eda_outputs/`: rolling-ρ trajectories CSVs, threshold-crossing tables CSV, diagnostic visualizations, calibration report, and EITHER calibration_locked.yaml (if locked) OR escalation report (if escalated).
3. **EDA → Confirmatory checkpoint complete:** Layer 1 review of EDA outputs against v2 specification; Layer 2 review of calibration_locked.yaml (if locking succeeded); Mike's arbitration to proceed to Stage 2 OR confirm escalation.
4. **Stage 2 confirmatory implementation script committed** with Layer 1 pre-execution review passed; Mike's arbitration to proceed (if Stage 2 reached).
5. **Stage 2 confirmatory execution complete** with canonical outputs committed under `phase_4b/reports/`: Markdown report, coefficient tables CSV, marginal effects CSV, transition-proxy results CSV, cross-scale comparison CSV, IF5 sensitivity results CSV, sensitivity-clustering comparison CSV.
6. **Two-field classification populated** for primary findings per Phase 4B v1.1 §6; interpretation_boundary clauses honored throughout execution and reporting.

If at any point the escalation rule fires (any of E1-E7 triggers per Markdown Section 5 of the pre-registration), Stage 2 is suspended and a second confirmatory pre-registration is required before further confirmatory execution; item 15 acceptance criterion 5 then maps to the second pre-registration's confirmatory outputs (after its own Layer 2 full cycle and Layer 3 routing).

---

## Maintenance log

This section records when items closed or new items added. Each entry references the operations log of the session in which the change occurred.

- **Item 9 added (session 9 close).** Prior-cycle canonical material discovered via primary-source verification at session-9 close. The session 9 operations log addendum records the discovery; this STANDING_ITEMS.md update commits the trigger structure for session 10 reconciliation.
- **Item 9 closed and removed (session 10).** Three deliverables completed: `PRIOR_CYCLE_INVENTORY.md`, `PRIOR_CYCLE_RECONCILIATION_PLAN.md`, and the canonical record update commit cluster. Layer 2 sanity scan returned PASS-with-notes; patches incorporated before commit. Item 9's acceptance criteria fully met. The reconciliation cluster's operations log records the closure.
- **Item 10 added (session 10).** ChatGPT and Gemini onboarding under session-9 framework, deferred during item 9 reconciliation as out-of-scope for that item. The session 10 operations log records the deferral arbitration.
- **Item 1 closed and removed (session 10).** Item 1 execution surfaced a pipeline gap; item 1 closes via the surfacing of the gap. Item 11 added to supersede.
- **Item 11 added (session 10).** Pipeline gap: outcome-construction not wired into intake. Supersedes items 1, 2, 3 in priority. The session 10 operations log addendum documents the diagnostic trace.
- **Item 11 closed and removed (session 11).** All three sub-deliverables resolved (archaeology identified `89b85f4`'s inline outcome construction; `construct_outcome` wired into `tier3_regression.py`; re-run-and-diff coherent at analytical level). Mike arbitrated C: replace canonical outputs, document substantive-equivalence. The session 11 operations log records the closure. Items 2 and 3 become first-eligible.
- **Item 2 closed and removed (session 12).** `git push origin main` executed cleanly; `origin/main` and local `main` at parity (`b8a6833`). The session 12 operations log records the closure.
- **Item 3 closed and removed (session 12 Stage 2 cluster).** Stage 2 moves-plan executed across two commits (`919db5b`, `adfdb28`). Mechanism deviation: `git mv` replaced with `Move-Item` + `git add` (untracked sources). Item 3 acceptance met. Item 4 (Stage 3) next-eligible.
- **Item 8 closed and removed (session 12 Stage 2 cluster).** `global_timeseries.csv` disambiguation resolved by README per Mike's Arbitration 1. README at `phase_4b/tier2_outputs/README.md`.
- **Item 4 closed and removed (session 13 Stage 3 cluster).** Manifest schema and scaffolding committed (`fc9d4c4`): `parquet_manifest.md`, `parquet_manifest.csv`, `regenerate_manifest.py`. Layer 2 sanity scan conditional greenlight with four polish edits incorporated. Mike arbitrations Q1b/Q2b/B/C recorded. Item 5 (Stage 4) next-eligible.
- **Item 5 closed and removed (session 14 Stage 4 cluster).** Quarantine moves executed, 55 staged items across three groups. Discovered gap: `canonical_artifacts_index.md` Section 5 named flight2_outputs naming as a Stage 4 target outside item 5's scope. Per Mike's A+C arbitration: honest-record the gap, promote to item 12. Item 6 (Stage 5) next-eligible by trigger.
- **Item 12 added (session 14).** flight2_outputs naming resolution. Promoted to its own tracked item per Mike's A+C arbitration. The session 14 operations log records the discovery and arbitration.
- **Item 6 closed and replaced by items 6a, 6b, 6c (session 15).** Substantive arbitration on F-form route selection across three Layer 2 routings + one Layer 3 substrate engagement. Layer 3 surfaced the shadow-copy fact (F_2_symmetric byte-identical shadow copies per FSS v1.1 §13.2). Mike arbitrated full acceptance of Layer 2 round-3 framing. The session 15 operations log records the engagement in full.
- **Items 13 and 14 added (session 15).** Ψ-operationalization (item 13, three components) and Q-form commitment (item 14, two components) surfaced during session 15 substrate verification. Independent; each may advance independently.
- **Item 6a closed and removed (session 16).** All seven acceptance components met (pre-registration committed; Open Element 14 clause; shadow-copy handling corroborated by SHA-256 analysis; EDA/confirmatory distinction; substrate-supported scope restriction; Layer 2 full cycle; Layer 3 routing in hand). The Layer 3 execution work becomes item 15. The session 16 operations log records the full cycle.
- **Item 15 added (session 16).** Item 6a Layer 3 execution. Two-stage with binding EDA → Confirmatory checkpoint, six acceptance components.
- **Item 15 acceptance component 1 closed (session 17).** Stage 1 EDA script committed at `phase_4b/scripts/item_6a_stage1_eda.py`, commit `22aedba`, v3 after full Layer 1 + Layer 2 cycle (R1/R2a/R3/S1b in v2; R4/R5/R6 in v3). The no-preserved-divergence pattern recorded as genuine framing-independence. Components 2-6 active.
- **Item 12 trigger met (session 18).** Item 15 component 2 execution attempt surfaced path mismatch (script `REPO_ROOT / "flight2_outputs"` inside repo vs. substrate at parent) and filename mismatch (v3 `DATA_FILES` vs. `flight2_production.py` RUNS outputs). Substrate verified at out-of-repo location, eight files, signatures consistent with real production, "exists with uncertain authority due to incident-proximity timeframe." The session 18 operations log records substrate verification, prior-Gemini consultation, trigger identification, trust characterization.
- **Item 15 acceptance component 2 status note (session 18).** v3.1 defensive patch produced (file-existence assertion + full-condition R5 propagation through `base_evals` keying and perturbation lookup), Layer-2-accepted, not file-committed (content in session 18 transcript). Component 2 execution blocked pending item 12 resolution. The session 18 operations log records the routing arc, Layer 2's R5 retrospective, and the five-role taxonomy resolution of the Layer 3 capability category-error.
- **Item 10 Gemini half closed (session 19).** Gemini (Layer 3) onboarding surface produced, full Layer 2 cycle (engagement + six required revisions + Mike's "field" workstream-split arbitration + clean acceptance greenlight), committed at `protocols/onboarding_current/gemini_onboarding_surface.md` (commit `2793373`). Supersedes the prior-cycle `protocols/onboarding/gemini_new_chat_primer.md`. A fresh Gemini instance instantiated cleanly and confirmed its capability boundary. Item 10 narrowed to ChatGPT half only; remains open pending a fresh ChatGPT instance needed for substantive work. Pragmatic-path note: v2 delivered to Gemini before the Layer 2 acceptance pass ran (out-of-sequence); acceptance pass completed retroactively, returned clean, full review lineage intact. The session 19 operations log records the full arc.
- **Item 7 trigger corrected (session 19).** Item 7's trigger previously gated F-multiplicativity verification on "v1.5 Overview revision work surfac[ing] from Phil's manuscript timeline." Per Mike's session-19 arbitration, the whole item — verification and the downstream v1.5 surgical fix — is ungated by Phil's timeline; it is executable at any time at Mike's discretion. Mike noted this correction had been made verbally in a prior session but never landed in the canonical text; a fresh Layer 1 reading the stale trigger this session re-derived the wrong gate. The amendment lands the correction in canonical text per the stale-trigger-hazard discipline (kit-revision-5 Section 8) so the error is not re-derived again. The session 19 operations log records the correction.