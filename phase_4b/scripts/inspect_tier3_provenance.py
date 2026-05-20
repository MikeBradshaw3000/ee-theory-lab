"""
Tier 3 data-provenance inspection script.

Inspects all candidate parquet files matching the four canonical filenames named in
reg_01_scale_interactions.yaml. For each candidate, prints metadata and structural
fields, then flags pass/fail against expected v1.1 Flight 2 production values.

Does NOT pick a canonical file automatically. Output is for human review.

Per Phase 4B specification v1.1 and Flight 6 Substrate Specification v1.1.
"""
import pyarrow.parquet as pq
from pathlib import Path
import sys

WORKSPACE_ROOT = Path(r"C:\Users\vkz244\EE_Theory_Lab")

CANONICAL_FILENAMES = [
    "flight6_probe1_overcrowding_20x20.parquet",
    "flight6_probe1_overcrowding_40x40.parquet",
    "flight6_probe2_starvation_FLR_20x20.parquet",
    "flight6_probe2_starvation_FLR_40x40.parquet",
]

EXPECTED_PRNG_SEED = "128561948"
EXPECTED_SUBSTRATE_VERSION = "v1.1"
EXPECTED_TOTAL_TICKS = "3000"
EXPECTED_COLUMN_COUNT = 25

REQUIRED_COLUMNS = {
    "Tick", "Agent_X", "Agent_Y", "b_i_v", "b_i_u", "b_i_r",
    "limiting_base_argmin", "Lambda_multiplicative", "Lambda_additive", "Lambda_total",
    "Local_Density", "Drive_Raw", "Term_Density_Pos", "Term_Overcrowding", "Term_Offset",
    "p_base", "p_act", "PRNG_draw", "is_active", "Psi_local",
    "gamma_coef", "Delta_v", "Delta_u", "Delta_r", "Term_Lambda",
}


def expected_rows_for_filename(filename):
    """Return expected row count given the canonical filename."""
    if "20x20" in filename:
        return 1_200_000
    elif "40x40" in filename:
        return 4_800_000
    return None


def expected_unique_cells_for_filename(filename):
    """Return expected unique cell count given the canonical filename."""
    if "20x20" in filename:
        return 400
    elif "40x40" in filename:
        return 1600
    return None


def expected_f_variant_for_filename(filename):
    """Return expected F_variant given the canonical filename."""
    if "probe1_overcrowding" in filename or "F2sym" in filename or "fusion_residual" in filename:
        return "F_2_symmetric"
    elif "starvation_FLR" in filename:
        return "F_LR"
    return None


def expected_scale_for_filename(filename):
    """Return expected scale (numeric) given the canonical filename."""
    if "20x20" in filename:
        return "20"
    elif "40x40" in filename:
        return "40"
    return None


def find_candidates(filename):
    """Return all paths to files matching the given filename across the workspace."""
    return sorted(WORKSPACE_ROOT.rglob(filename))


def decode_metadata(metadata):
    """Decode parquet custom metadata bytes to a string dict."""
    if metadata is None:
        return {}
    decoded = {}
    for k, v in metadata.items():
        try:
            key = k.decode("utf-8") if isinstance(k, bytes) else str(k)
            val = v.decode("utf-8") if isinstance(v, bytes) else str(v)
            decoded[key] = val
        except Exception as e:
            decoded[str(k)] = f"<decode error: {e}>"
    return decoded


def inspect_file(path, canonical_filename):
    """Inspect a single parquet file. Return a dict of findings."""
    result = {
        "path": str(path),
        "file_size_bytes": path.stat().st_size,
        "modification_time": path.stat().st_mtime,
        "errors": [],
        "checks": {},
    }
    try:
        pf = pq.ParquetFile(path)
        meta = pf.metadata
        schema_meta = pf.schema_arrow.metadata
    except Exception as e:
        result["errors"].append(f"Failed to open parquet: {e}")
        return result

    # Row count
    actual_rows = meta.num_rows
    expected_rows = expected_rows_for_filename(canonical_filename)
    result["row_count"] = actual_rows
    result["expected_row_count"] = expected_rows
    result["checks"]["row_count"] = (actual_rows == expected_rows)

    # Column count
    actual_cols = meta.num_columns
    result["column_count"] = actual_cols
    result["expected_column_count"] = EXPECTED_COLUMN_COUNT
    result["checks"]["column_count"] = (actual_cols == EXPECTED_COLUMN_COUNT)

    # Column names
    actual_col_names = set(meta.schema.names)
    missing = REQUIRED_COLUMNS - actual_col_names
    extra = actual_col_names - REQUIRED_COLUMNS
    result["columns_missing"] = sorted(missing)
    result["columns_extra"] = sorted(extra)
    result["checks"]["required_columns_present"] = (len(missing) == 0)

    # Custom metadata
    custom_meta = decode_metadata(schema_meta)
    result["custom_metadata"] = custom_meta

    # F_variant
    expected_fv = expected_f_variant_for_filename(canonical_filename)
    actual_fv = custom_meta.get("F_variant", "<missing>")
    result["expected_f_variant"] = expected_fv
    result["actual_f_variant"] = actual_fv
    result["checks"]["f_variant"] = (actual_fv == expected_fv)

    # Scale
    expected_scale = expected_scale_for_filename(canonical_filename)
    actual_scale = custom_meta.get("Scale", "<missing>")
    result["expected_scale"] = expected_scale
    result["actual_scale"] = actual_scale
    result["checks"]["scale"] = (actual_scale == expected_scale)

    # PRNG_seed
    actual_seed = custom_meta.get("PRNG_seed", "<missing>")
    result["expected_prng_seed"] = EXPECTED_PRNG_SEED
    result["actual_prng_seed"] = actual_seed
    result["checks"]["prng_seed"] = (actual_seed == EXPECTED_PRNG_SEED)

    # Substrate_version
    actual_substrate = custom_meta.get("Substrate_version", "<missing>")
    result["expected_substrate_version"] = EXPECTED_SUBSTRATE_VERSION
    result["actual_substrate_version"] = actual_substrate
    result["checks"]["substrate_version"] = (actual_substrate == EXPECTED_SUBSTRATE_VERSION)

    # Total_ticks
    actual_ticks = custom_meta.get("Total_ticks", "<missing>")
    result["expected_total_ticks"] = EXPECTED_TOTAL_TICKS
    result["actual_total_ticks"] = actual_ticks
    result["checks"]["total_ticks"] = (actual_ticks == EXPECTED_TOTAL_TICKS)

    # Execution_timestamp (informational, not check)
    result["execution_timestamp"] = custom_meta.get("Execution_timestamp", "<missing>")

    # Tick range and unique cells via single sweep
    try:
        tick_col_batches = pf.iter_batches(batch_size=200000, columns=["Tick", "Agent_X", "Agent_Y"])
        tick_min, tick_max = None, None
        unique_cells = set()
        for batch in tick_col_batches:
            df = batch.to_pandas()
            t_min = df["Tick"].min()
            t_max = df["Tick"].max()
            tick_min = t_min if tick_min is None else min(tick_min, t_min)
            tick_max = t_max if tick_max is None else max(tick_max, t_max)
            for x, y in zip(df["Agent_X"].values, df["Agent_Y"].values):
                unique_cells.add((int(x), int(y)))
        result["tick_min"] = int(tick_min) if tick_min is not None else None
        result["tick_max"] = int(tick_max) if tick_max is not None else None
        result["unique_cell_count"] = len(unique_cells)
        expected_cells = expected_unique_cells_for_filename(canonical_filename)
        result["expected_unique_cell_count"] = expected_cells
        result["checks"]["tick_range"] = (tick_min == 0 and tick_max == 2999)
        result["checks"]["unique_cells"] = (len(unique_cells) == expected_cells)
    except Exception as e:
        result["errors"].append(f"Failed to compute tick/cell stats: {e}")

    # Overall pass: all individual checks must pass and no errors
    result["all_checks_pass"] = (
        len(result["errors"]) == 0 and all(result["checks"].values())
    )

    return result


def print_inspection(result, canonical_filename, candidate_index):
    """Print a structured human-readable inspection report for one file."""
    print()
    print("=" * 90)
    print(f"Candidate #{candidate_index} for {canonical_filename}")
    print("=" * 90)
    print(f"Path: {result['path']}")
    print(f"File size: {result['file_size_bytes']:,} bytes")
    print(f"Modification timestamp (epoch): {result['modification_time']}")

    if result["errors"]:
        print()
        print("ERRORS:")
        for e in result["errors"]:
            print(f"  - {e}")
        print()
        print("OVERALL: FAIL (errors during inspection)")
        return

    print()
    print(f"Row count:    {result['row_count']:,}  (expected {result['expected_row_count']:,})  ->  {'PASS' if result['checks']['row_count'] else 'FAIL'}")
    print(f"Column count: {result['column_count']}  (expected {result['expected_column_count']})  ->  {'PASS' if result['checks']['column_count'] else 'FAIL'}")
    print(f"Required columns present: {'PASS' if result['checks']['required_columns_present'] else 'FAIL'}")
    if result["columns_missing"]:
        print(f"  MISSING: {result['columns_missing']}")
    if result["columns_extra"]:
        print(f"  EXTRA:   {result['columns_extra']}")

    print()
    print("Custom metadata:")
    for k, v in result["custom_metadata"].items():
        print(f"  {k}: {v}")

    print()
    print(f"F_variant:         actual={result['actual_f_variant']!r:25}  expected={result['expected_f_variant']!r}  ->  {'PASS' if result['checks']['f_variant'] else 'FAIL'}")
    print(f"Scale:             actual={result['actual_scale']!r:25}  expected={result['expected_scale']!r}  ->  {'PASS' if result['checks']['scale'] else 'FAIL'}")
    print(f"PRNG_seed:         actual={result['actual_prng_seed']!r:25}  expected={result['expected_prng_seed']!r}  ->  {'PASS' if result['checks']['prng_seed'] else 'FAIL'}")
    print(f"Substrate_version: actual={result['actual_substrate_version']!r:25}  expected={result['expected_substrate_version']!r}  ->  {'PASS' if result['checks']['substrate_version'] else 'FAIL'}")
    print(f"Total_ticks:       actual={result['actual_total_ticks']!r:25}  expected={result['expected_total_ticks']!r}  ->  {'PASS' if result['checks']['total_ticks'] else 'FAIL'}")
    print(f"Execution_timestamp: {result['execution_timestamp']}")

    if "tick_min" in result:
        print()
        print(f"Tick range:        {result['tick_min']} to {result['tick_max']}  (expected 0 to 2999)  ->  {'PASS' if result['checks']['tick_range'] else 'FAIL'}")
        print(f"Unique cell count: {result['unique_cell_count']}  (expected {result['expected_unique_cell_count']})  ->  {'PASS' if result['checks']['unique_cells'] else 'FAIL'}")

    print()
    print(f"OVERALL: {'PASS' if result['all_checks_pass'] else 'FAIL'}")


def main():
    eligible_by_filename = {}

    for canonical_filename in CANONICAL_FILENAMES:
        print()
        print("#" * 90)
        print(f"#  {canonical_filename}")
        print("#" * 90)

        candidates = find_candidates(canonical_filename)
        if not candidates:
            print(f"\nNo candidates found for {canonical_filename}.\n")
            eligible_by_filename[canonical_filename] = []
            continue

        eligible = []
        for i, path in enumerate(candidates, start=1):
            result = inspect_file(path, canonical_filename)
            print_inspection(result, canonical_filename, i)
            if result["all_checks_pass"]:
                eligible.append(result["path"])

        eligible_by_filename[canonical_filename] = eligible
        print()
        print(f"-- {len(eligible)} of {len(candidates)} candidates passed all checks for {canonical_filename} --")

    # Summary
    print()
    print()
    print("=" * 90)
    print("SUMMARY")
    print("=" * 90)
    for canonical_filename, eligible in eligible_by_filename.items():
        print()
        print(f"{canonical_filename}:")
        if not eligible:
            print("  NO ELIGIBLE CANDIDATES.")
        elif len(eligible) == 1:
            print(f"  Unique canonical: {eligible[0]}")
        else:
            print(f"  MULTIPLE ELIGIBLE — PAUSE FOR ARBITRATION:")
            for p in eligible:
                print(f"    - {p}")

    print()
    print("=" * 90)
    print("Decisive rule: A candidate is eligible only if it passes ALL checks.")
    print("If more than one candidate is eligible for the same logical artifact,")
    print("pause for provenance arbitration before Tier 3 execution.")
    print("=" * 90)


if __name__ == "__main__":
    main()
