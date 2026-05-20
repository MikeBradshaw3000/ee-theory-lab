import argparse, yaml, pandas as pd, gc, numpy as np
import statsmodels.formula.api as smf, statsmodels.api as sm
from pathlib import Path
from _phase_4b_common import verify_environment

def eta_floor_inversion(p_series, eta=0.01):
    boundary_mask = (p_series <= eta) | (p_series >= (1.0 - eta))
    p_clipped = np.clip(p_series, eta, 1.0 - eta)
    return np.log(p_clipped / (1.0 - p_clipped)), int(boundary_mask.sum())

def wrap_categorical(term):
    term_clean = term.strip()
    if term_clean.startswith("C(") and term_clean.endswith(")"): return term_clean
    if term_clean in ['F_variant', 'scale']: return f"C({term_clean})"
    return term_clean

def run_tier3(prereg_path):
    verify_environment()
    prereg_file = Path(prereg_path).resolve()
    with open(prereg_file, 'r') as f: spec = yaml.safe_load(f)

    print(f"--- Tier 3 Regression Executing: {prereg_file.name} ---")
    for field in ['data_files', 'outcome', 'model_family', 'predictors', 'interactions', 'excluded_variables', 'uncertainty_method', 'interpretation_boundary']:
        if field not in spec: raise ValueError(f"Missing required pre-registration field: {field}")

    if spec['interactions'] is not None:
        if not isinstance(spec['interactions'], dict) or 'family' not in spec['interactions'] or 'terms' not in spec['interactions']:
            raise ValueError("Interactions must use nested schema: {family: '...', terms: [...]}")

    dfs, run_ids = [], set()
    for fpath in spec['data_files']:
        df_part = pd.read_parquet(Path(fpath).resolve())
        run_id = Path(fpath).stem
        run_ids.add(run_id)
        df_part['run_id'] = run_id
        df_part['cluster_group'] = run_id + "_" + df_part['Step'].astype(str)
        dfs.append(df_part)

    df = pd.concat(dfs, ignore_index=True)
    del dfs; gc.collect()

    independent_run_count = len(run_ids)
    family = spec['model_family']
    outcome_var = spec['outcome']

    boundary_cnt = 0
    if outcome_var == 'logit_p_base':
        df['logit_p_base'], boundary_cnt = eta_floor_inversion(df['p_act'], eta=0.01)
        if family == 'fractional_logit':
            print("Defect 3 Protection Active: Converting 'logit_p_base' to raw bounded probability for Fractional Logit GLM.")
            df['p_base_raw'] = (df['p_act'] - 0.01) / (1.0 - 0.01)
            df['p_base_raw'] = np.clip(df['p_base_raw'], 0.0, 1.0)
            outcome_var = 'p_base_raw'

    boundary_rate = boundary_cnt / len(df) if len(df) > 0 else 0
    preds = [wrap_categorical(p) for p in spec['predictors']]
    formula = f"{outcome_var} ~ {' + '.join(preds)}"

    if spec['interactions'] and spec['interactions']['terms']:
        int_terms = []
        for t in spec['interactions']['terms']:
            parts = [wrap_categorical(p.strip()) for p in t.split(':')]
            int_terms.append(':'.join(parts))
        formula += " + " + " + ".join(int_terms)

    unc_method = spec['uncertainty_method']
    if unc_method in ['cluster_run_tick', 'cluster_run_step']:
        cov_type = 'cluster'
        cov_kwds = {'groups': df['cluster_group']}
        cluster_count = df['cluster_group'].nunique()
    elif unc_method == 'sandwich':
        cov_type = 'HC3'
        cov_kwds = None
        cluster_count = float('inf')
    else:
        raise ValueError(f"Unsupported uncertainty method: {unc_method}")

    if family == 'linear': model = smf.ols(formula, data=df)
    elif family == 'logistic': model = smf.logit(formula, data=df)
    elif family == 'fractional_logit': model = smf.glm(formula, data=df, family=sm.families.Binomial())
    elif family == 'multinomial_logistic': model = smf.mnlogit(formula, data=df)
    else: raise ValueError(f"Unsupported model family: {family}")

    result = model.fit(cov_type=cov_type, cov_kwds=cov_kwds)
    out_dir = prereg_file.parent.parent / "tier3_outputs"
    out_dir.mkdir(exist_ok=True)

    prereg_id = spec.get('prereg_id', prereg_file.stem)
    rep_path = out_dir / f"report_{prereg_id}.md"
    csv_path = out_dir / f"coefs_{prereg_id}.csv"

    with open(rep_path, 'w') as f:
        f.write(f"# Tier 3 Regression Report: {prereg_id}\n")
        f.write(f"**Interpretation Boundary:** {spec['interpretation_boundary']}\n\n")
        f.write(f"**Model Family Applied:** {family}\n")
        f.write(f"**Boundary Limit Hit (eta-floor inversion):** {boundary_cnt} rows ({boundary_rate:.4%})\n")
        if family == 'linear' and boundary_rate > 0.05:
            f.write("**WARNING:** High boundary floor saturation detected in linear model space. Leverage artifacts possible.\n")

        f.write(f"\n**Independent Runs:** {independent_run_count}\n")
        f.write(f"**Run-Step Clusters:** {cluster_count}\n\n")

        if independent_run_count < 10: f.write("**CAVEAT:** Independent run count < 10. Run-level replication is weak.\n\n")
        if cluster_count < 10: f.write("**CAVEAT:** Cluster count < 10. Significance language and p-values suppressed.\n\n")
        elif cluster_count < 30: f.write("**CAVEAT:** P-values reported descriptively; cluster count < 30 is too small for strong inferential interpretation.\n\n")

        f.write("```text\n")
        if cluster_count >= 10: f.write(result.summary().as_text())
        else: f.write(f"Coefficients:\n{result.params.to_string()}")
        f.write("\n```\n")

    summary_df = pd.DataFrame({'coef': result.params, 'std_err': result.bse, 'p_value': result.pvalues})
    summary_df.to_csv(csv_path)
    del df, model, result; gc.collect()
    print(f"Regression complete. Outputs saved to {out_dir.name}/")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prereg', required=True)
    args = parser.parse_args()
    run_tier3(args.prereg)