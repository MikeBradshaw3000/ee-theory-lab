"""
regenerate_manifest.py

Canonical manifest-regeneration script for Phase 4B.

Produces phase_4b/manifests/parquet_manifest.csv by inspecting Flight 6
production parquet files at the configured source data root. Schema and
field semantics specified in phase_4b/manifests/parquet_manifest.md.

This is the Stage 3 schema-specification scaffolding (per Mike's Q2b
arbitration: schema specification only at Stage 3; manifest population
deferred to Layer 3 routing). The scaffolding establishes the module
structure, the verification-vs-generation separation (per Mike's
arbitration C: verification logic in a separate module at
phase_4b/scripts/_manifest_verification.py), and the operational
contract for the regeneration flow.

Per Rule 7 (no inference-based repair of missing required telemetry):
the script does not silently repair missing or malformed parquet
outputs. It produces manifest rows with `fail` status and explicit
`verification_notes`. Diagnosis happens at the substrate level, not
by manifest editing.

THREE DISTINGUISHABLE OPERATIONS (per Layer 2 sanity scan clarification):
1. Manifest regeneration — computes per-file fields including `sha256`
   (the file's identity hash). Runs whenever parquet outputs change.
   This script implements this operation.
2. Substrate verification — applies FSS §14.1 checks via
   _manifest_verification.py. Populates verification_status,
   verification_notes, and the §14.1 payload fields. Runs as part of
   manifest regeneration (invoked from regenerate_manifest()).
3. Byte-identity verification — compares SHA-256 hashes across files in
   a shadow_copy_group to upgrade shadow_copy_status from
   presumed_shadow_copy to verified_shadow_copy. Separate from manifest
   regeneration. Updates the verification-record store at
   phase_4b/manifests/byte_identity_verifications.csv; subsequent
   manifest regeneration consults the store. Runs at session-level
   discretion (not at every manifest regeneration).

The `sha256` field is populated at every manifest regeneration
(operation 1). Byte-identity verification (operation 3) uses those
hashes but is not the same operation as computing them.

Usage:
    python phase_4b/scripts/regenerate_manifest.py

Outputs:
    phase_4b/manifests/parquet_manifest.csv (overwrites existing)
    Console summary: total rows, status distribution, verification
    counts, whether the manifest changed since last regeneration.

Status (2026-05-20, session 13 Stage 3): SCAFFOLDING ONLY. Layer 3
routing will implement the substantive logic in each function below.
The scaffolding establishes the contract that Layer 3's implementation
must honor.
"""

from __future__ import annotations

# Standard library imports
# Layer 3 implementation note: the type annotations below use `os.PathLike`
# in string form (safe under `from __future__ import annotations`). When
# Layer 3 fills in the implementation, import os explicitly or switch the
# type hints to `pathlib.Path | str` to avoid forward-reference fragility
# in case `from __future__ import annotations` is later removed.
# (To be filled in by Layer 3: csv, datetime, hashlib, os, pathlib, subprocess, sys, typing)

# Project imports
# (To be filled in by Layer 3: from phase_4b.scripts._manifest_verification import (
#      verify_required_columns, verify_realization_invariant,
#      verify_clipping_summary, verify_tick_range, ...))


# =============================================================================
# Configuration
# =============================================================================

MANIFEST_SCHEMA_VERSION = "1.0"

SOURCE_DATA_ROOT_DEFAULT = r"C:\Users\vkz244\EE_Theory_Lab\flight2_outputs"

MANIFEST_OUTPUT_PATH_DEFAULT = "phase_4b/manifests/parquet_manifest.csv"

VERIFICATION_RECORD_PATH_DEFAULT = "phase_4b/manifests/byte_identity_verifications.csv"
# The verification-record store for SHA-256 byte-identity checks. Separate
# from the manifest itself per arbitration B. Format and semantics specified
# in a follow-up document; for Stage 3 scaffolding, the path is reserved
# and the load_verification_records() function below declares the contract.


# Canonical schema field order. Must match parquet_manifest.md and CSV header.
SCHEMA_FIELDS = [
    # Identity & structure
    "logical_artifact_id",
    "physical_file_path",
    "artifact_role",
    "scale",
    "F_variant",
    "probe_name",
    "shadow_copy_group",
    "byte_identical_to",
    "shadow_copy_status",
    "byte_identity_verification_method",
    "byte_identity_verified_at",
    "byte_identity_verified_by",
    # FSS §14.1 verification payload
    "file_exists",
    "file_size_bytes",
    "sha256",
    "row_count",
    "column_count",
    "required_columns_present",
    "missing_required_columns",
    "tick_min",
    "tick_max",
    "tick_count",
    "unique_cells",
    "expected_cells",
    "non_empty",
    "realization_invariant_satisfied",
    "clipping_summary",
    "verification_status",
    "verification_notes",
    # Provenance
    "manifest_schema_version",
    "manifest_generated_at",
    "manifest_generated_by_script",
    "source_data_root",
    "git_head_at_generation",
]


SHADOW_COPY_STATUS_VALUES = {
    "genuine",
    "verified_shadow_copy",
    "presumed_shadow_copy",
    "not_applicable",
}

BYTE_IDENTITY_VERIFICATION_METHOD_VALUES = {
    "sha256_match",
    "file_size_and_spec_only",
    "not_checked",
    "not_applicable",
}
# Note: `sha256_match` is a compact method/result enum value. It reads as
# "method: SHA-256 hash comparison; result: match." See parquet_manifest.md
# for the design rationale (binary verification outcome paired with method
# in a single enum value rather than split into separate fields).

VERIFICATION_STATUS_VALUES = {
    "pass",
    "fail",
    "warning",
    "not_checked",
}


# =============================================================================
# Manifest generation contract
# =============================================================================

def regenerate_manifest(
    source_data_root: "str | os.PathLike" = SOURCE_DATA_ROOT_DEFAULT,
    output_path: "str | os.PathLike" = MANIFEST_OUTPUT_PATH_DEFAULT,
    verification_records_path: "str | os.PathLike" = VERIFICATION_RECORD_PATH_DEFAULT,
) -> dict:
    """
    Regenerate the parquet manifest CSV.

    Contract:
    1. Discover all parquet files under source_data_root.
    2. For each parquet file, compute identity & structure fields from
       the filename and from FSS §13.2 specification structure.
    3. Compute the per-file `sha256` hash. This is operation (1) per the
       module docstring — the file's identity hash, populated at every
       regeneration. Distinct from operation (3) byte-identity
       verification, which compares hashes across files in a
       shadow_copy_group.
    4. Load byte-identity verification records from
       verification_records_path; merge into shadow_copy_status and
       byte_identity_verification_method fields. If the verification-
       record store is absent, all shadow_copy_status values default to
       presumed_shadow_copy or not_applicable per FSS §13.2 spec.
    5. For each parquet file, invoke phase_4b/scripts/_manifest_verification.py
       to compute the FSS §14.1 verification payload (file size, row count,
       required columns, tick range, realization invariant, clipping
       summary, etc.). This is operation (2) per the module docstring.
    6. Set verification_status per the verification payload; populate
       verification_notes with specific reasons for fail/warning.
    7. Compute provenance fields (manifest_schema_version,
       manifest_generated_at, manifest_generated_by_script,
       source_data_root, git_head_at_generation).
    8. Sort rows by (scale, F_variant, probe_name, physical_file_path)
       for deterministic ordering.
    9. Write CSV to output_path; overwrite atomically.
    10. Return summary dict: total_rows, status_counts, verification_counts,
        changed_since_last (computed by diff against existing CSV if present).

    Per Rule 7: do not repair. If a parquet file is missing, malformed, or
    fails verification, the row records the failure with explicit
    verification_notes. Diagnosis is downstream; the manifest is honest
    about current state.

    Per arbitration B and operation (3) separation: SHA-256 byte-identity
    verification (comparing hashes across shadow_copy_group members to
    upgrade `presumed` to `verified`) does not run at every regeneration.
    The verification-record store is consulted; if a verification record
    exists for a file, the shadow_copy_status reflects it
    (verified_shadow_copy or genuine); if no record exists, the status is
    presumed_shadow_copy or not_applicable per FSS §13.2 structural
    expectation. Note that this is separate from operation (1)'s per-file
    `sha256` computation, which always runs.

    Layer 3 implements this function; Stage 3 scaffolding establishes the
    contract.
    """
    raise NotImplementedError(
        "Stage 3 scaffolding only. Layer 3 routing implements regenerate_manifest()."
    )


def load_verification_records(
    verification_records_path: "str | os.PathLike",
) -> dict:
    """
    Load the byte-identity verification record store.

    Contract:
    Returns a dict keyed by physical_file_path. Each value is a dict with
    keys: shadow_copy_status, byte_identity_verification_method,
    byte_identity_verified_at, byte_identity_verified_by, sha256.

    If the verification-record store does not exist (first run, never
    verified), returns an empty dict. The manifest regeneration then
    populates shadow_copy_status as presumed_shadow_copy or not_applicable
    based on FSS §13.2 structural expectation.

    The verification-record store format is the same CSV header subset
    as the manifest's byte-identity fields plus physical_file_path as
    the key. Updates to the store happen via a separate verify-byte-
    identity operation — operation (3) per the module docstring — which
    is not implemented in Stage 3 scaffolding and is queued for a future
    session.

    Layer 3 implements this function.
    """
    raise NotImplementedError(
        "Stage 3 scaffolding only. Layer 3 routing implements load_verification_records()."
    )


def get_git_head() -> str:
    """
    Return the current git HEAD SHA, or 'not_available' if not in a git
    working tree or git is not on PATH.

    Per arbitration B and per the manifest schema documentation:
    git_head_at_generation should not block manifest generation. If git
    metadata cannot be read, record 'not_available' rather than failing
    the whole manifest.

    Layer 3 implements this function.
    """
    raise NotImplementedError(
        "Stage 3 scaffolding only. Layer 3 routing implements get_git_head()."
    )


def diff_against_existing_manifest(
    new_rows: list,
    existing_csv_path: "str | os.PathLike",
) -> dict:
    """
    Compare the newly-generated manifest rows against the existing CSV at
    existing_csv_path. Return summary: changed_field_count, changed_row_count,
    new_rows_added, rows_removed.

    Used to populate the changed_since_last value in the regeneration summary.
    Layer 3 implements this function.
    """
    raise NotImplementedError(
        "Stage 3 scaffolding only. Layer 3 routing implements diff_against_existing_manifest()."
    )


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    # Layer 3 will implement:
    # - argparse for source_data_root, output_path overrides
    # - call regenerate_manifest()
    # - print summary to stdout (for operations-log paste-back)
    # - non-zero exit code if any rows have verification_status == fail
    raise NotImplementedError(
        "Stage 3 scaffolding only. Layer 3 routing implements the script entry point."
    )
