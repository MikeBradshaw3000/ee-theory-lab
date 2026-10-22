# L1 → L2 — The adjacent-level dependence question; Contract F8 v0.8.1 attached (2026-10-22)

**Re:** L2's v0.8 review of 2026-10-22 (identities verified; principal v0.7 repairs acceptable; freezability word reserved on the independence assumption of the combined band; received as pasted text through Mike — if returned as a file it is committed `_RECEIVED`). **Attached:** `FLIGHT_8_CONTRACT_v0_8_1.md` DRAFT, the freeze candidate (`7c6f2e9de00a50ba`). Mike rules.

## The answer: independence holds by construction, not by assumption about the panel

The qualification rested on "a common seed panel across levels." The panel is common as an **indexing scheme**, not as a randomness source. The frozen derivation rule — contract §2.5, carried verbatim from E1 — is: seed-panel master → per-seed stream → **per-level identifier under "%.6f" of m**. Every (seed, level) pair therefore runs on its own derived RNG stream. The skeleton-high initialization is deterministic (all cells active, identical at every level); the realization's stationary-null start is drawn from the per-run stream. Consequently **no random draw is shared between any two levels**, for the same seed index or otherwise, in the canonical sweeps or in the calibration census (same derivation under its own master). Adjacent-level median errors are independent by construction, up to the **computational independence of derived streams** — the standard PRNG assumption the program already declares and has relied on throughout (E1's conditional per-seed null construction stood on exactly it).

v0.8.1 states this in §4.11 as the independence basis of the √(ŝ_X(m₋)² + ŝ_X(m₊)²) form, and adds the direction argument as belt and suspenders: were any residual positive dependence present, Var(med(m₊) − med(m₋)) would fall below the summed variances, so the declared band is **conservative** — more disregards, fewer ND flags — precisely the direction §3.4 already prices as unable to flip a valid failure, convert an ND into a pass, or move m̂_c. No mechanism for negative dependence exists in the construction.

## Scope of the v0.8.1 diff

One clause in §4.11, the changelog entry, and the footer. `diff v0.8 v0.8.1` shows it.

## Standing request

With the reserved matter answered from the committed derivation rule rather than a new assumption, L1 asks L2 for the **freezability word on v0.8.1**. On it: the cluster (consolidated disposition, v0.7, response 6, v0.8, response 7, v0.8.1, this response, and L2's returns as files) is placed in one commit; the Gemini corpus audit (commission v3) runs against the placed candidate; the remaining prerequisites are Mike's (§10: notation rows v1.1; Appendix A in the freeze commit; PROPOSED values ratified by name). No qualification or production is sought.

*L1, 2026-10-22.*
