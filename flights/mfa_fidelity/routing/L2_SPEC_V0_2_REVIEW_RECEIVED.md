# Received Record — L2 Adversarial Review of Merge Specification v0.2
**Provenance:** Received from L2 via Mike, 2026-08-19/21, successor L1 conversation. Verbatim below the rule. Verdict: ACCEPTED WITH REQUIRED REFINEMENTS (nine, enumerated in its disposition). All nine were integrated into Merge Specification v0.3, which awaits L2 integration verification and Mike's freeze. The named §12.6 question (Gate-A Γ_ρ bypass) was answered NECESSARY BUT NOT SUFFICIENT with a two-level harness design, adopted in v0.3 §8.1.

---
L2 Adversarial Review — Merge Specification v0.2

Overall verdict: ACCEPTED WITH REQUIRED REFINEMENTS.

The architecture is coherent with the post-arbitration record, and the three certification objects are kept properly distinct. I find no reason to reopen D2, D5, Brief 3, MFP, or the jeopardy split. The named §12.6 question does expose a real issue, however: the proposed Γρ bypass is necessary for Gate A but not sufficient to establish bit-exactness. I also find several specification-level defects outside §12.6 that should be corrected before v0.3 freezes.

1. §12.6 — Gate-A Γρ bypass

(i) Is absent-not-zero sufficient?

VERDICT: NECESSARY BUT NOT SUFFICIENT.

The proposed construction is correct:

> Γρ = 0 → do not read activation_input → do not compute the ρ contribution → do not execute the added arithmetic.

That is substantially stronger than computing Gamma_rho * activation_input and obtaining numerical zero. It prevents the extended channel itself from perturbing the ancestor computation.

But Gate A certifies the merged implementation, not the algebraic equivalence of one new term. Refactoring can break bit identity without changing PRNG consumption.

There are at least four independent failure surfaces:

1. PRNG sequence: initialization and realization draws must remain identical.

2. Arithmetic expression/order: the surviving Ψ-Q calculation must execute with the same floating-point operation ordering as A.

3. State/update ordering: Q and clipping must occur at exactly the ancestor locations in the chain.

4. Telemetry/recomputation side effects: added instrumentation must not alter state, evaluation order, dtype, or stochastic consumption.

Thus the correct claim is:

> The Γρ no-read/no-arithmetic bypass removes the activation extension as a source of Gate-A divergence. Bit-exact preservation remains an empirical property of the complete channels-zeroed merged execution path and is established only by Gate A.

That is the same sufficiency-tested-not-asserted discipline already stated in the question.

(ii) Does the bypass need a preflight element?

YES.

I recommend a two-level Gate-A harness.

Structural preflight: establish before the full ancestor comparison that with Γρ=0:

the activation-read function/callback is never invoked;

no rho_global calculation is requested for Q;

no local-density access occurs for the Q activation term beyond whatever A independently requires for its ordinary drive;

Delta_from_rho is either structurally absent/disabled in Gate-A comparison output or emitted as a telemetry-only exact zero without entering the state-update expression;

noise-stream construction/draw is likewise absent under η_MFA=0;

dynamics-stream draw count/order equals the ancestor's expected consumption.

The key distinction in the third item matters because A already computes local density for its drive. Gate A cannot require "local density is never read"; it can require that extended Q does not introduce an additional Q-side read or computation.

Behavioral certification: run the complete matched-seed ancestor comparison and require bit-exact state/telemetry equality over the specified Gate-A horizon.

I would not make the structural preflight a substitute for bit-exact comparison. Its purpose is diagnostic: if Gate A fails, you can distinguish a bypass violation from some other refactoring divergence.

(iii) Is the symmetry with the D4 noise bypass valid?

Only partially. Revise the wording.

Both obey the same design principle:

> a disabled extension should contribute no execution capable of perturbing the ancestor path.

But they guard different things.

The η_MFA bypass primarily protects PRNG isolation/consumption plus removal of noise arithmetic.

The Γρ bypass protects arithmetic and data-access identity; the ρ channel itself consumes no PRNG draws.

So I would replace "symmetrical to the noise bypass" with:

> the same zero-channel structural-bypass principle used for η_MFA, applied here to a deterministic arithmetic/read extension.

Calling them symmetrical could imply identical failure modes when they are not.

2. §4.3 contains a more important Q issue

The minimal linear Q form is sensible and correctly avoids baking P4 into a Ψ-gated law. But this sentence is potentially stronger than the equation earns:

> "two committed coefficients, uniform across bases, preserving Q's diagonal structure (base independence as architectural product)."

A common ρ and Ψ driver applied to all three bases can generate correlation among their changes, even without cross-base causal terms. That does not violate the manuscript's intended independence, but "diagonal" needs to mean:

> no base value enters another base's update equation as an input.

It must not mean statistically independent base trajectories.

I recommend stating that explicitly, especially given the earlier Base-Space Registration distinction between common-cause correlation and coupling.

There is also a sign/orientation issue the spec needs to make explicit. The manuscript's bases are v,c,r, whereas the substrate uses v,u=1-c,r. An ecosystem-improving Q should move u upward when the corresponding MFA statement would move c downward. The spec should state once, mechanically, that Q operates on substrate u_base, and all Γ signs/telemetry are interpreted in that coordinate system. Otherwise a later contract can accidentally reason in c while code updates u.

3. §1.2 become/survive wording needs surgical clarification

You say the unified framework uses the Lineage A 13-step chain, then describe become_survive as B's asymmetric rule.

The specification should explicitly identify which portions of the 13-step execution skeleton remain common and which probability construction is replaced by rule-mode dispatch.

Otherwise an implementer could reasonably build either:

A's entire p_base→p_act construction and then layer become/survive on it, or

dispatch before that construction and compute B's probabilities directly.

Only one can be the intended rule-equivalent B implementation.

Since wrong-values-under-right-names is already your named dangerous defect class, the merge spec should make this impossible to infer incorrectly.

4. §5.1 initialization is currently under-specified and risks Gate A

This is the most significant general issue after Q.

You propose:

> init_activity ∈ {bernoulli_p, fixed_count}

and say A's Bernoulli and B's exact-count schemes are carried.

Fine. But Gate A requires more than selecting bernoulli_p. It requires A's exact initialization algorithm, including draw ordering relative to sequential base initialization.

Therefore the configuration surface needs to distinguish parameter choice from algorithmic lineage. At minimum, Gate A must freeze:

exact base-draw order;

exact activity-draw location in that order;

exact shape of Generator calls;

dtype/coercion behavior if relevant.

Likewise, B's fixed-count mode rebuilt with Generator.permutation is a new merged-instrument implementation, not preservation of B's legacy RNG behavior. The spec mostly understands this; §5.1 should say it explicitly.

5. §7.3 hash definition is not yet reproducible enough

"SHA-256 over the telemetry parquet(s) + config JSON" needs a canonical byte-level construction before freeze.

Questions otherwise remain:

parquet file ordering;

whether filenames enter the digest;

JSON serialization ordering/whitespace;

separator between constituent byte streams;

whether the manifest containing the hash is itself part of config;

multi-file telemetry ordering.

This is not a contract threshold; it belongs here at instrument level.

Define something like a canonical ordered artifact list plus canonical JSON serialization and hash exactly those bytes. Otherwise two semantically identical runs can hash differently, or worse, implementations can disagree about what the hash certifies.

6. §8.2 Gate B has one conceptual wording problem

This phrase:

> "aggregate/distributional parity on ρ trajectories at matched seeds"

should not imply seedwise trajectory identity under different RNG regimes.

Because B's RNG has deliberately been rebuilt, "matched seeds" do not create matched stochastic histories in the ancestor and merged instrument.

The rule-equivalence portion can be deterministic at matched inputs. The trajectory portion should be distributional/aggregate across a declared seed ensemble unless the verified B preflight gives you a stronger justified pairing construction.

I recommend separating:

B1 — deterministic rule equivalence: matched input states → identical p_become and p_survive.

B2 — dynamical distributional equivalence: declared ensemble → predeclared aggregate/distributional agreement of ρ behavior.

That prevents "matched seed" from quietly becoming a false pairing claim.

7. §8.3 Gate R is correctly separated, with one boundary to preserve

I approve the decision to put numerical recovery targets and tolerances in contracts rather than this merge specification.

But the spec should make explicit that Gate R machinery validation precedes Gate R scientific evaluation.

The implementation can first prove that it correctly computes the projection quantities. Only afterward does a contract ask whether those quantities recover MFA predictions.

That gives you:

R0: projection/reduction implementation correctness;

R1: scientific recovery against predeclared targets.

I am not insisting on those labels, but I am insisting on the distinction. Otherwise a failed recovery can become ambiguous between "the stream-level realization failed" and "the averaging bridge was implemented incorrectly."

That distinction follows directly from MFP's newly load-bearing status.

8. §9.2 manifest timing is excellent, but hash timing needs reconciliation

I strongly endorse:

> manifest written before the run from the config object the run actually consumes.

That is exactly the right defense against configuration transcription.

But §7.3 then says the end-of-run manifest hash is recorded in the run manifest.

So distinguish:

pre-run immutable configuration manifest from post-run completion record/hash augmentation, or use two files.

Do not permit the implementation to rewrite the supposedly pre-run authoritative configuration object after execution without an explicit immutable-config boundary.

A clean model would be:

run_config.json — frozen before execution, hashed itself;

run_record.json — emitted after execution, references the config hash and records telemetry hashes/environment/completion metadata.

The exact names are yours. The epistemic separation is the requirement.

9. §7.1 telemetry wording needs one correction

The parenthetical:

> "conditional Noise_Draw/rho_global"

groups two things that have different conditions.

Noise_Draw is conditional on η_MFA being enabled.

rho_global is required at least whenever Q_read=global, and may also be required by Gate R regardless of Q mode because aggregate ρ(t) is a recovery quantity.

So do not make rho_global merely conditional telemetry in a way that permits local-primary MFP runs to omit it. Gate R requires aggregate ρ in local mode precisely because local→aggregate recovery is the question.

10. One thing I specifically do not challenge

I do not object to the specification deferring E1–E5 thresholds, tolerances, regime definitions, stain-discriminator verdicts, persistence guards, or recovery target values to contracts.

That separation is correct. Pulling them into the merge specification would actually weaken outcome hygiene by mixing instrument construction with scientific scoring.

Likewise, I see no interpretation creep in carrying F_baseline as legacy-unused, provided the arbitration requirement remains hard.

L2 disposition for v0.3

Named §12.6 question: ACCEPTED WITH REQUIRED REFINEMENT. Retain the Γρ absent-not-zero bypass, add structural preflight, keep full bit-exact Gate A as the actual certification, and replace "symmetrical" with the common structural-bypass principle.

Full specification: ACCEPTED WITH REQUIRED REFINEMENTS before freeze:

1. define Γρ bypass as necessary, not self-certifying;
2. add Gate-A structural bypass/draw-order preflight;
3. clarify Q diagonal independence versus common-driver correlation and explicitly orient Q in u=1-c coordinates;
4. specify the common execution skeleton versus rule-mode probability dispatch;
5. make Gate-A initialization algorithm/draw ordering explicit;
6. canonicalize the hash construction and separate pre-run configuration from post-run run record;
7. split Gate B deterministic rule equivalence from ensemble-level dynamical equivalence; remove unjustified seedwise pairing language;
8. distinguish Gate-R bridge implementation correctness from scientific recovery;
9. require rho_global telemetry in local-primary recovery runs, not merely global-Q runs.

I find no architectural reason to reject the unified instrument. These are mostly places where the specification currently knows what it means but has not yet made it impossible for an implementation to mean something else. That is exactly what the merge specification needs to eliminate before code exists.

*End of received record.*
