import os
import wikipedia
from openai import OpenAI
from typing import Dict, Any
from utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger("ResearchAgent")

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class ResearchAgent:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found. Please set it in .env or environment.")
            raise ValueError("Missing OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def lookup_wikipedia(self, topic: str, sentences: int = 5) -> Dict[str, Any]:
        try:
            page = wikipedia.page(topic)
            summary = wikipedia.summary(topic, sentences=sentences)
            return {"title": page.title, "url": page.url, "summary": summary}
        except Exception as e:
            logger.warning("Wikipedia lookup failed: %s", e)
            try:
                results = wikipedia.search(topic, results=3)
                return {"title": None, "url": None, "search_results": results, "summary": ""}
            except Exception as e2:
                logger.error("Wikipedia fallback failed: %s", e2)
                return {"title": None, "url": None, "summary": ""}

    def condense(self, raw_summary: str, topic: str) -> str:
        if not raw_summary:
            return f"No summary found for {topic}."

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a concise research summarizer."},
                    {"role": "user", "content": f"Summarize and list 3-5 key facts about '{topic}':\n{raw_summary}"},
                ],
                max_tokens=400,
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            logger.error("Condense failed: %s", e)
            return raw_summary

    def run(self, topic: str) -> Dict[str, Any]:
        logger.info("Researching topic: %s", topic)
        wiki = self.lookup_wikipedia(topic)
        condensed = self.condense(wiki.get("summary", ""), topic)
        return {"topic": topic, "wikipedia": wiki, "condensed": condensed}
