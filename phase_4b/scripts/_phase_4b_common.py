import sys
import numpy as np
from pathlib import Path

def verify_environment():
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("Environment verification failed: venv is not active. (sys.prefix == sys.base_prefix)")
    if sys.version_info[:2] != (3, 14):
        raise RuntimeError(f"Environment verification failed: Python 3.14.x required, found {sys.version_info.major}.{sys.version_info.minor}")
    try:
        import pandas
        import pyarrow
        import statsmodels
        import yaml
        import scipy
        import scipy.ndimage
    except ImportError as e:
        raise RuntimeError(f"Environment verification failed: Missing required dependency. {e}")

def get_paths():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    flight2_pq_dir = project_root.parent / 'flight2_outputs'
    flight2_csv_dir = project_root.parent / 'flight2_analysis_outputs'
    return project_root, flight2_pq_dir, flight2_csv_dir

def eta_floor_inversion(p_act, eta=0.01):
    p_base_raw = (p_act - eta) / (1.0 - eta)
    boundary_count = int((p_base_raw <= 0.0).sum() + (p_base_raw >= 1.0).sum())
    p_base_clipped = np.clip(p_base_raw, 1e-10, 1.0 - 1e-10)
    logit_p_base = np.log(p_base_clipped / (1.0 - p_base_clipped))
    return logit_p_base, boundary_count
