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

### 1. Pre-registration reproducibility verification

**What.** Re-run `phase_4b/scripts/tier3_regression.py` against the committed yaml at commit `3189ab7` (`phase_4b/pre_registrations/reg_01_scale_interactions.yaml`). Diff outputs against the committed reg_01 outputs at the same commit (primary coefficients CSV, sensitivity CSV, regression report).

**Trigger.** First substantive action of the session immediately following Stage 1 completion (i.e., when this document, kit-revision-3, and the session 9 operations log have committed). Not Stage 2 — verification before further restructure work eliminates the risk of verifying against material that has moved.

**Acceptance.** Diff output committed to the operations log of the executing session. If outputs match the committed reg_01 outputs, the registered-scope-vs-actually-ran correspondence is clean and the item closes. If outputs do not match, a gap exists; the gap is surfaced as a routed task and remains tracked under a new item that supersedes this one.

**Toolchain.** `merge_globals.py` + `inspect_tier3_provenance.py` + `tier3_regression.py` together constitute the reproducibility toolchain (per session 8 inventory). All three are at workspace root pending Stage 2 move to `phase_4b/scripts/`; the reproducibility check should reference the workspace-root paths until Stage 2 executes.

---

### 2. Push to origin

**What.** `git push` to send the local main commits to `origin/main`.

**Trigger.** Post-Stage-1 natural commit cluster. Stage 1 is complete when all foundational documents, root-level orientation documents, STANDING_ITEMS.md, kit-revision-3, and the session 9 operations log are committed. Push fires once the cluster is closed; sequencing relative to the pre-registration reproducibility verification (item 1) is at Mike's arbitration.

**Acceptance.** `git push` reports success; `git log` confirms parity with `origin/main` (HEAD on local main matches HEAD on origin/main).

---

### 3. Stage 2 execution — canonical artifact moves

**What.** Execute the `git mv` operations specified in `RESTRUCTURE_INVENTORY.md` moves-plan. Moves include: Phase 4B specification and Flight 6 substrate specification to qualified-path locations (per `protocols/foundational/canonical_artifacts_index.md` Section 11); diagnostic stdout files to `phase_4b/diagnostics/`; Tier 2, Tier 1, cross-run output directories from untracked to canonical placement; routing artifacts to routing-archive path; reclassified canonical scripts (`inspect_tier3_provenance.py`, `merge_globals.py`) to `phase_4b/scripts/`.

**Trigger.** Stage 1 complete (all items in Stage 1 closed) AND item 1 (pre-registration reproducibility verification) executed. The dependency on item 1 is per its trigger note: verification before further restructure work.

**Acceptance.** All moves-plan items executed via `git mv`; commit cluster references `RESTRUCTURE_INVENTORY.md` items; `canonical_artifacts_index.md` updated to reflect new paths; `MANIFEST.md` updated to remove "pending Stage 2" markers; this STANDING_ITEMS.md entry closes.

---

### 4. Stage 3 execution — manifests for parquet outputs

**What.** Add manifests for parquet outputs (the eight Flight 6 production files in `flight2_outputs/`) and substrate files. Manifest format combines ChatGPT's Q4 recommendation with Flight 6 Substrate Specification Section 14.1's verification structure — one canonical manifest schema serving both purposes. Located at `phase_4b/outputs/parquet_manifest.csv` with documentation at `phase_4b/outputs/parquet_manifest.md` (or equivalent locations per Stage 2 placement).

**Trigger.** Stage 2 (item 3) complete.

**Acceptance.** Manifests committed at the specified locations; manifest content covers all eight production parquet files; `canonical_artifacts_index.md` updated to reflect manifest locations and authority.

---

### 5. Stage 4 execution — quarantine stale and scratch material

**What.** Move stale and scratch material to archive locations. Quarantine targets per `RESTRUCTURE_INVENTORY.md` Stage 4: the 22 scratch scripts at workspace root; the stale parallel `EE_Theory_Lab/phase_4B/` tree (capital B at workspace parent level).

**Trigger.** Stage 3 (item 4) complete.

**Acceptance.** Quarantine moves executed; `MANIFEST.md` updated to reflect quarantine locations; the parallel `phase_4B/` tree no longer surfaces in `git status` as an untracked-or-confused parent directory; this STANDING_ITEMS.md entry closes.

---

### 6. Stage 5 transition — next analytical phase

**What.** Decide which macro-level F-form adjudication route (aggregate trajectory comparisons, Ψ-structure analysis, Q-driven base drift, regime-transition timing, repeat-seed designs) becomes the next pre-registered analytical work. Specify the pre-registration. Route to Layer 2 for full cycle. Once pre-registered, route to Layer 3 (Gemini) for execution against canonical substrate data.

**Trigger.** Stage 4 (item 5) complete; restructure cluster fully landed.

**Acceptance.** Architectural decision arbitrated by Mike; new pre-registration committed under `phase_4b/pre_registrations/`; Layer 2 full cycle complete on the pre-registration; Layer 3 routing in hand.

---

### 7. F multiplicativity commitment verification

**What.** Verify the current commitment status of F(v,c,r)'s multiplicativity property. This is a precondition for the surgical fix to v1.5 Overview's "modest-resources-outperform-abundant" passage (per project memory: Move A field-observed puzzle is fine; Move B is self-referential and contradicts the situating-not-replacing stance; the multiplicative-composition point should live in technical sections on F rather than in Move B's prose).

**Trigger.** When v1.5 Overview revision work surfaces from Phil's manuscript timeline. Independent of restructure stages; not blocking other work.

**Acceptance.** Commitment status documented (either confirmed multiplicative, or specified as one of multiple compatible forms, or specified as open). Documentation written to a substantive location (likely State of the Theory v1.1 amendment if a commitment is locked, or to operations log if status is open). When status is documented, the v1.5 surgical fix becomes executable on Phil's timeline.

---

### 8. `global_timeseries.csv` rename-or-README decision

**What.** Decide whether to rename `phase_4b/tier2_outputs/global_timeseries.csv` to a name that disambiguates it from the per-probe-scale `global_timeseries_*.csv` files, or to add a README in `phase_4b/tier2_outputs/` documenting the file's role as the merged Tier 2 → Tier 3 bridging artifact. Canonical status of the file was settled during session 8 Stage 0 inventory; the disambiguating-documentation choice is pending.

**Trigger.** Stage 2 (item 3) execution. The rename or README addition happens during Stage 2, not after, because Stage 2 is when canonical artifact placement is settled.

**Acceptance.** Either rename executed via `git mv`, or README added at `phase_4b/tier2_outputs/README.md`. `canonical_artifacts_index.md` Section 5 updated to reflect the chosen disambiguation.

---

## Maintenance log

This section records when items closed or new items added. Each entry references the operations log of the session in which the change occurred.

*(Empty as of session 9 commit; entries added as items execute.)*

---

— Drafted by Claude as Layer 1 central node, Stage 1 root-level operational process artifact, session 9. No Layer 2 routing per the agreed sanity-scan-distribution convention (operational process artifact, not architectural deliverable). Ready for commit.
