"""
Third V8 diagnostic: test specific tick-0 Psi formulas against the data.
Read-only. Not committed.
"""
import pandas as pd
import numpy as np
from pathlib import Path

PARQUET = Path(r"C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\flight6_probe1_overcrowding_20x20.parquet")

df = pd.read_parquet(PARQUET)
df = df.sort_values(['Tick', 'Agent_X', 'Agent_Y']).reset_index(drop=True)

eps_alg = 1e-10
ticks = df['Tick'].nunique()
xs = df['Agent_X'].nunique()
ys = df['Agent_Y'].nunique()

is_act_3d = df['is_active'].values.reshape((ticks, xs, ys)).astype(int)
psi_3d = df['Psi_local'].to_numpy().reshape(ticks, xs, ys)

# Compute sum of active neighbors at tick 0
grid0 = is_act_3d[0].astype(float)
n_sum_active = (np.roll(grid0, 1, 0) + np.roll(grid0, -1, 0) + 
                np.roll(grid0, 1, 1) + np.roll(grid0, -1, 1) + 
                np.roll(np.roll(grid0, 1, 0), 1, 1) + np.roll(np.roll(grid0, 1, 0), -1, 1) + 
                np.roll(np.roll(grid0, -1, 0), 1, 1) + np.roll(np.roll(grid0, -1, 0), -1, 1))

psi_actual = psi_3d[0]

print("=== Test formulas for Psi_local at tick 0 ===\n")

# Formula A: Psi = (1 - 2*is_active) * sum_active_neighbors
# Inactive (is_active=0): Psi = 1 * sum = +sum
# Active (is_active=1): Psi = -1 * sum = -sum
psi_calc_A = (1.0 - 2.0 * grid0) * n_sum_active
diff_A = np.abs(psi_actual - psi_calc_A)
fails_A = int((diff_A > eps_alg).sum())
print(f"Formula A: Psi = (1 - 2*is_active) * sum(active neighbors)")
print(f"  Fails: {fails_A} / {xs*ys}")
print(f"  Max diff: {diff_A.max():.6e}\n")

# Formula B: Psi = (2*is_active - 1) * sum_active_neighbors (opposite sign)
psi_calc_B = (2.0 * grid0 - 1.0) * n_sum_active
diff_B = np.abs(psi_actual - psi_calc_B)
fails_B = int((diff_B > eps_alg).sum())
print(f"Formula B: Psi = (2*is_active - 1) * sum(active neighbors)")
print(f"  Fails: {fails_B} / {xs*ys}")
print(f"  Max diff: {diff_B.max():.6e}\n")

# Formula C: Psi = sum_active_neighbors (no sign flip)
diff_C = np.abs(psi_actual - n_sum_active)
fails_C = int((diff_C > eps_alg).sum())
print(f"Formula C: Psi = sum(active neighbors), no sign")
print(f"  Fails: {fails_C} / {xs*ys}")
print(f"  Max diff: {diff_C.max():.6e}\n")

# Formula D: maybe the substrate uses ds = is_active - p_act at tick 0 (mean-zero residual)
# This would make Psi = (is_active - p_act) * sum_active_neighbors
# Check this
p_act_0 = df[df['Tick']==0].sort_values(['Agent_X', 'Agent_Y'])['p_act'].values.reshape((xs, ys))
ds_residual = grid0 - p_act_0
psi_calc_D = ds_residual * n_sum_active
diff_D = np.abs(psi_actual - psi_calc_D)
fails_D = int((diff_D > eps_alg).sum())
print(f"Formula D: Psi = (is_active - p_act) * sum(active neighbors)")
print(f"  Fails: {fails_D} / {xs*ys}")
print(f"  Max diff: {diff_D.max():.6e}\n")

# Formula E: Psi = (is_active - p_act) * sum(is_active - p_act of neighbors)
# Maybe the substrate uses centered residuals on both sides
ds_3d_residual = (is_act_3d - df.sort_values(['Tick', 'Agent_X', 'Agent_Y'])['p_act'].values.reshape((ticks, xs, ys)))
ds_0_res = ds_3d_residual[0]
n_sum_res = (np.roll(ds_0_res, 1, 0) + np.roll(ds_0_res, -1, 0) + 
             np.roll(ds_0_res, 1, 1) + np.roll(ds_0_res, -1, 1) + 
             np.roll(np.roll(ds_0_res, 1, 0), 1, 1) + np.roll(np.roll(ds_0_res, 1, 0), -1, 1) + 
             np.roll(np.roll(ds_0_res, -1, 0), 1, 1) + np.roll(np.roll(ds_0_res, -1, 0), -1, 1))
psi_calc_E = ds_0_res * n_sum_res
diff_E = np.abs(psi_actual - psi_calc_E)
fails_E = int((diff_E > eps_alg).sum())
print(f"Formula E: Psi = (is_active - p_act) * sum((is_active - p_act) of neighbors)")
print(f"  Fails: {fails_E} / {xs*ys}")
print(f"  Max diff: {diff_E.max():.6e}\n")

# Show samples for the best-fitting formula
formulas = [('A', fails_A, psi_calc_A), ('B', fails_B, psi_calc_B), ('C', fails_C, n_sum_active), ('D', fails_D, psi_calc_D), ('E', fails_E, psi_calc_E)]
best = min(formulas, key=lambda x: x[1])
print(f"=== Best fitting formula: {best[0]} with {best[1]} fails ===")
if best[1] > 0:
    print(f"Sample mismatches under formula {best[0]}:")
    diff_best = np.abs(psi_actual - best[2])
    fail_locs = np.argwhere(diff_best > eps_alg)
    for loc in fail_locs[:5]:
        x, y = loc
        print(f"  ({x},{y}): is_active={int(grid0[x,y])}, actual_Psi={psi_actual[x,y]:.6f}, predicted_Psi={best[2][x,y]:.6f}, active_neighbors={n_sum_active[x,y]:.0f}")

# Sanity print: at the (0,15) cell where is_active=1 and Psi=-3
print(f"\n=== Sanity check at (0,15) ===")
print(f"  is_active: {int(grid0[0,15])}")
print(f"  p_act: {p_act_0[0,15]:.6f}")
print(f"  Psi_local actual: {psi_actual[0,15]:.6f}")
print(f"  sum(active neighbors): {n_sum_active[0,15]:.0f}")
print(f"  Formula A predict (1-2*is_act)*sum: {(1.0-2.0*grid0[0,15])*n_sum_active[0,15]:.6f}")
print(f"  Formula D predict (is_act-p_act)*sum: {(grid0[0,15]-p_act_0[0,15])*n_sum_active[0,15]:.6f}")
print(f"  Formula E predict (is_act-p_act)*sum(neighbors_residual): {psi_calc_E[0,15]:.6f}")
