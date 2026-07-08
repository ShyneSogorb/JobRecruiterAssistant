from pydantic import BaseModel
import json
from src.jobs.models import JobOffer

SYSTEM_PROMPT = """
You are an expert technical recruiter specialised in software engineering and game development.
"""

JSON_RULES = """
Return ONLY valid JSON.

Extract technologies as individual skills.

Do not group multiple technologies into a single string.

Good:
["C++", "Python", "Linux"]

Bad:
["Extensive experience in C++ and Python"]

Keep skill names concise.

Use canonical names whenever possible.

Examples:
"C++17/C++20" -> "C++"
"Python 3" -> "Python"
"Git workflows" -> "Git"

The description field must contain the original job description, not a summary.

Do not include spoken languages in required_skills. Put them only in the languages field.

Do not use markdown.

Do not explain anything.

Follow exactly the JSON schema below.
"""

class PromptBuilder:

    def __init__(self, language: str = "English") -> None:
        self.language = language

    def build_job_offer_parser(self, offer: str) -> str:

        return "\n\n".join([
            self._build_system_prompt(),
            self._build_json_rules(JobOffer),
            self._build_offer_prompt(offer)
        ])

    def _build_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def _build_json_rules(self, model: type[BaseModel]) -> str:
        schema = json.dumps(
            model.model_json_schema(),
            indent=4
        )
        return "\n\n".join([
            JSON_RULES,
            schema
        ])

    def _build_offer_prompt(self, offer: str) -> str:
        return "Job Offer:\n\n" + offer