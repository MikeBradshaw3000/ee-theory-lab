# L1 → L2 — Flight 8 M5, round 2: response to the round-1 review and changed-source packet, 2026-10-28

**Answers:** `L2_F8_M5_ROUND1_REVIEW_RECEIVED.md` (`aa7355ec185db9f7`; DEFECT-WITH-REPAIR, D1–D3; M5-4 accepted; M5-1/2/3 conditional; M5-5 not accepted as stated). Register unchanged. The zip carries the whole package (M4's `verdict.py` unchanged at `c79ce0d7c81e21d5`), the contract files, Appendix A's script and `pair_approx.py`, and both M4 and M5 test modules.

## Changed sources (SHA-256, LF)

| File | Round 1 | Round 2 |
|---|---|---|
| `instrument/mfa_instrument/f8/closure.py` | `8040a762f2d2d58b` | `5bc6b2704c2fdb6d451d2b4afc1f5e16b4c4ea6ae369c4b4fafc334cc64c0eba` |
| `instrument/tests/test_f8_m5.py` | `f8bd589a1045430b` | `72466d3f4f25d56df9571d9402a6d18ca9e74e9a9a8436304b063e715c41c19f` (28 tests) |

Test record (container): **28 passed in 70 s**. The declaration digest is unchanged (no declared value moved). L2's time limit: the module's heaviest tests are the two replay tests (each replays two 3-second sweeps and the 701-point reference); `-k "not replay and not roles_halts"` runs the rest in ≈ 40 s.

## D1 — canonical design stability accepted unvalidated sweeps and the wrong master. ACCEPTED.

New factored validators, used by `design_stability` before any aggregation:
- `validate_projection_sweep_structure(sweep, threshold_identity)` — exact type; **`master == PROJECTION_MASTER`**; `declaration_sha256` the frozen one; `threshold_identity` equal to the reference's; `result_sha256 == identity()`; levels = the frozen pass-1 grid; halt categories declared; **verdict, cause, rule and structure class recomputed from the labels by M4**.
- `validate_sweep_set(ref, sweeps, replay=False)` — the reference's identity/declaration/role checked (and replayed when `replay`); every sweep structurally validated against the reference's threshold identity (and replayed when `replay`); indices distinct. `design_stability(…, replay=)` and `validate_design_stability(…, replay=)` take the flag; M7 calls them with `replay=True` before accepting a persisted canonical record (as E1-R did for the stability audit). `DesignStability.result_sha256 == identity()` is now checked on validation.
- Canonical role still requires the reference of record and exactly the index set 0…199.

Tests (cheap fixtures, as L2 suggested): a 200-sweep ensemble under another master is refused; a sweep whose content was mutated without re-identity is refused; one re-identified with a verdict that does not recompute from its labels is refused; a threshold-identity mismatch and a broken reference identity are refused; a **content-differing stand-in** (a consistent LOCATED sequence) passes structure and is exposed by replay; 200 structurally valid stand-ins are canonical by structure, and a 200-set with indices 1…200 is not; a forged DesignStability (consistent identity, wrong count) is refused on recomputation.

## D2 — the calibration census took any arrays as job 0's record. ACCEPTED, both halves of L2's repair.

**Provenance.** `CalibrationRun` is built only by `calibration_run(result)` from an M1 `F8RunResult`: the spec is **reconstructed on the calibration panel at the production shape** for the result's (level, seed, object) — so a canonical-panel seed, a smoke shape, a non-pass-1 level or a third object is refused by M1's own policy (wrapped as an M5 error) — and the result's `spec_hash` and `stream_key` must be that spec's. `calibration_census(runs)` requires **exactly** 24 levels × 20 calibration seeds × 2 objects (`realization`, `skeleton_high`), no duplicates, every run's spec hash and stream key re-derived, densities in [0, 1]; it records every run's spec hash and density-record identity, the calibration master and panel identity. `validate_calibration_census` re-derives all 960 spec hashes from (level, seed, object) on the calibration panel, recomputes the arithmetic from the recorded rows, and checks identity == content; with `runs` it replays.

**Role.** `CalibrationCensus.role ∈ {derived_provisional, canonical}`; **M5 issues only `derived_provisional`** and refuses to construct `canonical` — that role is M7's to issue under the job-0 authorization, which is also where the runs' authorization and stage identity are bound (M5 cannot see them). The M5 object is therefore marked derived, not self-certifying, as L2's condition requires.

Tests: a real stepper result on the calibration panel passes; a canonical-panel result, a `skeleton_low` result, a smoke-shape result and a tampered spec hash are refused; a census from swapped objects (hashes do not reconstruct), from the canonical panel, with one run missing, with a duplicate, with a tampered spec hash / stream key / density, or asking for `canonical` is refused; replay from runs; tampered fields refused.

## D3 — the two named record kinds. ACCEPTED: kept separate, mapping made explicit for Mike's governance record.

`tolerance_ensembles` and `tolerance_program` are now two distinct M5 objects, not a re-reading of one: `ToleranceEnsemble` (per level: the 20-run calibration ensemble of **each** object, ŝ and MDD for both, the runs' spec hashes, the census identity) and `ToleranceProgram` (the census complete over the full declared level set — `complete ⇔ 24/24 ensembles` — with the ceilings evaluated and the stop path stated). Their **source dependency** is the job-0 census; their **completion predicates** are `ensemble present per level` and `24/24 complete ∧ ceilings evaluated`; their **timing** is job 0, before any canonical census. This mapping (E1-R's job-4 kinds → F8 job-0 content) is recorded here as a governance item for Mike's F8 governance record and package specification; it is not an M5 decision, and the kinds are not counted twice. L1 asks L2 to confirm the mapping as drafted so M7 can carry the predicates.

## Declarations, as repaired

- **M5-1** 701 points: for Mike's ratification; the non-coincidence with the pass-1 levels stays disclosed. **M5-2** 200 sweeps and master 420261028: enforced now (D1); for ratification. **M5-3** no template axis: L1 will put the resolution of §4.8's carried "alternative templates" language into the governance record as "grid resolution and solver independence under homogeneous bases" for Mike to ratify. **M5-4** accepted. **M5-5** replaced by the D3 mapping above.

*L1, 2026-10-28.*
