# NONCANONICAL DIAGNOSIS — Where the E1-R M6 onset-class failures arise

**Register:** bounded diagnosis phase under L2's successor conditions (`L2_E1R_M6_QUALIFICATION_RESPONSE_RECEIVED.md` `3f101a1b…` §4.2, §10: "a successor repair should begin with a bounded diagnosis phase rather than immediately changing M4") and Flight 8 contract condition 1 (handoff `SESSION_HANDOFF_2026-10-15_v2.md` `a3b0a427…` §4). **This document and every file beside it are NOT results of record.** Nothing here is canonical, nothing here is an authorization, nothing here specifies a repair. It is a finding about the committed E1-R stage-1 audit records, routed to L2 for confirmation before any M2/M4 change is specified for Flight 8.
**Ruling context:** Mike ruled 2026-10-15 (this chat's first act) for Flight 8 directly, not a successor E1 stage, with the three contract conditions. This finding discharges condition 1.
**Drafted by:** L1, 2026-10-15. **Decision authority:** Mike. **Does not reopen** E1-R stage 1 (`dc8b1a6b…`, closed adversely at `3ab65df`; production readiness FALSE).

---

## 0. The finding in one paragraph

All four onset-class failures arise in **M4's rule 4c as frozen** — the `[PROPOSED]` contiguous-uncertain-span limit of 3 levels, counted *in levels* and applied *after* the P2R-5/6 router has inserted 8 new levels into the band. Pass 1 located the threshold on **495/500 gentle-onset sweeps and 500/500 of each of the other three classes** in both ensembles; pass 2 then reversed those verdicts to `NOT_DISTINGUISHED (boundary_unresolved)` by densifying the band without changing the physical width of the mixing region. The effect is deterministic in the generator's geometry: an exact arithmetic replay of all 12,000 committed sweeps, assuming M2/M3 classify every run's regime correctly and consulting no run and no threshold, reproduces the committed error counts to within 0–3 sweeps per class per ensemble (gentle 500/500 both; abrupt 59/59 and 54/56; persistent 37/39 and 38/41; nonmonotone 50/51 and 58/58), and a 100-sweep end-to-end realization with the production cache agrees with the arithmetic replay on **100/100 final verdicts and rules**. M2, M3 and the qualified threshold cache contribute at most the residual (≤ 3/500 per class), which is verdict-neutral in the realized sample. The rule-4c/router combination is also what *correctly* holds `wide_mixed_boundary` to ND (pass 1 locates 52/500 and 59/500 of those; pass 2 catches every one), so the defect is a **resolution conflict between the archetype table's declared onset widths and a count-based span limit after densification**, not a transcription error in any module. As frozen, rule 4c is operationally a minimum-steepness criterion, which the contract's binding line-not-drama clause forbids (E1 v0.4 §5 rule 4d; v0.1 §LOCATED; v0.2 §LOCATED).

---

## 1. Inputs (committed, read-only; nothing reconstructed from memory)

Fresh clone of `MikeBradshaw3000/ee-theory-lab` at `60d6c59` (one commit past `18e86cd`; the commit of the v2 handoff). Identities measured from the clone (sha256, 16 hex):

| File | Identity | Role |
|---|---|---|
| `flights/mfa_fidelity/artifacts/e1/stage1/m6_design_audit.json` | `f3383e1be0835e64` | the committed record under diagnosis (master 202609221) |
| `flights/mfa_fidelity/artifacts/e1/stage1/m6_held_out_audit.json` | `f2340c82067b1c92` | the committed record under diagnosis (master 202609222) |
| `flights/mfa_fidelity/artifacts/e1/stage1/m6_audit_qualification.json` | `be65d972ef49f714` | NOT QUALIFIED, 10 reasons |
| `instrument/mfa_instrument/e1/audit.py` | `ce5ebecd7feb11f4` | M6 generator + scoring (L2's custody identity) |
| `instrument/mfa_instrument/e1/verdict.py` | `e4600b258072e345` | M4 verdict function + P2R router |
| `instrument/mfa_instrument/e1/classify.py` | `db94bbe0c26d7494` | M2 run status + level label |
| `instrument/mfa_instrument/e1/null.py` | `58c1104a9a5a78da` | M3 conditional null |
| `artifacts/e1/threshold_cache_qualified.json` | `608844ff7bd636d5` | production cache (file identity named by both audit records; body `4659b062…`) |
| `artifacts/e1/threshold_cache_qualification.json` | `5c933778c0a8f105` | its qualification record |
| `contracts/e1/E1_CONTRACT_v0_4.md` | `fb1d82bd267b9eee` | §5 verdict function and router as transcribed |
| `contracts/e1/E1_CONTRACT_v0_8.md` | `d6db7a7d41b2ca6f` | pass-2 arithmetic (C/E) |

Environment: Linux container, Python 3.13.16, numpy 2.4.4, pandas 3.0.3, pyarrow 24.0.0 (the three pins of the twenty that the instrument imports; the rest of the twenty-pin environment was not reproduced — see §6).

## 2. The mechanism, read from the frozen code

1. **Generator geometry (M6, `audit.py` `regime_at`).** For every onset-type archetype a sweep draws an onset `o` and a width `w` (gentle: `w ∈ [60k, 120k]` micro; abrupt-kind — `abrupt_onset`, `persistent_nonstationary_high_m`, `nonmonotone_amplitude` — `w ∈ [0, 20k]`; wide: `[150k, 250k]`). At level `m` each of the 20 seeds is SUSTAINED iff its fixed per-sweep uniform `u_s < frac(m)`, where `frac` rises linearly from 0 at `o − w/2` to 1 at `o + w/2`. The "onset" is thus a **mixing window of physical width `w`** in which seeds disagree.
2. **M2 labels** a level `S` (≥16 sustained, ≤2 null), `N` (the reverse), `M` (≥4 of each), else `U`. Inside the window, where `frac` is away from 0 and 1, the level is `M` by construction.
3. **Pass 1** samples 24 levels at spacing ≈ 30,435 micro. A gentle window (60–120k) contains 1–4 pass-1 levels; an abrupt window (≤ 20k) contains 0 or 1. Rule 4c passes (span ≤ 3), so pass 1 is `LOCATED` for essentially every sweep.
4. **Router P2R-5/6** inserts **8 evenly spaced interior points** into the band (the open interval between the highest confident `N` and the lowest confident `S`), spacing ≈ band/9.
5. **Rule 4c, evaluated again on the 32-level sequence,** recomputes the band and counts the levels strictly inside it: `span = len(inside)` (`verdict.py` `evaluate`, "every interior level is uncertain by construction of the band"). The densified levels that fall inside the mixing window are `M`; the span is now ≈ 9·w/B (`B` = pass-1 band width) plus whatever pass-1 levels were already inside. With the limit at 3 and the pass-1 band typically one or two spacings wide, any window wider than roughly 10–20k micro exceeds the limit → `NOT_DISTINGUISHED (boundary_unresolved)`.

Hence: gentle (`w ≥ 60k`) **can never pass**; abrupt-kind passes iff `w` is small relative to the band; the error rate is a deterministic, monotone function of `w`.

## 3. Arithmetic replay of all 12,000 committed sweeps (`predict_labels.py`, `98b6455b…`; rows `predicted_rows.json`, `4b349809…`)

For every class, every sweep index 0–499, both masters: reproduce the frozen parameter draw (`draw_params`, same redraw stream) and the per-seed regime uniforms (first 20 draws of `SeedSequence([master, class_index, sweep_index])`, exactly as `run_sweep` draws them); map each seed's regime to its intended run status (SUSTAINED→`SUSTAINED`, NULL→`NO_SUSTAINED`, DIP→`UNRESOLVED`); label with the frozen M2 `level_label`; route with the frozen M4 `route`; label the inserted levels the same way; evaluate with the frozen M4 `evaluate`. No run is generated and no threshold is read, so **M2/M3/cache behaviour is replaced by its ideal**; any difference from the committed record is the M2/M3/cache contribution.

| Class (intended) | Design: predicted / committed | Held-out: predicted / committed | Pass-1 verdict (predicted, both) |
|---|---|---|---|
| `gentle_onset` (LOCATED) | **500 / 500** | **500 / 500** | LOCATED 495, ND 5 |
| `abrupt_onset` (LOCATED) | **59 / 59** | 54 / 56 | LOCATED 500 |
| `persistent_nonstationary_high_m` (LOCATED) | 37 / 39 | 38 / 41 | LOCATED 500 |
| `nonmonotone_amplitude` (LOCATED) | 50 / 51 | **58 / 58** | LOCATED 500 |
| `no_sustained_anywhere` (NP) | 0 / 2 | 0 / 0 | NP 500 |
| `no_null_consistent_anywhere` (NP) | 0 / 0 | 0 / 0 | NP 500 |
| `two_resolved_crossings` (NP) | 0 / 0 | 0 / 0 | NP 500 |
| `reentrant` (NP) | 0 / 0 | 0 / 0 | NP 500 / 499 |
| `off_band_mixture` (ND) | 2 / 2 | 2 / 2 | ND 496 / 493 |
| `off_band_unresolved` (ND) | 1 / 1 | 0 / 0 | ND 493 / 492 |
| `wide_mixed_boundary` (ND) | 0 / 0 | 0 / 0 | **ND 448, LOCATED 52** / **ND 441, LOCATED 59** |
| `unresolved_heavy_boundary` (ND) | 0 / 0 | 0 / 0 | ND 500 |

Every predicted error in the four failing classes fires **rule 4c, cause `boundary_unresolved`** — no other rule, no other cause. Every one of them was `LOCATED` at pass 1 except the 5 gentle sweeps per ensemble whose window already held 4 pass-1 levels. Final spans among the errors: gentle 5–11 (never ≤ 3); abrupt-kind 4–6, against passes at 0–3.

**Error versus width** (abrupt_onset, both ensembles pooled, 2k-micro bins of `w`): 0/111, 0/110, 0/92, 0/94, 0/96, 0/106, 4/97, 11/100, 38/92, 60/102 for `w` = 0–2k … 18–20k. No error below `w` = 12k; the error is a step in `w`, as §2 predicts. The same holds for `persistent_nonstationary_high_m` (errors at `w` ≥ 12.5k) and `nonmonotone_amplitude` (`w` ≥ 14.6k).

**`wide_mixed_boundary` is the control.** Pass 1 wrongly locates ~10% of those sweeps (their 150–250k window happens to hold only ≤ 3 pass-1 levels); pass-2 densification correctly converts every one to ND. The rule is doing for that class exactly what it does to `gentle_onset`. The two classes differ only in `w`: 150–250k versus 60–120k. Rule 4c with limit 3 after 8 insertions cannot separate them, because its effective criterion is `w ≲ B/3`, and both windows exceed that.

## 4. End-to-end realization sample (`realize_sample.py`, `e7f47dc8…`; rows `realized_*.jsonl`)

To test the "M2/M3 ideal" assumption directly, sweeps 0–24 of each failing class were run **end to end through the frozen instrument with the production cache** (`load_production_cache`, role `production_frozen`; ≈ 50 s per sweep, 100 sweeps), design master, and every `SweepResult` row was kept (`compare.py`, `1e6db4ca…`).

| Class | n | pass-1 label strings identical | final label strings identical | final verdict identical | final rule identical | realized outcome |
|---|---|---|---|---|---|---|
| `gentle_onset` | 25 | 25 | 23 | **25** | **25** | 25 × (pass-1 LOCATED → 4c ND) |
| `abrupt_onset` | 25 | 25 | 24 | **25** | **25** | 20 LOCATED, 5 × (LOCATED → 4c ND) |
| `persistent_nonstationary_high_m` | 25 | 24 | 23 | **25** | **25** | 24 LOCATED, 1 × (LOCATED → 4c ND) |
| `nonmonotone_amplitude` | 25 | 24 | 24 | **25** | **25** | 22 LOCATED, 3 × (LOCATED → 4c ND) |

The six label-string differences are each a single level labelled `U` by the instrument where the ideal says `M` or `N` (one seed's run read `UNRESOLVED` by M2 against its M3 threshold) — isolated, verdict-neutral in every case. That is the whole observed M2/M3/cache footprint in the sample, and it is the size of the 0–3 residual in §3.

## 5. Attribution

| Component | Implicated? | Evidence |
|---|---|---|
| **M4 rule 4c** (span limit 3, counted in levels, after pass 2) **together with P2R-5/6** (8 insertions) | **Yes — the cause.** | §3: all errors fire 4c; all were LOCATED at pass 1; error is a deterministic step function of the generator's window width; the ideal-M2/M3 replay reproduces the committed counts. |
| M6 archetype table / generator declaration (gentle 60–120k; abrupt-kind 0–20k) | **Co-determinant, not a defect by itself.** | The widths are the contract's own definition of the morphologies the instrument must locate (v0.2 §audit, v0.3 item 8). The conflict is between these declared widths and 4c's effective resolution `w ≲ B/3`. |
| M2 (classify) | No. | Labels agree with the ideal on 94/100 strings; the 6 differences are isolated `U`s that change no verdict. |
| M3 (conditional null) / qualified cache | No. | Same evidence; cache is consulted only to classify runs, and run classification is not where the verdicts diverge. |
| M4 router arithmetic / collision fallback | No. | All 100 realized sweeps: P2R-5, 8 nominal, 8 realized, no fallback moves or drops. |
| Code-versus-contract transcription | No. | `evaluate` and `route` implement v0.4 §5 rules 1–4d and R1–R7 as written; the defect is in the `[PROPOSED]` values the contract itself said "ratify only if [the audit] clears" (v0.3 item 3–4; `verdict.py` header). M6 did not ratify them. The governance worked. |

**Why L2's caution was right and the diagnosis still lands on M4.** L2 (§10) declined to assign the defect from the aggregate records alone, noting the gentle-onset yield observation made the router "a legitimate suspect, not an established cause." The per-sweep replay supplies what the aggregates lacked: the pass-1 verdict, the rule that fired, and a deterministic width dependence. The router is implicated not through its yield but through what 4c does with that yield.

**Contract-level reading.** v0.4 §5 rule 4d carries the binding clause "Line-not-drama: no jump, slope, monotonicity, or separation criterion exists anywhere above," inherited from v0.1 ("arbitrarily gentle growth from floor above a locatable onset point satisfies LOCATED … any such criterion would refute the theory for behaving as its own working form predicts"). A span limit counted in post-densification levels is, operationally, a limit on the physical width of the mixing region relative to the band — a steepness criterion by another name. The audit found exactly the consequence the v0.1 clause warned of: the gentler the onset, the more certainly it is called ND.

## 6. Bounds of this diagnosis

- **Noncanonical throughout.** Produced in a cloud container, not on `CHA-88D57D3`; only three of the twenty pins reproduced; no M7 envelope; no authorization. The arithmetic replay reads no run and no threshold and so is environment-insensitive by construction; the 100-sweep realization is a check on the ideal assumption, not a result.
- **What it establishes:** where in M2/M3/M4/cache the committed onset failures arise, with the mechanism and its width dependence. **What it does not do:** specify, evaluate, or recommend any change to 4c, to the insertion count, or to the archetype widths. Those are repair-design decisions, which under L2 §4.2 come *after* this finding is confirmed and are frozen before any new qualification evidence is drawn.
- **Both E1-R ensembles remain burned** (L2 §4.2). This diagnosis used them diagnostically, as L2 permitted; it reinforces that neither can guard a successor.
- The six residual label differences in §4 were not traced to the specific run/threshold pair; they are small enough and verdict-neutral enough that tracing them is not on the critical path. L2 may ask for it.
- Nothing here bears on E1-R's projection-side results (dense reference, stability, design-stability, tolerance program), which never pass through rule 4c on a morphology of this kind (reference of record NO-NULL-PHASE → rule 2, no band).

## 7. What is asked of L2

1. **Confirm or refute the attribution** in §5 — that the onset failures arise in rule 4c as frozen, in interaction with P2R-5/6 densification, with M2/M3/cache contributing only the residual.
2. **Confirm the method** — that an exact replay of the committed draw hierarchy under an ideal-classifier assumption, checked against a 100-sweep realization, is sufficient evidence of *location* (not of *repair*) for the purposes of L2 §4.2's "bounded diagnosis phase first."
3. **Name any discriminating test** L2 wants run before the location is accepted (e.g., a realization sample on the held-out master; tracing the six residual `U` labels; a width-sweep with the ideal replay only).
4. **Confirm that the repair surface is now bounded to M4 + the M6 archetype/width declaration**, so that the Flight 8 contract may fold the repair into its own instrument version (handoff §4 condition 2) rather than re-opening M2 or M3 — noting that Flight 8 rebuilds M3's null and the archetype table regardless (pre-freeze §4.8, §4.9).

**Not asked:** any opinion on what the repair should be. That packet comes after this one.

## 8. Files in this bundle (all NONCANONICAL)

| File | Identity | Content |
|---|---|---|
| `E1R_M6_ONSET_DIAGNOSIS_FINDING_v1.md` | (this file) | the finding |
| `predict_labels.py` | `98b6455b0a6332b8` | arithmetic replay, all classes, both masters |
| `predicted_rows.json` | `4b3498096cac3d85` | 12,000 predicted rows (params, pass-1 labels, router row, final labels, verdict, rule, spans) |
| `realize_sample.py` | `e7f47dc844e2b2bd` | end-to-end realization of a sweep range with the production cache |
| `realized_gentle_onset.jsonl` | `639660794df79b9e` | 25 complete `SweepResult` rows |
| `realized_abrupt_onset.jsonl` | `49c761f36bbcdced` | 25 rows |
| `realized_persistent_nonstationary_high_m.jsonl` | `b9693bff30a8fc4b` | 25 rows |
| `realized_nonmonotone_amplitude.jsonl` | `b47909bf506158c6` | 25 rows |
| `compare.py` | `1e6db4ca23f6fff5` | realized-versus-predicted comparison |

Proposed placement, for Mike: `flights/mfa_fidelity/diagnosis/e1r_m6_onset/` with a README whose first line is NONCANONICAL, outside `artifacts/` and `build_records/`, so no package validator, registry or handoff can mistake any of it for a record. Routing to L2 as a packet: this finding plus `predict_labels.py`, `compare.py` and the four realized `.jsonl` files (`predicted_rows.json` is 4 MB and derivable from the script in under four minutes; send on request).

*L1, 2026-10-15. Every identity above was measured in this session from the fresh clone at `60d6c59` or from the files produced here.*
