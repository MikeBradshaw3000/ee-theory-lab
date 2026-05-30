# OBS001_10 - Layer 3 v1 code (VERBATIM GAP FLAGGED)

## Notice: This artifact body is not recoverable verbatim.

The recovery instance attempted to retrieve Layer 3's v1 code from the 2026-05-28 session and confirmed the following:

- Layer 3 returned the v1 code to Mike outside this chat (in the Gemini session).
- Mike attached it to the conversation as a file, not pasted inline. The transcript shows the user turn at this point as: `Files: - unnamed (UUID: 46246e1e-6bc5-4f93-886e-8ae8a6eb6840, Purpose: attachment); Content: "layer 3 code."`
- The attachment file is not present in `/mnt/user-data/uploads/` at the time of recovery (empty directory).
- The transcript at `/mnt/transcripts/2026-05-30-18-32-10-obs001-routing-archive-recovery.txt` references the UUID but does not contain the file's textual content.
- `conversation_search` does not return the v1 code body either.

Per the recovery-request discipline ("A flagged gap is recoverable; a silent reconstruction corrupts the archive's purpose"), the v1 code body is flagged here as not recoverable rather than reconstructed.

## Derived record (NOT the v1 body - describes only how v1 differed from v2)

What IS in the transcript verbatim is Layer 1's review of v1 against the contract - specifically `OBS001_11_LAYER1_CODE_REVIEW.md`. From that review, the four ways v1 differed from v2 (which IS recoverable verbatim at `OBS001_12_LAYER3_CODE_V2.md`) are:

1. **Parity check was unseeded.** v1's `run_parity_check` went directly to `test_grids = np.random.randint(0, 2, size=(100, 50, 50))` without first setting `PARITY_SEED = 7` and `np.random.seed(PARITY_SEED)`. The parity test inputs varied across pre-flight invocations.

2. **Top docstring used stronger claim language.** v1 said the parity check is "proving byte-for-byte mathematical equivalence" rather than "testing byte-for-byte mathematical equivalence" (v2). The `run_parity_check` docstring said "Validates local reimplementations against validated apparatus modules" rather than "Tests local reimplementations against apparatus modules" (v2).

3. **`import mesa` had no explanatory comment.** v1 imported mesa in the pre-flight `try` block but did not document why, given that the substrate logic itself does not use mesa. v2 added the explanatory comment: "C3-ENV-001 names Mesa 3.5.1 as a pinned dependency; if it fails to import, the environment itself is compromised regardless of whether this specific script uses it."

4. **Parity check did not cover the null functions.** v1's parity check verified `calculate_morans_i_toroidal_8`, `batch_morans_i_toroidal_8`, and `evaluate_window_ss` against CTL-001 and SS-001 respectively. It did NOT verify `compute_persistence_null` or `compute_meanI_state_null`. v2 added two additional parity sections at the end of `run_parity_check` covering both null functions, using the seed-reset pattern (`np.random.seed(PARITY_SEED)` before each pair of paired calls) so both functions consume identical random state.

These four differences are the substance of Layer 1's correction note. The substantive sections of v1 (substrate logic, sweep structure, configuration constants, telemetry schema, degeneracy diagnostics, output column structure, vocabulary discipline, naming discipline) were byte-equivalent to v2 - confirmed by Layer 1's pessimistic-on-passing cross-check at the second review pass.

## How to recover the v1 body if needed

The original attachment Mike used (UUID 46246e1e-6bc5-4f93-886e-8ae8a6eb6840) was a file on Mike's local machine, most likely saved to his Downloads folder by Gemini. If a verbatim v1 body is genuinely needed for the archive, Mike may still have that file locally and could attach it to the current session for direct transcription. Otherwise, the derived record above plus the v2 body at OBS001_12 with the four-item correction list at OBS001_11 constitute the canonical-record account of what v1 was and how it differed from v2.
