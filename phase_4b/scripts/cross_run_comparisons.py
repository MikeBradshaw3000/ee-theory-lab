import argparse
import pandas as pd
import numpy as np
from pathlib import Path

def assign_scale_verdict(row):
    try:
        m_rat = row['rho_mean_ratio']
        s_rat = row['rho_std_ratio']
        if pd.isna(m_rat) or pd.isna(s_rat):
            return 'not_assignable'
        if 0.95 <= m_rat <= 1.05:
            if s_rat < 0.95: return 'variance_reducing_only'
            return 'scale_stable'
        if m_rat > 1.05: return 'scale_dependent_strengthening'
        if m_rat < 0.95: return 'scale_dependent_disappearing'
        return 'scale_dependent_other'
    except KeyError:
        return 'not_assignable'

def run_comparisons(tier2_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    files = list(tier2_dir.glob("epoch_summary_*.csv"))
    if not files:
        print("No epoch summary files found for cross-run comparison.")
        return
    dfs = [pd.read_csv(f) for f in files]
    df_all = pd.concat(dfs, ignore_index=True)
    if 'f_variant' not in df_all.columns: df_all.rename(columns={'F_variant': 'f_variant'}, inplace=True)
    if 'scale' not in df_all.columns: df_all.rename(columns={'Scale': 'scale'}, inplace=True)
    df_all['probe_id'] = df_all['run_id'].str.replace(r'_(20x20|40x40)$', '', regex=True)
    n_epochs = df_all['epoch'].nunique()
    df_20 = df_all[df_all['scale'] == '20x20'].copy()
    df_40 = df_all[df_all['scale'] == '40x40'].copy()
    probes_20 = set(df_20['probe_id'])
    probes_40 = set(df_40['probe_id'])
    common_scale = probes_20 & probes_40
    only_20 = probes_20 - probes_40
    only_40 = probes_40 - probes_20
    print(f"[CROSS-SCALE] probe_ids at 20x20: {probes_20 if probes_20 else '{none}'}")
    print(f"[CROSS-SCALE] probe_ids at 40x40: {probes_40 if probes_40 else '{none}'}")
    print(f"[CROSS-SCALE] probe_ids common: {{{len(common_scale)} items}}")
    print(f"[CROSS-SCALE] probe_ids only at 20x20: {only_20 if only_20 else '{none}'}")
    print(f"[CROSS-SCALE] probe_ids only at 40x40: {only_40 if only_40 else '{none}'}")
    scale_merged = pd.merge(df_20, df_40, on=['probe_id', 'f_variant', 'epoch'], suffixes=('_20', '_40'))
    pairs_20 = set(zip(df_20['probe_id'], df_20['f_variant']))
    pairs_40 = set(zip(df_40['probe_id'], df_40['f_variant']))
    common_pairs = pairs_20 & pairs_40
    expected_scale_rows = len(common_pairs) * n_epochs
    actual_scale_rows = len(scale_merged)
    print(f"[CROSS-SCALE] merge produced {actual_scale_rows} rows. Expected (common_pairs x n_epochs) = {expected_scale_rows}.")
    if actual_scale_rows != expected_scale_rows:
        print("  --> [WARNING] CROSS-SCALE ROW COUNT MISMATCH!")
    if 'rho_mean_20' in scale_merged.columns:
        scale_merged['rho_mean_ratio'] = scale_merged['rho_mean_40'] / scale_merged['rho_mean_20']
        scale_merged['rho_std_ratio'] = scale_merged['rho_std_40'] / scale_merged['rho_std_20']
        scale_merged['verdict'] = scale_merged.apply(assign_scale_verdict, axis=1)
        scale_merged.to_csv(output_dir / "cross_scale_metrics.csv", index=False)
    with open(output_dir / "cross_scale_report.md", "w") as f:
        f.write("# Cross-Scale Comparisons Report\n\n")
        f.write("## Comparison Universe\n\n")
        f.write("### Cross-Scale\n")
        f.write(f"Probes compared (present at both 20x20 and 40x40): {common_scale if common_scale else 'None'}\n")
        exc_scale = only_20 | only_40
        f.write(f"Probes excluded from cross-scale comparison: {exc_scale if exc_scale else 'None'}\n\n")
        f.write("\n---\n")
        f.write("**DISCLAIMER:** Threshold cut points are descriptive only and not used adjudicatively.\n\n")
        f.write("Files generated:\n- cross_scale_metrics.csv\n")
    print(f"\nCross-scale comparisons complete. Outputs in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier2-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    run_comparisons(args.tier2_dir, args.output_dir)
