# Gate B v0.4 Canonical Joint Forecast Record — Pre-Freeze Requirement Discharged
**Produced:** 2026-08-27, Mike's machine, canonical environment. **Runner:** `forecast_v04.py`, sha256-16 `35CCDDE3BC4CF926` (full: `35ccdde3bc4cf926cea2eda571c788a84da25c4ed28a715df59f067804f0c9fe`) — digest-identical to the runner whose provisional output L2 reviewed in packet 4. Pinned source digest verified in-run. Reference-only: forecast pool 401–600, disjoint from calibration (101–120) and both certification pools (201–220, 301–320). No candidate output exists.

## Output (verbatim as returned)
```
GATE B v0.4 REPAIRED JOINT FORECAST  [CANONICAL]
python 3.14.4  numpy 2.4.4  pinned sha256 466455f20550b8c4...  analysis_seed 0x7A9B31C
no-tie reduction check: P(D_int>=12 | all-singleton blocks) = 0.0011158 (expect 0.0011158)
R=4000 pseudo-experiments (integer counts):
  TOST all-8 pass:   4000/4000
  KS no-alarm:       3977/4000   (total alarms 50; experiments with any tie block 3759)
  FULL-GATE pass:    3977/4000  = 0.9942
power vs 0.005 (worst-sd cell): 4000/4000 fail
End of repaired forecast record.
```

## Reproducibility fields (Amendment 6R mandatory set)
Runner digest as above; analysis RNG NumPy `default_rng(0x7A9B31C)` (PCG64); panel algorithm `choice(200, 40, replace=False)`, first 20 candidate-role, last 20 reference-role, same panel across all eight cells (cross-cell dependence preserved); Welch TOST per Amendment 3 (δ=0.003, α_cell=0.05/8); gross-divergence screen per Amendment 4R (tie-invariant ECDF D_int; exact conditional permutation null given tie blocks; alarm iff p ≤ 0.00125); integer counts as printed; environment python 3.14.4 / numpy 2.4.4; pinned `c3_w2_tcop.py` at `4d9a622` verified in-run.

## Disposition
Every integer matches the provisional record exactly — cross-environment determinism holds through the pinned rule, panel sampling, and the conditional-permutation DP. The Amendment-6R canonical-rerun requirement is **discharged**; this record, not the provisional one, supports the freeze decision. Remaining pre-freeze obligations are the downstream implementation set (wrapper source review and ten-run bit-identity record; 30-mutant qualification with attribution; solved-offset enumeration; FP-witness uint64 patterns), plus L2's packet-4 verdict and Mike's freeze word.
