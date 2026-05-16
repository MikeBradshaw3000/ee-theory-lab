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
    output_dir.mkdir(exist_ok=True)
    files = list(tier2_dir.glob("epoch_summary_*.csv"))
    if not files:
        print("No epoch summary files found for cross-run comparison.")
        return
        
    dfs = [pd.read_csv(f) for f in files]
    df_all = pd.concat(dfs, ignore_index=True)
    
    if 'f_variant' not in df_all.columns: df_all.rename(columns={'F_variant': 'f_variant'}, inplace=True)
    if 'scale' not in df_all.columns: df_all.rename(columns={'Scale': 'scale'}, inplace=True)
    
    # a) Cross-Scale
    df_20 = df_all[df_all['scale'] == '20x20'].copy()
    df_40 = df_all[df_all['scale'] == '40x40'].copy()
    
    scale_merged = pd.merge(df_20, df_40, on=['f_variant', 'epoch'], suffixes=('_20', '_40'))
    if 'rho_mean_20' in scale_merged.columns:
        scale_merged['rho_mean_ratio'] = scale_merged['rho_mean_40'] / scale_merged['rho_mean_20']
        scale_merged['rho_std_ratio'] = scale_merged['rho_std_40'] / scale_merged['rho_std_20']
        scale_merged['verdict'] = scale_merged.apply(assign_scale_verdict, axis=1)
        scale_merged.to_csv(output_dir / "cross_scale_metrics.csv", index=False)
    
    # b) Cross-F-form
    df_f2 = df_all[df_all['f_variant'] == 'F_2_symmetric'].copy()
    df_flr = df_all[df_all['f_variant'] == 'F_LR'].copy()
    
    ff_merged = pd.merge(df_f2, df_flr, on=['scale', 'epoch'], suffixes=('_f2', '_flr'))
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
        f.write("**DISCLAIMER:** Threshold cut points are descriptive only and not used adjudicatively.\n\n")
        f.write("Files generated:\n- cross_scale_metrics.csv\n- fform_comparison.csv\n")
        
    print(f"Cross-run comparisons complete. Outputs in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier2-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    run_comparisons(args.tier2_dir, args.output_dir)
