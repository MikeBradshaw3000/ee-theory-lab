# Ruling Record — Brief 3: Merge Architecture

**Ruled by:** Mike, 2026-08-18, successor L1 conversation.
**Ruling:** **Option (a) — one unified execution path — with two binding attachments:**

1. **The Lineage B rule-equivalence gate is specified to L2's standard:** the merged become/survive branch reproduces B's p_become and survival values at matched inputs against B's own preflight-verifier pattern (`run_parity_check`), plus aggregate/distributional parity on ρ trajectories at matched seeds.
2. **Commit `4d9a622` is named in the merge specification as Lineage B's canonical executable reference** — the pinned repository code is the ancestor's museum copy and the executable verification target for the future substrate rebuild; no live `lineage_b_native` mode is carried.

## Architecture as ruled

Single RNG regime: Lineage A's single explicit Generator; B's legacy-global regime is not carried. Single update-rule framework with the become/survive branch as a rule mode within it. Ancestor gates: **one bit-exact gate** (Lineage A, channels-zeroed limit, matched seed, conditional on draw-order discipline per S6(a)) and **one rule-equivalence gate** (Lineage B, per attachment 1). B's observable-null machinery is rebuilt onto Generator draws (S1(c)(5)); the rebuild is certified by the rule-equivalence gate, not by preservation.

## Rationale (as ruled, following discussion)

The witnesses exist to certify that the new instrument preserves what the ancestors established. A's bit-exact gate certifies the physics core the flight stands on. B's hypothetical second bit-exact gate would certify a native mode whose merged-instrument counterpart is a mandatory rebuild regardless (the null machinery cannot survive the RNG port) — it would certify the museum copy, not the working instrument; the working instrument's observables are certified by rule-equivalence either way. Meanwhile option (b)'s costs are concrete: two RNG backends in one codebase, a three-mode specification, and a tripled wrong-values-under-right-names surface — the program's named most-dangerous defect class, whose natural habitat is mode-conditional code. The D2 ruling weighed here: Q_read ∈ {local, global} already adds one switchable axis; compatibility modes would compound to six behavioral configurations multiplicatively. The one genuine benefit of (b) — both ancestors as live executable rebuild targets — is preserved sufficiently by attachment 2: the pinned commit is executable and canonical.

## Consequences for drafting

- The merge specification's parity section is now fully unblocked and writable: one bit-exact A gate (S6(a) conditions), one rule-equivalence B gate (L2's standard), `4d9a622` named as B's reference, D4's zero-amplitude no-draw bypass preserving the conditional A gate, and the MFP parity bridge (predeclared projection-level recovery targets) as its third, distinct certification layer — ancestor gates certify preservation; the bridge certifies recovery. The spec must keep these three certifications nominally and functionally separate.
- L2's "new experimental instrument with two ancestor witnesses" framing enters the specification language, as pre-committed under either ruling.
- Naming ledger addition owed at spec time: rule-mode dispatch labels for the become/survive branch vs. the symmetric chain, guarded against the wrong-values defect class alongside Q_read.

**D5 remains the sole open arbitration.**

*End of ruling record.*
