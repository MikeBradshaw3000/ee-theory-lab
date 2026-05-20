# Environment Reference

**Document role.** Operational reference for the production environment, dependency versions, and toolchain hazards. Distinct from `current_state.md` (session-volatile state) and `theoretical_context.md` (stable theoretical content) — this document holds operational/environmental detail that future Claude instances need for substrate and analytical work but that doesn't fit either of those documents' purposes.

**Authority.** Authoritative for documented environment specifications. When this document conflicts with primary source (actual installed versions, actual file paths, actual Python behavior), primary source wins and this document revises. The PowerShell command `python -c "import sys; print(sys.version)"` and equivalents are primary source for what is actually installed.

**Maintenance discipline.** Updated when the environment changes — Python version upgrade, dependency version change, new toolchain hazard surfaced through operational experience, path convention change. Updates committed alongside the operations log of the session in which the change occurred.

---

## Section 1: Production machine workspace

**Canonical workspace path:** `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\` (lowercase nested).

The repository root sits at the lowercase nested path. PowerShell prompts on Mike's machine typically show this path; commands assume Mike's shell is at this directory unless explicitly stated otherwise. Path conventions in this document and elsewhere are *relative to this directory* — Layer 1 commands should not prefix `ee-theory-lab\` as if from the parent directory. (Session 9 surfaced this as a path-doubling error; the corrective: treat the workspace as Mike's actual working directory, not as a path to be reproduced as a prefix.)

**Stale parallel tree to be archived:** `C:\Users\vkz244\EE_Theory_Lab\phase_4B\` (capital B at the top level — sibling of the canonical workspace, not inside it). To be archived during restructure Stage 4.

**Canonical data outputs:** `C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\` (absolute path; named `flight2_outputs` for inheritance reasons but contains Flight 6 files; the naming will be resolved during restructure Stage 4).

**Not inside OneDrive.** Verified 14 May 2026: OneDrive is anchored at `C:\Users\vkz244\OneDrive - University of Tennessee\` but this project sits alongside it. Environment is stable across network changes.

---

## Section 2: Python environment

**Virtual environment:** `C:\Users\vkz244\EE_Theory_Lab\venv\`

**Python version:** 3.14.x (Python 3.14.4 was the version verified 15 May 2026 per prior-cycle record; the venv is portable and survives network changes).

**Activation pattern:**

```powershell
cd C:\Users\vkz244\EE_Theory_Lab
.\venv\Scripts\activate
```

PowerShell prompt shows `(venv)` when active.

**Session-resilience check at script launch.** Substrate and analysis scripts should verify environment before running:
- `sys.prefix != sys.base_prefix` (venv active)
- Python version is 3.14.x
- Critical imports work (numpy, pandas, pyarrow, mesa, solara)

Fail-fast with actionable error messages. Network-switch resilient by design.

---

## Section 3: Dependencies

**Core dependencies:**
- `numpy` 2.4.4
- `pandas` 3.0.3
- `pyarrow` 24.0.0
- `mesa` 3.x (Mesa 3.x specifically; 2.x API is deprecated and the protocol does not use it)
- `solara` (recent)
- `networkx` (transitive dependency of mesa — common post-install pitfall when installed separately)
- `matplotlib`
- `altair`
- `scipy` (recent)
- `psutil` (optional, for memory diagnostics)

**Mesa 3.x API notes:**
- Flat namespace: imports like `from mesa.visualization import SolaraViz, make_space_component, make_plot_component, Slider`.
- Do not fabricate paths like `mesa.visualization.solara_viz.solara_viz` — that path does not exist; earlier work hallucinated it.
- Activation pattern: `model.agents.do("step")` and `model.agents.do("advance")` for synchronous two-phase update. `RandomActivation` is deprecated.

**numpy version pitfall:** Recent numpy versions moved `np.RankWarning` to `np.exceptions.RankWarning`. Scripts using the old path will fail with `AttributeError`. Either update the import path or remove warning-suppression lines.

---

## Section 4: PowerShell hazards and conventions

**File write idiom for Python source files.** Do not edit Python files via Notepad — it silently adds a UTF-8 BOM that Solara's autorouter chokes on. Use PowerShell here-string with explicit BOM-less UTF-8:

```powershell
[System.IO.File]::WriteAllText($path, $code, [System.Text.UTF8Encoding]::new($false))
```

PowerShell often does not auto-execute the final line after paste; Mike presses Enter manually.

**Pager bypass for git.** `git --no-pager <command>` bypasses the pager when long output is expected. When stuck in the pager interactively, `q` exits.

**Paste-back failure mode.** PowerShell commands in fenced code blocks should be unambiguously paste-targets. If a response is going to be pasted back into PS as if it were a command, that's a paste-back incident; recovery is Ctrl+C or Enter on an empty line to clear PS's multi-line continuation. Lean response text immediately above and below fenced command blocks keeps paste-targeting unambiguous. (Captured operationally in `protocols/foundational/standing_rules.md` Rule 2 and the instantiation kit's working-pattern section.)

---

## Section 5: Repository

**Repository path:** `C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\`

**Remote:** `https://github.com/MikeBradshaw3000/ee-theory-lab`

**Push discipline.** Local main may run several commits ahead of origin/main between push events; pushes fire at natural commit-cluster boundaries rather than per-commit. See `STANDING_ITEMS.md` for the current push-to-origin item if one is open.

---

## Section 6: Tools

- **Mesa 3.x + SolaraViz** — ABM substrate environment.
- **VS Code** — text editor, pure-editor mode (AI-agent features unused per protocol convention).
- **PowerShell** — Windows shell.
- **Node.js / docx npm package** — Word document generation (used selectively for Phil-facing artifacts).
- **ReportLab** — PDF transcripts.
- **Python + NumPy** — analytical work, Tier 3 regression execution.

---

## Section 7: Distribution pattern for multi-file delivery

When delivering multiple files to Mike's machine, the minimum-thumb-work pattern is *separate-file downloads*, not zips. The instantiation kit Section 3 specifies the convention; multi-file `present_files` calls bundle as zip (which requires `Expand-Archive`), while sequential single-file `present_files` calls deliver as separate files (which require only `Move-Item`).

For substantial multi-file operations where even sequential `present_files` is heavy, the alternative pattern is *Python+base64 distribution scripts*: one Python script with all files embedded as base64, Mike saves once, pastes one PowerShell block, files land at correct paths. Used in prior-cycle work for initial repo commit and Flight 2 closure commit; pattern preserved.

---

— Drafted by Claude as Layer 1 central node, session 10, deliverable 3 of item 9 reconciliation. New foundational document carrying prior-cycle environment/operational content into the canonical record. Pending Layer 2 sanity scan before commit.
