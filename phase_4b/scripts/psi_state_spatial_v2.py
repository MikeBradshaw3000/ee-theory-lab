"""
Psi_state_spatial v2 â€” Coherence Observable Design & Control Testing
Computes the co-equal state-based spatial observables (Psi_meanI_state, Psi_persistence_I)
with steady-state window scanning, permutation nulls, and synthetic discrimination tests.
"""

import argparse
import pandas as pd
import numpy as np
import scipy.stats
import scipy.ndimage
from pathlib import Path

# --- CORE MATH & VECTORIZED OBSERVABLES ---

def batch_morans_i(grids):
    """
    Vectorized, density-adjusted Moran's I over an array of 2D grids.
    Centers data by mean to adjust for rho.
    Shape of grids: (N, xs, xs) or (xs, xs) for a single grid.
    Returns: 1D array of Moran's I values of length N, or a single float.
    """
    is_single = False
    if grids.ndim == 2:
        is_single = True
        grids = grids[np.newaxis, :, :]

    N, xs, ys = grids.shape
    if xs != ys:
        raise ValueError(f"batch_morans_i requires square grids, got {xs}x{ys}")

    means = np.mean(grids, axis=(1,2), keepdims=True)
    z = grids - means
    z_sq_sum = np.sum(z**2, axis=(1,2))

    # Epsilon thresholding: if variance is computationally zero, it's a uniform grid.
    # Moran's I is undefined/degenerate here; we strictly return 0.0.
    valid = z_sq_sum > 1e-12

    res = np.zeros(N)
    if not np.any(valid):
        return float(res[0]) if is_single else res

    z_valid = z[valid]
    shifts = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    w_sum = len(shifts) * (xs**2)

    num = np.zeros(np.sum(valid))
    for dr, dc in shifts:
        num += np.sum(z_valid * np.roll(z_valid, shift=(dr, dc), axis=(1, 2)), axis=(1, 2))

    res[valid] = (xs**2 / w_sum) * (num / z_sq_sum[valid])

    return float(res[0]) if is_single else res

def compute_permutation_z(statistic_val, null_dist):
    """Returns (z_score, null_mean, null_sd)."""
    null_mean = np.mean(null_dist)
    null_sd = np.std(null_dist)
    if null_sd == 0:
        return 0.0, null_mean, null_sd
    return (statistic_val - null_mean) / null_sd, null_mean, null_sd


def _validate_and_reshape_grid(df, xs, col='is_active', W=1):
    """
    Strict validation to prevent silent reshaping of malformed telemetry.
    Fails fast on coordinate mismatch, missing cells, or duplicates.
    """
    x_unique = df['Agent_X'].nunique()
    y_unique = df['Agent_Y'].nunique()
    
    if x_unique != y_unique:
        raise ValueError(f"Grid malformed: Agent_X unique ({x_unique}) != Agent_Y unique ({y_unique}).")
    if x_unique != xs:
        raise ValueError(f"Grid malformed: expected Agent_X unique count {xs}; got {x_unique}.")
    
    expected_rows = W * xs * xs
    if len(df) != expected_rows:
        raise ValueError(f"Grid malformed: Expected {expected_rows} rows for W={W}, xs={xs}. Got {len(df)}.")
        
    if df.duplicated(subset=['Tick', 'Agent_X', 'Agent_Y']).any():
        raise ValueError("Grid malformed: Duplicate cell coordinates detected in tick/window.")
        
    df_sorted = df.sort_values(['Tick', 'Agent_X', 'Agent_Y'])
    return df_sorted[col].values.reshape((W, xs, xs))

# --- WINDOW & OBSERVABLE LOGIC ---

def process_window(window_df, xs, N_perms=199):
    """
    Computes diagnostics, both observables, and permutation nulls for a single time window.
    """
    W = window_df['Tick'].nunique()
    act_grids = _validate_and_reshape_grid(window_df, xs, col='is_active', W=W)
    
    # -- Density Trajectory Stats --
    rho_per_tick = np.mean(act_grids, axis=(1, 2))
    ticks = np.arange(W)
    slope, _, _, _, _ = scipy.stats.linregress(ticks, rho_per_tick)
    
    rho_mean = np.mean(rho_per_tick)
    rho_min = np.min(rho_per_tick)
    rho_max = np.max(rho_per_tick)
    
    if rho_mean == 0:
        return None  # Empty space, trivially unorganized.
        
    stats = {
        'rho_mean': rho_mean,
        'rho_sd': np.std(rho_per_tick),
        'rho_cv': np.std(rho_per_tick) / rho_mean,
        'rho_min': rho_min,
        'rho_max': rho_max,
        'rho_range_over_mean': (rho_max - rho_min) / rho_mean,
        'slope': slope,
        'relative_drift': abs(slope * W) / rho_mean
    }
    
    # Transparent Earned-Window Filters (flags, not hard exclusions).
    stats['steady_state_candidate'] = (
        (stats['relative_drift'] < 0.05) and
        (stats['rho_cv'] < 0.15) and
        (stats['rho_range_over_mean'] < 0.30)
    )
    
    # -- Co-Equal Observable 1: Psi_meanI_state --
    per_tick_I = batch_morans_i(act_grids)
    Psi_meanI_state = np.mean(per_tick_I)
    
    flat_act = act_grids.reshape(W, xs * xs)
    null_meanI = np.zeros(N_perms)
    for i in range(N_perms):
        idx = np.random.rand(W, xs * xs).argsort(axis=1)  # Independent shuffle per tick.
        shuffled = np.take_along_axis(flat_act, idx, axis=1).reshape(W, xs, xs)
        null_meanI[i] = np.mean(batch_morans_i(shuffled))
        
    z_meanI, e_meanI, sd_meanI = compute_permutation_z(Psi_meanI_state, null_meanI)
    stats.update({
        'Psi_meanI_state': Psi_meanI_state,
        'Psi_meanI_state_z': z_meanI,
        'Psi_meanI_state_null_E': e_meanI,
        'Psi_meanI_state_null_SD': sd_meanI
    })

    # -- Co-Equal Observable 2: Psi_persistence_I --
    P_grid = np.mean(act_grids, axis=0)
    Psi_persistence_I = batch_morans_i(P_grid)
    
    flat_P = P_grid.reshape(xs * xs)
    shuffled_Ps = np.array([np.random.permutation(flat_P).reshape(xs, xs) for _ in range(N_perms)])
    null_P_Is = batch_morans_i(shuffled_Ps)
    
    z_persI, e_persI, sd_persI = compute_permutation_z(Psi_persistence_I, null_P_Is)
    stats.update({
        'Psi_persistence_I': Psi_persistence_I,
        'Psi_persistence_I_z': z_persI,
        'Psi_persistence_I_null_E': e_persI,
        'Psi_persistence_I_null_SD': sd_persI
    })
    
    # -- Persistence Heterogeneity Diagnostics --
    p_mask = (P_grid >= 0.8).astype(int)
    labels, num_features = scipy.ndimage.label(p_mask)
    largest_comp = 0
    if num_features > 0:
        largest_comp = np.bincount(labels.flat)[1:].max() / (xs * xs)
        
    stats.update({
        'P_mean': np.mean(P_grid),
        'P_std': np.std(P_grid),
        'P_min': np.min(P_grid),
        'P_max': np.max(P_grid),
        'P_q25': np.percentile(P_grid, 25),
        'P_q50': np.percentile(P_grid, 50),
        'P_q75': np.percentile(P_grid, 75),
        'share_P_gt_0.5': np.mean(P_grid >= 0.5),
        'share_P_gt_0.8': np.mean(P_grid >= 0.8),
        'share_P_gt_0.95': np.mean(P_grid >= 0.95),
        'largest_component_P_gt_0.8': largest_comp
    })
    
    return stats

# --- SYNTHETIC POSITIVE-CONTROL GENERATOR ---

def get_exact_random_grid(xs, active_count):
    """Returns an xs by xs grid with EXACTLY active_count cells set to 1."""
    flat = np.zeros(xs * xs)
    flat[:active_count] = 1
    np.random.shuffle(flat)
    return flat.reshape((xs, xs))


def run_synthetic_controls(output_dir: Path, N_perms=199):
    output_dir.mkdir(parents=True, exist_ok=True)
    print("\nExecuting Synthetic Positive-Control Generator (Exact Rho Sampling)...")
    W = 100
    xs = 20
    
    # Case A: Stable localized cluster (block of 49 active cells; rho = 0.1225).
    grid_A = np.zeros((W, xs, xs))
    grid_A[:, 5:12, 5:12] = 1
    active_count_A = 49
    
    # Case B: Random at exact same rho (exactly 49 active cells per tick).
    grid_B = np.array([get_exact_random_grid(xs, active_count_A) for _ in range(W)])
    
    # Case C: High-rho unstructured (exactly 320 active cells per tick; rho = 0.8).
    grid_C = np.array([get_exact_random_grid(xs, 320) for _ in range(W)])
    
    # Case D: Transient synchronized-switching wave (moving 3-column block, 60 cells).
    grid_D = np.zeros((W, xs, xs))
    for t in range(W):
        col = t % xs
        grid_D[t, :, col:(col + 3)] = 1
        if col + 3 > xs:  # Wrap.
            grid_D[t, :, 0:((col + 3) - xs)] = 1
            
    # Case E: Spatially uniform high persistence (exactly P_i = 0.70 for all cells).
    # Give every cell exactly 70 ones and 30 zeros, independently shuffled.
    cell_timelines = np.zeros((xs * xs, W))
    for i in range(xs * xs):
        timeline = np.zeros(W)
        timeline[:70] = 1
        np.random.shuffle(timeline)
        cell_timelines[i] = timeline
    grid_E = cell_timelines.T.reshape((W, xs, xs))

    cases = {
        'Case_A_Stable_Cluster': {
            'grid': grid_A,
            'expected_pattern': "Stable contiguous block",
            'expected_Psi_meanI_state': "High positive",
            'expected_Psi_persistence_I': "High positive",
            'expected_P_std': "High (>0.3)",
            'control_purpose': "Positive control for true structural coherence"
        },
        'Case_B_Random_Same_Rho': {
            'grid': grid_B,
            'expected_pattern': f"Random noise at exact rho={active_count_A/(xs*xs)}",
            'expected_Psi_meanI_state': "~0",
            'expected_Psi_persistence_I': "~0",
            'expected_P_std': "~0",
            'control_purpose': "Negative control (random low-rho)"
        },
        'Case_C_High_Rho_Unstructured': {
            'grid': grid_C,
            'expected_pattern': "Random noise at exact rho=0.80",
            'expected_Psi_meanI_state': "~0",
            'expected_Psi_persistence_I': "~0",
            'expected_P_std': "~0",
            'control_purpose': "Negative control (random high-rho)"
        },
        'Case_D_Transient_Wave': {
            'grid': grid_D,
            'expected_pattern': "Moving wave",
            'expected_Psi_meanI_state': "High positive",
            'expected_Psi_persistence_I': "~0",
            'expected_P_std': "Low",
            'control_purpose': "Test divergence on transient vs persistent structure"
        },
        'Case_E_Uniform_High_Persistence': {
            'grid': grid_E,
            'expected_pattern': "Uniform exact persistence P_i=0.7",
            'expected_Psi_meanI_state': "~0",
            'expected_Psi_persistence_I': "~0",
            'expected_P_std': "Exactly 0",
            'control_purpose': "Degeneracy check (misreading uniform P as incoherence)"
        }
    }
    
    records = []
    for case_name, data in cases.items():
        print(f"  Evaluating {case_name}...")
        df_list = []
        for t in range(W):
            x, y = np.meshgrid(np.arange(xs), np.arange(xs), indexing='ij')
            df_t = pd.DataFrame({
                'Tick': t,
                'Agent_X': x.flatten(),
                'Agent_Y': y.flatten(),
                'is_active': data['grid'][t].flatten()
            })
            df_list.append(df_t)
            
        case_df = pd.concat(df_list)
        stats = process_window(case_df, xs, N_perms)
        if stats:
            # Prepend interpretation labels and case metadata.
            full_record = {
                'Case': case_name,
                'control_purpose': data['control_purpose'],
                'expected_pattern': data['expected_pattern'],
                'expected_Psi_meanI_state': data['expected_Psi_meanI_state'],
                'expected_Psi_persistence_I': data['expected_Psi_persistence_I'],
                'expected_P_std': data['expected_P_std'],
                **stats
            }
            records.append(full_record)
            
    pd.DataFrame(records).to_csv(output_dir / "synthetic_controls_summary.csv", index=False)
    print(f"Synthetic controls saved to {output_dir / 'synthetic_controls_summary.csv'}")

# --- MAIN SUBSTRATE ORCHESTRATION ---

def run_coherence_extraction(parquet_file: Path, output_dir: Path, window_lengths: list, stride: int, N_perms: int):
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = parquet_file.stem
    print(f"\nLoading Substrate: {parquet_file.name}")
    
    df = pd.read_parquet(parquet_file, columns=['Tick', 'Agent_X', 'Agent_Y', 'is_active', 'Psi_local'])
    xs = df['Agent_X'].nunique()
    max_tick = df['Tick'].max()

    # 1. Full-run sampled diagnostic timeseries (resolution = 10 ticks).
    print("Computing sampled diagnostic timeseries...")
    ts_records = []
    for t in range(0, max_tick + 1, 10):
        t_df = df[df['Tick'] == t]
        if t_df.empty:
            continue
        
        act_grid = _validate_and_reshape_grid(t_df, xs, col='is_active', W=1)
        psi_grid = _validate_and_reshape_grid(t_df, xs, col='Psi_local', W=1)
        
        ts_records.append({
            "run_id": run_id,
            "Tick": t,
            "rho": np.mean(act_grid),
            "Moran_I_Act_Instant": batch_morans_i(act_grid),
            "Moran_I_Psi_Instant_RefOnly": batch_morans_i(psi_grid)
        })
    pd.DataFrame(ts_records).to_csv(output_dir / f"sampled_timeseries_{run_id}.csv", index=False)

    # 2. Window-scan table.
    print(f"Executing rolling window scan (W={window_lengths}, Stride={stride})...")
    scan_records = []
    
    for W in window_lengths:
        # Guarantee final window is evaluated even if stride skips it.
        starts = list(range(0, max_tick - W + 2, stride))
        final_start = max_tick - W + 1
        if final_start >= 0 and (not starts or starts[-1] != final_start):
            starts.append(final_start)

        for start_t in starts:
            end_t = start_t + W - 1
            w_df = df[(df['Tick'] >= start_t) & (df['Tick'] <= end_t)]
            
            if w_df['Tick'].nunique() < W * 0.95:
                continue
                
            stats = process_window(w_df, xs, N_perms)
            if stats:
                stats['run_id'] = run_id
                stats['window_start'] = start_t
                stats['window_end'] = end_t
                stats['W'] = W
                scan_records.append(stats)
                
    if scan_records:
        scan_df = pd.DataFrame(scan_records)
        cols = ['run_id', 'window_start', 'window_end', 'W', 'steady_state_candidate'] + [
            c for c in scan_df.columns if c not in ['run_id', 'window_start', 'window_end', 'W', 'steady_state_candidate']
        ]
        scan_df[cols].to_csv(output_dir / f"window_scan_{run_id}.csv", index=False)
        
        candidates = scan_df['steady_state_candidate'].sum()
        print(f"Scan complete. Found {candidates} candidate steady-state windows out of {len(scan_df)} evaluated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet", type=Path, help="Target substrate file (required unless --controls-only)")
    parser.add_argument("--output-dir", type=Path, default=Path("."), help="Output directory")
    parser.add_argument("--window-lengths", type=int, nargs='+', default=[250, 500, 750], help="Lengths for rolling scan")
    parser.add_argument("--stride", type=int, default=100, help="Step size between rolling windows")
    parser.add_argument("--perm-n", type=int, default=199, help="Number of permutations for null models")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--controls-only", action='store_true', help="Run only the synthetic positive-control suite")
    
    args = parser.parse_args()
    
    np.random.seed(args.seed)
    
    if args.controls_only:
        run_synthetic_controls(args.output_dir, args.perm_n)
    else:
        if not args.parquet:
            raise ValueError("Must provide --parquet unless running --controls-only")
        run_coherence_extraction(args.parquet, args.output_dir, args.window_lengths, args.stride, args.perm_n)
        run_synthetic_controls(args.output_dir, args.perm_n)
