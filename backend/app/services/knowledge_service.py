from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.core.exceptions import KnowledgeNotFoundException
from app.models.entities import (
    KnowledgeItem, Entity, Keyword, KnowledgeExpert, RiskScore, Employee, User
)
from app.schemas.knowledge import (
    KnowledgeCreateRequest, KnowledgeUpdateRequest, KnowledgeListItem,
    KnowledgeListResponse, KnowledgeDetailOut, EntityOut, KeywordOut, ExpertOut
)
from app.nlp.embeddings import generate_embedding
from app.models.entities import Embedding

class KnowledgeService:
    @staticmethod
    def get_knowledge_list(
        db: Session,
        organization_id: int,
        category: Optional[str] = None,
        risk_level: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> KnowledgeListResponse:
        query = db.query(KnowledgeItem).filter(KnowledgeItem.organization_id == organization_id)

        if category:
            query = query.filter(KnowledgeItem.category == category)
        if status:
            query = query.filter(KnowledgeItem.status == status)
        if search:
            query = query.filter(KnowledgeItem.title.ilike(f"%{search}%"))

        all_items = query.all()

        # Join or filter by risk_level if requested
        result_items = []
        for item in all_items:
            latest_risk = db.query(RiskScore).filter(
                RiskScore.knowledge_id == item.knowledge_id,
                RiskScore.is_latest == True
            ).first()

            item_risk_level = latest_risk.risk_level if latest_risk else "medium"
            item_risk_score = latest_risk.risk_score if latest_risk else 50.0

            if risk_level and item_risk_level != risk_level.lower():
                continue

            result_items.append(KnowledgeListItem(
                knowledge_id=item.knowledge_id,
                title=item.title,
                category=item.category or "General",
                status=item.status,
                risk_score=item_risk_score,
                risk_level=item_risk_level,
                experts_count=len(item.experts) if item.experts else 0,
                tags=item.tags or [],
                created_at=item.created_at
            ))

        total = len(result_items)
        start_idx = (page - 1) * limit
        paginated = result_items[start_idx:start_idx + limit]

        return KnowledgeListResponse(
            total=total,
            page=page,
            limit=limit,
            items=paginated
        )

    @staticmethod
    def get_knowledge_detail(db: Session, knowledge_id: int, organization_id: int) -> KnowledgeDetailOut:
        item = db.query(KnowledgeItem).filter(
            KnowledgeItem.knowledge_id == knowledge_id,
            KnowledgeItem.organization_id == organization_id
        ).first()
        if not item:
            raise KnowledgeNotFoundException(knowledge_id)

        # Update access stats
        item.last_accessed = datetime.now(timezone.utc)
        item.access_count = (item.access_count or 0) + 1
        db.commit()

        # Get latest risk
        latest_risk = db.query(RiskScore).filter(
            RiskScore.knowledge_id == item.knowledge_id,
            RiskScore.is_latest == True
        ).first()

        # Build experts list
        experts_out = []
        for exp_link in item.experts:
            emp = exp_link.employee
            emp_user = emp.user if emp else None
            experts_out.append(ExpertOut(
                employee_id=exp_link.employee_id,
                full_name=emp_user.full_name if emp_user else f"Employee #{exp_link.employee_id}",
                expertise_level=exp_link.expertise_level,
                is_primary_expert=exp_link.is_primary_expert,
                years_of_experience=exp_link.years_of_experience,
                confidence_score=exp_link.confidence_score
            ))

        return KnowledgeDetailOut(
            knowledge_id=item.knowledge_id,
            title=item.title,
            description=item.description,
            category=item.category or "General",
            subcategory=item.subcategory,
            tags=item.tags or [],
            source_document_id=item.source_document_id,
            knowledge_type=item.knowledge_type or "procedure",
            status=item.status,
            is_verified=item.is_verified,
            confidence_score=item.confidence_score or 1.0,
            created_at=item.created_at,
            updated_at=item.updated_at,
            last_accessed=item.last_accessed,
            access_count=item.access_count or 0,
            entities=[EntityOut.from_orm(e) for e in item.entities],
            keywords=[KeywordOut.from_orm(k) for k in item.keywords],
            experts=experts_out,
            risk_score=latest_risk.risk_score if latest_risk else None,
            risk_level=latest_risk.risk_level if latest_risk else None
        )

    @staticmethod
    def create_knowledge_item(
        db: Session,
        organization_id: int,
        req: KnowledgeCreateRequest,
        created_by_user_id: int
    ) -> KnowledgeItem:
        item = KnowledgeItem(
            organization_id=organization_id,
            title=req.title,
            description=req.description,
            category=req.category,
            subcategory=req.subcategory,
            tags=req.tags,
            source_document_id=req.source_document_id,
            knowledge_type=req.knowledge_type,
            status=req.status,
            created_by=created_by_user_id
        )
        db.add(item)
        db.flush()

        # Add expert links
        for exp in req.experts:
            link = KnowledgeExpert(
                knowledge_id=item.knowledge_id,
                employee_id=exp.employee_id,
                expertise_level=exp.expertise_level,
                is_primary_expert=exp.is_primary_expert,
                years_of_experience=exp.years_of_experience,
                confidence_score=exp.confidence_score,
                identified_by="manual"
            )
            db.add(link)

        # Generate embedding for knowledge item description
        desc_text = f"{req.title}. {req.description or ''}"
        vec = generate_embedding(desc_text)
        emb = Embedding(
            knowledge_id=item.knowledge_id,
            embedding_model="all-MiniLM-L6-v2"
        )
        emb.set_vector(vec)
        db.add(emb)

        db.commit()
        db.refresh(item)
        return item
