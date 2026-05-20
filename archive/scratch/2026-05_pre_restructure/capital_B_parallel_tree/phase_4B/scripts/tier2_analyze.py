import argparse, gc, pandas as pd, numpy as np, pyarrow.parquet as pq
from pathlib import Path
from scipy.ndimage import label
from _phase_4b_common import verify_environment

def compute_morans_i(data, grid_size):
    z = data - np.mean(data)
    if np.std(z) == 0: return 0.0
    z_sq_sum = np.sum(z**2)
    shifts = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    w_sum = len(shifts) * (grid_size**2)
    num = sum(np.sum(z * np.roll(z, shift=(dr, dc), axis=(0, 1))) for dr, dc in shifts)
    return (grid_size**2 / w_sum) * (num / z_sq_sum)

def compute_same_sign_share(psi_grid):
    psi_sign = np.sign(psi_grid)
    shifts = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    v_pairs, s_pairs = 0, 0
    for dr, dc in shifts:
        n_sign = np.roll(psi_sign, shift=(dr, dc), axis=(0, 1))
        both_nz = (psi_sign != 0) & (n_sign != 0)
        v_pairs += np.sum(both_nz)
        s_pairs += np.sum(both_nz & (psi_sign == n_sign))
    return s_pairs / v_pairs if v_pairs > 0 else np.nan

def normalize_scale(x):
    return "20x20" if str(x) in ["20", "20x20", "20×20"] else ("40x40" if str(x) in ["40", "40x40", "40×40"] else str(x))

def compute_toroidal_clusters(binary_grid):
    lbl, num = label(binary_grid)
    if num <= 1: return lbl, num
    parent = np.arange(num + 1)
    def find(i):
        root = i
        while parent[root] != root: root = parent[root]
        curr = i
        while curr != root: nxt = parent[curr]; parent[curr] = root; curr = nxt
        return root
    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj: parent[ri] = rj
    r, c = binary_grid.shape
    for j in range(c):
        if binary_grid[0, j] and binary_grid[r - 1, j]: union(lbl[0, j], lbl[r - 1, j])
    for i in range(r):
        if binary_grid[i, 0] and binary_grid[i, c - 1]: union(lbl[i, 0], lbl[i, c - 1])
    lookup = np.array([find(i) for i in range(num + 1)])
    u_roots = np.unique(lookup[1:])
    r_to_n = {root: idx + 1 for idx, root in enumerate(u_roots)}
    r_to_n[0] = 0
    return np.array([r_to_n[lookup[i]] for i in range(num + 1)])[lbl], len(u_roots)

def run_tier2(parquet_path, output_dir):
    verify_environment()
    p_path, outdir = Path(parquet_path).resolve(), Path(output_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    print(f"--- Tier 2 Analysis Executing: {p_path.name} ---")

    target_steps = [0, 100, 500, 1000, 1500, 2000, 2500, 3000]
    epoch_bins = [-1, 99, 499, 999, 1499, 1999, 2499, 3001]
    epoch_labels = ["0-99", "100-499", "500-999", "1000-1499", "1500-1999", "2000-2499", "2500-3000"]

    global_ts_accum, dist_accum, psi_sign_accum, spatial_accum, boundary_accum, fingerprint_accum, q_effect_groups = [], [], [], [], [], [], {}
    pf = pq.ParquetFile(p_path)
    meta = pf.metadata
    c_meta = meta.metadata or {}
    f_variant = c_meta.get(b'F_variant', b'F_LR').decode()
    scale = normalize_scale(c_meta.get(b'Scale', b'20x20').decode())
    run_id = p_path.stem

    col_sizes = {}
    for i in range(meta.num_row_groups):
        rg = meta.row_group(i)
        for j in range(meta.num_columns):
            cm = rg.column(j)
            col_sizes[cm.path_in_schema] = col_sizes.get(cm.path_in_schema, 0) + cm.total_compressed_size

    cardinalities = {col: set() for col in ['Lambda_total', 'Drive_Raw', 'p_act', 'Psi_local', 'Local_Density']}
    step_groups = {}
    target_snapshots = {t: [] for t in target_steps}

    # FIXED: Added 'Agent_X' and 'Agent_Y' to stream whitelist
    cols = ['Step', 'Agent_X', 'Agent_Y', 'is_active', 'Psi_local', 'b_i_v', 'b_i_u', 'b_i_r',
            'Lambda_total', 'Drive_Raw', 'p_act', 'Local_Density', 'Delta_v', 'Delta_u', 'Delta_r']
    available_cols = [c for c in cols if c in meta.schema.names]

    for batch in pf.iter_batches(columns=available_cols):
        df_batch = batch.to_pandas()
        for col in cardinalities.keys():
            if col in df_batch.columns: cardinalities[col].update(np.round(df_batch[col].values, 6))

        for step, group in df_batch.groupby('Step'):
            if step not in step_groups:
                step_groups[step] = {'count': 0, 'rho_s': 0, 'psi_s': 0, 'LD_s': 0, 'D_s': 0, 'p_s': 0, 'v_s': 0, 'u_s': 0, 'r_s': 0, 'L_s': 0, 'v_sq': 0, 'u_sq': 0, 'r_sq': 0, 'L_sq': 0}
            tg = step_groups[step]
            tg['count'] += len(group)
            tg['rho_s'] += group['is_active'].sum()
            tg['psi_s'] += group['Psi_local'].sum()
            tg['LD_s'] += group['Local_Density'].sum()
            tg['D_s'] += group['Drive_Raw'].sum()
            tg['p_s'] += group['p_act'].sum()
            v, u, r_val, L = group['b_i_v'], group['b_i_u'], group['b_i_r'], group['Lambda_total']
            tg['v_s'] += v.sum(); tg['u_s'] += u.sum(); tg['r_s'] += r_val.sum(); tg['L_s'] += L.sum()
            tg['v_sq'] += (v**2).sum(); tg['u_sq'] += (u**2).sum(); tg['r_sq'] += (r_val**2).sum(); tg['L_sq'] += (L**2).sum()

        for step, group in df_batch[df_batch['Step'].isin(target_steps)].groupby('Step'):
            target_snapshots[step].append(group)

        if all(c in df_batch.columns for c in ['Step', 'Delta_v', 'Delta_u', 'Delta_r', 'Psi_local']):
            df_batch['epoch'] = pd.cut(df_batch['Step'], bins=epoch_bins, labels=epoch_labels, include_lowest=True)
            for ep, group in df_batch.groupby('epoch', observed=False):
                if pd.isna(ep): continue
                if ep not in q_effect_groups: q_effect_groups[ep] = {'count': 0, 'd_v': 0, 'd_u': 0, 'd_r': 0, 'psi': 0, 'pos': 0, 'neg': 0, 'zero': 0}
                qeg = q_effect_groups[ep]
                qeg['count'] += len(group); qeg['d_v'] += group['Delta_v'].sum(); qeg['d_u'] += group['Delta_u'].sum(); qeg['d_r'] += group['Delta_r'].sum(); qeg['psi'] += group['Psi_local'].sum()
                qeg['pos'] += (group['Psi_local'] > 0).sum(); qeg['neg'] += (group['Psi_local'] < 0).sum(); qeg['zero'] += (group['Psi_local'] == 0).sum()
        del df_batch; gc.collect()

    for step in target_steps:
        if not target_snapshots[step]: continue
        snap = pd.concat(target_snapshots[step], ignore_index=True)
        snap.sort_values(['Agent_X', 'Agent_Y'], inplace=True)
        grid_size = int(np.sqrt(len(snap)))
        if grid_size * grid_size != len(snap): continue

        for col in ['Lambda_total', 'Drive_Raw', 'p_act', 'Psi_local', 'b_i_v', 'b_i_u', 'b_i_r', 'Local_Density']:
            if col in snap.columns:
                d = snap[col]
                dist_accum.append({"run_id": run_id, "Step": step, "Metric": col, "mean": d.mean(), "sd": d.std(), "min": d.min(), "p01": d.quantile(0.01), "p05": d.quantile(0.05), "p25": d.quantile(0.25), "median": d.median(), "p75": d.quantile(0.75), "p95": d.quantile(0.95), "p99": d.quantile(0.99), "max": d.max()})

        if 'Psi_local' in snap.columns:
            pv = snap['Psi_local']; pn, pp = pv[pv < 0], pv[pv > 0]
            psi_sign_accum.append({"run_id": run_id, "Step": step, "psi_negative_count": len(pn), "psi_zero_count": len(pv[pv == 0]), "psi_positive_count": len(pp), "psi_mean_negative": pn.mean() if len(pn) > 0 else np.nan, "psi_mean_positive": pp.mean() if len(pp) > 0 else np.nan})

        if 'Psi_local' in snap.columns and 'is_active' in snap.columns:
            psi_grid, act_grid = snap['Psi_local'].values.reshape((grid_size, grid_size)), snap['is_active'].values.reshape((grid_size, grid_size))
            p_labels, p_num = compute_toroidal_clusters((psi_grid > 0).astype(int))
            n_labels, n_num = compute_toroidal_clusters((psi_grid < 0).astype(int))
            def comp_stats(lbls, num):
                if num == 0: return 0, 0, 0
                szs = np.bincount(lbls.flat)[1:]
                return szs.max(), szs.mean(), szs.sum()
            p_max, p_mean, p_tot = comp_stats(p_labels, p_num)
            n_max, n_mean, n_tot = comp_stats(n_labels, n_num)
            spatial_accum.append({"run_id": run_id, "Step": step, "Moran_I_Psi": compute_morans_i(psi_grid, grid_size), "Moran_I_Act": compute_morans_i(act_grid, grid_size), "same_sign_share": compute_same_sign_share(psi_grid), "pos_largest": p_max, "pos_mean_size": p_mean, "pos_total_cells": p_tot, "neg_largest": n_max, "neg_mean_size": n_mean, "neg_total_cells": n_tot})

        if all(c in snap.columns for c in ['b_i_v', 'b_i_u', 'b_i_r']):
            boundary_accum.append({"run_id": run_id, "Step": step, "v_low": (snap['b_i_v'] <= 0.01).sum(), "v_high": (snap['b_i_v'] >= 0.99).sum(), "u_low": (snap['b_i_u'] <= 0.01).sum(), "u_high": (snap['b_i_u'] >= 0.99).sum(), "r_low": (snap['b_i_r'] <= 0.01).sum(), "r_high": (snap['b_i_r'] >= 0.99).sum(), "v_min": snap['b_i_v'].min(), "v_max": snap['b_i_v'].max(), "u_min": snap['b_i_u'].min(), "u_max": snap['b_i_u'].max(), "r_min": snap['b_i_r'].min(), "r_max": snap['b_i_r'].max()})

    f_print = {"run_id": run_id, "total_size_bytes": p_path.stat().st_size, "rows": meta.num_rows}
    f_print.update({f"{k}_compressed_bytes": v for k, v in col_sizes.items() if k in cols})
    f_print.update({f"{k}_unique_count": len(v) for k, v in cardinalities.items() if len(v) > 0})
    fingerprint_accum.append(f_print)

    for step in sorted(step_groups.keys()):
        tg = step_groups[step]; n = tg['count']
        def c_sd(s, sq, n): return np.sqrt(max(0, (sq / n) - (s / n)**2))
        global_ts_accum.append({"run_id": run_id, "F_variant": f_variant, "scale": scale, "Step": step, "rho": tg['rho_s']/n, "psi_global": tg['psi_s']/n, "mean_v": tg['v_s']/n, "mean_u": tg['u_s']/n, "mean_r": tg['r_s']/n, "sd_v": c_sd(tg['v_s'], tg['v_sq'], n), "sd_u": c_sd(tg['u_s'], tg['u_sq'], n), "sd_r": c_sd(tg['r_s'], tg['r_sq'], n), "mean_Lambda": tg['L_s']/n, "sd_Lambda": c_sd(tg['L_s'], tg['L_sq'], n), "mean_Drive": tg['D_s']/n, "mean_p_act": tg['p_s']/n, "mean_Local_Density": tg['LD_s']/n})

    df_ts = pd.DataFrame(global_ts_accum); df_ts.to_csv(outdir / f"global_timeseries_{run_id}.csv", index=False)
    pd.DataFrame(dist_accum).to_csv(outdir / f"selected_tick_distributions_{run_id}.csv", index=False)
    pd.DataFrame(psi_sign_accum).to_csv(outdir / f"psi_sign_decomposition_{run_id}.csv", index=False)
    pd.DataFrame(spatial_accum).to_csv(outdir / f"psi_spatial_diagnostics_{run_id}.csv", index=False)
    pd.DataFrame(boundary_accum).to_csv(outdir / f"base_boundary_summary_{run_id}.csv", index=False)
    pd.DataFrame(fingerprint_accum).to_csv(outdir / f"compression_fingerprint_{run_id}.csv", index=False)

    df_ts['epoch'] = pd.cut(df_ts['Step'], bins=epoch_bins, labels=epoch_labels, include_lowest=True)
    df_epoch = df_ts.groupby(['run_id', 'F_variant', 'scale', 'epoch'], observed=False)[['rho', 'psi_global', 'mean_v', 'mean_u', 'mean_r', 'mean_Lambda', 'mean_Drive', 'mean_p_act']].agg(['mean', 'std', 'min', 'max']).reset_index()
    df_epoch.columns = ['_'.join(col).strip('_') for col in df_epoch.columns.values]
    df_epoch.to_csv(outdir / f"epoch_summary_{run_id}.csv", index=False)

    q_acc = []
    for ep in sorted(q_effect_groups.keys()):
        qeg = q_effect_groups[ep]; n = qeg['count']
        if n > 0: q_acc.append({'F_variant': f_variant, 'scale': scale, 'epoch': ep, 'mean_Delta_v': qeg['d_v']/n, 'mean_Delta_u': qeg['d_u']/n, 'mean_Delta_r': qeg['d_r']/n, 'mean_Psi_local': qeg['psi']/n, 'pos_Psi_share': qeg['pos']/n, 'neg_Psi_share': qeg['neg']/n, 'zero_Psi_share': qeg['zero']/n})
    pd.DataFrame(q_acc).to_csv(outdir / f"q_effect_decomposition_{run_id}.csv", index=False)
    print("\n[METHODOLOGICAL CAVEATS]\n  Cardinality counted at 1e-6 precision.\n  Connected component labeling is fully TOROIDAL.")
    print(f"\n[COMPLETE] Tier 2 analysis executed safely with Toroidal Patching for {run_id}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--parquet', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    run_tier2(args.parquet, args.output_dir)