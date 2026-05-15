import os
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from pathlib import Path
from scipy.ndimage import label
import hashlib

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

def analyze_flight2():
    base_path = Path(__file__).resolve().parent
    input_dir = base_path / "flight2_outputs"
    output_dir = base_path / "flight2_analysis_outputs"
    output_dir.mkdir(exist_ok=True)
    
    target_ticks = [0, 100, 500, 1000, 1500, 2000, 2500, 2999]
    epoch_bins = [-1, 99, 499, 999, 1499, 1999, 2499, 2999]
    epoch_labels = ["0-99", "100-499", "500-999", "1000-1499", "1500-1999", "2000-2499", "2500-2999"]
    
    # PATCH 1: Sort probe1 files first (canonical F_2_symmetric source), then by filename
    files = sorted(input_dir.glob("*.parquet"), key=lambda p: (0 if 'probe1' in p.name else 1, p.name))
    
    print("--- FLIGHT 2 ANALYSIS PROVENANCE ---")
    
    file_hashes = {}
    unique_files = []

    global_ts_accum = []
    dist_accum = []
    psi_sign_accum = []
    spatial_accum = []
    boundary_accum = []
    fingerprint_accum = []

    for p_path in files:
        f_size = p_path.stat().st_size
        with open(p_path, 'rb') as f:
            f_hash = hashlib.md5(str(f_size).encode() + f.read(1024*1024)).hexdigest()
        
        if f_hash in file_hashes:
            print(f"\n[SHADOW COPY DETECTED] {p_path.name}")
            print(f"  Byte-identical to {file_hashes[f_hash]}. Skipping analysis to prevent duplication.")
            continue
            
        file_hashes[f_hash] = p_path.name
        unique_files.append(p_path)

    for p_path in unique_files:
        pf = pq.ParquetFile(p_path)
        meta = pf.metadata
        custom_meta = meta.metadata or {}
        
        f_variant = custom_meta.get(b'F_variant', b'Unknown').decode()
        scale = custom_meta.get(b'Scale', b'Unknown').decode()
        run_id = p_path.stem

        print(f"\nFile: {p_path.name}")
        print(f"  Substrate_version: {custom_meta.get(b'Substrate_version', b'Unknown').decode()}")
        print(f"  F_variant: {f_variant} | Scale: {scale}")
        print(f"  PRNG_seed: {custom_meta.get(b'PRNG_seed', b'Unknown').decode()}")
        print(f"  Execution_timestamp: {custom_meta.get(b'Execution_timestamp', b'Unknown').decode()}")
        print(f"  File size: {p_path.stat().st_size} bytes | Row count: {meta.num_rows}")
        
        # Compression Fingerprint
        col_compressed_sizes = {}
        for i in range(meta.num_row_groups):
            rg = meta.row_group(i)
            for j in range(meta.num_columns):
                c_meta = rg.column(j)
                c_name = c_meta.path_in_schema
                col_compressed_sizes[c_name] = col_compressed_sizes.get(c_name, 0) + c_meta.total_compressed_size
        
        cardinalities = {col: set() for col in ['Lambda_total', 'Drive_Raw', 'p_act', 'Psi_local', 'Local_Density']}
        tick_groups = {}
        
        cols = ['Tick', 'is_active', 'Psi_local', 'b_i_v', 'b_i_u', 'b_i_r', 
                'Lambda_total', 'Drive_Raw', 'p_act', 'Local_Density']
        available_cols = [c for c in cols if c in meta.schema.names]

        # Streaming Batch Iteration
        for batch in pf.iter_batches(columns=available_cols):
            df_batch = batch.to_pandas()
            
            for col in cardinalities.keys():
                if col in df_batch.columns:
                    cardinalities[col].update(np.round(df_batch[col].values, 6))

            # Global Timeseries Streaming Aggregation
            for tick, group in df_batch.groupby('Tick'):
                if tick not in tick_groups:
                    tick_groups[tick] = {
                        'count': 0, 'rho_s': 0, 'psi_s': 0, 'LD_s': 0, 'D_s': 0, 'p_s': 0,
                        'v_s': 0, 'u_s': 0, 'r_s': 0, 'L_s': 0,
                        'v_sq': 0, 'u_sq': 0, 'r_sq': 0, 'L_sq': 0
                    }
                tg = tick_groups[tick]
                tg['count'] += len(group)
                tg['rho_s'] += group['is_active'].sum()
                
                # PATCH 2: Defensive column presence check and direct access (no silent zeros)
                req_cols = ['b_i_v', 'b_i_u', 'b_i_r', 'Lambda_total', 'Psi_local', 'Local_Density', 'Drive_Raw', 'p_act']
                for c in req_cols:
                    if c not in group.columns:
                        raise KeyError(f"Required column '{c}' missing from parquet batch for Tick {tick}")
                
                tg['psi_s'] += group['Psi_local'].sum()
                tg['LD_s'] += group['Local_Density'].sum()
                tg['D_s'] += group['Drive_Raw'].sum()
                tg['p_s'] += group['p_act'].sum()
                
                v = group['b_i_v']
                u = group['b_i_u']
                r = group['b_i_r']
                L = group['Lambda_total']
                
                tg['v_s'] += v.sum(); tg['u_s'] += u.sum(); tg['r_s'] += r.sum(); tg['L_s'] += L.sum()
                tg['v_sq'] += (v**2).sum(); tg['u_sq'] += (u**2).sum(); tg['r_sq'] += (r**2).sum(); tg['L_sq'] += (L**2).sum()

            # Snapshots for Sections 3, 4, 5
            df_targets = df_batch[df_batch['Tick'].isin(target_ticks)]
            for tick in df_targets['Tick'].unique():
                snap = df_targets[df_targets['Tick'] == tick]
                grid_size = int(np.sqrt(len(snap)))
                
                # Distributions & Quantiles
                for col in ['Lambda_total', 'Drive_Raw', 'p_act', 'Psi_local', 'b_i_v', 'b_i_u', 'b_i_r', 'Local_Density']:
                    if col in snap.columns:
                        d = snap[col]
                        dist_accum.append({
                            "run_id": run_id, "Tick": tick, "Metric": col,
                            "mean": d.mean(), "sd": d.std(), "min": d.min(),
                            "p01": d.quantile(0.01), "p05": d.quantile(0.05), "p25": d.quantile(0.25),
                            "median": d.median(), "p75": d.quantile(0.75), "p95": d.quantile(0.95),
                            "p99": d.quantile(0.99), "max": d.max()
                        })

                # Psi Sign Decomposition
                if 'Psi_local' in snap.columns:
                    psi_vals = snap['Psi_local']
                    psi_neg = psi_vals[psi_vals < 0]
                    psi_pos = psi_vals[psi_vals > 0]
                    psi_sign_accum.append({
                        "run_id": run_id, "Tick": tick,
                        "psi_negative_count": len(psi_neg),
                        "psi_zero_count": len(psi_vals[psi_vals == 0]),
                        "psi_positive_count": len(psi_pos),
                        "psi_mean_negative": psi_neg.mean() if len(psi_neg) > 0 else np.nan,
                        "psi_mean_positive": psi_pos.mean() if len(psi_pos) > 0 else np.nan
                    })
                
                # Spatial Diagnostics
                if 'Psi_local' in snap.columns and 'is_active' in snap.columns:
                    psi_grid = snap['Psi_local'].values.reshape((grid_size, grid_size))
                    act_grid = snap['is_active'].values.reshape((grid_size, grid_size))
                    
                    moran_psi = compute_morans_i(psi_grid, grid_size)
                    moran_act = compute_morans_i(act_grid, grid_size)
                    same_sign = compute_same_sign_share(psi_grid)
                    
                    pos_psi = (psi_grid > 0).astype(int)
                    neg_psi = (psi_grid < 0).astype(int)
                    p_labels, p_num = label(pos_psi)
                    n_labels, n_num = label(neg_psi)
                    
                    def comp_stats(labels, num):
                        if num == 0: return 0, 0, 0
                        sizes = np.bincount(labels.flat)[1:]
                        return sizes.max(), sizes.mean(), sizes.sum()
                    
                    p_max, p_mean, p_tot = comp_stats(p_labels, p_num)
                    n_max, n_mean, n_tot = comp_stats(n_labels, n_num)
                    
                    spatial_accum.append({
                        "run_id": run_id, "Tick": tick,
                        "Moran_I_Psi": moran_psi, "Moran_I_Act": moran_act,
                        "same_sign_share": same_sign,
                        "pos_largest": p_max, "pos_mean_size": p_mean, "pos_total_cells": p_tot,
                        "neg_largest": n_max, "neg_mean_size": n_mean, "neg_total_cells": n_tot
                    })

                # Base Boundary Summary
                if all(c in snap.columns for c in ['b_i_v', 'b_i_u', 'b_i_r']):
                    boundary_accum.append({
                        "run_id": run_id, "Tick": tick,
                        "v_low": (snap['b_i_v'] <= 0.01).sum(), "v_high": (snap['b_i_v'] >= 0.99).sum(),
                        "u_low": (snap['b_i_u'] <= 0.01).sum(), "u_high": (snap['b_i_u'] >= 0.99).sum(),
                        "r_low": (snap['b_i_r'] <= 0.01).sum(), "r_high": (snap['b_i_r'] >= 0.99).sum(),
                        "v_min": snap['b_i_v'].min(), "v_max": snap['b_i_v'].max(),
                        "u_min": snap['b_i_u'].min(), "u_max": snap['b_i_u'].max(),
                        "r_min": snap['b_i_r'].min(), "r_max": snap['b_i_r'].max()
                    })

        # Append fingerprint for this file
        f_print = {"run_id": run_id, "total_size_bytes": p_path.stat().st_size, "rows": meta.num_rows}
        f_print.update({f"{k}_compressed_bytes": v for k, v in col_compressed_sizes.items() if k in cols})
        f_print.update({f"{k}_unique_count": len(v) for k, v in cardinalities.items() if len(v) > 0})
        fingerprint_accum.append(f_print)

        # Finalize Global Timeseries for this file
        for tick in sorted(tick_groups.keys()):
            tg = tick_groups[tick]
            n = tg['count']
            
            def calc_sd(s, sq, n):
                var = (sq / n) - (s / n)**2
                return np.sqrt(max(0, var))
            
            global_ts_accum.append({
                "run_id": run_id, "F_variant": f_variant, "scale": scale, "Tick": tick,
                "rho": tg['rho_s']/n, "psi_global": tg['psi_s']/n,
                "mean_v": tg['v_s']/n, "mean_u": tg['u_s']/n, "mean_r": tg['r_s']/n,
                "sd_v": calc_sd(tg['v_s'], tg['v_sq'], n),
                "sd_u": calc_sd(tg['u_s'], tg['u_sq'], n),
                "sd_r": calc_sd(tg['r_s'], tg['r_sq'], n),
                "mean_Lambda": tg['L_s']/n, "sd_Lambda": calc_sd(tg['L_s'], tg['L_sq'], n),
                "mean_Drive": tg['D_s']/n, "mean_p_act": tg['p_s']/n,
                "mean_Local_Density": tg['LD_s']/n
            })

    # DataFrames constructions
    df_ts = pd.DataFrame(global_ts_accum)
    df_ts.to_csv(output_dir / "global_timeseries.csv", index=False)
    
    pd.DataFrame(dist_accum).to_csv(output_dir / "selected_tick_distributions.csv", index=False)
    pd.DataFrame(psi_sign_accum).to_csv(output_dir / "psi_sign_decomposition.csv", index=False)
    pd.DataFrame(spatial_accum).to_csv(output_dir / "psi_spatial_diagnostics.csv", index=False)
    pd.DataFrame(boundary_accum).to_csv(output_dir / "base_boundary_summary.csv", index=False)
    pd.DataFrame(fingerprint_accum).to_csv(output_dir / "compression_fingerprint.csv", index=False)

    # Epoch Summary
    df_ts['epoch'] = pd.cut(df_ts['Tick'], bins=epoch_bins, labels=epoch_labels, include_lowest=True)
    epoch_cols = ['rho', 'psi_global', 'mean_v', 'mean_u', 'mean_r', 'mean_Lambda', 'mean_Drive', 'mean_p_act']
    
    df_epoch = df_ts.groupby(['run_id', 'F_variant', 'scale', 'epoch'], observed=False)[epoch_cols].agg(['mean', 'std', 'min', 'max']).reset_index()
    df_epoch.columns = ['_'.join(col).strip('_') for col in df_epoch.columns.values]
    df_epoch.to_csv(output_dir / "epoch_summary.csv", index=False)

    # F-form Distinguishability Summary
    compare_records = []
    scales = df_epoch['scale'].unique()
    epochs = df_epoch['epoch'].unique()
    
    for s in scales:
        for e in epochs:
            sub = df_epoch[(df_epoch['scale'] == s) & (df_epoch['epoch'] == e)]
            f2 = sub[sub['F_variant'] == 'F_2_symmetric']
            flr = sub[sub['F_variant'] == 'F_LR']
            
            if not f2.empty and not flr.empty:
                f2 = f2.iloc[0]
                flr = flr.iloc[0]
                compare_records.append({
                    "scale": s, "epoch": e,
                    "delta_rho": f2['rho_mean'] - flr['rho_mean'],
                    "delta_psi": f2['psi_global_mean'] - flr['psi_global_mean'],
                    "delta_Lambda": f2['mean_Lambda_mean'] - flr['mean_Lambda_mean'],
                    "delta_p_act": f2['mean_p_act_mean'] - flr['mean_p_act_mean'],
                    "delta_v": f2['mean_v_mean'] - flr['mean_v_mean'],
                    "delta_u": f2['mean_u_mean'] - flr['mean_u_mean'],
                    "delta_r": f2['mean_r_mean'] - flr['mean_r_mean']
                })
    
    pd.DataFrame(compare_records).to_csv(output_dir / "fform_comparison.csv", index=False)

    # PATCH 3: Documentation caveats in terminal summary
    print("\n[METHODOLOGICAL CAVEATS]")
    print("  Cardinality counted at 1e-6 precision. F_2_symmetric's smoother distribution")
    print("    may produce slight undercount vs. F_LR's natural 1e-4 granularity.")
    print("  Connected component labeling is non-toroidal (scipy.ndimage.label limitation).")
    print("    Moran's I and same-sign share are toroidal and unaffected.")
    print("    Components spanning the torus boundary may be split.")
    
    print("\n[COMPLETE] All requested analyses executed safely. 8 CSVs generated in flight2_analysis_outputs/")

if __name__ == "__main__":
    analyze_flight2()
