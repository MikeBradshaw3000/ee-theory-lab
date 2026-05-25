# Mesa Environment Reproduction Guide

**Purpose:** rebuild the working Mesa environment exactly, on a fresh machine or in a fresh Claude / Gemini / ChatGPT context, **without relying on memory**.

**Status:** environment captured and standardized 2026-05-25 (see Sec. 0a). The capture blocks below are filled from the known-good machine; this guide is now the canonical reproduction record, paired with `cycle3/ENVIRONMENT_SNAPSHOT.md` (the raw capture) and `cycle3/requirements.lock.txt` (the authoritative pin set).

> Division of labor, so the documents do not compete: this guide = *how to reproduce* and the verification discipline; `ENVIRONMENT_SNAPSHOT.md` = *what was captured*; `requirements.lock.txt` = the exact pins a rebuild installs from. The guide points at the snapshot and lock file rather than duplicating their contents.

---

## 0a. Standardization decision (2026-05-25)

Cycle 3 standardizes on the **existing top-level `venv`** at `C:\Users\vkz244\EE_Theory_Lab\venv\`, captured 2026-05-25:

- Interpreter: `C:\Users\vkz244\EE_Theory_Lab\venv\Scripts\python.exe`
- Python `3.14.4`
- Mesa `3.5.1`

This was Mike's arbitration. Earlier drafts of this guide used a generic `.venv` placeholder name; that was a convention guess, not the actual directory. The directory is `venv` (no leading dot). Cycle 3 does not create a separate `.venv`. If a future cycle decides to standardize on a fresh `.venv`, that is a new decision recorded at that time — it does not retroactively apply here.

## 0b. Capture-from-known-good (for a future re-capture or a fresh machine)

To re-capture (e.g. after a dependency change), with the project `venv` ACTIVE:

```powershell
python --version
python -c "import sys; print(sys.executable)"
python -c "import mesa, sys; print('mesa', mesa.__version__)"
pip freeze > requirements.lock.txt
```

`requirements.lock.txt` is the authoritative pin set. Everything else here is the human-readable path to reproducing what that file encodes.

---

## 1. Python version

**Python 3.14.4** (captured 2026-05-25). Record the exact version so a rebuild does not silently drift; Mesa 3.x requires a modern CPython.

## 2. Virtual environment setup

A dedicated venv per project, at the project root. Do **not** install into system Python. The Cycle 3 canonical venv already exists at `C:\Users\vkz244\EE_Theory_Lab\venv\`. To rebuild it from scratch on a fresh machine:

```powershell
cd C:\Users\vkz244\EE_Theory_Lab
py -3.14 -m venv venv
```

(If the `py` launcher is unavailable or 3.14 is not installed, install CPython 3.14.4 first, then invoke that interpreter's `-m venv venv`.)

## 3. Activate the environment

PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

If activation is blocked by execution policy:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
(Process scope only - does not change machine policy. Re-run per session if needed.)

**Confirm activation before proceeding** - see Sec. 7. The prompt showing `(venv)` is necessary but **not** sufficient evidence; verify the interpreter path.

## 4. Package installation

**Preferred path (reproducible):** install from the committed lock file.
```powershell
pip install --upgrade pip
pip install -r requirements.lock.txt
```

`cycle3/requirements.lock.txt` is the full `pip freeze` from the captured environment. It is the authoritative source for every pin, including Mesa 3.5.1 and its transitive dependencies. Do not hand-list versions here that the lock file already encodes — read them from the lock file.

## 5. Mesa version and visualization / Solara dependencies

- Mesa version in use: **3.5.1** (captured 2026-05-25). The 3.x line changed the visualization API substantially vs 2.x; the lock file pins it.
- Whether the project runs the Mesa/Solara browser visualization or is headless batch + offline analysis: confirm against `requirements.lock.txt` (presence/absence of `solara` and its version). The React/interactive Scheffer and wave-zipper visualizations are **separate** from any Mesa-Solara server and do not impose a Solara dependency on the ABM itself — keep the two straight.

## 6. Dependency pins / lock-file recommendation

- `cycle3/requirements.lock.txt` (full `pip freeze`) is committed as the authoritative environment.
- Optionally keep a short hand-written `requirements.txt` listing only **direct** dependencies with `==` pins for human readability. The lock file is what a rebuild installs from; the short file is what a human reads.
- Capture provenance: **date 2026-05-25, machine = Mike's known-good Windows box, venv = `C:\Users\vkz244\EE_Theory_Lab\venv\`.** A pin set with no provenance is the environment-level version of the proliferation problem.

## 7. Confirm the ABM is using the intended environment (not system Python)

The environment analogue of the four-level distinction: "Python ran" is not "the intended Python ran." Verify, every fresh session:

```powershell
python -c "import sys; print(sys.executable)"
python -c "import mesa, sys; print(mesa.__version__, sys.executable)"
```

Expected interpreter path: `C:\Users\vkz244\EE_Theory_Lab\venv\Scripts\python.exe`
Expected Mesa version: `3.5.1`

If `sys.executable` points anywhere outside the project `venv` (e.g. a global `C:\Python3xx\` install or `venv_cycle1_archive`), stop - the activation did not take. Do not run any ABM script until this matches.

## 8. PowerShell hazards and copy/paste rules

These have bitten the project before; they are recorded so they do not again.

- **Em-dashes in YAML front-matter must be ASCII hyphens.** Pandoc front-matter chokes on the em-dash glyph; use `-`. Greek characters render correctly in the document body - the hazard is the YAML block specifically.
- **Here-string idiom for file writes.** Write multi-line files with a PowerShell here-string rather than pasting line-by-line:
  ```powershell
  @'
  ...file contents, literal, no variable expansion...
  '@ | Set-Content -Encoding utf8 path\to\file.py
  ```
  Use the single-quoted `@' ... '@` form to prevent `$` interpolation mangling code. The closing `'@` **must** be at column 0 (no leading whitespace) or PowerShell will not terminate the string.
- **Encoding:** write with `-Encoding utf8`. Greek symbols (rho, Psi, Lambda, mu) in script comments/strings will corrupt under the default encoding on some hosts.
- **Smart quotes from chat to editor.** Pasting code out of a chat client can substitute curly quotes and em-dashes for ASCII forms. After any paste of code, confirm quotes and dashes are ASCII before running.
- **One command per copy-pane, wait for output.** Do not batch multiple commands in a single block; paste, run, return output, then the next. `pip freeze` and similar long outputs go to the clipboard (`| Set-Clipboard`) when too long to mouse-select.
- **Path separators:** Windows paths use `\`; when a path is handed to a Python string, prefer raw strings `r"C:\Users\..."` or forward slashes to avoid escape-sequence surprises.

## 9. Minimal Mesa smoke test

The smoke test is the committed file **`cycle3/mesa_smoke_test.py`** (created and passed under the captured `venv` on 2026-05-25, test record `C3-ENV-001`). It is the canonical smoke test — do not re-embed or re-create a copy here, to avoid a near-twin. To run it:

```powershell
python cycle3\mesa_smoke_test.py
```

Expected tail: `SMOKE TEST OK`, with the active-agent / step counts the script asserts, and an interpreter path inside `venv`. This is an **L1 environment check only** - it says nothing about any Cycle 3 observable.

> Note: the Mesa 3.x `Agent` / `Model` constructor signatures differ from 2.x (3.x passes `model` positionally to `Agent.__init__` and uses `model.agents` / `AgentSet.do`). If the smoke test errors on the constructor, the installed Mesa is not the intended major version - recheck Sec. 5.

## 10. From zero to first successful local run

Ordered sequence. Do not skip the verification steps.

1. `cd C:\Users\vkz244\EE_Theory_Lab`
2. Confirm `venv` exists, or rebuild it (Sec. 2).
3. Activate (Sec. 3).
4. **Verify interpreter path (Sec. 7)** - gate; do not pass until it points into `venv` and Mesa reads 3.5.1.
5. Install from `requirements.lock.txt` (Sec. 4 preferred path).
6. Run the committed Mesa smoke test (Sec. 9) - must print `SMOKE TEST OK`.
7. Re-verify Mesa version matches Sec. 5.
8. Run the project's own minimal/sentinel ABM script once one is designated for Cycle 3 (record which: `[TBD — Cycle 3 sentinel not yet designated]`), confirming it (a) starts under the `venv` interpreter and (b) writes output to the expected location.
9. Confirm output artifacts landed where expected and are well-formed (open one, check finite values) - still L1, not interpretation.
10. Record the run in the test registry with a TEST_RECORD entry.

When step 10 is done, the environment is reproduced *and* the reproduction is documented. Either without the other is incomplete.
