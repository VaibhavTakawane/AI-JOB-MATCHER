from datetime import datetime
from pydantic import BaseModel, ConfigDict

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    salary: str | None = None
    description: str | None = None
    url: str
    source: str

    model_config = ConfigDict(from_attributes=True)
