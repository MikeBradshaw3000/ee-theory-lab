"""
Item 6a Stage 1 EDA Implementation Script (Revision 2 / v3)
Pre-registration reference: phase_4b/pre_registrations/item_6a_f_form_characterization.yaml
"""

import os
import yaml
import hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from pathlib import Path

# --- CONFIGURATION & SEARCH SPACES ---
W_CANDIDATES = [10, 25, 50, 100, 200]
TAU_CANDIDATES = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
Z_CANDIDATES = [5, 10, 25, 50, 100]

DATA_FILES = [
    "flight2_outputs/flight6_probe1_overcrowding_FLR_20x20.parquet",
    "flight2_outputs/flight6_probe1_overcrowding_F2sym_20x20.parquet"
]

# --- DIRECTORY SETUP ---
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EDA_OUT_DIR = REPO_ROOT / "phase_4b" / "pre_registrations" / "item_6a_f_form_characterization" / "eda_outputs"
DIAG_OUT_DIR = EDA_OUT_DIR / "diagnostics"
EDA_OUT_DIR.mkdir(parents=True, exist_ok=True)
DIAG_OUT_DIR.mkdir(parents=True, exist_ok=True)

# --- ALGORITHMIC LOGIC ---

def is_valid_probe_data(df):
    """Data-validity mask per v2 YAML shadow-copy handling."""
    cond_flr = df['F_variant'] == 'F_LR'
    cond_f2sym = (df['F_variant'] == 'F_2_symmetric') & (df['probe_name'] == 'probe1_overcrowding')
    return cond_flr | cond_f2sym

def compute_rolling_rho(df):
    """Computes per-tick mean and rolling W means.
    R5: Groups by full condition tuple to guarantee trajectory isolation.
    """
    df_tick = df.groupby(['run_id', 'F_variant', 'scale', 'probe_name', 'tick'])['is_active'].mean().reset_index()
    df_tick.rename(columns={'is_active': 'rho_raw_per_tick'}, inplace=True)
    df_tick = df_tick.sort_values(['run_id', 'tick'])

    records = []
    # R5: Full condition grouping
    for (run_id, f_var, scale, probe), group in df_tick.groupby(['run_id', 'F_variant', 'scale', 'probe_name']):
        for w in W_CANDIDATES:
            roll_rho = group['rho_raw_per_tick'].rolling(window=w, min_periods=w).mean()
            for idx, val in roll_rho.items():
                records.append({
                    'run_id': run_id,
                    'F_variant': f_var,
                    'scale': scale,
                    'probe_name': probe,
                    'tick': group.loc[idx, 'tick'],
                    'W': w,
                    'rolling_rho': val,
                    'rho_raw_per_tick': group.loc[idx, 'rho_raw_per_tick']
                })
    return pd.DataFrame(records)

def get_epoch_label(tick):
    """Canonical boundaries per Phase 4B v1.1 §3.1 T2.2"""
    if tick < 100: return "epoch_0-99"
    elif tick < 500: return "epoch_100-499"
    elif tick < 1000: return "epoch_500-999"
    elif tick < 1500: return "epoch_1000-1499"
    elif tick < 2000: return "epoch_1500-1999"
    elif tick < 2500: return "epoch_2000-2499"
    elif tick < 3000: return "epoch_2500-2999"
    else: return "epoch_3000+" 

def get_first_crossing(series_rho, ticks, tau, Z):
    """Finds first tick t where rho > tau for Z consecutive ticks.
    R6-alpha: Positional computation for substrate contiguity independence.
    """
    condition = (series_rho > tau).astype(int)
    consecutive = condition.rolling(window=Z, min_periods=Z).sum()
    match_idx = consecutive[consecutive == Z].first_valid_index()
    
    if match_idx is not None:
        pos = ticks.index.get_loc(match_idx)
        start_pos = pos - Z + 1
        if start_pos < 0:
            return None 
        return ticks.iloc[start_pos]
    return None

def evaluate_crossing_status(crossing_tick, W, Z, max_tick):
    if crossing_tick is None:
        return "no_crossing"
    if crossing_tick <= (W - 1) or crossing_tick >= (max_tick - Z):
        return "crossed_at_boundary"
    return "crossed_identifiable"

def generate_threshold_tables(df_rolling):
    results = []
    base_evals = {}
    
    for run_id, run_group in df_rolling.groupby('run_id'):
        max_tick = run_group['tick'].max()
        f_var = run_group['F_variant'].iloc[0]
        scale = run_group['scale'].iloc[0]
        
        for w in W_CANDIDATES:
            w_group = run_group[run_group['W'] == w]
            ticks = w_group['tick']
            rhos = w_group['rolling_rho']
            
            for tau in TAU_CANDIDATES:
                for z in Z_CANDIDATES:
                    cross_tick = get_first_crossing(rhos, ticks, tau, z)
                    status = evaluate_crossing_status(cross_tick, w, z, max_tick)
                    epoch = get_epoch_label(cross_tick) if cross_tick is not None else None
                    
                    key = (run_id, w, tau, z)
                    base_evals[key] = {
                        'run_id': run_id, 'F_variant': f_var, 'scale': scale,
                        'W': w, 'tau': tau, 'Z': z,
                        'first_crossing_tick': cross_tick,
                        'first_crossing_epoch': epoch,
                        'crossing_status_base': status, 
                        'crossing_status_final': status 
                    }
                    
    def get_valid_perturbation_keys(r_id, cw, ctau, cz):
        w_idx, tau_idx, z_idx = W_CANDIDATES.index(cw), TAU_CANDIDATES.index(ctau), Z_CANDIDATES.index(cz)
        perturb_keys = []
        for dw, dtau, dz in itertools.product([-1, 0, 1], repeat=3):
            if dw == 0 and dtau == 0 and dz == 0: continue 
            nw_idx, ntau_idx, nz_idx = w_idx + dw, tau_idx + dtau, z_idx + dz
            if (0 <= nw_idx < len(W_CANDIDATES) and 
                0 <= ntau_idx < len(TAU_CANDIDATES) and 
                0 <= nz_idx < len(Z_CANDIDATES)):
                perturb_keys.append((r_id, W_CANDIDATES[nw_idx], TAU_CANDIDATES[ntau_idx], Z_CANDIDATES[nz_idx]))
        return perturb_keys

    final_results = []
    for key, data in base_evals.items():
        run_id, w, tau, z = key
        status = data['crossing_status_base']
        base_tick = data['first_crossing_tick']
        
        if status == 'crossed_identifiable':
            is_unstable = False
            for pk in get_valid_perturbation_keys(run_id, w, tau, z):
                if pk in base_evals:
                    ptick = base_evals[pk]['first_crossing_tick']
                    if ptick is None or abs(base_tick - ptick) > 100:
                        is_unstable = True
                        break
            if is_unstable:
                data['crossing_status_final'] = 'unstable'
                
        final_results.append(data)
        
    return pd.DataFrame(final_results)

def evaluate_locking_rules(df_crossings):
    combos = []
    
    for (w, tau, z), group in df_crossings.groupby(['W', 'tau', 'Z']):
        if len(group) != 2: continue 
        
        # Base Identifiability 
        c1_base = (group['crossing_status_base'] == 'crossed_identifiable').all()
        # Final Identifiability
        c1_final = (group['crossing_status_final'] == 'crossed_identifiable').all()
        
        c3_base = False
        c3_final = False
        flr_tick_base = f2sym_tick_base = None
        flr_tick_final = f2sym_tick_final = None
        
        # R4: Calculate Base Discriminability (pre-perturbation ticks)
        if c1_base:
            flr_tick_base = group[group['F_variant'] == 'F_LR']['first_crossing_tick'].iloc[0]
            f2sym_tick_base = group[group['F_variant'] == 'F_2_symmetric']['first_crossing_tick'].iloc[0]
            if abs(flr_tick_base - f2sym_tick_base) > z:
                c3_base = True
        
        # Calculate Final Discriminability 
        if c1_final:
            flr_tick_final = flr_tick_base
            f2sym_tick_final = f2sym_tick_base
            c3_final = c3_base
                
        combos.append({
            'W': w, 'tau': tau, 'Z': z,
            'crit_1_base_pass': c1_base,
            'crit_3_base_pass': c3_base,
            'flr_tick_base': flr_tick_base,
            'f2sym_tick_base': f2sym_tick_base,
            'crit_1_final_pass': c1_final,
            'crit_3_final_pass': c3_final,
            'flr_tick_final': flr_tick_final,
            'f2sym_tick_final': f2sym_tick_final,
            'status_base_list': group['crossing_status_base'].tolist(),
            'status_final_list': group['crossing_status_final'].tolist()
        })
        
    df_eval = pd.DataFrame(combos)
    
    # R4: Strict E1 vs E7 Logic
    valid_base = df_eval[df_eval['crit_1_base_pass'] & df_eval['crit_3_base_pass']].copy() 
    valid_final = df_eval[df_eval['crit_1_final_pass'] & df_eval['crit_3_final_pass']].copy()
    
    escalation = None
    locked_combo = None
    
    if len(valid_final) == 0:
        if len(valid_base) > 0:
            escalation = ("E7", "Degeneracy: Admissible combinations existed but failed S1b perturbation stability checks.")
        else:
            escalation = ("E1", "Identifiability failed: No combinations satisfied criteria 1 and 3 on base trajectory.")
    else:
        valid_final = valid_final.sort_values(by=['W', 'Z', 'tau'], ascending=[True, False, False])
        locked_combo = valid_final.iloc[0]
            
    return df_eval, locked_combo, escalation

# --- OUTPUT WRITERS ---

def write_diagnostics(df_rolling, df_crossings, df_eval):
    for (run_id, w), group in df_rolling.groupby(['run_id', 'W']):
        plt.figure(figsize=(10,6))
        plt.plot(group['tick'], group['rolling_rho'], label=f'W={w}')
        for tau in TAU_CANDIDATES:
            plt.axhline(tau, color='gray', linestyle='--', alpha=0.3)
        plt.title(f"Rolling Rho - Run: {run_id} - W: {w}")
        plt.xlabel("Tick")
        plt.ylabel("Rolling Rho")
        plt.savefig(DIAG_OUT_DIR / f"traj_{run_id}_W{w}.png")
        plt.close()

    for w, group in df_rolling.groupby('W'):
        plt.figure(figsize=(10,6))
        for run_id, rgroup in group.groupby('run_id'):
            fvar = rgroup['F_variant'].iloc[0]
            plt.plot(rgroup['tick'], rgroup['rolling_rho'], label=f'{fvar} ({run_id})')
        for tau in TAU_CANDIDATES:
            plt.axhline(tau, color='gray', linestyle='--', alpha=0.3)
        plt.title(f"F_LR vs F_2_sym - W={w}")
        plt.legend()
        plt.savefig(DIAG_OUT_DIR / f"overlay_W{w}.png")
        plt.close()

def generate_reports(df_eval, locked_combo, escalation):
    df_eval.to_csv(EDA_OUT_DIR / "calibration_report.csv", index=False)
    
    if escalation:
        trig, reason = escalation
        report = f"# Escalation Report\n\n**Trigger:** {trig}\n**Evidence:** {reason}\n"
        report += "\n*Implication: Second confirmatory pre-registration required before further confirmatory execution.*\n"
        with open(EDA_OUT_DIR / "escalation_report.md", "w") as f:
            f.write(report)
            
        with open(EDA_OUT_DIR / "calibration_report.md", "w") as f:
            f.write("# Calibration Report\n\n**Outcome:** FAILED (Escalated)\nSee escalation_report.md\n")
    else:
        script_hash = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
        yaml_out = {
            "pre_registration_id": "item_6a_f_form_characterization",
            "stage_1_completion_date": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "locked_parameters": {
                "W": int(locked_combo['W']),
                "tau": float(locked_combo['tau']),
                "Z": int(locked_combo['Z'])
            },
            "locking_rule_evidence": {
                "criterion_1_identifiability": "Satisfied. Crossed identifiable boundaries and passed S1b joint perturbations.",
                "criterion_2_parsimony": "Ranked first lexicographically (W asc, Z desc, tau desc).",
                "criterion_3_cross_F_form_discriminability": f"Difference > Z ticks achieved. (FLR: {locked_combo['flr_tick_final']}, F2sym: {locked_combo['f2sym_tick_final']})"
            },
            "calibration_runs": [
                {"F_variant": "F_LR", "first_crossing_tick": int(locked_combo['flr_tick_final'])},
                {"F_variant": "F_2_symmetric", "first_crossing_tick": int(locked_combo['f2sym_tick_final'])}
            ],
            "e7_degeneracy_check_passed": True,
            "implementation_script_hash": script_hash,
            "eda_outputs_directory": str(EDA_OUT_DIR.relative_to(REPO_ROOT))
        }
        with open(REPO_ROOT / "phase_4b" / "pre_registrations" / "item_6a_f_form_characterization" / "calibration_locked.yaml", "w") as f:
            yaml.dump(yaml_out, f, sort_keys=False)
            
        with open(EDA_OUT_DIR / "calibration_report.md", "w") as f:
            f.write("# Calibration Report\n\n**Outcome:** SUCCESS (Locked)\n")
            f.write(f"Locked parameters: W={locked_combo['W']}, tau={locked_combo['tau']}, Z={locked_combo['Z']}\n")

# --- MAIN EXECUTION ---
def main():
    print("Starting Item 6a EDA Stage 1 (Revision 2 / v3)...")
    
    dfs = []
    for f in DATA_FILES:
        path = REPO_ROOT / f
        if path.exists():
            dfs.append(pd.read_parquet(path))
        else:
            print(f"[!] File not found, skipping for script-check: {path}")
            
    if not dfs:
        print("[!] No data loaded. Exiting.")
        return
        
    df_raw = pd.concat(dfs, ignore_index=True)
    df_raw['is_valid_probe_data'] = is_valid_probe_data(df_raw)
    df_valid = df_raw[df_raw['is_valid_probe_data']].copy()
    
    print("Computing rolling rho trajectories...")
    df_rolling = compute_rolling_rho(df_valid)
    df_rolling.to_csv(EDA_OUT_DIR / "rolling_rho_trajectories.csv", index=False)
    
    print("Generating threshold crossing tables...")
    df_crossings = generate_threshold_tables(df_rolling)
    df_crossings.to_csv(EDA_OUT_DIR / "threshold_crossing_tables.csv", index=False)
    
    print("Evaluating locking rules and escalations...")
    df_eval, locked_combo, escalation = evaluate_locking_rules(df_crossings)
    
    print("Writing diagnostics and final reports...")
    write_diagnostics(df_rolling, df_crossings, df_eval)
    generate_reports(df_eval, locked_combo, escalation)
    
    print("Item 6a EDA Stage 1 complete.")

if __name__ == "__main__":
    main()
