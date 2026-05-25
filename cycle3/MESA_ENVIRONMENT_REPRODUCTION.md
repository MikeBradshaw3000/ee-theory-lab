# Mesa Environment Reproduction Guide

**Purpose:** rebuild the working Mesa environment exactly, on a fresh machine or in a fresh Claude / Gemini / ChatGPT context, **without relying on memory**.

**How to use this document:** the `« FILL »` blocks below are filled *once*, by running the capture commands against the known-good machine, and then committed. Do not type version numbers from memory into the blocks — paste the captured output. This guide is the canonical environment record once the blocks are filled; until then it is a capture script with placeholders.

> Reference (verify, do not assume): the project lives under `C:\Users\vkz244\EE_Theory_Lab\`, Mesa is 3.x. Confirm both with the capture commands before treating them as true here.

---

## 0. Capture-from-known-good (do this first if a working machine still exists)

If the working environment is still intact, capture ground truth before anything else, then paste into the blocks below.

```powershell
# from the project root, with the project venv ACTIVE
python --version
python -c "import sys; print(sys.executable)"
python -c "import mesa, sys; print('mesa', mesa.__version__)"
pip freeze > requirements.lock.txt
```

`requirements.lock.txt` is the authoritative pin set. Everything else in this guide is the human-readable path to reproducing what that file encodes.

---

## 1. Python version

`« FILL: paste output of python --version »`

Minimum compatible / recommended interpreter for this environment: `« FILL »`. Mesa 3.x requires a modern CPython; record the exact version used so a rebuild does not silently drift.

## 2. Virtual environment setup

A dedicated venv per project. Do **not** install into system Python.

```powershell
cd C:\Users\vkz244\EE_Theory_Lab
python -m venv .venv
```

(If multiple Python versions are installed, invoke the intended one explicitly, e.g. `py -3.x -m venv .venv`, and record the launcher used here: `« FILL »`.)

## 3. Activate the environment

PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is blocked by execution policy:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
(Process scope only — does not change machine policy. Re-run per session if needed.)

**Confirm activation before proceeding** — see §7. The prompt showing `(.venv)` is necessary but **not** sufficient evidence; verify the interpreter path.

## 4. Package installation

**Preferred path (reproducible):** install from the committed lock file.
```powershell
pip install --upgrade pip
pip install -r requirements.lock.txt
```

**Cold path (no lock file yet):** install the named direct dependencies, then immediately freeze.
```powershell
pip install --upgrade pip
pip install mesa==« FILL »
# visualization stack, only if the project actually uses it — see §5
pip install solara==« FILL »
# analysis stack used by the Tier-2 / diagnostic scripts
pip install numpy==« FILL » pandas==« FILL » scipy==« FILL » pyarrow==« FILL »
pip freeze > requirements.lock.txt
```

> `pyarrow` is listed because the substrate persists parquet. Confirm against the lock file whether it is a direct dependency or pulled transitively, and record: `« FILL: direct / transitive »`.

## 5. Mesa version and visualization / Solara dependencies

- Mesa version in use: `« FILL »` (the 3.x line changed the visualization API substantially vs 2.x — pin it).
- Does this project run the Mesa/Solara browser visualization, or is it headless batch + offline analysis only? `« FILL: yes-Solara / headless-only »`
- If Solara is used: version `« FILL »`, and note that the React/interactive Scheffer and wave-zipper visualizations are **separate** from the Mesa-Solara server and do not impose a Solara dependency on the ABM itself. Keep the two straight when pinning.

## 6. Dependency pins / lock-file recommendation

- Commit `requirements.lock.txt` (full `pip freeze`) as the authoritative environment.
- Keep a short hand-written `requirements.txt` listing only **direct** dependencies with `==` pins, for human readability. The lock file is what a rebuild installs from; the short file is what a human reads.
- Record the pin set's capture date and the machine it came from here: `« FILL: date / machine »`. A pin set with no provenance is the environment-level version of the proliferation problem.

## 7. Confirm the ABM is using the intended environment (not system Python)

This is the environment analogue of the four-level distinction: "Python ran" ≠ "the intended Python ran." Verify, every fresh session:

```powershell
python -c "import sys; print(sys.executable)"
# MUST print a path inside ...\EE_Theory_Lab\.venv\ — NOT C:\Python3x\ or a global install
python -c "import mesa, sys; print(mesa.__version__, sys.executable)"
```

Expected interpreter path: `« FILL: paste the .venv python.exe path »`
Expected Mesa version: `« FILL »`

If `sys.executable` points anywhere outside the project venv, stop — the activation did not take. Do not run any ABM script until this matches.

## 8. PowerShell hazards and copy/paste rules

These have bitten the project before; they are recorded so they do not again.

- **Em-dashes in YAML front-matter must be ASCII hyphens.** Pandoc front-matter chokes on `—`; use `-`. Greek characters render correctly in the document body — the hazard is the YAML block specifically.
- **Here-string idiom for file writes.** Write multi-line files with a PowerShell here-string rather than pasting line-by-line:
  ```powershell
  @'
  ...file contents, literal, no variable expansion...
  '@ | Set-Content -Encoding utf8 path\to\file.py
  ```
  Use the single-quoted `@' ... '@` form to prevent `$` interpolation mangling code. The closing `'@` **must** be at column 0 (no leading whitespace) or PowerShell will not terminate the string.
- **Encoding:** write with `-Encoding utf8`. Greek symbols (ρ, Ψ, Λ, μ) in script comments/strings will corrupt under the default encoding on some hosts.
- **Smart quotes from chat → editor.** Pasting code out of a chat client can substitute `"` `'` `—` for ASCII forms. After any paste of code, confirm quotes and dashes are ASCII before running.
- **Path separators:** Windows paths use `\`; when a path is handed to a Python string, prefer raw strings `r"C:\Users\..."` or forward slashes to avoid escape-sequence surprises.

## 9. Minimal Mesa smoke test

Confirms Mesa imports and a trivial model steps under the intended interpreter. This is an **L1 environment check only** — it says nothing about any Cycle 3 observable.

```powershell
@'
import mesa, sys
print("interpreter:", sys.executable)
print("mesa:", mesa.__version__)

class Walker(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.steps_taken = 0
    def step(self):
        self.steps_taken += 1

class TinyModel(mesa.Model):
    def __init__(self, n=5, seed=42):
        super().__init__(seed=seed)
        for _ in range(n):
            Walker(self)
    def step(self):
        self.agents.do("step")

m = TinyModel()
for _ in range(3):
    m.step()
print("agents:", len(m.agents))
print("total steps:", sum(a.steps_taken for a in m.agents))
print("SMOKE TEST OK")
'@ | Set-Content -Encoding utf8 mesa_smoke_test.py
python mesa_smoke_test.py
```

Expected tail: `SMOKE TEST OK`, with `agents: 5` and `total steps: 15`, and an interpreter path inside `.venv`.

> Note: the Mesa 3.x `Agent` / `Model` constructor signatures differ from 2.x (3.x passes `model` positionally to `Agent.__init__` and uses `model.agents` / `AgentSet.do`). If the smoke test errors on the constructor, the installed Mesa is not the intended major version — recheck §5.

## 10. From zero to first successful local run

Ordered sequence. Do not skip the verification steps.

1. `cd C:\Users\vkz244\EE_Theory_Lab`
2. Create venv (§2) — or confirm `.venv` exists.
3. Activate (§3).
4. **Verify interpreter path (§7)** — gate; do not pass until it points into `.venv`.
5. Install from `requirements.lock.txt` (§4 preferred path).
6. Run the Mesa smoke test (§9) — must print `SMOKE TEST OK`.
7. Re-verify Mesa version matches §5.
8. Run the project's own minimal/sentinel ABM script (record which one is the designated sentinel: `« FILL: script path »`), confirming it (a) starts under the venv interpreter and (b) writes its output to the expected location.
9. Confirm output artifacts landed where expected and are well-formed (open one, check finite values) — this is still L1, not interpretation.
10. Record the run in the test registry with a TEST_RECORD entry. First real run included.

When step 10 is done, the environment is reproduced *and* the reproduction is documented. Either without the other is incomplete.
