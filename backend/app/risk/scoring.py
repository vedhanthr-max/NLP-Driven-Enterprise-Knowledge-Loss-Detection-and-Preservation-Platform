from typing import Tuple, Dict, Any, List
from app.core.config import settings

def calculate_risk_score(
    criticality: float,
    uniqueness: float,
    dependency: float,
    documentation_gap: float,
    availability_risk: float
) -> float:
    """
    Calculate composite knowledge-loss risk score using the exact documented weighted formula:
      RISK SCORE = (Criticality × 0.30) + (Uniqueness × 0.25) + (Dependency × 0.20) +
                   (Documentation_Gap × 0.15) + (Availability_Risk × 0.10)
    All inputs must be in 0.0 - 100.0 range.
    """
    # Normalize / clamp inputs between 0 and 100
    c = max(0.0, min(100.0, float(criticality)))
    u = max(0.0, min(100.0, float(uniqueness)))
    d = max(0.0, min(100.0, float(dependency)))
    g = max(0.0, min(100.0, float(documentation_gap)))
    a = max(0.0, min(100.0, float(availability_risk)))

    score = (
        (c * settings.WEIGHT_CRITICALITY) +
        (u * settings.WEIGHT_UNIQUENESS) +
        (d * settings.WEIGHT_DEPENDENCY) +
        (g * settings.WEIGHT_DOCUMENTATION_GAP) +
        (a * settings.WEIGHT_AVAILABILITY_RISK)
    )
    return round(score, 2)

def classify_risk_level(risk_score: float) -> str:
    """
    Classify risk score into documented risk levels:
      0  - 30 : low
      31 - 60 : medium
      61 - 80 : high
      81 - 100: critical
    """
    if risk_score <= settings.THRESHOLD_LOW:
        return "low"
    elif risk_score <= settings.THRESHOLD_MEDIUM:
        return "medium"
    elif risk_score <= settings.THRESHOLD_HIGH:
        return "high"
    else:
        return "critical"

def estimate_uniqueness_from_experts(num_experts: int) -> float:
    """
    Map count of experts to knowledge uniqueness score per Section 13.1 Factor 2:
      1 expert  → 95
      2 experts → 75
      3 experts → 60
      4-5 experts → 45
      6+ experts → 20
    """
    if num_experts <= 1:
        return 95.0
    elif num_experts == 2:
        return 75.0
    elif num_experts == 3:
        return 60.0
    elif 4 <= num_experts <= 5:
        return 45.0
    else:
        return 20.0

def estimate_documentation_gap(text: str) -> float:
    """
    Assess structural completeness of documentation:
    introduction (15), prerequisites (10), step_by_step (25), examples (20),
    troubleshooting (15), contact_info (10), update_recency (5).
    """
    if not text or len(text.strip()) < 50:
        return 100.0  # No/minimal documentation

    text_lower = text.lower()
    completeness = 0.0

    # Introduction / Overview
    if any(k in text_lower for k in ["introduction", "overview", "purpose", "about"]):
        completeness += 15.0

    # Prerequisites
    if any(k in text_lower for k in ["prerequisite", "requirements", "dependencies", "setup"]):
        completeness += 10.0

    # Step-by-step procedures
    if any(k in text_lower for k in ["step", "procedure", "workflow", "guide", "instructions", "how to"]):
        completeness += 25.0

    # Examples / Code / Configs
    if any(k in text_lower for k in ["example", "sample", "configuration", "code", "schema"]):
        completeness += 20.0

    # Troubleshooting / FAQ
    if any(k in text_lower for k in ["troubleshoot", "error", "issue", "faq", "debug", "incident"]):
        completeness += 15.0

    # Contact / Owner
    if any(k in text_lower for k in ["contact", "author", "maintainer", "owner", "team", "email"]):
        completeness += 10.0

    # Length boost (comprehensive document)
    word_count = len(text.split())
    if word_count > 1000:
        completeness = min(100.0, completeness + 5.0)

    gap = max(0.0, min(100.0, 100.0 - completeness))
    return round(gap, 2)
