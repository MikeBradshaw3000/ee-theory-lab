# Two-channel ordering probe — seeding implementation spec (CANONICAL)

**Status: CANONICAL. Ratified by Mike 2026-07-05: v2 accepted as canonical; static offset SOLVED-ALWAYS as primary (the deterministic iff-rule preserving conditional u/2 is retained in Section 3 as a DOCUMENTED ALTERNATIVE only, not the operative rule). Lineage: L1 draft v1 → L2 attack (reject-as-execution-ready; all section amendments + 15 under-determined items) → L1 full-acceptance merge with two disclosed additions (exactness note; build-scope framing) → L2 fidelity pass CLEAN, both additions accepted → Mike ratification. This spec does NOT seed. Ratification opens the BUILD stage only: L3 builds → L1 build-reviews → MIKE EXECUTES, and execution is the seed, under the Section 7 bounded authorization (a separate explicit call). Governed by TWO_CHANNEL_ORDERING_PROBE_CONTRACT.md (8c94d8c) and THRESHOLDING_ADDENDUM.md (8a777e6); on any discrepancy those win.**

## 0. Scope and fences

Defines the run apparatus producing CM-1/CM-0 probe output. Defines NO read, NO classification, NO gate evaluation — G1-G4 and onset are evaluated by a later, separately specified read against the frozen addendum. The u tiers {0.10, 0.25, 0.50} are contract-fixed; nothing here retunes anything on any observable. Inherited candidate-style CSV columns are apparatus machinery, never findings. L4 untouched; Comparator 0 unreclassified; CM-2 and Rule E B/C held; no density-stability claim. The run script performs no threshold evaluation and no "above CM-0" comparison (later read only).

## 1. Frozen inputs and preflight manifest

Inputs are frozen before build and recorded in a preflight manifest. The manifest includes: contract commit 8c94d8c; thresholding addendum commit 8a777e6; the numeric Delta_rho_match = 0.00283; the committed c -> kappa map at Lambda = 0.40; canonical seeds; all committed M2 parity NPZ paths; all null-extension parity NPZ paths; and SHA-256 digests for every file consumed by preflight or parity gates.

The build consumes no probe output. Missing files, shape mismatch, digest mismatch, wrong seed list, wrong c -> kappa mapping, or a threshold/addendum mismatch fails closed before any stage writes output. The preflight manifest itself is written once and then treated as immutable by later stages.

## 2. Construction

**Update rule (CM-1):**

    p_become,i(t) = sigma( logit(p_Lambda) + u_t + kappa * (2 q_i - 1) )
    survival: stay_active with probability p_Lambda — Lambda-only, neighbor-independent, NO u_t, NO kappa

u_t enters ONLY the becoming-active branch. RNG discipline: one rand_grid per tick shared by both branches, exactly as the committed step function draws it — this is what makes the u = 0 tier bit-exact against the committed record.

**Schedule (CM-1):** frozen deterministic block-constant three-level ramp; block b carries L(b) = [0, u/2, u][b mod 3]; cycle starts at block 0; period 75 ticks; identical at every cell and across all seeds. u = 0 tier: u_t = 0 at every block (parity tier; excluded from G1 by contract).

**CM-0 rows:** the SAME code path with constant u_t = u_const for all blocks; u_const fixed by the Section 3 solve. CM-0 is a comparator only, never a driver condition; no CM-0 row may be trimmed after any output exists.

**Driven-path construction check, hard pre-data gate (L2 amendment, adopted).** Stage A u = 0 parity proves the un-driven path only. Before any nonzero-u CM-1 or CM-0 row writes output, the build must pass a deterministic driven-path construction check. On fixed diagnostic states, for each u_t in {0, u/2, u_const, u} and for kappa in {0, +0.7599, -0.7599}, the implemented becoming-active probability field must equal sigma(logit(p_Lambda) + u_t + kappa * (2q - 1)) elementwise within strict floating tolerance. The same check must assert that survival probability is exactly p_Lambda and is invariant to u_t and kappa. The check verifies BOTH the CM-1 dynamic-schedule path and the CM-0 constant-offset path. It consumes no random draw, writes no probe row, changes no threshold, and is reported in the preflight manifest. Failure halts before Stage B or Stage C.

## 3. CM-0 static-offset preflight solve (L2 replacement, adopted; solved-always)

The CM-0 static offset is a common-mode object. It is solved at kappa = 0, one selected u_const per nonzero tier, and the same selected offset is applied across all c-labels. Per-c offset solves are excluded because they would allow CM-0 to absorb differential-channel structure. The resulting c-dependent realized rho behavior is recorded and handled later by G3, not pre-erased.

For each tier u in {0.10, 0.25, 0.50}, compute the expected driven common-mode time-mean rho using the ACTUAL finite-block schedule, not a quasi-static average of independent fixed points. Use the scalar update at kappa = 0:

    rho_{t+1} = s * rho_t + (1 - rho_t) * sigma(logit(p_Lambda) + L_t),  s = 0.40

where L_t is the frozen block schedule [0, u/2, u], 25 ticks per level. Iterate to the unique 3-block periodic orbit; rho_bar_sched(u) = mean rho over that orbit. Emit the periodic-orbit trace, convergence tolerance, and rho_bar_sched(u) to the preflight log.

**Exactness note (L1 strengthening, disclosed):** at kappa = 0 the becoming-active probability is spatially constant, so this recursion is EXACT for E[rho_t] by linearity of expectation — no independence or mean-field approximation is invoked. The solve target is exact-in-expectation, not approximate.

Solve u_const(u) such that the constant-offset scalar equilibrium equals rho_bar_sched(u). **The selected CM-0 offset is the solved u_const(u), always (Mike-ratified primary rule).** The legacy u/2 gap is reported diagnostically against tol = Delta_rho_match / 2 = 0.001415, but the build does not choose between u/2 and the solved offset after inspection; no discretionary branch exists. **Documented alternative (NOT the operative rule; retained per Mike's ratification):** a deterministic iff-rule — use u/2 iff the preflight gap is <= tol, else the solved offset, no discretion — was considered and is recorded here as the admissible fallback should a future arbitration prefer it; adopting it would require Mike's explicit re-arbitration and a spec amendment, never a build-time choice. (Contract Amendment 6's conditional-u/2 permission is narrowed, not violated, by solved-always.)

Emit, before any run: all schedule-level fixed points, the finite-block periodic-orbit mean, rho*(u/2), the u/2 gap, the tolerance, the solved u_const, and the selected offset. Selected offsets are frozen into the preflight manifest and must be reused by Stage C. Recomputing or changing offsets after seeing any run output is prohibited.

## 4. Design matrix, naming, collision safety

- **CM-1:** 9 c-labels {0, ±0.05, ±0.10, ±0.20, ±0.35} (committed kappa constants) × 4 tiers (u = 0, 0.10, 0.25, 0.50) × 5 canonical seeds = **180 runs**.
- **CM-0:** 9 c-labels × 3 solved static offsets × 5 seeds = **135 runs** (Mike-arbitrated full matrix).
- **Run structure:** TICKS_PER_RUN = 400 (16 blocks; 13 windows, starts 0..300 step 25); wave-one fixed rho-0.10 initialization; committed per-run seed discipline.
- **NPZ stems:** `c3_w2_tcop_cm1_states_L0.4_k{kstr}_u{ustr}_s{seed}.npz` / `c3_w2_tcop_cm0_states_L0.4_k{kstr}_uc{ucstr}_s{seed}.npz` (committed float sanitizer). **CSV names (fixed here):** `c3_w2_tcop_blocks.csv`, `c3_w2_tcop_windows.csv`, preflight log `c3_w2_tcop_preflight.json` — same collision discipline as the NPZs.
- **Naming and collision discipline (L2 replacement, adopted):** before any stage writes output, the script generates a complete expected-output manifest for all 315 NPZs, the block CSV, the window CSV, the preflight log, and any stage manifests. The manifest includes row identifiers, intended filenames, c-label, kappa, tier, selected offset, seed, stage, and expected shape. The strings `c3_w2_rule_c_m2_states_` and `c3_w2_null_extension_states_` must not appear in any save path. No target file may already exist unless it is part of an explicitly resumed stage with matching manifest hash and file digest; otherwise, collision halts before writing. Outputs are written to temporary names and atomically promoted only after per-file shape and digest checks pass.
- **Storage:** ~90 MB NPZs + CSVs. **Runtime:** ~5-6× the committed M2 compute (window nulls dominate; the added per-block propensity diagnostics of Section 5 are minor against that); staged execution means this need not be one sitting.

## 5. Recording (L2 replacement, adopted)

**Primary state record:** each run writes a per-tick state NPZ of shape (400, 50, 50). These NPZs are the primary source for any later deterministic reconstruction.

**Block CSV:** one row per run-block, 16 per run. Required columns: run_id, mode (cm1/cm0), stage, c_label, kappa, tier, u_t, u_const where applicable, seed, block_idx, schedule_phase = block_idx mod 3, block_in_primary_set, primary_exclusion_reason, block_rho, raw Psi_meanI_state, raw Psi_persistence_I, analytic realized_delta_p_driven, mean_p_become, mean_slope, q05_slope, tail_mass, p_min, p_max, full-surface prop_I, and inactive-cell-masked prop_I diagnostic.

**Window CSV:** one row per run-window, 13 per run. Required columns: all run identifiers; window_start_tick; window_start_block; window_start_schedule_phase; window_in_primary_family; primary_exclusion_reason; window_mean_rho; raw Psi_meanI_state; raw Psi_persistence_I; z columns via the committed null machinery; SS/degeneracy flags; inherited candidate-style columns explicitly marked apparatus-only (column-metadata flag); analytic realized_delta_p_u0_convention; driven-realized-contrast summary; window schedule-level composition; and the same G2/G4 propensity summaries as block-level diagnostics where computed at window level.

The later read may reconstruct deterministic propensity fields from the NPZs, but the reconstruction convention must be the same one checked by the driven-path construction gate. Any recorded prop_I, slope, or tail-mass summaries are diagnostics; the later read decides gate pass/fail against the frozen addendum. Aggregation stays per row and seed; no parameter-level averaging substitutes for row/seed records.

## 6. Preflight, parity gates, and execution order (L2 replacement, adopted)

Execution proceeds only through predeclared stages. Every stage checks the immutable preflight manifest, script digest, selected static offsets, expected row manifest, and output-collision manifest before writing. Any mismatch halts and routes to Mike.

1. **Apparatus parity:** committed run_parity_check, unchanged, must pass.
2. **Static-offset preflight solve:** Section 3 emits and freezes the selected offsets into the manifest.
3. **Driven-path construction check:** Section 2 deterministic probability-field checks (both CM-1 schedule and CM-0 constant-offset paths) must pass before any nonzero-u row writes output.
4. **Stage A — u = 0 parity tier:** 9 c-labels × 5 seeds = 45 runs, written to staging paths first. F3-A: ticks 0-199 bit-exact against the corresponding committed M2 NPZ for all 9 c-labels and all seeds. F3-B: (u = 0, c = 0) rows bit-exact against the null-extension NPZs over all 400 ticks. Any failure invalidates Stage A outputs, halts the seed, and routes to Mike. Only passing staged outputs are promoted to final paths.
5. **Stage B — CM-1 driven tiers:** 135 runs, only after all prior gates pass.
6. **Stage C — CM-0 matrix:** 135 runs, only after all prior gates pass. B and C may be swapped or interleaved only if the manifest fixes the complete row set and no script/preflight digest changes.

Stage selection via a strict single CLI argument (whitelist: preflight, stageA, stageB, stageC). No other command-line parameters; no row filters, offset overrides, or output-dir overrides. Stages are RNG-independent because every run reseeds per the committed discipline — a claim that holds only while no stage changes code, offsets, row list, or seed list, which the digest checks enforce. Partial resumes are allowed only when existing outputs match the immutable manifest and digest checks; otherwise the stage restarts or routes to Mike.

## 7. What this spec and its build do not do; authorization

Do not evaluate G1-G4 or onset; do not tune anything on any output; do not touch committed scripts or NPZs; do not verify the 9-window earned-window rule (read-side; the run records everything that verification will later need); do not reclassify, close, move, or open anything held.

**Single authorization, bounded (L2 replacement, adopted).** Mike's explicit seed authorization may cover the staged sequence exactly as specified: preflight, Stage A, Stage B, Stage C. It does not authorize retuning, grid changes, threshold changes, static-offset changes, CLI expansion, script edits, omission of failed rows, replacement of seeds, overwrite of committed artifacts, or reinterpretation of a failed gate. Any failure of apparatus parity, static-offset manifest, driven-path construction check, collision check, Stage A F3 parity, script-digest check, row-manifest check, or stage-output digest check halts the sequence and routes back to Mike. A rerun after code, manifest, offset, or spec changes requires a fresh explicit Mike call.

## 8. Build process (L2 replacement, adopted; scope framing L1-added)

L3 builds `c3_w2_tcop.py` as a modification of committed c3_w2_rule_c_m2.py. **Honest scope framing (L1, disclosed):** the build is now two things reviewed as two things — (i) the M2-derived dynamical core, which stays minimal-diff and gets line-level review against the committed original; (ii) the staging/manifest/atomic-promotion harness, which is NEW code reviewed as new code. The minimal-diff principle governs (i); the harness is justified by the two prior implementation defects and does not get to erode (i)'s auditability.

Core constraints: no refactor; no null computation moved into the trajectory loop; one random grid draw per tick preserved; committed seed order preserved; toroidal Moore-8 neighbor logic preserved; committed null machinery retained only after trajectory generation.

L1 build-review checkpoints, minimum: exact CM-1 formula; u_t enters becoming-active branch only; survival untouched; driven-path construction check present and covering both paths; static-offset finite-block solve present; selected offsets frozen; full 315-run manifest generated; full 135 CM-0 matrix present; collision/no-overwrite checks present; script digest enforced across stages; Stage A F3-A/F3-B implemented; block 15 and non-primary windows diagnostic-only with primary_exclusion_reason populated; required block/window columns present; inherited candidate columns apparatus-only flagged; CLI whitelist exact; no threshold evaluation or classification performed by the run script.

## 9. Attack-surface register (v1 items 1-7 dispositioned; L2 additions 8-15 carried)

1. kappa = 0 one-offset convention — L2 concurred; per-c solves rejected (would let CM-0 absorb differential structure).
2. tol = Delta_rho_match/2 — retained as the diagnostic tolerance; the discretionary branch removed (solved-always).
3. Quasi-static justification — superseded by the finite-block periodic-orbit solve (exact-in-expectation at kappa = 0).
4. Driven-path construction check — required; adopted as a hard pre-data gate (Section 2).
5. Single authorization — bounded per Section 7.
6. Block 15 — diagnostic-only with primary_exclusion_reason; no default slicing may include it in primary calculations.
7. Output leaking into thresholds/constants — closed by the immutable preflight manifest, frozen offsets, and digest checks.
8. Static-offset values frozen by manifest; unchangeable between Stages B and C.
9. Driven-path check verifies both CM-1 dynamic and CM-0 constant paths.
10. Output manifests + atomic promotion prevent partial failed stages from becoming usable probe output.
11. All later-read G2/G4 quantities recorded or reconstructible without new conventions.
12. Script/preflight digest checked at every stage.
13. Block 15 / non-primary leak prevention via flags and exclusion reasons.
14. CLI/resume behavior cannot alter row set, seeds, offsets, or destinations.
15. Inherited candidate-style columns carry an explicit apparatus-only flag.
