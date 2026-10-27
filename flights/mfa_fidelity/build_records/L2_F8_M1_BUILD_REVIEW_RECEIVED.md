# L2 — Flight 8 M1 source review, round 1 (qualified)

**Register:** Instrument build review. **Disposition: DEFECT-WITH-REPAIR (source-level); contract-completeness qualification.** No placement or run authorized.

## Evidence and limitation
The ZIP's five entries were read and SHA-256 prefixes verified: `__init__.py` `49dc56533fcb16f7`; `config.py` `afbce4b29272c9a1`; `dynamics.py` `b854b1360a0c75c6`; `test_f8_m1.py` `4a391b83a074c8d4`; build packet `85a74de16c2a2acf`. The separately uploaded `FLIGHT_8_CONTRACT_v0_8_4.md` was **not mounted at its advertised path**, and the freeze record and Appendix A were not supplied. Accordingly this is a source-level review against the packet's representations of the contract, **not a completed independent clause-by-clause verification of §§2.1–2.10, 4.1, 8 or the freeze record**. Do not treat it as final clearance.

## Declaration rulings
| Declaration | Ruling | Reason |
|---|---|---|
| B1 masters | **Conditionally acceptable, not ratified** | Two panels are reproducibly generated and checked for uniqueness and mutual disjointness. The code does not check actual disjointness against E1's retired *panel*, only inequality of master identifiers; the asserted retired-panel disjointness needs a direct check against the committed E1 panel. Governance ratification remains external. |
| B2 object-code stream key | **Requires contract confirmation** | The added object-code component makes streams distinct by construction in ordinary use, but changes the named three-stage derivation grammar. The frozen contract text must determine whether this is permitted elaboration or requires amendment. |
| B3 written probability form | **Source-consistent, conditional** | Both hazards use `1-exp(-h)` as declared; no evidence here of a numerical mismatch with the packet's formula. |
| B4 direct lambda-bar hazard | **Source-consistent, conditional** | The stepper uses homogeneous `lambda_bar` directly and records a fourth-root base. Whether bypassing F is expressly authorized requires inspection of the actual frozen contract/freeze record. |
| B5 post-tick rho record | **Source-consistent, conditional** | `rho[0]` is initialized state; `rho[t]` is after advance t, and the T=3000 tail indexes 2001–3000. Contract confirmation is still needed. |

## Defects and repairs

### D1 — Production level membership not enforced
`config.py::f8_run_spec` accepts **any positive** `level_micro` at production shape, although its own docstring promises a pass-1 level and the packet defines a frozen 24-level sweep. For example `level_micro=1000000` is accepted when the seed is on the canonical panel, despite not belonging to `F8_LEVELS_MICRO`. This permits a nominal production-shape record outside the frozen sweep.

**Repair:** At production shape require `level_micro in F8_LEVELS_MICRO`, except for explicitly distinguished, contract-authorized calibration/control jobs. Add negative tests for off-panel levels at production shape and positive tests for any explicitly permitted exception.

### D2 — Execution trusts mutable/constructible run-spec fields
`dynamics.py::run` checks only `spec.declaration_sha256`, then uses `spec.grid`, `ticks`, `eta_floor`, `g`, `mu`, `lambda_bar`, `obj`, `seed`, and `stream_key` without reconstructing or validating their relationships. `F8RunSpec` is a publicly constructible frozen dataclass; `dataclasses.replace(valid_spec, g=...)` retains the same declaration hash and changes the executed mechanism. Likewise a changed `lambda_bar` or `eta_floor` can execute under an apparently frozen declaration.

**Repair:** In `run`, independently reconstruct the authorized spec from canonical identity fields and compare all execution-affecting fields (including types), or use a single validated immutable internal spec with a complete field-equivalence check. Ensure the execution generator's key equals the recorded key. Add negative tests mutating each mechanism field via `dataclasses.replace`.

### D3 — Invalid reduced-shape inputs can generate undefined records
`f8_run_spec` does not enforce positive grid/ticks, or `ticks >= window`, or a tail length divisible by the window. A reduced `ticks=0` spec leads to empty tail and `nan` mean; other short runs silently generate zero windows or discard remainder ticks. A zero grid can also lead to division by zero.

**Repair:** Validate `grid > 0`, `ticks > 0`, and a well-defined reduced-run tail/window policy before constructing the spec; either require `tail_ticks >= window` and exact divisibility, or explicitly define and test a separate smoke-only output convention. Reject invalid values fail-closed.

### D4 — B1 retired-panel disjointness assertion not checked
`verify_frozen_identity` rejects the retired E1 master `20260917` but does not compare either new panel against the 20 actual E1 seeds. Different masters do not mathematically prove disjoint output panels.

**Repair:** Compare both new panels against the committed E1 retired panel (with its verified identity) at the appropriate preflight or governance binding stage; fail on overlap. Add a discriminating collision test.

## Testing and scope
The packet reports 29 passing M1 tests in its container. That result is **reported, not independently reproduced here**: the ZIP does not include the parent package dependencies required to run the module in isolation. Neither the canonical twenty-pin test run nor the committed contract, freeze record and Appendix A identity verification has been independently performed.

## Disposition
**DEFECT-WITH-REPAIR**, based on D1–D3; D4 is an additional declaration-verification gap. B2 and the remaining contract-sensitive rulings stay qualified until the actual frozen contract and freeze record are readable. L1 should repair the defects and return changed-source identities and discriminating tests. L2 must then complete the contract-specific review before any SOUND clearance. Mike retains placement and execution authority.
