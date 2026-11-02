# Flight 8 stage 1 — ratification record for the build declarations (v1.0, RATIFIED)

**Ratified by Mike, Theory Architect, 2026-11-02 ("As drafted")** on L1's v0.1 draft (57db4200613677f0…): every item in sections A–D below, including M6-7's (4s, 7s) reading, M6-4's floor, and D-date = 20261102, is of record from this commit. Section E's obligations bind M7.

**Purpose.** Every value the F8 instrument build (M1–M6, M-P1) declared as `[PROPOSED]` or "for ratification with the governance record", collected once, by name, with its source and the identity it binds. Mike ratifies each by name, as the freeze record (`16869692a043b139…`, §3) did for the contract's 26 PROPOSED values. Once ratified, this record is committed under `flights/mfa_fidelity/governance/f8_stage1/` and M7 cites it by identity; the `PLACEMENT_DATE` literal is set in the same act (item D-date).
**Repository pin:** `a487941` (M6 placed 2026-11-02; HEAD verified from a fresh clone). Nothing here changes any placed byte or the frozen contract (`e87277a2d11e948f…`).
**Status of the ⟂ marks.** They marked the items M7 depends on; all are now ratified.

---

## A. Masters (DERIVED@BUILD; contract §8, §5.3, §7.1) ⟂

| # | Master | Role | Declared in | Value |
|---|---|---|---|---|
| A1 | `F8_SEED_PANEL_MASTER` | canonical 20-seed panel (job 1 onward) | M1 `config.py` (B1, L2 M1 r2: "ratified only when the F8 governance record names M1's identity") | **20261026** |
| A2 | `F8_CALIBRATION_MASTER` | calibration panel (job 0, never scored) | M1 `config.py` | **120261026** |
| A3 | `VALIDATION_REPLICATE_MASTER` | null-validation attempt 1 (FAILED; retained immutable) | M3 `null.py` | **220261026** (record, not reusable) |
| A4 | attempt-2 `replicate_master` | null validation attempt 2 (PASSED under protocol 20ae18f0a85d9b6c…; ratified "Ratify" 2026-10-27 — restated here for completeness) | M3 `null.py` | **320261027** |
| A5 | `PROJECTION_MASTER` | finite-N design-stability sweeps (M5-2) | M5 `closure.py` | **420261028** |
| A6 | M-P1 corpus master | synthetic known-answer census (MP1-2) | M-P1 `evaluator.py` | **520261028** |
| A7 | M6 masters rule (M6-11) | design / held-out / pricing = 6 / 7 / 8 followed by the placement date | M6 `audit.py` `MASTER_PREFIXES`, `masters_for_date` | rule as stated; values fixed by **D-date** |

All distinct from one another and from E1's retired 20260917 and 202609221/2/3; `verify_frozen_identity` in each module checks its collision set.

## B. M5 declarations (closure and census; `closure.py` 9452dd11396350ab…) ⟂ for M7's package specification

| # | Declaration | Value | Source |
|---|---|---|---|
| M5-1 | dense census positions | **701** points over [250,000, 2,500,000] by round-half-even micro-units; the 24 pass-1 levels are NOT all among them (700 is not a multiple of 23) — disclosed; the reference of record is the dense grid alone | §4.8 [PROPOSED — E1's count]; L2 M5 r2 "for ratification" |
| M5-2 | design-stability ensemble | **200** sweeps, master 420261028 (A5) | E1's value carried; enforced (D1) |
| M5-3 | "alternative templates" (§4.8, carried E1 language) | read as **grid resolution (351 / 1,401 points) and solver independence (bisection vs Appendix A iteration, tol 1e-11)** under homogeneous inert bases; F8 has no template axis | L2 M5 r1 conditional → governance record |
| M5-4 | projected label from the stationary start π₁, 3,000 ticks, M2 geometry on the orbit | as built | L2 M5 r1 ACCEPTED (listed for completeness, no ratification needed) |
| M5-5 | record-kind mapping for M7's package spec | E1-R `tolerance_ensembles` ↦ F8 `ToleranceEnsemble` (one level's 20-seed calibration ensemble, both objects, ŝ and MDD); E1-R `tolerance_program` ↦ F8 `ToleranceProgram` (the census complete 24/24 with ceilings and stop path); kept as **separate kinds**, the mapping explicit | L2 M5 r1 D3 → "as repaired" |
| M5-6 | Appendix A binding tolerance | **1e-12** absolute on the fixed-point tables, Δm fields, m_lat; identity, level list, m_infl, π₁ exact; deviation reported (placement saw 5.55e-17 on `rho_sk[1.619565]`, Windows UCRT vs glibc) — and the **closure declaration digest change** that came with it (`11074edcacbe26d2…`) | L2 M5 r4–5 (D4 → SOUND); disclosure record f34fd281… |

## C. M-P1 declarations (`evaluator.py` 61179c7670ea8db3…; declaration digest cc1f176eb12dde34…) ⟂ for the M-P1 qualification of record

| # | Declaration | Value | Source |
|---|---|---|---|
| MP1-1 | synthetic census ŝ | **0.01** at every level (band ≈ 0.0119; noise amplitude 0.0054); a declared constant, not tied to job 0 (L1 recommended not; L2 accepted) | L2 MP1 r1 accepted |
| MP1-2 | corpus master | **520261028** (A6); a reduced or re-seeded run is not the record of qualification | accepted |
| MP1-3 | steep-continuous control | one adjacent rise of exactly 2·f_J × the branch's range at the first level above m_c, remaining rise rescaled to the endpoint (repaired per L2 r1 D5) | L2 r2 ACCEPTED |
| MP1-4 | reference level for ratio (iv) | the first pass-1 level ≥ m̂_c + Δm, with D7 reporting | accepted |
| MP1-5 | T-S1c domain | m̂_c … m_max inclusive | accepted |
| MP1-6 | edge flag for m̂_infl | set when an endpoint's one-sided slope exceeds the best interior central difference; gates nothing | accepted |
| MP1-7 | ratio-uncertainty convention | the ratio of two seed medians with the two calibrated widths k_R·ŝ(m)·1.2533/√20 stated separately; no propagated band, coverage or covariance claim (`RATIO_UNCERTAINTY_CONVENTION`) | L2 r2 ACCEPTED |

Also carried for the record: **F8 Interpretation 001** (6bf7304fd3ee287c…, ruled "A" 2026-10-29) and **002** (198d2991dd12168c…, ruled "E" 2026-10-30) — already of record; M7 carries both identities.

## D. M6 declarations (`audit.py` 246d01a957994f3c…; generator declaration v0.3 c73980585fc23820…; tuple digests audit 58693fafa1717b01…, generator dd0ff5ec51ff921b…) ⟂

| # | Declaration | Value | L2 disposition (r1/r2) |
|---|---|---|---|
| M6-1 | SUSTAINED source | reading E per Interpretation 002 — the count process of M5 `finite_n_counts`, stationary-null start | ruled; "technically acceptable" |
| M6-2 | NULL source | E at zero feedback (aggregate two-state chain), M6's own draw order | acceptable |
| M6-3 | DIP construction | nonterminal zero window w ∈ [0, 8]; terminal per-tick floor k_floor = ⌊idx_T/100⌋ + 1 = **142** → UNRESOLVED by support | acceptable |
| M6-4 | modulation floor | **r_floor = ρ*(m_min; η₀) = 0.066903** (stricter than π₁); enforced over the whole 362-key reachable surface (D1 repaired) | acceptable as a proposal |
| M6-5 | modulation ranges (proposal marginals) | D ∈ [−0.10, 0.10], drift minimum 2 % end-to-end; A_osc ∈ [0.05, 0.25]; P ∈ [50, 400]; A_att ∈ [0.5, 0.9]; M_sc ∈ [0.2, 0.4]; accepted distribution = conditioned on all preflight checks | coherent |
| M6-6 | redraw budget | **64** parameter attempts per sweep; exhaustion = generator halt | acceptable |
| M6-7 | two-crossing offsets | §5.2's "[4, 7] pass-1 spacings" read as the **fixed pair (4s, 7s) = (391,304, 684,782)** micro | coherent; **Mike's named confirmation required** |
| M6-8 | reachable adapter | 24 + 338 = **362** keys bound to the single M3 payload; production role by rebuild only; fail-closed; payload identity measured on the canonical machine (b37c7069e25a6166…, body df0834078c0343f0…; container 597e39bd… / fbb7efc9…) | acceptable |
| M6-9 | §4.3 price | **10,000** NULL replicates under the pricing master; event S_min > θ_P; exact CP-95 upper | event correct; count for ratification |
| M6-10 | job-0 comparison | method of declaration §8; **200** surrogate replicates per pass-1 level; values pending job 0 | acceptable |
| M6-11 | masters rule | 6 / 7 / 8 + placement date (A7) | coherent |
| M6-12 | wide width upper bound | ⌊1.6·w_U⌋ = **1,003,571** micro | implements the floor |
| M6-13 | width endpoints | lo = onset − ⌊w/2⌋, **hi = lo + w**; odd w: midpoint onset + ½ | accepted (D3) |
| M6-14 | reentrant onset range | **[347,826, 1,717,392]** = [m_min + s, m_max − 8s], §6.4's shared row | accepted (D4) |

**D-date. The placement date.** `PLACEMENT_DATE` → **20261102** (ratified) (the M6 placement commit `a487941`, 2026-11-02), giving masters **620261102 / 720261102 / 820261102**. Set by a one-line commit to `audit.py` whose only change is that literal, identity-checked by diff and by the 55-test module in the established state (L2 r1 D2 / r2 §3.2). No master is drawn before this record is committed.

## E. Obligations this record carries to M7 (not ratifications; listed so nothing is lost)

1. M7 is the sole issuer of the canonical job-0 census role (M5 issues `derived_provisional`).
2. The verdict of record is evaluated on the final level set (M4 obligation; M6 does this per sweep — M7 verifies on the record).
3. Remove `NullValidation.is_qualification_evidence()` (M3, "kept for one round").
4. `null.py` docstring names `price_familywise`, which does not exist — the price is `s_min_rejection_rate` (Interpretation 002 pt 9a); repair at the next L2-reviewed touch of M3.
5. The null-validation protocol identity 20ae18f0a85d9b6c… travels with its decision; attempt 1's FAILED record retained; the α-0.05 pairing disclosure (0.0445 > 0.0429 at module default) travels into the governance record.
6. M-P1's qualification of record is M7-issued on the canonical machine (container 900/900 is build evidence only).
7. Interpretation 001 and 002 identities; generator declaration tuple digest and the Markdown declaration's identity (v0.3, or v0.4 if the timing-prose correction is made); the adapter identity as measured on the canonical machine, read from a clean ASCII JSON (the suite record's appended lines are UTF-16 with CRs — legible, immutable, not to be parsed).
8. L2 r2 §6.1: the direct-DIP test's docstring overstates "forced w = 8"; fix at the next edit of `test_f8_m6.py`. L2 M-P1 r2 §5(b): stale comment at the below-boundary rise test in `test_f8_mp1.py`; fix at its next edit.
9. Cross-platform: adapter payload identity, M5's Appendix A deviation, and any exp()-derived field are recorded as "what the canonical machine saw"; the integer indices and declaration digests are the cross-platform identities.

## F. What this record does not do

It authorizes no run, draws no master, and changes no placed byte. Ratification of M6-1…14 freezes generator declaration v0.3 (or v0.4 with the prose-timing correction only) as the declaration of record; qualification (§7.1 order: M3 cache → M-P1 known-answer → masters → M6 design → held-out → `m6_audit_qualification`) and the canonical jobs each retain their own authorization.

*L1 draft v0.1 2026-11-02 from the committed objects at `a487941`; v1.0 after Mike's ratification the same day. The `PLACEMENT_DATE` literal is set in the commit that places this record.*
