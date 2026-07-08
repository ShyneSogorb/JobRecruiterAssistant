from src.jobs.models import JobOffer
from src.ai.prompts import PromptBuilder
from src.ai.client import AIClient

class JobOfferParser:

    def __init__(
        self,
        ai: AIClient,
        prompts: PromptBuilder
    ) -> None:
        self.ai = ai
        self.prompts = prompts

    def parse(self, offer: str) -> JobOffer:
        prompt = self.prompts.build_job_offer_parser(offer)
        response = self.ai.ask(prompt)
        return JobOffer.model_validate_json(response.message.content)