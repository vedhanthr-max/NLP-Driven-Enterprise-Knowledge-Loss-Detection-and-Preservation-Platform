from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class MLPredictRequest(BaseModel):
    criticality: float = Field(..., ge=0.0, le=100.0)
    uniqueness: float = Field(..., ge=0.0, le=100.0)
    dependency: float = Field(..., ge=0.0, le=100.0)
    documentation_gap: float = Field(..., ge=0.0, le=100.0)
    availability_risk: float = Field(..., ge=0.0, le=100.0)
    num_experts: Optional[int] = 1
    num_systems: Optional[int] = 2
    doc_length: Optional[int] = 500

class MLPredictResponse(BaseModel):
    predicted_level: str  # low, medium, high, critical
    confidence: float
    class_probabilities: Dict[str, float]
    model_version: str
    model_name: str

class MLModelMetrics(BaseModel):
    model_name: str
    model_type: str
    version: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: List[List[int]]
    feature_importances: Dict[str, float] = {}
    is_active: bool
    trained_at: datetime

class MLTrainingResponse(BaseModel):
    status: str
    message: str
    samples_count: int
    models_evaluated: List[MLModelMetrics]
    best_model_name: str
    best_model_accuracy: float
    best_model_f1: float
