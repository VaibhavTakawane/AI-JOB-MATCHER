from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.resume import Resume
from app.services.analysis_service import AnalysisService

router = APIRouter()

@router.post("/{resume_id}")
def analyze_resume(resume_id: int, db: Session = Depends(get_db)):
    # Fetch the resume from the database
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Analyze the resume using the AnalysisService
    analysis = AnalysisService.analyze_resume(db, resume)

    return analysis
