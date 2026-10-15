# Session Handoff — 2026-10-15 (E1-R stage 1 CLOSED; successor work opens)

**For the next L1 conversation.** Paste this as the first message. Written at the close of the session that ran E1-R's canonical jobs from the first authorization to the terminal stage-1 package.

**Roles.** Mike Bradshaw: Theory Architect, sole execution channel, final arbiter of every commit and ruling. L1 (you, Claude): design chamber. L2 (ChatGPT): adversarial source review, consulted in a fresh chat per packet. L3: retired. Phil Roundy writes the manuscript and is an EE scholar; he does not rule on the theory.

**Repository.** `github.com/MikeBradshaw3000/ee-theory-lab`, local `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab`. `main` is at **`3ab65dfe6380f1288b53ab4e3c7a0113fe09b470`**. Every identity below was measured from a fresh clone at that commit.

---

## 1. Cold-start protocol (in order, before any drafting)

1. **Source before pen.** Clone fresh; confirm HEAD is `3ab65df` or later. The container does not persist between chats. Never reconstruct a file from memory; extract bytes from committed objects or routed packets.
2. Read the project memory file `flight-program-state.md`; its last entries are this session's.
3. Read, from the clone: `flights/mfa_fidelity/governance/e1_stage1/` (the ratified amendment, governance record, specification, four authorizations and the registry); `flights/mfa_fidelity/build_records/L2_E1R_M6_QUALIFICATION_RESPONSE_RECEIVED.md` (L2's disposition, which sets the successor conditions); and `flights/mfa_fidelity/artifacts/e1/stage1/stage1_package.json` (the terminal record).
4. Then begin §4.

---

## 2. State of record: E1-R stage 1 is closed

**The stage.** Canonical stage identity `dc8b1a6b8fc66e35c9981a60d1d0527137734f6cb7a49d42a23dcf8089043c8c`, stage commit `cbbc767` (the last commit touching the bound surface). Governance chain: `E1R_AMENDMENT.md` `04058b21…` (v1, ratified with L2's five edits), `E1R_GOVERNANCE.json` `2e82102c…`, `PACKAGE_SPECIFICATION.json` `ed19cb79…`. Placement: `M7_SUITE_RECORD.json` `7d87ef2c…`, `M7_PLACEMENT_RECORD.json` `8cdfc320…`. The stage binds `canonical` on Mike's machine with the twenty-pin environment and no failures.

**Authorizations** (each file has exactly one commit; registry `AUTHORIZATION_REGISTRY.json` append-only across four revisions, now `1223e17b…`):

| v | File identity | Jobs | Commit |
|---|---|---|---|
| 1 | `aa2a05e5…` | dense_reference, reference_stability | `1856c1b` |
| 2 | `175d3776…` | projection_sweeps, tolerance_ensembles, tolerance_program | `502ba2f` |
| 3 | `846c0e59…` | m6_design_audit, m6_held_out_audit, m6_audit_qualification | `4bfe9c0` |
| 4 | `071223ce…` | resource_benchmark, stage1_package; tranche flag (levels 0.150000/0.332609/0.515217/0.697826/0.850000 × first three panel seeds); production NOT authorized | `e0beb8b` |

**Canonical results** (all under `flights/mfa_fidelity/artifacts/e1/stage1/`, each envelope naming its authorization and the stage):

| Job | Result | Record | Commit |
|---|---|---|---|
| dense_reference | reference of record **NO-NULL-PHASE**, 701/701, 0 halts | `b8b095a6…` | `f0f228f` |
| reference_stability | 6/6 alternatives, class reproduced by all, within Δm_stab; passes | `80f601f1…` | `e46a943` |
| projection_sweeps | **DESIGN-STABLE**, 200/200, 0 halts, match rate 1.0 | `68a3c8f9…` (+ ensemble `ad862129…`) | `2d7e00e` |
| tolerance_ensembles ×24 | all declared levels canonical, 1,000 replicates each | 24 files | `2d7e00e` |
| tolerance_program | complete, 24/24 replay-validated | `d10795a6…` | `f40f732` |
| m6_design_audit | execution-complete (500/500 per class, 0 halts); `ensemble_pass` **False** | `f3383e1b…` | `e0166d1` |
| m6_held_out_audit | execution-complete; `ensemble_pass` **False** | `f2340c82…` | `e0166d1` |
| m6_audit_qualification | **NOT QUALIFIED** (10 reasons) | `be65d972…` | `e6aecaf` |
| resource_benchmark | fits with margin (production ≈ 9,797 s, 133 GB vs 304 GB free) | `e15628ed…` | `153c507` |
| calibration_tranche | passed, 15/15 verifier+conformance, cleanup proven, quarantined | `e9f4d6c4…` | `153c507` |
| **stage1_package** | **complete TRUE, all_items_pass FALSE**; 15/15 valid-complete by full replay (46,678 s) | `d286f70d…` | `3ab65df` |

**Production readiness: FALSE.** Derived from the governance record's four prerequisites: `stage1_package` (scientific, valid_complete) met; `calibration_tranche` and `resource_actuals` (apparatus, pass) met; `m6_audit_qualification` (qualification, pass) **not met**. No branch stops declared. No production authorization exists and none will be issued for this stage. The spatial production/recovery program was never run under this instrument.

**The adverse finding (M6 morphology qualification).** Frozen cap: CP upper 95% bound on the applicable error ≤ 0.10. In both the design and held-out ensembles, four scientific archetypes failed on false-ND — `gentle_onset` 500/500 (ub 1.000; all 500 design sweeps realized full pass-2 yield of 8 insertions and still returned ND), `abrupt_onset` (ub 0.144/0.138), `nonmonotone_amplitude` (0.127/0.142), `persistent_nonstationary_high_m` (0.101/0.105). The other four scientific archetypes and all four ND archetypes pass at ≤2/500. Design and held-out agree class by class. The failure is one-sided (the instrument never fabricates science from ND morphology) and does not touch `no_null_consistent_anywhere`, the morphology the reference predicts — both facts are **diagnostic only** and were ruled irrelevant to the gate.

**Terminology of record (L2).** Say: "both canonical audit records were execution-complete under the E1-R package grammar, but four classes in each failed M6 `complete_pass` because their applicable-error CP upper bound exceeded the frozen 0.10 cap; consequently `ensemble_pass` was false and the joined M6 qualification was NOT QUALIFIED." Never: "the audit records were incomplete."

**Governance records in `build_records/`:** `L2_E1R_GOVERNANCE_REVIEW_PACKET.md` `0a1f79ee…` + `L2_E1R_GOVERNANCE_REVIEW_RECEIVED.md` `259e7062…` (the ratification review, `7dcd2d6`); `L2_E1R_M6_QUALIFICATION_CONSULTATION.md` `d4e60766…` + `L2_E1R_M6_QUALIFICATION_RESPONSE_RECEIVED.md` `3f101a1b…` (the disposition, `b7f61db`). Commit `c20d2b0` placed the pre-review v1 drafts by a file-placement error and was corrected at `cbbc767`; the message says so.

---

## 3. What E1-R established

- **Substrate form, projection side:** the closure's reference of record is NO-NULL-PHASE — the deterministic orbit exceeds the reference null at every one of 701 levels, with a unique fixed point and no structure change — stable under six alternative templates and design-stable at full ensemble. The provisional census finding of 2026-09-30 is now canonical.
- **Apparatus:** M1–M7 built, L2-cleared through 7+ review rounds, placed on Windows, and exercised end to end under record-based authorization; conditional per-seed null, qualified threshold cache, tolerance program, benchmark and quarantined tranche all passed.
- **Apparatus qualification, adverse:** the end-to-end morphology instrument (M2 classify → M3 null → M4 verdict/router → qualified cache) fails the frozen cap on four onset-type archetypes. L2 does not assign the defect to M4/rule 4c or any one component from this evidence; the gentle-onset yield observation makes the router a legitimate suspect, not an established cause.
- **E1-R's realization-level question** ("does the spatial lattice recover the closure's structure?") is answered only on the projection side. No E1-R result may be represented as confirming or refuting architectural P1 (amendment §2).

---

## 4. Successor work: L2's conditions bind

L2's ranked disposition (`3f101a1b…`), adopted by Mike 2026-10-09:

1. **This stage is closed and stays closed.** No same-stage repair; no relaxation of CAP, applicable error, the qualification rule or the prerequisite; no selective production on the reliable morphology.
2. **A successor instrument is legitimate, as a new stage.** Conditions: a **bounded diagnosis phase first** (where in M2/M3/M4/cache the onset failures arise — not a presumption that it's M4); the repair specified and frozen **before** any new qualification evidence; **both current audit ensembles are burned as guards** (their outcomes are known), so the successor needs a fresh, prospectively registered qualification ensemble/master; a new instrument version, new stage identity, new versioned amendment; **steps 1–2 do not carry over by declaration** if M2 or M4 change — the successor reruns every canonical job whose scoring, routing or interpretation depends on the changed instrument (exact carry-over set reviewed by L2 once the repair is specified); qualification passage required before any production.
3. **Flight 8** (successor mechanism class, per the pre-freeze consultation `314b56cc…`): exact discrete-time rule first (hazard h + g·λ·d, deactivation μ; discrete crossing gλ̄Δt = 1 − e^(−μΔt)); zero-floor structural skeleton plus positive-floor realization; Markov null by feedback removal (g = 0); a structural P1 endpoint; E1 data never used to tune its gates. Flight 8 inherits the instrument-repair obligation whether or not a successor E1 stage is opened.

**Open for Mike's ruling:** whether to open a successor instrument stage (diagnosis → repair → fresh guard) before Flight 8, or go to Flight 8 directly. Either way the diagnosis phase is first, and it is diagnostic work on the committed audit records, not a canonical act — it needs no authorization but must be kept segregated and labelled so it never becomes a result of record.

**Also queued (theory track, now unblocked):** the Overview v1.8 / v1.8.1 registration bundle — `theory/overview/` as the citable statement of record (v1.72 kept as provenance), promotion of participation rulings D1–D7 to `flights/mfa_fidelity/rulings/` (cited PD1–PD7), a notation-scope ruling with the Overview↔contract↔frozen-spec translation table. Mike held it behind the terminal E1-R record; drafts and a repo-mirrored placement bundle exist in Mike's files (2026-10-11). v1.8 changes nothing in Flight 8's design.

---

## 5. Lessons of record from this session (bind these)

- **Detached jobs on Windows: never `-NoNewWindow`.** A process started that way dies silently when the launching PowerShell window closes. Use `-WindowStyle Hidden` with stdout/stderr redirected to files; then the window may be closed. Chains: write a `.ps1` and launch it hidden with `-File`; nested quoting in `-Command` fails silently.
- **The Windows venv `python.exe` is a launcher shim**; the real interpreter is its child. Poll the child's CPU time, not the parent's.
- **UTC manages Windows Update on CHA-88D57D3** ("not available due to your organization's policy"); local pause is disabled and a deadline restart (TrustedInstaller, 2026-10-09 23:20) killed a 10-hour package run. Long runs may be interrupted; relaunch is cheap because M7 writes every record last. For future long runs, ask IT for a deferral window or plan relaunches.
- **Measured costs on Mike's machine:** dense reference 33 min; stability audit 4.2 h; 200 projection sweeps 4.3 h; tolerance ensembles ~11 min/level (4.4 h for 24); tolerance program finalizer 5.2 h (full replay); each M6 audit ~1.3 h; benchmark 2 min; tranche 5 min; stage-1 package 13 h (full replay of everything). A production run would be ~2.7 h and 133 GB.
- **File placement:** send placement files with a version suffix; every placement block refuses on hash mismatch and reports `absent`; a same-named earlier download silently shadows a new one; `.py` and sometimes `.json` downloads sit as `Unconfirmed *.crdownload` until Keep — find them by hash, not name. Small canonical JSON can be written directly via `[IO.File]::WriteAllBytes` from an ASCII string.
- **Raw strings in `python -c` cannot end in a backslash** — pass directories without the trailing separator.
- **The shell's cwd resets after a reboot**; a commit block issued from `C:\Users\vkz244` fails with "not a git repository". Check `git log -1 --oneline` after any reboot before committing.
- **Fresh-clone verification is the standard** after every commit: identities, envelopes, stage commit unchanged, registry history, and (where cheap) the record's own validator.
- Channel facts from prior sessions still hold: L2 returns only as file uploads; echo-identities-first; one PowerShell command per fenced block; `Set-Clipboard` on every result.

---

*Written by L1 at Mike's request, 2026-10-15, after the terminal stage-1 package commit (`3ab65df`), verified from a fresh clone.*
