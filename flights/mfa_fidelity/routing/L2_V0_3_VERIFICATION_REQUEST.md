# Note to L2 — Merge Specification v0.3: Scoped Integration Verification Request

**From:** L1, routed by Mike
**Accompanies:** `MERGE_SPECIFICATION_v0_3.md` (repository copy at commit `4afa756`, digest `dba76c36fa4efc185fe9304453ee3d89e98f028add026c2473fadea2b6f24e03`)
**Register:** closed. This is an integration verification, not a fresh adversarial pass — your v0.2 review's architecture verdict stands and is not reopened by this routing.

---

## 1. What v0.3 is

Your review of v0.2 (ACCEPTED WITH REQUIRED REFINEMENTS, nine enumerated) has been integrated in full. Each refinement is marked **[v0.3/L2-n]** at its section: L2-1/L2-2 at §8.1 (bypass necessary-not-sufficient in your claim language; four failure surfaces; two-level harness with structural preflight as diagnostic and behavioral bit-exact comparison as the gate; "symmetrical" replaced by the common structural-bypass principle); L2-3 at §4.3–4.4 (diagonality defined exactly as no-cross-base-input, common-driver correlation explicitly permitted via the Base-Space distinction; Q oriented in u_base = 1−c coordinates with the c-translation stated once); L2-4 at §1.2 (common skeleton vs. dispatched probability construction; the layered-on-A construction named as the wrong implementation); L2-5 at §5.1 (algorithmic lineage vs. parameter choice; Gate A freezes A's exact init algorithm — draw order, call shapes, dtype; fixed_count declared a new implementation certified under B2); L2-6 at §7.3 + §9.2 (run_config.json / run_record.json two-file model with immutable-config boundary; canonical byte-level digest construction — lexicographic filename order, filenames in-digest as UTF-8 lines, canonical JSON serialization, record outside every digest it reports); L2-7 at §8.2 (B1 deterministic rule equivalence / B2 declared-ensemble distributional; seedwise-pairing language retired); L2-8 at §8.3 (R0 implementation correctness precedes R1 scientific recovery; the ambiguity foreclosed stated); L2-9 at §7.2 (rho_global's dual condition — required in all Gate-R runs including local-primary; omission a spec violation).

One post-review addition, made by standing obligation rather than by your refinements: **§7.4 now records the completed lock-file read** (L1, pinned clone at `4d9a622`): twenty pins asserted (numpy 2.4.4, pandas 3.0.3, pyarrow 24.0.0 headline; Mesa 3.5.1 present-unused under the equivalence clause); two findings — the lock file carries a UTF-8 BOM, and it contains no Python-interpreter pin, so 3.14.x rests solely on the canonical executable's preflight hard-fail (v1.1 S7) and is asserted on that basis. §7 is no longer read-blocked. This addition is inside your verification scope as item (2) below.

## 2. Verification requested (closed register, three items)

1. **Per refinement, n = 1…9:** INTEGRATED AS REQUIRED, or INTEGRATION DEFECT with location and the respect in which the integration falls short of your requirement.
2. **Integration-introduced defects:** any defect the v0.2→v0.3 rewrite itself introduced, anywhere in the document, including the §7.4 lock-file addition. NONE FOUND is a complete answer.
3. **Freeze disposition:** FREEZE MAY PROCEED, or a NAMED BLOCKER with location.

A fresh full adversarial pass is not requested and its findings are not solicited; matters your v0.2 review accepted are settled absent an actual conflict, per your own stated review posture. If verification surfaces something outside the three items that you judge freeze-relevant, name it as a blocker under item 3 rather than as review commentary.

## 3. Sequencing

On your return: any INTEGRATION DEFECT or NAMED BLOCKER produces v0.4 and one further verification round on the changed text only. On a clean return (nine INTEGRATED AS REQUIRED / NONE FOUND / FREEZE MAY PROCEED), Mike's freeze word freezes v0.3 as the governing instrument specification; the frozen document routes to you for record, and contract drafting begins with E1's narrative telling.

*End of note.*
