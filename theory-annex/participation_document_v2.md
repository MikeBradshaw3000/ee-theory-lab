# Participation (v2)

**Status:** Exploratory-tier working document, version 2 (supersedes v1, 2026-09-05, same date); candidate Annex entry (TDA-003) if the Annex protocol is ratified. This version incorporates decisions D1–D6. **The decision set was ratified by Mike, 2026-09-05.** Section 8 is the decision record; Section 9 is the residual ledger. Self-contained: assumes only the base structure (v, c, r), Λ = F(v,c,r), the state variables ρ and Ψ, the action ontology, and (for situational coordinates) TDA-001.

---

## 1. The definition

**Participation:** χᵢ(t) = 1 if and only if, over a window W, agent i's action stream registers non-zero on viability (v) and social reinforcement (r), with cost of entrepreneurial participation (c) below unity, all evaluated at i's situational base-space configuration. Otherwise χᵢ(t) = 0.

**Density:** ρ(x, t) is the density of χ over location x's population measure — the coarse-grained field that the instrument's per-cell terrain approximates.

Elements of the definition:

- **All three bases, simultaneously (D1).** The condition preserves the asymmetry in c: non-zero registration on v and r, c below unity. If any base sits at its annihilating extreme — v = 0, r = 0, c = 1 — the agent is invisible to ρ. The condition is structurally mated to the multiplicative composition Λ = v(1−c)r: any annihilating extreme zeroes the product. Definition and composition assert the same thing at two levels — no base is dispensable, and no strength in one compensates for annihilation in another. This is the definitional face of base independence.
- **The window W (D5).** Literal instantaneous co-registration is measure-zero for event-like streams. Simultaneity means within-W: c-below-unity is a standing situational condition over the window, while v- and r-registration are events the window must catch. W is an **architectural parameter** — a declared timescale on which participation is defined, the same epistemic species as the Ψ window, not a tuning knob. The instrument already implicitly rules this way: discrete ticks make W = one tick by construction, so this decision aligns theory with existing practice at no cost to any flight.
- **Situational evaluation.** The configuration at which registration is evaluated is the agent's situational base-space point (TDA-001 §1, refinement), of which geographic location is the coarse proxy.
- **Order of definition.** Participation is the primitive; ρ is derived. The circular early formulation ("participation is contributing to ρ") is repaired by this ordering: participation is the registration; ρ is the measure aggregating registrations.

## 2. The geometric formulation

The three bases span the participation space. An action stream is a trajectory in time; participation is the stream's registration being non-zero in all three coordinates within W. The intersection of continuous stream and structural surface produces discontinuous crossings, marked by χᵢ(t). There is no partial membership and no degree of participation in the definition; degree-like structure lives elsewhere — in ρ as density, in Ψ as coherence.

Consequences:

**Participation is windowed and revocable.** χᵢ(t) switches off when any registration lapses beyond W. Nothing is joined, nothing is quit.

**Participation is relational.** Registration is defined against the bases as situationally configured; the same actions, transported to a different configuration, may register differently. Participation is a property of the stream-in-situation, not of the agent or the actions in isolation.

## 3. Attainable and realized projection (D2, adopted)

Two idioms in the April record — projection read off the stream (a mentor's actions constitute r-registration) and projection bounded by the situation (stigma forces r = 0; nothing the agent does can register) — are unified as follows:

**The terrain, as situationally configured, determines the attainable projection region; participation is realized registration, non-zero on all three coordinates, within that region.** Situational r = 0 collapses the attainable region so that no action from that situation registers as reinforcement, however the agent acts. Favorable terrain widens what is attainable without producing any registration by itself.

Architectural note: this articulation opens no second terrain-to-agent channel. Registration is a fact about the observational aperture — what counts — not an input driving the agent. The stream remains shaped only by Λ as locally configured.

## 4. What participation is not

**Not membership.** No roster, no enrollment, no status persisting independent of the stream. χ is the entire fact of the matter.

**Not experienced.** The theory does not ask whether the agent identifies as participating. An agent can participate without knowing the ecosystem exists, and self-identify intensely without participating. No interiority anywhere in the definition.

**Not contribution.** Ordinary language distinguishes participating from contributing meaningfully; the theory does not. All streams registering in ρ are participation. Whether streams compose into directional structure is Ψ's question, and conflating the two would smuggle an evaluation into a registration.

**Not intention or investment.** "Skin in the game" is an internal-state evaluation and is prohibited. An agent whose actions constitute reinforcement registers on r regardless of whether they care.

## 5. Two distinctions that do work

**Acting versus participating.** An agent can act — visibly, energetically, colloquially entrepreneurially — while registering zero on some base; such an agent is not participating. The r = 0 stigma case describes someone acting but outside the ecosystem. This distinction is a substantive output of the definition and survived its first designed test, with the recorded caveat that the test partly confirmed the definition rather than endangering it; the unforgiving test remains sufficiency, which has no definitional safety net.

**Permits versus occurs.** Λ > 0 means the terrain permits participation, never that it occurs. The favorable-conditions non-participant is not a puzzle: the stream didn't register, and the theory records that without explanation. Decision frameworks are forced into interiority here; this theory is silent on interiority by design.

## 6. Nearness to the boundary (D4, adopted)

**"Near the participation boundary" means |Λ − Λ*| is small, evaluated at the agent's situational configuration.** Grounds: base-space distance fails for want of a natural metric (the axes are incommensurable); susceptibility-based nearness is circular (large response is the consequence of nearness, not its definition); and nearness must live in the one quantity agents couple to, since Λ is the sole channel from structural conditions to agents.

Anisotropy is not lost — it relocates. Which base-space displacement most efficiently changes nearness is carried by the gradient of F at the situational point: near the activation surface, a small displacement along one axis may buy more δΛ than a large one along another (TDA-001 §2.2, the multiplicative-composition geometry). Nearness is scalar; the *cheapest direction of approach* is where the base structure speaks.

## 7. Relation to the cascade

ρ is participation density: the aggregate of χ, the quantity that rises through the first transition when Λ crosses Λ*. Ψ is not more participation; it is what participation can compose into when the μ(ρ) sign-change is crossed — directional structure among streams already registering. The two transitions, restated in this document's terms: first, conditions become sufficient for streams to register (participation appears); second, registration becomes sufficient for direction (coherence appears). Regime II is the regime of registration without composition.

Participation heterogeneity at a location decomposes exactly into TDA-001 §4's three legal differences — position (situational coordinates differ), draw (stochastic realization differs), projection (which bases the stream engages, and when, differ) — with no dispositional vocabulary required or permitted.

## 8. Decision record (ratified by Mike, 2026-09-05)

**D1 — Ratified: the all-three simultaneous requirement is committed.** Closes the April "candidate for commitment" flag deliberately. The requirement (non-zero on v and r, c below unity, within W) is adopted as the formal position, ending its ambient hardening.

**D2 — Adopted: the attainable/realized articulation (Section 3).** The sole architectural concern — a second terrain-to-agent channel — is retired: registration is aperture, not input.

**D3 — Rejected: the constituency-as-denominator structure.** One-base projectors do not define a theoretical population. Grounds: (i) ρ is a density over the coarse-graining unit's population measure in the committed architecture, and the quarantine of "fraction of the population" was the early warning against a special denominator; (ii) the April reasoning that partial projectors "feed Q" rests on an architecture violation — Q reads only (ρ, Ψ), so a mentor's actions modifying what other agents encounter would require the direct micro-to-terrain channel identified elsewhere as an uncommitted extension; (iii) TDA-001 supplies the disciplined replacement — partial projectors are texture in the within-location distribution over base-space: real, describable, candidate material for the extension horizon, but not a population in the committed formalism. This ruling accords with the April decision to withhold commitment.

**D4 — Adopted: nearness as |Λ − Λ*| at the situational configuration** (Section 6).

**D5 — Adopted: window-based simultaneity, W an architectural parameter** (Section 1). No change to any current flight; the instrument's tick already realizes W.

**D6 — Status fixed for χ-operationalization.** Not solvable by ruling; what is ruled is its classification: an instance — the central instance — of the empirical normalization problem, frozen in coordinate-assignment form, assigned to the measurement-theory horizon. Any location-grain proxy for χ carries the named assumption that within-location variance does not matter, which the resolution-ladder question (TDA-001 §6) can eventually test.

## 9. Residual ledger

**Committed (per Section 8 ratification):** the definition of Section 1 in full; the attainable/realized articulation; the nearness definition; the classification of χ-operationalization.

**Previously committed, unchanged:** the three bases and their bounds (r ≥ 0; stigma is r = 0, not negative); the action ontology; Λ as the sole channel; the geometric characterization with χᵢ(t).

**Open by design (not edges of this document):** the functional forms of F, μ(ρ), Q; the nucleation mechanism; the numerical value and empirical estimation of W beyond the instrument's tick.

**Extension horizon (explicitly outside the committed formalism):** direct micro-to-terrain coupling with actor-specific footprints — the channel that would be required for any future account of partial projectors' structural influence; flagged in the action-effects discussion as a genuine extension requiring care with base independence. Follow-up-paper material, not v1.5's.
