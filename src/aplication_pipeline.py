import os
from pathlib import Path
from typing import Callable

from pydantic import ValidationError
from modules.database.db_client import DbJobClient
from modules.utils.utility_library import symbols_removal

from modules.candidate_maker.candidatemaker import CandidateMakerPipeline
from modules.candidate_optimizer.candidateoptimizer import CandidateOptimizerPipeline
from src.ai.client import AIClient
from src.utils.cache import CacheManager
import src.utils.utils_library as Utils
from modules.models.candidate_models import CandidateProfile
from modules.models.job_models import JobOffer, TargetLanguage

import src.ai.static_prompts as StaticPrompts


from weasyprint import HTML
from src.ai.prompts_rules.candidate_parse import CV_EXTRACTOR_RULES
from src.ai.prompts_rules.role_rules import CV_PARSER_SYSTEM_PROMPT
from src.utils.logger import Logger

DEBUG = False

def get_candidate_path(language: str) -> str : return f"candidate/candidate.json"
CANDIDATE_EN_PATH = get_candidate_path("en")
CANDIDATE_ES_PATH = get_candidate_path("es")

class ApplicationPipeline:

    
    def __init__(self, ai: AIClient, cache: CacheManager, logger: Logger) -> None:
        self.ai = ai
        self.cache = cache
        self.logger = logger
        self.candidate_pipeline = CandidateMakerPipeline(self.ai, self.logger)
        self.optimizer_pipeline = CandidateOptimizerPipeline(self.ai, self.logger)
        pass

    @Utils.TimedFunction
    def _generate_and_save_candidate(self) -> CandidateProfile:
        self.logger.log("Generating the candidate from scratch")
        result = self.candidate_pipeline.build_candidate()
        self.logger.log("Candidate generated successfully")
        self.cache.save(result.model_dump_json(indent=4), CANDIDATE_EN_PATH)
        return result
    
    @Utils.TimedFunction
    def _get_candidate(self) -> CandidateProfile:

        self.logger.log("Trying to load candidate base from cache")
        candidate_data = self.cache.load(CANDIDATE_EN_PATH)
        if candidate_data == None:
            self.logger.log(f"Candidate could not be loaded from cache. File does not exists")
            result = self._generate_and_save_candidate()
            return result

        try:
            result = CandidateProfile.model_validate_json(str(self.cache.load(CANDIDATE_EN_PATH)))
            self.logger.log(f"Candidate {result.personal.name} loaded from cache successfully")
            return result
        
        except ValidationError:
            self.logger.log("The candidate could not be loaded from cache. JSON data was invalid")
            result = self._generate_and_save_candidate()
            return result
            
        

    @Utils.TimedFunction
    def _parse_job(self, description: str) -> JobOffer:

        if DEBUG:
            try:
                result = JobOffer.model_validate_json(str(self.cache.load("trabajo.json")))
                return result
            except ValidationError:
                ...

        self.logger.log("Parsing job")
        response = self.ai.ask(
        StaticPrompts.BuildJobDescriptionToJson(description),
            think=True,
            format=JobOffer.model_json_schema()
        )
        result = JobOffer.model_validate_json(response.message.content)
        self.logger.log(f"Job {result.role} successfully parsed")

        if DEBUG:
            self.cache.save(result.model_dump_json(), "trabajo.json")


        return result
    
    @Utils.TimedFunction
    def _select_match_candidate(self, job: JobOffer, candidate: CandidateProfile):
        self.logger.log(f"Making best match for {candidate.personal.name} as {job.role} at {job.company}")
        response = self.ai.ask(
            StaticPrompts.BuildCandidateJobAdapter(job.model_dump_json(), candidate.model_dump_json()),
            True,
            CandidateProfile.model_json_schema()
        )
        result = CandidateProfile.model_validate_json(response.message.content)
        self.logger.log(f"Best match for {candidate.personal.name} as {job.role} at {job.company} completed")
        return result

    @Utils.TimedFunction
    def _generate_html(self, candidate: CandidateProfile) -> str:
        self.logger.log(f"Generating a HTML-CV for {candidate.personal.name}")
        response = self.ai.ask(
            StaticPrompts.BuildCandidateJsonToHtml(candidate.model_dump_json()),
            True,
            None
        )
        result = response.message.content
        self.logger.log(f"HTML-CV for {candidate.personal.name} generated")
        return result
    
    @Utils.TimedFunction
    def _optimize_candidate(self, job: JobOffer, candidate: CandidateProfile) -> CandidateProfile:
        self.logger.log(f"Optimizing candidate {candidate.personal.name} for {job.role} at {job.company}")
        result = self.optimizer_pipeline.optimize(job, candidate)
        self.logger.log(f"Candidate {candidate.personal.name} successfully optimized for {job.role} at {job.company}")
        return result

    @Utils.TimedFunction
    def run(self, job:JobOffer) -> str:

        self.cache.save(job.model_dump_json(indent=4), "trabajo.json")

        candidate = self._get_candidate()
        self.cache.save(candidate.model_dump_json(indent=4), "candidato.json")

        #best_candidate = self._optimize_candidate(job, candidate)
        #self.cache.save(best_candidate.model_dump_json(indent=4), "mejor_candidato.json")

        #html = self._generate_html(best_candidate)
        html = self.cache.load("candidato.html")
        self.cache.save(html, "candidato.html")


        folder = Path(os.path.join("dist", f"{symbols_removal(job.role)}_at_{symbols_removal(job.company)}_position"))
        folder.mkdir(parents=True, exist_ok=True)

        pdf_target = os.path.join(folder, f"CV_{symbols_removal(candidate.personal.name)}.pdf")
        HTML(string=html).write_pdf(pdf_target)

        self.logger.log(f"Pdf generated successfully at {pdf_target}")

        return pdf_target


