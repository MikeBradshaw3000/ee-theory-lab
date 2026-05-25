# claude_session_handoffs/ — directory note

**Role:** historical record. Each dated subfolder is a point-in-time session handoff — the working state captured at the close of that session. Preserved per the operations-log honest-record principle (logs are not retroactively edited; they record what happened on their date).

## These are snapshots, not canonical sources

Some subfolders contain *copies* of artifacts that also live, in evolved form, elsewhere in the repo — notably `claude_instantiation_kit_v*.md`, `STANDING_ITEMS.md`, and various scripts. **Those copies are frozen snapshots of what the artifact looked like at that session. They are NOT the current canonical version.**

Current canonical locations (use these, never the dated copies):
- Instantiation kit → repo root (`claude_instantiation_kit_v4.md`, `_v5.md`, `_v5_1.md` — newest applies).
- `STANDING_ITEMS.md` → repo root.
- Scripts (`flight2_production.py`, `item_6a_stage1_eda.py`, etc.) → their canonical locations in the tree; verify path before reference.

Do not restore or reconstruct a canonical artifact from a handoff copy. If a dated copy and the canonical version disagree, the canonical version wins; the copy is only evidence of past state.

## Why some duplicate copies are absent from git

During the Cycle 2 closure (2026-05-24), the duplicate kit/STANDING_ITEMS/script copies inside this tree were **deliberately not committed**, to avoid hardening the proliferation that the continuity note identified as the reason the B2 source was once lost. The session *logs* are committed; the duplicate *canonical-artifact copies* are not. This absence is a decision, recorded here and in `cycle2/CYCLE2_CLOSURE.md` §3 (Population B), not an oversight.

## Span

Committed session handoffs span sessions 9–25. See `cycle2/CYCLE2_CLOSURE.md` for the full Cycle 2 closure record.
