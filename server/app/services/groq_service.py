import json
import re

from groq import Groq

from app.core.config import settings
from app.prompts.resume_prompt import RESUME_PROMPT


class GroqService:

    client = Groq(api_key=settings.GROQ_API_KEY,)

    MODEL = "openai/gpt-oss-120b"

    @classmethod
    def generate_json(cls, prompt: str):
        response = cls.client.chat.completions.create(
            model=cls.MODEL,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_object"
                }
        )
        text = response.choices[0].message.content.strip()

        text = (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            return json.loads(text)

        except json.JSONDecodeError:

            match = re.search(r"\{.*}", text, re.DOTALL)

            if match:
                return json.loads(match.group())
            raise Exception(f"Invalid JSON returned from Groq API:\n\n{text}")


    @classmethod
    def analyze_resume(cls, resume: str):
        prompt = RESUME_PROMPT.format(resume=resume)
        return cls.generate_json(prompt)
    