# L2 — Flight 8 M1, Round 2 source review (2026-10-26)

**Register:** Instrument build review against frozen Contract F8 v0.8.4 (`e87277a2d11e948f`), freeze record (`16869692a043b139`) and Appendix A (`94d527624beafa7c`).  **Verdict: SOUND (source review).** This is not authorization to place the module or execute a flight. Mike retains decision authority and canonical-suite execution remains a separate prerequisite.

## Evidence and independently executed tests

The delivered archive contains 38 regular files and five directory entries. The response (`9e8218f990b42fa8`), changed `f8/config.py` (`43ea8de23c0d718b`), `f8/dynamics.py` (`4d886e6acb51d331`), `tests/test_f8_m1.py` (`7cea440c282b369a`), and all three contract files match their declared SHA-256 prefixes. The three frozen reference documents are present; the round-1 missing-contract qualification is removed.

From `flights/mfa_fidelity/instrument`, independently ran `python -m pytest tests/test_f8_m1.py -q`: **65 passed, four failed solely because `pyarrow` is not installed**. Three failing tests import frozen E1 configuration, which imports `pyarrow.parquet`; the fourth calls the F8 Parquet writer, which imports `pyarrow`. An attempt to install `pyarrow` failed because package-network resolution is unavailable. Thus **69/69 has not been independently reproduced in this environment**. L1 reports 69/69 in its environment; that remains L1-reported, not L2-verified. The 65 passing tests provide positive source-level evidence; the four dependency-blocked tests must be rerun in an environment with `pyarrow` before the canonical acceptance condition is asserted.

## Round-1 defects and round-2 repair rulings

| Finding | Ruling | Basis |
|---|---|---|
| **D1 — production off-grid levels** | **REPAIRED** | `f8_run_spec` rejects off-panel levels at the 50×50/3000 production shape, for either seed panel; reduced-shape controls remain separately identified. Negative and positive level-membership tests pass. |
| **D2 — unvalidated constructed run spec** | **REPAIRED** | `validate_run_spec` reconstructs from identity fields and checks every dataclass field for value and exact type. `run` executes the reconstructed spec and derives its generator from the verified recorded key. Mutation tests pass. |
| **D3 — undefined reduced shapes** | **REPAIRED** | Grid 3–50, ticks 100–3000, and tail length divisible by the 100-tick window are enforced. This is a test/control shape policy, not a change to the frozen production shape. Invalid-shape and valid-window tests pass. |
| **D4 — retired E1 panel not checked directly** | **REPAIRED** | Frozen E1 retired seeds are carried as a literal with the E1 digest, and preflight rejects overlap with either F8 panel. Collision and tampering tests are present; direct E1 import-based cross-check tests were blocked by the missing dependency, so their independent execution remains outstanding. |
| **D5 — survival tested using window maximum** | **REPAIRED** | Survival now requires the minimum active count in every tail window to be positive. For an absorbing skeleton this is equivalent to a positive terminal count. The within-window-extinction regression passes. |

## Build declarations B1–B5

| Declaration | L2 ruling | Contract assessment |
|---|---|---|
| **B1 — canonical/calibration masters** | **SOURCE-SOUND; governance ratification reserved** | Distinct declared masters produce frozen, reproducible, disjoint panels; both are checked against the retired E1 seeds. Contract §8 treats masters as DERIVED@BUILD; the source alone does not ratify them. |
| **B2 — object code in RNG stream key** | **ACCEPTED as an explicit per-object stream separation** | Contract §2.5 fixes the master→seed→level identity and §4.11 requires distinct streams across levels. The recorded key `(seed, object_code, level_micro)` preserves those identities and adds object separation, without reusing random draws. This is a disclosed implementation elaboration, not a change to the level coordinate. This acceptance does **not** establish bit identity with E1's stream algorithm, which the contract does not demand for F8. The object-code mapping and key must remain frozen with this build. |
| **B3 — probability forms** | **SOUND** | The implementation evaluates `1-exp(-(eta_floor+g*lambda_bar*d)*dt)` for activation and `1-exp(-mu*dt)` for deactivation, with synchronous state reads and one full-grid uniform per tick, matching §§2.3–2.5. |
| **B4 — homogeneous λ̄ directly in hazard** | **SOUND** | §2.2 defines λ_i=F(v̄,ū,r̄)=λ̄; §2.8 sets λ̄ through homogeneous bases. The source derives `b=λ̄^(1/4)` under `F_2_symmetric(b,b,b)` and records b, while consuming the mathematically equal homogeneous λ̄. Freeze record §3 item 2 describes F as inert under these bases. |
| **B5 — post-advance density convention** | **SOUND** | `rho[0]` is initialization; `rho[t]` is the state after tick t. The final 1,000 post-advance states are partitioned into ten complete 100-tick windows, conforming to §4.1 and the tail-window mean in §4.11. The contract does not prescribe an incompatible pre-update convention. The Parquet roundtrip test remains dependency-blocked here. |

## Disposition and boundary

**SOUND** for the reviewed M1 implementation and the D1–D5 repairs, with B1 ratification external to this source verdict. **No source-level defect requiring a further repair was established.** The independent 69-test pass condition is **not certified** by L2: install `pyarrow` in the canonical environment and rerun `python -m pytest tests/test_f8_m1.py -q`, preserving its output and environment identity. Confirm the four previously blocked tests pass before treating the test prerequisite as discharged. No flight run is authorized by this review.
