"""
Phase 4b Cross-Run Comparison
Calculates the delta between two Parquet outputs to characterize cascade 
divergence, bifurcation thresholds, and structural network formation.
"""

import sys
import argparse
from pathlib import Path
import pandas as pd
from _phase_4b_common import verify_environment, setup_phase4_logger, get_active_module

logger = setup_phase4_logger("cross_run_compare")

def compare_runs(baseline_path, variant_path):
    verify_environment()
    
    base_file = Path(baseline_path)
    var_file = Path(variant_path)
    
    if not base_file.exists() or not var_file.exists():
        logger.error("One or both Parquet files not found.")
        sys.exit(1)
        
    logger.info(f"Loading Baseline: {base_file.name}")
    df_base = pd.read_parquet(base_file)
    
    logger.info(f"Loading Variant: {var_file.name}")
    df_var = pd.read_parquet(var_file)
    
    # Ensure structural parity before comparison
    if 'Step' not in df_base.columns or 'Step' not in df_var.columns:
        logger.error("Missing 'Step' index in outputs.")
        sys.exit(1)

    # Calculate Global Timeseries Aggregates
    base_agg = df_base.groupby('Step')['Psi_local'].mean()
    var_agg = df_var.groupby('Step')['Psi_local'].mean()
    
    # Align and compute divergence
    compare_df = pd.DataFrame({
        'Baseline_Mean_Psi': base_agg,
        'Variant_Mean_Psi': var_agg
    }).fillna(0)
    
    compare_df['Psi_Divergence'] = compare_df['Variant_Mean_Psi'] - compare_df['Baseline_Mean_Psi']
    
    # Log module context
    active_lambda = get_active_module("lambda_variable")
    logger.info(f"Active Structural Conduciveness Implementation: {active_lambda}")
    
    # Output Results
    output_filename = f"compare_{base_file.stem}_VS_{var_file.stem}.csv"
    compare_df.to_csv(output_filename)
    
    logger.info(f"Comparison complete. Divergence timeseries saved to: {output_filename}")
    
    # Print high-level summary
    max_div = compare_df['Psi_Divergence'].abs().max()
    max_div_step = compare_df['Psi_Divergence'].abs().idxmax()
    print("\n--- Cross-Run Summary ---")
    print(f"Maximum Psi Divergence: {max_div:.4f} (Occurred at Step {max_div_step})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cross-Run Comparison for Phase 4b")
    parser.add_argument("--baseline", required=True, help="Path to baseline parquet")
    parser.add_argument("--variant", required=True, help="Path to variant parquet")
    args = parser.parse_args()
    
    compare_runs(args.baseline, args.variant)