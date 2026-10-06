from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class RiskFactorsInput(BaseModel):
    criticality: float = Field(..., ge=0.0, le=100.0, description="Business criticality score (0-100)")
    uniqueness: float = Field(..., ge=0.0, le=100.0, description="Knowledge uniqueness score (0-100)")
    dependency: float = Field(..., ge=0.0, le=100.0, description="Organizational dependency score (0-100)")
    documentation_gap: float = Field(..., ge=0.0, le=100.0, description="Documentation gap score (0-100)")
    availability_risk: float = Field(..., ge=0.0, le=100.0, description="Expert availability risk score (0-100)")

class RiskFactorBreakdown(BaseModel):
    factor_name: str
    raw_score: float
    weight: float
    weighted_score: float
    interpretation: str

class RiskCalculationRequest(BaseModel):
    factors: RiskFactorsInput
    assessment_method: str = "rule_based"  # rule_based, ml, hybrid
    assessment_notes: Optional[str] = None

class RiskCalculationResponse(BaseModel):
    risk_id: Optional[int] = None
    knowledge_id: Optional[int] = None
    risk_score: float
    risk_level: str  # low, medium, high, critical
    factors: RiskFactorsInput
    factor_breakdown: List[RiskFactorBreakdown]
    recommendations: List[str]
    ml_predicted_level: Optional[str] = None
    ml_confidence: Optional[float] = None
    calculated_at: datetime

class TopRiskItem(BaseModel):
    knowledge_id: int
    title: str
    category: str
    risk_score: float
    risk_level: str
    experts_count: int
    primary_factor: str

class RiskDashboardSummary(BaseModel):
    total_knowledge_items: int
    critical_risk_count: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    average_risk_score: float

class RiskDistribution(BaseModel):
    critical: float
    high: float
    medium: float
    low: float

class PreservationProgressSummary(BaseModel):
    recommended: int
    planned: int
    in_progress: int
    completed: int

class RiskDashboardResponse(BaseModel):
    summary: RiskDashboardSummary
    risk_distribution: RiskDistribution
    top_critical_items: List[TopRiskItem]
    preservation_progress: PreservationProgressSummary
