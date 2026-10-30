# Ruling Record — F8 Interpretation 001: tail density ρ̂ of a run extinct inside the tail (Contract F8 v0.8.4 §3.4 and §4.11)

**Ruled by:** Mike, Theory Architect, 2026-10-29 ("A"), on L1's question in `L1_TO_L2_F8_MP1_ROUND2_RESPONSE_2026-10-29.md` and with L2's recommendation (M-P1 round 1, D4) that the interpretation cover §3.4 as well as §4.11 and be recorded as an identified interpretation alongside the frozen contract.
**Status:** an identified interpretation of the FROZEN contract (`FLIGHT_8_CONTRACT_v0_8_4.md`, SHA-256 `e87277a2d11e948f…`). The contract's bytes and identity are unchanged; this record resolves an ambiguity between two of its sentences and binds every instrument module that reads either.

## The two sentences

- **§4.11 per run:** "survival = tail-window active count > 0 at every tail window …; ρ̂ = tail-window mean density. A run that goes extinct is a valid observation (survival = 0, ρ̂ = 0), never 'missing'."
- **§3.4:** "ŝ_sk(m) = the same statistic under the skeleton rule from the high initialization (extinct runs contribute ρ̂ = 0 …)".

"ρ̂ = tail-window mean density" and "(ρ̂ = 0)" agree for a run extinct before the tail and disagree for a run that goes extinct inside the tail. Placed M1 (`dynamics.py` `cc663dd3c14197a8`, L2-cleared) implements the mean; the M5 census is built from that field; the round-1 M-P1 evaluator asserted the parenthetical. L2 surfaced the conflict (M-P1 round 1, D4) and declined to amend the contract silently, as did L1.

## The interpretation (binding)

1. **ρ̂ is the mean density over the entire declared tail (1,000 ticks), including the zero contributions after an extinction.** This is M1's placed `rho_tail_mean` (count-grid arithmetic: one integer sum over the tail counts, one division by tail_ticks × n_cells). It applies wherever the contract uses ρ̂ or "tail density": the per-run observable of §4.11, the seed-median med(m) of the four tests, and the census statistics ŝ(m) and ŝ_sk(m) of §3.4.
2. **An entirely inactive tail has ρ̂ = 0; extinction during the tail may instead yield survival = False and ρ̂ > 0.** The parentheticals "(survival = 0, ρ̂ = 0)" in §4.11 and "extinct runs contribute ρ̂ = 0" in §3.4 describe the run extinct before the tail begins. Survival is the window-minimum rule (active count > 0 throughout every tail window), so a run extinct inside the tail is non-surviving and carries its positive pre-extinction contributions in ρ̂. Both are valid observations, never "missing"; neither is coerced to the other.
3. **The evaluator (M-P1) verifies both measurements from the persisted trace using the placed M1 arithmetic** (`observation_from_result`: survival, ρ̂ and the window means recomputed from `active_counts` and required to equal the cached fields exactly), with regression cases covering extinction before the tail, inside an early tail window, inside the final window, and no extinction (`test_f8_mp1.py`, `test_extinction_before_inside_and_at_the_end_of_the_tail_is_a_valid_observation_as_m1_defines_it`).

## Consequences

- No change to placed M1, M2–M5 or Appendix A: their arithmetic already realizes points 1–2. The census identity and ŝ_sk are as computed by M5.
- The alternative reading (ρ̂ ≡ 0 for every non-surviving run) is rejected; adopting it later would be a change to placed M1 and to the census, through its own L2 round, never an M-P1 coercion.
- Where the four tests see this: T-S1′/T-S2 read survival only; T-S1c/T-R1′ read med(m), which for a skeleton level with fewer than 18 survivors is outside T-S1c's domain. The interpretation changes no verdict grammar.
- M7 carries this record's identity with the F8 governance record.

*Drafted by L1 from Mike's ruling, 2026-10-29; the text of points 1–3 follows L2's recommended wording.*
