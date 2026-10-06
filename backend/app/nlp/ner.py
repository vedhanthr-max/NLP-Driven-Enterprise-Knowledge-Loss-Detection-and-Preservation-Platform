import re
from typing import List, Dict, Any

# Domain-specific technology and system patterns
TECH_PATTERNS = [
    (r'\b(AWS|Amazon Web Services|EC2|RDS|S3|Lambda|DMS|CloudFront|IAM)\b', 'TECHNOLOGY', 0.95),
    (r'\b(Docker|Kubernetes|K8s|Containerd|Helm|Podman)\b', 'TECHNOLOGY', 0.95),
    (r'\b(PostgreSQL|Postgres|MySQL|Oracle|MongoDB|Redis|SQLite|Cassandra|DynamoDB)\b', 'TECHNOLOGY', 0.95),
    (r'\b(Python|Java|JavaScript|TypeScript|Go|Rust|C\+\+|PHP|C#|\.NET)\b', 'TECHNOLOGY', 0.92),
    (r'\b(FastAPI|Django|Flask|React|Angular|Vue|Next\.js|Node\.js|Express)\b', 'TECHNOLOGY', 0.92),
    (r'\b(Jenkins|GitLab CI|GitHub Actions|ArgoCD|Terraform|Ansible)\b', 'TECHNOLOGY', 0.94),
    (r'\b(Legacy Payment System|Payment Gateway|Core Banking|Billing Engine)\b', 'PRODUCT', 0.90),
    (r'\b(Migration|Deployment|Failover|Backup|Disaster Recovery|Monitoring|Incident Response)\b', 'PROCESS', 0.88),
]

_nlp = None

def get_spacy_model():
    """Lazily load spaCy model if available."""
    global _nlp
    if _nlp is False:
        return None
    if _nlp is not None:
        return _nlp
    try:
        import spacy
        # Try medium model first, then small model
        try:
            _nlp = spacy.load("en_core_web_md")
        except Exception:
            try:
                _nlp = spacy.load("en_core_web_sm")
            except Exception:
                _nlp = False
                return None
        return _nlp
    except Exception:
        _nlp = False
        return None

def extract_entities(text: str) -> List[Dict[str, Any]]:
    """
    Extract named entities using spaCy and domain-specific rule patterns.
    Returns entities with name, type, confidence, and context snippet.
    """
    if not text:
        return []

    entities = []
    seen = set()

    # 1. spaCy extraction if model is available
    nlp = get_spacy_model()
    if nlp:
        try:
            # Process up to first 50,000 chars to avoid memory issues
            doc = nlp(text[:50000])
            for ent in doc.ents:
                ent_name = ent.text.strip()
                if len(ent_name) < 2 or ent_name.lower() in seen:
                    continue
                
                # Map spaCy entity labels to standardized taxonomy
                ent_type = ent.label_
                if ent_type in ('PERSON', 'ORG', 'GPE', 'DATE', 'PRODUCT', 'EVENT'):
                    normalized_type = 'ORGANIZATION' if ent_type == 'ORG' else ent_type
                    confidence = 0.85
                    if ent_type == 'PERSON':
                        confidence = 0.92
                    elif ent_type == 'ORG':
                        confidence = 0.88
                        
                    start_char = max(0, ent.start_char - 30)
                    end_char = min(len(text), ent.end_char + 30)
                    context = text[start_char:end_char].replace('\n', ' ').strip()
                    
                    entities.append({
                        "entity_name": ent_name,
                        "entity_type": normalized_type,
                        "confidence": confidence,
                        "context": f"...{context}..."
                    })
                    seen.add(ent_name.lower())
        except Exception:
            pass

    # 2. Rule & Domain Regex Patterns
    for pattern, ent_type, confidence in TECH_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            matched_text = match.group(0).strip()
            if matched_text.lower() in seen or len(matched_text) < 2:
                continue
            
            start_char = max(0, match.start() - 30)
            end_char = min(len(text), match.end() + 30)
            context = text[start_char:end_char].replace('\n', ' ').strip()
            
            entities.append({
                "entity_name": matched_text,
                "entity_type": ent_type,
                "confidence": confidence,
                "context": f"...{context}..."
            })
            seen.add(matched_text.lower())

    # 3. Rule-based Person/Author detection fallback if spaCy person not found
    if not any(e['entity_type'] == 'PERSON' for e in entities):
        author_patterns = [
            r'(?:Author|Owner|Expert|Created by|Maintained by|Lead|Contact):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+))\s+(?:holds|possesses|manages|architected|configured)'
        ]
        for pat in author_patterns:
            for match in re.finditer(pat, text):
                name = match.group(1).strip()
                if name.lower() not in seen:
                    entities.append({
                        "entity_name": name,
                        "entity_type": "PERSON",
                        "confidence": 0.90,
                        "context": text[max(0, match.start()-20):min(len(text), match.end()+20)].replace('\n', ' ').strip()
                    })
                    seen.add(name.lower())

    return entities
