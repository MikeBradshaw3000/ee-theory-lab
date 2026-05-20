# Tier 1 Verification Report: flight6_probe2_starvation_FLR_40x40.parquet
Verdict: **PASS**

- V1_Drive_Decomp_Fails: 0
- V2_Term_Lambda_Fails: 0
- V3_Density_Fails: 0
- V4_Probability_Fails: 0
- V5_Realization_Fails: 0
- V6_F_Form_Fails: 0
- V7_Q_Diagonal_Fails: 0
- V8_Discipline_Fails: 0

## Tick 0 Psi Observability Note

Tick 0 Psi_local reconstruction skipped for V8: substrate computes tick-0 Psi from the
transition between the initial activation state held in state_history (deque-stored,
not persisted) and the post-step tick-0 state. The initial pre-step state is not
persisted in parquet, so tick-0 Psi cannot be reconstructed from persisted is_active
alone. V8 Psi reconstruction verifies ticks 1-2999. Tick-0 Psi remains a valid substrate
output for Tier 2 descriptive analysis, with this observability caveat.

ds inferred from is_active(t) - is_active(t-1) for t >= 1.
