import numpy as np
import pandas as pd
from app.risk.scoring import calculate_risk_score, classify_risk_level

def generate_realistic_risk_dataset(num_samples: int = 700, random_state: int = 42) -> pd.DataFrame:
    """
    Generate realistic enterprise knowledge-loss risk dataset reflecting actual operational distributions:
    - Legacy monolithic & banking systems (High criticality, high uniqueness, high gap)
    - Modern cloud-native microservices (High criticality, low uniqueness, low gap)
    - Supporting internal tooling (Low criticality, moderate uniqueness)
    - High-turnover specialized DevOps workflows (High availability risk, high dependency)
    """
    np.random.seed(random_state)
    data = []

    # Distribution archetypes:
    # Archetype 1: Legacy Core Systems (20% -> mostly CRITICAL / HIGH)
    n1 = int(num_samples * 0.25)
    for _ in range(n1):
        crit = np.random.uniform(85, 98)
        uniq = np.random.uniform(80, 99)
        dep = np.random.uniform(75, 95)
        gap = np.random.uniform(65, 95)
        avail = np.random.uniform(70, 95)
        experts = int(np.random.choice([1, 1, 2]))
        systems = int(np.random.randint(4, 9))
        doc_len = int(np.random.randint(200, 1500))
        score = calculate_risk_score(crit, uniq, dep, gap, avail)
        level = classify_risk_level(score)
        data.append({
            "criticality": crit, "uniqueness": uniq, "dependency": dep,
            "documentation_gap": gap, "availability_risk": avail,
            "num_experts": experts, "num_systems": systems, "doc_length": doc_len,
            "risk_score": score, "risk_level": level
        })

    # Archetype 2: Modern Well-Documented Services (30% -> mostly LOW)
    n2 = int(num_samples * 0.30)
    for _ in range(n2):
        crit = np.random.uniform(40, 70)
        uniq = np.random.uniform(10, 35)
        dep = np.random.uniform(30, 55)
        gap = np.random.uniform(5, 30)
        avail = np.random.uniform(10, 35)
        experts = int(np.random.randint(5, 12))
        systems = int(np.random.randint(1, 4))
        doc_len = int(np.random.randint(2000, 8000))
        score = calculate_risk_score(crit, uniq, dep, gap, avail)
        level = classify_risk_level(score)
        data.append({
            "criticality": crit, "uniqueness": uniq, "dependency": dep,
            "documentation_gap": gap, "availability_risk": avail,
            "num_experts": experts, "num_systems": systems, "doc_length": doc_len,
            "risk_score": score, "risk_level": level
        })

    # Archetype 3: Specialized Cloud Migration & DB Workflows (25% -> mostly HIGH / MEDIUM)
    n3 = int(num_samples * 0.25)
    for _ in range(n3):
        crit = np.random.uniform(70, 90)
        uniq = np.random.uniform(55, 80)
        dep = np.random.uniform(60, 85)
        gap = np.random.uniform(35, 65)
        avail = np.random.uniform(40, 75)
        experts = int(np.random.choice([2, 3, 4]))
        systems = int(np.random.randint(2, 6))
        doc_len = int(np.random.randint(1000, 3500))
        score = calculate_risk_score(crit, uniq, dep, gap, avail)
        level = classify_risk_level(score)
        data.append({
            "criticality": crit, "uniqueness": uniq, "dependency": dep,
            "documentation_gap": gap, "availability_risk": avail,
            "num_experts": experts, "num_systems": systems, "doc_length": doc_len,
            "risk_score": score, "risk_level": level
        })

    # Archetype 4: Standard Departmental Procedures (20% -> MEDIUM / LOW)
    n4 = num_samples - len(data)
    for _ in range(n4):
        crit = np.random.uniform(25, 60)
        uniq = np.random.uniform(30, 60)
        dep = np.random.uniform(25, 60)
        gap = np.random.uniform(30, 60)
        avail = np.random.uniform(25, 55)
        experts = int(np.random.randint(3, 7))
        systems = int(np.random.randint(1, 4))
        doc_len = int(np.random.randint(800, 2500))
        score = calculate_risk_score(crit, uniq, dep, gap, avail)
        level = classify_risk_level(score)
        data.append({
            "criticality": crit, "uniqueness": uniq, "dependency": dep,
            "documentation_gap": gap, "availability_risk": avail,
            "num_experts": experts, "num_systems": systems, "doc_length": doc_len,
            "risk_score": score, "risk_level": level
        })

    df = pd.DataFrame(data)
    # Shuffle dataset
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    return df
