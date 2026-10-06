import time
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.entities import Embedding, KnowledgeItem, DocumentChunk, RiskScore
from app.nlp.embeddings import generate_embedding, compute_cosine_similarity
from app.schemas.search import SearchResponse, SearchResultItem

class SearchService:
    @staticmethod
    def semantic_search(
        db: Session,
        organization_id: int,
        query: str,
        limit: int = 10,
        similarity_threshold: float = 0.25
    ) -> SearchResponse:
        """
        Execute natural language semantic search over document chunks and knowledge records.
        """
        start_time = time.time()
        if not query or not query.strip():
            return SearchResponse(
                query=query,
                total_results=0,
                search_time_ms=0.0,
                results=[]
            )

        # 1. Generate Query Vector
        query_vec = generate_embedding(query)

        # 2. Fetch all embeddings for this organization
        embeddings = db.query(Embedding).join(
            KnowledgeItem, Embedding.knowledge_id == KnowledgeItem.knowledge_id
        ).filter(
            KnowledgeItem.organization_id == organization_id
        ).all()

        # 3. Compute vector similarities and lexical overlap
        import re
        query_words = set(w.lower() for w in query.split() if len(w) > 2)
        scored_candidates = []
        for emb in embeddings:
            vec = emb.get_vector()
            vec_sim = compute_cosine_similarity(query_vec, vec)
            
            # Compute lexical keyword match with word boundaries and title weighting
            chunk_text = (emb.chunk.chunk_text if emb.chunk else "").lower()
            title_text = (emb.knowledge.title if emb.knowledge else "").lower()
            
            title_matches = sum(1 for qw in query_words if re.search(r'\b' + re.escape(qw) + r'\b', title_text))
            chunk_matches = sum(1 for qw in query_words if re.search(r'\b' + re.escape(qw) + r'\b', chunk_text))
            
            lexical_score = ((title_matches * 2.5 + chunk_matches) / (len(query_words) * 2.5)) if query_words else 0.0
            lexical_score = min(1.0, lexical_score)
            
            # Hybrid relevance: 50% vector + 50% lexical
            hybrid_score = (vec_sim * 0.50) + (lexical_score * 0.50)
            
            if hybrid_score >= similarity_threshold or title_matches > 0 or chunk_matches > 0:
                scored_candidates.append({
                    "embedding": emb,
                    "similarity": hybrid_score
                })

        # Sort descending by similarity
        scored_candidates.sort(key=lambda x: x["similarity"], reverse=True)

        # 4. Deduplicate by knowledge_id (take best chunk per knowledge item)
        seen_knowledge = set()
        results: List[SearchResultItem] = []

        for cand in scored_candidates:
            emb = cand["embedding"]
            k_id = emb.knowledge_id
            if k_id in seen_knowledge:
                continue
            seen_knowledge.add(k_id)

            knowledge = emb.knowledge
            chunk = emb.chunk

            snippet = chunk.chunk_text if chunk else (knowledge.description or "")
            # Truncate snippet
            if len(snippet) > 280:
                snippet = snippet[:280] + "..."

            # Get latest risk level
            latest_risk = db.query(RiskScore).filter(
                RiskScore.knowledge_id == k_id,
                RiskScore.is_latest == True
            ).first()

            results.append(SearchResultItem(
                knowledge_id=k_id,
                title=knowledge.title,
                description=knowledge.description,
                category=knowledge.category or "General",
                risk_level=latest_risk.risk_level if latest_risk else "medium",
                risk_score=latest_risk.risk_score if latest_risk else 50.0,
                relevance_score=round(cand["similarity"], 4),
                snippet=snippet,
                matched_chunk_id=chunk.chunk_id if chunk else None,
                source_document_id=knowledge.source_document_id
            ))

            if len(results) >= limit:
                break

        duration_ms = round((time.time() - start_time) * 1000, 2)
        return SearchResponse(
            query=query,
            total_results=len(results),
            search_time_ms=duration_ms,
            results=results
        )
