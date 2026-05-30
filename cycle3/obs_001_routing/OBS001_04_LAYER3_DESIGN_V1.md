# OBS001_04 - Layer 3 v1 design menu (A + B)

Source: Layer 3 (Gemini), responding verbatim to OBS001_03.

---

Message received and locked. Layer 3 is oriented to the Cycle 3 context and the strict constraints of this wave-one design contract.

I acknowledge that this is a design menu, not a code-production contract. No execution has occurred. The expectations outlined below describe what the design specifies, subject entirely to Layer 1 implementation review and Layer 2 substantive review.

Here are the eight design deliverables for wave one (A + B).

### 5.1 Local-rule specification

Both rules operate on the locked 50 x 50 toroidal grid, evaluating the Moore radius 1 (8-neighbor) active-neighbor count for each cell at tick $t$ to determine how the agent acts at tick $t+1$.

* **Initial Condition (Both Rules):** The grid is seeded at $t=0$ by assigning per-cell active-state values (1 for active, 0 for inactive) uniformly at random to achieve a target starting rho (e.g., 0.10).
* **Rule A (Strict Lower Threshold):** An agent acts (becomes or remains active) at $t+1$ if the count of active neighbors at $t$ is $\ge \tau_A$. If the count is $< \tau_A$, the agent deactivates. The rule has no upper bound.
* **Rule B (Range-bound / Life-like):** An agent acts (becomes or remains active) at $t+1$ strictly if the count of active neighbors at $t$ falls within a closed interval $[\tau_{B, min}, \tau_{B, max}]$. If the count is below $\tau_{B, min}$ or above $\tau_{B, max}$, the agent deactivates.

### 5.2 Lambda-like parameter for each rule

The structural conduciveness parameter, Lambda, is designed to map to the micro-rule thresholds. This mapping specifies how varying structural conduciveness is expected to alter the thresholds for agent action.

* **Rule A ($\Lambda_A$):** Maps inversely to the strict lower threshold $\tau_A$. Higher structural conduciveness corresponds to a lower active-neighbor count required to act. The design specifies varying $\tau_A$ across the integer range $\{1, 2, 3, 4\}$.
* **Rule B ($\Lambda_B$):** Maps to the position and width of the survival/activation band. Higher structural conduciveness lowers the floor of the band or widens it. To ensure the rule remains strictly range-bound and capable of forcing sustained motion, the design specifies shifting a narrow band across the neighborhood space: e.g., $[\tau_{B, min}, \tau_{B, max}] \in \{[1,2], [2,3], [3,4], [2,4]\}$.

### 5.3 Telemetry schema

The design specifies recording the following quantities to support the C3-CTL-001 and C3-SS-001 evaluation machinery:

* **Per-tick records:**
  * rho(t) (scalar mean of per-cell active-state values).
  * The complete $50 \times 50$ matrix of per-cell active-state values.

* **Per-window records (100-tick windows, 25-tick sliding step):**
  * Psi_meanI_state (per-tick spatial organization, averaged over the window) and its grid-local permutation null z-score.
  * Psi_persistence_I (spatial organization of the time-averaged persistence map) and its grid-local permutation null z-score.
  * The four SS-001 diagnostics: `relative_drift`, `rho_cv`, `rho_range_over_mean`, and `mean_rho`.
  * The two independent SS-001 flags: `Steady_State_Candidate` (evaluating against the 0.10, 0.10, 0.25 thresholds) and `Lifted_Activation_Candidate` (evaluating against the 0.05 threshold).

* **Rule-specific diagnostics (Per-run):**
  * `Tick_to_Freeze`: The tick index at which $\Delta \text{states} = 0$ for 10 consecutive ticks (designed to catch Rule A locking into static clusters).
  * `Tick_to_Zero`: The tick index at which rho(t) precisely equals 0.0.

* **Storage:** Per-tick active-state matrices stored in Parquet or compressed NPZ; windowed telemetry and diagnostics stored in a flat CSV, one row per (Lambda, Seed, Window_Start).

### 5.4 Minimal Lambda sweep

The design proposes a constrained sweep optimized for rapid failure detection.

* **Sweep A:** $\tau_A \in \{1, 2, 3, 4, 8\}$. (5 values).
* **Sweep B:** Band $\in \{[1,2], [2,3], [3,4], [2,4]\}$. (4 values).
* **Run Parameters:** 5 random seeds per parameter value. 200 ticks per run (yielding 5 candidate steady-state windows per run).
* **Total Run Count:** 45 runs.
* **Meaningful Failure:** 5 seeds is sufficient to detect if the rule-to-Lambda mapping is pathologically broken. If a parameter value designed to produce shifting structures (Rule B) results in a `Tick_to_Freeze` < 200 on 5 out of 5 seeds, the design fails at the micro-rule level. This distinguishes structural failure of the rule from stochastic undersampling.

### 5.5 Expected joint-signature outcomes

The design establishes the following expectations for the observable pair, which the sweep is built to test (and potentially falsify).

* **Rule A Expected Outcomes:** As structural conduciveness increases (threshold lowers), the system is expected to transition from inactive (low rho, low/low coherence) to frozen locked clusters. In the frozen state, the design expects an earned steady-state window to produce **high Psi_meanI_state / high Psi_persistence_I**. Rule A is not expected to produce a divergent signature because it lacks a mechanism to force structural motion.
* **Rule B Expected Outcomes:** As structural conduciveness varies the activation band, the design expects to find a lifted rho regime where the narrow band prevents static freezing. In these earned steady-state windows, the moving structures are expected to produce the divergent signature: **high Psi_meanI_state / low Psi_persistence_I**.

### 5.6 Gate attachment

The proposed runs strictly inherit the constraints of the cleared precondition gates:

* **C3-ENV-001:** Provides the locked Python 3.14.4 / Mesa 3.5.1 / NumPy 2.4.4 execution boundary. Licenses L1 implementation success.
* **C3-CTL-001:** Provides the validated observable math (8-neighbor toroidal Moran's I) and grid-local permutation null functions. Licenses L2 measurement validity, ensuring the observables accurately capture the state-based spatial geometry of the grid.
* **C3-SS-001:** Provides the windowing logic and the exact thresholds for the four filter diagnostics. Licenses the classification of an "earned steady-state window" and a "lifted activation" window as independent apparatus-grounded facts.

### 5.7 Four-level distinction per run-class

For any proposed sweep (Rule A or Rule B, at any Lambda value), the outcomes are strictly stratified:

* **L1 (Implementation):** The script executes without crashing, updates per-cell active-state values according to the specified local rule and topology, and successfully writes well-formed CSV and array outputs.
* **L2 (Measurement-Validity):** The computed Psi_meanI_state and Psi_persistence_I values accurately represent the spatial structure of the grid for that specific run, with grid-local nulls cleanly separating spatial organization from density.
* **L3 (Steady-State-Eligibility):** A 100-tick window within the run independently satisfies the SS-001 criteria for `Steady_State_Candidate` and `Lifted_Activation_Candidate`.
* **L4 (Interpretation):** [Empty by design]. What the returned joint-signature means for the theory of Regime-II-as-structural is strictly held for Mike / Layer 1.

### 5.8 Co-equal-pair guard

The design explicitly holds Psi_meanI_state and Psi_persistence_I as a co-equal pair. Neither observable is named or treated as theoretical Psi within the telemetry schema or the local-rule logic. The SS-001 flags `Steady_State_Candidate` and `Lifted_Activation_Candidate` are tracked and recorded independently. The divergence recorded in CTL-001 Case D acts as an empirical baseline for measurement validity, not an ontological tiebreaker for the theory.
