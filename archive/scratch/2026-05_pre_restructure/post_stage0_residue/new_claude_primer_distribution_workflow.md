# New Claude Primer Distribution Workflow

One file to commit: the updated `new_chat_primer.md` at `protocols/onboarding/new_chat_primer.md`.

This overwrites the existing Cycle 1 primer with the Cycle 2 Round 1 / post-Flight-2 version. The old primer doesn't reflect Flight 1/2 closures, standing rule #5, the three substantive findings, the v1.1 relationship clarification, or the calibration items. The new primer carries all of those.

## Step 1: Save `distribute_new_claude_primer.py`

Save the attached file to `C:\Users\vkz244\EE_Theory_Lab\`.

## Step 2: Run the distribution and commit

```powershell
cd C:\Users\vkz244\EE_Theory_Lab

python distribute_new_claude_primer.py

cd ee-theory-lab

Write-Host "`n=== File staged for commit ===" -ForegroundColor Cyan
git status --short

git add -A

Write-Host "`n=== Final commit preview ===" -ForegroundColor Cyan
git diff --cached --stat

git commit -m "Update new_chat_primer.md for Cycle 2 Round 1 post-Flight 2 closure state"
git push

Write-Host "`n=== Primer updated ===" -ForegroundColor Green
```

## Expected output

1. Python prints "Wrote new_chat_primer.md (14,228 bytes)..."
2. `git status --short` shows `M protocols/onboarding/new_chat_primer.md` (modified — the file already exists from the Cycle 1 commit)
3. `git diff --cached --stat` shows one file modified with line counts
4. Commit and push complete

If `git status` shows `??` (new file) instead of `M` (modified), that just means the prior path was different and you're committing fresh. Either is fine.

## After committing the primer

Send the session transition note (`session_transition_note_to_gemini_chatgpt.md`) to Gemini and ChatGPT before you sign off. They should be calibrated for the new Claude session before you start it tomorrow.

— Drafted by Claude
