from typing import List, Dict, Tuple
from collections import Counter
import re

TOPIC_TAXONOMY = {
    "Cloud Infrastructure": [
        "aws", "ec2", "s3", "cloud", "azure", "gcp", "vpc", "subnet", "load balancer", "route53", "terraform"
    ],
    "Database Administration": [
        "database", "sql", "postgres", "mysql", "oracle", "rds", "replication", "schema", "backup", "failover", "dms"
    ],
    "DevOps & Deployment": [
        "docker", "kubernetes", "k8s", "container", "jenkins", "pipeline", "ci/cd", "deployment", "helm", "git"
    ],
    "Security & Compliance": [
        "security", "compliance", "encryption", "iam", "firewall", "audit", "policy", "ssl", "tls", "vulnerability", "auth"
    ],
    "Application Development": [
        "frontend", "backend", "api", "microservice", "python", "javascript", "react", "fastapi", "framework", "architecture"
    ],
    "Legacy Systems": [
        "legacy", "mainframe", "cobol", "banking", "payment gateway", "proprietary", "monolith", "deprecated"
    ]
}

def extract_topics(text: str) -> Tuple[str, List[Dict[str, float]]]:
    """
    Classify document into primary technical topic and return confidence scores for all topics.
    """
    if not text:
        return "General Operations", []

    text_lower = text.lower()
    topic_scores = {}

    for topic, keywords in TOPIC_TAXONOMY.items():
        score = 0
        for kw in keywords:
            # Count word boundary matches
            matches = len(re.findall(r'\b' + re.escape(kw) + r'\b', text_lower))
            score += matches * (1.5 if " " in kw else 1.0)
        topic_scores[topic] = score

    total_score = sum(topic_scores.values())
    ranked = []

    if total_score > 0:
        for topic, score in topic_scores.items():
            confidence = round(score / total_score, 4)
            if confidence > 0.05:
                ranked.append({"topic": topic, "confidence": confidence})
        ranked.sort(key=lambda x: x["confidence"], reverse=True)

    if ranked:
        primary_topic = ranked[0]["topic"]
    else:
        primary_topic = "General Operations"
        ranked = [{"topic": "General Operations", "confidence": 1.0}]

    return primary_topic, ranked
