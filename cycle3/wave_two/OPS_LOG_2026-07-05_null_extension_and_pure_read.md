# Ops log — 2026-07-04/05: null-extension run + threshold-fixing pure read (contract step 1 → addendum)

**Session scope:** everything from the contract placement (8c94d8c) forward: the null-extension run ("initiate 1"), then the threshold-fixing pure read and its addendum. Committed in TWO commits (null-extension arc; thresholding arc), this log closing the second. The probe remains UNSEEDED throughout; nothing here opened seeding.

## Arc 1 — null-extension run (Mike: "Initiate 1")

1. Grounded against committed `c3_w2_rule_c_m2.py` (read in full). Confirmed parity holds by construction: the trajectory loop draws one rand block/tick with no null-permutation draws interleaved (nulls run after trajectory generation), so ticks 0-199 are draw-identical at TICKS_PER_RUN=400.
2. Build spec (option a: minimal diff, block stats deferred to the pure read). L2 attack: accept-with-amendments (4) — "two logic changes + one mechanical safety edit" wording; collision-halt on output stem; F3 helper kept outside the run script; inherited results-CSV fenced as apparatus sanity surface (LowLow_Nondegenerate_Candidate is inherited machinery, not a finding). All folded.
3. L3 built `c3_w2_null_extension.py` (copy of committed M2, three edits: TICKS_PER_RUN→400, sweeps→[(0.40,[(0.00,0.0000)])], output stems → c3_w2_null_extension_*). L1 build-review PASS (6 checkpoints; the load-bearing one — no null draw leaked into the trajectory loop — confirmed).
4. Run clean (no output = success signature). Outputs: 5 NPZs (~284 KB each, 400-tick) + 1 CSV. F3 gate (standalone helper, run then deleted before staging): bit-exact 5/5 seeds — the 400-tick floor family is a valid extension of the committed record.

**Arc-1 committed artifacts:** `cycle3/wave_two/c3_w2_null_extension.py`; `cycle3/data_out/c3_w2_null_extension_states_L0.4_kp0_0000_s{42,137,256,1024,31415}.npz`; `cycle3/data_out/c3_w2_null_extension_results.csv`.

## Arc 2 — threshold-fixing pure read (Mike: "pure read")

1. Forks arbitrated: Fork A → option iii (coarse 15-point pooled null, conservative max threshold — honoring the degenerate 3-alignment phase null); Fork B → concur (input manifest verified: all Λ=0.40 M2 responsive NPZs present, ±0.35/±0.20 both signs).
2. Read spec v1 → L2 attack (reject-as-execution-ready; 8 emission verdicts, 13 under-determined items). L1 accepted all; the significant owned miss was G1 emitting only correlation, dropping the amplitude threshold (the exact side door closed at contract stage, reopened one layer down). L1's one contest (3.7 operative floor) WITHDRAWN with ground (contract Section 7 conditions the setting-level flag on 9-window verification, not yet done → max-observed default correct). Spec v2 → L2 fidelity pass CLEAN.
3. Post-fidelity clarification: the per-cell time-shuffle control is algebraically invariant for persistence (a permutation cannot change a time-mean). L1-discovered, L2-concurred: axis-specific onset controls — time-shuffle for meanI, spatial-permutation for persistence. Spec v2.1.
4. Read script v1 executed. **Implementation defect 1:** G3 Δρ_match = 4e-5, caught by contradiction with the feasibility audit (cap min-ed over cross-c matched-rho TARGETS). L2-arbitrated defect repair (not threshold tuning): discriminating-set cap rule. v2 rerun (same frozen seed) — repair-isolation audit PASS, all non-3.4 emissions bit-identical, Δρ_match → 0.00283.
5. **Implementation defect 2:** onset meanI control used argsort(axis=1) (per-tick spatial, the committed z-convention) not the spec's per-cell time shuffle (axis=0). Caught by L2's invariance hardening clause (demonstration returned False, impossible under the labeled control). Axis fix consumes no RNG. v3 rerun — granular repair-isolation audit PASS (meanI raw + both persistence series + repair-1's g3 all bit-identical; only meanI residue changed; invariance demonstration True).
6. Valid v3 results frozen. Addendum authored from the v3 JSON. L2 fidelity pass on the addendum CLEAN (transcription, lineage, no-overreach all confirmed; v3 meanI residue correctly used, not the invalid v2 value).

**Frozen thresholds (addendum §2):** G1 r>0.7840 & slope>0.002628; G1b var>4.47e-6; G2 +0.3832/−0.3814; G3 Δρ_match=0.00283, N_bin_min=9, S_bin_min=3; G4 mean_slope≥0.2256, q05≥0.19884, tail≤0, [0.05,0.95]; onset meanI raw 0.00199/res 0.002113, persistence raw 0.02284/res 0.02311 (max-observed operative); feasibility OVERALL feasible.

**Validation of record:** the reconstructed G2 floors (0.3832/0.3814) independently reproduce the committed ~+0.38 anchor both signs — end-to-end validation of the propensity-reconstruction apparatus.

**Arc-2 committed artifacts:** `threshold_fixing_read.py` (v3, repo root — reproducible provenance of the frozen thresholds); `cycle3/data_out/threshold_fixing_read_results.json` (valid v3); `cycle3/data_out/threshold_fixing_read_results_INVALID_v1.json` and `_INVALID_v2.json` (audit-lineage record — proof the repairs were isolated); `cycle3/wave_two/THRESHOLD_FIXING_READ_SPEC_v2_1.md`; `cycle3/wave_two/THRESHOLDING_ADDENDUM.md`; this ops log.

## Process notes

- Two implementation defects, each caught by a discipline artifact (feasibility/Δ contradiction; L2 invariance hardening), each proven isolated by a built-in audit against the preserved prior JSON. The read spec's own machinery worked as designed.
- Two repairs disposed as defect-repair-not-threshold-tuning, both on the same ground: same frozen READ_RNG_SEED, deterministic-only changes, bit-identical reproduction of all non-target emissions — audit-proven, not asserted.
- F3 helper and any pure-read helper: run then deleted before staging (helper discipline).
- Render/download channel intermittent failures resolved via fresh unique transit filenames (standing pattern). Copy-Item silent failure (file lock) resolved with explicit error capture.
- All git operations Mike-executed; L1 drafted and routed only. Explicit-path staging; byte-state verification at destination; short single-line commit messages; two commits (null-extension arc, then thresholding arc).

## State at close

- Contract: CANONICAL (8c94d8c), now completed by the thresholding addendum.
- Null-extension run: DONE, F3-validated.
- Threshold-fixing pure read: DONE; thresholds frozen; design certified FEASIBLE / seedable.
- **Probe: UNSEEDED.** Seeding opens only on Mike's separate explicit call; nothing in this arc opened it.
- Named open item: the 9-window earned-window rule is NOT yet verified (operative onset floor is max-observed until it is).
- Held/untouched: CM-2; Rule E B/C; L4; Comparator 0 unreclassified; no mechanism class moved; no density-stability claim.
