# Item 6a — Re-scoped-and-Discharged Record (E4 remediation, session 24)

**Status / next action:** Final record, Layer-2-cleared (scan returned accept-with-register-edit; register edit applied). **Next: commit as the session-24 discharge cluster alongside the STANDING_ITEMS full-file overwrite; push remains held pending Mike's item-16 component-4 register call.** Companion artifact: `standing_items_edits_session24.md`.

**Register note (Layer 2 scan, applied):** this item was **re-scoped and discharged**, not discharged in the bare sense. The original item 6a pre-registration's within-fixed-probe IF1/IF2 design did not execute and was not merely trimmed; the primary mapping was re-aimed first. The label carries the re-scope register so the record cannot be read as implying the original pre-registration completed as designed.

---

## 1. What this discharges

Item 16 component 3 (E4 remediation) chose **Option A — re-scope to available substrate — taken to discharge.** Item 6a's F_LR-vs-F_2_symmetric characterization is closed by recording the structural finding the re-scoped substrate supports, with no further EDA or confirmatory execution to run.

**This is a re-scope before discharge, not completion of the original item 6a pre-registration.** Stated explicitly per the Layer 2 scan: *the original item 6a pre-registration could not be executed because its probe1_overcrowding F_LR arm did not exist; Option A re-scoped the item to the substrate-supported structural finding and discharged that re-scoped item without EDA/confirmatory execution.* It is neither item 6a abandoned nor an executed run returning null: the re-scoped finding was already in hand from architecture plus substrate signatures, so there is no analysis left whose execution would add to it.

## 2. The finding (as re-scoped and discharged)

**F_LR responds to the probe; F_2_symmetric does not.** Under F_2_symmetric the three probe conditions collapse to a single trajectory (the probe2_starvation and probe3_fusion_residual files are byte-identical shadow copies of probe1_overcrowding); under F_LR the starvation probe produces a genuinely distinct trajectory (probe2_starvation_FLR differs in content and size from the baseline). The architectural F-form difference the substrate cleanly supports is this difference in probe-sensitivity itself.

### Grounding (belt-and-suspenders, per Mike's session-24 election)

- **Record citation:** the F_2_symmetric shadow-copy structure was confirmed in code (sessions 21–22) and is specified at FSS v1.1 §13.2.
- **Direct verification (session 24, Mike-executed):** SHA-256 byte-identity across the F_2_symmetric probe arm at both scales —
  - 20×20: `flight6_probe1_overcrowding_20x20` and `flight6_probe2_starvation_F2sym_20x20` both `5D8F54966A1FF5B8328B6524752EA92C858C09EFCBA07B3B3451AD1DA3D0C897`.
  - 40×40: `flight6_probe1_overcrowding_40x40` and `flight6_probe2_starvation_F2sym_40x40` both `65F24CB0C816DEB2BE6870217BB78CDD976BA100B32BD74B2F1E3A014C461B24`.
  - The F_LR arm (`probe2_starvation_FLR`) is excluded from the identity claim by construction — it is the genuinely-distinct trajectory and is expected not to match.

## 3. Why discharge rather than re-scope-and-re-execute

The finding in §2 follows from the architecture (the symmetric-form shadow-copy property) plus the byte-verified substrate signatures. It does not require the rolling-ρ EDA, the W/τ/Z lock, or the IF1/IF2 confirmatory regressions to produce. Those procedures were built to deliver a within-fixed-probe F-form contrast that this substrate does not support (the F_2_symmetric arm is the probe-invariant baseline, so an F_variant contrast would conflate F-form with probe-perturbation-presence — the §3 fork of the A2 skeleton, resolved by Mike to option (a): re-aim to the structural claim). With the primary mapping re-aimed to the structural finding, there is no remaining execution. **This is a re-scope before discharge, not completion of the original item 6a pre-registration.** Discharge is therefore the terminal form of the re-scoped item.

## 4. Two-field classification (Phase 4B v1.1 §6)

- **Claim:** Under F_2_symmetric the probe conditions collapse to one trajectory; under F_LR the starvation probe yields a distinct trajectory. The F-form difference is a difference in probe-sensitivity.
- **Field 1 (epistemic status):** substrate-structural / architecture-entailed. Established by the symmetric-form shadow-copy property (FSS v1.1 §13.2) and byte-verified file identity, not by a fitted analytical result. Not a candidate-produced statistical finding.
- **Field 2 (architectural reach):** characterization only. It does **not** adjudicate the F_LR-vs-F_2_symmetric architectural selection (item 6c); it does not commit Ψ-operationalization (item 13) or Q-form (item 14); it does not estimate how F-form reshapes the Λ-pathway or density-pathway within a fixed probe (that contrast is unavailable on this substrate — see §5).

## 5. Dispositions (downstream coupling)

1. **Item 15 retires.** No Stage 1 EDA / Stage 2 confirmatory execution remains. The committed Stage 1 EDA script (`item_6a_stage1_eda.py`, `22aedba`) and the Layer-2-accepted-but-uncommitted v3.1 patch are superseded-in-place by the discharge — recorded as retired, not deleted.
2. **Item 12 narrows; stays open.** The consumer-adapter built for `item_6a_stage1_eda.py` is moot, but the substrate-hygiene part persists: the directory-naming question and the which-copy question (four tree-wide copies of probe1_overcrowding across three size-families / three dates; `flight2_outputs` not assumed canonical). Whether a general schema-adapter is warranted for other consumers (items 13/14, future Tier 2) is held open under item 12, not closed by 6a's discharge.
3. **Item 6c keeps the narrower evidence.** The probe-sensitivity finding is genuine evidence toward the F_LR/F_2_symmetric architectural selection (item 6c); item 6c stays open.
4. **The richer contrast routes to item 6b.** A clean within-probe F-form contrast (how F-form reshapes the Λ and density pathways) requires non-shadow F-form probe-differential substrate — exactly item 6b's `outside_phase_4b_scope` substrate-generation. Discharging 6a does **not** close the F-form question; it relocates the unanswered part to 6b.
5. **Item 16 component 3 — MET.** E4 remediation settled (Option A, re-scoped and discharged). Components 2 (downstream-claims review) and 4 (formal protocol-record register) remain open at Mike's arbitration.

## 6. Honest-record notes

- The §2 verification hash incidentally reproduces the real F_2_symmetric 20×20 value (`5D8F5496…`), the same value the session-20 determination used against the fabricated `…5492`. This corroborates the determination's primary-source basis and confirms the hash read genuine files. Noted as incidental only — the determination is made (item 16 component 1, MET session 23) and is not re-opened here.
- Item 6a was re-touched across sessions 15–24 (split from item 6; v1→v2 pre-reg with seven revisions; v3 EDA script + v3.1 patch; the path/filename friction that recharacterized item 12). The recurring difficulty traces to a single root: its probe1_overcrowding partition was believed substrate-supported only because the session-16 fabricated SHA claim asserted an F_LR probe1 trajectory that never existed. Session 24 is the first point at which the substrate truth was in hand to see this. The item was not ill-conceived; it rested on a misrepresentation. (The determination's formal subtype — verification-dressing over a real structural fact — is carried by item 16 and current_state.md; referenced here, not re-stated.)

— Layer 1 (Claude), session 24, item 6a re-scoped-and-discharged record (Layer-2-cleared)
