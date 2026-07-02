# Operations log - 2026-07-01 - Rule E bounded-A seed: path fix, run complete, grid-count discrepancy arbitrated

**Session:** 2026-07-01 (slug 2026-07-01_rule-e-bounded-a-seed)
**Layer 1:** Claude (architectural guardian, vocabulary enforcer)
**Execution channel:** Mike (sole; all PowerShell run by Mike, Claude drafts and routes)
**Layer 2 / Layer 3:** not engaged this segment
**Entry HEAD:** 4d48e57 (bounded-A build committed pre-run, L1-reviewed)
**Exit HEAD:** this commit (path fix + run outputs + corrected spec + this ops log + anchor refresh)
**Result:** bounded-A run SEEDED AND COMPLETE - 50 runs, F3 bit-exact, constants reproduced; grid-count discrepancy (spec 90 vs as-built 50) surfaced and arbitrated to 50 (first-pass parity); cross-direction extension NAMED, NOT TRIGGERED; READ NOT YET PERFORMED

## The seed and the path bug (first attempt halted at F3; fix mirrors 3abf8dd)

Mike seeded the committed build. The first attempt HALTED LOUDLY at F3 before any data was written: ModuleNotFoundError on c3_w2_rule_c_m2. Cause: verify_f3_bypass in the bounded build inserted sys.path at cycle3, but c3_w2_rule_c_m2.py lives in cycle3/wave_two - the IDENTICAL wrong-directory bug the first pass hit and fixed at 3abf8dd. Layer 3 reintroduced it in the bounded build; Layer 1 build review missed it despite the first-pass ops log recording the exact bug and fix - Layer 1's review checked the conditioning term, guards, and constants but did not check the import path against the known fix. Owned as an L1 review hole; the seed-blocking gate caught what the review should have. The one-line fix (matching the committed first-pass form exactly: os.path.join("cycle3", "wave_two")) was applied by Layer 1, shown transparently, arbitration matching the first pass (a filesystem path with one correct value, not a mechanism choice). The parity path (cycle3, for the battery modules) was correct and untouched. Per Mike's seed-then-commit sequencing, the corrected script was placed and the seed re-run before committing; the fix commits in this bundle alongside the outputs.

## The run (complete)

The re-seed ran clean to completion:
- **F3 PASSED bit-exact:** "d=0 Rule E bounded-A reproduces committed Rule C M2 bit-exactly over a full 400-tick trajectory at (Lambda=0.4, kappa=+/-0.7599, each seed)". The seed-blocking gate satisfied at runtime.
- **Split constants REPRODUCED exactly:** Plus Anchor M_ref=0.3714 / sigma_M=0.0025; Minus Anchor M_ref=0.4187 / sigma_M=0.0017 - byte-for-byte the committed first-pass reference values (the ddof=0 parity verified in build review held).
- **Outputs:** 50 state NPZs (c3_w2_rule_e_bounded_states_*.npz), window CSV (c3_w2_rule_e_bounded_windows.csv, 114295 bytes ~ 650 rows = 50 runs x 13 windows), block CSV (c3_w2_rule_e_bounded_blocks.csv, 84109 bytes ~ 800 rows = 50 runs x 16 blocks). No traceback; seed log ends at the Phase-1 anchors because Phase 2 prints nothing by design.

## The grid-count discrepancy (surfaced at seed; arbitrated)

The output verification surfaced a spec-vs-build discrepancy: the spec (Section 5, as L2-reviewed) predeclared "9 tiers x 2 signs x 5 seeds = 90 runs"; the build ran 50. Diagnosis: the build sweeps each base sign across its OWN-direction displacement tiers only (delta_val = delta_plus if base_sign=="+" else delta_minus) - and so did the FIRST PASS, whose committed findings record "50 runs = 5 d-tiers x 5 seeds x 2 signs" and whose hygiene audits passed on 50. The "90" was a predeclared line neither pass's build matched, carried into the bounded spec by inheritance from the first-pass spec, and missed twice in L1 review (first-pass build review and bounded build review - Layer 1 did not recount the sweep loop against the stated run count either time). Owned.

**Arbitration (Mike, Option 1):** the 50-run as-built form IS the instrument. Grounds: (1) first-pass parity - "same grid, only the term bounded" is literal only at 50; (2) the classification logic (sign-local reach, bracketing along the tier axis) was written for the own-direction ladder; cross-direction cells have no predeclared reading criteria; (3) the 50-run data is internally valid and complete. The spec's Section 5 was corrected accordingly (grid-count correction recorded in the spec itself with full lineage), and the status header notes the amendment.

**Cross-direction extension - NAMED, NOT TRIGGERED (Mike-arbitrated):** the 40 cross-direction cells (positive base with negative-displacement tiers and vice versa) remain AVAILABLE as a separately named instrument. They are NOT scoped by the corrected spec: what a cross-direction cell tests, and how sign-local bracketing reads across mixed directions, requires a design resolution before any such cell is run. If ever opened, the existing 50 runs are a strict subset of the 90 (same seeds, same constants, deterministic per-run seeding), so extension means running the 40 missing cells, not discarding anything. Opening it is Mike's call only, in the lineage of the Rule D stronger-turnover extension and the (superseded-by-selection) B/C alternatives.

## Committed this bundle (one commit, per Mike's seed-then-commit sequencing)

The one-line path fix in c3_w2_rule_e_bounded.py; the run outputs (window CSV + block CSV + 50 NPZs); the corrected spec (RULE_E_BOUNDED_GAIN_IMPLEMENTATION_SPEC.md, Section 5 grid-count correction + header amendment); this ops log; and an anchor refresh (bounded-A status: RUN COMPLETE, READ PENDING).

## What remains

The READ has not been performed. The window and block CSVs are unread; no candidate classification, no guard application, no result exists yet. Next step when Mike opens it: the read against the corrected spec's six-guard classification (per-(setting, seed), block CSV as the lag-dynamics / inert-channel / saturated-channel instrument), then L2 synthesis and arbitration, then the findings bundle - mirroring the first-pass arc. Candidates will PRODUCE or FAIL TO PRODUCE; nothing here presumes the outcome. L4 untouched.

Drafting partner: Layer 1 (Claude), routed and executed by Mike.
