from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.services.groq_service import GroqService

class AnalysisService:

    @staticmethod
    def analyze_resume(db: Session, resume: Resume):
        # Use GroqService to analyze the resume
        result = GroqService.analyze_resume(resume.extracted_text)

        # Create a new ResumeAnalysis instance
        analysis = ResumeAnalysis(
            resume_id=resume.id,
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            summary=result.get("summary"),
            experience=result.get("experience"),
            education=result.get("education"),
            skills=result.get("skills", []),
            preferred_roles=result.get("preferred_roles", []),
            projects=result.get("projects", []),
            raw_response=result
        )

        # Save the analysis result to the database
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis
