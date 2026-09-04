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

# Lineage B (become_survive) row family — Phase-2 item 4. Source of the field set:
# dynamics._step_become_survive sink fields, which transcribe c3_w2_tcop.py @ 4d9a622
# step_tcop_core (L263-272). The draw column is named rand_grid, B's own source name:
# it is the SINGLE shared draw consumed by both branches, a different role from A's
# per-cell PRNG_draw, and must never carry that name. Q columns are structurally
# absent: become_survive supports the Q-disabled subset only (N3 ruling of record).
#
# TIME SEMANTICS (normative, both families): the row at Tick = t carries POST-STEP
# is_active — the state after tick t's update. Pre-step index conventions required by
# any analysis (Gate B Amendment 2) are analysis-layer obligations; this ledger names
# what is recorded so that no consumer can misread the index.
BECOME_SURVIVE_COLUMNS = ["Tick", "Agent_X", "Agent_Y", "g_q", "p_become", "rand_grid",
                          "is_active", "Psi_local"]
