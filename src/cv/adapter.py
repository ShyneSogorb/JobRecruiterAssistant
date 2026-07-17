from src.ai.client import AIClient
from src.ai.prompts import PromptBuilder
from modules.models.candidate_models import CandidateProfile
from modules.models.job_models import JobOffer

class CVAdapter:

    def __init__(self, ai: AIClient, prompts: PromptBuilder) -> None:
        self.ai = ai
        self.prompts = prompts

    def adapt(
        self,
        # profile: CandidateProfile,
        profile: str,
        offer: JobOffer
    ) -> CandidateProfile:
        prompt = self.prompts.build_cv_adapter(profile, offer)
        response = self.ai.ask(prompt, True, CandidateProfile.model_json_schema())
        return CandidateProfile.model_validate_json(response.message.content)
