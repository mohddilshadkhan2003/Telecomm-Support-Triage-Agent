import re
from pathlib import Path

import yaml


class TriageEngine:
    def __init__(self, config_path: str = "config/settings.yaml"):
        base_dir = Path(__file__).resolve().parents[1]
        config_file = Path(config_path)

        if not config_file.is_absolute():
            config_file = base_dir / config_file

        with open(config_file, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file) or {}

        self.priority_scores = {
            "critical": 100,
            "high": 75,
            "medium": 50,
            "low": 25,
            "unclassified": 10,
        }

    def _clean_text(self, text: str) -> str:
        normalized = text.lower().replace("&", " and ")
        normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    def determine_category(self, text: str) -> str:
        cleaned_text = self._clean_text(text)
        categories = self.config.get("categories", {})

        for category, keywords in categories.items():
            if any(keyword.lower() in cleaned_text for keyword in keywords):
                return category

        return "general_inquiry"

    def determine_priority(self, text: str) -> tuple[str, int]:
        cleaned_text = self._clean_text(text)

        for priority_level in ["critical", "high", "medium", "low"]:
            keywords = self.config.get("priority_keywords", {}).get(priority_level, [])
            if any(keyword.lower() in cleaned_text for keyword in keywords):
                return priority_level, self.priority_scores[priority_level]

        return "unclassified", self.priority_scores["unclassified"]

    def get_auto_response(self, priority: str) -> str:
        responses = self.config.get("automated_responses", {})
        return responses.get(
            priority,
            responses.get("default", "Thank you for contacting Telecom Support. We will get back to you shortly."),
        )

    def analyze_query(self, query_text: str) -> dict:
        category = self.determine_category(query_text)
        priority, score = self.determine_priority(query_text)
        response = self.get_auto_response(priority)

        return {
            "category": category,
            "priority": priority,
            "priority_score": score,
            "automated_response": response,
        }
