"""
Item 12(3) Substrate Schema/Load Adapter.
Provides uniform ingestion, validation, and metadata injection for Phase 4B parquet files.

Provenance note (session 25):
  Layer 1 applied a mechanical node-review correction after Layer 2 consultation:
  the parsed base token was renamed from `probe_name` to `probe_base_name` to avoid
  collision with the canonical manifest `probe_name` vocabulary (which uses full forms
  such as `probe1_overcrowding`, `probe2_starvation_F2sym`). Original design and
  implementation by Layer 3 (Gemini), iteration 3.
"""

import sys
import re
import warnings
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq

# --- ENUMS & CONSTANTS ---
EXPECTED_PROBES = ['overcrowding', 'starvation', 'fusion_residual']
EXPECTED_F_FORMS = ['FLR', 'F2sym']
EXPECTED_SCALES = ['20x20', '40x40']

SCALE_METADATA_MAP = {'20x20': '20', '40x40': '40'}

# Section G Primary Source (25 columns, exact casing, file order)
EXPECTED_RAW_COLUMNS = [
    "Tick", "Agent_X", "Agent_Y", "b_i_v", "b_i_u", "b_i_r", "limiting_base_argmin",
    "Lambda_multiplicative", "Lambda_additive", "Lambda_total", "Local_Density",
    "Drive_Raw", "Term_Density_Pos", "Term_Overcrowding", "Term_Offset", "p_base",
    "p_act", "PRNG_draw", "is_active", "Psi_local", "gamma_coef", "Delta_v", "Delta_u",
    "Delta_r", "Term_Lambda"
]

INJECTED_COLUMNS = [
    "F_variant", "scale", "meta_PRNG_seed", "meta_Substrate_version",
    "meta_Execution_timestamp", "meta_Total_ticks", "probe_base_name",
    "F_form_token", "surrogate_run_id", "source_filename", "expected_shadow_copy"
]

# --- ENVIRONMENT GUARD ---
def _verify_environment():
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("Environment Guard Failed: Virtual environment not active.")
    if sys.version_info[:2] != (3, 14):
        raise RuntimeError(f"Environment Guard Failed: Expected Python 3.14.x, got {sys.version.split()[0]}")

# --- PARSERS & DECODERS ---
def _decode_meta(value):
    """Safely decodes pyarrow metadata (bytes -> str fallback)."""
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return str(value)

def _parse_filename(filename: str):
    """
    Right-to-left anchored filename parser.
    Fails fast on malformed names. Does not rely on simple '_' splitting.

    Returns the probe BASE token (probe_base_name), not the canonical manifest
    full form. See load_substrate_file docstring for the vocabulary distinction.
    """
    if not filename.endswith('.parquet'):
        raise ValueError(f"Filename parsing failed: '{filename}' does not end with .parquet")

    stem = filename[:-8]  # remove .parquet

    # 1. Parse Scale (Rightmost)
    scale = None
    for s in EXPECTED_SCALES:
        if stem.endswith(f"_{s}"):
            scale = s
            stem = stem[:-len(f"_{s}")]
            break
    if not scale:
        raise ValueError(f"Filename parsing failed: Scale not found/invalid in '{filename}'")

    # 2. Parse F_form (Optional, next rightmost)
    f_form = None
    for f in EXPECTED_F_FORMS:
        if stem.endswith(f"_{f}"):
            f_form = f
            stem = stem[:-len(f"_{f}")]
            break

    # 3. Parse probe base name (Leftover after standard prefix)
    match = re.match(r'^flight6_probe\d+_(.+)$', stem)
    if not match:
        raise ValueError(f"Filename parsing failed: Missing prefix or probe in '{filename}'")

    probe_base_name = match.group(1)
    if probe_base_name not in EXPECTED_PROBES:
        raise ValueError(f"Filename parsing failed: Unknown probe '{probe_base_name}'")

    return probe_base_name, f_form, scale

# --- CORE ADAPTER ---
def load_substrate_file(filepath: Path) -> pd.DataFrame:
    """
    Loads a single Phase 4B parquet file, validates schema and names, and injects logical columns.

    Docstring Constraints:
    - meta_* fields: Constant per loaded file. For audit/provenance only, NOT row-varying analytical variables.
    - surrogate_run_id: Presumes N=1 matched-seed substrate; must be re-evaluated if repeat-seed runs are
      introduced. ADDITIONAL WARNING (session 25): surrogate_run_id is derived from filepath.stem and is
      therefore IDENTICAL across same-named byte-identical copies living in different directories (e.g. the
      four tree-wide probe1_overcrowding copies). It does NOT uniquely key shadow copies. A future repeat-seed
      or multi-directory consumer must not trust surrogate_run_id as a unique key; use source_filename plus the
      handed-in directory if copy-level identity is needed.
    - source_filename: Records the file as handed in by the caller. Does NOT assert this is the canonical copy.
      (The which-copy-is-canonical question is item 12(2), out of adapter scope by construction.)
    - probe_base_name: The parsed BASE probe token (overcrowding / starvation / fusion_residual). This is NOT
      the canonical manifest `probe_name` vocabulary, which uses full forms (probe1_overcrowding,
      probe2_starvation_F2sym, probe2_starvation_FLR, probe3_fusion_residual). Do NOT join adapter output to the
      manifest on this field. If a future consumer needs a direct manifest join, add an explicit separate field
      (e.g. `manifest_probe_name` / `probe_name_full`) rather than reconstructing or overloading this one.
    - expected_shadow_copy: HARD CONSTRAINT. This is a naming-derived expectation only. It is NOT a byte-identity
      claim and asserts nothing about verified shadow-copy status for any file.
    """
    # Check 1: Environment
    _verify_environment()

    # Check 2: File presence
    if not filepath.exists():
        raise FileNotFoundError(f"Substrate file not found: {filepath}")

    # Check 3: Enum-anchored name validity
    probe_base_name, f_form_token, filename_scale = _parse_filename(filepath.name)

    # Check 4: Metadata readability
    pf = pq.ParquetFile(filepath)
    raw_meta = pf.metadata.metadata or {}

    if b'F_variant' not in raw_meta or b'Scale' not in raw_meta:
        raise ValueError(f"Metadata read failed: b'F_variant' or b'Scale' missing in {filepath.name}")

    decoded_meta = {k.decode('utf-8') if isinstance(k, bytes) else str(k): _decode_meta(v)
                    for k, v in raw_meta.items()}

    # Check 5: Scale consistency via normalization
    normalized_filename_scale = SCALE_METADATA_MAP[filename_scale]
    if normalized_filename_scale != decoded_meta['Scale']:
        raise ValueError(
            f"Scale mismatch: Filename implies {normalized_filename_scale}, "
            f"but metadata Scale is {decoded_meta['Scale']}"
        )

    # --- Read Table ---
    df = pd.read_parquet(filepath)

    # Check 6: Raw-column exact set match (order documented, not gated)
    raw_cols = set(df.columns)
    expected_cols = set(EXPECTED_RAW_COLUMNS)

    if raw_cols != expected_cols:
        missing = expected_cols - raw_cols
        extra = raw_cols - expected_cols
        raise ValueError(f"Schema mismatch in {filepath.name}. Missing: {missing}. Extra: {extra}")

    if list(df.columns) != EXPECTED_RAW_COLUMNS:
        warnings.warn(f"Column order drift detected in {filepath.name}. Set matches, but order differs from Section G.")

    # Check 7: Derived-column collision guard
    collision = set(INJECTED_COLUMNS).intersection(raw_cols)
    if collision:
        raise ValueError(f"Collision Guard Failed: Target injected columns {collision} already exist in raw data.")

    # --- Data Flow: Injection & Broadcast ---

    # Filename-derived
    df['source_filename'] = filepath.name
    df['probe_base_name'] = probe_base_name
    df['F_form_token'] = f_form_token
    df['surrogate_run_id'] = filepath.stem

    # Metadata-derived
    df['F_variant'] = decoded_meta['F_variant']
    df['scale'] = filename_scale  # e.g., '20x20'
    df['meta_PRNG_seed'] = decoded_meta.get('PRNG_seed', 'UNKNOWN')
    df['meta_Substrate_version'] = decoded_meta.get('Substrate_version', 'UNKNOWN')
    df['meta_Execution_timestamp'] = decoded_meta.get('Execution_timestamp', 'UNKNOWN')
    df['meta_Total_ticks'] = decoded_meta.get('Total_ticks', 'UNKNOWN')

    # Logic-derived (naming-derived expectation ONLY; not a byte-identity claim)
    is_f2 = df['F_variant'] == 'F_2_symmetric'
    is_shadow_probe = df['probe_base_name'].isin(['starvation', 'fusion_residual'])
    df['expected_shadow_copy'] = is_f2 & is_shadow_probe

    return df

# --- EXTENSION INTERFACE ---
def extend_for_item13(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extension point for future consumers (e.g., Phase 4B Item 13 spatial diagnostics).
    Future implementations can attach specific validity masks or computed fields here.
    """
    # Example placeholder: df['is_valid_probe_data'] = ...
    return df

if __name__ == "__main__":
    print("Item 12(3) Substrate Adapter instantiated. Available for import.")