yaml_content = """prereg_id: "reg_01_scale_interactions"
prereg_version: "1.0"
model_family: "linear"
formula_role: "authoritative"
formula: "logit_p_base ~ Lambda_total + Local_Density + Local_Density_squared + Term_Lambda + Term_Density_Pos + Term_Overcrowding + Psi_local + b_i_v + b_i_u + b_i_r + F_variant + scale + epoch + scale*F_variant + scale*rho_global + scale*psi_global"

canonical_input_filenames:
  - "flight6_probe1_overcrowding_20x20.parquet"
  - "flight6_probe1_overcrowding_40x40.parquet"
  - "flight6_probe2_starvation_FLR_20x20.parquet"
  - "flight6_probe2_starvation_FLR_40x40.parquet"

tier2_globals_path: "phase_4b/tier2_outputs/global_timeseries.csv"

outcome:
  name: "logit_p_base"
  construction: "eta_floor_inversion_of_p_base"
  eta: 0.01

predictors:
  - Lambda_total
  - Local_Density
  - Local_Density_squared
  - Term_Lambda
  - Term_Density_Pos
  - Term_Overcrowding
  - Psi_local
  - b_i_v
  - b_i_u
  - b_i_r
  - F_variant
  - scale
  - epoch

interactions:
  - "scale:F_variant"
  - "scale:rho_global"
  - "scale:psi_global"

excluded_variables:
  - "p_act"
  - "p_base"
  - "Drive_Raw"
  - "PRNG_draw"
  - "Delta_v"
  - "Delta_u"
  - "Delta_r"

uncertainty_method:
  primary: "cluster_robust"
  cluster_variable: "run_x_tick"
  sensitivity:
    - "cell"

interpretation_boundary:
  licenses: |
    1. Quantification of F-form main effect on logit(p_base) at the cellular
       level.
  does_not_adjudicate: |
    1. Architectural selection of F_LR vs F_2_symmetric for Open Element 14.
"""

# Writing it strictly using standard utf-8 without a BOM
with open("phase_4b/pre_registrations/reg_01_scale_interactions.yaml", "w", encoding="utf-8") as f:
    f.write(yaml_content)

print("SUCCESS: File cleanly written by Python with linear family!")