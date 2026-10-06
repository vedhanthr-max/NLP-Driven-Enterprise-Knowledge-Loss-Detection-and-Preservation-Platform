import re
from collections import Counter
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from app.nlp.preprocessor import clean_text, STOPWORDS

# Domain booster keywords
DOMAIN_TERMS = {
    "architecture", "database", "deployment", "infrastructure", "kubernetes", "migration",
    "failover", "replication", "security", "troubleshooting", "runbook", "payment", "legacy",
    "authentication", "authorization", "docker", "pipeline", "backend", "frontend", "api",
    "postgres", "mysql", "oracle", "redis", "backup", "compliance", "performance", "monitoring"
}

def extract_keywords(text: str, top_n: int = 15) -> List[Dict[str, Any]]:
    """
    Extract meaningful technical and operational keywords using TF-IDF and term frequencies.
    """
    if not text:
        return []

    cleaned = clean_text(text)
    # Tokenize words
    words = re.findall(r'\b[A-Za-z][A-Za-z0-9_\-]{2,}\b', cleaned.lower())
    filtered_words = [w for w in words if w not in STOPWORDS and len(w) > 2 and not w.isdigit()]

    if not filtered_words:
        return []

    word_freq = Counter(filtered_words)

    # Calculate TF-IDF
    tfidf_scores = {}
    try:
        sentences = [s for s in re.split(r'[.\n]+', cleaned) if len(s.split()) > 3]
        if len(sentences) >= 2:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.sum(axis=0).A1
            for word, score in zip(feature_names, scores):
                tfidf_scores[word.lower()] = float(score)
    except Exception:
        pass

    # Score each candidate word combining frequency + tfidf + domain relevance
    candidates = []
    max_freq = max(word_freq.values()) if word_freq else 1
    max_tfidf = max(tfidf_scores.values()) if tfidf_scores else 1.0

    for word, freq in word_freq.items():
        norm_freq = freq / max_freq
        norm_tfidf = (tfidf_scores.get(word, 0.0) / max_tfidf) if max_tfidf > 0 else 0.0
        domain_boost = 0.3 if word in DOMAIN_TERMS else 0.0
        composite_score = (norm_freq * 0.4) + (norm_tfidf * 0.4) + domain_boost

        candidates.append({
            "keyword": word,
            "frequency": freq,
            "tf_idf_score": round(composite_score, 4)
        })

    # Sort descending by composite score, then frequency
    candidates.sort(key=lambda x: (x["tf_idf_score"], x["frequency"]), reverse=True)
    return candidates[:top_n]
