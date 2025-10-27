import os
from openai import OpenAI
from typing import Dict, Any
from utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger("CriticAgent")

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class CriticAgent:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found. Please set it in .env or environment.")
            raise ValueError("Missing OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def critique(self, draft: str, research: Dict[str, Any]) -> Dict[str, str]:
        messages = [
            {"role": "system", "content": "You are a helpful critic that provides actionable feedback."},
            {
                "role": "user",
                "content": (
                    "Review the following draft:\n\n"
                    f"{draft}\n\nResearch summary:\n{research.get('condensed', '')}\n\n"
                    "Provide:\n"
                    "1. A brief summary (1–2 lines)\n"
                    "2. 3 strengths\n"
                    "3. 3 improvements\n"
                    "4. A short revised example paragraph."
                ),
            },
        ]

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=600,
                temperature=0.3,
            )
            feedback = resp.choices[0].message.content.strip()
            return {"feedback": feedback}
        except Exception as e:
            logger.error("CriticAgent failed: %s", e)
            return {"feedback": "Error generating feedback."}
