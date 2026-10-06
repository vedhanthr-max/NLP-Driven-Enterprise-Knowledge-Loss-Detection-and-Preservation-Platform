import os
import sys
from datetime import datetime, timezone, date

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.entities import (
    Organization, Department, User, Employee, Document, DocumentChunk,
    KnowledgeItem, Entity, Keyword, KnowledgeExpert, RiskScore,
    PreservationAction, Embedding, AuditLog
)
from app.nlp.embeddings import generate_embedding
from app.risk.scoring import calculate_risk_score, classify_risk_level
from app.ml.classifier import predict_risk_level

def seed():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        existing_org = db.query(Organization).filter(Organization.organization_name == "TechCorp Enterprise").first()
        if existing_org:
            print("Database already seeded with TechCorp Enterprise.")
            return

        print("Creating Organization & Departments...")
        org = Organization(
            organization_name="TechCorp Enterprise",
            description="Global Financial and Enterprise Software Solutions",
            industry="Financial Technology",
            size=500,
            subscription_tier="enterprise"
        )
        db.add(org)
        db.flush()

        dept_core = Department(organization_id=org.organization_id, department_name="Core Systems & Architecture")
        dept_devops = Department(organization_id=org.organization_id, department_name="DevOps & Cloud SRE")
        dept_data = Department(organization_id=org.organization_id, department_name="Database & Data Engineering")
        db.add_all([dept_core, dept_devops, dept_data])
        db.flush()

        print("Creating Users & Employees...")
        default_pwd = hash_password("Manager123!")

        # 1. Admin
        user_admin = User(
            organization_id=org.organization_id,
            email="admin@techcorp.com",
            password_hash=default_pwd,
            full_name="System Administrator",
            role="admin",
            department_id=dept_core.department_id,
            is_active=True
        )
        # 2. Manager
        user_manager = User(
            organization_id=org.organization_id,
            email="manager@techcorp.com",
            password_hash=default_pwd,
            full_name="John Doe",
            role="manager",
            department_id=dept_core.department_id,
            is_active=True
        )
        # 3. Rajesh Kumar (Sole expert on legacy banking)
        user_rajesh = User(
            organization_id=org.organization_id,
            email="rajesh@techcorp.com",
            password_hash=default_pwd,
            full_name="Rajesh Kumar",
            role="employee",
            department_id=dept_core.department_id,
            is_active=True
        )
        # 4. Arun Kumar (Database Lead)
        user_arun = User(
            organization_id=org.organization_id,
            email="arun@techcorp.com",
            password_hash=default_pwd,
            full_name="Arun Kumar",
            role="employee",
            department_id=dept_data.department_id,
            is_active=True
        )
        # 5. Priya Sharma (DevOps Specialist)
        user_priya = User(
            organization_id=org.organization_id,
            email="priya@techcorp.com",
            password_hash=default_pwd,
            full_name="Priya Sharma",
            role="employee",
            department_id=dept_devops.department_id,
            is_active=True
        )

        db.add_all([user_admin, user_manager, user_rajesh, user_arun, user_priya])
        db.flush()

        # Employee Profiles
        emp_rajesh = Employee(
            user_id=user_rajesh.user_id,
            organization_id=org.organization_id,
            department_id=dept_core.department_id,
            job_title="Principal Legacy Architect",
            expertise_level="expert",
            expertise_areas=["Legacy Payment System", "Java Monolith", "Oracle 9i", "COBOL Gateway"],
            status="active",
            bio="15 years managing core financial transaction processing engine."
        )
        emp_arun = Employee(
            user_id=user_arun.user_id,
            organization_id=org.organization_id,
            department_id=dept_data.department_id,
            job_title="Lead Database Administrator",
            expertise_level="expert",
            expertise_areas=["AWS RDS", "PostgreSQL", "MySQL Replication", "Database Failover"],
            status="active",
            bio="12 years database clustering and cloud data migration specialist."
        )
        emp_priya = Employee(
            user_id=user_priya.user_id,
            organization_id=org.organization_id,
            department_id=dept_devops.department_id,
            job_title="Senior DevOps Engineer",
            expertise_level="expert",
            expertise_areas=["Kubernetes", "Docker", "Helm", "CI/CD", "Terraform"],
            status="active",
            bio="Container orchestration and infrastructure automation lead."
        )
        db.add_all([emp_rajesh, emp_arun, emp_priya])
        db.flush()

        print("Seeding Knowledge Scenarios...")

        # ----------------------------------------------------------------------------------
        # SCENARIO 1: Legacy Payment System (CRITICAL RISK - 93.15)
        # ----------------------------------------------------------------------------------
        doc_legacy = Document(
            organization_id=org.organization_id,
            title="Legacy Payment Processing Engine Runbook",
            description="Core operational procedures for high-value transaction gateway built in 2005.",
            file_name="legacy_payment_system.txt",
            file_path="uploads/legacy_payment_system.txt",
            file_size=15420,
            file_type="txt",
            mime_type="text/plain",
            content_hash="hash_legacy_payment_001",
            pages=12,
            uploaded_by=user_manager.user_id,
            extraction_status="completed"
        )
        db.add(doc_legacy)
        db.flush()

        legacy_chunk_text = (
            "The Legacy Payment System processes over $5M in daily transactions. It connects to 5 critical banking "
            "partner networks via proprietary TCP sockets. In the event of a gateway disconnection, manual failover "
            "requires updating binary configuration flags in /etc/payment/gateway.conf and restarting the daemon. "
            "Only Rajesh Kumar holds operational knowledge of custom cryptographic keys and legacy database rollback scripts."
        )
        chunk_legacy = DocumentChunk(
            document_id=doc_legacy.document_id,
            chunk_index=0,
            chunk_text=legacy_chunk_text,
            token_count=65,
            page_number=1
        )
        db.add(chunk_legacy)
        db.flush()

        know_legacy = KnowledgeItem(
            organization_id=org.organization_id,
            title="Legacy Payment Processing System Administration",
            description=legacy_chunk_text,
            category="Legacy Systems",
            subcategory="Payment Gateways",
            tags=["payment", "legacy", "banking", "failover", "transactions"],
            source_document_id=doc_legacy.document_id,
            knowledge_type="procedure",
            status="active",
            confidence_score=0.96,
            created_by=user_manager.user_id
        )
        db.add(know_legacy)
        db.flush()

        # Link Expert
        db.add(KnowledgeExpert(
            knowledge_id=know_legacy.knowledge_id,
            employee_id=emp_rajesh.employee_id,
            expertise_level="expert",
            is_primary_expert=True,
            years_of_experience=15,
            identified_by="nlp_extracted"
        ))

        # Entities & Keywords
        db.add_all([
            Entity(knowledge_id=know_legacy.knowledge_id, document_id=doc_legacy.document_id, entity_name="Rajesh Kumar", entity_type="PERSON", confidence=0.95),
            Entity(knowledge_id=know_legacy.knowledge_id, document_id=doc_legacy.document_id, entity_name="Legacy Payment System", entity_type="PRODUCT", confidence=0.98),
            Entity(knowledge_id=know_legacy.knowledge_id, document_id=doc_legacy.document_id, entity_name="Oracle 9i", entity_type="TECHNOLOGY", confidence=0.92),
            Keyword(knowledge_id=know_legacy.knowledge_id, keyword="payment", frequency=14, tf_idf_score=0.91),
            Keyword(knowledge_id=know_legacy.knowledge_id, keyword="failover", frequency=8, tf_idf_score=0.88),
            Keyword(knowledge_id=know_legacy.knowledge_id, keyword="gateway", frequency=11, tf_idf_score=0.85)
        ])

        # Risk Score (Exact Section 31 values: 95, 98, 92, 85, 90 -> 93.15)
        score_val1 = calculate_risk_score(95, 98, 92, 85, 90)
        ml_res1 = predict_risk_level(95, 98, 92, 85, 90)
        risk_legacy = RiskScore(
            organization_id=org.organization_id,
            knowledge_id=know_legacy.knowledge_id,
            criticality=95.0,
            uniqueness=98.0,
            dependency=92.0,
            documentation_gap=85.0,
            availability_risk=90.0,
            risk_score=score_val1,
            risk_level=classify_risk_level(score_val1),
            ml_predicted_level=ml_res1["predicted_level"],
            ml_confidence=ml_res1["confidence"],
            prediction_model_version="1.0.0",
            assessment_method="rule_based",
            is_latest=True
        )
        db.add(risk_legacy)

        # Preservation Actions
        db.add_all([
            PreservationAction(
                organization_id=org.organization_id,
                knowledge_id=know_legacy.knowledge_id,
                action_type="documentation",
                action_description="Draft comprehensive architecture and step-by-step troubleshooting runbook for Legacy Payment Gateway.",
                priority="critical",
                status="in_progress",
                assigned_to=user_rajesh.user_id,
                deadline=date(2026, 10, 30),
                estimated_hours=120,
                actual_hours=25
            ),
            PreservationAction(
                organization_id=org.organization_id,
                knowledge_id=know_legacy.knowledge_id,
                action_type="secondary_expert",
                action_description="Designate and pair 2 junior developers with Rajesh Kumar for daily operational cross-training.",
                priority="critical",
                status="planned",
                assigned_to=user_manager.user_id,
                deadline=date(2026, 11, 15),
                estimated_hours=160,
                actual_hours=0
            )
        ])

        # Embeddings
        emb1 = Embedding(
            knowledge_id=know_legacy.knowledge_id,
            document_chunk_id=chunk_legacy.chunk_id,
            embedding_model="all-MiniLM-L6-v2"
        )
        emb1.set_vector(generate_embedding(legacy_chunk_text))
        db.add(emb1)

        # ----------------------------------------------------------------------------------
        # SCENARIO 2: Kubernetes Deployment Pipeline (LOW / MEDIUM - 37.5)
        # ----------------------------------------------------------------------------------
        doc_k8s = Document(
            organization_id=org.organization_id,
            title="Kubernetes Production Deployment Guide",
            description="Comprehensive guide for deploying containerized microservices to Kubernetes EKS.",
            file_name="k8s_deployment_pipeline.txt",
            file_path="uploads/k8s_deployment_pipeline.txt",
            file_size=42100,
            file_type="txt",
            mime_type="text/plain",
            content_hash="hash_k8s_deployment_002",
            pages=24,
            uploaded_by=user_manager.user_id,
            extraction_status="completed"
        )
        db.add(doc_k8s)
        db.flush()

        k8s_chunk_text = (
            "Standard deployment procedure for Kubernetes clusters using Helm charts and ArgoCD pipelines. "
            "Microservices are packaged with Docker and automatically rolled out with zero downtime using rolling updates. "
            "Troubleshooting guides, Prometheus monitoring dashboards, and alert runbooks are thoroughly maintained. "
            "Supported by 8 certified DevOps engineers across the SRE team."
        )
        chunk_k8s = DocumentChunk(
            document_id=doc_k8s.document_id,
            chunk_index=0,
            chunk_text=k8s_chunk_text,
            token_count=58,
            page_number=1
        )
        db.add(chunk_k8s)
        db.flush()

        know_k8s = KnowledgeItem(
            organization_id=org.organization_id,
            title="Kubernetes Microservices Deployment Pipeline",
            description=k8s_chunk_text,
            category="DevOps & Deployment",
            subcategory="Container Orchestration",
            tags=["kubernetes", "docker", "helm", "devops", "argocd", "deployment"],
            source_document_id=doc_k8s.document_id,
            knowledge_type="procedure",
            status="active",
            confidence_score=0.98,
            created_by=user_manager.user_id
        )
        db.add(know_k8s)
        db.flush()

        db.add(KnowledgeExpert(
            knowledge_id=know_k8s.knowledge_id,
            employee_id=emp_priya.employee_id,
            expertise_level="expert",
            is_primary_expert=True,
            years_of_experience=6,
            identified_by="nlp_extracted"
        ))

        db.add_all([
            Entity(knowledge_id=know_k8s.knowledge_id, document_id=doc_k8s.document_id, entity_name="Kubernetes", entity_type="TECHNOLOGY", confidence=0.99),
            Entity(knowledge_id=know_k8s.knowledge_id, document_id=doc_k8s.document_id, entity_name="Priya Sharma", entity_type="PERSON", confidence=0.94),
            Entity(knowledge_id=know_k8s.knowledge_id, document_id=doc_k8s.document_id, entity_name="Docker", entity_type="TECHNOLOGY", confidence=0.96),
            Keyword(knowledge_id=know_k8s.knowledge_id, keyword="kubernetes", frequency=18, tf_idf_score=0.95),
            Keyword(knowledge_id=know_k8s.knowledge_id, keyword="deployment", frequency=15, tf_idf_score=0.90),
            Keyword(knowledge_id=know_k8s.knowledge_id, keyword="helm", frequency=7, tf_idf_score=0.82)
        ])

        # Exact Section 31 values: 60, 25, 45, 15, 20 -> 37.5
        score_val2 = calculate_risk_score(60, 25, 45, 15, 20)
        ml_res2 = predict_risk_level(60, 25, 45, 15, 20)
        risk_k8s = RiskScore(
            organization_id=org.organization_id,
            knowledge_id=know_k8s.knowledge_id,
            criticality=60.0,
            uniqueness=25.0,
            dependency=45.0,
            documentation_gap=15.0,
            availability_risk=20.0,
            risk_score=score_val2,
            risk_level=classify_risk_level(score_val2),
            ml_predicted_level=ml_res2["predicted_level"],
            ml_confidence=ml_res2["confidence"],
            prediction_model_version="1.0.0",
            assessment_method="rule_based",
            is_latest=True
        )
        db.add(risk_k8s)

        emb2 = Embedding(
            knowledge_id=know_k8s.knowledge_id,
            document_chunk_id=chunk_k8s.chunk_id,
            embedding_model="all-MiniLM-L6-v2"
        )
        emb2.set_vector(generate_embedding(k8s_chunk_text))
        db.add(emb2)

        # ----------------------------------------------------------------------------------
        # SCENARIO 3: AWS Database Migration Procedure (HIGH RISK - 74.3)
        # ----------------------------------------------------------------------------------
        doc_aws = Document(
            organization_id=org.organization_id,
            title="AWS Database Migration Procedure",
            description="Complete procedure for migrating on-premises databases to AWS RDS with replication and testing.",
            file_name="aws_database_migration.txt",
            file_path="uploads/aws_database_migration.txt",
            file_size=28900,
            file_type="txt",
            mime_type="text/plain",
            content_hash="hash_aws_db_migration_003",
            pages=18,
            uploaded_by=user_manager.user_id,
            extraction_status="completed"
        )
        db.add(doc_aws)
        db.flush()

        aws_chunk_text = (
            "Complete step-by-step procedure for migrating on-premises MySQL and PostgreSQL databases to AWS RDS. "
            "Utilizes AWS Database Migration Service (DMS) for continuous replication and schema conversion. "
            "Cutover requires a maintenance window with validation queries and automated rollback script execution. "
            "Arun Kumar and Priya Sharma are the sole certified AWS database migration specialists on the project."
        )
        chunk_aws = DocumentChunk(
            document_id=doc_aws.document_id,
            chunk_index=0,
            chunk_text=aws_chunk_text,
            token_count=62,
            page_number=1
        )
        db.add(chunk_aws)
        db.flush()

        know_aws = KnowledgeItem(
            organization_id=org.organization_id,
            title="AWS RDS Database Migration and Continuous Replication",
            description=aws_chunk_text,
            category="Database Administration",
            subcategory="Cloud Migration",
            tags=["aws", "database", "rds", "migration", "dms", "replication"],
            source_document_id=doc_aws.document_id,
            knowledge_type="procedure",
            status="active",
            confidence_score=0.94,
            created_by=user_manager.user_id
        )
        db.add(know_aws)
        db.flush()

        db.add_all([
            KnowledgeExpert(
                knowledge_id=know_aws.knowledge_id,
                employee_id=emp_arun.employee_id,
                expertise_level="expert",
                is_primary_expert=True,
                years_of_experience=12,
                identified_by="nlp_extracted"
            ),
            KnowledgeExpert(
                knowledge_id=know_aws.knowledge_id,
                employee_id=emp_priya.employee_id,
                expertise_level="intermediate",
                is_primary_expert=False,
                years_of_experience=4,
                identified_by="nlp_extracted"
            )
        ])

        db.add_all([
            Entity(knowledge_id=know_aws.knowledge_id, document_id=doc_aws.document_id, entity_name="AWS RDS", entity_type="TECHNOLOGY", confidence=0.97),
            Entity(knowledge_id=know_aws.knowledge_id, document_id=doc_aws.document_id, entity_name="Arun Kumar", entity_type="PERSON", confidence=0.92),
            Entity(knowledge_id=know_aws.knowledge_id, document_id=doc_aws.document_id, entity_name="DMS", entity_type="TECHNOLOGY", confidence=0.91),
            Keyword(knowledge_id=know_aws.knowledge_id, keyword="migration", frequency=16, tf_idf_score=0.94),
            Keyword(knowledge_id=know_aws.knowledge_id, keyword="database", frequency=20, tf_idf_score=0.92),
            Keyword(knowledge_id=know_aws.knowledge_id, keyword="replication", frequency=9, tf_idf_score=0.86)
        ])

        # Exact Section 32 values: 95, 90, 85, 20, 33 -> 74.3
        score_val3 = calculate_risk_score(95, 90, 85, 20, 33)
        ml_res3 = predict_risk_level(95, 90, 85, 20, 33)
        risk_aws = RiskScore(
            organization_id=org.organization_id,
            knowledge_id=know_aws.knowledge_id,
            criticality=95.0,
            uniqueness=90.0,
            dependency=85.0,
            documentation_gap=20.0,
            availability_risk=33.0,
            risk_score=score_val3,
            risk_level=classify_risk_level(score_val3),
            ml_predicted_level=ml_res3["predicted_level"],
            ml_confidence=ml_res3["confidence"],
            prediction_model_version="1.0.0",
            assessment_method="rule_based",
            is_latest=True
        )
        db.add(risk_aws)

        db.add(PreservationAction(
            organization_id=org.organization_id,
            knowledge_id=know_aws.knowledge_id,
            action_type="secondary_expert",
            action_description="Train 2 additional database engineers in AWS DMS cutover procedures.",
            priority="high",
            status="recommended",
            assigned_to=user_arun.user_id,
            deadline=date(2026, 11, 20),
            estimated_hours=40,
            actual_hours=0
        ))

        emb3 = Embedding(
            knowledge_id=know_aws.knowledge_id,
            document_chunk_id=chunk_aws.chunk_id,
            embedding_model="all-MiniLM-L6-v2"
        )
        emb3.set_vector(generate_embedding(aws_chunk_text))
        db.add(emb3)

        # Commit everything
        db.commit()
        print("Database seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed()
