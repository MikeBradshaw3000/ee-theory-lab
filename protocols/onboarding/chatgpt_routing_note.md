# Layer 3 Engagement Returning for Synthesis — Flight 6 Substrate Spec v1

Routing Claude's independent Layer 3 review of the v1 specification. Independent engagement per protocol — Claude reviewed v1 without seeing your Layer 2 response first, then engaged your response after drafting. Below is the integrated comparison.

## Convergence

Claude concurs with your bottom line: v1 is substantially commit-ready with clarifications rather than architectural changes outstanding.

Strong convergence on:

- **Item A (pre-Q vs post-Q base logging).** Both layers identify this as the one substantively important item before commitment. Phase 4B residual analysis requires logged bases be the ones that produced the row's Λ, drive, and probability chain. Pre-Q required, post-Q optional as you specified.
- **Item C (base clipping count required).** Both layers support making this required reporting rather than optional. Consistent with the surfacing-hidden-dynamics discipline elsewhere in the spec.
- **Your prohibitions addition** ("Do not infer missing telemetry columns during analysis if the substrate failed to emit them"). Claude flagged this as strongly endorsed — it closes a failure mode the current prohibitions list doesn't quite cover, and applies the same anti-rationalization principle as pessimistic-on-passing.

## Partial divergence — Claude's extensions to your items

**Item B (ρ and Ψ indexing).** Claude agrees naming clarification is needed and wants to extend it. The indexing question is also a tick-semantics question: if Ψ_local is computed from ds(t) = is_active(t) − is_active(t−1), then Ψ(t) requires both tick t and tick t−1 activation states, while ρ(t+1) is the post-activation count at tick t+1. Parity hash sequence needs to be unambiguous about what is hashed at what tick boundary, not just what each quantity is named. Claude's extension: Section 6's tick-order pseudocode should explicitly mark hash-emission points.

**Item D (F_baseline parity scope).** Claude agrees and proposes tighter language: parity under F_baseline tests the channel, not the signal. The architectural claim being verified is "telemetry emission does not perturb dynamics," which is F-independent.

**Item E (Term_Lambda column).** Claude diverges here — wants Term_Lambda required, not recommended. Reasoning: the probability-chain decomposition into Λ-driven and density-driven terms is exactly what Phase 4B residual structure depends on. Having Drive_Raw without its Λ-attributable component forces analysis-stage reconstruction of something the substrate already computed. Same principle as your anti-inference prohibition.

## Items Claude raised that you did not flag

**Item F: Q update timing relative to Ψ_local computation.** Section 6 presumably orders: (1) compute Λ, drive, p_act per cell; (2) sample activation; (3) compute ds(t); (4) compute Ψ_local from ds(t); (5) apply Q from Ψ_local. The specification should make explicit that Q is applied after Ψ_local is computed for tick t and before tick t+1's Λ computation. This is implied but the ordering should be in canonical tick-pseudocode, not inferred. If your pre-Q logging clarification (Item A) is accepted, this ordering becomes the verification anchor: pre-Q bases logged at step (1), Δv/Δu/Δr logged at step (5).

**Item G: Realization-invariant verification granularity.** Section 14 requires zero mismatches reported per-artifact. Does this mean zero across all (cell, tick) pairs in the artifact, or zero when checked at a sampling rate? Published-paper reproducibility commitment suggests full per-(cell, tick) verification, but the specification should be explicit. If full verification is computationally costly for long runs, a documented sampling protocol is preferable to silent partial verification.

## Integrated Section 16.2 — combined draft

Combining both layers' contributions, Section 16.2 would read:

```markdown
### 16.2 Items surfaced by Layer 2 and Layer 3 cross-review

1. Telemetry timing clarification: required b_i_v, b_i_u, b_i_r columns record pre-Q base values used to compute Lambda_total, Drive_Raw, p_base, and p_act for that tick. Optional post-Q base columns may be added separately. (Both layers; Layer 2 originating.)

2. Parity series indexing clarification: hashed ρ(t) is post-activation for tick t; hashed Ψ(t) is computed from the same tick's activation-change correlation. Section 6 tick-order pseudocode should explicitly mark hash-emission points. (Layer 2 originating; Layer 3 extension on pseudocode marking.)

3. Base clipping counts required: per-tick clipping counts for v, u, r must be logged or summarized; nonzero clipping is surfaced in completion verification. (Both layers.)

4. F_baseline parity scope clarification: parity under F_baseline tests the channel (telemetry emission does not perturb dynamics), not the signal. Production F forms still require artifact-level realization-invariant verification. (Both layers; Layer 3 tightened framing.)

5. Term_Lambda = ALPHA * Lambda_total required, not optional. Probability-chain decomposition into Λ-driven and density-driven components is a Phase 4B analytical requirement; the substrate already computes this quantity and should emit it. (Layer 3 strengthening Layer 2's recommended-column proposal.)

6. Tick-order pseudocode in Section 6 must explicitly mark Q-application timing relative to Ψ_local computation: Q applied after Ψ_local computed for tick t, before tick t+1's Λ computation. With pre-Q logging (item 1), this ordering becomes the verification anchor. (Layer 3 originating.)

7. Realization-invariant verification granularity: Section 14 should specify whether zero-mismatch verification is full per-(cell, tick) or sampling-based. Full verification is the default; sampling protocols must be explicitly documented if adopted. (Layer 3 originating.)

8. Prohibitions addition: "Do not infer missing telemetry columns during analysis if the substrate failed to emit them. Derived columns are allowed only when explicitly specified; missing required telemetry means substrate failure, not analysis opportunity." (Layer 2 originating.)

No substantive architectural divergence identified between layers.
```

## Synthesis question for you

The items where Claude extended or strengthened your proposals (B pseudocode marking, E required Term_Lambda) and the two items Claude raised independently (F tick-order pseudocode, G verification granularity) — do any of these read as substantive divergence requiring further discussion before commitment, or are they all guardrail-level refinements compatible with your assessment?

If guardrail-level across the board, both layers converge on commit-readiness pending Section 16.2 resolution. If any rise to substantive, flag them and we run another synthesis cycle before routing to Mike's Step 4.

— Mike (drafted with Claude)
