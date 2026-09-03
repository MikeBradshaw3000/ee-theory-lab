# Gate B Specification v0.4 — Changed-Text Layer over v0.3
**Status:** DRAFT for L2 changed-text verification (Phase-2, packet 4). Carries v0.3 in full except Amendments 4 and 6, replaced below per L2's packet-3 repair set (items 1–4). Amendments 1, 2, 3, 5, 7, 8, 9 stand corrected-as-required and are not reopened; L2's implementation-stage conditions (prospective solved-offset enumeration before qualification; mutant-30 frozen-input determinism and window coverage shown at source review) are entered on the harness obligations ledger.
**Author:** L1, 2026-08-27.

## Amendment 4R — tie-valid gross-divergence screen (replaces v0.3 A4 entirely)

The v0.3 stable-order construction is **withdrawn**: the terminal statistic is discrete (lattice spacing 1/250,000), ties are not measure-zero (observed in 3,759 of 4,000 forecast experiments), and the withdrawn convention was tie-order dependent, alarming on identical samples in the degenerate case.

**Frozen screen (exact conditional permutation KS):**
- **Statistic:** with F̂(v) the right-continuous ECDF (P(X ≤ v)) of each 20-run sample, evaluated at each **unique pooled value**: D_int = max over unique-value prefixes of |2a − s|, where a = candidate observations ≤ v and s = pooled observations ≤ v. Tie-invariant by construction; within-tie ordering cannot enter.
- **Null:** the exact conditional permutation distribution of D_int **given the observed tie-block sizes** — all C(40,20) label assignments, computed by dynamic programming over blocks with state (candidate labels used, max-so-far), weights ∏ C(b_i, c_i).
- **Alarm rule:** p = P(D_int ≥ observed | tie blocks); **alarm iff p ≤ α_KS = 0.00125** (boundary inclusive, frozen). Familywise: Bonferroni across the eight cells from budget 0.01; each conditional test is exact level ≤ α_KS, so the family bound holds unconditionally.
- **No-tie reduction (verified):** with all-singleton blocks the statistic and pricing reduce exactly to the v0.3 rule — P(D_int ≥ 12) = 0.0011158 — so the repair strictly generalizes rather than replaces the calibrated behavior. Identical samples yield D_int = 0, p = 1: no alarm, correctly.
- Any alarm halts Gate B with the atomic failure record; the alarm layer is priced in the Amendment-6R forecast.

## Amendment 6R — joint forecast under the repaired screen + reproducibility record (replaces v0.3 A6)

Design unchanged (200 forecast seeds 401–600; 4,000 pseudo-experiments; disjoint 20 v 20 panels, same panel across all eight cells; full family jointly). **Recomputed under Amendment 4R** — the v0.3 figure is retired, not promoted.

**Provisional record (this packet, Part III; PROVISIONAL, py3.12.3):** TOST all-8 pass **4000/4000**; KS no-alarm **3977/4000** (50 alarms over 32,000 cell-tests; 3,759 experiments contained ties); **FULL-GATE 3977/4000 = 0.9942**; power vs 0.005 mean divergence, worst-SD cell: **4000/4000 fail**. Integer counts of record, not rounded rates.

**Reproducibility fields (mandatory in the canonical record):** runner source digest; analysis RNG = NumPy default_rng(0x7A9B31C) (PCG64); panel algorithm = choice(200, 40, replace=False), first 20 candidate-role, last 20 reference-role, panel shared across cells; Welch TOST exactly per Amendment 3; screen exactly per Amendment 4R; integer pass/alarm/failure counts; environment stamp; pinned-source digest verified in-run.

**Pre-freeze requirement:** this forecast reruns on the canonical environment with the identical runner; the canonical record, not this provisional one, supports the freeze decision.
