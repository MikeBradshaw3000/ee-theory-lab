import argparse
import yaml
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from pathlib import Path
from _phase_4b_common import verify_environment, eta_floor_inversion

def wrap_categorical(term):
    term_clean = term.strip()
    if term_clean.startswith("C(") and term_clean.endswith(")"):
        return term_clean
    if term_clean in ['f_variant', 'scale', 'F_variant', 'Scale']:
        return f"C({term_clean})"
    return term_clean

def run_tier3(prereg_file: Path):
    verify_environment()
    with open(prereg_file, 'r') as f:
        spec = yaml.safe_load(f)
        
    req_fields = ['data_files', 'outcome', 'model_family', 'predictors', 'interactions', 'excluded_variables', 'uncertainty_method', 'interpretation_boundary']
    for req in req_fields:
        if req not in spec:
            raise ValueError(f"T3 FAULT: Missing pre-registration field: {req}")
            
    prereg_id = spec.get('prereg_id', prereg_file.stem)
    dfs = []
    
    for fpath in spec['data_files']:
        p = Path(fpath)
        df_part = pd.read_parquet(p)
        df_part['run_id'] = p.stem
        dfs.append(df_part)
        
    df = pd.concat(dfs, ignore_index=True)
    df['cluster_group'] = df['run_id'] + "_" + df['Tick'].astype(str)
    
    cluster_count = df['cluster_group'].nunique()
    independent_run_count = df['run_id'].nunique()
    
    boundary_count = 0
    if spec['outcome'] == 'logit_p_base':
        df['logit_p_base'], boundary_count = eta_floor_inversion(df['p_act'])
        
    formula_parts = [wrap_categorical(p) for p in spec['predictors']]
    if spec['interactions'] and spec['interactions'].get('terms'):
        formula_parts.extend(spec['interactions']['terms'])
        
    formula_str = f"{spec['outcome']} ~ " + " + ".join(formula_parts)
    
    if spec['model_family'] == 'linear':
        model = smf.ols(formula_str, data=df)
    elif spec['model_family'] == 'logistic':
        model = smf.logit(formula_str, data=df)
    elif spec['model_family'] == 'fractional_logit':
        model = smf.glm(formula_str, data=df, family=sm.families.Binomial(link=sm.families.links.Logit()))
    elif spec['model_family'] == 'multinomial_logistic':
        model = smf.mnlogit(formula_str, data=df)
    else:
        raise ValueError(f"Unknown model_family: {spec['model_family']}")

    if spec['uncertainty_method'] == 'cluster_run_tick':
        result = model.fit(cov_type='cluster', cov_kwds={'groups': df['cluster_group']})
    elif spec['uncertainty_method'] == 'sandwich':
        result = model.fit(cov_type='HC3')
    else:
        result = model.fit()

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    out_dir = project_root / "phase_4b" / "tier3_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(out_dir / f"report_{prereg_id}.md", "w") as f:
        f.write(f"# Tier 3 Regression Report: {prereg_id}\n\n")
        f.write(f"**Interpretation Boundary:** {spec['interpretation_boundary']}\n\n")
        
        f.write(f"- Cluster Count: {cluster_count}\n")
        f.write(f"- Independent Runs: {independent_run_count}\n")
        f.write(f"- Eta-Boundary Count (if logit_p_base): {boundary_count} / {len(df)}\n\n")
        
        if independent_run_count < 10:
            f.write("> **CAVEAT:** Run-level replication is weak.\n\n")
        if cluster_count < 30:
            f.write("> **CAVEAT:** P-values reported descriptively; cluster count too small for strong inferential interpretation.\n\n")
            
        if cluster_count < 10:
            f.write("```\n" + result.params.to_string() + "\n```\n")
        else:
            f.write("```\n" + result.summary().as_text() + "\n```\n")
            
    coef_df = pd.DataFrame({
        'coef': result.params,
        'std_err': result.bse,
        'p_value': result.pvalues
    })
    coef_df.to_csv(out_dir / f"coefs_{prereg_id}.csv")
    print(f"Tier 3 complete. Outputs in {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prereg", type=Path, required=True)
    args = parser.parse_args()
    run_tier3(args.prereg)
