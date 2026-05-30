# OBS001_06 - Layer 3 v2 design menu (A + B)

Source: Layer 3 (Gemini), responding verbatim to OBS001_05.

---

Message received and locked. I acknowledge the corrections from Layer 1's implementation review. The framing discipline holds: this is a design menu, no execution has occurred, and L2 clearance remains strictly a Layer 1 judgment at review.

Here is the revised wave-one design menu (A + B), fully reconciled against the primary source and the six requested corrections.

### 5.1 Local-rule specification

Both rules operate on the locked 50 x 50 toroidal grid, evaluating the Moore radius 1 (8-neighbor) active-neighbor count for each cell at tick $t$ to determine how the agent acts at tick $t+1$.

* **Initial Condition (Both Rules):** The grid is seeded at $t=0$ by assigning per-cell active-state values (1 for active, 0 for inactive) uniformly at random to achieve a target starting $\rho$ (e.g., 0.10).
* **Rule A (Strict Lower Threshold):** An agent acts (becomes or remains active) at $t+1$ if the count of active neighbors at $t$ is $\ge \tau_A$. If the count is $< \tau_A$, the agent deactivates. The rule has no upper/overcrowding bound.
* **Rule B (Range-bound / Life-like):** An agent acts (becomes or remains active) at $t+1$ strictly if the count of active neighbors at $t$ falls within a closed interval $[\tau_{B, min}, \tau_{B, max}]$. If the count is below $\tau_{B, min}$ or above $\tau_{B, max}$, the agent deactivates.

### 5.2 Lambda-like parameter for each rule

The structural conduciveness parameter, $\Lambda$, maps to the micro-rule thresholds to drive the system through varying $\rho$ and coherence regimes.

* **Rule A ($\Lambda_A$):** Maps inversely to the strict lower threshold $\tau_A$. To resolve the seam between the primary source and substrate physics, the design adopts the fully pessimistic-on-passing path: sweeping the full integer range $\tau_A \in \{1, 2, 3, 4, 5, 6, 7, 8\}$. This allows the substrate to adjudicate exactly where the uniform-fill, locked-cluster, and extinction regimes live without prematurely asserting their boundaries.
* **Rule B ($\Lambda_B$):** Maps to the position and width of the activation band. The design specifies shifting this band across the neighborhood space: $[\tau_{B, min}, \tau_{B, max}] \in \{[1,2], [2,3], [3,4], [2,4]\}$.

### 5.3 Telemetry schema

The design specifies recording the following quantities:

* **Per-tick records:**
  * $\rho(t)$ (scalar mean of per-cell active-state values).
  * The complete $50 \times 50$ matrix of per-cell active-state values.

* **Per-window records (100-tick windows, 25-tick sliding step):**
  * Psi_meanI_state and its grid-local permutation null z-score.
  * Psi_persistence_I and its grid-local permutation null z-score.
  * The four SS-001 diagnostics: `relative_drift`, `rho_cv`, `rho_range_over_mean`, and `mean_rho`.
  * The two independent SS-001 flags: `Steady_State_Candidate` (evaluating against 0.10, 0.10, 0.25) and `Lifted_Activation_Candidate` (evaluating against 0.05).

* **Rule-specific diagnostics (per run):**
  * `Tick_to_Freeze`: The tick index at which $\Delta \text{states} = 0$ for 10 consecutive ticks.
  * `Tick_to_Zero`: The tick index at which $\rho(t)$ precisely equals 0.0.

* **Storage:** Per-tick active-state matrices in Parquet or compressed NPZ; windowed telemetry and diagnostics in a flat CSV.

### 5.4 Minimal Lambda sweep

The design proposes a constrained sweep to test the rules and fail meaningfully if the mapping is broken.

* **Sweep A:** $\tau_A \in \{1, 2, 3, 4, 5, 6, 7, 8\}$ (8 values).
* **Sweep B:** Band $\in \{[1,2], [2,3], [3,4], [2,4]\}$ (4 values).
* **Run Parameters:** 5 random seeds per parameter value. 200 ticks per run (yielding 5 candidate steady-state windows per run).
* **Total Run Count:** 60 runs (12 parameter sets $\times$ 5 seeds).
* **Meaningful Failure (Rule A):** If any $\Lambda$ value in Sweep A produces a divergent joint signature (high meanI / low persistence, or low meanI / high persistence) on 5/5 seeds in earned steady-state windows, the design fails at the micro-rule level. Rule A is intended to be non-discriminating (the both-agree baseline); a divergent outcome here reveals a failure of the architecture.
* **Meaningful Failure (Rule B):** If a parameter value designed to produce shifting structures produces `Tick_to_Freeze` < 200 on 5/5 seeds, the rule has structurally failed to force sustained motion.

### 5.5 Expected joint-signature outcomes

The design establishes the following per-value expectations for the observable pair within earned steady-state windows:

* **Sweep A Expectations (Non-discriminating baseline):** No $\Lambda$ value in Sweep A is expected to produce the Regime-II-candidate signature (lifted $\rho$ with low/low non-degenerate coherence) or the divergent signature. Rule A is expected to move the observables together.
  * **$\tau_A \in \{1, 2\}$:** Expected to run away to uniform saturation ($\rho \to 1.0$). Expected outcome: **Low/Low (Degenerate)** due to zero spatial variance.
  * **$\tau_A \in \{3, 4, 5\}$:** Expected to freeze into static structures. Expected outcome: **High/High** (High Psi_meanI_state / High Psi_persistence_I).
  * **$\tau_A \in \{6, 7, 8\}$:** Expected to extinguish ($\rho \to 0$). Expected outcome: **Low/Low (Degenerate)**.

* **Sweep B Expectations (Probe for Regime-II and Divergence):**
  * **Band [2,4]:** The wide band is expected to produce unstructured "boiling" dynamics. Expected outcome: Lifted $\rho$ with **Low Psi_meanI_state / Low Psi_persistence_I**. *This is explicitly the Regime-II-candidate regime.*
  * **Band [2,3]:** The narrow, classic Life-like band is expected to produce sustained moving structures. Expected outcome: Lifted $\rho$ with **High Psi_meanI_state / Low Psi_persistence_I**. *This is the divergent signature.*
  * **Bands [1,2] & [3,4]:** Expected to serve as boundary cases, likely tending toward noisy saturation (low/low) or extinction (low/low), framing the structural behavior of the middle bands.

### 5.6 Gate attachment

* **C3-ENV-001:** Provides the locked Python/Mesa/NumPy execution boundary. Licenses L1 implementation success.
* **C3-CTL-001:** Provides the validated observable math and grid-local permutation null functions. Licenses L2 measurement validity.
* **C3-SS-001:** Provides the windowing logic and the exact thresholds for the filter diagnostics. Licenses the classification of an "earned steady-state window" and a "lifted activation" window as independent apparatus-grounded facts.

### 5.7 Four-level distinction per run-class

* **L1 (Implementation):** The script executes without error, updating per-cell active-state values according to the specified rule and topology, writing well-formed outputs.
* **L2 (Measurement-Validity):** The computed observables accurately represent the spatial structure of the grid for that specific run, with grid-local nulls separating spatial organization from density.
* **L3 (Steady-State-Eligibility):** The two SS-001 flags (`Steady_State_Candidate` and `Lifted_Activation_Candidate`) are computed and reported independently for a 100-tick window. The window earns its classification for each flag separately; they are not conjoined into a single passing grade at the L3 level.
* **L4 (Interpretation):** [Empty by design]. What the returned values mean for Regime-II-as-structural is strictly held for Layer 1 / Mike.

### 5.8 Co-equal-pair guard

The design holds Psi_meanI_state and Psi_persistence_I as a co-equal pair. Neither observable is named or treated as theoretical Psi. The SS-001 flags remain independent. The CTL-001 Case D divergence is an empirical baseline for measurement validity, not an ontological tiebreaker.
