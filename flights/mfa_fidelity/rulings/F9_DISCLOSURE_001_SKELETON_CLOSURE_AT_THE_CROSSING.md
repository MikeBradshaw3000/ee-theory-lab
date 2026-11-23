# Disclosure Record — F9 Disclosure 001: the skeleton site closure at κ = 1.00 under the registered solver (Contract F9 v0.7 §4.2)

**Entered by:** Mike, Theory Architect, 2026-11-19, on L2's recommendation (M5 round-1 review, §8, Q8; `1700fe17f2280da6…`) that the limitation be recorded beside the contract before any fidelity report is built.
**Document type:** a DISCLOSURE, not a ruling and not a decision. It is filed in `rulings/` because that folder is the register of records that sit beside the contracts.
**Status:** an append-only disclosure beside the FROZEN contract (`FLIGHT_9_CONTRACT_v0_7.md`, SHA-256 `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`). It changes no byte of the contract, no registered value and no rule. It is not an interpretation: the contract's sentence is not in doubt.
**Scope.** Fidelity only. The site closure is a comparator (§4); nothing here is scored or enters B or D.

## What the contract registers

§4.2: the site closure is "iterated from p = 1 (skeleton) or p = π₁ (realization) to a fixed point: tolerance 1e-12 in max norm, at most 200,000 iterations. Nonconvergence is recorded 'comparator unavailable' for that arm and level and affects no endpoint." (Freeze record item 15.)

## What is disclosed

**On the three arms measured, the skeleton's closure at κ = 1.00 does not meet that tolerance within that cap, and the reason given below leads L1 to expect the same on the others.** κ = 1.00 is a registered level (§2.9) and is, by construction, the point where the zero-floor map loses stability at p = 0 (§4.1). There the iteration from p = 1 decays algebraically, not geometrically.

- **Measured (L1's container, placed `f9/closure.py` `7c20206595b7a518…`):** on T0, TA·P and TB·H the change after 200,000 applications was 1.3e-10, 1.9e-10 and 1.6e-10, each above 1e-12. The T0 case is a test in `test_f9_m5.py` and passed on the canonical machine (`f9_m5_module_canonical_2026-11-18.txt`) and on L2's.
- **Derived for T0 (L2, M5 round 1, §8):** at κ = 1 the uniform zero-floor map is f(p) = p − (q + q²/2)·p² + O(p³); with a = q + q²/2 ≈ 0.1977 the iterate behaves as 1/(a·n) and its change as 1/(a·n²), about 1.26e-10 at n = 200,000. Reaching 1e-12 would take about 2.25 million applications.
- **Expected, NOT measured:** the same on the other twelve arms. L1 has not run them. Until the fidelity job runs, this is an expectation.

## What follows

- **On the three measured arms** (T0, TA·P, TB·H) the skeleton's closure record at κ = 1.00 is `comparator unavailable` and carries no map (placed M5; L2: withholding the unconverged iterate is correct). **The other twelve arms are expected to return the same, subject to their authorized runs;** an arm whose closure does converge there simply has a comparator.
- **Wherever an arm's skeleton closure at κ = 1.00 does not converge,** the closure-referenced fidelity items for that arm's skeleton at that level are unavailable for that reason, and a report says so in those words. It is not an apparatus failure and not a defect of the instrument.
- The realization's closure at κ = 1.00 converged on the three arms measured, in 259 applications each (it has a floor). On those arms the skeleton's closures at the levels on either side converge: below the crossing to a small positive map near zero, just above it slowly (2,177 to 3,337 applications at κ = 1.05 on the three arms measured).
- **The solver is not changed.** A longer cap or a looser tolerance would be a change to a registered value. None is proposed.
- Each such level costs the full 200,000 applications: 60 to 120 s per arm in L1's container.

*Drafted by L1, 2026-11-19; revised 2026-11-20 to limit the consequences to the measured arms and to conditional future observations (L2 governance round 1, Q2). The expansion and the 2.25 million estimate are L2's.*
