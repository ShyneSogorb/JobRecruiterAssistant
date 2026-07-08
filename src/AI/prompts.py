from pydantic import BaseModel
import json
from src.candidate.models import CandidateProfile
from src.jobs.models import JobOffer
from src.ai.prompt_constants.json_rules import JSON_RULES
from src.ai.prompt_constants.cv_adapted_rules import CV_ADAPTER_RULES
from src.ai.prompt_constants.system_role import SYSTEM_PROMPT

class PromptBuilder:

    def __init__(self, language: str = "English") -> None:
        self.language = language

    def build_job_offer_parser(self, offer: str) -> str:

        return "\n\n".join([
            self._build_system_prompt(),
            self._build_json_rules(JobOffer),
            self._build_offer_prompt(offer)
        ])
    
    def _build_cv_task(self) -> str:
        return """
            Generate a new CandidateProfile adapted to this job offer.

            Return ONLY the adapted CandidateProfile.
        """
    
    def build_cv_adapter(self, profile: CandidateProfile, offer: JobOffer ) -> str:
        return "\n\n".join([
            self._build_system_prompt(),
            f"Output language: {self.language}",
            self._build_cv_adapter_rules(),
            self._build_json_rules(CandidateProfile),
            self._build_profile_prompt(profile),
            self._build_job_offer_model_prompt(offer),
            self._build_cv_task()
        ])
    
    def _build_profile_prompt(self, profile: CandidateProfile ) -> str:
            return (
                "Candidate Profile:\n\n"
                + profile.model_dump_json(indent=4)
            )

    def _build_job_offer_model_prompt(self, offer: JobOffer) -> str:
        return (
            "Job Offer:\n\n"
            + offer.model_dump_json(indent=4)
        )

    def _build_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def _build_cv_adapter_rules(self)-> str:
        return CV_ADAPTER_RULES

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