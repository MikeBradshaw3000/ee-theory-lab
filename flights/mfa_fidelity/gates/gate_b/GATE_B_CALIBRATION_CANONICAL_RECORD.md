# Gate B v0.2 §4 Pre-Freeze Calibration — CANONICAL Record
**Produced:** 2026-08-25, Mike's machine, canonical environment (python 3.14.4, numpy 2.4.4), runner `gate_b_calibration.py` (content verified statement-identical to L1 master by read-back and by deterministic output identity across environments). Pinned source digest verified in-run: `466455f2…b7e7`. Reference-only; calibration pool 101–120; no candidate output exists.

## Output (verbatim as returned)
```
GATE B v0.2 PRE-FREEZE CALIBRATION RECORD  [CANONICAL]
python 3.14.4  numpy 2.4.4  pinned sha256 466455f20550b8c41a984ce40db49ebe0e832ae56c269ab518b521c6ad83b7e7
seeds: calibration pool 101-120 (reference-only)
mode  drive    kappa |  mean_term   sd_term sd<=0.0054 | max_sd_blk
 cm0    0.0  +0.0000 |   0.399887  0.001441       True |   0.002630
 cm0   0.25  +0.0000 |   0.434548  0.001479       True |   0.002300
 cm0    0.0  +0.4221 |   0.386162  0.001841       True |   0.003072
 cm0    0.0  -0.4221 |   0.410937  0.001287       True |   0.002166
 cm0   0.25  +0.4221 |   0.426456  0.001723       True |   0.002755
 cm0   0.25  -0.4221 |   0.441252  0.001249       True |   0.001961
 cm1   0.25  +0.4221 |   0.401842  0.001811       True |   0.003071
 cm1   0.25  -0.4221 |   0.422706  0.001233       True |   0.002145
feasibility (all cells sd<=0.0054): True
split-half |mean diff| (equivalent-vs-equivalent, 10v10):
  cm0 (0.0,+0.0000): 0.000916
  cm0 (0.25,+0.0000): 0.000877
  cm0 (0.0,+0.4221): 0.001064
  cm0 (0.0,-0.4221): 0.000736
  cm0 (0.25,+0.4221): 0.001118
  cm0 (0.25,-0.4221): 0.000775
  cm1 (0.25,+0.4221): 0.000915
  cm1 (0.25,-0.4221): 0.000745
End of calibration record.
```

## Disposition
Cross-environment identity: every printed value matches the L1 container record exactly (deterministic legacy MT19937 under numpy 2.4.4). §4 feasibility bound satisfied in all 8 cells; variance reproduction well within the declared 2× qualification factor (exact). The spec's pre-freeze calibration requirement is discharged; the CM-1 gap flagged in packet-2 Part IV is closed. Comparator/acceptance-grammar freeze remains gated on L2's v0.2 verification return and Mike's freeze word.
