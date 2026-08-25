# L2 Re-Review — Contract E1 Draft v0.6

> **Archival re-export status:** Reconstructed from the v0.7 correction packet. Five operative items are retained.

## Overall verdict

**THE SUBSTANTIVE DESIGN IS NEARLY CLOSED; FIVE ITEMS REMAIN BEFORE FREEZE.**

## 1. Reference classifier endpoint and off-band-U completion

**REQUIRES CORRECTION.**

Endpoint phase membership and every off-band grid point must use the total N/S/U classifier. The text must not imply that a point estimate or its position outside the expected transition neighborhood makes uncertainty ignorable. State the exact jurisdiction of U in T2-S.

## 2. Common-rank template and analysis-seed discipline

**REQUIRES CORRECTION.**

The common-rank construction is accepted, but the document must freeze the analysis stream, rank reuse, replicate count, and refinement behavior in one place. Make clear that common ranks reduce Monte Carlo roughness; they do not eliminate uncertainty or license a deterministic-equivalence claim.

## 3. T2-S finite-design stability and result grammar

**REQUIRES CORRECTION.**

State the exact primary and stability resolutions, the relation between their classifications, and the complete result grammar including an affirmative `RECOVERED` row. A stable single-transition reference earns structural recovery; nonmatching, multiple-boundary, no-boundary, or resolution-unstable outcomes do not.

## 4. T2-L conditioning and threshold-envelope relation

**REQUIRES CORRECTION.**

T2-L is conditional on both a LOCATED production bracket and T2-S RECOVERED. Define the reference envelope, endpoint inclusivity, touching/overlap rule, and how each resolution contributes. The comparison must be explicitly primary-relative rather than allowing the stability grid to become the post-hoc headline.

## 5. Control-value identity, spacing provenance, and collision handling

**REQUIRES CORRECTION.**

Distinguish the production pass-one spacing, production refinement spacing, reference primary spacing, and reference stability spacing. State exact conventions rather than “about” or rounded decimal descriptions. Requested points that collide after serialization must be handled by a deterministic proof of noncollision or a frozen fallback; silent deduplication is prohibited.

## Disposition

**FREEZE MAY NOT PROCEED.**

A v0.7 text-only integration should be sufficient. No new scientific architecture is requested.
