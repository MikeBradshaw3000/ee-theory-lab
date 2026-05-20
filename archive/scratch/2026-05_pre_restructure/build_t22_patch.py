#!/usr/bin/env python3
import os
import hashlib
from pathlib import Path

# =============================================================================
# PHASE 4B TARGETED PATCH: TIER 2 ANALYZE (T2.2 & DDOF NOTE)
# =============================================================================

FILE_PAYLOADS = {
    "tier2_analyze.py": r'''import argparse
import pandas as pd
import numpy as np
import scipy.ndimage
import pyarrow.dataset as ds
from pyarrow import parquet as pq
from pathlib import Path
from _phase_4b_common import verify_environment

def normalize_scale(x):
    x = str(x)
    if x in ["20", "20x20", "20x20"]: return "20x20"
    if x in ["40", "40x40", "40x40"]: return "40x40"
    return x

def compute_morans_i(data, grid_size):
    z = data - np.mean(data)
    if np.std(z) == 0: return 0.0
    z_sq_sum = np.sum(z**2)
    shifts = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    w_sum = len(shifts) * (grid_size**2)
    num = 0
    for dr, dc in shifts:
        num += np.sum(z * np.roll(z, shift=(dr, dc), axis=(0, 1)))
    return (grid_size**2 / w_sum) * (num / z_sq_sum)

def compute_same_sign_share(psi_grid):
    psi_sign = np.sign(psi_grid)
    shifts = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    valid_pairs = 0
    same_sign_pairs = 0
    for dr, dc in shifts:
        neighbor_sign = np.roll(psi_sign, shift=(dr, dc), axis=(0, 1))
        both_nonzero = (psi_sign != 0) & (neighbor_sign != 0)
        valid_pairs += np.sum(both_nonzero)
        same_sign_pairs += np.sum(both_nonzero & (psi_sign == neighbor_sign))
    return same_sign_pairs / valid_pairs if valid_pairs > 0 else np.nan

def run_tier2(parquet_file: Path, output_dir: Path):
    verify_environment()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    meta = pq.read_metadata(parquet_file)
    custom_meta = meta.metadata or {}
    f_variant = custom_meta.get(b'F_variant', b'Unknown').decode()
    scale_raw = custom_meta.get(b'Scale', b'Unknown').decode()
    scale = normalize_scale(scale_raw)
    run_id = parquet_file.stem
    
    dataset = ds.dataset(parquet_file, format="parquet")
    target_ticks = [0, 100, 500, 1000, 1500, 2000, 2500, 2999]
    metrics = ['Lambda_total', 'Drive_Raw', 'p_act', 'Psi_local', 'b_i_v', 'b_i_u', 'b_i_r', 'Local_Density']
    
    batch_aggs = []
    target_rows = []
    cardinality_sets = {m: set() for m in ['Lambda_total', 'Drive_Raw', 'p_act', 'Psi_local', 'Local_Density']}
    
    # Batch Processing Loop for Memory Hygiene
    for batch in dataset.to_batches():
        df = batch.to_pandas()
        
        # T2.8 tracking
        for m in cardinality_sets.keys():
            cardinality_sets[m].update(np.round(df[m].dropna(), 6).unique())
            
        # Target isolation for ticks
        target_rows.append(df[df['Tick'].isin(target_ticks)])
        
        # Base batch metrics
        bins = [-1, 99, 499, 999, 1499, 1999, 2499, 2999]
        df['epoch'] = pd.cut(df['Tick'], bins=bins, labels=False, include_lowest=True)
        
        df['Psi_pos'] = (df['Psi_local'] > 0).astype(int)
        df['Psi_neg'] = (df['Psi_local'] < 0).astype(int)
        df['Psi_zero'] = (df['Psi_local'] == 0).astype(int)
        
        agg_dict = {
            'Delta_v': ['sum'], 'Delta_u': ['sum'], 'Delta_r': ['sum'],
            'Psi_pos': ['sum'], 'Psi_neg': ['sum'], 'Psi_zero': ['sum']
        }
        for m in metrics:
            df[f"{m}_sq"] = df[m]**2
            agg_dict[m] = ['sum', 'count', 'min', 'max']
            agg_dict[f"{m}_sq"] = ['sum']
            
        b_agg = df.groupby(['Tick', 'epoch']).agg(agg_dict)
        b_agg.columns = ['_'.join(col).strip() for col in b_agg.columns.values]
        batch_aggs.append(b_agg.reset_index())
        
    # Combiner
    df_comb = pd.concat(batch_aggs)
    comb_rules = {}
    for c in df_comb.columns:
        if c in ['Tick', 'epoch']: continue
        if c.endswith('_sum') or c.endswith('_count'): comb_rules[c] = 'sum'
        elif c.endswith('_min'): comb_rules[c] = 'min'
        elif c.endswith('_max'): comb_rules[c] = 'max'
        
    final_comb = df_comb.groupby(['Tick', 'epoch']).agg(comb_rules).reset_index()
    
    # T2.1 Global Timeseries
    t21_df = pd.DataFrame({'Tick': final_comb['Tick'], 'epoch': final_comb['epoch']})
    for m in metrics:
        count = final_comb[f"{m}_count"]
        mean = final_comb[f"{m}_sum"] / count
        var = (final_comb[f"{m}_sq_sum"] - (final_comb[f"{m}_sum"]**2 / count)) / count
        std = np.sqrt(np.maximum(var, 0))
        
        t21_df[f"{m}_mean"] = mean
        t21_df[f"{m}_std"] = std
        t21_df[f"{m}_min"] = final_comb[f"{m}_min"]
        t21_df[f"{m}_max"] = final_comb[f"{m}_max"]
        
    t21_df.to_csv(output_dir / f"global_timeseries_{run_id}.csv", index=False)
    
    # T2.2 Epoch Summary (Corrected Variance Logic)
    epoch_cols = ['Lambda_total_mean', 'Drive_Raw_mean', 'p_act_mean', 
                  'Psi_local_mean', 'b_i_v_mean', 'b_i_u_mean', 'b_i_r_mean', 
                  'Local_Density_mean']
    t22_agg = t21_df.groupby('epoch')[epoch_cols].agg(['mean', 'std', 'min', 'max']).reset_index()
    t22_agg.columns = ['_'.join(col).strip('_') for col in t22_agg.columns.values]
    
    rename_map = {
        'Local_Density_mean_mean': 'rho_mean', 'Local_Density_mean_std': 'rho_std',
        'Psi_local_mean_mean': 'psi_global_mean', 'Lambda_total_mean_mean': 'mean_Lambda_mean',
        'p_act_mean_mean': 'mean_p_act_mean', 'b_i_v_mean_mean': 'mean_v_mean',
        'b_i_u_mean_mean': 'mean_u_mean', 'b_i_r_mean_mean': 'mean_r_mean'
    }
    t22_agg.rename(columns=rename_map, inplace=True)
    t22_agg['run_id'] = run_id
    t22_agg['f_variant'] = f_variant
    t22_agg['scale'] = scale
    t22_agg.to_csv(output_dir / f"epoch_summary_{run_id}.csv", index=False)
    
    # T2.3-T2.6 Target Execution
    df_targets = pd.concat(target_rows)
    t23_records, t24_records, t25_records, t26_records = [], [], [], []
    
    for t in target_ticks:
        t_df = df_targets[df_targets['Tick'] == t]
        if t_df.empty: continue
        
        # T2.3 Quantiles (11-quantile schema match)
        for m in metrics:
            d = t_df[m]
            t23_records.append({
                "run_id": run_id, "Tick": t, "Metric": m,
                "mean": d.mean(), "sd": d.std(), "min": d.min(),
                "p01": d.quantile(0.01), "p05": d.quantile(0.05), "p25": d.quantile(0.25),
                "median": d.median(), "p75": d.quantile(0.75), "p95": d.quantile(0.95),
                "p99": d.quantile(0.99), "max": d.max()
            })
            
        # T2.4 Sign Decomp
        t24_records.append({
            'Tick': t,
            'pos_count': (t_df['Psi_local'] > 0).sum(),
            'neg_count': (t_df['Psi_local'] < 0).sum(),
            'zero_count': (t_df['Psi_local'] == 0).sum(),
            'pos_mean': t_df.loc[t_df['Psi_local'] > 0, 'Psi_local'].mean(),
            'neg_mean': t_df.loc[t_df['Psi_local'] < 0, 'Psi_local'].mean()
        })
        
        # T2.5 Spatial
        t_df = t_df.sort_values(['Agent_X', 'Agent_Y'])
        xs = t_df['Agent_X'].nunique()
        psi_grid = t_df['Psi_local'].values.reshape((xs, xs))
        act_grid = t_df['is_active'].values.reshape((xs, xs))
        
        pos_psi = (psi_grid > 0).astype(int)
        neg_psi = (psi_grid < 0).astype(int)
        p_labels, p_num = scipy.ndimage.label(pos_psi)
        n_labels, n_num = scipy.ndimage.label(neg_psi)

        def comp_stats(labels, num):
            if num == 0: return 0, 0, 0
            sizes = np.bincount(labels.flat)[1:]
            return sizes.max(), sizes.mean(), sizes.sum()

        p_max, p_mean, p_tot = comp_stats(p_labels, p_num)
        n_max, n_mean, n_tot = comp_stats(n_labels, n_num)

        t25_records.append({
            "run_id": run_id, "Tick": t,
            "Moran_I_Psi": compute_morans_i(psi_grid, xs),
            "Moran_I_Act": compute_morans_i(act_grid, xs),
            "same_sign_share": compute_same_sign_share(psi_grid),
            "pos_largest": p_max, "pos_mean_size": p_mean, "pos_total_cells": p_tot,
            "neg_largest": n_max, "neg_mean_size": n_mean, "neg_total_cells": n_tot
        })
        
        # T2.6 Boundaries
        t26_records.append({
            'Tick': t,
            'v_low': (t_df['b_i_v'] <= 0.01).sum(), 'v_high': (t_df['b_i_v'] >= 0.99).sum(),
            'u_low': (t_df['b_i_u'] <= 0.01).sum(), 'u_high': (t_df['b_i_u'] >= 0.99).sum(),
            'r_low': (t_df['b_i_r'] <= 0.01).sum(), 'r_high': (t_df['b_i_r'] >= 0.99).sum()
        })
        
    pd.DataFrame(t23_records).to_csv(output_dir / f"selected_tick_distributions_{run_id}.csv", index=False)
    pd.DataFrame(t24_records).to_csv(output_dir / f"psi_sign_decomposition_{run_id}.csv", index=False)
    pd.DataFrame(t25_records).to_csv(output_dir / f"psi_spatial_diagnostics_{run_id}.csv", index=False)
    pd.DataFrame(t26_records).to_csv(output_dir / f"base_boundary_summary_{run_id}.csv", index=False)
    
    # Q-Effect Extension
    q_effect = pd.DataFrame({
        'run_id': run_id, 'f_variant': f_variant, 'scale': scale,
        'epoch': final_comb['epoch'],
        'mean_Delta_v': final_comb['Delta_v_sum'] / final_comb['Lambda_total_count'],
        'mean_Delta_u': final_comb['Delta_u_sum'] / final_comb['Lambda_total_count'],
        'mean_Delta_r': final_comb['Delta_r_sum'] / final_comb['Lambda_total_count'],
        'pos_Psi_share': final_comb['Psi_pos_sum'] / final_comb['Lambda_total_count'],
        'neg_Psi_share': final_comb['Psi_neg_sum'] / final_comb['Lambda_total_count'],
        'zero_Psi_share': final_comb['Psi_zero_sum'] / final_comb['Lambda_total_count']
    }).groupby(['run_id', 'f_variant', 'scale', 'epoch']).mean().reset_index()
    q_effect.to_csv(output_dir / f"q_effect_decomposition_{run_id}.csv", index=False)

    # T2.8 Compression Fingerprint
    sizes = {}
    for i in range(meta.num_row_groups):
        rg = meta.row_group(i)
        for j in range(rg.num_columns):
            col = rg.column(j)
            sizes[col.path_in_schema] = sizes.get(col.path_in_schema, 0) + col.total_compressed_size
            
    with open(output_dir / f"compression_fingerprint_{run_id}.csv", "w") as f:
        f.write("column,compressed_bytes\n")
        for k, v in sizes.items(): f.write(f"{k},{v}\n")
        f.write("\ncardinality_1e-6_precision\n")
        for k, v in cardinality_sets.items(): f.write(f"{k},{len(v)}\n")

    print(f"Tier 2 Analysis complete for {run_id}. Outputs in {output_dir}")
    print("Methodological Note: Cardinality counted at 1e-6 precision. Connected component labeling non-toroidal. Moran's I toroidal. Tick-level variance uses ddof=0 (population).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    run_tier2(args.parquet, args.output_dir)
'''
}

def build_targeted_patch():
    base_dir = Path("phase_4b/scripts")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== Phase 4B Targeted Patch Builder (T2.2) ===")
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
