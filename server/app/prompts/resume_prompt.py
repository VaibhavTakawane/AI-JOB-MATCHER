RESUME_PROMPT = """
You are an expert HR recruiter.

Analyze the resume and return ONLY valid JSON.

Return this structure:

{{
    "name":"",
    "email":"",
    "phone":"",
    "summary":"",
    "experience":"",
    "education":"",
    "skills":[],
    "preferred_roles":[],
    "projects":[]
}}

Resume:

{resume}
"""
