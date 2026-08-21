from sqlalchemy.orm import Session
from app.models.job import Job

class JobService:

    @staticmethod
    def save_jobs(db:Session, jobs:list):
        saved = []

        for item in jobs:
            exists = db.query(Job).filter(Job.url == item["url"]).first()

            if exists:
                saved.append(exists)
                continue
            job = Job(**item)
            db.add(job)

            saved.append(job)
        db.commit()
        return saved