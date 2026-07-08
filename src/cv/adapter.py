from src.ai.client import AIClient
from src.ai.prompts import PromptBuilder
from src.candidate.models import CandidateProfile
from src.jobs.models import JobOffer

class CVAdapter:

    def __init__(self, ai: AIClient, prompts: PromptBuilder) -> None:
        self.ai = ai
        self.prompts = prompts

    def adapt(
        self,
        profile: CandidateProfile,
        offer: JobOffer
    ) -> CandidateProfile:
        prompt = self.prompts.build_cv_adapter(profile, offer)
        response = self.ai.ask(prompt)
        return CandidateProfile.model_validate_json(response.message.content)
