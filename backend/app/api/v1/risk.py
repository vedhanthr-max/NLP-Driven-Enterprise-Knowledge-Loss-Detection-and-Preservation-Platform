from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.services.risk_service import RiskService
from app.models.entities import User, RiskScore, KnowledgeItem, AuditLog
from app.schemas.risk import (
    RiskCalculationRequest, RiskCalculationResponse, RiskDashboardResponse, RiskFactorsInput
)
from app.risk.scoring import calculate_risk_score, classify_risk_level
from app.risk.explainability import generate_risk_breakdown, generate_recommendations
from app.ml.classifier import predict_risk_level

router = APIRouter(prefix="/risk", tags=["Risk Analysis"])

@router.get("/dashboard", response_model=RiskDashboardResponse)
def get_risk_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve executive risk metrics, KPI counts, and distribution percentages."""
    return RiskService.get_organization_dashboard(db, current_user.organization_id)

@router.post("/analyze/{knowledge_id}", response_model=RiskCalculationResponse)
def analyze_risk(
    knowledge_id: int,
    req: RiskCalculationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calculate, persist, and explain risk assessment for a specific knowledge item."""
    factors = req.factors
    risk_record = RiskService.calculate_and_save_risk(
        db=db,
        knowledge_id=knowledge_id,
        criticality=factors.criticality,
        uniqueness=factors.uniqueness,
        dependency=factors.dependency,
        documentation_gap=factors.documentation_gap,
        availability_risk=factors.availability_risk,
        assessment_method=req.assessment_method,
        assessment_notes=req.assessment_notes,
        current_user_id=current_user.user_id
    )

    breakdown = generate_risk_breakdown(
        factors.criticality, factors.uniqueness, factors.dependency,
        factors.documentation_gap, factors.availability_risk
    )
    recommendations = generate_recommendations(
        factors.criticality, factors.uniqueness, factors.dependency,
        factors.documentation_gap, factors.availability_risk,
        risk_record.risk_level
    )

    db.add(AuditLog(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        action_type="assess",
        resource_type="risk",
        resource_id=risk_record.risk_id,
        resource_name=f"Risk: {risk_record.risk_level} ({risk_record.risk_score})",
        status="success"
    ))
    db.commit()

    return RiskCalculationResponse(
        risk_id=risk_record.risk_id,
        knowledge_id=knowledge_id,
        risk_score=risk_record.risk_score,
        risk_level=risk_record.risk_level,
        factors=factors,
        factor_breakdown=breakdown,
        recommendations=recommendations,
        ml_predicted_level=risk_record.ml_predicted_level,
        ml_confidence=risk_record.ml_confidence,
        calculated_at=risk_record.calculated_at
    )

@router.post("/simulate", response_model=RiskCalculationResponse)
def simulate_risk(req: RiskFactorsInput):
    """
    Simulate risk calculation on arbitrary factor sliders without persisting.
    Useful for interactive frontend sandbox studio.
    """
    score = calculate_risk_score(
        req.criticality, req.uniqueness, req.dependency,
        req.documentation_gap, req.availability_risk
    )
    level = classify_risk_level(score)
    breakdown = generate_risk_breakdown(
        req.criticality, req.uniqueness, req.dependency,
        req.documentation_gap, req.availability_risk
    )
    recommendations = generate_recommendations(
        req.criticality, req.uniqueness, req.dependency,
        req.documentation_gap, req.availability_risk, level
    )
    ml_pred = predict_risk_level(
        req.criticality, req.uniqueness, req.dependency,
        req.documentation_gap, req.availability_risk
    )

    return RiskCalculationResponse(
        risk_id=None,
        knowledge_id=None,
        risk_score=score,
        risk_level=level,
        factors=req,
        factor_breakdown=breakdown,
        recommendations=recommendations,
        ml_predicted_level=ml_pred["predicted_level"],
        ml_confidence=ml_pred["confidence"],
        calculated_at=datetime.now(timezone.utc)
    )

@router.get("/history/{knowledge_id}", response_model=List[RiskCalculationResponse])
def get_risk_history(
    knowledge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve historical risk assessments for a knowledge item."""
    scores = db.query(RiskScore).filter(
        RiskScore.knowledge_id == knowledge_id,
        RiskScore.organization_id == current_user.organization_id
    ).order_by(RiskScore.calculated_at.desc()).all()

    out = []
    for r in scores:
        factors = RiskFactorsInput(
            criticality=r.criticality,
            uniqueness=r.uniqueness,
            dependency=r.dependency,
            documentation_gap=r.documentation_gap,
            availability_risk=r.availability_risk
        )
        breakdown = generate_risk_breakdown(
            r.criticality, r.uniqueness, r.dependency,
            r.documentation_gap, r.availability_risk
        )
        recommendations = generate_recommendations(
            r.criticality, r.uniqueness, r.dependency,
            r.documentation_gap, r.availability_risk, r.risk_level
        )
        out.append(RiskCalculationResponse(
            risk_id=r.risk_id,
            knowledge_id=r.knowledge_id,
            risk_score=r.risk_score,
            risk_level=r.risk_level,
            factors=factors,
            factor_breakdown=breakdown,
            recommendations=recommendations,
            ml_predicted_level=r.ml_predicted_level,
            ml_confidence=r.ml_confidence,
            calculated_at=r.calculated_at
        ))
    return out
