# F8 M7 design note (2026-11-02, round 2) — what is carried from E1 M7 and what F8 changes

**Sources of record.** E1 M7 `e1/runner.py` `f33fbb54c115225c…` (L2 rounds 1–7, SOUND; placed 7ebb87e) and its governance records under `governance/e1_stage1/`; Contract F8 v0.8.4 §7.1–§7.4; Interpretations 001 (`6bf7304f…`) and 002 (`198d2991…`); the ratification record v1.0 (`cdedfcb4…`) §E; the placed F8 modules at `2c8827b`.

## 1. Carried verbatim (same objects, same grammar)

- The three principles and their mechanics: `AuthorizationRecord` (version, issuer, exact stage identity, governance/spec identities, authorized jobs, tranche panel, production flag with the prerequisite-manifest identity), `AuthorizationRegistry` (append-only; prefix check over the file's git history; exactly one commit per version file), `load_authorization` / `require_authorized` (the only entry of an authorization into a gate), `SOURCE_LITERALS_GRANT_NOTHING`.
- Canonical persistence: `_encode` / `_decode` over a closed registry of record types; the envelope (type, schema identity, stage identity, authorization record and file identities, version, job, record); `_write` LF canonical bytes; `persist_record` (no binding) and `_persist_canonical` (private to `run_canonical_job`); `load_record` with duplicate-key and nonfinite refusal, byte-canonical check, schema and stage checks, `require_job` loading the authorization from the committed file.
- `M7PlacementRecord` and `M7SuiteRecord` with `verify_placement` (placement commit = last commit touching runner/test; clearance file committed at its identity, naming both files and SOUND; suite record typed, passing, same files and commit).
- Production prerequisites: `PrerequisiteEntry` / `ProductionPrerequisiteManifest` (committed; names must EQUAL the governance record's exact set; each record loaded at its file identity through its own validator with committed dependencies; `PREREQ_STATES` per type; readiness = all valid-complete ∧ required passages ∧ no branch stop), content-addressed memo.
- Package: `PackageItem` / `PackageSpecification` validated against the governance record (vocabulary, required items, producer/output type, closed predicate alphabet with type applicability, exact dependency schema); `_assemble` in dependency order from loaded items only, canonical items under their producer's job; `StagePackage` (role, identities, rows, two derived states) written LAST and validated by replay; the provisional assembly for development only.
- `TrancheQuarantine` (integrity/cost/provenance only; `__getattr__` blocks everything else; replay by re-execution) and `ResourceBenchmark` (every file fact re-derived; projections derived) — on F8 run artifacts.
- Stage binding: bound sources from disk equal to cleared literals, CRLF refused, committed and clean surface, stage commit = last commit touching the surface, Gate A/B/R0 records, Gate B environment qualification (twenty pins, lock identity), record-schema identity, declaration digest.

## 2. Changed for F8

| Area | E1 | F8 |
|---|---|---|
| Run artifacts | E1 M1 telemetry parquet + rho parquet + run-config JSON; tier-1 verifier re-run; conformance preflight | M1 `F8RunResult`: rho parquet (`write_rho_table`) + canonical `RunProvenance` JSON; trace replay via M-P1 `observation_from_result` (spec reconstructed) and M2 status against the adapter; M1 re-execution replay (`replay=True`, same platform) |
| Level record | (level) × 20 canonical seeds, pass 2 through a router manifest | (level, object, panel) × 20 panel seeds, under the lattice job that produced it — the job → (objects, panel) mapping `JOB_OBJECTS` is enforced before any run (L2 r1 D2); panels: canonical, calibration, **stability** (Interpretation 003); pass 2 impossible in production (M1 guard) → `EvaluabilityHalt`; execution metadata derived from spec + trace (D4a); per-run record read as canonical bytes (D4b); every loaded record bound to its slot (D4c) |
| Scoring object | threshold cache files (M6) with qualification record | the committed adapter record (M6 `ThresholdAdapter`, canonical machine), re-derived on the platform-independent surface; `adapter_platform_match` required for canonical |
| Governance | `E1RGovernance` + amendment markdown | `F8Governance`: contract/freeze/Appendix A/Interpretation/ratification identities; eight declaration digests; attempt-2 protocol identity + disclosed decision; `placement_date`; nine masters; adapter body; vocabulary/required/prerequisites/branch stops; M5-5 mapping — all checked against the placed modules |
| Jobs | 10 (dense reference, stability, projection sweeps, tolerances, M6 audits, benchmark, package) | 17 per §7.3; `SCIENTIFIC_JOBS` gated by the §7.1 readiness; 5 `LATTICE_JOBS`; `JOB_GRAPH` dependencies are EXECUTABLE (one `require_job_dependencies` on both the job route and the direct `run_level` route): known-answer → design → held-out; job 0 → skeleton census (+ `SkeletonAssessment`) → skeleton stability → realization census → realization stability → P1 (L2 r1 D3) |
| Readiness | prerequisites incl. `stage1_package`; production = the 640-run sweep after the package | prerequisites are apparatus/qualification items; `MANDATORY_PREREQUISITES` = known-answer pass, M6 qualification pass, **job-0 census pass (both ceilings)** — the governance grammar cannot omit or weaken them (D3a); the package is the end state; branch stops name prerequisites |
| Derived items | level list, ensemble sizes, closure publication (R1a), null precision, router collision, conformance | level list (+W_res), ensemble sizes, closure publication (Appendix A binding), null law (indices/modes/payload/protocol), router collision (+338), conformance (M1 determinism) |
| New records | — | `MorphologyRecord` (§7.3 item 3; scope per Interpretation 003 pt 1–2), `SkeletonAssessment` (item 1; D3c), `StabilitySweep` + `StabilityRecord` (items 2, 4 on the independent stability panel; Interpretation 003 pt 6–8), `ToleranceEnsembles` (M5-5's separate kind; D5b) |
| M3 touch | — | obligations 3–4 of the ratification record §E, placed with M7 |

## 3. Obligations of §E discharged or carried

1. Sole issuer of the canonical census role — `_census_from_records` (job 0) only. ✔
2. Verdict of record on the final level set — for M6's synthetic sweeps, M6's own `run_sweep` evaluates the final set and `validate_audit_record` replays; for the realization census, Interpretation 003 pt 1–2 (Mike, H1 route a): the morphology record is a restricted pass-1 report, `final_set_obligation` recorded as `open` whenever insertions are requested, `discharged_identically` when none are. ✔ (ruled)
3. `is_qualification_evidence()` removed. ✔
4. `price_familywise` docstring corrected. ✔
5. Protocol identity with its decision — `F8Governance.null_validation_protocol_sha256` and the TYPED `null_validation_decision`, which must EQUAL `NULL_VALIDATION_DECISION_OF_RECORD`, itself re-derived at bind from the committed attempt records (bound by identity in `DECLARATION_RECORDS`); `NullLawRecord.protocol_sha256`. ✔ (D7)
6. M-P1 qualification of record — job `mp1_known_answer` (M7-issued; validator replays the corpus). ✔
7. Identities — governance fields; `CONTRACT_RECORDS` and `DECLARATION_RECORDS` (the approved M6 generator declaration Markdown, the three null-validation attempt files) literals in the stage; adapter from the committed ASCII JSON. ✔ (D7)
8. Stale comments in `test_f8_m6.py` / `test_f8_mp1.py` — left to their next edits (not touched here). carried
9. exp()-derived fields recorded, compared, never assumed — `platform_tag`, `adapter_platform_match`, `ClosurePublicationRecord.max_abs_deviation`, `NullLawRecord.payload_identity`. ✔

## 4. Declarations M7-1…9 — see the round-1 packet §3 and the round-2 response §1–§2.

M7-9 (Interpretation 003, ratified 2026-11-03 at `1978a01`, `6ebf0ad3…`): morphology scope (H1 a) and the independent stability panel declared in M1 by the a′ touch (H2 a); `PRODUCTION_RUNS` = 3,360.

## 5. Producer and timing of §7.3 item 3's reporting (L2 r2 §6)

The realization census (`realization_census`) emits the canonical realization sweep and the morphology record. T-R1′ is first evaluated in `realization_stability` (on the canonical and the stability sweep, against the calibration-census bands) and again, with the steepest-ascent diagnostic and the full fidelity tier (ii)–(iv), in `p1_evaluation` by M-P1's `evaluate_p1`. The contract's item-3 reporting is complete when P1 is; no result is absent from the final pipeline, and no new output is invented for it.

## 6. Round-3 changes (L2 r2 R2-1…R2-7)

Dependency paths confined to the prerequisites tree and the resolved manifest graph in the readiness key; one semantic predecessor gate on both production routes, memoised on the full dependency surface; the clearance parser reads outside quoted and code material and fails closed; Interpretation 003 bound as the seventh contract record; skeleton stability by the same crossing index; the census committed before its stability job; M1's and M7's declaration-digest checks unconditional.

M7-8 (memos): the grammar's derivations are pure functions of content; process-local memos cache them on keys built from every input (stage: HEAD, surface status, surface file hashes, frozen code key, platform; production adapter: adapter identity, frozen code key, platform; readiness: stage, authorization, manifest identity, the readable surface of the prerequisites tree, governance identity, package-spec identity, frozen code key; artifact replay: record identity, artifact tree digest, adapter identity, replay flag, frozen code key; live adapter: frozen code key). Nothing is persisted; a miss re-derives. Round 3 added the dependency-gate memo (R2-2) and narrowed the readiness tree component to its read set; round 4 refuses directory/file aliases in every keyed tree before any cached success (R3-1).

*L1, 2026-11-02.*
