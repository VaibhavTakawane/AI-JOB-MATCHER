RECOMMENDATION_PROMPT = """
You are an ATS recruiter.

Return ONLY valid JSON.

Do not write explanations.
Do not write markdown.
Do not write text before or after the JSON.

{{
    "match_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "reason": ""
}}

Candidate:
{candidate}

Job:
{job}
"""
