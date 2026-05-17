import argparse
import pandas as pd
import numpy as np
from pathlib import Path

def run_postprocess(tier2_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    files = list(tier2_dir.glob("epoch_summary_*.csv"))
    if not files:
        print("No epoch summary files found for Tier 2 postprocessing.")
        return
    dfs = [pd.read_csv(f) for f in files]
    df_all = pd.concat(dfs, ignore_index=True)
    if 'f_variant' not in df_all.columns: df_all.rename(columns={'F_variant': 'f_variant'}, inplace=True)
    if 'scale' not in df_all.columns: df_all.rename(columns={'Scale': 'scale'}, inplace=True)
    if 'Drive_Raw_mean_mean' in df_all.columns and 'Drive_Raw_mean' in df_all.columns:
        raise ValueError("Schema ambiguity: both Drive_Raw_mean and Drive_Raw_mean_mean present.")
    elif 'Drive_Raw_mean_mean' in df_all.columns:
        df_all = df_all.rename(columns={'Drive_Raw_mean_mean': 'drive_mean_canonical'})
    elif 'Drive_Raw_mean' in df_all.columns:
        df_all = df_all.rename(columns={'Drive_Raw_mean': 'drive_mean_canonical'})
    else:
        raise ValueError("No drive column found (expected Drive_Raw_mean or Drive_Raw_mean_mean).")
    REQUIRED_T27_COLUMNS = {
        'rho_mean', 'psi_global_mean', 'mean_Lambda_mean',
        'mean_p_act_mean', 'mean_v_mean', 'mean_u_mean', 'mean_r_mean',
        'drive_mean_canonical'
    }
    missing = REQUIRED_T27_COLUMNS - set(df_all.columns)
    if missing:
        raise ValueError(
            f"T2.7 schema validation failed. Missing required columns in epoch_summary CSVs: {missing}. "
            f"Available columns: {sorted(df_all.columns)}"
        )
    df_f2 = df_all[df_all['f_variant'] == 'F_2_symmetric'].copy()
    df_flr = df_all[df_all['f_variant'] == 'F_LR'].copy()
    numeric_cols = df_all.select_dtypes(include=[np.number]).columns.drop(['epoch'], errors='ignore')
    print("=== Shadow-Copy Verification (F_2_symmetric) ===")
    grouped = df_f2.groupby(['scale', 'epoch'])[numeric_cols]
    diffs = grouped.max() - grouped.min()
    for (scale, epoch), row in diffs.iterrows():
        max_diff = row.max()
        if max_diff > 1e-10:
            raise ValueError(
                f"SHADOW COPY VERIFICATION FAILED at scale={scale}, epoch={epoch}. "
                f"Max divergence: {max_diff:.3e}"
            )
    for s in df_f2['scale'].unique():
        scale_diffs = diffs.xs(s, level='scale')
        max_for_scale = scale_diffs.max().max()
        print(f"[PASS] Scale {s} F_2_symmetric probes verified as byte-identical shadow copies "
              f"(max divergence {max_for_scale:.2e} <= 1e-10).")
    canonical_f2 = df_f2[df_f2['run_id'].str.contains('probe1_overcrowding')].copy()
    canonical_flr = df_flr[df_flr['run_id'].str.contains('probe2_starvation_FLR')].copy()
    n_epochs = df_all['epoch'].nunique()
    n_scales = df_all['scale'].nunique()
    expected_canonical_rows = n_epochs * n_scales
    assert len(canonical_f2) == expected_canonical_rows, (
        f"Canonical F_2_symmetric selection cardinality wrong: got {len(canonical_f2)}, "
        f"expected {expected_canonical_rows} (n_scales={n_scales} x n_epochs={n_epochs}). "
        f"Matched run_ids: {sorted(canonical_f2['run_id'].unique())}"
    )
    assert len(canonical_flr) == expected_canonical_rows, (
        f"Canonical F_LR selection cardinality wrong: got {len(canonical_flr)}, "
        f"expected {expected_canonical_rows}. "
        f"Matched run_ids: {sorted(canonical_flr['run_id'].unique())}"
    )
    assert canonical_f2.groupby(['scale', 'epoch']).size().max() == 1, (
        "Canonical F_2_symmetric selection has duplicate (scale, epoch) entries."
    )
    assert canonical_flr.groupby(['scale', 'epoch']).size().max() == 1, (
        "Canonical F_LR selection has duplicate (scale, epoch) entries."
    )
    print("\n=== Canonical Run Selection ===")
    print(f"F_2_symmetric canonical representatives: {list(canonical_f2['run_id'].unique())}")
    print(f"F_LR canonical representatives: {list(canonical_flr['run_id'].unique())}")
    ff_merged = pd.merge(canonical_f2, canonical_flr, on=['scale', 'epoch'], suffixes=('_f2', '_flr'))
    ff_merged['delta_rho'] = ff_merged['rho_mean_f2'] - ff_merged['rho_mean_flr']
    ff_merged['delta_psi'] = ff_merged['psi_global_mean_f2'] - ff_merged['psi_global_mean_flr']
    ff_merged['delta_Lambda'] = ff_merged['mean_Lambda_mean_f2'] - ff_merged['mean_Lambda_mean_flr']
    ff_merged['delta_p_act'] = ff_merged['mean_p_act_mean_f2'] - ff_merged['mean_p_act_mean_flr']
    ff_merged['delta_v'] = ff_merged['mean_v_mean_f2'] - ff_merged['mean_v_mean_flr']
    ff_merged['delta_u'] = ff_merged['mean_u_mean_f2'] - ff_merged['mean_u_mean_flr']
    ff_merged['delta_r'] = ff_merged['mean_r_mean_f2'] - ff_merged['mean_r_mean_flr']
    ff_merged['delta_drive'] = ff_merged['drive_mean_canonical_f2'] - ff_merged['drive_mean_canonical_flr']
    out_cols = ['scale', 'epoch'] + [c for c in ff_merged.columns if c.startswith('delta_')]
    ff_merged[out_cols].to_csv(output_dir / "fform_comparison.csv", index=False)
    actual_rows = len(ff_merged)
    print(f"\n[T2.7 CROSS-F-FORM] merge produced {actual_rows} rows. Expected {expected_canonical_rows} ({n_scales} scales x {n_epochs} epochs).")
    if actual_rows != expected_canonical_rows:
        print("  --> [WARNING] CROSS-F-FORM ROW COUNT MISMATCH!")
    print(f"Tier 2 postprocessing complete. Outputs in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier2-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    run_postprocess(args.tier2_dir, args.output_dir)
