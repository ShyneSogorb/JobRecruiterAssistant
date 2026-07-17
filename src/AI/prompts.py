from pydantic import BaseModel
import json
from modules.models.candidate_models import CandidateProfile
from modules.models.job_models import JobOffer
from src.ai.prompt_constants.json_rules import JSON_RULES_COMMON, JOB_OFFER_JSON_RULES
from src.ai.prompt_constants.cv_adapted_rules import CV_ADAPTER_RULES
from src.ai.prompt_constants.system_role import SYSTEM_PROMPT
from src.ai.prompt_constants.html_rules import HTML_RULES

class PromptBuilder:

    def __init__(self, language: str = "English") -> None:
        self.language = language


    
    def _build_cv_task(self) -> str:
        return """
            Generate a new CandidateProfile adapted to this job offer.

            Return ONLY the adapted CandidateProfile.
        """
    
    def _build_cv_html(self) -> str:
        return HTML_RULES
    
    def build_cv_adapter(self, profile: str, offer: JobOffer ) -> str:
        return "\n\n".join([
            self._build_system_prompt(),
            self._build_cv_adapter_rules(),
            self._build_json_rules(False),
            self._build_profile_prompt(profile),
            self._build_job_offer_model_prompt(offer),
            self._build_cv_task()
        ])
    
    def build_cv_html(self, profile: CandidateProfile, offer: JobOffer ) -> str:
        return "\n\n".join([
            self._build_profile_prompt(profile),
            self._build_job_offer_model_prompt(offer),
            self._build_cv_html()
        ])

    def _build_profile_prompt(self, profile: str | CandidateProfile ) -> str:
            result = "Candidate Profile:\n\n" 
            if type(profile) == str:
                result += profile
            elif type(profile) == CandidateProfile:
                result += profile.model_dump_json(indent=4)

            return result

    def _build_job_offer_model_prompt(self, offer: JobOffer) -> str:
        return (
            "Job Offer:\n\n"
            + offer.model_dump_json(indent=4)
        )

    def _build_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def _build_cv_adapter_rules(self)-> str:
        return CV_ADAPTER_RULES

    def _build_json_rules(self, job_offer_rules: bool) -> str:
        return "\n\n" + (JOB_OFFER_JSON_RULES if job_offer_rules else JSON_RULES_COMMON)

    def _build_offer_prompt(self, offer: str) -> str:
        return "Job Offer:\n\n" + offer