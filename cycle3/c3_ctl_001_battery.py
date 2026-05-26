import numpy as np
import pandas as pd
import os

# ==========================================
# C3-CTL-001: Synthetic Control Battery
# Topology: 50x50, Toroidal, Moore Radius 1
# ==========================================

GRID_SIZE = 50
N_CELLS = GRID_SIZE * GRID_SIZE
TICKS = 100
PERMUTATIONS = 199

def calculate_morans_i_toroidal_8(grid):
    """
    Computes Moran's I for a single 2D grid using 8-neighbor
    (Moore radius 1) toroidal (wrapping) adjacency.
    """
    grid_mean = np.mean(grid)
    grid_var = np.var(grid)

    # Degeneracy guard
    if grid_var < 1e-9:
        return 0.0

    centered = grid - grid_mean

    w_sum = (
        np.roll(centered, 1, axis=0) + np.roll(centered, -1, axis=0) +
        np.roll(centered, 1, axis=1) + np.roll(centered, -1, axis=1) +
        np.roll(np.roll(centered, 1, axis=0), 1, axis=1) +
        np.roll(np.roll(centered, 1, axis=0), -1, axis=1) +
        np.roll(np.roll(centered, -1, axis=0), 1, axis=1) +
        np.roll(np.roll(centered, -1, axis=0), -1, axis=1)
    )

    numerator = np.sum(centered * w_sum)
    denominator = np.sum(centered**2)

    return (1.0 / 8.0) * (numerator / denominator)

def batch_morans_i_toroidal_8(grids):
    """
    Vectorized Moran's I for a 3D array (ticks, height, width).
    Used to rapidly compute the per-tick null distributions.
    """
    grid_mean = np.mean(grids, axis=(1, 2), keepdims=True)
    grid_var = np.var(grids, axis=(1, 2), keepdims=True)

    valid_mask = np.squeeze(grid_var) > 1e-9
    if not np.any(valid_mask):
        return np.zeros(grids.shape[0])

    centered = grids - grid_mean

    w_sum = (
        np.roll(centered, 1, axis=1) + np.roll(centered, -1, axis=1) +
        np.roll(centered, 1, axis=2) + np.roll(centered, -1, axis=2) +
        np.roll(np.roll(centered, 1, axis=1), 1, axis=2) +
        np.roll(np.roll(centered, 1, axis=1), -1, axis=2) +
        np.roll(np.roll(centered, -1, axis=1), 1, axis=2) +
        np.roll(np.roll(centered, -1, axis=1), -1, axis=2)
    )

    numerator = np.sum(centered * w_sum, axis=(1, 2))
    denominator = np.sum(centered**2, axis=(1, 2))

    I_vals = np.zeros(grids.shape[0])
    np.divide(numerator, denominator, out=I_vals, where=valid_mask)
    return (1.0 / 8.0) * I_vals

def compute_persistence_null(grid, actual_I, num_permutations=PERMUTATIONS):
    """Permutation null for the time-averaged persistence map."""
    if np.var(grid) < 1e-9:
        return 0.0, 0.0

    flat_grid = grid.flatten()
    null_Is = np.zeros(num_permutations)

    for i in range(num_permutations):
        shuffled = np.random.permutation(flat_grid).reshape((GRID_SIZE, GRID_SIZE))
        null_Is[i] = calculate_morans_i_toroidal_8(shuffled)

    null_mean = np.mean(null_Is)
    null_std = np.std(null_Is)

    z_score = (actual_I - null_mean) / null_std if null_std > 1e-9 else 0.0
    return z_score, null_std

def compute_meanI_state_null(actual_grids, actual_meanI, num_permutations=PERMUTATIONS):
    """
    Permutation null for the per-tick state organization.
    Shuffles per-cell values WITHIN each tick, preserving exact tick density.
    """
    null_meanIs = np.zeros(num_permutations)
    ticks, h, w = actual_grids.shape
    flat_grids = actual_grids.reshape(ticks, -1)

    for p in range(num_permutations):
        # Generate random indices to shuffle each tick independently
        rand_idx = np.random.rand(ticks, h * w).argsort(axis=1)
        shuffled_flat = np.take_along_axis(flat_grids, rand_idx, axis=1)
        shuffled_grids = shuffled_flat.reshape(ticks, h, w)

        tick_Is = batch_morans_i_toroidal_8(shuffled_grids)
        null_meanIs[p] = np.mean(tick_Is)

    null_mean = np.mean(null_meanIs)
    null_std = np.std(null_meanIs)

    z_score = (actual_meanI - null_mean) / null_std if null_std > 1e-9 else 0.0
    return z_score, null_std

# ==========================================
# Case Generators
# ==========================================

def generate_case_A():
    """Case A: Stable Cluster (Positive Control). rho = 0.10."""
    grids = np.zeros((TICKS, GRID_SIZE, GRID_SIZE), dtype=int)
    grids[:, :10, :25] = 1
    return grids

def generate_case_B():
    """Case B: Random Low-rho (Negative Control). Exact rho = 0.10."""
    grids = np.zeros((TICKS, GRID_SIZE, GRID_SIZE), dtype=int)
    for t in range(TICKS):
        flat = np.zeros(N_CELLS, dtype=int)
        flat[:250] = 1
        np.random.shuffle(flat)
        grids[t] = flat.reshape((GRID_SIZE, GRID_SIZE))
    return grids

def generate_case_C():
    """Case C: Random High-rho (Negative Control). Exact rho = 0.80."""
    grids = np.zeros((TICKS, GRID_SIZE, GRID_SIZE), dtype=int)
    for t in range(TICKS):
        flat = np.zeros(N_CELLS, dtype=int)
        flat[:2000] = 1
        np.random.shuffle(flat)
        grids[t] = flat.reshape((GRID_SIZE, GRID_SIZE))
    return grids

def generate_case_D():
    """Case D: Transient Wave (Divergence Case). rho = 0.10."""
    grids = np.zeros((TICKS, GRID_SIZE, GRID_SIZE), dtype=int)
    base = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    base[:, :5] = 1
    for t in range(TICKS):
        grids[t] = np.roll(base, t, axis=1)
    return grids

def generate_case_E():
    """
    Case E: Uniform High Persistence (Degeneracy Control).
    Every cell active exactly 70 of 100 ticks, independently shuffled.
    """
    cell_histories = np.zeros((N_CELLS, TICKS), dtype=int)
    for i in range(N_CELLS):
        seq = np.array([1]*70 + [0]*30)
        np.random.shuffle(seq)
        cell_histories[i] = seq

    grids = cell_histories.T.reshape((TICKS, GRID_SIZE, GRID_SIZE))
    return grids

# ==========================================
# Execution and Analytics Pipeline
# ==========================================

def run_battery():
    cases = {
        "A_Stable_Cluster": generate_case_A(),
        "B_Random_Low_Rho": generate_case_B(),
        "C_Random_High_Rho": generate_case_C(),
        "D_Transient_Wave": generate_case_D(),
        "E_Uniform_Persistence": generate_case_E()
    }

    results = []

    for case_name, grids in cases.items():
        # 1. Per-tick active-state metrics & grid-local null
        tick_rhos = [np.mean(grid) for grid in grids]
        tick_Is = batch_morans_i_toroidal_8(grids)

        rho_mean = np.mean(tick_rhos)
        psi_meanI_state = np.mean(tick_Is)

        meanI_z, _ = compute_meanI_state_null(grids, psi_meanI_state)

        # 2. Persistence metrics & grid-local null
        persistence_grid = np.mean(grids, axis=0)
        p_std = np.std(persistence_grid)

        psi_persistence_I = calculate_morans_i_toroidal_8(persistence_grid)
        persistence_z, _ = compute_persistence_null(persistence_grid, psi_persistence_I)

        results.append({
            "Case": case_name,
            "Mean_Rho": round(rho_mean, 4),
            "Psi_meanI_state": round(psi_meanI_state, 4),
            "MeanI_Z": round(meanI_z, 2),
            "Psi_persistence_I": round(psi_persistence_I, 4),
            "P_std": round(p_std, 4),
            "Persistence_Z": round(persistence_z, 2)
        })

    df_results = pd.DataFrame(results)

    # Route output to cycle3 directory
    output_dir = os.path.join("cycle3", "data_out")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "c3_ctl_001_results.csv")
    df_results.to_csv(out_path, index=False)

    print("\n--- C3-CTL-001 Battery Execution Complete ---")
    print(df_results.to_string(index=False))
    print(f"\nResults saved to {out_path}")

if __name__ == "__main__":
    np.random.seed(42)
    run_battery()
