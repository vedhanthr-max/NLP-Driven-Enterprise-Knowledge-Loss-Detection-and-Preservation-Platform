import os
import json
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import get_current_user, require_role
from app.models.entities import User, MLModel, AuditLog
from app.schemas.ml import MLPredictRequest, MLPredictResponse, MLTrainingResponse, MLModelMetrics
from app.ml.classifier import predict_risk_level
from app.ml.trainer import train_and_evaluate_models, MODEL_STORAGE_PATH

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

@router.get("/metrics")
def get_model_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve actual empirical training and evaluation metrics from disk/database."""
    metadata_path = os.path.join(MODEL_STORAGE_PATH, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            data = json.load(f)
            return data

    # If metadata file doesn't exist yet, train models
    result = train_and_evaluate_models(num_samples=700, save_best=True)
    return result

@router.post("/predict", response_model=MLPredictResponse)
def predict_risk(
    req: MLPredictRequest,
    current_user: User = Depends(get_current_user)
):
    """Perform real-time machine learning risk classification."""
    res = predict_risk_level(
        criticality=req.criticality,
        uniqueness=req.uniqueness,
        dependency=req.dependency,
        documentation_gap=req.documentation_gap,
        availability_risk=req.availability_risk,
        num_experts=req.num_experts or 1,
        num_systems=req.num_systems or 2,
        doc_length=req.doc_length or 1000
    )
    return MLPredictResponse(**res)

@router.post("/train", response_model=MLTrainingResponse)
def trigger_training(
    current_user: User = Depends(require_role(["admin", "manager"])),
    db: Session = Depends(get_db)
):
    """Trigger model re-training, cross-validation, and empirical evaluation."""
    result = train_and_evaluate_models(num_samples=700, save_best=True)

    # Record best model in database
    for m in result["models_evaluated"]:
        ml_rec = MLModel(
            organization_id=current_user.organization_id,
            model_name=m["model_name"],
            model_type=m["model_type"],
            version=m["version"],
            model_path="ml_models/risk_classifier.pkl",
            scaler_path="ml_models/scaler.pkl",
            accuracy=m["accuracy"],
            precision=m["precision"],
            recall=m["recall"],
            f1_score=m["f1_score"],
            training_data_size=result["samples_count"],
            training_samples=result["samples_count"],
            features_used=list(m["feature_importances"].keys()),
            hyperparameters={},
            is_active=m["is_active"],
            performance_notes=f"CV F1 mean: {m.get('cv_f1_mean')}"
        )
        db.add(ml_rec)

    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="train_model",
        resource_type="ml_model",
        resource_name=result["best_model_name"],
        status="success"
    ))
    db.commit()

    return MLTrainingResponse(**result)
