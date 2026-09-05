from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.resume import JobResponse  # NEW

from app.models.resume_analysis import ResumeAnalysis
from app.services.job_scraper_service import JobScraper
from app.services.job_service import JobService

router = APIRouter()


# CHANGED
@router.post("/search/{resume_id}", response_model=list[JobResponse])
def search_job(resume_id: int, db: Session = Depends(get_db)):
    analysis = (db.query(ResumeAnalysis).filter(
        ResumeAnalysis.resume_id == resume_id).first())

    if analysis is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    role = (analysis.preferred_roles[0]
            if analysis.preferred_roles and len(analysis.preferred_roles) > 0
            else "Software Developer"
            )

    # jobs = JobScraper.search(role)
    try:
        jobs = JobScraper.search(role)
    except Exception as e:
        print(f"JOB SEARCH ERROR: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Job search failed: {str(e)}"
    )
    saved = JobService.save_jobs(db, jobs)

    return saved
