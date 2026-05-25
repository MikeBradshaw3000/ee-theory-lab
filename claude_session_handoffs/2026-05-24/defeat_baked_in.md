# The "Baked In" Defeat Condition — What the ABM Must Produce

*Strategic half (Layer 1 / Mike / manuscript). Sets the discrimination any Layer 3
measurement design must satisfy to count as defeating the objection, and supplies the
defense logic for the manuscript's Plausible-Mechanism section. Governed by
pessimistic-on-passing and sufficiency-tested-not-asserted.*

## 1. The objection, stated at full strength
A reviewer says: the two Landau normal forms were written with a coherence coupling
constrained to be non-positive at low activation density. Integrating them therefore
*must* yield a regime where ρ is lifted and Ψ is near zero. The MFA "demonstration"
shows what was assumed. Regime II is an artifact of the formalism, not a finding.

## 2. The trap a naive ABM walks into
Putting the same dynamics on a grid does not answer this. If each cell's coherence
quantity is updated by a rule that is a discretization of dΨ/dt = (coherence
coupling)·Ψ − γΨ³ — i.e., if the density-keyed sign-change is wired into the local
rule — then the ABM re-encodes the assumption at finer grain. The divergence "appears"
because it was installed cell-by-cell. A sharp reviewer rightly calls this baking-in at
higher resolution. **The measurement signature alone cannot defeat the objection.**
What defeats it is where the signature comes *from*.

## 3. The defeat condition (a conjunction, not a single test)
The ABM produces a defeating result only if all three hold together:

**(A) Clean agent-rule audit.** The agent-level rules contain no representation of the
two-stage cascade: no second-order dynamic keyed to density, no coherence coupling whose
sign flips at a set activation level, no normal form. They contain only (i) action in
response to *local* structural conduciveness (the candidate local composition, e.g.
v(1−c)r — not committed), and (ii) a coherence contribution that accrues *only* through
co-activation with neighbors. Agents act; nothing decides.

**(B) Emergent signature.** From those rules, the macroscopic (ρ, Ψ) reading exhibits a
range of structural conduciveness where ρ is substantially lifted while Ψ remains near
zero, with Ψ liftoff occurring at higher conduciveness than ρ liftoff.

**(C) Traceability.** The gap is attributable to the relational mechanism — insufficient
co-active multiplicity at low ρ — and not to any coefficient, threshold, or measurement
choice (see §5).

The reviewer-defeating claim is the conjunction: *the rules carry no two-stage structure
and no density threshold, yet the high-activation / low-coherence regime appears and
persists, because coherence is relational and a sparse grid cannot supply the mutual
reinforcement coherence requires.*

## 4. The ontological hinge — and why it is not itself a baked-in choice
A reviewer's natural counter: "you chose a relational coherence rule because you knew it
would open the gap — so the gap is baked into the rule." The answer is that relationality
is not a free modeling choice. Coherence *is* mutual, system-level reinforcement; mutual
reinforcement requires a multiplicity; a single actor cannot reinforce itself. The
relational character of the rule is *entailed by what coherence means*, the same
ontological constraint that closes the low-density μ(ρ) vulnerability in the MFA.

This is the strongest available form of the defense: **one primitive replaces two assumed
normal forms.** In the MFA, the regime structure looks installed by two equations. The
ABM shows that a *single* ontological commitment — coherence is relational — is
sufficient to produce the same regime structure on a discrete substrate, with the second
"equation" never written down. What looked assumed is shown to be a consequence.

## 5. Alternatives that must be ruled out (pessimistic-on-passing)
A signature passable by any of these is too weak. Each needs its discrimination; note
which are code audits versus measurements.

1. **Discretized-equation artifact** *(code audit — the decisive one)*. The local
   coherence rule is a disguised discretization of the second normal form. Discrimination:
   inspect the rule that updates the per-cell coherence quantity. It must not reference ρ
   and must not contain a sign-changing, density-keyed coefficient; it must grow only
   through actual co-activation. If it passes this audit *and* the gap still appears,
   baking-in is excluded. This is sufficiency-tested-not-asserted: do not accept "we
   measured Ψ"; test that the rule producing Ψ does not contain the result.
2. **Smuggled threshold** *(code audit)*. A "relational" rule that nonetheless fires only
   above k co-active neighbors is the sign-change in disguise. Discrimination: the
   coherence contribution must be continuous in co-activation with no hand-set neighbor
   threshold. Threshold-like behavior in (ρ, Ψ) space emerging from a thresholdless local
   rule is the genuine result; a set k is the reviewer's point conceded.
3. **Measurement/definitional artifact** *(measurement)*. The Ψ aggregate reads near-zero
   from how it is aggregated (signed cancellation, density-suppressed normalization), not
   from absent coherence. Discrimination: use a Ψ aggregate that registers spatial
   mutual-reinforcement structure (the B2(A) spatial-autocorrelation lineage), not a naive
   mean of the per-cell quantity; verify against a positive control — a configuration
   known to be coherent must read high Ψ.
4. **Saturation / scaling / transient** *(measurement)*. The gap is a units mismatch or a
   slow transient on the way to coherence, not a regime. Discrimination: hold conduciveness
   fixed to steady state; Regime II must be a persistent steady state with ρ activated and
   Ψ near zero — consistent with the manuscript claim that Regime II is real and persistent,
   not a way-point.
5. **Trivial low-density** *(measurement)*. ρ-up/Ψ-zero observed only where ρ barely
   clears its own liftoff is just "little happening." Discrimination: the signature must
   hold where ρ is well above its liftoff while Ψ stays near zero; the conduciveness gap
   between the two liftoffs must be non-trivial.

## 6. Scope — what this can and cannot establish (honest framing)
The ABM does not confirm the theory. It converts "you assumed the divergence" into "the
divergence is robust to specification — it appears even when the two-stage structure is
not written into the dynamics, from a single ontological primitive." That is a
defeasibility result, not a proof, and the manuscript should claim exactly that and no
more. A candidate measurement produces, or fails to produce, the divergence; it does not
demonstrate the theory.

## 7. Load-bearing flag (Layer 1 cannot close this from here)
The decisive discrimination (§5.1) is an audit of the rule that updates the per-cell
coherence quantity in the actual Flight 6 substrate (`Psi_local`). That rule is past
Layer 1's memory horizon. Whether the existing substrate already defeats the objection
turns entirely on how `Psi_local` is computed: if from a relational, thresholdless
co-activation rule, the existing runs may carry the result; if from a μ-discretization,
no aggregate over them can defeat baking-in, and a new substrate with audited local rules
is required. **First action before any measurement: confirm the `Psi_local` update rule
against §5.1 — Mike/Layer 3, against the substrate.**
