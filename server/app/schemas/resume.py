from datetime import datetime
from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    filename: str
    created_at: datetime


class RecommendationResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    match_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    reason: str

    # NEW: real job data from DB
    title: str | None = None
    company: str | None = None
    location: str | None = None
    url: str | None = None
    salary: str | None = None

    model_config = {"from_attributes": True}


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    salary: str | None = None
    url: str
    source: str
    description: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
