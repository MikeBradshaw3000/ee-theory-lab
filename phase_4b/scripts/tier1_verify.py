import argparse
import gc
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from pathlib import Path
from _phase_4b_common import verify_environment, get_paths

def run_tier1_verification(parquet_file: Path):
    verify_environment()
    _, _, _ = get_paths()
    
    meta = pq.read_metadata(parquet_file)
    custom_meta = meta.metadata or {}
    f_variant = custom_meta.get(b'F_variant', b'').decode()
    if f_variant not in ['F_LR', 'F_2_symmetric']:
        raise ValueError(f"T1 FAULT: Missing or unknown F_variant in metadata: {f_variant}. Only F_LR and F_2_symmetric permitted.")
    
    df = pd.read_parquet(parquet_file)
    
    # C2 Hardening: Coordinate validation
    x_vals = sorted(df["Agent_X"].unique())
    y_vals = sorted(df["Agent_Y"].unique())
    xs, ys = len(x_vals), len(y_vals)
    
    if x_vals != list(range(xs)) or y_vals != list(range(ys)):
        raise ValueError("R2 FAULT: Coordinates do not form complete consecutive sets.")
    if df.duplicated(["Tick", "Agent_X", "Agent_Y"]).any():
        raise ValueError("R2 FAULT: Duplicate Tick-Agent_X-Agent_Y rows.")
        
    df = df.sort_values(['Tick', 'Agent_X', 'Agent_Y'])
    eps_alg = 1e-10
    eps_sig = 1e-9
    
    report_data = {}
    
    # V1. Drive decomposition
    v1_diff = np.abs(df['Drive_Raw'] - (df['Term_Lambda'] + df['Term_Density_Pos'] + df['Term_Overcrowding'] + df['Term_Offset']))
    report_data['V1_Drive_Decomp_Fails'] = (v1_diff > eps_alg).sum()
    
    # V2. Term_Lambda
    v2_diff = np.abs(df['Term_Lambda'] - (4.0 * df['Lambda_total']))
    report_data['V2_Term_Lambda_Fails'] = (v2_diff > eps_alg).sum()
    
    # V3. Density components
    v3_pos = np.abs(df['Term_Density_Pos'] - (3.0 * df['Local_Density']))
    v3_over = np.abs(df['Term_Overcrowding'] - (-4.0 * df['Local_Density']**2))
    v3_off = np.abs(df['Term_Offset'] - (-4.0))
    report_data['V3_Density_Fails'] = ((v3_pos > eps_alg) | (v3_over > eps_alg) | (v3_off > eps_alg)).sum()
    
    # V4. Probability chain
    p_base_calc = 1.0 / (1.0 + np.exp(-df['Drive_Raw']))
    p_act_calc = p_base_calc + 0.01 * (1.0 - p_base_calc)
    report_data['V4_Probability_Fails'] = ((np.abs(df['p_base'] - p_base_calc) > eps_sig) | (np.abs(df['p_act'] - p_act_calc) > eps_sig)).sum()
    
    # V5. Realization invariant
    report_data['V5_Realization_Fails'] = (df['is_active'] != (df['PRNG_draw'] < df['p_act'])).sum()
    
    # V6. F-form computation
    if f_variant == 'F_LR':
        f_calc = df[['b_i_v', 'b_i_u', 'b_i_r']].min(axis=1)
        report_data['V6_F_Form_Fails'] = (np.abs(df['Lambda_total'] - f_calc) > eps_alg).sum()
    else:
        v6_1 = np.abs(df['Lambda_total'] - (df['Lambda_multiplicative'] * df['Lambda_additive']))
        report_data['V6_F_Form_Fails'] = (v6_1 > eps_alg).sum()
        
    # V7. Q diagonal discipline
    v7_v = np.abs(df['Delta_v'] - (0.001 * df['Psi_local']))
    v7_u = np.abs(df['Delta_u'] - (0.001 * df['Psi_local']))
    v7_r = np.abs(df['Delta_r'] - (0.001 * df['Psi_local']))
    report_data['V7_Q_Diagonal_Fails'] = ((v7_v > eps_alg) | (v7_u > eps_alg) | (v7_r > eps_alg)).sum()
    
    # V8. Pre-Q vs post-Q tick discipline & Toroidal Moore Psi_local
    ticks = df['Tick'].nunique()
    is_act_3d = df['is_active'].values.reshape((ticks, xs, ys)).astype(int)
    ds_3d = np.zeros_like(is_act_3d, dtype=float)
    ds_3d[1:] = is_act_3d[1:] - is_act_3d[:-1]
    
    psi_3d = df['Psi_local'].to_numpy().reshape(ticks, xs, ys)
    psi_calc_3d = np.zeros_like(ds_3d, dtype=float)
    
    # V8a: Tick 0 Psi reconstruction is not possible from persisted is_active alone.
    # Substrate computes tick-0 Psi from state_history deque storing initial pre-step
    # activation state, which is consumed by deque rotation and not persisted to parquet.
    # V8 Psi reconstruction verifies ticks 1 through ticks-1.
    v8_psi_fails = 0
    
    for t in range(1, ticks):
        grid = ds_3d[t]
        n_sum = (np.roll(grid, 1, 0) + np.roll(grid, -1, 0) + 
                 np.roll(grid, 1, 1) + np.roll(grid, -1, 1) + 
                 np.roll(np.roll(grid, 1, 0), 1, 1) + np.roll(np.roll(grid, 1, 0), -1, 1) + 
                 np.roll(np.roll(grid, -1, 0), 1, 1) + np.roll(np.roll(grid, -1, 0), -1, 1))
        psi_calc_3d[t] = grid * n_sum
        v8_psi_fails += (np.abs(psi_3d[t] - psi_calc_3d[t]) > eps_alg).sum()
        
    # Tick discipline for base components
    df_next = df.groupby(['Agent_X', 'Agent_Y'])[['b_i_v', 'b_i_u', 'b_i_r']].shift(-1)
    b_v_calc = np.clip(df['b_i_v'] + df['Delta_v'], 0.0, 1.0)
    v8_tick_fails = ((np.abs(df_next['b_i_v'] - b_v_calc) > eps_alg) & df_next['b_i_v'].notna()).sum()
    
    report_data['V8_Discipline_Fails'] = int(v8_psi_fails + v8_tick_fails)
    
    total_fails = sum(report_data.values())
    verdict = "PASS" if total_fails == 0 else "FAIL"
    
    # Path discipline
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    out_dir = project_root / "phase_4b" / "tier1_reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"tier1_{parquet_file.stem}.md"
    
    with open(report_path, 'w') as f:
        f.write(f"# Tier 1 Verification Report: {parquet_file.name}\n")
        f.write(f"Verdict: **{verdict}**\n\n")
        for k, v in report_data.items():
            f.write(f"- {k}: {v}\n")
        f.write("\n## Tick 0 Psi Observability Note\n\n")
        f.write("Tick 0 Psi_local reconstruction skipped for V8: substrate computes tick-0 Psi from the\n")
        f.write("transition between the initial activation state held in state_history (deque-stored,\n")
        f.write("not persisted) and the post-step tick-0 state. The initial pre-step state is not\n")
        f.write("persisted in parquet, so tick-0 Psi cannot be reconstructed from persisted is_active\n")
        f.write("alone. V8 Psi reconstruction verifies ticks 1-2999. Tick-0 Psi remains a valid substrate\n")
        f.write("output for Tier 2 descriptive analysis, with this observability caveat.\n\n")
        f.write("ds inferred from is_active(t) - is_active(t-1) for t >= 1.\n")
        
    del df
    gc.collect()
    print(f"[{verdict}] {parquet_file.name} - Report generated at {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet", type=Path, required=True)
    args = parser.parse_args()
    run_tier1_verification(args.parquet)
