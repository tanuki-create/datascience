from __future__ import annotations

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


def require_dependencies():
    try:
        import numpy as np
        import pandas as pd
        import sklearn  # noqa: F401
    except ModuleNotFoundError as exc:
        missing = exc.name or "a required package"
        sys.exit(
            "This example requires pandas, numpy, and scikit-learn. "
            f"Missing package: {missing}. "
            "Install them with: python -m pip install pandas numpy scikit-learn"
        )

    return np, pd


def make_one_hot_encoder():
    from sklearn.preprocessing import OneHotEncoder

    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)
