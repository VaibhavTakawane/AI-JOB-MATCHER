from fastapi import APIRouter

from app.routers.auth_router import router as AuthRouter
from app.routers.resume_router import router as ResumeRouter
from app.routers.analysis_router import router as AnalysisRouter
from app.routers.jobs_router import router as jobsRouter
from app.routers.recommendation_router import router as recommendationRouter

api_router = APIRouter()

api_router.include_router(AuthRouter, prefix="/auth", tags=["Auth"])
api_router.include_router(ResumeRouter, prefix="/resumes", tags=["Resumes"])
api_router.include_router(AnalysisRouter, prefix="/analysis", tags=["Analysis"])
api_router.include_router(jobsRouter, prefix="/jobsRouter", tags=["jobsRouter"])
api_router.include_router(recommendationRouter, prefix="/recommendation", tags=["recommendation"])
