import json
from typing import List, Dict, Any

class WatsonxParser:
    @staticmethod
    def parse_ideas(raw_output: str) -> List[Dict[str, Any]]:
        """
        Parses the raw string output from Watsonx into a list of Idea dictionaries.
        Strips markdown wrappers if present.
        """
        cleaned = raw_output.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "", 1)
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict) and "ideas" in parsed:
                return parsed["ideas"]
            if isinstance(parsed, list):
                return parsed
            return []
        except json.JSONDecodeError:
            # Fallback if the LLM completely fails to produce valid JSON
            return []
