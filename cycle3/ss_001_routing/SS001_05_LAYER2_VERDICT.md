# Layer 2 - C3-SS-001 substantive review verdict (verbatim)

> Source: ChatGPT's response to SS001_LAYER2_REVIEW_REQUEST.md, routed back via Mike's paste. Archived verbatim in pure ASCII (any Greek letters or em-dashes in the source paste rendered as ASCII equivalents per the canonical-doc convention).

---

# Layer 2 review - C3-SS-001 steady-state apparatus

## Verdict

**Accept as-is. Advance C3-SS-001.**

The concerns Layer 1 surfaced are real, but they do **not** rise to the level of a design-blocking weakness. The apparatus's stated gate is not "each case isolates exactly one filter"; it is whether the window apparatus correctly admits and rejects known synthetic windows using the four flags: lifted activation plus the three steadiness filters. On that criterion, the canonical CSV does what it is supposed to do: all 30 windows produce the expected `(Steady_State_Candidate, Lifted_Activation_Candidate)` pair.

I recommend outcome **(a): substantive design accepted as-is**, with a short non-blocking note in the test record that Cases 2 and 3 are **flag-level controls**, not pure per-filter unit tests.

---

## 1. Filter isolation vs. flag outcome

### Judgment

**Flag outcome is sufficient for this gate.**

The purpose of C3-SS-001 is to validate the earned-window apparatus before any integration test can read values as Regime-II-relevant. The registry frames this as: windows must be earned by explicit diagnostics, with relative drift, rho CV, and range/mean all contributing to steady-state eligibility. It does not require pure per-filter isolation. 

Layer 1 is right that Case 2 does not uniquely test the drift filter. A strong monotone ramp naturally increases CV and range as well as relative drift. That is not an accident; it is mathematical coupling among the diagnostics for a ramp. But for real windows, that coupling is desirable: a drifting trajectory should be rejected even if more than one filter catches it. 

Layer 1 is also right that Case 3's period-20 sine creates drift residual in some windows. But all Case 3 windows still produce the intended flag pair: not steady, lifted activation. The apparatus correctly rejects high wobble even when the rejection is carried by more than one steadiness filter. 

### Recommendation

Do **not** revise Cases 2 and 3 before advancing C3-SS-001.

Add a record note:

> Cases 2 and 3 validate steady-state rejection at the flag level, not pure one-filter isolation. Filter coupling is expected for strong ramps and finite-window oscillations. The apparatus is conservative: a window failing any steadiness diagnostic is rejected.

If later the project wants filter-unit tests, create a supplemental diagnostic test. Do not block this gate.

---

## 2. Case 4 margins

### Judgment

**Adequate as-is.**

Case 4 is designed to be steady but not lifted. It does that. Mean rho stays around 0.02, well below the lifted threshold of 0.05, while drift, CV, and range remain within steadiness thresholds. The CV and range margins are the narrowest in the design, but they are not dangerously close for the canonical seeded run.

Would lowering the noise amplitude from +/-0.002 to +/-0.001 make it cleaner? Yes. Is that necessary for the L2 gate? No.

The current Case 4 correctly separates:

- **steady**: yes;
- **lifted activation**: no.

That is the intended discrimination.

### Recommendation

Do **not** patch Case 4 before advancing.

Record as a non-blocking note if desired:

> Case 4 has the narrowest CV/range margins, but it remains safely below steadiness thresholds in the canonical seeded run and correctly fails lifted activation. Noise-amplitude tightening is optional future polish, not required for gate clearance.

---

## 3. Battery extension

### Judgment

A seventh and eighth case would be useful as **filter-unit diagnostics**, but they are not required for C3-SS-001.

The proposed additions are analytically sensible:

- a drift-only case with relative drift just above threshold but CV/range below threshold;
- a pure wobble case with an integral number of periods and no regression drift.

Those would improve per-filter isolation. But adding them now would turn this from a steady-state eligibility gate into a more exhaustive diagnostic-suite design. The existing battery already tests the necessary decision logic:

- flat lifted passes;
- monotone drift fails;
- high wobble fails;
- low trivial is steady but not lifted;
- late stabilization has early failures and late pass;
- step transition has plateau windows pass and transition-spanning windows fail.

That is enough for the precondition gate.

### Recommendation

Do **not** require extension now.

Optional later item:

> C3-SS supplemental filter-unit test: isolate relative drift, CV, and range/mean independently.

But keep it separate from the current gate.

---

## 4. Other validity notes

### A. Record window interval convention

The CSV uses windows like `0,100`, `25,125`, etc. The record should state whether `Window_End` is exclusive or inclusive. The script appears to operate on 100-tick windows, so `0,100` likely means ticks 0-99. This is not a blocker, but it should be explicit.

Suggested note:

> Window intervals are reported as `[Window_Start, Window_End)` unless otherwise specified.

### B. Keep the two flags independent

The two-output design is good:

- `Steady_State_Candidate`
- `Lifted_Activation_Candidate`

Do not combine them into a single "Regime-II eligible" flag at this stage. Real-substrate interpretation later needs both, plus the coherence observable pair and L4 judgment.

### C. No L4 leakage

This gate says nothing about Regime II itself. It validates the steady-state/lifted-window apparatus on synthetic rho trajectories. That boundary should be kept in the record.

---

## Final recommendation

**Outcome (a): accept as-is.**

C3-SS-001 can advance. Layer 1 should fill the test record's post-execution block and update the registry/status accordingly.

Suggested record language:

> Layer 2 accepted C3-SS-001 at the flag-discrimination level. The apparatus correctly admits/rejects all 30 canonical synthetic windows according to the pre-specified `(Steady_State_Candidate, Lifted_Activation_Candidate)` expectations. Cases 2 and 3 are not pure per-filter unit tests; filter coupling is expected for strong ramps and finite-window oscillations. This is non-blocking because the gate tests earned-window flag behavior, not isolated unit testing of each filter. Case 4 margins are adequate for the canonical seeded run. C3-SS-001 clears the steady-state eligibility precondition, with no Regime-II interpretation attached.
