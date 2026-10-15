# Ruling — Notation Scope and the Overview ↔ Contract ↔ Frozen-Specification Translation Table (v1)

**Status:** RATIFIED by Mike, 2026-10-15, with §3 ruled as option (a). Drafted by L1 under the introduction plan Mike agreed 2026-10-11.
**Purpose:** to fix, once, which symbols belong to which document, so that the same letter meaning different things in the Overview, the E1 contract and amendment, and the frozen specification can never be read across a boundary. The E1-R amendment §9 repaired one such collision (the unlabelled η(t)); this ruling makes the rule general and records the table.

---

## 1. The scope rule

1. **Three notational domains, each sovereign in its own documents.**
   - **O** — the Overview of the Theory (`theory/overview/`, currently v1.8.1): the mean-field statement.
   - **C** — flight contracts, amendments and governance records (`flights/mfa_fidelity/contracts/`, `governance/`): the pre-registered claims and their grammar. Flight 8's contract will carry the amendment §9 names.
   - **S** — the frozen specification and the instrument (`flights/mfa_fidelity/spec/MERGE_SPECIFICATION_v0_4_FROZEN.md`, `instrument/`): the substrate rule as implemented. Frozen; its names cannot change without a new specification version.
2. **A symbol means what its domain's document says, and nothing else.** No document may use a symbol from another domain without naming the domain (e.g. "the Overview's β", "the specification's β").
3. **Correspondence is stated only in this table.** Where an object in one domain corresponds to an object in another, the correspondence is an entry here, with its nature stated (identity, projection, or name-only). A correspondence not in the table does not exist for governance purposes.
4. **Frozen names win in S.** Where S and the amendment disagree (the specification's `η_MFA` for the Landau noise term; the amendment's ξ_ρ(t)), S keeps its name inside S, the amendment's name is used in C and O, and the table records the pair. Nothing in S is renamed.
5. **The table is append-only.** A new flight, specification version or Overview version adds rows; existing rows are never rewritten, only marked superseded with the version that superseded them.

## 2. The translation table

| Object | O — Overview v1.8.1 | C — E1-R amendment §9 / Flight 8 | S — frozen spec v0.4 / instrument | Nature of correspondence |
|---|---|---|---|---|
| Structural bases | v, c, r | v, c, r | v, c, r (`u_base ≡ 1 − c` is the cost-complement base; `u_t` is the exogenous drive — never the same symbol) | identity of meaning; S adds the complement and the drive |
| Control quantity | Λ = F(v, c, r), one function at two resolutions (§7) | Λ (per-cell, locally configured) | Λ via the F dispatch, per cell | identity; O's aggregate Λ is the coarse-graining of S's per-cell Λ (MFP bridge) |
| Activation density | ρ (§10) | ρ | `density/8` (Moore-neighborhood active fraction, local read, D2 ruling); global ρ as committed comparator | projection: O's ρ is the mean-field projection of S's lattice density |
| Coherence | Ψ (§12) | Ψ | Ψ_local (mechanism telemetry); aggregate Ψ a secondary observable (D5 ruling) | projection |
| Self-reinforcement coupling | **g₀** in g₀Λρ(1 − ρ) | **g** in the activation hazard h + g·λ·d (Flight 8) | **β** in drive = αΛ + β·(density/8) − δ·(density/8)² − γ_offset (symmetric chain) | projection; **the same letter β names different objects in O and S — see §3** |
| Lapse / deactivation | **β** (lapse rate, −βρ) | **μ** (deactivation rate; amendment §9: "β is already taken by the density coupling") | none — the frozen symmetric chain is memoryless per cell and has no deactivation term (E1-R amendment §1) | O's β ↔ C's μ: identity of meaning, different letters; absent in S by construction |
| Spontaneous registration | **αΛ(1 − ρ)** — the spontaneous term, part of the mean dynamics; an imperfection parameter | **η_floor** reserved for the deterministic spontaneous-action floor (amendment §9) | **η_floor** = 0.01, A's nucleation floor: p_act = p_base + η_floor(1 − p_base) | projection: O's spontaneous term is the mean-field image of S's floor; O's α is not S's α |
| Λ-coefficient in the drive | (none; absorbed in F and g₀) | — | **α** in drive = αΛ + … | S-only; **not** O's α |
| Fluctuation / noise | **ξ_ρ(t)** (v1.8.1), the residue the mean field does not resolve; never merged with the spontaneous term | **ξ_ρ(t)**, law and covariance stated (amendment §9) | **η_MFA**, "the Landau noise term" (spec §1.4 naming note, frozen) | identity of meaning; name-only difference, frozen in S |
| External deterministic field | — | **h(t)** (amendment §9) | — | C-only |
| Coherence coefficient | **μ(ρ)** (§12), sign change at the second transition | μ(ρ) | (not realized in E1; Ψ_local mechanism only) | identity; **O's μ(ρ) is not C's μ — see §3** |
| Second-transition saturation | γ in −γΨ³ | — | — | O-only; S's `γ_offset` is an unrelated drive offset |
| Activation boundary | Λ* = β/g₀ (minimal form, spontaneous term removed) | Λ* (Flight 8: discrete crossing gλ̄Δt = 1 − e^(−μΔt); zero-floor skeleton exact, positive-floor realization rounded) | no boundary — the symmetric chain has a unique fixed point everywhere (E1-R reference of record: NO-NULL-PHASE) | O's Λ* is the continuous limit of C's crossing; absent in S |
| Window | W (PD5) | W declared per contract | one tick | declaration, per PD5 |
| Feedback operator | Q(ρ, Ψ) → bases | Q | Q base update, clipped, per-base (Γ = 0 in E1) | identity; D2 ruling fixes the read mode |

## 3. The collision Mike must rule on: β and μ

Assembling the table made one fact explicit that the amendment's §9 repair did not address, because §9 looked only at the contract and the specification:

- In the **Overview**, β is the lapse rate and μ(ρ) is the coherence coefficient.
- In the **frozen specification**, β is the density-coupling coefficient in the drive.
- In the **amendment's Flight 8 names**, μ is the deactivation rate — chosen *because* β was "already taken by the density coupling," i.e. taken in S.

So the Overview's β (lapse) is the amendment's μ (deactivation), and the Overview's μ(ρ) (coherence) is a different object from the amendment's μ. Under rule 1.2 this is legal — each domain is sovereign — and the table records it. But Flight 8's contract will state its rule in C's names and cite the Overview's §10 as the mean-field target, and a reader will meet "β" and "μ" meaning two things on one page.

Options, for Mike:

- **(a) Keep all names; the table governs.** Flight 8's contract carries a one-line reminder at first use ("μ here is the deactivation rate; the Overview's lapse rate β; not the Overview's μ(ρ)"). No document changes. *L1's recommendation:* lowest cost; the Overview was written for its own readers and its β/μ are the natural letters there; the frozen β cannot change; and the amendment's μ is already of record.
- **(b) Rename in the Overview** at the next version (v1.9): lapse rate → μ₀ or δ, coherence coefficient keeps μ(ρ). Requires a §15-sanctioned notation revision and re-registration; touches §10, §12, §14, §18.
- **(c) Rename in Flight 8's contract**: deactivation rate → some letter other than μ (κ, say), freeing μ for coherence across O and C. Contradicts the committed amendment §9 wording ("deactivation rate is written μ"), so it would need a Flight 8 contract clause superseding §9's letter for Flight 8 — permitted, since §9 is E1-R's amendment, but it should be done once, before the contract freezes.

**Ruled by Mike, 2026-10-15: option (a).** All names kept; this table governs; Flight 8's contract carries the one-line reminder at first use of μ. The table above stands as written.

## 4. Consequences

- **Flight 8 drafting:** the contract states its rule in C's names, cites Overview §10 as the mean-field target through this table, and cites PD1–PD7 for participation. It may not cite the Annex (TDA-000 §3).
- **The third-order lattice-versus-ODE comparison** (held per amendment §10) is a comparison across the O–S boundary and may be specified only in terms of table rows marked "projection" or "identity"; a comparison that pairs objects not in the table is not evaluable.
- **Review packets to L2** that quote across domains must name the domain of every symbol.
- **The Overview README** cross-references this ruling.

## 5. Provenance

Amendment §9 (ratified 2026-10-06, commit `cbbc767`): η_floor reserved, ξ_ρ(t) for forcing, h(t) for a field, μ for deactivation, η(t) retired. Spec §1.4 naming note (frozen v0.4): u_base, u_t, η_floor, η_MFA, no symbol reuse. Overview v1.8.1 §10 (2026-10-11): ξ_ρ(t) adopted; the substrate's floor and forcing named as the program names them. D2 and D5 ruling records (2026-08-18) for the read modes. MFP registration v1.1 for the projection relationship.

*End of ruling (draft).*
