# L1 → L2 — Flight 8 M1, round 2: response to the round-1 review and changed-source packet, 2026-10-26

**Answers:** `L2_F8_M1_BUILD_REVIEW_RECEIVED.md` (`0eac901c8027d134`; DEFECT-WITH-REPAIR, qualified because the frozen contract was not readable). **Supersedes the round-1 sources;** the round-1 packet (`85a74de16c2a2acf`) stands as the record of B1–B5. Register unchanged: nothing placed until L2 clears and Mike's canonical suite passes; no run authorized.

**The qualification is now removable.** The round-1 delivery did not put the contract in your environment. This zip carries the frozen contract, the freeze record and Appendix A **at their repository paths**, together with the whole `mfa_instrument` package, so the test module runs in isolation (L1 checked it from a fresh directory holding only the zip's contents: 69 passed, the Appendix A binding test included, none skipped).

| Reference file (in the zip) | SHA-256 |
|---|---|
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md` — frozen | `e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182` |
| `flights/mfa_fidelity/contracts/flight8/FLIGHT_8_FREEZE_RECORD.md` | `16869692a043b139030ca3ab1ef3ed988c638bf25a6f04fb651b2e8db76da3e2` |
| `flights/mfa_fidelity/contracts/flight8/APPENDIX_A_OF_RECORD.md` | `94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653` |

## Changed sources (SHA-256, LF)

| File | Round 1 | Round 2 |
|---|---|---|
| `instrument/mfa_instrument/f8/__init__.py` | `49dc56533fcb16f7` | unchanged |
| `instrument/mfa_instrument/f8/config.py` | `afbce4b29272c9a1` | `43ea8de23c0d718b246936c7ff6f18e4f8e5243f77ddb240d896e5d00bdf0e07` |
| `instrument/mfa_instrument/f8/dynamics.py` | `b854b1360a0c75c6` | `4d886e6acb51d331240b97a1065a2967b846c548d319d08aa599acaf58d32765` |
| `instrument/tests/test_f8_m1.py` | `4a391b83a074c8d4` | `7cea440c282b369a611ed3d3ab3c729d1ddb4ee6ca49a76e042eb106c066fc9a` |

The rest of `mfa_instrument/` (package root, `e1/`, `gates/`) is the committed tree at `5d8af44`, unmodified, included so the tests import. Test record (container): `python3 -B -m pytest tests/test_f8_m1.py -q -p no:cacheprovider` → **69 passed**, one process; E1's `test_e1_m1_m2.py` unaffected, 58 passed.

## Defects — all accepted, all repaired

**D1 — production level membership. ACCEPTED.** `f8_run_spec` now refuses a production-shape run (50×50, 3000 ticks) at any level outside `F8_LEVELS_MICRO`, for both panels. No exception is authorized at M1: every production-shape lattice job in §7.3 (job 0's two parts, the three sweeps of §4.11) runs on the pass-1 levels. M5's 701-point census is a closure computation, not a lattice run, and never constructs a run spec. Below production shape any level stays admissible for controls, as stated. Tests: four off-grid levels refused on each panel; all 24 accepted; one off-grid level accepted at smoke shape.

**D2 — execution trusted constructible spec fields. ACCEPTED.** New `validate_run_spec` rebuilds the authorized spec from the supplied spec's identity fields (level, seed, object, panel, grid, ticks). It then requires **every** field equal in value and in exact type. `dynamics.run` executes only the rebuilt spec, and draws its generator **from the recorded stream key** (`generator_from_key`), after checking that key against the derivation. `panel` is now a spec field, so a calibration-panel spec cannot pass as canonical, nor the reverse. Tests: 18 `dataclasses.replace` mutations (g, η_floor, μ, λ̄, base, object, panel, seed, level, level id, tail, window, stream key, declaration hash, and two same-value type changes: `g=1` int, `grid=50.0` float) are each refused by both `validate_run_spec` and `run`. A foreign object is refused. A run's initial state equals the one drawn from its own recorded key. One case is intentionally **not** a refusal: substituting a valid reduced grid or tick count yields exactly the reduced spec that `f8_run_spec` would build for that shape. That spec records its own shape and claims no production identity, so it is accepted. A dedicated test states this.

**D3 — undefined reduced shapes. ACCEPTED.** The shape policy is now part of the frozen declaration (field `reduced_shape_policy`): grid ≥ 3, so the periodic Moore neighbours are distinct; grid ≤ 50 and ticks ≤ 3000; ticks ≥ one window; tail = min(1000, ticks), which must be a whole number of 100-tick windows. Anything else fails closed at construction. Tests: ten undefined shapes refused (grid 0, 1, 2, −3; ticks 0, 50, 150, 950; 51×3000; 50×3001); six defined shapes give whole windows and finite means. The test default `SMOKE` moved from 60 to 100 ticks under the policy.

**D4 — retired-panel disjointness checked only by master. ACCEPTED** (the test module already compared the panels against E1's; the preflight did not). E1's retired panel is now carried as a literal, `E1_RETIRED_SEED_PANEL`, bound to **E1's own frozen digest** `68309ed9…` (verified equal to `mfa_instrument/e1/config.py`'s `E1_SEED_PANEL` and its literal in the test). `verify_frozen_identity` checks that digest, then fails on any overlap between E1's retired seeds and either F8 panel. No `e1` import occurs at run time. The discriminating test plants one retired seed into the canonical panel, re-points that panel's digest so only the overlap can fail, and the preflight raises "retired panel". A second test shows a tampered retired literal is caught.

**D5 — survival used the window maximum. L1-FOUND, REPAIRED.** Round 1 scored survival as "max active count > 0 in every tail window". A skeleton run extinct *inside* the last tail window therefore scored as surviving. §4.11 reads "tail-window active count > 0 at every tail window"; under an exactly absorbing skeleton the only sound reading is "> 0 throughout every window". The rule is now the **minimum** over each window. For the skeleton that is exactly counts[T] > 0. Test: a smoke-shape skeleton run that dies inside its last window must not survive (the round-1 rule would have passed it), and a production-shape survivor satisfies survival ⇔ counts[T] > 0.

The declaration changed (`e1_retired_panel_sha256`, `reduced_shape_policy` added), so its digest literal is now `0d9657d79c8b1c63…`. The level and panel literals and their digests are unchanged.

## B1–B5 — for your ruling, now with the contract in hand

- **B1 (masters 20261026 canonical / 120261026 calibration).** The D4 repair supplies the direct retired-panel check you asked for. Ratification of the masters remains Mike's, through the F8 governance record.
- **B2 (object code in the stream key).** Contract §2.5: "one uniform per cell per tick from the run's RNG stream, derivation rule as E1 (seed-panel master → per-seed stream → per-level identifier under "%.6f" of m)". §4.11, independence basis: "each (seed, level) pair runs on its own derived RNG stream … no random draw is shared between levels". The build keeps the master → seed → level chain. The level enters as its exact micro-unit integer, the value whose "%.6f" rendering is the identifier. The build adds an object component, because §4.11 runs three canonical sweeps (skeleton-high, skeleton-low, realization) over the same panel and levels. Without the object code all three would draw identical uniforms at each (seed, level). L1 reads the addition as a conforming realization of §2.5 and asks L2 to rule. If L2 reads it as needing a clause, the contract's own path is a new version.
- **B4 (λ̄ consumed directly).** Contract §2.2: "**homogeneous** across cells [RULED 2026-10-20]: v_i = v̄, u_i = ū, r_i = r̄. λ_i = F(v̄, ū, r̄) = λ̄"; §2.8: "a sweep level sets λ̄ (through the homogeneous bases) so that m takes the level's value". Freeze record §3 item 2: "under homogeneous bases F is inert to P1 (every cell carries λ̄ and each level sets λ̄ through the bases to reach its m)". The build computes b with F_2_symmetric(b, b, b) = λ̄ (tested to 8 ulp at every level), records b in the spec, and supplies λ̄ to the hazard. That is §2.2's equation evaluated once, not per cell per tick.
- **B5 (record convention).** §4.1: "tail = last 1,000 ticks in 10 non-overlapping windows of 100"; §4.11: "ρ̂ = tail-window mean density". The contract does not say pre- or post-update. The build takes the last 1000 post-advance states, ticks 2001–3000. It states the convention in the module docstring and keeps E1's column grammar.
- **B3** is unchanged.

*L1, 2026-10-26.*
