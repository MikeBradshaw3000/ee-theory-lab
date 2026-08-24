"""mfa_instrument.schema_contract — The NORMATIVE telemetry schema ledger.

Item 6 of L2's bounded hardening pass (closure review): the frozen column ledger
lives in this neutral specification-level module. BOTH the writer (telemetry.py)
and the verifier (verify.py) import from here; the verifier never obtains its
normative expectation from the module whose output it verifies, so no single
constant edit can move emitted schema and verification expectation together.

Source of the 25-column family: flight2_production.py @ 4d9a622 telemetry row
dict, read verbatim (Merge Specification v0.4 FROZEN §7.1).
"""

ANCESTOR_COLUMNS = [
    "Tick", "Agent_X", "Agent_Y", "b_i_v", "b_i_u", "b_i_r", "limiting_base_argmin",
    "Lambda_multiplicative", "Lambda_additive", "Lambda_total", "Local_Density",
    "Drive_Raw", "Term_Density_Pos", "Term_Overcrowding", "Term_Offset", "p_base",
    "p_act", "PRNG_draw", "is_active", "Psi_local", "gamma_coef", "Delta_v",
    "Delta_u", "Delta_r", "Term_Lambda",
]
EXTENSION_COLUMNS = ["Delta_from_Psi", "Delta_from_rho"]   # spec §4.5 (rho channel)
NOISE_COLUMN = "Noise_Draw"                                 # conditional (η_MFA)
RHO_TABLE_COLUMNS = ["Tick", "rho_global"]                  # spec §7.2 tick table
