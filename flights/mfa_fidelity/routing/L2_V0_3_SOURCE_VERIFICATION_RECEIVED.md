# Received Record — L2 Source-Level Integration Verification of Merge Specification v0.3
**Provenance:** Received from L2 via Mike, 2026-08-21, upon L1's corrected self-contained packet (routing note + verbatim v0.3, packet digest 7174876543541e258256245d4c16982de1a7f29ca118229ad3b5d0f80bdffbe0). L2 stated the review superseded its NOT CHECKABLE return and compared marked v0.3 text against the nine refinements without reopening the v0.2 architectural verdict.

## Verdicts
- **L2-1** (Γρ bypass necessary-not-self-certifying): INTEGRATED AS REQUIRED.
- **L2-2** (two-level Gate-A harness; drive-side vs. added Q-side density read): INTEGRATED AS REQUIRED.
- **L2-3** (diagonality as no-cross-base-input; common-driver correlation permitted; u_base=1−c orientation with mechanical c-translation): INTEGRATED AS REQUIRED — "closes the interpretation defect identified in v0.2."
- **L2-4** (common skeleton vs. wholesale probability dispatch; layered-on-A construction expressly barred): INTEGRATED AS REQUIRED.
- **L2-5** (init algorithmic lineage): **INTEGRATION DEFECT — §5.1 fixed_count paragraph.** "Not preservation of B's behavior" ruled broader than required — B2 exists to test preservation of B's distributional behavior; what is not preserved is B's legacy initialization algorithm, RNG regime, and seedwise stochastic history. Required replacement in substance supplied; created an unnecessary §5.1/§8.2 contradiction.
- **L2-6** (canonical hashing; run_config/run_record immutable-config separation): INTEGRATED AS REQUIRED.
- **L2-7** (B1/B2 split; seedwise pairing retired): INTEGRATED AS REQUIRED.
- **L2-8** (R0/R1 separation; ambiguity foreclosed; asymmetry attaches after R0): INTEGRATED AS REQUIRED.
- **L2-9** (rho_global dual condition incl. local-primary Gate-R runs): INTEGRATED AS REQUIRED.

## Integration-introduced defects
- **Defect: §6.2** — "preserving Gate A exactly" conflicts with §8.1's necessary-not-sufficient discipline (cross-section defect: the v0.2-era self-certifying wording survived beside the newly installed principle). Required replacement in substance supplied.
- **§7.4 lock-file addition:** NONE FOUND within the scoped review — pins/BOM/no-interpreter-pin/3.14.x-attribution and Mesa-present-unused wording verified as internally consistent; L2 noted it did not independently re-audit the twenty package values against a separately supplied lock-file source.

## Freeze disposition
NAMED BLOCKERS: the §5.1 and §6.2 wording corrections. "Both blockers are narrow wording corrections... After those two passages are corrected, the changed text alone is sufficient for the final verification round." FREEZE MAY NOT YET PROCEED.

**Disposition:** both corrections applied in v0.4 per L2's required substance, marked [v0.4/blocker-n]; verified in the subsequent changed-text rounds.
