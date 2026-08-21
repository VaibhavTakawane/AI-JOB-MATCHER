import concurrent.futures

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.recommendation import Recommendation
from app.models.resume_analysis import ResumeAnalysis

from app.services.groq_service import GroqService
from app.prompts.recommendation_prompt import RECOMMENDATION_PROMPT

CANDIDATE_POOL_LIMIT = 50   # how many jobs we even bother scoring
MAX_RECOMMENDATIONS = 25    # how many best matches we keep/return
MAX_WORKERS = 10            # parallel Groq calls in flight at once


class RecommendationService:

    @staticmethod
    def _score_job(candidate_text: str, job: Job):
        """Score a single job against the candidate. Runs in a worker thread."""
        prompt = RECOMMENDATION_PROMPT.format(
            candidate=candidate_text,
            job={
                "title": job.title or "Software Developer",
                "company": job.company or "TCS",
                "description": job.description or "Give me jobs according to my title and company",
            }
        )
        try:
            result = GroqService.generate_json(prompt)
            return job, result
        except Exception:
            # one bad/slow Groq call shouldn't kill the whole batch
            return job, None

    @staticmethod
    def generate(db: Session, resume_id: int):
        analysis = (
            db.query(ResumeAnalysis)
            .filter(ResumeAnalysis.resume_id == resume_id)
            .first()
        )

        if analysis is None:
            return []

        # Only consider the most recent CANDIDATE_POOL_LIMIT jobs, not the whole table
        jobs = (
            db.query(Job)
            .order_by(Job.created_at.desc())
            .limit(CANDIDATE_POOL_LIMIT)
            .all()
        )

        scored = []

        # Fire Groq calls concurrently instead of one-by-one
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(RecommendationService._score_job,
                                analysis.raw_response, job)
                for job in jobs
            ]
            for future in concurrent.futures.as_completed(futures):
                job, result = future.result()
                if result is not None:
                    scored.append((job, result))

        # Rank by match_score and keep only the top MAX_RECOMMENDATIONS
        scored.sort(key=lambda pair: pair[1].get(
            "match_score", 0), reverse=True)
        top = scored[:MAX_RECOMMENDATIONS]

        recommendation = []
        for job, result in top:
            recommended = Recommendation(
                resume_id=resume_id,
                job_id=job.id,
                match_score=result["match_score"],
                matched_skills=result["matched_skills"],
                missing_skills=result["missing_skills"],
                reason=result["reason"]
            )
            db.add(recommended)
            recommendation.append(recommended)

        db.commit()

        return recommendation
