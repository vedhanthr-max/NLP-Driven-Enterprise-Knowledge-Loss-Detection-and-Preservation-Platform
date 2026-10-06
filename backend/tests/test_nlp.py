from app.nlp.preprocessor import clean_text, preprocess_text, chunk_text, tokenize
from app.nlp.ner import extract_entities
from app.nlp.keywords import extract_keywords
from app.nlp.topic_extractor import extract_topics
from app.nlp.embeddings import generate_embedding, compute_cosine_similarity

def test_clean_text_normalizes_whitespace():
    raw = "  Hello \t\t World!  \r\n\r\n\r\n  Next line   with   spaces.  "
    cleaned = clean_text(raw)
    assert "\t" not in cleaned
    assert "   " not in cleaned
    assert cleaned.startswith("Hello World!")

def test_preprocess_text_removes_stopwords():
    text = "The quick brown fox jumps over the lazy dog and is running in the field"
    result = preprocess_text(text)
    words = result.split()
    assert "the" not in words
    assert "and" not in words
    assert "is" not in words
    assert "brown" in words
    assert "fox" in words

def test_chunking_strategy():
    long_text = " ".join([f"Sentence {i} describing operational workflow step." for i in range(200)])
    chunks = chunk_text(long_text, chunk_size=50, overlap=10)
    assert len(chunks) > 1
    assert all("chunk_text" in c for c in chunks)
    assert all("token_count" in c for c in chunks)

def test_ner_entity_extraction():
    text = "Rajesh Kumar deployed the payment system using Docker, Kubernetes and PostgreSQL in us-east-1."
    entities = extract_entities(text)
    assert len(entities) >= 2
    types = [e["entity_type"] for e in entities]
    names = [e["entity_name"].lower() for e in entities]
    assert "TECHNOLOGY" in types or "PRODUCT" in types
    assert any("docker" in n or "kubernetes" in n or "postgresql" in n for n in names)

def test_keyword_extraction():
    text = "Database migration to AWS RDS requires replication, backup, failover testing, and schema validation. Database database database."
    keywords = extract_keywords(text, top_n=5)
    assert len(keywords) >= 2
    kw_names = [k["keyword"] for k in keywords]
    assert "database" in kw_names or "migration" in kw_names
    assert all(k["frequency"] >= 1 for k in keywords)

def test_topic_identification():
    text = "Deploying containerized microservices to AWS EC2 instances with VPC and load balancers."
    topic, ranked = extract_topics(text)
    assert topic in ("Cloud Infrastructure", "DevOps & Deployment", "Application Development")
    assert len(ranked) >= 1

def test_embedding_generation_384_dimensions():
    text = "Enterprise knowledge management platform vector embedding test."
    vec = generate_embedding(text)
    assert len(vec) == 384
    assert all(isinstance(v, (float, int)) for v in vec)

def test_cosine_similarity():
    v1 = generate_embedding("Kubernetes deployment and docker containers")
    v2 = generate_embedding("Kubernetes deployment and docker containers")
    v3 = generate_embedding("Baking chocolate chip cookies in the kitchen")
    
    sim_identical = compute_cosine_similarity(v1, v2)
    sim_different = compute_cosine_similarity(v1, v3)
    
    assert sim_identical >= 0.99
    assert sim_different < sim_identical
