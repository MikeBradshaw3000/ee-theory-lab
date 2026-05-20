"""
Extended V8 diagnostic: test hypothesis that ds_3d[0] = is_active[0]
(rather than 0), making the 187 nonzero tick-0 Psi_local values reconstructable.
Read-only. Not committed to canonical record.
"""
import pandas as pd
import numpy as np
from pathlib import Path

PARQUET = Path(r"C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\flight6_probe1_overcrowding_20x20.parquet")

print(f"Loading {PARQUET.name}...")
df = pd.read_parquet(PARQUET)
df = df.sort_values(['Tick', 'Agent_X', 'Agent_Y']).reset_index(drop=True)

eps_alg = 1e-10
ticks = df['Tick'].nunique()
xs = df['Agent_X'].nunique()
ys = df['Agent_Y'].nunique()
print(f"Grid: {xs} x {ys}, {ticks} ticks")

is_act_3d = df['is_active'].values.reshape((ticks, xs, ys)).astype(int)
psi_3d = df['Psi_local'].to_numpy().reshape(ticks, xs, ys)

# ============================================================================
# Hypothesis 1 (current verifier): ds_3d[0] = 0, so Psi_local[0] should be 0
# ============================================================================
print("\n=== Hypothesis 1 (current verifier): Psi_local[0] should be 0 ===")
h1_fails = int((np.abs(psi_3d[0]) > eps_alg).sum())
print(f"Tick 0 nonzero Psi_local: {h1_fails} / {xs*ys}")

# ============================================================================
# Hypothesis 2: ds_3d[0] = is_active[0], reconstruct Psi_local[0] from it
# ============================================================================
print("\n=== Hypothesis 2: ds_3d[0] = is_active[0], reconstruct Psi_local[0] ===")
grid0 = is_act_3d[0].astype(float)
n_sum0 = (np.roll(grid0, 1, 0) + np.roll(grid0, -1, 0) + 
          np.roll(grid0, 1, 1) + np.roll(grid0, -1, 1) + 
          np.roll(np.roll(grid0, 1, 0), 1, 1) + np.roll(np.roll(grid0, 1, 0), -1, 1) + 
          np.roll(np.roll(grid0, -1, 0), 1, 1) + np.roll(np.roll(grid0, -1, 0), -1, 1))
psi_calc_tick0_h2 = grid0 * n_sum0

h2_diff = np.abs(psi_3d[0] - psi_calc_tick0_h2)
h2_fails = int((h2_diff > eps_alg).sum())
print(f"Reconstruction fails at tick 0: {h2_fails} / {xs*ys}")
print(f"Max diff: {h2_diff.max():.6e}")

# ============================================================================
# Hypothesis 3: Psi_local[0] uses a different ds formulation entirely
# (e.g., ds = is_active * something, or initial Psi from a separate process)
# Look at the pattern: are the 187 nonzero cells the active ones?
# ============================================================================
print("\n=== Hypothesis 3: pattern analysis ===")
active_at_0 = is_act_3d[0]
nonzero_psi_at_0 = (np.abs(psi_3d[0]) > eps_alg).astype(int)

active_count = int(active_at_0.sum())
nonzero_psi_count = int(nonzero_psi_at_0.sum())
both_active_and_nonzero = int(((active_at_0 == 1) & (nonzero_psi_at_0 == 1)).sum())
active_but_zero_psi = int(((active_at_0 == 1) & (nonzero_psi_at_0 == 0)).sum())
inactive_but_nonzero_psi = int(((active_at_0 == 0) & (nonzero_psi_at_0 == 1)).sum())

print(f"Tick 0: {active_count} active cells, {nonzero_psi_count} nonzero Psi cells")
print(f"  Active AND nonzero Psi: {both_active_and_nonzero}")
print(f"  Active but zero Psi: {active_but_zero_psi}")
print(f"  Inactive but nonzero Psi: {inactive_but_nonzero_psi}")

# ============================================================================
# Hypothesis 4: Psi_local[0] = is_active[0] * sum(is_active neighbors at 0)
# Same as hypothesis 2 explicitly checked
# Show sample values to inspect
# ============================================================================
print("\n=== Sample tick-0 cells with nonzero Psi_local ===")
nz_locs = np.argwhere(nonzero_psi_at_0 == 1)
print(f"First 10 nonzero Psi locations (x, y, is_active, Psi_local, reconstructed_h2):")
for loc in nz_locs[:10]:
    x, y = loc
    print(f"  ({x},{y}): is_active={active_at_0[x,y]}, Psi_local={psi_3d[0,x,y]:.6f}, h2_recon={psi_calc_tick0_h2[x,y]:.6f}")

# Also show 5 cells where active but zero Psi
zero_psi_active = np.argwhere((active_at_0 == 1) & (nonzero_psi_at_0 == 0))
if len(zero_psi_active) > 0:
    print(f"\nFirst 5 active-but-zero-Psi locations (x, y, is_active, Psi_local, neighbors_active):")
    for loc in zero_psi_active[:5]:
        x, y = loc
        neighbors = 0
        for dx, dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            nx, ny = (x+dx) % xs, (y+dy) % ys
            neighbors += active_at_0[nx, ny]
        print(f"  ({x},{y}): is_active={active_at_0[x,y]}, Psi_local={psi_3d[0,x,y]:.6f}, active_neighbors={neighbors}")

# ============================================================================
# Conclusion
# ============================================================================
print("\n=== INTERPRETATION ===")
if h2_fails == 0:
    print("Hypothesis 2 holds: ds_3d[0] = is_active[0] reconstruction is EXACT.")
    print("The substrate is self-consistent. The current Tier 1 verifier's")
    print("'tick 0 Psi_local must be 0' assumption is WRONG for v1.1.")
    print("Tier 1 V8 needs revision to test the correct tick-0 invariant.")
elif h2_fails < h1_fails:
    print(f"Hypothesis 2 closer but not exact: {h2_fails} fails vs h1's {h1_fails}")
    print("Mixed behavior — may need to look at sample values above to understand.")
else:
    print(f"Hypothesis 2 ({h2_fails} fails) no better than h1 ({h1_fails}).")
    print("Neither tick-0 model fits. Investigate substrate or look at v1.1 spec.")
