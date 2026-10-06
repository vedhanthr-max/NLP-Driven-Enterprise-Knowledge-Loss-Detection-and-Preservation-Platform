from typing import List, Dict, Any
from app.core.config import settings

def generate_risk_breakdown(
    criticality: float,
    uniqueness: float,
    dependency: float,
    documentation_gap: float,
    availability_risk: float
) -> List[Dict[str, Any]]:
    """
    Generate detailed explainability breakdown for each factor's contribution.
    """
    factors = [
        {
            "factor_name": "Knowledge Criticality",
            "raw_score": round(criticality, 2),
            "weight": settings.WEIGHT_CRITICALITY,
            "weighted_score": round(criticality * settings.WEIGHT_CRITICALITY, 2),
            "interpretation": (
                "Severe business vulnerability; core operations depend directly on this knowledge."
                if criticality >= 80 else
                "Important operational asset with notable revenue/system impact."
                if criticality >= 50 else
                "Standard supporting or informational knowledge with minor impact."
            )
        },
        {
            "factor_name": "Knowledge Uniqueness",
            "raw_score": round(uniqueness, 2),
            "weight": settings.WEIGHT_UNIQUENESS,
            "weighted_score": round(uniqueness * settings.WEIGHT_UNIQUENESS, 2),
            "interpretation": (
                "Extreme single-person dependency; critical knowledge silo with only 1 primary expert."
                if uniqueness >= 80 else
                "Limited expertise distribution; only 2-3 personnel familiar with procedures."
                if uniqueness >= 50 else
                "Well-distributed organizational knowledge across 4+ team members."
            )
        },
        {
            "factor_name": "Organizational Dependency",
            "raw_score": round(dependency, 2),
            "weight": settings.WEIGHT_DEPENDENCY,
            "weighted_score": round(dependency * settings.WEIGHT_DEPENDENCY, 2),
            "interpretation": (
                "Enterprise-wide dependency across multiple mission-critical systems and departments."
                if dependency >= 80 else
                "Multiple dependent applications or core departmental business workflows."
                if dependency >= 50 else
                "Localized dependency within a single project team."
            )
        },
        {
            "factor_name": "Documentation Gap",
            "raw_score": round(documentation_gap, 2),
            "weight": settings.WEIGHT_DOCUMENTATION_GAP,
            "weighted_score": round(documentation_gap * settings.WEIGHT_DOCUMENTATION_GAP, 2),
            "interpretation": (
                "Severe documentation void; missing architecture diagrams, runbooks, and recovery guides."
                if documentation_gap >= 70 else
                "Partial documentation exists but lacks troubleshooting or edge-case workflows."
                if documentation_gap >= 40 else
                "Thorough, up-to-date documentation with step-by-step procedures and code examples."
            )
        },
        {
            "factor_name": "Expert Availability Risk",
            "raw_score": round(availability_risk, 2),
            "weight": settings.WEIGHT_AVAILABILITY_RISK,
            "weighted_score": round(availability_risk * settings.WEIGHT_AVAILABILITY_RISK, 2),
            "interpretation": (
                "High departure or retirement risk; immediate succession planning required."
                if availability_risk >= 75 else
                "Moderate availability vulnerability due to role seniority or market demand."
                if availability_risk >= 45 else
                "Stable tenure with low near-term attrition probability."
            )
        }
    ]
    return factors

def generate_recommendations(
    criticality: float,
    uniqueness: float,
    dependency: float,
    documentation_gap: float,
    availability_risk: float,
    risk_level: str
) -> List[str]:
    """
    Generate targeted preservation recommendations based on factor breaches.
    """
    recommendations = []

    # High uniqueness / single expert
    if uniqueness >= 70:
        recommendations.append("Designate at least two secondary backup experts for paired knowledge transfer.")
        recommendations.append("Schedule structured weekly 2-hour knowledge handover sessions over the next 30 days.")

    # High documentation gap
    if documentation_gap >= 60:
        recommendations.append("Draft comprehensive technical architecture and troubleshooting runbooks.")
        recommendations.append("Record interactive screen walkthroughs of critical deployment and recovery workflows.")

    # High criticality & dependency
    if criticality >= 75 or dependency >= 75:
        recommendations.append("Implement automated failover mechanisms and architectural isolation to reduce systemic dependency.")
        recommendations.append("Conduct disaster recovery tabletop exercises to validate knowledge documentation.")

    # High availability risk
    if availability_risk >= 70:
        recommendations.append("Accelerate succession planning and cross-departmental mentoring before planned departures.")

    # Baseline fallback if low risk
    if not recommendations:
        if risk_level == "low":
            recommendations.append("Maintain routine quarterly documentation reviews and new team member onboarding.")
        else:
            recommendations.append("Review documentation periodically and expand cross-training across adjacent teams.")

    return recommendations
