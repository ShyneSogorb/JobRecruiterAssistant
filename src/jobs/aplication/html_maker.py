from src.ai.client import AIClient
from src.ai.prompts import PromptBuilder
from modules.models.candidate_models import CandidateProfile
from modules.models.job_models import JobOffer


class HtmlCVMaker:
    def __init__(self, ai: AIClient, prompt: PromptBuilder) -> None:
        self.ai = ai
        self.prompt = prompt
        pass


    def generate_application(self, offer: JobOffer, candidate:CandidateProfile):
        prompt = self.prompt.build_cv_html(candidate, offer)
        response = self.ai.ask(prompt, True, None)
        return response.message.content



