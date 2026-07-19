from modules.job.prompts import JobPromptBuilder
from modules.models.candidate_models import ListString
from modules.models.job_models import JobOffer
from src.ai.prompts import PromptBuilder
from src.ai.client import AIClient
from src.utils.logger import Logger

class JobOfferParser:

    def __init__(
        self,
        ai: AIClient
    ) -> None:
        self.ai = ai
        self.prompts = JobPromptBuilder()
        self.logger = Logger.get_global()

    def parse(self, offer: JobOffer) -> JobOffer:
        self.logger.log(f"Parsing job offer {offer.role} at {offer.company}")

        self.logger.log("Extracting offer skills")

        prompt = self.prompts.build_job_offer_parser(offer.model_dump_json(), JobOffer.model_json_schema())
        response = self.ai.ask(prompt, True, JobOffer.model_json_schema())
        result = JobOffer.model_validate_json(response.message.content)

        self.logger.log("Extracting ats-words")

        prompt = self.prompts.build_job_ats_extractor(result.model_dump_json())
        response = self.ai.ask(prompt, format=ListString.model_json_schema())
        result.ats_keywords = ListString.model_validate_json(response.message.content).array

        self.logger.log(f"Parsed job {result.role} at {result.company}")
        return result