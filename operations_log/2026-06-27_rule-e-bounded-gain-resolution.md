# Operations log - 2026-06-27 - Rule E bounded-gain design resolution (modified Candidate A selected)

**Session:** 2026-06-27 (slug 2026-06-27_rule-e-bounded-gain-resolution)
**Layer 1:** Claude (architectural guardian, vocabulary enforcer, routing-note author)
**Execution channel:** Mike (sole; all PowerShell run by Mike, Claude drafts and routes)
**Layer 2:** ChatGPT (mean-field substantive review / recommendation)
**Layer 3:** not engaged (no implementation; design-level only)
**Entry HEAD:** ba79726 (Rule E first-pass scoped negative recorded; bounded-gain pass named-not-triggered, no construction selected)
**Exit HEAD:** this commit (bounded-gain construction resolved at the design level; still unseeded)
**Result:** modified Candidate A selected as the first bounded-gain follow-up construction; B and C held as conditionally-admissible alternatives under a formal freeze discipline; NON-SEEDING

## What this session did

Opened and resolved the Rule E bounded-gain follow-up at the design level. The session opened a non-seeding design-resolution memo proposing three candidate gain-control constructions, routed it to Layer 2 for review before any spec, took Layer 2's review and recommendation, and arbitrated the selected construction into a design resolution. No run was seeded; no implementation spec was drafted; Layer 3 was not engaged.

## Cold-start grounding and session-open housekeeping

Cold-start grounding confirmed entry HEAD ba79726, tree clean, anchor read. One untracked pure-read helper (read_obs001_nearnull_scale.py) was gitignored as wave-two read-helper scaffolding (literal-enumeration entry, committed 8e431ee) before substantive work, clearing the cold-start untracked-file noise. The Rule E first-pass result-recording bundle from the prior session (findings a56731c, anchor refresh ba79726) was confirmed in the committed record and governing.

## The bounded-gain proposal memo (non-seeding)

A non-seeding design-resolution memo was drafted proposing three candidate gain-control constructions for a possible bounded-gain follow-up, each required to preserve the full Rule E admissibility envelope (block-lagged only; Lambda-configuration locus / becoming-active channel only; no leak into survival or turnover; the four fenced forms; separability at alpha=0). Candidate A: direct bound on the realized conditioning term. Candidate B: alpha ladder recalibrated against a conditioned-excursion scale via direct displacement targeting. Candidate C: two-scale standardization with a frozen conditioned-scale denominator. The memo did not rank the candidates and made the dynamic-centering fence the load-bearing review question - specifically whether B and C, which lean on a measured-once-and-frozen conditioned-scale constant, collapse into dynamic centering against rho or hold. The memo seeded nothing and authorized no Layer 3 work.

## Route-first decision and the L2 routing packet

Per Mike's route-first decision, the memo was NOT committed before review. A self-contained L2 routing packet was built (continuing-context note + full memo + the contract's load-bearing clauses - Section 1 admissibility conditions and four fenced forms, Section 4 separability, Section 3 honest-scope bound - inline, no placeholder, since L2 direct-fetch remains non-functional). The packet led with the genuine question (do B/C collapse into dynamic centering under their freeze discipline) and explicitly invited Layer 2 to flag conflicts and to resist soft convergence.

## Layer 2 review and recommendation

Layer 2 accepted the bounded-gain memo as an admissible design-resolution artifact and recommended modified Candidate A as the first follow-up construction, holding B and C as conditionally-admissible alternatives. Substantive content of the review:

- Dynamic-centering crux: B and C do NOT collapse into dynamic centering merely by using a conditioned-scale constant, PROVIDED a strict formal freeze discipline holds. Layer 2 hardened the informal freeze into seven binding conditions (M_ref stays un-conditioned reference; conditioned scale measured in a separate run; frozen before the swept run; not recomputed by seed/window/tier/flag/running-rho; characterization run not tuned on observables or LowLow; scale used only in the becoming-active channel; alpha=0 still bypasses to exact recovery). The margin is thin and the discipline must be formal, not informal.
- Tier-specific bound (the catch): Layer 2 caught that Layer 1's proposal specified a single global d_max for all tiers, which reproduces the first-pass identical-tiers pathology in bounded form - small tiers saturate to the same maximum as large tiers when g_E is large. Fix: each tier d_j gets its own bound |Delta_j| by logit inversion at base p_Lambda=0.40, so the tier determines its own maximum realized displacement.
- Smooth over hard clip: tanh preferred for the first bounded pass; hard clipping creates flat plateaus and a discontinuous relay. Hard clip not fenced, just not the selected first-pass shape.
- Saturated-channel-candidate flag: if a candidate appears only while the bound is active nearly always, record it as a saturated-channel candidate, not a clean responsive-channel candidate, pending audit. New discriminator alongside the lag-dynamics and inert-channel guards.
- B/C not selected: both require a separate characterization run (a later seeding decision and an added ambiguity surface) and both retain a linear-gain mis-sizing risk; C additionally keeps the unbounded linear form and so inherits the first pass's main structural risk.
- Failure precision: the first-pass failure was calibration-internal to the UNBOUNDED standardized-gain construction and exposed an over-driven feedback mode; it does not close Rule E but argues against another unbounded linear standardized pass as the next instrument.

## Arbitration and the design resolution

Mike arbitrated modified Candidate A in. The design resolution was drafted recording: the selected construction (smooth tier-specific bounded realized term, each tier capped at its own Delta_j by logit inversion at p_Lambda=0.40, alpha=0 bypass preserved); the additional block-resolved diagnostics (raw g_E, pre-bound term, post-bound term, effective Lambda, bound-activation frequency) and the saturated-channel-candidate flag; B and C held under the seven-condition formal freeze discipline; the carried failure-precision; and a synthesis note recording the convergence as genuine-with-a-caveat. The resolution is non-seeding: no spec, no run, no Layer 3.

## Synthesis discipline recorded

The convergence on modified-A is recorded as genuine-with-a-caveat. Layer 2's selection rests on grounds independent of Layer 1's framing (the unbounded-linear-risk argument against C; the characterization-seed economy of A) and caught a real defect in Layer 1's A (the global-d_max identical-tiers pathology) - independent evidence of substantive engagement, not soft agreement. The caveat: Layer 1's proposal memo had already framed A as the simplicity / seeding-economy option, so part of L2's A-preference may be Layer 1 framing returning through L2. This does not overturn the selection (the tier-specific catch and unbounded-linear-risk argument go beyond the simplicity point) but is recorded so the selection is not treated as fully independent arbitration. B and C are held as genuinely admissible-under-discipline, not dismissed - the freeze was hardened by L2, not waved off. The tier-specific catch is recorded in the lineage of the Rule D R3 saturation catch (L3-surfaced) and the lag upper-bound correction (L2, 2026-06-05): an external layer correcting a Layer 1 construction defect.

## Committed this session (one commit)

Design resolution (RULE_E_BOUNDED_GAIN_RESOLUTION.md), this ops log, and a light anchor refresh (Rule E horizon line updated from "named-not-triggered, no construction" to "bounded-gain construction resolved to modified-A, B/C held, still unseeded") - committed together. The bounded-gain proposal memo and the L2 routing packet were transit artifacts (route-first); the resolution supersedes the proposal memo and is the committed record of the construction selection.

## What remains Mike's call

The natural next artifact, when and if opened, is the bounded-A implementation spec (honoring this resolution, the contract, the opens resolution, the F3 alpha-zero bypass constraint, the Section 3 additional diagnostics and saturated-channel flag, and the Layer 3 recording structure). Drafting that spec is Mike's call; seeding its run is a further separate call. The standing HOLD on further wave-two seeding is unchanged; this resolution is a design-level open resolved, not a seed.

Drafting partner: Layer 1 (Claude), routed and executed by Mike.
