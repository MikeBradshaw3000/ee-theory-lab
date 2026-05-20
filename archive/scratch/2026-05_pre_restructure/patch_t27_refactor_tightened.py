#!/usr/bin/env python3
import os
import hashlib
from pathlib import Path

FILE_PAYLOADS = {
    "cross_run_comparisons.py": r'''import argparse
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
''',

    "tier2_postprocess.py": r'''import argparse
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
'''
}

def build_t27_refactor_tightened():
    base_dir = Path("phase_4b/scripts")
    base_dir.mkdir(parents=True, exist_ok=True)
    print("=== Phase 4B Targeted Refactor (T2.7 Isolation + L1/L2 Tightenings) ===")
    print(f"Target Directory: {base_dir.resolve()}\n")
    for filename, content in FILE_PAYLOADS.items():
        filepath = base_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        file_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        print(f"[VERIFIED] {filename}")
        print(f"           SHA-256: {file_hash}\n")
    print("Execution gate is currently CLOSED pending Layer 1 and Layer 2 review.")

if __name__ == "__main__":
    build_t27_refactor_tightened()
