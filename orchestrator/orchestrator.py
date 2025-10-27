import os
import json
from typing import Dict, Any
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.critic_agent import CriticAgent
from utils.logger import get_logger

logger = get_logger("Orchestrator")

OUTPUT_DIR = os.path.join(os.getcwd(), "outputs")


class Orchestrator:
    def __init__(self):
        self.researcher = ResearchAgent()
        self.writer = WriterAgent()
        self.critic = CriticAgent()

    def _ensure_dir(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    def _safe_topic_slug(self, topic: str) -> str:
        slug = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in topic).strip()
        return slug.replace(" ", "_")[:100] or "topic"

    def run(self, topic: str) -> Dict[str, Any]:
        logger.info("Starting pipeline for topic: %s", topic)
        research = self.researcher.run(topic)
        writer_out = self.writer.run(research)
        draft = writer_out.get("draft", "")
        critic_out = self.critic.critique(draft, research)
        feedback = critic_out.get("feedback", "")

        slug = self._safe_topic_slug(topic)
        out_dir = os.path.join(OUTPUT_DIR, slug)
        self._ensure_dir(out_dir)

        files = {
            "research.json": research,
            "draft.txt": draft,
            "feedback.txt": feedback,
        }

        for fname, content in files.items():
            path = os.path.join(out_dir, fname)
            try:
                if fname.endswith(".json"):
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(content, f, indent=2, ensure_ascii=False)
                else:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content if isinstance(content, str) else str(content))
                logger.info("Wrote %s", path)
            except Exception as e:
                logger.error("Failed to write %s: %s", path, e)

        logger.info("Pipeline complete for: %s", topic)
        return {"topic": topic, "out_dir": out_dir, "research": research, "draft": draft, "feedback": feedback}
