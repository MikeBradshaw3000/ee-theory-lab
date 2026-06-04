# Rule D R3 findings — turnover-limited activation, scoped negative for the predeclared R3 grid

**Status:** CANONICAL. Reading of the Rule D R3 behavioral map (`cycle3/data_out/c3_w2_rule_d_r3_results.csv`, committed c1ff920) against the Rule D design contract Section 4 matched-coupling bracket. Layer 2-concurred 2026-06-03 (read against its own mean-field prediction; agreement reached by two independent routes — Layer 1's per-(setting, seed) bracket read and Layer 2's density-level R3 recurrence — not by deferral). The contract (`RULE_D_DESIGN_CONTRACT.md`, R3-amended) governs the mechanism, fences, and success criterion; the resolution memo (`D_OPENS_RESOLUTION.md`, R3-corrected) governs the grid; this file reads the run against them. On any discrepancy, the CSV is primary source over this restatement.

---

## The call

**Rule D R3 fails to produce the turnover-limited near-null mechanism under the locked topology and the predeclared R3 grid.** At matched responsive coupling, lower-turnover settings produce the required signed anchors, but increasing `theta_turnover` does not move the co-equal observable pair into near-null / near-null while preserving lifted, non-degenerate activation. The arc **rests** on this negative result for the R3 grid; it does **not** close the broader turnover-limited mechanism class, because a stronger-turnover floor / degeneracy endpoint was not reached by `theta_turnover = 0.50` under R3.

This is a real negative result, read from the map and not patched after it was seen. The two contract guards (Section 4.3 density-confound, Section 4.4 live-coupling exposure) do not bind, because their precondition is a both-observable near-null candidate row to audit, and none exists.

---

## What was read

Rule D R3 at the resolved grid: `theta_turnover` in {0, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50} x matched responsive kappa (realized contrast c = -0.35 and c = +0.35, both signs, kappa = -/+0.7599) x seeds {42, 137, 256, 1024, 31415}, Lambda = 0.40 only. 70 settings x 5 windows (window_start 0/25/50/75/100) = 350 rows. Window structure 200 ticks / 100-tick windows / step 25; 50x50 Moore-radius-1 toroidal; LOW_Z_THRESH = 2.0; SS-001 earned-window criterion. Parity pre-flight cleared. Read per-(setting, seed) flag counts, never per-band means; the settled measurement windows (window_start >= 25) carry the reading, the window_start = 0 rows carry the pre-settling transient and are not the measurement windows.

R3 mechanism: active-cell persistence is `s_Lambda * (1 - theta_turnover)` — Rule C's neighbor-independent Lambda-survival (`s_Lambda = 0.40` at this anchor) retained, `theta_turnover` an ADDITIONAL independent churn hazard on top. `theta_turnover = 0` recovers Rule C exactly.

---

## 1. Precondition met — signed lower anchor, both signs

`theta_turnover = 0` recovers the Rule C signed regime under R3 (distributionally, not bit-identically; different RNG-stream consumption between scripts):

- c = -0.35: `Psi_meanI_state_z` ~ +3.6 to +6, `Psi_persistence_I_z` ~ -3.5 to -5.4 — signed, negative-persistence.
- c = +0.35: `Psi_meanI_state_z` ~ +5 to +6, `Psi_persistence_I_z` ~ +5 to +8 — signed, positive-persistence.
- `saturation_degenerate` / `extinction_degenerate` False; `rho_mean` ~0.417-0.420 (c=-0.35) / ~0.371-0.373 (c=+0.35) on the settled windows. `theta_turnover = 0` does NOT saturate — the R3 fix holds; `effective_persistence = 0.40 = s_Lambda * (1 - 0)`.

Both brackets have a valid signed lower end. The reach precondition (contract Section 4.2) is met, so any near-null the map emits would not be non-discriminating-by-default.

## 2. Candidate not produced

`saturation_degenerate` and `extinction_degenerate` are False on all 350 rows. `LowLow_Nondegenerate_Candidate` fires on no row. `rho` stays lifted across the whole ladder (no collapse, no saturation; the theta ladder moves `rho_mean` only modestly — c=-0.35 ~0.42 at theta=0 down to ~0.36 at theta=0.50; c=+0.35 ~0.37 down to ~0.29). Realized neighbor exposure stays nontrivial throughout: `q_mean` ~0.36-0.42 (c=-0.35) / ~0.29-0.37 (c=+0.35), `mean_abs_perturbation` ~0.056-0.077 across the ladder — coupling was live at every theta, not driven inert. No both-observable near-null bracket appears at matched responsive coupling at any `theta_turnover`.

## 3. Per-sign map

- **c = -0.35 (negative coupling):** as `theta_turnover` rises, `Psi_persistence_I_z` STAYS negative-signed at every theta (~ -3 to -5 even at theta=0.50). `Psi_meanI_state_z` does NOT decay toward null — it climbs strongly positive, ~ +14 to +22 at theta=0.35-0.50. Neither observable approaches null.
- **c = +0.35 (positive coupling):** `Psi_persistence_I_z` STAYS robustly positive-signed at every theta (~ +4 to +9 throughout, including theta=0.50). `Psi_meanI_state_z` decays through near-null and into negative values — near zero for some seeds at theta=0.20 (256: +0.10 / -0.31; 31415: +0.10), mildly negative at theta=0.35 (~ -1 to -2.4), solidly negative at theta=0.50 (~ -3 to -6.3). meanI transits through null into a negative-signed regime; persistence never leaves positive.

At neither sign is the co-equal pair jointly near-null at any `theta_turnover`. Per the contract Section 4.1 produce-or-fail table, this is the bottom row: responsive coupling remains signed (jointly never near-null) across the tested ladder, with no degeneration.

## 4. Single-axis finding (apparatus-level; fenced from L4)

The two observables respond differently to independent churn: **single-axis turnover sensitivity with persistence-sign retention.** `Psi_meanI_state` is turnover-sensitive (its sign moves, and at c=+0.35 reverses); `Psi_persistence_I` sign is turnover-robust (holds the coupling-side sign across the whole ladder at both signs).

Order-parameter reading (Layer 2): `Psi_persistence_I` tracks the spatial pattern of where activity keeps being regenerated across the window, which remains clustered (or anti-clustered) as long as the becoming-active kernel keeps re-injecting the same neighborhood propensity each tick — robust to individual active-site churn. `Psi_meanI_state` tracks the instantaneous active-state configuration at each tick, which independent churn can puncture, so per-tick meanI can fall through null and reverse even while the same regions remain persistently favored over the window. This is a one-dimensional-density mean-field's blind spot; it needs at least a pair / age-structured reading. Mechanistically, the becoming-active transition re-injects the q-dependent birth source every tick, so added independent turnover shortens active-cell residence time without removing the live coupling — which is why `rho` stayed lifted, exposure stayed live, and the persistence axis kept the coupling sign.

This is a substantive apparatus-level observable result. It is NOT a Rule D success (it is not a both-observable near-null bracket), and it does NOT resolve the L4 ontological question (which observable, if either, IS Regime-II coherence). That the two observables do not move together under churn is recorded and fenced from L4; it does not select either observable as theoretical Psi.

## 5. Guards do not bind

The density-confound guard (Section 4.3) and the live-coupling-exposure guard (Section 4.4) do not adjudicate a candidate, because there is no joint near-null candidate row to audit. Recorded for completeness: exposure was live across the ladder (Section 2 above), and the theta ladder's effect on `rho_mean` was modest and monotone, not a large density displacement — but these are not used to qualify a candidate, because none exists.

## 6. Follow-up disposition — named, not triggered

**Named-not-triggered follow-up:** Because the R3 ladder did not reach a floor or degeneracy endpoint by `theta_turnover = 0.50`, a stronger-turnover endpoint extension remains available if Mike wants to test whether the negative result extends toward a churn-dominant boundary. This follow-up is not opened here. "Triggered" means eligible for Mike's later opening, not automatically seeded; no seed is required to sustain the present scoped negative.

Precision on the variant: under R3, `theta_turnover = 0.50` halves Rule C's survival (net persistence 0.40 -> 0.20) rather than imposing a short absolute lifetime, so the ladder is additional churn on top of `s_Lambda`, not a total-lifetime ladder. If a follow-up changes from R3's additional-churn-hazard form into an absolute-lifetime / stronger lifetime-control variant, it is an endpoint-extension VARIANT — to be opened and named as such, not run silently as "the same R3 grid." Canonical R3 preserves Rule C's neighbor-independent Lambda-survival and adds turnover on top; that is why `theta_turnover = 0` recovers Rule C instead of saturating, and any variant that drops that structure is a different mechanism realization requiring its own placement.

## 7. Arc status — rests, not closes

Rule D R3 satisfies the signed-anchor precondition and preserves lifted, non-degenerate activation across the tested turnover ladder, but it does not produce a matched-coupling near-null / near-null bracket. The arc therefore **rests** on a negative result for the R3 grid. It does not close the broader turnover-limited mechanism class, because a stronger-turnover endpoint was not reached. This rest is the direct analogue of the Rule C first-pass rest on A-prime: the strongest warranted claim is stated, and the door is left open exactly as wide as the unreached endpoint warrants — no wider.

---

## What this finding does NOT do

- Does not close the turnover-limited mechanism class (no endpoint reached).
- Does not reopen or reclassify Rule C M2 / A-prime, and does not alter the Comparator 0 / Comparator epsilon floor findings.
- Does not resolve the L4 ontological question; neither observable is named theoretical Psi.
- Does not harden the weak-form Rule B prior.
- Does not seed any probe; the named follow-up remains Mike's call to open.

---

## Registry sentence

Rule D R3: signed-anchor precondition met; no degeneracy; no joint near-null / near-null bracket; no LowLow_Nondegenerate_Candidate. Fails to produce the turnover-limited mechanism under the locked topology and predeclared R3 grid. Observed single-axis decoupling: meanI is turnover-sensitive while persistence sign remains robust. Rule D R3 rests here; stronger-turnover endpoint extension is named-not-triggered.
