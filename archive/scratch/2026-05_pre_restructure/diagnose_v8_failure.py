"""
Diagnostic script for Tier 1 V8 failure on flight6_probe1_overcrowding_20x20.
Splits V8 into Psi_local reconstruction vs base evolution tick discipline.
Read-only. Not committed to canonical record.
"""
import pandas as pd
import numpy as np
from pathlib import Path

PARQUET = Path(r"C:\Users\vkz244\EE_Theory_Lab\flight2_outputs\flight6_probe1_overcrowding_20x20.parquet")

print(f"Loading {PARQUET.name}...")
df = pd.read_parquet(PARQUET)
print(f"Loaded {len(df):,} rows, {df['Tick'].nunique()} ticks")

df = df.sort_values(['Tick', 'Agent_X', 'Agent_Y']).reset_index(drop=True)

eps_alg = 1e-10
ticks = df['Tick'].nunique()
xs = df['Agent_X'].nunique()
ys = df['Agent_Y'].nunique()
print(f"Grid: {xs} x {ys} = {xs*ys} cells, {ticks} ticks")

# ============================================================================
# V8a: Psi_local toroidal Moore reconstruction
# ============================================================================
print("\n=== V8a: Psi_local toroidal Moore reconstruction ===")
is_act_3d = df['is_active'].values.reshape((ticks, xs, ys)).astype(int)
ds_3d = np.zeros_like(is_act_3d, dtype=float)
ds_3d[1:] = is_act_3d[1:] - is_act_3d[:-1]

psi_3d = df['Psi_local'].to_numpy().reshape(ticks, xs, ys)
psi_calc_3d = np.zeros_like(ds_3d, dtype=float)

v8a_tick0_fails = int((np.abs(psi_3d[0]) > eps_alg).sum())
print(f"Tick 0 Psi_local nonzero: {v8a_tick0_fails}")

v8a_per_tick_fails = []
for t in range(1, ticks):
    grid = ds_3d[t]
    n_sum = (np.roll(grid, 1, 0) + np.roll(grid, -1, 0) + 
             np.roll(grid, 1, 1) + np.roll(grid, -1, 1) + 
             np.roll(np.roll(grid, 1, 0), 1, 1) + np.roll(np.roll(grid, 1, 0), -1, 1) + 
             np.roll(np.roll(grid, -1, 0), 1, 1) + np.roll(np.roll(grid, -1, 0), -1, 1))
    psi_calc_3d[t] = grid * n_sum
    diff = np.abs(psi_3d[t] - psi_calc_3d[t])
    fails = int((diff > eps_alg).sum())
    if fails > 0:
        v8a_per_tick_fails.append((t, fails, float(diff.max())))

v8a_total = v8a_tick0_fails + sum(f for _, f, _ in v8a_per_tick_fails)
print(f"V8a total Psi reconstruction fails: {v8a_total}")
print(f"Ticks with reconstruction fails: {len(v8a_per_tick_fails)}")
if v8a_per_tick_fails:
    print("First 10 failing ticks (tick, count, max_diff):")
    for t, f, d in v8a_per_tick_fails[:10]:
        print(f"  Tick {t}: {f} fails, max diff {d:.6e}")

# ============================================================================
# V8b: Base evolution tick discipline
# ============================================================================
print("\n=== V8b: Base evolution tick discipline ===")
df_next = df.groupby(['Agent_X', 'Agent_Y'])[['b_i_v', 'b_i_u', 'b_i_r']].shift(-1)
b_v_calc = np.clip(df['b_i_v'] + df['Delta_v'], 0.0, 1.0)
b_u_calc = np.clip(df['b_i_u'] + df['Delta_u'], 0.0, 1.0)
b_r_calc = np.clip(df['b_i_r'] + df['Delta_r'], 0.0, 1.0)

v8b_v_mask = (np.abs(df_next['b_i_v'] - b_v_calc) > eps_alg) & df_next['b_i_v'].notna()
v8b_u_mask = (np.abs(df_next['b_i_u'] - b_u_calc) > eps_alg) & df_next['b_i_u'].notna()
v8b_r_mask = (np.abs(df_next['b_i_r'] - b_r_calc) > eps_alg) & df_next['b_i_r'].notna()

v8b_v_fails = int(v8b_v_mask.sum())
v8b_u_fails = int(v8b_u_mask.sum())
v8b_r_fails = int(v8b_r_mask.sum())
v8b_total = v8b_v_fails + v8b_u_fails + v8b_r_fails

print(f"V8b base evolution fails:")
print(f"  b_i_v: {v8b_v_fails}")
print(f"  b_i_u: {v8b_u_fails}")
print(f"  b_i_r: {v8b_r_fails}")
print(f"V8b total: {v8b_total}")

# Note: the current Tier 1 code only tests b_i_v in v8_tick_fails, but we test all three
# above for completeness. Adjust if Tier 1 logic changes.
print(f"\nNote: Tier 1 currently only counts b_i_v mismatches as v8_tick_fails: {v8b_v_fails}")

# Sample locations of failures if any
if v8b_v_fails > 0:
    fail_idx = df.index[v8b_v_mask]
    print(f"\nFirst 5 b_i_v failure locations (Tick, X, Y, b_i_v, Delta_v, expected_next, actual_next):")
    for idx in fail_idx[:5]:
        row = df.loc[idx]
        expected = max(0.0, min(1.0, row['b_i_v'] + row['Delta_v']))
        actual = df_next.loc[idx, 'b_i_v']
        print(f"  Tick {row['Tick']}, ({row['Agent_X']},{row['Agent_Y']}): b_i_v={row['b_i_v']:.6f}, Delta_v={row['Delta_v']:.6e}, expected={expected:.6f}, actual={actual:.6f}")

# ============================================================================
# Summary
# ============================================================================
print("\n=== SUMMARY ===")
print(f"V8a Psi reconstruction fails: {v8a_total}")
print(f"V8b b_i_v base evolution fails (current Tier 1 logic): {v8b_v_fails}")
print(f"V8b b_i_u base evolution fails (not currently in Tier 1): {v8b_u_fails}")
print(f"V8b b_i_r base evolution fails (not currently in Tier 1): {v8b_r_fails}")
print(f"Sum of V8a + V8b_v = {v8a_total + v8b_v_fails} (should match Tier 1's reported V8_Discipline_Fails=187)")
