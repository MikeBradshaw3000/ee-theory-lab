# OBS001_14 - Layer 3 apparatus-level interpretation

Source: Layer 3 (Gemini), responding verbatim to OBS001_13. Apparatus-level interpretation only; no L4 reading produced.

---

Message received and locked. Here is the apparatus-level interpretation of the pasted CSV outputs for the Wave One (A+B) sweep, strictly observing the framing and vocabulary disciplines.

### 1. Per-Rule, Per-Lambda Summary

**Rule A (Strict Lower Threshold)**

* **$\tau_A \in \{1, 2, 3\}$:** The run produced uniform saturation. On all 5 seeds, activation density (`mean_rho`) drove toward 1.0. The apparatus recorded `saturation_degenerate` as `True`. For $\tau_A=1$ and $2$, saturation occurred rapidly (`Tick_to_Freeze` < 10). For $\tau_A=3$, saturation took longer (`Tick_to_Freeze` 41-57), resulting in early windows failing `Steady_State_Candidate` before stabilizing at 1.0.
* **$\tau_A \in \{4, 5, 6, 7, 8\}$:** The run produced immediate extinction. On all 5 seeds across all 5 values, `mean_rho` dropped below the 0.05 threshold immediately (`Tick_to_Zero` $\le$ 4). The apparatus recorded `extinction_degenerate` as `True` and `Lifted_Activation_Candidate` as `False`.

**Rule B (Range-Bound / Life-Like)**

* **Band [1,2]:** The run produced earned lifted steady-state windows. On 5/5 seeds, the system stabilized at `mean_rho` $\approx 0.326$. In these windows, the apparatus recorded a divergent signature: high per-tick spatial organization (`Psi_meanI_state_z` $\approx 195$) and low/negative persistence (`Psi_persistence_I_z` $\approx -15$).
* **Band [2,3]:** The run produced earned lifted steady-state windows. On 5/5 seeds, the system stabilized at `mean_rho` $\approx 0.385$. In these windows, the apparatus recorded a divergent signature: high per-tick spatial organization (`Psi_meanI_state_z` $\approx 145$) and low/negative persistence (`Psi_persistence_I_z` $\approx -8$).
* **Band [2,4]:** The run produced earned lifted steady-state windows. On 5/5 seeds, the system stabilized at `mean_rho` $\approx 0.466$. In these windows, the apparatus recorded a divergent signature: high per-tick spatial organization (`Psi_meanI_state_z` $\approx 240$) and low/negative persistence (`Psi_persistence_I_z` $\approx -4$).
* **Band [3,4]:** The run produced zero earned lifted steady-state windows. The apparatus recorded `Steady_State_Candidate` as `False` across 4 seeds due to persistent upward drift (failing the `relative_drift` and `rho_range_over_mean` thresholds), and the 5th seed (31415) triggered `extinction_degenerate`.

### 2. Comparison Against Design v2 Expectations

* **Sweep A (Expected: Non-discriminating baseline):** The run produced the expected non-discriminating behavior. On 5/5 seeds across all 8 parameters, the apparatus recorded zero instances of a divergent joint signature and zero instances of a `LowLow_Nondegenerate_Candidate` signature. The Rule A meaningful-failure criterion was not triggered.
* **Sweep B [2,4] (Expected to be tested for `LowLow_Nondegenerate_Candidate`):** The run produced an unexpected outcome for this specific parameter. Instead of the low/low non-degenerate signature, 5/5 seeds produced the divergent signature (high `Psi_meanI_state` / low `Psi_persistence_I`).
* **Sweep B [2,3] (Expected to be tested for the divergent signature):** The run produced the expected outcome. On 5/5 seeds, earned steady-state windows with lifted activation recorded the divergent signature.
* **Sweep B [1,2] & [3,4] (Expected to serve as boundary cases):** The run produced boundary behavior for [3,4] (failure to earn steady-state), but [1,2] behaved identically to the core active bands, producing a clear divergent signature rather than extinction or saturation.

### 3. 3/5 and 4/5 Patterns

The apparatus recorded a distinct 4/5 pattern in Sweep B, Band [3,4]. While the meaningful-failure threshold is strictly 5/5, 4 out of 5 seeds experienced a slow, sustained upward drift in `mean_rho` that failed to settle into an earned steady-state window within the 200-tick run length. The 1 remaining seed (31415) dropped to a near-zero trivial baseline.

### 4. Substrate Dynamics Observed Across Rule A

The substrate adjudicated the Rule A regime locations definitively under the locked topology:

* **Uniform Saturation:** The substrate placed this regime exclusively at $\tau_A \in \{1, 2, 3\}$.
* **Immediate Extinction:** The substrate placed this regime exclusively at $\tau_A \in \{4, 5, 6, 7, 8\}$.
* **Locked Clusters:** The hypothesized intermediate regime was not produced at any $\tau_A$ value in this sweep. The substrate transitioned directly from uniform saturation at $\tau_A=3$ to extinction at $\tau_A=4$.

### 5. LowLow_Nondegenerate_Candidate Across the Full Sweep

The `LowLow_Nondegenerate_Candidate` flag fired `False` for every single row in the dataset (300 out of 300 candidate windows).

* **In Rule A:** The flag was blocked by degeneracy. Every window triggered either `saturation_degenerate` = `True` or `extinction_degenerate` = `True`.
* **In Rule B:** The flag was blocked by massive per-tick spatial organization. In the earned lifted steady-state windows (Bands [1,2], [2,3], and [2,4]), `extinction_degenerate` and `saturation_degenerate` correctly read `False`, but the `Psi_meanI_state_z` values ranged from $140$ to $250$. This heavily violated the structural requirement that the `Psi_meanI_state_z` score remain below the "low" threshold (|z| < 2.0).
