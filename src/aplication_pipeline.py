import os
from pathlib import Path

from pydantic import ValidationError
from modules.introduction_maker.introduction_maker import IntoductionMaker
from modules.translator.translator import Translator
from modules.utils.utility_library import symbols_removal

from modules.candidate_maker.candidatemaker import CandidateMakerPipeline
from modules.candidate_optimizer.candidateoptimizer import CandidateOptimizerPipeline
from src.ai.client import AIClient
from src.utils.cache import CacheManager
import src.utils.utils_library as Utils
from modules.models.candidate_models import CandidateProfile
from modules.models.job_models import EJobState, JobApplication, JobOffer, TargetLanguage

import src.ai.static_prompts as StaticPrompts


from weasyprint import HTML
from src.utils.logger import Logger

DEBUG = False

CANDIDATE_PATH = f"candidate/candidate.json"

class ApplicationPipeline:

    
    def __init__(self, ai: AIClient, cache: CacheManager, logger: Logger) -> None:
        self.ai = ai
        self.cache = cache
        self.logger = logger
        self.candidate_pipeline = CandidateMakerPipeline(self.ai, self.logger)
        self.optimizer_pipeline = CandidateOptimizerPipeline(self.ai, self.logger)
        self.translator = Translator(self.ai, self.logger)
        self.introducer = IntoductionMaker(self.ai, self.logger)

    @Utils.TimedFunction
    def _generate_and_save_candidate(self) -> CandidateProfile:
        self.logger.log("Generating the candidate from scratch")
        result = self.candidate_pipeline.build_candidate()
        self.logger.log("Candidate generated successfully")
        self.cache.save(result.model_dump_json(indent=4), CANDIDATE_PATH)
        return result
    
    @Utils.TimedFunction
    def _get_candidate(self) -> CandidateProfile:

        self.logger.log("Trying to load candidate base from cache")
        candidate_data = self.cache.load(CANDIDATE_PATH)
        if candidate_data == None:
            self.logger.log(f"Candidate could not be loaded from cache. File does not exists")
            result = self._generate_and_save_candidate()
            return result

        try:
            result = CandidateProfile.model_validate_json(str(self.cache.load(CANDIDATE_PATH)))
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
    def _deduce_language(self, job: JobOffer, candidate: CandidateProfile) -> CandidateProfile:
        self.logger.log(f"Optimizing candidate {candidate.personal.name} for {job.role} at {job.company}")
        result = self.optimizer_pipeline.optimize(job, candidate)
        self.logger.log(f"Candidate {candidate.personal.name} successfully optimized for {job.role} at {job.company}")
        return result

    @Utils.TimedFunction
    def run(self, app:JobApplication) -> JobApplication:

        self.cache.save(app.job.model_dump_json(indent=4), "trabajo.json")

        candidate = self._get_candidate()
        self.cache.save(candidate.model_dump_json(indent=4), "candidato.json")

        best_candidate = self._optimize_candidate(app.job, candidate)
        self.cache.save(best_candidate.model_dump_json(indent=4), "mejor_candidato.json")

        html = self._generate_html(best_candidate)
        #html = self.cache.load("candidato.html")
        self.cache.save(html, "candidato.html")

        cover_letter=self.introducer.build_cover_letter_text(app.job, best_candidate)
        hiring_manager=self.introducer.build_hiring_manager_text(app.job, best_candidate)

        app.salary = self.introducer.calculate_salary(app.job, html)
        app.score = self.introducer.calculate_match(app.job, html)

        if app.job.target_language != TargetLanguage.English:
            html            =self.translator.translate_html(html,               app.job.target_language)
            cover_letter    =self.translator.translate_text(cover_letter,       app.job.target_language)
            hiring_manager  =self.translator.translate_text(hiring_manager,     app.job.target_language)

        app.cv = html

        folder = Path(os.path.join("dist", f"{symbols_removal(app.job.role)}_at_{symbols_removal(app.job.company)}_position"))
        folder.mkdir(parents=True, exist_ok=True)

        pdf_target = os.path.join(folder, f"CV_{symbols_removal(candidate.personal.name)}.pdf")
        HTML(string=html).write_pdf(pdf_target)
        
        app.cover_letter=cover_letter
        app.hiring_manager=hiring_manager

        app.cv_path = os.path.abspath(pdf_target)

        self.logger.log(f"Pdf generated successfully at {pdf_target}")

        app.state = EJobState.READY
        return app


