# L2 Independent Changed-Source Verification — E1 Stage-1 Module M7, Round 6

**Reviewer:** L2  
**Date:** 2026-10-04  
**Reviewed packet SHA-256:** `3b8d496be069edc82b6fba956e3d771a1247ae235942c9ac4450171deb8edda6`  
**Round-5 cleared baseline:** `e1/runner.py` `7d943998d35d315150638e4c74f74d0c8d760ebd6314c451d077387c44873e7d`; `tests/test_e1_m7.py` `cb7de9cd9901355db78862e17f032460613264b827faf4bc433fd5e4e0aed944`  
**Round-6 extracted identities:** `e1/runner.py` `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769`; `tests/test_e1_m7.py` `23bd6e69a0ab37d0316e8e8407dc9c9e5211ef7849054959221b272c35030785`

## 1. Independent identity verification

I independently reconstructed the supplied Round-6 packet from the authoritative file content and recomputed its SHA-256. The full packet digest is:

`3b8d496be069edc82b6fba956e3d771a1247ae235942c9ac4450171deb8edda6`

This matches the routed packet identity prefix `3b8d496b…`.

I independently extracted the two cumulative fenced source files and hashed their verbatim contents with their terminal LF. They reproduce the Round-6 identities above. I did not take those source identities from L1's digest block as the verification operation.

## 2. Changed-source comparison against the cleared Round-5 baseline

I compared the extracted Round-6 runner directly against the Round-5 runner that I cleared at `7d943998…73e7d`.

The runner diff is exactly **41 changed lines: 22 additions and 19 deletions**. I find no undisclosed executable change outside that changed set. The changes are:

- import of `posixpath` as `_pp`;
- `RUNNER_VERSION` moved from v5 to v6;
- five repo-relative declared paths changed from `os.path.join(...)` constructions to fixed POSIX literals;
- the frozen runner-declaration digest changed to the new v6 identity;
- `verify_frozen_identity()` gained a fail-closed backslash/platform-independence guard;
- repo-relative Git/pathspec and committed-object compositions on the reviewed surface use `_pp.join` rather than host-dependent `os.path.join`;
- `_require_committed` normalizes `os.path.relpath(...)` to `/` before the Git-object check.

These changes correspond to the disclosed 41-line runner diff. They do not alter the Round-5 scientific/governance mechanics, package predicates, authorization semantics, router replay, tolerance program, benchmark semantics, or memoization logic.

The extracted test file compares against the cleared Round-5 test source as disclosed: the module-scoped `chain` fixture setup is enclosed in `try/except BaseException` with `mp.undo()` before re-raising, and one Round-6 platform-independence regression test is appended. I found no other substantive test change.

## 3. Windows placement failure and source repair

The reported Round-5 placement failure is consistent with the cleared source: `GOVERNANCE_ROOT_REL` was constructed with `os.path.join` and is embedded in `RUNNER_DECLARATION`. On Windows, that construction produces a backslashed value, so a declaration digest frozen from Linux bytes cannot reproduce. M7 therefore correctly failed closed, but the declaration itself was not platform-independent.

Round 6 repairs that defect at its source. The declaration-bound path is now a literal POSIX repo-relative string, and all five declared path constants are likewise fixed POSIX literals. Repo-relative Git pathspec construction is explicitly POSIX. Host-filesystem access still joins the repository root to those relative strings with `os.path.join`, which is appropriate: Windows accepts forward slashes in such relative path components, while the identity/pathspec surface remains platform-independent.

The new guard is also useful defense in depth. A backslash in the frozen declaration representation or any of the five declared path constants makes `verify_frozen_identity()` refuse rather than allowing a host-specific declaration to proceed.

I find the source repair correctly targeted to the observed Windows placement defect.

## 4. Fixture-leak repair

The second reported failure mode is also credible from the Round-5 test source. The module-scoped `chain` fixture creates a manual `pytest.MonkeyPatch` and previously reached `mp.undo()` only after a successful setup/yield lifecycle. An exception during setup could therefore leave installed stubs active in the pytest process.

Round 6 encloses the entire setup after `MonkeyPatch()` creation in `try/except BaseException`; on any setup failure it executes `mp.undo()` and re-raises. The normal post-yield `mp.undo()` remains. This closes the disclosed setup-failure leak without changing the successful fixture path.

The packet's temporary forced-failure cleanup probe is supporting evidence reported by L1, not a committed regression test. The source structure itself is sufficient for this changed-source review to establish that the cleanup path now exists and is fail-safe for setup exceptions.

## 5. New regression test

`test_r6_declared_paths_are_platform_independent` materially exercises the repaired invariant on a non-Windows host:

- the current frozen identity must verify;
- the declaration representation must contain no backslash;
- each of the five declared path constants must be slash-based;
- replacing each constant with a backslashed form must cause M7 identity verification to refuse;
- reconstruction of the old Windows-style `governance_root` must produce a declaration digest different from the v6 literal.

This is a discriminating regression for the specific source-level failure class that escaped the Linux-only Round-5 suite. It does not substitute for the canonical Windows suite, and L1 states that limitation correctly.

## 6. Test evidence and evidentiary boundary

L1 reports **28 M7 tests passing** on the final Round-6 bytes, split across six groups: 18 in group A, 2 in B1, 3 in B2, 3 in B3, 1 in B4, and 1 in B5. The supplied test source is coherent with the added twenty-eighth test and with the repaired fixture.

I did not independently execute the multi-minute B1-B5 suite or a Windows canonical suite in this review. Therefore those execution counts remain L1's execution evidence. My independent findings here are the packet/source identities, the direct Round-5-to-Round-6 changed-source comparison, and the source-level adequacy of the repair.

The decisive remaining platform proof is exactly what the packet states: after this clearance, the repaired bytes must pass the canonical suite on Mike's Windows machine. A future Windows failure would be new evidence and would reopen placement; this source clearance does not pre-judge that run.

## 7. Regression against Round-5 clearance

I find no Round-6 change that reopens a Round-5 hold. The previously cleared Round-5 governance/specification join, true completion semantics, full router replay, exact benchmark manifest, tolerance-program closure, committed-file requirements, wording corrections, test families, and the two accepted content-addressed memos are untouched except insofar as repo-relative committed-path construction is made platform-independent.

The real-repository default-deny/noncanonical state remains an intended pre-governance condition, not an M7 defect.

## 8. Disposition

**FINAL VERDICT: SOUND**

**Placement disposition: PLACEABLE FOR THE REPAIRED WINDOWS PLACEMENT ATTEMPT.**

For packet SHA-256 `3b8d496be069edc82b6fba956e3d771a1247ae235942c9ac4450171deb8edda6`, I clear the following exact source identities:

- `e1/runner.py` — `f33fbb54c115225cb290db6f689b973bb0b30d81c4e1fab215d4fb2a9c22c769`
- `tests/test_e1_m7.py` — `23bd6e69a0ab37d0316e8e8407dc9c9e5211ef7849054959221b272c35030785`

The 41-line runner change is verified against my cleared Round-5 runner. The Windows declaration/path defect is repaired coherently; the setup-failure monkeypatch leak is closed; the new regression test is appropriately discriminating; and I find no new source-level defect requiring a hold.

This clearance authorizes no governance ratification, Package Specification approval, production authorization, or scientific execution. It clears these exact Round-6 M7 bytes for placement and the required canonical Windows suite. Placement remains contingent on that suite passing on the placed identities.

— **L2**
