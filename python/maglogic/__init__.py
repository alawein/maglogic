"""
MagLogic: Nanomagnetic Logic Simulation Suite

A comprehensive computational magnetism framework for nanomagnetic logic (NML) 
device simulation and analysis. This package provides tools for:

- OOMMF and MuMax3 simulation analysis
- Logic gate and cellular automata modeling
- Magnetization dynamics visualization
- Machine learning-based state classification
- High-performance computing integration

Author: Meshal Alawein
Email: meshal@berkeley.edu
Institution: University of California, Berkeley
License: MIT

Example Usage:
    >>> import maglogic
    >>> from maglogic.demos import demo_nand_nor
    >>> result = demo_nand_nor.run_simulation(clock_angle=60, input_A=1, input_B=0)
    >>> print(f"Logic output: {result['logic_output']}")
"""

# Version information
__version__ = "1.0.0"
__author__ = "Meshal Alawein"
__email__ = "meshal@berkeley.edu"
__license__ = "MIT"
__copyright__ = "Copyright 2025, University of California, Berkeley"

# Package metadata
__title__ = "MagLogic"
__description__ = "Nanomagnetic Logic Simulation Suite"
__url__ = "https://github.com/alawein/maglogic"
__download_url__ = "https://github.com/alawein/maglogic/releases"
__docs_url__ = "https://github.com/alawein/maglogic/tree/main/docs"
__paper_url__ = "https://doi.org/10.1109/LMAG.2019.2912398"

# Import version check
import sys
if sys.version_info < (3, 8):
    raise ImportError(
        f"MagLogic requires Python 3.8 or higher. "
        f"Current version: {sys.version_info.major}.{sys.version_info.minor}"
    )

# ---------------------------------------------------------------------------
# Lazy imports -- heavy dependencies (NumPy, SciPy, Matplotlib) are loaded on
# first access rather than at package import time.  This keeps `import maglogic`
# fast (~0.01 s) while still exposing the same public API.
# ---------------------------------------------------------------------------

import importlib as _importlib

# Map of public names to (module_path, attribute_name) for lazy loading
_LAZY_IMPORTS: dict = {
    # core.constants  (wildcard -- re-export the two main dicts)
    "PHYSICAL_CONSTANTS": (".core.constants", "PHYSICAL_CONSTANTS"),
    "MATERIAL_CONSTANTS": (".core.constants", "MATERIAL_CONSTANTS"),
    # core.units  (wildcard)
    # Parsers
    "OOMMFParser": (".parsers.oommf_parser", "OOMMFParser"),
    "MuMax3Parser": (".parsers.mumax3_parser", "MuMax3Parser"),
    # Analysis
    "MagnetizationAnalyzer": (".analysis.magnetization", "MagnetizationAnalyzer"),
    # Visualization
    "BerkeleyStyle": (".visualization.berkeley_style", "BerkeleyStyle"),
    "berkeley_style": (".visualization.berkeley_style", "berkeley_style"),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_path, attr = _LAZY_IMPORTS[name]
        try:
            mod = _importlib.import_module(module_path, __name__)
        except ImportError as e:
            import warnings
            warnings.warn(
                f"Could not import {module_path}: {e}. "
                f"Install complete dependencies with: pip install maglogic[all]",
                ImportWarning,
            )
            raise AttributeError(name) from e
        val = getattr(mod, attr)
        # Cache on the module so __getattr__ is not called again
        globals()[name] = val
        return val
    raise AttributeError(f"module 'maglogic' has no attribute {name!r}")

# Define what gets imported with "from maglogic import *"
__all__ = [
    # Version info
    "__version__", "__author__", "__email__", "__license__",
    
    # Core classes
    "OOMMFParser", "MuMax3Parser", "MagnetizationAnalyzer", 
    "BerkeleyStyle", 
    # TODO: Add when implemented: "EnergyAnalyzer", "LogicAnalyzer", "MagnetizationPlotter"
    
    # Utilities
    "berkeley_style",
    # TODO: Add when implemented: "get_config", "set_config"
    
    # Constants (imported from core.constants)
    "PHYSICAL_CONSTANTS", "MATERIAL_CONSTANTS",
]

def get_version():
    """Get the current version of MagLogic."""
    return __version__

def get_info():
    """Get comprehensive package information."""
    return {
        "name": __title__,
        "version": __version__,
        "description": __description__,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "url": __url__,
        "docs_url": __docs_url__,
        "paper_url": __paper_url__,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    }

def check_dependencies():
    """
    Check if all required dependencies are installed and working.
    
    Returns:
        dict: Status of each dependency group
    """
    status = {
        "core": True,
        "visualization": True,
        "ml": True,
        "gui": True,
        "hpc": True,
        "simulators": {"oommf": False, "mumax3": False}
    }
    
    # Check core scientific computing dependencies
    try:
        import numpy, scipy, matplotlib, pandas
    except ImportError:
        status["core"] = False
    
    # Check visualization dependencies
    try:
        import plotly, seaborn, bokeh
    except ImportError:
        status["visualization"] = False
    
    # Check machine learning dependencies
    try:
        import sklearn
        try:
            import torch
        except ImportError:
            pass
        try:
            import tensorflow
        except ImportError:
            pass
    except ImportError:
        status["ml"] = False
    
    # Check GUI dependencies
    try:
        import PyQt5
    except ImportError:
        status["gui"] = False
    
    # Check HPC dependencies
    try:
        import mpi4py, h5py
    except ImportError:
        status["hpc"] = False
    
    # Check simulator availability
    import subprocess
    import os
    
    # Check OOMMF
    try:
        result = subprocess.run(
            ["oommf", "+version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            status["simulators"]["oommf"] = True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Check MuMax3
    try:
        result = subprocess.run(
            ["mumax3", "-version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            status["simulators"]["mumax3"] = True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return status

def print_system_info():
    """Print comprehensive system and dependency information."""
    import platform
    
    print("="*60)
    print("MagLogic System Information")
    print("="*60)
    
    # Package info
    info = get_info()
    print(f"Package: {info['name']} v{info['version']}")
    print(f"Author: {info['author']} ({info['email']})")
    print(f"License: {info['license']}")
    print(f"Documentation: {info['docs_url']}")
    
    # System info
    print(f"\nSystem: {platform.system()} {platform.release()}")
    print(f"Python: {info['python_version']}")
    print(f"Architecture: {platform.machine()}")
    
    # Dependency status
    print("\nDependency Status:")
    deps = check_dependencies()
    for category, status in deps.items():
        if category == "simulators":
            print(f"  Simulators:")
            for sim, available in status.items():
                status_str = "✓ Available" if available else "✗ Not found"
                print(f"    {sim.upper()}: {status_str}")
        else:
            status_str = "✓ Available" if status else "✗ Missing"
            print(f"  {category.capitalize()}: {status_str}")
    
    print("="*60)

# TODO: Set up logging configuration when utils module is implemented
# from .utils.logging_config import setup_logging
# setup_logging()

# NOTE: berkeley_style.setup() is no longer called eagerly at import time.
# Users who need Berkeley-styled plots should call:
#   from maglogic.visualization.berkeley_style import berkeley_style
#   berkeley_style.setup()
