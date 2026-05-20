#!/usr/bin/env python3
import os
import hashlib
from pathlib import Path

# =============================================================================
# PHASE 4B TARGETED PATCH: CROSS RUN PROBE-MIXING & ASYMMETRY DIAGNOSTICS
# Target HEAD: df9122e
# =============================================================================

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
    
    # Derive probe_id by safely stripping trailing scale suffixes
    df_all['probe_id'] = df_all['run_id'].str.replace(r'_(20x20|40x40)$', '', regex=True)
    n_epochs = df_all['epoch'].nunique()
    
    # ==========================================
    # a) Cross-Scale
    # ==========================================
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
    
    # ==========================================
    # b) Cross-F-form
    # ==========================================
    df_f2 = df_all[df_all['f_variant'] == 'F_2_symmetric'].copy()
    df_flr = df_all[df_all['f_variant'] == 'F_LR'].copy()
    
    ff_expected_total = 0
    ff_universe = {}
    
    for s in ['20x20', '40x40']:
        p_f2 = set(df_f2[df_f2['scale'] == s]['probe_id'])
        p_flr = set(df_flr[df_flr['scale'] == s]['probe_id'])
        c_ff = p_f2 & p_flr
        o_f2 = p_f2 - p_flr
        o_flr = p_flr - p_f2
        
        ff_universe[s] = {'common': c_ff, 'only_f2': o_f2, 'only_flr': o_flr}
        
        print(f"[CROSS-F-FORM] scale={s}, probe_ids in F_2_symmetric: {{{len(p_f2)} items}}")
        print(f"[CROSS-F-FORM] scale={s}, probe_ids in F_LR: {{{len(p_flr)} items}}")
        print(f"[CROSS-F-FORM] scale={s}, probe_ids common: {{{len(c_ff)} items}}")
        print(f"[CROSS-F-FORM] scale={s}, probe_ids only in F_2_symmetric: {o_f2 if o_f2 else '{none}'}")
        print(f"[CROSS-F-FORM] scale={s}, probe_ids only in F_LR: {o_flr if o_flr else '{none}'}")
        
        ff_expected_total += len(c_ff) * n_epochs

    ff_merged = pd.merge(df_f2, df_flr, on=['probe_id', 'scale', 'epoch'], suffixes=('_f2', '_flr'))
    actual_ff_rows = len(ff_merged)
    
    print(f"[CROSS-F-FORM] merge produced {actual_ff_rows} rows. Expected (sum of common_probes_per_scale x n_epochs) = {ff_expected_total}.")
    if actual_ff_rows != ff_expected_total:
        print("  --> [WARNING] CROSS-F-FORM ROW COUNT MISMATCH!")

    if 'rho_mean_f2' in ff_merged.columns:
        ff_merged['delta_rho'] = ff_merged['rho_mean_f2'] - ff_merged['rho_mean_flr']
        ff_merged['delta_psi'] = ff_merged.get('psi_global_mean_f2', np.nan) - ff_merged.get('psi_global_mean_flr', np.nan)
        ff_merged['delta_Lambda'] = ff_merged.get('mean_Lambda_mean_f2', np.nan) - ff_merged.get('mean_Lambda_mean_flr', np.nan)
        ff_merged['delta_p_act'] = ff_merged.get('mean_p_act_mean_f2', np.nan) - ff_merged.get('mean_p_act_mean_flr', np.nan)
        ff_merged['delta_v'] = ff_merged.get('mean_v_mean_f2', np.nan) - ff_merged.get('mean_v_mean_flr', np.nan)
        ff_merged['delta_u'] = ff_merged.get('mean_u_mean_f2', np.nan) - ff_merged.get('mean_u_mean_flr', np.nan)
        ff_merged['delta_r'] = ff_merged.get('mean_r_mean_f2', np.nan) - ff_merged.get('mean_r_mean_flr', np.nan)
        ff_merged.to_csv(output_dir / "fform_comparison.csv", index=False)
        
    with open(output_dir / "cross_scale_report.md", "w") as f:
        f.write("# Cross-Run Comparisons Report\n\n")
        
        f.write("## Comparison Universe\n\n")
        f.write("### Cross-Scale\n")
        f.write(f"Probes compared (present at both 20x20 and 40x40): {common_scale if common_scale else 'None'}\n")
        exc_scale = only_20 | only_40
        f.write(f"Probes excluded from cross-scale comparison: {exc_scale if exc_scale else 'None'}\n\n")
        
        f.write("### Cross-F-Form\n")
        for s in ['20x20', '40x40']:
            c_ff = ff_universe[s]['common']
            exc_ff = ff_universe[s]['only_f2'] | ff_universe[s]['only_flr']
            f.write(f"Probes compared at scale={s} (present in both F_2_symmetric and F_LR): {c_ff if c_ff else 'None'}\n")
            f.write(f"Probes excluded from cross-F-form comparison at scale={s}: {exc_ff if exc_ff else 'None'}\n")
        
        f.write("\n---\n")
        f.write("**DISCLAIMER:** Threshold cut points are descriptive only and not used adjudicatively.\n\n")
        f.write("Files generated:\n- cross_scale_metrics.csv\n- fform_comparison.csv\n")
        
    print(f"\nCross-run comparisons complete. Outputs in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier2-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    run_comparisons(args.tier2_dir, args.output_dir)
'''
}

def build_targeted_patch():
    base_dir = Path("phase_4b/scripts")
    base_dir.mkdir(parents=True, exist_ok=True)
    print("=== Phase 4B Targeted Patch: cross_run_comparisons.py (Probe Mixing & Diagnostics) ===")
    print(f"Target Directory: {base_dir.resolve()}\n")
    for filename, content in FILE_PAYLOADS.items():
        filepath = base_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        file_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        print(f"[VERIFIED] {filename}")
        print(f"           SHA-256: {file_hash}\n")
    print("Execution gate is currently CLOSED pending Layer 1 and Layer 2 patch review.")

if __name__ == "__main__":
    build_targeted_patch()
