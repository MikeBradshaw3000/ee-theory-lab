# Operations log - 2026-07-04 - Two-channel ordering-probe design resolution

**Session date:** 2026-07-04
**Layer 1 instance:** cold-started from RESUME_2026-05-30.md (supersession header 2026-07-02c) at HEAD f7c7fba; grounding via single-clip consolidated read (HEAD + status + cycle3 listing + anchor + WAVE_TWO_PATTERN_SYNTHESIS.md + READING_D_PASS1_FINDINGS.md + TWO_CHANNEL_PROPOSAL.md), clipboard-captured per thumb-economy request.
**Arbiter:** Mike Bradshaw
**Outcome:** Two-channel ordering-probe DESIGN RESOLUTION completed and recorded (CM-1 primary; CM-2 held; CM-0 comparator; probe NAMED-NOT-TRIGGERED). Non-seeding throughout: no run, no implementation spec, no Layer 3 engagement.

## Sequence

1. **Grounding.** HEAD f7c7fba confirmed (matches instantiation-note expectation); tree clean; presence checks passed (all governing files present; NPZ inventory consistent with the anchor). Grounded from the anchor and the three latest governing files; earlier contracts/findings carried from the anchor summary with files-govern discipline.
2. **Fork direction (routed through Mike).** Layer 2 recommended the two-channel ordering probe as the next non-seeding design-resolution path over the B/C responsive pass (held, not abandoned; bounded near-empty per pass 1) and rest (available, not chosen). Recorded as L2 recommendation; the three-way arbitration remained Mike's. L2's direction fixed the discriminating question and seven required fences.
3. **v1 memo (Layer 1).** Design-resolution draft: discriminating question fixed; seven fences; three candidate common-mode constructions compared not silently picked (CM-0 static rejected-as-driver/retained-as-comparator; CM-1 exogenous frozen schedule; CM-2 uniform Rule E-class conditioning); L1 recommended CM-1 while flagging that it deviates from the named instrument's committed class wording ("admissible Rule E class") and so requires explicit amendment - surfaced as a fork, not applied.
4. **L2 review of v1: accept-with-amendments.** CM-1 primary concurrence (independent grounds: relay-lift would confound the ordering read between a common-mode finding and another lagged-feedback relay finding); instrument renaming to "exogenous common-mode lift with differential-channel sweep"; CM-2 relay-lift rejected as primary and held with an own-design-resolution requirement; schedule-imprint hard requirement (no rho_t imprint, no common-mode-lift claim); rho/prop_I stratified read; prop_I full-propensity-surface computation with common/differential/realized decomposition; two falsification tightenings (control-surviving raw organization required at kappa~0; differential-channel activation required before failure-to-track counts); factorization demoted to expected local diagnostic; deterministic frozen waveform preferred (identifiability first); one shared schedule across seeds; and the zero-mode-synchrony-vs-spatial-organization reading category (genuine L2 addition; L1's v1 missed it). Genuine-engagement check passed (contact with specific committed numbers throughout). Note: a later paste duplicated this v1 review verbatim; recorded as paste duplication, no conflict.
5. **v2 memo (Layer 1 synthesis).** All L2 amendments incorporated with attribution; CM-1-primary convergence recorded as refinement-driven under the framing asymmetry (L1 framed first). Two L1 additions, flagged for L2 return pass: the L4-adjacency fence on zero-mode language (driver imprint never recorded as coherence/Regime-II/theoretical-Psi-bearing) and the cadence-aliasing constraint (schedule period off the committed 2-block ring signature).
6. **Mike's arbitration.** CM-1 primary with amendments; CM-2 held; CM-0 comparator; no seeding. Instrument renaming ratified within the arbitration. Mike noted session-side context weight (expired uploads); conceptual arbitration and routing unaffected; exact file-level audits flagged for a fresh session if needed.
7. **L2 return pass on the two L1 additions: accept with precision amendments.** (i) Primary label "zero-mode driver imprint" / "global-count driver imprint"; "zero-mode temporal coordination" only in qualified form; unqualified "synchrony" excluded. (ii) Aliasing constraint broadened: avoid the 2-block artifact cadence AND trivial aliases of the observation-window structure; period chosen for identifiability (measurable imprint, multiple cycles); exact window structure to be verified from committed scripts at contract stage. (iii) G1 precision: imprint must exceed static-i.i.d./CM-0 expectation at the same mean rho (driver imprint, not stochastic tracking); threshold a contract-stage open.
8. **Final memo produced** incorporating the return-pass amendments; Mike's commit ratifies the final text (wording-level amendments fall within his "with amendments" arbitration).

## Committed this session

- cycle3/wave_two/TWO_CHANNEL_ORDERING_PROBE_DESIGN_RESOLUTION.md (governs the probe's design resolution)
- operations_log/2026-07-04_two_channel_design_resolution.md (this file)

## Standing state after this session

- Two-channel ordering probe: DESIGN-RESOLVED (CM-1 primary, exogenous common-mode lift with differential-channel sweep); NAMED-NOT-TRIGGERED; contract stage opens only on Mike's separate, explicit opening; contract-stage opens enumerated in the resolution Section 7.
- CM-2 (endogenous common-mode variant): HELD; own design resolution required; separate from the Rule E B/C hold.
- Rule E B/C responsive pass: HELD, named-not-triggered, not abandoned.
- Rest-wave-two: available, not chosen.
- All four wave-two instrument arcs: rest on scoped negatives, unchanged. Reading-D pass-1 result: unchanged. Comparator 0 classification: unchanged. L4: untouched.
- Parallel workstreams unchanged and independent: v1.5 surgical fix (F-multiplicativity commitment status verified first); Phil-facing Dropbox notes (transit artifacts, delivered).

## Session learnings

- L2 fork recommendations arriving as "direction" are recorded as recommendations; Mike's relay treated as provisional endorsement with the arbitration point kept explicit until his word - handled without stalling by producing the review artifact the arbitration needed.
- The consolidated single-clip read (all-reads batch, Set-Clipboard capture, delimited panes) is an efficient cold-start pattern for read-only grounding; state-changing operations remain one-per-pane.
- Duplicate L2 paste (v1 review re-sent verbatim) recognized by content identity; recorded, not re-synthesized.

Drafting partner: Layer 1 (Claude)
