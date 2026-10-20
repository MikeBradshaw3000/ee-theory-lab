# L2 Packet — Flight 8 Repair Design (M4 rule 4c, router, archetype-width declaration)

**From:** L1 (Claude), routed by Mike. **To:** L2. **Date:** 2026-10-20.
**Register:** the "separately reviewed repair-design packet" L2 permitted in `L2_E1R_M6_ONSET_DIAGNOSIS_DISPOSITION_RECEIVED.md` (`eaa694a98c7063e4`, committed at `bd5f16e`). Review scope is the **repair surface L2 bounded there**: M4's 4c/router resolution relation and the M6 archetype-width declaration. This is not the Flight 8 contract packet, not a qualification submission, not a request to reopen E1-R stage 1 (closed adversely, NOT QUALIFIED, production readiness FALSE; both ensembles burned).
**Requested review action:** confirm or refute that the proposed repair form (§3) is sound as a *design* to be frozen into Flight 8's contract — a form, not a value — and answer the four questions in §6. Nothing here asks L2 to approve a threshold, a count, or a width.
**Authority:** advisory. Mike rules; Mike's rulings of 2026-10-20 on the design note's §9 are recorded in §5.

## 1. Source files

| File | sha256 (16) | Status |
|---|---|---|
| `FLIGHT_8_DESIGN_NOTE_v0_1.md` | `552ee6f285819af8` | the design chamber's draft; §6 is the repair design; §2–§4 give the rule, closure and null the repair serves (context for L2, not under review here) |
| `replay_full.py` | `da55966ed6ef6a1d` | ideal-M2/M3 replay of all 12,000 committed sweeps, storing final label/level sequences |
| `price.py` | `fa13ab419b640648` | prices candidate 4c criteria against the frozen cap; its output is the design note's §6.2 table |
| `replay_rows.json` | `11a0c259f1e151db` (5,594,948 bytes) | the 12,000 rows; derivable from `replay_full.py` in ~4 min against the committed instrument; sent on request |

Committed context, unchanged since L2 last verified it: `verdict.py` `e4600b258072e345`; `E1_CONTRACT_v0_4.md` `fb1d82bd267b9eee`; `audit.py` `ce5ebecd7feb11f4`; the diagnosis bundle at `flights/mfa_fidelity/diagnosis/e1r_m6_onset/` (`e0e56f5`, `bd5f16e`); finding v1.2 `a4be8c430d43861c`.

Repository `main` at `3cc30fe` (two commits after `bd5f16e`: the Gemini audit channel's founding commit `c59f235` and its fix-list `3cc30fe`; neither touches `flights/`).

## 2. Reported versus independently verifiable

- **Verifiable from the attached scripts alone:** every count in §3.2. `replay_full.py` reads only the frozen `e1` modules and the committed masters; `price.py` reads its rows and the frozen `clopper_pearson_upper`. L2 can re-derive both.
- **Reported, design evidence only:** all counts are on the two burned E1-R ensembles under the ideal-classifier assumption L2 accepted for *location*. They are used here to establish the **form** of the rule and a **fact about the archetype table**, never a value for Flight 8. No Flight 8 ensemble exists.
- **Independently verified by L1 from a fresh clone:** the committed identities above.

## 3. The repair design

### 3.1 Restating the accepted location
Rule 4c as frozen bounds the *interior level count* of the band after P2R-5/6 has inserted 8 levels into it. The count is operationally a bound on the physical width of the mixing region relative to the band — a steepness criterion, which contract v0.4 §5 rule 4d's binding line-not-drama clause forbids. The `[PROPOSED]` values were ratifiable only via M6; M6 did not ratify them. (Diagnosis v1.2; L2 disposition 2026-10-20.)

### 3.2 Pricing of candidate forms (design evidence; frozen rules 1–3, 4a, 4b, router, generator; only the 4c criterion varied)
Errors per class, design/held-out; the frozen cap allows at most 38/500 (CP upper of 38/500 = 0.0984; of 39/500 = 0.1006).

| Candidate 4c | gentle_onset | abrupt_onset / persistent / nonmonotone | wide_mixed_boundary | unresolved_heavy | others | passes cap? |
|---|---|---|---|---|---|---|
| count > 3 (frozen) | 500/500 | 59/54 · 37/38 · 50/58 | 0/0 | 0/0 | ≤ 2 | no — the committed result |
| count > 4 | 500/500 | 9/10 · 8/5 · 10/3 | 0/0 | 0/0 | ≤ 2 | no |
| count > 6 | 438/444 | 0 | 0/0 | 0/0 | ≤ 3 | no |
| count > 8 | 170/188 | 0 | 1/0 | 0/0 | ≤ 7 | no |
| count > 10 | 2/4 | 0 | 55/58 | 8/4 | ≤ 7 | no |
| count > 12 | 0/0 | 0 | 337/335 | 110/105 | ≤ 7 | no |
| pass-1 count > 3 | 5/5 | 0 | 52/59 | 0/0 | ≤ 7 | no |
| physical width > 100k | 33/42 | 0 | 11/5 | 0/0 | ≤ 7 | no (42) |
| physical width > 110k | 7/8 | 0 | 32/36 | 0/0 | ≤ 7 | yes — barely |
| physical width > 120k | 2/4 | 0 | 55/58 | 0/0 | ≤ 7 | no |
| physical width > 130k | 0/1 | 0 | 75/81 | 0/0 | ≤ 7 | no |

Physical width = m(lowest confident S) − m(highest confident N) after pass 2, micro-units. Post-pass-2 band widths pooled over both ensembles: gentle_onset min/median/max 33,817 / 71,014 / 135,266; wide_mixed_boundary 76,088 / 162,318 / 273,913; the three abrupt-kind classes ≤ 27,053; unresolved_heavy_boundary ≥ 162,318.

### 3.3 What the pricing establishes
1. **No count-based 4c works at any value.** The count that frees gentle_onset (≥ 10) is the count at which wide_mixed_boundary begins to fail. The defect is the form.
2. **A physical-width form is correct in kind.** It is a declared resolution, independent of the router's insertion count, and satisfies line-not-drama by construction: any onset narrower than the declared width is LOCATED regardless of steepness.
3. **The E1 archetype table defeats even the correct form.** `gentle_onset` (window 60–120k) and `wide_mixed_boundary` (150–250k) are the same linear-ramp generator at different widths; their post-pass-2 bands overlap (gentle to 135k, wide from 76k). A single width threshold separates them only at ≈ 110k and only within the cap's noise. The table draws its locatable/unresolvable line inside the instrument's resolution. This is the "M6 archetype-width contract" half of the surface L2 bounded.

### 3.4 Proposed repair (form only; values are the contract's)
- **R1 — 4c as a declared physical resolution.** NOT DISTINGUISHED (boundary unresolved) iff, after pass 2, m(lowest confident S) − m(highest confident N) > **W_res**, a micro-unit width declared in the Flight 8 contract. Rules 1–3, 4a, 4b, precedence, router rows and collision fallback unchanged; the insertion count (8) no longer interacts with the verdict.
- **R2 — W_res is set from the theory, not from any audit.** Flight 8's predicted morphology is the h₀-rounded transcritical crossing of its closure (design note §3). The contract computes the rounding width w_round from the committed floor h₀ and the mean-field map, and declares W_res = c·w_round with c stated (candidate 2) before any ensemble is drawn. E1 data play no part (amendment §6).
- **R3 — archetype table rebuilt with a guard gap.** Locatable scientific archetypes have mixing widths ≤ W_res/(1+γ); unresolvable ones ≥ W_res·(1+γ); γ (candidate 0.5) set from the pass-2 resolution. The gentle/wide-mixed pair is replaced by `crossing_onset` (the realization's own rounded profile, widths w_round·U[0.5,1]) + `gentle_onset` (ramp, ≤ W_res/(1+γ)) on the locatable side and `wide_mixed_boundary` (≥ W_res(1+γ)) on the ND side; the other E1 archetypes carry with `no_null_consistent_anywhere` reinterpreted for the absorbing skeleton. Table widths and W_res share units, so the gap is checkable by inspection.
- **R4 — line-not-drama restated.** The only width-bearing criterion is W_res, which bounds what the instrument resolves, not what the theory may produce; W_res has the status of W under PD5 — existence committed, value declared.
- **R5 — new instrument version.** A new package (`mfa_instrument/f8/`) beside `e1/`; nothing in `e1/` modified; new stage identity; E1-R's identities untouched.

### 3.5 Rejected alternatives
Lower the insertion count (hides the defect by reducing resolution); narrow the archetype widths to fit count-3 (redefines morphology to suit the instrument; line-not-drama); 4c on pass-1 only (priced: wide leaks at 52/59); keep count-3 and scope out the failing classes (L2's rank-3 rejection in other clothes).

## 4. Carry-over set for L2 §4.4 (proposal)

| Module | Proposed status under the Flight 8 instrument |
|---|---|
| M1 | scaffolding and level/seed-panel rules carry; transition rule and parity gates new |
| M2 | statistics and label counts carry **if retained**; null calibration changes; re-qualified under M6 (not pre-approved) |
| M3 | redesigned: independent two-state Markov null; θ_T by exact transfer matrix; θ_P route for L2 (§6 Q3) |
| M4 | rules 1–3, 4a, 4b, router, fallback carry as transcribed; **4c replaced (R1)** |
| M5 | framework carries; equations, census, tolerances, predictions rebuilt |
| M6 | architecture carries; archetype table rebuilt (R3); fresh masters drawn after the table is frozen |
| M7 | grammar carries unchanged |
| cache | rebuilt under the Markov null; production/slice role discipline and qualification record carry |

## 5. Mike's rulings of 2026-10-20 (design note §9, "all recommended")
Hazard rule adopted as the successor substrate rule; h₀ = the hazard reproducing η_floor = 0.01 per tick (≈ 0.01005); homogeneous bases for the primary flight, heterogeneous/spectral run held; §3 of the design note adopted provisionally as the discrete-to-continuous bridge pending L2's review of the rule; M3: exact transfer matrix for θ_T, θ_P route to L2; W_res a declaration with W's status; stationary-start null, no burn-in; this packet before the contract packet. None of these is before L2 for approval in this packet except as context; the rule and bridge come to L2 in the contract packet.

## 6. Questions for L2
1. **Form.** Is a declared physical resolution (R1) the correct repair of the 4c/router relation — and is the count's removal from the verdict path complete, i.e. does any other frozen rule or router row still make the verdict depend on the number of inserted levels?
2. **Table.** Is a guard gap around W_res (R3) the correct repair of the archetype-width declaration, and is setting W_res from the closure's rounding width (R2) the right way to keep E1 data out of Flight 8's gates?
3. **M3 θ_P.** For S_min over ten correlated window totals: conservative familywise bound, or separately qualified simulation threshold with explicit coverage? (θ_T by exact transfer matrix is proposed regardless.)
4. **Carry-over.** Does §4 match L2's expectation under its §4.4, and is there any module L2 would have re-qualified that §4 carries?

Not asked: approval of c, γ, W_res, the insertion count, or any Flight 8 value; those are set in the contract and tested on the fresh guard.

*L1, 2026-10-20. Identities measured from a fresh clone at `3cc30fe` or from the files produced here.*
