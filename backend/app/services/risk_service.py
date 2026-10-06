from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import KnowledgeNotFoundException
from app.models.entities import KnowledgeItem, RiskScore, PreservationAction, User, KnowledgeExpert
from app.risk.scoring import calculate_risk_score, classify_risk_level
from app.risk.explainability import generate_risk_breakdown, generate_recommendations
from app.ml.classifier import predict_risk_level

class RiskService:
    @staticmethod
    def calculate_and_save_risk(
        db: Session,
        knowledge_id: int,
        criticality: float,
        uniqueness: float,
        dependency: float,
        documentation_gap: float,
        availability_risk: float,
        assessment_method: str = "rule_based",
        assessment_notes: Optional[str] = None,
        current_user_id: Optional[int] = None
    ) -> RiskScore:
        """
        Execute full risk calculation, ML prediction, factor breakdown, and preservation recommendations.
        """
        knowledge = db.query(KnowledgeItem).filter(KnowledgeItem.knowledge_id == knowledge_id).first()
        if not knowledge:
            raise KnowledgeNotFoundException(knowledge_id)

        # 1. Deterministic Score Calculation
        risk_score_val = calculate_risk_score(
            criticality=criticality,
            uniqueness=uniqueness,
            dependency=dependency,
            documentation_gap=documentation_gap,
            availability_risk=availability_risk
        )
        risk_level = classify_risk_level(risk_score_val)

        # 2. Machine Learning Inference
        num_experts = len(knowledge.experts) if knowledge.experts else 1
        ml_result = predict_risk_level(
            criticality=criticality,
            uniqueness=uniqueness,
            dependency=dependency,
            documentation_gap=documentation_gap,
            availability_risk=availability_risk,
            num_experts=num_experts,
            num_systems=3,
            doc_length=len(knowledge.description or "")
        )

        # Mark previous risk scores as not latest
        db.query(RiskScore).filter(
            RiskScore.knowledge_id == knowledge_id,
            RiskScore.is_latest == True
        ).update({"is_latest": False})

        # Create new RiskScore record
        risk_record = RiskScore(
            organization_id=knowledge.organization_id,
            knowledge_id=knowledge_id,
            criticality=criticality,
            uniqueness=uniqueness,
            dependency=dependency,
            documentation_gap=documentation_gap,
            availability_risk=availability_risk,
            risk_score=risk_score_val,
            risk_level=risk_level,
            ml_predicted_level=ml_result["predicted_level"],
            ml_confidence=ml_result["confidence"],
            prediction_model_version=ml_result["model_version"],
            assessment_method=assessment_method,
            assessed_by=current_user_id,
            assessment_notes=assessment_notes,
            is_latest=True,
            calculated_at=datetime.now(timezone.utc)
        )
        db.add(risk_record)

        # 3. Automated Preservation Recommendations for high/critical risks
        recs = generate_recommendations(
            criticality=criticality,
            uniqueness=uniqueness,
            dependency=dependency,
            documentation_gap=documentation_gap,
            availability_risk=availability_risk,
            risk_level=risk_level
        )

        # Automatically create preservation actions if high or critical
        if risk_level in ("high", "critical"):
            for rec in recs[:2]:  # Top 2 recommendations
                existing_action = db.query(PreservationAction).filter(
                    PreservationAction.knowledge_id == knowledge_id,
                    PreservationAction.action_description == rec
                ).first()
                if not existing_action:
                    action = PreservationAction(
                        organization_id=knowledge.organization_id,
                        knowledge_id=knowledge_id,
                        action_type="documentation" if "documentation" in rec.lower() else "secondary_expert",
                        action_description=rec,
                        priority=risk_level,
                        status="recommended",
                        created_by=current_user_id
                    )
                    db.add(action)

        db.commit()
        db.refresh(risk_record)
        return risk_record

    @staticmethod
    def get_organization_dashboard(db: Session, organization_id: int) -> Dict[str, Any]:
        """Aggregate organization-wide risk KPI scorecards, risk distributions, and alerts."""
        knowledge_items = db.query(KnowledgeItem).filter(
            KnowledgeItem.organization_id == organization_id
        ).all()
        total_items = len(knowledge_items)

        latest_risks = db.query(RiskScore).filter(
            RiskScore.organization_id == organization_id,
            RiskScore.is_latest == True
        ).all()

        crit_count = sum(1 for r in latest_risks if r.risk_level == "critical")
        high_count = sum(1 for r in latest_risks if r.risk_level == "high")
        med_count = sum(1 for r in latest_risks if r.risk_level == "medium")
        low_count = sum(1 for r in latest_risks if r.risk_level == "low")

        avg_score = round(sum(r.risk_score for r in latest_risks) / len(latest_risks), 2) if latest_risks else 0.0

        total_assessed = max(1, len(latest_risks))
        distribution = {
            "critical": round((crit_count / total_assessed) * 100, 1),
            "high": round((high_count / total_assessed) * 100, 1),
            "medium": round((med_count / total_assessed) * 100, 1),
            "low": round((low_count / total_assessed) * 100, 1)
        }

        # Top critical items
        sorted_risks = sorted(latest_risks, key=lambda x: x.risk_score, reverse=True)[:5]
        top_critical = []
        for r in sorted_risks:
            k = r.knowledge
            top_critical.append({
                "knowledge_id": r.knowledge_id,
                "title": k.title if k else f"Knowledge #{r.knowledge_id}",
                "category": k.category if k else "General",
                "risk_score": r.risk_score,
                "risk_level": r.risk_level,
                "experts_count": len(k.experts) if k and k.experts else 1,
                "primary_factor": "Uniqueness" if r.uniqueness >= 80 else "Criticality"
            })

        # Preservation action progress
        actions = db.query(PreservationAction).filter(
            PreservationAction.organization_id == organization_id
        ).all()
        preservation_progress = {
            "recommended": sum(1 for a in actions if a.status == "recommended"),
            "planned": sum(1 for a in actions if a.status == "planned"),
            "in_progress": sum(1 for a in actions if a.status == "in_progress"),
            "completed": sum(1 for a in actions if a.status == "completed")
        }

        return {
            "summary": {
                "total_knowledge_items": total_items,
                "critical_risk_count": crit_count,
                "high_risk_count": high_count,
                "medium_risk_count": med_count,
                "low_risk_count": low_count,
                "average_risk_score": avg_score
            },
            "risk_distribution": distribution,
            "top_critical_items": top_critical,
            "preservation_progress": preservation_progress
        }
