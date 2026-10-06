import os
import joblib
import json
from typing import Dict, Any, Tuple
from app.ml.feature_engineering import prepare_single_feature_vector, CLASSES
from app.ml.trainer import MODEL_STORAGE_PATH, train_and_evaluate_models

_model = None
_scaler = None

def get_classifier():
    """Load or train model and scaler for inference."""
    global _model, _scaler
    if _model is not None and _scaler is not None:
        return _model, _scaler

    model_path = os.path.join(MODEL_STORAGE_PATH, "risk_classifier.pkl")
    scaler_path = os.path.join(MODEL_STORAGE_PATH, "scaler.pkl")

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        # Trigger training to build models
        train_and_evaluate_models(num_samples=700, save_best=True)

    try:
        _model = joblib.load(model_path)
        _scaler = joblib.load(scaler_path)
        return _model, _scaler
    except Exception:
        # Re-train if corrupt
        train_and_evaluate_models(num_samples=700, save_best=True)
        _model = joblib.load(model_path)
        _scaler = joblib.load(scaler_path)
        return _model, _scaler

def predict_risk_level(
    criticality: float,
    uniqueness: float,
    dependency: float,
    documentation_gap: float,
    availability_risk: float,
    num_experts: int = 1,
    num_systems: int = 2,
    doc_length: int = 1000
) -> Dict[str, Any]:
    """
    Execute ML risk level prediction with confidence and class probabilities.
    """
    model, scaler = get_classifier()
    features = prepare_single_feature_vector(
        criticality=criticality,
        uniqueness=uniqueness,
        dependency=dependency,
        documentation_gap=documentation_gap,
        availability_risk=availability_risk,
        num_experts=num_experts,
        num_systems=num_systems,
        doc_length=doc_length
    )

    scaled_features = scaler.transform(features)
    predicted_class = str(model.predict(scaled_features)[0])

    class_probs = {}
    confidence = 0.85
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(scaled_features)[0]
        model_classes = list(model.classes_)
        for c, p in zip(model_classes, probabilities):
            class_probs[str(c)] = round(float(p), 4)
        confidence = round(float(max(probabilities)), 4)
    else:
        for c in CLASSES:
            class_probs[c] = 1.0 if c == predicted_class else 0.0

    return {
        "predicted_level": predicted_class,
        "confidence": confidence,
        "class_probabilities": class_probs,
        "model_version": "1.0.0",
        "model_name": type(model).__name__
    }
