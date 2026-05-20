"""Apply Tier 2 sanity check fix v2 to tier3_regression.py.

Previous fix assumed pandas merge would apply _t3/_t2 suffixes to clashing column names.
Empirical result shows this did not happen as expected. New approach: rename our computed
columns to _t3 BEFORE the merge to avoid relying on suffix behavior.
"""
import pathlib

script_path = pathlib.Path(r"C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\phase_4b\scripts\tier3_regression.py")
content = script_path.read_text(encoding="utf-8")

old_block = """    for run in df['run_id'].unique():
        t2_file = t2_dir / f"global_timeseries_{run}.csv"
        if t2_file.exists():
            t2_df = pd.read_csv(t2_file)
            # Tier 2 schema uses rho_global and psi_global as first-class columns.
            # Use suffixes to distinguish our computed values from Tier 2's stored values.
            comp = tick_aggregates[tick_aggregates['run_id'] == run].merge(
                t2_df, on='Tick', suffixes=('_t3', '_t2')
            )
            
            # Hard-fail if expected Tier 2 columns do not exist in the schema
            expected_cols = {'rho_global_t2', 'psi_global_t2'}
            missing_cols = expected_cols - set(comp.columns)
            
            if missing_cols:
                raise ValueError(
                    f"T3 FAULT: Tier 2 Sanity Check failed to execute. Missing expected columns {missing_cols} "
                    f"in {t2_file.name}. Available columns: {sorted(comp.columns)}"
                )
                
            diff_rho = (comp['rho_global_t3'] - comp['rho_global_t2']).abs()
            diff_psi = (comp['psi_global_t3'] - comp['psi_global_t2']).abs()
            
            t2_mismatch_count += (diff_rho > 1e-10).sum() + (diff_psi > 1e-10).sum()
            t2_max_diff = max(t2_max_diff, diff_rho.max(), diff_psi.max())
            t2_files_checked += 1"""

new_block = """    for run in df['run_id'].unique():
        t2_file = t2_dir / f"global_timeseries_{run}.csv"
        if t2_file.exists():
            t2_df = pd.read_csv(t2_file)
            # Tier 2 schema uses rho_global and psi_global as first-class columns.
            # Explicitly rename our computed columns to _t3 before merge to avoid
            # relying on pandas auto-suffix behavior.
            t3_aggs = tick_aggregates[tick_aggregates['run_id'] == run].rename(
                columns={'rho_global': 'rho_global_t3', 'psi_global': 'psi_global_t3'}
            )
            comp = t3_aggs.merge(t2_df, on='Tick')
            
            # Hard-fail if expected Tier 2 columns do not exist in the schema
            expected_cols = {'rho_global', 'psi_global'}
            missing_cols = expected_cols - set(comp.columns)
            
            if missing_cols:
                raise ValueError(
                    f"T3 FAULT: Tier 2 Sanity Check failed to execute. Missing expected columns {missing_cols} "
                    f"in {t2_file.name}. Available columns: {sorted(comp.columns)}"
                )
                
            diff_rho = (comp['rho_global_t3'] - comp['rho_global']).abs()
            diff_psi = (comp['psi_global_t3'] - comp['psi_global']).abs()
            
            t2_mismatch_count += (diff_rho > 1e-10).sum() + (diff_psi > 1e-10).sum()
            t2_max_diff = max(t2_max_diff, diff_rho.max(), diff_psi.max())
            t2_files_checked += 1"""

content_new = content.replace(old_block, new_block)
edit_applied = content_new != content
script_path.write_text(content_new, encoding="utf-8")
print(f"Tier 2 sanity check fix v2: {'APPLIED' if edit_applied else 'NOT APPLIED'}")
