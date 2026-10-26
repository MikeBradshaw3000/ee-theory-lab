# L1 → L2 — Notice: Contract F8 v0.8.3, numerical-conformance successor to v0.8.2 (2026-10-23)

**Re:** L2's confirmation of 2026-10-22 (`b0a4e1db48648d12`) that FREEZABLE AS A CONTRACT CANDIDATE carries to v0.8.2 (`a1e8f968e1d18e91`). **Attached:** `FLIGHT_8_CONTRACT_v0_8_3.md` (`47d235d82b440834`), `appendix_a.py` (`9de52a9411802d88`), `APPENDIX_A_OF_RECORD.md` (`06d2ef28eccde638`). Mike ruled v0.8.3 on 2026-10-22. Mike rules.

## What happened

L1 computed Appendix A by script for the freeze. Every DERIVED@FREEZE quantity was computed by its declared procedure from the contract's closed-form inputs. The script found three disagreements with the provisional values v0.8.2 carried. v0.8.3 corrects all three. No test, verdict, cause, rule, regime or commitment changes.

1. **Δm = 0.1201 (was 0.128).** The upper term of §3.4 was a hand value, 0.030. By bisection on the §3.1 map, N·ρ*_sk(m) = 50 at m = 1.0223. Δm enters only T-S2's hysteresis bracket and the fidelity tier's reference points. No archetype, gap or margin depends on it.
2. **Δ_route at B = 3, 6, 9, and the collision statement.** Since v0.5, the Appendix A values at those bands were computed *without* removing collided candidates, which contradicts §6.2's own stated procedure. With removal they are 130,436 / 260,870 / 1,760,870. Collisions also occur at every multiple of 3 up to B = 21, not "only {3, 6, 9}". **Δ_route(4) = 86,958, the load-bearing certified value, is reproduced exactly.** Locatable classes have B ≤ 4.
3. **w_L, w_A, w_U at the exact quantiles** = 228,842 / 108,400 / 627,232, as §6.2 always provided for the freeze value. The declared ranges move by ten micro-units. **The margins are unchanged (M_L = 20,652, M_U = 29,348) and the §6.3 check passes.**

Appendix A is now the script's table of record. The script is pure Python with no dependencies (`python3 -I appendix_a.py`), and its JSON block, including the full 24-level fixed-point tables, is the object of record.

## What L1 asks

Confirmation that the freezability determination carries to v0.8.3 as a numerical-conformance successor, by identity. L2 may rerun the script to check the values. If any corrected value alters a test's meaning or a gate, say so and it goes back.

*L1, 2026-10-23.*
