from fastapi import APIRouter
from app.api.v1 import auth, documents, knowledge, risk, ml, search, preservation, employees, audit

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(knowledge.router)
api_router.include_router(risk.router)
api_router.include_router(ml.router)
api_router.include_router(search.router)
api_router.include_router(preservation.router)
api_router.include_router(employees.router)
api_router.include_router(audit.router)
