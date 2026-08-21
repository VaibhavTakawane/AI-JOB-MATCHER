from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id : Mapped[int] = mapped_column(primary_key=True)

    resume_id : Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    job_id : Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    match_score : Mapped[int]
    matched_skills : Mapped[list] = mapped_column(JSON)
    missing_skills : Mapped[list] = mapped_column(JSON)
    reason : Mapped[str]

    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)