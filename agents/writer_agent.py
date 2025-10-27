import os
from openai import OpenAI
from typing import Dict, Any
from utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger("WriterAgent")

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class WriterAgent:
    def __init__(self, model: str = DEFAULT_MODEL, tone: str = "informative"):
        self.model = model
        self.tone = tone
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found. Please set it in .env or environment.")
            raise ValueError("Missing OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def build_prompt(self, research: Dict[str, Any]) -> str:
        condensed = research.get("condensed", "")
        topic = research.get("topic")
        wiki = research.get("wikipedia", {})
        extras = []
        if wiki.get("title"):
            extras.append(f"Wikipedia: {wiki.get('title')} ({wiki.get('url')})")
        return (
            f"Write a clear, 400–600 word article on '{topic}'.\n"
            f"Tone: {self.tone}.\nUse the research below:\n\n"
            f"{condensed}\n\nAdditional sources:\n{chr(10).join(extras)}"
        )

    def run(self, research: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self.build_prompt(research)
        logger.info("WriterAgent generating draft for: %s", research.get("topic"))

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful and creative writer."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=900,
                temperature=0.6,
            )
            draft = resp.choices[0].message.content.strip()
            return {"draft": draft}
        except Exception as e:
            logger.error("WriterAgent failed: %s", e)
            return {"draft": "Error generating draft."}
