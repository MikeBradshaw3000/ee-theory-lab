# ORIENTATION

**You are looking at the EE Theory Lab repository.** This file is the entry point for any fresh reader — Claude instance, Mike, or any other party — who needs to orient on what this repository is and where to find things.

The repository supports the EE Theory Lab project: a formal generative theory of entrepreneurial ecosystem (EE) emergence, developed by Mike Bradshaw (Theory Architect, Max Fuller Center for Innovation and Entrepreneurship, University of Tennessee at Chattanooga) in collaboration with Dr. Phil Roundy. The repository is the canonical record for Phase 4B work (substrate implementation, analytical procedures, regression results) and the protocol infrastructure for the multi-AI collaboration that supports that work.

---

## What to read first

The order depends on who you are and what you need.

**Fresh Claude instance starting a new chat:** read the instantiation kit first. The kit is attached at session open by Mike; it lives in `claude_session_handoffs/YYYY-MM-DD[-N]/` directories. The kit is the compressed cold-start surface; it points you at the canonical material when you need it.

**Anyone wanting the protocol structure:** start at `protocols/foundational/README.md`. It is the entry point for the foundational document set — six documents covering protocol structure, standing rules, vocabulary discipline, canonical artifacts, current state, and the reading sequence among them.

**Anyone wanting current project state:** read `CURRENT_STATE.md` at this root level. It is the project-level current state, complementary to `protocols/foundational/current_state.md` (which is scoped to Phase 4B and protocol infrastructure).

**Anyone wanting to know what's at this top level:** read `MANIFEST.md` at this root level. It lists the top-level directories and what each contains.

---

## What this repository contains

This is a high-level pointer set. For canonical detail on artifact locations and authority, see `protocols/foundational/canonical_artifacts_index.md`.

- **`protocols/foundational/`** — Canonical foundational document set (six documents). Load-bearing protocol infrastructure that Claude instances instantiate against. Authority: each document is authoritative for its content domain.
- **`phase_4b/`** — Phase 4B work: substrate-output-consumer scripts, intake module, regression consumer, pre-registrations, regression outputs, Tier 1/2 derived outputs, cross-run analyses. Heavy directory; see `canonical_artifacts_index.md` for what is where.
- **`flights/`** — Flight specifications. Includes the Flight 6 Substrate Specification v1.1 at `flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf`.
- **`operations_log/`** — Session-by-session operations logs. Each session's log captures what happened, what was committed, what is open, and the resume anchor for the next session.
- **`claude_session_handoffs/`** — Session-handoff folders for cold-starting fresh Claude chats. Each folder contains the kit and the just-closed session's operations log.
- **`RESTRUCTURE_INVENTORY.md`** (workspace root) — Stage 0 inventory deliverable from the repository restructure. Categorizes working-tree files and specifies the Stage 2 moves-plan.
- **`STANDING_ITEMS.md`** (workspace root, pending Stage 1) — Deferred-items tracker. Each item has a trigger condition and acceptance criterion; the tracker is consulted at session open per the bullet-proof deferral process.

Several substantive specifications (State of the Theory v1.1, v1.5 Overview, Phase 4B Specification v1.1) live at specific paths or as Mike-local files. See `canonical_artifacts_index.md` Section 1 and Section 11 for canonical location and citation discipline.

---

## What this repository does not contain

- **Manuscript drafts.** Phil's v1.5 Overview manuscript work is independent of this repository; the manuscript-side workstream is Phil's. References to manuscript implications in operations logs are at protocol level, not draft level.
- **Personal communication.** Conversational material between Mike and Claude, ChatGPT, or Gemini is captured in operations logs as substantive findings, not as transcripts.
- **Side-channel notes that compete with the kit for instantiation authority.** Per the protocol, opening instructions for next-session Claude are single sentences pointing at the kit; substantive operational knowledge lives inside the kit (or in the foundational set the kit points at).

---

## The repository is mid-restructure

As of session 9, the repository is in Stage 1 of a six-stage restructure. Many files in working-tree positions are pending `git mv` operations during Stage 2; the canonical destinations are specified in `RESTRUCTURE_INVENTORY.md`. If a path in this orientation document or the artifacts index does not yet match the canonical destination, it is because Stage 2 has not executed. The Stage sequence:

- **Stage 0** — Freeze and inventory. Committed.
- **Stage 1** — Add orientation spine. In progress.
- **Stage 2** — Move canonical artifacts via `git mv`.
- **Stage 3** — Add manifests for parquet outputs and substrate files.
- **Stage 4** — Quarantine stale and scratch material.
- **Stage 5** — Resume Phase 4B analytical work.

For the current restructure status, see `CURRENT_STATE.md` and `protocols/foundational/current_state.md`.

---

## Authority hierarchy

When documents conflict, the hierarchy is:

1. **Primary source** — the actual files, code, git log, parquet metadata. Wins over all descriptions.
2. **Canonical specifications** — State of the Theory v1.1, Phase 4B Specification v1.1, Flight 6 Substrate Specification v1.1. Each is authoritative for its content domain.
3. **Foundational document set** — `protocols/foundational/`. Authoritative for protocol structure, standing rules, vocabulary, artifact locations, current state.
4. **Operations logs** — historical record. Authoritative for what happened in past sessions; for historical session facts, operations logs outrank the instantiation kit.
5. **Instantiation kit** — compressed surface over the foundational set. Wins over working memory but loses to canonical material and to operations logs for historical claims.
6. **This orientation document** — surface-level entry pointer. Not authoritative for content; defers to the documents it points at.

Per Rule 1, primary-source verification is the discipline that makes the hierarchy operational.

---

— Drafted by Claude as Layer 1 central node, Stage 1 root-level orientation, session 9. Layer 2 sanity scan return incorporated (authority hierarchy patch: operations logs reordered above instantiation kit for historical-session-fact authority). Ready for commit.
