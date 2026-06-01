# Operations log — 2026-05-31 — wave-two design phase opened; Rule C contract placed canonical

**Session date:** 2026-05-31
**Layer:** Layer 1 (Claude)
**Execution channel:** Mike (sole)
**HEAD at session start:** 3f5af0f
**Commits this session:** two — (1) contract + this ops log; (2) anchor refresh. Hashes recorded in the next anchor, not here (this log is inside commit 1 and cannot reference its own hash).

---

## What this session did

Mike opened the wave-two DESIGN PHASE and accepted the resulting design contract, which was placed canonical at `cycle3/wave_two/DESIGN_CONTRACT.md`. No probe was seeded — seeding remains a separate step, Mike's call to open. The contract iterated through four review drafts (v1 -> v4) in-session; v4 was accepted and placed (banner updated review-draft -> canonical, function form moved from fixed-within-the-draft-line to canonically fixed). A new `cycle3/wave_two/` subdir was created to home the growing wave-two artifact set rather than spreading it flat across `cycle3/` with prefixes as wave one did.

## Sequence

1. **Cold-start grounding.** HEAD confirmed 3f5af0f; manifest passed (routing archive 17 files, OBS-001 NPZ 60, tree clean against origin/main); current anchor and kit v5.1 read. Carried the six refinements + two precision notes (not the five-amendment compression).

2. **Phase opened; forks arbitrated.** Mike confirmed scope holds and opened the design phase. Forks arbitrated by Mike: Rule C divergence on the BECOMING-ACTIVE transition (not survival), single signed coefficient kappa; the comparator a SEPARATE process (not a weak-kappa limit of Rule C); seeds held at the wave-one five. Function form left open as the genuine Layer 2 question.

3. **Function fixed via Layer 2 (contract v1 -> v2).** Routed a self-contained function-form question (continuing context). Layer 2 returned logit-linear centered, coefficient-null separable: p_become = sigma(logit(p_Lambda) + kappa * g(q)), g(q) = 2q - 1 fixed centered. Corrected Layer 1's uncentered lean (uncentered q would let kappa move average activation tendency, not only local coupling). Added: fence-integrity prohibition list (no kappa-on-global-rho, no dynamic centering, no hidden feedback in Lambda baseline, no piecewise sign-specific form); realized-contrast tracking p(q=1) - p(q=0); large-|kappa| as a degeneracy probe; the survival-must-not-stabilize fence; a bounded-linear audit form held in reserve. Divergences preserved as Layer-2-originated.

4. **CSV read (primary source) and open-B correction (v2 -> v3).** Pulled the wave-one OBS-001 CSV (`cycle3/data_out/c3_obs_001_results.csv`, 300 rows) under the canonical venv. Read with a flag-reconciliation cross-check (pessimistic-on-passing on the session-state read, not only on probes): of 97 non-degenerate-lifted rows, `Psi_meanI_state_z` positive on ALL 97 (min ~139), zero near-null, zero negative; persistence has a 6-row near-null band (z ~ -1.85 to -0.06, mean ~ -1.43). Dual-degeneracy confirmed (125 both-flag rows; 97 reconciled). Finding: wave one contains NO lifted-near-null meanI region. Drove open B SPLIT (persistence half readable; meanI half not) and a new Section 5.1 recording what the absence does/does not establish.

5. **Layer 2 conferral on v3 (v3 -> v4).** Two genuine questions: Q1 (5.1 fence strength), Q2 (comparator calibration circularity). Layer 2: Q1 — keep "held open, not predicted" but soften "wave one has no standing to predict" to "wave one sharpens the diagnostic target but does not predict Rule C reach"; qualify "hard corner." Q2 — CONFIRMED the circularity (tuning to hold meanI_z in +/-2.0 is near-null by selection against the band it floors); recommended SPLITTING the comparator into Comparator 0 (Lambda-only floor, calibrated on rho-lift alone) and Comparator epsilon (weak-neighbor audit, magnitude bounded by a predeclared realized-contrast ceiling |delta_p| <= epsilon * pbar_Lambda fixed before observing z-scores), near-null meanI an OUTPUT not a target.

6. **Fork arbitrated; v4; acceptance; placement.** The comparator split is a step past the arbitrated singular-comparator scope; surfaced as a fork. Mike arbitrated: take the split. v4 folded in Q1 + Q2. Mike accepted v4. Placement: new `cycle3/wave_two/` subdir; contract at `cycle3/wave_two/DESIGN_CONTRACT.md`; generated BOM-less single-LF to match the `PROBE_DESIGN_INPUTS_HELD.md` sibling convention (verified sibling first3=35,32,67 last2=46,10); placed and verified at destination (size 14610, first3=35,32,87 `# W` no BOM, last2=46,10 single LF).

## Discipline notes this session

- **Function form fixed by Layer 2, not by Layer 1 framing.** The genuine question went to Layer 2 open; the centering correction came back from Layer 2 and was taken. Both Layer-2 divergences (centering, survival fence) recorded as Layer-2-originated in the contract, not absorbed as Layer 1's.
- **Circularity caught at conferral, not after seeding.** Q2 was flagged by Layer 1 as the point it was least sure of in its own construction, routed as such, and Layer 2 confirmed it. The split resolved it structurally rather than by rewording. Pessimistic-on-passing applied to Layer 1's own design, not only to probes.
- **Scope-step surfaced, not folded silently.** The comparator split exceeds the arbitrated singular-comparator scope; it was put to Mike as a fork and is recorded in the contract's Section 6 apparatus-scope note and reflected in the anchor refresh (commit 2).
- **Open B did not close the way v2 anticipated; recorded as split, not forced.** The meanI near-null scale is OBSERVED from Comparator 0, not set from wave one (which lacks it). The honest non-closure is the record.

## State at close

- **Contract placed canonical** at `cycle3/wave_two/DESIGN_CONTRACT.md`, committed this session (commit 1, with this log).
- **Anchor refreshed** (commit 2) to record: phase open, contract placed, comparator split against the arbitrated singular-comparator scope, the two downstream opens.
- **Untracked at repo root:** `read_obs001_nearnull_scale.py` (the pure-read CSV summary script). Harmless; not committed; removable or retainable at Mike's discretion.
- **Not seeded.** No wave-two probe exists.

## Resume anchor for next session

First action: cold-start grounding — confirm HEAD (will be the commit-2 anchor-refresh hash), manifest check, read the refreshed anchor and kit. The refreshed anchor (commit 2) is the primary orientation and carries the current wave-two state; this log is the just-closed session's detail.

Wave-two path from the placed contract's Section 10:

1. Set grid density against the realized-contrast scale (open).
2. Run Comparator 0 (Lambda-only): record whether lifted independent activation gives near-null observables under this apparatus, or whether organization is the default (the latter is a finding, not a failure). Run Comparator epsilon as the weak-coupling audit around it.
3. Seeding is Mike's call to open.

Two genuine opens downstream: kappa-grid density, and what Comparator 0 observes. Carry-forward unchanged: six refinements + two precision notes; weak-form Rule B prior preserved-not-hardened; L4 ontological question unsettled; vocabulary quarantine binding.

Drafting partner: Claude (Layer 1), 2026-05-31.
