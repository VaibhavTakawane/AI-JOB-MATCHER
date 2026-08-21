# from fastapi import APIRouter, Depends

# from app.database.db import get_db
# from sqlalchemy.orm import Session

# from app.services.recommendation_service import RecommendationService
# from app.schemas.resume import RecommendationResponse


# router = APIRouter()

# @router.post("/{resume_id}", response_model=list[RecommendationResponse])
# async def recommend_job(resume_id:int, db:Session = Depends(get_db)):
#     return RecommendationService.generate(db, resume_id)
from fastapi import APIRouter, Depends

from app.database.db import get_db
from sqlalchemy.orm import Session

from app.services.recommendation_service import RecommendationService
from app.schemas.resume import RecommendationResponse
from app.models.job import Job

router = APIRouter()


@router.post("/{resume_id}", response_model=list[RecommendationResponse])
async def recommend_job(resume_id: int, db: Session = Depends(get_db)):
    recommendations = RecommendationService.generate(db, resume_id)

    if not recommendations:
        return []

    # ONE query for all jobs instead of one query per recommendation
    job_ids = [rec.job_id for rec in recommendations]
    jobs = db.query(Job).filter(Job.id.in_(job_ids)).all()
    job_map = {job.id: job for job in jobs}

    result = []
    for rec in recommendations:
        job = job_map.get(rec.job_id)
        result.append({
            "id": rec.id,
            "resume_id": rec.resume_id,
            "job_id": rec.job_id,
            "match_score": rec.match_score,
            "matched_skills": rec.matched_skills,
            "missing_skills": rec.missing_skills,
            "reason": rec.reason,
            "title": job.title if job else None,
            "company": job.company if job else None,
            "location": job.location if job else None,
            "url": job.url if job else None,
            "salary": job.salary if job else None,
        })
    return result
