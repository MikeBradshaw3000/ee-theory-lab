# F8 M6 placement note (2026-10-30)

**Placed:** `mfa_instrument/f8/audit.py` `246d01a957994f3c55566011f895518dfb9a81066c57d378a5109267be65bf13`; `tests/test_f8_m6.py` `808b24dc3dcc1041e3e28de17884718b4e1edfc5a3f531a3a80020bea66c55ca` (55 tests) — the bytes L2 cleared SOUND in build review round 2 (`L2_F8_M6_BUILD_REVIEW_ROUND2_RECEIVED.md`), after round 1 DEFECT-WITH-REPAIR D1–D4 (`…ROUND1_RECEIVED.md`), both reviews received as byte copies. Generator declaration v0.3 `c73980585fc23820…` (v0.1, v0.2 retained) is a DRAFT for Mike's ratification with the governance record (M6-1…14); it is not frozen by placement. Declaration digests in source: audit `58693fafa1717b01…`, generator `dd0ff5ec51ff921b…`. Nothing in M1–M5, M-P1 or e1 is modified.

**`PLACEMENT_DATE = None` in the placed source.** Per declaration §9 / Interpretation 002 pt 8 the masters are 6/7/8 + the placement date; the literal is set in a later one-line commit once Mike ratifies M6-11 with the governance record, identity-checked against this placement (L2 r1 D2, r2 §3.2). Until then every production path refuses (measured: 55/55 in both sentinel states).

**Adapter payload identity:** measured on the canonical machine at placement and recorded in the suite record: `python -c "from mfa_instrument.f8 import audit as A; a=A.build_adapter(); print(a.payload_identity, a.body_sha256)"`; the container values were `597e39bd5093e51d…` / `fbb7efc99993bc1f…` (platform-sensitive through `exp`; M5 Appendix A discipline).

**Obligations recorded (L2 r2 §6, nonblocking), for the next L2-reviewed touch of these files, not applied to the cleared bytes:**
1. `test_dip_direct_function_with_an_empty_process_and_the_last_nonterminal_window` — its name/docstring says "forced w = 8"; the test does not force the selector (with the zero process consuming no draws, `default_rng(0).integers(0, 9)` returns 7). Cite it as direct-function floor and threshold-boundary evidence; L2 independently ran the forced w = 8 case (UNRESOLVED, terminal sum 14,200). At the next edit, force the selector or rename.
2. Declaration v0.3 §12 prose timings (210.3 / 207.4 s) differ from the captured record (213.70 / 211.17 s); cite the record. Correct in v0.4 at ratification.
3. M7 carries: Interpretation 002 identity, generator declaration tuple digest `dd0ff5ec…`, declaration v0.3/v0.4 identity, the adapter identity as measured on the canonical machine, the masters derivation record, and M3's `price_familywise` docstring obligation.

**Suite:** canonical suite on the pinned root, output `f8_m6_suite_2026-10-30.txt`, committed with this placement (expected: prior 760 passed, 2 skipped + 55 = 815 passed, 2 skipped, ≈ 60 min).
