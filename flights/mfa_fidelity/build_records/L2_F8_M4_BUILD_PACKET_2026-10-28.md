# L1 → L2 — Flight 8 instrument module M4: build packet (round 1), 2026-10-28

**Register.** Instrument build review under Contract F8 v0.8.4 (FROZEN, `e87277a2d11e948f`). Verdict SOUND / DEFECT-WITH-REPAIR. Nothing placed until L2 clears and the canonical suite passes on Mike's machine; no run authorized. M1–M3 are placed at `7023916` (M2/M3 L2 SOUND round 4). The zip carries the whole `mfa_instrument` package at `7023916` plus the two new files, the contract, freeze record and Appendix A at repository paths; tests run from `flights/mfa_fidelity/instrument`.

**Scope (contract §4.4–§4.7, §6.2).** The verdict function and the pass-2 router. Everything is carried **verbatim** from E1's M4 (the 2026-10-20 diagnosis implicated none of it) except **rule 4c**, which the contract replaces.

## Files (SHA-256, LF)

| File | Identity | Status |
|---|---|---|
| `instrument/mfa_instrument/f8/verdict.py` | `c79ce0d7c81e21d5a9c036e2957a436a6eaa4a8e6f19dddb8e6cae89372537d2` | new (M4) |
| `instrument/tests/test_f8_m4.py` | `8b8976b2c3602e0cc3932676cc6a091c69569af515bc183c374208578afa6d12` | new, 17 tests |

Test record (container): **17 passed** in 8 s. No other file changes; `e1/` untouched (its M4 declaration digest and `BOUNDARY_SPAN_LIMIT = 3` are asserted unchanged by a test).

## What carries verbatim (and how that is checked)

Rules 1, 2, 3, 4a, 4b; precedence 1 > 2 > 3 > 4 and a > b > c > d; `OFF_BAND_U_ALLOWANCE = 2`; router rows P2R-1…P2R-7 with 8 insertions in P2R-5/6 and 4 + 4 in P2R-4; `evenly_spaced_interior` (round-half-to-even, exact integer micro-units); `_resolve_collisions` (move to the round-half-even midpoint of the accepted neighbours within the interval, else drop; every action recorded); the reachable-surface derivation of the collision audit; the dead rows P2R-3/4/7 asserted by test. The test module feeds identical label patterns to **E1's own router on E1's grid** and F8's on F8's grid and requires equal rows and equal interval *indices*; the arithmetic helpers are checked equal on shared inputs. The archetype table's twelve names and intended verdicts are the contract's §5.2 (E1's set; the 4c cause renamed).

## What changes: rule 4c (contract §4.4)

> 4c (F8). NOT DISTINGUISHED (boundary unresolved at declared resolution W_res) iff, after pass 2, the measured width of the band — m(lowest confident S) − m(highest confident N) on the final level set — exceeds W_res (§4.5). Otherwise 4d: LOCATED, bracket [m₋, m₊].

Implemented as `width = levels[hi] − levels[lo]`; `width > W_RES_MICRO` → 4c with cause `boundary_unresolved_at_W_res`; else 4d. W_res = 293,478 = 3 s, taken from M1 and checked equal at every preflight. E1's `BOUNDARY_SPAN_LIMIT` (a level count) does not exist in the module. The evidence carries the measured width and W_res on both branches. `measured_band_width_micro` and `final_level_set` (pass-1 levels ∪ kept insertions) are provided for M7.

**Tests on 4c:** a pass-1 band of exactly 3 spacings (= W_res) is LOCATED (strict `>`); 4 spacings is 4c; the same label pattern on a denser final level set, where the inserted levels narrow the band to one insertion-gap pair (< W_res) while **three** interior levels remain uncertain, is LOCATED — the case E1's count-based rule would have read against its limit of 3. `inspect.getsource(evaluate)` contains none of "slope / jump / monoton / amplitude / separation" (§4.7).

## Totality

For every one of the 4⁷ = 16,384 label sequences on a 7-level sub-grid straddling m = 1, `evaluate` equals an **independent reference transcription of §4.4** written in the test module (rules 1–3, 4a, 4b, 4c-as-width), rule by rule and cause by cause; every rule fires on some sequence; a bracket exists iff LOCATED and its width ≤ W_res.

## Appendix A reproduced from the router's own arithmetic

`routing_slack_table(9)` — Appendix A's procedure: every band of B spacings, eight round-half-even insertions, collided candidates **removed** (worst case), final set = pass-1 levels in the band ∪ kept insertions, Δ_route(B) = 2 × largest final gap — returns **21,740 / 43,480 / 65,218 / 86,958 / 108,696 / 130,436 / 152,174 / 173,914 / 195,654**, equal to Appendix A's table and its JSON (`verify_against_appendix_a` reads the committed file, checks its identity `94d52762…`, and compares); max over B ≤ 4 = 86,958 at B = 4. `collision_audit`: 276 reachable bands, 84 colliding, exactly at **B ∈ {3, 6, 9, 12, 15, 18, 21}** (Appendix A's `collision_B`); the proof does not close; the fallback is live and is exercised in a test (band 0.25 → 0.5435: two candidates collide, both moved, eight distinct interior insertions result). The live router moves/drops; the audit removes, as Appendix A does; both are reported.

## Declarations for L2 (none pre-approved)

- **M4-1 Cause token.** The contract's 4c verdict reads "boundary unresolved at declared resolution W_res"; the token is `boundary_unresolved_at_W_res` (E1's `boundary_unresolved` is not reused, so a record cannot be mistaken for E1's count-based verdict). The §5.2 table's two 4c classes carry this cause.
- **M4-2 "After pass 2".** `evaluate` is a pure function of (labels, levels); the contract's "after pass 2" is a protocol fact M7 enforces by evaluating the verdict of record on `final_level_set`. At pass 1 the same function drives the router, as in E1.
- **M4-3 Reachability unchanged.** On the F8 grid the reachable rows remain P2R-5/6 only; P2R-3/4/7 dead, as E1's record states.

*L1, 2026-10-28.*
