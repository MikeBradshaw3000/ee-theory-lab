#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
from pathlib import Path

from _phase_4b_common import verify_environment
from _phase_4b_intake import (
    load_prereg, normalize_prereg, load_canonical_inputs,
    promote_metadata_to_columns, construct_derived_variables,
    attach_tier2_globals, validate_formula_variables, echo_intake_summary
)

def build_cluster_group(df, cluster_var):
    if cluster_var == 'run_x_tick':
        return df['run_id'] + "_" + df['Tick'].astype(str)
    elif cluster_var == 'cell':
        return df['run_id'] + "_" + df['Agent_X'].astype(str) + "_" + df['Agent_Y'].astype(str)
    else:
        return df[cluster_var]

def get_model(formula_str, data, family):
    if family == 'ols':
        return smf.ols(formula_str, data=data)
    elif family == 'logit':
        return smf.logit(formula_str, data=data)
    elif family == 'fractional_logit':
        return smf.glm(formula_str, data=data, family=sm.families.Binomial(link=sm.families.links.Logit()))
    elif family == 'multinomial_logistic':
        return smf.mnlogit(formula_str, data=data)
    else:
        raise ValueError(f"Unknown model_family: {family}")

def write_coefficients_csv(result, filepath):
    coef_df = pd.DataFrame({
        'coef': result.params,
        'std_err': result.bse,
        'p_value': result.pvalues
    })
    
    coef_df['empirical_result'] = ""
    coef_df['structural_status'] = ""
    coef_df['classification_notes'] = ""
    
    coef_df.to_csv(filepath)

def run_tier3(prereg_file: Path):
    verify_environment()
    
    spec = load_prereg(prereg_file)
    normalized = normalize_prereg(spec)
    df, metadata = load_canonical_inputs(normalized)
    df = promote_metadata_to_columns(df, metadata)
    df = construct_derived_variables(df, normalized)
    df = attach_tier2_globals(df, normalized)
    
        
    validate_formula_variables(df, normalized)
    print(echo_intake_summary(df, metadata, normalized))
    
    df['cluster_group_primary'] = build_cluster_group(df, normalized.cluster_variable)
    cluster_count = df['cluster_group_primary'].nunique()
    
    model_primary = get_model(normalized.formula, df, normalized.model_family)
    
    if normalized.primary_uncertainty_method == 'cluster_robust':
        result_primary = model_primary.fit(cov_type='cluster', cov_kwds={'groups': df['cluster_group_primary']})
    else:
        result_primary = model_primary.fit()

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    out_dir = project_root / "phase_4b" / "tier3_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    write_coefficients_csv(result_primary, out_dir / f"coefs_{normalized.prereg_id}.csv")
    
    sensitivity_results = {}
    for sens_c_var in normalized.sensitivity_methods:
        sens_c_var_clean = sens_c_var
        if sens_c_var in ["cluster_run_tick", "run_x_tick"]:
            sens_c_var_clean = "run_x_tick"
            
        cg_col = f"cluster_group_sens_{sens_c_var_clean}"
        df[cg_col] = build_cluster_group(df, sens_c_var_clean)
        
        s_model = get_model(normalized.formula, df, normalized.model_family)
        s_result = s_model.fit(cov_type='cluster', cov_kwds={'groups': df[cg_col]})
            
        sensitivity_results[sens_c_var_clean] = s_result
        write_coefficients_csv(s_result, out_dir / f"coefs_{normalized.prereg_id}_sensitivity_{sens_c_var_clean}.csv")
    
    # REPORT GENERATION
    with open(out_dir / f"report_{normalized.prereg_id}.md", "w") as f:
        def w(text=""):
            print(text, file=f)

        bt = '`' * 3

        w(f"# Tier 3 Regression Report: {normalized.prereg_id}")
        w()
        w("### Interpretation Boundary")
        w()
        w("#### What this regression licenses")
        w()
        w(spec['interpretation_boundary']['licenses'])
        w()
        w("#### What this regression does not adjudicate")
        w()
        w(spec['interpretation_boundary']['does_not_adjudicate'])
        w()
        w("### Dataset Details")
        w()
        w(f"- **Files loaded:** {', '.join([m.source_file for m in metadata])}")
        w(f"- **Independent runs:** {len(metadata)}")
        w(f"- **Primary Cluster Count ({normalized.cluster_variable}):** {cluster_count}")
        w()
        
        if normalized.outcome_construction == "eta_floor_inversion_of_p_base":
            boundary_count = (df['p_act'] <= 0.01).sum() + (df['p_act'] >= 0.99).sum()
            w(f"- **Eta-Boundary Count:** {boundary_count} / {len(df)}")
            w()
            
        if len(metadata) < 10:
            w("> **CAVEAT:** Run-level replication is weak.")
            w()
        if cluster_count < 30:
            w("> **CAVEAT:** P-values reported descriptively; cluster count too small for strong inferential interpretation.")
            w()
            
        w("### Primary Model Results")
        w()
        w(bt)
        if cluster_count < 10:
            w(result_primary.params.to_string())
        else:
            w(result_primary.summary().as_text())
        w(bt)
        w()
            
        if sensitivity_results:
            w("### Sensitivity analysis (NOT the primary uncertainty method)")
            w()
            for c_var, s_result in sensitivity_results.items():
                w(f"#### Clustered by: {c_var}")
                w()
                if len(s_result.params) > 0:
                    w(bt)
                    w(s_result.summary().as_text())
                    w(bt)
                    w()
                    
        w("### Classification Status")
        w()
        w("> Classification fields are intentionally left blank for post-output review. ")
        w("Tier 3 estimates inform classification but do not assign structural status automatically. ")
        w("Classification is performed by Mike or routed AI review against the registered interpretation_boundary.")
            
    print(f"Tier 3 complete. Report and CSV(s) successfully generated in {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prereg", type=Path, required=True)
    args = parser.parse_args()
    run_tier3(args.prereg)

