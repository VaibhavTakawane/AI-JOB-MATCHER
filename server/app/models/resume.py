from datetime import datetime
from sqlalchemy import  String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base

class Resume(Base):
    __tablename__ = "resumes"

    id : Mapped[int] = mapped_column(primary_key=True)
    filename : Mapped[str] = mapped_column(String(255))
    file_path : Mapped[str] = mapped_column(String(500))
    extracted_text : Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    analysis = relationship("ResumeAnalysis", back_populates="resume", uselist=False)