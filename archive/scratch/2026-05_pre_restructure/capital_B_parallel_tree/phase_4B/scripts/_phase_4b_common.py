"""
Phase 4b Common Utilities
Core analytics dependencies, environment verification, and architectural registers.
"""

import sys
import logging
from pathlib import Path

def verify_environment():
    """
    Enforces strict environment parity. 
    Verifies all required Phase 4b analytical dependencies are present before execution.
    """
    missing = []
    
    try:
        import statsmodels.api as sm
    except ImportError:
        missing.append('statsmodels')
        
    try:
        import yaml
    except ImportError:
        missing.append('pyyaml')
        
    try:
        import scipy
    except ImportError:
        missing.append('scipy')
        
    try:
        import pyarrow
    except ImportError:
        missing.append('pyarrow')
        
    if missing:
        raise RuntimeError(
            f"Missing dependency: {', '.join(missing)}. "
            f"Please run 'pip install {' '.join(missing)}'."
        )

def setup_phase4_logger(name):
    """Standardized logging configuration for all Phase 4b analytics scripts."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('--- %(levelname)s: %(message)s ---')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

# ==========================================
# IMPLEMENTATION CHOICE REGISTER
# ==========================================
# Standing Protocol: All implementation choices in simulations must be versioned 
# and documented as swappable modules.
#
# NOTE: "Structural conduciveness" is restricted strictly as a descriptive name 
# for the variable Lambda. It is not a substitute for Lambda in technical execution.
#
# DO NOT use rejected legacy terminology in these modules.
# ==========================================

ACTIVE_MODULE_VERSIONS = {
    "mu_calculation": "mu_linear_v0",
    "lambda_variable": "lambda_base_v1", 
    "spatial_topology": "toroidal_v2"
}

def get_active_module(module_type):
    """Retrieves the currently versioned implementation choice for a given module."""
    return ACTIVE_MODULE_VERSIONS.get(module_type, "unregistered_module")