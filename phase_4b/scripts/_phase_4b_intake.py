import os
import re
import yaml
import patsy
import pandas as pd
import pyarrow.parquet as pq
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, List, Dict, Any

from _phase_4b_common import get_paths, eta_floor_inversion

# =============================================================================
# CONSTANTS & REGISTRIES
# =============================================================================

CLUSTER_VARIABLE_ALIASES = {
    "cluster_run_tick": "run_x_tick",
    "run_x_tick": "run_x_tick",
    "cell": "cell",
}

CATEGORICAL_VARIABLES = {"F_variant", "scale", "epoch"}

# =============================================================================
# EXCEPTIONS
# =============================================================================

class PreregSchemaError(Exception):
    def __init__(self, field, expected, actual, context=""):
        super().__init__(f"PreregSchemaError [{context}]: Field '{field}' expected {expected}, got {actual}.")

class CanonicalInputError(Exception):
    def __init__(self, file_path, missing_element, context=""):
        super().__init__(f"CanonicalInputError [{context}]: File '{file_path}' missing required element '{missing_element}'.")

class MetadataPromotionError(Exception):
    def __init__(self, run_id, missing_field, context=""):
        super().__init__(f"MetadataPromotionError [{context}]: Run '{run_id}' missing required metadata '{missing_field}'.")

class DerivedVariableError(Exception):
    def __init__(self, variable, missing_sources, rule, context=""):
        super().__init__(f"DerivedVariableError [{context}]: Rule '{rule}' for '{variable}' failed. Missing sources: {missing_sources}.")

class FormulaVariableError(Exception):
    def __init__(self, missing_vars, available_cols, context=""):
        super().__init__(f"FormulaVariableError [{context}]: Formula variables missing from DataFrame: {missing_vars}. Available: {available_cols}.")

# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass(frozen=True)
class NormalizedPrereg:
    prereg_id: str
    prereg_version: str
    outcome_name: str
    outcome_construction: str
    outcome_eta: float | None
    model_family: str
    formula: str
    formula_role: str
    predictors: List[str]
    interactions: List[str]
    primary_uncertainty_method: str
    cluster_variable: str
    sensitivity_methods: List[str]
    excluded_variables: List[str]
    canonical_input_filenames: List[str]
    tier2_globals_path: str
    derived_variable_specs: Dict[str, str]

@dataclass(frozen=True)
class MetadataRecord:
    file_path: Path
    run_id: str
    source_file: str
    f_variant: str
    scale: str
    prng_seed: int
    substrate_version: str
    total_ticks: int
    execution_timestamp: str
    row_count: int

# =============================================================================
# CONSTRUCTION RULES REGISTRY
# =============================================================================

def _square_of_local_density(df: pd.DataFrame, norm: NormalizedPrereg) -> pd.DataFrame:
    if 'Local_Density' not in df.columns:
        raise DerivedVariableError("Local_Density_squared", ["Local_Density"], "square_of_local_density")
    df['Local_Density_squared'] = df['Local_Density'] ** 2
    return df

def _groupwise_mean_is_active(df: pd.DataFrame, norm: NormalizedPrereg) -> pd.DataFrame:
    if not {'run_id', 'Tick', 'is_active'}.issubset(df.columns):
        raise DerivedVariableError("rho_global", ["run_id", "Tick", "is_active"], "groupwise_mean_is_active_by_run_and_tick")
    aggs = df.groupby(["run_id", "Tick"])['is_active'].mean().reset_index(name='rho_global')
    return df.merge(aggs, on=["run_id", "Tick"], how="left")

def _groupwise_mean_psi_local(df: pd.DataFrame, norm: NormalizedPrereg) -> pd.DataFrame:
    if not {'run_id', 'Tick', 'Psi_local'}.issubset(df.columns):
        raise DerivedVariableError("psi_global", ["run_id", "Tick", "Psi_local"], "groupwise_mean_psi_local_by_run_and_tick")
    aggs = df.groupby(["run_id", "Tick"])['Psi_local'].mean().reset_index(name='psi_global')
    return df.merge(aggs, on=["run_id", "Tick"], how="left")

def _seven_bin_categorical(df: pd.DataFrame, norm: NormalizedPrereg) -> pd.DataFrame:
    if 'Tick' not in df.columns:
        raise DerivedVariableError("epoch", ["Tick"], "seven_bin_categorical_from_tick")
    bins = [-1, 99, 499, 999, 1499, 1999, 2499, 2999]
    df['epoch'] = pd.cut(df['Tick'], bins=bins, labels=False, include_lowest=True)
    return df

def _eta_floor_inversion(df: pd.DataFrame, norm: NormalizedPrereg) -> pd.DataFrame:
    if 'p_act' not in df.columns:
        raise DerivedVariableError("logit_p_base", ["p_act"], "eta_floor_inversion_of_p_base")
    eta = norm.outcome_eta if norm.outcome_eta is not None else 0.01
    df['logit_p_base'], _ = eta_floor_inversion(df['p_act'], eta=eta)
    return df

CONSTRUCTION_REGISTRY = {
    "square_of_local_density": _square_of_local_density,
    "groupwise_mean_is_active_by_run_and_tick": _groupwise_mean_is_active,
    "groupwise_mean_psi_local_by_run_and_tick": _groupwise_mean_psi_local,
    "seven_bin_categorical_from_tick": _seven_bin_categorical,
    "eta_floor_inversion_of_p_base": _eta_floor_inversion
}

ETA_REQUIRED_RULES = {"eta_floor_inversion_of_p_base"}

# =============================================================================
# INTAKE FUNCTIONS
# =============================================================================

def load_prereg(path: Path) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def _extract_formula_vars(formula: str) -> set:
    try:
        desc = patsy.ModelDesc.from_formula(formula)
    except Exception as e:
        raise PreregSchemaError("formula", "valid Patsy formula", f"Parse Error: {e}", "Formula Parse")
    
    terms = desc.lhs_termlist + desc.rhs_termlist
    vars_set = set()
    for term in terms:
        for factor in term.factors:
            name = factor.name()
            # Unwrap C()
            m = re.match(r"^C\(([^,)]+)", name)
            if m:
                vars_set.add(m.group(1).strip())
            else:
                vars_set.add(name.strip())
    return vars_set

def normalize_prereg(spec: dict) -> NormalizedPrereg:
    def req(field, expected_type, parent=spec, path="root"):
        if field not in parent:
            raise PreregSchemaError(f"{path}.{field}", expected_type.__name__, "Missing")
        val = parent[field]
        if not isinstance(val, expected_type):
            raise PreregSchemaError(f"{path}.{field}", expected_type.__name__, type(val).__name__)
        return val

    # Identity
    prereg_id = req("prereg_id", str)
    prereg_version = req("prereg_version", str)

    # Outcome
    outcome = req("outcome", dict)
    out_name = req("name", str, outcome, "outcome")
    out_const = req("construction", str, outcome, "outcome")
    
    if out_const not in CONSTRUCTION_REGISTRY:
        raise PreregSchemaError("outcome.construction", f"key in registry", out_const)
        
    out_eta = outcome.get("eta")
    if out_const in ETA_REQUIRED_RULES and not isinstance(out_eta, float):
        raise PreregSchemaError("outcome.eta", "float", type(out_eta).__name__)

    # Model
    mod_fam = req("model_family", str)
    valid_fams = {"ols", "logit", "fractional_logit", "multinomial_logistic"}
    if mod_fam not in valid_fams:
        raise PreregSchemaError("model_family", f"enum {valid_fams}", mod_fam)

    raw_formula = req("formula", str)
    f_role = req("formula_role", str)
    if f_role != "authoritative":
        raise PreregSchemaError("formula_role", "'authoritative'", f_role)

    # Auto-wrap categoricals idempotently
    formula = raw_formula
    for cat_var in CATEGORICAL_VARIABLES:
        # Wrap if standalone, ignore if already inside C()
        formula = re.sub(rf"(?<!C\()\b{cat_var}\b(?!\))", f"C({cat_var})", formula)

    # Predictors & Interactions
    predictors = req("predictors", list)
    interactions = spec.get("interactions", [])
    if not isinstance(interactions, list):
        raise PreregSchemaError("interactions", "list", type(interactions).__name__)

    # Uncertainty
    uncert = req("uncertainty_method", dict)
    pri_uncert = req("primary", str, uncert, "uncertainty_method")
    raw_clust = req("cluster_variable", str, uncert, "uncertainty_method")
    
    if raw_clust not in CLUSTER_VARIABLE_ALIASES:
        raise PreregSchemaError("uncertainty_method.cluster_variable", f"key in aliases", raw_clust)
    cluster_var = CLUSTER_VARIABLE_ALIASES[raw_clust]
    
    sens = uncert.get("sensitivity", [])
    if not isinstance(sens, list):
        raise PreregSchemaError("uncertainty_method.sensitivity", "list", type(sens).__name__)

    # Excluded
    excluded = req("excluded_variables", list)

    # Inputs
    input_files = req("canonical_input_filenames", list)
    t2_path = req("tier2_globals_path", str)

    # Derived
    derived = spec.get("derived_variables", {})
    if not isinstance(derived, dict):
        raise PreregSchemaError("derived_variables", "dict", type(derived).__name__)
        
    for k, v in derived.items():
        if v not in CONSTRUCTION_REGISTRY:
            raise PreregSchemaError(f"derived_variables.{k}", "key in registry", v)

    # VALIDATIONS (Items 4 and 5)
    form_vars = _extract_formula_vars(formula)
    
    for p in predictors:
        if p not in form_vars:
            raise PreregSchemaError("predictors", "subset of formula variables", f"'{p}' missing from formula")
            
    for i in interactions:
        comps = [c.strip() for c in i.split(':')]
        for c in comps:
            if c not in form_vars:
                raise PreregSchemaError("interactions", "components in formula variables", f"'{c}' missing from formula")

    form_var_check_pool = set(predictors) | {c.strip() for i in interactions for c in i.split(':')} | CATEGORICAL_VARIABLES | set(derived.keys()) | {out_name}
    
    for fv in form_vars:
        if fv not in form_var_check_pool:
            raise PreregSchemaError("formula", "variables declared in predictors/interactions/derived", f"Undeclared: {fv}")

    excl_set = set(excluded)
    pred_int_form_set = set(predictors) | {c.strip() for i in interactions for c in i.split(':')} | form_vars
    contradiction = excl_set.intersection(pred_int_form_set)
    if contradiction:
        raise PreregSchemaError("excluded_variables", "disjoint from active variables", f"Contradiction: {contradiction}")

    return NormalizedPrereg(
        prereg_id=prereg_id, prereg_version=prereg_version, outcome_name=out_name, outcome_construction=out_const,
        outcome_eta=out_eta, model_family=mod_fam, formula=formula, formula_role=f_role, predictors=predictors,
        interactions=interactions, primary_uncertainty_method=pri_uncert, cluster_variable=cluster_var,
        sensitivity_methods=sens, excluded_variables=excluded, canonical_input_filenames=input_files,
        tier2_globals_path=t2_path, derived_variable_specs=derived
    )

def load_canonical_inputs(normalized: NormalizedPrereg) -> Tuple[pd.DataFrame, List[MetadataRecord]]:
    project_root, flight2_pq_dir, _ = get_paths()
    dfs = []
    records = []

    for fname in normalized.canonical_input_filenames:
        fpath = flight2_pq_dir / fname
        if not fpath.exists():
            raise CanonicalInputError(fname, "File existence", "load_canonical_inputs")

        meta = pq.read_metadata(fpath)
        custom_meta = meta.metadata or {}
        
        def get_m(key):
            val = custom_meta.get(key.encode())
            if val is None:
                raise CanonicalInputError(fname, f"Parquet custom metadata: {key}", "load_canonical_inputs")
            return val.decode()

        f_variant = get_m("F_variant")
        scale_raw = get_m("Scale")
        scale = "40x40" if "40" in scale_raw else "20x20"
        
        run_id = fpath.stem
        
        # Build Record
        rec = MetadataRecord(
            file_path=fpath, run_id=run_id, source_file=fname, f_variant=f_variant, scale=scale,
            prng_seed=int(get_m("PRNG_seed") if b"PRNG_seed" in custom_meta else 0),
            substrate_version=custom_meta.get(b"substrate_version", b"").decode(),
            total_ticks=int(custom_meta.get(b"total_ticks", b"0").decode() or 0),
            execution_timestamp=custom_meta.get(b"execution_timestamp", b"").decode(),
            row_count=meta.num_rows
        )
        records.append(rec)

        # Load DF
        df_part = pd.read_parquet(fpath)
        df_part['run_id'] = run_id
        df_part['source_file'] = fname
        dfs.append(df_part)

    return pd.concat(dfs, ignore_index=True), records

def promote_metadata_to_columns(df: pd.DataFrame, metadata: List[MetadataRecord]) -> pd.DataFrame:
    meta_df = pd.DataFrame([
        {'run_id': m.run_id, 'F_variant': m.f_variant, 'scale': m.scale}
        for m in metadata
    ])
    
    if meta_df.isnull().values.any():
        raise MetadataPromotionError("ALL", "Null fields detected in metadata records.")
        
    merged = df.merge(meta_df, on='run_id', how='left')
    if merged['F_variant'].isnull().any():
        bad_runs = df[merged['F_variant'].isnull()]['run_id'].unique()
        raise MetadataPromotionError(str(bad_runs), "Matching MetadataRecord", "promote_metadata_to_columns")
        
    return merged

def construct_derived_variables(df: pd.DataFrame, normalized: NormalizedPrereg) -> pd.DataFrame:
    for var_name, rule_id in normalized.derived_variable_specs.items():
        if rule_id not in CONSTRUCTION_REGISTRY:
            raise DerivedVariableError(var_name, "N/A", rule_id, "Unknown Rule")
        rule_func = CONSTRUCTION_REGISTRY[rule_id]
        df = rule_func(df, normalized)
    return df

def attach_tier2_globals(df: pd.DataFrame, normalized: NormalizedPrereg) -> pd.DataFrame:
    project_root, _, _ = get_paths()
    t2_path = project_root / normalized.tier2_globals_path
    
    if not t2_path.exists():
        raise CanonicalInputError(normalized.tier2_globals_path, "File existence", "attach_tier2_globals")
        
    t2_df = pd.read_csv(t2_path)
    if not {'run_id', 'Tick'}.issubset(t2_df.columns):
        raise CanonicalInputError(normalized.tier2_globals_path, "run_id or Tick column", "attach_tier2_globals")
        
    orig_rows = len(df)
    merged = df.merge(t2_df, on=['run_id', 'Tick'], how='left')
    
    if len(merged) != orig_rows:
        raise CanonicalInputError(normalized.tier2_globals_path, "1:1 Merge Integrity", f"Row count changed {orig_rows} -> {len(merged)}")
        
    return merged

def validate_formula_variables(df: pd.DataFrame, normalized: NormalizedPrereg) -> None:
    form_vars = _extract_formula_vars(normalized.formula)
    missing = form_vars - set(df.columns)
    if missing:
        raise FormulaVariableError(list(missing), list(df.columns), "validate_formula_variables")

def echo_intake_summary(df: pd.DataFrame, metadata: List[MetadataRecord], normalized: NormalizedPrereg) -> str:
    lines = ["=== PHASE 4B INTAKE SUMMARY ==="]
    
    lines.append("\n[Resolved Input Files]")
    for m in metadata:
        lines.append(f"  - {m.source_file}: {m.row_count} rows")
        
    lines.append("\n[Promoted Metadata Columns]")
    for m in metadata:
        lines.append(f"  - {m.run_id} -> F_variant: {m.f_variant}, scale: {m.scale}")
        
    lines.append("\n[Constructed Derived Variables]")
    for k, v in normalized.derived_variable_specs.items():
        lines.append(f"  - {k} (via {v})")
        
    lines.append(f"\n[Outcome]: {normalized.outcome_name} (via {normalized.outcome_construction})")
    lines.append(f"[Model Family]: {normalized.model_family}")
    lines.append(f"[Cluster Variable (Post-Alias)]: {normalized.cluster_variable}")
    lines.append(f"[Independent Run Count]: {len(metadata)}")
    
    lines.append(f"\n[Resolved Formula]: {normalized.formula}")
    form_vars = _extract_formula_vars(normalized.formula)
    lines.append(f"[Formula Variables Extracted]: {list(form_vars)}")
    
    missing = form_vars - set(df.columns)
    lines.append(f"[Formula Variables Missing]: {'none' if not missing else list(missing)}")
    
    return "\n".join(lines)