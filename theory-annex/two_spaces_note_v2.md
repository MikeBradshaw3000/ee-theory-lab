# Note: Two Spaces — Geographic Space, Base-Space, and Action Streams (v2)

**Status:** Exploratory-tier working note, version 2 (supersedes v1, 2026-09-05, same date). Drafted in an off-protocol discussion; carries no standing until Mike routes and tiers it. Sections 1–2 and 4–5 clarify committed architecture; Section 3 contains flagged candidate claims; Section 6 contains a flagged future-instrument question.

---

## 1. The distinction

The project uses "space" in two unrelated senses. This note makes the distinction explicit so architectural reasoning and manuscript prose cannot conflate them.

**Geographic space** is where agents are located: the substrate lattice, neighborhoods, the region. Points in it are *locations*. In the committed architecture, geographic space functions as an interaction structure — it fixes adjacency and the footprint over which perturbations land. The specific lattice geometry is an accessory assumption of the instrument, not a commitment of the theory.

**Base-space** is the abstract three-dimensional space with coordinates (v, c, r). Points in it are *conditions* — configurations of structural circumstance. The theory's central objects live here: Λ = F(v, c, r) is a function on base-space; the activation threshold is a surface in base-space; the regimes partition base-space (together with the state variables ρ and Ψ). Base independence is a statement about the axes of this space — three orthogonal directions, none a function of another — enforced architecturally by Q's diagonal structure.

**The terrain maps geography into base-space.** At the instrument's resolution, the terrain assigns one base-space point to each location: a base-space-valued field over geographic space. Λ becomes a scalar field over the lattice by composing F with this map.

**Refinement (situational coordinates).** The one-point-per-location terrain is a coarse-graining. In a real place, a single location contains many agents, and the (v, c, r) bearing on each agent's action stream is *situational*: two agents in the same building face different transition costs, different reinforcement, different viability access. The architecture's existing phrase — Λ *as locally configured* — already carries this: "local" is ultimately local to the agent's situation, with geographic locality as proxy. What geography does is *correlate* base-space positions without collapsing them: co-located agents share rents, institutions, and the same landing perturbations, so their coordinates cluster. A location is therefore a **distribution over base-space**, not a point; the instrument's terrain field is the coarse-grained summary of that distribution.

## 2. Consequences

**2.1 Proximity in one space implies nothing about proximity in the other.** Two adjacent neighborhoods can occupy distant base-space regions; two cities on different continents can occupy nearly the same one. This asymmetry is the theory's universality claim in structural form: dynamics depend on base-space position; geography enters only through the interaction structure and the spatial texture of the terrain map. The same asymmetry recurs at agent scale (Section 4): two agents at one address can sit far apart in base-space.

**2.2 Actions decompose into a where and a what.** Every action on structural conditions has a geographic support (footprint) and a base-space displacement (the vector δ(v, c, r) written at each supported location). A mayor's public endorsement: wide footprint, displacement almost entirely along the r-axis. A new fund: narrow footprint, displacement mostly along v. "Magnitude" decomposes into footprint size, displacement length, displacement *direction*, and local susceptibility where it lands. Direction matters because F is not isotropic: near the activation surface, a small displacement along one axis may cross it while a large one along another does nothing — the multiplicative-composition property of F expressed geometrically. Effect size is a joint property of the action and the system state, not of the action: susceptibility grows near the transitions, so an identical act is inert deep in Regime I and can be decisive near the second transition.

**2.3 The empirical normalization problem is a coordinate-assignment problem — with a named silent assumption.** Locating a real region in the formalism means constructing its terrain map from measurable quantities. Because real data arrives aggregated by geography while the coordinates are situational, any location-grain measurement silently assumes that within-location variance does not matter to the dynamics. That assumption now has a name and a place in the formalism (Section 6), which means it can eventually be tested rather than inherited.

## 3. Worked example: districts and density

The innovation-district phenomenon (Brookings; Katz & Wagner) makes the distinction earn its keep.

**A district is a shape imposed on the terrain map, not a base-space object.** District-building takes a finite budget of base-space displacement and compresses its geographic footprint: co-location pushes c down over a few blocks, proximity pushes r up, anchor institutions push v. "District" is geographic; the conditions it creates are base-space. The Brookings literature runs these together for lack of the decomposition.

**Local supercriticality.** Substrate dynamics are local, so what matters at a location is local activation density, not the regional aggregate. Concentration concentrates activation: a district can push a small patch past thresholds the surrounding region is nowhere near, while the region idles in Regime I or II.

**Candidate claim (open element, flagged):** a functioning district is a *nucleation site* — a small region in which the coherent phase forms locally and from which it may or may not propagate. The nucleation mechanism is a declared open element; the district phenomenon is a candidate empirical handle on it, not an application of settled theory. Whether districts nucleate coherence or remain high-ρ islands is a Regime II/III question at sub-regional scale.

**Situating without adopting.** The Brookings causal story (spillovers, networking, serendipity) is interaction- and decision-level narrative and is not imported. The retained observation: density works, when it works, because geographic concentration alters local base configuration and local activation density, moving a patch of the map relative to the transition surfaces. Failure cases — districts reproducing the geographic form and producing nothing — are concentration that moved buildings without moving base-space position, or displacement landing on low-susceptibility terrain. Same geographic form, different base-space result: the district-scale instance of the modest-resources puzzle, and the reason district playbooks do not copy between cities.

**Candidate claim (stronger, held loosely):** if coherence nucleates and propagates, the effective boundary of an ecosystem is the geographic support of the Ψ ≠ 0 pattern — an output of the dynamics, not an input assumption, and not necessarily coincident with administrative or self-declared boundaries.

## 4. Action streams: heterogeneity without dispositions

Different action streams at the same geographic location do not behave the same. The architecture accounts for this through exactly three channels, none of which requires heterogeneous agents:

**4.1 Position.** Co-located agents occupy different situational base-space points (Section 1 refinement) and therefore sit at different distances from the activation surface. A single perturbation — one footprint, one displacement direction — produces divergent effects across streams because effect depends on each situation's position relative to the surface: an agent deep in the supercritical region barely registers it; one just below may be carried across; one far below moves without observable change. Heterogeneous response with zero heterogeneous interpretation: no dispositions, no preferences, no deliberation. The variation lives in the geometry of situations.

**4.2 Realization.** Activation is stochastic. Two agents at identical base-space points produce different sample paths — same statistics, different streams. The ensemble is homogeneous; every realization is individual.

**4.3 Projection.** Participation is geometric: a stream projecting non-zero onto all three bases simultaneously, with intersections marked by the χᵢ(t) indicator. Streams at one location differ in which bases their actions engage and when — one thick with r-relevant action and never touching v, another crossing all three surfaces intermittently.

"Not all acting the same" thus decomposes into three legal kinds of difference — different position, different draw, different projection. Where prose is tempted toward "some agents are more entrepreneurial," the architecture supplies "some situations sit nearer the surface, and some realizations crossed it" — sayable, and unlike the dispositional version, measurable in principle.

**Connection to the literature.** The within-location distribution is one of the *textures* existing research streams describe: the networks stream largely concerns per-agent variation in r; the opportunity stream, per-agent variation in v-access. This strengthens their standing as candidate feedstocks for the open functional forms — empirical windows into the distribution the current abstraction integrates over, not rivals to it.

## 5. Guards

**5.1 Lake Vision.** The lake surface is geographic space; the genealogical image contains no base-space. The metaphor cannot carry this distinction and must not be asked to.

**5.2 Manuscript prose.** Management readers will hear "space" as geography on every occurrence. Wherever base-space appears in Phil-facing prose, it requires an unmissable introduction ("the space of structural conditions," or equivalent) on early uses.

**5.3 Vocabulary.** The two-space framing does not license scalar summaries of conditions ("conduciveness," "favorability"). The value of the decomposition is that an action's effect is expressible per-base and per-direction; collapsing to a scalar discards the content.

## 6. Resolution ladder (future-instrument question, flagged; no bearing on current flights)

Three rungs of resolution: the MFA (no geography, no agents), the lattice (geography, one stream per location), reality (many streams per location). Each rung down adds heterogeneity the rung above integrates over. The current MFA-fidelity question — does the lattice reproduce the mean-field cascade — is the first instance of a repeatable question: **does the coarse-graining commute with the dynamics?** The second instance, not currently instrumented and out of scope for all current flights, is whether a distribution-per-cell substrate produces the same regime structure as the point-per-cell substrate. Agreement would vindicate the one-point terrain as accessory; disagreement — e.g., within-location variance in distance-to-surface smearing a transition or changing its character — would be a genuine finding about what the theory's claims quantify over, and would bear directly on the normalization assumption named in 2.3.
