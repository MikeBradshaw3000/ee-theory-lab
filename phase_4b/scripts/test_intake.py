import copy
import os
import pandas as pd
from pathlib import Path
from _phase_4b_intake import (
    normalize_prereg, load_canonical_inputs, promote_metadata_to_columns, 
    construct_derived_variables, validate_formula_variables,
    PreregSchemaError, CanonicalInputError, MetadataPromotionError, 
    DerivedVariableError, FormulaVariableError, MetadataRecord
)
from _phase_4b_common import get_paths

print("=== EXECUTING §4.3 TEST SUITE ===")

BASE_SPEC = {
    "prereg_id": "test_suite", "prereg_version": "1.0", "model_family": "ols",
    "formula_role": "authoritative", "formula": "y ~ x",
    "canonical_input_filenames": [], "tier2_globals_path": "",
    "outcome": {"name": "y", "construction": "eta_floor_inversion_of_p_base", "eta": 0.01},
    "predictors": ["x"], "interactions": [], "excluded_variables": [],
    "uncertainty_method": {"primary": "cluster_robust", "cluster_variable": "run_x_tick", "sensitivity": []},
    "interpretation_boundary": {"licenses": "", "does_not_adjudicate": ""}
}

# 1a. PreregSchemaError: outcome-as-bare-string
spec1a = copy.deepcopy(BASE_SPEC)
spec1a["outcome"] = "y"
try:
    normalize_prereg(spec1a)
    print("[FAIL] 1a: PreregSchemaError (outcome-as-bare-string) not raised")
except PreregSchemaError as e:
    print(f"[PASS] 1a: Caught {type(e).__name__} - {e}")

# 1b. PreregSchemaError: formula-references-undeclared-variable
spec1b = copy.deepcopy(BASE_SPEC)
spec1b["formula"] = "y ~ z"
try:
    normalize_prereg(spec1b)
    print("[FAIL] 1b: PreregSchemaError (undeclared variable) not raised")
except PreregSchemaError as e:
    print(f"[PASS] 1b: Caught {type(e).__name__} - {e}")

# 1c. PreregSchemaError: excluded-variable-in-predictors
spec1c = copy.deepcopy(BASE_SPEC)
spec1c["excluded_variables"] = ["x"]
try:
    normalize_prereg(spec1c)
    print("[FAIL] 1c: PreregSchemaError (excluded in predictors) not raised")
except PreregSchemaError as e:
    print(f"[PASS] 1c: Caught {type(e).__name__} - {e}")

# 2a. CanonicalInputError: Missing Input File
spec2a = copy.deepcopy(BASE_SPEC)
spec2a["canonical_input_filenames"] = ["does_not_exist.parquet"]
try:
    norm2a = normalize_prereg(spec2a)
    load_canonical_inputs(norm2a)
    print("[FAIL] 2a: CanonicalInputError (missing file) not raised")
except CanonicalInputError as e:
    print(f"[PASS] 2a: Caught {type(e).__name__} - {e}")

# 2b. CanonicalInputError: Missing Metadata
_, flight2_pq_dir, _ = get_paths()
dummy_file_name = "missing_meta_test.parquet"
dummy_file_path = flight2_pq_dir / dummy_file_name
pd.DataFrame({'run_id': ['test_run'], 'tick': [1]}).to_parquet(dummy_file_path)

spec2b = copy.deepcopy(BASE_SPEC)
spec2b["canonical_input_filenames"] = [dummy_file_name]
try:
    norm2b = normalize_prereg(spec2b)
    load_canonical_inputs(norm2b)
    print("[FAIL] 2b: CanonicalInputError (missing metadata) not raised")
except CanonicalInputError as e:
    print(f"[PASS] 2b: Caught {type(e).__name__} - {e}")
finally:
    if dummy_file_path.exists():
        dummy_file_path.unlink()

# Prepare a valid normalized spec for remaining downstream tests
norm_base = normalize_prereg(BASE_SPEC)

# 3. MetadataPromotionError: DataFrame row without matching MetadataRecord
fake_metadata = [MetadataRecord(
    file_path=Path("fake.parquet"), run_id="known_run", source_file="fake.parquet",
    f_variant="F_LR", scale="20x20", prng_seed=0, substrate_version="v1.1",
    total_ticks=100, execution_timestamp="2026-01-01", row_count=1
)]
df_meta = pd.DataFrame({"run_id": ["unmatched_run"]})
try:
    promote_metadata_to_columns(df_meta, fake_metadata)
    print("[FAIL] 3: MetadataPromotionError not raised")
except MetadataPromotionError as e:
    print(f"[PASS] 3: Caught {type(e).__name__} - {e}")

# 4. DerivedVariableError: Source column absent for declared derived variable
spec4 = copy.deepcopy(BASE_SPEC)
spec4["derived_variables"] = {"Local_Density_squared": "square_of_local_density"}
norm4 = normalize_prereg(spec4)
df_no_source = pd.DataFrame({"run_id": ["r1"], "y": [1], "x": [1]})  # missing Local_Density
try:
    construct_derived_variables(df_no_source, norm4)
    print("[FAIL] 4: DerivedVariableError not raised")
except DerivedVariableError as e:
    print(f"[PASS] 4: Caught {type(e).__name__} - {e}")

# 5. FormulaVariableError: Variable missing from end dataframe
df_formula = pd.DataFrame({"y": [1]}) # Formula y ~ x requires x
try:
    validate_formula_variables(df_formula, norm_base)
    print("[FAIL] 5: FormulaVariableError not raised")
except FormulaVariableError as e:
    print(f"[PASS] 5: Caught {type(e).__name__} - {e}")

print("=== TEST SUITE COMPLETE ===")
