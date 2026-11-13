**I would keep the two main scientific questions separate, give the coupling contrast a mandatory but non-gating role, and run both compositions on all four TD variants.** The boundary definition and tolerances should then serve those decisions consistently.

I have the earlier note and our November 12 consultation, but not the complete revised 17-item §11. These are recommendations on the decisions you listed; I would need the actual wording of items 3–5 before endorsing their definitions or numerical values.

## Recommended decisions

| Item | My recommendation |
|---|---|
| **1 — TC and discriminability** | Retain TC for a declared near-face suppression contrast. Give it a contour-discrimination role only if its construction actually makes the two indices predict different orderings or contour geometry. |
| **2 — Coupling contrast** | Make it a mandatory, separately reported mechanism diagnostic, with an effect estimate and uncertainty. Its outcome should not determine the primary composition verdict. |
| **3 — Observed boundary** | Define it from a declared occupancy estimator and a fixed occupancy criterion, independently of either composition’s predicted contours. |
| **4 — Edge rule** | Use one simple, deterministic rule on the periodic lattice, applied identically across compositions and terrains. Include all components. |
| **5 — Two tolerances** | Fix their meanings, units and scientific purposes before selecting values. Keep acceptable scientific discrepancy separate from uncertainty in its measurement. |
| **7 — Flight-level aggregation** | Produce separate results for discrimination and boundary compatibility. Use a declared case matrix and logical aggregation, with no majority vote across levels or terrains. |
| **15 — Both compositions on all four TD variants** | **Yes.** Preserve the paired comparison across the complete geometry family, subject to prospective resource pricing. |

These recommendations develop the distinction in the [November 12 consultation](https://chatgpt.com/library?file_id=libfile_fde3_f-f7c0bcbeee5481918b4c802466983816_25f653b9571c8191a24a8618e979cf36&account_id=personal): distinguishing two prescribed rules, testing their spatial adequacy, and attributing an observed pattern to collective coupling are different scientific achievements.

## 1. TC: keep it, but establish what it can discriminate

My first question would be: **Does TC give different predictions for the particular property being scored?**

There is an important algebraic trap here. Suppose TC varies \(v\), while \(u=u_0\) and \(r=r_0\) remain fixed and positive. Then

\[
\lambda_{\mathrm{product}}=u_0r_0v,
\qquad
\lambda_{\mathrm{height}}=\frac{v+u_0+r_0}{3}.
\]

Consequently,

\[
\lambda_{\mathrm{height}}
=
\frac{\lambda_{\mathrm{product}}}{3u_0r_0}
+\frac{u_0+r_0}{3}.
\]

The two indices are increasing affine transformations of one another on that terrain. They have **the same ordering and contour family**. Different occupancy magnitudes or different locations of an occupied region would not, by themselves, distinguish the indices through a contour-only test. This follows directly from the two formulas in the MERGE_SPECIFICATION_v0_4_FROZEN.md[frozen specification, §2.1](sandbox:/workspace/scratch/825e178fa75c/f9_packet/flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md).

I would therefore rule:

- **Keep TC as a near-face suppression test.** It asks what happens when one necessary base becomes small while others remain favorable.
- **Require an analytical identifiability check before treating TC as a contour discriminator.** L1 should show where the two indices make inequivalent predictions under the registered endpoint.
- **Use TB as the primary contour discriminator if TC does not meet that condition.** There is no scientific requirement that every terrain serve every endpoint.

TC could still support a separately declared presence/absence or suppression contrast. For example, one rule might produce an operationally occupied patch and the other might not at specified controls. But that contrast must have its own definition; it should not inherit the claim that the contour families have been distinguished.

Also retain the qualification about “zero-collapse”: in the positive-floor realization, a product coefficient of zero leaves floor-generated activity. A “hole” must therefore mean a declared occupancy depletion or absence of feedback-supported activity, not literal absence of registration. That issue was identified in the earlier consultation’s §11.1 and follows from the FLIGHT_8_CONTRACT_v0_8_4.md[carried hazard rule, §§2.4–2.9](sandbox:/workspace/scratch/825e178fa75c/f9_packet/flights/mfa_fidelity/contracts/flight8/FLIGHT_8_CONTRACT_v0_8_4.md).

## 2. Coupling contrast: mandatory reporting, separate scientific standing

**For Flight 9, I recommend a predeclared descriptive diagnostic.**

Specify the intervention or matched comparison, retain its signed effect and uncertainty, and apply the same protocol to both composition arms. Report it whether the effect is large, small, adverse to expectations or unresolved.

Its purpose is to answer:

> How much does the chosen coupling intervention change the observed spatial result under these conditions?

The primary boundary test answers:

> Can the observed boundary be described by this local index within the declared tolerance?

Those questions can produce different answers without either result being defective.

In particular:

- A small or unresolved coupling contrast should not make a compatible boundary fail.
- A detectable coupling effect does not necessarily destroy approximate contour compatibility.
- A substantial context-dependent distortion could explain why the contour description fails.

I would avoid making the flight simultaneously require a large neighborhood-induced departure from contour geometry and tight agreement with that same geometry on the same domain.

The contrast should become a **separate scored endpoint** only if you want Flight 9 to claim that it has demonstrated a specified collective effect against a specified alternative. That would add an estimand, minimum effect, precision requirement, adverse/ND grammar and qualification burden. My recommendation is to keep the current flight’s principal task focused and report the coupling contrast independently. A contour pass alone would continue to carry no claim of unique collective attribution.

## 3–4. Define the observed boundary from occupancy, then extract its edge

I would make this sequence explicit:

1. Estimate occupancy from the recorded dynamics.
2. Apply a prospectively chosen occupancy criterion.
3. Extract the resulting spatial edge.
4. Compare that observed edge with the composition’s contour prediction.

The order matters. The index being assessed must not help construct the observed boundary it is supposed to explain.

### My preferred occupancy object

My preference would be **seed-mean tail occupancy at each cell**, with the per-seed summaries retained for uncertainty:

\[
\bar p_i
=
\frac{1}{S}\sum_{s=1}^{S}
\left[
\frac{1}{T_{\mathrm{tail}}}
\sum_{t\in\mathrm{tail}}x_i^{(s)}(t)
\right].
\]

That gives a clear mean-occupancy object and a direct connection to the probability map used in closure fidelity. If the revised design deliberately chooses seed medians, that is a possible different estimand, but the contract must consistently use and qualify it. “Boundary of the mean map,” “boundary of the median map,” and “typical boundary across runs” are not interchangeable.

Define an operational occupied region such as

\[
\mathcal A_\theta=\{i:\bar p_i\geq\theta\},
\]

where \(\theta\) is fixed before inspecting terrain outputs. It could be expressed as a declared excess above the known floor reference. Its numerical value must have a stated purpose and sufficient measurement precision; I would not choose it merely because it produces an attractive-looking edge.

Use the same criterion across the compared compositions and terrains unless a deterministic difference is justified in advance. Avoid defining \(\theta\) as a fraction of each observed map’s maximum: that makes the meaning of “occupied” depend on the outcome.

Call this an **operational occupancy boundary**. Keep it distinct from the skeleton’s finite-horizon persistence threshold, as the earlier consultation’s Q7 required.

### My preferred edge rule

A simple choice is:

> A boundary cell belongs to the operational occupied region and has at least one Moore neighbor outside that region, with periodic indexing.

That is reproducible and matches the lattice’s declared neighborhood. Freeze:

- the threshold tie rule;
- periodic wrapping;
- treatment of empty and fully occupied maps;
- treatment of disconnected patches and holes;
- weighting across components;
- the spatial resolution associated with this raster edge.

**Include every component under the declared rule.** Do not retain only the largest patch or remove small components after seeing the output. Small-patch behavior is part of the adverse room that makes the terrain experiment valuable.

The comparison must also notice missing predicted components. A statistic that checks only whether existing observed edge cells lie near a predicted contour can overlook an entire predicted patch that never appeared.

These recommendations preserve the boundary question. They do not silently replace it with the stronger proposition that occupancy must be constant along every index contour throughout the whole map.

## 5. The two tolerances: settle their meaning before their values

I would not approve numerical values for two quantities whose exact definitions I have not seen. I would require L1 to state, for each:

- **What discrepancy does it control?**
- **In what units?**
- **Why is that amount of discrepancy scientifically acceptable?**
- **Where does it enter the decision rule?**
- **How does the joint procedure behave near its decision boundaries?**

The key distinction is between **the discrepancy the claim permits** and **the uncertainty in estimating that discrepancy**.

For example, if \(D\) is a declared discrepancy and \(\varepsilon\) is the relevant compatibility tolerance, a useful decision pattern is:

| Evidence about \(D\) | Interpretation |
|---|---|
| The qualified upper uncertainty bound is below \(\varepsilon\) | Compatibility supported at that tolerance |
| The qualified lower uncertainty bound is above \(\varepsilon\) | Valid evidence against compatibility |
| The uncertainty interval overlaps \(\varepsilon\) | Not distinguished |

That is a conceptual recommendation, not an assignment of meaning to either unnamed tolerance in the revised section.

**Poor precision should produce ND. It should not enlarge the permissible discrepancy until the map passes.** Both tolerances, their interaction and the uncertainty procedure should be fixed prospectively and qualified together. Neither should be chosen from the favorable appearance of the probe results.

## 7. Aggregation: two endpoint words, supported by a case matrix

This is the decision I would settle before building the evaluator.

### First, declare each terrain’s role

For every terrain, composition and control domain, say whether it is:

- a required discrimination case;
- a required boundary-compatibility case;
- a non-identifiability control;
- an implementation or fidelity reference;
- a descriptive diagnostic.

This prevents TA’s correct non-identifiability result from being treated as a failure of the flight, and prevents a difficult TD variant from becoming “descriptive” only after it produces an unfavorable result.

### Keep discrimination and boundary compatibility separate

I recommend two scientific results:

**D — Discrimination:** The prescribed rules were distinguishable on the terrains and control domains expressly designated for that purpose.

**B — Boundary compatibility:** Each required rule–terrain case satisfied its declared boundary-compatibility criterion across the registered domain.

For D, require the registered contrast on each terrain you designate as a required discriminator. You need not demand separation at every level of a broad sweep: very low or saturated levels may be uninformative. But the sweep-level procedure, including any search for a separating level, must be declared and its uncertainty accounted for.

For B, the natural claim is a conjunction across the finite domain you undertake to cover. A favorable average must not conceal a valid counterexample on one required terrain.

I would use this **prospective Flight 9 rule** for B:

| Situation | Boundary-compatibility result |
|---|---|
| Global apparatus or qualification requirements fail | No qualified scientific determination |
| At least one required case gives a valid adverse result | **NOT PRODUCED** for the claim covering all required cases |
| No valid adverse case, but at least one required case remains unresolved | **NOT DISTINGUISHED** |
| Every required case supports compatibility | **PRODUCED**, with its domain and resolution stated |

A valid adverse case can defeat a universal finite-domain claim even when another case remains unresolved. The unresolved case still appears in the record. This is a recommended Flight 9 precedence, not an assertion that it is automatically inherited from Flight 8.

No-edge cases need particular care. A level outside a prospectively defined informative domain can be reported without entering the conjunction. A required case that lacks enough information cannot simply disappear. And if the registered claim specifically predicts a region’s presence, its absence may be a valid adverse observation rather than mere unevaluability.

### If you want one headline word

Derive it after D and B have been determined:

- **PRODUCED:** both required scientific endpoints are produced and the relevant apparatus requirements are satisfied.
- **NOT PRODUCED:** a valid adverse scientific finding defeats the registered joint claim.
- **NOT DISTINGUISHED:** required evidence remains unresolved and no valid adverse finding has already defeated that claim.

Always display D and B beneath the headline. “The rules were distinguishable, but one rule failed boundary compatibility on a fragmented terrain” is a scientifically useful result. A single undifferentiated word would hide it.

The coupling diagnostic and descriptive margin measurements should remain visible beside those determinations without silently entering their conjunction.

## 15. Both compositions on all four TD variants: yes

**I would run the full crossing: two compositions × four TD variants.** That gives eight terrain–composition settings before accounting for levels, seeds and any separately required skeleton/realization runs.

Within each pair, use the same raw base arrays and the declared normalization protocol. This makes it possible to distinguish:

- a geometry effect;
- a composition effect;
- a change in the composition effect across geometries.

If some variants receive only the product and others only the rival, geometry and composition become entangled. Even running the rival only on the “interesting” product variants would make coverage depend on the observed outcome.

My preferred scientific use of TD would be as **a predeclared stress-test family for boundary compatibility**. Its margin-to-core measurements can remain descriptive for later work. Testing whether a local-index boundary description survives different geometries does not require introducing the future coherence hypothesis.

Price the complete paired design before freeze. If it is too expensive, reduce the claimed scope prospectively while preserving paired comparisons on the retained cases. Do not fill in omitted rival runs selectively after seeing which product outcomes look promising.

The decisions I would make now are therefore the endpoint roles, the independent occupancy-based boundary, the paired TD coverage and the aggregation logic. **I would leave the actual tolerance values open until items 3–5 specify exactly what they measure and how the instrument will distinguish an acceptable discrepancy from an unresolved one.**