import numpy as np
import pandas as pd
from typing import Tuple, List
from sklearn.preprocessing import StandardScaler

FEATURE_NAMES = [
    "criticality", "uniqueness", "dependency", "documentation_gap",
    "availability_risk", "num_experts", "num_systems", "doc_length"
]

TARGET_NAME = "risk_level"

# Canonical ordering of class labels
CLASSES = ["low", "medium", "high", "critical"]

def extract_features(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Extract feature matrix X and target array y from DataFrame."""
    X = df[FEATURE_NAMES].values
    y = df[TARGET_NAME].values
    return X, y

def prepare_single_feature_vector(
    criticality: float,
    uniqueness: float,
    dependency: float,
    documentation_gap: float,
    availability_risk: float,
    num_experts: int = 2,
    num_systems: int = 2,
    doc_length: int = 1000
) -> np.ndarray:
    """Prepare single row 2D feature array for inference."""
    return np.array([[
        float(criticality),
        float(uniqueness),
        float(dependency),
        float(documentation_gap),
        float(availability_risk),
        float(num_experts),
        float(num_systems),
        float(doc_length)
    ]], dtype=np.float32)
